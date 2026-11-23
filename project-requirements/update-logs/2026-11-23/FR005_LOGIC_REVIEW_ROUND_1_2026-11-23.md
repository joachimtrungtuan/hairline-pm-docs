# FR-005 logic review, round 1: fixes and two owner rulings (2026-11-23)

## Summary

Round 1 of the FR-005 logic review (requirements graph programme, Phase 10 pilot) raised 24 findings. Four were planted test defects (all caught). Fourteen were fixed here, two were rejected with the second reviewer's evidence, and seven wait in the findings ledger because another FR owns them.

## Owner rulings (2026-11-23)

- **Admin edit of an accepted quote is kept.** An admin may edit any field except price, currency and promotion, including date range, appointment and treatment details. An edit of the date range or appointment runs the same slot check as the FR-006 admin appointment change, updates the booking's current appointment and emits `booking.rescheduled`; an edit of treatment details notifies the patient through `treatment.plan_changed`; the acceptance snapshot never changes.
- **The "Message Provider" button on the quote detail screen is kept.** It opens the conversation in the Messages inbox; chat is never embedded in a quote screen.

## Documents changed

| Document | Version | Change |
|---|---|---|
| FR-005 PRD | 3.6 | Provider field rows retagged from a retired graph field to `ENT-provider.awards`; promotion-code failure at confirmation (A8, Edge Cases, REQ-005-026); accepted total is the price after promotion (REQ-005-037); price per graft uses the offered price before promotion (REQ-005-051); REQ-005-006 and REQ-005-023 carry the admin-edit ruling |
| FR-004 PRD | 4.2 | REQ-004-084 names the admin edit beside the FR-006 admin appointment change |
| FR-006 PRD | 2.18 | REQ-006-067 names the admin edit as a date-change path |
| FR-010 PRD | 2.11 | REQ-010-027, REQ-010-042, REQ-010-043, Boundary and A2 lines name the admin edit as the exception to "FR-010 is the only path" |
| FR-012 PRD | 2.15 | REQ-012-006 and REQ-012-029: chat is not embedded in quote screens; a quote screen may link to the inbox conversation |

## Graph

Change-set `graph/changesets/2026-11-23-fr005-logic-review-r1-fixes.yaml` (71 operations, 93 change rows): five new Steps (STP-005-023 to 027) for the provider and admin screens and three missing branches; new `next` links including the hand-offs to the FR-006 admin cancel and hold expiry; steps 010 and 014 moved to the booking stage; live edges removed from two retired rules; twelve rule statements reworded. Lint unchanged at 31. Backup `graph/backups/graph-2026-11-23-pre-fr005-logic-r1.db`.

## Not changed

- Nine rules in FR-006, FR-007B, FR-010, FR-015 and FR-016 still describe the FR-006 admin appointment change without naming the admin edit; they are recorded for those FRs' own reviews.
- The patient-entered promotion code has no data home before acceptance: implementation backlog.
