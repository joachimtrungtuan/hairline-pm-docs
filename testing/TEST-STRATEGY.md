# Hairline Test Strategy

**Status:** Active
**Created:** 2026-10-19
**Last Updated:** 2026-10-20
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
manual/v<N>/                              one folder per product plan version (product-plans/v<N>/)
└── phases/<phase-folder>/                one folder per phase of that plan version
    ├── test-guide.md                     copied from templates/manual-test-guide-template.md
    ├── batches/                          scaffolds: case definitions only, never filled in
    │   └── B<NN>-<module>-<slug>.md      copied from templates/manual-batch-template.md
    └── results/
        └── run-<NN>-<YYYY-MM-DD>/        one folder per test run
            ├── B<NN>-<module>-<slug>.md  result copy of each scaffold
            └── summary.md                run Progress Summary, from templates/manual-run-summary-template.md
```

- **Plan version** is the product plan's version folder: `product-plans/v<N>/plan.md` defines the phases, their scope, and their exit gates. Each plan version has its own phase set, so phase folders are never shared across versions. The testing folder holds no plan copy; the test guide links to the product plan.
- **Phase folder** names match `product-plans/v<N>/phases/<phase-folder>/`. Current version `v2` (September 2026 roadmap): `phase-1-controlled-commercial-pilot`, `phase-2-clinical-patient-operations`, `phase-3-settlement-partner-growth`, `phase-4-scale-optimization`.
- **Test guide** holds only test content: entry and exit criteria, environment and accounts, team setup, and the end-to-end run order across batches.
- **Batch** = one module slice in that phase (for example PR-01 or A-02). The file in `batches/` is the **scaffold**: case definitions only. Nobody fills it in; it changes only when the cases change (§3).
- **Run** = one test pass on a phase: a full pass, or a retest of the cases listed by the retest list. Every run creates a new folder `results/run-<NN>-<YYYY-MM-DD>/` (`NN` counts runs in the phase from `01`; the date is the day the run starts) with one result copy per scaffold and a `summary.md`. The `manual-test-bug-sync` skill creates it (`new-run`): it copies the current scaffolds, and carries each case's **Bug ID** and **Bug status** forward from the previous run so the bug lifecycle continues. Results start empty.
- **Earlier runs are frozen.** Once a newer run exists, older run folders are history: no merges or bug-status writes go there. The latest run of each phase is the working record.
- **Templates are never filled in place.** Every new guide, scaffold, or run summary starts as a copy of a file in `templates/`.
- **Exit criteria are uniform.** Every test guide uses the exit-criteria wording of `templates/manual-test-guide-template.md` §2, plus the exit gate items of that phase in the product plan. No phase adds stricter generic criteria. They are checked against the latest full run together with any later retest runs.
- **Evidence files** live in the file-sharing service the tester chooses, not in the repository; result rows hold only the links. See §5.
- **One tester per batch run.** A result copy is run by one tester at a time; parallel testers take different batches.

---

## 3. Versioning

Three levels, each protecting copies already in a tester's hands:

| Level | Where it is recorded | When it changes |
|---|---|---|
| Plan version (`v1`, `v2`, ...) | Product plan folder `product-plans/v<N>/`; batch control **Plan / phase** (for example `v2 / Phase 1`) | A new product plan version. Create `manual/v<N>/` with that version's phase set; copy forward the cases that still apply with the same base IDs. The previous version folder is frozen with its runs. |
| Batch version (`1.0`, `1.1`, `2.0`) | Batch control **Batch version** in the scaffold; test guide Change Log | Change to an issued scaffold (see below). Each batch has its own version. |
| Case revision (`r1`, `r2`) | Case ID suffix; Case Change Log | A case's steps, preconditions, test data, or expected result change. |

**Before a scaffold is first used in a run**, edit it in place with no version or revision bump; new cases still get a `Created` row in the Case Change Log. After that:

| Change | Action |
|---|---|
| Scope or flow change inside the same plan version: functions added, removed, or substantially changed for the batch | Bump the batch major version (`1.x` → `2.0`). Retire cases that no longer apply and add new ones. Add a test guide Change Log row. |
| Small change: wording, steps, data, expected-result clarification | Bump the batch minor version (`1.0` → `1.1`) and add a test guide Change Log row naming the batch. |
| The change alters a case's steps, preconditions, test data, or expected result | In addition to the batch bump, bump that case's revision and add a Case Change Log row. A batch bump that changes no case (for example Flow Overview wording) bumps no revision. |

Results, notes, and bug statuses never bump a version or revision. Scaffold changes reach testers through the next run, because `new-run` copies the current scaffolds. A returned copy whose batch major version differs from its run's result file is rejected; one with an older minor version or older case revisions is a stale copy: its results for changed cases are not merged and the tester reruns the current revision.

Copies made before 2026-10-20 carry the single row **Phase / plan version** (`Phase 1 / v1.0`). They are read as plan `v2`, batch version `1.0`.

---

## 4. Manual Test Case Identifier

Format: `<MODULE><NN>-FR<NNN>-<SEQ> r<REV>`; example `PR01-FR002-03 r1`.

| Part | Meaning |
|---|---|
| `PR01` | Module code without hyphen (`P01`–`P07`, `PR01`–`PR07`, `A01`–`A10`, `S01`–`S06`); no letter suffix such as `A09a` |
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

**Open bug** means Bug status `Found`, `Logged`, `Fixed - retest`, or `Reopened`, plus a `Fail` row whose Bug status is still `Closed` (a regression not yet reopened). `Fixed - retest` stays open until a retest passes. The Batch Summary and run summary Progress Summary **Open bugs** columns and every phase's exit criteria use this definition.

**Notes** carry usability observations and any other observation. Write what the user experienced, where, and why it hurts (for example: "No loading indicator after clicking Send Invite; clicked twice and two invites were created").

**Evidence** lists screenshot or recording file names, or links, separated by `, `. Rules:

- **Name:** `<case base ID>-<YYYYMMDD>-<n>.<ext>`, where the date is the run date (the row's Last tested) and `n` counts files for that case on that date, for example `PR02-FR004-03-20261019-1.png`. A retest has a new date, so its files never overwrite earlier evidence.
- **Storage:** the tester uploads every screenshot and recording to any file-sharing service they choose, makes each link openable by the team without a separate request, and writes only the links in Evidence. No evidence file is committed to the repository or sent with the batch. A retest happens in a later run, so earlier links stay in the earlier run's result file; the tester keeps those files available.
- **Bugs:** the Plane bug lists the evidence links.

**Last tested** is `YYYY-MM-DD`.

**Row format:** each case is one table row on one physical line. Use `<br>` for a line break inside a cell (`<br/>` and `<br />` are accepted as the same); a real line break splits the row and the file is rejected. Never type the vertical-bar character inside a cell.

---

## 6. Test Data and Accounts

- Batch files reference accounts by placeholder only, for example `{V1}` or `{A1}`. Account placeholders map to the row IDs in `test-data/credentials/`: `A#` admin, `S#` provider staff, `V#` provider, `P#` patient, `AF#` affiliate.
- Mailbox placeholders name inboxes the team controls for emails sent during a test, not login accounts: `{Invite mailbox n}` (staff and team invitations), `{New provider mailbox n}` (provider onboarding and activation), `{Admin invite mailbox}` (admin team invitations).
- `test-data/placeholder-registry.md` is the single list of every placeholder in use, with its role, phases, and the credentials row or mailbox behind it. Add a placeholder there before using it in a test guide or batch; never create a second placeholder for the same account or role.
- Credentials are internal. They are sent to the external tester privately and are never written into batch files or tester deliverables.
- Each batch defines its own data sets (`DS-<MODULE><NN>-<NN>`, for example `DS-PR01-02`) in its **Test Data Sets** section. Data sets are designed from PRD business rules: valid values, boundaries, and invalid values.

---

## 7. Tester Workflow

1. Receive the phase `test-guide.md`, the result copies for the run (from `results/run-<NN>-<YYYY-MM-DD>/`), and credentials (privately). Never work on the scaffolds in `batches/`.
2. Run each batch alone: one tester per result copy at a time. In its Batch Control, fill **Tester** (`Name (YYYY-MM-DD)`) and **Build tested** (`<build> (YYYY-MM-DD)`); if the tester or build changes during the run, add the new entry after `; ` and never delete earlier entries. Then follow the guide's run order (for a retest run, only the listed cases). In case rows, fill only: **Actual result / data**, **Result**, **Notes**, **Evidence** (named `<case base ID>-<YYYYMMDD>-<n>.<ext>`, see §5), **Bug status** (`Found` when a new bug is seen), **Last tested**. The team owns **Bug ID** and every later Bug status.
3. Do not change IDs (including the revision suffix), steps, expected results, version rows, or table structure. Questions or proposed case changes go in Notes.
4. Return the filled result copies. They are merged into the run's result files by the `manual-test-bug-sync` skill, which validates IDs, columns, versions, and allowed values. Never paste results into the repository by hand.

---

## 8. Bug Lifecycle

Fail rows with `Bug status = Found` are logged in Plane (`create-bug-tasks` and `plane-api-commands` skills, orchestrated by `manual-test-bug-sync`). The Plane ID is written back and the status set to `Logged`. When Plane shows the issue resolved, the status becomes `Fixed - retest`, and the case is listed for retest. Retest outcomes set `Closed` or `Reopened`.

---

## 9. Results Location

| Output | Location |
|---|---|
| Manual results | `manual/v<N>/phases/<phase>/results/run-<NN>-<YYYY-MM-DD>/`: one result file per batch, plus `summary.md` (see §2) |
| Manual evidence files | The tester's chosen file-sharing service; links in each case row's Evidence (see §5) |
| Web E2E results | `automated/web-e2e/results/` (SQLite and artifacts; see that folder's README) |
| Android skill reports and session screenshots (`android-emulator-qa`, `android-flow-test`, `android-flow-register`) | `results/YYYY-MM-DD/` |
| API skill reports (`api-testing`, `api-flow-testing`) | Returned in the conversation; no file is written. Learnings go to the endpoint and flow profiles under `automated/api/` after user confirmation |
| Pre-2026-10-19 plans and reports | `archive/` (unchanged; see `archive/README.md`) |
