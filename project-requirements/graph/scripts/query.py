"""Read-only queries over the requirements graph DB.

Usage: query.py <command> [args] [--db DB_PATH] [--json]

  impact <node-id> [--depth N]   nodes reachable through any edge, either direction, up to N hops (default 2)
  lifecycle <timeline>           Stages of a timeline in sequence order, with what acts, is read or written,
                                 applies, is emitted and belongs at each Stage
  cites <node-id>                nodes with an edge to this node (for a Field: the Screens that show it)
  fr <FR-id>                     nodes owned by the FR, grouped by type
  history <node-id>              change rows for the node, newest first
  at <node-id> <ISO-timestamp>   the node's attributes at that time, replayed from its change rows
  changeset <changeset-id>       every change row of one change-set

Output is a plain table, or JSON with --json. Exit codes: 0 ok, 1 not found or bad argument, 2 database error.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from common import DEFAULT_DB_PATH, Schema, SchemaError, load_schema, open_db

# Field-to-Entity membership lives in fields.entity_id, not in edges, but a change to either side
# affects the other, so impact traverses it like an edge.
IMPACT_SQL = """
WITH RECURSIVE
  link(a, b) AS (
    SELECT from_id, to_id FROM edges
    UNION ALL SELECT to_id, from_id FROM edges
    UNION ALL SELECT id, entity_id FROM fields
    UNION ALL SELECT entity_id, id FROM fields
  ),
  walk(id, hop) AS (
    SELECT :start, 0
    UNION
    SELECT link.b, walk.hop + 1 FROM walk JOIN link ON link.a = walk.id WHERE walk.hop < :depth
  )
SELECT min(walk.hop) AS hop, n.owner_fr, n.type, n.id, n.title, n.status
FROM walk JOIN nodes n ON n.id = walk.id
WHERE walk.id <> :start
GROUP BY n.id
ORDER BY hop, n.owner_fr IS NULL, n.owner_fr, n.type, n.id
"""

CHANGE_COLUMNS = ["changeset_id", "at", "changed_by", "node_id", "attribute", "old_value", "new_value", "reason", "source_id"]

# (output column, verb, direction): "in" means the related node points at the Stage, "out" the reverse.
LIFECYCLE_LINKS = (
    ("actors", "acts in", "in"),
    ("reads", "reads", "out"),
    ("writes", "writes", "out"),
    ("rules", "applies at", "in"),
    ("events", "emits", "out"),
    ("screens", "belongs to", "in"),
)


class QueryError(ValueError):
    """The query names something that does not exist or an argument is invalid."""


@dataclass
class Result:
    columns: list[str]
    rows: list[dict[str, Any]]


def decode(text: str | None) -> Any:
    """Change values are stored as JSON; fall back to raw text for rows written by other means."""
    if text is None:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def _require_node(conn: sqlite3.Connection, node_id: str, node_type: str | None = None) -> str:
    row = conn.execute("SELECT type FROM nodes WHERE id = ?", (node_id,)).fetchone()
    if row is None:
        raise QueryError(f"node {node_id!r} does not exist")
    if node_type and row[0] != node_type:
        raise QueryError(f"node {node_id!r} is a {row[0]}, not a {node_type}")
    return row[0]


def _parse_timestamp(text: str) -> datetime:
    try:
        moment = datetime.fromisoformat(text)
    except ValueError:
        raise QueryError(f"{text!r} is not an ISO timestamp (e.g. 2026-11-05T10:00:00+07:00)") from None
    return moment.replace(tzinfo=timezone.utc) if moment.tzinfo is None else moment


def _change_rows(conn: sqlite3.Connection, where: str, params: tuple, order: str) -> list[dict[str, Any]]:
    sql = f"SELECT {', '.join(CHANGE_COLUMNS)} FROM changes WHERE {where} ORDER BY id {order}"
    rows = []
    for row in conn.execute(sql, params):
        item = dict(zip(CHANGE_COLUMNS, row))
        item["old_value"], item["new_value"] = decode(item["old_value"]), decode(item["new_value"])
        rows.append(item)
    return rows


def impact(conn: sqlite3.Connection, node_id: str, depth: int = 2) -> Result:
    if depth < 1:
        raise QueryError(f"--depth must be at least 1, got {depth}")
    _require_node(conn, node_id)
    columns = ["hop", "owner_fr", "type", "id", "title", "status"]
    rows = [dict(zip(columns, r)) for r in conn.execute(IMPACT_SQL, {"start": node_id, "depth": depth})]
    return Result(columns, rows)


def lifecycle(conn: sqlite3.Connection, schema: Schema, timeline: str) -> Result:
    timelines = schema.enum("timeline")
    if timeline not in timelines:
        raise QueryError(f"unknown timeline {timeline!r}; known: {list(timelines)}")
    stages = conn.execute(
        "SELECT id, title, json_extract(attrs, '$.sequence') FROM nodes "
        "WHERE type = 'Stage' AND status = 'active' AND json_extract(attrs, '$.timeline') = ? ORDER BY 3, id",
        (timeline,),
    ).fetchall()
    rows = []
    for stage_id, title, sequence in stages:
        row: dict[str, Any] = {"sequence": sequence, "stage": stage_id, "title": title}
        for column, verb, direction in LIFECYCLE_LINKS:
            near, far = ("to_id", "from_id") if direction == "in" else ("from_id", "to_id")
            row[column] = [r[0] for r in conn.execute(
                f"SELECT e.{far} FROM edges e JOIN nodes n ON n.id = e.{far} "
                f"WHERE e.verb = ? AND e.{near} = ? AND n.status = 'active' ORDER BY 1",
                (verb, stage_id),
            )]
        rows.append(row)
    return Result(["sequence", "stage", "title", *(c for c, _, _ in LIFECYCLE_LINKS)], rows)


def cites(conn: sqlite3.Connection, node_id: str) -> Result:
    _require_node(conn, node_id)
    columns = ["id", "verb", "type", "owner_fr", "title", "status", "edge_attrs"]
    rows = []
    for r in conn.execute(
        "SELECT e.from_id, e.verb, n.type, n.owner_fr, n.title, n.status, e.attrs "
        "FROM edges e JOIN nodes n ON n.id = e.from_id WHERE e.to_id = ? ORDER BY e.verb, n.type, e.from_id",
        (node_id,),
    ):
        item = dict(zip(columns, r))
        item["edge_attrs"] = json.loads(item["edge_attrs"])
        rows.append(item)
    return Result(columns, rows)


def fr(conn: sqlite3.Connection, schema: Schema, fr_id: str) -> Result:
    _require_node(conn, fr_id, "FR")
    columns = ["type", "id", "title", "status", "version"]
    rows = [dict(zip(columns, r)) for r in conn.execute(
        "SELECT type, id, title, status, version FROM nodes WHERE owner_fr = ?", (fr_id,)
    )]
    type_order = {name: i for i, name in enumerate(schema.node_types)}
    rows.sort(key=lambda r: (type_order.get(r["type"], len(type_order)), r["id"]))
    return Result(columns, rows)


def history(conn: sqlite3.Connection, node_id: str) -> Result:
    _require_node(conn, node_id)
    columns = [c for c in CHANGE_COLUMNS if c != "node_id"]
    return Result(columns, _change_rows(conn, "node_id = ?", (node_id,), "DESC"))


def at(conn: sqlite3.Connection, node_id: str, timestamp: str) -> Result:
    """Replay the node's change rows up to the timestamp; an absent (null) new value removes the attribute."""
    _require_node(conn, node_id)
    moment = _parse_timestamp(timestamp)
    state: dict[str, Any] = {}
    seen = False
    for row in _change_rows(conn, "node_id = ?", (node_id,), "ASC"):
        if _parse_timestamp(row["at"]) > moment:
            continue
        seen = True
        if row["new_value"] is None:
            state.pop(row["attribute"], None)
        else:
            state[row["attribute"]] = row["new_value"]
    if not seen:
        raise QueryError(f"node {node_id!r} has no recorded state at or before {timestamp}")
    return Result(["attribute", "value"], [{"attribute": k, "value": v} for k, v in sorted(state.items())])


def changeset(conn: sqlite3.Connection, changeset_id: str) -> Result:
    rows = _change_rows(conn, "changeset_id = ?", (changeset_id,), "ASC")
    if not rows:
        raise QueryError(f"change-set {changeset_id!r} does not exist")
    return Result([c for c in CHANGE_COLUMNS if c != "changeset_id"], [{k: v for k, v in r.items() if k != "changeset_id"} for r in rows])


def _cell(value: Any) -> str:
    if value is None:
        return "-"
    if isinstance(value, list):
        return ", ".join(str(v) for v in value) or "-"
    if isinstance(value, dict):
        return "; ".join(f"{k}={_cell(v)}" for k, v in value.items()) or "-"
    if isinstance(value, bool):
        return "true" if value else "false"
    return " ".join(str(value).split())


def format_table(result: Result) -> str:
    if not result.rows:
        return "(no rows)"
    cells = [[_cell(row.get(c)) for c in result.columns] for row in result.rows]
    widths = [max(len(col), *(len(line[i]) for line in cells)) for i, col in enumerate(result.columns)]
    lines = ["  ".join(col.ljust(w) for col, w in zip(result.columns, widths)), "  ".join("-" * w for w in widths)]
    lines += ["  ".join(cell.ljust(w) for cell, w in zip(line, widths)) for line in cells]
    return "\n".join(line.rstrip() for line in lines)


def run(conn: sqlite3.Connection, schema: Schema, args: argparse.Namespace) -> Result:
    if args.command == "impact":
        return impact(conn, args.node_id, args.depth)
    if args.command == "lifecycle":
        return lifecycle(conn, schema, args.timeline)
    if args.command == "cites":
        return cites(conn, args.node_id)
    if args.command == "fr":
        return fr(conn, schema, args.fr_id)
    if args.command == "history":
        return history(conn, args.node_id)
    if args.command == "at":
        return at(conn, args.node_id, args.timestamp)
    return changeset(conn, args.changeset_id)


def build_parser() -> argparse.ArgumentParser:
    shared = argparse.ArgumentParser(add_help=False)
    shared.add_argument("--db", default=str(DEFAULT_DB_PATH), help="DB file (default: graph.db in the graph folder)")
    shared.add_argument("--json", action="store_true", help="print JSON instead of a table")
    parser = argparse.ArgumentParser(description="Read-only queries over the requirements graph DB.")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("impact", parents=[shared], help="nodes reachable within N hops")
    p.add_argument("node_id")
    p.add_argument("--depth", type=int, default=2)
    sub.add_parser("lifecycle", parents=[shared], help="Stages of a timeline").add_argument("timeline")
    sub.add_parser("cites", parents=[shared], help="nodes with an edge to a node").add_argument("node_id")
    sub.add_parser("fr", parents=[shared], help="nodes owned by an FR").add_argument("fr_id")
    sub.add_parser("history", parents=[shared], help="change rows for a node").add_argument("node_id")
    p = sub.add_parser("at", parents=[shared], help="a node's attributes at a time")
    p.add_argument("node_id")
    p.add_argument("timestamp")
    sub.add_parser("changeset", parents=[shared], help="rows of one change-set").add_argument("changeset_id")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        schema = load_schema()
    except SchemaError as exc:
        print(f"query: {exc}", file=sys.stderr)
        return 1
    try:
        conn = open_db(args.db)
    except (FileNotFoundError, sqlite3.Error) as exc:
        print(f"query: {exc}", file=sys.stderr)
        return 2
    try:
        result = run(conn, schema, args)
    except QueryError as exc:
        print(f"query: {exc}", file=sys.stderr)
        return 1
    except sqlite3.Error as exc:
        print(f"query: database error: {exc}", file=sys.stderr)
        return 2
    finally:
        conn.close()
    print(json.dumps(result.rows, indent=2, ensure_ascii=False) if args.json else format_table(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
