# FR-007B logic review, pass 1: fixes (2026-11-23)

## Summary

Pass 1 of the FR-007B (Payment Installments) logic review (requirements graph programme) raised 30 findings; all were accepted. The FR-007B PRD is fixed (v1.15) and a graph change-set is prepared. The change-set was validated on a scratch copy of the graph only (lint count unchanged at 27); it is not applied to the live graph.

## Rulings recorded (filing work)

- **Overdue.** Overdue is a calculated flag, not a status: from the day after the due date while the installment is unpaid. The patient gets one overdue notice and the billing admins one notice. The provider sees a banner from Overdue and is notified only when the plan is Defaulted. The Overdue status value and the provider overdue alert are removed.
- **Cancellation point.** The FR-029 Unpaid Balance Cancellation Point is counted from the due date of the first missed installment and wins over pending retries, the grace period and Defaulted. It hands the Confirmed booking to FR-006 B8. While unset nothing cancels automatically.
- **Pending provider fault.** While the support-required marker is on there is no charge, retry, reminder, Overdue, Defaulted or late fee, and the clocks pause. A replacement plan recalculates all dates; otherwise charges resume at the FR-006 Screen 10 submit.
- **Cancel route guard.** Cancel Booking is open only in Accepted, Payment Window Expired or Confirmed (In Progress only through the provider-fault route). After treatment starts a Defaulted plan is resolved by payment only.
- **Refund.** FR-006 and FR-007 compute and approve the refund; FR-007B voids the unpaid installments and records the outcome. The refund base is the paid amount excluding late fees.
- **Date change.** When the remaining installments cannot all fit the cutoff days, FR-006 blocks the change and nothing changes. The insufficient-time notice and its steps are retired.
- **Provider-fault branch.** The full-refund and replacement-plan branch is entered only from FR-006 B4 and B5. The unpaid-balance cancellation (B8) uses the common cancel step and then the refund ladder.
- **Installment threshold.** Days to procedure must be at least the cutoff days plus 30; the maximum count is the days minus the cutoff days, divided by 30, rounded down, plus 1.
- **Late fee.** Added once to the installment when the grace period, counted from the due date, passes unpaid; collected with the next successful charge; excluded from the refund base. The rescheduling fee does not apply to installment plans in V1.
- **Hard decline and Defaulted.** A hard decline gets no automatic retry and the plan is Defaulted on day 11 after the due date; the patient can use Pay now or update the card. Later installments of a Defaulted plan are paused until an admin resolves it. Mark as Resolved records the external payment and can reopen the plan; admin retries do not count toward the 3 automatic retries.
- **Money movement.** Commission, payout timing and the share movement point to FR-007 and FR-017; FR-007B keeps only that the plan is Completed when the final installment is paid.
- **Smaller fixes.** Reminders follow the FR-007 payment reminder setting; installments need a card; the Payment Options step has three options; the last installment absorbs the rounding remainder; one spelling of Cancelled; stray cross-reference lines carry their rule text.

## Documents changed

- **FR-007B PRD (v1.15)**: Multi-Tenant Breakdown, Communication Structure, Entry Points, Main Flow and Alternative Flows A2, A3, B1 to B4; Screens 1, 2, 4, 5 and 6; Business Rules (new Overdue, cancellation point, pending fault, cancel route, Defaulted pause, eligibility and cutoff rules; Admin Editability; Payment and Billing); User Stories 1, 2, 3, 5 and 6; Edge Cases; Requirement Summary (REQ-007B-009, 014, 018, 019, 021, 022, 024, 026, 027 reworded, new REQ-007B-101 to 107); Dependencies; Appendix: Change Log row.
- **Graph (change-set only)** `graph/changesets/2026-11-23-fr007b-logic-p1-fixes.yaml`: Rule statements reworded to match the PRD; new Rules REQ-007B-101 to 107; new Steps STP-007B-305 and 410 to 414; Steps 604, 605 and 606 retired; new Event for the overdue notice; the provider overdue alert and insufficient-time events retired; new ENT-installment-payment fields for the Overdue flag, late fee and payment source; new metrics field for Defaulted plans; status enum changes; edge changes on the installment-failure, cancellation, date-change and provider-fault flows.

## Not changed

- FR-006, FR-007, FR-010, FR-017, FR-029, FR-030 and FR-020 PRDs, and the FR-029 settings in the graph, are unchanged. Their sentences that conflict with the rulings above are listed with the open questions in `plans/reports/docs-manager-261123-fr007b-logic-p1-fixes.md`.
- The change-set retitles three outgoing edges of FR-006 steps that point to the FR-007B common cancel step (labels only).

## Applied

The controller applied the change-set to the live graph on 2026-11-23 (369 change rows). Lint stays at 27 findings, and graph.json was re-exported. The day boundary for the charge, the Overdue flag and the late fee now follows FR-007: the calendar day in the clinic's timezone.
