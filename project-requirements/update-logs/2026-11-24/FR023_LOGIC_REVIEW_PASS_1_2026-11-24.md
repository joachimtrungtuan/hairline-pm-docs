# FR-023 Logic Review Pass 1 (2026-11-24)

**Scope**: FR-023 Data Retention and Compliance, PRD v1.7 to v1.8, plus a prepared graph change-set that is **not applied yet**.
**Type**: Major update (substantially revised PRD; the account-deletion lifecycle, the status model and the stage placement changed).
**Source of findings**: `plans/reports/tester-261124-fr023-logic-p1.md` (16 findings). Fixer report: `plans/reports/docs-manager-261124-fr023-logic-p1-fixes.md`.

## Files changed

- `functional-requirements/fr023-data-retention-compliance/prd.md` (v1.8).
- NEW `graph/changesets/2026-11-24-fr023-logic-p1-fixes.yaml` (prepared, not applied; `write.py` has not been run).

## What changed in the PRD

- **Approval cancels the open inquiry**: at admin approval, before anything is anonymised, the system cancels the patient's open inquiry through FR-003. Nothing is cancelled at submission, on a denial or while approval is blocked. Deletion request submission stays blocked while an inquiry is at Accepted or later. REQ-023-003 and REQ-023-040 now also cover inquiries cancelled by the system at approval (new REQ-023-042).
- **Nothing is physically removed**: every category is anonymised or archived in place; scan media belong to Medical Records, not Media. The protected categories are Medical Records, Financial Records and Account Profile, and the Admin confirms them on every approval (the old exclusion alternative flow is merged into the main flow).
- **Record-type mapping**: reviews, messages and support cases are Communications (anonymised); inquiry and scans are Medical Records; quote, acceptance event, booking and payment are Financial Records (new REQ-023-044 and a mapping table).
- **Denied outcome**: new status, step, patient notice and a required reason, matching FR-016 REQ-016-173 (new REQ-023-043).
- **Obligation block**: an active obligation blocks approval; the request stays Pending Admin Review marked blocked by obligation and the patient is told the expected timeline. The 30-day clock never pauses; a breach while blocked is shown but excused. FR-023 owns the one obligation list.
- **Verification Required** stays open until an Admin denies it with a reason; there is no auto-close. The Admin decides "insufficient proof" during review, and the DSR queue shows an overdue open request after the deadline.
- **Status lifecycle** (new REQ-023-046): every status has a step that sets it; the system sets Fulfilled at the single outcome notice and FR-016 owns the certificate.
- **Retention**: default 10 years with a floor of 10; a jurisdiction override may only extend, and "stricter" means longer; the review flag is a field of the request (new REQ-023-045).
- **Out of scope**: patient data export (data portability) at launch.
- Entry points, the audit-log references, stage placement of steps and rules, and the notification wording were aligned with the above.

## Prepared graph change-set (not applied)

Adds 6 steps, 2 flows, 5 rules (REQ-023-042 to 046), 2 events and 3 fields with 5 enum values; reworks the main path; retires the old exclusion flow and its second notice step. One hand-off edge goes from the new cancellation step to FR-003's STP-003-085 (an edge only; no FR-003 node is changed). Counts by type are in the fixer report.

## Neighbour rows queued (not changed here)

FR-001, FR-016, FR-003 and the system PRD each have queued rows in `plans/reports/logic-review-ledger.md` (section "FR-023, pass 1").

## Defaults chosen without an owner ruling

Seven calendar days for the deadline-approaching notice, no new patient restriction while a request is pending, resubmission allowed after a denial, Fulfilled set by the system, and the mapping of quote, acceptance event, booking and payment to Financial Records. They are listed in `plans/reports/owner-review-261123-1308-phase-10-defaults-applied.md` (entries 67 to 72 for the owner rulings).
