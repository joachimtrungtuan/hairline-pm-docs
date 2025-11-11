# Product Requirements Document: Treatment Execution & Documentation

**Module**: PR-03: Treatment Execution & Documentation
**Feature Branch**: `fr010-treatment-execution`
**Created**: 2025-11-11
**Status**: Draft
**Source**: FR-010 from system-prd.md

---

## Executive Summary

The Treatment Execution & Documentation module enables providers to document the entire hair transplant procedure lifecycle from patient arrival through treatment completion. This module serves as the critical transition point where patients move from "scheduled" bookings to active "in progress" treatments and eventually to "aftercare" status. The module captures comprehensive procedure details including surgeon information, techniques used, graft counts, treatment notes, before/during/after photos, and post-operative instructions that form the foundation for subsequent aftercare activities.

This module operates exclusively within the Provider Platform (PR-03) tenant, with data outputs consumed by both the Patient Platform (treatment completion notifications, post-op instructions) and Admin Platform (oversight, billing triggers). The module bridges the pre-treatment phase (bookings, scheduling) with the post-treatment phase (aftercare, final payment processing), ensuring complete documentation for audit trail, quality assurance, and seamless transition to long-term aftercare.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-XX)**: NOT directly involved during treatment execution; receives completion notifications and post-op instructions after treatment finishes
- **Provider Platform (PR-03)**: PRIMARY tenant - providers document all treatment activities in real-time
- **Admin Platform (A-XX)**: Oversight only - admins can view treatment progress, access documentation, monitor completion rates
- **Shared Services (S-05)**: Media Storage Service handles before/during/after photos and treatment documentation uploads

### Multi-Tenant Breakdown

**Patient Platform (P-XX)**:

- Receives real-time status updates (booking moved to "In Progress" when patient arrives)
- Receives treatment completion notification with post-op instructions
- Views treatment summary after completion (graft count, technique used, assigned medications)
- Accesses before/after photos uploaded by provider
- NOT involved in real-time treatment documentation

**Provider Platform (PR-03)**:

- Mark patient as "arrived" (triggers "In Progress" status)
- Document real-time treatment progress and observations
- Capture procedure details: surgeon, technique, graft count, donor/recipient areas
- Upload before/during/after photos with timestamps
- Record treatment notes and observations during procedure
- Prescribe post-operative medications with dosage and frequency
- Generate and send post-op instruction sheet to patient
- Select aftercare template to activate aftercare plan
- Mark treatment as "completed" (triggers "Aftercare" status and payment collection if pending)

**Admin Platform (A-XX)**:

- View all active treatments (real-time "In Progress" list)
- Monitor treatment completion rates by provider
- Access complete treatment documentation for quality assurance
- Review before/after photos for provider verification
- Audit treatment records for compliance
- View final payment collection status
- NO direct intervention in treatment documentation (provider-owned process)

**Shared Services (S-05)**:

- **Media Storage Service**: Secure storage for treatment photos with watermarking, encryption, and retrieval
- **S-02 Payment Processing Service**: Triggered for final payment collection upon treatment completion

### Communication Structure

**In Scope**:

- System-generated status notifications to patient (booking moved to "In Progress", treatment completed)
- Post-op instruction delivery to patient via email/in-app notification
- Provider-to-patient medication prescription delivery
- Admin notification of treatment completion for billing purposes

**Out of Scope**:

- Real-time chat between patient and provider during treatment (patients are physically present)
- Video documentation of procedure (future enhancement)
- Live streaming of treatment progress to patient's family (future enhancement)
- SMS notifications to patient's emergency contact (handled by S-03: Notification Service configuration)

### Entry Points

**Primary Entry Point**:

1. Provider navigates to "Scheduled Appointments" section in Provider Platform dashboard
2. Provider selects confirmed booking with procedure date = today or past
3. System displays patient details, booking confirmation, treatment package, pre-op notes
4. Provider clicks "Mark Patient as Arrived" button
5. System transitions booking status from "Confirmed" → "In Progress"
6. Treatment documentation interface becomes active

**Secondary Entry Points**:

- Provider can resume documentation for "In Progress" treatments from dashboard
- Provider can view completed treatments from "Treatment History" section (read-only mode)

**Access Requirements**:

- Provider must have role: Owner, Admin, or Doctor (Coordinators cannot document treatments)
- Patient must have "Confirmed" booking status (payment completed)
- Procedure date must be today or in the past (cannot mark future appointments as "In Progress")

---

## Business Workflows

### Main Flow: Treatment Execution & Documentation

**Actors**: Provider (Doctor/Surgeon), Patient, System, Admin
**Trigger**: Patient arrives at clinic on scheduled procedure day
**Outcome**: Treatment documented, patient receives post-op instructions, booking status moves to "Aftercare"

**Steps**:

1. **Patient Arrival**
   - Patient arrives at clinic and checks in with front desk
   - Provider (Doctor) opens Provider Platform and navigates to "Scheduled Appointments"
   - Provider selects patient's booking from list of today's appointments
   - System displays patient summary: name, contact details (visible post-payment), booking details, treatment package, medical questionnaire with alerts, 3D scans

2. **Pre-Procedure Review**
   - Provider reviews patient's medical questionnaire responses
   - System highlights critical medical alerts (red) and standard alerts (yellow) in color-coded format
   - Provider reviews 3D scans captured during inquiry phase
   - Provider confirms treatment plan: technique, estimated graft count, donor/recipient areas
   - Provider clicks "Mark Patient as Arrived" button

3. **Status Transition to "In Progress"**
   - System automatically updates booking status from "Confirmed" → "In Progress"
   - System sends notification to patient mobile app: "Your treatment is starting"
   - System records arrival timestamp
   - Treatment documentation interface activates

4. **Before-Treatment Documentation**
   - Provider captures "before" photos of patient's head (multiple angles)
   - System watermarks photos with anonymized patient ID and timestamp
   - Provider documents pre-procedure observations and notes
   - Provider confirms surgeon assignment (selected during quote creation, can be changed if needed)

5. **Treatment Execution & Real-Time Updates**
   - Provider begins hair transplant procedure
   - Provider updates treatment progress at intervals:
     - Donor area harvesting progress
     - Graft extraction count (running total)
     - Recipient area implantation progress
     - Technique specifics (manual FUE, motorized FUE, DHI pen, etc.)
   - Provider captures "during" photos at key milestones (optional)
   - Provider records observations and any complications or deviations from plan

6. **Treatment Completion Documentation**
   - Provider captures "after" photos of completed procedure (multiple angles)
   - System watermarks photos with patient ID and timestamp
   - Provider documents final treatment details:
     - Total graft count (actual, may differ from estimate)
     - Donor area(s) used
     - Recipient area(s) covered
     - Technique(s) employed
     - Procedure duration (start time - end time)
     - Complications or notable events (if any)
   - Provider uploads treatment summary notes

7. **Post-Operative Medication Prescription**
   - Provider prescribes post-op medications:
     - Medication name (e.g., "Amoxicillin 500mg")
     - Dosage (e.g., "1 capsule")
     - Frequency (e.g., "2x daily for 7 days")
     - Instructions (e.g., "Take with food")
   - System generates medication schedule for patient
   - System sends medication list to patient via email and in-app notification

8. **Aftercare Template Selection**
   - Provider selects aftercare template from admin-created list (e.g., "Standard FUE Aftercare - 12 months")
   - Provider customizes template with patient-specific instructions
   - Provider specifies any additional restrictions or guidelines
   - System generates complete aftercare plan with milestones based on template

9. **Post-Op Instruction Generation**
   - System generates post-op instruction sheet including:
     - Washing instructions and timeline
     - Sleeping position guidelines
     - Activity restrictions (exercise, sun exposure, swimming)
     - Medication schedule
     - Follow-up appointment details (if applicable)
     - Emergency contact information (clinic and Hairline aftercare team)
   - System sends post-op instructions to patient via email and in-app notification

10. **Treatment Completion & Status Transition**
    - Provider clicks "Mark Treatment as Completed" button
    - System transitions booking status from "In Progress" → "Aftercare"
    - System sends completion notification to patient: "Your procedure is complete! View your aftercare plan"
    - System activates patient's aftercare plan (milestones, scans, questionnaires begin)
    - System triggers final payment collection (if deposit-only payment, collects remaining balance)
    - System notifies admin of treatment completion for billing reconciliation

### Alternative Flows

**A1: Patient Arrives Early (Before Scheduled Time)**:

- **Trigger**: Patient arrives 1+ hours before scheduled procedure time
- **Steps**:
  1. Provider attempts to mark patient as "arrived"
  2. System displays warning: "Scheduled procedure time is [TIME]. Mark as arrived anyway?"
  3. Provider confirms or postpones arrival marking
  4. If confirmed, system proceeds with status transition to "In Progress"
- **Outcome**: Treatment proceeds earlier than scheduled; original appointment time preserved in booking record

**A2: Multiple Surgeons/Clinicians Involved**:

- **Trigger**: Procedure requires multiple surgeons (e.g., large graft count, specialized technique)
- **Steps**:
  1. Provider documents primary surgeon (selected during quote)
  2. Provider adds secondary surgeon(s) from clinic staff list
  3. System records all clinicians involved with their roles
  4. Treatment notes can specify which surgeon handled which phase
- **Outcome**: All involved clinicians credited in treatment record

**A3: Treatment Plan Modified During Procedure**:

- **Trigger**: Provider discovers different donor area quality or patient requests scope change mid-procedure
- **Steps**:
  1. Provider pauses documentation to update treatment plan
  2. Provider adjusts estimated graft count, donor area selection, or technique
  3. Provider documents reason for modification in notes
  4. System preserves original plan for comparison with final results
  5. Provider continues treatment with modified plan
- **Outcome**: Both original and modified treatment plans documented for audit trail

**A4: Treatment Paused/Resumed (Multi-Day Procedure)**:

- **Trigger**: Large procedure requiring multiple sessions over 2-3 days
- **Steps**:
  1. Provider marks day 1 session as "Paused" with next session date
  2. System maintains "In Progress" status but flags as "Multi-Day Procedure"
  3. Provider resumes documentation on day 2
  4. System consolidates all session notes into single treatment record
  5. Provider marks entire procedure as "Completed" after final session
- **Outcome**: Multi-day procedure tracked as single treatment with session-by-session documentation

**B1: Patient No-Show (Does Not Arrive)**:

- **Trigger**: Patient fails to arrive at clinic on scheduled procedure day
- **Steps**:
  1. Provider waits reasonable grace period (e.g., 2 hours past appointment time)
  2. Provider attempts to contact patient via phone/messaging
  3. If patient unreachable or cancels last-minute, provider marks booking as "No-Show"
  4. System transitions booking status from "Confirmed" → "No-Show"
  5. System applies no-show policy: deposit retained, remaining balance refunded (per cancellation policy)
  6. System notifies admin of no-show for financial reconciliation
  7. System sends notification to patient with rebooking options
- **Outcome**: Booking flagged as no-show; financial penalties applied; rebooking offered

**B2: Medical Complication Prevents Treatment Start**:

- **Trigger**: Pre-procedure review reveals unmanaged medical condition or patient arrives unwell
- **Steps**:
  1. Provider identifies medical issue during pre-procedure consultation
  2. Provider documents reason treatment cannot proceed (e.g., "Patient has active scalp infection")
  3. Provider marks booking as "Postponed - Medical Reasons"
  4. System transitions status from "Confirmed" → "Postponed"
  5. System triggers rescheduling workflow (no financial penalty to patient)
  6. Provider provides medical clearance requirements and suggests new dates
  7. System notifies admin and patient of postponement
- **Outcome**: Treatment postponed without penalty; patient given medical clearance instructions

**B3: Treatment Interrupted (Emergency, Equipment Failure)**:

- **Trigger**: Unexpected interruption during treatment (medical emergency, power outage, equipment malfunction)
- **Steps**:
  1. Provider pauses treatment and documents interruption reason
  2. Provider assesses patient safety and treatment status
  3. If treatment can resume within 2 hours:
     - Provider marks treatment as "Paused - Interruption"
     - System maintains "In Progress" status
     - Provider resumes and completes treatment when issue resolved
  4. If treatment cannot resume (extended interruption or patient safety concern):
     - Provider marks treatment as "Incomplete - Interrupted"
     - System transitions status to "Requires Rescheduling"
     - Provider documents completed work (grafts harvested/implanted)
     - System triggers rescheduling workflow for treatment completion
- **Outcome**: Treatment interrupted, documented, and either resumed or rescheduled based on circumstances

**B4: Patient Withdraws Consent During Procedure**:

- **Trigger**: Patient requests to stop treatment mid-procedure (rare but possible)
- **Steps**:
  1. Provider stops procedure immediately
  2. Provider documents patient's withdrawal of consent with timestamp
  3. Provider completes emergency post-procedure care (wound closure, dressing)
  4. Provider marks treatment as "Incomplete - Patient Withdrawal"
  5. System documents completed work (grafts harvested/implanted to that point)
  6. Provider generates modified post-op instructions for partial procedure
  7. System triggers financial reconciliation (partial refund based on work completed)
  8. System notifies admin of situation for manual intervention
- **Outcome**: Treatment stopped, partial work documented, financial adjustment initiated

---

## Screen Specifications

### Screen 1: Treatment Dashboard - Scheduled Appointments List

**Purpose**: Display all confirmed bookings scheduled for today and upcoming days; allow provider to initiate treatment documentation by marking patient as arrived.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Patient Name | text | Yes (read-only) | Full name of patient (visible post-payment) | Display only |
| Patient ID | text | Yes (read-only) | Anonymized patient identifier (e.g., "HPID251011A47B2") | Display only |
| Procedure Date | date | Yes (read-only) | Scheduled date of treatment | Display only |
| Procedure Time | time | Yes (read-only) | Scheduled time slot | Display only |
| Treatment Type | select | Yes (read-only) | Hair transplant technique (FUE, DHI, FUT) | Display only |
| Estimated Grafts | number | Yes (read-only) | Graft count from quote | Display only |
| Assigned Surgeon | select | Yes (read-only) | Clinician selected during quote | Display only |
| Booking Status | badge | Yes (read-only) | Current status: "Confirmed", "In Progress", "Completed" | Color-coded: blue (confirmed), orange (in progress), green (completed) |
| Actions | button group | Yes | "View Details", "Mark as Arrived" (if today/past), "View Treatment Record" (if completed) | Buttons enabled/disabled based on status and date |

**Business Rules**:

- **Date Filtering**: Default view shows today's appointments; provider can switch to "Upcoming" (next 7 days) or "All Scheduled"
- **Mark as Arrived Enabled**: "Mark as Arrived" button enabled ONLY if:
  - Booking status = "Confirmed"
  - Procedure date ≤ today
  - Provider role = Owner, Admin, or Doctor (not Coordinator)
- **Status Badges**: Color-coded for quick visual scanning (blue = confirmed, orange = in progress, green = completed)
- **Sort Order**: Default sort by procedure time (earliest first); provider can re-sort by patient name or graft count

**Notes**:

- This is the primary entry point for treatment documentation workflow
- List view optimized for quick scanning during busy clinic days
- Mobile-responsive design for providers using tablets in treatment rooms

---

### Screen 2: Patient Arrival Confirmation & Pre-Procedure Review

**Purpose**: Display comprehensive patient information for provider to review before marking as arrived; confirm readiness to begin treatment.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Patient Full Name | text | Yes (read-only) | Patient's complete name | Display only |
| Contact Phone | text | Yes (read-only) | Patient's phone number | Display only |
| Treatment Package | text | Yes (read-only) | Selected treatment package from quote | Display only |
| Estimated Graft Count | number | Yes (read-only) | Graft estimate from quote | Display only |
| Assigned Surgeon | select | Yes | Clinician who will perform procedure | Editable if change needed before arrival marking |
| Medical Questionnaire | expandable section | Yes (read-only) | Patient's medical history responses | Color-coded alerts: red (critical), yellow (standard), green (none) |
| 3D Scans | image viewer | Yes (read-only) | Patient's head scans from inquiry | Interactive 3D viewer with zoom/rotate |
| Booking Notes | text area | No (read-only) | Any special notes from booking or admin | Display only |
| Arrival Time | time | No | Actual arrival time (auto-filled with current time when marked) | System-generated, editable |
| Confirm Arrival | button | Yes | Primary action to mark patient as arrived | Triggers status transition to "In Progress" |

**Business Rules**:

- **Medical Alert Display**: Critical conditions (red) displayed prominently at top; standard alerts (yellow) in expandable section; green checkmark if no alerts
- **Surgeon Change**: If assigned surgeon is unavailable, provider can reassign to another clinician before marking arrival (change logged in audit trail)
- **3D Scan Viewer**: Interactive viewer allows provider to zoom, rotate, and review multiple angles captured during inquiry
- **Confirm Arrival Action**: Upon clicking "Confirm Arrival":
  - System records arrival timestamp
  - Status transitions from "Confirmed" → "In Progress"
  - Treatment documentation interface activates
  - Patient receives push notification: "Your treatment is starting"
  - Provider redirected to Treatment Documentation screen

**Notes**:

- This screen acts as final safety check before beginning procedure
- Provider must acknowledge viewing medical alerts (implicit acknowledgment via arrival confirmation)
- Screen includes "Cancel" option to return to dashboard if patient not ready or medical issue identified

---

### Screen 3: Treatment Documentation Interface (During Procedure)

**Purpose**: Real-time documentation of treatment progress, observations, and photos during active procedure; central workspace for all treatment activities.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Treatment Status | badge | Yes (read-only) | Current status: "In Progress" | Display only |
| Procedure Start Time | time | Yes (read-only) | Timestamp when marked as arrived | Display only |
| Elapsed Time | timer | Yes (read-only) | Live timer showing procedure duration | Updates every minute |
| Assigned Surgeon | select | Yes | Primary surgeon performing procedure | Editable; dropdown of clinic staff with "Doctor" role |
| Additional Clinicians | multi-select | No | Other clinicians assisting (if applicable) | Optional; dropdown of clinic staff |
| Donor Area(s) | multi-select | Yes | Body areas for graft extraction | Options: "Back of head (occipital)", "Sides of head (temporal)", "Beard area", "Chest", "Other" |
| Recipient Area(s) | multi-select | Yes | Target areas for graft implantation | Options: "Hairline", "Crown", "Mid-scalp", "Temples", "Beard" |
| Technique(s) Used | multi-select | Yes | Hair transplant method(s) employed | Options from treatment catalog: "Manual FUE", "Motorized FUE", "DHI", "FUT", "Sapphire FUE" |
| Grafts Harvested | number | Yes | Running count of grafts extracted from donor area | Min: 0, Max: 10000, incremental updates allowed |
| Grafts Implanted | number | Yes | Running count of grafts implanted in recipient area | Min: 0, Max: value of "Grafts Harvested" |
| Treatment Notes | rich text area | Yes | Real-time observations, complications, deviations from plan | Max 5000 characters; supports bullet points, timestamps |
| Before Photos | image uploader | Yes | Photos captured before procedure starts | Min 3 images (front, sides, top); Max 10 images; JPG/PNG; Max 10MB per file |
| During Photos | image uploader | No | Optional photos at key milestones during procedure | Max 20 images; JPG/PNG; Max 10MB per file |
| After Photos | image uploader | Yes | Photos captured after procedure completion | Min 3 images (front, sides, top); Max 10 images; JPG/PNG; Max 10MB per file |
| Complications/Deviations | checkbox + text area | No | Flag if any issues occurred; describe | If checked, text area becomes required (max 1000 chars) |
| Save Progress | button | Yes | Save current documentation state without completing | Allows provider to pause and resume later |
| Mark as Completed | button | Yes | Finalize treatment documentation and move to next phase | Triggers validation of all required fields before proceeding |

**Business Rules**:

- **Auto-Save**: System auto-saves all field changes every 2 minutes to prevent data loss
- **Photo Watermarking**: All uploaded photos automatically watermarked with anonymized patient ID and timestamp before storage
- **Graft Count Validation**: "Grafts Implanted" cannot exceed "Grafts Harvested" (error message if attempted)
- **Required Field Validation**: "Mark as Completed" button disabled until all required fields populated
- **Elapsed Timer**: Live timer provides awareness of procedure duration; no enforcement of time limits
- **Technique Multi-Select**: Provider can document hybrid techniques (e.g., "FUE + DHI") if multiple methods used in same procedure

**Notes**:

- This screen remains active throughout procedure (can be hours); designed for tablet use in treatment room
- Large touch-friendly buttons and inputs for ease of use with gloves
- Progress saved continuously to prevent loss if browser closes or device battery dies
- Photos uploaded to secure storage (S-05: Media Storage Service) with encryption

---

### Screen 4: Post-Operative Documentation & Completion

**Purpose**: Finalize treatment documentation, prescribe medications, generate post-op instructions, select aftercare template, and complete treatment status transition.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Final Graft Count | number | Yes (editable) | Total grafts successfully implanted | Pre-filled from "Grafts Implanted"; editable for final adjustment |
| Procedure End Time | time | Yes | Timestamp when procedure completed | Auto-filled with current time; editable |
| Total Procedure Duration | time (read-only) | Yes (calculated) | Total time from start to end | Calculated: End Time - Start Time |
| Treatment Summary | text area | Yes | Brief summary of procedure outcome | Max 1000 characters; provider's assessment |
| Medications Prescribed | repeating section | Yes | List of post-op medications | Min 1 medication required; see medication fields below |
| - Medication Name | text | Yes | Drug name and dosage (e.g., "Amoxicillin 500mg") | Max 100 characters |
| - Dosage | text | Yes | Amount per dose (e.g., "1 capsule") | Max 50 characters |
| - Frequency | select | Yes | How often to take | Options: "1x daily", "2x daily", "3x daily", "Every 8 hours", "Every 12 hours", "As needed" |
| - Duration | text | Yes | Length of medication course (e.g., "7 days", "Until finished") | Max 50 characters |
| - Instructions | text area | No | Special instructions (e.g., "Take with food", "Avoid alcohol") | Max 200 characters |
| Aftercare Template | select | Yes | Pre-defined aftercare milestone plan | Dropdown of admin-created templates (e.g., "Standard FUE - 12 months", "DHI - 6 months") |
| Custom Aftercare Instructions | text area | No | Patient-specific aftercare guidance beyond template | Max 1000 characters; supplements template instructions |
| Activity Restrictions | multi-select | Yes | Physical activities to avoid | Options: "Strenuous exercise (2 weeks)", "Sun exposure (4 weeks)", "Swimming (3 weeks)", "Sauna/steam room (4 weeks)", "Alcohol (1 week)" |
| Follow-Up Appointment | date + time | No | In-person follow-up if needed (uncommon, as aftercare is remote) | Optional; date must be future |
| Generate Post-Op Instructions | button | Yes | Create patient instruction sheet | Opens preview modal with generated instructions |
| Complete Treatment | button | Yes | Finalize treatment and transition to aftercare status | Triggers status change, aftercare activation, final payment |

**Business Rules**:

- **Medication Repeating Section**: Provider can add multiple medications; "Add Medication" button to add new entry; "Remove" button to delete entry
- **Aftercare Template Required**: Provider MUST select aftercare template; this determines milestone structure, scan frequency, questionnaire schedule
- **Custom Instructions Supplement Template**: Custom instructions added to template-generated aftercare plan (not replacement)
- **Post-Op Instructions Preview**: Provider must review generated instructions before final completion; can edit/adjust as needed
- **Complete Treatment Validation**: All required fields must be filled before "Complete Treatment" button enabled
- **Complete Treatment Action**:
  - System transitions booking status from "In Progress" → "Aftercare"
  - System activates patient's aftercare plan based on selected template
  - System sends post-op instructions to patient via email and in-app notification
  - System sends medication schedule to patient
  - System triggers final payment collection (if deposit-only booking)
  - System notifies admin of treatment completion for billing
  - Provider redirected to "Treatment Complete" confirmation screen

**Notes**:

- This is the final step in treatment documentation workflow
- Post-op instructions auto-generated from template but provider can customize
- Aftercare template selection is critical - determines entire 6-12 month aftercare structure
- Provider cannot return to edit after clicking "Complete Treatment" (final snapshot captured)

---

## Business Rules

### General Module Rules

- **Rule 1**: Booking status MUST transition through sequence: Confirmed → In Progress → Aftercare → Completed (no skipping stages)
- **Rule 2**: Treatment documentation MUST be initiated by marking patient as "arrived" (cannot pre-document treatments)
- **Rule 3**: Procedure date MUST be today or in past to enable "Mark as Arrived" action (cannot mark future appointments)
- **Rule 4**: Provider role MUST be Owner, Admin, or Doctor to document treatments (Coordinators can view but not edit)
- **Rule 5**: All timestamps (arrival, start, end) MUST be recorded in UTC and displayed in provider's local timezone
- **Rule 6**: Treatment documentation MUST be completed within 24 hours of marking patient as arrived (system sends reminder notifications)
- **Rule 7**: Maximum one treatment can be "In Progress" per patient at any time (prevents duplicate documentation)

### Data & Privacy Rules

- **Privacy Rule 1**: Patient full name and contact details visible to provider ONLY after payment completion (pre-payment shows anonymized ID)
- **Privacy Rule 2**: Treatment photos MUST be encrypted at rest using AES-256 (handled by S-05: Media Storage Service)
- **Privacy Rule 3**: All treatment photos MUST be watermarked with anonymized patient ID and timestamp before storage
- **Privacy Rule 4**: Treatment documentation MUST be retained for minimum 7 years per healthcare compliance regulations
- **Privacy Rule 5**: Only assigned provider clinic can access patient's treatment documentation (other clinics cannot view)
- **Audit Rule**: All changes to treatment documentation MUST be logged with timestamp, user ID, and action type (create, update, delete)
- **HIPAA/GDPR**: Treatment photos and medical notes constitute Protected Health Information (PHI) and MUST comply with data protection regulations

### Admin Editability Rules

**Editable by Admin**:

- Treatment catalog (hair transplant techniques available for selection during documentation)
- Aftercare templates (milestone structures, questionnaire schedules, scan frequencies)
- Medication templates (common post-op medication presets to speed up prescribing)
- Post-op instruction templates (standard instruction text that providers can customize)
- Photo upload limits (max number of photos, max file size)

**Fixed in Codebase (Not Editable)**:

- Status transition sequence (Confirmed → In Progress → Aftercare → Completed cannot be changed)
- Photo watermarking algorithm (anonymized patient ID + timestamp format)
- Encryption standards (AES-256 for photos, TLS 1.3 for data in transit)
- Audit log retention (10 years minimum, immutable)
- Required fields for treatment completion (graft count, technique, surgeon, photos, medications, aftercare template)

**Configurable with Restrictions**:

- Admin can adjust "treatment documentation completion deadline" (default 24 hours, range 12-48 hours)
- Admin can configure reminder notification timing (default: 12 hours after arrival if not completed)
- Admin cannot disable required fields or bypass validation rules (ensures data quality)

### Payment & Billing Rules

- **Payment Rule 1**: Final payment MUST be collected upon treatment completion if patient paid deposit only
- **Payment Rule 2**: Provider payout MUST be triggered after treatment marked as "Completed" (admin initiates payout process)
- **Billing Rule 1**: Treatment completion timestamp determines billing cycle cutoff (treatments completed by month-end included in that month's reconciliation)
- **Currency Rule**: Final payment amount locked at booking time (no currency fluctuation adjustment at treatment completion)
- **No-Show Rule**: If patient marked as "No-Show", deposit retained per cancellation policy, provider receives payout for deposit minus platform commission

---

## Success Criteria

### Patient Experience Metrics

- **SC-001**: Patients receive treatment status updates in real-time (status change notifications delivered within 1 minute of provider action)
- **SC-002**: Patients receive post-op instructions within 5 minutes of treatment completion
- **SC-003**: 95% of patients report receiving clear, understandable post-op instructions (measured via post-treatment survey)
- **SC-004**: Patients can view their before/after photos in mobile app within 1 hour of treatment completion

### Provider Efficiency Metrics

- **SC-005**: Providers complete treatment documentation within 1 hour of procedure end for 90% of treatments
- **SC-006**: Providers spend less than 10 minutes on post-treatment documentation (medication prescribing, aftercare template selection, post-op instructions)
- **SC-007**: 85% of providers report treatment documentation workflow as "easy to use" or "very easy to use" (measured via provider satisfaction survey)
- **SC-008**: Provider can upload and watermark treatment photos in under 2 minutes per photo set

### Admin Management Metrics

- **SC-009**: Admins can view all active treatments (currently "In Progress") in real-time dashboard
- **SC-010**: 100% of completed treatments have full documentation (no missing required fields)
- **SC-011**: Admins can audit any treatment record within 30 seconds (search by patient ID, provider, date)
- **SC-012**: Zero incidents of missing treatment documentation in completed bookings

### System Performance Metrics

- **SC-013**: Status transition from "Confirmed" → "In Progress" completes within 2 seconds
- **SC-014**: Photo uploads complete within 10 seconds per photo (for files up to 10MB on standard broadband)
- **SC-015**: Treatment documentation auto-save occurs every 2 minutes with no data loss
- **SC-016**: System supports 50 concurrent "In Progress" treatments across all providers without performance degradation
- **SC-017**: 99.9% uptime for treatment documentation functionality during business hours

### Business Impact Metrics

- **SC-018**: Treatment completion rate (confirmed bookings that reach "Completed" status) exceeds 95%
- **SC-019**: Final payment collection success rate exceeds 98% (for bookings with deposit-only payment)
- **SC-020**: Zero financial discrepancies between documented treatments and billing records
- **SC-021**: Provider payout processing time reduced by 40% compared to manual treatment record collection

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **FR-004 / Module PR-02: Inquiry & Quote Management**
  - **Why needed**: Treatment documentation requires access to quote details (estimated graft count, technique, assigned surgeon, treatment package)
  - **Integration point**: Provider views quote details in pre-procedure review screen; quote data pre-fills treatment documentation fields

- **FR-006 / Module P-03: Booking & Payment**
  - **Why needed**: Treatment can only be documented for "Confirmed" bookings (payment completed); final payment collection triggered upon treatment completion
  - **Integration point**: System validates booking status before allowing "Mark as Arrived"; treatment completion triggers final payment processing

- **FR-011 / Module P-05: Aftercare & Progress Monitoring**
  - **Why needed**: Treatment completion activates patient's aftercare plan; aftercare template selection during treatment documentation determines entire aftercare structure
  - **Integration point**: Provider selects aftercare template in post-treatment documentation; system generates aftercare milestones, scan schedules, questionnaire cadence based on template

- **FR-009 / Module PR-01: Auth & Team Management**
  - **Why needed**: Treatment documentation requires authenticated provider with appropriate role (Owner, Admin, Doctor); surgeon assignment draws from clinic staff list
  - **Integration point**: System validates provider role before enabling treatment documentation; surgeon dropdown populated from clinic staff with "Doctor" role

- **FR-020 / Module S-03: Notification Service**
  - **Why needed**: Status transition notifications sent to patient (treatment started, treatment completed); post-op instructions and medication schedules delivered via email/push
  - **Integration point**: Treatment documentation triggers notification events; notification service handles delivery to patient mobile app and email

### External Dependencies (APIs, Services)

- **External Service 1: S-05 Media Storage Service**
  - **Purpose**: Secure storage for treatment photos (before/during/after) with encryption, watermarking, and retrieval
  - **Integration**: RESTful API for photo uploads; automatic watermarking with patient ID and timestamp; encrypted storage
  - **Failure handling**: If storage service unavailable, photos queued locally on provider device and uploaded when service restored; treatment completion blocked until photos uploaded successfully

- **External Service 2: S-02 Payment Processing Service (Stripe)**
  - **Purpose**: Process final payment upon treatment completion (if patient paid deposit only)
  - **Integration**: Treatment completion triggers payment intent for remaining balance; Stripe API processes payment
  - **Failure handling**: If payment fails, system flags booking as "Pending Final Payment"; admin notified to manually reconcile; treatment still marked as "Completed" (payment decoupled from treatment status)

### Data Dependencies

- **Entity 1: Confirmed Booking Record**
  - **Why needed**: Treatment documentation can only be initiated for bookings with status = "Confirmed" (payment completed)
  - **Source**: P-03: Booking & Payment module; booking confirmed when patient completes payment

- **Entity 2: Quote Details (Treatment Package, Graft Estimate, Surgeon)**
  - **Why needed**: Quote details pre-fill treatment documentation fields; provider reviews estimated graft count vs. actual graft count
  - **Source**: PR-02: Inquiry & Quote Management module; quote accepted by patient during booking

- **Entity 3: Aftercare Templates**
  - **Why needed**: Provider must select aftercare template during treatment completion; template defines milestone structure for entire aftercare phase
  - **Source**: Admin Platform A-09: System Settings & Configuration; admin creates and manages aftercare templates

- **Entity 4: Provider Clinic Staff List**
  - **Why needed**: Surgeon assignment and additional clinician selection require active staff members with appropriate roles
  - **Source**: PR-01: Auth & Team Management module; provider creates staff accounts with roles (Doctor, Coordinator, etc.)

---

## Assumptions

### User Behavior Assumptions

- **Assumption 1**: Providers will mark patients as "arrived" promptly when they check in (not hours later)
- **Assumption 2**: Providers will document treatment progress in real-time or immediately after procedure (not days later from memory)
- **Assumption 3**: Providers will upload before/after photos from same device used for treatment documentation (not separately)
- **Assumption 4**: Providers will select appropriate aftercare template based on treatment type and patient needs (not randomly)
- **Assumption 5**: Patients will arrive on scheduled procedure date (no-show rate below 5%)

### Technology Assumptions

- **Assumption 1**: Providers use tablets or desktop computers in treatment rooms with stable internet connectivity
- **Assumption 2**: Providers have access to digital cameras or smartphone cameras for before/after photos (or use device camera)
- **Assumption 3**: Photo file sizes average 2-5MB per image (modern smartphone quality)
- **Assumption 4**: Treatment documentation interface accessed via modern web browsers (Chrome, Safari, Firefox, Edge - latest 2 versions)
- **Assumption 5**: Media storage service (S-05) has sufficient capacity for 10,000+ treatment photo sets per year

### Business Process Assumptions

- **Assumption 1**: Hair transplant procedures typically last 4-8 hours (treatment documentation designed for long-duration procedures)
- **Assumption 2**: Providers perform 1-5 treatments per day (system designed for moderate concurrent treatment volume per clinic)
- **Assumption 3**: Aftercare plans are standardized enough to use templates with minor customization (not fully bespoke per patient)
- **Assumption 4**: Final payment collection occurs on treatment day or immediately after (not deferred weeks later)
- **Assumption 5**: Providers prescribe 3-5 medications per patient on average (medication prescribing interface designed for this volume)

---

## Implementation Notes

### Technical Considerations

- **Architecture**: Treatment documentation requires real-time data persistence with auto-save every 2 minutes to prevent data loss during long procedures
- **Technology**: Photo uploads should support chunked/resumable transfers for large files (10MB) on potentially unstable clinic internet connections
- **Performance**: Image watermarking should occur asynchronously server-side (not blocking provider workflow); watermarked images cached for fast retrieval
- **Storage**: Treatment photos require long-term archival storage (7+ years) with fast retrieval (< 5 seconds) for provider/admin/patient access

### Integration Points

- **Integration 1: Provider Platform → Media Storage Service (S-05)**
  - **Data format**: Multipart form upload with metadata (patient ID, treatment ID, photo type: "before"/"during"/"after", timestamp)
  - **Authentication**: OAuth 2.0 bearer token with provider identity
  - **Error handling**: If upload fails, photos queued locally; retry with exponential backoff; provider notified of pending uploads

- **Integration 2: Provider Platform → Payment Processing Service (S-02)**
  - **Data format**: JSON payload with booking ID, remaining balance amount, currency, patient payment method ID
  - **Authentication**: API key authentication (server-to-server)
  - **Error handling**: If payment fails, log error, flag booking as "Pending Final Payment", notify admin; do not block treatment completion

- **Integration 3: Provider Platform → Notification Service (S-03)**
  - **Data format**: JSON payload with notification type ("treatment_started", "treatment_completed"), recipient (patient ID), message content, delivery channels (email, push)
  - **Authentication**: API key authentication (server-to-server)
  - **Error handling**: If notification fails, queue for retry; notifications are informational, not critical to treatment workflow

- **Integration 4: Provider Platform → Patient Platform (P-05 Aftercare Activation)**
  - **Data format**: JSON payload with patient ID, aftercare template ID, custom instructions, treatment completion date, milestone schedule
  - **Authentication**: OAuth 2.0 bearer token with provider identity
  - **Error handling**: If aftercare activation fails, treatment still marked complete, but admin notified to manually activate aftercare plan

### Scalability Considerations

- **Current scale**: Expected 50-100 treatments per day across all providers at launch
- **Growth projection**: Plan for 500 treatments per day within 12 months as provider network grows
- **Peak load**: Handle 100 concurrent "In Progress" treatments (100 providers documenting simultaneously)
- **Data volume**: Expect 200GB of treatment photos per month (average 10 photos per treatment, 5MB per photo, 1000 treatments/month)
- **Scaling strategy**: Horizontal scaling of API servers; CDN for photo delivery; separate database for treatment records with read replicas for reporting

### Security Considerations

- **Authentication**: Providers must authenticate via OAuth 2.0 with role-based access control (RBAC); only Owner, Admin, Doctor roles can document treatments
- **Authorization**: Providers can only document treatments for their own clinic's bookings (cross-clinic access forbidden); system validates clinic ownership before allowing documentation
- **Encryption**: All treatment photos encrypted at rest (AES-256) in media storage service; photos transmitted over TLS 1.3; patient medical data encrypted in database
- **Audit trail**: All treatment documentation actions logged with timestamp, provider user ID, IP address, action type (create, update, status change); audit logs immutable and retained 10 years
- **Threat mitigation**: Rate limiting on photo uploads (max 50 uploads per hour per provider) to prevent abuse; file type validation (only JPG, PNG allowed) and virus scanning on uploads
- **Compliance**: Treatment documentation must comply with HIPAA-equivalent standards (access controls, audit trails, encryption); patient consent obtained during booking for photo storage and usage

---

## User Scenarios & Testing

### User Story 1 - Provider Documents Standard FUE Treatment (Priority: P1)

A provider performs a routine FUE (Follicular Unit Extraction) hair transplant procedure and documents the entire treatment from patient arrival through completion, including before/after photos, graft counts, and post-op instructions.

**Why this priority**: This is the core workflow that 80%+ of treatments follow; must work flawlessly for MVP launch. Represents the happy path with no complications or deviations.

**Independent Test**: Can be fully tested by creating a confirmed booking, marking patient as arrived, filling in all required treatment details, uploading photos, prescribing medications, selecting aftercare template, and verifying status transitions to "Aftercare" with all data persisted correctly.

**Acceptance Scenarios**:

1. **Given** a confirmed booking with procedure date = today, **When** provider marks patient as "arrived", **Then** booking status transitions to "In Progress" and treatment documentation interface activates
2. **Given** treatment documentation interface is active, **When** provider uploads 3 "before" photos, **Then** photos are watermarked with patient ID and timestamp and stored securely
3. **Given** provider has documented graft counts and technique, **When** provider clicks "Mark as Completed", **Then** system validates all required fields are filled before proceeding
4. **Given** all required fields are filled, **When** provider completes treatment documentation, **Then** status transitions to "Aftercare", patient receives post-op instructions, aftercare plan activates, and final payment processing triggered

---

### User Story 2 - Provider Handles Treatment Interruption (Priority: P2)

During an active treatment, a power outage interrupts the procedure. Provider documents the interruption, marks treatment as paused, and resumes documentation when power restored.

**Why this priority**: Edge case that occurs infrequently (< 5% of treatments) but critical for data integrity; providers must be able to pause and resume without losing documentation.

**Independent Test**: Can be tested by starting treatment documentation, filling some fields, simulating interruption (close browser tab), verifying auto-saved data persists, re-opening treatment record, and resuming documentation from where provider left off.

**Acceptance Scenarios**:

1. **Given** treatment documentation is in progress, **When** provider closes browser unexpectedly, **Then** all data entered up to last auto-save (2 minutes ago) is preserved
2. **Given** treatment was paused due to interruption, **When** provider re-opens treatment record, **Then** system displays last saved state with option to resume
3. **Given** provider resumes interrupted treatment, **When** provider continues documentation and marks as complete, **Then** interruption logged in audit trail but treatment completes normally

---

### User Story 3 - Provider Manages Patient No-Show (Priority: P2)

A patient fails to arrive at clinic on scheduled procedure day. Provider waits reasonable grace period, attempts to contact patient, and marks booking as "No-Show" to trigger financial reconciliation.

**Why this priority**: Occurs in 3-5% of bookings; important for financial accuracy and rebooking workflow; not critical for MVP but needed for production operations.

**Independent Test**: Can be tested by creating confirmed booking, not marking patient as arrived, waiting until grace period expires (or manually triggering no-show action), and verifying status transitions to "No-Show" with deposit retained and admin notified.

**Acceptance Scenarios**:

1. **Given** a confirmed booking with procedure date = today, **When** patient does not arrive within 2 hours of scheduled time, **Then** provider can mark booking as "No-Show"
2. **Given** provider marks booking as "No-Show", **When** action confirmed, **Then** booking status changes to "No-Show", deposit retained, admin notified, patient receives rebooking offer
3. **Given** patient marked as no-show, **When** admin reviews, **Then** admin can override no-show status if patient had valid emergency (manual intervention)

---

### User Story 4 - Provider Prescribes Multiple Post-Op Medications (Priority: P1)

After completing treatment, provider prescribes 4 medications (antibiotic, painkiller, anti-inflammatory, topical solution) with different dosages and frequencies. Patient receives complete medication schedule via email and app.

**Why this priority**: Medication prescribing is required for every treatment; must handle multiple medications with varying schedules; critical for patient safety and post-op care.

**Independent Test**: Can be tested by completing treatment documentation, adding 4 medications with different frequencies (1x daily, 2x daily, 3x daily, as needed), saving, and verifying patient receives email with all 4 medications listed with correct dosages and instructions.

**Acceptance Scenarios**:

1. **Given** provider is on post-treatment documentation screen, **When** provider adds first medication with dosage and frequency, **Then** medication appears in list with all details
2. **Given** first medication is added, **When** provider clicks "Add Medication" to add second, **Then** new medication entry form appears below first medication
3. **Given** provider has added 4 medications, **When** provider completes treatment, **Then** patient receives medication schedule via email and in-app notification with all 4 medications clearly listed

---

### User Story 5 - Provider Selects Aftercare Template and Customizes Instructions (Priority: P1)

Provider completes treatment and selects "Standard FUE Aftercare - 12 months" template. Provider adds custom instruction: "Patient has sensitive skin, use extra moisturizer during washing phase". System generates aftercare plan with template milestones + custom instructions.

**Why this priority**: Aftercare template selection is required for every treatment; links treatment phase to aftercare phase; custom instructions allow personalization without rebuilding entire aftercare plan.

**Independent Test**: Can be tested by completing treatment, selecting aftercare template from dropdown, adding custom instructions, completing treatment, and verifying patient's aftercare plan includes both template milestones (automated scans, questionnaires) and custom instructions.

**Acceptance Scenarios**:

1. **Given** provider is on post-treatment documentation screen, **When** provider selects aftercare template "Standard FUE - 12 months", **Then** system displays template summary (duration, milestone count, scan frequency)
2. **Given** template selected, **When** provider adds custom instructions "Use extra moisturizer", **Then** custom instructions saved alongside template selection
3. **Given** treatment completed with template and custom instructions, **When** patient opens aftercare plan in mobile app, **Then** patient sees both automated milestones from template and custom instructions from provider

---

### User Story 6 - Admin Audits Completed Treatment Record (Priority: P2)

Admin receives report of potential issue with treatment. Admin searches for patient by ID, views complete treatment record including all photos, graft counts, medications, and provider notes to verify accuracy and completeness.

**Why this priority**: Admin oversight critical for quality assurance and dispute resolution; not used daily but essential for compliance and patient safety.

**Independent Test**: Can be tested by completing a treatment with full documentation, logging in as admin, searching for patient by ID, and verifying admin can view all treatment details including photos, notes, medications, and audit trail of who documented what and when.

**Acceptance Scenarios**:

1. **Given** admin is on admin platform, **When** admin searches for patient by ID or name, **Then** system displays list of patient's bookings with treatment statuses
2. **Given** admin selects completed treatment, **When** admin opens treatment record, **Then** admin can view all documentation: photos, graft counts, techniques, medications, notes, timestamps
3. **Given** admin is viewing treatment record, **When** admin clicks "View Audit Trail", **Then** system displays chronological log of all documentation actions with provider names and timestamps

---

### Edge Cases

- **What happens when provider uploads 50 photos (exceeds max limit)?** System enforces max limits per photo type: 10 before photos, 20 during photos, 10 after photos. Upload interface disables "Add Photo" button when limit reached; displays message "Maximum [photo type] photos reached".

- **How does system handle provider attempting to mark future appointment as arrived?** "Mark as Arrived" button disabled for bookings with procedure date > today; tooltip displays "Cannot mark future appointments as arrived. Wait until procedure date."

- **What occurs if provider closes browser during treatment documentation without manually saving?** Auto-save mechanism persists all field changes every 2 minutes to server; when provider re-opens treatment record, last auto-saved state restored; provider can continue from where they left off.

- **How to manage two providers attempting to document same treatment simultaneously?** System implements optimistic locking: first provider to save changes succeeds; second provider receives warning "Another user has modified this treatment record. Reload to see latest version?" with option to review changes before overwriting.

- **What happens when media storage service is unavailable during photo upload?** Photos queued locally on provider device with status "Pending Upload"; background process retries upload every 5 minutes; provider sees "Photos uploading..." indicator; treatment completion blocked until all photos successfully uploaded.

- **How does system handle provider forgetting to complete treatment documentation?** System sends reminder notification to provider 12 hours after marking patient as arrived if treatment still "In Progress"; second reminder at 24 hours; admin dashboard flags treatments "In Progress" > 24 hours as "Overdue Documentation" for manual follow-up.

- **What occurs if patient's remaining balance payment fails during treatment completion?** Treatment documentation still completes successfully (treatment status → "Aftercare"); booking flagged as "Pending Final Payment"; admin notified to manually reconcile payment; patient receives email "Payment failed, please update payment method"; provider payout delayed until payment resolved.

- **How to manage provider realizing they selected wrong aftercare template after completing treatment?** Provider cannot edit completed treatment record; provider contacts admin to manually adjust aftercare plan; admin can override aftercare template and regenerate milestones; audit trail logs admin intervention.

---

## Functional Requirements Summary

### Core Requirements

- **FR-001**: System MUST allow providers to mark confirmed bookings as "arrived" when patient checks in at clinic, transitioning status to "In Progress"
- **FR-002**: System MUST validate provider role (Owner, Admin, Doctor) before allowing treatment documentation; Coordinators cannot document treatments
- **FR-003**: System MUST auto-save treatment documentation every 2 minutes during active procedures to prevent data loss
- **FR-004**: System MUST require minimum documentation before allowing treatment completion: surgeon assignment, donor/recipient areas, technique, graft counts, before/after photos (min 3 each), medications (min 1), aftercare template selection
- **FR-005**: System MUST watermark all uploaded treatment photos with anonymized patient ID and timestamp before storing in media storage service
- **FR-006**: System MUST transition booking status from "In Progress" → "Aftercare" upon treatment completion, triggering aftercare plan activation and final payment collection
- **FR-007**: System MUST send real-time status notifications to patient mobile app when treatment starts ("In Progress") and when treatment completes ("Aftercare")
- **FR-008**: System MUST generate and send post-op instruction sheet to patient via email and in-app notification within 5 minutes of treatment completion
- **FR-009**: System MUST activate patient's aftercare plan based on provider-selected template, generating milestones, scan schedules, and questionnaire cadence
- **FR-010**: System MUST enforce treatment documentation completion within 24 hours of marking patient as arrived; send reminder notifications at 12 and 24 hours if incomplete

### Data Requirements

- **FR-011**: System MUST persist all treatment documentation fields with audit trail: graft counts, techniques, donor/recipient areas, photos, medications, notes, timestamps, provider actions
- **FR-012**: System MUST link treatment documentation to original quote details, allowing providers to compare estimated vs. actual graft counts
- **FR-013**: System MUST store treatment photos encrypted at rest (AES-256) with retention period of 7+ years per healthcare compliance regulations
- **FR-014**: System MUST maintain immutable audit log of all treatment documentation actions: who documented, what changed, when changed (timestamp), IP address

### Security & Privacy Requirements

- **FR-015**: System MUST restrict treatment documentation access to provider clinic that owns the booking (no cross-clinic access)
- **FR-016**: System MUST encrypt patient medical data (treatment notes, complications, medications) in transit (TLS 1.3) and at rest (AES-256)
- **FR-017**: System MUST implement role-based access control (RBAC) for treatment documentation: Doctor role required to document, Coordinator role can view only
- **FR-018**: System MUST validate file types on photo uploads (only JPG, PNG allowed) and perform virus scanning before storage
- **FR-019**: System MUST rate-limit photo uploads (max 50 uploads per hour per provider) to prevent abuse or system overload

### Integration Requirements

- **FR-020**: System MUST integrate with S-05 Media Storage Service for secure photo uploads with automatic watermarking, encryption, and retrieval
- **FR-021**: System MUST integrate with S-02 Payment Processing Service to trigger final payment collection upon treatment completion (if deposit-only booking)
- **FR-022**: System MUST integrate with S-03 Notification Service to send status notifications, post-op instructions, and medication schedules to patients
- **FR-023**: System MUST integrate with P-05 Aftercare Module to activate patient's aftercare plan based on provider-selected template at treatment completion
- **FR-024**: System MUST expose RESTful API endpoints for treatment documentation CRUD operations (create treatment record, update progress, upload photos, complete treatment)

---

## Key Entities

- **Entity 1 - Treatment Record**
  - **Key attributes** (conceptual): Booking ID (foreign key), patient ID, provider clinic ID, assigned surgeon ID, additional clinician IDs, procedure start time, procedure end time, total duration, donor areas, recipient areas, techniques used, estimated graft count (from quote), actual graft count, treatment notes, complications flag, status ("In Progress", "Completed"), created timestamp, completed timestamp
  - **Relationships**: One booking has one treatment record; one treatment record belongs to one provider clinic; one treatment record has one assigned surgeon (primary); one treatment record can have multiple additional clinicians; one treatment record has multiple treatment photos

- **Entity 2 - Treatment Photo**
  - **Key attributes**: Treatment record ID (foreign key), photo type ("before", "during", "after"), file URL (encrypted storage path), original file name, file size, upload timestamp, watermark applied (boolean), uploaded by (provider user ID)
  - **Relationships**: One treatment record has many treatment photos; one treatment photo belongs to one treatment record

- **Entity 3 - Medication Prescription**
  - **Key attributes**: Treatment record ID (foreign key), medication name, dosage, frequency, duration, special instructions, prescribed by (provider user ID), prescribed timestamp
  - **Relationships**: One treatment record has many medication prescriptions; one medication prescription belongs to one treatment record

- **Entity 4 - Aftercare Plan**
  - **Key attributes**: Treatment record ID (foreign key), aftercare template ID (foreign key), custom instructions, activation timestamp, plan duration (months), milestone count, scan frequency, questionnaire frequency
  - **Relationships**: One treatment record has one aftercare plan; one aftercare plan references one aftercare template; one aftercare plan belongs to one patient

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-11 | 1.0 | Initial PRD creation for FR-010 Treatment Execution & Documentation | Claude (AI) |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | [Name] | [Date] | [Status] |
| Technical Lead | [Name] | [Date] | [Status] |
| Provider Stakeholder | [Name] | [Date] | [Status] |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-010 from system-prd.md (Lines 682-705)
**Last Updated**: 2025-11-11
