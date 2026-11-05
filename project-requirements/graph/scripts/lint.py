"""Check the whole requirements graph against its guardrails.

Usage: lint.py [--db DB_PATH] [--fr FR-NNN] [--json]

Prints one row per finding and exits 1 if there is any finding, 0 if the graph is clean,
2 on a usage or database error. Every finding has a stable ID, rule code plus subject
(for example L03:SCR-004-01), so finding counts can be compared between runs.

Only current requirements are checked: retired nodes, and edges with a retired end, are
history and are skipped. --fr keeps findings whose subject node is owned by that FR, so
findings about unowned nodes (Stages, Actors, Sources, and L01 missing-owner findings)
never appear with it.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Any

from common import DEFAULT_DB_PATH, Edge, Graph, Node, Schema, SchemaError, load_graph, load_schema, open_db, validate_fr

RULES: dict[str, str] = {
    "L01": "node lacks an owning FR or an attribute that its type requires in schema.yaml",
    "L02": "Rule applies at no Stage",
    "L03": "Screen shows a non-Field, or shows nothing",
    "L04": "Event does not have exactly one producer Stage",
    "L05": "Field calculated_by column and 'calculated by' edge disagree",
    "L06": "edge verb not allowed for its node-type pair",
    "L07": "'shows' edge has a missing or invalid provenance",
    "L08": "Stage timeline structure is broken: follows nothing, follows across timelines, "
           "shares a sequence, or a parallel timeline with a standalone entry has no Stage that enters from "
           "or joins another Stage",
    "L09": "Entity has no Fields",
    "L10": "Rule or Entity has no 'decided by' Source",
    "L11": "Field node has no row in the fields table",
}

MAIN_TIMELINE = "main"


@dataclass(frozen=True)
class Finding:
    rule: str
    key: str  # node ID, or a from>verb>to key for edge findings
    node_id: str  # subject node, used for the --fr filter
    message: str

    @property
    def id(self) -> str:
        return f"{self.rule}:{self.key}"

    def as_dict(self) -> dict[str, str]:
        return {"id": self.id, "rule": self.rule, "node_id": self.node_id, "message": self.message}


def edge_key(e: Edge) -> str:
    return f"{e.from_id}>{e.verb.replace(' ', '-')}>{e.to_id}"


def check_l01(g: Graph, schema: Schema) -> list[Finding]:
    out = []
    for n in g.active.values():
        spec = schema.node_types.get(n.type)
        if spec is None:
            continue
        if spec.owner_fr == "required" and not n.owner_fr:
            out.append(Finding("L01", n.id, n.id, f"{n.type} {n.id} has no owning FR"))
        for attr in sorted(spec.attrs.required):
            if attr not in n.attrs:
                out.append(Finding("L01", f"{n.id}#{attr}", n.id, f"{n.type} {n.id} lacks required attribute {attr!r}"))
    return out


def check_l02(g: Graph) -> list[Finding]:
    applies = g.out("applies at")
    out = []
    for n in g.of_type("Rule"):
        if not any(g.active[e.to_id].type == "Stage" for e in applies.get(n.id, [])):
            out.append(Finding("L02", n.id, n.id, f"Rule {n.id} applies at no active Stage"))
    return out


def check_l03(g: Graph) -> list[Finding]:
    shows = g.out("shows")
    out = []
    for n in g.of_type("Screen"):
        edges = shows.get(n.id, [])
        if not edges:
            out.append(Finding("L03", n.id, n.id, f"Screen {n.id} has no 'shows' edges"))
        for e in edges:
            target = g.active[e.to_id]
            if target.type != "Field":
                out.append(Finding("L03", f"{n.id}>{e.to_id}", n.id, f"Screen {n.id} shows {target.type} {e.to_id}, not a Field"))
    return out


def check_l04(g: Graph) -> list[Finding]:
    emits = g.into("emits")
    out = []
    for n in g.of_type("Event"):
        producers = sorted(e.from_id for e in emits.get(n.id, []) if g.active[e.from_id].type == "Stage")
        if len(producers) != 1:
            detail = "no producer Stage" if not producers else f"{len(producers)} producer Stages: {', '.join(producers)}"
            out.append(Finding("L04", n.id, n.id, f"Event {n.id} has {detail}"))
    return out


def check_l05(g: Graph) -> list[Finding]:
    # Compared on all edges, retired ends included: this checks two copies of one fact stay in sync.
    edge_targets: dict[str, set[str]] = defaultdict(set)
    for e in g.edges:
        if e.verb == "calculated by":
            edge_targets[e.from_id].add(e.to_id)
    out = []
    for n in g.of_type("Field"):
        column = g.calculated_by.get(n.id)
        expected = {column} if column else set()
        actual = edge_targets.get(n.id, set())
        if expected != actual:
            out.append(Finding(
                "L05", n.id, n.id,
                f"Field {n.id}: calculated_by column is {column or 'empty'}, "
                f"'calculated by' edges point at {', '.join(sorted(actual)) or 'nothing'}",
            ))
    return out


def check_l06(g: Graph, schema: Schema) -> list[Finding]:
    out = []
    for e in g.live_edges:
        pair = (g.active[e.from_id].type, g.active[e.to_id].type)
        verb = schema.edge_verbs.get(e.verb)
        if verb is None or pair not in verb.pairs:
            allowed = ", ".join(f"{a}->{b}" for a, b in sorted(verb.pairs)) if verb else "verb not in schema.yaml"
            out.append(Finding("L06", edge_key(e), e.from_id, f"'{e.verb}' cannot join {pair[0]} -> {pair[1]} (allowed: {allowed})"))
    return out


def check_l07(g: Graph, schema: Schema) -> list[Finding]:
    allowed = set(schema.enum("provenance"))
    out = []
    for e in g.live_edges:
        if e.verb != "shows":
            continue
        value = e.attrs.get("provenance")
        if value is None:
            out.append(Finding("L07", edge_key(e), e.from_id, f"{e.from_id} shows {e.to_id} without a provenance"))
        elif value not in allowed:
            out.append(Finding("L07", edge_key(e), e.from_id, f"{e.from_id} shows {e.to_id} with invalid provenance {value!r}"))
    return out


def _sequence_order(n: Node) -> tuple[int, str]:
    """Sort key for Stages: by sequence, a missing or non-integer sequence last, then by ID."""
    sequence = n.attrs.get("sequence")
    return (sequence if type(sequence) is int else sys.maxsize, n.id)


def check_l08(g: Graph) -> list[Finding]:
    follows = g.out("follows")
    stages = g.of_type("Stage")
    out = []
    for n in stages:
        sequence = n.attrs.get("sequence")
        is_first = type(sequence) is int and sequence == 1
        if is_first or n.attrs.get("standalone_entry") is True:
            continue
        if not any(g.active[e.to_id].type == "Stage" for e in follows.get(n.id, [])):
            out.append(Finding("L08", n.id, n.id, f"Stage {n.id} (sequence {sequence}) follows no Stage and is not a standalone entry"))

    for n in stages:
        for e in follows.get(n.id, []):
            target = g.active[e.to_id]
            if target.type != "Stage":
                continue
            own, other = n.attrs.get("timeline"), target.attrs.get("timeline")
            if own != other:
                out.append(Finding(
                    "L08", edge_key(e), n.id,
                    f"Stage {n.id} (timeline {own}) follows {target.id} on a different timeline ({other})",
                ))

    by_slot: dict[tuple[str, int], list[str]] = defaultdict(list)
    for n in stages:
        timeline, sequence = n.attrs.get("timeline"), n.attrs.get("sequence")
        if isinstance(timeline, str) and type(sequence) is int:
            by_slot[(timeline, sequence)].append(n.id)
    for (timeline, sequence), ids in by_slot.items():
        if len(ids) > 1:
            ids.sort()
            out.append(Finding(
                "L08", "+".join(ids), ids[0],
                f"Stages {', '.join(ids)} share sequence {sequence} on timeline {timeline}",
            ))

    # A parallel timeline that can start on its own (it has a standalone entry) must still link to
    # another timeline somewhere; any of its Stages may carry the link. Account timelines have no
    # standalone entry and are not checked.
    by_timeline: dict[str, list[Node]] = defaultdict(list)
    for n in stages:
        timeline = n.attrs.get("timeline")
        if isinstance(timeline, str) and timeline != MAIN_TIMELINE:
            by_timeline[timeline].append(n)
    for timeline, members in by_timeline.items():
        if not any(n.attrs.get("standalone_entry") is True for n in members):
            continue
        if any(
            g.active[e.to_id].type == "Stage"
            for n in members
            for e in g.edges_from(n.id, "enters from") + g.edges_from(n.id, "joins")
        ):
            continue
        first = min(members, key=_sequence_order)
        out.append(Finding(
            "L08", first.id, first.id,
            f"Timeline {timeline} has no Stage with an 'enters from' or 'joins' edge to a Stage",
        ))
    return out


def check_l09(g: Graph) -> list[Finding]:
    with_fields = {entity for fid, entity in g.entity_of.items() if fid in g.active}
    return [
        Finding("L09", n.id, n.id, f"Entity {n.id} has no active Fields")
        for n in g.of_type("Entity")
        if n.id not in with_fields
    ]


def check_l10(g: Graph) -> list[Finding]:
    decided = g.out("decided by")
    out = []
    for n in g.of_type("Rule") + g.of_type("Entity"):
        if not any(g.active[e.to_id].type == "Source" for e in decided.get(n.id, [])):
            out.append(Finding("L10", n.id, n.id, f"{n.type} {n.id} has no 'decided by' Source"))
    return out


def check_l11(g: Graph) -> list[Finding]:
    return [
        Finding("L11", n.id, n.id, f"Field {n.id} has no row in the fields table")
        for n in g.of_type("Field")
        if n.id not in g.entity_of
    ]


def lint(conn: sqlite3.Connection, schema: Schema, fr: str | None = None) -> list[Finding]:
    """Run every rule and return findings sorted by ID. With fr, keep findings whose subject that FR owns."""
    g = load_graph(conn)
    findings = (
        check_l01(g, schema) + check_l02(g) + check_l03(g) + check_l04(g) + check_l05(g)
        + check_l06(g, schema) + check_l07(g, schema) + check_l08(g) + check_l09(g) + check_l10(g)
        + check_l11(g)
    )
    if fr is not None:
        findings = [f for f in findings if f.node_id in g.nodes and g.nodes[f.node_id].owner_fr == fr]
    return sorted(findings, key=lambda f: (f.rule, f.key))


def format_table(findings: list[Finding]) -> str:
    if not findings:
        return "No findings."
    rows = [("ID", "Message")] + [(f.id, f.message) for f in findings]
    width = max(len(r[0]) for r in rows)
    lines = [f"{a.ljust(width)}  {b}" for a, b in rows]
    lines.insert(1, f"{'-' * width}  {'-' * 7}")
    counts: dict[str, int] = defaultdict(int)
    for f in findings:
        counts[f.rule] += 1
    summary = ", ".join(f"{rule}: {n}" for rule, n in sorted(counts.items()))
    lines.append("")
    lines.append(f"{len(findings)} finding(s) ({summary})")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check the requirements graph against its guardrails.")
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH), help="graph DB (default: graph.db in the graph folder)")
    parser.add_argument("--fr", help="only report findings on nodes owned by this FR (FR-NNN)")
    parser.add_argument("--json", action="store_true", help="print findings as JSON")
    args = parser.parse_args(argv)
    try:
        schema = load_schema()
        conn = open_db(args.db, read_only=True)
        try:
            if args.fr:
                validate_fr(conn, schema, args.fr)
            findings = lint(conn, schema, args.fr)
        finally:
            conn.close()
    except (SchemaError, FileNotFoundError, ValueError, sqlite3.Error) as exc:
        print(f"lint: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({"count": len(findings), "findings": [f.as_dict() for f in findings]}, indent=2, ensure_ascii=False))
    else:
        print(format_table(findings))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
