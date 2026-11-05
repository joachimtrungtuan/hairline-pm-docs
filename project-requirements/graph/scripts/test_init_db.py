"""Tests for init_db.py and the schema loader. Run: .venv/bin/python scripts/test_init_db.py"""

from __future__ import annotations

import contextlib
import io
import sqlite3
import tempfile
import unittest
from pathlib import Path

import yaml

import init_db
from common import SCHEMA_PATH, SchemaError, connect, load_schema, parse_schema

EXPECTED_TABLES = {"nodes", "fields", "enum_values", "edges", "sources", "changes"}


class InitDbTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.db_path = self.dir / "graph.db"
        init_db.init_db(self.db_path)
        self.conn = connect(self.db_path)
        self.conn.executemany(
            "INSERT INTO nodes (id, type, owner_fr, title) VALUES (?, ?, ?, ?)",
            [
                ("FR-004", "FR", None, "Quote management"),
                ("STG-main-02-quote", "Stage", None, "Quote"),
                ("ENT-quote", "Entity", "FR-004", "Quote"),
                ("REQ-004-012", "Rule", "FR-004", "Quote expiry"),
                ("ENT-quote.status", "Field", "FR-004", "Quote status"),
                ("SRC-MTG-002-D03", "Source", None, "Meeting 002 decision 3"),
            ],
        )
        self.conn.commit()

    def tearDown(self) -> None:
        self.conn.close()
        self._tmp.cleanup()

    def assertRejected(self, sql: str, params: tuple = (), message: str | None = None) -> None:
        with self.assertRaises(sqlite3.IntegrityError) as ctx:
            self.conn.execute(sql, params)
        if message:
            self.assertIn(message, str(ctx.exception))
        self.conn.rollback()


class TestStructure(InitDbTestCase):
    def test_tables_exist(self) -> None:
        names = {r[0] for r in self.conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
        self.assertTrue(EXPECTED_TABLES <= names, names)

    def test_triggers_exist(self) -> None:
        names = {r[0] for r in self.conn.execute("SELECT name FROM sqlite_master WHERE type = 'trigger'")}
        for name in ("nodes_no_delete", "nodes_id_immutable", "changes_no_delete", "nodes_owner_fr_type_insert",
                     "fields_key_immutable", "sources_id_immutable"):
            self.assertIn(name, names)

    def test_user_version_matches_schema(self) -> None:
        self.assertEqual(self.conn.execute("PRAGMA user_version").fetchone()[0], load_schema().version)


class TestNodeInvariants(InitDbTestCase):
    def test_owner_fr_must_be_fr(self) -> None:
        self.assertRejected(
            "INSERT INTO nodes (id, type, owner_fr, title) VALUES ('REQ-004-013', 'Rule', 'ENT-quote', 'x')",
            message="nodes.owner_fr must reference an existing node of type FR",
        )

    def test_owner_fr_update_must_be_fr(self) -> None:
        self.assertRejected("UPDATE nodes SET owner_fr = 'STG-main-02-quote' WHERE id = 'ENT-quote'", message="type FR")

    def test_owner_fr_must_exist(self) -> None:
        self.assertRejected("INSERT INTO nodes (id, type, owner_fr, title) VALUES ('ENT-x', 'Entity', 'FR-999', 'x')")

    def test_unknown_node_type_rejected(self) -> None:
        self.assertRejected("INSERT INTO nodes (id, type, title) VALUES ('TL-main', 'Timeline', 'x')")

    def test_delete_node_blocked(self) -> None:
        self.assertRejected("DELETE FROM nodes WHERE id = 'STG-main-02-quote'", message="cannot be deleted")

    def test_id_update_blocked(self) -> None:
        self.assertRejected("UPDATE nodes SET id = 'STG-main-02-quotation' WHERE id = 'STG-main-02-quote'", message="immutable")

    def test_type_update_blocked(self) -> None:
        self.assertRejected("UPDATE nodes SET type = 'Actor' WHERE id = 'STG-main-02-quote'", message="immutable")

    def test_retire_and_rename_allowed(self) -> None:
        self.conn.execute("UPDATE nodes SET status = 'retired', title = 'Quotation', version = 2 WHERE id = 'STG-main-02-quote'")
        row = self.conn.execute("SELECT status, title FROM nodes WHERE id = 'STG-main-02-quote'").fetchone()
        self.assertEqual(row, ("retired", "Quotation"))


class TestFieldsAndEnums(InitDbTestCase):
    def _add_status_field(self) -> None:
        self.conn.execute(
            "INSERT INTO fields (id, entity_id, name, data_type, required, calculated_by) "
            "VALUES ('ENT-quote.status', 'ENT-quote', 'status', 'enum', 1, NULL)"
        )
        self.conn.executemany(
            "INSERT INTO enum_values (field_id, value, label, sort_order) VALUES ('ENT-quote.status', ?, ?, ?)",
            [("draft", "Draft", 1), ("sent", "Sent", 2)],
        )

    def test_field_on_non_entity_fails(self) -> None:
        self.assertRejected(
            "INSERT INTO fields (id, entity_id, name, data_type) VALUES ('ENT-quote.status', 'STG-main-02-quote', 'status', 'enum')",
            message="fields.entity_id must reference an existing node of type Entity",
        )

    def test_calculated_by_must_be_rule(self) -> None:
        self.assertRejected(
            "INSERT INTO fields (id, entity_id, name, data_type, calculated_by) "
            "VALUES ('ENT-quote.status', 'ENT-quote', 'status', 'enum', 'ENT-quote')",
            message="type Rule",
        )

    def test_calculated_by_rule_accepted(self) -> None:
        self.conn.execute(
            "INSERT INTO fields (id, entity_id, name, data_type, calculated_by) "
            "VALUES ('ENT-quote.status', 'ENT-quote', 'status', 'enum', 'REQ-004-012')"
        )

    def test_field_id_must_be_field_node(self) -> None:
        self.assertRejected(
            "INSERT INTO fields (id, entity_id, name, data_type) VALUES ('REQ-004-012', 'ENT-quote', 'status', 'enum')",
            message="type Field",
        )

    def test_enum_cascade(self) -> None:
        self._add_status_field()
        self.assertEqual(self.conn.execute("SELECT count(*) FROM enum_values").fetchone()[0], 2)
        self.conn.execute("DELETE FROM fields WHERE id = 'ENT-quote.status'")
        self.assertEqual(self.conn.execute("SELECT count(*) FROM enum_values").fetchone()[0], 0)

    def test_field_key_is_immutable(self) -> None:
        self._add_status_field()
        self.conn.execute("INSERT INTO nodes (id, type, owner_fr, title) VALUES ('ENT-quote.state', 'Field', 'FR-004', 'x')")
        self.conn.execute("INSERT INTO nodes (id, type, owner_fr, title) VALUES ('ENT-order', 'Entity', 'FR-004', 'Order')")
        self.conn.commit()
        for sql in (
            "UPDATE fields SET id = 'ENT-quote.state' WHERE id = 'ENT-quote.status'",
            "UPDATE fields SET entity_id = 'ENT-order' WHERE id = 'ENT-quote.status'",
            "UPDATE fields SET name = 'state' WHERE id = 'ENT-quote.status'",
        ):
            self.assertRejected(sql, message="immutable")
        self.conn.execute("UPDATE fields SET data_type = 'text', required = 1 WHERE id = 'ENT-quote.status'")

    def test_duplicate_enum_value_fails(self) -> None:
        self._add_status_field()
        self.assertRejected("INSERT INTO enum_values (field_id, value) VALUES ('ENT-quote.status', 'draft')", message="UNIQUE")

    def test_referenced_node_cannot_be_deleted_by_fk(self) -> None:
        self.conn.execute("DROP TRIGGER nodes_no_delete")
        self._add_status_field()
        self.assertRejected("DELETE FROM nodes WHERE id = 'ENT-quote'", message="FOREIGN KEY")


class TestEdges(InitDbTestCase):
    SQL = "INSERT INTO edges (from_id, verb, to_id, attrs) VALUES (?, ?, ?, ?)"

    def test_duplicate_edge_fails(self) -> None:
        params = ("REQ-004-012", "applies at", "STG-main-02-quote", "{}")
        self.conn.execute(self.SQL, params)
        self.assertRejected(self.SQL, params, message="UNIQUE")

    def test_unknown_verb_fails(self) -> None:
        self.assertRejected(self.SQL, ("REQ-004-012", "owns", "STG-main-02-quote", "{}"))

    def test_invalid_attrs_json_fails(self) -> None:
        self.assertRejected(self.SQL, ("REQ-004-012", "applies at", "STG-main-02-quote", "not json"))


class TestSourcesAndChanges(InitDbTestCase):
    def _add_source(self) -> None:
        self.conn.execute(
            "INSERT INTO sources (id, kind, ref, section, date, lifecycle) "
            "VALUES ('SRC-MTG-002-D03', 'meeting', 'sources/mtg-002.md', 'D03', '2026-10-16', 'validated')"
        )

    def _add_change(self, source_id: str | None) -> None:
        self.conn.execute(
            'INSERT INTO changes (changeset_id, at, changed_by, node_id, attribute, old_value, new_value, reason, source_id) '
            "VALUES ('cs-1', '2026-11-05T10:00:00', 'tester', 'ENT-quote', 'title', 'Quote', 'Quotation', 'rename', ?)",
            (source_id,),
        )

    def test_source_row_must_be_source_node(self) -> None:
        self.assertRejected(
            "INSERT INTO sources (id, kind, ref, lifecycle) VALUES ('ENT-quote', 'meeting', 'x', 'validated')",
            message="type Source",
        )

    def test_source_id_is_immutable(self) -> None:
        self._add_source()
        self.conn.execute("INSERT INTO nodes (id, type, title) VALUES ('SRC-MTG-003-D01', 'Source', 'Meeting 003 decision 1')")
        self.conn.commit()
        self.assertRejected("UPDATE sources SET id = 'SRC-MTG-003-D01' WHERE id = 'SRC-MTG-002-D03'", message="immutable")
        self.conn.execute("UPDATE sources SET lifecycle = 'incorporated' WHERE id = 'SRC-MTG-002-D03'")

    def test_unknown_lifecycle_fails(self) -> None:
        self.assertRejected("INSERT INTO sources (id, kind, ref, lifecycle) VALUES ('SRC-MTG-002-D03', 'meeting', 'x', 'approved')")

    def test_change_with_and_without_source(self) -> None:
        self._add_source()
        self._add_change("SRC-MTG-002-D03")
        self._add_change(None)
        self.assertEqual(self.conn.execute("SELECT count(*) FROM changes").fetchone()[0], 2)

    def test_change_source_must_be_source(self) -> None:
        with self.assertRaises(sqlite3.IntegrityError):
            self._add_change("ENT-quote")
        self.conn.rollback()

    def test_changes_append_only(self) -> None:
        self._add_change(None)
        self.conn.commit()
        self.assertRejected("DELETE FROM changes", message="append-only")
        self.assertRejected("UPDATE changes SET reason = 'edited'", message="append-only")


class TestCommandLine(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.db_path = Path(self._tmp.name) / "graph.db"

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def run_main(self, *args: str) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = init_db.main([str(self.db_path), *args])
        return code, out.getvalue(), err.getvalue()

    def test_refuses_existing_without_force(self) -> None:
        self.assertEqual(self.run_main()[0], 0)
        code, _, err = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("--force", err)

    def test_force_creates_backup_and_fresh_db(self) -> None:
        self.assertEqual(self.run_main()[0], 0)
        with contextlib.closing(connect(self.db_path)) as conn:
            conn.execute("INSERT INTO nodes (id, type, title) VALUES ('FR-001', 'FR', 'Old data')")
            conn.commit()

        code, out, _ = self.run_main("--force")
        self.assertEqual(code, 0)
        backups = list((self.db_path.parent / "backups").glob("graph-*.db"))
        self.assertEqual(len(backups), 1)
        self.assertRegex(backups[0].name, r"^graph-\d{8}-\d{6}\.db$")
        self.assertIn(str(backups[0]), out)
        with contextlib.closing(sqlite3.connect(backups[0])) as old:
            self.assertEqual(old.execute("SELECT count(*) FROM nodes").fetchone()[0], 1)
        with contextlib.closing(sqlite3.connect(self.db_path)) as new:
            self.assertEqual(new.execute("SELECT count(*) FROM nodes").fetchone()[0], 0)

    def test_second_force_in_same_second_keeps_both_backups(self) -> None:
        self.run_main()
        self.run_main("--force")
        self.run_main("--force")
        self.assertEqual(len(list((self.db_path.parent / "backups").glob("graph-*.db"))), 2)


class TestSchema(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = load_schema()
        self.raw = yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8"))

    def test_loads_all_types_and_verbs(self) -> None:
        self.assertEqual(
            set(self.schema.node_types),
            {"FR", "Stage", "Actor", "Entity", "Field", "Rule", "Event", "Setting", "Screen", "Source"},
        )
        self.assertEqual(len(self.schema.edge_verbs), 14)
        self.assertIn("carried from previous screen", self.schema.enum("provenance"))
        self.assertIn("partially incorporated", self.schema.enum("source_lifecycle"))

    def test_allowed_pairs(self) -> None:
        self.assertEqual(self.schema.allowed_pairs("shows"), {("Screen", "Field")})
        self.assertEqual(self.schema.allowed_pairs("decided by"), {("Rule", "Source"), ("Entity", "Source")})
        with self.assertRaises(SchemaError):
            self.schema.allowed_pairs("owns")

    def test_id_patterns_match_documented_examples(self) -> None:
        examples = {
            "FR": "FR-004",
            "Stage": "STG-main-02-quote",
            "Actor": "ACT-patient",
            "Entity": "ENT-quote",
            "Field": "ENT-quote.status",
            "Rule": "REQ-004-012",
            "Event": "EVT-quote-withdrawn",
            "Setting": "SET-quote-expiry-window",
            "Screen": "SCR-004-01",
            "Source": "SRC-MTG-002-D03",
        }
        for node_type, node_id in examples.items():
            self.assertRegex(node_id, self.schema.id_pattern(node_type), node_type)
        self.assertNotRegex("ENT-quote", self.schema.id_pattern("Field"))
        with self.assertRaises(SchemaError):
            self.schema.id_pattern("Timeline")

    def test_malformed_verb_pair_rejected(self) -> None:
        self.raw["edge_verbs"]["shows"]["pairs"] = [["Screen"]]
        with self.assertRaisesRegex(SchemaError, r"edge_verbs\.shows\.pairs\[0\]"):
            parse_schema(self.raw)

    def test_unknown_type_in_pair_rejected(self) -> None:
        self.raw["edge_verbs"]["joins"]["pairs"] = [["Timeline", "Stage"]]
        with self.assertRaisesRegex(SchemaError, "unknown node type 'Timeline'"):
            parse_schema(self.raw)

    def test_bad_id_pattern_rejected(self) -> None:
        self.raw["node_types"]["Rule"]["id_pattern"] = "^REQ-(\\d{3}$"
        with self.assertRaisesRegex(SchemaError, "invalid regex"):
            parse_schema(self.raw)

    def test_unknown_attr_type_rejected(self) -> None:
        self.raw["node_types"]["Stage"]["attrs"]["required"]["timeline"] = "colour"
        with self.assertRaisesRegex(SchemaError, "colour"):
            parse_schema(self.raw)


if __name__ == "__main__":
    unittest.main(verbosity=1)
