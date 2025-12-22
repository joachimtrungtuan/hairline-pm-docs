# Product Requirements Document: Messaging & Communication

**Module**: P-06: Communication | PR-06: Communication | A-10: Communication Monitoring & Support  
**Feature Branch**: `fr012-secure-messaging`  
**Created**: 2025-11-11  
**Status**: ✅ Verified & Approved  
**Source**: FR-012 from local-docs/project-requirements/system-prd.md; Transcriptions (HairlineApp-Part1/Part2, Hairline-AdminPlatform-Part1/Part2)

---

## Executive Summary

Enable secure, auditable, real-time messaging between patients and providers across the Hairline platform to support quote clarification, procedure coordination, and patient care. Patients can communicate directly with providers throughout their journey from quote review through post-procedure phases. Admins monitor all conversations with keyword flagging and can intervene ONLY in emergency situations (serious policy violations, urgent disputes, patient safety emergencies). The module supports text and media messages, read receipts, conversation history, and real-time notifications, improving response times, patient reassurance, provider communication efficiency, and operational transparency while meeting medical data privacy obligations.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-06)**: In-app chat with providers for quote questions, procedure clarifications, and coordination; notifications for new messages; view conversation history; send text and media.
- **Provider Platform (PR-06)**: Direct messaging with patients for quote clarification, procedure coordination, and post-booking questions; view conversation history; send text and media responses.
- **Admin Platform (A-10)**: Communication monitoring center for oversight, keyword flagging, and compliance logging; read-only monitoring with emergency-only intervention capability for critical situations (serious policy violations, urgent disputes, patient safety emergencies); can request 3D scans or schedule reviews.
- **Shared Services (S-03, S-05)**: Notification Service for push/email alerts; Media Storage Service for secure handling of images/videos attached to messages.

### Multi-Tenant Breakdown

**Patient Platform (P-06)**:

- View Messages Inbox with all provider conversations; filter by read/unread status; search by provider name or message content; sort by latest activity or date.
- See conversation previews with last message, unread counts, and timestamps; real-time updates.
- Open individual conversations to view full chat history with provider.
- Compose and send messages to providers (quote clarification, procedure questions, coordination).
- Attach media to messages: Images (JPG/PNG max 5MB), Video (MP4 max 10MB), PDF (max 10MB); max 5 attachments per message.
- View thumbnails and playback inline for images/videos; download PDFs.
- See read receipts and timestamps per message.
- Receive real-time notifications for new provider messages; badge counts for unread in inbox and app navigation.
- Chat available from quote received through post-procedure phases.

**Provider Platform (PR-06)**:

- Access Messages popup/submenu from header navigation showing recent patient conversations with unread counts.
- Quick view of most recent 10 conversations in popup; "View All" for full list.
- Send and receive messages with patients for quote-related questions and procedure coordination.
- View conversation history per patient with timestamps and read receipts.
- Attach media to responses: Images (JPG/PNG max 5MB) for before/after photos and facility images, Video (MP4 max 10MB) for procedure demonstrations, PDF (max 10MB) for treatment plans; max 5 attachments per message.
- Receive notifications for new patient messages; unread badge on header messages icon.
- Conversations visible for patients who have received quotes from this provider.

**Admin Platform (A-10)**:

- Communication Monitoring Center as primary message list: monitor all patient ↔ provider conversations (and any admin-patient communications) with read-only access (default).
- Comprehensive filtering and search: by patient, provider, service type, quote ID, inquiry ID, date range, keyword flags, manual observation flags, intervention status; all filters applied simultaneously.
- Conversation list with preview, participants, last message timestamp, flag indicators, inquiry reference.
- Automatic keyword flagging system to detect off-platform solicitation or policy violations (red flags).
- **Manual flagging for observation**: Admin can flag conversations for closer monitoring without notifying users (orange flags); flag types: Off-Platform Risk, Potential Dispute, Quality Concern, Follow-Up Needed, Other.
- Flag history tracking: view all flag events, status changes, and admin notes for each conversation.
- Select conversation to open detailed Message Thread View for full conversation history, participant info, flag management, and actions.
- **Emergency intervention capability**: Admin can send messages ONLY in critical situations (serious policy violations, urgent disputes, patient safety emergencies).
- Intervention actions: flag for observation, resolve flags, export conversation logs (with flag history), request 3D scan, schedule review.
- Configure moderation rules and automatic keyword flags; maintain compliance audit trail.
- Admin emergency messages clearly identified with "Hairline Admin" badge; logged with mandatory reason.

**Shared Services (S-03, S-05)**:

- S-03 Notification Service to deliver timely user alerts (push/email as configured).
- S-05 Media Storage for secure storage and retrieval of attachments; virus/malware scanning pipeline.

### Communication Structure

**In Scope**:

- Patient ↔ Provider in-app messaging (quote questions, procedure clarifications, post-booking coordination).
- Text and media messages with attachments: Images (JPG/PNG max 5MB), Video (MP4 max 10MB), PDF (max 10MB); max 5 attachments per message.
- Media thumbnails and inline playback for images and videos.
- Real-time notifications, read receipts, conversation history, and compliance logging.
- Admin monitoring with keyword flagging for compliance and policy enforcement.
- **Emergency-only admin intervention** for critical situations (estimated <5% of conversations).
- Conversation history accessible from quote received through post-procedure phases.

**Out of Scope**:

- Live video calls (can be scheduled/triggered but delivered by separate video consultation module).
- SMS channel management (handled by S-03 Notification Service configuration; **SMS as a transport for secure messaging is not part of MVP and will only be available if/when S-03 adds SMS support in a later phase**).
- Routine admin participation in conversations (admin intervention is emergency-only, not standard practice).
- Patient ↔ Hairline Support general help (may be added in future release; currently handled outside messaging module).
- Patient ↔ Aftercare Team specialized support (may be added in future release; currently handled outside messaging module).

### Entry Points

**Automatic Chat Creation**: When a provider submits their **first quote** for a patient inquiry, the system automatically creates a new chat conversation between that patient and provider. The conversation appears immediately in both parties' message inboxes. If the same patient-provider pair later has additional inquiries/quotes, they continue using the **same unified conversation** (one conversation per patient-provider pair, regardless of number of quotes).

**Patient Platform**: Patients access their Messages/Inbox screen (Screen 1) from the main navigation in the mobile app. The inbox displays all conversations with providers who have sent quotes, with filtering and search capabilities. Patients tap a conversation to open the full chat view (Screen 2). Chat is NOT accessible from quote detail screens—only from the dedicated inbox. Conversations remain accessible from quote received through post-procedure phases.

**Provider Platform**: Providers access patient conversations through a Messages popup/submenu in the header navigation (Screen 3), showing recent conversations with unread counts. The popup provides quick access to recent messages; tapping a conversation opens the full chat view (Screen 4). New conversations appear when providers submit quotes. Chat is NOT accessible from quote detail or inquiry screens—only from the dedicated messages list.

**Admin Platform**: Admins access the Communication Monitoring Center from the Admin platform navigation (Screen 5), which serves as the comprehensive message list monitoring all patient-provider conversations (and any admin-patient communications). The center includes advanced filtering by patient, provider, service, quote/inquiry ID, date range, flags, and intervention status. Selecting a conversation opens the detailed Message Thread View (Screen 6A) for review and flagging; admins can activate Emergency Intervention mode (Screen 6B) if critical situation requires direct messaging.

**Notifications**: Push/email notifications deep-link users directly into the specific conversation in their inbox. Keyword flags alert admins and deep-link to flagged conversations for review.

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

- **Trigger**: Patient or provider includes attachment (images, videos, or PDFs)
- **Steps**:
  1. System validates file type (JPG/PNG, MP4, or PDF) and size (images max 5MB, video max 10MB, PDF max 10MB).
  2. System validates attachment count (max 5 per message).
  3. If valid, system stores media securely and links it to the message; generates thumbnails for images/videos.
  4. If invalid, system displays specific error message and blocks upload.
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
  2. Admin clicks "Enable Emergency Intervention" button and confirms action; system activates Screen 6B (Emergency Intervention Mode).
  3. Screen 6B displays prominent warning banner: "🚨 EMERGENCY INTERVENTION MODE - Both patient and provider will be notified".
  4. Admin selects mandatory emergency reason (Policy Violation / Urgent Dispute / Patient Safety) and optionally adds internal justification notes.
  5. Admin reviews full conversation context and flag history (still visible in Screen 6B).
  6. Admin composes emergency intervention message clearly addressing both parties (e.g., policy enforcement, dispute mediation, safety guidance).
  7. Admin reviews preview and clicks Send; both patient and provider receive immediate notification.
  8. System marks message with "Hairline Admin" badge in conversation thread (visible to all parties).
  9. System logs emergency intervention with timestamp, admin user, emergency reason, justification notes, and full message content.
  10. If conversation was previously flagged, system updates flag status to "Intervention Completed".
  11. System returns admin to Screen 6A with intervention message visible in thread.
- **Outcome**: Emergency situation addressed; policy enforced; patient/provider receive authoritative guidance; intervention logged for audit and compliance review; conversation state updated.

**B1: Invalid Content**:

- **Trigger**: Attachment exceeds limits or unsupported type
- **Steps**:
  1. System validates attachment before upload.
  2. If invalid, system blocks upload and displays specific error:
     - "Image must be JPG or PNG format, max 5MB"
     - "Video must be MP4 format, max 10MB"
     - "PDF must be max 10MB"
     - "Maximum 5 attachments per message"
  3. User can retry with valid content.
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

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Search | text | No | Search conversations by provider name, message content | Min 2 chars |
| Filter by Status | select | No | Filter conversations by read/unread status | Options: All / Unread / Read |
| Sort by | select | No | Sort conversations | Options: Latest Activity (default) / Provider Name / Date Created |
| Conversation list | list | Yes | Shows all patient-provider conversations with preview | Paginated; 20 per page |
| Provider avatar | image | Yes | Provider profile picture or placeholder | Read-only; displayed in list |
| Provider name | text | Yes | Provider name and clinic | Read-only; displayed in list |
| Last message preview | text | Yes | Preview of last message (truncated) | Max 100 chars; shows "You: " prefix if patient sent |
| Unread badge | indicator | N/A | Shows unread message count | Red badge with count; hidden if 0 |
| Timestamp | text | Yes | Time of last message | Relative (e.g., "2h ago") or absolute (e.g., "Dec 19") |
| Admin intervention indicator | badge | N/A | Shows if admin has intervened in conversation | Orange "Admin" badge; only visible if admin message exists |

**Business Rules**:

- Conversations automatically created when provider sends their **first** quote; appear in inbox immediately.
- **One conversation per provider**: If a patient receives multiple quotes from the same provider (different inquiries/treatments), they all appear in ONE unified conversation - patient sees only one entry for that provider in inbox.
- Conversations sorted by latest activity by default (most recent at top).
- Unread count badge updates in real-time when new messages arrive.
- Tapping a conversation opens the full chat view (Screen 2).
- Search searches provider name and message content; results update as user types.
- Empty state message shown when no conversations exist: "No messages yet. When a provider sends you a quote, a conversation will start here."
- Pull-to-refresh to sync latest messages.
- Archived conversations hidden by default (future feature).

**Notes**:

- Display clear visual distinction between read and unread conversations (bold text for unread).
- Show typing indicator in conversation preview if provider is actively typing.
- Long-press on conversation for quick actions: Mark as Read/Unread, Archive (future).
- Smooth scroll performance even with 50+ conversations.
- Skeleton loading state while fetching conversation list.

---

#### Screen 2: Patient ↔ Provider Chat (Patient)

**Purpose**: Allow patients to message providers with quote questions, procedure clarifications, and coordination questions; receive timely responses.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Message text | text | Yes | Core message body | Max 2000 chars, no prohibited terms |
| Attachment | image/video/pdf | No | Optional media to support the message | Images: JPG/PNG max 5MB; Video: MP4 max 10MB; PDF: max 10MB; Max 5 attachments per message |
| Provider name | display | Yes | Shows provider name and clinic | Read-only; contextual to conversation |
| Send button | action | Yes | Submits message | Disabled until text or attachment present |
| Read status | indicator | N/A | Shows if message was read by provider | Auto-updated in real time |

**Business Rules**:

- Show typing/sending states and error states; retry control available for failed sends.
- Submit disabled until message text or attachment is provided.
- Display timestamps and read receipts per message.
- Patient sees conversation only with providers who have sent them quotes.
- **One conversation per patient-provider pair**: If same provider sends multiple quotes (different inquiries/treatments), all discussions happen in the same unified conversation.
- Chat is ONLY accessible from the Messages/Inbox screen, NOT from quote detail screens.
- New conversation automatically created when provider submits their **first** quote; subsequent quotes from same provider use existing conversation.
- Conversation accessible from quote received through post-procedure phases across all treatments with that provider.
- Admin may intervene in emergencies only; admin messages display with "Hairline Admin" badge.

**Notes**:

- Provide clear attachment guidance: Images (JPG/PNG, max 5MB), Video (MP4, max 10MB), PDF (max 10MB).
- Display file size and type before upload; show validation errors if limits exceeded.
- Maximum 5 attachments per message.
- Provider identity displayed to patient (not anonymous).
- Admin emergency intervention is rare (<5% of conversations) and only for critical situations.

---

### Provider Platform

#### Screen 3: Messages List (Provider)

**Purpose**: Allow providers to view and filter their patient conversations in a popup submenu from the header navigation, see unread counts, and quickly access specific patient chats.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Search | text | No | Search by patient name, inquiry/quote ID, or message content | Min 2 chars; filters list in real-time |
| Filter: Read Status | toggle | No | Filter by read/unread conversations | Options: All / Unread Only |
| Filter: Date Range | dropdown | No | Filter by activity date | Options: Today / Last 7 days / Last 30 days / All |
| Filter: Service Type | dropdown | No | Filter by treatment/service category | Options from service catalog |
| Clear Filters | button | No | Reset all filters | Returns to default view (recent 10) |
| Conversation list | list | Yes | Shows provider-patient conversations with preview | Displayed in popup/dropdown from header; shows up to 20 filtered results |
| Patient name | text | Yes | Patient name (anonymized until payment per FR-003) | Read-only; displayed in list |
| Inquiry/Quote ID | text | No | Associated inquiry or quote reference | Displayed if available; helps identify case |
| Service type | text | Yes | Treatment category for context | Read-only; brief label |
| Last message preview | text | Yes | Preview of last message (truncated) | Max 50 chars; shows "You: " prefix if provider sent |
| Unread badge | indicator | N/A | Shows unread message count | Red badge with count; hidden if 0 |
| Timestamp | text | Yes | Time of last message | Relative (e.g., "1h ago") |
| View All Messages | link | Yes | Link to full messages page if needed | Opens expanded view (future enhancement) |

**Business Rules**:

- Accessible from header navigation as popup/submenu (always visible, no navigation required).
- Default view: most recent 10 conversations sorted by latest activity.
- **One conversation per patient**: If a provider sends multiple quotes to the same patient (different inquiries/treatments), all discussions appear in ONE unified conversation - provider sees only one entry for that patient.
- Filters applied in real-time as provider types/selects; up to 20 filtered results shown.
- Search filters across patient name, inquiry/quote ID, and message content simultaneously.
- Inquiry/Quote ID search useful when provider wants to reference specific treatment within a patient conversation.
- Unread count badge displayed on header messages icon (total unread across all conversations).
- Tapping a conversation closes popup and opens full chat view (Screen 4) with that conversation loaded.
- Real-time updates when new patient messages arrive; unread badge updates immediately.
- Quick access without leaving current page/workflow.

**Notes**:

- Lightweight popup interface with filtering for quick message management.
- Filters help providers prioritize urgent or specific conversations (e.g., "Show unread from last 7 days").
- Does not require full page navigation; provider can continue working while checking messages.
- Search is particularly useful for finding conversations related to specific inquiry/quote IDs.
- If more than 20 results, show "Showing 20 of X conversations - refine filters" message.
- Mobile: may slide in from side with collapsible filter section; Desktop: dropdown from header with inline filters.
- Filters persist during session until cleared.

---

#### Screen 4: Provider ↔ Patient Chat (Provider)

**Purpose**: Allow providers to respond to patient questions about quotes, procedures, and coordination; build trust and clarify details before booking.

**Layout Structure**: 3-panel layout for desktop/tablet (responsive for mobile)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Panel Location |
|------------|------|----------|-------------|------------------|----------------|
| **LEFT PANEL: Conversation List** ||||||
| Conversation list | list | Yes | Shows all provider's patient conversations with preview | Synchronized with Screen 3; shows same conversations | Left |
| Patient name | text | Yes | Patient identifier in list | Read-only; anonymized per FR-003 | Left |
| Last message preview | text | Yes | Preview of last message | Max 50 chars; "You: " prefix if provider sent | Left |
| Unread badge | indicator | N/A | Shows unread count | Red badge with number | Left |
| Timestamp | text | Yes | Time of last message | Relative (e.g., "1h ago") | Left |
| Active indicator | highlight | Yes | Shows currently selected conversation | Highlighted background for selected conversation | Left |
| **CENTER PANEL: Message Thread** ||||||
| Message thread | scrollable panel | Yes | Full conversation history with selected patient | Chronological order; auto-scroll to latest | Center |
| Message text | text | Yes | Each message content | Read-only for history | Center |
| Message sender | indicator | Yes | Shows if patient, provider, or admin sent | "You" for provider, patient name, "Hairline Admin" | Center |
| Message timestamp | datetime | Yes | When message was sent | Displayed per message | Center |
| Message attachments | thumbnails/links | No | Images, videos, PDFs in messages | Clickable to view/download | Center |
| Read status | indicator | N/A | Shows if message was read by patient | Checkmark or "Read" indicator per message | Center |
| Admin badge | indicator | N/A | "Hairline Admin" badge on admin messages | Visible if admin intervened | Center |
| Compose message area | textarea | Yes | Provider response to patient questions | Max 2000 chars; at bottom of center panel | Center |
| Attachment upload | file upload | No | Add supporting media | Images: JPG/PNG max 5MB; Video: MP4 max 10MB; PDF: max 10MB; Max 5 attachments per message | Center |
| Send button | action | Yes | Submits message | Disabled until text or attachment present | Center |
| **RIGHT PANEL: Conversation Info & Tools** ||||||
| Patient identifier | display | Yes | Patient name and ID (anonymized until payment per FR-003) | Read-only; contextual header | Right |
| Patient avatar | image | No | Patient profile picture or placeholder | Displayed at top of right panel | Right |
| Quote references | list | No | All quotes associated with this patient-provider pair | Clickable links to quotes; shows inquiry/quote IDs with service types (e.g., "Quote #123 - Hair Transplant"); helps provider maintain context across multiple treatments | Right |
| Service types | list | Yes | Treatment categories for all quotes | Read-only; comma-separated if multiple | Right |
| Conversation started | datetime | Yes | When conversation was created | Read-only | Right |
| Message count | number | Yes | Total messages in thread | Read-only; updates live | Right |
| Flag indicator | badge | N/A | Shows if conversation has been flagged by admin | Warning icon if keyword-flagged | Right |
| Actions menu | buttons | No | Additional conversation actions | Options: Archive (future), Export conversation, View patient profile | Right |

**Business Rules**:

- Provider can only message patients who have received quotes from them.
- **One conversation per patient-provider pair**: If provider sends multiple quotes to same patient (different inquiries/treatments), all communication happens in ONE unified conversation.
- Quote references section shows ALL inquiry/quote IDs chronologically, helping provider track which treatment each message refers to.
- Patient identity is anonymized (e.g., "Mark P." + ID) until payment confirmation per FR-003.
- All conversations monitored by admin with keyword flagging for compliance.
- Messages logged for compliance and audit.
- Provider sees full conversation history with timestamps and read receipts across all treatments with that patient.
- Admin may intervene in emergencies only; admin messages display with "Hairline Admin" badge visible to both parties.

**Notes**:

- **3-panel layout**: Left panel (conversation list), Center panel (message thread with compose area), Right panel (patient info & tools).
- **Desktop/Tablet**: All 3 panels visible simultaneously; left panel width ~25%, center panel ~50%, right panel ~25%.
- **Mobile**: Single panel view with navigation; left panel (list) → center panel (messages) when conversation selected; right panel accessible via info icon.
- **Left panel**: Synchronized with Screen 3 (popup); selecting conversation updates center and right panels without full page reload.
- **Center panel**: Auto-scrolls to latest message when conversation opens; compose area fixed at bottom.
- **Right panel**: Always shows context for selected conversation; quote references section collapses if no multiple quotes.
- Encourage providers to respond within 24 hours for best patient experience.
- **Multiple quotes visible**: Quote references section in right panel displays all quote IDs with service types (e.g., "Quote #123 - Hair Transplant", "Quote #456 - Beard Transplant") to help provider maintain context.
- Providers can attach treatment plans (PDF), facility photos (JPG/PNG), or before/after examples (JPG/PNG/MP4) to build trust.
- Attachment guidance: Images (JPG/PNG, max 5MB), Video (MP4, max 10MB), PDF (max 10MB); maximum 5 attachments per message.
- Providers should reference specific quote ID in messages when discussing different treatments (e.g., "Regarding your hair transplant quote #123...").
- Clear indication when message contains flagged keywords (warning shown to provider before sending).
- Admin emergency intervention is rare and only for critical situations (policy violations, urgent disputes, safety concerns).

---

### Admin Platform

#### Screen 5: Communication Monitoring Center (Admin)

**Purpose**: Comprehensive message list monitoring all patient-provider conversations (and any admin-patient communications) with advanced filtering and search capabilities for compliance, policy enforcement, and case investigation.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Search | text | No | Find conversations by patient, provider, keyword, inquiry ID | Min 2 chars; searches across all fields |
| Filters | multi-component | No | Comprehensive filtering bar with: Patient (autocomplete), Provider (autocomplete), Service Type (multi-select), Quote ID (text), Inquiry ID (text), Date Range (date picker with presets: Today/Last 7 days/Last 30 days), Flag Type (multi-select: Keyword Flagged/Manually Flagged/Intervened/No Flags), Conversation Status (multi-select: Active/Resolved/Escalated) | All filters applied simultaneously with AND logic; filters persist across session |
| Apply Filters | button | No | Apply all selected filters simultaneously | All filters combined with AND logic |
| Clear Filters | button | No | Reset all filters to default | Restores full conversation list |
| Sort By | dropdown | No | Sort conversation list | Options: Latest Activity / Oldest First / Most Flagged / Provider Name / Patient Name |
| Conversation list | list | Yes | Shows all conversations with preview, participants, flags, timestamps | Paginated; 20 per page |
| Patient name | text | Yes | Patient identifier (anonymized per FR-003) | Read-only; displayed in list |
| Provider name | text | Yes | Provider/clinic name | Read-only; displayed in list |
| Inquiry ID | text | No | Associated inquiry reference | Displayed if available |
| Last message preview | text | Yes | Preview of last message | Max 100 chars |
| Keyword flags | badge | N/A | Red badge for automatic keyword flags | Shows count if multiple |
| Manual flags | badge | N/A | Orange badge for admin observation flags | Shows flag type on hover |
| Intervention indicator | badge | N/A | Shows if admin has intervened | "Admin" badge if intervention occurred |
| Timestamp | text | Yes | Time of last message | Relative (e.g., "2h ago") or absolute |
| Message count | number | Yes | Total messages in conversation | Displayed in list |

**Business Rules**:

- Accessible from Admin platform main navigation as primary monitoring interface.
- Shows ALL patient-provider conversations (and any admin-patient communications) by default; filters narrow the view.
- All filters applied simultaneously with AND logic (e.g., Filter by Provider A AND Inquiry ID 12345 AND Date Range Last 7 Days).
- **Comprehensive filtering**: Patient, Provider, Service Type, Quote ID, Inquiry ID, Date Range, Flag Type, Conversation Status - all can be combined.
- **Inquiry ID filtering**: Admin can filter by inquiry ID to view all conversations related to a specific case (one inquiry may generate multiple provider quotes → multiple conversations).
- Conversation list updates in real-time when new messages arrive or flags are added.
- Keyword flags (red badges) automatically appear when policy violation terms detected.
- Manual observation flags (orange badges) added by admins for proactive monitoring.
- Tapping/selecting a conversation opens detailed Message Thread View (Screen 6A) for full history, flag management, and optional emergency intervention activation (Screen 6B).
- Pagination with 20 conversations per page; scroll to load more.
- Export filtered conversation list to CSV/PDF for compliance audits.
- Clear visual distinction for conversations with flags, interventions, or high message counts.

**Notes**:

- This is the main entry screen for admin messaging - comprehensive overview of all conversations.
- Filter bar should be prominent and easy to use; filters persist across sessions.
- Show total conversation count and filtered count (e.g., "Showing 15 of 247 conversations").
- Visual hierarchy: flagged conversations more prominent than unflagged.
- Preset filter quick actions: "Flagged Only", "Intervened Today", "Unresolved Flags", "Last 24 Hours".
- **Inquiry ID filtering**: Powerful for case investigation - shows all provider conversations for one inquiry side-by-side.
- Export functionality: Export visible/filtered list with conversation metadata (no message content in list export).
- Responsive design: filters collapse to sidebar on mobile; conversation list remains scrollable.
- Performance: Load first 20 conversations quickly; lazy load more on scroll.
- Badge tooltips: Hover over flags/badges to see flag type, reason, timestamp.

---

#### Screen 6A: Message Thread Detail - Monitoring & Flagging (Admin)

**Purpose**: Default view for reviewing specific conversation with full message history, participant information, and flag management capabilities for admin monitoring and observation.

**Activated by**: Selecting a conversation from Screen 5 (Communication Monitoring Center)

**Layout Structure**: 3-panel layout for desktop/tablet (responsive for mobile)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Panel Location |
|------------|------|----------|-------------|------------------|----------------|
| **LEFT PANEL: Conversation List** ||||||
| Conversation list | list | Yes | Shows all conversations from Screen 5 with applied filters | Synchronized with Screen 5; same filtering applies | Left |
| Patient/Provider names | text | Yes | Conversation participants in list | Read-only; displayed in list items | Left |
| Flag indicators | badges | N/A | Red (keyword) or orange (manual) badges | Visible on flagged conversations | Left |
| Last message preview | text | Yes | Preview of last message | Max 50 chars | Left |
| Timestamp | text | Yes | Time of last message | Relative (e.g., "2h ago") | Left |
| Active indicator | highlight | Yes | Shows currently selected conversation | Highlighted background for selected conversation | Left |
| **CENTER PANEL: Message Thread** ||||||
| Conversation header | group | Yes | Shows participants, inquiry/quote IDs, service types, timestamps | Read-only; at top of center panel | Center |
| Patient name | text | Yes | Patient identifier (anonymized per FR-003) | Read-only; in header | Center |
| Provider name | text | Yes | Provider/clinic name | Read-only; in header | Center |
| Message thread | scrollable panel | Yes | Full conversation history with all messages | Read-only; chronological order; main center content | Center |
| Message sender | indicator | Yes | Shows if patient, provider, or admin sent message | Color-coded or icon-based per message | Center |
| Message text | text | Yes | Full message content | Read-only; displayed per message | Center |
| Message attachments | links/thumbnails | No | Images, videos, PDFs attached to messages | Clickable to view/download; inline with messages | Center |
| Message timestamp | datetime | Yes | When message was sent | Displayed per message | Center |
| Read receipts | indicator | Yes | Shows if message was read | Checkmark or "Read" indicator per message | Center |
| Admin badge | indicator | N/A | "Hairline Admin" badge on existing admin messages | Auto-displayed on past admin interventions | Center |
| **RIGHT PANEL: Conversation Info & Flag Management Tools** ||||||
| Conversation metadata | group | Yes | Summary info | Read-only section at top | Right |
| Inquiry IDs | list | No | Associated inquiry references (may be multiple) | Clickable links to inquiries if available | Right |
| Quote IDs | list | No | Associated quote references (may be multiple) | Clickable links to quotes if available | Right |
| Service types | list | Yes | Treatment/service categories | Comma-separated if multiple | Right |
| Conversation started | datetime | Yes | Timestamp when conversation created | Read-only | Right |
| Message count | number | Yes | Total messages in thread | Read-only; updates live | Right |
| Keyword flags panel | panel | No | All automatic keyword flags detected | Collapsible section; list with keyword, timestamp, context snippet | Right |
| Manual flags panel | panel | No | All admin observation flags | Collapsible section; list with flag type, admin user, timestamp, notes | Right |
| Flag history | timeline | No | Chronological timeline of all flag events | Collapsible section; added, reviewed, resolved, escalated with admin names | Right |
| Flag for Observation | button | No | Add manual observation flag | Prominent button; opens flag type dialog | Right |
| Flag type | select | Yes (when flagging) | Type of observation flag | Options: Off-Platform Risk / Potential Dispute / Quality Concern / Follow-Up Needed / Other | Right (in dialog) |
| Flag notes | textarea | No | Internal admin notes about flag | Max 500 chars; NOT visible to users | Right (in dialog) |
| Resolve Flag | button | No | Mark flag as resolved | Button next to each flag; confirmation required | Right |
| Enable Emergency Intervention | button | No | Activate emergency intervention mode (Screen 6B) | Prominent button with warning styling; opens confirmation dialog | Right |
| Actions menu | dropdown | No | Additional admin actions | Options: Export conversation, Request 3D scan, Schedule review | Right |

**Business Rules**:

- Opened when admin selects a conversation from Screen 5 (Monitoring Center list).
- **Default read-only state**: Admin can review but NOT send messages in this mode.
- Full conversation history displayed in chronological order; auto-scroll to latest message.
- All flags (keyword and manual) displayed prominently in dedicated panels.
- Flag history shows complete audit trail: who added, when, type, status changes.
- Manual flagging available without leaving thread view; flag appears immediately and silently (no user notification).
- Conversation header shows ALL inquiry/quote IDs if patient-provider pair has multiple treatments.
- "Enable Emergency Intervention" button only visible to admins with intervention permissions.
- All admin view actions logged with timestamp, admin user, and action type.
- Export conversation: Includes full message history, attachments metadata, flag history, intervention logs.

**Notes**:

- **3-panel layout**: Left panel (conversation list from Screen 5), Center panel (message thread with conversation header), Right panel (conversation info & flag management tools).
- **Desktop/Tablet**: All 3 panels visible simultaneously; left panel width ~25%, center panel ~50%, right panel ~25%.
- **Mobile**: Single panel view with navigation; left panel (list) → center panel (messages) when conversation selected; right panel accessible via info/tools icon.
- **Left panel**: Synchronized with Screen 5; shows same filtered conversation list; selecting conversation updates center and right panels without full page reload.
- **Center panel**: Full message history in chronological order; auto-scrolls to latest message when conversation opens; read-only (no message composition in monitoring mode).
- **Right panel**: Always shows context for selected conversation; collapsible sections for flags (keyword flags, manual flags, flag history); action buttons at bottom.
- Back to Screen 5: Navigation breadcrumb or back button returns to Screen 5 with filters preserved.
- Real-time updates: new messages appear immediately in center panel if conversation is open; left panel list updates with new message previews.
- Attachment preview: inline thumbnails for images/videos in center panel; download links for PDFs.
- Flag management: Quick "Flag for Observation" button in right panel; detailed flag history timeline; resolve buttons next to each flag.
- Performance: Lazy load old messages if conversation has 100+ messages; left panel list uses virtualization for 100+ conversations.
- **Emergency intervention access**: "Enable Emergency Intervention" button prominent in right panel; clicking shows confirmation dialog explaining implications, then transitions to Screen 6B state.
- Keyboard shortcuts: Esc to close thread view, ↑/↓ to navigate conversation list, F to flag, E to enable emergency mode (with confirmation).

---

#### Screen 6B: Message Thread Detail - Emergency Intervention (Admin)

**Purpose**: Activated state allowing admin to actively intervene in critical situations by sending messages directly into the patient-provider conversation. ONLY for serious policy violations, urgent disputes, or patient safety emergencies.

**Activated by**: Clicking "Enable Emergency Intervention" button in Screen 6A and confirming action

**Layout Structure**: 3-panel layout maintained from Screen 6A (responsive for mobile)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Panel Location |
|------------|------|----------|-------------|------------------|----------------|
| Emergency warning banner | alert | Yes | Prominent red/orange banner across top of all panels | Displays: "🚨 EMERGENCY INTERVENTION MODE - Both patient and provider will be notified of your message" | Top (spans all panels) |
| **LEFT PANEL: Conversation List** ||||||
| Conversation list | list | Yes | Same conversation list from Screen 6A | Read-only in emergency mode; can switch conversations | Left |
| Active indicator | highlight | Yes | Shows currently selected conversation | Highlighted background; locked during message composition | Left |
| **CENTER PANEL: Message Thread & Compose** ||||||
| Conversation header | group | Yes | Same conversation header from Screen 6A | Shows participants, inquiry/quote IDs; read-only | Center (top) |
| Message thread | scrollable panel | Yes | Full conversation history (same as 6A) | Read-only; chronological order; remains visible for context | Center (main) |
| Message sender | indicator | Yes | Shows if patient, provider, or admin sent | Same as 6A | Center |
| Message text (history) | text | Yes | Historical message content | Read-only | Center |
| Message timestamp | datetime | Yes | When message was sent | Per message | Center |
| Compose area separator | divider | Yes | Visual separator before compose area | Prominent line with "Admin Intervention Message" label | Center (divider) |
| Message text (admin) | textarea | Yes | Admin emergency intervention message to patient and provider | Max 2000 chars; clearly worded for both parties; fixed at bottom of center panel | Center (bottom) |
| Attachment (admin) | file upload | No | Optional admin attachment (emergency only) | Images: JPG/PNG max 5MB; PDF: max 10MB; Max 5 attachments per message | Center (bottom) |
| Preview button | button | No | Preview how message will appear | Opens preview overlay in center panel | Center (bottom) |
| Send button | action | Yes | Send admin emergency message | Disabled until emergency reason selected and message text present; requires confirmation click | Center (bottom) |
| Cancel / Return to Monitoring | button | Yes | Exit emergency mode without sending | Returns to Screen 6A without sending intervention | Center (bottom) |
| **RIGHT PANEL: Intervention Controls & Context** ||||||
| Conversation metadata | group | Yes | Same metadata from Screen 6A | Inquiry IDs, quote IDs, service types, timestamps | Right (top) |
| Emergency reason | select | Yes | Mandatory reason for intervention | Options: Policy Violation / Urgent Dispute / Patient Safety; must be selected before sending; prominently displayed | Right (middle) |
| Emergency justification | textarea | No | Internal notes explaining intervention decision | Max 500 chars; logged for compliance audit; NOT sent to users | Right (middle) |
| All flags panels | collapsible | No | Keyword flags, manual flags, flag history remain visible | Same as Screen 6A; provide context for intervention decision | Right (middle) |
| Intervention checklist | panel | Yes | Pre-send checklist | Ensures: Reason selected, Message clear, Both parties addressed, Attachments valid (if any) | Right (bottom) |
| Warning reminder | alert | Yes | Persistent reminder in right panel | "This message will be sent to BOTH patient and provider" | Right (bottom) |

**Business Rules**:

- **Explicit activation required**: Admin must click "Enable Emergency Intervention" in Screen 6A and confirm action.
- **Warning banner always visible**: Prominent alert that both parties will be notified.
- **Mandatory reason selection**: Admin CANNOT send message until emergency reason is selected.
- Emergency justification (internal notes) logged for compliance audit but NOT sent to users.
- Message appears in thread with "Hairline Admin" badge visible to both patient and provider.
- Both patient and provider receive push/email notification of admin intervention.
- Admin emergency message CANNOT be edited or deleted after sending.
- System logs: timestamp, admin user, emergency reason, justification notes, full message content.
- Intervention automatically updates conversation flag status if previously flagged.
- After sending, system returns admin to Screen 6A (monitoring mode) with intervention visible in thread.
- **Rare use**: Target <5% of conversations; intervention should be last resort.

**Notes**:

- **3-panel layout maintained**: Left panel (conversation list, read-only during composition), Center panel (message thread + compose area at bottom), Right panel (intervention controls & context).
- **Warning banner spans all panels**: Emergency warning banner at very top crosses all three panels for maximum visibility.
- **Desktop/Tablet**: All 3 panels visible simultaneously; same proportions as Screen 6A (~25% / 50% / 25%).
- **Mobile**: Center panel becomes full-screen with compose area; right panel accessible via "Intervention Controls" button; left panel minimized.
- **Left panel**: Conversation list remains visible but locked during message composition; admin can cancel to switch conversations if needed.
- **Center panel**: Top shows full message history (read-only context); bottom shows compose area with clear separator labeled "Admin Intervention Message"; compose area sticky/fixed at bottom with send/cancel buttons.
- **Right panel**: Emergency reason selection at top (mandatory, prominently displayed); justification notes below; flags panels collapsible for context; intervention checklist at bottom ensures all requirements met before sending.
- **Visual emphasis on seriousness**: Red/orange warning banner across all panels, confirmation dialogs, explicit reason requirement, intervention checklist.
- Preview button opens overlay in center panel showing exactly how message will appear to users (with "Hairline Admin" badge).
- Cancel button prominently available in both center (compose area) and right panels - admin can exit without sending if situation de-escalates.
- Attachment option available for sending policy documents, compliance notices, or safety instructions.
- Intervention message should be professional, authoritative, and clearly explain action/requirement to both parties.
- Best practices guidance tooltip: "Address both parties, state reason clearly, provide specific action required, maintain professional tone."
- Send button disabled until: (1) Emergency reason selected, (2) Message text entered, (3) Checklist items confirmed.
- After sending: System transitions back to Screen 6A with intervention message visible in thread; both patient and provider notified immediately.
- System tracks intervention success rate (conversation resolved vs escalated further); post-intervention conversation may auto-flag for follow-up review (configurable).

---

## Business Rules

### General Module Rules

- All conversations and message events (sent, delivered, read) are logged with timestamps and participants.
- Message content size and attachment limits enforced to ensure reliable delivery and storage.
- All timestamps displayed in the user's local timezone; admin views can toggle UTC for audits.
- Admin emergency interventions are logged with mandatory reason, timestamp, and admin user for compliance oversight.

### Data & Privacy Rules

  Reference Principle II from constitution: Medical Data Privacy & Security

- Provider identities are visible to patients in messaging (patients chat directly with providers who have sent them quotes).
- Patient identity is partially anonymized (e.g., "Mark P." + ID) until payment confirmation per FR-003 business rules.
- Patient PII and media are protected; all data encrypted in transit and at rest per policy.
- Medical communications retained for minimum 7 years; deletion requests result in archival with access restrictions.
- All access to conversations is auditable with user, timestamp, and reason when required.
- Admin has monitoring access to all patient-provider conversations with emergency-only intervention capability.
- Admin emergency interventions logged with timestamp, admin user, emergency reason, and full message content.
- Compliance with GDPR and HIPAA-equivalent practices; patient consent respected for data sharing.

### Admin Editability Rules

  Reference Principle VIII from constitution: Admin-Editable Content

**Editable by Admin**:

- Keyword/phrase flags that trigger moderation or escalation cues.
- Notification preferences and quiet hours policy.
- Emergency intervention reason options (Policy Violation / Urgent Dispute / Patient Safety / Other).

**Fixed in Codebase (Not Editable)**:

- Cryptographic standards and security controls.
- Read receipt semantics and audit logging requirements.
- Minimum retention periods mandated by compliance.
- Attachment type and size limits: Images (JPG/PNG max 5MB), Video (MP4 max 10MB), PDF (max 10MB).
- Maximum number of attachments per message (5).
- Message character limits (2000 chars).

**Configurable with Restrictions**:

- Escalation routing rules (allowed destinations/roles only).
- Conversation export controls (available to specific admin roles).
- Emergency intervention permissions (restricted to authorized admin roles only).

### Payment & Billing Rules *(if applicable)*

  Delete this section if not applicable

Not applicable to messaging scope; no payment flows in this module.

---

## Success Criteria

  These should be testable without knowing implementation details

### Patient Experience Metrics

- **SC-001**: Patients receive visible confirmation that messages are sent within 1 second in 95% of attempts.
- **SC-002**: Patients see new provider replies within 5 seconds of being sent in 95% of conversations.
- **SC-003**: Patient Messages Inbox loads and displays conversation list within 2 seconds in 95% of cases.
- **SC-004**: Inbox search and filter operations complete within 1 second with results displayed in real-time.
- **SC-005**: Provider and Admin header popup message lists load within 500ms when opened (lightweight quick view).
- **SC-006**: 80% of patient quote questions receive a first response from provider within 24 hours.

### Provider Efficiency Metrics

- **SC-007**: Providers can locate and respond to a patient message within 60 seconds using conversation list and filters.
- **SC-008**: 95% of patient-provider messages acknowledge delivery within 2 seconds.
- **SC-009**: Provider response rate to patient messages is at least 90% within 48 hours of receipt.

### Admin Management Metrics

- **SC-010**: Admins can find any conversation in under 10 seconds via search/filters (including inquiry ID search) in 95% of cases.
- **SC-011**: 100% of message events (send, read), admin flag actions, and admin emergency interventions recorded in audit logs and exportable.
- **SC-012**: Keyword flagging correctly highlights 95% of configured terms without false positives exceeding 5%.
- **SC-013**: Manual observation flags are used for proactive monitoring in 10-20% of conversations (enables early detection).
- **SC-014**: Admin emergency interventions occur in <5% of total conversations (intervention is rare and emergency-only).
- **SC-015**: At least 50% of emergency interventions are preceded by manual observation flags (showing proactive monitoring effectiveness).

### System Performance Metrics

- **SC-016**: 99.9% uptime for messaging read/send functionality measured monthly.
- **SC-017**: 95% of message send operations (patient, provider, admin) complete within 2 seconds under normal load.
- **SC-018**: Zero loss of persisted messages; queued messages eventually deliver or fail with explicit user notice.
- **SC-019**: Notifications delivered within 5 seconds in 95% of cases.

### Business Impact Metrics

- **SC-020**: Quote acceptance rate improves by 15% within 3 months of launch (attributed to improved patient-provider communication).
- **SC-021**: Patient satisfaction with provider communication is rated 4.5+ stars (measured via post-procedure survey).
- **SC-022**: Keyword flagging system detects and prevents at least 95% of off-platform solicitation attempts within first 6 months.
- **SC-023**: Manual observation flags enable early intervention, reducing escalation to formal provider warnings by 30%.
- **SC-024**: Admin emergency interventions resolve critical situations with 90% success rate without requiring provider suspension.

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- P-01: Auth & Profile Management
  - Why needed: Identity and access control for participants.
  - Integration point: Use authenticated user context and roles for conversation access.

- FR-004: Quote Submission & Management
  - Why needed: Enable patient-provider chat only when provider has sent quote to patient.
  - Integration point: Check quote existence before allowing conversation creation.

- FR-007: Payment Processing
  - Why needed: Lift patient anonymization when payment is confirmed per FR-003.
  - Integration point: Subscribe to payment confirmation events to update patient visibility.

- S-03: Notification Service
  - Why needed: Deliver real-time alerts for new messages and admin emergency interventions.
  - Integration point: Publish notification events on message state changes.

- S-05: Media Storage Service
  - Why needed: Secure storage and retrieval of attachments.
  - Integration point: Generate secure media links and metadata for threads.

### External Dependencies (APIs, Services)

- Device push notification providers (for mobile alerts)
  - Purpose: Deliver device notifications to patients and providers.
  - Integration: Use platform-standard push delivery; fallback to in-app badges and email where applicable.
  - Failure handling: Queue retry; show in-app banners; notify user if delays persist.

### Data Dependencies

- Active user accounts with verified roles (patient, provider, admin)
  - Why needed: Determine access and routing; authenticate participants.
  - Source: P-01 Auth & Profile.

- Quote submission records
  - Why needed: Enable patient-provider chat only when provider has sent a quote to patient.
  - Source: FR-004 Quote Submission & Management.

- Payment confirmation status
  - Why needed: Lift patient anonymization when payment is confirmed per FR-003.
  - Source: FR-007 Payment Processing.

---

## Assumptions

### User Behavior Assumptions

- Patients have questions about quotes before accepting (pricing, packages, procedure details, timing).
- Patients may attach images/videos to clarify their concerns or provide additional context.
- Majority of patient messaging occurs on mobile devices.
- Providers respond to patient messages during business hours (24-48 hour response time expected).

### Technology Assumptions

- Patients use smartphones with camera capabilities; can capture/upload JPG/PNG images and MP4 videos.
- Provider/Admin web apps accessed via modern browsers (latest 2 versions) with file upload capabilities.
- Intermittent connectivity is common; pending/retry behavior required.
- Secure media storage is available for attachments (images, videos, PDFs).
- Client-side validation for file types and sizes before upload to prevent unnecessary uploads.

### Business Process Assumptions

- Providers monitor patient message inbox during business hours and respond within 24-48 hours.
- Admins monitor all patient-provider conversations for compliance with keyword flagging.
- Admin emergency intervention is RARE and used only for critical situations (estimated <5% of conversations).
- Emergency intervention used for: serious policy violations, urgent disputes that providers cannot resolve, patient safety emergencies.
- Providers are expected to maintain professional communication standards and not solicit off-platform contact.

---

## Implementation Notes

### Technical Considerations

- Architecture: Real-time messaging delivery with persistence and audit logging.
- Technology: Media handling supports JPG/PNG images (max 5MB), MP4 videos (max 10MB), and PDF files (max 10MB); client-side validation before upload; background upload for larger files with progress indication.
- Performance: Degrade gracefully on poor connectivity with retries and clear status; optimize video compression on mobile devices.
- Storage: Medical communications retained per compliance with fast retrieval for care contexts; efficient media storage with thumbnail generation for images/videos.
- Admin intervention: Emergency-only mode with mandatory reason tracking and audit logging.

### Integration Points

- Patient app → Messaging service
  - Data format: Structured message payloads with participant IDs and attachment metadata.
  - Authentication: Tenant-authenticated sessions; role-based permissions.
  - Error handling: Retry on transient failures; clear feedback to user.

- Provider web app → Messaging service
  - Data format: Patient conversation queries, message composition, media attachments.
  - Authentication: Provider-authenticated sessions; access scoped to own patients.
  - Error handling: Validation feedback; retry mechanisms; keyword flag warnings.

- Admin dashboard → Messaging service
  - Data format: Read-only conversation monitoring; emergency intervention payloads with mandatory reason.
  - Authentication: Admin roles only; scoped access; emergency intervention permission check.
  - Error handling: Paged results; robust filtering; export fallbacks; intervention logging.

### Scalability Considerations

- Current scale: Expect dozens to hundreds of concurrent conversations at launch.
- Growth projection: 5× growth in 12 months with seasonal peaks.
- Peak load: Handle sudden spikes (campaigns/product launches) without delivery delays.
- Data volume: Growing media attachments; efficient storage and lifecycle management required.
- Scaling strategy: Horizontally scalable messaging and notification services; background processing for heavy tasks.

### Security Considerations

- Authentication: Strong session controls; MFA is a planned mandatory control for Admin/Provider and will be enforced platform-wide once the shared MFA stack (FR-026 / FR-031) is delivered; until then enforce strong passwords, throttling, and re-authentication flows per policy.
- Authorization: Role-based access; least-privilege visibility to conversations.
- Encryption: All content encrypted in transit (TLS 1.3) and at rest (AES-256); media links protected.
- Audit trail: Immutable logs of access and message events retained per policy; admin interventions specially flagged.
- Threat mitigation: Abuse prevention on messaging and media uploads; keyword moderation and rate controls; emergency intervention tracking.
- Compliance: Align with GDPR and HIPAA-equivalent standards; data residency honored.
- Admin intervention controls: Mandatory reason tracking; limited to authorized roles; full audit logging; performance monitoring to ensure <5% usage rate.

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
5. Given conversation is flagged for observation, when patient or provider opens their messages, then NO indication of flag is visible (silent monitoring).

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

- **Excessive attachments**: Enforce 5 attachments max per message; display clear error "Maximum 5 attachments per message" if exceeded.
- **Oversized attachments**: Block upload and show specific error based on type (e.g., "Image must be under 5MB", "Video must be under 10MB", "PDF must be under 10MB").
- **Unsupported file types**: Block upload and show "Only JPG/PNG images (max 5MB), MP4 videos (max 10MB), and PDF files (max 10MB) are allowed."
- **No provider response within 48 hours**: Auto-remind provider; if still no response after 72 hours, admin may intervene via emergency mode to follow up.
- **Account deletion request with open conversations**: Archive conversations; restrict access per policy; admin emergency messages preserved in archive.
- **Simultaneous sends**: Maintain message ordering and idempotency safeguards; admin emergency messages sorted chronologically with patient/provider messages.
- **Provider persistent off-platform solicitation**: Admin intervenes with warning via emergency mode; repeated violations may trigger provider review/suspension.
- **Patient safety emergency during conversation**: Admin can intervene immediately using emergency mode to provide guidance or escalate to medical team.
- **Admin intervention visibility**: Admin emergency messages visible to both patient and provider; cannot be deleted or edited by any party.
- **Manual flag escalation**: Conversation manually flagged for observation escalates to emergency intervention when situation worsens; flag status updated to "Intervention Completed" after intervention.
- **Multiple flags on same conversation**: System handles multiple manual flags (e.g., flagged as "Off-Platform Risk", later flagged as "Potential Dispute"); flag history shows chronological sequence.
- **Flag without action**: Flagged conversations where concern doesn't materialize; admin can mark flag as "Resolved - No Action Needed" without intervention.
- **Multiple conversations per inquiry**: One patient inquiry can generate multiple quotes from different providers, resulting in multiple conversations; admin filters by inquiry ID to view all related conversations for comprehensive case review (e.g., patient disputes pricing across multiple quotes).

---

## Functional Requirements Summary

### Core Requirements

- **REQ-012-001**: System MUST automatically create a new conversation between patient and provider when provider submits their **first** quote for patient inquiry; subsequent quotes from same provider to same patient MUST add inquiry/quote IDs to existing conversation (one conversation per patient-provider pair).
- **REQ-012-002**: System MUST provide a Messages Inbox view for patients showing all conversations with filtering (read/unread status), search (provider name, message content), and sorting (latest activity, provider name, date created) capabilities.
- **REQ-012-003**: System MUST provide a Messages popup/submenu in header navigation for providers showing recent conversations (max 10) with unread counts and quick access to patient chats.
- **REQ-012-004**: System MUST provide a Communication Monitoring Center for admins as comprehensive message list with advanced filtering (patient, provider, service type, quote ID, inquiry ID, date range, flag type, conversation status) applied simultaneously.
- **REQ-012-005**: System MUST provide a detailed Message Thread View for admins with two states: Screen 6A (default monitoring/flagging state with read-only access) and Screen 6B (activated emergency intervention state with message composition), accessible when conversation is selected from monitoring center.
- **REQ-012-006**: System MUST enable in-app messaging for Patient ↔ Provider with text and media, accessible ONLY through dedicated Messages/Inbox screens (not through quote detail screens).
- **REQ-012-007**: System MUST deliver real-time notifications for new messages to intended recipients (patients, providers, and both parties when admin intervenes); update unread badges in inbox views and header popup menus.
- **REQ-012-008**: Users MUST be able to view complete conversation history with timestamps and read receipts.
- **REQ-012-009**: System MUST enforce attachment type and size limits (Images: JPG/PNG max 5MB; Video: MP4 max 10MB; PDF: max 10MB; max 5 attachments per message) and provide specific user feedback on violations.
- **REQ-012-010**: System MUST log message lifecycle events (sent, delivered, read) and admin emergency interventions for audit.
- **REQ-012-011**: System MUST allow admins to manually flag conversations for observation with flag type selection (Off-Platform Risk / Potential Dispute / Quality Concern / Follow-Up Needed / Other) and optional internal notes.
- **REQ-012-012**: System MUST distinguish between automatic keyword flags (red) and manual observation flags (orange) in admin monitoring center and thread detail view; flagging must NOT notify patient or provider.
- **REQ-012-013**: System MUST allow admins to send messages in patient-provider conversations ONLY for emergency situations with mandatory reason tracking (Policy Violation / Urgent Dispute / Patient Safety).
- **REQ-012-014**: System MUST clearly identify admin messages with "Hairline Admin" badge visible to both patient and provider.

### Data Requirements

- **REQ-012-015**: System MUST maintain conversations per patient-provider pair with searchable metadata (patient ID, provider ID, inquiry ID, quote reference, status, unread_count, keyword flags, manual observation flags, admin_intervened flag, emergency_reason, last_message_at).
- **REQ-012-016**: System MUST store flag history for each conversation including flag type, timestamp, admin user, status (active/resolved), and internal notes.
- **REQ-012-017**: System MUST store attachments securely with links to their parent messages, access controls, and metadata (file type, size, upload timestamp, thumbnail URLs for images/videos).

### Security & Privacy Requirements

- **REQ-012-018**: System MUST enable patient-provider messaging only when provider has sent a quote to patient.
- **REQ-012-019**: System MUST encrypt all message content and media in transit and at rest and protect access by role.
- **REQ-012-020**: System MUST retain medical communications for at least 7 years and support audit export for compliance.
- **REQ-012-021**: Admin MUST have monitoring access to all patient-provider conversations with manual flagging capability and EMERGENCY-ONLY intervention capability.
- **REQ-012-022**: System MUST maintain patient anonymization (e.g., "Mark P." + ID) until payment confirmation per FR-003.
- **REQ-012-023**: System MUST log all admin actions (manual flags, flag status changes, emergency interventions) with timestamp, admin user, reason/notes, and action type for compliance audit.
- **REQ-012-024**: System MUST restrict admin intervention to authorized admin roles only; track intervention frequency to ensure <5% threshold; manual observation flags can be used more liberally for proactive monitoring.

### Integration Requirements

- **REQ-012-025**: System MUST integrate with Quote Management (FR-004) to automatically create or update conversation when quote is submitted (create new if first quote from provider to patient; add quote/inquiry ID to existing if subsequent); conversation must reference all inquiry IDs (array) for admin filtering and case tracking; conversation appears or updates in both inboxes immediately.
- **REQ-012-026**: System MUST integrate with Notification Service (S-03) to send alerts on message events (including admin emergency interventions to both parties) and update unread badges; manual observation flags must NOT trigger notifications.
- **REQ-012-027**: System MUST integrate with Media Storage Service (S-05) for attachments with secure retrieval.
- **REQ-012-028**: System MUST integrate with Payment Processing (FR-007) to lift patient anonymization upon payment confirmation.

### Marking Unclear Requirements

No unresolved clarifications remain for this scope. Patient ↔ Provider messaging is in scope for V1 with admin emergency-only intervention capability for critical situations.

---

## Key Entities

- Entity 1 - Conversation: Unified thread of messages between a patient-provider pair (with optional admin emergency participation). One conversation per patient-provider pair regardless of number of inquiries/quotes.
  - Key attributes: patient_id, provider_id, inquiry_ids (array), quote_references (array), status, keyword_flags (array), manual_observation_flags (array), admin_intervened (boolean), emergency_reason (if admin intervened), created/updated times, last_message_at.
  - Relationships: Has many messages; has many flags; belongs to one patient and one provider; belongs to multiple inquiries (array); references multiple quotes (array); may include admin emergency messages.
  - Note: Arrays store chronologically ordered IDs as patient-provider pair may have multiple treatment inquiries/quotes over time.

- Entity 2 - Message: Single unit of communication within a conversation.
  - Key attributes: sender (patient/provider/admin), sender_type, text, attachments, timestamps (sent/read), delivery/read status, admin_badge (boolean), emergency_reason (if sender is admin).
  - Relationships: Belongs to one conversation; has many attachments; generates notifications (to both patient and provider when admin sends emergency message).

- Entity 3 - Attachment: Media linked to a message.
  - Key attributes: type (jpg/png/mp4/pdf), size (bytes), secure location (URL), thumbnail/preview metadata (for images/videos), upload timestamp, original filename.
  - Validation constraints: Images (JPG/PNG max 5MB), Video (MP4 max 10MB), PDF (max 10MB); max 5 per message.
  - Relationships: Belongs to one message; access controlled by conversation permissions.

- Entity 4 - Flag: Admin observation flag or automatic keyword flag for a conversation.
  - Key attributes: conversation_id, flag_type (automatic_keyword / manual_observation), category (for manual: Off-Platform Risk / Potential Dispute / Quality Concern / Follow-Up Needed / Other; for automatic: keyword matched), status (active / resolved / escalated_to_intervention), admin_user (for manual flags), internal_notes (for manual flags), created_timestamp, updated_timestamp, resolved_timestamp.
  - Relationships: Belongs to one conversation; created by one admin user (for manual flags); may trigger admin actions.

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-11 | 1.0 | Initial PRD creation | AI |
| 2025-11-11 | 1.1 | Filled scope, workflows, rules, and criteria | AI |
| 2025-12-19 | 2.0 | Major update: Changed from Patient ↔ Support/Aftercare model to Patient ↔ Provider direct messaging; providers chat directly with patients about quotes and procedures; admin has monitoring with emergency-only intervention capability (serious policy violations, urgent disputes, patient safety emergencies); unified all terms to "provider"; organized screens by tenant platform | AI |
| 2025-12-19 | 2.1 | Clarified entry points: Conversations automatically created when provider submits quote; accessible ONLY through dedicated Messages/Inbox screens (not through quote detail screens); updated workflows, user stories, and requirements to reflect inbox-based access pattern | AI |
| 2025-12-19 | 2.2 | Added specific attachment requirements: Images (JPG/PNG max 5MB), Video (MP4 max 10MB), PDF (max 10MB), max 5 attachments per message; updated all screen specifications, business rules, edge cases, and requirements with detailed validation rules and error messages | AI |
| 2025-12-19 | 2.3 | Added manual observation flagging workflow for admins: flag conversations for closer monitoring without notifying users; flag types (Off-Platform Risk, Potential Dispute, Quality Concern, Follow-Up Needed, Other); flag history tracking; updated admin screen, workflows (A2), user stories, requirements, success criteria, and key entities to support proactive monitoring without immediate intervention | AI |
| 2025-12-19 | 2.4 | Added Patient Messages Inbox screen (Screen 1) with filtering (read/unread status), search (provider name, message content), and sorting capabilities; conversation list with unread badges, last message preview, timestamps; renumbered chat screen to Screen 2; updated entry points, workflows, user stories (new User Story 1 for inbox management), requirements, and success criteria to reflect inbox-first navigation pattern | AI |
| 2025-12-19 | 2.5 | Reordered screen specifications: Patient Platform (Screens 1, 2) → Provider Platform (Screen 3) → Admin Platform (Screen 4); updated screen code numbers to use simple incremental numbering across all tenants (per standard PRD convention) | AI |
| 2025-12-19 | 2.6 | Added Inquiry ID filtering to Admin Communication Monitoring Center: admins can filter/search by inquiry ID to view all conversations related to a specific case (useful for dispute resolution, compliance audits, case investigations); updated data requirements, key entities, and integration requirements to reference inquiry_id | AI |
| 2025-12-19 | 2.7 | Added Messages List popup/submenu for Provider (Screen 3) accessible from header navigation; renumbered Provider chat to Screen 4; restructured Admin platform with Screen 5 (Communication Monitoring Center - comprehensive message list with advanced filtering by patient, provider, service, quote ID, inquiry ID, date range, flags, status) and Screen 6A/6B (Message Thread Detail with separate monitoring and emergency intervention states); updated entry points, multi-tenant breakdown, and requirements | AI |
| 2025-12-19 | 2.8 | Added filtering capabilities to Provider Messages List (Screen 3): search, read status, date range, service type filters; clarified unified conversation model: ONE conversation per patient-provider pair regardless of number of quotes (verified with transcriptions showing relationship-based "message them directly" language); conversation entity updated with quote_references and inquiry_ids arrays; multiple quote references displayed in provider chat for context; updated all screens, workflows, requirements (REQ-012-001, REQ-012-025), and key entities | AI |
| 2025-12-19 | 2.9 | Split Screen 6 into two explicit subsections for clarity: Screen 6A (Message Thread Detail - Monitoring & Flagging) as default read-only state with flag management, and Screen 6B (Message Thread Detail - Emergency Intervention) as activated state with message composition, mandatory reason selection, and prominent warnings; emphasizes seriousness of intervention capability and provides clearer design/implementation guidance; updated entry points and references throughout document | AI |
| 2025-12-19 | 2.10 | Added explicit 3-panel layout structure to Provider (Screen 4) and Admin (Screens 6A/6B) message detail views: LEFT panel (conversation list synchronized with inbox/monitoring center), CENTER panel (message thread with compose area for provider or read-only for admin monitoring), RIGHT panel (conversation info, tools, quote references for provider; flag management and intervention controls for admin); documented responsive behavior for desktop/tablet/mobile; updated data fields tables to include panel location column; enhanced notes sections with layout specifications | AI |
| 2025-12-22 | 2.11 | Verified & aligned with system PRD updates: patient ↔ provider is V1 messaging channel; support/aftercare messaging deferred; standardized patient identity reveal to post-payment only; marked MFA as planned control per Constitution; fixed duplicate REQ IDs in summary | AI |

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
