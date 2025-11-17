# Product Requirements Document: Admin Access Control & Permissions

**Module**: A-09: System Settings & Configuration
**Feature Branch**: `fr031-admin-access-control`
**Created**: 2025-11-14
**Status**: Draft
**Source**: FR-031 from system-prd.md

---

## Executive Summary

The Admin Access Control & Permissions module provides a comprehensive role-based access control (RBAC) system for the Hairline Admin Platform, enabling secure and granular management of admin team members and their permissions. This module ensures that admin staff have appropriate access to platform features based on their role (aftercare specialist, billing staff, support staff, super admin), while maintaining full auditability and compliance with healthcare data security requirements.

This module directly supports Principle II (Medical Data Privacy & Security) and Principle VI (Data Integrity & Audit Trail) from the Hairline Platform Constitution by enforcing the principle of least privilege and maintaining comprehensive audit trails of all permission changes and admin actions.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-XX)**: Not applicable - this module operates exclusively within Admin Platform
- **Provider Platform (PR-XX)**: Not applicable - provider team management handled separately in PR-01
- **Admin Platform (A-09)**: Complete admin user, role, and permission management system
- **Shared Services (S-XX)**: None required - module operates as standalone admin capability

### Multi-Tenant Breakdown

**Patient Platform (P-XX)**:

- No patient-facing functionality

**Provider Platform (PR-XX)**:

- No provider-facing functionality
- Provider platform has its own separate team management in PR-01 (not part of this FR)

**Admin Platform (A-09)**:

- Admin staff member invitation and management
- Role creation and configuration
- Permission matrix definition and assignment
- Team member role assignment
- Access control enforcement across all admin features
- Audit trail of permission changes and administrative actions

**Shared Services (S-XX)**:

- No shared services required
- Permission checks executed within admin platform backend

### Communication Structure

**In Scope**:

- Email notifications for admin team member invitations
- Email notifications for role assignment changes
- Email notifications for permission changes (to affected admin users)
- System notifications for access denial attempts

**Out of Scope**:

- SMS notifications (handled by S-03: Notification Service if needed)
- Real-time permission updates via WebSocket (V2 enhancement)
- External identity provider integration (OAuth, SAML - V2 enhancement)

### Entry Points

- **Super Admin Access**: Super admins access "User & Permission Management" section from Admin Platform settings menu
- **Initial Setup**: First super admin account created during platform deployment/installation
- **Team Member Onboarding**: New admin staff members receive invitation email with account activation link
- **Permission Enforcement**: All admin API endpoints and UI components check permissions on every request
- **Audit Trail Access**: Admin actions logged automatically and viewable in audit trail interface

---

## Business Workflows

### Main Flow: Admin Team Member Invitation

**Actors**: Super Admin, New Admin User, System
**Trigger**: Super Admin clicks "Invite Team Member" button in User Management screen
**Outcome**: New admin account created with assigned role and permissions, invitation email sent

**Steps**:

1. Super Admin navigates to User & Permission Management section
2. Super Admin clicks "Invite Team Member" button
3. System displays invitation form with fields: email, name, assigned role
4. Super Admin enters: email address, full name, selects role from dropdown (e.g., "Aftercare Specialist")
5. System validates: email format, email not already in use, role exists
6. Super Admin clicks "Send Invitation"
7. System creates new admin account with status "Pending Activation"
8. System assigns selected role to new account
9. System generates unique activation token (expires in 72 hours)
10. System sends invitation email with activation link and role information
11. System displays confirmation: "Invitation sent to [email]"
12. New Admin User receives email and clicks activation link
13. System validates token (not expired, not already used)
14. System displays password setup screen
15. New Admin User enters password (meeting password requirements)
16. System activates account and sets status to "Active"
17. System redirects to login screen with success message
18. New Admin User logs in and sees dashboard with role-appropriate features

### Alternative Flows

**A1: Re-send Invitation (Token Expired)**:

- **Trigger**: Admin team member did not activate account within 72 hours
- **Steps**:
  1. Super Admin views pending invitations list
  2. Super Admin identifies expired invitation (status: "Expired")
  3. Super Admin clicks "Re-send Invitation" button
  4. System generates new activation token (72-hour expiry)
  5. System sends new invitation email
  6. System updates invitation status to "Pending Activation"
- **Outcome**: New invitation email sent with fresh activation link

**A2: Role Change for Existing Admin User**:

- **Trigger**: Admin user's responsibilities change, requiring different role
- **Steps**:
  1. Super Admin navigates to active team members list
  2. Super Admin selects target admin user
  3. Super Admin clicks "Change Role" button
  4. System displays role change dialog with current role highlighted
  5. Super Admin selects new role from dropdown
  6. System displays permission comparison (current vs new role permissions)
  7. Super Admin confirms role change
  8. System updates user's role assignment
  9. System logs role change in audit trail (who changed, old role, new role, timestamp)
  10. System sends email notification to affected user about role change
  11. System immediately enforces new role permissions (next API call reflects new permissions)
- **Outcome**: Admin user's permissions updated to match new role

**A3: Create Custom Role**:

- **Trigger**: Super Admin needs role not covered by standard roles (e.g., specialized analytics-only role)
- **Steps**:
  1. Super Admin navigates to Roles & Permissions tab
  2. Super Admin clicks "Create New Role"
  3. System displays role creation form
  4. Super Admin enters: role name, role description
  5. Super Admin selects permissions from permission matrix (checkboxes for each feature)
  6. System displays permission summary and potential conflicts/warnings
  7. Super Admin clicks "Create Role"
  8. System validates: unique role name, at least one permission selected
  9. System saves new role definition
  10. System logs role creation in audit trail
  11. New role appears in role dropdown for team member assignment
- **Outcome**: New custom role available for assignment to admin users

**B1: Invalid Email Address**:

- **Trigger**: Super Admin enters malformed email address
- **Steps**:
  1. System validates email format on form submission
  2. System displays inline error: "Invalid email format. Please enter valid email address."
  3. Super Admin corrects email address
  4. Super Admin re-submits form
  5. System proceeds with invitation if validation passes
- **Outcome**: Validation error prevents invitation with invalid email

**B2: Email Already in Use**:

- **Trigger**: Super Admin attempts to invite user with email already associated with active or pending account
- **Steps**:
  1. System checks email uniqueness against existing admin accounts
  2. System displays error message: "An admin account with this email already exists. Status: [Active/Pending]. To re-send invitation, go to Pending Invitations."
  3. Super Admin cancels invitation or corrects email address
- **Outcome**: Duplicate account prevented; user directed to re-send invitation flow if needed

**B3: Unauthorized Access Attempt**:

- **Trigger**: Admin user attempts to access feature not permitted by their role
- **Steps**:
  1. Admin user clicks on restricted feature (e.g., Billing section)
  2. System checks user's permissions against required permission
  3. System denies access and displays message: "Access Denied: You do not have permission to access this feature. Contact your administrator if you need access."
  4. System logs access denial attempt in audit trail (user, feature, timestamp, IP address)
  5. System sends alert to Super Admin if multiple failed attempts detected (potential security issue)
- **Outcome**: Unauthorized access blocked; security event logged

**B4: Permission Conflict on Role Assignment**:

- **Trigger**: Super Admin attempts to assign role that would create permission conflict (e.g., read-only analyst assigned to billing role)
- **Steps**:
  1. System detects conflicting permissions during role assignment
  2. System displays warning: "This role has permissions that conflict with user's current constraints. Review permissions before proceeding."
  3. System highlights conflicting permissions
  4. Super Admin reviews conflicts and either: (a) proceeds with assignment, or (b) cancels and creates custom role
- **Outcome**: Permission conflicts identified and resolved before assignment

---

## Screen Specifications

### Screen 1: User & Permission Management Dashboard

**Purpose**: Provides overview of all admin team members, pending invitations, and quick access to user management actions

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Active Users Count | number (read-only) | N/A | Total number of active admin accounts | Auto-calculated |
| Pending Invitations Count | number (read-only) | N/A | Number of invitations awaiting activation | Auto-calculated |
| User Search | text | No | Search by name or email | Real-time filter |
| Role Filter | select (dropdown) | No | Filter users by assigned role | Multi-select allowed |
| Status Filter | select (dropdown) | No | Filter by Active/Pending/Suspended | Single select |

**Data Table - Active Users**:

| Column | Type | Description | Actions |
|--------|------|-------------|---------|
| Name | text | Admin user full name | Click to view details |
| Email | text | Admin user email address | - |
| Role | text | Assigned role name | Clickable to change |
| Last Login | datetime | Timestamp of most recent login | Relative format (e.g., "2 hours ago") |
| Status | badge | Active/Suspended | Color-coded |
| Actions | buttons | Change Role, Suspend, View Audit | Dropdown menu |

**Business Rules**:

- Super Admin accounts cannot be suspended by other users (system protection)
- At least one active Super Admin must exist at all times (prevent lockout)
- Suspended users cannot log in but accounts remain in system (soft suspension)
- Search filters users in real-time without page reload
- Pagination: Display 25 users per page with "Load More" option
- Sort columns: Name (A-Z), Last Login (most recent first), Role (alphabetical)

**Notes**:

- Display warning banner if only one Super Admin exists: "Warning: Only one Super Admin account. Consider adding backup admin."
- Show notification dot on Pending Invitations tab if invitations are about to expire (< 24 hours)
- Export user list to CSV with all columns and applied filters

---

### Screen 2: Invite Team Member Form

**Purpose**: Allows Super Admin to invite new admin team members with role assignment

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Email Address | text (email input) | Yes | New admin user's email | Valid email format; unique (not in use) |
| Full Name | text | Yes | Admin user's display name | Max 100 characters |
| Assigned Role | select (dropdown) | Yes | Role to assign to new user | Must select from available roles |
| Send Welcome Email | checkbox | No | Include platform overview in invitation | Default: checked |

**Business Rules**:

- Email validation occurs on blur (field loses focus) for immediate feedback
- Role dropdown populated from active roles only (archived roles excluded)
- Role dropdown displays: role name + brief description on hover
- "Send Welcome Email" option adds additional onboarding content to invitation email
- Form cannot be submitted until all required fields pass validation
- Invitation token expires after 72 hours (configurable in A-09 settings)

**Notes**:

- Display role permission summary below role dropdown (expandable section)
- Show estimated invitation expiry time: "Invitation will expire on [date] at [time]"
- Provide "Preview Invitation Email" button to review email before sending

---

### Screen 3: Role & Permission Matrix

**Purpose**: Allows Super Admin to create, edit, and manage roles with granular permission assignment

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Role Name | text | Yes | Name of role (e.g., "Aftercare Specialist") | Max 50 chars; unique |
| Role Description | textarea | Yes | Purpose and responsibilities of role | Max 500 chars |
| Permission Categories | accordion | Yes | Grouped permissions by feature area | At least one permission required |

**Permission Matrix Structure** (Expandable Categories):

**Category: Patient Management (A-01)**:

| Permission | Description | Access Level |
|------------|-------------|--------------|
| View Patients | View patient list and profiles | ☐ Read |
| Edit Patients | Modify patient information | ☐ Write |
| Delete Patients | Archive patient accounts | ☐ Delete |

**Category: Provider Management (A-02)**:

| Permission | Description | Access Level |
|------------|-------------|--------------|
| View Providers | View provider list and profiles | ☐ Read |
| Edit Providers | Modify provider information | ☐ Write |
| Onboard Providers | Create new provider accounts | ☐ Write |
| Suspend Providers | Suspend/activate provider accounts | ☐ Delete |

**Category: Aftercare Management (A-03)**:

| Permission | Description | Access Level |
|------------|-------------|--------------|
| View Aftercare Cases | View aftercare patient list | ☐ Read |
| Manage Aftercare | Assign specialists, edit plans | ☐ Write |
| Chat with Patients | Access aftercare chat | ☐ Write |
| Schedule Consultations | Book video consultations | ☐ Write |

**Category: Billing & Financial (A-05)**:

| Permission | Description | Access Level |
|------------|-------------|--------------|
| View Transactions | View patient and provider transactions | ☐ Read |
| Process Payouts | Initiate provider payouts | ☐ Write |
| Issue Refunds | Process patient refunds | ☐ Write (requires approval) |
| View Financial Reports | Access revenue analytics | ☐ Read |

**Category: System Settings (A-09)**:

| Permission | Description | Access Level |
|------------|-------------|--------------|
| View Settings | View system configuration | ☐ Read |
| Edit Settings | Modify system settings | ☐ Write (Super Admin only) |
| Manage Users | Create/edit admin accounts | ☐ Write (Super Admin only) |
| Manage Roles | Create/edit roles and permissions | ☐ Write (Super Admin only) |

**Business Rules**:

- Permissions organized by module code (A-01, A-02, etc.) for traceability
- "Select All" checkbox available for each category
- Permission dependencies highlighted (e.g., "Edit Patients" requires "View Patients")
- System prevents creating role with zero permissions
- Super Admin permissions cannot be removed from Super Admin role (system protection)
- Permission changes take effect immediately for all users with that role (next API call)
- Role edits logged in audit trail with before/after permission comparison

**Notes**:

- Display warning when granting sensitive permissions (billing, user management)
- Show number of users currently assigned to role being edited
- Provide "Clone Role" option to create new role based on existing one
- Export permission matrix to CSV for documentation purposes

---

### Screen 4: User Detail & Audit Trail

**Purpose**: Displays comprehensive information about specific admin user including activity history and permission changes

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| User Profile | section (read-only) | N/A | Name, email, role, status, created date | - |
| Current Role | badge | N/A | Currently assigned role with color coding | - |
| Last Login | datetime | N/A | Most recent successful login | - |
| Login Count | number | N/A | Total number of logins since account creation | - |
| Account Status | badge | N/A | Active/Suspended/Pending | - |

**Audit Trail Table**:

| Column | Type | Description | Format |
|--------|------|-------------|--------|
| Timestamp | datetime | When action occurred | "2025-11-14 14:32:15 UTC" |
| Action Type | text | Type of action (Login, Role Change, Permission Grant, Access Denied) | Badge with color |
| Details | text | Description of action | "Role changed from 'Support Staff' to 'Aftercare Specialist' by <admin@hairline.com>" |
| IP Address | text | IP address of action (security audit) | "192.168.1.1" |
| Outcome | badge | Success/Failed/Denied | Color-coded |

**Business Rules**:

- Audit trail shows last 100 actions by default with "Load More" option
- Audit trail searchable by action type, date range, outcome
- Audit entries immutable (cannot be edited or deleted)
- Login failures logged with reason (invalid password, account suspended, etc.)
- Access denial attempts logged with requested feature/endpoint
- Audit trail exportable to CSV for compliance reporting
- Sensitive actions (role changes, permission grants) highlighted in audit trail

**Notes**:

- Display security alerts if suspicious activity detected (multiple failed logins, unusual access patterns)
- Provide "Send Password Reset" button for Super Admins (forces password reset on next login)
- Show comparison view when viewing role change events (old role permissions vs new role permissions)

---

## Business Rules

### General Module Rules

- **Rule 1**: All admin users MUST have at least one role assigned (no "roleless" accounts)
- **Rule 2**: Super Admin role MUST always have full system access (cannot be restricted)
- **Rule 3**: Permission changes take effect immediately (no caching; enforced on next API call)
- **Rule 4**: At least one active Super Admin account MUST exist at all times (system protection against lockout)
- **Rule 5**: All administrative actions (role changes, permission grants, user suspensions) MUST be logged in audit trail
- **Rule 6**: Invitation tokens expire after 72 hours (configurable via A-09 settings)
- **Rule 7**: Suspended admin users cannot log in but accounts remain in system (soft suspension, not deletion)

### Data & Privacy Rules

- **Privacy Rule 1**: Audit trail entries are immutable and retained for 10 years (compliance requirement per Constitution Principle VI)
- **Privacy Rule 2**: IP addresses logged for security audit purposes (GDPR-compliant logging)
- **Privacy Rule 3**: Password reset requests logged in audit trail with requester identity
- **Audit Rule**: All access to sensitive features (billing, patient medical data, provider financial data) MUST be logged with: timestamp, user ID, action, IP address, outcome
- **GDPR Compliance**: Admin user data (email, name) can be anonymized on account deletion request, but audit trail preserved with anonymized identifiers

### Admin Editability Rules

**Editable by Super Admin**:

- Create, edit, delete custom roles
- Assign/change roles for any admin user
- Suspend/activate admin accounts
- Configure invitation token expiry time (default 72 hours, range 24-168 hours)
- Create permission matrix for custom roles
- Re-send invitation emails for pending accounts

**Fixed in Codebase (Not Editable)**:

- Super Admin role permissions (always full access)
- Core permission categories (cannot rename or remove: Patient Management, Provider Management, Billing, etc.)
- Audit trail retention period (10 years, per Constitution)
- Password hashing algorithm (bcrypt, cost factor 12)
- Password requirements (12 chars minimum, 1 upper, 1 lower, 1 digit, 1 special char)

**Configurable with Restrictions**:

- Invitation token expiry (configurable within 24-168 hour range)
- Maximum failed login attempts before lockout (configurable in A-09: Authentication Settings)
- Session timeout duration (configurable in A-09: Authentication Settings)
- Number of concurrent sessions per admin user (default: 3, range: 1-5)

---

## Success Criteria

### Admin Management Efficiency Metrics

- **SC-001**: Super Admins can invite and activate new admin team members in under 2 minutes (from invitation to account activation)
- **SC-002**: Role assignment changes take effect immediately (enforced on next user action/API call within 1 second)
- **SC-003**: 90% of admin team member invitations are activated within 24 hours of sending
- **SC-004**: Super Admins can create custom roles with granular permissions in under 5 minutes

### Security & Compliance Metrics

- **SC-005**: 100% of administrative actions (role changes, permission grants, suspensions) are logged in audit trail
- **SC-006**: Zero unauthorized access to restricted admin features (all access attempts properly validated)
- **SC-007**: Audit trail entries are immutable and retained for 10 years per compliance requirements
- **SC-008**: All admin users have MFA enabled (enforced for admin platform per Constitution Principle II)
- **SC-009**: Password reset requests are processed and logged within 2 minutes

### User Experience Metrics

- **SC-010**: Admin users can identify their role and permissions within 3 clicks from dashboard
- **SC-011**: Permission matrix clearly displays all granted and denied permissions for any role
- **SC-012**: New admin team members receive clear invitation emails with activation instructions
- **SC-013**: 95% of admin users successfully activate accounts on first attempt without support

### System Performance Metrics

- **SC-014**: Permission checks execute in under 50ms for API endpoint authorization
- **SC-015**: Audit trail queries return results within 1 second for last 100 entries
- **SC-016**: Role permission updates propagate to all user sessions within 5 seconds
- **SC-017**: System supports 100+ concurrent admin users with different roles without performance degradation

### Operational Impact Metrics

- **SC-018**: Reduction in unauthorized access attempts by 80% through clear permission enforcement
- **SC-019**: Support tickets related to admin access issues reduced by 60% through self-service permission visibility
- **SC-020**: Time to onboard new admin team members reduced by 70% through streamlined invitation workflow

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **FR-009 / Module PR-01**: Provider Team & Role Management
  - **Why needed**: Provider-facing team management relies on the global RBAC schema, roles, and permission definitions governed by this module
  - **Integration point**: Admin-defined roles/permissions are surfaced to provider tenant management flows; changes to role definitions cascade to provider team capabilities

- **FR-020 / Module S-03**: Notifications & Alerts
  - **Why needed**: Delivers transactional email/in-app alerts for admin invitations, role changes, suspensions, and audit events
  - **Integration point**: Admin platform emits notification events that FR-020 templates render; ensures consistent messaging across tenants

- **FR-026 / Module A-09**: App Settings & Security Policies
  - **Why needed**: Provides authentication throttling, OTP configuration, password policy enforcement
  - **Integration point**: Admin user login and password reset flows use authentication settings from FR-026

- **FR-001 / Module P-01**: Patient Auth & Profile Management
  - **Why needed**: Shares authentication infrastructure and security patterns
  - **Integration point**: Similar session management, password hashing, MFA enforcement patterns

- **Module S-03**: Notification Service
  - **Why needed**: Sends invitation emails, role change notifications, password reset emails
  - **Integration point**: Triggers email notifications for admin user lifecycle events

- **Module A-01 through A-10**: All Admin Platform Modules
  - **Why needed**: Permission checks enforced across all admin features
  - **Integration point**: Every admin API endpoint checks user permissions before granting access

### External Dependencies (APIs, Services)

- **External Service: Email Delivery Service** (Twilio SendGrid / AWS SES)
  - **Purpose**: Delivers invitation emails, role change notifications, password reset emails
  - **Integration**: RESTful API calls for email sending
  - **Failure handling**: Queue emails for retry if delivery fails; log failures in audit trail; admin notification if emails fail for 24+ hours

- **External Service: System Clock / Time Service**
  - **Purpose**: Accurate timestamps for audit trail entries and token expiration
  - **Integration**: System time (NTP synchronized)
  - **Failure handling**: Use server time as fallback; alert if time drift detected

### Data Dependencies

- **Entity: Admin User Accounts**
  - **Why needed**: Cannot assign roles or permissions without existing admin accounts
  - **Source**: Initial super admin created during platform deployment; subsequent accounts created via invitation flow

- **Entity: Role Definitions**
  - **Why needed**: Cannot assign roles to users without predefined or custom roles
  - **Source**: System ships with default roles (Super Admin, Aftercare Specialist, Billing Staff, Support Staff); custom roles created via this module

- **State: Active Roles**
  - **Why needed**: Only active (non-archived) roles can be assigned to new or existing users
  - **Source**: Role management within this module (FR-031)

---

## Assumptions

### User Behavior Assumptions

- **Assumption 1**: Super Admins will create roles before inviting team members (logical workflow)
- **Assumption 2**: New admin team members will activate accounts within 72 hours of invitation
- **Assumption 3**: Admin users will primarily access platform from trusted devices/networks (office, VPN)
- **Assumption 4**: Super Admins will review and update team member roles periodically (quarterly or when responsibilities change)

### Technology Assumptions

- **Assumption 1**: Admin platform accessed via modern web browsers (Chrome, Firefox, Safari, Edge - latest 2 versions)
- **Assumption 2**: Admin users have stable internet connectivity (office network or reliable home internet)
- **Assumption 3**: Email delivery service (SendGrid/SES) has 99%+ uptime for invitation emails
- **Assumption 4**: System clock synchronized via NTP for accurate audit trail timestamps

### Business Process Assumptions

- **Assumption 1**: Super Admin role assigned to senior operations staff (CEO, CTO, Operations Manager)
- **Assumption 2**: Aftercare specialists check aftercare cases at least twice daily during business hours
- **Assumption 3**: Billing staff process payouts on scheduled basis (weekly, bi-weekly, or monthly)
- **Assumption 4**: Support staff respond to patient and provider inquiries within 24 hours
- **Assumption 5**: Admin team members notified of role changes via email and acknowledge changes within 24 hours

---

## Implementation Notes

### Technical Considerations

- **Architecture**: Role-based access control (RBAC) implemented via middleware on all admin API endpoints
- **Technology**: Permission checks execute before business logic (fail-fast approach)
- **Performance**: Permission matrix cached in memory for fast lookups (invalidate cache on role/permission changes)
- **Storage**: Audit trail stored in separate database table with indexes on user_id, timestamp, action_type for fast queries
- **Security**: JWT tokens include role and permission claims for stateless authorization (token signed with RS256)

### Integration Points

- **Integration 1**: Admin API endpoints check permissions via middleware
  - **Data format**: JWT token with role and permissions claims
  - **Authentication**: Bearer token authentication
  - **Error handling**: Return 403 Forbidden with clear error message if permission denied

- **Integration 2**: Notification Service for invitation and role change emails
  - **Data format**: JSON payload with email template ID, recipient email, template variables
  - **Authentication**: Internal service-to-service authentication (API key)
  - **Error handling**: Queue failed emails for retry; log failures in audit trail

- **Integration 3**: Audit trail writes for all admin actions
  - **Data format**: Structured log entries (timestamp, user_id, action_type, details, IP address, outcome)
  - **Authentication**: Internal service (no external auth)
  - **Error handling**: Buffer audit entries and batch-write to database; alert if audit writes fail (critical security issue)

### Scalability Considerations

- **Current scale**: Expected 10-20 admin users at launch
- **Growth projection**: Plan for 50-100 admin users within 12 months (as platform scales to multiple countries)
- **Peak load**: Permission checks on every admin API call (100-500 requests/minute estimated)
- **Data volume**: Audit trail grows by ~1,000 entries per day (admin actions logged)
- **Scaling strategy**: Cache permission matrix in Redis for fast lookups; partition audit trail by date for query performance; horizontal scaling of admin API servers

### Security Considerations

- **Authentication**: MFA required for all admin platform users (per Constitution Principle II)
- **Authorization**: Role-based access control with granular permissions per feature/module
- **Encryption**: JWT tokens signed with RS256 (asymmetric encryption) to prevent token tampering
- **Audit trail**: All permission changes, role assignments, and admin actions logged with timestamp, user, IP address
- **Threat mitigation**: Rate limiting on admin login endpoint to prevent brute-force attacks (max 5 attempts per 15 minutes)
- **Compliance**: GDPR-compliant audit logging; PII anonymization on account deletion request; audit trail immutable and retained 10 years

---

## User Scenarios & Testing

### User Story 1 - Invite Aftercare Specialist (Priority: P1)

As a Super Admin, I need to invite a new aftercare nurse to the admin platform so they can start managing aftercare cases without accessing sensitive billing or provider data.

**Why this priority**: Core onboarding workflow required for day-one operations; enables team growth and role separation

**Independent Test**: Can be fully tested by creating new admin account, assigning "Aftercare Specialist" role, and verifying access to aftercare features only

**Acceptance Scenarios**:

1. **Given** Super Admin is logged into admin platform, **When** Super Admin invites new user with email "<nurse@hairline.com>" and role "Aftercare Specialist", **Then** invitation email sent within 1 minute and new account created with status "Pending Activation"

2. **Given** new aftercare nurse receives invitation email, **When** nurse clicks activation link and sets password, **Then** account activated and nurse can log in with aftercare dashboard access

3. **Given** aftercare nurse is logged in, **When** nurse attempts to access Billing section, **Then** access denied with message "You do not have permission to access this feature" and attempt logged in audit trail

---

### User Story 2 - Create Custom Role for Analytics Staff (Priority: P2)

As a Super Admin, I need to create a custom "Analytics Viewer" role with read-only access to reports and dashboards, so analytics staff can view data without modifying it.

**Why this priority**: Enables specialized roles for growing team; supports principle of least privilege

**Independent Test**: Can be tested by creating custom role with read-only permissions, assigning to test user, and verifying read access without write capabilities

**Acceptance Scenarios**:

1. **Given** Super Admin navigates to Roles & Permissions, **When** Super Admin creates new role "Analytics Viewer" with permissions: View Financial Reports (read), View Patient Data (read), View Provider Data (read), **Then** role saved and available in role dropdown for user assignment

2. **Given** custom role "Analytics Viewer" exists, **When** Super Admin assigns role to user "<analyst@hairline.com>", **Then** user can view reports but cannot edit data, process payouts, or modify settings

3. **Given** analytics viewer is logged in, **When** user attempts to edit patient information, **Then** edit button hidden or disabled and action denied if attempted via API

---

### User Story 3 - Audit Trail Review for Compliance (Priority: P1)

As a Super Admin, I need to review audit trail of all administrative actions to ensure compliance with data protection regulations and identify unauthorized access attempts.

**Why this priority**: Critical for compliance with healthcare data regulations (HIPAA, GDPR); required for security audits

**Independent Test**: Can be tested by performing various admin actions (role changes, suspensions, access attempts) and verifying all actions logged with correct details

**Acceptance Scenarios**:

1. **Given** Super Admin navigates to User Audit Trail, **When** Super Admin selects user "<support@hairline.com>", **Then** audit trail displays all actions by that user with timestamps, action types, and outcomes

2. **Given** admin user with "Support Staff" role attempts to access Provider Billing section, **When** access denied due to insufficient permissions, **Then** access denial logged in audit trail with: timestamp, user ID, requested feature, IP address, outcome "Denied"

3. **Given** Super Admin reviews audit trail for last 30 days, **When** Super Admin exports audit log to CSV, **Then** CSV file contains all audit entries with columns: timestamp, user, action, details, IP address, outcome

---

### User Story 4 - Role Change Notification (Priority: P2)

As an admin user, I need to be notified immediately when my role or permissions change, so I understand what features I can now access or no longer access.

**Why this priority**: Transparency and user awareness; reduces support tickets from confused users

**Independent Test**: Can be tested by changing user's role and verifying email notification sent with permission comparison

**Acceptance Scenarios**:

1. **Given** admin user "<support@hairline.com>" has role "Support Staff", **When** Super Admin changes role to "Aftercare Specialist", **Then** user receives email notification within 5 minutes with: old role, new role, permission changes summary

2. **Given** role change notification received, **When** user logs in after role change, **Then** dashboard reflects new role permissions (aftercare features visible, support features hidden)

3. **Given** user's role changed from "Billing Staff" to "Support Staff", **When** user attempts to access previously permitted billing feature, **Then** access denied and user informed: "Your permissions have changed. You no longer have access to this feature."

---

### User Story 5 - Prevent System Lockout (Priority: P1)

As a platform administrator, I need the system to prevent the last Super Admin account from being suspended or deleted, so the platform always has at least one admin with full access.

**Why this priority**: Critical system protection; prevents complete lockout requiring database intervention

**Independent Test**: Can be tested by attempting to suspend or delete the only Super Admin account and verifying action blocked

**Acceptance Scenarios**:

1. **Given** only one Super Admin account exists ("<admin@hairline.com>"), **When** another admin attempts to suspend this account, **Then** action blocked with error message: "Cannot suspend the last Super Admin account. Add another Super Admin first."

2. **Given** two Super Admin accounts exist, **When** Super Admin suspends one of the two Super Admin accounts, **Then** suspension succeeds and remaining Super Admin can continue managing platform

3. **Given** only one Super Admin exists, **When** Super Admin attempts to change own role to non-Super Admin role, **Then** action blocked with warning: "You are the last Super Admin. Assign Super Admin role to another user before changing your role."

---

### Edge Cases

- **Edge Case 1**: What happens when admin user's session is active and their role is changed by another Super Admin?
  - **Handling**: Current session remains valid until next API call; next API call checks updated permissions and enforces new role; user may see "Permission denied" on action if new role lacks permission; session not forcibly terminated (graceful permission enforcement)

- **Edge Case 2**: How does system handle simultaneous role changes by two Super Admins on the same user?
  - **Handling**: Database-level locking prevents concurrent updates; second Super Admin receives error: "Role change failed - this user's role was just updated by another admin. Refresh and try again." Audit trail logs both attempts with outcomes (success, conflict)

- **Edge Case 3**: What occurs if invitation email delivery fails (email service down)?
  - **Handling**: System queues invitation email for retry (3 attempts with exponential backoff); if all retries fail, invitation marked "Delivery Failed" and Super Admin notified; Super Admin can manually re-send invitation once email service restored

- **Edge Case 4**: How to manage admin user who forgets password before activating account?
  - **Handling**: Pending activation accounts do not support password reset (no password set yet); user must request new invitation from Super Admin; original invitation token invalidated to prevent duplicate accounts

- **Edge Case 5**: What happens if audit trail write fails (database connection lost)?
  - **Handling**: Critical actions (role changes, suspensions) buffered in memory and retried on database reconnection; if buffer full or database unavailable for extended period, admin actions temporarily blocked with message: "System maintenance in progress. Please try again shortly." Alert sent to infrastructure team immediately (audit trail failure is critical security issue)

---

## Functional Requirements Summary

### Core Requirements

- **FR-001**: System MUST allow Super Admins to invite new admin team members via email with role assignment
- **FR-002**: System MUST support creation of custom roles with granular permission assignment per admin module (A-01 through A-10)
- **FR-003**: System MUST enforce role-based access control on all admin API endpoints and UI components
- **FR-004**: System MUST provide predefined roles: Super Admin, Aftercare Specialist, Billing Staff, Support Staff
- **FR-005**: System MUST log all administrative actions (role changes, permission grants, user suspensions, access denials) in immutable audit trail
- **FR-006**: System MUST prevent suspension or deletion of the last Super Admin account (system protection)
- **FR-007**: System MUST send email notifications for: new invitations, role changes, password resets, repeated access denials

### Data Requirements

- **FR-008**: System MUST maintain admin user accounts with: email, name, password hash, assigned role(s), status (active/pending/suspended), creation date, last login timestamp
- **FR-009**: System MUST maintain role definitions with: role name, description, assigned permissions (as permission matrix)
- **FR-010**: System MUST maintain audit trail entries with: timestamp, user ID, action type, action details, IP address, outcome (success/failed/denied)
- **FR-011**: System MUST retain audit trail for minimum 10 years per compliance requirements (Constitution Principle VI)

### Security & Privacy Requirements

- **FR-012**: System MUST enforce Multi-Factor Authentication (MFA) for all admin platform users (per Constitution Principle II)
- **FR-013**: System MUST use bcrypt (cost factor 12+) for password hashing
- **FR-014**: System MUST enforce password requirements: minimum 12 characters, 1 uppercase, 1 lowercase, 1 digit, 1 special character
- **FR-015**: System MUST sign JWT tokens with RS256 (asymmetric encryption) to prevent tampering
- **FR-016**: System MUST include role and permission claims in JWT tokens for stateless authorization
- **FR-017**: System MUST invalidate user sessions immediately upon account suspension
- **FR-018**: System MUST anonymize admin user PII (email, name) on account deletion request, while preserving audit trail with anonymized identifier

### Integration Requirements

- **FR-019**: System MUST integrate with Notification Service (S-03) for email delivery (invitations, role changes, password resets)
- **FR-020**: System MUST provide permission check API for all admin modules to enforce access control
- **FR-021**: System MUST cache permission matrix in memory for fast authorization checks (< 50ms per check)
- **FR-022**: System MUST invalidate permission cache within 5 seconds of role or permission changes

---

## Key Entities

- **Entity 1 - Admin User Account**
  - **Key attributes**: user_id (UUID), email (unique), name, password_hash, assigned_role_id (foreign key), status (active/pending/suspended), created_at (timestamp), last_login_at (timestamp), MFA_enabled (boolean), invitation_token (nullable, expires after 72 hours)
  - **Relationships**: One admin user has one assigned role; one role can be assigned to many admin users; one admin user has many audit trail entries

- **Entity 2 - Role Definition**
  - **Key attributes**: role_id (UUID), role_name (unique), description, is_system_role (boolean - true for Super Admin/predefined roles), permissions (JSON object - permission matrix), created_at (timestamp), updated_at (timestamp), created_by (admin user ID)
  - **Relationships**: One role has many admin users assigned; one role has many permission grants (stored as JSON)

- **Entity 3 - Audit Trail Entry**
  - **Key attributes**: audit_id (UUID), timestamp (indexed), user_id (foreign key), action_type (enum: login, role_change, permission_grant, access_denied, user_suspended, password_reset), action_details (JSON object with context), ip_address, outcome (enum: success, failed, denied), session_id (for tracking related actions)
  - **Relationships**: One admin user has many audit trail entries; audit entries are immutable (no updates or deletes)

- **Entity 4 - Permission**
  - **Key attributes**: permission_id (UUID), permission_name (unique), module_code (e.g., A-01, A-02), permission_category (read/write/delete), description, is_super_admin_only (boolean)
  - **Relationships**: Permissions are assigned to roles via permission matrix (many-to-many through role permissions JSON)

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-14 | 1.0 | Initial PRD creation for FR-031: Admin Access Control & Permissions | Claude AI / Speckit |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | TBD | TBD | Pending |
| Technical Lead | TBD | TBD | Pending |
| Security Lead | TBD | TBD | Pending |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-011 Aftercare & Recovery Management PRD
**Last Updated**: 2025-11-14
