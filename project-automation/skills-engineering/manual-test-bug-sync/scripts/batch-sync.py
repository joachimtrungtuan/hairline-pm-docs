#!/usr/bin/env python3
"""Deterministic table engine for Hairline manual test batch files.

Parses, validates, diffs, and merges batch files that follow
`testing/templates/manual-batch-template.md`, writes bug IDs and statuses,
maps Plane states to bug statuses, builds retest lists, and refreshes the
Batch Summary and phase plan Progress Summary tables.

This script never talks to Plane or the network. Plane reads and writes are
done by the plane-api-commands skill; this script only consumes their output.

Run with the isolated interpreter:  python3 -I batch-sync.py <command> --help
Every command prints JSON (or Markdown with --format md). Write commands are
dry-run unless --apply is given.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path

# ---------------------------------------------------------------- contract --

CASE_COLUMNS = [
    "ID", "Title", "Priority", "PRD flow ref", "Preconditions", "Test data",
    "Steps", "Expected result", "Actual result / data", "Result", "Notes",
    "Evidence", "Bug ID", "Bug status", "Last tested",
]
TESTER_COLUMNS = ["Actual result / data", "Result", "Notes", "Evidence", "Bug status", "Last tested"]
RUN_COLUMNS = ["Actual result / data", "Result", "Notes", "Evidence", "Last tested"]
TEAM_COLUMNS = ["Bug ID"]
DEFINITION_COLUMNS = [c for c in CASE_COLUMNS if c not in TESTER_COLUMNS + TEAM_COLUMNS + ["ID"]]

RESULTS = ["Not tested", "Pass", "Fail", "Blocked", "Retired"]
TESTER_RESULTS = ["Not tested", "Pass", "Fail", "Blocked"]
EXECUTED_RESULTS = {"Pass", "Fail", "Blocked"}
BUG_STATUSES = ["—", "Found", "Logged", "Fixed - retest", "Closed", "Reopened"]
TESTER_BUG_STATUSES = {"—", "Found"}
TEAM_BUG_STATUSES = {"Logged", "Fixed - retest", "Closed", "Reopened"}
OPEN_BUG_STATUSES = {"Found", "Logged", "Fixed - retest", "Reopened"}
PLANE_TRACKED_STATUSES = {"Logged", "Reopened", "Fixed - retest"}

TRANSITIONS = {
    "—": {"Found"},
    "Found": {"Logged", "—"},
    "Logged": {"Fixed - retest"},
    "Reopened": {"Fixed - retest"},
    "Fixed - retest": {"Closed", "Reopened"},
    "Closed": {"Reopened"},
}

CONTROL_TESTER_FIELDS = ["Tester", "Build tested"]
SUMMARY_COLUMNS = ["Total", "Pass", "Fail", "Blocked", "Not tested", "Open bugs"]
PROGRESS_COLUMNS = ["Batch"] + SUMMARY_COLUMNS + ["Last tested"]
SKIP_SECTION_COMPARE = {"Batch Control", "Test Cases", "Batch Summary"}

# Module codes per TEST-STRATEGY §4: P01-P07, PR01-PR07, A01-A10, S01-S06 (no letter suffixes).
CASE_ID_RE = re.compile(r"^(?P<base>(?:PR|[PAS])\d{2}-FR\d{3}-\d{2})\s+r(?P<rev>\d+)$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
BUG_KEY_RE = re.compile(r"^[A-Z][A-Z0-9]*-\d+$")
BR_RE = re.compile(r"<br\s*/?>", re.I)
CONTROL_ENTRY_RE = re.compile(r"^.+\(\d{4}-\d{2}-\d{2}\)$")
URL_RE = re.compile(r"^https?://\S+$")
VERSION_RE = re.compile(r"Phase\s*(?P<phase>\d+)\s*/\s*v?(?P<major>\d+)\.(?P<minor>\d+)", re.I)

# Plane state -> action. Group decides by default; names override the group.
PLANE_GROUP_ACTION = {
    "completed": "fixed",
    "cancelled": "cancelled",
    "backlog": "open",
    "unstarted": "open",
    "started": "open",
    "triage": "open",
}
PLANE_NAME_ACTION = {"waiting for deployment": "hold"}


class SyncError(Exception):
    pass


# ----------------------------------------------------------------- helpers --

def today_str(override: str | None) -> str:
    if override:
        return override
    try:
        from zoneinfo import ZoneInfo
        return dt.datetime.now(ZoneInfo("Asia/Saigon")).date().isoformat()
    except Exception:  # noqa: BLE001 - tz database missing
        return dt.date.today().isoformat()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canon_br(text: str) -> str:
    """`<br/>`, `<br />`, `<BR>` are the same line break as `<br>`."""
    return BR_RE.sub("<br>", text)


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", canon_br(text.replace("\r", ""))).strip()


def valid_date(value: str) -> bool:
    if not DATE_RE.match(value):
        return False
    try:
        dt.date.fromisoformat(value)
        return True
    except ValueError:
        return False


def split_row(line: str) -> list[str]:
    s = line.strip().replace("\r", "")
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def render_row(cells: list[str]) -> str:
    return "|" + "|".join(f" {c} " if c else " " for c in cells) + "|"


def is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", c) for c in cells)


def plain(cell: str) -> str:
    return cell.replace("*", "").strip()


def bug_keys(cell: str) -> list[str]:
    return [k.strip() for k in re.split(r"[,;]", cell) if k.strip()]


def normalize_enum(value: str, allowed: list[str], empty_default: str, dash_alias: str | None = None):
    """Return (canonical_value_or_None, warning_or_None)."""
    v = value.strip()
    if v in allowed:
        return v, None
    if v == "":
        return empty_default, f"empty value treated as `{empty_default}`"
    folded = re.sub(r"[‐-―\-]", "-", v).lower()
    folded = re.sub(r"\s*-\s*", " - ", folded) if " - " in "".join(allowed) else folded
    for a in allowed:
        if folded == a.lower():
            return a, f"`{v}` normalized to `{a}`"
    if dash_alias and re.fullmatch(r"[‐-―\-]+|n/?a|none", v, re.I):
        return dash_alias, f"`{v}` normalized to `{dash_alias}`"
    return None, None


def issue(level: str, code: str, message: str, **extra) -> dict:
    d = {"level": level, "code": code, "message": message}
    d.update(extra)
    return d


# ----------------------------------------------------------------- parsing --

class Batch:
    def __init__(self, path: Path):
        self.path = path
        raw = path.read_text(encoding="utf-8")
        self.lines = raw.split("\n")
        self.errors: list[dict] = []
        self.sections = self._sections()
        self.control, self.control_lines = self._control()
        self.header: list[str] = []
        self.cases: list[dict] = []
        self.index: dict[str, dict] = {}
        self._cases()

    # sections: title -> (start, end) where start is the heading line
    def _sections(self) -> dict[str, tuple[int, int]]:
        heads = [(i, l[3:].strip()) for i, l in enumerate(self.lines) if l.startswith("## ")]
        out = {"__preamble__": (0, heads[0][0] if heads else len(self.lines))}
        for n, (i, title) in enumerate(heads):
            end = heads[n + 1][0] if n + 1 < len(heads) else len(self.lines)
            out[title] = (i, end)
        return out

    def section_find(self, needle: str) -> tuple[int, int] | None:
        for title, span in self.sections.items():
            if title == needle or (needle.lower() in title.lower() and title != "__preamble__"):
                return span
        return None

    def table(self, span: tuple[int, int]) -> list[int]:
        start, end = span
        rows, started = [], False
        for i in range(start + 1, end):
            if self.lines[i].lstrip().startswith("|"):
                rows.append(i)
                started = True
            elif started:
                break
        return rows

    def _control(self):
        span = self.section_find("Batch Control")
        if not span:
            self.errors.append(issue("error", "missing_section", "Section `## Batch Control` not found"))
            return {}, {}
        values, where = {}, {}
        for i in self.table(span)[2:]:
            cells = split_row(self.lines[i])
            if len(cells) >= 2:
                values[plain(cells[0])] = cells[1]
                where[plain(cells[0])] = i
        return values, where

    def _cases(self):
        span = self.section_find("Test Cases")
        if not span:
            self.errors.append(issue("error", "missing_section", "Section `## Test Cases` not found"))
            return
        rows = self.table(span)
        if len(rows) < 2:
            self.errors.append(issue("error", "missing_table", "Test Cases table not found"))
            return
        self.header = split_row(self.lines[rows[0]])
        if not is_separator(split_row(self.lines[rows[1]])):
            self.errors.append(issue("error", "bad_table", "Test Cases header separator row missing", line=rows[1] + 1))
        width = len(self.header)
        for i in rows[2:]:
            line = self.lines[i]
            cells = split_row(line)
            if "\\|" in line:
                self.errors.append(issue("error", "pipe_in_cell", "Escaped vertical bar inside a cell", line=i + 1))
            if len(cells) != width:
                self.errors.append(issue(
                    "error", "column_count",
                    f"Row has {len(cells)} cells, header has {width}: a `|` typed inside a cell adds a cell, a deleted cell "
                    "removes one, and a real line break inside a cell splits the row (use `<br>`). Columns after that "
                    "point are shifted; fix the row in the tester copy",
                    line=i + 1, row_start=cells[0] if cells else ""))
                continue
            row = dict(zip(self.header, cells))
            m = CASE_ID_RE.match(row.get("ID", ""))
            if not m:
                self.errors.append(issue("error", "bad_case_id", f"Case ID `{row.get('ID', '')}` does not match `<MODULE><NN>-FR<NNN>-<SEQ> r<REV>` with MODULE one of P, PR, A, S (for example `PR01-FR002-03 r1`)", line=i + 1))
                continue
            case = {"id": row["ID"], "base": m.group("base"), "rev": int(m.group("rev")), "cells": row, "line": i}
            if case["base"] in self.index:
                self.errors.append(issue("error", "duplicate_case", f"Case `{case['base']}` appears twice", line=i + 1))
                continue
            self.index[case["base"]] = case
            self.cases.append(case)

    # derived
    @property
    def batch_id(self) -> str:
        return plain(self.control.get("Batch", ""))

    @property
    def version(self) -> dict | None:
        m = VERSION_RE.search(self.control.get("Phase / plan version", ""))
        if not m:
            return None
        return {k: int(v) for k, v in m.groupdict().items()}

    def section_text(self, title: str) -> str:
        start, end = self.sections[title]
        body = self.lines[start + 1:end] if title != "__preamble__" else self.lines[start:end]
        return "\n".join(norm(l) for l in body if norm(l))

    def write(self, expect_sha: str | None = None):
        if expect_sha and sha256(self.path) != expect_sha:
            raise SyncError(f"{self.path} changed since the preview (sha mismatch). Re-run the preview.")
        atomic_write(self.path, "\n".join(self.lines))


def atomic_write(path: Path, text: str):
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".batch-sync-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def load_hub(path: str) -> Batch:
    b = Batch(Path(path))
    if b.header and b.header != CASE_COLUMNS:
        b.errors.append(issue("error", "noncanonical_header",
                              "Test Cases header does not match the template columns", header=b.header, expected=CASE_COLUMNS))
    return b


# ---------------------------------------------------------------- find-hub --

def phase_folder_major(path: Path) -> tuple[str, int] | None:
    # .../phases/<phase-folder>/v<major>.0/batches/<file>.md
    try:
        vdir = path.parent.parent
        m = re.fullmatch(r"v(\d+)\.\d+", vdir.name)
        return (vdir.parent.name, int(m.group(1))) if m else None
    except Exception:  # noqa: BLE001
        return None


def cmd_find_hub(args) -> dict:
    tester = Batch(Path(args.tester))
    tv = tester.version
    out = {"tester": str(tester.path), "batch": tester.batch_id, "version": tv, "matches": [], "status": "not_found"}
    if not tester.batch_id or not tv:
        out["status"] = "tester_control_unreadable"
        return out
    root = Path(args.root)
    majors: dict[str, int] = {}
    for vdir in root.glob("*/v*"):
        m = re.fullmatch(r"v(\d+)\.\d+", vdir.name)
        if m:
            majors[vdir.parent.name] = max(majors.get(vdir.parent.name, 0), int(m.group(1)))
    for p in sorted(root.glob("*/v*/batches/*.md")):
        hub = Batch(p)
        hv = hub.version
        if hub.batch_id != tester.batch_id or not hv or hv["phase"] != tv["phase"]:
            continue
        folder = phase_folder_major(p)
        out["matches"].append({
            "path": str(p), "version": hv, "folder_major": folder[1] if folder else None,
            "frozen": bool(folder and majors.get(folder[0], 0) > folder[1]),
            "major_match": hv["major"] == tv["major"], "minor_match": hv["minor"] == tv["minor"],
        })
    exact = [m for m in out["matches"] if m["major_match"]]
    if len(exact) > 1:
        out["status"] = "ambiguous"
    elif len(exact) == 1:
        m = exact[0]
        out["hub"] = m["path"]
        out["status"] = "frozen_version" if m["frozen"] else ("ok" if m["minor_match"] else "minor_version_mismatch")
    elif out["matches"]:
        out["status"] = "major_version_mismatch"
    return out


# ----------------------------------------------------------------- compare --

def control_entries(value: str) -> list[str]:
    v = value.strip()
    if not v or v.startswith("{"):
        return []
    return [e.strip() for e in v.split(";") if e.strip()]


def entry_name(entry: str) -> str:
    return re.sub(r"\s*\(\d{4}-\d{2}-\d{2}\)$", "", entry).strip().lower()


def control_entries_update(field: str, hub_value: str, tester_value: str, tester_ran: bool):
    """Tester and Build tested accumulate `Name (YYYY-MM-DD)` entries joined by `; `; never overwrite."""
    warns = []
    hub_e, tes_e = control_entries(hub_value), control_entries(tester_value)
    if not tes_e:
        if tester_ran:
            warns.append(issue("warning", "control_field_blank",
                               f"Batch Control `{field}` is blank or still a placeholder in the tester copy; ask the tester for it "
                               "(`Name (YYYY-MM-DD)`); Plane bugs need it", field=field))
        return None, warns
    seen = {norm(e).lower() for e in hub_e}
    new = [e for e in tes_e if norm(e).lower() not in seen]
    if not new:
        return None, warns
    bad = [e for e in new if not CONTROL_ENTRY_RE.match(e)]
    if bad:
        warns.append(issue("warning", "control_entry_format",
                           f"Batch Control `{field}` entries {bad} are not `Name (YYYY-MM-DD)`; appended as written", field=field))
    if field == "Tester" and hub_e:
        hub_names = {entry_name(e) for e in hub_e}
        others = [e for e in new if entry_name(e) not in hub_names]
        if others:
            warns.append(issue("warning", "tester_changed",
                               f"A different tester ({'; '.join(others)}) is merging into a batch already tested by "
                               f"{'; '.join(hub_e)}; earlier entries are kept and the new ones appended", field=field))
    return {"field": field, "hub": hub_value, "tester": tester_value, "to": "; ".join(hub_e + new)}, warns


def compare(hub: Batch, tester: Batch, today: str, allow_minor: bool, resolutions: dict[str, str]) -> dict:
    res = {
        "hub": str(hub.path), "tester": str(tester.path), "hub_sha256": sha256(hub.path),
        "file_errors": [], "warnings": [], "control_updates": [], "cases": [],
        "missing_in_tester": [], "unknown_in_tester": [],
    }
    res["file_errors"] += [dict(e, file="hub") for e in hub.errors]
    res["file_errors"] += [dict(e, file="tester") for e in tester.errors]
    if tester.header and hub.header and tester.header != hub.header:
        res["file_errors"].append(issue("error", "header_changed", "Tester changed the Test Cases header (columns renamed, added, removed, or reordered)", tester=tester.header, hub=hub.header))
    if hub.batch_id != tester.batch_id:
        res["file_errors"].append(issue("error", "batch_mismatch", f"Batch `{tester.batch_id}` does not match hub `{hub.batch_id}`"))
    hv, tv = hub.version, tester.version
    stale_copy = bool(hv and tv and hv["phase"] == tv["phase"] and hv["major"] == tv["major"] and tv["minor"] < hv["minor"])
    if not hv or not tv:
        res["file_errors"].append(issue("error", "version_unreadable", "`Phase / plan version` unreadable in hub or tester file"))
    elif hv["phase"] != tv["phase"] or hv["major"] != tv["major"]:
        res["file_errors"].append(issue("error", "version_mismatch", f"Tester file is Phase {tv['phase']} v{tv['major']}.{tv['minor']}, hub is Phase {hv['phase']} v{hv['major']}.{hv['minor']}"))
    elif hv["minor"] != tv["minor"]:
        lvl = "warning" if allow_minor else "error"
        target = res["warnings"] if allow_minor else res["file_errors"]
        target.append(issue(lvl, "minor_version_mismatch", f"Tester file is v{tv['major']}.{tv['minor']}, hub is v{hv['major']}.{hv['minor']}; case revisions are still checked per case"))

    # Non-result sections: report edits as tester proposals, never merged. A copy issued before the
    # hub's last minor bump differs because the hub changed, so those differences are not proposals.
    stale_note = (f"stale copy, plan version v{tv['major']}.{tv['minor']} < hub v{hv['major']}.{hv['minor']}; "
                  "the difference is most likely the hub's own later edit, not a tester proposal") if stale_copy else ""
    for title in hub.sections:
        if title in SKIP_SECTION_COMPARE:
            continue
        if title not in tester.sections:
            res["warnings"].append(issue("warning", "section_removed", f"Tester copy lacks section `{title}` (not merged)"))
        elif hub.section_text(title) != tester.section_text(title):
            if stale_copy:
                res["warnings"].append(issue("warning", "section_stale", f"Section `{title}` differs ({stale_note}; not merged)", section=title))
            else:
                res["warnings"].append(issue("warning", "section_edited", f"Tester edited section `{title}`; treat as a proposal (not merged)", section=title))
    for field, value in tester.control.items():
        hub_value = hub.control.get(field)
        if hub_value is None:
            res["warnings"].append(issue("warning", "control_field_added", f"Tester added Batch Control field `{field}` (not merged)"))
        elif field in CONTROL_TESTER_FIELDS:
            continue
        elif norm(value) != norm(hub_value):
            if stale_copy and field == "Phase / plan version":
                continue  # already reported as minor_version_mismatch
            res["warnings"].append(issue("warning", "control_field_edited", f"Tester changed Batch Control `{field}` (not merged; proposal)", hub=hub_value, tester=value))
    tester_ran = any(normalize_enum(c["cells"].get("Result", ""), RESULTS, "Not tested")[0] in EXECUTED_RESULTS for c in tester.cases)
    for field in CONTROL_TESTER_FIELDS:
        if field not in hub.control_lines:
            continue
        upd, warns = control_entries_update(field, hub.control.get(field, ""), tester.control.get(field, ""), tester_ran)
        res["warnings"] += warns
        if upd:
            res["control_updates"].append(upd)

    for case in hub.cases:
        if case["base"] not in tester.index:
            res["missing_in_tester"].append(case["id"])
    for case in tester.cases:
        if case["base"] not in hub.index:
            res["unknown_in_tester"].append({"id": case["id"], "title": case["cells"].get("Title", "")})
            continue
        res["cases"].append(compare_case(hub.index[case["base"]], case, today, resolutions.get(case["base"])))
    if res["missing_in_tester"]:
        res["warnings"].append(issue("warning", "missing_cases", "Hub cases absent from tester copy (left unchanged)", cases=res["missing_in_tester"]))
    if res["unknown_in_tester"]:
        res["warnings"].append(issue("warning", "unknown_cases", "Tester copy has cases not in the hub (not merged; proposals for the plan owner)", cases=res["unknown_in_tester"]))

    counts = {}
    for c in res["cases"]:
        counts[c["status"]] = counts.get(c["status"], 0) + 1
    res["counts"] = counts
    blocked = res["file_errors"] or any(c["status"] in ("rejected", "conflict") for c in res["cases"]) or res["unknown_in_tester"]
    res["mergeable_all"] = not blocked
    res["mergeable_partial"] = not res["file_errors"]
    return res


SHIFT_HINT = ("Columns look shifted: a `|` typed inside a cell plus a deleted cell keeps the cell count but moves values "
              "into the wrong columns. Fix the row in the tester copy")


def evidence_entries(cell: str) -> list[str]:
    return [e.strip() for e in re.split(r"<br>|[,;]", canon_br(cell)) if e.strip()]


def evidence_issue(base: str, cell: str) -> dict | None:
    """Evidence holds file names `<case base ID>-<YYYYMMDD>-<n>.<ext>` or links (TEST-STRATEGY §5)."""
    entries = evidence_entries(cell)
    texty = [e for e in entries if re.search(r"\s", e) and not URL_RE.match(e)]
    if texty:
        return issue("error", "column_shift_suspected", f"Evidence holds text, not file names or links (`{texty[0][:60]}`). {SHIFT_HINT}")
    name_re = re.compile(re.escape(base) + r"-\d{8}-\d+\.[A-Za-z0-9]+$")
    off = [e for e in entries if not URL_RE.match(e) and not name_re.match(e)]
    if off:
        return issue("warning", "evidence_name", f"Evidence {off} does not follow `{base}-<YYYYMMDD>-<n>.<ext>`; rename the files and the cell before storing them")
    return None


def compare_case(h: dict, t: dict, today: str, resolution: str | None) -> dict:
    hc, tc = h["cells"], t["cells"]
    out = {"id": h["id"], "base": h["base"], "status": "unchanged", "changes": [], "issues": [], "bug_status": None}
    errs = out["issues"]

    stale = t["rev"] < h["rev"]
    if stale:
        # The hub changed the case after this copy was issued: definition differences are the hub's
        # own edit, not tester proposals.
        errs.append(issue("error", "stale_revision",
                          f"Stale copy, revision r{t['rev']} < hub r{h['rev']}: the case changed after this copy was issued. "
                          f"Results not merged; send the tester r{h['rev']} to rerun"))
    elif t["rev"] != h["rev"]:
        errs.append(issue("error", "revision_mismatch", f"Tester copy has r{t['rev']}, hub is r{h['rev']} (the hub never issued r{t['rev']})"))
    for col in ([] if stale else DEFINITION_COLUMNS):
        if norm(tc[col]) != norm(hc[col]):
            errs.append(issue("error", "definition_changed", f"Definition column `{col}` changed (proposal; not merged)", column=col, hub=hc[col], tester=tc[col]))
    if tc["Bug ID"].strip() and norm(tc["Bug ID"]) != norm(hc["Bug ID"]):
        errs.append(issue("error", "team_column_changed", "Tester changed `Bug ID` (team-owned)", hub=hc["Bug ID"], tester=tc["Bug ID"]))

    result, w = normalize_enum(tc["Result"], RESULTS, "Not tested")
    if result is None:
        errs.append(issue("error", "bad_result", f"Result `{tc['Result']}` is not one of {TESTER_RESULTS}"))
    elif w:
        errs.append(issue("warning", "result_normalized", w))
    bstatus, w = normalize_enum(tc["Bug status"], BUG_STATUSES, "—", dash_alias="—")
    if bstatus is None:
        errs.append(issue("error", "bad_bug_status", f"Bug status `{tc['Bug status']}` is not one of {BUG_STATUSES}"))
    elif w:
        errs.append(issue("warning", "bug_status_normalized", w))
    last = tc["Last tested"].strip()
    if last and not valid_date(last):
        errs.append(issue("error", "bad_date", f"Last tested `{last}` is not a valid YYYY-MM-DD date"))
    elif last and last > today:
        errs.append(issue("warning", "future_date", f"Last tested `{last}` is after today ({today})"))
    if norm(tc["Evidence"]) != norm(hc["Evidence"]):
        ev = evidence_issue(h["base"], tc["Evidence"])
        if ev:
            errs.append(ev)
    positional = [i for i in errs if i["code"] in ("bad_result", "bad_bug_status", "bad_date")]
    if len(positional) >= 2 and not any(i["code"] == "column_shift_suspected" for i in errs):
        errs.append(issue("error", "column_shift_suspected", SHIFT_HINT))

    if hc["Result"] == "Retired":
        if any(norm(tc[c]) != norm(hc[c]) for c in TESTER_COLUMNS):
            errs.append(issue("error", "case_retired", "Case is Retired in the hub; tester results not merged"))
    if result == "Retired" and hc["Result"] != "Retired":
        errs.append(issue("error", "tester_set_retired", "Only the plan owner sets `Retired`"))
    if result in EXECUTED_RESULTS and not last:
        errs.append(issue("error", "last_tested_missing", f"Result `{result}` needs a Last tested date"))
    if bstatus in TEAM_BUG_STATUSES and not (tc["Bug ID"].strip() or hc["Bug ID"].strip()):
        errs.append(issue("error", "bug_id_required", f"Bug status `{bstatus}` requires a Bug ID"))
    elif bstatus in TEAM_BUG_STATUSES and bstatus != hc["Bug status"].strip():
        errs.append(issue("warning", "tester_bug_status_ignored", f"Tester copy shows team status `{bstatus}`; hub `{hc['Bug status']}` is authoritative (team-owned)"))
    if result == "Fail" and not tc["Actual result / data"].strip():
        errs.append(issue("warning", "fail_without_actual", "Fail without Actual result / data"))
    if result == "Blocked" and not tc["Notes"].strip():
        errs.append(issue("warning", "blocked_without_reason", "Blocked without a reason in Notes"))
    if result == "Fail" and bstatus == "—" and hc["Bug status"] == "—":
        errs.append(issue("warning", "fail_without_bug_flag", "Fail but Bug status `—`; ask whether to log a bug"))

    if any(i["level"] == "error" for i in errs):
        out["status"] = "rejected"
        return out

    tv = {c: canon_br(tc[c].strip()) for c in RUN_COLUMNS}
    tv["Result"] = result
    hub_last = hc["Last tested"].strip()
    newer = bool(last) and (not hub_last or last > hub_last)
    differing = [c for c in RUN_COLUMNS if norm(tv[c]) != norm(hc[c])]
    defaults = {"Result": "Not tested"}
    conflict_reason = None
    take = []
    for c in differing:
        hub_empty = norm(hc[c]) in ("", defaults.get(c, ""))
        if hub_empty or newer:
            take.append(c)
        else:
            conflict_reason = "hub_has_same_or_newer_run"
    take_run = bool(take)

    hb = hc["Bug status"].strip()
    new_bs, bs_reason = hb, None
    # Decisions on team-owned statuses depend on the hub status and the newer run only, never on
    # what the tester copy shows (a tester who leaves `Closed` on a failing row must not hide it).
    if hb == "Fixed - retest" and newer and result in ("Pass", "Fail"):
        new_bs = "Closed" if result == "Pass" else "Reopened"
        bs_reason = "retest_outcome"
    elif hb == "Closed" and newer and result == "Fail":
        conflict_reason = conflict_reason or "closed_bug_failed_again"
        errs.append(issue("warning", "fail_on_closed_bug",
                          f"Fail on Closed bug {hc['Bug ID'].strip() or '(no Bug ID)'}: set Reopened (resolve `reopen`, same Bug ID), "
                          "or keep `hub` and log a new bug if it is a different defect"))
        bs_reason = "kept_hub_team_status"
    elif hb in TEAM_BUG_STATUSES:
        if hb in ("Logged", "Reopened") and newer and result == "Pass":
            errs.append(issue("warning", "open_bug_case_passed", f"Case passed while bug is `{hb}`; status kept, confirm with the team"))
        bs_reason = "kept_hub_team_status"
    elif bstatus != hb and hb in TESTER_BUG_STATUSES and bstatus in TESTER_BUG_STATUSES:
        new_bs, bs_reason = bstatus, "tester_flag"

    if conflict_reason and resolution not in ("tester", "hub", "reopen"):
        out["status"] = "conflict"
        out["conflict"] = {
            "reason": conflict_reason,
            "hub": {c: hc[c] for c in RUN_COLUMNS + ["Bug ID", "Bug status"]},
            "tester": {**{c: tv[c] for c in RUN_COLUMNS}, "Bug status": bstatus},
            "options": ["reopen", "hub"] if conflict_reason == "closed_bug_failed_again" else ["tester", "hub"],
        }
        return out
    if resolution == "hub":
        out["status"] = "unchanged"
        out["resolved_with"] = "hub"
        return out
    if resolution in ("tester", "reopen") and conflict_reason:
        take = differing
        take_run = True
        out["resolved_with"] = resolution
        if conflict_reason == "closed_bug_failed_again":
            new_bs, bs_reason = "Reopened", "user_reopened"
        elif hb == "Fixed - retest" and result in ("Pass", "Fail"):
            new_bs, bs_reason = ("Closed" if result == "Pass" else "Reopened"), "retest_outcome"

    for c in take:
        out["changes"].append({"column": c, "from": hc[c], "to": tv[c]})
    if new_bs != hb:
        if new_bs in TEAM_BUG_STATUSES and not hc["Bug ID"].strip():
            errs.append(issue("error", "bug_id_required", f"`{new_bs}` requires a Bug ID"))
            out["status"] = "rejected"
            out["changes"] = []
            return out
        out["bug_status"] = {"from": hb, "to": new_bs, "reason": bs_reason}
        out["changes"].append({"column": "Bug status", "from": hb, "to": new_bs})
    elif bs_reason == "kept_hub_team_status" and bstatus != hb:
        errs.append(issue("info", "kept_hub_bug_status", f"Hub `{hb}` kept; tester copy showed `{bstatus}`"))
    if out["changes"]:
        out["status"] = "update"
    return out


def apply_case_changes(hub: Batch, case_result: dict):
    case = hub.index[case_result["base"]]
    cells = [case["cells"][c] for c in hub.header]
    for ch in case_result["changes"]:
        cells[hub.header.index(ch["column"])] = ch["to"]
        case["cells"][ch["column"]] = ch["to"]
    hub.lines[case["line"]] = render_row(cells)


def set_control(hub: Batch, field: str, value: str):
    i = hub.control_lines[field]
    cells = split_row(hub.lines[i])
    cells[1] = value
    hub.lines[i] = render_row(cells)
    hub.control[field] = value


# ----------------------------------------------------------------- summary --

def fail_on_closed(cells: dict) -> bool:
    """A Fail row whose bug is still `Closed` is a regression the team has not reopened yet."""
    return cells["Bug status"].strip() == "Closed" and cells["Result"].strip() == "Fail"


def is_open_bug(cells: dict) -> bool:
    return cells["Bug status"].strip() in OPEN_BUG_STATUSES or fail_on_closed(cells)


def compute_summary(batch: Batch) -> dict:
    s = dict.fromkeys(SUMMARY_COLUMNS, 0)
    last = ""
    for c in batch.cases:
        r = c["cells"]["Result"].strip()
        if r != "Retired":
            s["Total"] += 1
            key = r if r in ("Pass", "Fail", "Blocked") else "Not tested"
            s[key] += 1
        if is_open_bug(c["cells"]):
            s["Open bugs"] += 1
        lt = c["cells"]["Last tested"].strip()
        if valid_date(lt) and lt > last:
            last = lt
    s["Last tested"] = last or "—"
    return s


def write_batch_summary(batch: Batch, s: dict) -> dict:
    span = batch.section_find("Batch Summary")
    if not span:
        raise SyncError(f"{batch.path}: `## Batch Summary` section not found")
    rows = batch.table(span)
    if len(rows) < 2 or [plain(c) for c in split_row(batch.lines[rows[0]])] != SUMMARY_COLUMNS:
        raise SyncError(f"{batch.path}: Batch Summary header must be {SUMMARY_COLUMNS}")
    new = render_row([str(s[c]) for c in SUMMARY_COLUMNS])
    if len(rows) >= 3:
        old = batch.lines[rows[2]]
        batch.lines[rows[2]] = new
    else:
        old = ""
        batch.lines.insert(rows[1] + 1, new)
    return {"from": old, "to": new}


def update_plan(plan_path: Path, summaries: dict[str, dict]) -> tuple[list[str], dict]:
    lines = plan_path.read_text(encoding="utf-8").split("\n")
    head = next((i for i, l in enumerate(lines) if l.startswith("## ") and "Progress Summary" in l), None)
    if head is None:
        raise SyncError(f"{plan_path}: Progress Summary section not found")
    rows, started = [], False
    for i in range(head + 1, len(lines)):
        if lines[i].startswith("## "):
            break
        if lines[i].lstrip().startswith("|"):
            rows.append(i)
            started = True
        elif started:
            break
    if len(rows) < 2 or [plain(c) for c in split_row(lines[rows[0]])] != PROGRESS_COLUMNS:
        raise SyncError(f"{plan_path}: Progress Summary header must be {PROGRESS_COLUMNS}")
    report = {"updated": [], "added": [], "unmatched_rows": []}
    total_row, seen = None, set()
    for i in rows[2:]:
        key = plain(split_row(lines[i])[0])
        if key.lower() == "total":
            total_row = i
        elif key in summaries:
            s = summaries[key]
            lines[i] = render_row([split_row(lines[i])[0]] + [str(s[c]) for c in SUMMARY_COLUMNS + ["Last tested"]])
            report["updated"].append(key)
            seen.add(key)
        else:
            report["unmatched_rows"].append(key)
    insert_at = total_row if total_row is not None else rows[-1] + 1
    for key in sorted(set(summaries) - seen):
        s = summaries[key]
        lines.insert(insert_at, render_row([key] + [str(s[c]) for c in SUMMARY_COLUMNS + ["Last tested"]]))
        insert_at += 1
        report["added"].append(key)
        if total_row is not None:
            total_row += 1
    totals = {c: sum(s[c] for s in summaries.values()) for c in SUMMARY_COLUMNS}
    dates = [s["Last tested"] for s in summaries.values() if valid_date(s["Last tested"])]
    totals["Last tested"] = max(dates) if dates else "—"
    total_line = render_row(["**Total**"] + [f"**{totals[c]}**" for c in SUMMARY_COLUMNS + ["Last tested"]])
    if total_row is not None:
        lines[total_row] = total_line
    else:
        lines.insert(insert_at, total_line)
    report["totals"] = totals
    return lines, report


def batches_for(args) -> list[Path]:
    paths: list[Path] = []
    if getattr(args, "plan", None):
        paths += sorted((Path(args.plan).parent / "batches").glob("*.md"))
    if getattr(args, "root", None):
        paths += sorted(Path(args.root).glob("*/v*/batches/*.md"))
    paths += [Path(p) for p in (getattr(args, "batch", None) or [])]
    if not paths:
        if getattr(args, "plan", None) or getattr(args, "root", None):
            where = Path(args.plan).parent / "batches" if getattr(args, "plan", None) else Path(args.root) / "*/v*/batches"
            raise SyncError(f"No batch files found in {where}. The plan has no written batches yet, so there is nothing "
                            "to summarize or scan; its Progress Summary was left unchanged")
        raise SyncError("Give --batch FILE, --plan plan.md, or --root phases-dir")
    return paths


# ----------------------------------------------------------------- commands --

def load_resolutions(items: list[str] | None) -> dict[str, str]:
    out = {}
    for item in items or []:
        if "=" not in item:
            raise SyncError(f"--resolve expects CASE=tester|hub|reopen, got `{item}`")
        k, v = item.split("=", 1)
        k = k.strip().split()[0]
        if v not in ("tester", "hub", "reopen"):
            raise SyncError(f"--resolve value must be tester, hub, or reopen (got `{v}`)")
        out[k] = v
    return out


def cmd_validate(args) -> dict:
    hub, tester = load_hub(args.hub), Batch(Path(args.tester))
    r = compare(hub, tester, today_str(args.today), args.allow_minor_mismatch, {})
    errors = list(r["file_errors"])
    warnings = list(r["warnings"])
    for c in r["cases"]:
        errors += [dict(i, case=c["id"]) for i in c["issues"] if i["level"] == "error"]
        warnings += [dict(i, case=c["id"]) for i in c["issues"] if i["level"] == "warning"]
    conflicts = [{"case": c["id"], "reason": c["conflict"]["reason"], "options": c["conflict"]["options"]}
                 for c in r["cases"] if c.get("conflict")]
    return {"hub": r["hub"], "tester": r["tester"], "valid": not errors and not r["unknown_in_tester"],
            "errors": errors, "warnings": warnings, "conflicts": conflicts, "unknown_in_tester": r["unknown_in_tester"],
            "missing_in_tester": r["missing_in_tester"]}


def cmd_diff(args) -> dict:
    hub, tester = load_hub(args.hub), Batch(Path(args.tester))
    return compare(hub, tester, today_str(args.today), args.allow_minor_mismatch, load_resolutions(args.resolve))


def cmd_merge(args) -> dict:
    hub, tester = load_hub(args.hub), Batch(Path(args.tester))
    r = compare(hub, tester, today_str(args.today), args.allow_minor_mismatch, load_resolutions(args.resolve))
    if r["file_errors"]:
        return {**r, "applied": False, "reason": "file-level errors block every merge"}
    if not r["mergeable_all"] and not args.partial:
        return {**r, "applied": False, "reason": "rejected cases, unresolved conflicts, or unknown cases; fix them, pass --resolve, or pass --partial to merge only clean cases"}
    updates = [c for c in r["cases"] if c["status"] == "update"]
    skipped = [c["id"] for c in r["cases"] if c["status"] in ("rejected", "conflict")]
    if not args.apply:
        return {**r, "applied": False, "would_update": [c["id"] for c in updates], "would_skip": skipped}
    if not args.expect_sha:
        raise SyncError("--apply needs --expect-sha <hub_sha256 from the confirmed diff>")
    if sha256(hub.path) != args.expect_sha:
        raise SyncError("Hub changed since the confirmed diff (sha mismatch). Re-run diff and re-confirm.")
    for c in updates:
        apply_case_changes(hub, c)
    for cu in r["control_updates"]:
        set_control(hub, cu["field"], cu["to"])
    summary = compute_summary(hub)
    write_batch_summary(hub, summary)
    hub.write()
    return {"applied": True, "hub": str(hub.path), "updated": [c["id"] for c in updates], "skipped": skipped,
            "control_updates": r["control_updates"], "batch_summary": summary, "hub_sha256_after": sha256(hub.path)}


def cmd_bugs(args) -> dict:
    out = {"to_log": [], "fail_without_bug_flag": [], "fail_on_closed_bug": [], "notes_to_review": [], "batches": []}
    for p in batches_for(args):
        b = Batch(p)
        ctx = {"batch_file": str(p), "batch": b.batch_id, "phase_version": b.control.get("Phase / plan version", ""),
               "module": b.control.get("Module", ""), "frs": b.control.get("FRs", ""),
               "platform": b.control.get("Platform", ""), "build_tested": b.control.get("Build tested", ""),
               "prd_sources": b.control.get("PRD sources", "")}
        out["batches"].append({**ctx, "errors": b.errors})
        for c in b.cases:
            cells = c["cells"]
            row = {"case": c["id"], "batch_file": str(p), "batch": b.batch_id, **{k: cells[k] for k in CASE_COLUMNS if k != "ID"}}
            bs, result = cells["Bug status"].strip(), cells["Result"].strip()
            if bs == "Found":
                out["to_log"].append({**row, "context": ctx})
            elif result == "Fail" and bs == "—":
                out["fail_without_bug_flag"].append(row)
            elif fail_on_closed(cells):
                out["fail_on_closed_bug"].append({**row, "action": "set Reopened with set-bug (Closed -> Reopened, same Bug ID), "
                                                  "or log a new bug if it is a different defect"})
            elif result != "Fail" and bs == "—" and cells["Notes"].strip():
                out["notes_to_review"].append({"case": c["id"], "batch_file": str(p), "Result": result, "Notes": cells["Notes"]})
    return out


def check_bug_value(bug_id: str):
    keys = bug_keys(bug_id)
    if not keys or any(not BUG_KEY_RE.match(k) for k in keys):
        raise SyncError(f"Bug ID `{bug_id}` must be Plane keys like HAIRL-1234 (comma-separated for split FE/BE tasks)")
    return ", ".join(keys)


def cmd_set_bug(args) -> dict:
    hub = load_hub(args.batch[0])
    if hub.errors:
        return {"applied": False, "errors": hub.errors}
    updates = json.loads(Path(args.updates).read_text(encoding="utf-8")) if args.updates else [
        {"case": args.case, "status": args.status, "bug_id": args.bug_id}]
    before = sha256(hub.path)
    planned, errors = [], []
    for u in updates:
        base = (u.get("case") or "").split()[0]
        case = hub.index.get(base)
        if not case:
            errors.append(issue("error", "unknown_case", f"Case `{u.get('case')}` not in {hub.path.name}"))
            continue
        cur_bs, cur_id = case["cells"]["Bug status"].strip(), case["cells"]["Bug ID"].strip()
        status = u.get("status") or cur_bs
        if status not in BUG_STATUSES:
            errors.append(issue("error", "bad_bug_status", f"`{status}` is not a Bug status", case=base))
            continue
        try:
            new_id = check_bug_value(u["bug_id"]) if u.get("bug_id") else cur_id
        except SyncError as e:
            errors.append(issue("error", "bad_bug_id", str(e), case=base))
            continue
        if status != cur_bs and status not in TRANSITIONS.get(cur_bs, set()) and not args.force:
            errors.append(issue("error", "illegal_transition", f"`{cur_bs}` -> `{status}` is not allowed (use --force only on explicit user instruction)", case=base))
            continue
        if status in TEAM_BUG_STATUSES and not new_id:
            errors.append(issue("error", "bug_id_required", f"`{status}` requires a Bug ID", case=base))
            continue
        if status == "Logged" and cur_bs == "Found" and not u.get("bug_id"):
            errors.append(issue("error", "bug_id_required", "Found -> Logged needs the new Plane key", case=base))
            continue
        planned.append({"case": case["id"], "base": base, "changes": [
            ch for ch in ({"column": "Bug ID", "from": cur_id, "to": new_id}, {"column": "Bug status", "from": cur_bs, "to": status})
            if ch["from"] != ch["to"]]})
    result = {"batch": str(hub.path), "hub_sha256": before, "planned": planned, "errors": errors, "applied": False}
    if errors or not args.apply:
        return result
    if args.expect_sha and before != args.expect_sha:
        raise SyncError("Batch changed since the preview (sha mismatch)")
    for p in planned:
        apply_case_changes(hub, p)
    result["batch_summary"] = compute_summary(hub)
    write_batch_summary(hub, result["batch_summary"])
    hub.write()
    result["applied"] = True
    return result


def classify_state(key: str, states: dict, groups: dict, hold: set[str]) -> dict:
    raw = states.get(key)
    if raw is None:
        return {"key": key, "action": "unknown", "state": None}
    name = raw.get("state") if isinstance(raw, dict) else raw
    group = (raw.get("group") if isinstance(raw, dict) else None) or groups.get((name or "").lower())
    lname = (name or "").lower()
    if lname in hold or PLANE_NAME_ACTION.get(lname) == "hold":
        action = "hold"
    elif lname in PLANE_NAME_ACTION:
        action = PLANE_NAME_ACTION[lname]
    else:
        action = PLANE_GROUP_ACTION.get((group or "").lower(), "unknown")
    return {"key": key, "state": name, "group": group, "action": action}


def cmd_apply_states(args) -> dict:
    states = json.loads(Path(args.states).read_text(encoding="utf-8"))
    groups = {}
    if args.values:
        values = json.loads(Path(args.values).read_text(encoding="utf-8"))
        groups = {s["name"].lower(): s.get("group") for s in values.get("states", [])}
    hold = {h.lower() for h in args.hold_state or []}
    out = {"set_fixed_retest": [], "ask_user": [], "no_change": [], "applied": []}
    for p in batches_for(args):
        b = load_hub(str(p))
        if b.errors:
            out["ask_user"].append({"batch_file": str(p), "reason": "batch_has_errors", "errors": b.errors})
            continue
        todo = []
        for c in b.cases:
            bs, ids = c["cells"]["Bug status"].strip(), c["cells"]["Bug ID"].strip()
            if bs not in PLANE_TRACKED_STATUSES or not ids:
                continue
            per_key = [classify_state(k, states, groups, hold) for k in bug_keys(ids)]
            actions = {k["action"] for k in per_key}
            row = {"batch_file": str(p), "case": c["id"], "bug_status": bs, "bug_id": ids, "plane": per_key}
            if "cancelled" in actions:
                out["ask_user"].append({**row, "reason": "plane_cancelled"})
            elif "unknown" in actions:
                out["ask_user"].append({**row, "reason": "plane_state_unknown"})
            elif bs == "Fixed - retest" and actions != {"fixed"}:
                out["ask_user"].append({**row, "reason": "plane_moved_back_after_fix"})
            elif bs in ("Logged", "Reopened") and actions == {"fixed"}:
                out["set_fixed_retest"].append(row)
                todo.append({"base": c["base"], "case": c["id"], "changes": [{"column": "Bug status", "from": bs, "to": "Fixed - retest"}]})
            else:
                out["no_change"].append({**row, "reason": "awaiting_deployment" if "hold" in actions else "not_resolved_in_plane"})
        if args.apply and todo:
            for t in todo:
                apply_case_changes(b, t)
            write_batch_summary(b, compute_summary(b))
            b.write()
            out["applied"].append({"batch_file": str(p), "cases": [t["case"] for t in todo]})
    return out


def cmd_retest_list(args) -> dict:
    items, reopen = [], []
    for p in batches_for(args):
        b = Batch(p)
        for c in b.cases:
            row = {"phase_version": b.control.get("Phase / plan version", ""), "batch": b.batch_id,
                   "batch_file": str(p), "case": c["id"], "title": c["cells"]["Title"],
                   "bug_id": c["cells"]["Bug ID"], "last_tested": c["cells"]["Last tested"]}
            if c["cells"]["Bug status"].strip() == "Fixed - retest":
                items.append(row)
            elif fail_on_closed(c["cells"]):
                reopen.append(row)
    # Fail rows on a Closed bug are not retest items yet: the team reopens the bug first.
    return {"count": len(items), "retest": items, "needs_reopen": reopen}


def cmd_summary(args) -> dict:
    out = {"batches": [], "plan": None, "applied": bool(args.apply)}
    summaries = {}
    for p in batches_for(args):
        b = load_hub(str(p))
        if b.errors:
            out["batches"].append({"batch_file": str(p), "errors": b.errors})
            continue
        s = compute_summary(b)
        summaries[b.batch_id] = s
        change = write_batch_summary(b, s)
        if args.apply and change["from"] != change["to"]:
            b.write()
        entry = {"batch_file": str(p), "batch": b.batch_id, "summary": s, "changed": change["from"] != change["to"]}
        flagged = [c["id"] for c in b.cases if fail_on_closed(c["cells"])]
        if flagged:
            entry["fail_on_closed_bug"] = flagged  # counted as open bugs; set Reopened with set-bug
        out["batches"].append(entry)
    if args.plan:
        lines, report = update_plan(Path(args.plan), summaries)
        if args.apply:
            atomic_write(Path(args.plan), "\n".join(lines))
        out["plan"] = {"path": args.plan, **report}
    return out


# ---------------------------------------------------------------- markdown --

def md_cell(v) -> str:
    return str(v).replace("|", "/").replace("\n", " ") if v not in (None, "") else "(empty)"


def to_markdown(cmd: str, data: dict) -> str:
    out = []
    if cmd in ("diff", "merge"):
        out.append(f"**Hub:** `{data.get('hub')}`  \n**Tester copy:** `{data.get('tester')}`  \n**Hub sha256:** `{data.get('hub_sha256')}`")
        out.append(f"**Counts:** {data.get('counts')}  \n**Mergeable (all):** {data.get('mergeable_all')}  \n**Mergeable (partial):** {data.get('mergeable_partial')}")
        if data.get("file_errors"):
            out.append("### File-level errors (block the merge)\n" + "\n".join(f"- `{e['code']}` ({e.get('file', '')}): {e['message']}" + (f" (line {e['line']})" if e.get("line") else "") for e in data["file_errors"]))
        if data.get("warnings"):
            def cases_of(w):
                ids = [c["id"] if isinstance(c, dict) else c for c in w.get("cases", [])]
                return f": {', '.join(ids)}" if ids else ""
            out.append("### Warnings and tester proposals (not merged)\n" + "\n".join(f"- `{w['code']}`: {w['message']}{cases_of(w)}" for w in data["warnings"]))
        if data.get("control_updates"):
            out.append("### Batch Control updates\n" + "\n".join(f"- {c['field']}: {md_cell(c['hub'])} -> {md_cell(c['to'])}" for c in data["control_updates"]))
        table = ["### Per-case preview", "", "| Case | Status | Changes | Issues |", "|---|---|---|---|"]
        for c in data.get("cases", []):
            ch = "<br>".join(f"{x['column']}: {md_cell(x['from'])} -> {md_cell(x['to'])}" for x in c["changes"]) or "—"
            iss = []
            for i in c["issues"]:
                detail = f" (hub: {md_cell(i['hub'])}; tester: {md_cell(i['tester'])})" if "hub" in i and "tester" in i else ""
                iss.append(f"{i['level']}: {i['message']}{detail}")
            if c.get("conflict"):
                cf = c["conflict"]
                hub_s = ", ".join(f"{k}={md_cell(v)}" for k, v in cf["hub"].items() if v)
                tes_s = ", ".join(f"{k}={md_cell(v)}" for k, v in cf["tester"].items() if v)
                iss.append(f"conflict: {cf['reason']} (options: {', '.join(cf['options'])})<br>hub: {hub_s}<br>tester: {tes_s}")
            table.append(f"| {c['id']} | {c['status']} | {md_cell(ch)} | {md_cell('<br>'.join(iss) or '—')} |")
        out.append("\n".join(table))
        return "\n\n".join(out) + "\n"
    if cmd == "retest-list":
        out.append(f"**Cases awaiting retest:** {data['count']}\n\n| Phase / version | Batch | Case | Title | Bug ID | Last tested |\n|---|---|---|---|---|---|")
        for i in data["retest"]:
            out.append(f"| {md_cell(i['phase_version'])} | {i['batch']} | {i['case']} | {md_cell(i['title'])} | {md_cell(i['bug_id'])} | {md_cell(i['last_tested'])} |")
        if data.get("needs_reopen"):
            out.append("\n**Fail on a Closed bug (reopen before retest):** "
                       + ", ".join(f"{i['case']} ({md_cell(i['bug_id'])})" for i in data["needs_reopen"]))
        return "\n".join(out) + "\n"
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


# --------------------------------------------------------------------- cli --

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp, fmt=False):
        sp.add_argument("--today", help="Override today's date (YYYY-MM-DD); default Asia/Saigon date")
        if fmt:
            sp.add_argument("--format", choices=["json", "md"], default="json")

    def pair(sp):
        sp.add_argument("--hub", required=True, help="Hub batch file under testing/manual/phases")
        sp.add_argument("--tester", required=True, help="Tester-returned batch file (any path)")
        sp.add_argument("--allow-minor-mismatch", action="store_true", help="Accept a minor plan-version difference (user-confirmed)")

    def scope(sp):
        sp.add_argument("--batch", action="append", help="Batch file (repeatable)")
        sp.add_argument("--plan", help="Phase plan.md; uses sibling batches/*.md")
        sp.add_argument("--root", help="testing/manual/phases (all phases and versions)")

    sp = sub.add_parser("find-hub", help="Locate the hub batch file for a tester copy")
    sp.add_argument("--tester", required=True)
    sp.add_argument("--root", required=True, help="testing/manual/phases")
    common(sp)

    sp = sub.add_parser("validate", help="Validate a tester copy against its hub file")
    pair(sp); common(sp)

    sp = sub.add_parser("diff", help="Per-case merge preview (no writes)")
    pair(sp); common(sp, fmt=True)
    sp.add_argument("--resolve", action="append", help="CASE=tester|hub|reopen for a reported conflict")

    sp = sub.add_parser("merge", help="Merge tester results into the hub (dry-run unless --apply)")
    pair(sp); common(sp, fmt=True)
    sp.add_argument("--resolve", action="append", help="CASE=tester|hub|reopen for a reported conflict")
    sp.add_argument("--partial", action="store_true", help="Merge clean cases; skip rejected and conflicted ones")
    sp.add_argument("--apply", action="store_true")
    sp.add_argument("--expect-sha", help="hub_sha256 from the diff the user confirmed (required with --apply)")

    sp = sub.add_parser("bugs", help="List rows to log in Plane and rows to review")
    scope(sp); common(sp)

    sp = sub.add_parser("set-bug", help="Write Bug ID / Bug status for cases (dry-run unless --apply)")
    sp.add_argument("--batch", action="append", required=True)
    sp.add_argument("--case")
    sp.add_argument("--status")
    sp.add_argument("--bug-id")
    sp.add_argument("--updates", help="JSON list of {case, status, bug_id}")
    sp.add_argument("--force", action="store_true", help="Allow a non-standard transition (explicit user instruction only)")
    sp.add_argument("--apply", action="store_true")
    sp.add_argument("--expect-sha")
    common(sp)

    sp = sub.add_parser("apply-states", help="Map Plane states to bug statuses (dry-run unless --apply)")
    scope(sp); common(sp)
    sp.add_argument("--states", required=True, help='JSON {"HAIRL-1234": "Finished"} or {"HAIRL-1234": {"state": ..., "group": ...}}')
    sp.add_argument("--values", help="plane-values.json to resolve state groups")
    sp.add_argument("--hold-state", action="append", help="Extra Plane state name meaning 'fixed but not deployed'")
    sp.add_argument("--apply", action="store_true")

    sp = sub.add_parser("retest-list", help="List cases with Bug status `Fixed - retest`")
    scope(sp); common(sp, fmt=True)

    sp = sub.add_parser("summary", help="Recompute Batch Summary and plan Progress Summary (dry-run unless --apply)")
    scope(sp); common(sp)
    sp.add_argument("--apply", action="store_true")
    return p


COMMANDS = {
    "find-hub": cmd_find_hub, "validate": cmd_validate, "diff": cmd_diff, "merge": cmd_merge,
    "bugs": cmd_bugs, "set-bug": cmd_set_bug, "apply-states": cmd_apply_states,
    "retest-list": cmd_retest_list, "summary": cmd_summary,
}


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        data = COMMANDS[args.cmd](args)
    except (SyncError, OSError, json.JSONDecodeError) as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        return 2
    if getattr(args, "format", "json") == "md":
        sys.stdout.write(to_markdown(args.cmd, data))
    else:
        sys.stdout.write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
