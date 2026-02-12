# FR-007B - Split Payment / Installment Plans

**Module**: P-03: Booking & Payment | S-02: Payment Processing Service
**Feature Branch**: `fr007b-payment-installments`
**Created**: 2025-11-10
**Status**: Draft
**Source**: FR-007B from local-docs/project-requirements/system-prd.md (Split Payment / Installment Plans) + Constitution (.specify/memory/constitution.md)

---

## Executive Summary

Enable patients to pay for hair transplant procedures through interest-free installment plans spanning 2-9 months, providing financial flexibility while ensuring full payment completion 30 days before the scheduled procedure date. The installment system automatically calculates available payment plans based on the time remaining until the procedure, handles scheduled automatic charges, manages payment failures with retry logic, and notifies both patients and admins of payment status. This feature focuses on what patients need (flexible payment options with clear terms) and why (making procedures more accessible while protecting provider and platform revenue), without prescribing how the technical implementation should work.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-03)**: Patient selects installment plan at checkout; views installment schedule and payment history; receives reminders before each installment; sees available installment options based on procedure date
- **Provider Platform (PR-05)**: Provider views booking payment status (installment plan active, payments on track, overdue installments)
- **Admin Platform (A-05)**: Admin monitors and manages installment plans across bookings; handles defaulted installment plans and refunds. Customer-facing installment configuration (enabled installment counts, cutoff days, minimum booking amount, grace period) is managed in **FR-029 (A-09)**.
- **Shared Services (S-02/S-03)**: Payment Processing Service executes scheduled installment charges and retry logic; Notification Service sends installment reminders and payment confirmations

### Multi-Tenant Breakdown

**Patient Platform (P-03)**:

- Select installment plan from available options at booking checkout
- View maximum installments available based on time until procedure
- See clear breakdown of installment amounts and payment schedule
- Receive reminders 3 days before each scheduled installment
- View installment payment history and upcoming payments
- Update payment method for installments if needed
- Receive notifications of successful/failed installment payments

**Provider Platform (PR-05)**:

- View booking payment status: installment plan active, number of installments, completion percentage
- See payment progress: which installments have been paid, which are upcoming
- Receive alerts for overdue installments that may affect booking
- Access payment history for installment-based bookings

**Admin Platform (A-05)**:

- View installment plan configuration (managed in FR-029) and link to configuration screen for authorized users
- Monitor all active installment plans across the platform
- View installment payment success/failure rates
- Handle defaulted installment plans (failed payments after retries)
- Process refunds for canceled bookings with partial installment payments
- Generate reports on installment plan usage and performance
- View aging reports for overdue installments

**Shared Services (S-02, S-03)**:

- S-02: Processes scheduled installment charges on due dates; executes retry logic for failed payments (3 attempts); calculates available installments based on procedure date
- S-03: Sends reminders 3 days before installment due; sends payment confirmations and failure notifications; alerts admins of payment issues

### Communication Structure

**In Scope**:

- Email/push notifications for installment payment reminders (3 days before due date)
- Payment confirmation notifications for successful installment charges
- Payment failure notifications for declined/failed installments
- Admin alerts for defaulted installment plans
- Booking status change notifications when final installment completes

**Out of Scope**:

- SMS notifications (handled by S-03 channel configuration; **no SMS installment notifications are available in MVP and this channel is a future enhancement**)
- Chat/messaging between patient and provider about payment terms
- Marketing content about installment plans

### Entry Points

- Patient has accepted a quote (FR-005) and reaches the **Payment Options** step in the booking & payment flow (FR-006/FR-007), then selects **"Pay in Installments"**, which hands off to FR-007B Screen 1
- Patient views installment schedule from booking details screen
- Admin accesses installment management from billing/financial management module
- Provider views installment status from booking overview screen

---

## Business Workflows

### Main Flow: Patient Selects Installment Plan and Completes Payments

**Actors**: Patient, System (Payment Processing Service), Admin
**Upstream Context**: Quote has been accepted (FR-005) and booking details (procedure date, total cost) are available via FR-006; FR-007 has presented a **Payment Options** step where the patient chose **"Pay in Installments"** instead of **"Pay in Full"**.
**Trigger**: Patient confirms the choice to **"Pay in Installments"** on the Payment Options step and proceeds to the Installment Plan selection screen (Screen 1 in this FR)
**Outcome**: Booking confirmed with installment plan; scheduled installments charged automatically; booking fully paid by the configured cutoff date (minimum 30 days before procedure, configured via FR-029)

**Steps**:

1. Patient reviews booking summary with total procedure cost and sees that **"Pay in Installments"** is selected as the payment option
2. System calculates feasible installment options based on time until procedure date and the configured cutoff days (minimum 30 days before procedure, configured via FR-029) with monthly installments
3. System displays installment options (e.g., "Pay in 2-5 installments" if procedure is in 6 months)
4. Patient selects desired installment plan (e.g., 4 monthly installments)
5. System calculates installment amount (total ÷ number of installments) and displays payment schedule with dates
6. Patient confirms installment plan selection and provides payment method
7. System processes first installment immediately to confirm booking
8. System schedules remaining installments on monthly intervals
9. System marks booking as "Confirmed - Installment Plan Active"
10. Three days before each scheduled installment, System sends reminder to patient
11. On due date, System automatically charges payment method
12. On successful charge, System updates installment status and sends confirmation
13. System repeats steps 10-12 for each remaining installment
14. When final installment completes by the cutoff date, System marks booking as "Fully Paid"

### Alternative Flows

**A1: Patient Chooses Fewer Installments Than Maximum Available**:

- **Trigger**: Patient wants to pay faster than the maximum allowed installments
- **Steps**:
  1. Patient selects fewer installments (e.g., 3 installments when 6 are available)
  2. System calculates higher installment amount with same total
  3. System adjusts payment schedule accordingly
- **Outcome**: Booking completed with shorter payment timeline; same 30-day buffer maintained
- **Outcome**: Booking completed with shorter payment timeline; same cutoff window maintained

**A2: Patient Opts for Full Payment Instead of Installments (Handled by FR-007)**:

- **Trigger**: On the Payment Options step (FR-007), patient selects **"Pay in Full"** instead of **"Pay in Installments"**
- **Steps** (owned by FR-007, summarized here for branching clarity):
  1. System routes patient to the standard full-payment checkout flow defined in FR-007
  2. System processes full payment immediately
  3. System marks booking as "Fully Paid"
- **Outcome**: Booking confirmed without installment plan; **FR-007B is not invoked** in this path

**A3: Patient Updates Payment Method Mid-Plan**:

- **Trigger**: Patient's payment method expired or needs to change card
- **Steps**:
  1. Patient navigates to booking details and selects "Update Payment Method"
  2. Patient provides new payment method details
  3. System validates and saves new payment method
  4. System applies new payment method to remaining installments
- **Outcome**: Future installments charged to new payment method; previous installments unaffected

**B1: Installment Payment Fails**:

- **Trigger**: Scheduled installment charge is declined or fails
- **Steps**:
  1. System detects payment failure and logs the failure reason
  2. System immediately notifies patient of failed payment with clear error message
  3. System schedules first retry attempt for next day
  4. If retry fails, System waits 3 days and attempts second retry
  5. If second retry fails, System waits 7 days and attempts third retry
  6. If all 3 retries fail, System flags installment plan as "Defaulted"
  7. System notifies admin of defaulted plan and overdue booking
  8. Admin reviews and contacts patient to resolve payment issue
- **Outcome**: Payment resolved manually or booking canceled per admin decision; patient may be charged late fees or rescheduling fees

**B2: Patient Cancels Booking With Active Installment Plan**:

- **Trigger**: Patient requests booking cancellation before completing all installments
- **Steps**:
  1. Patient requests cancellation through app or admin support
  2. System calculates paid installments to date and applicable refund per cancellation policy
  3. Admin reviews cancellation request and calculates refund amount
  4. System processes refund based on cancellation timing (e.g., >30 days = 90% refund of paid amount)
  5. System cancels remaining scheduled installments
  6. System updates booking status to "Canceled - Partial Refund"
- **Outcome**: Patient refunded per policy; no further installments charged; provider notified

**B3: Procedure Date Changes After Installment Plan Established**:

- **Trigger**: Admin manually reschedules a confirmed booking due to emergency or exceptional circumstances (per FR-016 Admin Patient Management; patient self-service rescheduling remains deferred to V2 per FR-006 and system PRD)
- **Steps**:
  1. Rescheduling request triggers installment plan recalculation
  2. System checks if new procedure date allows completion of remaining installments (30-day buffer)
  3. **If sufficient time**: System adjusts installment schedule dates to align with new procedure date
  4. **If insufficient time**: System notifies patient that remaining balance must be paid immediately or installment plan canceled
  5. Admin, in coordination with patient, either collects remaining balance immediately or cancels booking per cancellation policy
- **Outcome**: Installment plan adjusted to new schedule or remaining balance paid immediately; booking date updated

---

## Screen Specifications

### Patient Platform Screens

#### Screen 1: Patient Checkout - Installment Plan Selection

**Purpose**: Allow patient to select installment plan option at booking checkout

**Data Fields**:

| Field Name           | Type   | Required | Description                        | Validation Rules                                      |
|---------------------|--------|----------|------------------------------------|-------------------------------------------------------|
| Total Amount         | number | Yes      | Total procedure cost               | Positive amount; matches accepted quote               |
| Time Until Procedure | date   | Yes      | Days remaining until procedure     | At least 60 days (for minimum 2 installments + buffer)|
| Maximum Installments | number | Yes      | Calculated max installments available | 2-9; based on (days until procedure - 30) ÷ 30     |
| Selected Installments| select | Yes      | Patient's chosen number of installments | Must be ≤ maximum available                      |
| Installment Amount   | number | Yes      | Amount per installment             | Total ÷ selected installments                         |
| Payment Schedule     | table  | Yes      | Dates and amounts for each installment | First installment is today; subsequent monthly     |
| Payment Method       | form   | Yes      | Card details for recurring charges | Valid payment method required                         |

**Business Rules**:

- Display clear explanation: "Final payment must complete 30 days before your procedure"
- Show maximum installments prominently with calculation explanation
- Allow patient to select any number from 2 to maximum available
- First installment charged immediately upon confirmation
- Display full payment schedule with dates before patient confirms
- Show comparison: installment plan vs. full payment
- Disable installment option if procedure is less than 60 days away

**Notes**:

- Use visual payment timeline showing each installment date
- Highlight that installments are interest-free
- Show clear "Pay in Full" alternative option
- Provide calculator tool to experiment with different installment counts

---

#### Screen 2: Patient Booking Details - Installment Schedule View

**Purpose**: Allow patient to view installment payment schedule and history

**Data Fields**:

| Field Name            | Type   | Required | Description                           | Validation Rules                            |
|----------------------|--------|----------|---------------------------------------|---------------------------------------------|
| Total Amount          | number | Yes      | Total procedure cost                  | Matches booking total                       |
| Installments Paid     | number | Yes      | Count of completed installments       | 0 to total installments                     |
| Installments Remaining| number | Yes      | Count of upcoming installments        | Total minus paid                            |
| Next Payment Date     | date   | Conditional | Date of next scheduled installment | Only if installments remaining > 0          |
| Next Payment Amount   | number | Conditional | Amount of next installment         | Only if installments remaining > 0          |
| Payment History       | list   | Yes      | Past installment payments with dates and statuses | Read-only history                 |
| Payment Method        | text   | Yes      | Last 4 digits of card on file         | Masked for security                         |

**Business Rules**:

- Show progress bar: installments completed / total installments
- Display countdown: "X days until next payment"
- Show reminder status: "Reminder sent" or "Reminder pending"
- Highlight overdue installments in red with "Payment Failed - Retry in Progress"
- Allow update of payment method with "Update Card" button
- Show final payment deadline: "All payments complete by [date]"

**Notes**:

- Use visual timeline with checkmarks for completed installments
- Show clear status for each installment: Paid, Scheduled, Overdue, Failed
- Provide download option for payment receipts

---

### Provider Platform Screens

#### Screen 3: Provider Installment Plans Overview

**Purpose**: Allow provider to see all their bookings that use installment plans, with high-level status and risk indicators

**Data Fields**:

| Field Name               | Type   | Required | Description                                           | Validation Rules                          |
|--------------------------|--------|----------|-------------------------------------------------------|-------------------------------------------|
| Booking ID               | text   | Yes      | Unique booking identifier                             | Clickable link to booking detail          |
| Patient Name             | text   | Yes      | Patient full name (revealed post-payment)            | Display only                              |
| Procedure Date           | date   | Yes      | Scheduled procedure date                              | Format: DD-MM-YYYY                        |
| Total Amount             | number | Yes      | Total procedure cost                                  | Matches booking total                     |
| Installments Paid        | number | Yes      | Number of completed installments                      | 0 to total installments                   |
| Total Installments       | number | Yes      | Total installments in plan                            | 2–9                                       |
| Completion Percentage    | number | Yes      | Percentage of total amount collected                  | 0–100% (auto-calculated)                  |
| Next Payment Date        | date   | No       | Date of next scheduled installment (if any)           | Only if installments remaining > 0        |
| Next Payment Amount      | number | No       | Amount of next installment (if any)                   | Only if installments remaining > 0        |
| Plan Status              | badge  | Yes      | "Active", "Completed", "Overdue", "Defaulted"         | Color-coded                               |
| Overdue Days             | number | No       | Days since first missed/failed installment            | Only for "Overdue"/"Defaulted" plans      |

**Business Rules**:

- List includes only bookings for the **current provider** that have an active or completed installment plan (no one-time payments).
- Providers see **status and progress only**; they cannot change payment schedules or retry charges (admin-only actions).
- Overdue and defaulted plans are visually emphasized (e.g., warning badges, sort to top).
- Clicking a row opens the shared **Booking Installment Plan Detail** screen for that booking.

**Notes**:

- Table should support filtering by plan status (Active, Completed, Overdue, Defaulted) and procedure date range.
- Default sort: nearest upcoming procedure date, then highest risk (Overdue/Defaulted) at top.

---

#### Screen 4: Provider Booking Installment Plan Detail

**Purpose**: Provide the provider with a detailed, read-only view of a single booking’s installment plan, schedule, and payment history

**Data Fields**:

| Field Name                | Type   | Required | Description                                          | Validation Rules                          |
|---------------------------|--------|----------|------------------------------------------------------|-------------------------------------------|
| Booking ID                | text   | Yes      | Unique booking identifier                            | Display only                              |
| Patient Name              | text   | Yes      | Patient full name (revealed post-payment)           | Display only                              |
| Provider Name             | text   | Yes      | Clinic/provider name                                 | Display only                              |
| Procedure Date            | date   | Yes      | Scheduled procedure date                             | Format: DD-MM-YYYY                        |
| Total Amount              | number | Yes      | Total procedure cost                                 | Matches booking total                     |
| Total Installments        | number | Yes      | Total installments in plan                           | 2–9                                       |
| Installments Paid         | number | Yes      | Number of completed installments                     | 0 to total installments                   |
| Installments Remaining    | number | Yes      | Number of upcoming installments                      | Total minus paid                          |
| Completion Percentage     | number | Yes      | Percentage of total amount collected                 | 0–100% (auto-calculated)                  |
| Final Payment Deadline    | date   | Yes      | Date by which all installments must be completed     | Must meet configured cutoff rule          |
| Plan Status               | badge  | Yes      | "Active", "Completed", "Overdue", "Defaulted"        | Color-coded                               |
| Payment Method Summary    | text   | Yes      | Masked card details or payment method descriptor     | Display only                              |
| Installment Schedule      | table  | Yes      | Row per installment with date, amount, and status    | See sub-table below                       |

**Installment Schedule Sub-Table**:

| Field Name        | Type   | Required | Description                               | Validation Rules                |
|-------------------|--------|----------|-------------------------------------------|---------------------------------|
| Installment #     | number | Yes      | Sequence number (1..N)                    | 1–9                             |
| Due Date          | date   | Yes      | Scheduled charge date                     | Format: DD-MM-YYYY              |
| Amount            | number | Yes      | Installment amount                        | Must sum to Total Amount        |
| Status            | badge  | Yes      | "Scheduled", "Paid", "Failed", "Retrying" | Color-coded                     |
| Paid Date         | date   | No       | Actual payment date (if paid)             | Present only for Paid           |
| Failure Reason    | text   | No       | Processor error message (if failed)       | Read-only                       |

**Business Rules**:

- View is **read-only**; providers can see schedule and history but **cannot** modify plan or trigger payments.
- If plan is "Overdue" or "Defaulted", show instruction banner: "Please contact Hairline support; payment follow-up is handled by admin team."
- All dates and amounts are consistent with underlying payment records; discrepancies must be treated as data errors and surfaced via internal alerts (out of scope for UI behavior here).

**Notes**:

- This screen is accessible from Provider Installment Plans Overview (provider tenant).
- Layout should reuse components from the patient’s installment schedule view where possible, with additional provider-specific context.

---

### Admin Platform Screens

#### Screen 5: Admin Installment Plan Management Dashboard

**Purpose**: Allow admin to monitor and manage all installment plans across platform

**Data Fields**:

| Field Name                | Type       | Required | Description                                     | Validation Rules          |
|--------------------------|------------|----------|-------------------------------------------------|---------------------------|
| Active Plans Count        | number     | Yes      | Total installment plans currently active        | Non-negative integer      |
| Overdue Installments      | number     | Yes      | Count of failed installments after retries      | Flagged for admin action  |
| Total Installment Revenue | number     | Yes      | Sum of all installment payments collected       | Aggregate across all bookings |
| Average Installments      | number     | Yes      | Average number of installments selected         | Analytics metric          |
| Success Rate              | percentage | Yes      | Successful installment charges / total attempts | Performance indicator     |
| Plan List                 | table      | Yes      | All installment plans with patient, provider, status, progress | Filterable and sortable |

**Business Rules**:

- Flag installment plans with overdue payments (after 3 failed retries)
- Show aging report: days overdue for failed installments
- Allow admin to manually retry failed installment
- Allow admin to contact patient for payment resolution
- Allow admin to cancel booking for chronically defaulted plans
- Show revenue forecast based on scheduled installments

**Notes**:

- Use dashboard widgets for key metrics
- Provide drill-down into individual installment plan details
- Export capabilities for financial reporting and reconciliation

---

#### Screen 6: Admin Booking Installment Plan Detail

**Purpose**: Provide admin with a detailed, actionable view of a single booking’s installment plan, schedule, and payment history, including controls for resolving payment issues

**Data Fields**:

| Field Name                | Type   | Required | Description                                          | Validation Rules                          |
|---------------------------|--------|----------|------------------------------------------------------|-------------------------------------------|
| Booking ID                | text   | Yes      | Unique booking identifier                            | Display only                              |
| Patient Name              | text   | Yes      | Patient full name                                    | Display only                              |
| Provider Name             | text   | Yes      | Clinic/provider name                                 | Display only                              |
| Procedure Date            | date   | Yes      | Scheduled procedure date                             | Format: DD-MM-YYYY                        |
| Total Amount              | number | Yes      | Total procedure cost                                 | Matches booking total                     |
| Total Installments        | number | Yes      | Total installments in plan                           | 2–9                                       |
| Installments Paid         | number | Yes      | Number of completed installments                     | 0 to total installments                   |
| Installments Remaining    | number | Yes      | Number of upcoming installments                      | Total minus paid                          |
| Completion Percentage     | number | Yes      | Percentage of total amount collected                 | 0–100% (auto-calculated)                  |
| Final Payment Deadline    | date   | Yes      | Date by which all installments must be completed     | Must meet configured cutoff rule          |
| Plan Status               | badge  | Yes      | "Active", "Completed", "Overdue", "Defaulted"        | Color-coded                               |
| Payment Method Summary    | text   | Yes      | Masked card details or payment method descriptor     | Display only                              |
| Installment Schedule      | table  | Yes      | Row per installment with date, amount, and status    | Same structure as provider detail screen  |
| Admin Action Panel        | group  | Yes      | Section with admin-only controls and justification   | See Business Rules                        |

**Business Rules**:

- Admin can perform the following actions (subject to internal policy and audit logging):
  - **Retry Charge** on a failed installment (invokes payment processor via S-02).
  - **Mark as Resolved** when an external/manual payment issue has been handled.
  - **Cancel Plan & Apply Cancellation Policy**, which:
    - Stops future installments.
    - Calculates refunds per cancellation policy.
    - Updates booking status per Business Workflows.
- All admin actions MUST:
  - Require a justification text input (minimum 20 characters).
  - Be logged with timestamp, admin ID, action type, and justification.
- Certain actions are only available based on plan status:
  - "Retry Charge" available only for "Failed" or "Overdue" installments.
  - "Cancel Plan & Apply Cancellation Policy" available for "Active" or "Overdue" plans; disabled for "Completed" plans.
- Admin cannot directly edit financial amounts; changes must be made via refunds/adjustments defined in payment rules.

**Notes**:

- This screen is accessible from the Admin Installment Plan Management Dashboard when an admin clicks into a specific plan.
- Layout should reuse the same base visual structure as the provider detail screen, with the additional Admin Action Panel.

---

## Business Rules

### General Module Rules

- Installment plans are interest-free (0% APR) for all patients
- Available installment options: 2, 3, 4, 5, 6, 7, 8, or 9 monthly payments (enabled in FR-029)
- Final payment MUST complete by the configured cutoff days before scheduled procedure date (minimum 30 days; configured in FR-029)
- System offers only installment counts that are feasible given booking date, procedure date, monthly frequency, and the cutoff window
- First installment charged immediately upon booking confirmation
- Subsequent installments charged monthly (30-day intervals)
- Installment amount calculated as: total procedure cost ÷ number of installments (rounded to 2 decimal places)
- Patient can choose fewer installments than maximum available (pay faster)
- Single full payment option always available as alternative to installments

### Data & Privacy Rules

- Payment method details stored securely per PCI-DSS standards (via payment processor)
- Platform does not store full credit card numbers (only tokenized references)
- All installment payment records encrypted at rest and in transit
- Access to installment payment data follows RBAC: patients see their own installments; providers see booking payment status; admins see all plans
- All installment lifecycle events logged for tamper-evident audit trail
- Compliance: PCI-DSS (via processor), GDPR/HIPAA-aligned handling of payment data

### Admin Editability Rules

**Editable by Admin**:

- Customer-facing installment plan settings are configured via **FR-029 (A-09)**:
  - Enabled installment counts (2-9)
  - Cutoff days (30-90) requiring full payment completion before procedure date
  - Minimum booking amount eligibility threshold
  - First installment type (deposit vs equal split)
  - Late payment grace period before booking cancellation

**Fixed in Codebase (Not Editable)**:

- Interest rate (always 0% - interest-free policy)
- Installment frequency (monthly; 30-day intervals)
- Core payment security controls and encryption standards
- Number of retry attempts for failed payments (3 attempts)
- Retry schedule for failed payments (1 day, 3 days, 7 days later)
- Reminder timing (3 days before due date)
- Audit logging scope for payment events

**Configurable with Restrictions**:

- Cancellation refund policy for installment plans (admin sets percentages per timing window)
- Payment processor integration settings (requires technical deployment, not runtime editable)

### Payment & Billing Rules

- Installment charges are automatic on scheduled dates (patient consent given at checkout)
- Failed installments trigger 3 automatic retry attempts: 1 day, 3 days, 7 days later
- After 3 failed retries, installment plan marked as "Defaulted" and admin notified
- Patient can update payment method anytime before next installment
- Cancellation refunds calculated based on timing: >30 days = 90% of paid installments; 15-30 days = 50%; <15 days = no refund
- Platform commission calculated on total procedure cost (commission rate configured in FR-029 and snapshotted at booking), deducted from provider payout after final installment completes
- Provider payout delayed until all installments completed and booking reaches "Fully Paid" status
- Rescheduling procedure date may require installment plan adjustment or immediate payment of remaining balance

### Admin Action & Audit Rules

Per Hairline Platform Constitution (Principle VI: Data Integrity & Audit Trail), all admin actions that modify installment plan state MUST be audited:

**Admin Actions Requiring Justification & Audit Logging**:

- **Retry Charge**: Manually triggering a payment retry on a failed installment (requires justification minimum 20 characters; logged with timestamp, admin ID, action type, installment ID, retry attempt number)
- **Mark as Resolved**: Marking a failed installment as resolved when external/manual payment has been handled (requires justification minimum 20 characters; logged with timestamp, admin ID, action type, installment ID, resolution method)
- **Cancel Plan & Apply Cancellation Policy**: Canceling an active installment plan and applying refund policy (requires justification minimum 20 characters; logged with timestamp, admin ID, action type, installment plan ID, booking ID, refund amount, cancellation reason)

**Audit Trail Requirements**:

- All admin actions documented in Screen 6 (Admin Booking Installment Plan Detail) MUST be logged to the immutable audit trail system (S-06: Audit Log Service)
- Audit logs MUST be retained for 10 years per constitution requirements
- Audit logs MUST include: timestamp (UTC), admin user ID, admin name, action type, affected entity IDs (installment plan ID, booking ID, patient ID), justification text, before/after state (if applicable), IP address
- Failed admin action attempts (e.g., insufficient permissions, validation errors) MUST also be logged
- Audit logs MUST be tamper-proof and queryable for compliance reporting

**Access Control**:

- Only authorized admin roles (Billing Admin, Financial Manager, Super Admin) can execute installment management actions
- Role-based access control (RBAC) enforced per FR-031 (Admin Access Control & Permissions)
- All installment data access (read and write) is subject to RBAC validation

---

## Success Criteria

### Patient Experience Metrics

- **SC-001**: Patients can select and confirm installment plan within 2 minutes of reaching checkout
- **SC-002**: 90% of patients successfully complete installment plan enrollment on first attempt without errors
- **SC-003**: 80% of patients find installment plan options clear and understandable (survey-based)

### Provider Efficiency Metrics

- **SC-004**: Providers can view installment payment status for any booking in under 30 seconds
- **SC-005**: Providers receive payout within 2 business days after final installment completes and procedure finishes
- **SC-006**: 95% of bookings with installment plans result in full payment completion

### Admin Management Metrics

- **SC-007**: Admins can identify and resolve defaulted installment plans within 24 hours of flag
- **SC-008**: Admin-configured installment parameters (buffer, max installments) apply to new bookings within 1 minute
- **SC-009**: 100% of installment payment lifecycle events (scheduled, charged, failed, retried) are auditable

### System Performance Metrics

- **SC-010**: 95% of scheduled installment charges execute within 5 minutes of due time
- **SC-011**: Payment reminders sent within 1 hour of scheduled time (3 days before due)
- **SC-012**: Failed payment retry logic executes automatically without manual intervention
- **SC-013**: Zero duplicate charges on idempotent retries in all tested scenarios

### Business Impact Metrics

- **SC-014**: Booking conversion rate increases by 20% due to installment plan availability
- **SC-015**: Installment plan adoption reaches 40% of all bookings within first 3 months
- **SC-016**: Average transaction value increases by 15% (patients book higher-cost procedures with installments)
- **SC-017**: Installment payment success rate ≥ 92% (successful charges / total attempted charges)
- **SC-018**: Defaulted installment plans < 5% of all active plans

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **FR-006: Booking & Scheduling**
  - **Why needed**: Installment plan tied to booking confirmation and procedure date
  - **Integration point**: Booking creation triggers installment plan setup; procedure date determines maximum installments

- **FR-007: Payment Processing**
  - **Why needed**: Core payment infrastructure for processing installment charges
  - **Integration point**: Uses same payment gateway, security controls, receipt generation; installments extend deposit/final payment logic

- **P-01: Auth & Profile Management**
  - **Why needed**: Only authenticated patients can enroll in installment plans
  - **Integration point**: Patient profile linked to installment payment schedule and history

- **A-05: Billing & Financial Reconciliation**
  - **Why needed**: Admin oversight of installment plans and revenue reconciliation
  - **Integration point**: Installment revenue tracked separately from one-time payments; affects provider payout timing

- **S-03: Notification Service**
  - **Why needed**: Send installment reminders, confirmations, and failure notifications
  - **Integration point**: Triggers on installment lifecycle events (scheduled, charged, failed, completed)

### External Dependencies (APIs, Services)

- **PCI-compliant Payment Processor (Stripe)**
  - **Purpose**: Processes recurring installment charges; stores tokenized payment methods; handles automatic retries
  - **Integration**: Scheduled charge API, payment method tokenization, webhook notifications for charge status
  - **Failure handling**: Retry logic with exponential backoff; notify patient and admin of persistent failures; support manual payment submission

- **Scheduled Job Processor**
  - **Purpose**: Executes time-based installment charges and reminders
  - **Integration**: Cron-based or queue-based job scheduling for installment due dates
  - **Failure handling**: Queue failed jobs for retry; alert admin if scheduling system unavailable

### Data Dependencies

- **Active booking with procedure date**
  - **Why needed**: Calculate available installments and payment schedule
  - **Source**: Booking & Scheduling module (FR-006)

- **Accepted quote with total pricing**
  - **Why needed**: Calculate installment amounts
  - **Source**: Quote acceptance flow (FR-005)

- **Patient payment method on file**
  - **Why needed**: Process recurring installment charges
  - **Source**: Patient payment method enrollment during checkout

---

## Assumptions

### User Behavior Assumptions

- Patients prefer smaller monthly payments over single large payment
- Patients will keep payment method valid for duration of installment plan
- Patients check email/app for installment reminders before due date
- Patients understand "interest-free" means no additional charges beyond procedure cost
- Most patients will complete installment plans without defaulting

### Technology Assumptions

- Payment processor supports scheduled/recurring charges
- Payment processor provides webhook notifications for charge success/failure
- Mobile app has reliable push notification delivery for reminders
- Patients have access to email and mobile app for payment notifications
- System has scheduled job processor for timely installment execution

### Business Process Assumptions

- 30-day buffer before procedure is sufficient for final payment confirmation
- 3 retry attempts with increasing delays adequate to resolve temporary payment issues
- Admin intervention required only for persistent payment failures after retries
- Provider payouts can be delayed until installment plan completes (acceptable business terms)
- Cancellation refund policy applies same percentages to installment plans as single payments
- Rescheduling procedure date is infrequent enough that manual installment adjustment is acceptable

---

## Implementation Notes

### Technical Considerations

- Scheduled jobs must execute reliably on exact dates (use robust job queue with monitoring)
- Installment charges must be idempotent (prevent duplicate charges on retry)
- Payment method tokenization required for recurring charges (do not store card details)
- Timezone handling critical for installment due dates (use UTC internally, display in patient timezone)
- Financial calculations must round correctly (avoid floating point errors)

### Performance Targets

Per Hairline Platform Constitution (Principle VIII: Performance & Scalability):

- **API response times**: p95 < 500ms, p99 < 1000ms (excluding external payment processor calls)
- **Installment calculation**: < 200ms for determining available options and calculating schedule
- **Schedule retrieval**: < 300ms for loading patient installment history and upcoming payments
- **Admin dashboard queries**: < 500ms for installment plan list and filtering operations
- **Payment processing**: Acknowledge charge initiation within 100ms; actual charge completion time depends on payment processor (typically 2-5 seconds)
- **Reminder job execution**: 95% of reminders sent within 1 hour of scheduled time (3 days before due date)
- **Retry job scheduling**: Failed payment retries scheduled within 5 minutes of failure detection

### Integration Points

- Payment processor webhook integration for charge status updates (success, failure, requires action)
- Notification service triggers on installment lifecycle events
- Booking status updates when installment milestones reached (first charge, final charge, default)
- Admin dashboard polling for real-time installment plan monitoring

### Scalability Considerations

- Expected 200-500 bookings/month at launch; 40% may use installments = 80-200 active installment plans
- Plan for 10x growth within 12 months: 2,000 active installment plans
- Each plan has 2-9 scheduled charges = 4,000-18,000 scheduled jobs over plan lifetimes
- Peak load on monthly payment dates (concentrated around 1st of month if patients book similarly)
- Ensure job queue can handle 500+ simultaneous installment charges on peak days

### Security Considerations

- RBAC enforced across tenants; patients see only their own installment data
- All payment method details tokenized (never store card numbers)
- Installment schedule and amounts are immutable once confirmed (prevent tampering)
- Full audit trail for all installment payment attempts (success, failure, retry, refund)
- Admin access to installment management logged with user ID and timestamp
- Compliance alignment with PCI-DSS for recurring charges

---

## User Scenarios & Testing

### User Story 1 - Select Installment Plan at Checkout (Priority: P1)

Patient selects installment plan during booking checkout, sees payment schedule, and confirms first installment to secure booking.

**Why this priority**: Core functionality enabling patients to access installment plans; critical for feature adoption and business value.

**Independent Test**: Create a booking with procedure date 6 months away; select 4 installment plan; confirm first payment; verify booking confirmed and remaining 3 installments scheduled.

**Acceptance Scenarios**:

1. **Given** a booking with procedure in 6 months (180 days), **When** patient views checkout, **Then** system displays installment options 2-5 (maximum 5 installments allowed per calculation)
2. **Given** patient selects 4 installment plan, **When** patient reviews payment schedule, **Then** system shows 4 equal installments with first charged today and remaining monthly
3. **Given** patient confirms installment plan, **When** first installment processes successfully, **Then** booking is confirmed and remaining 3 installments are scheduled at 30-day intervals

---

### User Story 2 - Automatic Installment Charging and Reminders (Priority: P1)

System sends reminder 3 days before installment due, automatically charges payment method on due date, and confirms successful payment to patient.

**Why this priority**: Core automation that reduces manual work and ensures timely payments; essential for installment plans to function.

**Independent Test**: Set up installment plan with test dates; trigger reminder 3 days before due; trigger automatic charge on due date; verify payment processed and confirmation sent.

**Acceptance Scenarios**:

1. **Given** an installment due in 3 days, **When** reminder trigger executes, **Then** patient receives email and push notification with amount and date
2. **Given** installment due date arrives, **When** scheduled charge executes, **Then** payment method is charged automatically
3. **Given** installment charge succeeds, **When** payment confirmed, **Then** patient receives confirmation notification and installment marked as paid in booking details

---

### User Story 3 - Handle Failed Installment Payments (Priority: P1)

System detects failed installment charge, notifies patient immediately, executes 3 retry attempts with increasing delays, and flags plan as defaulted if all retries fail.

**Why this priority**: Critical error handling to recover from payment failures and protect revenue; prevents silent failures.

**Independent Test**: Simulate failed installment charge; verify immediate patient notification; verify 3 retry attempts execute on schedule (1 day, 3 days, 7 days); verify admin notification if all retries fail.

**Acceptance Scenarios**:

1. **Given** scheduled installment charge fails, **When** failure detected, **Then** patient is notified immediately with clear error message and guidance
2. **Given** first retry attempt is due (1 day later), **When** retry executes and fails, **Then** system schedules second retry for 3 days later
3. **Given** all 3 retry attempts fail, **When** retries exhausted, **Then** system flags installment plan as "Defaulted" and notifies admin for intervention

---

### User Story 4 - Patient Updates Payment Method Mid-Plan (Priority: P2)

Patient navigates to booking details, selects "Update Payment Method," provides new card details, and confirms; remaining installments charged to new card.

**Why this priority**: Important for user experience and reducing failed payments due to expired cards; secondary to core flows.

**Independent Test**: Create active installment plan; patient updates payment method; verify new method saved; trigger next installment charge and verify new method used.

**Acceptance Scenarios**:

1. **Given** patient has active installment plan, **When** patient navigates to booking details and selects "Update Payment Method," **Then** secure payment form displayed
2. **Given** patient provides valid new payment method, **When** patient confirms, **Then** system validates and saves new payment method
3. **Given** new payment method saved, **When** next installment charge executes, **Then** new payment method is charged (not old method)

---

### User Story 5 - Admin Manages Defaulted Installment Plans (Priority: P2)

Admin views dashboard showing defaulted installment plans (failed after 3 retries), reviews patient and booking details, contacts patient to resolve, and manually retries payment or cancels booking.

**Why this priority**: Important for recovering revenue and maintaining booking integrity; handled by admin so not patient-blocking.

**Independent Test**: Create defaulted installment plan; admin views flagged plan in dashboard; admin initiates manual retry; verify payment processed or booking canceled per admin decision.

**Acceptance Scenarios**:

1. **Given** an installment plan flagged as "Defaulted," **When** admin views installment management dashboard, **Then** defaulted plan appears with patient, booking, and overdue details
2. **Given** admin reviews defaulted plan, **When** admin contacts patient and resolves payment issue, **Then** admin can manually trigger payment retry
3. **Given** payment issue unresolved, **When** admin decides to cancel booking, **Then** system cancels booking, refunds per policy, and cancels remaining installments

---

### User Story 6 - Patient Cancels Booking With Partial Installments Paid (Priority: P3)

Patient requests booking cancellation after paying 2 of 4 installments; admin reviews cancellation timing; system calculates refund per policy; refund processed and remaining installments canceled.

**Why this priority**: Less frequent scenario (cancellations are minority of bookings); important for fairness but not core to happy path.

**Independent Test**: Create installment plan with 2 of 4 installments paid; patient requests cancellation 20 days before procedure; verify refund calculated at 50% of paid amount; verify remaining 2 installments canceled.

**Acceptance Scenarios**:

1. **Given** patient has paid 2 of 4 installments, **When** patient requests cancellation 20 days before procedure, **Then** system calculates refund as 50% of paid amount per cancellation policy
2. **Given** refund calculated, **When** admin approves cancellation, **Then** refund is processed to patient's original payment method
3. **Given** cancellation confirmed, **When** system updates booking status, **Then** remaining 2 installments are canceled (not charged)

---

### Edge Cases

- What happens when patient's payment method expires mid-plan? (Charge fails; retry logic engages; patient notified to update card)
- How does system handle procedure date rescheduled after installment plan established? (Recalculate installment schedule if sufficient time; otherwise require immediate payment of remaining balance)
- What occurs if first installment fails at checkout? (Booking not confirmed; patient prompted to retry immediately or use different payment method)
- How to manage patient requesting fewer installments mid-plan? (Not supported; patient can pay remaining balance early to complete plan)
- What if admin increases the cutoff window from 30 to 45 days via FR-029? (Applies only to new bookings; existing installment plans unchanged)
- How does system handle refund for partial installments if patient disputes charge? (Admin reviews dispute; processes refund per resolution; may cancel booking or allow continuation)
- What if payment processor webhook fails to deliver charge status? (System polls payment status as fallback; ensures no missed confirmations or retries)

---

## Functional Requirements Summary

### Core Requirements

- **REQ-007b-001**: System MUST offer interest-free installment payment plans with 2-9 monthly payments
- **REQ-007b-002**: System MUST determine feasible installment options based on time until procedure, monthly frequency, and cutoff days configured in FR-029 (minimum 30 days); offered options are limited to enabled installment counts configured in FR-029 (2-9)
- **REQ-007b-003**: System MUST enforce the cutoff window: final installment must complete by the configured cutoff days before procedure date (minimum 30 days; configured in FR-029)
- **REQ-007b-004**: System MUST calculate installment amounts as: total procedure cost ÷ number of installments
- **REQ-007b-005**: System MUST charge first installment immediately upon booking confirmation
- **REQ-007b-006**: System MUST schedule remaining installments at 30-day intervals

### Data Requirements

- **REQ-007b-007**: System MUST maintain installment schedule with amounts and due dates per booking
- **REQ-007b-008**: System MUST track installment payment status: scheduled, paid, failed, retried, overdue
- **REQ-007b-009**: System MUST persist patient payment method securely for recurring charges (tokenized)

### Security & Privacy Requirements

- **REQ-007b-010**: System MUST tokenize payment methods (never store full card numbers)
- **REQ-007b-011**: System MUST encrypt all installment payment records at rest and in transit
- **REQ-007b-012**: System MUST log all installment payment attempts with timestamp, amount, status, and user

### Integration Requirements

- **REQ-007b-013**: System MUST integrate with payment processor for scheduled/recurring charges
- **REQ-007b-014**: System MUST send payment reminders 3 days before each installment due date
- **REQ-007b-015**: System MUST automatically charge payment method on installment due date
- **REQ-007b-016**: System MUST send confirmation notification after successful installment charge

### Error Handling Requirements

- **REQ-007b-017**: System MUST detect failed installment charges and notify patient immediately
- **REQ-007b-018**: System MUST execute 3 automatic retry attempts for failed installments: 1 day, 3 days, 7 days later
- **REQ-007b-019**: System MUST flag installment plan as "Defaulted" after 3 failed retry attempts
- **REQ-007b-020**: System MUST notify admin of defaulted installment plans for intervention

### Cancellation & Refund Requirements

- **REQ-007b-021**: System MUST support patient-initiated payment method updates for active installment plans
- **REQ-007b-022**: System MUST calculate refunds for canceled bookings with partial installments paid per cancellation policy
- **REQ-007b-023**: System MUST cancel remaining installments when booking is canceled
- **REQ-007b-024**: System MUST handle procedure date rescheduling by recalculating installment schedule or requiring immediate payment

---

## Key Entities

- **Entity 1 - Installment Plan**: Represents the payment schedule for a booking
  - **Key attributes**: booking ID, total amount, number of installments, installment amount, cutoff_days, creation date, status (active, completed, defaulted, canceled)
  - **Relationships**: belongs to one booking; has many installment payments; linked to one patient payment method

- **Entity 2 - Installment Payment**: Represents a single scheduled/completed installment charge
  - **Key attributes**: installment plan ID, due date, amount, status (scheduled, paid, failed, retried, overdue), payment date, retry count, failure reason
  - **Relationships**: belongs to one installment plan; linked to payment transaction record

- **Entity 3 - Payment Method**: Represents tokenized recurring payment method
  - **Key attributes**: token/reference ID, last 4 digits, expiration date, patient ID, active status
  - **Relationships**: belongs to one patient; used by one or more installment plans

---

## Appendix: Change Log

| Date       | Version | Changes                 | Author |
|------------|---------|-------------------------|--------|
| 2025-11-10 | 1.0     | Initial PRD creation    | AI     |
| 2025-12-16 | 1.1     | Documentation alignment: Moved customer-facing installment configuration ownership to FR-029 (cutoff days, enabled installment counts, eligibility thresholds) and removed conflicting admin-configurable ranges/formulas; retained monthly schedule execution and retry/reminder behavior here. | AI |
| 2026-02-12 | 1.2     | Constitution alignment enhancements: Added explicit performance targets (p95 < 500ms API response times, job execution timing) to Implementation Notes; added Admin Action & Audit Rules subsection documenting audit logging requirements for admin actions (retry charge, mark as resolved, cancel plan) per Constitution Principle VI. | AI |

---

## Appendix: Approvals

| Role            | Name   | Date   | Signature/Approval |
|-----------------|--------|--------|--------------------|
| Product Owner   | [Name] | [Date] | [Status]           |
| Technical Lead  | [Name] | [Date] | [Status]           |
| Stakeholder     | [Name] | [Date] | [Status]           |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0
**Based on**: FR-007B from system-prd.md (Split Payment / Installment Plans)
**Last Updated**: 2026-02-12
