# Product Requirements Document: App Settings & Security Policies

**Module**: A-09: System Settings & Configuration
**Feature Branch**: `fr026-app-settings-security`
**Created**: 2025-11-04
**Status**: ✅ Verified & Approved
**Source**: FR-026 from system-prd.md, Client transcription (Hairline-AdminPlatformPart2.txt)

---

## Executive Summary

The App Settings & Security Policies module provides a centralized, audited, and versioned configuration surface for application-wide settings, security policies, app data lists, and notification templates that affect multiple modules and tenants (Patient, Provider, Admin). This module is the single source of truth for critical system configurations including authentication throttling, OTP parameters, centrally managed lists (countries, discovery questions), and notification templates.

**Problem**: Currently, settings are scattered across different modules, making it difficult to maintain consistency, audit changes, or roll back problematic configurations. Security policies like authentication throttling and OTP expiry are hardcoded, preventing operational flexibility.

**Solution**: A unified admin interface where authorized administrators can view, create, update, and version settings within clearly defined groups (Authentication & Security, App Data Lists, Notifications). All changes require a reason and are fully auditable (who/when/old value/new value).

**Value Delivered**:

- **Operational Efficiency**: Admins can adjust security policies without code deployments
- **Auditability**: Complete audit trail of all configuration changes
- **Consistency**: Single source of truth for settings consumed by Patient, Provider, and Admin platforms
- **Risk Mitigation**: Ability to rapidly adjust configurations forward-only (no rollback) with a complete audit trail
- **Compliance**: Demonstrated control over security parameters for audits

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-01)**: Consumes authentication policies, OTP configurations, country/calling code lists, and discovery question options
- **Provider Platform (PR-06)**: Indirectly consumes centrally managed lists for profile settings
- **Admin Platform (A-09)**: Primary interface for viewing, editing, and versioning all settings
- **Shared Services (S-03)**: Notification Service consumes OTP email templates for delivery

### Multi-Tenant Breakdown

**Patient Platform (P-01)**:

- Patient registration and login flows apply authentication throttling policies
- OTP verification for email confirmation applies OTP expiry and resend cooldown
- Profile forms use centrally managed country and calling code lists
- Discovery questions ("How did you find us?") display options from centralized list
- Changes to settings propagate to patient app within 1 minute

**Provider Platform (PR-06 & PR-01)**:

- Provider staff management (PR-06) indirectly uses centrally managed lists
- Authentication throttling (PR-01) applies to provider login attempts
- OTP parameters (PR-01) apply to provider email verification flows

**Admin Platform (A-09)**:

- Admins access Settings Management UI to view and edit configurations
- All changes require reason entry and are logged with timestamp, admin ID, old value, new value
- Version history displays for each setting group
- Rollback capability is not supported; admins make forward-only changes
- Role-based access restricts sensitive settings to authorized admins only
- Sensitive values (API keys, secrets) are masked in UI and logs

**Shared Services (S-03)**:

- Notification Service reads OTP email templates for verification and password reset emails
- Template changes do NOT affect users already in a flow (existing OTP emails remain unchanged)
- New template versions apply only to new OTP generation requests

### Communication Structure

**In Scope**:

- Admin editing OTP email templates (verification, password reset)
- Template preview functionality
- Template variable substitution ({code}, {email}, {expiry_minutes})

**Out of Scope**:

- Actual email sending (handled by S-03: Notification Service)
- SMS notifications (future enhancement, V2)
- Push notification templates (handled separately in notification preferences module)
- Legal content management (see FR-027: Terms & Conditions, Privacy Policy, Consent forms)
- Regional configuration and pricing (see FR-028: Location presentation, starting prices by currency)
- Payment system configuration (see FR-029: Stripe account management, conversion rates, split payment rules)
- Notification rules and event-based triggers (see FR-030: Event-to-notification mapping, channel configuration)
- Admin access control and role-based permissions (see FR-031: Role management, permission matrix)

### Entry Points

**Admin-Initiated**:

- Admin navigates to Settings → Authentication & Security to edit throttling policies
- Admin navigates to Settings → App Data to manage country lists or discovery questions
- Admin navigates to Settings → Notifications to edit OTP email templates

**System-Triggered**:

- Settings cache refresh occurs automatically every 60 seconds
- Dependent services (Patient app, Provider app, Notification service) poll for setting changes
- Version history automatically captures changes on save

---

## Business Workflows

### Main Flow: Admin Edits Authentication Throttling Policy

**Actors**: Admin, System, Patient Platform (P-01), Provider Platform (PR-01)
**Trigger**: Admin determines that current lockout policy (5 attempts, 15-minute lockout) is too strict and needs adjustment
**Outcome**: Updated throttling policy (7 attempts, 10-minute lockout) is saved, versioned, audited, and propagated to all platforms within 1 minute

**Steps**:

1. Admin logs into Admin Platform and navigates to Settings → Authentication & Security
2. System displays current authentication throttling configuration:
   - Max Login Attempts: 5
   - Lockout Duration: 15 minutes
   - Last Modified: 2025-10-15 14:23 by <admin@hairline.com>
3. Admin clicks "Edit" button for Authentication Throttling section
4. System displays editable form with current values pre-populated
5. Admin changes "Max Login Attempts" from 5 to 7
6. Admin changes "Lockout Duration" from 15 to 10 minutes
7. Admin clicks "Save Changes"
8. System validates inputs (max attempts 1-10, lockout 5-60 minutes)
9. System opens a modal titled "Change Reason" requiring admin to enter an explanation (10-500 chars). Admin enters: "Reducing lockout to improve user experience based on support ticket analysis" and confirms.
10. System creates audit log entry:
    - Timestamp: 2025-11-04 10:45:22
    - Admin: <admin@hairline.com> (ID: A-12345)
    - Setting Group: Authentication Throttling
    - Old Values: {max_attempts: 5, lockout_minutes: 15}
    - New Values: {max_attempts: 7, lockout_minutes: 10}
    - Reason: "Reducing lockout to improve user experience based on support ticket analysis"
11. System increments version number (v1.2 → v1.3)
12. System saves new configuration to database
13. System invalidates settings cache
14. System displays success message: "Authentication throttling updated successfully (v1.3)"
15. Within 60 seconds, Patient Platform and Provider Platform poll settings API and receive updated throttling policy
16. New login attempts on Patient and Provider platforms immediately apply new throttling rules (7 attempts, 10-minute lockout)

### Alternative Flows

**A1: Admin Edits Centrally Managed Country List**:

- **Trigger**: Admin needs to add new country to support expanded patient base
- **Steps**:
  1. Admin navigates to Settings → App Data → Countries & Calling Codes
  2. System displays current list of countries with calling codes
  3. Admin clicks "Add Country"
  4. Admin enters country name "Albania", calling code "+355", ISO code "AL"
  5. Admin clicks "Save"
  6. System opens a modal titled "Change Reason" requiring admin to enter an explanation (10-500 chars). Admin enters: "Expanding service to Albanian market" and confirms.
  7. System validates country code uniqueness
  8. System creates audit log and versions change
  9. Within 1 minute, Patient app profile forms display "Albania" in country dropdown
- **Outcome**: New country available in all patient/provider profile forms

**A2: Admin Edits OTP Email Template**:

- **Trigger**: Marketing team requests updated branding in verification emails
- **Steps**:
  1. Admin navigates to Settings → Notifications → OTP Email Templates
  2. System displays list of templates (Verification Email, Password Reset Email)
  3. Admin selects "Verification Email" template
  4. System displays template editor with current HTML/text content and available variables
  5. Admin modifies email copy, adds new branding elements
  6. Admin uses "Preview" button to see rendered email with sample data
  7. Admin clicks "Save"
  8. System opens a modal titled "Change Reason" requiring admin to enter an explanation (10-500 chars). Admin enters: "Updated branding per marketing guidelines Q4 2025" and confirms.
  9. System versions template (v2.1 → v2.2)
  10. System creates audit log
  11. New OTP generation requests use v2.2 template
  12. Users already in verification flow continue using v2.1 template (no disruption)

- **Outcome**: New verification emails reflect updated branding

**A3: Admin Edits Discovery Question Options**:

- **Trigger**: Admin identifies new traffic source that should be tracked
- **Steps**:
  1. Admin navigates to Settings → App Data → Discovery Questions
  2. System displays current options: "Social Media", "Search Engine", "Friend Referral", "Online Ad"
  3. Admin clicks "Add Option"
  4. Admin enters new option: "Medical Tourism Forum"
  5. Admin uses drag-and-drop to reorder options (priority ranking)
  6. Admin clicks "Save"
  7. System opens a modal titled "Change Reason" requiring admin to enter an explanation (10-500 chars). Admin enters: "Tracking new traffic source from medical tourism forums" and confirms.
  8. System versions discovery questions (v1.4 → v1.5)
  9. Within 1 minute, Patient app registration form displays new option

- **Outcome**: Patients see updated discovery question options during registration

**B1: Admin Attempts Invalid Configuration**:

- **Trigger**: Admin enters out-of-range value for authentication throttling
- **Steps**:
  1. Admin attempts to set "Max Login Attempts" to 0
  2. System validates input and detects violation (valid range: 1-10)
  3. System displays error message: "Max Login Attempts must be between 1 and 10"
  4. Admin corrects value to 3
  5. System re-validates and accepts change
  6. Normal flow continues
- **Outcome**: Invalid configurations prevented before save

**B2: Settings Propagation Failure**:

- **Trigger**: Patient Platform fails to retrieve updated settings due to network issue
- **Steps**:
  1. Admin successfully updates authentication throttling
  2. Patient Platform attempts to poll settings API but network timeout occurs
  3. Patient Platform logs error and continues using cached settings
  4. Patient Platform retries poll on next scheduled interval (60 seconds)
  5. On successful retry, Patient Platform receives updated settings and applies them
  6. System logs propagation delay but does not alert (self-healing)
- **Outcome**: Settings eventually consistent across all platforms (within 1 minute of successful retry)

---

## Screen Specifications

### Screen 1: Settings Management Dashboard

**Purpose**: Provides overview of all setting groups with quick access to edit interfaces

**Data Fields**:

| Field Name          | Type               | Required | Description                                     | Validation Rules   |
| ------------------- | ------------------ | -------- | ----------------------------------------------- | ------------------ |
| Setting Group Name  | text (read-only)   | N/A      | Name of setting group                           | N/A (display only) |
| Current Version     | text (read-only)   | N/A      | Current version number (e.g., "v1.3")           | N/A (display only) |
| Last Modified       | datetime (read-only) | N/A      | Timestamp of last change                        | N/A (display only) |
| Modified By         | text (read-only)   | N/A      | Admin email who made last change                | N/A (display only) |
| Quick Actions       | button group       | N/A      | Edit, View History                              | N/A                |

**Business Rules**:

- Only admins with "Settings Management" permission can access this screen
- Setting groups are organized into sections: Authentication & Security, App Data, Notifications
- "Edit" button disabled for setting groups marked as "Fixed in Codebase"
- "View History" always available (read-only)

**Notes**:

- Use card-based layout for setting groups
- Color-code groups by category (blue: security, green: data, yellow: notifications)
- Display warning icon if setting change pending propagation

**Setting Groups (detailed)**:

- Authentication & Security
  - Authentication Throttling (max attempts, lockout duration)
  - OTP Configuration (expiry time, resend limits; code length is fixed, view-only)
  - Password Policy (fixed in codebase, view-only)
- App Data
  - Countries & Calling Codes (name, ISO code, calling code, flag, order, active)
  - Discovery Questions (answer options, order, active)
- Notifications
  - OTP Email Templates
    - Verification Email
    - Password Reset Email

---

### Screen 2: Authentication Throttling Editor

**Purpose**: Allows admin to configure login attempt limits and lockout duration

**Data Fields**:

| Field Name          | Type     | Required | Description                                         | Validation Rules                   |
| ------------------- | -------- | -------- | --------------------------------------------------- | ---------------------------------- |
| Max Login Attempts  | number   | Yes      | Maximum failed login attempts before lockout        | Range: 1-10, integer only          |
| Lockout Duration    | number   | Yes      | Lockout duration in minutes                         | Range: 5-60, integer only          |

**Business Rules**:

- Changes apply immediately upon save (no staging)
- Existing locked-out users continue to serve existing lockout duration (no retroactive changes)
- New login attempts apply new throttling policy immediately after propagation

**Notes**:

- Display current values prominently before edit
- Show preview of impact: "Users will be locked out after X failed attempts for Y minutes"
- Display warning if reducing security (e.g., increasing attempts or reducing lockout)
- On save, a modal prompts for the mandatory change reason (10-500 chars)

---

### Screen 3: OTP Configuration Editor

**Purpose**: Allows admin to configure global OTP expiry time (shared across verification and password reset flows) and resend rate limits

**Data Fields**:

| Field Name           | Type               | Required | Description                                    | Validation Rules               |
| -------------------- | ------------------ | -------- | ---------------------------------------------- | ------------------------------ |
| OTP Code Length      | number (read-only) | N/A      | Length of OTP code (FIXED at 6)                | FIXED (not editable)           |
| OTP Expiry Time      | number             | Yes      | OTP code expiry in minutes (applies to ALL OTP flows: email verification and password reset) | Range: 5-30, integer only      |
| Resend Cooldown      | number             | Yes      | Minimum seconds between OTP resend requests    | Range: 30-300, integer only    |
| Max Resend Attempts  | number             | Yes      | Maximum OTP resend requests per hour           | Range: 3-10, integer only      |

**Business Rules**:

- OTP length is FIXED at 6 digits in codebase (not editable)
- Single global OTP expiry: the configured `OTP Expiry Time` applies uniformly to **both** email verification and password reset OTP flows (no separate per-flow expiry)
- Default OTP expiry: 15 minutes
- Default resend cooldown: 60 seconds
- Default max resend attempts: 5 per hour
- Changes apply only to NEW OTP generation requests
- Existing OTP codes in users' inboxes retain original expiry time

**Rate Limiting Interaction Logic**:

The system enforces BOTH constraints simultaneously (whichever is more restrictive applies):

1. **Cooldown Constraint**: User must wait at least `Resend Cooldown` seconds between consecutive resend requests
2. **Hourly Limit Constraint**: User cannot exceed `Max Resend Attempts` resend requests within a 1-hour rolling window

**Logic**: User can resend OTP IF AND ONLY IF:

- Cooldown period has elapsed since last resend (e.g., ≥60 seconds) AND
- Hourly limit not exceeded (e.g., <5 attempts in last 60 minutes)

**Examples**:

- **Scenario 1**: Cooldown = 60s, Max = 5/hour
  - User can resend approximately every 60 seconds, up to 5 times per hour
  - If user sends 5 times in 5 minutes (60s apart), 6th request blocked until 60 minutes elapsed from 1st request

- **Scenario 2**: Cooldown = 30s, Max = 10/hour
  - User can resend approximately every 30 seconds, up to 10 times per hour
  - If user sends 10 times in 5 minutes (30s apart), 11th request blocked until 60 minutes elapsed from 1st request

- **Scenario 3**: Cooldown = 300s (5 min), Max = 10/hour
  - User can resend approximately every 5 minutes
  - Hourly limit theoretically allows 12 requests (60min ÷ 5min), but max enforced at 10
  - Cooldown is more restrictive, effectively limiting to ~10-12 requests per hour

**Counter Reset Logic**:

- **Rolling Window (RECOMMENDED)**: Hourly counter calculated as "number of resend requests in last 60 minutes from current time"
  - Example: User sent OTPs at 10:00, 10:05, 10:10, 10:15, 10:20 (5 requests)
  - At 10:30, user has 5 requests in last 60 min (blocked if max=5)
  - At 11:01, user has 4 requests in last 60 min (10:05, 10:10, 10:15, 10:20) - 10:00 request outside window
  - User can now resend (cooldown satisfied, hourly limit not exceeded)

- **Fixed Window (NOT RECOMMENDED)**: Counter resets at exact hourly boundaries (e.g., 10:00, 11:00, 12:00)
  - Issue: User could send 5 at 10:59 and 5 at 11:01 (10 requests in 2 minutes)
  - Creates burst traffic vulnerability

**Implementation**: Use rolling window to prevent burst abuse

**Notes**:

- Display "FIXED" badge next to OTP Code Length field
- Provide tooltip explaining why length is not editable
- Show impact preview: "Users must enter OTP within X minutes of receiving email"
- On save, a modal prompts for the mandatory change reason (10-500 chars)

---

### Screen 4: Country & Calling Code Manager

**Purpose**: Centralized management of countries and calling codes used across all platforms

**Data Fields**:

| Field Name     | Type     | Required | Description                                | Validation Rules                          |
| -------------- | -------- | -------- | ------------------------------------------ | ----------------------------------------- |
| Country Name   | text     | Yes      | Full country name (e.g., "United Kingdom") | Max 100 chars, unique                     |
| ISO Code       | text     | Yes      | ISO 3166-1 alpha-2 code (e.g., "GB")       | Exactly 2 uppercase chars, unique         |
| Calling Code   | text     | Yes      | International calling code (e.g., "+44")   | Format: +[1-4 digits]                     |
| Country Flag   | file     | Yes      | Country flag asset (SVG preferred; PNG fallback) | Types: .svg or .png; Max size: 1 MB; Recommended dimensions: SVG scalable, PNG ≥ 128x128 |
| Display Order  | number   | No       | Sort priority (lower = higher priority)    | Integer, default: 999                     |
| Active         | checkbox | Yes      | Whether country is visible in UI           | Default: true                             |

**Business Rules**:

- Country names must be unique
- ISO codes must be unique and valid per ISO 3166-1 alpha-2 standard
- Calling codes can be duplicated (e.g., USA and Canada both use +1)
- Deactivating country does NOT delete (soft delete, archived)
- Changes propagate to Patient app profile forms within 1 minute
- Drag-and-drop reordering updates Display Order field
- SVG is the preferred format for flags; PNG is allowed only when SVG is not available
- For PNG uploads, enforce minimum resolution of 128x128 and square aspect ratio (1:1)
- Store flag assets in centralized media storage/CDN and reference by URL

**Notes**:

- Provide bulk import capability (CSV upload with validation)
- Display validation errors inline
- Show usage count (how many users have selected this country)
- Warn before deactivating country with active users
- Preview uploaded flag (SVG/PNG) next to country name in list views

---

### Screen 5: Discovery Questions Manager

**Purpose**: Manage "How did you find us?" question options displayed during patient registration

**Data Fields**:

| Field Name     | Type               | Required | Description                                      | Validation Rules            |
| -------------- | ------------------ | -------- | ------------------------------------------------ | --------------------------- |
| Question Text  | text (read-only)   | N/A      | Fixed question: "How did you find out about us?" | FIXED (not editable)        |
| Answer Option  | text               | Yes      | Answer choice (e.g., "Social Media")             | Max 100 chars, unique       |
| Display Order  | number             | No       | Sort priority (lower = displayed first)          | Integer, default: 999       |
| Active         | checkbox           | Yes      | Whether option is visible in UI                  | Default: true               |

**Business Rules**:

- Question text is FIXED ("How did you find out about us?")
- Answer options must be unique
- At least 2 active options must exist at all times
- Deactivating option does NOT delete historical data
- Changes propagate to Patient app within 1 minute
- Drag-and-drop reordering updates Display Order field

**Notes**:

- Provide drag-and-drop reordering UI
- Display usage analytics (how many patients selected each option)
- Warn if deactivating frequently selected option
- Suggest common options when adding new (autocomplete)
- On save, a modal prompts for the mandatory change reason (10-500 chars)

---

### Screen 6: OTP Email Template Editor

**Purpose**: Edit email templates for OTP verification and password reset emails

**Data Fields**:

| Field Name               | Type               | Required | Description                           | Validation Rules                  |
| ------------------------ | ------------------ | -------- | ------------------------------------- | --------------------------------- |
| Template Name            | text (read-only)   | N/A      | Template identifier                   | FIXED (not editable)              |
| Subject Line             | text               | Yes      | Email subject line                    | Max 200 chars                     |
| Email Body (HTML)        | rich text          | Yes      | HTML email content                    | Max 50,000 chars, valid HTML      |
| Email Body (Plain Text)  | textarea           | Yes      | Fallback plain text version           | Max 10,000 chars                  |
| Available Variables      | list (read-only)   | N/A      | {code}, {email}, {expiry_minutes}, {app_name} | Display only          |

**Business Rules**:

- Template name is FIXED (cannot rename templates)
- Subject and body must include {code} variable
- HTML body must be valid (system validates on save)
- Plain text body is fallback for email clients that don't support HTML
- Variables are automatically substituted at send time
- Preview functionality renders sample email with fake data
- Changes apply only to NEW OTP generation requests (existing emails unaffected)

**Notes**:

- **IMPORTANT**: This screen serves BOTH "Verification Email" and "Password Reset Email" templates. Implement a template selector/chooser (dropdown or tabs) at the top of the screen to allow admins to switch between templates without navigating away.
- Provide rich text editor (WYSIWYG) for HTML body
- Provide live preview panel showing rendered email
- Highlight required variables ({code}) in editor
- Provide sample data for preview ({code} = "123456", {expiry_minutes} = "15")
- Warn if {code} variable is missing
- On save, a modal prompts for the mandatory change reason (10-500 chars)

---

### Screen 7: Version History Viewer

**Purpose**: Display complete audit trail of changes for a specific setting group

**Data Fields**:

| Field Name      | Type               | Required | Description                               | Validation Rules   |
| --------------- | ------------------ | -------- | ----------------------------------------- | ------------------ |
| Version Number  | text (read-only)   | N/A      | Version identifier (e.g., "v1.3")         | N/A (display only) |
| Changed On      | datetime (read-only) | N/A      | Timestamp of change                       | N/A (display only) |
| Changed By      | text (read-only)   | N/A      | Admin email who made change               | N/A (display only) |
| Change Type     | text (read-only)   | N/A      | "Update", "Initial"                      | N/A (display only) |
| Old Values      | JSON (read-only)   | N/A      | Previous configuration values             | N/A (display only) |
| New Values      | JSON (read-only)   | N/A      | Updated configuration values              | N/A (display only) |
| Change Reason   | text (read-only)   | N/A      | Admin-provided explanation                | N/A (display only) |
| Actions         | button group       | N/A      | View Details                              | N/A                |

**Business Rules**:

- Version history is immutable (cannot delete or edit)
- Versions displayed in reverse chronological order (newest first)
- Diff view highlights changed fields (old → new)
- Sensitive values (API keys) masked in version history

**Notes**:

- Use diff highlighting (red for removed, green for added)
- Provide search/filter by date range, admin, or change type
- Pagination for long version histories (50 entries per page)

---

## Business Rules

### General Module Rules

- **Rule 1**: All setting changes MUST require a change reason (minimum 10 characters, maximum 500 characters) captured via modal after clicking Save
- **Rule 2**: Setting changes MUST be versioned with auto-incremented version numbers (v1.0, v1.1, v1.2, etc.)
- **Rule 3**: Setting changes MUST propagate to dependent services within 1 minute (60-second polling interval)
- **Rule 4**: Settings cache MUST be invalidated immediately upon save to ensure propagation
- **Rule 5**: All timestamps MUST be stored in UTC and displayed in admin's local timezone

### Data & Privacy Rules

- **Privacy Rule 1**: Sensitive setting values (API keys, secrets, credentials) MUST be masked in UI (display as "••••••••")
- **Privacy Rule 2**: Sensitive values MUST be masked in audit logs (display as "[REDACTED]")
- **Privacy Rule 3**: Full sensitive values MUST be viewable only by admins with "View Sensitive Settings" permission
- **Audit Rule 1**: All setting changes MUST be logged with timestamp, admin ID, admin email, old values, new values, and reason
- **Audit Rule 2**: Audit logs MUST be immutable (no deletion, no editing)
- **Audit Rule 3**: Audit logs MUST be retained for minimum 10 years per compliance requirements
- **GDPR**: Admin activity logs are exempt from GDPR deletion requests (business records, legal requirement)

### Admin Editability Rules

**Editable by Admin**:

- Authentication throttling: max login attempts (range: 1-10), lockout duration (range: 5-60 minutes)
- OTP configuration: expiry time (range: 5-30 minutes), resend cooldown (range: 30-300 seconds), max resend attempts (range: 3-10)
- Country list: add, edit, deactivate countries and calling codes
- Discovery questions: add, edit, deactivate answer options
- OTP email templates: subject line, HTML body, plain text body

**Fixed in Codebase (Not Editable)**:

- Password policy: minimum 12 characters, at least 1 uppercase, 1 lowercase, 1 digit, 1 special character from !@#$%^&(),.?":{}|<>
- OTP code length: FIXED at 6 digits
- Discovery question text: FIXED as "How did you find out about us?"
- Template names: Cannot rename OTP email templates
- Setting group structure: Cannot create new setting groups (predefined)

**Configurable with Restrictions**:

- Admin can deactivate countries but cannot delete (soft delete, archived)
- Admin can deactivate discovery options but must maintain at least 2 active options
- Admin can edit email templates but must include required variables ({code} for OTP templates)

---

## Success Criteria

### Admin Management Metrics

- **SC-001**: Admins can update authentication throttling policy in under 1 minute (from login to save)
- **SC-002**: 100% of setting changes captured with who/when/what-before/what-after audit trail
- **SC-003**: Setting changes propagate to dependent services within ≤ 1 minute (measured from save to consumption)
- **SC-004**: Version history displays complete audit trail for any setting group within 2 seconds

### System Performance Metrics

- **SC-005**: Settings Management Dashboard loads in under 1 second for 95% of requests
- **SC-006**: Setting change save operation completes within 500ms for 95% of requests
- **SC-007**: Version history query returns results in under 1 second for 95% of requests
- **SC-008**: Settings API responds to polling requests in under 200ms for 99% of requests
- **SC-009**: System supports 1,000 concurrent admin users viewing settings without degradation

### Data Integrity Metrics

- **SC-010**: Zero production incidents linked to settings drift after enabling versioning and forward-only changes
- **SC-011**: 100% of setting changes successfully propagate to all dependent services (no data loss)
- **SC-012**: Audit logs capture 100% of changes with no gaps or missing entries

### Security & Compliance Metrics

- **SC-013**: Zero exposure of sensitive setting values (API keys, secrets) in UI or logs
- **SC-014**: 100% of unauthorized access attempts to Settings Management UI are blocked
- **SC-015**: Security scanning shows no exposure of sensitive values in browser console or network requests
- **SC-016**: Compliance audits successfully verify complete audit trail for all configuration changes

### Business Impact Metrics

- **SC-017**: Reduction in code deployments for security policy adjustments by 80% (can adjust via UI instead)
- **SC-018**: Average time to adjust security policy reduced from 2 hours (code deployment) to under 5 minutes (UI change)
- **SC-019**: Zero downtime deployments for security policy changes (previously required app restart)
- **SC-020**: Reduction in support tickets related to configuration errors due to clear audit history and fast forward changes

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **FR-001 / Module P-01: Auth & Profile Management**
  - **Why needed**: P-01 consumes authentication throttling, OTP configuration, country lists, discovery questions
  - **Integration point**: P-01 polls Settings API every 60 seconds to retrieve latest configurations; applies to login flows, OTP verification, profile forms

- **FR-009 / Module PR-01: Auth & Team Management**
  - **Why needed**: PR-01 consumes authentication throttling and OTP configuration for provider login and email verification
  - **Integration point**: PR-01 polls Settings API every 60 seconds to retrieve authentication policies

- **FR-020 / Module S-03: Notification Service**
  - **Why needed**: S-03 consumes OTP email templates for verification and password reset emails
  - **Integration point**: S-03 retrieves template by name via Settings API when generating OTP email; caches template for 1 minute

- **Module S-05: Media Storage Service**
  - **Why needed**: S-05 stores country flag assets (SVG/PNG) uploaded via Country Manager UI
  - **Integration point**: Settings UI uploads flag file to S-05 API, receives URL, and stores URL in country settings

- **FR-024 / Module A-09: Treatment & Package Management**
  - **Why needed**: Treatments are admin-created foundation items managed through Settings UI
  - **Relationship**: FR-024 Part A (Treatments) is admin-configured; admin creates treatments (FUE, FUT, DHI) with name, description, type, video, images, technique details
  - **Integration point**: Treatment management is a submodule of A-09 System Settings & Configuration; shares same Settings Management UI and audit trail
  - **Scope clarification**: FR-026 provides the settings infrastructure; FR-024 implements treatment-specific CRUD operations

- **FR-011 / Module A-03: Aftercare Team Management**
  - **Why needed**: Aftercare milestone templates are admin-created and managed through Settings UI
  - **Relationship**: Aftercare templates (Post-Op Phase, Recovery Phase, Growth Phase, Final Assessment) are admin-configured with milestones, scan frequency, questionnaires, educational resources
  - **Integration point**: Providers select from admin-created templates during treatment completion; templates define complete aftercare plan structure
  - **Scope clarification**: FR-026 provides the settings infrastructure; FR-011 implements aftercare template-specific management

- **Admin Authentication & Authorization Module**
  - **Why needed**: Cannot restrict access to Settings Management UI without authentication and role-based permissions
  - **Required roles**: "Settings Manager" (view + edit all settings), "Settings Viewer" (read-only), "Security Admin" (view sensitive values unmasked)
  - **Required permissions**: "read:settings", "write:settings", "view:sensitive", "edit:auth-policies", "edit:app-data", "edit:templates"
  - **Integration point**: All Settings Management UI screens enforce role checks before allowing access; all API endpoints validate OAuth 2.0 tokens with appropriate scopes

### External Dependencies (APIs, Services)

- **None**: This module has no external dependencies (self-contained within Hairline platform)

### Data Dependencies

- **Entity 1: Admin User Accounts**
  - **Why needed**: Cannot audit changes without admin user identity
  - **Source**: Admin authentication module (A-09 user management)

- **State 1: Role-Based Permissions**
  - **Why needed**: Cannot restrict access to Settings Management UI without permission checks
  - **Source**: Admin permission management (A-09 user & permission management)

---

## Assumptions

### User Behavior Assumptions

- **Assumption 1**: Admins will provide meaningful change reasons (not just "update" or "test")
- **Assumption 2**: Admins will use preview functionality to verify email template changes before saving
- **Assumption 3**: Admins will monitor propagation status after critical changes (e.g., security policy updates)

### Technology Assumptions

- **Assumption 1**: Admin web app accessed via modern browsers (Chrome, Safari, Firefox, Edge - last 2 versions)
- **Assumption 2**: Admins have stable internet connection (not optimized for offline mode)
- **Assumption 3**: Settings database supports ACID transactions (prevent partial updates)
- **Assumption 4**: Dependent services (Patient app, Provider app) can poll Settings API every 60 seconds without performance impact

### Business Process Assumptions

- **Assumption 1**: Settings changes are infrequent (not expected to change hourly or daily)
- **Assumption 2**: Admins have authority to modify security policies without external approval
- **Assumption 3**: 1-minute propagation delay is acceptable for non-critical settings (e.g., discovery questions)
- **Assumption 4**: Security policy changes apply prospectively only (do not retroactively affect locked-out users)

---

## Implementation Notes

### Technical Considerations

- **Architecture**: Settings stored in centralized database with cache layer (Redis recommended) for fast retrieval
- **Versioning**: Implement event sourcing pattern to capture all changes (append-only log)
- **Propagation**: Polling mechanism (pull-based) preferred over webhooks (push-based) for simplicity and reliability
- **Cache Invalidation**: Invalidate cache immediately on save; dependent services detect stale cache via version comparison

### Integration Points

- **Integration 1: Patient Platform → Settings API**
  - **Data format**: JSON response with version number and setting values
  - **Authentication**: OAuth 2.0 bearer token with "read:settings" scope
  - **Error handling**: If API unreachable, Patient Platform continues using cached settings for up to 1 minute, then logs error and retries

- **Integration 2: Notification Service → Settings API (Template Retrieval)**
  - **Data format**: JSON response with template name, subject, HTML body, plain text body, variables
  - **Authentication**: OAuth 2.0 bearer token with "read:settings" scope
  - **Error handling**: If API unreachable, use fallback template (hardcoded default); log error for admin review

- **Integration 3: Admin UI → Settings API (CRUD Operations)**
  - **Data format**: JSON request/response for create, read, update operations
  - **Authentication**: OAuth 2.0 bearer token with "write:settings" scope (restricted to authorized admins)
  - **Error handling**: Display user-friendly error messages for validation failures; retry logic for network timeouts

### Scalability Considerations

- **Current scale**: Expected 10-20 setting changes per week at launch
- **Growth projection**: Minimal growth (settings are finite, not user-generated content)
- **Peak load**: Up to 1,000 concurrent admins viewing settings during incident response
- **Data volume**: Expect 5,000 version history entries per year (assuming 100 changes/week across all settings)
- **Scaling strategy**: Cache frequently accessed settings (countries, discovery questions) in memory; database indexes on version_number and timestamp for fast version history queries

### Security Considerations

- **Authentication**: Multi-factor authentication required for admin access to Settings Management UI
- **Authorization**: Role-based access control (RBAC) enforced:
  - "Settings Manager" role: Can view and edit all settings
  - "Settings Viewer" role: Can view settings and version history (read-only)
  - "Security Admin" role: Can view sensitive values (API keys, secrets) unmasked
- **Encryption**: Sensitive setting values (API keys, secrets) encrypted at rest using AES-256
- **Audit trail**: All admin actions logged with IP address, user agent, timestamp, and change details
- **Rate limiting**: Settings API rate limited to 100 requests/minute per admin to prevent abuse
- **Input validation**: All user inputs sanitized to prevent XSS, SQL injection, command injection
- **HTML Sanitization for Email Templates**:
  - **Sanitization Library**: MUST use DOMPurify (JavaScript) or Bleach (Python) for server-side HTML sanitization
  - **Allowed HTML Tags**: `<p>`, `<br>`, `<a>`, `<strong>`, `<em>`, `<ul>`, `<ol>`, `<li>`, `<h1>`, `<h2>`, `<h3>`, `<h4>`, `<h5>`, `<h6>`, `<img>`, `<table>`, `<tr>`, `<td>`, `<th>`, `<thead>`, `<tbody>`, `<span>`, `<div>`
  - **Allowed HTML Attributes**: `href` (on `<a>` only), `src` (on `<img>` only), `alt` (on `<img>` only), `title`, `class`, `style` (limited to safe CSS properties: color, font-size, font-weight, text-align, padding, margin, background-color)
  - **Prohibited HTML Tags**: `<script>`, `<iframe>`, `<object>`, `<embed>`, `<form>`, `<input>`, `<button>`, `<select>`, `<textarea>`, `<link>`, `<meta>`, `<base>`, `<applet>`, `<audio>`, `<video>`
  - **Prohibited HTML Attributes**: All event handlers (`onclick`, `onerror`, `onload`, `onmouseover`, etc.), `javascript:` in `href`, `data:` URIs in `src`, `formaction`, `srcdoc`
  - **URL Validation**: All `href` and `src` attributes MUST be validated against whitelist of allowed protocols (http://, https://, mailto:) and reject javascript:, data:, vbscript:, file:
  - **CSS Sanitization**: If `style` attribute is allowed, MUST strip dangerous CSS properties (expression, behavior, -moz-binding, import, @import)
  - **Content Security Policy (CSP)**: Template preview iframe MUST render with restrictive CSP headers:
    - `default-src 'none'`
    - `img-src https: data:`
    - `style-src 'unsafe-inline'`
    - `script-src 'none'`
  - **XSS Prevention Test Cases**:
    1. Template containing `<script>alert('XSS')</script>` MUST be sanitized to empty string
    2. Template containing `<img src=x onerror=alert('XSS')>` MUST strip onerror attribute
    3. Template containing `<a href="javascript:alert('XSS')">Click</a>` MUST reject javascript: protocol
    4. Template containing `<div style="background:url('javascript:alert(1)')">` MUST strip dangerous CSS
    5. Template containing `{code}<script>alert(1)</script>` MUST render variable substitution but sanitize script tag
- **Compliance**: Audit logs retained for 10 years per compliance requirements; immutable (no deletion)

### Initial Configuration / Seeding

**Database Seeding Requirements**:

- **Authentication Throttling**:
  - Max Login Attempts: 5
  - Lockout Duration: 15 minutes
- **OTP Configuration**:
  - Expiry Time: 15 minutes
  - Resend Cooldown: 60 seconds
  - Max Resend Attempts: 5 per hour
- **Discovery Questions**:
  - Initial Option 1: "Search Engine" (Order: 1)
  - Initial Option 2: "Social Media" (Order: 2)
  - Initial Option 3: "Friend Recommendation" (Order: 3)
- **Countries**:
  - Minimum initial set: Turkey (TR, +90), UK (GB, +44), USA (US, +1), Germany (DE, +49)
- **Templates**:
  - Default "Verification Email" and "Password Reset Email" templates MUST be seeded with standard branding and variables

---

## User Scenarios & Testing

### User Story 1 - Update Authentication Throttling Policy (Priority: P1)

Admin needs to reduce login attempt lockout from 5 attempts to 7 attempts based on user feedback that current policy is too strict.

**Why this priority**: Critical security configuration that directly impacts user experience; must be adjustable without code deployment.

**Independent Test**: Can be fully tested by: (1) Admin updates throttling policy via UI, (2) Reason modal appears and is submitted, (3) Verify audit log created, (4) Wait 1 minute, (5) Test login with new policy on Patient app, (6) Verify 7 attempts allowed before lockout.

**Acceptance Scenarios**:

1. **Given** admin is logged in and has "Settings Manager" role, **When** admin navigates to Settings → Authentication & Security, **Then** system displays current throttling policy (5 attempts, 15-minute lockout)
2. **Given** admin is editing throttling policy, **When** admin changes max attempts to 7 and clicks Save, then submits the reason modal, **Then** system saves new policy, creates audit log, increments version number
3. **Given** admin saved new throttling policy 30 seconds ago, **When** patient attempts login on Patient app, **Then** new policy (7 attempts) applies immediately
4. **Given** patient makes 6 failed login attempts, **When** patient attempts 7th login, **Then** system allows attempt (does not lock out until 8th attempt)
5. **Given** admin views version history, **When** admin selects version history for authentication throttling, **Then** system displays complete audit trail including admin ID, timestamp, old/new values, and reason

---

### User Story 2 - Edit OTP Email Template (Priority: P1)

Marketing team requests updated branding in OTP verification emails; admin needs to update template without code deployment.

**Why this priority**: Critical communication channel; branding changes are frequent business requirement.

**Independent Test**: Can be fully tested by: (1) Admin edits OTP template via UI, (2) Preview rendered email, (3) Click Save and submit reason modal, (4) Request new OTP on Patient app, (5) Verify email received with new branding.

**Acceptance Scenarios**:

1. **Given** admin is logged in and has "Settings Manager" role, **When** admin navigates to Settings → Notifications → OTP Email Templates, **Then** system displays list of templates (Verification Email, Password Reset Email)
2. **Given** admin selected "Verification Email" template, **When** admin modifies HTML body and clicks "Preview", **Then** system displays rendered email with sample data ({code} = "123456")
3. **Given** admin previewed email and verified branding, **When** admin clicks Save and submits the reason modal, **Then** system versions template, creates audit log
4. **Given** admin saved new template 30 seconds ago, **When** patient requests new OTP on Patient app, **Then** patient receives email with new branding
5. **Given** patient already received OTP before template change, **When** admin saves new template, **Then** patient's existing OTP email remains unchanged (no retroactive changes)

---

### User Story 3 - Add New Country to Centralized List (Priority: P1)

Admin needs to add "Albania" to country list to support expanded patient base in Balkan region.

**Why this priority**: Business expansion requirement; must be updatable without code deployment.

**Independent Test**: Can be fully tested by: (1) Admin adds Albania via UI (including flag upload), (2) Submit reason modal, (3) Wait 1 minute, (4) Open Patient app profile form, (5) Verify "Albania" appears in country dropdown with flag.

**Acceptance Scenarios**:

1. **Given** admin is logged in and has "Settings Manager" role, **When** admin navigates to Settings → App Data → Countries & Calling Codes, **Then** system displays current list of countries
2. **Given** admin clicks "Add Country", **When** admin enters country name "Albania", ISO code "AL", calling code "+355", **Then** system validates uniqueness of name and ISO code
3. **Given** admin entered valid country data and uploaded flag, **When** admin clicks Save and submits the reason modal with "Expanding to Albanian market", **Then** system creates audit log, versions country list
4. **Given** admin saved new country 30 seconds ago, **When** patient opens profile form on Patient app, **Then** "Albania" appears in country dropdown
5. **Given** patient selects "Albania" in country dropdown, **When** patient views phone number field, **Then** calling code defaults to "+355"

---

---

### User Story 4 - Add Discovery Question Option (Priority: P2)

Marketing team identifies new traffic source (medical tourism forums); admin needs to add new discovery question option to track this source.

**Why this priority**: Business intelligence requirement; helps track marketing effectiveness.

**Independent Test**: Can be fully tested by: (1) Admin adds "Medical Tourism Forum" option via UI, (2) Reorder options via drag-and-drop, (3) Wait 1 minute, (4) Patient registers on app, (5) Verify new option appears in discovery question.

**Acceptance Scenarios**:

1. **Given** admin is logged in and has "Settings Manager" role, **When** admin navigates to Settings → App Data → Discovery Questions, **Then** system displays current options (Social Media, Search Engine, Friend Referral, Online Ad)
2. **Given** admin clicks "Add Option", **When** admin enters "Medical Tourism Forum", **Then** system validates option uniqueness
3. **Given** admin added new option, **When** admin uses drag-and-drop to reorder options, **Then** system updates display order (1, 2, 3, 4, 5)
4. **Given** admin saved new option and submitted reason modal with "Tracking forum traffic", **When** patient registers on Patient app 1 minute later, **Then** "Medical Tourism Forum" appears in discovery question dropdown
5. **Given** patient selects "Medical Tourism Forum" during registration, **When** admin views analytics, **Then** selection is tracked and reported in discovery question analytics

---

### User Story 5 - View Version History for Audit Compliance (Priority: P2)

Compliance officer requests complete audit trail of all authentication policy changes for quarterly audit report.

**Why this priority**: Regulatory compliance requirement; demonstrates control over security configurations.

**Independent Test**: Can be fully tested by: (1) Admin makes 5 configuration changes over time, (2) Compliance officer requests audit review, (3) Admin views version history in UI, (4) Verify all changes captured with who/when/what.

**Acceptance Scenarios**:

1. **Given** compliance officer requests audit trail, **When** admin navigates to Settings → Authentication & Security → Authentication Throttling → Version History, **Then** system displays complete version history
2. **Given** version history displayed, **When** admin selects date range filter (Q3 2025), **Then** system displays only versions created in that quarter
3. **Given** version history contains 50+ entries, **When** admin scrolls to bottom of page, **Then** system loads next 50 entries (pagination)
4. **Given** admin views specific version, **When** admin clicks "View Details", **Then** system displays diff view highlighting changed fields (red: removed, green: added)

---

### Edge Cases

- What happens when **admin attempts to deactivate one of the last 2 active discovery question options**? System prevents deactivation and displays error: "At least 2 active options required. Cannot deactivate this option."
- How does system handle **concurrent edits by two admins to same setting group**? System detects concurrent edit before save and displays modal popup: "This setting was updated by [admin email] 30 seconds ago. Your changes may conflict. Review the latest version before saving." Modal shows diff of latest changes and options: "Reload Latest Version" or "Save Anyway (Overwrite)".
- What occurs if **Settings API is unreachable during Patient app polling**? Patient app logs error, continues using cached settings for up to 1 minute, retries poll every 60 seconds.
- How to manage **sensitive value (API key) visibility in version history**? System masks sensitive values in version history UI (display as "[REDACTED]"); admins with "View Sensitive Settings" permission can click "Show" to unmask.
- How does system handle **settings propagation during Patient app deployment**? Settings API remains available during deployments; Patient app retrieves settings after restart; no data loss.
- What occurs if **admin deletes country that active patients have selected in profile**? System prevents hard delete (soft delete only); patients who selected deleted country retain selection; country hidden from new users.

---

## Functional Requirements Summary

### Core Requirements

- **REQ-026-001**: System MUST provide Settings Management UI accessible only to admins with "Settings Manager" or "Settings Viewer" role
- **REQ-026-002**: System MUST require change reason (10-500 characters) for all setting modifications
- **REQ-026-003**: System MUST version all setting changes with auto-incremented version numbers (v1.0, v1.1, v1.2, etc.)
- **REQ-026-004**: System MUST create immutable audit log for every change capturing: timestamp, admin ID, admin email, setting group, old values, new values, change reason
- **REQ-026-005**: System MUST propagate setting changes to dependent services within 1 minute via polling mechanism
- **REQ-026-006**: System MUST invalidate settings cache immediately upon save to trigger propagation
- **REQ-026-007**: System MUST NOT support rollback. Admins make forward-only changes; version history is read-only.
- **REQ-026-008**: System MUST display version history in reverse chronological order with diff highlighting (old → new)

### Data Requirements

- **REQ-026-009**: System MUST store authentication throttling settings: max login attempts (1-10), lockout duration (5-60 minutes)
- **REQ-026-010**: System MUST store OTP configuration: expiry time (5-30 minutes), resend cooldown (30-300 seconds), max resend attempts (3-10)
- **REQ-026-011**: System MUST store centrally managed country list: country name, ISO code, calling code, display order, active status
- **REQ-026-012**: System MUST store centrally managed discovery question options: answer option, display order, active status
- **REQ-026-013**: System MUST store OTP email templates: template name, subject line, HTML body, plain text body, version number

### Security & Privacy Requirements

- **REQ-026-014**: System MUST mask sensitive values (API keys, secrets) in UI and audit logs (display as "••••••••" or "[REDACTED]")
- **REQ-026-015**: System MUST restrict "View Sensitive Settings" permission to authorized admins only
- **REQ-026-016**: System MUST encrypt sensitive values at rest using AES-256
- **REQ-026-017**: Multi-factor authentication for admin access to Settings Management UI is a future (non-MVP) requirement and MUST be enforced once the shared MFA stack (FR-031) is delivered.
- **REQ-026-018**: System MUST rate limit Settings API to 100 requests/minute per admin to prevent abuse
- **REQ-026-019**: System MUST retain audit logs for minimum 10 years per compliance requirements
- **REQ-026-020**: System MUST validate all admin inputs to prevent XSS, SQL injection, command injection attacks

### Integration Requirements

- **REQ-026-021**: System MUST expose Settings API (RESTful) for dependent services to poll configurations
- **REQ-026-022**: Settings API MUST return JSON response with version number, setting values, and last modified timestamp
- **REQ-026-023**: Settings API MUST support OAuth 2.0 authentication with "read:settings" or "write:settings" scopes
- **REQ-026-024**: System MUST NOT expose a rollback API.

---

## Key Entities

- **Entity 1 - Setting Group**: Represents a collection of related settings (e.g., Authentication Throttling, OTP Configuration)
  - **Key attributes**: group_id, group_name, group_category (security/data/notifications), current_version, last_modified, last_modified_by
  - **Relationships**: One Setting Group has many Versions; One Setting Group has many Audit Log Entries

- **Entity 2 - Version**: Represents a specific version of a setting group configuration
  - **Key attributes**: version_id, version_number, setting_group_id, version_data (JSON), created_at, created_by, change_reason, change_type (update/initial)
  - **Relationships**: Many Versions belong to one Setting Group

- **Entity 3 - Audit Log Entry**: Immutable record of a setting change
  - **Key attributes**: log_id, setting_group_id, timestamp, admin_id, admin_email, admin_ip, old_values (JSON), new_values (JSON), change_reason
  - **Relationships**: Many Audit Log Entries belong to one Setting Group; Many Audit Log Entries belong to one Admin

- **Entity 4 - Country**: Centrally managed country data
  - **Key attributes**: country_id, country_name, iso_code, calling_code, display_order, active, created_at, updated_at
  - **Relationships**: Referenced by Patient profiles, Provider profiles

- **Entity 5 - Discovery Question Option**: Centrally managed discovery question answer choices
  - **Key attributes**: option_id, option_text, display_order, active, usage_count, created_at, updated_at
  - **Relationships**: Referenced by Patient registration data

- **Entity 6 - Email Template**: OTP email template configuration
  - **Key attributes**: template_id, template_name, subject_line, html_body, plain_text_body, version_number, required_variables (JSON), created_at, updated_at
  - **Relationships**: One Template has many Versions; Consumed by Notification Service (S-03)

---

## Appendix: Change Log

| Date       | Version | Changes                                 | Author       |
| ---------- | ------- | --------------------------------------- | ------------ |
| 2025-11-04 | 1.0     | Initial PRD creation                    | AI Assistant |
| 2025-12-11 | 1.1     | Verified status, approvals, footer update | AI Assistant |

---

## Appendix: Approvals

| Role           | Name                     | Date       | Signature/Approval |
| -------------- | ------------------------ | ---------- | ------------------ |
| Product Owner  | Hairline Product Owner   | 2025-12-11 | ✅ Approved         |
| Technical Lead | Hairline Technical Lead  | 2025-12-11 | ✅ Approved         |
| Security Lead  | Hairline Security Lead   | 2025-12-11 | ✅ Approved         |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (PRD Standards & Requirements)
**Based on**: FR-011 Aftercare & Recovery Management PRD, FR-026 from system-prd.md
**Last Updated**: 2025-12-11
