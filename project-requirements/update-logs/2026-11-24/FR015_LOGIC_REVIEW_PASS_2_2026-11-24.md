# FR-015 Logic Review, Pass 2 (2026-11-24)

**Type**: Major update (revised PRD, version 1.29 to 1.30, with a prepared graph change-set)
**Scope**: FR-015 Provider Management (Admin-Initiated)
**Source of findings**: `plans/reports/tester-261124-fr015-logic-p2.md` (10 findings; all accepted, each a fix or an owner default)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr015-provider-management/prd.md`

- **Suspended clinic that sets its password**: Main Flow step 21 makes a provider eligible for inquiry distribution only when its status is Active and the password is set (Rules 3 and 9). Alternative Flow A1 hands a Suspended clinic back only through steps 14 to 18; it stays Suspended and read-only (FR-032 Rule 6) until reactivated (REQ-015-031).
- **Closure request on Screen 3**: the header shows a Closure request notice (request date and the provider's reason) while a request is pending, with two actions: Deactivate Provider (opens Screen 4) and Reject Request (review notes required, minimum 20 characters). No new screen (REQ-015-087, A7 steps 1 and 6).
- **Reject Request permission**: it needs the FR-031 Suspend Providers permission, the same as the deactivation it declines (permissions bullet, A7 step 6, REQ-015-069).
- **Closure rejection wording**: the edge case line now says the provider keeps its current status, as A7 does.
- **Cascade and FR-037**: suspension and deactivation also end every FR-037 monitoring assignment of the provider, as FR-037 Rule 5e (REQ-037-094) rules; stated in A5, the Deactivation line, and Screen 4 (REQ-015-017).
- **Cascade scope**: the cascade acts only on records that existed at the effective time of the status event, so anything created after a quick reactivation is never touched (A5 step 2, REQ-015-020).
- **Deactivated provider**: the Screen 3 header hides Edit Profile and all tabs are read-only; documents can still be viewed and downloaded; Tab 3 and Tab 7 keep their own rules; review actions in Tab 5 follow FR-013 (REQ-015-032).
- **Earnings on completed bookings (owner default 253)**: money earned on bookings completed normally before a suspension or deactivation is released by an admin through the FR-017 admin financial resolution route, whatever the clinic's status; while unpaid shares remain an admin may change the Payout Method of a Deactivated clinic in Tab 7 (new REQ-015-138; new Earnings Release Rule in Payment and Billing, Tab 7 edit eligibility, Dependencies FR-017 text).
- **Dependencies**: FR-017 and FR-037 entries mention the two hand-offs.
- Change log row, version and Last Updated set.

One business question took an owner default (entry 253 in the Phase 10 defaults report): earnings on normally completed bookings are released by an admin, and a Deactivated clinic's Payout Method stays editable while shares are unpaid.

## Graph change-set

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr015-logic-p2-fixes.yaml`

- New rule REQ-015-138 with stage (Suspended, Offboarded), object (`ENT-provider.payout_method`, Screen 3) and source edges.
- Updated statements: REQ-015-017, REQ-015-020, REQ-015-031, REQ-015-032, REQ-015-069, REQ-015-087; title of REQ-015-068 (the platform retention period, not 7 years); titles of STP-015-021, STP-015-171, STP-015-176; description of SCR-015-03.
- Edges: STP-015-018 to STP-015-019 now carries the condition REQ-015-031 (provider status is Active), so a Suspended clinic never reaches STP-015-021; the closure reject edge moves from STP-015-173 to STP-015-171 (no back flag) and STP-015-176 is placed on SCR-015-03; REQ-015-087 and REQ-015-032 apply to SCR-015-03.
- Cross-FR edges all start at an FR-015 node and end at an FR-037 rule (FR-015 references REQ-037-094; STP-015-152 and STP-015-174 apply it); no other FR's node is updated or retired.
- Test-applied on a scratch copy of the graph: 34 change rows, no errors; the copy was deleted. The change-set was then applied to the live graph by the controller.

## Not changed here

FR-017 (state that its admin financial resolution route also releases earnings on normally completed bookings of a Suspended or Deactivated clinic), FR-032 (REQ-032-074 and REQ-032-076 still say a rejected closure request leaves the provider Active), FR-013 (confirm review actions in Tab 5 for a Deactivated provider) and FR-031 (confirm Reject Request sits under Suspend Providers) are queued in the logic review ledger section for FR-015. FR-037 and FR-009 need no change. Minor observations (early-stage wiring, admin_id on a scheduled change, the Screen 3 allowed-actions list, the Security Considerations pointer, Resend Activation Email permission wording, the Featured toggle at creation, the Commission Start Date time zone) are listed under Leftovers in the same ledger section.
