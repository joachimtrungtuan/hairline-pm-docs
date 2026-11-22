# FR-007B - Split Payment / Installment Plans

**Module**: P-03: Booking & Payment | S-02: Payment Processing Service
**Feature Branch**: `fr007b-payment-installments`
**Created**: 2025-11-10
**Status**: 🟡 Revised — Pending Consolidated Verification
**Source**: FR-007B from local-docs/project-requirements/system-prd.md (Split Payment / Installment Plans) + Constitution (.specify/memory/constitution.md)

---

## Executive Summary

Enable patients to pay for hair transplant procedures through interest-free installment plans spanning 2-9 months, providing financial flexibility while ensuring full payment completion by the cutoff before the scheduled procedure date (30 days is the minimum and default, set in FR-029). The installment system automatically calculates available payment plans based on the time remaining until the procedure, handles scheduled automatic charges, manages payment failures with retry logic, and notifies both patients and admins of payment status. This feature focuses on what patients need (flexible payment options with clear terms) and why (making procedures more accessible while protecting provider and platform revenue), without prescribing how the technical implementation should work.

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
- Receive alerts for overdue installments that may affect booking (REQ-007B-032)
- Access payment history for installment-based bookings

**Admin Platform (A-05)**:

- View installment plan configuration (managed in FR-029) and link to configuration screen for authorized users (REQ-007B-079)
- Monitor all active installment plans across the platform
- View installment payment success/failure rates
- Handle defaulted installment plans (failed payments after retries)
- Process refunds for canceled bookings with partial installment payments
- Generate reports on installment plan usage and performance (REQ-007B-075)
- View aging reports for overdue installments

**Shared Services (S-02, S-03)**:

- S-02: Processes scheduled installment charges on due dates; executes retry logic for failed payments (3 attempts, only after a technical failure); calculates available installments based on procedure date
- S-03: Sends reminders 3 days before installment due; sends payment confirmations and failure notifications; alerts admins of payment issues

### Communication Structure

**In Scope**:

- Email/push notifications for installment payment reminders (3 days before due date) (REQ-007B-092)
- Payment confirmation notifications for successful installment charges
- Payment failure notifications for declined/failed installments
- Admin alerts for defaulted installment plans
- Provider alert when an installment becomes overdue
- Patient insufficient-time notice when a procedure date change leaves too little time for the remaining installments
- Booking status change notifications when final installment completes (REQ-007B-093)

**Out of Scope**:

- SMS notifications (handled by S-03 channel configuration; **no SMS installment notifications are available in MVP and this channel is a future enhancement**) (REQ-007B-092)
- Chat/messaging between patient and provider about payment terms (REQ-007B-092)
- Marketing content about installment plans (REQ-007B-092)

### Entry Points

- Patient has accepted a quote (FR-005) and reaches the **Payment Options** step in the booking & payment flow (FR-006/FR-007), then selects **"Pay in Installments"**, which hands off to FR-007B Screen 1 (REQ-007B-028)
- Patient views installment schedule from booking details screen (REQ-007B-028)
- Admin accesses installment management from billing/financial management module (REQ-007B-028)
- Provider views installment status from booking overview screen (REQ-007B-028)

---

## Business Workflows

### Main Flow: Patient Selects Installment Plan and Completes Payments

**Actors**: Patient, System (Payment Processing Service), Admin
**Upstream Context**: Subquote has been accepted (FR-005) and booking details are available via FR-006: the procedure date, and the plan total, currency and exchange rate copied read-only from the FR-005 accepted snapshot through the booking; FR-007 has presented a **Payment Options** step where the patient chose **"Pay in Installments"** instead of **"Pay in Full"**.
**Trigger**: Patient confirms the choice to **"Pay in Installments"** on the Payment Options step and proceeds to the Installment Plan selection screen (Screen 1 in this FR)
**Outcome**: Booking confirmed with installment plan; scheduled installments charged automatically; booking fully paid by the configured cutoff date (minimum 30 days before procedure, configured via FR-029)

**Steps**:

1. Patient reviews booking summary with the booking total (accepted price after promotion) in the accepted currency and sees that **"Pay in Installments"** is selected as the payment option
2. System calculates feasible installment options based on time until procedure date and the configured cutoff days (minimum 30 days before procedure, configured via FR-029) with monthly installments
3. System displays installment options (e.g., "Pay in 2-6 installments" if procedure is in 6 months)
4. Patient selects desired installment plan (e.g., 4 monthly installments)
5. System calculates installment amount (total ÷ number of installments) and displays payment schedule with dates
6. Patient confirms installment plan selection and provides payment method
7. System charges the first installment at checkout; its success confirms the existing `Accepted` booking (FR-006) and consumes any promotion use reserved at acceptance (FR-019)
8. System schedules remaining installments on monthly intervals
9. System records the booking as `Confirmed` (FR-006) with installment plan status active
10. Three days before each scheduled installment, System sends reminder to patient
11. On due date, System automatically charges payment method
12. On successful charge, System updates installment status and sends confirmation
13. System repeats steps 10-12 for each remaining installment
14. When final installment completes by the cutoff date, System marks the installment plan as completed (shown as "Fully Paid"); the booking status continues to follow FR-006

### Alternative Flows

**A1: Patient Chooses Fewer Installments Than Maximum Available**:

- **Trigger**: Patient wants to pay faster than the maximum allowed installments
- **Steps**:
  1. Patient selects fewer installments (e.g., 3 installments when 6 are available)
  2. System calculates higher installment amount with same total
  3. System adjusts payment schedule accordingly
- **Outcome**: Booking completed with shorter payment timeline; same cutoff window maintained

**A2: Patient Opts for Full Payment Instead of Installments (Handled by FR-007)**:

- **Trigger**: On the Payment Options step (FR-007), patient selects **"Pay in Full"** instead of **"Pay in Installments"**
- **Steps** (owned by FR-007, summarized here for branching clarity):
  1. System routes patient to the standard full-payment checkout flow defined in FR-007
  2. System processes full payment immediately
  3. System records the payment as paid in full; booking status follows FR-006 (`Confirmed` on successful payment)
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
  3. If the failure was technical, System schedules first retry attempt after a wait of 1 day
  4. If retry fails, System waits 3 days and attempts second retry
  5. If second retry fails, System waits 7 days and attempts third retry
  6. If all 3 retries fail, System flags installment plan as "Defaulted"
  7. System notifies the admin, the patient and the provider of the defaulted plan and overdue booking
  8. Admin reviews and contacts patient to resolve payment issue
- **Hard decline**: If the charge was hard declined (the issuer refuses the payment), System does not retry automatically; the patient is notified and must retry or update the card
- **Outcome**: Payment resolved manually, or the admin cancels the booking through the FR-006 Cancel Booking action with a mandatory reason; patient may be charged late fees or rescheduling fees, with amounts set in the FR-029 late-fee and rescheduling-fee settings; the late fee is charged when the late payment grace period (FR-029) has passed without payment
- **Boundary**: B1 covers installments after the first. A missed or failed later installment never causes `Payment Window Expired`, automatic booking cancellation, or inquiry cancellation (FR-006). Failure of the first installment at checkout is part of the first payment step and follows the FR-006 payment hold (see Edge Cases).

**B2: Patient Cancels Booking With Active Installment Plan**:

- **Trigger**: Patient requests booking cancellation before completing all installments
- **Steps**:
  1. Patient requests cancellation through Contact Support; after subquote acceptance the patient cannot cancel in the app (FR-006), and the request reaches the admin queue in FR-016
  2. System calculates paid installments to date and applicable refund per cancellation policy
  3. Admin reviews the request and cancels the booking through the FR-006 Cancel Booking action with a mandatory reason and audit entry; the refund amount follows the refund rules in FR-006 (Payment & Billing Rules: the refund ladder set in FR-029, or the provider-fault terms where the provider is at fault)
  4. System processes refund as a percentage of the amount paid so far, per the refund ladder owned by FR-029
  5. System cancels remaining scheduled installments
  6. System records the partial refund outcome on the instalment plan; booking status moves to `Cancelled` per FR-006
- **Outcome**: Patient refunded per policy; no further installments charged; provider notified

**B3: Procedure Date Changes After Installment Plan Established**:

- **Trigger**: Admin manually reschedules a confirmed booking due to emergency or exceptional circumstances (per FR-016 Admin Patient Management; patient self-service rescheduling remains deferred to V2 per FR-006 and system PRD)
- **Steps**:
  1. The admin date change, made through the FR-006 Change Appointment action and notified to the patient and provider through `booking.rescheduled`, triggers installment plan recalculation from the updated booking date; the plan total, currency and the accepted snapshot do not change
  2. System checks if new procedure date allows completion of remaining installments (30-day buffer)
  3. **If sufficient time**: System adjusts installment schedule dates to align with new procedure date
  4. **If insufficient time**: System sends the patient an insufficient-time notice that the remaining balance must be paid immediately or installment plan canceled
  5. The patient pays the remaining balance immediately, and the system sends reminders until it is paid; or the admin, in coordination with the patient, cancels the booking through the FR-006 Cancel Booking action
- **Outcome**: Installment plan adjusted to new schedule or remaining balance paid immediately; booking date updated

**B4: Provider Fault After Acceptance**:

- **Trigger**: Before treatment starts (booking `Accepted` or `Confirmed`), the provider withdraws the accepted quote, drops out, or is suspended or deactivated, and an admin transfers the patient to a replacement provider through FR-006 Alternative Flow B5 by authoring a replacement quote in the same inquiry. A provider fault during `Aftercare` reassigns only the aftercare provider (FR-011) and does not change the installment plan
- **Steps**:
  1. System cancels the remaining scheduled installments of the original booking
  2. When the provider withdraws, drops out, or is suspended or deactivated (FR-006 Alternative Flows B4 and B5), the patient is refunded in full every installment already paid and pays no cancellation fee, and the replacement booking takes a new payment
  3. Any installment plan for the replacement booking takes its total, currency and exchange rate from the replacement quote's acceptance snapshot, never from the original snapshot or a live quote
- **Outcome**: Patient continues with the replacement provider in the same inquiry. On a provider withdrawal, drop-out, suspension or deactivation every paid installment is refunded in full, no cancellation fee applies, and the replacement booking takes a new payment
- **Boundary**: Exact refund, fund-release and payment-allocation override mechanics are defined later in FR-007, FR-007B and FR-017

---

## Screen Specifications

### Patient Platform Screens

#### Screen 1: Patient Checkout - Installment Plan Selection

**Purpose**: Allow patient to select installment plan option at booking checkout

**Data Fields**:

| Field Name           | Type   | Required | Description                        | Validation Rules                                      | Graph field |
|---------------------|--------|----------|------------------------------------|-------------------------------------------------------|---|
| Total Amount         | number | Yes      | Booking total (accepted price after promotion) | Read-only; copied from the accepted snapshot through the FR-006 booking; already includes the accepted promotion and any patient promotion code; never recomputed | ENT-installment-plan.total_amount |
| Currency             | text   | Yes      | Accepted patient currency          | Read-only; copied with the exchange rate from the accepted snapshot; used for every installment | ENT-installment-plan.currency |
| Time Until Procedure | date   | Yes      | Days remaining until procedure     | At least 60 days (for minimum 2 installments + buffer) | ENT-installment-plan.days_until_procedure |
| Maximum Installments | number | Yes      | Calculated max installments available | 2-9; (days until procedure - 30) ÷ 30 + 1, rounded down (60 days gives 2) | ENT-installment-plan.max_installments |
| Selected Installments| select | Yes      | Patient's chosen number of installments | Must be ≤ maximum available | ENT-installment-plan.installment_count |
| Installment Amount   | number | Yes      | Amount per installment             | Total ÷ selected installments | ENT-installment-plan.installment_amount |
| Payment Schedule     | table  | Yes      | Dates and amounts for each installment | First installment is today; subsequent monthly | ENT-installment-payment.due_date, ENT-installment-payment.amount |
| Payment Method       | form   | Yes      | Card details for recurring charges | Valid payment method required | ENT-payment-method.token_reference |

**Business Rules**:

- Display clear explanation: "Final payment must complete 30 days before your procedure" (REQ-007B-035)
- Show maximum installments prominently with calculation explanation (REQ-007B-035)
- Allow patient to select any number from 2 to maximum available (REQ-007B-036)
- First installment charged at checkout when the patient confirms the plan; its success confirms the existing `Accepted` booking (FR-006) (REQ-007B-005)
- Show the total and every installment amount in the accepted currency (REQ-007B-025)
- A failed first installment can be retried, or another payment method used, only while the original FR-006 payment hold is active (FR-007 REQ-007-017); when the hold expires the booking moves to `Payment Window Expired` and installment checkout is blocked (REQ-007B-026, REQ-007B-052)
- Display full payment schedule with dates before patient confirms (REQ-007B-037)
- Show comparison: installment plan vs. full payment (REQ-007B-038)
- Disable installment option if procedure is less than 60 days away (REQ-007B-039)

**Notes**:

- Use visual payment timeline showing each installment date (REQ-007B-042)
- Highlight that installments are interest-free (REQ-007B-042)
- Show clear "Pay in Full" alternative option (REQ-007B-040)
- Provide calculator tool to experiment with different installment counts (REQ-007B-042)

---

#### Screen 2: Patient Booking Details - Installment Schedule View

**Purpose**: Allow patient to view installment payment schedule and history

**Data Fields**:

| Field Name            | Type   | Required | Description                           | Validation Rules                            | Graph field |
|----------------------|--------|----------|---------------------------------------|---------------------------------------------|---|
| Total Amount          | number | Yes      | Booking total (accepted price after promotion) | Matches booking total | ENT-installment-plan.total_amount |
| Currency              | text   | Yes      | Accepted patient currency             | Read-only; from the accepted snapshot; same for all installments | ENT-installment-plan.currency |
| Installments Paid     | number | Yes      | Count of completed installments       | 0 to total installments (REQ-007B-094) | ENT-installment-plan.installments_paid |
| Installments Remaining| number | Yes      | Count of upcoming installments        | Total minus paid (REQ-007B-094) | ENT-installment-plan.installments_remaining |
| Next Payment Date     | date   | Conditional | Date of next scheduled installment | Only if installments remaining > 0 (REQ-007B-094) | ENT-installment-plan.next_payment_date |
| Next Payment Amount   | number | Conditional | Amount of next installment         | Only if installments remaining > 0 (REQ-007B-094) | ENT-installment-plan.next_payment_amount |
| Payment History       | list   | Yes      | Past installment payments with dates and statuses | Read-only history | ENT-installment-payment.payment_date, ENT-installment-payment.status |
| Payment Method        | text   | Yes      | Last 4 digits of card on file         | Masked for security | ENT-payment-method.last_four_digits |
| Update Payment Method Button | button | Yes | "Update Payment Method" action button | Navigates to P03.1 Payment Methods Management screen; allows patient to update the default payment method used for remaining installment charges | no graph field (control) |

**Business Rules**:

- Show progress bar: installments completed / total installments (REQ-007B-044)
- Display countdown: "X days until next payment" (REQ-007B-044)
- Show reminder status: "Reminder sent" or "Reminder pending" (REQ-007B-044)
- Highlight overdue installments in red with "Payment Failed - Retry in Progress" (REQ-007B-045)
- Allow update of payment method with "Update Card" button (REQ-007B-021, REQ-007B-047)
- Show final payment deadline: "All payments complete by [date]" (REQ-007B-044)

**Notes**:

- Use visual timeline with checkmarks for completed installments (REQ-007B-044)
- Show clear status for each installment: Scheduled, Retrying, Paid, Failed, Overdue, Cancelled (REQ-007B-008, REQ-007B-044)
- Provide download option for payment receipts (REQ-007B-046)

---

### Provider Platform Screens

#### Screen 3: Provider Installment Plans Overview

**Purpose**: Allow provider to see all their bookings that use installment plans, with high-level status and risk indicators

**Data Fields**:

| Field Name               | Type   | Required | Description                                           | Validation Rules                          | Graph field |
|--------------------------|--------|----------|-------------------------------------------------------|-------------------------------------------|---|
| Booking ID               | text   | Yes      | Unique booking identifier                             | Clickable link to booking detail | ENT-booking.id |
| Patient Name             | text   | Yes      | Patient full name (revealed post-payment)            | Display only | ENT-patient.name |
| Procedure Date           | date   | Yes      | Scheduled procedure date                              | Format: DD-MM-YYYY | ENT-booking.appointment_at |
| Total Amount             | number | Yes      | Booking total (accepted price after promotion) | Matches booking total | ENT-installment-plan.total_amount |
| Installments Paid        | number | Yes      | Number of completed installments                      | 0 to total installments | ENT-installment-plan.installments_paid |
| Total Installments       | number | Yes      | Total installments in plan                            | 2–9 | ENT-installment-plan.installment_count |
| Completion Percentage    | number | Yes      | Percentage of total amount collected                  | 0–100% (auto-calculated) (REQ-007B-094) | ENT-installment-plan.completion_percentage |
| Next Payment Date        | date   | No       | Date of next scheduled installment (if any)           | Only if installments remaining > 0 | ENT-installment-plan.next_payment_date |
| Next Payment Amount      | number | No       | Amount of next installment (if any)                   | Only if installments remaining > 0 | ENT-installment-plan.next_payment_amount |
| Plan Status              | badge  | Yes      | "Active", "Canceled", "Completed", "Defaulted"; an Overdue flag is shown beside it when a due date has passed and the installment is unpaid (calculated, not stored) (REQ-007B-100) | Color-coded | ENT-installment-plan.status, ENT-installment-plan.is_overdue |
| Overdue Days             | number | No       | Days since first missed/failed installment            | Only for plans flagged Overdue or "Defaulted" (REQ-007B-095) | ENT-installment-plan.overdue_days |

**Business Rules**:

- List includes only bookings for the **current provider** that have an active or completed installment plan (no one-time payments). (REQ-007B-030)
- Providers see **status and progress only**; they cannot change payment schedules or retry charges (admin-only actions). (REQ-007B-029)
- Overdue and defaulted plans are visually emphasized (e.g., warning badges, sort to top). (REQ-007B-033)
- Clicking a row opens the shared **Booking Installment Plan Detail** screen for that booking. (REQ-007B-030)

**Notes**:

- Table should support filtering by plan status (Active, Canceled, Completed, Defaulted), the Overdue flag and procedure date range. (REQ-007B-033)
- Default sort: nearest upcoming procedure date, then highest risk (Overdue/Defaulted) at top. (REQ-007B-033)

---

#### Screen 4: Provider Booking Installment Plan Detail

**Purpose**: Provide the provider with a detailed, read-only view of a single booking’s installment plan, schedule, and payment history

**Data Fields**:

| Field Name                | Type   | Required | Description                                          | Validation Rules                          | Graph field |
|---------------------------|--------|----------|------------------------------------------------------|-------------------------------------------|---|
| Booking ID                | text   | Yes      | Unique booking identifier                            | Display only | ENT-booking.id |
| Patient Name              | text   | Yes      | Patient full name (revealed post-payment)           | Display only | ENT-patient.name |
| Provider Name             | text   | Yes      | Clinic/provider name                                 | Display only | ENT-provider.name |
| Procedure Date            | date   | Yes      | Scheduled procedure date                             | Format: DD-MM-YYYY | ENT-booking.appointment_at |
| Total Amount              | number | Yes      | Booking total (accepted price after promotion) | Matches booking total | ENT-installment-plan.total_amount |
| Currency                  | text   | Yes      | Accepted patient currency                            | Read-only; from the accepted snapshot | ENT-installment-plan.currency |
| Total Installments        | number | Yes      | Total installments in plan                           | 2–9 | ENT-installment-plan.installment_count |
| Installments Paid         | number | Yes      | Number of completed installments                     | 0 to total installments | ENT-installment-plan.installments_paid |
| Installments Remaining    | number | Yes      | Number of upcoming installments                      | Total minus paid | ENT-installment-plan.installments_remaining |
| Completion Percentage     | number | Yes      | Percentage of total amount collected                 | 0–100% (auto-calculated) | ENT-installment-plan.completion_percentage |
| Final Payment Deadline    | date   | Yes      | Date by which all installments must be completed     | Must meet configured cutoff rule | ENT-installment-plan.final_payment_deadline |
| Plan Status               | badge  | Yes      | "Active", "Canceled", "Completed", "Defaulted"; an Overdue flag is shown beside it when a due date has passed and the installment is unpaid (calculated, not stored) | Color-coded | ENT-installment-plan.status, ENT-installment-plan.is_overdue |
| Payment Method Summary    | text   | Yes      | Masked card details or payment method descriptor     | Display only | ENT-payment-method.last_four_digits |
| Installment Schedule      | table  | Yes      | Row per installment with date, amount, and status    | See sub-table below | ENT-installment-payment |

**Installment Schedule Sub-Table**:

| Field Name        | Type   | Required | Description                               | Validation Rules                | Graph field |
|-------------------|--------|----------|-------------------------------------------|---------------------------------|---|
| Installment #     | number | Yes      | Sequence number (1..N)                    | 1–9 | ENT-installment-payment.installment_number |
| Due Date          | date   | Yes      | Scheduled charge date                     | Format: DD-MM-YYYY | ENT-installment-payment.due_date |
| Amount            | number | Yes      | Installment amount                        | Must sum to Total Amount | ENT-installment-payment.amount |
| Status            | badge  | Yes      | "Scheduled", "Retrying", "Paid", "Failed", "Overdue", "Cancelled" | Color-coded | ENT-installment-payment.status |
| Paid Date         | date   | No       | Actual payment date (if paid)             | Present only for Paid | ENT-installment-payment.payment_date |
| Failure Reason    | text   | No       | Processor error message (if failed)       | Read-only | ENT-installment-payment.failure_reason |

**Business Rules**:

- View is **read-only**; providers can see schedule and history but **cannot** modify plan or trigger payments. (REQ-007B-029)
- If plan is flagged Overdue or is "Defaulted", show instruction banner: "Please contact Hairline support; payment follow-up is handled by admin team." (REQ-007B-031)
- All dates and amounts are consistent with underlying payment records; discrepancies must be treated as data errors and surfaced via internal alerts (out of scope for UI behavior here). (REQ-007B-034)

**Notes**:

- This screen is accessible from Provider Installment Plans Overview (provider tenant).
- Layout should reuse components from the patient’s installment schedule view where possible, with additional provider-specific context.

---

### Admin Platform Screens

#### Screen 5: Admin Installment Plan Management Dashboard

**Purpose**: Allow admin to monitor and manage all installment plans across platform

**Data Fields**:

| Field Name                | Type       | Required | Description                                     | Validation Rules          | Graph field |
|--------------------------|------------|----------|-------------------------------------------------|---------------------------|---|
| Active Plans Count        | number     | Yes      | Total installment plans currently active        | Non-negative integer | ENT-installment-plan-metrics.active_plans_count |
| Overdue Installments      | number     | Yes      | Count of failed installments after retries      | Flagged for admin action | ENT-installment-plan-metrics.overdue_installments_count |
| Total Installment Revenue | number     | Yes      | Sum of all installment payments collected       | Aggregate across all bookings | ENT-installment-plan-metrics.total_installment_revenue |
| Average Installments      | number     | Yes      | Average number of installments selected         | Analytics metric | ENT-installment-plan-metrics.average_installments |
| Success Rate              | percentage | Yes      | Successful installment charges / total attempts | Performance indicator | ENT-installment-plan-metrics.success_rate |
| Plan List                 | table      | Yes      | All installment plans with patient, provider, status, progress | Filter criteria are owned by FR-022 (Search and Filter) | ENT-patient.name, ENT-provider.name, ENT-installment-plan.status, ENT-installment-plan.completion_percentage |

**Business Rules**:

- Flag installment plans with overdue payments (after 3 failed retries) (REQ-007B-075)
- Show aging report: days overdue for failed installments (REQ-007B-076)
- Allow admin to manually retry failed installment (REQ-007B-080)
- Allow admin to contact patient for payment resolution (REQ-007B-051)
- Allow admin to cancel booking for chronically defaulted plans through the FR-006 Cancel Booking action (REQ-007B-051)
- Show revenue forecast based on scheduled installments (REQ-007B-077)

**Notes**:

- Use dashboard widgets for key metrics (REQ-007B-075)
- Provide drill-down into individual installment plan details (REQ-007B-075)
- Export capabilities for financial reporting and reconciliation (REQ-007B-078)

---

#### Screen 6: Admin Booking Installment Plan Detail

**Purpose**: Provide admin with a detailed, actionable view of a single booking’s installment plan, schedule, and payment history, including controls for resolving payment issues

**Data Fields**:

| Field Name                | Type   | Required | Description                                          | Validation Rules                          | Graph field |
|---------------------------|--------|----------|------------------------------------------------------|-------------------------------------------|---|
| Booking ID                | text   | Yes      | Unique booking identifier                            | Display only | ENT-booking.id |
| Patient Name              | text   | Yes      | Patient full name                                    | Display only | ENT-patient.name |
| Provider Name             | text   | Yes      | Clinic/provider name                                 | Display only | ENT-provider.name |
| Procedure Date            | date   | Yes      | Scheduled procedure date                             | Format: DD-MM-YYYY | ENT-booking.appointment_at |
| Total Amount              | number | Yes      | Booking total (accepted price after promotion) | Matches booking total | ENT-installment-plan.total_amount |
| Currency                  | text   | Yes      | Accepted patient currency                            | Read-only; from the accepted snapshot | ENT-installment-plan.currency |
| Total Installments        | number | Yes      | Total installments in plan                           | 2–9 | ENT-installment-plan.installment_count |
| Installments Paid         | number | Yes      | Number of completed installments                     | 0 to total installments | ENT-installment-plan.installments_paid |
| Installments Remaining    | number | Yes      | Number of upcoming installments                      | Total minus paid | ENT-installment-plan.installments_remaining |
| Completion Percentage     | number | Yes      | Percentage of total amount collected                 | 0–100% (auto-calculated) | ENT-installment-plan.completion_percentage |
| Final Payment Deadline    | date   | Yes      | Date by which all installments must be completed     | Must meet configured cutoff rule | ENT-installment-plan.final_payment_deadline |
| Plan Status               | badge  | Yes      | "Active", "Canceled", "Completed", "Defaulted"; an Overdue flag is shown beside it when a due date has passed and the installment is unpaid (calculated, not stored) | Color-coded | ENT-installment-plan.status, ENT-installment-plan.is_overdue |
| Payment Method Summary    | text   | Yes      | Masked card details or payment method descriptor     | Display only | ENT-payment-method.last_four_digits |
| Installment Schedule      | table  | Yes      | Row per installment with date, amount, and status    | Same structure as provider detail screen | ENT-installment-payment.installment_number, ENT-installment-payment.due_date, ENT-installment-payment.amount, ENT-installment-payment.status, ENT-installment-payment.payment_date, ENT-installment-payment.failure_reason |
| Admin Action Panel        | group  | Yes      | Section with admin-only controls and justification   | See Business Rules | no graph field (control) |

**Business Rules**:

- Admin can perform the following actions (subject to internal policy and audit logging):
  - **Retry Charge** on a failed installment (invokes payment processor via S-02). (REQ-007B-080)
  - **Mark as Resolved** when an external/manual payment issue has been handled. (REQ-007B-081)
  - See REQ-007B-023.
- All admin actions MUST:
  - Require a justification text input (minimum 20 characters). (REQ-007B-083)
  - Be logged with timestamp, admin ID, action type, and justification. (REQ-007B-083)
- Certain actions are only available based on plan status:
  - "Retry Charge" available only for "Failed" or "Overdue" installments. (REQ-007B-080)
- Admin cannot directly edit financial amounts; changes must be made via refunds/adjustments defined in payment rules. (REQ-007B-085)

**Notes**:

- This screen is accessible from the Admin Installment Plan Management Dashboard when an admin clicks into a specific plan.
- Layout should reuse the same base visual structure as the provider detail screen, with the additional Admin Action Panel.

---

## Business Rules

### General Module Rules

- Installment plans are interest-free (0% APR) for all patients (REQ-007B-001)
- See REQ-007B-001, REQ-007B-002.
- See REQ-007B-003.
- System offers only installment counts that are feasible given booking date, procedure date, monthly frequency, and the cutoff window (REQ-007B-002)
- See REQ-007B-005.
- Installment plan total, currency and exchange rate are copied read-only from the FR-005 accepted snapshot through the FR-006 booking. The total already includes the accepted promotion and any patient promotion code (FR-019). It is never recomputed from a live quote, sibling option, package library price or current exchange rate (REQ-007B-025)
- `Payment Window Expired` applies only to the first payment step (acceptance to first installment). Missed later installments never cause `Payment Window Expired` or inquiry cancellation (FR-006) (REQ-007B-026, REQ-007B-052)
- See REQ-007B-006.
- See REQ-007B-004.
- See REQ-007B-036.
- Single full payment option always available as alternative to installments (REQ-007B-040, REQ-007B-041)

### Data & Privacy Rules

- Payment method details stored securely per PCI-DSS standards (via payment processor) (REQ-007B-073)
- See REQ-007B-010.
- See REQ-007B-011.
- Access to installment payment data follows RBAC: patients see their own installments; providers see booking payment status; admins see all plans (REQ-007B-072)
- See REQ-007B-012.
- Compliance: PCI-DSS (via processor), GDPR/HIPAA-aligned handling of payment data (REQ-007B-073)

### Admin Editability Rules

**Editable by Admin**:

- Customer-facing installment plan settings are configured via **FR-029 (A-09)** (REQ-007B-079):
  - Enabled installment counts (2-9)
  - Cutoff days (30-90) requiring full payment completion before procedure date
  - Minimum booking amount eligibility threshold
  - Late payment grace period before booking cancellation; it also sets when a late fee is charged for an unpaid installment (REQ-007B-099)
  - Late fee and rescheduling fee amounts

**Fixed in Codebase (Not Editable)** (REQ-007B-074):

- Interest rate (always 0% - interest-free policy)
- Installment frequency (monthly; 30-day intervals)
- Core payment security controls and encryption standards
- Number of retry attempts for failed payments (3 attempts, only after a technical failure)
- Retry schedule for failed payments (waits of 1 day, 3 days, 7 days)
- Reminder timing (3 days before due date)
- Audit logging scope for payment events

**Configurable with Restrictions**:

- Cancellation refund ladder for installment plans (owned by FR-029, Payment settings) (REQ-007B-056)
- Payment processor integration settings (requires technical deployment, not runtime editable) (REQ-007B-074)

### Payment & Billing Rules

- Installment charges are automatic on scheduled dates (patient consent given at checkout) (REQ-007B-015, REQ-007B-043)
- See REQ-007B-018.
- See REQ-007B-019, REQ-007B-020.
- See REQ-007B-021, REQ-007B-047.
- See REQ-007B-022, REQ-007B-054.
- A late fee is charged when the late payment grace period (FR-029) has passed without payment; the amounts of the late fee and the rescheduling fee are set by the admin in FR-029 (REQ-007B-099, REQ-007B-050)
- Money movement follows the owner decisions that replace the missing Payment Routing Spec: Hairline is the seller on the card payment, and Hairline's balance pays refunds, chargebacks and Stripe fees first and recovers the clinic's part afterwards. Hairline holds the payment; the clinic's share moves to the clinic's locked Stripe balance 60 days before treatment (30 days for an installment plan once it is fully paid) and is paid out at release. If the booking is cancelled after the share has moved, Hairline refunds the patient per the refund ladder, pulls the share back from the clinic's locked balance and deducts any shortfall from the clinic's next payout. If the booking is rescheduled after the share has moved, Hairline always pulls it back and moves it again 60 or 30 days before the new date (REQ-007B-098)
- Platform commission calculated on the booking total (accepted price after promotion), using the commission type (Percentage or Flat Rate) and value from the snapshot taken at booking confirmation (FR-029), deducted from provider payout after final installment completes (REQ-007B-070)
- Provider payout delayed until all installments completed and the instalment plan is fully paid (REQ-007B-071, REQ-007B-049)
- See REQ-007B-024, REQ-007B-060, REQ-007B-061, REQ-007B-062.
- Installment charges must be idempotent (prevent duplicate charges on retry) (REQ-007B-068)
- Installment schedule and amounts are immutable once confirmed (prevent tampering) (REQ-007B-069)
- Cancellation refund policy applies same percentages to installment plans as to single payments (REQ-007B-055)
- For a provider-selected promotion or patient-entered code, the first successful installment consumes the promotion use reserved at acceptance (an automatic promotion's use is consumed at acceptance per FR-019); installments never apply or remove a promotion (REQ-007B-048)
- Installment revenue tracked separately from one-time payments
- Providers receive payout within 2 business days after final installment completes and procedure finishes
- Timezone handling critical for installment due dates (use UTC internally, display in patient timezone)
- Admins can identify and resolve defaulted installment plans within 24 hours of flag

### Admin Action & Audit Rules

Per Hairline Platform Constitution (Principle VI: Data Integrity & Audit Trail), all admin actions that modify installment plan state MUST be audited (REQ-007B-083):

**Admin Actions Requiring Justification & Audit Logging**:

- **Retry Charge**: Manually triggering a payment retry on a failed installment (requires justification minimum 20 characters; logged with timestamp, admin ID, action type, installment ID, retry attempt number) (REQ-007B-080, REQ-007B-084)
- **Mark as Resolved**: Marking a failed installment as resolved when external/manual payment has been handled (requires justification minimum 20 characters; logged with timestamp, admin ID, action type, installment ID, resolution method) (REQ-007B-081, REQ-007B-084)
- **Cancelling a booking with an installment plan** is not a plan action: the admin uses the FR-006 Cancel Booking action, which stops the remaining installments and applies the refund (REQ-007B-023, REQ-007B-053, REQ-007B-057, REQ-007B-058)

**Audit Trail Requirements**:

- All admin actions documented in Screen 6 (Admin Booking Installment Plan Detail) MUST be logged to the immutable audit trail system (S-06: Audit Log Service) (REQ-007B-086)
- Audit log retention follows the system PRD, Platform-Wide Rules: One 10-year retention period (REQ-007B-087)
- Audit logs MUST include: timestamp (UTC), admin user ID, admin name, action type, affected entity IDs (installment plan ID, booking ID, patient ID), justification text, before/after state (if applicable), IP address (REQ-007B-088)
- Failed admin action attempts (e.g., insufficient permissions, validation errors) MUST also be logged (REQ-007B-089)
- Audit logs MUST be tamper-proof and queryable for compliance reporting (REQ-007B-086)
- Admin access to installment management logged with user ID and timestamp (REQ-007B-086)

**Access Control**:

- Only authorized admin roles (Billing Admin, Financial Manager, Super Admin) can execute installment management actions (REQ-007B-090)
- Role-based access control (RBAC) enforced per FR-031 (Admin Access Control & Permissions) (REQ-007B-091)
- All installment data access (read and write) is subject to RBAC validation (REQ-007B-091)

**Carried from dropped sections (original wording)**:

- **Failure handling**: Queue failed jobs for retry; alert admin if scheduling system unavailable
- **Provenance**: resolves the AcceptanceEvent, accepted parent quote and subquote IDs and versions through its booking (FR-007 REQ-007-019)
- **Entity 3 - Payment Method**: The single record of a patient's saved payment method, used by installment plans here and read by the FR-007 payment screens and the FR-016 patient payments view. The payment methods it records are card and bank transfer. For a card it is a tokenized recurring payment method; for a bank transfer, which has no saved card, there is no card token, last 4 digits or expiration date to show
- **Ownership**: FR-007B owns installment plans and payment methods; the Stripe account and the split-payment setting belong to FR-029

---

## Dependencies

Related FRs: FR-006 (installment plan tied to booking confirmation and procedure date), FR-007 (core payment infrastructure for processing installment charges; uses same payment gateway, security controls, receipt generation; installments extend deposit/final payment logic), FR-019 (the accepted promotion and any patient promotion code are already in the plan total). Related modules: P-01 (only authenticated patients can enroll in installment plans), A-05 (admin oversight of installment plans and revenue reconciliation), S-03 (send installment reminders, confirmations, and failure notifications).

---

## User Scenarios & Testing

### User Story 1 - Select Installment Plan at Checkout (Priority: P1)

Patient selects installment plan during booking checkout, sees payment schedule, and confirms first installment to secure booking.

**Why this priority**: Core functionality enabling patients to access installment plans; critical for feature adoption and business value.

**Independent Test**: Create a booking with procedure date 6 months away; select 4 installment plan; confirm first payment; verify booking confirmed and remaining 3 installments scheduled.

**Acceptance Scenarios**:

1. **Given** a booking with procedure in 6 months (180 days), **When** patient views checkout, **Then** system displays installment options 2-6 (maximum 6 installments allowed per calculation)
2. **Given** patient selects 4 installment plan, **When** patient reviews payment schedule, **Then** system shows 4 equal installments with first charged today and remaining monthly
3. **Given** patient confirms installment plan, **When** first installment processes successfully, **Then** booking is confirmed and remaining 3 installments are scheduled at 30-day intervals
4. **Given** a parent quote with several options and date ranges where the patient accepted one subquote with a promotion, **When** patient views checkout, **Then** the plan total equals that subquote's accepted price after promotion and is not recalculated from the quote, sibling options or library prices
5. **Given** an active installment plan, **When** later installments are charged after exchange rates move, **Then** every installment is charged in the accepted currency at the accepted exchange rate and the total is unchanged
6. **Given** the first installment failed and the FR-006 payment hold has expired, **When** patient retries, **Then** the retry is rejected and the booking shows `Payment Window Expired`

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

System detects failed installment charge, notifies patient immediately, executes 3 retry attempts with increasing delays when the failure was technical, and flags plan as defaulted if all retries fail. After a hard decline there is no automatic retry; the patient must retry or update the card.

**Why this priority**: Critical error handling to recover from payment failures and protect revenue; prevents silent failures.

**Independent Test**: Simulate failed installment charge; verify immediate patient notification; verify 3 retry attempts execute on schedule (waits of 1 day, 3 days, 7 days) after a technical failure; verify a hard decline notifies the patient and triggers no automatic retry; verify admin notification if all retries fail.

**Acceptance Scenarios**:

1. **Given** scheduled installment charge fails, **When** failure detected, **Then** patient is notified immediately with clear error message and guidance
2. **Given** a technical failure and the first retry attempt is due (1 day later), **When** retry executes and fails, **Then** system schedules second retry after a wait of 3 days
3. **Given** all 3 retry attempts fail, **When** retries exhausted, **Then** system flags installment plan as "Defaulted" and notifies the admin (for intervention), the patient and the provider
4. **Given** a later installment is defaulted, **When** admin reviews it, **Then** the booking is not moved to `Payment Window Expired` and the inquiry is not cancelled
5. **Given** the charge was hard declined, **When** failure detected, **Then** the patient is notified and must retry or update the card, and no automatic retry is scheduled

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

Admin views dashboard showing defaulted installment plans (failed after 3 retries), reviews patient and booking details, contacts patient to resolve, and manually retries payment or cancels the booking through the FR-006 Cancel Booking action.

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

**Independent Test**: Create installment plan with 2 of 4 installments paid; patient requests cancellation 20 days before procedure; verify refund calculated as a percentage of the paid amount per the FR-029 refund ladder; verify remaining 2 installments canceled.

**Acceptance Scenarios**:

1. **Given** patient has paid 2 of 4 installments, **When** patient requests cancellation 20 days before procedure, **Then** system calculates refund as a percentage of the paid amount per the FR-029 refund ladder
2. **Given** refund calculated, **When** admin approves cancellation, **Then** refund is processed to patient's original payment method
3. **Given** cancellation confirmed, **When** system updates booking status, **Then** remaining 2 installments are canceled (not charged)

---

### Edge Cases

- What happens when patient's payment method expires mid-plan? (Charge is declined; no automatic retry; patient is notified and must retry or update the card) (REQ-007B-018)
- How does system handle procedure date rescheduled after installment plan established? (Recalculate installment schedule if sufficient time; otherwise require immediate payment of remaining balance) (REQ-007B-024, REQ-007B-061, REQ-007B-062)
- What occurs if first installment fails at checkout? (Booking stays `Accepted` and not confirmed; patient may retry or use a different payment method only while the original FR-006 payment hold is active, per FR-007 REQ-007-017; when the hold expires the booking moves to `Payment Window Expired`, installment checkout is blocked, and recovery follows FR-006) (REQ-007B-026, REQ-007B-052)
- What if a later installment is missed? (B1 retry and default handling applies, with automatic retries only after a technical failure; it never causes `Payment Window Expired` or inquiry cancellation) (REQ-007B-052, REQ-007B-018)
- What if the provider fails after acceptance? (Alternative Flow B4 and FR-006 Alternative Flow B5 apply) (REQ-007B-027, REQ-007B-063, REQ-007B-064, REQ-007B-096, REQ-007B-097)
- What if the quote, package or promotion is edited after acceptance? (No effect; the plan reads only the accepted snapshot)
- How to manage patient requesting fewer installments mid-plan? (Not supported; patient can pay remaining balance early to complete plan) (REQ-007B-066)
- What if admin increases the cutoff window from 30 to 45 days via FR-029? (Applies only to new bookings; existing installment plans unchanged) (REQ-007B-065)
- How does system handle refund for partial installments if patient disputes charge? (Admin reviews dispute; processes refund per resolution; may cancel booking or allow continuation) (REQ-007B-059)
- What if payment processor webhook fails to deliver charge status? (System polls payment status as fallback; ensures no missed confirmations or retries) (REQ-007B-067)

---

## Functional Requirements Summary

### Core Requirements

- **REQ-007B-001**: System MUST offer interest-free installment payment plans with 2-9 monthly payments
- **REQ-007B-002**: System MUST determine feasible installment options based on time until procedure, monthly frequency, and cutoff days configured in FR-029 (minimum 30 days); the maximum number of installments is (days until procedure - 30) ÷ 30 + 1, rounded down, so 60 days allows 2 installments; offered options are limited to enabled installment counts configured in FR-029 (2-9)
- **REQ-007B-003**: System MUST enforce the cutoff window: final installment must complete by the configured cutoff days before procedure date (minimum 30 days; configured in FR-029)
- **REQ-007B-004**: System MUST calculate installment amounts as equal shares: booking total (accepted price after promotion) ÷ number of installments, rounded to 2 decimal places
- **REQ-007B-005**: System MUST charge the first installment at checkout; its success confirms the existing `Accepted` booking (FR-006)
- **REQ-007B-006**: System MUST schedule remaining installments at 30-day intervals

### Data Requirements

- **REQ-007B-007**: System MUST maintain installment schedule with amounts and due dates per booking
- **REQ-007B-008**: System MUST track installment payment status as one list: scheduled, retrying, paid, failed, overdue, cancelled
- **REQ-007B-009**: System MUST persist patient payment method securely for recurring charges (tokenized)

### Security & Privacy Requirements

- **REQ-007B-010**: System MUST tokenize payment methods (never store full card numbers)
- **REQ-007B-011**: System MUST encrypt all installment payment records at rest and in transit
- **REQ-007B-012**: System MUST log every installment payment attempt and lifecycle event (scheduled, charged, failed, retried, refunded) with timestamp, amount, status, and user, in a tamper-evident audit trail

### Integration Requirements

- **REQ-007B-013**: System MUST integrate with payment processor for scheduled/recurring charges
- **REQ-007B-014**: System MUST send payment reminders 3 days before each installment due date
- **REQ-007B-015**: System MUST automatically charge payment method on installment due date
- **REQ-007B-016**: System MUST send confirmation notification after successful installment charge

### Error Handling Requirements

- **REQ-007B-017**: System MUST detect failed installment charges and notify patient immediately
- **REQ-007B-018**: System MUST execute 3 automatic retry attempts for an installment whose charge failed for a technical reason, with waits of 1 day, 3 days and 7 days (retries fall on day 1, day 4 and day 11 after the failure). After a hard decline System MUST NOT retry automatically; it MUST notify the patient, who must retry or update the card
- **REQ-007B-019**: System MUST flag installment plan as "Defaulted" after 3 failed retry attempts
- **REQ-007B-020**: System MUST notify the admin (for intervention), the patient and the provider of a defaulted installment plan

### Cancellation & Refund Requirements

- **REQ-007B-021**: System MUST allow the patient to update the payment method of an active installment plan at any time before the next installment is charged; the new method applies to the remaining installments only
- **REQ-007B-022**: System MUST calculate refunds for canceled bookings with partial installments paid as a percentage of the amount paid so far, per the cancellation refund ladder owned by FR-029
- **REQ-007B-023**: System MUST cancel remaining installments when booking is canceled; stopping the installments and the refund happen inside the FR-006 Cancel Booking action, and installment plans have no separate cancel action
- **REQ-007B-024**: System MUST handle procedure date rescheduling by recalculating installment schedule or requiring immediate payment; when the new date leaves too little time for the remaining installments, System MUST notify the patient (insufficient-time notice)

### Accepted Snapshot & Payment Window Requirements

- **REQ-007B-025**: System MUST copy the installment plan total, currency and exchange rate read-only from the FR-005 accepted snapshot through the FR-006 booking; the total already includes the accepted promotion and any patient promotion code; it MUST NOT be recomputed and MUST be shown with its currency on all installment screens
- **REQ-007B-026**: System MUST allow first-installment retries only within the original FR-006 payment hold; `Payment Window Expired` applies only to that first payment step, and missed later installments MUST NOT cause `Payment Window Expired` or inquiry cancellation
- **REQ-007B-027**: When the provider fails after acceptance, System MUST cancel remaining installments with no patient cancellation fee. On a provider withdrawal, drop-out, suspension or deactivation, System MUST refund in full every installment already paid, and the replacement booking takes a new payment per FR-006 Alternative Flows B4 and B5

---

## Appendix: Change Log

| Date       | Version | Changes                 | Author |
|------------|---------|-------------------------|--------|
| 2026-11-22 | 1.13 | Requirements graph programme baseline: PRD compressed to the checklist structure (each rule stated once, field rows tagged with graph field ids, dropped classes removed). No rule changes. Earlier history (v1.0 to v1.12) and the change request CR-FR007B-20261016-01 (change-request-2026-10-16-mtg002-quote-model-alignment.md) are in `archived/prd-baseline-2026-11-08/` and in git history. | Product Owner / Documentation |
| 2026-11-23 | 1.14 | Independent compression review: four clauses from the dropped Dependencies and Key Entities sections restored in original wording under Business Rules (scheduler failure handling, installment plan provenance, payment method record, FR-007B and FR-029 ownership). No rule changes. | Controller |

---

## Appendix: Approvals

| Role            | Name   | Date   | Signature/Approval |
|-----------------|--------|--------|--------------------|
| Product Owner   | Product Owner | 2026-10-18 | Approved v1.5 via MTG-002 decision log (documentation only) |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0
**Based on**: FR-007B from system-prd.md (Split Payment / Installment Plans)
**Last Updated**: 2026-11-22
