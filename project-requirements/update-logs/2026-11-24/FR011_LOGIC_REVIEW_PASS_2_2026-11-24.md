# FR-011 Logic Review, Pass 2 (2026-11-24)

**Type**: Major update (revised PRD, version 1.13 to 1.14, with a graph change-set)
**Scope**: FR-011 Aftercare and Recovery Management
**Source of findings**: `plans/reports/tester-261124-fr011-logic-p2.md` (13 findings, all ruled fixes; eight had a business decision, all taken as recommended)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr011-aftercare-recovery-management/prd.md`

- **One closing rule (REQ-011-101)**: every ending of aftercare (completed, paperwork-only completion, patient subscription cancellation once the paid period ends, admin cancellation) stops all reminders and emits the completion event with an outcome value; the booking then moves to Completed. Admins get a Cancel Aftercare control with a mandatory reason on Screen 14 Tab 4 (audited). New Business Rules section "Closing Rule"; C3, C4, D1, D4 and new D7 point at it.
- **Milestones and tasks**: time ends a milestone; a required task not done by the milestone end becomes Missed (new task status); the plan completes at the end of the last milestone; Missed counts as not done in the percentage (REQ-011-023, REQ-011-024, REQ-011-096).
- **Reminder and escalation clock**: the 2-day reminder and 4-day escalation (REQ-011-090, same two settings) also run for a paid add-on whose plan is not activated (from payment) and for a standalone request assigned to a provider who has not finished the plan (from assignment); the clock restarts at a handover or admin assignment. The add-on "unassigned after 7 days" expiry is removed; the 7-day unassigned rejection stays for standalone only (REQ-011-053, REQ-011-037, REQ-011-090).
- **Plan status**: new status Pending activation; an add-on is refused while a plan for the booking is Pending activation, Active or Completed (REQ-011-092).
- **Hairline-team delivery**: the coordinator gets Configure Plan, Propose Extension or Change, Set Urgent Flag and Clear Urgent Flag on Screen 14 Tab 4; after a handover the coordinator confirms the plan and the system activates it (A2); a change proposed by a coordinator needs a different approving admin (REQ-011-098).
- **Money**: a reassignment has no automatic refund and no refund ladder; a standalone plan refunds only by admin manual refund (REQ-007-100), a treatment-linked case reached through the FR-006 B7 decision follows FR-006 Screen 11 (REQ-006-019) (REQ-011-075, D5, Screen 19). The handover fee in the treatment-linked flow is paid from Hairline revenue; "Hairline keeps the rest of the price" stays for the add-on and standalone flows (REQ-011-040, REQ-011-057). Screen 19 gets a Reassignment Type marker (provider handover or admin reassignment).
- **Add-on template and participation**: the alternative template must carry the same price as the price already paid (REQ-011-100); aftercare participation is a provider profile yes or no setting owned by FR-015, and the original provider is assigned only when Active and participating, otherwise the Hairline team (REQ-011-054).
- **FR-038 conversions**: a converted request that ends Rejected or Expired lets the patient start a new standalone request from the same source data with a new idempotency key; the monitoring case stays final (REQ-011-093, REQ-011-094; new B5 in Workflow 2).
- **Discounts**: discount codes do not apply to aftercare in this release; the Enable Discounts row is removed from the template form.
- **Wording**: a suspended provider's case is cancelled or kept by choice (D4); Rejected versus Expired is explained on Screen 15; "response" to the 2-hour urgent escalation means clearing the flag (REQ-011-099).
- **Screen 15**: Mark Awaiting Provider Availability and Clear Awaiting Mark with an audited note.
- Change log row for version 1.14 is added; Last Updated is unchanged (same date).

## Graph change-set

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr011-logic-p2-fixes.yaml`

- New: rule REQ-011-101; steps STP-011-073 to STP-011-080 (coordinator confirms the plan, system activates it, admin cancels aftercare, coordinator proposes a change, coordinator clears the urgent flag, system rejects a standalone request unassigned after 7 days, reminder after 2 days, escalation after 4 days); field ENT-aftercare-audit-entry.reassignment_type with values provider_handover and admin_reassignment; enum values plan pending_activation and task missed.
- Updated to mirror the PRD: 18 rule statements (six with new titles), nine step titles, one flow, three events, three settings, two status descriptions.
- Edges: new next edges wire the new steps and the closing rule (STP-011-006, 045, 053, 065, 067 reach STP-011-065); REQ-011-101 applies at the five ending steps; STP-011-056 next STP-011-017 for the 48-hour expiry; back edges for the clock restart; Screen 19 shows reassignment_type; Screen 15 shows the audit reason.
- Removed edges: STP-011-027 done by the specialist and its Screen 10 edge (the step is now the coordinator on Screen 14); SCR-011-16 shows the discounts field. The discounts field node is retired.
- Cross-FR edges: FR-011 references REQ-007-100 and REQ-006-019 (edges only). No other FR's node is updated or retired.
- Test-applied on a scratch copy of the graph: 176 change rows, no errors; the copy was deleted. The change-set was then applied to the live graph by the controller.

## Not changed here

Neighbour changes are queued, not edited: FR-006 (read the completion outcome), FR-015 (aftercare participation field and its screen row), FR-038 (new standalone request after Rejected or Expired), FR-030 (notices for the new endings), FR-007 and FR-017 (handover fee paid from Hairline revenue in the treatment-linked flow). Leftovers: the entry point from Screen 1 to Screen 7 for Cancel Subscription, whether a submitted review can complete the booking in FR-006 (REQ-006-060), and the early platform stage pin of STP-011-062, STP-011-001 and REQ-011-014.
