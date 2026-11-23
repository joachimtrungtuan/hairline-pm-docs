# FR-006 logic review, pass 2: fixes (2026-11-23)

## Summary

Pass 2 of the FR-006 logic review (requirements graph programme) raised 16 findings and left three pass-1 items partly open; all were accepted. The FR-006 PRD is fixed (v2.20) and a second graph change-set is prepared. The change-set was validated on a scratch copy of the graph only (lint count unchanged from the live baseline); it is not applied to the live graph, so applying it, the export and the consistency run stay with the controller.

## Rulings recorded (filing work)

- **Pending provider fault.** From the withdrawal or drop-out trigger the booking carries `supportRequired` with cause `ProviderFault`. Payment, payment reminders and revive are blocked, and the hold does not expire until the Screen 10 submit. Screen 10 re-checks the booking status at submit: `Accepted` or `Confirmed` proceed, `In Progress` goes to Alternative Flow B7. A B2 cancel in this period takes cause `ProviderFault`, the full refund and no fee.
- **Close inquiry.** New admin action for a `Cancelled` booking that still carries `supportRequired`: the inquiry becomes `Cancelled`, the marker is cleared and the patient is notified. It replaces the old "cancel via B2" wording.
- **Cancel Booking scope.** Screen 6 does not offer Cancel Booking in `In Progress` or `Aftercare`; an in-progress cancellation goes through the Screen 11 Cancel route.
- **One refund per closure.** Process Refund and the automatic refund exclude each other; the in-progress fault has one refund route per decision (Move to Aftercare through FR-007, Cancel through the Screen 9 refund step).
- **In-progress refund source.** The refund comes out of the held payout; if the payout was already released, the shortfall is deducted from the provider's next payout (carried by FR-017, not edited here).
- **Unpaid balance.** The cancellation point counts days after the due date of the first missed installment and applies only to bookings confirmed after the value is set; unset means no automatic cancellation. B8 voids the remaining installments and reaches the refund calculation once.
- **Emergency edit.** Changes only the appointment time on the same date and the booking notes; dates go through Screen 8; price, package, provider and clinic are never changed. Screen 6 lists the editable fields.
- **Smaller fixes.** Screen 8 checks the new date against the payment deadline of an `Accepted` booking; fee and refund amounts on the cancel notice are system-filled; Screen 11 is read-only after a recorded decision until the route completes; stale text in B1, B2, B5, Screens 1, 4, 5, 6 and 9 aligned.

## Documents changed

- **FR-006 PRD (v2.20)**: Alternative Flows B1, B2, B5, B7 and B8; Screens 1, 4, 5, 6, 7, 8, 9, 10 and 11; Business Rules; REQ-006-004, 011, 016 to 019 and 074 reworded; new REQ-006-081, 082 and 083; User Story 4 scenarios; one Edge Case; Appendix: Change Log row.
- **Graph (change-set only)** `graph/changesets/2026-11-23-fr006-logic-p2-fixes.yaml`: Rule statements reworded to match the PRD; new Rules REQ-006-081 to 083; new Steps STP-006-210 (Close inquiry), STP-006-211 and STP-006-609; new Flow FLW-006-close-inquiry; edge changes on the provider-fault, cancel, in-progress fault, unpaid-balance and emergency-edit routes; Screen 6 shows edges for the closure cause and support-required fields; Setting `SET-unpaid-balance-cancellation-point` gains a days unit and a reworded description.

## Not changed

- FR-004, FR-007B, FR-017 and FR-029 PRDs are unchanged. Their sentences that still say a booking never cancels automatically for an unpaid balance, or that route to "cancel the inquiry and booking in FR-006", are listed with the open questions (including the 7 versus 30 days mismatch) in `plans/reports/docs-manager-261123-fr006-logic-p2-fixes.md`.

## Applied

- 2026-11-23: change-set applied to the live graph by the controller (123 change rows); backup `graph/backups/graph-2026-11-23-pre-fr006-logic-p2.db`; lint 27 findings, unchanged; `graph.json` re-exported.
