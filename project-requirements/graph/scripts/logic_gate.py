"""Mechanical gate for one logic-review report (checklists/logic-review.md, procedure step 4).

Usage: logic_gate.py --manifest MANIFEST.json --report REPORT.md --defects SEALED.json
                     [--db DB_PATH] [--prd PRD_PATH] [--json]

The review copy (DB and PRD) defaults to the paths recorded in the manifest; both must still match the
manifest's sha256, so citations are checked against exactly what the reviewer read. The report is void
when any of these holds:
  - a manifest item has no row in the Verdicts table, or a row names an unknown item or repeats one;
  - a row's verdict is not OK, finding or cannot verify;
  - an OK or finding row cites fewer than two references (bare verdict), or a cannot-verify row gives
    no reason;
  - an id cited in the Verdicts Evidence column or in the Scenarios section is not in the review DB,
    or a cited PRD line (prd:N or prd:N-M) is outside the review PRD;
  - a Flow in the manifest has no "### Scenario <FLW-id>" walkthrough;
  - the "Not checked or could not verify" section is missing, empty, or a bare "none";
  - a planted defect has no finding row on any of the manifest items it lists.

Output names every failure and the planted-defect recall. This output is for the controller only.
Exit codes: 0 pass, 1 void, 2 bad input (unreadable or malformed file, review copy changed).

Reviewer B coverage count (a count for the controller, not a gate on B):
    logic_gate.py --manifest MANIFEST.json --report A_REPORT.md --b-report B_REPORT.md [--json]
Counts the OK rows reviewer A gave on high-risk items (boundary edges, neighbour FRs, Flows, and Steps,
Stages, Actors, Settings and Rules), and how many of them the Item column of B's "## Attacks" table
names. Lists those B did not name. Never voids anything: exit 0 whenever both reports and the manifest
parse, 2 otherwise. No DB, PRD or defect file is read in this mode.
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from common import Schema, SchemaError, load_schema, open_db
from logic_manifest import KIND_FLOW, file_sha256

VERDICTS = ("ok", "finding", "cannot verify")
DEFECT_KINDS = (
    "contradicting threshold across FRs",
    "reversed word",
    "removed link",
    "unreachable stage",
    "actor permission swap",
)
SECTION_VERDICTS = "verdicts"
SECTION_SCENARIOS = "scenarios"
SECTION_NOT_CHECKED = "not checked or could not verify"
SECTION_ATTACKS = "attacks"
TABLE_COLUMNS = ("item", "verdict", "evidence", "note")
HIGH_RISK_KINDS = ("boundary edge", "neighbour FR", KIND_FLOW)
HIGH_RISK_NODE_TYPES = ("Step", "Stage", "Actor", "Setting", "Rule")
MIN_CITATIONS = 2

_PRD_REF = re.compile(r"\bprd:(\d+)(?:-(\d+))?\b", re.IGNORECASE)
_FENCE = re.compile(r"^\s*(```|~~~)")
_H2 = re.compile(r"^##\s+(.+?)\s*#*\s*$")
_SCENARIO = re.compile(r"^###\s+Scenario\s+(FLW-[A-Za-z0-9-]*[A-Za-z0-9])\b")
_SEPARATOR = re.compile(r"^\|?\s*:?-{3,}")
_BARE_NONE = re.compile(r"none\W*", re.IGNORECASE)


class GateInputError(ValueError):
    """Raised when an input file cannot be read or does not have the expected shape."""


@dataclass
class Row:
    line: int
    item: str
    verdict: str
    evidence: str
    note: str


@dataclass
class GateResult:
    failures: list[str] = field(default_factory=list)
    defects_total: int = 0
    defects_found: list[str] = field(default_factory=list)
    defects_missed: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.failures

    def as_dict(self) -> dict[str, Any]:
        return {
            "result": "pass" if self.passed else "void",
            "failures": self.failures,
            "planted_defects": {"total": self.defects_total, "found": self.defects_found, "missed": self.defects_missed},
        }


@dataclass
class CoverageResult:
    ok_total: int = 0
    named: list[str] = field(default_factory=list)
    not_named: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {"high_risk_ok_rows_by_a": self.ok_total, "named_by_b": len(self.named), "not_named_by_b": self.not_named}


def id_token_regex(schema: Schema) -> re.Pattern[str]:
    """A token that looks like a graph id: any node type's prefix (from schema.yaml), a dash, then id
    characters ending in a letter, digit or underscore (so a trailing full stop is not part of it)."""
    prefixes = set()
    for node_type in schema.node_types.values():
        match = re.match(r"\^([A-Z]+)-", node_type.id_regex.pattern)
        if match:
            prefixes.add(match.group(1))
    if not prefixes:
        raise SchemaError("no node type id pattern starts with an uppercase prefix")
    alternatives = "|".join(sorted(prefixes, key=len, reverse=True))
    return re.compile(rf"(?<![\w-])(?:{alternatives})-[A-Za-z0-9_.-]*[A-Za-z0-9_]")


def _read_json(path: Path, what: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise GateInputError(f"cannot read {what} {path}: {exc}") from None
    except json.JSONDecodeError as exc:
        raise GateInputError(f"{what} {path} is not valid JSON: {exc}") from None


def load_manifest(path: Path) -> dict[str, Any]:
    manifest = _read_json(path, "manifest")
    try:
        ids = [item["id"] for item in manifest["items"]]
        _ = (manifest["fr"], manifest["db"]["path"], manifest["db"]["sha256"], manifest["prd"]["path"],
             manifest["prd"]["sha256"], int(manifest["prd"]["lines"]))
        _ = [item["kind"] for item in manifest["items"]]
    except (KeyError, TypeError, ValueError) as exc:
        raise GateInputError(f"manifest {path} is missing a required key or has a wrong type: {exc}") from None
    if len(set(ids)) != len(ids):
        raise GateInputError(f"manifest {path} repeats an item id")
    return manifest


def load_defects(path: Path, manifest: dict[str, Any]) -> list[dict[str, Any]]:
    """Read the sealed planted-defect file and check every defect can be matched to manifest items."""
    data = _read_json(path, "planted-defect file")
    if not isinstance(data, dict) or data.get("fr") != manifest["fr"]:
        raise GateInputError(f"planted-defect file {path} is not for {manifest['fr']}")
    defects = data.get("defects")
    if not isinstance(defects, list) or not defects:
        raise GateInputError(f"planted-defect file {path} has no defects list")
    known = {item["id"] for item in manifest["items"]}
    seen: set[str] = set()
    for index, defect in enumerate(defects):
        where = f"planted-defect file {path} defects[{index}]"
        if not isinstance(defect, dict) or not isinstance(defect.get("id"), str) or not defect["id"]:
            raise GateInputError(f"{where}: needs a non-empty string id")
        if defect["id"] in seen:
            raise GateInputError(f"{where}: repeats id {defect['id']}")
        seen.add(defect["id"])
        if defect.get("kind") not in DEFECT_KINDS:
            raise GateInputError(f"{where}: kind must be one of {list(DEFECT_KINDS)}")
        items = defect.get("items")
        if not isinstance(items, list) or not items or not all(isinstance(i, str) for i in items):
            raise GateInputError(f"{where}: items must be a non-empty list of manifest item ids")
        unknown = [i for i in items if i not in known]
        if unknown:
            raise GateInputError(f"{where}: items not in the manifest: {unknown}")
    return defects


def split_sections(lines: list[str]) -> dict[str, tuple[int, list[str]]]:
    """Level-2 sections by lowercased heading, outside fenced code: heading line number and body lines.
    A repeated heading keeps its first occurrence."""
    sections: dict[str, tuple[int, list[str]]] = {}
    current: list[str] | None = None
    in_fence = False
    for number, line in enumerate(lines, start=1):
        if _FENCE.match(line):
            in_fence = not in_fence
        match = None if in_fence else _H2.match(line)
        if match:
            title = match.group(1).strip().lower()
            current = [] if title not in sections else None
            if current is not None:
                sections[title] = (number, current)
            continue
        if current is not None:
            current.append(line)
    return sections


def _cells(line: str) -> list[str]:
    text = line.strip()
    if text.startswith("|"):
        text = text[1:]
    if text.endswith("|"):
        text = text[:-1]
    return [cell.strip() for cell in text.split("|")]


def parse_verdict_rows(start: int, body: list[str], failures: list[str]) -> list[Row]:
    """Rows of the first table in the Verdicts section. Column order is read from its header."""
    rows: list[Row] = []
    columns: dict[str, int] | None = None
    for offset, line in enumerate(body, start=1):
        if not line.strip().startswith("|"):
            if columns is not None and rows and not line.strip():
                break
            continue
        cells = _cells(line)
        if columns is None:
            names = [c.lower() for c in cells]
            missing = [c for c in TABLE_COLUMNS if c not in names]
            if missing:
                failures.append(f"Verdicts table header (report line {start + offset}) lacks columns {missing}")
                return []
            columns = {c: names.index(c) for c in TABLE_COLUMNS}
            continue
        if _SEPARATOR.match(line.strip()):
            continue
        value = {name: cells[i] if i < len(cells) else "" for name, i in columns.items()}
        rows.append(Row(start + offset, value["item"].strip("`"), value["verdict"].strip("`*").lower(), value["evidence"], value["note"]))
    if columns is None:
        failures.append("Verdicts section has no table")
    return rows


class CitationChecker:
    def __init__(self, conn: sqlite3.Connection, schema: Schema, prd_lines: int) -> None:
        self.conn = conn
        self.id_token = id_token_regex(schema)
        self.prd_lines = prd_lines

    def references(self, text: str) -> list[str]:
        """Every id token and PRD line reference in the text, in order."""
        found = [m.group(0) for m in self.id_token.finditer(text)]
        found += [m.group(0).lower() for m in _PRD_REF.finditer(text)]
        return found

    def problems(self, text: str) -> list[str]:
        out = []
        for token in sorted({m.group(0) for m in self.id_token.finditer(text)}):
            if self.conn.execute("SELECT 1 FROM nodes WHERE id = ?", (token,)).fetchone() is None:
                out.append(f"cited id {token} is not in the review graph")
        for m in _PRD_REF.finditer(text):
            first = int(m.group(1))
            last = int(m.group(2) or first)
            if not 1 <= first <= last <= self.prd_lines:
                out.append(f"cited PRD line {m.group(0)} is outside 1-{self.prd_lines}")
        return out


def check_report(report_text: str, manifest: dict[str, Any], defects: list[dict[str, Any]],
                 checker: CitationChecker) -> GateResult:
    result = GateResult()
    failures = result.failures
    lines = report_text.splitlines()
    sections = split_sections(lines)

    rows: list[Row] = []
    if SECTION_VERDICTS in sections:
        start, body = sections[SECTION_VERDICTS]
        rows = parse_verdict_rows(start, body, failures)
    else:
        failures.append("no '## Verdicts' section")

    manifest_ids = [item["id"] for item in manifest["items"]]
    known = set(manifest_ids)
    counted: dict[str, Row] = {}  # rows that count: known item, valid verdict, evidence present
    first_line: dict[str, int] = {}
    for row in rows:
        where = f"report line {row.line} ({row.item or 'no item'})"
        if row.item not in known:
            failures.append(f"{where}: item is not in the manifest")
            continue
        if row.item in first_line:
            failures.append(f"{where}: second row for this item (first at report line {first_line[row.item]})")
            continue
        first_line[row.item] = row.line
        if row.verdict not in VERDICTS:
            failures.append(f"{where}: verdict {row.verdict!r} is not one of OK, finding, cannot verify")
            continue
        for problem in checker.problems(row.evidence):
            failures.append(f"{where}: {problem}")
        if row.verdict == "cannot verify":
            if not row.note.strip():
                failures.append(f"{where}: cannot verify without a reason in Note; counts as missing")
                continue
        elif len(set(checker.references(row.evidence))) < MIN_CITATIONS:
            failures.append(f"{where}: {row.verdict.upper() if row.verdict == 'ok' else row.verdict} without evidence "
                            f"(cite at least {MIN_CITATIONS} ids or PRD lines compared); counts as missing")
            continue
        counted[row.item] = row
    for item_id in manifest_ids:
        if item_id not in first_line:
            failures.append(f"missing row for manifest item {item_id}")

    flows = [item["node_id"] for item in manifest["items"] if item["kind"] == KIND_FLOW]
    if SECTION_SCENARIOS in sections:
        start, body = sections[SECTION_SCENARIOS]
        walked = {m.group(1) for line in body if (m := _SCENARIO.match(line))}
        for problem in checker.problems("\n".join(body)):
            failures.append(f"Scenarios section: {problem}")
        for flow in flows:
            if flow not in walked:
                failures.append(f"no '### Scenario {flow}' walkthrough for manifest flow {flow}")
    elif flows:
        failures.append("no '## Scenarios' section, but the manifest lists flows")

    if SECTION_NOT_CHECKED not in sections:
        failures.append("no '## Not checked or could not verify' section")
    else:
        text = " ".join(line.strip() for line in sections[SECTION_NOT_CHECKED][1]).strip()
        if not text:
            failures.append("'Not checked or could not verify' section is empty")
        elif _BARE_NONE.fullmatch(text):
            failures.append("'Not checked or could not verify' says none without a sentence saying why")

    finding_items = {row.item for row in counted.values() if row.verdict == "finding"}
    result.defects_total = len(defects)
    for defect in defects:
        if finding_items.intersection(defect["items"]):
            result.defects_found.append(defect["id"])
        else:
            result.defects_missed.append(defect["id"])
            failures.append(f"planted defect {defect['id']} missed: no finding row on {', '.join(defect['items'])}")
    return result


def is_high_risk(item: dict[str, Any]) -> bool:
    """Reviewer B's attack classes (checklist, "High-risk items for reviewer B")."""
    return item["kind"] in HIGH_RISK_KINDS or item.get("type") in HIGH_RISK_NODE_TYPES


def attacked_items(start: int, body: list[str]) -> set[str]:
    """Item ids in the Item column of the first table of B's Attacks section."""
    column: int | None = None
    named: set[str] = set()
    for line in body:
        if not line.strip().startswith("|"):
            if column is not None and named and not line.strip():
                break
            continue
        cells = _cells(line)
        if column is None:
            names = [c.lower() for c in cells]
            if "item" not in names:
                raise GateInputError(f"B's Attacks table header (report line {start}) has no Item column")
            column = names.index("item")
            continue
        if _SEPARATOR.match(line.strip()):
            continue
        if column < len(cells) and cells[column].strip("`* "):
            named.add(cells[column].strip("`* "))
    if column is None:
        raise GateInputError("B's Attacks section has no table")
    return named


def run_b_coverage(manifest_path: Path, a_report_path: Path, b_report_path: Path) -> CoverageResult:
    manifest = load_manifest(manifest_path)
    texts = {}
    for what, path in (("A report", a_report_path), ("B report", b_report_path)):
        try:
            texts[what] = path.read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            raise GateInputError(f"cannot read {what} {path}: {exc}") from None
    a_sections = split_sections(texts["A report"])
    if SECTION_VERDICTS not in a_sections:
        raise GateInputError(f"A report {a_report_path} has no '## Verdicts' section")
    problems: list[str] = []
    rows = parse_verdict_rows(*a_sections[SECTION_VERDICTS], problems)
    if problems:
        raise GateInputError(f"A report {a_report_path}: {problems[0]}")
    b_sections = split_sections(texts["B report"])
    if SECTION_ATTACKS not in b_sections:
        raise GateInputError(f"B report {b_report_path} has no '## Attacks' section")
    named = attacked_items(*b_sections[SECTION_ATTACKS])

    high_risk = {item["id"] for item in manifest["items"] if is_high_risk(item)}
    ok_rows: list[str] = []  # first row per item only, as in the gate
    seen: set[str] = set()
    for row in rows:
        if row.item in seen:
            continue
        seen.add(row.item)
        if row.item in high_risk and row.verdict == "ok":
            ok_rows.append(row.item)
    result = CoverageResult(ok_total=len(ok_rows))
    for item_id in ok_rows:
        (result.named if item_id in named else result.not_named).append(item_id)
    return result


def run_gate(manifest_path: Path, report_path: Path, defects_path: Path, db: str | None = None,
             prd: str | None = None) -> GateResult:
    manifest = load_manifest(manifest_path)
    defects = load_defects(defects_path, manifest)
    db_path = Path(db or manifest["db"]["path"]).resolve()
    prd_path = Path(prd or manifest["prd"]["path"]).resolve()
    for path, expected, what in ((db_path, manifest["db"]["sha256"], "review DB"), (prd_path, manifest["prd"]["sha256"], "review PRD")):
        if not path.is_file():
            raise GateInputError(f"{what} {path} does not exist")
        if file_sha256(path) != expected:
            raise GateInputError(f"{what} {path} changed since the manifest was built (sha256 differs)")
    try:
        report_text = report_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise GateInputError(f"cannot read report {report_path}: {exc}") from None
    schema = load_schema()
    conn = open_db(db_path, schema, read_only=True)
    try:
        return check_report(report_text, manifest, defects, CitationChecker(conn, schema, int(manifest["prd"]["lines"])))
    finally:
        conn.close()


def format_text(result: GateResult) -> str:
    out = [f"Gate: {'PASS' if result.passed else 'VOID'}"]
    out += [f"  - {failure}" for failure in result.failures]
    out.append(f"Planted defects found: {len(result.defects_found)} of {result.defects_total}"
               + (f" (missed: {', '.join(result.defects_missed)})" if result.defects_missed else ""))
    return "\n".join(out)


def format_coverage(result: CoverageResult) -> str:
    out = [f"Reviewer B coverage: {len(result.named)} of {result.ok_total} high-risk OK rows by A named in B's Attacks"]
    if result.not_named:
        out.append("Not named by B:")
        out += [f"  - {item}" for item in result.not_named]
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Mechanical gate for one logic-review report.")
    parser.add_argument("--manifest", required=True, help="manifest JSON from logic_manifest.py")
    parser.add_argument("--report", required=True, help="reviewer A report (Markdown)")
    parser.add_argument("--defects", help="sealed planted-defect JSON (required unless --b-report is given)")
    parser.add_argument("--b-report", help="reviewer B report: print the B coverage count instead of running the gate")
    parser.add_argument("--db", help="review DB (default: the path recorded in the manifest)")
    parser.add_argument("--prd", help="review PRD (default: the path recorded in the manifest)")
    parser.add_argument("--json", action="store_true", help="print the result as JSON")
    args = parser.parse_args(argv)
    if args.b_report:
        try:
            coverage = run_b_coverage(Path(args.manifest), Path(args.report), Path(args.b_report))
        except (GateInputError, OSError) as exc:
            print(f"logic_gate: {exc}", file=sys.stderr)
            return 2
        print(json.dumps(coverage.as_dict(), indent=2, ensure_ascii=False) if args.json else format_coverage(coverage))
        return 0
    if not args.defects:
        parser.error("--defects is required unless --b-report is given")
    try:
        result = run_gate(Path(args.manifest), Path(args.report), Path(args.defects), args.db, args.prd)
    except (GateInputError, SchemaError, FileNotFoundError, sqlite3.Error) as exc:
        print(f"logic_gate: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result.as_dict(), indent=2, ensure_ascii=False) if args.json else format_text(result))
    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main())
