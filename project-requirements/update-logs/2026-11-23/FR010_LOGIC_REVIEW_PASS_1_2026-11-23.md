# FR-010 Logic Review Pass 1 Fixes - 2026-11-23

**Scope**: FR-010 (Treatment Execution and Documentation) only. PRD version 2.12 to 2.13, plus a prepared graph change-set.

## What changed in the PRD

- **Early close of an In Progress case without a fault**: the admin closes it on FR-006 Screen 11; the treatment record gets a new Closed Early status that stops reminders and the Overdue Documentation flag. The provider's close request and the interrupted-treatment path now lead to that decision (Alternative Flows B3 and B4; Rule 17).
- **End Treatment gate and deadline**: at least one day must be finished, and the button stays off while the case is on hold. The documentation deadline and first reminder run from the moment the gate is first met, not from Check In.
- **Completion handoff**: saving End Treatment marks the treatment Completed, FR-006 moves the booking to Aftercare in that step whether or not the FR-011 signal arrives, and the FR-007 confirmation window starts (Integration 5). A failed FR-011 signal shows as a dashboard flag and is retried.
- **One Check In rule**: appointment timezone, no Defaulted installment, no support-required marker, one case In Progress per patient, generic reason shown to the provider, and a late Check In prompt after the appointment date (Alternative Flow A3).
- **Provider fault**: an admin may record a provider fault from Screen 8 without the provider withdrawing; the support-required marker blocks documentation and every End Treatment, the admin button included.
- **Plan details lock at the end of the treatment** (Screen 9 and Rule 8); the actual graft count stays the correction path.
- **Admin notices are dashboard flags**, not FR-030 events; Integration 3 uses the FR-030 event names.
- **No-show**: no fixed waiting time; the 2-hour wording is removed.
- Wording fixes: the A1 No branch, "FR-010 Screen 9" wording, Need caution/attention as a final status.
- New requirements REQ-010-115 to REQ-010-120.

## Graph

Prepared only, not applied: `local-docs/project-requirements/graph/changesets/2026-11-23-fr010-logic-p1-fixes.yaml`. On a scratch copy it applies cleanly and the lint count stays at 27. The two Steps that led to the FR-006 Cancel Booking step now lead to the FR-006 Screen 11 step.

## Neighbour items (not changed here)

FR-006 Screen 11 and its provider-fault trigger wording, FR-016 Cancel Booking button, FR-007B REQ-007B-104, FR-011 status-change wording. Tracked in the logic-review ledger.

## Decisions

Owner decisions 46 to 53 in `plans/reports/owner-review-261123-1308-phase-10-defaults-applied.md`.

## Applied

The controller applied the change-set to the live graph on 2026-11-23 (169 change rows, backup `graph/backups/graph-2026-11-23-pre-fr010-logic-p1.db`). Lint count 27, equal to the baseline. `graph.json` re-exported.
