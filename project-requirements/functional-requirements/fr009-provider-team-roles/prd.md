# Product Requirements Document: Provider Team & Role Management

**Module**: PR-01: Auth & Team Management
**Feature Branch**: `fr009-provider-team-roles`
**Created**: 2025-11-11
**Status**: ✅ Verified & Approved
**Source**: FR-009 from system-prd.md

---

## Executive Summary

The Provider Team & Role Management feature enables multi-user collaboration within provider organizations by allowing clinic owners to invite team members, assign role-based permissions, and manage access to the Hairline platform. This feature is essential for medium to large clinics where multiple staff members need to collaborate on patient inquiries, quote creation, treatment execution, and aftercare management while maintaining appropriate access controls and audit trails.

**Business Value**: Enables provider organizations to operate efficiently with multiple staff members, reduces bottlenecks by distributing workload, improves response times to patient inquiries, and maintains security through role-based access control.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-XX)**: No direct patient-facing functionality
- **Provider Platform (PR-01)**: Complete team management interface, role assignment, permission controls, team member invitations, activity audit logs
- **Admin Platform (A-01)**: Oversight of all provider teams, ability to view team structures, audit team member activities across providers, manage suspended accounts
- **Shared Services (S-03, S-06)**: S-03 Notification Service for team member invitations and management emails; S-06 Audit Log Service for immutable recording of team management actions

### Multi-Tenant Breakdown

**Patient Platform (P-XX)**:

- No functionality in patient app
- Patients may see team member names/roles in communications (e.g., "Dr. Sarah responded to your inquiry")

**Provider Platform (PR-01)**:

- Team dashboard showing all active team members with roles
- Invite team member flow with email invitation
- Role assignment and modification interface
- Permission management screen
- Team member removal/suspension capability
- Activity log viewer showing team member actions
- Profile management for each team member

**Admin Platform (A-01)**:

- System-wide view of all provider teams
- Ability to view team composition for any provider
- Audit log access for compliance investigations
- Capability to suspend individual team members or entire teams
- Analytics on team sizes, role distribution across platform
- Override capability for emergency access removal

**Shared Services (S-03, S-06)**:

- S-03: Notification Service sends invitation and team-management emails with secure signup links
- Provider Auth Service (PR-01) handles team member account creation, login, password reset, and session management while enforcing PR-01/FR-031 permission checks
- S-06: Audit Log Service records all team management actions for compliance

### Provider Role Model

The provider platform uses four clinic-side roles that directly reflect how real clinics operate, while keeping clear separation from Hairline's own Admin Platform roles:

- **Owner (Main Account Holder)**: Single primary account per provider organization. Responsible for bank details and payouts, contract acceptance, and high-risk configuration. Mapped to the "provider admin / main account holder" described in the client transcription.
- **Manager (Clinic Manager / Operations)**: Operational lead and front-of-staff representative. Can see and manage the full patient journey in the provider portal (inquiries, quotes, schedules, day-to-day operations), coordinate staff work, and manage most team settings, but cannot change bank details or ownership.
- **Clinical Staff**: Medical staff who perform procedures and aftercare (surgeons, clinicians, nurses). Focused on in-progress and aftercare sections, treatment documentation, scans, and medical notes. Limited or no access to billing or sensitive configuration.
- **Billing Staff**: Finance-oriented staff who work with quotes and payouts ("how much they're making"). Can view and reconcile financial information but cannot alter clinical records or manage team structure/ownership.

### Communication Structure

**In Scope**:

- Email invitations to new team members with secure signup link
- Email notifications when team member role changes
- Email notifications when team member is removed or suspended
- In-platform notifications for team management events

**Out of Scope**:

- SMS notifications for team management (handled by S-03: Notification Service if needed; **no SMS is sent in MVP and this channel is reserved for future phases**)
- Video tutorials for team onboarding (handled by separate content module)
- Chat/messaging between team members (separate collaboration feature)

### Entry Points

- **Provider Owner**: Accesses team management from provider dashboard main navigation ("Team" tab)
- **Provider Manager**: Accesses operational team management features from settings menu (within Owner-defined limits)
- **New Team Member**: Receives email invitation with signup link, creates account, automatically assigned to provider organization with specified role
- **Admin Platform**: System administrators access team management oversight from admin dashboard provider detail view

---

## Business Workflows

### Main Flow: Invite Team Member

**Actors**: Provider Owner, System, New Team Member (invitee)
**Trigger**: Provider Owner clicks "Invite Team Member" button in team management dashboard
**Outcome**: Team member receives invitation email, creates account, gains access to provider platform with assigned role

**Steps**:

1. Provider Owner navigates to team management dashboard
2. System displays current team members with their roles and status
3. Provider Owner clicks "Invite Team Member" button
4. System presents invitation form with fields: email address, first name, last name, role selection
5. Provider Owner enters team member details and selects role (Manager, Clinical, Billing). Owner role is not assignable from this flow and is reserved for the single primary account holder managed via Admin Platform (FR-031).
6. System validates email format and checks for duplicate email within organization
7. Provider Owner reviews invitation details and clicks "Send Invitation"
8. System generates secure invitation token (expires in 7 days)
9. System sends email to invitee with invitation link, provider organization name, and role being offered
10. System creates pending invitation record with status "Invited"
11. System displays confirmation message to Provider Owner
12. New Team Member receives email and clicks invitation link
13. System validates invitation token (not expired, not already used)
14. System presents account creation form pre-filled with email, first name, last name
15. New Team Member sets password and accepts terms of service
16. System creates team member account and links to provider organization with assigned role
17. System marks invitation as "Accepted"
18. System sends confirmation email to both Provider Owner and new team member
19. System logs all actions in audit trail
20. New Team Member can immediately log in with new credentials

### Alternative Flows

**A2: Reinvite expired invitation**:

- **Trigger**: Invitation token expired (7 days passed) and team member hasn't signed up
- **Steps**:
  1. Provider Owner views pending invitations list
  2. System shows invitation status as "Expired"
  3. Provider Owner clicks "Resend Invitation" button
  4. System generates new invitation token and sends new email
  5. Old invitation token invalidated
- **Outcome**: Team member receives fresh invitation with new 7-day expiry

**A3: Team member already has account (different provider)**:

- **Trigger**: Invitee email address already exists in system for another provider organization (single-membership rule)
- **Steps**:
  1. System detects existing membership during invitation validation
  2. System displays blocking error: "This email already belongs to another provider team. Remove the member from their current provider or invite them with a different email."
  3. Provider Owner may contact Hairline Admin to request ownership transfer (manual process in FR-031) if employment changes
- **Outcome**: Cross-provider duplication prevented; membership transfers require admin intervention

**B1: Invalid email address**:

- **Trigger**: Provider Owner enters malformed email address
- **Steps**:
  1. System validates email format on blur or submit
  2. System displays inline error message: "Please enter a valid email address"
  3. Provider Owner corrects email
  4. System re-validates and allows submission
- **Outcome**: Only valid email addresses accepted

**B2: Duplicate email within same organization**:

- **Trigger**: Provider Owner invites email that already exists as team member or pending invitation
- **Steps**:
  1. System checks email against existing team members and pending invitations
  2. System displays error: "This email is already part of your team"
  3. System suggests: "View team member" or "Resend invitation" if pending
  4. Provider Owner either cancels or takes suggested action
- **Outcome**: Duplicate prevented, existing record maintained

**B3: Invitation link already used**:

- **Trigger**: Team member clicks invitation link that was already accepted
- **Steps**:
  1. System detects invitation status is "Accepted"
  2. System displays message: "This invitation has already been used. Please log in with your existing credentials."
  3. System provides login link
- **Outcome**: Prevents duplicate account creation

**B4: Network error during invitation send**:

- **Trigger**: Email service fails to send invitation
- **Steps**:
  1. System attempts to send invitation email
  2. Email service returns error
  3. System logs error and retries up to 3 times with exponential backoff
  4. If all retries fail, system marks invitation as "Pending Send"
  5. System displays warning to Provider Owner: "Invitation created but email failed. We'll retry automatically."
  6. Background job retries sending every 10 minutes for 24 hours
  7. If still failing after 24 hours, system alerts admin team
- **Outcome**: Invitation record created, email eventually delivered or admin intervenes

---

### Main Flow: Change Team Member Role

**Actors**: Provider Owner/Admin, System, Affected Team Member
**Trigger**: Provider Owner/Admin clicks "Edit" on team member row in team dashboard
**Outcome**: Team member's role and permissions updated, team member notified

**Steps**:

1. Provider Owner/Admin views team management dashboard
2. System displays list of team members with current roles
3. Provider Owner/Admin clicks "Edit" button next to team member name (Owner rows show locked badge and no edit action)
4. System presents role selection dropdown with current role pre-selected
5. Provider Owner/Admin selects new role from dropdown (Owner role is read-only; demotion/promotion to Owner must be escalated to platform admins)
6. System displays permission comparison: "Current permissions" vs "New permissions"
7. Provider Owner/Admin reviews changes and clicks "Update Role"
8. System validates actor has permission to assign selected role
9. System updates team member's role in database
10. System immediately applies new permissions to any active sessions
11. System sends email to affected team member: "Your role has been changed to [Role]"
12. System logs role change in audit trail with timestamp, actor, old role, new role
13. System displays success confirmation
14. Affected team member's next page load reflects new permissions

### Alternative Flows

**A4: Attempt to modify Owner role via provider UI**:

- **Trigger**: Any provider user (Owner or Admin) attempts to modify the Owner's role from the provider platform
- **Steps**:
  1. System detects target role is Owner (single primary account holder)
  2. System displays error: "Ownership for this provider is managed by Hairline Admins. Please contact support to request changes."
  3. Edit dialog closes without making changes
- **Outcome**: Ownership is never changed from the provider platform; all ownership transfers/demotions happen via Admin Platform (FR-031), preserving the single-owner invariant

**B5: Team member currently performing critical action**:

- **Trigger**: Role change attempted while team member is mid-transaction (e.g., submitting quote)
- **Steps**:
  1. System updates role in database
  2. System allows in-progress action to complete with old permissions
  3. Next action uses new permissions
  4. System logs that in-flight action completed with previous permission set
- **Outcome**: No transaction interruption, clean permission transition

---

### Main Flow: Remove Team Member

**Actors**: Provider Owner/Admin, System, Removed Team Member
**Trigger**: Provider Owner/Admin clicks "Remove" on team member row
**Outcome**: Team member's access revoked, data reassigned or archived, team member notified

**Steps**:

1. Provider Owner/Admin clicks "Remove" button next to team member name
2. System presents confirmation dialog with warning about data reassignment
3. System displays list of team member's current responsibilities:
   - Active inquiries assigned to them
   - Draft quotes in progress
   - Upcoming scheduled appointments
4. System prompts: "Reassign to:" with dropdown of remaining team members
5. Provider Owner/Admin selects reassignment target or chooses "Archive unassigned"
6. Provider Owner/Admin confirms removal
7. System validates actor has permission to remove target team member
8. System immediately revokes all active sessions for removed team member
9. System reassigns all active work items to selected team member
10. System archives team member's historical records (maintains for audit)
11. System sends email to removed team member: "Your access to [Provider Name] has been removed"
12. System logs removal in audit trail with reason (if provided)
13. System displays success confirmation
14. Removed team member's next login attempt shows: "You no longer have access to this organization"

### Alternative Flows

**A6: Self-removal by Owner**:

- **Trigger**: Provider Owner attempts to remove themselves
- **Steps**:
  1. System detects actor is removing themselves
  2. System immediately blocks request with error: "Owners cannot remove their own accounts. Ask another Owner or Hairline Admin to perform this action."
  3. Error is logged in audit trail for compliance
- **Outcome**: Owner removal actions must be initiated by a different Owner or escalated to platform admins

**A7: Remove team member with no active work**:

- **Trigger**: Team member being removed has no assigned inquiries, quotes, or appointments
- **Steps**:
  1. System detects no active work items
  2. System skips reassignment step
  3. Removal proceeds immediately after confirmation
- **Outcome**: Simplified flow for inactive team members

**B6: Team member removed has active patient communication**:

- **Trigger**: Removed team member has ongoing message threads with patients
- **Steps**:
  1. System detects active message threads
  2. System displays warning: "This member has active patient conversations"
  3. System prompts: "New messages from patients will be routed to [reassigned team member]"
  4. Provider Owner confirms understanding
  5. System updates message routing
  6. System sends automated message to patients: "Your inquiry is now being handled by [new team member]"
- **Outcome**: Seamless patient communication continuity

---

## Screen Specifications

### Provider Platform (PR-01)

#### Screen 1: Team Management Dashboard

**Purpose**: Central interface for viewing all team members, their roles, status, quota usage, and available actions.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Team Member Name | Display (text) | N/A | Full name of team member | Display only |
| Email | Display (email) | N/A | Team member's email address | Display only |
| Role | Display (badge/tag) | N/A | Current role (Owner/Manager/Clinical/Billing) | Display only |
| Role Lock Indicator | Icon | N/A | Shows lock icon for Owner rows (non-editable) | Display only |
| Status | Display (badge) | N/A | Active, Invited, Suspended | Display only |
| Last Active | Display (timestamp) | N/A | Last login or activity timestamp | Display as relative time |
| Workload Summary | Display (chip) | N/A | Counts of inquiries/quotes assigned | Display only |
| Actions | Button group | N/A | Edit, Remove, Transfer, View Activity | Hidden for Owner rows |
| Team Size Meter | Progress bar | N/A | Current members vs centrally approved limit | Turns amber at 90%, red at 100% |

**Business Rules**:

- Only Owners and Managers can access dashboard; Managers have read-only visibility into Owner rows.
- Owner rows display lock badge with tooltip: "Ownership changes managed by Hairline Admins."
- "Invited" status rows show "Resend Invitation" and "Cancel Invitation."
- "Suspended" rows show "Reactivate."
- Current logged-in user's row highlighted with "(You)."
- Sorting: Owners (locked) → Managers → Clinical → Billing, alphabetical.
- Search/filter by name, email, role, status.
- Banner surfaces central team-size policy and provides link to "Request More Seats" modal (sends request to Admin Platform).

**Notes**:

- Pagination/infinite scroll for >50 members.
- Quick stats: Total, Active, Pending, Suspended, Seats Remaining.
- CSV export for audit.

---

#### Screen 2: Invite Team Member Form

**Purpose**: Collect info needed to invite a new team member.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| First Name | text | Yes | Team member's first name | 2-50 characters, letters, spaces, hyphens |
| Last Name | text | Yes | Team member's last name | 2-50 characters |
| Email | email | Yes | Work email | Valid email, unique within org, not exceeding seat limit |
| Role | select/dropdown | Yes | Owner/Manager/Clinical/Billing | Owner option shows warning + lock icon |
| Personal Message | textarea | No | Optional note for invitation email | Max 500 chars |
| Seat Limit Banner | Display | N/A | Shows remaining seats & link to request more if depleted | Display-only |

**Business Rules**:

- Email uniqueness enforced per org; duplicates prompt "View member / Resend invitation" CTA.
- Role dropdown includes inline permission summary; Owner option is always disabled in this screen and annotated: "Primary Owner can only be set or changed by Hairline Admins."
- Form blocked when seat limit reached; CTA changes to "Request more seats" which routes to admin workflow.
- SSE updates show send status; success toast: "Invitation sent to [email] (expires in 7 days)."

**Notes**:

- Optional profile photo upload (future).
- CSV bulk invite (future).
- Draft invitations backlog (future).

---

#### Screen 3: Role & Permission Management Dialog

**Purpose**: Modify existing team member roles (non-Owner) and view permission changes.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Team Member Name | Display | N/A | Full name | Read-only |
| Current Role | Display (badge) | N/A | Existing role | Read-only |
| New Role | select/dropdown | Yes | Target role | Must differ from current; Owner option disabled |
| Permission Comparison | Display (table) | N/A | Side-by-side diff | Read-only |
| Reason for Change | textarea | No | Optional audit note | Max 250 chars |
| Email Notification Toggle | checkbox | No | Allow suppressing notification (default on) | If off, requires justification |

**Business Rules**:

- Owner records show disabled form with callout: "Contact Hairline Admin to adjust ownership."
- Cannot change own role.
- Permissions diff highlights removals (red) and additions (green).
- Confirmation modal summarises risk (e.g., losing billing access).

**Notes**:

- Provide impact summary (# of inquiries/quotes affected).
- Display last role change timestamp + actor.

---

#### Screen 4: Remove or Suspend Team Member Modal

**Purpose**: Reassign work and revoke access in a guided flow.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Responsibilities List | table | N/A | Active inquiries, quotes, appointments | Auto-generated |
| Reassignment Dropdown | select | Yes (if outstanding work) | Target team member | Filters by role compatibility |
| Removal Reason | select + textarea | Yes | Categorized reason + optional notes | Predefined reasons |
| Session Revocation Toggle | checkbox | Yes | Force logout all sessions | Locked to true |
| Notification Preview | display | N/A | Email template summary | Pulls from FR-020 notification templates |

**Business Rules**:

- Modal unavailable for Owners; CTA replaced with instructions to contact admin.
- Reassignment required when outstanding work exists; otherwise option to archive.
- Removal triggers notifications to removed member and provider owner, plus audit event.
- Suspensions use same modal with different final state.

**Notes**:

- Provide bulk reassignment for >10 inquiries (wizard launches Screen 5).
- Show SLA: "Transfers must complete before confirming removal."

---

#### Screen 5: Task Transfer Wizard

**Purpose**: Handle high-volume reassignment and ensure continuity before removal.

**Steps**:

1. **Select Workloads**: Breakdown by entity type with counts (inquiries, quotes, appointments, messages).
2. **Assign Targets**: Map each workload type to a target member (supports split assignments).
3. **Review & Confirm**: Summary of transfers, notifications to recipients, and audit preview.

**Business Rules**:

- Wizard auto-suggests targets based on role + current workload.
- Transfers blocked if target lacks required permissions; prompts to update role first.
- Completion required before removal modal allows final confirmation.

---

#### Screen 6: Team Member Detail Page (Provider Dashboard)

**Purpose**: Provide comprehensive view of individual team member's profile, workload, permissions, and activity for provider owners/admins to manage and monitor.

**Access Control**: Accessible by Owners and Admins only. Team members cannot view other members' detail pages (except their own profile in account settings).

**Entry Points**:

- Click team member name/row in Screen 1 (Team Management Dashboard)
- Direct link from reassignment workflows
- Search results in team directory

**Layout Structure**: Tabbed interface with overview header

**Header Section**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Profile Photo | image | No | Team member avatar (default to initials) | JPG/PNG, max 2MB, square aspect |
| Full Name | display (text) | N/A | First name + Last name | Read-only; click to edit in modal |
| Email | display (email) | N/A | Primary email address | Read-only |
| Role Badge | badge | N/A | Current role with lock icon if Owner | Color-coded by role |
| Status Indicator | badge | N/A | Active / Invited / Suspended | Real-time status |
| Last Active | display (timestamp) | N/A | Last login or action timestamp | Relative time with tooltip |
| Quick Actions | button group | N/A | Edit Role, Remove Member, View Activity Log | Context-aware based on actor permissions |

**Tab 1: Overview**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Member Since | display (date) | N/A | Account creation / invitation acceptance date | Read-only |
| Phone Number | display (tel) | No | Contact phone (if provided during setup) | Masked for privacy |
| Department/Specialty | text | No | Optional organizational label (e.g., "Surgeon", "Reception") | Max 50 chars; editable by Owner/Admin |
| Current Workload Summary | card/widget | N/A | Active inquiries (count), Draft quotes (count), Upcoming appointments (count), Unread messages (count) | Click counts to filter relevant lists |
| Permissions Matrix | table | N/A | Read-only table showing what this role can/cannot do | Grouped by feature area; links to Screen 3 for role changes |

**Tab 2: Activity Log**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Date Range Filter | date picker | No | Filter by start/end date | Defaults to last 30 days |
| Action Type Filter | multi-select dropdown | No | Filter by action categories (Login, Inquiry, Quote, Treatment, Patient Communication, Settings) | Multi-select |
| Activity Timeline | list/table | N/A | Chronological list of actions | Columns: Timestamp, Action Type, Description, Related Entity (link), IP Address (if enabled) |
| Export CSV | button | N/A | Download filtered activity log | Includes all columns plus metadata |

**Tab 3: Assigned Work**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Work Category Tabs | sub-tabs | N/A | Inquiries, Quotes, Appointments, Messages | Badge shows count per category |
| Work Item List | table | N/A | Context-specific columns per category | Sortable by date, status, priority |
| Bulk Reassign | button | N/A | Select multiple items and reassign to another member | Opens Screen 5 (Task Transfer Wizard) |

**Business Rules**:

- Owner rows show lock badge on role field with tooltip: "Ownership managed by Hairline Admins. Contact support to change."
- "Edit Role" action only available if actor has permission (Owners can edit all non-Owners; Admins cannot edit Owners).
- "Remove Member" action shows confirmation with impact summary (pulls data from Screen 4).
- Activity log respects privacy rules and the global audit retention policy; IP addresses remain visible in full to authorized admins for the duration of the retention period.
- If viewing own detail page, "Remove Member" and "Edit Role" actions are hidden (cannot self-modify).
- Suspended members show banner: "This member is suspended. Reactivate to restore access."
- Invited (pending) members show limited data: only Overview tab with invitation status and "Resend Invitation" / "Cancel Invitation" actions.

---

### Team Member Onboarding Experience (Public/PR-01)

#### Screen 7: Invitation Landing

**Purpose**: Validate invitation token and orient new team member.

**Key Elements**:

- Provider branding (name, logo), role summary, invitation expiry countdown.
- CTA: "Accept & Create Account" (new user) with secondary link "Already have an account with this provider? Log in to continue."
- Security notice referencing central policies (strong password requirements, audit logging; MFA to be introduced in a future release—see **Future Improvements: MFA/2FA**).

**Validation**:

- Token validity, seat availability (double-check), invitation status (Pending only).

---

#### Screen 8: Account Setup (MFA Enrollment – Future Enhancement)

**Purpose**: Collect core account details (including a verified contact phone) and enforce security before granting access. MFA enrollment is **not implemented in the initial release of FR-009** and is treated as a **future improvement**.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Email | display | N/A | Pre-filled from invitation, locked | Read-only; must match invitation token |
| First Name | text | Yes | Editable first name | 2-50 characters; letters/spaces/hyphen |
| Last Name | text | Yes | Editable last name | 2-50 characters; letters/spaces/hyphen |
| Phone Number | tel | Yes | Primary contact phone for this team member (also used later for MFA where applicable) | E.164 format; uniqueness per user within provider; must be verified via one-time code where possible |
| Password | password | Yes | Account password | Must satisfy FR-026 policy (length + complexity) |
| Confirm Password | password | Yes | Re-enter password | Must match Password |
| Accept Terms | checkbox | Yes | Confirm platform terms & privacy | Must be checked before submission |
| Create Account CTA | button | N/A | Submit enrollment | Disabled until required fields valid |

> **Deferred Fields (Future Improvement – MFA/2FA)**  
> The following field is **explicitly out of scope for the initial implementation of FR-009** and will be implemented later once platform-wide MFA is delivered (see Constitution + FR-031 / FR-026):  
>
> - MFA Setup Method – selection of MFA factor (SMS, Authenticator App, Security Key)

**Business Rules**:

- Password setup must succeed before account is activated.
- MFA enrollment for provider team members will be added in a future release and is **not** enforced in the initial FR-009 scope.
- If invitee already has global Hairline account, screen switches to login-only acceptance flow.

---

#### Screen 9: First-Login Permission Tour

**Purpose**: Educate new members on allowed actions and pending tasks.

**Components**:

- Role overview card (permissions summary).
- Required next steps (e.g., complete profile, review assigned inquiries handed over via Screen 5).
- Notification opt-in management referencing FR-020 templates.

**Business Rules**:

- Tour must be acknowledged before hitting dashboard.
- Logs acceptance in audit trail.

---

### Admin Platform (A-01)

#### Screen 10: Provider Team Directory

**Purpose**: Give Hairline admins a cross-provider view for support and compliance.

**Data Fields / UI Elements**:

| Field Name | Type | Required | Description | Validation / Notes |
|------------|------|----------|-------------|--------------------|
| Global Search | input | No | Search by provider name, member email, or status | Debounced; supports wildcard |
| Provider Name | display (link) | N/A | Provider organization name | Click opens provider profile in admin console |
| Provider ID | display | N/A | Internal provider identifier | Read-only |
| Team Member Name | display | N/A | Full name of team member | Read-only |
| Email | display | N/A | Team member email | Read-only |
| Role | badge | N/A | Owner/Manager/Clinical/Billing | Owner rows show lock icon |
| Ownership Flag | icon | N/A | Indicates primary owner | Tooltip: "Primary Owner" |
| Status | badge | N/A | Active, Invited, Suspended | Color-coded |
| Last Login | display (timestamp) | N/A | Most recent login timestamp | Relative time with tooltip for exact timestamp |
| Actions | button group | N/A | Force suspend, reset invitation, view audit log, impersonate (read-only) | Buttons enabled based on admin permissions |
| Filters Panel | chips/checkboxes | No | Filter by status, role, region | Multi-select |
| Pagination Controls | pagination | N/A | Navigate through result pages | Server-driven |

---

#### Screen 11: Team Member Detail Page (Admin Console)

**Purpose**: Provide platform admins with comprehensive oversight of individual team members across all providers, including audit logs, compliance monitoring, and emergency intervention capabilities.

**Access Control**: Accessible by platform administrators only. Supports read-only impersonation mode for troubleshooting.

**Entry Points**:

- Click team member name/row in Screen 10 (Provider Team Directory)
- Search results from global admin search
- Audit investigation links from compliance reports
- Alert notifications for suspicious activity

**Layout Structure**: Tabbed interface with admin control header

**Header Section**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Profile Photo | image | No | Team member avatar | Read-only; same as provider view |
| Full Name | display (text) | N/A | First name + Last name | Read-only |
| Email | display (email) | N/A | Primary email address | Read-only; clickable to send admin email |
| Provider Organization | display (link) | N/A | Provider name this member belongs to | Click to view provider detail in admin console |
| Role Badge | badge | N/A | Current role with ownership indicator | Color-coded by role |
| Status Indicator | badge | N/A | Active / Invited / Suspended / Flagged | Real-time status; "Flagged" shown if compliance alert exists |
| Account Created | display (timestamp) | N/A | Original account creation date | Relative time with tooltip |
| Last Active | display (timestamp) | N/A | Most recent login or action timestamp | Relative time with tooltip; highlight if >30 days inactive |
| Admin Actions | button group | N/A | Force Suspend, Reset Password, Transfer Ownership (if Owner), View Sessions, Impersonate (Read-Only) | High-privilege actions require re-authentication; MFA-based re-auth is a future enhancement tied to platform-wide MFA rollout |

**Tab 1: Profile & Overview**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Account ID | display (text) | N/A | System-generated unique identifier | Read-only; copyable |
| Member Since | display (date) | N/A | Invitation acceptance date | Read-only |
| Phone Number | display (tel) | No | Contact phone | Masked; admin can reveal with MFA (future enhancement; initially standard re-auth only) |
| Department/Specialty | display (text) | No | Provider-defined label | Read-only; editable by provider only |
| Permission Summary | table | N/A | Current role permissions | Read-only; shows effective permissions |
| Linked Devices | list | N/A | Registered devices for MFA | **Future improvement** – placeholder for when MFA is implemented; includes device type, last used, location |
| Compliance Flags | alert list | N/A | Active compliance issues or investigations | Links to investigation records |
| Account Notes (Admin-Only) | textarea | No | Internal admin notes not visible to provider or member | Max 2000 chars; audit-logged on every edit |

**Tab 2: Complete Activity Audit Log**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Date Range Filter | date picker | No | Filter by start/end date | Defaults to last 90 days; can query up to 2 years |
| Action Type Filter | multi-select dropdown | No | Filter by action categories (Login, Patient Access, Data Export, Settings Change, Communication, Treatment) | Multi-select; includes admin-specific categories |
| Risk Level Filter | dropdown | No | Filter by risk classification (High, Medium, Low) | Auto-classified by system |
| Activity Timeline | list/table | N/A | Chronological list of all actions | Columns: Timestamp, Action Type, Description, Related Entity (link), IP Address, Location, Device, Risk Level |
| IP Address Tracking | display | N/A | Full IP history with geolocation | Shows all IPs used; flags VPN/proxy usage |
| Export Full Audit | button | N/A | Download complete audit trail | CSV/JSON format; includes all fields; requires strong re-authentication (MFA in future release) |
| Flag for Investigation | button | N/A | Mark activity for compliance review | Creates investigation case in FR-031 |
| Pagination Controls | pagination | N/A | Navigate through activity pages | Server-side pagination, 100 events per page |

**Tab 3: Assigned Work**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Work Category Tabs | sub-tabs | N/A | Inquiries, Quotes, Appointments, Messages | Badge shows count per category |
| Work Item List | table | N/A | Context-specific columns per category | Sortable by date, status, priority; includes patient ID, status, assigned date, last activity |
| Patient Link | link | N/A | Links to patient detail page in admin console | Opens patient record in FR-016 (Admin Patient Management) |
| Provider Context | display (badge) | N/A | Shows which provider organization this work belongs to | Always displays since this is admin view |
| Bulk Reassign | button | N/A | Select multiple items and reassign to another member | Opens reassignment workflow; admin can override provider-level restrictions |
| Filter by Status | dropdown | No | Filter work items by status (Draft, Active, Completed, Overdue) | Applies to current category tab |
| Filter by Priority | dropdown | No | Filter by urgency (High, Medium, Low) | Auto-calculated based on SLA deadlines |
| Workload Metrics | display (widget) | N/A | Summary stats: Total items, Overdue count, Avg response time | Provides context for investigations |

**Business Rules**:

- Admins can view assigned work to understand team member's current responsibilities during investigations
- All work items link to relevant patient/inquiry/quote records with proper permissions
- "Overdue" status highlights items past SLA deadlines, supporting compliance reviews
- Bulk reassign available for emergency situations (e.g., team member suspended, provider transition)
- Work item access respects admin permissions defined in FR-031 (Admin Access Control)
- Provides context for questions like: "Why did this member access Patient X's data?" → Check if Patient X is in their assigned work

**Tab 4: Security & Sessions**:

**(Initial FR-009 scope note: Implementation of this tab is deferred for a later improvement phase and is not required for the current build.)*

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Active Sessions | list | N/A | Current logged-in sessions | Shows device, browser, IP, location, started timestamp |
| Session Actions | button group | N/A | Force Logout (single session), Force Logout All | Requires re-authentication; MFA re-auth will be introduced in a future release |
| Login History | table | N/A | Last 100 login attempts | Columns: Timestamp, IP, Location, Device, Success/Failure, Failure Reason |
| Failed Login Count | display (number) | N/A | Failed attempts in last 24 hours | Highlights if >5 attempts |
| MFA Status | badge | N/A | Enabled / Disabled / Enforced | **Future improvement** – will show MFA method (SMS, App, Key) once MFA exists |
| MFA Reset | button | N/A | Force MFA re-enrollment | **Future improvement** – requires MFA re-auth + justification once MFA exists |
| Password Last Changed | display (timestamp) | N/A | Last password change date | Flags if >90 days old |
| Force Password Reset | button | N/A | Invalidate password and require reset | Requires re-authentication + justification (MFA re-auth in future release) |
| Anomaly Alerts | list | N/A | Suspicious login patterns detected by system | E.g., "Login from new country", "Unusual access time" |

**Tab 5: Provider Relationship**:

**(Initial FR-009 scope note: Implementation of this tab is deferred for a later improvement phase and is not required for the current build.)*

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Current Provider | display (link) | N/A | Provider organization name | Click to view provider profile |
| Membership Status | badge | N/A | Active / Pending / Suspended / Removed | Current status |
| Invitation History | table | N/A | All invitations sent to this email | Columns: Date, Inviting Provider, Role Offered, Status |
| Role Change History | table | N/A | All role modifications | Columns: Date, Old Role, New Role, Changed By, Reason |
| Transfer History | table | N/A | Provider membership transfers | If email was moved between providers via FR-031 |
| Transfer to New Provider | button | N/A | Initiate ownership transfer workflow | Opens Screen 13 (Ownership Override Panel) |
| Remove from Provider | button | N/A | Admin-forced removal | Requires re-authentication + justification (MFA requirement deferred to future release); logs high-priority audit event |

**Business Rules**:

- All admin actions (suspend, password reset, session logout, etc.) require strong re-authentication before execution; MFA-based re-authentication is **planned as a future improvement** and is not part of the initial FR-009 scope.
- Every admin action generates high-priority audit log entry with justification field (required).
- Owner records show additional "Ownership Transfer" action that launches Screen 13 workflow.
- "Impersonate (Read-Only)" mode allows admin to view platform as team member would see it, but disables all write actions and displays persistent banner: "Viewing as [Name] - Read-Only Admin Mode."
- Patient data access log obeys data retention policies: anonymized after 1 year, deleted after 2 years (unless part of active investigation).
- Compliance flags automatically trigger notification to admin compliance team via FR-020.
- IP addresses shown in full for admins (not anonymized) to support security investigations.
- Activity log export includes admin metadata (who exported, when, for what case) for chain of custody.

**Notes**:

- Real-time updates via SSE: session changes, login attempts, and activity updates reflected immediately.
- Breadcrumb navigation: Admin Dashboard > Provider Team Directory > [Member Name]
- Mobile responsive with collapsible tabs.
- Supports "Compare Members" feature: select multiple members and compare activity patterns side-by-side (future enhancement).
- Integration with FR-031 (Admin Access Control) for permission checks on sensitive actions.
- Links to patient records respect admin permissions defined in FR-016 (Admin Patient Management).

---

#### Screen 12: Team Size Policy Console

**Purpose**: Centrally configure seat limits and review provider requests.

**Components**:

- Provider detail pane with current limit, utilization, historical changes.
- Request queue (submitted from Screen 1) with approve/deny workflows.
- Automation rules (e.g., auto-approve uplift up to 10 seats for verified providers).

**Business Rules**:

- Changes propagate immediately to provider dashboards via pub/sub.
- Every adjustment recorded with rationale and admin actor.

---

#### Screen 13: Ownership Override Panel

**Purpose**: Allow platform admins to manage exceptional ownership cases.

**Capabilities**:

- Transfer ownership between accounts with dual confirmation.
- Revoke ownership from the current Owner (e.g., compliance issue) while selecting a single successor Owner, preserving the one-owner-per-provider rule.
- Notification hooks into FR-020 templates for affected parties.

**Business Rules**:

- Requires MFA re-auth for admin before finalizing.
- Generates high-priority audit entries flagged for compliance review.

---

## Business Rules

### General Module Rules

- **Rule 1**: Every provider organization must have exactly one Owner at all times (single primary account holder).
- **Rule 2**: Owner role assignments cannot be created, changed, or demoted through the provider platform UI; all ownership creation/transfer/removal flows route to the Admin Platform (FR-031) for manual intervention and audit.
- **Rule 3**: Owner accounts can never perform management actions on their own ownership (no self-removal or self-demotion); ownership changes must be performed by a different authorized actor in the Admin Platform.
- **Rule 4**: Team member accounts are scoped to a single provider organization—an email cannot belong to more than one provider team at a time. Transfers require platform admin intervention.
- **Rule 5**: All team management actions (invite, role change, removal) are logged in audit trail with timestamp, actor, and action details.
- **Rule 6**: Invitation links expire after 7 days—expired invitations can be resent with new expiry.
- **Rule 7**: Maximum team size per provider organization defaults to 100 members and is centrally configured from the Admin Platform (FR-031). Providers submit limit-increase requests that must be approved by platform admins before additional invitations are allowed.
- **Rule 8**: Detailed permission matrices and per-feature toggles are defined centrally in FR-031; FR-009 defines provider team roles and consumes those centrally managed permissions rather than allowing clinics to edit them directly in this module.

### Data & Privacy Rules

- **Privacy Rule 1**: Team member email addresses are visible only within their own provider organization
- **Privacy Rule 2**: Team member activity logs are accessible only to Owners and Admins within same organization
- **Privacy Rule 3**: IP addresses in team member activity logs are retained in full for security and compliance investigations, subject to the global audit log retention and access rules defined in the Constitution
- **Privacy Rule 4**: Removed team members' historical records are archived (not deleted) for compliance—visible only to Owners and platform admins
- **Audit Rule**: All access to team member data must be logged with timestamp, accessing user, and action performed
- **GDPR Compliance**: Team members can request data export (personal data only) and account deletion (marks as deleted, archives for compliance period)

### Admin Editability Rules

**Editable by Admin (Hairline platform admins)**:

- Maximum team size limit per provider (default 100, adjustable 1-500)
- Ownership overrides (promote/demote Owner role) when compliance requires changes; actions logged and not exposed to providers
- Force-transfer of ownership when original Owner leaves organization (performed via Admin Platform only)
- Invitation expiry period (default 7 days, range 1-30 days)
- Activity log retention period (default 2 years, minimum 1 year for compliance)
- Force-suspend individual team member accounts for terms violations
- Force-remove team member in emergency situations (bypasses Owner-only rule)

**Fixed in Codebase (Not Editable)**:

- Role hierarchy and permissions model (Owner > Manager > Clinical > Billing)
- Minimum number of Owners required (always 1)
- Audit log structure and required fields
- Email invitation template structure (content editable, structure fixed)
- Session management security parameters

**Configurable with Restrictions**:

- Admin can view any provider's team structure but cannot modify without provider consent (audit trail logged)
- Admin can suspend team members but cannot delete accounts (compliance requirement)

### Payment & Billing Rules

*Not applicable to this module—team management itself has no direct payment flows. Provider subscription billing (future) may factor in team size.*

---

## Success Criteria

### Provider Efficiency Metrics

- **SC-001**: Provider Owners can invite a new team member in under 2 minutes from dashboard to invitation sent
- **SC-002**: 90% of team member invitations accepted within 48 hours of email receipt
- **SC-003**: Team member role changes apply immediately (within 5 seconds) to active sessions
- **SC-004**: Providers with multi-user teams respond to inquiries 40% faster than single-user providers

### User Experience Metrics

- **SC-005**: 95% of new team members successfully create accounts on first invitation attempt without support assistance
- **SC-006**: Team management dashboard loads in under 2 seconds for provider organizations with up to 100 team members
- **SC-007**: Zero unauthorized access incidents due to improper permission enforcement
- **SC-008**: 100% of role changes reflected correctly in permission checks within 5 seconds

### Admin Management Metrics

- **SC-009**: Platform admins can view team composition for any provider in under 10 seconds
- **SC-010**: 100% of team management actions logged in audit trail with no data loss
- **SC-011**: Emergency team member suspension completes within 30 seconds of admin action

### System Performance Metrics

- **SC-012**: Team management API endpoints respond within 500ms for 95% of requests
- **SC-013**: System supports 500 concurrent team member invitations without degradation
- **SC-014**: Session permission updates propagate to all active sessions within 5 seconds
- **SC-015**: 99.9% uptime for team authentication and authorization services

### Business Impact Metrics

- **SC-016**: 70% of provider organizations with 3+ team members achieve higher patient satisfaction scores than single-user providers
- **SC-017**: Multi-user provider organizations process 50% more inquiries per month than single-user providers
- **SC-018**: Provider churn rate reduced by 25% for organizations using team features (team collaboration increases stickiness)

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **FR-031 / Module A-09**: Admin Access Control & Permissions
  - **Why needed**: Provides the master RBAC framework, default role definitions, and permission matrices that provider teams inherit
  - **Integration point**: Provider team roles are synced with admin-defined permissions; updates from FR-031 propagate to provider invitation, role assignment, and enforcement flows

- **FR-020 / Module S-03**: Notifications & Alerts
  - **Why needed**: Centralizes transactional templates (email + in-app) for invitations, role changes, removals, and reassignment alerts
  - **Integration point**: Team management flows publish notification events consumed by FR-020 channels; template changes propagate without code updates

- **FR-015 / Module A-02**: Provider Management (Admin-Initiated)
  - **Why needed**: Provider organizations and initial owner accounts are created and managed by admins; team members attach to these provider entities
  - **Integration point**: Team member records reference provider organizations and owners created via FR-015 flows

- **FR-032 / Module PR-06**: Provider Dashboard Settings & Profile Management
  - **Why needed**: Owner-level settings (including billing, notification preferences, and profile details) rely on FR-009 roles (especially Owner) for access control
  - **Integration point**: FR-032 screens use FR-009 role permissions (via PR-01/FR-031) to gate access to sensitive settings like billing

- **FR-003 & FR-004 / Module PR-02**: Inquiry Submission & Distribution; Quote Submission & Management
  - **Why needed**: Team members need role-based access to inquiries
  - **Integration point**: Inquiry and quote views apply FR-009 role permissions (via PR-02) when filtering and enforcing what each team member can see and edit

- **FR-010 / Module PR-03**: Treatment Execution & Documentation
  - **Why needed**: Clinical Staff need access to record treatment details
  - **Integration point**: Treatment workflow checks team member role before allowing procedure documentation (only Clinical Staff and, where appropriate, the Owner can act as documenting providers)

- **Module S-03**: Notification Service
  - **Why needed**: Email invitations, role change notifications, removal notifications
  - **Integration point**: Team management triggers send email events to notification service

- **Module S-06**: Audit Log Service
  - **Why needed**: Record all team management actions for compliance
  - **Integration point**: All team management operations write to centralized audit log

### External Dependencies (APIs, Services)

- **External Service 1**: SendGrid/AWS SES (Email Service)
  - **Purpose**: Deliver invitation emails, role change notifications, removal notifications
  - **Integration**: RESTful API calls to send transactional emails with secure token links
  - **Failure handling**: Queue emails for retry (up to 3 attempts with exponential backoff), mark invitation as "Pending Send", background job retries for 24 hours

- **External Service 2**: MaxMind GeoIP (Optional)
  - **Purpose**: Geolocation of IP addresses for security monitoring in activity logs
  - **Integration**: API lookup of IP address to city/country
  - **Failure handling**: Graceful degradation—if service unavailable, show IP address without location

### Data Dependencies

- **Entity 1**: Provider Organization Profile
  - **Why needed**: Team members must be associated with a valid provider organization
  - **Source**: Provider Management (FR-015)

- **Entity 2**: Provider Subscription/Billing Status
  - **Why needed**: Future consideration—team member limits may be tied to subscription tier
  - **Source**: Billing module (future)

---

## Assumptions

### User Behavior Assumptions

- **Assumption 1**: Provider Owners understand the security implications of assigning Owner role to other team members
- **Assumption 2**: Team members invited will have access to their email to receive invitation links within 7 days
- **Assumption 3**: Clinics will clearly define internal role responsibilities before inviting team members to platform
- **Assumption 4**: Team members removed from platform will not require ongoing access to historical data (archival sufficient)

### Technology Assumptions

- **Assumption 1**: Provider staff use modern web browsers (Chrome, Safari, Firefox, Edge - last 2 versions) for accessing provider web app
- **Assumption 2**: Providers have stable internet connectivity for managing team members
- **Assumption 3**: Email delivery is reliable (99%+ delivery rate for transactional emails)
- **Assumption 4**: Session management infrastructure can propagate permission changes within 5 seconds

### Business Process Assumptions

- **Assumption 1**: Provider organizations have 1-20 team members on average (design for up to 100)
- **Assumption 2**: Team composition changes infrequently (1-2 changes per month per provider)
- **Assumption 3**: Providers follow principle of least privilege when assigning roles
- **Assumption 4**: Admins will not need to frequently intervene in provider team management (self-service model)

---

## Implementation Notes

### Technical Considerations

- **Architecture**: Role-based access control (RBAC) model with permissions cached in user session tokens to avoid database lookups on every request
- **Performance**: Team member permissions denormalized into session JWT claims for fast permission checks without database roundtrips
- **Caching**: Team member role changes must invalidate all active sessions for that user within 5 seconds (pub/sub pattern)
- **Storage**: Audit logs stored in append-only ledger for immutability and compliance

### Integration Points

- **Integration 1**: Provider web app calls Team Management API for all CRUD operations
  - **Data format**: JSON payloads with team member details, role enums, timestamps
  - **Authentication**: OAuth 2.0 bearer tokens with role claims
  - **Error handling**: Return 403 Forbidden for permission violations, 409 Conflict for business rule violations

- **Integration 2**: Authentication service validates team member credentials and builds session with role context
  - **Data format**: JWT tokens with claims: user_id, provider_org_id, role, permissions[]
  - **Authentication**: Session token refresh on role change events
  - **Error handling**: Force re-authentication if role change detected

- **Integration 3**: Audit logging service receives events from all team management actions
  - **Data format**: Structured log events with timestamp, actor, action type, target, changes
  - **Authentication**: Internal service-to-service auth
  - **Error handling**: Async event publishing with retry queue

### Scalability Considerations

- **Current scale**: 100-200 provider organizations at launch, average 3-5 team members each = 300-1000 total users
- **Growth projection**: 1000 provider organizations within 12 months, 3000-5000 total users
- **Peak load**: Minimal—team management is infrequent operation (not real-time transactional)
- **Data volume**: Audit logs will grow—expect 10-50 events per provider per month = 500K-1M audit events per year
- **Scaling strategy**: Database read replicas for audit log queries, archive old audit logs to cold storage after 1 year (retain for compliance)

### Security Considerations

- **Authentication**: Team member accounts use same strong authentication as provider owners (password only in initial FR-009 scope; MFA is planned as a future enhancement per Constitution / FR-031 and will be applied platform-wide, including provider admins and staff, in a later release)
- **Authorization**: Every API request validates role permissions before execution—fail closed on permission check errors
- **Encryption**: All team member data encrypted at rest (AES-256), in transit (TLS 1.3)
- **Audit trail**: All team management actions logged with actor, timestamp, IP address, action details
- **Threat mitigation**:
  - Rate limiting on invitation sends (max 10 invitations per hour per provider to prevent abuse)
  - Invitation tokens single-use and time-limited (7 days) to prevent replay attacks
  - Session invalidation on role change to prevent privilege escalation
- **Compliance**: GDPR right-to-access and right-to-deletion supported for team members

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

A coordinator leaves the clinic and the owner needs to remove their access to the platform. The owner removes the team member, reassigns their active inquiries to another coordinator, and the departing team member can no longer log in.

**Why this priority**: Critical for security and compliance—must be able to immediately revoke access for departing staff. Prevents unauthorized data access.

**Independent Test**: Remove an existing team member and verify they can no longer authenticate, and verify their assigned work was reassigned to another team member.

**Acceptance Scenarios**:

1. **Given** owner clicks "Remove" on a team member's row, **When** confirmation dialog appears, **Then** system displays list of team member's active responsibilities (5 active inquiries, 2 draft quotes)
2. **Given** owner is prompted to reassign work, **When** owner selects another coordinator from dropdown as reassignment target, **Then** system confirms reassignment and warns that removed team member will lose access immediately
3. **Given** owner confirms removal, **When** system processes removal, **Then** all active sessions for removed team member are invalidated immediately
4. **Given** removed team member's work was reassigned, **When** new coordinator logs in, **Then** they see the 5 inquiries and 2 draft quotes now assigned to them
5. **Given** removed team member tries to log in, **When** they enter credentials, **Then** authentication fails with message "You no longer have access to this organization. Contact your clinic owner if you believe this is an error."
6. **Given** owner views team dashboard after removal, **When** dashboard refreshes, **Then** removed team member no longer appears in active team list but appears in audit log as "Removed"

---

### User Story 4 - Enforce Single-Provider Membership (Priority: P2)

A clinic owner attempts to invite a surgeon who is currently active in another provider organization. The system blocks the invitation, ensuring staff cannot belong to two providers simultaneously, and guides the owner to request an admin-managed transfer.

**Why this priority**: Prevents compliance issues, billing confusion, and data leakage between providers by enforcing one-organization-per-member.

**Independent Test**: Attempt to invite an email that already belongs to a different provider and verify the system blocks the action with the correct escalation path.

**Acceptance Scenarios**:

1. **Given** a clinician (e.g., Dr. Smith) is an active Clinical Staff member of Provider A, **When** Provider B owner enters <doctor.smith@clinic.com> in the invite form, **Then** system detects the existing membership before sending the invitation.
2. **Given** the conflict is detected, **When** the owner attempts to proceed, **Then** the form displays blocking error copy: "This email already belongs to another provider team. Contact Hairline Admin to request a transfer."
3. **Given** owner clicks "Request Transfer" link, **When** request is submitted, **Then** FR-031 admin console receives a task to review and, upon approval, automatically removes the doctor from Provider A before allowing a new invitation.
4. **Given** the transfer is approved and processed by admins, **When** Provider B re-sends the invitation, **Then** it succeeds because the email is no longer tied to another provider.

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

Each clinic has exactly one primary Owner account. All other elevated users are Admins. The system must prevent creation of additional Owners from the provider UI and ensure that ownership can only be transferred via the Admin Platform (FR-031).

**Why this priority**: Critical business rule that protects organizational integrity—having a single clearly identified Owner simplifies billing, legal responsibility, and access control.

**Independent Test**: Attempt to create or assign a second Owner via all provider-facing flows (invitation form, role edit dialog, admin console actions) and verify that every attempt is blocked with guidance to contact Hairline Admins; verify that system surfaces which account is the current Owner without allowing in-app changes.

**Acceptance Scenarios**:

1. **Given** provider Owner opens the "Invite Team Member" form, **When** they open the Role dropdown, **Then** Owner is visible as a non-selectable option with tooltip "Primary Owner can only be set or changed by Hairline Admins."
2. **Given** any provider user (Owner or Admin) opens the role edit dialog for the current Owner, **When** they attempt to change the role, **Then** the form is disabled and displays callout: "Ownership is managed by Hairline Admins. Please contact support to request changes."
3. **Given** an Admin attempts to update a team member's role to Owner via any provider UI, **When** they submit the change, **Then** system blocks the request with error: "Cannot assign Owner role from provider portal. Contact Hairline Admins."
4. **Given** ownership has been transferred via Admin Platform (FR-031), **When** the provider Owner next logs in, **Then** they see updated Owner designation in the team management screens and cannot modify it themselves.

---

### Edge Cases

- **What happens when invitation email bounces (invalid email address)?**
  System logs bounce event, marks invitation status as "Bounced", and notifies provider owner via in-app notification: "Invitation to [email] failed—email address may be invalid. Please verify and resend."

- **How does system handle provider owner inviting 100+ team members at once?**
  System enforces rate limit: maximum 10 invitations per hour per provider organization. If limit exceeded, display error: "You've reached the invitation limit (10 per hour). Please try again later." This prevents abuse and email service quota exhaustion.

- **What occurs if team member clicks invitation link on mobile device vs desktop?**
  Invitation link and account creation flow are fully responsive—works on any device. After account creation, mobile user is prompted to "Download Mobile App" (if patient platform) or "Bookmark this page" (if provider web app).

- **What happens if owner removes team member while they're actively submitting a quote?**
  System allows in-progress transaction to complete (quote submission succeeds). However, after submission completes, session is invalidated on next request. Team member sees: "Your access has been removed. Please contact clinic owner."

- **How does system handle two admins simultaneously trying to change same team member's role?**
  Optimistic locking: last write wins. First admin's change is applied. Second admin's attempt returns conflict error: "This team member's role was recently changed by [Admin Name]. Please refresh and try again."

---

## Future Improvements: MFA/2FA (Not in Initial FR-009 Scope)

The system-wide Constitution and `system-prd.md` require Multi-Factor Authentication (MFA) for certain user classes (e.g., admin platform users, provider admins). However, **FR-009 focuses on team & role management** and **does not deliver MFA/2FA functionality in its initial implementation**. All MFA-related behaviors referenced in this document are explicitly treated as **future improvements**, to be implemented once the shared authentication/MFA stack is available (primarily via FR-026 App Settings & Security and FR-031 Admin Access Control).

**Deferred items for future implementation (out of scope for current FR-009 build):**

- **Team Member Onboarding (Provider Side)**:
  - MFA enrollment during team member account setup (Screen 8): phone number capture for MFA, MFA factor selection, and enforcement that "password + MFA" must succeed before activation.
- **Admin Console Security Controls**:
  - MFA-gated actions in Screen 11 (Admin Team Member Detail): export full audit requiring MFA, session actions requiring MFA re-auth, MFA Status and MFA Reset controls, and admin-force removal/reset flows that currently mention MFA.
  - Device-level MFA concepts such as "Linked Devices" are documented as placeholders only.
- **Strong Re-Auth vs MFA**:
  - Where this PRD currently mentions "re-authentication" for high-privilege actions, the **initial implementation** will rely on password-based re-auth only. Upgrading these flows to **MFA-backed re-auth** is a **future enhancement** aligned with the platform-wide MFA rollout.

Implementation teams MUST treat the above as **non-blocking, non-MVP requirements** for FR-009 and track them against the corresponding security/MFA epics instead of this feature’s delivery scope.

---

## Functional Requirements Summary

### Core Requirements

> Note: This section summarizes the normative requirements already described in Business Workflows, Screen Specifications, and Business Rules. In case of conflict, the Business Rules section prevails.

- **REQ-009-001**: System MUST allow provider owners to invite team members via email with secure, time-limited invitation links (7-day expiry)
- **REQ-009-002**: System MUST support four distinct provider roles with hierarchical permissions: Owner (Main Account Holder), Manager (Clinic Operations), Clinical Staff, Billing Staff
- **REQ-009-003**: System MUST enforce role-based access control for all provider platform features and data
- **REQ-009-004**: System MUST allow Owners and Managers to modify non-Owner team member roles with immediate permission updates
- **REQ-009-005**: System MUST allow Owners and Managers to remove non-Owner team members with immediate access revocation
- **REQ-009-006**: System MUST enforce "at least one owner" rule—prevent removal or demotion of last owner
- **REQ-009-007**: System MUST send email notifications for team management events (invitation, role change, removal)
- **REQ-009-008**: System MUST enforce single-provider membership—an email can only belong to one provider organization at a time; invitations for emails tied to another provider must be blocked or escalated for admin-managed transfer

### Data Requirements

> Note: Data requirements are summarized here for traceability; field-level definitions and provenance are specified in Screen Specifications and Key Entities.

- **REQ-009-009**: System MUST maintain team member records with: name, email, role, status (Active/Invited/Suspended), invitation date, acceptance date, last activity timestamp
- **REQ-009-010**: System MUST persist invitation records with: token, expiry date, status (Pending/Accepted/Expired/Cancelled), sender, recipient email, role offered
- **REQ-009-011**: System MUST store role permission definitions in configuration (Owner, Manager, Clinical Staff, Billing Staff permission sets)
- **REQ-009-012**: System MUST maintain team member-to-provider organization relationships with role assignment per organization

### Security & Privacy Requirements

> Note: Security and privacy requirements extend the platform-wide Constitution; see Business Rules and the Constitution for non-negotiable baselines.

- **REQ-009-013**: System MUST log all team management actions in audit trail with: timestamp, actor, action type, target team member, old values, new values, IP address
- **REQ-009-014**: System MUST invalidate all active sessions for a team member within 5 seconds of role change or removal
- **REQ-009-015**: System MUST validate actor permissions before allowing any team management action (invite, role change, removal)
- **REQ-009-016**: System MUST generate cryptographically secure, single-use invitation tokens that expire after 7 days
- **REQ-009-017**: System MUST encrypt all team member data at rest (AES-256) and in transit (TLS 1.3)
- **REQ-009-018**: System MUST enforce rate limiting on invitations: maximum 10 invitations per hour per provider organization

### Integration Requirements

> Note: Integration requirements summarize how FR-009 interacts with shared services and other FRs; detailed interaction patterns are documented in Dependencies and Implementation Notes.

- **REQ-009-019**: System MUST integrate with email service to send invitation and notification emails with 99%+ delivery rate
- **REQ-009-020**: System MUST integrate with authentication service to create team member accounts and manage sessions
- **REQ-009-021**: System MUST publish role change events to session management service for real-time permission updates
- **REQ-009-022**: System MUST write all team management events to centralized audit logging service

---

## Key Entities

- **Entity 1 - Team Member**:
  - **Key attributes**: user_id, email, first_name, last_name, status (Active/Invited/Suspended), created_at, last_active_at
  - **Relationships**: One team member belongs to exactly one provider organization at any given time. Transfers require admin-assisted reassignment that archives the old membership before creating a new one. One team member has many audit log entries.

- **Entity 2 - Team Member Organization Role**:
  - **Key attributes**: team_member_id, provider_org_id (unique), role (Owner/Manager/Clinical/Billing), assigned_at, assigned_by
  - **Relationships**: One-to-one mapping per team member ensuring unique provider linkage; record persists for audit/history when transfers occur.

- **Entity 3 - Invitation**:
  - **Key attributes**: invitation_id, token (secure random), email, first_name, last_name, role, provider_org_id, invited_by, status (Pending/Accepted/Expired/Cancelled), expires_at, accepted_at
  - **Relationships**: One invitation belongs to one provider organization. One invitation invited by one existing team member (owner/admin). One invitation may result in one team member account.

- **Entity 4 - Role Permission Definition**:
  - **Key attributes**: role_name (Owner/Manager/Clinical/Billing), permissions[] (array of permission strings like "inquiries.view", "quotes.create", "team.manage")
  - **Relationships**: Static configuration entity. Each team member organization role references one role permission definition.

- **Entity 5 - Team Activity Audit Log**:
  - **Key attributes**: event_id, team_member_id, provider_org_id, timestamp, action_type (Login/InviteSent/RoleChanged/MemberRemoved/QuoteCreated/InquiryViewed), description, ip_address, related_entity_type, related_entity_id
  - **Relationships**: Many audit log entries belong to one team member. Many audit log entries belong to one provider organization.

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-11 | 1.0 | Initial PRD creation for FR-009: Provider Team & Role Management | Claude (AI) |
| 2025-11-21 | 1.1 | **Screen 11 Enhancement**: Added Tab 3 "Assigned Work" to Admin Console Team Member Detail Page (Screen 11) to provide admins with context on current workload during investigations. Renumbered subsequent tabs (Patient Data Access Log → Tab 4, Security & Sessions → Tab 5, Provider Relationship → Tab 6, Compliance & Investigations → Tab 7). Verified necessity of all admin oversight tabs against original transcription requirements. | Claude (AI) |
| 2025-12-03 | 1.2 | **MFA/2FA Scope Clarification for FR-009**: Marked all MFA-related behaviors in team member signup and admin console as future improvements (not in initial implementation scope), while keeping phone number as a required field on Screen 8 for contact and future MFA use. Added explicit **Future Improvements: MFA/2FA** section summarizing deferred items and aligned wording with Constitution / FR-026 / FR-031. | GPT-5.1 (AI) |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | [Name] | [Date] | [Status] |
| Technical Lead | [Name] | [Date] | [Status] |
| Stakeholder | [Name] | [Date] | [Status] |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B
**Based on**: FR-009 from system-prd.md
**Last Updated**: 2025-11-11
