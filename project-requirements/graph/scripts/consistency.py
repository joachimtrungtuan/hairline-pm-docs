"""Cross-FR consistency checks over the requirements graph DB (read-only).

Each check returns (columns, rows); query.py exposes them as the commands boundary, ownership, flow,
joins and coverage. Only active nodes count. A row is a finding for a person to decide, not an error:
the checks cannot tell an intended sharing of data from an accidental one.

Stage order is known only inside one timeline (attrs.sequence). Two Stages on different timelines are
never treated as "earlier" or "later" than each other.
"""

from __future__ import annotations

import json
import re
import sqlite3
from collections import defaultdict
from typing import Any

Rows = tuple[list[str], list[dict[str, Any]]]

SAMPLE_SIZE = 3


def _active(conn: sqlite3.Connection, node_type: str) -> dict[str, dict[str, Any]]:
    rows = conn.execute(
        "SELECT id, owner_fr, title, attrs FROM nodes WHERE type = ? AND status = 'active'", (node_type,))
    return {r[0]: {"id": r[0], "owner_fr": r[1], "title": r[2], "attrs": json.loads(r[3])} for r in rows}


def _edges(conn: sqlite3.Connection, verb: str) -> list[tuple[str, str]]:
    """Edges of one verb whose two ends are both active."""
    return [tuple(r) for r in conn.execute(
        "SELECT e.from_id, e.to_id FROM edges e"
        " JOIN nodes a ON a.id = e.from_id AND a.status = 'active'"
        " JOIN nodes b ON b.id = e.to_id AND b.status = 'active'"
        " WHERE e.verb = ? ORDER BY e.from_id, e.to_id", (verb,))]


def _referenced_pairs(conn: sqlite3.Connection) -> set[tuple[str, str]]:
    """(FR-A, FR-B) where FR-A has a references edge to an active Rule owned by FR-B."""
    return {tuple(r) for r in conn.execute(
        "SELECT e.from_id, r.owner_fr FROM edges e JOIN nodes r ON r.id = e.to_id AND r.status = 'active'"
        " WHERE e.verb = 'references' AND r.owner_fr IS NOT NULL")}


def boundary(conn: sqlite3.Connection) -> Rows:
    """FR pairs where one FR's Screens show, or Rules apply to, data another FR owns, with no references edge.

    A Field counts as owned by the FR that owns its Entity.
    """
    referenced = _referenced_pairs(conn)
    found: dict[tuple[str, str, str], list[str]] = defaultdict(list)
    shows = conn.execute(
        "SELECT s.owner_fr, ent.owner_fr, s.id || ' shows ' || f.id FROM edges e"
        " JOIN nodes s ON s.id = e.from_id AND s.status = 'active'"
        " JOIN nodes fn ON fn.id = e.to_id AND fn.status = 'active'"
        " JOIN fields f ON f.id = e.to_id"
        " JOIN nodes ent ON ent.id = f.entity_id AND ent.status = 'active'"
        " WHERE e.verb = 'shows' AND s.owner_fr <> ent.owner_fr ORDER BY s.id, f.id")
    for from_fr, to_fr, sample in shows:
        found[("screen shows field", from_fr, to_fr)].append(sample)
    applies = conn.execute(
        "SELECT r.owner_fr, coalesce(ent.owner_fr, t.owner_fr), r.id || ' applies to ' || t.id FROM edges e"
        " JOIN nodes r ON r.id = e.from_id AND r.status = 'active' AND r.type = 'Rule'"
        " JOIN nodes t ON t.id = e.to_id AND t.status = 'active' AND t.type IN ('Entity', 'Field')"
        " LEFT JOIN fields f ON f.id = t.id"
        " LEFT JOIN nodes ent ON ent.id = f.entity_id"
        " WHERE e.verb = 'applies to' AND r.owner_fr <> coalesce(ent.owner_fr, t.owner_fr) ORDER BY r.id, t.id")
    for from_fr, to_fr, sample in applies:
        found[("rule applies to data", from_fr, to_fr)].append(sample)
    rows = [
        {"kind": kind, "from_fr": from_fr, "data_owner_fr": to_fr, "links": len(samples), "sample": samples[:SAMPLE_SIZE]}
        for (kind, from_fr, to_fr), samples in sorted(found.items())
        if (from_fr, to_fr) not in referenced
    ]
    return ["kind", "from_fr", "data_owner_fr", "links", "sample"], rows


def _name_key(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", title.lower())


def ownership(conn: sqlite3.Connection) -> Rows:
    """Entities, Settings or Events that two FRs appear to own, and Fields owned apart from their Entity."""
    rows: list[dict[str, Any]] = []
    for node_type in ("Entity", "Event", "Setting"):
        nodes = _active(conn, node_type)
        groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
        for node in nodes.values():
            groups[("same name", _name_key(node["title"]))].append(node)
            table = node["attrs"].get("table")
            if node_type == "Entity" and table:
                groups[("same table", table.lower())].append(node)
        for (kind, key), members in sorted(groups.items()):
            owners = sorted({m["owner_fr"] for m in members if m["owner_fr"]})
            if key and len(owners) > 1:
                rows.append({"kind": f"{kind}, different owners", "type": node_type, "name": key,
                             "owners": owners, "nodes": sorted(m["id"] for m in members)})
    mismatched = conn.execute(
        "SELECT f.id, fn.owner_fr, ent.id, ent.owner_fr FROM fields f"
        " JOIN nodes fn ON fn.id = f.id AND fn.status = 'active'"
        " JOIN nodes ent ON ent.id = f.entity_id AND ent.status = 'active'"
        " WHERE fn.owner_fr IS NOT ent.owner_fr ORDER BY f.id")
    for field_id, field_owner, entity_id, entity_owner in mismatched:
        rows.append({"kind": "field owner differs from entity owner", "type": "Field", "name": field_id,
                     "owners": [o for o in (field_owner, entity_owner) if o], "nodes": [field_id, entity_id]})
    return ["kind", "type", "name", "owners", "nodes"], rows


class _Stages:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.nodes = _active(conn, "Stage")

    def position(self, stage_id: str) -> tuple[str | None, int]:
        attrs = self.nodes[stage_id]["attrs"]
        return attrs.get("timeline"), int(attrs.get("sequence", 0))

    def before(self, a: str, b: str) -> bool:
        """a is earlier than b on the same timeline."""
        (timeline_a, seq_a), (timeline_b, seq_b) = self.position(a), self.position(b)
        return timeline_a == timeline_b and seq_a < seq_b

    def upstream(self, stage_id: str) -> set[str]:
        """The Stage itself and every earlier Stage on its timeline."""
        return {s for s in self.nodes if s == stage_id or self.before(s, stage_id)}

    def ordered(self) -> list[str]:
        return sorted(self.nodes, key=lambda s: (self.position(s)[0] or "", self.position(s)[1], s))


def _by_target(pairs: list[tuple[str, str]]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = defaultdict(list)
    for source, target in pairs:
        grouped[target].append(source)
    return grouped


def flow(conn: sqlite3.Connection) -> Rows:
    """Events nothing consumes, Entities written but never read (or the reverse), and Stages that read nothing."""
    stages = _Stages(conn)
    rows: list[dict[str, Any]] = []
    emitted = _by_target(_edges(conn, "emits"))
    applies_at = defaultdict(list)
    for rule_id, stage_id in _edges(conn, "applies at"):
        applies_at[rule_id].append(stage_id)
    consumers = defaultdict(list)
    for rule_id, target in conn.execute(
            "SELECT e.from_id, e.to_id FROM edges e"
            " JOIN nodes r ON r.id = e.from_id AND r.status = 'active' AND r.type = 'Rule'"
            " JOIN nodes t ON t.id = e.to_id AND t.status = 'active' AND t.type = 'Event'"
            " WHERE e.verb = 'applies to' ORDER BY e.from_id"):
        consumers[target].append(rule_id)
    events = _active(conn, "Event")
    for event_id in sorted(emitted):
        emit_stages = sorted(emitted[event_id])
        rules = consumers.get(event_id, [])
        if not rules:
            rows.append({"kind": "event emitted, no rule applies to it", "node": event_id,
                         "owner_fr": events[event_id]["owner_fr"], "stages": emit_stages, "detail": []})
            continue
        rule_stages = [s for r in rules for s in applies_at.get(r, [])]
        if rule_stages and all(stages.before(s, e) for s in rule_stages for e in emit_stages):
            rows.append({"kind": "event consumed only at earlier stages", "node": event_id,
                         "owner_fr": events[event_id]["owner_fr"], "stages": emit_stages,
                         "detail": sorted(set(rule_stages))})
    written = _by_target(_edges(conn, "writes"))
    read = _by_target(_edges(conn, "reads"))
    for entity_id, entity in sorted(_active(conn, "Entity").items()):
        writes, reads = sorted(written.get(entity_id, [])), sorted(read.get(entity_id, []))
        if writes and not reads:
            kind = "entity written, never read"
        elif reads and not writes:
            kind = "entity read, never written"
        elif not reads and not writes:
            kind = "entity neither read nor written at any stage"
        elif all(stages.before(r, w) for r in reads for w in writes):
            kind = "entity read only before it is written"
        else:
            continue
        rows.append({"kind": kind, "node": entity_id, "owner_fr": entity["owner_fr"],
                     "stages": writes, "detail": reads})
    reading = {stage_id for stage_id, _ in _edges(conn, "reads")}
    counts = {verb: defaultdict(int) for verb in ("writes", "emits")}
    for verb, tally in counts.items():
        for stage_id, _ in _edges(conn, verb):
            tally[stage_id] += 1
    rules_at = defaultdict(int)
    for stage_list in applies_at.values():
        for stage_id in stage_list:
            rules_at[stage_id] += 1
    for stage_id in stages.ordered():
        if stage_id not in reading:
            rows.append({"kind": "stage reads no data", "node": stage_id, "owner_fr": None, "stages": [],
                         "detail": [f"writes {counts['writes'][stage_id]}", f"emits {counts['emits'][stage_id]}",
                                    f"rules {rules_at[stage_id]}"]})
    return ["kind", "node", "owner_fr", "stages", "detail"], rows


def joins(conn: sqlite3.Connection) -> Rows:
    """Whether the Stages linked across timelines carry the data they need.

    "A enters from B": every Entity read at A should be written at A, at B, or earlier on either timeline.
    "A joins B": something written on A's timeline up to A should be read at B.
    """
    stages = _Stages(conn)
    writes_at, reads_at = defaultdict(set), defaultdict(set)
    for stage_id, entity_id in _edges(conn, "writes"):
        writes_at[stage_id].add(entity_id)
    for stage_id, entity_id in _edges(conn, "reads"):
        reads_at[stage_id].add(entity_id)

    def written_upstream(stage_id: str) -> set[str]:
        return {e for s in stages.upstream(stage_id) for e in writes_at[s]}

    rows: list[dict[str, Any]] = []
    for entry, source in _edges(conn, "enters from"):
        link = f"{entry} enters from {source}"
        available = written_upstream(entry) | written_upstream(source)
        missing = sorted(reads_at[entry] - available)
        for entity_id in missing:
            rows.append({"link": link, "kind": "read at entry, not written upstream", "entity": entity_id})
        if not reads_at[entry]:
            rows.append({"link": link, "kind": "entry stage reads no data", "entity": None})
    for joining, joined in _edges(conn, "joins"):
        link = f"{joining} joins {joined}"
        if not written_upstream(joining) & reads_at[joined]:
            rows.append({"link": link, "kind": "join carries no data the joined stage reads", "entity": None})
    return ["link", "kind", "entity"], rows


def coverage(conn: sqlite3.Connection) -> Rows:
    """Screens no Actor uses, Stages no Actor acts in, and Rules tied to no Stage (unless scope is global)."""
    rows: list[dict[str, Any]] = []
    used = {screen_id for _, screen_id in _edges(conn, "uses")}
    for screen_id, screen in sorted(_active(conn, "Screen").items()):
        if screen_id not in used:
            rows.append({"kind": "screen without actor", "node": screen_id, "owner_fr": screen["owner_fr"],
                         "title": screen["title"]})
    acted = {stage_id for _, stage_id in _edges(conn, "acts in")}
    stages = _Stages(conn)
    for stage_id in stages.ordered():
        if stage_id not in acted:
            rows.append({"kind": "stage without actor", "node": stage_id, "owner_fr": None,
                         "title": stages.nodes[stage_id]["title"]})
    staged = {rule_id for rule_id, _ in _edges(conn, "applies at")}
    for rule_id, rule in sorted(_active(conn, "Rule").items()):
        if rule_id not in staged and rule["attrs"].get("scope") != "global":
            rows.append({"kind": "rule without stage", "node": rule_id, "owner_fr": rule["owner_fr"],
                         "title": rule["title"]})
    return ["kind", "node", "owner_fr", "title"], rows


CHECKS = {"boundary": boundary, "ownership": ownership, "flow": flow, "joins": joins, "coverage": coverage}
