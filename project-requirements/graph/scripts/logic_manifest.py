"""Build the logic-review manifest for one FR: every item a reviewer must give a verdict on.

Usage: logic_manifest.py <FR-id> [--db DB_PATH] [--prd PRD_PATH] [--format json|md] [--out PATH]

Items (one stable id each, see checklists/logic-review.md "Manifest items"):
  S:<heading-path>        every heading of the PRD, with its line range
  N:<node-id>             every active node the FR owns, and every active node one live edge away
                          from an owned node that the FR does not own (Stages, Actors, Sources,
                          other FRs' nodes)
  E:<from>><verb>><to>    every live edge with one end in this FR and the other in another FR
  F:<FR-id>               every neighbour FR: the far end of a boundary edge, an FR named in an owned
                          Step's hand-off, or the owner of a Step on a listed Flow's path
  N:<FLW-id>              every Flow whose 'next' path from its 'starts at' Step passes through an
                          owned Step, with that path

The DB is opened read-only. The PRD defaults to the frozen baseline folder named by the FR node's
'module' attribute. Exit codes: 0 ok, 1 bad argument or missing file, 2 database error.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from common import DEFAULT_DB_PATH, GRAPH_DIR, Graph, Node, Schema, SchemaError, load_graph, load_schema, open_db, validate_fr
from lint import edge_key

PROJECT_ROOT = GRAPH_DIR.parents[2]
BASELINE_DIR = PROJECT_ROOT / "archived" / "prd-baseline-2026-11-08"
MANIFEST_VERSION = 1

KIND_SECTION = "section"
KIND_OWNED = "owned node"
KIND_REFERENCED = "referenced node"
KIND_EDGE = "boundary edge"
KIND_NEIGHBOUR = "neighbour FR"
KIND_FLOW = "flow"
KIND_ORDER = (KIND_SECTION, KIND_OWNED, KIND_REFERENCED, KIND_EDGE, KIND_NEIGHBOUR, KIND_FLOW)

_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
_FENCE = re.compile(r"^\s*(```|~~~)")
_SLUG_JUNK = re.compile(r"[^a-z0-9]+")
_FR_MENTION = re.compile(r"\bFR-(\d{3}[A-Z]?|SYS)\b")
_STEP_MENTION = re.compile(r"\bSTP-(\d{3}[A-Z]?|SYS)-\d{3}\b")


class ManifestError(ValueError):
    """Raised when the FR, the PRD or the arguments cannot produce a manifest."""


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _slug(text: str) -> str:
    return _SLUG_JUNK.sub("-", text.lower()).strip("-") or "untitled"


def prd_sections(lines: list[str]) -> list[dict[str, Any]]:
    """Every Markdown heading outside fenced code, with its own line range (up to the next heading).

    The id is the slug path of the heading and its level-2-and-deeper ancestors, so it survives edits
    that shift line numbers; a repeated path gets a ~2, ~3 suffix in document order.
    """
    found: list[tuple[int, int, str]] = []  # (line number, level, text)
    in_fence = False
    for number, line in enumerate(lines, start=1):
        if _FENCE.match(line):
            in_fence = not in_fence
            continue
        match = None if in_fence else _HEADING.match(line)
        if match:
            found.append((number, len(match.group(1)), match.group(2).strip()))

    sections: list[dict[str, Any]] = []
    seen: dict[str, int] = {}
    ancestors: list[tuple[int, str]] = []  # (level, slug) of open headings
    for index, (number, level, text) in enumerate(found):
        while ancestors and ancestors[-1][0] >= level:
            ancestors.pop()
        ancestors.append((level, _slug(text)))
        path_parts = [slug for lvl, slug in ancestors if lvl > 1] or [ancestors[-1][1]]
        path = "/".join(path_parts)
        seen[path] = seen.get(path, 0) + 1
        if seen[path] > 1:
            path = f"{path}~{seen[path]}"
        end = found[index + 1][0] - 1 if index + 1 < len(found) else len(lines)
        sections.append({"id": f"S:{path}", "kind": KIND_SECTION, "heading": text, "level": level,
                         "lines": [number, end]})
    return sections


def default_prd_path(g: Graph, fr: str) -> Path:
    module = g.nodes[fr].attrs.get("module")
    if not module:
        raise ManifestError(f"{fr} has no 'module' attribute naming its baseline folder; pass --prd")
    return BASELINE_DIR / str(module) / "prd.md"


def _home(n: Node) -> str | None:
    """The FR a node belongs to: an FR node is its own home; ownerless nodes have none."""
    return n.id if n.type == "FR" else n.owner_fr


def flow_path(g: Graph, flow_id: str) -> tuple[list[str], list[dict[str, Any]]]:
    """Steps reachable from the Flow's 'starts at' Steps through live 'next' links, in breadth-first
    order, and each 'next' link on the way once."""
    steps: list[str] = []
    links: list[dict[str, Any]] = []
    queue = [e.to_id for e in g.edges_from(flow_id, "starts at")]
    seen = set(queue)
    while queue:
        step = queue.pop(0)
        steps.append(step)
        for e in g.edges_from(step, "next"):
            links.append({"from": e.from_id, "to": e.to_id, **{k: e.attrs[k] for k in ("condition", "label", "back") if k in e.attrs}})
            if e.to_id not in seen:
                seen.add(e.to_id)
                queue.append(e.to_id)
    return steps, links


def _mentioned_frs(text: str) -> set[str]:
    return {f"FR-{m}" for m in _FR_MENTION.findall(text)} | {f"FR-{m}" for m in _STEP_MENTION.findall(text)}


def build_manifest(conn: sqlite3.Connection, schema: Schema, fr: str, prd_path: Path, db_path: Path,
                   now: datetime | None = None) -> dict[str, Any]:
    validate_fr(conn, schema, fr)
    g = load_graph(conn)
    if not prd_path.is_file():
        raise ManifestError(f"PRD {prd_path} does not exist")
    lines = prd_path.read_text(encoding="utf-8").splitlines()

    type_order = {name: i for i, name in enumerate(schema.node_types)}

    def node_key(node_id: str) -> tuple[int, str]:
        return (type_order.get(g.active[node_id].type, len(type_order)), node_id)

    def node_item(node_id: str, kind: str) -> dict[str, Any]:
        n = g.active[node_id]
        return {"id": f"N:{n.id}", "kind": kind, "node_id": n.id, "type": n.type, "title": n.title, "owner_fr": n.owner_fr}

    ours = {n.id for n in g.active.values() if _home(n) == fr}
    owned = sorted((i for i in ours if i != fr), key=node_key)

    referenced: set[str] = set()
    boundary = []
    neighbours: set[str] = set()
    for e in g.live_edges:
        ends = (g.active[e.from_id], g.active[e.to_id])
        for near, far in (ends, ends[::-1]):
            if _home(near) != fr or _home(far) == fr:
                continue
            if far.type not in ("FR", "Flow"):
                referenced.add(far.id)
            if _home(far) is not None:
                boundary.append(e)
                neighbours.add(_home(far))

    owned_steps = {i for i in owned if g.active[i].type == "Step"}
    for step in owned_steps:
        for key in ("handoff_to", "handoff_from"):
            neighbours |= _mentioned_frs(str(g.active[step].attrs.get(key) or ""))

    flows = []
    for flow in sorted(n.id for n in g.of_type("Flow")):
        steps, links = flow_path(g, flow)
        if not owned_steps.intersection(steps):
            continue
        attrs = g.active[flow].attrs
        neighbours |= {g.active[s].owner_fr for s in steps}  # Steps always have an owner (schema)
        flows.append({
            "id": f"N:{flow}", "kind": KIND_FLOW, "node_id": flow, "type": "Flow", "title": g.active[flow].title,
            "flow_kind": attrs.get("kind"), "starts_at": [e.to_id for e in g.edges_from(flow, "starts at")],
            "steps": [{"id": s, "owner_fr": g.active[s].owner_fr} for s in steps], "next": links,
        })

    neighbours = {n for n in neighbours if n != fr and n in g.active and g.active[n].type == "FR"}
    edge_items = {}
    for e in boundary:
        edge_items[f"E:{edge_key(e)}"] = {"id": f"E:{edge_key(e)}", "kind": KIND_EDGE, "from": e.from_id, "verb": e.verb,
                                          "to": e.to_id, "attrs": e.attrs}
    neighbour_items = []
    for nb in sorted(neighbours):
        crossing = sorted(k for k, v in edge_items.items() if nb in (_home(g.active[v["from"]]), _home(g.active[v["to"]])))
        neighbour_items.append({"id": f"F:{nb}", "kind": KIND_NEIGHBOUR, "fr": nb, "title": g.active[nb].title,
                                "prd_path": g.active[nb].attrs.get("prd_path"), "boundary_edges": crossing})

    items = (
        prd_sections(lines)
        + [node_item(i, KIND_OWNED) for i in owned]
        + [node_item(i, KIND_REFERENCED) for i in sorted(referenced, key=node_key)]
        + [edge_items[k] for k in sorted(edge_items)]
        + neighbour_items
        + flows
    )
    counts = {kind: sum(1 for item in items if item["kind"] == kind) for kind in KIND_ORDER}
    return {
        "manifest_version": MANIFEST_VERSION,
        "fr": fr,
        "generated_at": (now or datetime.now(timezone.utc)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "db": {"path": str(db_path), "sha256": file_sha256(db_path), "schema_version": schema.version},
        "prd": {"path": str(prd_path), "sha256": file_sha256(prd_path), "lines": len(lines)},
        "counts": counts,
        "items": items,
    }


def _cell(value: Any) -> str:
    """Markdown table cell: no pipe characters, no line breaks."""
    return str("" if value is None else value).replace("|", "/").replace("\n", " ")


def _table(header: list[str], rows: list[list[Any]]) -> list[str]:
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    out += ["| " + " | ".join(_cell(c) for c in row) + " |" for row in rows]
    return out


def to_markdown(manifest: dict[str, Any]) -> str:
    items = manifest["items"]
    by_kind = {kind: [i for i in items if i["kind"] == kind] for kind in KIND_ORDER}
    out = [
        f"# {manifest['fr']} logic-review manifest",
        "",
        f"Generated: {manifest['generated_at']}",
        f"Graph: {manifest['db']['path']} (schema v{manifest['db']['schema_version']}, sha256 {manifest['db']['sha256'][:12]})",
        f"PRD: {manifest['prd']['path']} ({manifest['prd']['lines']} lines, sha256 {manifest['prd']['sha256'][:12]})",
        "",
        "Give one verdict row per item id below, in this order (checklists/logic-review.md, Report format).",
        "",
        "## PRD sections", "",
        *_table(["Item", "Heading", "Lines"], [[i["id"], i["heading"], f"prd:{i['lines'][0]}-{i['lines'][1]}"] for i in by_kind[KIND_SECTION]]),
        "", "## Nodes the FR owns", "",
        *_table(["Item", "Type", "Title"], [[i["id"], i["type"], i["title"]] for i in by_kind[KIND_OWNED]]),
        "", "## Nodes the FR references", "",
        *_table(["Item", "Type", "Owner", "Title"], [[i["id"], i["type"], i["owner_fr"] or "none", i["title"]] for i in by_kind[KIND_REFERENCED]]),
        "", "## Boundary edges", "",
        *_table(["Item", "From", "Verb", "To"], [[i["id"], i["from"], i["verb"], i["to"]] for i in by_kind[KIND_EDGE]]),
        "", "## Neighbour FRs", "",
        *_table(["Item", "Title", "Boundary edges"], [[i["id"], i["title"], len(i["boundary_edges"])] for i in by_kind[KIND_NEIGHBOUR]]),
        "", "## Flows", "",
        *_table(["Item", "Kind", "Starts at", "Steps"], [[i["id"], i["flow_kind"] or "", ", ".join(i["starts_at"]), len(i["steps"])] for i in by_kind[KIND_FLOW]]),
    ]
    for flow in by_kind[KIND_FLOW]:
        out += ["", f"### Path of {flow['node_id']}", ""]
        rows = [[link["from"], link["to"], link.get("condition", ""), link.get("label", ""), "yes" if link.get("back") else ""]
                for link in flow["next"]]
        out += _table(["From step", "To step", "Condition", "Label", "Back"], rows) if rows else ["Single step, no 'next' links."]
    return "\n".join(out) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build the logic-review manifest for one FR.")
    parser.add_argument("fr", help="FR id, for example FR-005")
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH), help="graph DB, opened read-only (default: graph.db)")
    parser.add_argument("--prd", help="PRD file (default: the FR's frozen baseline PRD)")
    parser.add_argument("--format", choices=("json", "md"), default="json", help="output format (default json)")
    parser.add_argument("--out", help="write here instead of stdout")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    db_path = Path(args.db).resolve()
    try:
        schema = load_schema()
        conn = open_db(db_path, schema, read_only=True)
    except (SchemaError, FileNotFoundError) as exc:
        print(f"logic_manifest: {exc}", file=sys.stderr)
        return 1
    except sqlite3.Error as exc:
        print(f"logic_manifest: {exc}", file=sys.stderr)
        return 2
    try:
        if args.prd:
            prd_path = Path(args.prd).resolve()
        else:
            validate_fr(conn, schema, args.fr)
            prd_path = default_prd_path(load_graph(conn), args.fr)
        manifest = build_manifest(conn, schema, args.fr, prd_path, db_path)
    except (ManifestError, ValueError, OSError) as exc:
        print(f"logic_manifest: {exc}", file=sys.stderr)
        return 1
    except sqlite3.Error as exc:
        print(f"logic_manifest: database error: {exc}", file=sys.stderr)
        return 2
    finally:
        conn.close()
    text = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n" if args.format == "json" else to_markdown(manifest)
    if args.out:
        try:
            Path(args.out).write_text(text, encoding="utf-8")
        except OSError as exc:
            print(f"logic_manifest: cannot write {args.out}: {exc}", file=sys.stderr)
            return 1
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
