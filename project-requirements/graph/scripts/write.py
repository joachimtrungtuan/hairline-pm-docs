"""Apply one change-set file to the requirements graph DB in a single transaction.

Usage: write.py CHANGESET_FILE [--db DB_PATH]

A change-set is a JSON (.json) or YAML (any other suffix) mapping:

    reason: why the change is made            (required)
    by: who makes it                          (required)
    source_id: SRC-...                        (optional; a Source node, existing or added in this change-set)
    operations: [ {op: <name>, ...}, ... ]    (required, applied in order)

Operations and their keys (? marks optional keys):

    add_node          id, type, title, owner_fr?, status?, attrs?      (not for Field or Source)
    update_node       id, title?, owner_fr?, status?, attrs?, source?  (attrs merge; a null value removes the key;
                                                                       source updates a Source node's sources row)
    retire_node       id
    add_field         id, entity_id, name, data_type, title, owner_fr?, required?, calculated_by?, status?, attrs?
    update_field      id, data_type?, required?, calculated_by?        (null calculated_by clears it)
    add_enum_value    field_id, value, label?, sort_order?             (omitted sort_order: highest on the field + 1, or 0)
    retire_enum_value field_id, value
    add_edge          from, verb, to, attrs?
    remove_edge       from, verb, to
    add_source        id, title, kind, ref, lifecycle, section?, date?, attrs?

Every operation is validated against schema.yaml before anything is written. The whole
change-set is rejected if any operation is invalid.

Exit codes: 0 applied, 1 change-set invalid (nothing written), 2 database error (nothing written).
"""

from __future__ import annotations

import argparse
import json
import secrets
import sqlite3
import sys
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Callable

import yaml

from common import DEFAULT_DB_PATH, AttrSpec, Schema, SchemaError, load_schema, open_db

CALCULATED_BY = "calculated by"
TOP_LEVEL_KEYS = {"reason", "by", "source_id", "operations"}
SOURCE_COLUMNS = ("kind", "ref", "section", "date", "lifecycle")
FIELD_COLUMNS = ("entity_id", "name", "data_type", "required", "calculated_by")

# op name -> (required keys, optional keys), excluding "op" itself.
OP_KEYS: dict[str, tuple[set[str], set[str]]] = {
    "add_node": ({"id", "type", "title"}, {"owner_fr", "status", "attrs"}),
    "update_node": ({"id"}, {"title", "owner_fr", "status", "attrs", "source"}),
    "retire_node": ({"id"}, set()),
    "add_field": ({"id", "entity_id", "name", "data_type", "title"}, {"owner_fr", "required", "calculated_by", "status", "attrs"}),
    "update_field": ({"id"}, {"data_type", "required", "calculated_by"}),
    "add_enum_value": ({"field_id", "value"}, {"label", "sort_order"}),
    "retire_enum_value": ({"field_id", "value"}, set()),
    "add_edge": ({"from", "verb", "to"}, {"attrs"}),
    "remove_edge": ({"from", "verb", "to"}, set()),
    "add_source": ({"id", "title", "kind", "ref", "lifecycle"}, {"section", "date", "attrs"}),
}

# Keys that look like updates but would break an invariant; named so the error explains why.
IMMUTABLE_KEYS = {
    "update_node": {"type": "a node's type is immutable; retire it and add a new node",
                    "new_id": "a node's id is immutable once cited; change its title instead"},
    "update_field": {"entity_id": "a field's entity is part of its id and cannot change; add a new field",
                     "name": "a field's name is part of its id and cannot change; change the node title instead"},
}


class ChangeSetError(ValueError):
    """The change-set is invalid. Carries every problem found; nothing was written."""

    def __init__(self, problems: list[str]) -> None:
        self.problems = list(problems)
        super().__init__("\n".join(self.problems))


def encode(value: Any) -> str | None:
    """Serialise a value for changes.old_value/new_value. JSON keeps types so history can be replayed."""
    return None if value is None else json.dumps(value, ensure_ascii=False, sort_keys=True)


def utc_iso(moment: datetime) -> str:
    """Fixed-width UTC timestamp, so string order equals time order."""
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    return moment.astimezone(timezone.utc).isoformat(timespec="microseconds")


def _normalise_dates(value: Any) -> Any:
    """YAML turns unquoted 2026-10-16 into a date object; store dates as ISO strings like JSON input does."""
    if isinstance(value, dict):
        return {k: _normalise_dates(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_normalise_dates(v) for v in value]
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return value


def load_changeset(path: Path | str) -> dict[str, Any]:
    """Read a change-set file. Raises ChangeSetError when it cannot be read or parsed."""
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ChangeSetError([f"cannot read change-set file {path}: {exc}"]) from None
    try:
        data = json.loads(text) if path.suffix.lower() == ".json" else yaml.safe_load(text)
    except (json.JSONDecodeError, yaml.YAMLError) as exc:
        raise ChangeSetError([f"change-set file {path} cannot be parsed: {exc}"]) from None
    return _normalise_dates(data)


def _is_iso_date(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 10:
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def _value_problem(schema: Schema, attr_type: str, value: Any) -> str | None:
    """Return why value does not fit attr_type, or None when it fits."""
    if attr_type == "text":
        ok = isinstance(value, str) and value.strip() != ""
        expected = "a non-empty string"
    elif attr_type == "int":
        ok = isinstance(value, int) and not isinstance(value, bool)
        expected = "an integer"
    elif attr_type == "bool":
        ok = isinstance(value, bool)
        expected = "true or false"
    elif attr_type == "date":
        ok = _is_iso_date(value)
        expected = "a YYYY-MM-DD date"
    else:
        allowed = schema.enum(attr_type)
        ok = isinstance(value, str) and value in allowed
        expected = f"one of {list(allowed)}"
    return None if ok else f"must be {expected}, got {value!r}"


def _attr_problems(schema: Schema, spec: AttrSpec, attrs: dict[str, Any]) -> list[str]:
    allowed = {**spec.required, **spec.optional}
    problems = []
    for key, value in attrs.items():
        if key not in allowed:
            problems.append(f"attribute {key!r} is not allowed (allowed: {sorted(allowed) or 'none'})")
            continue
        problem = _value_problem(schema, allowed[key], value)
        if problem:
            problems.append(f"attribute {key!r} {problem}")
    for key in spec.required:
        if key not in attrs:
            problems.append(f"required attribute {key!r} is missing")
    return problems


def _text_problem(value: Any, key: str) -> str | None:
    if isinstance(value, str) and value.strip():
        return None
    return f"{key} must be a non-empty string, got {value!r}"


class GraphView:
    """The graph as the change-set sees it: committed rows overlaid with earlier operations' effects."""

    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn
        self._nodes: dict[str, dict[str, Any] | None] = {}
        self._fields: dict[str, dict[str, Any] | None] = {}
        self._sources: dict[str, dict[str, Any] | None] = {}
        self._edges: dict[tuple[str, str, str], dict[str, Any] | None] = {}
        self._enums: dict[tuple[str, str], dict[str, Any] | None] = {}

    def _cached(self, cache: dict, key: Any, sql: str, params: tuple, build: Callable[[tuple], dict]) -> Any:
        if key not in cache:
            row = self.conn.execute(sql, params).fetchone()
            cache[key] = None if row is None else build(row)
        return cache[key]

    def node(self, node_id: str) -> dict[str, Any] | None:
        return self._cached(
            self._nodes, node_id,
            "SELECT type, owner_fr, title, status, attrs FROM nodes WHERE id = ?", (node_id,),
            lambda r: {"type": r[0], "owner_fr": r[1], "title": r[2], "status": r[3], "attrs": json.loads(r[4])},
        )

    def field(self, field_id: str) -> dict[str, Any] | None:
        return self._cached(
            self._fields, field_id,
            f"SELECT {', '.join(FIELD_COLUMNS)} FROM fields WHERE id = ?", (field_id,),
            lambda r: {**dict(zip(FIELD_COLUMNS, r)), "required": bool(r[3])},
        )

    def source(self, source_id: str) -> dict[str, Any] | None:
        return self._cached(
            self._sources, source_id,
            f"SELECT {', '.join(SOURCE_COLUMNS)} FROM sources WHERE id = ?", (source_id,),
            lambda r: dict(zip(SOURCE_COLUMNS, r)),
        )

    def edge(self, key: tuple[str, str, str]) -> dict[str, Any] | None:
        return self._cached(
            self._edges, key,
            "SELECT attrs FROM edges WHERE from_id = ? AND verb = ? AND to_id = ?", key,
            lambda r: json.loads(r[0]),
        )

    def enum_value(self, key: tuple[str, str]) -> dict[str, Any] | None:
        return self._cached(
            self._enums, key,
            "SELECT label, sort_order FROM enum_values WHERE field_id = ? AND value = ?", key,
            lambda r: {"label": r[0], "sort_order": r[1]},
        )

    def next_sort_order(self, field_id: str) -> int:
        """One past the field's highest sort_order, counting values added or retired earlier in this change-set."""
        rows = self.conn.execute("SELECT value, label, sort_order FROM enum_values WHERE field_id = ?", (field_id,))
        for value, label, sort_order in rows:
            self._enums.setdefault((field_id, value), {"label": label, "sort_order": sort_order})
        orders = [v["sort_order"] for (fid, _), v in self._enums.items() if fid == field_id and v is not None]
        return max(orders) + 1 if orders else 0

    def set_node(self, node_id: str, value: dict[str, Any]) -> None:
        self._nodes[node_id] = value

    def set_field(self, field_id: str, value: dict[str, Any]) -> None:
        self._fields[field_id] = value

    def set_source(self, source_id: str, value: dict[str, Any]) -> None:
        self._sources[source_id] = value

    def set_edge(self, key: tuple[str, str, str], value: dict[str, Any] | None) -> None:
        self._edges[key] = value

    def set_enum_value(self, key: tuple[str, str], value: dict[str, Any] | None) -> None:
        self._enums[key] = value


@dataclass
class Plan:
    """SQL to run and history rows to append, built only from operations that passed validation."""

    statements: list[tuple[str, tuple]] = field(default_factory=list)
    changes: list[tuple[str, str, str | None, str | None]] = field(default_factory=list)
    created: set[str] = field(default_factory=set)

    def run(self, sql: str, *params: Any) -> None:
        self.statements.append((sql, params))

    def record(self, node_id: str, attribute: str, old: Any, new: Any) -> None:
        old_text, new_text = encode(old), encode(new)
        if old_text != new_text:
            self.changes.append((node_id, attribute, old_text, new_text))


class Planner:
    """Validates operations one by one against the schema and the evolving view, and plans their writes.

    Each handler returns its problems. A handler touches the view and plan only after all its checks pass,
    so later operations are validated against the effects of earlier valid ones.
    """

    def __init__(self, conn: sqlite3.Connection, schema: Schema) -> None:
        self.schema = schema
        self.view = GraphView(conn)
        self.plan = Plan()
        self.handlers: dict[str, Callable[[dict[str, Any]], list[str]]] = {
            name: getattr(self, f"_{name}") for name in OP_KEYS
        }

    # ---- shared checks -------------------------------------------------------------------

    def _existing(self, node_id: Any, key: str, expected_type: str | None = None) -> tuple[dict | None, str | None]:
        if not isinstance(node_id, str) or not node_id:
            return None, f"{key} must be a node id string, got {node_id!r}"
        node = self.view.node(node_id)
        if node is None:
            return None, f"{key} {node_id!r} does not exist"
        if expected_type and node["type"] != expected_type:
            return None, f"{key} {node_id!r} is a {node['type']}, not a {expected_type}"
        return node, None

    def _owner_problems(self, node_type: str, owner: Any) -> list[str]:
        rule = self.schema.node_types[node_type].owner_fr
        if owner is None:
            return [f"{node_type} nodes require an owning FR (owner_fr)"] if rule == "required" else []
        if rule == "forbidden":
            return [f"{node_type} nodes must not have an owning FR, got owner_fr {owner!r}"]
        _, problem = self._existing(owner, "owner_fr", "FR")
        return [problem] if problem else []

    def _source_problems(self, src: dict[str, Any]) -> list[str]:
        problems = [p for p in (_text_problem(src.get("kind"), "kind"), _text_problem(src.get("ref"), "ref")) if p]
        if src.get("section") is not None and _text_problem(src["section"], "section"):
            problems.append(_text_problem(src["section"], "section"))
        if src.get("date") is not None and not _is_iso_date(src["date"]):
            problems.append(f"date must be a YYYY-MM-DD date, got {src['date']!r}")
        lifecycles = self.schema.enum("source_lifecycle")
        if src.get("lifecycle") not in lifecycles:
            problems.append(f"lifecycle must be one of {list(lifecycles)}, got {src.get('lifecycle')!r}")
        return problems

    def _new_node(self, op: dict[str, Any], node_type: str) -> tuple[dict[str, Any] | None, list[str]]:
        """Check the common parts of any node creation; return the node record when they pass."""
        problems = []
        node_id = op.get("id")
        if not isinstance(node_id, str) or not self.schema.id_pattern(node_type).fullmatch(node_id):
            problems.append(f"id {node_id!r} does not match the {node_type} pattern {self.schema.id_pattern(node_type).pattern}")
        elif self.view.node(node_id) is not None:
            problems.append(f"node {node_id!r} already exists")
        if problem := _text_problem(op.get("title"), "title"):
            problems.append(problem)
        problems += self._owner_problems(node_type, op.get("owner_fr"))
        status = op.get("status", "active")
        if status not in self.schema.enum("node_status"):
            problems.append(f"status must be one of {list(self.schema.enum('node_status'))}, got {status!r}")
        attrs = op.get("attrs", {})
        if not isinstance(attrs, dict):
            problems.append(f"attrs must be a mapping, got {attrs!r}")
        else:
            problems += _attr_problems(self.schema, self.schema.node_types[node_type].attrs, attrs)
        if problems:
            return None, problems
        return {"type": node_type, "owner_fr": op.get("owner_fr"), "title": op["title"], "status": status, "attrs": dict(attrs)}, []

    def _create_node(self, node_id: str, node: dict[str, Any]) -> None:
        self.view.set_node(node_id, node)
        self.plan.created.add(node_id)
        self.plan.run(
            "INSERT INTO nodes (id, type, owner_fr, title, status, attrs) VALUES (?, ?, ?, ?, ?, ?)",
            node_id, node["type"], node["owner_fr"], node["title"], node["status"], json.dumps(node["attrs"], ensure_ascii=False),
        )
        for attribute in ("type", "title", "owner_fr", "status"):
            self.plan.record(node_id, attribute, None, node[attribute])
        for key, value in sorted(node["attrs"].items()):
            self.plan.record(node_id, f"attrs.{key}", None, value)

    def _set_calculated_by(self, field_id: str, old: str | None, new: str | None) -> None:
        """fields.calculated_by and the `calculated by` edge always change together, recorded as one attribute."""
        current = dict(self.view.field(field_id) or {})
        current["calculated_by"] = new
        self.view.set_field(field_id, current)
        self.plan.run("UPDATE fields SET calculated_by = ? WHERE id = ?", new, field_id)
        if old is not None:
            self.view.set_edge((field_id, CALCULATED_BY, old), None)
            self.plan.run("DELETE FROM edges WHERE from_id = ? AND verb = ? AND to_id = ?", field_id, CALCULATED_BY, old)
        if new is not None:
            self.view.set_edge((field_id, CALCULATED_BY, new), {})
            self.plan.run("INSERT INTO edges (from_id, verb, to_id) VALUES (?, ?, ?)", field_id, CALCULATED_BY, new)
        self.plan.record(field_id, "field.calculated_by", old, new)

    def _edge_key(self, op: dict[str, Any]) -> tuple[tuple[str, str, str] | None, dict | None, dict | None, list[str]]:
        problems = []
        verb = op.get("verb")
        if not isinstance(verb, str) or verb not in self.schema.edge_verbs:
            problems.append(f"unknown edge verb {verb!r}; known: {sorted(self.schema.edge_verbs)}")
        src, p1 = self._existing(op.get("from"), "from")
        dst, p2 = self._existing(op.get("to"), "to")
        problems += [p for p in (p1, p2) if p]
        if problems:
            return None, None, None, problems
        return (op["from"], verb, op["to"]), src, dst, []

    # ---- operations ----------------------------------------------------------------------

    def _add_node(self, op: dict[str, Any]) -> list[str]:
        node_type = op.get("type")
        if not isinstance(node_type, str) or node_type not in self.schema.node_types:
            return [f"unknown node type {node_type!r}; known: {sorted(self.schema.node_types)}"]
        detail = self.schema.node_types[node_type].detail_table
        if detail == "fields":
            return [f"{node_type} nodes need a fields row too; use add_field"]
        if detail == "sources":
            return [f"{node_type} nodes need a sources row too; use add_source"]
        node, problems = self._new_node(op, node_type)
        if problems:
            return problems
        self._create_node(op["id"], node)
        return []

    def _update_node(self, op: dict[str, Any]) -> list[str]:
        node, problem = self._existing(op.get("id"), "id")
        if problem:
            return [problem]
        updates = set(op) & OP_KEYS["update_node"][1]
        if not updates:
            return ["nothing to update; give title, owner_fr, status, attrs or source"]
        node_id, node_type = op["id"], node["type"]
        new = {**node, "attrs": dict(node["attrs"])}
        problems = []
        if "title" in op:
            if problem := _text_problem(op["title"], "title"):
                problems.append(problem)
            new["title"] = op["title"]
        if "owner_fr" in op:
            problems += self._owner_problems(node_type, op["owner_fr"])
            new["owner_fr"] = op["owner_fr"]
        if "status" in op:
            if op["status"] not in self.schema.enum("node_status"):
                problems.append(f"status must be one of {list(self.schema.enum('node_status'))}, got {op['status']!r}")
            new["status"] = op["status"]
        if "attrs" in op:
            if not isinstance(op["attrs"], dict) or not op["attrs"]:
                problems.append(f"attrs must be a non-empty mapping, got {op['attrs']!r}")
            else:
                for key, value in op["attrs"].items():
                    if value is None:
                        new["attrs"].pop(key, None)
                    else:
                        new["attrs"][key] = value
                problems += _attr_problems(self.schema, self.schema.node_types[node_type].attrs, new["attrs"])
        old_src = new_src = None
        if "source" in op:
            if self.schema.node_types[node_type].detail_table != "sources":
                problems.append(f"source applies only to Source nodes; {node_id!r} is a {node_type}")
            elif not isinstance(op["source"], dict) or not op["source"] or set(op["source"]) - set(SOURCE_COLUMNS):
                problems.append(f"source must be a non-empty mapping with keys from {list(SOURCE_COLUMNS)}, got {op['source']!r}")
            else:
                old_src = self.view.source(node_id) or {}
                new_src = {**old_src, **op["source"]}
                problems += self._source_problems(new_src)
        if problems:
            return problems
        before = len(self.plan.changes)
        for attribute in ("title", "owner_fr", "status"):
            self.plan.record(node_id, attribute, node[attribute], new[attribute])
        for key in sorted(set(node["attrs"]) | set(new["attrs"])):
            self.plan.record(node_id, f"attrs.{key}", node["attrs"].get(key), new["attrs"].get(key))
        if new_src is not None:
            for column in SOURCE_COLUMNS:
                self.plan.record(node_id, f"source.{column}", old_src.get(column), new_src.get(column))
        if len(self.plan.changes) == before:
            return ["the update changes nothing"]
        self.view.set_node(node_id, new)
        self.plan.run(
            "UPDATE nodes SET title = ?, owner_fr = ?, status = ?, attrs = ? WHERE id = ?",
            new["title"], new["owner_fr"], new["status"], json.dumps(new["attrs"], ensure_ascii=False), node_id,
        )
        if new_src is not None:
            self.view.set_source(node_id, new_src)
            self.plan.run(
                f"UPDATE sources SET {', '.join(c + ' = ?' for c in SOURCE_COLUMNS)} WHERE id = ?",
                *(new_src.get(c) for c in SOURCE_COLUMNS), node_id,
            )
        return []

    def _retire_node(self, op: dict[str, Any]) -> list[str]:
        node, problem = self._existing(op.get("id"), "id")
        if problem:
            return [problem]
        if node["status"] == "retired":
            return [f"node {op['id']!r} is already retired"]
        self.view.set_node(op["id"], {**node, "status": "retired"})
        self.plan.run("UPDATE nodes SET status = 'retired' WHERE id = ?", op["id"])
        self.plan.record(op["id"], "status", node["status"], "retired")
        return []

    def _add_field(self, op: dict[str, Any]) -> list[str]:
        node, problems = self._new_node(op, "Field")
        _, problem = self._existing(op.get("entity_id"), "entity_id", "Entity")
        if problem:
            problems.append(problem)
        if problem := _text_problem(op.get("name"), "name"):
            problems.append(problem)
        elif isinstance(op.get("entity_id"), str) and op.get("id") != f"{op['entity_id']}.{op['name']}":
            problems.append(f"id must be <entity_id>.<name> = {op['entity_id']}.{op['name']!s}, got {op.get('id')!r}")
        if problem := _text_problem(op.get("data_type"), "data_type"):
            problems.append(problem)
        required = op.get("required", False)
        if not isinstance(required, bool):
            problems.append(f"required must be true or false, got {required!r}")
        calculated_by = op.get("calculated_by")
        if calculated_by is not None:
            _, problem = self._existing(calculated_by, "calculated_by", "Rule")
            if problem:
                problems.append(problem)
        if problems:
            return problems
        field_id = op["id"]
        self._create_node(field_id, node)
        detail = {"entity_id": op["entity_id"], "name": op["name"], "data_type": op["data_type"], "required": required, "calculated_by": None}
        self.view.set_field(field_id, detail)
        self.plan.run(
            "INSERT INTO fields (id, entity_id, name, data_type, required) VALUES (?, ?, ?, ?, ?)",
            field_id, detail["entity_id"], detail["name"], detail["data_type"], int(required),
        )
        for column in ("entity_id", "name", "data_type", "required"):
            self.plan.record(field_id, f"field.{column}", None, detail[column])
        if calculated_by is not None:
            self._set_calculated_by(field_id, None, calculated_by)
        return []

    def _update_field(self, op: dict[str, Any]) -> list[str]:
        _, problem = self._existing(op.get("id"), "id", "Field")
        if problem:
            return [problem]
        field_id = op["id"]
        current = self.view.field(field_id)
        if current is None:
            return [f"Field {field_id!r} has no fields row"]
        updates = set(op) & OP_KEYS["update_field"][1]
        if not updates:
            return ["nothing to update; give data_type, required or calculated_by"]
        problems = []
        if "data_type" in op and (problem := _text_problem(op["data_type"], "data_type")):
            problems.append(problem)
        if "required" in op and not isinstance(op["required"], bool):
            problems.append(f"required must be true or false, got {op['required']!r}")
        if op.get("calculated_by") is not None:
            _, problem = self._existing(op["calculated_by"], "calculated_by", "Rule")
            if problem:
                problems.append(problem)
        if problems:
            return problems
        new = {**current, **{k: op[k] for k in ("data_type", "required") if k in op}}
        calc_changes = "calculated_by" in op and op["calculated_by"] != current["calculated_by"]
        if new == current and not calc_changes:
            return ["the update changes nothing"]
        if new != current:
            self.view.set_field(field_id, new)
            self.plan.run("UPDATE fields SET data_type = ?, required = ? WHERE id = ?", new["data_type"], int(new["required"]), field_id)
            for column in ("data_type", "required"):
                self.plan.record(field_id, f"field.{column}", current[column], new[column])
        if calc_changes:
            self._set_calculated_by(field_id, current["calculated_by"], op["calculated_by"])
        return []

    def _enum_key(self, op: dict[str, Any]) -> tuple[tuple[str, str] | None, list[str]]:
        problems = []
        _, problem = self._existing(op.get("field_id"), "field_id", "Field")
        if problem:
            problems.append(problem)
        if not isinstance(op.get("value"), str) or not op["value"]:
            problems.append(f"value must be a non-empty string, got {op.get('value')!r}")
        return (None, problems) if problems else ((op["field_id"], op["value"]), [])

    def _add_enum_value(self, op: dict[str, Any]) -> list[str]:
        key, problems = self._enum_key(op)
        if key and self.view.enum_value(key) is not None:
            problems.append(f"field {key[0]!r} already has enum value {key[1]!r}")
        label, sort_order = op.get("label"), op.get("sort_order")
        if label is not None and (problem := _text_problem(label, "label")):
            problems.append(problem)
        if sort_order is not None and (not isinstance(sort_order, int) or isinstance(sort_order, bool)):
            problems.append(f"sort_order must be an integer, got {sort_order!r}")
        if problems:
            return problems
        if sort_order is None:
            sort_order = self.view.next_sort_order(key[0])
        value = {"label": label, "sort_order": sort_order}
        self.view.set_enum_value(key, value)
        self.plan.run("INSERT INTO enum_values (field_id, value, label, sort_order) VALUES (?, ?, ?, ?)", *key, label, sort_order)
        self.plan.record(key[0], f"enum.{key[1]}", None, value)
        return []

    def _retire_enum_value(self, op: dict[str, Any]) -> list[str]:
        key, problems = self._enum_key(op)
        if problems:
            return problems
        old = self.view.enum_value(key)
        if old is None:
            return [f"field {key[0]!r} has no enum value {key[1]!r}"]
        # enum_values has no status column, so a retired value leaves the list; its history stays in changes.
        self.view.set_enum_value(key, None)
        self.plan.run("DELETE FROM enum_values WHERE field_id = ? AND value = ?", *key)
        self.plan.record(key[0], f"enum.{key[1]}", old, None)
        return []

    def _add_edge(self, op: dict[str, Any]) -> list[str]:
        key, src, dst, problems = self._edge_key(op)
        if problems:
            return problems
        from_id, verb, to_id = key
        spec = self.schema.edge_verbs[verb]
        if (src["type"], dst["type"]) not in spec.pairs:
            allowed = ", ".join(f"{a} -> {b}" for a, b in sorted(spec.pairs))
            problems.append(f"verb {verb!r} cannot join {src['type']} -> {dst['type']} (allowed: {allowed})")
        attrs = op.get("attrs", {})
        if not isinstance(attrs, dict):
            problems.append(f"attrs must be a mapping, got {attrs!r}")
        else:
            problems += [f"edge {p}" for p in _attr_problems(self.schema, spec.attrs, attrs)]
        if self.view.edge(key) is not None:
            problems.append(f"edge {from_id} {verb} {to_id} already exists")
        if not problems and verb == CALCULATED_BY:
            current = (self.view.field(from_id) or {}).get("calculated_by")
            if current is not None:
                problems.append(f"field {from_id!r} is already calculated by {current!r}; change it with update_field")
        if problems:
            return problems
        if verb == CALCULATED_BY:
            self._set_calculated_by(from_id, None, to_id)
            return []
        self.view.set_edge(key, dict(attrs))
        self.plan.run("INSERT INTO edges (from_id, verb, to_id, attrs) VALUES (?, ?, ?, ?)", *key, json.dumps(attrs, ensure_ascii=False))
        self.plan.record(from_id, f"edge:{verb}:{to_id}", None, attrs)
        return []

    def _remove_edge(self, op: dict[str, Any]) -> list[str]:
        key, _, _, problems = self._edge_key(op)
        if problems:
            return problems
        old = self.view.edge(key)
        if old is None:
            return [f"edge {key[0]} {key[1]} {key[2]} does not exist"]
        if key[1] == CALCULATED_BY:
            self._set_calculated_by(key[0], key[2], None)
            return []
        self.view.set_edge(key, None)
        self.plan.run("DELETE FROM edges WHERE from_id = ? AND verb = ? AND to_id = ?", *key)
        self.plan.record(key[0], f"edge:{key[1]}:{key[2]}", old, None)
        return []

    def _add_source(self, op: dict[str, Any]) -> list[str]:
        node, problems = self._new_node(op, "Source")
        src = {c: op.get(c) for c in SOURCE_COLUMNS}
        problems += self._source_problems(src)
        if problems:
            return problems
        source_id = op["id"]
        self._create_node(source_id, node)
        self.view.set_source(source_id, src)
        self.plan.run(
            f"INSERT INTO sources (id, {', '.join(SOURCE_COLUMNS)}) VALUES (?, ?, ?, ?, ?, ?)",
            source_id, *(src[c] for c in SOURCE_COLUMNS),
        )
        for column in SOURCE_COLUMNS:
            self.plan.record(source_id, f"source.{column}", None, src[column])
        return []

    # ---- change-set ----------------------------------------------------------------------

    def check_operation(self, op: Any) -> list[str]:
        if not isinstance(op, dict):
            return [f"must be a mapping, got {op!r}"]
        name = op.get("op")
        if not isinstance(name, str) or name not in self.handlers:
            return [f"unknown op {name!r}; known: {sorted(self.handlers)}"]
        required, optional = OP_KEYS[name]
        problems = [why for key, why in IMMUTABLE_KEYS.get(name, {}).items() if key in op]
        unknown = set(op) - required - optional - {"op"} - set(IMMUTABLE_KEYS.get(name, {}))
        if unknown:
            problems.append(f"unknown keys {sorted(unknown)}; allowed: {sorted(required | optional)}")
        missing = required - set(op)
        if missing:
            problems.append(f"missing required keys {sorted(missing)}")
        return problems or self.handlers[name](op)


def build_plan(conn: sqlite3.Connection, schema: Schema, changeset: Any) -> tuple[Plan, dict[str, Any]]:
    """Validate a whole change-set and plan its writes. Raises ChangeSetError listing every problem."""
    if not isinstance(changeset, dict):
        raise ChangeSetError([f"change-set must be a mapping with keys {sorted(TOP_LEVEL_KEYS)}"])
    problems = []
    unknown = set(changeset) - TOP_LEVEL_KEYS
    if unknown:
        problems.append(f"change-set: unknown keys {sorted(unknown)}; allowed: {sorted(TOP_LEVEL_KEYS)}")
    for key in ("reason", "by"):
        if problem := _text_problem(changeset.get(key), key):
            problems.append(f"change-set: {problem}")
    operations = changeset.get("operations")
    if not isinstance(operations, list) or not operations:
        problems.append("change-set: operations must be a non-empty list")
        operations = []
    planner = Planner(conn, schema)
    for index, op in enumerate(operations):
        name = op.get("op") if isinstance(op, dict) else None
        problems += [f"operations[{index}] ({name}): {p}" for p in planner.check_operation(op)]
    # Checked after the operations so a Source added by this change-set can be cited by it.
    source_id = changeset.get("source_id")
    if source_id is not None:
        _, problem = planner._existing(source_id, "source_id", "Source")
        if problem:
            problems.append(f"change-set: {problem}")
    if problems:
        raise ChangeSetError(problems)
    return planner.plan, {"reason": changeset["reason"], "by": changeset["by"], "source_id": source_id}


def apply_changeset(conn: sqlite3.Connection, schema: Schema, changeset: Any, now: datetime | None = None) -> tuple[str, int]:
    """Validate then apply a change-set atomically. Returns (changeset_id, number of change rows).

    Validation reads inside the same write transaction, so no other writer can change the graph
    between the checks and the writes. Any failure rolls everything back.
    """
    if conn.in_transaction:
        raise sqlite3.ProgrammingError("apply_changeset needs a connection with no open transaction")
    moment = now or datetime.now(timezone.utc)
    conn.execute("BEGIN IMMEDIATE")
    try:
        plan, meta = build_plan(conn, schema, changeset)
        for sql, params in plan.statements:
            conn.execute(sql, params)
        # One version step per change-set for each pre-existing node it touched; new nodes start at 1.
        touched = sorted({node_id for node_id, *_ in plan.changes} - plan.created)
        conn.executemany("UPDATE nodes SET version = version + 1 WHERE id = ?", [(n,) for n in touched])
        at = utc_iso(moment)
        changeset_id = f"cs-{moment.astimezone(timezone.utc):%Y%m%d-%H%M%S}-{secrets.token_hex(4)}"
        conn.executemany(
            "INSERT INTO changes (changeset_id, at, changed_by, node_id, attribute, old_value, new_value, reason, source_id) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [(changeset_id, at, meta["by"], *change, meta["reason"], meta["source_id"]) for change in plan.changes],
        )
        conn.commit()
    except BaseException:
        conn.rollback()
        raise
    return changeset_id, len(plan.changes)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Apply one change-set file to the requirements graph DB.")
    parser.add_argument("changeset", help="change-set file (.json, or YAML for any other suffix)")
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH), help="DB file (default: graph.db in the graph folder)")
    args = parser.parse_args(argv)
    try:
        schema = load_schema()
        changeset = load_changeset(args.changeset)
    except (SchemaError, ChangeSetError) as exc:
        print(f"write: {exc}", file=sys.stderr)
        return 1
    try:
        conn = open_db(args.db, schema)
    except (FileNotFoundError, sqlite3.Error) as exc:
        print(f"write: {exc}", file=sys.stderr)
        return 2
    try:
        changeset_id, rows = apply_changeset(conn, schema, changeset)
    except ChangeSetError as exc:
        print("write: change-set rejected, nothing written:", file=sys.stderr)
        for problem in exc.problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1
    except sqlite3.Error as exc:
        print(f"write: database error, nothing written: {exc}", file=sys.stderr)
        return 2
    finally:
        conn.close()
    print(f"Applied change-set {changeset_id}: {rows} change rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
