# FR-035 - Patient Help Center & Support Submission

**Module**: P-08: Help Center & Support Access | Integrates with FR-033 (Help Centre Content Management) and FR-034 (Support Center & Ticketing System)
**Feature Branch**: `fr035-patient-help-support`
**Created**: 2026-03-06
**Status**: Draft
**Source**: FR-035 from system-prd.md, Client transcriptions (HairlineApp-Part2.txt, Hairline-AdminPlatform-Part1.txt, Hairline-ProviderPlatformPart2.txt), missing-mobile-flows-design-complement.md (Flow P08.1)

---

## Executive Summary

The Patient Help Center & Support Submission module provides the patient-facing interface for accessing self-service help content and submitting support requests directly from the patient mobile app. This feature acts as the patient-side reading layer for Help Centre content managed by admins via FR-033, and as the patient-side submission interface for support cases managed via FR-034.

**Key Objectives**:

- Provide patients with 24/7 access to self-service help resources (FAQs, articles, resources, videos) tailored to the patient audience
- Enable patients to submit support requests, feedback, and feature requests directly from the mobile app, creating tracked cases in FR-034
- Enable two-way threaded communication between patients and admin support staff within support cases
- Reduce support ticket volume by enabling patients to find answers independently before contacting support
- Maintain complete content isolation: patients see only patient-audience content, never provider content

**Problem Solved**: Without a dedicated patient-facing help center, patients must rely on external channels (email, phone) for support — leading to slower response times, lost inquiries, and no self-service path. This module ensures patients can find answers independently and, when needed, submit tracked support requests with full two-way communication and status visibility.

**Business Value**:

- **Improved Patient Satisfaction**: Immediate access to self-service answers and transparent ticket tracking with two-way communication
- **Reduced Support Load**: Self-service content deflects common questions, allowing admin staff to focus on complex issues
- **Complete Multi-Tenant Support**: Completes the support architecture across all three platforms (Patient via FR-035, Provider via FR-032, Admin via FR-034)
- **Compliance & Audit Trail**: All support interactions tracked with case IDs, timestamps, and communication history via FR-034
- **Healthcare Safety**: Emergency contact information always accessible for post-procedure patient safety

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-08)**: Full patient-facing Help Center experience — browse help content, search, submit support requests and feedback, view and manage support tickets with two-way communication
- **Provider Platform (PR-XX)**: Not applicable (providers access help via FR-032) (REQ-035-034)
- **Admin Platform (A-XX)**: Not applicable (admins manage content via FR-033, manage tickets via FR-034) (REQ-035-034)
- **Shared Services (S-03)**: Notification Service for support case email notifications (status changes, admin replies, case closure)

### Multi-Tenant Breakdown

**Patient Platform (P-08)**:

- Patients access Help Center from patient mobile app navigation (Settings screen or in-app deep links)
- Patients browse help content organized by 4 content types: FAQs, Articles (Tutorial Guides + Troubleshooting Tips), Resources, Videos
- Patients search across all published patient-audience help content
- Patients view content detail with "Was this helpful?" feedback
- Patients submit support requests via Contact Support form, creating tracked cases in FR-034
- Patients view their submitted support tickets with status, priority, and communication thread
- Patients reply to admin messages within support cases (two-way threaded communication)
- Patients receive email and push notifications on case status changes and admin replies (via FR-020, S-03)

**Provider Platform (PR-XX)**:

- See REQ-035-034.

**Admin Platform (A-XX)**:

- See REQ-035-034.
- Admin actions that affect patient experience: publishing/unpublishing content (FR-033), responding to patient cases (FR-034), updating case status (FR-034)

**Shared Services (S-03)**:

- Sends email notifications to patients when support case status changes (Open -> In Progress, In Progress -> Resolved, Resolved -> Closed) (REQ-035-031)
- Sends email notifications to patients when admin replies to their case (REQ-035-031)
- Sends case closure notification when auto-closure period expires (REQ-035-031)

### Communication Structure

**In Scope**:

- Patient browsing and reading admin-published Help Center content (read-only consumption of FR-033 content)
- Patient submitting support requests and feedback via Contact Support form (creates cases in FR-034)
- Patient viewing support ticket status, communication thread, and case details
- Patient replying to admin messages within support cases (two-way threaded communication via FR-034)
- Patient receiving notifications on case updates (via FR-020, S-03)
- Patient providing "Was this helpful?" feedback on help content (aggregated, anonymous)

**Out of Scope**:

- **REQ-035-078**: Out of scope: Help Center content creation, editing, publishing (handled by FR-033: Help Centre Content Management)
- **REQ-035-079**: Out of scope: Support case management, assignment, escalation, resolution (handled by FR-034: Support Center & Ticketing)
- **REQ-035-080**: Out of scope: Real-time in-app chat between patient and admin (future enhancement)
- **REQ-035-081**: Out of scope: Service Status page (provider-only feature per FR-033)
- **REQ-035-082**: Out of scope: Aftercare-specific communications (handled by FR-011: Aftercare & Recovery Management)
- **REQ-035-083**: Out of scope: Provider-to-patient secure messaging (handled by FR-012: Secure Messaging)
- **REQ-035-084**: Out of scope: Automated chatbot responses (future enhancement)
- **REQ-035-085**: Out of scope: Community forum (future enhancement)

### Entry Points

- Patient navigates to "Help & Support" from Settings screen (FR-026 / P01.2-S1) (REQ-035-033)
- In-app deep link from other screens (e.g., contextual help links from booking, payment, or aftercare screens) (REQ-035-033)
- Push notification tap (e.g., tapping a case status change notification navigates to Ticket Detail) (REQ-035-033)
- Report a Problem row on the Help & Support Hub opens Contact Support (Screen 5) with the category preset to Technical Issue; the system attaches the device, operating system, app version, and report time per FR-034 REQ-034-164 (REQ-035-033)
- Help and Support entry for a person who is not logged in (for example when sign-up fails, FR-001 REQ-001-170): shows only the support contact details (phone and email), with no case and no help content (REQ-035-024, REQ-035-033)

---

## Business Workflows

### Main Flow: Patient Accesses Help Center and Finds Answer

**Actors**: Patient, System, FR-033 Help Centre Content Service
**Trigger**: Patient navigates to Help & Support from Settings or in-app deep link
**Outcome**: Patient finds answer to their question via self-service content

**Flow Diagram**:

```mermaid
flowchart TD
    S1["1. Patient navigates to Help & Support from Settings or in-app deep link"] --> S2["2. System displays Help & Support Hub (Screen 1) with search bar, Help Center link, Contact Support link, My Support Tickets link, and Emergency Contact section"]
    S2 --> S3["3. Patient taps Browse Help Center"]
    S3 --> S4["4. System displays Help Center Browser (Screen 2) with 4 content type cards: FAQs, Articles, Resources, Videos"]
    S4 --> S5["5. Patient selects a content type (e.g., FAQs)"]
    S5 --> S6["6. System displays content list for selected type (e.g., collapsible FAQ topic sections)"]
    S6 --> S7["7. Patient taps content item to view detail"]
    S7 --> S8["8. System displays content detail (title, body, Was this helpful?, related content)"]
    S8 --> S9["9. Patient taps Was this helpful? Yes"]
    S9 --> S10["10. System logs aggregated feedback and displays thank-you confirmation"]
```

### Alternative Flows

**A1: Patient Searches for Help Content**

- **Trigger**: Patient types in search bar on Help & Support Hub or Help Center Browser
- **Outcome**: Patient finds relevant content via search results

```mermaid
flowchart TD
    A1S1["1. Patient types search query in search bar"] --> A1S2["2. System searches across all published patient-audience content (FAQs, Articles, Resources, Videos)"]
    A1S2 --> A1S3["3. System displays matching results ranked by relevance on the Help Center Browser (Screen 2)"]
    A1S3 --> A1S4["4. Patient taps a result to view content detail"]
```

**A2: Patient Cannot Find Answer and Contacts Support**

- **Trigger**: Patient searches and gets no results, or taps "No" on "Was this helpful?" on any content type (FAQ, article, resource, or video)
- **Outcome**: Patient is routed to Contact Support form

```mermaid
flowchart TD
    A2S1["1. Patient taps No on Was this helpful? or sees no search results"] --> A2S2["2. System displays Still need help? Contact Support CTA"]
    A2S2 --> A2S3["3. Patient taps Contact Support"]
    A2S3 --> A2S4["4. System displays Contact Support form (Screen 5)"]
```

**A3: Patient Submits Support Request**

- **Trigger**: Patient taps Contact Support from Hub, Ticket List, or after unsuccessful help search, or taps Report a Problem on the Hub (Screen 5 then opens with the category preset to Technical Issue and the device details attached, FR-034 REQ-034-164)
- **Outcome**: Support case created in FR-034, patient sees the confirmation screen (a confirmation email follows unless an admin has switched it off)

```mermaid
flowchart TD
    A3S1["1. Patient opens Contact Support form (Screen 5)"] --> A3S2["2. Patient enters case title, selects category, writes description, selects priority, optionally attaches files"]
    A3S2 --> A3S3["3. Patient taps Submit"]
    A3S3 --> A3S4["4. System creates support case in FR-034 with case ID (CASE-YYYY-#####), Ticket Source = Patient App, Submitter Type = Patient"]
    A3S4 --> A3S5["5. System links case to patient record via logged-in session"]
    A3S5 --> A3S6["6. System sends confirmation email to patient with case reference number (via S-03) unless an admin has switched it off; sent in parallel with step 7, and the screen does not wait for it"]
    A3S5 --> A3S7["7. System displays confirmation screen with Case ID and message: We will respond within 24 hours on business days"]
    A3S7 --> A3S8["8. System navigates to My Support Tickets (Screen 3)"]
```

**A4: Patient Views and Replies to Support Ticket**

- **Trigger**: Patient taps a ticket from My Support Tickets list, or taps a case notice (push or in-app) that opens Ticket Detail (REQ-035-031)
- **Outcome**: Patient views case detail and replies to admin message

```mermaid
flowchart TD
    A4S1["1. Patient navigates to My Support Tickets (Screen 3)"] --> A4S2["2. System displays list of patient's support cases with status badges and last activity timestamps"]
    A4S2 --> A4S3["3. Patient taps a ticket card"]
    A4S3 -->|case is Open or In Progress| A4S4["4. System displays Ticket Detail (Screen 4) with case info, communication thread, and reply input"]
    A4S3 -->|case is Resolved| A5S1ref["Flow A5, step 1"]
    A4N["Patient taps a case notice"] --> A4S4
    A4S4 --> A4S5["5. Patient types reply and taps Send"]
    A4S5 --> A4S6["6. System adds patient reply to communication thread"]
    A4S6 --> A4S7["7. System notifies assigned admin via FR-020 (support.case_user_reply event)"]
```

**A5: Patient Replies to Resolved Case (Auto-Reopen)**

- **Trigger**: Patient replies to a case with status "Resolved" during the auto-closure window
- **Outcome**: Case automatically reopens to "Open" status

```mermaid
flowchart TD
    A5S1["1. Patient views Ticket Detail for a Resolved case (opened from the list, or after the case becomes Resolved in flow A6)"] --> A5S2["2. Patient sees auto-closure countdown: This case will close in X days if no further reply (no Resolved window and no countdown when the closure period is Immediately)"]
    A5S2 --> A5S3["3. Patient types reply describing unresolved issue"]
    A5S3 --> A5S4["4. System adds reply to communication thread"]
    A5S4 --> A5S5["5. System automatically reopens case to Open status"]
    A5S5 --> A5S5a["5a. System sends the admin a support.case_reopened notice, in addition to the reply notice (FR-034 REQ-034-092)"]
    A5S5 --> A5S6["6. Patient sees status badge update immediately"]
    A5S6 --> A5S7["7. Admin receives support.case_user_reply notification via FR-020"]
```

**A6: Resolved Case Closes**

- **Trigger**: Admin marks a case Resolved and the patient does not reply before the auto-closure period ends (or the period is Immediately)
- **Outcome**: Case is Closed; the patient sees the Closed Case Banner and can create a new ticket or, when the support email setting has a value, ask for the case to be reopened by email

```mermaid
flowchart TD
    A6S1["1. System sends the resolution summary email when the case becomes Resolved, if Send Resolution Email is checked on the case and the notification settings allow it, and not to a deleted patient (REQ-035-070, REQ-035-075)"] -->|period is 3, 7, or 14 days| A6S2["2. Patient views Ticket Detail and sees the countdown (flow A5 if the patient replies)"]
    A6S1 -->|period is Immediately| A6S3
    A6S2 -->|no reply before the period ends| A6S3["3. The case is Closed when the closure period ends; FR-034 REQ-034-062 owns the auto-close and REQ-035-067 the patient-side result"]
    A6S3 --> A6S4["4. System sends the support.case_closed notice to the patient, unless the patient account is deleted (REQ-035-075)"]
    A6S4 --> A6S5["5. Patient opens Ticket Detail; System shows the Closed Case Banner in place of the reply input (REQ-035-069)"]
    A6S5 -->|Create New Ticket| A6S6["6a. Patient taps Create New Ticket and Contact Support form opens (Screen 5)"]
    A6S5 -->|Email support, shown only when the support email setting has a value| A6S7["6b. Patient taps Email support; an email to the support address opens with the case ID in the subject (FR-034 Workflow B3)"]
    A6S2 -->|reply sent as the case closes| A6S8["7. System refuses the reply with a message, keeps the typed text visible for copying, and shows the Closed Case Banner (REQ-035-068)"]
    A6S8 --> A6S5
```

**B1: Server Finds a Problem After Submit**

- **Trigger**: Patient taps Submit on a Contact Support form that passed every on-screen check (Submit is enabled only when every field is valid), and the server finds a problem with the submission
- **Outcome**: Patient corrects the reported fields and resubmits

```mermaid
flowchart TD
    B1S1["1. Patient taps Submit with every field valid"] --> B1S2["2. System checks the submission on the server and finds a failure"]
    B1S2 --> B1S3["3. System highlights the affected fields with inline error messages"]
    B1S3 --> B1S4["4. Patient corrects the reported errors and resubmits"]
```

**B2: Help Center Content Unavailable**

- **Trigger**: API error prevents loading Help Center content
- **Outcome**: Patient sees error state with retry option and Contact Support fallback

```mermaid
flowchart TD
    B2S1["1. Patient navigates to Help Center Browser"] --> B2S2["2. System fails to load content from FR-033 API"]
    B2S2 --> B2S3["3. System displays cached content if available, otherwise shows: Help Center temporarily unavailable. Please try again later."]
    B2S3 --> B2S4["4. Patient taps Retry or navigates to Contact Support as fallback"]
```

**B3: Submission Cannot Complete Now**

- **Trigger**: Patient taps Submit or attaches a file and a supporting service cannot complete the step right now, or the file fails the virus scan
- **Outcome**: Patient sees a clear end state for each cause and never loses the request

```mermaid
flowchart TD
    B3S1["1. Patient taps Submit or attaches a file and the step cannot complete right now"] -->|device offline or FR-034 server error| B3S2["2a. System queues the submission on the device (one request waits at a time; a second submit is refused with a message to wait until the first is sent) and shows: queued, will be sent when online (a server error is retried with growing waits) (REQ-035-062)"]
    B3S2 --> B3S3["3a. System sends the queued submission when connectivity returns; the patient gets the Case ID after it is sent, and flow A3 continues"]
    B3S3 -->|not sent within 24 hours| B3S8["3b. System tells the patient the request was not sent and keeps the typed text so it can be sent again (REQ-035-062)"]
    B3S1 -->|10 new tickets already in the last hour| B3S4["2b. System refuses the submission and shows a message to wait before trying again (REQ-035-063)"]
    B3S1 -->|virus scanner unavailable| B3S5["2c. System refuses the file with a try again later message; the patient can send the case without it (REQ-035-014)"]
    B3S5 --> B3S6["3c. Patient taps Submit without the file and flow A3 continues"]
    B3S1 -->|file fails the virus scan| B3S9["2e. System refuses the file with the FR-034 message (REQ-034-106); the patient can send the case without it (REQ-035-058, REQ-035-059)"]
    B3S9 --> B3S6
    B3S1 -->|media storage unavailable| B3S7["2d. System creates the case without the files, queues the files for retry, and tells the patient of the delay (REQ-035-061)"]
```

---

## Screen Specifications

### Screen 1: Help & Support Hub

**Purpose**: Central entry point for all help resources and support channels

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Screen Title | text | Yes | "Help & Support" | Displayed at top of screen | no graph field (static text) |
| Back Navigation | action | Yes | Back arrow to return to Settings or previous screen | Top-left corner | no graph field (control) |
| Search Bar | text | Yes | "Search help articles..." placeholder; full-text search across all published patient-audience Help Center content (FAQs, Articles, Resources, Videos) | Results appear on the Help Center Browser (Screen 2), whichever search bar the patient types in; scoped to patient audience only (FR-033 Rule 3); relevance-ranked results are required for P1 | no graph field (control) |
| Browse Help Center | link | Yes | Row with book/article icon + "Help Center" label + chevron | Navigates to Screen 2; covers 4 content types: FAQs, Articles (Tutorial Guides + Troubleshooting Tips), Resources, Videos (FR-033 REQ-033-003) | no graph field (control) |
| Contact Support | link | Yes | Row with headset/message icon + "Contact Support" label + chevron | Opens Contact Support form (Screen 5), creating new ticket via FR-034 | no graph field (control) |
| Report a Problem | link | Yes | Row with warning icon + "Report a Problem" label + chevron | Opens Contact Support form (Screen 5) with the category preset to Technical Issue (the patient can change it); the system attaches the device, operating system, app version, and report time per FR-034 REQ-034-164; the patient does not enter them | no graph field (control) |
| My Support Tickets | link | Yes | Row with ticket icon + "My Support Tickets" label + chevron + open ticket count badge | Navigates to Screen 3; badge shows count of open/in-progress tickets | ENT-support-case.status |
| Emergency Contact Section | group | Yes | Always-rendered section at bottom of screen with emergency contact details; each row shows when it has a value, and at least one always has (FR-026 keeps at least one of the two set) | Must remain visible regardless of scroll position (sticky or always rendered) | no graph field (group of two App Settings) |
| — Emergency Phone | text | Conditional | Emergency phone number for urgent post-treatment concerns | Shown only when its App Setting has a value; read-only; tap-to-call on mobile | no graph field (App Setting SET-support-emergency-contact-phone) |
| — Emergency Email | text | Conditional | Emergency email address | Shown only when its App Setting has a value; read-only; tap-to-compose on mobile | no graph field (App Setting SET-support-emergency-contact-email) |

**Business Rules**:

- All Help Center content is read-only for patients; it is managed exclusively by admins via FR-033 and scoped to the patient audience (FR-033 REQ-033-008) (REQ-035-001)
- Search covers all published patient-audience Help Center content (FAQs, Articles, Resources, Videos); results are ranked by relevance; if no results match, show a "Contact Support" prompt. Full-text search is required for P1 and must not be downgraded to browse-only behavior. (REQ-035-036)
- **[Design Addition — not in FR-033/FR-034]** Emergency contact section is a healthcare UX best practice for post-procedure patient safety; the section is always rendered — it cannot be hidden or require scrolling past it. Emergency phone and email values are two App Settings owned by FR-026 (support emergency contact phone and email); this screen displays them. Each row is shown only when its setting has a value: a row with no value is left out, and the Contact Support row stays. FR-026 must keep at least one of the two values set: its settings screen refuses to save both blank, so the section is never empty. (REQ-035-039, REQ-035-040)
- See REQ-035-010.
- A person who is not logged in sees only the support contact details (phone and email) when reaching Help and Support, for example when sign-up fails (FR-001 REQ-001-170); no case and no help content is shown (REQ-035-024, REQ-035-033)
- "My Support Tickets" badge count reflects open + in-progress tickets only; hidden when count is 0 (REQ-035-041)

---

### Screen 2: Help Center Browser

**Purpose**: Browse patient-facing help content organized by content type, search articles, and view content detail

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Screen Title | text | Yes | "Help Center" | Displayed at top of screen | no graph field (static text) |
| Back Navigation | action | Yes | Back arrow to return to Help & Support Hub (Screen 1) | Top-left corner | no graph field (control) |
| Search Bar | text | Yes | Full-text search across all patient-audience help content. | Auto-suggests results while typing; scoped to patient audience (FR-033 Rule 3); required for P1 | no graph field (control) |
| Content Type Cards | group | Yes | Tappable content type tiles (4 content types for patient platform per FR-033 REQ-033-003) | Content types: FAQs, Articles, Resources, Videos; all four cards are always shown; no Service Status for patients. Articles content type contains subtypes: Tutorial Guides, Troubleshooting Tips — shown as secondary filters within the Articles list view | ENT-help-centre-content.content_type |
| — Content Type Icon | icon | Yes | Icon representing the content type | Visual differentiator per content type | ENT-help-centre-content.content_type |
| — Content Type Label | text | Yes | Content type name | Read-only | ENT-help-centre-content.content_type |
| — Item Count Badge | badge | No | Number of published items in the content type | Read-only; hidden if count is 0 | no graph field (derived count) |
| — Empty Content Type State | group | Conditional | Shown when a content type has 0 published items | Content type card is shown greyed out but still tappable, with label "No content available yet"; tapping shows empty state message | no graph field (state message) |
| Featured / Popular Articles | list | No | **[Design Addition]** Automatic shortlist of the five patient articles with the most views in the past 30 days | Not defined in FR-033; generated automatically from view analytics (FR-033 REQ-033-018), not curated by admins. Up to 5 items. (REQ-035-044) | ENT-help-centre-content |
| Content Unavailable State | group | Conditional | Shown when Help Center content cannot be loaded (API unavailable) | "Help Center temporarily unavailable. Please try again later." with retry button. Alternatively, display cached content if available. | no graph field (state message) |

**Content Type: FAQs (FR-033 REQ-033-006)**

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| FAQ Topic Sections | group | Yes | Collapsible accordion sections organized by topic (FR-033 REQ-033-006) | Topics are admin-defined via FR-033; each section header shows topic name + item count; tapping expands/collapses the section | ENT-help-centre-content.topic |
| — FAQ Item | group | Yes | Individual FAQ entry within a topic section | Tapping expands the answer inline (accordion style) or navigates to FAQ detail | ENT-help-centre-content |
| — FAQ Question | text | Yes | The question text | Bold; always visible as accordion header | ENT-help-centre-content.title |
| — FAQ Answer | text | Yes | The answer text (rich text) | Shown on expand; supports formatted text and inline images | ENT-help-centre-content.body |
| — "Was this helpful?" | group | Yes | Binary feedback on the FAQ answer | Same behavior as Article Detail feedback (see below), including the Contact Support prompt after No | ENT-help-centre-content.helpfulness_rating |

**Content Type: Articles (Tutorial Guides + Troubleshooting Tips)**

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Article Subtype Filter | chips | Yes | Filter chips: "All", "Tutorial Guides", "Troubleshooting Tips" | "All" default; filters the article list by subtype | no graph field (control) |
| Article List | list | Yes | Full list of published articles for the selected subtype | Shown after patient selects Articles content type | ENT-help-centre-content |
| — Item Title | text | Yes | Article title | Tappable; navigates to article detail | ENT-help-centre-content.title |
| — Item Excerpt | text | No | 1-2 line description or preview | Truncated with ellipsis | ENT-help-centre-content.summary |
| — Last Updated | datetime | No | Date content was last published or updated | Relative or short date format | ENT-help-centre-content.updated_at |
| Article Detail — Title | text | Yes | Full article title | Read-only | ENT-help-centre-content.title |
| Article Detail — Body | text | Yes | Full article/guide content (rich text, scrollable) | Read-only; supports formatted text, inline images | ENT-help-centre-content.body |
| Article Detail — "Was this helpful?" | group | Yes | Binary feedback: "Yes" / "No" buttons; displays "Thank you for your feedback" confirmation on tap | Feedback is aggregated at the content level — admin dashboards show total Yes/No counts per article. Individual patient identity is not stored with feedback responses per FR-033 Privacy Rule 2 ("aggregated for patients, not individual user level"). | ENT-help-centre-content.helpfulness_rating |
| Article Detail — Contact Support CTA | link | Conditional | "Still need help? Contact Support" shown after patient taps "No" on helpfulness | Routes to Contact Support form Screen 5 (FR-034) | no graph field (control) |
| Article Detail — Related Articles | list | No | Up to 4 related content items from FR-033 (manual or auto-suggested) | Shown only when FR-033 provides related items, with no minimum; none shown when there are none; may link across content types (e.g., article linking to a related video tutorial); tappable | ENT-help-centre-content.related_content_ids |

**Content Type: Resources (Resource Library)**

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Resource List | list | Yes | List of downloadable resources (PDFs, documents) | Shown after patient selects Resources content type | ENT-help-centre-content |
| — File Title | text | Yes | Resource file title | Tappable; navigates to resource detail | ENT-help-centre-content.title |
| — File Type Icon | icon | Yes | Icon indicating file format (PDF, DOC, etc.) | Visual differentiator by format | ENT-help-centre-content.file_type |
| — File Size | text | Yes | File size display (e.g., "2.4 MB") | Read-only | ENT-help-centre-content.file_size |
| — Last Updated | datetime | No | Date resource was last published or updated | Relative or short date format | ENT-help-centre-content.updated_at |
| Resource Detail — Title | text | Yes | Full resource title | Read-only | ENT-help-centre-content.title |
| Resource Detail — File Preview | group | Yes | In-app preview of the file (PDF viewer, document viewer) | Read-only; scrollable; shows at least the first page | ENT-help-centre-content.attachments |
| Resource Detail — Download Button | action | Yes | Download file to device | Tap initiates download; shows progress indicator; saves to device downloads folder | ENT-help-centre-content.attachments |
| Resource Detail — "Was this helpful?" | group | Yes | Binary feedback on the resource | Same aggregated feedback behavior as articles, including the Contact Support prompt after No | ENT-help-centre-content.helpfulness_rating |

**Content Type: Video Tutorials**

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Video List | list | Yes | List of published video tutorials | Shown after patient selects Videos content type | ENT-help-centre-content |
| — Video Thumbnail | image | Yes | Preview thumbnail of the video | Tappable; navigates to video detail | ENT-help-centre-content.thumbnail_url |
| — Video Title | text | Yes | Video tutorial title | Displayed below or beside thumbnail | ENT-help-centre-content.title |
| — Video Duration | text | Yes | Video length (e.g., "3:45") | Read-only | ENT-help-centre-content.duration |
| — Last Updated | datetime | No | Date video was last published or updated | Relative or short date format | ENT-help-centre-content.updated_at |
| Video Detail — Embedded Player | video | Yes | In-app video player with play/pause, seek, fullscreen controls | Streams video content; supports standard playback controls | ENT-help-centre-content.attachments |
| Video Detail — Title | text | Yes | Full video title | Read-only; displayed below player | ENT-help-centre-content.title |
| Video Detail — Description | text | Yes | Video description (rich text) | Read-only; scrollable | ENT-help-centre-content.body |
| Video Detail — Transcript Link | link | No | Link to view video transcript | Opens transcript in a scrollable text view; accessibility best practice | ENT-help-centre-content.transcript |
| Video Detail — "Was this helpful?" | group | Yes | Binary feedback on the video | Same aggregated feedback behavior as articles, including the Contact Support prompt after No | ENT-help-centre-content.helpfulness_rating |

**General Content List (shared across content types)**

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| No Results State | group | Conditional | Shown when search returns 0 results | "No results for '[query]'. Try different keywords or Contact Support." | no graph field (state message) |
| Empty Content State | group | Conditional | Shown when a content type has no published items | "No [content type] available yet. Check back later or Contact Support." | no graph field (state message) |

**Business Rules**:

- All content data is managed by admins via FR-033 and delivered to patients via FR-035; patients have read-only access with no ability to create, edit, or delete content (FR-033 Rule 2, REQ-033-008) (REQ-035-001)
- Patient content is completely isolated from provider content — patients only see patient-audience content (FR-033 Rule 1, Rule 3, REQ-033-021) (REQ-035-002)
- See REQ-035-036. Search is scoped to the patient audience repository; empty search results must always surface a "Contact Support" path (REQ-035-038).
- "Was this helpful?" feedback is aggregated at the content level — admin dashboards show total Yes/No counts per content item. Per FR-033 Privacy Rule 2, patient analytics are aggregated and not tracked at individual user level. Feedback responses do not store individual patient identity. (REQ-035-007, REQ-035-027)
- Content updates published by admin propagate to patient view within 1 minute (FR-033) (REQ-035-028)
- FAQ content must be displayed in collapsible topic sections per FR-033 REQ-033-006, not as a flat list (REQ-035-003)
- Related content suggestions may cross content types (e.g., an article may link to a related video tutorial); related content is admin-configured in FR-033 and FR-035 shows up to 4 when configured, with no minimum
- The Contact Support prompt follows a No tap on "Was this helpful?" for every content type (FAQ, article, resource, video), and search results are shown on this screen (REQ-035-038)
- When Help Center content is unavailable (API down), display cached content if available or show "Help Center temporarily unavailable" with a retry option (REQ-035-045)

---

### Screen 3: My Support Tickets

**Purpose**: List all support cases submitted by the patient, with ability to create new tickets

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Screen Title | text | Yes | "My Support Tickets" | Displayed at top of screen | no graph field (static text) |
| Back Navigation | action | Yes | Back arrow to return to Help & Support Hub (Screen 1) | Top-left corner | no graph field (control) |
| Create New Ticket Button | action | Yes | Primary CTA to submit a new support request | Opens Contact Support Form (Screen 5); on successful submission, displays confirmation then returns to this ticket list (Screen 3); always visible (REQ-035-086) | no graph field (control) |
| Filter Chips | chips | Yes | Filter ticket list: All, Open, In Progress, Resolved, Closed | "All" is default; tapping a chip filters the list. Resolved and Closed are **separate** chips because Resolved cases still accept patient replies (during the auto-closure window), while Closed cases are read-only (FR-034 REQ-034-003). Filter criteria are owned by FR-022 REQ-022-073. | ENT-support-case.status |
| Ticket Card | group | Yes | Individual support case summary row (tappable) | Tapping navigates to Ticket Detail view (Screen 4) | ENT-support-case |
| — Case ID | text | Yes | Unique case reference (format: CASE-YYYY-#####) | Read-only; displayed in subdued style | ENT-support-case.case_id |
| — Title | text | Yes | Case title of the support request (FR-034 REQ-034-020) | Bold; truncated to 1-2 lines | ENT-support-case.title |
| — Status Badge | badge | Yes | Current lifecycle status: Open, In Progress, Resolved, Closed | Color-coded: Open (blue), In Progress (amber), Resolved (green), Closed (grey) | ENT-support-case.status |
| — Priority Badge | badge | Yes | Priority level: Low, Medium, High, Urgent | Color-coded: Low (grey), Medium (blue), High (orange), Urgent (red); shown alongside status badge for at-a-glance triage awareness | ENT-support-case.priority |
| — Submitted Date | datetime | Yes | Date the ticket was submitted | Short date format | ENT-support-case.submitted_at |
| — Last Updated | datetime | Yes | Timestamp of last activity (admin reply, status change) | Relative format: "2h ago", "Yesterday" | ENT-support-case.last_updated_at |
| Empty State | group | Conditional | Shown when patient has no tickets (or none match filter) | "No support tickets yet. Need help? Tap 'Create New Ticket'." (REQ-035-077) | no graph field (state message) |

**Business Rules**:

- Tickets are ordered by most recently updated (newest activity at top) within each filter tab (REQ-035-046)
- All statuses (Open, In Progress, Resolved, Closed) are visible in "All"; filter chips narrow the view per status group
- Creating a new ticket follows FR-034 Workflow A5: patient enters title (10-200 chars, mandatory), selects category (Technical Issue, Account Access, Payment Question, Booking Issue, General Inquiry, Feature Request, Bug Report, Feedback — "Provider Support" and "Patient Support" are admin-internal categories not shown to patients), enters description (20-5000 chars), selects priority (Low, Medium, High, Urgent), and optionally attaches files (max 5 files, 10 MB each, JPG/PNG/PDF/DOC/DOCX); system creates case with Ticket Source = "Patient App", Submitter Type = "Patient" (FR-034 REQ-034-021, REQ-034-024) (REQ-035-009, REQ-035-010, REQ-035-012, REQ-035-013)
- Patient receives a confirmation email with the case reference number upon submission unless an admin has switched the notice off in the Admin notification settings (FR-030, FR-034 REQ-034-090); the in-app confirmation always shows (FR-020, FR-034 A5 step 11) (REQ-035-055)
- Ticket cards are always tappable regardless of status — patients can view the full thread even for Closed cases (REQ-035-047)
- Resolved cases display a subtle "Auto-closes in X days" indicator to set expectations about the closure window (FR-034 REQ-034-061); on the last day it reads "Auto-closes today", and it is not shown when the closure period is Immediately because there is no Resolved window (REQ-035-048)

---

### Screen 4: Ticket Detail View

**Purpose**: Full support case detail with communication thread and patient reply capability

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Screen Title | text | Yes | Case title (FR-034 REQ-034-020) | Displayed at top of screen | ENT-support-case.title |
| Back Navigation | action | Yes | Back arrow to return to My Support Tickets (Screen 3) | Top-left corner | no graph field (control) |
| Case ID | text | Yes | Unique case reference (CASE-YYYY-#####) | Read-only | ENT-support-case.case_id |
| Status Badge | badge | Yes | Current case status: Open, In Progress, Resolved, Closed | Color-coded per status (same palette as Screen 3) | ENT-support-case.status |
| Priority Badge | badge | Yes | Priority level: Low, Medium, High, Urgent | Color-coded: Low (grey), Medium (blue), High (orange), Urgent (red); read-only | ENT-support-case.priority |
| Case Category | badge | Yes | Selected category (e.g., "Account Access", "Payment Question") | Read-only | ENT-support-case.category |
| Submitted Date | datetime | Yes | Date and time case was submitted | Read-only | ENT-support-case.submitted_at |
| Auto-Closure Countdown | text | Conditional | "This case will close in X days if no further reply" | Shown only when status = Resolved; displays remaining days in auto-closure window (FR-034 REQ-034-061, configurable: Immediately, 3, 7, or 14 days, default 7); on the last day it reads "This case will close today if no further reply"; with Immediately there is no Resolved window, so no countdown is shown. Helps patient understand the urgency of replying if their issue persists. Hidden for Open, In Progress, and Closed statuses. | no graph field (derived; Setting SET-support-case-auto-closure-period) |
| Resolution Summary | text | Conditional | Admin-provided resolution summary displayed when case is resolved or closed (FR-034 REQ-034-059, REQ-034-060) | Read-only; shown only when status = Resolved or Closed and admin has entered a resolution summary. Displayed prominently above the communication thread with a "Resolution" header. The resolution summary is also emailed to the patient when the case becomes Resolved, if the admin left Send Resolution Email checked on the case (FR-034 REQ-034-060, REQ-034-161) and the notification settings allow it (FR-030); the summary always shows here. (REQ-035-070) | ENT-support-case-resolution.resolution_summary |
| Feedback Resolution | badge | Conditional | For feedback/feature request cases only: Implemented, Planned, Declined, Under Review | Read-only; shown only when admin has set a feedback resolution value (FR-034 REQ-034-006) | ENT-support-case.feedback_resolution |
| Your Request — Description | text | Yes | The description the patient wrote when submitting the case | Read-only; shown above the communication thread (REQ-035-017) | ENT-support-case.description |
| Your Request — Attachments | file | Conditional | The files the patient attached when submitting the case | Read-only; shown above the communication thread; tap to view full-size or download | ENT-support-case.attachments |
| Communication Thread | list | Yes | Chronological list of all messages (admin replies + patient messages) | Scrollable; newest message at bottom; messages marked with sender label (You / Support Team) | ENT-support-case-message |
| — Message Sender | text | Yes | Label: "You" for patient messages, "Support Team" for admin replies | Read-only | ENT-support-case-message.sender_type |
| — Message Body | text | Yes | Full message content | Read-only for admin messages; supports plain text | ENT-support-case-message.content |
| — Message Timestamp | datetime | Yes | Date and time message was sent | Relative or absolute format | ENT-support-case-message.sent_at |
| — Attachment | file | Conditional | Attached screenshot or document within message | Read-only; tap to view full-size or download; max 10 MB per file, formats: JPG, PNG, PDF, DOC, DOCX (FR-034 REQ-034-036/037) | ENT-support-case-message.attachments |
| Reply Input Field | text | Conditional | Multi-line text input for patient to reply to admin | Shown when case is Open, In Progress, or **Resolved** (FR-034 REQ-034-026); hidden **only** for Closed cases. Replying to a Resolved case triggers automatic reopening to Open status. A reply that reaches the server after the case has closed is refused with a message and the typed text stays visible for copying (REQ-035-068). | ENT-support-case-message.content |
| Attachment Button | action | Conditional | Button to attach files to reply | Shown alongside Reply Input Field; max 10 MB per file, formats: JPG/PNG/PDF/DOC/DOCX; max 5 files per message; a reply file follows the same virus-scan rules as a case file (REQ-035-014, REQ-035-059). | ENT-support-case-message.attachments |
| Send Reply Button | action | Conditional | Submits patient reply to the case thread | Enabled when reply input is non-empty; hidden for Closed cases; admin notified on send via FR-020 (support.case_user_reply); a reply that cannot be sent right now (device offline, server error, or media storage unavailable) is refused with a retry message and the typed text is kept (REQ-035-066) | no graph field (control) |
| Closed Case Banner | group | Conditional | Informational banner shown when case is Closed | "This case is closed. If you still need help, you can create a new ticket or contact support to request this case be reopened." with "Create New Ticket" link to Screen 5 and "Email support" link that opens an email to the support address (the emergency email setting on Screen 1) with the case ID in the subject; the clause "or contact support to request this case be reopened" and the Email support link are shown only when that setting has a value (the sentence then ends after "create a new ticket"). Provides both paths: new ticket creation (in-app) and case reopening via admin (FR-034 Workflow B3, REQ-034-017). (REQ-035-069) | no graph field (control) |
| Empty Thread State | text | Conditional | Shown when no messages exist yet (case just created) | "Your case has been submitted. Our team will respond within 24 hours on business days." (aligns with FR-034 SC-003) (REQ-035-087) | no graph field (state message) |

**Business Rules**:

- Patients can reply to admin messages when the case is Open, In Progress, or **Resolved** (FR-034 REQ-034-026); **only Closed** cases are fully read-only. This is critical for healthcare — patients must be able to report that a resolved issue has recurred (e.g., post-treatment complications) during the auto-closure window. (REQ-035-018)
- A Closed case that an Admin reopens (FR-034 REQ-034-017) shows again as an Open case with the reply box; see REQ-035-071
- Replying to a Resolved case automatically reopens it to Open status; the patient sees the status badge update immediately and the admin receives a support.case_reopened notice (FR-034 REQ-034-092, FR-030) in addition to the reply notice (REQ-035-019)
- Cases auto-close after 7 days in Resolved status if no patient reply (configurable: Immediately, 3, 7, or 14 days per FR-034 REQ-034-061/062); the patient receives a support.case_closed notification. The auto-closure countdown is visible in the Ticket Detail to set clear expectations. With Immediately there is no Resolved window: the case goes straight to Closed, no countdown or Auto-closes indicator is shown, and the patient uses the Closed Case Banner (reopen request or new ticket). (REQ-035-067)
- Patient replies are added to the shared communication thread; the assigned admin notification for each reply (recipients, content, and whether it can be switched off) is defined in FR-020 REQ-020-111 (support.case_user_reply event) (REQ-035-065)
- Internal admin notes are never shown to the patient — only messages explicitly sent to the patient are visible in the thread (FR-034 REQ-034-013, REQ-034-046) (REQ-035-023)
- Feedback resolution field is only shown for feedback, feature request, or bug report case categories (FR-034 REQ-034-006); values: Implemented, Planned, Declined, Under Review
- Status changes (Open -> In Progress, In Progress -> Resolved, Resolved -> Closed) and admin replies trigger push/email notifications to the patient per FR-020 (support.case_status_changed, support.case_resolved, support.case_closed, support.case_admin_reply) (REQ-035-031)

---

### Screen 5: Contact Support Form

**Purpose**: Structured form for patients to submit new support requests or feedback, creating a tracked case in FR-034

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Screen Title | text | Yes | "Contact Support" | Displayed at top of screen | no graph field (static text) |
| Back Navigation | action | Yes | Back arrow to return to previous screen (Hub or Ticket List) | Top-left corner; prompts "Discard draft?" confirmation if form has unsaved input (REQ-035-057) | no graph field (control) |
| Case Title | text | Yes | Patient-entered title describing their issue (FR-034 REQ-034-020) | Min 10 characters, max 200 characters; no auto-generation; placeholder: "Briefly describe your issue" | ENT-support-case.title |
| Category Picker | dropdown | Yes | Support case category selection | Options: Technical Issue, Account Access, Payment Question, Booking Issue, General Inquiry, Feature Request, Bug Report, Feedback, shown under their current labels (FR-034 REQ-034-030; labels are edited in FR-034 REQ-034-087); preset to Technical Issue when the form is opened from Report a Problem. "Provider Support" and "Patient Support" are admin-internal categories and are never shown to patients, whatever their label. Brief inline description per category to help patients select correctly: Feature Request = "Suggest a new feature or improvement", Bug Report = "Report something that is broken or not working as expected", Feedback = "Share general feedback about your experience". | ENT-support-case.category |
| Description | text | Yes | Detailed description of the issue or feedback | Multi-line input; min 20 characters, max 5000 characters (FR-034 REQ-034-035); placeholder: "Describe your issue in detail so we can help you faster" | ENT-support-case.description |
| Priority Picker | dropdown | Yes | Patient-selected priority level | Options: Low, Medium, High, Urgent (FR-034 REQ-034-031); default: Medium. Brief inline descriptions help patients self-triage: Low = "General question", Medium = "Something isn't working right", High = "Blocking my care or booking", Urgent = "Critical issue needing immediate attention" | ENT-support-case.priority |
| Attachments | file | No | Optional file attachments (screenshots, documents) | Max 5 files per submission, max 10 MB per file; accepted formats: JPG, PNG, PDF, DOC, DOCX (FR-034 REQ-034-036/037); tap to add; shows thumbnail preview with remove option; virus-scanned before acceptance. (REQ-035-088) | ENT-support-case.attachments |
| Submit Button | action | Yes | Submits the support request | Disabled until all required fields pass validation; on tap: creates case (CASE-YYYY-#####), links to patient record via session (FR-034 REQ-034-024), sets Ticket Source = "Patient App" and Submitter Type = "Patient", sends confirmation email unless an admin has switched it off in the Admin notification settings (FR-030, FR-034 REQ-034-090) | ENT-support-case.case_id |
| Cancel / Discard | action | Yes | Cancels form and returns to previous screen | Prompts "Discard this request?" if any field has input; no data saved on cancel (REQ-035-057) | no graph field (control) |

**Business Rules**:

- All fields except Attachments are mandatory; the Submit button remains disabled until Title (>= 10 chars), Category, Description (>= 20 chars), and Priority are all valid (REQ-035-049). A failure found by the server after Submit is covered by Alternative Flow B1 (REQ-035-050).
- Upon successful submission, the system displays a confirmation screen showing the assigned Case ID (CASE-YYYY-#####) and the message "We will respond within 24 hours on business days" (FR-034 SC-003), then navigates to My Support Tickets (Screen 3); the confirmation always shows in the app, whether or not the confirmation email is sent (REQ-035-054)
- File uploads are validated client-side (format + size) before upload and server-side (virus scan + format whitelist) before acceptance (FR-034 REQ-034-036/037); a file that fails the scan is refused with the FR-034 message (REQ-034-106) (REQ-035-058)
- Category selection drives downstream admin routing — this is transparent to the patient but important for response time (REQ-035-053)
- Priority inline descriptions are a healthcare UX pattern to reduce mis-triage; patients in distress tend to over-select "Urgent" without guidance, which degrades response quality for truly urgent cases (REQ-035-051)
- **[Design Addition]** Category inline descriptions (Feature Request, Bug Report, Feedback) help patients distinguish between overlapping categories — all three appear in FR-034 REQ-034-030 but without patient-facing guidance on when to use each (REQ-035-052)

---

## Business Rules

### General Module Rules

- **Rule 1**: See REQ-035-001.
- **Rule 2**: See REQ-035-002.
- **Rule 3**: See REQ-035-010.
- **Rule 4**: See REQ-035-028.
- **Rule 5**: All timestamps displayed in user's local timezone (REQ-035-035)
- **Search**: Full-text search, relevance ordering, and inline suggestions are required for the patient Help Center MVP scope. (REQ-035-037)
- **Caching**: Help Center content should be cached locally on the patient device to support offline browsing and reduce API load. Cache invalidation should respect the 1-minute content propagation SLA from FR-033. (REQ-035-045, REQ-035-028)
- **Media Storage Service (S-05) failure handling**: for file uploads, the case is created without the files, the files are queued for retry, and the patient is told of the delay (REQ-035-061)
- **FR-034 Ticketing API error handling**: Retry with exponential backoff on 5xx errors; a submission that cannot be sent (offline or server error) is queued and shows "queued, will be sent when online", and it gets its Case ID after it is sent; only one request waits in the queue at a time (a second submit is refused with a message to wait until the first is sent), and one not sent within 24 hours is reported to the patient as not sent, with the text kept so it can be sent again (REQ-035-062)
- **FR-020/S-03 Notification Service error handling**: Notification delivery failures do not block case operations; retry asynchronously (REQ-035-064)
- **Threat mitigation**: Rate limiting on new ticket submissions (max 10 new tickets per hour per patient; the patient sees a wait message); replies are not counted by this limit; file upload virus scanning (when the scanner is unavailable the file is refused with a "try again later" message and the case or reply can be sent without it); input sanitization for all text fields (REQ-035-063, REQ-035-089, REQ-035-014)
- Admin team responds to patient support cases within 24 hours on business days (FR-034 SC-003); every patient-facing line says "within 24 hours on business days"
- Help Center content is curated to avoid medical advice and focus on platform usage, appointment management, and general information (FR-033 Assumption 5)

### Data & Privacy Rules

- **Privacy Rule 1**: See REQ-035-007 and REQ-035-027.
- **Privacy Rule 2**: See REQ-035-023.
- **Privacy Rule 3**: Patient support case data is accessible only to the submitting patient and authorized admin staff (REQ-035-072)
- **Privacy Rule 4**: File attachments in support cases are virus-scanned before acceptance and encrypted at rest (REQ-035-014)
- **Audit Rule**: All support case lifecycle events (creation, status changes, messages, attachments) are logged with timestamp and user ID in FR-034 case timeline (REQ-035-073)
- **Audit trail**: All support case lifecycle events logged with timestamp, patient ID, and action type (managed by FR-034) (REQ-035-073)
- **Compliance**: Patient support data handling follows the same HIPAA/GDPR compliance requirements as all patient data in the platform (REQ-035-074)

### Admin Editability Rules

**Editable by Admin**:

- Help Center content (FAQs, articles, resources, videos) — managed via FR-033
- Support case status, assignment, resolution — managed via FR-034
- Auto-closure period for resolved cases (Immediately, 3, 7, or 14 days, default 7 days) — configured via FR-034
- Emergency contact phone number and email — two App Settings owned by FR-026; at least one must stay set
- Help Centre content category descriptions shown to patients — managed via FR-033

**Fixed in Codebase (Not Editable)**:

- 4 content types for patient platform: FAQs, Articles, Resources, Videos (FR-033 REQ-033-003) (REQ-035-042)
- Support case lifecycle workflow: Open -> In Progress -> Resolved -> Closed (fixed in the codebase, not editable by admin); it moves forward only, except that a patient reply reopens a Resolved case (REQ-035-019) and an Admin can reopen a Closed case (FR-034 REQ-034-017), after which the patient sees the case as Open with the reply box again and receives the FR-034 reopen notice (REQ-034-163) (REQ-035-071)
- Case ID format: CASE-YYYY-##### (REQ-035-056)
- File attachment limits: max 10 MB per file, max 5 files per message, formats: JPG/PNG/PDF/DOC/DOCX (REQ-035-013)
- Contact Support form validation: title min 10 chars, description min 20 chars (REQ-035-009)

**Configurable with Restrictions**:

- Patient-visible support categories (admin cannot add or remove categories from the fixed list; the labels are editable in FR-034 REQ-034-087, the picker shows the current label, and the two internal categories stay hidden whatever their label) (REQ-035-076)

**Carried from dropped sections (original wording)**:

- **Assumption 3**: Emergency contact phone and email values are configured by admin before FR-035 goes live

---

## Dependencies

- **FR-033**: Help Centre Content Management; patient-specific content consumed read-only, updates propagate within 1 minute.
- **FR-034**: Support Center & Ticketing System; creates support cases and provides the two-way communication thread.
- **FR-020**: Notifications & Alerts; push and email notifications for support case updates.
- **FR-001**: Patient Authentication & Profile; authenticated session provides the patient ID.
- **FR-026**: App Settings & Security; Settings screen entry point and emergency contact settings; the settings screen must refuse to save both support contact values (phone and email) blank, so at least one always has a value.

---

## User Scenarios & Testing

### User Story 1 - Patient Finds Answer via Help Center (Priority: P1)

A patient who has questions about post-treatment hair care navigates to the Help Center from their Settings screen, browses the FAQs section, expands the relevant topic, and finds the answer they need — all without submitting a support ticket.

**Why this priority**: Self-service content access is the primary value proposition of the Help Center and the most common user journey. Deflecting support tickets directly reduces operational costs.

**Independent Test**: Can be fully tested by navigating to Help Center, browsing content types, viewing content detail, and submitting "Was this helpful?" feedback.

**Acceptance Scenarios**:

1. **Given** a patient is on the Settings screen, **When** they tap "Help & Support", **Then** the Help & Support Hub (Screen 1) is displayed with search bar, Help Center link, Contact Support link, My Support Tickets link, and Emergency Contact section
2. **Given** a patient is on the Help & Support Hub, **When** they tap "Help Center", **Then** the Help Center Browser (Screen 2) is displayed with 4 content type cards (FAQs, Articles, Resources, Videos)
3. **Given** a patient selects the FAQs content type, **When** the FAQ list loads, **Then** FAQs are displayed in collapsible accordion sections organized by admin-defined topics (FR-033 REQ-033-006)
4. **Given** a patient reads an FAQ answer, **When** they tap "Yes" on "Was this helpful?", **Then** the system logs aggregated positive feedback and displays "Thank you for your feedback"

---

### User Story 2 - Patient Submits Support Request (Priority: P1)

A patient encountering a payment issue cannot find an answer in the Help Center, so they navigate to Contact Support, fill out the form with their issue details, and submit it. They receive a confirmation with a case ID and can immediately see their new ticket in My Support Tickets.

**Why this priority**: Support ticket submission is the core fallback when self-service fails. Without it, patients have no in-app support path, which is unacceptable for a healthcare platform.

**Independent Test**: Can be fully tested by submitting a support request and verifying case creation in FR-034, confirmation display, and ticket appearance in My Support Tickets list.

**Acceptance Scenarios**:

1. **Given** a patient is on the Help & Support Hub, **When** they tap "Contact Support", **Then** the Contact Support form (Screen 5) is displayed with title, category, description, priority, and attachment fields
2. **Given** a patient fills all required fields (title >= 10 chars, category selected, description >= 20 chars, priority selected), **When** they tap Submit, **Then** the system creates a support case in FR-034 with CASE-YYYY-##### ID, Ticket Source = "Patient App", Submitter Type = "Patient"
3. **Given** a support case is created successfully, **When** submission completes, **Then** the patient sees a confirmation screen with the Case ID and "We will respond within 24 hours on business days", and is navigated to My Support Tickets (Screen 3)
4. **Given** a patient has submitted a support request, **When** they view My Support Tickets, **Then** the new ticket appears at the top with status "Open" and the submitted details

---

### User Story 3 - Patient Communicates with Admin via Ticket Thread (Priority: P2)

A patient who submitted a support request receives a notification that admin has replied. They open the ticket, read the admin's response, type a follow-up question, and send it — continuing the conversation thread.

**Why this priority**: Two-way communication is essential for resolving complex support issues. Without it, patients must rely on external email for follow-ups, breaking the in-app experience.

**Independent Test**: Can be tested by viewing an existing ticket with admin replies, sending a patient reply, and verifying the reply appears in the thread and admin is notified.

**Acceptance Scenarios**:

1. **Given** a patient has a ticket with an admin reply, **When** they open the Ticket Detail (Screen 4), **Then** the communication thread shows all messages chronologically with sender labels ("You" / "Support Team") and timestamps
2. **Given** a patient is viewing a ticket with status Open or In Progress, **When** they type a reply and tap Send, **Then** the reply is added to the communication thread and the admin receives a support.case_user_reply notification
3. **Given** a patient is viewing a ticket with status Resolved, **When** they type and send a reply, **Then** the case automatically reopens to Open status, the status badge updates immediately, and the admin is notified

---

### User Story 4 - Patient Views Resolved Case with Auto-Closure (Priority: P2)

A patient's support case has been resolved by admin. The patient views the resolution summary, sees the auto-closure countdown, and decides whether to accept the resolution or reply to reopen the case.

**Why this priority**: The resolve-to-close lifecycle with auto-closure is critical for healthcare — patients must have a clear window to report recurring issues (e.g., post-treatment complications).

**Independent Test**: Can be tested by viewing a Resolved ticket showing resolution summary and auto-closure countdown, then either letting it auto-close or replying to reopen.

**Acceptance Scenarios**:

1. **Given** a patient has a ticket with status Resolved, **When** they open the Ticket Detail, **Then** they see the resolution summary above the thread and an auto-closure countdown ("This case will close in X days if no further reply")
2. **Given** a Resolved ticket's auto-closure period expires (7 days default), **When** the patient has not replied, **Then** the case automatically transitions to Closed and the patient receives a support.case_closed notification
3. **Given** a patient has a Closed ticket, **When** they open the Ticket Detail, **Then** the reply input is hidden and a Closed Case Banner is shown with the option to create a new ticket and, when the support email setting has a value, to email support to ask for a reopen

---

### User Story 5 - Patient Browses Video Tutorials and Downloads Resources (Priority: P3)

A patient preparing for their upcoming procedure browses the Help Center for educational content. They watch a video tutorial on post-treatment care and download a PDF guide for reference.

**Why this priority**: Rich content types (videos, resources) enhance the self-service experience but are secondary to core FAQ/article browsing and support ticket functionality.

**Independent Test**: Can be tested by navigating to Videos content type, playing a video, navigating to Resources, and downloading a PDF.

**Acceptance Scenarios**:

1. **Given** a patient selects the Videos content type, **When** the video list loads, **Then** each video shows thumbnail, title, and duration
2. **Given** a patient taps a video, **When** the video detail loads, **Then** the embedded player plays the video with standard controls (play/pause, seek, fullscreen) and shows title, description, and transcript link
3. **Given** a patient selects the Resources content type and taps a resource, **When** the resource detail loads, **Then** a file preview is shown with a download button, and tapping download saves the file to the device

---

### Edge Cases

- What happens when a patient submits a support request while offline? The submission is queued on the device and shows "queued, will be sent when online"; it is sent when connectivity returns and gets its Case ID then; only one request waits in the queue at a time (a second submit is refused with a message to wait until the first is sent), and one not sent within 24 hours is reported as not sent, with the text kept so it can be sent again (Alternative Flow B3). (REQ-035-062)
- How does the system handle a patient who uploads a file that fails virus scanning? The file is refused with the FR-034 message (REQ-034-106), and the patient can send the case or reply without it. (REQ-035-059)
- What happens when a patient views Help Center with no published content (e.g., first launch before admin populates content)? Each content type card shows "No content available yet. Check back later or Contact Support." (REQ-035-043)
- How does the system handle a patient deleting their account while support cases are active? Open, In Progress, and Resolved cases stay with the Admin, marked "Patient Account Deleted" (FR-034 REQ-034-109), and notices to the deleted patient stop; patient identity is anonymized per data retention policy (FR-023). (REQ-035-075)
- What happens when the auto-closure countdown reaches 0 while the patient is actively viewing the ticket? The screen learns of the closure on its next refresh or when the patient sends a reply; a reply sent after closure is refused with a message, the typed text stays visible for copying, and the Closed Case Banner replaces the reply input (Alternative Flow A6). (REQ-035-068)

---

## Functional Requirements Summary

### Core Requirements

- **REQ-035-001**: System MUST display patient-specific Help Center content (FAQs, Articles, Resources, Videos) managed by admins in FR-033 as read-only resources (FR-033 REQ-033-003, REQ-033-008)
- **REQ-035-002**: System MUST enforce content isolation — patients see only patient-audience content, never provider content (FR-033 REQ-033-021)
- **REQ-035-003**: System MUST display FAQ content in collapsible accordion sections organized by admin-defined topics (FR-033 REQ-033-006)
- **REQ-035-004**: System MUST display article content with subtype filtering (Tutorial Guides, Troubleshooting Tips)
- **REQ-035-005**: System MUST support in-app video playback for video tutorials with play/pause, seek, and fullscreen controls
- **REQ-035-006**: System MUST support in-app file preview and download for resource documents
- **REQ-035-007**: System MUST provide "Was this helpful?" binary feedback on all content types, with feedback aggregated anonymously at the content level (FR-033 Privacy Rule 2)
- **REQ-035-008**: System MUST display up to 4 related content suggestions when FR-033 configures them (no minimum; none when none are configured); suggestions may cross content types

### Support Submission Requirements

- **REQ-035-009**: System MUST allow patients to submit support requests via Contact Support form with title (10-200 chars), category, description (20-5000 chars), priority, and optional file attachments (FR-034 REQ-034-020, REQ-034-030, REQ-034-031, REQ-034-035)
- **REQ-035-010**: System MUST automatically create support cases in FR-034 with Ticket Source = "Patient App" and Submitter Type = "Patient" on form submission (FR-034 REQ-034-021, REQ-034-024)
- **REQ-035-011**: System MUST link patient-submitted cases to patient records using logged-in patient session (FR-034 REQ-034-024)
- **REQ-035-012**: System MUST display 8 patient-visible categories under their current labels: Technical Issue, Account Access, Payment Question, Booking Issue, General Inquiry, Feature Request, Bug Report, Feedback (FR-034 REQ-034-030; labels edited in FR-034 REQ-034-087; "Provider Support" and "Patient Support" excluded as admin-internal whatever their label)
- **REQ-035-013**: System MUST support file attachments up to 10 MB per file, maximum 5 files per message (the initial request and each reply may each carry up to 5 files), formats: JPG, PNG, PDF, DOC, DOCX (FR-034 REQ-034-036/037)
- **REQ-035-014**: System MUST virus-scan all patient-uploaded files before acceptance; when the scanner is unavailable the file is refused with a "try again later" message and the case or reply can be sent without it; a file attached to a reply follows the same scan rules as a file attached to a new case

### Ticket Management Requirements

- **REQ-035-015**: System MUST display patient's submitted support tickets with case ID, title, status (Open/In Progress/Resolved/Closed), priority, submitted date, and last updated timestamp
- **REQ-035-016**: Retired. The patient ticket status filter (All, Open, In Progress, Resolved, Closed) is owned by FR-022 REQ-022-073
- **REQ-035-017**: System MUST display the patient's original request (description and initial attachments) and the full communication thread for each ticket showing all messages from patient and admin with sender labels and timestamps
- **REQ-035-018**: System MUST allow patients to reply to admin messages when case is Open, In Progress, or Resolved (FR-034 REQ-034-026); reply input hidden only for Closed cases
- **REQ-035-019**: System MUST automatically reopen Resolved cases to Open status when patient sends a reply, and send the admin a support.case_reopened notice (FR-034 REQ-034-092)
- **REQ-035-020**: System MUST display auto-closure countdown on Resolved tickets showing remaining days before automatic closure (FR-034 REQ-034-061); "closes today" on the last day; none when the closure period is Immediately
- **REQ-035-021**: System MUST display resolution summary when admin has provided one (FR-034 REQ-034-059, REQ-034-060)
- **REQ-035-022**: System MUST display Feedback Resolution status (Implemented, Planned, Declined, Under Review) for feedback/feature request/bug report cases when set by admin (FR-034 REQ-034-006)
- **REQ-035-023**: System MUST hide internal admin notes from patient view — only messages explicitly sent to the patient are visible (FR-034 REQ-034-013, REQ-034-046)

### Security & Privacy Requirements

- **REQ-035-024**: System MUST require patient authentication to access Help Center content, submit support requests, and view tickets; a person who is not logged in sees only the support contact details (phone and email), with no case and no help content
- **REQ-035-025**: System MUST ensure patients can only view their own support cases — no access to other patients' cases
- **REQ-035-026**: Retired. Encryption in transit and at rest (TLS 1.3, AES-256) is recorded once in the system PRD security requirements, which this module follows
- **REQ-035-027**: System MUST aggregate "Was this helpful?" feedback without storing individual patient identity (FR-033 Privacy Rule 2)

### Integration Requirements

- **REQ-035-028**: System MUST consume patient-specific Help Center content from FR-033 REST API with content updates reflected within 1 minute of admin publishing
- **REQ-035-029**: System MUST create support cases via FR-034 Ticketing API on patient form submission
- **REQ-035-030**: System MUST receive and display case status updates, admin replies, and resolution summaries from FR-034
- **REQ-035-031**: System MUST trigger patient notifications via FR-020/S-03 for case status changes, admin replies (support.case_admin_reply), and case closure

### Marking Unclear Requirements

- **REQ-035-032**: Retired. The attachment limit is settled in REQ-035-013: up to 5 files per message, replies included.

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-11-22 | 1.2 | Requirements graph programme baseline: PRD compressed to the checklist structure (each rule stated once, field rows tagged with graph field ids, dropped classes removed). No rule changes. Earlier history (v1.0 to v1.1) is in `archived/prd-baseline-2026-11-08/` and in git history. | Product Owner / Documentation |
| 2026-11-23 | 1.3 | Independent compression review: 1 clause(s) from dropped sections restored in original wording under Business Rules. No rule changes. | Product Owner / Documentation |
| 2026-11-24 | 1.4 | Logic review pass 1: not-logged-in view, Report a Problem entry, optional emergency rows, Immediately closure (no Resolved window), notification-setting wording, new flows A6 (Resolved case closes) and B3 (submission cannot complete now), reopen notice, original request shown on Ticket Detail, refusal of a reply sent after closure, related content up to 4, single "within 24 hours on business days" wording. See update log FR035_LOGIC_REVIEW_PASS_1_2026-11-24. | Product Owner / Documentation |
| 2026-11-24 | 1.5 | Logic review pass 2: Closed Case Banner email link shown only with a support email, at least one support contact value always set (FR-026), Resolved case from the list reaches the reopen path, reply failure rule, offline queue limit (one request, 24 hours), resolution email switch named as in FR-034, lifecycle moves back (patient reply, Admin reopen), Report a Problem preset, notice stop for deleted patients on flow A6, failed virus scan branch, notice tap entry. See update log FR035_LOGIC_REVIEW_PASS_2_2026-11-24. | Product Owner / Documentation |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|---------------------|

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-035 from system-prd.md, FR-033 Help Centre Content Management, FR-034 Support Center & Ticketing System
**Last Updated**: 2026-11-24
