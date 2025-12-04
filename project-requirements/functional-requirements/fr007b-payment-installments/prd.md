# Product Requirements Document: Split Payment / Installment Plans (FR-007B)

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
- **Admin Platform (A-05)**: Admin monitors installment plans across all bookings; configures installment plan parameters (number of installments, buffer period); handles defaulted installment plans; processes refunds for installment plans
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

- Configure installment plan parameters: allowed number of installments (2-9), mandatory buffer period before procedure (default 30 days)
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

- Patient selects installment plan during booking checkout after accepting a quote
- Patient views installment schedule from booking details screen
- Admin accesses installment management from billing/financial management module
- Provider views installment status from booking overview screen

---

## Business Workflows

### Main Flow: Patient Selects Installment Plan and Completes Payments

**Actors**: Patient, System (Payment Processing Service), Admin
**Trigger**: Patient proceeds to checkout after accepting a quote
**Outcome**: Booking confirmed with installment plan; scheduled installments charged automatically; booking fully paid 30 days before procedure

**Steps**:

1. Patient reviews booking summary with total procedure cost
2. System calculates maximum available installments based on time until procedure date (procedure date minus 30-day buffer, divided by monthly installments)
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
14. When final installment completes (30 days before procedure), System marks booking as "Fully Paid"

### Alternative Flows

**A1: Patient Chooses Fewer Installments Than Maximum Available**:

- **Trigger**: Patient wants to pay faster than the maximum allowed installments
- **Steps**:
  1. Patient selects fewer installments (e.g., 3 installments when 6 are available)
  2. System calculates higher installment amount with same total
  3. System adjusts payment schedule accordingly
- **Outcome**: Booking completed with shorter payment timeline; same 30-day buffer maintained

**A2: Patient Opts for Full Payment Instead of Installments**:

- **Trigger**: Patient prefers to pay entire amount upfront
- **Steps**:
  1. Patient selects "Pay in Full" option at checkout
  2. System processes full payment immediately
  3. System marks booking as "Fully Paid"
- **Outcome**: Booking confirmed without installment plan; same as existing FR-007 payment flow

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

- **Trigger**: Patient or provider reschedules procedure date
- **Steps**:
  1. Rescheduling request triggers installment plan recalculation
  2. System checks if new procedure date allows completion of remaining installments (30-day buffer)
  3. **If sufficient time**: System adjusts installment schedule dates to align with new procedure date
  4. **If insufficient time**: System notifies patient that remaining balance must be paid immediately or installment plan canceled
  5. Patient chooses to pay remaining balance or cancel booking
- **Outcome**: Installment plan adjusted to new schedule or remaining balance paid immediately; booking date updated

---

## Screen Specifications

### Screen 1: Patient Checkout - Installment Plan Selection

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

### Screen 2: Patient Booking Details - Installment Schedule View

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

### Screen 3: Admin Installment Plan Management Dashboard

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

## Business Rules

### General Module Rules

- Installment plans are interest-free (0% APR) for all patients
- Available installment options: 2, 3, 4, 5, 6, 7, 8, or 9 monthly payments
- Final payment MUST complete 30 days before scheduled procedure date (mandatory buffer)
- Maximum installments calculated as: (days until procedure - 30) ÷ 30, capped at 9
- Minimum time for installment plan: 60 days (allows 2 installments + 30-day buffer)
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

- Installment buffer period (default 30 days, configurable range 14-60 days)
- Maximum number of installments allowed (default 9, configurable range 2-12)
- Retry attempt timing (default: 1 day, 3 days, 7 days)
- Payment reminder timing (default: 3 days before due)
- Late fees for failed installments (optional, configurable per policy)

**Fixed in Codebase (Not Editable)**:

- Interest rate (always 0% - interest-free policy)
- Core payment security controls and encryption standards
- Number of retry attempts for failed payments (3 attempts)
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
- Platform commission calculated on total procedure cost, deducted from provider payout after final installment completes
- Provider payout delayed until all installments completed and booking reaches "Fully Paid" status
- Rescheduling procedure date may require installment plan adjustment or immediate payment of remaining balance

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
- What if admin changes installment buffer period from 30 to 14 days? (Applies only to new bookings; existing installment plans unchanged)
- How does system handle refund for partial installments if patient disputes charge? (Admin reviews dispute; processes refund per resolution; may cancel booking or allow continuation)
- What if payment processor webhook fails to deliver charge status? (System polls payment status as fallback; ensures no missed confirmations or retries)

---

## Functional Requirements Summary

### Core Requirements

- **FR-001**: System MUST offer interest-free installment payment plans with 2-9 monthly payments
- **FR-002**: System MUST calculate maximum available installments based on time until procedure: (days until procedure - 30) ÷ 30, capped at 9
- **FR-003**: System MUST enforce 30-day buffer: final installment must complete 30 days before procedure date
- **FR-004**: System MUST calculate installment amounts as: total procedure cost ÷ number of installments
- **FR-005**: System MUST charge first installment immediately upon booking confirmation
- **FR-006**: System MUST schedule remaining installments at 30-day intervals

### Data Requirements

- **FR-007**: System MUST maintain installment schedule with amounts and due dates per booking
- **FR-008**: System MUST track installment payment status: scheduled, paid, failed, retried, overdue
- **FR-009**: System MUST persist patient payment method securely for recurring charges (tokenized)

### Security & Privacy Requirements

- **FR-010**: System MUST tokenize payment methods (never store full card numbers)
- **FR-011**: System MUST encrypt all installment payment records at rest and in transit
- **FR-012**: System MUST log all installment payment attempts with timestamp, amount, status, and user

### Integration Requirements

- **FR-013**: System MUST integrate with payment processor for scheduled/recurring charges
- **FR-014**: System MUST send payment reminders 3 days before each installment due date
- **FR-015**: System MUST automatically charge payment method on installment due date
- **FR-016**: System MUST send confirmation notification after successful installment charge

### Error Handling Requirements

- **FR-017**: System MUST detect failed installment charges and notify patient immediately
- **FR-018**: System MUST execute 3 automatic retry attempts for failed installments: 1 day, 3 days, 7 days later
- **FR-019**: System MUST flag installment plan as "Defaulted" after 3 failed retry attempts
- **FR-020**: System MUST notify admin of defaulted installment plans for intervention

### Cancellation & Refund Requirements

- **FR-021**: System MUST support patient-initiated payment method updates for active installment plans
- **FR-022**: System MUST calculate refunds for canceled bookings with partial installments paid per cancellation policy
- **FR-023**: System MUST cancel remaining installments when booking is canceled
- **FR-024**: System MUST handle procedure date rescheduling by recalculating installment schedule or requiring immediate payment

---

## Key Entities

- **Entity 1 - Installment Plan**: Represents the payment schedule for a booking
  - **Key attributes**: booking ID, total amount, number of installments, installment amount, buffer period, creation date, status (active, completed, defaulted, canceled)
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
| [DATE]     | 1.1     | [Description of changes]| [Name] |

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
**Last Updated**: 2025-11-10
