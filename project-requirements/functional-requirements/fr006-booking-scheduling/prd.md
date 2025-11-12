# Product Requirements Document: Booking & Scheduling (FR-006)

**Module**: P-03: Booking & Payment | PR-02: Inquiry & Quote Management | A-01: Patient Management & Oversight
**Feature Branch**: `fr006-booking-scheduling`
**Created**: 2025-11-04
**Status**: ✅ Verified & Approved
**Source**: FR-006 from `system-prd.md`; aligned with Constitution (`constitution-summary.md`, `.specify/memory/constitution.md`); client transcriptions in `transcriptions/`; continuation from FR-004 (Quote Submission) and FR-005 (Quote Comparison & Acceptance); coordinated with FR-007/FR-007B (Payments)

---

## Executive Summary

Enable patients to convert accepted quotes into confirmed procedure bookings by paying deposits. When a patient accepts a quote (FR-005), the appointment slot is automatically confirmed (pre-scheduled by provider during quote creation). No additional slot selection is required. This module operationalizes the handoff from quote acceptance to confirmed booking through payment, enforcing deposit collection, provider calendar blocking, confirmations, and cancellation policy enforcement. The module ensures provider calendar integrity and patient/admin notifications.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-03)**: Booking confirmation flow and payment initiation after quote acceptance.
- **Provider Platform (PR-02)**: Calendar exposure and blocking, booking visibility, reschedule approvals.
- **Admin Platform (A-01/A-05/A-09)**: Oversight, policy configuration, financial reconciliation, notifications governance.
- **Shared Services (S-02/S-03/S-05)**: Payments, notifications, document storage.

### Multi-Tenant Breakdown

**Patient Platform (P-03)**:

- Review accepted quote details with pre-scheduled appointment slot (already confirmed upon quote acceptance - no selection needed).
- Pay deposit or choose installment plan within offered limits; view booking confirmation and itinerary basics.
- View cancellation policy and refund outcomes.

**Provider Platform (PR-02)**:

- View accepted/confirmed bookings in table list format (no calendar view); receive confirmation notifications; enforce check-in workflow on arrival (handoff to FR-010).
- View deposit state and payment status (no card details); apply cancellation policy outcomes.
- Monitor booking status transitions and patient arrival readiness.

**Admin Platform (A-01, A-05, A-09)**:

- Monitor booking pipeline, intervene in disputes, process exceptional modifications under audit.
- Configure global cancellation policy schedule, booking confirmation templates, and notification preferences per constitution limits.
- View financials for deposits/refunds (FR-017) and commission impacts.

**Shared Services (S-02, S-03, S-05)**:

- S-02 Payment Processing: deposits, refunds, installments.
- S-03 Notification Service: confirmations, reminders, reschedule/cancellation notices.
- S-05 Media Storage: stores booking documents (confirmations, invoices) and itinerary files.

### Communication Structure

**In Scope**:

- Email/push confirmations for booking creation, payment receipt, reminders, reschedule outcomes, cancellation outcomes.
- In-app notifications for booking state changes and reminders.

**Out of Scope**:

- Direct patient↔provider chat (handled by FR-012 scope); SMS optionality is handled by S-03 settings.
- Travel booking details (handled by FR-008) beyond minimal itinerary placeholders.

### Entry Points

- Patient-initiated via mobile from the Accepted Quote detail view.
- Activation: Becomes available immediately after FR-005 quote acceptance.
- Confirmation: Occurs after successful deposit (or first installment) per FR-007/FR-007B, which also unmask patient identity and blocks provider calendar.

---

## Business Workflows

### Main Flow: Quote Acceptance → Booking Confirmation

**Actors**: Patient, Provider, Admin, Payment Service, Notification Service
**Trigger**: Patient accepts a quote (FR-005) - appointment slot already pre-scheduled and confirmed by provider during quote creation
**Outcome**: Booking confirmed; deposit paid; provider calendar blocked; confirmations sent

**Steps**:

1. Patient opens Accepted Quote detail view (from FR-005) and reviews quote details including pre-scheduled appointment slot (already confirmed - no selection needed).
2. Patient proceeds directly to payment screen (deposit or installment plan per FR-007B eligibility).
3. System calculates required deposit (admin-configurable percentage, default 20–30% range) and presents cancellation policy.
4. Patient confirms and submits payment.
5. Payment Service authorizes and captures deposit (or schedules installments).
6. System sets booking to Confirmed, unmasking patient identity to provider per constitution.
7. Provider calendar auto-blocks the confirmed slot and displays booking details in provider dashboard.
8. Notification Service sends confirmations to patient and provider; Admin dashboard updates.

### Alternative Flows

**A1: Installment Plan Selected**:

- **Trigger**: Patient chooses an eligible installment plan.
- **Steps**:
  1. System computes max installments based on time until procedure; ensures completion ≥30 days before procedure.
  2. Schedule installment charges and reminders; mark booking Confirmed upon successful initial charge.
- **Outcome**: Booking confirmed; payment schedule tracked; reminders enabled.

**A2: Reschedule Request (Patient-Initiated)** - **DEFERRED TO V2**:

- **Note**: Rescheduling functionality is deferred to V2 pending business validation. The auto-scheduled workflow (provider pre-schedules slots in quote, patient accepts = slot confirmed) reduces the need for rescheduling. If rescheduling is required, it will be handled through admin intervention or future enhancement.
- **Current Behavior**: Once booking is confirmed, date changes require admin intervention or cancellation/rebooking.

**B1: Payment Failure**:

- **Trigger**: Deposit payment fails.
- **Steps**:
  1. System retries payment up to 3 times automatically.
  2. System holds the accepted quote and appointment slot for 48 hours (admin-configurable) to allow patient to retry payment.
  3. During the hold period, the slot remains reserved; patient can retry payment from the Accepted Quote view.
  4. If payment still fails after 48 hours, system releases the slot and moves quote status back to "Quote" (available for acceptance again, but slot may no longer be available if provider has reallocated it).
  5. System notifies both patient and provider of payment failure and slot release.
- **Outcome**: Booking not confirmed; quote remains valid but slot availability is not guaranteed after release; patient may retry if slot still available; provider notified of slot release.

**B2: Cancellation**:

- **Trigger**: Patient or provider requests cancellation.
- **Steps**:
  1. System applies cancellation policy based on timing (see Business Rules section).
  2. Admin review required for exceptions (medical emergencies, provider-initiated cancellations).
  3. Refunds processed per policy schedule.
- **Outcome**: Refunds per policy; status updated to "Cancelled"; audit logged; slot released back to provider calendar.

---

## Screen Specifications

### Patient Platform

#### Screen 1: Payment & Booking Confirmation (Patient)

**Purpose**: Review accepted quote details (continuation from FR-005), view pre-scheduled appointment slot (already confirmed), proceed to payment

**Note**: This screen is accessed directly from FR-005's Accepted Quote detail view. All quote data fields from FR-004 and FR-005 are displayed (read-only) for context.

**Data Fields** (Continuation from FR-005):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Quote Summary | group | Yes | Treatment, packages, pricing (from FR-004/FR-005) | Read-only; from accepted quote |
| Pre-Scheduled Appointment | datetime | Yes | Appointment slot (already confirmed upon quote acceptance) | Read-only; from accepted quote |
| Provider Name | text | Yes | Provider/clinic name | Read-only; from accepted quote |
| Total Amount | number | Yes | Total quote amount | Read-only; from accepted quote |
| Deposit Amount | number | Yes | Calculated deposit (admin-configurable %, default 20-30%) | Within configured bounds |
| Deposit Percentage | text | Yes | Display deposit percentage used | Read-only; for transparency |
| Remaining Balance | number | Yes | Total - Deposit | Calculated automatically |
| Payment Option | select | Yes | Full payment or Installments (2–9 months) | Max installments based on date buffer (FR-007B) |
| Installment Plan | select | Conditional | Number of installments if selected | Only shown if installment option selected |
| Currency | text | Yes | Payment currency | Read-only; from accepted quote |
| Cancellation Policy | text | Yes | Policy summary with refund schedule | Read-only; admin-configured |
| Cancellation Policy Ack | checkbox | Yes | User acknowledges policy | Must be checked before payment |
| Terms & Conditions Ack | checkbox | Yes | User acknowledges T&C | Must be checked before payment |

**Business Rules**:

- All quote details from FR-004/FR-005 are displayed read-only (treatment, packages, pricing, appointment slot).
- Appointment slot is already confirmed (no selection needed) - displayed prominently.
- Deposit amount calculated using admin-configured percentage (default 20-30% range).
- Disable Pay button until all required acknowledgments (cancellation policy, T&C) are checked.
- Show clear breakdown: total amount, deposit amount, remaining balance, currency.
- Display time zone relative labels and local time conversions for appointment slot.
- If installment plan selected, show installment schedule and completion date (must be ≥30 days before procedure).

**Notes**:

- This screen is a continuation of FR-005's Accepted Quote flow.
- Appointment slot cannot be changed here (already confirmed in quote acceptance).
- Link to full cancellation policy document if needed.

---

#### Screen 2: Booking Confirmation & Itinerary (Patient)

**Purpose**: Display confirmed booking, reference number, next steps, basic itinerary

**Data Fields** (Continuation from Screen 1):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Booking Reference | text | Yes | Unique booking reference number | Format per HPID/booking scheme |
| Booking Status | badge | Yes | Confirmed | Must be "Confirmed" |
| Quote Reference | text | Yes | Original quote reference | Read-only; from accepted quote |
| Provider Name | text | Yes | Provider/clinic name | Read-only; from accepted quote |
| Provider Contact | group | Yes | Clinic address, phone, email | Read-only; unmasked after payment |
| Procedure Date | datetime | Yes | Confirmed appointment slot | Read-only; from accepted quote |
| Procedure Time | time | Yes | Appointment start time | Read-only; from accepted quote |
| Treatment Type | text | Yes | Treatment name (FUE, FUT, etc.) | Read-only; from accepted quote |
| Total Amount | number | Yes | Total booking amount | Read-only; from accepted quote |
| Deposit Paid | number | Yes | Deposit amount paid | Read-only; from payment |
| Payment Status | badge | Yes | Deposit paid / Installments scheduled / Full paid | Must reflect latest payment state |
| Remaining Balance | number | Yes | Amount remaining to pay | Calculated automatically |
| Next Payment Due | datetime | Conditional | Next installment due date | Only shown if installments active |
| Payment Method | text | Yes | Payment method used | Read-only; from payment |
| Itinerary Summary | text | Yes | High-level pre-op steps | Read-only; from provider |
| Cancellation Policy | link | Yes | Link to full cancellation policy | Read-only |

**Business Rules**:

- Trigger notifications to patient/provider upon display.
- Display all booking details clearly with appointment slot prominently shown.
- Show payment status and next steps (if installments, show schedule).
- Provide "Add to Calendar" functionality (ICS file download).
- Link to travel booking (FR-008) when available.

**Notes**:

- This screen appears immediately after successful payment.
- All data continues from previous screens (quote, payment).
- Include provider contact information (now unmasked after payment confirmation).

---

### Provider Platform

#### Screen 3: Bookings Dashboard (Provider)

**Purpose**: View accepted and confirmed bookings in table list format; monitor booking status and payment state

**Note**: Provider dashboard uses table list format only (no calendar view). This is consistent with previous FRs (FR-004, FR-005) which use table-based interfaces.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Booking Reference | text | Yes | Unique booking reference | Sortable, filterable |
| Patient Name | text | Yes | Anonymized (e.g., "Mark P. - PAT-00123") or full name if confirmed | Unmask only after payment |
| Patient Code | text | Yes | Patient identifier | Read-only |
| Inquiry Reference | text | Yes | Original inquiry HPID | Link to inquiry details |
| Quote Reference | text | Yes | Original quote reference | Link to quote details |
| Booking Status | badge | Yes | Accepted / Confirmed / In Progress / Cancelled | Filterable by status |
| Appointment Date | datetime | Yes | Pre-scheduled appointment slot | Sortable by date |
| Treatment Type | text | Yes | Treatment name | Filterable |
| Total Amount | number | Yes | Total booking amount | Sortable |
| Deposit Status | badge | Yes | Pending / Paid / Partial | Filterable |
| Deposit Amount | number | Yes | Deposit amount (if paid) | Read-only |
| Payment Status | badge | Yes | Deposit only / Installments / Full paid | Read-only |
| Created Date | datetime | Yes | Booking creation timestamp | Sortable |
| Actions | buttons | Yes | View Details, Check In (if confirmed) | RBAC enforced |

**Business Rules**:

- Table list format only (no calendar view).
- Auto-block appointment slot upon booking confirmation (enforced at database level).
- Patient identity remains masked until booking status is "Confirmed" (payment success).
- Filtering options: Status, Date Range, Treatment Type, Payment Status.
- Sorting options: Date, Amount, Status, Created Date.
- Clicking on booking row opens booking detail view (Screen 4).
- System prevents overlapping appointments (enforced at booking confirmation - if two patients accept quotes with overlapping slots, first payment confirmation wins; second booking attempt will fail with conflict error).

**Notes**:

- Consistent with provider interface patterns from FR-004 and FR-005.
- Show payment summary figures without revealing card details.
- Appointment slot blocking is automatic and enforced - no manual calendar management needed.

---

#### Screen 4: Booking Detail View (Provider)

**Purpose**: View complete booking details with full context from inquiry, quote, acceptance, and booking stages

**Data Fields** (Continuation from Screen 3, aggregating data from FR-003, FR-004, FR-005, FR-006):

**Section 1: Booking & Scheduling Information** (from FR-006):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Booking Reference | text | Yes | Unique booking reference | Read-only |
| Booking Status | badge | Yes | Current status (Accepted/Confirmed/In Progress/Cancelled) | Read-only |
| Booking Created Date | datetime | Yes | Booking creation timestamp | Read-only |
| Appointment Date | datetime | Yes | Confirmed appointment slot (pre-scheduled in quote) | Read-only |
| Appointment Time | time | Yes | Appointment start time | Read-only |
| Appointment Duration | text | Yes | Estimated procedure duration | Read-only; from quote |

**Section 2: Patient Information** (from FR-003, unmasked if Confirmed):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Patient Anonymized ID | text | Yes | Patient code (always visible) | Read-only |
| Patient Name | text | Conditional | Full name (if Confirmed) or masked (e.g., "Mark P. - PAT-00123") | Unmask only if status = Confirmed |
| Patient Email | text | Conditional | Email address (if Confirmed) | Unmask only if status = Confirmed |
| Patient Phone | text | Conditional | Phone number (if Confirmed) | Unmask only if status = Confirmed |
| Patient Location | text | Yes | Country/city | Read-only; from inquiry |
| Patient Age | number | Yes | Patient age | Read-only; from inquiry |
| Patient Gender | text | Yes | Gender | Read-only; from inquiry |

**Section 3: Problem & Concern Information** (from FR-003):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Treatment Type Requested | text | Yes | Hair/Beard/Both | Read-only; from inquiry |
| Problem/Concern Description | text | Yes | Patient's hair concern description | Read-only; from inquiry |
| Duration of Concern | text | Yes | How long patient has had the concern | Read-only; from inquiry |
| Previous Treatments | text | No | Previous treatments tried | Read-only; from inquiry |
| Symptom Severity | number | Yes | Severity rating (1-10) | Read-only; from inquiry |
| Lifestyle Factors | text | No | Relevant lifestyle information | Read-only; from inquiry |
| Additional Notes | text | No | Patient's additional notes | Read-only; from inquiry |
| Media Files | links | No | Photos/videos uploaded by patient | Read-only; from inquiry |
| 3D Scan | link/viewer | Yes | Link to patient 3D scan with viewer | Read-only; from inquiry |

**Section 4: Medical Information** (from FR-003):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Medical Alerts | chips | Yes | Patient medical risk flags (Critical/Standard/None) | Read-only; color-coded |
| Medical Questionnaire | link | Yes | Link to full medical questionnaire responses | Read-only; from inquiry |
| Allergies | text | No | Known allergies | Read-only; from questionnaire |
| Current Medications | text | No | Current medications | Read-only; from questionnaire |
| Chronic Conditions | text | No | Chronic health conditions | Read-only; from questionnaire |

**Section 5: Quote Information** (from FR-004):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Quote Reference | text | Yes | Original quote reference | Read-only; link to quote |
| Quote Created Date | datetime | Yes | Quote creation date | Read-only |
| Quote Accepted Date | datetime | Yes | Quote acceptance date | Read-only; from FR-005 |
| Treatment Type | text | Yes | Selected treatment (FUE, FUT, DHI, etc.) | Read-only; from quote |
| Estimated Graft Count | number | Yes | Estimated number of grafts | Read-only; from quote |
| Technique Specifications | text | No | Technique details | Read-only; from quote |
| Packages Selected | list | No | Hotel, transport, medication packages | Read-only; from quote |
| Clinician Assigned | text | Yes | Clinician who will perform procedure | Read-only; from quote |
| Provider Notes | text | No | Provider's notes to patient | Read-only; from quote |
| Treatment Plan (per-day) | table | Yes | Day-by-day treatment plan | Read-only; from quote |

**Section 6: Pricing & Payment Information** (from FR-004, FR-006, FR-007):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Currency | text | Yes | Payment currency | Read-only; from quote |
| Treatment Price | number | Yes | Base treatment price | Read-only; from quote |
| Package Prices | number | Yes | Total package prices | Read-only; from quote |
| Discount Applied | number | No | Discount amount (if any) | Read-only; from quote |
| Total Quote Amount | number | Yes | Total quote amount | Read-only; from quote |
| Deposit Percentage | text | Yes | Deposit percentage used | Read-only; admin-configured |
| Deposit Amount | number | Yes | Deposit amount required/paid | Read-only |
| Deposit Status | badge | Yes | Pending/Paid/Partial | Read-only |
| Deposit Paid Date | datetime | Conditional | Date deposit was paid | Read-only; if paid |
| Payment Method | text | Conditional | Payment method used | Read-only; if paid |
| Payment Status | badge | Yes | Deposit only / Installments / Full paid | Read-only |
| Payment Schedule | table | Conditional | Installment schedule (if applicable) | Only shown if installments |
| Remaining Balance | number | Yes | Amount remaining to pay | Calculated |
| Final Payment Due Date | datetime | Conditional | Final payment due date | Read-only; if applicable |

**Section 7: Inquiry Context** (from FR-003):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Inquiry Reference | text | Yes | Original inquiry HPID | Read-only; link to inquiry |
| Requested Countries | list | Yes | Countries patient selected for treatment | Read-only; from inquiry |
| Requested Date Ranges | list | Yes | All date ranges patient requested | Read-only; from inquiry |
| Budget Range | text | No | Patient's budget range | Read-only; from inquiry |

**Actions**:

| Action | Type | Condition | Description |
|--------|------|-----------|-------------|
| Check In | button | Status = Confirmed, Appointment date = today or past | Mark patient as arrived (handoff to FR-010) |
| View Inquiry | link | Always | Open full inquiry details (FR-003) |
| View Quote | link | Always | Open full quote details (FR-004) |
| View 3D Scan | link | Always | Open 3D scan viewer |
| View Medical Questionnaire | link | Always | Open medical questionnaire |

**Business Rules**:

- Patient full identity only visible if booking status is "Confirmed" (payment successful).
- All booking data is read-only (cannot be edited by provider).
- Check In button only available if status is "Confirmed" and appointment date is today or past.
- All sections display data from previous stages (inquiry → quote → acceptance → booking) in chronological order.
- Links to original inquiry and quote provide full context and audit trail.

**Notes**:

- This screen aggregates all information from the patient journey (inquiry through booking).
- UI may use tabs or accordion sections to organize information by stage.
- Payment details shown without card information.
- All data is read-only to maintain data integrity and audit trail.

---

### Admin Platform

#### Screen 5: Bookings Management Dashboard (Admin)

**Purpose**: Monitor all bookings across platform, intervene in disputes, process cancellations, configure policies

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Booking Reference | text | Yes | Unique booking reference | Sortable, filterable, searchable |
| Patient Name | text | Yes | Full patient name | Searchable |
| Patient Email | text | Yes | Patient email | Searchable |
| Provider Name | text | Yes | Provider/clinic name | Filterable |
| Booking Status | badge | Yes | Accepted / Confirmed / In Progress / Cancelled / Completed | Filterable |
| Appointment Date | datetime | Yes | Appointment slot | Sortable, filterable by date range |
| Treatment Type | text | Yes | Treatment name | Filterable |
| Total Amount | number | Yes | Total booking amount | Sortable |
| Deposit Status | badge | Yes | Pending / Paid / Partial | Filterable |
| Payment Status | badge | Yes | Deposit only / Installments / Full paid | Filterable |
| Created Date | datetime | Yes | Booking creation timestamp | Sortable |
| Actions | buttons | Yes | View Details, Edit (emergency), Cancel, Process Refund | RBAC enforced |

**Business Rules**:

- Full access to all booking data across all providers and patients.
- Search functionality: by booking reference, patient name, patient email, provider name.
- Filtering: Status, Provider, Date Range, Treatment Type, Payment Status.
- Admin can manually intervene in bookings (emergency modifications) with audit trail.
- Admin can process cancellations and refunds per policy.
- All admin actions require audit logging with reason/justification.

**Notes**:

- Admin has full visibility and override capabilities for dispute resolution.
- All actions are audited for compliance.

---

#### Screen 6: Booking Detail & Intervention (Admin)

**Purpose**: View complete booking details with full context from all stages, and perform administrative actions

**Data Fields** (Continuation from Screen 5, aggregating data from FR-003, FR-004, FR-005, FR-006):

**Section 1: Booking & Scheduling Information** (from FR-006):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Booking Reference | text | Yes | Unique booking reference | Read-only |
| Booking Status | badge | Yes | Current status | Editable by admin (with reason) |
| Booking Created Date | datetime | Yes | Booking creation timestamp | Read-only |
| Appointment Date | datetime | Yes | Appointment slot | Editable by admin (with reason) |
| Appointment Time | time | Yes | Appointment start time | Editable by admin (with reason) |
| Appointment Duration | text | Yes | Estimated procedure duration | Read-only; from quote |

**Section 2: Patient Information** (from FR-003, always visible to admin):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Patient ID | text | Yes | Patient code | Read-only |
| Patient Name | text | Yes | Full name | Read-only |
| Patient Email | text | Yes | Email address | Read-only |
| Patient Phone | text | Yes | Phone number | Read-only |
| Patient Address | text | No | Full address | Read-only; from profile |
| Patient Location | text | Yes | Country/city | Read-only; from inquiry |
| Patient Age | number | Yes | Patient age | Read-only; from inquiry |
| Patient Gender | text | Yes | Gender | Read-only; from inquiry |
| Patient Date of Birth | date | Yes | Date of birth | Read-only; from profile |

**Section 3: Problem & Concern Information** (from FR-003):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Treatment Type Requested | text | Yes | Hair/Beard/Both | Read-only; from inquiry |
| Problem/Concern Description | text | Yes | Patient's hair concern description | Read-only; from inquiry |
| Duration of Concern | text | Yes | How long patient has had the concern | Read-only; from inquiry |
| Previous Treatments | text | No | Previous treatments tried | Read-only; from inquiry |
| Symptom Severity | number | Yes | Severity rating (1-10) | Read-only; from inquiry |
| Lifestyle Factors | text | No | Relevant lifestyle information | Read-only; from inquiry |
| Additional Notes | text | No | Patient's additional notes | Read-only; from inquiry |
| Media Files | links | No | Photos/videos uploaded by patient | Read-only; from inquiry |
| 3D Scan | link/viewer | Yes | Link to patient 3D scan with viewer | Read-only; from inquiry |

**Section 4: Medical Information** (from FR-003):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Medical Alerts | chips | Yes | Patient medical risk flags (Critical/Standard/None) | Read-only; color-coded |
| Medical Questionnaire | link | Yes | Link to full medical questionnaire responses | Read-only; from inquiry |
| Allergies | text | No | Known allergies | Read-only; from questionnaire |
| Current Medications | text | No | Current medications | Read-only; from questionnaire |
| Chronic Conditions | text | No | Chronic health conditions | Read-only; from questionnaire |
| Previous Surgeries | text | No | Previous surgical procedures | Read-only; from questionnaire |

**Section 5: Quote Information** (from FR-004):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Quote Reference | text | Yes | Original quote reference | Read-only; link to quote |
| Quote Created Date | datetime | Yes | Quote creation date | Read-only |
| Quote Accepted Date | datetime | Yes | Quote acceptance date | Read-only; from FR-005 |
| Treatment Type | text | Yes | Selected treatment (FUE, FUT, DHI, etc.) | Read-only; from quote |
| Estimated Graft Count | number | Yes | Estimated number of grafts | Read-only; from quote |
| Technique Specifications | text | No | Technique details | Read-only; from quote |
| Packages Selected | list | No | Hotel, transport, medication packages | Read-only; from quote |
| Clinician Assigned | text | Yes | Clinician who will perform procedure | Read-only; from quote |
| Provider Notes | text | No | Provider's notes to patient | Read-only; from quote |
| Treatment Plan (per-day) | table | Yes | Day-by-day treatment plan | Read-only; from quote |

**Section 6: Provider Information** (from provider profile):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Provider Name | text | Yes | Provider/clinic name | Read-only |
| Provider Contact | text | Yes | Clinic contact information | Read-only |
| Provider Address | text | Yes | Clinic address | Read-only |
| Provider Email | text | Yes | Provider email | Read-only |
| Provider Phone | text | Yes | Provider phone | Read-only |

**Section 7: Pricing & Payment Information** (from FR-004, FR-006, FR-007):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Currency | text | Yes | Payment currency | Read-only; from quote |
| Treatment Price | number | Yes | Base treatment price | Read-only; from quote |
| Package Prices | number | Yes | Total package prices | Read-only; from quote |
| Discount Applied | number | No | Discount amount (if any) | Read-only; from quote |
| Total Quote Amount | number | Yes | Total quote amount | Read-only; from quote |
| Deposit Percentage | text | Yes | Deposit percentage used | Read-only; admin-configured |
| Deposit Amount | number | Yes | Deposit amount required/paid | Read-only |
| Deposit Status | badge | Yes | Pending/Paid/Partial | Read-only |
| Payment History | table | Yes | All payments (deposit, installments, final) with dates, amounts, methods | Read-only |
| Payment Status | badge | Yes | Deposit only / Installments / Full paid | Read-only |
| Payment Schedule | table | Conditional | Installment schedule (if applicable) | Only shown if installments |
| Remaining Balance | number | Yes | Amount remaining to pay | Calculated |
| Final Payment Due Date | datetime | Conditional | Final payment due date | Read-only; if applicable |
| Refund History | table | Yes | All refunds processed with dates, amounts, reasons | Read-only |

**Section 8: Inquiry Context** (from FR-003):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Inquiry Reference | text | Yes | Original inquiry HPID | Read-only; link to inquiry |
| Requested Countries | list | Yes | Countries patient selected for treatment | Read-only; from inquiry |
| Requested Date Ranges | list | Yes | All date ranges patient requested | Read-only; from inquiry |
| Budget Range | text | No | Patient's budget range | Read-only; from inquiry |

**Section 9: Audit & History**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Audit Log | table | Yes | All status changes and admin actions with timestamps, users, reasons | Read-only; immutable |
| Status History | timeline | Yes | Chronological status changes | Read-only |
| Internal Notes | table | Yes | Admin internal notes (not visible to patient/provider) | Editable by admin |
| Version History | table | Yes | Quote version history (if quote was edited) | Read-only |

**Intervention Actions**:

| Action | Type | Condition | Description |
|--------|------|-----------|-------------|
| Modify Status | button | Always | Change booking status (requires reason) |
| Modify Appointment Date | button | Always | Change appointment date/time (requires reason) |
| Process Refund | button | Booking cancelled or eligible | Process refund per cancellation policy |
| Cancel Booking | button | Always | Cancel booking (requires reason) |
| Add Internal Note | button | Always | Add admin-only note |
| View Inquiry | link | Always | Open full inquiry details (FR-003) |
| View Quote | link | Always | Open full quote details (FR-004) |
| View 3D Scan | link | Always | Open 3D scan viewer |
| View Medical Questionnaire | link | Always | Open medical questionnaire |

**Business Rules**:

- Admin has full visibility to all patient and provider information (no masking).
- Admin can modify booking status and appointment date (emergency cases only) with required reason/justification.
- All modifications are logged in audit trail with who/when/what/why.
- Admin can process refunds per cancellation policy.
- Admin can add internal notes to booking (not visible to patient/provider).
- All sections display data from previous stages (inquiry → quote → acceptance → booking) in chronological order.
- Links to original inquiry and quote provide full context and audit trail.

**Notes**:

- This screen aggregates all information from the complete patient journey (inquiry through booking).
- UI may use tabs or accordion sections to organize information by stage.
- Full administrative access for dispute resolution and exceptional cases.
- All actions require justification and are fully audited.
- Payment details shown without card information (PCI compliance).

---

## Business Rules

### General Module Rules

- Booking is confirmed only after successful deposit or first installment charge.
- Appointment slot is automatically confirmed when patient accepts quote (pre-scheduled by provider during quote creation) - no additional slot selection needed.
- Provider calendars must be accurate; confirmed bookings auto-block times at database level; overlapping appointments are prevented.
- All timestamps shown in patient's local timezone; provider view shows both local and clinic time.
- **Overlapping Appointment Prevention**: If two patients accept quotes with overlapping appointment slots, the first patient to complete payment confirmation wins. The second booking attempt will fail with a conflict error, and the quote status will revert to "Quote" (available for acceptance again, but slot may no longer be available). System enforces this at booking confirmation time with atomic transaction checks.

### Data & Privacy Rules

- Patient identity remains masked to provider until booking is Confirmed (payment success).
- Booking, payment, and personal data are encrypted at rest and in transit; audit logs are immutable.
- Retain booking and financial records ≥7 years; hard deletes prohibited (soft-delete/archive only).

### Admin Editability Rules

**Editable by Admin** (via A-09: System Settings & Configuration):

- **Deposit Rate**: Admin MUST be able to configure deposit percentage (default range: 20-30% of total booking amount) via **FR-029: Payment System Configuration**. This is configurable per provider or globally. Changes apply to new bookings only (existing bookings retain original deposit rate).
- Cancellation policy schedule (thresholds and refund percentages).
- Payment failure hold duration (default: 48 hours) - how long to hold accepted quote and slot after payment failure.
- Notification templates for booking confirmations/reminders; booking confirmation content.
- Commission settings.

**Fixed in Codebase (Not Editable)**:

- Password policy and OTP length; identity unmasking rule tied to payment confirmation.
- Audit logging enablement and retention guarantees.
- Overlapping appointment prevention logic (enforced at database level).

**Configurable with Restrictions**:

- Payment options availability per region/currency (cannot alter gateway compliance requirements).

### Payment & Billing Rules

- **Deposit Rate**: Deposit percentage is admin-configurable (default: 20-30% of total). Admin can set different rates per provider or use global default. Deposit amount is calculated at booking creation time and locked.
- Deposit required to confirm booking; final payment per FR-007 schedule.
- Installments must complete ≥30 days before procedure; failures trigger retries, then flag for admin.
- **Post-Acceptance Hold**: After quote acceptance, the system holds the reserved appointment slot for 48 hours to allow the patient to complete initial payment (deposit or first installment). If no payment is completed within 48 hours, the reservation is released and the slot becomes available again.
- **Payment Failure Handling**:
  - If deposit payment fails, system retries up to 3 times automatically.
  - Accepted quote and appointment slot are held for 48 hours (admin-configurable) to allow patient to retry payment.
  - During hold period, slot remains reserved; patient can retry payment from Accepted Quote view.
  - If payment still fails after hold period, slot is released and quote status reverts to "Quote" (available for acceptance again, but slot availability not guaranteed).
  - Quote remains valid but slot may no longer be available if provider has reallocated it.
- Refunds per cancellation policy example in `system-prd.md`; provider cancellations require admin approval and full refund.
- Prices shown in patient's currency; exchange rate locked at quote acceptance; payouts per locked rate.

### Rescheduling Rules

- **Rescheduling is deferred to V2**: The auto-scheduled workflow (provider pre-schedules slots in quote, patient accepts = slot confirmed) reduces the need for rescheduling. Rescheduling functionality will be evaluated for V2 based on business needs.
- **Current Behavior**: Once booking is confirmed, date changes require admin intervention or cancellation/rebooking per cancellation policy.

---

## Success Criteria

### Patient Experience Metrics

- **SC-001**: Patients can confirm a booking in ≤3 minutes from accepted quote.
- **SC-002**: 90% of patients complete deposit on first attempt.
- **SC-003**: Booking confirmation and receipts delivered within 1 minute of payment.

### Provider Efficiency Metrics

- **SC-004**: Calendar auto-block occurs within 10 seconds of booking confirmation.
- **SC-005**: 0% double-bookings due to system-enforced conflicts.
- **SC-006**: 0% overlapping appointments due to system-enforced conflict prevention.

### Admin Management Metrics

- **SC-007**: 100% of booking lifecycle events are auditable with user/timestamp.
- **SC-008**: Support tickets related to scheduling decrease by 30% within 2 months of launch.
- **SC-009**: Refund processing SLA ≤ 3 business days for eligible cases.

### System Performance Metrics

- **SC-010**: Booking creation completes in <2 seconds p95 (excluding external payment time).
- **SC-011**: Supports 1,000 concurrent booking attempts without degradation.
- **SC-012**: 99.5%+ uptime for booking flows.
- **SC-013**: Zero lost confirmed bookings.

### Business Impact Metrics

- **SC-014**: 85% of accepted quotes convert to confirmed bookings (aligned with system targets).
- **SC-015**: Deposit capture rate ≥ 80% within 24 hours of quote acceptance.
- **SC-016**: Refund disputes < 2% of total bookings.

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **FR-001 / Module P-01**: Auth & Profile; required for authenticated patient actions and identity unmasking post-payment.
  - **Integration point**: Booking flow requires verified patient and profile data.
- **FR-004 / Module PR-02**: Quote Submission; provides pre-scheduled slots and quote breakdown.
- **FR-005 / Module P-02**: Quote Comparison & Acceptance; triggers booking entry point (appointment slot already confirmed upon quote acceptance).
- **FR-007 & FR-007B / Modules P-03, S-02**: Payments and Installments; deposit capture, schedules, refunds.
- **FR-020 / S-03**: Notifications; confirmations, reminders, and alerts.
- **FR-010 / PR-03**: Post-confirmation treatment execution starts on arrival.
- **FR-026 / Module A-09**: System Settings & Configuration; deposit rate configuration, payment failure hold duration configuration.
- **FR-029 / Module A-09**: Payment System Configuration; deposit rate configuration is managed here (admin-configurable percentage, default 20-30% range, per-provider or global settings).

### External Dependencies (APIs, Services)

- Payment processor for deposits/installments/refunds (PCI compliant); retry with backoff, hold booking for 48 hours on failure.
- Calendar/ICS generation for add-to-calendar links.

### Data Dependencies

- Active provider calendars with pre-scheduled slots from quotes (PR-02).
- Accepted quote with itemized pricing, currency, and discount applications (FR-004/019).
- Patient verified profile and medical status flags (P-01/P-02) for provider readiness.

---

## Assumptions

### User Behavior Assumptions

- Patients act within 24–72 hours after quote acceptance to book.
- Patients understand and accept cancellation terms before paying.
- Majority use mobile; need clear time zone handling.

### Technology Assumptions

- Patient devices support secure payments and push notifications.
- Provider/admin access via modern browsers; stable connectivity expected at clinics.
- Notification service can deliver emails/push near real-time.

### Business Process Assumptions

- Providers maintain accurate calendars and honor confirmed slots.
- Admins process edge-case cancellations within published SLAs.
- Discounts/commissions already resolved before booking stage.

---

## Implementation Notes

### Technical Considerations

- Idempotent booking creation with slot holds to prevent race conditions; atomic confirm on payment success.
- Calendar conflict detection and prevention; status transitions auditable.
- Resilient to payment gateway latency; clear user states during processing.

### Integration Points

- Patient app to booking API for slot selection and payment initiation.
  - Data: accepted quote ID, slot ID, payment choice, acknowledgments.
  - Auth: patient token; RBAC enforcing ownership.
  - Errors: validation feedback; recoverable payment failures.
- Provider calendar API for blocking/unblocking; admin oversight API for audit and dispute actions.

### Scalability Considerations

- Expect hundreds of concurrent bookings during campaigns; ensure slot-hold locking performs under load.
- Background jobs for reminders and installment schedules; horizontal scaling for booking endpoints.

### Security Considerations

- MFA enforced for provider/admin tenants; RBAC everywhere.
- TLS 1.3 in transit; AES-256 at rest; no storage of card PANs; webhook signature verification.
- Full audit trail on state changes and access; rate limiting and anti-abuse protections on booking/payment endpoints.

---

## User Scenarios & Testing

### User Story 1 - Confirm Booking with Deposit (Priority: P1)

Patient confirms a booking from an accepted quote by selecting a pre-scheduled slot and paying the deposit.

**Why this priority**: Core conversion event from interest to revenue.

**Independent Test**: Accept a quote, select slot, pay deposit, verify confirmation, calendar block, and notifications.

**Acceptance Scenarios**:

1. Given an accepted quote with valid slots, When patient pays deposit, Then booking status is Confirmed and provider sees unmasked identity.
2. Given a confirmed booking, When confirmation is generated, Then both parties receive it within 1 minute.
3. Given confirmation, When viewing provider calendar, Then slot is blocked and non-overlapping.

---

### User Story 2 - Payment Failure Handling (Priority: P1)

Patient's deposit payment fails; system holds slot for retry period; patient successfully retries payment.

**Why this priority**: Critical for conversion and user experience.

**Independent Test**: Simulate payment failure, verify hold period, retry payment, confirm booking.

**Acceptance Scenarios**:

1. Given an accepted quote with payment failure, When system holds slot for 48 hours, Then patient can retry payment and booking confirms successfully.
2. Given payment failure after hold period expires, When slot is released, Then quote status reverts to "Quote" and provider is notified.

---

### User Story 3 - Overlapping Appointment Prevention (Priority: P1)

Two patients accept quotes with overlapping appointment slots; first payment confirmation wins; second attempt fails gracefully.

**Why this priority**: Prevents double-booking and ensures calendar integrity.

**Independent Test**: Two patients accept quotes with overlapping slots, first completes payment, second attempts payment, verify conflict handling.

**Acceptance Scenarios**:

1. Given two accepted quotes with overlapping slots, When first patient completes payment, Then booking confirms and slot is blocked.
2. Given overlapping slot conflict, When second patient attempts payment, Then booking fails with conflict error and quote status reverts.

---

### User Story 4 - Apply Cancellation Policy (Priority: P2)

Late cancellation applies refund schedule; provider cancellation triggers full refund and admin approval flow.

**Why this priority**: Protects trust and platform economics.

**Independent Test**: Trigger patient late cancellation and provider cancellation; verify refund outcomes and audit logs.

**Acceptance Scenarios**:

1. Given a confirmed booking, When patient cancels <15 days prior, Then refund is computed per policy and logged.
2. Given a confirmed booking, When provider cancels with admin approval, Then patient receives full refund immediately and provider penalty tracked.

### Edge Cases

- Payment succeeds but confirmation email fails: confirmation must still be visible in-app; retry email.
- Simultaneous payment attempts for overlapping slots: enforce atomic transaction checks; first payment confirmation wins; second fails with conflict error.
- Installment plan default before deadline: flag booking, notify admin and patient; apply policy.
- Provider emergency closure: admin-approved cancellation, full refund, suggest alternatives.
- Payment failure after quote acceptance: hold slot for configurable duration (default 48 hours); allow retry; release slot if payment not completed.
- Two patients accept quotes with same slot simultaneously: first to complete payment wins; second booking attempt fails with clear error message.

---

## Functional Requirements Summary

### Core Requirements

- **FR-006.1**: Patients MUST be able to proceed to payment after accepting a quote (appointment slot already pre-scheduled and confirmed by provider during quote creation - no slot selection needed).
- **FR-006.2**: System MUST confirm booking only after successful deposit/initial installment and unmask patient identity to provider.
- **FR-006.3**: System MUST auto-block provider calendar for confirmed bookings and prevent overlapping appointments (first payment confirmation wins; second attempt fails with conflict error).
- **FR-006.4**: System MUST enforce cancellation policy with scheduled refunds per policy (rescheduling deferred to V2).
- **FR-006.5**: System MUST hold accepted quote and appointment slot for configurable duration (default 48 hours) after payment failure to allow retry.

### Data Requirements

- **FR-006.6**: System MUST store booking reference, slot, status history, payment state, refund state, and audit trail ≥7 years.
- **FR-006.7**: System MUST link bookings to accepted quotes, treatments, packages, and provider calendars.

### Security & Privacy Requirements

- **FR-006.8**: System MUST keep patient identity masked until payment confirmation; encrypt PII at rest and in transit.
- **FR-006.9**: System MUST log all booking state changes and accesses with user, timestamp, and reason.

### Integration Requirements

- **FR-006.10**: System MUST integrate with Payment Service for deposits, installments, refunds, and lock exchange rate.
- **FR-006.11**: System MUST integrate with Notification Service for confirmations, reminders, and policy notices.

### Configuration Requirements

- **FR-006.12**: Admin MUST be able to configure deposit percentage (default: 20-30% range) via **FR-029: Payment System Configuration** (Module A-09: System Settings & Configuration).
- **FR-006.13**: Admin MUST be able to configure payment failure hold duration (default: 48 hours) via A-09: System Settings & Configuration.

### Marking Unclear Requirements

None.

---

## Key Entities

- **Entity 1 - Booking**: Represents a confirmed or pending booking derived from an accepted quote.
  - **Key attributes**: booking reference, quote ID, provider ID, patient ID, slot, status, payment state, refund state.
  - **Relationships**: One booking links to one accepted quote; one provider calendar entry; one patient.

- **Entity 2 - Calendar Slot**: Represents a provider’s pre-scheduled appointment time.
  - **Key attributes**: provider ID, start/end, capacity, hold/blocked flags, expiration.
  - **Relationships**: One slot can be held or blocked by at most one booking.

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-04 | 1.0 | Initial PRD creation | AI |
| 2025-11-04 | 1.1 | Major revisions: Removed slot selection step (slot auto-confirmed on quote acceptance); Added deposit rate management (admin-configurable); Deferred rescheduling to V2; Defined payment failure handling (48-hour hold); Added all 3 tenant screen specifications with data continuity; Updated provider dashboard to table-only format; Added overlapping appointment prevention logic | AI |
| 2025-11-04 | 1.2 | Enhanced booking detail screens: Added comprehensive data from all previous stages (FR-003 inquiry, FR-004 quote, FR-005 acceptance) to provider and admin booking detail screens; Clarified deposit rate management is handled in FR-029: Payment System Configuration | AI |
| 2025-11-12 | 1.3 | Status updated to Verified & Approved; All approvals completed | Product Team |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner |  | 2025-11-12 | ✅ Approved |
| Technical Lead |  | 2025-11-12 | ✅ Approved |
| Stakeholder |  | 2025-11-12 | ✅ Approved |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-011 Aftercare & Recovery Management PRD
**Last Updated**: 2025-11-12
