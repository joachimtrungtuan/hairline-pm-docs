# FR-029 Logic Review Pass 1 (2026-11-23)

## What changed

- **PRD:** `functional-requirements/fr029-payment-system-config/prd.md` is now v1.17.
- **Graph:** a prepared change-set `graph/changesets/2026-11-23-fr029-logic-p1-fixes.yaml` (251 operations). It is written and checked on a scratch copy of `graph.db`. It is **not applied** to the live graph.
- Nothing outside FR-029 was edited. Items in neighbour PRDs are queued, not fixed.

## Decisions applied in the PRD

- **Installment schedule and cutoff:** the first installment is due on the booking day, then every 30 days. A plan of n installments needs at least cutoff + 30 x (n - 1) days between booking and procedure, so the minimum lead time for installments is cutoff + 30 days. Screen 4 always shows it, shows the minimum for each count, and warns when the cutoff is above 60 days. A booking too close to the procedure sees no installment option, and no message offers one.
- **Balance due days:** 1 to 30 days, default 7. A booking confirmed with fewer days left than this gets full payment only.
- **Unpaid balance cancellation point:** 1 to 30 days after the first missed due date, smaller than the balance due days and than the installment cutoff. It may be "Not set"; while it is not set nothing is cancelled. It covers any unpaid balance (deposit and balance, or installments) and wins over pending retries and the Defaulted state.
- **Hairline's share of a patient cancellation fee:** may be "Not set". While it is not set Hairline keeps the whole fee and billing admins are flagged.
- **Clinic cancellation deduction:** now set on Screen 7 (it was only a FR-017 setting): a fixed amount in the Fee Currency, no starting value, no deduction while it is not set. FR-017 reads it.
- **Screen 7 validation:** a save is refused, naming the field, when balance due days, the cancellation point or the confirmation window is out of range, when the cancellation point is not smaller than both the balance due days and the cutoff, or when the settlement cutoff day and payout day are the same.
- **Locks:** the refund ladder and the rescheduling fee now lock at booking confirmation, like the late fee, grace period, cancellation point and cutoff. The share, the deduction and the confirmation window apply on the day of the event.
- **Settlement and confirmation window:** the settlement period is weekly only in V1; admins edit the cutoff day and payout day, which must differ. The confirmation window is 1 to 30 days, default 7.
- **Fees:** a fixed late fee and a fixed rescheduling fee are stated in the Fee Currency (the default currency when Screen 7 was last saved) and converted at the booking's accepted rate; the late fee percentage is of the late installment. The late fee is charged once, after the grace period and the retries. The rescheduling fee never applies to a change an admin makes in V1. A Default Currency change never reinterprets stored fee amounts; the admin is asked to re-confirm Screen 7.
- **Currency:** a routed account that does not support the booking currency is charged in USD at the locked rate. A price in a third currency goes via USD with the markup applied once, on the pair for the shown currency; installment eligibility uses the base rate without markup. A locked rate survives deletion of its pair. A currency that is the Default Currency of an active Stripe account cannot be disabled.
- **Rate protection:** a pair is compared with its rate 24 hours earlier. The yellow badge clears only when an admin clicks Acknowledge on Screen 2B (logged); a later normal sync does not clear it.
- **Stripe accounts:** Account Status is Active, Inactive or Archived; an account an open booking or active installment plan uses is archived, not deleted. A booking keeps the account that took its first payment for every later charge and refund. On production only Live, Active accounts are routed and the Global Fallback is Active and Live. A patient with no profile country is asked to add one, with no alert; the unsupported-country alert goes out once per country per day.
- Two new main flows are written out in the PRD: "Configure Refund, Fees and Settlement" and "Manage Supported Currencies". New requirements REQ-029-150 to REQ-029-156.

## Graph change-set summary

- Updated text of 32 Rules, 15 Settings, 15 entity fields and 14 Steps; Screens 1, 2A, 2B, 4, 6 and 7 descriptions.
- New Rules REQ-029-150 to 156; new Steps STP-029-159 to 178; new main flows FLW-029-main-refund-fees-settlement and FLW-029-main-currency-management.
- New fields `clinic_cancellation_deduction` and `fee_currency` on the Screen 7 entity, shown on SCR-029-08; new enum value `archived` on the account status.
- `unpaid_balance_cancellation_point` becomes an optional integer; `hairline_cancellation_fee_share` becomes optional.
- STP-029-151 becomes the admin Acknowledge step (done by the platform admin on Screen 2B), followed by the new logging step STP-029-159. STP-029-152 no longer sits on the deposit screen.
- **Ownership move:** `SET-clinic-cancellation-deduction` moves from FR-017 to FR-029. FR-017 keeps its rule REQ-017-180 that reads it.
- Scratch validation: `write.py` applied it (407 change rows); `lint.py --json` count 27, the same as the live baseline, with the same findings.

## Queued, not fixed here

- FR-007B: the tail after the cutoff.
- FR-007: the stored routed Stripe account on the booking, and REQ-007-092 behaviour while the share is not set.
- FR-017: reading the clinic cancellation deduction from Screen 7.

Full per-finding detail: `plans/reports/docs-manager-261123-fr029-logic-p1-fixes.md`.

## Applied

- 2026-11-23: change-set `2026-11-23-fr029-logic-p1-fixes.yaml` applied to the live graph. Backup `graph/backups/graph-2026-11-23-pre-fr029-logic-p1.db`. Lint count 27 (unchanged). `graph.json` re-exported. SET-clinic-cancellation-deduction is now owned by FR-029.
