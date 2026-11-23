# FR-007 Logic Review Pass 1 - 2026-11-23

**Scope**: FR-007 Payment Processing PRD (v1.14 to v1.15) and a prepared requirements-graph change-set.

**Graph status**: The change-set is prepared and validated on a scratch copy of the graph only. It is not applied to the live graph; the controller applies it. Lint on the scratch copy stayed at the baseline count.

## What changed

- **Final payment due date**: One rule. The final payment is due the FR-029 balance due days before the procedure (default 7). Overdue starts the day after, flagged once by a scheduled job, with a notice to billing admins. Reminder timing is an admin setting of whole days 0 to 14 before the due date, up to 3 reminders, default 3 days before and on the due date.
- **Unpaid balance**: It cancels a booking only through the FR-029 Unpaid Balance Cancellation Point when an admin has set one, run by FR-006 Alternative Flow B8, and only for bookings confirmed after the point is set. Screen 2 shows the point when set.
- **Refund approval**: Applies only to exception refunds and manual refunds. The approver is any other admin with billing permission, never the requester; both are recorded. Added a Deny action with a reason, an awaiting-approval state, and an escalation notice to billing admins after 2 business days; nothing is approved automatically. Closure-case refunds need no second approval.
- **Screen 6**: The single refund control, with a refund case selector (closure case, exception, manual), an admin-set amount field, a closure cause row, and approval status, requester and approver rows. One reason rule: 10 to 500 characters.
- **Refund amounts**: The ladder percentage applies to the amount paid toward the booking total, late fees excluded; the cancellation fee is the amount paid less the amount refunded. The refund after a closure is the amount the closure case sets.
- **Clinic share**: For the deposit-and-balance option, the part paid above Hairline's commission moves at the 60-day mark and each later payment tops it up.
- **Payout eligibility**: Waits for completion plus the confirmation window with no problem raised, or an admin resolution. New steps for the retry and replacement paths.
- **Late capture**: A payment captured after the hold expired or after a non-provider cancellation is refunded in full automatically, with an audit entry and a patient notice.
- **Payment options**: Three options (in full now, deposit now and balance later, installments 2 to 9). FR-007 Screen 1 shows the chosen option read-only.
- **Payment status**: At Risk removed. Refunded means all paid money returned; deposit Partial defined.
- **Standalone aftercare payment**: New flow A3. Refunds are an admin decision with a reason; the provider's money is released after the confirmation window counted from the payment.
- **Smaller items**: Pre-promotion price label renamed; recovery wording names who cancels the inquiry; provider-fault payout hold and release steps added; refund-of-admin-set-amount step added; the duplicate revive step retired in favour of the FR-006 route; one sentence that payment and reminders are blocked while an FR-006 provider fault is pending.

## Files

- `local-docs/project-requirements/functional-requirements/fr007-payment-processing/prd.md` (v1.15)
- `local-docs/project-requirements/graph/changesets/2026-11-23-fr007-logic-p1-fixes.yaml` (not yet applied)

## Neighbour follow-ups (other FRs, not edited here)

- FR-006: Screen 1 needs the third payment option; the B8 trigger wording must cover deposit-and-balance; Process Refund must open FR-007 Screen 6.
- FR-017: refund action must open Screen 6; its overdue definition and invoice status list differ from FR-007.

## Applied

- 2026-11-23: change-set applied to the live graph by the controller (361 change rows); backup `graph/backups/graph-2026-11-23-pre-fr007-logic-p1.db`; lint 27 findings, unchanged; `graph.json` re-exported.
