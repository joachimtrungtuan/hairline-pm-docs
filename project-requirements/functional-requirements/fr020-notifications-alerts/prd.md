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

- Patient Platform (P-01/P-03 overlay): Receive push/email notifications; manage global Email/Push toggles (MVP) and view notification history.
- Provider Platform (PR-02/PR-05 overlay): Receive notifications for inquiries, quotes, bookings, payments, and messages; manage notification preferences (can choose which notification types to receive); view notifications via dropdown.
- Admin Platform (A-09): Receive notifications for major system events (provider onboarding, payment issues, escalations, system alerts); configure default notification policies, SMS enablement, throttling thresholds, and view delivery dashboards; view notifications via dropdown.
- Shared Services (S-03): Unified Notification Service orchestrating channels (email, push, and SMS in future phases) with templates, throttling, and delivery tracking. SMS delivery is not implemented in MVP and is treated as a future enhancement.

### Scope Boundaries

In Scope:

- Notification types:
  - **Patient notifications**: quote received, quote updated, quote expired, booking confirmed, payment received, payment reminder, message received, appointment reminder, treatment started (when provider marks patient as arrived), treatment completed (with post-op instructions), aftercare milestone, aftercare task due (3D scan, questionnaire), aftercare task overdue, cancellation (booking/treatment), standalone aftercare activation, standalone aftercare payment confirmation.
  - **Provider notifications**: inquiry received, quote accepted, quote expired (when quote expires without acceptance), booking confirmed, payment received, payout received (when admin processes provider payout with invoice), promotion/discount available (new platform discount requiring provider approval), message received, treatment start reminder (upcoming appointments), task in progress reminder (for treatments not completed), treatment completion confirmation (when treatment documentation is successfully saved), aftercare escalation, cancellation (inquiry/booking), payment reminder (for pending payments).
  - **Admin notifications**: provider onboarding requests, payment failures, system escalations, critical aftercare cases, provider document expiration warnings, high-priority support tickets, system alerts, treatment completion (for billing/payout processing), payout failures.
- Channels: email, push; SMS is an optional/configurable channel for urgent events in the target architecture but is **not available in MVP** (no SMS notifications are sent until a later phase explicitly enables this capability).
- User preferences (MVP):
  - **Patients**: global Email/Push toggles (managed in FR-001: Patient Authentication & Profile Management, Settings → Notifications section); per‑category preferences deferred to V2 (not in scope).
  - **Providers**: can choose which notification types to receive (quote notifications, schedule notifications, treatment start notifications, aftercare notifications, review notifications, promotion/discount notifications) via notification preferences settings (managed in PR-06: Profile & Settings Management, Settings → Notifications section).
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

#### Screen 1: Patient – Notification Settings (MVP)

Purpose: Let patients toggle global Email/Push preferences.

**Note**: This screen is managed by FR-001: Patient Authentication & Profile Management (Settings → Notifications section).

Data Fields:

| Field Name        | Type   | Required | Description                 | Validation Rules       |
|-------------------|--------|----------|-----------------------------|------------------------|
| Email notifications | switch | Yes    | Enable/disable all emails   | Persist per user       |
| Push notifications  | switch | Yes    | Enable/disable all pushes   | Persist per device/app |

Business Rules:

- Category-level settings are not present in MVP (documented as future).

Notes:

- Explain urgent SMS usage where enabled by policy.
- Screen location: Patient App → Settings → Notifications (FR-001).

---

#### Screen 2: Patient – Notification Listing

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

Notes:

- Screen location: Patient App → Notifications (dedicated tab or menu item).
- Notifications persist for 90 days; older notifications archived.

---

### Provider Platform Screens

#### Screen 3: Provider – Notification Dropdown

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

Notes:

- Located in provider dashboard header (bell icon).
- Real-time updates via WebSocket or polling.
- Dropdown expands to show full list with infinite scroll (no separate listing screen).
- Maximum height with scrollable content area.

---

#### Screen 4: Provider – Notification Settings

Purpose: Let providers choose which notification types to receive.

**Note**: This screen is managed by PR-06: Profile & Settings Management (Settings → Notifications section). **Note**: PR-06 does not have a dedicated FR document yet; this screen specification is part of the provider platform settings functionality.

Data Fields:

| Field Name        | Type   | Required | Description                 | Validation Rules       |
|-------------------|--------|----------|-----------------------------|------------------------|
| Quote notifications | switch | Yes    | Enable/disable quote-related notifications (inquiry received, quote accepted, quote expired) | Persist per provider |
| Schedule notifications | switch | Yes    | Enable/disable booking-related notifications (booking confirmed, treatment start reminders) | Persist per provider |
| Treatment start notifications | switch | Yes    | Enable/disable treatment start reminders | Persist per provider |
| Aftercare notifications | switch | Yes    | Enable/disable aftercare escalation notifications | Persist per provider |
| Review notifications | switch | Yes    | Enable/disable review-related notifications | Persist per provider |
| Promotion/Discount notifications | switch | Yes    | Enable/disable promotion/discount notifications (new platform discounts requiring approval) | Persist per provider |
| Email notifications | switch | Yes    | Enable/disable all email notifications | Persist per provider |
| Push notifications  | switch | Yes    | Enable/disable all push notifications | Persist per provider |

Business Rules:

- Individual notification type toggles control which event types trigger notifications.
- Global Email/Push toggles control delivery channels (if Email is off, no emails sent regardless of individual toggles).
- Changes are saved immediately and take effect within 1 minute.
- Default values: Quote notifications = ON, Schedule notifications = ON, Treatment start notifications = ON, Aftercare notifications = OFF, Review notifications = OFF, Promotion/Discount notifications = ON.

Notes:

- Screen location: Provider Platform → Settings → Notifications (PR-06).
- Providers can disable specific notification types while keeping others enabled.
- Critical notifications (e.g., payment received) may not be disableable per admin policy.

---

### Admin Platform Screens

#### Screen 5: Admin – Notification Dropdown

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
- Filter options within dropdown: All, Unread, Critical, By Type (Payment, Escalation, System Alert, etc.).
- Search functionality: search by notification content within dropdown.

Notes:

- Located in admin dashboard header (bell icon).
- Real-time updates via WebSocket or polling.
- Dropdown expands to show full list with infinite scroll (no separate listing screen).
- Maximum height with scrollable content area.
- Critical notifications (payment failures, escalations) always shown at top regardless of timestamp.

---

#### Screen 6: Admin – Notification Policy & Monitoring

Purpose: Configure defaults and monitor delivery.

**Note**: This screen is part of FR-030: Notification Rules & Configuration. Template management is handled in FR-030 (Notification Template Editor) and FR-026 (App Settings & Security Policies for OTP templates).

Data Fields:

| Field Name       | Type  | Required | Description                                   | Validation Rules           |
|------------------|-------|----------|-----------------------------------------------|----------------------------|
| SMS enabled      | switch| No       | Toggle SMS for urgent categories               | Admin role required        |
| Throttle limits  | form  | Yes      | Per type/channel rate limits                   | Safe bounds enforced       |
| Templates        | list  | Yes      | Link to template management (FR-030)           | Navigate to FR-030 editor  |
| Delivery dashboard| panel| Yes      | Success/failure counts, last 24h, by type      | N/A                        |

Business Rules:

- Changes to throttling and SMS take effect immediately and are audited.
- Template management redirects to FR-030: Notification Rules & Configuration for full template editor.

Notes:

- Email template management: See FR-030 (Notification Rules & Configuration) for comprehensive template editor with dynamic variables, multi-language support, and preview capabilities.
- OTP email templates: Managed separately in FR-026 (App Settings & Security Policies) for verification and password reset emails.

---

## Success Criteria

- SC-001: 95% of eligible events generate a notification within 2 seconds.
- SC-002: 99% of notifications respect user global Email/Push preferences.
- SC-003: Throttling reduces duplicate notifications by ≥ 90% during spikes.
- SC-004: Delivery status recorded for 100% of attempts.
- SC-005: Notification Settings loads in ≤ 1 second (p95).

---

## Business Rules

- **Patient Preferences**: Global Email/Push toggles available to patients in MVP (managed in FR-001: Patient Authentication & Profile Management, Settings → Notifications); category preferences deferred to V2.
- **Provider Preferences**: Providers can choose which notification types to receive (quote notifications, schedule notifications, treatment start notifications, aftercare notifications, review notifications, promotion/discount notifications) via notification preferences settings (managed in PR-06: Profile & Settings Management, Settings → Notifications section). **Note**: PR-06 does not have a dedicated FR document yet.
- **Admin Notifications**: Admins receive notifications for major system events (provider onboarding, payment failures, escalations, critical aftercare cases, system alerts).
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

- Supported channels (Email/Push; SMS behind config), baseline event types per FR-020.

Configurable with Restrictions:

- Maximum SMS volume, high‑priority categories allowed for SMS.

---

## Dependencies

- **FR-001**: Patient Authentication & Profile Management (patient notification preferences UI in Settings → Notifications).
- **FR-012**: Messaging (message received events).
- **FR-026**: App Settings & Security Policies (OTP email templates for verification and password reset).
- **FR-030**: Notification Rules & Configuration (notification template management, template editor, notification rule configuration).
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
  - Provider preferences: Managed in PR-06 (Profile & Settings Management) under Settings → Notifications section (providers can toggle individual notification types on/off: quote notifications, schedule notifications, treatment start notifications, aftercare notifications, review notifications, promotion/discount notifications). **Note**: PR-06 does not have a dedicated FR document yet; provider notification preferences are part of the provider platform settings functionality.

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

- FR-001: System MUST send email for key events per templates.
- FR-002: System MUST send push notifications to mobile app.
- FR-003: System MUST support optional/configurable SMS for urgent events.
- FR-004: System MUST allow patients to configure notification preferences (MVP: global Email/Push toggles managed in FR-001: Patient Authentication & Profile Management).
- FR-004B: System MUST allow providers to configure notification preferences (choose which notification types to receive: quote, schedule, treatment start, aftercare, review, promotion/discount notifications).
- FR-005: System MUST support notification types listed in Scope (including payment reminders, task in progress reminders, aftercare standalone flow notifications, cancellations, and admin notifications for major events).
- FR-006: System MUST throttle notifications to prevent spam and log suppression.
- FR-007: System MUST track and expose delivery status per attempt.
- FR-008: System MUST provide notification listing screen for patients to view notification history (paginated, 20 per page).
- FR-009: System MUST provide notification dropdown in provider dashboard header with infinite scroll (loads 20 notifications per batch, no separate listing screen).
- FR-010: System MUST provide notification dropdown in admin dashboard header with infinite scroll (loads 20 notifications per batch, no separate listing screen).
- FR-011: System MUST send notifications to admins for major system events (provider onboarding, payment failures, escalations, critical aftercare cases, system alerts).

---

## Key Entities

- **NotificationEvent**: type, subject, recipient, payload metadata, createdAt.
- **NotificationAttempt**: channel, provider, status, timestamp, error, correlationId.
- **PatientPreference**: userId, emailEnabled, pushEnabled, updatedAt (MVP scope; managed in FR-001).
- **ProviderPreference**: providerId, quoteNotification, scheduleNotification, startTreatmentNotification, afterCareNotification, reviewNotification, updatedAt (allows providers to choose which notification types to receive).
- **NotificationRecord**: notificationId, recipientId, recipientType (patient/provider/admin), type, title, message, readStatus, createdAt, readAt (for notification listing screens).

---

## Appendix: Change Log

| Date       | Version | Changes                                       | Author |
|------------|---------|-----------------------------------------------|--------|
| 2025-11-11 | 1.0     | Initial PRD creation (MVP scope)             | AI     |
| 2025-11-16 | 1.1     | Added admin notifications, additional notification types (payment reminder, task in progress, aftercare standalone, cancellation), notification listing screens (patient, provider dropdown, admin dropdown), clarified notification preference management (FR-001 for patients, provider preferences), clarified notification content and email template management (FR-030, FR-026) | AI     |

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
**Last Updated**: 2025-11-11
