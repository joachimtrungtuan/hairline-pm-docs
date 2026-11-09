"""Migrate a version 4 graph DB to schema version 5 in place, after backing it up.

Usage: migrate_schema_v5.py [--db DB_PATH]

Version 5 adds the edge verbs `references` (an FR cites a Rule homed in another FR or in the system
PRD) and `applies to` (a Rule constrains an Actor, Screen, Entity, Field or Event), the optional Rule
attributes `aliases` and `scope`, and the FR-SYS / REQ-SYS-NNN id forms. Attributes and id patterns
need no DB change, because attrs are JSON and patterns are checked by write.py. The verbs do: init_db.py writes the verb list into a CHECK on edges.verb, and SQLite cannot alter a CHECK, so
the edges table is rebuilt with the new list and every row copied in rowid order. The DB's
PRAGMA user_version then becomes 5, which write.py and query.py require to match schema.yaml.

Run it only after schema.yaml says version 5 and lists the new verb:

    version: 5
    ...
      applies to:
        pairs: [[Rule, Actor], [Rule, Screen], [Rule, Entity], [Rule, Field], [Rule, Event]]
      references:
        pairs: [[FR, Rule]]

The DB is copied to backups/graph-YYYYMMDD-HHMMSS.db first. The rebuild runs in one transaction with
foreign keys checked before commit; on any error nothing changes. Exit codes: 0 migrated, 1 schema or
DB not in the expected state, 2 database error.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sqlite3
import sys
from pathlib import Path

from common import DEFAULT_DB_PATH, Schema, SchemaError, connect, load_schema
from init_db import backup_path_for, build_ddl

FROM_VERSION, TO_VERSION = 4, 5
NEW_VERBS = ("references", "applies to")


class MigrationError(ValueError):
    """The schema or DB is not in the state this migration expects; nothing was changed."""


def _edges_ddl(schema: Schema) -> list[str]:
    """The CREATE TABLE and CREATE INDEX statements for edges, taken from init_db so both stay identical."""
    ddl = build_ddl(schema)
    table = re.search(r"CREATE TABLE edges \(.*?\) STRICT;", ddl, re.S)
    indexes = re.findall(r"CREATE INDEX \w+ ON edges\([^)]*\);", ddl)
    if table is None or not indexes:
        raise MigrationError("init_db.build_ddl no longer has the expected edges table and index")
    return [table.group(0), *indexes]


def migrate(db_path: Path, schema: Schema) -> Path:
    """Rebuild the edges table for the new verb list and set user_version. Returns the backup path."""
    missing = [verb for verb in NEW_VERBS if verb not in schema.edge_verbs]
    if schema.version != TO_VERSION or missing:
        raise MigrationError(f"schema.yaml must be version {TO_VERSION} with the verbs {list(NEW_VERBS)}; update it first")
    if not db_path.is_file():
        raise MigrationError(f"database {db_path} does not exist")
    conn = connect(db_path)
    try:
        version = conn.execute("PRAGMA user_version").fetchone()[0]
        if version != FROM_VERSION:
            raise MigrationError(f"database {db_path} is version {version}, not {FROM_VERSION}")
        before = conn.execute("SELECT rowid, from_id, verb, to_id, attrs FROM edges ORDER BY rowid").fetchall()
        backup = backup_path_for(db_path)
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(db_path, backup)
        # Foreign keys must be off while the table is swapped (SQLite's documented ALTER procedure);
        # foreign_key_check below proves nothing broke before the commit.
        conn.execute("PRAGMA foreign_keys = OFF")
        conn.execute("BEGIN IMMEDIATE")
        try:
            conn.execute("ALTER TABLE edges RENAME TO edges_v4")
            conn.execute("DROP INDEX edges_to_id")
            for statement in _edges_ddl(schema):
                conn.execute(statement)
            conn.execute("INSERT INTO edges (rowid, from_id, verb, to_id, attrs) SELECT rowid, from_id, verb, to_id, attrs FROM edges_v4")
            conn.execute("DROP TABLE edges_v4")
            if conn.execute("PRAGMA foreign_key_check").fetchall():
                raise MigrationError("foreign key check failed after the rebuild")
            after = conn.execute("SELECT rowid, from_id, verb, to_id, attrs FROM edges ORDER BY rowid").fetchall()
            if after != before:
                raise MigrationError("edges differ after the rebuild")
            conn.execute(f"PRAGMA user_version = {TO_VERSION}")
            conn.commit()
        except BaseException:
            conn.rollback()
            raise
        finally:
            conn.execute("PRAGMA foreign_keys = ON")
    finally:
        conn.close()
    return backup


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Migrate a version 4 graph DB to schema version 5.")
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH), help="DB file (default: graph.db in the graph folder)")
    args = parser.parse_args(argv)
    try:
        backup = migrate(Path(args.db).resolve(), load_schema())
    except (SchemaError, MigrationError) as exc:
        print(f"migrate: {exc}", file=sys.stderr)
        return 1
    except (OSError, sqlite3.Error) as exc:
        print(f"migrate: database error, nothing changed: {exc}", file=sys.stderr)
        return 2
    print(f"Backed up to {backup}; {args.db} is now schema version {TO_VERSION}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
