# FR-005 logic review, round 2: fixes (2026-11-23)

## Summary

Round 2 of the FR-005 logic review (requirements graph programme, Phase 10 pilot) raised 21 findings. Four were planted test defects (all caught). Eleven were fixed here, none was rejected, and six wait in the findings ledger because another FR or the shared stage list owns them (four of the six repeat round 1 items). Nine of the eleven round 1 defects were confirmed gone; the two left over are fixed here.

## Decision recorded (filing work, no owner question)

- After an admin-authored replacement acceptance (FR-006 provider-fault transfer) the original accepted subquote takes the state **Superseded**: read-only, never acceptable again, its acceptance record and snapshot unchanged. REQ-005-004 already used the word; REQ-005-052 now defines it.

## Documents changed

- **FR-005 PRD (v3.7)**: terms acknowledgment is required on a patient acceptance and empty on an admin replacement acceptance (REQ-005-024); the inquiry-cancellation cascade cancels only draft, sent and expired quotes (REQ-003-013); Superseded state (REQ-005-052, Screens 1 and 4, Alternative Flow A9); Screen 4 shows "Cancelled (Provider Status)" with the reason "Provider account suspended or deactivated" (REQ-005-039); REQ-005-016 says the question is an FR-012 message and the provider notice arrives within 5 minutes at the latest.
- **FR-010 PRD (v2.12)**: the FAQ on editing an accepted quote agrees with the owner ruling of 2026-11-23 (an admin may edit every field except price, currency and promotion).
- **Graph** (change-set `graph/changesets/2026-11-23-fr005-logic-review-r2-fixes.yaml`, 53 change rows; backup `graph/backups/graph-2026-11-23-pre-fr005-logic-r2.db`): new Steps STP-005-028 (Message Provider) and STP-005-029 (stale-version rejection); STP-005-014 placed on SCR-005-01; replacement steps ordered STP-006-605, STP-005-016, STP-006-606, with STP-005-016 on SCR-006-10 at the booking stage; enum value `superseded` on `ENT-subquote.acceptance_state`; `ENT-acceptance-event.terms_acknowledged_at` no longer required; owning steps for REQ-005-044 and REQ-005-048; 11 links removed from six retired FR-005 rules. Lint unchanged at 31 findings.
- **Tooling**: `graph/scripts/logic_gate.py` no longer range-checks citations of other documents (`frNNN prd:N`, `system-prd:N`) against the reviewed PRD.

## Not changed

- Findings owned by FR-003, FR-007, FR-014, FR-019, FR-022 and the shared stage list are queued in `plans/reports/logic-review-ledger.md` (project root) for those FRs' reviews.
