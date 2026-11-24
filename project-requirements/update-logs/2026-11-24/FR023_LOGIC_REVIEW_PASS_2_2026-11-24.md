# FR-023 Logic Review Pass 2 (2026-11-24)

**Scope**: FR-023 Data Retention and Compliance, PRD v1.8 to v1.9, plus a prepared graph change-set that is **not applied yet**. This was the last review pass.
**Type**: Major update (account-deletion lifecycle rules revised: open requests, blocked requests, outcome notice, cancellation gate, passport exception).
**Source of findings**: `plans/reports/tester-261124-fr023-logic-p2.md` (10 findings). Fixer report: `plans/reports/docs-manager-261124-fr023-logic-p2-fixes.md`.

## Files changed

- `functional-requirements/fr023-data-retention-compliance/prd.md` (v1.9).
- NEW `graph/changesets/2026-11-24-fr023-logic-p2-fixes.yaml` (prepared, not applied; `write.py` has not been run).

## What changed in the PRD

- **Open requests**: a request is open in any status before Fulfilled or Denied. The queue shows an overdue open request (Pending Admin Review, Verification Required or In Progress), and the system warns the Admins 7 calendar days before the deadline. Deny is not available once the request is In Progress, because the inquiry is already cancelled.
- **Blocked requests**: the system clears the blocked mark when the obligation ends or an approval check passes, and notifies the Admins that the request can be approved (FR-016 REQ-016-067). An Admin may deny a blocked request. The expected timeline is the obligation end date, or "after the obligation completes".
- **Obligation list**: an inquiry that is Completed no longer counts; the list says which items FR-001 and FR-003 block at submission, and that the full list is checked at approval.
- **Outcome notice**: sent to the contact address captured at approval, before anonymisation, and kept only until delivered.
- **Refresh at approval**: a refreshed classification that differs from the one the Admin reviewed returns the request to review with the jurisdiction flag set.
- **Passport data**: the passport number and passport photo are erased at an approved deletion, a named exception to the no-physical-removal rule (FR-008 REQ-008-069). Other travel data is anonymised in place.
- **Record-type mapping**: rows added for treatment documentation and photos, aftercare data, questionnaire answers, discount records, travel records, and credentials, devices and sessions.
- **Cancellation gate**: anonymisation starts only after the FR-003 cancellation and its provider notices complete; a failed cancellation keeps the request In Progress, shows it in the queue and is retried.

## Prepared graph change-set (not applied)

Adds 3 steps, updates 17 nodes and moves 5 edges (remove and add), with the deletion-requested stage gaining reads and writes edges. Edges only touch other FRs' nodes (references to REQ-016-067 and REQ-008-069, applies edges to REQ-008-069); no neighbour node is changed. Counts by type are in the fixer report.

## Neighbour rows queued (not changed here)

FR-016, FR-001, FR-003, FR-020 and the system PRD (section "FR-023, pass 2" in `plans/reports/logic-review-ledger.md`).

## Defaults chosen without an owner ruling

Passport number and photo erased at approval (entry 73 in `plans/reports/owner-review-261123-1308-phase-10-defaults-applied.md`); a Completed inquiry does not block a deletion request (controller decision, recorded under entry 68).
