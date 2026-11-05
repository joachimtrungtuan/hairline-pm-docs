"""Shared helpers for the requirements graph scripts: schema loading, DB access and the in-memory graph."""

from __future__ import annotations

import json
import re
import sqlite3
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

GRAPH_DIR = Path(__file__).resolve().parent.parent
SCHEMA_PATH = GRAPH_DIR / "schema.yaml"
DEFAULT_DB_PATH = GRAPH_DIR / "graph.db"
ACTIVE = "active"

OWNER_RULES = ("required", "optional", "forbidden")
DETAIL_TABLES = ("fields", "sources")
REQUIRED_ENUMS = ("node_status", "source_lifecycle", "provenance")


class SchemaError(ValueError):
    """Raised when schema.yaml is malformed or a lookup names something it does not define."""


@dataclass(frozen=True)
class AttrSpec:
    required: dict[str, str]
    optional: dict[str, str]


@dataclass(frozen=True)
class NodeType:
    name: str
    id_regex: re.Pattern[str]
    owner_fr: str
    detail_table: str | None
    attrs: AttrSpec


@dataclass(frozen=True)
class EdgeVerb:
    name: str
    pairs: frozenset[tuple[str, str]]
    attrs: AttrSpec


@dataclass(frozen=True)
class Schema:
    version: int
    enums: dict[str, tuple[str, ...]]
    attr_types: tuple[str, ...]
    node_types: dict[str, NodeType]
    edge_verbs: dict[str, EdgeVerb]

    def allowed_pairs(self, verb: str) -> frozenset[tuple[str, str]]:
        """Return the (from_type, to_type) pairs a verb may join."""
        try:
            return self.edge_verbs[verb].pairs
        except KeyError:
            raise SchemaError(f"unknown edge verb {verb!r}; known: {sorted(self.edge_verbs)}") from None

    def id_pattern(self, node_type: str) -> re.Pattern[str]:
        """Return the compiled ID regex for a node type."""
        try:
            return self.node_types[node_type].id_regex
        except KeyError:
            raise SchemaError(f"unknown node type {node_type!r}; known: {sorted(self.node_types)}") from None

    def enum(self, name: str) -> tuple[str, ...]:
        try:
            return self.enums[name]
        except KeyError:
            raise SchemaError(f"unknown enum {name!r}; known: {sorted(self.enums)}") from None


def _fail(where: str, message: str) -> SchemaError:
    return SchemaError(f"schema.yaml {where}: {message}")


def _mapping(value: Any, where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise _fail(where, f"expected a mapping, got {type(value).__name__}")
    return value


def _string_list(value: Any, where: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not value:
        raise _fail(where, "expected a non-empty list")
    for i, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            raise _fail(f"{where}[{i}]", f"expected a non-empty string, got {item!r}")
    if len(set(value)) != len(value):
        raise _fail(where, "contains duplicate values")
    return tuple(value)


def _attr_spec(raw: Any, where: str, valid_types: set[str]) -> AttrSpec:
    if raw is None:
        return AttrSpec({}, {})
    raw = _mapping(raw, where)
    unknown = set(raw) - {"required", "optional"}
    if unknown:
        raise _fail(where, f"unknown keys {sorted(unknown)}; allowed: required, optional")
    parts: dict[str, dict[str, str]] = {}
    for part in ("required", "optional"):
        section = _mapping(raw.get(part) or {}, f"{where}.{part}")
        for key, attr_type in section.items():
            if not isinstance(key, str) or not key:
                raise _fail(f"{where}.{part}", f"attribute name must be a non-empty string, got {key!r}")
            if attr_type not in valid_types:
                raise _fail(f"{where}.{part}.{key}", f"type {attr_type!r} is not an attr type or enum name")
        parts[part] = dict(section)
    overlap = set(parts["required"]) & set(parts["optional"])
    if overlap:
        raise _fail(where, f"attributes listed as both required and optional: {sorted(overlap)}")
    return AttrSpec(parts["required"], parts["optional"])


def parse_schema(raw: Any) -> Schema:
    """Validate a parsed schema document and build a Schema. Raises SchemaError on any defect."""
    raw = _mapping(raw, "root")
    for key in ("version", "enums", "attr_types", "node_types", "edge_verbs"):
        if key not in raw:
            raise _fail("root", f"missing required key {key!r}")

    version = raw["version"]
    if not isinstance(version, int) or isinstance(version, bool) or version < 1:
        raise _fail("version", f"expected a positive integer, got {version!r}")

    enums = {name: _string_list(values, f"enums.{name}") for name, values in _mapping(raw["enums"], "enums").items()}
    for name in REQUIRED_ENUMS:
        if name not in enums:
            raise _fail("enums", f"missing required enum {name!r}")

    attr_types = _string_list(raw["attr_types"], "attr_types")
    clash = set(attr_types) & set(enums)
    if clash:
        raise _fail("attr_types", f"names clash with enum names: {sorted(clash)}")
    valid_types = set(attr_types) | set(enums)

    node_types: dict[str, NodeType] = {}
    for name, spec in _mapping(raw["node_types"], "node_types").items():
        where = f"node_types.{name}"
        if not isinstance(name, str) or not re.fullmatch(r"[A-Z][A-Za-z]*", name):
            raise _fail(where, "node type names must be capitalised words")
        spec = _mapping(spec, where)
        unknown = set(spec) - {"id_pattern", "owner_fr", "detail_table", "attrs"}
        if unknown:
            raise _fail(where, f"unknown keys {sorted(unknown)}")
        pattern = spec.get("id_pattern")
        if not isinstance(pattern, str) or not pattern.startswith("^") or not pattern.endswith("$"):
            raise _fail(f"{where}.id_pattern", "must be a regex string anchored with ^ and $")
        try:
            id_regex = re.compile(pattern)
        except re.error as exc:
            raise _fail(f"{where}.id_pattern", f"invalid regex: {exc}") from None
        owner = spec.get("owner_fr")
        if owner not in OWNER_RULES:
            raise _fail(f"{where}.owner_fr", f"must be one of {list(OWNER_RULES)}, got {owner!r}")
        detail = spec.get("detail_table")
        if detail is not None and detail not in DETAIL_TABLES:
            raise _fail(f"{where}.detail_table", f"must be one of {list(DETAIL_TABLES)}, got {detail!r}")
        node_types[name] = NodeType(name, id_regex, owner, detail, _attr_spec(spec.get("attrs"), f"{where}.attrs", valid_types))

    # The DB triggers hard-code these types as reference targets, so the schema must define them.
    for required_type in ("FR", "Entity", "Field", "Rule", "Source"):
        if required_type not in node_types:
            raise _fail("node_types", f"missing required node type {required_type!r}")

    edge_verbs: dict[str, EdgeVerb] = {}
    for name, spec in _mapping(raw["edge_verbs"], "edge_verbs").items():
        where = f"edge_verbs.{name}"
        if not isinstance(name, str) or not re.fullmatch(r"[a-z]+( [a-z]+)*", name):
            raise _fail(where, "verb names must be lowercase words separated by single spaces")
        spec = _mapping(spec, where)
        unknown = set(spec) - {"pairs", "attrs"}
        if unknown:
            raise _fail(where, f"unknown keys {sorted(unknown)}")
        raw_pairs = spec.get("pairs")
        if not isinstance(raw_pairs, list) or not raw_pairs:
            raise _fail(f"{where}.pairs", "expected a non-empty list of [from_type, to_type]")
        pairs: set[tuple[str, str]] = set()
        for i, pair in enumerate(raw_pairs):
            if not isinstance(pair, list) or len(pair) != 2:
                raise _fail(f"{where}.pairs[{i}]", f"expected [from_type, to_type], got {pair!r}")
            for end in pair:
                if end not in node_types:
                    raise _fail(f"{where}.pairs[{i}]", f"unknown node type {end!r}")
            if tuple(pair) in pairs:
                raise _fail(f"{where}.pairs[{i}]", f"duplicate pair {pair!r}")
            pairs.add((pair[0], pair[1]))
        edge_verbs[name] = EdgeVerb(name, frozenset(pairs), _attr_spec(spec.get("attrs"), f"{where}.attrs", valid_types))

    return Schema(version, enums, attr_types, node_types, edge_verbs)


def load_schema(path: Path | str = SCHEMA_PATH) -> Schema:
    """Read and validate schema.yaml."""
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SchemaError(f"cannot read schema file {path}: {exc}") from None
    try:
        raw = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise SchemaError(f"schema file {path} is not valid YAML: {exc}") from None
    return parse_schema(raw)


def connect(path: Path | str) -> sqlite3.Connection:
    """Open the graph DB with foreign keys enforced. Fails if this SQLite build cannot enforce them."""
    conn = sqlite3.connect(str(path))
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        if conn.execute("PRAGMA foreign_keys").fetchone()[0] != 1:
            raise sqlite3.DatabaseError("this SQLite build cannot enforce foreign keys")
    except Exception:
        conn.close()
        raise
    return conn


def open_db(path: Path | str, schema: Schema | None = None, read_only: bool = False) -> sqlite3.Connection:
    """Open an existing graph DB. Never creates a file, unlike a plain sqlite3.connect.

    read_only opens it with mode=ro. With schema, a DB built from another schema version is refused.
    """
    path = Path(path).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"database {path} does not exist; create it with init_db.py")
    conn = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True) if read_only else connect(path)
    if schema is not None:
        db_version = conn.execute("PRAGMA user_version").fetchone()[0]
        if db_version != schema.version:
            conn.close()
            raise sqlite3.DatabaseError(
                f"database {path} has schema version {db_version} but schema.yaml is version {schema.version}; migrate first"
            )
    return conn


def parse_attrs(raw: str | None, where: str) -> dict[str, Any]:
    """Decode an attrs JSON column. The DB CHECK guarantees an object; this guards older or hand-built files."""
    try:
        value = json.loads(raw or "{}")
    except json.JSONDecodeError as exc:
        raise ValueError(f"{where}: attrs is not valid JSON: {exc}") from None
    if not isinstance(value, dict):
        raise ValueError(f"{where}: attrs must be a JSON object")
    return value


def validate_fr(conn: sqlite3.Connection, schema: Schema, fr: str) -> None:
    """Raise ValueError unless fr is an FR node in the graph."""
    if not schema.id_pattern("FR").match(fr):
        raise ValueError(f"{fr!r} is not an FR id (expected FR-NNN)")
    row = conn.execute("SELECT type FROM nodes WHERE id = ?", (fr,)).fetchone()
    if row is None or row[0] != "FR":
        raise ValueError(f"{fr} is not an FR in the graph")


@dataclass(frozen=True)
class Node:
    id: str
    type: str
    owner_fr: str | None
    title: str
    status: str
    attrs: dict[str, Any]


@dataclass(frozen=True)
class Edge:
    from_id: str
    verb: str
    to_id: str
    attrs: dict[str, Any]


@dataclass
class Graph:
    """The whole graph read into memory. Live edges are those whose two ends are both active."""

    nodes: dict[str, Node]
    edges: list[Edge]
    calculated_by: dict[str, str | None]  # fields.id -> fields.calculated_by
    entity_of: dict[str, str]  # fields.id -> fields.entity_id
    active: dict[str, Node] = field(init=False)
    live_edges: list[Edge] = field(init=False)
    _live_from: dict[tuple[str, str], list[Edge]] = field(init=False, repr=False)
    _live_to: dict[tuple[str, str], list[Edge]] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.active = {k: n for k, n in self.nodes.items() if n.status == ACTIVE}
        self.live_edges = [e for e in self.edges if e.from_id in self.active and e.to_id in self.active]
        self._live_from = defaultdict(list)
        self._live_to = defaultdict(list)
        for e in self.live_edges:
            self._live_from[(e.from_id, e.verb)].append(e)
            self._live_to[(e.to_id, e.verb)].append(e)

    def of_type(self, node_type: str) -> list[Node]:
        return [n for n in self.active.values() if n.type == node_type]

    def edges_from(self, node_id: str, verb: str) -> list[Edge]:
        """Live edges with this verb leaving node_id, in insertion order."""
        return self._live_from.get((node_id, verb), [])

    def edges_to(self, node_id: str, verb: str) -> list[Edge]:
        """Live edges with this verb arriving at node_id, in insertion order."""
        return self._live_to.get((node_id, verb), [])

    def out(self, verb: str) -> dict[str, list[Edge]]:
        """Live edges with this verb, grouped by from_id."""
        grouped: dict[str, list[Edge]] = defaultdict(list)
        for e in self.live_edges:
            if e.verb == verb:
                grouped[e.from_id].append(e)
        return grouped

    def into(self, verb: str) -> dict[str, list[Edge]]:
        """Live edges with this verb, grouped by to_id."""
        grouped: dict[str, list[Edge]] = defaultdict(list)
        for e in self.live_edges:
            if e.verb == verb:
                grouped[e.to_id].append(e)
        return grouped


def load_graph(conn: sqlite3.Connection) -> Graph:
    """Read every node, edge and field link into a Graph."""
    nodes = {
        r[0]: Node(r[0], r[1], r[2], r[3], r[4], parse_attrs(r[5], f"node {r[0]}"))
        for r in conn.execute("SELECT id, type, owner_fr, title, status, attrs FROM nodes")
    }
    edges = [
        Edge(r[0], r[1], r[2], parse_attrs(r[3], f"edge {r[0]} {r[1]} {r[2]}"))
        for r in conn.execute("SELECT from_id, verb, to_id, attrs FROM edges ORDER BY rowid")
    ]
    calculated_by: dict[str, str | None] = {}
    entity_of: dict[str, str] = {}
    for fid, entity_id, calc in conn.execute("SELECT id, entity_id, calculated_by FROM fields"):
        calculated_by[fid] = calc
        entity_of[fid] = entity_id
    return Graph(nodes, edges, calculated_by, entity_of)
