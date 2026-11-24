# FR-010 Logic Review Pass 2 Fixes - 2026-11-23

**Scope**: FR-010 (Treatment Execution and Documentation) only. PRD version 2.13 to 2.14, plus a prepared graph change-set.

## What changed in the PRD

- **Admin case listing (Screen 7)**: a case status filter (default In Progress), a flag filter, a Case Status column and a Flags column. Screen 8 opens from it for a case in any status.
- **Failed completion signal**: the flag shows in the Flags column and on Screen 8, where a Retry Completion Signal button sends it again. Flags clear when the case closes.
- **Early close without a fault (owner decisions 54 and 55)**: the refund comes out of what the patient paid, the provider's share becomes eligible for payout on the decision date after the refund and commission, and there is no waiting window. The system sets Closed Early and signals FR-011. A partly delivered treatment ends with End Treatment and needs no close request.
- **Provider fault while In Progress**: the admin can cancel the booking through FR-006 Screen 11; the treatment record becomes Cancelled and `treatment.cancelled` is emitted (new requirement REQ-010-122). A provider status cascade can also leave the record Closed Early.
- **Check In**: the reasons for a disabled Check In are listed; the patient is notified on early and late Check In.
- **Documentation reminder**: the first reminder defaults to 6 hours, with a range from 1 hour up to the deadline minus 1 hour.
- **Integration 5**: the End Treatment save and the booking move succeed or fail together; a support-required marker raised during the modal rejects the save.
- Removed the "completion milestone" wording; providers see completed and Closed Early treatments read-only.
- New requirements REQ-010-121 and REQ-010-122; REQ-010-115 and REQ-010-116 reworded.

## Graph

Prepared only, not applied: `local-docs/project-requirements/graph/changesets/2026-11-23-fr010-logic-p2-fixes.yaml`. On a scratch copy it applies cleanly and the lint count stays at 27. It restates the stale rule text and titles from the PRD, adds the early-close steps (Closed Early and FR-011 signal, then payout eligible, then the FR-007 payout step) and a retry step, joins the Check In steps that were dead ends, and drops two edges to a step retired earlier.

## Neighbour items (not changed here)

FR-006 Screen 11 wording for the early close and the In Progress cancel, FR-007 payout step wording, FR-011 handling of the Closed Early signal, FR-030 `treatment.cancelled` listing. Tracked in the logic-review ledger.

## Decisions

Owner decisions 54 and 55 in `plans/reports/owner-review-261123-1308-phase-10-defaults-applied.md`.

## Applied

The controller applied the change-set to the live graph on 2026-11-24 (127 change rows, backup `graph/backups/graph-2026-11-23-pre-fr010-logic-p2.db`). Lint count 27, equal to the baseline. `graph.json` re-exported.
