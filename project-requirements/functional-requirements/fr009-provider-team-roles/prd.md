# FR-009 - Provider Team & Role Management

**Module**: PR-01: Auth & Team Management
**Feature Branch**: `fr009-provider-team-roles`
**Created**: 2025-11-11
**Status**: Proposed revision (v1.12); prior v1.2 document marked Verified & Approved
**Source**: FR-009 from system-prd.md

---

## Executive Summary

The Provider Team & Role Management feature enables multi-user collaboration within provider organizations by allowing clinic owners to invite team members, assign role-based permissions, and manage access to the Hairline platform. This feature is essential for medium to large clinics where multiple staff members need to collaborate on patient inquiries, quote creation, treatment execution, and aftercare management while maintaining appropriate access controls and audit trails.

**Business Value**: Enables provider organizations to operate efficiently with multiple staff members, reduces bottlenecks by distributing workload, improves response times to patient inquiries, and maintains security through role-based access control.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-XX)**: No direct patient-facing functionality
- **Provider Platform (PR-01)**: Complete team management interface, role assignment, permission controls, team member invitations, activity audit logs (REQ-009-029)
- **Admin Platform (A-01)**: Oversight of all provider teams, ability to view team structures, audit team member activities across providers, manage suspended accounts (REQ-009-027)
- **Shared Services (S-03, S-06)**: S-03 Notification Service for team member invitations and management emails; S-06 Audit Log Service for immutable recording of team management actions (REQ-009-030)

### Multi-Tenant Breakdown

**Patient Platform (P-XX)**:

- No functionality in patient app
- Patients may see team member names/roles in communications (e.g., "Dr. Sarah responded to your inquiry") (REQ-009-026)

**Provider Platform (PR-01)**:

- Team dashboard showing all active team members with roles (REQ-009-029)
- Invite team member flow with email invitation (REQ-009-029)
- Role assignment and modification interface (REQ-009-029)
- Permission management screen (REQ-009-029)
- Team member removal/suspension capability (REQ-009-029)
- Activity log viewer showing team member actions (REQ-009-029)
- Profile management for each team member (REQ-009-029)

**Admin Platform (A-01)**:

- System-wide view of all provider teams (REQ-009-027)
- Ability to view team composition for any provider (REQ-009-027)
- Audit log access for compliance investigations (REQ-009-027)
- Capability to suspend individual team members or entire teams (REQ-009-027)
- Analytics on team sizes, role distribution across platform (REQ-009-028)
- Override capability for emergency access removal (REQ-009-027)

**Shared Services (S-03, S-06)**:

- S-03: Notification Service sends invitation and team-management emails with secure signup links (REQ-009-030)
- Provider Auth Service (PR-01) handles team member account creation, login, password reset, and session management while enforcing PR-01/FR-031 permission checks (REQ-009-030)
- S-06: Audit Log Service records all team management actions for compliance (REQ-009-030)

### Provider Role Model

The provider platform starts with four protected clinic-side roles that directly reflect how real clinics operate, while keeping clear separation from Hairline's own Admin Platform roles. There are no custom provider roles. (REQ-009-002)

- **Owner (Main Account Holder)**: Single primary account per provider organization. Responsible for bank details and payouts, contract acceptance, and high-risk configuration. Mapped to the "provider admin / main account holder" described in the client transcription. (REQ-009-031)
- **Manager (Clinic Manager / Operations)**: Operational lead and front-of-staff representative. Can see and manage the full patient journey in the provider portal (inquiries, quotes, schedules, day-to-day operations), coordinate staff work, and manage most team settings, but cannot change bank details or assign/change the Owner role. (REQ-009-032)
- **Clinical Staff**: Medical staff who perform procedures and aftercare (surgeons, clinicians, nurses). Focused on in-progress and aftercare sections, treatment documentation, scans, and medical notes. **Default**: limited or no access to billing or sensitive configuration (final per-feature permissions are configured centrally in FR-031 and may deviate from this default). (REQ-009-033)
- **Billing Staff**: Finance-oriented staff who work with quotes and payouts ("how much they're making"). Can view and reconcile financial information but cannot alter clinical records or manage team structure or assign/change the Owner role. (REQ-009-034)

### Communication Structure

**In Scope**:

- Email invitations to new team members with secure signup link (REQ-009-035)
- Email notifications when team member role changes (REQ-009-035)
- Email notifications when team member is removed, suspended, or reactivated (REQ-009-035)
- In-platform notifications for team management events (REQ-009-035)
- These notices (invitation, accepted, role changed, removed, suspended, reactivated, Owner handover, invitation delivery failure) need matching entries in the FR-030 notification catalogue (REQ-009-007)

**Out of Scope**:

- SMS notifications for team management (handled by S-03: Notification Service if needed; **no SMS is sent in MVP and this channel is reserved for future phases**) (REQ-009-036)
- Video tutorials for team onboarding (handled by separate content module) (REQ-009-036)
- Chat/messaging between team members (separate collaboration feature) (REQ-009-036)

### Entry Points

- **Provider Owner**: Accesses team management from provider dashboard main navigation ("Team" tab) (REQ-009-037)
- **Provider Manager**: Accesses operational team management features from settings menu (within the Manager permissions defined in FR-031) (REQ-009-037)
- **New Team Member**: Receives email invitation with signup link, creates account, automatically assigned to provider organization with specified role (REQ-009-037)
- **Admin Platform**: System administrators access team management oversight from admin dashboard provider detail view (REQ-009-037)

---

## Business Workflows

### Main Flow: Invite Team Member

**Actors**: Provider Owner or Manager, System, New Team Member (invitee)
**Trigger**: Provider Owner or Manager clicks "Invite Team Member" button in team management dashboard
**Outcome**: Team member receives invitation email, creates account, gains access to provider platform with assigned role

**Steps**:

1. Provider Owner or Manager navigates to team management dashboard
2. System displays current team members with their roles and status
3. Provider Owner or Manager clicks "Invite Team Member" button
4. System presents invitation form with fields: email address, first name, last name, role selection
5. Provider Owner or Manager enters team member details and selects a non-Owner role. The Owner can choose Manager, Clinical Staff, or Billing Staff; for a Manager the form lists only Clinical Staff and Billing Staff. Owner is not assignable from this flow and is reserved for the single primary account holder. (REQ-009-038)
6. System validates email format and checks for duplicate email within organization. The invitation is blocked while the provider organization is Suspended, because the Team page is view-only for a Suspended provider (Rule 10) (REQ-009-039)
7. Provider Owner or Manager reviews invitation details and clicks "Send Invitation"
8. System generates secure invitation token (expires in 7 days) (REQ-009-016)
9. System sends email to invitee with invitation link, provider organization name, and role being offered (REQ-009-040)
10. System creates an invitation record with status "Pending". No team member record exists yet; the team list shows the pending invitation with the "Invited" badge (REQ-009-041)
11. System displays confirmation message to the Provider Owner or Manager who sent the invitation (REQ-009-042)
12. New Team Member receives email and clicks invitation link
13. System validates invitation token (not expired, not already used) (REQ-009-043)
14. System presents account creation form pre-filled with email, first name, last name (REQ-009-044)
15. New Team Member sets password and accepts terms of service (REQ-009-045)
16. System creates the team member record (status Active) and links it to the provider organization with the assigned role. This is the first point at which the invitee becomes a team member (REQ-009-045)
17. System marks invitation as "Accepted" (REQ-009-045)
18. System sends confirmation email to both Provider Owner and new team member (REQ-009-046)
19. System logs all actions in audit trail (REQ-009-013)
20. New Team Member can immediately log in with new credentials (REQ-009-047)

### Alternative Flows

**A2: Reinvite expired invitation**:

- **Trigger**: Invitation token expired (7 days passed) and team member hasn't signed up
- **Steps**:
  1. Provider Owner views pending invitations list
  2. System shows invitation status as "Expired"
  3. Provider Owner clicks "Resend Invitation" button
  4. System checks that a seat is free. When none is free, the resend is blocked with the Screen 2 seat limit message and the invitation stays Expired (REQ-009-048)
  5. System generates new invitation token and sends new email (REQ-009-048)
  6. Old invitation token invalidated (REQ-009-048)
- **Outcome**: Team member receives fresh invitation with new 7-day expiry (REQ-009-048)

**A3: Team member already has account (different provider)**:

- **Trigger**: Invitee email address already belongs to another provider organization as Owner, team member, or pending invitation (global provider email identity rule, REQ-009-008). Memberships and pending invitations of a Deactivated provider (FR-015) do not count (REQ-009-049)
- **Steps**:
  1. System detects existing membership during invitation validation (REQ-009-049)
  2. System displays blocking error: "This email already belongs to another provider team. Remove the member from their current provider team before inviting them here." (REQ-009-049)
- **Outcome**: Cross-provider duplication prevented; invitee must first be removed from their current provider team before they can be invited here (REQ-009-049)

**B1: Invalid email address**:

- **Trigger**: Provider Owner enters malformed email address
- **Steps**:
  1. System validates email format on blur or submit (REQ-009-050)
  2. System displays inline error message: "Please enter a valid email address" (REQ-009-050)
  3. Provider Owner corrects email (REQ-009-050)
  4. System re-validates and allows submission (REQ-009-050)
- **Outcome**: Only valid email addresses accepted (REQ-009-050)

**B2: Duplicate email within same organization**:

- **Trigger**: Provider Owner invites email that already exists as team member or pending invitation
- **Steps**:
  1. System checks email against existing team members and pending invitations (REQ-009-051)
  2. System displays error: "This email is already part of your team" (REQ-009-051)
  3. System suggests: "View team member" or "Resend invitation" if pending (REQ-009-051)
  4. Provider Owner either cancels or takes suggested action (REQ-009-051)
- **Outcome**: Duplicate prevented, existing record maintained (REQ-009-051)

**B3: Invitation link already used**:

- **Trigger**: Team member clicks invitation link that was already accepted
- **Steps**:
  1. System detects invitation status is "Accepted"
  2. System displays message: "This invitation has already been used. Please log in with your existing credentials." (REQ-009-053)
  3. System provides login link (REQ-009-053)
- **Outcome**: Prevents duplicate account creation

**B4: Network error during invitation send**:

- **Trigger**: Email service fails to send invitation
- **Steps**:
  1. System attempts to send invitation email
  2. Email service returns error
  3. System logs the error and retries sending under the FR-030 notification retry rule (REQ-009-054)
  4. If all retries fail, the invitation stays Pending and the system sets its delivery state to "Pending Send". "Pending Send" is a delivery state, not an invitation status, and the invitation takes a seat while it is Pending (Rule 6) (REQ-009-054)
  5. System displays warning to Provider Owner: "Invitation created but email failed. We'll retry automatically." (REQ-009-054)
  6. If sending still fails when the FR-030 retry rule is exhausted, system alerts admin team (REQ-009-055)
- **Outcome**: Invitation record created, email eventually delivered or admin intervenes (REQ-009-054)

**A8: Cancel a pending invitation**:

- **Trigger**: Provider Owner or Manager clicks "Cancel Invitation" on a Pending invitation row. A Manager can cancel only invitations for Clinical Staff and Billing Staff, the same limit as for removal (REQ-009-193)
- **Steps**:
  1. Provider Owner or Manager clicks "Cancel Invitation" (REQ-009-193)
  2. System invalidates the token, sets the invitation status to "Cancelled", frees the seat, and logs the cancellation in the audit trail (REQ-009-193)
- **Outcome**: The invitation can no longer be accepted, and the person can be invited again (REQ-009-193)

---

### Main Flow: Change Team Member Role

**Actors**: Provider Owner or Manager with role-edit permission, System, Affected Team Member
**Trigger**: Authorized actor clicks "Edit" on team member row in team dashboard
**Outcome**: Team member's role and permissions updated, team member notified

**Steps**:

1. Authorized provider actor views team management dashboard
2. System displays list of team members with current roles
3. Authorized actor clicks "Edit" button next to team member name (Owner rows show locked badge and no edit action)
4. System presents role selection dropdown with current role pre-selected
5. Authorized actor selects a non-Owner role from the dropdown (Owner role is read-only and cannot be reassigned in this module)
6. System displays permission comparison: "Current permissions" vs "New permissions" (REQ-009-056)
7. Authorized actor reviews changes and clicks "Update Role"
8. System validates actor has permission to assign selected role (REQ-009-015)
9. System updates team member's role in database (REQ-009-057)
10. System immediately applies new permissions to any active sessions (REQ-009-057)
11. System sends email to affected team member: "Your role has been changed to [Role]" (REQ-009-058)
12. System logs role change in audit trail with timestamp, actor, old role, new role (REQ-009-013)
13. System displays success confirmation
14. Affected team member's next page load reflects new permissions (REQ-009-057)

### Alternative Flows

**A4: Attempt to modify Owner role via provider UI**:

- **Trigger**: Any provider user (Owner or Manager) attempts to modify the Owner's role from the provider platform
- **Steps**:
  1. System detects target role is Owner (single primary account holder)
  2. System displays error: "The primary Owner role is fixed and cannot be changed." (REQ-009-065)
  3. Edit dialog closes without making changes
- **Outcome**: Owner role remains unchanged; no provider-facing workflow can reassign the primary Owner role (REQ-009-065)

**B5: Team member currently performing critical action**:

- **Trigger**: Role change attempted while team member is mid-transaction (e.g., submitting quote)
- **Steps**:
  1. System updates role in database (REQ-009-066)
  2. System allows in-progress action to complete with old permissions (REQ-009-066)
  3. Next action uses new permissions (REQ-009-066)
  4. System logs that in-flight action completed with previous permission set (REQ-009-066)
- **Outcome**: No transaction interruption, clean permission transition

---

### Main Flow: Remove Team Member

**Actors**: Provider Owner or Manager, System, Removed Team Member
**Trigger**: Provider Owner or Manager clicks "Remove" on team member row. The Owner can remove any non-Owner member; a Manager can remove only Clinical Staff and Billing Staff (REQ-009-005)
**Outcome**: Team member's access revoked, open items handed to a replacement clinician or archived, team member notified

**Steps**:

1. Provider Owner or Manager clicks "Remove" button next to team member name
2. System presents confirmation dialog with warning about handing over open items (REQ-009-067)
3. System displays the open items that name the team member as responsible clinician (REQ-009-067, REQ-009-191):
   - Draft quotes in progress (REQ-009-067)
   - Open treatment records (REQ-009-067)
   - Upcoming scheduled appointments (REQ-009-067)
4. System prompts: "Replacement clinician:" with dropdown of remaining team members (REQ-009-067)
5. Provider Owner or Manager selects the replacement clinician. "Archive unassigned" is offered only when the team member has no open items; otherwise a replacement clinician must be chosen (REQ-009-068)
6. Provider Owner or Manager confirms removal
7. System validates actor has permission to remove target team member: the Owner may remove any non-Owner member, a Manager only Clinical Staff and Billing Staff (REQ-009-015, REQ-009-005)
8. System immediately revokes all active sessions for removed team member (REQ-009-069)
9. System replaces the removed member with the selected replacement clinician as responsible clinician on the open items (REQ-009-070)
10. System archives team member's historical records (maintains for audit) (REQ-009-071)
11. System sends email to removed team member: "Your access to [Provider Name] has been removed" (REQ-009-072)
12. System logs removal in audit trail with the removal reason (required) (REQ-009-073)
13. System displays success confirmation
14. Removed team member's next login attempt shows: "You no longer have access to this organization. Contact your clinic owner if you believe this is an error." (REQ-009-074)

### Alternative Flows

**A6: Self-removal by Owner**:

- **Trigger**: Provider Owner attempts to remove themselves
- **Steps**:
  1. System detects actor is removing themselves (REQ-009-075)
  2. System immediately blocks request with error: "Owners cannot remove their own accounts." (REQ-009-075)
  3. Error is logged in audit trail for compliance (REQ-009-075)
- **Outcome**: Self-removal is blocked (REQ-009-075)

**A7: Remove team member with no active work**:

- **Trigger**: Team member being removed is the responsible clinician on no open quotes, treatment records, or appointments
- **Steps**:
  1. System detects no open items (REQ-009-076)
  2. System skips the replacement clinician step (REQ-009-076)
  3. Removal proceeds immediately after confirmation (REQ-009-076)
- **Outcome**: Simplified flow for inactive team members (REQ-009-076)

**B6: Removal does not affect clinic conversations**:

- **Trigger**: Removed team member took part in patient message threads
- **Steps**:
  1. System leaves the clinic's patient conversations unchanged: each conversation belongs to the clinic (one conversation per patient and provider, FR-012), so no routing changes and no patient message is sent (REQ-009-077)
- **Outcome**: Patient conversations continue with the clinic (REQ-009-077)

**A9: Suspend or reactivate a team member**:

- **Trigger**: Provider Owner or Manager clicks "Suspend" on an Active member row or "Reactivate" on a Suspended member row (Screens 1 and 6). The Owner can act on any non-Owner member; a Manager only on Clinical Staff and Billing Staff (REQ-009-192)
- **Steps**:
  1. Provider Owner or Manager clicks "Suspend" or "Reactivate". Suspend opens the Screen 4 modal with the final state Suspended (REQ-009-082, REQ-009-192)
  2. System sets the member to Suspended (recording that the clinic set it, revoking all active sessions) or back to Active, emails the member, and logs the change in the audit trail (REQ-009-082, REQ-009-192)
- **Outcome**: The member is suspended or reactivated. A suspension set by Hairline can be lifted only by a Hairline admin, so the clinic sees no "Reactivate" on it (REQ-009-192)

### Admin Flow: Hand Over the Owner Role

**Actors**: Hairline admin, System, new Owner, previous Owner
**Trigger**: Hairline admin clicks "Hand over Owner role" on Screen 12
**Outcome**: The new Owner holds the Owner role, the previous Owner is a Manager, both are notified (Rule 11, REQ-009-174)

**Steps**:

1. Hairline admin clicks "Hand over Owner role", picks an active team member of that provider, enters a required reason, and confirms (REQ-009-174)
2. System makes the picked member the Owner and the previous Owner a Manager, and sets the provider record's Owner login email to the new Owner's email (REQ-009-174, REQ-009-196)
3. System logs the handover in the FR-009 audit trail and FR-015 Tab 8: Activity Log with the admin as actor, and emails the new and the previous Owner (REQ-009-174)

---

## Screen Specifications

### Provider Platform (PR-01)

#### Screen 1: Team Management Dashboard

**Purpose**: Central interface for viewing all team members, their roles, status, quota usage, and available actions.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Team Member Name | Display (text) | N/A | Full name of team member | Display only | ENT-team-member.first_name, ENT-team-member.last_name |
| Email | Display (email) | N/A | Team member's email address | Display only | ENT-team-member.email |
| Role | Display (badge/tag) | N/A | Current provider role | Display only | ENT-team-member-org-role.role_id |
| Role Lock Indicator | Icon | N/A | Shows lock icon for Owner rows (non-editable) | Display only | no graph field (control) |
| Status | Display (badge) | N/A | Team member status Active or Suspended, with who set a suspension (clinic or Hairline); a pending invitation row shows the "Invited" badge (an invitation, not a member status) | Display only | ENT-team-member.status, ENT-team-member.suspended_by, ENT-invitation.status |
| Last Active | Display (timestamp) | N/A | Last login or activity timestamp | Display as relative time | ENT-team-member.last_active_at |
| Workload Summary | Display (chip) | N/A | Count of draft quotes that name the member as responsible clinician | Display only (REQ-009-099) | ENT-team-member.draft_quotes_count |
| Actions | Button group | N/A | Edit, Suspend, Remove, View Activity | Hidden for Owner rows; Suspend and Remove are offered to a Manager only on Clinical Staff and Billing Staff rows (REQ-009-192) | no graph field (control) |
| Team Size Meter | Progress bar | N/A | Seat usage (non-Owner team members with status Active or Suspended plus pending invitations not past expiry; see Rule 6) vs centrally approved limit | Turns amber at 90%, red at 100% (REQ-009-095) | ENT-provider-team-summary.seat_usage, ENT-provider.seat_limit |

**Business Rules**:

- Only Owners and authorized Managers can access the dashboard; non-Owner users have read-only visibility into Owner rows. (REQ-009-087)
- Owner rows display lock badge with tooltip: "Primary Owner role cannot be changed." (REQ-009-088)
- Pending invitation rows (badge "Invited") show "Resend Invitation" and "Cancel Invitation." (REQ-009-089)
- Active rows show "Suspend" (same modal as Remove, Screen 4; REQ-009-082). "Suspended" rows show "Reactivate", except a suspension set by Hairline, which only a Hairline admin can lift. (REQ-009-090, REQ-009-192)
- While the provider organization is Suspended, the dashboard is view-only (Rule 10): invite, resend, cancel invitation, role change, suspend, reactivate, and remove actions are unavailable, and the page shows "Your account is suspended. Team changes are unavailable. Please contact support." (REQ-009-153)
- Current logged-in user's row highlighted with "(You)." (REQ-009-091)
- Sorting: Owners (locked) first, then other roles alphabetically. (REQ-009-092)
- Search/filter by name, email, role, status. (REQ-009-093)
- Banner surfaces central team-size policy and provides link to "Request More Seats", which opens an FR-034 support case pre-filled as a seat-increase request; the admin applies an approved increase by editing Seat Limit in FR-015 Screen 3 Tab 1. (REQ-009-094)

**Notes**:

- Pagination/infinite scroll for >50 members. (REQ-009-096)
- Quick stats: Total, Active, Pending Invitations (count of invitations with status Pending that are not past expires_at), Suspended, Seats Remaining. (REQ-009-097; ENT-provider-team-summary.total_members, ENT-provider-team-summary.active_members, ENT-provider-team-summary.pending_invitations, ENT-provider-team-summary.suspended_members, ENT-provider-team-summary.seats_remaining)
- CSV export for audit. (REQ-009-098)

---

#### Screen 2: Invite Team Member Form

**Purpose**: Collect info needed to invite a new team member.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| First Name | text | Yes | Team member's first name | 2-50 characters, letters, spaces, hyphens (REQ-009-175) | ENT-invitation.first_name |
| Last Name | text | Yes | Team member's last name | 2-50 characters (REQ-009-175) | ENT-invitation.last_name |
| Email | email | Yes | Work email | Valid email; globally unique across provider organizations (Owners, team members, pending invitations; REQ-009-008); not exceeding seat limit | ENT-invitation.email |
| Role | select/dropdown | Yes | Manager, Clinical Staff, and Billing Staff (FR-031). When a Manager is inviting, the list shows only Clinical Staff and Billing Staff | Owner option shows warning + lock icon and is disabled | ENT-invitation.role |
| Personal Message | textarea | No | Optional note for invitation email | Max 500 chars (REQ-009-176) | ENT-invitation.personal_message |
| Seat Limit Banner | Display | N/A | Shows remaining seats & link to request more if depleted | Display-only | ENT-provider-team-summary.seats_remaining |

**Business Rules**:

- Email uniqueness is global (global provider email identity rule, REQ-009-008). An email already on this team or pending here prompts the "View member / Resend invitation" CTA (B2). An email used by another provider organization (Owner, member, or pending invitation) shows the A3 blocking error; emails freed by a Deactivated provider can be invited. (REQ-009-052)
- Role dropdown includes inline permission summary from FR-031's current matrix; Owner option is always disabled in this screen and annotated: "Primary Owner cannot be set or changed from this screen." (REQ-009-100)
- Form unavailable while the provider organization is Suspended (Team page view-only, Rule 10); admin invitations are blocked separately (Screen 12, REQ-009-024). (REQ-009-153)
- Form blocked when seat limit reached; CTA changes to "Request more seats", which opens an FR-034 support case pre-filled as a seat-increase request (FR-015 Rule 7); the admin edits Seat Limit in FR-015 Screen 3 Tab 1. (REQ-009-101)
- SSE updates show send status; success toast: "Invitation sent to [email] (expires in 7 days)." (REQ-009-042)

**Notes**:

- Optional profile photo upload (future). (REQ-009-102)
- CSV bulk invite (future). (REQ-009-102)
- Draft invitations backlog (future). (REQ-009-102)

---

#### Screen 3: Role & Permission Management Dialog

**Purpose**: Modify existing team member roles (non-Owner) and view permission changes.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Team Member Name | Display | N/A | Full name | Read-only | ENT-team-member.first_name, ENT-team-member.last_name |
| Current Role | Display (badge) | N/A | Existing role | Read-only | ENT-team-member-org-role.role_id |
| New Role | select/dropdown | Yes | Target role | Must differ from current; Owner option disabled (REQ-009-063) | ENT-team-member-org-role.role_id |
| Permission Comparison | Display (table) | N/A | Side-by-side diff | Read-only | ENT-role-permission-definition.permissions |
| Reason for Change | textarea | No | Optional audit note | Max 250 chars (REQ-009-063) | ENT-team-activity-audit-log.description |

**Business Rules**:

- Owner records show disabled form with callout: "Primary Owner role cannot be changed." (REQ-009-059)
- The affected team member is always notified by email of a role change; there is no option to suppress the notification. (REQ-009-058)
- Cannot change own role. (REQ-009-061)
- A Manager can change the role of Clinical Staff and Billing Staff only; a Manager cannot change the role of the Owner or of another Manager. (REQ-009-004)
- Permissions diff highlights removals (red) and additions (green). (REQ-009-056)
- Confirmation modal summarises risk (e.g., losing billing access). (REQ-009-062)

**Notes**:

- Provide impact summary (# of quotes and appointments naming the member as responsible clinician). (REQ-009-062)
- Display last role change timestamp + actor. (REQ-009-062)

---

#### Screen 4: Remove or Suspend Team Member Modal

**Purpose**: Reassign work and revoke access in a guided flow.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Responsibilities List | table | N/A | Draft quotes, open treatment records, and upcoming appointments that name the member as responsible clinician | Auto-generated | ENT-team-member.draft_quotes_count, ENT-team-member.upcoming_appointments_count |
| Replacement Clinician Dropdown | select | Yes (if open items) | Replacement clinician for the open items | Filters by role compatibility | no graph field (control) |
| Removal Reason | select + textarea | Yes | Categorized reason + optional notes | Predefined reasons (REQ-009-083) | ENT-team-member.removal_reason_category, ENT-team-member.removal_reason_note |
| Session Revocation Toggle | checkbox | Yes | Force logout all sessions | Locked to true (REQ-009-083) | no graph field (control) |
| Notification Preview | display | N/A | Email template summary | Pulls from FR-020 notification templates | no graph field (control) |

**Business Rules**:

- Modal unavailable for Owners; no provider-facing workflow can remove or suspend the primary Owner. (REQ-009-079)
- A replacement clinician is required when open items exist; otherwise option to archive. (REQ-009-080)
- Removal triggers notifications to removed member and provider owner, plus audit event. (REQ-009-081)
- Suspensions use same modal with different final state. (REQ-009-082)
- Remove and Suspend are offered to a Manager only for Clinical Staff and Billing Staff members; the Owner can use them on any non-Owner member. (REQ-009-192)

**Notes**:

- Provide bulk reassignment for >10 open items (wizard launches Screen 5). (REQ-009-084)
- Show SLA: "Transfers must complete before confirming removal." (REQ-009-084)

---

#### Screen 5: Task Transfer Wizard

**Purpose**: Handle high-volume reassignment and ensure continuity before removal.

**Steps**:

1. **Select Workloads**: Breakdown by item type with counts (quotes, treatment records, appointments). (REQ-009-085; ENT-team-member.draft_quotes_count, ENT-team-member.upcoming_appointments_count)
2. **Assign Targets**: Map each workload type to a target member (supports split assignments). (REQ-009-085)
3. **Review & Confirm**: Summary of transfers, notifications to recipients, and audit preview. (REQ-009-085)

**Business Rules**:

- Wizard auto-suggests targets based on role + current workload. (REQ-009-086)
- Transfers blocked if target lacks required permissions; prompts to update role first. (REQ-009-086)
- Completion required before removal modal allows final confirmation. (REQ-009-086)

---

#### Screen 6: Team Member Detail Page (Provider Dashboard)

**Purpose**: Provide comprehensive view of individual team member's profile, workload, permissions, and activity for provider owners/admins to manage and monitor.

**Access Control**: Accessible by Owners and Managers only. Team members cannot view other members' detail pages (except their own profile in account settings). (REQ-009-103)

**Entry Points**:

- Click team member name/row in Screen 1 (Team Management Dashboard)
- Direct link from reassignment workflows
- Search results in team directory

**Layout Structure**: Tabbed interface with overview header

**Header Section**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Profile Photo | image | No | Team member avatar (default to initials) | JPG/PNG, max 2MB, square aspect | ENT-team-member.profile_photo |
| Full Name | display (text) | N/A | First name + Last name | Read-only for others | ENT-team-member.first_name, ENT-team-member.last_name |
| Email | display (email) | N/A | Primary email address | Read-only | ENT-team-member.email |
| Role Badge | badge | N/A | Current role with lock icon if Owner | Color-coded by role | ENT-team-member-org-role.role_id |
| Status Indicator | badge | N/A | Active / Suspended for team members; "Invited" for a pending invitation | Real-time status | ENT-team-member.status, ENT-invitation.status |
| Last Active | display (timestamp) | N/A | Last login or action timestamp | Relative time with tooltip | ENT-team-member.last_active_at |
| Quick Actions | button group | N/A | Edit Role, Suspend or Reactivate, Remove Member, View Activity Log | Context-aware based on actor permissions; Suspend and Remove Member are offered to a Manager only on Clinical Staff and Billing Staff members (REQ-009-192) | no graph field (control) |

**Tab 1: Overview**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Member Since | display (date) | N/A | Account creation / invitation acceptance date | Read-only | ENT-team-member.created_at |
| Phone Number | display (tel) | Yes | Contact phone (required at account setup, Screen 8) | Masked for privacy (REQ-009-109) | ENT-team-member.phone_number |
| Department/Specialty | text | No | Optional organizational label (e.g., "Surgeon", "Reception") | Max 50 chars; editable by Owner/Manager (REQ-009-109) | ENT-team-member.department_specialty |
| Current Workload Summary | card/widget | N/A | Draft quotes (count) and Upcoming appointments (count) that name the member as responsible clinician | Click counts to filter relevant lists (REQ-009-099) | ENT-team-member.draft_quotes_count, ENT-team-member.upcoming_appointments_count |
| Permissions Matrix | table | N/A | Read-only table showing what this role can/cannot do | Grouped by feature area; links to Screen 3 for role changes | ENT-role-permission-definition.permissions |

**Tab 2: Activity Log**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Date Range Filter | date picker | No | Filter by start/end date | Defaults to last 30 days (REQ-009-110) | ENT-team-activity-audit-log.timestamp |
| Action Type Filter | multi-select dropdown | No | Filter by action categories (Login, Inquiry, Quote, Treatment, Patient Communication, Settings) | Multi-select (REQ-009-110) | ENT-team-activity-audit-log.action_type |
| Activity Timeline | list/table | N/A | Chronological list of actions | Columns: Timestamp, Action Type, Description, Related Entity (link), IP Address (if enabled) | ENT-team-activity-audit-log.timestamp, ENT-team-activity-audit-log.action_type, ENT-team-activity-audit-log.description, ENT-team-activity-audit-log.related_entity_type, ENT-team-activity-audit-log.ip_address |
| Export CSV | button | N/A | Download filtered activity log | Includes all columns plus metadata (REQ-009-177) | no graph field (control) |

**Tab 3: Assigned Work**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Work Category Tabs | sub-tabs | N/A | Quotes, Treatment records, Appointments | Badge shows count per category (REQ-009-111) | no graph field (control) |
| Work Item List | table | N/A | Context-specific columns per category | Sortable by date, status, priority (REQ-009-178) | no graph field (list of work items) |
| Bulk Reassign | button | N/A | Select multiple items and reassign to another member | Opens Screen 5 (Task Transfer Wizard) (REQ-009-111) | no graph field (control) |

**Business Rules**:

- Owner rows show lock badge on role field with tooltip: "Primary Owner role cannot be changed." (REQ-009-088)
- "Edit Role" action only available if actor has permission (Owners can edit all non-Owners; Managers can edit only Clinical Staff and Billing Staff, never the Owner or another Manager). (REQ-009-104)
- "Remove Member" action shows confirmation with impact summary (pulls data from Screen 4). (REQ-009-105)
- Activity log respects privacy rules and the global audit retention policy; IP addresses remain visible in full to authorized admins for the duration of the retention period. (REQ-009-156)
- If viewing own detail page, "Remove Member" and "Edit Role" actions are hidden (cannot self-modify). (REQ-009-106)
- Suspended members show banner: "This member is suspended. Reactivate to restore access." The banner and the Reactivate action apply only to a suspension set by the clinic; a suspension set by Hairline shows no Reactivate. (REQ-009-107, REQ-009-192)
- A pending invitation (badge "Invited") is not yet a team member and shows limited data: only the Overview tab with invitation status and "Resend Invitation" / "Cancel Invitation" actions. (REQ-009-108)

---

### Team Member Onboarding Experience (Public/PR-01)

#### Screen 7: Invitation Landing

**Purpose**: Validate invitation token and orient new team member.

**Key Elements**:

- Provider branding (name, logo), role summary, invitation expiry countdown. (REQ-009-112; ENT-provider.name, ENT-invitation.role, ENT-invitation.expires_at)
- CTA: "Accept & Create Account" (new user) with secondary link "Already have an account with this provider? Log in to continue." (REQ-009-112)
- Security notice referencing central policies (strong password requirements, audit logging; MFA to be introduced in a future release—see **Future Improvements: MFA/2FA**). (REQ-009-112)

**Validation**:

- Token validity, and invitation status (Pending and not past expires_at only), which means the invitation is still Pending and its seat is held (Rule 6); this is not a fresh seat availability test. (REQ-009-043)
- Provider status: for a Deactivated provider the page shows the invalid-invitation message "This invitation is no longer valid."; for a Suspended provider it shows "This clinic is temporarily unavailable", the invitation stays Pending, and its expiry keeps running. (REQ-009-195)

---

#### Screen 8: Account Setup (MFA Enrollment – Future Enhancement)

**Purpose**: Collect core account details (including a verified contact phone) and enforce security before granting access. MFA enrollment is **not implemented in the initial release of FR-009** and is treated as a **future improvement**.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Email | display | N/A | Pre-filled from invitation, locked | Read-only; must match invitation token (REQ-009-113) | ENT-invitation.email |
| First Name | text | Yes | Editable first name | 2-50 characters; letters/spaces/hyphen (REQ-009-113) | ENT-team-member.first_name |
| Last Name | text | Yes | Editable last name | 2-50 characters; letters/spaces/hyphen (REQ-009-113) | ENT-team-member.last_name |
| Phone Number | tel | Yes | Primary contact phone for this team member (also used later for MFA where applicable) | E.164 format; uniqueness per user within provider; must be verified via one-time code where possible (REQ-009-113) | ENT-team-member.phone_number |
| Password | password | Yes | Account password | Must satisfy FR-026 policy (length + complexity) (REQ-009-113) | ENT-team-member.password |
| Confirm Password | password | Yes | Re-enter password | Must match Password (REQ-009-113) | ENT-team-member.password |
| Accept Terms | checkbox | Yes | Confirm platform terms & privacy | Must be checked before submission (REQ-009-113) | ENT-team-member.terms_accepted_at |
| Create Account CTA | button | N/A | Submit enrollment | Disabled until required fields valid (REQ-009-190) | no graph field (control) |

> **Deferred Fields (Future Improvement – MFA/2FA)**  
> The following field is **explicitly out of scope for the initial implementation of FR-009** and will be implemented later once platform-wide MFA is delivered (see Constitution + FR-031 / FR-026):  
>
> - MFA Setup Method – selection of MFA factor (SMS, Authenticator App, Security Key) (REQ-009-167; ENT-team-member.mfa_setup_method)

**Business Rules**:

- Password setup must succeed before account is activated. (REQ-009-114)
- MFA enrollment for provider team members will be added in a future release and is **not** enforced in the initial FR-009 scope. (REQ-009-167)
- If invitee already has global Hairline account, screen switches to login-only acceptance flow, unless the email belongs to another provider (A3). (REQ-009-115)

---

#### Screen 9: First-Login Permission Tour

**Purpose**: Educate new members on allowed actions and pending tasks.

**Components**:

- Role overview card (permissions summary). (ENT-role-permission-definition.permissions)
- Required next steps (e.g., complete profile, review items handed over via Screen 5).
- Notification opt-in management referencing FR-020 templates. (REQ-009-187)

**Business Rules**:

- Tour must be acknowledged before hitting dashboard. (REQ-009-116)
- Logs acceptance in audit trail. (REQ-009-116)

---

### Admin Platform (A-01)

#### Screen 10: Provider Team Directory

**Purpose**: Give Hairline admins a cross-provider view for support and compliance.

**Data Fields / UI Elements**:

| Field Name | Type | Required | Description | Validation / Notes | Graph field |
|------------|------|----------|-------------|--------------------|-------------|
| Global Search | input | No | Search by provider name, member email, or status | Debounced; supports wildcard (REQ-009-184) | no graph field (control) |
| Provider Name | display (link) | N/A | Provider organization name | Click opens provider profile in admin console | ENT-provider.name |
| Provider ID | display | N/A | Internal provider identifier | Read-only | ENT-provider.id |
| Team Member Name | display | N/A | Full name of team member | Read-only | ENT-team-member.first_name, ENT-team-member.last_name |
| Email | display | N/A | Team member email | Read-only | ENT-team-member.email |
| Role | badge | N/A | Provider role | Owner rows show lock icon | ENT-team-member-org-role.role_id |
| Ownership Flag | icon | N/A | Indicates primary owner | Tooltip: "Primary Owner" (REQ-009-186) | no graph field (control) |
| Status | badge | N/A | Team member status Active or Suspended; a pending invitation row shows the "Invited" badge | Color-coded | ENT-team-member.status, ENT-invitation.status |
| Last Login | display (timestamp) | N/A | Most recent login timestamp | Relative time with tooltip for exact timestamp | ENT-team-member.last_login_at |
| Actions | button group | N/A | Force suspend, Reactivate, resend invitation, view audit log, impersonate | Buttons enabled based on admin permissions; Force suspend is not offered on the Owner row (use the Owner handover first, REQ-009-161); Reactivate shows on a Suspended member; resend invitation is the A2 resend; Impersonate is Super Admin only and follows the FR-015 "Login as Provider" rules (see Screen 11 Business Rules) (REQ-009-117) | no graph field (control) |
| Filters Panel | chips/checkboxes | No | Filter by status, role, region | Multi-select (REQ-009-185) | no graph field (control) |
| Pagination Controls | pagination | N/A | Navigate through result pages | Server-driven | no graph field (control) |

**Notes**:

- For a single provider's team with an admin invite action, see Screen 12 (embedded in FR-015 Screen 3, Tab 3: Staff List).

---

#### Screen 11: Team Member Detail Page (Admin Console)

**Purpose**: Provide platform admins with comprehensive oversight of individual team members across all providers, including audit logs, compliance monitoring, and emergency intervention capabilities.

**Access Control**: Accessible by platform administrators only. Supports a Super Admin-only impersonation session for support and troubleshooting, governed by the FR-015 "Login as Provider" rules (limited write; see Business Rules below). (REQ-009-118)

**Entry Points**:

- Click team member name/row in Screen 10 (Provider Team Directory)
- Search results from global admin search
- Audit investigation links from compliance reports
- Alert notifications for suspicious activity

**Layout Structure**: Tabbed interface with admin control header

**Header Section**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Profile Photo | image | No | Team member avatar | Read-only; same as provider view | ENT-team-member.profile_photo |
| Full Name | display (text) | N/A | First name + Last name | Read-only | ENT-team-member.first_name, ENT-team-member.last_name |
| Email | display (email) | N/A | Primary email address | Read-only; clickable to send admin email (REQ-009-188) | ENT-team-member.email |
| Provider Organization | display (link) | N/A | Provider name this member belongs to | Click to view provider detail in admin console | ENT-provider.name |
| Role Badge | badge | N/A | Current role with ownership indicator | Color-coded by role | ENT-team-member-org-role.role_id |
| Status Indicator | badge | N/A | Active / Suspended / Flagged for team members; "Invited" for a pending invitation | Real-time status; "Flagged" shown if compliance alert exists (REQ-009-119) | ENT-team-member.status, ENT-invitation.status |
| Account Created | display (timestamp) | N/A | Original account creation date | Relative time with tooltip | ENT-team-member.created_at |
| Last Active | display (timestamp) | N/A | Most recent login or action timestamp | Relative time with tooltip; highlight if >30 days inactive (REQ-009-119) | ENT-team-member.last_active_at |
| Admin Actions | button group | N/A | Force Suspend, Reactivate, Reset Password, View Sessions, Impersonate | High-privilege actions require re-authentication; MFA-based re-auth is a future enhancement tied to platform-wide MFA rollout; Force Suspend is not offered on the Owner row (REQ-009-161) | no graph field (control) |

**Tab 1: Profile & Overview**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Account ID | display (text) | N/A | System-generated unique identifier | Read-only; copyable | ENT-team-member.user_id |
| Member Since | display (date) | N/A | Invitation acceptance date | Read-only | ENT-team-member.created_at |
| Phone Number | display (tel) | No | Contact phone | Masked; admin can reveal with MFA (future enhancement; initially standard re-auth only) (REQ-009-121) | ENT-team-member.phone_number |
| Department/Specialty | display (text) | No | Provider-defined label | Read-only; editable by provider only | ENT-team-member.department_specialty |
| Permission Summary | table | N/A | Current role permissions | Read-only; shows effective permissions | ENT-role-permission-definition.permissions |
| Linked Devices | list | N/A | Registered devices for MFA | **Future improvement** – placeholder for when MFA is implemented; includes device type, last used, location | ENT-team-member.linked_devices |
| Compliance Flags | alert list | N/A | Active compliance issues or investigations | Links to investigation records | ENT-team-member.compliance_flags |
| Account Notes (Admin-Only) | textarea | No | Internal admin notes not visible to provider or member | Max 2000 chars; audit-logged on every edit (REQ-009-120) | ENT-team-member.account_notes |

**Tab 2: Complete Activity Audit Log**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Date Range Filter | date picker | No | Filter by start/end date | Defaults to last 90 days; can query up to 10 years (global audit-log retention) (REQ-009-122) | ENT-team-activity-audit-log.timestamp |
| Action Type Filter | multi-select dropdown | No | Filter by action categories (Login, Patient Access, Data Export, Settings Change, Communication, Treatment) | Multi-select; includes admin-specific categories (REQ-009-122) | ENT-team-activity-audit-log.action_type |
| Risk Level Filter | dropdown | No | Filter by risk classification (High, Medium, Low) | Auto-classified by system (REQ-009-123) | ENT-team-activity-audit-log.risk_level |
| Activity Timeline | list/table | N/A | Chronological list of all actions | Columns: Timestamp, Action Type, Description, Related Entity (link), IP Address, Location, Device, Risk Level | ENT-team-activity-audit-log.timestamp, ENT-team-activity-audit-log.action_type, ENT-team-activity-audit-log.description, ENT-team-activity-audit-log.related_entity_type, ENT-team-activity-audit-log.ip_address, ENT-team-activity-audit-log.location, ENT-team-activity-audit-log.device, ENT-team-activity-audit-log.risk_level |
| IP Address Tracking | display | N/A | Full IP history with geolocation | Shows all IPs used; flags VPN/proxy usage (REQ-009-124) | ENT-team-activity-audit-log.ip_address, ENT-team-activity-audit-log.location, ENT-team-activity-audit-log.vpn_proxy_flag |
| Export Full Audit | button | N/A | Download complete audit trail | CSV/JSON format; includes all fields; requires strong re-authentication (MFA in future release) (REQ-009-125) | no graph field (control) |
| Flag for Investigation | button | N/A | Mark activity for compliance review | Creates investigation case in FR-031 (REQ-009-126) | no graph field (control) |
| Pagination Controls | pagination | N/A | Navigate through activity pages | Server-side pagination, 100 events per page (REQ-009-122) | no graph field (control) |

**Tab 3: Assigned Work**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Work Category Tabs | sub-tabs | N/A | Quotes, Treatment records, Appointments | Badge shows count per category (REQ-009-179) | no graph field (control) |
| Work Item List | table | N/A | Context-specific columns per category | Sortable by date, status, priority; includes patient ID, status, assigned date, last activity (REQ-009-180) | no graph field (list of work items) |
| Patient Link | link | N/A | Links to patient detail page in admin console | Opens patient record in FR-016 (Admin Patient Management) (REQ-009-182) | no graph field (control) |
| Provider Context | display (badge) | N/A | Shows which provider organization this work belongs to | Always displays since this is admin view | ENT-provider.name |
| Bulk Reassign | button | N/A | Select multiple items and reassign to another member | Opens reassignment workflow; admin can override provider-level restrictions | no graph field (control) |
| Filter by Status | dropdown | No | Filter work items by status (Draft, Active, Completed, Overdue) | Applies to current category tab (REQ-009-181) | no graph field (control) |
| Filter by Priority | dropdown | No | Filter by urgency (High, Medium, Low) | Auto-calculated based on SLA deadlines (REQ-009-130) | no graph field (control) |
| Workload Metrics | display (widget) | N/A | Summary stats: Total items, Overdue count, Avg response time | Provides context for investigations (REQ-009-130) | ENT-team-member.total_work_items, ENT-team-member.overdue_work_items, ENT-team-member.avg_response_time |

**Business Rules**:

- Admins can view assigned work to understand team member's current responsibilities during investigations (REQ-009-127)
- All work items link to relevant patient/inquiry/quote records with proper permissions (REQ-009-127)
- "Overdue" status highlights items past SLA deadlines, supporting compliance reviews (REQ-009-128)
- Bulk reassign available for emergency situations (e.g., team member suspended, provider transition) (REQ-009-129)
- Work item access respects admin permissions defined in FR-031 (Admin Access Control) (REQ-009-127)
- Provides context for questions like: "Why did this member access Patient X's data?" → Check if Patient X is in their assigned work (REQ-009-127)

**Tab 4: Security & Sessions**:

**(Initial FR-009 scope note: Implementation of this tab is deferred for a later improvement phase and is not required for the current build.)* (REQ-009-131)

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Active Sessions | list | N/A | Current logged-in sessions | Shows device, browser, IP, location, started timestamp | ENT-team-member.active_sessions |
| Session Actions | button group | N/A | Force Logout (single session), Force Logout All | Requires re-authentication; MFA re-auth will be introduced in a future release | no graph field (control) |
| Login History | table | N/A | Last 100 login attempts | Columns: Timestamp, IP, Location, Device, Success/Failure, Failure Reason | ENT-team-member.login_history |
| Failed Login Count | display (number) | N/A | Failed attempts in last 24 hours | Highlights if >5 attempts | ENT-team-member.failed_login_count_24h |
| MFA Status | badge | N/A | Enabled / Disabled / Enforced | **Future improvement** – will show MFA method (SMS, App, Key) once MFA exists | ENT-team-member.mfa_status |
| MFA Reset | button | N/A | Force MFA re-enrollment | **Future improvement** – requires MFA re-auth + justification once MFA exists | no graph field (control) |
| Password Last Changed | display (timestamp) | N/A | Last password change date | Flags if >90 days old | ENT-team-member.password_changed_at |
| Force Password Reset | button | N/A | Invalidate password and require reset | Requires re-authentication + justification (MFA re-auth in future release) | no graph field (control) |
| Anomaly Alerts | list | N/A | Suspicious login patterns detected by system | E.g., "Login from new country", "Unusual access time" | ENT-team-member.anomaly_alerts |

**Tab 5: Provider Relationship**:

**(Initial FR-009 scope note: Implementation of this tab is deferred for a later improvement phase and is not required for the current build.)* (REQ-009-131)

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Current Provider | display (link) | N/A | Provider organization name | Click to view provider profile | ENT-provider.name |
| Membership Status | badge | N/A | Active / Suspended / Removed | Current team member status; a pending invitation is not a membership and appears only in Invitation History | ENT-team-member.status |
| Invitation History | table | N/A | All invitations sent to this email | Columns: Date, Inviting Provider, Role Offered, Status | ENT-invitation.created_at, ENT-provider.name, ENT-invitation.role, ENT-invitation.status |
| Role Change History | table | N/A | All role modifications | Columns: Date, Old Role, New Role, Changed By, Reason | ENT-team-member-org-role.role_id |
| Remove from Provider | button | N/A | Admin-forced removal | Requires re-authentication + justification (MFA requirement deferred to future release); logs high-priority audit event; not offered on the Owner row (use the Owner handover first, REQ-009-162) | no graph field (control) |

**Business Rules**:

- All admin actions (suspend, password reset, session logout, etc.) require strong re-authentication before execution; MFA-based re-authentication is **planned as a future improvement** and is not part of the initial FR-009 scope. (REQ-009-132)
- Every admin action generates high-priority audit log entry with justification field (required). (REQ-009-133)
- **Impersonate** follows the FR-015 "Login as Provider" rules, which own this behavior (FR-015 Screen 3); FR-009 applies them to impersonating an individual team member: (REQ-009-023)
  - Impersonation is blocked when the provider is Deactivated ("Login as Provider is not available for a deactivated provider."). When the provider is Suspended, the session is read-only under FR-032 Rule 6, the same as for the user.
  - Super Admin only. Before starting, the admin enters a reason (min 20 chars) and re-authenticates with password (MFA re-authentication is a future enhancement tied to the platform-wide MFA rollout).
  - The impersonated session shows a persistent banner: "You are viewing as [Name] — admin session by [Admin Name]" with an "End Session" action.
  - The admin may act on the impersonated user's behalf, except changing that user's password or login email, or changing payout/bank or financial settings; those actions are blocked during the session.
  - Session start (with reason), session end, and every write action performed during the session are logged in the FR-009 audit trail and FR-015 Tab 8: Activity Log, attributed to the admin acting as the user.
  - The session ends automatically after the standard 30-minute admin inactivity timeout.
- Patient data access log is kept for 10 years, like all audit logs (global audit-log rule); it is not anonymized after 1 year or deleted after 2 years. (REQ-009-134)
- Compliance flags automatically trigger notification to admin compliance team via FR-020. (REQ-009-135)
- IP addresses shown in full for admins (not anonymized) to support security investigations. (REQ-009-136)
- Activity log export includes admin metadata (who exported, when, for what case) for chain of custody. (REQ-009-137)

**Notes**:

- Real-time updates via SSE: session changes, login attempts, and activity updates reflected immediately. (REQ-009-183)
- Breadcrumb navigation: Admin Dashboard > Provider Team Directory > [Member Name]
- Mobile responsive with collapsible tabs.
- Supports "Compare Members" feature: select multiple members and compare activity patterns side-by-side (future enhancement). (REQ-009-138)
- Integration with FR-031 (Admin Access Control) for permission checks on sensitive actions.
- Links to patient records respect admin permissions defined in FR-016 (Admin Patient Management). (REQ-009-182)

---

#### Screen 12: Provider Team (Admin, Single Provider)

**Purpose**: Let Hairline admins view one provider's team and invite staff on that provider's behalf. This view is embedded in FR-015 Screen 3 (Provider Profile Details), Tab 3: Staff List.

**Access Control**: Platform administrators. Viewing follows admin access to the provider profile; the Invite Staff Member action requires the FR-031 "Edit Providers" permission. Impersonate remains Super Admin only. (REQ-009-139)

**Data Fields / UI Elements**:

| Field Name | Type | Required | Description | Validation / Notes | Graph field |
|------------|------|----------|-------------|--------------------|-------------|
| Team Member Name | display (link) | N/A | Full name of team member | Click opens Screen 11 | ENT-team-member.first_name, ENT-team-member.last_name |
| Email | display | N/A | Team member email | Read-only | ENT-team-member.email |
| Role | badge | N/A | Provider role | Owner row shows lock icon | ENT-team-member-org-role.role_id |
| Ownership Flag | icon | N/A | Indicates primary owner | Tooltip: "Primary Owner" (REQ-009-186) | no graph field (control) |
| Status | badge | N/A | Team member status Active or Suspended; a pending invitation row shows the "Invited" badge | Color-coded | ENT-team-member.status, ENT-invitation.status |
| Last Login | display (timestamp) | N/A | Most recent login timestamp | Relative time with tooltip for exact timestamp | ENT-team-member.last_login_at |
| Seat Usage | display | N/A | Non-Owner team members with status Active or Suspended plus invitations with status Pending that are not past expires_at, against the provider's Seat Limit (FR-015); the Owner, Removed members, and Expired, Cancelled, or Accepted invitations do not count (Rule 6) | Example: "12 / 100 seats used" (REQ-009-148) | ENT-provider-team-summary.seat_usage, ENT-provider.seat_limit |
| Row Actions | button group | N/A | Force suspend, Reactivate, resend invitation, view audit log, impersonate | Same behavior and permissions as Screen 10 and Screen 11; Force suspend and Force remove are not offered on the Owner row (REQ-009-161, REQ-009-162) | no graph field (control) |
| Invite Staff Member | button | N/A | Opens the admin invite form for this provider | Hidden or disabled without FR-031 "Edit Providers"; disabled with reason when blocked (see Business Rules) | no graph field (control) |
| Hand over Owner role | button | N/A | Opens the Owner handover dialog for this provider (Rule 11) | Hairline admin action; not available to provider users (REQ-009-174) | no graph field (control) |

**Invite Staff Member Form (admin)**:

| Field Name | Type | Required | Description | Validation / Notes | Graph field |
|------------|------|----------|-------------|--------------------|-------------|
| Email Address | email | Yes | Invitee email | Same validation as Screen 2, including the global provider email identity rule (REQ-009-008) and duplicate pending invitation checks | ENT-invitation.email |
| Role | dropdown | Yes | One of the provider's assignable roles | Manager, Clinical Staff, and Billing Staff only (FR-031); Owner is not offered | ENT-invitation.role |
| First Name | text | Yes | Invitee first name | Same validation as Screen 2 (REQ-009-175) | ENT-invitation.first_name |
| Last Name | text | Yes | Invitee last name | Same validation as Screen 2 (REQ-009-175) | ENT-invitation.last_name |

**Hand Over Owner Role Dialog (admin)**:

| Field Name | Type | Required | Description | Validation / Notes | Graph field |
|------------|------|----------|-------------|--------------------|-------------|
| New Owner | select | Yes | One active team member of this provider | Active members only; the current Owner is not listed (REQ-009-174) | no graph field (control) |
| Reason for Handover | textarea | Yes | Reason recorded in the audit trail | Required (REQ-009-174) | ENT-team-activity-audit-log.description |
| Confirm Handover | button | N/A | Confirms the handover | Asks the admin to confirm before it runs (REQ-009-174) | no graph field (control) |

**Business Rules**:

- The list shows only the selected provider's members and pending invitations; no cross-provider data appears in this view. (REQ-009-140)
- Admin invitations use the normal FR-009 invitation flow: same invitation email, acceptance flow (Screens 7-9), token rules, and expiry (REQ-009-016), and the same per-provider invitation rate limit (REQ-009-018). (REQ-009-141)
- Admins cannot assign the Owner role in the invite form. The Owner role changes hands only through the Hairline admin Owner handover (Rule 11, REQ-009-174), which is a separate admin action and not part of invitations. (REQ-009-142)
- Invite is blocked when the provider's Seat Limit (FR-015) is reached, with message: "This provider has reached its seat limit. Increase the Seat Limit in Tab 1 before inviting." (REQ-009-143)
- Invite is blocked when the provider status is Suspended or Deactivated, with message: "Invitations are unavailable while this provider is [Status]." (REQ-009-144)
- Each admin invitation is logged in the FR-009 audit trail and in FR-015 Tab 8: Activity Log, recording the inviting admin as the actor. (REQ-009-025)
- Existing admin actions (force suspend, reactivate, resend invitation, view audit log, impersonate) remain available from each row. Resend invitation is the A2 resend, including its seat check. (REQ-009-145)
- Hand over Owner role: the admin picks an active team member and a reason and confirms; the new member becomes Owner, the previous Owner becomes a Manager, the handover is logged, and both are emailed (Rule 11). The provider record's Owner login email then becomes the new Owner's email. The Owner already has a team member record and an org-role record, created with the provider account at onboarding (FR-015), so the handover changes roles on existing records. (REQ-009-174, REQ-009-196)

---

## Business Rules

### General Module Rules

- **Rule 1**: Every provider organization must have exactly one Owner at all times (single primary account holder). (REQ-009-146)
- **Rule 2**: Owner role assignments cannot be created, changed, or demoted through the provider platform UI. The Owner changes only through the Hairline admin handover (Rule 11). (REQ-009-147)
- **Rule 3 (Global Provider Email Identity)**: An email belongs to at most one provider organization at a time, across all forms of membership: Owner (created via FR-015), team member, or pending invitation. When a provider is Deactivated (FR-015), its Owner, team member, and pending-invitation emails are freed for reuse; the old records stay archived and are not reactivated by reuse. FR-015 provider creation and owner login-email edits apply this same rule. (REQ-009-008)
- **Rule 4**: All team management actions (invite, role change, removal) are logged in audit trail with timestamp, actor, and action details. (REQ-009-013)
- **Rule 5**: Invitation links expire after 7 days—expired invitations can be resent with new expiry. (REQ-009-016)
- **Rule 6**: Maximum team size per provider organization defaults to 100 members and is configured by admins per FR-015. Seat usage counts non-Owner team members with status Active or Suspended plus invitations with status Pending that are not past expires_at, and each person is counted once. The Owner, Removed members, and Expired, Cancelled, or Accepted invitations do not count. A Suspended member keeps the seat; only removal frees it. Providers can request limit increases through support per FR-015; invitations must be blocked when seat usage reaches the limit. (REQ-009-148; REQ-015-010)
- **Rule 7**: FR-031 defines provider roles and their permission matrices centrally; FR-009 handles team assignment and consumes those definitions without allowing clinics to edit them. (REQ-009-011; REQ-031-005)
- **Rule 8**: Provider roles are limited to the four clinic roles: Owner, Manager, Clinical Staff, and Billing Staff. Custom provider roles do not exist. (REQ-009-002)
- **Rule 9 (Invitation and Team Member Model)**: An invited person exists only as an invitation (Pending, Accepted, Expired, Cancelled) until they accept. A team member record is created only when the invitation is accepted. Team member statuses are Active, Suspended, and Removed, stored as `active`, `suspended`, and `inactive` (`inactive` means Removed and is kept for compatibility). A Removed member never takes a seat. "Invited" is only the badge that team lists show for a Pending invitation row; it is not a team member status. Legacy invitees that the old invite flow stored as team member rows (status `inactive` or `pending`, never accepted and no password set) are migrated into invitations: Pending if their invite or activation link has not expired, otherwise Expired. The placeholder member row is then deleted, so after migration `inactive` means Removed only (CR-FR009-20261028-01). (REQ-009-150; REQ-009-151; REQ-009-152)
- **Rule 10 (Suspended Provider Team Management)**: While the provider organization is Suspended (FR-015; banner per FR-032 Rule 6), the provider Team page and team member detail pages are view-only. Provider users cannot invite, resend or cancel an invitation, change a role, suspend, reactivate, or remove a member. The Team page shows "Your account is suspended. Team changes are unavailable. Please contact support." Admin invitations to a Suspended or Deactivated provider are blocked by REQ-009-024. (REQ-009-153)
- **Rule 11 (Owner Handover)**: Only a Hairline admin can hand the Owner role of a provider organization to another person; no provider-side user can do it (Rule 2). The handover is one admin action, so the provider organization has exactly one Owner before and after it (Rule 1). The new Owner must already be an active team member of that provider organization, and the previous Owner becomes a Manager. The action requires a reason, is recorded in the FR-009 audit trail (Rule 4) and FR-015 Tab 8: Activity Log with the admin as actor, and the new and the previous Owner are notified by email. After the handover the provider record's Owner login email is the new Owner's email (REQ-009-196). REQ-009-174.
- **Rule 12 (Work belongs to the clinic)**: Inquiries, bookings, and messages belong to the clinic as a whole. A named person is recorded only as the responsible clinician on quotes and treatment records (`clinician_ids`, FR-004 and FR-010) and on appointments. Removal and suspension list only those items and require a replacement clinician for the open ones; the lists on the FR-004 and FR-010 records are rewritten when a member is removed. (REQ-009-191)
- **Rule 13 (Suspend and Reactivate)**: The Owner can suspend or remove any non-Owner member; a Manager can suspend or remove only Clinical Staff and Billing Staff. A suspension records who set it, the clinic or the platform. A suspension set by the platform can be lifted only by a Hairline admin; the clinic sees no Reactivate on it. (REQ-009-192)
- **Rule 14 (Invitations and provider status)**: When a provider is Deactivated (FR-015), the system cancels every Pending invitation (status Cancelled, audit entry). Screen 7 checks the provider status before an invitation is accepted. (REQ-009-194, REQ-009-195)
- One team member belongs to exactly one provider organization at any given time. Transfers require admin-assisted reassignment that archives the old membership before creating a new one. (REQ-009-189)
- Team Member Organization Role: One-to-one mapping per team member ensuring unique provider linkage; record persists for audit/history when transfers occur.
- Team Member: Name, email, phone number, and password belong to the individual team member; clinic-level settings stay with the provider organization

### Data & Privacy Rules

- **Privacy Rule 1**: Team member email addresses are visible only within their own provider organization (REQ-009-154)
- **Privacy Rule 2**: Team member activity logs are accessible only to Owners and Managers within same organization (REQ-009-155)
- **Privacy Rule 3**: IP addresses in team member activity logs are retained in full for security and compliance investigations, subject to the global audit log retention and access rules defined in the Constitution (REQ-009-156)
- **Privacy Rule 4**: Removed team members' historical records are archived (not deleted) for compliance—visible only to Owners and platform admins (REQ-009-157)
- **Audit Rule**: All access to team member data must be logged with timestamp, accessing user, and action performed (REQ-009-158)
- **GDPR Compliance**: Team members can request data export (personal data only) and account deletion through support (FR-034). A Hairline admin removes the account (status Removed; there is no fourth status) and anonymizes the member's personal data, and audit entries keep an anonymous label for the existing audit retention period. An Owner must go through the Owner handover first (REQ-009-159)
- **Authentication**: Team member accounts use same strong authentication as provider owners (password only in initial FR-009 scope; MFA is planned as a future enhancement per Constitution / FR-031 and will be applied platform-wide, including provider admins and staff, in a later release)
- **Authorization**: Every API request validates role permissions before execution—fail closed on permission check errors
- **Storage**: Audit logs stored in append-only ledger for immutability and compliance
- **Provider web app calls Team Management API for all CRUD operations**: Authentication: OAuth 2.0 bearer tokens with role claims. Error handling: Return 403 Forbidden for permission violations, 409 Conflict for business rule violations
- **Audit logging service receives events from all team management actions**: Authentication: Internal service-to-service auth. Error handling: Async event publishing with retry queue
- **MaxMind GeoIP (Optional)**: Failure handling: Graceful degradation—if service unavailable, show IP address without location (REQ-009-173)
- Provider staff use modern web browsers (Chrome, Safari, Firefox, Edge - last 2 versions) for accessing provider web app

### Admin Editability Rules

**Editable by Admin (Hairline platform admins)**:

- Maximum team size limit per provider (default 100, adjustable 1-500) (REQ-009-160)
- Force-suspend individual team member accounts for terms violations; not offered on the Owner row (REQ-009-161)
- Reactivate a Suspended team member; a suspension set by the platform can be lifted only by a Hairline admin (REQ-009-192)
- Force-remove team member in emergency situations (any member except the Owner, who changes only through the Owner handover) (REQ-009-162)
- Hand over the Owner role to an active team member (Screen 12; Rule 11) (REQ-009-174)
- Invite staff to a single provider with a non-Owner role (Screen 12; requires FR-031 "Edit Providers") (REQ-009-024)

**Fixed in Codebase (Not Editable)**:

- Protected role identities and primary Owner rule. Role permissions are configured centrally in FR-031, not by provider organizations. (REQ-009-163)
- Number of Owners (always exactly 1) (REQ-009-163)
- Team activity log retention: the global audit-log rule applies (10 years); there is no FR-009 retention setting (REQ-009-163)
- Audit log structure and required fields (REQ-009-163)
- Invitation expiry: always 7 days, not a setting (REQ-009-016)
- Email invitation template structure (content editable, structure fixed) (REQ-009-163)
- Session management security parameters (REQ-009-163)

**Configurable with Restrictions**:

- Admin can view any provider's team structure but cannot modify it without provider consent (audit trail logged), except the admin actions defined in Screens 10-12 (including inviting staff via Screen 12 and actions taken during a Super Admin impersonation session) (REQ-009-164)
- Admin can suspend team members but cannot hard-delete accounts (compliance requirement); on a deletion request the admin removes the account and anonymizes personal data (Data & Privacy Rules, GDPR Compliance) (REQ-009-165)

### Payment & Billing Rules

*Not applicable to this module—team management itself has no direct payment flows. Provider subscription billing (future) may factor in team size.* (REQ-009-166)

---

## Dependencies

- **FR-031**: Admin Access Control & Permissions (provider roles and permission matrices)
- **FR-020**: Notifications & Alerts (invitation, role change, removal, and reassignment templates)
- **FR-030**: Notification Rules & Configuration (catalogue entries for the team notices, REQ-009-007)
- **FR-012**: Messaging & Communication (one conversation per patient and provider, unaffected by a removal)
- **FR-015**: Provider Management (provider organizations and owner accounts, Seat Limit, "Login as Provider"; Staff List embeds Screen 12)
- **FR-032**: Provider Dashboard Settings & Profile Management (Owner-level settings gated by FR-009 roles)
- **FR-003 and FR-004**: Inquiry Submission & Distribution; Quote Submission & Management (role-based access to inquiries and quotes)
- **FR-010**: Treatment Execution & Documentation (which roles may document treatment is defined only in FR-010 Rule 4, REQ-010-002)
- Shared services: S-03 Notification Service, S-06 Audit Log Service



---

## User Scenarios & Testing

### User Story 1 - Owner Invites First Team Member (Priority: P1)

A clinic owner has been using the platform solo and now wants to bring their office coordinator/front-of-staff onto the platform to help manage patient inquiries and scheduling. The owner invites this team member, who successfully creates a Manager account and starts managing inquiries.

**Why this priority**: Core functionality—without team invitations, multi-user collaboration is impossible. This is the foundational feature that unlocks all other team management capabilities.

**Independent Test**: Can be fully tested by inviting a new team member via email, having them create an account, and verifying they can log in and access features appropriate to their assigned role.

**Acceptance Scenarios**:

1. **Given** clinic owner is logged into provider dashboard, **When** they navigate to "Team" tab and click "Invite Team Member", **Then** invitation form appears with fields for name, email, role, and optional message
2. **Given** owner fills out invitation form with coordinator/front-of-staff details and role "Manager", **When** they click "Send Invitation", **Then** system sends email to the new Manager with invitation link and displays success confirmation
3. **Given** the new Manager receives invitation email, **When** they click the invitation link, **Then** they are directed to account creation page with email and name pre-filled
4. **Given** the new Manager creates password and accepts terms, **When** they submit account creation form, **Then** account is created with Manager role and they can immediately log in
5. **Given** the new Manager logs in for first time, **When** they access dashboard, **Then** they see only features and data appropriate to Manager role (can view inquiries, manage schedules, but cannot access billing/ownership settings)

---

### User Story 2 - Owner Changes Team Member Role (Priority: P1)

A clinician who was initially invited as "Clinical Staff" (limited to treatment execution) is being promoted to "Manager" to help with operational management and team oversight. The owner changes their role and the clinician immediately gains access to additional operational features.

**Why this priority**: Role changes are common as team members grow in responsibility or as organizational needs change. Must work reliably to maintain proper access control.

**Independent Test**: Invite a team member with one role, then edit their role to a different one, and verify permissions update immediately in their active session.

**Acceptance Scenarios**:

1. **Given** owner is viewing team management dashboard, **When** they click "Edit" on a team member row, **Then** role editing dialog appears showing current role and dropdown to select new role
2. **Given** owner selects new role "Manager" for team member currently "Clinical Staff", **When** permission comparison table is displayed, **Then** owner can see which permissions are being added (e.g., team management, analytics) and which remain unchanged
3. **Given** owner reviews permission changes and clicks "Update Role", **When** system processes the change, **Then** team member's role is updated in database and email notification sent to affected team member
4. **Given** affected team member is actively logged in during role change, **When** they navigate to a new page or refresh, **Then** new permissions are immediately reflected (can now access Manager-level menu items)
5. **Given** audit log is enabled, **When** role change completes, **Then** activity log records timestamp, owner who made change, old role, new role, and reason (if provided)

---

### User Story 3 - Owner Removes Team Member (Priority: P1)

A coordinator leaves the clinic and the owner needs to remove their access to the platform. The owner removes the team member, names a replacement clinician for the open quotes and appointments, and the departing team member can no longer log in.

**Why this priority**: Critical for security and compliance—must be able to immediately revoke access for departing staff. Prevents unauthorized data access.

**Independent Test**: Remove an existing team member and verify they can no longer authenticate, and verify the open items now name the replacement clinician.

**Acceptance Scenarios**:

1. **Given** owner clicks "Remove" on a team member's row, **When** confirmation dialog appears, **Then** system displays the open items that name the team member as responsible clinician (2 draft quotes, 3 upcoming appointments)
2. **Given** owner is prompted to name a replacement clinician, **When** owner selects another coordinator from dropdown as replacement clinician, **Then** system confirms the replacement and warns that removed team member will lose access immediately
3. **Given** owner confirms removal, **When** system processes removal, **Then** all active sessions for removed team member are invalidated immediately
4. **Given** removed team member's open items were handed over, **When** new coordinator logs in, **Then** they see the 2 draft quotes and 3 appointments that now name them as responsible clinician
5. **Given** removed team member tries to log in, **When** they enter credentials, **Then** authentication fails with message "You no longer have access to this organization. Contact your clinic owner if you believe this is an error."
6. **Given** owner views team dashboard after removal, **When** dashboard refreshes, **Then** removed team member no longer appears in active team list but appears in audit log as "Removed"

---

### User Story 4 - Enforce Single-Provider Membership (Priority: P2)

A clinic owner attempts to invite a surgeon who is currently active in another provider organization. The system blocks the invitation, ensuring staff cannot belong to two providers simultaneously.

**Why this priority**: Prevents compliance issues, billing confusion, and data leakage between providers by enforcing one-organization-per-member.

**Independent Test**: Attempt to invite an email that already belongs to a different provider and verify the system blocks the action with clear remediation guidance.

**Acceptance Scenarios**:

1. **Given** a clinician (e.g., Dr. Smith) is an active Clinical Staff member of Provider A, **When** Provider B owner enters <doctor.smith@clinic.com> in the invite form, **Then** system detects the existing membership before sending the invitation.
2. **Given** the conflict is detected, **When** the owner attempts to proceed, **Then** the form displays blocking error copy: "This email already belongs to another provider team. Remove the member from their current provider team before inviting them here."
3. **Given** the clinician is removed from Provider A, **When** Provider B re-sends the invitation, **Then** it succeeds because the email is no longer tied to another provider.

---

### User Story 5 - Admin Views Activity Log for Audit (Priority: P2)

A clinic admin needs to review team activity for a specific period to understand who accessed patient data for a compliance audit. They view the activity log filtered by date range and export it as a CSV for the audit report.

**Why this priority**: Important for compliance and security, but not part of daily workflow. Supports periodic audits and incident investigations.

**Independent Test**: Perform several team management actions, then view activity log and verify all actions are logged with correct timestamps, actors, and details.

**Acceptance Scenarios**:

1. **Given** admin navigates to team member detail page, **When** they click "View Activity" tab, **Then** activity log loads showing all actions by that team member with timestamps, action types, descriptions
2. **Given** activity log contains 1000+ events, **When** admin applies date range filter (last 30 days), **Then** log updates to show only events within selected date range
3. **Given** admin wants to focus on sensitive actions, **When** they apply action type filter "Patient Data Access", **Then** log shows only events where team member viewed or edited patient medical information
4. **Given** filtered activity log is displayed, **When** admin clicks "Export CSV", **Then** CSV file downloads containing all filtered events with columns: timestamp, action type, description, IP address, related entity
5. **Given** admin reviews exported data, **When** they open CSV in spreadsheet, **Then** all audit fields are present and readable for compliance reporting

---

### User Story 6 - System Enforces "Single Owner" Rule (Priority: P1)

Each clinic has exactly one primary Owner account. All other elevated users are Admins. The system must prevent creation of additional Owners from the provider UI.

**Why this priority**: Critical business rule that protects organizational integrity—having a single clearly identified Owner simplifies billing, legal responsibility, and access control.

**Independent Test**: Attempt to create or assign a second Owner via all provider-facing flows (invitation form, role edit dialog) and verify that every attempt is blocked; verify that system surfaces which account is the current Owner without allowing in-app changes.

**Acceptance Scenarios**:

1. **Given** provider Owner opens the "Invite Team Member" form, **When** they open the Role dropdown, **Then** Owner is visible as a non-selectable option with tooltip "Primary Owner cannot be set or changed from this screen."
2. **Given** any provider user (Owner or Manager) opens the role edit dialog for the current Owner, **When** they attempt to change the role, **Then** the form is disabled and displays callout: "Primary Owner role cannot be changed."
3. **Given** a Manager attempts to update a team member's role to Owner via any provider UI, **When** they submit the change, **Then** system blocks the request with error: "Cannot assign the primary Owner role from the provider portal."

---

### Edge Cases

- **What happens when invitation email bounces (invalid email address)?**
  System logs the bounce event, keeps the invitation status Pending with delivery state "Pending Send" (there is no Bounced status), and notifies provider owner via in-app notification: "Invitation to [email] failed—email address may be invalid. Please cancel the invitation and invite again with the correct address." (REQ-009-168)

- **How does system handle provider owner inviting 100+ team members at once?**
  System enforces rate limit: maximum 10 invitations per hour per provider organization. If limit exceeded, display error: "You've reached the invitation limit (10 per hour). Please try again later." This prevents abuse and email service quota exhaustion. (REQ-009-169)

- **What occurs if team member clicks invitation link on mobile device vs desktop?**
  Invitation link and account creation flow are fully responsive—works on any device. After account creation, mobile user is prompted to "Download Mobile App" (if patient platform) or "Bookmark this page" (if provider web app). (REQ-009-170)

- **What happens if owner removes team member while they're actively submitting a quote?**
  System allows in-progress transaction to complete (quote submission succeeds). However, after submission completes, session is invalidated on next request. Team member sees: "Your access has been removed. Please contact clinic owner." (REQ-009-078)

- **How does system handle two admins simultaneously trying to change same team member's role?**
  The last change wins. The later change overwrites the earlier one and no error is shown to either person. The activity log records both changes with who made each. (REQ-009-171)

---

## Future Improvements: MFA/2FA (Not in Initial FR-009 Scope)

The system-wide Constitution and `system-prd.md` require Multi-Factor Authentication (MFA) for certain user classes (e.g., admin platform users, provider admins). However, **FR-009 focuses on team & role management** and **does not deliver MFA/2FA functionality in its initial implementation**. All MFA-related behaviors referenced in this document are explicitly treated as **future improvements**, to be implemented once the shared authentication/MFA stack is available (primarily via FR-026 App Settings & Security and FR-031 Admin Access Control).

**Deferred items for future implementation (out of scope for current FR-009 build):**

- **Team Member Onboarding (Provider Side)**:
  - MFA enrollment during team member account setup (Screen 8): phone number capture for MFA, MFA factor selection, and enforcement that "password + MFA" must succeed before activation. (REQ-009-167)
- **Admin Console Security Controls**:
  - MFA-gated actions in Screen 11 (Admin Team Member Detail): export full audit requiring MFA, session actions requiring MFA re-auth, MFA Status and MFA Reset controls, and admin-force removal/reset flows that currently mention MFA. (REQ-009-167)
  - Device-level MFA concepts such as "Linked Devices" are documented as placeholders only. (REQ-009-167)
- **Strong Re-Auth vs MFA**:
  - Where this PRD currently mentions "re-authentication" for high-privilege actions, the **initial implementation** will rely on password-based re-auth only. Upgrading these flows to **MFA-backed re-auth** is a **future enhancement** aligned with the platform-wide MFA rollout. (REQ-009-167)

Implementation teams MUST treat the above as **non-blocking, non-MVP requirements** for FR-009 and track them against the corresponding security/MFA epics instead of this feature’s delivery scope.

---

## Functional Requirements Summary

### Core Requirements

> Note: This section summarizes the normative requirements already described in Business Workflows, Screen Specifications, and Business Rules. In case of conflict, the Business Rules section prevails.

- **REQ-009-001**: System MUST allow the Provider Owner or Manager to invite team members via email with secure, time-limited invitation links (7-day expiry), MUST let a Manager invite only Clinical Staff and Billing Staff (the Owner can also invite a Manager), and MUST make provider-side team management view-only while the provider organization is Suspended, blocking invite, resend, role change, suspend, and remove (Rule 10)
- **REQ-009-002**: System MUST support the four provider roles (Owner, Manager, Clinical Staff, Billing Staff) defined in FR-031; custom provider roles do not exist
- **REQ-009-003**: System MUST enforce role-based access control for all provider platform features and data
- **REQ-009-004**: System MUST allow the Owner to modify the role of any non-Owner team member, and a Manager to modify the role only of members below Manager (Clinical Staff and Billing Staff), never the Owner or another Manager, with immediate permission updates
- **REQ-009-005**: System MUST allow the Owner to remove or suspend any non-Owner team member and a Manager to remove or suspend only Clinical Staff and Billing Staff, with immediate access revocation
- **REQ-009-006**: System MUST keep exactly one Owner per provider organization at all times—prevent removal or demotion of the Owner and prevent a second Owner from being created from the provider platform; the Owner changes only through the Hairline admin handover (REQ-009-174)
- **REQ-009-007**: System MUST send email notifications for team management events (invitation, role change, removal, suspension, reactivation, Owner handover); these notices need matching FR-030 catalogue entries
- **REQ-009-008**: System MUST enforce the global provider email identity rule (Rule 3): an email can belong to only one provider organization at a time as Owner, team member, or pending invitation; invitations, FR-015 provider creation, and FR-015 owner login-email edits that use an email tied to another non-Deactivated provider must be blocked; emails of Deactivated providers are freed for reuse while their records stay archived
- **REQ-009-174**: System MUST let only a Hairline admin hand the Owner role of a provider organization to another person (Rule 11). The provider organization keeps exactly one Owner before, during, and after the handover, and no provider-side user can start a handover. The new Owner MUST already be an active team member of that organization; the previous Owner becomes a Manager; the action requires a reason; and the new and the previous Owner are both notified by email. The admin starts it from Screen 12

### Data Requirements

> Note: Data requirements are summarized here for traceability; field-level definitions and provenance are specified in Screen Specifications.

- **REQ-009-009**: System MUST maintain team member records with: name, email, role, status (Active/Suspended/Removed), invitation date, acceptance date, last activity timestamp. A team member record is created only when an invitation is accepted
- **REQ-009-010**: System MUST persist invitation records with: token, expiry date, status (Pending/Accepted/Expired/Cancelled), email delivery state (a failed send is "Pending Send" on a Pending invitation, not a status), sender, recipient email, role offered. Until acceptance an invited person exists only as an invitation; "Invited" is the display badge for a Pending invitation, not a team member status
- **REQ-009-011**: System MUST consume the provider role permission definitions configured centrally in FR-031
- **REQ-009-012**: System MUST maintain team member-to-provider organization relationships with role assignment per organization

### Security & Privacy Requirements

> Note: Security and privacy requirements extend the platform-wide Constitution; see Business Rules and the Constitution for non-negotiable baselines.

- **REQ-009-013**: System MUST log all team management actions in audit trail with: timestamp, actor, action type, target team member, old values, new values, IP address
- **REQ-009-014**: System MUST apply a team member's role change to their active sessions within 5 seconds without forcing logout: the previous permissions stop applying, and the member's next request uses the refreshed permissions. System MUST invalidate all active sessions for a team member within 5 seconds of removal
- **REQ-009-015**: System MUST validate actor permissions before allowing any team management action (invite, role change, removal)
- **REQ-009-016**: System MUST generate cryptographically secure, single-use invitation tokens that expire after 7 days
- **REQ-009-017**: System MUST encrypt all team member data at rest (AES-256) and in transit (TLS 1.3)
- **REQ-009-018**: System MUST enforce rate limiting on invitations: maximum 10 invitations per hour per provider organization

### Integration Requirements

> Note: Integration requirements summarize how FR-009 interacts with shared services and other FRs; detailed interaction patterns are documented in Dependencies.

- **REQ-009-019**: System MUST integrate with email service to send invitation and notification emails with 99%+ delivery rate
- **REQ-009-020**: System MUST integrate with authentication service to create team member accounts and manage sessions
- **REQ-009-021**: System MUST publish role change events to session management service for real-time permission updates
- **REQ-009-022**: System MUST write all team management events to centralized audit logging service
- **REQ-009-023**: System MUST restrict admin impersonation of a provider team member to Super Admins and apply the FR-015 "Login as Provider" rules: reason (min 20 chars) and password re-authentication before start, persistent banner with End Session, write actions allowed except changing the user's password, login email, or payout/bank/financial settings, session start/end and every write action logged and attributed to the admin, and automatic end after 30 minutes of inactivity. Impersonation MUST be blocked when the provider is Deactivated and MUST be read-only under FR-032 Rule 6 when the provider is Suspended
- **REQ-009-024**: System MUST let admins with the FR-031 "Edit Providers" permission invite staff to a single provider from FR-009 Screen 12 (FR-015 Screen 3, Tab 3) using the normal invitation flow and expiry, assigning only a non-Owner role available to that provider, and blocking the invite when the provider's Seat Limit is reached or the provider is Suspended or Deactivated
- **REQ-009-025**: System MUST log each admin-initiated invitation in the FR-009 audit trail and FR-015 Tab 8: Activity Log with the inviting admin as actor

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-11-24 | 1.12 (proposed) | Logic review pass 1: a Manager may remove or suspend only Clinical Staff and Billing Staff; work belongs to the clinic and a person is named only as responsible clinician; Suspend and Reactivate flow with who set a suspension; Owner handover action on Screen 12 with the login email following the new Owner; seat check on resend; Cancel Invitation flow; Deactivated provider cancels Pending invitations; Screen 7 provider-status checks; invitation expiry fixed at 7 days; account deletion by admin with anonymization; B6 no longer reroutes messages. | Documentation |
| 2026-11-22 | 1.11 (proposed) | Requirements graph programme baseline: PRD compressed to the checklist structure (each rule stated once, field rows tagged with graph field ids, dropped classes removed). No rule changes. Earlier history (v1.0 to v1.10) and the change requests CR-FR009-20260929-01, CR-FR009-20261015-01, CR-FR009-20261015-02, CR-FR015-20261027-01 and CR-FR009-20261028-01 are in `archived/prd-baseline-2026-11-08/fr009-provider-team-roles/` and in git history. | Documentation |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | Joachim Trung Tuan | 2026-10-27 | Approved v1.6 seat usage and impersonation alignment (documentation only), with CR-FR015-20261027-01 |
| Product Owner | Joachim Trung Tuan | 2026-10-28 | Approved v1.7 invitation and team member model and seat usage (documentation only), with CR-FR009-20261028-01 |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B
**Based on**: FR-009 from system-prd.md
**Last Updated**: 2026-11-24 (proposed revision v1.12; prior approval status unchanged)
