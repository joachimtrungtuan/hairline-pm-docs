"""Render the graph-owned sections of one FR PRD as markdown.

Usage: render.py FR-NNN [--db DB_PATH] [--out FILE]

Writes to stdout, or to FILE with --out. The output is a derived document: edits made to it
by hand are lost on the next render. Content owned by another FR is never restated; it
appears only as a citation of its node ID (a cited Rule renders as "[REQ-NNN-NNN] title").
Retired nodes are left out of every section except the Change Log, which is history.
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from common import ACTIVE, DEFAULT_DB_PATH, Edge, Graph, Node, Schema, SchemaError, load_graph, load_schema, open_db, validate_fr

HEADER = "<!-- rendered from graph.db; do not edit by hand -->"
NONE = "_None._"


@dataclass(frozen=True)
class FieldRow:
    id: str
    entity_id: str
    name: str
    data_type: str
    required: bool
    calculated_by: str | None


def one_line(text: Any) -> str:
    """Collapse whitespace so a value fits on one heading or list line."""
    return " ".join(str(text).split()) if text is not None else ""


def cell(value: Any) -> str:
    """Make a value safe for a markdown table cell: no literal pipe, no raw line break."""
    text = "" if value is None else str(value)
    text = text.replace("|", "/").replace("\r\n", "\n").replace("\r", "\n").strip().replace("\n", "<br>")
    return text or "-"


def table(headers: list[str], rows: Iterable[list[Any]]) -> list[str]:
    lines = ["| " + " | ".join(cell(h) for h in headers) + " |", "|" + "---|" * len(headers)]
    lines += ["| " + " | ".join(cell(v) for v in row) + " |" for row in rows]
    return lines


def yes_no(value: Any) -> str:
    return "yes" if value is True else "no" if value is False else "-"


class FrView:
    """Everything one FR's rendered sections need, read once from the DB."""

    def __init__(self, conn: sqlite3.Connection, schema: Schema, fr_id: str) -> None:
        self.schema = schema
        self.fr_id = fr_id
        self.g: Graph = load_graph(conn)
        self.fr: Node = self.g.nodes[fr_id]
        self.fields = {
            r[0]: FieldRow(r[0], r[1], r[2], r[3], bool(r[4]), r[5])
            for r in conn.execute("SELECT id, entity_id, name, data_type, required, calculated_by FROM fields")
        }
        self.enum_values: dict[str, list[tuple[str, str | None]]] = defaultdict(list)
        for fid, value, label in conn.execute("SELECT field_id, value, label FROM enum_values ORDER BY field_id, sort_order, value"):
            self.enum_values[fid].append((value, label))
        self.sources = {
            r[0]: r for r in conn.execute("SELECT id, kind, ref, section, date, lifecycle FROM sources")
        }
        self.changes = conn.execute(
            "SELECT c.changeset_id, c.at, c.changed_by, c.node_id, c.reason, c.source_id FROM changes c "
            "JOIN nodes n ON n.id = c.node_id WHERE n.owner_fr = ? OR n.id = ? ORDER BY c.id",
            (fr_id, fr_id),
        ).fetchall()
        self.owned = {n.id: n for n in self.g.active.values() if n.owner_fr == fr_id}

    # Lookups -----------------------------------------------------------------

    def owned_of(self, node_type: str) -> list[Node]:
        return sorted((n for n in self.owned.values() if n.type == node_type), key=lambda n: n.id)

    def out_edges(self, node_id: str, verb: str) -> list[Edge]:
        return self.g.edges_from(node_id, verb)

    def in_edges(self, node_id: str, verb: str) -> list[Edge]:
        return self.g.edges_to(node_id, verb)

    def cite(self, node_id: str) -> str:
        node = self.g.nodes.get(node_id)
        if node is None:
            return node_id
        suffix = " (retired)" if node.status != ACTIVE else ""
        return f"[{node.id}] {one_line(node.title)}{suffix}"

    def label(self, node_id: str) -> str:
        node = self.g.nodes.get(node_id)
        return f"{one_line(node.title)} ({node_id})" if node else node_id

    def is_foreign(self, node_id: str) -> bool:
        node = self.g.nodes.get(node_id)
        return node is not None and node.owner_fr is not None and node.owner_fr != self.fr_id

    def workflow_stages(self) -> dict[str, Node]:
        """Stages the FR's Rules apply at, its Screens belong to, or that produce its Events."""
        ids: set[str] = set()
        for rule in self.owned_of("Rule"):
            ids |= {e.to_id for e in self.out_edges(rule.id, "applies at")}
        for screen in self.owned_of("Screen"):
            ids |= {e.to_id for e in self.out_edges(screen.id, "belongs to")}
        for event in self.owned_of("Event"):
            ids |= {e.from_id for e in self.in_edges(event.id, "emits")}
        return {i: self.g.active[i] for i in ids if self.g.active[i].type == "Stage"}

    def stage_sort_key(self, stage: Node) -> tuple[int, int, str]:
        timelines = self.schema.enums.get("timeline", ())
        timeline = stage.attrs.get("timeline")
        sequence = stage.attrs.get("sequence")
        return (
            timelines.index(timeline) if timeline in timelines else len(timelines),
            sequence if type(sequence) is int else sys.maxsize,
            stage.id,
        )

    # Sections ----------------------------------------------------------------

    def scope(self) -> list[str]:
        summary = one_line(self.fr.attrs.get("summary")) or "_No summary recorded._"
        lines = [f"**{self.fr_id} - {one_line(self.fr.title)}**", "", summary]
        if self.fr.attrs.get("module"):
            lines += ["", f"Module: {one_line(self.fr.attrs['module'])}"]
        return lines

    def actors(self) -> list[str]:
        stages = self.workflow_stages()
        screens = {s.id for s in self.owned_of("Screen")}
        rows = []
        for actor in sorted(self.g.of_type("Actor"), key=lambda n: n.id):
            acts_in = sorted(e.to_id for e in self.out_edges(actor.id, "acts in") if e.to_id in stages)
            uses = sorted(e.to_id for e in self.out_edges(actor.id, "uses") if e.to_id in screens)
            if acts_in or uses:
                rows.append([actor.id, actor.title, ", ".join(acts_in), ", ".join(uses)])
        return table(["Actor", "Title", "Acts in", "Uses screens"], rows) if rows else [NONE]

    def workflows(self) -> list[str]:
        stages = sorted(self.workflow_stages().values(), key=self.stage_sort_key)
        if not stages:
            return [NONE]
        screens_at: dict[str, list[str]] = defaultdict(list)
        for screen in self.owned_of("Screen"):
            for e in self.out_edges(screen.id, "belongs to"):
                screens_at[e.to_id].append(f"{screen.id} {one_line(screen.title)}")
        lines: list[str] = []
        by_timeline: dict[str, list[Node]] = defaultdict(list)
        for stage in stages:
            by_timeline[stage.attrs.get("timeline") or "unassigned"].append(stage)
        for timeline, members in by_timeline.items():
            if lines:
                lines.append("")
            lines += [f"### Timeline: {one_line(timeline)}", ""]
            lines += table(
                ["Seq", "Stage", "Screens"],
                ([s.attrs.get("sequence"), self.label(s.id), "<br>".join(screens_at.get(s.id, []))] for s in members),
            )
        return lines

    def screen_specifications(self) -> list[str]:
        screens = self.owned_of("Screen")
        if not screens:
            return [NONE]
        lines: list[str] = []
        for screen in screens:
            if lines:
                lines.append("")
            lines += [f"### {screen.id}: {one_line(screen.title)}", ""]
            stages = ", ".join(self.label(e.to_id) for e in self.out_edges(screen.id, "belongs to")) or "-"
            facts = [f"Stage: {stages}"]
            if screen.attrs.get("platform"):
                facts.append(f"Platform: {one_line(screen.attrs['platform'])}")
            lines += ["; ".join(facts), ""]
            if screen.attrs.get("description"):
                lines += [str(screen.attrs["description"]).strip(), ""]
            rows = []
            # Edge insertion order is the authored display order of the fields on the screen.
            for e in self.out_edges(screen.id, "shows"):
                field = self.fields.get(e.to_id)
                default_label = field.name if field else self.g.nodes[e.to_id].title
                rows.append([e.attrs.get("label") or default_label, yes_no(e.attrs.get("editable")), e.attrs.get("provenance"), e.to_id])
            lines += table(["Label", "Editable", "Provenance", "Entity field"], rows) if rows else [NONE]
        return lines

    def business_rules(self) -> list[str]:
        owned = self.owned_of("Rule")
        # A foreign Rule is cited when any edge links it to a node this FR owns.
        cited: set[str] = set()
        for e in self.g.live_edges:
            for mine, other in ((e.from_id, e.to_id), (e.to_id, e.from_id)):
                if mine in self.owned and self.g.active[other].type == "Rule" and self.is_foreign(other):
                    cited.add(other)
        for node_id in self.owned:
            calc = self.fields[node_id].calculated_by if node_id in self.fields else None
            if calc and self.is_foreign(calc):
                cited.add(calc)
        if not owned and not cited:
            return [NONE]
        lines: list[str] = []
        for rule in owned:
            if lines:
                lines.append("")
            lines += [f"### {self.cite(rule.id)}", "", str(rule.attrs.get("statement", "")).strip() or "_No statement recorded._"]
            if rule.attrs.get("rationale"):
                lines += ["", f"_Rationale:_ {str(rule.attrs['rationale']).strip()}"]
        if cited:
            if lines:
                lines.append("")
            lines += ["### Cited rules", ""] + [f"- {self.cite(rid)}" for rid in sorted(cited)]
        return lines

    def field_rows(self, field_ids: Iterable[str]) -> list[list[Any]]:
        rows = []
        for fid in sorted(field_ids):
            f = self.fields[fid]
            name = f"{f.name} ({fid})"
            if self.is_foreign(fid):
                rows.append([name, f"cited, owned by {self.g.nodes[fid].owner_fr}", "-", "-", "-"])
                continue
            enums = ", ".join(v if not label or label == v else f"{v} ({label})" for v, label in self.enum_values.get(fid, []))
            calc = self.cite(f.calculated_by) if f.calculated_by else ""
            rows.append([name, f.data_type, yes_no(f.required), enums, calc])
        return rows

    def data(self) -> list[str]:
        headers = ["Field", "Type", "Required", "Enum values", "Calculated by"]
        active_fields = [f for f in self.fields.values() if f.id in self.g.active]
        lines: list[str] = []
        for entity in self.owned_of("Entity"):
            if lines:
                lines.append("")
            lines += [f"### {entity.id}: {one_line(entity.title)}", ""]
            facts = [str(entity.attrs[k]).strip() for k in ("description",) if entity.attrs.get(k)]
            if entity.attrs.get("table"):
                facts.append(f"Table: `{one_line(entity.attrs['table'])}`")
            if facts:
                lines += facts + [""]
            ids = [f.id for f in active_fields if f.entity_id == entity.id]
            lines += table(headers, self.field_rows(ids)) if ids else [NONE]
        foreign: dict[str, list[str]] = defaultdict(list)
        for f in active_fields:
            if f.id in self.owned and f.entity_id not in self.owned:
                foreign[f.entity_id].append(f.id)
        for entity_id in sorted(foreign):
            if lines:
                lines.append("")
            owner = self.g.nodes[entity_id].owner_fr if entity_id in self.g.nodes else None
            lines += [f"### Fields added to {self.label(entity_id)}, owned by {owner or 'no FR'}", ""]
            lines += table(headers, self.field_rows(foreign[entity_id]))
        return lines or [NONE]

    def events(self) -> list[str]:
        rows = [
            [
                e.id, e.title,
                ", ".join(self.label(x.from_id) for x in self.in_edges(e.id, "emits")),
                e.attrs.get("description"), e.attrs.get("payload"),
            ]
            for e in self.owned_of("Event")
        ]
        return table(["Event", "Title", "Produced at", "Description", "Payload"], rows) if rows else [NONE]

    def settings(self) -> list[str]:
        rows = [
            [
                s.id, s.title, s.attrs.get("default"), s.attrs.get("unit"),
                ", ".join(sorted(x.from_id for x in self.in_edges(s.id, "governed by"))),
                s.attrs.get("description"),
            ]
            for s in self.owned_of("Setting")
        ]
        return table(["Setting", "Title", "Default", "Unit", "Governs rules", "Description"], rows) if rows else [NONE]

    def dependencies(self) -> list[str]:
        """Other FRs owning nodes that this FR's own edges point at, plus entities its fields extend."""
        touched: dict[str, set[str]] = defaultdict(set)
        for e in self.g.live_edges:
            if e.from_id in self.owned and self.is_foreign(e.to_id):
                touched[self.g.nodes[e.to_id].owner_fr].add(e.to_id)
        for fid in self.owned:
            f = self.fields.get(fid)
            if f and self.is_foreign(f.entity_id):
                touched[self.g.nodes[f.entity_id].owner_fr].add(f.entity_id)
        rows = [
            [fr, self.g.nodes[fr].title if fr in self.g.nodes else "", ", ".join(sorted(ids))]
            for fr, ids in sorted(touched.items())
        ]
        return table(["FR", "Title", "Nodes"], rows) if rows else [NONE]

    def sources_section(self) -> list[str]:
        cited_by: dict[str, set[str]] = defaultdict(set)
        for node_id, node in self.owned.items():
            if node.type in ("Rule", "Entity"):
                for e in self.out_edges(node_id, "decided by"):
                    cited_by[e.to_id].add(node_id)
        for _cs, _at, _by, node_id, _reason, source_id in self.changes:
            if source_id and node_id in self.owned:
                cited_by[source_id].add(node_id)
        rows = []
        for sid in sorted(cited_by):
            _id, kind, ref, section, date, lifecycle = self.sources.get(sid, (sid, None, None, None, None, None))
            rows.append([sid, kind, ref, section, date, lifecycle, ", ".join(sorted(cited_by[sid]))])
        return table(["Source", "Kind", "Ref", "Section", "Date", "Lifecycle", "Cited by"], rows) if rows else [NONE]

    def change_log(self) -> list[str]:
        sets: dict[str, dict[str, Any]] = {}
        for cs, at, by, node_id, reason, _source in self.changes:
            entry = sets.setdefault(cs, {"at": at, "by": [], "nodes": [], "reasons": []})
            entry["at"] = max(entry["at"], at)
            for key, value in (("by", by), ("nodes", node_id), ("reasons", reason)):
                if value not in entry[key]:
                    entry[key].append(value)
        if not sets:
            return [NONE]
        ordered = sorted(sets.items(), key=lambda kv: (kv[1]["at"], kv[0]), reverse=True)
        rows = [
            [cs, e["at"], ", ".join(e["by"]), ", ".join(sorted(e["nodes"])), "; ".join(e["reasons"])]
            for cs, e in ordered
        ]
        return table(["Change set", "Date", "By", "Nodes", "Reason"], rows)

    def render(self) -> str:
        sections = [
            ("Scope", self.scope),
            ("Actors", self.actors),
            ("Workflows", self.workflows),
            ("Screen Specifications", self.screen_specifications),
            ("Business Rules", self.business_rules),
            ("Data", self.data),
            ("Events", self.events),
            ("Settings", self.settings),
            ("Dependencies", self.dependencies),
            ("Sources", self.sources_section),
            ("Change Log", self.change_log),
        ]
        lines = [HEADER]
        for heading, build in sections:
            lines += ["", f"## {heading}", ""] + build()
        return "\n".join(lines) + "\n"


def render(conn: sqlite3.Connection, schema: Schema, fr_id: str) -> str:
    validate_fr(conn, schema, fr_id)
    return FrView(conn, schema, fr_id).render()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render the graph-owned sections of one FR PRD as markdown.")
    parser.add_argument("fr", help="FR id, e.g. FR-004")
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH), help="graph DB (default: graph.db in the graph folder)")
    parser.add_argument("--out", help="write to this file instead of stdout")
    args = parser.parse_args(argv)
    try:
        schema = load_schema()
        conn = open_db(args.db, read_only=True)
        try:
            text = render(conn, schema, args.fr)
        finally:
            conn.close()
        if args.out:
            out = Path(args.out)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(text, encoding="utf-8")
        else:
            sys.stdout.write(text)
    except (SchemaError, FileNotFoundError, ValueError, OSError, sqlite3.Error) as exc:
        print(f"render: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
