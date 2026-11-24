# FR-030 Logic Review, Pass 2 (Final) - 2026-11-24

**Document**: `local-docs/project-requirements/functional-requirements/fr030-notification-rules-config/prd.md`
**Version**: 1.24 to 1.25
**Source review**: `plans/reports/tester-261124-fr030-logic-p2.md`
**Graph change-set**: `local-docs/project-requirements/graph/changesets/2026-11-24-fr030-logic-p2-fixes.yaml` (test-applied on a scratch copy, 71 change rows; not applied to the live graph)

## Summary

The second and final logic review of FR-030 found 15 new items and 8 earlier fixes that were only partly done. All 15 are closed in the PRD, with matching graph operations where the item has graph rows. The change-set is waiting for the controller to apply.

## What Changed In The PRD

- A locked notice overrides the patient's channel toggles; the old sentence that global toggles still apply is removed.
- Escalation is offered only for locked notices; `aftercare.escalation_triggered` no longer has configurable escalation recipients.
- `inquiry.cancelled`, `booking.cancelled`, `system.alert` and `system.escalation` join the locked list. An approved account deletion still sends no cancellation notice.
- The Add Rule trigger no longer offers "timing" as a reason for a second rule; payment reminders have no fixed hour of day.
- The legal acceptance reminder is stated once as still reaching the user through at least one channel despite opt-out; the indicator row, REQ-030-019 and REQ-030-241 no longer contradict it.
- SMS wording says "selected events"; SMS stays out of the MVP.
- "Not opened" applies to email only.
- The in-app entry uses the event's catalogue default title and body when the rule has no push template; `dsr.fulfilled` creates no in-app entry.
- The Failed Deliveries list has one action, Retry (failed status only, logged); Mark Resolved and the separate re-trigger are removed; Workflow B1 gets a step 10.
- The appointment reminder defaults to two reminders, 7 days and 1 day before the appointment.
- The rate limit row names `SET-notification-throttling-thresholds`.
- Dependencies now list FR-013, FR-014, FR-023, FR-027 and FR-034.
- `account.email_change_code` gets a catalogue Rule (REQ-030-253); template language handling is stated one way.

## Graph Change-Set Contents

- New: REQ-030-253 (Rule), STP-030-072 (Retry step after STP-030-057).
- Updated: statements of the rules that mirror the PRD changes, `EVT-booking-appointment-reminder`, `ENT-notification-rule.escalation_conditions`, `ENT-notification-delivery-log` (read view) and `SET-notification-throttling-thresholds`.
- New edges: two `applies to` edges to `EVT-booking-cancelled`, the edges of the new Rule and Step, and 11 `references` edges from FR-030 to rules of FR-013, FR-014, FR-023, FR-027 and FR-034.

## Queued For Neighbour FRs

FR-020 (mirror row sentence, locked list for `inquiry.cancelled`, `booking.cancelled`, `system.alert`, `system.escalation`, opened marker on email attempts) and FR-020 / FR-006 (appointment reminder figures). Details in `plans/reports/docs-manager-261124-fr030-logic-p2-fixes.md`.
