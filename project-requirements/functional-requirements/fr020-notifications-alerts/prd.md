# Product Requirements Document: Notifications & Alerts

**Module**: S-03: Notification Service
**Feature Branch**: `fr020-notifications-alerts`
**Created**: 2025-11-11
**Status**: Draft
**Source**: FR-020 from local-docs/project-requirements/system-prd.md; Transcriptions (patient/admin/provider references)

---

## Executive Summary

Provide reliable, configurable notifications (email, push, optional SMS) for key lifecycle events across patients and providers. Deliver timely alerts, respect user preferences, prevent spam via throttling, and track delivery for operational visibility. MVP supports global Email/Push toggles on the patient app; fine‑grained category preferences follow in V2.

---

## Module Scope

### Multi-Tenant Architecture

- Patient Platform (P-01/P-03 overlay): Receive push/email notifications; manage global Email/Push toggles (MVP) and view notification history.
- Provider Platform (PR-02/PR-05 overlay): Receive notifications for inquiries, quotes, bookings, payments, and messages; basic preference controls.
- Admin Platform (A-09): Configure default notification policies, SMS enablement, throttling thresholds, and view delivery dashboards.
- Shared Services (S-03): Unified Notification Service orchestrating channels (email, push, SMS) with templates, throttling, and delivery tracking.

### Scope Boundaries

In Scope:

- Notification types: inquiry received, quote submitted, booking confirmed, payment received, message received, appointment reminder, aftercare milestone.
- Channels: email, push; SMS optional/configurable for urgent events.
- User preferences (MVP): global Email/Push toggles; per‑category preferences deferred to V2 (not in scope).
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

### Screen 1: Patient – Notification Settings (MVP)

Purpose: Let patients toggle global Email/Push preferences.

Data Fields:

| Field Name        | Type   | Required | Description                 | Validation Rules       |
|-------------------|--------|----------|-----------------------------|------------------------|
| Email notifications | switch | Yes    | Enable/disable all emails   | Persist per user       |
| Push notifications  | switch | Yes    | Enable/disable all pushes   | Persist per device/app |

Business Rules:

- Category-level settings are not present in MVP (documented as future).

Notes:

- Explain urgent SMS usage where enabled by policy.

---

### Screen 2: Admin – Notification Policy & Monitoring

Purpose: Configure defaults and monitor delivery.

Data Fields:

| Field Name       | Type  | Required | Description                                   | Validation Rules           |
|------------------|-------|----------|-----------------------------------------------|----------------------------|
| SMS enabled      | switch| No       | Toggle SMS for urgent categories               | Admin role required        |
| Throttle limits  | form  | Yes      | Per type/channel rate limits                   | Safe bounds enforced       |
| Templates        | list  | Yes      | Manage message templates per type/channel      | Preview required before save|
| Delivery dashboard| panel| Yes      | Success/failure counts, last 24h, by type      | N/A                        |

Business Rules:

- Changes to throttling and SMS take effect immediately and are audited.

---

## Success Criteria

- SC-001: 95% of eligible events generate a notification within 2 seconds.
- SC-002: 99% of notifications respect user global Email/Push preferences.
- SC-003: Throttling reduces duplicate notifications by ≥ 90% during spikes.
- SC-004: Delivery status recorded for 100% of attempts.
- SC-005: Notification Settings loads in ≤ 1 second (p95).

---

## Business Rules

- Global Email/Push toggles available to patients in MVP; category preferences deferred to V2.
- One notification record per attempt with channel, provider, status, and timestamp.
- Throttling and suppression policies are transparent in audit logs.

### Admin Editability

Editable by Admin:

- Throttling thresholds, SMS enablement, default channel policies, templates.

Fixed in Codebase (Not Editable):

- Supported channels (Email/Push; SMS behind config), baseline event types per FR-020.

Configurable with Restrictions:

- Maximum SMS volume, high‑priority categories allowed for SMS.

---

## Dependencies

- FR-012 Messaging (message received events).
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
- FR-004: System MUST allow patients/providers to configure notification preferences (MVP: global Email/Push toggles for patient app).
- FR-005: System MUST support notification types listed in Scope.
- FR-006: System MUST throttle notifications to prevent spam and log suppression.
- FR-007: System MUST track and expose delivery status per attempt.

---

## Key Entities

- NotificationEvent: type, subject, recipient, payload metadata, createdAt.
- NotificationAttempt: channel, provider, status, timestamp, error, correlationId.
- Preference: userId, emailEnabled, pushEnabled, updatedAt (MVP scope).

---

## Appendix: Change Log

| Date       | Version | Changes                                       | Author |
|------------|---------|-----------------------------------------------|--------|
| 2025-11-11 | 1.0     | Initial PRD creation (MVP scope)             | AI     |

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
