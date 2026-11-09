"""Migrate a version 5 graph DB to schema version 6, after backing it up.

Usage: migrate_schema_v6.py [--db DB_PATH]

Version 6 adds the flow model (D42): the node types Step and Flow, and the edge verbs `done by`, `at`, `on`,
`applies`, `next` and `starts at`. init_db.py writes the node type list into a CHECK on nodes.type and the
verb list into a CHECK on edges.verb. SQLite cannot alter a CHECK, and rebuilding `nodes` in place would
make SQLite rewrite the foreign keys and triggers of every table that names it. So the migration builds a
fresh DB beside the old one from init_db.build_ddl (the exact DDL a new DB gets), copies every row of every
table with its rowid, proves each table's rows are identical and that foreign keys hold, and only then
replaces the old file. The old DB is first copied to backups/graph-YYYYMMDD-HHMMSS.db.

Run it only after schema.yaml says version 6 and lists the new types and verbs. Exit codes: 0 migrated,
1 schema or DB not in the expected state, 2 database error. On any error the old DB is left unchanged.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sqlite3
import sys
from pathlib import Path

from common import DEFAULT_DB_PATH, Schema, SchemaError, connect, load_schema
from init_db import backup_path_for, build_ddl

FROM_VERSION, TO_VERSION = 5, 6
NEW_TYPES = ("Step", "Flow")
NEW_VERBS = ("done by", "at", "on", "applies", "next", "starts at")
# Parents before children, so the copy order matches the foreign keys even though they are checked at the end.
TABLES = ("nodes", "fields", "enum_values", "edges", "sources", "changes")


class MigrationError(ValueError):
    """The schema or DB is not in the state this migration expects; nothing was changed."""


def _columns(conn: sqlite3.Connection, schema_name: str, table: str) -> list[str]:
    return [row[1] for row in conn.execute(f"PRAGMA {schema_name}.table_info({table})")]


def _rows(conn: sqlite3.Connection, schema_name: str, table: str, columns: list[str]) -> list[tuple]:
    cols = ", ".join(f'"{c}"' for c in columns)
    return conn.execute(f"SELECT rowid, {cols} FROM {schema_name}.{table} ORDER BY rowid").fetchall()


def migrate(db_path: Path, schema: Schema) -> Path:
    """Rebuild the DB under the version 6 DDL and replace the old file. Returns the backup path."""
    missing = [t for t in NEW_TYPES if t not in schema.node_types] + [v for v in NEW_VERBS if v not in schema.edge_verbs]
    if schema.version != TO_VERSION or missing:
        raise MigrationError(f"schema.yaml must be version {TO_VERSION} with {list(NEW_TYPES + NEW_VERBS)}; missing {missing}")
    if not db_path.is_file():
        raise MigrationError(f"database {db_path} does not exist")
    old = connect(db_path)
    try:
        version = old.execute("PRAGMA user_version").fetchone()[0]
        if version != FROM_VERSION:
            raise MigrationError(f"database {db_path} is version {version}, not {FROM_VERSION}")
    finally:
        old.close()

    backup = backup_path_for(db_path)
    backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(db_path, backup)

    new_path = db_path.with_name(db_path.name + ".v6-tmp")
    if new_path.exists():
        new_path.unlink()
    conn = sqlite3.connect(new_path, isolation_level=None)
    try:
        conn.executescript(build_ddl(schema))
        conn.execute("ATTACH DATABASE ? AS old", (str(db_path),))
        conn.execute("PRAGMA foreign_keys = OFF")
        conn.execute("BEGIN IMMEDIATE")
        for table in TABLES:
            columns = _columns(conn, "old", table)
            if columns != _columns(conn, "main", table):
                raise MigrationError(f"table {table} has different columns in the old DB")
            cols = ", ".join(f'"{c}"' for c in columns)
            conn.execute(f"INSERT INTO main.{table} (rowid, {cols}) SELECT rowid, {cols} FROM old.{table} ORDER BY rowid")
            if _rows(conn, "main", table, columns) != _rows(conn, "old", table, columns):
                raise MigrationError(f"table {table} differs after the copy")
        conn.execute("COMMIT")
        conn.execute("PRAGMA foreign_keys = ON")
        if conn.execute("PRAGMA main.foreign_key_check").fetchall():
            raise MigrationError("foreign key check failed after the copy")
        if conn.execute("PRAGMA main.integrity_check").fetchone()[0] != "ok":
            raise MigrationError("integrity check failed after the copy")
        if conn.execute("PRAGMA main.user_version").fetchone()[0] != TO_VERSION:
            raise MigrationError("new DB does not carry the new user_version")
        conn.execute("DETACH DATABASE old")
    except BaseException:
        if conn.in_transaction:
            conn.execute("ROLLBACK")
        conn.close()
        new_path.unlink(missing_ok=True)
        raise
    conn.close()
    os.replace(new_path, db_path)
    return backup


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Migrate a version 5 graph DB to schema version 6.")
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
