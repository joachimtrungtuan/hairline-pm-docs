# Product Requirements Document: Admin Access Control & Permissions

**Module**: A-09: System Settings & Configuration
**Feature Branch**: `fr031-admin-access-control`
**Created**: 2025-11-14
**Status**: ✅ Verified & Approved
**Source**: FR-031 from system-prd.md

---

## Executive Summary

The Admin Access Control & Permissions module is a **Super Admin-only configuration tool** that serves as the **single source of truth** for all role definitions and permission matrices across the entire Hairline platform. This module enables Super Admins to:

1. **Define Admin Platform Role Permissions**: Configure what permissions each admin role has (Super Admin, Aftercare Specialist, Billing Staff, Support Staff)
2. **Define Provider Platform Role Permissions**: Configure what permissions each provider role has (Owner, Manager, Clinical Staff, Billing Staff)
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

- **Permission enforcement only**: Provider Platform consumes and enforces RBAC rules defined in Admin Platform (FR-031)
- **No configuration UI**: Provider users do not see or access role permission configuration; they only experience the enforced permissions
- **Read-only consumption**: Provider Platform reads permission matrices from FR-031 and applies them when provider team members access features
- **Note**: Provider team member invitation and role assignment is handled in PR-01/FR-009, but the permission definitions for those roles come from FR-031

**Admin Platform (A-09)** (Super Admin Only):

- **Admin role permission configuration**: Super Admins define what permissions each admin role has (Super Admin, Aftercare Specialist, Billing Staff, Support Staff)
- **Provider role permission configuration**: Super Admins define what permissions each provider role has (Owner, Manager, Clinical Staff, Billing Staff)
- **Admin team member management**: Super Admins invite admin users and assign them predefined roles
- Permission matrix definition and editing for both admin and provider roles
- Centralized RBAC configuration interface accessible only to Super Admins
- Audit trail of all permission changes and role assignments
- Access control: Only Super Admins can access this module; regular admin users and providers cannot view or modify role permissions

**Shared Services (S-03)**:

- Invitation and role/permission change notifications delivered via S-03
- Permission checks executed within admin platform backend

### Communication Structure

**In Scope**:

- Email notifications for admin team member invitations
- Email notifications for role assignment changes
- Email notifications for permission changes (to affected admin users)
- System notifications for access denial attempts

**Out of Scope**:

- SMS notifications (handled by S-03: Notification Service if needed; **no SMS admin notifications are available in MVP and SMS will only be enabled if/when S-03 adds SMS delivery in a later phase**)
- Real-time permission updates via WebSocket (V2 enhancement)
- External identity provider integration (OAuth, SAML - V2 enhancement)

### Entry Points

- **Super Admin Access Only**: Super Admins access this module via "Settings > User Roles & Permissions" in the Admin Platform
- **Access Restriction**: This module is hidden from non-Super Admin users; only Super Admins can view and access it
- **Initial Setup**: First Super Admin account created during platform deployment/installation
- **Configuration Workflow**:
  - Super Admins configure role permissions for admin and provider roles
  - Super Admins invite admin team members and assign them roles
  - Provider owners invite their team members (FR-009) but cannot configure role permissions
- **Permission Enforcement**: Configured permissions enforced across all platforms on every API request
- **Audit Trail Access**: All Super Admin actions logged automatically and viewable in audit trail interface

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
7. Super Admin enters admin user details and selects role (Super Admin, Aftercare Specialist, Billing Staff, Support Staff)
8. System validates email format and checks for duplicate email within admin team
9. Super Admin reviews invitation details and clicks "Send Invitation"
10. System generates secure invitation token (expires in 7 days)
11. System sends email to invitee with invitation link, Hairline Admin Platform branding, and role being offered
12. System creates pending invitation record with status "Invited"
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
  7. System displays permission comparison (current vs new role permissions) and effective date/time
  8. Super Admin confirms role change
  9. System validates Effective From is not in the past
  10. System updates user's role assignment with Effective From timestamp
  11. System logs role change in audit trail (who changed, old role, new role, effective_from, timestamp)
  12. System sends email notification to affected user about role change (includes effective date/time)
  13. System enforces new role permissions on the first API call at or after Effective From
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

- **Trigger**: Super Admin needs to modify permissions for a provider role (Owner, Manager, Clinical Staff, Billing Staff)
- **Steps**:
  1. Super Admin navigates to Settings > User Roles & Permissions > Provider Roles tab
  2. System displays list of provider roles (Owner, Manager, Clinical Staff, Billing Staff) with user counts
  3. Super Admin clicks "Edit Permissions" on target provider role (e.g., "Clinical Staff")
  4. System opens Permission Matrix Modal (Screen 4) with provider permissions
  5. System displays current permissions checked and shows user count: "Currently assigned to [X] users across [Y] providers"
  6. Super Admin modifies permissions (e.g., grants "View Financial Reports" to Clinical Staff)
  7. System displays permission comparison showing additions/removals
  8. System shows warning if removing critical permissions (e.g., "This will remove access to [feature] for all Clinical Staff members")
  9. System displays count of affected provider team members across all providers
  10. Super Admin reviews changes and clicks "Save Changes"
  11. System validates permission changes (e.g., Owner role must retain full access)
  12. System saves updated permission matrix
  13. System logs permission change in audit trail with before/after comparison
  14. System syncs permission changes to Provider Platform (FR-009) within 5 seconds
  15. System displays confirmation: "Provider role permissions updated. Changes will take effect for all [Role] members on next page load."
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
  2. System displays error: "This email is already part of the admin team"
  3. System suggests: "View team member" or "Resend invitation" if pending
  4. Super Admin either cancels or takes suggested action
- **Outcome**: Duplicate prevented, existing record maintained

**B3: Invitation Link Already Used**:

- **Trigger**: Admin user clicks invitation link that was already accepted
- **Steps**:
  1. System detects invitation status is "Accepted"
  2. System displays message: "This invitation has already been used. Please log in with your existing credentials."
  3. System provides login link
- **Outcome**: Prevents duplicate account creation

**B4: Network Error During Invitation Send**:

- **Trigger**: Email service fails to send invitation
- **Steps**:
  1. System attempts to send invitation email
  2. Email service returns error
  3. System logs error and retries up to 3 times with exponential backoff
  4. If all retries fail, system marks invitation as "Pending Send"
  5. System displays warning to Super Admin: "Invitation created but email failed. We'll retry automatically."
  6. Background job retries sending every 10 minutes for 24 hours
  7. If still failing after 24 hours, system alerts admin team
- **Outcome**: Invitation record created, email eventually delivered or admin intervenes

**B5: Unauthorized Access Attempt**:

- **Trigger**: Admin user attempts to access feature not permitted by their role
- **Steps**:
  1. **On page load**: System checks user's permissions and hides all UI elements (menu items, buttons, tabs) for features user cannot access
  2. **If feature cannot be hidden** (e.g., shared page with mixed permissions or direct URL access): Admin user navigates to restricted feature
  3. System checks user's permissions against required permission
  4. System denies access and displays message: "Access Denied: You do not have permission to access this feature. Contact your administrator if you need access."
  5. System logs access denial attempt in audit trail (user, feature, timestamp, IP address)
  6. System sends alert to Super Admin if multiple failed attempts detected (potential security issue)
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

**Purpose**: Define and configure permission matrices for admin platform roles (Super Admin, Aftercare Specialist, Billing Staff, Support Staff)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Role List | table | N/A | List of all admin roles | Display: Role Name, Description, # Users, Actions |
| Role Name | text | N/A | Name of role | Read-only for system roles |
| Users Count | number | N/A | Number of admin users with this role | Display only, clickable to filter Tab 2 |
| Actions | button group | N/A | Edit Permissions, View Users, Clone Role | Disabled for Super Admin role |

**Actions**:

- **Edit Permissions**: Opens permission matrix modal/panel for selected role
- **View Users**: Switches to Tab 2 filtered by this role
- **Clone Role**: Creates new custom role based on existing role
- **Create New Role**: Creates custom admin role with specific permissions

**Business Rules**:

- Super Admin role permissions cannot be edited (locked, full access)
- System roles (Super Admin, Aftercare Specialist, Billing Staff, Support Staff) can be edited but not deleted
- Custom roles can be created, edited, and deleted (if no users assigned)
- Permission changes take effect on the next API call after propagation (≤ 5 seconds) for all users with that role

---

#### Tab 2: Admin Users

**Purpose**: Manage admin team members - invite, assign roles, suspend, view activity

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Search Bar | text input | No | Search users by name or email | Real-time filtering |
| Filter: Role | dropdown | No | Filter users by assigned role | All Roles, Super Admin, Aftercare Specialist, Billing Staff, Support Staff |
| Filter: Status | dropdown | No | Filter by user status | All, Active, Suspended, Pending Invitation |
| User Name | Display (text) | N/A | Full name of admin user | Display only |
| Email | Display (email) | N/A | Admin user's email address | Display only |
| Role | Display (badge) | N/A | Assigned role | Color-coded by role |
| Role Effective From | Display (datetime) | N/A | When the assigned role becomes active | Display only |
| Last Login | datetime | N/A | Timestamp of most recent login | Relative format (e.g., "2 hours ago") |
| Status | badge | N/A | Active/Suspended/Pending | Color-coded |
| Actions | button group | N/A | Change Role, Suspend, View Audit | Dropdown menu |

**Actions**:

- **Invite Team Member**: Opens invitation form (Screen 2)
- **Change Role**: Opens role assignment modal
- **Suspend/Activate**: Suspend or reactivate admin user
- **View Audit**: Opens user detail page with audit trail (Screen 5)

**Business Rules**:

- Super Admin accounts cannot be suspended by other users (system protection)
- At least one active Super Admin must exist at all times (prevent lockout)
- Suspended users cannot log in but accounts remain in system (soft suspension)
- Search filters users in real-time without page reload
- Pagination: Display 25 users per page with "Load More" option
- Sort columns: Name (A-Z), Last Login (most recent first), Role (alphabetical)

**Notes**:

- Display warning banner if only one Super Admin exists: "Warning: Only one Super Admin account. Consider adding backup admin."
- Show notification dot on Pending Invitations sub-tab if invitations are about to expire (< 24 hours)
- Export user list to CSV with all columns and applied filters

---

#### Tab 3: Provider Roles

**Purpose**: Define and configure permission matrices for provider platform roles (Owner, Manager, Clinical Staff, Billing Staff)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Role List | table | N/A | List of provider roles | Display: Role Name, Description, Total Users Across All Providers, Actions |
| Role Name | text | N/A | Name of provider role | Read-only (Owner, Manager, Clinical Staff, Billing Staff) |
| Total Users | number | N/A | Count of provider team members with this role across all providers | Display only, informational |
| Last Modified | datetime | N/A | When permissions were last updated | Display only |
| Actions | button group | N/A | Edit Permissions, View Users | Owner role has lock icon |

**Actions**:

- **Edit Permissions**: Opens permission matrix modal/panel for selected role (Provider Platform permissions)
- **View Users**: Links to FR-015 (Provider Management) to view providers and their team members with this role

**Business Rules**:

- Owner role must always have full access to all provider features (cannot be restricted)
- Provider roles are system-defined (cannot add/remove roles)
- Permission changes sync to Provider Platform (FR-009) within 5 seconds
- Permission changes affect all provider team members with that role across all providers
- System shows warning when editing: "This will affect [count] provider team members across all provider organizations"

**Notes**:

- Display sync status indicator: "Last synced to Provider Platform: [timestamp]"
- Show impact summary before saving: "This change will affect [X] providers and [Y] team members"

---

### Screen 2: Invite Team Member Form

**Purpose**: Allows Super Admin to invite new admin team members with role assignment. Accessed from "Invite Team Member" button in Admin Users tab.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| First Name | text | Yes | Admin user's first name | Max 50 characters; letters, spaces, hyphens only |
| Last Name | text | Yes | Admin user's last name | Max 50 characters; letters, spaces, hyphens only |
| Email Address | email input | Yes | New admin user's email | Valid email format; unique (not already in use); lowercase conversion |
| Phone Number | tel input | No | Admin user's phone number | E.164 format validation; optional for now (MFA implementation planned for future) |
| Assigned Role | select (dropdown) | Yes | Role to assign to new user | Must select from available admin roles (Super Admin, Aftercare Specialist, Billing Staff, Support Staff) |
| Personal Message | textarea | No | Optional welcome message from Super Admin | Max 500 characters; included in invitation email |

**Actions**:

- **Send Invitation**: Generates invitation token and sends email
- **Cancel**: Closes form without sending invitation
- **Preview Email**: Opens preview modal showing how invitation email will appear

**Business Rules**:

- Email validation occurs on blur (field loses focus) for immediate feedback
- System checks for duplicate email across all admin users (active, suspended, pending)
- Role dropdown populated from active admin roles only (archived roles excluded)
- Role dropdown displays: role name + brief description on hover
- Form cannot be submitted until all required fields pass validation
- Invitation token expires after 7 days (168 hours)
- Personal message is optional but recommended for first-time team setup
- Phone number field is optional (MFA will be implemented in future enhancement)

**Validation Messages**:

- Email already in use: "This email is already associated with an admin account. Please use a different email or check existing team members."
- Invalid email format: "Please enter a valid email address."
- Invalid phone format: "Please enter a valid phone number (e.g., +1234567890)."
- Role not selected: "Please select a role for this team member."

**Notes**:

- Display role permission summary below role dropdown (expandable section showing what this role can access)
- Show estimated invitation expiry time: "Invitation will expire in 7 days on [date] at [time]"
- System auto-generates preview showing: invitee name, role, personal message (if provided), invitation link placeholder
- After successful send, show confirmation: "Invitation sent to [email]. They have 7 days to accept."

---

### Screen 3: Admin Account Setup (Onboarding)

**Purpose**: New admin user account creation after accepting invitation. This screen is accessed via the invitation link sent in the email. Collects account details and enforces security requirements before granting access to Admin Platform.

**Context**: Displayed after new admin user clicks invitation link in email and token is validated by system.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Email | display (read-only) | N/A | Pre-filled from invitation, locked | Read-only; must match invitation token |
| First Name | text | Yes | Editable first name (pre-filled from invitation) | 2-50 characters; letters, spaces, hyphens only |
| Last Name | text | Yes | Editable last name (pre-filled from invitation) | 2-50 characters; letters, spaces, hyphens only |
| Phone Number | tel input | No | Primary contact phone for admin user | E.164 format (e.g., +1234567890); optional for now (MFA planned for future) |
| Password | password | Yes | Account password | Must satisfy password policy: min 12 chars, uppercase, lowercase, number, special char from !@#$%^&(),.?\":{}&#124;<> |
| Confirm Password | password | Yes | Re-enter password | Must match Password field exactly |
| Accept Terms | checkbox | Yes | Confirm platform terms & privacy policy | Must be checked before submission |

**Actions**:

- **Create Account**: Submits form and creates admin account
- **Cancel**: Returns to login page (invalidates invitation token if clicked)

**Business Rules**:

- Email field is pre-filled from invitation token and cannot be edited
- First Name and Last Name are pre-filled from invitation but can be edited
- Password must meet system security policy (defined in FR-026):
  - Minimum 12 characters
  - At least one uppercase letter
  - At least one lowercase letter
  - At least one number
  - At least one special character from !@#$%^&(),.?":{}|<>
- "Create Account" button disabled until all required fields are valid and terms are accepted
- Phone number is optional for now (MFA enrollment will be added in future enhancement)
- Invitation token validated before displaying form
- Expired or invalid tokens redirect to error page with "Request New Invitation" option

**Validation Messages**:

- Password too weak: "Password must be at least 12 characters with uppercase, lowercase, number, and special character from !@#$%^&(),.?\":{}|<>."
- Password mismatch: "Passwords do not match."
- Terms not accepted: "You must accept the Terms of Service to continue."
- Invalid phone format: "Please enter a valid phone number (e.g., +1234567890)."

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
10. New admin user can immediately log in with new credentials

**Notes**:

- Display provider branding (Hairline Admin Platform logo and name)
- Show invitation expiry countdown if less than 24 hours remaining: "Your invitation expires in [X] hours"
- Show assigned role in header: "You've been invited as [Role Name]"
- Include personal message from Super Admin if provided (display below header)
- Security notice: "Strong password required. All admin actions are logged for security."
- MFA enrollment section marked as "Coming Soon" with note: "Multi-factor authentication will be required in future updates"

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
- Warning (if Provider Role): "Changes will affect all provider organizations"

---

#### View Mode 1: Single Role Edit (Default)

**Purpose**: Edit permissions for one specific role with detailed checkboxes organized by category.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Role Name | text | Yes | Name of role (e.g., "Aftercare Specialist") | **Locked for system roles** (Super Admin, Aftercare Specialist, Billing Staff, Support Staff) and provider roles (Owner, Manager, Clinical Staff, Billing Staff). **Editable only for custom roles**. When editable: max 50 chars; unique. |
| Role Description | textarea | Yes | Purpose and responsibilities of role | Max 500 chars |
| Permission Categories | accordion | Yes | Grouped permissions by feature area | At least one permission required |

**Permission Matrix Structure** (Expandable Categories):

**Category: Dashboard & Overview (A-01)**:

| Permission | Description | Access Level |
|------------|-------------|--------------|
| View Dashboard | Access main admin dashboard | ☐ Read |
| View Patient Overview | View patients across all lifecycle stages | ☐ Read |

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

**Category: Quotes & Inquiries Oversight (A-01)**:

| Permission | Description | Access Level |
|------------|-------------|--------------|
| View Inquiries Overview | View all inquiries across lifecycle stages | ☐ Read |
| View Quote Details | View all quotes per inquiry | ☐ Read |
| Edit Quotes | Modify quotes (provider cancellations, rescheduling) | ☐ Write |
| Reassign Providers | Manually assign/reassign providers to inquiries | ☐ Write |

**Category: Reviews & Ratings Management (A-01)**:

| Permission | Description | Access Level |
|------------|-------------|--------------|
| View Reviews | View all patient reviews | ☐ Read |
| Moderate Reviews | Approve/reject/edit reviews | ☐ Write |
| Add Reviews | Import authenticated reviews for providers | ☐ Write |
| Manage Review Categories | Configure review categories and labels | ☐ Write |

**Category: Billing & Financial (A-05)**:

| Permission | Description | Access Level |
|------------|-------------|--------------|
| View Transactions | View patient and provider transactions | ☐ Read |
| Process Payouts | Initiate provider payouts | ☐ Write |
| Issue Refunds | Process patient refunds | ☐ Write (requires approval) |
| View Financial Reports | Access revenue analytics | ☐ Read |
| View Patient Billing | View patient invoices and payment status | ☐ Read |
| Send Payment Reminders | Send payment reminders to patients | ☐ Write |
| Download Invoices | Download patient/provider invoices | ☐ Read |

**Category: Promotions & Discounts (A-06)**:

| Permission | Description | Access Level |
|------------|-------------|--------------|
| View Discounts | View all discount codes (Hairline and provider) | ☐ Read |
| Create Discounts | Create platform-wide discount codes | ☐ Write |
| Edit Discounts | Modify discount parameters | ☐ Write |
| Track Discount Usage | View discount statistics and ROI | ☐ Read |
| Approve Provider Discounts | Approve/decline provider discount requests | ☐ Write |

**Category: Affiliate Management (A-07)**:

| Permission | Description | Access Level |
|------------|-------------|--------------|
| View Affiliates | View affiliate list and details | ☐ Read |
| Create Affiliates | Add new affiliate accounts | ☐ Write |
| Edit Affiliates | Modify affiliate profiles and commission rules | ☐ Write |
| Process Affiliate Payouts | Process affiliate commission payments | ☐ Write |
| View Affiliate Performance | View referral counts and conversions | ☐ Read |

**Category: Analytics & Reporting (A-08)**:

| Permission | Description | Access Level |
|------------|-------------|--------------|
| View Analytics Dashboard | Access platform-wide analytics overview | ☐ Read |
| View Provider Analytics | View provider performance metrics | ☐ Read |
| View Financial Analytics | View revenue and conversion analytics | ☐ Read |
| Export Reports | Export analytics reports (PDF/CSV) | ☐ Read |
| View Treatment Outcomes | Access treatment outcomes analytics | ☐ Read |

**Category: Communication & Support (A-10)**:

| Permission | Description | Access Level |
|------------|-------------|--------------|
| View Support Center | Access patient support cases | ☐ Read |
| Respond to Support | Send messages to patients/providers | ☐ Write |
| View Provider-Patient Messages | Monitor provider-to-patient communications | ☐ Read |
| Flag Communications | Flag suspicious or policy-violating messages | ☐ Write |
| Export Conversation Transcripts | Export chat transcripts for compliance | ☐ Read |

**Category: Travel Management (A-04)**:

| Permission | Description | Access Level |
|------------|-------------|--------------|
| View Travel Bookings | View flight and hotel bookings | ☐ Read |
| Manage Travel Settings | Configure travel API settings and commissions | ☐ Write |
| View Travel Reports | View travel booking analytics | ☐ Read |

**Category: System Settings (A-09)**:

| Permission | Description | Access Level |
|------------|-------------|--------------|
| View Settings | View system configuration | ☐ Read |
| Edit Settings | Modify system settings | ☐ Write (Super Admin only) |
| Manage Users | Create/edit admin accounts | ☐ Write (Super Admin only) |
| Manage Roles | Create/edit roles and permissions | ☐ Write (Super Admin only) |
| Manage Terms & Conditions | Edit patient/provider terms and consent | ☐ Write |
| Manage App Data | Edit countries, discovery questions, location presentation | ☐ Write |
| Manage Treatment Catalog | Create/edit treatments and packages | ☐ Write |
| Manage Aftercare Templates | Create/edit aftercare milestone templates | ☐ Write |
| Manage Notification Templates | Edit email templates (OTP, confirmations) | ☐ Write |
| Configure Payment Settings | Manage Stripe accounts, commission rates, split pay | ☐ Write |
| Manage Help Centre | Create/edit Help Centre content for providers | ☐ Write |

**Provider Platform Permission Categories** (for configuring Owner, Manager, Clinical Staff, Billing Staff roles):

**Category: Patient Inquiries & Quotes (PR-02)**:

| Permission | Description | Access Level |
|------------|-------------|--------------|
| View Inquiries | View patient inquiry list and details | ☐ Read |
| Respond to Inquiries | Submit quotes and respond to inquiries | ☐ Write |
| Edit Quotes | Modify submitted quotes | ☐ Write |
| Accept/Decline Quotes | Accept or decline patient quote acceptances | ☐ Write |
| View Quote History | View all quotes for inquiries | ☐ Read |

**Category: Appointments & Scheduling (PR-02)**:

> Note: In the System PRD, appointment slot pre-scheduling is part of the inquiry/quote flow; this category is tracked under PR-02 for module-code consistency.

| Permission | Description | Access Level |
|------------|-------------|--------------|
| View Appointments | View scheduled appointments | ☐ Read |
| Schedule Appointments | Create and schedule appointments | ☐ Write |
| Edit Appointments | Modify appointment details | ☐ Write |
| Cancel Appointments | Cancel scheduled appointments | ☐ Write |
| View Calendar | Access provider calendar view | ☐ Read |

**Category: Treatment & Procedures (PR-03)**:

| Permission | Description | Access Level |
|------------|-------------|--------------|
| View In-Progress Cases | View patients currently in treatment | ☐ Read |
| Document Treatment | Add treatment notes, scans, photos | ☐ Write |
| Update Treatment Status | Change patient treatment stage | ☐ Write |
| View Treatment History | Access historical treatment records | ☐ Read |

**Category: Aftercare Management (PR-04)**:

| Permission | Description | Access Level |
|------------|-------------|--------------|
| View Aftercare Cases | View aftercare patient list | ☐ Read |
| Manage Aftercare Plans | Create and edit aftercare plans | ☐ Write |
| Chat with Patients | Access aftercare messaging | ☐ Write |
| Schedule Consultations | Book video consultations | ☐ Write |
| View Progress Reports | Access patient progress data | ☐ Read |

**Category: Financial & Billing (PR-05)**:

| Permission | Description | Access Level |
|------------|-------------|--------------|
| View Financial Dashboard | View revenue and earnings | ☐ Read |
| View Payouts | View payment history and upcoming payouts | ☐ Read |
| Manage Bank Details | Update payment account information | ☐ Write (Owner only) |
| View Financial Reports | Access financial analytics | ☐ Read |

**Category: Team Management (PR-01)**:

| Permission | Description | Access Level |
|------------|-------------|--------------|
| View Team Members | View team member list | ☐ Read |
| Invite Team Members | Send team member invitations | ☐ Write |
| Edit Team Member Roles | Change team member roles (non-Owner) | ☐ Write (Owner/Manager only) |
| Remove Team Members | Remove or suspend team members | ☐ Write (Owner only) |
| View Team Activity | Access team activity logs | ☐ Read |

**Category: Provider Settings (PR-06)**:

| Permission | Description | Access Level |
|------------|-------------|--------------|
| View Profile | View provider profile information | ☐ Read |
| Edit Profile | Update provider profile details | ☐ Write |
| Manage Treatments | Add/edit treatment offerings | ☐ Write |
| Manage Promotions | Create and edit discount codes | ☐ Write |
| View Settings | View provider settings | ☐ Read |
| Edit Settings | Modify provider settings | ☐ Write (Owner only) |

**Modal Actions** (Single Role Mode):

- **Save Changes**: Saves permission changes and closes modal
- **Cancel**: Closes modal (shows confirmation dialog if unsaved changes exist)
- **Reset to Default**: Resets to system-recommended permissions for this role (if available)
- **Preview Impact**: Shows which users and providers will be affected by changes
- **Switch to Matrix View**: Switches to 2-axis matrix comparison view (shows confirmation dialog if unsaved changes exist)
- **Close (X button)**: Closes modal (shows confirmation dialog if unsaved changes exist)

---

#### View Mode 2: Matrix Comparison View

**Purpose**: View and edit permissions across multiple roles simultaneously in a 2-axis table format for easy comparison and bulk editing.

**Layout**: 2-axis table where:

- **Rows** = Permissions (grouped by category/module)
- **Columns** = Roles (all roles of the same type: Admin or Provider)
- **Cell Values** = Checkboxes (☐ = unchecked, ☑ = checked) or access level indicators (Read/Write/Delete/None)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Role Type Filter | toggle | Yes | Filter to Admin Roles or Provider Roles | Single selection |
| Permission Categories | expandable sections | Yes | Group permissions by module/feature area | Expand/collapse per category |
| Matrix Table | table | Yes | 2-axis table with permissions as rows, roles as columns | Scrollable horizontally and vertically |

**Matrix Table Structure**:

**Example for Admin Roles**:

| Permission | Category | Super Admin | Aftercare Specialist | Billing Staff | Support Staff | Custom Role 1 |
|------------|----------|-------------|---------------------|---------------|---------------|---------------|
| View Dashboard | A-01 | ☑ | ☑ | ☑ | ☑ | ☑ |
| View Patient Overview | A-01 | ☑ | ☑ | ☑ | ☑ | ☑ |
| View Patients | A-01 | ☑ | ☑ | ☑ | ☑ | ☑ |
| Edit Patients | A-01 | ☑ | ☐ | ☐ | ☐ | ☐ |
| Delete Patients | A-01 | ☑ | ☐ | ☐ | ☐ | ☐ |
| View Quotes & Inquiries | A-01 | ☑ | ☐ | ☐ | ☐ | ☐ |
| Edit Quotes | A-01 | ☑ | ☐ | ☐ | ☐ | ☐ |
| View Reviews | A-01 | ☑ | ☑ | ☐ | ☐ | ☐ |
| Moderate Reviews | A-01 | ☑ | ☐ | ☐ | ☐ | ☐ |
| View Providers | A-02 | ☑ | ☑ | ☑ | ☑ | ☑ |
| Edit Providers | A-02 | ☑ | ☐ | ☐ | ☐ | ☐ |
| Onboard Providers | A-02 | ☑ | ☐ | ☐ | ☐ | ☐ |
| Suspend Providers | A-02 | ☑ | ☐ | ☐ | ☐ | ☐ |
| View Aftercare Cases | A-03 | ☑ | ☑ | ☐ | ☐ | ☐ |
| Manage Aftercare | A-03 | ☑ | ☑ | ☐ | ☐ | ☐ |
| Chat with Patients (Aftercare) | A-03 | ☑ | ☑ | ☐ | ☐ | ☐ |
| Schedule Consultations | A-03 | ☑ | ☑ | ☐ | ☐ | ☐ |
| View Transactions | A-05 | ☑ | ☐ | ☑ | ☐ | ☐ |
| Process Payouts | A-05 | ☑ | ☐ | ☑ | ☐ | ☐ |
| Issue Refunds | A-05 | ☑ | ☐ | ☐ | ☐ | ☐ |
| View Patient Billing | A-05 | ☑ | ☐ | ☑ | ☐ | ☐ |
| View Discounts | A-06 | ☑ | ☐ | ☑ | ☐ | ☐ |
| Create Discounts | A-06 | ☑ | ☐ | ☐ | ☐ | ☐ |
| View Affiliates | A-07 | ☑ | ☐ | ☐ | ☐ | ☐ |
| View Analytics | A-08 | ☑ | ☑ | ☑ | ☐ | ☐ |
| View Support Center | A-10 | ☑ | ☑ | ☐ | ☑ | ☐ |
| Respond to Support | A-10 | ☑ | ☑ | ☐ | ☑ | ☐ |
| View Settings | A-09 | ☑ | ☑ | ☑ | ☑ | ☑ |
| Edit Settings | A-09 | ☑ | ☐ | ☐ | ☐ | ☐ |
| Manage Users | A-09 | ☑ | ☐ | ☐ | ☐ | ☐ |
| Manage Roles | A-09 | ☑ | ☐ | ☐ | ☐ | ☐ |

**Example for Provider Roles**:

| Permission | Category | Owner | Manager | Clinical Staff | Billing Staff |
|------------|----------|-------|---------|----------------|---------------|
| View Inquiries | PR-02 | ☑ | ☑ | ☐ | ☐ |
| Respond to Inquiries | PR-02 | ☑ | ☑ | ☐ | ☐ |
| View Appointments | PR-02 | ☑ | ☑ | ☑ | ☐ |
| Schedule Appointments | PR-02 | ☑ | ☑ | ☑ | ☐ |
| View In-Progress Cases | PR-03 | ☑ | ☑ | ☑ | ☐ |
| Document Treatment | PR-03 | ☑ | ☑ | ☑ | ☐ |
| View Financial Dashboard | PR-05 | ☑ | ☑ | ☐ | ☑ |
| View Payouts | PR-05 | ☑ | ☑ | ☐ | ☑ |
| Manage Bank Details | PR-05 | ☑ | ☐ | ☐ | ☐ |
| View Team Members | PR-01 | ☑ | ☑ | ☐ | ☐ |
| Invite Team Members | PR-01 | ☑ | ☑ | ☐ | ☐ |

**Matrix View Features**:

- **Column Headers**: Role names with user count badges (e.g., "Super Admin (3 users)")
- **Row Headers**: Permission name + category/module code
- **Cell Interaction**: Click checkbox to toggle permission for that role
- **Bulk Actions**:
  - "Select All" checkbox in column header to grant all permissions to a role
  - "Select All" checkbox in row header to grant permission to all roles
  - "Select Category" to grant all permissions in a category to selected roles
- **Visual Indicators**:
  - Locked cells (Super Admin, Owner) shown with lock icon and disabled checkbox
  - Permission dependencies highlighted (e.g., "Edit" row highlighted when "View" is checked)
  - Color coding: Green = granted, Gray = not granted, Red = locked/protected
- **Filtering**:
  - Filter permissions by category/module
  - Search permissions by name
  - Show only differences between roles
- **Sorting**:
  - Sort columns (roles) alphabetically or by user count
  - Sort rows (permissions) by category or alphabetically

**Modal Actions** (Matrix Mode):

- **Save All Changes**: Saves all permission changes across all roles and closes modal
- **Cancel**: Closes modal (shows confirmation dialog if unsaved changes exist)
- **Reset Role to Default**: Resets selected role(s) to system-recommended permissions (shows confirmation dialog if unsaved changes exist)
- **Export Matrix**: Export matrix to CSV/Excel for documentation
- **Switch to Single Role View**: Switches to single role edit mode for focused editing (shows confirmation dialog if unsaved changes exist)
- **Close (X button)**: Closes modal (shows confirmation dialog if unsaved changes exist)

**Business Rules** (Matrix Mode):

- All business rules from Single Role Mode apply
- Changes can be made to multiple roles simultaneously
- System shows confirmation dialog listing all affected roles and user counts before saving
- Locked roles (Super Admin, Owner) remain locked in matrix view
- Permission dependencies apply across all roles (e.g., checking "Edit" for any role auto-checks "View" for that role)

**Business Rules** (Both Modes):

- Permissions organized by module code (A-01, A-02 for admin; PR-01, PR-02, etc. for provider) for traceability
- "Select All" checkbox available for each category
- Permission dependencies highlighted (e.g., "Edit Patients" requires "View Patients")
- System prevents saving role with zero permissions
- **Admin Role Protection**: Super Admin permissions cannot be removed from Super Admin role (system protection, checkboxes disabled)
- **Provider Role Protection**: Owner role must always have full access to all provider features (cannot be restricted, checkboxes disabled for critical permissions)
- Permission changes take effect for all users with that role on the next API call after propagation (≤ 5 seconds)
- **Provider Permission Propagation**: Changes to provider role permissions automatically sync to Provider Platform (FR-009) within 5 seconds
- Role edits logged in audit trail with before/after permission comparison
- **UI Enforcement**: Admin and Provider platforms hide UI elements (menu items, buttons, tabs, sections) for features users cannot access based on their role permissions

**Validation**:

- Display warning when granting sensitive permissions (billing, user management, provider suspension)
- Show confirmation dialog before saving: "This will affect [X] users. Continue?"
- For provider roles: "This will affect [Y] team members across [Z] provider organizations. Continue?"
- Highlight permission dependencies (selecting "Edit X" automatically selects "View X")

**Notes**:

- Modal is scrollable for long permission lists
- Permissions grouped by feature area with expand/collapse accordions
- Search/filter box to quickly find specific permissions
**Unsaved Changes Protection**:

- **Detection**: System tracks all permission changes (checkbox toggles, bulk selections) and compares against saved state
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

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| User Profile | section (read-only) | N/A | Name, email, role, status, created date | - |
| Current Role | badge | N/A | Currently assigned role with color coding | - |
| Role Effective From | datetime | N/A | When the current role became (or will become) active | - |
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
- **Rule 3**: Authorization MUST be evaluated server-side on every API call using the latest role assignment and permission matrix. Server-side caching is allowed only if invalidated/updated within 5 seconds of a role/permission change; enforcement MUST reflect changes on the next API call after cache invalidation.
- **Rule 4**: At least one active Super Admin account MUST exist at all times (system protection against lockout)
- **Rule 5**: All administrative actions (role changes, permission grants, user suspensions) MUST be logged in audit trail
- **Rule 6**: Invitation tokens expire after 7 days (configurable via A-09 settings; range 1-30 days)
- **Rule 7**: Suspended admin users cannot log in but accounts remain in system (soft suspension, not deletion)
- **Rule 8**: Role assignments MUST be stored with an **Effective From** timestamp; enforcement MUST respect that effective date/time on authorization checks
- **Rule 9**: Role names for system-defined roles (admin + provider) MUST be immutable (not editable/renamable); only custom admin roles can be renamed.

### Data & Privacy Rules

- **Privacy Rule 1**: Audit trail entries are immutable and retained for 10 years (compliance requirement per Constitution Principle VI)
- **Privacy Rule 2**: IP addresses logged for security audit purposes (GDPR-compliant logging)
- **Privacy Rule 3**: Password reset requests logged in audit trail with requester identity
- **Audit Rule**: All access to sensitive features (billing, patient medical data, provider financial data) MUST be logged with: timestamp, user ID, action, IP address, outcome
- **GDPR Compliance**: Admin user data (email, name) can be anonymized on account deletion request, but audit trail preserved with anonymized identifiers

### Provider Role Permission Rules

- **Provider Rule 1**: Provider role descriptions in FR-009 are recommended defaults; the configured permission matrix in FR-031 is authoritative and may grant additional access (e.g., Clinical Staff granted read-only financial reporting)

### Admin Editability Rules

**Editable by Super Admin**:

- Create, edit, delete custom roles
- Assign/change roles for any admin user
- Suspend/activate admin accounts
- Configure invitation token expiry time (default 7 days, range 1-30 days)
- Create permission matrix for custom roles
- Re-send invitation emails for pending accounts

**Fixed in Codebase (Not Editable)**:

- Super Admin role permissions (always full access)
- System role names (Super Admin, Aftercare Specialist, Billing Staff, Support Staff) and provider role names (Owner, Manager, Clinical Staff, Billing Staff)
- Core permission categories (cannot rename or remove: Patient Management, Provider Management, Billing, etc.)
- Audit trail retention period (10 years, per Constitution)
- Password hashing algorithm (bcrypt, cost factor 12)
- Password requirements (12 chars minimum, 1 upper, 1 lower, 1 digit, 1 special char)

**Configurable with Restrictions**:

- Invitation token expiry (configurable within 1-30 day range)
- Maximum failed login attempts before lockout (configurable in A-09: Authentication Settings)
- Session timeout duration (configurable in A-09: Authentication Settings)
- Number of concurrent sessions per admin user (default: 3, range: 1-5)

---

## Success Criteria

### Admin Management Efficiency Metrics

- **SC-001**: Super Admins can invite and activate new admin team members in under 2 minutes (from invitation to account activation)
- **SC-002**: Role assignment changes take effect on the next user action/API call within 5 seconds
- **SC-003**: 90% of admin team member invitations are activated within 24 hours of sending
- **SC-004**: Super Admins can create custom roles with granular permissions in under 5 minutes

### Security & Compliance Metrics

- **SC-005**: 100% of administrative actions (role changes, permission grants, suspensions) are logged in audit trail
- **SC-006**: Zero unauthorized access to restricted admin features (all access attempts properly validated)
- **SC-007**: Audit trail entries are immutable and retained for 10 years per compliance requirements
- **SC-008**: System architecture supports MFA integration (MFA is a planned Post-MVP requirement and will be enforced platform-wide once the shared MFA stack is delivered per Constitution Principle II)
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
  - **Why needed**: FR-009 handles provider team member invitation, assignment, and management. FR-031 provides the **centralized permission configuration** for provider roles that FR-009 consumes and enforces.
  - **Integration point**:
    - **FR-031 defines and configures** provider role permission matrices (Owner, Manager, Clinical Staff, Billing Staff permissions)
    - **FR-009 consumes** these permission definitions from FR-031 and enforces them when provider team members access features
    - Permission changes made in FR-031 automatically propagate to FR-009 enforcement
    - Both modules share the underlying authorization infrastructure while keeping **admin roles** (Super Admin, Aftercare Specialist, Billing Staff, Support Staff) separate from **provider roles** in terms of management, but unified in terms of permission configuration

- **FR-015**: Provider Management
  - **Why needed**: FR-015 handles provider organization management and provides oversight of provider team members
  - **Integration point**:
    - **FR-031**: Configures what provider roles can do (RBAC configuration)
    - **FR-015**: Views provider organizations and their team members (oversight and management)
    - "View Users" action in FR-031 Provider Roles tab links to FR-015
    - This separation avoids duplication: FR-031 = RBAC configuration, FR-015 = provider oversight

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
- **Assumption 2**: New admin team members will activate accounts within 7 days of invitation
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
- **Security**: Authorization is evaluated server-side per request using the current role assignment and permission matrix. JWT tokens are used for authentication (user/session identity) and are signed with RS256.

### Integration Points

- **Integration 1**: Admin API endpoints check permissions via middleware
  - **Data format**: JWT token containing authenticated user/session identifiers (not authoritative role/permission claims)
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

- **Authentication**: MFA support planned (MFA will be a mandatory control for all admin platform users Post-MVP, once the shared stack is available per Constitution Principle II)
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

1. **Given** Super Admin navigates to Settings > User Roles & Permissions, **When** Super Admin creates new role "Analytics Viewer" with permissions: View Financial Reports (read), View Patient Data (read), View Provider Data (read), **Then** role saved and available in role dropdown for user assignment

2. **Given** custom role "Analytics Viewer" exists, **When** Super Admin assigns role to user "<analyst@hairline.com>", **Then** user can view reports but cannot edit data, process payouts, or modify settings

3. **Given** analytics viewer is logged in, **When** user attempts to edit patient information, **Then** edit button hidden or disabled and action denied if attempted via API

---

### User Story 3 - Configure Provider Role Permissions (Priority: P1)

As a Super Admin, I need to configure and manage permissions for provider roles (Owner, Manager, Clinical Staff, Billing Staff) so that provider team members have appropriate access to platform features based on their role, and these permissions are consistently enforced across all provider organizations.

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

2. **Given** admin user with "Support Staff" role attempts to access Provider Billing section, **When** access denied due to insufficient permissions, **Then** access denial logged in audit trail with: timestamp, user ID, requested feature, IP address, outcome "Denied"

3. **Given** Super Admin reviews audit trail for last 30 days, **When** Super Admin exports audit log to CSV, **Then** CSV file contains all audit entries with columns: timestamp, user, action, details, IP address, outcome

---

### User Story 5 - Role Change Notification (Priority: P2)

As an admin user, I need to be notified immediately when my role or permissions change, so I understand what features I can now access or no longer access.

**Why this priority**: Transparency and user awareness; reduces support tickets from confused users

**Independent Test**: Can be tested by changing user's role and verifying email notification sent with permission comparison

**Acceptance Scenarios**:

1. **Given** admin user "<support@hairline.com>" has role "Support Staff", **When** Super Admin changes role to "Aftercare Specialist", **Then** user receives email notification within 5 minutes with: old role, new role, permission changes summary

2. **Given** role change notification received, **When** user logs in after role change, **Then** dashboard reflects new role permissions (aftercare features visible, support features hidden)

3. **Given** user's role changed from "Billing Staff" to "Support Staff", **When** user attempts to access previously permitted billing feature, **Then** access denied and user informed: "Your permissions have changed. You no longer have access to this feature."

---

### User Story 6 - Prevent System Lockout (Priority: P1)

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

- **REQ-031-001**: System MUST allow Super Admins to invite new admin team members via email with role assignment
- **REQ-031-002**: System MUST support creation of custom roles with granular permission assignment per admin module (A-01 through A-10)
- **REQ-031-003**: System MUST enforce role-based access control on all admin API endpoints and UI components
- **REQ-031-004**: System MUST provide predefined admin roles: Super Admin, Aftercare Specialist, Billing Staff, Support Staff
- **REQ-031-005**: System MUST provide centralized configuration interface for provider role permissions (Owner, Manager, Clinical Staff, Billing Staff)
- **REQ-031-006**: System MUST automatically sync provider role permission changes to Provider Platform (FR-009) within 5 seconds
- **REQ-031-007**: System MUST prevent modification of Owner role permissions that would remove full access to provider features
- **REQ-031-008**: System MUST log all administrative actions (role changes, permission grants, user suspensions, access denials) in immutable audit trail
- **REQ-031-009**: System MUST prevent suspension or deletion of the last Super Admin account (system protection)
- **REQ-031-010**: System MUST send email notifications for: new invitations, role changes, password resets, repeated access denials
- **REQ-031-011**: System MUST support role assignment changes with **Effective From** date/time tracking (stored and auditable)

### Data Requirements

- **REQ-031-012**: System MUST maintain admin user accounts with: email, name, password hash, assigned role(s), role effective date/time, status (active/pending/suspended), creation date, last login timestamp
- **REQ-031-013**: System MUST maintain role definitions with: role name, description, assigned permissions (as permission matrix)
- **REQ-031-014**: System MUST maintain audit trail entries with: timestamp, user ID, action type, action details, IP address, outcome (success/failed/denied)
- **REQ-031-015**: System MUST retain audit trail for minimum 10 years per compliance requirements (Constitution Principle VI)

### Security & Privacy Requirements

- **REQ-031-016**: System MUST be architected to support Multi-Factor Authentication (MFA) integration as a planned Post-MVP requirement (per Constitution Principle II)
- **REQ-031-017**: System MUST use bcrypt (cost factor 12+) for password hashing
- **REQ-031-018**: System MUST enforce password requirements: minimum 12 characters, 1 uppercase, 1 lowercase, 1 digit, 1 special character
- **REQ-031-019**: System MUST sign JWT tokens with RS256 (asymmetric encryption) to prevent tampering
- **REQ-031-020**: System MUST perform server-side authorization evaluation on each API call based on current role assignments and permission matrices; JWT tokens MUST NOT be the authoritative source of permissions
- **REQ-031-021**: System MUST invalidate active sessions (and/or reject access tokens) immediately upon account suspension; at minimum, all API calls MUST be rejected for suspended accounts starting with the next request
- **REQ-031-022**: System MUST anonymize admin user PII (email, name) on account deletion request, while preserving audit trail with anonymized identifier

### Integration Requirements

- **REQ-031-023**: System MUST integrate with Notification Service (S-03) for email delivery (invitations, role changes, password resets)
- **REQ-031-024**: System MUST provide permission check API for all admin modules to enforce access control
- **REQ-031-025**: System MUST cache permission matrix in memory for fast authorization checks (< 50ms per check)
- **REQ-031-026**: System MUST invalidate permission cache within 5 seconds of role or permission changes

---

## Key Entities

- **Entity 1 - Admin User Account**
  - **Key attributes**: user_id (UUID), email (unique), name, password_hash, assigned_role_id (foreign key), role_effective_from (timestamp), status (active/pending/suspended), created_at (timestamp), last_login_at (timestamp), MFA_enabled (boolean), invitation_token (nullable, expires after 7 days)
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
| 2026-01-04 | 1.0.1 | Lock system/provider role names (Issue #3 option 1); mark status + approvals as ✅ Verified & Approved | GPT-5.2 (AI) |

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
**Last Updated**: 2026-01-04
