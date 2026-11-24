# FR-004 Logic Review Pass 2 - Update Log

**Date**: 2026-11-24
**Scope**: FR-004 Quote Submission & Management PRD v4.4 and a prepared graph change-set
**Type**: Major update (rule changes, new steps, restated rules)

## Documents changed

- `functional-requirements/fr004-quote-submission/prd.md`: v4.3 to v4.4
- Prepared, not applied: `graph/changesets/2026-11-24-fr004-logic-p2-fixes.yaml` (applying it is the controller's step)

## What changed

- **Withdrawal of an accepted quote.** Allowed while the booking is Accepted or Confirmed, before check-in, with no provider-fault marker (was Confirmed only). Withdraw opens a confirmation that names the consequence: the booking goes to the admin for a transfer or refund. An ineligible accepted quote shows no Withdraw and a short note; the "contact support" wording for the provider is gone.
- **Frozen accepted quote.** REQ-004-109 now covers every field of the accepted quote except admin notes. One term is used everywhere: provider-fault marker (Glossary entry added).
- **Replacement quote.** Its currency is captured at the first Screen 8 save, shown on Screen 8 (new Currency row), and fixed after that. The draft is hidden from the provider and the patient until accepted, Screen 8 is its only edit surface, and it is excluded from Screens 2 and 7. A blocked Screen 8 names the failed precondition.
- **Replacement acceptance.** A new System step after the FR-005 acceptance record moves the draft from draft through sent to accepted and sets the first-send time. The acceptance runs no cancel-other-quotes cascade: the original quote keeps its status, and other open replacement drafts are cancelled silently with no provider notice. The cascade of REQ-004-003 now runs on the patient's acceptance only.
- **Restore.** Offered only for an expired quote and for a quote archived from draft or sent, while the inquiry is open, the provider is Active, there is no active acceptance and no provider-fault marker. Other archived quotes show no Restore. A failed guard blocks the restore with a message that names it. A new promotion reservation is taken only when the quote holds none.
- **Expiry events.** `quote.expiring_soon` and `quote.expired` fire once per expiry window; a restore opens a fresh window.
- **Banner.** Neutral wording for an inquiry that an admin closed or cancelled: "This inquiry was closed. Your quote can no longer be changed."
- **Lists and scenarios.** Screen 8 added to the Admin Platform and Entry Points lists. The null-expiry exception is stated on REQ-004-002, REQ-004-036 and the Expiry and Timer rows. User scenarios 24 to 28 added (withdraw before acceptance, the pending-fault freeze, the restore block, the replacement acceptance, the other replacement drafts). The 7-day auto-archive re-author case is stated in Workflow 7.
- **Graph change-set.** Restates 20 rule statements, adds 5 steps and 1 flow, retitles 5 steps and one flow, updates five screens, two quote fields and three events, adds the edge from the booking stage to the withdrawn event, moves the replacement-draft cascade to its own Platform Admin step, and adds branches for the Screen 8 preconditions and the restore guards.

## Open items for neighbouring FRs (not edited here)

- FR-006 Screen 10 ("saves the replacement quote on submit") and its mandatory adjustment reason beside FR-004 Screen 8.
- FR-005 REQ-005-052 (exactly one subquote Accepted and not superseded) fails between the withdrawal and the replacement acceptance; FR-005 lines on the cascade and the replacement draft.
- FR-030 REQ-030-035 and REQ-030-036: expiry events once per expiry window.
- FR-003 REQ-003-013: the cascade trigger for the replacement draft.
- FR-019: reservation release and re-take on archive and restore.
- The FR-010 and FR-005 mirrors of the pending-fault block; FR-006 Alternative Flow B5 expiry text, REQ-006-018 and FR-005 REQ-005-045 (queued from pass 1).
- STP-003-046 still has a `next` edge to the retired step STP-004-002.

## Validation

The change-set was applied to a scratch copy of the graph only: 108 change rows, lint 27 findings, identical to the baseline. Every REQ-004 statement in the PRD summary equals its graph statement.

## Applied

Applied by the controller on 2026-11-24. Backup `graph/backups/graph-2026-11-24-pre-fr004-logic-p2.db`; lint 27 findings, unchanged; `graph.json` exported. The controller moved STP-004-125 to STG-main-04-booking (where FR-005 records the replacement acceptance), so the `STP-005-016 next STP-004-125` edge is a forward edge with no back flag. Cross-FR change: `STP-005-016 next STP-006-606` now runs through STP-004-125.
