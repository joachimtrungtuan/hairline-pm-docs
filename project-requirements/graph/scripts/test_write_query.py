"""Tests for write.py and query.py. Run: .venv/bin/python scripts/test_write_query.py"""

from __future__ import annotations

import contextlib
import copy
import io
import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import init_db
import query
import write
from common import connect, load_schema

SCHEMA = load_schema()
T0 = datetime(2026, 11, 5, 1, 0, 0, tzinfo=timezone.utc)

FIXTURE: dict[str, Any] = {
    "reason": "Load the quote fixture",
    "by": "tester",
    "source_id": "SRC-MTG-002-D03",
    "operations": [
        {"op": "add_source", "id": "SRC-MTG-002-D03", "title": "Meeting 002 decision 3", "kind": "meeting",
         "ref": "sources/mtg-002.md", "section": "D03", "date": "2026-10-16", "lifecycle": "validated"},
        {"op": "add_node", "id": "FR-004", "type": "FR", "title": "Quote management", "attrs": {"module": "P-02"}},
        {"op": "add_node", "id": "STG-main-02-quote", "type": "Stage", "title": "Quote", "attrs": {"timeline": "main", "sequence": 2}},
        {"op": "add_node", "id": "STG-main-03-acceptance", "type": "Stage", "title": "Acceptance", "attrs": {"timeline": "main", "sequence": 3}},
        {"op": "add_edge", "from": "STG-main-03-acceptance", "verb": "follows", "to": "STG-main-02-quote"},
        {"op": "add_node", "id": "ACT-patient", "type": "Actor", "title": "Patient", "attrs": {"group": "patient"}},
        {"op": "add_edge", "from": "ACT-patient", "verb": "acts in", "to": "STG-main-03-acceptance"},
        {"op": "add_node", "id": "ENT-quote", "type": "Entity", "owner_fr": "FR-004", "title": "Quote", "attrs": {"table": "quotes"}},
        {"op": "add_edge", "from": "STG-main-02-quote", "verb": "writes", "to": "ENT-quote"},
        {"op": "add_edge", "from": "STG-main-03-acceptance", "verb": "reads", "to": "ENT-quote"},
        {"op": "add_node", "id": "REQ-004-012", "type": "Rule", "owner_fr": "FR-004", "title": "Quote total",
         "attrs": {"statement": "Total is the sum of line items."}},
        {"op": "add_edge", "from": "REQ-004-012", "verb": "applies at", "to": "STG-main-02-quote"},
        {"op": "add_edge", "from": "REQ-004-012", "verb": "decided by", "to": "SRC-MTG-002-D03"},
        {"op": "add_field", "id": "ENT-quote.status", "entity_id": "ENT-quote", "name": "status", "data_type": "enum",
         "required": True, "title": "Quote status", "owner_fr": "FR-004"},
        {"op": "add_enum_value", "field_id": "ENT-quote.status", "value": "draft", "label": "Draft", "sort_order": 1},
        {"op": "add_enum_value", "field_id": "ENT-quote.status", "value": "sent", "label": "Sent", "sort_order": 2},
        {"op": "add_field", "id": "ENT-quote.total", "entity_id": "ENT-quote", "name": "total", "data_type": "decimal",
         "title": "Quote total", "owner_fr": "FR-004", "calculated_by": "REQ-004-012"},
        {"op": "add_node", "id": "SCR-004-01", "type": "Screen", "owner_fr": "FR-004", "title": "Quote review"},
        {"op": "add_edge", "from": "SCR-004-01", "verb": "belongs to", "to": "STG-main-03-acceptance"},
        {"op": "add_edge", "from": "SCR-004-01", "verb": "shows", "to": "ENT-quote.total",
         "attrs": {"provenance": "system calculated", "label": "Total", "editable": False}},
        {"op": "add_edge", "from": "ACT-patient", "verb": "uses", "to": "SCR-004-01"},
    ],
}


class GraphTestCase(unittest.TestCase):
    load_fixture = True

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.db_path = self.dir / "graph.db"
        init_db.init_db(self.db_path)
        self.conn = connect(self.db_path)
        self.fixture_id = self.apply(FIXTURE, T0)[0] if self.load_fixture else None

    def tearDown(self) -> None:
        self.conn.close()
        self._tmp.cleanup()

    def apply(self, changeset: dict[str, Any], now: datetime | None = None) -> tuple[str, int]:
        return write.apply_changeset(self.conn, SCHEMA, changeset, now)

    def ops(self, *operations: dict[str, Any], **top: Any) -> dict[str, Any]:
        return {"reason": "test", "by": "tester", **top, "operations": list(operations)}

    def snapshot(self) -> str:
        return "\n".join(self.conn.iterdump())

    def assertRejected(self, changeset: dict[str, Any], *fragments: str) -> write.ChangeSetError:
        before = self.snapshot()
        with self.assertRaises(write.ChangeSetError) as ctx:
            self.apply(changeset)
        message = str(ctx.exception)
        for fragment in fragments:
            self.assertIn(fragment, message)
        self.assertFalse(self.conn.in_transaction)
        self.assertEqual(self.snapshot(), before, "a rejected change-set must leave the DB untouched")
        return ctx.exception

    def count(self, sql: str, *params: Any) -> int:
        return self.conn.execute(sql, params).fetchone()[0]


class TestFixtureLoad(GraphTestCase):
    def test_rows_created(self) -> None:
        self.assertEqual(self.count("SELECT count(*) FROM nodes"), 10)
        self.assertEqual(self.count("SELECT count(*) FROM fields"), 2)
        self.assertEqual(self.count("SELECT count(*) FROM enum_values"), 2)
        self.assertEqual(self.count("SELECT count(*) FROM sources"), 1)
        # 9 explicit edges plus the calculated-by mirror.
        self.assertEqual(self.count("SELECT count(*) FROM edges"), 10)

    def test_field_has_node_and_field_rows(self) -> None:
        self.assertEqual(self.count("SELECT count(*) FROM nodes WHERE id = 'ENT-quote.status' AND type = 'Field'"), 1)
        row = self.conn.execute("SELECT entity_id, name, data_type, required FROM fields WHERE id = 'ENT-quote.status'").fetchone()
        self.assertEqual(row, ("ENT-quote", "status", "enum", 1))

    def test_calculated_by_creates_mirror_edge(self) -> None:
        self.assertEqual(self.count("SELECT count(*) FROM fields WHERE id = 'ENT-quote.total' AND calculated_by = 'REQ-004-012'"), 1)
        self.assertEqual(self.count("SELECT count(*) FROM edges WHERE from_id = 'ENT-quote.total' AND verb = 'calculated by' AND to_id = 'REQ-004-012'"), 1)

    def test_changes_one_changeset_with_source(self) -> None:
        rows = self.conn.execute("SELECT DISTINCT changeset_id, changed_by, reason, source_id FROM changes").fetchall()
        self.assertEqual(rows, [(self.fixture_id, "tester", "Load the quote fixture", "SRC-MTG-002-D03")])
        title = self.conn.execute("SELECT old_value, new_value FROM changes WHERE node_id = 'ENT-quote' AND attribute = 'title'").fetchone()
        self.assertEqual(title, (None, '"Quote"'))

    def test_new_nodes_start_at_version_one(self) -> None:
        self.assertEqual(self.count("SELECT count(*) FROM nodes WHERE version <> 1"), 0)


class TestUpdates(GraphTestCase):
    def test_update_bumps_version_once_per_changeset(self) -> None:
        changeset_id, rows = self.apply(self.ops(
            {"op": "update_node", "id": "REQ-004-012", "title": "Quote total rule"},
            {"op": "update_node", "id": "REQ-004-012", "attrs": {"rationale": "Agreed in meeting"}},
        ))
        self.assertEqual(self.count("SELECT version FROM nodes WHERE id = 'REQ-004-012'"), 2)
        changed = self.conn.execute(
            "SELECT attribute, old_value, new_value FROM changes WHERE changeset_id = ? ORDER BY id", (changeset_id,)
        ).fetchall()
        self.assertEqual(changed, [("title", '"Quote total"', '"Quote total rule"'), ("attrs.rationale", None, '"Agreed in meeting"')])
        self.assertEqual(rows, 2)

    def test_attr_removed_with_null(self) -> None:
        self.apply(self.ops({"op": "update_node", "id": "ENT-quote", "attrs": {"table": None}}))
        self.assertEqual(self.conn.execute("SELECT attrs FROM nodes WHERE id = 'ENT-quote'").fetchone()[0], "{}")

    def test_retire_node(self) -> None:
        self.apply(self.ops({"op": "retire_node", "id": "SCR-004-01"}))
        self.assertEqual(self.conn.execute("SELECT status, version FROM nodes WHERE id = 'SCR-004-01'").fetchone(), ("retired", 2))

    def test_retire_enum_value(self) -> None:
        self.apply(self.ops({"op": "retire_enum_value", "field_id": "ENT-quote.status", "value": "sent"}))
        self.assertEqual(self.count("SELECT count(*) FROM enum_values WHERE field_id = 'ENT-quote.status'"), 1)
        row = self.conn.execute("SELECT old_value, new_value FROM changes WHERE attribute = 'enum.sent' ORDER BY id DESC").fetchone()
        self.assertEqual((json.loads(row[0]), row[1]), ({"label": "Sent", "sort_order": 2}, None))

    def test_enum_sort_order_defaults_after_highest(self) -> None:
        self.apply(self.ops(
            {"op": "add_enum_value", "field_id": "ENT-quote.status", "value": "accepted"},
            {"op": "add_enum_value", "field_id": "ENT-quote.status", "value": "expired"},
            {"op": "add_enum_value", "field_id": "ENT-quote.status", "value": "manual", "sort_order": 10},
            {"op": "add_field", "id": "ENT-quote.channel", "entity_id": "ENT-quote", "name": "channel", "data_type": "enum",
             "title": "Quote channel", "owner_fr": "FR-004"},
            {"op": "add_enum_value", "field_id": "ENT-quote.channel", "value": "app"},
        ))
        orders = dict(self.conn.execute("SELECT field_id || '.' || value, sort_order FROM enum_values").fetchall())
        self.assertEqual(orders["ENT-quote.status.accepted"], 3)
        self.assertEqual(orders["ENT-quote.status.expired"], 4)
        self.assertEqual(orders["ENT-quote.status.manual"], 10)
        self.assertEqual(orders["ENT-quote.channel.app"], 0)
        # A value retired earlier in the same change-set no longer counts towards the highest.
        self.apply(self.ops(
            {"op": "retire_enum_value", "field_id": "ENT-quote.status", "value": "manual"},
            {"op": "add_enum_value", "field_id": "ENT-quote.status", "value": "withdrawn"},
        ))
        self.assertEqual(self.count("SELECT sort_order FROM enum_values WHERE value = 'withdrawn'"), 5)
        self.assertRejected(self.ops({"op": "add_enum_value", "field_id": "ENT-quote.status", "value": "x", "sort_order": "1"}),
                            "sort_order must be an integer")

    def test_update_source_lifecycle(self) -> None:
        self.apply(self.ops({"op": "update_node", "id": "SRC-MTG-002-D03", "source": {"lifecycle": "incorporated"}}))
        self.assertEqual(self.conn.execute("SELECT lifecycle FROM sources").fetchone()[0], "incorporated")

    def test_remove_edge(self) -> None:
        self.apply(self.ops({"op": "remove_edge", "from": "ACT-patient", "verb": "uses", "to": "SCR-004-01"}))
        self.assertEqual(self.count("SELECT count(*) FROM edges WHERE verb = 'uses'"), 0)
        self.assertEqual(self.count("SELECT version FROM nodes WHERE id = 'ACT-patient'"), 2)


class TestCalculatedBySync(GraphTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.apply(self.ops({"op": "add_node", "id": "REQ-004-013", "type": "Rule", "owner_fr": "FR-004",
                             "title": "Discounted total", "attrs": {"statement": "Total after discount."}}))

    def mirror(self, field_id: str) -> tuple[Any, list[str]]:
        column = self.conn.execute("SELECT calculated_by FROM fields WHERE id = ?", (field_id,)).fetchone()[0]
        edges = [r[0] for r in self.conn.execute("SELECT to_id FROM edges WHERE from_id = ? AND verb = 'calculated by'", (field_id,))]
        return column, edges

    def test_update_field_moves_edge(self) -> None:
        self.apply(self.ops({"op": "update_field", "id": "ENT-quote.total", "calculated_by": "REQ-004-013"}))
        self.assertEqual(self.mirror("ENT-quote.total"), ("REQ-004-013", ["REQ-004-013"]))

    def test_update_field_clears_edge(self) -> None:
        self.apply(self.ops({"op": "update_field", "id": "ENT-quote.total", "calculated_by": None}))
        self.assertEqual(self.mirror("ENT-quote.total"), (None, []))

    def test_remove_edge_clears_column(self) -> None:
        self.apply(self.ops({"op": "remove_edge", "from": "ENT-quote.total", "verb": "calculated by", "to": "REQ-004-012"}))
        self.assertEqual(self.mirror("ENT-quote.total"), (None, []))

    def test_add_edge_sets_column(self) -> None:
        self.apply(self.ops({"op": "add_edge", "from": "ENT-quote.status", "verb": "calculated by", "to": "REQ-004-013"}))
        self.assertEqual(self.mirror("ENT-quote.status"), ("REQ-004-013", ["REQ-004-013"]))

    def test_add_edge_refuses_second_calculator(self) -> None:
        self.assertRejected(
            self.ops({"op": "add_edge", "from": "ENT-quote.total", "verb": "calculated by", "to": "REQ-004-013"}),
            "already calculated by 'REQ-004-012'",
        )

    def test_calculated_by_must_be_rule(self) -> None:
        self.assertRejected(self.ops({"op": "update_field", "id": "ENT-quote.total", "calculated_by": "ENT-quote"}), "not a Rule")


class TestValidation(GraphTestCase):
    def test_id_must_match_type_pattern(self) -> None:
        self.assertRejected(
            self.ops({"op": "add_node", "id": "RULE-1", "type": "Rule", "owner_fr": "FR-004", "title": "x", "attrs": {"statement": "s"}}),
            "operations[0] (add_node)", "does not match the Rule pattern",
        )

    def test_duplicate_id(self) -> None:
        self.assertRejected(self.ops({"op": "add_node", "id": "ACT-patient", "type": "Actor", "title": "x"}), "already exists")

    def test_unknown_attribute(self) -> None:
        self.assertRejected(self.ops({"op": "add_node", "id": "ACT-provider", "type": "Actor", "title": "Provider", "attrs": {"colour": "red"}}),
                            "attribute 'colour' is not allowed")

    def test_required_attribute_missing(self) -> None:
        self.assertRejected(self.ops({"op": "add_node", "id": "STG-main-04-booking", "type": "Stage", "title": "Booking", "attrs": {"timeline": "main"}}),
                            "required attribute 'sequence' is missing")

    def test_attribute_type_and_enum(self) -> None:
        self.assertRejected(
            self.ops({"op": "add_node", "id": "STG-main-04-booking", "type": "Stage", "title": "Booking", "attrs": {"timeline": "side", "sequence": "4"}}),
            "attribute 'timeline' must be one of", "attribute 'sequence' must be an integer",
        )

    def test_update_cannot_drop_required_attribute(self) -> None:
        self.assertRejected(self.ops({"op": "update_node", "id": "REQ-004-012", "attrs": {"statement": None}}), "required attribute 'statement'")

    def test_owner_required(self) -> None:
        self.assertRejected(self.ops({"op": "add_node", "id": "EVT-quote-sent", "type": "Event", "title": "Quote sent"}), "require an owning FR")

    def test_owner_forbidden(self) -> None:
        self.assertRejected(self.ops({"op": "add_node", "id": "ACT-admin", "type": "Actor", "owner_fr": "FR-004", "title": "Admin"}),
                            "must not have an owning FR")

    def test_owner_must_be_fr(self) -> None:
        self.assertRejected(self.ops({"op": "add_node", "id": "EVT-quote-sent", "type": "Event", "owner_fr": "ENT-quote", "title": "x"}),
                            "is a Entity, not a FR")

    def test_owner_cannot_be_cleared_when_required(self) -> None:
        self.assertRejected(self.ops({"op": "update_node", "id": "ENT-quote", "owner_fr": None}), "require an owning FR")

    def test_edge_pair_not_allowed(self) -> None:
        self.assertRejected(self.ops({"op": "add_edge", "from": "ACT-patient", "verb": "writes", "to": "ENT-quote"}),
                            "verb 'writes' cannot join Actor -> Entity")

    def test_unknown_verb(self) -> None:
        self.assertRejected(self.ops({"op": "add_edge", "from": "ACT-patient", "verb": "likes", "to": "ENT-quote"}), "unknown edge verb")

    def test_shows_requires_provenance(self) -> None:
        self.assertRejected(self.ops({"op": "add_edge", "from": "SCR-004-01", "verb": "shows", "to": "ENT-quote.status"}),
                            "edge required attribute 'provenance' is missing")

    def test_shows_provenance_from_enum(self) -> None:
        self.assertRejected(
            self.ops({"op": "add_edge", "from": "SCR-004-01", "verb": "shows", "to": "ENT-quote.status", "attrs": {"provenance": "guess"}}),
            "edge attribute 'provenance' must be one of",
        )

    def test_edge_attrs_on_plain_verb(self) -> None:
        self.assertRejected(self.ops({"op": "add_edge", "from": "ACT-patient", "verb": "acts in", "to": "STG-main-02-quote", "attrs": {"label": "x"}}),
                            "is not allowed")

    def test_duplicate_edge(self) -> None:
        self.assertRejected(self.ops({"op": "add_edge", "from": "ACT-patient", "verb": "uses", "to": "SCR-004-01"}), "already exists")

    def test_field_needs_add_field(self) -> None:
        self.assertRejected(self.ops({"op": "add_node", "id": "ENT-quote.notes", "type": "Field", "owner_fr": "FR-004", "title": "Notes"}),
                            "use add_field")

    def test_source_needs_add_source(self) -> None:
        self.assertRejected(self.ops({"op": "add_node", "id": "SRC-X", "type": "Source", "title": "x"}), "use add_source")

    def test_field_id_must_follow_entity_and_name(self) -> None:
        self.assertRejected(
            self.ops({"op": "add_field", "id": "ENT-quote.notes", "entity_id": "ENT-quote", "name": "note", "data_type": "text",
                      "title": "Notes", "owner_fr": "FR-004"}),
            "id must be <entity_id>.<name>",
        )

    def test_field_entity_must_be_entity(self) -> None:
        self.assertRejected(
            self.ops({"op": "add_field", "id": "REQ-004-012.x", "entity_id": "REQ-004-012", "name": "x", "data_type": "text",
                      "title": "x", "owner_fr": "FR-004"}),
            "not a Entity",
        )

    def test_field_owner_required(self) -> None:
        self.assertRejected(
            self.ops({"op": "add_field", "id": "ENT-quote.notes", "entity_id": "ENT-quote", "name": "notes", "data_type": "text", "title": "Notes"}),
            "Field nodes require an owning FR",
        )

    def test_field_name_immutable(self) -> None:
        self.assertRejected(self.ops({"op": "update_field", "id": "ENT-quote.status", "name": "state"}), "cannot change")

    def test_type_immutable(self) -> None:
        self.assertRejected(self.ops({"op": "update_node", "id": "ENT-quote", "type": "Rule"}), "type is immutable")

    def test_update_that_changes_nothing(self) -> None:
        self.assertRejected(self.ops({"op": "update_node", "id": "ENT-quote", "title": "Quote"}), "changes nothing")

    def test_enum_duplicate_and_missing(self) -> None:
        self.assertRejected(self.ops({"op": "add_enum_value", "field_id": "ENT-quote.status", "value": "draft"}), "already has enum value")
        self.assertRejected(self.ops({"op": "retire_enum_value", "field_id": "ENT-quote.status", "value": "void"}), "has no enum value")

    def test_source_lifecycle_and_date(self) -> None:
        self.assertRejected(
            self.ops({"op": "add_source", "id": "SRC-MTG-003", "title": "x", "kind": "meeting", "ref": "r", "lifecycle": "approved", "date": "16/10/2026"}),
            "lifecycle must be one of", "date must be a YYYY-MM-DD date",
        )

    def test_changeset_source_must_be_source(self) -> None:
        self.assertRejected(self.ops({"op": "retire_node", "id": "SCR-004-01"}, source_id="ENT-quote"), "source_id 'ENT-quote' is a Entity")

    def test_reason_and_by_required(self) -> None:
        self.assertRejected({"operations": [{"op": "retire_node", "id": "SCR-004-01"}]}, "reason must be", "by must be")

    def test_unknown_op_and_keys(self) -> None:
        self.assertRejected(self.ops({"op": "delete_node", "id": "SCR-004-01"}), "unknown op 'delete_node'")
        self.assertRejected(self.ops({"op": "retire_node", "id": "SCR-004-01", "why": "x"}), "unknown keys ['why']")

    def test_late_failure_rolls_back_earlier_operations(self) -> None:
        error = self.assertRejected(self.ops(
            {"op": "add_node", "id": "ACT-provider", "type": "Actor", "title": "Provider", "attrs": {"group": "provider"}},
            {"op": "retire_node", "id": "SCR-004-01"},
            {"op": "add_edge", "from": "ACT-provider", "verb": "acts in", "to": "STG-missing"},
        ), "operations[2] (add_edge): to 'STG-missing' does not exist")
        self.assertEqual(len(error.problems), 1)

    def test_later_operation_sees_earlier_one(self) -> None:
        self.apply(self.ops(
            {"op": "add_node", "id": "ACT-provider", "type": "Actor", "title": "Provider", "attrs": {"group": "provider"}},
            {"op": "add_edge", "from": "ACT-provider", "verb": "acts in", "to": "STG-main-02-quote"},
        ))
        self.assertEqual(self.count("SELECT count(*) FROM edges WHERE from_id = 'ACT-provider'"), 1)


class TestCli(GraphTestCase):
    def run_cli(self, module: Any, *argv: str) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = module.main(list(argv))
        return code, out.getvalue(), err.getvalue()

    def test_write_yaml_file(self) -> None:
        path = self.dir / "cs.yaml"
        path.write_text(
            "reason: add a source\nby: tester\noperations:\n"
            "  - {op: add_source, id: SRC-MTG-003, title: Meeting 3, kind: meeting, ref: sources/mtg-003.md,"
            " date: 2026-10-20, lifecycle: pending review}\n",
            encoding="utf-8",
        )
        code, out, _ = self.run_cli(write, str(path), "--db", str(self.db_path))
        self.assertEqual(code, 0)
        self.assertIn("Applied change-set", out)
        self.assertEqual(self.conn.execute("SELECT date FROM sources WHERE id = 'SRC-MTG-003'").fetchone()[0], "2026-10-20")

    def test_write_invalid_exit_1(self) -> None:
        path = self.dir / "cs.json"
        path.write_text(json.dumps(self.ops({"op": "retire_node", "id": "ACT-nobody"})), encoding="utf-8")
        code, _, err = self.run_cli(write, str(path), "--db", str(self.db_path))
        self.assertEqual(code, 1)
        self.assertIn("operations[0] (retire_node)", err)

    def test_write_unparsable_exit_1(self) -> None:
        path = self.dir / "cs.json"
        path.write_text("{not json", encoding="utf-8")
        self.assertEqual(self.run_cli(write, str(path), "--db", str(self.db_path))[0], 1)

    def test_write_missing_db_exit_2(self) -> None:
        path = self.dir / "cs.json"
        path.write_text(json.dumps(self.ops({"op": "retire_node", "id": "SCR-004-01"})), encoding="utf-8")
        missing = self.dir / "none.db"
        self.assertEqual(self.run_cli(write, str(path), "--db", str(missing))[0], 2)
        self.assertFalse(missing.exists(), "the write script must not create a DB")

    def test_query_table_and_json(self) -> None:
        code, out, _ = self.run_cli(query, "fr", "FR-004", "--db", str(self.db_path))
        self.assertEqual(code, 0)
        self.assertIn("REQ-004-012", out)
        code, out, _ = self.run_cli(query, "fr", "FR-004", "--db", str(self.db_path), "--json")
        self.assertEqual(code, 0)
        self.assertEqual(len(json.loads(out)), 5)

    def test_query_not_found_exit_1(self) -> None:
        self.assertEqual(self.run_cli(query, "impact", "ENT-nothing", "--db", str(self.db_path))[0], 1)


class TestQueries(GraphTestCase):
    def test_impact_finds_rule_from_screen_in_two_hops(self) -> None:
        rows = {r["id"]: r for r in query.impact(self.conn, "SCR-004-01").rows}
        self.assertEqual(rows["REQ-004-012"]["hop"], 2)
        self.assertEqual(rows["ENT-quote.total"]["hop"], 1)
        self.assertEqual(rows["REQ-004-012"]["owner_fr"], "FR-004")
        self.assertNotIn("SCR-004-01", rows)

    def test_impact_depth_limits(self) -> None:
        ids = {r["id"] for r in query.impact(self.conn, "SCR-004-01", depth=1).rows}
        self.assertEqual(ids, {"ENT-quote.total", "STG-main-03-acceptance", "ACT-patient"})

    def test_impact_rows_ordered_by_hop(self) -> None:
        hops = [r["hop"] for r in query.impact(self.conn, "SCR-004-01", depth=3).rows]
        self.assertEqual(hops, sorted(hops))

    def test_lifecycle(self) -> None:
        rows = query.lifecycle(self.conn, SCHEMA, "main").rows
        self.assertEqual([r["stage"] for r in rows], ["STG-main-02-quote", "STG-main-03-acceptance"])
        quote, acceptance = rows
        self.assertEqual((quote["writes"], quote["rules"]), (["ENT-quote"], ["REQ-004-012"]))
        self.assertEqual((acceptance["actors"], acceptance["reads"], acceptance["screens"]), (["ACT-patient"], ["ENT-quote"], ["SCR-004-01"]))

    def test_lifecycle_unknown_timeline(self) -> None:
        with self.assertRaises(query.QueryError):
            query.lifecycle(self.conn, SCHEMA, "sideways")

    def test_cites_field_lists_screen_with_provenance(self) -> None:
        rows = query.cites(self.conn, "ENT-quote.total").rows
        self.assertEqual([(r["id"], r["verb"]) for r in rows], [("SCR-004-01", "shows")])
        self.assertEqual(rows[0]["edge_attrs"]["provenance"], "system calculated")

    def test_fr_grouped_by_type(self) -> None:
        rows = query.fr(self.conn, SCHEMA, "FR-004").rows
        self.assertEqual([r["type"] for r in rows], ["Entity", "Field", "Field", "Rule", "Screen"])
        with self.assertRaises(query.QueryError):
            query.fr(self.conn, SCHEMA, "ENT-quote")

    def test_history_and_at_round_trip(self) -> None:
        t1, t2 = T0 + timedelta(hours=1), T0 + timedelta(hours=2)
        self.apply(self.ops({"op": "update_node", "id": "REQ-004-012", "attrs": {"statement": "Version two."}}), t1)
        self.apply(self.ops({"op": "update_node", "id": "REQ-004-012", "attrs": {"statement": "Version three."}, "title": "Total"}), t2)

        history = [(r["attribute"], r["old_value"], r["new_value"]) for r in query.history(self.conn, "REQ-004-012").rows]
        self.assertEqual(history[:3], [
            ("attrs.statement", "Version two.", "Version three."),
            ("title", "Quote total", "Total"),
            ("attrs.statement", "Total is the sum of line items.", "Version two."),
        ])
        self.assertEqual(history[-1], ("type", None, "Rule"))

        def state(moment: datetime) -> dict[str, Any]:
            return {r["attribute"]: r["value"] for r in query.at(self.conn, "REQ-004-012", moment.isoformat()).rows}

        self.assertEqual(state(T0)["attrs.statement"], "Total is the sum of line items.")
        between = state(t1 + timedelta(minutes=30))
        self.assertEqual((between["attrs.statement"], between["title"]), ("Version two.", "Quote total"))
        latest = state(t2)
        self.assertEqual((latest["attrs.statement"], latest["title"]), ("Version three.", "Total"))
        self.assertEqual(latest["owner_fr"], "FR-004")
        with self.assertRaises(query.QueryError):
            query.at(self.conn, "REQ-004-012", (T0 - timedelta(seconds=1)).isoformat())
        # A timestamp without an offset is read as UTC, the zone change rows are stored in.
        self.assertEqual(query.at(self.conn, "REQ-004-012", "2026-11-05T02:30:00").rows, query.at(self.conn, "REQ-004-012", "2026-11-05T09:30:00+07:00").rows)

    def test_at_replays_set_clear_set(self) -> None:
        t1, t2, t3 = (T0 + timedelta(hours=h) for h in (1, 2, 3))
        self.apply(self.ops({"op": "update_node", "id": "REQ-004-012", "attrs": {"rationale": "First"}}), t1)
        self.apply(self.ops({"op": "update_node", "id": "REQ-004-012", "attrs": {"rationale": None}}), t2)
        self.apply(self.ops({"op": "update_node", "id": "REQ-004-012", "attrs": {"rationale": "Second"}}), t3)

        def rationale(moment: datetime) -> Any:
            rows = query.at(self.conn, "REQ-004-012", moment.isoformat()).rows
            return {r["attribute"]: r["value"] for r in rows}.get("attrs.rationale", "absent")

        self.assertEqual([rationale(t) for t in (T0, t1, t2, t3)], ["absent", "First", "absent", "Second"])

    def test_changeset_returns_all_rows(self) -> None:
        expected = self.count("SELECT count(*) FROM changes WHERE changeset_id = ?", self.fixture_id)
        rows = query.changeset(self.conn, self.fixture_id).rows
        self.assertEqual(len(rows), expected)
        self.assertGreater(expected, 50)
        self.assertEqual({r["node_id"] for r in rows} >= {"FR-004", "ENT-quote.total", "SRC-MTG-002-D03"}, True)
        with self.assertRaises(query.QueryError):
            query.changeset(self.conn, "cs-missing")


if __name__ == "__main__":
    unittest.main(verbosity=1)
