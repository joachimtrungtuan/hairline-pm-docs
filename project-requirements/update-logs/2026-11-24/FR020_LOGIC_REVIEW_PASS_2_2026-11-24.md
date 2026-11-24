# FR-020 Logic Review Pass 2 (2026-11-24)

**Scope**: FR-020 Notifications and Alerts, PRD v2.17 to v2.18. Pass 2 (the last pass) of the logic review; 15 findings, 14 fixed in FR-020, 1 deferred to the backlog (P2-13, SMS is post-MVP), with the changes to other FRs queued.
**Evidence**: reviewer report `plans/reports/tester-261124-fr020-logic-p2.md`; fixer report `plans/reports/docs-manager-261124-fr020-logic-p2-fixes.md`.
**Graph**: the change-set `local-docs/project-requirements/graph/changesets/2026-11-24-fr020-logic-p2-fixes.yaml` is prepared and NOT applied (the controller applies it). The pass 1 change-set is already applied to the live graph.
**Owner defaults**: entry 99 (an Admin Close inquiry sends no provider notice) and entry 100 (`dsr.fulfilled` by email to the captured address, address deleted after a final failure) in `plans/reports/owner-review-261123-1308-phase-10-defaults-applied.md`.

## Changes to the PRD

- Provider-caused cancellation notice: the three pre-acceptance variants are chosen in a stated order (other live offers remain; no live offer and an explicit selection, the confirm variant; no live offer and no explicit selection, the redistribution variant) (`provider.status_cancellation_patient` row, REQ-020-013).
- Redistribution reminder: not sent, and a pending one dropped, when the redistribution no longer awaits the patient's confirmation (REQ-020-159).
- `booking.cancelled` causes follow FR-006: Admin cancellation, provider drop-out at the Screen 10 submit, system cancellation for an unpaid balance including an FR-007B plan default; "patient drop-out" deleted; a suspension or deactivation closure sends `booking.provider_fault_replacement` and not `booking.cancelled` (REQ-020-092).
- `inquiry.cancelled` has a second variant for an Admin close: closed by Hairline, the reason as FR-006 defines, no replacement will follow, Contact Admin/Support action. A deletion cancellation sends the patient no `inquiry.cancelled` (REQ-020-076).
- `quote.cancelled_inquiry`: an Admin close is no longer a trigger; the system cancellation at the approval of an account deletion (FR-023 REQ-023-042) is, with no reason shown (REQ-020-020).
- Alternative Flow B2: a notice counts as complete when its first attempt is handed to a channel or it has ended `failed` after the last retry (REQ-020-040).
- `dsr.fulfilled`: email only, to the contact address FR-023 captured, critical, no in-app record; after a final failure the captured address is deleted and the Admin sees the failure in the delivery log (REQ-020-161).
- Alternative Flow A1: every patient notice creates the in-app record whatever the channel toggles; `suppressed` describes the email and push attempts only (REQ-020-038).
- REQ-020-071 and User Story 4 scenario 1: a first send attempt within 5 minutes on both email and push, with the patient's own cancellation reason.
- Consolidated Screen Notes: on the provider and admin surfaces a link to an archived notice opens the notification dropdown with the "no longer available" message (REQ-020-068).
- Not changed: P2-13 (the meaning of "urgent" for the post-MVP SMS gate) is deferred to the backlog.

## Graph change-set (prepared, not applied)

- 36 operations (37 change rows): 11 node updates (10 rules and step STP-020-008, retitled with a new description), 10 edge removals and 15 edge additions; no node, field or enum value added.
- Rules REQ-020-036, -038, -039, -040, -041, -042, -043 and -046 move from STG-main-01-inquiry to STG-platform-01-all-stages; REQ-020-041 also applies to ENT-notification-record; REQ-020-076 applies at STG-main-02-quote and STG-main-04-booking.
- Steps 006 and 007 gain a `next` edge to step 004 (recorded as suppressed or coalesced); the edges 006 to 003 and 008 to 004 keep their ends with fuller labels.
- Test-applied on a scratch copy of the graph: applied cleanly; the copy was deleted. No node of another FR is touched.

## Cross-FR rows queued

FR-006 (UnpaidBalance mapping, drop-out event overlap, Close inquiry notice pointer), FR-003 and FR-004 (carve-outs for the replacement provider), FR-030 (catalogue rows, event descriptions, `emits` edge), FR-023 (REQ-023-042 and REQ-023-033); see the pass 2 section of `plans/reports/logic-review-ledger.md`.
