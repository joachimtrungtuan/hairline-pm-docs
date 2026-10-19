# Hairline Test Strategy

**Status:** Active
**Created:** 2026-10-19
**Last Updated:** 2026-10-19
**Owner:** Product / QA lead (Vân Tay Media)

This document defines how testing is organized in `local-docs/testing/`. It is the contract for people, AI agents, and the `manual-test-bug-sync` skill. Hub navigation lives in [README.md](README.md).

---

## 1. Testing Tracks

| Track | Purpose | Owner | Location |
|---|---|---|---|
| Manual testing | Usability issues (top priority) and functional bugs, run by a human tester or the tester's AI agent against a live environment | Product / QA, external tester | `manual/` |
| Automated web E2E | Deterministic Playwright regression of dashboard functions and flows | Product / QA | `automated/web-e2e/` (governed by its `TESTING-CONSTITUTION.md`) |
| Automated API | Single-endpoint and multi-step API flow checks run by the `api-testing` and `api-flow-testing` skills | Product / QA | `automated/api/` |
| Automated Android | Emulator journeys run by the `android-flow-test` skill (patient mobile app, archived scope) | Product / QA | `automated/android/` |
| Backend unit and integration tests | Code-level tests inside the backend repository | Development team | `main/hairline-backend/` (not managed here) |

Manual and automated tracks are **separate**. They share no identifiers. The only link between them is the source of truth they both test: the user flows and business rules in the FR PRDs (`project-requirements/functional-requirements/frNNN-*/prd.md`).

---

## 2. Manual Testing Structure

```text
manual/phases/<phase-folder>/
└── v<major>.0/                     one folder per major plan version
    ├── plan.md                     copied from templates/manual-phase-plan-template.md
    └── batches/
        └── B<NN>-<module>-<slug>.md copied from templates/manual-batch-template.md
```

- **Phase** follows the release roadmap (`reports/2026-09-06/admin-provider-implementation-status-and-release-roadmap.md`, four-phase table). Phase folders: `phase-1-controlled-commercial-pilot`, `phase-2-clinical-patient-operations`, `phase-3-settlement-partner-growth`, `phase-4-scale-optimization`.
- **Batch** = one module slice in that phase (for example PR-01 or A-02). The phase plan defines the end-to-end run order across batches.
- **Batch file is the living record.** It holds the case definitions and the latest results. Retests overwrite the result columns in place; git keeps the history. There are no separate run copies.
- **Templates are never filled in place.** Every new plan or batch starts as a copy of a file in `templates/`.

---

## 3. Versioning

| Change | Action |
|---|---|
| Scope or flow change: functions added, removed, or substantially changed in the phase | Create a new major version folder (`v1.0` → `v2.0`). Copy forward unchanged cases with the same IDs. The old folder is frozen and keeps its results. |
| Small change: wording, steps, data, expected-result clarification | Edit in place. Bump the minor version in `plan.md` (`1.0` → `1.1`) and add a change-log row. |
| A single case's steps, preconditions, data, or expected result change | Bump that case's revision (`r1` → `r2`) and add a row to the batch's case change log. |

Results, notes, and bug statuses never bump a version or revision.

---

## 4. Manual Test Case Identifier

Format: `<MODULE><NN>-FR<NNN>-<SEQ> r<REV>`; example `PR01-FR002-03 r1`.

| Part | Meaning |
|---|---|
| `PR01` | Module code without hyphen (`P01`–`P07`, `PR01`–`PR07`, `A01`–`A10`, `S01`–`S06`) |
| `FR002` | Primary FR under test. Other FRs touched are cited in the **PRD flow ref** column |
| `03` | Two-digit sequence counting cases for that module and FR pair, starting at `01` |
| `r1` | Case revision |

Rules: the base ID (without revision) never changes and is never reused, including after a case is retired. A retired case stays in its table with Result `Retired` and a note naming the replacement.

---

## 5. Recorded Values

**Result** (filled by the tester):

| Value | Meaning |
|---|---|
| `Not tested` | Default; not run yet |
| `Pass` | Every expected result observed |
| `Fail` | At least one expected result not observed, or a blocking usability problem |
| `Blocked` | Could not run; a precondition, environment, or dependency failed (state the reason in Notes) |
| `Retired` | Case no longer applies in this version (set only by the plan owner) |

**Bug status** (one per case row):

| Value | Meaning | Bug ID required |
|---|---|---|
| `—` | No bug | No |
| `Found` | Bug observed, not yet logged in Plane | No |
| `Logged` | Logged in Plane | Yes |
| `Fixed - retest` | Development marked fixed; awaiting retest | Yes |
| `Closed` | Retest passed | Yes |
| `Reopened` | Retest failed; same Plane ID reused | Yes |

**Notes** carry usability observations and any other observation. Write what the user experienced, where, and why it hurts (for example: "No loading indicator after clicking Send Invite; clicked twice and two invites were created").

**Evidence** is a screenshot or recording file name or link. **Last tested** is `YYYY-MM-DD`.

---

## 6. Test Data and Accounts

- Batch files reference accounts by placeholder only, for example `{V1}` or `{A1}`. Placeholders map to the row IDs in `test-data/credentials/` (`A#` admin, `S#` provider staff, `V#` provider, `P#` patient).
- Credentials are internal. They are sent to the external tester privately and are never written into batch files or tester deliverables.
- Each batch defines its own data sets (`DS-<MODULE><NN>-<NN>`, for example `DS-PR01-02`) in its **Test Data Sets** section. Data sets are designed from PRD business rules: valid values, boundaries, and invalid values.

---

## 7. Tester Workflow

1. Receive the phase `plan.md`, the batch files to run, and credentials (privately).
2. Fill **Tester** and **Build tested** in each batch's Batch Control, then follow the plan's run order. In case rows, fill only: **Actual result / data**, **Result**, **Notes**, **Evidence** (files named `<case ID>-<n>`, e.g. `PR02-FR004-03-1.png`), **Bug status** (`Found` when a bug is seen), **Last tested**. The team owns **Bug ID** and every later Bug status.
3. Do not change IDs (including the revision suffix), steps, expected results, or table structure. Questions or proposed case changes go in Notes.
4. Return the filled batch files. They are merged back into the hub by the `manual-test-bug-sync` skill, which validates IDs, columns, and allowed values. Never paste results into the hub by hand.

---

## 8. Bug Lifecycle

Fail rows with `Bug status = Found` are logged in Plane (`create-bug-tasks` and `plane-api-commands` skills, orchestrated by `manual-test-bug-sync`). The Plane ID is written back and the status set to `Logged`. When Plane shows the issue resolved, the status becomes `Fixed - retest`, and the case is listed for retest. Retest outcomes set `Closed` or `Reopened`.

---

## 9. Results Location

| Output | Location |
|---|---|
| Manual results | In the batch files themselves |
| Web E2E results | `automated/web-e2e/results/` (SQLite and artifacts; see that folder's README) |
| API and Android skill reports | `results/YYYY-MM-DD/` |
| Pre-2026-10-19 plans and reports | `archive/` (unchanged; see `archive/README.md`) |
