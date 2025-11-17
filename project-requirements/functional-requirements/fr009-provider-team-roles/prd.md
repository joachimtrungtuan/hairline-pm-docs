# Product Requirements Document: Provider Team & Role Management

**Module**: PR-01: Auth & Team Management
**Feature Branch**: `fr009-provider-team-roles`
**Created**: 2025-11-11
**Status**: Draft
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
- **Shared Services (S-02)**: Email service for team member invitations, S-04: Authentication service for team member login

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

**Shared Services (S-02, S-04)**:

- S-02: Email service sends invitation emails with secure signup links
- S-04: Authentication service handles team member account creation, login, password reset
- S-04: Session management maintains role/permission context
- S-05: Audit logging service records all team management actions

### Communication Structure

**In Scope**:

- Email invitations to new team members with secure signup link
- Email notifications when team member role changes
- Email notifications when team member is removed or suspended
- In-platform notifications for team management events

**Out of Scope**:

- SMS notifications for team management (handled by S-03: Notification Service if needed)
- Video tutorials for team onboarding (handled by separate content module)
- Chat/messaging between team members (separate collaboration feature)

### Entry Points

- **Provider Owner**: Accesses team management from provider dashboard main navigation ("Team" tab)
- **Provider Admin**: Accesses limited team management features from settings menu
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
5. Provider Owner enters team member details and selects role (Owner, Admin, Doctor, Coordinator)
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

**A1: Owner invites another Owner**:

- **Trigger**: Provider Owner selects "Owner" role for new team member
- **Steps**:
  1. System displays warning: "Owners have full access including billing and team removal. Are you sure?"
  2. Provider Owner confirms understanding
  3. Invitation proceeds with Owner role
- **Outcome**: New Owner has equal privileges to existing Owner(s)

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

- **Trigger**: Invitee email address already exists in system for another provider
- **Steps**:
  1. System detects existing account during invitation validation
  2. System sends different email: "You've been invited to join [Provider Name] with [Role]"
  3. Team member clicks link and logs in with existing credentials
  4. System presents consent screen: "Accept invitation to join [Provider Name] as [Role]?"
  5. Team member accepts
  6. System adds provider organization to team member's account
  7. Team member can now switch between multiple provider organizations
- **Outcome**: Single team member account linked to multiple provider organizations

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
3. Provider Owner/Admin clicks "Edit" button next to team member name
4. System presents role selection dropdown with current role pre-selected
5. Provider Owner/Admin selects new role from dropdown
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

**A4: Admin trying to change Owner role**:

- **Trigger**: Provider Admin attempts to modify a Provider Owner's role
- **Steps**:
  1. System detects actor role is Admin and target role is Owner
  2. System displays error: "Only Owners can modify other Owners' roles"
  3. Edit dialog closes without making changes
- **Outcome**: Owner role protection maintained

**A5: Last Owner being demoted**:

- **Trigger**: Provider Owner attempts to change own role or another Owner's role when only one Owner remains
- **Steps**:
  1. System counts total Owners in organization
  2. System detects only 1 Owner exists
  3. System displays error: "At least one Owner must remain. Promote another team member to Owner first."
  4. System prevents role change
- **Outcome**: Organization always has at least one Owner

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
  2. System counts remaining Owners
  3. If other Owners exist: Allow removal with extra confirmation
  4. If last Owner: Display error "Cannot remove last Owner. Transfer ownership first."
- **Outcome**: Organization always has at least one Owner

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

### Screen 1: Team Management Dashboard

**Purpose**: Central interface for viewing all team members, their roles, status, and actions available

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Team Member Name | Display (text) | N/A | Full name of team member | Display only |
| Email | Display (email) | N/A | Team member's email address | Display only |
| Role | Display (badge/tag) | N/A | Current role (Owner/Admin/Doctor/Coordinator) | Display only |
| Status | Display (badge) | N/A | Active, Invited, Suspended | Display only |
| Last Active | Display (timestamp) | N/A | Last login or activity timestamp | Display as relative time |
| Actions | Button group | N/A | Edit, Remove, View Activity buttons | Role-based visibility |

**Business Rules**:

- Only Owners and Admins can access team management dashboard
- Owners see all team members including other Owners
- Admins cannot see or modify Owner accounts (except read-only view)
- "Invited" status team members show "Resend Invitation" and "Cancel Invitation" actions
- "Suspended" team members show "Reactivate" action
- Current logged-in user's row is highlighted and shows "(You)" label
- List sorted by: Owners first, then by role hierarchy, then alphabetically by name
- Search/filter box allows filtering by name, email, or role
- Empty state shows "No team members yet. Invite your first team member to get started."

**Notes**:

- Consider pagination or infinite scroll for clinics with 50+ team members
- Quick stats at top: Total team members, Active, Pending invitations, Suspended
- Export button allows downloading team member list (CSV) for auditing

---

### Screen 2: Invite Team Member Form

**Purpose**: Collect information needed to invite a new team member to the provider organization

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| First Name | text | Yes | Team member's first name | 2-50 characters, letters, spaces, hyphens |
| Last Name | text | Yes | Team member's last name | 2-50 characters, letters, spaces, hyphens |
| Email | email | Yes | Team member's work email | Valid email format, unique within org |
| Role | select/dropdown | Yes | Role to assign (Owner/Admin/Doctor/Coordinator) | Must select one option |
| Personal Message | textarea | No | Optional message to include in invitation email | Max 500 characters |

**Business Rules**:

- Email must not already exist as active or invited team member in this organization
- Email format validated on blur
- Role dropdown shows role name with brief description of permissions
- If selecting "Owner" role, display warning banner: "Owners have full access including billing and ability to remove other team members"
- Personal message preview shown below textarea
- Form requires explicit "Send Invitation" button click (no auto-submit)
- After submission, form clears and returns to team dashboard
- Success toast notification: "Invitation sent to [email]"

**Notes**:

- Consider adding profile photo upload (optional) for immediate team roster completeness
- Allow bulk invite via CSV upload for large clinic onboarding (future enhancement)
- Provide "Save as Draft" option for partial invitations (future enhancement)

---

### Screen 3: Edit Team Member Role Dialog

**Purpose**: Modify an existing team member's role and view permission changes

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Team Member Name | Display (text) | N/A | Full name of team member being edited | Read-only |
| Current Role | Display (badge) | N/A | Existing role | Read-only |
| New Role | select/dropdown | Yes | Role to change to | Must select different role |
| Permission Comparison | Display (table) | N/A | Side-by-side permissions for current vs new role | Read-only |
| Reason for Change | textarea | No | Optional reason for audit trail | Max 250 characters |

**Business Rules**:

- Cannot change last Owner in organization to non-Owner role
- Admin users cannot change Owner roles
- Cannot change own role (must be done by another Owner/Admin)
- Permission comparison table shows: Permission category, Current access (checkmark/X), New access (checkmark/X)
- Permissions being removed are highlighted in red
- Permissions being added are highlighted in green
- "Update Role" button disabled until new role selected and different from current
- Confirmation required if removing critical permissions (e.g., Owner → Admin loses billing access)

**Notes**:

- Consider showing impact statement: "This change will affect X active inquiries and Y draft quotes"
- Add "Notify team member" checkbox (default checked) to optionally suppress email notification

---

### Screen 4: Team Member Activity Log

**Purpose**: View audit trail of actions performed by a specific team member for accountability and compliance

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Timestamp | Display (datetime) | N/A | When action occurred | ISO format, display in local timezone |
| Action Type | Display (badge) | N/A | Category: Login, Quote Created, Inquiry Viewed, etc. | Read-only |
| Description | Display (text) | N/A | Human-readable description of action | Read-only |
| IP Address | Display (text) | N/A | IP address of action origin | Display only for Owners |
| Related Entity | Link | N/A | Link to related inquiry, quote, patient, etc. | Clickable if entity still exists |

**Business Rules**:

- Only Owners and Admins can view activity logs
- Admins can only view logs for non-Owner team members
- Logs retained for minimum 2 years for compliance
- Sensitive actions flagged: Patient data access, quote submission, payment handling
- Filter options: Date range, action type, related entity type
- Export button downloads filtered logs as CSV
- Pagination: 50 events per page
- Real-time updates: New actions appear without page refresh

**Notes**:

- Consider anonymizing IP addresses after 90 days for privacy compliance
- Add "Flag for Review" button for suspicious activity
- Show geolocation of IP address for security monitoring (city/country level)

---

## Business Rules

### General Module Rules

- **Rule 1**: Every provider organization must have at least one Owner at all times
- **Rule 2**: Team member accounts are scoped to provider organizations—one email can be associated with multiple provider organizations with different roles
- **Rule 3**: All team management actions (invite, role change, removal) are logged in audit trail with timestamp, actor, and action details
- **Rule 4**: Invitation links expire after 7 days—expired invitations can be resent with new expiry
- **Rule 5**: Maximum team size per provider organization: 100 members (soft limit, can be increased by admin)

### Data & Privacy Rules

- **Privacy Rule 1**: Team member email addresses are visible only within their own provider organization
- **Privacy Rule 2**: Team member activity logs are accessible only to Owners and Admins within same organization
- **Privacy Rule 3**: IP addresses in activity logs are anonymized after 90 days (retain only country-level location)
- **Privacy Rule 4**: Removed team members' historical records are archived (not deleted) for compliance—visible only to Owners and platform admins
- **Audit Rule**: All access to team member data must be logged with timestamp, accessing user, and action performed
- **GDPR Compliance**: Team members can request data export (personal data only) and account deletion (marks as deleted, archives for compliance period)

### Admin Editability Rules

**Editable by Admin (Hairline platform admins)**:

- Maximum team size limit per provider (default 100, adjustable 1-500)
- Invitation expiry period (default 7 days, range 1-30 days)
- Activity log retention period (default 2 years, minimum 1 year for compliance)
- Force-suspend individual team member accounts for terms violations
- Force-remove team member in emergency situations (bypasses Owner-only rule)

**Fixed in Codebase (Not Editable)**:

- Role hierarchy and permissions model (Owner > Admin > Doctor > Coordinator)
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

- **FR-006 / Module PR-01**: Provider Authentication & Profile
  - **Why needed**: Team members must authenticate through provider auth system
  - **Integration point**: Team member accounts use same authentication service, session management, and login flows as provider owners

- **FR-007 / Module PR-02**: Provider Inquiry Management
  - **Why needed**: Team members need role-based access to inquiries
  - **Integration point**: Inquiry views filter and permission checks based on team member role

- **FR-008 / Module PR-03**: Provider Quote Management
  - **Why needed**: Doctors and Coordinators need access to create and manage quotes
  - **Integration point**: Quote creation and editing respects role permissions

- **FR-010 / Module PR-04**: Treatment Execution & Documentation
  - **Why needed**: Doctors need access to record treatment details
  - **Integration point**: Treatment workflow checks team member role before allowing procedure documentation

- **Module S-02**: Notification Service
  - **Why needed**: Email invitations, role change notifications, removal notifications
  - **Integration point**: Team management triggers send email events to notification service

- **Module S-04**: Authentication & Authorization Service
  - **Why needed**: Centralized auth for all team members, session management
  - **Integration point**: Team member login, password reset, session tokens

- **Module S-05**: Audit Logging Service
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
  - **Source**: Provider onboarding (FR-001)

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

- **Authentication**: Team member accounts use same strong authentication as provider owners (password + optional MFA)
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

A clinic owner has been using the platform solo and now wants to bring their office coordinator onto the platform to help manage patient inquiries and scheduling. The owner invites the coordinator, who successfully creates an account and starts managing inquiries.

**Why this priority**: Core functionality—without team invitations, multi-user collaboration is impossible. This is the foundational feature that unlocks all other team management capabilities.

**Independent Test**: Can be fully tested by inviting a new team member via email, having them create an account, and verifying they can log in and access features appropriate to their assigned role.

**Acceptance Scenarios**:

1. **Given** clinic owner is logged into provider dashboard, **When** they navigate to "Team" tab and click "Invite Team Member", **Then** invitation form appears with fields for name, email, role, and optional message
2. **Given** owner fills out invitation form with coordinator details and role "Coordinator", **When** they click "Send Invitation", **Then** system sends email to coordinator with invitation link and displays success confirmation
3. **Given** coordinator receives invitation email, **When** they click the invitation link, **Then** they are directed to account creation page with email and name pre-filled
4. **Given** coordinator creates password and accepts terms, **When** they submit account creation form, **Then** account is created with Coordinator role and they can immediately log in
5. **Given** coordinator logs in for first time, **When** they access dashboard, **Then** they see only features and data appropriate to Coordinator role (can view inquiries, manage schedules, but cannot access billing)

---

### User Story 2 - Owner Changes Team Member Role (Priority: P1)

A doctor who was initially invited as a "Doctor" (limited to treatment execution) is being promoted to "Admin" to help with operational management and team oversight. The owner changes their role and the doctor immediately gains access to additional features.

**Why this priority**: Role changes are common as team members grow in responsibility or as organizational needs change. Must work reliably to maintain proper access control.

**Independent Test**: Invite a team member with one role, then edit their role to a different one, and verify permissions update immediately in their active session.

**Acceptance Scenarios**:

1. **Given** owner is viewing team management dashboard, **When** they click "Edit" on a team member row, **Then** role editing dialog appears showing current role and dropdown to select new role
2. **Given** owner selects new role "Admin" for team member currently "Doctor", **When** permission comparison table is displayed, **Then** owner can see which permissions are being added (e.g., team management, analytics) and which remain unchanged
3. **Given** owner reviews permission changes and clicks "Update Role", **When** system processes the change, **Then** team member's role is updated in database and email notification sent to affected team member
4. **Given** affected team member is actively logged in during role change, **When** they navigate to a new page or refresh, **Then** new permissions are immediately reflected (can now access Admin menu items)
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

### User Story 4 - Team Member Accepts Invitation to Join Second Provider (Priority: P2)

A doctor who already has an account with Provider A is invited by Provider B to also work with them part-time. The doctor accepts the invitation and can now switch between both provider organizations from a single account.

**Why this priority**: Supports real-world scenario where medical professionals work with multiple clinics. Improves user experience by avoiding multiple accounts.

**Independent Test**: Invite an existing team member (with account at different provider) to a second provider organization and verify they can switch between both organizations.

**Acceptance Scenarios**:

1. **Given** Provider B owner invites doctor using email that already exists for Provider A, **When** invitation is sent, **Then** system detects existing account and sends special email: "You've been invited to join [Provider B] as Doctor"
2. **Given** doctor receives invitation email, **When** they click invitation link, **Then** they are directed to login page (not account creation) with message "Log in to accept invitation to [Provider B]"
3. **Given** doctor logs in with existing credentials, **When** authentication succeeds, **Then** consent screen appears: "Accept invitation to join [Provider B] with role Doctor?"
4. **Given** doctor clicks "Accept", **When** system processes acceptance, **Then** Provider B is added to doctor's account and they see organization switcher in navigation
5. **Given** doctor has access to multiple organizations, **When** they use organization switcher dropdown, **Then** they can seamlessly switch between Provider A and Provider B with appropriate role/permissions for each

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

### User Story 6 - System Enforces "At Least One Owner" Rule (Priority: P1)

A clinic has two owners. One owner attempts to remove themselves from the team. The system allows the removal since another owner remains. However, when the second owner tries to remove themselves or change their role, the system prevents it to ensure at least one owner always exists.

**Why this priority**: Critical business rule that protects organizational integrity—without an owner, the provider organization would be orphaned and unmanageable.

**Independent Test**: Create scenario with two owners, remove one successfully, then attempt to remove or demote the last owner and verify system prevents it.

**Acceptance Scenarios**:

1. **Given** provider organization has two owners (Owner A and Owner B), **When** Owner A clicks "Remove" on their own account, **Then** system allows removal with confirmation: "Another owner will remain (Owner B). Proceed?"
2. **Given** Owner A confirms self-removal, **When** system processes removal, **Then** Owner A's access is revoked and Owner B remains as sole owner
3. **Given** Owner B (now sole owner) attempts to remove themselves, **When** they click "Remove" on own account, **Then** system displays error: "Cannot remove last owner. Promote another team member to Owner first or transfer ownership."
4. **Given** Owner B attempts to change own role from Owner to Admin, **When** they select new role in edit dialog, **Then** system displays error: "At least one Owner must remain. Promote another team member to Owner first."
5. **Given** Owner B promotes another team member to Owner, **When** promotion completes, **Then** Owner B can now remove themselves or change own role (since two owners exist again)

---

### Edge Cases

- **What happens when invitation email bounces (invalid email address)?**
  System logs bounce event, marks invitation status as "Bounced", and notifies provider owner via in-app notification: "Invitation to [email] failed—email address may be invalid. Please verify and resend."

- **How does system handle provider owner inviting 100+ team members at once?**
  System enforces rate limit: maximum 10 invitations per hour per provider organization. If limit exceeded, display error: "You've reached the invitation limit (10 per hour). Please try again later." This prevents abuse and email service quota exhaustion.

- **What occurs if team member clicks invitation link on mobile device vs desktop?**
  Invitation link and account creation flow are fully responsive—works on any device. After account creation, mobile user is prompted to "Download Mobile App" (if patient platform) or "Bookmark this page" (if provider web app).

- **How to manage team member who belongs to 10+ provider organizations?**
  Organization switcher becomes dropdown menu with search/filter capability. Recent organizations appear at top. Pin favorite organizations for quick access. Limit: maximum 20 provider organizations per team member account (soft limit, can be increased by admin).

- **What happens if owner removes team member while they're actively submitting a quote?**
  System allows in-progress transaction to complete (quote submission succeeds). However, after submission completes, session is invalidated on next request. Team member sees: "Your access has been removed. Please contact clinic owner."

- **How does system handle two admins simultaneously trying to change same team member's role?**
  Optimistic locking: last write wins. First admin's change is applied. Second admin's attempt returns conflict error: "This team member's role was recently changed by [Admin Name]. Please refresh and try again."

---

## Functional Requirements Summary

### Core Requirements

- **FR-001**: System MUST allow provider owners to invite team members via email with secure, time-limited invitation links (7-day expiry)
- **FR-002**: System MUST support four distinct roles with hierarchical permissions: Owner, Admin, Doctor, Coordinator
- **FR-003**: System MUST enforce role-based access control for all provider platform features and data
- **FR-004**: System MUST allow owners and admins to modify team member roles with immediate permission updates
- **FR-005**: System MUST allow owners and admins to remove team members with immediate access revocation
- **FR-006**: System MUST enforce "at least one owner" rule—prevent removal or demotion of last owner
- **FR-007**: System MUST send email notifications for team management events (invitation, role change, removal)
- **FR-008**: System MUST support multi-organization accounts—one email can be team member at multiple providers with different roles

### Data Requirements

- **FR-009**: System MUST maintain team member records with: name, email, role, status (Active/Invited/Suspended), invitation date, acceptance date, last activity timestamp
- **FR-010**: System MUST persist invitation records with: token, expiry date, status (Pending/Accepted/Expired/Cancelled), sender, recipient email, role offered
- **FR-011**: System MUST store role permission definitions in configuration (Owner, Admin, Doctor, Coordinator permission sets)
- **FR-012**: System MUST maintain team member-to-provider organization relationships with role assignment per organization

### Security & Privacy Requirements

- **FR-013**: System MUST log all team management actions in audit trail with: timestamp, actor, action type, target team member, old values, new values, IP address
- **FR-014**: System MUST invalidate all active sessions for a team member within 5 seconds of role change or removal
- **FR-015**: System MUST validate actor permissions before allowing any team management action (invite, role change, removal)
- **FR-016**: System MUST generate cryptographically secure, single-use invitation tokens that expire after 7 days
- **FR-017**: System MUST encrypt all team member data at rest (AES-256) and in transit (TLS 1.3)
- **FR-018**: System MUST enforce rate limiting on invitations: maximum 10 invitations per hour per provider organization

### Integration Requirements

- **FR-019**: System MUST integrate with email service to send invitation and notification emails with 99%+ delivery rate
- **FR-020**: System MUST integrate with authentication service to create team member accounts and manage sessions
- **FR-021**: System MUST publish role change events to session management service for real-time permission updates
- **FR-022**: System MUST write all team management events to centralized audit logging service

---

## Key Entities

- **Entity 1 - Team Member**:
  - **Key attributes**: user_id, email, first_name, last_name, status (Active/Invited/Suspended), created_at, last_active_at
  - **Relationships**: One team member can belong to many provider organizations (multi-organization support). Each membership has a role assignment. One team member has many audit log entries.

- **Entity 2 - Team Member Organization Role**:
  - **Key attributes**: team_member_id, provider_org_id, role (Owner/Admin/Doctor/Coordinator), assigned_at, assigned_by
  - **Relationships**: Links team member to provider organization with specific role. Many-to-many join entity.

- **Entity 3 - Invitation**:
  - **Key attributes**: invitation_id, token (secure random), email, first_name, last_name, role, provider_org_id, invited_by, status (Pending/Accepted/Expired/Cancelled), expires_at, accepted_at
  - **Relationships**: One invitation belongs to one provider organization. One invitation invited by one existing team member (owner/admin). One invitation may result in one team member account.

- **Entity 4 - Role Permission Definition**:
  - **Key attributes**: role_name (Owner/Admin/Doctor/Coordinator), permissions[] (array of permission strings like "inquiries.view", "quotes.create", "team.manage")
  - **Relationships**: Static configuration entity. Each team member organization role references one role permission definition.

- **Entity 5 - Team Activity Audit Log**:
  - **Key attributes**: event_id, team_member_id, provider_org_id, timestamp, action_type (Login/InviteSent/RoleChanged/MemberRemoved/QuoteCreated/InquiryViewed), description, ip_address, related_entity_type, related_entity_id
  - **Relationships**: Many audit log entries belong to one team member. Many audit log entries belong to one provider organization.

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-11 | 1.0 | Initial PRD creation for FR-009: Provider Team & Role Management | Claude (AI) |

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
