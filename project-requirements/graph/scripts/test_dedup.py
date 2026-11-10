"""Tests for Rule de-duplication: merge_node, lint L12 and L13, query.py duplicates and the v5 to v8 migrations.

Run from the scripts folder: /usr/bin/python3 -m unittest -q
"""

from __future__ import annotations

import contextlib
import copy
import io
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest import mock

import yaml

import init_db
import lint
import migrate_schema_v5
import migrate_schema_v6
import migrate_schema_v7
import migrate_schema_v8
import query
import write
from common import SCHEMA_PATH, connect, parse_schema
from test_write_query import SCHEMA, GraphTestCase


def run_cli(module: Any, *argv: str) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = module.main(list(argv))
    return code, out.getvalue(), err.getvalue()


def rule(rule_id: str, statement: str, owner: str = "FR-004", **attrs: str) -> dict[str, Any]:
    return {"op": "add_node", "id": rule_id, "type": "Rule", "owner_fr": owner, "title": rule_id,
            "attrs": {"statement": statement, **attrs}}


class DedupTestCase(GraphTestCase):
    """The write fixture plus REQ-004-020, a Rule to merge REQ-004-012 into, which already carries an alias."""

    def setUp(self) -> None:
        super().setUp()
        self.apply(self.ops(
            rule("REQ-004-020", "Quote total counts every line item exactly once.", aliases="REQ-004-099"),
            {"op": "add_edge", "from": "REQ-004-020", "verb": "applies at", "to": "STG-main-02-quote"},
            {"op": "add_edge", "from": "REQ-004-020", "verb": "applies at", "to": "STG-main-03-acceptance"},
            {"op": "update_node", "id": "REQ-004-012", "attrs": {"aliases": "REQ-004-098, REQ-004-020"}},
        ))

    def edges(self, node_id: str) -> set[tuple[str, str, str]]:
        return set(self.conn.execute(
            "SELECT from_id, verb, to_id FROM edges WHERE from_id = ? OR to_id = ?", (node_id, node_id)
        ).fetchall())

    def merge(self, survivor: str = "REQ-004-020", loser: str = "REQ-004-012") -> dict[str, Any]:
        return self.ops({"op": "merge_node", "survivor": survivor, "loser": loser})


class TestMergeNode(DedupTestCase):
    def test_merge_leaves_one_node_with_all_edges_and_aliases(self) -> None:
        changeset_id, _ = self.apply(self.merge())
        status = dict(self.conn.execute("SELECT id, status FROM nodes WHERE id IN ('REQ-004-012', 'REQ-004-020')"))
        self.assertEqual(status, {"REQ-004-012": "retired", "REQ-004-020": "active"})
        self.assertEqual(self.edges("REQ-004-012"), set())
        self.assertEqual(self.edges("REQ-004-020"), {
            ("REQ-004-020", "applies at", "STG-main-02-quote"),  # the loser's copy was dropped, not duplicated
            ("REQ-004-020", "applies at", "STG-main-03-acceptance"),
            ("REQ-004-020", "decided by", "SRC-MTG-002-D03"),
            ("ENT-quote.total", "calculated by", "REQ-004-020"),
        })
        calc = self.conn.execute("SELECT calculated_by FROM fields WHERE id = 'ENT-quote.total'").fetchone()[0]
        self.assertEqual(calc, "REQ-004-020")
        attrs = json.loads(self.conn.execute("SELECT attrs FROM nodes WHERE id = 'REQ-004-020'").fetchone()[0])
        # Own alias first, then the loser, then the loser's aliases without the survivor's own id.
        self.assertEqual(attrs["aliases"], "REQ-004-099, REQ-004-012, REQ-004-098")
        self.assertEqual(attrs["statement"], "Quote total counts every line item exactly once.")
        attributes = {(r[0], r[1]) for r in self.conn.execute(
            "SELECT node_id, attribute FROM changes WHERE changeset_id = ?", (changeset_id,))}
        self.assertIn(("REQ-004-012", "status"), attributes)
        self.assertIn(("REQ-004-020", "attrs.aliases"), attributes)
        self.assertIn(("ENT-quote.total", "field.calculated_by"), attributes)
        self.assertIn(("REQ-004-012", "edge:applies at:STG-main-02-quote"), attributes)
        self.assertNotIn("L05:ENT-quote.total", {f.id for f in lint.lint(self.conn, SCHEMA)})

    def test_later_operation_sees_the_merge(self) -> None:
        self.apply(self.ops(
            {"op": "merge_node", "survivor": "REQ-004-020", "loser": "REQ-004-012"},
            {"op": "remove_edge", "from": "REQ-004-020", "verb": "decided by", "to": "SRC-MTG-002-D03"},
        ))
        self.assertNotIn(("REQ-004-020", "decided by", "SRC-MTG-002-D03"), self.edges("REQ-004-020"))

    def test_invalid_change_set_writes_nothing(self) -> None:
        bad = self.merge()
        bad["operations"].append({"op": "retire_node", "id": "REQ-404-404"})
        self.assertRejected(bad, "operations[1] (retire_node)")

    def test_database_failure_rolls_back_the_whole_merge(self) -> None:
        self.conn.execute(
            "CREATE TRIGGER block_retire BEFORE UPDATE OF status ON nodes WHEN NEW.status = 'retired' "
            "BEGIN SELECT RAISE(ABORT, 'blocked'); END")
        self.conn.commit()
        before = self.snapshot()
        with self.assertRaises(sqlite3.IntegrityError):
            self.apply(self.merge())
        self.assertEqual(self.snapshot(), before)

    def test_rejections(self) -> None:
        self.assertRejected(self.merge("REQ-004-020", "REQ-004-020"), "same node")
        self.assertRejected(self.merge("REQ-004-020", "REQ-404-404"), "loser 'REQ-404-404' does not exist")
        self.assertRejected(self.merge("REQ-004-020", "ENT-quote"), "only nodes of one type merge")
        self.assertRejected(self.merge("STG-main-02-quote", "STG-main-03-acceptance"), "no 'aliases' attribute")
        self.assertRejected(self.ops({"op": "merge_node", "survivor": "REQ-004-020"}), "missing required keys ['loser']")
        self.apply(self.ops({"op": "retire_node", "id": "REQ-004-012"}))
        self.assertRejected(self.merge(), "loser 'REQ-004-012' is retired, not active")


class TestLintDedup(DedupTestCase):
    def ids(self, fr: str | None = None) -> set[str]:
        return {f.id for f in lint.lint(self.conn, SCHEMA, fr) if f.rule in ("L12", "L13")}

    def test_normalise_statement(self) -> None:
        self.assertEqual(lint.normalise_statement("  The System MUST, shall   show a  quote-total! "), "show quote total")
        self.assertEqual(lint.normalise_statement("The system must."), "")

    def test_l12_exact_after_normalisation(self) -> None:
        self.apply(self.ops(rule("REQ-004-021", "Total is the sum of line-items"),
                            {"op": "add_edge", "from": "REQ-004-021", "verb": "applies at", "to": "STG-main-02-quote"}))
        findings = {f.id: f.message for f in lint.lint(self.conn, SCHEMA) if f.rule == "L12"}
        self.assertIn("REQ-004-021 (same text)", findings["L12:REQ-004-012"])
        self.assertIn("REQ-004-012 (same text)", findings["L12:REQ-004-021"])

    def test_l12_similar_pair_and_fr_filter(self) -> None:
        self.apply(self.ops(
            {"op": "add_node", "id": "FR-005", "type": "FR", "title": "Acceptance"},
            rule("REQ-004-030", "Patient identifiers MUST remain anonymized to providers until payment confirmation."),
            rule("REQ-005-008", "System MUST keep patient identity masked to providers until payment confirmation.", "FR-005"),
        ))
        findings = {f.id: f.message for f in lint.lint(self.conn, SCHEMA) if f.rule == "L12"}
        self.assertIn("REQ-005-008 (similar 0.8", findings["L12:REQ-004-030"])
        self.assertIn("L12:REQ-005-008", self.ids("FR-005"))
        self.assertNotIn("L12:REQ-004-030", self.ids("FR-005"))

    def test_l12_skips_pairs_marked_distinct(self) -> None:
        self.apply(self.ops(rule("REQ-004-021", "Total is the sum of line-items"),
                            rule("REQ-004-022", "Total is the sum of line-items", distinct_from="REQ-004-021")))
        findings = {f.id: f.message for f in lint.lint(self.conn, SCHEMA) if f.rule == "L12"}
        # Marked on one side only, the pair is skipped both ways; REQ-004-012 is still unmarked.
        self.assertNotIn("REQ-004-022", findings["L12:REQ-004-021"])
        self.assertNotIn("REQ-004-021", findings["L12:REQ-004-022"])
        self.assertIn("REQ-004-012", findings["L12:REQ-004-022"])

    def test_l12_ignores_different_rules_and_retired_ones(self) -> None:
        self.assertEqual({i for i in self.ids() if i.startswith("L12")}, set())
        self.apply(self.ops(rule("REQ-004-021", "Total is the sum of line items."),
                            {"op": "retire_node", "id": "REQ-004-021"}))
        self.assertEqual({i for i in self.ids() if i.startswith("L12")}, set())

    def test_l13_rule_without_applies_at(self) -> None:
        self.apply(self.ops(rule("REQ-004-021", "Quotes expire after the window.")))
        self.assertIn("L13:REQ-004-021", self.ids())
        self.assertNotIn("L02:REQ-004-021", {f.id for f in lint.lint(self.conn, SCHEMA)})
        # An edge to a retired Stage still counts for L13; L02 reports that case.
        self.apply(self.ops({"op": "add_edge", "from": "REQ-004-021", "verb": "applies at", "to": "STG-main-02-quote"},
                            {"op": "retire_node", "id": "STG-main-02-quote"}))
        self.assertNotIn("L13:REQ-004-021", self.ids())
        self.assertIn("L02:REQ-004-021", {f.id for f in lint.lint(self.conn, SCHEMA)})

    def test_rule_placed_by_applies_to_or_global_scope(self) -> None:
        self.apply(self.ops(rule("REQ-004-021", "Only the patient may accept a quote."),
                            {"op": "add_edge", "from": "REQ-004-021", "verb": "applies to", "to": "ACT-patient"},
                            {"op": "add_edge", "from": "REQ-004-021", "verb": "applies to", "to": "ENT-quote.total"},
                            rule("REQ-004-022", "All money is shown in the patient's chosen currency.", scope="global")))
        lint_ids = {f.id for f in lint.lint(self.conn, SCHEMA)}
        for rule_id in ("REQ-004-021", "REQ-004-022"):
            self.assertNotIn(f"L13:{rule_id}", lint_ids)
            self.assertNotIn(f"L02:{rule_id}", lint_ids)
        # A Rule whose only target is retired acts nowhere: L02 fires, L13 does not.
        self.apply(self.ops({"op": "retire_node", "id": "ACT-patient"},
                            {"op": "retire_node", "id": "ENT-quote.total"}))
        lint_ids = {f.id for f in lint.lint(self.conn, SCHEMA)}
        self.assertIn("L02:REQ-004-021", lint_ids)
        self.assertNotIn("L13:REQ-004-021", lint_ids)

    def test_applies_to_rejects_other_targets_and_scope_values(self) -> None:
        self.assertRejected(self.ops(rule("REQ-004-021", "Quotes expire."),
                                     {"op": "add_edge", "from": "REQ-004-021", "verb": "applies to", "to": "STG-main-02-quote"}),
                            "applies to")
        self.assertRejected(self.ops(rule("REQ-004-021", "Quotes expire.", scope="local")), "scope")


class TestSystemHome(GraphTestCase):
    def test_system_prd_home_and_references(self) -> None:
        self.apply(self.ops(
            {"op": "add_node", "id": "FR-SYS", "type": "FR", "title": "System PRD"},
            {"op": "add_node", "id": "FR-005", "type": "FR", "title": "Acceptance"},
            rule("REQ-SYS-001", "Every timestamp is stored in UTC.", owner="FR-SYS", scope="global"),
            {"op": "add_edge", "from": "FR-005", "verb": "references", "to": "REQ-SYS-001"},
        ))
        self.assertEqual(self.count("SELECT count(*) FROM nodes WHERE id = 'REQ-SYS-001' AND owner_fr = 'FR-SYS'"), 1)
        self.assertRejected(self.ops(rule("REQ-SYSX-001", "Bad id.", owner="FR-SYS")), "pattern")

    def test_cli_lists_l12(self) -> None:
        self.apply(self.ops(rule("REQ-004-021", "Total is the sum of line items")))
        code, out, _ = run_cli(lint, "--db", str(self.db_path), "--json")
        self.assertEqual(code, 1)
        self.assertIn("L12:REQ-004-021", {f["id"] for f in json.loads(out)["findings"]})


class TestQueryDuplicates(DedupTestCase):
    def test_text_match(self) -> None:
        result = query.duplicates(self.conn, "Total is the sum of the line items")
        self.assertEqual([(r["id"], r["match"], r["score"]) for r in result.rows][0], ("REQ-004-012", "exact", 1.0))
        self.assertEqual(query.duplicates(self.conn, "Quotes expire after fourteen days").rows, [])

    def test_report_and_json(self) -> None:
        self.apply(self.ops(rule("REQ-004-021", "Total is the sum of line-items")))
        code, out, _ = run_cli(query, "duplicates", "--db", str(self.db_path), "--json")
        self.assertEqual(code, 0)
        rows = json.loads(out)
        self.assertEqual([(r["rule_a"], r["rule_b"], r["match"]) for r in rows], [("REQ-004-012", "REQ-004-021", "exact")])
        code, out, _ = run_cli(query, "duplicates", "--db", str(self.db_path), "--text", "Total is the sum of line items")
        self.assertEqual(code, 0)
        self.assertIn("REQ-004-021", out)

    def test_empty_text_is_rejected(self) -> None:
        code, _, err = run_cli(query, "duplicates", "--db", str(self.db_path), "--text", "  ")
        self.assertEqual(code, 1)
        self.assertIn("non-empty", err)


def v7_raw():
    """schema.yaml as it was before version 8: no 'external' actor group."""
    raw = copy.deepcopy(yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8")))
    raw["version"] = 7
    raw["enums"]["actor_group"].remove(migrate_schema_v8.NEW_GROUP)
    return raw


def v6_raw():
    """schema.yaml as it was before version 7: no 'system' actor group."""
    raw = v7_raw()
    raw["version"] = 6
    raw["enums"]["actor_group"].remove(migrate_schema_v7.NEW_GROUP)
    return raw


def v5_raw():
    """schema.yaml as it was before version 6: no Step or Flow types, flow verbs or flow_kind enum."""
    raw = v6_raw()
    raw["version"] = 5
    for node_type in migrate_schema_v6.NEW_TYPES:
        del raw["node_types"][node_type]
    for verb in migrate_schema_v6.NEW_VERBS:
        del raw["edge_verbs"][verb]
    del raw["enums"]["flow_kind"]
    return raw


def v5_schema():
    return parse_schema(v5_raw())


def v6_schema():
    return parse_schema(v6_raw())


def v7_schema():
    return parse_schema(v7_raw())


def v8_schema():
    return parse_schema(yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8")))


def v4_schema():
    """schema.yaml as it was before version 5: no 'references' or 'applies to' verbs."""
    raw = v5_raw()
    raw["version"] = 4
    for verb in migrate_schema_v5.NEW_VERBS:
        del raw["edge_verbs"][verb]
    return parse_schema(raw)


class TestMigrateV5(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.db = Path(self._tmp.name) / "graph.db"
        init_db.init_db(self.db, schema=v4_schema())
        conn = connect(self.db)
        write.apply_changeset(conn, v4_schema(), {"reason": "seed", "by": "tester", "operations": [
            {"op": "add_node", "id": "FR-004", "type": "FR", "title": "Quotes"},
            {"op": "add_node", "id": "FR-005", "type": "FR", "title": "Acceptance"},
            {"op": "add_node", "id": "STG-main-02-quote", "type": "Stage", "title": "Quote", "attrs": {"timeline": "main", "sequence": 2}},
            rule("REQ-004-008", "Identity stays masked."),
            {"op": "add_edge", "from": "REQ-004-008", "verb": "applies at", "to": "STG-main-02-quote"},
        ]})
        conn.close()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_migrates_and_accepts_references(self) -> None:
        schema = v5_schema()
        backup = migrate_schema_v5.migrate(self.db, schema)
        self.assertTrue(backup.is_file())
        conn = connect(self.db)
        try:
            self.assertEqual(conn.execute("PRAGMA user_version").fetchone()[0], 5)
            self.assertEqual(conn.execute("SELECT from_id, verb, to_id FROM edges").fetchall(),
                             [("REQ-004-008", "applies at", "STG-main-02-quote")])
            write.apply_changeset(conn, schema, {"reason": "cite", "by": "tester", "operations": [
                {"op": "add_edge", "from": "FR-005", "verb": "references", "to": "REQ-004-008"},
                {"op": "add_node", "id": "ACT-provider", "type": "Actor", "title": "Provider", "attrs": {"group": "provider"}},
                {"op": "add_edge", "from": "REQ-004-008", "verb": "applies to", "to": "ACT-provider"}]})
            fresh = Path(self._tmp.name) / "fresh.db"
            init_db.init_db(fresh, schema=schema)
            ddl = "SELECT name, sql FROM sqlite_master WHERE tbl_name = 'edges' ORDER BY name"
            fresh_conn = connect(fresh)
            self.assertEqual(conn.execute(ddl).fetchall(), fresh_conn.execute(ddl).fetchall())
            fresh_conn.close()
        finally:
            conn.close()

    def test_refuses_wrong_schema_or_db_version(self) -> None:
        before = self.db.read_bytes()
        with self.assertRaises(migrate_schema_v5.MigrationError):
            migrate_schema_v5.migrate(self.db, v4_schema())
        migrate_schema_v5.migrate(self.db, v5_schema())
        with self.assertRaises(migrate_schema_v5.MigrationError):
            migrate_schema_v5.migrate(self.db, v5_schema())
        self.assertNotEqual(self.db.read_bytes(), before)


class TestMigrateV6(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.db = Path(self._tmp.name) / "graph.db"
        init_db.init_db(self.db, schema=v5_schema())
        conn = connect(self.db)
        write.apply_changeset(conn, v5_schema(), {"reason": "seed", "by": "tester", "operations": [
            {"op": "add_node", "id": "FR-004", "type": "FR", "title": "Quotes"},
            {"op": "add_node", "id": "STG-main-02-quote", "type": "Stage", "title": "Quote", "attrs": {"timeline": "main", "sequence": 2}},
            {"op": "add_node", "id": "ACT-provider", "type": "Actor", "title": "Provider", "attrs": {"group": "provider"}},
            rule("REQ-004-008", "Identity stays masked."),
            {"op": "add_edge", "from": "REQ-004-008", "verb": "applies at", "to": "STG-main-02-quote"},
        ]})
        conn.close()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def dump(self, path: Path) -> dict[str, list[tuple]]:
        conn = connect(path)
        try:
            return {t: conn.execute(f"SELECT rowid, * FROM {t} ORDER BY rowid").fetchall() for t in migrate_schema_v6.TABLES}
        finally:
            conn.close()

    def test_old_db_refuses_step_until_migrated(self) -> None:
        conn = connect(self.db)
        with self.assertRaises(sqlite3.IntegrityError):
            conn.execute("INSERT INTO nodes (id, type, owner_fr, title) VALUES ('STP-004-001', 'Step', 'FR-004', 'x')")
        conn.close()

    def test_migrates_rows_unchanged_and_accepts_flow(self) -> None:
        before = self.dump(self.db)
        backup = migrate_schema_v6.migrate(self.db, v6_schema())
        self.assertTrue(backup.is_file())
        self.assertEqual(self.dump(self.db), before)
        conn = connect(self.db)
        try:
            self.assertEqual(conn.execute("PRAGMA user_version").fetchone()[0], 6)
            write.apply_changeset(conn, v6_schema(), {"reason": "flow", "by": "tester", "operations": [
                {"op": "add_node", "id": "STP-004-001", "type": "Step", "title": "Send quote", "owner_fr": "FR-004"},
                {"op": "add_edge", "from": "STP-004-001", "verb": "done by", "to": "ACT-provider"},
                {"op": "add_edge", "from": "STP-004-001", "verb": "at", "to": "STG-main-02-quote"},
                {"op": "add_edge", "from": "STP-004-001", "verb": "applies", "to": "REQ-004-008"},
                {"op": "add_node", "id": "FLW-004-main", "type": "Flow", "title": "Quote main flow", "attrs": {"kind": "main"}},
                {"op": "add_edge", "from": "FLW-004-main", "verb": "starts at", "to": "STP-004-001"}]})
            fresh = Path(self._tmp.name) / "fresh.db"
            init_db.init_db(fresh, schema=v6_schema())
            ddl = "SELECT type, name, sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%' ORDER BY name"
            fresh_conn = connect(fresh)
            self.assertEqual(conn.execute(ddl).fetchall(), fresh_conn.execute(ddl).fetchall())
            fresh_conn.close()
        finally:
            conn.close()

    def test_refuses_wrong_schema_or_db_version_and_leaves_db(self) -> None:
        before = self.db.read_bytes()
        with self.assertRaises(migrate_schema_v6.MigrationError):
            migrate_schema_v6.migrate(self.db, v5_schema())
        self.assertEqual(self.db.read_bytes(), before)
        migrate_schema_v6.migrate(self.db, v6_schema())
        with self.assertRaises(migrate_schema_v6.MigrationError):
            migrate_schema_v6.migrate(self.db, v6_schema())
        self.assertFalse(self.db.with_name(self.db.name + ".v6-tmp").exists())


class TestMigrateV7(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.db = Path(self._tmp.name) / "graph.db"
        init_db.init_db(self.db, schema=v6_schema())
        conn = connect(self.db)
        write.apply_changeset(conn, v6_schema(), {"reason": "seed", "by": "tester", "operations": [
            {"op": "add_node", "id": "ACT-provider", "type": "Actor", "title": "Provider", "attrs": {"group": "provider"}},
        ]})
        conn.close()
        self.system_actor = {"reason": "system actor", "by": "tester", "operations": [
            {"op": "add_node", "id": "ACT-system", "type": "Actor", "title": "Hairline system", "attrs": {"group": "system"}}]}

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def dump(self, path: Path) -> dict[str, list[tuple]]:
        conn = connect(path)
        try:
            return {t: conn.execute(f"SELECT rowid, * FROM {t} ORDER BY rowid").fetchall() for t in migrate_schema_v6.TABLES}
        finally:
            conn.close()

    def test_old_schema_refuses_system_group(self) -> None:
        conn = connect(self.db)
        try:
            with self.assertRaises(write.ChangeSetError):
                write.apply_changeset(conn, v6_schema(), self.system_actor)
        finally:
            conn.close()

    def test_migrates_rows_unchanged_and_accepts_system_group(self) -> None:
        before = self.dump(self.db)
        backup = migrate_schema_v7.migrate(self.db, v7_schema())
        self.assertTrue(backup.is_file())
        self.assertEqual(backup.parent, self.db.parent / "backups")
        self.assertEqual(self.dump(self.db), before)
        self.assertEqual(self.dump(backup), before)
        conn = connect(self.db)
        try:
            self.assertEqual(conn.execute("PRAGMA user_version").fetchone()[0], 7)
            write.apply_changeset(conn, v7_schema(), self.system_actor)
            self.assertEqual(conn.execute("SELECT json_extract(attrs, '$.group') FROM nodes WHERE id = 'ACT-system'").fetchone()[0], "system")
            fresh = Path(self._tmp.name) / "fresh.db"
            init_db.init_db(fresh, schema=v7_schema())
            ddl = "SELECT type, name, sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%' ORDER BY name"
            fresh_conn = connect(fresh)
            self.assertEqual(conn.execute(ddl).fetchall(), fresh_conn.execute(ddl).fetchall())
            fresh_conn.close()
        finally:
            conn.close()

    def test_refuses_wrong_schema_or_db_version_and_leaves_db(self) -> None:
        before = self.db.read_bytes()
        with self.assertRaises(migrate_schema_v7.MigrationError):
            migrate_schema_v7.migrate(self.db, v6_schema())
        self.assertEqual(self.db.read_bytes(), before)
        self.assertFalse((self.db.parent / "backups").exists())
        migrate_schema_v7.migrate(self.db, v7_schema())
        with self.assertRaises(migrate_schema_v7.MigrationError):
            migrate_schema_v7.migrate(self.db, v7_schema())

    def test_refuses_db_whose_ddl_drifted_from_the_schema(self) -> None:
        conn = connect(self.db)
        conn.execute("CREATE INDEX stray_index ON nodes(title)")
        conn.commit()
        conn.close()
        before = self.db.read_bytes()
        with self.assertRaises(migrate_schema_v7.MigrationError):
            migrate_schema_v7.migrate(self.db, v7_schema())
        self.assertEqual(self.db.read_bytes(), before)
        self.assertFalse((self.db.parent / "backups").exists())

    def test_cli_migrates_and_reports_missing_db(self) -> None:
        # schema.yaml is now a later version, so the CLI is given the version 7 schema it was written for.
        with mock.patch.object(migrate_schema_v7, "load_schema", v7_schema):
            code, out, _ = run_cli(migrate_schema_v7, "--db", str(self.db))
            self.assertEqual(code, 0)
            self.assertIn("schema version 7", out)
            code, _, err = run_cli(migrate_schema_v7, "--db", str(Path(self._tmp.name) / "missing.db"))
        self.assertEqual(code, 1)
        self.assertIn("does not exist", err)


class TestMigrateV8(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.db = Path(self._tmp.name) / "graph.db"
        init_db.init_db(self.db, schema=v7_schema())
        conn = connect(self.db)
        write.apply_changeset(conn, v7_schema(), {"reason": "seed", "by": "tester", "operations": [
            {"op": "add_node", "id": "ACT-system", "type": "Actor", "title": "Hairline system", "attrs": {"group": "system"}},
        ]})
        conn.close()
        self.external_actor = {"reason": "external actor", "by": "tester", "operations": [
            {"op": "add_node", "id": "ACT-stripe", "type": "Actor", "title": "Stripe", "attrs": {"group": "external"}}]}

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def dump(self, path: Path) -> dict[str, list[tuple]]:
        conn = connect(path)
        try:
            return {t: conn.execute(f"SELECT rowid, * FROM {t} ORDER BY rowid").fetchall() for t in migrate_schema_v6.TABLES}
        finally:
            conn.close()

    def test_old_schema_refuses_external_group(self) -> None:
        conn = connect(self.db)
        try:
            with self.assertRaises(write.ChangeSetError):
                write.apply_changeset(conn, v7_schema(), self.external_actor)
        finally:
            conn.close()

    def test_migrates_rows_unchanged_and_accepts_external_group(self) -> None:
        before = self.dump(self.db)
        backup = migrate_schema_v8.migrate(self.db, v8_schema())
        self.assertTrue(backup.is_file())
        self.assertEqual(backup.parent, self.db.parent / "backups")
        self.assertEqual(self.dump(self.db), before)
        self.assertEqual(self.dump(backup), before)
        conn = connect(self.db)
        try:
            self.assertEqual(conn.execute("PRAGMA user_version").fetchone()[0], 8)
            write.apply_changeset(conn, v8_schema(), self.external_actor)
            self.assertEqual(conn.execute("SELECT json_extract(attrs, '$.group') FROM nodes WHERE id = 'ACT-stripe'").fetchone()[0], "external")
            fresh = Path(self._tmp.name) / "fresh.db"
            init_db.init_db(fresh, schema=v8_schema())
            ddl = "SELECT type, name, sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%' ORDER BY name"
            fresh_conn = connect(fresh)
            self.assertEqual(conn.execute(ddl).fetchall(), fresh_conn.execute(ddl).fetchall())
            fresh_conn.close()
        finally:
            conn.close()

    def test_refuses_wrong_schema_or_db_version_and_leaves_db(self) -> None:
        before = self.db.read_bytes()
        with self.assertRaises(migrate_schema_v8.MigrationError):
            migrate_schema_v8.migrate(self.db, v7_schema())
        self.assertEqual(self.db.read_bytes(), before)
        self.assertFalse((self.db.parent / "backups").exists())
        migrate_schema_v8.migrate(self.db, v8_schema())
        with self.assertRaises(migrate_schema_v8.MigrationError):
            migrate_schema_v8.migrate(self.db, v8_schema())

    def test_refuses_db_whose_ddl_drifted_from_the_schema(self) -> None:
        conn = connect(self.db)
        conn.execute("CREATE INDEX stray_index ON nodes(title)")
        conn.commit()
        conn.close()
        before = self.db.read_bytes()
        with self.assertRaises(migrate_schema_v8.MigrationError):
            migrate_schema_v8.migrate(self.db, v8_schema())
        self.assertEqual(self.db.read_bytes(), before)
        self.assertFalse((self.db.parent / "backups").exists())

    def test_cli_migrates_and_reports_missing_db(self) -> None:
        code, out, _ = run_cli(migrate_schema_v8, "--db", str(self.db))
        self.assertEqual(code, 0)
        self.assertIn("schema version 8", out)
        code, _, err = run_cli(migrate_schema_v8, "--db", str(Path(self._tmp.name) / "missing.db"))
        self.assertEqual(code, 1)
        self.assertIn("does not exist", err)


if __name__ == "__main__":
    unittest.main()
