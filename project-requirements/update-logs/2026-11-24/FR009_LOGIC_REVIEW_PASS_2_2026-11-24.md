# FR-009 Logic Review, Pass 2 (2026-11-24)

**Type**: Major update (revised PRD, version 1.12 to 1.13 proposed, with a graph change-set)
**Scope**: FR-009 Provider Team and Role Management
**Source of findings**: `plans/reports/tester-261124-fr009-logic-p2.md` (17 findings, all ruled fixes; five carried a business decision, taken as recommended and recorded as defaults 236 to 240)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr009-provider-team-roles/prd.md`

- **Moving between clinics**: a move is the old clinic removing the member (membership archived, email free), then the new clinic sending a new invitation. There is no admin transfer flow. The duplicate-email error now tells the inviting clinic to ask the other clinic to remove the person or contact Hairline support (Rule 3, A3, US4, REQ-009-189, REQ-009-049).
- **Removed members**: a Removed member's email is free for any provider; accepting an invitation always creates a new team member record and an archived record stays archived; the login-only branch reuses the person's existing login. The duplicate check (B2) counts only Active and Suspended members and Pending invitations (Rules 3 and 9, main flow step 16, REQ-009-008, REQ-009-045, REQ-009-051, REQ-009-150).
- **Removed filter**: Screen 1 gets a Removed status value for the Owner only, listing name, role, removal date and reason and opening Screen 6 read-only. A Removed member's logs follow Privacy Rule 4 (Screen 1, Screen 6, Privacy Rules 2 and 4, REQ-009-093, REQ-009-155, REQ-009-157).
- **Archive unassigned**: the option is gone from the Remove flow, REQ-009-068, REQ-009-080 and the Screen 4 rule. A7 stays the only no-open-items path.
- **Owner record**: the Owner's team member record is created with the provider account (FR-015), the stated exception to "created only when an invitation is accepted" (Rule 9, REQ-009-009, the team member entity description).
- **Manager role limit** (default 236): a Manager's New Role list holds only Clinical Staff and Billing Staff, so only the Owner creates Managers (role change flow, Screen 3, REQ-009-004, REQ-009-063).
- **Suspend and replacement clinician**: A9 now lists the open items and asks for a replacement clinician before the Suspended state is set, reusing the Remove flow steps; Reactivate does not give the items back (A9, Rule 12, REQ-009-191).
- **Admin acts on a team member** (default 237): one admin flow with four steps: force suspend (recorded as set by the platform), Reactivate, Force remove, and Delete account through a "Remove and anonymize personal data" control on Screen 11 that needs a support case reference. Force suspend and Force remove need a named replacement clinician first. Force remove is added to the Screen 10 and Screen 12 Actions columns (REQ-009-159, REQ-009-161, REQ-009-162, REQ-009-165, REQ-009-117, REQ-009-145).
- **Platform suspension** (default 238): while a suspension was set by Hairline, the clinic sees no Remove either; only a Hairline admin can lift the suspension or remove the member (Rule 13, Screen 1, REQ-009-192, REQ-009-090).
- **Resend**: A2 covers a Pending invitation as well as an Expired one; the seat check is for Expired only; a Pending resend replaces the link and gives a fresh 7 days with no seat change (A2, REQ-009-048, step title of the seat check).
- **Invitation page messages**: Expired shows "This invitation has expired. Ask your clinic to send a new one."; Cancelled shows "This invitation is no longer valid." (Screen 7, main flow step 13, REQ-009-043).
- **Suspended login**: a Suspended member's login is refused with a message that names the clinic owner or Hairline support, from who set the suspension (A9 step 5, Rule 13, new REQ-009-197).
- **Role change that removes rights** (default 239): the Change Role dialog requires a replacement clinician for the member's open items before saving (role change flow step 8, Screen 3, Rule 12, REQ-009-191).
- **Owner handover and provider status** (default 240): allowed while the provider is Suspended, unavailable while it is Deactivated (Rule 11, Screen 12, REQ-009-174).
- **Handover permissions**: admin handover step 2 states that the new permissions apply to active sessions (REQ-009-057).
- **Deactivated provider**: new A10 states the system cancels every Pending invitation (REQ-009-194).
- **Task Transfer Wizard**: Remove flow step 5 opens Screen 5 above 10 open items; the wizard collects one replacement per workload type and moves nothing; step 9 applies the choices; the Screen 5 line now says "Transfers are applied when you confirm the removal." (REQ-009-084, REQ-009-085, REQ-009-086).
- **Two minor fixes**: main flow step 15 lists the phone number; Remove flow step 4 says the list is filtered by role compatibility.
- Change log row for version 1.13 is added; Last Updated is set to 2026-11-24.

## Graph change-set

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr009-logic-p2-fixes.yaml`

- New: rule REQ-009-197; steps STP-009-082 to STP-009-090; flows FLW-009-admin-member-actions and FLW-009-deactivated-provider-cancels-invitations.
- Updated to mirror the PRD: 28 rule statements, 5 step titles, the team member entity description. No node is retired.
- Edges: rule wiring for REQ-009-197; the new steps with their stage, actor, screen, rule and next edges; branches from the role change, suspend, Remove and A2 steps; STP-009-040 applies REQ-009-004; STP-009-080 applies REQ-009-057; ACT-provider uses SCR-009-06; REQ-009-192 and REQ-009-162 apply to the admin screens; REQ-009-157 applies to Screens 1 and 6; Screen 1 shows the removal reason and the removal date.
- Removed edges: none.
- Cross-FR edges: none.
- Test-applied on a scratch copy of the graph: 180 change rows, no errors, every FR-009 step reachable from a flow; the copy was deleted and the real graph was not touched.

## Not changed here

Neighbour changes for FR-004 and FR-010 (clinician lists rewritten also on suspension, role change and admin actions), FR-015 (Owner login email controls, handover not while Deactivated, the deactivation trigger for REQ-009-194, Removed email free), FR-030 and FR-020 (events and notices for Reactivate, Cancel Invitation and Owner handover) and FR-031 (Manager role-change row) are queued in the logic review ledger section for FR-009, not applied. Minor observations not fixed are listed there as leftovers.
