# FR-017 Logic Review, Pass 1 (2026-11-24)

**Type**: Major update (revised PRD, version 2.18 to 2.19, with a graph change-set)
**Scope**: FR-017 Admin Billing and Financial Management
**Source of findings**: `plans/reports/tester-261124-fr017-logic-p1.md` (18 findings; all accepted, five with a recorded default)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr017-admin-billing-finance/prd.md`

- **Two payout rails, two vocabularies**: a settlement statement is manual-rail only, with the states Pending Approval, Approved, Overdue, Paid and Voided. Processing, Failed, the `transfer.*` webhooks, Retry Payout and the three automatic attempts belong to the Stripe Connect per-booking payout, listed in a Stripe Connect payouts section on Screen 2 (REQ-017-186, REQ-017-187).
- **Mark as Paid**: new control on Screen 3 with re-authentication, bank reference, payment date and an optional bank charge recorded as a Bank Charge adjustment; the statement becomes Paid, the audit entry is "Payout Marked Paid", the clinic is notified and the invoice document is generated on that event (REQ-017-188).
- **Overdue statements**: approval makes an Overdue statement payable at once; it never waits for the next payout day. Unapprove is not offered once the payout day has passed (REQ-017-076, REQ-017-153).
- **Funds-released gate**: statements, the running total and per-booking payouts include only released earnings; the earnings summary shows Pending release and Released (REQ-017-189).
- **Screen 7 outcomes**: release in full, refund in full, and refund in part with release of the rest; the refund outcomes open FR-007 Screen 6 with an admin-set amount. A Release earnings resolution settles a Suspended or Deactivated clinic with no target cycle (REQ-017-190, REQ-017-193).
- **Refunds**: Screen 4b is a launcher into FR-007 Screen 6; FR-017 keeps the invoice status effect and the payout effect. The FR-017 refund validation and approval text is removed, and the closure refund of General Module Rule 13 is started by the system through FR-007 (REQ-017-199).
- **Invoice statuses**: every FR-017 screen uses the FR-007 Payment Status list; Overdue is read from the Final Payment Status and shows from the day after the due date; At Risk is a separate flag; a part refund is a refund-history row. The "7 days" figure remains only as the reminder and alert cadence (REQ-017-050, REQ-017-083, REQ-017-084, REQ-017-086).
- **Installment job**: one hourly job in the clinic's timezone; reminders at 9 AM clinic time, 3 days before the due date (REQ-017-183).
- **Clinic balance record**: signed entries (refund deduction, chargeback recovery, clinic cancellation deduction, bank charge) applied to the next payout on either rail and shown on Screens 2, 3 and 9. A debt with no further payout coming stays open until an admin writes it off with a mandatory reason and an audit entry (REQ-017-191, REQ-017-192, REQ-017-075).
- **No forfeiture**: the earlier ban rule is removed; the earnings of a removed clinic are always settled by an admin through General Module Rule 16 and the Release earnings route (REQ-017-138; REQ-017-173 retired).
- **Stripe readiness**: Not onboarded, Restricted or Ready, and a Waiting for clinic setup state on the per-booking payout list (REQ-017-196).
- **Manual Review Required**: set by the fraud flag or after three failed attempts; approval and retry are disabled; an admin clears it with a review note, audited (REQ-017-194).
- **Hairline discount reimbursement**: its own row on the statement and the per-booking payout, read from the frozen booking snapshot (REQ-017-195).
- **Affiliate payouts on Screen 6**: payable only when the month is closed, the balance is at or above the USD 50 minimum (none for an Inactive affiliate), readiness is Ready and no hold applies; a Held or Flagged column; readiness comes from FR-018 and the floor is checked in USD after conversion (REQ-017-197, REQ-017-198).
- **Clinic cancellation deduction**: FR-029 Screen 7 named as the source; applied only while set, in the Fee Currency converted to the payout currency, through the clinic balance record (REQ-017-180).
- **Outstanding-invoice alert**: defaults to 7 days (REQ-017-182).
- **Minor**: User Story 1 uses the stated defaults instead of "every Friday"; the Integration 1 line follows the two-rail wording.
- The change log row and Last Updated are set.

## Graph change-set

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr017-logic-p1-fixes.yaml`

- New: rules REQ-017-186 to REQ-017-199; entity ENT-clinic-balance-entry; 13 fields; 25 enum values; flows FLW-017-per-booking-payout and FLW-017-clinic-balance; steps STP-017-084 to STP-017-099.
- Updated: 47 rule statements (some titles and rationales), 10 step titles, screen, flow and setting descriptions; the Screen 4b node is now "Refund Launcher".
- Retired: REQ-017-173, REQ-017-094, REQ-017-095, REQ-017-096, REQ-017-097, REQ-017-146; five old invoice Payment Status enum values.
- Removed edges: the two main-flow `next` edges that sent every approved statement to the Stripe transfer step; the old refund-rule `applies` edge on the flagged-invoice step; nine Screen 4b refund-field `shows` edges; four Screen 5 discount-code `shows` edges.
- Cross-FR edges: REQ-017-198 applies to an FR-018 field; STP-017-089 is on FR-007 Screen 6; Screen 5 shows FR-019 promotion fields (edges only). No node owned by another FR is updated or retired.
- Test-applied on a scratch copy of the graph: 627 change rows, no errors, no unreachable step; the copy was deleted. The change-set was then applied to the live graph by the controller.

## Not changed here

Neighbour changes for FR-006, FR-007 (including the owner of the payout execution window setting), FR-007B, FR-014, FR-015, FR-018, FR-019, FR-029, FR-030 and FR-031 are queued in the logic review ledger section for FR-017 and are not part of this change. Minor observations and the leftovers (unused statement enum values, the refund entity's remaining fields, the reminder type list) are listed there too.
