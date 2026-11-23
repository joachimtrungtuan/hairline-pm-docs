"""Tests for logic_gate.py. Run from this folder: /usr/bin/python3 -m unittest test_logic_gate"""

from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

import logic_gate
from common import connect
from test_logic_manifest import build_fixture, make_manifest

# Two planted defects, matched by a finding row on any item they list.
DEFECTS = {
    "fr": "FR-005",
    "round": 1,
    "defects": [
        {"id": "D1", "kind": "reversed word", "items": ["N:REQ-005-001"], "description": "48 hours after became before"},
        {"id": "D2", "kind": "removed link", "items": ["N:STP-005-002", "S:business-workflows/main-flow"],
         "description": "STP-005-002 lost its 'on' Screen"},
    ],
}
FINDING_ITEMS = {"N:REQ-005-001", "N:STP-005-002"}
EVIDENCE = "REQ-005-001 compared with SET-slot-hold and prd:11-12"
SCENARIO = """### Scenario FLW-quote-journey

| Step | Actor | Screen | Reads | Writes | Rules | Events | Next stage | Note |
|---|---|---|---|---|---|---|---|---|
| STP-004-001 | ACT-provider | SCR-004-01 | | | | | STG-main-03-accept | |
| STP-005-002 | ACT-patient | SCR-005-01 | | ENT-acceptance.state | REQ-005-001 | EVT-quote-accepted | STG-main-03-accept | prd:5 |
"""
NOT_CHECKED = "Payment hand-off to FR-007 could not be verified: FR-007 is not in this review copy."


def report(manifest: dict, rows: dict[str, str] | None = None, scenarios: str | None = SCENARIO,
           not_checked: str | None = NOT_CHECKED, drop: tuple[str, ...] = ()) -> str:
    """A complete report for the manifest. rows overrides whole table lines by item id; drop removes items."""
    rows = rows or {}
    table = ["| Item | Verdict | Evidence | Note |", "|---|---|---|---|"]
    for item in manifest["items"]:
        if item["id"] in drop:
            continue
        verdict = "finding" if item["id"] in FINDING_ITEMS else "OK"
        table.append(rows.get(item["id"], f"| {item['id']} | {verdict} | {EVIDENCE} | Q1 checked |"))
    parts = ["# FR-005 logic review, round 1, reviewer A", "",
             "Checklist: project-requirements/graph/checklists/logic-review.md v0.1", "",
             "## Verdicts", "", *table, "", "## Findings", "", "1. REQ-005-001 contradicts SET-slot-hold.", ""]
    if scenarios is not None:
        parts += ["## Scenarios", "", scenarios, ""]
    if not_checked is not None:
        parts += ["## Not checked or could not verify", "", not_checked, ""]
    return "\n".join(parts)


def b_report(items: list[str], attacks: str | None = None) -> str:
    """Reviewer B's report with one Attacks row per item id (or the given Attacks section body)."""
    if attacks is None:
        rows = [f"| {item} | OK | upheld | {EVIDENCE} | Q11 |" for item in items]
        attacks = "\n".join(["| Item | A's verdict | B's verdict | Evidence | Note |", "|---|---|---|---|---|", *rows])
    parts = ["# FR-005 logic review, round 1, reviewer B (adversarial)", ""]
    if attacks != "<none>":
        parts += ["## Attacks", attacks, ""]
    parts += ["## New scenarios", "", "### Scenario cancel at acceptance", "", "## Not checked or could not verify", "Nothing."]
    return "\n".join(parts)


# High-risk items of the fixture manifest: boundary edges, neighbour FRs, the Flow, and Rules, Settings,
# Steps, Stages and Actors (owned or referenced). Entities, Fields, Events, Screens, Sources and PRD sections are not.
HIGH_RISK = [
    "E:FR-004>references>REQ-005-001", "E:REQ-005-001>applies-to>ENT-quote", "E:SCR-004-01>shows>ENT-acceptance.state",
    "E:STP-004-001>next>STP-005-001", "F:FR-004", "F:FR-006", "N:FLW-quote-journey", "N:REQ-005-001", "N:SET-slot-hold",
    "N:STP-005-001", "N:STP-005-002", "N:STG-main-03-accept", "N:ACT-patient", "N:STP-004-001",
]
HIGH_RISK_OK = [i for i in HIGH_RISK if i not in FINDING_ITEMS]


class GateTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)
        self.db_path, self.prd_path = build_fixture(self.dir)
        self.manifest = make_manifest(self.db_path, self.prd_path)
        self.manifest_path = self.dir / "manifest.json"
        self.manifest_path.write_text(json.dumps(self.manifest), encoding="utf-8")
        self.defects_path = self.dir / "sealed.json"
        self.write_defects(DEFECTS)
        self.report_path = self.dir / "report.md"

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def write_defects(self, data: dict) -> None:
        self.defects_path.write_text(json.dumps(data), encoding="utf-8")

    def gate(self, text: str) -> logic_gate.GateResult:
        self.report_path.write_text(text, encoding="utf-8")
        return logic_gate.run_gate(self.manifest_path, self.report_path, self.defects_path)

    def assertVoid(self, result: logic_gate.GateResult, fragment: str) -> None:
        self.assertFalse(result.passed)
        self.assertTrue(any(fragment in f for f in result.failures), f"{fragment!r} not in {result.failures}")

    def run_main(self, argv: list[str]) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = logic_gate.main(argv)
        return code, out.getvalue(), err.getvalue()

    # Pass

    def test_complete_report_passes_with_full_recall(self) -> None:
        result = self.gate(report(self.manifest))
        self.assertEqual(result.failures, [])
        self.assertEqual((result.defects_found, result.defects_total), (["D1", "D2"], 2))

    def test_main_exit_codes_and_json(self) -> None:
        self.report_path.write_text(report(self.manifest), encoding="utf-8")
        argv = ["--manifest", str(self.manifest_path), "--report", str(self.report_path), "--defects", str(self.defects_path)]
        code, out, _ = self.run_main(argv)
        self.assertEqual(code, 0)
        self.assertIn("Planted defects found: 2 of 2", out)
        self.report_path.write_text(report(self.manifest, drop=("N:SET-slot-hold",)), encoding="utf-8")
        code, out, _ = self.run_main(argv + ["--json"])
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(out)["result"], "void")

    def test_cannot_verify_with_reason_passes(self) -> None:
        rows = {"N:SET-slot-hold": "| N:SET-slot-hold | cannot verify | | default unit not stated in the PRD |"}
        self.assertTrue(self.gate(report(self.manifest, rows)).passed)

    def test_none_with_a_reason_passes(self) -> None:
        text = report(self.manifest, not_checked="None: every manifest item and flow was compared above.")
        self.assertTrue(self.gate(text).passed)

    def test_id_followed_by_full_stop_is_cited_correctly(self) -> None:
        rows = {"N:ENT-acceptance": "| N:ENT-acceptance | OK | Written at STG-main-03-accept, shown as ENT-acceptance.state. | |"}
        self.assertTrue(self.gate(report(self.manifest, rows)).passed)

    # Void

    def test_missing_row_voids(self) -> None:
        self.assertVoid(self.gate(report(self.manifest, drop=("E:STP-004-001>next>STP-005-001",))),
                        "missing row for manifest item E:STP-004-001>next>STP-005-001")

    def test_unknown_and_repeated_rows_void(self) -> None:
        rows = {"N:SET-slot-hold": f"| N:SET-slot-hold | OK | {EVIDENCE} | |\n| N:REQ-005-777 | OK | REQ-005-001, prd:1 | |"}
        self.assertVoid(self.gate(report(self.manifest, rows)), "item is not in the manifest")
        rows = {"N:SET-slot-hold": "| N:SET-slot-hold | OK | | |\n| N:SET-slot-hold | OK | " + EVIDENCE + " | |"}
        self.assertVoid(self.gate(report(self.manifest, rows)), "second row for this item")

    def test_bare_ok_voids(self) -> None:
        for evidence in ("", "checked", "REQ-005-001", "prd:3 and prd:3"):
            with self.subTest(evidence=evidence):
                rows = {"N:SET-slot-hold": f"| N:SET-slot-hold | OK | {evidence} | |"}
                self.assertVoid(self.gate(report(self.manifest, rows)), "OK without evidence")

    def test_bare_finding_and_reasonless_cannot_verify_void(self) -> None:
        rows = {"N:REQ-005-001": "| N:REQ-005-001 | finding | wrong | Q1 |"}
        self.assertVoid(self.gate(report(self.manifest, rows)), "finding without evidence")
        rows = {"N:SET-slot-hold": "| N:SET-slot-hold | cannot verify | | |"}
        self.assertVoid(self.gate(report(self.manifest, rows)), "cannot verify without a reason")

    def test_unknown_verdict_voids(self) -> None:
        rows = {"N:SET-slot-hold": f"| N:SET-slot-hold | fine | {EVIDENCE} | |"}
        self.assertVoid(self.gate(report(self.manifest, rows)), "is not one of OK, finding, cannot verify")

    def test_cited_id_absent_from_graph_voids(self) -> None:
        rows = {"N:SET-slot-hold": "| N:SET-slot-hold | OK | SET-slot-hold vs REQ-005-042 | |"}
        self.assertVoid(self.gate(report(self.manifest, rows)), "cited id REQ-005-042 is not in the review graph")

    def test_prd_line_out_of_range_voids(self) -> None:
        for ref in ("prd:0", "prd:15", "prd:9-3", "prd:10-99"):
            with self.subTest(ref=ref):
                rows = {"N:SET-slot-hold": f"| N:SET-slot-hold | OK | SET-slot-hold vs {ref} | |"}
                self.assertVoid(self.gate(report(self.manifest, rows)), f"cited PRD line {ref} is outside 1-14")

    def test_neighbour_prd_line_is_not_range_checked(self) -> None:
        for ref in ("fr006 prd:173", "fr007b prd:2044-2045", "see fr003 prd:1232", "system-prd:1933"):
            with self.subTest(ref=ref):
                rows = {"N:SET-slot-hold": f"| N:SET-slot-hold | OK | SET-slot-hold vs {ref} | |"}
                result = self.gate(report(self.manifest, rows))
                self.assertFalse([f for f in result.failures if "is outside" in f])

    def test_bad_citation_in_scenario_voids(self) -> None:
        text = report(self.manifest, scenarios=SCENARIO.replace("EVT-quote-accepted", "EVT-quote-acepted"))
        self.assertVoid(self.gate(text), "Scenarios section: cited id EVT-quote-acepted")

    def test_missed_planted_defect_voids(self) -> None:
        rows = {"N:STP-005-002": f"| N:STP-005-002 | OK | {EVIDENCE} | |"}
        result = self.gate(report(self.manifest, rows))
        self.assertVoid(result, "planted defect D2 missed")
        self.assertEqual((result.defects_found, result.defects_missed), (["D1"], ["D2"]))

    def test_defect_matches_any_listed_item(self) -> None:
        rows = {"N:STP-005-002": f"| N:STP-005-002 | OK | {EVIDENCE} | |",
                "S:business-workflows/main-flow": f"| S:business-workflows/main-flow | finding | {EVIDENCE} | Q2 |"}
        self.assertTrue(self.gate(report(self.manifest, rows)).passed)

    def test_missing_or_bare_not_checked_section_voids(self) -> None:
        self.assertVoid(self.gate(report(self.manifest, not_checked=None)), "no '## Not checked or could not verify' section")
        self.assertVoid(self.gate(report(self.manifest, not_checked="")), "section is empty")
        self.assertVoid(self.gate(report(self.manifest, not_checked="None.")), "none without a sentence")

    def test_missing_flow_walkthrough_voids(self) -> None:
        self.assertVoid(self.gate(report(self.manifest, scenarios="### Scenario cancel at acceptance\n\nNo steps.")),
                        "no '### Scenario FLW-quote-journey' walkthrough")
        self.assertVoid(self.gate(report(self.manifest, scenarios=None)), "no '## Scenarios' section")

    def test_missing_verdicts_section_voids(self) -> None:
        text = report(self.manifest).replace("## Verdicts", "## Results")
        self.assertVoid(self.gate(text), "no '## Verdicts' section")

    # Reviewer B coverage count: informative only, never void

    def coverage(self, a_text: str, b_text: str) -> logic_gate.CoverageResult:
        self.report_path.write_text(a_text, encoding="utf-8")
        b_path = self.dir / "b-report.md"
        b_path.write_text(b_text, encoding="utf-8")
        return logic_gate.run_b_coverage(self.manifest_path, self.report_path, b_path)

    def coverage_main(self, a_text: str, b_text: str, *extra: str) -> tuple[int, str, str]:
        self.report_path.write_text(a_text, encoding="utf-8")
        b_path = self.dir / "b-report.md"
        b_path.write_text(b_text, encoding="utf-8")
        return self.run_main(["--manifest", str(self.manifest_path), "--report", str(self.report_path),
                              "--b-report", str(b_path), *extra])

    def test_high_risk_fixture_list_matches_the_manifest(self) -> None:
        manifest_high_risk = [i["id"] for i in self.manifest["items"] if logic_gate.is_high_risk(i)]
        self.assertEqual(sorted(manifest_high_risk), sorted(HIGH_RISK))

    def test_b_coverage_full(self) -> None:
        result = self.coverage(report(self.manifest), b_report(HIGH_RISK_OK))
        self.assertEqual((result.ok_total, len(result.named), result.not_named), (len(HIGH_RISK_OK), len(HIGH_RISK_OK), []))

    def test_b_coverage_lists_the_rows_b_did_not_name(self) -> None:
        named = [i for i in HIGH_RISK_OK if i not in ("F:FR-006", "N:ACT-patient")]
        result = self.coverage(report(self.manifest), b_report(named))
        self.assertEqual(result.ok_total, len(HIGH_RISK_OK))
        self.assertEqual(len(result.named), len(HIGH_RISK_OK) - 2)
        self.assertEqual(sorted(result.not_named), ["F:FR-006", "N:ACT-patient"])

    def test_b_coverage_counts_only_high_risk_ok_rows_of_a(self) -> None:
        # A's finding rows (REQ-005-001, STP-005-002) and OK rows on Entities or sections are outside the count;
        # B naming them, or naming ids A never gave, changes nothing.
        extra = ["N:ENT-quote", "N:REQ-005-001", "N:STP-005-002", "S:business-rules", "N:REQ-999-999"]
        result = self.coverage(report(self.manifest), b_report(HIGH_RISK_OK[:3] + extra))
        self.assertEqual((result.ok_total, len(result.named)), (len(HIGH_RISK_OK), 3))
        rows = {"N:SET-slot-hold": f"| N:SET-slot-hold | cannot verify | | not in the PRD |"}
        result = self.coverage(report(self.manifest, rows), b_report([]))
        self.assertEqual(result.ok_total, len(HIGH_RISK_OK) - 1)
        self.assertNotIn("N:SET-slot-hold", result.not_named)

    def test_b_coverage_counts_a_repeated_row_once_and_ignores_unknown_rows(self) -> None:
        rows = {"N:SET-slot-hold": f"| N:SET-slot-hold | OK | {EVIDENCE} | |\n| N:SET-slot-hold | OK | {EVIDENCE} | |\n"
                                   f"| N:REQ-005-777 | OK | {EVIDENCE} | |"}
        result = self.coverage(report(self.manifest, rows), b_report([]))
        self.assertEqual(result.ok_total, len(HIGH_RISK_OK))

    def test_b_coverage_exits_zero_even_when_nothing_is_named_or_a_report_is_void(self) -> None:
        code, out, _ = self.coverage_main(report(self.manifest, drop=("N:SET-slot-hold",)), b_report([]))
        self.assertEqual(code, 0)
        self.assertIn(f"0 of {len(HIGH_RISK_OK) - 1} high-risk OK rows", out)
        self.assertIn("  - N:ACT-patient", out)
        code, out, _ = self.coverage_main(report(self.manifest), b_report(HIGH_RISK_OK))
        self.assertEqual(code, 0)
        self.assertNotIn("Not named", out)

    def test_b_coverage_json_and_item_cells_with_backticks(self) -> None:
        code, out, _ = self.coverage_main(report(self.manifest), b_report([f"`{i}`" for i in HIGH_RISK_OK[1:]]), "--json")
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertEqual(data["high_risk_ok_rows_by_a"], len(HIGH_RISK_OK))
        self.assertEqual((data["named_by_b"], data["not_named_by_b"]), (len(HIGH_RISK_OK) - 1, [HIGH_RISK_OK[0]]))

    def test_b_coverage_bad_input_exits_two(self) -> None:
        for b_text, a_text, message in (
            (b_report([], attacks="<none>"), report(self.manifest), "no '## Attacks' section"),
            (b_report([], attacks="No table here."), report(self.manifest), "no table"),
            (b_report([], attacks="| Note |\n|---|\n| x |"), report(self.manifest), "no Item column"),
            (b_report([]), report(self.manifest).replace("## Verdicts", "## Results"), "no '## Verdicts' section"),
        ):
            with self.subTest(message=message):
                code, _, err = self.coverage_main(a_text, b_text)
                self.assertEqual(code, 2)
                self.assertIn(message, err)

    def test_defects_still_required_without_b_report(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
            logic_gate.main(["--manifest", str(self.manifest_path), "--report", str(self.report_path)])
        self.assertEqual(raised.exception.code, 2)

    # Bad input: exit 2, not a verdict on the report

    def test_review_copy_changed_after_manifest_is_an_input_error(self) -> None:
        conn = connect(self.db_path)
        conn.execute("UPDATE nodes SET title = 'Changed' WHERE id = 'SET-slot-hold'")
        conn.commit()
        conn.close()
        with self.assertRaisesRegex(logic_gate.GateInputError, "changed since the manifest"):
            self.gate(report(self.manifest))
        self.report_path.write_text(report(self.manifest), encoding="utf-8")
        code, _, err = self.run_main(["--manifest", str(self.manifest_path), "--report", str(self.report_path),
                                      "--defects", str(self.defects_path)])
        self.assertEqual(code, 2)
        self.assertIn("changed since the manifest", err)

    def test_malformed_defect_files_are_input_errors(self) -> None:
        bad = [
            ({**DEFECTS, "fr": "FR-004"}, "is not for FR-005"),
            ({**DEFECTS, "defects": []}, "has no defects list"),
            ({**DEFECTS, "defects": [{"id": "D1", "kind": "typo", "items": ["N:REQ-005-001"]}]}, "kind must be one of"),
            ({**DEFECTS, "defects": [{"id": "D1", "kind": "removed link", "items": ["N:REQ-005-777"]}]}, "not in the manifest"),
            ({**DEFECTS, "defects": [DEFECTS["defects"][0], DEFECTS["defects"][0]]}, "repeats id D1"),
        ]
        for data, message in bad:
            with self.subTest(message=message):
                self.write_defects(data)
                with self.assertRaisesRegex(logic_gate.GateInputError, message):
                    self.gate(report(self.manifest))

    def test_malformed_manifest_is_an_input_error(self) -> None:
        self.manifest_path.write_text(json.dumps({"fr": "FR-005"}), encoding="utf-8")
        with self.assertRaisesRegex(logic_gate.GateInputError, "missing a required key"):
            self.gate(report(self.manifest))


if __name__ == "__main__":
    unittest.main()
