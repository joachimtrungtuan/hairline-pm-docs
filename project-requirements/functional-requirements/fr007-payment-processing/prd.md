# FR-007 - Payment Processing

**Module**: P-03: Booking & Payment | PR-05: Financial Management & Reporting | A-01: Patient Management & Oversight | A-05: Billing & Financial Reconciliation | S-02: Payment Processing Service | S-03: Notification Service
**Feature Branch**: `fr007-payment-processing`
**Created**: 2025-11-04
**Status**: 🟡 Revised — Documentation Approved; Consolidated Verification Pending
**Source**: FR-007 from `system-prd.md`; [SRC-MTG-002](../../sources/meetings/meeting-02-launch-quote-options-fund-release-and-payments.md#mtg-002-o01-quote-option-contract) and the approved FR-004/FR-005/FR-006 accepted-subquote handoff; Constitution (.specify/memory/constitution.md)

---

## Executive Summary

Enable patients to pay securely for procedures (a deposit, installments or payment in full at booking, and any balance by its due date, the FR-029 balance due days before the procedure) in supported currencies and methods, while ensuring compliant handling of payments, automated receipt/invoice generation, platform commission calculation, and timely provider payouts after treatment completion. This module focuses on the what/why of payments across tenants: a clear, trustworthy checkout for patients, transparent payout tracking for providers, and configurable oversight for admins. It excludes implementation details and adheres to the Hairline Constitution (multi-tenant separation, privacy, auditability, and compliance).

Payment consumes one accepted subquote through the [FR-006 Booking](../fr006-booking-scheduling/prd.md#key-entities) and its immutable FR-005 AcceptanceEvent. The selected package/services, date range, appointment, offered price, attached promotion, currency/exchange-rate snapshot, and inherited parent context are not reselected or repriced at checkout. Payment amount and currency are read from the accepted snapshot, which already includes the accepted promotion and any patient code applied before acceptance (FR-019); no promotion code can be entered, removed, or replaced at checkout or payment. Initial payment requires the valid FR-006 exclusive slot hold; successful deposit, first installment, or full payment confirms that same booking and creates its appointment record.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-03)**: Patient pays deposit to confirm the accepted subquote's booking, or uses an eligible installment/full-payment alternative; pays any final amount by its due date; views payment status, receipts, and invoices; selects a supported payment method while currency remains the accepted snapshot value; receives payment confirmations and reminders.
- **Provider Platform (PR-05)**: Provider views booking payment status and patient payment progress; sees commission deducted amounts; accesses payout statements and history once treatment is marked complete (payout execution managed in FR-017).
- **Admin Platform (A-01)**: Admin views patient payment progress across bookings as part of patient management oversight; views payment details with full context from inquiry/quote/booking stages; monitors payment status as part of patient journey tracking.
- **Admin Platform (A-05)**: Admin processes refunds per policy; reconciliation dashboards and payment/commission report exports are managed in FR-017 (commission rates, deposit defaults, and the refund ladder configured via FR-029; provider payout execution managed in FR-017).
- **Shared Services (S-02/S-03)**: Payment Processing Service handles authorizations/captures/refunds and payout preparation; Notification Service delivers confirmations and reminders.

### Multi-Tenant Breakdown

**Patient Platform (P-03)**:

- Choose a payment option (pay in full now, deposit now and balance later, or installments) and complete the first payment to confirm the booking (REQ-007-098)
- Complete the final payment by its due date: the FR-029 balance due days before the procedure, default 7 days (REQ-007-036)
- Choose supported payment method (card or bank transfer)
- View the locked accepted currency; see clear totals, fees, and remaining balance
- View receipts/invoices and payment history (REQ-007-026)
- Receive confirmations and reminders for upcoming or overdue payments

**Provider Platform (PR-05)**:

- View booking payment status (unpaid/deposit paid/final paid/refunded) (REQ-007-023)
- View patient payment progress (deposit status, installment progress, final payment status) (REQ-007-023)
- View upcoming and completed payouts with commission deducted (payout execution managed in FR-017) (REQ-007-023)
- Access payout statements for accounting (generated in FR-017) (REQ-007-023)

**Admin Platform (A-01)**:

- View patient payment progress across all bookings (deposit status, installment progress, final payment status) as part of patient management oversight (REQ-007-024)
- View payment details with full context from inquiry/quote/booking stages for patient journey tracking (REQ-007-024)
- Monitor payment status and send payment reminders to patients (REQ-007-024)
- Access payment information when managing patient accounts and resolving disputes (REQ-007-024)

**Admin Platform (A-05)**:

- Approve and process refunds per cancellation policy (refund amount calculation per FR-006 cancellation policy)
- Reconciliation dashboards, payment/commission report exports, and reconciliation monitoring: see FR-017: Admin Billing & Financial Management
- **Note**: Commission rate and deposit defaults are configured via FR-029: Payment System Configuration (system-level settings)
- **Note**: Provider payout execution and invoice generation are managed in FR-017: Admin Billing & Financial Management

**Shared Services (S-02, S-03)**:

- S-02: Orchestrates payment lifecycle, refunds, and payout preparation
- S-03: Sends payment confirmations, reminders, and administrative alerts

### Communication Structure

**In Scope**:

- Payment confirmations (deposit, final) to patient (REQ-007-027)
- Payment reminders for upcoming final payment (REQ-007-027)
- Refund confirmations to patient and provider (REQ-007-027)
- Payout notifications to provider after execution (the payout-executed event is owned by FR-017) (REQ-007-027)

**Out of Scope**:

- Chat/messaging between patient and provider (handled elsewhere)
- SMS channel specifics (handled by S-03 configuration; **SMS payment notifications are not available in MVP and will only be enabled in a future phase via S-03/FR-020/FR-030**) (REQ-007-028)
- Any non-payment content (marketing, aftercare content)

### Entry Points

- Patient initiates payment in booking confirmation flow (deposit required) (REQ-007-029)
- Patient initiates final payment from booking details or a reminder before the due date (REQ-007-029)
- Admin processes refunds per cancellation policy (refund amounts per the FR-029 refund ladder and FR-006 policy) (REQ-007-029)
- Patient pays for a standalone aftercare plan once an admin has assigned a provider and the provider has configured the plan (FR-011; REQ-007-088)
- **Note**: Provider payout execution is handled in FR-017: Admin Billing & Financial Management

---

## Business Workflows

### Main Flow: Deposit + Final Payment (Split Payment)

**Actors**: Patient, Provider, Admin, System (Payment Processing Service)
**Trigger**: Patient opens payment for one accepted subquote's pending FR-006 booking; later completes final payment
**Outcome**: Booking confirmed upon deposit; booking fully paid after final payment; receipts/invoices issued; payout becomes eligible after completion is marked and the patient confirmation window ends with no problem raised, or an admin resolves the case

**Payment options**: The patient chooses one of three options on FR-006 Screen 1: pay in full now (Alternative Flow A1), deposit now and the balance later (this flow), or installments, 2 to 9 (FR-007B). FR-007 Screen 1 shows the chosen option read-only (REQ-007-098).

**Initial Payment Guard**: Before calling the payment processor, validate the FR-006 handoff (FR-006 owns these checks): the booking is `Accepted`; the parent inquiry is not `Cancelled`; the parent quote and accepted subquote are still `Accepted`; the provider is still Active (FR-015); parent/subquote versions match the AcceptanceEvent (`acceptedSubquoteVersion = acceptedParentQuoteVersion`); and that event owns the unexpired exclusive appointment hold. Payment cannot select a different package, option/date-price record, appointment, or quote price. This hold guard applies to the first confirming charge, not to later installments/final payments on an already confirmed booking.

**Steps**:

1. Patient reviews the accepted subquote summary (selected package/services, date range, appointment/timezone, offered price, accepted promotion and discounted price, locked currency), payable booking total, deposit amount, and remaining balance. (REQ-007-031)
2. System displays supported payment methods and any applicable fees/requirements (REQ-007-032)
3. Patient selects payment method and confirms deposit payment
4. System processes payment and returns success or actionable challenge (e.g., additional authentication)
5. On success, System confirms the same FR-006 booking, creates its appointment record from the hold (until this point only the temporary hold exists), and, for a provider-selected promotion or patient-entered code, consumes the promotion use reserved at acceptance (FR-019 REQ-019-014; an automatic promotion's use was already consumed at acceptance under FR-019 REQ-019-015); generates receipt and invoice from that booking's recorded terms; sends confirmation to patient and provider. A retry or duplicate callback cannot create a second booking or change the accepted selection.
6. By the due date, Patient initiates final payment from booking details or from a reminder
7. System processes final payment and updates booking to fully paid; issues final receipt/invoice; sends confirmations (REQ-007-083)
8. After completion is marked and the patient confirmation window ends with no problem raised, or after an admin resolves the case, the provider payout becomes eligible (REQ-007-089; payout execution handled in FR-017: Admin Billing & Financial Management)

**Clinic share (Main Flow, clinic share)**: At the 60-day mark before the treatment date, or right away when less time remains, the part of the amount paid that is above Hairline's commission moves to the clinic's locked balance; each later payment tops it up (REQ-007-090).

**Reminders and overdue (Main Flow, reminders and overdue)**: Reminders for the final payment follow the admin timing setting (REQ-007-038). From the day after the due date with a balance unpaid, a scheduled job flags the booking Overdue once and notifies billing admins (REQ-007-036). Where an admin has set the FR-029 Unpaid Balance Cancellation Point, FR-006 Alternative Flow B8 cancels the booking at that point (REQ-007-021).

### Alternative Flows

**A1: Full Payment at Booking**:

- **Trigger**: Patient prefers to pay the full amount at booking instead of split payments
- **Steps**:
  1. Patient selects full payment for the same accepted subquote's booking; the Initial Payment Guard still applies. (REQ-007-084)
  2. System processes that booking's payable full amount and marks the same booking Confirmed and fully paid.
  3. System issues receipt/invoice and sends confirmations
- **Outcome**: Booking is confirmed and fully paid; payout stays pending until completion is marked and the confirmation window ends with no problem raised, or an admin resolves the case (REQ-007-089)

**A2: Refund Due to Cancellation**:

- **Trigger**: A booking closes with a cancellation cause (FR-006), or an admin enters an exception or manual refund
- **Steps**:
  1. Admin opens Refund Processing (Screen 6) and reviews the closure case, the cancellation timing and the refund the case sets: a full refund with no fee for a provider withdrawal, drop-out, suspension or deactivation; the FR-029 refund ladder (launch default: >30 days = 90%, 15-30 days = 50%, <15 days = no refund) on the amount paid toward the booking total, late payment fees excluded, for a patient-request cancellation; the admin-set amount for an in-treatment provider fault (REQ-006-053, REQ-007-063, REQ-007-097)
  2. System sets the refund for the case and starts it. A closure-case refund needs no second approval.
  3. System updates booking/payment status and sends confirmation notices
  4. Exception or manual refund: the admin selects that case on Screen 6, enters the reason (10 to 500 characters) and, for an exception, the documentation, and submits; the refund is awaiting approval (REQ-007-064)
  5. A different admin with billing permission approves or denies within 2 business days; the requester, approver and decision go in the audit entry (REQ-007-015, REQ-007-067)
  6. On denial, System records the denial with its reason, keeps the booking and payment status and notifies the patient (REQ-007-086)
  7. When 2 business days pass with no decision, System sends an escalation notice to billing admins; the refund stays awaiting approval and is never approved or denied automatically (REQ-007-015)
  8. Where the clinic's share has already moved, System pulls it back, deducts any shortfall from the clinic's next payout and splits any cancellation fee, the amount paid less the amount refunded, by the admin-set percentage (REQ-007-091, REQ-007-092)
- **Outcome**: Refund processed for the closure case, or approved or denied for an exception or manual refund; provider payout eligibility updated

**A3: Standalone Aftercare Payment**:

- **Trigger**: An admin has assigned a provider to a standalone aftercare plan and the provider has configured it (FR-011)
- **Steps**:
  1. Patient pays for the standalone aftercare plan (REQ-007-088)
  2. System processes the payment, activates the aftercare plan and issues the receipt and invoice
  3. System releases the provider's money after the patient confirmation window counted from the payment, with no problem raised, or after an admin resolves a problem case (REQ-007-100)
  4. An admin decides any refund of the aftercare payment with a reason on Screen 6; no refund ladder applies (REQ-007-100)
- **Outcome**: Aftercare is active once the payment succeeds; refunds are an admin decision

**B1: Payment Authentication Required / Challenge Failed**:

- **Trigger**: Additional authentication requested; patient fails or abandons
- **Steps**:
  1. System informs patient of the authentication requirement and guides action
  2. If challenge fails or times out, System presents retry and alternative method options
- **Outcome**: Payment remains incomplete until successful authentication; booking not confirmed. Retrying is allowed only while the original FR-006 hold remains active; an authentication challenge does not restart the payment window. Payment failure never extends or restarts the slot hold. The slot stays held only until the single hold that started at subquote acceptance expires (FR-026 slot-hold duration, default 48 hours).

**B2: Payment Failure or Decline**:

- **Trigger**: Payment is declined or fails
- **Steps**:
  1. System classifies failure type (hard decline vs transient error).
  2. For transient errors, Payment Service performs up to 3 automatic retries using exponential backoff (per Constitution) with idempotency safeguards; surface progress and final failure to patient if retries exhaust.
  3. For hard declines, System displays clear error and suggested next steps (retry, use different method).
  4. Patient retries or selects another method against the same accepted snapshot while the original FR-006 hold remains valid.
- **Outcome**: Booking remains unconfirmed until successful initial payment; failure/retry does not change the accepted selection. Payment failure never extends or restarts the slot hold. The slot stays held only until the single hold that started at subquote acceptance expires (FR-026 slot-hold duration, default 48 hours).

**B3: Invalid Accepted Handoff / Payment Window Expired**:

- **Trigger**: Initial payment is requested for an ineligible inquiry/selection, mismatched accepted versions, or a released/expired hold.
- **Steps**:
  1. Reject the request before calling the payment processor and show the FR-006 outcome/recovery instructions.
  2. On hold expiry, FR-006 releases the hold, creates no appointment record, and records `Payment Window Expired`; payment against that accepted selection remains blocked.
  3. Retain the AcceptanceEvent and snapshot unchanged. Do not reopen the parent quote or make the accepted subquote selectable again; recovery is by the patient cancelling the inquiry and starting a new inquiry, or by the FR-006 audited admin revive.
  4. An admin revive is owned by FR-006 (REQ-006-017). It does not extend the expired hold; it starts a new hold, and initial payment then runs the Initial Payment Guard against that new hold.
  5. A payment captured after the hold expired, or after the booking was cancelled for a cause other than a provider fault, is recorded, does not confirm or revive the booking, and is refunded in full automatically with an audit entry and a patient notice, with no admin approval (REQ-007-096).
- **Outcome**: No new charge or booking confirmation against an invalid handoff; no package/date/price reselection inside checkout.

**B4: Provider Fault After Acceptance**:

- **Trigger**: After subquote acceptance and before treatment starts (booking `Accepted` or `Confirmed`), the accepted provider withdraws, drops out, or has a suspension or deactivation take effect. A provider fault during `Aftercare` reassigns only the aftercare provider or team (FR-011) and has no payment effect here. A treatment already started and interrupted by the provider's fault is not this flow: an admin decides the refund (see Fund Release & Money Routing Rules).
- **Steps**:
  1. FR-006 Alternative Flow B5 closes the booking with the provider-fault cause, or with the provider-status cause for a suspension or deactivation (FR-006 B4), and releases the hold. An admin authors a replacement quote in the same inquiry; when the replacement is accepted, a new linked acceptance record and a single supersession record are created.
  2. Payment against the closed booking is blocked. The patient is refunded in full everything paid, with no cancellation fee and no second approval, whether the provider withdraws, drops out, or is suspended or deactivated (FR-006 B4); the replacement booking takes a new payment.
  3. The replacement booking takes its payable amount and currency from the replacement quote's acceptance snapshot, takes a new payment, and follows the main flow. (REQ-007-046)
- **Outcome**: The patient is not charged for the provider fault. Exact refund, fund-release, and payment-allocation mechanics are defined in FR-007, FR-007B, and FR-017.

---

## Screen Specifications

**Shared Accepted-Selection Source Contract**: All checkout, payment-detail, payout-summary, receipt/invoice, and refund views below resolve commercial facts through the FR-006 Booking's acceptance snapshot, not a current parent-quote price range, sibling subquotes, or reusable package-library prices. Parent clinical facts are inherited snapshot context; package/services and date/appointment are the one accepted subquote. Optional captured price components are informational and must not be added again to the offered price. Show the accepted promotion and discount as frozen in the snapshot and take payment amounts and currency from the snapshot; no code entry, removal, replacement, or price-changing revalidation is available at checkout or payment (FR-019). Actual payments/refunds and later authorized booking interventions remain separate auditable records.

### Patient Platform

#### Screen 1: Patient Checkout (Deposit)

**Purpose**: Allow patient to make the first payment of the chosen option (full payment, deposit, or first installment) to confirm booking

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Accepted Selection | group | Yes | Package/services, date range, appointment/timezone, inherited treatment context, and accepted subquote reference | Read-only; FR-006 acceptance snapshot | ENT-booking.accepted_subquote_id, ENT-subquote.package_snapshot, ENT-subquote.included_and_custom_services, ENT-subquote.date_range, ENT-subquote.appointment_at, ENT-subquote.appointment_timezone, ENT-quote.treatment_id |
| Accepted Subquote Amount | number | Yes | Offered price for exactly one accepted option/date-price record | Read-only; acceptance snapshot; never sum sibling alternatives | ENT-subquote.offered_price |
| Discount Applications | group | Conditional | Accepted promotion and discount frozen in the acceptance snapshot, including any patient code applied before acceptance | Read-only; acceptance snapshot; no code input at checkout | ENT-subquote.promotion_snapshot, ENT-acceptance-event.promotion_code |
| Total Amount | number | Yes | Payable booking total under the recorded commercial terms | Positive amount; accepted discounted price from the acceptance snapshot, never recomputed, without double-counting components | ENT-booking.payable_total |
| Deposit Amount | number | Yes | Deposit to confirm booking | Admin-configurable percentage (default 20-30% range, configured via FR-029) of the booking total (accepted price after promotion, from the acceptance snapshot); within allowed range | ENT-booking.deposit_amount |
| Currency | text | Yes | Accepted patient payment currency | Read-only; accepted currency/exchange-rate snapshot; no checkout reselection | ENT-quote.currency_snapshot |
| Payment Option | select | Yes | Pay in full now, deposit now and balance later, or installments (2 to 9) | Read-only; chosen on FR-006 Screen 1; one of three options (REQ-007-098) | ENT-booking.payment_option |
| Payment Hold Expires At | datetime | Yes | Deadline for the initial confirming payment | Read-only; the single FR-006 hold that started at subquote acceptance, or the new hold after an admin revive; display countdown and disable payment after expiry (REQ-007-049) | ENT-slot-hold.hold_expires_at |
| Payment Method | select | Yes | Card or bank transfer | Must be in supported methods | ENT-payment.payment_method |
| Billing Details | text | Yes | Name, address, contact | Required for invoicing | ENT-payment.billing_details |

**Business Rules**:

- Show clear breakdown: total, deposit, remaining balance, currency (REQ-007-033)
- Disable payment button until all required fields are valid (REQ-007-048)
- Display clear error messaging and retry options on failure (REQ-007-042)
- Do not reveal provider direct contact details until booking confirmed (REQ-007-047)
- Apply the Initial Payment Guard before processor submission; initial payment failure never extends or restarts the hold. Eligible installment selection is owned by FR-007B and confirms booking only after its first successful charge. (REQ-007-017, REQ-007-001, REQ-007-005)

**Notes**:

- Show progress indicator during processing; avoid blocking UI for more than a few seconds without feedback (REQ-007-048)
- Preserve entered details if payment attempt fails to allow quick retry (REQ-007-048)

---

#### Screen 2: Patient Final Payment

**Purpose**: Allow patient to complete the final payment by its due date, the FR-029 balance due days before the procedure (default 7 days)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Accepted Selection | group | Yes | Accepted subquote reference, package, and appointment context for this booking | Read-only; same FR-006 acceptance snapshot as initial payment | ENT-booking.accepted_subquote_id, ENT-subquote.package_snapshot, ENT-subquote.included_and_custom_services, ENT-subquote.date_range, ENT-subquote.appointment_at, ENT-subquote.appointment_timezone, ENT-quote.treatment_id |
| Remaining Balance | number | Yes | Amount still due on this booking | Positive; reconciled payable total less recorded successful payments and authorized adjustments (REQ-007-081) | ENT-booking.remaining_balance |
| Final Payment Due Date | datetime | Yes | Date the balance is due | Read-only; the FR-029 balance due days before the procedure (REQ-007-036) | ENT-booking.final_payment_due_at |
| Unpaid Balance Cancellation Point | text | Conditional | Day on which an unpaid balance cancels the booking | Read-only; shown only when an admin has set the FR-029 point and the booking was confirmed after it was set; days after the first missed due date (REQ-007-021) | no graph field (setting value) |
| Currency | text | Yes | Accepted patient payment currency | Read-only; same locked currency/exchange-rate snapshot as initial payment | ENT-quote.currency_snapshot |
| Payment Method | select | Yes | Card or bank transfer | Supported methods | ENT-payment.payment_method |
| Billing Details | text | Yes | For invoice | Required if changed since deposit | ENT-payment.billing_details |

**Business Rules**:

- Display due date and countdown to procedure date (REQ-007-037)
- Send reminders at the days set in the payment reminder timing setting: whole days 0 to 14 before the due date, up to 3 reminders, default 3 days before the due date and on the due date (REQ-007-038)
- The balance is overdue from the day after the due date: the booking is flagged Overdue once and billing admins are notified (REQ-007-036). An overdue final payment never causes `Payment Window Expired`; it cancels the booking only through the FR-006 unpaid balance cancellation at the FR-029 Unpaid Balance Cancellation Point, when an admin has set one (REQ-007-021).

**Notes**:

- Keep summary of previous payments and remaining balance visible

---

### Provider Platform

#### Screen 3: Booking Payment Status & Progress (Provider)

**Purpose**: View complete payment information with full context from inquiry, quote, booking, and payment stages

**Note**: This screen aggregates payment data with context from previous stages (FR-003, FR-004, FR-005, FR-006) to provide comprehensive payment view. This complements FR-006's Booking Detail View (Screen 4) which shows all booking information including payment summary.

**Data Fields** (Continuation from FR-006 Screen 4, aggregating data from FR-003, FR-004, FR-005, FR-006, FR-007):

**Section 1: Booking & Payment Context** (from FR-006):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Booking Reference | text | Yes | Unique booking reference | Read-only; link to FR-006 booking detail | ENT-booking.id |
| Booking Status | badge | Yes | Current FR-006 status, including Accepted and Payment Window Expired | Read-only; full lifecycle owned by FR-006 | ENT-booking.status |
| Appointment Date | datetime | Yes | Accepted appointment; held before initial payment, appointment record created at successful initial payment | Read-only; acceptance snapshot | ENT-booking.appointment_at |
| Inquiry Reference | text | Yes | Original inquiry HPID | Read-only; link to inquiry | ENT-inquiry.reference |
| Parent Quote Reference | text | Yes | Accepted parent quote reference | Read-only; acceptedParentQuoteId; historical context, not payment target | ENT-booking.accepted_parent_quote_id |
| Accepted Subquote Reference | text | Yes | One selected option/date-price combination | Read-only; acceptedSubquoteId; link to accepted selection | ENT-booking.accepted_subquote_id |
| Accepted Provenance | group | Yes | AcceptanceEvent ID, accepted parent/subquote versions, Quote Option ID, and option/date-price ID | Read-only; versions equal the accepted parent aggregate revision | ENT-acceptance-event.id, ENT-acceptance-event.accepted_parent_quote_version, ENT-acceptance-event.accepted_subquote_version, ENT-acceptance-event.quote_option_id, ENT-acceptance-event.option_date_price_id |
| Accepted Date Range / Timezone | group | Yes | Chosen range and appointment timezone | Read-only; acceptance snapshot | ENT-subquote.date_range, ENT-subquote.appointment_timezone |
| Payment Hold Expires At | datetime | Conditional | Original initial-payment hold deadline | Read-only; pending booking only; no new hold for later payments | ENT-slot-hold.hold_expires_at |

**Section 2: Patient Information** (from FR-003, unmasked if Confirmed):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Patient Anonymized ID | text | Yes | Patient code (always visible) | Read-only | ENT-patient.anonymized_id |
| Patient Name | text | Conditional | Full name (if Confirmed) or masked (e.g., "Mark P. - PAT-00123") | Unmask only if status = Confirmed (FR-006 REQ-006-002 and REQ-006-008) | ENT-patient.name |
| Patient Location | text | Yes | Country/city | Read-only; from inquiry | ENT-patient.country, ENT-patient.city |
| Treatment Type Requested | text | Yes | Hair/Beard/Both | Read-only; from inquiry | ENT-inquiry.treatment_area_id |

**Section 3: Accepted Quote & Treatment Information** (FR-005 snapshot via FR-006):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Treatment Type | text | Yes | Selected treatment (FUE, FUT, DHI, etc.) | Read-only; inherited accepted parent context | ENT-quote.treatment_id |
| Estimated Graft Count | number | Yes | Estimated number of grafts | Read-only; inherited accepted parent context | ENT-quote.estimated_grafts |
| Accepted Package / Services | group | Yes | One accepted package snapshot and its included/custom services | Read-only; quote-local snapshot, not all parent options or current library | ENT-subquote.package_snapshot, ENT-subquote.included_and_custom_services |
| Clinician Assigned | text | Yes | Clinician assigned in the accepted treatment context | Read-only; inherited acceptance snapshot | ENT-quote.clinician_ids |

**Section 4: Accepted Pricing Breakdown** (FR-005 snapshot via FR-006):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Currency | text | Yes | Accepted payment currency | Read-only; locked snapshot | ENT-quote.currency_snapshot |
| Treatment Price | number | Conditional | Treatment component, if captured in accepted pricing | Read-only; informational; not added on top of offered price | ENT-quote-option-item.price |
| Package / Service Price Components | group | Conditional | Captured components of the single accepted package | Read-only; informational; exclude sibling options and live library prices | ENT-quote-option-item.price |
| Discount Applied | group | Conditional | Accepted promotion and discount breakdown frozen at acceptance | Read-only; recorded terms; no live recalculation of historical applications | ENT-subquote.promotion_snapshot, ENT-acceptance-event.promotion_code |
| Accepted Subquote Amount | number | Yes | Offered price of the selected option/date-price record, before the accepted promotion | Read-only; acceptance snapshot | ENT-subquote.offered_price |
| Payable Booking Total | number | Yes | Accepted discounted price payable for this booking | Read-only; booking commercial terms; no component double-counting | ENT-booking.payable_total |

**Section 5: Payment Progress & Status** (from FR-007):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Deposit Percentage | text | Yes | Deposit percentage used | Read-only; admin-configured via FR-029 | ENT-booking.deposit_percentage |
| Deposit Amount | number | Yes | Required deposit amount | FR-029 deposit percentage of the booking total (accepted price after promotion, from the acceptance snapshot) | ENT-booking.deposit_amount |
| Deposit Status | badge | Yes | Pending / Paid / Partial (part of the deposit received) | Read-only | ENT-booking.deposit_status |
| Deposit Paid Date | datetime | Conditional | Date deposit was paid | Read-only; if paid | ENT-booking.deposit_paid_at |
| Payment Method (Deposit) | text | Conditional | Payment method used for deposit | Read-only; if paid | ENT-booking.deposit_payment_method |
| Payment Status | badge | Yes | Unpaid / Deposit only / Installments active / Full paid / Refunded | Read-only; the single list owned by FR-007 (Payment & Billing Rules) | ENT-booking.payment_status |
| Overdue Flag | badge | Conditional | Shown when the due date has passed and the amount is unpaid | Read-only; calculated, not stored; separate from Payment Status | ENT-booking.is_overdue |
| Installment Progress | group | Conditional | Current installment number, total installments, next due date, completion percentage | Only shown if installments active; read from the installment plan (FR-007B): completion percentage and installments paid | ENT-installment-plan.completion_percentage, ENT-installment-plan.installments_paid |
| Final Payment Status | badge | Yes | Not Due / Due / Paid / Overdue | Read-only | ENT-booking.final_payment_status |
| Final Payment Due Date | datetime | Conditional | The FR-029 balance due days before the procedure | Read-only | ENT-booking.final_payment_due_at |
| Final Payment Amount | number | Conditional | Final payment amount due | Calculated | ENT-booking.final_payment_amount |
| Final Payment Method | text | Conditional | Payment method used for final payment | Read-only; if paid | ENT-booking.final_payment_method |
| Final Payment Paid Date | datetime | Conditional | Date final payment was paid | Read-only; if paid | ENT-booking.final_payment_paid_at |
| Remaining Balance | number | Yes | Amount remaining to pay | Calculated | ENT-booking.remaining_balance |
| Total Paid Amount | number | Yes | Sum of all payments made | Calculated (REQ-007-082) | ENT-booking.paid_amount |

**Section 6: Payment History** (from FR-007):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Payment History | table | Yes | All payments (deposit, installments, final) with dates, amounts, methods, status | Read-only | ENT-booking.payment_history |
| Payment Transaction ID | text | Yes | Payment processor transaction ID | Read-only | ENT-payment.transaction_id |
| Payment Receipt Link | link | Yes | Link to payment receipt/invoice | Read-only | ENT-payment.receipt_ref |
| Refund History | table | Conditional | All refunds processed (if any) with dates, amounts, reasons | Read-only; if refunds exist | ENT-booking.refund_history |

**Section 7: Payout Information** (from FR-017, conditional):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Payout Status | badge | Conditional | Value from the single payout status list owned by FR-017 | Only shown after treatment completion | ENT-payout.status |
| Gross Amount | number | Conditional | Total paid by patient | Read-only; if payout eligible | ENT-payout.gross_amount |
| Commission | text | Conditional | Platform commission type (Percentage or Flat Rate) and value | Read-only; read from the commission snapshot taken at booking confirmation (FR-029), never from live configuration | ENT-commission.commission_type, ENT-commission.rate_value |
| Commission Amount | number | Conditional | Platform commission deducted | Read-only; if payout eligible | ENT-payout.commission_amount |
| Net Payout | number | Conditional | Amount to provider | Read-only; if payout eligible | ENT-payout.net_amount |
| Payout Execution Date | datetime | Conditional | Date payout was executed | Read-only; if executed | ENT-payout.executed_at |
| Payout Statement Link | link | Conditional | Link to detailed payout invoice (FR-017) | Only shown if payout executed | ENT-payout.statement_ref |

**Actions**:

| Action | Type | Condition | Description | Graph field |
|--------|------|-----------|-------------|-------------|
| View Booking Details | link | Always | Open FR-006 booking detail view (full context) | no graph field (control) |
| View Accepted Selection | link | Always | Open the accepted subquote snapshot and inherited parent context via FR-006 | no graph field (control) |
| View Inquiry | link | Always | Open full inquiry details (FR-003) | no graph field (control) |
| View Payment Receipt | link | Conditional | Open payment receipt/invoice (if payment exists) | no graph field (control) |
| View Payout Details | link | Conditional | Open payout details in FR-017 (if payout exists) | no graph field (control) |

**Business Rules**:

- Payment status reflects real-time payment progress (deposit, installments, final payment) (REQ-007-051)
- Provider can see payment progress but cannot modify payment information (REQ-007-050)
- Patient full identity only visible if booking status is "Confirmed" (payment successful), as stated in FR-006 REQ-006-002 and REQ-006-008
- All payment data is read-only for provider (REQ-007-050)
- Payout information links to FR-017: Admin Billing & Financial Management for detailed payout statements
- All sections display data from previous stages (inquiry → quote → booking → payment) in chronological order (REQ-007-052)

**Notes**:

- This screen provides comprehensive payment view with full context from patient journey
- UI may use tabs or accordion sections to organize information by stage
- Payment details shown without card information (PCI compliance) (REQ-007-053)
- This complements FR-006's Booking Detail View which shows all booking information; this screen focuses specifically on payment details
- Payment status updates in real-time as patient makes payments (REQ-007-051)

---

#### Screen 4: Provider Payout Overview (Provider)

**Purpose**: View payout status and details for completed treatments with full context from booking and payment stages

**Note**: Detailed payout execution and invoice generation are managed in FR-017: Admin Billing & Financial Management. This screen provides comprehensive view with context from previous stages and links to detailed payout information.

**Data Fields** (Continuation from Screen 3, aggregating data from FR-003, FR-004, FR-006, FR-007, FR-017):

**Section 1: Booking & Treatment Context** (from FR-006):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Booking Reference | text | Yes | Unique booking reference | Read-only; link to FR-006 booking detail | ENT-booking.id |
| Treatment Completion Date | datetime | Yes | Date treatment was marked complete | Read-only | ENT-treatment-record.completed_at |
| Treatment Type | text | Yes | Selected treatment (FUE, FUT, DHI, etc.) | Read-only; inherited accepted parent context | ENT-quote.treatment_id |
| Estimated Graft Count | number | Yes | Estimated number of grafts | Read-only; inherited accepted parent context | ENT-quote.estimated_grafts |
| Clinician Assigned | text | Yes | Clinician recorded for the completed procedure | Read-only; actual FR-010 execution record, with accepted assignment retained as history | ENT-quote.clinician_ids |

**Section 2: Patient Information** (from FR-003):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Patient Name | text | Yes | Full patient name (unmasked after treatment) | Read-only | ENT-patient.name |
| Patient ID | text | Yes | Patient code | Read-only | ENT-patient.anonymized_id |
| Treatment Type Requested | text | Yes | Hair/Beard/Both | Read-only; from inquiry | ENT-inquiry.treatment_area_id |

**Section 3: Payment Summary** (from FR-007):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Currency | text | Yes | Accepted payment currency | Read-only; locked snapshot | ENT-quote.currency_snapshot |
| Accepted Subquote Amount | number | Yes | Offered price for the accepted option/date-price record | Read-only; acceptance snapshot via booking | ENT-subquote.offered_price |
| Payable Booking Total | number | Yes | Accepted discounted price payable for this booking | Read-only; recorded booking terms | ENT-booking.payable_total |
| Total Paid Amount | number | Yes | Sum of all payments made by patient | Read-only | ENT-booking.paid_amount |
| Payment Status | badge | Yes | Unpaid / Deposit only / Installments active / Full paid / Refunded | Read-only; the single list owned by FR-007 (Payment & Billing Rules) | ENT-booking.payment_status |
| Payment History | link | Yes | Link to full payment history (Screen 3) | Read-only | ENT-booking.payment_history |

**Section 4: Payout Calculation** (from FR-017):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Gross Amount | number | Yes | Total paid by patient | Positive; read-only | ENT-payout.gross_amount |
| Commission | text | Yes | Platform commission type (Percentage or Flat Rate) and value | Read-only; read from the commission snapshot taken at booking confirmation (FR-029), never from live configuration | ENT-commission.commission_type, ENT-commission.rate_value |
| Commission Amount | number | Yes | Platform commission deducted | Calculated; read-only | ENT-payout.commission_amount |
| Net Payout | number | Yes | Amount to provider | Gross minus commission; read-only (REQ-007-056) | ENT-payout.net_amount |
| Payout Currency | text | Yes | Provider's payout currency | Read-only; provider-configured | ENT-payout.payout_currency |
| Exchange Rate | number | Conditional | Accepted currency conversion rate (if multi-currency) | Read-only; locked at subquote acceptance and retained by FR-006 | ENT-quote.locked_exchange_rate_snapshot |

**Section 5: Payout Status & Execution** (from FR-017):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Payout Status | badge | Yes | Value from the single payout status list owned by FR-017 | Read-only; valid transitions owned by FR-017 | ENT-payout.status |
| Payout Eligibility Date | datetime | Conditional | Date payout became eligible | Read-only; after treatment completion | ENT-payout.eligibility_at |
| Payout Execution Date | datetime | Conditional | Date payout was executed | Read-only; if executed | ENT-payout.executed_at |
| Payout Method | text | Conditional | Payout method (bank transfer, etc.) | Read-only; if executed | ENT-payout.payout_method |
| Payout Transaction ID | text | Conditional | Payout transaction reference | Read-only; if executed | ENT-payout.transaction_id |
| Payout Statement Link | link | Conditional | Link to detailed payout invoice (FR-017) | Only shown if payout executed | ENT-payout.statement_ref |
| Payout Invoice | link | Conditional | Download payout invoice PDF | Only shown if payout executed | ENT-payout.invoice_ref |

**Section 6: Accepted Treatment Details** (FR-005 snapshot via FR-006):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Parent Quote Reference | text | Yes | Accepted parent quote reference and aggregate revision | Read-only; history via FR-006 | ENT-booking.accepted_parent_quote_id |
| Accepted Subquote Reference | text | Yes | One accepted option/date-price combination | Read-only; snapshot and AcceptanceEvent via FR-006 | ENT-booking.accepted_subquote_id |
| Accepted Package / Services | group | Yes | One accepted package snapshot and included/custom services | Read-only; not all parent alternatives | ENT-subquote.package_snapshot, ENT-subquote.included_and_custom_services |
| Accepted Date Range / Appointment | group | Yes | Selected range, appointment date/time, and timezone | Read-only; acceptance snapshot; later intervention retained separately | ENT-subquote.date_range, ENT-subquote.appointment_at, ENT-subquote.appointment_timezone |

**Actions**:

| Action | Type | Condition | Description | Graph field |
|--------|------|-----------|-------------|-------------|
| View Booking Details | link | Always | Open FR-006 booking detail view (full context) | no graph field (control) |
| View Payment Details | link | Always | Open Screen 3: Payment Status & Progress | no graph field (control) |
| View Accepted Selection | link | Always | Open the accepted subquote snapshot and inherited parent context via FR-006 | no graph field (control) |
| Download Payout Invoice | link | Conditional | Download payout invoice PDF (if payout executed) | no graph field (control) |
| View Payout Details (FR-017) | link | Conditional | Open detailed payout information in FR-017 (if payout exists) | no graph field (control) |

**Business Rules**:

- Payout visible only after the provider has marked the procedure complete; the clinic's share is then released per Fund Release & Money Routing Rules (after the patient's confirmation window with no problem raised, or after an admin resolves a problem case) (REQ-007-054)
- Commission shown and deducted from payout amount; the commission type (Percentage or Flat Rate) and value come from the snapshot taken at booking confirmation (FR-029), so later configuration changes do not affect the booking (REQ-007-014)
- Payout calculation based on total paid amount (not just deposit) (REQ-007-055)
- History of payouts accessible for accounting (REQ-007-057)
- Links to FR-017 for detailed payout statements and invoices
- All payout data is read-only for provider (payout execution is owned by FR-017: automatic on the Stripe Connect rail after release; on the manual rail an admin approves the settlement statement and marks it paid) (REQ-007-050)

**Notes**:

- This screen provides comprehensive payout view with full context from booking and payment stages
- UI may use tabs or accordion sections to organize information
- This complements FR-006's Booking Detail View and Screen 3's Payment Status view
- Detailed payout invoices and statements are generated in FR-017: Admin Billing & Financial Management
- Payout execution follows FR-017 (see Fund Release & Money Routing Rules); provider can only view status and details

---

### Admin Platform

**Configuration Reference**: Payment system settings (deposit percentages, commission rates, supported payment methods) are configured and reviewed via `FR-029: Payment System Configuration`. This module links admins out to FR-029 when configuration context is needed; no configuration data is duplicated here.

#### Screen 5: Patient Payment Progress Dashboard (Admin)

**Purpose**: Allow admin to monitor patient payment progress across all bookings (list/dashboard view)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Booking ID | text | Yes | Reference identifier | Searchable, filterable, clickable link | ENT-booking.id |
| Patient Name | text | Yes | Full patient name | Searchable | ENT-patient.name |
| Provider Name | text | Yes | Provider/clinic name | Filterable | ENT-provider.name |
| Total Amount | number | Yes | Total booking amount | Sortable | ENT-booking.payable_total |
| Deposit Amount | number | Yes | Required deposit amount | FR-029 deposit percentage of the booking total (accepted price after promotion, from the acceptance snapshot) | ENT-booking.deposit_amount |
| Deposit Status | badge | Yes | Pending / Paid / Partial (part of the deposit received) | Filterable | ENT-booking.deposit_status |
| Deposit Paid Date | datetime | Conditional | Date deposit was paid | Read-only; if paid | ENT-booking.deposit_paid_at |
| Payment Status | badge | Yes | Unpaid / Deposit only / Installments active / Full paid / Refunded | Filterable; the single list owned by FR-007 (Payment & Billing Rules) | ENT-booking.payment_status |
| Overdue Flag | badge | Conditional | Shown when the due date has passed and the amount is unpaid | Filterable; calculated, not stored; separate from Payment Status | ENT-booking.is_overdue |
| Installment Progress | text | Conditional | "X of Y installments paid" | Only shown if installments active; read from the installment plan (FR-007B): installments paid and completion percentage | ENT-installment-plan.installments_paid, ENT-installment-plan.completion_percentage |
| Next Payment Due Date | datetime | Conditional | Next installment or final payment due date | Read-only | ENT-booking.next_payment_due_at |
| Final Payment Status | badge | Yes | Not Due / Due / Paid / Overdue | Filterable | ENT-booking.final_payment_status |
| Remaining Balance | number | Yes | Amount remaining to pay | Calculated, sortable | ENT-booking.remaining_balance |
| Actions | buttons | Yes | View Payment Details, Process Refund, Send Reminder | RBAC enforced | no graph field (control) |

**Business Rules**:

- Admin can view payment progress for all bookings across all providers (REQ-007-060)
- Filtering options: Payment Status, Provider, Date Range, Overdue Payments (REQ-007-060)
- Clicking on Booking ID or "View Payment Details" opens Screen 5B: Payment Detail View
- Admin can send payment reminders to patients
- Admin can process refunds per FR-006 cancellation policy (opens Screen 6)
- All payment data in dashboard is read-only (REQ-007-061)

**Notes**:

- This screen provides comprehensive payment monitoring across the platform
- Dashboard/list view for quick overview and filtering
- Links to detailed payment information (Screen 5B) and booking information (FR-006 Screen 6)

---

#### Screen 5B: Payment Detail View (Admin)

**Purpose**: View complete payment information with full context from all stages for a specific booking

**Note**: This screen is accessed from Screen 5 (Payment Progress Dashboard) by clicking "View Payment Details" or a booking row. It provides comprehensive payment view with context from previous stages (FR-003, FR-004, FR-005, FR-006, FR-007).

**Data Fields** (Continuation from Screen 5, aggregating data from FR-003, FR-004, FR-005, FR-006, FR-007):

**Section 1: Booking & Payment Context** (from FR-006):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Booking Reference | text | Yes | Unique booking reference | Read-only; link to FR-006 booking detail | ENT-booking.id |
| Booking Status | badge | Yes | Current FR-006 status, including Accepted and Payment Window Expired | Read-only; full lifecycle owned by FR-006 | ENT-booking.status |
| Appointment Date | datetime | Yes | Accepted appointment; held before initial payment, appointment record created at successful initial payment | Read-only; acceptance snapshot | ENT-booking.appointment_at |
| Inquiry Reference | text | Yes | Original inquiry HPID | Read-only; link to inquiry | ENT-inquiry.reference |
| Parent Quote Reference | text | Yes | Accepted parent quote reference | Read-only; acceptedParentQuoteId; historical context, not payment target | ENT-booking.accepted_parent_quote_id |
| Accepted Subquote Reference | text | Yes | One selected option/date-price combination | Read-only; acceptedSubquoteId; link to accepted selection | ENT-booking.accepted_subquote_id |
| Accepted Provenance | group | Yes | AcceptanceEvent ID, accepted parent/subquote versions, Quote Option ID, and option/date-price ID | Read-only; versions equal the accepted parent aggregate revision | ENT-acceptance-event.id, ENT-acceptance-event.accepted_parent_quote_version, ENT-acceptance-event.accepted_subquote_version, ENT-acceptance-event.quote_option_id, ENT-acceptance-event.option_date_price_id |
| Accepted Date Range / Timezone | group | Yes | Chosen range and appointment timezone | Read-only; acceptance snapshot | ENT-subquote.date_range, ENT-subquote.appointment_timezone |
| Payment Hold Expires At | datetime | Conditional | Original initial-payment hold deadline | Read-only; pending booking only; no new hold for later payments | ENT-slot-hold.hold_expires_at |

**Section 2: Patient Information** (from FR-003, always visible to admin):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Patient ID | text | Yes | Patient code | Read-only | ENT-patient.anonymized_id |
| Patient Name | text | Yes | Full patient name | Read-only | ENT-patient.name |
| Patient Email | text | Yes | Email address | Read-only | ENT-patient.email |
| Patient Phone | text | Yes | Phone number | Read-only | ENT-patient.phone |
| Patient Address | text | No | Full address | Read-only; from profile | ENT-patient.address |
| Patient Location | text | Yes | Country/city | Read-only; from inquiry | ENT-patient.country, ENT-patient.city |
| Patient Age | number | Yes | Patient age | Read-only; from inquiry | ENT-patient.age |
| Patient Gender | text | Yes | Gender | Read-only; from inquiry | ENT-patient.gender |
| Treatment Type Requested | text | Yes | Hair/Beard/Both | Read-only; from inquiry | ENT-inquiry.treatment_area_id |

**Section 3: Accepted Quote & Treatment Information** (FR-005 snapshot via FR-006):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Treatment Type | text | Yes | Selected treatment (FUE, FUT, DHI, etc.) | Read-only; inherited accepted parent context | ENT-quote.treatment_id |
| Estimated Graft Count | number | Yes | Estimated number of grafts | Read-only; inherited accepted parent context | ENT-quote.estimated_grafts |
| Accepted Package / Services | group | Yes | One accepted package snapshot and its included/custom services | Read-only; quote-local snapshot, not all parent options or current library | ENT-subquote.package_snapshot, ENT-subquote.included_and_custom_services |
| Clinician Assigned | text | Yes | Clinician assigned in the accepted treatment context | Read-only; inherited acceptance snapshot | ENT-quote.clinician_ids |

**Section 4: Accepted Pricing Breakdown** (FR-005 snapshot via FR-006):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Currency | text | Yes | Accepted payment currency | Read-only; locked snapshot | ENT-quote.currency_snapshot |
| Treatment Price | number | Conditional | Treatment component, if captured in accepted pricing | Read-only; informational; not added on top of offered price | ENT-quote-option-item.price |
| Package / Service Price Components | group | Conditional | Captured components of the single accepted package | Read-only; informational; exclude sibling options and live library prices | ENT-quote-option-item.price |
| Discount Applied | group | Conditional | Accepted promotion and discount breakdown frozen at acceptance | Read-only; recorded terms; no live recalculation of historical applications | ENT-subquote.promotion_snapshot, ENT-acceptance-event.promotion_code |
| Accepted Subquote Amount | number | Yes | Offered price of the selected option/date-price record, before the accepted promotion | Read-only; acceptance snapshot | ENT-subquote.offered_price |
| Payable Booking Total | number | Yes | Accepted discounted price payable for this booking | Read-only; booking commercial terms; no component double-counting | ENT-booking.payable_total |

**Section 5: Payment Progress & Status** (from FR-007):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Deposit Percentage | text | Yes | Deposit percentage used | Read-only; admin-configured via FR-029 | ENT-booking.deposit_percentage |
| Deposit Amount | number | Yes | Required deposit amount | FR-029 deposit percentage of the booking total (accepted price after promotion, from the acceptance snapshot) | ENT-booking.deposit_amount |
| Deposit Status | badge | Yes | Pending / Paid / Partial (part of the deposit received) | Read-only | ENT-booking.deposit_status |
| Deposit Paid Date | datetime | Conditional | Date deposit was paid | Read-only; if paid | ENT-booking.deposit_paid_at |
| Payment Method (Deposit) | text | Conditional | Payment method used for deposit | Read-only; if paid | ENT-booking.deposit_payment_method |
| Payment Status | badge | Yes | Unpaid / Deposit only / Installments active / Full paid / Refunded | Read-only; the single list owned by FR-007 (Payment & Billing Rules) | ENT-booking.payment_status |
| Overdue Flag | badge | Conditional | Shown when the due date has passed and the amount is unpaid | Read-only; calculated, not stored; separate from Payment Status | ENT-booking.is_overdue |
| Installment Progress | group | Conditional | Current installment number, total installments, next due date, completion percentage | Only shown if installments active; read from the installment plan (FR-007B): completion percentage and installments paid | ENT-installment-plan.completion_percentage, ENT-installment-plan.installments_paid |
| Final Payment Status | badge | Yes | Not Due / Due / Paid / Overdue | Read-only | ENT-booking.final_payment_status |
| Final Payment Due Date | datetime | Conditional | The FR-029 balance due days before the procedure | Read-only | ENT-booking.final_payment_due_at |
| Final Payment Amount | number | Conditional | Final payment amount due | Calculated | ENT-booking.final_payment_amount |
| Final Payment Method | text | Conditional | Payment method used for final payment | Read-only; if paid | ENT-booking.final_payment_method |
| Final Payment Paid Date | datetime | Conditional | Date final payment was paid | Read-only; if paid | ENT-booking.final_payment_paid_at |
| Remaining Balance | number | Yes | Amount remaining to pay | Calculated | ENT-booking.remaining_balance |
| Total Paid Amount | number | Yes | Sum of all payments made | Calculated | ENT-booking.paid_amount |

**Section 6: Payment History** (from FR-007):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Payment History | table | Yes | All payments (deposit, installments, final) with dates, amounts, methods, transaction IDs, status | Read-only | ENT-booking.payment_history |
| Payment Transaction ID | text | Yes | Payment processor transaction ID | Read-only | ENT-payment.transaction_id |
| Payment Receipt Link | link | Yes | Link to payment receipt/invoice | Read-only | ENT-payment.receipt_ref |
| Refund History | table | Conditional | All refunds processed (if any) with dates, amounts, reasons, transaction IDs | Read-only; if refunds exist | ENT-booking.refund_history |

**Section 7: Provider Information** (from provider profile):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Provider Name | text | Yes | Provider/clinic name | Read-only | ENT-provider.name |
| Provider Contact | text | Yes | Clinic contact information | Read-only | ENT-provider.phone, ENT-provider.address |
| Provider Email | text | Yes | Provider email | Read-only | ENT-provider.email |

**Section 8: Payout Information** (from FR-017, conditional):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Payout Status | badge | Conditional | Value from the single payout status list owned by FR-017 | Only shown after treatment completion | ENT-payout.status |
| Gross Amount | number | Conditional | Total paid by patient | Read-only; if payout eligible | ENT-payout.gross_amount |
| Commission | text | Conditional | Platform commission type (Percentage or Flat Rate) and value | Read-only; read from the commission snapshot taken at booking confirmation (FR-029), never from live configuration | ENT-commission.commission_type, ENT-commission.rate_value |
| Commission Amount | number | Conditional | Platform commission deducted | Read-only; if payout eligible | ENT-payout.commission_amount |
| Net Payout | number | Conditional | Amount to provider | Read-only; if payout eligible | ENT-payout.net_amount |
| Payout Link | link | Conditional | Link to payout details in FR-017 | Only shown if payout exists | ENT-payout.id |

**Actions**:

| Action | Type | Condition | Description | Graph field |
|--------|------|-----------|-------------|-------------|
| View Booking Details | link | Always | Open FR-006 booking detail view (full context) | no graph field (control) |
| View Accepted Selection | link | Always | Open the accepted subquote snapshot and inherited parent context via FR-006 | no graph field (control) |
| View Inquiry | link | Always | Open full inquiry details (FR-003) | no graph field (control) |
| Process Refund | button | Booking cancelled or eligible | Open Screen 6: Refund Processing (REQ-007-093) | no graph field (control) |
| Send Payment Reminder | button | Payment due or overdue | Send reminder to patient (REQ-007-094) | no graph field (control) |
| View Payment Receipt | link | If payment exists | Open payment receipt/invoice | no graph field (control) |
| View Payout Details | link | If payout exists | Open payout details in FR-017 | no graph field (control) |

**Business Rules**:

- Admin has full visibility to all patient and provider information (no masking)
- See REQ-007-051.
- All payment data is read-only except for refund processing and reminder actions (REQ-007-061)
- See REQ-007-052.
- Links to the inquiry, accepted subquote snapshot, parent revision, and booking preserve the audit trail; the current editable quote is not the pricing source. (REQ-007-062)

**Notes**:

- This screen provides comprehensive payment view with full context from patient journey
- UI may use tabs or accordion sections to organize information by stage
- See REQ-007-053.
- This complements FR-006's Booking Detail View (Screen 6) which shows all booking information; this screen focuses specifically on payment details
- Payment status updates in real-time as patient makes payments (REQ-007-051)

---

#### Screen 6: Refund Processing (Admin)

**Purpose**: Process refunds per cancellation policy with full context from booking and payment stages

**Note**: This screen is accessed from Screen 5 (Payment Progress Dashboard) or Screen 5B (Payment Detail View) when admin clicks "Process Refund". It provides comprehensive refund processing with context from previous stages.

**Data Fields** (Continuation from Screen 5/5B, aggregating data from FR-003, FR-004, FR-006, FR-007):

**Section 1: Booking & Cancellation Context** (from FR-006):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Booking Reference | text | Yes | Unique booking reference | Read-only; link to FR-006 booking detail | ENT-booking.id |
| Booking Status | badge | Yes | Current status | Read-only | ENT-booking.status |
| Closure Cause | badge | Conditional | Why the booking closed (FR-006) | Read-only; drives the closure case (REQ-006-053) | ENT-booking.closure_cause |
| Appointment Date | datetime | Yes | Original accepted appointment slot/timezone | Read-only; acceptance snapshot; later intervention retained separately | ENT-booking.appointment_at |
| Accepted Selection | group | Yes | Accepted subquote, parent revision, and package/date context | Read-only; resolved through FR-006 Booking | ENT-booking.accepted_subquote_id, ENT-subquote.package_snapshot, ENT-subquote.included_and_custom_services, ENT-subquote.date_range, ENT-subquote.appointment_at, ENT-subquote.appointment_timezone, ENT-quote.treatment_id |
| Cancellation Date | datetime | Yes | Date of cancellation request | Read-only | ENT-booking.cancellation_requested_at |
| Days Before Procedure | number | Yes | Days until procedure date | Calculated, read-only | ENT-payment.days_before_procedure |
| Cancellation Reason | text | Yes | Reason for cancellation | Read-only; from cancellation request | ENT-booking.cancellation_reason |

**Section 2: Patient Information** (from FR-003):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Patient Name | text | Yes | Full patient name | Read-only | ENT-patient.name |
| Patient Email | text | Yes | Email address | Read-only | ENT-patient.email |
| Patient Phone | text | Yes | Phone number | Read-only | ENT-patient.phone |
| Patient ID | text | Yes | Patient code | Read-only | ENT-patient.anonymized_id |

**Section 3: Accepted Treatment Information** (FR-005 snapshot via FR-006):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Treatment Type | text | Yes | Selected treatment (FUE, FUT, DHI, etc.) | Read-only; inherited accepted parent context | ENT-quote.treatment_id |
| Provider Name | text | Yes | Provider/clinic name | Read-only | ENT-provider.name |
| Accepted Subquote Amount | number | Yes | Original offered price of the accepted subquote | Read-only; acceptance snapshot | ENT-subquote.offered_price |
| Payable Booking Total | number | Yes | Booking amount used by the existing refund policy | Read-only; recorded terms and authorized adjustments; refund percentages unchanged | ENT-booking.payable_total |

**Section 4: Payment Summary** (from FR-007):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Currency | text | Yes | Accepted payment currency | Read-only; locked snapshot | ENT-quote.currency_snapshot |
| Total Paid Amount | number | Yes | Total amount paid by patient | Read-only | ENT-booking.paid_amount |
| Deposit Paid | number | Yes | Deposit amount paid | Read-only | ENT-booking.deposit_paid_amount |
| Final Payment Paid | number | Conditional | Final payment amount paid | Read-only; if paid | ENT-booking.final_payment_paid_amount |
| Payment History | table | Yes | All payments made (deposit, installments, final) with dates and amounts | Read-only | ENT-booking.payment_history |
| Original Payment Methods | list | Yes | Payment methods used (may be multiple if installments) | Read-only | ENT-payment.payment_method |

**Section 5: Refund Calculation** (from FR-006 cancellation policy):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Cancellation Policy | text | Yes | Applicable refund percentage per the FR-029 refund ladder | Read-only; based on timing | ENT-payment.applied_cancellation_policy |
| Refund Percentage | number | Yes | Refund percentage (launch default 90% / 50% / 0%) | Read-only; per the FR-029 refund ladder and FR-006 policy; applies to the amount paid toward the booking total, late payment fees excluded | ENT-payment.refund_percentage |
| Calculated Refund Amount | number | Yes | Refund amount to process | Calculated per the refund case (REQ-007-063); cannot exceed paid amount | ENT-payment.refund_amount |
| Refund Breakdown | text | Yes | Explanation of calculation (e.g., "50% of £3,000 = £1,500") | Read-only; for transparency | ENT-payment.refund_breakdown |

**Section 6: Refund Processing** (Admin Action):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Refund Case | select | Yes | Closure case (from FR-006), exception to the policy, or manual | Defaults to the closure case when the booking closed with a cause; one control for every refund (REQ-007-097) | ENT-payment.refund_case |
| Admin-Set Amount | number | Conditional | Refund amount an admin sets | Open only for an admin-set case (in-treatment provider fault, manual); from zero up to the amount paid | ENT-payment.admin_set_amount |
| Refund Reason | textarea | Yes | Reason for refund | Mandatory audit field; 10 to 500 characters (REQ-007-068) | ENT-payment.refund_reason |
| Refund Destination | select | Yes | Where refund will be sent | Defaults to original payment method; can select alternative | ENT-payment.refund_destination |
| Refund Method | text | Yes | Refund method (original payment method or alternative) | Read-only; based on selection | ENT-payment.refund_method |
| Approval Status | badge | Conditional | Not required, awaiting approval, approved or denied | Read-only; exception and manual refunds only (REQ-007-015) | ENT-payment.approval_status |
| Requested By | text | Conditional | Admin who submitted the refund | Read-only; recorded in the audit entry | ENT-payment.requested_by |
| Decided By | text | Conditional | Other admin with billing permission who approved or denied | Read-only; never the requester | ENT-payment.approved_by |
| Decision Reason | textarea | Conditional | Reason for the approval or denial | 10 to 500 characters; required on denial | ENT-payment.decision_reason |
| Exception Documentation | file | Conditional | Medical emergency documentation or other exception proof | Required if exception to policy | ENT-payment.exception_documentation |
| Process Refund | button | Yes | Confirm and process refund; for an exception or manual refund, submit it for approval | Enabled when all required fields complete (REQ-007-095) | no graph field (control) |

**Section 7: Refund History** (if previous refunds exist):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Previous Refunds | table | Conditional | Previous refunds processed (if any) with dates, amounts, reasons | Read-only; if refunds exist | ENT-booking.refund_history |

**Actions**:

| Action | Type | Condition | Description | Graph field |
|--------|------|-----------|-------------|-------------|
| View Booking Details | link | Always | Open FR-006 booking detail view (full context) | no graph field (control) |
| View Payment Details | link | Always | Open Screen 5B: Payment Detail View | no graph field (control) |
| View Accepted Selection | link | Always | Open the accepted subquote snapshot and inherited parent context via FR-006 | no graph field (control) |
| Cancel Refund | button | Always | Cancel refund processing and return to dashboard | no graph field (control) |
| Process Refund | button | All fields complete | Confirm and process refund (REQ-007-095) | no graph field (control) |
| Approve Refund | button | Refund awaiting approval; signed-in admin is not the requester | Approve the exception or manual refund | no graph field (control) |
| Deny Refund | button | Refund awaiting approval; signed-in admin is not the requester | Deny it; a reason is required, the booking and payment status stay, and the patient is notified (REQ-007-086) | no graph field (control) |

**Business Rules**:

- Screen 6 is the single refund execution control. FR-006 Process Refund and the FR-017 refund action open it (REQ-007-097).
- Closure-case refunds run with no second approval: a full refund with no fee for a provider withdrawal, drop-out, suspension or deactivation; the refund ladder for a patient-request cancellation; the admin-set amount for an in-treatment provider fault (REQ-006-053)
- Refund ladder set in FR-029 (launch default): more than 30 days before procedure 90% refund; 15 to 30 days 50% refund; fewer than 15 days no refund (unless an approved exception, for example a medical emergency). The percentage applies to the amount paid toward the booking total, late payment fees excluded; the cancellation fee is the amount paid less the amount refunded (REQ-007-063, REQ-007-092).
- Approval applies only to an exception refund and a manually entered refund: a different admin with billing permission approves or denies within 2 business days, the refund is awaiting approval until then, and an escalation notice goes to billing admins when the 2 business days pass; nothing is approved or denied automatically (REQ-007-015)
- Exceptions to policy (e.g., medical emergency) require documentation upload and a second admin's approval (REQ-007-064)
- Refund processed to original payment method by default; admin can select alternative method (REQ-007-065)
- Refund amount cannot exceed total paid amount (REQ-007-066)
- All refund actions are auditable with timestamp, actor, reason, and approval chain (REQ-007-067)
- Refund processing updates booking status and notifies patient and provider (REQ-007-069)

**Notes**:

- See REQ-007-063.
- Medical emergency exceptions require documentation upload (medical certificate, doctor's note, etc.)
- This screen provides full context from booking and payment stages to inform refund decisions
- UI should clearly display refund calculation breakdown for transparency
- All sections display data from previous stages to provide complete context for refund processing

---

**Configuration Access**: Admin users who need to view or edit deposit, commission, or payment method settings follow the in-app link to `FR-029: Payment System Configuration`, where those settings are managed. This FR does not duplicate or display that configuration.

---

## Business Rules

### General Module Rules

- Initial payment is required to confirm the accepted subquote's booking: deposit (default 20-30% range, configured via FR-029), eligible first installment per FR-007B, or the full-payment alternative, as chosen among the three payment options (REQ-007-098). Scheduling installments alone is not confirmation.
- Final payment is due the FR-029 balance due days before the procedure (launch default 7). A balance unpaid the day after that date is Overdue, flagged once and notified to billing admins (REQ-007-036)
- While an FR-006 provider fault is pending on a booking, from the fault until the admin's submit on Screen 10, payment and payment reminders against it are blocked (REQ-006-081)
- A payment captured after the hold expired or after a non-provider cancellation is refunded in full automatically (REQ-007-096)
- Full payment option is always available as an alternative to split payments (REQ-007-035)
- Receipts and invoice/payment documents are generated for every successful transaction; FR-017 retains one invoice record per booking, updated for later payments rather than duplicating it per option/charge. (REQ-007-039)
- Provider payout occurs only at release after treatment completion (see Fund Release & Money Routing Rules; payout execution is managed in FR-017) (REQ-007-040)
- **Retry Policy (Constitution-aligned)**: For transient processor/network failures, Payment Service MUST perform up to 3 automatic retries using exponential backoff with jitter (and idempotency) before marking a payment attempt failed; hard declines require explicit patient action to retry. (REQ-007-041)
- Initial payment requires the Initial Payment Guard above, implementing FR-006's pre-booking validation; Payment failure never extends or restarts the slot hold. The slot stays held only until the single hold that started at subquote acceptance expires (FR-026 slot-hold duration, default 48 hours). `Payment Window Expired` blocks further payment against that selection without reopening its parent/subquote; only the FR-006 audited admin revive creates a new hold. Later payments use the confirmed booking and do not require a new acceptance hold. (REQ-007-017, REQ-007-044)
- One booking's payments resolve one accepted subquote and its AcceptanceEvent; payment attempts and callbacks cannot fan out into sibling-option bookings. (REQ-007-077)
- The appointment record is created only on successful initial payment; before that, only the temporary hold keyed by provider, appointment date/time, and time zone exists (FR-006).
- `Payment Window Expired` applies only to the first payment step (acceptance to deposit or first installment), as stated in FR-006. A missed later installment or final payment never causes `Payment Window Expired`, and an unpaid balance cancels the booking only through the FR-006 unpaid balance cancellation (Alternative Flow B8) at the FR-029 Unpaid Balance Cancellation Point, when an admin has set one and only for bookings confirmed after it is set; otherwise it is flagged and notified.
- Provider fault after acceptance follows FR-006 Alternative Flow B5 (Alternative Flow B4 above); on a withdrawal, drop-out, suspension, or deactivation the patient is refunded in full everything paid, and the replacement booking takes a new payment. A treatment already started and interrupted by the provider's fault follows the admin-decided refund in Fund Release & Money Routing Rules. (REQ-007-022)
- All financial events require idempotent handling to prevent duplicates
- Payment records, refunds, and payouts must be immutable once confirmed, with corrective entries for adjustments (REQ-007-078)
- Provide clear user messaging; support retries; ensure idempotency to prevent duplicates
- Patient uses a modern smartphone with reliable internet during payment
- Provider and admin use modern browsers on desktop for financial views

### Data & Privacy Rules

- See system PRD, Platform-Wide Rules: No card numbers stored
- Access to payment data follows RBAC: patients see their own transactions; providers see payout-related booking financials; admins see system-wide financials (REQ-007-071)
- All payment lifecycle events are logged for a tamper-evident audit trail
- Only authenticated patients can pay and view receipts (REQ-007-030)
- Uses patient profile and booking ownership for access
- RBAC enforced across tenants; providers see only payout-related financials for their bookings (REQ-007-071)
- Full audit trail for financial events and administrative actions affecting payouts and refunds
- **Note**: Encryption of payment-related PII, PCI-DSS/GDPR/HIPAA-aligned handling, and the ban on database sharing across tenants are governed by the [system PRD](../../system-prd.md), not restated here

### Admin Editability Rules

**Editable by Admin**:

- **Note**: Commission rates and deposit defaults are managed at system level via **FR-029: Payment System Configuration** (not editable in this module)
- Supported payment methods and currencies (enable/disable) - managed via FR-029 (REQ-007-073)
- Refund approvals and reasons (within FR-006 cancellation policy) (REQ-007-074)
- **Note**: Payout execution is managed in **FR-017: Admin Billing & Financial Management** (not in this module)

**Fixed in Codebase (Not Editable)**: Security controls, financial audit scope, and duplicate-charge protections are governed by the [system PRD](../../system-prd.md), not restated here.

**Configurable with Restrictions**:

- Payment reminder timing: the single payment-reminder setting, owned by this module and read by FR-030; whole days 0 to 14 before the due date, up to 3 reminders, default 3 days before the due date and on the due date (REQ-007-076)
- **Note**: The payout execution timing window is owned by FR-017 (not in this module) (REQ-007-076)

### Payment & Billing Rules

- See REQ-007-002.
- Deposit payment is collected at booking confirmation (admin-configurable percentage, default 20-30% range, configured via FR-029); final payment by its due date, the FR-029 balance due days before the procedure (REQ-007-034)
- Default deposit set to 20-30% range (admin-configurable via FR-029) unless provider-specific override exists
- The FR-029 booking total (accepted price after promotion, from the acceptance snapshot) is the single base for the deposit percentage, instalment amounts, and commission (REQ-007-014, REQ-007-034)
- Refunds follow the FR-006 cancellation policy and the refund ladder set in FR-029 (launch default: >30 days before = 90% refund; 15-30 days before = 50% refund; <15 days before = no refund), unless an approved exception, for example a medical emergency. The percentage applies to the amount paid toward the booking total, late payment fees excluded; the cancellation fee is the amount paid less the amount refunded (REQ-007-063, REQ-007-092)
- See REQ-007-004.
- Patient payment currency and applicable exchange rates come from the accepted snapshot and remain read-only throughout checkout and later payments; provider payout currency follows existing configuration and the locked conversion contract. (REQ-007-059)
- See REQ-007-016 and REQ-007-018.
- The accepted promotion and discounted price are frozen at acceptance (FR-019). Checkout and payment offer no code entry, removal, replacement, or price-changing revalidation; do not mutate the AcceptanceEvent or reapply current promotion settings to payments. See REQ-007-020.
- See REQ-007-010.
- See REQ-007-013.
- See REQ-007-014.
- **Payment status list**: One payment status list, owned by FR-007, is used on every screen that shows a booking's payment status, including the booking, patient-management, and billing screens of FR-003, FR-006, and FR-017: Unpaid, Deposit only, Installments active, Full paid, Refunded. Refunded means all money paid has been returned; a part refund leaves the previous status and shows in the refund history. Overdue is not a status value. It is a separate flag, calculated and not stored: true when the due date has passed and the amount is unpaid, on the booking and on the installment plan. An installment payment's own status keeps its overdue value (FR-007B). Deposit status Partial means only part of the deposit amount has been received and the rest is still due; the booking is not confirmed until the full deposit is paid. (REQ-007-099)
- **Booking payment fields**: FR-007 owns every payment field recorded on the booking; FR-006 keeps the booking status and its cause and reads payment state from FR-007.
- **Processor fees**: See REQ-007-087.

### Fund Release & Money Routing Rules

**Note**: The Payment Routing Spec that the fund-release brief refers to is missing. The Product Owner's four Stripe Connect money-movement decisions below (when the clinic's share moves, how the payment is split, bookings far ahead, pulling money back) replace that missing spec. Release and payout execution are owned by FR-017.

- **Release, part 1 (per booking, at Treatment)**: The provider marks the procedure complete. The patient may confirm, or raise a problem, within a confirmation window (default 7 days; an admin-editable setting). If the patient gives no answer, the booking is released automatically. A problem pauses the release until an admin resolves it. A standalone aftercare payment uses the same window counted from the payment. (REQ-007-089, REQ-007-100)
- **Release, part 2 (per provider)**: Released amounts are paid out through a provider payout pipeline, either by Stripe Connect or by a manual settlement cycle in which an admin marks the payout as paid. Payouts are manual first; Revolut is added later. (REQ-007-089)
- **Seller and balance**: See REQ-007-090.
- **When the clinic's share moves**: See REQ-007-090 and REQ-007-014. For the deposit-and-balance option, the part of the amount paid above Hairline's commission moves at the 60-day mark and each later payment tops it up.
- **Cancellation after the share has moved**: Hairline refunds the patient the amount the closure case sets (REQ-006-053), pulls the share back from the clinic's locked balance, and deducts any shortfall from the clinic's next payout. (REQ-007-091)
- **Reschedule after the share has moved**: See REQ-007-091.
- **Clinic withdrawal and patient cancellation fee**: See REQ-007-092.
- **Treatment interrupted by the provider's fault**: For a treatment already started and interrupted by the provider's fault (FR-006 Alternative Flow B7), an admin reviews each case and sets the patient refund amount, from zero up to the full amount paid, with a mandatory reason and an audit entry. The provider's payout for that booking is held from the fault until the FR-006 route completes; the refund comes out of the held payout, and a shortfall after release is deducted from the provider's next payout (FR-017). (REQ-007-022)
- **Standalone aftercare payment**: No refund ladder applies; an admin decides any refund with a reason as a manual refund, and the provider's money is released after the confirmation window counted from the payment. (REQ-007-100)
- **Refund ladder**: The cancellation refund percentages are an admin setting owned by FR-029 and apply globally (the data model allows a per-clinic ladder later); FR-006 owns the cancellation policy itself.
- Payouts are available to providers within 2 business days after admin execution
- The provider cannot self-execute payouts (payout execution in FR-017)
- Payout execution (FR-017) updates Provider views and generates statements

**Carried from dropped sections (original wording)**:

- **Key attributes**: booking reference, amount, currency, payment method (the saved payment method record owned by FR-007B, which covers bank transfer as well as card), processor fee, status, timestamps, receipt/invoice refs

---

## Dependencies

Related FRs and modules:

- FR-006 Booking & Scheduling: one accepted subquote provides immutable pricing/appointment context; initial successful charge confirms its booking
- FR-004 / FR-005 Quote Structure & Subquote Acceptance: the single accepted commercial choice
- FR-019 Promotions & Discount Management: the accepted promotion is frozen into the acceptance snapshot
- FR-017 Admin Billing & Financial Management: provider payout execution and invoice generation
- FR-029 Payment System Configuration: commission rates, deposit defaults, and the refund ladder are configured at system level
- FR-011 Aftercare & Recovery Management: a standalone aftercare plan is paid for through this module
- P-01 Auth & Profile Management: only authenticated patients can pay and view receipts
- PR-05 Financial Management & Reporting: payout visibility and statements
- S-03 Notification Service: confirmations, reminders, and alerts

---

## User Scenarios & Testing

### User Story 1 - Pay Deposit to Confirm Booking (Priority: P1)

Patient pays deposit to confirm booking and receives immediate confirmation with receipt/invoice.

**Why this priority**: Confirms the booking and unlocks provider commitment; critical for revenue capture.

**Independent Test**: Accept one subquote among multiple providers/parents/options/dates; pay its deposit within the existing hold; verify exactly one confirmed booking, receipt, and invoice with the accepted context.

**Acceptance Scenarios**:

1. **Given** a booking requiring a deposit (admin-configurable percentage, default 20-30% range), **When** the patient pays the deposit successfully, **Then** the booking is marked confirmed and a receipt/invoice is issued and delivered.
2. **Given** a required additional authentication step, **When** the patient completes it successfully, **Then** the payment completes and confirmation is shown within 5 seconds.
3. **Given** a payment failure, **When** the patient retries with a different method, **Then** the system prevents duplicate charges and confirms only a single successful payment.
4. **Given** several parent quotes and sibling subquotes, **When** initial payment is opened, **Then** only the accepted package/services, date range, appointment/timezone, price, promotion, and inherited parent context are shown; no sibling prices are summed or selectable.
5. **Given** the package library or current promotion settings change after acceptance, **When** payment or an invoice is opened, **Then** the accepted snapshot remains unchanged; no code input is shown at checkout, and any request to apply, remove, or replace a code is rejected (FR-019).
6. **Given** an expired/released hold, ineligible selection, or mismatched accepted aggregate versions, **When** initial payment is submitted, **Then** no processor request occurs; FR-006's outcome is shown, and no quote is reopened.
7. **Given** a failed initial payment within its hold, **When** the patient retries, **Then** the same acceptance provenance, currency, and original hold deadline are used; only successful deposit/eligible first installment/full payment confirms the booking.
8. **Given** an accepted booking with a promotion whose usage is reserved, **When** the initial payment succeeds, **Then** the appointment record is created from the hold, the reserved promotion usage is consumed, and the amount and currency charged equal the acceptance snapshot.
9. **Given** a `Payment Window Expired` booking revived by an admin, **When** the patient opens payment, **Then** the deadline shown is the new hold started at the revive time, not an extension of the expired hold.

---

### User Story 2 - Pay Final Balance by Its Due Date (Priority: P1)

Patient completes the final payment by its due date and receives confirmation.

**Why this priority**: Ensures full payment is secured, reducing on-site friction.

**Independent Test**: For a confirmed booking with remaining balance, complete final payment and verify updated status and receipt/invoice.

**Acceptance Scenarios**:

1. **Given** a confirmed booking with a remaining balance, **When** the patient pays the final amount, **Then** the booking is marked fully paid and a final receipt/invoice is delivered.
2. **Given** a final payment due date, **When** it is approaching within 3 days, **Then** the patient receives a reminder notification.
3. **Given** a confirmed booking paid through deposit/installments, **When** final payment is calculated, **Then** the balance uses its recorded payable terms and actual successful payments/adjustments, retaining the original accepted selection and currency; no new acceptance hold is required.
4. **Given** a confirmed booking whose final payment is overdue, **When** the due date passes, **Then** the booking is flagged and the admin notified; the booking does not become `Payment Window Expired` and is not cancelled.

---

### User Story 3 - Process Refund per Policy (Priority: P2)

Admin processes a refund request according to cancellation policy; patient and provider are notified.

**Why this priority**: Required for trust and policy compliance.

**Independent Test**: Cancel a booking at different time windows; verify calculated refund and notifications.

**Acceptance Scenarios**:

1. **Given** a cancellation 20 days before procedure, **When** admin approves refund, **Then** the system refunds 50% (the launch default of the refund ladder, FR-029) and updates booking/payment status with audit log.
2. **Given** an exception refund request for a cancellation 5 days before procedure, **When** a different admin denies it, **Then** the system records the decision with reason and notifies the patient. (REQ-007-086)

---

### Edge Cases

- Payment challenge required but device/app loses focus; flow must resume gracefully (REQ-007-080)
- Duplicate submission from rapid taps; idempotency ensures single charge (REQ-007-085)
- Patient locale/system currency or market exchange rate changes after acceptance; payment currency/rates remain the accepted values, not a new checkout selection
- Hold expires during an authentication challenge; retry cannot extend/recreate the hold or bypass FR-006 eligibility; only an FR-006 audited admin revive starts a new hold (REQ-007-043)
- Provider withdraws or drops out after the deposit is paid; FR-006 Alternative Flow B5 applies and the patient is refunded in full everything paid with no fee; the replacement booking takes a new payment
- Duplicate or late processor callbacks must not create another booking, replace the accepted choice, or bypass FR-006's confirmation rules; reconcile financial events under the existing payment/booking owners
- Accepted pricing lacks optional component itemization; show the complete offered price without inventing treatment/package components (REQ-007-079)
- Refund requested outside policy window; admin records exception with documentation (REQ-007-064)
- A payment succeeds after the hold expired or after a non-provider cancellation; it does not confirm the booking and is refunded in full automatically (REQ-007-096)
- No admin decides an exception or manual refund within 2 business days; billing admins get an escalation notice and the refund stays awaiting approval (REQ-007-015)
- Payout blocked while the provider has not marked the procedure complete or a problem case is open; release waits until completion is marked or an admin resolves the case (REQ-007-058)

---

## Functional Requirements Summary

### Core Requirements

- **REQ-007-001**: System MUST allow patients to pay the accepted subquote's booking by one of three options (REQ-007-098): in full now, a deposit now with the balance by its due date, or installments per FR-007B; the first successful charge confirms the same booking.
- **REQ-007-002**: System MUST support card and bank transfer methods for payments
- **REQ-007-003**: System MUST support multiple currencies (at minimum USD, EUR, GBP, TRY) and display accurate totals
- **REQ-007-004**: System MUST generate and deliver receipts/invoices for successful payments and refunds
- **REQ-007-005**: System MUST confirm the existing accepted-selection booking only on a successful initial charge (deposit, eligible first installment, or full payment), mark it fully paid when its balance is settled, and process duplicate callbacks idempotently.

### Data Requirements

- **REQ-007-006**: System MUST maintain complete payment history per booking, including refunds and payout references
- **REQ-007-007**: System MUST compute platform commission per transaction and link to provider payout records
- **REQ-007-016**: All payment, receipt/invoice, provider/admin financial-detail, and refund views MUST use one FR-006 Booking's immutable accepted subquote snapshot as the commercial base; exclude sibling alternatives/live library prices and prevent component double-counting. The accepted promotion and discounted price are read from the snapshot and never recomputed; no promotion code can be entered, removed, or replaced at checkout or payment.
- **REQ-007-019**: Payment history MUST resolve through its booking to the AcceptanceEvent, accepted parent/subquote IDs, equal aggregate versions, selected option/date-price provenance, and original snapshot; subsequent authorized admin interventions (FR-006 revive, appointment change, cancellation, and provider-fault transfer) remain separately recorded.
- **REQ-007-087**: A processor fee on a payment or a refund MUST be recorded on that payment's or refund's own record. Fees on transfers and payouts are recorded in FR-017, which shows both in its per-booking reconciliation view.

### Security & Privacy Requirements

- **REQ-007-008**: Retired. See system PRD, Platform-Wide Rules: No card numbers stored
- **REQ-007-009**: System MUST log all financial events with actor, timestamp, booking ID, and outcomes
- **REQ-007-010**: System MUST support additional authentication for payments when required by issuer/regulation

### Integration Requirements

- **REQ-007-011**: System MUST support processor-driven payment flows for authorization, capture, and refund
- **REQ-007-012**: System MUST support release of the clinic's share and its payout with commission deduction and statement generation, per Fund Release & Money Routing Rules (payout execution is owned by FR-017)
- **REQ-007-017**: Before initial processor submission, system MUST validate FR-006 selection eligibility, accepted versions, and exclusive unexpired hold ownership; invalid handoffs are blocked and hold expiry follows `Payment Window Expired`, without hold extension or quote reopening. Payment failure MUST NOT extend or restart the hold; only the FR-006 audited admin revive creates a new hold. Later confirmed-booking payments do not acquire a new acceptance hold.
- **REQ-007-018**: System MUST read the payment amount and the accepted patient currency/exchange-rate from the FR-005 accepted snapshot for initial and subsequent payments, never recomputed; checkout cannot change these values or reselect package/date/appointment/quote price.
- **REQ-007-020**: On the first successful initial payment, System MUST confirm the booking, create its appointment record from the hold (FR-006), and, for a provider-selected promotion or patient-entered code, consume the promotion use reserved at acceptance (FR-019 REQ-019-014). An automatic promotion's use is consumed at acceptance and follows FR-019 REQ-019-015.
- **REQ-007-021**: `Payment Window Expired` MUST apply only to the first payment step, as stated in FR-006 (REQ-006-016). A missed later installment or final payment MUST NOT cause `Payment Window Expired`, booking cancellation, or inquiry cancellation.
- **REQ-007-022**: When a provider fault after acceptance closes a booking (FR-006 Alternative Flow B5), System MUST block further payment against it. When the provider withdraws, drops out, or is suspended or deactivated (FR-006 Alternative Flow B4), the patient is refunded in full everything paid, with no patient fee, and the replacement booking takes a new payment. For a treatment already started and interrupted by the provider's fault, an admin MUST review the case and set the patient refund amount, from zero up to the full amount paid, with a mandatory reason and an audit entry, and the provider's payout for that booking MUST be held until the admin decides (see Fund Release & Money Routing Rules). Detailed refund and fund-release mechanics are defined in FR-007B and FR-017.
- **REQ-007-088**: System MUST process the payment for a standalone aftercare plan (FR-011). The patient pays only after an admin has assigned a provider and that provider has configured the plan; the successful payment activates the aftercare.
- **REQ-007-089**: Provider money MUST be released in two parts (see Fund Release & Money Routing Rules): release per booking at Treatment, after the patient's confirmation window with no problem raised (default 7 days, admin-editable) or after an admin resolves a problem case, then payout per provider (FR-017).
- **REQ-007-090**: Hairline MUST be the seller on the card payment and hold the payment; the clinic's share moves to the clinic's locked Stripe balance 60 days before the scheduled treatment date (30 days for an installment plan once fully paid), or right away when less time remains at payment, and is paid out at release. For the deposit-and-balance option, the part of the amount paid that is above Hairline's commission moves at the 60-day mark and each later payment tops it up. Hairline's balance pays refunds, chargebacks, and Stripe fees first and recovers the clinic's part afterwards.
- **REQ-007-091**: When a cancellation or a reschedule happens after the clinic's share has moved, the share MUST be pulled back (see Fund Release & Money Routing Rules): on cancellation the patient is refunded the amount the closure case sets (REQ-006-053) and any shortfall is deducted from the clinic's next payout; on reschedule the share moves again 60 or 30 days before the new date.
- **REQ-007-092**: When a clinic withdraws or drops out after acceptance (FR-006 Alternative Flow B5), a fixed charge set in admin settings MUST be deducted from the clinic's next payout. The patient cancellation fee is the amount paid toward the booking total less the amount refunded. It MUST be split between Hairline and the clinic by a percentage set in admin settings. Neither setting has a starting value; an admin sets it.

### Refunds, Options and Status Requirements

- **REQ-007-096**: A payment captured after the hold expired, or after the booking was cancelled for a cause other than a provider fault, is recorded and does not confirm or revive the booking. System MUST refund it in full automatically, write an audit entry and notify the patient, with no admin approval.
- **REQ-007-097**: Every refund is executed on Screen 6. The admin picks the case: a closure case (the amount follows the FR-006 closure cause, REQ-006-053), an exception to the policy, or a manual refund. The amount field is open only for an admin-set case (in-treatment provider fault, manual), from zero up to the amount paid. FR-006 Process Refund and the FR-017 refund action open this screen instead of running their own refund.
- **REQ-007-098**: The patient chooses one of three payment options on FR-006 Screen 1: pay in full now, a deposit now with the balance later, or installments (2 to 9, FR-007B). FR-007 Screen 1 shows the chosen option read-only. The first successful charge of the chosen option confirms the booking.
- **REQ-007-099**: Payment status values: Unpaid (nothing paid), Deposit only (deposit paid, balance not), Installments active (plan started, not fully paid), Full paid (whole payable total paid), Refunded (all money paid has been returned; a part refund leaves the previous status and shows in the refund history). Deposit status Partial means only part of the deposit amount has been received and the rest is still due; the booking is not confirmed until the full deposit is paid. At Risk is not a status.
- **REQ-007-100**: For a standalone aftercare payment (REQ-007-088) no refund ladder applies: an admin decides any refund with a reason on Screen 6 as a manual refund (REQ-007-015). The provider's money is released after the same patient confirmation window as a booking, counted from the date of the payment instead of procedure completion.

### Marking Unclear Requirements

- **REQ-007-013**: Platform is Merchant of Record; platform issues patient invoices, manages refunds and tax implications, and pays out net to providers
- **REQ-007-014**: Commission is calculated on the accepted price after promotion (the FR-029 booking total) using the commission type (Percentage or Flat Rate) and value from the snapshot taken at booking confirmation. Hairline keeps the commission first, before the clinic's share moves; only the net share moves to the clinic and is paid out at release after treatment completion; not pro‑rata across deposit/final
- **REQ-007-015**: Admin approval applies only to an exception refund and a manually entered refund. The approver is any other admin with billing permission, never the requester, and approves or denies within 2 business days; until then the refund is awaiting approval. When 2 business days pass with no decision, System sends an escalation notice to billing admins and never approves or denies on its own. A closure-case refund (REQ-006-053) runs with no second approval. The requester, approver, decision and reason are logged and notifications sent

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-11-22 | 1.13 | Requirements graph programme baseline: PRD compressed to the checklist structure (each rule stated once, field rows tagged with graph field ids, dropped classes removed). No rule changes. Earlier history (v1.0 to v1.12) and the change requests CR-FR007-20261013-01 and CR-FR007-20261016-01 are in `archived/prd-baseline-2026-11-08/fr007-payment-processing/` and in git history. | Product Owner / Documentation |
| 2026-11-23 | 1.14 | Independent compression review: 1 clause(s) from dropped sections restored in original wording under Business Rules. No rule changes. | Product Owner / Documentation |
| 2026-11-23 | 1.15 | Logic review of the payment rules. One due date for the final payment (the FR-029 balance due days before the procedure), Overdue from the next day with a scheduled trigger and billing-admin notice, and reminder timing as an admin setting of 0 to 14 days, up to 3. An unpaid balance cancels a booking only at the FR-029 Unpaid Balance Cancellation Point, shown on Screen 2 when set. Refund approval now applies only to exception and manual refunds, needs a different admin with billing permission, has a Deny action, an awaiting-approval state and an escalation notice after 2 business days; closure-case refunds need no second approval. Screen 6 is the single refund control with a refund case selector and an admin-set amount; one reason rule of 10 to 500 characters. The ladder applies to the amount paid, late fees excluded, and the cancellation fee is the amount paid less the amount refunded. The clinic share for the deposit-and-balance option moves above Hairline's commission and is topped up by later payments. Payout eligibility waits for the confirmation window. Three payment options shown on Screen 1. A payment captured when the booking is not payable is refunded in full automatically. Payment status list drops At Risk and defines Refunded and the deposit Partial state. A standalone aftercare payment flow, an in-treatment fault payout hold and refund steps, retry and replacement steps wired, and the duplicate revive step retired in favour of FR-006. | Product Owner / Documentation |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner — v1.6 documentation delta | Joachim Trung Tuan | 2026-10-13 | Approved to complete remaining Meeting 2 quote-model work; implementation reconciliation and consolidated verification pending. |
| Product Owner — v1.7 documentation delta | Joachim Trung Tuan | 2026-10-16 | Approved via the MTG-002 quote-model decision log; implementation reconciliation and consolidated verification pending. |
| Product Owner — v1.8 documentation delta | Joachim Trung Tuan | 2026-10-16 | Approved via the MTG-002 Product Owner follow-up decisions; implementation reconciliation and consolidated verification pending. |
| Product Owner — v1.10 documentation delta | Product Owner | 2026-10-18 | Approved v1.10 via MTG-002 decision log (documentation only) |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0
**Based on**: FR-007 Payment Processing (system-prd.md)
**Last Updated**: 2026-11-23
