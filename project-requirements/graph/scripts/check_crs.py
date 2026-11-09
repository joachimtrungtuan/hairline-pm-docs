#!/usr/bin/env python3
"""Check that every Approved Change Request is recorded in its PRD's change log.

Usage: check_crs.py [--root FR_FOLDER] [--json]

For each change-request-*.md under the functional-requirements folder, read its
**Change Request ID** and **Decision Status**. A CR whose status starts with
"Approved" must have its ID in the "## Appendix: Change Log" section of prd.md in
the same folder. A missing ID is reported with whether a change-log row exists on the
CR's Decision Date, which usually means the change is logged but not cited. CRs with another status (such as Proposed) are listed but not
checked; they stay out of the graph (D42).

Exit codes: 0 every Approved CR is recorded, 1 one or more are not, 2 error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[2] / "functional-requirements"
FIELD = r"^\*\*{name}\*\*:\s*(.+?)\s*$"
CHANGE_LOG = "## Appendix: Change Log"


def _field(text: str, name: str) -> str | None:
    m = re.search(FIELD.format(name=re.escape(name)), text, re.MULTILINE)
    return m.group(1) if m else None


def change_log_section(prd_text: str) -> str | None:
    """Return the text of the PRD's Appendix: Change Log section, or None if absent."""
    start = prd_text.find(CHANGE_LOG)
    if start < 0:
        return None
    body = prd_text[start + len(CHANGE_LOG):]
    nxt = re.search(r"^#{1,2} ", body, re.MULTILINE)
    return body[: nxt.start()] if nxt else body


def check(root: Path) -> dict:
    rows = []
    for cr in sorted(root.glob("*/change-request-*.md")):
        text = cr.read_text(encoding="utf-8")
        cr_id = _field(text, "Change Request ID")
        status = _field(text, "Decision Status") or ""
        row = {"cr": cr_id, "file": str(cr.relative_to(root)), "status": status, "result": "not checked"}
        if not status.startswith("Approved"):
            rows.append(row)
            continue
        prd = cr.parent / "prd.md"
        if not cr_id:
            row["result"] = "no Change Request ID"
        elif not prd.exists():
            row["result"] = "no prd.md beside the CR"
        else:
            log = change_log_section(prd.read_text(encoding="utf-8"))
            if log is None:
                row["result"] = "PRD has no Appendix: Change Log"
            elif re.search(rf"(?<![\w-]){re.escape(cr_id)}(?![\w-])", log):
                row["result"] = "recorded"
            else:
                m = re.search(r"\d{4}-\d{2}-\d{2}", _field(text, "Decision Date") or "")
                dated = m and re.search(rf"^\|\s*{m.group(0)}\s*\|", log, re.MULTILINE)
                row["result"] = "missing from change log" + (
                    f" (a row dated {m.group(0)} exists without the ID)" if dated else " (no row on the decision date)")
        rows.append(row)
    failures = [r for r in rows if r["status"].startswith("Approved") and r["result"] != "recorded"]
    return {
        "approved": sum(r["status"].startswith("Approved") for r in rows),
        "not_checked": sum(not r["status"].startswith("Approved") for r in rows),
        "failures": failures,
        "rows": rows,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=str(DEFAULT_ROOT), help="functional-requirements folder")
    parser.add_argument("--json", action="store_true", help="print the full result as JSON")
    args = parser.parse_args(argv)
    root = Path(args.root)
    if not root.is_dir():
        print(f"error: {root} is not a folder", file=sys.stderr)
        return 2
    result = check(root)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for r in result["failures"]:
            print(f"{r['cr'] or '?'}\t{r['file']}\t{r['result']}")
        for r in result["rows"]:
            if r["result"] == "not checked":
                print(f"{r['cr'] or '?'}\t{r['file']}\tnot checked ({r['status']})")
        print(f"{result['approved']} Approved CRs, {len(result['failures'])} not recorded; {result['not_checked']} not checked")
    return 1 if result["failures"] else 0


if __name__ == "__main__":
    sys.exit(main())
