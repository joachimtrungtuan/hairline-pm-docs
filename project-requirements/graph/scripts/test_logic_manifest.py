"""Tests for logic_manifest.py. Run from this folder: /usr/bin/python3 -m unittest test_logic_manifest"""

from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

import init_db
import logic_manifest
from common import connect, load_schema, open_db

SCHEMA = load_schema()
NOW = datetime(2026, 11, 10, 1, 0, tzinfo=timezone.utc)

# FR-005 (under review) owns a Rule, an Entity with one Field, an Event, a Setting, a Screen and two Steps;
# FR-004 owns the Step that hands over to FR-005 and a second, FR-004-only flow. FR-006 is named only in a
# Step hand-off. REQ-005-099 is retired and must not appear.
FIXTURE = """
INSERT INTO nodes (id, type, owner_fr, title, status, attrs) VALUES
  ('FR-004', 'FR', NULL, 'Quote submission', 'active', '{"module": "fr004-quote-submission"}'),
  ('FR-005', 'FR', NULL, 'Quote acceptance', 'active', '{"module": "fr005-quote-comparison-acceptance"}'),
  ('FR-006', 'FR', NULL, 'Booking', 'active', '{}'),
  ('STG-main-02-quote', 'Stage', NULL, 'Quote', 'active', '{"timeline": "main", "sequence": 2}'),
  ('STG-main-03-accept', 'Stage', NULL, 'Accept', 'active', '{"timeline": "main", "sequence": 3}'),
  ('ACT-patient', 'Actor', NULL, 'Patient', 'active', '{"group": "patient"}'),
  ('ACT-provider', 'Actor', NULL, 'Provider', 'active', '{"group": "provider"}'),
  ('SRC-MTG-002-D05', 'Source', NULL, 'Meeting 2 decision 5', 'active', '{}'),
  ('ENT-quote', 'Entity', 'FR-004', 'Quote', 'active', '{}'),
  ('SCR-004-01', 'Screen', 'FR-004', 'Quote builder', 'active', '{}'),
  ('STP-004-001', 'Step', 'FR-004', 'Provider sends quote', 'active', '{}'),
  ('STP-004-002', 'Step', 'FR-004', 'Provider edits draft', 'active', '{}'),
  ('REQ-005-001', 'Rule', 'FR-005', 'Hold slot', 'active', '{"statement": "Acceptance holds the slot for 48 hours."}'),
  ('REQ-005-099', 'Rule', 'FR-005', 'Old rule', 'retired', '{"statement": "Retired."}'),
  ('ENT-acceptance', 'Entity', 'FR-005', 'Acceptance', 'active', '{}'),
  ('ENT-acceptance.state', 'Field', 'FR-005', 'Acceptance state', 'active', '{}'),
  ('EVT-quote-accepted', 'Event', 'FR-005', 'Quote accepted', 'active', '{}'),
  ('SET-slot-hold', 'Setting', 'FR-005', 'Slot hold', 'active', '{"default": "48", "unit": "hours"}'),
  ('SCR-005-01', 'Screen', 'FR-005', 'Accept | confirm', 'active', '{}'),
  ('STP-005-001', 'Step', 'FR-005', 'Patient reviews quote', 'active', '{}'),
  ('STP-005-002', 'Step', 'FR-005', 'Patient accepts', 'active', '{"handoff_to": "FR-006 booking starts"}'),
  ('FLW-quote-journey', 'Flow', NULL, 'Quote to acceptance', 'active', '{"kind": "journey"}'),
  ('FLW-004-main', 'Flow', NULL, 'Quote drafting', 'active', '{"kind": "main"}');
INSERT INTO fields (id, entity_id, name, data_type, required, calculated_by) VALUES
  ('ENT-acceptance.state', 'ENT-acceptance', 'state', 'enum', 1, NULL);
INSERT INTO sources (id, kind, ref, section, date, lifecycle) VALUES
  ('SRC-MTG-002-D05', 'meeting', 'mtg-002.md', 'D05', '2026-09-09', 'validated');
INSERT INTO edges (from_id, verb, to_id, attrs) VALUES
  ('ACT-patient', 'acts in', 'STG-main-03-accept', '{}'),
  ('ACT-provider', 'acts in', 'STG-main-02-quote', '{}'),
  ('REQ-005-001', 'applies at', 'STG-main-03-accept', '{}'),
  ('REQ-005-001', 'governed by', 'SET-slot-hold', '{}'),
  ('REQ-005-001', 'decided by', 'SRC-MTG-002-D05', '{}'),
  ('REQ-005-001', 'applies to', 'ENT-quote', '{}'),
  ('REQ-005-099', 'applies to', 'ENT-quote', '{}'),
  ('FR-004', 'references', 'REQ-005-001', '{}'),
  ('STG-main-03-accept', 'emits', 'EVT-quote-accepted', '{}'),
  ('STG-main-03-accept', 'writes', 'ENT-acceptance', '{}'),
  ('SCR-005-01', 'belongs to', 'STG-main-03-accept', '{}'),
  ('SCR-005-01', 'shows', 'ENT-acceptance.state', '{"provenance": "system calculated"}'),
  ('SCR-004-01', 'shows', 'ENT-acceptance.state', '{"provenance": "retrieved"}'),
  ('STP-004-001', 'done by', 'ACT-provider', '{}'),
  ('STP-004-001', 'at', 'STG-main-02-quote', '{}'),
  ('STP-004-002', 'done by', 'ACT-provider', '{}'),
  ('STP-004-002', 'at', 'STG-main-02-quote', '{}'),
  ('STP-005-001', 'done by', 'ACT-patient', '{}'),
  ('STP-005-001', 'at', 'STG-main-03-accept', '{}'),
  ('STP-005-002', 'done by', 'ACT-patient', '{}'),
  ('STP-005-002', 'at', 'STG-main-03-accept', '{}'),
  ('STP-005-002', 'on', 'SCR-005-01', '{}'),
  ('STP-005-002', 'applies', 'REQ-005-001', '{}'),
  ('STP-004-001', 'next', 'STP-005-001', '{}'),
  ('STP-005-001', 'next', 'STP-005-002', '{"condition": "REQ-005-001", "label": "slot free"}'),
  ('FLW-quote-journey', 'starts at', 'STP-004-001', '{}'),
  ('FLW-004-main', 'starts at', 'STP-004-002', '{}');
"""

PRD = """# FR-005 - Quote Acceptance
Intro line.
## Business Workflows
### Main Flow
1. Patient accepts the quote.
```
## Not a heading inside a fence
```
### Alternative Flows
## Business Rules
### Notes
Holds last 48 hours.
### Notes
Second notes block.
"""


def build_fixture(directory: Path) -> tuple[Path, Path]:
    """Create a temp graph DB and PRD for FR-005 in directory; return their paths."""
    db_path = directory / "graph.db"
    init_db.init_db(db_path)
    conn = connect(db_path)
    try:
        conn.executescript(FIXTURE)
        conn.commit()
    finally:
        conn.close()
    prd_path = directory / "prd.md"
    prd_path.write_text(PRD, encoding="utf-8")
    return db_path, prd_path


def make_manifest(db_path: Path, prd_path: Path) -> dict:
    conn = open_db(db_path, SCHEMA, read_only=True)
    try:
        return logic_manifest.build_manifest(conn, SCHEMA, "FR-005", prd_path, db_path, now=NOW)
    finally:
        conn.close()


def run_main(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = logic_manifest.main(argv)
    return code, out.getvalue(), err.getvalue()


class ManifestTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.db_path, self.prd_path = build_fixture(self.dir)
        self.manifest = make_manifest(self.db_path, self.prd_path)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def ids(self, kind: str) -> list[str]:
        return [i["id"] for i in self.manifest["items"] if i["kind"] == kind]

    def test_sections_skip_fenced_headings_and_number_repeats(self) -> None:
        sections = [i for i in self.manifest["items"] if i["kind"] == logic_manifest.KIND_SECTION]
        self.assertEqual([(s["id"], s["lines"]) for s in sections], [
            ("S:fr-005-quote-acceptance", [1, 2]),
            ("S:business-workflows", [3, 3]),
            ("S:business-workflows/main-flow", [4, 8]),
            ("S:business-workflows/alternative-flows", [9, 9]),
            ("S:business-rules", [10, 10]),
            ("S:business-rules/notes", [11, 12]),
            ("S:business-rules/notes~2", [13, 14]),
        ])
        self.assertEqual(self.manifest["prd"]["lines"], 14)

    def test_owned_nodes_are_active_nodes_of_the_fr_in_schema_type_order(self) -> None:
        self.assertEqual(self.ids(logic_manifest.KIND_OWNED), [
            "N:ENT-acceptance", "N:ENT-acceptance.state", "N:REQ-005-001", "N:EVT-quote-accepted",
            "N:SET-slot-hold", "N:SCR-005-01", "N:STP-005-001", "N:STP-005-002",
        ])

    def test_referenced_nodes_are_one_live_edge_away_and_not_flows_or_frs(self) -> None:
        self.assertEqual(sorted(self.ids(logic_manifest.KIND_REFERENCED)), sorted([
            "N:STG-main-03-accept", "N:ACT-patient", "N:ENT-quote", "N:SCR-004-01", "N:STP-004-001", "N:SRC-MTG-002-D05",
        ]))

    def test_boundary_edges_cross_to_another_frs_node(self) -> None:
        self.assertEqual(self.ids(logic_manifest.KIND_EDGE), sorted([
            "E:FR-004>references>REQ-005-001",
            "E:REQ-005-001>applies-to>ENT-quote",
            "E:SCR-004-01>shows>ENT-acceptance.state",
            "E:STP-004-001>next>STP-005-001",
        ]))

    def test_neighbours_include_handoff_frs(self) -> None:
        self.assertEqual(self.ids(logic_manifest.KIND_NEIGHBOUR), ["F:FR-004", "F:FR-006"])
        fr004 = next(i for i in self.manifest["items"] if i["id"] == "F:FR-004")
        self.assertEqual(len(fr004["boundary_edges"]), 4)

    def test_only_flows_through_owned_steps_are_listed_with_their_path(self) -> None:
        flows = [i for i in self.manifest["items"] if i["kind"] == logic_manifest.KIND_FLOW]
        self.assertEqual([f["id"] for f in flows], ["N:FLW-quote-journey"])
        flow = flows[0]
        self.assertEqual([s["id"] for s in flow["steps"]], ["STP-004-001", "STP-005-001", "STP-005-002"])
        self.assertEqual(flow["next"][1], {"from": "STP-005-001", "to": "STP-005-002", "condition": "REQ-005-001", "label": "slot free"})

    def test_flow_with_a_loop_is_walked_once(self) -> None:
        conn = connect(self.db_path)
        conn.execute("INSERT INTO edges (from_id, verb, to_id, attrs) VALUES ('STP-005-002', 'next', 'STP-005-001', '{\"back\": true}')")
        conn.commit()
        conn.close()
        flow = next(i for i in make_manifest(self.db_path, self.prd_path)["items"] if i["kind"] == logic_manifest.KIND_FLOW)
        self.assertEqual(len(flow["steps"]), 3)
        self.assertEqual(len(flow["next"]), 3)

    def test_item_ids_are_unique_and_stable(self) -> None:
        ids = [i["id"] for i in self.manifest["items"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(ids, [i["id"] for i in make_manifest(self.db_path, self.prd_path)["items"]])
        self.assertEqual(sum(self.manifest["counts"].values()), len(ids))

    def test_markdown_lists_every_item_without_pipes_in_cells(self) -> None:
        text = logic_manifest.to_markdown(self.manifest)
        for item in self.manifest["items"]:
            self.assertIn(item["id"], text)
        self.assertIn("Accept / confirm", text)
        self.assertIn("### Path of FLW-quote-journey", text)

    def test_unknown_fr_is_rejected(self) -> None:
        conn = open_db(self.db_path, SCHEMA, read_only=True)
        try:
            with self.assertRaises(ValueError):
                logic_manifest.build_manifest(conn, SCHEMA, "FR-099", self.prd_path, self.db_path)
        finally:
            conn.close()

    def test_default_prd_path_uses_module(self) -> None:
        conn = open_db(self.db_path, SCHEMA, read_only=True)
        try:
            g = logic_manifest.load_graph(conn)
        finally:
            conn.close()
        self.assertEqual(logic_manifest.default_prd_path(g, "FR-005"),
                         logic_manifest.BASELINE_DIR / "fr005-quote-comparison-acceptance" / "prd.md")
        with self.assertRaises(logic_manifest.ManifestError):
            logic_manifest.default_prd_path(g, "FR-006")

    def test_main_writes_json_and_leaves_the_db_unchanged(self) -> None:
        before = logic_manifest.file_sha256(self.db_path)
        out = self.dir / "manifest.json"
        code, _, err = run_main(["FR-005", "--db", str(self.db_path), "--prd", str(self.prd_path), "--out", str(out)])
        self.assertEqual((code, err), (0, ""))
        data = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(data["fr"], "FR-005")
        self.assertEqual(data["db"]["sha256"], before)
        self.assertEqual(logic_manifest.file_sha256(self.db_path), before)

    def test_main_markdown_to_stdout(self) -> None:
        code, out, _ = run_main(["FR-005", "--db", str(self.db_path), "--prd", str(self.prd_path), "--format", "md"])
        self.assertEqual(code, 0)
        self.assertTrue(out.startswith("# FR-005 logic-review manifest"))

    def test_main_errors(self) -> None:
        self.assertEqual(run_main(["FR-099", "--db", str(self.db_path), "--prd", str(self.prd_path)])[0], 1)
        self.assertEqual(run_main(["FR-005", "--db", str(self.dir / "none.db"), "--prd", str(self.prd_path)])[0], 1)
        self.assertEqual(run_main(["FR-005", "--db", str(self.db_path), "--prd", str(self.dir / "none.md")])[0], 1)
        self.assertEqual(run_main(["FR-006", "--db", str(self.db_path)])[0], 1)


if __name__ == "__main__":
    unittest.main()
