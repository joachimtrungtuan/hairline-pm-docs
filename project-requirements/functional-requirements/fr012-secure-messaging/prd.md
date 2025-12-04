# Product Requirements Document: Messaging & Communication

**Module**: P-06: Communication | A-10: Communication Monitoring & Support
**Feature Branch**: `fr012-secure-messaging`
**Created**: 2025-11-11
**Status**: Draft
**Source**: FR-012 from local-docs/project-requirements/system-prd.md; Transcriptions (HairlineApp-Part1/Part2, Hairline-AdminPlatform-Part1/Part2)

---

## Executive Summary

Enable secure, auditable, real-time messaging across the Hairline platform to support patient care and operational coordination. Patients can communicate with Hairline Support (general help) and Aftercare Specialists (post‑procedure guidance). Admins monitor conversations, triage and escalate as needed, and maintain a complete compliance log. The module supports text and media messages, read receipts, conversation history, and real-time notifications, improving response times, patient reassurance, and operational transparency while meeting medical data privacy obligations.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-06)**: In-app chat with Hairline Support and Aftercare Specialists; notifications for new messages; view conversation history; send text and media.
- **Provider Platform (PR-06)**: Provider ↔ Admin operational messaging (e.g., billing, scheduling clarifications); read-only visibility of patient conversations only when explicitly shared via admin for case review.
- **Admin Platform (A-10)**: Communication center for monitoring, triage, keyword flagging, escalation, and compliance logging; can initiate outreach to patients or providers; can request 3D scans or schedule reviews.
- **Shared Services (S-03, S-05)**: Notification Service for push/email alerts; Media Storage Service for secure handling of images/videos attached to messages.

### Multi-Tenant Breakdown

**Patient Platform (P-06)**:

- Compose and send messages to Hairline Support or assigned Aftercare Specialist team.
- Attach media (images/videos) to messages; view thumbnails and playback inline.
- View conversation list and full history; see read receipts and timestamps.
- Receive real-time notifications for new messages; badge counts for unread.

**Provider Platform (PR-06)**:

- Send and receive messages with Admin for operational topics (e.g., billing, scheduling).
- View admin-shared patient conversation excerpts as part of a case review (no direct patient DM in V1).
- Receive notifications for new admin messages and escalation requests.

**Admin Platform (A-10)**:

- Unified inbox: filter by channel, status, flags, keywords.
- Monitor patient ↔ Support and patient ↔ Aftercare conversations with audit trail.
- Initiate messages to patients (e.g., escalation follow-ups) and to providers (operational queries).
- Trigger actions: request 3D scan, schedule a review, mark urgent, assign owner.
- Configure moderation rules and keyword flags; export conversation logs for disputes.

**Shared Services (S-03, S-05)**:

- S-03 Notification Service to deliver timely user alerts (push/email as configured).
- S-05 Media Storage for secure storage and retrieval of attachments; virus/malware scanning pipeline.

### Communication Structure

**In Scope**:

- Patient ↔ Hairline Support in-app messaging (text, images, video).
- Patient ↔ Aftercare Specialists in-app messaging (post‑procedure care).
- Provider ↔ Admin messaging for operational topics.
- Real-time notifications, read receipts, conversation history, and compliance logging.
- Admin monitoring, keyword flagging, and escalation workflow.

**Out of Scope**:

- Direct Patient ↔ Provider messaging (may be considered in a future release).
- Live video calls (can be scheduled/triggered from Admin but delivered by separate module).
- SMS channel management (handled by S-03 Notification Service configuration; **SMS as a transport for secure messaging is not part of MVP and will only be available if/when S-03 adds SMS support in a later phase**).

### Entry Points

Patients access chat from Support and Aftercare sections in the mobile app. Aftercare chat becomes available upon procedure completion or aftercare enrollment. Providers access Admin chat from their dashboard’s communications panel. Admins access the Communication Center from the Admin platform navigation. Notifications, keyword flags, and escalations can also deep‑link into specific conversations.

---

## Business Workflows

### Main Flow: Patient ↔ Support Messaging

**Actors**: Patient, Support Agent, Admin (oversight), System
**Trigger**: Patient opens Support and sends a new message
**Outcome**: Support receives and responds; patient sees timely reply; conversation logged

**Steps**:

1. Patient composes a text message and optionally attaches media; taps Send.
2. System validates content (size/type), records the message, and updates conversation state.
3. System delivers real-time notification to Support and updates unread counters.
4. Support opens the conversation, reads the message; system records read receipt.
5. Support replies; patient receives notification and sees the new message in real time.
6. System logs all events (sent, delivered, read) to audit trail; conversation remains searchable.

### Alternative Flows

**A1: Attachment Flow**:

- **Trigger**: Patient includes image/video attachment
- **Steps**:
  1. System validates allowed file types and size.
  2. System stores media securely and links it to the message.
- **Outcome**: Attachment appears in the thread with preview; recipients can view/playback.

**A2: Escalation Flow**:

- **Trigger**: Support flags a message as urgent (e.g., reported complications)
- **Steps**:
  1. System elevates priority, assigns to Aftercare Specialist or medical lead.
  2. Admin optionally triggers a 3D scan request or schedules a review.
- **Outcome**: Patient receives guidance quickly; escalation is logged with timestamps and assignee.

**B1: Invalid Content**:

- **Trigger**: Attachment exceeds limits or unsupported type
- **Steps**:
  1. System blocks upload and explains allowed types/limits.
  2. Patient can retry with valid content.
- **Outcome**: Valid content sent; conversation integrity maintained.

**B2: Intermittent Connectivity**:

- **Trigger**: Network lost during send
- **Steps**:
  1. System queues the message locally and indicates pending state.
  2. On reconnect, system retries; if failure persists, prompts user to resend.
- **Outcome**: Message eventually sent or user notified to retry; no silent loss.

---

## Screen Specifications

### Screen 1: Patient Chat

**Purpose**: Allow patients to message Hairline Support and Aftercare Specialists, share media, and receive timely responses.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Message text | text | Yes | Core message body | Max 2000 chars, no prohibited terms |
| Attachment | image/video | No | Optional media to support the message | Max 50MB per file; types: jpg, png, mp4 |
| Recipient channel | select | Yes | Support or Aftercare | Default: last used channel |
| Send button | action | Yes | Submits message | Disabled until text or attachment present |
| Read status | indicator | N/A | Shows if message was read | Auto-updated in real time |

**Business Rules**:

- Show typing/sending states and error states; retry control available for failed sends.
- Submit disabled until message text or attachment is provided.
- Display timestamps and read receipts per message.
- Patient sees only their own conversations; no exposure of provider identities.

**Notes**:

- Provide clear attachment guidance (allowed types/sizes).
- Indicate escalation status when a conversation is marked urgent.
- Limit attachment count per message to prevent overload (e.g., up to 5).

---

### Screen 2: Admin Communication Center

**Purpose**: Monitor, triage, and act on conversations across channels with auditability.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Search | text | No | Find conversations by user, keyword, status | Min 2 chars |
| Filters | multi-select | No | Channel, priority, status, assignee, flags | Applied instantly |
| Conversation list | list | Yes | View threads with badges and previews | Sorted by latest activity |
| Message thread | panel | Yes | Read/write view with attachments | Read receipts visible |
| Actions | buttons | No | Escalate, assign, request 3D scan, schedule review | Confirmations required |

**Business Rules**:

- Escalations require an assignee and reason.
- Exported logs include timestamps, participants, and message content identifiers.

**Notes**:

- Show compliance flags inline; allow mark-as-resolved with reason.

---

### Screen 3: Provider ↔ Admin Chat

**Purpose**: Allow providers to coordinate with Admin for operational matters without exposing patient PII unnecessarily.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Message text | text | Yes | Provider/admin message body | Max 2000 chars |
| Attachment | file | No | Supporting documents (e.g., invoice) | Types: pdf, jpg, png; Max 20MB |
| Subject | text | No | Optional topic label | Max 120 chars |

**Business Rules**:

- Patient PII hidden unless case explicitly shared by Admin for review.
- Messages logged and searchable by Admin only.

**Notes**:

- Provider sees only their threads and admin responses.

---

## Business Rules

### General Module Rules

- All conversations and message events (sent, delivered, read, escalated) are logged with timestamps and participants.
- Message content size and attachment limits enforced to ensure reliable delivery and storage.
- All timestamps displayed in the user’s local timezone; admin views can toggle UTC for audits.

### Data & Privacy Rules

  Reference Principle II from constitution: Medical Data Privacy & Security

- Provider identities are not exposed to patients in messaging unless business rules elsewhere allow it; patients interact with Hairline Support and Aftercare teams.
- Patient PII and media are protected; all data encrypted in transit and at rest per policy.
- Medical communications retained for minimum 7 years; deletion requests result in archival with access restrictions.
- All access to conversations is auditable with user, timestamp, and reason when required.
- Compliance with GDPR and HIPAA-equivalent practices; patient consent respected for data sharing.

### Admin Editability Rules

  Reference Principle VIII from constitution: Admin-Editable Content

**Editable by Admin**:

- Allowed attachment types and max sizes within safety limits.
- Keyword/phrase flags that trigger moderation or escalation cues.
- Notification preferences and quiet hours policy.

**Fixed in Codebase (Not Editable)**:

- Cryptographic standards and security controls.
- Read receipt semantics and audit logging requirements.
- Minimum retention periods mandated by compliance.

**Configurable with Restrictions**:

- Escalation routing rules (allowed destinations/roles only).
- Conversation export controls (available to specific admin roles).

### Payment & Billing Rules *(if applicable)*

  Delete this section if not applicable

Not applicable to messaging scope; no payment flows in this module.

---

## Success Criteria

  These should be testable without knowing implementation details

### Patient Experience Metrics

- **SC-001**: Patients receive visible confirmation that messages are sent within 1 second in 95% of attempts.
- **SC-002**: Patients see new replies within 5 seconds of being sent in 95% of conversations.
- **SC-003**: 90% of patient support inquiries receive a first response within 15 minutes during support hours.

### Provider Efficiency Metrics

- **SC-004**: Providers can locate and respond to an Admin message within 60 seconds using search and filters.
- **SC-005**: 95% of provider-admin messages acknowledge delivery within 2 seconds.
- **SC-006**: Escalation follow-ups to providers are actioned (first response) within 30 minutes during business hours for 90% of cases.

### Admin Management Metrics

- **SC-007**: Admins can find any conversation in under 10 seconds via search/filters in 95% of cases.
- **SC-008**: 100% of message events (send, read, escalation) recorded in audit logs and exportable.
- **SC-009**: Keyword flagging correctly highlights 95% of configured terms without false positives exceeding 5%.

### System Performance Metrics

- **SC-010**: 99.9% uptime for messaging read/send functionality measured monthly.
- **SC-011**: 95% of message send operations complete within 2 seconds under normal load.
- **SC-012**: Zero loss of persisted messages; queued messages eventually deliver or fail with explicit user notice.
- **SC-013**: Notifications delivered within 5 seconds in 95% of cases during support hours.

### Business Impact Metrics

- **SC-014**: Support-related patient satisfaction scores improve by 20% within 3 months of launch.
- **SC-015**: Aftercare-related follow-up compliance improves by 25% (measured by on-time scan submissions and questionnaire completions).
- **SC-016**: Support ticket volume for “how to contact support” declines by 50% within 1 month of launch.

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- P-01: Auth & Profile Management
  - Why needed: Identity and access control for participants.
  - Integration point: Use authenticated user context and roles for conversation access.

- S-03: Notification Service
  - Why needed: Deliver real-time alerts for new messages/escalations.
  - Integration point: Publish notification events on message state changes.

- S-05: Media Storage Service
  - Why needed: Secure storage and retrieval of attachments.
  - Integration point: Generate secure media links and metadata for threads.

### External Dependencies (APIs, Services)

- Device push notification providers (for mobile alerts)
  - Purpose: Deliver device notifications to patients.
  - Integration: Use platform-standard push delivery; fallback to in-app badges and email where applicable.
  - Failure handling: Queue retry; show in-app banners; notify user if delays persist.

### Data Dependencies

- Active user accounts with verified roles (patient, support, aftercare, provider, admin)
  - Why needed: Determine access and routing.
  - Source: P-01 Auth & Profile.

- Aftercare enrollment state for patient ↔ Aftercare channel
  - Why needed: Enables aftercare conversations post‑procedure.
  - Source: Aftercare modules.

---

## Assumptions

### User Behavior Assumptions

- Patients often contact support during/after booking and during aftercare.
- Patients may attach images/videos to clarify concerns.
- Majority of patient messaging occurs on mobile devices.

### Technology Assumptions

- Patients use smartphones with camera capabilities.
- Provider/Admin web apps accessed via modern browsers (latest 2 versions).
- Intermittent connectivity is common; pending/retry behavior required.
- Secure media storage is available for attachments.

### Business Process Assumptions

- Support and Aftercare teams monitor inboxes continuously during support hours and on-call for escalations.
- Admins have authority to initiate scan requests and schedule reviews.
- Providers respond to admin messages during business hours.

---

## Implementation Notes

### Technical Considerations

- Architecture: Real-time messaging delivery with persistence and audit logging.
- Technology: Media handling supports common mobile formats; background upload for large files.
- Performance: Degrade gracefully on poor connectivity with retries and clear status.
- Storage: Medical media retained per compliance with fast retrieval for care contexts.

### Integration Points

- Patient app → Messaging service
  - Data format: Structured message payloads with participant IDs and attachment metadata.
  - Authentication: Tenant-authenticated sessions; role-based permissions.
  - Error handling: Retry on transient failures; clear feedback to user.

- Admin dashboard → Messaging service
  - Data format: Queries for conversation lists, flags, and audit exports.
  - Authentication: Admin roles only; scoped access.
  - Error handling: Paged results; robust filtering; export fallbacks.

### Scalability Considerations

- Current scale: Expect dozens of concurrent conversations at launch; grow to hundreds.
- Growth projection: 5× growth in 12 months with seasonal peaks.
- Peak load: Handle sudden spikes (campaigns/incidents) without delivery delays.
- Data volume: Growing media attachments; efficient storage and lifecycle management required.
- Scaling strategy: Horizontally scalable messaging and notification services; background processing for heavy tasks.

### Security Considerations

- Authentication: Strong session controls; MFA required for Admin/Provider per policy.
- Authorization: Role-based access; least-privilege visibility to conversations.
- Encryption: All content encrypted in transit and at rest; media links protected.
- Audit trail: Immutable logs of access and message events retained per policy.
- Threat mitigation: Abuse prevention on messaging and media uploads; keyword moderation and rate controls.
- Compliance: Align with GDPR and HIPAA-equivalent standards; data residency honored.

---

## User Scenarios & Testing

### User Story 1 - Patient gets timely support (Priority: P1)

A patient opens Support, sends a message about a concern, and receives a timely response with reassurance.

Why this priority: Core to patient trust and platform value; reduces anxiety and improves satisfaction.

Independent Test: Send a message from a test patient; verify support receives, responds, and patient sees the reply with read receipts and notifications.

Acceptance Scenarios:

1. Given a logged-in patient on Support chat, when they send a valid text message, then the message appears in the thread with sending and sent states in under 1 second.
2. Given Support is active, when Support replies, then the patient sees the reply and receives a notification within 5 seconds.
3. Given Support opens the patient’s message, when the message is viewed, then the sender sees a read receipt within 2 seconds.

---

### User Story 2 - Escalate an urgent case (Priority: P1)

Support identifies a potentially urgent medical issue and escalates to an Aftercare Specialist, who responds promptly.

Why this priority: Patient safety and clinical responsiveness.

Independent Test: Flag a conversation as urgent; verify assignment, timestamped escalation, and patient notification.

Acceptance Scenarios:

1. Given a support agent in a conversation, when they flag the thread as urgent and choose an assignee, then the system records the escalation and assigns ownership.
2. Given an assigned specialist, when the escalation is created, then the specialist receives a notification and sees the conversation in their priority queue.

---

### User Story 3 - Provider coordinates with Admin (Priority: P2)

A provider reaches out to Admin regarding a billing clarification and receives resolution.

Why this priority: Ensures smooth operations between partners and Hairline.

Independent Test: Provider sends a message; Admin replies; provider receives and acknowledges.

Acceptance Scenarios:

1. Given a logged-in provider, when they send a message to Admin, then Admin’s inbox shows the new thread with unread badge and preview.
2. Given Admin replies, when the provider opens the thread, then the message shows with read status and any attachments.

### Edge Cases

- Excessive attachments in one message: enforce count/size limits and communicate clearly.
- No response within defined SLA: auto-remind assigned party; allow admin to re-route/close with reason.
- Account deletion request with open conversations: archive conversations; restrict access per policy.
- Simultaneous sends: maintain message ordering and idempotency safeguards.

---

## Functional Requirements Summary

### Core Requirements

- FR-001: System MUST enable in-app messaging for Patient ↔ Support and Patient ↔ Aftercare with text and media.
- FR-002: System MUST deliver real-time notifications for new messages to intended recipients.
- FR-003: Users MUST be able to view complete conversation history with timestamps and read receipts.
- FR-004: System MUST enforce attachment type and size limits and provide user feedback on violations.
- FR-005: System MUST log message lifecycle events (sent, delivered, read, escalated) for audit.

### Data Requirements

- FR-006: System MUST maintain conversations per participant with searchable metadata (channel, status, flags).
- FR-007: System MUST store attachments securely with links to their parent messages and access controls.

### Security & Privacy Requirements

- FR-008: System MUST restrict visibility so patients cannot directly message providers in V1.
- FR-009: System MUST encrypt all message content and media in transit and at rest and protect access by role.
- FR-010: System MUST retain medical communications for at least 7 years and support audit export for compliance.

### Integration Requirements

- FR-011: System MUST integrate with Notification Service to send alerts on message events.
- FR-012: System MUST integrate with Media Storage Service for attachments with secure retrieval.

### Marking Unclear Requirements

No unresolved clarifications remain for this scope. Direct Patient ↔ Provider messaging is explicitly out of scope for V1 and tracked as a potential future enhancement.

---

## Key Entities

- Entity 1 - Conversation: Thread of messages between participants for a specific channel.
  - Key attributes: participants, channel (Support/Aftercare/Admin/Provider), status, flags, created/updated times, escalation data.
  - Relationships: Has many messages; belongs to participants.

- Entity 2 - Message: Single unit of communication within a conversation.
  - Key attributes: sender, text, attachments, timestamps (sent/read), delivery/read status.
  - Relationships: Belongs to one conversation; has many attachments; generates notifications.

- Entity 3 - Attachment: Media linked to a message.
  - Key attributes: type, size, secure location, thumbnail/preview metadata.
  - Relationships: Belongs to one message; access controlled by conversation permissions.

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-11 | 1.0 | Initial PRD creation | AI |
| 2025-11-11 | 1.1 | Filled scope, workflows, rules, and criteria | AI |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | [Name] | [Date] | [Status] |
| Technical Lead | [Name] | [Date] | [Status] |
| Stakeholder | [Name] | [Date] | [Status] |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-011 Aftercare & Recovery Management PRD
**Last Updated**: 2025-11-03
