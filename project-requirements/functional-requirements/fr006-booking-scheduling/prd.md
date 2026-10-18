# FR-006 - Booking & Scheduling

**Module**: P-03: Booking & Payment | PR-02: Inquiry & Quote Management | A-01: Patient Management & Oversight
**Feature Branch**: `fr006-booking-scheduling`
**Created**: 2025-11-04
**Status**: 🟡 Revised — Pending Consolidated Verification
**Source**: FR-006 from `system-prd.md`; SRC-MTG-002, CR-FR006-20260915-01 and CR-FR006-20261016-01; continuation from FR-004 (Quote Submission) and FR-005 v2.3 (Subquote Comparison & Acceptance); coordinated with FR-007/FR-007B (Payments)
**Change Request**: [CR-FR006-20261016-01 — MTG-002 quote model alignment](change-request-2026-10-16-mtg002-quote-model-alignment.md)

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
- No in-app booking cancellation: from acceptance onward the patient sees a "Contact support" action, and an admin performs any cancellation (Alternative Flow B2).

**Provider Platform (PR-02)**:

- View accepted/confirmed bookings in table list format (no calendar view); receive confirmation notifications; enforce check-in workflow on arrival (handoff to FR-010).
- View deposit state and payment status (no card details); apply cancellation policy outcomes.
- Monitor booking status transitions and patient arrival readiness.

**Admin Platform (A-01, A-05, A-09)**:

- Monitor booking pipeline, intervene in disputes, process exceptional modifications under audit.
- Perform the governed booking interventions from Screens 6 to 10: revive a `Payment Window Expired` booking, change the appointment, cancel a booking (including support-routed patient requests), run the provider-fault transfer with an admin-authored replacement quote, and hand an Aftercare-stage provider fault to the FR-011 aftercare reassignment.
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
7. System creates the appointment record from the held slot, converts the hold into a provider calendar block, and displays booking details in provider dashboard.
8. Notification Service sends confirmations to patient and provider; Admin dashboard updates.

### Alternative Flows

**A1: Installment Plan Selected**:

- **Trigger**: Patient chooses an eligible installment plan.
- **Steps**:
  1. System determines feasible installment options based on FR-029 split payment settings (enabled installment counts, cutoff days, minimum booking amount) and procedure date constraints (completion ≥30 days before procedure).
  2. Schedule installment charges and reminders per FR-007B; mark booking Confirmed upon successful initial charge.
- **Outcome**: Booking confirmed; payment schedule tracked; reminders enabled.

**A2: Reschedule Request (Patient-Initiated)** - **DEFERRED TO V2**:

- **Note**: Rescheduling functionality is deferred to V2 pending business validation. The provider pre-schedules the appointment in the subquote; acceptance fixes that appointment choice and reserves its slot for the payment window, while successful payment confirms the booking. If a date change is required, it is handled through the audited admin appointment change (Screen 8) or a future enhancement.
- **Current Behavior**: The patient cannot reschedule. A date change requires the audited admin appointment change on Screen 8, which sends the mandatory `booking.rescheduled` notice to the patient and provider, or an admin cancellation (Alternative Flow B2).

**B1: Payment Failure**:

- **Trigger**: The first payment step (deposit or first installment) fails.
- **Steps**:
  1. Payment Service applies retry policy per **FR-007 (exponential backoff with idempotency)**.
  2. Payment failure never extends or restarts the slot hold. The slot stays held only until the single hold that started at subquote acceptance expires (FR-026 slot-hold duration, default 48 hours).
  3. While that hold is active, the slot remains reserved; patient can retry payment from the Accepted Subquote view.
  4. If no payment succeeds before the hold expires, system releases the hold and blocks further payment against that slot; no appointment record exists for the expired selection. The FR-005 AcceptanceEvent and accepted snapshot remain immutable; the system MUST NOT reopen the parent quote or make the accepted subquote selectable again. Recovery follows the Payment Window Expired recovery route (see Payment & Billing Rules).
  5. System sends the mandatory Payment Window Expired notice to the patient and the provider (the provider learns the slot is free).
- **Outcome**: Booking transitions to `Payment Window Expired`; the hold is released, payment against that accepted selection is blocked, and both parties are notified. The FR-005 AcceptanceEvent and snapshot remain immutable; the prior parent quote and accepted subquote are not reopened. The patient contacts support; an admin either revives the booking (Screen 7) or cancels it (Alternative Flow B2, Screen 9), after which the patient may start a new inquiry.
- **Boundary**: B1 and `Payment Window Expired` apply only to the first payment step (acceptance to deposit or first installment). A missed later installment or final payment never causes `Payment Window Expired` or inquiry cancellation; it is handled by FR-007 and FR-007B.

**B3: Cancellation During Post-Acceptance Slot Hold (Support-Routed)**:

- **Trigger**: While the post-acceptance appointment slot hold is active (post-acceptance, pre-payment), the patient asks support to cancel, or an admin decides to cancel. The patient cannot cancel in-app from the `Accepted` stage onward (FR-003 Workflow 5 allows patient self-cancellation only in the Inquiry and Quoted stages).
- **Steps**:
  1. An admin cancels the booking through Alternative Flow B2 on Screen 9, with a mandatory reason.
  2. System immediately releases the appointment slot hold; the slot returns to the provider's availability.
  3. The booking transitions from `Accepted` to `Cancelled` and the inquiry transitions to `Cancelled`. The accepted parent quote stays `accepted` for history. The AcceptanceEvent is kept unchanged; no supersession record is written, because a supersession record is written only at a provider-fault replacement acceptance (Alternative Flow B5).
  4. System sends `booking.cancelled` to the patient and the provider, including the cancellation reason; the provider can reallocate the slot.
  5. Booking/payment flow becomes inaccessible for this inquiry.
- **Outcome**: Slot released immediately; no appointment record is created; no payment collected; the provider is notified and can reallocate the slot; the patient can create a new inquiry.

**B2: Booking Cancellation (Admin Only)**:

- **Trigger**: From acceptance onward, the patient asks support to cancel through the "Contact support" action (the patient has no in-app cancel action after acceptance), or an admin decides a cancellation is needed (for example to settle a dispute). Only an admin performs the cancellation.
- **Allowed source states**: `Accepted`, `Payment Window Expired`, `Confirmed`, `In Progress`, and `Aftercare`. `Cancelled` and `Completed` are terminal and cannot be cancelled again.
- **Steps**:
  1. Admin opens Cancel Booking on Screen 6, which opens Screen 9, selects the request source (patient request through support, or admin decision), and enters a mandatory reason.
  2. Admin confirms the cancellation in a confirmation dialog that states the effects below.
  3. System transitions the booking to `Cancelled` with the admin's reason as the cancellation reason and the inquiry to `Cancelled`. The accepted parent quote stays `accepted` for history. The AcceptanceEvent and accepted snapshot stay unchanged; no supersession record is written.
  4. System releases any active hold or calendar block and blocks further payment against the accepted selection.
  5. System writes an audit entry (admin, timestamp, source state, request source, reason) and sends `booking.cancelled` to the patient and the provider, including the cancellation reason.
  6. Refunds and cancellation fees follow the cancellation policy and are handled under the payment placeholder; exact mechanics are defined later in FR-007, FR-007B, and FR-017.
- **Outcome**: Booking and inquiry are `Cancelled`; the accepted quote stays `accepted`; the action is audited; the slot is released back to the provider calendar.
- **Boundary**: Provider withdrawal of the accepted quote or provider drop-out after acceptance follows Alternative Flow B5, a provider fault while the booking is `In Progress` follows Alternative Flow B7, and a provider fault in the `Aftercare` stage follows Alternative Flow B6, not this flow. B2 is also the cancel route an admin chooses in Alternative Flow B7.

**B4: Provider Suspended or Deactivated (Admin-Initiated Cascade)**:

- **Trigger**: The provider's `Suspended` or `Deactivated` status becomes effective under [FR-015 Alternative Flow A5 and Screen 4](../fr015-provider-management/prd.md#screen-4-provider-suspensiondeactivation-modal).
- **Steps**:
  1. Every non-terminal booking of that provider before treatment starts (`Accepted` including unpaid within the payment hold, and `Confirmed`) transitions to `Cancelled` with cancellation cause `ProviderSuspended` or `ProviderDeactivated` and an independent `supportRequired` marker. The provider-status event itself authorizes the cascade; no per-booking approval is required. A booking in `In Progress` is not cancelled: it stays `In Progress`, receives the cause and the `supportRequired` marker, and follows Alternative Flow B7. A booking in `Aftercare` is not cancelled: it stays `Aftercare`, receives the cause and the `supportRequired` marker, and follows Alternative Flow B6.
  2. For each cancelled booking, System immediately releases any active appointment hold, reservation, or confirmed calendar slot and blocks further payment against the accepted selection, even if the original hold had time remaining.
  3. The FR-005 AcceptanceEvent, accepted snapshot, and booking/payment history are kept unchanged. The closure is recorded on the booking as its cancellation cause; no supersession record is written at this point. The supersession record is written once, when the replacement acceptance is created in Alternative Flow B5.
  4. An admin rehomes each affected patient to a replacement provider in the same inquiry through the provider-fault transfer in Alternative Flow B5 (steps 4 to 6), including its payment placeholder: paid amounts move with the patient as credit toward the replacement booking, any unused part is refunded, and the patient pays no fee.
  5. Patient and admin notifications and the admin support handoff follow FR-015 Screen 4; FR-006 does not send a patient-cancellation or payment-retry message for these bookings.
- **Outcome**: Bookings before treatment starts are cancelled with a provider-status cause, flagged for admin support, and rehomed by admin through Alternative Flow B5 in the same inquiry; `In Progress` bookings keep their status and wait for the admin decision in Alternative Flow B7; `Aftercare` bookings keep their status and move to aftercare reassignment through Alternative Flow B6.
- **Boundary**: B4 is the trigger for provider-status cases; the transfer itself follows B5, the `In Progress` decision follows B7, and the aftercare reassignment follows B6. Distinct from admin cancellation (B2/B3), provider-requested Cancel/Close Case (FR-010), and `Payment Window Expired` (B1). Provider reactivation never restores cancelled bookings, holds, or payment windows. A later deactivation does not overwrite an earlier `ProviderSuspended` cause.

**B5: Provider Fault After Acceptance (Admin Direct Transfer)**:

- **Trigger**: After subquote acceptance and before treatment starts (booking `Accepted` or `Confirmed`), the selected provider withdraws the accepted quote or drops out, or the provider's suspension or deactivation takes effect (entered from Alternative Flow B4). The transfer is limited to bookings before treatment starts: a provider fault while the booking is `In Progress` follows Alternative Flow B7, and a provider fault in the `Aftercare` stage follows Alternative Flow B6.
- **Steps**:
  1. The original booking transitions to `Cancelled` with cancellation cause `ProviderFault` (or `ProviderSuspended` / `ProviderDeactivated` when entered from B4) and the `supportRequired` marker. The closure is recorded on the booking as its cause; no supersession record is written yet.
  2. System immediately releases any active hold or calendar block of the original provider and blocks further payment against the original accepted selection.
  3. The original FR-005 AcceptanceEvent and accepted snapshot are kept unchanged as history.
  4. An admin opens Start Provider-Fault Transfer on Screen 6 (Screen 10), selects a replacement provider, and authors a replacement quote for that provider inside the same inquiry through [FR-004 Workflow 7](../fr004-quote-submission/prd.md#workflow-7-admin-replacement-quote-provider-fault-transfer) and [FR-004 Screen 8](../fr004-quote-submission/prd.md#screen-8-admin-replacement-quote-authoring). This admin-authored replacement quote is the only exception to the FR-004 rule that no new quote is created once an inquiry has an acceptance. The admin may adjust the package and price on the replacement quote; every field set by the admin is audited with a mandatory reason.
  5. The admin selects one option and one date-price row of the replacement quote and confirms. System creates a new admin-authored AcceptanceEvent that points to that replacement quote, option, and date-price row like any other acceptance, so price, promotion, commission, and the acceptance snapshot work unchanged. In the same transaction System writes the single supersession record owned by FR-005 that links the closed original AcceptanceEvent to the new one (append-only single insert, cause taken from the original booking), and acquires the slot hold for the replacement appointment. The patient re-enters nothing.
  6. A replacement booking is created from the new acceptance and follows the main flow from that record.
  7. Notifications: when the provider withdraws, FR-004 sends the mandatory `quote.withdrawn` notice and FR-006 does not send it again. The patient and admin are notified of the transfer through `booking.provider_fault_replacement` (FR-020 and FR-030). The replacement acceptance sends the patient the mandatory `booking.scheduled` notice with the replacement payment deadline, and the replacement provider learns of the booking through `quote.accepted` (outcome `selected_subquote_accepted`). The original provider is not notified by these events.
  8. Travel carries over through FR-008: when the replacement booking's travel context is created, the patient's passport record carries over to it, and the flight and hotel records are copied to it and flagged "travel-date review required" for admin review. The original travel records stay read-only on the closed booking, and the patient re-enters nothing.
- **Replacement quote not accepted**: If the admin does not record a replacement acceptance, the replacement quote expires under the normal FR-004 quote expiry. The inquiry stays flagged `supportRequired` and is not cancelled automatically. The admin may author another replacement quote through FR-004 Screen 8, or cancel the inquiry and booking through Alternative Flow B2 (Screen 9).
- **Payment placeholder**: Amounts the patient has already paid move with the patient as credit toward the replacement booking; any unused part is refunded; the patient pays no cancellation fee because the fault is not theirs. Exact refund, fund-release, and payment-allocation override mechanics are defined later in FR-007, FR-007B, and FR-017.
- **Outcome**: The patient keeps the same inquiry and moves to a replacement provider without a new patient acceptance. Every admin action in the transfer is audited.
- **Boundary**: For provider suspension or deactivation, Alternative Flow B4 is the trigger and closes the booking; this flow owns the transfer. Distinct from admin cancellation (B2/B3), aftercare reassignment (B6), the `In Progress` provider-fault decision (B7), and `Payment Window Expired` (B1).

**B6: Provider Fault During Aftercare (Aftercare Reassignment)**:

- **Trigger**: While the booking is `Aftercare` (treatment done), the provider withdraws or drops out of aftercare, or the provider's suspension or deactivation takes effect (entered from Alternative Flow B4).
- **Steps**:
  1. The booking stays `Aftercare` and the treatment record stays unchanged. No new quote, no new acceptance, and no new payment are created, and the AcceptanceEvent is not superseded.
  2. When entered from B4, the booking carries the provider-status cause and the `supportRequired` marker; the original provider loses aftercare actions on the case.
  3. An admin opens Reassign Aftercare on Screen 6, which links to the FR-011 aftercare reassignment screen, and reassigns the aftercare case to another provider or to the Hairline aftercare team, with a mandatory reason, confirmation, and audit entry, following FR-011.
  4. The admin's reassignment resolves the `supportRequired` marker with an audited resolution.
- **Outcome**: The patient continues aftercare with the new provider or team on the same booking.
- **Boundary**: The provider-fault transfer with a new acceptance (B5) applies only before treatment starts. Aftercare plan, milestone, and notification details are owned by FR-011.

**B7: Provider Fault While In Progress (Admin Decision)**:

- **Trigger**: While the booking is `In Progress` (after Check In and before treatment completion), the provider withdraws or drops out, or the provider's suspension or deactivation takes effect (entered from Alternative Flow B4).
- **Steps**:
  1. The booking stays `In Progress` and is not cancelled automatically. System sets the `supportRequired` marker and records the cause (`ProviderFault`, or `ProviderSuspended` / `ProviderDeactivated` when entered from B4). No replacement quote and no replacement acceptance are created, and the AcceptanceEvent is not superseded.
  2. An admin opens Resolve In-Progress Provider Fault on Screen 6 (Screen 11) and decides case by case, with a mandatory reason and a confirmation:
     - **Move to Aftercare and reassign**: System moves the booking from `In Progress` to `Aftercare`, keeps the treatment record as recorded, and opens the FR-011 aftercare reassignment screen (FR-011 Screen 19), where the admin assigns a new aftercare provider or the Hairline aftercare team following Alternative Flow B6.
     - **Cancel the booking**: System opens Screen 9 and the admin cancels the booking through Alternative Flow B2; the booking and inquiry become `Cancelled` and the accepted quote stays `accepted`.
  3. System writes an audit entry (admin, timestamp, cause, chosen route, reason), and the admin's decision resolves the `supportRequired` marker with an audited resolution.
- **Payment placeholder**: Paid amounts, refunds, and provider payouts for a treatment interrupted by a provider fault are handled under the payment placeholder; exact mechanics are defined later in FR-007, FR-007B, and FR-017.
- **Outcome**: The patient either continues on the same booking in `Aftercare` with a new aftercare provider or team, or the booking and inquiry are `Cancelled` with the admin's reason.
- **Boundary**: The provider-fault transfer with a new acceptance (B5) is never used for an `In Progress` booking. Distinct from the provider-requested Cancel/Close Case in FR-010.

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
| Pre-Scheduled Appointment | datetime | Yes | Appointment selected by the accepted subquote | Read-only; the booking's current appointment (the accepted appointment unless an admin changed it on Screen 8) |
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
| Total Amount | number | Yes | Booking total: the accepted price after promotion | Read-only; from acceptance snapshot |
| Deposit Amount | number | Yes | Calculated deposit (admin-configurable %, default 20-30%) | Within configured bounds |
| Deposit Percentage | text | Yes | Display deposit percentage used | Read-only; for transparency |
| Remaining Balance | number | Yes | Total - Deposit | Calculated automatically |
| Payment Option | select | Yes | Full payment or Installments (2–9) | Feasible installment options based on FR-029 split payment settings and FR-007B schedule rules (completion ≥30 days before procedure) |
| Installment Plan | select | Conditional | Number of installments if selected | Only shown if installment option selected |
| Currency | text | Yes | Payment currency and locked exchange-rate context | Read-only; from acceptance snapshot |
| Cancellation Policy | text | Yes | Policy summary with refund schedule | Read-only; admin-configured |
| Cancellation Policy Ack | checkbox | Yes | User acknowledges policy | Must be checked before payment |
| Terms & Conditions Ack | checkbox | Yes | User acknowledges T&C | Must be checked before payment |
| Contact Support | button | Yes | Opens a support request to cancel or change the booking | Always shown; there is no in-app cancel action after acceptance |

**Blocked State (Inquiry Cancelled)**:

If pre-booking validation fails (parent inquiry cancelled, by the patient before acceptance per FR-003 Workflow 5 or by an admin after acceptance), this screen displays a read-only blocked state instead of the payment form:

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
- If the booking is `Payment Window Expired` or `Cancelled` for any other cause (provider withdrawal or fault, provider suspension or deactivation), the screen shows the same read-only blocked layout with a banner that names the cause; all payment fields and actions are hidden.
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
| Procedure Date | datetime | Yes | Confirmed appointment slot | Read-only; the booking's current appointment (the accepted appointment unless an admin changed it on Screen 8) |
| Procedure Time | time | Yes | Appointment start time | Read-only; the booking's current appointment (the accepted appointment unless an admin changed it on Screen 8) |
| Treatment Type | text | Yes | Inherited treatment name (FUE, FUT, etc.) | Read-only; from parent snapshot |
| Total Amount | number | Yes | Total booking amount | Read-only; from accepted subquote snapshot |
| Currency | text | Yes | Currency of the accepted price | Read-only; from acceptance snapshot |
| Deposit Paid | number | Yes | Deposit amount paid | Read-only; from payment |
| Payment Status | badge | Yes | Deposit paid / Installments scheduled / Full paid | Must reflect latest payment state |
| Remaining Balance | number | Yes | Amount remaining to pay | Calculated automatically |
| Next Payment Due | datetime | Conditional | Next installment due date | Only shown if installments active |
| Payment Method | text | Yes | Payment method used | Read-only; from payment |
| Cancellation Policy | link | Yes | Link to full cancellation policy | Read-only |
| Contact Support | button | Yes | Opens a support request for cancellation or other booking changes | Always shown; there is no in-app cancel action after acceptance |

**Business Rules**:

- Trigger notifications to patient/provider upon display.
- Display all booking details clearly with appointment slot prominently shown.
- Show payment status and next steps (if installments, show schedule).
- Provide "Add to Calendar" functionality (ICS file download).
- Link to travel booking (FR-008) when available.

**Notes**:

- This screen appears immediately after successful payment.
- All data continues from the accepted subquote snapshot and the payment record.
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
| Total Amount | number | Yes | Accepted price and currency | Sortable; from acceptance snapshot |
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
- FR-005 prevents a second acceptance from acquiring a slot already held or blocked by another pending or confirmed booking. FR-006 revalidates exclusive hold ownership before payment initiation and, after successful payment, atomically creates the appointment record and converts that hold into the confirmed calendar block.

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
| Appointment Date | datetime | Yes | Appointment slot | Read-only; the booking's current appointment (the accepted appointment unless an admin changed it on Screen 8) |
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
| Treatment Plan (per-day) | table | Yes | Day-by-day treatment plan shown as relative days (Day 1, Day 2...) | Read-only; accepted subquote snapshot; never converted to calendar dates |

**Section 6: Pricing & Payment Information** (from FR-004, FR-006, FR-007):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Currency | text | Yes | Payment currency and locked exchange-rate context | Read-only; acceptance snapshot |
| Offered Price | number | Yes | Offered price of the accepted subquote, as entered before any promotion | Read-only; acceptance snapshot |
| Promotion Applied | group | No | Structured promotion included in the accepted price | Read-only; acceptance snapshot |
| Accepted Price | number | Yes | Booking total: the accepted price after promotion | Read-only; acceptance snapshot |
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
| Total Amount | number | Yes | Accepted price and currency | Sortable; from acceptance snapshot |
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
| Booking Status | badge | Yes | Current status | Read-only; changed only through the governed intervention actions below (revive, cancel, provider-fault transfer) |
| Booking Created Date | datetime | Yes | Booking creation timestamp | Read-only |
| Appointment Date | datetime | Yes | Current appointment slot | Read-only; changed only through Change Appointment (Screen 8) |
| Appointment Time | time | Yes | Current appointment start time | Read-only; changed only through Change Appointment (Screen 8) |

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
| Treatment Plan (per-day) | table | Yes | Day-by-day treatment plan shown as relative days (Day 1, Day 2...) | Read-only; accepted subquote snapshot; never converted to calendar dates |

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
| Offered Price | number | Yes | Offered price of the accepted subquote, as entered before any promotion | Read-only; acceptance snapshot |
| Promotion Applied | group | No | Structured promotion included in the accepted price | Read-only; acceptance snapshot |
| Accepted Price | number | Yes | Booking total: the accepted price after promotion | Read-only; acceptance snapshot |
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
| Revive Booking | button | Booking is `Payment Window Expired` | Opens Screen 7; revives the booking to `Accepted` only (mandatory reason; guarded per Admin Status and Date Intervention rules) |
| Change Appointment | button | Booking is `Accepted` or `Confirmed` | Opens Screen 8; changes the appointment date/time (mandatory reason and slot availability check), sends `booking.rescheduled`, and triggers an FR-008 travel-date review for any linked travel records |
| Cancel Booking | button | Booking is `Accepted`, `Payment Window Expired`, `Confirmed`, `In Progress`, or `Aftercare` | Opens Screen 9; cancels the booking on an admin decision or a support-routed patient request (mandatory reason) |
| Start Provider-Fault Transfer | button | Booking is `Accepted` or `Confirmed` with a provider fault (withdrawal, drop-out, or provider-status cancellation with `supportRequired`); never shown for `In Progress` or `Aftercare` | Opens Screen 10; cancels the original booking with the provider-fault cause if not already cancelled, and assigns a replacement provider through an admin-authored replacement quote |
| Resolve In-Progress Provider Fault | button | Booking is `In Progress` with a provider fault and `supportRequired` | Opens Screen 11; the admin either moves the booking to `Aftercare` and reassigns the aftercare provider through FR-011 Screen 19, or cancels the booking through Screen 9 (Alternative Flow B7) |
| Reassign Aftercare | link | Booking is `Aftercare` with a provider fault or `supportRequired` | Opens the FR-011 aftercare reassignment screen for this booking's aftercare case (Alternative Flow B6) |
| Change Treatment Details | link | Booking is `Confirmed`, `In Progress`, `Aftercare`, or `Completed` | Opens the FR-010 Change Treatment Details screen (FR-010 Screen 9) for plan days, clinician set, and estimated graft count; mandatory reason, audit entry, and `treatment.plan_changed` |
| Process Refund | button | Booking cancelled or eligible | Process refund per cancellation policy (payment placeholder; mechanics in FR-007, FR-007B, and FR-017) |
| Add Internal Note | button | Always | Add admin-only note |
| View Inquiry | link | Always | Open full inquiry details (FR-003) |
| View Accepted Selection | link | Always | Open accepted subquote and AcceptanceEvent details (FR-005) |
| View Parent Quote | link | Always | Open source parent quote details (FR-004) |
| View 3D Scan | link | Always | Open 3D scan viewer |
| View Medical Questionnaire | link | Always | Open medical questionnaire |

**Business Rules**:

- Admin has full visibility to all patient and provider information (no masking).
- Admin can revive a `Payment Window Expired` booking, change an appointment, cancel a booking, start the provider-fault transfer, resolve an `In Progress` provider fault, and open the aftercare reassignment only through the actions above and under the Admin Status and Date Intervention rules, each with a mandatory reason. No other manual status change is allowed; the Booking Status field is never edited directly.
- Dispute resolution uses only these governed actions; there is no separate status-override action.
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

#### Screen 7: Revive Booking (Admin Modal)

**Purpose**: Revive a `Payment Window Expired` booking to `Accepted` with a new slot hold, opened from Screen 6 Revive Booking.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Booking Reference | text | Yes | Booking being revived | Read-only |
| Current Status | badge | Yes | Must be `Payment Window Expired` | Read-only; action unavailable for any other status |
| Appointment | datetime | Yes | Booking's current appointment date/time and time zone | Read-only; slot availability is re-checked on confirm |
| Promotion Use Check | indicator | Conditional | Shown when the accepted promotion has a usage limit; states whether one use can be taken again | Read-only; revive blocked when the limit has no room |
| New Payment Deadline | datetime | Yes | Revive time plus the FR-026 slot-hold duration | Read-only; calculated |
| Reason | textarea | Yes | Why the booking is revived | Mandatory; 10 to 500 characters |
| Confirm | checkbox | Yes | Admin confirms the revive and the new hold | Must be checked before submit |

**Business Rules**:

- On submit, System re-checks that the slot is free and that the promotion limit has room; if either check fails, the revive is rejected with the reason shown and nothing changes.
- On success, the booking returns to `Accepted`, a new hold of the FR-026 duration starts, and the AcceptanceEvent and snapshot stay unchanged.
- Audit entry: admin, timestamp, reason, old and new status, new hold expiry.
- Resulting notice: the mandatory `booking.revived` notice to the patient (with the new payment deadline) and the provider.

#### Screen 8: Change Appointment (Admin Modal)

**Purpose**: Change the appointment date/time of an `Accepted` or `Confirmed` booking, opened from Screen 6 Change Appointment.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Booking Reference | text | Yes | Booking being changed | Read-only |
| Current Appointment | datetime | Yes | Booking's current appointment date/time and time zone | Read-only |
| Accepted Appointment | datetime | Yes | Appointment captured in the acceptance snapshot | Read-only; never changed |
| New Appointment Date | date | Yes | New appointment date | Required; must differ from the current appointment; not in the past |
| New Appointment Time | time | Yes | New appointment start time | Required; in the provider's time zone |
| Reason | textarea | Yes | Why the appointment changes | Mandatory; 10 to 500 characters |
| Travel Review Notice | indicator | Conditional | Shown when travel records are linked; states that an FR-008 travel-date review will be raised | Read-only |
| Confirm | checkbox | Yes | Admin confirms the change | Must be checked before submit |

**Business Rules**:

- Available only while the booking is `Accepted` or `Confirmed`.
- On submit, System checks that the new provider date/time and time zone are free and rejects the change if not; the hold (for `Accepted`) or calendar block (for `Confirmed`) moves only on success. An `Accepted` booking keeps its original hold expiry.
- The booking's current appointment is updated; the acceptance snapshot keeps the accepted appointment as the baseline. Booking notices read the booking's current appointment.
- Audit entry: admin, timestamp, reason, old and new appointment.
- Resulting notice: the mandatory `booking.rescheduled` notice to the patient and the provider, with the old and new appointment. Linked travel records get an FR-008 travel-date review.

#### Screen 9: Cancel Booking (Admin Modal)

**Purpose**: Cancel a booking on an admin decision or on a patient request received through support, opened from Screen 6 Cancel Booking (Alternative Flows B2 and B3).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Booking Reference | text | Yes | Booking being cancelled | Read-only |
| Current Status | badge | Yes | Source booking state | Read-only; must be `Accepted`, `Payment Window Expired`, `Confirmed`, `In Progress`, or `Aftercare` |
| Request Source | select | Yes | Patient request through support, or admin decision | Required |
| Support Ticket Reference | text | Conditional | Support case that carries the patient's request | Required when Request Source is patient request |
| Reason | textarea | Yes | Cancellation reason shown to the patient and provider | Mandatory; 10 to 500 characters |
| Effects Summary | text | Yes | States that the booking and inquiry become `Cancelled`, the accepted quote stays `accepted`, any hold or calendar block is released, and refunds follow the payment placeholder | Read-only |
| Confirm | checkbox | Yes | Admin confirms the cancellation | Must be checked before submit |

**Business Rules**:

- Only an admin can cancel a booking; the patient has no in-app cancel action from acceptance onward.
- On submit, the booking becomes `Cancelled` with the reason as its cancellation reason, the inquiry becomes `Cancelled`, the accepted quote stays `accepted`, the AcceptanceEvent stays unchanged with no supersession record, and any hold or calendar block is released.
- Audit entry: admin, timestamp, source state, request source, support ticket reference, reason.
- Resulting notice: `booking.cancelled` to the patient and the provider, including the reason.
- Refunds and fees follow the payment placeholder (FR-007, FR-007B, and FR-017).

#### Screen 10: Provider-Fault Transfer and Replacement Quote (Admin)

**Purpose**: Move a patient to a replacement provider in the same inquiry after a provider fault, through an admin-authored replacement quote and a new admin-authored acceptance (Alternative Flow B5), opened from Screen 6 Start Provider-Fault Transfer.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Original Booking | text | Yes | Booking reference, provider, status, and cause | Read-only |
| Fault Type | select | Conditional | Provider withdrawal or provider drop-out | Required when the booking is not already cancelled by the provider-status cascade; prefilled as `ProviderSuspended` or `ProviderDeactivated` otherwise |
| Replacement Provider | search select | Yes | Provider who takes over the patient | Required; must be active and not the original provider |
| Replacement Quote | form | Yes | Quote for the replacement provider in the same inquiry, using the FR-004 quote fields (treatment, package, options, date-price rows with appointment, price, and currency) | Required; validated as an FR-004 quote; authored by the admin |
| Selected Option and Date-Price Row | select | Yes | The option and date-price row that becomes the replacement acceptance | Required; exactly one; the appointment slot must be free |
| Adjustment Reason | textarea | Yes | Why the package or price differs from the original accepted selection | Mandatory; 10 to 500 characters |
| Paid Amount Carry-Over | text | Yes | Amounts already paid on the original booking | Read-only; handled under the payment placeholder |
| Confirm | checkbox | Yes | Admin confirms the transfer | Must be checked before submit |

**Business Rules**:

- Available only for `Accepted` or `Confirmed` bookings with a provider fault, including bookings already cancelled by the provider-status cascade with `supportRequired`. An `In Progress` provider fault uses Screen 11 instead.
- The replacement quote is authored through FR-004 Workflow 7 and FR-004 Screen 8. If no replacement acceptance is recorded, the replacement quote expires under the normal FR-004 quote expiry; the inquiry stays `supportRequired` and is not cancelled automatically, and the admin may author another replacement quote or cancel the inquiry and booking through Screen 9.
- If the original booking is not yet cancelled, submit first cancels it with cause `ProviderFault` and releases its hold or calendar block.
- On submit, System saves the replacement quote, creates the admin-authored AcceptanceEvent that points to the selected replacement quote, option, and date-price row, writes the single FR-005 supersession record linking the original AcceptanceEvent to the new one, acquires the replacement slot hold, and creates the replacement booking in `Accepted`. The admin-authored replacement quote is the only quote that may be created after an inquiry has an acceptance.
- Audit entry: admin, timestamp, fault type, replacement provider, replacement quote reference, selected option and row, adjustment reason; the `supportRequired` marker is resolved with an audited resolution.
- Resulting notices: `booking.provider_fault_replacement` to the patient and admin; `booking.scheduled` to the patient with the replacement payment deadline; `quote.accepted` (outcome `selected_subquote_accepted`) to the replacement provider.

#### Screen 11: Resolve In-Progress Provider Fault (Admin Modal)

**Purpose**: Record the admin's case-by-case decision for a provider fault while the booking is `In Progress` (Alternative Flow B7), opened from Screen 6 Resolve In-Progress Provider Fault.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Booking Reference | text | Yes | Booking, provider, and current treatment day | Read-only |
| Current Status | badge | Yes | Source booking state | Read-only; must be `In Progress` with `supportRequired` |
| Fault Cause | text | Yes | `ProviderFault`, `ProviderSuspended`, or `ProviderDeactivated` | Read-only |
| Resolution Route | radio | Yes | Move to Aftercare and reassign the aftercare provider, or cancel the booking | Exactly one |
| Reason | textarea | Yes | Why the admin chose this route | Mandatory; 10 to 500 characters |
| Effects Summary | text | Yes | For Move to Aftercare: the booking becomes `Aftercare`, the treatment record is kept as recorded, and FR-011 Screen 19 opens for the reassignment. For Cancel: Screen 9 opens with the reason prefilled | Read-only |
| Confirm | checkbox | Yes | Admin confirms the decision | Must be checked before submit |

**Business Rules**:

- No replacement quote and no replacement acceptance are offered on this screen; the provider-fault transfer (Screen 10) is limited to bookings before treatment starts.
- Move to Aftercare: on submit, System moves the booking from `In Progress` to `Aftercare` and opens FR-011 Screen 19, where the admin assigns the new aftercare provider or the Hairline aftercare team (Alternative Flow B6); FR-011 sends `aftercare.provider_reassigned` to the patient and the new aftercare provider.
- Cancel: on submit, System opens Screen 9; the cancellation follows Alternative Flow B2 and sends `booking.cancelled`.
- Audit entry: admin, timestamp, fault cause, chosen route, reason; the `supportRequired` marker is resolved with an audited resolution.
- Money stays with the payment placeholder (FR-007, FR-007B, and FR-017).

---

## Business Rules

### General Module Rules

- Booking is confirmed only after successful deposit or first installment charge.
- Appointment slot is selected by the accepted subquote and held for payment; no additional slot selection is permitted.
- Provider calendars must be accurate; confirmed bookings auto-block times at database level; overlapping appointments are prevented.
- All timestamps shown in patient's local timezone; provider view shows both local and clinic time.
- **Overlapping Appointment Prevention**: FR-005 atomically acquires an exclusive slot hold when acceptance is created. A second acceptance for a held or blocked slot is rejected before any AcceptanceEvent or booking handoff is created. Exclusivity is enforced by a uniqueness rule on active holds (provider, appointment date/time, and time zone), so a concurrent second acceptance for the same slot fails and the patient is told the slot was just taken. FR-006 verifies hold ownership before payment and converts the hold into a confirmed calendar block on payment success; stale or invalid handoffs are rejected before the payment gateway is called.

### Data & Privacy Rules

- Patient identity remains masked to provider until booking is Confirmed (payment success).
- Booking, payment, and personal data are encrypted at rest and in transit; audit logs are immutable.
- Retain booking and financial records ≥7 years; hard deletes prohibited (soft-delete/archive only).

### Admin Editability Rules

**Editable by Admin** (via A-09: System Settings & Configuration):

- **Deposit Rate**: Admin MUST be able to configure deposit percentage (default range: 20-30% of total booking amount) via **FR-029: Payment System Configuration**. This is configurable per provider or globally. Changes apply to new bookings only (existing bookings retain original deposit rate).
- Cancellation policy schedule (thresholds and refund percentages).
- Slot-hold duration and the "hold expiring soon" reminder lead time are owned by **FR-026** (versioned and audited; hold default 48 hours). FR-006 consumes them and has no separate hold setting.
- Notification templates for booking confirmations/reminders; booking confirmation content (configured via **FR-030: Notification Rules & Configuration**).
- Commission settings (FR-029); commission is fixed at booking confirmation.

**Confirmed Booking Data Integrity (Admin Override)**:

- Confirmed bookings are **read-only for patients and providers**.
- Admins MAY perform emergency modifications limited to the Admin Status and Date Intervention rules below, but MUST do so as **append-only, versioned intervention events** (who/when/what/why) rather than overwriting historical records.
- Financial transactions (payments/refunds) remain immutable once confirmed; admin actions reference the original transaction IDs and create new adjustment/refund events as needed.

**Admin Status and Date Intervention Rules**:

- **Revive `Payment Window Expired`**: Admin MAY move a booking from `Payment Window Expired` back to `Accepted` only with a mandatory reason. The system re-checks that the slot (provider, appointment date/time, and time zone) is free and rejects the revive if it is not. On success, a new hold of the FR-026 slot-hold duration starts at the revive time. If the accepted promotion has a usage limit, the revive needs one use again: a provider-selected promotion or patient code re-reserves one use, and an automatic promotion takes one use again. The system rejects the revive if the limit has no room. The action is audited, the AcceptanceEvent and snapshot stay unchanged, and the system sends the mandatory "booking revived" notice to the patient (with the new payment deadline) and to the provider (slot held again).
- **Change appointment date/time**: Allowed only for `Accepted` or `Confirmed` bookings with a mandatory reason (Screen 8). The system checks that the new provider date/time and time zone are free and rejects the change if not; the hold or calendar block moves only on success. The booking's current appointment changes; the acceptance snapshot keeps the accepted appointment as the baseline, and booking notices read the booking's current appointment. The change is audited, sends the mandatory `booking.rescheduled` notice to the patient and the provider with the old and new appointment, and triggers an FR-008 travel-date review for any travel records already linked to the booking.
- **Cancel booking**: Only an admin cancels a booking, from `Accepted`, `Payment Window Expired`, `Confirmed`, `In Progress`, or `Aftercare`, with a mandatory reason, a confirmation, and an audit entry (Screen 9; Alternative Flow B2). The booking and the inquiry become `Cancelled`, the accepted quote stays `accepted`, and `booking.cancelled` is sent to the patient and the provider. Patient requests to cancel after acceptance reach the admin through support.
- **Provider-fault transfer**: Only an admin starts the transfer and authors the replacement quote (Screen 10; Alternative Flow B5), with a mandatory reason and audit entry.
- **Aftercare reassignment**: A provider fault during `Aftercare` is handled by the FR-011 aftercare reassignment (Alternative Flow B6); the booking status does not change.
- **In-Progress provider fault**: A provider fault while the booking is `In Progress` keeps the booking `In Progress` with `supportRequired`; only an admin resolves it on Screen 11 (Alternative Flow B7), either by moving the booking to `Aftercare` and reassigning the aftercare provider through FR-011 Screen 19, or by cancelling the booking through Screen 9, with a mandatory reason and audit entry.
- **No other status jumps**: Admin cannot set any other booking status manually. All other transitions follow the governed flows (payment, admin cancellation, FR-010 treatment progress, provider-status cascade, provider-fault transfer, and the In-Progress provider-fault move to `Aftercare`).

**Fixed in Codebase (Not Editable)**:

- Password policy and OTP length; identity unmasking rule tied to payment confirmation.
- Audit logging enablement and retention guarantees.
- Overlapping appointment prevention logic (enforced at database level).

**Configurable with Restrictions**:

- Payment options availability per region/currency (cannot alter gateway compliance requirements).

### Payment & Billing Rules

- **Deposit Rate**: Deposit percentage is admin-configurable (default: 20-30% of total). Admin can set different rates per provider or use global default. Deposit and installment settings are locked at booking confirmation (FR-029).
- Deposit required to confirm booking; final payment per FR-007 schedule.
- Installments must complete ≥30 days before procedure; failures trigger retries, then flag for admin.
- **Post-Acceptance Hold**: Subquote acceptance places one temporary exclusive hold keyed by provider, appointment date/time, and time zone. The hold blocks other patients from that slot for the FR-026 slot-hold duration (default 48 hours), which starts at acceptance. The hold is fixed: payment failure or retry never extends or restarts it. The patient must complete the first payment step (deposit or first installment) before the hold expires. The appointment record is created only on successful payment; if the hold expires, it is released and no appointment exists.
- **Hold Expiring Soon**: Before the hold expires, the patient receives a "hold expiring soon" reminder; the lead time is set by admin in FR-026.
- **Payment Window Expired**: Hold expiry moves the pending booking from `Accepted` to `Payment Window Expired`: the hold is released, payment is disabled, the AcceptanceEvent/snapshot remain immutable, neither the parent quote nor accepted subquote is reopened, and the mandatory Payment Window Expired notice goes to patient and provider. The outcome is final for that accepted selection except for the audited admin revive (Admin Status and Date Intervention Rules).
- **Payment Window Expired Recovery**: The patient contacts support; an admin either performs the audited revive (Screen 7) or cancels the booking (Screen 9), after which the patient may start a new inquiry. One acceptance per inquiry still applies.
- **First-Payment Boundary**: `Payment Window Expired` applies only to the first payment step (acceptance to deposit or first installment). A missed later installment or final payment never causes `Payment Window Expired`, booking cancellation, or inquiry cancellation; it is handled by FR-007 and FR-007B.
- **Payment Failure Handling**:
  - If the first payment fails, Payment Service applies retry policy per FR-007 (exponential backoff) and surfaces failures for patient action when needed.
  - The patient can retry payment from the Accepted Subquote view only while the original hold is active.
  - If no payment succeeds before the hold expires, the hold is released, further payment against it is blocked, and the booking becomes `Payment Window Expired`.
- Refunds per cancellation policy example in `system-prd.md`. Provider withdrawal or drop-out after acceptance follows Alternative Flow B5 and its payment placeholder before treatment starts, or Alternative Flow B7 while `In Progress`; the patient pays no cancellation fee.
- **Provider-Status Cancellation**: Bookings cancelled by an effective provider suspension/deactivation (Alternative Flow B4) are rehomed by admin to a replacement provider in the same inquiry through the Alternative Flow B5 transfer. Its payment placeholder applies: paid amounts move with the patient as credit, any unused part is refunded, and the patient pays no fee; exact mechanics are defined later in FR-007, FR-007B, and FR-017. Provider eligibility is revalidated at booking-confirming payment (FR-015 Rule 9). A payment captured while suspension/deactivation becomes effective is recorded and treated as paid money under the B5 payment placeholder; it never confirms or revives the booking.
- Prices shown in patient's currency; exchange rate locked in the subquote acceptance snapshot; payouts use that locked rate.
- **Promotion and Commission**: The promotion and accepted price are frozen at subquote acceptance and never change in FR-006, except through a new linked acceptance record in Alternative Flow B5. Commission is fixed at booking confirmation on the accepted price after promotion, in the quote currency, read from the acceptance snapshot (FR-029). The commission figure shown on the FR-004 quote screen is indicative only.

### Rescheduling Rules

- **Rescheduling is deferred to V2**: The provider pre-schedules the appointment in the subquote; acceptance fixes the chosen appointment and reserves its slot, and successful payment confirms the booking. Rescheduling functionality will be evaluated for V2 based on business needs.
- **Current Behavior**: The patient cannot reschedule. Date changes require the audited admin appointment change (Screen 8), which sends `booking.rescheduled`, or an admin cancellation per cancellation policy.

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
- **FR-004 / Module PR-02**: Quote Submission; provides the Option/date-price records that carry the pre-scheduled appointment and price.
- **FR-005 / Module P-02**: Subquote Comparison & Acceptance; supplies the immutable accepted subquote and inherited parent snapshot and triggers booking entry.
- **FR-007 & FR-007B / Modules P-03, S-02**: Payments and Installments; deposit capture, schedules, refunds.
- **FR-020 / S-03**: Notifications; confirmations, reminders, and alerts.
- **FR-030 / Module A-09**: Notification Rules & Configuration; booking confirmation/reminder templates and notification policy rules consumed by S-03, including the events FR-006 triggers (`booking.scheduled`, `booking.hold_expiring_soon`, `booking.payment_window_expired`, `booking.revived`, `booking.rescheduled`, `booking.cancelled`, `booking.provider_fault_replacement`). FR-004 produces `quote.withdrawn`; FR-006 reacts to it by starting the provider-fault transfer.
- **FR-026 / Module A-09**: App Settings & Security; owns the slot-hold duration (default 48 hours) and the "hold expiring soon" reminder lead time.
- **FR-010 / PR-03**: Post-confirmation treatment execution starts on arrival.
- **FR-011 / Module A-03**: Aftercare & Recovery Management; owns the aftercare reassignment screen used when a provider fault occurs during `Aftercare` (Alternative Flow B6).
- **FR-029 / Module A-09**: Payment System Configuration; deposit, split payment, and commission settings are managed here (deposit default 20-30% range; installment options and cutoff rules; commission default 15-25% range, per-provider or global settings).

### External Dependencies (APIs, Services)

- Payment processor for deposits/installments/refunds (PCI compliant); retry with backoff within the fixed post-acceptance hold; failure never extends the hold.
- Calendar/ICS generation for add-to-calendar links.

### Data Dependencies

- Active provider calendars with pre-scheduled slots from FR-004 Option/date-price records (PR-02).
- FR-005 AcceptanceEvent with accepted subquote/parent identifiers and versions, complete snapshot, locked currency/exchange rate, and promotion data (FR-004/FR-019).
- Patient verified profile and medical status flags (P-01/P-02) for provider readiness.

---

## Assumptions

### User Behavior Assumptions

- Patients complete the first payment within the post-acceptance slot-hold window (default 48 hours).
- Patients understand and accept cancellation terms before paying.
- Majority use mobile; need clear time zone handling.

### Technology Assumptions

- Patient devices support secure payments and push notifications.
- Provider/admin access via modern browsers; stable connectivity expected at clinics.
- Notification service can deliver emails/push near real-time.

### Business Process Assumptions

- Providers maintain accurate calendars and honor confirmed slots.
- Admins process edge-case cancellations within published SLAs.
- Promotion and accepted price are frozen at subquote acceptance; commission is fixed at booking confirmation on the accepted price after promotion (the FR-004 quote-screen commission figure is indicative).

---

## Implementation Notes

### Technical Considerations

- Idempotent booking creation with slot holds to prevent race conditions; atomic confirm and appointment-record creation on payment success.
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

Patient's first payment fails; the original post-acceptance hold stays in place without extension; patient retries payment before the hold expires.

**Why this priority**: Critical for conversion and user experience.

**Independent Test**: Accept a subquote, simulate payment failure, verify the hold expiry time is unchanged, retry payment, confirm booking.

**Acceptance Scenarios**:

1. Given an accepted subquote whose hold started at acceptance, When the first payment fails and the patient retries before the hold expires, Then the hold expiry time is unchanged, the retry runs against the same immutable selection, and on success the booking confirms and the appointment record is created.
2. Given no successful payment when the hold expires, When the hold is released, Then the booking becomes `Payment Window Expired`, no appointment record exists, payment against that selection is blocked, the acceptance snapshot remains immutable, and patient and provider receive the Payment Window Expired notice.
3. Given a confirmed booking on an installment plan, When a later installment is missed, Then the booking does not become `Payment Window Expired` and the inquiry is not cancelled; FR-007B handles the missed installment.
4. Given a `Payment Window Expired` booking, When an admin revives it with a reason and the slot and promotion usage are still available, Then the booking returns to `Accepted` with a new hold, the action is audited, the AcceptanceEvent is unchanged, and patient and provider receive the "booking revived" notice; if the slot or promotion usage is unavailable, the revive is rejected.

---

### User Story 3 - Overlapping Appointment Prevention (Priority: P1)

Two patients attempt to accept subquotes for the same appointment slot; the first atomic acceptance acquires the exclusive hold and the second acceptance is rejected before creating another accepted selection.

**Why this priority**: Prevents double-booking and ensures calendar integrity.

**Independent Test**: Submit concurrent acceptance requests for the same slot; verify exactly one exclusive hold, one AcceptanceEvent, and one booking handoff are created, while the rejected request leaves its quote and inquiry state unchanged.

**Acceptance Scenarios**:

1. Given two concurrent acceptance attempts for the same slot, When the atomic reservation check runs, Then exactly one attempt acquires the hold and creates an AcceptanceEvent; the other fails on the active-hold uniqueness rule and that patient is told the slot was just taken.
2. Given a slot already held or blocked by another pending or confirmed booking, When a patient attempts acceptance, Then acceptance is rejected before quote/inquiry state changes, AcceptanceEvent creation, booking handoff, or payment initiation.

---

### User Story 4 - Apply Cancellation Policy (Priority: P2)

A late cancellation performed by an admin at the patient's request applies the refund schedule; provider withdrawal or drop-out after acceptance follows the provider-fault transfer in Alternative Flow B5 before treatment starts, or the admin decision in Alternative Flow B7 while `In Progress`.

**Why this priority**: Protects trust and platform economics.

**Independent Test**: Trigger an admin cancellation on a patient's support request and a provider withdrawal; verify the policy refund for the cancellation, the Alternative Flow B5 transfer route for the provider withdrawal, and the audit logs.

**Acceptance Scenarios**:

1. Given a confirmed booking and a patient cancellation request received through support, When an admin cancels the booking <15 days prior with a reason on Screen 9, Then the booking and inquiry become `Cancelled`, the accepted quote stays `accepted`, the action is audited, `booking.cancelled` is sent, and the refund follows the policy under the payment placeholder.
3. Given a confirmed booking, When the patient opens the booking, Then no in-app cancel action is shown and a "Contact support" action is shown instead.
2. Given a confirmed booking, When the provider withdraws or drops out, Then the booking is cancelled with cause `ProviderFault`, an admin can transfer the patient to a replacement provider in the same inquiry through an admin-authored replacement quote and a new admin-authored acceptance, the single supersession record linking the original AcceptanceEvent to the new one is written at the replacement acceptance, and the patient pays no cancellation fee.
4. Given an `Aftercare` booking, When the provider drops out of aftercare, Then the booking stays `Aftercare`, no new acceptance or payment is created, and an admin reassigns the aftercare provider or team through FR-011.

### Edge Cases

- Payment succeeds but confirmation email fails: confirmation must still be visible in-app; retry email.
- A stale or forged booking handoff references a slot not exclusively held by its AcceptanceEvent: reject it before payment initiation and leave the valid reservation unchanged.
- Installment plan default before deadline: flag booking, notify admin and patient; apply policy.
- Provider emergency closure after acceptance: handled as provider fault; before treatment starts the admin transfers the patient to a replacement provider in the same inquiry (Alternative Flow B5); while `In Progress` the admin moves the booking to `Aftercare` with an aftercare reassignment or cancels it (Alternative Flow B7).
- Provider suspended or deactivated while the patient is paying: the booking-confirming payment step revalidates provider eligibility and rejects the payment before the gateway is called. If a capture still completes concurrently, record it, keep the booking `Cancelled` with the provider-status cause and `supportRequired`, and treat the captured amount as paid money that moves with the patient under the B5 payment placeholder when the admin rehomes the patient (Alternative Flows B4 and B5).
- Payment failure after subquote acceptance: the single hold that started at acceptance (FR-026 duration, default 48 hours) is never extended; retry is allowed only while it is active; on expiry, set `Payment Window Expired`, release the hold, block payment against that selection, and do not reopen the parent quote or accepted subquote.
- Two patients attempt to accept subquotes with the same slot simultaneously: the atomic acceptance transaction creates one exclusive hold and one AcceptanceEvent; the losing attempt receives a clear unavailable-slot error and creates no booking handoff.
- Patient submits payment while inquiry is being cancelled concurrently: system MUST perform atomic pre-booking validation at payment submission time (not just at screen entry). If inquiry transitions to "Cancelled" between screen load and payment submission, payment MUST be rejected with message "This inquiry has been cancelled" and no charge processed. Payment gateway must not be called if inquiry is cancelled.
- Patient is on Screen 1 when inquiry cancellation notification arrives: system SHOULD use real-time push (WebSocket/SSE) to transition Screen 1 to blocked state without requiring page refresh.

---

## Functional Requirements Summary

### Core Requirements

- **REQ-006-001**: Patients MUST be able to proceed to payment after accepting one subquote; FR-006 MUST consume its package, date range, appointment, price, promotion, and inherited parent context without reselection.
- **REQ-006-002**: System MUST confirm booking only after successful deposit/initial installment and unmask patient identity to provider.
- **REQ-006-003**: System MUST require an exclusive appointment hold, keyed by provider, appointment date/time, and time zone, created atomically with FR-005 acceptance; reject any handoff that does not own the valid hold before payment initiation; and create the appointment record and convert the hold into a provider calendar block only after successful payment confirmation.
- **REQ-006-004**: System MUST enforce cancellation policy with scheduled refunds per policy (rescheduling deferred to V2). Only an admin MAY cancel a booking, from `Accepted`, `Payment Window Expired`, `Confirmed`, `In Progress`, or `Aftercare`, with a mandatory reason, confirmation, and audit entry; the booking and inquiry MUST become `Cancelled`, the accepted quote MUST stay `accepted`, and `booking.cancelled` MUST be sent. The patient MUST NOT have an in-app cancel action from acceptance onward and MUST be offered "Contact support" instead.
- **REQ-006-005**: System MUST hold the accepted subquote's appointment slot with one fixed hold that starts at subquote acceptance and lasts the FR-026 slot-hold duration (default 48 hours); payment failure MUST NOT extend or restart it. If the hold expires before the first payment succeeds, System MUST set the booking to `Payment Window Expired`, release the hold, create no appointment record, block payment against that accepted selection, and preserve the immutable AcceptanceEvent/snapshot without reopening the prior parent quote or accepted subquote. Recovery is by the audited admin revive, or by admin cancellation on a support request followed by a new inquiry.
- **REQ-006-015**: When a provider's suspension or deactivation becomes effective, System MUST cancel that provider's `Accepted` and `Confirmed` bookings with cause `ProviderSuspended` or `ProviderDeactivated` and an independent `supportRequired` marker, release holds/reservations/slots, block further payment, revalidate provider eligibility at booking-confirming payment, treat any racing capture as paid money under the B5 payment placeholder, retain the accepted snapshot and booking/payment history, write the supersession record only at the replacement acceptance, and let an admin rehome the patient to a replacement provider in the same inquiry through Alternative Flow B5, without restoration on reactivation (Alternative Flow B4; FR-015 A5/Screen 4). `In Progress` and `Aftercare` bookings MUST keep their status and receive the cause and `supportRequired` (Alternative Flows B7 and B6).
- **REQ-006-016**: `Payment Window Expired` MUST apply only to the first payment step (acceptance to deposit or first installment). A missed later installment or final payment MUST NOT cause `Payment Window Expired`, booking cancellation, or inquiry cancellation.
- **REQ-006-017**: Admin MAY revive a `Payment Window Expired` booking to `Accepted` only through Screen 7 with a mandatory reason, a slot availability re-check, a new hold of the FR-026 duration, one promotion use taken again where the accepted promotion has a usage limit (re-reserved for a provider-selected promotion or patient code, taken again for an automatic promotion; the revive is rejected if the limit has no room), an audit entry, an unchanged AcceptanceEvent, and a mandatory "booking revived" notice to patient and provider. Appointment date changes MUST be made through Screen 8, MUST pass a slot availability check, MUST update the booking's current appointment while the acceptance snapshot keeps the accepted baseline, MUST send `booking.rescheduled`, and MUST trigger an FR-008 travel review for any travel records already linked to the booking. No other manual status change is allowed.
- **REQ-006-018**: When the provider withdraws or drops out after acceptance and before treatment starts, System MUST cancel the booking with cause `ProviderFault`, release the hold or calendar block, keep the AcceptanceEvent unchanged, and let an admin transfer the patient to a replacement provider in the same inquiry through an admin-authored replacement quote and a new admin-authored acceptance that points to that quote, option, and date-price row (Alternative Flow B5, Screen 10; FR-004 Workflow 7 and Screen 8). A replacement quote that is not accepted MUST expire under the normal quote expiry, the inquiry MUST stay `supportRequired` without automatic cancellation, and the admin MAY author another replacement quote or cancel the inquiry and booking. System MUST write the single supersession record linking the original AcceptanceEvent to the new one at the replacement acceptance, as one append-only insert; the B4 or B5 closure is recorded on the booking as its cause. A provider fault during `Aftercare` MUST NOT create a new quote, acceptance, or payment; the booking stays `Aftercare` and an admin reassigns the aftercare provider or team through FR-011 (Alternative Flow B6); the replacement booking MUST receive the carried-over passport and copied flight and hotel records flagged "travel-date review required" per FR-008, with the originals kept read-only on the closed booking.
- **REQ-006-019**: When a provider fault occurs while the booking is `In Progress`, System MUST keep the booking `In Progress`, MUST NOT cancel it automatically or create a replacement quote or acceptance, and MUST flag it `supportRequired` with the cause. Only an admin MAY resolve it on Screen 11 (Alternative Flow B7), with a mandatory reason, confirmation, and audit entry, by either moving the booking to `Aftercare` and reassigning the aftercare provider or team through FR-011 Screen 19, or cancelling the booking through Screen 9.

### Data Requirements

- **REQ-006-006**: System MUST store booking reference, slot, status history, payment state, refund state, and audit trail ≥7 years.
- **REQ-006-007**: System MUST link each booking to exactly one FR-005 AcceptanceEvent, accepted parent quote identifier/version, accepted subquote identifier/version, immutable acceptance snapshot, and provider calendar slot. `acceptedSubquoteVersion` MUST equal `acceptedParentQuoteVersion`.

### Security & Privacy Requirements

- **REQ-006-008**: System MUST keep patient identity masked until payment confirmation; encrypt PII at rest and in transit.
- **REQ-006-009**: System MUST log all booking state changes and accesses with user, timestamp, and reason.

### Integration Requirements

- **REQ-006-010**: System MUST integrate with Payment Service for deposits, installments, and refunds, and MUST use the exchange rate locked in the acceptance snapshot without relocking it.
- **REQ-006-011**: System MUST integrate with Notification Service for confirmations, reminders, and policy notices, and MUST trigger these FR-030 events: `booking.scheduled` (displayed as "Booking Accepted — Slot Held (Pending Payment)"; mandatory, patient only, sent on patient acceptance and on an admin-authored replacement acceptance; the provider is told by `quote.accepted`), `booking.rescheduled` (mandatory, patient and provider, sent on an admin appointment change with the old and new appointment), `booking.cancelled` (patient and provider, sent on admin cancellation with the reason), `booking.hold_expiring_soon` (patient reminder, and admin exception alert), `booking.payment_window_expired` (mandatory, patient and provider, and admin exception alert), `booking.revived` (mandatory, patient and provider), and `booking.provider_fault_replacement` (mandatory, patient and admin exception alert). FR-004 is the only producer of `quote.withdrawn`; FR-006 does not emit it and reacts to it by starting the provider-fault transfer in Alternative Flow B5.

### Configuration Requirements

- **REQ-006-012**: Admin MUST be able to configure deposit percentage (default: 20-30% range) via **FR-029: Payment System Configuration** (Module A-09: System Settings & Configuration).
- **REQ-006-013**: System MUST read the slot-hold duration (default: 48 hours) and the "hold expiring soon" reminder lead time from FR-026 and MUST NOT keep a separate FR-006 hold setting.
- **REQ-006-014**: System MUST verify the parent inquiry is not in "Cancelled" status before allowing entry to the booking/payment flow. If cancelled, system MUST block entry and display a read-only blocked state (Screen 1 blocked state) with clear messaging.

### Marking Unclear Requirements

- None open for provider-fault routing: before treatment starts the transfer applies (Alternative Flow B5), while `In Progress` the admin decides case by case (Alternative Flow B7), and during `Aftercare` the aftercare reassignment applies (Alternative Flow B6).

---

## Key Entities

- **Entity 1 - Booking**: Represents a confirmed or pending booking derived from one accepted subquote and its inherited parent context.
  - **Key attributes**: booking reference, acceptanceEventId, acceptedParentQuoteId, acceptedParentQuoteVersion, acceptedSubquoteId, acceptedSubquoteVersion, acceptanceSnapshot, providerId, patientId, holdAppointmentAt and holdAppointmentTimezone (the hold key with providerId; they follow the booking's current appointment), status, cancellationReason, supportRequired (with audited admin resolution), payment state, refund state.
  - **Version invariant**: `acceptedSubquoteVersion = acceptedParentQuoteVersion`; both identify the accepted FR-004 aggregate revision.
  - **Status values**: `Accepted` (subquote accepted, awaiting payment) → `Confirmed` (deposit paid) → `In Progress` (procedure started, via FR-010) → `Aftercare` (treatment complete; aftercare active via FR-011) → `Completed` (aftercare complete / final review submitted). An `In Progress` booking with a provider fault moves to `Aftercare` only through the admin decision on Screen 11 (Alternative Flow B7). From `Accepted`, hold expiry transitions to `Payment Window Expired`. From `Payment Window Expired`, only the audited admin revive returns the booking to `Accepted` with a new hold. `Confirmed` is a booking status only, never a quote status. `supportRequired` is a marker, not a status.
  - **Cancelled entries** (source state, actor, cause): (1) `Accepted`, `Payment Window Expired`, `Confirmed`, `In Progress`, or `Aftercare` → `Cancelled` by admin cancellation (Screen 9), including support-routed patient requests, with the admin's reason; the inquiry also becomes `Cancelled` and the accepted quote stays `accepted` (Alternative Flows B2 and B3). (2) `Accepted` or `Confirmed` → `Cancelled` by the provider-fault transfer, cause `ProviderFault` (Alternative Flow B5). (3) `Accepted` or `Confirmed` → `Cancelled` by the system on an effective provider suspension or deactivation, cause `ProviderSuspended` or `ProviderDeactivated` with `supportRequired = true` (Alternative Flow B4), followed by the B5 transfer. A provider fault or provider-status event while `In Progress` does not cancel the booking; it stays `In Progress` with `supportRequired` until the admin moves it to `Aftercare` with an aftercare reassignment or cancels it through entry (1) (Alternative Flow B7). A provider fault or provider-status event during `Aftercare` does not cancel the booking; it stays `Aftercare` and follows the aftercare reassignment (Alternative Flow B6). `Completed` and `Cancelled` are terminal.
  - **Relationships**: One booking links to one AcceptanceEvent, one accepted subquote and parent quote context, one provider calendar entry, and one patient.

- **Entity 2 - Calendar Slot**: Represents a provider's pre-scheduled appointment time.
  - **Key attributes**: provider ID, appointment date/time, time zone, start/end, hold/blocked flags, hold start, hold expiry.
  - **Hold and appointment**: Acceptance places a temporary exclusive hold keyed by provider, appointment date/time, and time zone that blocks other patients for the FR-026 slot-hold duration. The appointment record is created only on successful payment. On hold expiry the hold is released and no appointment exists.
  - **Release triggers**: (1) Post-acceptance hold expiry without successful first payment (FR-026 duration, 48h default), (2) Admin cancellation during the hold period, including a support-routed patient request (immediate release per B3 flow), (3) Admin booking cancellation per B2 flow, (4) Provider suspension/deactivation cascade per B4 flow (immediate release, including holds with time remaining), (5) Provider fault before treatment starts per B5 flow, (6) Admin appointment change per Screen 8 (the hold or block moves to the new appointment).
  - **Relationships**: One provider, appointment date/time, and time zone can be held or blocked by at most one pending or confirmed booking; acceptance and hold acquisition are atomic.

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
| 2026-10-14 | 2.6 | Aligned provider suspension/deactivation cancellation cascade per CR-FR015-20261013-01 and FR-015 v1.9: added Alternative Flow B4, Provider-Status Cancellation payment rule, racing-capture edge case, REQ-006-015, Booking cancellationReason/supportRequired attributes, and the cascade slot-release trigger. Consolidated verification remains pending. | Vân Tay Media |
| 2026-10-16 | 2.7 | MTG-002 quote model alignment: one fixed post-acceptance hold for the FR-026 duration keyed by provider, appointment date/time and time zone, never extended by payment failure, with the appointment record created only on payment (S1-2, S2-5, S1-6; M3, M4, D14); first-payment-only Payment Window Expired boundary and recovery route (S1-1; D1); guarded admin revive and date change replacing unrestricted status/date edits (FR-006-3; D2, D11, M17); new Alternative Flow B5 provider-fault transfer with payment placeholder (S1-3; D3, D6, D6-M); promotion and commission wording (S2-4; D12, D13, M5); triggered FR-030 events (S4-1, S4-2; D22, M13, M17); booking-only `Confirmed` (D23); REQ-006-016 to REQ-006-018 added. Provider suspension or deactivation after acceptance now closes the booking and hands off to the B5 transfer with the payment placeholder, replacing "no automatic refund or rebooking"; B3 supersession via linked record (M18, FR-006-8). Minors: FR-006-5, FR-006-6, FR-006-7, S1-9, FR-006-9 (O), FR-006-10 (O). Cross-FR alignment: REQ-006-011 now names the exact FR-030 event keys; REQ-006-017 routes admin date changes to an FR-008 travel review. See CR-FR006-20261016-01. Consolidated verification pending. | Product Owner / Documentation |
| 2026-10-16 | 2.8 | Product Owner Q-series follow-up (Q18, Q23): Alternative Flow B5 step 7 and REQ-006-018 now state that the replacement booking receives the carried-over passport and copied flight and hotel records flagged "travel-date review required" per FR-008, with originals read-only on the closed booking; Overlapping Appointment Prevention rule and User Story 3 scenario 1 now state that the active-hold uniqueness rule (provider, appointment date/time, time zone) makes a concurrent second acceptance fail and the patient is told the slot was just taken. See [CR-FR006-20261016-01](./change-request-2026-10-16-mtg002-quote-model-alignment.md). Consolidated verification pending. | Product Owner / Documentation |
| 2026-10-18 | 2.9 | Consolidated verification corrections: booking Total Amount on Screen 1 is the accepted price after promotion, and Screens 4 and 6 add an Accepted Price row beside the pre-promotion Offered Price (Q25, D12); B2 trigger is patient-only and User Story 4 routes provider withdrawal or drop-out to the Alternative Flow B5 transfer, with refund amounts left to the payment placeholder (D6, D6-M); REQ-006-011 and Dependencies no longer list `quote.withdrawn` as an FR-006 event (FR-004 is the only producer; FR-006 reacts by starting B5), add admin exception recipients for hold expiring soon, Payment Window Expired and provider-fault replacement, and B5 step 6 notifies patient and admin instead of both providers (Q11, Q31, Q32); admin revive takes one promotion use again by source (re-reserved for provider-selected promotions and patient codes, taken again for automatic promotions) (Q30); admin date change on Screen 6 and in the intervention rules triggers an FR-008 travel-date review. See CR-FR006-20261016-01. | Product Owner / Documentation |
| 2026-10-18 | 2.10 | Final audit corrections (Q35, Q36, Q37, Q42, Q43): Alternative Flow B5 now uses an admin-authored replacement quote for the replacement provider in the same inquiry, and the replacement AcceptanceEvent points to its quote, option and date-price row; the single supersession record is written at the replacement acceptance, while the B4 and B5 closures are recorded on the booking as its cause. New Alternative Flow B6: a provider fault during `Aftercare` keeps the booking and treatment record and hands the case to the FR-011 aftercare reassignment with no new acceptance or payment; B4 no longer cancels `Aftercare` bookings. B2 and B3 are admin-only cancellations (support-routed patient requests from acceptance onward), from any non-terminal booking state, with the booking and inquiry `Cancelled` and the accepted quote kept `accepted`; Payment Window Expired recovery is support-routed; patient Screens 1 and 2 show Contact Support. Booking entity lists every `Cancelled` entry by source state, actor and cause. FR-006 now produces `booking.rescheduled` (mandatory, patient and provider) on the admin appointment change and `booking.cancelled` on admin cancellation; booking notices read the booking's current appointment; `booking.scheduled` is patient-only and mandatory and also fires on the replacement acceptance, and the replacement provider is told by `quote.accepted`. Screen 6 Booking Status and appointment fields are read-only and its actions open new admin Screens 7 (Revive Booking), 8 (Change Appointment), 9 (Cancel Booking) and 10 (Provider-Fault Transfer and Replacement Quote), plus a Reassign Aftercare link to FR-011. Booking key attributes use the hold-key fields instead of `slotId`. The `In Progress` provider-fault route is listed under Marking Unclear Requirements. User Story 4, REQ-006-004, REQ-006-005, REQ-006-011, REQ-006-017 and REQ-006-018 updated. Round-two corrections (Q45, Q49): a provider fault while `In Progress` keeps the booking `In Progress` with `supportRequired` (B4 no longer cancels `In Progress` bookings), and new Alternative Flow B7 and admin Screen 11 let the admin either move the booking to `Aftercare` and reassign the aftercare provider through FR-011 Screen 19 or cancel it through Screen 9; the B5 transfer, Screen 10 and the Start Provider-Fault Transfer action are limited to bookings before treatment starts, the Marking Unclear entry is resolved, and REQ-006-019 is added. B5 now cites FR-004 Workflow 7 and Screen 8 for the replacement quote, and a replacement quote that is not accepted expires normally while the inquiry stays `supportRequired` and the admin may author another or cancel. Admin cancellation (B2, B3, Screen 9) no longer writes a supersession record, matching the schema's supersession causes (`ProviderFault`, `ProviderSuspended`, `ProviderDeactivated`). See CR-FR006-20261016-01. | Product Owner / Documentation |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | [NAME NOT RECORDED] | 2025-11-12 | ✅ Approved through v1.7 |
| Technical Lead | [NAME NOT RECORDED] | 2025-11-12 | ✅ Approved through v1.7 |
| Stakeholder | [NAME NOT RECORDED] | 2025-11-12 | ✅ Approved through v1.7 |
| Product Owner | Product Owner | 2026-09-16 | Approved through v2.5 accepted-subquote handoff, complete screen provenance, exclusive acceptance-time slot reservation, payment-window, and appointment-confirmation boundaries; consolidated verification pending |
| Product Owner | Product Owner | 2026-10-18 | Approved v2.10 via MTG-002 decision log (documentation only) |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-011 Aftercare & Recovery Management PRD
**Last Updated**: 2026-10-18
