# FR-006 - Booking & Scheduling

**Module**: P-03: Booking & Payment | PR-02: Inquiry & Quote Management | A-01: Patient Management & Oversight
**Feature Branch**: `fr006-booking-scheduling`
**Created**: 2025-11-04
**Status**: 🟡 Revised — Pending Consolidated Verification
**Source**: FR-006 from `system-prd.md`; SRC-MTG-002 and CR-FR006-20260915-01; continuation from FR-004 (Quote Submission) and FR-005 v2.3 (Subquote Comparison & Acceptance); coordinated with FR-007/FR-007B (Payments)

---

## Executive Summary

Enable patients to convert one accepted subquote into a confirmed procedure booking by paying a deposit or first installment. FR-006 consumes FR-005's immutable acceptance snapshot: the selected package, date range, appointment, price, and promotion from the subquote plus inherited parent quote/provider/treatment context. `acceptedSubquoteVersion` equals `acceptedParentQuoteVersion` because both identify the same FR-004 parent aggregate revision. No commercial or appointment reselection is permitted. This module operationalizes that handoff through payment, provider calendar blocking, confirmations, and cancellation policy enforcement while preserving the exact accepted selection.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-03)**: Booking confirmation flow and payment initiation from an accepted subquote.
- **Provider Platform (PR-02)**: Calendar exposure and blocking, booking visibility, reschedule approvals.
- **Admin Platform (A-01/A-05/A-09)**: Oversight, policy configuration, financial reconciliation, notifications governance.
- **Shared Services (S-02/S-03/S-05)**: Payments, notifications, document storage.

### Multi-Tenant Breakdown

**Patient Platform (P-03)**:

- Review the accepted subquote and inherited parent context with its pre-scheduled appointment slot; no package, date, appointment, or price selection is available.
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

- Direct patient↔provider chat (handled by FR-012 scope); SMS optionality is handled by S-03 settings and **does not exist in MVP (no SMS booking notifications are sent until a future phase explicitly enables SMS in S-03/FR-020/FR-030)**.
- Travel booking details (handled by FR-008) beyond minimal itinerary placeholders.

### Entry Points

- Patient-initiated via mobile from the Accepted Subquote detail view.
- Activation: Becomes available immediately after FR-005 subquote acceptance.
- Confirmation: Occurs after successful deposit (or first installment) per FR-007/FR-007B, which also unmask patient identity and blocks provider calendar.

---

## Business Workflows

### Main Flow: Subquote Acceptance → Booking Confirmation

**Actors**: Patient, Provider, Admin, Payment Service, Notification Service
**Trigger**: Patient accepts one subquote in FR-005; its appointment slot was pre-scheduled on the resolved FR-004 Option/date-price record
**Outcome**: Booking confirmed; deposit paid; provider calendar blocked; confirmations sent

**Pre-Booking Validation**: Before entering the booking/payment flow, system MUST verify:

- The parent inquiry is NOT in "Cancelled" status (FR-003 Workflow 5). If cancelled, system blocks entry with message: "This inquiry has been cancelled. Booking is no longer available."
- The accepted subquote and parent quote are still in "Accepted" status, their versions match the FR-005 AcceptanceEvent, and the AcceptanceEvent owns the slot's valid exclusive payment-window hold.

**Steps**:

1. Patient opens the Accepted Subquote detail view and reviews the immutable accepted selection and inherited parent context; no commercial or appointment field can be reselected.
2. Patient proceeds directly to payment screen (deposit or installment plan per FR-029 split payment configuration and FR-007B eligibility).
3. System queries FR-029 payment settings and calculates required deposit (admin-configurable percentage, default 20–30% range) and presents cancellation policy.
4. Patient confirms and submits payment.
5. Payment Service authorizes and captures deposit (or schedules installments).
6. System sets booking to Confirmed, unmasking patient identity to provider per constitution.
7. Provider calendar auto-blocks the confirmed slot and displays booking details in provider dashboard.
8. Notification Service sends confirmations to patient and provider; Admin dashboard updates.

### Alternative Flows

**A1: Installment Plan Selected**:

- **Trigger**: Patient chooses an eligible installment plan.
- **Steps**:
  1. System determines feasible installment options based on FR-029 split payment settings (enabled installment counts, cutoff days, minimum booking amount) and procedure date constraints (completion ≥30 days before procedure).
  2. Schedule installment charges and reminders per FR-007B; mark booking Confirmed upon successful initial charge.
- **Outcome**: Booking confirmed; payment schedule tracked; reminders enabled.

**A2: Reschedule Request (Patient-Initiated)** - **DEFERRED TO V2**:

- **Note**: Rescheduling functionality is deferred to V2 pending business validation. The provider pre-schedules the appointment in the subquote; acceptance fixes that appointment choice and reserves its slot for the payment window, while successful payment confirms the booking. If a date change is required, it is handled through admin intervention or a future enhancement.
- **Current Behavior**: Once booking is confirmed, date changes require admin intervention or cancellation/rebooking.

**B1: Payment Failure**:

- **Trigger**: Deposit payment fails.
- **Steps**:
  1. Payment Service applies retry policy per **FR-007 (exponential backoff with idempotency)**.
  2. System holds the accepted subquote's appointment slot for 48 hours (admin-configurable) to allow patient to retry payment.
  3. During the hold period, the slot remains reserved; patient can retry payment from the Accepted Subquote view.
  4. If payment still fails after 48 hours, system releases the slot and blocks further payment against that slot. The FR-005 AcceptanceEvent and accepted snapshot remain immutable; the system MUST NOT reopen the parent quote or make the accepted subquote selectable again. Recovery requires a new current subquote or an audited admin intervention.
  5. System notifies both patient and provider of payment failure and slot release.
- **Outcome**: Booking transitions to `Payment Window Expired`; the slot is released, payment against that accepted selection is permanently blocked, and the provider is notified. The FR-005 AcceptanceEvent and snapshot remain immutable. Recovery requires a new current subquote or an audited admin intervention; the prior parent quote and accepted subquote are not reopened.

**B3: Patient Cancels Inquiry During 48-Hour Slot Hold**:

- **Trigger**: Patient cancels the parent inquiry (FR-003 Workflow 5) while the 48-hour appointment slot hold is active (post-acceptance, pre-payment).
- **Steps**:
  1. System validates cancellation eligibility per FR-003 Workflow 5 (inquiry is in Accepted stage — cancellation allowed).
  2. System immediately releases the 48-hour appointment slot hold; slot returned to provider's availability.
  3. Accepted subquote and its parent quote transition to "Cancelled (Inquiry Cancelled)"; the AcceptanceEvent is retained and marked superseded; inquiry transitions to "Cancelled".
  4. System notifies provider of both inquiry cancellation and slot release (slot is now available for reallocation).
  5. System notifies patient of successful cancellation with confirmation.
  6. Booking/payment flow becomes inaccessible for this inquiry.
- **Outcome**: Slot released immediately; no booking created; no payment collected; provider notified and can reallocate slot; patient can create a new inquiry.

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

**Purpose**: Review the accepted subquote and inherited parent context, view its pre-scheduled appointment slot, and proceed to payment without reselection

**Note**: This screen is accessed directly from FR-005's Accepted Subquote detail view. The FR-005 acceptance snapshot is the authoritative read-only source.

**Data Fields** (Continuation from FR-005):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Parent Quote Reference | text | Yes | Accepted parent quote identifier and version | Read-only; from AcceptanceEvent |
| Accepted Subquote Reference | text | Yes | Accepted subquote identifier and version | Read-only; from AcceptanceEvent; version MUST equal the accepted parent quote version |
| Accepted Selection Summary | group | Yes | Package, services, date range, appointment, price, promotion, and treatment plan plus inherited treatment context | Read-only; from acceptance snapshot |
| Pre-Scheduled Appointment | datetime | Yes | Appointment selected by the accepted subquote | Read-only; from acceptance snapshot |
| Provider Name | text | Yes | Provider/clinic name | Read-only; inherited parent context |
| Treatment Type | text | Yes | Accepted treatment and technique context | Read-only; inherited parent snapshot |
| Estimated Graft Count | number | Yes | Accepted graft estimate | Read-only; inherited parent snapshot |
| Clinician Assigned | text | Yes | Clinician attached to the accepted parent quote | Read-only; inherited parent snapshot |
| Provider Notes | text | No | Provider notes attached to the accepted parent quote | Read-only; inherited parent snapshot |
| Visual Plan | link/viewer | No | Accepted visual treatment plan | Read-only; inherited parent snapshot |
| Provider Requirements | group | No | Provider requirements attached to the accepted parent quote | Read-only; inherited parent snapshot |
| Quote Attachments | links | No | Documents and media attached to the accepted parent quote | Read-only; inherited parent snapshot |
| Parent Quote Expiry | datetime | Yes | Expiry captured when the subquote was accepted | Read-only; inherited parent snapshot |
| Acceptance Audit Context | group | Yes | AcceptanceEvent reference, actor, timestamp, and source aggregate version | Read-only; from AcceptanceEvent and acceptance snapshot |
| Total Amount | number | Yes | Accepted subquote offered price | Read-only; from acceptance snapshot |
| Deposit Amount | number | Yes | Calculated deposit (admin-configurable %, default 20-30%) | Within configured bounds |
| Deposit Percentage | text | Yes | Display deposit percentage used | Read-only; for transparency |
| Remaining Balance | number | Yes | Total - Deposit | Calculated automatically |
| Payment Option | select | Yes | Full payment or Installments (2–9) | Feasible installment options based on FR-029 split payment settings and FR-007B schedule rules (completion ≥30 days before procedure) |
| Installment Plan | select | Conditional | Number of installments if selected | Only shown if installment option selected |
| Currency | text | Yes | Payment currency and locked exchange-rate context | Read-only; from acceptance snapshot |
| Cancellation Policy | text | Yes | Policy summary with refund schedule | Read-only; admin-configured |
| Cancellation Policy Ack | checkbox | Yes | User acknowledges policy | Must be checked before payment |
| Terms & Conditions Ack | checkbox | Yes | User acknowledges T&C | Must be checked before payment |

**Blocked State (Inquiry Cancelled)**:

If pre-booking validation fails (parent inquiry cancelled per FR-003 Workflow 5), this screen displays a read-only blocked state instead of the payment form:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Blocked Banner | banner | Yes | "This inquiry has been cancelled. Booking is no longer available." | Full-width, prominent styling |
| Accepted Selection Summary | group | Yes | Accepted subquote and inherited parent context | Read-only; greyed out |
| Cancellation Timestamp | datetime | Yes | When the inquiry was cancelled | Read-only; from inquiry |
| Back to Dashboard | button | Yes | Returns patient to Inquiry Dashboard (FR-003 Screen 8) | Always enabled |

All payment fields and actions are hidden. Patient can only view the blocked state and navigate back.

**Business Rules**:

- All accepted subquote and inherited parent details from the FR-005 acceptance snapshot are displayed read-only.
- Appointment is already selected by the accepted subquote and its slot is held for payment; no selection is available here. The booking is confirmed only after successful payment.
- If parent inquiry is in "Cancelled" status, screen enters blocked state (see above) — payment form is hidden, blocked banner is displayed.
- Deposit amount calculated using admin-configured percentage (default 20-30% range).
- Disable Pay button until all required acknowledgments (cancellation policy, T&C) are checked.
- Show clear breakdown: total amount, deposit amount, remaining balance, currency.
- Display time zone relative labels and local time conversions for appointment slot.
- If installment plan selected, show installment schedule and completion date (must be ≥30 days before procedure).
- Only show installment options returned as feasible per FR-029 configuration + FR-007B schedule rules; if none are feasible, allow Pay-in-Full only with a clear explanation.

**Notes**:

- This screen is a continuation of FR-005's Accepted Subquote flow.
- Package, date range, appointment, and price cannot be changed or reselected here.
- Link to full cancellation policy document if needed.

---

#### Screen 2: Booking Confirmation & Itinerary (Patient)

**Purpose**: Display confirmed booking, reference number, next steps, basic itinerary

**Data Fields** (Continuation from Screen 1):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Booking Reference | text | Yes | Unique booking reference number | Format per HPID/booking scheme |
| Booking Status | badge | Yes | Confirmed | Must be "Confirmed" |
| Parent Quote Reference | text | Yes | Accepted parent quote identifier/version | Read-only; from AcceptanceEvent |
| Accepted Subquote Reference | text | Yes | Accepted subquote identifier/version | Read-only; from AcceptanceEvent |
| Provider Name | text | Yes | Provider/clinic name | Read-only; inherited parent context |
| Provider Contact | group | Yes | Clinic address, phone, email | Read-only; unmasked after payment |
| Procedure Date | datetime | Yes | Confirmed appointment slot | Read-only; from accepted subquote snapshot |
| Procedure Time | time | Yes | Appointment start time | Read-only; from accepted subquote snapshot |
| Treatment Type | text | Yes | Inherited treatment name (FUE, FUT, etc.) | Read-only; from parent snapshot |
| Total Amount | number | Yes | Total booking amount | Read-only; from accepted subquote snapshot |
| Deposit Paid | number | Yes | Deposit amount paid | Read-only; from payment |
| Payment Status | badge | Yes | Deposit paid / Installments scheduled / Full paid | Must reflect latest payment state |
| Remaining Balance | number | Yes | Amount remaining to pay | Calculated automatically |
| Next Payment Due | datetime | Conditional | Next installment due date | Only shown if installments active |
| Payment Method | text | Yes | Payment method used | Read-only; from payment |
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
| Accepted Subquote Reference | text | Yes | Accepted subquote identifier | Link to accepted selection details |
| Parent Quote Reference | text | Yes | Source parent quote identifier | Link to parent quote audit details |
| Booking Status | badge | Yes | Accepted / Payment Window Expired / Confirmed / In Progress / Aftercare / Completed / Cancelled | Filterable by status |
| Appointment Date | datetime | Yes | Pre-scheduled appointment slot | Sortable by date |
| Treatment Type | text | Yes | Treatment name | Filterable |
| Total Amount | number | Yes | Total booking amount | Sortable |
| Deposit Status | badge | Yes | Pending / Paid / Partial | Filterable |
| Deposit Amount | number | Yes | Deposit amount (if paid) | Read-only |
| Payment Status | badge | Yes | Deposit only / Installments / Full paid | Read-only |
| Created Date | datetime | Yes | Booking creation timestamp | Sortable |
| Actions | buttons | Yes | View Details, Check In (if confirmed + fully paid) | RBAC enforced |

**Business Rules**:

- Table list format only (no calendar view).
- Auto-block appointment slot upon booking confirmation (enforced at database level).
- Patient identity remains masked until booking status is "Confirmed" (payment success).
- Filtering options: Status, Date Range, Treatment Type, Payment Status.
- Sorting options: Date, Amount, Status, Created Date.
- Clicking on booking row opens booking detail view (Screen 4).
- FR-005 prevents a second acceptance from acquiring a slot already held or blocked by another pending or confirmed booking. FR-006 revalidates exclusive hold ownership before payment initiation and atomically converts that hold into the confirmed calendar block after successful payment.

**Notes**:

- Consistent with provider interface patterns from FR-004 and FR-005.
- Show payment summary figures without revealing card details.
- Appointment slot blocking is automatic and enforced - no manual calendar management needed.

---

#### Screen 4: Booking Detail View (Provider)

**Purpose**: View complete booking details with full context from inquiry, parent quote, accepted subquote, acceptance, and booking stages

**Data Fields** (Continuation from Screen 3, aggregating data from FR-003, FR-004, FR-005, FR-006):

**Section 1: Booking & Scheduling Information** (from FR-006):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Booking Reference | text | Yes | Unique booking reference | Read-only |
| Booking Status | badge | Yes | Current status (Accepted/Payment Window Expired/Confirmed/In Progress/Aftercare/Completed/Cancelled) | Read-only |
| Booking Created Date | datetime | Yes | Booking creation timestamp | Read-only |
| Appointment Date | datetime | Yes | Confirmed appointment slot (pre-scheduled in quote) | Read-only |
| Appointment Time | time | Yes | Appointment start time | Read-only |

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

**Section 5: Accepted Selection Information** (from FR-004 and FR-005):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Parent Quote Reference | text | Yes | Accepted parent quote identifier/version | Read-only; link to parent quote audit |
| Accepted Subquote Reference | text | Yes | Accepted subquote identifier/version | Read-only; link to AcceptanceEvent |
| Accepted Date | datetime | Yes | Subquote acceptance date | Read-only; from AcceptanceEvent |
| Accepted Provider | text | Yes | Provider/clinic captured at acceptance | Read-only; inherited parent snapshot |
| Treatment Type | text | Yes | Selected treatment (FUE, FUT, DHI, etc.) | Read-only; inherited parent snapshot |
| Estimated Graft Count | number | Yes | Estimated number of grafts | Read-only; inherited parent snapshot |
| Technique Specifications | text | No | Technique details | Read-only; inherited parent snapshot |
| Visual Plan | link/viewer | No | Accepted visual treatment plan | Read-only; inherited parent snapshot |
| Selected Package and Services | group | Yes | Exact package snapshot and included/custom services | Read-only; accepted subquote snapshot |
| Clinician Assigned | text | Yes | Clinician who will perform procedure | Read-only; inherited parent snapshot |
| Provider Notes | text | No | Provider's notes to patient | Read-only; inherited parent snapshot |
| Provider Requirements | group | No | Provider requirements attached to the accepted parent quote | Read-only; inherited parent snapshot |
| Quote Attachments | links | No | Documents and media attached to the accepted parent quote | Read-only; inherited parent snapshot |
| Parent Quote Expiry | datetime | Yes | Expiry captured when the subquote was accepted | Read-only; inherited parent snapshot |
| Acceptance Audit Context | group | Yes | AcceptanceEvent reference, actor, timestamp, and source aggregate version | Read-only; from AcceptanceEvent and acceptance snapshot |
| Selected Date Range | date range | Yes | Accepted patient-requested range | Read-only; accepted subquote snapshot |
| Treatment Plan (per-day) | table | Yes | Day-by-day treatment plan | Read-only; accepted subquote snapshot |

**Section 6: Pricing & Payment Information** (from FR-004, FR-006, FR-007):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Currency | text | Yes | Payment currency and locked exchange-rate context | Read-only; acceptance snapshot |
| Offered Price | number | Yes | Complete accepted subquote price | Read-only; acceptance snapshot |
| Promotion Applied | group | No | Structured promotion included in the accepted price | Read-only; acceptance snapshot |
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
| Check In | button | Status = Confirmed, Appointment date = today or past, Payment Status = Full paid | Mark patient as arrived (handoff to FR-010) |
| View Inquiry | link | Always | Open full inquiry details (FR-003) |
| View Accepted Selection | link | Always | Open accepted subquote and AcceptanceEvent details (FR-005) |
| View Parent Quote | link | Always | Open source parent quote details (FR-004) |
| View 3D Scan | link | Always | Open 3D scan viewer |
| View Medical Questionnaire | link | Always | Open medical questionnaire |

**Business Rules**:

- Patient full identity only visible if booking status is "Confirmed" (payment successful).
- All booking data is read-only (cannot be edited by provider).
- Check In button only available if status is "Confirmed", appointment date is today or past, and Payment Status is "Full paid" (no outstanding balance).
- All sections display data from previous stages (inquiry → parent quote/subquote → acceptance → booking) in chronological order.
- Links to the inquiry, accepted selection, and source parent quote provide full context and audit trail.

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
| Booking Status | badge | Yes | Accepted / Payment Window Expired / Confirmed / In Progress / Aftercare / Completed / Cancelled | Filterable |
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

**Section 5: Accepted Selection Information** (from FR-004 and FR-005):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Parent Quote Reference | text | Yes | Accepted parent quote identifier/version | Read-only; link to parent quote audit |
| Accepted Subquote Reference | text | Yes | Accepted subquote identifier/version | Read-only; link to AcceptanceEvent |
| Accepted Date | datetime | Yes | Subquote acceptance date | Read-only; from AcceptanceEvent |
| Accepted Provider | text | Yes | Provider/clinic captured at acceptance | Read-only; inherited parent snapshot |
| Treatment Type | text | Yes | Selected treatment (FUE, FUT, DHI, etc.) | Read-only; inherited parent snapshot |
| Estimated Graft Count | number | Yes | Estimated number of grafts | Read-only; inherited parent snapshot |
| Technique Specifications | text | No | Technique details | Read-only; inherited parent snapshot |
| Visual Plan | link/viewer | No | Accepted visual treatment plan | Read-only; inherited parent snapshot |
| Selected Package and Services | group | Yes | Exact package snapshot and included/custom services | Read-only; accepted subquote snapshot |
| Clinician Assigned | text | Yes | Clinician who will perform procedure | Read-only; inherited parent snapshot |
| Provider Notes | text | No | Provider's notes to patient | Read-only; inherited parent snapshot |
| Provider Requirements | group | No | Provider requirements attached to the accepted parent quote | Read-only; inherited parent snapshot |
| Quote Attachments | links | No | Documents and media attached to the accepted parent quote | Read-only; inherited parent snapshot |
| Parent Quote Expiry | datetime | Yes | Expiry captured when the subquote was accepted | Read-only; inherited parent snapshot |
| Acceptance Audit Context | group | Yes | AcceptanceEvent reference, actor, timestamp, and source aggregate version | Read-only; from AcceptanceEvent and acceptance snapshot |
| Selected Date Range | date range | Yes | Accepted patient-requested range | Read-only; accepted subquote snapshot |
| Treatment Plan (per-day) | table | Yes | Day-by-day treatment plan | Read-only; accepted subquote snapshot |

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
| Currency | text | Yes | Payment currency and locked exchange-rate context | Read-only; acceptance snapshot |
| Offered Price | number | Yes | Complete accepted subquote price | Read-only; acceptance snapshot |
| Promotion Applied | group | No | Structured promotion included in the accepted price | Read-only; acceptance snapshot |
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
| Version History | table | Yes | Parent quote and subquote version history captured at acceptance | Read-only |

**Intervention Actions**:

| Action | Type | Condition | Description |
|--------|------|-----------|-------------|
| Modify Status | button | Always | Change booking status (requires reason) |
| Modify Appointment Date | button | Always | Change appointment date/time (requires reason) |
| Process Refund | button | Booking cancelled or eligible | Process refund per cancellation policy |
| Cancel Booking | button | Always | Cancel booking (requires reason) |
| Add Internal Note | button | Always | Add admin-only note |
| View Inquiry | link | Always | Open full inquiry details (FR-003) |
| View Accepted Selection | link | Always | Open accepted subquote and AcceptanceEvent details (FR-005) |
| View Parent Quote | link | Always | Open source parent quote details (FR-004) |
| View 3D Scan | link | Always | Open 3D scan viewer |
| View Medical Questionnaire | link | Always | Open medical questionnaire |

**Business Rules**:

- Admin has full visibility to all patient and provider information (no masking).
- Admin can modify booking status and appointment date (emergency cases only) with required reason/justification.
- All modifications are logged in audit trail with who/when/what/why.
- Admin can process refunds per cancellation policy.
- Admin can add internal notes to booking (not visible to patient/provider).
- All sections display data from previous stages (inquiry → parent quote/subquote → acceptance → booking) in chronological order.
- Links to the inquiry, accepted selection, and source parent quote provide full context and audit trail.

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
- Appointment slot is selected by the accepted subquote and held for payment; no additional slot selection is permitted.
- Provider calendars must be accurate; confirmed bookings auto-block times at database level; overlapping appointments are prevented.
- All timestamps shown in patient's local timezone; provider view shows both local and clinic time.
- **Overlapping Appointment Prevention**: FR-005 atomically acquires an exclusive slot hold when acceptance is created. A second acceptance for a held or blocked slot is rejected before any AcceptanceEvent or booking handoff is created. FR-006 verifies hold ownership before payment and converts the hold into a confirmed calendar block on payment success; stale or invalid handoffs are rejected before the payment gateway is called.

### Data & Privacy Rules

- Patient identity remains masked to provider until booking is Confirmed (payment success).
- Booking, payment, and personal data are encrypted at rest and in transit; audit logs are immutable.
- Retain booking and financial records ≥7 years; hard deletes prohibited (soft-delete/archive only).

### Admin Editability Rules

**Editable by Admin** (via A-09: System Settings & Configuration):

- **Deposit Rate**: Admin MUST be able to configure deposit percentage (default range: 20-30% of total booking amount) via **FR-029: Payment System Configuration**. This is configurable per provider or globally. Changes apply to new bookings only (existing bookings retain original deposit rate).
- Cancellation policy schedule (thresholds and refund percentages).
- Payment failure hold duration (default: 48 hours) - how long to hold the accepted subquote's slot after payment failure.
- Notification templates for booking confirmations/reminders; booking confirmation content (configured via **FR-030: Notification Rules & Configuration**).
- Commission settings.

**Confirmed Booking Data Integrity (Admin Override)**:

- Confirmed bookings are **read-only for patients and providers**.
- Admins MAY perform emergency modifications (e.g., appointment date/time, status corrections), but MUST do so as **append-only, versioned intervention events** (who/when/what/why) rather than overwriting historical records.
- Financial transactions (payments/refunds) remain immutable once confirmed; admin actions reference the original transaction IDs and create new adjustment/refund events as needed.

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
- **Post-Acceptance Hold**: After subquote acceptance, the system holds the reserved appointment slot for 48 hours to allow the patient to complete initial payment (deposit or first installment). If no payment is completed within 48 hours, the reservation is released and payment against that slot is blocked without mutating the accepted selection.
- **Payment Window Expired**: Hold expiry moves the pending booking from `Accepted` to `Payment Window Expired`. This is a terminal payment-window outcome for that accepted selection: the slot is released, payment is disabled, the AcceptanceEvent/snapshot remain immutable, and neither the parent quote nor accepted subquote is reopened.
- **Payment Failure Handling**:
  - If deposit payment fails, Payment Service applies retry policy per FR-007 (exponential backoff) and surfaces failures for patient action when needed.
  - The accepted subquote's appointment slot is held for 48 hours (admin-configurable) to allow patient to retry payment.
  - During the hold period, the slot remains reserved; patient can retry payment from the Accepted Subquote view.
  - If payment still fails after the hold period, the slot is released and further payment against it is blocked.
  - The AcceptanceEvent and snapshot remain immutable. Recovery requires a new current subquote or audited admin intervention; the parent quote is not automatically reopened.
- Refunds per cancellation policy example in `system-prd.md`; provider cancellations require admin approval and full refund.
- Prices shown in patient's currency; exchange rate locked in the subquote acceptance snapshot; payouts use that locked rate.

### Rescheduling Rules

- **Rescheduling is deferred to V2**: The provider pre-schedules the appointment in the subquote; acceptance fixes the chosen appointment and reserves its slot, and successful payment confirms the booking. Rescheduling functionality will be evaluated for V2 based on business needs.
- **Current Behavior**: Once booking is confirmed, date changes require admin intervention or cancellation/rebooking per cancellation policy.

---

## Success Criteria

### Patient Experience Metrics

- **SC-001**: Patients can confirm a booking in ≤3 minutes from an accepted subquote.
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

- **SC-014**: 85% of accepted subquotes convert to confirmed bookings (aligned with system targets).
- **SC-015**: Deposit capture rate ≥ 80% within 24 hours of subquote acceptance.
- **SC-016**: Refund disputes < 2% of total bookings.

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **FR-001 / Module P-01**: Auth & Profile; required for authenticated patient actions and identity unmasking post-payment.
  - **Integration point**: Booking flow requires verified patient and profile data.
- **FR-004 / Module PR-02**: Quote Submission; provides pre-scheduled slots and quote breakdown.
- **FR-005 / Module P-02**: Subquote Comparison & Acceptance; supplies the immutable accepted subquote and inherited parent snapshot and triggers booking entry.
- **FR-007 & FR-007B / Modules P-03, S-02**: Payments and Installments; deposit capture, schedules, refunds.
- **FR-020 / S-03**: Notifications; confirmations, reminders, and alerts.
- **FR-030 / Module A-09**: Notification Rules & Configuration; booking confirmation/reminder templates and notification policy rules consumed by S-03.
- **FR-010 / PR-03**: Post-confirmation treatment execution starts on arrival.
- **FR-029 / Module A-09**: Payment System Configuration; deposit, split payment, and commission settings are managed here (deposit default 20-30% range; installment options and cutoff rules; commission default 15-25% range, per-provider or global settings).

### External Dependencies (APIs, Services)

- Payment processor for deposits/installments/refunds (PCI compliant); retry with backoff, hold booking for 48 hours on failure.
- Calendar/ICS generation for add-to-calendar links.

### Data Dependencies

- Active provider calendars with pre-scheduled slots from FR-004 Option/date-price records (PR-02).
- FR-005 AcceptanceEvent with accepted subquote/parent identifiers and versions, complete snapshot, locked currency/exchange rate, and promotion data (FR-004/FR-019).
- Patient verified profile and medical status flags (P-01/P-02) for provider readiness.

---

## Assumptions

### User Behavior Assumptions

- Patients act within 24–48 hours after subquote acceptance to book.
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

- Patient app to booking API for payment initiation (slot is pre-scheduled and read-only).
  - Data: AcceptanceEvent ID, accepted parent quote ID/version, accepted subquote ID/version, immutable acceptance snapshot, pre-scheduled slot ID, payment choice, and acknowledgments. The accepted subquote and parent version values MUST be equal.
  - Auth: patient token; RBAC enforcing ownership.
  - Errors: validation feedback; recoverable payment failures.
- Provider calendar API for blocking/unblocking; admin oversight API for audit and dispute actions.

### Scalability Considerations

- Expect hundreds of concurrent bookings during campaigns; ensure slot-hold locking performs under load.
- Background jobs for reminders and installment schedules; horizontal scaling for booking endpoints.

### Security Considerations

- MFA is a **planned mandatory control** for Admin and Provider tenants and MUST be treated as a future (non-MVP) requirement until the shared MFA stack is delivered (per Constitution / FR-026 / FR-031). Until then, enforce strong password policies, throttling, and re-authentication flows where appropriate; RBAC everywhere.
- TLS 1.3 in transit; AES-256 at rest; no storage of card PANs; webhook signature verification.
- Full audit trail on state changes and access; rate limiting and anti-abuse protections on booking/payment endpoints.

---

## User Scenarios & Testing

### User Story 1 - Confirm Booking with Deposit (Priority: P1)

Patient confirms a booking from an accepted subquote by paying the deposit; package, date range, appointment, and price remain exactly as accepted.

**Why this priority**: Core conversion event from interest to revenue.

**Independent Test**: Accept a subquote, pay deposit, and verify the booking preserves the accepted snapshot, calendar block, and notifications.

**Acceptance Scenarios**:

1. Given an accepted subquote with a valid held slot, When patient pays deposit, Then booking preserves the accepted selection, becomes Confirmed, and provider sees unmasked identity.
2. Given a confirmed booking, When confirmation is generated, Then both parties receive it within 1 minute.
3. Given confirmation, When viewing provider calendar, Then slot is blocked and non-overlapping.
4. Given a booking handoff with a stale parent aggregate version or mismatched accepted parent/subquote versions, When FR-006 validates the handoff, Then the system rejects it before booking creation or payment initiation and does not mutate the appointment slot or FR-005 AcceptanceEvent.

---

### User Story 2 - Payment Failure Handling (Priority: P1)

Patient's deposit payment fails; system holds slot for retry period; patient successfully retries payment.

**Why this priority**: Critical for conversion and user experience.

**Independent Test**: Simulate payment failure, verify hold period, retry payment, confirm booking.

**Acceptance Scenarios**:

1. Given an accepted subquote with payment failure, When system holds its slot for 48 hours, Then patient can retry payment against the same immutable selection and booking confirms successfully.
2. Given payment failure after the hold period expires, When the slot is released, Then the booking becomes `Payment Window Expired`, payment against that selection is permanently blocked, the acceptance snapshot remains immutable, and both parties are notified.

---

### User Story 3 - Overlapping Appointment Prevention (Priority: P1)

Two patients attempt to accept subquotes for the same appointment slot; the first atomic acceptance acquires the exclusive hold and the second acceptance is rejected before creating another accepted selection.

**Why this priority**: Prevents double-booking and ensures calendar integrity.

**Independent Test**: Submit concurrent acceptance requests for the same slot; verify exactly one exclusive hold, one AcceptanceEvent, and one booking handoff are created, while the rejected request leaves its quote and inquiry state unchanged.

**Acceptance Scenarios**:

1. Given two concurrent acceptance attempts for the same slot, When the atomic reservation check runs, Then exactly one attempt acquires the hold and creates an AcceptanceEvent.
2. Given a slot already held or blocked by another pending or confirmed booking, When a patient attempts acceptance, Then acceptance is rejected before quote/inquiry state changes, AcceptanceEvent creation, booking handoff, or payment initiation.

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
- A stale or forged booking handoff references a slot not exclusively held by its AcceptanceEvent: reject it before payment initiation and leave the valid reservation unchanged.
- Installment plan default before deadline: flag booking, notify admin and patient; apply policy.
- Provider emergency closure: admin-approved cancellation, full refund, suggest alternatives.
- Payment failure after subquote acceptance: hold the slot for the configurable duration (default 48 hours) and allow retry only during that window; on expiry, set `Payment Window Expired`, release the slot, permanently block payment against that selection, and do not reopen the parent quote or accepted subquote.
- Two patients attempt to accept subquotes with the same slot simultaneously: the atomic acceptance transaction creates one exclusive hold and one AcceptanceEvent; the losing attempt receives a clear unavailable-slot error and creates no booking handoff.
- Patient submits payment while inquiry is being cancelled concurrently: system MUST perform atomic pre-booking validation at payment submission time (not just at screen entry). If inquiry transitions to "Cancelled" between screen load and payment submission, payment MUST be rejected with message "This inquiry has been cancelled" and no charge processed. Payment gateway must not be called if inquiry is cancelled.
- Patient is on Screen 1 when inquiry cancellation notification arrives: system SHOULD use real-time push (WebSocket/SSE) to transition Screen 1 to blocked state without requiring page refresh.

---

## Functional Requirements Summary

### Core Requirements

- **REQ-006-001**: Patients MUST be able to proceed to payment after accepting one subquote; FR-006 MUST consume its package, date range, appointment, price, promotion, and inherited parent context without reselection.
- **REQ-006-002**: System MUST confirm booking only after successful deposit/initial installment and unmask patient identity to provider.
- **REQ-006-003**: System MUST require an exclusive appointment hold created atomically with FR-005 acceptance, reject any handoff that does not own the valid hold before payment initiation, and convert that hold into a provider calendar block only after successful payment confirmation.
- **REQ-006-004**: System MUST enforce cancellation policy with scheduled refunds per policy (rescheduling deferred to V2).
- **REQ-006-005**: System MUST hold the accepted subquote's appointment slot for a configurable duration (default 48 hours) after payment failure. If the hold expires, System MUST set the booking to `Payment Window Expired`, release the slot, permanently block payment against that accepted selection, preserve the immutable AcceptanceEvent/snapshot, and require a new current subquote or audited admin intervention for recovery without reopening the prior parent quote or accepted subquote.

### Data Requirements

- **REQ-006-006**: System MUST store booking reference, slot, status history, payment state, refund state, and audit trail ≥7 years.
- **REQ-006-007**: System MUST link each booking to exactly one FR-005 AcceptanceEvent, accepted parent quote identifier/version, accepted subquote identifier/version, immutable acceptance snapshot, and provider calendar slot. `acceptedSubquoteVersion` MUST equal `acceptedParentQuoteVersion`.

### Security & Privacy Requirements

- **REQ-006-008**: System MUST keep patient identity masked until payment confirmation; encrypt PII at rest and in transit.
- **REQ-006-009**: System MUST log all booking state changes and accesses with user, timestamp, and reason.

### Integration Requirements

- **REQ-006-010**: System MUST integrate with Payment Service for deposits, installments, refunds, and lock exchange rate.
- **REQ-006-011**: System MUST integrate with Notification Service for confirmations, reminders, and policy notices.

### Configuration Requirements

- **REQ-006-012**: Admin MUST be able to configure deposit percentage (default: 20-30% range) via **FR-029: Payment System Configuration** (Module A-09: System Settings & Configuration).
- **REQ-006-013**: Admin MUST be able to configure payment failure hold duration (default: 48 hours) via A-09: System Settings & Configuration.
- **REQ-006-014**: System MUST verify the parent inquiry is not in "Cancelled" status before allowing entry to the booking/payment flow. If cancelled, system MUST block entry and display a read-only blocked state (Screen 1 blocked state) with clear messaging.

### Marking Unclear Requirements

None.

---

## Key Entities

- **Entity 1 - Booking**: Represents a confirmed or pending booking derived from one accepted subquote and its inherited parent context.
  - **Key attributes**: booking reference, acceptanceEventId, acceptedParentQuoteId, acceptedParentQuoteVersion, acceptedSubquoteId, acceptedSubquoteVersion, acceptanceSnapshot, providerId, patientId, slotId, status, payment state, refund state.
  - **Version invariant**: `acceptedSubquoteVersion = acceptedParentQuoteVersion`; both identify the accepted FR-004 aggregate revision.
  - **Status values**: `Accepted` (subquote accepted, awaiting payment) → `Confirmed` (deposit paid) → `In Progress` (procedure started, via FR-010) → `Aftercare` (treatment complete; aftercare active via FR-011) → `Completed` (aftercare complete / final review submitted). From `Accepted`, hold expiry transitions to `Payment Window Expired`; governed cancellation transitions to `Cancelled`.
  - **Relationships**: One booking links to one AcceptanceEvent, one accepted subquote and parent quote context, one provider calendar entry, and one patient.

- **Entity 2 - Calendar Slot**: Represents a provider's pre-scheduled appointment time.
  - **Key attributes**: provider ID, start/end, capacity, hold/blocked flags, expiration.
  - **Release triggers**: (1) Payment failure hold expiry (48h default), (2) Patient-initiated inquiry cancellation during hold period (FR-003 Workflow 5, immediate release per B3 flow), (3) Booking cancellation per B2 flow.
  - **Relationships**: One slot can be held or blocked by at most one pending or confirmed booking; acceptance and hold acquisition are atomic.

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-04 | 1.0 | Initial PRD creation | AI |
| 2025-11-04 | 1.1 | Major revisions: Removed slot selection step (slot auto-confirmed on quote acceptance); Added deposit rate management (admin-configurable); Deferred rescheduling to V2; Defined payment failure handling (48-hour hold); Added all 3 tenant screen specifications with data continuity; Updated provider dashboard to table-only format; Added overlapping appointment prevention logic | AI |
| 2025-11-04 | 1.2 | Enhanced booking detail screens: Added comprehensive data from all previous stages (FR-003 inquiry, FR-004 quote, FR-005 acceptance) to provider and admin booking detail screens; Clarified deposit rate management is handled in FR-029: Payment System Configuration | AI |
| 2025-11-12 | 1.3 | Status updated to Verified & Approved; All approvals completed | Product Team |
| 2025-12-16 | 1.4 | Documentation alignment: Clarified installment option eligibility and payment option wording to reference FR-029 as the configuration source for deposit/split payment/commission settings (no functional change). | AI |
| 2026-02-05 | 1.5 | Added pre-booking validation guard (inquiry not cancelled), Alternative Flow B3 (patient cancels inquiry during 48h slot hold with immediate release). See FR-003 Workflow 5 and cancel-inquiry-fr-impact-report.md | Product & Engineering |
| 2026-02-09 | 1.6 | Integrity fixes: Added Screen 1 blocked state spec (cancelled inquiry UI), REQ-006-014 (pre-booking cancellation guard requirement), concurrent payment+cancellation race edge cases, explicit Booking status enum, Calendar Slot release triggers, fixed Last Updated date. | AI |
| 2026-03-03 | 1.7 | Cross-FR alignment: Added `Aftercare` to booking status enum and booking status filters; clarified Check In requires Payment Status = Full paid (no outstanding balance) to align with FR-010/FR-007. | Product alignment (2026-03-03) |
| 2026-09-15 | 2.0 | Reconciled FR-006 with FR-005 v2.0: booking now consumes one immutable accepted subquote and inherited parent context; screens and entities carry parent/subquote identifiers and versions; package/date/appointment/price reselection is prohibited; payment-expiry and slot-conflict handling preserve the AcceptanceEvent instead of reopening a parent quote. See CR-FR006-20260915-01. Status reset pending consolidated verification. | Product Owner / Documentation |
| 2026-09-16 | 2.1 | Post-verification clarification: defined `acceptedSubquoteVersion` as equal to `acceptedParentQuoteVersion`, both sourced from the accepted FR-004 aggregate `QuoteVersion`; applied the invariant to the booking handoff, screen provenance, requirement, and entity contract. Verification status remains pending consolidated review. | Product Owner / Verification alignment |
| 2026-09-16 | 2.2 | Reconciled payment-hold expiry: introduced terminal `Payment Window Expired`, removed the contradictory post-expiry retry path, permanently blocks payment against the expired accepted selection, and requires a new current subquote or audited admin intervention without reopening prior quote records. Verification status remains pending consolidated review. | Product Owner / Verification alignment |
| 2026-09-16 | 2.3 | Clarified the appointment lifecycle boundary: subquote acceptance fixes the appointment choice and reserves the slot for the payment window; only successful deposit or first-installment payment confirms the booking. Removed remaining wording that equated acceptance with slot/booking confirmation. | Product Owner / Documentation |
| 2026-09-16 | 2.4 | Resolved the slot-reservation concurrency contract: FR-005 acceptance atomically acquires one exclusive appointment hold; a second acceptance is rejected before AcceptanceEvent or booking-handoff creation; FR-006 revalidates hold ownership before payment and converts it to a confirmed calendar block on success. | Product Owner / Verification resolution |
| 2026-09-16 | 2.5 | Completed accepted-snapshot screen provenance: Patient Screen 1 and Provider/Admin booking details now enumerate inherited provider, treatment, graft, clinician, note, visual-plan, requirement, attachment, expiry, version, and acceptance-audit context as read-only snapshot data. Consolidated verification remains pending. | Product Owner / Verification resolution |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | [NAME NOT RECORDED] | 2025-11-12 | ✅ Approved through v1.7 |
| Technical Lead | [NAME NOT RECORDED] | 2025-11-12 | ✅ Approved through v1.7 |
| Stakeholder | [NAME NOT RECORDED] | 2025-11-12 | ✅ Approved through v1.7 |
| Product Owner | Product Owner | 2026-09-16 | Approved through v2.5 accepted-subquote handoff, complete screen provenance, exclusive acceptance-time slot reservation, payment-window, and appointment-confirmation boundaries; consolidated verification pending |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-011 Aftercare & Recovery Management PRD
**Last Updated**: 2026-09-16
