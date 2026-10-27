# FR-016 - Admin Patient Management

**Module**: A-01: Patient Management & Oversight
**Feature Branch**: `fr016-admin-patient-mgmt`
**Created**: 2025-11-11
**Status**: 🟡 Revised — Pending Consolidated Verification
**Source**: FR-016 from system-prd.md; FR-015 v1.9 provider-status cancellation cascade
**Change Request**: [CR-FR016-20261016-01 — MTG-002 quote model alignment](change-request-2026-10-16-mtg002-quote-model-alignment.md) (previous: [CR-FR016-20261014-01 — Provider status cancellation cascade](change-request-2026-10-14-provider-status-cancellation-cascade.md))
**Related Change Request**: [CR-FR020-20261027-01 — Admin-support alert recipients and provider status email timing](../fr020-notifications-alerts/change-request-2026-10-27-admin-support-recipients-status-email-timing.md)

---

## Executive Summary

The Admin Patient Management module provides Hairline internal administrators with comprehensive oversight and management capabilities for all patient accounts and activities across the platform. This module enables admins to monitor the patient journey from initial inquiry through treatment completion, intervene in cases requiring support, and manage patient data while maintaining strict privacy and compliance standards.

This is a critical operational module that ensures the platform can provide effective patient support, resolve disputes, maintain data quality, and comply with regulatory requirements for medical data management.

**Note on Scan Media (V1 vs V2)**: In V1, patient "3D scans" are implemented as standardized head scan photo sets (multiple 2D views; JPG/PNG). An interactive 3D model viewer is a V2 enhancement.

### Business Value

- **Operational Oversight**: Complete visibility into patient activities, treatment status, and platform engagement
- **Patient Support**: Tools to assist patients who encounter issues or need help completing their journey
- **Dispute Resolution**: Capability to investigate and resolve conflicts between patients and providers
- **Data Governance**: Ensure patient data quality, handle privacy requests, and maintain compliance
- **Platform Health**: Monitor patient satisfaction, identify friction points, and improve conversion rates

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-##)**: No direct patient-facing functionality - patients are unaware of admin oversight
- **Provider Platform (PR-##)**: No provider-facing functionality - providers don't see admin interventions
- **Admin Platform (A-01)**: Full patient management interface with search, view, edit, and oversight capabilities
- **Admin Platform Role Model**: Admin roles and permissions follow FR-031 (Admin Access Control & Permissions): default roles Super Admin, Aftercare Specialist, Billing Staff, and Support Staff, plus custom roles
- **Shared Services (S-##)**: Uses S-03 (Notification Service) for alerts and S-05 (Media Storage Service) for accessing patient scans

### Multi-Tenant Breakdown

**Patient Platform (P-##)**:

- No direct functionality in patient app
- Patients may receive notifications when admins take actions on their behalf (password resets, manual interventions)

**Provider Platform (PR-##)**:

- No direct functionality in provider platform
- Providers unaware of admin oversight except when admins mediate disputes

**Admin Platform (A-01)**:

- Complete patient account search and filtering
- View all patient profile information and treatment history
- Access patient medical history, head scan capture assets *(V1 photo set; V2 true 3D)*, and documents
- View complete inquiry, quote, booking, and treatment lifecycle
- Monitor patient-provider communications for compliance
- Manually intervene in bookings (reschedule, modify, cancel)
- Reset patient passwords and unlock accounts
- Suspend or deactivate patient accounts
- View patient support escalations/context via Support Center (see FR-034)
- Generate patient reports and analytics

**Shared Services (S-##)**:

- **S-03: Notification Service**: Sends notifications when admins take actions affecting patients
- **S-05: Media Storage Service**: Provides access to patient head scan assets *(V1 photo set; V2 true 3D)*, photos, documents
- **S-06: Audit Log Service**: Logs all admin actions on patient accounts for compliance

### Communication Structure

**In Scope**:

- Admin viewing patient-provider message history (read-only monitoring)
- Admin viewing patient support history/context via Support Center (see FR-034)
- Admin ability to flag/review communications for policy violations
- System-generated notifications to patients when admin takes action

**Out of Scope**:

- Direct admin-to-patient messaging (handled by Support Center & Ticketing system; see FR-034)
- Admin intercepting or modifying patient-provider messages in real-time

### Entry Points

- Admin logs into admin dashboard and navigates to "Patients" section
- Admin searches for specific patient by name, email, patient code, or ID
- Admin filters patient list by status (inquiry, quoted, scheduled, in-progress, aftercare, completed)
- System alerts admin to patients requiring attention (failed payments, flagged communications, disputes)
- Admin receives escalations requiring account-level intervention (via Support Center; see FR-034)

---

## Business Workflows

### Main Flow: Patient Account Search and Overview

**Actors**: Admin, System
**Trigger**: Admin needs to find and review patient information
**Outcome**: Admin locates patient and views complete profile summary

**Steps**:

1. Admin navigates to "Patients" section in admin dashboard
2. System displays patient list with default filters (recent activity, all statuses)
3. Admin enters search criteria (name, email, patient code, phone) OR applies filters (status, date range, location, provider)
4. System executes search and returns matching patient records
5. System displays results in paginated list with key information:
   - Patient name and code (e.g., "Mark Peterson #HP258742")
   - Current journey stage (Inquiry, Quoted, Accepted, Confirmed, In Progress, Aftercare, Completed, Cancelled), using the FR-003 stage list
   - Registration date
   - Last activity timestamp
   - Provider assignment (if applicable)
   - Flags/alerts (payment issues, compliance concerns, support escalations)
6. Admin clicks on patient row to view detailed profile
7. System loads patient detail view with tabbed sections:
   - **Overview**: Profile summary, contact info, current status
   - **Treatment Journey**: Milestone timeline summarizing journey progress with deep links to the latest case stage/inquiry detail
   - **Medical Data**: Medical questionnaire, head scan assets *(V1 photo set; V2 true 3D)*, health history
   - **Payments**: Payment history, outstanding balances, refunds
   - **Communications**: Message history with providers and support
   - **Admin Actions**: Audit log of admin interventions
8. Admin reviews information and takes action as needed

### Alternative Flows (Manual Intervention)

**A1: Admin views patient treatment milestone timeline**:

- **Trigger**: Admin needs to see complete patient journey from inquiry to completion
- **Steps**:
  1. From patient detail view, admin selects "Treatment Journey" tab
  2. System displays chronological milestone cards (Inquiry submitted, Quote approved, Booking confirmed, Travel complete, Procedure complete, Aftercare checkpoints)
  3. Each milestone surfaces concise status + timestamp and includes a "Open Case Detail" link that launches the dedicated inquiry/case page for full context of that stage
- **Outcome**: Admin understands patient's complete journey and can identify issues

**A2: Admin accesses patient medical data**:

- **Trigger**: Admin needs to review patient medical history or scans for support/dispute resolution
- **Steps**:
  1. From patient detail view, admin selects "Medical Data" tab
  2. System requests admin justification for access (audit trail requirement)
  3. Admin enters reason for accessing medical data
  4. System logs access with timestamp, admin ID, and justification
  5. System displays:
     - Medical questionnaire responses with severity flags (red, yellow, green)
     - Head scan viewer *(V1 photo set gallery; V2 interactive 3D model)*
     - Uploaded photos/videos
     - Declared medications and allergies
     - Previous procedure history
  6. Admin reviews data and closes tab
  7. System marks medical data access in audit log
- **Outcome**: Admin has reviewed necessary medical information; access is fully audited

**A3: Admin views patient payment history**:

- **Trigger**: Admin needs to verify payment status or investigate payment dispute
- **Steps**:
  1. From patient detail view, admin selects "Payments" tab
  2. System displays complete payment history:
     - All successful transactions (deposit, installments, final payment)
     - Failed payment attempts with error reasons
     - Refunds issued with justification
     - Outstanding balances
     - Payment method used
     - Currency and exchange rates
  3. Admin can click on transaction to view Stripe payment intent details
  4. Admin can initiate refund with enhanced confirmation for amounts > $1,000
- **Outcome**: Admin has complete financial picture of patient account

**B1: Admin cannot find patient in search**:

- **Trigger**: Search returns no results
- **Steps**:
  1. System displays "No patients found matching your search criteria"
  2. System suggests broadening search:
     - Remove date range filters
     - Try partial name match
     - Search by phone number instead of email
  3. Admin adjusts search criteria and retries
  4. If still no results, admin checks if patient account exists in different status or was deactivated
- **Outcome**: Admin either finds patient with adjusted search or confirms patient doesn't exist

---

### Main Flow: Manual Patient Intervention

**Actors**: Admin, Patient, System
**Trigger**: Admin needs to modify patient account or booking due to exceptional circumstance
**Outcome**: Admin successfully intervenes, changes are applied, patient notified

**Steps**:

1. Admin locates patient account via search
2. Admin identifies issue requiring intervention (e.g., patient unable to complete payment, account locked, suspected fraud)
3. Admin reviews patient's current status and determines appropriate action
4. Admin selects action from available options:
   - Reset password
   - Unlock account (after failed login attempts)
   - Update patient profile information
   - Suspend account (fraud prevention)
   - Initiate manual refund (when payment service unavailable or support requires override)
   - Log admin note / follow-up task
5. System displays confirmation dialog with:
   - Summary of action to be taken
   - Impact on patient (e.g., "Patient will receive password reset email")
   - Required justification field
6. Admin enters justification for intervention (required for audit compliance)
7. Admin confirms action
8. System executes action:
   - Updates patient account state
   - Logs action in audit trail with admin ID, timestamp, justification
   - Sends notification to patient (if applicable)
9. System displays confirmation: "Action completed successfully"
10. Admin verifies change in patient account

### Alternative Flows

**A4: Admin resets patient password**:

- **Trigger**: Patient unable to access account and contacts support
- **Steps**:
  1. Admin locates patient account
  2. Admin clicks "Reset Password" button
  3. System displays confirmation dialog: "Send password reset email to [patient email]?"
  4. Admin enters justification: "Patient requested password reset via Support Center case #1234"
  5. Admin confirms action
  6. System generates password reset token
  7. System sends email to patient with reset link (6-digit OTP)
  8. System logs admin action in audit trail
  9. System displays: "Password reset email sent to patient"
- **Outcome**: Patient receives reset email and can regain account access

**A6: Admin suspends patient account**:

- **Trigger**: Fraud detection system flags suspicious activity or multiple policy violations
- **Steps**:
  1. Admin reviews flagged patient account
  2. Admin investigates evidence (multiple accounts, payment chargebacks, policy violations)
  3. Admin determines account suspension is necessary
  4. Admin clicks "Suspend Account" button
  5. System displays warning: "This action will immediately prevent patient login and cancel active bookings. Proceed?"
  6. Admin enters detailed justification: "Multiple fraudulent payment attempts - 3 chargebacks in 1 month"
  7. Admin selects suspension duration: 30 days, 90 days, Permanent
  8. Admin confirms suspension
  9. System immediately revokes patient authentication tokens
  10. System cancels each active booking through the FR-006 admin booking cancellation, using the suspension justification as the cancellation reason; refunds follow the FR-006 payment placeholder
  11. System sends suspension notification to patient with appeal process information
  12. System logs suspension in audit trail with full justification
- **Outcome**: Account suspended, patient locked out, audit trail created

*Note: Booking modifications or cancellations occur on the dedicated case/inquiry detail page; the intervention flow links admins there rather than duplicating controls.*

**A8: Admin handles a support-routed booking cancellation or change request**:

- **Trigger**: From subquote acceptance onward the patient has no in-app booking cancellation; the patient uses Contact Support on the FR-006 booking screens, and the request is logged as an FR-034 support case of type booking cancellation or booking change
- **Steps**:
  1. Admin opens the request from Screen 9 (Booking Support Requests) or from the patient's Overview tab
  2. Admin reviews the booking reference, current booking status, current appointment, and the patient's stated reason
  3. For a cancellation request, admin opens the FR-006 Cancel Booking action (FR-006 Screen 9), which applies to any booking state from `Accepted` to `Aftercare`, enters the mandatory reason, and confirms; the booking and inquiry become `Cancelled`, the accepted quote stays accepted, the patient and provider receive `booking.cancelled`, and refunds follow the FR-006 payment placeholder
  4. For a change request, admin opens the FR-006 Change Appointment action (FR-006 Screen 8), which applies to `Accepted` or `Confirmed` bookings; the patient and provider receive `booking.rescheduled`
  5. If the admin declines the request, admin records a decline reason, and the patient is answered through the FR-034 support case
  6. System links the outcome to the request, marks it Resolved or Declined, and logs the action on Screen 7
- **Outcome**: Every post-acceptance cancellation or change goes through one audited FR-006 action, and the patient's request has a recorded outcome

**A7: Admin resolves provider-caused cancellation support**:

- **Trigger**: FR-015 provider suspension or deactivation (FR-015 Alternative Flow A5 and Screen 4) cancels a patient's case/inquiry or provider participation, or closes an accepted booking for the FR-006 provider-fault transfer while the inquiry stays open, with cause `ProviderSuspended` or `ProviderDeactivated` and sets `supportRequired` ("Admin Support Required"); admin receives the mandatory FR-020 admin-support alert (sent to admins with the FR-031 Respond to Support permission)
- **Access**: Viewing the Admin Support Required list and the patient's Provider-Caused Impacts requires FR-031 View Patients; Resolve Support requires FR-031 Respond to Support (default roles Super Admin, Aftercare Specialist, and Support Staff)
- **Steps**:
  1. Admin filters Screen 1 by "Admin Support Required: Unresolved" or opens the alert's deep link
  2. Admin reviews the patient's Provider-Caused Impacts (Screen 2): affected inquiry/case references, prior stage, cancellation cause, and any linked FR-034 support case
  3. Admin assists the patient through existing owners (rebooking, refunds, care continuity, FR-034 support case if created); FR-016 adds no automatic rebooking, refund, or ticket creation
  4. Admin selects "Resolve Support" on the affected record and enters a resolution reason
  5. System records the resolution reason and audit event (Screen 7), then clears the marker; the cancellation cause remains unchanged
- **Outcome**: Provider-caused impact is resolved with an audit trail; an inquiry's marker stays set while any linked provider-caused impact on it remains unresolved

---

### Note: Patient Support Center / Ticketing

FR-016 references patient support escalations, but **formal Support Center + Ticketing** (intake, triage, ticket lifecycle, and agent workflows) is specified in a dedicated requirement: **FR-034** (system-level entry in `local-docs/project-requirements/system-prd.md`).

**B5: Patient requests data deletion (GDPR)**:

- **Trigger**: Patient exercises "right to be forgotten" under GDPR
- **Steps**:
  1. Admin receives data deletion request (via Support Center / compliant support channel; see FR-034)
  2. Admin verifies patient identity and confirms legitimate request
  3. Admin checks if patient has active bookings or outstanding financial obligations
  4. If active obligations exist, admin explains data cannot be deleted yet (legal requirement)
  5. If no obligations, admin initiates data deletion workflow:
     - Mark account for anonymization
     - Remove PII (name, email, phone, address)
     - Retain anonymized medical records (7-year healthcare compliance)
     - Archive transaction history (7-year financial compliance)
  6. System executes deletion workflow (soft delete with anonymization)
  7. System generates data deletion certificate for audit
  8. Admin sends confirmation to patient: "Your data has been deleted per GDPR requirements"
  9. Admin closes the request
- **Outcome**: Patient data deleted while maintaining compliance with retention laws

---

## Screen Specifications

### Screen 1: Patient List View

**Purpose**: Allows admins to search, filter, and browse all patient accounts on the platform

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Search Input | text | No | Search by name, email, patient code, phone | Min 2 characters |
| Status Filter | multi-select | No | Filter by journey stage | Options: Inquiry, Quoted, Accepted, Confirmed, In Progress, Aftercare, Completed, Cancelled (the FR-003 stage list) |
| Account Status Filter | multi-select | No | Filter by account status | Options: Active, Suspended, Deactivated |
| Date Range Filter | date-range | No | Filter by registration date or last activity | Start date ≤ End date |
| Location Filter | select | No | Filter by patient country | Country list from admin settings |
| Provider Filter | select | No | Filter by assigned provider | Active providers only |
| Admin Support Filter | select | No | Filter patients with provider-caused cancellation impacts (FR-015 A5) | Options: All, Unresolved, Resolved; Unresolved = any linked case/inquiry with `supportRequired` set |
| Sort By | select | No | Sort results | Options: Name, Date, Status, Last Activity |
| Results Per Page | select | No | Pagination control | Options: 25, 50, 100 |

**Table Columns (per patient row)**:

| Column | Description |
|--------|-------------|
| Patient ID | Canonical `HPID` code (sortable, copy on click) |
| Patient Name | Avatar, full name, primary email stacked |
| Phone Number | International format with country code |
| Age | Derived from DOB for quick clinical context |
| Problem | Top-level treatment focus (Hair, Beard, Both, etc.) |
| Location | Country (and city when space allows) |
| Requested Date | Upcoming/most recent requested treatment window |
| Med Alerts | Badge: Critical / Standard / None, matches patient medical questionnaire severity |
| Payment | Latest payment status badge (Paid, Pending, Deposit Due, Refund, etc.) |
| Stage | Current journey stage badge (Inquiry, Quoted, Accepted, Confirmed, In Progress, Aftercare, Completed, Cancelled), using the FR-003 stage list. "Cancelled" indicates a patient-initiated inquiry cancellation in the Inquiry or Quoted stage (FR-003 Workflow 5) — admin has oversight only, no reversal — an admin cancellation of a booking through FR-006 (shown as "Cancelled — Admin"), or a provider-caused cancellation shown as "Cancelled — Provider Suspended" or "Cancelled — Provider Deactivated". An unresolved provider-caused impact adds a separate "Admin Support Required" badge, including when the inquiry stage itself is not cancelled. |
| Last Active | Relative timestamp of last platform action |
| Action | Overflow menu with shortcuts: open case, view detail, quick actions |

**Business Rules**:

- Default view shows all patients sorted by last activity (most recent first)
- Search executes automatically after 500ms typing pause (debounced search)
- Filters are combinable (e.g., "Status: In Progress AND Location: UK")
- Patient list updates in real-time when new patients register (WebSocket push)
- Patient codes always displayed alongside names for unique identification
- Row layout mirrors inquiry list so admins immediately recognize patient intent/context
- Stage badges color-coded: Inquiry (blue), Quoted (purple), Accepted (teal), Confirmed (green), In Progress (orange), Aftercare (light green), Completed (gray), Cancelled (red); the Suspended account status badge is dark red
- Flagged patients show red alert icon with hover tooltip explaining flag reason
- "Admin Support Required" badge is independent of Stage and Status Filter; it clears only when every linked provider-caused impact is resolved (Flow A7). Provider-caused cancellations are never labelled "Cancelled by patient"
- Clicking row navigates to patient detail view

**Notes**:

- List view supports column sorting (click column header to sort)
- Export functionality allows downloading filtered results as CSV
- Bulk actions available for selected patients (e.g., send notification to multiple)
- Performance: Pagination required; fetch 25 results per page to avoid slow queries
- **Inline Edit (highlight)**: Every displayed field supports inline editing with autosave + audit logging, so admins can adjust patient info without opening detail view

---

### Screen 2: Patient Detail View - Overview Tab

**Purpose**: Displays comprehensive patient profile summary and current status

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Patient Name | text | Yes (display only) | Full legal name | Read-only |
| Patient Code | text | Yes (display only) | Unique identifier (e.g., HP258742) | Read-only |
| Email | email | Yes (display only) | Contact email | Read-only |
| Phone | text | Yes (display only) | Phone with country code | Read-only |
| Date of Birth | date | No (display only) | Patient age calculation | Read-only |
| Location | text | Yes (display only) | Country, city | Read-only |
| Registration Date | datetime | Yes (display only) | Account creation timestamp | Read-only |
| Last Activity | datetime | Yes (display only) | Most recent platform action | Read-only |
| Current Status | badge | Yes (display only) | Journey stage | Read-only, color-coded |
| Assigned Provider | link | No (display only) | Provider name (if applicable) | Click to navigate to provider profile |
| Account Status | badge | Yes (display only) | Active, Suspended, Deactivated | Read-only, color-coded |
| Cancellation Reason | text | Conditional (display only) | Patient-selected cancellation reason (from FR-026 Screen 5a options), or provider-caused cause `ProviderSuspended` / `ProviderDeactivated` (FR-015 A5) | Read-only; only shown when Current Status = Cancelled |
| Cancellation Timestamp | datetime | Conditional (display only) | When the inquiry was cancelled by the patient | Read-only; only shown when Current Status = Cancelled |
| Flags/Alerts | list | No (display only) | Active warnings or concerns | Clickable to view details |
| Provider-Caused Impacts | list | Conditional (display only) | One row per affected inquiry/case: inquiry/case reference (deep link), prior stage, cancellation cause, Admin Support Required state (Unresolved/Resolved with reason, admin, timestamp), linked FR-034 support case (if any) | Read-only; shown when any FR-015 A5 impact exists |
| Resolve Support | action | Conditional | Clears Admin Support Required on one affected record | Resolution reason required (minimum 20 characters); shown only for unresolved records and only to admins with the FR-031 Respond to Support permission |

**Business Rules**:

- All personal information displayed is read-only in Overview tab
- Admin must use "Edit Patient" button to modify profile fields
- Patient code is hyperlinked (click to copy to clipboard)
- Email and phone are clickable (email opens mail client, phone copies to clipboard)
- "Assigned Provider" link navigates to provider management module
- Status badges use consistent color scheme across all admin views
- Flags/alerts section shows maximum 3 most critical items; click "View All" to see complete list
- "Last Activity" timestamp updates in real-time if patient is currently active
- When Current Status is "Cancelled", Cancellation Reason and Cancellation Timestamp are displayed below the status badge. Admin has oversight only — no reversal action is available (per FR-003 Workflow 5 design decision). Cancellation reason sourced from FR-026 Screen 5a managed options; reason is patient-private but visible to admin for oversight.
- Provider-caused impacts (FR-015 A5) are not patient cancellations: show the cause, not "Cancelled by patient". Resolving support records a reason and audit event before clearing the marker; the cause and cancelled state remain. Provider-confidential suspension/deactivation reasons are not shown here; admins follow the FR-015 provider record for them.

**Notes**:

- Profile photo displayed if patient uploaded one
- Discovery question response shown (how patient found platform)
- Quick action buttons: "Reset Password", "Suspend Account", "Send Notification"
- Admin access to this tab is logged in audit trail (basic profile view, not medical data)

---

### Screen 3: Patient Detail View - Treatment Journey Tab

**Purpose**: Displays milestone-level progress of the patient journey and routes admins to the canonical inquiry/case page for deep dives

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Milestone List | component | Yes (display only) | Chronological list of major journey milestones | Read-only, descending |
| Milestone Name | badge | Yes (display only) | Inquiry Submitted, Quote Approved, Inquiry Cancelled, Booking Confirmed, Travel Complete, Procedure Complete, Aftercare Checkpoint, etc. | Color-coded; "Inquiry Cancelled" uses red/warning style |
| Milestone Date | datetime | Yes (display only) | Timestamp milestone achieved | Read-only |
| Summary | text | Yes (display only) | Key datapoints (provider, location, payment amount) | 1-2 lines max |
| Case Detail Link | button | Yes | Opens inquiry/case detail focused on the stage | Opens in new tab; deep link required |
| Admin Notes | textarea | No | Optional note per milestone | Stored with audit trail |

**Business Rules**:

- Milestones display most recent first and collapse intermediate system events to avoid duplicating case detail
- Each milestone card includes "Open Case Detail" which navigates to the canonical screen where full actions occur
- Active/in-progress milestone anchored at top with live status indicator
- Failed milestones (e.g., payment failed) show warning icon and link to relevant payment record
- "Inquiry Cancelled" milestone displays as a terminal card with: cancellation reason (from FR-026 Screen 5a), cancellation timestamp, and "Cancelled by Patient" indicator. The "Open Case Detail" link navigates to the inquiry detail page showing the read-only cancelled state. If quotes were auto-cancelled as cascade, the milestone summary notes the count (e.g., "3 quotes cancelled")
- Provider-caused cancellations (FR-015 A5) display a terminal "Cancelled — Provider Suspended" or "Cancelled — Provider Deactivated" card with prior stage, effective timestamp, and Admin Support Required state; for shared unaccepted inquiries the card notes the cancelled provider participation while the inquiry milestone stays active
- Admin notes are optional but, when provided, log to audit trail referencing the milestone
- Export generates concise milestone report (no duplicate case data)

**Notes**:

- Tab emphasizes summary; all rich detail/editing continues to live in Hairline overview/case page
- Real-time updates still push new milestones without refresh

---

### Screen 4: Patient Detail View - Medical Data Tab

**Purpose**: Displays patient medical questionnaire, head scan assets, and health history with strict access controls

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Access Justification | textarea | Yes (required for access) | Admin reason for viewing medical data | Min 20 characters |
| Medical Questionnaire | component | Yes (display only) | Responses with severity flags | Read-only, color-coded |
| Head Scan Viewer | media viewer | No (display only) | Latest head scan assets (V1 photo set; V2 3D model) | Read-only |
| Previous Scans | gallery | No (display only) | Historical head scan uploads for comparison | Clickable thumbnails |
| Uploaded Photos | gallery | No (display only) | Patient-uploaded images | Clickable thumbnails |
| Declared Medications | list | No (display only) | Current medications | Read-only |
| Allergies | list | No (display only) | Known allergies | Read-only |
| Previous Procedures | list | No (display only) | Prior treatments | Read-only |

**Business Rules**:

- **CRITICAL**: Admin must enter justification before viewing medical data (audit compliance)
- Justification dialog appears immediately upon clicking "Medical Data" tab
- All Super Admins have full access to medical data (with mandatory justification)
- Every access logged with: admin ID, timestamp, justification, data viewed
- Medical questionnaire responses color-coded by severity:
  - Red (Critical): HIV, blood disorders, heart conditions
  - Yellow (Standard): Allergies, medications, controlled conditions
  - Green (No alerts): No medical concerns
- V1: Head scan viewer shows a photo set gallery with zoom and basic comparison
- V2: Interactive 3D viewer (if available) allows rotation and zoom; downloads logged in audit trail
- Photo gallery supports zoom but prevents right-click save (security measure)

**Notes**:

- Medical data tab shows warning banner: "Protected Health Information - Access Logged"
- "Request Provider Medical Report" button available to request additional info from provider
- Medical data encryption status indicator displayed (AES-256 encrypted at rest)
- Compliance note: "Data retained per healthcare regulations (7 years minimum)"

---

### Screen 5: Patient Detail View - Payments Tab

**Purpose**: Displays complete financial history including transactions, refunds, and outstanding balances

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Payment Summary | component | Yes (display only) | Total paid, outstanding, refunds | Calculated fields, read-only |
| Transaction List | table | Yes (display only) | All payment transactions | Sortable, filterable |
| Transaction Date | datetime | Yes (display only) | When transaction occurred | Read-only |
| Transaction Type | badge | Yes (display only) | Deposit, Installment, Final, Refund | Color-coded |
| Amount | currency | Yes (display only) | Transaction amount in currency | Read-only, formatted |
| Payment Method | text | Yes (display only) | Card type, last 4 digits | Read-only, masked |
| Status | badge | Yes (display only) | Success, Failed, Pending, Refunded | Color-coded |
| Stripe Payment ID | link | Yes (display only) | Stripe payment intent ID | Click to open Stripe dashboard |
| Admin Actions | button-group | No | Actions available | Context-dependent (e.g., "Issue Refund", "Retry Payment") |

**Business Rules**:

- Payment summary auto-calculates: Total Paid, Outstanding Balance, Total Refunds
- Transaction list defaults to descending date order (most recent first)
- Failed payments show error message from payment processor with troubleshooting tips
- Currency displayed in original transaction currency (GBP, USD, EUR, etc.)
- Exchange rates shown for multi-currency bookings
- Stripe Payment ID links directly to Stripe dashboard for admins with Stripe access
- "Issue Refund" button available only for succeeded payments
- Refunds require admin justification; amounts > $1,000 trigger extended confirmation modal (no separate role)
- Installment plans show: total installments, paid installments, remaining installments, next due date

**Notes**:

- Payment timeline visualization shows payment schedule vs. actual payments
- "Send Payment Reminder" button for overdue installments
- "Export Transactions" generates CSV for accounting purposes
- Real-time payment status updates (WebSocket notification when payment succeeds/fails)
- Commission calculation shown: Total Amount, Provider Share, Hairline Commission

---

### Screen 6: Patient Detail View - Communications Tab

**Purpose**: Displays all patient communications with providers, support, and aftercare team for monitoring and compliance

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Conversation List | list | Yes (display only) | All conversation threads | Grouped by recipient (provider, support, aftercare) |
| Conversation Partner | text | Yes (display only) | Who patient communicated with | Read-only |
| Last Message Date | datetime | Yes (display only) | Most recent message timestamp | Read-only |
| Message Count | number | Yes (display only) | Total messages in thread | Read-only |
| Flagged Indicator | icon | No (display only) | Shows if conversation flagged | Clickable to see flag reason |
| Message Thread | component | Yes (display only) | Full conversation history | Read-only, scrollable |
| Message Sender | badge | Yes (display only) | Patient or Provider/Support | Color-coded |
| Message Text | text | Yes (display only) | Message content | Read-only, supports images |
| Message Timestamp | datetime | Yes (display only) | When message sent | Read-only |

**Business Rules**:

- All messages are read-only; admins cannot send messages from this view
- Conversations grouped by partner: "With Provider: Dr. Mehmet's Clinic", "With Support Team", "With Aftercare Team"
- Flagged conversations highlighted in red (flagged by automated keyword detection or manual provider report)
- Keywords that trigger auto-flagging: "outside platform", "direct payment", "bank transfer", "WhatsApp", phone numbers, email addresses
- Admin can manually flag/unflag conversations with justification
- Message thread displays chronologically with clear sender identification
- Images in messages displayed as thumbnails; click to view full size
- Export conversation as PDF for dispute resolution documentation

**Notes**:

- Compliance warning banner: "All communications monitored for platform policy compliance"
- "Flag for Review" button allows admin to escalate suspicious conversations
- Search within conversation thread functionality
- Real-time updates: New messages appear without page refresh
- Flagged conversations generate notification in admin dashboard
- Anonymized patient identity maintained in pre-payment messages (display as "Patient #HP12345")

---

### Screen 7: Patient Detail View - Admin Actions Tab

**Purpose**: Displays audit trail of all admin interventions and actions taken on patient account

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Admin Action List | table | Yes (display only) | Chronological log of actions | Sortable, filterable |
| Action Date | datetime | Yes (display only) | When action occurred | Read-only |
| Admin Name | text | Yes (display only) | Which admin performed action | Read-only |
| Action Type | badge | Yes (display only) | Type of intervention | Allowed values: Password Reset, Account Unlock, Profile Update, Manual Refund, Account Suspension, Medical Data Access, Data Deletion Request, Admin Note, Patient Inquiry Cancellation (system-generated audit entry when patient cancels inquiry via FR-003 Workflow 5 — logs who/when/reason), Provider-Caused Cancellation (system-generated entry per affected case/inquiry from FR-015 A5 — logs provider-status event, cause, prior stage), Provider Support Resolution (logs affected record, resolution reason, admin) |
| Action Description | text | Yes (display only) | Summary of what changed | Read-only |
| Justification | text | Yes (display only) | Admin reason for action | Read-only, expandable |
| Impact | badge | No (display only) | Severity of action | Low, Medium, High |

**Business Rules**:

- **CRITICAL**: All admin actions MUST be logged (audit compliance requirement)
- Actions displayed in descending chronological order
- Admin name links to admin profile for accountability
- Action types restricted to enumerated list above; any new action type requires PRD update
- Justification field required for every action (minimum 20 characters)
- Actions marked as "System-Generated" if automated (e.g., auto-unlock account after lockout period)
- Export audit log as PDF or CSV for compliance reporting
- Audit log immutable (admins cannot delete or modify past entries)
- Sensitive actions (medical data access) highlighted in distinct color

**Notes**:

- Search and filter audit log by action type, date range, admin name
- "Show Only My Actions" toggle to filter by logged-in admin
- Audit log integrates with system-wide audit service (S-06)
- Tamper-proof checksums ensure log integrity
- Retention: Audit logs retained for minimum 10 years (compliance requirement)
- All entries currently originate from the single Super Admin role (no role hierarchy in MVP)

---

### Screen 8: Patient Deletion Requests List (GDPR)

**Purpose**: Provide a simple queue of patients who requested account/data deletion, so admins can review the request reason and optionally contact the patient before approving

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Screen Title | text | Yes (display only) | "Deletion Requests" | Located under **User management → Patients** |
| Search | text | No | Search by patient name, email, or HPID | Debounced; case-insensitive |
| Filters | group | No | Filter controls | Default filter: Status = Pending Admin Review |
| Deletion Requests Table | table | Yes (display only) | List of patients with deletion requests | Sorted by oldest pending first (SLA risk) |
| Table Column: Patient ID | text | Yes (display only) | Patient HPID identifier | Copy to clipboard |
| Table Column: Patient Name | text | Yes (display only) | Patient full name | Click opens patient detail overview in a new tab |
| Table Column: Patient Email | text | Yes (display only) | Primary email | Read-only |
| Table Column: Submitted At | datetime | Yes (display only) | When request was submitted | Server time |
| Table Column: Reason (Optional) | text | No (display only) | Patient-provided reason (if any) | Truncated to 1 line; expand in modal |
| Table Column: SLA Due By | datetime | Yes (display only) | Latest completion target | Submitted At + 30 calendar days (FR-023) |
| Table Column: Actions | buttons | Yes (display only) | Primary action: Review | Opens review/approve modal |
| Empty State | group | Conditional (display only) | No deletion requests to show | Message: "No pending deletion requests" |
| Review / Approve Modal | modal | Conditional | Modal shown when admin clicks Review | Displays request reason and approve/deny actions |
| Modal: Patient Summary | group | Yes (display only) | Patient name, HPID, email | Read-only |
| Modal: Request Details | group | Yes (display only) | Submitted at, SLA due by, reason (if provided) | Read-only |
| Modal: Contact Options | buttons | Yes (display only) | Quick actions: Call patient / Email patient | Opens system dialer/email client (or internal contact tools) |
| Modal: Admin Notes | text | No | Optional notes about verification/contact | Stored in audit trail if approving/denying |
| Modal: Approve Button | action | Conditional | Approves deletion request | Requires enhanced confirmation + justification |
| Modal: Deny Button | action | Conditional | Denies deletion request | Requires justification |
| Modal: Close Button | action | Yes | Close modal | No changes |
| Audit Trail Link | link | Yes (display only) | Link to audit log entries for this request | Opens Screen 7 filtered to this request ID |

**Business Rules**:

- This screen is a queue for deletion requests initiated by patients and must align with the deletion request lifecycle defined in FR-023
- Admin may contact the patient (call/email) for additional confirmation before approving; no separate verification workflow is introduced in this UI
- System validates active obligations at the time of approval; if obligations exist, approval is blocked and the admin sees an actionable message (request remains pending)
- Approve triggers anonymization + archival workflow; protected medical/financial records are retained for legal minimums with restricted access (no hard-delete)
- Deny records a reason and notifies the patient; the request remains auditable
- Approve/Deny actions require justification and are written to the audit trail with request ID metadata

### Screen 9: Booking Support Requests (Cancellation and Change)

**Purpose**: Give admins one queue of patient requests to cancel or change a booking after subquote acceptance, which patients raise through Contact Support because they cannot cancel in the app, and route each one to the governed FR-006 action (Flow A8)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Screen Title | text | Yes (display only) | "Booking Support Requests" | Located under **User management → Patients** |
| Search | text | No | Search by patient name, HPID, booking reference, or support case reference | Debounced; case-insensitive |
| Request Type Filter | select | No | Filter by request type | Options: All, Cancellation, Appointment Change |
| Request Status Filter | select | No | Filter by request status | Options: Open, Resolved, Declined; default Open |
| Requests Table | table | Yes (display only) | One row per request | Sorted by oldest open request first |
| Table Column: Support Case Reference | link | Yes (display only) | FR-034 support case that holds the request | Opens the support case |
| Table Column: Patient | text | Yes (display only) | Patient name and HPID | Click opens the patient Overview tab |
| Table Column: Booking Reference and Status | text | Yes (display only) | Booking reference and current booking status | Read-only |
| Table Column: Current Appointment | datetime | Yes (display only) | The booking's current appointment date and time with time zone | Read-only |
| Table Column: Request Type | badge | Yes (display only) | Cancellation or Appointment Change | Read-only |
| Table Column: Patient Reason | text | No (display only) | Reason the patient gave | Truncated to one line; expand in panel |
| Table Column: Submitted At | datetime | Yes (display only) | When the patient raised the request | Read-only |
| Action: Cancel Booking | button | Conditional | Opens the FR-006 Cancel Booking action (FR-006 Screen 9) prefilled with the request source and support case reference | Shown for cancellation requests when the booking is `Accepted`, `Payment Window Expired`, `Confirmed`, `In Progress`, or `Aftercare` |
| Action: Change Appointment | button | Conditional | Opens the FR-006 Change Appointment action (FR-006 Screen 8) | Shown for change requests when the booking is `Accepted` or `Confirmed` |
| Action: Decline Request | button | Conditional | Declines the request without changing the booking | Shown for open requests; decline reason required (minimum 20 characters) |
| Outcome | text | Conditional (display only) | Action taken, admin, timestamp, and linked audit entry | Shown for Resolved or Declined requests |

**Business Rules**:

- Requests appear here when the patient uses Contact Support on an FR-006 booking screen from acceptance onward; requests for an inquiry still in the Inquiry or Quoted stage are not listed, because the patient can cancel those in the app (FR-003)
- The admin performs a cancellation or appointment change only through the FR-006 action; FR-006 holds the mandatory reason, confirmation, audit entry, and notice (`booking.cancelled` or `booking.rescheduled`) for that action
- A request becomes Resolved when its FR-006 action completes, and Declined when the admin records a decline reason; the patient is answered through the FR-034 support case in both cases
- Every action on this screen is logged on Screen 7 with the request and booking references
- Refund amounts and cancellation fees are not set here; they follow the FR-006 payment placeholder

## Business Rules

### General Module Rules

- **Rule 1**: All admin actions on patient accounts MUST be logged in audit trail with timestamp, admin ID, and justification
- **Rule 2**: Admins MUST NOT modify patient medical data (questionnaire responses, scans); medical data is immutable except by patients
- **Rule 3**: MVP supports a single Super Admin role with full visibility/edit rights; granular RBAC is deferred
- **Rule 4**: High-impact actions (account suspension, refunds > $1000, permanent data deletion) MUST require enhanced confirmation + justification, even though the same Super Admin executes them
- **Rule 5**: Admin access to patient medical data MUST trigger access justification prompt (HIPAA/GDPR compliance)
- **Rule 6**: Patient account deactivation MUST be soft-delete (archive) not hard-delete; data retained per compliance requirements (7 years)
- **Rule 7**: Admin interventions that affect bookings (reschedule, cancel) MUST go through the FR-006 Change Appointment or Cancel Booking action and MUST notify both patient and provider within 5 minutes through `booking.rescheduled` or `booking.cancelled`
- **Rule 8**: Provider-caused cancellations (FR-015 A5, causes `ProviderSuspended` / `ProviderDeactivated`) carry an independent Admin Support Required marker that only an admin resolution with reason and audit event can clear; the cause is never overwritten. FR-016 does not auto-create FR-034 tickets or change FR-034's workflow

### Data & Privacy Rules

- **Privacy Rule 1**: Admin access to patient medical data MUST be logged with justification (Protected Health Information)
- **Privacy Rule 2**: Patient scans displayed in admin interface MUST be read-only and access-controlled (prevent unauthorized distribution)
- **Privacy Rule 3**: Super Admins can download patient scans; all downloads are logged in audit trail for compliance
- **Privacy Rule 4**: Patient payment card details NEVER stored or displayed in admin interface (PCI-DSS compliance)
- **Privacy Rule 5**: Patient data deletion requests (GDPR right to be forgotten) MUST result in anonymization + archival, not permanent deletion
- **Privacy Rule 6**: Archived patient data accessible only through dedicated archive interface (requires explicit justification and logged access)
- **Audit Rule**: Every admin action MUST be logged with immutable audit trail (who, what, when, why)
- **HIPAA/GDPR**: Patient consent required before sharing medical data with third parties; admin cannot share medical data outside platform

### Admin Editability Rules

**Editable by Admin**:

- Patient profile information (name, email, phone, location) with justification
- Patient account status (active, suspended, deactivated)
- Booking appointment date only through the FR-006 guarded date change: allowed for `Accepted` or `Confirmed` bookings, with a mandatory reason and a slot availability check, and triggering an FR-008 travel-date review for any linked travel records (emergency reschedules with provider coordination)
- Booking cancellation only through the FR-006 Cancel Booking action: allowed from `Accepted` through `Aftercare`, on an admin decision or a support-routed patient request, with a mandatory reason, confirmation, and audit entry (Flow A8, Screen 9)
- Payment status (manual refund issuance, payment retry)
- Support escalations context (view-only link to Support Center; see FR-034)

**Fixed (Not Editable by Admin)**:

- Patient medical questionnaire responses (immutable; submitted by patient only)
- Patient head scan assets (photo sets in V1; 3D scans in V2) and uploaded photos (immutable; uploaded by patient only)
- Transaction timestamps and amounts (immutable financial records)
- Audit log entries (immutable for compliance)
- Patient password (admin can reset but cannot view current password)

**High-Impact Actions (require extended confirmation + justification)**:

- Account suspension (30+ days or permanent)
- Refunds exceeding $1,000
- Manual booking modifications during active treatment (handled on case detail screen)
- Bulk patient notifications
- Patient data deletion (GDPR requests)

---

## Success Criteria

### Admin Efficiency Metrics

- **SC-001**: Admins can locate any patient account via search in under 10 seconds (search results in < 2 seconds)
- **SC-002**: Admins can complete routine patient interventions (password reset, account unlock) in under 1 minute
- **SC-003**: Complete patient profile overview loads in under 3 seconds including all tabs (lazy loading for large datasets)
- **SC-004**: Admin audit log search and filtering returns results in under 5 seconds for queries spanning 1 year of data

### Patient Support Metrics

- **SC-005**: 90% of patient support escalations resolved within 24 hours using patient management tools (in coordination with Support Center; see FR-034)
- **SC-006**: Average time to resolve payment issues reduced by 50% with comprehensive payment history view
- **SC-007**: Patient satisfaction with admin support interventions rated 4.5+ stars (out of 5)
- **SC-008**: 95% of admin interventions completed in a single pass (no rework/escalation required)

### Data Governance Metrics

- **SC-009**: 100% of admin actions on patient accounts logged in audit trail (zero missing entries)
- **SC-010**: 100% of medical data access requires justification prompt (zero unauthorized access)
- **SC-011**: Patient data deletion requests (GDPR) completed within 30 days of verification
- **SC-012**: Zero incidents of patient data leakage or unauthorized access through admin interface

### Platform Health Metrics

- **SC-013**: Admin monitoring identifies and resolves 80% of patient friction points before they escalate to Support Center cases (see FR-034)
- **SC-014**: Admin dispute resolution reduces patient-provider conflicts by 60% through mediation tools
- **SC-015**: Manual booking interventions account for < 5% of total bookings (most bookings proceed smoothly)
- **SC-016**: Admin-flagged communications for policy violations reviewed and resolved within 48 hours

### System Performance Metrics

- **SC-017**: Patient search supports 1,000+ concurrent admin users without degradation
- **SC-018**: Patient detail view loads in < 3 seconds for 95% of requests
- **SC-019**: Real-time updates (new patient activity, payment notifications) delivered to admin dashboard within 5 seconds
- **SC-020**: Audit log queries spanning 10 years of data return results in under 10 seconds

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **FR-001 / Module P-01: Auth & Profile Management**
  - **Why needed**: Patient management relies on patient profile data, authentication status, and account metadata
  - **Integration point**: Admin interface fetches patient profile information via API; password reset triggers P-01 authentication service

- **FR-003 / Module P-02: Quote Request & Management**
  - **Why needed**: Admin views patient inquiries, quotes received, and quote acceptance history
  - **Integration point**: Treatment journey tab displays inquiry and quote data; admin can view quote details

- **FR-006 / Module P-03: Booking & Payment**
  - **Why needed**: Admin monitors booking status and payment history, and intervenes in bookings only through the FR-006 governed actions
  - **Integration point**: Payment tab fetches transaction history; Flow A8 and Screen 9 open the FR-006 Change Appointment and Cancel Booking actions

- **FR-011 / Module P-05: Aftercare & Progress Monitoring**
  - **Why needed**: Admin views patient aftercare status, milestone completion, and can access aftercare data
  - **Integration point**: Treatment journey shows aftercare progress; admin can assign aftercare specialists

- **FR-012 / Module P-06: Communication**
  - **Why needed**: Admin monitors patient-provider and patient-support communications for compliance
  - **Integration point**: Communications tab fetches message history; admin can flag conversations

- **FR-002 / Module P-07: 3D Scan Capture & Viewing**
  - **Why needed**: Admin views patient head scan assets (V1 photo set; V2 true 3D) for dispute resolution and support
  - **Integration point**: Medical data tab embeds head scan viewer component

- **FR-015 / Module A-02: Provider Management**
  - **Why needed**: Provider suspension/deactivation closes affected bookings (transfer through FR-006 Alternative Flow B5 after acceptance, inquiry stays open), cancels unaccepted participation, and sets the Admin Support Required marker (FR-015 Alternative Flow A5, Screen 4)
  - **Integration point**: FR-016 consumes cause, prior stage, affected references, and marker; owns admin filtering and audited resolution (Flow A7)

- **FR-034 / Support Center & Ticketing**
  - **Why needed**: Admin assistance for provider-caused cancellations may use a support case
  - **Integration point**: Linked support case reference shown in Provider-Caused Impacts; FR-034's workflow unchanged, no automatic ticket creation

- **FR-020 / Module S-03: Notification Service**
  - **Why needed**: Admin actions trigger notifications to patients (password reset, booking modifications)
  - **Integration point**: System sends notifications when admin intervenes; admin can manually send notifications

- **Module S-05: Media Storage Service**
  - **Why needed**: Admin accesses patient head scan assets, photos, and documents stored in media service
  - **Integration point**: Medical data tab fetches scan media from storage with proper authentication

- **Module S-06: Audit Log Service** (if exists)
  - **Why needed**: All admin actions logged in centralized audit service for compliance
  - **Integration point**: Every admin action sends audit log entry to shared service

### External Dependencies (APIs, Services)

- **Stripe API**
  - **Purpose**: View payment transaction details, initiate refunds, verify payment status
  - **Integration**: RESTful API calls to Stripe for payment intent lookups; webhook verification for payment events
  - **Failure handling**: If Stripe API unavailable, display cached payment status with warning; retry failed refunds automatically

- **Email Service (SendGrid / AWS SES)**
  - **Purpose**: Send notifications to patients when admin takes actions (password reset, booking modification)
  - **Integration**: SMTP or API integration for email delivery
  - **Failure handling**: Queue emails for retry if service unavailable; notify admin if email delivery fails

### Data Dependencies

- **Entity: Patient Accounts**
  - **Why needed**: Cannot display patient management interface without patient data
  - **Source**: Patient registration module (P-01), continuously updated as patients use platform

- **Entity: Treatment Bookings**
  - **Why needed**: Cannot display treatment journey or intervene in bookings without booking data
  - **Source**: Booking module (P-03), updated throughout booking lifecycle

- **State: Admin Permissions**
  - **Why needed**: Cannot authenticate Super Admin access without admin authentication configuration
  - **Source**: Admin authentication and permission module (A-09 System Settings)

- **State: Provider Profiles**
  - **Why needed**: Cannot assign providers or view provider relationships without provider data
  - **Source**: Provider onboarding module (A-02)

---

## Assumptions

### User Behavior Assumptions

- **Assumption 1**: Admins have basic understanding of patient journey stages and platform workflows
- **Assumption 2**: Admins will enter meaningful justifications when prompted (audit compliance)
- **Assumption 3**: Admins will use search filters effectively rather than scrolling through entire patient list
- **Assumption 4**: Most admin interventions are reactive (responding to Support Center escalations; see FR-034) rather than proactive monitoring

### Technology Assumptions

- **Assumption 1**: Admins access platform via desktop/laptop browsers (Chrome, Firefox, Safari - latest 2 versions)
- **Assumption 2**: Admins have stable internet connectivity (patient data and scan media require significant bandwidth)
- **Assumption 3**: Admin interface supports screen resolutions ≥ 1366x768 (responsive design for tablets acceptable)
- **Assumption 4**: Database query performance optimized with proper indexing on patient search fields (name, email, code, date)

### Business Process Assumptions

- **Assumption 1**: Admin team operates during business hours with on-call coverage for emergencies (24/7 monitoring not required initially)
- **Assumption 2**: Super admin coverage is available within 4 business hours to perform any high-impact confirmations
- **Assumption 3**: Patient support escalations escalate to admin interventions only when support team cannot resolve via communication (see FR-034)
- **Assumption 4**: Admin interventions are exceptional; most patient journeys proceed smoothly without admin involvement (< 10% of patients require intervention)

---

## Implementation Notes

### Technical Considerations

- **Architecture**: Patient management interface requires robust search engine (Elasticsearch or similar) for fast full-text patient search across large datasets
- **Performance**: Patient detail view uses lazy loading for tabs (load data only when tab clicked) to prevent slow initial page load
- **Performance**: Head scan viewer uses progressive loading (low-res preview first, high-res on demand) for large scan files
- **Storage**: Audit log requires separate database or table with write-optimized schema (append-only, no updates/deletes)
- **Caching**: Patient list search results cached for 30 seconds (Redis) to reduce database load for repeated searches

### Integration Points

- **Integration 1**: Admin dashboard fetches patient data from patient microservice API via REST
  - **Data format**: JSON payload with patient profile, status, metadata
  - **Authentication**: Admin JWT token with Super Admin role validation
  - **Error handling**: Display cached data if API unavailable; show warning banner

- **Integration 2**: Medical data tab requests head scan media from media storage service
  - **Data format**: Signed URLs for secure scan file access (S3 presigned URLs)
  - **Authentication**: Admin token verified; access logged in audit service
  - **Error handling**: Display error message if scan unavailable; offer retry button

- **Integration 3**: Audit log writes to centralized audit service via message queue
  - **Data format**: Audit event JSON with admin ID, action type, timestamp, justification, patient ID
  - **Authentication**: Internal service-to-service authentication
  - **Error handling**: Queue audit events locally if service unavailable; retry with exponential backoff

### Scalability Considerations

- **Current scale**: Support 10-50 concurrent admin users at launch
- **Growth projection**: Plan for 100-200 concurrent admins within 12 months as platform scales
- **Peak load**: Handle 500+ patient searches per minute during business hours
- **Data volume**: Support patient database of 100,000+ patients with fast search (< 2 second response)
- **Scaling strategy**: Horizontal scaling of admin API servers; read replicas for patient database; Elasticsearch cluster for search

### Security Considerations

- **Authentication**: Admins MUST authenticate via multi-factor authentication (MFA required for production access)
- **Authorization**: Single Super Admin role validated on every API call; additional RBAC tiers deferred but tracked for future scope
- **Encryption**: All patient data encrypted in transit (TLS 1.3) and at rest (AES-256)
- **Audit trail**: Every admin action logged with tamper-proof checksums; audit logs immutable (append-only)
- **Threat mitigation**: Rate limiting on patient search API (max 100 searches per admin per minute) to prevent data scraping
- **Threat mitigation**: Admin session timeout after 30 minutes of inactivity; re-authentication required for sensitive actions
- **Compliance**: HIPAA-compliant handling of medical data; GDPR-compliant data deletion process; PCI-DSS compliance for payment data access

---

## User Scenarios & Testing

### User Story 1 - Admin Searches for Patient to Resolve Support Escalation (Priority: P1)

Admin receives a support escalation (via Support Center; see FR-034) from a patient unable to complete payment. Admin needs to quickly locate patient account, review payment history, identify issue, and initiate manual intervention to resolve.

**Why this priority**: This is the most common admin workflow - responding to patient support requests. Platform success depends on effective patient support.

**Independent Test**: Can be fully tested by creating test patient account, simulating failed payment, creating a support escalation (via Support Center; see FR-034), and verifying admin can locate patient, view payment details, and take action (retry payment or issue refund).

**Acceptance Scenarios**:

1. **Given** admin is logged into admin dashboard, **When** admin enters patient email in search field, **Then** system returns matching patient within 2 seconds with key details displayed (name, code, status)
2. **Given** admin views patient detail, **When** admin clicks "Payments" tab, **Then** system loads complete payment history within 1 second showing all transactions, failed attempts, and outstanding balances
3. **Given** admin identifies failed payment, **When** admin clicks "Retry Payment" button and enters justification, **Then** system initiates payment retry and logs admin action in audit trail
4. **Given** payment retry successful, **When** system updates payment status, **Then** admin sees confirmation and patient receives notification of successful payment

---

### User Story 2 - Admin Views Patient Medical Data for Dispute Resolution (Priority: P1)

Provider claims patient misrepresented medical history. Admin needs to access patient medical questionnaire and scans to investigate dispute and mediate between patient and provider.

**Why this priority**: Dispute resolution is critical for platform trust and legal protection. Admin must have ability to access medical data with proper safeguards.

**Independent Test**: Can be tested by creating test patient with completed medical questionnaire and uploaded head scan assets, simulating dispute scenario, and verifying admin prompted for access justification, can view data, and access is fully logged in audit trail.

**Acceptance Scenarios**:

1. **Given** admin navigates to patient detail view, **When** admin clicks "Medical Data" tab, **Then** system displays justification prompt requiring admin to enter reason for access (minimum 20 characters)
2. **Given** admin enters valid justification, **When** admin submits justification, **Then** system logs access in audit trail with timestamp, admin ID, and justification, then displays medical questionnaire with severity flags
3. **Given** medical questionnaire displayed, **When** admin reviews responses, **Then** critical conditions (HIV, blood disorders) highlighted in red, standard conditions (allergies, medications) in yellow
4. **Given** admin clicks Head Scan Viewer, **When** media loads, **Then** scan assets display (V1 photo set gallery; V2 interactive 3D model where available); downloads logged in audit trail

---

### User Story 3 - Admin Manually Reschedules Booking Due to Emergency (Priority: P1)

Patient contacts support with medical emergency requiring postponement of procedure. Admin needs to coordinate with provider, modify booking date, and notify all parties without disrupting payment or other booking details.

**Why this priority**: Emergency booking modifications are critical patient support scenarios that require admin intervention. Handling these smoothly impacts patient satisfaction and provider relationships.

**Independent Test**: Can be tested by creating confirmed booking, simulating emergency request, and verifying admin can modify booking date through the FR-006 guarded date change, system notifies patient and provider, payment details remain intact, and any linked travel records are flagged for an FR-008 travel-date review.

**Acceptance Scenarios**:

1. **Given** admin locates patient with confirmed booking, **When** admin clicks "Modify Booking" button, **Then** system displays booking details and the available FR-006 actions (Change Appointment, Cancel Booking)
2. **Given** admin selects "Change Appointment Date", **When** admin enters new date (coordinated with provider offline) and justification ("Patient medical emergency"), **Then** system validates new date is available and prompts for confirmation
3. **Given** admin confirms modification, **When** system processes change, **Then** the booking's current appointment is updated, the patient and provider receive `booking.rescheduled` with the old and new appointment, any linked travel records are flagged for an FR-008 travel-date review, and audit log records admin action
4. **Given** booking rescheduled, **When** admin views booking details, **Then** new date displayed with note "Rescheduled by admin on [date] - Reason: [justification]"

---

### User Story 4 - Admin Resets Patient Password (Priority: P1)

Patient locked out of account after multiple failed login attempts. Patient contacts support requesting account unlock and password reset. Admin needs to verify patient identity, reset password, and unlock account.

**Why this priority**: Account access issues are frequent support requests. Quick resolution critical for patient experience.

**Independent Test**: Can be tested by creating test patient account, triggering account lockout via failed login attempts, and verifying admin can reset password, unlock account, and patient receives reset email.

**Acceptance Scenarios**:

1. **Given** admin locates locked patient account, **When** admin views account status, **Then** system displays "Account Status: Locked" badge and "Unlock Account" button
2. **Given** admin clicks "Reset Password" button, **When** system displays confirmation dialog, **Then** admin enters justification ("Patient requested via Support Center case #1234") and confirms action
3. **Given** admin confirms password reset, **When** system processes request, **Then** system generates 6-digit OTP reset code, sends email to patient with reset link, logs admin action in audit trail
4. **Given** password reset email sent, **When** patient receives email and completes reset, **Then** patient can log in with new password and account status changes to "Active"

---

### User Story 5 - Admin Monitors Patient-Provider Communications for Policy Violations (Priority: P2)

Automated system flags patient-provider conversation containing keywords suggesting off-platform transaction attempt ("direct payment", "WhatsApp"). Admin needs to review flagged conversation, determine if policy violation occurred, and take appropriate action (warning, suspension).

**Why this priority**: Compliance monitoring protects platform revenue and ensures all transactions occur on-platform per terms of service. Important but not as urgent as direct patient support.

**Independent Test**: Can be tested by simulating patient-provider conversation with flagged keywords, verifying system auto-flags conversation, and confirming admin can review, determine action, and log decision.

**Acceptance Scenarios**:

1. **Given** automated system detects flagged keywords in patient-provider conversation, **When** flag is triggered, **Then** system generates notification in admin dashboard and marks conversation with red flag icon
2. **Given** admin navigates to patient's Communications tab, **When** admin views conversation list, **Then** flagged conversation highlighted with warning indicator and flag reason displayed
3. **Given** admin clicks flagged conversation, **When** conversation thread loads, **Then** flagged messages highlighted with keyword indicator; admin can review full context
4. **Given** admin determines policy violation occurred, **When** admin clicks "Take Action" button, **Then** admin selects action (warning to patient, warning to provider, suspend account), enters justification, and confirms; system logs decision and executes action

---

### User Story 6 - Admin Processes Patient Data Deletion Request (GDPR) (Priority: P2)

Patient exercises "right to be forgotten" under GDPR and submits data deletion request. Admin needs to verify patient identity, check for active bookings or financial obligations, and if clear, initiate data anonymization process while retaining required compliance records.

**Why this priority**: Legal compliance requirement but relatively infrequent request. Important to handle correctly but not as time-sensitive as active bookings or payments.

**Independent Test**: Can be tested by creating test patient with completed treatment history, submitting GDPR deletion request, and verifying admin follows verification workflow, executes anonymization, and generates deletion certificate.

**Acceptance Scenarios**:

1. **Given** a patient submits an account deletion request, **When** admin opens **User management → Patients → Deletion Requests**, **Then** the request appears in the pending queue with submitted date, optional reason, and SLA due date
2. **Given** admin clicks "Review" on a request, **When** the modal opens, **Then** admin can view the patient’s optional reason and has quick actions to call/email the patient before approval
3. **Given** the patient has no active obligations, **When** admin clicks "Approve" and confirms with justification, **Then** the system initiates anonymization + archival workflow while retaining compliance records per healthcare regulations and logs the action in the audit trail
4. **Given** the request cannot be approved due to active obligations at the time of approval, **When** admin clicks "Approve", **Then** the system blocks approval and shows an actionable message; the request remains pending

---

### User Story 7 - Admin Suspends Patient Account Due to Fraud (Priority: P2)

Fraud detection system flags patient account with multiple chargebacks and suspicious activity. Admin investigates evidence, determines account suspension necessary, and executes suspension with documentation for potential legal follow-up.

**Why this priority**: Fraud prevention important for platform financial health but occurs infrequently. Requires careful investigation and documentation.

**Independent Test**: Can be tested by creating test patient account, simulating fraud indicators (multiple chargebacks, duplicate accounts), and verifying admin can investigate, suspend account with justification, and system logs all actions.

**Acceptance Scenarios**:

1. **Given** fraud detection system flags patient account, **When** admin receives alert, **Then** admin navigates to patient detail view and sees red warning banner: "Fraud Alert: Multiple payment chargebacks detected"
2. **Given** admin reviews evidence (payment history, chargeback details, activity patterns), **When** admin determines suspension warranted, **Then** admin clicks "Suspend Account" button
3. **Given** suspension dialog displayed, **When** admin enters detailed justification ("3 chargebacks in 30 days totaling $2,500; suspected fraudulent activity") and selects suspension duration (30 days / 90 days / Permanent), **Then** admin confirms action
4. **Given** admin confirms suspension, **When** system processes suspension, **Then** system immediately revokes patient authentication tokens (forces logout), cancels active bookings with refund processing, sends suspension notification to patient with appeal process information, and logs full audit trail with evidence references

---

### User Story 8 - Admin Reviews Patient with Cancelled Inquiry (Priority: P3)

Patient cancelled their inquiry via FR-003 Workflow 5. Admin needs to view the cancelled state for oversight, verify cascade completed correctly (quotes auto-cancelled, providers notified), and confirm no further action is required.

**Why this priority**: Cancellation oversight is passive — admin has no reversal capability. Important for audit completeness but lower priority than active interventions.

**Independent Test**: Create patient with inquiry in Quoted stage with 2 quotes, patient cancels inquiry, verify admin sees correct status, cancellation reason/timestamp, milestone card, auto-cancelled quotes, and audit trail entry.

**Acceptance Scenarios**:

1. **Given** admin searches for a patient who cancelled their inquiry, **When** admin views patient list (Screen 1), **Then** Stage column shows "Cancelled" badge (red) with note "Cancelled by patient"
2. **Given** admin opens patient detail Overview tab (Screen 2), **When** Current Status shows "Cancelled", **Then** Cancellation Reason and Cancellation Timestamp fields are visible below the status badge; no reversal action is available
3. **Given** admin views Treatment Journey tab (Screen 3), **When** milestones load, **Then** "Inquiry Cancelled" appears as terminal milestone card with reason, timestamp, and count of auto-cancelled quotes (e.g., "2 quotes cancelled")
4. **Given** admin views Admin Actions tab (Screen 7), **When** filtering by action type, **Then** system-generated "Patient Inquiry Cancellation" audit entry is visible with patient who/when/reason details

---

### User Story 9 - Admin Resolves Provider-Caused Cancellation Support (Priority: P1)

A provider is suspended or deactivated (FR-015 A5) and the patient's case is cancelled, or their accepted booking is closed and awaits rehoming through FR-006 Alternative Flow B5. Admin must find the patient, assist, and resolve the support marker with an audit trail.

**Why this priority**: Patients lose an accepted or ongoing treatment through no action of their own and are instructed to contact admins.

**Independent Test**: Suspend a provider with one confirmed case and one shared unaccepted inquiry for different patients; verify both patients appear under "Admin Support Required: Unresolved", show the correct cause and references, and clear only after a reasoned resolution.

**Acceptance Scenarios**:

1. **Given** a case cancelled with `ProviderSuspended`, **When** admin filters Screen 1 by Admin Support Required = Unresolved, **Then** the patient appears with the "Cancelled — Provider Suspended" stage and Admin Support Required badge, never "Cancelled by patient"
2. **Given** admin opens Screen 2, **When** Provider-Caused Impacts loads, **Then** it shows the inquiry/case reference, prior stage, cause, and linked FR-034 case (if any)
3. **Given** admin resolves one of two unresolved impacts on the same inquiry, **When** resolution is saved with a reason, **Then** an audit event is logged, that record's marker clears, the cause remains, and the inquiry stays flagged until the second impact is resolved

---

### Edge Cases

- **Edge Case 1**: How does system handle concurrent admin modifications (two admins modifying same patient booking simultaneously)?
  - **Handling**: System uses optimistic locking; first admin's change succeeds, second admin receives error: "This booking was just modified by [Admin Name]. Please refresh and retry."; forces second admin to reload current state before making changes

- **Edge Case 2**: What occurs if a new Support Center case is created while an admin is actively viewing the patient's account?
  - **Handling**: System pushes real-time notification to admin's dashboard: "New support escalation from this patient"; admin can click notification to open the Support Center case without losing current context; escalation appears in patient's overview section (via link to Support Center)

- **Edge Case 3**: How to manage admin accessing patient account while patient is actively logged in and making changes?
  - **Handling**: Admin sees banner: "Patient currently active on platform (last activity: 30 seconds ago)"; admin's view refreshes automatically when patient makes changes; if admin attempts modification, system warns: "Patient is actively using the platform - your changes may conflict"

- **Edge Case 4**: What happens when admin tries to reset password for patient who just changed password themselves?
  - **Handling**: System displays warning: "Patient changed password 5 minutes ago. Reset anyway?"; admin must confirm they still want to reset (logs additional justification); patient receives notification: "Your password was reset by admin - if this wasn't you, contact support immediately"

- **Edge Case 5**: How does system handle patient data deletion request when patient has pending refund?
  - **Handling**: System prevents deletion: "Cannot process deletion request - patient has pending refund of £500. Deletion will be available after refund completes."; admin can schedule deletion for after refund clears; system sends automated notification when patient becomes eligible

- **Edge Case 6**: What occurs if admin issues refund and Stripe API call fails?
  - **Handling**: System queues refund for automatic retry (exponential backoff: 1 min, 5 min, 15 min); admin sees status "Refund Pending"; if all retries fail after 1 hour, system alerts admin: "Refund failed - manual intervention required"; admin can review Stripe error and retry manually

---

## Functional Requirements Summary

### Core Requirements

- **REQ-016-001**: System MUST allow admins to search patients by name, email, patient code, or phone number with results returned in < 2 seconds
- **REQ-016-002**: System MUST display comprehensive patient profile including: personal info, current journey status, registration date, last activity, and flags/alerts
- **REQ-016-003**: System MUST provide complete treatment journey timeline showing all inquiries, quotes, bookings, payments, procedures, and aftercare milestones
- **REQ-016-004**: System MUST allow admins to view patient medical questionnaire and head scan assets (V1 photo set; V2 true 3D) with mandatory access justification prompt (HIPAA/GDPR compliance)
- **REQ-016-005**: System MUST display complete payment history including successful transactions, failed attempts, refunds, outstanding balances, and installment schedules
- **REQ-016-006**: System MUST allow admins to view all patient communications (with providers, support, aftercare) for compliance monitoring
- **REQ-016-007**: System MUST log every admin action on patient accounts in immutable audit trail with timestamp, admin ID, action type, and justification

### Admin Intervention Requirements

- **REQ-016-008**: System MUST allow admins to reset patient passwords with email notification sent to patient
- **REQ-016-009**: System MUST allow admins to unlock patient accounts after failed login attempts
- **REQ-016-010**: System MUST allow admins to reschedule bookings only through the FR-006 Change Appointment action with justification, notifying both patient and provider through `booking.rescheduled`
- **REQ-016-011**: System MUST allow admins to initiate refunds with enhanced confirmation workflow for amounts > $1,000
- **REQ-016-012**: System MUST allow admins to suspend patient accounts (30 days / 90 days / Permanent) with justification
- **REQ-016-013**: System MUST allow admins to update patient profile information (name, email, phone, location) with justification and audit logging
- **REQ-016-028**: System MUST display FR-015 provider-caused cancellation causes (`ProviderSuspended`, `ProviderDeactivated`) distinctly from patient cancellation and let admins filter/badge patients with unresolved Admin Support Required records
- **REQ-016-029**: System MUST show, per affected record, the inquiry/case reference, prior stage, cancellation cause, support state, and linked FR-034 support case (if any)
- **REQ-016-030**: System MUST require a resolution reason and log an audit event before clearing Admin Support Required; the cause remains, an inquiry's marker stays while any linked provider-caused impact is unresolved, and no ticket is auto-created
- **REQ-016-031**: System MUST list patient booking cancellation and change requests raised through Contact Support after acceptance on Screen 9, open the matching FR-006 action for each, and record a Resolved or Declined outcome with reason and audit entry
- **REQ-016-032**: System MUST NOT cancel or change a booking from FR-016 except through the FR-006 Cancel Booking or Change Appointment action, including cancellations caused by patient account suspension

### Data Governance Requirements

- **REQ-016-014**: System MUST require admins to enter access justification before viewing patient medical data (minimum 20 characters)
- **REQ-016-015**: System MUST log all medical data access in audit trail (who accessed, when, what data viewed, justification)
- **REQ-016-016**: System MUST process patient data deletion requests (GDPR) via anonymization + archival workflow, retaining compliance records (7 years)
- **REQ-016-017**: System MUST prevent hard deletion of patient accounts; all deletions must be soft-deletes with anonymization

### Security & Privacy Requirements

- **REQ-016-019**: System MUST enforce authenticated Super Admin access with MFA; additional RBAC tiers are out-of-scope for this release
- **REQ-016-020**: System MUST require enhanced confirmation + justification for high-impact actions (suspensions > 30 days, refunds > $1,000, permanent account deletions) even though the same Super Admin executes them
- **REQ-016-021**: System MUST log all admin downloads of patient head scan media in audit trail with timestamp, admin ID, and justification
- **REQ-016-022**: System MUST encrypt all patient data in transit (TLS 1.3) and at rest (AES-256)
- **REQ-016-023**: System MUST never display patient payment card details in admin interface (PCI-DSS compliance)

### Integration Requirements

- **REQ-016-024**: System MUST integrate with patient authentication module (P-01) for password reset and account unlock functionality
- **REQ-016-025**: System MUST integrate with payment module (P-03) to display transaction history and initiate refunds via Stripe API
- **REQ-016-026**: System MUST integrate with media storage service (S-05) to display patient head scan media with secure signed URLs
- **REQ-016-027**: System MUST integrate with notification service (S-03) to send notifications when admin takes actions affecting patients

---

## Key Entities

- **Entity 1 - Patient Account**
  - **Key attributes**: patient_id (unique code), name, email, phone, date_of_birth, location (country, city), registration_date, last_activity, account_status (active, suspended, deactivated), journey_status (inquiry, quoted, accepted, scheduled, in-progress, aftercare, completed, cancelled), cancellation_reason (conditional, from FR-026 Screen 5a or provider-caused `ProviderSuspended` / `ProviderDeactivated`), cancelled_at (conditional), flags/alerts; provider-caused impact context (affected references, prior stage, `supportRequired`, resolution audit, linked FR-034 case) is owned by the inquiry/case records per FR-015 Key Entities and read here
  - **Relationships**: One patient has many inquiries; one patient has many bookings; one patient has many payments; one patient has many communications (with providers, support, aftercare)

- **Entity 2 - Admin Action Log (Audit Trail)**
  - **Key attributes**: action_id, admin_id, patient_id, action_type (password_reset, booking_modification, refund, suspension), action_description, justification, timestamp, impact_level (low, medium, high), approval_status (approved, pending, rejected) - reserved for future RBAC implementation
  - **Relationships**: One admin performs many actions; one patient account has many admin actions performed on it

- **Entity 3 - Medical Data Access Log**
  - **Key attributes**: access_id, admin_id, patient_id, data_type (medical_questionnaire, 3d_scan, photos), access_timestamp, justification, data_accessed (specific fields/scans viewed)
  - **Relationships**: One admin has many medical data access logs; one patient has many medical data access logs

*Note*: Patient Support Ticket entities and lifecycle are specified in **FR-034** (Support Center & Ticketing).

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-11 | 1.0 | Initial PRD creation for FR-016 Admin Patient Management | AI Assistant |
| 2025-11-21 | 1.1 | Updated status to ✅ Verified & Approved and aligned admin role/medical access rules | AI Assistant |
| 2025-12-29 | 1.2 | Removed formal Support Ticket system scope from FR-016 and referenced dedicated FR-034 (Support Center & Ticketing) | AI Assistant |
| 2026-02-05 | 1.3 | Cancel Inquiry flow (FR-003 Workflow 5): Added "Cancelled" and "Accepted" to Stage filter and badge values (Screen 1); added "Patient Inquiry Cancellation" as system-generated audit event type (Screen 7) | AI     |
| 2026-02-09 | 1.4 | Cancellation integrity fixes: Added cancellation reason/timestamp fields to Screen 2 (Overview) with oversight-only rules. Added "Inquiry Cancelled" milestone to Screen 3 (Treatment Journey) with cascade summary. Updated Entity 1 journey_status enum to include accepted/cancelled with cancellation fields. Completed status badge color coding for all journey stages. Added User Story 8 (admin reviews cancelled inquiry). Fixed Last Updated date. | AI |
| 2026-03-03 | 1.5 | Clarified V1 scan media as head scan photo sets and updated admin medical data viewing to treat interactive 3D model viewing as a V2 enhancement. Updated viewer terminology, dependencies, and requirements accordingly. | AI |
| 2026-10-14 | 1.6 | Aligned provider suspension/deactivation cancellation cascade per CR-FR015-20261013-01 and FR-015 v1.9 | Vân Tay Media |
| 2026-10-16 | 1.7 | MTG-002 quote model alignment (minor wording, decision M18): the admin-support trigger and its user story now include an accepted booking closed for the FR-006 provider-fault transfer while the inquiry stays open. No CR needed (clarification only). | Vân Tay Media |
| 2026-10-18 | 1.8 | Consolidated verification corrections (decision D2): admin booking date edits are limited to the FR-006 guarded date change (`Accepted` or `Confirmed`, mandatory reason, slot availability check), and User Story 3 now flags linked travel records for an FR-008 travel-date review instead of stating that travel details remain intact. No CR: this aligns FR-016 with the existing FR-006 rule (CR-FR006-20261016-01) and does not change FR-016 scope. | Vân Tay Media |
| 2026-10-18 | 1.9 | Final audit corrections (Q37, Q42, Q43): journey stage lists in the Main Flow and Screen 1 now use the FR-003 stage list (Inquiry, Quoted, Accepted, Confirmed, In Progress, Aftercare, Completed, Cancelled); Suspended moves to a new Account Status Filter. New Flow A8 and Screen 9 (Booking Support Requests) route support-routed patient cancellation and change requests to the FR-006 Cancel Booking and Change Appointment actions with outcome, reason and audit entry. Rule 7, Admin Editability, User Story 3, REQ-016-010 and the FR-006 dependency use the FR-006 actions and `booking.rescheduled` or `booking.cancelled`; patient account suspension cancels bookings through FR-006. REQ-016-031 and REQ-016-032 added. See CR-FR016-20261016-01. | Product Owner / Documentation |
| 2026-10-27 | 1.10 | FR-015 dev-team follow-up decisions (F7), aligned with [CR-FR020-20261027-01](../fr020-notifications-alerts/change-request-2026-10-27-admin-support-recipients-status-email-timing.md): Flow A7 and Screen 2 Resolve Support require the FR-031 Respond to Support permission, and the Admin Support Required list requires View Patients; the admin-support alert goes to admins with Respond to Support. Wording: the Module Scope role-model line now points to the FR-031 admin roles and permissions instead of the outdated single Super Admin role. | Product Owner / Documentation |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | Product Owner | 2026-10-18 | Approved v1.9 via MTG-002 decision log (documentation only) |
| Product Owner | Joachim Trung Tuan | 2026-10-27 | Approved v1.10 (documentation only) with CR-FR020-20261027-01 |
| Technical Lead | [Pending] | [Pending] | [Pending] |
| Stakeholder | [Pending] | [Pending] | [Pending] |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0
**Based on**: FR-011 Aftercare & Recovery Management PRD template
**Last Updated**: 2026-10-27
