# Product Requirements Document: Payment Processing (FR-007)

**Module**: P-03: Booking & Payment | PR-05: Financial Management & Reporting | A-05: Billing & Financial Reconciliation | S-02: Payment Processing Service | S-03: Notification Service
**Feature Branch**: `fr007-payment-processing`
**Created**: 2025-11-04
**Status**: Draft
**Source**: FR-007 from local-docs/project-requirements/system-prd.md (Payment Processing) + Constitution (.specify/memory/constitution.md)

---

## Executive Summary

Enable patients to pay securely for procedures (deposit at booking and final payment before or on procedure day) in supported currencies and methods, while ensuring compliant handling of payments, automated receipt/invoice generation, platform commission calculation, and timely provider payouts after treatment completion. This module focuses on the what/why of payments across tenants: a clear, trustworthy checkout for patients, transparent payout tracking for providers, and configurable oversight for admins. It excludes implementation details and adheres to the Hairline Constitution (multi-tenant separation, privacy, auditability, and compliance).

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-03)**: Patient pays deposit to confirm booking; pays final amount by procedure date; views payment status, receipts, and invoices; selects supported payment method and currency; receives payment confirmations and reminders.
- **Provider Platform (PR-05)**: Provider views booking payment status and scheduled payouts; sees commission deducted amounts; accesses payout statements and history once treatment is marked complete.
- **Admin Platform (A-05)**: Admin configures commission rates and deposit defaults; approves/executes provider payouts post-treatment; processes refunds per policy; monitors payment dashboards, reconciliation, and reports.
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
- View upcoming and completed payouts with commission deducted
- Access payout statements for accounting

**Admin Platform (A-05)**:

- Configure commission rate per provider or tier (within policy bounds)
- Configure deposit percentage defaults and allowed range
- Review and trigger provider payouts after treatment completion
- Approve and process refunds per cancellation policy
- View reconciliation dashboards and export payment/commission reports

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
- SMS channel specifics (handled by S-03 configuration)
- Any non-payment content (marketing, aftercare content)

### Entry Points

- Patient initiates payment in booking confirmation flow (deposit required)
- Patient initiates final payment from booking details prior to procedure date
- Admin initiates provider payout after treatment is marked completed

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
8. After treatment completion, Admin reviews the booking and triggers provider payout; System calculates commission and prepares payout statement; provider is notified

### Alternative Flows

**A1: Full Payment at Booking**:

- **Trigger**: Patient prefers to pay the full amount at booking instead of split payments
- **Steps**:
  1. Patient selects full payment option
  2. System processes full amount and marks booking fully paid
  3. System issues receipt/invoice and sends confirmations
- **Outcome**: Booking is confirmed and fully paid; payout remains pending until treatment completion

**A2: Refund Due to Cancellation**:

- **Trigger**: Patient cancels booking; cancellation policy determines refund amount
- **Steps**:
  1. Admin reviews cancellation timing and applicable refund schedule
  2. System calculates refundable amount and initiates refund
  3. System updates booking/payment status and sends confirmation notices
- **Outcome**: Refund processed according to policy; provider payout eligibility updated

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

### Screen 1: Patient Checkout (Deposit)

**Purpose**: Allow patient to pay deposit to confirm booking

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Total Amount | number | Yes | Total procedure price | Positive amount; matches booking |
| Deposit Amount | number | Yes | Deposit to confirm booking | Percent of total; within allowed range |
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

### Screen 2: Patient Final Payment

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

### Screen 3: Provider Payout Overview

**Purpose**: Allow provider to view payout status and details for completed treatments

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Booking ID | text | Yes | Reference identifier | Must match existing booking |
| Patient Alias | text | Yes | Anonymized patient reference | No PII until confirmed |
| Gross Amount | number | Yes | Total paid by patient | Positive |
| Commission | number | Yes | Platform commission deducted | Within configured range |
| Net Payout | number | Yes | Amount to provider | Gross minus commission |
| Payout Status | select | Yes | Pending/Executed/On Hold | Valid transitions only |

**Business Rules**:

- Payout visible only after treatment marked complete by admin
- Commission shown and deducted from payout amount
- History of payouts accessible for accounting

**Notes**:

- This is a read-only view for providers; payout execution is admin-controlled

---

### Screen 4: Admin Payout & Refund Management

**Purpose**: Allow admin to execute payouts and process refunds per policy

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Treatment Completion Flag | checkbox | Yes | Eligibility for payout | Requires completed status |
| Commission Rate | number | Yes | Provider commission configuration | Within allowed bounds |
| Refund Amount | number | Conditional | Calculated per policy | Cannot exceed paid amount |
| Refund Reason | text | Yes | Reason for refund | Mandatory audit field |
| Payout Execution | action | Yes | Trigger payout | Allowed only when eligible |

**Business Rules**:

- Refunds follow cancellation schedule; admin approval required
- Payout execution creates immutable payout record and statement
- All actions are auditable with timestamp, actor, and reason

---

## Business Rules

### General Module Rules

- Deposit is required to confirm a booking; default 30% (admin-configurable within allowed range)
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

- Provider commission rate (within 15–25% bounds per policy)
- Deposit percentage default (e.g., 20–30%) and allowable range per provider
- Supported payment methods and currencies (enable/disable)
- Refund approvals and reasons (within policy)
- Payout execution after verifying treatment completion

**Fixed in Codebase (Not Editable)**:

- Core security controls and encryption standards
- Audit logging scope for financial events
- Idempotency and duplicate-charge protections

**Configurable with Restrictions**:

- Payment reminder timing templates (e.g., 3 days before due date)
- Payout execution timing windows (e.g., business days)

### Payment & Billing Rules

- Payment methods include cards, bank transfers, and mainstream digital wallets supported by the processor
- Deposit payment is collected at booking confirmation; final payment before or on procedure day
- Refunds follow cancellation schedule (example: >30d 90%; 15–30d 50%; <15d no refund unless exception)
- Invoices and receipts are issued for every successful payment and refund
- Prices are displayed in the patient’s selected currency; provider payouts occur in provider’s configured payout currency with fair conversion
- Support additional authentication flows when requested by issuer/regulation
- Platform is the Merchant of Record; platform issues invoices to patients, handles refunds/taxes, and pays providers net of commission
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
  - **Why needed**: Deposit is tied to booking confirmation; final payment linked to procedure date
  - **Integration point**: Booking state updates on payment events

- **PR-05: Financial Management & Reporting**
  - **Why needed**: Providers need payout visibility and statements
  - **Integration point**: Payout and commission details surfaced in provider portal

- **A-05: Billing & Financial Reconciliation**
  - **Why needed**: Admin config and payout execution responsibilities
  - **Integration point**: Commission settings, payout approvals, refund processing

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

- Admin marks treatment completion; provider cannot self-execute payouts
- Default deposit set to 30% unless provider-specific override exists
- Refund exceptions (e.g., medical emergency) require documentation and admin approval

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

1. **Given** a booking requiring a 30% deposit, **When** the patient pays the deposit successfully, **Then** the booking is marked confirmed and a receipt/invoice is issued and delivered.
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

1. **Given** a cancellation 20 days before procedure, **When** admin approves refund, **Then** the system refunds 50% and updates booking/payment status with audit log.
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

- **FR-001**: System MUST allow patients to pay deposit to confirm bookings and final amount by due date
- **FR-002**: System MUST support card, bank transfer, and digital wallet methods for payments
- **FR-003**: System MUST support multiple currencies (at minimum USD, EUR, GBP, TRY) and display accurate totals
- **FR-004**: System MUST generate and deliver receipts/invoices for successful payments and refunds
- **FR-005**: System MUST mark bookings confirmed on deposit, fully paid after final payment, and update related statuses

### Data Requirements

- **FR-006**: System MUST maintain complete payment history per booking, including refunds and payout references
- **FR-007**: System MUST compute platform commission per transaction and link to provider payout records

### Security & Privacy Requirements

- **FR-008**: System MUST ensure no card numbers are stored by the platform; only the processor handles them
- **FR-009**: System MUST log all financial events with actor, timestamp, booking ID, and outcomes
- **FR-010**: System MUST support additional authentication for payments when required by issuer/regulation

### Integration Requirements

- **FR-011**: System MUST support processor-driven payment flows for authorization, capture, and refund
- **FR-012**: System MUST support payout execution with commission deduction and statement generation

### Marking Unclear Requirements

- **FR-013**: Platform is Merchant of Record; platform issues patient invoices, manages refunds and tax implications, and pays out net to providers
- **FR-014**: Commission is deducted on the total procedure cost at the time of provider payout after treatment completion (admin‑triggered); not pro‑rata across deposit/final
- **FR-015**: Refunds require Admin approval with an SLA to approve/deny within 2 business days; the decision and reason are logged and notifications sent

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
| [DATE] | 1.1 | [Description of changes] | [Name] |

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
**Last Updated**: 2025-11-04
