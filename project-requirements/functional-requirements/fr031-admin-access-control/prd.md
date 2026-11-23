# FR-031 - Admin Access Control & Permissions

**Module**: A-09: System Settings & Configuration
**Feature Branch**: `fr031-admin-access-control`
**Created**: 2025-11-14
**Status**: Revision v1.2 (requirements graph programme baseline); v1.0.2 baseline verified and approved
**Source**: FR-031 from system-prd.md

---

## Executive Summary

The Admin Access Control & Permissions module is a **Super Admin-only configuration tool** that serves as the **single source of truth** for all role definitions and permission matrices across the entire Hairline platform. This module enables Super Admins to: (REQ-031-028)

1. **Define Admin Platform Role Permissions**: Configure what permissions each admin role has (Super Admin, Aftercare Coordinator, Billing Admin, Support Staff) (REQ-031-004)
2. **Define Provider Platform Roles and Permissions**: Configure the permissions of the four provider roles (Owner, Manager, Clinical Staff, Billing Staff) (REQ-031-005)
3. **Manage Admin Team Members**: Invite admin users and assign them roles (team member invitation/management for providers is handled separately in FR-009)

**Key Distinction**: This module is exclusively for **Super Admins to configure RBAC rules**. Regular admin users and providers do not have access to this module. Provider owners can assign roles to their team members (FR-009), but only Super Admins can define what permissions those roles have.

This centralized approach ensures consistent security policies across all platforms, enables Super Admins to configure and update role permissions from a single interface, and maintains full auditability and compliance with healthcare data security requirements.

This module directly supports Principle II (Medical Data Privacy & Security) and Principle VI (Data Integrity & Audit Trail) from the Hairline Platform Constitution by enforcing the principle of least privilege and maintaining comprehensive audit trails of all permission changes and administrative actions.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-01)**: Not applicable - this module operates exclusively within Admin Platform
- **Provider Platform (PR-01)**: Consumes and enforces RBAC rules configured in Admin Platform (no configuration UI in provider platform)
- **Admin Platform (A-09)**: All RBAC configuration happens here - Super Admins configure role permissions for both admin and provider roles
- **Shared Services (S-03)**: Sends invitation and role/permission change notifications; permission sync handled via API

### Multi-Tenant Breakdown

**Patient Platform (P-01)**:

- No patient-facing functionality

**Provider Platform (PR-01)**:

- **Permission enforcement only**: Provider Platform consumes and enforces RBAC rules defined in Admin Platform (FR-031) (REQ-031-029)
- **No configuration UI**: Provider users do not see or access role permission configuration; they only experience the enforced permissions
- **Read-only consumption**: Provider Platform reads permission matrices from FR-031 and applies them when provider team members access features
- **Note**: Provider team member invitation and role assignment is handled in PR-01/FR-009, but the permission definitions for those roles come from FR-031

**Admin Platform (A-09)** (Super Admin Only):

- **Admin role permission configuration**: Super Admins define what permissions each admin role has (Super Admin, Aftercare Coordinator, Billing Admin, Support Staff)
- **Provider role configuration**: Super Admins define permissions for the four provider roles (Owner, Manager, Clinical Staff, Billing Staff)
- **Admin team member management**: Super Admins invite admin users and assign them predefined roles
- **Finance admin (actor)**: the admin team member who works the financial screens of the Admin Platform (payouts, billing, provider financial reports). The predefined admin role for this work is Billing Admin; Super Admin also has full access. Which financial screens an admin can reach follows the Billing & Financial permissions in Screen 4
- Permission matrix definition and editing for both admin and provider roles
- Centralized RBAC configuration interface accessible only to Super Admins
- Audit trail of all permission changes and role assignments
- Access control: Only Super Admins can access this module; regular admin users and providers cannot view or modify role permissions (REQ-031-028)

**Shared Services (S-03)**:

- Invitation and role/permission change notifications delivered via S-03 (REQ-020-152)
- Permission checks executed within admin platform backend

### Communication Structure

**In Scope**:

- Email notifications for admin team member invitations (REQ-031-010)
- Email notifications for role assignment changes (REQ-031-010)
- Email notifications for permission changes (to affected admin users) (REQ-031-032)
- System notifications for access denial attempts

**Out of Scope**:

- SMS notifications (handled by S-03: Notification Service if needed; **no SMS admin notifications are available in MVP and SMS will only be enabled if/when S-03 adds SMS delivery in a later phase**) (REQ-031-031)
- Real-time permission updates via WebSocket (V2 enhancement) (REQ-031-031)
- External identity provider integration (OAuth, SAML - V2 enhancement) (REQ-031-031)

### Entry Points

- **Super Admin Access Only**: Super Admins access this module via "Settings > User Roles & Permissions" in the Admin Platform (REQ-031-027)
- **Access Restriction**: This module is hidden from non-Super Admin users; only Super Admins can view and access it (REQ-031-027)
- **Initial Setup**: First Super Admin account created during platform deployment/installation (REQ-031-027)
- **Configuration Workflow**:
  - Super Admins configure role permissions for admin and provider roles
  - Super Admins invite admin team members and assign them roles
  - Provider owners invite their team members (FR-009) but cannot configure role permissions (REQ-031-027)
- **Permission Enforcement**: Configured permissions enforced across all platforms on every API request (REQ-031-020)
- **Audit Trail Access**: All Super Admin actions logged automatically and viewable in audit trail interface (REQ-031-008)

---

## Business Workflows

### Main Flow: Admin Team Member Invitation

**Actors**: Super Admin, New Admin User, System
**Trigger**: Super Admin clicks "Invite Team Member" button in Settings > User Roles & Permissions screen
**Outcome**: New admin user receives invitation email, creates account, gains access to admin platform with assigned role

**Steps**:

1. Super Admin navigates to Settings > User Roles & Permissions
2. System displays 3-tab interface (Admin Roles, Admin Users, Provider Roles)
3. Super Admin selects "Admin Users" tab
4. System displays current admin team members with their roles and status
5. Super Admin clicks "Invite Team Member" button
6. System presents invitation form with fields: email address, first name, last name, role selection
7. Super Admin enters admin user details and selects role (Super Admin, Aftercare Coordinator, Billing Admin, Support Staff)
8. System validates email format and checks for duplicate email within admin team
9. Super Admin reviews invitation details and clicks "Send Invitation"
10. System generates secure invitation token (expires in 7 days)
11. System sends email to invitee with invitation link, Hairline Admin Platform branding, and role being offered (sent within 1 minute of the Super Admin clicking Send Invitation)
12. System records the invitation on the new admin user's account with status "Invited"
13. System displays confirmation message to Super Admin
14. New Admin User receives email and clicks invitation link
15. System validates invitation token (not expired, not already used)
16. System displays Admin Account Setup screen (Screen 3) pre-filled with email, first name, last name
17. New Admin User reviews pre-filled information, enters phone number (optional), sets password, and accepts terms of service
18. New Admin User clicks "Create Account"
19. System validates all inputs (password strength, terms acceptance)
20. System creates admin account with assigned role
21. System marks invitation as "Accepted"
22. System sends confirmation email to both Super Admin and new admin user
23. System logs account creation in audit trail
24. System displays success message and redirects to login page
25. New Admin User can immediately log in with new credentials

### Alternative Flows

**A1: Re-send Invitation (Token Expired)**:

- **Trigger**: Invitation token expired (7 days passed) and admin user hasn't signed up
- **Steps**:
  1. Super Admin views pending invitations list
  2. System shows invitation status as "Expired"
  3. Super Admin clicks "Resend Invitation" button
  4. System generates new invitation token and sends new email
  5. Old invitation token invalidated
- **Outcome**: Admin user receives fresh invitation with new 7-day expiry

**A2: Role Change for Existing Admin User**:

- **Trigger**: Admin user's responsibilities change, requiring different role
- **Steps**:
  1. Super Admin navigates to Settings > User Roles & Permissions > Admin Users tab
  2. Super Admin selects target admin user from the list
  3. Super Admin clicks "Change Role" action
  4. System displays role change dialog with current role highlighted
  5. Super Admin selects new role from dropdown
  6. Super Admin sets **Effective From** date/time (default: now)
  7. System displays permission comparison (current vs new role permissions) and effective date/time (REQ-031-075)
  8. Super Admin confirms role change
  9. System validates Effective From is not in the past
  10. System updates user's role assignment with Effective From timestamp
  11. System logs role change in audit trail (who changed, old role, new role, effective_from, timestamp)
  12. System sends email notification to affected user about role change (includes effective date/time)
  13. System shows the affected user an "Acknowledge role change" action (banner after sign-in and a link in the email); the acknowledgement time is stored on the account (Rule 10)
  14. System enforces new role permissions on the first API call at or after Effective From
- **Outcome**: Admin user's permissions updated to match new role

**A3: Create Custom Admin Role**:

- **Trigger**: Super Admin needs admin role not covered by standard roles (e.g., specialized analytics-only role)
- **Steps**:
  1. Super Admin navigates to Settings > User Roles & Permissions > Admin Roles tab
  2. Super Admin clicks "Create New Role" button
  3. System displays role creation form
  4. Super Admin enters: role name, role description
  5. System opens Permission Matrix Modal (Screen 4) for admin permissions
  6. Super Admin selects permissions from permission matrix (checkboxes for each feature)
  7. System displays permission summary and potential conflicts/warnings
  8. Super Admin clicks "Save Changes"
  9. System validates: unique role name, at least one permission selected
  10. System saves new role definition
  11. System logs role creation in audit trail
  12. New role appears in Admin Roles tab and in role dropdown for team member assignment
- **Outcome**: New custom admin role available for assignment to admin team members

**A4: Configure Provider Role Permissions**:

- **Trigger**: Super Admin needs to modify permissions for a provider role
- **Steps**:
  1. Super Admin navigates to Settings > User Roles & Permissions > Provider Roles tab
  2. System displays the four provider roles with user counts
  3. Super Admin clicks "Edit Permissions" on target provider role (e.g., "Clinical Staff")
  4. System opens Permission Matrix Modal (Screen 4) with provider permissions
  5. System displays current permissions checked and shows user count: "Currently assigned to [X] users across [Y] providers"
  6. Super Admin modifies permissions (e.g., grants "View Financial Reports" to Clinical Staff)
  7. System displays permission comparison showing additions/removals (REQ-031-075)
  8. System shows warning if removing critical permissions (e.g., "This will remove access to [feature] for all Clinical Staff members")
  9. System displays count of affected provider team members across all providers
  10. Super Admin reviews changes and clicks "Save Changes"
  11. System validates permission changes (e.g., Owner role must retain full access)
  12. System saves updated permission matrix
  13. System logs permission change in audit trail with before/after comparison
  14. System syncs permission changes to Provider Platform (FR-009) within 5 seconds
  15. System displays confirmation: "Provider role permissions updated. Changes reach all [Role] members within 5 seconds and apply on their next request." (REQ-031-075)
  16. All provider team members with this role receive updated permissions on their next API call
- **Outcome**: Provider role permissions updated and automatically propagated to all provider organizations; changes enforced immediately

**B1: Invalid Email Address**:

- **Trigger**: Super Admin enters malformed email address
- **Steps**:
  1. System validates email format on blur or submit
  2. System displays inline error message: "Please enter a valid email address"
  3. Super Admin corrects email
  4. System re-validates and allows submission
- **Outcome**: Only valid email addresses accepted

**B2: Duplicate Email Within Admin Team**:

- **Trigger**: Super Admin invites email that already exists as admin user or pending invitation
- **Steps**:
  1. System checks email against existing admin team members and pending invitations
  2. System displays error: "This email is already associated with an admin account. Please use a different email or check existing team members."
  3. System suggests: "View team member" or "Resend invitation" if pending
  4. Super Admin either cancels or takes suggested action
- **Outcome**: Duplicate prevented, existing record maintained

**B3: Invitation Link Already Used**:

- **Trigger**: Admin user clicks invitation link that was already accepted
- **Steps**:
  1. System detects invitation status is "Accepted"
  2. System displays message: "This invitation has already been used. Please log in with your existing credentials." (REQ-031-041)
  3. System provides login link
- **Outcome**: Prevents duplicate account creation

**B4: Network Error During Invitation Send**:

- **Trigger**: Email service fails to send invitation
- **Steps**:
  1. System attempts to send invitation email
  2. Email service returns error
  3. System logs each failed delivery in the audit trail and retries according to the notification retry rule owned by FR-030 (this flow sets no retry count or interval of its own)
  4. If all retries under that rule fail, system marks invitation as "Pending Send"
  5. System displays warning to Super Admin: "Invitation created but email failed. We'll retry automatically."
  6. If the invitation still cannot be sent 24 hours after it was created, the invitation becomes "Expired"
  7. System alerts the admin team; Super Admin can resend the invitation (A1)
- **Outcome**: Invitation record created; email delivered through the retry rule, or the invitation expires and the Super Admin resends it

**B5: Unauthorized Access Attempt**:

- **Trigger**: Admin user attempts to access feature not permitted by their role
- **Steps**:
  1. **On page load**: System checks user's permissions and hides all UI elements (menu items, buttons, tabs) for features user cannot access
  2. **If feature cannot be hidden** (e.g., shared page with mixed permissions or direct URL access): Admin user navigates to restricted feature
  3. System checks user's permissions against required permission
  4. System denies access and displays message: "Access Denied: You do not have permission to access this feature. Contact your administrator if you need access."
  5. System logs access denial attempt in audit trail (user, feature, timestamp, IP address)
  6. System sends alert to Super Admin when one admin is refused 5 times within 10 minutes (launch default; the count and the time window are admin settings in A-09; potential security issue)
- **Outcome**: Unauthorized features hidden from UI; access blocked if directly accessed; security event logged

**Note**: The system follows "hide first, deny second" approach:

- **Preferred**: Hide unauthorized menu items, buttons, and navigation elements so users never see features they can't access
- **Fallback**: Display access denied message only when hiding is not feasible (direct URL access, shared pages with partial access)

**B6: Sensitive Permission Warning**:

- **Trigger**: Super Admin assigns role with sensitive permissions (billing, user management, provider suspension, financial data)
- **Steps**:
  1. System detects role contains sensitive permissions (flagged as "sensitive" in permission definition)
  2. System displays warning modal: "This role grants access to sensitive features: [Billing & Financial Data, Process Payouts, View Transactions]. Confirm assignment?"
  3. System displays full permission summary for the role being assigned
  4. Super Admin reviews permissions and either: (a) confirms assignment, or (b) cancels to select different role
- **Outcome**: Super Admin makes informed decision about sensitive permission assignment; prevents accidental over-privileging

---

## Screen Specifications

### Screen 1: User Roles & Permissions (Tabbed Interface)

**Purpose**: Centralized interface for Super Admins to configure RBAC for the entire platform and manage admin team members. Accessed via Settings > User Roles & Permissions.

**Layout**: Three-tab interface with consistent navigation

**Tabs**:

1. **Admin Roles** - Configure admin role permissions
2. **Admin Users** - Manage admin team members
3. **Provider Roles** - Configure provider role permissions

**Note on Provider User Oversight**: Viewing and managing provider team members is handled in FR-015 (Provider Management). Super Admins can view provider organizations and drill down to see their team members there. This module (FR-031) focuses solely on RBAC configuration - defining what each role can do, not managing who has those roles in provider organizations.

---

#### Tab 1: Admin Roles

**Purpose**: Define and configure permission matrices for admin platform roles (Super Admin, Aftercare Coordinator, Billing Admin, Support Staff)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---------------|
| Role List | table | N/A | List of all admin roles | Display: Role Name, Description, # Users, Actions | ENT-role-permission-definition.role_name, ENT-role-permission-definition.description, ENT-role-permission-definition.user_count |
| Role Name | text | N/A | Name of role | Read-only for system roles | ENT-role-permission-definition.role_name |
| Users Count | number | N/A | Number of admin users with this role | Display only, clickable to filter Tab 2 | ENT-role-permission-definition.user_count |
| Actions | button group | N/A | Edit Permissions, View Users, Clone Role | Edit Permissions and Clone Role are disabled for the Super Admin role; View Users stays available (REQ-031-052) | no graph field (control) |

**Actions**:

- **Edit Permissions**: Opens permission matrix modal/panel for selected role
- **View Users**: Switches to Tab 2 filtered by this role (REQ-031-080)
- **Clone Role**: Creates new custom role based on existing role (REQ-031-057)
- **Create New Role**: Creates custom admin role with specific permissions (REQ-031-058)

**Business Rules**:

- Super Admin role permissions cannot be edited (locked, full access) (REQ-031-051)
- System roles (Super Admin, Aftercare Coordinator, Billing Admin, Support Staff) cannot be deleted; all of them except Super Admin can be edited (REQ-031-056)
- Custom roles can be created, edited, and deleted (if no users assigned) (REQ-031-057)
- Permission changes take effect on the next API call after propagation (≤ 5 seconds) for all users with that role

---

#### Tab 2: Admin Users

**Purpose**: Manage admin team members - invite, assign roles, suspend, view activity

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---------------|
| Search Bar | text input | No | Search users by name or email | Real-time filtering | no graph field (control) |
| Filter: Role | dropdown | No | Filter users by assigned role | All Roles, then every active admin role including custom roles (predefined: Super Admin, Aftercare Coordinator, Billing Admin, Support Staff) | ENT-admin-user-account.assigned_role_id |
| Filter: Status | dropdown | No | Filter by user status | All, Active, Suspended, Pending Invitation | ENT-admin-user-account.status, ENT-admin-user-account.invitation_status |
| User Name | Display (text) | N/A | Full name of admin user | Display only | ENT-admin-user-account.name |
| Email | Display (email) | N/A | Admin user's email address | Display only | ENT-admin-user-account.email |
| Role | Display (badge) | N/A | Assigned role | Color-coded by role | ENT-admin-user-account.assigned_role_id |
| Role Effective From | Display (datetime) | N/A | When the assigned role becomes active | Display only | ENT-admin-user-account.role_effective_from |
| Last Login | datetime | N/A | Timestamp of most recent login | Relative format (e.g., "2 hours ago") | ENT-admin-user-account.last_login_at |
| Status | badge | N/A | Active/Suspended/Pending | Color-coded | ENT-admin-user-account.status |
| Actions | button group | N/A | Change Role, Suspend, View Audit | Dropdown menu | no graph field (control) |

**Actions**:

- **Invite Team Member**: Opens invitation form (Screen 2)
- **Change Role**: Opens role assignment modal (REQ-031-082)
- **Suspend/Activate**: Suspend or reactivate admin user (not available for Super Admin accounts) (REQ-031-053)
- **View Audit**: Opens user detail page with audit trail (Screen 5)

**Business Rules**:

- A Super Admin account cannot be suspended by any other user, and cannot be removed, demoted or deactivated by anyone inside the product, including its holder; if ever needed, this is done outside the product (system protection)
- At least one active Super Admin must exist at all times (prevent lockout) (REQ-031-085)
- Suspended users cannot log in but accounts remain in system (soft suspension) (REQ-031-053)
- Search filters users in real-time without page reload (REQ-022-115)
- Pagination: Display 25 users per page with "Load More" option (REQ-031-098)
- Sort columns: Name (A-Z), Last Login (most recent first), Role (alphabetical) (REQ-031-098)

**Notes**:

- Display warning banner if only one Super Admin exists: "Warning: Only one Super Admin account. Consider adding backup admin." (REQ-031-085)
- Show notification dot on Pending Invitations sub-tab if invitations are about to expire (< 24 hours) (REQ-031-042)
- Export user list to CSV with all columns and applied filters (REQ-031-098)
- Each user row shows whether the user has acknowledged the latest role change (Acknowledged or Awaiting acknowledgement) (REQ-031-124; ENT-admin-user-account.role_change_acknowledged_at)

---

#### Tab 3: Provider Roles

**Purpose**: Define and configure permission matrices for the four provider roles (Owner, Manager, Clinical Staff, Billing Staff).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---------------|
| Role List | table | N/A | List of provider roles | Display: Role Name, Description, Total Users Across All Providers, Actions | ENT-role-permission-definition.role_name, ENT-role-permission-definition.description, ENT-role-permission-definition.user_count |
| Role Name | text | N/A | Name of provider role | Read-only; the four provider role names are fixed | ENT-role-permission-definition.role_name |
| Total Users | number | N/A | Count of provider team members with this role across all providers | Display only, informational | ENT-role-permission-definition.user_count |
| Last Modified | datetime | N/A | When permissions were last updated | Display only | ENT-role-permission-definition.updated_at |
| Actions | button group | N/A | Edit Permissions, View Users | Owner role has a lock icon | no graph field (control) |

**Actions**:

- **Edit Permissions**: Opens permission matrix modal/panel for selected role (Provider Platform permissions)
- **View Users**: Links to FR-015 (Provider Management) to view providers and their team members with this role (REQ-031-080)

**Business Rules**:

- Owner role must always have full access to all provider features (cannot be restricted)
- The four provider roles (Owner, Manager, Clinical Staff, Billing Staff) cannot be renamed or removed, and no other provider roles can be created or cloned; Super Admins configure only their permissions (REQ-031-056; REQ-031-055)
- Actions limited to named roles (for example Owner only) stay limited to those roles even if the permission is granted to another role (REQ-031-068)
- Permission changes sync to Provider Platform (FR-009) within 5 seconds
- Permission changes affect all provider team members with that role across all providers (REQ-031-066)
- System shows warning when editing: "This will affect [count] provider team members across all provider organizations" (REQ-031-074)

**Notes**:

- Display sync status indicator: "Last synced to Provider Platform: [timestamp]" (REQ-031-079; ENT-role-permission-definition.last_synced_at)
- Show impact summary before saving: "This change will affect [X] providers and [Y] team members"

---

### Screen 2: Invite Team Member Form

**Purpose**: Allows Super Admin to invite new admin team members with role assignment. Accessed from "Invite Team Member" button in Admin Users tab.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---------------|
| First Name | text | Yes | Admin user's first name | Max 50 characters; letters, spaces, hyphens only | ENT-admin-user-account.first_name |
| Last Name | text | Yes | Admin user's last name | Max 50 characters; letters, spaces, hyphens only | ENT-admin-user-account.last_name |
| Email Address | email input | Yes | New admin user's email | Valid email format; unique (not already in use); lowercase conversion | ENT-admin-user-account.email |
| Phone Number | tel input | No | Admin user's phone number | E.164 format validation; optional for now (MFA implementation planned for future) | ENT-admin-user-account.phone_number |
| Assigned Role | select (dropdown) | Yes | Role to assign to new user | Must select from the active admin roles, including custom roles (predefined: Super Admin, Aftercare Coordinator, Billing Admin, Support Staff) | ENT-admin-user-account.assigned_role_id |
| Personal Message | textarea | No | Optional welcome message from Super Admin | Max 500 characters; included in invitation email | ENT-admin-user-account.personal_message |

**Actions**:

- **Send Invitation**: Generates invitation token and sends email
- **Cancel**: Closes form without sending invitation
- **Preview Email**: Opens preview modal showing how invitation email will appear

**Business Rules**:

- Email validation occurs on blur (field loses focus) for immediate feedback (REQ-031-034)
- System checks for duplicate email across all admin users (active, suspended, pending) (REQ-031-035)
- Role dropdown populated from active admin roles, including custom admin roles (REQ-031-036)
- Role dropdown displays: role name + brief description on hover (REQ-031-036)
- Form cannot be submitted until all required fields pass validation (REQ-031-033)
- Invitation token expires after 7 days (168 hours) (REQ-031-037)
- Personal message is optional but recommended for first-time team setup
- Phone number field is optional (MFA will be implemented in future enhancement) (REQ-031-048)

**Validation Messages**:

- Email already in use: "This email is already associated with an admin account. Please use a different email or check existing team members."
- Invalid email format: "Please enter a valid email address."
- Invalid phone format: "Please enter a valid phone number (e.g., +1234567890)." (REQ-031-121)
- Role not selected: "Please select a role for this team member."

**Notes**:

- Display role permission summary below role dropdown (expandable section showing what this role can access) (REQ-031-036)
- Show estimated invitation expiry time: "Invitation will expire in 7 days on [date] at [time]" (REQ-031-038)
- System auto-generates preview showing: invitee name, role, personal message (if provided), invitation link placeholder (REQ-031-038)
- After successful send, show confirmation: "Invitation sent to [email]. They have 7 days to accept." (REQ-031-038)

---

### Screen 3: Admin Account Setup (Onboarding)

**Purpose**: New admin user account creation after accepting invitation. This screen is accessed via the invitation link sent in the email. Collects account details and enforces security requirements before granting access to Admin Platform.

**Context**: Displayed after new admin user clicks invitation link in email and token is validated by system.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---------------|
| Email | display (read-only) | N/A | Pre-filled from invitation, locked | Read-only; must match invitation token | ENT-admin-user-account.email |
| First Name | text | Yes | Editable first name (pre-filled from invitation) | 2-50 characters; letters, spaces, hyphens only | ENT-admin-user-account.first_name |
| Last Name | text | Yes | Editable last name (pre-filled from invitation) | 2-50 characters; letters, spaces, hyphens only | ENT-admin-user-account.last_name |
| Phone Number | tel input | No | Primary contact phone for admin user | E.164 format (e.g., +1234567890); optional for now (MFA planned for future) | ENT-admin-user-account.phone_number |
| Password | password | Yes | Account password | Must satisfy the password policy (see system PRD, Platform-Wide Rules: Password and one-time-code policy) | ENT-admin-user-account.password_hash |
| Confirm Password | password | Yes | Re-enter password | Must match Password field exactly | no graph field (control) |
| Accept Terms | checkbox | Yes | Confirm platform terms & privacy policy | Must be checked before submission | ENT-admin-user-account.terms_accepted_at |

**Actions**:

- **Create Account**: Submits form and creates admin account
- **Cancel**: Returns to login page (invalidates the invitation token if clicked; the invitation then shows as "Expired") (REQ-031-047; REQ-031-039)

**Business Rules**:

- Email field is pre-filled from invitation token and cannot be edited (REQ-031-044)
- First Name and Last Name are pre-filled from invitation but can be edited (REQ-031-044)
- Password must meet the password policy: see system PRD, Platform-Wide Rules: Password and one-time-code policy (REQ-031-045; REQ-SYS-007)
- "Create Account" button disabled until all required fields are valid and terms are accepted (REQ-031-046)
- Phone number is optional for now (MFA enrollment will be added in future enhancement) (REQ-031-048)
- Invitation token validated before displaying form (REQ-031-040)
- Expired or invalid tokens redirect to error page with "Request New Invitation" option (REQ-031-040)

**Validation Messages**:

- Password too weak: "Password must be at least 12 characters with uppercase, lowercase, number, and special character from !@#$%^&(),.?\":{}|<>." (REQ-031-045)
- Password mismatch: "Passwords do not match." (REQ-031-045)
- Terms not accepted: "You must accept the Terms of Service to continue." (REQ-031-046)
- Invalid phone format: "Please enter a valid phone number (e.g., +1234567890)." (REQ-031-121)

**Success Flow**:

1. New admin user fills in all required fields
2. System validates all inputs
3. New admin user checks "Accept Terms" and clicks "Create Account"
4. System creates admin account with assigned role from invitation
5. System marks invitation as "Accepted"
6. System logs account creation in audit trail
7. System sends confirmation email to both new admin user and Super Admin who sent invitation
8. System displays success message: "Account created successfully! Redirecting to login..."
9. System redirects to admin login page after 3 seconds
10. New admin user can immediately log in with new credentials (REQ-031-049)

**Notes**:

- Display provider branding (Hairline Admin Platform logo and name) (REQ-031-122)
- Show invitation expiry countdown if less than 24 hours remaining: "Your invitation expires in [X] hours" (REQ-031-044)
- Show assigned role in header: "You've been invited as [Role Name]" (REQ-031-044)
- Include personal message from Super Admin if provided (display below header) (REQ-031-044)
- Security notice: "Strong password required. All admin actions are logged for security." (REQ-031-123)
- MFA enrollment section marked as "Coming Soon" with note: "Multi-factor authentication will be required in future updates" (REQ-031-048)

---

### Screen 4: Permission Matrix Modal (Super Admin Only)

**Purpose**: Modal/panel that opens when editing permissions for a specific role from Tab 1 (Admin Roles) or Tab 3 (Provider Roles). This is the **centralized RBAC configuration interface** where Super Admins define what each role can do.

**Access Control**: Only Super Admins can access this screen. Opened via "Edit Permissions" action from Tab 1 or Tab 3.

**View Modes**: Screen 4 supports two view modes:

1. **Single Role Edit Mode** (default): Edit permissions for one role at a time
2. **Matrix Comparison Mode**: View/edit permissions across multiple roles in a 2-axis table format

**Modal Header**:

- Title: "Edit Permissions: [Role Name]" (Single Role Mode) or "Permission Matrix: [Role Type]" (Matrix Mode)
- Role Type Badge: "Admin Role" or "Provider Role"
- View Toggle: Switch between "Single Role" and "Matrix View"
- User Count: "Currently assigned to [X] users" (Single Role Mode only)
- Warning (if Provider Role): "Changes will affect all provider organizations" (REQ-031-074)

---

#### View Mode 1: Single Role Edit (Default)

**Purpose**: Edit permissions for one specific role with detailed checkboxes organized by category.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---------------|
| Role Name | text | Yes | Name of role (e.g., "Aftercare Coordinator") | **Locked for system-defined roles**. Editable for custom admin roles only. When editable: max 50 chars; unique within the role's guard. | ENT-role-permission-definition.role_name |
| Role Description | textarea | Yes | Purpose and responsibilities of role | Max 500 chars | ENT-role-permission-definition.description |
| Permission Categories | accordion | Yes | Grouped permissions by feature area | At least one permission required | ENT-role-permission-definition.permissions, ENT-permission.feature_area, ENT-permission.permission_name, ENT-permission.description, ENT-permission.permission_category |

**Permission Matrix Structure** (Expandable Categories):

**Category: Dashboard & Overview (A-01)**: (REQ-031-101)

| Permission | Description | Access Level | Graph field |
|------------|-------------|--------------|---------------|
| View Dashboard | Access main admin dashboard | ☐ Read | ENT-permission |
| View Patient Overview | View patients across all lifecycle stages | ☐ Read | ENT-permission |

**Category: Patient Management (A-01)**: (REQ-031-102)

| Permission | Description | Access Level | Graph field |
|------------|-------------|--------------|---------------|
| View Patients | View patient list and profiles | ☐ Read | ENT-permission |
| Edit Patients | Modify patient information | ☐ Write | ENT-permission |
| Delete Patients | Archive patient accounts | ☐ Delete | ENT-permission |

**Category: Provider Management (A-02)**: (REQ-031-103)

| Permission | Description | Access Level | Graph field |
|------------|-------------|--------------|---------------|
| View Providers | View provider list and profiles | ☐ Read | ENT-permission |
| Edit Providers | Modify provider information | ☐ Write | ENT-permission |
| Onboard Providers | Create new provider accounts | ☐ Write | ENT-permission |
| Suspend Providers | Suspend/activate provider accounts | ☐ Delete | ENT-permission |

**Category: Aftercare Management (A-03)**: (REQ-031-104)

| Permission | Description | Access Level | Graph field |
|------------|-------------|--------------|---------------|
| View Aftercare Cases | View aftercare patient list | ☐ Read | ENT-permission |
| Manage Aftercare | Assign specialists, edit plans | ☐ Write | ENT-permission |
| Chat with Patients | Access aftercare chat | ☐ Write | ENT-permission |
| Schedule Consultations | Book video consultations | ☐ Write | ENT-permission |

**Category: Quotes & Inquiries Oversight (A-01)**: (REQ-031-105)

| Permission | Description | Access Level | Graph field |
|------------|-------------|--------------|---------------|
| View Inquiries Overview | View all inquiries across lifecycle stages | ☐ Read | ENT-permission |
| View Quote Details | View all quotes per inquiry | ☐ Read | ENT-permission |
| Edit Quotes | Modify quotes (provider cancellations, rescheduling) | ☐ Write | ENT-permission |
| Reassign Providers | Manually assign/reassign providers to inquiries | ☐ Write | ENT-permission |

**Category: Reviews & Ratings Management (A-01)**: (REQ-031-106)

| Permission | Description | Access Level | Graph field |
|------------|-------------|--------------|---------------|
| View Reviews | View all patient reviews | ☐ Read | ENT-permission |
| Moderate Reviews | Approve/reject/edit reviews | ☐ Write | ENT-permission |
| Add Reviews | Import authenticated reviews for providers | ☐ Write | ENT-permission |
| Manage Review Categories | Configure review categories and labels | ☐ Write | ENT-permission |

**Category: Billing & Financial (A-05)**: (REQ-031-107)

| Permission | Description | Access Level | Graph field |
|------------|-------------|--------------|---------------|
| View Transactions | View patient and provider transactions | ☐ Read | ENT-permission |
| Process Payouts | Initiate provider payouts | ☐ Write | ENT-permission |
| Issue Refunds | Process patient refunds | ☐ Write (requires approval; any admin holding this permission may approve, no second person is required; approval step defined in FR-007) (REQ-031-069; REQ-007-015) | ENT-permission |
| View Financial Reports | Access revenue analytics | ☐ Read | ENT-permission |
| View Patient Billing | View patient invoices and payment status | ☐ Read | ENT-permission |
| Send Payment Reminders | Send payment reminders to patients | ☐ Write | ENT-permission |
| Download Invoices | Download patient/provider invoices | ☐ Read | ENT-permission |

**Category: Promotions & Discounts (A-06)**: (REQ-031-108)

| Permission | Description | Access Level | Graph field |
|------------|-------------|--------------|---------------|
| View Discounts | View all discount codes (Hairline and provider) | ☐ Read | ENT-permission |
| Create Discounts | Create platform-wide discount codes | ☐ Write | ENT-permission |
| Edit Discounts | Modify discount parameters | ☐ Write | ENT-permission |
| Track Discount Usage | View discount statistics and ROI | ☐ Read | ENT-permission |
| Manage Admin Campaign Adoptions | Manage provider accept/decline participation and admin override actions for admin-created both-fees campaigns | ☐ Write | ENT-permission |

**Category: Affiliate Management (A-07)**: (REQ-031-109)

| Permission | Description | Access Level | Graph field |
|------------|-------------|--------------|---------------|
| View Affiliates | View affiliate list and details | ☐ Read | ENT-permission |
| Create Affiliates | Add new affiliate accounts | ☐ Write | ENT-permission |
| Edit Affiliates | Modify affiliate profiles and commission rules | ☐ Write | ENT-permission |
| Process Affiliate Payouts | Process affiliate commission payments | ☐ Write | ENT-permission |
| View Affiliate Performance | View referral counts and conversions | ☐ Read | ENT-permission |

**Category: Analytics & Reporting (A-08)**: (REQ-031-110)

| Permission | Description | Access Level | Graph field |
|------------|-------------|--------------|---------------|
| View Analytics Dashboard | Access platform-wide analytics overview | ☐ Read | ENT-permission |
| View Provider Analytics | View provider performance metrics | ☐ Read | ENT-permission |
| View Financial Analytics | View revenue and conversion analytics | ☐ Read | ENT-permission |
| Export Reports | Export analytics reports (PDF/CSV) | ☐ Read | ENT-permission |
| View Treatment Outcomes | Access treatment outcomes analytics | ☐ Read | ENT-permission |

**Category: Communication & Support (A-10)**: (REQ-031-111)

| Permission | Description | Access Level | Graph field |
|------------|-------------|--------------|---------------|
| View Support Center | Access patient support cases | ☐ Read | ENT-permission |
| Respond to Support | Send messages to patients/providers | ☐ Write | ENT-permission |
| View Provider-Patient Messages | Monitor provider-to-patient communications | ☐ Read | ENT-permission |
| Flag Communications | Flag suspicious or policy-violating messages | ☐ Write | ENT-permission |
| Export Conversation Transcripts | Export chat transcripts for compliance | ☐ Read | ENT-permission |

**Category: Travel Management (A-04)**: (REQ-031-112)

| Permission | Description | Access Level | Graph field |
|------------|-------------|--------------|---------------|
| View Travel Bookings | View flight and hotel bookings | ☐ Read | ENT-permission |
| Manage Travel Settings | Configure travel API settings and commissions | ☐ Write | ENT-permission |
| View Travel Reports | View travel booking analytics | ☐ Read | ENT-permission |

**Category: System Settings (A-09)**: (REQ-031-113)

| Permission | Description | Access Level | Graph field |
|------------|-------------|--------------|---------------|
| View Settings | View system configuration | ☐ Read | ENT-permission |
| Edit Settings | Modify system settings | ☐ Write (Super Admin only) (REQ-031-067) | ENT-permission |
| Manage Users | Create/edit admin accounts | ☐ Write (Super Admin only) (REQ-031-067) | ENT-permission |
| Manage Roles | Create/edit roles and permissions | ☐ Write (Super Admin only) (REQ-031-067) | ENT-permission |
| Manage Terms & Conditions | Edit patient/provider terms and consent | ☐ Write | ENT-permission |
| Manage App Data | Edit countries, discovery questions, location presentation | ☐ Write | ENT-permission |
| Manage Treatment Catalog | Create/edit treatments and packages | ☐ Write | ENT-permission |
| Manage Aftercare Templates | Create/edit aftercare milestone templates | ☐ Write | ENT-permission |
| Manage Notification Templates | Edit email templates (OTP, confirmations) | ☐ Write | ENT-permission |
| Configure Payment Settings | Manage Stripe accounts, commission rates, split pay | ☐ Write | ENT-permission |
| Manage Help Centre | Create/edit Help Centre content for providers | ☐ Write | ENT-permission |
| View Sensitive Settings | View the full value of sensitive settings (for example API keys) | ☐ Read | ENT-permission |
| Manage Authentication Policies | Edit authentication policy settings (for example lockout and session timeout) | ☐ Write | ENT-permission |

FR-026 refers to these permission names for its screens: View Settings, Edit Settings, View Sensitive Settings, Manage Authentication Policies, Manage App Data and Manage Notification Templates.

**Provider Platform Permission Categories** (for configuring the four provider roles):

**Category: Patient Inquiries & Quotes (PR-02)**: (REQ-031-114)

| Permission | Description | Access Level | Graph field |
|------------|-------------|--------------|---------------|
| View Inquiries | View patient inquiry list and details | ☐ Read | ENT-permission |
| Respond to Inquiries | Submit quotes and respond to inquiries | ☐ Write | ENT-permission |
| Edit Quotes | Modify submitted quotes | ☐ Write | ENT-permission |
| Accept/Decline Quotes | Accept or decline patient quote acceptances | ☐ Write | ENT-permission |
| View Quote History | View all quotes for inquiries | ☐ Read | ENT-permission |

**Category: Appointments & Scheduling (PR-02)**: (REQ-031-115)

> Note: In the System PRD, appointment slot pre-scheduling is part of the inquiry/quote flow; this category is tracked under PR-02 for module-code consistency.

| Permission | Description | Access Level | Graph field |
|------------|-------------|--------------|---------------|
| View Appointments | View scheduled appointments | ☐ Read | ENT-permission |
| Schedule Appointments | Create and schedule appointments | ☐ Write | ENT-permission |
| Edit Appointments | Modify appointment details | ☐ Write | ENT-permission |
| Cancel Appointments | Cancel scheduled appointments | ☐ Write | ENT-permission |
| View Calendar | Access provider calendar view | ☐ Read | ENT-permission |

**Category: Treatment & Procedures (PR-03)**: (REQ-031-116)

| Permission | Description | Access Level | Graph field |
|------------|-------------|--------------|---------------|
| View In-Progress Cases | View patients currently in treatment | ☐ Read | ENT-permission |
| Document Treatment | Add treatment notes, scans, photos | ☐ Write (Owner or Clinical Staff only) | ENT-permission |
| Update Treatment Status | Change patient treatment stage | ☐ Write | ENT-permission |
| View Treatment History | Access historical treatment records | ☐ Read | ENT-permission |

**Category: Aftercare Management (PR-04)**: (REQ-031-117)

| Permission | Description | Access Level | Graph field |
|------------|-------------|--------------|---------------|
| View Aftercare Cases | View aftercare patient list | ☐ Read | ENT-permission |
| Manage Aftercare Plans | Create and edit aftercare plans | ☐ Write | ENT-permission |
| Chat with Patients | Access aftercare messaging | ☐ Write | ENT-permission |
| Schedule Consultations | Book video consultations | ☐ Write | ENT-permission |
| View Progress Reports | Access patient progress data | ☐ Read | ENT-permission |

**Category: Financial & Billing (PR-05)**: (REQ-031-118)

| Permission | Description | Access Level | Graph field |
|------------|-------------|--------------|---------------|
| View Financial Dashboard | View revenue and earnings | ☐ Read | ENT-permission |
| View Payouts | View payment history and upcoming payouts | ☐ Read | ENT-permission |
| Manage Bank Details | Update payment account information | ☐ Write (Owner only) | ENT-permission |
| View Financial Reports | Access financial analytics | ☐ Read | ENT-permission |

**Category: Team Management (PR-01)**: (REQ-031-119)

| Permission | Description | Access Level | Graph field |
|------------|-------------|--------------|---------------|
| View Team Members | View team member list | ☐ Read | ENT-permission |
| Invite Team Members | Send team member invitations | ☐ Write | ENT-permission |
| Edit Team Member Roles | Change team member roles (non-Owner) | ☐ Write (Owner or Manager only) | ENT-permission |
| Remove Team Members | Remove or suspend team members | ☐ Write (Owner only) | ENT-permission |
| View Team Activity | Access team activity logs | ☐ Read | ENT-permission |

**Category: Provider Settings (PR-06)**: (REQ-031-120)

| Permission | Description | Access Level | Graph field |
|------------|-------------|--------------|---------------|
| View Profile | View provider profile information | ☐ Read | ENT-permission |
| Edit Profile | Update provider profile details | ☐ Write | ENT-permission |
| Manage Treatments | Add/edit treatment offerings | ☐ Write | ENT-permission |
| Manage Promotions | Create and edit discount codes | ☐ Write | ENT-permission |
| View Settings | View provider settings | ☐ Read | ENT-permission |
| Edit Settings | Modify provider settings | ☐ Write (Owner only) | ENT-permission |

**Modal Actions** (Single Role Mode):

- **Save Changes**: Saves permission changes and closes modal
- **Cancel**: Closes modal (shows confirmation dialog if unsaved changes exist)
- **Reset to Default**: Resets to system-recommended permissions for this role (if available) (REQ-031-076)
- **Preview Impact**: Shows which users and providers will be affected by changes (REQ-031-076)
- **Switch to Matrix View**: Switches to 2-axis matrix comparison view (shows confirmation dialog if unsaved changes exist)
- **Close (X button)**: Closes modal (shows confirmation dialog if unsaved changes exist)

---

#### View Mode 2: Matrix Comparison View

**Purpose**: View and edit permissions across multiple roles simultaneously in a 2-axis table format for easy comparison and bulk editing. (REQ-031-077)

**Layout**: 2-axis table where:

- **Rows** = Permissions (grouped by category/module)
- **Columns** = Roles (all roles of the same type: Admin or Provider, including custom admin roles)
- **Cell Values** = Checkboxes (☐ = unchecked, ☑ = checked) or access level indicators (Read/Write/Delete/None)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---------------|
| Role Type Filter | toggle | Yes | Filter to Admin Roles or Provider Roles | Single selection | no graph field (control) |
| Permission Categories | expandable sections | Yes | Group permissions by module/feature area | Expand/collapse per category | ENT-permission.feature_area |
| Matrix Table | table | Yes | 2-axis table with permissions as rows, roles as columns | Scrollable horizontally and vertically | ENT-permission.permission_name, ENT-permission.module_code, ENT-role-permission-definition.role_name, ENT-role-permission-definition.permissions, ENT-role-permission-definition.user_count |

**Matrix Table Structure**:

**Example for Admin Roles** (default permissions of the predefined roles):

| Permission | Category | Super Admin | Aftercare Coordinator | Billing Admin | Support Staff | Graph field |
|------------|----------|-------------|---------------------|---------------|---------------|---------------|
| View Dashboard | A-01 | ☑ | ☑ | ☑ | ☑ | ENT-permission, ENT-role-permission-definition |
| View Patient Overview | A-01 | ☑ | ☑ | ☑ | ☑ | ENT-permission, ENT-role-permission-definition |
| View Patients | A-01 | ☑ | ☑ | ☑ | ☑ | ENT-permission, ENT-role-permission-definition |
| Edit Patients | A-01 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| Delete Patients | A-01 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| View Quotes & Inquiries | A-01 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| Edit Quotes | A-01 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| View Reviews | A-01 | ☑ | ☑ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| Moderate Reviews | A-01 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| View Providers | A-02 | ☑ | ☑ | ☑ | ☑ | ENT-permission, ENT-role-permission-definition |
| Edit Providers | A-02 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| Onboard Providers | A-02 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| Suspend Providers | A-02 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| View Aftercare Cases | A-03 | ☑ | ☑ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| Manage Aftercare | A-03 | ☑ | ☑ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| Chat with Patients (Aftercare) | A-03 | ☑ | ☑ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| Schedule Consultations | A-03 | ☑ | ☑ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| View Transactions | A-05 | ☑ | ☐ | ☑ | ☐ | ENT-permission, ENT-role-permission-definition |
| Process Payouts | A-05 | ☑ | ☐ | ☑ | ☐ | ENT-permission, ENT-role-permission-definition |
| Issue Refunds | A-05 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| View Patient Billing | A-05 | ☑ | ☐ | ☑ | ☐ | ENT-permission, ENT-role-permission-definition |
| View Discounts | A-06 | ☑ | ☐ | ☑ | ☐ | ENT-permission, ENT-role-permission-definition |
| Create Discounts | A-06 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| View Affiliates | A-07 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| View Analytics | A-08 | ☑ | ☑ | ☑ | ☐ | ENT-permission, ENT-role-permission-definition |
| View Support Center | A-10 | ☑ | ☑ | ☐ | ☑ | ENT-permission, ENT-role-permission-definition |
| Respond to Support | A-10 | ☑ | ☑ | ☐ | ☑ | ENT-permission, ENT-role-permission-definition |
| View Settings | A-09 | ☑ | ☑ | ☑ | ☑ | ENT-permission, ENT-role-permission-definition |
| Edit Settings | A-09 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| Manage Users | A-09 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| Manage Roles | A-09 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |

**Example for Provider Roles** (default permissions of the four provider roles):

| Permission | Category | Owner | Manager | Clinical Staff | Billing Staff | Graph field |
|------------|----------|-------|---------|----------------|---------------|---------------|
| View Inquiries | PR-02 | ☑ | ☑ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| Respond to Inquiries | PR-02 | ☑ | ☑ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| View Appointments | PR-02 | ☑ | ☑ | ☑ | ☐ | ENT-permission, ENT-role-permission-definition |
| Schedule Appointments | PR-02 | ☑ | ☑ | ☑ | ☐ | ENT-permission, ENT-role-permission-definition |
| View In-Progress Cases | PR-03 | ☑ | ☑ | ☑ | ☐ | ENT-permission, ENT-role-permission-definition |
| Document Treatment | PR-03 | ☑ | ☑ | ☑ | ☐ | ENT-permission, ENT-role-permission-definition |
| View Financial Dashboard | PR-05 | ☑ | ☑ | ☐ | ☑ | ENT-permission, ENT-role-permission-definition |
| View Payouts | PR-05 | ☑ | ☑ | ☐ | ☑ | ENT-permission, ENT-role-permission-definition |
| Manage Bank Details | PR-05 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| View Team Members | PR-01 | ☑ | ☑ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| Invite Team Members | PR-01 | ☑ | ☑ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |

**Matrix View Features**:

- **Column Headers**: Role names with user count badges (e.g., "Super Admin (3 users)")
- **Row Headers**: Permission name + category/module code
- **Cell Interaction**: Click checkbox to toggle permission for that role
- **Bulk Actions**:
  - "Select All" checkbox in column header to grant all permissions to a role
  - "Select All" checkbox in row header to grant permission to all roles
  - "Select Category" to grant all permissions in a category to selected roles
- **Visual Indicators**:
  - Locked cells (Super Admin, Owner) shown with lock icon and disabled checkbox (REQ-031-077)
  - Permission dependencies highlighted (e.g., "Edit" row highlighted when "View" is checked)
  - Color coding: Green = granted, Gray = not granted, Red = locked/protected
- **Filtering**: (REQ-031-077)
  - Filter permissions by category/module
  - Search permissions by name
  - Show only differences between roles
- **Sorting**: (REQ-031-077)
  - Sort columns (roles) alphabetically or by user count
  - Sort rows (permissions) by category or alphabetically

**Modal Actions** (Matrix Mode):

- **Save All Changes**: Saves all permission changes across all roles and closes modal
- **Cancel**: Closes modal (shows confirmation dialog if unsaved changes exist)
- **Reset Role to Default**: Resets selected role(s) to system-recommended permissions (shows confirmation dialog if unsaved changes exist) (REQ-031-076)
- **Export Matrix**: Export matrix to CSV/Excel for documentation (REQ-031-077)
- **Switch to Single Role View**: Switches to single role edit mode for focused editing (shows confirmation dialog if unsaved changes exist)
- **Close (X button)**: Closes modal (shows confirmation dialog if unsaved changes exist)

**Business Rules** (Matrix Mode):

- All business rules from Single Role Mode apply
- Changes can be made to multiple roles simultaneously (REQ-031-077)
- System shows confirmation dialog listing all affected roles and user counts before saving (REQ-031-074)
- Locked roles (Super Admin, Owner) remain locked in matrix view
- Permission dependencies apply across all roles (e.g., checking "Edit" for any role auto-checks "View" for that role) (REQ-031-070)

**Business Rules** (Both Modes):

- Permissions organized by module code (A-01, A-02 for admin; PR-01, PR-02, etc. for provider) for traceability (REQ-031-072)
- "Select All" checkbox available for each category (REQ-031-072)
- Permission dependencies highlighted (e.g., "Edit Patients" requires "View Patients")
- System prevents saving role with zero permissions (REQ-031-071)
- **Admin Role Protection**: Super Admin permissions cannot be removed from Super Admin role (system protection, checkboxes disabled)
- **Provider Role Protection**: Owner role must always have full access to all provider features (cannot be restricted, checkboxes disabled for critical permissions)
- Permission changes take effect for all users with that role on the next API call after propagation (≤ 5 seconds)
- **Provider Permission Propagation**: Changes to provider role permissions automatically sync to Provider Platform (FR-009) within 5 seconds
- Role edits logged in audit trail with before/after permission comparison (REQ-031-081)
- **UI Enforcement**: Admin and Provider platforms hide UI elements (menu items, buttons, tabs, sections) for features users cannot access based on their role permissions (REQ-031-088)

**Validation**:

- Display warning when granting sensitive permissions (billing, user management, provider suspension) (REQ-031-073)
- Show confirmation dialog before saving: "This will affect [X] users. Continue?" (REQ-031-074)
- For provider roles: "This will affect [Y] team members across [Z] provider organizations. Continue?" (REQ-031-074)
- Highlight permission dependencies (selecting "Edit X" automatically selects "View X") (REQ-031-070)

**Notes**:

- Modal is scrollable for long permission lists
- Permissions grouped by feature area with expand/collapse accordions
- Search/filter box to quickly find specific permissions
**Unsaved Changes Protection**:

- **Detection**: System tracks all permission changes (checkbox toggles, bulk selections) and compares against saved state (REQ-031-078)
- **Warning Triggers**: Confirmation dialog appears when user attempts to:
  - Click "Cancel" button
  - Click "X" (close) button
  - Click outside modal (backdrop click)
  - Switch between view modes (Single Role ↔ Matrix)
  - Navigate away from page (browser back/forward)
- **Confirmation Dialog**:
  - Title: "Unsaved Changes"
  - Message: "You have unsaved changes. Are you sure you want to discard them?"
  - Options:
    - **"Discard Changes"**: Closes modal and discards all unsaved changes
    - **"Save Changes"**: Saves changes and then closes modal
    - **"Cancel"**: Returns to modal to continue editing
- **No Warning**: If no changes have been made, modal closes immediately without confirmation
- **Visual Indicator**: Modal header shows "Unsaved changes" badge or indicator when changes exist

---

### Screen 5: User Detail & Audit Trail

**Purpose**: Displays comprehensive information about specific admin user including activity history and permission changes

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---------------|
| User Profile | section (read-only) | N/A | Name, email, role, status, created date | - | ENT-admin-user-account.name, ENT-admin-user-account.email, ENT-admin-user-account.assigned_role_id, ENT-admin-user-account.status, ENT-admin-user-account.created_at |
| Current Role | badge | N/A | Currently assigned role with color coding | - | ENT-admin-user-account.assigned_role_id |
| Role Effective From | datetime | N/A | When the current role became (or will become) active | - | ENT-admin-user-account.role_effective_from |
| Role Change Acknowledged | datetime / badge | N/A | When the user acknowledged the latest role change, or Awaiting acknowledgement | Display only | ENT-admin-user-account.role_change_acknowledged_at |
| Last Login | datetime | N/A | Most recent successful login | - | ENT-admin-user-account.last_login_at |
| Login Count | number | N/A | Total number of logins since account creation | - | ENT-admin-user-account.login_count |
| Account Status | badge | N/A | Active/Suspended/Pending | - | ENT-admin-user-account.status |

**Audit Trail Table**:

| Column | Type | Description | Format | Graph field |
|--------|------|-------------|--------|---------------|
| Timestamp | datetime | When action occurred | "2025-11-14 14:32:15 UTC" | ENT-admin-audit-trail-entry.timestamp |
| Action Type | text | Type of action (Login, Role Change, Permission Grant, Access Denied) | Badge with color | ENT-admin-audit-trail-entry.action_type |
| Details | text | Description of action | "Role changed from 'Support Staff' to 'Aftercare Coordinator' by <admin@hairline.com>" | ENT-admin-audit-trail-entry.action_details |
| IP Address | text | IP address of action (security audit) | "192.168.1.1" | ENT-admin-audit-trail-entry.ip_address |
| Outcome | badge | Success/Failed/Denied | Color-coded | ENT-admin-audit-trail-entry.outcome |

**Business Rules**:

- Audit trail shows last 100 actions by default with "Load More" option (REQ-031-094)
- Audit trail searchable by action type, date range, outcome (REQ-031-094; REQ-022-117)
- Audit entries immutable (cannot be edited or deleted)
- Login failures logged with reason (invalid password, account suspended, etc.) (REQ-031-094)
- Access denial attempts logged with requested feature/endpoint (REQ-031-089)
- Audit trail exportable to CSV for compliance reporting (REQ-031-095)
- Sensitive actions (role changes, permission grants) highlighted in audit trail (REQ-031-094)
- Admin actions on a patient account (managed in FR-016) appear in the acting admin's audit trail on this screen; patient accounts and admin accounts remain separate records

**Notes**:

- Display security alerts if suspicious activity detected (multiple failed logins, unusual access patterns) (REQ-031-096)
- Provide "Send Password Reset" button for Super Admins (forces password reset on next login) (REQ-031-093)
- Show comparison view when viewing role change events (old role permissions vs new role permissions) (REQ-031-094)

---

## Business Rules

### General Module Rules

- **Rule 1**: Every admin user MUST have exactly one role assigned (no "roleless" accounts) (REQ-031-050)
- **Rule 2**: Super Admin role MUST always have full system access (cannot be restricted) (REQ-031-051)
- **Rule 3**: Authorization MUST be evaluated server-side on every API call using the latest role assignment and permission matrix. Server-side caching is allowed only if invalidated/updated within 5 seconds of a role/permission change; enforcement MUST reflect changes on the next API call after cache invalidation. (REQ-031-020; REQ-031-026)
- **Rule 4**: At least one active Super Admin account MUST exist at all times (system protection against lockout) (REQ-031-085)
- **Rule 5**: All administrative actions (role changes, permission grants, user suspensions) MUST be logged in audit trail (REQ-031-008; REQ-031-083)
- **Rule 6**: Invitation tokens expire after 7 days (configurable via A-09 settings; range 1-30 days) (REQ-031-037)
- **Rule 7**: Suspended admin users cannot log in but accounts remain in system (soft suspension, not deletion); Super Admin accounts are never suspended inside the product (REQ-031-053; REQ-031-009)
- **Rule 8**: Role assignments MUST be stored with an **Effective From** timestamp; enforcement MUST respect that effective date/time on authorization checks (REQ-031-011; REQ-031-082)
- **Rule 9**: Role names for system-defined roles (admin + provider) MUST be immutable (not editable/renamable); only custom admin roles can be renamed. (REQ-031-055)
- **Rule 10**: After an admin user's role changes, the user MUST acknowledge the change within 24 hours; the acknowledgement time is stored on the account and shown to Super Admins (REQ-031-124)
- Only active roles can be assigned to new or existing users (REQ-031-036)
- **Role Definition**: An admin role may be assigned to admin users; a provider role may be assigned across provider organizations. Each role has permission grants; cloned admin roles retain an independent permission snapshot. (REQ-031-057)
- **Admin User Account**: One admin user has one assigned role; one role can be assigned to many admin users (REQ-031-050)
- Admin platform accessed via modern web browsers (Chrome, Firefox, Safari, Edge - latest 2 versions)
- Admin users will primarily access platform from trusted devices/networks (office, VPN)
- Super Admins will review and update team member roles periodically (quarterly or when responsibilities change)
- Email delivery service (SendGrid/SES) has 99%+ uptime for invitation emails
- Super Admin role assigned to senior operations staff (CEO, CTO, Operations Manager)
- Aftercare coordinators check aftercare cases at least twice daily during business hours
- Billing Admins process payouts on scheduled basis (weekly, bi-weekly, or monthly)
- Support staff respond to patient and provider inquiries within 24 hours

### Data & Privacy Rules

- **Privacy Rule 1**: Audit trail entries are immutable; retention follows the system PRD, Platform-Wide Rules: One 10-year retention period (REQ-031-015; REQ-SYS-002)
- **Privacy Rule 2**: IP addresses logged for security audit purposes (GDPR-compliant logging) (REQ-031-014)
- **Privacy Rule 3**: Password reset requests logged in audit trail with requester identity (REQ-031-092)
- **Audit Rule**: All access to sensitive features (billing, patient medical data, provider financial data) MUST be logged with: timestamp, user ID, action, IP address, outcome (REQ-031-091)
- **GDPR Compliance**: Admin user data (email, name) can be anonymized on account deletion request, but audit trail preserved with anonymized identifiers (REQ-031-022)
- **System Clock / Time Service**: Accurate timestamps for audit trail entries and token expiration; System time (NTP synchronized); Use server time as fallback; alert if time drift detected
- **Architecture**: Role-based access control (RBAC) implemented via middleware on all admin API endpoints
- **Technology**: Permission checks execute before business logic (fail-fast approach)
- **Integration 1**: Admin API endpoints check permissions via middleware
  - **Data format**: JWT token containing authenticated user/session identifiers (not authoritative role/permission claims)
  - **Authentication**: Bearer token authentication
  - **Error handling**: Return 403 Forbidden with clear error message if permission denied
- **Integration 2**: Notification Service for invitation and role change emails
  - **Data format**: JSON payload with email template ID, recipient email, template variables
  - **Authentication**: Internal service-to-service authentication (API key)
- **Integration 3**: Audit trail writes for all admin actions
  - **Authentication**: Internal service (no external auth)
  - **Error handling**: Buffer audit entries and batch-write to database; alert if audit writes fail (critical security issue)
- **Authentication**: MFA support planned (MFA will be a mandatory control for all admin platform users Post-MVP, once the shared stack is available per Constitution Principle II) (REQ-031-016)
- **Authorization**: Role-based access control with granular permissions per feature/module
- **Threat mitigation**: Rate limiting on admin login endpoint to prevent brute-force attacks (max 5 attempts per 15 minutes) (REQ-031-100)
- Both modules share the underlying authorization infrastructure while keeping **admin roles** (Super Admin, Aftercare Coordinator, Billing Admin, Support Staff) separate from **provider roles** in terms of management, but unified in terms of permission configuration
- **Data format**: Structured log entries (timestamp, user_id, action_type, details, IP address, outcome)

### Provider Role Permission Rules

- **Provider Rule 1**: Provider role descriptions in FR-009 are recommended defaults; the configured permission matrix in FR-031 is authoritative and may grant additional access (e.g., Clinical Staff granted read-only financial reporting) (REQ-031-064)

### Admin Editability Rules

**Editable by Super Admin**:

- Create, edit, delete custom admin roles (REQ-031-057)
- Assign/change roles for any admin user (REQ-031-054)
- Suspend/activate admin accounts
- Configure invitation token expiry time (default 7 days, range 1-30 days) (REQ-031-037)
- Create permission matrix for custom admin roles
- Re-send invitation emails for pending accounts (REQ-031-042)

**Fixed in Codebase (Not Editable)**:

- Super Admin role permissions (always full access) (REQ-031-051)
- System role names (Super Admin, Aftercare Coordinator, Billing Admin, Support Staff) and the four protected provider role names (Owner, Manager, Clinical Staff, Billing Staff) (REQ-031-055)
- Owner-only provider capabilities (REQ-031-068)
- Core permission categories (cannot rename or remove: Patient Management, Provider Management, Billing, etc.) (REQ-031-065)
- Audit trail retention period (retention follows the system PRD, Platform-Wide Rules: One 10-year retention period) (REQ-031-015; REQ-SYS-002)
- Password hashing algorithm (bcrypt, cost factor 12) (REQ-031-017)
- Password requirements (see system PRD, Platform-Wide Rules: Password and one-time-code policy) (REQ-SYS-007)

**Configurable with Restrictions**:

- Invitation token expiry (configurable within 1-30 day range) (REQ-031-037)
- Maximum failed login attempts before lockout (configurable in A-09: Authentication Settings; default 5 failed attempts with a 15-minute lockout, the same setting as FR-001; the admin login rate limit (REQ-031-100) is a separate control and stays) (REQ-031-099)
- Session timeout duration: the admin inactivity timeout set in A-09 (FR-026; default 30 minutes) (REQ-031-099)
- Number of concurrent sessions per admin user (default: 3, range: 1-5) (REQ-031-099)
- Repeated access denial alert threshold (default 5 refusals for one admin within 10 minutes; configurable in A-09) (REQ-031-090)

---

## Dependencies

- **FR-009**: Provider Team & Role Management (consumes and enforces the provider role permission matrices configured in FR-031)
- **FR-015**: Provider Management (provider organizations and oversight of provider team members)
- **FR-020**: Notifications & Alerts (transactional email/in-app alerts for admin invitations, role changes, suspensions, and audit events; module S-03 Notification Service)
- **FR-026**: App Settings & Security Policies (authentication settings used by admin login and password reset flows)
- **FR-001**: Patient Auth & Profile Management (shared authentication infrastructure and security patterns)
- **Modules A-01 through A-10**: all Admin Platform modules (permission checks enforced across all admin features)

---

## User Scenarios & Testing

### User Story 1 - Invite Aftercare Coordinator (Priority: P1)

As a Super Admin, I need to invite a new aftercare nurse to the admin platform so they can start managing aftercare cases without accessing sensitive billing or provider data.

**Why this priority**: Core onboarding workflow required for day-one operations; enables team growth and role separation

**Independent Test**: Can be fully tested by creating new admin account, assigning "Aftercare Coordinator" role, and verifying access to aftercare features only

**Acceptance Scenarios**:

1. **Given** Super Admin is logged into admin platform, **When** Super Admin invites new user with email "<nurse@hairline.com>" and role "Aftercare Coordinator", **Then** invitation email sent within 1 minute and new account created with status "Pending"

2. **Given** new aftercare nurse receives invitation email, **When** nurse clicks activation link and sets password, **Then** account activated and nurse can log in with aftercare dashboard access

3. **Given** aftercare nurse is logged in, **When** nurse attempts to access Billing section, **Then** access denied with message "You do not have permission to access this feature" and attempt logged in audit trail

---

### User Story 2 - Create Custom Role for Analytics Staff (Priority: P2)

As a Super Admin, I need to create a custom "Analytics Viewer" role with read-only access to reports and dashboards, so analytics staff can view data without modifying it.

**Why this priority**: Enables specialized roles for growing team; supports principle of least privilege

**Independent Test**: Can be tested by creating custom role with read-only permissions, assigning to test user, and verifying read access without write capabilities

**Acceptance Scenarios**:

1. **Given** Super Admin navigates to Settings > User Roles & Permissions, **When** Super Admin creates new role "Analytics Viewer" with permissions: View Financial Reports (read), View Patient Data (read), View Provider Data (read), **Then** role saved and available in role dropdown for user assignment

2. **Given** custom role "Analytics Viewer" exists, **When** Super Admin assigns role to user "<analyst@hairline.com>", **Then** user can view reports but cannot edit data, process payouts, or modify settings

3. **Given** analytics viewer is logged in, **When** user attempts to edit patient information, **Then** edit button hidden or disabled and action denied if attempted via API

---

### User Story 3 - Configure Provider Role Permissions (Priority: P1)

As a Super Admin, I need to configure the permissions of the four provider roles so that provider team members have appropriate access to platform features based on their role, and these permissions are consistently enforced across all provider organizations.

**Why this priority**: Centralized RBAC configuration ensures consistent security policies; provider role permissions must be configurable from Admin Platform; changes must propagate to Provider Platform automatically

**Independent Test**: Can be tested by modifying provider role permissions in FR-031, verifying changes sync to Provider Platform (FR-009), and confirming provider team members receive updated permissions

**Acceptance Scenarios**:

1. **Given** Super Admin navigates to Settings > User Roles & Permissions and selects "Provider Roles" view, **When** Super Admin edits "Clinical Staff" role and grants "View Financial Reports" permission, **Then** permission change saved and synced to Provider Platform within 5 seconds

2. **Given** Clinical Staff role permissions have been updated, **When** a provider team member with Clinical Staff role logs in or refreshes, **Then** they can now access financial reports (if granted) or are denied access (if removed)

3. **Given** Super Admin attempts to remove critical permissions from Owner role, **When** Super Admin tries to save changes, **Then** system blocks action with error: "Owner role must maintain full access to all provider features"

4. **Given** provider role permission change has been made, **When** Super Admin views audit trail, **Then** change is logged with: role name, permissions added/removed, affected provider count, timestamp, and actor

---

### User Story 4 - Audit Trail Review for Compliance (Priority: P1)

As a Super Admin, I need to review audit trail of all administrative actions to ensure compliance with data protection regulations and identify unauthorized access attempts.

**Why this priority**: Critical for compliance with healthcare data regulations (HIPAA, GDPR); required for security audits

**Independent Test**: Can be tested by performing various admin actions (role changes, suspensions, access attempts) and verifying all actions logged with correct details

**Acceptance Scenarios**:

1. **Given** Super Admin navigates to User Audit Trail, **When** Super Admin selects user "<support@hairline.com>", **Then** audit trail displays all actions by that user with timestamps, action types, and outcomes

2. **Given** admin user with "Support Staff" role attempts to access Provider Billing section, **When** access denied due to insufficient permissions, **Then** access denial logged in audit trail with: timestamp, user ID, requested feature, IP address, outcome "Denied" (REQ-031-089)

3. **Given** Super Admin reviews audit trail for last 30 days, **When** Super Admin exports audit log to CSV, **Then** CSV file contains all audit entries with columns: timestamp, user, action, details, IP address, outcome

---

### User Story 5 - Role Change Notification (Priority: P2)

As an admin user, I need to be notified immediately when my role or permissions change, so I understand what features I can now access or no longer access.

**Why this priority**: Transparency and user awareness; reduces support tickets from confused users

**Independent Test**: Can be tested by changing user's role and verifying email notification sent with permission comparison

**Acceptance Scenarios**:

1. **Given** admin user "<support@hairline.com>" has role "Support Staff", **When** Super Admin changes role to "Aftercare Coordinator", **Then** user receives email notification within 5 minutes with: old role, new role, permission changes summary (REQ-031-084)

2. **Given** role change notification received, **When** user logs in after role change, **Then** dashboard reflects new role permissions (aftercare features visible, support features hidden)

3. **Given** user's role changed from "Billing Admin" to "Support Staff", **When** user attempts to access previously permitted billing feature, **Then** access denied and user informed: "Your permissions have changed. You no longer have access to this feature." (REQ-031-084)

---

### User Story 6 - Prevent System Lockout (Priority: P1)

As a platform administrator, I need the system to prevent any Super Admin account from being suspended by another user, removed, demoted or self-deactivated inside the product, so the platform always has an admin with full access.

**Why this priority**: Critical system protection; prevents complete lockout requiring database intervention

**Independent Test**: Can be tested by attempting to suspend, demote or deactivate a Super Admin account and verifying the action is blocked

**Acceptance Scenarios**:

1. **Given** a Super Admin account exists ("<admin@hairline.com>"), **When** another admin attempts to suspend this account, **Then** action blocked with error message: "A Super Admin account cannot be suspended. Super Admin accounts can only be changed outside the product."

2. **Given** two Super Admin accounts exist, **When** one Super Admin attempts to suspend the other, **Then** action blocked with the same message and both accounts stay active

3. **Given** a Super Admin is signed in, **When** they attempt to change their own role or deactivate their own account, **Then** action blocked with message: "A Super Admin account cannot be demoted or deactivated in the product. This can only be done outside the product."

---

### Edge Cases

- **Edge Case 1**: What happens when admin user's session is active and their role is changed by another Super Admin?
  - **Handling**: Current session remains valid until next API call; next API call checks updated permissions and enforces new role; user may see "Permission denied" on action if new role lacks permission; session not forcibly terminated (graceful permission enforcement) (REQ-031-087)

- **Edge Case 2**: How does system handle simultaneous role changes by two Super Admins on the same user?
  - **Handling**: Database-level locking prevents concurrent updates; second Super Admin receives error: "Role change failed - this user's role was just updated by another admin. Refresh and try again." Audit trail logs both attempts with outcomes (success, conflict) (REQ-031-086)

- **Edge Case 3**: What occurs if invitation email delivery fails (email service down)?
  - **Handling**: System retries the invitation email according to the FR-030 notification retry rule; while sending keeps failing the invitation shows "Pending Send" and the Super Admin is notified; if the email still cannot be sent 24 hours after the invitation was created, the invitation becomes "Expired"; Super Admin can re-send the invitation once the email service is restored (REQ-031-043; REQ-030-008)

- **Edge Case 4**: How to manage admin user who forgets password before activating account?
  - **Handling**: Pending activation accounts do not support password reset (no password set yet); user must request new invitation from Super Admin; original invitation token invalidated to prevent duplicate accounts (REQ-031-093)

- **Edge Case 5**: What happens if audit trail write fails (database connection lost)?
  - **Handling**: Critical actions (role changes, suspensions) buffered in memory and retried on database reconnection; if buffer full or database unavailable for extended period, admin actions temporarily blocked with message: "System maintenance in progress. Please try again shortly." Alert sent to infrastructure team immediately (audit trail failure is critical security issue) (REQ-031-097)

---

## Functional Requirements Summary

### Core Requirements

- **REQ-031-001**: System MUST allow Super Admins to invite new admin team members via email with role assignment; the invitation email is sent within 1 minute
- **REQ-031-002**: System MUST support creation of custom roles with granular permission assignment per admin module (A-01 through A-10)
- **REQ-031-003**: System MUST enforce role-based access control on all admin API endpoints and UI components
- **REQ-031-004**: System MUST provide predefined admin roles: Super Admin, Aftercare Coordinator, Billing Admin, Support Staff
- **REQ-031-005**: System MUST provide centralized configuration for the permissions of the four provider roles (Owner, Manager, Clinical Staff, Billing Staff); no other provider roles exist
- **REQ-031-006**: System MUST automatically sync provider role permission changes to Provider Platform (FR-009) within 5 seconds
- **REQ-031-007**: System MUST prevent modification of Owner role permissions that would remove full access to provider features, with the message: "Owner role must maintain full access to all provider features"
- **REQ-031-008**: System MUST log all administrative actions (role changes, permission grants, user suspensions, access denials) in immutable audit trail
- **REQ-031-009**: System MUST NOT allow a Super Admin account to be suspended by another user, or removed, demoted or self-deactivated inside the product (system protection; if ever needed, this is done outside the product), and MUST show a message saying so when it is attempted
- **REQ-031-010**: System MUST send email notifications for: new invitations, role changes, password resets, repeated access denials
- **REQ-031-011**: System MUST support role assignment changes with **Effective From** date/time tracking (stored and auditable)
- **REQ-031-124**: System MUST ask an admin user to acknowledge a role change within 24 hours; the acknowledgement time is stored on the account and shown to Super Admins

### Data Requirements

- **REQ-031-012**: System MUST maintain admin user accounts with: email, name, password hash, assigned role, role effective date/time, role change acknowledgement time, status (active/pending/suspended), creation date, last login timestamp
- **REQ-031-013**: System MUST maintain role definitions with: guard-scoped role name, description, assigned permissions (as permission matrix), and system/custom status (custom roles exist for admin roles only)
- **REQ-031-014**: System MUST maintain audit trail entries with: timestamp, user ID, action type, action details, IP address, outcome (success/failed/denied)
- **REQ-031-015**: Audit trail retention follows the system PRD, Platform-Wide Rules: One 10-year retention period

### Security & Privacy Requirements

- **REQ-031-016**: System MUST be architected to support Multi-Factor Authentication (MFA) integration as a planned Post-MVP requirement (per Constitution Principle II)
- **REQ-031-017**: System MUST use bcrypt (cost factor 12+) for password hashing
- **REQ-031-018**: Retired. Password requirements follow the system PRD, Platform-Wide Rules: Password and one-time-code policy.
- **REQ-031-019**: System MUST sign JWT tokens with RS256 (asymmetric encryption) to prevent tampering
- **REQ-031-020**: System MUST perform server-side authorization evaluation on each API call based on current role assignments and permission matrices; JWT tokens MUST NOT be the authoritative source of permissions
- **REQ-031-021**: System MUST invalidate active sessions (and/or reject access tokens) immediately upon account suspension; at minimum, all API calls MUST be rejected for suspended accounts starting with the next request
- **REQ-031-022**: System MUST anonymize admin user PII (email, name) on account deletion request, while preserving audit trail with anonymized identifier

### Integration Requirements

- **REQ-031-023**: System MUST send the admin invitation, role change and password reset emails through the platform notification service defined in FR-020
- **REQ-031-024**: System MUST provide permission check API for all admin modules to enforce access control
- **REQ-031-025**: System MUST cache permission matrix in memory for fast authorization checks (< 50ms per check)
- **REQ-031-026**: System MUST invalidate permission cache within 5 seconds of role or permission changes

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-11-22 | 1.3 | Requirements graph programme baseline: PRD compressed to the checklist structure (each rule stated once, field rows tagged with graph field ids, dropped classes removed). No rule changes. Earlier history (v1.0 to v1.2) and the change request CR-FR031-20260929-01 (file change-request-2026-09-29-global-custom-provider-roles.md) are in `archived/prd-baseline-2026-11-08/fr031-admin-access-control/` and in git history. | Documentation |
| 2026-11-23 | 1.4 | Owner ruling 2026-11-23: the aftercare specialist is clinic staff on the provider side; the Hairline admin role is renamed Aftercare Coordinator with unchanged permissions. Role name replaced in 18 place(s). No permission change. | Documentation |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | TBD | 2026-01-04 | ✅ Verified & Approved |
| Technical Lead | TBD | 2026-01-04 | ✅ Verified & Approved |
| Security Lead | TBD | 2026-01-04 | ✅ Verified & Approved |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-011 Aftercare & Recovery Management PRD
**Last Updated**: 2026-11-23 (requirements graph programme baseline; prior approval dated 2026-01-04)
