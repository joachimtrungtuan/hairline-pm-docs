# FR-018 Logic Review, Pass 2 (2026-11-24)

**Type**: Major update (revised PRD, version 2.8 to 2.9, with a graph change-set)
**Scope**: FR-018 Affiliate Management
**Source of findings**: `plans/reports/tester-261124-fr018-logic-p2.md` (13 findings, all ruled fix; three new defaults 263 to 265 recorded in the owner-review defaults file)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr018-affiliate-management/prd.md`

- **Who bears the discount**: the affiliate discount is treated like every other FR-019 discount (commission is calculated on the price after the promotion, so Hairline's commission and the provider's payout both fall in proportion to their shares). The affiliate commission itself is still deducted from Hairline's commission only. Rule 15 becomes a commission ceiling: commission percentage not above the platform default Hairline commission percentage; fixed amounts keep the review warning. Module Scope, Rules 2, 14 and 15, Assumption 4, Screens 2, 3.2 and 4 follow (REQ-018-044, REQ-018-054, REQ-018-055, REQ-018-041, REQ-018-111, REQ-018-003, REQ-018-183, REQ-018-196; cites REQ-019-016 and REQ-019-037).
- **Ceiling override**: a breach blocks the save unless the admin ticks Override and enters a required Approval reference, stored in the audit entry; nothing is disabled automatically (REQ-018-055).
- **Suspended then offboarded normally**: the Manual Review Required hold is cleared and readiness follows the stored bank details; a ban still forfeits (B5, Screen 3.3, Screen 7, Payment Rules 4 and 6, REQ-018-097, REQ-018-311, REQ-018-313).
- **Inactive affiliates**: new Payment Rule 7: an Inactive affiliate stays in the cycle list while it has unpaid commission; the next run pays the whole unpaid balance including the current month's part; later commission is paid with no $50 threshold; a refund reversal after Inactive is written off with an audit entry (REQ-018-318, REQ-018-067, REQ-018-068).
- **Completed booking**: the payment that leaves the booking fully paid (pay in full, final balance or last installment), called the final payment in the PRD (Rule 1, Payment Rule 1, Integration 2, REQ-018-309, REQ-018-043; cites REQ-007-083, REQ-007-084, REQ-007B-049).
- **Re-onboarding**: an Inactive affiliate without a ban flag does not count in the email uniqueness test; the person comes back as a new affiliate record with a new ID and zero balance; a banned email stays blocked (Screen 2, Screen 3.3, Rule 12, REQ-018-078, REQ-018-213, REQ-018-101).
- **First code failure**: the affiliate stays Active with no code, the failure and reason go to the audit panel and Screen 3, and the admin creates the code from Screen 4 with the stored settings (Main Flow step 8, Screens 3 and 4, REQ-018-307).
- **Referral credit**: "valid" means the affiliate is Active when the quote is accepted; no credit and no commission otherwise (Rule 11, REQ-018-051, REQ-018-308, REQ-018-312).
- **Referral link**: shown only with an Active Auto-apply code that is not disabled by account status; otherwise "No auto-apply code", and an old link opens the normal landing page with no attribution (Rule 11, Screens 9, 9.1 and 10.3, REQ-018-135, REQ-018-051).
- **Settlement preview**: B5 step 4 shows the settlement outcome; queue, forfeit, write off and the audit entry apply after the admin confirms (B5 steps 4 to 6, Screen 3.3, REQ-018-097).
- **Offboarding a Pending affiliate**: the activation link is invalidated and resend disabled; Screens 10.1 and 10.2 show "This activation link is no longer valid"; Permanent ban is hidden while Pending; Settlement Outcome reads "Nothing to settle" (REQ-018-152, REQ-018-156, REQ-018-087, REQ-018-317).
- **Portal states**: Screen 9.2 shows a read-only "Disabled by account status" badge and blocks copy while the marker is set; Screen 9.3 shows "Held" (Suspended) or "Final balance" (Inactive) instead of the rollover note; B3 states a Suspended affiliate can log in and view but cannot copy codes or links (REQ-018-306, REQ-018-310, REQ-018-144).
- **After reinstatement**: held commission is paid in the next run under the normal $50 threshold (Payment Rule 3).
- The change log row and Last Updated are set.

## Graph change-set

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr018-logic-p2-fixes.yaml`

- New: rule REQ-018-318; steps STP-018-140 (apply the settlement outcome), STP-018-141 (clear the hold of a Suspended affiliate), STP-018-142 (in-flight commission, B5), STP-018-143 (in-flight commission, B6); enum value nothing_to_settle on ENT-affiliate.settlement_outcome.
- B5 chain now runs 125, 140, 141, 126; the next edge STP-018-125 to STP-018-126 is removed; STP-018-129 leads to STP-018-142 and STP-018-136 to STP-018-143. Steps 006, 007 and 008 lose their on-screen edge to SCR-018-07 (system steps). The in-flight rule REQ-018-312 moves from the admin confirm steps (STP-018-125, STP-018-133) to the new system steps.
- Rule statements and some titles updated to mirror the PRD; step titles and prd_ref values, and the referral link field description, updated.
- Cross-FR edges: FR-018 now references REQ-007-083, REQ-007-084, REQ-007B-049, REQ-019-016 and REQ-019-037; the reference to REQ-007-036 is removed. No other FR's node is updated or retired.
- Test-applied on a scratch copy of the graph: 111 change rows, no errors; the copy was deleted.

## Not changed here

Neighbour changes for FR-017, FR-019, FR-020, FR-029, FR-030, FR-031 (override permission), FR-005, FR-007 and FR-007B are queued in the logic review ledger section for FR-018 pass 2 and are not part of this change. Minor observations 1, 2, 4, 6 and 7 are left as they are and listed under the ledger leftovers.
