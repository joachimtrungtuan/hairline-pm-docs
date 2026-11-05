"""Create an empty requirements graph database.

Usage: init_db.py [DB_PATH] [--force]

DB_PATH defaults to graph.db in the graph folder. An existing file is never overwritten
unless --force is given; with --force the old file is first copied to
backups/graph-YYYYMMDD-HHMMSS.db next to it.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

from common import DEFAULT_DB_PATH, Schema, SchemaError, connect, load_schema

# (table, column, required node type of the referenced row). Foreign keys prove the
# referenced node exists; these triggers additionally prove it is the right kind of node.
TYPE_REFERENCES = (
    ("nodes", "owner_fr", "FR"),
    ("fields", "id", "Field"),
    ("fields", "entity_id", "Entity"),
    ("fields", "calculated_by", "Rule"),
    ("sources", "id", "Source"),
    ("changes", "source_id", "Source"),
)


def _sql_list(values: tuple[str, ...] | list[str]) -> str:
    return ", ".join("'" + v.replace("'", "''") + "'" for v in values)


def build_ddl(schema: Schema) -> str:
    """Return the full DDL. Closed value lists come from schema.yaml so the DB and schema agree."""
    types = _sql_list(sorted(schema.node_types))
    verbs = _sql_list(sorted(schema.edge_verbs))
    statuses = _sql_list(schema.enum("node_status"))
    lifecycles = _sql_list(schema.enum("source_lifecycle"))

    tables = f"""
-- Every graph node, including FRs. IDs are immutable; a node is retired by status, never deleted.
CREATE TABLE nodes (
    id       TEXT PRIMARY KEY,
    type     TEXT NOT NULL CHECK (type IN ({types})),
    owner_fr TEXT REFERENCES nodes(id),
    title    TEXT NOT NULL CHECK (length(trim(title)) > 0),
    status   TEXT NOT NULL DEFAULT 'active' CHECK (status IN ({statuses})),
    version  INTEGER NOT NULL DEFAULT 1 CHECK (version >= 1),
    attrs    TEXT NOT NULL DEFAULT '{{}}' CHECK (json_valid(attrs) AND json_type(attrs) = 'object')
) STRICT;
CREATE INDEX nodes_owner_fr ON nodes(owner_fr);
CREATE INDEX nodes_type ON nodes(type);

-- Structured definition of a Field node. Each field belongs to exactly one Entity.
CREATE TABLE fields (
    id            TEXT PRIMARY KEY REFERENCES nodes(id),
    entity_id     TEXT NOT NULL REFERENCES nodes(id),
    name          TEXT NOT NULL CHECK (length(trim(name)) > 0),
    data_type     TEXT NOT NULL CHECK (length(trim(data_type)) > 0),
    required      INTEGER NOT NULL DEFAULT 0 CHECK (required IN (0, 1)),
    calculated_by TEXT REFERENCES nodes(id),
    UNIQUE (entity_id, name)
) STRICT;
CREATE INDEX fields_calculated_by ON fields(calculated_by);

-- Allowed values of an enum Field. Removed together with their field.
CREATE TABLE enum_values (
    field_id   TEXT NOT NULL REFERENCES fields(id) ON DELETE CASCADE,
    value      TEXT NOT NULL CHECK (length(value) > 0),
    label      TEXT,
    sort_order INTEGER NOT NULL DEFAULT 0,
    UNIQUE (field_id, value)
) STRICT;

-- Typed relationships between nodes. Which node types a verb may join is checked by the write script.
CREATE TABLE edges (
    from_id TEXT NOT NULL REFERENCES nodes(id),
    verb    TEXT NOT NULL CHECK (verb IN ({verbs})),
    to_id   TEXT NOT NULL REFERENCES nodes(id),
    attrs   TEXT NOT NULL DEFAULT '{{}}' CHECK (json_valid(attrs) AND json_type(attrs) = 'object'),
    UNIQUE (from_id, verb, to_id)
) STRICT;
CREATE INDEX edges_to_id ON edges(to_id);

-- Structured record of a Source node: where a decision or requirement came from.
CREATE TABLE sources (
    id        TEXT PRIMARY KEY REFERENCES nodes(id),
    kind      TEXT NOT NULL CHECK (length(trim(kind)) > 0),
    ref       TEXT NOT NULL CHECK (length(trim(ref)) > 0),
    section   TEXT,
    date      TEXT CHECK (date IS NULL OR date GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'),
    lifecycle TEXT NOT NULL CHECK (lifecycle IN ({lifecycles}))
) STRICT;

-- Append-only history: one row per attribute change, grouped by change set.
CREATE TABLE changes (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    changeset_id TEXT NOT NULL,
    at           TEXT NOT NULL,
    changed_by   TEXT NOT NULL,
    node_id      TEXT NOT NULL REFERENCES nodes(id),
    attribute    TEXT NOT NULL,
    old_value    TEXT,
    new_value    TEXT,
    reason       TEXT NOT NULL CHECK (length(trim(reason)) > 0),
    source_id    TEXT REFERENCES sources(id)
) STRICT;
CREATE INDEX changes_changeset ON changes(changeset_id);
CREATE INDEX changes_node_id ON changes(node_id);
CREATE INDEX changes_source_id ON changes(source_id);
"""

    triggers = [
        """
-- Retire nodes by status; deleting would break citations and history.
CREATE TRIGGER nodes_no_delete BEFORE DELETE ON nodes
BEGIN SELECT RAISE(ABORT, 'nodes cannot be deleted; set status to retired'); END;

-- Node IDs are cited by other documents and must never change; rename the title instead.
CREATE TRIGGER nodes_id_immutable BEFORE UPDATE OF id ON nodes WHEN NEW.id IS NOT OLD.id
BEGIN SELECT RAISE(ABORT, 'nodes.id is immutable; change the title instead'); END;

-- Changing a node type would silently invalidate every type-checked reference to it.
CREATE TRIGGER nodes_type_immutable BEFORE UPDATE OF type ON nodes WHEN NEW.type IS NOT OLD.type
BEGIN SELECT RAISE(ABORT, 'nodes.type is immutable; retire the node and create a new one'); END;

-- A detail row stays attached to the node it describes; a Field's ID is built from its entity and name.
CREATE TRIGGER fields_key_immutable BEFORE UPDATE OF id, entity_id, name ON fields
WHEN NEW.id IS NOT OLD.id OR NEW.entity_id IS NOT OLD.entity_id OR NEW.name IS NOT OLD.name
BEGIN SELECT RAISE(ABORT, 'fields.id, entity_id and name are immutable; retire the field and add a new one'); END;
CREATE TRIGGER sources_id_immutable BEFORE UPDATE OF id ON sources WHEN NEW.id IS NOT OLD.id
BEGIN SELECT RAISE(ABORT, 'sources.id is immutable'); END;

-- History is append-only.
CREATE TRIGGER changes_no_delete BEFORE DELETE ON changes
BEGIN SELECT RAISE(ABORT, 'changes rows cannot be deleted; history is append-only'); END;
CREATE TRIGGER changes_no_update BEFORE UPDATE ON changes
BEGIN SELECT RAISE(ABORT, 'changes rows cannot be updated; history is append-only'); END;
"""
    ]
    for table, column, node_type in TYPE_REFERENCES:
        message = f"{table}.{column} must reference an existing node of type {node_type}"
        condition = f"NEW.{column} IS NOT NULL AND (SELECT type FROM nodes WHERE id = NEW.{column}) IS NOT '{node_type}'"
        for event, suffix in (("INSERT", "insert"), (f"UPDATE OF {column}", "update")):
            triggers.append(
                f"CREATE TRIGGER {table}_{column}_type_{suffix} BEFORE {event} ON {table} WHEN {condition}\n"
                f"BEGIN SELECT RAISE(ABORT, '{message}'); END;\n"
            )
    return tables + "\n".join(triggers) + f"\nPRAGMA user_version = {schema.version};\n"


def create_db(path: Path, schema: Schema) -> None:
    """Build a fresh DB at path. Built in a temp file first so a failure never leaves a half-made DB."""
    tmp = path.with_name(path.name + ".tmp")
    tmp.unlink(missing_ok=True)
    try:
        conn = connect(tmp)
        try:
            conn.executescript(build_ddl(schema))
            conn.commit()
        finally:
            conn.close()
        os.replace(tmp, path)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise


def backup_path_for(db_path: Path, now: datetime | None = None) -> Path:
    """Return an unused backups/graph-YYYYMMDD-HHMMSS.db path beside the DB."""
    stamp = (now or datetime.now()).strftime("%Y%m%d-%H%M%S")
    backups = db_path.parent / "backups"
    candidate = backups / f"graph-{stamp}.db"
    n = 1
    while candidate.exists():
        candidate = backups / f"graph-{stamp}-{n}.db"
        n += 1
    return candidate


def init_db(db_path: Path, force: bool = False, schema: Schema | None = None) -> Path | None:
    """Create the DB. Returns the backup path when an existing DB was replaced, else None."""
    schema = schema or load_schema()
    backup = None
    if db_path.exists():
        if not force:
            raise FileExistsError(f"{db_path} already exists; pass --force to replace it (a backup is made first)")
        if not db_path.is_file():
            raise FileExistsError(f"{db_path} exists and is not a regular file")
        backup = backup_path_for(db_path)
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(db_path, backup)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    create_db(db_path, schema)
    return backup


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create an empty requirements graph database.")
    parser.add_argument("db_path", nargs="?", default=str(DEFAULT_DB_PATH), help="DB file (default: graph.db in the graph folder)")
    parser.add_argument("--force", action="store_true", help="replace an existing DB after backing it up")
    args = parser.parse_args(argv)
    db_path = Path(args.db_path).resolve()
    try:
        backup = init_db(db_path, force=args.force)
    except (SchemaError, FileExistsError, OSError, sqlite3.Error) as exc:
        print(f"init_db: {exc}", file=sys.stderr)
        return 1
    if backup:
        print(f"Backed up previous DB to {backup}")
    print(f"Created {db_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
