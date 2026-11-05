"""Tests for lint.py, export.py and render.py. Run: .venv/bin/python scripts/test_lint_export_render.py"""

from __future__ import annotations

import contextlib
import io
import json
import re
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

import export
import init_db
import lint
import render
import write
from common import connect, load_schema

SCHEMA = load_schema()

# One FR, two Stages, one Actor, one Entity with two Fields (one enum, one calculated),
# one Rule, one Event, one Screen with a shows edge, one Source and one change row.
FIXTURE = """
INSERT INTO nodes (id, type, owner_fr, title, attrs) VALUES
  ('FR-004', 'FR', NULL, 'Quote management', '{"module": "P-02", "summary": "Providers build and send quotes."}'),
  ('STG-main-01-inquiry', 'Stage', NULL, 'Inquiry', '{"timeline": "main", "sequence": 1}'),
  ('STG-main-02-quote', 'Stage', NULL, 'Quote', '{"timeline": "main", "sequence": 2}'),
  ('ACT-provider', 'Actor', NULL, 'Provider', '{"group": "provider"}'),
  ('SRC-MTG-002-D03', 'Source', NULL, 'Meeting 002 decision 3', '{}'),
  ('ENT-quote', 'Entity', 'FR-004', 'Quote', '{"table": "quotes"}'),
  ('REQ-004-001', 'Rule', 'FR-004', 'Quote total', '{"statement": "The total is the sum of line items."}'),
  ('ENT-quote.status', 'Field', 'FR-004', 'Quote status', '{}'),
  ('ENT-quote.total', 'Field', 'FR-004', 'Quote total', '{}'),
  ('EVT-quote-sent', 'Event', 'FR-004', 'Quote sent', '{"payload": "quote id"}'),
  ('SCR-004-01', 'Screen', 'FR-004', 'Quote builder', '{"platform": "provider web"}');
INSERT INTO sources (id, kind, ref, section, date, lifecycle) VALUES
  ('SRC-MTG-002-D03', 'meeting', 'transcriptions/mtg-002.md', 'D03', '2026-10-16', 'validated');
INSERT INTO fields (id, entity_id, name, data_type, required, calculated_by) VALUES
  ('ENT-quote.status', 'ENT-quote', 'status', 'enum', 1, NULL),
  ('ENT-quote.total', 'ENT-quote', 'total', 'decimal', 1, 'REQ-004-001');
INSERT INTO enum_values (field_id, value, label, sort_order) VALUES
  ('ENT-quote.status', 'sent', 'Sent', 2),
  ('ENT-quote.status', 'draft', 'Draft', 1);
INSERT INTO edges (from_id, verb, to_id, attrs) VALUES
  ('STG-main-02-quote', 'follows', 'STG-main-01-inquiry', '{}'),
  ('ACT-provider', 'acts in', 'STG-main-02-quote', '{}'),
  ('ACT-provider', 'uses', 'SCR-004-01', '{}'),
  ('REQ-004-001', 'applies at', 'STG-main-02-quote', '{}'),
  ('REQ-004-001', 'decided by', 'SRC-MTG-002-D03', '{}'),
  ('ENT-quote', 'decided by', 'SRC-MTG-002-D03', '{}'),
  ('ENT-quote.total', 'calculated by', 'REQ-004-001', '{}'),
  ('STG-main-02-quote', 'emits', 'EVT-quote-sent', '{}'),
  ('SCR-004-01', 'belongs to', 'STG-main-02-quote', '{}'),
  ('SCR-004-01', 'shows', 'ENT-quote.status', '{"provenance": "system calculated", "label": "Status | state", "editable": false}');
INSERT INTO changes (changeset_id, at, changed_by, node_id, attribute, old_value, new_value, reason, source_id) VALUES
  ('CS-0001', '2026-11-05T09:00:00Z', 'ba', 'REQ-004-001', 'statement', NULL, 'The total is the sum of line items.',
   'Initial load', 'SRC-MTG-002-D03');
"""


def run_main(module, argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = module.main(argv)
    return code, out.getvalue(), err.getvalue()


class GraphTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.db_path = self.dir / "graph.db"
        init_db.init_db(self.db_path)
        self.conn = connect(self.db_path)
        self.conn.executescript(FIXTURE)
        self.conn.commit()

    def tearDown(self) -> None:
        self.conn.close()
        self._tmp.cleanup()

    def sql(self, statement: str, params: tuple = ()) -> None:
        self.conn.execute(statement, params)
        self.conn.commit()

    def add_node(self, id_: str, type_: str, owner: str | None, title: str, attrs: str = "{}") -> None:
        self.sql("INSERT INTO nodes (id, type, owner_fr, title, attrs) VALUES (?, ?, ?, ?, ?)", (id_, type_, owner, title, attrs))

    def add_edge(self, a: str, verb: str, b: str, attrs: str = "{}") -> None:
        self.sql("INSERT INTO edges (from_id, verb, to_id, attrs) VALUES (?, ?, ?, ?)", (a, verb, b, attrs))

    def drop_edge(self, a: str, verb: str, b: str) -> None:
        self.sql("DELETE FROM edges WHERE from_id = ? AND verb = ? AND to_id = ?", (a, verb, b))

    def finding_ids(self, fr: str | None = None) -> set[str]:
        return {f.id for f in lint.lint(self.conn, SCHEMA, fr)}


class TestLint(GraphTestCase):
    def test_clean_fixture_has_no_findings(self) -> None:
        self.assertEqual(lint.lint(self.conn, SCHEMA), [])
        code, out, _ = run_main(lint, ["--db", str(self.db_path)])
        self.assertEqual(code, 0)
        self.assertIn("No findings.", out)

    def test_empty_db_is_clean(self) -> None:
        empty = self.dir / "empty.db"
        init_db.init_db(empty)
        code, out, _ = run_main(lint, ["--db", str(empty), "--json"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), {"count": 0, "findings": []})

    def test_l01_owner_missing(self) -> None:
        self.sql("UPDATE nodes SET owner_fr = NULL WHERE id = 'ENT-quote'")
        self.assertIn("L01:ENT-quote", self.finding_ids())

    def test_l01_required_attribute_missing(self) -> None:
        self.sql("UPDATE nodes SET attrs = '{}' WHERE id = 'ACT-provider'")
        self.assertEqual(self.finding_ids(), {"L01:ACT-provider#group"})
        self.sql("""UPDATE nodes SET attrs = '{"timeline": "main"}' WHERE id = 'STG-main-02-quote'""")
        self.assertIn("L01:STG-main-02-quote#sequence", self.finding_ids())

    def test_l02_rule_applies_nowhere(self) -> None:
        self.drop_edge("REQ-004-001", "applies at", "STG-main-02-quote")
        self.assertIn("L02:REQ-004-001", self.finding_ids())

    def test_l02_retired_stage_does_not_count(self) -> None:
        self.sql("UPDATE nodes SET status = 'retired' WHERE id = 'STG-main-02-quote'")
        self.assertIn("L02:REQ-004-001", self.finding_ids())

    def test_l03_screen_shows_nothing(self) -> None:
        self.drop_edge("SCR-004-01", "shows", "ENT-quote.status")
        self.assertIn("L03:SCR-004-01", self.finding_ids())

    def test_l03_screen_shows_non_field(self) -> None:
        self.add_edge("SCR-004-01", "shows", "ENT-quote", '{"provenance": "retrieved"}')
        self.assertIn("L03:SCR-004-01>ENT-quote", self.finding_ids())

    def test_l04_event_without_producer(self) -> None:
        self.drop_edge("STG-main-02-quote", "emits", "EVT-quote-sent")
        self.assertIn("L04:EVT-quote-sent", self.finding_ids())

    def test_l04_event_with_two_producers(self) -> None:
        self.add_edge("STG-main-01-inquiry", "emits", "EVT-quote-sent")
        self.assertIn("L04:EVT-quote-sent", self.finding_ids())

    def test_l05_calculated_by_out_of_sync(self) -> None:
        self.sql("UPDATE fields SET calculated_by = NULL WHERE id = 'ENT-quote.total'")
        self.assertIn("L05:ENT-quote.total", self.finding_ids())

    def test_l05_edge_without_column(self) -> None:
        self.add_edge("ENT-quote.status", "calculated by", "REQ-004-001")
        self.assertIn("L05:ENT-quote.status", self.finding_ids())

    def test_l06_verb_not_allowed_for_pair(self) -> None:
        self.add_edge("ACT-provider", "applies at", "STG-main-01-inquiry")
        self.assertIn("L06:ACT-provider>applies-at>STG-main-01-inquiry", self.finding_ids())

    def test_l07_provenance_missing(self) -> None:
        self.sql("UPDATE edges SET attrs = '{}' WHERE verb = 'shows'")
        self.assertIn("L07:SCR-004-01>shows>ENT-quote.status", self.finding_ids())

    def test_l07_provenance_invalid(self) -> None:
        self.sql("""UPDATE edges SET attrs = '{"provenance": "guessed"}' WHERE verb = 'shows'""")
        self.assertIn("L07:SCR-004-01>shows>ENT-quote.status", self.finding_ids())

    def test_l08_stage_follows_nothing(self) -> None:
        self.drop_edge("STG-main-02-quote", "follows", "STG-main-01-inquiry")
        self.assertIn("L08:STG-main-02-quote", self.finding_ids())

    def test_l08_standalone_entry_is_allowed(self) -> None:
        self.drop_edge("STG-main-02-quote", "follows", "STG-main-01-inquiry")
        self.sql("""UPDATE nodes SET attrs = '{"timeline": "main", "sequence": 2, "standalone_entry": true}' WHERE id = 'STG-main-02-quote'""")
        self.assertNotIn("L08:STG-main-02-quote", self.finding_ids())

    def test_l08_follows_stage_on_other_timeline(self) -> None:
        self.sql("""UPDATE nodes SET attrs = '{"timeline": "aftercare", "sequence": 2}' WHERE id = 'STG-main-02-quote'""")
        self.add_edge("STG-main-02-quote", "enters from", "STG-main-01-inquiry")
        self.assertEqual(self.finding_ids(), {"L08:STG-main-02-quote>follows>STG-main-01-inquiry"})

    def test_l08_stages_share_sequence_on_timeline(self) -> None:
        self.add_node("STG-main-02-review", "Stage", None, "Review", '{"timeline": "main", "sequence": 2}')
        self.add_edge("STG-main-02-review", "follows", "STG-main-01-inquiry")
        self.assertEqual(self.finding_ids(), {"L08:STG-main-02-quote+STG-main-02-review"})
        self.sql("UPDATE nodes SET status = 'retired' WHERE id = 'STG-main-02-review'")
        self.assertEqual(self.finding_ids(), set())

    def add_aftercare_timeline(self) -> None:
        self.add_node("STG-aftercare-01-checkin", "Stage", None, "Check-in",
                      '{"timeline": "aftercare", "sequence": 1, "standalone_entry": true}')
        self.add_node("STG-aftercare-02-review", "Stage", None, "Review", '{"timeline": "aftercare", "sequence": 2}')
        self.add_edge("STG-aftercare-02-review", "follows", "STG-aftercare-01-checkin")

    def test_l08_parallel_timeline_needs_a_link(self) -> None:
        self.add_aftercare_timeline()
        self.assertEqual(self.finding_ids(), {"L08:STG-aftercare-01-checkin"})
        for verb in ("enters from", "joins"):
            self.add_edge("STG-aftercare-01-checkin", verb, "STG-main-02-quote")
            self.assertEqual(self.finding_ids(), set(), verb)
            self.drop_edge("STG-aftercare-01-checkin", verb, "STG-main-02-quote")

    def test_l08_link_on_last_stage_is_enough(self) -> None:
        self.add_aftercare_timeline()
        for verb in ("enters from", "joins"):
            self.add_edge("STG-aftercare-02-review", verb, "STG-main-01-inquiry")
            self.assertEqual(self.finding_ids(), set(), verb)
            self.drop_edge("STG-aftercare-02-review", verb, "STG-main-01-inquiry")

    def test_l08_timeline_without_standalone_entry_needs_no_link(self) -> None:
        self.add_node("STG-patient-01-registered", "Stage", None, "Registered", '{"timeline": "patient-account", "sequence": 1}')
        self.assertEqual(self.finding_ids(), set())

    def test_l08_link_to_retired_stage_does_not_count(self) -> None:
        self.add_aftercare_timeline()
        self.add_edge("STG-aftercare-02-review", "joins", "STG-main-01-inquiry")
        self.sql("UPDATE nodes SET status = 'retired' WHERE id = 'STG-main-01-inquiry'")
        self.assertIn("L08:STG-aftercare-01-checkin", self.finding_ids())

    def test_l09_entity_without_fields(self) -> None:
        self.add_node("ENT-booking", "Entity", "FR-004", "Booking")
        self.add_edge("ENT-booking", "decided by", "SRC-MTG-002-D03")
        self.assertEqual(self.finding_ids(), {"L09:ENT-booking"})

    def test_l10_rule_without_source(self) -> None:
        self.drop_edge("REQ-004-001", "decided by", "SRC-MTG-002-D03")
        self.assertEqual(self.finding_ids(), {"L10:REQ-004-001"})

    def test_l10_entity_without_source(self) -> None:
        self.drop_edge("ENT-quote", "decided by", "SRC-MTG-002-D03")
        self.assertEqual(self.finding_ids(), {"L10:ENT-quote"})

    def test_l11_field_node_without_fields_row(self) -> None:
        self.add_node("ENT-quote.currency", "Field", "FR-004", "Quote currency")
        self.assertEqual(self.finding_ids(), {"L11:ENT-quote.currency"})
        self.assertEqual(self.finding_ids("FR-004"), {"L11:ENT-quote.currency"})

    def test_fr_filter(self) -> None:
        self.add_node("FR-005", "FR", None, "Quote acceptance")
        self.add_node("REQ-005-001", "Rule", "FR-005", "Acceptance window", '{"statement": "x"}')
        self.add_edge("REQ-005-001", "decided by", "SRC-MTG-002-D03")
        self.assertEqual(self.finding_ids("FR-004"), set())
        self.assertEqual(self.finding_ids("FR-005"), {"L02:REQ-005-001"})

    def test_cli_reports_findings_and_exit_code(self) -> None:
        self.drop_edge("REQ-004-001", "decided by", "SRC-MTG-002-D03")
        code, out, _ = run_main(lint, ["--db", str(self.db_path), "--json"])
        self.assertEqual(code, 1)
        data = json.loads(out)
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["findings"][0]["id"], "L10:REQ-004-001")
        code, out, _ = run_main(lint, ["--db", str(self.db_path)])
        self.assertEqual(code, 1)
        self.assertIn("L10:REQ-004-001", out)

    def test_cli_rejects_unknown_fr_and_missing_db(self) -> None:
        code, _, err = run_main(lint, ["--db", str(self.db_path), "--fr", "FR-999"])
        self.assertEqual(code, 2)
        self.assertIn("FR-999", err)
        missing = self.dir / "missing.db"
        code, _, _ = run_main(lint, ["--db", str(missing)])
        self.assertEqual(code, 2)
        self.assertFalse(missing.exists(), "lint must not create a DB file")


class TestExport(GraphTestCase):
    def test_sorted_and_complete(self) -> None:
        data = export.build_export(self.conn, now=datetime(2026, 11, 5, tzinfo=timezone.utc))
        self.assertEqual(list(data), ["generated_at", "schema_version", "nodes", "fields", "enum_values", "edges", "sources", "changes"])
        self.assertEqual(data["generated_at"], "2026-11-05T00:00:00Z")
        self.assertEqual(data["schema_version"], SCHEMA.version)
        ids = [n["id"] for n in data["nodes"]]
        self.assertEqual(ids, sorted(ids))
        self.assertEqual(len(ids), 11)
        edge_keys = [(e["from_id"], e["verb"], e["to_id"]) for e in data["edges"]]
        self.assertEqual(edge_keys, sorted(edge_keys))
        self.assertEqual([v["value"] for v in data["enum_values"]], ["draft", "sent"])
        self.assertEqual(data["changes"], [{
            "id": "CS-0001", "at": "2026-11-05T09:00:00Z", "changed_by": "ba", "reason": "Initial load",
            "source_id": "SRC-MTG-002-D03", "nodes_added": [], "nodes_updated": ["REQ-004-001"],
            "edges_added": 0, "edges_removed": 0, "rows": 1,
        }])
        self.assertEqual(data["nodes"][ids.index("FR-004")]["attrs"]["module"], "P-02")

    def test_retired_rows_excluded_unless_requested(self) -> None:
        self.sql("UPDATE nodes SET status = 'retired' WHERE id = 'ENT-quote.status'")
        data = export.build_export(self.conn)
        self.assertNotIn("ENT-quote.status", {n["id"] for n in data["nodes"]})
        self.assertNotIn("ENT-quote.status", {f["id"] for f in data["fields"]})
        self.assertEqual(data["enum_values"], [])
        self.assertNotIn("ENT-quote.status", {e["to_id"] for e in data["edges"]})
        full = export.build_export(self.conn, include_retired=True)
        self.assertIn("ENT-quote.status", {n["id"] for n in full["nodes"]})
        self.assertEqual(len(full["enum_values"]), 2)

    def test_empty_db_has_no_change_sets(self) -> None:
        empty = self.dir / "empty.db"
        init_db.init_db(empty)
        conn = connect(empty)
        try:
            self.assertEqual(export.build_export(conn)["changes"], [])
        finally:
            conn.close()

    def test_change_sets_list_added_and_updated_nodes_newest_first(self) -> None:
        db = self.dir / "applied.db"
        init_db.init_db(db)
        conn = connect(db)
        try:
            first, rows = write.apply_changeset(conn, SCHEMA, {
                "reason": "Load quote rule", "by": "tester", "operations": [
                    {"op": "add_source", "id": "SRC-MTG-002-D03", "title": "Meeting 002 decision 3", "kind": "meeting",
                     "ref": "sources/mtg-002.md", "section": "D03", "date": "2026-10-16", "lifecycle": "validated"},
                    {"op": "add_node", "id": "FR-004", "type": "FR", "title": "Quote management", "attrs": {"module": "P-02"}},
                    {"op": "add_node", "id": "REQ-004-012", "type": "Rule", "owner_fr": "FR-004", "title": "Quote total",
                     "attrs": {"statement": "Total is the sum of line items."}},
                    {"op": "add_edge", "from": "REQ-004-012", "verb": "decided by", "to": "SRC-MTG-002-D03"},
                ],
            }, datetime(2026, 11, 5, 1, tzinfo=timezone.utc))
            changes = export.build_export(conn)["changes"]
            self.assertEqual(len(changes), 1)
            self.assertEqual(changes[0]["id"], first)
            self.assertEqual(changes[0]["nodes_added"], ["FR-004", "REQ-004-012", "SRC-MTG-002-D03"])
            self.assertEqual(changes[0]["nodes_updated"], [])
            self.assertEqual((changes[0]["edges_added"], changes[0]["edges_removed"], changes[0]["rows"]), (1, 0, rows))
            self.assertEqual((changes[0]["changed_by"], changes[0]["reason"], changes[0]["source_id"]), ("tester", "Load quote rule", None))

            second, rows = write.apply_changeset(conn, SCHEMA, {
                "reason": "Rename and re-source", "by": "ba", "source_id": "SRC-MTG-002-D03", "operations": [
                    {"op": "update_node", "id": "REQ-004-012", "title": "Quote grand total"},
                    {"op": "remove_edge", "from": "REQ-004-012", "verb": "decided by", "to": "SRC-MTG-002-D03"},
                    {"op": "add_node", "id": "ACT-provider", "type": "Actor", "title": "Provider", "attrs": {"group": "provider"}},
                ],
            }, datetime(2026, 11, 5, 2, tzinfo=timezone.utc))
            changes = export.build_export(conn)["changes"]
            self.assertEqual([c["id"] for c in changes], [second, first])
            self.assertEqual(changes[0]["nodes_added"], ["ACT-provider"])
            self.assertEqual(changes[0]["nodes_updated"], ["REQ-004-012"])
            self.assertEqual((changes[0]["edges_added"], changes[0]["edges_removed"], changes[0]["rows"]), (0, 1, rows))
            self.assertEqual(changes[0]["source_id"], "SRC-MTG-002-D03")

            # A calculated field's `calculated by` edge is recorded as field.calculated_by, not as an edge row.
            write.apply_changeset(conn, SCHEMA, {
                "reason": "Quote entity", "by": "ba", "operations": [
                    {"op": "add_node", "id": "ENT-quote", "type": "Entity", "owner_fr": "FR-004", "title": "Quote", "attrs": {"table": "quotes"}},
                    {"op": "add_field", "id": "ENT-quote.total", "entity_id": "ENT-quote", "name": "total", "data_type": "decimal",
                     "title": "Quote total", "owner_fr": "FR-004", "calculated_by": "REQ-004-012"},
                ],
            }, datetime(2026, 11, 5, 3, tzinfo=timezone.utc))
            latest = export.build_export(conn)["changes"][0]
            self.assertEqual((latest["nodes_added"], latest["nodes_updated"]), (["ENT-quote", "ENT-quote.total"], []))
            self.assertEqual((latest["edges_added"], latest["edges_removed"]), (1, 0))
        finally:
            conn.close()

    def test_cli_writes_file(self) -> None:
        out_path = self.dir / "out" / "graph.json"
        code, out, _ = run_main(export, [str(out_path), "--db", str(self.db_path)])
        self.assertEqual(code, 0, out)
        data = json.loads(out_path.read_text(encoding="utf-8"))
        self.assertEqual(len(data["sources"]), 1)
        self.assertFalse(out_path.with_name("graph.json.tmp").exists())


class TestRender(GraphTestCase):
    HEADINGS = [
        "## Scope", "## Actors", "## Workflows", "## Screen Specifications", "## Business Rules",
        "## Data", "## Events", "## Settings", "## Dependencies", "## Sources", "## Change Log",
    ]

    def rendered(self, fr: str = "FR-004") -> str:
        return render.render(self.conn, SCHEMA, fr)

    def test_header_and_headings_in_order(self) -> None:
        text = self.rendered()
        self.assertTrue(text.startswith("<!-- rendered from graph.db; do not edit by hand -->\n"))
        positions = [text.index(h + "\n") for h in self.HEADINGS]
        self.assertEqual(positions, sorted(positions))

    def test_section_content(self) -> None:
        text = self.rendered()
        self.assertIn("**FR-004 - Quote management**", text)
        self.assertIn("Providers build and send quotes.", text)
        self.assertIn("### [REQ-004-001] Quote total\n\nThe total is the sum of line items.", text)
        self.assertIn("| 2 | Quote (STG-main-02-quote) | SCR-004-01 Quote builder |", text)
        self.assertIn("| Status / state | no | system calculated | ENT-quote.status |", text)
        self.assertIn("| status (ENT-quote.status) | enum | yes | draft (Draft), sent (Sent) | - |", text)
        self.assertIn("[REQ-004-001] Quote total |", text)  # calculated-by column cites the Rule
        self.assertIn("| EVT-quote-sent | Quote sent | Quote (STG-main-02-quote) |", text)
        self.assertIn("| ACT-provider | Provider | STG-main-02-quote | SCR-004-01 |", text)
        self.assertIn("| SRC-MTG-002-D03 | meeting |", text)
        self.assertIn("| CS-0001 | 2026-11-05T09:00:00Z | ba | REQ-004-001 | Initial load |", text)

    def test_foreign_rule_rendered_as_citation_only(self) -> None:
        self.add_node("FR-005", "FR", None, "Quote acceptance")
        self.add_node("REQ-005-001", "Rule", "FR-005", "Discount cap", '{"statement": "SECRET BODY TEXT"}')
        self.add_node("ENT-quote.discount", "Field", "FR-004", "Discount")
        self.sql("INSERT INTO fields (id, entity_id, name, data_type, calculated_by) VALUES ('ENT-quote.discount', 'ENT-quote', 'discount', 'decimal', 'REQ-005-001')")
        self.add_edge("ENT-quote.discount", "calculated by", "REQ-005-001")
        text = self.rendered()
        self.assertIn("### Cited rules\n\n- [REQ-005-001] Discount cap\n", text)
        self.assertNotIn("SECRET BODY TEXT", text)
        self.assertNotIn("### [REQ-005-001]", text)
        self.assertIn("| FR-005 | Quote acceptance | REQ-005-001 |", text)

    def test_no_pipe_inside_cells(self) -> None:
        self.sql("UPDATE nodes SET title = 'Quote | builder' WHERE id = 'SCR-004-01'")
        self.sql("""UPDATE nodes SET attrs = '{"payload": "id | total\\nline two"}' WHERE id = 'EVT-quote-sent'""")
        text = self.rendered()
        tables: list[list[str]] = []
        previous_was_row = False
        for line in text.splitlines():
            is_row = line.startswith("|")
            if is_row and not previous_was_row:
                tables.append([])
            if is_row:
                tables[-1].append(line)
            previous_was_row = is_row
        self.assertGreater(len(tables), 5)
        for rows in tables:
            widths = {len(re.findall(r"\|", r)) for r in rows}
            self.assertEqual(len(widths), 1, rows)
        self.assertIn("id / total<br>line two", text)

    def test_empty_fr_renders_none_sections(self) -> None:
        self.add_node("FR-010", "FR", None, "Empty FR")
        text = self.rendered("FR-010")
        for heading in self.HEADINGS:
            self.assertIn(heading + "\n", text)
        self.assertIn("_No summary recorded._", text)

    def test_cli_out_file_and_bad_fr(self) -> None:
        out_path = self.dir / "fr004.md"
        code, _, _ = run_main(render, ["FR-004", "--db", str(self.db_path), "--out", str(out_path)])
        self.assertEqual(code, 0)
        self.assertIn("## Change Log", out_path.read_text(encoding="utf-8"))
        code, _, err = run_main(render, ["SCR-004-01", "--db", str(self.db_path)])
        self.assertEqual(code, 2)
        self.assertIn("not an FR id", err)


if __name__ == "__main__":
    unittest.main()
