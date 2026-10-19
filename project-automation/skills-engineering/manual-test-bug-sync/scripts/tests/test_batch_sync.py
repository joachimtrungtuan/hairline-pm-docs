"""Stdlib unit tests for batch-sync.py.

Run from anywhere:  python3 -I -m unittest discover -s <this folder> -v
Fixtures are built in a temporary folder; no project file is read or written.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "batch-sync.py"
_spec = importlib.util.spec_from_file_location("batch_sync", SCRIPT)
bs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bs)

TODAY = "2026-10-19"
COLS = bs.CASE_COLUMNS


def case(cid="PR01-FR002-01 r1", **cells) -> dict:
    row = {c: "" for c in COLS}
    row.update({"ID": cid, "Title": "Owner invites a clinician", "Priority": "High", "PRD flow ref": "FR-002 › Main Flow 2",
                "Preconditions": "Signed in as {V1}", "Test data": "DS-PR01-01", "Steps": "1. Open Team<br>2. Click Invite",
                "Expected result": "1. Invite sent", "Result": "Not tested", "Bug status": "—"})
    row.update(cells)
    return row


def batch_text(rows, tester="{Name}", build="{Version or date}", version="Phase 1 / v1.0", overview="Owner invites staff.",
               raw_rows: list[str] | None = None) -> str:
    lines = [
        "# B01 — PR-01 Team", "", "## Batch Control", "", "| Field | Value |", "|---|---|", "| Batch | B01 |",
        f"| Phase / plan version | {version} |", "| Module | PR-01 |", "| FRs | FR-002 |", "| PRD sources | x |",
        "| Platform | Provider dashboard |", f"| Tester | {tester} |", f"| Build tested | {build} |", "",
        "## Flow Overview", "", overview, "", "## Test Cases", "",
        "| " + " | ".join(COLS) + " |", "|" + "---|" * len(COLS),
    ]
    lines += [bs.render_row([r[c] for c in COLS]) for r in rows]
    lines += raw_rows or []
    lines += ["", "## Batch Summary", "", "| Total | Pass | Fail | Blocked | Not tested | Open bugs |",
              "|---|---|---|---|---|---|", "| 0 | 0 | 0 | 0 | 0 | 0 |", "", "## Case Change Log", "",
              "| Case | Revision | Date | Change |", "|---|---|---|---|", "| PR01-FR002-01 | r1 | 2026-10-19 | Created |", ""]
    return "\n".join(lines)


PLAN = """# Phase 1 plan

## 5. Progress Summary

| Batch | Total | Pass | Fail | Blocked | Not tested | Open bugs | Last tested |
|---|---|---|---|---|---|---|---|
| B01 | 0 | 0 | 0 | 0 | 0 | 0 | — |
| **Total** | | | | | | | |
"""


def run(*argv) -> tuple[int, dict]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = bs.main([str(a) for a in argv])
    text = out.getvalue() if code == 0 else err.getvalue()
    return code, json.loads(text) if text.strip().startswith("{") else {"raw": text}


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.vdir = self.root / "phases" / "phase-1-x" / "v1.0"
        (self.vdir / "batches").mkdir(parents=True)
        self.plan = self.vdir / "plan.md"
        self.plan.write_text(PLAN, encoding="utf-8")
        self.hub = self.vdir / "batches" / "B01-pr01-team.md"
        self.tester = self.root / "returned.md"

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, hub_rows, tester_rows=None, hub_kw=None, tester_kw=None, tester_raw=None):
        self.hub.write_text(batch_text(hub_rows, **(hub_kw or {})), encoding="utf-8")
        if tester_rows is not None or tester_raw is not None:
            self.tester.write_text(batch_text(tester_rows or [], raw_rows=tester_raw, **(tester_kw or {})), encoding="utf-8")

    def pair(self, cmd, *extra):
        return run(cmd, "--hub", self.hub, "--tester", self.tester, "--today", TODAY, *extra)

    @staticmethod
    def codes(items):
        return {i["code"] for i in items}


class FailOnClosedBug(Base):
    def setUp(self):
        super().setUp()
        self.closed = case(Result="Pass", **{"Bug ID": "HAIRL-1500", "Bug status": "Closed", "Last tested": "2026-10-10",
                                             "Actual result / data": "Invite sent"})

    def test_retest_fail_left_closed_is_a_conflict_with_warning(self):
        failed = dict(self.closed, Result="Fail", **{"Last tested": "2026-10-18", "Actual result / data": "Invite not sent"})
        self.write([self.closed], [failed])
        _, d = self.pair("diff")
        c = d["cases"][0]
        self.assertEqual(c["status"], "conflict")
        self.assertEqual(c["conflict"]["reason"], "closed_bug_failed_again")
        self.assertIn("fail_on_closed_bug", self.codes(c["issues"]))
        _, v = self.pair("validate")
        self.assertEqual(v["conflicts"][0]["reason"], "closed_bug_failed_again")
        self.assertIn("fail_on_closed_bug", self.codes(v["warnings"]))
        _, m = self.pair("merge")
        self.assertFalse(m["applied"])

    def test_reopen_resolution_sets_reopened(self):
        failed = dict(self.closed, Result="Fail", **{"Last tested": "2026-10-18", "Actual result / data": "Invite not sent"})
        self.write([self.closed], [failed])
        _, d = self.pair("diff", "--resolve", "PR01-FR002-01=reopen")
        self.assertEqual(d["cases"][0]["bug_status"]["to"], "Reopened")

    def test_hub_fail_on_closed_counts_open_and_is_listed(self):
        self.write([dict(self.closed, Result="Fail")])
        _, s = run("summary", "--plan", self.plan)
        self.assertEqual(s["batches"][0]["summary"]["Open bugs"], 1)
        self.assertEqual(s["batches"][0]["fail_on_closed_bug"], ["PR01-FR002-01 r1"])
        _, b = run("bugs", "--plan", self.plan)
        self.assertEqual([r["case"] for r in b["fail_on_closed_bug"]], ["PR01-FR002-01 r1"])
        _, r = run("retest-list", "--plan", self.plan)
        self.assertEqual((r["count"], len(r["needs_reopen"])), (0, 1))

    def test_fixed_retest_counts_as_open(self):
        self.write([dict(self.closed, Result="Fail", **{"Bug status": "Fixed - retest"})])
        _, s = run("summary", "--plan", self.plan)
        self.assertEqual(s["batches"][0]["summary"]["Open bugs"], 1)

    def test_open_bug_case_passed_warns_even_when_tester_keeps_status(self):
        logged = dict(self.closed, Result="Fail", **{"Bug status": "Logged"})
        passed = dict(logged, Result="Pass", **{"Last tested": "2026-10-18"})
        self.write([logged], [passed])
        _, d = self.pair("diff")
        self.assertIn("open_bug_case_passed", self.codes(d["cases"][0]["issues"]))


class Formatting(Base):
    def test_br_variants_are_not_definition_edits(self):
        for variant in ("<br/>", "<br />", "<BR>"):
            with self.subTest(variant=variant):
                self.write([case()], [case(Steps=f"1. Open Team{variant}2. Click Invite")])
                _, v = self.pair("validate")
                self.assertTrue(v["valid"], v["errors"])

    def test_letter_suffixed_module_rejected(self):
        self.write([case()], [case("A09a-FR031-01 r1")])
        _, v = self.pair("validate")
        self.assertIn("bad_case_id", self.codes(v["errors"]))

    def test_pipe_in_cell_reports_column_count(self):
        good = case(Result="Pass", **{"Last tested": "2026-10-18", "Actual result / data": "Saved"})
        raw = bs.render_row([good[c] for c in COLS]).replace("| Saved |", "| Saved | extra |")
        self.write([case()], tester_raw=[raw])
        _, v = self.pair("validate")
        err = next(e for e in v["errors"] if e["code"] == "column_count")
        self.assertIn("deleted cell", err["message"])

    def test_pipe_plus_deleted_cell_detected_as_shift(self):
        # Tester typed `|` inside Notes and deleted the empty Evidence cell: 15 cells, Notes text lands in Evidence.
        row = case(Result="Pass", **{"Last tested": "2026-10-18", "Notes": "Slow save", "Evidence": "no spinner shown"})
        self.write([case()], [row])
        _, v = self.pair("validate")
        self.assertIn("column_shift_suspected", self.codes(v["errors"]))

    def test_evidence_naming(self):
        ok = case(Result="Pass", **{"Last tested": "2026-10-18", "Evidence": "PR01-FR002-01-20261018-1.png, https://x.test/v"})
        self.write([case()], [ok])
        _, v = self.pair("validate")
        self.assertTrue(v["valid"], v["errors"])
        self.assertNotIn("evidence_name", self.codes(v["warnings"]))
        self.write([case()], [dict(ok, Evidence="shot-1.png")])
        _, v = self.pair("validate")
        self.assertIn("evidence_name", self.codes(v["warnings"]))


class ControlFields(Base):
    def test_blank_tester_and_build_warn_when_results_present(self):
        ran = case(Result="Pass", **{"Last tested": "2026-10-18"})
        self.write([case()], [ran], tester_kw={"tester": "", "build": "{Version or date}"})
        _, v = self.pair("validate")
        blanks = [w for w in v["warnings"] if w["code"] == "control_field_blank"]
        self.assertEqual({w["field"] for w in blanks}, {"Tester", "Build tested"})

    def test_entries_accumulate_and_new_tester_warns(self):
        hub_kw = {"tester": "Linh (2026-10-10)", "build": "1.4.0 (2026-10-10)"}
        ran = case(Result="Pass", **{"Last tested": "2026-10-18"})
        self.write([case()], [ran], hub_kw=hub_kw, tester_kw={"tester": "Minh (2026-10-18)", "build": "1.4.1 (2026-10-18)"})
        code, d = self.pair("diff")
        self.assertIn("tester_changed", self.codes(d["warnings"]))
        code, m = self.pair("merge", "--apply", "--expect-sha", d["hub_sha256"])
        self.assertTrue(m["applied"], m)
        text = self.hub.read_text(encoding="utf-8")
        self.assertIn("| Tester | Linh (2026-10-10); Minh (2026-10-18) |", text)
        self.assertIn("| Build tested | 1.4.0 (2026-10-10); 1.4.1 (2026-10-18) |", text)


class StaleCopies(Base):
    def test_older_case_revision_is_stale_not_a_proposal(self):
        self.write([case("PR01-FR002-01 r2", Steps="1. Open Team<br>2. Click Invite Member")], [case()])
        _, v = self.pair("validate")
        codes = self.codes(v["errors"])
        self.assertIn("stale_revision", codes)
        self.assertNotIn("definition_changed", codes)
        msg = next(e["message"] for e in v["errors"] if e["code"] == "stale_revision")
        self.assertIn("r1 < hub r2", msg)

    def test_older_minor_version_sections_are_stale(self):
        self.write([case()], [case()], hub_kw={"version": "Phase 1 / v1.1", "overview": "Owner invites staff (edited)."},
                   tester_kw={"version": "Phase 1 / v1.0"})
        _, d = self.pair("diff", "--allow-minor-mismatch")
        codes = self.codes(d["warnings"])
        self.assertIn("section_stale", codes)
        self.assertNotIn("section_edited", codes)
        self.assertNotIn("control_field_edited", codes)


class Summary(Base):
    def test_plan_without_batches_gives_clear_message(self):
        code, err = run("summary", "--plan", self.plan)
        self.assertEqual(code, 2)
        self.assertIn("No batch files found", err["error"])
        self.assertEqual(self.plan.read_text(encoding="utf-8"), PLAN)


if __name__ == "__main__":
    unittest.main()
