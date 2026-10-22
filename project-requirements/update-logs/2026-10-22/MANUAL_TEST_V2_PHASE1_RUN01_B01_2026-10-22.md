# Manual Test v2 Phase 1 Run 01: B01 Results Recorded

**Date:** 2026-10-22
**Type:** Manual test run created and first batch results merged (approved by the user)

## Why

The tester returned the first filled batch of the v2 Phase 1 manual test plan (B01, A-02 Provider Onboarding and Status Management). The results had to be recorded in the run structure from `TEST-STRATEGY.md` without changing the tester's verdicts.

## What Changed

- **New run** `testing/manual/v2/phases/phase-1-controlled-commercial-pilot/results/run-01-2026-10-21/`: created with `manual-test-bug-sync` `new-run --type full`, dated the day testing started. It holds result files for B01 to B06; B02 to B06 are still Not tested.
- **B01 merged** into `run-01-2026-10-21/B01-a02-provider-onboarding.md` through `batch-sync.py merge` (no hand edits):
  - Tester: Khue Dinh (2026-10-21). Build tested: 2026-10-21 build (2026-10-21); no build identifier was given.
  - 23 of 23 cases: 2 Pass (05, 18), 17 Fail (01 to 04, 06 to 08, 12 to 17, 19, 21 to 23), 4 Blocked (09, 10, 11, 20).
  - Bug status stays `—` on all Fail rows; bug logging is a later step.
- **Normalization before merge** (agreed with the user), so the tester copy fits the result-file format:
  - The tester wrote one result per expected-result item. The case Result is Fail if any item failed, else Blocked if any item was blocked, else Pass; the per-item results are kept in Notes.
  - The tester's evidence labels moved to Notes ("Evidence order"); Evidence holds the bare links in the tester's order.
  - Actual result text is unchanged. Last tested is 2026-10-21 on every case.

## Items for Review (verdicts recorded as given)

- 22 and 23: Fail with no Actual result and notes copied from 21; likely not run.
- 05 and 18: Pass although the message wording differs from the expected text (05 "The email has already been taken"; 18 missing permanence warning).
- 02 and 16: some items marked Pass with different wording; 02 did not use the DS-A02-01 data.
- 01: the tile-sum check cannot be verified because the screen has no status tiles.
- Design and PRD gaps the tester raised: "Didn't receive activation email?" link (09 to 11), "Invite Staff Member" against "Add New Staff" (15, 16), reactivation modal (17), deactivate warning (18).
- Likely defects: Super Admin gets "Error / Forbidden" when editing (12 to 14); no leave-wizard confirmation (06); Vietnamese error text in the English UI (07). Tester proposal on character-limit consistency (04).

## Verification

- `validate`: valid, with warnings only (`fail_without_bug_flag` on 17 rows, `fail_without_actual` on 22 and 23, `section_stale` for the older "How to Fill In This File" section, not merged).
- `merge --apply --expect-sha`: 23 updated, 0 skipped; batch summary Total 23, Pass 2, Fail 17, Blocked 4, Not tested 0, Open bugs 0.
- `summary --run`: no further changes needed.

## Triage (2026-10-22, decided by Joachim Trung)

- FR-015 PRD check: Payout Frequency has no preselected value, clinic Contact Email is required, Clinic Name and Search allow up to 200 characters, and Flat Rate Currency is required for Flat Rate. The test expectations match, so these failures are bugs.
- Bug status set to `Found` through `set-bug` on 13 cases for the separate bug-task step: 01, 02, 03, 04, 06, 07, 08, 12, 13, 14, 15, 16, 19. Batch summary now shows 13 open bugs.
- A dated `Triage 2026-10-22` line was added to Notes on 21 cases through `merge` (tester text unchanged): which failure is the bug, what goes to the deferred backlog (01 status tiles, 09 to 11, 17, 18, 21), or why the case is skipped (22, 23 not reliably run; 16 item 6 and 19 items 2 and 3 accepted as recorded; 15 "Add New Staff" naming accepted).
- Untouched: 05 (Pass) and 20 (Blocked on a missing restricted-admin test account).
- Deferred backlog (`deferred-backlog` skill): DEF-001 to DEF-007 added to `deferred-backlog/v01-2026-10-22.md`, one per case (01, 09, 10, 11, 17, 18, 21), reason "Not in the current design; not built in this phase", decided by Joachim Trung on 2026-10-22, revisit trigger none. v01 Delta: new 7, open 7.

## Bug Logging (2026-10-22)

- Bug tasks HAIRL-1553 to HAIRL-1630 were created in Plane under the parent HAIRL-1552 (Phase 1 milestone). The source file is `project-automation/task-creation/2026-10-22/implementation-tasks-2026-10-22-001.md`. The six tester tasks HAIRL-1545 to HAIRL-1550 moved under the new manual testing parent HAIRL-1551.
- `manual-test-bug-sync` `set-bug` set Bug status to `Logged` on 21 cases, with their Plane keys in Bug ID (several keys where a case has FE and BE tasks). Eight rows went from `—` to `Found` first, because `set-bug` does not allow `—` to `Logged` directly. Batch Summary is unchanged: 2 Pass, 17 Fail, 4 Blocked, 21 open bugs.
