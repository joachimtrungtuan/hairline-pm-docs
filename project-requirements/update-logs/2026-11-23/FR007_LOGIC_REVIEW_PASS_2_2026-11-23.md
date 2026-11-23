# FR-007 Logic Review Pass 2 - 2026-11-23

**Scope**: FR-007 Payment Processing PRD (v1.15 to v1.16) and a prepared requirements-graph change-set.

**Graph status**: The change-set is prepared and validated on a scratch copy of the graph only. It is not applied to the live graph; the controller applies it. Lint on the scratch copy stayed at the baseline count with no new finding. It builds on the pass 1 change-set, which must be applied first.

## What changed

- **Unpaid balance cancellation**: The unpaid balance cancels only at the FR-029 cancellation point (FR-006 Alternative Flow B8), for bookings confirmed after the point is set. REQ-007-021 and User Story 2 say so.
- **Short notice**: A booking confirmed with fewer days left than the FR-029 balance due days pays the full amount at confirmation. Deposit and balance and installments are not offered (new REQ-007-101).
- **Final Payment Status**: One stored status moved by the scheduled job (Not Due, Due on the due date, Overdue the day after), by calendar day in the clinic's timezone. The Overdue flag reads from it and clears, and reminders stop, when the booking is Cancelled or Completed. The hard-coded 3 days is removed. The patient gets one overdue notice.
- **Refund amount**: An exception or manual refund amount is set by the admin, from zero up to the amount still refundable, with a required reason and the ladder amount shown beside it.
- **Closure refunds**: The refund case is bound to the recorded closure cause, and the system starts closure refunds. Only the exception and manual cases are chosen by an admin.
- **Approval**: New Awaiting approval view for other billing admins. Approval leads to execution and denial ends with a notice. After 2 business days the request escalates to a super-admin. Self-approval is never allowed. The sum of refunds on a booking is capped at the amount paid.
- **Partial deposit**: A partial deposit is refunded in full automatically when the hold expires, the same route as a late capture. Payment Status stays Unpaid, because there is no Pending value.
- **Clinic share**: Full payment and the plan completion step now lead to the share movement step; the late capture step leads to the automatic refund step.
- **Payment option**: Chosen on FR-006 and changeable only before the first successful payment, by returning to FR-006. Screen 1 gains an Amount Due Now row. The payment option enum order is fixed.
- **Standalone aftercare payment**: A lightweight aftercare payment record (no booking) opens Screens 5B and 6. Retry and the 48-hour expiry follow FR-011 Alternative Flow B1; FR-011's automatic refund stays for its failure cases. An admin refund of that payment goes through the manual refund route.

## Files

- `local-docs/project-requirements/functional-requirements/fr007-payment-processing/prd.md` (v1.16)
- `local-docs/project-requirements/graph/changesets/2026-11-23-fr007-logic-p2-fixes.yaml` (not yet applied)

## Neighbour follow-ups (other FRs, not edited here)

- FR-006: the closure causes for patient request and admin cancellation are missing from the closure cause list; Screen 1 must offer only full payment on short notice; B8 wording.
- FR-029: check that the unpaid balance cancellation point (a number of days after the first missed due date) falls before the procedure date for the due date setting; the balance due days range.
- FR-030: templates for the patient overdue notice and the super-admin escalation notice.
- FR-011: link the aftercare payment steps to its retry and expiry flow.
- FR-007B: the plan completion step now leads to the clinic share step.

## Owner confirmations needed

- A booking confirmed with exactly as many days left as the balance due days is treated as due on the confirmation day (pays in full).
- Payment Status Unpaid for a partial deposit.
- The admin-set amount for an in-treatment closure is set in FR-006 and shown read-only on Screen 6.

## Applied

- 2026-11-23: change-set applied to the live graph by the controller (222 change rows); backup `graph/backups/graph-2026-11-23-pre-fr007-logic-p2.db`; lint 27 findings, unchanged; `graph.json` re-exported.
