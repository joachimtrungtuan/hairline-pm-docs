# FR-026 - App Settings & Security Policies

**Module**: A-09: System Settings & Configuration
**Feature Branch**: `fr026-app-settings-security`
**Created**: 2025-11-04
**Status**: 🟡 Revised — Pending Consolidated Verification
**Source**: FR-026 from system-prd.md, Client transcription (Hairline-AdminPlatformPart2.txt)

---

## Executive Summary

The App Settings & Security Policies module provides a centralized, audited, and versioned configuration surface for application-wide settings, security policies, app data lists, and notification templates that affect multiple modules and tenants (Patient, Provider, Admin). This module is the single source of truth for critical system configurations including authentication throttling, OTP parameters, centrally managed lists (countries, discovery questions), and notification templates.

**Problem**: Currently, settings are scattered across different modules, making it difficult to maintain consistency, audit changes, or roll back problematic configurations. Security policies like authentication throttling and OTP expiry are hardcoded, preventing operational flexibility.

**Solution**: A unified admin interface where authorized administrators can view, create, update, and version settings within clearly defined groups (Authentication & Security, App Data, Notifications, Analytics). All changes require a reason and are fully auditable (who/when/old value/new value).

**Value Delivered**:

- **Operational Efficiency**: Admins can adjust security policies without code deployments
- **Auditability**: Complete audit trail of all configuration changes
- **Consistency**: Single source of truth for settings consumed by Patient, Provider, and Admin platforms
- **Risk Mitigation**: Ability to rapidly adjust configurations forward-only (no rollback) with a complete audit trail
- **Compliance**: Demonstrated control over security parameters for audits

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-01)**: Consumes authentication policies, OTP configurations, country/calling code lists, discovery question options, inquiry cancellation reason options, account deletion reason options, the re-verification threshold, the landing background, and the profile photo limits (REQ-026-040)
- **Provider Platform (PR-06 and PR-02)**: Consumes centrally managed profile lists and the versioned Quote Configuration (quote currency, quote expiry window, and quote-expiring-soon lead time) (REQ-026-040)
- **Quote Acceptance and Booking (FR-005 and FR-006)**: Consume the versioned slot-hold duration and the hold-expiring-soon reminder lead time from the Quote Configuration (REQ-026-040)
- **Admin Platform (A-09)**: Primary interface for viewing, editing, and versioning all settings (REQ-026-040)
- **Admin Platform (A-02)**: FR-015 provider creation (Screen 2 Step 2) and provider profile editing (Screen 3 Tab 1) consume the centrally managed Provider Specialties list (REQ-026-040)
- **Analytics (PR-05 and A-08)**: FR-014 provider and admin analytics consume the versioned Analytics Configuration (SLA target, engagement thresholds, outlier threshold, benchmark refresh frequency, optional commission target) (REQ-026-040)
- **Shared Services (S-03)**: Notification Service consumes OTP email templates for delivery (REQ-026-040)

### Multi-Tenant Breakdown

**Patient Platform (P-01)**:

- Patient registration and login flows apply authentication throttling policies (REQ-026-041)
- OTP verification for email confirmation applies OTP expiry and resend cooldown (REQ-026-041)
- Profile forms use centrally managed country and calling code lists (REQ-026-041)
- Discovery questions ("How did you find us?") display options from centralized list (REQ-026-041)
- Changes to settings propagate to patient app within 1 minute (REQ-026-005)

**Provider Platform (PR-06, PR-01 & PR-02)**:

- Provider staff management (PR-06) indirectly uses centrally managed lists (REQ-026-042)
- Authentication throttling (PR-01) applies to provider login attempts (REQ-026-042)
- OTP parameters (PR-01) apply to provider email verification flows (REQ-026-042)
- Quote creation (PR-02) consumes the quote currency, quote expiry window, and quote-expiring-soon lead time from one configuration version; FR-004 copies the currency and expiry window read-only onto each quote at first send (REQ-026-026, REQ-026-037)

**Admin Platform (A-09)**:

- Admins access Settings Management UI to view and edit configurations
- All changes require reason entry and are logged with timestamp, admin ID, old value, new value (REQ-026-002, REQ-026-004)
- Version history displays for each setting group
- Rollback capability is not supported; admins make forward-only changes (REQ-026-007)
- Role-based access uses the FR-031 permissions View Settings and Edit Settings (Super Admin only), with narrower edit permissions for some screens (REQ-026-015, REQ-026-054)
- Sensitive values (API keys, secrets) are masked in UI and logs (REQ-026-014)

**Admin Platform (A-02)**:

- FR-015 provider creation wizard (Screen 2 Step 2) populates the required Specialty select from the active Provider Specialties list (REQ-026-039)
- FR-015 provider profile editing (Screen 3 Tab 1) uses the same list; a provider's stored specialty still displays after that value is deactivated (REQ-026-039)

**Shared Services (S-03)**:

- Notification Service reads OTP email templates for verification and password reset emails
- Template changes do NOT affect users already in a flow (existing OTP emails remain unchanged) (REQ-026-106)
- New template versions apply only to new OTP generation requests (REQ-026-106)

### Communication Structure

**In Scope**:

- Admin editing OTP email templates (verification, password reset)
- Template preview functionality (REQ-026-105)
- Template variable substitution ({code}, {email}, {expiry_minutes}, {app_name}) (REQ-026-104)

**Out of Scope**:

- Actual email sending (handled by S-03: Notification Service) (REQ-026-043)
- SMS notifications (future enhancement, V2) (REQ-026-043)
- Push notification templates (handled separately in notification preferences module) (REQ-026-043)
- Legal content management (see FR-027: Terms & Conditions, Privacy Policy, Consent forms) (REQ-026-043)
- Regional configuration and pricing (see FR-028: Location presentation, starting prices by currency) (REQ-026-043)
- Payment system configuration (see FR-029: Stripe account management, conversion rates, split payment rules) (REQ-026-043)
- Notification rules and event-based triggers (see FR-030: Event-to-notification mapping, channel configuration) (REQ-026-043)
- Admin access control and role-based permissions (see FR-031: Role management, permission matrix) (REQ-026-043)

### Entry Points

**Admin-Initiated**:

- Admin navigates to Settings → Authentication & Security to edit throttling policies (REQ-026-044)
- Admin navigates to Settings → App Data to manage country lists, discovery questions, inquiry cancellation reasons, account deletion reasons, provider specialties, inquiry configuration, or quote configuration (REQ-026-044)
- Admin navigates to Settings → Notifications to edit OTP email templates (REQ-026-044)
- Admin edits the platform Settings on Screen 8 (Platform Settings Editor), each under its own setting group on Screen 1
- Admin navigates to Settings → Analytics to edit analytics configuration consumed by FR-014 (REQ-026-044)

**System-Triggered**:

- Settings cache refresh occurs automatically every 60 seconds (REQ-026-005)
- Dependent services (Patient app, Provider app, Notification service) poll for setting changes (REQ-026-005)
- Version history automatically captures changes on save (REQ-026-003)

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
  4. Admin enters country name "Albania", calling code "+355", ISO code "AL" and uploads the Albanian flag as an SVG file; System checks the file type and size before Save (REQ-026-122)
  5. Admin clicks "Save"
  6. System opens a modal titled "Change Reason" requiring admin to enter an explanation (10-500 chars). Admin enters: "Expanding service to Albanian market" and confirms.
  7. System validates ISO code uniqueness
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
  12. Codes and emails already sent keep v2.1 and their original expiry (no disruption); a resend is a new code and uses v2.2 (REQ-026-106)

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

**A4: Admin Edits Inquiry Cancellation Reasons**:

- **Trigger**: Product team identifies need to add, reorder, or deactivate cancellation reason options for the patient inquiry cancellation flow (FR-003 Workflow 5)
- **Steps**:
  1. Admin navigates to Settings → App Data → Inquiry Cancellation Reasons
  2. System displays current active reasons: "Changed my mind", "Found a better option elsewhere", "Medical concerns", "Financial reasons", "Travel restrictions", "Timeline doesn't work", "Other"
  3. Admin clicks "Add Reason" and enters: "Provider communication issues"
  4. Admin toggles "Requires Explanation" to Yes (patient must provide free text when selecting this reason)
  5. Admin uses drag-and-drop to reorder reasons (priority ranking)
  6. Admin clicks "Save"
  7. System opens a modal titled "Change Reason" requiring admin to enter an explanation (10-500 chars). Admin enters: "Adding new cancellation tracking category from patient feedback" and confirms.
  8. System versions cancellation reasons list (v1.0 → v1.1)
  9. Within 1 minute, Patient app cancellation modal (FR-003 Screen 8a) displays updated reason options

- **Outcome**: Patients see updated cancellation reason options when cancelling an inquiry

**A5: Admin Edits Account Deletion Reasons**:

- **Trigger**: Product team identifies need to add, reorder, or deactivate deletion reason options for the patient account deletion flow (FR-001 Screen 16)
- **Steps**:
  1. Admin navigates to Settings → App Data → Account Deletion Reasons
  2. System displays current active reasons: "I no longer use this app", "I found a better alternative", "The app doesn't meet my needs", "Too many notifications or emails", "Concerns about privacy or data security", "I had technical issues or bugs", "The app is difficult to use", "I'm taking a break and may return later", "Others"
  3. Admin clicks "Add Reason" and enters: "Dissatisfied with support"
  4. Admin toggles "Requires Explanation" to Yes (patient may provide free text when selecting this reason)
  5. Admin uses drag-and-drop to reorder reasons (priority ranking)
  6. Admin clicks "Save"
  7. System opens a modal titled "Change Reason" requiring admin to enter an explanation (10-500 chars). Admin enters: "Adding new deletion tracking category from patient feedback" and confirms.
  8. System versions deletion reasons list (v1.0 → v1.1)
  9. Within 1 minute, Patient app deletion screen (FR-001 Screen 16) displays updated reason options

- **Outcome**: Patients see updated account deletion reason options when requesting account deletion

**A6: Admin Configures Inquiry Treatment Areas and Lead Time**:

- **Trigger**: Product team needs to add or retire an inquiry treatment-area choice, change its image/icon, or adjust how many days patients must wait before a preferred treatment date.
- **Steps**:
  1. Admin navigates to Settings → App Data → Inquiry Configuration.
  2. Admin adds, edits, reorders, activates, or deactivates a treatment-area option. Each option has a label and an image/icon asset.
  3. Admin sets Minimum Inquiry Lead Time in whole days. The current default is 3 days.
  4. Admin clicks Save and supplies the required change reason.
  5. System validates that active option labels are unique, an image/icon asset is present, and lead time is between 0 and 730 days.
  6. System versions and audits the change, invalidates configuration caches, and exposes the active catalog and lead-time value through the patient configuration API.
  7. New inquiry sessions receive the new configuration within one minute; submitted inquiries retain their historical treatment-area snapshot.

- **Outcome**: Admin can change future inquiry options and the date blocked window without a code change. Implementation must confirm the patient client consumes the dynamic response before treating ordinary configuration changes as release-free.

**A7: Admin Configures Quote and Slot-Hold Settings**:

- **Trigger**: Product team needs to change the quote expiry window, the quote-expiring-soon lead time, the slot-hold duration, or the hold-expiring-soon reminder lead time.
- **Steps**:
  1. Admin navigates to Settings → App Data → Quote Configuration.
  2. Admin sees the quote currency as a read-only value. It is the FR-029 Default Currency and can be changed only in FR-029 Screen 6. Each Default Currency change in FR-029 creates a new Quote Configuration version.
  3. Admin enters whole-number hours for the quote expiry window (default 48), the quote-expiring-soon lead time (default 12), the slot-hold duration (default 48), and the hold-expiring-soon lead time (default 12).
  4. Admin saves with a mandatory change reason.
  5. System checks that the quote expiry window is 24 to 336 hours, the slot-hold duration is 24 to 168 hours, and each lead time is at least 1 hour and at most half of the window it warns about, then versions and audits the change, invalidates the configuration cache, and exposes the active values and configuration version through the authenticated Settings API.
  6. When a provider first sends a parent Quote, FR-004 copies the quote currency and the quote expiry window read-only onto it and records the configuration version used. Drafts carry neither value. Later setting changes never affect a sent quote, and there is no per-quote extension except the admin restore of an expired quote (REQ-004-105) and the admin-authored replacement quote (REQ-004-036).
  7. When a patient accepts a subquote, FR-005 and FR-006 place one fixed slot hold for the slot-hold duration in effect at acceptance. Later setting changes never alter an existing hold, and payment failure never extends or restarts it.
- **Outcome**: Quotes and slot holds use one auditable configuration source without retroactively changing sent quotes or existing holds.

**A8: Admin Configures Analytics Parameters**:

- **Trigger**: Product or operations team needs to change a threshold or target used by FR-014 analytics.
- **Steps**:
  1. Admin navigates to Settings → Analytics → Analytics Configuration.
  2. Admin edits one or more values: TTFQ SLA target (minutes), At Risk and Dormant thresholds (days), price outlier threshold (%), benchmark refresh frequency, and optional target monthly commission.
  3. System validates the values (for example, Dormant must be greater than At Risk) and blocks save on error.
  4. Admin saves with a mandatory change reason.
  5. System versions and audits the change, invalidates the configuration cache, and exposes the active values through the authenticated Settings API.
  6. FR-014 applies the active version at its next calculation or benchmark refresh and records the configuration version used with its aggregates.
- **Outcome**: Analytics thresholds and targets change without a code release, from one auditable source. Exports and scheduled-export files that were already generated are not rewritten.

**A9: Admin Edits Provider Specialties**:

- **Trigger**: Admin needs to add, rename, reorder, or retire a specialty value offered when creating or editing a provider (FR-015)
- **Steps**:
  1. Admin navigates to Settings → App Data → Provider Specialties
  2. System displays the current list: "Hair Transplant Surgeon", "Dermatologist", "Trichologist", "Plastic Surgeon", "Other", with active status and display order
  3. Admin clicks "Add Specialty" and enters: "Hair Restoration Physician"; or renames, reorders (drag-and-drop), or deactivates an existing value
  4. Admin clicks "Save"
  5. System validates that names are unique (case-insensitive), at most 100 characters, and that at least one value remains active
  6. System opens a modal titled "Change Reason" requiring admin to enter an explanation (10-500 chars). Admin enters: "Adding specialty requested by provider onboarding team" and confirms.
  7. System versions the list (v1.0 → v1.1), creates an audit log entry, and invalidates the settings cache
  8. Within 1 minute, the FR-015 Specialty select (Screen 2 Step 2, Screen 3 Tab 1) shows only active values in display order; renamed values show the new name everywhere, including on existing provider profiles
- **Outcome**: Admin controls the specialty values offered for new and edited providers without a code release. Deactivated values are no longer selectable, but providers that already hold them keep and still display them.

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

| Field Name          | Type               | Required | Description                                     | Validation Rules   | Graph field |
| ------------------- | ------------------ | -------- | ----------------------------------------------- | ------------------ | --- |
| Setting Group Name  | text (read-only)   | N/A      | Name of setting group                           | N/A (display only) | ENT-setting-group.group_name |
| Current Version     | text (read-only)   | N/A      | Current version number (e.g., "v1.3")           | N/A (display only) | ENT-setting-group.current_version |
| Last Modified       | datetime (read-only) | N/A      | Timestamp of last change                        | N/A (display only) | ENT-setting-group.last_modified |
| Modified By         | text (read-only)   | N/A      | Admin email who made last change                | N/A (display only) | ENT-setting-group.last_modified_by |
| Quick Actions       | button group       | N/A      | Edit, View History                              | N/A | no graph field (control) |

**Business Rules**:

- Only admins with the View Settings permission can open the Settings screens; each screen's edit permission is in the table under Security Controls (REQ-026-001)
- Setting groups are organized into sections: Authentication & Security, App Data, Notifications, Analytics (REQ-026-108)
- "Edit" button disabled for setting groups marked as "Fixed in Codebase" (REQ-026-109)
- "View History" always available (read-only) (REQ-026-110)

**Notes**:

- Use card-based layout for setting groups
- Color-code groups by category (blue: security, green: data, yellow: notifications, purple: analytics)
- Display warning icon if setting change pending propagation (REQ-026-137)

**Setting Groups (detailed)**:

- Authentication & Security
  - Authentication Throttling (max attempts, lockout duration)
  - OTP Configuration (expiry time, resend limits; code length is fixed, view-only)
  - Password Policy (fixed in codebase, view-only)
  - Re-Verification Threshold and Admin Session Policy (concurrent sessions, inactivity timeout), edited on Screen 8
- App Data
  - Countries & Calling Codes (name, ISO code, calling code, flag, order, active)
  - Discovery Questions (answer options, order, active)
  - Inquiry Cancellation Reasons (reason label, order, requires_explanation, active)
  - Account Deletion Reasons (reason label, requires_explanation, display order, active)
  - Provider Specialties (specialty name, display order, active)
  - Inquiry Configuration (treatment-area options with image/icon assets, and minimum inquiry lead time)
  - Quote Configuration (quote currency shown read-only from FR-029, quote expiry window, quote-expiring-soon lead time, slot-hold duration, hold-expiring-soon lead time)
  - Platform Settings edited on Screen 8: landing background, profile photo limits, head scan quality minimums, acceptance terms text, timezone options, support emergency contact, limits owned by other features (discovery source options are the Discovery Questions answer options, Screen 5)
- Notifications
  - OTP Email Templates
    - Verification Email
    - Password Reset Email
  - Provider Notification Types, edited on Screen 8
- Analytics
  - Analytics Configuration (TTFQ SLA target, engagement thresholds, price outlier threshold, benchmark refresh frequency, optional target monthly commission)

---

### Screen 2: Authentication Throttling Editor

**Purpose**: Allows admin to configure login attempt limits and lockout duration

**Data Fields**:

| Field Name          | Type     | Required | Description                                         | Validation Rules                   | Graph field |
| ------------------- | -------- | -------- | --------------------------------------------------- | ---------------------------------- | --- |
| Max Login Attempts  | number   | Yes      | Maximum failed login attempts before lockout; one shared setting for patients, providers and admins | Range: 1-10, integer only (REQ-026-009) | ENT-auth-throttling-policy.max_login_attempts |
| Lockout Duration    | number   | Yes      | Lockout duration in minutes                         | Range: 5-60, integer only (REQ-026-009) | ENT-auth-throttling-policy.lockout_duration_minutes |

**Business Rules**:

- Changes apply upon save (no staging), within 60 seconds of saving (propagation) (REQ-026-070)
- Existing locked-out users continue to serve existing lockout duration (no retroactive changes) (REQ-026-071)
- New login attempts apply new throttling policy after propagation (REQ-026-070)
- One failed-attempt counter is kept per account and is shared by sign-in and verification-code entry, so a wrong password and a wrong code count together (REQ-001-180). It returns to zero after a successful sign-in or code entry and when a lockout ends. A lowered Max Login Attempts applies from the next failed attempt: an account already at or above the new limit locks on its next failure, and saving the setting locks nobody (REQ-026-145)
- The shared Max Login Attempts lockout also applies to admin sign-in, together with the fixed admin endpoint throttle of 5 attempts per 15 minutes (REQ-031-100); whichever trips first applies (REQ-026-116)

**Notes**:

- Display current values prominently before edit
- Show preview of impact: "Users will be locked out after X failed attempts for Y minutes" (REQ-026-135)
- Display warning if reducing security (e.g., increasing attempts or reducing lockout) (REQ-026-132)
- On save, a modal prompts for the mandatory change reason (10-500 chars) (REQ-026-002)

---

### Screen 3: OTP Configuration Editor

**Purpose**: Allows admin to configure global OTP expiry time (shared across verification and password reset flows) and resend rate limits

**Data Fields**:

| Field Name           | Type               | Required | Description                                    | Validation Rules               | Graph field |
| -------------------- | ------------------ | -------- | ---------------------------------------------- | ------------------------------ | --- |
| OTP Code Length      | number (read-only) | N/A      | Length of OTP code (FIXED at 6)                | FIXED (not editable) (REQ-026-060) | ENT-otp-configuration.otp_code_length |
| OTP Expiry Time      | number             | Yes      | OTP code expiry in minutes (governs registration email verification and password reset; re-verification and email-change codes follow FR-001 and are outside this setting) | Range: 5-30, integer only (REQ-026-010, REQ-026-072) | ENT-otp-configuration.otp_expiry_minutes |
| Resend Cooldown      | number             | Yes      | Minimum seconds between OTP resend requests    | Range: 30-300, integer only (REQ-026-010) | ENT-otp-configuration.resend_cooldown_seconds |
| Max Resend Attempts  | number             | Yes      | Maximum OTP resend requests per rolling 60 minutes | Range: 3-10, integer only (REQ-026-010) | ENT-otp-configuration.max_resend_attempts_per_hour |

**Business Rules**:

- OTP length is FIXED at 6 digits in codebase (not editable) (REQ-026-060)
- Single global OTP expiry: the configured `OTP Expiry Time` applies uniformly to **both** registration email verification and password reset OTP flows (no separate per-flow expiry) (REQ-026-072)
- Re-verification and email-change codes follow FR-001 (fixed 15 minutes, REQ-001-098), are outside this setting, and are sent with the email verification template (REQ-026-072)
- In the email, `{expiry_minutes}` is the lifetime of the code being sent: the OTP Expiry Time for registration verification and password reset, the fixed 15 minutes for re-verification and email-change codes (REQ-026-072)
- Default OTP expiry: 15 minutes
- Default resend cooldown: 60 seconds
- Default max resend attempts: 5 per rolling 60 minutes
- Changes apply only to NEW OTP generation requests (REQ-026-073)
- Existing OTP codes in users' inboxes retain original expiry time; a resend always issues a new code under the expiry value in force at the moment of the resend (REQ-026-073)

**Rate Limiting Interaction Logic**:

The system enforces BOTH constraints simultaneously (whichever is more restrictive applies): (REQ-026-074)

1. **Cooldown Constraint**: User must wait at least `Resend Cooldown` seconds between consecutive resend requests
2. **Hourly Limit Constraint**: User cannot exceed `Max Resend Attempts` resend requests within a 1-hour rolling window

**Logic**: User can resend OTP IF AND ONLY IF: (REQ-026-074)

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
  - Cooldown alone would allow 12 requests per hour, so the hourly limit applies: up to 10 requests per hour

**Counter Reset Logic**:

- **Rolling Window**: Hourly counter calculated as "number of resend requests in last 60 minutes from current time" (REQ-026-075)
  - Example: User sent OTPs at 10:00, 10:05, 10:10, 10:15, 10:20 (5 requests)
  - At 10:30, user has 5 requests in last 60 min (blocked if max=5)
  - At 11:01, user has 4 requests in last 60 min (10:05, 10:10, 10:15, 10:20) - 10:00 request outside window
  - User can now resend (cooldown satisfied, hourly limit not exceeded)

- **Fixed Window (not used)**: Counter resets at exact hourly boundaries (e.g., 10:00, 11:00, 12:00) (REQ-026-075)
  - Issue: User could send 5 at 10:59 and 5 at 11:01 (10 requests in 2 minutes)
  - Creates burst traffic vulnerability

**Implementation**: Use rolling window to prevent burst abuse (REQ-026-075)

**Notes**:

- Display "FIXED" badge next to OTP Code Length field
- Provide tooltip explaining why length is not editable
- Show impact preview: "Users must enter OTP within X minutes of receiving email" (REQ-026-136)
- See REQ-026-002.

---

### Screen 4: Country & Calling Code Manager

**Purpose**: Centralized management of countries and calling codes used across all platforms

**Data Fields**:

| Field Name     | Type     | Required | Description                                | Validation Rules                          | Graph field |
| -------------- | -------- | -------- | ------------------------------------------ | ----------------------------------------- | --- |
| Country Name   | text     | Yes      | Full country name (e.g., "United Kingdom") | Max 100 chars, unique (REQ-026-122, REQ-026-076) | ENT-country.country_name |
| ISO Code       | text     | Yes      | ISO 3166-1 alpha-2 code (e.g., "GB")       | Exactly 2 uppercase chars, unique (REQ-026-122, REQ-026-076) | ENT-country.iso_code |
| Calling Code   | text     | Yes      | International calling code (e.g., "+44")   | Format: +[1-4 digits] (REQ-026-122, REQ-026-077) | ENT-country.calling_code |
| Country Flag   | file     | Yes when an admin adds a country; a seeded country may have none and an imported country has none until uploaded | Country flag asset (SVG preferred; PNG fallback). A country with no flag has the state "flag missing" and cannot be set Active (REQ-026-128) | Types: .svg or .png; Max size: 1 MB; Recommended dimensions: SVG scalable, PNG ≥ 128x128 (REQ-026-122, REQ-026-079) | ENT-country.flag_url |
| Display Order  | number   | No       | Sort priority (lower = higher priority)    | Integer, default: 999 (REQ-026-122) | ENT-country.display_order |
| Active         | checkbox | Yes      | Whether country is visible in UI           | Default: true | ENT-country.active |

**Business Rules**:

- Country names must be unique (REQ-026-076)
- ISO codes must be unique and valid per ISO 3166-1 alpha-2 standard (REQ-026-076)
- Calling codes can be duplicated (e.g., USA and Canada both use +1) (REQ-026-077)
- Deactivating country does NOT delete (soft delete, archived) (REQ-026-078)
- Changes propagate to Patient app profile forms within 1 minute (REQ-026-005)
- Drag-and-drop reordering updates Display Order field (REQ-026-133)
- SVG is the preferred format for flags; PNG is allowed only when SVG is not available (REQ-026-079)
- For PNG uploads, enforce minimum resolution of 128x128 and square aspect ratio (1:1) (REQ-026-079)
- Store flag assets in centralized media storage/CDN and reference by URL (REQ-026-011)
- The final active country cannot be deactivated; a deactivation that would leave no active country is rejected with a message (REQ-026-141)
- A deactivated country keeps applying in FR-028 (regional groupings and fallback starting prices) until an admin edits them (REQ-028-083, REQ-028-092) (REQ-026-129)

**Notes**:

- Provide bulk import capability (CSV upload with validation) (REQ-026-128)
- The CSV has one row per country with the columns Country Name, ISO Code, Calling Code and Display Order (optional); it has no flag column. Every row is validated before anything is saved. An imported country is saved Inactive with a "flag missing" state and cannot be activated until the admin uploads its flag (REQ-026-128)
- Display validation errors inline
- Show usage count (how many users have selected this country) (REQ-026-111)
- Warn before deactivating a country with active users, and list the FR-028 regional groupings and fallback price rows that use it (REQ-026-129)
- Preview uploaded flag (SVG/PNG) next to country name in list views

---

### Screen 5: Discovery Questions Manager

**Purpose**: Manage "How did you find us?" question options displayed during patient registration

**Data Fields**:

| Field Name     | Type               | Required | Description                                      | Validation Rules            | Graph field |
| -------------- | ------------------ | -------- | ------------------------------------------------ | --------------------------- | --- |
| Question Text  | text (read-only)   | N/A      | Fixed question: "How did you find out about us?" | FIXED (not editable) (REQ-026-057) | ENT-discovery-question-option.question_text |
| Answer Option  | text               | Yes      | Answer choice (e.g., "Social Media")             | Max 100 chars, unique (REQ-026-123, REQ-026-080) | ENT-discovery-question-option.option_text |
| Display Order  | number             | No       | Sort priority (lower = displayed first)          | Integer, default: 999 (REQ-026-123) | ENT-discovery-question-option.display_order |
| Active         | checkbox           | Yes      | Whether option is visible in UI                  | Default: true | ENT-discovery-question-option.active |

**Business Rules**:

- Question text is FIXED ("How did you find out about us?") (REQ-026-057)
- Answer options must be unique (REQ-026-080)
- At least 2 active options must exist at all times (REQ-026-081)
- Deactivating option does NOT delete historical data (REQ-026-082)
- Changes propagate to Patient app within 1 minute (REQ-026-005)
- See REQ-026-133.

**Notes**:

- Provide drag-and-drop reordering UI (REQ-026-133)
- Display usage analytics (how many patients selected each option) (REQ-026-111)
- Warn if deactivating frequently selected option (REQ-026-129)
- Suggest common options when adding new (autocomplete) (REQ-026-134)
- See REQ-026-002.

---

### Screen 5a: Inquiry Cancellation Reasons Manager

**Purpose**: Centralized management of predefined cancellation reason options displayed to patients during inquiry cancellation (FR-003 Screen 8a)

**Data Fields**:

| Field Name            | Type     | Required | Description                                           | Validation Rules                    | Graph field |
| --------------------- | -------- | -------- | ----------------------------------------------------- | ----------------------------------- | --- |
| Reason Label          | text     | Yes      | Display text for the cancellation reason               | Max 100 chars, unique (REQ-026-124, REQ-026-083) | ENT-inquiry-cancellation-reason.reason_label |
| Requires Explanation  | checkbox | Yes      | Whether patient must provide free text when selecting  | Default: false; "Other" always true (REQ-026-124, REQ-026-085) | ENT-inquiry-cancellation-reason.requires_explanation |
| Display Order         | number   | No       | Sort priority (lower = displayed first)                | Integer, default: 999 (REQ-026-124) | ENT-inquiry-cancellation-reason.display_order |
| Active                | checkbox | Yes      | Whether reason is visible in cancellation modal        | Default: true | ENT-inquiry-cancellation-reason.active |

**Business Rules**:

- Reason labels must be unique (case-insensitive) (REQ-026-083)
- At least 2 active reasons must exist at all times (REQ-026-084)
- The "Other" reason is FIXED (cannot be deactivated or deleted) and always requires explanation (REQ-026-085)
- Deactivating a reason does NOT delete historical data — previously captured cancellation reasons retain their original label in audit logs (REQ-026-086)
- See REQ-026-005.
- See REQ-026-133.
- When "Requires Explanation" is true for a reason, FR-003 Screen 8a must show a mandatory free text field (max 500 chars) when that reason is selected (REQ-026-087)

**Notes**:

- Provide drag-and-drop reordering UI (same pattern as Discovery Questions) (REQ-026-133)
- Display usage analytics: how many patients selected each reason, with date range filter (REQ-026-111)
- Warn before deactivating a frequently selected reason (REQ-026-129)
- See REQ-026-002.
- Consumer: FR-003 Screen 8a (Cancel Inquiry Confirmation Modal) reads this list to populate the cancellation reason selector (REQ-026-032)

---

### Screen 5b: Account Deletion Reasons Manager

**Purpose**: Centralized management of predefined deletion reason options displayed to patients during account deletion request (FR-001 Screen 16)

**Data Fields**:

| Field Name            | Type     | Required | Description                                           | Validation Rules                      | Graph field |
| --------------------- | -------- | -------- | ----------------------------------------------------- | ------------------------------------- | --- |
| Reason Label          | text     | Yes      | Display text for the deletion reason                  | Max 100 chars, unique (REQ-026-125, REQ-026-088) | ENT-account-deletion-reason.reason_label |
| Requires Explanation  | checkbox | Yes      | Whether patient may provide free text when selecting  | Default: false; "Others" always true (REQ-026-125, REQ-026-090) | ENT-account-deletion-reason.requires_explanation |
| Display Order         | number   | No       | Sort priority (lower = displayed first)               | Integer, default: 999 (REQ-026-125) | ENT-account-deletion-reason.display_order |
| Active                | checkbox | Yes      | Whether reason is visible in deletion request screen  | Default: true | ENT-account-deletion-reason.active |

**Business Rules**:

- Reason labels must be unique (case-insensitive) (REQ-026-088)
- At least 2 active reasons must exist at all times (REQ-026-089)
- The "Others" reason is FIXED (cannot be deactivated or deleted) and always requires explanation (REQ-026-090)
- Deactivating a reason does NOT delete historical data — previously captured deletion reasons retain their original label in audit logs (REQ-026-091)
- See REQ-026-005.
- See REQ-026-133.
- When "Requires Explanation" is true for a reason, FR-001 Screen 16 must show an optional free text field (max 500 chars) when that reason is selected (the deletion reason field overall remains optional per FR-001 business rules) (REQ-026-092)

**Notes**:

- Provide drag-and-drop reordering UI (same pattern as Inquiry Cancellation Reasons) (REQ-026-133)
- Display usage analytics: how many patients selected each reason, with date range filter (REQ-026-111)
- Warn before deactivating a frequently selected reason (REQ-026-129)
- See REQ-026-002.
- Consumer: FR-001 Screen 16 (Delete Account / DSR screen) reads this list to populate the deletion reason selector (REQ-026-033)

---

### Screen 5c: Inquiry Configuration Manager

**Purpose**: Allow Admin to manage treatment-area options displayed at inquiry creation, the problem-duration list offered in the inquiry's detailed information step, and the blocked window before a patient may select a preferred treatment date.

| Field Name | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- |
| Treatment Area Label | text | Yes | Patient-facing option label | Unique among active options; max 100 chars (REQ-026-126, REQ-026-096) | ENT-treatment-area.label |
| Image/Icon Asset | media URL | Yes | Image or icon returned with the option | Must resolve to an approved S-05-managed asset (REQ-026-096) | ENT-treatment-area.image_or_icon_url |
| Display Order | number | Yes | Display sequence in the inquiry form | Unique integer order; drag-and-drop supported (REQ-026-126, REQ-026-096) | ENT-treatment-area.display_order |
| Active | checkbox | Yes | Whether the option is selectable for new inquiries | Default true; cannot deactivate the final active option; deactivation preserves historical records (REQ-026-036) | ENT-treatment-area.is_active |
| Minimum Inquiry Lead Time | number | Yes | Whole days blocked before a patient may select a preferred range | Integer 0-730; default 3 (REQ-026-035, REQ-026-096) | ENT-inquiry-scheduling-policy.minimum_inquiry_lead_days |
| Problem Duration Label | text | Yes | Patient-facing option of the problem-duration list (FR-003 Screen 3, Duration) | Unique among active options; max 100 chars (REQ-026-139) | no graph field (Setting) |
| Problem Duration Display Order | number | Yes | Display sequence of the problem-duration options | Unique integer order (REQ-026-139) | no graph field (Setting) |
| Problem Duration Active | checkbox | Yes | Whether the option is selectable for new inquiries | Default true; cannot deactivate the final active option; deactivation preserves historical records (REQ-026-139) | no graph field (Setting) |

**Business Rules**:

- The treatment-area list starts with three seeded options, Hair, Beard and Both (REQ-003-120), listed in Initial Configuration / Seeding. The admin may edit them afterwards. (REQ-026-034)
- The problem-duration list starts with five values, editable by Admin: Less than 6 months; 6 to 12 months; 1 to 2 years; 2 to 5 years; More than 5 years. Admin may create, edit, reorder, activate, or deactivate options; at least one stays active. A deactivated duration is no longer offered, and answers already stored stay readable. Consumer: FR-003 Screen 3. (REQ-026-139)
- Admin may create, edit, reorder, activate, or deactivate treatment-area options. Options referenced by an inquiry cannot be deleted. (REQ-026-093)
- System MUST retain at least one active treatment-area option. A deactivation that would leave no active option is rejected. (REQ-026-036)
- The patient configuration API returns active options in display order with `id`, `label`, and `image_or_icon_url`, plus `minimum_inquiry_lead_days`. (REQ-026-025, REQ-026-034, REQ-026-035)
- The API must not return inactive options for new inquiries. Historical inquiry views use the saved option snapshot. (REQ-026-094)
- Minimum Inquiry Lead Time applies to both the calendar's disabled-date calculation and backend inquiry submission validation. (REQ-026-095)
- Saving either setting requires a change reason, version increment, immutable audit entry, and immediate cache invalidation. (REQ-026-002, REQ-026-003, REQ-026-004, REQ-026-006)

---

### Screen 5d: Quote Configuration Manager

**Purpose**: Own the quote expiry window, the quote-expiring-soon lead time, the slot-hold duration, and the hold-expiring-soon reminder lead time, and show the quote currency that FR-004 copies onto each parent Quote at first send.

| Field Name | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- |
| Quote Currency | read-only label | Yes | ISO 4217 currency copied read-only onto each parent Quote at first send. It is the FR-029 Default Currency (FR-029 Screen 6), not a separate setting. Consumer: FR-004 | Changed only in FR-029; never provider-editable (REQ-026-037) | ENT-quote-configuration.currency_code |
| Quote Expiry Window | number | Yes | Whole hours copied read-only onto each parent Quote at first send to compute its expiry timestamp. Consumer: FR-004 | Whole hours from 24 to 336; default 48 hours (REQ-026-037) | ENT-quote-configuration.quote_expiry_hours |
| Quote Expiring Soon Lead Time | number | Yes | Whole hours before a sent quote expires at which FR-004 emits `quote.expiring_soon` (delivered through FR-030 and FR-020). Consumer: FR-004 | Whole hours from 1 up to half of the Quote Expiry Window; default 12 hours (REQ-026-037) | ENT-quote-configuration.quote_expiring_soon_lead_hours |
| Slot-Hold Duration | number | Yes | Whole hours of the one fixed, exclusive slot hold placed at subquote acceptance, and of the new hold placed by an FR-006 admin revive. Consumers: FR-005 and FR-006 | Whole hours from 24 to 168; default 48 hours (REQ-026-037) | ENT-quote-configuration.slot_hold_hours |
| Hold Expiring Soon Lead Time | number | Yes | Whole hours before a slot hold expires at which the patient receives the "hold expiring soon" reminder (triggered by FR-006, delivered through FR-030 and FR-020). Consumer: FR-006 | Whole hours from 1 up to half of the Slot-Hold Duration; default 12 hours (REQ-026-037) | ENT-quote-configuration.hold_expiring_soon_lead_hours |

**Business Rules**:

- The quote currency is the FR-029 Default Currency. FR-026 keeps no second currency setting. When the FR-029 Default Currency changes, the Quote Configuration records a new version so one version number identifies every value FR-004 copies. (REQ-026-037)
- FR-004 copies the quote currency and the quote expiry window read-only onto each parent Quote at first send and records the configuration version it used. Drafts carry neither value. Later changes never affect a sent quote, and no per-quote extension exists except the admin restore of an expired quote (REQ-004-105) and the admin-authored replacement quote (REQ-004-036), which captures its currency at its first Screen 8 save (REQ-004-082). (REQ-026-027)
- The slot hold starts at subquote acceptance. Each hold uses the slot-hold duration in effect when it is placed; later changes never alter an existing hold. Payment failure or retry never extends or restarts a hold. (REQ-026-030)
- Lead-time changes apply only to reminders that have not yet been sent. When a lead time is raised and a reminder's time has already passed, that reminder is skipped, not sent late. (REQ-026-031)
- Saving requires a change reason, version increment, immutable audit entry, and immediate cache invalidation. (REQ-026-002, REQ-026-003, REQ-026-004, REQ-026-006)
- Currency conversion and exchange-rate locking remain owned by FR-029 and occur at acceptance; this screen does not manage conversion rates. (REQ-026-097)

---

### Screen 5e: Analytics Configuration Manager

**Purpose**: Own the platform-wide thresholds and targets consumed by FR-014 provider and admin analytics.

| Field Name | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- |
| TTFQ SLA Target | number | Yes | Platform-wide time-to-first-quote target in minutes, used for TTFQ colour coding and benchmark charts | Positive whole number of minutes; default 120 (REQ-026-038) | ENT-analytics-configuration.ttfq_sla_minutes |
| At Risk Threshold | number | Yes | Day boundary after which a provider without qualifying activity is At Risk; FR-014 defines what counts as activity | Positive whole number of days; default 7 (REQ-026-038) | ENT-analytics-configuration.at_risk_days |
| Dormant Threshold | number | Yes | Day boundary after which a provider without qualifying activity is Dormant; FR-014 defines what counts as activity | Positive whole number of days; must be greater than At Risk Threshold; default 30 (REQ-026-038, REQ-026-100) | ENT-analytics-configuration.dormant_days |
| Price Outlier Threshold | number | Yes | Percentage deviation from the treatment median that flags a price outlier (FR-014 Screen 13) | Whole number from 1 to 100; default 30 (REQ-026-038) | ENT-analytics-configuration.price_outlier_percent |
| Benchmark Refresh Frequency | select | Yes | How often FR-014 recomputes provider benchmarks | Daily, Weekly, or Monthly; default Weekly (REQ-026-038) | ENT-analytics-configuration.benchmark_refresh_frequency |
| Target Monthly Commission | currency amount | No | Reference line on FR-014 Screen 12 Widget 2 | Optional; positive amount in the reporting currency of FR-014 admin financial analytics; blank by default (REQ-026-038) | ENT-analytics-configuration.target_monthly_commission |

**Business Rules**:

- See REQ-026-002, REQ-026-003, REQ-026-004, REQ-026-006.
- Recalculation rule: live dashboards and benchmarks always use the configuration version active when they are calculated, including for past periods shown on screen. After a change, the next calculation recolours and re-buckets every period in view (for example, last month's TTFQ tiers after an SLA change); past periods are not frozen at older values. Each aggregate records the configuration version used. PDF/CSV exports and scheduled-export files already generated are never rewritten; they keep the values and version from their generation time. (REQ-026-029)
- When Target Monthly Commission is blank, FR-014 hides the reference line; clearing a previously set value hides it again. (REQ-026-098)
- Per-provider SLA overrides are out of scope; all providers are measured against the same platform SLA target. (REQ-026-099)

---

### Screen 5f: Provider Specialties Manager

**Purpose**: Centralized management of the specialty values offered in the FR-015 provider Specialty select (Screen 2 Step 2 provider creation wizard, Screen 3 Tab 1 provider profile editing)

**Data Fields**:

| Field Name     | Type     | Required | Description                                                | Validation Rules                                   | Graph field |
| -------------- | -------- | -------- | ---------------------------------------------------------- | -------------------------------------------------- | --- |
| Specialty Name | text     | Yes      | Display text for the specialty                             | Max 100 chars, unique (case-insensitive) (REQ-026-039) | ENT-provider-specialty.specialty_name |
| Display Order  | number   | No       | Sort priority (lower = displayed first)                    | Integer, default: 999 | ENT-provider-specialty.display_order |
| Active         | checkbox | Yes      | Whether the value is selectable in FR-015 Specialty select | Default: true; at least one value must stay active (REQ-026-039) | ENT-provider-specialty.active |

**Business Rules**:

- Admin can add, rename, reorder, and deactivate values; hard delete is not supported (deactivate instead) (REQ-026-039)
- At least one active value must exist at all times; deactivating the final active value is blocked with a validation message (REQ-026-039)
- Deactivated values disappear from the FR-015 Specialty select for new selections; providers that already hold a deactivated value keep it, and it still displays on their profile (including in Screen 3 Tab 1 as the current value) until an admin changes it (REQ-026-039)
- Providers reference the specialty by its stable ID, so a rename applies to the display everywhere, including existing provider profiles (REQ-026-039)
- Saving requires a change reason, version increment, immutable audit entry (old and new values), and immediate cache invalidation (REQ-026-002, REQ-026-003, REQ-026-004, REQ-026-006)
- Changes propagate to FR-015 within 1 minute (REQ-026-005)
- See REQ-026-133.

**Notes**:

- Provide drag-and-drop reordering UI (same pattern as Inquiry Cancellation Reasons) (REQ-026-133)
- Show how many providers hold each value; warn before deactivating a value that providers currently hold (REQ-026-111, REQ-026-129)
- See REQ-026-002.
- Consumer: FR-015 / A-02 Screen 2 Step 2 and Screen 3 Tab 1 read the active list to populate the Specialty select (REQ-026-039)

---

### Screen 6: OTP Email Template Editor

**Purpose**: Edit email templates for OTP verification and password reset emails

**Data Fields**:

| Field Name               | Type               | Required | Description                           | Validation Rules                  | Graph field |
| ------------------------ | ------------------ | -------- | ------------------------------------- | --------------------------------- | --- |
| Template Name            | text (read-only)   | N/A      | Template identifier                   | FIXED (not editable) (REQ-026-058) | ENT-email-template.template_name |
| Subject Line             | text               | Yes      | Email subject line                    | Max 200 chars (REQ-026-127) | ENT-email-template.subject_line |
| Email Body (HTML)        | rich text          | Yes      | HTML email content                    | Max 50,000 chars, valid HTML (REQ-026-127, REQ-026-102) | ENT-email-template.html_body |
| Email Body (Plain Text)  | textarea           | Yes      | Fallback plain text version           | Max 10,000 chars (REQ-026-127) | ENT-email-template.plain_text_body |
| Available Variables      | list (read-only)   | N/A      | {code}, {email}, {expiry_minutes}, {app_name} | Display only (REQ-026-104). `{expiry_minutes}` is the lifetime of the code being sent: the OTP Expiry Time for registration and password reset, 15 for re-verification and email-change codes (REQ-026-072) | ENT-email-template.available_variables |

**Business Rules**:

- Template name is FIXED (cannot rename templates) (REQ-026-058)
- Subject and body must include {code} variable (REQ-026-101)
- HTML body must be valid (system validates on save) (REQ-026-102)
- Plain text body is fallback for email clients that don't support HTML (REQ-026-103)
- Variables are automatically substituted at send time (REQ-026-104)
- Preview functionality renders sample email with fake data (REQ-026-105)
- Changes apply only to NEW OTP generation requests (existing emails unaffected); a resend is a new code and uses the template version and expiry in force at the moment of the resend (REQ-026-106)

**Notes**:

- **IMPORTANT**: This screen serves BOTH "Verification Email" and "Password Reset Email" templates. Implement a template selector/chooser (dropdown or tabs) at the top of the screen to allow admins to switch between templates without navigating away. (REQ-026-131)
- Provide rich text editor (WYSIWYG) for HTML body
- Provide live preview panel showing rendered email
- Highlight required variables ({code}) in editor
- Provide sample data for preview ({code} = "123456", {expiry_minutes} = "15") (REQ-026-105)
- Warn if {code} variable is missing (REQ-026-101)
- See REQ-026-002.

---

### Screen 7: Version History Viewer

**Purpose**: Display complete audit trail of changes for a specific setting group

**Data Fields**:

| Field Name      | Type               | Required | Description                               | Validation Rules   | Graph field |
| --------------- | ------------------ | -------- | ----------------------------------------- | ------------------ | --- |
| Version Number  | text (read-only)   | N/A      | Version identifier (e.g., "v1.3")         | N/A (display only) | ENT-setting-version.version_number |
| Changed On      | datetime (read-only) | N/A      | Timestamp of change, shown in the admin's browser timezone with the zone named beside the time (REQ-026-050) | N/A (display only) | ENT-settings-audit-entry.timestamp |
| Changed By      | text (read-only)   | N/A      | Admin email who made change               | N/A (display only) | ENT-settings-audit-entry.admin_email |
| Change Type     | text (read-only)   | N/A      | "Update", "Initial", "System" (a Quote Configuration version created by a Default Currency change in FR-029) | N/A (display only) | ENT-setting-version.change_type |
| Old Values      | JSON (read-only)   | N/A      | Previous configuration values             | N/A (display only) | ENT-settings-audit-entry.old_values |
| New Values      | JSON (read-only)   | N/A      | Updated configuration values              | N/A (display only) | ENT-settings-audit-entry.new_values |
| Change Reason   | text (read-only)   | N/A      | Admin-provided explanation                | N/A (display only) | ENT-settings-audit-entry.change_reason |
| Actions         | button group       | N/A      | View Details                              | N/A | no graph field (control) |

**Business Rules**:

- Version history is immutable (cannot delete or edit) (REQ-026-007)
- Versions displayed in reverse chronological order (newest first) (REQ-026-008)
- Diff view highlights changed fields (old → new) (REQ-026-008)
- Sensitive values (API keys) masked in version history; no FR-026 setting is sensitive at launch, so the "Show" control appears only for a value later marked sensitive (REQ-026-052)
- A Quote Configuration version created by a Default Currency change in FR-029 (REQ-029-053) has Change Type "System", the fixed reason text "Default currency changed in Payment Configuration", and Changed By set to the admin who confirmed the change in FR-029. The change reason rule (REQ-026-002) covers changes made on FR-026 screens. (REQ-026-142)

**Notes**:

- Use diff highlighting (red for removed, green for added) (REQ-026-008)
- Provide search/filter by date range, admin, or change type (REQ-026-130)
- Pagination for long version histories (50 entries per page) (REQ-026-130)

---

### Screen 8: Platform Settings Editor

**Purpose**: Lets an admin view and change the platform Settings that other modules read and that are not edited on Screens 2 to 7. Each Setting sits in one of the four setting groups on Screen 1 (Authentication & Security, App Data, Notifications; none belongs to Analytics).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- |
| Re-Verification Threshold | number (minutes) | Yes | How long after a patient's last successful sign-in the patient must confirm identity again before a sensitive action (FR-001 Screens 16 and 18) | Whole minutes from 1 to 60; default 5, the value FR-001 uses (REQ-026-112) | no graph field (Setting) |
| Admin Concurrent Sessions | number | Yes | Number of concurrent sessions allowed for one admin user (consumer: FR-031) | Whole number from 1 to 5; default 3 (REQ-026-116) | no graph field (Setting) |
| Admin Inactivity Timeout | number (minutes) | Yes | Standard admin inactivity timeout (consumer: FR-031). A Login as Provider session ends after its own fixed 30 minutes of inactivity (REQ-015-026) or when the admin's own session ends under this timeout, whichever comes first | Whole minutes from 5 to 240; default 30 (REQ-026-116) | no graph field (Setting) |
| Landing Background Images | image set | No | Background images that rotate behind the patient landing screen (FR-001) | Image assets only; rotation follows the admin configuration; with no images set, none are shown (REQ-026-113) | no graph field (Setting) |
| Profile Photo Accepted Formats | multi-select | Yes | File formats a patient may upload as a profile photo (read by FR-001 REQ-001-082) | Default JPG and PNG (REQ-026-114) | no graph field (Setting) |
| Profile Photo Maximum Size | number (MB) | Yes | Largest profile photo a patient may upload (read by FR-001 REQ-001-082) | Default 5 MB (REQ-026-114) | no graph field (Setting) |
| Head Scan Minimum Brightness Score | number | Yes | Lowest brightness score a head scan photo may have and still pass the basic quality check (consumer: FR-002 REQ-002-034, REQ-002-050) | Whole number from 0 to 100; default 40. A photo passes when both its brightness and its blur score reach their minimum (REQ-026-117) | no graph field (Setting) |
| Head Scan Minimum Blur Score | number | Yes | Lowest blur score a head scan photo may have and still pass the basic quality check (consumer: FR-002 REQ-002-034, REQ-002-050) | Whole number from 0 to 100; default 40 (REQ-026-117) | no graph field (Setting) |
| Head Video Duration Limits | number pair (seconds) | No | Minimum and maximum duration of a head video. Not used until head video ships (REQ-002-035) | No value is fixed in this document (REQ-026-117) | no graph field (Setting) |
| Acceptance Terms Text | text | Yes | Legal copy and terms acknowledgment text shown at quote acceptance (consumer: FR-005). Terms & Conditions, Privacy Policy and consent forms stay in FR-027 | Edited with the same change reason and versioning as every other Setting. Until the admin sets the text, the quote acceptance action that needs the acknowledgment checkbox is blocked with a message (REQ-026-118) | no graph field (Setting) |
| Timezone Options | list | Yes | Timezone choices from GMT-12 to GMT+14, each shown with its offset and a city example such as "(GMT+3) Istanbul" (consumers: FR-032, FR-021) | Offsets GMT-12 to GMT+14 (REQ-026-121) | no graph field (Setting) |
| Provider Notification Types | list | Yes | Notification types offered in provider notification preferences (consumers: FR-032, FR-020) | Core types quote, schedule, treatment, aftercare and review cannot be removed (REQ-026-120) | no graph field (Setting) |
| Support Emergency Contact Phone | text | No | Emergency phone number shown read-only with tap-to-call on the patient Help & Support Hub (FR-035 Screen 1) | No default; a save that changes the phone or the email must leave at least one of them set (REQ-026-143), and FR-035 assumes the admin sets it before go-live (REQ-026-115) | SET-support-emergency-contact-phone |
| Support Emergency Contact Email | text | No | Emergency email address shown read-only with tap-to-compose on the patient Help & Support Hub (FR-035 Screen 1) | No default; a save that changes the phone or the email must leave at least one of them set (REQ-026-143), and FR-035 assumes the admin sets it before go-live (REQ-026-115) | SET-support-emergency-contact-email |
| Treatment Creation Rate Limit | number | Yes | Maximum new treatments per admin per hour (owner: FR-024) | Range and default follow FR-024; a new record counts once, when first saved as Active or Inactive (REQ-026-140) | no graph field (Setting) |
| Package Creation Rate Limit | number | Yes | Maximum new packages per provider per hour (owner: FR-024) | Range and default follow FR-024; a new record counts once, when first saved as Active or Inactive, and a clone counts (REQ-026-140) | no graph field (Setting) |
| Admin Invitation Token Expiry | number (days) | Yes | Lifetime of an admin team invitation token (owner: FR-031) | Range and default follow FR-031 (REQ-026-140) | no graph field (Setting) |
| Admin Repeated Denial Threshold | number pair | Yes | Count of refusals of one admin and the time window that trigger the Super Admin alert (owner: FR-031) | Range and default follow FR-031 (REQ-026-140) | no graph field (Setting) |

**Business Rules**:

- Saving requires a change reason, version increment, immutable audit entry, and immediate cache invalidation, as on every other Settings screen. (REQ-026-002, REQ-026-003, REQ-026-004, REQ-026-006)
- Failed admin sign-ins use the shared Max Login Attempts setting on Screen 2 (default 5, with the shared lockout duration); there is no separate admin setting, and the fixed FR-031 endpoint throttle of 5 attempts per 15 minutes applies in addition, whichever trips first (REQ-031-100). (REQ-026-116)
- When an admin signs in while already at the Admin Concurrent Sessions limit, the oldest session is ended and the new one opens. A change to the session limit or the inactivity timeout applies from each open session's next request; sessions above a lowered limit are ended oldest first (REQ-026-116)
- The discovery source options of the registration question are the Discovery Questions answer options managed on Screen 5; Screen 8 holds no second list. (REQ-026-119)
- Where the table says no value is fixed, an admin sets the value here and can change it without a code release. (REQ-026-117)
- A save that changes Support Emergency Contact Phone or Email and leaves both blank is refused with the message "Set at least one emergency contact (phone or email)."; other Screen 8 rows can be saved while both are still blank, as at launch. While both are blank the patient Help & Support Hub hides the emergency contact section (REQ-026-143, REQ-035-040)
- The group "Limits owned by other features" (the last four rows) only lists Settings whose owning FR makes them admin-editable; range, default and counting rule stay with the owning FR (REQ-026-140)
- The edit permission for these Settings is in the permission table under Security Controls (REQ-026-001).

---

## Business Rules

### General Module Rules

- **Rule 1**: All setting changes MUST require a change reason (minimum 10 characters, maximum 500 characters) captured via modal after clicking Save on an FR-026 screen (REQ-026-002). A Quote Configuration version created by a Default Currency change in FR-029 is not covered by this rule; it is recorded as Change Type "System" with a fixed reason (REQ-026-142)
- **Rule 2**: Setting changes MUST be versioned with auto-incremented version numbers (v1.0, v1.1, v1.2, etc.) (REQ-026-003)
- **Rule 3**: Setting changes MUST propagate to dependent services within 1 minute (60-second polling interval) (REQ-026-005)
- **Rule 4**: Settings cache MUST be invalidated immediately upon save to ensure propagation (REQ-026-006)
- **Rule 5**: All timestamps MUST be stored in UTC. Admin screens show times in the admin's browser timezone, with the zone named beside the time; the Timezone Options list is the choice offered to patients and providers only (REQ-026-050)

### Data & Privacy Rules

- **Privacy scope**: No FR-026 setting is sensitive at launch. The masking, encryption and "View Sensitive Settings" rules below apply only to a setting later marked sensitive, and the Screen 7 "Show" control appears only for such a value (REQ-026-014, REQ-026-016, REQ-026-052)
- **Privacy Rule 1**: Sensitive setting values (API keys, secrets, credentials) MUST be masked in UI (display as "••••••••") (REQ-026-014)
- **Privacy Rule 2**: Sensitive values MUST be masked in audit logs (display as "[REDACTED]") (REQ-026-014)
- **Privacy Rule 3**: Full sensitive values MUST be viewable only by admins with "View Sensitive Settings" permission (REQ-026-015)
- **Audit Rule 1**: All setting changes MUST be logged with timestamp, admin ID, admin email, old values, new values, and reason (REQ-026-004)
- **Audit Rule 2**: Audit logs MUST be immutable (no deletion, no editing) (REQ-026-004)
- **Audit Rule 3**: Audit log retention follows the system PRD, Platform-Wide Rules: One 10-year retention period
- **GDPR**: Admin activity logs are exempt from GDPR deletion requests (business records, legal requirement) (REQ-026-051)

### Admin Editability Rules

**Editable by Admin**:

- Authentication throttling: max login attempts (range: 1-10), lockout duration (range: 5-60 minutes) (REQ-026-009)
- OTP configuration: expiry time (range: 5-30 minutes), resend cooldown (range: 30-300 seconds), max resend attempts (range: 3-10) (REQ-026-010)
- Country list: add, edit, deactivate countries and calling codes (REQ-026-011)
- Discovery questions: add, edit, deactivate answer options (REQ-026-012)
- Inquiry cancellation reasons: add, edit, reorder, deactivate reason options (FR-003 consumer) (REQ-026-032)
- Account deletion reasons: add, edit, reorder, deactivate reason options (FR-001 Screen 16 consumer) (REQ-026-033)
- Provider specialties: add, rename, reorder, deactivate specialty values (FR-015 Screen 2 Step 2 and Screen 3 Tab 1 consumer) (REQ-026-039)
- Inquiry configuration: add, edit, reorder, activate, or deactivate treatment-area options and set the minimum inquiry lead time (FR-003 consumer) (REQ-026-034, REQ-026-035, REQ-026-093)
- Quote configuration: set the quote expiry window and the quote-expiring-soon lead time (FR-004 consumer), and the slot-hold duration and the hold-expiring-soon lead time (FR-005 and FR-006 consumers); the quote currency is shown read-only because it is the FR-029 Default Currency (REQ-026-037)
- Analytics configuration: TTFQ SLA target, At Risk and Dormant thresholds, price outlier threshold, benchmark refresh frequency, and optional target monthly commission (FR-014 consumer) (REQ-026-038)
- OTP email templates: subject line, HTML body, plain text body (REQ-026-013)
- Platform Settings (Screen 8): re-verification threshold; admin concurrent sessions and inactivity timeout; landing background images; profile photo formats and maximum size; head scan quality minimums and head video duration limits; acceptance terms text; timezone options; provider notification types; support emergency contact phone and email (REQ-026-112, REQ-026-113, REQ-026-114, REQ-026-115, REQ-026-116, REQ-026-117, REQ-026-118, REQ-026-120, REQ-026-121)

**Fixed in Codebase (Not Editable)**:

- Password policy: fixed in codebase and not admin-editable; the policy is defined by REQ-SYS-007 (system PRD, Platform-Wide Rules: Password and one-time-code policy). FR-026 holds SET-password-policy only as the stored value other FRs read; it is not editable on FR-026 screens (REQ-SYS-007)
- OTP code length: FIXED at 6 digits (REQ-026-060)
- IP/device-level rate limiting: Fixed thresholds enforced at the application layer (not admin-configurable): max 20 failed login attempts per IP address per hour; IP lockout duration: 1 hour (REQ-026-056)
- Discovery question text: FIXED as "How did you find out about us?" (REQ-026-057)
- Template names: Cannot rename OTP email templates (REQ-026-058)
- Setting group structure: Cannot create new setting groups (predefined) (REQ-026-059)

**Configurable with Restrictions**:

- Admin can deactivate countries but cannot delete (soft delete, archived) (REQ-026-078)
- Admin can deactivate discovery options but must maintain at least 2 active options (REQ-026-081)
- Admin can deactivate cancellation reasons but must maintain at least 2 active reasons; "Other" reason cannot be deactivated (REQ-026-084, REQ-026-085)
- Admin can deactivate account deletion reasons but must maintain at least 2 active reasons; "Others" reason cannot be deactivated (REQ-026-089, REQ-026-090)
- Admin can deactivate provider specialties but cannot delete them and must maintain at least 1 active value; providers holding a deactivated value keep it and it still displays (REQ-026-039)
- Admin can edit email templates but must include required variables ({code} for OTP templates) (REQ-026-101)
- Admin can add or remove provider notification types but cannot remove the core types (quote, schedule, treatment, aftercare, review) (REQ-026-120)

### Security Controls

- **Authorization**: Role-based access control (RBAC) enforced with the FR-031 admin permissions (REQ-031-113); one gate for every Settings screen (REQ-026-001, REQ-026-054):
  - View Settings: view settings and version history (read-only) on every screen
  - Edit Settings: Super Admin only (REQ-031-067)
  - View Sensitive Settings: view the full value of a sensitive setting; applies only to a setting later marked sensitive

  | Screen group | Permission to view | Permission to edit |
  | --- | --- | --- |
  | Screen 1 Dashboard, Screen 7 Version History | View Settings | Not editable |
  | Screens 2 and 3 Authentication Throttling, OTP Configuration | View Settings | Manage Authentication Policies |
  | Screens 4, 5, 5a, 5b, 5c, 5f App Data lists | View Settings | Manage App Data |
  | Screen 5d Quote Configuration, Screen 5e Analytics Configuration | View Settings | Edit Settings |
  | Screen 6 OTP Email Templates | View Settings | Manage Notification Templates |
  | Screen 8 Platform Settings, admin session rows | View Settings | Manage Authentication Policies |
  | Screen 8 Platform Settings, all other rows | View Settings | Edit Settings |

  FR-031 names countries and discovery questions under Manage App Data and lockout and session timeout under Manage Authentication Policies; assigning the other App Data lists and the OTP settings to those permissions is queued for FR-031 to confirm.
- **Encryption**: Sensitive setting values (API keys, secrets) encrypted at rest using AES-256 (REQ-026-016)
- **Audit trail**: All admin actions logged with IP address, user agent, timestamp, and change details (REQ-026-053)
- **Rate limiting**: Settings API rate limiting is defined once in the system PRD (moved from this document)
- **IP/device-level rate limiting**: Fixed at application layer (not admin-configurable); max 20 failed login attempts per IP address per hour with a 1-hour IP lockout. Enforced independently of the per-user authentication throttling configured in Screen 2. Both constraints apply simultaneously (whichever triggers first locks the user out). (REQ-026-056)
- **Input validation**: All user inputs sanitized to prevent XSS, SQL injection, command injection (REQ-026-020)
- **HTML Sanitization for Email Templates**: (REQ-026-069)
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
- **Compliance**: Audit logs are immutable (no deletion); retention follows the system PRD, Platform-Wide Rules: One 10-year retention period (REQ-026-004)

### Integration Rules

- **Cache Invalidation**: Invalidate cache immediately on save; dependent services detect stale cache via version comparison
- **Integration 1: Patient Platform → Settings API**
  - **Data format**: JSON response with version number and setting values
  - **Authentication**: OAuth 2.0 bearer token with "read:settings" scope
  - **Error handling**: If API unreachable, Patient Platform continues using cached settings until the next successful poll, logs the error, and retries on the next 60-second poll (REQ-026-046)

- **Integration 2: Notification Service → Settings API (Template Retrieval)**
  - **Data format**: JSON response with template name, subject, HTML body, plain text body, variables
  - **Authentication**: OAuth 2.0 bearer token with "read:settings" scope
  - **Error handling**: If API unreachable, use fallback template (hardcoded default); log error for admin review (REQ-026-047)

- **Integration 3: Admin UI → Settings API (CRUD Operations)**
  - **Data format**: JSON request/response for create, read, update operations
  - **Authentication**: OAuth 2.0 bearer token with "write:settings" scope (restricted to authorized admins)
  - **Error handling**: Display user-friendly error messages for validation failures; retry logic for network timeouts

- **FR-001 / Module P-01: Auth & Profile Management**
  - **Integration point**: P-01 polls Settings API every 60 seconds to retrieve latest configurations; applies to login flows, OTP verification, profile forms

- **FR-003 / Module P-02: Quote Request & Management**
  - **Integration point**: P-02 retrieves active cancellation reasons for Workflow 5 and retrieves the active ordered treatment-area catalog with `minimum_inquiry_lead_days` for Screen 1, Screen 5, and backend submission validation. Submitted inquiries retain their treatment-area snapshot.

- **FR-004 / Module PR-02: Inquiry & Quote Management**
  - **Integration point**: At first send, FR-004 retrieves one versioned configuration response, copies the ISO 4217 currency and the expiry window read-only onto the parent Quote, computes `expiresAt` from the send time, and records the configuration version. FR-004 emits `quote.expiring_soon` at the configured lead time. Sent quotes do not change when configuration is updated. (REQ-026-026, REQ-026-027)

- **FR-005 and FR-006 / Quote Acceptance and Booking**
  - **Integration point**: Acceptance and an FR-006 admin revive read the active slot-hold duration when the hold is placed. FR-006 has no separate hold setting. (REQ-026-030)

- **FR-029 / Payment System Configuration**
  - **Integration point**: The Settings API returns the FR-029 Default Currency as the quote currency; a change in FR-029 records a new Quote Configuration version.

- **FR-014 / Modules PR-05 and A-08: Provider Analytics & Reporting**
  - **Integration point**: Analytics calculations and benchmark jobs retrieve one configuration version from the Settings API and record that version with the aggregates they produce.

- **FR-009 / Module PR-01: Auth & Team Management**
  - **Integration point**: PR-01 polls Settings API every 60 seconds to retrieve authentication policies

- **FR-020 / Module S-03: Notification Service**
  - **Integration point**: S-03 retrieves template by name via Settings API when generating OTP email; caches template for 1 minute. Quote-expiring-soon and hold-expiring-soon reminders are delivered through FR-030 and FR-020 at the lead times set in the Quote Configuration

- **Module S-05: Media Storage Service**
  - **Integration point**: Settings UI uploads an approved asset to the S-05 API, receives its URL, and stores that URL in the applicable country or inquiry treatment-area configuration.

- **FR-031 / Admin Authentication & Authorization Module**
  - **Why needed**: Cannot restrict access to Settings Management UI without authentication and role-based permissions
  - **Required access levels**: the FR-031 permissions View Settings, Edit Settings, Manage App Data, Manage Authentication Policies, Manage Notification Templates and View Sensitive Settings (REQ-031-113); the screen-to-permission table is under Security Controls
  - **Integration point**: All Settings Management UI screens enforce role checks before allowing access; all API endpoints validate OAuth 2.0 tokens with appropriate scopes (REQ-026-001, REQ-026-023)

The following modules consume FR-026 infrastructure. They are listed here for traceability; FR-026 implementation does NOT block on them.

- **FR-024 / Module A-09: Treatment & Package Management**
  - **Relationship**: FR-026 provides the settings infrastructure (audit trail, versioning, UI shell); FR-024 implements treatment-specific CRUD operations within that infrastructure
  - **Integration point**: Treatment management shares the Settings Management UI and audit trail established by FR-026 (REQ-026-061)

- **FR-011 / Module A-03: Aftercare Team Management**
  - **Relationship**: FR-026 provides the settings infrastructure; FR-011 implements aftercare milestone template management within that infrastructure
  - **Integration point**: Providers select from admin-created aftercare templates; templates are managed via the A-09 settings surface defined in FR-026 (REQ-026-061)

- **FR-002, FR-005, FR-031, FR-032, FR-035**
  - **Relationship**: Each consumes platform Settings described on Screen 8: FR-002 the head scan quality minimums, FR-005 the acceptance terms text, FR-031 the admin session settings, FR-032 the provider notification types and timezone options, FR-035 the support emergency contact
  - **Integration point**: Each reads the active values through the Settings API; FR-026 implementation does NOT block on them

- **FR-015 / Module A-02: Provider Management**
  - **Relationship**: FR-026 owns the Provider Specialties list; FR-015 consumes it
  - **Integration point**: FR-015 Screen 2 Step 2 and Screen 3 Tab 1 populate the required Specialty select from the active list and store the selected specialty ID on the provider (REQ-026-039)

### Operating Conditions

- Admin web app accessed via modern browsers (Chrome, Safari, Firefox, Edge - last 2 versions)
- Admins have stable internet connection (not optimized for offline mode)
- Settings database supports ACID transactions (prevent partial updates)
- Dependent services (Patient app, Provider app) can poll Settings API every 60 seconds without performance impact
- Admins have authority to modify security policies without external approval
- 1-minute propagation delay is acceptable for non-critical settings (e.g., discovery questions)
- Security policy changes apply prospectively only (do not retroactively affect locked-out users; a lowered attempt limit applies from the next failed attempt) (REQ-026-071, REQ-026-145)

### Initial Configuration / Seeding

**Database Seeding Requirements**:

- **Authentication Throttling**:
  - Max Login Attempts: 5
  - Lockout Duration: 15 minutes
- **OTP Configuration**:
  - Expiry Time: 15 minutes
  - Resend Cooldown: 60 seconds
  - Max Resend Attempts: 5 per hour
- **Discovery Questions**: (REQ-026-064)
  - Initial Option 1: "Search Engine" (Order: 1)
  - Initial Option 2: "Social Media" (Order: 2)
  - Initial Option 3: "Friend Referral" (Order: 3)
- **Inquiry Cancellation Reasons**: (REQ-026-065)
  - Initial Option 1: "Changed my mind" (Order: 1, Requires Explanation: No)
  - Initial Option 2: "Found a better option elsewhere" (Order: 2, Requires Explanation: No)
  - Initial Option 3: "Medical concerns" (Order: 3, Requires Explanation: No)
  - Initial Option 4: "Financial reasons" (Order: 4, Requires Explanation: No)
  - Initial Option 5: "Travel restrictions" (Order: 5, Requires Explanation: No)
  - Initial Option 6: "Timeline doesn't work" (Order: 6, Requires Explanation: No)
  - Initial Option 7: "Other" (Order: 7, Requires Explanation: Yes, FIXED — cannot be deactivated)
- **Account Deletion Reasons**: (REQ-026-066)
  - Initial Option 1: "I no longer use this app" (Order: 1, Requires Explanation: No)
  - Initial Option 2: "I found a better alternative" (Order: 2, Requires Explanation: No)
  - Initial Option 3: "The app doesn't meet my needs" (Order: 3, Requires Explanation: No)
  - Initial Option 4: "Too many notifications or emails" (Order: 4, Requires Explanation: No)
  - Initial Option 5: "Concerns about privacy or data security" (Order: 5, Requires Explanation: No)
  - Initial Option 6: "I had technical issues or bugs" (Order: 6, Requires Explanation: No)
  - Initial Option 7: "The app is difficult to use" (Order: 7, Requires Explanation: No)
  - Initial Option 8: "I'm taking a break and may return later" (Order: 8, Requires Explanation: No)
  - Initial Option 9: "Others" (Order: 9, Requires Explanation: Yes, FIXED — cannot be deactivated)
- **Provider Specialties**: (REQ-026-039)
  - Initial Value 1: "Hair Transplant Surgeon" (Order: 1)
  - Initial Value 2: "Dermatologist" (Order: 2)
  - Initial Value 3: "Trichologist" (Order: 3)
  - Initial Value 4: "Plastic Surgeon" (Order: 4)
  - Initial Value 5: "Other" (Order: 5)
- **Inquiry Configuration**:
  - Treatment areas: three options, Hair, Beard and Both (Order: 1, 2, 3), each seeded with an image or icon asset supplied at setup (REQ-003-120, REQ-026-034)
  - Problem durations: Less than 6 months; 6 to 12 months; 1 to 2 years; 2 to 5 years; More than 5 years (Order: 1 to 5) (REQ-026-139)
  - Minimum Inquiry Lead Time: 3 days
- **Platform Settings**:
  - Re-Verification Threshold: 5 minutes
  - Admin Concurrent Sessions: 3
  - Admin Inactivity Timeout: 30 minutes
  - Profile Photo Accepted Formats: JPG and PNG; Profile Photo Maximum Size: 5 MB
  - Head Scan Minimum Brightness Score: 40; Head Scan Minimum Blur Score: 40 (REQ-026-117)
  - Timezone Options: every whole-hour offset from GMT-12 to GMT+14, each with a city example (REQ-026-121)
  - Provider Notification Types: the five core types, quote, schedule, treatment, aftercare and review (REQ-026-120)
  - Landing Background Images: none; with none set, no background images are shown (REQ-026-113)
  - Acceptance Terms Text: no seeded text; quote acceptance that needs the acknowledgment checkbox is blocked with a message until the admin sets it (REQ-026-118)
  - Support Emergency Contact Phone and Email: no default
- **Countries**: (REQ-026-067)
  - Minimum initial set: Turkey (TR, +90), UK (GB, +44), USA (US, +1), Germany (DE, +49)
- **Templates**: (REQ-026-068)
  - Default "Verification Email" and "Password Reset Email" templates MUST be seeded with standard branding and variables
- **Quote Configuration**:
  - Quote Currency: the FR-029 Default Currency (not seeded as a separate value)
  - Quote Expiry Window: 48 hours
  - Quote Expiring Soon Lead Time: 12 hours
  - Slot-Hold Duration: 48 hours
  - Hold Expiring Soon Lead Time: 12 hours
- **Analytics Configuration**:
  - TTFQ SLA Target: 120 minutes
  - At Risk Threshold: 7 days
  - Dormant Threshold: 30 days
  - Price Outlier Threshold: 30%
  - Benchmark Refresh Frequency: Weekly
  - Target Monthly Commission: not set (reference line hidden)
- **Why needed**: FR-005 places the slot hold at acceptance and FR-006 manages it; both consume the slot-hold duration. FR-006 also consumes the hold-expiring-soon lead time for the patient reminder.

**Carried from dropped sections (original wording)**:

- **SC-015**: Security scanning shows no exposure of sensitive values in browser console or network requests
- **None**: This module has no external dependencies (self-contained within Hairline platform)

---

## Dependencies

- FR-001 / Module P-01: Auth & Profile Management: consumes authentication throttling, OTP configuration, country lists, discovery questions, the re-verification threshold, the landing background, and the profile photo limits
- FR-002: head scan quality minimums
- FR-003 / Module P-02: Quote Request & Management: inquiry cancellation reason options for the patient cancellation modal (Screen 8a), active inquiry treatment-area options, minimum inquiry lead time
- FR-004 / Module PR-02: Inquiry & Quote Management: quote currency, quote expiry window, quote-expiring-soon lead time
- FR-005 and FR-006 / Quote Acceptance and Booking: both consume the slot-hold duration; FR-006 also the hold-expiring-soon lead time for the patient reminder; FR-005 also the acceptance terms text
- FR-009 / Module PR-01: Auth & Team Management: authentication throttling and OTP configuration for provider login and email verification
- FR-011 / Module A-03: Aftercare Team Management: aftercare milestone template management within the settings infrastructure
- FR-014 / Modules PR-05 and A-08: Provider Analytics & Reporting: versioned Analytics Configuration for TTFQ SLA colour coding, provider engagement status, price outlier detection, benchmark refresh cadence, and the optional commission reference line
- FR-015 / Module A-02: Provider Management: Provider Specialties list
- FR-020 / Module S-03: Notification Service: OTP email templates for verification and password reset emails; the `inquiry.ttfq_sla_breached` alert uses the Analytics Configuration TTFQ SLA target
- FR-024 / Module A-09: Treatment & Package Management: treatment-specific CRUD within the settings infrastructure
- FR-029 / Payment System Configuration: the Default Currency is the quote currency
- FR-031 / Admin Authentication & Authorization Module: role-based permissions; admin session settings
- FR-032: provider notification types and timezone options
- FR-021: timezone options and UTC timestamp storage
- FR-035: support emergency contact
- Module S-05: Media Storage Service: country flag assets and treatment-area image/icon assets

---

## User Scenarios & Testing

### User Story 1 - Update Authentication Throttling Policy (Priority: P1)

Admin needs to reduce login attempt lockout from 5 attempts to 7 attempts based on user feedback that current policy is too strict.

**Why this priority**: Critical security configuration that directly impacts user experience; must be adjustable without code deployment.

**Independent Test**: Can be fully tested by: (1) Admin updates throttling policy via UI, (2) Reason modal appears and is submitted, (3) Verify audit log created, (4) Wait 1 minute, (5) Test login with new policy on Patient app, (6) Verify 7 attempts allowed before lockout.

**Acceptance Scenarios**:

1. **Given** admin is logged in and has the View Settings permission and the edit permission of the screen, **When** admin navigates to Settings → Authentication & Security, **Then** system displays current throttling policy (5 attempts, 15-minute lockout)
2. **Given** admin is editing throttling policy, **When** admin changes max attempts to 7 and clicks Save, then submits the reason modal, **Then** system saves new policy, creates audit log, increments version number
3. **Given** admin saved new throttling policy at least 1 minute ago, **When** patient attempts login on Patient app, **Then** new policy (7 attempts) applies
4. **Given** patient makes 6 failed login attempts, **When** patient attempts 7th login, **Then** system allows attempt (does not lock out until 8th attempt)
5. **Given** admin views version history, **When** admin selects version history for authentication throttling, **Then** system displays complete audit trail including admin ID, timestamp, old/new values, and reason

---

### User Story 2 - Edit OTP Email Template (Priority: P1)

Marketing team requests updated branding in OTP verification emails; admin needs to update template without code deployment.

**Why this priority**: Critical communication channel; branding changes are frequent business requirement.

**Independent Test**: Can be fully tested by: (1) Admin edits OTP template via UI, (2) Preview rendered email, (3) Click Save and submit reason modal, (4) Request new OTP on Patient app, (5) Verify email received with new branding.

**Acceptance Scenarios**:

1. **Given** admin is logged in and has the View Settings permission and the edit permission of the screen, **When** admin navigates to Settings → Notifications → OTP Email Templates, **Then** system displays list of templates (Verification Email, Password Reset Email)
2. **Given** admin selected "Verification Email" template, **When** admin modifies HTML body and clicks "Preview", **Then** system displays rendered email with sample data ({code} = "123456")
3. **Given** admin previewed email and verified branding, **When** admin clicks Save and submits the reason modal, **Then** system versions template, creates audit log
4. **Given** admin saved new template at least 1 minute ago, **When** patient requests new OTP on Patient app, **Then** patient receives email with new branding
5. **Given** patient already received OTP before template change, **When** admin saves new template, **Then** patient's existing OTP email remains unchanged (no retroactive changes)

---

### User Story 3 - Add New Country to Centralized List (Priority: P1)

Admin needs to add "Albania" to country list to support expanded patient base in Balkan region.

**Why this priority**: Business expansion requirement; must be updatable without code deployment.

**Independent Test**: Can be fully tested by: (1) Admin adds Albania via UI (including flag upload), (2) Submit reason modal, (3) Wait 1 minute, (4) Open Patient app profile form, (5) Verify "Albania" appears in country dropdown with flag.

**Acceptance Scenarios**:

1. **Given** admin is logged in and has the View Settings permission and the edit permission of the screen, **When** admin navigates to Settings → App Data → Countries & Calling Codes, **Then** system displays current list of countries
2. **Given** admin clicks "Add Country", **When** admin enters country name "Albania", ISO code "AL", calling code "+355", **Then** system validates uniqueness of name and ISO code
3. **Given** admin entered valid country data and uploaded flag, **When** admin clicks Save and submits the reason modal with "Expanding to Albanian market", **Then** system creates audit log, versions country list
4. **Given** admin saved new country at least 1 minute ago, **When** patient opens profile form on Patient app, **Then** "Albania" appears in country dropdown
5. **Given** patient selects "Albania" in country dropdown, **When** patient views phone number field, **Then** calling code defaults to "+355"

---

---

### User Story 4 - Add Discovery Question Option (Priority: P2)

Marketing team identifies new traffic source (medical tourism forums); admin needs to add new discovery question option to track this source.

**Why this priority**: Business intelligence requirement; helps track marketing effectiveness.

**Independent Test**: Can be fully tested by: (1) Admin adds "Medical Tourism Forum" option via UI, (2) Reorder options via drag-and-drop, (3) Wait 1 minute, (4) Patient registers on app, (5) Verify new option appears in discovery question.

**Acceptance Scenarios**:

1. **Given** admin is logged in and has the View Settings permission and the edit permission of the screen, **When** admin navigates to Settings → App Data → Discovery Questions, **Then** system displays current options (Social Media, Search Engine, Friend Referral, Online Ad)
2. **Given** admin clicks "Add Option", **When** admin enters "Medical Tourism Forum", **Then** system validates option uniqueness
3. **Given** admin added new option, **When** admin uses drag-and-drop to reorder options, **Then** system updates display order (1, 2, 3, 4, 5)
4. **Given** admin saved new option and submitted reason modal with "Tracking forum traffic", **When** patient registers on Patient app 1 minute later, **Then** "Medical Tourism Forum" appears in discovery question dropdown
5. **Given** patient selects "Medical Tourism Forum" during registration, **When** admin views analytics, **Then** selection is tracked and reported in discovery question analytics

---

### User Story 5 - Manage Inquiry Cancellation Reasons (Priority: P2)

Product team receives patient feedback suggesting a new cancellation reason category; admin adds it to the centralized list.

**Why this priority**: Enables data-driven understanding of why patients cancel inquiries; must be adjustable without code deployment.

**Independent Test**: Can be fully tested by: (1) Admin adds new reason via UI, (2) Submit reason modal, (3) Wait 1 minute, (4) Patient initiates inquiry cancellation on app, (5) Verify new reason appears in cancellation modal.

**Acceptance Scenarios**:

1. **Given** admin is logged in and has the View Settings permission and the edit permission of the screen, **When** admin navigates to Settings → App Data → Inquiry Cancellation Reasons, **Then** system displays current list of active reasons with usage counts
2. **Given** admin clicks "Add Reason", **When** admin enters "Provider communication issues" with Requires Explanation = Yes, **Then** system validates label uniqueness
3. **Given** admin added new reason and reordered via drag-and-drop, **When** admin clicks Save and submits reason modal with "Adding cancellation tracking category from patient feedback", **Then** system versions reason list, creates audit log
4. **Given** admin saved new reason at least 1 minute ago, **When** patient taps Cancel Inquiry on Patient app, **Then** "Provider communication issues" appears in reason selector with mandatory explanation field
5. **Given** admin deactivates "Travel restrictions" reason, **When** patient who previously cancelled with that reason is viewed in analytics, **Then** historical data retains "Travel restrictions" label

---

### User Story 6 - View Version History for Audit Compliance (Priority: P2)

Compliance officer requests complete audit trail of all authentication policy changes for quarterly audit report.

**Why this priority**: Regulatory compliance requirement; demonstrates control over security configurations.

**Independent Test**: Can be fully tested by: (1) Admin makes 5 configuration changes over time, (2) Compliance officer requests audit review, (3) Admin views version history in UI, (4) Verify all changes captured with who/when/what.

**Acceptance Scenarios**:

1. **Given** compliance officer requests audit trail, **When** admin navigates to Settings → Authentication & Security → Authentication Throttling → Version History, **Then** system displays complete version history
2. **Given** version history displayed, **When** admin selects date range filter (Q3 2025), **Then** system displays only versions created in that quarter
3. **Given** version history contains 50+ entries, **When** admin scrolls to bottom of page, **Then** system loads next 50 entries (pagination)
4. **Given** admin views specific version, **When** admin clicks "View Details", **Then** system displays diff view highlighting changed fields (red: removed, green: added)

---

### User Story 7 - Manage Inquiry Configuration (Priority: P1)

Admin needs to manage the treatment-area choices and minimum inquiry lead time without a code deployment, while keeping the patient inquiry flow and submission validation aligned.

**Why this priority**: Inquiry creation depends on this configuration; the patient calendar and backend validation must use the same current value.

**Independent Test**: Can be fully tested by: (1) Admin creates or updates a treatment-area option with an approved S-05 asset, sets the lead time, and submits the change reason; (2) Verify versioning, audit entry, and cache invalidation; (3) Retrieve the active configuration as a patient; (4) submit an inactive option and an early date; (5) confirm both are rejected and historical inquiries retain their saved snapshot.

**Acceptance Scenarios**:

1. **Given** admin is logged in with the Manage App Data permission, **When** admin opens Settings → App Data → Inquiry Configuration, **Then** the system displays treatment-area options in display order and the current minimum inquiry lead time.
2. **Given** admin enters a unique label, approved S-05 image/icon URL, display order, active state, and a whole-day lead time from 0 through 730, **When** admin saves with a change reason, **Then** the system versions and audits the update and invalidates the configuration cache.
3. **Given** the configuration change was saved, **When** the patient client retrieves its configuration, **Then** it receives only active ordered options with IDs, labels, image/icon URLs, and `minimum_inquiry_lead_days` together.
4. **Given** an option has become inactive or a selected date is earlier than the configured threshold, **When** the patient submits an inquiry, **Then** backend validation rejects the submission.
5. **Given** an inquiry was submitted with an active treatment-area option, **When** that option is later changed or deactivated, **Then** the historical inquiry retains its original treatment-area snapshot.

---

### User Story 8 - Manage Quote Configuration (Priority: P1)

Admin needs one versioned source for the quote expiry window, the slot-hold duration, and their reminder lead times, with the quote currency taken from FR-029.

**Independent Test**: Change the quote expiry window and the slot-hold duration with a reason; verify version/audit records and cache invalidation; send a new quote and confirm its currency, expiry, and recorded configuration version; confirm a quote sent earlier and a hold placed earlier are unchanged.

**Acceptance Scenarios**:

1. **Given** a quote expiry window of 24 to 336 hours, a slot-hold duration of 24 to 168 hours, and each lead time from 1 hour up to half of its window, **When** Admin saves with a reason, **Then** the system versions and audits the configuration and invalidates its cache.
2. **Given** the new configuration is active, **When** a provider first sends a parent Quote, **Then** FR-004 copies the FR-029 Default Currency and the quote expiry window read-only onto it and records the configuration version; a draft carries neither value.
3. **Given** a quote was sent before the change, **When** configuration changes, **Then** its currency and expiry remain unchanged.
4. **Given** a slot hold was placed before the slot-hold duration changed, **When** the duration changes, **Then** that hold keeps its original end time and only new holds use the new duration.
5. **Given** Admin enters a window outside its bounds, a lead time under 1 hour, or a lead time longer than half of its window, **When** Admin saves, **Then** the system blocks the save and shows a validation error.

---

### User Story 9 - Manage Analytics Configuration (Priority: P2)

Admin needs one versioned source for the thresholds and targets used by FR-014 analytics.

**Independent Test**: Change the SLA target and engagement thresholds with a reason; verify version/audit records and cache invalidation; confirm FR-014 uses the new values on its next calculation and records the configuration version; confirm a previously generated export is unchanged.

**Acceptance Scenarios**:

1. **Given** valid values, **When** Admin saves with a reason, **Then** the system versions and audits the configuration and invalidates its cache.
2. **Given** Admin enters a Dormant Threshold that is not greater than the At Risk Threshold, **When** Admin saves, **Then** the system blocks the save and shows a validation error.
3. **Given** Target Monthly Commission is blank, **When** FR-014 renders Screen 12 Widget 2, **Then** no reference line is shown; **Given** a target is set, **Then** the line appears at that value.
4. **Given** an export was generated before the change, **When** configuration changes, **Then** that export file is not rewritten.

---

### Edge Cases

- What happens when **admin attempts to deactivate one of the last 2 active discovery question options**? System prevents deactivation and displays error: "At least 2 active options required. Cannot deactivate this option." (REQ-026-081)
- How does system handle **concurrent edits by two admins to same setting group**? System detects concurrent edit before save and displays modal popup: "This setting was updated by [admin email] 30 seconds ago. Your changes may conflict. Review the latest version before saving." Modal shows diff of latest changes and options: "Reload Latest Version" or "Save Anyway (Overwrite)". (REQ-026-049)
- What occurs if **Settings API is unreachable during Patient app polling**? Patient app logs error, continues using cached settings until the next successful poll, retries poll every 60 seconds. (REQ-026-046)
- How to manage **sensitive value (API key) visibility in version history**? System masks sensitive values in version history UI (display as "[REDACTED]"); admins with "View Sensitive Settings" permission can click "Show" to unmask. (REQ-026-052)
- How does system handle **settings propagation during Patient app deployment**? Settings API remains available during deployments; Patient app retrieves settings after restart; no data loss. (REQ-026-048)
- What happens when **admin attempts to deactivate the "Other" cancellation reason**? System prevents deactivation and displays error: "'Other' is a fixed reason and cannot be deactivated." (REQ-026-085)
- What happens when **admin attempts to deactivate the "Others" deletion reason**? System prevents deactivation and displays error: '"Others" is a fixed reason and cannot be deactivated.' (REQ-026-090)
- What happens when **admin deactivates a cancellation reason while a patient is mid-cancellation flow**? Patient app uses cached reason list (up to 1 minute stale); if patient submits with a now-deactivated reason, system still accepts the submission (reason was valid at flow start). Next cancellation flow loads updated list. (REQ-026-062)
- What happens when **the Settings API is unavailable as a provider first sends a quote**? FR-004 blocks the send and keeps the quote as a draft; it never sends a quote with a guessed or stale currency or expiry. The provider can retry. (REQ-026-063)
- What happens when **the Settings API is unavailable as a slot hold is placed** (subquote acceptance or an FR-006 admin revive)? The action is blocked and can be retried; no stale or guessed slot-hold duration is used. (REQ-026-144)
- What happens when **admin changes the slot-hold duration while holds are active**? Existing holds keep their original end time; holds placed after the change use the new duration. (REQ-026-030)
- What occurs if **admin deletes country that active patients have selected in profile**? System prevents hard delete (soft delete only); patients who selected deleted country retain selection; country hidden from new users. (REQ-026-078)

---

## Functional Requirements Summary

### Core Requirements

- **REQ-026-001**: System MUST provide Settings Management UI accessible only to admins with the View Settings permission, and editing only to admins with the edit permission of the screen as set in the permission table under Security Controls (FR-031 permissions)
- **REQ-026-002**: System MUST require change reason (10-500 characters) for all setting modifications
- **REQ-026-003**: System MUST version all setting changes with auto-incremented version numbers (v1.0, v1.1, v1.2, etc.)
- **REQ-026-004**: System MUST create immutable audit log for every change capturing: timestamp, admin ID, admin email, setting group, old values, new values, change reason
- **REQ-026-005**: System MUST propagate setting changes to dependent services within 1 minute via polling mechanism
- **REQ-026-006**: System MUST invalidate settings cache immediately upon save to trigger propagation
- **REQ-026-007**: System MUST NOT support rollback. Admins make forward-only changes; version history is read-only.
- **REQ-026-008**: System MUST display version history in reverse chronological order with diff highlighting (old → new)

### Data Requirements

- **REQ-026-009**: System MUST store authentication throttling settings: max login attempts (1-10), lockout duration (5-60 minutes)
- **REQ-026-145**: System MUST keep one failed-attempt counter per account, shared by sign-in and verification-code entry (a wrong password and a wrong code count together, REQ-001-180). The counter MUST return to zero after a successful sign-in or code entry and when a lockout ends. A lowered Max Login Attempts MUST apply from the next failed attempt: an account already at or above the new limit locks on its next failure, and saving the setting locks no account.
- **REQ-026-010**: System MUST store OTP configuration: expiry time (5-30 minutes), resend cooldown (30-300 seconds), max resend attempts (3-10)
- **REQ-026-011**: System MUST store centrally managed country list: country name, ISO code, calling code, country flag asset URL (stored via S-05 Media Storage; required when an admin adds a country, the admin uploads the flag on Screen 4; a seeded country may have none and an imported country has none until uploaded), display order, active status
- **REQ-026-012**: System MUST store centrally managed discovery question options: answer option, display order, active status
- **REQ-026-012a**: System MUST store centrally managed inquiry cancellation reason options: reason label, requires_explanation flag, display order, active status. Consumer: FR-003 Screen 8a. (graph id REQ-026-032)
- **REQ-026-012b**: System MUST store centrally managed account deletion reason options: reason label, requires_explanation flag, display order, active status. Consumer: FR-001 Screen 16. (graph id REQ-026-033)
- **REQ-026-012c**: System MUST store centrally managed inquiry treatment-area options: stable option ID, label, image/icon asset URL, display order, and active status. Consumer: FR-003 Screen 1. (graph id REQ-026-034)
- **REQ-026-012d**: System MUST store a versioned minimum inquiry lead time as a whole number of days from 0 through 730. Default: 3 days. Consumer: FR-003 Screen 5 and submission validation. (graph id REQ-026-035)
- **REQ-026-012e**: System MUST prevent deactivation of the final active inquiry treatment-area option. (graph id REQ-026-036)
- **REQ-026-139**: System MUST store the centrally managed problem-duration list: option label, display order, active status. Starting values, editable by Admin: Less than 6 months; 6 to 12 months; 1 to 2 years; 2 to 5 years; More than 5 years. At least one option stays active. Consumer: FR-003 Screen 3 (Duration).
- **REQ-026-012f**: System MUST store one versioned Quote Configuration containing the quote expiry window (whole hours from 24 to 336, default 48), the quote-expiring-soon lead time (whole hours from 1 up to half of the expiry window, default 12), the slot-hold duration (whole hours from 24 to 168, default 48), and the hold-expiring-soon lead time (whole hours from 1 up to half of the slot-hold duration, default 12). The quote currency MUST be the FR-029 Default Currency, not a separate setting, and each change to the FR-029 Default Currency MUST create a new Quote Configuration version so the version recorded on a quote identifies both the hours and the currency used. Consumers: FR-004 (currency, expiry window, quote-expiring-soon lead time), FR-005 and FR-006 (slot-hold duration), and FR-006 (hold-expiring-soon lead time). (graph id REQ-026-037)
- **REQ-026-012g**: System MUST store one versioned Analytics Configuration containing TTFQ SLA target (positive whole minutes, default 120), At Risk threshold (whole days, default 7), Dormant threshold (whole days, greater than At Risk, default 30), price outlier threshold (whole percent 1-100, default 30), benchmark refresh frequency (Daily, Weekly, or Monthly; default Weekly), and optional target monthly commission (blank by default). Consumer: FR-014. (graph id REQ-026-038)
- **REQ-026-012h**: System MUST store a centrally managed Provider Specialties list: stable specialty ID, specialty name (max 100 chars, unique case-insensitive), display order, active status; seeded with Hair Transplant Surgeon, Dermatologist, Trichologist, Plastic Surgeon, Other. Admins can add, rename, reorder, and deactivate values (no hard delete); at least one value MUST remain active; changes MUST be versioned and audit-logged. Deactivated values MUST be hidden from new selection while providers that hold them keep and still display them; renames MUST apply to display everywhere. Consumer: FR-015 Screen 2 Step 2 and Screen 3 Tab 1. (graph id REQ-026-039)
- **REQ-026-013**: System MUST store OTP email templates: template name, subject line, HTML body, plain text body, version number

### Security & Privacy Requirements

- **REQ-026-014**: System MUST mask sensitive values (API keys, secrets) in UI and audit logs (display as "••••••••" or "[REDACTED]")
- **REQ-026-015**: System MUST restrict "View Sensitive Settings" permission to authorized admins only
- **REQ-026-016**: System MUST encrypt sensitive values at rest using AES-256
- **REQ-026-017**: Multi-factor authentication for admin access to Settings Management UI is a future (non-MVP) requirement and MUST be enforced once the shared MFA stack (FR-031) is delivered.
- **REQ-026-018** (retired): Settings API rate limiting moved to the system PRD, which holds one Rule shared with the matching FR-028 admin rate limit
- **REQ-026-019** (retired): Audit log retention moved to the system PRD, Platform-Wide Rules: One 10-year retention period
- **REQ-026-020**: System MUST validate all admin inputs to prevent XSS, SQL injection, command injection attacks

### Integration Requirements

- **REQ-026-021**: System MUST expose Settings API (RESTful) for dependent services to poll configurations
- **REQ-026-022**: Settings API MUST return JSON response with version number, setting values, and last modified timestamp
- **REQ-026-023**: Settings API MUST support OAuth 2.0 authentication with "read:settings" or "write:settings" scopes
- **REQ-026-024**: System MUST NOT expose a rollback API.
- **REQ-026-025**: The patient configuration response MUST return active ordered treatment-area options and `minimum_inquiry_lead_days` together so the client calendar and backend validator use one configuration source.
- **REQ-026-026**: The authenticated Settings API MUST return the quote currency, the quote expiry window, both lead times, the slot-hold duration, the configuration version, and the last-modified timestamp together, so FR-004 sends each parent Quote from one consistent configuration version and can record that version on the quote.
- **REQ-026-027**: Quote Configuration changes MUST affect only quotes first sent after activation; the currency and expiry already copied onto a sent quote MUST remain unchanged, drafts MUST carry neither value, and no per-quote extension is allowed except the admin restore of an expired quote (REQ-004-105) and the admin-authored replacement quote (REQ-004-036), which captures its currency at its first Screen 8 save (REQ-004-082).
- **REQ-026-028**: The authenticated Settings API MUST return all Analytics Configuration values with the configuration version and last-modified timestamp so FR-014 calculations use one consistent version and can record it with their aggregates.
- **REQ-026-029**: Analytics Configuration changes MUST apply from FR-014's next calculation or benchmark refresh to every period then displayed (past periods are not frozen), and MUST NOT rewrite exports or scheduled-export files that were already generated.
- **REQ-026-030**: Each slot hold MUST use the slot-hold duration in effect when the hold is placed (at subquote acceptance or an FR-006 admin revive); later changes MUST NOT alter an existing hold, and payment failure MUST NOT extend or restart a hold.
- **REQ-026-031**: Changes to the quote-expiring-soon or hold-expiring-soon lead time MUST apply only to reminders not yet sent; when a lead time is raised and a reminder's time has already passed, that reminder MUST be skipped, not sent late.

### Platform Settings Requirements

- **REQ-026-112**: System MUST store a Re-Verification Threshold Setting (whole minutes from 1 to 60, default 5, the value FR-001 uses), the time after a patient's last successful sign-in beyond which FR-001 asks the patient to confirm identity again before a sensitive action. Consumer: FR-001 Screens 16 and 18.
- **REQ-026-113**: System MUST let an admin manage the Landing Background Images Setting, the set of background images that rotate behind the patient landing screen; with none set, no background images are shown. Consumer: FR-001.
- **REQ-026-114**: System MUST store Profile Photo Accepted Formats (default JPG and PNG) and Profile Photo Maximum Size (default 5 MB) as admin-changeable Settings. Consumer: FR-001 REQ-001-082.
- **REQ-026-115**: System MUST store the Support Emergency Contact Phone and Support Emergency Contact Email Settings, with no default, for display read-only on the patient Help & Support Hub. A save that changes either value and leaves both blank is refused with a message; other Screen 8 rows can be saved while both are blank (REQ-026-143). Consumer: FR-035 Screen 1.
- **REQ-026-116**: System MUST store the admin session Settings: concurrent sessions per admin user (1 to 5, default 3), the admin inactivity timeout (whole minutes from 5 to 240, default 30), and no separate admin failed-login Setting: failed admin sign-ins use the shared Max Login Attempts Setting of Screen 2, and the fixed FR-031 endpoint throttle of 5 attempts per 15 minutes applies in addition, whichever trips first (REQ-031-100). A Login as Provider session ends after its own fixed 30 minutes of inactivity (REQ-015-026) or when the admin's own session ends under the admin inactivity timeout, whichever comes first. When an admin signs in while already at the concurrent-session limit, the oldest session is ended and the new one opens; a change to the session limit or the inactivity timeout applies from each open session's next request, and sessions above a lowered limit are ended oldest first. Consumer: FR-031.
- **REQ-026-117**: System MUST store the head scan Settings FR-002 still reads: a minimum brightness score and a minimum blur score (each a whole number from 0 to 100, default 40, admin-editable; a photo passes when both reach their minimum), and head video duration limits, which are not used until head video ships (REQ-002-035). File size, total size and required views are product constants in FR-002 (REQ-002-033, REQ-002-032) and are not Settings. Consumer: FR-002 REQ-002-034, REQ-002-035, REQ-002-050.
- **REQ-026-118**: System MUST store the acceptance legal copy and terms acknowledgment text shown at quote acceptance as a versioned Setting, with no seeded text; until the admin sets it, the quote acceptance action that needs the acknowledgment checkbox is blocked with a message. Consumer: FR-005.
- **REQ-026-119**: System MUST offer the registration question "How did you find out about us?" from the Discovery Questions options managed on Screen 5. Consumer: FR-001.
- **REQ-026-120**: System MUST store the provider notification types offered in provider notification preferences, seeded with the five core types. Admins can add or remove types, but the core types (quote, schedule, treatment, aftercare, review) cannot be removed. Consumers: FR-032, FR-020.
- **REQ-026-121**: System MUST store the timezone options (every whole-hour offset from GMT-12 to GMT+14 at launch, each with its offset and a city example). Consumers: FR-032, FR-021.
- **REQ-026-140**: System MUST list on Screen 8, under the group "Limits owned by other features", the Settings whose owning FR makes them admin-editable: the treatment creation rate limit and the package creation rate limit (FR-024; a new record counts once, when first saved as Active or Inactive), the admin invitation token expiry and the admin repeated denial threshold (FR-031). Range, default and counting rule stay with the owning FR.
- **REQ-026-141**: System MUST prevent deactivation of the final active country; a deactivation that would leave no active country is rejected with a message.
- **REQ-026-142**: A Quote Configuration version created by a Default Currency change in FR-029 (REQ-029-053) MUST have Change Type "System", the fixed reason text "Default currency changed in Payment Configuration", and Changed By set to the admin who confirmed the change in FR-029; the change reason rule (REQ-026-002) covers changes made on FR-026 screens.
- **REQ-026-143**: System MUST refuse a save that changes the Support Emergency Contact Phone or Email when it leaves both blank, with the message "Set at least one emergency contact (phone or email)."; a save that changes neither value is not checked, so other Screen 8 rows can be saved while both are blank, as at launch. While both are blank the patient Help & Support Hub hides the emergency contact section (REQ-035-040).
- **REQ-026-144**: When the Settings API is unavailable as a slot hold is placed at subquote acceptance or an FR-006 admin revive, the action MUST be blocked and can be retried; no stale or guessed slot-hold duration is used.

### Screen Field Limits and Behaviours

- **REQ-026-122**: On Screen 4, Country Name MUST be at most 100 characters and unique; ISO Code MUST be exactly 2 uppercase letters and unique; Calling Code MUST be "+" followed by 1 to 4 digits; Display Order MUST be a whole number (default 999); Country Flag MUST be an SVG or PNG file of at most 1 MB.
- **REQ-026-123**: On Screen 5, Answer Option MUST be at most 100 characters and unique; Display Order MUST be a whole number (default 999).
- **REQ-026-124**: On Screen 5a, Reason Label MUST be at most 100 characters and unique; Display Order MUST be a whole number (default 999); "Other" always requires an explanation.
- **REQ-026-125**: On Screen 5b, Reason Label MUST be at most 100 characters and unique; Display Order MUST be a whole number (default 999); "Others" always requires an explanation.
- **REQ-026-126**: On Screen 5c, Treatment Area Label MUST be at most 100 characters and unique among active options; Display Order MUST be a unique whole number.
- **REQ-026-127**: On Screen 6, Subject Line MUST be at most 200 characters, Email Body (HTML) at most 50,000 characters, and Email Body (Plain Text) at most 10,000 characters.
- **REQ-026-128**: Screen 4 MUST offer bulk import of countries from a CSV file with no flag column, with validation of every row before anything is saved. An imported country is saved Inactive with the state "flag missing", which means its flag is empty, and cannot be activated until the admin uploads its flag.
- **REQ-026-129**: Before an admin deactivates a country that active users have selected, a discovery option, cancellation reason, or deletion reason that patients frequently select, or a provider specialty that providers currently hold, the system MUST warn the admin.
- **REQ-026-130**: Screen 7 MUST let an admin filter version history by date range, admin, and change type, and MUST show 50 entries per page.
- **REQ-026-131**: Screen 6 MUST let an admin switch between the Verification Email and Password Reset Email templates without leaving the screen.
- **REQ-026-132**: Screen 2 MUST show an admin a warning when a change reduces security (more attempts allowed or a shorter lockout).
- **REQ-026-045**: The system validates admin input before save and rejects an out-of-range value with an error message stating the valid range (for example, "Max Login Attempts must be between 1 and 10" for 0); the admin corrects the value and the system re-validates.
- **REQ-026-138**: After a successful save of the authentication throttling policy, the system shows a success message that names the setting group and the new version, for example "Authentication throttling updated successfully (v1.3)".

---

## Appendix: Change Log

| Date       | Version | Changes                                 | Author       |
| ---------- | ------- | --------------------------------------- | ------------ |
| 2026-11-22 | 1.17 | Requirements graph programme baseline: PRD compressed to the checklist structure (each rule stated once, field rows tagged with graph field ids, dropped classes removed). No rule changes. Earlier history (v1.0 to v1.16) and the change requests (change-request-2026-09-04-inquiry-configuration.md, change-request-2026-09-10-quote-configuration-ownership.md, CR-FR026-20261013-01 in change-request-2026-10-13-analytics-configuration.md, CR-FR026-20261015-01 in change-request-2026-10-15-provider-specialty-list.md, CR-FR026-20261016-01 in change-request-2026-10-16-mtg002-quote-model-alignment.md) are in `archived/prd-baseline-2026-11-08/` and in git history. | Product Owner / Documentation |
| 2026-11-23 | 1.18 | Independent compression review: 2 clause(s) from dropped sections restored in original wording under Business Rules. No rule changes. | Product Owner / Documentation |
| 2026-11-24 | 1.19 | Logic review pass 1: permissions replace the working role names, with a screen-to-permission table (REQ-026-001, REQ-026-054); treatment areas seeded Hair, Beard and Both (REQ-026-034); head scan Settings reduced to two quality minimums (default 40 each) and video limits marked unused (REQ-026-117); admin sign-in uses the shared lockout and the fixed FR-031 throttle together (REQ-026-116); Change Type System for FR-029 currency versions (REQ-026-142); creation limits owned by other features listed on Screen 8 (REQ-026-140); reminder skip rule when a lead time is raised (REQ-026-031); country CSV columns, final active country guard and deactivation warning for FR-028 (REQ-026-128, REQ-026-141, REQ-026-129); emergency contact at-least-one rule (REQ-026-143); bounds for the re-verification threshold and admin inactivity timeout; seeding and empty rules for timezones, notification types, landing images, acceptance terms; Settings API outage at hold placement (REQ-026-144). | Product Owner / Documentation |
| 2026-11-24 | 1.20 | Logic review pass 2: one shared failed-attempt counter with reset and lowered-limit rule (REQ-026-145); admin session limit and timeout enforcement (REQ-026-116); flag upload added to the country scenario (REQ-026-122); expiry value in the email variable and resend under the version and expiry in force (REQ-026-072, REQ-026-073, REQ-026-106); admin times in the browser timezone (REQ-026-050); emergency contact check only on a save that changes those rows (REQ-026-143); flag missing means an empty flag (REQ-026-011, REQ-026-128); stale head scan wording fixed. | Product Owner / Documentation |

---

## Appendix: Approvals

| Role           | Name                     | Date       | Signature/Approval |
| -------------- | ------------------------ | ---------- | ------------------ |
| Product Owner  | Hairline Product Owner   | 2025-12-11 | ✅ Approved         |
| Technical Lead | Hairline Technical Lead  | 2025-12-11 | ✅ Approved         |
| Security Lead  | Hairline Security Lead   | 2025-12-11 | ✅ Approved         |
| Product Owner  | Hairline Product Owner   | 2026-10-16 | ✅ Approved (v1.13 documentation; implementation reconciliation required) |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (PRD Standards & Requirements)
**Based on**: FR-011 Aftercare & Recovery Management PRD, FR-026 from system-prd.md
**Last Updated**: 2026-11-24
