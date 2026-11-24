# FR-004 Logic Review Pass 1 - Update Log

**Date**: 2026-11-24
**Scope**: FR-004 Quote Submission & Management PRD v4.3 and a prepared graph change-set
**Type**: Major update (structural rule changes, new requirement rules, new flows and steps)

## Documents changed

- `functional-requirements/fr004-quote-submission/prd.md`: v4.2 to v4.3
- Prepared, not applied: `graph/changesets/2026-11-24-fr004-logic-p1-fixes.yaml` (applying it is the controller's step)

## What changed

- **Withdrawal and soft-delete.** A provider withdraws a sent quote before acceptance from the quote detail screen (Screen 3), with an optional reason. A provider soft-deletes drafts only; a sent quote leaves the offered state by withdrawal, by expiry, or through the patient's choice. Withdrawal of an accepted quote is allowed only while the booking is Confirmed, before check-in, with no provider-fault marker, and needs a reason; in every other state the action is hidden and the provider is pointed to contact support.
- **Provider-fault transfer follows FR-006.** The booking keeps its status and slot hold, with the support-required marker, until the admin submits the replacement on FR-006 Screen 10. Screen 8 opens for a pending or closed fault (booking Accepted, Confirmed, or Cancelled with the marker) until a replacement acceptance is recorded for the transfer. The original acceptance stays the active one until then.
- **New rules.** REQ-004-109 freezes the accepted quote while the marker is on (the replacement quote is the only quote write; admin notes stay allowed). REQ-004-110 defines an active acceptance once. REQ-004-111 cancels a replacement draft without notice when an admin closes or cancels the inquiry.
- **Replacement quote.** No expiry, no expiring-soon notice, stays a draft that the patient does not see until the admin records the acceptance; at that moment the first-send time and the currency are captured. The case ends by Close inquiry (FR-006 Screen 6) or the FR-006 cancel flow, not by "cancel the inquiry and booking".
- **Promotions.** Archiving a quote releases its promotion reservation. Restoring an expired quote (and an archived sent quote returning to sent) re-checks the promotion and takes a new reservation; the restore is blocked with a message when the limit is used up or the promotion has ended. Owner business default, accepted on 2026-11-23.
- **Restore targets.** Archived draft returns to draft with the 7-day count restarted; archived sent quote returns to sent if its original expiry has not passed, otherwise to expired. Restore is blocked with an active acceptance or the marker.
- **Draft retention.** The 7 days count from the last edit and are a fixed platform rule with no setting.
- **Citations.** The identity rule cites the platform-wide rule (REQ-SYS-001); the restore notice cites its FR-030 catalogue entry (REQ-030-218); the not-selected notice names the `quote.accepted` outcome value (REQ-030-038).
- **Graph change-set.** Updates 19 rule statements, adds 3 rules, 6 flows and 13 steps, updates screens, three quote fields and two events, and removes two edges from FR-004 steps to retired steps.

## Open items for neighbouring FRs (not edited here)

- FR-006 Alternative Flow B5, Screen 10 and REQ-006-018, and FR-005 REQ-005-045, still say an unaccepted replacement quote expires and FR-004 sends `quote.expired`.
- FR-005 (replacement-quote and withdrawal text), FR-003 REQ-003-013, FR-019 reservation release on archive, and FR-030 REQ-030-128 producer list need to match.
- The FR-005 and FR-010 mirrors of the pending-fault block on edits of the accepted quote.
- STP-003-046 still has a `next` edge to the retired step STP-004-002.

## Applied

The controller applied the change-set to the live graph on 2026-11-24 (274 change rows, backup `graph/backups/graph-2026-11-24-pre-fr004-logic-p1.db`). The lint count is 27, the same as the baseline. `graph.json` was re-exported.
