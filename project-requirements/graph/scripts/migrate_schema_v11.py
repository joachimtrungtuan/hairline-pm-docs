"""Migrate a version 10 graph DB to schema version 11, after backing it up.

Usage: migrate_schema_v11.py [--db DB_PATH]

Version 11 adds two optional Screen attributes, `display_only` (bool) and `display_only_reason` (text), which
mark a Screen that legitimately shows no stored Field so lint L03 skips it. Both live only inside the JSON
attrs of Screen nodes, so no table, CHECK or trigger changes. The migration therefore keeps every row and only
moves PRAGMA user_version from 10 to 11, which write.py, query.py and the other scripts require to match
schema.yaml. Before touching the DB it proves the DDL is exactly what init_db.build_ddl writes for the new
schema, so a DB that drifted from its schema is refused instead of being stamped as version 11. The old DB is
first copied to backups/graph-YYYYMMDD-HHMMSS.db.

Run it only after schema.yaml says version 11 and lists both attributes on Screen. Exit codes: 0 migrated,
1 schema or DB not in the expected state, 2 database error. On any error the DB keeps its old version.
"""

from __future__ import annotations

import argparse
import shutil
import sqlite3
import sys
from pathlib import Path

from common import DEFAULT_DB_PATH, Schema, SchemaError, connect, load_schema
from init_db import backup_path_for, build_ddl

FROM_VERSION, TO_VERSION = 10, 11
NEW_SCREEN_ATTRS = ("display_only", "display_only_reason")
_DDL_QUERY = "SELECT type, name, sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%' ORDER BY type, name"


class MigrationError(ValueError):
    """The schema or DB is not in the state this migration expects; nothing was changed."""


def _expected_ddl(schema: Schema) -> list[tuple]:
    """The DDL a new DB gets from this schema, read back from an in-memory DB."""
    conn = sqlite3.connect(":memory:")
    try:
        conn.executescript(build_ddl(schema))
        return conn.execute(_DDL_QUERY).fetchall()
    finally:
        conn.close()


def migrate(db_path: Path, schema: Schema) -> Path:
    """Set user_version to 11 after checking the DDL and taking a backup. Returns the backup path."""
    screen_attrs = schema.node_types["Screen"].attrs.optional
    if schema.version != TO_VERSION or any(a not in screen_attrs for a in NEW_SCREEN_ATTRS):
        raise MigrationError(f"schema.yaml must be version {TO_VERSION} with {', '.join(NEW_SCREEN_ATTRS)} on Screen; update it first")
    if not db_path.is_file():
        raise MigrationError(f"database {db_path} does not exist")
    conn = connect(db_path)
    try:
        version = conn.execute("PRAGMA user_version").fetchone()[0]
        if version != FROM_VERSION:
            raise MigrationError(f"database {db_path} is version {version}, not {FROM_VERSION}")
        if conn.execute(_DDL_QUERY).fetchall() != _expected_ddl(schema):
            raise MigrationError(f"database {db_path} does not have the DDL that schema.yaml version {TO_VERSION} produces")
    finally:
        conn.close()

    backup = backup_path_for(db_path)
    backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(db_path, backup)

    conn = connect(db_path)
    try:
        conn.execute(f"PRAGMA user_version = {TO_VERSION}")
        if conn.execute("PRAGMA user_version").fetchone()[0] != TO_VERSION:
            raise MigrationError("DB does not carry the new user_version")
        if conn.execute("PRAGMA foreign_key_check").fetchall():
            raise MigrationError("foreign key check failed")
    finally:
        conn.close()
    return backup


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Migrate a version 10 graph DB to schema version 11.")
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
