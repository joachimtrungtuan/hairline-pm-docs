# FR-030 - Notification Rules & Configuration

**Module**: A-09: System Settings & Configuration | S-03: Notification Service
**Feature Branch**: `fr030-notification-rules-config`
**Created**: 2025-11-13
**Status**: ✅ Verified & Approved
**Source**: FR-030 from system-prd.md

---

## Executive Summary

The Notification Rules & Configuration module provides comprehensive administrative control over the Hairline platform's notification system. This module enables admins to configure event-to-notification mappings, define delivery channels (email, push, and SMS in future phases), manage notification templates, and establish recipient preferences across all three platform tenants (Patient, Provider, Admin). By centralizing notification configuration, the system ensures consistent, timely, and appropriate communication with all platform users while maintaining flexibility to adapt notification strategies as the business evolves. **In MVP, only email and push are available; SMS is an optional channel planned for later phases once S-03 SMS support is enabled.**

This module extends the foundational OTP template management capabilities from FR-026 (App Settings & Security Policies) to encompass all notification types across the platform, creating a unified notification governance system.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (Mobile App)**: Receives notifications based on configured rules; users cannot modify system-level notification rules but can manage their personal preferences
- **Provider Platform (Web)**: Receives notifications based on configured rules; providers can manage personal notification preferences within admin-defined boundaries
- **Admin Platform (A-09)**: Full administrative control over notification rule configuration, template management, channel preferences, and testing capabilities
- **Shared Services (S-03)**: Notification Service executes configured rules, manages delivery across channels, tracks delivery status, and maintains notification logs

### Multi-Tenant Breakdown

**Patient Platform (Mobile App)**:

- Patients receive notifications triggered by system events (quote received, booking confirmed, payment due, aftercare milestone, etc.)
- Patients can view notification history in-app
- Patients can manage personal notification preferences within boundaries set by admin (e.g., cannot disable critical payment notifications)
- Notifications delivered via email and push notifications in MVP; SMS delivery is optional and only becomes available in later phases when enabled in S-03/FR-020.

**Provider Platform (Web)**:

- Providers receive notifications for inquiries, quote responses, booking confirmations, payment receipts, patient arrivals, aftercare escalations
- Providers can manage team notification routing (which staff members receive which notification types)
- Providers can set business hours for non-urgent notifications
- Notifications delivered via email and web push notifications

**Admin Platform (A-09)**:

- Admins configure notification rules: which events trigger notifications, to whom, via which channels
- Admins create and edit notification templates with dynamic variables and multi-language support
- Admins define channel preferences per event type and recipient type
- Admins test notification rules before activation
- Admins monitor notification delivery metrics and troubleshoot failed deliveries
- Admins manage notification escalation rules for time-sensitive events

**Shared Services (S-03)**:

- S-03 Notification Service consumes configured rules from A-09
- Evaluates event triggers in real-time and determines recipients and channels
- Renders notification templates with dynamic data
- Manages delivery queue and retry logic for failed deliveries
- Tracks delivery status (sent, delivered, opened, failed) per channel
- Provides delivery logs and metrics to A-09 for monitoring

### Communication Structure

**In Scope**:

- Email notification configuration and template management
- Push notification (mobile and web) configuration and template management
- SMS notification configuration for critical events (optional, admin-enabled, **not available in MVP; SMS becomes usable only when S-03 SMS delivery is implemented in a later phase**)
- Event-to-notification mapping (which events trigger which notifications)
- Recipient rule configuration (who receives notifications based on role, relationship, preferences)
- Channel preference configuration per event type and recipient type
- Notification template editor with variable substitution and preview
- Multi-language notification template support
- Notification testing and preview capabilities
- Delivery status tracking and retry management
- Notification analytics and delivery metrics

**Out of Scope**:

- Real-time chat/messaging between users (handled by P-06: Communication)
- Video consultation notifications (covered under aftercare-specific notifications)
- Third-party notification platform integrations beyond email, SMS, push (e.g., WhatsApp, Telegram - future enhancement)
- User-to-user notification forwarding or sharing
- Notification content personalization based on AI/ML (future enhancement)

### Entry Points

Admins access notification configuration through:

1. **Admin Dashboard → Settings → Alerts & Notifications**: Primary entry point for notification rule management and notification template setup
2. **Admin Dashboard → Settings → Alerts & Notifications**: Dedicated area for managing notification templates (email, push, SMS in future)
3. **Event-driven**: System events automatically trigger notification evaluation based on configured rules (S-03)
4. **Template Testing**: Admins can send test notifications to themselves before activating rules

Activation method: Notification rules activate immediately upon saving (with confirmation prompt). Template changes apply to new notifications immediately; in-flight notifications use the template version active at creation time.

---

## Admin-Configurable Notification Event Catalog (Preset by Backend)

### Core Rule

- The list of notification events that appear in **`Settings → Alerts & Notifications`** is a **preset backend event catalog**.
- Admins can **only configure events that appear in this catalog UI** (enable/disable, channels, timing, templates, retries, escalation).
- **If an event does not appear in the catalog UI, it cannot be configured** (it is either not implemented, not enabled for the current environment, or intentionally not exposed).

### MVP: Admin-Configurable Event Types (Shown in UI)

Below is the platform-wide set of events that MUST be configurable by admins in MVP. This table is the **source of truth** for MVP notification event coverage (FR-020 must align to this catalog).

Notes:

- **Backend event keys** below are **illustrative**. The backend owns the final canonical keys, but they MUST be stable identifiers exposed via the event catalog API.
- If an event is not present in this table, it should **not appear** in `Settings → Alerts & Notifications` and therefore **cannot be configured**.

| Category | Event (Display Name) | Example Backend Event Key | Primary Recipients | Notes |
|----------|-----------------------|---------------------------|--------------------|-------|
| Account/Auth | Email Verification / OTP Code | `account.email_verification_code` | Patient, Provider, Admin | Extends FR-026 OTP templates; **security-critical** and non-disableable by default |
| Account/Auth | Password Reset Code / Link | `account.password_reset` | Patient, Provider, Admin | **Security-critical** and non-disableable by default |
| Account/Auth | New Account Created (Welcome / Onboarding) | `account.created` | Patient, Provider | Optional; can be disabled if not needed |
| Inquiry | Inquiry Submitted (Provider notified) | `inquiry.submitted` | Provider | “New inquiry matching clinic/location” |
| Inquiry | Inquiry Cancelled | `inquiry.cancelled` | Provider, Patient (optional), Admin (optional) | Patient-initiated inquiry cancellation (FR-003 Workflow 5). Fires when patient cancels inquiry in Inquiry, Quoted, or Accepted stages. Cancellation reason is patient-private — provider notification says only "Inquiry cancelled by patient". |
| Quote | Quote Submitted / Ready (Patient notified) | `quote.submitted` | Patient | Starts quote expiry timer (see below) |
| Quote | Quote Updated / Revised | `quote.updated` | Patient, Provider | Notify on meaningful changes (price/package/dates) |
| Quote | Quote Expiring Soon | `quote.expiring_soon` | Patient, Provider | Default expiry window is policy-bound (e.g., 48h) |
| Quote | Quote Expired | `quote.expired` | Patient, Provider | Sent on expiry processing completion |
| Quote | Quote Accepted | `quote.accepted` | Provider, Patient, Admin (optional) | Provider receives acceptance details |
| Quote | Quote Declined | `quote.declined` | Provider, Patient (optional) | Useful for provider follow-up / analytics |
| Quote | Quote Cancelled (Inquiry Cancelled) | `quote.cancelled_inquiry` | Provider | Auto-cancelled quote due to patient inquiry cancellation (FR-003 Workflow 5). Provider receipt is mandatory — admin cannot disable this event. Cancellation reason is patient-private; provider notification says only "Inquiry cancelled by patient". |
| Booking/Schedule | Booking Scheduled (Pending Payment) | `booking.scheduled` | Patient, Provider | “Schedule notifications” prior to payment confirmation |
| Booking/Schedule | Booking Confirmed | `booking.confirmed` | Patient, Provider | Critical |
| Booking/Schedule | Booking Rescheduled | `booking.rescheduled` | Patient, Provider | Critical if schedule changes |
| Booking/Schedule | Booking Cancelled | `booking.cancelled` | Patient, Provider, Admin (optional) | Include cancellation reason where appropriate |
| Booking/Schedule | Appointment Reminder | `booking.appointment_reminder` | Patient, Provider | Scheduled reminders; policy-driven |
| Treatment | Treatment Start / Day-1 Starting | `treatment.started` | Patient, Provider | “Treatment start notifications” |
| Treatment | Treatment Cancelled | `treatment.cancelled` | Patient, Provider, Admin (optional) | Used when treatment is cancelled after scheduling/confirmation |
| Treatment | Treatment Completed (Post‑Op Instructions) | `treatment.completed` | Patient, Provider, Admin (optional) | Completion confirmation; triggers post-op and aftercare next steps |
| Treatment | Treatment Documentation Completed | `treatment.documentation_completed` | Provider | Sent when treatment documentation is successfully saved |
| Treatment | Task In Progress Reminder | `treatment.task_in_progress_reminder` | Provider | Reminder for incomplete treatment tasks or documentation |
| Payment | Payment Received / Receipt | `payment.received` | Patient, Provider, Admin (optional) | Critical |
| Payment | Payment Failed | `payment.failed` | Patient, Admin (optional) | Critical |
| Payment | Payment Due Reminder (Installment / Balance) | `payment.due_reminder` | Patient | “Installment reminder” (split-pay compatible) |
| Billing/Payouts | Provider Payout Processed | `payout.provider_processed` | Provider, Admin (optional) | “They’ve been paid” notification to provider |
| Billing/Payouts | Affiliate Payout Processed | `payout.affiliate_processed` | Affiliate, Admin (optional) | If affiliate program is enabled |
| Billing/Payouts | Payout Failed | `payout.failed` | Admin, Provider (optional), Affiliate (optional) | Failure processing payout; recipients depend on payout type |
| Messaging/Support | New Message Received | `message.received` | Patient, Provider, Admin (optional) | Real-time notification for new messages |
| Messaging/Support | Support Case Created | `support.case_created` | Patient, Provider, Admin | Sent to submitter confirming case creation with case ID; Admin notification if case is urgent or unassigned |
| Messaging/Support | Support Case Assigned | `support.case_assigned` | Admin | Sent to assigned admin when case is assigned to them |
| Messaging/Support | Support Case Status Changed | `support.case_status_changed` | Patient, Provider | Sent when case status changes (Open → In Progress, In Progress → Resolved); includes status update and context |
| Messaging/Support | Support Case Admin Reply | `support.case_admin_reply` | Patient, Provider | Sent when admin replies to case in communication thread; includes message content |
| Messaging/Support | Support Case User Reply | `support.case_user_reply` | Admin | Sent to assigned admin (or all support staff if unassigned) when patient/provider replies to case |
| Messaging/Support | Support Case Resolved | `support.case_resolved` | Patient, Provider | Sent when case is marked as Resolved; includes resolution summary and feedback resolution (if applicable) |
| Messaging/Support | Support Case Reopened | `support.case_reopened` | Patient, Provider, Admin | Sent when closed case is reopened; includes reopening reason |
| Messaging/Support | Support Case Closed | `support.case_closed` | Patient, Provider | Sent when case is closed (final status); includes resolution summary |
| Messaging/Support | Support Case Escalated | `support.case_escalated` | Admin | Sent to escalation recipient (senior admin or technical team) when case is escalated |
| Aftercare | Aftercare Activated | `aftercare.activated` | Patient, Provider | Includes assigned provider/clinician info where applicable |
| Aftercare | Aftercare Milestone Due | `aftercare.milestone_due` | Patient, Provider (optional) | Milestone-driven reminders |
| Aftercare | Scan Due / Missed Scan Reminder | `aftercare.scan_due` / `aftercare.scan_missed` | Patient | “Missed scans MUST trigger reminder notifications” |
| Aftercare | Questionnaire Due / Missed Questionnaire Reminder | `aftercare.questionnaire_due` / `aftercare.questionnaire_missed` | Patient | “Questionnaire due” + reminder if missed |
| Aftercare | Aftercare Escalation / Red Flag Triggered | `aftercare.escalation_triggered` | Provider, Admin, Patient (optional) | Critical; escalation recipients configurable |
| Aftercare | Standalone Aftercare Payment Confirmed | `aftercare.standalone_payment_confirmed` | Patient, Provider (optional), Admin (optional) | Used for standalone aftercare flow payment confirmation |
| Reviews | Review Request | `review.requested` | Patient | “Review notifications” (typically post-treatment) |
| Promotions/Discounts | Provider Approval Needed for Platform Discount | `promotion.discount_approval_requested` | Provider | “Approval notifications to providers when new platform discount is created” |
| Provider/Compliance | Provider Onboarding Requested | `provider.onboarding_requested` | Admin | New provider onboarding request awaiting review/approval |
| Provider/Compliance | Provider Document Expiration Warning | `provider.document_expiration_warning` | Admin, Provider (optional) | License/credential expiry warnings; timing is policy-driven |
| System/Operations | System Escalation | `system.escalation` | Admin | Operational escalation events requiring admin action |
| System/Operations | System Alert | `system.alert` | Admin | System health/monitoring alerts surfaced via notifications |

### Post‑MVP / Hidden Events (Not Shown in UI Until Enabled)

These event types may exist in backend roadmap but MUST NOT appear in admin UI until the backend supports them end-to-end and product enables them.

| Category | Event (Display Name) | Example Backend Event Key | Notes |
|----------|-----------------------|---------------------------|-------|
| Channels | SMS Delivery Enabled | `channel.sms_enabled` | SMS is future; **not available in MVP** |
| Aftercare | Medication / Washing / Activity Reminders | `aftercare.medication_reminder` / `aftercare.washing_reminder` / `aftercare.activity_reminder` | Scheduled reminders referenced in system PRD; enable when milestone engine supports schedules |
| Travel | Passport / Travel Document Required | `travel.passport_required` | Only show once travel module + event publishing exists |
| Travel | Flight / Hotel Itinerary Updates | `travel.itinerary_updated` | Post‑release travel roadmap |

## Business Workflows

### Main Flow: Admin Reviews Event Catalog and Toggles / Configures Notification Rules

**Actors**: Admin (Hairline operations team), S-03 Notification Service (system), Recipient (Patient/Provider)
**Trigger**: Admin opens `Settings → Alerts & Notifications` to review the backend event catalog and (per event) enable/disable notifications and configure channels/timing/templates.
**Outcome**: Selected event(s) are enabled/disabled and/or configured; S-03 uses the saved configuration when those backend events occur

**Steps**:

1. Admin navigates to Admin Platform → `Settings → Alerts & Notifications`
2. System displays the **backend event catalog** (grouped by category) with each row showing current status (Enabled/Disabled), channels, and last modified
3. Admin selects an event row (e.g., "Payment Due Reminder") and reviews its current configuration
4. Admin toggles the event **On/Off**:
   - If toggled **Off**, S-03 will not send notifications for this event (except where policy marks it critical/non-disableable). **Security-critical events (OTP verification, password reset) are non-disableable by default** and must show a locked toggle.
   - If toggled **On**, the event becomes active using its saved configuration
5. Admin clicks **Configure** (or expands the row) to edit settings for that event
6. System displays event-specific configuration options (channels, timing, templates, retries, escalation)
7. Admin configures recipient rules (where applicable):
   - Recipient type: Patient (booking owner)
   - Additional recipients: None (or specify admin roles if escalation needed)
8. Admin configures channel preferences:
   - Email: Enabled (required for payment reminders)
   - Push notification: Enabled
   - SMS: Optional (admin can enable for critical payment reminders in future phases; **SMS is not available in MVP**)
9. Admin selects notification template for each enabled channel:
   - Email template: "Payment Reminder - 3 Days Before Due"
   - Push template: "Payment Due Soon"
   - SMS template: "Payment Reminder" (if enabled in a later phase)
10. Admin configures delivery timing:
    - Trigger: 3 days (72 hours) before installment due date
    - Delivery time: 9:00 AM in recipient's local timezone
    - Retry logic: Retry once after 1 hour if email delivery fails
11. Admin configures escalation rules (optional):
    - If payment still not received 24 hours after reminder, escalate to admin billing team
12. Admin previews notification templates with sample data
13. System renders templates with placeholder data and displays preview
14. Admin clicks "Save Draft" to save configuration without activating (if Draft supported for this event)
15. System validates rule configuration and saves as draft
16. Admin clicks "Test Rule" to send test notification to themselves
17. System generates test notification and delivers to admin's email/phone
18. Admin receives test notification and verifies content, formatting, and delivery
19. Admin clicks "Activate Rule" (or toggles status to Active)
20. System prompts: "This rule will activate immediately and apply to all matching events. Continue?"
21. Admin confirms activation
22. System activates rule and notifies S-03 Notification Service of new rule
23. System displays confirmation: "Notification rule activated successfully"
24. S-03 Notification Service begins monitoring for event triggers matching this rule

### Alternative Flows

**A1: Admin Edits Existing Notification Rule**:

- **Trigger**: Admin needs to modify delivery timing or add SMS channel to existing rule
- **Steps**:
  1. Admin navigates to Settings → Alerts & Notifications and filters by event type
  2. Admin clicks "Edit" on existing rule
  3. Admin modifies delivery timing from 3 days to 5 days before due date
  4. Admin enables SMS channel and selects SMS template
  5. Admin previews changes
  6. Admin saves changes (applies immediately to future events)
  7. System logs change with timestamp and admin user ID
- **Outcome**: Rule updated; future notifications use new configuration; in-flight notifications use old configuration

**A2: Admin Deactivates Notification Rule Temporarily**:

- **Trigger**: Admin wants to pause notifications during system maintenance or holiday period
- **Steps**:
  1. Admin navigates to Settings → Alerts & Notifications
  2. Admin toggles rule status from "Active" to "Paused"
  3. System prompts: "Paused rules will not trigger notifications. Reactivate when ready."
  4. Admin confirms pause
  5. System pauses rule and stops triggering notifications for this event
  6. Admin reactivates rule when ready by toggling status back to "Active"
- **Outcome**: Notifications paused temporarily; no notifications lost (system queues events and evaluates when rule reactivated if within retry window)

**A3: Admin Creates Multi-Language Notification Template**:

- **Trigger**: Admin needs to support multiple locales for the same event (initially English and Turkish per FR-021)
- **Steps**:
  1. Admin navigates to Settings → Alerts & Notifications and opens the Templates section
  2. Admin selects event type: "Quote Received"
  3. Admin selects language: English (default) from the **supported locales list** (managed in FR-021)
  4. Admin edits email template with subject, body, variables
  5. Admin clicks "Add Translation"
  6. System displays language dropdown populated from **FR-021 supported locales**
  7. Admin selects Turkish
  8. Admin edits Turkish version of template (subject, body, same variables)
  9. Admin saves template with both languages
  10. System validates both templates have matching variables
  11. S-03 Notification Service selects template language based on recipient's language preference and fallback rules (FR-021)
- **Outcome**: Template supports multiple languages; recipients receive notification in their preferred language

**B1: Notification Delivery Fails (Email Bounce)**:

- **Trigger**: Email delivery fails due to invalid email address or mailbox full
- **Steps**:
  1. S-03 Notification Service attempts email delivery via SMTP
  2. Email server returns bounce error (invalid address or mailbox full)
  3. System logs failed delivery with error code and timestamp
  4. System evaluates retry configuration for this notification type
  5. If retry enabled, system queues retry attempt for 1 hour later
  6. After retry attempts exhausted (max 3 retries), system marks notification as "Failed - Permanent"
  7. System flags patient account with "Email delivery issue" indicator
  8. Admin receives alert if event is critical (e.g., payment confirmation)
  9. Admin contacts patient via alternative channel (phone, in-app message) to update email address
- **Outcome**: Failed delivery logged; admin alerted for critical notifications; patient account flagged for follow-up

**B2: Template Variable Missing or Invalid**:

- **Trigger**: Admin creates template with variable that doesn't exist in event payload
- **Steps**:
  1. Admin creates notification template with variable `{{patient.procedure_date}}`
  2. Admin saves template
  3. System validates template against event payload schema
  4. System detects `patient.procedure_date` not available in event payload (should be `booking.procedure_date`)
  5. System displays error: "Variable `patient.procedure_date` not available for this event. Available variables: [list]"
  6. Admin corrects variable to `{{booking.procedure_date}}`
  7. System validates successfully and saves template
- **Outcome**: Template validation prevents runtime errors; admin corrects variable before activation

**B3: Duplicate Rules for Same Event (Not Possible in Catalog-Based UI)**:

- **Trigger**: Admin attempts to create a second rule for the same event type
- **Steps**:
  1. Admin navigates to `Settings → Alerts & Notifications`
  2. System displays one canonical configuration entry per backend event type (event catalog row)
  3. Admin selects the event (e.g., "Quote Submitted") and clicks "Configure"
  4. System opens the existing configuration for that event; there is no "create duplicate rule" action
- **Outcome**: Conflicting duplicate rules cannot exist because configuration is **one-per-event** in the admin UI

---

## Screen Specifications

### Screen 1: Alerts & Notifications (Rules Dashboard)

**Purpose**: Provides admin with overview of all configurable notification events (from the backend event catalog) and their configured rules, grouped by category, with quick access to edit, test, and pause/activate rules.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Event Category | select (dropdown) | No | Filter rules by category (All, Booking, Payment, Aftercare, Travel, Provider, Admin) | Predefined categories only |
| Rule Status | select (dropdown) | No | Filter by status (All, Active, Paused, Draft) | Predefined statuses only |
| Search Rules | text | No | Search by event name, template name, or recipient type | Max 100 characters |
| Rules List | table | Yes | Displays all rules matching filters | Sortable by event name, status, last modified; **each row is a “Rule Row” described by the fields below** |
| Rules List – Rule Row: Event Name | link | Yes | Event that triggers notification (e.g., "Quote Submitted", "Payment Received") | Sourced from backend event catalog; click opens this event’s Rule Editor |
| Rules List – Rule Row: Recipient Type | badge | Yes | Who receives notification (Patient, Provider, Admin, Multiple) | Display only |
| Rules List – Rule Row: Channels | icon set | Yes | Enabled channels (email icon, push icon; SMS icon shown only post‑MVP when SMS is enabled) | Display only |
| Rules List – Rule Row: Status | badge | Yes | Active (green), Paused (yellow), Draft (gray) | Display only |
| Rules List – Rule Row: Last Modified | datetime | Yes | Timestamp of last modification | Display in admin's local timezone |
| Rules List – Rule Row: Actions | button group | Yes | Configure, Test, Deactivate/Activate (and Delete if permitted) | Permission-based visibility |

**Business Rules**:

- Rules grouped by event category (Booking, Payment, Aftercare, etc.) for easier navigation
- Active rules displayed with green status badge; paused rules with yellow badge
- Critical event rules (payment confirmations, procedure reminders) cannot be deleted, only paused
- Deleting a rule requires confirmation prompt: "This will stop notifications for this event. Continue?"
- Testing a rule sends sample notification to admin's registered email/phone immediately
- Clicking a rule row (or the Event Name link / "Configure" action) opens **Screen 2: Alerts & Notifications (Rule Editor)** for that event
- Rule Editor MUST include a clear "Back to list" / breadcrumb link returning to the Rules Dashboard with the previous filters preserved

**Notes**:

- Table should support column sorting and filtering
- Pagination if more than 50 rules configured
- Export rules to CSV for audit/backup purposes

---

### Screen 2: Alerts & Notifications (Rule Editor)

**Purpose**: Allows admin to create or edit notification rules, configure recipient targeting, channel preferences, delivery timing, and template selection.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Rule Name | text | Yes | Internal name for rule (not shown to recipients) | Max 100 chars, unique per event |
| Event Type | select (dropdown) | Yes | System event that triggers notification | Predefined event list from backend; admin cannot create or rename event types here |
| Event Category | text (read-only) | Yes | Auto-populated based on event type | Display only |
| Recipient Type | multi-select | Yes | Who receives notification (Patient, Provider, Admin, Affiliate) | At least one recipient type required |
| Recipient Filter Rules | JSON editor | No | Advanced filtering (e.g., only patients in specific regions) | Valid JSON schema |
| Email Channel | toggle (on/off) | No | Enable email delivery | Default: on |
| Email Template | select (dropdown) | Conditional | Template to use for email (required if email enabled) | Must select template if channel enabled |
| Push Notification Channel | toggle (on/off) | No | Enable push notification delivery | Default: on for patients/providers |
| Push Template | select (dropdown) | Conditional | Template for push notification (required if push enabled) | Must select template if channel enabled |
| SMS Channel | toggle (on/off) | No | Enable SMS delivery (premium feature). **Hidden/disabled in MVP**; only shown when SMS delivery is enabled in S-03 in a post‑MVP phase | Default: off; admin approval required |
| SMS Template | select (dropdown) | Conditional | Template for SMS (required if SMS enabled in a future phase) | Must select template if channel enabled |
| Delivery Timing | select (dropdown) | Yes | When to send notification (Immediate, Scheduled, Delayed) | Predefined options |
| Schedule Time | datetime picker | Conditional | Specific time to send (required if Scheduled selected) | Future datetime only |
| Delay Duration | number + unit | Conditional | Delay before sending (required if Delayed selected; e.g., "3 days before event", "1 hour after event") | Min 1 hour, max 90 days |
| Delivery Timezone | select (dropdown) | Yes | Timezone for delivery (Recipient Local Time, UTC, Specific Timezone) | Default: Recipient Local Time |
| Retry Configuration | toggle (on/off) | No | Enable automatic retry for failed deliveries | Default: on |
| Max Retry Attempts | number | Conditional | Maximum retry attempts (required if retry enabled) | Min 1, max 5, default 3 |
| Retry Interval | number + unit | Conditional | Time between retries (e.g., "1 hour", "6 hours") | Min 1 hour, max 24 hours |
| Escalation Rules | toggle (on/off) | No | Enable escalation if condition not met | Default: off for non-critical events |
| Escalation Condition | textarea | Conditional | Condition for escalation (e.g., "Payment not received within 24 hours") | Max 500 chars |
| Escalation Recipients | multi-select | Conditional | Admin roles to notify on escalation | Required if escalation enabled |
| Rule Status | select (dropdown) | Yes | Active, Paused, Draft | Default: Draft for new rules |

**Business Rules**:

- **MVP**: At least one delivery channel (email or push) must be enabled (SMS is hidden/disabled)
- **Post‑MVP**: SMS may be enabled where available, but at least one channel must be enabled overall
- If event is time-sensitive (payment reminder, appointment reminder), admin must configure retry logic
- SMS channel requires admin approval and incurs additional cost per message
- Template selection filtered by channel type (only email templates shown for email channel)
- Delivery timezone "Recipient Local Time" automatically adjusts delivery time based on recipient's profile timezone
- Escalation rules only available for critical event types (payment, booking, medical concerns)
- Draft rules not executed by system until status changed to Active
- Paused rules can be reactivated without losing configuration

**Notes**:

- Preview pane on right side shows live template preview with sample data
- "Test Rule" button sends test notification to admin's contact info
- "Save Draft" allows saving without activating; "Save & Activate" activates immediately
- Change log displayed at bottom showing rule modification history
- Provide breadcrumb and a "Back to list" action to return to **Screen 1: Alerts & Notifications (Rules Dashboard)** without losing the admin’s filters/search context

---

### Screen 3: Alerts & Notifications (Template Editor)

**Purpose**: Allows admin to create and edit notification templates for email and push (and SMS post‑MVP) with support for dynamic variables, multi-language content, and rich formatting.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Template Name | text | Yes | Internal name for template | Max 100 chars, unique per event + channel |
| Event Type | select (dropdown) | Yes | Event this template applies to | Predefined event list |
| Channel Type | select (dropdown) | Yes | Delivery channel (Email, Push Notification; SMS post‑MVP only) | Fixed at creation (cannot change) |
| Language | select (dropdown) | Yes | Template language (locale) | Must be in supported locales list (FR-021); can create multiple language versions |
| Email Subject | text | Conditional | Email subject line (required for email channel) | Max 200 chars, supports variables |
| Email Body | rich text editor | Conditional | Email body content (required for email channel) | Max 10,000 chars, supports HTML/variables |
| Push Title | text | Conditional | Push notification title (required for push channel) | Max 100 chars, supports variables |
| Push Body | textarea | Conditional | Push notification body (required for push channel) | Max 500 chars, supports variables |
| SMS Body | textarea | Conditional | SMS message body (required for SMS channel) | Max 160 chars (1 SMS segment), supports variables |
| Available Variables | list (read-only) | Yes | Variables available for this event type (e.g., `{{patient.display_name}}`, `{{booking.date}}`) | Display only; click to insert |
| Variable Preview Values | JSON editor | No | Sample values for template preview | Valid JSON; used only for preview |
| Template Status | select (dropdown) | Yes | Active, Draft, Archived | Default: Draft |

**Business Rules**:

- Email templates support rich text formatting (bold, italic, links, images, buttons)
- Push notification templates support plain text only with limited formatting (bold, italic via markdown)
- SMS templates support plain text only; no formatting; 160 characters per SMS segment (platform warns if exceeds 1 segment)
- Variables must be enclosed in double curly braces: `{{variable.name}}`
- System validates all variables exist in event payload before allowing template activation (recipient-specific payload schemas apply; provider recipients pre-confirmation MUST NOT have access to unmasked patient PII fields per the platform masking rules)
- Templates can be versioned; changes create new version while preserving previous versions for audit
- Archived templates cannot be selected in notification rules but remain for historical records
- Multi-language templates must have matching variable usage across all language versions

**Notes**:

- Split-screen layout: editor on left, live preview on right
- Preview automatically updates as admin types
- "Insert Variable" dropdown inserts variable at cursor position
- "Send Test" button sends test notification to admin with preview values
- Template version history displayed at bottom with **“Revert by Creating New Version”** capability (no in-place rollback; reverting creates a new version from a selected prior version)

---

## Business Rules

### General Module Rules

- **Rule 1**: All notification rule changes logged in audit trail with admin user ID, timestamp, old configuration, and new configuration
- **Rule 2**: Critical event notifications (payment confirmations, procedure reminders, medical escalations) cannot be deleted, only paused temporarily
- **Rule 3**: Exactly **one** notification rule configuration exists per event type (one row per backend event in the catalog UI); duplicate rules for the same event type are not supported
- **Rule 4**: Notification templates must be activated before they can be selected in notification rules
- **Rule 5**: All timestamps in notifications displayed in recipient's local timezone (derived from profile settings)
- **Rule 6**: System enforces rate limiting per recipient to prevent notification spam: maximum 10 notifications per hour per recipient (critical notifications exempt)
- **Rule 7**: Notification delivery retries follow exponential backoff: 1st retry after 1 hour, 2nd retry after 3 hours, 3rd retry after 6 hours (configurable per rule)

### Data & Privacy Rules

- **Privacy Rule 1**: Notification delivery logs must not expose full recipient contact information (email/phone masked in admin interfaces)
- **Privacy Rule 2**: Notification content must not include sensitive medical information unless encrypted (email encryption via TLS, SMS not used for sensitive data)
- **Privacy Rule 3**: Notification templates stored with encryption at rest; only decrypted during delivery
- **Privacy Rule 4**: Recipients can opt out of non-critical notifications via profile preferences; system must respect opt-out for all non-critical notification types
- **Privacy Rule 5**: **Provider-facing notifications MUST follow the existing patient-identity masking rules used across the platform**: until treatment is confirmed via completed payment, patient identifiers remain masked/hidden (examples in FR-003 and FR-006). Provider templates MUST NOT be able to reference unmasked patient name/email/phone pre-confirmation; they may only use the same masked display fields used elsewhere (e.g., `patient.display_name` which renders masked pre-confirmation and unmasked post-confirmation).
- **Privacy Rule 6**: Notification logs retained for 90 days for operational purposes; then archived (immutable) for audit/compliance retention. **No hard deletes** of notification logs; when a user requests deletion, the system must **anonymize/redact personal identifiers** in archived logs per platform retention/compliance policy (see FR-023).
- **Audit Rule**: All notification rule modifications logged with admin user ID, timestamp, change summary, and reason (if provided)
- **GDPR**: Recipients can request export of all notifications sent to them; system provides notification history in machine-readable format (JSON/CSV)

### Admin Editability Rules

**Editable by Admin**:

- Event-to-notification mappings (which events trigger which notifications)
- Notification templates (subject, body, formatting, variables) for all channels
- Recipient targeting rules (who receives notifications based on role, relationship, event context)
- Channel preferences per event type (enable/disable email, push, SMS)
- Delivery timing configuration (immediate, scheduled, delayed)
- Retry logic parameters (max attempts, interval between retries)
- Escalation rules for time-sensitive notifications
- Notification delivery hours (e.g., no non-urgent notifications between 10 PM - 7 AM recipient local time)

**Fixed in Codebase (Not Editable)**:

- Core event definitions (system events that can trigger notifications - e.g., "Quote Received", "Payment Confirmed")
- Variable schema per event type (which variables available in notification templates per event)
- Maximum retry attempts (hard limit: 5 retries to prevent infinite loops)
- Rate limiting thresholds (max 10 notifications per hour per recipient)
- Encryption algorithms for notification content (AES-256 at rest, TLS 1.3 in transit)
- Delivery channel integrations (SMTP provider, push notification service, SMS gateway API)

**Non-Disableable by Default (Security-Critical)**:

- **Account/Auth notifications (OTP verification, password reset)** are security-critical and MUST be **non-disableable by default** in the admin UI (toggle locked; no pause).
- If the product explicitly allows a break-glass disable path, it MUST:
  - Require Super Admin permission (FR-031) + re-authentication
  - Show an imminent critical warning explaining impact (users cannot sign up/reset passwords)
  - Require multiple confirmation steps (e.g., typed event name + final confirm)
  - Require an audit reason and log it as a security event

**Event Catalog Source**:

- The list of available notification events is maintained by backend services (S-03 + core modules) as a central "event catalog".
- Admin UIs (e.g., `Settings → Alerts & Notifications`) can only **select from this catalog**; they cannot create arbitrary new event types.
- New event types are introduced via backend/product releases and then exposed to the admin as selectable items for configuration (rule on/off, channels, timing, templates).

**Configurable with Restrictions**:

- SMS channel availability: Admin can enable SMS for specific event types, but each SMS incurs cost; requires budget approval for high-volume events
- Notification testing: Admins can send test notifications to themselves or designated test accounts; cannot send to production recipients without rule activation
- Template versioning: Admins can create new template versions; system retains previous versions for audit; “revert” creates a **new** version copied from a selected prior version and requires admin confirmation

---

## Success Criteria

### Patient Experience Metrics

- **SC-001**: Patients receive quote received notifications within 5 minutes of provider submitting quote for 95% of quotes
- **SC-002**: Patients receive payment reminder notifications at configured time (e.g., 3 days before due) with 98%+ accuracy
- **SC-003**: Patients can view notification history in-app and access past notifications for 90 days
- **SC-004**: Patients who opt out of non-critical notifications successfully stop receiving those notifications (0 opt-out violations)

### Provider Efficiency Metrics

- **SC-005**: Providers receive new inquiry notifications within 5 minutes of patient submitting inquiry for 95% of inquiries
- **SC-006**: Providers receive payment confirmation notifications within 2 minutes of successful payment for 98% of payments
- **SC-007**: Providers can configure team notification routing to distribute notifications to appropriate staff members

### Admin Management Metrics

- **SC-008**: Admins can create and activate a notification rule for an event type (from the backend event catalog) in under 10 minutes
- **SC-009**: Admins can edit notification template and see changes applied to new notifications immediately (within 1 minute)
- **SC-010**: Admins can view notification delivery metrics in real-time dashboard with 5-minute data refresh
- **SC-011**: Admins receive alerts for critical notification delivery issues (e.g., email gateway down) within 5 minutes of issue detection

### System Performance Metrics

- **SC-012**: System evaluates notification rules and triggers delivery within 30 seconds of event occurrence for 95% of events
- **SC-013**: Email delivery initiated within 2 minutes of notification trigger for 95% of email notifications
- **SC-014**: Push notification delivery initiated within 1 minute of notification trigger for 95% of push notifications
- **SC-015**: System processes 1,000+ concurrent notification deliveries without performance degradation
- **SC-016**: Notification delivery success rate: 95%+ for email, 98%+ for push
- **SC-017**: Failed notification retries executed within configured intervals (e.g., 1 hour, 3 hours, 6 hours) with 98%+ punctuality

### Business Impact Metrics

- **SC-018**: Notification delivery rate improves booking conversion by providing timely reminders and updates (measure via A/B testing)
- **SC-019**: Payment reminder notifications reduce overdue installments by 40% compared to no-reminder baseline
- **SC-020**: Aftercare engagement increases by 30% due to timely milestone reminder notifications

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **FR-026 / Module A-09**: App Settings & Security Policies
  - **Why needed**: FR-030 extends OTP template management capabilities from FR-026 to encompass all notification types
  - **Integration point**: Uses centralized template storage and audit trail infrastructure from FR-026

- **FR-021 / Module A-09**: Multi‑Language & Localization (i18n)
  - **Why needed**: Notification templates and delivery must respect supported locales, user language preference, and fallback rules
  - **Integration point**: Template language dropdown and validation use FR-021 supported locales; S-03 selects template variant using recipient locale + fallback order defined in FR-021

- **FR-001 / Module P-01**: Auth & Profile Management (Patient)
  - **Why needed**: Requires patient profile data for notification personalization (name, email, phone, language preference, timezone)
  - **Integration point**: S-03 Notification Service queries P-01 APIs to retrieve recipient profile data before rendering templates

- **FR-009 / Module PR-01**: Auth & Team Management (Provider)
  - **Why needed**: Requires provider profile and team member data for notification routing
  - **Integration point**: S-03 queries PR-01 APIs to determine which provider team members receive notifications based on roles

- **FR-031 / Module A-09**: Admin Access Control & Permissions
  - **Why needed**: Notification configuration requires granular admin permissions (some admins configure rules, others only view analytics)
  - **Integration point**: FR-030 enforces permission checks via FR-031 permission matrix before allowing rule modifications

- **FR-003 / Module P-02**: Inquiry Submission & Distribution
  - **Why needed**: Inquiry events trigger notifications (inquiry submitted, quote received, quote expiring)
  - **Integration point**: P-02 publishes inquiry events to S-03 Notification Service for evaluation against notification rules

- **FR-007 / Module P-03**: Payment Processing
  - **Why needed**: Payment events trigger notifications (payment received, payment due, payment failed, installment reminder)
  - **Integration point**: P-03 publishes payment events to S-03 Notification Service for notification triggering

- **FR-011 / Module P-05**: Aftercare & Recovery Management
  - **Why needed**: Aftercare events trigger notifications (milestone due, scan reminder, questionnaire reminder, escalation alert)
  - **Integration point**: P-05 publishes aftercare events to S-03 Notification Service for notification triggering

### External Dependencies (APIs, Services)

- **External Service 1**: SMTP Email Service (e.g., SendGrid, Amazon SES, Mailgun)
  - **Purpose**: Delivers transactional email notifications to recipients
  - **Integration**: RESTful API or SMTP protocol for email delivery; webhook for delivery status updates (bounces, opens, clicks)
  - **Failure handling**: If SMTP service unavailable, queue emails for retry; alert admin if outage exceeds 15 minutes; fallback to secondary SMTP provider if configured

- **External Service 2**: Push Notification Service (e.g., Firebase Cloud Messaging for mobile, Web Push for web)
  - **Purpose**: Delivers push notifications to patient mobile apps and provider web browsers
  - **Integration**: RESTful API for push delivery; FCM for Android/iOS, Web Push API for browsers
  - **Failure handling**: If push service unavailable, queue notifications for retry; alert admin if outage exceeds 15 minutes; notifications expire after 24 hours (recipient sees notification history in-app instead)

- **External Service 3**: SMS Gateway (e.g., Twilio, Vonage, Africa's Talking) – **future**
  - **Purpose**: Delivers SMS notifications for critical events (optional, admin-enabled) once SMS is enabled in S-03 in a post‑MVP phase
  - **Integration**: RESTful API for SMS delivery; webhook for delivery status updates (planned)
  - **Failure handling**: If SMS gateway unavailable, queue SMS for retry (max 3 attempts); fallback to email/push notification if SMS fails; alert admin of SMS delivery issues. **This behaviour is future-facing; no SMS is sent in MVP.**

- **External Service 4**: Template Rendering Engine (e.g., Handlebars, Twig, Blade)
  - **Purpose**: Renders notification templates with dynamic variables before delivery
  - **Integration**: Server-side template engine embedded in S-03 Notification Service
  - **Failure handling**: If template rendering fails due to invalid template syntax, log error, alert admin, fallback to plain text notification template

### Data Dependencies

- **Entity 1**: User Profile Data (Patient, Provider, Admin)
  - **Why needed**: Required for notification personalization (name, email, phone, language preference, timezone)
  - **Source**: FR-001 (Patient Profile), FR-009 (Provider Profile), FR-031 (Admin Profile)

- **Entity 2**: Booking and Treatment Data
  - **Why needed**: Required for booking-related notifications (appointment date, clinic name, treatment type, costs)
  - **Source**: FR-006 (Booking & Scheduling), FR-010 (Treatment Execution)

- **Entity 3**: Payment Transaction Data
  - **Why needed**: Required for payment-related notifications (amount due, due date, payment status, installment schedule)
  - **Source**: FR-007 (Payment Processing), FR-007B (Split Payment / Installment Plans)

- **Entity 4**: Inquiry and Quote Data
  - **Why needed**: Required for inquiry/quote notifications (quote amount, provider name, quote expiry date)
  - **Source**: FR-003 (Inquiry Submission), FR-004 (Quote Submission)

---

## Assumptions

### User Behavior Assumptions

- **Assumption 1**: Patients and providers prefer email and push notifications over SMS for non-critical communications due to cost and intrusiveness
- **Assumption 2**: Patients check notifications within 6 hours of delivery for time-sensitive events (quotes, payments, appointments)
- **Assumption 3**: Admins will configure notification rules during initial platform setup and make incremental changes over time rather than frequent major reconfigurations
- **Assumption 4**: Recipients will update their contact information (email, phone) promptly if notifications fail to deliver
- **Assumption 5**: Providers will configure team notification routing to ensure critical notifications (new inquiries, patient arrivals) reach appropriate staff members

### Technology Assumptions

- **Assumption 1**: Email clients used by recipients support HTML emails with basic formatting (bold, italic, links, buttons)
- **Assumption 2**: Patient mobile devices support push notifications (iOS APNs, Android FCM)
- **Assumption 3**: Provider web browsers support Web Push API for browser-based push notifications
- **Assumption 4**: Email open tracking and link click tracking available via SMTP service pixel tracking (may not be 100% accurate due to email client privacy features)
- **Assumption 5**: SMS delivery available in all countries where Hairline operates (or graceful fallback to email/push if SMS unavailable in specific regions)
- **Assumption 6**: Notification delivery infrastructure can scale horizontally to handle peak loads (e.g., Black Friday promotion triggering 10,000 simultaneous notifications)

### Business Process Assumptions

- **Assumption 1**: Critical notifications (payment confirmations, appointment reminders, medical escalations) must be delivered with higher priority and stricter SLAs than non-critical notifications (marketing, general updates)
- **Assumption 2**: Notification templates will be updated infrequently (quarterly or less) once initial templates finalized
- **Assumption 3**: Multi-language notification support required for English and Turkish initially (per FR-021); additional languages added based on market expansion
- **Assumption 4**: Notification delivery metrics reviewed weekly by admin team to identify and resolve delivery issues
- **Assumption 5**: Admins will test notification rules in staging environment before activating in production to prevent erroneous notifications to real users

---

## Implementation Notes

### Technical Considerations

- **Architecture**: Event-driven architecture with pub-sub pattern; system modules publish events to message queue (e.g., RabbitMQ, AWS SQS); S-03 Notification Service subscribes to events and evaluates notification rules asynchronously
- **Technology**: Notification templates rendered server-side using template engine (Handlebars, Twig, Blade) to prevent XSS vulnerabilities from user-generated content in variables
- **Performance**: Notification rule evaluation must be optimized for low latency (<30 seconds from event to delivery initiation); use in-memory caching (Redis) for frequently accessed notification rules and templates
- **Storage**: Notification delivery logs stored in separate database or log aggregation service (e.g., Elasticsearch) to prevent performance impact on primary application database
- **Scalability**: S-03 Notification Service must support horizontal scaling; use distributed job queue (e.g., Sidekiq, Bull) for notification delivery jobs to distribute load across multiple worker instances

### Integration Points

- **Integration 1**: System modules (P-02, P-03, P-05, etc.) publish events to message queue via standard event publishing API
  - **Data format**: JSON event payload with event type, entity IDs (patient ID, booking ID, etc.), timestamp, and event-specific data
  - **Authentication**: Internal service-to-service authentication via JWT or API key
  - **Error handling**: If message queue unavailable, retry publishing event with exponential backoff; alert admin if queue outage exceeds 5 minutes

- **Integration 2**: S-03 Notification Service queries profile APIs (P-01, PR-01, FR-031) to retrieve recipient data for template rendering
  - **Data format**: RESTful JSON API returning recipient profile (name, email, phone, language, timezone)
  - **Authentication**: Service-to-service API calls authenticated via internal JWT tokens
  - **Error handling**: If profile API unavailable, fallback to basic notification template without personalization; retry profile fetch before next notification delivery attempt

- **Integration 3**: S-03 Notification Service integrates with external SMTP, push, and SMS services via RESTful APIs
  - **Data format**: JSON payloads conforming to external service API specifications
  - **Authentication**: API keys stored in secure vault (AWS Secrets Manager, HashiCorp Vault)
  - **Error handling**: If external service returns 5xx error, retry with exponential backoff (max 3 retries); if all retries fail, mark notification as failed and alert admin

### Scalability Considerations

- **Current scale**: Expected 500 notifications per day at launch (inquiries, quotes, bookings across 100 patients and 10 providers)
- **Growth projection**: Plan for 10,000 notifications per day within 12 months (2,000 patients, 50 providers, multiple notifications per booking lifecycle)
- **Peak load**: Handle 1,000 simultaneous notifications during promotional campaigns or system-wide reminders (e.g., Black Friday sale, daylight saving time change triggering rescheduled notifications)
- **Data volume**: Expect 100 MB of notification logs per month (retained for 90 days = 300 MB operational). Archived retention duration follows platform audit/compliance policy (see FR-023); size scales linearly with retention.
- **Scaling strategy**:
  - Horizontal scaling of S-03 Notification Service workers (Kubernetes pod autoscaling based on queue depth)
  - Distributed message queue (RabbitMQ cluster or AWS SQS) to handle high event throughput
  - In-memory caching (Redis cluster) for notification rules and templates to reduce database load
  - CDN for email template assets (images, logos) to reduce server load and improve email rendering performance

### Security Considerations

- **Authentication**: Admin access to notification configuration requires authentication via FR-031 admin authentication system; admins cannot impersonate recipients for notification testing
- **Authorization**: Granular permission checks enforced via FR-031 permission matrix; some admins can configure rules, others only view analytics
- **PII Redaction (Provider Pre-Confirmation)**: When the recipient is a provider and treatment is not yet confirmed via completed payment, S-03 MUST apply the same patient-identity masking rules used elsewhere in the platform (e.g., FR-003/FR-006) and MUST NOT include unmasked patient identifiers (full name, email, phone) in the provider recipient payload.
- **Encryption**: Notification templates stored encrypted at rest (AES-256); decrypted only during template rendering in S-03 Notification Service
- **Audit trail**: All notification rule modifications logged with admin user ID, timestamp, change summary, IP address; logs retained for 10 years for compliance
- **Threat mitigation**:
  - Rate limiting on notification delivery to prevent abuse (max 10 notifications per hour per recipient)
  - Template validation to prevent XSS attacks (variables HTML-escaped during rendering)
  - SMTP authentication and SPF/DKIM/DMARC configured to prevent email spoofing
  - Webhook signature verification for delivery status updates to prevent spoofed bounce notifications
- **Compliance**:
  - GDPR: Recipients can opt out of non-critical notifications; system respects opt-out preferences
  - CAN-SPAM: Email notifications include unsubscribe link for marketing emails (transactional emails exempt)
  - TCPA (US): SMS notifications only sent with explicit recipient consent; opt-out via "STOP" keyword supported

---

## User Scenarios & Testing

### User Story 1 - Admin Configures Payment Reminder Notifications (Priority: P1)

Admin needs to configure automated payment reminder notifications to reduce overdue installments. Patient should receive email and push notifications 3 days before installment due date. (SMS is post‑MVP only.)

**Why this priority**: Payment reminders are critical for cash flow and reducing payment defaults. This is the highest-value notification type for the business.

**Independent Test**: Can be fully tested by creating notification rule, triggering test payment due event, verifying admin receives test notification with correct timing, content, and delivery channels.

**Acceptance Scenarios**:

1. **Given** admin is logged into Admin Platform → Settings → Alerts & Notifications, **When** admin selects the "Payment Due Reminder" event from the event catalog and clicks "Configure", **Then** system displays the event configuration form with event-specific configuration options
2. **Given** admin configures rule with email and push channels enabled, delivery timing "3 days before due date at 9:00 AM recipient local time", retry enabled (max 3 attempts), **When** admin clicks "Save Draft", **Then** system validates rule configuration and saves as draft status
3. **Given** admin clicks "Test Rule", **When** system generates test notification with sample payment data (patient name "Test Patient", amount due "$200", due date "2025-11-16"), **Then** admin receives test email and push notification within 2 minutes with correct personalized content
4. **Given** admin reviews test notification and verifies content correct, **When** admin clicks "Activate Rule", **Then** system prompts for confirmation, activates rule upon confirmation, and displays success message "Notification rule activated successfully"
5. **Given** notification rule active, **When** patient has installment payment due in 3 days (due date 2025-11-16, current date 2025-11-13), **Then** system triggers notification at 9:00 AM patient local time on 2025-11-13 and delivers email and push notification to patient
6. **Given** email delivery fails due to invalid email address, **When** system detects bounce error, **Then** system logs failed delivery, queues retry attempt for 1 hour later, and alerts admin if retry also fails

---

### User Story 2 - Admin Creates Multi-Language Notification Template (Priority: P1)

Admin needs to create email notification template for "Quote Received" event in both English and Turkish to support patients in UK and Turkey. Template must include patient name, quote amount, provider name, and expiry date with consistent formatting across languages.

**Why this priority**: Multi-language support is critical for international patient base. Quote received notification is high-volume and directly impacts conversion rates.

**Independent Test**: Can be fully tested by creating template in both languages, sending test notifications in each language, verifying correct language selection based on recipient language preference.

**Acceptance Scenarios**:

1. **Given** admin navigates to Admin Platform → Settings → Alerts & Notifications, **When** admin clicks "Create New Template" and selects event type "Quote Received", channel "Email", language "English", **Then** system displays email template editor with available variables for Quote Received event
2. **Given** admin edits template with subject "Your Hair Transplant Quote from {{provider.name}}", body "Hello {{patient.first_name}}, You've received a quote for {{quote.treatment_type}} from {{provider.name}}. Quote Amount: {{quote.total_amount}} {{quote.currency}}. Quote expires on {{quote.expiry_date}}. View your quote in the app.", **When** admin clicks "Save Draft", **Then** system validates template variables against event payload schema and saves template as draft
3. **Given** admin clicks "Add Translation", **When** admin selects language "Turkish" and edits Turkish template with translated subject and body (same variables), **Then** system validates both templates have matching variables and saves Turkish version
4. **Given** admin clicks "Activate Template", **When** system validates both language versions active, **Then** system activates template and displays success message
5. **Given** notification rule configured with "Quote Received" event and template activated, **When** patient with language preference "Turkish" receives quote from provider, **Then** S-03 Notification Service renders Turkish template and sends Turkish-language email to patient
6. **Given** patient with language preference "English" receives quote, **When** S-03 evaluates notification rule, **Then** system renders English template and sends English-language email

---

### User Story 3 - Admin Monitors Notification Delivery and Troubleshoots Failures (Priority: P2)

Admin needs to monitor notification delivery performance to identify and resolve delivery issues. Admin should see real-time delivery rates, failure reasons, and drill down into specific failed notifications for troubleshooting.

**Why this priority**: Monitoring and troubleshooting capabilities are essential for maintaining high delivery rates and quickly resolving issues before they impact large numbers of users.

**Independent Test**: Can be fully tested by triggering mix of successful and failed notification deliveries (via test rules), verifying admin can view metrics in dashboard, filter by failure reason, and retry failed deliveries.

**Acceptance Scenarios**:

1. **Given** admin navigates to Admin Platform → Settings → Alerts & Notifications, **When** admin views delivery/log information for an event or runs a test notification, **Then** system displays delivery status and failure reasons (where applicable) and allows export to CSV for troubleshooting
2. **Given** dashboard shows 950 emails sent, 900 delivered (94.7%), 50 failed (5.3%), **When** admin clicks on "Failed Deliveries" metric, **Then** system displays detailed list of 50 failed notifications with recipient (masked), event type, channel, failure reason, timestamp
3. **Given** failed notifications list shows 30 failures with reason "Invalid email address", 15 with reason "Mailbox full", 5 with reason "SMTP timeout", **When** admin filters by failure reason "Invalid email address", **Then** system displays 30 failed notifications with invalid email addresses
4. **Given** admin identifies pattern (all failures for email domain "@oldprovideremail.com"), **When** admin contacts affected patients to update email addresses, **Then** patients update their profiles with new email addresses
5. **Given** patient updates email address from invalid to valid, **When** admin clicks "Retry" on failed notification in dashboard, **Then** system re-triggers notification delivery to updated email address and marks as successfully delivered if delivery succeeds
6. **Given** admin marks resolved failures as "Resolved", **When** admin refreshes dashboard, **Then** resolved failures removed from active failures list but retained in notification logs for audit trail

---

### Edge Cases

- What happens when **admin creates notification rule with delivery timing "3 days before event" but event occurs in less than 3 days**?
  - System evaluates notification rule when event created; if delivery timing already passed, system triggers notification immediately with note "Delivery timing adjusted due to short notice" in admin logs
  - Alternatively, admin can configure rule to skip notification if timing not feasible (e.g., don't send "3 days before" reminder if event is tomorrow)

- How does system handle **template variable missing in event payload at runtime** (e.g., template uses `{{patient.phone}}` but phone number not provided in patient profile)?
  - System renders template with placeholder text for missing variable (e.g., "[Phone number not provided]") or omits section containing missing variable if template designed with conditional logic
  - System logs warning in admin notification logs: "Variable `patient.phone` not available for notification [notification_id]; rendered with placeholder"
  - Admin receives alert if missing variable affects critical notification (e.g., appointment reminder missing appointment time)

- What occurs if **recipient has multiple email addresses or phone numbers in profile** (e.g., primary and secondary)?
  - System prioritizes primary contact info (primary email, primary phone); delivers to primary only
  - If delivery to primary fails, system can optionally retry with secondary contact info (configurable per notification rule via "Retry with secondary contact" toggle)
  - Admin can configure notification rule to send to both primary and secondary simultaneously for critical events (e.g., payment confirmation sent to both primary and secondary email)

- How to manage **notification delivery during recipient timezone changes** (e.g., daylight saving time transitions)?
  - System automatically adjusts delivery timing based on recipient's current timezone setting at time of delivery
  - If recipient travels to different timezone and updates profile, future notifications use new timezone
  - Scheduled notifications (e.g., "9:00 AM recipient local time") calculated dynamically at delivery time, not statically when notification scheduled

- What happens when **admin deactivates notification rule while notifications queued for delivery**?
  - System immediately stops adding new notifications to queue for deactivated rule
  - Notifications already queued (not yet delivered) remain in queue and delivered as scheduled
  - If admin wants to cancel queued notifications, admin must explicitly "Purge Queue" (with confirmation prompt: "This will cancel X pending notifications. Continue?")

- How does system handle **conflicting notification preferences** (e.g., admin rule requires email delivery but recipient opted out of emails)?
  - System respects recipient opt-out for non-critical notifications (marketing, general updates) and does not deliver
  - For critical notifications (payment confirmations, appointment reminders), system overrides opt-out and delivers via at least one channel (displays banner in-app explaining why critical notification delivered despite opt-out)
  - Admin can designate notification types as "Critical - Cannot Opt Out" in rule configuration

- What occurs if **external notification service (SMTP, push, SMS) experiences prolonged outage** (e.g., 24 hours)?
  - System queues notifications for retry with exponential backoff (up to 24-hour window)
  - If service restored within 24 hours, queued notifications delivered (may result in burst of deliveries)
  - If outage exceeds 24 hours, system marks notifications as "Failed - Service Outage" and alerts admin
  - Admin can manually re-trigger notifications after service restored or switch to backup notification provider if configured

---

## Functional Requirements Summary

### Core Requirements

- **REQ-030-001**: System MUST allow admins to create notification rules by selecting event type, configuring recipient targeting, enabling delivery channels (email, push, and SMS in future phases), selecting templates per channel, and defining delivery timing. In MVP, only email and push can actually be enabled; SMS is reserved for later phases once S‑03 SMS support is implemented.
- **REQ-030-002**: System MUST evaluate notification rules in real-time (<30 seconds) when system events occur and trigger notifications for all matching rules
- **REQ-030-003**: System MUST deliver email notifications via SMTP service within 2 minutes of trigger for 95% of emails
- **REQ-030-004**: System MUST deliver push notifications via FCM/Web Push within 1 minute of trigger for 95% of push notifications
- **REQ-030-005**: System MUST support optional SMS notifications for critical events (payment reminders, appointment alerts) with admin approval and cost tracking in post‑MVP phases; **MVP does not send SMS**.
- **REQ-030-006**: System MUST provide notification template editor supporting rich text (email), plain text (push, SMS), dynamic variables, and multi-language content. SMS templates, if configured, are only used when SMS delivery is enabled in a later phase.
- **REQ-030-007**: System MUST validate notification templates before activation to ensure all variables exist in event payload and template syntax is valid
- **REQ-030-008**: System MUST automatically retry failed notification deliveries according to configured retry logic (max 3-5 attempts with exponential backoff)
- **REQ-030-009**: System MUST log all notification deliveries (successful and failed) with recipient (masked), event, channel, timestamp, delivery status, and failure reason (if applicable)
- **REQ-030-010**: System MUST provide real-time notification delivery analytics dashboard with metrics: total sent, delivered, failed, opened (email), clicked (email), grouped by event type, channel, recipient type

### Data Requirements

- **REQ-030-011**: System MUST store notification rules with: event type, recipient targeting rules, channel preferences, template IDs, delivery timing, retry configuration, escalation rules, rule status (active/paused/draft)
- **REQ-030-012**: System MUST store notification templates with: template name, event type, channel type, language, content (subject, body), variables, status (active/draft/archived), version history
- **REQ-030-013**: System MUST maintain notification delivery logs for 90 days in operational database; archive logs for audit/compliance retention (no hard delete). If a user requests deletion, the system MUST anonymize/redact personal identifiers in those logs per platform retention/compliance policy (see FR-023).
- **REQ-030-014**: System MUST track notification engagement metrics (email opens, email clicks) via pixel tracking and link tracking from SMTP service

### Security & Privacy Requirements

- **REQ-030-015**: System MUST encrypt notification templates at rest using AES-256; decrypt only during template rendering in S-03 Notification Service
- **REQ-030-016**: System MUST mask recipient contact information (email, phone) in admin interfaces to protect privacy (e.g., "mar***@example.com", "+44***1234")
- **REQ-030-017**: System MUST enforce rate limiting to prevent notification spam: maximum 10 notifications per hour per recipient (critical notifications exempt from rate limiting)
- **REQ-030-018**: System MUST HTML-escape all template variables during rendering to prevent XSS attacks from user-generated content
- **REQ-030-019**: System MUST respect recipient opt-out preferences for non-critical notifications (marketing, general updates); critical notifications (payment, appointment) override opt-out with in-app explanation
- **REQ-030-020**: System MUST log all notification rule modifications with admin user ID, timestamp, change summary, IP address; logs retained for 10 years for audit compliance

### Integration Requirements

- **REQ-030-021**: System MUST integrate with SMTP service (SendGrid, Amazon SES, Mailgun) for email delivery via RESTful API or SMTP protocol
- **REQ-030-022**: System MUST integrate with push notification services (Firebase Cloud Messaging for mobile, Web Push API for web) for push notification delivery
- **REQ-030-023**: System MUST integrate with SMS gateway (Twilio, Vonage) for SMS delivery via RESTful API (optional, admin-enabled)
- **REQ-030-024**: System MUST receive delivery status updates (bounces, opens, clicks) from external services via webhooks with signature verification to prevent spoofing
- **REQ-030-025**: System MUST publish notification events to audit log service (Elasticsearch, CloudWatch Logs) for compliance and troubleshooting

---

## Key Entities

- **Entity 1 - Notification Rule**: Represents configuration for triggering notifications based on system events
  - **Key attributes**: rule_id (unique), rule_name, event_type, event_category, recipient_targeting_rules (JSON), channel_preferences (email/push/SMS enabled), email_template_id, push_template_id, sms_template_id, delivery_timing (immediate/scheduled/delayed), delivery_timezone, retry_enabled, max_retry_attempts, retry_interval, escalation_enabled, escalation_conditions (JSON), escalation_recipients (admin role IDs), rule_status (active/paused/draft), created_by (admin_user_id), created_at, updated_at, activated_at
  - **Relationships**: One notification rule maps to one event type; one rule references one template per enabled channel; one rule can trigger many notification deliveries; many rules can be created by one admin user

- **Entity 2 - Notification Template**: Represents reusable content template for notifications
  - **Key attributes**: template_id (unique), template_name, event_type, channel_type (email/push/SMS), language (en-US/tr-TR/etc.), content (JSON: subject, body, formatting), variables (array of variable names used in template), status (active/draft/archived), version_number, previous_version_id (for versioning), created_by (admin_user_id), created_at, updated_at, activated_at
  - **Relationships**: One template maps to one event type and one channel type; one template can have multiple language versions (sibling templates); one template can be referenced by many notification rules; many templates can be created by one admin user

- **Entity 3 - Notification Delivery Log**: Represents record of individual notification delivery attempt
  - **Key attributes**: delivery_id (unique), rule_id, template_id, recipient_type (patient/provider/admin), recipient_id (user_id), recipient_contact (email/phone - masked in admin interface), event_type, event_id (e.g., booking_id, payment_id), channel_type (email/push/SMS), delivery_status (sent/delivered/opened/clicked/failed), failure_reason (if failed), retry_count, delivered_at, opened_at (email only), clicked_at (email only), notification_content_snapshot (rendered template for audit), created_at
  - **Relationships**: One delivery log maps to one notification rule and one template; one delivery log maps to one recipient (user); many delivery logs can be created for one event (if multiple notification rules apply); one recipient can have many delivery logs

- **Entity 4 - Notification Engagement Metrics**: Aggregated metrics for notification delivery performance
  - **Key attributes**: metric_id (unique), date_period (daily/weekly/monthly), event_type, channel_type, recipient_type, total_sent, total_delivered, total_failed, total_opened (email only), total_clicked (email only), delivery_rate (percentage), open_rate (percentage, email only), click_rate (percentage, email only), avg_delivery_time_seconds, failure_reasons_breakdown (JSON: count per failure reason), created_at
  - **Relationships**: Metrics aggregated from many notification delivery logs; one metric record per date period + event type + channel type + recipient type combination

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-13 | 1.0 | Initial PRD creation for FR-030: Notification Rules & Configuration | AI Agent (Claude) |
| 2025-12-22 | 1.1 | Verified per template; aligned retention to no hard-delete (FR-023); clarified provider pre-confirmation masking; locked security-critical auth events; cleaned tenant placeholder labels | AI Assistant |
| 2026-02-05 | 1.2 | Cancel Inquiry flow (FR-003 Workflow 5): Updated `inquiry.cancelled` event notes; added `quote.cancelled_inquiry` event with mandatory provider receipt (admin cannot disable); cancellation reason is patient-private | AI     |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | TBD | 2025-12-22 | ✅ Verified & Approved |
| Technical Lead | TBD | 2025-12-22 | ✅ Verified & Approved |
| Stakeholder | TBD | 2025-12-22 | ✅ Verified & Approved |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-011 Aftercare & Recovery Management PRD
**Last Updated**: 2025-12-22
