# FR-007B Logic Review Pass 2 (2026-11-23)

## What changed

- **PRD:** `functional-requirements/fr007b-payment-installments/prd.md` is now v1.16.
- **Graph:** a prepared change-set `graph/changesets/2026-11-23-fr007b-logic-p2-fixes.yaml` (158 operations). It is written and checked on a scratch copy of `graph.db`. It is **not applied** to the live graph.
- Nothing outside FR-007B was edited. Items in neighbour PRDs are queued, not fixed.

## Decisions applied in the PRD

- The support-required marker now also pauses the cancellation-point count and the hand-off to FR-006 Alternative Flow B8 (the FR-007B side only).
- A Defaulted plan pauses its later installments: they keep dates and amounts and carry no Overdue flag, notice, reminder or late fee. When the plan returns to Active, whoever paid, each past-due paused installment is charged once at the next daily run.
- Mark as Resolved is only a recorded bank transfer into Hairline's account (amount, date, receiving account, reference), approved by a second billing admin. FR-007 owns the manual payment record.
- Late fee: a fixed fee is converted at the plan's accepted rate, a percentage applies to the late installment amount, the fee stays outside the clinic share and commission, it waits until retries end, it lapses with the plan, and a provider-fault full refund returns a collected fee.
- Screen 1 shows the late fee, grace period and cancellation point, and the plan keeps them as confirmed. The overdue notice states the cancellation date when the point is set.
- Insufficient funds is retried like a technical failure. A hard decline is an expired, lost, stolen, invalid or fraud-flagged card, and a hard decline on a retry cancels the retries still pending.
- On the first overdue day the retry runs first and the overdue notice replaces that day's failure notice.
- A date change keeps due dates, count and amounts and recalculates only the Final Payment Deadline. Only enabled installment counts are offered. Pay now can pay the next scheduled installment or all remaining ones early. The provider list covers plans of any status. The clinic share moves as FR-007 sets.
- One void step runs before the refund and sets the plan Cancelled; "canceled" becomes "cancelled".
- The daily job schedule is stated as FR-017's; FR-007B states only the boundary.

## Graph change-set summary

- New Rules REQ-007B-108 to 112; new plan fields `late_fee_setting`, `grace_period_days`, `cancellation_point_days` shown on Screen 1; new Steps STP-007B-015, 415, 416, 417, 418; STP-007B-504 retired and STP-007B-701 is the single void step.
- Guards on edges 701 to 702, 702 to 703, 408 to STP-006-301 and 503 to STP-006-301 use the `condition` attribute; edges of retired steps are removed.
- Scratch validation: `write.py` applied it (233 change rows); `lint.py --json` count 27, the same as the live baseline, with the same findings.

## Queued, not fixed here

- FR-006 B8 marker wording; FR-007 manual payment record, refund and share treatment of a manual payment; FR-029 late fee wording (currency and base) and the cancellation-point range; FR-017 hourly or clinic-day job schedule.
- No late-fee notice exists in the PRD, so no late-fee event is modelled.

Full per-finding detail: `plans/reports/docs-manager-261123-fr007b-logic-p2-fixes.md`.

## Applied

- 2026-11-23: change-set `2026-11-23-fr007b-logic-p2-fixes.yaml` applied to the live graph (233 change rows). Backup `graph/backups/graph-2026-11-23-pre-fr007b-logic-p2.db`. Lint count 27 (unchanged). `graph.json` re-exported.
