# Change Request: Admin Staff Invite from Provider View and Limited-Write Impersonation

**Change Request ID**: CR-FR009-20261015-01
**Primary FR**: FR-009
**Triggering FR / Event**: FR-015 fifth verification pass (2026-10-15) found that FR-009 described admin impersonation as read-only while FR-015 "Login as Provider" allows limited write actions, and that FR-015 Tab 3: Staff List needed a single-provider team view with an admin "Invite Staff Member" action that FR-009 did not define
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-15
**Decision Date**: 2026-10-15
**PRD Version Change**: v1.3 (proposed) to v1.4 (proposed)
**Related Commit(s)**: Pending — no commit requested for this change

---

## Decision Summary

FR-009 Screens 10 and 11 offered "Impersonate (Read-Only)", disabling all write actions, while FR-015 Screen 3 "Login as Provider" lets a Super Admin act on the provider's behalf with specific exclusions. FR-009 also had only a cross-provider admin directory (Screen 10), with no admin invite path, while FR-015 Tab 3: Staff List is a single-provider view.

The Product Owner chose: (1) the FR-015 rule wins; FR-009 impersonation is limited-write and follows the FR-015 "Login as Provider" rules; (2) admins can invite staff from a per-provider team view embedded in FR-015 Tab 3, using FR-009's normal invitation flow.

## Baseline State

**Source version**: FR-009 v1.3 (proposed), Screen 10 Actions, Screen 11 Access Control, Admin Actions and Business Rules, REQ-009-001 to REQ-009-022

- Impersonation was read-only: all write actions disabled, banner "Viewing as [Name] - Read-Only Admin Mode."
- No admin single-provider team view; Screen 10 listed members across all providers.
- No admin-initiated invitation; only Owners and authorized Manager-base users could invite.

## Approved State

**Target version**: [FR-009 v1.4 (proposed)](prd.md), Screens 10-12, Admin Editability Rules, FR-015 dependency, REQ-009-023 to REQ-009-025

- Impersonate follows the FR-015 "Login as Provider" rules (FR-015 is the owner): Super Admin only; reason (min 20 chars) and password re-authentication (MFA later); persistent banner "You are viewing as [Name] — admin session by [Admin Name]" with End Session; admin may act on the user's behalf except changing password, login email, or payout/bank/financial settings; session start/end and every write action logged and attributed to the admin; automatic end after 30 minutes of inactivity.
- New **Screen 12: Provider Team (Admin, Single Provider)**, embedded in FR-015 Screen 3 Tab 3: Staff List, lists the provider's members (name, email, role, ownership flag, status, last login) and offers Invite Staff Member.
- Admin invite: email plus one of the provider's non-Owner roles; normal FR-009 invitation email, acceptance flow, and expiry; blocked at the provider's Seat Limit (FR-015) or when the provider is Suspended or Deactivated; requires FR-031 "Edit Providers"; logged in the FR-009 audit trail and FR-015 Tab 8 with the inviting admin. Ownership transfer stays in FR-009's existing flow.
- Existing row actions (force suspend, reset invitation, view audit log, impersonate) remain available.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Admin impersonation | Read-only; all writes disabled | Limited write per FR-015 "Login as Provider" rules | Product Owner decision; FR-015 rule wins |
| Impersonation banner | "Viewing as [Name] - Read-Only Admin Mode." | "You are viewing as [Name] — admin session by [Admin Name]" with End Session | Align with FR-015 |
| Admin per-provider team view | Not defined | Screen 12, embedded in FR-015 Tab 3 | FR-015 Tab 3 shows only that provider's team |
| Admin invitation | Not allowed | Allowed with FR-031 "Edit Providers", non-Owner roles only, Seat Limit and provider status checks | Product Owner decision |
| Audit | FR-009 audit trail | FR-009 audit trail plus FR-015 Tab 8 for admin invites and impersonation activity | Traceability of admin actions |
| Requirements | REQ-009-001 to 022 | Added REQ-009-023 to REQ-009-025 | Make the rules testable |

## Scope and Impact

### In Scope

- FR-009 Screens 10 and 11 impersonation wording, new Screen 12, Admin Editability Rules, FR-015 dependency note, REQ-009-023 to REQ-009-025, and the PRD change log row.
- This FR-local Change Request.

### Out of Scope

- Provider-side invitation, role change, and removal flows (unchanged).
- Ownership transfer rules (unchanged).
- MFA re-authentication (remains a future enhancement).
- System PRD, technical specification, and data schema updates.
- Source code, API, or live configuration changes.

### Affected Contracts

- **PRD owner**: [FR-009](prd.md) — Screens 10-12, Admin Editability Rules, Dependencies (FR-015), REQ-009-023 to REQ-009-025.
- **Related FRs**: [FR-015](../fr015-provider-management/prd.md) v1.13 Screen 3 "Login as Provider" rules (owner of impersonation rules), Tab 1 Seat Limit, Tab 3: Staff List (embeds Screen 12), Tab 8: Activity Log. [FR-031](../fr031-admin-access-control/prd.md) "Edit Providers" permission and provider role definitions.
- **System documents**: Unchanged.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed; no source code or runtime behavior was inspected or changed.
- **Required assessment**: Impersonation session handling (write enablement with blocked password, login email, and payout/bank/financial changes; banner; inactivity timeout; per-action audit attribution), admin invitation endpoint and permission check, Seat Limit and provider status checks on admin invites, Tab 3 single-provider team listing, and audit entries in FR-009 and FR-015 Tab 8.
- **Compatibility / rollout risk**: Any existing read-only impersonation implementation must be widened carefully; the excluded actions must be blocked server-side, not only hidden in the UI.
- **Data migration**: None expected; invitation records may need to identify an admin as the sender.

## Acceptance and Validation

- A non-Super Admin cannot start impersonation; a Super Admin must enter a reason of at least 20 characters and re-enter their password.
- During impersonation, the banner and End Session are visible; ordinary write actions succeed and are logged with the admin as actor; changing password, login email, or payout/bank/financial settings is blocked.
- An idle impersonation session ends after 30 minutes.
- In FR-015 Tab 3, only the selected provider's members appear; an admin with "Edit Providers" can invite an email with a non-Owner role, and the invitee receives the normal invitation email with the normal expiry.
- Owner is not offered as a role; invite is blocked at the Seat Limit and for Suspended or Deactivated providers; admins without "Edit Providers" cannot invite.
- Each admin invitation appears in the FR-009 audit trail and FR-015 Tab 8 with the inviting admin.

## Approval and Traceability

- **Requested by**: Product Owner, Joachim Trung Tuan, during FR-015 verification review.
- **Approved by**: Product Owner, Joachim Trung Tuan, 2026-10-15; FR-009 documentation delta only.
- **Decision evidence**: FR-015 fifth verification pass AskUserQuestion answers (impersonation follows FR-015 limited-write rules; admins can invite staff from the per-provider view), confirmed with "Yes".
- **PRD change log**: [FR-009 Appendix: Change Log](prd.md#appendix-change-log), v1.4 (proposed) dated 2026-10-15.
- **Update log**: [FR015_FIFTH_VERIFICATION_FIXES_2026-10-15.md](../../update-logs/2026-10-15/FR015_FIFTH_VERIFICATION_FIXES_2026-10-15.md).
- **Supersedes**: None.
- **Superseded by**: None.
