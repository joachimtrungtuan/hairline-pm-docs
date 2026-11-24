# FR-012 - Messaging & Communication

**Module**: P-06: Communication | PR-07: Communication & Messaging | A-10: Communication Monitoring & Support  
**Feature Branch**: `fr012-secure-messaging`  
**Created**: 2025-11-11  
**Status**: ✅ Verified & Approved  
**Source**: FR-012 from local-docs/project-requirements/system-prd.md; Transcriptions (HairlineApp-Part1/Part2, Hairline-AdminPlatform-Part1/Part2)

---

## Executive Summary

Enable secure, auditable, real-time messaging and audio/video communication between patients and providers across the Hairline platform to support quote clarification, procedure coordination, and patient care. Patients can communicate directly with providers throughout their journey from quote review through post-procedure phases via text messaging, media sharing, and live audio/video calls. Admins monitor all conversations with keyword flagging and can intervene ONLY in emergency situations (serious policy violations, urgent disputes, patient safety emergencies). The module supports text and media messages, audio/video calls via Twilio, read receipts, conversation history, and real-time notifications, improving response times, patient reassurance, provider communication efficiency, and operational transparency while meeting medical data privacy obligations.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-06)**: In-app chat with providers for quote questions, procedure clarifications, and coordination; audio/video calls for live consultations; notifications for new messages and calls; view conversation history; send text and media.
- **Provider Platform (PR-07)**: Direct messaging with patients for quote clarification, procedure coordination, and post-booking questions; audio/video call capability for consultations; view conversation history; send text and media responses.
- **Admin Platform (A-10)**: Communication monitoring center for oversight, keyword flagging, and compliance logging; read-only monitoring with emergency-only intervention capability for critical situations (serious policy violations, urgent disputes, patient safety emergencies).
- **Shared Services (S-03, S-05)**: Notification Service for push/email alerts; Media Storage Service for secure handling of images/videos attached to messages; Twilio integration for audio/video calls.

### Multi-Tenant Breakdown

**Patient Platform (P-06)**:

- View Messages Inbox with all provider conversations; filter by read/unread status; search by provider name or message content; sort by latest activity or date.
- See conversation previews with last message, unread counts, and timestamps; real-time updates.
- Open individual conversations to view full chat history with provider.
- Compose and send messages to providers (quote clarification, procedure questions, coordination).
- Initiate or receive audio/video calls with providers for live consultations and discussions via Twilio.
- Attach media to messages (REQ-012-009).
- View thumbnails and playback inline for images/videos; download PDFs. (REQ-012-039, REQ-012-043)
- See read receipts and timestamps per message.
- Receive real-time notifications for new provider messages and incoming calls; badge counts for unread in inbox and app navigation.
- Chat and call features available from quote received through post-procedure phases. (REQ-012-031)

**Provider Platform (PR-07)**:

- Access Messages popup/submenu from header navigation showing recent patient conversations with unread counts.
- Quick view of most recent 10 conversations in popup; "View All" for full list.
- Send and receive messages with patients for quote-related questions and procedure coordination.
- Initiate or receive audio/video calls with patients for consultations and detailed explanations via Twilio.
- View conversation history per patient with timestamps and read receipts.
- Attach media to responses: Images for before/after photos and facility images, Video for procedure demonstrations, PDF for treatment plans (REQ-012-009).
- Receive notifications for new patient messages and incoming calls; unread badge on header messages icon.
- Conversations visible for patients who have received quotes from this provider.

**Admin Platform (A-10)**:

- Communication Monitoring Center as primary message list: monitor all patient ↔ provider conversations with read-only access (default).
- Comprehensive filtering and search: by patient, provider, service type, quote ID, inquiry ID, date range, keyword flags, manual observation flags, intervention status; all filters applied simultaneously.
- Conversation list with preview, participants, last message timestamp, flag indicators, inquiry reference.
- Automatic keyword flagging system to detect off-platform solicitation or policy violations (red flags).
- **Manual flagging for observation**: Admin can flag conversations for closer monitoring without notifying users (orange flags); flag types: Off-Platform Risk, Potential Dispute, Quality Concern, Follow-Up Needed, Other.
- Flag history tracking: view all flag events, status changes, and admin notes for each conversation.
- Select conversation to open detailed Message Thread View for full conversation history, participant info, flag management, and actions.
- **Emergency intervention capability**: Admin can send messages ONLY in critical situations (serious policy violations, urgent disputes, patient safety emergencies).
- Intervention actions: flag for observation, resolve flags (REQ-012-077).
- Configure moderation rules and automatic keyword flags; maintain compliance audit trail.
- Admin emergency messages clearly identified with "Hairline Admin" badge; logged with mandatory reason.

**Shared Services (S-03, S-05, Twilio)**:

- S-03 Notification Service to deliver timely user alerts (push/email as configured).
- S-05 Media Storage for secure storage and retrieval of attachments; virus/malware scanning pipeline: every attachment from a patient, provider or admin is scanned, and a file that fails the scan is refused. (REQ-012-044)
- Twilio for audio/video call infrastructure and real-time communication.

### Communication Structure

**In Scope**:

- Patient ↔ Provider in-app messaging (quote questions, procedure clarifications, post-booking coordination).
- Text and media messages with attachments (REQ-012-009).
- See REQ-012-043.
- Real-time notifications, read receipts, conversation history, and compliance logging.
- Admin monitoring with keyword flagging for compliance and policy enforcement.
- **Emergency-only admin intervention** for critical situations (monitoring target: under 5% of conversations, REQ-012-024).
- See REQ-012-031.
- **Audio and video call functionality** using Twilio for real-time consultation and communication between patients and providers. Calls are started from the chat header; each call leaves a system entry in the conversation (audio or video, start time, duration, outcome answered, missed, declined or failed), shown in the thread but not counted as an unread message, as the last-message preview or toward the monthly count of conversations with at least one message, and call content is not recorded or monitored. (REQ-012-032)

**Out of Scope**:

- SMS channel management (handled by S-03 Notification Service configuration; **SMS as a transport for secure messaging is not part of MVP and will only be available if/when S-03 adds SMS support in a later phase**). (REQ-012-030)
- Routine admin participation in conversations (admin intervention is emergency-only, not standard practice). (REQ-012-030)
- Patient ↔ Hairline Support general help (may be added in future release; currently handled outside messaging module). (REQ-012-030)
- Patient ↔ Aftercare Team specialized support (may be added in future release; currently handled outside messaging module). (REQ-012-030)

### Entry Points

**Automatic Chat Creation**: See REQ-012-001 and REQ-012-025.

**Patient Platform**: Patients access their Messages/Inbox screen (Screen 1) from the main navigation in the mobile app. The inbox displays all conversations with providers who have sent quotes, with filtering and search capabilities. Chat is NOT embedded in quote detail screens—a quote screen may link to the conversation in the dedicated inbox (REQ-005-015), where chat takes place. (REQ-012-029)

**Provider Platform**: Providers access patient conversations through a Messages popup/submenu in the header navigation (Screen 3), showing recent conversations with unread counts. The popup provides quick access to recent messages; tapping a conversation opens the full chat view (Screen 4). New conversations appear when providers submit quotes. Chat is NOT accessible from quote detail or inquiry screens—only from the dedicated messages list. (REQ-012-029)

**Admin Platform**: Admins access the Communication Monitoring Center from the Admin platform navigation (Screen 5), which serves as the comprehensive message list monitoring all patient-provider conversations. The center includes advanced filtering by patient, provider, service, quote/inquiry ID, date range, flags, and intervention status. Selecting a conversation opens the detailed Message Thread View (Screen 6A) for review and flagging; admins can activate Emergency Intervention mode (Screen 6B) if critical situation requires direct messaging. (REQ-012-029)

**Notifications**: Push/email notifications deep-link users directly into the specific conversation in their inbox. (REQ-012-029) Keyword flags alert admins and deep-link to flagged conversations for review. (REQ-012-094)

---

## Business Workflows

### Main Flow: Patient ↔ Provider Messaging

**Actors**: Patient, Provider, Admin (emergency monitoring), System  
**Trigger**: Provider submits a quote for a patient inquiry  
**Outcome**: Conversation available (created if first quote, or existing conversation reused if subsequent quote); patient and provider can exchange messages; conversation logged; admin can monitor and intervene only in emergencies

**Steps**:

1. Provider submits quote for patient inquiry; system checks if conversation already exists for this patient-provider pair:
   - **If first quote**: System creates a new conversation, adds inquiry/quote ID.
   - **If subsequent quote**: System adds new inquiry/quote ID to existing conversation's quote_references array.
2. Conversation appears in patient's Messages/Inbox (Screen 1) and provider's Messages/Inbox immediately (or moves to top if existing); patient sees conversation preview with provider name and unread badge.
3. Patient opens their Messages/Inbox, sees new conversation with unread badge, taps to open full chat (Screen 2).
4. Patient composes a text message with questions (e.g., about procedure, packages, pricing, timing) and optionally attaches media; taps Send.
5. System validates content (size/type), records the message, and updates conversation state.
6. System delivers real-time notification to Provider and updates unread counters in provider's inbox.
7. Provider opens the conversation from their Messages/Inbox, reads the message; system records read receipt.
8. Provider replies with clarifications or additional information; patient receives notification and sees unread badge in inbox.
9. Patient opens conversation from inbox; sees new message in real time; unread badge clears.
10. System logs all events (sent, delivered, read) to audit trail; conversation remains searchable; admin can monitor with keyword flagging.

### Alternative Flows

**A1: Attachment Flow**:

- **Trigger**: Patient, provider or admin includes attachment (images, videos, or PDFs; admins attach images and PDFs only)
- **Steps**:
  1. System validates each attachment's file type (JPG/PNG, MP4, or PDF) and size (images max 5MB, video max 10MB, PDF max 10MB) and the attachment count (max 5 per message), and scans it for malware.
  2. If valid, system stores media securely and links it to the message; generates thumbnails for images/videos.
  3. If a file fails validation or the scan, system refuses that file with a specific error message; the message can still be sent without it.
- **Outcome**: Valid attachments appear in the thread with preview (images/videos) or download link (PDFs); recipients can view/playback/download.

**A2: Admin Manual Flagging for Observation**:

- **Trigger**: Admin identifies conversation requiring closer monitoring but not immediate intervention (suspicious pattern, borderline language, emerging dispute)
- **Steps**:
  1. Admin reviews conversation and identifies potential concern.
  2. Admin selects "Flag for Observation" action.
  3. System prompts admin to select flag type: "Off-Platform Risk" / "Potential Dispute" / "Quality Concern" / "Follow-Up Needed" / "Other".
  4. Admin optionally adds internal notes (not visible to patient/provider).
  5. System marks conversation with flag badge in admin dashboard.
  6. Flagged conversations appear in admin's "Flagged" filter for easy tracking.
  7. System logs flag action with timestamp, admin user, flag type, and notes.
- **Outcome**: Conversation marked for closer observation; admin can monitor developments; flag history tracked for review; no notification sent to patient/provider.

**A3: Admin Emergency Intervention**:

- **Trigger**: Admin detects CRITICAL situation requiring immediate intervention (serious policy violation, urgent dispute, patient safety emergency)
- **Steps**:
  1. Admin identifies emergency via automatic keyword flag, manual observation flag escalation, or direct detection in Screen 6A (Message Thread Detail - Monitoring).
  2. Admin clicks "Enable Emergency Intervention" button and confirms action; system activates Screen 6B (Emergency Intervention Mode), sets the conversation's active flags to escalated_to_intervention, and the conversation status becomes Escalated. Cancelling Screen 6B without sending changes nothing: the flags and the status return to what they were before enabling.
  3. Screen 6B displays prominent warning banner: "🚨 EMERGENCY INTERVENTION MODE - Both patient and provider will be notified".
  4. Admin selects mandatory emergency reason (Policy Violation / Urgent Dispute / Patient Safety) and optionally adds internal justification notes.
  5. Admin reviews full conversation context and flag history (still visible in Screen 6B).
  6. Admin composes emergency intervention message clearly addressing both parties (e.g., policy enforcement, dispute mediation, safety guidance).
  7. Admin reviews preview and clicks Send; both patient and provider receive immediate notification.
  8. System marks message with "Hairline Admin" badge in conversation thread (visible to all parties).
  9. System logs emergency intervention with timestamp, admin user, emergency reason, justification notes, and full message content.
  10. If conversation was previously flagged, system updates flag status to "Intervention Completed"; unless the post-intervention flag setting is off, system raises a system flag with category Follow-Up Needed for follow-up review.
  11. System returns admin to Screen 6A with intervention message visible in thread.
- **Outcome**: Emergency situation addressed; policy enforced; patient/provider receive authoritative guidance; intervention logged for audit and compliance review; conversation state updated.

**A4: Audio or Video Call**:

- **Trigger**: Patient or provider taps Audio Call or Video Call in the chat header
- **Steps**:
  1. Patient or provider taps Audio Call or Video Call in the chat header.
  2. System connects the call through Twilio and notifies the other party of the incoming call; the other party answers, declines or does not answer. If the call cannot be established, REQ-012-033 applies and the call is recorded with outcome failed.
  3. System writes a call entry in the conversation thread (sender: system) with audio or video, start time, duration and outcome (answered, missed, declined or failed); the entry does not count as an unread message, as the last-message preview, or toward the monthly count of conversations with at least one message.
- **Outcome**: Every call leaves a record in the conversation; call content is not recorded or monitored.

**B1: Invalid Content**:

- **Trigger**: Attachment exceeds limits, has an unsupported type or fails the malware scan
- **Steps**:
  1. System validates attachment before upload.
  2. If invalid, system blocks upload and displays specific error:
     - "Image must be JPG or PNG format, max 5MB"
     - "Video must be MP4 format, max 10MB"
     - "PDF must be max 10MB"
     - "Maximum 5 attachments per message"
     - "This file failed the security scan and was not attached"
  3. User can retry with valid content or send the message without the refused file.
- **Outcome**: Only valid content sent; conversation integrity maintained; clear user guidance provided.

**B2: Intermittent Connectivity**:

- **Trigger**: Network lost during send
- **Steps**:
  1. System queues the message locally and indicates pending state.
  2. On reconnect, system retries; if failure persists, prompts user to resend.
- **Outcome**: Message eventually sent or user notified to retry; no silent loss.

---

## Screen Specifications

### Patient Platform

#### Screen 1: Messages Inbox (Patient)

**Purpose**: Allow patients to view all their conversations with providers, filter and search messages, see unread counts, and select a conversation to open.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Search | text | No | Search conversations by provider name, message content | Min 2 chars | no graph field (control) |
| Filter by Status | select | No | Filter conversations by read/unread status | Options: All / Unread / Read | no graph field (control) |
| Sort by | select | No | Sort conversations | Options: Latest Activity (default) / Provider Name / Date Created | no graph field (control) |
| Conversation list | list | Yes | Shows all patient-provider conversations with preview | Paginated; 20 per page (REQ-012-047) | no graph field (list of the rows below) |
| Provider avatar | image | Yes | Provider profile picture or placeholder | Read-only; displayed in list | ENT-provider-profile.logo_url |
| Provider name | text | Yes | Provider name and clinic | Read-only; displayed in list | ENT-provider.name, ENT-provider-profile.clinic_name |
| Last message preview | text | Yes | Preview of last message (truncated) | Max 100 chars; shows "You: " prefix if patient sent (REQ-012-047) | ENT-conversation.last_message_preview |
| Unread badge | indicator | N/A | Shows unread message count | Red badge with count; hidden if 0 | ENT-conversation.unread_count |
| Timestamp | text | Yes | Time of last message | Relative (e.g., "2h ago") or absolute (e.g., "Dec 19") (REQ-012-047) | ENT-conversation.last_message_at |
| Admin intervention indicator | badge | No | Shows if admin has intervened in conversation | Conditional: Visible ONLY if 'admin_intervened' is true. Orange "Admin" badge. (REQ-012-049) | ENT-conversation.admin_intervened |

**Business Rules**:

- See REQ-012-001 and REQ-012-025.
- **One conversation per provider**: patient sees only one entry for that provider in inbox (REQ-012-001).
- Conversations sorted by latest activity by default (most recent at top). (REQ-012-046)
- Unread count badge updates in real-time when new messages arrive. (REQ-012-048)
- Tapping a conversation opens the full chat view (Screen 2). (REQ-012-051)
- Search searches provider name and message content; results update as user types. (REQ-022-070)
- Empty state message shown when no conversations exist: "No messages yet. When a provider sends you a quote, a conversation will start here." (REQ-012-050)
- Pull-to-refresh to sync latest messages. (REQ-012-050)
- Archived conversations hidden by default (future feature). (REQ-012-050)

**Notes**:

- Display clear visual distinction between read and unread conversations (bold text for unread). (REQ-012-048)
- Show typing indicator in conversation preview if provider is actively typing. (REQ-012-051)
- Long-press on conversation for quick actions: Mark as Read/Unread, Archive (future). (REQ-012-051)
- Smooth scroll performance even with 50+ conversations.
- Skeleton loading state while fetching conversation list.

---

#### Screen 2: Patient ↔ Provider Chat (Patient)

**Purpose**: Allow patients to message providers with quote questions, procedure clarifications, and coordination questions; receive timely responses.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Message text | text | No | Core message body; text or at least one attachment is needed to send | Max 2000 chars; a message with flagged terms warns the patient but is not blocked: it is sent and raises an automatic keyword flag (REQ-012-035) | ENT-message.text |
| Attachment | image/video/pdf | No | Optional media to support the message; a message may be attachment-only | See REQ-012-009. | ENT-message.attachments |
| Translation switch | toggle | No | On/off switch for machine translation of messages for the reader | Shown and working only while the platform-wide translation switch (FR-021) is on; behavior owned by FR-021 (REQ-012-108) | no graph field (control) |
| Provider name | display | Yes | Shows provider name and clinic | Read-only; contextual to conversation | ENT-provider.name, ENT-provider-profile.clinic_name |
| Audio Call button | action | Yes | Initiates audio call via Twilio | Icon button in header; disabled if provider offline (optional) (REQ-012-032) | no graph field (control) |
| Video Call button | action | Yes | Initiates video call via Twilio | Icon button in header; disabled if provider offline (optional) (REQ-012-032) | no graph field (control) |
| Send button | action | Yes | Submits message | See REQ-012-037. | no graph field (control) |
| Read status | indicator | N/A | Shows if message was read by provider | Auto-updated in real time | ENT-message.read_at |
| Call entry | indicator | N/A | System entry for a call: audio or video, start time, duration and outcome (answered, missed, declined or failed) | Read-only; not counted as an unread message, last-message preview or toward the monthly conversations-with-a-message figure (REQ-012-032) | ENT-message.call_type, ENT-message.call_started_at, ENT-message.call_duration_seconds, ENT-message.call_outcome |

**Business Rules**:

- Show typing/sending states and error states; retry control available for failed sends. (REQ-012-038)
- Submit disabled until message text or attachment is provided. (REQ-012-037)
- See REQ-012-008.
- On a read-only conversation the composer, attach control and call buttons are disabled with a banner giving the reason. (REQ-012-018)
- See REQ-012-001.
- See REQ-012-006.
- See REQ-012-001.
- Conversation accessible from quote received through post-procedure phases across all treatments with that provider. (REQ-012-031)
- See REQ-012-013 and REQ-012-014.

**Notes**:

- Provide clear attachment guidance (REQ-012-041).
- Display file size and type before upload; show validation errors if limits exceeded. (REQ-012-041)
- See REQ-012-009.
- See REQ-012-052.
- See REQ-012-024 and REQ-012-090.

---

### Provider Platform

#### Screen 3: Messages List (Provider)

**Purpose**: Allow providers to view and filter their patient conversations in a popup submenu from the header navigation, see unread counts, and quickly access specific patient chats.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Search | text | No | Search by patient identifier (masked until payment is confirmed), inquiry/quote ID, or message content | Min 2 chars; filters list in real-time | no graph field (control) |
| Filter: Read Status | toggle | No | Filter by read/unread conversations | Options: All / Unread Only | no graph field (control) |
| Filter: Date Range | dropdown | No | Filter by activity date | Options: Today / Last 7 days / Last 30 days / All | no graph field (control) |
| Filter: Service Type | dropdown | No | Filter by treatment/service category | Options from service catalog | no graph field (control) |
| Clear Filters | button | No | Reset all filters | Returns to default view (recent 10) | no graph field (control) |
| Conversation list | list | Yes | Shows provider-patient conversations with preview | Displayed in popup/dropdown from header; shows up to 20 filtered results | no graph field (list of the rows below) |
| Patient name | text | Yes | Patient name (anonymized until payment per FR-003) | Read-only; displayed in list (REQ-012-028) | ENT-patient.name, ENT-patient.anonymized_id |
| Inquiry/Quote ID | text | No | Associated inquiry or quote reference | Displayed if available; helps identify case | ENT-conversation.inquiry_ids, ENT-conversation.quote_references |
| Service type | text | Yes | Treatment category for context | Read-only; brief label | ENT-conversation.service_types |
| Last message preview | text | Yes | Preview of last message (truncated) | Max 50 chars; shows "You: " prefix if the viewer sent it (REQ-012-055) | ENT-conversation.last_message_preview |
| Unread badge | indicator | N/A | Shows unread message count | Red badge with count, one count per clinic (REQ-012-001); hidden if 0 | ENT-conversation.unread_count |
| Timestamp | text | Yes | Time of last message | Relative (e.g., "1h ago") | ENT-conversation.last_message_at |
| Future phase: View All Messages | link | No | Link to full messages page if needed | Opens expanded view (future enhancement) (REQ-012-057) | no graph field (control) |

**Business Rules**:

- Accessible from header navigation as popup/submenu (always visible, no navigation required). (REQ-012-053)
- Default view: most recent 10 conversations sorted by latest activity. (REQ-012-053)
- **One conversation per patient**: provider sees only one entry for that patient (REQ-012-001).
- Filters applied in real-time as provider types/selects; up to 20 filtered results shown. (REQ-012-054)
- Search filters across the patient identifier (masked until payment is confirmed), inquiry/quote ID, and message content simultaneously. (REQ-012-054)
- Inquiry/Quote ID search useful when provider wants to reference specific treatment within a patient conversation. (REQ-012-054)
- Unread count badge displayed on header messages icon (total unread across all conversations). (REQ-012-056)
- Tapping a conversation closes popup and opens full chat view (Screen 4) with that conversation loaded. (REQ-012-053)
- Real-time updates when new patient messages arrive; unread badge updates immediately. (REQ-012-056)

**Notes**:

- Lightweight popup interface with filtering for quick message management.
- Filters help providers prioritize urgent or specific conversations (e.g., "Show unread from last 7 days").
- If more than 20 results, show "Showing 20 of X conversations - refine filters" message. (REQ-012-055)
- Mobile: may slide in from side with collapsible filter section; Desktop: dropdown from header with inline filters.
- Filters persist during session until cleared. (REQ-012-054)

---

#### Screen 4: Provider ↔ Patient Chat (Provider)

**Purpose**: Allow providers to respond to patient questions about quotes, procedures, and coordination; build trust and clarify details before booking.

**Layout Structure**: 3-panel layout for desktop/tablet (responsive for mobile)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Panel Location | Graph field |
|------------|------|----------|-------------|------------------|----------------|-------------|
| **LEFT PANEL: Conversation List** | | | | | | |
| Conversation list | list | Yes | Shows all provider's patient conversations with preview | Synchronized with Screen 3; shows same conversations | Left | no graph field (list of the rows below) |
| Patient name | text | Yes | Patient identifier in list | Read-only; anonymized per FR-003 | Left | ENT-patient.name, ENT-patient.anonymized_id |
| Last message preview | text | Yes | Preview of last message | Max 50 chars; "You: " prefix if the viewer sent it | Left | ENT-conversation.last_message_preview |
| Unread badge | indicator | N/A | Shows unread count | Red badge with number; one count per clinic (REQ-012-001) | Left | ENT-conversation.unread_count |
| Timestamp | text | Yes | Time of last message | Relative (e.g., "1h ago") | Left | ENT-conversation.last_message_at |
| Active indicator | highlight | Yes | Shows currently selected conversation | Highlighted background for selected conversation | Left | no graph field (control) |
| **CENTER PANEL: Message Thread** | | | | | | |
| Message thread | scrollable panel | Yes | Full conversation history with selected patient | Chronological order; auto-scroll to latest | Center | no graph field (list of the message rows below) |
| Message text | text | Yes | Each message content | Read-only for history | Center | ENT-message.text |
| Message sender | indicator | Yes | Shows if patient, provider, admin or system sent | "You" on the viewer's own messages and the colleague's name on other clinic team members' messages, the patient's masked identifier until payment is confirmed and then the patient name, "Hairline Admin", "System" for call entries (REQ-012-060) | Center | ENT-message.sender |
| Message timestamp | datetime | Yes | When message was sent | Displayed per message | Center | ENT-message.sent_at |
| Message attachments | thumbnails/links | No | Images, videos, PDFs in messages | Clickable to view/download | Center | ENT-message.attachments |
| Read status | indicator | N/A | Shows if message was read by patient | Checkmark or "Read" indicator per message | Center | ENT-message.read_at |
| Call entry | indicator | N/A | System entry for a call: audio or video, start time, duration and outcome (answered, missed, declined or failed) | Read-only (REQ-012-032) | Center | ENT-message.call_type, ENT-message.call_started_at, ENT-message.call_duration_seconds, ENT-message.call_outcome |
| Admin badge | indicator | N/A | "Hairline Admin" badge on admin messages | Visible if admin intervened | Center | ENT-message.admin_badge |
| Compose message area | textarea | Yes | Provider response to patient questions | Max 2000 chars; at bottom of center panel; a message may be attachment-only | Center | ENT-message.text |
| Attachment upload | file upload | No | Add supporting media | See REQ-012-009. | Center | ENT-message.attachments |
| Translation switch | toggle | No | On/off switch for machine translation of messages for the reader | Shown and working only while the platform-wide translation switch (FR-021) is on; behavior owned by FR-021 (REQ-012-108) | Center | no graph field (control) |
| Send button | action | Yes | Submits message | See REQ-012-037. | Center | no graph field (control) |
| **RIGHT PANEL: Conversation Info & Tools** | | | | | | |
| Patient identifier | display | Yes | Patient name and ID (anonymized until payment per FR-003) | Read-only; contextual header | Right | ENT-patient.name, ENT-patient.anonymized_id |
| Patient avatar | image | No | Patient profile picture once payment is confirmed, placeholder before | Displayed at top of right panel | Right | ENT-patient.profile_picture |
| Audio Call button | action | Yes | Initiates audio call via Twilio | Icon button in header/tools panel | Right | no graph field (control) |
| Video Call button | action | Yes | Initiates video call via Twilio | Icon button in header/tools panel | Right | no graph field (control) |
| Quote references | list | No | All quotes associated with this patient-provider pair | Clickable links to quotes; shows inquiry/quote IDs with service types (e.g., "Quote #123 - Hair Transplant"); helps provider maintain context across multiple treatments | Right | ENT-conversation.quote_references |
| Service types | list | Yes | Treatment categories for all quotes | Read-only; comma-separated if multiple | Right | ENT-conversation.service_types |
| Conversation started | datetime | Yes | When conversation was created | Read-only | Right | ENT-conversation.created_at |
| Message count | number | Yes | Total messages in thread | Read-only; updates live | Right | ENT-conversation.message_count |
| Flag indicator | badge | N/A | Shows if the conversation has an open flag of any type (keyword, manual or system) | Warning icon if the conversation has an open flag of any type | Right | ENT-conversation.keyword_flags, ENT-conversation.manual_observation_flags, ENT-flag.status |
| Actions menu | buttons | No | Additional conversation actions | Options: Archive (future), View patient profile (hidden until payment is confirmed); Export conversation is deferred to a future phase (REQ-012-061) | Right | no graph field (control) |

**Business Rules**:

- Provider can only message patients who have received quotes from them. (REQ-012-018, REQ-012-063)
- On a read-only conversation the composer, attach control and call buttons are disabled with a banner giving the reason. (REQ-012-018)
- See REQ-012-001.
- Quote references section shows ALL inquiry/quote IDs chronologically, helping provider track which treatment each message refers to. (REQ-012-058)
- Patient identity is anonymized (e.g., "Mark P." + ID) until payment confirmation per FR-003; until then the sender label, avatar and search on this screen use the masked identifier and View patient profile is hidden. (REQ-012-028)
- All conversations monitored by admin with keyword flagging for compliance. (REQ-012-021, REQ-012-094)
- See REQ-012-010.
- Provider sees full conversation history with timestamps and read receipts across all treatments with that patient. (REQ-012-059)
- See REQ-012-013 and REQ-012-014.

**Notes**:

- **3-panel layout**: Left panel (conversation list), Center panel (message thread with compose area), Right panel (patient info & tools).
- **Desktop/Tablet**: All 3 panels visible simultaneously; left panel width ~25%, center panel ~50%, right panel ~25%.
- **Mobile**: Single panel view with navigation; left panel (list) → center panel (messages) when conversation selected; right panel accessible via info icon.
- **Left panel**: Synchronized with Screen 3 (popup); selecting conversation updates center and right panels without full page reload.
- **Center panel**: Auto-scrolls to latest message when conversation opens; compose area fixed at bottom.
- **Right panel**: Always shows context for selected conversation; quote references section collapses if no multiple quotes.
- Encourage providers to respond within 24 hours for best patient experience. (REQ-012-062)
- See REQ-012-058.
- Providers can attach treatment plans (PDF), facility photos (JPG/PNG), or before/after examples (JPG/PNG/MP4) to build trust. (REQ-012-062)
- See REQ-012-009 and REQ-012-041.
- Providers should reference specific quote ID in messages when discussing different treatments (e.g., "Regarding your hair transplant quote #123..."). (REQ-012-062)
- Clear indication when message contains flagged keywords (warning shown to provider before sending); the message is not blocked, it is sent and raises an automatic keyword flag. (REQ-012-036)
- See REQ-012-024 and REQ-012-090.

---

### Admin Platform

#### Screen 5: Communication Monitoring Center (Admin)

**Purpose**: Comprehensive message list monitoring all patient-provider conversations with advanced filtering and search capabilities for compliance, policy enforcement, and case investigation.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Search | text | No | Find conversations by patient, provider, keyword, inquiry ID | Min 2 chars; searches across all fields | no graph field (control) |
| Filters | multi-component | No | Comprehensive filtering bar with: Patient (autocomplete), Provider (autocomplete), Service Type (multi-select), Quote ID (text), Inquiry ID (text), Date Range (date picker with presets: Today/Last 7 days/Last 30 days), Flag Type (multi-select: Keyword Flagged/Manually Flagged/System Flagged/Intervened/No Flags), Flag Category (multi-select: Off-Platform Risk/Potential Dispute/Quality Concern/Follow-Up Needed/Other), Conversation Status (multi-select: Active/Resolved/Escalated) | All filters applied simultaneously with AND logic; filters persist across session | no graph field (control) |
| Apply Filters | button | No | Apply all selected filters simultaneously | All filters combined with AND logic | no graph field (control) |
| Clear Filters | button | No | Reset all filters to default | Restores full conversation list | no graph field (control) |
| Sort By | dropdown | No | Sort conversation list | Options: Latest Activity / Oldest First / Most Flagged / Provider Name / Patient Name (REQ-012-065) | no graph field (control) |
| Conversation list | list | Yes | Shows all conversations with preview, participants, flags, timestamps | See REQ-012-066. | no graph field (list of the rows below) |
| Patient name | text | Yes | Real patient name (admins see the unmasked name) | Read-only; displayed in list | ENT-patient.name |
| Provider name | text | Yes | Provider/clinic name | Read-only; displayed in list | ENT-provider.name |
| Inquiry ID | text | No | Associated inquiry reference | Displayed if available | ENT-conversation.inquiry_ids |
| Last message preview | text | Yes | Preview of last message | Max 100 chars | ENT-conversation.last_message_preview |
| Keyword flags | badge | N/A | Red badge for automatic keyword flags | Shows count if multiple | ENT-conversation.keyword_flags |
| Manual flags | badge | N/A | Orange badge for admin observation flags | Shows flag type on hover | ENT-conversation.manual_observation_flags |
| Intervention indicator | badge | N/A | Shows if admin has intervened | "Admin" badge if intervention occurred | ENT-conversation.admin_intervened |
| Timestamp | text | Yes | Time of last message | Relative (e.g., "2h ago") or absolute | ENT-conversation.last_message_at |
| Message count | number | Yes | Total messages in conversation | Displayed in list | ENT-conversation.message_count |
| Intervention rate | indicator | N/A | Interventions in the current calendar month divided by conversations with at least one message in that month (call entries are not messages), shown against the monitoring target of under 5% | Read-only; the target blocks nothing (REQ-012-024) | no graph field (dashboard panel) |
| Intervention success rate | indicator | N/A | Successful interventions divided by interventions older than 30 days | Read-only; worked out when the screen is read, no stored result (REQ-012-089) | no graph field (dashboard panel) |
| Moderation keyword list | list | No | Keywords and phrases that raise an automatic keyword flag | Editable by admins; saved with the Save action of the Moderation settings group (REQ-012-105) | no graph field (setting) |
| Post-intervention flag | toggle | No | Whether the system raises a follow-up flag after an emergency intervention | On by default; saved with the Save action of the Moderation settings group (REQ-012-089, REQ-012-105) | no graph field (setting) |
| Save moderation settings | button | No | Saves the keyword list and the post-intervention flag switch together | Each saved change is written to the audit log as a moderation setting change (REQ-012-010, REQ-012-105) | no graph field (control) |

**Business Rules**:

- Accessible from Admin platform main navigation as primary monitoring interface. (REQ-012-029)
- Shows ALL patient-provider conversations by default; filters narrow the view. (REQ-012-064)
- Filters, how they combine, and that they are remembered are stated once in REQ-022-122 (FR-022); the filter fields are listed in the data fields above.
- See REQ-012-068.
- Conversation list updates in real-time when new messages arrive or flags are added. (REQ-012-067)
- Keyword flags (red badges) automatically appear when policy violation terms detected. (REQ-012-094)
- Manual observation flags (orange badges) added by admins for proactive monitoring. (REQ-012-095)
- The follow-up queue is this screen filtered by the Follow-Up Needed flag category. (REQ-012-098)
- Moderation settings group: admins edit the keyword list and the post-intervention flag switch here and save them with one Save action. (REQ-012-105)
- Tapping/selecting a conversation opens detailed Message Thread View (Screen 6A) for full history, flag management, and optional emergency intervention activation (Screen 6B). (REQ-012-067)
- Pagination with 20 conversations per page; scroll to load more. (REQ-012-066)
- Clear visual distinction for conversations with flags, interventions, or high message counts. (REQ-012-066)

**Notes**:

- This is the main entry screen for admin messaging - comprehensive overview of all conversations.
- Filter bar should be prominent and easy to use; filters persist across sessions.
- Show total conversation count and filtered count (e.g., "Showing 15 of 247 conversations"). (REQ-012-066)
- Visual hierarchy: flagged conversations more prominent than unflagged.
- Preset filter quick actions: "Flagged Only", "Intervened Today", "Unresolved Flags", "Last 24 Hours". (REQ-012-065)
- **Inquiry ID filtering**: Powerful for case investigation - shows all provider conversations for one inquiry side-by-side.
- Responsive design: filters collapse to sidebar on mobile; conversation list remains scrollable.
- Performance: Load first 20 conversations quickly; lazy load more on scroll.
- Badge tooltips: Hover over flags/badges to see flag type, reason, timestamp. (REQ-012-066)

---

#### Screen 6A: Message Thread Detail - Monitoring & Flagging (Admin)

**Purpose**: Default view for reviewing specific conversation with full message history, participant information, and flag management capabilities for admin monitoring and observation.

**Activated by**: Selecting a conversation from Screen 5 (Communication Monitoring Center)

**Layout Structure**: 3-panel layout for desktop/tablet (responsive for mobile)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Panel Location | Graph field |
|------------|------|----------|-------------|------------------|----------------|-------------|
| **LEFT PANEL: Conversation List** | | | | | | |
| Conversation list | list | Yes | Shows all conversations from Screen 5 with applied filters | Synchronized with Screen 5; same filtering applies | Left | no graph field (list of the rows below) |
| Patient/Provider names | text | Yes | Conversation participants in list | Read-only; displayed in list items | Left | ENT-patient.name, ENT-provider.name |
| Flag indicators | badges | N/A | Red (keyword) or orange (manual) badges | Visible on flagged conversations | Left | ENT-conversation.keyword_flags, ENT-conversation.manual_observation_flags |
| Last message preview | text | Yes | Preview of last message | Max 50 chars | Left | ENT-conversation.last_message_preview |
| Timestamp | text | Yes | Time of last message | Relative (e.g., "2h ago") | Left | ENT-conversation.last_message_at |
| Active indicator | highlight | Yes | Shows currently selected conversation | Highlighted background for selected conversation | Left | no graph field (control) |
| **CENTER PANEL: Message Thread** | | | | | | |
| Conversation header | group | Yes | Shows participants, inquiry/quote IDs, service types, timestamps | Read-only; at top of center panel | Center | ENT-conversation.inquiry_ids, ENT-conversation.quote_references, ENT-conversation.service_types, ENT-conversation.created_at |
| Patient name | text | Yes | Real patient name (admins see the unmasked name) | Read-only; in header | Center | ENT-patient.name |
| Provider name | text | Yes | Provider/clinic name | Read-only; in header | Center | ENT-provider.name |
| Message thread | scrollable panel | Yes | Full conversation history with all messages | Read-only; chronological order; main center content | Center | no graph field (list of the message rows below) |
| Message sender | indicator | Yes | Shows if patient, provider, admin or system sent message | Color-coded or icon-based per message | Center | ENT-message.sender |
| Message text | text | Yes | Full message content | Read-only; displayed per message | Center | ENT-message.text |
| Message attachments | links/thumbnails | No | Images, videos, PDFs attached to messages | Clickable to view/download; inline with messages | Center | ENT-message.attachments |
| Message timestamp | datetime | Yes | When message was sent | Displayed per message | Center | ENT-message.sent_at |
| Read receipts | indicator | Yes | Shows if message was read | Checkmark or "Read" indicator per message | Center | ENT-message.read_at |
| Call entry | indicator | N/A | System entry for a call: audio or video, start time, duration and outcome (answered, missed, declined or failed) | Read-only (REQ-012-032) | Center | ENT-message.call_type, ENT-message.call_started_at, ENT-message.call_duration_seconds, ENT-message.call_outcome |
| Admin badge | indicator | N/A | "Hairline Admin" badge on existing admin messages | Auto-displayed on past admin interventions | Center | ENT-message.admin_badge |
| **RIGHT PANEL: Conversation Info & Flag Management Tools** | | | | | | |
| Conversation metadata | group | Yes | Summary info | Read-only section at top (REQ-012-079) | Right | ENT-conversation.inquiry_ids, ENT-conversation.quote_references, ENT-conversation.service_types, ENT-conversation.created_at, ENT-conversation.message_count |
| Inquiry IDs | list | No | Associated inquiry references (may be multiple) | Clickable links to inquiries if available | Right | ENT-conversation.inquiry_ids |
| Quote IDs | list | No | Associated quote references (may be multiple) | Clickable links to quotes if available | Right | ENT-conversation.quote_references |
| Service types | list | Yes | Treatment/service categories | Comma-separated if multiple | Right | ENT-conversation.service_types |
| Conversation started | datetime | Yes | Timestamp when conversation created | Read-only | Right | ENT-conversation.created_at |
| Message count | number | Yes | Total messages in thread | Read-only; updates live | Right | ENT-conversation.message_count |
| Keyword flags panel | panel | No | All automatic keyword flags detected | Collapsible section; list with keyword, timestamp, context snippet | Right | ENT-conversation.keyword_flags, ENT-flag.context_snippet, ENT-flag.created_timestamp |
| Manual flags panel | panel | No | All admin observation flags | Collapsible section; list with flag type, admin user, timestamp, notes | Right | ENT-conversation.manual_observation_flags, ENT-flag.category, ENT-flag.admin_user, ENT-flag.created_timestamp, ENT-flag.internal_notes |
| Flag history | timeline | No | Chronological timeline of all flag events | Collapsible section; added, reviewed, resolved, escalated with admin names | Right | ENT-flag.status, ENT-flag.created_timestamp, ENT-flag.resolved_timestamp, ENT-flag.admin_user |
| Flag for Observation | button | No | Add manual observation flag | Prominent button; opens flag type dialog | Right | no graph field (control) |
| Flag type | select | Yes (when flagging) | Type of observation flag | Options: Off-Platform Risk / Potential Dispute / Quality Concern / Follow-Up Needed / Other | Right (in dialog) | ENT-flag.category |
| Flag notes | textarea | No | Internal admin notes about flag | Max 500 chars; NOT visible to users | Right (in dialog) | ENT-flag.internal_notes |
| Resolve Flag | button | No | Mark flag as resolved | Button next to each flag; confirmation required (REQ-012-073); disabled for a flag in escalated_to_intervention (REQ-012-085) | Right | no graph field (control) |
| Enable Emergency Intervention | button | No | Activate emergency intervention mode (Screen 6B) | Prominent button with warning styling; opens confirmation dialog; not available on a read-only conversation (REQ-012-018) or while another emergency intervention session is open on the conversation (REQ-012-085) | Right | no graph field (control) |
| Actions menu | dropdown | No | Additional admin actions | Future phase: Export conversation is deferred; no other actions in this menu | Right | no graph field (control) |

**Business Rules**:

- **Default read-only state**: Admin can review but NOT send messages in this mode. (REQ-012-069)
- Full conversation history displayed in chronological order; auto-scroll to latest message. (REQ-012-070)
- All flags (keyword and manual) displayed prominently in dedicated panels. (REQ-012-071)
- Flag history shows complete audit trail: who added, when, type, status changes. (REQ-012-071)
- Manual flagging available without leaving thread view; flag appears immediately and silently (no user notification). Exception: the provider's conversation screen (Screen 4) shows the flag indicator; the patient is still not notified. (REQ-012-072)
- Conversation header shows ALL inquiry/quote IDs if patient-provider pair has multiple treatments. (REQ-012-070)
- "Enable Emergency Intervention" button only visible to admins with intervention permissions. (REQ-012-074)
- All admin view actions logged with timestamp, admin user, and action type. (REQ-012-075)
- Future phase: Export conversation (full message history, attachments metadata, flag history, intervention logs) is deferred. (REQ-012-076)

**Notes**:

- **3-panel layout**: Left panel (conversation list from Screen 5), Center panel (message thread with conversation header), Right panel (conversation info & flag management tools).
- **Desktop/Tablet**: All 3 panels visible simultaneously; left panel width ~25%, center panel ~50%, right panel ~25%.
- **Mobile**: Single panel view with navigation; left panel (list) → center panel (messages) when conversation selected; right panel accessible via info/tools icon.
- **Left panel**: Synchronized with Screen 5; shows same filtered conversation list; selecting conversation updates center and right panels without full page reload.
- **Center panel**: Full message history in chronological order; auto-scrolls to latest message when conversation opens; read-only (no message composition in monitoring mode).
- **Right panel**: Always shows context for selected conversation; collapsible sections for flags (keyword flags, manual flags, flag history); action buttons at bottom.
- Back to Screen 5: Navigation breadcrumb or back button returns to Screen 5 with filters preserved. (REQ-012-078)
- Real-time updates: new messages appear immediately in center panel if conversation is open; left panel list updates with new message previews. (REQ-012-078)
- Attachment preview: inline thumbnails for images/videos in center panel; download links for PDFs.
- Flag management: Quick "Flag for Observation" button in right panel; detailed flag history timeline; resolve buttons next to each flag.
- Performance: Lazy load old messages if conversation has 100+ messages; left panel list uses virtualization for 100+ conversations.
- **Emergency intervention access**: "Enable Emergency Intervention" button prominent in right panel; clicking shows confirmation dialog explaining implications, then transitions to Screen 6B state. (REQ-012-080)
- Keyboard shortcuts: Esc to close thread view, ↑/↓ to navigate conversation list, F to flag, E to enable emergency mode (with confirmation). (REQ-012-078)

---

#### Screen 6B: Message Thread Detail - Emergency Intervention (Admin)

**Purpose**: Activated state allowing admin to actively intervene in critical situations by sending messages directly into the patient-provider conversation. ONLY for serious policy violations, urgent disputes, or patient safety emergencies.

**Activated by**: Clicking "Enable Emergency Intervention" button in Screen 6A and confirming action

**Layout Structure**: 3-panel layout maintained from Screen 6A (responsive for mobile)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Panel Location | Graph field |
|------------|------|----------|-------------|------------------|----------------|-------------|
| Emergency warning banner | alert | Yes | Prominent red/orange banner across top of all panels | Displays: "🚨 EMERGENCY INTERVENTION MODE - Both patient and provider will be notified of your message" | Top (spans all panels) | no graph field (control) |
| **LEFT PANEL: Conversation List** | | | | | | |
| Conversation list | list | Yes | Same conversation list from Screen 6A | Read-only in emergency mode; can switch conversations | Left | no graph field (list of the rows below) |
| Active indicator | highlight | Yes | Shows currently selected conversation | Highlighted background; locked during message composition | Left | no graph field (control) |
| **CENTER PANEL: Message Thread & Compose** | | | | | | |
| Conversation header | group | Yes | Same conversation header from Screen 6A | Shows participants, inquiry/quote IDs; read-only | Center (top) | ENT-patient.name, ENT-provider.name, ENT-conversation.inquiry_ids, ENT-conversation.quote_references |
| Message thread | scrollable panel | Yes | Full conversation history (same as 6A) | Read-only; chronological order; remains visible for context | Center (main) | no graph field (list of the message rows below) |
| Message sender | indicator | Yes | Shows if patient, provider, or admin sent | Same as 6A | Center | ENT-message.sender |
| Message text (history) | text | Yes | Historical message content | Read-only | Center | ENT-message.text |
| Message timestamp | datetime | Yes | When message was sent | Per message | Center | ENT-message.sent_at |
| Call entry | indicator | N/A | System entry for a call: audio or video, start time, duration and outcome (answered, missed, declined or failed) | Read-only (REQ-012-032) | Center | ENT-message.call_type, ENT-message.call_started_at, ENT-message.call_duration_seconds, ENT-message.call_outcome |
| Compose area separator | divider | Yes | Visual separator before compose area | Prominent line with "Admin Intervention Message" label | Center (divider) | no graph field (control) |
| Message text (admin) | textarea | Yes | Admin emergency intervention message to patient and provider | Max 2000 chars; clearly worded for both parties; fixed at bottom of center panel | Center (bottom) | ENT-message.text |
| Attachment (admin) | file upload | No | Optional admin attachment (emergency only) | Images: JPG/PNG max 5MB; PDF: max 10MB; Max 5 attachments per message (REQ-012-042) | Center (bottom) | ENT-message.attachments |
| Preview button | button | No | Preview how message will appear | Opens preview overlay in center panel | Center (bottom) | no graph field (control) |
| Send button | action | Yes | Send admin emergency message | Disabled until emergency reason selected and message text present; requires confirmation click | Center (bottom) | no graph field (control) |
| Cancel / Return to Monitoring | button | Yes | Exit emergency mode without sending | Returns to Screen 6A without sending intervention | Center (bottom) | no graph field (control) |
| **RIGHT PANEL: Intervention Controls & Context** | | | | | | |
| Conversation metadata | group | Yes | Same metadata from Screen 6A | Inquiry IDs, quote IDs, service types, timestamps | Right (top) | ENT-conversation.inquiry_ids, ENT-conversation.quote_references, ENT-conversation.service_types, ENT-conversation.created_at, ENT-conversation.message_count |
| Emergency reason | select | Yes | Mandatory reason for intervention | Options: Policy Violation / Urgent Dispute / Patient Safety; must be selected before sending; prominently displayed | Right (middle) | ENT-message.emergency_reason |
| Emergency justification | textarea | No | Internal notes explaining intervention decision | Max 500 chars (REQ-012-083) | Right (middle) | ENT-message.emergency_justification |
| All flags panels | collapsible | No | Keyword flags, manual flags, flag history remain visible | Same as Screen 6A; provide context for intervention decision | Right (middle) | ENT-conversation.keyword_flags, ENT-conversation.manual_observation_flags, ENT-flag.context_snippet, ENT-flag.category, ENT-flag.admin_user, ENT-flag.internal_notes, ENT-flag.status, ENT-flag.created_timestamp, ENT-flag.resolved_timestamp |
| Intervention checklist | panel | Yes | Pre-send checklist | Ensures: Reason selected, Message clear, Both parties addressed, Attachments valid (if any) | Right (bottom) | no graph field (control) |
| Warning reminder | alert | Yes | Persistent reminder in right panel | "This message will be sent to BOTH patient and provider" | Right (bottom) | no graph field (control) |

**Business Rules**:

- **Explicit activation required**: Admin must click "Enable Emergency Intervention" in Screen 6A and confirm action. (REQ-012-080)
- **Warning banner always visible**: Prominent alert that both parties will be notified. (REQ-012-081)
- See REQ-012-082.
- Emergency justification (internal notes) logged for compliance audit but NOT sent to users. (REQ-012-083)
- See REQ-012-014.
- Both patient and provider receive push/email notification of admin intervention. (REQ-012-007)
- Admin emergency message CANNOT be edited or deleted after sending. (REQ-012-084)
- System logs: timestamp, admin user, emergency reason, justification notes, full message content.
- Enabling intervention sets the conversation's active flags to escalated_to_intervention and sending marks them intervention_completed; cancelling without sending restores the flags and changes nothing. Only one emergency intervention session can be open per conversation at a time, and Resolve Flag is disabled for a flag in escalated_to_intervention. (REQ-012-085, REQ-012-109)
- After sending, system returns admin to Screen 6A (monitoring mode) with intervention visible in thread. (REQ-012-086)
- **Rare use**: monitoring target of under 5% of conversations (shown on Screen 5, blocks nothing); intervention should be last resort. (REQ-012-024)

**Notes**:

- **3-panel layout maintained**: Left panel (conversation list, read-only during composition), Center panel (message thread + compose area at bottom), Right panel (intervention controls & context).
- **Warning banner spans all panels**: Emergency warning banner at very top crosses all three panels for maximum visibility.
- **Desktop/Tablet**: All 3 panels visible simultaneously; same proportions as Screen 6A (~25% / 50% / 25%).
- **Mobile**: Center panel becomes full-screen with compose area; right panel accessible via "Intervention Controls" button; left panel minimized.
- **Left panel**: Conversation list remains visible but locked during message composition; admin can cancel to switch conversations if needed. (REQ-012-087)
- **Center panel**: Top shows full message history (read-only context); bottom shows compose area with clear separator labeled "Admin Intervention Message"; compose area sticky/fixed at bottom with send/cancel buttons.
- **Right panel**: Emergency reason selection at top (mandatory, prominently displayed); justification notes below; flags panels collapsible for context; intervention checklist at bottom ensures all requirements met before sending.
- **Visual emphasis on seriousness**: Red/orange warning banner across all panels, confirmation dialogs, explicit reason requirement, intervention checklist.
- Preview button opens overlay in center panel showing exactly how message will appear to users (with "Hairline Admin" badge). (REQ-012-087)
- Cancel button prominently available in both center (compose area) and right panels - admin can exit without sending if situation de-escalates. (REQ-012-087)
- Attachment option available for sending policy documents, compliance notices, or safety instructions. (REQ-012-042)
- Intervention message should be professional, authoritative, and clearly explain action/requirement to both parties. (REQ-012-088)
- Best practices guidance tooltip: "Address both parties, state reason clearly, provide specific action required, maintain professional tone." (REQ-012-088)
- Send button disabled until: (1) Emergency reason selected, (2) Message text entered, (3) Checklist items confirmed. (REQ-012-082)
- After sending: System transitions back to Screen 6A with intervention message visible in thread; both patient and provider notified immediately. (REQ-012-086, REQ-012-007)
- System tracks intervention success: an intervention counts as successful when no new flag is raised on that conversation in the 30 days after it (the post-intervention flag does not count); Screen 5 shows the intervention success rate, successful interventions divided by interventions older than 30 days, worked out when the screen is read. After sending, the system raises a system flag with category Follow-Up Needed for follow-up review unless the post-intervention flag switch on Screen 5 is off (default on). (REQ-012-089)

---

## Business Rules

### General Module Rules

- All conversations and message events (sent, delivered, read) are logged with timestamps and participants. (REQ-012-010)
- Message content size and attachment limits enforced to ensure reliable delivery and storage. (REQ-012-009)
- Timestamp display (the user's local timezone, admin UTC toggle) is stated once in the system PRD and applies to every screen of this module.
- See REQ-012-010 and REQ-012-023.
- Twilio (for audio/video calls), failure handling: Display connection error message; allow retry; fallback to text messaging if call cannot be established; the call entry records outcome failed. (REQ-012-033)
- Device push notification providers (for mobile alerts), integration: Use platform-standard push delivery; fallback to in-app badges and email where applicable. Failure handling: Queue retry; show in-app banners; notify user if delays persist. (REQ-012-034)
- Emergency intervention used for: serious policy violations, urgent disputes that providers cannot resolve, patient safety emergencies. (REQ-012-090)
- Providers are expected to maintain professional communication standards and not solicit off-platform contact. (REQ-012-093)
- Provider/Admin web apps accessed via modern browsers (latest 2 versions) with file upload capabilities.
- Client-side validation for file types and sizes before upload to prevent unnecessary uploads.
- Background upload for larger files with progress indication.
- Performance: Degrade gracefully on poor connectivity with retries and clear status; optimize video compression on mobile devices.
- Error handling: Retry on transient failures; clear feedback to user.

### Data & Privacy Rules

  Reference Principle II from constitution: Medical Data Privacy & Security

- Provider identities are visible to patients in messaging (patients chat directly with providers who have sent them quotes). (REQ-012-052)
- Patient identity masking until payment confirmation is stated once in the system PRD masking Rule; it applies to what the provider sees, and admins see the real patient name.
- Patient PII and media are protected; encryption in transit and at rest follows the encryption record in the system PRD.
- Message retention follows the system PRD, Platform-Wide Rules: One 10-year retention period; on account deletion the patient's messages and attachments are anonymised in place per FR-023 (REQ-023-044) and kept for the retention period, and admin emergency messages are kept. (REQ-012-020, REQ-012-100)
- Role-based access to conversations and the audit of that access are stated once in the system PRD (retired here); the reason is recorded with the emergency intervention message; the "intervention enabled" audit entry carries no reason and is written even when the session is cancelled. (REQ-012-101)
- See REQ-012-021.
- See REQ-012-023.
- GDPR and HIPAA-equivalent compliance, patient consent, and data residency are stated once in the system PRD (moved from this module).
- Encryption: Content and media encryption in transit and at rest follows the encryption record in the system PRD; media links protected.
- Authentication: Strong session controls; MFA is a planned mandatory control for Admin/Provider and will be enforced platform-wide once the shared MFA stack (FR-026 / FR-031) is delivered; until then enforce strong passwords, throttling, and re-authentication flows per policy.
- Authorization: Role-based access; least-privilege visibility to conversations.
- Authentication: Provider-authenticated sessions; access scoped to own patients.
- Audit trail: Immutable logs of access and message events retained per the system PRD, Platform-Wide Rules: One 10-year retention period; admin interventions specially flagged. (REQ-012-102)
- Threat mitigation: Abuse prevention on messaging and media uploads; keyword moderation and rate controls; emergency intervention tracking.

### Admin Editability Rules

  Reference Constitution: Medical Data Privacy & Security (Core Principles II) and Data Integrity & Audit Trail (Core Principles VI)

**Editable by Admin** (REQ-012-105):

- Keyword/phrase flags that trigger moderation or escalation cues, and the post-intervention flag switch (default on), in the Moderation settings group on Screen 5; the keyword list starts empty and the admin team fills it before go-live.
- Notification preferences and quiet hours policy are configured in FR-030 (moved from this module).

**Fixed in Codebase (Not Editable)** (REQ-012-106):

- Cryptographic standards and security controls.
- Read receipt semantics and audit logging requirements.
- The retention period (system PRD, Platform-Wide Rules: One 10-year retention period).
- Attachment type and size limits (REQ-012-009).
- Maximum number of attachments per message (REQ-012-009).
- Message character limits (2000 chars). (REQ-012-035)
- Emergency intervention reasons: the fixed list Policy Violation / Urgent Dispute / Patient Safety (REQ-012-013).

**Configurable with Restrictions** (REQ-012-107):

- Escalation routing rules (allowed destinations/roles only).
- Future phase: Conversation export controls (admin conversation export is deferred).
- Emergency intervention permissions (restricted to authorized admin roles only).

### Payment & Billing Rules *(if applicable)*

Not applicable to messaging scope; no payment flows in this module.

---

## Dependencies

- P-01 Auth & Profile Management: identity and access control for participants (REQ-001-011, REQ-009-002).
- FR-003 Inquiry Submission & Distribution: defines patient anonymization/masking rules and pseudonymous identifiers used across patient/provider views.
- FR-004 Quote Submission & Management: enable patient-provider chat only when provider has sent quote to patient.
- FR-007 Payment Processing: lift patient anonymization when payment is confirmed per FR-003 (REQ-006-002, REQ-007-020, REQ-006-008).
- S-03 Notification Service: deliver real-time alerts for new messages and admin emergency interventions; events catalogued in FR-030 (REQ-030-061, REQ-020-028, REQ-020-033).
- S-05 Media Storage Service: secure storage and retrieval of attachments (REQ-002-024).
- FR-021 Multi-Language & Localization: owns the machine translation of messages between patient and clinic and the platform-wide translation switch (REQ-012-108, REQ-021-119).
- FR-023: anonymises the patient's messages and attachments in place on account deletion (REQ-023-044).

---

## User Scenarios & Testing

### User Story 1 - Patient views inbox and manages conversations (Priority: P1)

A patient receives quotes from 3 providers, opens their Messages/Inbox (Screen 1), sees 3 conversations with unread badges, filters by "Unread", searches for a specific provider by name, and taps a conversation to open the chat.

Why this priority: Core navigation pattern; patients need to manage multiple provider conversations efficiently.

Independent Test: Create 3 provider quotes; verify conversations appear in patient inbox; test filter by unread; test search by provider name; verify conversation opens on tap.

Acceptance Scenarios:

1. Given a provider submits a quote, when the quote is submitted, then a new conversation appears in patient's Messages/Inbox (Screen 1) with provider name, unread badge, and timestamp.
2. Given patient has 5 conversations with 2 unread, when patient selects "Unread" filter, then only 2 unread conversations are displayed.
3. Given patient has multiple conversations, when patient types provider name in search, then conversation list filters to matching providers in real-time.
4. Given patient taps a conversation in inbox, when tapped, then full chat view (Screen 2) opens showing conversation history.
5. Given patient has unread messages, when patient opens conversation and reads messages, then unread badge clears in inbox view.

---

### User Story 2 - Patient asks provider about quote (Priority: P1)

A patient receives multiple quotes, opens their Messages/Inbox, sees conversations with providers who sent quotes, opens a specific conversation, has questions about one provider's package options and procedure details, sends a message to the provider, and receives clarification within 24 hours.

Why this priority: Core to quote acceptance and booking conversion; helps patients make informed decisions.

Independent Test: Provider submits quote; verify conversation auto-created in both inboxes; patient opens from inbox; test patient sends message; verify provider receives, responds, and patient sees reply with read receipts and notifications.

Acceptance Scenarios:

1. Given a logged-in patient opens their Messages/Inbox and selects a conversation, when they send a valid text message with questions, then the message appears in the thread with sending and sent states in under 1 second.
2. Given provider is notified, when provider opens conversation from their Messages/Inbox and replies within 24 hours, then the patient receives notification and sees unread badge in inbox.
3. Given patient opens conversation with new message, when the message is viewed, then the provider sees a read receipt within 2 seconds and patient's inbox unread badge clears.

---

### User Story 3 - Admin flags conversation for observation (Priority: P1)

Admin reviews conversations, notices a provider using borderline language that could escalate to off-platform solicitation, manually flags conversation as "Off-Platform Risk" for closer monitoring without alerting the parties, and continues to observe.

Why this priority: Proactive monitoring prevents policy violations before they require intervention; enables early detection without disrupting user experience.

Independent Test: Admin reviews conversation with borderline language; selects "Flag for Observation"; chooses "Off-Platform Risk" flag type; adds internal note; verify conversation marked with orange flag in dashboard; verify patient/provider receive no notification; verify flag appears in "Flagged" filter.

Acceptance Scenarios:

1. Given admin is viewing a conversation, when admin selects "Flag for Observation" action, then system prompts for flag type selection.
2. Given admin selects flag type "Off-Platform Risk" and adds note "Provider mentioned 'better pricing outside app'", when admin confirms, then conversation is marked with orange flag badge in admin dashboard.
3. Given conversation is flagged, when admin views conversation list with "Flagged" filter, then flagged conversation appears with flag type indicator.
4. Given conversation is flagged, when admin opens conversation, then flag history panel shows flag type, timestamp, admin user, and internal notes.
5. Given conversation is flagged for observation, when patient or provider opens their messages, then neither party is notified and the patient sees NO indication of the flag; the provider's chat screen (Screen 4) shows the flag indicator.

---

### User Story 4 - Admin emergency intervention for policy violation (Priority: P1)

Admin detects serious off-platform solicitation attempt via keyword flag; admin enables emergency intervention mode, selects reason, and sends policy enforcement message to both patient and provider.

Why this priority: Platform integrity and compliance; prevents revenue loss; protects patients from unauthorized transactions.

Independent Test: Provider sends message with flagged keyword (e.g., "contact me on WhatsApp"); admin receives flag, enables emergency mode, selects "Policy Violation" reason, sends intervention; verify both parties receive admin message with badge.

Acceptance Scenarios:

1. Given a provider sends a message containing flagged keyword, when the message is sent, then the system automatically flags the conversation in admin dashboard with keyword badge.
2. Given admin identifies serious policy violation, when admin enables emergency intervention mode and selects "Policy Violation" as reason, then admin can compose and send message.
3. Given admin sends emergency intervention message, when the message is sent, then both patient and provider receive notification and see message with "Hairline Admin" badge.
4. Given admin emergency intervention occurred, when viewing audit log, then intervention is logged with timestamp, admin user, emergency reason ("Policy Violation"), and full message content.

---

### User Story 5 - Provider responds with detailed clarification (Priority: P1)

A provider receives patient question about package options and graft count estimation, attaches facility photos and treatment plan diagram, and provides detailed explanation within 24 hours.

Why this priority: Enhances provider-patient communication; increases quote acceptance rate; builds trust.

Independent Test: Provider receives patient message with questions; attaches media; sends detailed response; verify patient receives with attachments and notifications.

Acceptance Scenarios:

1. Given a provider viewing patient conversation, when they compose a response and attach images (facility photos, treatment plans), then the message is sent with attachments within 2 seconds.
2. Given patient receives provider response, when patient opens the message, then attachments are viewable with thumbnails and full-size preview.
3. Given provider response includes multiple attachments, when patient views conversation, then all attachments display inline with proper formatting.

### Edge Cases

- **Excessive attachments**: Enforce 5 attachments max per message; display clear error "Maximum 5 attachments per message" if exceeded. (REQ-012-040)
- **Oversized attachments**: Block upload and show the specific error for the type; the exact messages are those in Alternative Flow B1. (REQ-012-040)
- **Unsupported file types**: Block upload and show "Only JPG/PNG images (max 5MB), MP4 videos (max 10MB), and PDF files (max 10MB) are allowed." (REQ-012-040)
- **File fails the malware scan**: The file is refused with a specific message; the message can still be sent without it. (REQ-012-044)
- **No provider response within 48 hours**: The clock starts at the patient's oldest unanswered message and stops at any provider reply, counted in calendar hours; it also stops while the conversation is read-only and starts again from the next unanswered patient message when the conversation reopens. At 48 hours the system reminds the provider (once per unanswered stretch); if there is still no reply at 72 hours, the system itself creates a flag of type system with category Follow-Up Needed on the conversation (no admin is named on it) and sends additional provider reminders via notifications. The follow-up queue is Screen 5 filtered by the Follow-Up Needed category. A provider reply closes the system flag automatically (closed by the system, no admin action), after which the conversation can be Resolved. Admin messaging remains emergency-only. (REQ-012-098)
- **Account deletion request with open conversations**: The patient's messages and attachments are anonymised in place per FR-023 and kept for the retention period; admin emergency messages are kept; the conversation becomes read-only. (REQ-012-100, REQ-012-018)
- **Simultaneous sends**: Maintain message ordering and idempotency safeguards; admin emergency messages sorted chronologically with patient/provider messages. (REQ-012-104)
- **Provider persistent off-platform solicitation**: Admin intervenes with warning via emergency mode; repeated violations may trigger provider review/suspension. (REQ-012-091)
- **Patient safety emergency during conversation**: Admin can intervene immediately using emergency mode to provide guidance or escalate to the on-call Admin. (REQ-012-092)
- **Admin intervention visibility**: Admin emergency messages visible to both patient and provider; cannot be deleted or edited by any party. (REQ-012-084)
- **Manual flag escalation**: Conversation manually flagged for observation escalates to emergency intervention when situation worsens; flag status updated to "Intervention Completed" after intervention. (REQ-012-085)
- **Multiple flags on same conversation**: System handles multiple manual flags (e.g., flagged as "Off-Platform Risk", later flagged as "Potential Dispute"); flag history shows chronological sequence. (REQ-012-096)
- **Flag without action**: Flagged conversations where concern doesn't materialize; admin can mark flag as "Resolved - No Action Needed" without intervention. (REQ-012-097)
- **Multiple conversations per inquiry**: One patient inquiry can generate multiple quotes from different providers, resulting in multiple conversations; admin filters by inquiry ID to view all related conversations for comprehensive case review (e.g., patient disputes pricing across multiple quotes). (REQ-012-068)

---

## Functional Requirements Summary

### Core Requirements

- **REQ-012-001**: System MUST automatically create a new conversation between patient and provider when provider submits their **first** quote for patient inquiry; subsequent quotes from same provider to same patient MUST add inquiry/quote IDs to existing conversation (one conversation per patient-provider pair). The provider side of the pair is the clinic: every clinic team member with messaging permission reads and replies in the same conversation. The unread count is kept once per clinic: when one team member opens the conversation it counts as read for the whole clinic.
- **REQ-012-002**: System MUST provide a Messages Inbox view for patients showing all conversations, sortable by latest activity, provider name, or date created. Search and filtering of the inbox is stated once in REQ-022-070 (first release).
- **REQ-012-003**: System MUST provide a Messages popup/submenu in header navigation for providers showing recent conversations (max 10) with unread counts and quick access to patient chats.
- **REQ-012-004**: System MUST provide a Communication Monitoring Center for admins as the message list of all conversations. Its filters, how they combine, and that they are remembered are stated once in REQ-022-122.
- **REQ-012-005**: System MUST provide a detailed Message Thread View for admins with two states: Screen 6A (default monitoring/flagging state with read-only access) and Screen 6B (activated emergency intervention state with message composition), accessible when conversation is selected from monitoring center.
- **REQ-012-006**: System MUST enable in-app messaging for Patient ↔ Provider with text and media, accessible ONLY through dedicated Messages/Inbox screens (chat is not embedded in quote detail screens; a quote screen may link to the conversation in the inbox, REQ-005-015).
- **REQ-012-007**: System MUST deliver real-time notifications for new messages to intended recipients (patients, providers, and both parties when admin intervenes); update unread badges in inbox views and header popup menus. The notification events are defined in the FR-030 event catalogue. The intervention notice to both parties and the admin keyword alert cannot be switched off or held; the other chat notices follow the user's notification settings.
- **REQ-012-008**: Users MUST be able to view complete conversation history with timestamps and read receipts.
- **REQ-012-009**: System MUST enforce attachment type and size limits (Images: JPG/PNG max 5MB; Video: MP4 max 10MB; PDF: max 10MB; max 5 attachments per message) and provide specific user feedback on violations. The checks and the malware scan run on every attachment from a patient, provider or admin; a file that fails is refused with a specific message and the message can still be sent without it.
- **REQ-012-010**: System MUST log message lifecycle events (sent, delivered, read) and these audit events: attachment sent, keyword flag raised, manual flag raised, system flag raised, flag resolved, emergency intervention enabled, the emergency intervention message, call entry, and moderation setting changed.
- **REQ-012-011**: System MUST allow admins to manually flag conversations for observation with flag type selection (Off-Platform Risk / Potential Dispute / Quality Concern / Follow-Up Needed / Other) and optional internal notes.
- **REQ-012-012**: System MUST distinguish between automatic keyword flags (red) and manual observation flags (orange) in admin monitoring center and thread detail view; flagging must NOT notify patient or provider. Exception for the provider's view: the provider's conversation screen still shows the flag indicator for an open flag of any type (the patient is still not notified).
- **REQ-012-013**: System MUST allow admins to send messages in patient-provider conversations ONLY for emergency situations with mandatory reason tracking (Policy Violation / Urgent Dispute / Patient Safety).
- **REQ-012-014**: System MUST clearly identify admin messages with "Hairline Admin" badge visible to both patient and provider.
- **REQ-012-108**: Patient and provider chat screens MUST offer an on/off switch for machine translation of messages for the reader. The switch is shown and works only while the platform-wide translation switch (FR-021) is on. The translation behavior itself is owned by FR-021; this module owns only the switch in the conversation thread.
- **REQ-012-109**: Conversation status MUST be calculated from the conversation's flags, with no manual control: Escalated while a flag is escalated_to_intervention (the admin has enabled emergency intervention on Screen 6B and has not yet sent or cancelled); Resolved only when the conversation has at least one flag and all its flags are closed (resolved or intervention_completed); otherwise Active, which covers a conversation with no flag and one with any open flag that is not under intervention. Enabling emergency intervention is the step that sets the flags to escalated_to_intervention; cancelling Screen 6B puts the flags back as they were. While an emergency intervention session is open the conversation shows Escalated whether or not it has a flag; with no flag, the audit entries are the record of the session.

### Data Requirements

- **REQ-012-015**: System MUST maintain conversations per patient-provider pair with searchable metadata (patient ID, provider ID, inquiry ID, quote reference, status, unread_count, keyword flags, manual observation flags, admin_intervened flag, emergency_reason, last_message_at).
- **REQ-012-016**: System MUST store flag history for each conversation including flag type, timestamp, admin user, status (active / resolved / escalated_to_intervention / intervention_completed; "Resolved - No Action Needed" shows as resolved), and internal notes.
- **REQ-012-017**: System MUST store attachments securely with links to their parent messages, access controls, and metadata (file type, size, upload timestamp, thumbnail URLs for images/videos).

### Security & Privacy Requirements

- **REQ-012-018**: System MUST enable patient-provider messaging only when provider has sent a quote to patient. The conversation is open while the pair has a live quote, booking or aftercare; it becomes read-only (history kept for both parties, nobody can send, admins can still view it) when the provider is suspended or deactivated, the patient's account is deleted, or nothing live is left between the pair, and it opens again when the same provider sends a new quote. Read-only is derived from those conditions and is not a stored conversation status. On a read-only conversation the composer, attach control and call buttons are disabled with a banner giving the reason, and Enable Emergency Intervention is not available.
- **REQ-012-019**: Encryption of message content and media in transit and at rest follows the encryption record in the system PRD. The role-based access part is retired and is covered by the one system-PRD Rule on role-based, audited access.
- **REQ-012-020**: System MUST retain messages and attachments as set by the system PRD, Platform-Wide Rules: One 10-year retention period.
- **REQ-012-021**: Admin MUST have monitoring access to all patient-provider conversations with manual flagging capability and EMERGENCY-ONLY intervention capability.
- **REQ-012-022**: Retired. Patient anonymization until payment is stated once in the system PRD masking Rule. Providers see the masked form; admins see the real patient name.
- **REQ-012-023**: System MUST log all admin actions (manual flags, flag status changes, enabling emergency intervention, emergency interventions, moderation setting changes) with timestamp, admin user, reason/notes, and action type for compliance audit.
- **REQ-012-024**: System MUST restrict admin intervention to authorized admin roles only; Screen 5 shows the intervention rate (interventions in the calendar month divided by conversations with at least one message in that month; call entries are not messages) against a monitoring target of under 5%, which blocks nothing; manual observation flags can be used more liberally for proactive monitoring.

### Integration Requirements

- **REQ-012-025**: System MUST integrate with Quote Management (FR-004) to automatically create or update conversation when quote is submitted (create new if first quote from provider to patient; add quote/inquiry ID to existing if subsequent); conversation must reference all inquiry IDs (array) for admin filtering and case tracking; conversation appears or updates in both inboxes immediately.
- **REQ-012-026**: Manual observation flags MUST NOT trigger notifications. Delivery of message-event alerts and unread-badge updates follows the notification-service Rule in FR-020 (REQ-020-028), except that the intervention notice to both parties and the admin keyword alert are always delivered (REQ-012-007).
- **REQ-012-027**: System MUST integrate with Media Storage Service (S-05) for attachments with secure retrieval.
- **REQ-012-028**: System MUST integrate with Payment Processing (FR-007) to lift patient anonymization upon payment confirmation. Until then, on the provider screens the sender label, avatar and search use the masked identifier and View patient profile is hidden.

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-11-22 | 2.14 | Requirements graph programme baseline: PRD compressed to the checklist structure (each rule stated once, field rows tagged with graph field ids, dropped classes removed). No rule changes. Earlier history (v1.0 to v2.13) is in `archived/prd-baseline-2026-11-08/` and in git history. | AI |
| 2026-11-23 | 2.15 | FR-005 r1 logic review, finding N14 and the owner ruling of 2026-11-23 (the Message Provider button is kept): REQ-012-006 and REQ-012-029 say chat is not embedded in quote detail screens and that a quote screen may link to the conversation in the inbox (REQ-005-015). | Product Owner / Documentation |
| 2026-11-24 | 2.16 | FR-012 logic review: conversation status precedence and the step that escalates flags (REQ-012-109, REQ-012-085); intervention success is 30 days without a new flag and the post-intervention flag uses the new system flag type (REQ-012-089); the under 5% rate is a monitoring target shown on Screen 5 (REQ-012-024); the 48-hour clock, the system flag at 72 hours and the Follow-Up Needed queue on Screen 5 (REQ-012-098); intervention notice and keyword alert cannot be held (REQ-012-007); translation switch follows the FR-021 platform switch (REQ-012-108); provider screens keep the masked identifier, placeholder avatar and hidden profile link until payment (REQ-012-028, REQ-012-060, REQ-012-061); account deletion anonymises messages and attachments in place per FR-023 (REQ-012-100, REQ-012-020); conversation lifecycle and read-only state (REQ-012-018); one clinic-level conversation per pair (REQ-012-001); emergency reasons are a fixed list and a Moderation settings group is added on Screen 5 (REQ-012-105, REQ-012-106); attachment checks and malware scan for every sender (REQ-012-009, REQ-012-040, REQ-012-044); calls leave a system entry and are not recorded (REQ-012-032, new flow A4); audit event types and the reason recorded at intervention enable (REQ-012-010, REQ-012-023, REQ-012-101); dead admin-patient communications reference removed (REQ-012-064); medical team replaced by the on-call Admin (REQ-012-092). | Product Owner / Documentation |
| 2026-11-24 | 2.17 | FR-012 logic review, second pass: the intervention notice and keyword alert are always delivered (REQ-012-026); the intervention reason is recorded with the emergency message and the enabled entry carries none (REQ-012-101); an open intervention session shows Escalated with or without a flag (REQ-012-109); a provider reply closes the system flag, the 48-hour reminder is sent once per unanswered stretch and the response clock stops while the conversation is read-only (REQ-012-098); the flag indicator on Screen 4 covers an open flag of any type; Screen 5 shows an intervention success rate (REQ-012-089); read-only conversations disable the composer, attach control, call buttons and Enable Emergency Intervention (REQ-012-018); call entries get stored fields and a failed outcome and do not count as unread, preview or monthly-denominator messages (REQ-012-032, REQ-012-033); Save control, audit event, empty starting keyword list for the moderation settings (REQ-012-010, REQ-012-023, REQ-012-105); clinic team members see a colleague's name, one unread count per clinic (REQ-012-001, REQ-012-060, REQ-012-055); Resolve Flag disabled under intervention and one session per conversation (REQ-012-085); audit export removed from retention (REQ-012-020); masking link to the provider list (REQ-012-028). | Product Owner / Documentation |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | TBD | 2025-12-22 | ✅ Verified & Approved |
| Technical Lead | TBD | 2025-12-22 | ✅ Verified & Approved |
| Stakeholder | TBD | 2025-12-22 | ✅ Verified & Approved |

---

**Template Version**: 2.0.0 (Constitution-Compliant)  
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Governance → PRD Standards & Requirements (NON-NEGOTIABLE)  
**Based on**: FR-011 Aftercare & Recovery Management PRD  
**Last Updated**: 2026-11-24
