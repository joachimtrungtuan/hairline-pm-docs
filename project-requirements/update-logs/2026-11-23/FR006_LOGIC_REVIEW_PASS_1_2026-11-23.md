# FR-006 logic review, pass 1: fixes (2026-11-23)

## Summary

Pass 1 of the FR-006 logic review (requirements graph programme) raised 17 findings, all accepted. The FR-006 PRD is fixed (v2.19) and a graph change-set is prepared. The change-set was validated on a scratch copy of the graph only; it is not applied to the live graph, so applying it, the export and the backup are for the controller.

## Rulings recorded (filing work)

- **One refund wording.** A full refund with no fee applies when the provider withdraws, drops out, or is suspended or deactivated before treatment starts. The FR-029 refund ladder applies to every other cancellation. An in-treatment provider fault takes an admin-set refund, with a reason and an audit entry, and the provider payout is held.
- **In-progress fault (Screen 11).** Screen 9 shows the Screen 11 amount read-only on that route and the ladder does not apply. The decision only records the choice; the `supportRequired` marker and the payout hold resolve once, when the chosen route completes (Screen 9 submit for Cancel, FR-011 Screen 19 submit for Aftercare).
- **`Aftercare`** also covers a treatment closed early by an admin decision on Screen 11; the decision date is the aftercare start handed to FR-011.
- **Provider-fault transfer.** The original booking is cancelled at the admin submit on Screen 10, not at the trigger.
- **Unpaid balance.** The system cancellation of an Installments booking is a new Alternative Flow (B8) with closure cause `UnpaidBalance`; the inquiry is cancelled too; `booking.cancelled` is sent on any cancellation; the rule stays inactive until the FR-029 cancellation point is set.
- **Date changes.** Screen 8 and the admin edit of the accepted quote (REQ-005-023) run the same checks; the FR-029 rescheduling fee never applies to an admin-made change in V1; Screen 8 blocks when no installment plan is feasible.
- **Provider identity** stays visible to the provider once the booking has reached `Confirmed`, including after a later cancellation.

## Documents changed

- **FR-006 PRD (v2.19)**: Alternative Flows B1, B2, B4, B5, B7 and new B8; Screens 1, 3, 4, 6, 7, 8, 9, 10 and 11; Business Rules; REQ-006-004, 008, 011, 016 to 020; Appendix: Change Log row.
- **Graph (change-set only)** `graph/changesets/2026-11-23-fr006-logic-p1-fixes.yaml`: new Steps STP-006-206 to 209, 804, 805, 901 and 902; new Flows FLW-006-b8, FLW-006-change-appointment and FLW-006-emergency-edit; enum value `unpaid_balance` on `ENT-booking.closure_cause`; reworded Rules and Step titles; the B5 chain reordered; refund and installment edges for the provider-status cascade; four waiting cross-FR hand-offs to the appointment change stitched; retired-rule edges removed; the `quote.withdrawn` producer edge removed from the booking stage. Scratch run: lint 31 findings before, 27 after (the four resolved are hand-off findings), no new finding.

## Not changed

- Rules without an applying Step are listed in `plans/reports/docs-manager-261123-fr006-logic-p1-fixes.md` for the backlog.
- FR-005, FR-007B and FR-029 PRDs were read only at the hand-off points and are unchanged; open questions for their owners are in the same report.

## Applied

- 2026-11-23: change-set applied to the live graph by the controller (184 change rows); backup `graph/backups/graph-2026-11-23-pre-fr006-logic-p1.db`; lint 31 to 27 findings, none new; `graph.json` re-exported.
