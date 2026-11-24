# FR-031 Logic Review, Pass 2 (2026-11-24)

**Type**: Major update (revised PRD, version 1.5 to 1.6, with a graph change-set)
**Scope**: FR-031 Admin Access Control and Permissions
**Source of findings**: `plans/reports/tester-261124-fr031-logic-p2.md` (11 findings, all ruled fix), plus one item carried over from the FR-032 pass 2 review (the provider default table and a Manager's profile and notification rights)

## What changed in the PRD

File: `local-docs/project-requirements/functional-requirements/fr031-admin-access-control/prd.md`

- **Sensitive-permission warning on assignment**: the invitation flow (step 8) and the role-change flow A2 (step 7) now show the warning with the role's permission summary when the chosen role holds a sensitive permission, and the Super Admin confirms; A3 step 7 cites the same rule (REQ-031-073).
- **Role-change acknowledgement**: the affected admin sees an "Acknowledge role change" banner on the admin dashboard, on every admin page until acknowledged (not inside the Super Admin-only module); clicking it stores the time in role_change_acknowledged_at (REQ-031-124, A2 step 13).
- **Deleted account status**: deleting a suspended account sets status Deleted; it is hidden from the Admin Users list unless the Status filter "Deleted" is chosen, offers only View Audit, cannot be reactivated, and counts neither as a role holder (REQ-031-129) nor as a Super Admin (REQ-031-085). Status lists, Screen 5, Rule 7 and the Data Requirements line carry the new value (REQ-031-126, REQ-031-012).
- **Actions by account status**: Suspend on Active accounts only, Reactivate and Delete on Suspended accounts only; an Invited account is removed only with Cancel and has no Change Role action. Mirrored in A8, the Actions row and bullets of Tab 2, and the editability list (REQ-031-126).
- **Super Admin invitations**: Cancel and Resend work on an invitation for a Super Admin role until it is accepted; only Active Super Admin accounts count for the single-Super-Admin banner (A9, Rule 4, Tab 2, REQ-031-009, REQ-031-127, REQ-031-085).
- **Pending Send**: the invitation shows "Pending Send" from the first failed delivery; B4 step 4, the warning text in step 5, Edge Case 3 and the A1 trigger agree (REQ-031-043).
- **Provider role sync**: after the 3 automatic tries fail the role stays "Sync failed / not yet applied"; a Super Admin can press "Retry sync" on the Provider Roles tab (saving the matrix again also re-sends it) and every attempt is logged. New A4 step 20 and a Tab 3 note (REQ-031-130).
- **Resolve Installments**: new admin write permission in the Billing and Financial table and the admin default table (Super Admin and Billing Admin), with new rule REQ-031-135 in Core Requirements; FR-007B added to Dependencies.
- **Refunds with one holder**: a refund that needs approval stays "awaiting approval" until a second admin holds Issue Refunds; the banner text says so (REQ-031-069, REQ-031-085).
- **View and Edit Billing Settings**: the provider permission "Manage Bank Details" is renamed, in both the permission table and the provider default table (REQ-031-068, REQ-031-118).
- **Provider settings permissions**: new provider permission Edit Notification Settings (Owner and Manager by default; Edit Settings stays Owner only); the provider default table gains View Profile and Edit Profile for Owner and Manager (REQ-031-120).
- **Small wording fixes**: the audit outcome "conflict" in Edge Case 2 is now "failed"; user story 2 scenario 1 uses the matrix names "View Patients" and "View Providers".
- The status line, change log row (v1.6) and Last Updated are set.

## Graph change-set

File: `local-docs/project-requirements/graph/changesets/2026-11-24-fr031-logic-p2-fixes.yaml`

- New: rule REQ-031-135; steps STP-031-026 (warning in the invitation flow), STP-031-216 (warning in A2), STP-031-215 (acknowledgement click) and STP-031-420 (Retry sync); enum value "deleted" on ENT-admin-user-account.status.
- Edges: the four new steps carry at, done by, applies (and on, except STP-031-215); branches with the sensitive-permission condition from STP-031-007 and STP-031-207 into the new warning steps (the direct edges stay); STP-031-214 now leads through STP-031-215 to STP-031-213; STP-031-419 leads to STP-031-420; STP-031-307 applies REQ-031-073; REQ-031-135 edges.
- Removed edges: STP-031-214 next STP-031-213 (replaced by the path through STP-031-215) and STP-031-214 on SCR-031-01 (the banner belongs to the admin dashboard, no matching screen node exists, none was created).
- Rule statements updated to mirror the PRD: REQ-031-009, -012, -043, -068, -069, -085, -086, -107, -118, -120, -126, -127, -129, -130. Step titles updated: STP-031-214, -221, -227, -734. Descriptions updated on the fields password_hash, role_change_acknowledged_at and status.
- Fields: password_hash and role_effective_from are no longer required (the account exists as Invited before a password is set, and no PRD line sets the effective date at invitation).
- Cross-FR edges: none added to another FR's node and no other FR's node updated; the new step STP-031-215 is done by the shared actor ACT-platform-admin.
- Test-applied on a scratch copy of the graph: 79 change rows, no errors; the copy was deleted. The change-set was then applied to the live graph by the controller.

## Not changed here

Neighbour changes queued, no other PRD touched: FR-007B (replace the role list in REQ-007B-090 and "billing admin" in REQ-007B-081 and REQ-007B-109 with the Resolve Installments permission), FR-007 (REQ-007-015 escalation wording for a single holder and the "billing permission" wording), FR-032 (name the gating permission in each row of its who-edits-what table), FR-026 (the acknowledgement banner belongs to the admin shell), FR-030 (catalogue entry for the provider role sync-failure alert).

Business defaults recorded for the owner: 306 (Super Admin invitations), 307 (Resolve Installments), 308 (refunds with one holder), 309 (Edit Notification Settings and Manager profile rights).
