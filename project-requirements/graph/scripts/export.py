"""Export the requirements graph to graph.json for the viewer.

Usage: export.py [OUT_PATH] [--db DB_PATH] [--include-retired]

OUT_PATH defaults to graph.json in the graph folder. Only active nodes are written unless
--include-retired is given. Rows that belong to a left-out node go with it: the fields of a
left-out Entity or Field node, their enum values, edges touching it, and its source record.
Plain reference columns (owner_fr, calculated_by) are kept as stored. Every list is sorted by its key so successive exports diff cleanly.

History is exported as one summary per change-set in `changes`, newest first, whatever the node
filter: its metadata, the node ids it added and updated, its edge counts and its row count. The
individual change rows stay in graph.db (query.py history / changeset).
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from common import ACTIVE, DEFAULT_DB_PATH, GRAPH_DIR, open_db, parse_attrs

DEFAULT_OUT_PATH = GRAPH_DIR / "graph.json"


def build_export(conn: sqlite3.Connection, include_retired: bool = False, now: datetime | None = None) -> dict[str, Any]:
    nodes = []
    for id_, type_, owner, title, status, version, attrs in conn.execute(
        "SELECT id, type, owner_fr, title, status, version, attrs FROM nodes ORDER BY id"
    ):
        if include_retired or status == ACTIVE:
            nodes.append({
                "id": id_, "type": type_, "owner_fr": owner, "title": title,
                "status": status, "version": version, "attrs": parse_attrs(attrs, f"node {id_}"),
            })
    kept = {n["id"] for n in nodes}

    fields = [
        {"id": id_, "entity_id": entity, "name": name, "data_type": data_type, "required": bool(required), "calculated_by": calc}
        for id_, entity, name, data_type, required, calc in conn.execute(
            "SELECT id, entity_id, name, data_type, required, calculated_by FROM fields ORDER BY id"
        )
        if id_ in kept and entity in kept
    ]
    kept_fields = {f["id"] for f in fields}

    enum_values = [
        {"field_id": fid, "value": value, "label": label, "sort_order": order}
        for fid, value, label, order in conn.execute(
            "SELECT field_id, value, label, sort_order FROM enum_values ORDER BY field_id, sort_order, value"
        )
        if fid in kept_fields
    ]

    edges = [
        {"from_id": a, "verb": verb, "to_id": b, "attrs": parse_attrs(attrs, f"edge {a} {verb} {b}")}
        for a, verb, b, attrs in conn.execute("SELECT from_id, verb, to_id, attrs FROM edges ORDER BY from_id, verb, to_id")
        if a in kept and b in kept
    ]

    sources = [
        {"id": id_, "kind": kind, "ref": ref, "section": section, "date": date, "lifecycle": lifecycle}
        for id_, kind, ref, section, date, lifecycle in conn.execute(
            "SELECT id, kind, ref, section, date, lifecycle FROM sources ORDER BY id"
        )
        if id_ in kept
    ]

    stamp = (now or datetime.now(timezone.utc)).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "generated_at": stamp,
        "schema_version": conn.execute("PRAGMA user_version").fetchone()[0],
        "nodes": nodes,
        "fields": fields,
        "enum_values": enum_values,
        "edges": edges,
        "sources": sources,
        "changes": build_change_sets(conn),
    }


def build_change_sets(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    """Summarise the changes table per change-set, newest first.

    write.py records a created node with a `type` row whose old value is NULL, and `type` never
    changes afterwards, so a node is added by a set when its first row in that set is that row.
    Edges are `edge:<verb>:<to>` rows (NULL old value = added, NULL new value = removed); the
    `field.calculated_by` row stands for its `calculated by` edge, so a change of target counts as
    one removal plus one addition.
    """
    sets: dict[str, dict[str, Any]] = {}
    first_row: dict[tuple[str, str], bool] = {}
    for cs_id, at, by, reason, source_id, node_id, attribute, old, new in conn.execute(
        "SELECT changeset_id, at, changed_by, reason, source_id, node_id, attribute, old_value, new_value "
        "FROM changes ORDER BY id"
    ):
        cs = sets.get(cs_id)
        if cs is None:
            cs = sets[cs_id] = {
                "id": cs_id, "at": at, "changed_by": by, "reason": reason, "source_id": source_id,
                "nodes_added": [], "nodes_updated": set(), "edges_added": 0, "edges_removed": 0, "rows": 0,
            }
        cs["rows"] += 1
        if (cs_id, node_id) not in first_row:
            first_row[(cs_id, node_id)] = created = attribute == "type" and old is None
            if created:
                cs["nodes_added"].append(node_id)
            else:
                cs["nodes_updated"].add(node_id)
        if attribute.startswith("edge:") or attribute == "field.calculated_by":
            cs["edges_added"] += new is not None
            cs["edges_removed"] += old is not None
    for cs in sets.values():
        cs["nodes_added"].sort()
        cs["nodes_updated"] = sorted(cs["nodes_updated"])
    return sorted(sets.values(), key=lambda cs: (cs["at"], cs["id"]), reverse=True)


def write_json(data: dict[str, Any], out_path: Path) -> None:
    """Write via a temp file and rename, so a failed export never leaves a truncated graph.json."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = out_path.with_name(out_path.name + ".tmp")
    try:
        tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        os.replace(tmp, out_path)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Export the requirements graph to graph.json.")
    parser.add_argument("out_path", nargs="?", default=str(DEFAULT_OUT_PATH), help="output file (default: graph.json in the graph folder)")
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH), help="graph DB (default: graph.db in the graph folder)")
    parser.add_argument("--include-retired", action="store_true", help="also export retired nodes and rows that reference them")
    args = parser.parse_args(argv)
    out_path = Path(args.out_path).resolve()
    try:
        conn = open_db(args.db, read_only=True)
        try:
            data = build_export(conn, include_retired=args.include_retired)
        finally:
            conn.close()
        write_json(data, out_path)
    except (FileNotFoundError, ValueError, OSError, sqlite3.Error) as exc:
        print(f"export: {exc}", file=sys.stderr)
        return 2
    print(
        f"Wrote {out_path}: {len(data['nodes'])} nodes, {len(data['fields'])} fields, "
        f"{len(data['enum_values'])} enum values, {len(data['edges'])} edges, {len(data['sources'])} sources, {len(data['changes'])} change-sets"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
