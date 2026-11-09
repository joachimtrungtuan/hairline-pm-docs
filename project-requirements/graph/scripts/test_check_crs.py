import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import check_crs

PRD = "# FR\n\nBody mentions CR-FR001-20260101-02.\n\n## Appendix: Change Log\n\n| Date | Version | Change |\n|---|---|---|\n| 2026-01-01 | 1.1 | Applied CR-FR001-20260101-01. |\n\n## Appendix: Approvals\n\nCR-FR001-20260101-03 approved.\n"


def cr(cr_id, status):
    return f"# Change Request\n\n**Change Request ID**: {cr_id}  \n**Decision Status**: {status}\n**Decision Date**: 2026-01-01\n"


class TestCheckCrs(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        d = self.root / "fr001-x"
        d.mkdir()
        (d / "prd.md").write_text(PRD)
        self.d = d

    def tearDown(self):
        self.tmp.cleanup()

    def add(self, name, cr_id, status):
        (self.d / f"change-request-{name}.md").write_text(cr(cr_id, status))

    def test_recorded_cr_passes(self):
        self.add("a", "CR-FR001-20260101-01", "Approved")
        result = check_crs.check(self.root)
        self.assertEqual(result["failures"], [])
        self.assertEqual(result["rows"][0]["result"], "recorded")

    def test_cr_named_only_outside_change_log_fails(self):
        self.add("b", "CR-FR001-20260101-02", "Approved")
        self.add("c", "CR-FR001-20260101-03", "Approved — superseded in part by CR-X")
        result = check_crs.check(self.root)
        self.assertEqual([f["cr"] for f in result["failures"]], ["CR-FR001-20260101-02", "CR-FR001-20260101-03"])
        self.assertTrue(all(f["result"] == "missing from change log (a row dated 2026-01-01 exists without the ID)" for f in result["failures"]))

    def test_id_prefix_does_not_match_longer_id(self):
        self.add("d", "CR-FR001-20260101-0", "Approved")
        self.assertTrue(check_crs.check(self.root)["failures"][0]["result"].startswith("missing from change log"))

    def test_proposed_cr_not_checked(self):
        self.add("e", "CR-FR001-20260101-09", "Proposed")
        result = check_crs.check(self.root)
        self.assertEqual((result["approved"], result["not_checked"], result["failures"]), (0, 1, []))

    def test_missing_prd_and_exit_code(self):
        other = self.root / "fr002-y"
        other.mkdir()
        (other / "change-request-z.md").write_text(cr("CR-FR002-20260101-01", "Approved"))
        self.assertEqual(check_crs.check(self.root)["failures"][0]["result"], "no prd.md beside the CR")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(check_crs.main(["--root", str(self.root)]), 1)


if __name__ == "__main__":
    unittest.main()
