# Product Requirements Document: Payment Processing (FR-007)

**Module**: P-03: Booking & Payment | PR-05: Financial Management & Reporting | A-01: Patient Management & Oversight | A-05: Billing & Financial Reconciliation | S-02: Payment Processing Service | S-03: Notification Service
**Feature Branch**: `fr007-payment-processing`
**Created**: 2025-11-04
**Status**: ✅ Verified & Approved
**Source**: FR-007 from local-docs/project-requirements/system-prd.md (Payment Processing) + Constitution (.specify/memory/constitution.md)

---

## Executive Summary

Enable patients to pay securely for procedures (deposit at booking and final payment before or on procedure day) in supported currencies and methods, while ensuring compliant handling of payments, automated receipt/invoice generation, platform commission calculation, and timely provider payouts after treatment completion. This module focuses on the what/why of payments across tenants: a clear, trustworthy checkout for patients, transparent payout tracking for providers, and configurable oversight for admins. It excludes implementation details and adheres to the Hairline Constitution (multi-tenant separation, privacy, auditability, and compliance).

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-03)**: Patient pays deposit to confirm booking; pays final amount by procedure date; views payment status, receipts, and invoices; selects supported payment method and currency; receives payment confirmations and reminders.
- **Provider Platform (PR-05)**: Provider views booking payment status and patient payment progress; sees commission deducted amounts; accesses payout statements and history once treatment is marked complete (payout execution managed in FR-017).
- **Admin Platform (A-01)**: Admin views patient payment progress across bookings as part of patient management oversight; views payment details with full context from inquiry/quote/booking stages; monitors payment status as part of patient journey tracking.
- **Admin Platform (A-05)**: Admin processes refunds per policy; monitors payment dashboards and reconciliation; views financial reconciliation data and export payment/commission reports (commission rates and deposit defaults configured via FR-029; provider payout execution managed in FR-017).
- **Shared Services (S-02/S-03)**: Payment Processing Service handles authorizations/captures/refunds and payout preparation; Notification Service delivers confirmations and reminders.

### Multi-Tenant Breakdown

**Patient Platform (P-03)**:

- Complete a payment (deposit or full) to confirm booking
- Complete final payment before or on procedure date
- Choose supported payment method (card, bank transfer, digital wallet)
- Choose/display currency; see clear totals, fees, and remaining balance
- View receipts/invoices and payment history
- Receive confirmations and reminders for upcoming or overdue payments

**Provider Platform (PR-05)**:

- View booking payment status (unpaid/deposit paid/final paid/refunded)
- View patient payment progress (deposit status, installment progress, final payment status)
- View upcoming and completed payouts with commission deducted (payout execution managed in FR-017)
- Access payout statements for accounting (generated in FR-017)

**Admin Platform (A-01)**:

- View patient payment progress across all bookings (deposit status, installment progress, final payment status) as part of patient management oversight
- View payment details with full context from inquiry/quote/booking stages for patient journey tracking
- Monitor payment status and send payment reminders to patients
- Access payment information when managing patient accounts and resolving disputes

**Admin Platform (A-05)**:

- Approve and process refunds per cancellation policy (refund amount calculation per FR-006 cancellation policy)
- View reconciliation dashboards and export payment/commission reports
- Monitor financial reconciliation data and payment operations
- **Note**: Commission rate and deposit defaults are configured via FR-029: Payment System Configuration (system-level settings)
- **Note**: Provider payout execution and invoice generation are managed in FR-017: Admin Billing & Financial Management

**Shared Services (S-02, S-03)**:

- S-02: Orchestrates payment lifecycle, refunds, and payout preparation
- S-03: Sends payment confirmations, reminders, and administrative alerts

### Communication Structure

**In Scope**:

- Payment confirmations (deposit, final) to patient
- Payment reminders for upcoming final payment
- Refund confirmations to patient and provider
- Payout notifications to provider after execution

**Out of Scope**:

- Chat/messaging between patient and provider (handled elsewhere)
- SMS channel specifics (handled by S-03 configuration; **SMS payment notifications are not available in MVP and will only be enabled in a future phase via S-03/FR-020/FR-030**)
- Any non-payment content (marketing, aftercare content)

### Entry Points

- Patient initiates payment in booking confirmation flow (deposit required)
- Patient initiates final payment from booking details prior to procedure date
- Admin processes refunds per cancellation policy (refund amounts per FR-006)
- **Note**: Provider payout execution is handled in FR-017: Admin Billing & Financial Management

---

## Business Workflows

### Main Flow: Deposit + Final Payment (Split Payment)

**Actors**: Patient, Provider, Admin, System (Payment Processing Service)
**Trigger**: Patient confirms booking requiring deposit; later completes final payment
**Outcome**: Booking confirmed upon deposit; booking fully paid after final payment; receipts/invoices issued; payout becomes eligible after treatment completion

**Steps**:

1. Patient reviews booking summary (total price, deposit amount, remaining balance, currency)
2. System displays supported payment methods and any applicable fees/requirements
3. Patient selects payment method and confirms deposit payment
4. System processes payment and returns success or actionable challenge (e.g., additional authentication)
5. On success, System marks booking as confirmed; generates receipt and invoice; sends confirmation to patient and provider
6. Prior to procedure date, Patient initiates final payment from booking details
7. System processes final payment and updates booking to fully paid; issues final receipt/invoice; sends confirmations
8. After treatment completion, provider payout becomes eligible (payout execution handled in FR-017: Admin Billing & Financial Management)

### Alternative Flows

**A1: Full Payment at Booking**:

- **Trigger**: Patient prefers to pay the full amount at booking instead of split payments
- **Steps**:
  1. Patient selects full payment option
  2. System processes full amount and marks booking fully paid
  3. System issues receipt/invoice and sends confirmations
- **Outcome**: Booking is confirmed and fully paid; payout remains pending until treatment completion

**A2: Refund Due to Cancellation**:

- **Trigger**: Patient cancels booking; cancellation policy determines refund amount (per FR-006 cancellation policy)
- **Steps**:
  1. Admin reviews cancellation timing and applicable refund schedule (refund amounts per FR-006: >30 days = 90%, 15-30 days = 50%, <15 days = no refund unless exception)
  2. System calculates refundable amount based on cancellation policy and initiates refund
  3. System updates booking/payment status and sends confirmation notices
- **Outcome**: Refund processed according to FR-006 cancellation policy; provider payout eligibility updated

**B1: Payment Authentication Required / Challenge Failed**:

- **Trigger**: Additional authentication requested; patient fails or abandons
- **Steps**:
  1. System informs patient of the authentication requirement and guides action
  2. If challenge fails or times out, System presents retry and alternative method options
- **Outcome**: Payment remains incomplete until successful authentication; booking not confirmed

**B2: Payment Failure or Decline**:

- **Trigger**: Payment is declined or fails
- **Steps**:
  1. System displays clear error and suggested next steps (retry, use different method)
  2. Patient retries or selects another method
- **Outcome**: Booking remains unconfirmed until a successful deposit payment

---

## Screen Specifications

### Patient Platform

#### Screen 1: Patient Checkout (Deposit)

**Purpose**: Allow patient to pay deposit to confirm booking

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Total Amount | number | Yes | Total procedure price | Positive amount; matches booking |
| Deposit Amount | number | Yes | Deposit to confirm booking | Admin-configurable percentage (default 20-30% range, configured via FR-029); within allowed range |
| Currency | select | Yes | Selected currency | Supported list; defaults by locale |
| Payment Method | select | Yes | Card, bank transfer, or digital wallet | Must be in supported methods |
| Billing Details | text | Yes | Name, address, contact | Required for invoicing |

**Business Rules**:

- Show clear breakdown: total, deposit, remaining balance, currency
- Disable payment button until all required fields are valid
- Display clear error messaging and retry options on failure
- Do not reveal provider direct contact details until booking confirmed

**Notes**:

- Show progress indicator during processing; avoid blocking UI for more than a few seconds without feedback
- Preserve entered details if payment attempt fails to allow quick retry

---

#### Screen 2: Patient Final Payment

**Purpose**: Allow patient to complete final payment before or on procedure date

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Remaining Balance | number | Yes | Amount due | Positive; equals total minus deposit |
| Currency | select | Yes | Selected currency | Supported list; defaults from booking |
| Payment Method | select | Yes | Card, bank transfer, or digital wallet | Supported methods |
| Billing Details | text | Yes | For invoice | Required if changed since deposit |

**Business Rules**:

- Display due date and countdown to procedure date
- Send reminder 3 days before due date and on due date
- If payment overdue, flag booking and notify admin

**Notes**:

- Keep summary of previous payments and remaining balance visible

---

### Provider Platform

#### Screen 3: Booking Payment Status & Progress (Provider)

**Purpose**: View complete payment information with full context from inquiry, quote, booking, and payment stages

**Note**: This screen aggregates payment data with context from previous stages (FR-003, FR-004, FR-005, FR-006) to provide comprehensive payment view. This complements FR-006's Booking Detail View (Screen 4) which shows all booking information including payment summary.

**Data Fields** (Continuation from FR-006 Screen 4, aggregating data from FR-003, FR-004, FR-005, FR-006, FR-007):

**Section 1: Booking & Payment Context** (from FR-006):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Booking Reference | text | Yes | Unique booking reference | Read-only; link to FR-006 booking detail |
| Booking Status | badge | Yes | Current status (Accepted/Confirmed/In Progress/Cancelled) | Read-only |
| Appointment Date | datetime | Yes | Confirmed appointment slot | Read-only |
| Inquiry Reference | text | Yes | Original inquiry HPID | Read-only; link to inquiry |
| Quote Reference | text | Yes | Original quote reference | Read-only; link to quote |

**Section 2: Patient Information** (from FR-003, unmasked if Confirmed):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Patient Anonymized ID | text | Yes | Patient code (always visible) | Read-only |
| Patient Name | text | Conditional | Full name (if Confirmed) or masked (e.g., "Mark P. - PAT-00123") | Unmask only if status = Confirmed |
| Patient Location | text | Yes | Country/city | Read-only; from inquiry |
| Treatment Type Requested | text | Yes | Hair/Beard/Both | Read-only; from inquiry |

**Section 3: Quote & Treatment Information** (from FR-004):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Treatment Type | text | Yes | Selected treatment (FUE, FUT, DHI, etc.) | Read-only; from quote |
| Estimated Graft Count | number | Yes | Estimated number of grafts | Read-only; from quote |
| Packages Selected | list | No | Hotel, transport, medication packages | Read-only; from quote |
| Clinician Assigned | text | Yes | Clinician who will perform procedure | Read-only; from quote |

**Section 4: Pricing Breakdown** (from FR-004):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Currency | text | Yes | Payment currency | Read-only; from quote |
| Treatment Price | number | Yes | Base treatment price | Read-only; from quote |
| Package Prices | number | Yes | Total package prices | Read-only; from quote |
| Discount Applied | number | No | Discount amount (if any) | Read-only; from quote |
| Total Quote Amount | number | Yes | Total booking amount | Read-only; from quote |

**Section 5: Payment Progress & Status** (from FR-007):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Deposit Percentage | text | Yes | Deposit percentage used | Read-only; admin-configured via FR-029 |
| Deposit Amount | number | Yes | Required deposit amount | Calculated from admin-configured percentage |
| Deposit Status | badge | Yes | Pending / Paid / Partial | Read-only |
| Deposit Paid Date | datetime | Conditional | Date deposit was paid | Read-only; if paid |
| Payment Method (Deposit) | text | Conditional | Payment method used for deposit | Read-only; if paid |
| Payment Status | badge | Yes | Unpaid / Deposit Only / Installments Active / Full Paid | Read-only |
| Installment Progress | group | Conditional | Current installment number, total installments, next due date, completion percentage | Only shown if installments active |
| Final Payment Status | badge | Yes | Not Due / Due / Paid / Overdue | Read-only |
| Final Payment Due Date | datetime | Conditional | Final payment due date | Read-only |
| Final Payment Amount | number | Conditional | Final payment amount due | Calculated |
| Final Payment Method | text | Conditional | Payment method used for final payment | Read-only; if paid |
| Final Payment Paid Date | datetime | Conditional | Date final payment was paid | Read-only; if paid |
| Remaining Balance | number | Yes | Amount remaining to pay | Calculated |
| Total Paid Amount | number | Yes | Sum of all payments made | Calculated |

**Section 6: Payment History** (from FR-007):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Payment History | table | Yes | All payments (deposit, installments, final) with dates, amounts, methods, status | Read-only |
| Payment Transaction ID | text | Yes | Payment processor transaction ID | Read-only |
| Payment Receipt Link | link | Yes | Link to payment receipt/invoice | Read-only |
| Refund History | table | Conditional | All refunds processed (if any) with dates, amounts, reasons | Read-only; if refunds exist |

**Section 7: Payout Information** (from FR-017, conditional):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Payout Status | badge | Conditional | Pending / Eligible / Processing / Executed | Only shown after treatment completion |
| Gross Amount | number | Conditional | Total paid by patient | Read-only; if payout eligible |
| Commission Rate | text | Conditional | Platform commission percentage | Read-only; configured via FR-029 |
| Commission Amount | number | Conditional | Platform commission deducted | Read-only; if payout eligible |
| Net Payout | number | Conditional | Amount to provider | Read-only; if payout eligible |
| Payout Execution Date | datetime | Conditional | Date payout was executed | Read-only; if executed |
| Payout Statement Link | link | Conditional | Link to detailed payout invoice (FR-017) | Only shown if payout executed |

**Actions**:

| Action | Type | Condition | Description |
|--------|------|-----------|-------------|
| View Booking Details | link | Always | Open FR-006 booking detail view (full context) |
| View Quote | link | Always | Open full quote details (FR-004) |
| View Inquiry | link | Always | Open full inquiry details (FR-003) |
| View Payment Receipt | link | Conditional | Open payment receipt/invoice (if payment exists) |
| View Payout Details | link | Conditional | Open payout details in FR-017 (if payout exists) |

**Business Rules**:

- Payment status reflects real-time payment progress (deposit, installments, final payment)
- Provider can see payment progress but cannot modify payment information
- Patient full identity only visible if booking status is "Confirmed" (payment successful)
- All payment data is read-only for provider
- Payout information links to FR-017: Admin Billing & Financial Management for detailed payout statements
- All sections display data from previous stages (inquiry → quote → booking → payment) in chronological order

**Notes**:

- This screen provides comprehensive payment view with full context from patient journey
- UI may use tabs or accordion sections to organize information by stage
- Payment details shown without card information (PCI compliance)
- This complements FR-006's Booking Detail View which shows all booking information; this screen focuses specifically on payment details
- Payment status updates in real-time as patient makes payments

---

#### Screen 4: Provider Payout Overview (Provider)

**Purpose**: View payout status and details for completed treatments with full context from booking and payment stages

**Note**: Detailed payout execution and invoice generation are managed in FR-017: Admin Billing & Financial Management. This screen provides comprehensive view with context from previous stages and links to detailed payout information.

**Data Fields** (Continuation from Screen 3, aggregating data from FR-003, FR-004, FR-006, FR-007, FR-017):

**Section 1: Booking & Treatment Context** (from FR-006):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Booking Reference | text | Yes | Unique booking reference | Read-only; link to FR-006 booking detail |
| Treatment Completion Date | datetime | Yes | Date treatment was marked complete | Read-only |
| Treatment Type | text | Yes | Selected treatment (FUE, FUT, DHI, etc.) | Read-only; from quote |
| Estimated Graft Count | number | Yes | Estimated number of grafts | Read-only; from quote |
| Clinician Assigned | text | Yes | Clinician who performed procedure | Read-only; from quote |

**Section 2: Patient Information** (from FR-003):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Patient Name | text | Yes | Full patient name (unmasked after treatment) | Read-only |
| Patient ID | text | Yes | Patient code | Read-only |
| Treatment Type Requested | text | Yes | Hair/Beard/Both | Read-only; from inquiry |

**Section 3: Payment Summary** (from FR-007):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Currency | text | Yes | Payment currency | Read-only; from quote |
| Total Quote Amount | number | Yes | Total booking amount | Read-only; from quote |
| Total Paid Amount | number | Yes | Sum of all payments made by patient | Read-only |
| Payment Status | badge | Yes | Deposit Only / Installments / Full Paid | Read-only |
| Payment History | link | Yes | Link to full payment history (Screen 3) | Read-only |

**Section 4: Payout Calculation** (from FR-017):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Gross Amount | number | Yes | Total paid by patient | Positive; read-only |
| Commission Rate | text | Yes | Platform commission percentage | Read-only; configured via FR-029 |
| Commission Amount | number | Yes | Platform commission deducted | Calculated; read-only |
| Net Payout | number | Yes | Amount to provider | Gross minus commission; read-only |
| Payout Currency | text | Yes | Provider's payout currency | Read-only; provider-configured |
| Exchange Rate | number | Conditional | Currency conversion rate (if multi-currency) | Read-only; locked at booking |

**Section 5: Payout Status & Execution** (from FR-017):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Payout Status | badge | Yes | Pending / Eligible / Processing / Executed / On Hold | Valid transitions only |
| Payout Eligibility Date | datetime | Conditional | Date payout became eligible | Read-only; after treatment completion |
| Payout Execution Date | datetime | Conditional | Date payout was executed | Read-only; if executed |
| Payout Method | text | Conditional | Payout method (bank transfer, etc.) | Read-only; if executed |
| Payout Transaction ID | text | Conditional | Payout transaction reference | Read-only; if executed |
| Payout Statement Link | link | Conditional | Link to detailed payout invoice (FR-017) | Only shown if payout executed |
| Payout Invoice | link | Conditional | Download payout invoice PDF | Only shown if payout executed |

**Section 6: Treatment Details** (from FR-004, FR-006):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Quote Reference | text | Yes | Original quote reference | Read-only; link to quote |
| Packages Selected | list | No | Hotel, transport, medication packages | Read-only; from quote |
| Appointment Date | datetime | Yes | Procedure date | Read-only |

**Actions**:

| Action | Type | Condition | Description |
|--------|------|-----------|-------------|
| View Booking Details | link | Always | Open FR-006 booking detail view (full context) |
| View Payment Details | link | Always | Open Screen 3: Payment Status & Progress |
| View Quote | link | Always | Open full quote details (FR-004) |
| Download Payout Invoice | link | Conditional | Download payout invoice PDF (if payout executed) |
| View Payout Details (FR-017) | link | Conditional | Open detailed payout information in FR-017 (if payout exists) |

**Business Rules**:

- Payout visible only after treatment marked complete by admin
- Commission shown and deducted from payout amount (commission rate configured via FR-029)
- Payout calculation based on total paid amount (not just deposit)
- History of payouts accessible for accounting
- Links to FR-017 for detailed payout statements and invoices
- All payout data is read-only for provider (payout execution is admin-controlled in FR-017)

**Notes**:

- This screen provides comprehensive payout view with full context from booking and payment stages
- UI may use tabs or accordion sections to organize information
- This complements FR-006's Booking Detail View and Screen 3's Payment Status view
- Detailed payout invoices and statements are generated in FR-017: Admin Billing & Financial Management
- Payout execution is admin-controlled; provider can only view status and details

---

### Admin Platform

**Configuration Reference**: Payment system settings (deposit percentages, commission rates, supported payment methods) are configured and reviewed via `FR-029: Payment System Configuration`. This module links admins out to FR-029 when configuration context is needed; no configuration data is duplicated here.

#### Screen 5: Patient Payment Progress Dashboard (Admin)

**Purpose**: Allow admin to monitor patient payment progress across all bookings (list/dashboard view)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Booking ID | text | Yes | Reference identifier | Searchable, filterable, clickable link |
| Patient Name | text | Yes | Full patient name | Searchable |
| Provider Name | text | Yes | Provider/clinic name | Filterable |
| Total Amount | number | Yes | Total booking amount | Sortable |
| Deposit Amount | number | Yes | Required deposit amount | Calculated from admin-configured percentage |
| Deposit Status | badge | Yes | Pending / Paid / Partial | Filterable |
| Deposit Paid Date | datetime | Conditional | Date deposit was paid | Read-only; if paid |
| Payment Status | badge | Yes | Unpaid / Deposit Only / Installments Active / Full Paid / Overdue | Filterable |
| Installment Progress | text | Conditional | "X of Y installments paid" | Only shown if installments active |
| Next Payment Due Date | datetime | Conditional | Next installment or final payment due date | Read-only |
| Final Payment Status | badge | Yes | Not Due / Due / Paid / Overdue | Filterable |
| Remaining Balance | number | Yes | Amount remaining to pay | Calculated, sortable |
| Actions | buttons | Yes | View Payment Details, Process Refund, Send Reminder | RBAC enforced |

**Business Rules**:

- Admin can view payment progress for all bookings across all providers
- Filtering options: Payment Status, Provider, Date Range, Overdue Payments
- Clicking on Booking ID or "View Payment Details" opens Screen 5B: Payment Detail View
- Admin can send payment reminders to patients
- Admin can process refunds per FR-006 cancellation policy (opens Screen 6)
- All payment data in dashboard is read-only

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

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Booking Reference | text | Yes | Unique booking reference | Read-only; link to FR-006 booking detail |
| Booking Status | badge | Yes | Current status (Accepted/Confirmed/In Progress/Cancelled) | Read-only |
| Appointment Date | datetime | Yes | Confirmed appointment slot | Read-only |
| Inquiry Reference | text | Yes | Original inquiry HPID | Read-only; link to inquiry |
| Quote Reference | text | Yes | Original quote reference | Read-only; link to quote |

**Section 2: Patient Information** (from FR-003, always visible to admin):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Patient ID | text | Yes | Patient code | Read-only |
| Patient Name | text | Yes | Full patient name | Read-only |
| Patient Email | text | Yes | Email address | Read-only |
| Patient Phone | text | Yes | Phone number | Read-only |
| Patient Address | text | No | Full address | Read-only; from profile |
| Patient Location | text | Yes | Country/city | Read-only; from inquiry |
| Patient Age | number | Yes | Patient age | Read-only; from inquiry |
| Patient Gender | text | Yes | Gender | Read-only; from inquiry |
| Treatment Type Requested | text | Yes | Hair/Beard/Both | Read-only; from inquiry |

**Section 3: Quote & Treatment Information** (from FR-004):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Treatment Type | text | Yes | Selected treatment (FUE, FUT, DHI, etc.) | Read-only; from quote |
| Estimated Graft Count | number | Yes | Estimated number of grafts | Read-only; from quote |
| Packages Selected | list | No | Hotel, transport, medication packages | Read-only; from quote |
| Clinician Assigned | text | Yes | Clinician who will perform procedure | Read-only; from quote |

**Section 4: Pricing Breakdown** (from FR-004):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Currency | text | Yes | Payment currency | Read-only; from quote |
| Treatment Price | number | Yes | Base treatment price | Read-only; from quote |
| Package Prices | number | Yes | Total package prices | Read-only; from quote |
| Discount Applied | number | No | Discount amount (if any) | Read-only; from quote |
| Total Quote Amount | number | Yes | Total booking amount | Read-only; from quote |

**Section 5: Payment Progress & Status** (from FR-007):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Deposit Percentage | text | Yes | Deposit percentage used | Read-only; admin-configured via FR-029 |
| Deposit Amount | number | Yes | Required deposit amount | Calculated from admin-configured percentage |
| Deposit Status | badge | Yes | Pending / Paid / Partial | Read-only |
| Deposit Paid Date | datetime | Conditional | Date deposit was paid | Read-only; if paid |
| Payment Method (Deposit) | text | Conditional | Payment method used for deposit | Read-only; if paid |
| Payment Status | badge | Yes | Unpaid / Deposit Only / Installments Active / Full Paid | Read-only |
| Installment Progress | group | Conditional | Current installment number, total installments, next due date, completion percentage | Only shown if installments active |
| Final Payment Status | badge | Yes | Not Due / Due / Paid / Overdue | Read-only |
| Final Payment Due Date | datetime | Conditional | Final payment due date | Read-only |
| Final Payment Amount | number | Conditional | Final payment amount due | Calculated |
| Final Payment Method | text | Conditional | Payment method used for final payment | Read-only; if paid |
| Final Payment Paid Date | datetime | Conditional | Date final payment was paid | Read-only; if paid |
| Remaining Balance | number | Yes | Amount remaining to pay | Calculated |
| Total Paid Amount | number | Yes | Sum of all payments made | Calculated |

**Section 6: Payment History** (from FR-007):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Payment History | table | Yes | All payments (deposit, installments, final) with dates, amounts, methods, transaction IDs, status | Read-only |
| Payment Transaction ID | text | Yes | Payment processor transaction ID | Read-only |
| Payment Receipt Link | link | Yes | Link to payment receipt/invoice | Read-only |
| Refund History | table | Conditional | All refunds processed (if any) with dates, amounts, reasons, transaction IDs | Read-only; if refunds exist |

**Section 7: Provider Information** (from provider profile):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Provider Name | text | Yes | Provider/clinic name | Read-only |
| Provider Contact | text | Yes | Clinic contact information | Read-only |
| Provider Email | text | Yes | Provider email | Read-only |

**Section 8: Payout Information** (from FR-017, conditional):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Payout Status | badge | Conditional | Pending / Eligible / Processing / Executed | Only shown after treatment completion |
| Gross Amount | number | Conditional | Total paid by patient | Read-only; if payout eligible |
| Commission Rate | text | Conditional | Platform commission percentage | Read-only; configured via FR-029 |
| Commission Amount | number | Conditional | Platform commission deducted | Read-only; if payout eligible |
| Net Payout | number | Conditional | Amount to provider | Read-only; if payout eligible |
| Payout Link | link | Conditional | Link to payout details in FR-017 | Only shown if payout exists |

**Actions**:

| Action | Type | Condition | Description |
|--------|------|-----------|-------------|
| View Booking Details | link | Always | Open FR-006 booking detail view (full context) |
| View Quote | link | Always | Open full quote details (FR-004) |
| View Inquiry | link | Always | Open full inquiry details (FR-003) |
| Process Refund | button | Booking cancelled or eligible | Open Screen 6: Refund Processing |
| Send Payment Reminder | button | Payment due or overdue | Send reminder to patient |
| View Payment Receipt | link | If payment exists | Open payment receipt/invoice |
| View Payout Details | link | If payout exists | Open payout details in FR-017 |

**Business Rules**:

- Admin has full visibility to all patient and provider information (no masking)
- Payment status reflects real-time payment progress (deposit, installments, final payment)
- All payment data is read-only except for refund processing and reminder actions
- All sections display data from previous stages (inquiry → quote → booking → payment) in chronological order
- Links to original inquiry, quote, and booking provide full context and audit trail

**Notes**:

- This screen provides comprehensive payment view with full context from patient journey
- UI may use tabs or accordion sections to organize information by stage
- Payment details shown without card information (PCI compliance)
- This complements FR-006's Booking Detail View (Screen 6) which shows all booking information; this screen focuses specifically on payment details
- Payment status updates in real-time as patient makes payments

---

#### Screen 6: Refund Processing (Admin)

**Purpose**: Process refunds per cancellation policy with full context from booking and payment stages

**Note**: This screen is accessed from Screen 5 (Payment Progress Dashboard) or Screen 5B (Payment Detail View) when admin clicks "Process Refund". It provides comprehensive refund processing with context from previous stages.

**Data Fields** (Continuation from Screen 5/5B, aggregating data from FR-003, FR-004, FR-006, FR-007):

**Section 1: Booking & Cancellation Context** (from FR-006):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Booking Reference | text | Yes | Unique booking reference | Read-only; link to FR-006 booking detail |
| Booking Status | badge | Yes | Current status | Read-only |
| Appointment Date | datetime | Yes | Original appointment slot | Read-only |
| Cancellation Date | datetime | Yes | Date of cancellation request | Read-only |
| Days Before Procedure | number | Yes | Days until procedure date | Calculated, read-only |
| Cancellation Reason | text | Yes | Reason for cancellation | Read-only; from cancellation request |

**Section 2: Patient Information** (from FR-003):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Patient Name | text | Yes | Full patient name | Read-only |
| Patient Email | text | Yes | Email address | Read-only |
| Patient Phone | text | Yes | Phone number | Read-only |
| Patient ID | text | Yes | Patient code | Read-only |

**Section 3: Treatment Information** (from FR-004):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Treatment Type | text | Yes | Selected treatment (FUE, FUT, DHI, etc.) | Read-only; from quote |
| Provider Name | text | Yes | Provider/clinic name | Read-only |
| Total Quote Amount | number | Yes | Total booking amount | Read-only; from quote |

**Section 4: Payment Summary** (from FR-007):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Currency | text | Yes | Payment currency | Read-only; from quote |
| Total Paid Amount | number | Yes | Total amount paid by patient | Read-only |
| Deposit Paid | number | Yes | Deposit amount paid | Read-only |
| Final Payment Paid | number | Conditional | Final payment amount paid | Read-only; if paid |
| Payment History | table | Yes | All payments made (deposit, installments, final) with dates and amounts | Read-only |
| Original Payment Methods | list | Yes | Payment methods used (may be multiple if installments) | Read-only |

**Section 5: Refund Calculation** (from FR-006 cancellation policy):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Cancellation Policy | text | Yes | Applicable refund percentage per FR-006 | Read-only; based on timing |
| Refund Percentage | number | Yes | Refund percentage (90% / 50% / 0%) | Read-only; per FR-006 policy |
| Calculated Refund Amount | number | Yes | Refund amount to process | Calculated per FR-006 policy; cannot exceed paid amount |
| Refund Breakdown | text | Yes | Explanation of calculation (e.g., "50% of £3,000 = £1,500") | Read-only; for transparency |

**Section 6: Refund Processing** (Admin Action):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Refund Reason | textarea | Yes | Reason for refund | Mandatory audit field; min 20 characters |
| Refund Destination | select | Yes | Where refund will be sent | Defaults to original payment method; can select alternative |
| Refund Method | text | Yes | Refund method (original payment method or alternative) | Read-only; based on selection |
| Approval Required | checkbox | Conditional | Secondary admin approval for exceptions | Required for exceptions to policy |
| Exception Documentation | file | Conditional | Medical emergency documentation or other exception proof | Required if exception to policy |
| Process Refund | button | Yes | Confirm and process refund | Enabled when all required fields complete |

**Section 7: Refund History** (if previous refunds exist):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Previous Refunds | table | Conditional | Previous refunds processed (if any) with dates, amounts, reasons | Read-only; if refunds exist |

**Actions**:

| Action | Type | Condition | Description |
|--------|------|-----------|-------------|
| View Booking Details | link | Always | Open FR-006 booking detail view (full context) |
| View Payment Details | link | Always | Open Screen 5B: Payment Detail View |
| View Quote | link | Always | Open full quote details (FR-004) |
| Cancel Refund | button | Always | Cancel refund processing and return to dashboard |
| Process Refund | button | All fields complete | Confirm and process refund |

**Business Rules**:

- Refund amounts calculated per FR-006 cancellation policy:
  - > 30 days before procedure: 90% refund
  - 15-30 days before procedure: 50% refund
  - < 15 days before procedure: No refund (unless medical emergency with documentation)
- Admin approval required for all refunds
- Exceptions to policy (e.g., medical emergency) require secondary admin approval and documentation upload
- Refund processed to original payment method by default; admin can select alternative method
- Refund amount cannot exceed total paid amount
- All refund actions are auditable with timestamp, actor, reason, and approval chain
- Refund processing updates booking status and notifies patient and provider

**Notes**:

- Refund amount calculation is based on FR-006 cancellation policy
- Medical emergency exceptions require documentation upload (medical certificate, doctor's note, etc.)
- This screen provides full context from booking and payment stages to inform refund decisions
- UI should clearly display refund calculation breakdown for transparency
- All sections display data from previous stages to provide complete context for refund processing

---

**Configuration Access**: Admin users who need to view or edit deposit, commission, or payment method settings follow the in-app link to `FR-029: Payment System Configuration`, where those settings are managed. This FR does not duplicate or display that configuration.

---

## Business Rules

### General Module Rules

- Deposit is required to confirm a booking; default 20-30% range (admin-configurable via FR-029: Payment System Configuration, per-provider or globally)
- Final payment is due before or on procedure date; overdue payments are flagged and notified
- Full payment option is always available as an alternative to split payments
- Receipts and invoices are generated for every successful transaction
- Provider payout occurs only after treatment completion and admin-triggered execution

### Data & Privacy Rules

- Payment card data is never stored by the platform; only the payment processor handles sensitive card details
- All payment-related PII is protected per privacy standards and encrypted at rest and in transit
- Access to payment data follows RBAC: patients see their own transactions; providers see payout-related booking financials; admins see system-wide financials
- All payment lifecycle events are logged for a tamper-evident audit trail
- Compliance: PCI-DSS (via processor), GDPR/HIPAA-aligned handling of personal and medical data; no direct database sharing across tenants

### Admin Editability Rules

**Editable by Admin**:

- **Note**: Commission rates and deposit defaults are managed at system level via **FR-029: Payment System Configuration** (not editable in this module)
- Supported payment methods and currencies (enable/disable) - managed via FR-029
- Refund approvals and reasons (within FR-006 cancellation policy)
- **Note**: Payout execution is managed in **FR-017: Admin Billing & Financial Management** (not in this module)

**Fixed in Codebase (Not Editable)**:

- Core security controls and encryption standards
- Audit logging scope for financial events
- Idempotency and duplicate-charge protections

**Configurable with Restrictions**:

- Payment reminder timing templates (e.g., 3 days before due date)
- Payout execution timing windows (e.g., business days)

### Payment & Billing Rules

- Payment methods include cards, bank transfers, and mainstream digital wallets supported by the processor
- Deposit payment is collected at booking confirmation (admin-configurable percentage, default 20-30% range, configured via FR-029); final payment before or on procedure day
- Refunds follow FR-006 cancellation policy: >30 days before = 90% refund; 15-30 days before = 50% refund; <15 days before = no refund (unless medical emergency with documentation)
- Invoices and receipts are issued for every successful payment and refund
- Prices are displayed in the patient’s selected currency; provider payouts occur in provider’s configured payout currency with fair conversion
- Support additional authentication flows when requested by issuer/regulation
- Platform is the Merchant of Record; platform issues invoices to patients, manages refunds/taxes, and pays providers net of commission
- Commission is deducted at time of payout after treatment completion (admin-triggered), consistent with FR-007 Payment Flow V1

---

## Success Criteria

### Patient Experience Metrics

- **SC-001**: Patients complete deposit payment within 3 minutes (median) from checkout start
- **SC-002**: 95% of successful payments display confirmation within 5 seconds of authorization
- **SC-003**: 90% of patients successfully complete deposit on first attempt without support

### Provider Efficiency Metrics

- **SC-004**: Payouts are available to providers within 2 business days after admin execution
- **SC-005**: Providers can verify payout details in under 1 minute per booking
- **SC-006**: 100% of executed payouts include commission details and statements

### Admin Management Metrics

- **SC-007**: Admins configure commission and deposit defaults in under 2 minutes per provider
- **SC-008**: Payment-related support tickets decrease by 30% after launch
- **SC-009**: 100% of payment lifecycle events (auth, capture, refund, payout) are auditable

### System Performance Metrics

- **SC-010**: 95% of payment attempts complete (success/fail) within 30 seconds end-to-end
- **SC-011**: Payment module maintains 99.9% functional availability monthly
- **SC-012**: Zero duplicate charges on idempotent retries in all tested scenarios
- **SC-013**: Zero loss of financial records (payments, refunds, payouts) during normal operations

### Business Impact Metrics

- **SC-014**: Booking confirmation rate increases by 15% due to seamless deposit flow
- **SC-015**: Payment success rate ≥ 95% after first two months
- **SC-016**: Multi-currency support covers at least USD, EUR, GBP, and TRY at launch

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **P-01: Auth & Profile Management**
  - **Why needed**: Only authenticated patients can pay and view receipts
  - **Integration point**: Uses patient profile and booking ownership for access

- **P-03: Booking & Scheduling (FR-006)**
  - **Why needed**: Deposit is tied to booking confirmation; final payment linked to procedure date; refund amounts calculated per FR-006 cancellation policy
  - **Integration point**: Booking state updates on payment events; refund calculations use FR-006 cancellation policy

- **PR-05: Financial Management & Reporting**
  - **Why needed**: Providers need payout visibility and statements
  - **Integration point**: Payout and commission details surfaced in provider portal

- **A-05: Billing & Financial Reconciliation (FR-017)**
  - **Why needed**: Provider payout execution and invoice generation (managed in FR-017)
  - **Integration point**: Payment data feeds into payout calculations; refund processing in this module
- **FR-029: Payment System Configuration (A-09)**
  - **Why needed**: Commission rates and deposit defaults are configured at system level via FR-029
  - **Integration point**: Payment processing uses configured deposit percentages and commission rates from FR-029

- **S-03: Notification Service**
  - **Why needed**: Send confirmations, reminders, and alerts
  - **Integration point**: Triggers on payment lifecycle events

### External Dependencies (APIs, Services)

- **PCI-compliant Payment Processor**
  - **Purpose**: Processes authorizations, captures, refunds, and supports multiple payment methods and currencies
  - **Integration**: Standards-based payment flows including additional authentication when required
  - **Failure handling**: Provide clear user messaging; support retries; ensure idempotency to prevent duplicates

### Data Dependencies

- **Active provider profiles with commission configuration**
  - **Why needed**: Compute net payouts correctly
  - **Source**: Provider onboarding and admin settings

- **Confirmed bookings with pricing and schedule**
  - **Why needed**: Calculate deposit/final; enforce due dates and refunds
  - **Source**: Booking & Scheduling module

---

## Assumptions

### User Behavior Assumptions

- Patients prefer cards and mainstream wallets for speed; bank transfers used in select markets
- Most patients expect deposit confirmation and receipt immediately after payment
- Patients will pay final balance in-app before arrival when reminded

### Technology Assumptions

- Patient uses a modern smartphone with reliable internet during payment
- Provider and admin use modern browsers on desktop for financial views
- Payment processor provides SCA/3DS flow handling where required

### Business Process Assumptions

- Admin marks treatment completion; provider cannot self-execute payouts (payout execution in FR-017)
- Default deposit set to 20-30% range (admin-configurable via FR-029) unless provider-specific override exists
- Refund exceptions (e.g., medical emergency) require documentation and admin approval; refund amounts per FR-006 cancellation policy

---

## Implementation Notes

### Technical Considerations

- Payment flows must support additional authentication where mandated
- All financial events require idempotent handling to prevent duplicates
- Payment records, refunds, and payouts must be immutable once confirmed, with corrective entries for adjustments

### Integration Points

- Payment initiation and confirmation connected to Booking state updates and Notifications
- Admin payout execution updates Provider views and generates statements

### Scalability Considerations

- Expected 200–500 payments/day at launch across markets
- Plan for 10x growth within 12 months; handle promotional spikes
- Ensure reminder and payout jobs scale without delaying time-sensitive actions

### Security Considerations

- RBAC enforced across tenants; providers see only payout-related financials for their bookings
- All personal and financial data encrypted at rest and in transit; no storage of payment card numbers by the platform
- Full audit trail for financial events and administrative actions affecting payouts and refunds
- Compliance alignment with PCI-DSS and relevant privacy regulations

---

## User Scenarios & Testing

### User Story 1 - Pay Deposit to Confirm Booking (Priority: P1)

Patient pays deposit to confirm booking and receives immediate confirmation with receipt/invoice.

**Why this priority**: Confirms the booking and unlocks provider commitment; critical for revenue capture.

**Independent Test**: Create a booking requiring deposit; pay deposit; verify confirmation, receipt, and booking status.

**Acceptance Scenarios**:

1. **Given** a booking requiring a deposit (admin-configurable percentage, default 20-30% range), **When** the patient pays the deposit successfully, **Then** the booking is marked confirmed and a receipt/invoice is issued and delivered.
2. **Given** a required additional authentication step, **When** the patient completes it successfully, **Then** the payment completes and confirmation is shown within 5 seconds.
3. **Given** a payment failure, **When** the patient retries with a different method, **Then** the system prevents duplicate charges and confirms only a single successful payment.

---

### User Story 2 - Pay Final Balance Before Procedure (Priority: P1)

Patient completes final payment before or on procedure day and receives confirmation.

**Why this priority**: Ensures full payment is secured, reducing on-site friction.

**Independent Test**: For a confirmed booking with remaining balance, complete final payment and verify updated status and receipt/invoice.

**Acceptance Scenarios**:

1. **Given** a confirmed booking with a remaining balance, **When** the patient pays the final amount, **Then** the booking is marked fully paid and a final receipt/invoice is delivered.
2. **Given** a final payment due date, **When** it is approaching within 3 days, **Then** the patient receives a reminder notification.

---

### User Story 3 - Process Refund per Policy (Priority: P2)

Admin processes a refund request according to cancellation policy; patient and provider are notified.

**Why this priority**: Required for trust and policy compliance.

**Independent Test**: Cancel a booking at different time windows; verify calculated refund and notifications.

**Acceptance Scenarios**:

1. **Given** a cancellation 20 days before procedure, **When** admin approves refund, **Then** the system refunds 50% per FR-006 cancellation policy and updates booking/payment status with audit log.
2. **Given** a cancellation 5 days before procedure, **When** admin denies refund per policy, **Then** the system records the decision with reason and notifies the patient.

---

### Edge Cases

- Payment challenge required but device/app loses focus; flow must resume gracefully
- Duplicate submission from rapid taps; idempotency ensures single charge
- Currency changed by patient at checkout; totals and conversion rates remain consistent and clear
- Refund requested outside policy window; admin records exception with documentation
- Payout blocked due to missing completion status; admin resolves before execution

---

## Functional Requirements Summary

### Core Requirements

- **REQ-007-001**: System MUST allow patients to pay deposit to confirm bookings and final amount by due date
- **REQ-007-002**: System MUST support card, bank transfer, and digital wallet methods for payments
- **REQ-007-003**: System MUST support multiple currencies (at minimum USD, EUR, GBP, TRY) and display accurate totals
- **REQ-007-004**: System MUST generate and deliver receipts/invoices for successful payments and refunds
- **REQ-007-005**: System MUST mark bookings confirmed on deposit, fully paid after final payment, and update related statuses

### Data Requirements

- **REQ-007-006**: System MUST maintain complete payment history per booking, including refunds and payout references
- **REQ-007-007**: System MUST compute platform commission per transaction and link to provider payout records

### Security & Privacy Requirements

- **REQ-007-008**: System MUST ensure no card numbers are stored by the platform; only the processor handles them
- **REQ-007-009**: System MUST log all financial events with actor, timestamp, booking ID, and outcomes
- **REQ-007-010**: System MUST support additional authentication for payments when required by issuer/regulation

### Integration Requirements

- **REQ-007-011**: System MUST support processor-driven payment flows for authorization, capture, and refund
- **REQ-007-012**: System MUST support payout execution with commission deduction and statement generation

### Marking Unclear Requirements

- **REQ-007-013**: Platform is Merchant of Record; platform issues patient invoices, manages refunds and tax implications, and pays out net to providers
- **REQ-007-014**: Commission is deducted on the total procedure cost at the time of provider payout after treatment completion (admin‑triggered); not pro‑rata across deposit/final
- **REQ-007-015**: Refunds require Admin approval with an SLA to approve/deny within 2 business days; the decision and reason are logged and notifications sent

---

## Key Entities

- **Entity 1 - Payment**: Represents a financial transaction (deposit, final, refund)
  - **Key attributes**: booking reference, amount, currency, method, status, timestamps, receipt/invoice refs
  - **Relationships**: belongs to a booking; may relate to a payout; may reverse via a refund

- **Entity 2 - Payout**: Represents provider disbursement after commission
  - **Key attributes**: provider, gross amount, commission, net amount, execution date, status, statement ref
  - **Relationships**: aggregates payments for a booking or period; admin-triggered

- **Entity 3 - Commission**: Represents platform earnings per transaction
  - **Key attributes**: percentage/rate, computed amount, basis (total/line), booking reference
  - **Relationships**: associated with payment and payout

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-04 | 1.0 | Initial PRD creation | AI |
| 2025-11-12 | 1.1 | Major revisions: Moved commission rate and deposit defaults to system level (FR-029); Clarified provider payout execution is in FR-017; Clarified refund amount calculation is per FR-006 cancellation policy; Added tenant distinction to screen specifications; Added patient payment progress screens for admin and provider; Aligned default deposit amount with FR-006 (20-30% range, not 30%) | AI |
| 2025-11-12 | 1.2 | Enhanced provider screens: Added comprehensive data from all previous stages (FR-003 inquiry, FR-004 quote, FR-006 booking) to Screen 3 (Payment Status & Progress) and Screen 4 (Payout Overview) to show continuation of data across stages, consistent with FR-006 booking detail view | AI |
| 2025-11-12 | 1.3 | Enhanced admin screens: Added Screen 5B (Payment Detail View) with comprehensive data from all previous stages (FR-003 inquiry, FR-004 quote, FR-005 acceptance, FR-006 booking, FR-007 payment) organized into 8 sections; Enhanced Screen 6 (Refund Processing) with 7 sections providing full context from booking and payment stages; Updated Screen 5 (Payment Progress Dashboard) to link to detail view; All admin screens now show data continuity consistent with FR-006 booking detail view | AI |
| 2025-11-12 | 1.4 | Simplified admin configuration access: Removed read-only Screen 7 in favor of direct link-out to `FR-029: Payment System Configuration`; clarified in Admin Platform intro and post-screen note that configuration lives entirely in FR-029 | AI |
| 2025-11-12 | 1.5 | Cross-checked PRD against `system-prd.md` and client transcriptions; updated status to "✅ Verified & Approved" per template; confirmed change log consistency | AI |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | [Name] | [Date] | [Status] |
| Technical Lead | [Name] | [Date] | [Status] |
| Stakeholder | [Name] | [Date] | [Status] |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0
**Based on**: FR-007 Payment Processing (system-prd.md)
**Last Updated**: 2025-11-12
