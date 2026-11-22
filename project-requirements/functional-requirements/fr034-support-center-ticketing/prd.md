# FR-034 - Support Center & Ticketing System

**Module**: A-10: Communication Monitoring & Support | A-01: Patient Management & Oversight
**Feature Branch**: `fr034-support-center-ticketing`
**Created**: December 30, 2025
**Status**: ✅ Verified & Approved
**Source**: FR-034 from system-prd.md, Client transcription (Hairline-AdminPlatform-Part1.txt)

---

## Executive Summary

The Support Center & Ticketing System provides a unified formal support system for managing both patient and provider inquiries, technical issues, feedback submissions, and general support requests. This module enables Hairline admin staff to create, track, and resolve support cases systematically across all platform tenants, ensuring consistent service quality and maintaining comprehensive audit trails for compliance and dispute resolution.

**Purpose**: This feature establishes a structured support case management system to handle user questions and issues from THREE sources:

1. **Patient Submissions** (via FR-035): Patients submit support requests, questions, and feedback through the patient mobile app
2. **Provider Submissions** (via FR-032): Providers submit support requests and feedback/suggestions through the provider Help Centre
3. **Manual Admin Entry**: Admin staff manually create cases for inquiries received via email, phone, or other external channels

**Common support scenarios include**:

- "I don't understand how this works"
- "This feature is not working for me"
- Payment or booking clarification questions
- Account access issues
- General platform navigation help
- Feature requests and product feedback
- Bug reports and technical issues

**Problem Solved**: Without a formal unified support system, patient and provider inquiries risk being lost, duplicated, or inconsistently resolved. This module ensures every support request from any source is tracked, prioritized, assigned, and resolved with complete accountability and auditability.

**Business Value**:

- **Improved User Satisfaction**: Faster, more consistent support response times for both patients and providers
- **Operational Efficiency**: Centralized support case tracking across all tenants reduces staff workload and prevents duplicate efforts
- **Unified Workflow**: Single consistent status workflow (Open → In Progress → Resolved → Closed) for all ticket types
- **Feedback Management**: Optional Feedback Resolution tracking (Implemented, Planned, Declined, Under Review) for feature requests and suggestions
- **Compliance & Audit Trail**: Immutable case history supports dispute resolution and regulatory compliance

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-08)**: Patient-facing support ticket submission UI accessible from patient app Help Center (FR-035: Patient Help Center & Support Submission); patients can submit support requests and feedback directly from patient mobile app
- **Provider Platform (PR-06)**: Provider-facing support ticket and feedback submission UI accessible from Help Centre (FR-032 Screen 5.5 and 5.6); providers can submit support requests and feedback directly from provider platform
- **Admin Platform (A-10, A-01)**: Core support case management interface for admin staff to intake, track, categorize, prioritize, assign, and resolve support cases for both patient and provider inquiries from all sources (patient app, provider portal, manual admin entry)
- **Shared Services (S-03)**: Notification Service used to send status updates and replies to patients/providers via email

### Multi-Tenant Breakdown

**Patient Platform (P-08)**:

- Patients can submit support requests and feedback via FR-035 (Patient Help Center & Support Submission) accessible from patient mobile app
- Patients can view their submitted cases with full case details including status, feedback resolution (if applicable), and complete communication thread
- Patients can reply to admin messages within the case, enabling two-way threaded communication
- Patients receive email notifications when admin responds to their submissions or updates status
- Patient submissions automatically create support cases in FR-034 with unified status workflow
- Submission types include: Technical issues, account questions, booking help, general inquiries, feedback, and feature requests

**Provider Platform (PR-06)**:

- Providers can submit support requests via Contact Support form (FR-032 Screen 5.5) accessible from Help Centre
- Providers can submit feedback and suggestions via Feedback & Suggestions form (FR-032 Screen 5.6) accessible from Help Centre
- Providers can view their submitted cases with full case details including status, feedback resolution (if applicable), and complete communication thread
- Providers can reply to admin messages within the case, enabling two-way threaded communication
- Providers receive email notifications when admin responds to their submissions or updates status

**Admin Platform (A-10: Communication Monitoring & Support)**:

- Admin staff create support cases manually (from incoming emails, phone calls, chat messages) OR cases are automatically created from patient app submissions (FR-035) or provider portal submissions (FR-032)
- Admin staff view and manage patient support requests submitted through patient app (FR-035)
- Admin staff view and manage provider support requests submitted through Help Centre Contact Support form (FR-032 Screen 5.5)
- Admin staff view and manage patient and provider feedback submissions (FR-035 and FR-032 Screen 5.6)
- Admin staff categorize cases using centralized managed category list (Technical Issue, Account Access, Payment Question, Booking Issue, General Inquiry, Provider Support, Feature Request, Bug Report, Patient Support, Feedback)
- Admin staff set case priority using centralized managed priority list (Low, Medium, High, Urgent)
- Admin staff assign cases to specific support team members for informational purposes only (all admins can view and work on all cases regardless of assignment)
- Admin staff track case lifecycle with **unified status workflow**: Open → In Progress → Resolved → Closed (consistent across all ticket types and sources)
- Admin staff track **Feedback Resolution** for feedback/feature request tickets: Implemented, Planned, Declined, Under Review (optional field)
- Admin staff view comprehensive case timeline showing all events with full context: messages from admin/patient/provider, status changes, feedback resolution updates, internal notes, attachments, and account interventions
- Admin staff can engage in two-way threaded communication with patients and providers within case timeline
- Admin staff can identify **Ticket Source** (Patient App, Provider Portal, Manual Admin Entry) and **Submitter Type** (Patient, Provider, Admin)
- Admin staff link cases to specific patient records (by Hairline Patient ID, email, or phone number) or provider records to enable context and deep-linking to account management modules
- Admin staff can deep-link from linked cases to patient management module (A-01) or provider management module (A-02) for account interventions
- Admin staff reassign cases to other team members with reason tracking
- Admin staff reopen closed cases if patient/provider indicates issue not resolved

**Admin Platform (A-01: Patient Management & Oversight)**:

- Admins accessing patient records can view linked support cases for that patient (REQ-034-073)
- Support case context appears in patient detail view (e.g., "3 open support cases" with links) (REQ-034-073)
- Admins can initiate account interventions (password reset, account suspension) directly from support cases (REQ-034-074)

**Shared Services (S-03: Notification Service)**:

- Sends email notifications to patients when:
  - Support case is created (optional confirmation)
  - Support case status changes (Open → In Progress, In Progress → Resolved)
  - Admin replies to patient inquiry
  - Case is closed with resolution summary
- Sends email notifications to providers when:
  - Support case is created for their inquiry
  - Support case status changes
  - Admin replies to provider question
  - Case is resolved
  - Case is closed

### Communication Structure

**In Scope**:

- Admin-to-patient email notifications for support case updates (via S-03)
- Admin-to-provider email notifications for support case updates (via S-03)
- Internal admin notes within support cases (not visible to patients/providers)
- Admin-to-admin case assignment notifications
- Case timeline with complete message history
- Attachment support for case communications (screenshots, documents)

**Out of Scope**: (REQ-034-076)

- Real-time in-app chat between patient and admin (future enhancement)
- Real-time in-app chat between provider and admin (future enhancement)
- Aftercare-specific communications (handled by FR-011: Aftercare & Recovery Management)
- Provider ↔ Patient secure messaging (handled by FR-012: Secure Messaging)
- Video consultations for support (future enhancement)
- SMS notifications for support case updates (future enhancement - S-03 SMS integration)
- Phone call integration or VoIP (future enhancement)

### Entry Points

**Patient App Entry**:

- Patients access Contact Support and Feedback submission forms from patient app Help Center (FR-035: Patient Help Center & Support Submission) (REQ-034-070)
- Patient submissions automatically create support cases in FR-034 system with unified status workflow
- Patients can view status of their submitted tickets in patient app

**Provider Platform Entry**:

- Providers access Contact Support form from Help Centre (FR-032 Screen 5.5) to submit support requests (REQ-034-070)
- Providers access Feedback & Suggestions form from Help Centre (FR-032 Screen 5.6) to submit feedback (REQ-034-070)
- Provider submissions automatically create support cases in FR-034 system with unified status workflow

**Admin Platform Entry**:

- Admin staff access Support Center module from main admin navigation menu (REQ-034-070)
- Default view shows case listing screen with all cases (Open and In Progress by default) (REQ-034-070)
- All admin staff can view all cases regardless of assignment (assignment is informational only)
- Admin receives email notification when new support case is created or assigned to them (REQ-034-071)
- Admin can create new support case manually from case listing screen via "Create New Case" button (REQ-034-070)
- Super Admin accesses Support Center Configuration via Settings > Support Center path to manage centralized lists (categories, priorities, resolution categories, root causes, tags) (REQ-034-070)

**System-Triggered Entry**:

- System automatically creates support case when patient submits Contact Support or Feedback request via patient app (FR-035)
- System automatically creates support case when provider submits Contact Support request via Help Centre (FR-032 Screen 5.5)
- System automatically creates support case when provider submits Feedback & Suggestions via Help Centre (FR-032 Screen 5.6)
- Admin creates support case when patient or provider contacts via email (manual case creation from email content)
- Admin creates support case when patient or provider contacts via phone (manual case entry after call)

**Integration Entry**:

- Support cases linkable from patient management module (A-01) - admins view patient's support history (REQ-034-073)
- Support cases linkable from provider management module (A-02) - admins view provider's support history (REQ-034-073)
- Deep-link from support case to patient/provider record for account interventions

---

## Business Workflows

### Main Flow: Patient Support Case Lifecycle

**Actors**: Admin Staff, Patient (external), System, S-03 Notification Service  
**Trigger**: Patient contacts Hairline via email, phone, or external channel with support inquiry  
**Outcome**: Support case created, tracked, resolved, and closed with complete audit trail

**Steps**:

1. **Admin Staff** receives patient inquiry via email, phone, or other external channel
2. **Admin Staff** logs into Admin Platform and navigates to Support Center module
3. **Admin Staff** clicks "Create New Support Case" button
4. **System** displays case creation form
5. **Admin Staff** enters case details:
   - **Case Title**: Brief description (e.g., "Cannot login to account")
   - **Category**: Selects from the master category list of ten (for example Technical Issue, Account Access, Payment Question, Booking Issue, General Inquiry)
   - **Priority**: Sets priority level (Low, Medium, High, Urgent)
   - **Patient Identifier**: Links case to patient by HPID, email, or phone number
   - **Description**: Full details of patient's inquiry or issue
   - **Attachments**: Uploads any relevant screenshots or documents patient provided
6. **System** validates inputs and creates support case record with status "Open" (REQ-034-096)
7. **System** assigns unique case ID (e.g., "CASE-2025-12345")
8. **System** records case creation timestamp and admin user who created it (REQ-034-097)
9. **Admin Staff** assigns case to appropriate team member or department
10. **System** sends email notification to assigned admin staff member
11. **System** optionally sends confirmation email to patient (via S-03) acknowledging case creation
12. **Assigned Admin Staff** reviews case details and changes status to "In Progress"
13. **System** logs status change in case timeline
14. **Assigned Admin Staff** investigates issue and communicates with patient via email
15. **Admin Staff** adds internal notes to case (e.g., "Password reset completed")
16. **Admin Staff** updates case status to "Resolved" once issue is fixed
17. **System** logs resolution timestamp and sends email to patient with resolution summary (via S-03)
18. **Admin Staff** closes case after confirming patient satisfaction or after 7-day auto-close period
19. **System** sets case status to "Closed" and marks case lifecycle complete
20. **System** archives case data with immutable audit trail for compliance retention

### Alternative Flows

**A1: Case Requires Escalation**:

- **Trigger**: Admin determines case requires senior staff or technical team involvement (applies equally to patient-submitted and provider-submitted cases)
- **Steps**:
  1. Admin clicks "Reassign Case" (there is no separate escalation button or form) (REQ-034-103)
  2. System displays the Reassign Case modal (Screen 5)
  3. Admin selects the new assignee, enters the required reassignment reason, and ticks "Escalate"
  4. System raises case priority to "High" or "Urgent" as the admin chooses
  5. System sends the escalation notice to the new assignee
  6. System logs the reassignment in case timeline, marked as an escalation
- **Outcome**: Case reassigned to higher-level support staff with increased priority (REQ-034-103)

**A2: Case Requires Patient Account Intervention**:

- **Trigger**: Admin needs to reset patient password, suspend account, or modify patient data
- **Steps**:
  1. Admin clicks "View Patient Record" link in support case
  2. System deep-links to patient management module (A-01) with patient HPID pre-filled
  3. Admin performs account intervention (password reset, account unlock, data correction)
  4. Admin returns to support case and adds note documenting intervention
  5. System logs intervention in both support case timeline and patient account audit trail (REQ-034-074)
- **Outcome**: Patient account issue resolved with audit trail across both modules

**A3: Provider Submits Contact Support Request via Help Centre**:

- **Trigger**: Provider needs direct assistance and submits support request through Help Centre (FR-032 Screen 5.5)
- **Steps**:
  1. Provider navigates to Help Centre and selects "Contact Support" subscreen (FR-032 Screen 5.5)
  2. System displays support request form (subject, category, message, priority, optional attachment)
  3. Provider completes form with support request details and submits
  4. System validates form fields and automatically creates support case with unique case ID (CASE-YYYY-#####)
  5. System links case to provider record (provider ID automatically linked from logged-in provider session)
  6. System sets case category based on provider's selection (Technical Issue, Account Access, Payment Question, Booking Issue, General Inquiry, Provider Support: the six provider categories, a subset of the ten-category master list) (REQ-034-101)
  7. System sets case priority based on provider's selection (Low, Medium, High, Urgent) (REQ-034-101)
  8. System sets case status to "Open" and routes it to the Support Staff pool (team is a routing label only) (REQ-034-100)
  9. System sets Ticket Source to "Provider Portal" and Submitter Type to "Provider"
  10. System displays confirmation to provider: "Support request submitted. Case #[number]. Our team will respond within 24 hours." (REQ-034-098)
  11. System sends confirmation email to provider with case reference number (via S-03) (REQ-034-099)
  12. System sends notification to the Support Staff pool (REQ-034-099)
  13. Admin reviews case in Support Center, updates status (Open → In Progress → Resolved → Closed), and responds
  14. Provider can view case status and admin responses in their Contact Support subscreen (FR-032 Screen 5.5)
- **Outcome**: Provider support request automatically creates support case, tracked and managed in FR-034 with unified status workflow

**A4: Provider Submits Feedback & Suggestions via Help Centre**:

- **Trigger**: Provider wants to submit feedback or suggestion through Help Centre (FR-032 Screen 5.6)
- **Steps**:
  1. Provider navigates to Help Centre and selects "Feedback & Suggestions" subscreen (FR-032 Screen 5.6)
  2. System displays feedback submission form (feedback type, title, description, priority)
  3. Provider completes form with feedback details and submits
  4. System validates form fields and automatically creates support case with unique case ID (CASE-YYYY-#####)
  5. System links case to provider record (provider ID automatically linked from logged-in provider session)
  6. System sets case category from the feedback type: Feature Request and Bug Report keep their own categories; Suggestion and Other are filed under category Feedback (no new categories) (REQ-034-101)
  7. System sets case priority based on provider's suggested priority (Low, Medium, High, Urgent) (REQ-034-101)
  8. System sets case status to "Open" and routes it to the Support Staff pool (team is a routing label only) (REQ-034-100)
  9. System sets Ticket Source to "Provider Portal" and Submitter Type to "Provider"
  10. System displays confirmation to provider: "Thank you for your feedback! Case #[number]. We'll review your submission." (REQ-034-098)
  11. System sends confirmation email to provider with case reference number (via S-03) (REQ-034-099)
  12. System sends notification to the Support Staff pool (REQ-034-099)
  13. Admin reviews feedback in Support Center, updates status (Open → In Progress → Resolved → Closed), sets Feedback Resolution (Implemented, Planned, Declined, Under Review), and optionally responds
  14. Provider can view submission status and feedback resolution in their Feedback & Suggestions subscreen (FR-032 Screen 5.6)
- **Outcome**: Provider feedback automatically creates support case, tracked and managed in FR-034 with unified status workflow and feedback resolution tracking

**A5: Patient Submits Support Request or Feedback via Patient App**:

- **Trigger**: Patient needs assistance or wants to submit feedback through patient app (FR-035: Patient Help Center & Support Submission)
- **Steps**:
  1. Patient navigates to Help Center in patient mobile app and selects "Contact Support" or "Submit Feedback" (FR-035)
  2. System displays submission form (subject, category, message, priority, optional attachment)
  3. Patient completes form with support request or feedback details and submits
  4. System validates form fields and automatically creates support case with unique case ID (CASE-YYYY-#####)
  5. System links case to patient record (patient ID automatically linked from logged-in patient session)
  6. System sets case category based on patient's selection (Technical Issue, Account Access, Payment Question, Booking Issue, General Inquiry, Feature Request, Bug Report, Feedback: the eight patient categories, a subset of the ten-category master list) (REQ-034-101)
  7. System sets case priority based on patient's selection (Low, Medium, High, Urgent) (REQ-034-101)
  8. System sets case status to "Open" and routes it to the Support Staff pool (team is a routing label only) (REQ-034-100)
  9. System sets Ticket Source to "Patient App" and Submitter Type to "Patient"
  10. System displays confirmation to patient: "Support request submitted. Case #[number]. Our team will respond within 24 hours." (REQ-034-098)
  11. System sends confirmation email to patient with case reference number (via S-03) (REQ-034-099)
  12. System sends notification to the Support Staff pool (REQ-034-099)
  13. Admin reviews case in Support Center, updates status (Open → In Progress → Resolved → Closed), and responds to patient
  14. For feedback submissions, admin sets Feedback Resolution (Implemented, Planned, Declined, Under Review) as appropriate
  15. Patient can view case status, feedback resolution, and admin responses in their Help Center (FR-035)
- **Outcome**: Patient support request or feedback automatically creates support case, tracked and managed in FR-034 with unified status workflow

**A6: Case Requires Provider Account Intervention**:

- **Trigger**: Admin needs to resolve provider-related issue from support case
- **Steps**:
  1. Admin views provider support case in Support Center
  2. Admin clicks "View Provider Record" link in support case (only available if case is linked to provider record)
  3. System deep-links to provider management module (A-02) with provider ID pre-filled
  4. Admin performs provider account intervention if needed
  5. Admin returns to support case and adds note documenting resolution
  6. System logs intervention in both support case timeline and provider account audit trail (REQ-034-074)
- **Outcome**: Provider account issue resolved with audit trail across both modules

**B1: Invalid Patient Identifier**:

- **Trigger**: Admin enters patient email/phone/HPID that doesn't exist in system
- **Steps**:
  1. System validates patient identifier against patient database
  2. System displays error message: "Patient not found. Please verify identifier or create case without patient link." (REQ-034-104)
  3. Admin corrects identifier or selects "No Patient Link" option for anonymous inquiries
  4. System allows case creation without patient linkage (REQ-034-104)
- **Outcome**: Case created for inquiry from non-registered user or with corrected patient identifier

**B2: Case Reassignment (Assigned Admin Unavailable)**:

- **Trigger**: Assigned admin is out of office or unable to handle case
- **Steps**:
  1. Admin manager or colleague opens case
  2. Admin clicks "Reassign Case" button
  3. System displays team member list
  4. Admin selects new assignee and enters reassignment reason
  5. System updates case assignment and notifies new assignee (REQ-034-105)
  6. System logs reassignment action in case timeline (REQ-034-105)
- **Outcome**: Case ownership transferred with audit trail

**B3: Patient Requests Case Reopening**:

- **Trigger**: Patient responds to closed case email stating issue not fully resolved
- **Steps**:
  1. Admin receives patient email reply
  2. Admin locates closed case by case ID
  3. Admin clicks "Reopen Case" button
  4. System prompts for reopening reason
  5. System changes case status from "Closed" to "Open"
  6. System logs reopening action with timestamp and reason
  7. Admin reassigns or continues investigation
- **Outcome**: Case lifecycle extended to ensure full resolution

**B4: Attachment Upload Failure**:

- **Trigger**: Admin attempts to upload file exceeding size limit or unsupported format
- **Steps**:
  1. System validates file size (max 10MB per file) and format (images, PDFs, documents)
  2. System displays error: "File exceeds 10MB limit" or "Unsupported file format" (REQ-034-106)
  3. Admin compresses file or converts format
  4. Admin retries upload
  5. System accepts valid file and attaches to case
- **Outcome**: Attachment successfully added to case or admin uses alternative method (email file separately)

---

## Screen Specifications

### Screen 1: Support Case Listing (Primary View)

**Purpose**: Primary admin interface for browsing, searching, filtering, and managing all support cases with quick actions

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---------|
| Create New Case Button | button | N/A | Initiates case creation flow (opens Screen 2) | Click action | no graph field (control) |
| Search Bar | text input | No | Search cases by case ID, patient name, provider name, email, phone, keywords in title/description | Min 3 chars to trigger search, real-time search (REQ-034-117) | no graph field (control) |
| Filter Bar (grouped) | filter group | No | Comprehensive filtering controls including: **Status Filter** (multi-select dropdown: Open, In Progress, Resolved, Closed; Default: Open + In Progress), **Priority Filter** (multi-select dropdown: Low, Medium, High, Urgent; Default: All priorities), **Category Filter** (multi-select dropdown from centralized category list; Default: All categories), **Ticket Source Filter** (multi-select dropdown: Patient App, Provider Portal, Manual Admin Entry; Default: All sources), **Submitter Type Filter** (multi-select dropdown: Patient, Provider, Admin; Default: All types), **Date Range Filter** (date picker for creation date range; Default: Last 90 days), **Assigned To Filter** (dropdown select: All Users, specific user; Default: All Users) | All filters are cumulative (AND logic); Filter selections persist during session (REQ-034-116) | ENT-support-case.status, ENT-support-case.priority, ENT-support-case.category, ENT-support-case.ticket_source, ENT-support-case.submitter_type, ENT-support-case.submitted_at, ENT-support-case.assigned_admin_id |
| Quick Stats Bar | stats component | N/A | Displays summary metrics: Open (X), In Progress (X), Urgent (X), Unassigned (X) | Display only, updates based on current filters | no graph field (control) |
| Case List Table | data table | N/A | Displays cases matching filters with 13 columns (see below); 50 cases per page default | Sortable columns, paginated; default sort by Last Updated descending (REQ-034-120) | no graph field (table of the column rows below) |
| **Table Column 1**: Selection Checkbox | checkbox | No | Checkbox for bulk action selection | Multi-select enabled; used for bulk operations | no graph field (control) |
| **Table Column 2**: Case ID | link | N/A | Unique case identifier (format: CASE-YYYY-#####, e.g., CASE-2025-12345); Width: 140px | Clickable link to case detail view (Screen 3); Sortable | ENT-support-case.case_id |
| **Table Column 3**: Case Title | text | N/A | Brief case summary; Width: 200px | Truncated with ellipsis if >50 chars; full title shown on hover; Sortable (REQ-034-160) | ENT-support-case.title |
| **Table Column 4**: Status | badge | N/A | Current status with color coding; Width: 100px | Open (blue), In Progress (yellow), Resolved (green), Closed (gray); Sortable | ENT-support-case.status |
| **Table Column 5**: Priority | badge | N/A | Priority level with color coding; Width: 80px | Low (gray), Medium (blue), High (orange), Urgent (red); Sortable | ENT-support-case.priority |
| **Table Column 6**: Category | text | N/A | Case category from centralized list; Width: 120px | Truncated if needed; Sortable | ENT-support-case.category |
| **Table Column 7**: Ticket Source | badge | N/A | Origin of support case; Width: 120px | Patient App / Provider Portal / Manual Admin Entry; Color-coded badge; Sortable | ENT-support-case.ticket_source |
| **Table Column 8**: Submitter Type | badge | N/A | Type of user who submitted case; Width: 100px | Patient / Provider / Admin; Color-coded badge; Sortable | ENT-support-case.submitter_type |
| **Table Column 9**: Linked Patient/Provider | link | No | Patient name + HPID or Provider clinic name; Width: 150px | Clickable if linked, empty if not linked; Not sortable | ENT-patient.name, ENT-patient.patient_id, ENT-provider.name |
| **Table Column 10**: Assigned To | text with avatar | No | Admin staff member handling case; Width: 120px | Shows "Unassigned" if not assigned; Display name with avatar; Sortable | ENT-support-case.assigned_admin_id |
| **Table Column 11**: Created Date | datetime | N/A | Case creation timestamp (format: YYYY-MM-DD HH:mm); Width: 130px | Local timezone; Sortable | ENT-support-case.submitted_at |
| **Table Column 12**: Last Updated | datetime | N/A | Most recent modification timestamp (format: YYYY-MM-DD HH:mm); Width: 130px | Local timezone; Default sort column (descending); Sortable | ENT-support-case.last_updated_at |
| **Table Column 13**: Actions | button group | N/A | Quick action buttons; Width: 180px | View, Reassign, Resolve, Reopen, Close; Buttons shown/hidden based on case status; Not sortable (REQ-034-118) | no graph field (control) |
| Bulk Assign Button | button | N/A | Assign selected cases to admin user | Enabled only if cases selected (REQ-034-119) | no graph field (control) |
| Bulk Close Button | button | N/A | Close selected cases (only if all are Resolved status) | Enabled only if cases selected and all Resolved (REQ-034-119) | no graph field (control) |
| Pagination Controls | component | N/A | Navigate through case list pages | 50 cases per page default; Shows: Previous, 1, 2, 3, ..., Next (REQ-034-120) | no graph field (control) |

**Quick Actions (per row)**: (REQ-034-118)

- **View**: Opens case detail view (Screen 3)
- **Reassign**: Opens reassignment modal (Screen 5) - only for Open/In Progress cases
- **Resolve**: Opens resolution modal (Screen 4) - only for In Progress cases
- **Reopen**: Reopens case (changes status from Closed to Open) - only for Closed cases
- **Close**: Closes case - only for Resolved cases

**Business Rules**:

- Default view shows Open and In Progress cases from last 90 days, sorted by Last Updated descending; the provider My Support Cases list (FR-032 Screen 5.7) uses this same default and refers to this rule, while its 20-cases-per-page detail is a separate rule in FR-032 (REQ-034-114)
- All admin staff see all cases regardless of assignment (assignment is informational only)
- Clicking case ID or row navigates to Case Detail View (Screen 3)
- Status badges color-coded (Open=blue, In Progress=yellow, Resolved=green, Closed=gray) (REQ-034-122)
- Priority badges color-coded (Low=gray, Medium=blue, High=orange, Urgent=red) (REQ-034-122)
- Urgent cases always sorted to top of list regardless of other sort order (REQ-034-115)
- Cases with no activity for longer than the Case Inactivity Threshold (Screen 7, default 14 days) marked with warning icon (REQ-034-078)
- Search is real-time and searches across: Case ID, Case Title, Description, Patient Name, Provider Name, Email, Phone (REQ-034-117)
- Filters are cumulative (AND logic between different filter types) (REQ-034-116)
- Filter selections persist during session (REQ-034-116)

**Notes**:

- Use sticky table header for scrolling through long case lists
- Display empty state message if no cases match filters: "No cases found. Try adjusting your filters or create a new case." (REQ-034-121)
- Show total case count matching current filters at top of table: "Showing X cases" (REQ-034-121)
- Consider implementing saved filter presets as future enhancement
- Display "Quick Stats" bar above table: Open (X) | In Progress (X) | Urgent (X) | Unassigned (X) (REQ-034-121)

---

### Screen 2: Create/Edit Support Case Form

**Purpose**: Allows admin staff to create new support cases or edit existing case details

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---------|
| Case Title | text input | Yes | Brief summary of case (e.g., "Cannot reset password") | Max 200 chars, min 10 chars, NO auto-generation (REQ-034-130) | ENT-support-case.title |
| Category | dropdown select | Yes | Case type classification from centralized category list | Options: Technical Issue, Account Access, Payment Question, Booking Issue, General Inquiry, Provider Support, Patient Support, Feature Request, Bug Report, Feedback | ENT-support-case.category |
| Priority | dropdown select | Yes | Urgency level from centralized priority list | Options: Low, Medium, High, Urgent | ENT-support-case.priority |
| Ticket Source | dropdown select (readonly if auto-created) | Yes | Origin of support case | Options: Patient App, Provider Portal, Manual Admin Entry; Auto-populated for app-submitted tickets, editable for manual entries (REQ-034-124) | ENT-support-case.ticket_source |
| Submitter Type | dropdown select (readonly if auto-created) | Yes | Type of user who submitted case | Options: Patient, Provider, Admin; Auto-populated for app-submitted tickets, editable for manual entries (REQ-034-124) | ENT-support-case.submitter_type |
| Patient Identifier | text input with autocomplete | No | HPID, email, or phone to link case to patient record | Must match existing patient if provided; optional field; Required if Submitter Type = Patient, unless No Patient Link is chosen (REQ-034-123) | ENT-support-case.patient_id, ENT-patient.patient_id, ENT-patient.name |
| Provider Identifier | text input with autocomplete | No | Provider ID or clinic name (if case is provider-related) | Must match existing provider if provided; optional field; Required if Submitter Type = Provider (REQ-034-123) | ENT-support-case.provider_id, ENT-provider.name |
| Description | textarea | Yes | Full details of inquiry or issue | Min 20 chars, max 5000 chars, supports plain text (REQ-034-128) | ENT-support-case.description |
| Internal Notes | textarea | No | Admin-only notes not visible to patient/provider | Max 2000 chars per note entry (REQ-034-130) | ENT-support-case-timeline-event.description |
| Attachments | file upload | No | Supporting documents, screenshots, emails | Max 5 files per message, 10MB per file, formats: JPG, PNG, PDF, DOC, DOCX (REQ-034-130) | ENT-support-case.attachments |
| Assigned To | dropdown select (admin users) | No | Admin staff member responsible for case (informational only) | List of active admin users with "Support Staff" role (REQ-034-126) | ENT-support-case.assigned_admin_id |
| Status | dropdown select | Yes | Current case lifecycle stage | Options: Open (default), In Progress, Resolved, Closed | ENT-support-case.status |
| Feedback Resolution | dropdown select | No | Resolution outcome for feedback/feature request tickets (optional) | Options: Implemented, Planned, Declined, Under Review; Only applicable for Category = Feature Request, Bug Report, or Feedback (REQ-034-125) | ENT-support-case.feedback_resolution |
| Tags | multi-select | No | Optional labels for categorization (e.g., "Bug", "Feature Request") | Max 5 tags per case (REQ-034-130) | ENT-support-case.tags |

**Business Rules**:

- **Case Title is ALWAYS REQUIRED** - no auto-generation from Description
- Patient Identifier field shows autocomplete suggestions as admin types (match by name, email, HPID); Required if Submitter Type = Patient, unless No Patient Link is chosen (REQ-034-123)
- Provider Identifier field shows autocomplete suggestions as admin types (match by name, clinic ID); Required if Submitter Type = Provider (REQ-034-123)
- If patient identifier provided, system displays patient name and HPID for confirmation (REQ-034-123)
- If provider identifier provided, system displays provider clinic name and ID for confirmation (REQ-034-123)
- Linking case to patient/provider record enables "View Patient Record" or "View Provider Record" button for deep-linking to A-01 or A-02 (REQ-034-123)
- Ticket Source automatically set based on submission origin: Patient App (FR-035), Provider Portal (FR-032), or Manual Admin Entry; readonly for auto-created tickets, editable for manual entries (REQ-034-124)
- Submitter Type automatically set based on submission origin (Patient, Provider, or Admin); readonly for auto-created tickets, editable for manual entries (REQ-034-124)
- Attachments scanned for viruses before upload completes
- Internal Notes section visible to every admin who has the "View Support Center" permission (REQ-034-083)
- Status defaults to "Open" for new cases (REQ-034-096)
- Status follows unified workflow: Open → In Progress → Resolved → Closed (cannot skip stages except for case reopening) (REQ-034-102)
- Priority defaults to "Medium" for new cases (REQ-034-096)
- Assigned To field optional on creation; can be assigned later (assignment is informational only - all admins can work on all cases) (REQ-034-126)
- Feedback Resolution field only visible and applicable when Category = Feature Request, Bug Report, or Feedback (REQ-034-125)
- Feedback Resolution optional but recommended for feedback-type tickets; tracks outcome independently of case status (REQ-034-125)
- Case cannot be marked "Closed" until status is "Resolved" (validation rule) (REQ-034-102)
- System logs all field changes with timestamp and admin user for audit trail (REQ-034-129)

**Notes**:

- Display character count for Title and Description fields (REQ-034-128)
- Show "Link to Patient Record" button if patient identifier matched
- Show "Link to Provider Record" button if provider identifier matched

---

### Screen 3: Support Case Detail View

**Purpose**: Displays complete case information, two-way communication thread, comprehensive timeline with full context, and all case management actions

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---------|
| Case ID | text (readonly) | N/A | Unique case identifier (e.g., CASE-2025-12345) | Display only | ENT-support-case.case_id |
| Case Title | text (readonly, editable via edit mode) | Yes | Brief case summary | Max 200 chars | ENT-support-case.title |
| Status | badge | Yes | Current case status with color coding (Open, In Progress, Resolved, Closed) | Visual indicator only | ENT-support-case.status |
| Priority | badge | Yes | Urgency level with color coding | Visual indicator only | ENT-support-case.priority |
| Category | text (readonly) | Yes | Case type | Display only | ENT-support-case.category |
| Ticket Source | badge | Yes | Origin of support case | Options: Patient App, Provider Portal, Manual Admin Entry; Display only | ENT-support-case.ticket_source |
| Submitter Type | badge | Yes | Type of user who submitted case | Options: Patient, Provider, Admin; Display only | ENT-support-case.submitter_type |
| Feedback Resolution | badge | No | Resolution outcome for feedback tickets | Options: Implemented, Planned, Declined, Under Review; Only displayed for feedback/feature request tickets | ENT-support-case.feedback_resolution |
| Created Date | datetime (readonly) | N/A | Case creation timestamp | Display only | ENT-support-case.submitted_at |
| Last Updated | datetime (readonly) | N/A | Most recent modification timestamp | Display only | ENT-support-case.last_updated_at |
| Assigned To | text with avatar | No | Admin staff member handling case (informational only) | Display name and profile photo | ENT-support-case.assigned_admin_id |
| Linked Patient | link | No | Patient name and HPID (if linked) | Clickable link to patient record in A-01; only available if case is linked to patient | ENT-patient.name, ENT-patient.patient_id |
| Linked Provider | link | No | Provider clinic name and ID (if linked) | Clickable link to provider record in A-02; only available if case is linked to provider | ENT-provider.name |
| Description | text block | Yes | Full case details (initial submission) | Display only (editable via edit mode) | ENT-support-case.description |
| Communication Thread | threaded conversation component | N/A | Two-way conversation thread showing messages from admin, patient, and provider with full message content and context | Scrollable, chronological (oldest first), shows sender name, avatar, timestamp, message content | ENT-support-case-message.sender_name, ENT-support-case-message.sender_type, ENT-support-case-message.sent_at, ENT-support-case-message.content, ENT-support-case-message.parent_message_id, ENT-support-case-message.is_read, ENT-support-case-message.attachments |
| Case Timeline | vertical timeline component | N/A | Comprehensive timeline showing all case events with full context: case creation, status changes, feedback resolution updates, assignments, reassignments, internal notes, attachments, account interventions, case reopening | Readonly, scrollable, reverse chronological (newest first) | ENT-support-case-timeline-event.event_type, ENT-support-case-timeline-event.event_timestamp, ENT-support-case-timeline-event.actor_id, ENT-support-case-timeline-event.actor_type, ENT-support-case-timeline-event.description, ENT-support-case-timeline-event.is_internal_note, ENT-support-case-attachment.file_name, ENT-support-case-attachment.file_size, ENT-support-case-attachment.uploaded_by_id |
| Add Internal Note Button | button | N/A | Allows admin to add internal note to case (not visible to patient/provider) | Opens note entry modal | no graph field (control) |
| Reply to Patient/Provider Button | button | N/A | Allows admin to send message in communication thread (visible to patient/provider) | Opens message composition modal; sends notification email | no graph field (control) |
| Update Status Button | button | N/A | Changes case status (Open → In Progress → Resolved → Closed) | Opens status change modal | no graph field (control) |
| Resolve Case Button | button | N/A | Marks case as Resolved with resolution summary | Opens resolution modal (Screen 4); only enabled for In Progress cases | no graph field (control) |
| Reassign Case Button | button | N/A | Transfers case to another admin (informational only) | Opens reassignment modal (Screen 5) | no graph field (control) |
| Reopen Case Button | button | N/A | Reopens closed case (changes status from Closed to Open) | Opens reopen reason modal; only visible for Closed cases | no graph field (control) |
| Close Case Button | button | N/A | Marks case as Closed (only enabled if status is Resolved) | Confirmation required (REQ-034-134) | no graph field (control) |
| Edit Case Button | button | N/A | Opens case edit form (Screen 2) to modify case details | Enabled for all statuses | no graph field (control) |

**Communication Thread Structure**:

Each message in the thread displays:

- **Sender**: Name and avatar (Admin Staff Name, Patient Name, or Provider Clinic Name)
- **Sender Type Badge**: Admin / Patient / Provider
- **Timestamp**: Date and time of message
- **Message Content**: Full message text with formatting support
- **Attachments**: If any, displayed as downloadable links/thumbnails
- **Read Status**: A read flag is stored for each message now, and the unread badge (see Notes) is required; an admin-facing display of whether the patient/provider has viewed a message is a future enhancement

**Timeline Event Types with Full Context**: (REQ-034-133)

- **Case Created**: Shows who created it, initial description, category, priority, and linked patient/provider
- **Status Changed**: Shows old status → new status, who changed it, and reason/context if provided
- **Feedback Resolution Updated**: Shows old resolution → new resolution, who updated it, and notes
- **Case Assigned**: Shows previous assignee → new assignee, who performed assignment, and reason
- **Case Reassigned**: Shows reassignment details with full reason and context
- **Internal Note Added**: Shows full note content (admin-only), who added it, marked with "Admin Only" badge
- **Message Sent**: Shows full message content, sender (admin/patient/provider), recipient type
- **Message Received**: Shows full message content from patient/provider in response to admin
- **Attachment Uploaded**: Shows attachment name, size, who uploaded it, download link
- **Account Intervention**: Shows what intervention was performed (password reset, account unlock, etc.), who performed it, link to patient/provider record
- **Case Resolved**: Shows resolution summary, resolution category, feedback resolution (if applicable), who resolved it
- **Case Reopened**: Shows who reopened it (an admin, or System for an automatic reopen), reason for reopening, previous resolution summary
- **Case Closed**: Shows who closed it, auto-close vs manual close indicator
- **Case Escalated**: Shows the reassignment marked as an escalation, the reason, and the raised priority
- **Notification Sent / Notification Failed**: Shows the notification, its recipient, and its delivery result
- **Admin Deactivated**: Shows that the assigned admin account was deactivated and the case became unassigned

**Business Rules**:

- Communication Thread displays messages in chronological order (oldest first) to show conversation flow (REQ-034-131)
- Timeline displays events in reverse chronological order (newest first) to show latest updates (REQ-034-131)
- Timeline shows full context for each event, not just milestones - includes all details of what happened
- Patient and provider can reply to admin messages from their apps (FR-035, FR-032), creating two-way conversation
- When patient/provider replies, message appears in Communication Thread and timeline logged as "Message Received from [Patient/Provider]" (REQ-034-132)
- Admin messages sent via "Reply to Patient/Provider" button appear in Communication Thread and trigger email notification via S-03 (REQ-034-132)
- Internal Notes visible to every admin who has the "View Support Center" permission (not shown in Communication Thread, only in Timeline with "Admin Only" badge) (REQ-034-083)
- Messages to patient/provider logged in both Communication Thread and Timeline (REQ-034-132)
- Status transitions follow lifecycle: Open → In Progress → Resolved → Closed (cannot skip stages except for reopening) (REQ-034-102)
- System prevents closing case unless status is "Resolved" first (REQ-034-102)
- Linked Patient/Provider names clickable to deep-link to patient/provider management modules (only if case is linked) (REQ-034-134)
- Deep-link buttons only visible when case is linked to patient or provider record (REQ-034-134)
- "Reopen Case" button only visible when case status is "Closed" (REQ-034-134)
- "Resolve Case" button only visible when case status is "In Progress" (REQ-034-134)
- All admins can view and work on all cases regardless of assignment (assignment is informational only)

**Notes**:

- Use expandable/collapsible timeline entries for long notes, messages, or intervention details
- Display attachment thumbnails in timeline and communication thread with download links
- Highlight urgent cases with red border and alert icon
- Display warning if case has had no activity for longer than the Case Inactivity Threshold (Screen 7, default 14 days) (REQ-034-078)
- Show unread message count badge (required) if patient/provider has sent new messages since last admin view (REQ-034-135)
- Use different visual styling for admin messages vs patient/provider messages in Communication Thread (similar to chat interface)
- Consider implementing @ mentions for internal notes to notify specific admin team members (future enhancement)

---

### Screen 4: Case Resolution Modal

**Purpose**: Allows admin to document case resolution and close case with resolution summary

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---------|
| Resolution Summary | textarea | Yes | Brief description of how issue was resolved | Min 20 chars, max 1000 chars | ENT-support-case-resolution.resolution_summary |
| Resolution Category | dropdown select | Yes | Type of resolution | Options: Issue Fixed, Information Provided, Account Intervention, Escalated to Provider, User Error, Cannot Reproduce, Duplicate Case, Other | ENT-support-case-resolution.resolution_category |
| Feedback Resolution | dropdown select | No | Resolution outcome for feedback/feature request tickets (optional) | Options: Implemented, Planned, Declined, Under Review; Only displayed and applicable for Category = Feature Request, Bug Report, or Feedback | ENT-support-case-resolution.feedback_resolution |
| Root Cause | dropdown select | No | Underlying cause of issue (for analytics) | Options: User Confusion, Technical Bug, Account Configuration, Payment Gateway Issue, Provider Error, System Outage, Other | ENT-support-case-resolution.root_cause |
| Send Resolution Email | checkbox | Yes | Send email to patient/provider with resolution summary | Default: checked (REQ-034-161) | no graph field (control) |
| Auto-Close After | dropdown select | Yes | Days to wait before auto-closing case | Options: Immediately, 3 days, 7 days, 14 days (default: 7 days) (REQ-034-140) | ENT-support-case-resolution.auto_close_period_days |
| Internal Resolution Notes | textarea | No | Admin-only notes about resolution (not sent to patient/provider) | Max 2000 chars (REQ-034-138) | ENT-support-case-timeline-event.description |
| Mark as Resolved Button | button | Yes | Changes case status to Resolved and logs resolution details | Saves and closes modal | no graph field (control) |
| Cancel Button | button | Yes | Closes modal without saving | No changes made | no graph field (control) |

**Business Rules**:

- Resolution Summary included in email sent to patient/provider (if Send Resolution Email checked) (REQ-034-137)
- Feedback Resolution field only visible when case Category = Feature Request, Bug Report, or Feedback (REQ-034-125)
- Feedback Resolution tracks outcome independently of case status (e.g., case can be Resolved with Feedback Resolution = Planned) (REQ-034-125)
- Feedback Resolution included in resolution email to submitter if populated (REQ-034-137)
- Internal Resolution Notes only visible to admin staff (not included in patient/provider-facing communications) (REQ-034-138)
- System automatically closes case after specified auto-close period if patient/provider doesn't respond (REQ-034-139)
- If patient/provider replies while the case is Resolved (before the auto-close period expires), the case is reopened automatically and the system records a Reopening by System with the reason "User replied" (REQ-034-139)
- A reply to a Closed case does not reopen it automatically; it goes to an admin, who decides whether to reopen it (Screen 6) (REQ-034-139)
- Resolution Category and Root Cause captured for analytics and trend identification (REQ-034-136)
- System logs resolution timestamp, feedback resolution (if applicable), and admin user who marked case resolved (REQ-034-136)
- Case cannot be marked Resolved without entering Resolution Summary

**Notes**:

- Use plain language in Resolution Summary field guidance: "Explain to the patient/provider how their issue was resolved"
- For feedback tickets, display guidance: "Select Feedback Resolution to communicate outcome to submitter (e.g., 'Implemented in version 2.5', 'Planned for Q2 2026', 'Declined due to technical constraints')"
- Preview resolution email content before sending (including Feedback Resolution if applicable) (REQ-034-141)
- Display warning if case was open for >14 days: "This case took longer than average to resolve. Consider documenting learnings." (REQ-034-141)

---

### Screen 5: Reassign Case Modal

**Purpose**: Allows admin to reassign case to another admin team member with reason tracking for informational purposes

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---------|
| Current Assignee | text (readonly) | N/A | Current admin user assigned to case (or "Unassigned") | Display only | ENT-support-case.assigned_admin_id |
| New Assignee | dropdown select | Yes | Admin user to reassign case to | List of active admin users with "Support Staff" role; cannot select current assignee (REQ-034-144) | ENT-support-case-assignment.assigned_to_admin_id |
| Reassignment Reason | textarea | Yes | Reason for reassigning case (also the reason recorded for an escalation) | Min 10 chars, max 500 chars (REQ-034-144) | ENT-support-case-assignment.assignment_reason |
| Escalate | checkbox | No | Marks the reassignment as an escalation: raises the case priority to High or Urgent and sends the escalation notice to the new assignee | Default: unchecked; when ticked, the admin chooses High or Urgent as the new priority | ENT-support-case-assignment.is_escalation |
| Notify New Assignee | checkbox | Yes | Send email notification to new assignee | Default: checked (REQ-034-162) | no graph field (control) |
| Reassign Case Button | button | Yes | Confirms reassignment and updates case | Saves and closes modal | no graph field (control) |
| Cancel Button | button | Yes | Closes modal without saving | No changes made | no graph field (control) |

**Business Rules**:

- Assignment is informational only - all admins can view and work on all cases regardless of assignment
- System logs reassignment in case timeline with timestamp, old assignee, new assignee, reason, and admin who performed reassignment (REQ-034-142)
- If "Notify New Assignee" checked, system sends email notification via S-03 with case details and reassignment reason (REQ-034-142)
- Reassignment does not change case status or restrict access for other admins (REQ-034-143)
- Escalation has no separate screen or form: it is the Escalate tick in this modal, with the reassignment reason required. The timeline marks the reassignment as an escalation. This applies equally to patient-submitted and provider-submitted cases (REQ-034-103)
- Admin can reassign case to themselves or to another team member (REQ-034-143)
- System displays reassignment history in case timeline to track case ownership changes (REQ-034-142)

**Notes**:

- Display new assignee's current case load (number of Open/In Progress cases) to help with workload balancing (REQ-034-144)
- Consider adding "Reassign to Team" option for assigning to a team rather than individual (future enhancement)
- Showing assignee availability status is out of scope

---

### Screen 6: Reopen Case Modal

**Purpose**: Allows admin to reopen closed case when patient/provider indicates issue not fully resolved

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---------|
| Previous Resolution Summary | text (readonly) | N/A | Resolution summary from when case was previously resolved | Display only | ENT-support-case-resolution.resolution_summary |
| Previous Closure Date | datetime (readonly) | N/A | Date when case was closed | Display only | ENT-support-case-resolution.closed_at |
| Reopening Reason | textarea | Yes | Reason for reopening case (e.g., "Patient reports issue persists") | Min 20 chars, max 1000 chars (REQ-034-148) | ENT-support-case-reopening.reopening_reason |
| Assign To | dropdown select | No | Admin user to assign reopened case to | List of active admin users; optional, defaults to previous assignee if available (REQ-034-148) | ENT-support-case-reopening.new_assignee_id |
| New Priority | dropdown select | Yes | Priority level for reopened case | Options: Low, Medium, High, Urgent; defaults to previous priority (REQ-034-148) | ENT-support-case-reopening.new_priority |
| Notify Patient/Provider | checkbox | Yes | Send email to patient/provider acknowledging case reopening | Default: checked (REQ-034-163) | no graph field (control) |
| Reopen Case Button | button | Yes | Changes case status from Closed to Open and logs reopening | Saves and closes modal | no graph field (control) |
| Cancel Button | button | Yes | Closes modal without reopening case | No changes made | no graph field (control) |

**Business Rules**:

- Case status changes from "Closed" to "Open" when reopened (REQ-034-145)
- System logs reopening in case timeline with timestamp, reopening reason, admin who reopened it, and reference to previous resolution (REQ-034-145)
- If "Notify Patient/Provider" checked, system sends email notification via S-03 acknowledging case reopening (REQ-034-146)
- Reopened case appears in default case listing view (Open status) (REQ-034-147)
- Previous resolution summary remains in case history for reference (REQ-034-145)
- Case timeline shows clear "Case Reopened" event with full context of why it was reopened (REQ-034-145)
- Admin can adjust priority when reopening to reflect urgency (e.g., escalate if issue was marked resolved incorrectly) (REQ-034-148)

**Notes**:

- Display previous communication thread and resolution summary above form for context
- Offer "Reopen Reason Templates" for common scenarios (e.g., "Issue persists", "New information received", "Resolution did not work") as an optional feature managed in Screen 7 (Section 7); admins can always type a custom reason
- Show time elapsed since case was closed (e.g., "Closed 3 days ago")

---

### Screen 7: Support Center Configuration (Settings Path)

**Purpose**: Allows Super Admin to manage centralized lists and configuration options for Support Center module (accessed via Settings > Support Center)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---------|
| **Section 1: Case Categories** | section header | N/A | Manage centralized case category list | N/A | no graph field (section header) |
| Category List Table | data table | N/A | Displays all case categories with columns: Category Name, Display Order, Status (Active/Inactive), Used Count, Actions (Edit) | Sortable by display order; built-in categories cannot be deleted or switched off, so Deactivate/Activate and Delete are not offered for them; the only edits offered are the category label and display order (REQ-034-171) | ENT-support-case-category.name, ENT-support-case-category.display_order, ENT-support-case-category.status, ENT-support-case-category.used_count |
| Add Category Button | button | N/A | Not offered: categories cannot be added to the built-in list | N/A | no graph field (control) |
| Category Label (in modal) | text input | Yes | Label shown for a built-in case category (the label is what stays editable) | Max 50 chars; must be unique; Built-in labels: Technical Issue, Account Access, Payment Question, Booking Issue, General Inquiry, Provider Support, Patient Support, Feature Request, Bug Report, Feedback (REQ-034-154) | ENT-support-case-category.name |
| Category Display Order (in modal) | number input | Yes | Sort order for dropdown display (1-100) | Must be positive integer; determines order in dropdown lists (REQ-034-153) | ENT-support-case-category.display_order |
| Category Status (in modal) | toggle | Yes | Always Active for built-in categories | Built-in categories cannot be switched off | ENT-support-case-category.status |
| **Section 2: Case Priorities** | section header | N/A | Manage centralized case priority list | N/A | no graph field (section header) |
| Priority List Table | data table | N/A | Displays all priorities with columns: Priority Name, Color Code, Display Order, Status (Active/Inactive), Used Count, Actions (Edit, Deactivate/Activate, Delete) | Sortable by display order; cannot delete priorities with active cases; Low, Medium, High and Urgent cannot be renamed, switched off or deleted (REQ-034-172) | ENT-support-case-priority.name, ENT-support-case-priority.color_code, ENT-support-case-priority.display_order, ENT-support-case-priority.status, ENT-support-case-priority.used_count |
| Add Priority Button | button | N/A | Opens modal to add new priority level | Click action; an added priority carries no escalation or resolution-time rule unless one is defined (REQ-034-172) | no graph field (control) |
| Priority Name (in modal) | text input | Yes | Name of priority level | Max 20 chars; must be unique; the four built-in names (Low, Medium, High, Urgent) cannot be changed (REQ-034-154) | ENT-support-case-priority.name |
| Priority Color Code (in modal) | color picker | Yes | Badge color for priority display | Options: gray, blue, orange, red, green, purple | ENT-support-case-priority.color_code |
| Priority Display Order (in modal) | number input | Yes | Sort order for dropdown display (1-10) | Must be positive integer (REQ-034-153) | ENT-support-case-priority.display_order |
| Priority Status (in modal) | toggle | Yes | Active or Inactive | Inactive priorities hidden from new case creation; the four built-in priorities cannot be switched off | ENT-support-case-priority.status |
| **Section 3: Resolution Categories** | section header | N/A | Manage resolution category options | N/A | no graph field (section header) |
| Resolution Category List Table | data table | N/A | Displays all resolution categories with columns: Category Name, Display Order, Status (Active/Inactive), Used Count, Actions (Edit, Deactivate/Activate, Delete) | Sortable by display order; cannot be deleted while in use (Deactivate is offered instead) | ENT-support-resolution-category.name, ENT-support-resolution-category.display_order, ENT-support-resolution-category.status, ENT-support-resolution-category.used_count |
| Add Resolution Category Button | button | N/A | Opens modal to add new resolution category | Click action | no graph field (control) |
| Resolution Category Name (in modal) | text input | Yes | Name of resolution category | Max 50 chars; must be unique; Examples: Issue Fixed, Information Provided, Account Intervention, Escalated to Provider, User Error, Cannot Reproduce, Duplicate Case, Other (REQ-034-154) | ENT-support-resolution-category.name |
| Resolution Category Display Order (in modal) | number input | Yes | Sort order for dropdown display (1-100) | Must be positive integer | ENT-support-resolution-category.display_order |
| Resolution Category Status (in modal) | toggle | Yes | Active or Inactive | Inactive categories hidden from resolution modal | ENT-support-resolution-category.status |
| **Section 4: Root Cause Options** | section header | N/A | Manage root cause options for analytics | N/A | no graph field (section header) |
| Root Cause List Table | data table | N/A | Displays all root cause options with columns: Root Cause Name, Display Order, Status (Active/Inactive), Used Count, Actions (Edit, Deactivate/Activate, Delete) | Sortable by display order; cannot be deleted while in use (Deactivate is offered instead) | ENT-support-root-cause.name, ENT-support-root-cause.display_order, ENT-support-root-cause.status, ENT-support-root-cause.used_count |
| Add Root Cause Button | button | N/A | Opens modal to add new root cause option | Click action | no graph field (control) |
| Root Cause Name (in modal) | text input | Yes | Name of root cause | Max 50 chars; must be unique; Examples: User Confusion, Technical Bug, Account Configuration, Payment Gateway Issue, Provider Error, System Outage, Other (REQ-034-154) | ENT-support-root-cause.name |
| Root Cause Display Order (in modal) | number input | Yes | Sort order for dropdown display (1-100) | Must be positive integer | ENT-support-root-cause.display_order |
| Root Cause Status (in modal) | toggle | Yes | Active or Inactive | Inactive options hidden from resolution modal | ENT-support-root-cause.status |
| **Section 5: Case Tags** | section header | N/A | Manage custom case tags for categorization | N/A | no graph field (section header) |
| Tag List Table | data table | N/A | Displays all tags with columns: Tag Name, Color, Used Count, Actions (Edit, Delete) | Sortable by tag name; can delete tags even if used (removes from cases) (REQ-034-151) | ENT-support-case-tag.name, ENT-support-case-tag.color, ENT-support-case-tag.used_count |
| Add Tag Button | button | N/A | Opens modal to add new tag | Click action | no graph field (control) |
| Tag Name (in modal) | text input | Yes | Name of tag | Max 30 chars; must be unique; Examples: Bug, Feature Request, Urgent, VIP (REQ-034-154) | ENT-support-case-tag.name |
| Tag Color (in modal) | color picker | Yes | Badge color for tag display | Options: gray, blue, orange, red, green, purple, yellow, pink | ENT-support-case-tag.color |
| **Section 6: Auto-Escalation Rules** | section header | N/A | Configure automatic case escalation thresholds | N/A | no graph field (section header) |
| Urgent Case Unassigned Threshold | number input | Yes | Hours before an urgent case that is still unassigned auto-escalates to Super Admin (a fixed alert email goes to admins after 1 hour first) | Min: 1, Max: 48, Default: 24 hours (REQ-034-155) | no graph field (setting SET-support-urgent-unassigned-escalation-threshold) |
| High Priority Case Threshold | number input | Yes | Hours before high priority case auto-escalates if no status change | Min: 12, Max: 72, Default: 48 hours (REQ-034-155) | no graph field (setting SET-support-high-priority-escalation-threshold) |
| Case Inactivity Threshold | number input | Yes | Days before case with no activity flagged for admin review; also the one clock behind the inactivity warnings in the case list and case detail view | Min: 7, Max: 90, Default: 14 days (REQ-034-078, REQ-034-155) | no graph field (setting SET-support-case-inactivity-threshold) |
| **Section 7: Reopen Reason Templates** | section header | N/A | Manage reopening reason templates for quick selection (optional) | N/A | no graph field (section header) |
| Reopen Reason Templates Table | data table | N/A | Displays templates with columns: Template Text, Used Count, Actions (Edit, Deactivate/Activate, Delete) | Optional feature; admins can also enter custom reasons; a template cannot be deleted while in use (Deactivate is offered instead) (REQ-034-157) | ENT-support-reopen-template.template_text, ENT-support-reopen-template.used_count |
| Add Template Button | button | N/A | Opens modal to add new template | Click action | no graph field (control) |
| Template Text (in modal) | text input | Yes | Pre-written reopening reason text | Max 200 chars; Examples: "Issue persists", "New information received", "Resolution did not work", "Patient reported problem still occurring" (REQ-034-154) | ENT-support-reopen-template.template_text |
| Save Configuration Button | button | Yes | Saves all changes to configuration | Validates all fields; updates centralized lists immediately | no graph field (control) |
| Cancel Button | button | Yes | Discards unsaved changes | Confirmation required if changes exist | no graph field (control) |

**Business Rules**:

- Only Super Admin can access this screen; there is no Support Manager role and no "Manage Support Configuration" permission (REQ-034-149)
- Configuration screen accessible via Settings > Support Center path in admin navigation (REQ-034-149)
- All changes to centralized lists take effect immediately for new case creation and case updates (REQ-034-150)
- Cannot delete categories, priorities, or resolution categories that are currently used by active cases (status = Open or In Progress); resolution categories, root causes, and reopen reason templates also cannot be deleted while in use, and Deactivate is offered instead. Case tags stay freely deletable (REQ-034-151)
- The four built-in priorities (Low, Medium, High, Urgent) cannot be renamed, switched off, or deleted; admins may add other priorities, which have no escalation or resolution-time rule unless one is defined (REQ-034-172)
- Built-in case categories are fixed for patients: categories cannot be added to the list, deleted, or switched off; the label and display order remain editable (REQ-034-171)
- Can deactivate items instead of deleting; deactivated items hidden from dropdowns but preserved for historical data (REQ-034-151)
- Used Count shows number of cases currently using each option (helps prevent accidental deletion of important items) (REQ-034-152)
- Display Order determines the sequence items appear in dropdown lists throughout Support Center (REQ-034-153)
- Feedback Resolution options (Implemented, Planned, Declined, Under Review) are fixed in codebase (not configurable) to maintain consistency across product feedback tracking
- Auto-escalation thresholds configurable within defined ranges to prevent overly aggressive or too lenient escalation (REQ-034-155)
- All configuration changes logged in audit trail with timestamp, admin user ID, and change description (REQ-034-156)
- System validates uniqueness of names within each category to prevent duplicates (REQ-034-154)
- Reopen Reason Templates are optional; admins can always enter custom reasons even if templates exist (REQ-034-157)
- **Notification templates and rules** for support case notifications (case created, status changed, admin replied, case resolved, case closed) are managed in FR-030 (Notification Rules & Configuration), not in this screen

**Notes**:

- Use drag-and-drop interface for reordering display order (alternative to manual number entry)
- Show warning when attempting to delete item with active usage: "X cases currently use this [category/priority]. Please deactivate instead." (REQ-034-158)
- Display "Default" badge for system-required items that cannot be deleted (e.g., "Open", "Closed" statuses if applicable)
- Consider adding import/export functionality for configuration backup and migration across environments (future enhancement)
- Show last modified timestamp and admin user for each configuration item (REQ-034-159)
- Provide bulk actions for activating/deactivating multiple items at once (REQ-034-159)

---

## Business Rules

### General Module Rules

- **Rule 1**: All support cases must have unique case IDs generated sequentially (format: CASE-YYYY-#####) (REQ-034-002)
- **Rule 2**: **Unified Status Workflow**: Case lifecycle follows strict progression: Open → In Progress → Resolved → Closed (consistent across all ticket types and sources; cannot skip stages, except for case reopening) (REQ-034-003)
- **Rule 3**: Cases can be reopened after closure if patient/provider indicates issue not fully resolved (REQ-034-017)
- **Rule 4**: **Ticket Source Tracking**: All cases must have Ticket Source (Patient App, Provider Portal, Manual Admin Entry) to identify submission origin (REQ-034-004)
- **Rule 5**: **Submitter Type Tracking**: All cases must have Submitter Type (Patient, Provider, Admin) to identify who submitted the case (REQ-034-005)
- **Rule 6**: **Feedback Resolution Tracking**: Cases with Category = Feature Request, Bug Report, or Feedback can optionally track Feedback Resolution (Implemented, Planned, Declined, Under Review) independently of case status (REQ-034-006)
- **Rule 7**: **Centralized Category Management**: FR-034 owns the support-case categories (Help Centre content categories belong to FR-033). The ten names (Technical Issue, Account Access, Payment Question, Booking Issue, General Inquiry, Provider Support, Patient Support, Feature Request, Bug Report, Feedback) are the master list to ensure consistency across all case submissions; the patient and provider submission forms show subsets of it. The built-in categories are fixed for patients: they cannot be added to, deleted or switched off (REQ-034-018, REQ-034-030, REQ-034-171)
- **Rule 8**: **Centralized Priority Management**: Case priorities managed in centralized list (Low, Medium, High, Urgent) to ensure consistent prioritization across system; the four built-in priorities cannot be renamed, switched off or deleted, and admins may add further priorities (REQ-034-019, REQ-034-031, REQ-034-172)
- **Rule 9**: **Assignment is Informational Only**: All admin staff can view and work on all cases regardless of assignment; assignment field is for informational/organizational purposes only and does not restrict access (REQ-034-007)
- **Rule 10**: **Two-Way Communication Support**: Patients and providers can reply to admin messages from their apps (FR-035, FR-032), creating threaded conversation within case (REQ-034-014)
- **Rule 11**: **Comprehensive Timeline with Full Context**: Case timeline shows all events with complete details and context (not just milestones), including full message content, intervention details, status change reasons, etc. (REQ-034-008)
- **Rule 12**: Maximum case resolution time (a limit for any single case, separate from the success-criteria goals): 48 hours for Urgent, 5 business days for High, 10 business days for Medium/Low priority (REQ-034-077)
- **Rule 13**: Cases with no activity for longer than the Case Inactivity Threshold (Screen 7, default 14 days) flagged for admin review and potential closure; the same threshold drives the warning shown in the case list and case detail view (REQ-034-078)
- **Rule 14**: Support cases distinct from aftercare communications (FR-011) and provider-patient messaging (FR-012) (REQ-034-076)
- **Rule 15**: Admin staff can link multiple cases to same patient/provider for trend analysis (REQ-034-079)
- **Rule 16**: Support cases support patient submissions (FR-035), provider submissions (FR-032), and manual admin entries in single unified system
- **Rule 17**: When patient/provider replies to case, message appears in Communication Thread and triggers email notification to assigned admin (or all support staff if unassigned) (REQ-034-080)
- **Rule 18**: **Report a problem**: FR-034 owns the Report a problem rule for the patient app; FR-035 and FR-001 point to it (see REQ-034-164)
- **Rule 19**: **Provider-caused cancellation link**: A support case can be linked to a provider-caused cancellation; the system does not create a ticket automatically (see REQ-034-166)
- **Rule 20**: **Booking request values**: FR-034 owns request type, request status, decline reason and outcome for booking cancellation and change requests; FR-016 only shows them (see REQ-034-167 to REQ-034-170)
- Admin staff access Support Center via modern web browsers (Chrome, Safari, Firefox, Edge - last 2 versions)
- Email delivery via S-03 Notification Service is reliable with >95% delivery rate
- Support staff available during business hours (8am-6pm UTC) for case assignment and resolution

### Data & Privacy Rules

- **Privacy Rule 1**: Patient full names, contact details, and medical information visible to admin users granted Support Center access via RBAC; within Support Center, all cases are visible regardless of assignment (REQ-034-081)
- **Privacy Rule 2**: Support case data encrypted at rest (AES-256) and in transit (TLS 1.3) (REQ-034-040, REQ-034-041)
- **Privacy Rule 3**: Case timeline and all messages logged with immutable audit trail (cannot be deleted, only appended) (REQ-034-082)
- **Privacy Rule 4**: Internal Notes visible to every admin who has the "View Support Center" permission (not visible to patients/providers) (REQ-034-083)
- **Privacy Rule 5**: FR-034 provides no case-data export
- **Audit Rule**: All access to support cases logged with timestamp, admin user ID, IP address, and action performed (REQ-034-043)
- **HIPAA/GDPR**: Support cases may contain medical information; handle as PHI with healthcare-grade security (REQ-034-085)
- **Data Retention**: Support case retention follows the system PRD, Platform-Wide Rules: One 10-year retention period; archive after closure, do not hard delete (REQ-034-038)
- **Storage**: Case attachments stored in cloud object storage (S3) with pre-signed URLs for secure, time-limited access
- **Authentication**: Admin staff authenticate via FR-031 (Admin Access Control). MFA is enforced once the shared MFA stack (FR-026 / FR-031) is delivered; until then, implement strong password policies, throttling, and re-authentication flows per Constitution.
- **Authorization**: Role-Based Access Control (RBAC) enforces granular permissions: (REQ-034-094)
  - Support Staff: Create, view, edit, reassign, and resolve cases (assignment is informational only and does not restrict access)
  - Super Admin: Full access including Support Center configuration management, receipt of escalations, and audit log export (no hard delete; archive only)
  - There is no Support Manager role and no "Manage Support Configuration" permission
- **Threat mitigation**: Rate limiting on case creation API (max 60 cases/hour per admin user) to prevent abuse (REQ-034-095)
- **Compliance**: HIPAA-compliant handling of patient medical information in case descriptions and attachments (REQ-034-085)
- If patient record deleted, support case retains anonymized copy of patient name/email for audit trail (REQ-034-109)
- If provider record deactivated, support case retains provider name for historical reference (REQ-034-110)
- Internal service-to-service authentication (API key or mutual TLS)
- If notification fails, log error and retry following the FR-030 retry rule; mark notification as failed in case timeline (REQ-034-113)

### Admin Editability Rules

**Editable by Admin (via Admin Platform UI)**: (REQ-034-086)

- Case category, priority, status, title, description (per-case editing in Screen 2)
- Case assignment (transfer to another admin user via Screen 5)
- Internal notes and admin-only comments (in Screen 3)
- Patient/provider linkage (add, modify, or remove linked records in Screen 2)
- Case tags and labels (per-case in Screen 2)
- Resolution summary and resolution category (in Screen 4)
- Auto-close period (Immediately, 3, 7, or 14 days after resolution in Screen 4)

**Configurable by Super Admin (via Settings > Support Center - Screen 7)**: (REQ-034-087)

- Case categories list (built-in list: edit label and reorder only; categories cannot be added, deactivated or deleted, as Screen 7 states)
- Case priorities list (the four built-in priorities Low, Medium, High, Urgent cannot be renamed, deactivated or deleted; other priorities can be added, edited, deactivated and reordered; color coding)
- Resolution categories list (add, edit, deactivate, reorder)
- Root cause options list (add, edit, deactivate, reorder)
- Case tags master list (add, edit, delete, color coding)
- Auto-escalation thresholds (configurable within defined ranges: 1-48 hours for urgent cases, 12-72 hours for high priority, 7-90 days for inactivity)
- Reopen reason templates (add, edit, delete)

**Fixed in Codebase (Not Editable)**: (REQ-034-088)

- Case lifecycle stages (Open, In Progress, Resolved, Closed)
- Feedback Resolution options (Implemented, Planned, Declined, Under Review)
- Case ID format and generation logic (CASE-YYYY-#####)
- Ticket Source options (Patient App, Provider Portal, Manual Admin Entry)
- Submitter Type options (Patient, Provider, Admin)
- Audit trail structure and immutability
- Encryption algorithms (AES-256 for data at rest, TLS 1.3 for data in transit)
- Maximum attachment size (10MB per file)

**Configurable with Restrictions (via FR-030: Notification Rules & Configuration)**: (REQ-034-089)

- Email notification templates for support case events (content editable, trigger logic fixed):
  - Support Case Created
  - Support Case Assigned
  - Support Case Status Changed
  - Support Case Admin Reply
  - Support Case User Reply
  - Support Case Resolved
  - Support Case Reopened
  - Support Case Closed
  - Support Case Escalated
- Notification delivery channels (email, push) per support case event type
- Notification timing and retry logic for support case notifications

### Notification Rules

- **Notification Rule 1**: Patients receive email notifications when: (REQ-034-090)
  - Support case created (optional confirmation)
  - Case status changes to "In Progress" (admin is working on it)
  - Admin sends message/reply to patient
  - Case marked "Resolved" with resolution summary
  - Case closed
- **Notification Rule 2**: Providers receive email notifications when: (REQ-034-091)
  - Support case created for their inquiry
  - Case status changes
  - Admin sends message/reply to provider
  - Case marked "Resolved" with resolution summary
  - Case closed
- **Notification Rule 3**: Admin staff receive email notifications when: (REQ-034-092)
  - Case assigned to them
  - Case escalated to them (escalations go to Super Admin)
  - Patient/provider replies to a case (one email per reply)
  - A case is reopened (a separate reopening notice, in addition to the reply email)
  - Urgent case created and still unassigned after 1 hour (a fixed alert email to admins; if the case is still unassigned at the Urgent Case Unassigned Threshold in Screen 7, default 24 hours, it escalates to Super Admin)
- **Notification Rule 4**: All notifications sent via S-03 Notification Service; failed sends are retried following the FR-030 retry rule (REQ-034-047, REQ-034-051)
- **Notification Rule 5**: Email notifications include case ID, title, status, and direct link to admin case view (for admin recipients) (REQ-034-093)

**Carried from dropped sections (original wording)**:

- **Integration point**: Support Center calls S-03 API to trigger notification events (support.case_created, support.case_assigned, support.case_status_changed, support.case_admin_reply, support.case_user_reply, support.case_resolved, support.case_reopened, support.case_closed, support.case_escalated); S-03 delivers notifications based on rules configured in FR-030
- **None for MVP**: Support Center operates entirely within Hairline platform with no external API dependencies
- **Search**: Implement full-text search index on case ID, title, description, patient/provider names, email, and phone for fast keyword searches (internal notes are not indexed for search)

---

## Dependencies

- FR-035 (Patient Help Center & Support Access): patient-submitted support requests and feedback create support cases
- FR-032 (Provider Dashboard Settings & Help Centre): provider-submitted support requests (Screen 5.5) and feedback (Screen 5.6) create support cases
- FR-033 (Help Centre Content Management): no direct integration; provides content displayed in FR-032 and FR-035
- FR-031 (Admin Access Control & Permissions): support staff roles and permissions managed via RBAC
- FR-016 (Patient Management & Oversight): support cases linked to patient records by HPID, email, or phone number
- FR-015 (Provider Management): support cases linked to provider records by provider ID or clinic name
- FR-020 (Notification Service, S-03): email and push notifications to patients, providers, and admin staff
- FR-030 (Notification Rules & Configuration): support case notification templates, delivery channels, timing, and recipient rules
- FR-026 (App Settings & Security): security settings (admin session timeout, audit logging) apply to Support Center

---


## User Scenarios & Testing

### User Story 1 - Admin Creates Support Case from Patient Email (Priority: P1)

Admin staff receives email from patient saying "I can't log into my account" and creates a support case to track resolution.

**Why this priority**: Core support case intake workflow - if this doesn't work, support system is unusable

**Independent Test**: Can be fully tested by admin creating case from email inquiry, assigning to support staff, and verifying case appears in dashboard

**Acceptance Scenarios**:

1. **Given** admin staff receives patient email inquiry, **When** admin logs into Support Center and clicks "Create New Case", **Then** case creation form displays with all required fields
2. **Given** admin enters case title "Patient cannot login", category "Account Access", priority "High", and patient email, **When** admin clicks "Create Case", **Then** system creates case with unique case ID and status "Open"
3. **Given** case is created, **When** admin assigns case to support team member, **Then** system sends email notification to assigned admin and logs assignment in case timeline
4. **Given** case is assigned, **When** assigned admin opens case and changes status to "In Progress", **Then** system logs status change and sends email notification to patient that case is being investigated

---

### User Story 2 - Admin Resolves Support Case with Account Intervention (Priority: P1)

Support staff investigates "cannot login" case, resets patient password, documents resolution, and closes case.

**Why this priority**: Core case resolution workflow including intervention and closure - critical for completing support cycle

**Independent Test**: Can be tested by admin investigating case, performing password reset via A-01 deep-link, documenting resolution, and verifying case closure

**Acceptance Scenarios**:

1. **Given** admin is reviewing "cannot login" case, **When** admin clicks "View Patient Record" link, **Then** system opens patient management module (A-01) with patient details pre-loaded
2. **Given** admin is in patient management view, **When** admin performs password reset, **Then** system logs intervention in both patient audit trail and support case timeline
3. **Given** patient issue is resolved, **When** admin returns to case and clicks "Mark as Resolved", **Then** system displays resolution modal prompting for resolution summary
4. **Given** admin enters resolution summary "Password reset completed, sent new credentials to patient email", **When** admin clicks "Submit", **Then** system changes case status to "Resolved" and sends resolution email to patient
5. **Given** case is marked Resolved, **When** 7 days pass without patient response, **Then** system auto-closes case and sets status to "Closed"

---

### User Story 3 - Admin Searches and Filters Cases (Priority: P1)

An admin searches for all urgent cases assigned to specific team member to ensure timely resolution.

**Why this priority**: Essential for support management and oversight - managers must be able to monitor workload and prioritize urgent issues

**Independent Test**: Can be tested by creating multiple test cases with different priorities, statuses, and assignments, then verifying search and filters return correct results

**Acceptance Scenarios**:

1. **Given** an admin is on Support Center dashboard, **When** the admin navigates to "All Cases" view, **Then** system displays case list with default filters (Open + In Progress cases from last 90 days)
2. **Given** the admin is viewing case list, **When** the admin selects "Urgent" priority filter and specific admin user from "Assigned To" filter, **Then** system displays only urgent cases assigned to that user
3. **Given** filtered case list is displayed, **When** the admin clicks case row, **Then** system navigates to case detail view with full timeline

---

### User Story 4 - Admin Handles Provider Support Case (Priority: P2)

Admin staff receives operational question from provider clinic about payment schedule and creates provider support case.

**Why this priority**: Important for provider satisfaction but lower priority than patient-facing support in MVP

**Independent Test**: Can be tested by creating case with "Provider Support" category, linking to provider record, and verifying resolution workflow

**Acceptance Scenarios**:

1. **Given** admin receives email from provider asking about payout schedule, **When** admin creates new case with category "Provider Support", **Then** system allows admin to link case to provider record by provider ID or clinic name
2. **Given** case is linked to provider, **When** admin views case details, **Then** system displays "Link to Provider Record" button for deep-linking to provider management module (A-02)
3. **Given** admin resolves provider inquiry, **When** admin marks case as Resolved with resolution summary, **Then** system sends resolution email to provider contact email
4. **Given** provider support case is closed, **When** admin views provider record in A-02, **Then** closed case appears in provider's support case history

---

### User Story 5 - Patient Requests Case Reopening (Priority: P2)

Patient responds to case closure email stating issue not fully resolved; admin reopens case for further investigation.

**Why this priority**: Important for ensuring complete resolution but less frequent scenario than initial case creation/resolution

**Independent Test**: Can be tested by closing a case, then admin manually reopening it to verify state transition

**Acceptance Scenarios**:

1. **Given** case is in "Closed" status, **When** patient emails support saying issue persists, **Then** admin locates closed case by case ID
2. **Given** admin is viewing closed case, **When** admin clicks "Reopen Case" button, **Then** system prompts for reopening reason
3. **Given** admin enters reopening reason "Patient reports issue persists after password reset", **When** admin confirms reopening, **Then** system changes case status from "Closed" to "Open" and logs reopening in case timeline
4. **Given** case is reopened, **When** admin reassigns case to support staff, **Then** system sends assignment notification and allows admin to continue investigation

---

### User Story 6 - Admin Escalates Urgent Case (Priority: P2)

Support staff member encounters complex technical issue requiring more senior attention; escalates the case by reassigning it with the Escalate option.

**Why this priority**: Important for handling complex cases but less frequent than standard support workflows

**Independent Test**: Can be tested by creating case, then escalating it through the Reassign Case modal to verify priority increase and notification

**Acceptance Scenarios**:

1. **Given** support staff member is reviewing case involving system outage, **When** the staff member determines escalation needed, **Then** the staff member clicks "Reassign Case" (there is no separate escalation form)
2. **Given** the Reassign Case modal is displayed, **When** the staff member selects the new assignee, enters reassignment reason "Database connection errors", and ticks "Escalate" with priority "Urgent", **Then** system updates case priority to "Urgent"
3. **Given** case is escalated, **When** system processes the reassignment, **Then** system sends the escalation notice to the new assignee and logs the reassignment in case timeline marked as an escalation
4. **Given** the new assignee receives the notice, **When** the new assignee opens the case, **Then** case shows the escalation in its timeline with the full reason

---

### Edge Cases

- **What happens when admin attempts to link case to patient with duplicate email addresses?**
  - System displays list of all patients with matching email and prompts admin to select correct patient by HPID (REQ-034-107)
  - Admin can choose to create case without patient link if ambiguous (REQ-034-107)

- **How does system handle case assignment when assigned admin is deactivated or leaves organization?**
  - System automatically detects deactivated admin accounts and marks their assigned cases as "Unassigned" (REQ-034-108)
  - Support Staff receive notification to reassign orphaned cases (REQ-034-108)
  - Case timeline logs admin account deactivation event (REQ-034-108)

- **What occurs if patient deletes their account while support case is open?**
  - Support case remains in system with anonymized patient identifier for audit trail compliance (REQ-034-109)
  - Case marked with "Patient Account Deleted" badge (REQ-034-109)
  - Admin cannot deep-link to patient record but can still close case with resolution notes (REQ-034-109)

- **How to manage attachment upload when file contains malware or virus?**
  - System scans all uploaded files using antivirus service before accepting
  - If malware detected, system rejects upload and displays error: "File rejected due to security scan failure" (REQ-034-106)
  - Admin notified to request patient/provider send file via alternative secure method (REQ-034-106)

- **What happens when two admins simultaneously edit same case?**
  - System uses optimistic locking with "last write wins" strategy (REQ-034-111)
  - If conflict detected, admin receives warning: "This case was modified by another admin. Please review recent changes before saving." (REQ-034-111)
  - Admin can review other admin's changes and decide whether to overwrite or discard their edits (REQ-034-111)

- **How does system handle case search with special characters or SQL injection attempts?**
  - System sanitizes all search input to prevent SQL injection attacks (REQ-034-112)
  - Special characters escaped before executing search query (REQ-034-112)
  - Search limited to alphanumeric characters, spaces, and common punctuation (REQ-034-112)

- **What occurs if S-03 Notification Service is down and cannot send case notification emails?**
  - System queues the notification for retry following the FR-030 retry rule (FR-030 owns the retry schedule and count) (REQ-034-113)
  - Case timeline logs notification failure with timestamp (REQ-034-113)
  - Admin dashboard displays notification status indicator (sent, pending, failed) (REQ-034-113)
  - If the notification still fails once the FR-030 retry rule is exhausted, admin receives alert to manually contact patient/provider (REQ-034-113)

---

## Functional Requirements Summary

### Core Requirements

- **REQ-034-001**: System MUST provide admin interface for creating support cases with title (always required, no auto-generation), category (from centralized managed list), priority (from centralized managed list), ticket source, submitter type, patient/provider linkage, description, feedback resolution (optional), and attachments
- **REQ-034-002**: System MUST assign unique case IDs in format CASE-YYYY-##### (year and sequential number)
- **REQ-034-003**: **Unified Status Workflow**: System MUST support case lifecycle progression: Open → In Progress → Resolved → Closed (consistent across all ticket types and sources)
- **REQ-034-004**: System MUST track Ticket Source (Patient App, Provider Portal, Manual Admin Entry) for all support cases
- **REQ-034-005**: System MUST track Submitter Type (Patient, Provider, Admin) for all support cases
- **REQ-034-006**: System MUST support optional Feedback Resolution tracking (Implemented, Planned, Declined, Under Review) for feedback/feature request tickets independently of case status
- **REQ-034-007**: System MUST allow admin staff to assign cases to specific admin users for informational purposes only (assignment does not restrict access - all admins can view and work on all cases)
- **REQ-034-008**: System MUST maintain immutable comprehensive case timeline with all events showing full context and details (not just milestones): creation, status changes with reasons, feedback resolution changes, assignments, reassignments with reasons, notes, messages, attachments, account interventions with details, case reopening with reasons - each logged with timestamp and admin/patient/provider attribution
- **REQ-034-009**: System MUST allow admins to link support cases to patient records by HPID, email, or phone number
- **REQ-034-010**: System MUST allow admins to link support cases to provider records by provider ID or clinic name
- **REQ-034-011**: System MUST provide deep-linking from support case to patient management module (A-01) for account interventions when case is linked to patient record
- **REQ-034-012**: System MUST provide deep-linking from support case to provider management module (A-02) for provider record access when case is linked to provider record
- **REQ-034-013**: System MUST allow admins to add internal notes to cases that are not visible to patients/providers
- **REQ-034-014**: System MUST support two-way threaded communication between admin and patient/provider within case, allowing patient/provider to reply to admin messages from their apps (FR-035, FR-032)
- **REQ-034-015**: System MUST display Communication Thread showing all messages from admin, patient, and provider in chronological order with sender identification
- **REQ-034-016**: System MUST allow admins to reassign cases to other admin users with reason tracking
- **REQ-034-017**: System MUST allow admins to reopen closed cases with reopening reason when patient/provider indicates issue not resolved
- **REQ-034-018**: System MUST use centralized managed lists for case categories to ensure consistency across all submissions
- **REQ-034-019**: System MUST use centralized managed lists for case priorities to ensure consistency across system
- **REQ-034-020**: System MUST require case title field with no auto-generation (admin must provide title manually)
- **REQ-034-021**: System MUST automatically create support cases when patients submit Contact Support or Feedback requests via patient app (FR-035)
- **REQ-034-022**: System MUST automatically create support cases when providers submit Contact Support requests via Help Centre (FR-032 Screen 5.5)
- **REQ-034-023**: System MUST automatically create support cases when providers submit Feedback & Suggestions via Help Centre (FR-032 Screen 5.6)
- **REQ-034-024**: System MUST automatically link patient-submitted cases to patient records using logged-in patient session and set Ticket Source = "Patient App", Submitter Type = "Patient"
- **REQ-034-025**: System MUST automatically link provider-submitted cases to provider records using logged-in provider session and set Ticket Source = "Provider Portal", Submitter Type = "Provider"
- **REQ-034-026**: System MUST allow patients to view status, feedback resolution, communication thread, and reply to admin messages for their submitted support cases in patient app (FR-035)
- **REQ-034-027**: System MUST allow providers to view status, feedback resolution, communication thread, and reply to admin messages for their submitted support cases and feedback in Help Centre (FR-032 Screen 5.5 and 5.6)
- **REQ-034-028**: System MUST send email notifications to patients when admin responds to their submissions or updates case status (via S-03)
- **REQ-034-029**: System MUST send email notifications to providers when admin responds to their submissions or updates case status (via S-03)
- **REQ-034-164**: **Report a problem**: FR-034 owns the Report a problem rule for the patient app (FR-035 and FR-001 point to it). A problem report MUST create a support case with the device, operating system, app version, and report timestamp attached, and problem report submissions MUST be throttled

### Data Requirements

- **REQ-034-030**: System MUST support case categories: Technical Issue, Account Access, Payment Question, Booking Issue, General Inquiry, Provider Support, Patient Support, Feature Request, Bug Report, Feedback
- **REQ-034-031**: System MUST support priority levels: Low, Medium, High, Urgent
- **REQ-034-032**: System MUST support Ticket Source options: Patient App, Provider Portal, Manual Admin Entry
- **REQ-034-033**: System MUST support Submitter Type options: Patient, Provider, Admin
- **REQ-034-034**: System MUST support Feedback Resolution options: Implemented, Planned, Declined, Under Review (optional field for feedback/feature request tickets)
- **REQ-034-035**: System MUST store case description with minimum 20 characters and maximum 5000 characters
- **REQ-034-036**: System MUST support file attachments up to 10MB per file, with up to 5 files per message (replies included)
- **REQ-034-037**: System MUST support attachment formats: JPG, PNG, PDF, DOC, DOCX
- **REQ-034-038**: System MUST retain all case data per the system PRD, Platform-Wide Rules: One 10-year retention period (archive after closure, do not hard delete)
- **REQ-034-039**: System MUST capture resolution details: resolution summary, resolution category, feedback resolution (optional), root cause (optional), and resolution timestamp
- **REQ-034-167**: A support case raised for a booking cancellation or booking change MUST carry a request type: booking cancellation or booking change (shown in FR-016 as Cancellation or Appointment Change)
- **REQ-034-168**: Such a case MUST carry a request status of Open, Resolved, or Declined. The request status describes what happened to the patient's request; the case status (Open, In Progress, Resolved, Closed) describes the support work on the case. Both are kept and shown, and neither replaces the other
- **REQ-034-169**: When an admin declines a request, the system MUST require a decline reason of at least 20 characters
- **REQ-034-170**: For a Resolved or Declined request, the system MUST record the outcome: the action taken, the admin who took it, the time, and a link to the audit entry
- **FR-034 owns these four values** (request type, request status, decline reason, outcome); FR-016 Screen 9 only shows them

### Security & Privacy Requirements

- **REQ-034-040**: System MUST encrypt all case data at rest using AES-256 encryption
- **REQ-034-041**: System MUST encrypt all case data in transit using TLS 1.3
- **REQ-034-042**: System MUST enforce RBAC permissions for case access (Support Staff and Super Admin roles)
- **REQ-034-043**: System MUST log all case access and modifications with timestamp, admin user ID, IP address, and action performed
- **REQ-034-044**: System MUST scan uploaded attachments for viruses/malware before accepting
- **REQ-034-045**: System MUST prevent case deletion (soft delete/archive only) to maintain immutable audit trail
- **REQ-034-046**: System MUST mark Internal Notes as admin-only and prevent patient/provider access

### Integration Requirements

- **REQ-034-047**: System MUST integrate with S-03 Notification Service to send notifications for support case events (case created, assigned, status changed, admin reply, user reply, resolved, reopened, closed, escalated) based on notification rules configured in FR-030
- **REQ-034-048**: System MUST publish support case notification events to S-03 with complete case context (case ID, title, status, submitter info, message content, etc.) for template rendering
- **REQ-034-049**: System MUST support all notification delivery channels configured in FR-030 for support case events (email, push; SMS in future phases)
- **REQ-034-050**: System MUST determine notification recipients based on case attributes (submitter type, assigned admin, case priority, escalation rules) and FR-030 recipient rules
- **REQ-034-051**: System MUST rely on S-03 retry logic for failed notification deliveries (retry logic configured in FR-030, not FR-034)
- **REQ-034-052**: System MUST log notification events in case timeline (notification sent, delivery status) for audit trail
- **REQ-034-053**: System MUST provide RESTful API for case creation, retrieval, update, and search operations
- **REQ-034-166**: System MUST allow an admin to link a support case to a provider-caused cancellation (FR-015 A5 impact shown in FR-016 Provider-Caused Impacts); the system MUST NOT create a support case automatically when a provider-caused cancellation happens

**Note**: Notification templates, delivery timing, channel preferences, and recipient rules for all support case notifications are managed centrally in FR-030 (Notification Rules & Configuration), not in FR-034. Admin configures these via Settings → Alerts & Notifications → Messaging/Support category. (REQ-034-089)

### Case Listing & Reporting Requirements

- **REQ-034-054**: System MUST provide Support Center case listing screen as primary view with quick stats bar displaying: open cases count, in progress count, urgent cases count, unassigned cases count
- **REQ-034-055**: System MUST display case list with comprehensive filters: status, priority, category, ticket source, submitter type, date range, assigned admin, and search functionality
- **REQ-034-056**: System MUST support keyword search across case ID, case title, description, patient name, provider name, email address, and phone number (internal notes are not searched)
- **REQ-034-057**: System MUST highlight urgent cases in dashboard and case lists with visual indicators (red badges, alert icons)
- **REQ-034-058**: System MUST display warning for cases with no activity for longer than the Case Inactivity Threshold (Screen 7, default 14 days)

### Case Resolution & Closure Requirements

- **REQ-034-059**: System MUST require resolution summary (min 20 chars, max 1000 chars) before case can be marked Resolved
- **REQ-034-060**: System MUST send resolution email to patient/provider when case marked Resolved (if "Send Resolution Email" option enabled)
- **REQ-034-061**: System MUST support auto-closure period: Immediately, 3, 7, or 14 days after case marked Resolved (default 7 days)
- **REQ-034-062**: System MUST automatically close case after auto-closure period expires if patient/provider doesn't respond
- **REQ-034-063**: Merged into REQ-034-017 (one rule: admins reopen closed cases, and a reopening reason is required)
- **REQ-034-064**: System MUST log reopening reason in case timeline when case is reopened
- **REQ-034-165**: System MUST record an automatic reopen (a patient or provider reply to a Resolved case) as a Reopening record reopened by System with the reason "User replied"

### Performance & Scalability Requirements

- **REQ-034-065**: System MUST complete case creation within 2 seconds for 95% of requests
- **REQ-034-066**: System MUST load case detail view (including timeline) within 2 seconds
- **REQ-034-067**: System MUST return case search results within 1 second for keyword searches
- **REQ-034-068**: System MUST support 50 concurrent admin users managing cases without performance degradation
- **REQ-034-069**: System MUST handle the expected 100 to 200 case creations per day at launch, absorb peaks of up to 500 per day, and scale to 1000 cases per day within 12 months

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-11-22 | 2.7 | Requirements graph programme baseline: PRD compressed to the checklist structure (rules cited by REQ id, field rows tagged with graph field ids, dropped classes removed). No rule changes. Earlier history (v1.0 to v2.6) is in `archived/prd-baseline-2026-11-08/fr034-support-center-ticketing/` and in git history. The live PRD names no change requests. | AI Assistant |
| 2026-11-23 | 2.8 | Independent compression review: 3 clause(s) from dropped sections restored in original wording under Business Rules. No rule changes. | AI Assistant |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (PRD Standards & Requirements)  
**Based on**: FR-011 Aftercare & Recovery Management PRD
**Last Updated**: 2026-11-23
