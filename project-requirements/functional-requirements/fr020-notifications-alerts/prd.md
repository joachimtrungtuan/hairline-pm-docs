# Product Requirements Document: Notifications & Alerts

**Module**: S-03: Notification Service
**Feature Branch**: `fr020-notifications-alerts`
**Created**: 2025-11-11
**Status**: ✅ Verified & Approved
**Source**: FR-020 from local-docs/project-requirements/system-prd.md; Transcriptions (patient/admin/provider references)

---

## Executive Summary

Provide reliable, configurable notifications (email, push, optional SMS in future phases) for key lifecycle events across patients and providers. Deliver timely alerts, respect user preferences, prevent spam via throttling, and track delivery for operational visibility. MVP supports global Email/Push toggles on the patient app; fine‑grained category preferences follow in V2, and any SMS delivery is explicitly deferred beyond MVP.

---

## Module Scope

### Multi-Tenant Architecture

- Patient Platform (FR-001: Patient Authentication & Profile Management): Receive push/email notifications; manage global Email/Push toggles (MVP) and view notification history (listing specified in FR-020).
- Provider Platform (FR-032: Provider Dashboard Settings & Profile Management / PR-06): Receive notifications for inquiries, quotes, bookings, payments, and messages; manage notification preferences; view notifications via dropdown.
- Admin Platform (FR-030: Notification Rules & Configuration + FR-020 dropdown): Receive notifications for configurable events per FR-030 event catalog; configure default notification policies, SMS enablement, throttling thresholds, and view delivery dashboards; view notifications via dropdown.
- Affiliate Program (if enabled): Receive affiliate payout notifications; configuration is managed via FR-030 event catalog and rules.
- Shared Services (S-03): Unified Notification Service orchestrating channels (email, push, and SMS in future phases) with templates, throttling, and delivery tracking. SMS delivery is not implemented in MVP and is treated as a future enhancement.

### Scope Boundaries

In Scope:

- Notification event types (MVP):
  - **Source of truth**: `FR-030: Notification Rules & Configuration` (Admin-Configurable Notification Event Catalog).
  - The table below mirrors FR-030 for completeness; **if any mismatch exists, FR-030 prevails**.

| Category | Event (Display Name) | Example Backend Event Key | Primary Recipients | Notes |
|----------|-----------------------|---------------------------|--------------------|-------|
| Account/Auth | Email Verification / OTP Code | `account.email_verification_code` | Patient, Provider, Admin | Extends FR-026 OTP templates; **security-critical** and non-disableable by default |
| Account/Auth | Password Reset Code / Link | `account.password_reset` | Patient, Provider, Admin | **Security-critical** and non-disableable by default |
| Account/Auth | New Account Created (Welcome / Onboarding) | `account.created` | Patient, Provider | Optional; can be disabled if not needed |
| Inquiry | Inquiry Submitted (Provider notified) | `inquiry.submitted` | Provider | “New inquiry matching clinic/location” |
| Inquiry | Inquiry Cancelled | `inquiry.cancelled` | Provider, Patient (optional), Admin (optional) | Cancellation of inquiry prior to booking where applicable |
| Quote | Quote Submitted / Ready (Patient notified) | `quote.submitted` | Patient | Starts quote expiry timer (see below) |
| Quote | Quote Updated / Revised | `quote.updated` | Patient, Provider | Notify on meaningful changes (price/package/dates) |
| Quote | Quote Expiring Soon | `quote.expiring_soon` | Patient, Provider | Default expiry window is policy-bound (e.g., 48h) |
| Quote | Quote Expired | `quote.expired` | Patient, Provider | Sent on expiry processing completion |
| Quote | Quote Accepted | `quote.accepted` | Provider, Patient, Admin (optional) | Provider receives acceptance details |
| Quote | Quote Declined | `quote.declined` | Provider, Patient (optional) | Useful for provider follow-up / analytics |
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
| Messaging/Support | Support Ticket Updated / Reply Added | `support.ticket_updated` | Patient, Admin | Support center communications |
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

- Channels: email, push; SMS is an optional/configurable channel for urgent events in the target architecture but is **not available in MVP** (no SMS notifications are sent until a later phase explicitly enables this capability).
- User preferences (MVP):
  - **Patients**: global Email/Push toggles (managed in FR-001: Patient Authentication & Profile Management, Settings → Notifications section); per‑category preferences deferred to V2 (not in scope).
  - **Providers**: can choose which notification types to receive (quote notifications, schedule notifications, treatment start notifications, aftercare notifications, promotion/discount notifications) via notification preferences settings (managed in PR-06: Profile & Settings Management, Settings → Notifications section).
- Notification listing screens: patient notification history screen (full listing page), provider notification dropdown (infinite scroll), admin notification dropdown (infinite scroll).
- Throttling/de‑duplication and delivery tracking.

Out of Scope:

- In‑app messaging content design (covered in FR-012).
- Per‑category user preferences on patient app (explicitly V2).

### Entry Points

- System events published by core modules (inquiry, quote, booking, payment, chat, scheduling, aftercare) trigger notifications via S-03.
- Users access Settings → Notifications to set global Email/Push toggles (MVP).

---

## Business Workflows

### Main Flow: Event → Notification Dispatch

Actors: System, Notification Service, Recipient
Trigger: Business event occurs (e.g., booking confirmed)
Outcome: Recipient receives notification according to channel preferences

Steps:

1. Event emitted with payload (type, actor, subject, recipient id).
2. Notification Service evaluates preferences and throttling.
3. Builds message from template and routes to enabled channels.
4. Records delivery attempt and status; exposes audit.
5. (If SMS enabled and urgent) include SMS path; else email/push only.

### Alternative Flows

- A1: Preference Disabled
  - Trigger: Recipient has disabled Email or Push.
  - Outcome: Channel suppressed; delivery attempted on remaining enabled channels.

- B1: Throttling
  - Trigger: Excessive events in short time window.
  - Outcome: Coalesce or defer per policy; record suppression in audit.

- B2: Channel Failure
  - Trigger: Email/push/SMS provider unavailable.
  - Outcome: Retry with backoff; failover when configured; status reflects failure cause.

---

## Screen Specifications

### Patient Platform Screens

Notification settings UI for patients is defined in `FR-001: Patient Authentication & Profile Management` (Settings → Notifications). FR-020 relies on that screen; it is not re-specified here to avoid duplication.

#### Screen 1: Patient – Notification Listing

Purpose: Display notification history for patients to view all received notifications.

Data Fields:

| Field Name        | Type   | Required | Description                 | Validation Rules       |
|-------------------|--------|----------|-----------------------------|------------------------|
| Notification List | list   | Yes      | Chronological list of notifications | Paginated, 20 per page |
| Notification Type | badge  | Yes      | Type indicator (quote, booking, payment, etc.) | Read-only |
| Title             | text   | Yes      | Notification title/subject  | Read-only |
| Message           | text   | Yes      | Notification body content   | Read-only, truncated with "Read more" |
| Timestamp         | datetime | Yes    | When notification was sent  | Read-only, relative time |
| Read Status       | badge  | Yes      | Read/Unread indicator       | Toggle on click |
| Action Button     | button | No       | Deep link to related content | Context-dependent |

Business Rules:

- Notifications sorted by most recent first (newest at top).
- Unread notifications highlighted with visual indicator.
- Clicking notification marks as read and navigates to related content (if applicable).
- Filter options: All, Unread, By Type (Quote, Booking, Payment, Aftercare, etc.).
- Search functionality: search by notification content.

---

### Provider Platform Screens

#### Screen 2: Provider – Notification Dropdown

Purpose: Display notifications in provider dashboard header dropdown with infinite scroll.

Data Fields:

| Field Name        | Type   | Required | Description                 | Validation Rules       |
|-------------------|--------|----------|-----------------------------|------------------------|
| Notification Count | badge | Yes      | Unread notification count   | Real-time update |
| Notification Items | list   | Yes      | Infinite scroll list of notifications | Load more on scroll |
| Notification Type | badge  | Yes      | Type indicator              | Read-only |
| Title             | text   | Yes      | Notification title          | Read-only, truncated |
| Message           | text   | No       | Notification body content   | Read-only, truncated |
| Timestamp         | datetime | Yes    | When notification was sent  | Read-only, relative time |
| Read Status       | indicator | Yes    | Read/Unread dot             | Visual indicator |
| Load More Trigger | scroll | Yes      | Infinite scroll trigger     | Loads next batch on scroll |

Business Rules:

- Dropdown shows notifications with infinite scroll (loads 20 notifications per batch).
- Notifications sorted by most recent first (newest at top).
- Unread count badge updates in real-time.
- Clicking notification marks as read and navigates to related content.
- Infinite scroll loads more notifications as user scrolls down.
- Filter options within dropdown: All, Unread, By Type (Quote, Booking, Payment, etc.).
- Search functionality: search by notification content within dropdown.

---

Provider notification settings UI is defined in `FR-032: Provider Dashboard Settings & Profile Management (PR-06)` under Settings → Notifications. FR-020 consumes those preferences; the screen itself is not re-specified here.

---

### Admin Platform Screens

#### Screen 3: Admin – Notification Dropdown

Purpose: Display notifications in admin dashboard header dropdown with infinite scroll.

Data Fields:

| Field Name        | Type   | Required | Description                 | Validation Rules       |
|-------------------|--------|----------|-----------------------------|------------------------|
| Notification Count | badge | Yes      | Unread notification count   | Real-time update |
| Notification Items | list   | Yes      | Infinite scroll list of notifications | Load more on scroll |
| Notification Type | badge  | Yes      | Type indicator (critical, warning, info) | Read-only, color-coded |
| Title             | text   | Yes      | Notification title          | Read-only, truncated |
| Message           | text   | No       | Notification body content   | Read-only, truncated |
| Timestamp         | datetime | Yes    | When notification was sent  | Read-only, relative time |
| Read Status       | indicator | Yes    | Read/Unread dot             | Visual indicator |
| Priority Indicator | badge | No       | Critical/High priority badge | For urgent items |
| Load More Trigger | scroll | Yes      | Infinite scroll trigger     | Loads next batch on scroll |

Business Rules:

- Dropdown shows notifications with infinite scroll (loads 20 notifications per batch).
- Notifications sorted by most recent first (newest at top).
- Critical notifications highlighted with red badge and always shown at top (before non-critical).
- Unread count badge updates in real-time.
- Clicking notification marks as read and navigates to related content.
- Infinite scroll loads more notifications as user scrolls down.
- Filter options within dropdown: All, Unread, Critical, By Type (Payment, Aftercare, Booking, Support, etc.).
- Search functionality: search by notification content within dropdown.

---

Notification policy, throttling, and delivery monitoring UI live in `FR-030: Notification Rules & Configuration` (including template editor; OTP templates in `FR-026`). FR-020 depends on those capabilities and does not re-specify the admin screen.

---

### Consolidated Screen Notes

- Patient – Notification Listing: Patient App → Notifications (dedicated tab or menu item); notifications persist for 90 days then archive.
- Provider – Notification Dropdown: Provider dashboard header bell icon; real-time updates (WebSocket or polling); infinite scroll within dropdown at max height.
- Admin – Notification Dropdown: Admin dashboard header bell icon; real-time updates (WebSocket or polling); infinite scroll within dropdown at max height; critical items pinned above non-critical.
- Patient notification settings: Owned by `FR-001: Patient Authentication & Profile Management` (Settings → Notifications).
- Provider notification settings: Owned by `FR-032: Provider Dashboard Settings & Profile Management (PR-06)` (Settings → Notifications).
- Admin policy/config screens: Owned by `FR-030: Notification Rules & Configuration` (template editor) and `FR-026: App Settings & Security Policies` (OTP templates).

## Success Criteria

- SC-001: 95% of eligible events generate a notification without violating platform performance NFRs (API p95 < 500ms, p99 < 1000ms), and users typically see notifications within ~2 seconds under normal load.
- SC-002: 99% of notifications respect user global Email/Push preferences.
- SC-003: Throttling reduces duplicate notifications by ≥ 90% during spikes.
- SC-004: Delivery status recorded for 100% of attempts.
- SC-005: Notification Settings loads in ≤ 1 second (p95).

---

## Business Rules

- **Patient Preferences**: Global Email/Push toggles available to patients in MVP (managed in FR-001: Patient Authentication & Profile Management, Settings → Notifications); category preferences deferred to V2.
- **Provider Preferences**: Providers can choose which notification types to receive (quote notifications, schedule notifications, treatment start notifications, aftercare notifications, promotion/discount notifications) via notification preferences settings (managed in FR-032: Provider Dashboard Settings & Profile Management, Settings → Notifications section).
- **Admin Notifications**: Admin recipients and event coverage are defined by the FR-030 event catalog and configured rules (no additional hard-coded admin event list in FR-020).
- One notification record per attempt with channel, provider, status, and timestamp.
- Throttling and suppression policies are transparent in audit logs.
- **Notification Content Management**: Notification content (titles, messages, templates) is managed in FR-030: Notification Rules & Configuration via the Notification Template Editor.
- **Email Template Management**:
  - General notification email templates: Managed in FR-030 (Notification Rules & Configuration) with support for dynamic variables, multi-language content, rich text formatting, and preview capabilities.
  - OTP email templates (verification, password reset): Managed in FR-026 (App Settings & Security Policies) as part of authentication settings.

### Admin Editability

Editable by Admin:

- Throttling thresholds, SMS enablement, default channel policies, templates.

Fixed in Codebase (Not Editable):

- Supported channels (Email/Push; SMS behind config), baseline event types per FR-030 event catalog.

Configurable with Restrictions:

- Maximum SMS volume, high‑priority categories allowed for SMS.

---

## Dependencies

- **FR-001**: Patient Authentication & Profile Management (patient notification preferences UI in Settings → Notifications).
- **FR-012**: Messaging (message received events).
- **FR-026**: App Settings & Security Policies (OTP email templates for verification and password reset).
- **FR-030**: Notification Rules & Configuration (notification template management, template editor, notification rule configuration).
- **FR-032**: Provider Dashboard Settings & Profile Management (PR-06; provider notification preferences UI).
- P-02/P-03/P-05 events for inquiry/quote/booking/aftercare milestones.
- S-03 Notification Service; Email/Push/SMS providers via configured adapters.

---

## Assumptions

- Users understand global Email/Push toggles; granular controls to be introduced later.
- SMS costs are controlled via caps; only urgent categories use SMS.

---

## Implementation Notes

- Event-driven design; idempotent handlers; retries with backoff.
- Delivery provider abstraction; per-channel template library.
- Privacy: no sensitive content in notifications; deep links use secure tokens.
- **Notification Content Management**: Notification templates (email, push, SMS) are managed in FR-030: Notification Rules & Configuration via the Notification Template Editor, which supports dynamic variables, multi-language content, rich text formatting (email), and preview capabilities.
- **Email Template Management**:
  - General notification email templates: Managed in FR-030 (Notification Rules & Configuration) - admins can create/edit templates per event type and channel with variable substitution, multi-language support, and preview.
  - OTP email templates: Managed separately in FR-026 (App Settings & Security Policies) for email verification and password reset flows.
- **Notification Preferences**:
  - Patient preferences: Managed in FR-001 (Patient Authentication & Profile Management) under Settings → Notifications screen.
  - Provider preferences: Managed in FR-032 (Provider Dashboard Settings & Profile Management) under Settings → Notifications section (providers can toggle individual notification types on/off: quote notifications, schedule notifications, treatment start notifications, aftercare notifications, promotion/discount notifications).

---

## User Scenarios & Testing

### User Story 1 – Patient toggles preferences (P1)

Why: Respect user choice on communication channels.

Independent Test: Disable Email and verify only Push is delivered for eligible events.

Acceptance Scenarios:

1. Given Email is disabled, when an event fires, then no email is sent and push is delivered (if enabled).
2. Given both Email and Push disabled, when an event fires, then no notification is sent and suppression is logged.

### User Story 2 – Admin enables SMS for urgent events (P2)

Why: Ensure urgent communication reaches users reliably.

Independent Test: Mark “appointment reminder” as SMS‑eligible; verify SMS sent under policy.

Acceptance Scenarios:

1. Given SMS is enabled for urgent reminders, when a reminder event fires, then an SMS is sent and logged.
2. Given SMS volume cap reached, when more SMS would be sent, then they are suppressed and recorded.

### User Story 3 – Spike throttling (P2)

Why: Avoid spamming users during bursts.

Independent Test: Simulate high‑frequency message events; ensure de‑duplication.

Acceptance Scenarios:

1. Given many identical events in a short window, when throttling applies, then only coalesced notifications are sent.
2. Given throttling suppressed some events, when admin reviews logs, then suppression entries are visible.

---

## Functional Requirements Summary

- REQ-020-001: System MUST send email for key events per templates.
- REQ-020-002: System MUST send push notifications to mobile app.
- REQ-020-003: System MUST support optional/configurable SMS for urgent events.
- REQ-020-004: System MUST allow patients to configure notification preferences (MVP: global Email/Push toggles managed in FR-001: Patient Authentication & Profile Management).
- REQ-020-004B: System MUST allow providers to configure notification preferences (choose which notification types to receive: quote, schedule, treatment start, aftercare, promotion/discount notifications).
- REQ-020-005: System MUST support notification event types in the FR-030 MVP event catalog (Admin-Configurable Notification Event Types), routed to enabled channels and templates.
- REQ-020-006: System MUST throttle notifications to prevent spam and log suppression.
- REQ-020-007: System MUST track and expose delivery status per attempt.
- REQ-020-008: System MUST provide notification listing screen for patients to view notification history (paginated, 20 per page).
- REQ-020-009: System MUST provide notification dropdown in provider dashboard header with infinite scroll (loads 20 notifications per batch, no separate listing screen).
- REQ-020-010: System MUST provide notification dropdown in admin dashboard header with infinite scroll (loads 20 notifications per batch, no separate listing screen).
- REQ-020-011: System MUST send notifications to admins for any enabled FR-030 event types where Admin is a primary or optional recipient (per rule configuration).

---

## Key Entities

- **NotificationEvent**: type, subject, recipient, payload metadata, createdAt.
- **NotificationAttempt**: channel, provider, status, timestamp, error, correlationId.
- **PatientPreference**: userId, emailEnabled, pushEnabled, updatedAt (MVP scope; managed in FR-001).
- **ProviderPreference**: providerId, quoteNotification, scheduleNotification, startTreatmentNotification, afterCareNotification, promotionDiscountNotification, updatedAt (allows providers to choose which notification types to receive).
- **NotificationRecord**: notificationId, recipientId, recipientType (patient/provider/admin), type, title, message, readStatus, createdAt, readAt (for notification listing screens).

---

## Appendix: Change Log

| Date       | Version | Changes                                       | Author |
|------------|---------|-----------------------------------------------|--------|
| 2025-11-11 | 1.0     | Initial PRD creation (MVP scope)             | AI     |
| 2025-11-16 | 1.1     | Added admin notifications, additional notification types (payment reminder, task in progress, aftercare standalone, cancellation), notification listing screens (patient, provider dropdown, admin dropdown), clarified notification preference management (FR-001 for patients, provider preferences), clarified notification content and email template management (FR-030, FR-026) | AI     |
| 2025-12-05 | 1.2     | Removed duplicate screen specs (patient settings, provider settings, admin policy) now referenced to their owning FRs (FR-001, PR-06, FR-030/FR-026) | AI     |
| 2025-12-05 | 1.3     | Renumbered screens, consolidated screen notes, and referenced exact FRs (FR-001, FR-032/PR-06, FR-030, FR-026) | AI     |
| 2026-01-16 | 1.4     | Aligned FR-020 notification event types to match FR-030 MVP event catalog; designated FR-030 as source of truth for event coverage | AI     |

---

## Appendix: Approvals

| Role           | Name | Date | Signature/Approval |
|----------------|------|------|--------------------|
| Product Owner  |      |      |                    |
| Technical Lead |      |      |                    |
| Stakeholder    |      |      |                    |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Last Updated**: 2026-01-16
