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
- **Data-Driven Improvements**: Case analytics identify recurring issues across both patient and provider experiences, informing product improvements

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
- Admin staff categorize cases using centralized managed category list (Technical Issue, Account Access, Payment Question, Booking Issue, General Inquiry, Provider Support, Feature Request, Bug Report, Patient Support)
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
- Admin staff view case analytics in reporting view (open case count, average resolution time, case volume by category, ticket source breakdown, feedback resolution status)

**Admin Platform (A-01: Patient Management & Oversight)**:

- Admins accessing patient records can view linked support cases for that patient
- Support case context appears in patient detail view (e.g., "3 open support cases" with links)
- Admins can initiate account interventions (password reset, account suspension) directly from support cases

**Shared Services (S-03: Notification Service)**:

- Sends email notifications to patients when:
  - Support case status changes (Open → In Progress, In Progress → Resolved)
  - Admin replies to patient inquiry
  - Case is closed with resolution summary
- Sends email notifications to providers when:
  - Support case is created for their inquiry
  - Admin replies to provider question
  - Case is resolved
- Notification preferences configurable per case category

### Communication Structure

**In Scope**:

- Admin-to-patient email notifications for support case updates (via S-03)
- Admin-to-provider email notifications for support case updates (via S-03)
- Internal admin notes within support cases (not visible to patients/providers)
- Admin-to-admin case assignment notifications
- Case timeline with complete message history
- Attachment support for case communications (screenshots, documents)

**Out of Scope**:

- Real-time in-app chat between patient and admin (future enhancement)
- Real-time in-app chat between provider and admin (future enhancement)
- Aftercare-specific communications (handled by FR-011: Aftercare & Recovery Management)
- Provider ↔ Patient secure messaging (handled by FR-012: Secure Messaging)
- Video consultations for support (future enhancement)
- SMS notifications for support case updates (future enhancement - S-03 SMS integration)
- Phone call integration or VoIP (future enhancement)

### Entry Points

**Patient App Entry**:

- Patients access Contact Support and Feedback submission forms from patient app Help Center (FR-035: Patient Help Center & Support Submission)
- Patient submissions automatically create support cases in FR-034 system with unified status workflow
- Patients can view status of their submitted tickets in patient app

**Provider Platform Entry**:

- Providers access Contact Support form from Help Centre (FR-032 Screen 5.5) to submit support requests
- Providers access Feedback & Suggestions form from Help Centre (FR-032 Screen 5.6) to submit feedback
- Provider submissions automatically create support cases in FR-034 system with unified status workflow

**Admin Platform Entry**:

- Admin staff access Support Center module from main admin navigation menu
- Default view shows case listing screen with all cases (Open and In Progress by default)
- All admin staff can view all cases regardless of assignment (assignment is informational only)
- Admin receives email notification when new support case is created or assigned to them
- Admin can create new support case manually from case listing screen via "Create New Case" button
- Super Admin and authorized admin staff access Support Center Configuration via Settings > Support Center path to manage centralized lists (categories, priorities, resolution categories, root causes, tags)

**System-Triggered Entry**:

- System automatically creates support case when patient submits Contact Support or Feedback request via patient app (FR-035)
- System automatically creates support case when provider submits Contact Support request via Help Centre (FR-032 Screen 5.5)
- System automatically creates support case when provider submits Feedback & Suggestions via Help Centre (FR-032 Screen 5.6)
- Admin creates support case when patient or provider contacts via email (manual case creation from email content)
- Admin creates support case when patient or provider contacts via phone (manual case entry after call)

**Integration Entry**:

- Support cases linkable from patient management module (A-01) - admins view patient's support history
- Support cases linkable from provider management module (A-02) - admins view provider's support history
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
   - **Category**: Selects from predefined categories (Technical Issue, Account Access, Payment Question, Booking Issue, General Inquiry)
   - **Priority**: Sets priority level (Low, Medium, High, Urgent)
   - **Patient Identifier**: Links case to patient by HPID, email, or phone number
   - **Description**: Full details of patient's inquiry or issue
   - **Attachments**: Uploads any relevant screenshots or documents patient provided
6. **System** validates inputs and creates support case record with status "Open"
7. **System** assigns unique case ID (e.g., "CASE-2025-12345")
8. **System** records case creation timestamp and admin user who created it
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

- **Trigger**: Admin determines case requires senior staff or technical team involvement
- **Steps**:
  1. Admin clicks "Escalate Case" button
  2. System displays escalation form with reason field
  3. Admin selects escalation recipient (senior admin or technical team)
  4. System updates case priority to "High" or "Urgent"
  5. System sends escalation notification to selected recipient
  6. System logs escalation action in case timeline
- **Outcome**: Case reassigned to higher-level support staff with increased priority

**A2: Case Requires Patient Account Intervention**:

- **Trigger**: Admin needs to reset patient password, suspend account, or modify patient data
- **Steps**:
  1. Admin clicks "View Patient Record" link in support case
  2. System deep-links to patient management module (A-01) with patient HPID pre-filled
  3. Admin performs account intervention (password reset, account unlock, data correction)
  4. Admin returns to support case and adds note documenting intervention
  5. System logs intervention in both support case timeline and patient account audit trail
- **Outcome**: Patient account issue resolved with audit trail across both modules

**A3: Provider Submits Contact Support Request via Help Centre**:

- **Trigger**: Provider needs direct assistance and submits support request through Help Centre (FR-032 Screen 5.5)
- **Steps**:
  1. Provider navigates to Help Centre and selects "Contact Support" subscreen (FR-032 Screen 5.5)
  2. System displays support request form (subject, category, message, priority, optional attachment)
  3. Provider completes form with support request details and submits
  4. System validates form fields and automatically creates support case with unique case ID (CASE-YYYY-#####)
  5. System links case to provider record (provider ID automatically linked from logged-in provider session)
  6. System sets case category based on provider's selection (Technical Issue, Account Access, Payment Question, Booking Issue, General Inquiry, Provider Support)
  7. System sets case priority based on provider's selection (Low, Medium, High, Urgent)
  8. System sets case status to "Open" and assigns to default provider support team
  9. System sets Ticket Source to "Provider Portal" and Submitter Type to "Provider"
  10. System displays confirmation to provider: "Support request submitted. Case #[number]. Our team will respond within 24 hours."
  11. System sends confirmation email to provider with case reference number (via S-03)
  12. System sends notification to assigned admin team member
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
  6. System sets case category based on feedback type (Feature Request, Bug Report, Suggestion, Other)
  7. System sets case priority based on provider's suggested priority (Low, Medium, High, Urgent)
  8. System sets case status to "Open" and assigns to product/feedback team
  9. System sets Ticket Source to "Provider Portal" and Submitter Type to "Provider"
  10. System displays confirmation to provider: "Thank you for your feedback! Case #[number]. We'll review your submission."
  11. System sends confirmation email to provider with case reference number (via S-03)
  12. System sends notification to assigned admin team member
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
  6. System sets case category based on patient's selection (Technical Issue, Account Access, Payment Question, Booking Issue, General Inquiry, Feature Request, Bug Report, Feedback)
  7. System sets case priority based on patient's selection (Low, Medium, High, Urgent)
  8. System sets case status to "Open" and assigns to patient support team
  9. System sets Ticket Source to "Patient App" and Submitter Type to "Patient"
  10. System displays confirmation to patient: "Support request submitted. Case #[number]. Our team will respond within 24 hours."
  11. System sends confirmation email to patient with case reference number (via S-03)
  12. System sends notification to assigned admin team member
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
  6. System logs intervention in both support case timeline and provider account audit trail
- **Outcome**: Provider account issue resolved with audit trail across both modules

**B1: Invalid Patient Identifier**:

- **Trigger**: Admin enters patient email/phone/HPID that doesn't exist in system
- **Steps**:
  1. System validates patient identifier against patient database
  2. System displays error message: "Patient not found. Please verify identifier or create case without patient link."
  3. Admin corrects identifier or selects "No Patient Link" option for anonymous inquiries
  4. System allows case creation without patient linkage
- **Outcome**: Case created for inquiry from non-registered user or with corrected patient identifier

**B2: Case Reassignment (Assigned Admin Unavailable)**:

- **Trigger**: Assigned admin is out of office or unable to handle case
- **Steps**:
  1. Admin manager or colleague opens case
  2. Admin clicks "Reassign Case" button
  3. System displays team member list with availability indicators
  4. Admin selects new assignee and enters reassignment reason
  5. System updates case assignment and notifies new assignee
  6. System logs reassignment action in case timeline
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
  2. System displays error: "File exceeds 10MB limit" or "Unsupported file format"
  3. Admin compresses file or converts format
  4. Admin retries upload
  5. System accepts valid file and attaches to case
- **Outcome**: Attachment successfully added to case or admin uses alternative method (email file separately)

---

## Screen Specifications

### Screen 1: Support Case Listing (Primary View)

**Purpose**: Primary admin interface for browsing, searching, filtering, and managing all support cases with quick actions

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Create New Case Button | button | N/A | Initiates case creation flow (opens Screen 2) | Click action |
| Search Bar | text input | No | Search cases by case ID, patient name, provider name, email, keywords in title/description | Min 3 chars to trigger search, real-time search |
| Filter Bar (grouped) | filter group | No | Comprehensive filtering controls including: **Status Filter** (multi-select dropdown: Open, In Progress, Resolved, Closed; Default: Open + In Progress), **Priority Filter** (multi-select dropdown: Low, Medium, High, Urgent; Default: All priorities), **Category Filter** (multi-select dropdown from centralized category list; Default: All categories), **Ticket Source Filter** (multi-select dropdown: Patient App, Provider Portal, Manual Admin Entry; Default: All sources), **Submitter Type Filter** (multi-select dropdown: Patient, Provider, Admin; Default: All types), **Date Range Filter** (date picker for creation date range; Default: Last 30 days), **Assigned To Filter** (dropdown select: All Users, specific user; Default: All Users) | All filters are cumulative (AND logic); Filter selections persist during session |
| Quick Stats Bar | stats component | N/A | Displays summary metrics: Open (X), In Progress (X), Urgent (X), Unassigned (X) | Display only, updates based on current filters |
| Case List Table | data table | N/A | Displays cases matching filters with 13 columns (see below); 50 cases per page default | Sortable columns, paginated; default sort by Last Updated descending |
| **Table Column 1**: Selection Checkbox | checkbox | No | Checkbox for bulk action selection | Multi-select enabled; used for bulk operations |
| **Table Column 2**: Case ID | link | N/A | Unique case identifier (format: CASE-YYYY-#####, e.g., CASE-2025-12345); Width: 140px | Clickable link to case detail view (Screen 3); Sortable |
| **Table Column 3**: Case Title | text | N/A | Brief case summary; Width: 200px | Truncated with ellipsis if >50 chars; full title shown on hover; Sortable |
| **Table Column 4**: Status | badge | N/A | Current status with color coding; Width: 100px | Open (blue), In Progress (yellow), Resolved (green), Closed (gray); Sortable |
| **Table Column 5**: Priority | badge | N/A | Priority level with color coding; Width: 80px | Low (gray), Medium (blue), High (orange), Urgent (red); Sortable |
| **Table Column 6**: Category | text | N/A | Case category from centralized list; Width: 120px | Truncated if needed; Sortable |
| **Table Column 7**: Ticket Source | badge | N/A | Origin of support case; Width: 120px | Patient App / Provider Portal / Manual Admin Entry; Color-coded badge; Sortable |
| **Table Column 8**: Submitter Type | badge | N/A | Type of user who submitted case; Width: 100px | Patient / Provider / Admin; Color-coded badge; Sortable |
| **Table Column 9**: Linked Patient/Provider | link | No | Patient name + HPID or Provider clinic name; Width: 150px | Clickable if linked, empty if not linked; Not sortable |
| **Table Column 10**: Assigned To | text with avatar | No | Admin staff member handling case; Width: 120px | Shows "Unassigned" if not assigned; Display name with avatar; Sortable |
| **Table Column 11**: Created Date | datetime | N/A | Case creation timestamp (format: YYYY-MM-DD HH:mm); Width: 130px | Local timezone; Sortable |
| **Table Column 12**: Last Updated | datetime | N/A | Most recent modification timestamp (format: YYYY-MM-DD HH:mm); Width: 130px | Local timezone; Default sort column (descending); Sortable |
| **Table Column 13**: Actions | button group | N/A | Quick action buttons; Width: 180px | View, Reassign, Resolve, Reopen, Close; Buttons shown/hidden based on case status; Not sortable |
| Bulk Assign Button | button | N/A | Assign selected cases to admin user | Enabled only if cases selected |
| Bulk Close Button | button | N/A | Close selected cases (only if all are Resolved status) | Enabled only if cases selected and all Resolved |
| Pagination Controls | component | N/A | Navigate through case list pages | 50 cases per page default; Shows: Previous, 1, 2, 3, ..., Next |

**Quick Actions (per row)**:

- **View**: Opens case detail view (Screen 3)
- **Reassign**: Opens reassignment modal (Screen 6) - only for Open/In Progress cases
- **Resolve**: Opens resolution modal (Screen 5) - only for In Progress cases
- **Reopen**: Reopens case (changes status from Closed to Open) - only for Closed cases
- **Close**: Closes case - only for Resolved cases

**Business Rules**:

- Default view shows Open and In Progress cases from last 30 days, sorted by Last Updated descending
- All admin staff see all cases regardless of assignment (assignment is informational only)
- Clicking case ID or row navigates to Case Detail View (Screen 3)
- Status badges color-coded (Open=blue, In Progress=yellow, Resolved=green, Closed=gray)
- Priority badges color-coded (Low=gray, Medium=blue, High=orange, Urgent=red)
- Urgent cases always sorted to top of list regardless of other sort order
- Cases with >7 days since last update marked with warning icon
- Search is real-time and searches across: Case ID, Case Title, Description, Patient Name, Provider Name, Email, Phone
- Filters are cumulative (AND logic between different filter types)
- Filter selections persist during session

**Notes**:

- Use sticky table header for scrolling through long case lists
- Display empty state message if no cases match filters: "No cases found. Try adjusting your filters or create a new case."
- Show total case count matching current filters at top of table: "Showing X cases"
- Consider implementing saved filter presets as future enhancement
- Display "Quick Stats" bar above table: Open (X) | In Progress (X) | Urgent (X) | Unassigned (X)

---

### Screen 2: Create/Edit Support Case Form

**Purpose**: Allows admin staff to create new support cases or edit existing case details

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Case Title | text input | Yes | Brief summary of case (e.g., "Cannot reset password") | Max 200 chars, min 10 chars, NO auto-generation |
| Category | dropdown select | Yes | Case type classification from centralized category list | Options: Technical Issue, Account Access, Payment Question, Booking Issue, General Inquiry, Provider Support, Patient Support, Feature Request, Bug Report, Feedback |
| Priority | dropdown select | Yes | Urgency level from centralized priority list | Options: Low, Medium, High, Urgent |
| Ticket Source | dropdown select (readonly if auto-created) | Yes | Origin of support case | Options: Patient App, Provider Portal, Manual Admin Entry; Auto-populated for app-submitted tickets, editable for manual entries |
| Submitter Type | dropdown select (readonly if auto-created) | Yes | Type of user who submitted case | Options: Patient, Provider, Admin; Auto-populated for app-submitted tickets, editable for manual entries |
| Patient Identifier | text input with autocomplete | No | HPID, email, or phone to link case to patient record | Must match existing patient if provided; optional field; Required if Submitter Type = Patient |
| Provider Identifier | text input with autocomplete | No | Provider ID or clinic name (if case is provider-related) | Must match existing provider if provided; optional field; Required if Submitter Type = Provider |
| Description | textarea | Yes | Full details of inquiry or issue | Min 20 chars, max 5000 chars, supports plain text |
| Internal Notes | textarea | No | Admin-only notes not visible to patient/provider | Max 2000 chars per note entry |
| Attachments | file upload | No | Supporting documents, screenshots, emails | Max 5 files, 10MB per file, formats: JPG, PNG, PDF, DOC, DOCX |
| Assigned To | dropdown select (admin users) | No | Admin staff member responsible for case (informational only) | List of active admin users with "Support Staff" role |
| Status | dropdown select | Yes | Current case lifecycle stage | Options: Open (default), In Progress, Resolved, Closed |
| Feedback Resolution | dropdown select | No | Resolution outcome for feedback/feature request tickets (optional) | Options: Implemented, Planned, Declined, Under Review; Only applicable for Category = Feature Request, Bug Report, or Feedback |
| Tags | multi-select | No | Optional labels for categorization (e.g., "Bug", "Feature Request") | Max 5 tags per case |

**Business Rules**:

- **Case Title is ALWAYS REQUIRED** - no auto-generation from Description
- Patient Identifier field shows autocomplete suggestions as admin types (match by name, email, HPID); Required if Submitter Type = Patient
- Provider Identifier field shows autocomplete suggestions as admin types (match by name, clinic ID); Required if Submitter Type = Provider
- If patient identifier provided, system displays patient name and HPID for confirmation
- If provider identifier provided, system displays provider clinic name and ID for confirmation
- Linking case to patient/provider record enables "View Patient Record" or "View Provider Record" button for deep-linking to A-01 or A-02
- Ticket Source automatically set based on submission origin: Patient App (FR-035), Provider Portal (FR-032), or Manual Admin Entry; readonly for auto-created tickets, editable for manual entries
- Submitter Type automatically set based on submission origin (Patient, Provider, or Admin); readonly for auto-created tickets, editable for manual entries
- Attachments scanned for viruses before upload completes
- Internal Notes section only visible to admin staff with appropriate permissions
- Status defaults to "Open" for new cases
- Status follows unified workflow: Open → In Progress → Resolved → Closed (cannot skip stages except for case reopening)
- Priority defaults to "Medium" for new cases
- Assigned To field optional on creation; can be assigned later (assignment is informational only - all admins can work on all cases)
- Feedback Resolution field only visible and applicable when Category = Feature Request, Bug Report, or Feedback
- Feedback Resolution optional but recommended for feedback-type tickets; tracks outcome independently of case status
- Case cannot be marked "Closed" until status is "Resolved" (validation rule)
- System logs all field changes with timestamp and admin user for audit trail

**Notes**:

- Use rich text editor for Description field to support formatting (bold, lists, links)
- Display character count for Title and Description fields
- Show "Link to Patient Record" button if patient identifier matched
- Show "Link to Provider Record" button if provider identifier matched
- Provide "Save as Draft" option to allow admins to partially complete case and return later

---

### Screen 3: Support Case Detail View

**Purpose**: Displays complete case information, two-way communication thread, comprehensive timeline with full context, and all case management actions

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Case ID | text (readonly) | N/A | Unique case identifier (e.g., CASE-2025-12345) | Display only |
| Case Title | text (readonly, editable via edit mode) | Yes | Brief case summary | Max 200 chars |
| Status | badge | Yes | Current case status with color coding (Open, In Progress, Resolved, Closed) | Visual indicator only |
| Priority | badge | Yes | Urgency level with color coding | Visual indicator only |
| Category | text (readonly) | Yes | Case type | Display only |
| Ticket Source | badge | Yes | Origin of support case | Options: Patient App, Provider Portal, Manual Admin Entry; Display only |
| Submitter Type | badge | Yes | Type of user who submitted case | Options: Patient, Provider, Admin; Display only |
| Feedback Resolution | badge | No | Resolution outcome for feedback tickets | Options: Implemented, Planned, Declined, Under Review; Only displayed for feedback/feature request tickets |
| Created Date | datetime (readonly) | N/A | Case creation timestamp | Display only |
| Last Updated | datetime (readonly) | N/A | Most recent modification timestamp | Display only |
| Assigned To | text with avatar | No | Admin staff member handling case (informational only) | Display name and profile photo |
| Linked Patient | link | No | Patient name and HPID (if linked) | Clickable link to patient record in A-01; only available if case is linked to patient |
| Linked Provider | link | No | Provider clinic name and ID (if linked) | Clickable link to provider record in A-02; only available if case is linked to provider |
| Description | text block | Yes | Full case details (initial submission) | Display only (editable via edit mode) |
| Communication Thread | threaded conversation component | N/A | Two-way conversation thread showing messages from admin, patient, and provider with full message content and context | Scrollable, chronological (oldest first), shows sender name, avatar, timestamp, message content |
| Case Timeline | vertical timeline component | N/A | Comprehensive timeline showing all case events with full context: case creation, status changes, feedback resolution updates, assignments, reassignments, internal notes, attachments, account interventions, case reopening | Readonly, scrollable, reverse chronological (newest first) |
| Add Internal Note Button | button | N/A | Allows admin to add internal note to case (not visible to patient/provider) | Opens note entry modal |
| Reply to Patient/Provider Button | button | N/A | Allows admin to send message in communication thread (visible to patient/provider) | Opens message composition modal; sends notification email |
| Update Status Button | button | N/A | Changes case status (Open → In Progress → Resolved → Closed) | Opens status change modal |
| Resolve Case Button | button | N/A | Marks case as Resolved with resolution summary | Opens resolution modal (Screen 5); only enabled for In Progress cases |
| Reassign Case Button | button | N/A | Transfers case to another admin (informational only) | Opens reassignment modal (Screen 6) |
| Reopen Case Button | button | N/A | Reopens closed case (changes status from Closed to Open) | Opens reopen reason modal; only visible for Closed cases |
| Close Case Button | button | N/A | Marks case as Closed (only enabled if status is Resolved) | Confirmation required |
| Edit Case Button | button | N/A | Opens case edit form (Screen 2) to modify case details | Enabled for all statuses |

**Communication Thread Structure**:

Each message in the thread displays:

- **Sender**: Name and avatar (Admin Staff Name, Patient Name, or Provider Clinic Name)
- **Sender Type Badge**: Admin / Patient / Provider
- **Timestamp**: Date and time of message
- **Message Content**: Full message text with formatting support
- **Attachments**: If any, displayed as downloadable links/thumbnails
- **Read Status**: Indicates if patient/provider has viewed the message (future enhancement)

**Timeline Event Types with Full Context**:

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
- **Case Reopened**: Shows who reopened it, reason for reopening, previous resolution summary
- **Case Closed**: Shows who closed it, auto-close vs manual close indicator

**Business Rules**:

- Communication Thread displays messages in chronological order (oldest first) to show conversation flow
- Timeline displays events in reverse chronological order (newest first) to show latest updates
- Timeline shows full context for each event, not just milestones - includes all details of what happened
- Patient and provider can reply to admin messages from their apps (FR-035, FR-032), creating two-way conversation
- When patient/provider replies, message appears in Communication Thread and timeline logged as "Message Received from [Patient/Provider]"
- Admin messages sent via "Reply to Patient/Provider" button appear in Communication Thread and trigger email notification via S-03
- Internal Notes only visible to admin staff with appropriate permissions (not shown in Communication Thread, only in Timeline with "Admin Only" badge)
- Messages to patient/provider logged in both Communication Thread and Timeline
- Status transitions follow lifecycle: Open → In Progress → Resolved → Closed (cannot skip stages except for reopening)
- System prevents closing case unless status is "Resolved" first
- Linked Patient/Provider names clickable to deep-link to patient/provider management modules (only if case is linked)
- Deep-link buttons only visible when case is linked to patient or provider record
- "Reopen Case" button only visible when case status is "Closed"
- "Resolve Case" button only visible when case status is "In Progress"
- All admins can view and work on all cases regardless of assignment (assignment is informational only)

**Notes**:

- Use expandable/collapsible timeline entries for long notes, messages, or intervention details
- Display attachment thumbnails in timeline and communication thread with download links
- Highlight urgent cases with red border and alert icon
- Display warning if case has been open for >7 days without status update
- Show unread message count badge if patient/provider has sent new messages since last admin view
- Use different visual styling for admin messages vs patient/provider messages in Communication Thread (similar to chat interface)
- Consider implementing @ mentions for internal notes to notify specific admin team members (future enhancement)

---

### Screen 4: Case Resolution Modal

**Purpose**: Allows admin to document case resolution and close case with resolution summary

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Resolution Summary | textarea | Yes | Brief description of how issue was resolved | Min 20 chars, max 1000 chars |
| Resolution Category | dropdown select | Yes | Type of resolution | Options: Issue Fixed, Information Provided, Account Intervention, Escalated to Provider, User Error, Cannot Reproduce, Duplicate Case, Other |
| Feedback Resolution | dropdown select | No | Resolution outcome for feedback/feature request tickets (optional) | Options: Implemented, Planned, Declined, Under Review; Only displayed and applicable for Category = Feature Request, Bug Report, or Feedback |
| Root Cause | dropdown select | No | Underlying cause of issue (for analytics) | Options: User Confusion, Technical Bug, Account Configuration, Payment Gateway Issue, Provider Error, System Outage, Other |
| Send Resolution Email | checkbox | Yes | Send email to patient/provider with resolution summary | Default: checked |
| Auto-Close After | dropdown select | Yes | Days to wait before auto-closing case | Options: Immediately, 3 days, 7 days, 14 days (default: 7 days) |
| Internal Resolution Notes | textarea | No | Admin-only notes about resolution (not sent to patient/provider) | Max 2000 chars |
| Mark as Resolved Button | button | Yes | Changes case status to Resolved and logs resolution details | Saves and closes modal |
| Cancel Button | button | Yes | Closes modal without saving | No changes made |

**Business Rules**:

- Resolution Summary included in email sent to patient/provider (if Send Resolution Email checked)
- Feedback Resolution field only visible when case Category = Feature Request, Bug Report, or Feedback
- Feedback Resolution tracks outcome independently of case status (e.g., case can be Resolved with Feedback Resolution = Planned)
- Feedback Resolution included in resolution email to submitter if populated
- Internal Resolution Notes only visible to admin staff (not included in patient/provider-facing communications)
- System automatically closes case after specified auto-close period if patient/provider doesn't respond
- If patient/provider responds before auto-close period expires, case reopened automatically
- Resolution Category and Root Cause captured for analytics and trend identification
- System logs resolution timestamp, feedback resolution (if applicable), and admin user who marked case resolved
- Case cannot be marked Resolved without entering Resolution Summary

**Notes**:

- Use plain language in Resolution Summary field guidance: "Explain to the patient/provider how their issue was resolved"
- For feedback tickets, display guidance: "Select Feedback Resolution to communicate outcome to submitter (e.g., 'Implemented in version 2.5', 'Planned for Q2 2026', 'Declined due to technical constraints')"
- Preview resolution email content before sending (including Feedback Resolution if applicable)
- Display warning if case was open for >14 days: "This case took longer than average to resolve. Consider documenting learnings."

---

### Screen 5: Reassign Case Modal

**Purpose**: Allows admin to reassign case to another admin team member with reason tracking for informational purposes

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Current Assignee | text (readonly) | N/A | Current admin user assigned to case (or "Unassigned") | Display only |
| New Assignee | dropdown select | Yes | Admin user to reassign case to | List of active admin users with "Support Staff" role; cannot select current assignee |
| Reassignment Reason | textarea | Yes | Reason for reassigning case | Min 10 chars, max 500 chars |
| Notify New Assignee | checkbox | Yes | Send email notification to new assignee | Default: checked |
| Reassign Case Button | button | Yes | Confirms reassignment and updates case | Saves and closes modal |
| Cancel Button | button | Yes | Closes modal without saving | No changes made |

**Business Rules**:

- Assignment is informational only - all admins can view and work on all cases regardless of assignment
- System logs reassignment in case timeline with timestamp, old assignee, new assignee, reason, and admin who performed reassignment
- If "Notify New Assignee" checked, system sends email notification via S-03 with case details and reassignment reason
- Reassignment does not change case status or restrict access for other admins
- Admin can reassign case to themselves or to another team member
- System displays reassignment history in case timeline to track case ownership changes

**Notes**:

- Display new assignee's current case load (number of Open/In Progress cases) to help with workload balancing
- Consider adding "Reassign to Team" option for assigning to a team rather than individual (future enhancement)
- Show assignee availability status if integrated with admin calendar (future enhancement)

---

### Screen 6: Reopen Case Modal

**Purpose**: Allows admin to reopen closed case when patient/provider indicates issue not fully resolved

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Previous Resolution Summary | text (readonly) | N/A | Resolution summary from when case was previously resolved | Display only |
| Previous Closure Date | datetime (readonly) | N/A | Date when case was closed | Display only |
| Reopening Reason | textarea | Yes | Reason for reopening case (e.g., "Patient reports issue persists") | Min 20 chars, max 1000 chars |
| Assign To | dropdown select | No | Admin user to assign reopened case to | List of active admin users; optional, defaults to previous assignee if available |
| New Priority | dropdown select | Yes | Priority level for reopened case | Options: Low, Medium, High, Urgent; defaults to previous priority |
| Notify Patient/Provider | checkbox | Yes | Send email to patient/provider acknowledging case reopening | Default: checked |
| Reopen Case Button | button | Yes | Changes case status from Closed to Open and logs reopening | Saves and closes modal |
| Cancel Button | button | Yes | Closes modal without reopening case | No changes made |

**Business Rules**:

- Case status changes from "Closed" to "Open" when reopened
- System logs reopening in case timeline with timestamp, reopening reason, admin who reopened it, and reference to previous resolution
- If "Notify Patient/Provider" checked, system sends email notification via S-03 acknowledging case reopening
- Reopened case appears in default case listing view (Open status)
- Previous resolution summary remains in case history for reference
- Case timeline shows clear "Case Reopened" event with full context of why it was reopened
- Admin can adjust priority when reopening to reflect urgency (e.g., escalate if issue was marked resolved incorrectly)

**Notes**:

- Display previous communication thread and resolution summary above form for context
- Consider adding "Reopen Reason Templates" for common scenarios (e.g., "Issue persists", "New information received", "Resolution did not work") (future enhancement)
- Show time elapsed since case was closed (e.g., "Closed 3 days ago")

---

### Screen 7: Support Center Configuration (Settings Path)

**Purpose**: Allows Super Admin and authorized admin staff to manage centralized lists and configuration options for Support Center module (accessed via Settings > Support Center)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| **Section 1: Case Categories** | section header | N/A | Manage centralized case category list | N/A |
| Category List Table | data table | N/A | Displays all case categories with columns: Category Name, Display Order, Status (Active/Inactive), Used Count, Actions (Edit, Deactivate/Activate, Delete) | Sortable by display order; cannot delete categories with active cases |
| Add Category Button | button | N/A | Opens modal to add new case category | Click action |
| Category Name (in modal) | text input | Yes | Name of case category | Max 50 chars; must be unique; Examples: Technical Issue, Account Access, Payment Question, Booking Issue, General Inquiry, Provider Support, Patient Support, Feature Request, Bug Report, Feedback |
| Category Display Order (in modal) | number input | Yes | Sort order for dropdown display (1-100) | Must be positive integer; determines order in dropdown lists |
| Category Status (in modal) | toggle | Yes | Active or Inactive | Inactive categories hidden from new case creation but preserved for existing cases |
| **Section 2: Case Priorities** | section header | N/A | Manage centralized case priority list | N/A |
| Priority List Table | data table | N/A | Displays all priorities with columns: Priority Name, Color Code, Display Order, Status (Active/Inactive), Used Count, Actions (Edit, Deactivate/Activate, Delete) | Sortable by display order; cannot delete priorities with active cases |
| Add Priority Button | button | N/A | Opens modal to add new priority level | Click action |
| Priority Name (in modal) | text input | Yes | Name of priority level | Max 20 chars; must be unique; Examples: Low, Medium, High, Urgent |
| Priority Color Code (in modal) | color picker | Yes | Badge color for priority display | Options: gray, blue, orange, red, green, purple |
| Priority Display Order (in modal) | number input | Yes | Sort order for dropdown display (1-10) | Must be positive integer |
| Priority Status (in modal) | toggle | Yes | Active or Inactive | Inactive priorities hidden from new case creation |
| **Section 3: Resolution Categories** | section header | N/A | Manage resolution category options | N/A |
| Resolution Category List Table | data table | N/A | Displays all resolution categories with columns: Category Name, Display Order, Status (Active/Inactive), Used Count, Actions (Edit, Deactivate/Activate, Delete) | Sortable by display order |
| Add Resolution Category Button | button | N/A | Opens modal to add new resolution category | Click action |
| Resolution Category Name (in modal) | text input | Yes | Name of resolution category | Max 50 chars; must be unique; Examples: Issue Fixed, Information Provided, Account Intervention, Escalated to Provider, User Error, Cannot Reproduce, Duplicate Case, Other |
| Resolution Category Display Order (in modal) | number input | Yes | Sort order for dropdown display (1-100) | Must be positive integer |
| Resolution Category Status (in modal) | toggle | Yes | Active or Inactive | Inactive categories hidden from resolution modal |
| **Section 4: Root Cause Options** | section header | N/A | Manage root cause options for analytics | N/A |
| Root Cause List Table | data table | N/A | Displays all root cause options with columns: Root Cause Name, Display Order, Status (Active/Inactive), Used Count, Actions (Edit, Deactivate/Activate, Delete) | Sortable by display order |
| Add Root Cause Button | button | N/A | Opens modal to add new root cause option | Click action |
| Root Cause Name (in modal) | text input | Yes | Name of root cause | Max 50 chars; must be unique; Examples: User Confusion, Technical Bug, Account Configuration, Payment Gateway Issue, Provider Error, System Outage, Other |
| Root Cause Display Order (in modal) | number input | Yes | Sort order for dropdown display (1-100) | Must be positive integer |
| Root Cause Status (in modal) | toggle | Yes | Active or Inactive | Inactive options hidden from resolution modal |
| **Section 5: Case Tags** | section header | N/A | Manage custom case tags for categorization | N/A |
| Tag List Table | data table | N/A | Displays all tags with columns: Tag Name, Color, Used Count, Actions (Edit, Delete) | Sortable by tag name; can delete tags even if used (removes from cases) |
| Add Tag Button | button | N/A | Opens modal to add new tag | Click action |
| Tag Name (in modal) | text input | Yes | Name of tag | Max 30 chars; must be unique; Examples: Bug, Feature Request, Urgent, VIP |
| Tag Color (in modal) | color picker | Yes | Badge color for tag display | Options: gray, blue, orange, red, green, purple, yellow, pink |
| **Section 6: Auto-Escalation Rules** | section header | N/A | Configure automatic case escalation thresholds | N/A |
| Urgent Case Unassigned Threshold | number input | Yes | Hours before urgent unassigned case auto-escalates to support manager | Min: 1, Max: 48, Default: 24 hours |
| High Priority Case Threshold | number input | Yes | Hours before high priority case auto-escalates if no status change | Min: 12, Max: 72, Default: 48 hours |
| Case Inactivity Threshold | number input | Yes | Days before case with no activity flagged for admin review | Min: 7, Max: 90, Default: 14 days |
| **Section 7: Reopen Reason Templates** | section header | N/A | Manage reopening reason templates for quick selection (optional) | N/A |
| Reopen Reason Templates Table | data table | N/A | Displays templates with columns: Template Text, Used Count, Actions (Edit, Delete) | Optional feature; admins can also enter custom reasons |
| Add Template Button | button | N/A | Opens modal to add new template | Click action |
| Template Text (in modal) | text input | Yes | Pre-written reopening reason text | Max 200 chars; Examples: "Issue persists", "New information received", "Resolution did not work", "Patient reported problem still occurring" |
| Save Configuration Button | button | Yes | Saves all changes to configuration | Validates all fields; updates centralized lists immediately |
| Cancel Button | button | Yes | Discards unsaved changes | Confirmation required if changes exist |

**Business Rules**:

- Only Super Admin and admin users with "Manage Support Configuration" permission can access this screen
- Configuration screen accessible via Settings > Support Center path in admin navigation
- All changes to centralized lists take effect immediately for new case creation and case updates
- Cannot delete categories, priorities, or resolution categories that are currently used by active cases (status = Open or In Progress)
- Can deactivate items instead of deleting; deactivated items hidden from dropdowns but preserved for historical data
- Used Count shows number of cases currently using each option (helps prevent accidental deletion of important items)
- Display Order determines the sequence items appear in dropdown lists throughout Support Center
- Feedback Resolution options (Implemented, Planned, Declined, Under Review) are fixed in codebase (not configurable) to maintain consistency across product feedback tracking
- Auto-escalation thresholds configurable within defined ranges to prevent overly aggressive or too lenient escalation
- All configuration changes logged in audit trail with timestamp, admin user ID, and change description
- System validates uniqueness of names within each category to prevent duplicates
- Reopen Reason Templates are optional; admins can always enter custom reasons even if templates exist
- **Notification templates and rules** for support case notifications (case created, status changed, admin replied, case resolved, case closed) are managed in FR-030 (Notification Rules & Configuration), not in this screen

**Notes**:

- Use drag-and-drop interface for reordering display order (alternative to manual number entry)
- Show warning when attempting to delete item with active usage: "X cases currently use this [category/priority]. Please deactivate instead."
- Display "Default" badge for system-required items that cannot be deleted (e.g., "Open", "Closed" statuses if applicable)
- Consider adding import/export functionality for configuration backup and migration across environments (future enhancement)
- Show last modified timestamp and admin user for each configuration item
- Provide bulk actions for activating/deactivating multiple items at once

---

## Business Rules

### General Module Rules

- **Rule 1**: All support cases must have unique case IDs generated sequentially (format: CASE-YYYY-#####)
- **Rule 2**: **Unified Status Workflow**: Case lifecycle follows strict progression: Open → In Progress → Resolved → Closed (consistent across all ticket types and sources; cannot skip stages, except for case reopening)
- **Rule 3**: Cases can be reopened after closure if patient/provider indicates issue not fully resolved
- **Rule 4**: **Ticket Source Tracking**: All cases must have Ticket Source (Patient App, Provider Portal, Manual Admin Entry) to identify submission origin
- **Rule 5**: **Submitter Type Tracking**: All cases must have Submitter Type (Patient, Provider, Admin) to identify who submitted the case
- **Rule 6**: **Feedback Resolution Tracking**: Cases with Category = Feature Request, Bug Report, or Feedback can optionally track Feedback Resolution (Implemented, Planned, Declined, Under Review) independently of case status
- **Rule 7**: **Centralized Category Management**: Case categories managed in centralized list (Technical Issue, Account Access, Payment Question, Booking Issue, General Inquiry, Provider Support, Patient Support, Feature Request, Bug Report, Feedback) to ensure consistency across all case submissions
- **Rule 8**: **Centralized Priority Management**: Case priorities managed in centralized list (Low, Medium, High, Urgent) to ensure consistent prioritization across system
- **Rule 9**: **Assignment is Informational Only**: All admin staff can view and work on all cases regardless of assignment; assignment field is for informational/organizational purposes only and does not restrict access
- **Rule 10**: **Two-Way Communication Support**: Patients and providers can reply to admin messages from their apps (FR-035, FR-032), creating threaded conversation within case
- **Rule 11**: **Comprehensive Timeline with Full Context**: Case timeline shows all events with complete details and context (not just milestones), including full message content, intervention details, status change reasons, etc.
- **Rule 12**: Maximum case resolution time target: 48 hours for Urgent, 5 business days for High, 10 business days for Medium/Low priority
- **Rule 13**: Cases with no activity for >14 days flagged for admin review and potential closure
- **Rule 14**: Support cases distinct from aftercare communications (FR-011) and provider-patient messaging (FR-012)
- **Rule 15**: Admin staff can link multiple cases to same patient/provider for trend analysis
- **Rule 16**: Support cases support patient submissions (FR-035), provider submissions (FR-032), and manual admin entries in single unified system
- **Rule 17**: When patient/provider replies to case, message appears in Communication Thread and triggers email notification to assigned admin (or all support staff if unassigned)

### Data & Privacy Rules

- **Privacy Rule 1**: Patient full names, contact details, and medical information visible to admin users granted Support Center access via RBAC; within Support Center, all cases are visible regardless of assignment
- **Privacy Rule 2**: Support case data encrypted at rest (AES-256) and in transit (TLS 1.3)
- **Privacy Rule 3**: Case timeline and all messages logged with immutable audit trail (cannot be deleted, only appended)
- **Privacy Rule 4**: Internal Notes visible only to admin staff with "View Internal Notes" permission (not visible to patients/providers)
- **Privacy Rule 5**: Patient/provider can request case data export for GDPR compliance via data subject access request
- **Audit Rule**: All access to support cases logged with timestamp, admin user ID, IP address, and action performed
- **HIPAA/GDPR**: Support cases may contain medical information; handle as PHI with healthcare-grade security
- **Data Retention**: Support cases retained for minimum 10 years (meets 7-year healthcare minimum and aligns with audit-trail retention requirements); archive after closure, do not hard delete

### Admin Editability Rules

**Editable by Admin (via Admin Platform UI)**:

- Case category, priority, status, title, description (per-case editing in Screen 2)
- Case assignment (transfer to another admin user via Screen 5)
- Internal notes and admin-only comments (in Screen 3)
- Patient/provider linkage (add, modify, or remove linked records in Screen 2)
- Case tags and labels (per-case in Screen 2)
- Resolution summary and resolution category (in Screen 4)
- Auto-close period (3, 7, or 14 days after resolution in Screen 4)

**Configurable by Super Admin (via Settings > Support Center - Screen 7)**:

- Case categories list (add, edit, deactivate, reorder)
- Case priorities list (add, edit, deactivate, reorder, color coding)
- Resolution categories list (add, edit, deactivate, reorder)
- Root cause options list (add, edit, deactivate, reorder)
- Case tags master list (add, edit, delete, color coding)
- Auto-escalation thresholds (configurable within defined ranges: 1-48 hours for urgent cases, 12-72 hours for high priority, 7-90 days for inactivity)
- Reopen reason templates (add, edit, delete)

**Fixed in Codebase (Not Editable)**:

- Case lifecycle stages (Open, In Progress, Resolved, Closed)
- Feedback Resolution options (Implemented, Planned, Declined, Under Review)
- Case ID format and generation logic (CASE-YYYY-#####)
- Ticket Source options (Patient App, Provider Portal, Manual Admin Entry)
- Submitter Type options (Patient, Provider, Admin)
- Audit trail structure and immutability
- Encryption algorithms (AES-256 for data at rest, TLS 1.3 for data in transit)
- Maximum attachment size (10MB per file)

**Configurable with Restrictions (via FR-030: Notification Rules & Configuration)**:

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

- **Notification Rule 1**: Patients receive email notifications when:
  - Support case created (optional confirmation)
  - Case status changes to "In Progress" (admin is working on it)
  - Admin sends message/reply to patient
  - Case marked "Resolved" with resolution summary
  - Case closed
- **Notification Rule 2**: Providers receive email notifications when:
  - Support case created for their inquiry
  - Admin sends message/reply to provider
  - Case marked "Resolved" with resolution summary
- **Notification Rule 3**: Admin staff receive email notifications when:
  - Case assigned to them
  - Case escalated to them
  - Patient/provider responds to case (reopens closed case)
  - Urgent case created and unassigned for >1 hour
- **Notification Rule 4**: All notifications sent via S-03 Notification Service with retry logic for failed sends
- **Notification Rule 5**: Email notifications include case ID, title, status, and direct link to admin case view (for admin recipients)

---

## Success Criteria

### Patient Experience Metrics

- **SC-001**: Patients receive confirmation that their support inquiry was received within 1 hour of contacting Hairline
- **SC-002**: 80% of patient support cases resolved within 48 hours for urgent issues, 5 business days for non-urgent issues
- **SC-003**: Patients receive at least one status update within 24 hours of case creation
- **SC-004**: 90% of patients report satisfaction with support response time and resolution quality (future: post-resolution survey)

### Provider Efficiency Metrics

- **SC-005**: Providers receive response to operational questions within 24 hours for 90% of inquiries
- **SC-006**: Provider support cases resolved within 48 hours for technical issues, 5 business days for operational questions

### Admin Management Metrics

- **SC-007**: Admins can create and assign new support case within 2 minutes
- **SC-008**: Admins can view complete case history and timeline in single screen without needing to navigate multiple views
- **SC-009**: Support managers can view real-time dashboard of open, urgent, and unassigned cases
- **SC-010**: 100% of support cases linked to patient or provider records for traceability

### System Performance Metrics

- **SC-012**: Support case creation completes within 2 seconds for 95% of requests
- **SC-013**: Case list view loads within 3 seconds with 1000+ cases in system
- **SC-014**: Case detail view loads within 2 seconds including full timeline history
- **SC-015**: Case search returns results within 1 second for keyword searches
- **SC-016**: System supports 50 concurrent admin users managing support cases without performance degradation
- **SC-017**: 99.9% uptime for Support Center module

### Business Impact Metrics

- **SC-018**: Support case system reduces average resolution time by 40% compared to email-only support
- **SC-019**: Support case analytics identify top 5 recurring issues within first 30 days of launch
- **SC-020**: Admin staff handle 50% more support inquiries per day with structured case management
- **SC-021**: Patient support-related inquiries organized and trackable with zero lost or forgotten cases
- **SC-022**: Audit trail completeness: 100% of support interactions logged with timestamp and admin attribution

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **FR-035 / Module P-08: Help Center & Support Access**
  - **Why needed**: Patient-submitted support requests and feedback automatically create support cases in FR-034 system
  - **Integration point**: Patient submissions via FR-035 create support cases with Ticket Source = "Patient App" and Submitter Type = "Patient"; patients view case status and admin responses via FR-035

- **FR-032 / Module PR-06: Provider Dashboard Settings & Help Centre**
  - **Why needed**: Provider-submitted support requests (Screen 5.5) and feedback (Screen 5.6) automatically create support cases in FR-034 system
  - **Integration point**: Provider submissions via FR-032 create support cases with Ticket Source = "Provider Portal" and Submitter Type = "Provider"; providers view case status and admin responses via FR-032

- **FR-033 / Module A-09: Help Centre Content Management**
  - **Why needed**: Help Centre content managed by admins for both provider and patient audiences; referenced in FR-032 and FR-035 submission forms
  - **Integration point**: Support Center does not directly integrate with FR-033; FR-033 provides content displayed in FR-032 and FR-035 Help Centres

- **FR-031 / Module A-10: Admin Access Control & Permissions**
  - **Why needed**: Support staff roles and permissions (View Cases, Edit Cases, Reassign Cases, View Internal Notes) managed via RBAC system
  - **Integration point**: Support Center enforces permission checks before allowing admin users to access or modify cases

- **FR-016 / Module A-01: Patient Management & Oversight**
  - **Why needed**: Support cases linked to patient records by HPID, email, or phone number
  - **Integration point**: Deep-link from support case to patient detail view; patient detail view displays linked support cases

- **FR-015 / Module A-02: Provider Management**
  - **Why needed**: Provider support cases linked to provider records by provider ID or clinic name
  - **Integration point**: Deep-link from support case to provider detail view; provider detail view displays linked support cases

- **FR-020 / Module S-03: Notification Service**
  - **Why needed**: Send email and push notifications to patients, providers, and admin staff for case updates, assignments, and resolutions
  - **Integration point**: Support Center calls S-03 API to trigger notification events (support.case_created, support.case_assigned, support.case_status_changed, support.case_admin_reply, support.case_user_reply, support.case_resolved, support.case_reopened, support.case_closed, support.case_escalated); S-03 delivers notifications based on rules configured in FR-030

- **FR-030 / Module A-09: Notification Rules & Configuration**
  - **Why needed**: Centralized management of support case notification templates, delivery channels, timing, and recipient rules
  - **Integration point**: Support case notification event types defined in FR-030 Admin-Configurable Notification Event Catalog (Messaging/Support category); admin configures templates and rules via Settings → Alerts & Notifications

- **FR-026 / Module A-09: App Settings & Security**
  - **Why needed**: Security settings (admin session timeout, audit logging) apply to Support Center module
  - **Integration point**: Support Center enforces security policies configured in A-09

### External Dependencies (APIs, Services)

- **None for MVP**: Support Center operates entirely within Hairline platform with no external API dependencies
- **Future Enhancement**: Integration with external ticketing systems (Zendesk, Freshdesk) for advanced support workflows

### Data Dependencies

- **Entity 1: Patient Records**
  - **Why needed**: Cannot link support cases to patients without active patient accounts
  - **Source**: Patient onboarding and authentication (FR-001)

- **Entity 2: Provider Records**
  - **Why needed**: Cannot link provider support cases without active provider accounts
  - **Source**: Provider onboarding (FR-015)

- **Entity 3: Admin User Accounts**
  - **Why needed**: Cannot assign cases to admin staff without active admin user accounts with appropriate roles
  - **Source**: Admin user management (FR-031)

- **Entity 4: Notification Templates**
  - **Why needed**: Email notifications require predefined templates for case status updates
  - **Source**: Notification configuration (FR-030)

---

## Assumptions

### User Behavior Assumptions

- **Assumption 1**: Patients and providers will use in-app submission (FR-035 and FR-032) as primary method for contacting support; email/phone submissions become secondary channels
- **Assumption 2**: Admin staff will manually create support cases from incoming emails and phone calls for users who contact via external channels
- **Assumption 3**: Majority of support cases resolve within 48-72 hours with single admin response
- **Assumption 4**: Patients and providers check email regularly for case status updates (email is primary notification channel)
- **Assumption 5**: Admin staff use standardized resolution categories and feedback resolution options for consistent case analytics
- **Assumption 6**: Users will appreciate unified status workflow (Open → In Progress → Resolved → Closed) for consistency across all ticket types

### Technology Assumptions

- **Assumption 1**: Admin staff access Support Center via modern web browsers (Chrome, Safari, Firefox, Edge - last 2 versions)
- **Assumption 2**: Email delivery via S-03 Notification Service is reliable with >95% delivery rate
- **Assumption 3**: System handles up to 500 support cases per day during peak periods
- **Assumption 4**: Case attachments stored in cloud storage (S3 or equivalent) with CDN for fast retrieval
- **Assumption 5**: Database supports full-text search for case keyword searches

### Business Process Assumptions

- **Assumption 1**: Hairline employs dedicated support staff with "Support Agent" role to handle cases
- **Assumption 2**: Support staff available during business hours (8am-6pm UTC) for case assignment and resolution
- **Assumption 3**: Urgent cases escalated to support manager if unresolved after 24 hours
- **Assumption 4**: Resolved cases auto-close after 7 days if patient doesn't respond (configurable)
- **Assumption 5**: Support case data retained for 10 years minimum for compliance and dispute resolution

---

## Implementation Notes

### Technical Considerations

- **Architecture**: Support Center requires real-time case status updates; consider using WebSocket or Server-Sent Events (SSE) for live dashboard updates to avoid polling
- **Performance**: Case timeline with hundreds of events requires pagination or lazy loading to prevent slow page loads
- **Search**: Implement full-text search index on case title, description, notes, and patient/provider names for fast keyword searches
- **Storage**: Case attachments stored in cloud object storage (S3) with pre-signed URLs for secure, time-limited access
- **Audit Trail**: Use append-only database table or event sourcing pattern for immutable case timeline history

### Integration Points

- **Integration 1: Patient Management Module (A-01)**
  - **Data format**: Support case links to patient record via HPID (Hairline Patient ID)
  - **Authentication**: Admin session JWT token with RBAC permissions
  - **Error handling**: If patient record deleted, support case retains anonymized copy of patient name/email for audit trail

- **Integration 2: Provider Management Module (A-02)**
  - **Data format**: Support case links to provider record via provider ID or clinic name
  - **Authentication**: Admin session JWT token with RBAC permissions
  - **Error handling**: If provider record deactivated, support case retains provider name for historical reference

- **Integration 3: Notification Service (S-03)**
  - **Data format**: JSON payload with case ID, recipient email, notification type, case details
  - **Authentication**: Internal service-to-service authentication (API key or mutual TLS)
  - **Error handling**: If notification fails, log error and retry up to 3 times with exponential backoff; mark notification as failed in case timeline

### Scalability Considerations

- **Current scale**: Expected 100-200 support cases per day at launch
- **Growth projection**: Plan for 1000 cases per day within 12 months as patient base grows
- **Peak load**: Handle 50 concurrent case creations during marketing campaigns or system outages (10x normal)
- **Data volume**: Expect 500KB average case size (text + attachments); 100GB total storage in year 1
- **Scaling strategy**: Horizontal scaling of API servers; database read replicas for case search and reporting; CDN for attachment delivery

### Security Considerations

- **Authentication**: Admin staff authenticate via FR-031 (Admin Access Control). MFA is enforced once the shared MFA stack (FR-026 / FR-031) is delivered; until then, implement strong password policies, throttling, and re-authentication flows per Constitution.
- **Authorization**: Role-Based Access Control (RBAC) enforces granular permissions:
  - Support Agent: Create, view, edit, and resolve cases (assignment is informational only and does not restrict access)
  - Support Manager: View all cases, reassign cases, access case analytics
  - Super Admin: Full access including configuration management and audit log export (no hard delete; archive only)
- **Encryption**: All case data encrypted at rest (AES-256) and in transit (TLS 1.3)
- **Audit trail**: Every case access, modification, and status change logged with timestamp, admin user ID, IP address, and action
- **Threat mitigation**: Rate limiting on case creation API (max 60 cases/hour per admin user) to prevent abuse
- **Compliance**: HIPAA-compliant handling of patient medical information in case descriptions and attachments; GDPR data export support for patient right to access

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

Support manager searches for all urgent cases assigned to specific team member to ensure timely resolution.

**Why this priority**: Essential for support management and oversight - managers must be able to monitor workload and prioritize urgent issues

**Independent Test**: Can be tested by creating multiple test cases with different priorities, statuses, and assignments, then verifying search and filters return correct results

**Acceptance Scenarios**:

1. **Given** support manager is on Support Center dashboard, **When** manager navigates to "All Cases" view, **Then** system displays case list with default filters (Open + In Progress cases from last 30 days)
2. **Given** manager is viewing case list, **When** manager selects "Urgent" priority filter and specific admin user from "Assigned To" filter, **Then** system displays only urgent cases assigned to that user
3. **Given** filtered case list is displayed, **When** manager clicks case row, **Then** system navigates to case detail view with full timeline

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

Support agent encounters complex technical issue requiring senior staff; escalates case to technical team.

**Why this priority**: Important for handling complex cases but less frequent than standard support workflows

**Independent Test**: Can be tested by creating case, then escalating it to verify priority increase and notification

**Acceptance Scenarios**:

1. **Given** support agent is reviewing case involving system outage, **When** agent determines escalation needed, **Then** agent clicks "Escalate Case" button
2. **Given** escalation modal is displayed, **When** agent selects "Technical Team" as escalation recipient and enters escalation reason "Database connection errors", **Then** system updates case priority to "Urgent"
3. **Given** case is escalated, **When** system processes escalation, **Then** system sends email notification to technical team and logs escalation in case timeline
4. **Given** technical team receives notification, **When** team member opens case, **Then** case displays escalation badge and full escalation context

---

### Edge Cases

- **What happens when admin attempts to link case to patient with duplicate email addresses?**
  - System displays list of all patients with matching email and prompts admin to select correct patient by HPID
  - Admin can choose to create case without patient link if ambiguous

- **How does system handle case assignment when assigned admin is deactivated or leaves organization?**
  - System automatically detects deactivated admin accounts and marks their assigned cases as "Unassigned"
  - Support manager receives notification to reassign orphaned cases
  - Case timeline logs admin account deactivation event

- **What occurs if patient deletes their account while support case is open?**
  - Support case remains in system with anonymized patient identifier for audit trail compliance
  - Case marked with "Patient Account Deleted" badge
  - Admin cannot deep-link to patient record but can still close case with resolution notes

- **How to manage attachment upload when file contains malware or virus?**
  - System scans all uploaded files using antivirus service before accepting
  - If malware detected, system rejects upload and displays error: "File rejected due to security scan failure"
  - Admin notified to request patient/provider send file via alternative secure method

- **What happens when two admins simultaneously edit same case?**
  - System uses optimistic locking with "last write wins" strategy
  - If conflict detected, admin receives warning: "This case was modified by another admin. Please review recent changes before saving."
  - Admin can review other admin's changes and decide whether to overwrite or discard their edits

- **How does system handle case search with special characters or SQL injection attempts?**
  - System sanitizes all search input to prevent SQL injection attacks
  - Special characters escaped before executing search query
  - Search limited to alphanumeric characters, spaces, and common punctuation

- **What occurs if S-03 Notification Service is down and cannot send case notification emails?**
  - System queues notification for retry with exponential backoff (retry at 1 min, 5 min, 15 min)
  - Case timeline logs notification failure with timestamp
  - Admin dashboard displays notification status indicator (sent, pending, failed)
  - If notification fails after 3 retries, admin receives alert to manually contact patient/provider

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

### Data Requirements

- **REQ-034-030**: System MUST support case categories: Technical Issue, Account Access, Payment Question, Booking Issue, General Inquiry, Provider Support, Patient Support, Feature Request, Bug Report, Feedback
- **REQ-034-031**: System MUST support priority levels: Low, Medium, High, Urgent
- **REQ-034-032**: System MUST support Ticket Source options: Patient App, Provider Portal, Manual Admin Entry
- **REQ-034-033**: System MUST support Submitter Type options: Patient, Provider, Admin
- **REQ-034-034**: System MUST support Feedback Resolution options: Implemented, Planned, Declined, Under Review (optional field for feedback/feature request tickets)
- **REQ-034-035**: System MUST store case description with minimum 20 characters and maximum 5000 characters
- **REQ-034-036**: System MUST support file attachments up to 10MB per file, maximum 5 files per case
- **REQ-034-037**: System MUST support attachment formats: JPG, PNG, PDF, DOC, DOCX
- **REQ-034-038**: System MUST retain all case data for minimum 10 years for compliance (archive after closure, do not hard delete)
- **REQ-034-039**: System MUST capture resolution details: resolution summary, resolution category, feedback resolution (optional), root cause (optional), and resolution timestamp

### Security & Privacy Requirements

- **REQ-034-040**: System MUST encrypt all case data at rest using AES-256 encryption
- **REQ-034-041**: System MUST encrypt all case data in transit using TLS 1.3
- **REQ-034-042**: System MUST enforce RBAC permissions for case access (Support Agent, Support Manager, Super Admin roles)
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

**Note**: Notification templates, delivery timing, channel preferences, and recipient rules for all support case notifications are managed centrally in FR-030 (Notification Rules & Configuration), not in FR-034. Admin configures these via Settings → Alerts & Notifications → Messaging/Support category.

### Case Listing & Reporting Requirements

- **REQ-034-054**: System MUST provide Support Center case listing screen as primary view with quick stats bar displaying: open cases count, in progress count, urgent cases count, unassigned cases count
- **REQ-034-055**: System MUST display case list with comprehensive filters: status, priority, category, ticket source, submitter type, date range, assigned admin, and search functionality
- **REQ-034-056**: System MUST support keyword search across case title, description, notes, and patient/provider names
- **REQ-034-057**: System MUST highlight urgent cases in dashboard and case lists with visual indicators (red badges, alert icons)
- **REQ-034-058**: System MUST display warning for cases open >7 days without status update

### Case Resolution & Closure Requirements

- **REQ-034-059**: System MUST require resolution summary (min 20 chars, max 1000 chars) before case can be marked Resolved
- **REQ-034-060**: System MUST send resolution email to patient/provider when case marked Resolved (if "Send Resolution Email" option enabled)
- **REQ-034-061**: System MUST support auto-closure period: 3, 7, or 14 days after case marked Resolved (default 7 days)
- **REQ-034-062**: System MUST automatically close case after auto-closure period expires if patient/provider doesn't respond
- **REQ-034-063**: System MUST allow admins to reopen closed cases if patient/provider indicates issue not fully resolved
- **REQ-034-064**: System MUST log reopening reason in case timeline when case is reopened

### Performance & Scalability Requirements

- **REQ-034-065**: System MUST complete case creation within 2 seconds for 95% of requests
- **REQ-034-066**: System MUST load case detail view (including timeline) within 2 seconds
- **REQ-034-067**: System MUST return case search results within 1 second for keyword searches
- **REQ-034-068**: System MUST support 50 concurrent admin users managing cases without performance degradation
- **REQ-034-069**: System MUST handle up to 500 case creations per day at launch, scalable to 1000+ cases per day

---

## Key Entities

- **Entity 1 - Support Case**:
  - **Key attributes**: Case ID (unique), case title (required, no auto-generation), category (from centralized managed list), priority (from centralized managed list), status, ticket source, submitter type, feedback resolution (optional), created date, last updated date, assigned admin user ID (informational only), linked patient HPID (optional), linked provider ID (optional), description, resolution summary (when resolved), resolution category, auto-close period
  - **Relationships**: One support case belongs to one patient (optional); one support case belongs to one provider (optional); one support case assigned to one admin user (optional, informational only); one support case has many timeline events; one support case has many messages; one support case has many attachments; patient-submitted cases automatically linked to patient record; provider-submitted cases automatically linked to provider record

- **Entity 2 - Case Message**:
  - **Key attributes**: Message ID, case ID, sender type (Admin, Patient, Provider), sender user ID, message content, message timestamp, read status (unread, read), parent message ID (for threading, optional), attachments (optional)
  - **Relationships**: Many messages belong to one support case; one message sent by one user (admin, patient, or provider); messages form threaded conversation

- **Entity 3 - Case Timeline Event**:
  - **Key attributes**: Event ID, case ID, event type (case created, status changed, feedback resolution changed, note added, message sent, message received, attachment uploaded, case assigned, case reassigned, account intervention performed, case resolved, case reopened, case closed), event timestamp, actor user ID (admin, patient, or provider who performed action), actor type (Admin, Patient, Provider), event description with full context, internal note flag (true if admin-only note), related message ID (if event is message-related), related attachment ID (if event is attachment-related)
  - **Relationships**: Many timeline events belong to one support case; one timeline event created by one actor (admin, patient, or provider)

- **Entity 4 - Case Attachment**:
  - **Key attributes**: Attachment ID, case ID, file name, file size, file type (MIME type), storage URL (S3 or CDN), uploaded timestamp, uploaded by user ID (admin, patient, or provider), uploader type (Admin, Patient, Provider), virus scan status (pending, clean, infected)
  - **Relationships**: Many attachments belong to one support case; one attachment uploaded by one user (admin, patient, or provider)

- **Entity 5 - Case Assignment**:
  - **Key attributes**: Assignment ID, case ID, assigned to admin user ID (informational only), assigned by admin user ID, assignment timestamp, assignment reason (initial assignment, reassignment)
  - **Relationships**: Many assignments belong to one support case (tracks reassignment history); one assignment references one admin user (assignee) and one admin user (assigner); assignment is informational only and does not restrict case access

- **Entity 6 - Case Resolution**:
  - **Key attributes**: Resolution ID, case ID, resolution summary, resolution category (issue fixed, information provided, account intervention, etc.), feedback resolution (optional: Implemented, Planned, Declined, Under Review), root cause (optional), resolved timestamp, resolved by admin user ID, auto-close period (days), closure timestamp (when auto-closed or manually closed), closed by admin user ID (if manually closed)
  - **Relationships**: One resolution belongs to one support case; one resolution created by one admin user

- **Entity 7 - Case Reopening**:
  - **Key attributes**: Reopening ID, case ID, reopening reason, reopening timestamp, reopened by admin user ID, previous resolution reference, new priority (if changed), new assignee (if changed)
  - **Relationships**: Many reopenings belong to one support case (tracks reopening history); one reopening performed by one admin user

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-12-30 | 1.0 | Initial PRD creation for FR-034 Patient Support Center & Ticketing | AI Assistant |
| 2026-01-11 | 1.1 | Added provider-facing support ticket and feedback submission functionality: Updated scope to include provider submissions via Help Centre (FR-032 Screen 5.5 and 5.6); Added workflows for provider Contact Support and Feedback submissions; Added functional requirements for automatic case creation from provider submissions; Updated Support Case entity to include source tracking; Provider submissions automatically create support cases in FR-034 system | AI Assistant |
| 2026-01-16 | 2.0 | Major scope extension to unified multi-tenant support system: Renamed title to "Support Center & Ticketing System" to reflect unified system for both patients and providers; Added patient submission capability via FR-035 (Patient Help Center & Support Submission); Updated Executive Summary to document THREE submission sources (Patient App, Provider Portal, Manual Admin Entry); Updated Multi-Tenant Architecture to include patient platform submission (P-08); Added workflow A5 for patient submissions via FR-035; Implemented **Unified Status Workflow** (Open → In Progress → Resolved → Closed) consistent across all ticket types and sources; Added **Ticket Source** tracking field (Patient App, Provider Portal, Manual Admin Entry); Added **Submitter Type** tracking field (Patient, Provider, Admin); Added **Feedback Resolution** tracking field (Implemented, Planned, Declined, Under Review) for feedback/feature request tickets independent of case status; Updated Screen 2 (Create/Edit Support Case Form) with new fields: Ticket Source, Submitter Type, Feedback Resolution, and expanded Category options; Updated Screen 3 (Support Case Detail View) to display new tracking fields; Updated Screen 5 (Case Resolution & Closure Modal) with Feedback Resolution field and business rules; Updated Business Rules to document unified workflow and new tracking requirements; Updated Dependencies to include FR-035 and FR-032 references; Updated Assumptions to reflect patient and provider in-app submissions as primary method; Updated Functional Requirements Summary with patient submission requirements and unified workflow specifications | AI Assistant |
| 2026-01-26 | 2.1 | Major refinements for systematic consistency and improved UX: **Removed Master Case complexity** (removed duplicate detection workflow A6); **Replaced Admin Dashboard with simple Case Listing screen** as primary view (Screen 1); **Added centralized managed lists** for case categories and priorities to ensure consistency; **Made assignment informational only** - all admins can view and work on all cases regardless of assignment; **Implemented two-way threaded communication** - patients and providers can reply to admin messages from their apps (FR-035, FR-032), creating conversation thread within case; **Enhanced timeline to show comprehensive context** - displays all events with full details and context (not just milestones), including full message content, intervention details, status change reasons, etc.; **Added Reassign Case flow** with Screen 5 (Reassign Case Modal) including reason tracking; **Added Reopen Case flow** with Screen 6 (Reopen Case Modal) with reopening reason and priority adjustment; **Added Screen 7: Support Center Configuration** (Settings > Support Center path) for Super Admin to manage centralized lists (categories, priorities, resolution categories, root causes, tags, auto-escalation rules, reopen reason templates); **Clarified notification management** - removed notification templates from Screen 7 and established FR-030 as source of truth for all support case notification configuration; **Added 9 support case notification event types** to FR-030 and FR-020 (support.case_created, support.case_assigned, support.case_status_changed, support.case_admin_reply, support.case_user_reply, support.case_resolved, support.case_reopened, support.case_closed, support.case_escalated); **Added action buttons to listing screen** (View, Reassign, Resolve, Reopen, Close); **Made Case Title always required** - removed auto-generation rule; **Clarified deep-linking** - only available when case is linked to patient/provider record; **Added detailed search and filter specifications** including Ticket Source and Submitter Type filters; **Updated Multi-Tenant Architecture** to document two-way communication capability; **Added Entity 2 (Case Message)** for communication thread; **Added Entity 7 (Case Reopening)** for reopening tracking; Updated all business rules, screen specifications, functional requirements, admin editability rules, and integration requirements to reflect systematic consistency improvements; **Updated system PRD (FR-035)** to explicitly document patient two-way communication capability with admin | AI Assistant |
| 2026-01-26 | 2.2 | **Removed Case export functionality:** Removed Export Case Button from Screen 3 (Support Case Detail View); Removed Export Filtered Cases Button from Screen 1 (All Cases Listing); Removed Business Scenario B5 (Case Export Failure); Removed User Story 7 (Admin Exports Cases for Compliance Audit); Removed export-related business rules, constraints, and performance metrics (SC-011); Removed REQ-034-034 (case export requirement); Updated REQ-034-024 to focus on internal notes being admin-only without export reference; Removed Export Cases permission from RBAC integration point; Removed maximum case export limit from technical constraints; Case export feature was accidentally included and is now removed from both admin-facing (FR-034) and provider-facing (FR-032) specifications | AI Assistant |
| 2026-01-26 | 2.3 | Constitution alignment updates: Set support case retention to **10 years** (aligns with audit-trail retention; exceeds 7-year minimum); clarified Support Center access semantics (visibility is not restricted by assignment); aligned Provider module naming to **PR-06** (per FR-032); clarified MFA language as dependent on shared MFA stack delivery (FR-026 / FR-031). | AI Assistant |
| 2026-01-26 | 2.4 | Naming alignment: Updated patient Help/Support module references from **P-XX** to **P-08** to match Constitution module breakdown (Help Center & Support Access). | AI Assistant |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | [Name] | [Date] | Pending |
| Technical Lead | [Name] | [Date] | Pending |
| Stakeholder | [Name] | [Date] | Pending |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (PRD Standards & Requirements)  
**Based on**: FR-011 Aftercare & Recovery Management PRD
**Last Updated**: 2026-01-26
