# FR-031 - Admin Access Control & Permissions

**Module**: A-09: System Settings & Configuration
**Feature Branch**: `fr031-admin-access-control`
**Created**: 2025-11-14
**Status**: Revision v1.7 (requirements graph programme baseline with logic review pass 2 and cross-FR alignment applied); v1.0.2 baseline verified and approved
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
8. System validates email format and checks for duplicate email within admin team; if the chosen role holds a sensitive permission, System shows the sensitive-permission warning with the role's permission summary and the Super Admin confirms (REQ-031-073)
9. Super Admin reviews invitation details and clicks "Send Invitation"
10. System generates secure invitation token (expires after the configured invitation expiry; 7 days at launch)
11. System creates the new admin user's account with the assigned role and status "Invited" and records the invitation on it (REQ-031-039)
12. System sends email to invitee with invitation link, Hairline Admin Platform branding, and role being offered (sent within 1 minute of the Super Admin clicking Send Invitation)
13. System displays confirmation message to Super Admin
14. New Admin User receives email and clicks invitation link
15. System validates invitation token (not expired, not already used)
16. System displays Admin Account Setup screen (Screen 3) pre-filled with email, first name, last name
17. New Admin User reviews pre-filled information, enters phone number (optional), sets password, and accepts the Admin Terms of Service (acceptance belongs to this feature; the legal text is maintained under REQ-027-011)
18. New Admin User clicks "Create Account"
19. System validates all inputs (password strength, Admin Terms of Service acceptance)
20. System sets the account Active with the assigned role
21. System marks invitation as "Accepted"
22. System sends confirmation email to both Super Admin and new admin user
23. System logs account creation in audit trail
24. System displays success message and redirects to login page
25. New Admin User can immediately log in with new credentials

### Alternative Flows

**A1: Re-send Invitation (Pending or Expired)**:

- **Trigger**: An invitation is still pending (status "Invited", or "Pending Send" from the first failed delivery, B4) or its token expired, and the admin user hasn't signed up
- **Steps**:
  1. Super Admin opens the Pending Invitations sub-tab of the Admin Users tab
  2. System shows each invitation's status ("Invited", "Expired" or "Pending Send")
  3. Super Admin clicks "Resend Invitation" button
  4. System generates new invitation token and sends new email
  5. Old invitation token invalidated
- **Outcome**: Admin user receives fresh invitation with a new expiry (the configured invitation expiry, 7 days at launch)

**A2: Role Change for Existing Admin User**:

- **Trigger**: Admin user's responsibilities change, requiring different role
- **Steps**:
  1. Super Admin navigates to Settings > User Roles & Permissions > Admin Users tab
  2. Super Admin selects target admin user from the list (a Super Admin row has no Change Role action, REQ-031-054)
  3. Super Admin clicks "Change Role" action
  4. System displays role change dialog with current role highlighted
  5. Super Admin selects new role from dropdown
  6. Super Admin sets **Effective From** date/time (default: now; the earliest allowed value is now)
  7. System displays permission comparison (current vs new role permissions) and effective date/time (REQ-031-075); if the new role holds a sensitive permission, System also shows the sensitive-permission warning with the role's permission summary (REQ-031-073)
  8. Super Admin confirms role change (and the warning, when shown)
  9. System validates Effective From is not before now
  10. System stores the new role as the user's pending role with its Effective From; the current role stays in force until Effective From, and a second role change made before then replaces the pending one (REQ-031-125)
  11. System logs role change in audit trail (who changed, old role, new role, effective_from, timestamp)
  12. System sends email notification to affected user about role change (includes effective date/time)
  13. System shows the affected admin an "Acknowledge role change" banner on the admin dashboard, on every admin page until acknowledged (not inside the Super Admin-only module), once the change takes effect (plus a link in the email); when the affected admin clicks it, System stores the time in role_change_acknowledged_at; the 24 hours of Rule 10 start when the change takes effect, and Super Admins see an "Overdue" flag on an unacknowledged change after that (nothing is blocked and no reminder is sent)
  14. At Effective From the pending role becomes the user's role and System enforces its permissions on the first API call at or after that time
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
  7. System displays permission summary and potential conflicts/warnings, including the sensitive-permission warning (B6, REQ-031-073)
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
  17. If the sync in step 14 fails, System marks the role's sync status "Sync failed" and retries automatically (3 tries)
  18. System sends an in-app alert to all Super Admins
  19. The Provider Roles tab shows the role as "not yet applied" until a retry succeeds (REQ-031-130)
  20. If the 3 automatic tries all fail, the role stays "Sync failed / not yet applied"; a Super Admin presses "Retry sync" on the Provider Roles tab (saving the matrix again also re-sends it), and System re-sends the role and logs every attempt in the audit trail (REQ-031-130)
- **Outcome**: Provider role permissions updated and automatically propagated to all provider organizations; changes enforced immediately

**A7: Edit Admin Role Permissions**:

- **Trigger**: Super Admin changes what an existing admin role other than Super Admin may do
- **Steps**:
  1. Super Admin opens the Admin Roles tab and clicks "Edit Permissions" on the role
  2. System opens Permission Matrix Modal (Screen 4) with the role's current permissions
  3. Super Admin changes permissions and clicks "Save Changes"; System shows the comparison of additions and removals and the sensitive-permission warning when needed (B6)
  4. System saves the matrix and logs the change in the audit trail with before and after
  5. System sends the permission change email (REQ-031-032) to every admin user holding the role
  6. On each signed-in user's next request System checks the updated permissions; no session is ended (REQ-031-087)
- **Outcome**: The role's new permissions apply to everyone holding it from their next request (REQ-031-131)

**A8: Suspend, Reactivate or Delete an Admin Account**:

- **Trigger**: Super Admin needs to stop, restore or remove an admin account other than a Super Admin account
- **Steps**:
  1. Super Admin clicks "Suspend" on the row of an Active user in the Admin Users tab (Suspend is offered on Active accounts only)
  2. System asks for confirmation and a required reason
  3. System sets status "Suspended", ends the user's active sessions, emails the user and logs the action with the reason in the audit trail
  4. To restore, Super Admin clicks "Reactivate" on the suspended user (offered on Suspended accounts only); System sets status Active, emails the user and logs the action
  5. To remove, Super Admin clicks "Delete" on a suspended user (offered on Suspended accounts only) and confirms; System anonymises the user's name and email under REQ-031-022, keeps the audit entries with the anonymised identifier, sets status "Deleted" and logs the deletion; a Deleted account is hidden from the Admin Users list unless the Status filter "Deleted" is chosen, offers only View Audit and cannot be reactivated
  6. An "Invited" account is removed only with Cancel (A9), and Change Role is not offered on it (cancel and re-invite instead)
- **Outcome**: Access stopped, restored or removed with a full audit record; a Super Admin account shows none of these actions and is only changed outside the product (REQ-031-126)

**A9: Cancel a Pending Invitation**:

- **Trigger**: Super Admin withdraws an invitation that has not been accepted (this includes an invitation for a Super Admin role: REQ-031-009 protects accepted Super Admin accounts only, and Resend works the same way until the invitation is accepted)
- **Steps**:
  1. Super Admin opens the Pending Invitations sub-tab and clicks "Cancel" on an invitation
  2. System asks for confirmation
  3. System removes the "Invited" account, invalidates the invitation link and logs the cancellation in the audit trail
- **Outcome**: The invitation and its account no longer exist and the link no longer works (REQ-031-127)

**A10: Request New Invitation**:

- **Trigger**: Invitee opens an expired or invalid invitation link
- **Steps**:
  1. System shows the error page with a "Request New Invitation" option
  2. Invitee clicks "Request New Invitation"
  3. System notifies all Super Admins by email and in the app, with a link to the invitation row in the Pending Invitations sub-tab
  4. A Super Admin resends the invitation (A1)
- **Outcome**: Super Admins learn that the invitee is waiting (REQ-031-128)

**A11: Delete or Clone a Custom Admin Role**:

- **Trigger**: Super Admin removes a custom admin role or starts a new one from an existing role
- **Steps**:
  1. Super Admin clicks "Delete" on a custom role in the Admin Roles tab
  2. System blocks the deletion while any admin user (including an "Invited" account; a Deleted account does not count) or any pending role change holds the role, and tells the Super Admin to reassign them first
  3. Otherwise System asks for confirmation, deletes the role and logs the deletion in the audit trail
  4. To clone, Super Admin clicks "Clone Role"; System opens the creation form with the permissions copied and the name "Copy of [role name]", editable and cut to 50 characters, and saving continues as in A3
- **Outcome**: A custom role is removed only when nobody holds it; a clone is an independent role (REQ-031-129)

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
  4. System marks the invitation "Pending Send" from the first failed delivery
  5. System displays warning to Super Admin: "Invitation created but the email could not be sent yet. The system retries under the notification rule, and you can resend the invitation yourself. The invitation expires if it is still unsent after 24 hours."
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
  6. System sends alert to Super Admin when one admin is refused 5 times within 10 minutes (launch default; the count and the time window are each an admin setting in A-09; potential security issue)
- **Outcome**: Unauthorized features hidden from UI; access blocked if directly accessed; security event logged

**Note**: The system follows "hide first, deny second" approach:

- **Preferred**: Hide unauthorized menu items, buttons, and navigation elements so users never see features they can't access
- **Fallback**: Display access denied message only when hiding is not feasible (direct URL access, shared pages with partial access)

**B6: Sensitive Permission Warning**:

- **Trigger**: Super Admin saves a permission matrix that adds a sensitive permission, or assigns a role that holds one (sensitive permissions: all financial write permissions such as refunds, payouts and payment settings, Manage Roles, Manage Users and Delete Patients; REQ-031-073)
- **Steps**:
  1. System detects role contains sensitive permissions (flagged as "sensitive" in permission definition)
  2. System displays warning modal: "This role grants access to sensitive features: [Issue Refunds, Process Payouts, Manage Users]. Confirm?"
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
| Actions | button group | N/A | Edit Permissions, View Users, Clone Role, Delete (custom roles only) | Edit Permissions and Clone Role are disabled for the Super Admin role; View Users stays available (REQ-031-052) | no graph field (control) |

**Actions**:

- **Edit Permissions**: Opens permission matrix modal/panel for selected role
- **View Users**: Switches to Tab 2 filtered by this role (REQ-031-080)
- **Clone Role**: Creates new custom role based on existing role; the name starts as "Copy of [role name]", is editable and is cut to 50 characters (REQ-031-057, REQ-031-129)
- **Delete**: Removes a custom role; blocked while any admin user (including an "Invited" account) or any pending role change holds it (REQ-031-129)
- **Create New Role**: Creates custom admin role with specific permissions (REQ-031-058)

**Business Rules**:

- Super Admin role permissions cannot be edited (locked, full access) (REQ-031-051)
- System roles (Super Admin, Aftercare Coordinator, Billing Admin, Support Staff) cannot be deleted; all of them except Super Admin can be edited (REQ-031-056)
- Custom roles can be created, edited, and deleted (only while no admin user, including an "Invited" account, and no pending role change holds the role) (REQ-031-057, REQ-031-129)
- Permission changes take effect on the next API call after propagation (≤ 5 seconds) for all users with that role

---

#### Tab 2: Admin Users

**Purpose**: Manage admin team members - invite, assign roles, suspend, reactivate, delete, view activity

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---------------|
| Search Bar | text input | No | Search users by name or email | Real-time filtering | no graph field (control) |
| Filter: Role | dropdown | No | Filter users by assigned role | All Roles, then every admin role including custom roles (predefined: Super Admin, Aftercare Coordinator, Billing Admin, Support Staff) | ENT-admin-user-account.assigned_role_id |
| Filter: Status | dropdown | No | Filter by user status | All, Active, Suspended, Invited, Deleted; a Deleted account is hidden unless "Deleted" is chosen (REQ-031-126) | ENT-admin-user-account.status, ENT-admin-user-account.invitation_status |
| User Name | Display (text) | N/A | Full name of admin user | Display only | ENT-admin-user-account.name |
| Email | Display (email) | N/A | Admin user's email address | Display only | ENT-admin-user-account.email |
| Role | Display (badge) | N/A | Assigned role | Color-coded by role | ENT-admin-user-account.assigned_role_id |
| Role Effective From | Display (datetime) | N/A | When the assigned role becomes active | Display only | ENT-admin-user-account.role_effective_from |
| Last Login | datetime | N/A | Timestamp of most recent login | Relative format (e.g., "2 hours ago") | ENT-admin-user-account.last_login_at |
| Status | badge | N/A | Active, Suspended, Invited or Deleted | Color-coded | ENT-admin-user-account.status |
| Actions | button group | N/A | Change Role (not on an Invited account), Suspend (Active accounts only), Reactivate (Suspended accounts only), Delete (Suspended accounts only), View Audit | Dropdown menu; a Super Admin row shows only View Audit; a Deleted account shows only View Audit; an Invited account is removed only with Cancel (REQ-031-126) | no graph field (control) |

**Actions**:

- **Invite Team Member**: Opens invitation form (Screen 2)
- **Change Role**: Opens role assignment modal (REQ-031-082); not offered on an Invited account (cancel and re-invite instead) (REQ-031-126)
- **Suspend**: Offered on Active accounts only; asks for confirmation and a required reason, ends the user's sessions and emails the user (not available for Super Admin accounts) (REQ-031-053, REQ-031-126)
- **Reactivate**: Offered on Suspended accounts only; returns the user to Active and emails the user (REQ-031-126)
- **Delete**: Offered to a Super Admin on a suspended non-Super Admin account only; anonymises the account under REQ-031-022 and sets its status to Deleted, after which the account cannot be reactivated (REQ-031-126)
- **View Audit**: Opens user detail page with audit trail (Screen 5)

**Business Rules**:

- A Super Admin account cannot be suspended by any other user, and cannot be removed, demoted or deactivated by anyone inside the product, including its holder; Tab 2 shows no Change Role, Suspend or Delete action on a Super Admin row, and if ever needed this is done outside the product (system protection) (REQ-031-009, REQ-031-054)
- Suspended users cannot log in but accounts remain in system (soft suspension) (REQ-031-053)
- Search filters users in real-time without page reload (REQ-022-115)
- Pagination: Display 25 users per page with "Load More" option (REQ-031-098)
- Sort columns: Name (A-Z), Last Login (most recent first), Role (alphabetical) (REQ-031-098)

**Notes**:

- Display warning banner while only one Active Super Admin account exists (Invited, Suspended and Deleted accounts do not count): "Warning: Only one Super Admin account. Consider adding backup admin. Refunds that need approval are blocked until a second admin holds Issue Refunds." (REQ-031-085)
- Show notification dot on Pending Invitations sub-tab if invitations are about to expire (< 24 hours) (REQ-031-042)
- Export user list to CSV with all columns and applied filters (REQ-031-098)
- Each user row shows whether the user has acknowledged the latest role change (Acknowledged, Awaiting acknowledgement, or Overdue once 24 hours have passed since the change took effect without an acknowledgement) (REQ-031-124; ENT-admin-user-account.role_change_acknowledged_at)
- A user with a pending role change shows the pending role and its Effective From beside the current role (REQ-031-125; ENT-admin-user-account.pending_role_id, ENT-admin-user-account.pending_role_effective_from)

**Pending Invitations sub-tab** (REQ-031-127):

- Lists every invitation not yet accepted, with columns Name, Email, Role, Invited by, Expires at and Status ("Invited", "Expired" or "Pending Send") (ENT-admin-user-account.invited_by, ENT-admin-user-account.invitation_expires_at, ENT-admin-user-account.invitation_status)
- Row actions: "Resend" (A1) and "Cancel" (A9); Cancel removes the "Invited" account, invalidates the invitation link and writes an audit entry; both work on an invitation for a Super Admin role until it is accepted (REQ-031-127)

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

- Display sync status indicator: "Last synced to Provider Platform: [timestamp]" (REQ-031-079; ENT-role-permission-definition.last_synced_at); a role whose sync failed shows "Sync failed" and "not yet applied" until a retry succeeds, and offers a "Retry sync" action to a Super Admin (REQ-031-130)
- Show impact summary before saving: "This change will affect [X] providers and [Y] team members"

---

### Screen 2: Invite Team Member Form

**Purpose**: Allows Super Admin to invite new admin team members with role assignment. Accessed from "Invite Team Member" button in Admin Users tab.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---------------|
| First Name | text | Yes | Admin user's first name | 2-50 characters; letters, spaces, hyphens only | ENT-admin-user-account.first_name |
| Last Name | text | Yes | Admin user's last name | 2-50 characters; letters, spaces, hyphens only | ENT-admin-user-account.last_name |
| Email Address | email input | Yes | New admin user's email | Valid email format; unique (not already in use); lowercase conversion | ENT-admin-user-account.email |
| Phone Number | tel input | No | Admin user's phone number | E.164 format validation; optional for now (MFA implementation planned for future) | ENT-admin-user-account.phone_number |
| Assigned Role | select (dropdown) | Yes | Role to assign to new user | Must select from the admin roles, including custom roles (predefined: Super Admin, Aftercare Coordinator, Billing Admin, Support Staff) | ENT-admin-user-account.assigned_role_id |
| Personal Message | textarea | No | Optional welcome message from Super Admin | Max 500 characters; included in invitation email | ENT-admin-user-account.personal_message |

**Actions**:

- **Send Invitation**: Generates invitation token and sends email
- **Cancel**: Closes form without sending invitation
- **Preview Email**: Opens preview modal showing how invitation email will appear

**Business Rules**:

- Email validation occurs on blur (field loses focus) for immediate feedback (REQ-031-034)
- System checks for duplicate email across all admin users (active, suspended, invited) and pending invitations (REQ-031-035)
- Role dropdown populated from the admin roles, including custom admin roles (REQ-031-036)
- Role dropdown displays: role name + brief description on hover (REQ-031-036)
- Form cannot be submitted until all required fields pass validation (REQ-031-033)
- Invitation token expires after the configured invitation expiry (7 days at launch, adjustable from 1 to 30 days in A-09 settings) (REQ-031-037)
- Personal message is optional but recommended for first-time team setup
- Phone number field is optional (MFA will be implemented in future enhancement) (REQ-031-048)

**Validation Messages**:

- Email already in use: "This email is already associated with an admin account. Please use a different email or check existing team members."
- Invalid email format: "Please enter a valid email address."
- Invalid phone format: "Please enter a valid phone number (e.g., +1234567890)." (REQ-031-121)
- Role not selected: "Please select a role for this team member."

**Notes**:

- Display role permission summary below role dropdown (expandable section showing what this role can access) (REQ-031-036)
- Show estimated invitation expiry time: "Invitation will expire in [N] days on [date] at [time]", where N is the configured invitation expiry (REQ-031-038)
- System auto-generates preview showing: invitee name, role, personal message (if provided), invitation link placeholder (REQ-031-038)
- After successful send, show confirmation: "Invitation sent to [email]. They have [N] days to accept.", where N is the configured invitation expiry (REQ-031-038)

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
| Accept Terms | checkbox | Yes | Confirm the Admin Terms of Service and privacy policy (acceptance belongs to this feature; the legal text is managed in FR-027, REQ-027-025) | Must be checked before submission | ENT-admin-user-account.terms_accepted_at |

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
- Expired or invalid tokens redirect to error page with "Request New Invitation" option, which notifies all Super Admins (A10) (REQ-031-040, REQ-031-128)
- Accepting the Admin Terms of Service is part of this feature; the legal text is edited under Edit Settings and viewed under View Settings in FR-027 (REQ-031-133)

**Validation Messages**:

- Password too weak: "Password must be at least 12 characters with uppercase, lowercase, number, and special character from !@#$%^&(),.?\":{}|<>." (REQ-031-045)
- Password mismatch: "Passwords do not match." (REQ-031-045)
- Terms not accepted: "You must accept the Admin Terms of Service to continue." (REQ-031-046)
- Invalid phone format: "Please enter a valid phone number (e.g., +1234567890)." (REQ-031-121)

**Success Flow**:

1. New admin user fills in all required fields
2. System validates all inputs
3. New admin user checks "Accept Terms" and clicks "Create Account"
4. System sets the account Active with the assigned role from the invitation
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
| Edit Patients | Modify patient information and run patient account actions: reset password, unlock account, lift suspension and take action on a flagged conversation (FR-016) | ☐ Write | ENT-permission |
| Delete Patients | Approve patient account deletion requests (FR-016) | ☐ Delete | ENT-permission |

**Category: Provider Management (A-02)**: (REQ-031-103)

| Permission | Description | Access Level | Graph field |
|------------|-------------|--------------|---------------|
| View Providers | View provider list and profiles | ☐ Read | ENT-permission |
| Edit Providers | Modify provider information | ☐ Write | ENT-permission |
| Onboard Providers | Create new provider accounts | ☐ Write | ENT-permission |
| Suspend Providers | Suspend/activate provider accounts, including Reject Request on an account-closure request | ☐ Delete | ENT-permission |

**Category: Aftercare Management (A-03)**: (REQ-031-104)

| Permission | Description | Access Level | Graph field |
|------------|-------------|--------------|---------------|
| View Aftercare Cases | View aftercare patient list | ☐ Read | ENT-permission |
| Manage Aftercare | Assign specialists, edit plans | ☐ Write | ENT-permission |
| Chat with Patients | Access aftercare chat | ☐ Write | ENT-permission |
| Schedule Consultations | Book video consultations | ☐ Write | ENT-permission |

When the Hairline team delivers a case, the Aftercare Coordinator uses these permissions on the FR-011 admin aftercare Screens 13 to 19, including Screen 14 Tab 4 (plan configuration, extension or change proposals and the urgent flag); no separate coordinator screens exist (REQ-011-004).

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
| Moderate Reviews | Decide takedown requests, remove a review, remove a provider response and resolve a flag | ☐ Write | ENT-permission |
| Add Reviews | Import authenticated reviews for providers | ☐ Write | ENT-permission |
| Manage Review Categories | Configure review categories and labels | ☐ Write | ENT-permission |
| Manage Review Settings | Configure photo guidelines, the removal reason catalog, flagging and the takedown decision deadline | ☐ Write | ENT-permission |
| Export Reviews | Export review data (audited) | ☐ Read | ENT-permission |

**Category: Billing & Financial (A-05)**: (REQ-031-107)

| Permission | Description | Access Level | Graph field |
|------------|-------------|--------------|---------------|
| View Transactions | View patient and provider transactions | ☐ Read | ENT-permission |
| Process Payouts | Run provider payout actions in FR-017: approve, unapprove, void, mark as paid, retry, release earnings, clear Manual Review Required, write off a clinic balance and override a payout status; each money-moving action asks for financial re-authentication (REQ-017-047) | ☐ Write | ENT-permission |
| Issue Refunds | Process patient refunds | ☐ Write (requires approval by another admin holding this permission, never the requester; the approval step and its 2-business-day escalation are defined in FR-007; while only one admin holds this permission, a refund that needs approval stays "awaiting approval" until a second holder exists) (REQ-031-069; REQ-007-015) | ENT-permission |
| View Financial Reports | Access revenue analytics | ☐ Read | ENT-permission |
| View Patient Billing | View patient invoices and payment status | ☐ Read | ENT-permission |
| Send Payment Reminders | Send payment reminders to patients (FR-007, FR-016); held by default by the same roles as Retry Charge | ☐ Write | ENT-permission |
| Retry Charge | Retry a failed patient payment charge (FR-007B) | ☐ Write | ENT-permission |
| Resolve Installments | Record a manual bank transfer for an unpaid installment and approve one entered by a colleague; the approver is never the requester (REQ-031-135) | ☐ Write | ENT-permission |
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
| Manage Affiliates | Add affiliates, edit profiles and commission rules, generate codes, suspend, reinstate, offboard and ban | ☐ Write (the Affiliate Program Settings panel and the commission ceiling override stay Super Admin only) (REQ-031-067) | ENT-permission |
| Process Affiliate Payouts | Process affiliate commission payments | ☐ Write | ENT-permission |
| View Affiliate Performance | View referral counts and conversions | ☐ Read | ENT-permission |

**Category: Analytics & Reporting (A-08)**: (REQ-031-110)

| Permission | Description | Access Level | Graph field |
|------------|-------------|--------------|---------------|
| View Analytics Dashboard | Access platform-wide analytics overview | ☐ Read | ENT-permission |
| View Provider Analytics | View provider performance metrics | ☐ Read | ENT-permission |
| View Financial Analytics | View revenue and conversion analytics | ☐ Read | ENT-permission |
| Export Reports | Export analytics reports (PDF/CSV); gates nothing yet, because FR-014 offers admins no analytics export (REQ-014-315) | ☐ Read | ENT-permission |
| View Treatment Outcomes | Access treatment outcomes analytics | ☐ Read | ENT-permission |

**Category: Communication & Support (A-10)**: (REQ-031-111)

| Permission | Description | Access Level | Graph field |
|------------|-------------|--------------|---------------|
| View Support Center | Access patient support cases | ☐ Read | ENT-permission |
| Respond to Support | Send messages to patients/providers | ☐ Write | ENT-permission |
| View Provider-Patient Messages | Read patient and provider conversations for monitoring | ☐ Read | ENT-permission |
| Flag Communications | Flag suspicious or policy-violating messages | ☐ Write | ENT-permission |
| Enable Emergency Intervention | Step into a conversation as an emergency intervention (FR-012) | ☐ Write | ENT-permission |
| Export Conversation Transcripts | Export chat transcripts for compliance (deferred to a future phase; conversation export is not available yet) | ☐ Read | ENT-permission |

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
| Manage App Data | Edit the FR-026 App Data lists (countries and calling codes, discovery questions, inquiry cancellation reasons, account deletion reasons, inquiry configuration and provider specialties), location presentation and starting prices | ☐ Write | ENT-permission |
| Manage Treatment Catalog | Create, edit and deactivate treatments, manage the treatment types list and the medication and post-op instruction templates; provider packages are view-only for admins | ☐ Write | ENT-permission |
| Manage Aftercare Templates | Create/edit aftercare milestone templates | ☐ Write | ENT-permission |
| Manage Notification Templates | Edit email templates (OTP, confirmations) | ☐ Write | ENT-permission |
| Configure Payment Settings | Manage Stripe accounts, commission rates, split pay (the permission FR-029 calls PaymentConfigAdmin) | ☐ Write | ENT-permission |
| Manage Help Centre | Create/edit Help Centre content for providers and patients | ☐ Write | ENT-permission |
| View Sensitive Settings | View the full value of sensitive settings (for example API keys) | ☐ Read | ENT-permission |
| Manage Authentication Policies | Edit authentication policy settings (for example lockout, the admin session limit and inactivity timeout, and the one-time-code (OTP) settings) | ☐ Write | ENT-permission |
| Manage Localization | Manage languages, translations and machine translation (FR-021) | ☐ Write (editing English source values, changing the default language, publishing, rollback, moving a language to Active, the free-text translation switch and budget, and machine translation credentials stay Super Admin only) (REQ-031-067) | ENT-permission |

**Super Admin-only actions** (REQ-031-067): the write permissions Edit Settings, Manage Users and Manage Roles; the Manage Localization actions listed in its row above; the Affiliate Program Settings panel and the commission ceiling override under Manage Affiliates; Login as Provider (REQ-015-069); and the Support Center settings (Screen 7 of FR-034) and the support audit export (REQ-034-094). Their cells stay disabled for every other role.

Legal content (terms of service, privacy policy, consent text) has no permission of its own: it is edited under Edit Settings and viewed under View Settings (REQ-027-011).

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
| View and Edit Billing Settings | View and edit the provider billing settings tab, including bank account details | ☐ Write (Owner only; viewing the tab needs the same permission) | ENT-permission |
| View Financial Reports | Access financial analytics | ☐ Read | ENT-permission |

**Category: Team Management (PR-01)**: (REQ-031-119)

| Permission | Description | Access Level | Graph field |
|------------|-------------|--------------|---------------|
| View Team Members | View team member list | ☐ Read | ENT-permission |
| Invite Team Members | Send team member invitations | ☐ Write (a Manager may invite Clinical Staff and Billing Staff only) | ENT-permission |
| Edit Team Member Roles | Change team member roles (non-Owner) | ☐ Write (Owner or Manager only; a Manager may set only Clinical Staff and Billing Staff and cannot create a Manager) | ENT-permission |
| Remove Team Members | Remove or suspend team members | ☐ Write (Owner: any non-Owner member; Manager: Clinical Staff and Billing Staff only) | ENT-permission |
| View Team Activity | Access team activity logs | ☐ Read | ENT-permission |

**Category: Provider Settings (PR-06)**: (REQ-031-120)

| Permission | Description | Access Level | Graph field |
|------------|-------------|--------------|---------------|
| View Profile | View provider profile information | ☐ Read | ENT-permission |
| Edit Profile | Update provider profile details | ☐ Write | ENT-permission |
| Manage Treatments | Set a treatment Offered or Not Offered and configure its pricing, including Quick Copy Pricing (FR-024) | ☐ Write | ENT-permission |
| Manage Packages | Create, edit, clone and deactivate packages and use quick price edit (FR-024) | ☐ Write | ENT-permission |
| Manage Promotions | Create and edit discount codes | ☐ Write | ENT-permission |
| View Settings | View provider settings | ☐ Read | ENT-permission |
| Edit Settings | Modify provider settings | ☐ Write (Owner only) | ENT-permission |
| Edit Notification Settings | Change the clinic's notification preferences | ☐ Write (default holders Owner and Manager) | ENT-permission |

**Modal Actions** (Single Role Mode):

- **Save Changes**: Saves permission changes and closes modal
- **Cancel**: Closes modal (shows confirmation dialog if unsaved changes exist)
- **Reset to Default**: Resets a predefined role to its default permissions (the default tables below); not offered on custom roles (REQ-031-076, REQ-031-134)
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

**Default permissions for Admin Roles**: Super Admin holds every admin permission; for every other predefined role a permission not listed in this table is off, and Reset to Default restores exactly these values (REQ-031-134).

| Permission | Category | Super Admin | Aftercare Coordinator | Billing Admin | Support Staff | Graph field |
|------------|----------|-------------|---------------------|---------------|---------------|---------------|
| View Dashboard | A-01 | ☑ | ☑ | ☑ | ☑ | ENT-permission, ENT-role-permission-definition |
| View Patient Overview | A-01 | ☑ | ☑ | ☑ | ☑ | ENT-permission, ENT-role-permission-definition |
| View Patients | A-01 | ☑ | ☑ | ☑ | ☑ | ENT-permission, ENT-role-permission-definition |
| Edit Patients | A-01 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| Delete Patients | A-01 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| View Inquiries Overview | A-01 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| Edit Quotes | A-01 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| View Reviews | A-01 | ☑ | ☑ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| Moderate Reviews | A-01 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| View Providers | A-02 | ☑ | ☑ | ☑ | ☑ | ENT-permission, ENT-role-permission-definition |
| Edit Providers | A-02 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| Onboard Providers | A-02 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| Suspend Providers | A-02 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| View Aftercare Cases | A-03 | ☑ | ☑ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| Manage Aftercare | A-03 | ☑ | ☑ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| Chat with Patients | A-03 | ☑ | ☑ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| Schedule Consultations | A-03 | ☑ | ☑ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| View Transactions | A-05 | ☑ | ☐ | ☑ | ☐ | ENT-permission, ENT-role-permission-definition |
| Process Payouts | A-05 | ☑ | ☐ | ☑ | ☐ | ENT-permission, ENT-role-permission-definition |
| Issue Refunds | A-05 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| Retry Charge | A-05 | ☑ | ☐ | ☑ | ☐ | ENT-permission, ENT-role-permission-definition |
| Send Payment Reminders | A-05 | ☑ | ☐ | ☑ | ☐ | ENT-permission, ENT-role-permission-definition |
| Resolve Installments | A-05 | ☑ | ☐ | ☑ | ☐ | ENT-permission, ENT-role-permission-definition |
| View Patient Billing | A-05 | ☑ | ☐ | ☑ | ☐ | ENT-permission, ENT-role-permission-definition |
| View Discounts | A-06 | ☑ | ☐ | ☑ | ☐ | ENT-permission, ENT-role-permission-definition |
| Create Discounts | A-06 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| View Affiliates | A-07 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| View Analytics Dashboard | A-08 | ☑ | ☑ | ☑ | ☐ | ENT-permission, ENT-role-permission-definition |
| View Support Center | A-10 | ☑ | ☑ | ☐ | ☑ | ENT-permission, ENT-role-permission-definition |
| Respond to Support | A-10 | ☑ | ☑ | ☐ | ☑ | ENT-permission, ENT-role-permission-definition |
| View Provider-Patient Messages | A-10 | ☑ | ☑ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| Flag Communications | A-10 | ☑ | ☑ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| Enable Emergency Intervention | A-10 | ☑ | ☑ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| View Settings | A-09 | ☑ | ☑ | ☑ | ☑ | ENT-permission, ENT-role-permission-definition |
| Edit Settings | A-09 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| Manage Users | A-09 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| Manage Roles | A-09 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |

**Default permissions for Provider Roles**: Owner holds every provider permission; for every other provider role a permission not listed in this table is off, and Reset to Default restores exactly these values (REQ-031-134).

| Permission | Category | Owner | Manager | Clinical Staff | Billing Staff | Graph field |
|------------|----------|-------|---------|----------------|---------------|---------------|
| View Inquiries | PR-02 | ☑ | ☑ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| Respond to Inquiries | PR-02 | ☑ | ☑ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| View Appointments | PR-02 | ☑ | ☑ | ☑ | ☐ | ENT-permission, ENT-role-permission-definition |
| Schedule Appointments | PR-02 | ☑ | ☑ | ☑ | ☐ | ENT-permission, ENT-role-permission-definition |
| View In-Progress Cases | PR-03 | ☑ | ☑ | ☑ | ☐ | ENT-permission, ENT-role-permission-definition |
| Document Treatment | PR-03 | ☑ | ☐ | ☑ | ☐ | ENT-permission, ENT-role-permission-definition |
| View Financial Dashboard | PR-05 | ☑ | ☑ | ☐ | ☑ | ENT-permission, ENT-role-permission-definition |
| View Payouts | PR-05 | ☑ | ☑ | ☐ | ☑ | ENT-permission, ENT-role-permission-definition |
| View and Edit Billing Settings | PR-05 | ☑ | ☐ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| View Team Members | PR-01 | ☑ | ☑ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| Invite Team Members | PR-01 | ☑ | ☑ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| View Profile | PR-06 | ☑ | ☑ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| Edit Profile | PR-06 | ☑ | ☑ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |
| Edit Notification Settings | PR-06 | ☑ | ☑ | ☐ | ☐ | ENT-permission, ENT-role-permission-definition |

**Matrix View Features**:

- **Column Headers**: Role names with user count badges (e.g., "Super Admin (3 users)")
- **Row Headers**: Permission name + category/module code
- **Cell Interaction**: Click checkbox to toggle permission for that role
- **Bulk Actions**:
  - "Select All" checkbox in column header to grant all permissions to a role
  - "Select All" checkbox in row header to grant permission to all roles
  - "Select Category" to grant all permissions in a category to selected roles
  - Every bulk action skips the Super Admin-only permissions, whose cells stay disabled for every role other than Super Admin (REQ-031-067, REQ-031-077)
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
- **Reset Role to Default**: Resets selected predefined role(s) to their default permissions (shows confirmation dialog if unsaved changes exist) (REQ-031-076)
- **Export Matrix**: Export matrix to CSV/Excel for documentation (REQ-031-077)
- **Switch to Single Role View**: Switches to single role edit mode for focused editing (shows confirmation dialog if unsaved changes exist)
- **Close (X button)**: Closes modal (shows confirmation dialog if unsaved changes exist)

**Business Rules** (Matrix Mode):

- All business rules from Single Role Mode apply
- Changes can be made to multiple roles simultaneously (REQ-031-077)
- System shows confirmation dialog listing all affected roles and user counts before saving (REQ-031-074)
- Locked roles (Super Admin, Owner) remain locked in matrix view
- Permission dependencies apply across all roles (checking any write permission that has a matching View permission, such as Edit Patients, Manage Aftercare or Moderate Reviews, auto-checks that View for that role) (REQ-031-070)

**Business Rules** (Both Modes):

- Permissions organized by module code (A-01, A-02 for admin; PR-01, PR-02, etc. for provider) for traceability (REQ-031-072)
- "Select All" checkbox available for each category; it skips the Super Admin-only permissions (REQ-031-072, REQ-031-077)
- Permission dependencies highlighted (e.g., "Edit Patients" requires "View Patients")
- System prevents saving role with zero permissions (REQ-031-071)
- **Admin Role Protection**: Super Admin permissions cannot be removed from Super Admin role (system protection, checkboxes disabled)
- **Provider Role Protection**: Owner role must always have full access to all provider features (cannot be restricted, checkboxes disabled for critical permissions)
- Permission changes take effect for all users with that role on the next API call after propagation (≤ 5 seconds)
- **Provider Permission Propagation**: Changes to provider role permissions automatically sync to Provider Platform (FR-009) within 5 seconds
- Role edits logged in audit trail with before/after permission comparison (REQ-031-081)
- **UI Enforcement**: Admin and Provider platforms hide UI elements (menu items, buttons, tabs, sections) for features users cannot access based on their role permissions (REQ-031-088)

**Validation**:

- Display warning when a permission matrix is saved with a newly granted sensitive permission, and again when a role holding one is assigned to a user (B6); sensitive permissions are all financial write permissions (refunds, payouts, payment settings), Manage Roles, Manage Users and Delete Patients (REQ-031-073)
- Show confirmation dialog before saving: "This will affect [X] users. Continue?" (REQ-031-074)
- For provider roles: "This will affect [Y] team members across [Z] provider organizations. Continue?" (REQ-031-074)
- Highlight permission dependencies (selecting a write permission automatically selects its matching View permission) (REQ-031-070)

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

**Purpose**: Displays comprehensive information about specific admin user including activity history and permission changes. The trail on this screen shows access-control events only; actions on patients, reviews and other records stay in the logs of their own features (REQ-031-132)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---------------|
| User Profile | section (read-only) | N/A | Name, email, role, status, created date | - | ENT-admin-user-account.name, ENT-admin-user-account.email, ENT-admin-user-account.assigned_role_id, ENT-admin-user-account.status, ENT-admin-user-account.created_at |
| Current Role | badge | N/A | Currently assigned role with color coding | - | ENT-admin-user-account.assigned_role_id |
| Role Effective From | datetime | N/A | When the current role became (or will become) active | - | ENT-admin-user-account.role_effective_from |
| Role Change Acknowledged | datetime / badge | N/A | When the user acknowledged the latest role change, or Awaiting acknowledgement, or Overdue once 24 hours have passed since the change took effect | Display only | ENT-admin-user-account.role_change_acknowledged_at |
| Last Login | datetime | N/A | Most recent successful login | - | ENT-admin-user-account.last_login_at |
| Login Count | number | N/A | Total number of logins since account creation | - | ENT-admin-user-account.login_count |
| Account Status | badge | N/A | Active, Suspended, Invited or Deleted | - | ENT-admin-user-account.status |

**Audit Trail Table**:

| Column | Type | Description | Format | Graph field |
|--------|------|-------------|--------|---------------|
| Timestamp | datetime | When action occurred | "2025-11-14 14:32:15 UTC" | ENT-admin-audit-trail-entry.timestamp |
| Action Type | text | Type of action: Login, Role Change, Permission Grant, Access Denied, Password Reset, User Suspended, User Reactivated, User Deleted, Account Created, Role Created, Role Deleted, Role Permissions Edited, Invitation Sent, Invitation Resent, Invitation Cancelled, Invitation Delivery Failed, Sensitive Access; the action-type filter lists all of them | Badge with color | ENT-admin-audit-trail-entry.action_type |
| Details | text | Description of action | "Role changed from 'Support Staff' to 'Aftercare Coordinator' by <admin@hairline.com>" | ENT-admin-audit-trail-entry.action_details |
| IP Address | text | IP address of action (security audit) | "192.168.1.1" | ENT-admin-audit-trail-entry.ip_address |
| Outcome | badge | Success/Failed/Denied | Color-coded | ENT-admin-audit-trail-entry.outcome |

**Business Rules**:

- Audit trail shows the last 30 days by default, 100 rows at a time with a "Load More" option; the date range filter reaches further back (REQ-031-094)
- Audit trail searchable by action type, date range, outcome (REQ-031-094; REQ-022-117)
- Audit entries immutable (cannot be edited or deleted)
- Login failures logged with reason (invalid password, account suspended, etc.) (REQ-031-094)
- Access denial attempts logged with requested feature/endpoint (REQ-031-089)
- Audit trail exportable to CSV for compliance reporting (REQ-031-095)
- Sensitive actions (role changes, permission grants) highlighted in audit trail (REQ-031-094)
- This screen shows access-control events only: sign-ins, access denials, invitations, role and permission changes, suspensions, reactivations and deletions. Actions on patient accounts (the FR-016 patient action log), reviews and other records stay in the logs of their own features; patient accounts and admin accounts remain separate records (REQ-031-132)

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
- **Rule 4**: No Super Admin account can be removed, demoted, suspended or deactivated inside the product, so a Super Admin always exists (system protection against lockout); a warning banner shows while only one Active Super Admin account exists (REQ-031-009; REQ-031-085)
- **Rule 5**: All administrative actions (role changes, permission grants, user suspensions) MUST be logged in audit trail (REQ-031-008; REQ-031-083)
- **Rule 6**: Invitation tokens expire after 7 days (configurable via A-09 settings; range 1-30 days) (REQ-031-037)
- **Rule 7**: Suspended admin users cannot log in but accounts remain in system (soft suspension; a Super Admin may delete a suspended non-Super Admin account, anonymised under REQ-031-022, which then shows status Deleted and cannot be reactivated); Super Admin accounts are never suspended inside the product (REQ-031-053; REQ-031-009; REQ-031-126)
- **Rule 8**: A role change MUST be stored as a pending role with an **Effective From** timestamp: the current role applies until Effective From, a second change made before then replaces the pending one, and Effective From cannot be before now; enforcement MUST respect that date/time on authorization checks (REQ-031-011; REQ-031-082; REQ-031-125)
- **Rule 9**: Role names for system-defined roles (admin + provider) MUST be immutable (not editable/renamable); only custom admin roles can be renamed. (REQ-031-055)
- **Rule 10**: After an admin user's role changes, the user MUST acknowledge the change within 24 hours of it taking effect; the acknowledgement time is stored on the account and shown to Super Admins, who see an "Overdue" flag when it is late; nothing is blocked and no reminder is sent (REQ-031-124)
- Every existing role can be assigned to new or existing users; roles have no active or inactive status and cannot be deactivated (REQ-031-036)
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
- Assign/change roles for any admin user except Super Admin accounts (REQ-031-054)
- Suspend (Active accounts), reactivate (Suspended accounts) and delete (Suspended, non-Super Admin accounts only) admin accounts (REQ-031-126)
- Configure invitation token expiry time (default 7 days, range 1-30 days) (REQ-031-037)
- Create permission matrix for custom admin roles
- Re-send invitation emails for pending accounts (REQ-031-042) and cancel a pending invitation (REQ-031-127)

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
- Maximum failed login attempts before lockout (configurable in A-09: Authentication Settings; default 5 failed attempts with a 15-minute lockout, the same setting as FR-001; the admin login rate limit (REQ-031-100) is a separate control and stays, and whichever trips first applies, REQ-026-116) (REQ-031-099)
- Session timeout duration: the admin inactivity timeout set in A-09 (FR-026; whole minutes from 5 to 240, default 30) (REQ-031-099)
- Number of concurrent sessions per admin user (default: 3, range: 1-5); at the limit, a new sign-in ends the oldest session; a change to the limit or to the inactivity timeout applies from each open session's next request, and sessions above a lowered limit end oldest first (REQ-031-099, REQ-026-116)
- Repeated access denial alert: the count (default 5 refusals for one admin) and the time window (default 10 minutes) are each configurable in A-09 (REQ-031-090)

---

## Dependencies

- **FR-009**: Provider Team & Role Management (consumes and enforces the provider role permission matrices configured in FR-031)
- **FR-015**: Provider Management (provider organizations and oversight of provider team members)
- **FR-020**: Notifications & Alerts (transactional email/in-app alerts for admin invitations, role changes, suspensions, and audit events; module S-03 Notification Service)
- **FR-007**: Payment processing (approval step and 2-business-day escalation for Issue Refunds)
- **FR-007B**: Split Payment / Installment Plans (consumes the Retry Charge and Resolve Installments permissions)
- **FR-027**: Legal content settings (the Admin Terms of Service text; acceptance at account set-up belongs to FR-031)
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

1. **Given** Super Admin is logged into admin platform, **When** Super Admin invites new user with email "<nurse@hairline.com>" and role "Aftercare Coordinator", **Then** invitation email sent within 1 minute and new account created with status "Invited"

2. **Given** new aftercare nurse receives invitation email, **When** nurse clicks activation link and sets password, **Then** account activated and nurse can log in with aftercare dashboard access

3. **Given** aftercare nurse is logged in, **When** nurse attempts to access Billing section, **Then** access denied with message "You do not have permission to access this feature" and attempt logged in audit trail

---

### User Story 2 - Create Custom Role for Analytics Staff (Priority: P2)

As a Super Admin, I need to create a custom "Analytics Viewer" role with read-only access to reports and dashboards, so analytics staff can view data without modifying it.

**Why this priority**: Enables specialized roles for growing team; supports principle of least privilege

**Independent Test**: Can be tested by creating custom role with read-only permissions, assigning to test user, and verifying read access without write capabilities

**Acceptance Scenarios**:

1. **Given** Super Admin navigates to Settings > User Roles & Permissions, **When** Super Admin creates new role "Analytics Viewer" with permissions: View Financial Reports (read), View Patients (read), View Providers (read), **Then** role saved and available in role dropdown for user assignment

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
  - **Handling**: Database-level locking prevents concurrent updates; second Super Admin receives error: "Role change failed - this user's role was just updated by another admin. Refresh and try again." Audit trail logs both attempts with outcomes (success, failed) (REQ-031-086)

- **Edge Case 3**: What occurs if invitation email delivery fails (email service down)?
  - **Handling**: System retries the invitation email according to the FR-030 notification retry rule; from the first failed delivery the invitation shows "Pending Send" and the Super Admin is warned and can resend it; if the email still cannot be sent 24 hours after the invitation was created, the invitation becomes "Expired"; Super Admin can re-send the invitation once the email service is restored (REQ-031-043; REQ-030-008)

- **Edge Case 4**: How to manage admin user who forgets password before activating account?
  - **Handling**: Accounts still in the "Invited" status do not support password reset (no password set yet); user must request new invitation from Super Admin; original invitation token invalidated to prevent duplicate accounts (REQ-031-093)

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
- **REQ-031-009**: System MUST NOT allow a Super Admin account to be suspended by another user, or removed, demoted or self-deactivated inside the product (system protection; if ever needed, this is done outside the product), and MUST show a message saying so when it is attempted; an invitation for a Super Admin role is not yet an account and can be cancelled or resent until it is accepted
- **REQ-031-010**: System MUST send email notifications for: new invitations, role changes, password resets, repeated access denials
- **REQ-031-011**: System MUST support role assignment changes with **Effective From** date/time tracking (stored and auditable); the current role stays in force until Effective From
- **REQ-031-124**: System MUST ask an admin user to acknowledge a role change within 24 hours of it taking effect; the acknowledgement time is stored on the account and shown to Super Admins, who see an "Overdue" flag when it is late; nothing is blocked and no reminder is sent
- **REQ-031-125**: System MUST store a role change as a pending role with its Effective From (never earlier than now); the current role applies until Effective From, and a second change made before then replaces the pending one
- **REQ-031-126**: System MUST let a Super Admin suspend an Active account (with a required reason), reactivate a Suspended account back to Active, and delete a Suspended non-Super Admin account; deletion anonymises the account under REQ-031-022 and sets its status to Deleted, after which it is hidden from the Admin Users list unless the Status filter "Deleted" is chosen, offers only View Audit, cannot be reactivated and is not counted as a role holder (REQ-031-129) or as a Super Admin (REQ-031-085); an Invited account is removed only with Cancel (REQ-031-127) and has no Change Role action; a Super Admin account can never be suspended, demoted or deleted inside the product
- **REQ-031-127**: System MUST list pending invitations (Invited, Expired, Pending Send) in a Pending Invitations sub-tab where a Super Admin can re-send or cancel them, including an invitation for a Super Admin role until it is accepted; cancelling removes the invitation and its account and the link stops working
- **REQ-031-128**: System MUST notify all Super Admins when an invitee uses "Request New Invitation" on an expired or invalid link
- **REQ-031-129**: System MUST let a Super Admin delete a custom admin role only while no admin user (including an "Invited" account, but not a Deleted one) and no pending role change holds it, and MUST name a cloned role "Copy of [role name]" cut to 50 characters; roles have no active or inactive status
- **REQ-031-130**: System MUST, when a provider role permission change fails to reach the Provider Platform after 3 automatic tries, show the role as "Sync failed" and "not yet applied", alert the Super Admin in-app, and keep showing that state until a retry succeeds; after the 3 automatic tries fail the role stays "Sync failed / not yet applied", a Super Admin can press "Retry sync" on the Provider Roles tab (saving the matrix again also re-sends it), and every attempt is logged in the audit trail
- **REQ-031-131**: System MUST let a Super Admin edit the permissions of an admin role, with the sensitive-permission warning when needed, and apply the new permissions to everyone holding the role from their next request
- **REQ-031-132**: System MUST limit the audit trail on the admin user detail screen to access-control events; actions on other records stay in the logs of their own features
- **REQ-031-133**: System MUST ask a new admin to accept the Admin Terms of Service when setting up the account; the legal text itself is edited in FR-027
- **REQ-031-134**: System MUST define each predefined role's default permissions as a full table (a permission not listed is off) and restore exactly that table on Reset to Default
- **REQ-031-135**: System MUST offer the admin write permission Resolve Installments (record a manual bank transfer for an unpaid installment and approve one entered by a colleague; the approver is never the requester), held by default by Super Admin and Billing Admin

### Data Requirements

- **REQ-031-012**: System MUST maintain admin user accounts with: email, name, password hash, assigned role, role effective date/time, role change acknowledgement time, pending role and its effective date/time, status (active/invited/suspended/deleted), creation date, last login timestamp
- **REQ-031-013**: System MUST maintain role definitions with: guard-scoped role name, description, assigned permissions (as permission matrix), and system/custom status (custom roles exist for admin roles only)
- **REQ-031-014**: System MUST maintain audit trail entries with: timestamp, user ID, action type (the access-control events listed on the user detail screen), action details, IP address, outcome (success/failed/denied)
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
| 2026-11-24 | 1.5 | Logic review pass 1 applied. Invitation creates the account as Invited (steps and labels aligned); pending role with Effective From; Super Admin accounts cannot be demoted, suspended or deleted in the product; suspend, reactivate and delete flows; sensitive permission list widened; provider team-removal and refund-approval rules corrected; audit trail limited to access-control events with a 30-day default; new flows for editing admin role permissions, cancelling invitations, requesting a new invitation, deleting and cloning roles and sync failure; permission rows added or reworded for messaging, localization, reviews, treatments and packages, patients, retry charge and affiliates; default tables made full and renamed; settings ownership pointers to FR-021, FR-027 and FR-034. See the update log of the same date. | Documentation |
| 2026-11-24 | 1.6 | Logic review pass 2 applied. Sensitive-permission warning added to the invitation and role-change flows; the role-change acknowledgement is shown to the affected admin on the admin dashboard; new Deleted account status and the status each account action is offered on; Super Admin invitations can be cancelled or resent until accepted and only Active Super Admins count for the single-Super-Admin banner; Pending Send starts at the first failed delivery; provider role sync can be retried by a Super Admin; new permissions Resolve Installments (admin), Edit Notification Settings (provider) and View and Edit Billing Settings (renamed from Manage Bank Details); provider default table gains View Profile and Edit Profile for Manager; refunds raised by the only holder of Issue Refunds wait for a second holder; small wording fixes. See the update log of the same date. | Documentation |
| 2026-11-25 | 1.7 | Cross-FR alignment. Permission descriptions now name what neighbouring modules gate on them: Edit Patients covers password reset, unlock, lifting a suspension and action on a flagged conversation (FR-016); Process Payouts covers the FR-017 payout actions under financial re-authentication; Manage App Data names the FR-026 App Data lists; Manage Treatment Catalog adds the medication and post-op instruction templates; Manage Authentication Policies names the admin session settings; Export Reports noted as gating nothing in FR-014. Send Payment Reminders added to the Billing Admin defaults, mirroring Retry Charge. Aftercare Coordinator screens named. Session limit and timeout changes apply from each open session's next request. | Documentation |

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
**Last Updated**: 2026-11-25 (cross-FR alignment; prior approval dated 2026-01-04)
