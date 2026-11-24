# FR-007B - Split Payment / Installment Plans

**Module**: P-03: Booking & Payment | S-02: Payment Processing Service
**Feature Branch**: `fr007b-payment-installments`
**Created**: 2025-11-10
**Status**: 🟡 Revised — Pending Consolidated Verification
**Source**: FR-007B from local-docs/project-requirements/system-prd.md (Split Payment / Installment Plans) + Constitution (local-docs/project-requirements/constitution.md)

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
- Receive reminders before each scheduled installment at the times set in the FR-007 payment reminder setting (REQ-007B-014)
- View installment payment history and upcoming payments
- Update payment method for installments if needed
- Receive notifications of successful/failed installment payments

**Provider Platform (PR-05)**:

- View booking payment status: installment plan active, number of installments, completion percentage
- See payment progress: which installments have been paid, which are upcoming
- See an Overdue banner on the plan detail screen, and be notified when a plan is Defaulted (REQ-007B-031, REQ-007B-032)
- Access payment history for installment-based bookings

**Admin Platform (A-05)**:

- View installment plan configuration (managed in FR-029) and link to configuration screen for authorized users (REQ-007B-079)
- Monitor all active installment plans across the platform
- View installment payment success/failure rates
- Handle defaulted installment plans (failed payments after retries, or a hard decline unpaid on day 11) with Retry Charge or Mark as Resolved (REQ-007B-080, REQ-007B-081)
- Review cancelled bookings with partial installment payments; FR-006 and FR-007 compute and approve the refund (REQ-007B-022)
- Generate reports on installment plan usage and performance (REQ-007B-075)
- View aging reports for overdue installments

**Shared Services (S-02, S-03)**:

- S-02: Processes scheduled installment charges on due dates; executes retry logic for failed payments (3 attempts, only after a retryable failure); calculates available installments based on procedure date
- S-03: Sends reminders at the times set in the FR-007 payment reminder setting; sends payment confirmations, failure notifications and the overdue notice; alerts admins of payment issues

### Communication Structure

**In Scope**:

- Email/push notifications for installment payment reminders at the times set in the FR-007 payment reminder setting (REQ-007B-014, REQ-007B-092)
- Payment confirmation notifications to the patient for successful installment charges (REQ-007B-016)
- Payment failure notifications for declined/failed installments
- Overdue notice: one notice to the patient and one to the billing admins on the day after a due date passes unpaid (REQ-007B-101)
- Notification of the admin, the patient and the provider when a plan is Defaulted (REQ-007B-020); while an installment is only Overdue the provider sees the banner on the plan detail screen (REQ-007B-032)
- Booking status change notification to the patient when the final installment completes (REQ-007B-093)

**Out of Scope**:

- SMS notifications (handled by S-03 channel configuration; **no SMS installment notifications are available in MVP and this channel is a future enhancement**) (REQ-007B-092)
- Chat/messaging between patient and provider about payment terms (REQ-007B-092)
- Marketing content about installment plans (REQ-007B-092)

### Entry Points

- Patient has accepted a quote (FR-005) and reaches the **Payment Options** step in the booking & payment flow (FR-006/FR-007), which offers pay in full, deposit and balance, or installments, then selects **"Pay in Installments"**, which hands off to FR-007B Screen 1; FR-007B governs the installment option only (REQ-007B-028)
- Patient views installment schedule from booking details screen (REQ-007B-028)
- Admin accesses installment management from billing/financial management module (REQ-007B-028)
- Provider views installment status from booking overview screen (REQ-007B-028)

---

## Business Workflows

### Main Flow: Patient Selects Installment Plan and Completes Payments

**Actors**: Patient, System (Payment Processing Service), Admin
**Upstream Context**: Subquote has been accepted (FR-005) and booking details are available via FR-006: the procedure date, and the plan total, currency and exchange rate copied read-only from the FR-005 accepted snapshot through the booking; FR-007 has presented a **Payment Options** step where the patient chose **"Pay in Installments"** instead of paying in full or deposit and balance.
**Trigger**: Patient confirms the choice to **"Pay in Installments"** on the Payment Options step and proceeds to the Installment Plan selection screen (Screen 1 in this FR)
**Outcome**: Booking confirmed with installment plan; scheduled installments charged automatically; booking paid in full, normally by the configured cutoff date (minimum 30 days before procedure, configured via FR-029); retries and the grace period can run past it (REQ-007B-107)

**Steps**:

1. Patient reviews booking summary with the booking total (accepted price after promotion) in the accepted currency and sees that **"Pay in Installments"** is selected as the payment option
2. System checks eligibility (installments enabled in FR-029, the booking total at or above the FR-029 minimum converted at the locked rate, and days until the procedure at least the cutoff days plus 30; with fewer days only pay in full is offered) and calculates feasible installment options from the cutoff days (minimum 30 days before procedure, configured via FR-029) with monthly installments; only the counts enabled in FR-029 up to the maximum are offered, and when none fits only pay in full is offered (REQ-007B-002, REQ-007B-106)
3. System displays the installment options: the enabled counts up to the maximum (e.g., "Pay in 2-6 installments" if procedure is in 6 months and every count is enabled)
4. Patient selects desired installment plan (e.g., 4 monthly installments)
5. System calculates installment amount (total ÷ number of installments, rounded down; the last installment is the total minus the others, so the amounts sum to the total) and displays payment schedule with dates (REQ-007B-004)
6. Patient confirms installment plan selection and provides a card; installments need a saved card and the first installment uses it, so a bank transfer cannot pay an installment plan (REQ-007B-009)
7. System charges the first installment at checkout; its success confirms the existing `Accepted` booking (FR-006) and consumes any promotion use reserved at acceptance (FR-019)
8. System schedules remaining installments on monthly intervals
9. System records the booking as `Confirmed` (FR-006) with installment plan status active
10. System sends reminders to the patient at the times set in the FR-007 payment reminder setting (up to 3, default 3 days before and on the due date), unless the booking carries the support-required marker (REQ-007B-014, REQ-007B-103)
11. On the due date, System automatically charges the card, unless the support-required marker is on (REQ-007B-103)
12. On successful charge, System updates installment status and sends confirmation
13. System repeats steps 10-12 for each remaining installment
14. When the final installment is paid (normally by the cutoff date), System marks the installment plan as completed (shown as "Fully Paid"); the booking status continues to follow FR-006. The booking's Payment Status becomes Full paid at that moment (FR-007 REQ-007-099), the fully-paid event FR-018 reads (REQ-018-309).

### Alternative Flows

**A1: Patient Chooses Fewer Installments Than Maximum Available**:

- **Trigger**: Patient wants to pay faster than the maximum allowed installments
- **Steps**:
  1. Patient selects fewer installments (e.g., 3 installments when 6 are available)
  2. System calculates higher installment amount with same total
  3. System adjusts payment schedule accordingly
- **Outcome**: Booking completed with shorter payment timeline; same cutoff window maintained

**A2: Patient Chooses Another Payment Option Instead of Installments (Handled by FR-007)**:

- **Trigger**: On the Payment Options step (FR-007), patient selects **"Pay in Full"** or deposit and balance instead of **"Pay in Installments"**
- **Steps** (owned by FR-007, summarized here for branching clarity):
  1. System routes patient to the full-payment or deposit-and-balance checkout flow defined in FR-007
  2. System processes the payment as FR-007 defines
  3. System records the payment per FR-007; booking status follows FR-006
- **Outcome**: Booking confirmed without installment plan; **FR-007B is not invoked** in this path

**A3: Patient Updates Payment Method Mid-Plan**:

- **Trigger**: Patient's payment method expired or needs to change card
- **Steps**:
  1. Patient navigates to booking details and selects "Update Payment Method", which opens payment method management (FR-001 REQ-001-151)
  2. Patient provides new card details
  3. System validates and saves new payment method
  4. System applies new payment method to remaining installments
  5. When an installment is Failed or Overdue, System offers to charge it with the new card (the patient can also use Pay now on Screen 2); neither happens while the booking carries the support-required marker (REQ-007B-021, REQ-007B-103)
- **Outcome**: Future installments charged to new payment method, and a Failed or Overdue installment offered for charge; previous installments unaffected

**B1: Installment Payment Fails or Is Missed**:

- **Trigger**: Scheduled installment charge is declined or fails
- **Steps**:
  1. System detects payment failure and logs the failure reason
  2. System immediately notifies patient of failed payment with clear error message
  3. On the day after the due date the day's retry, if one is due, runs first; if the installment is still unpaid, System shows it Overdue, sends the patient one overdue notice, which replaces that day's failure notice and states the date on which the booking will be cancelled when the cancellation point is set, and notifies the billing admins once; the provider sees the Overdue banner only (REQ-007B-100, REQ-007B-101)
  4. If the failure is retryable (any failure except a hard decline, so a technical fault or insufficient funds), System schedules first retry attempt after a wait of 1 day
  5. If retry fails, System waits 3 days and attempts second retry
  6. If second retry fails, System waits 7 days and attempts third retry
  7. If all 3 retries fail, System flags installment plan as "Defaulted"
  8. System notifies the admin, the patient and the provider of the defaulted plan and overdue booking
  9. Admin reviews and contacts patient to resolve payment issue, with Retry Charge or Mark as Resolved; the admin cancels through the FR-006 Cancel Booking action only while the booking is `Accepted`, `Payment Window Expired` or `Confirmed`. After treatment has started a Defaulted plan is resolved by payment only (REQ-007B-104)
  10. When the Unpaid Balance Cancellation Point saved on the plan is set (the booking was confirmed after FR-029 set it), System hands the Confirmed booking to FR-006 Alternative Flow B8 (cause UnpaidBalance) that many days after the due date of the first missed installment, whatever the retry, grace period or Defaulted state; pending retries and the grace period end with the plan. While the point is unset nothing cancels automatically. It covers any unpaid balance. While the booking carries the support-required marker the count pauses and nothing is handed over (REQ-007B-102, REQ-007B-103)
- **Hard decline**: A hard decline is a refusal because the card is expired, lost, stolen, invalid or flagged for fraud; insufficient funds is not a hard decline. After a hard decline System does not retry automatically, and a hard decline on a retry cancels the retries still pending; the patient is notified and must use Pay now on Screen 2 or update the card, which re-offers the charge. If the installment is still unpaid on day 11 after its due date, the plan is flagged Defaulted (REQ-007B-018, REQ-007B-019, REQ-007B-021)
- **Late fee**: The late fee is added once to the installment when the late payment grace period saved on the plan, counted from the due date, passes unpaid and no automatic retry is pending (the fee waits until the retries end); it is collected with the next successful charge, never as a separate charge, and the refund base excludes it. The amount is set in FR-029 and saved on the plan at confirmation; its currency, base and treatment are in REQ-007B-110 (REQ-007B-099, REQ-007B-110)
- **Pending provider fault**: While the booking carries the support-required marker (FR-006 REQ-006-081), System does not charge, retry, remind, flag Overdue or Defaulted, add a late fee or hand the booking to FR-006 Alternative Flow B8, and the retry, grace and cancellation-point clocks pause, not reset. If a replacement is accepted, the replacement plan recalculates all dates (B4); otherwise charges resume at the FR-006 Screen 10 submit (REQ-007B-103)
- **Defaulted plan**: Later installments are paused: they keep their dates and amounts, are not Overdue and get no overdue notice, reminder or late fee. The plan returns to Active when no installment is Failed or Overdue, whoever paid (REQ-007B-108), and each paused installment whose due date has passed is then charged once at the next daily run, before any Overdue flag or notice that day, with the normal failure handling (REQ-007B-105, REQ-007B-108)
- **Outcome**: Payment resolved by the patient or manually, or the admin cancels the booking where its state allows it; no rescheduling fee applies in V1 (REQ-007B-050)
- **Boundary**: B1 covers installments after the first. A missed or failed later installment never causes `Payment Window Expired` or inquiry cancellation (FR-006); it cancels the booking only at the cancellation point of step 10. Failure of the first installment at checkout is part of the first payment step and follows the FR-006 payment hold (see Edge Cases).

**B2: Patient Cancels Booking With Active Installment Plan**:

- **Trigger**: Patient requests booking cancellation before completing all installments
- **Steps**:
  1. Patient requests cancellation through Contact Support; after subquote acceptance the patient cannot cancel in the app (FR-006), and the request reaches the admin queue in FR-016
  2. System shows the admin the amount paid so far, excluding late fees, and the unpaid installments (REQ-007B-022)
  3. Admin reviews the request and cancels the booking through the FR-006 Cancel Booking action with a mandatory reason and audit entry, only while the booking is `Accepted`, `Payment Window Expired` or `Confirmed` (`In Progress` only through the FR-006 provider-fault route)
  4. System voids the remaining unpaid installments before the refund is computed: it waits for any charge already in flight, cancels the unpaid installments and sets the plan `Cancelled`; a charge that still succeeds is added to the refund base (REQ-007B-023)
  5. FR-006 and FR-007 compute the refund as a percentage of the paid amount per the refund ladder in FR-029 (or the provider-fault terms) and start it; a refund that needs approval follows FR-007 REQ-007-015: another admin who holds the Issue Refunds permission (FR-031), escalating to a super-admin, never self-approved. System records the refund outcome on the installment plan once FR-007 has started the refund; booking status moves to `Cancelled` per FR-006 (REQ-007B-057)
  6. System notifies the provider that the booking with an active plan was cancelled (REQ-007B-058)
- **Outcome**: Patient refunded per policy; no further installments charged; provider notified

**B3: Procedure Date Changes After Installment Plan Established**:

- **Trigger**: Admin manually reschedules a confirmed booking due to emergency or exceptional circumstances (per FR-016 Admin Patient Management; patient self-service rescheduling remains deferred to V2 per FR-006 and system PRD)
- **Steps**:
  1. The admin date change, made through the FR-006 Change Appointment action and notified to the patient and provider through `booking.rescheduled`, triggers an installment plan check against the updated booking date; the plan total, currency and the accepted snapshot do not change
  2. System checks that every remaining installment, on its existing due date, still falls at least the cutoff days (the cutoff saved on the plan) before the new date (REQ-007B-061)
  3. **If every remaining installment fits**: the due dates, count and amounts stay as they were; System recalculates only the Final Payment Deadline from the new date and returns the schedule to FR-006 Screen 8 read-only
  4. **If no feasible plan**: System returns no feasible plan and FR-006 blocks the change (FR-006 REQ-006-017); the booking date and the plan stay as they were and no notice is sent (REQ-007B-062)
  5. The admin may cancel the booking through the FR-006 Cancel Booking action instead
- **Outcome**: Booking date updated with the plan's due dates unchanged and the Final Payment Deadline recalculated, or the change blocked with nothing changed; no rescheduling fee applies to an admin date change in V1 (REQ-007B-050)

**B4: Provider Fault After Acceptance**:

- **Trigger**: Before treatment starts (booking `Accepted` or `Confirmed`), the provider withdraws the accepted quote, drops out, or is suspended or deactivated, and an admin transfers the patient to a replacement provider through FR-006 Alternative Flow B5 by authoring a replacement quote in the same inquiry. A provider fault during `Aftercare` reassigns only the aftercare provider (FR-011) and does not change the installment plan
- **Steps**:
  1. System voids the remaining unpaid installments of the booking as in B2 step 4 (waits for any charge in flight, sets the plan `Cancelled`, adds a charge that still succeeds to the refund base); this step is common to the provider-fault cancellation, the admin cancellation (B2) and the unpaid-balance cancellation (FR-006 Alternative Flow B8)
  2. Only when the provider withdraws, drops out, or is suspended or deactivated (FR-006 Alternative Flows B4 and B5), the patient is refunded in full every installment already paid and any late fee already collected, and pays no cancellation fee, and the replacement booking takes a new payment. The unpaid-balance cancellation does not take this branch: it follows the refund ladder in FR-006 (REQ-007B-027)
  3. Any installment plan for the replacement booking takes its total, currency and exchange rate from the replacement quote's acceptance snapshot, never from the original snapshot or a live quote
- **Outcome**: Patient continues with the replacement provider in the same inquiry. On a provider withdrawal, drop-out, suspension or deactivation every paid installment and any collected late fee is refunded in full, no cancellation fee applies, and the replacement booking takes a new payment
- **Boundary**: Refund, fund-release and payment-allocation mechanics are owned by FR-007 and FR-017 (REQ-007B-096)

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
| Time Until Procedure | number | Yes      | Days remaining until procedure     | At least the cutoff days plus 30 (so 2 installments fit with the final one by the cutoff) | ENT-installment-plan.days_until_procedure |
| Maximum Installments | number | Yes      | Calculated max installments available | 2-9; (days until procedure - cutoff days) ÷ 30, rounded down, plus 1 (60 days with a 30-day cutoff gives 2) | ENT-installment-plan.max_installments |
| Selected Installments| select | Yes      | Patient's chosen number of installments | One of the counts enabled in FR-029 that is ≤ the maximum available | ENT-installment-plan.installment_count |
| Installment Amount   | number | Yes      | Amount per installment             | Total ÷ selected installments, rounded down; the last installment is the total minus the others | ENT-installment-plan.installment_amount |
| Payment Schedule     | table  | Yes      | Dates and amounts for each installment | First installment is today; subsequent monthly | ENT-installment-payment.due_date, ENT-installment-payment.amount |
| Late Fee             | text   | No       | Fee added to an installment that stays unpaid after the grace period | Read-only; the FR-029 value in force at confirmation (fixed amount, or percentage of the late installment amount), saved on the plan (REQ-007B-111) | ENT-installment-plan.late_fee_setting |
| Grace Period         | number | No       | Days after a due date before the late fee is added | Read-only; the FR-029 value in force at confirmation, saved on the plan (REQ-007B-111) | ENT-installment-plan.grace_period_days |
| Cancellation Point   | number | No       | Days after the first missed due date at which an unpaid balance cancels the booking | Shown only when set in FR-029; read-only; saved on the plan at confirmation (REQ-007B-111) | ENT-installment-plan.cancellation_point_days |
| Payment Method       | form   | Yes      | Card details for recurring charges | Valid card required; a bank transfer cannot pay installments | ENT-payment-method.token_reference |

**Business Rules**:

- Display clear explanation: "Final payment must complete [cutoff days] days before your procedure" (REQ-007B-035)
- Show maximum installments prominently with calculation explanation (REQ-007B-035)
- Allow patient to select any enabled count (FR-029) from 2 to the maximum available (REQ-007B-036)
- First installment charged at checkout when the patient confirms the plan; its success confirms the existing `Accepted` booking (FR-006) (REQ-007B-005)
- Show the total and every installment amount in the accepted currency (REQ-007B-025)
- A failed first installment can be retried, or another payment method used, only while the original FR-006 payment hold is active (FR-007 REQ-007-017); when the hold expires the booking moves to `Payment Window Expired` and installment checkout is blocked (REQ-007B-026, REQ-007B-052)
- Display full payment schedule with dates before patient confirms (REQ-007B-037)
- Show comparison: installment plan vs. full payment (REQ-007B-038)
- Show the late fee, the grace period and, when the cancellation point is set, that an unpaid balance cancels the booking that many days after the first missed due date, before the patient confirms; the plan keeps these values as they were at confirmation (REQ-007B-111)
- Offer the installment option only when installments are enabled, the booking total is at or above the FR-029 minimum (converted at the locked rate) and the days until the procedure are at least the cutoff days plus 30 and at least one enabled count is within the maximum; otherwise the installment option is not shown and only pay in full is offered (REQ-007B-039, REQ-007B-106)

**Notes**:

- Use visual payment timeline showing each installment date (REQ-007B-042)
- Highlight that installments are interest-free (REQ-007B-042)
- Show the other payment options FR-007 offers (pay in full, deposit and balance) as alternatives (REQ-007B-040)
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
| Update Payment Method Button | button | Yes | "Update Payment Method" action button | Opens payment method management from the FR-001 menu (FR-001 REQ-001-151); allows patient to update the default card used for remaining installment charges | no graph field (control) |
| Pay Now Button | button | Conditional | "Pay now" action on a Failed or Overdue installment, or on the next scheduled installment | Charges the installment at once with the card on file; on an Active plan it can also pay the next scheduled installment, or all remaining installments, in due-date order, and the due dates of unpaid ones do not change (REQ-007B-112); hidden while the booking carries the support-required marker (REQ-007B-021, REQ-007B-103) | no graph field (control) |
| Overdue Flag | badge | No | Marks an unpaid installment from the day after its due date | Calculated, not stored (REQ-007B-100) | ENT-installment-payment.is_overdue |
| Late Fee | number | No | Late fee added to an installment | Shown once the grace period passes unpaid; collected with the next successful charge (REQ-007B-099, REQ-007B-110) | ENT-installment-payment.late_fee_amount |

**Business Rules**:

- Show progress bar: installments completed / total installments (REQ-007B-044)
- Display countdown: "X days until next payment" (REQ-007B-044)
- Show reminder status: "Reminder sent" or "Reminder pending" (REQ-007B-044)
- Highlight Overdue installments in red with the label "Overdue"; a separate "Retry scheduled" tag shows while an automatic retry is pending (REQ-007B-045)
- Allow update of payment method with "Update Card" button (REQ-007B-021, REQ-007B-047)
- Show final payment deadline: "All payments complete by [date]" (REQ-007B-044)

**Notes**:

- Use visual timeline with checkmarks for completed installments (REQ-007B-044)
- Show clear status for each installment: Scheduled, Retrying, Paid, Failed, Cancelled, with an Overdue flag beside it (REQ-007B-008, REQ-007B-044)
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
| Plan Status              | badge  | Yes      | "Active", "Cancelled", "Completed", "Defaulted"; an Overdue flag is shown beside it when a due date has passed and the installment is unpaid (calculated, not stored) (REQ-007B-100) | Color-coded | ENT-installment-plan.status, ENT-installment-plan.is_overdue |
| Overdue Days             | number | No       | Days since first missed/failed installment            | Only for plans flagged Overdue or "Defaulted" (REQ-007B-095) | ENT-installment-plan.overdue_days |

**Business Rules**:

- List includes only bookings for the **current provider** that have an installment plan of any status (no one-time payments). (REQ-007B-030)
- Providers see **status and progress only**; they cannot change payment schedules or retry charges (admin-only actions). (REQ-007B-029)
- Overdue and defaulted plans are visually emphasized (e.g., warning badges, sort to top). (REQ-007B-033)
- Clicking a row opens the shared **Booking Installment Plan Detail** screen for that booking. (REQ-007B-030)

**Notes**:

- Table should support filtering by plan status (Active, Cancelled, Completed, Defaulted), the Overdue flag and procedure date range. (REQ-007B-033)
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
| Plan Status               | badge  | Yes      | "Active", "Cancelled", "Completed", "Defaulted"; an Overdue flag is shown beside it when a due date has passed and the installment is unpaid (calculated, not stored) | Color-coded | ENT-installment-plan.status, ENT-installment-plan.is_overdue |
| Payment Method Summary    | text   | Yes      | Masked card details or payment method descriptor     | Display only | ENT-payment-method.last_four_digits |
| Installment Schedule      | table  | Yes      | Row per installment with date, amount, and status    | See sub-table below | ENT-installment-payment |

**Installment Schedule Sub-Table**:

| Field Name        | Type   | Required | Description                               | Validation Rules                | Graph field |
|-------------------|--------|----------|-------------------------------------------|---------------------------------|---|
| Installment #     | number | Yes      | Sequence number (1..N)                    | 1–9 | ENT-installment-payment.installment_number |
| Due Date          | date   | Yes      | Scheduled charge date                     | Format: DD-MM-YYYY | ENT-installment-payment.due_date |
| Amount            | number | Yes      | Installment amount                        | Must sum to Total Amount | ENT-installment-payment.amount |
| Status            | badge  | Yes      | "Scheduled", "Retrying", "Paid", "Failed", "Cancelled" | Color-coded | ENT-installment-payment.status |
| Overdue Flag      | badge  | No       | Shown beside the status from the day after the due date while unpaid | Calculated, not stored (REQ-007B-100) | ENT-installment-payment.is_overdue |
| Paid Date         | date   | No       | Actual payment date (if paid)             | Present only for Paid | ENT-installment-payment.payment_date |
| Failure Reason    | text   | No       | Processor error message (if failed)       | Read-only | ENT-installment-payment.failure_reason |

**Business Rules**:

- View is **read-only**; providers can see schedule and history but **cannot** modify plan or trigger payments. (REQ-007B-029)
- If an installment is Overdue or the plan is "Defaulted", show instruction banner: "Please contact Hairline support; payment follow-up is handled by admin team." (REQ-007B-031)
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
| Overdue Installments      | number     | Yes      | Count of installments flagged Overdue, including those with an automatic retry pending | Flagged for admin action | ENT-installment-plan-metrics.overdue_installments_count |
| Defaulted Plans           | number     | Yes      | Count of plans flagged Defaulted                | Flagged for admin action | ENT-installment-plan-metrics.defaulted_plans_count |
| Total Installment Revenue | number     | Yes      | Sum of all installment payments collected       | Aggregate across all bookings | ENT-installment-plan-metrics.total_installment_revenue |
| Average Installments      | number     | Yes      | Average number of installments selected         | Analytics metric | ENT-installment-plan-metrics.average_installments |
| Success Rate              | percentage | Yes      | Successful installment charges / total attempts | Performance indicator | ENT-installment-plan-metrics.success_rate |
| Plan List                 | table      | Yes      | All installment plans with patient, provider, status, progress | Filter criteria are owned by FR-022 (Search and Filter) | ENT-patient.name, ENT-provider.name, ENT-installment-plan.status, ENT-installment-plan.completion_percentage |

**Business Rules**:

- Flag Overdue installments, and plans that are Defaulted (after 3 failed retries, or a hard decline unpaid on day 11) (REQ-007B-075, REQ-007B-019)
- Show aging report: days overdue for Overdue installments (REQ-007B-076)
- Allow admin to manually retry a Failed or Overdue installment (REQ-007B-080)
- Allow admin to contact patient for payment resolution (REQ-007B-051)
- Allow admin to cancel booking for chronically defaulted plans through the FR-006 Cancel Booking action, only while the booking is `Accepted`, `Payment Window Expired` or `Confirmed` (REQ-007B-051, REQ-007B-104)
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
| Plan Status               | badge  | Yes      | "Active", "Cancelled", "Completed", "Defaulted"; an Overdue flag is shown beside it when a due date has passed and the installment is unpaid (calculated, not stored) | Color-coded | ENT-installment-plan.status, ENT-installment-plan.is_overdue |
| Payment Method Summary    | text   | Yes      | Masked card details or payment method descriptor     | Display only | ENT-payment-method.last_four_digits |
| Installment Schedule      | table  | Yes      | Row per installment with date, amount, status, Overdue flag, late fee and payment source (automatic or manual) | Same structure as provider detail screen, plus the late fee and the payment source | ENT-installment-payment.installment_number, ENT-installment-payment.due_date, ENT-installment-payment.amount, ENT-installment-payment.status, ENT-installment-payment.is_overdue, ENT-installment-payment.late_fee_amount, ENT-installment-payment.payment_source, ENT-installment-payment.payment_date, ENT-installment-payment.failure_reason |
| Admin Action Panel        | group  | Yes      | Section with admin-only controls and justification   | See Business Rules | no graph field (control) |

**Business Rules**:

- Admin can perform the following actions (subject to internal policy and audit logging):
  - **Retry Charge** on a Failed or Overdue installment (invokes payment processor via S-02). It does not count toward the 3 automatic retries; on success the installment is Paid and the plan follows REQ-007B-108, on failure it returns to Failed and the plan is unchanged. (REQ-007B-080, REQ-007B-108)
  - **Mark as Resolved** only for a bank transfer into Hairline's account: the admin enters the amount, date, receiving account and reference, and a second admin who holds the Resolve Installments permission (FR-031) approves it, never the same admin. On approval the system sets the installment Paid with payment source manual and passes the payment to FR-007, which owns the manual payment record, the refund of a manual payment and the clinic-share movement for it. The plan then follows REQ-007B-108. (REQ-007B-081, REQ-007B-109)
- All admin actions MUST:
  - Require a justification text input (minimum 20 characters). (REQ-007B-083)
  - Be logged with timestamp, admin ID, action type, and justification. (REQ-007B-083)
- Certain actions are only available based on plan status:
  - "Retry Charge" available only for "Failed" or "Overdue" installments. (REQ-007B-080)
- While a plan is Defaulted its later installments are paused and carry no Overdue flag, notice, reminder or late fee; the plan returns to Active as REQ-007B-108 sets, whoever pays. (REQ-007B-105, REQ-007B-108)
- After treatment has started a Defaulted plan is resolved by payment only; there is no cancel route. (REQ-007B-104)
- Admin cannot directly edit financial amounts; changes must be made via refunds/adjustments defined in payment rules. (REQ-007B-085)

**Notes**:

- This screen is accessible from the Admin Installment Plan Management Dashboard when an admin clicks into a specific plan.
- Layout should reuse the same base visual structure as the provider detail screen, with the additional Admin Action Panel.

---

## Business Rules

### General Module Rules

- Installment plans are interest-free (0% APR) for all patients (REQ-007B-001)
- The final installment must complete by the configured cutoff days before the procedure date (minimum 30 days; configured in FR-029) (REQ-007B-003)
- System offers only installment counts that are feasible given booking date, procedure date, monthly frequency, and the cutoff window (REQ-007B-002)
- The first installment is charged at checkout; its success confirms the existing `Accepted` booking (FR-006) (REQ-007B-005)
- Installment plan total, currency and exchange rate are copied read-only from the FR-005 accepted snapshot through the FR-006 booking. The total already includes the accepted promotion and any patient promotion code (FR-019). It is never recomputed from a live quote, sibling option, package library price or current exchange rate (REQ-007B-025)
- `Payment Window Expired` applies only to the first payment step (acceptance to first installment). Missed later installments never cause `Payment Window Expired` or inquiry cancellation (FR-006); they cancel the booking only at the FR-029 Unpaid Balance Cancellation Point, when one is set (REQ-007B-026, REQ-007B-052, REQ-007B-102)
- Remaining installments are scheduled at 30-day intervals (REQ-007B-006)
- Installment amounts are equal shares of the booking total, rounded down; the last installment is the total minus the others (REQ-007B-004)
- The patient may choose any enabled installment count (FR-029) from 2 up to the maximum; when none fits the installment option is not shown; the same cutoff window applies (REQ-007B-036, REQ-007B-106)
- The other payment options FR-007 offers (pay in full, deposit and balance) are always available as alternatives to installments (REQ-007B-040, REQ-007B-041)
- No rescheduling fee is charged on an installment plan in V1 (REQ-007B-050)
- Overdue is the day after the due date while the installment is unpaid and not paused; the day's retry runs first; the patient gets one overdue notice, which replaces that day's failure notice and states the cancellation date when the point is set, and the billing admins one notice, and the provider sees the banner only until the plan is Defaulted (REQ-007B-100, REQ-007B-101)
- The installment option is offered only when installments are enabled, the booking total is at or above the FR-029 minimum (converted at the locked rate) and the days until the procedure are at least the cutoff days plus 30 and at least one enabled count is within the maximum (REQ-007B-106)
- While the booking carries the support-required marker (FR-006 REQ-006-081) nothing is charged, retried, reminded, flagged, fee-ed or handed to FR-006 Alternative Flow B8, and the retry, grace and cancellation-point clocks pause, not reset; a replacement plan recalculates all dates, otherwise charges resume at the FR-006 Screen 10 submit (REQ-007B-103)
- The FR-006 Cancel Booking route is open only while the booking is `Accepted`, `Payment Window Expired` or `Confirmed` (`In Progress` only through the FR-006 provider-fault route); after treatment starts a Defaulted plan is resolved by payment only (REQ-007B-104)
- Later installments on a Defaulted plan are paused, not Overdue and fee-free until the plan returns to Active; each past-due one is then charged once at the next daily run (REQ-007B-105, REQ-007B-108)
- Retries and the grace period continue past the cutoff; the plan is Completed when the final installment is paid, after which the clinic's share moves as FR-007 REQ-007-090 sets (REQ-007B-107)
- A Defaulted plan returns to Active when no installment is Failed or Overdue, whoever paid (the patient with Pay now or a new card, an admin Retry Charge, or Mark as Resolved), and is Completed when every installment is Paid (REQ-007B-108)
- An installment is settled outside the card only as a recorded bank transfer into Hairline's account, approved by a second admin who holds the Resolve Installments permission (REQ-007B-109)
- A fixed late fee is converted at the plan's accepted exchange rate, a percentage fee applies to the late installment amount, the fee is outside the clinic's share and commission, an uncollected fee lapses when the plan ends, and a provider-fault full refund returns a collected fee (REQ-007B-110)
- The plan keeps the late fee, grace period and cancellation point in force at confirmation (REQ-007B-111)
- On an Active plan Pay now can also pay the next scheduled installment, or all remaining installments, in due-date order (REQ-007B-112)

### Data & Privacy Rules

- Payment method details stored securely per PCI-DSS standards (via payment processor) (REQ-007B-073)
- Payment methods are tokenized; full card numbers are never stored (REQ-007B-010)
- Installment payment records are encrypted at rest and in transit (REQ-007B-011)
- Access to installment payment data follows RBAC: patients see their own installments; providers see booking payment status; admins see all plans (REQ-007B-072)
- Every installment payment attempt and lifecycle event is logged in a tamper-evident audit trail (REQ-007B-012)
- Compliance: PCI-DSS (via processor), GDPR/HIPAA-aligned handling of payment data (REQ-007B-073)

### Admin Editability Rules

**Editable by Admin**:

- Customer-facing installment plan settings are configured via **FR-029 (A-09)** (REQ-007B-079):
  - Enabled installment counts (2-9)
  - Cutoff days (30-90) requiring full payment completion before procedure date
  - Minimum booking amount eligibility threshold
  - Late payment grace period, counted from the due date; when it passes unpaid the late fee is added once to the installment (REQ-007B-099)
  - Late fee amount (the rescheduling fee does not apply to installment plans in V1, REQ-007B-050)
  - Unpaid Balance Cancellation Point (days after the first missed due date; applies to bookings confirmed after it was set; while unset nothing cancels automatically) (REQ-007B-102)
  - A plan keeps the late fee, grace period and cancellation point in force when it was confirmed; a later change applies only to plans confirmed afterwards (REQ-007B-111)
- Payment reminder timing is the FR-007 setting (whole days 0 to 14 before the due date, up to 3 reminders, default 3 days before and on the due date) (REQ-007B-014)

**Fixed in Codebase (Not Editable)** (REQ-007B-074):

- Interest rate (always 0% - interest-free policy)
- Installment frequency (monthly; 30-day intervals)
- Core payment security controls and encryption standards
- Number of retry attempts for failed payments (3 attempts, only after a retryable failure)
- Retry schedule for failed payments (waits of 1 day, 3 days, 7 days)
- Audit logging scope for payment events

**Configurable with Restrictions**:

- Cancellation refund ladder for installment plans (owned by FR-029, Payment settings) (REQ-007B-056)
- Payment processor integration settings (requires technical deployment, not runtime editable) (REQ-007B-074)

### Payment & Billing Rules

- Installment charges are automatic on scheduled dates (patient consent given at checkout) (REQ-007B-015, REQ-007B-043)
- A retryable failure (anything except a hard decline, so a technical fault or insufficient funds) gets 3 automatic retries after waits of 1, 3 and 7 days; a hard decline (expired, lost, stolen, invalid or fraud-flagged card) gets none and cancels any retry still pending, and the installment is Defaulted on day 11 after its due date if still unpaid; admin retries do not count toward the 3 (REQ-007B-018)
- The plan is flagged Defaulted after 3 failed retries, or on day 11 after a hard decline; the admin, the patient and the provider are notified (REQ-007B-019, REQ-007B-020)
- The patient can update the card of an active plan at any time before the next installment is charged; the new card applies to the remaining installments and to a Failed or Overdue one, which the update re-offers to charge (REQ-007B-021, REQ-007B-047)
- The refund base is the paid amount excluding late fees; FR-006 and FR-007 compute the refund per the FR-029 refund ladder, and FR-007B only voids the unpaid installments and records the outcome (REQ-007B-022, REQ-007B-054)
- A late fee is added once to an installment when the late payment grace period saved on the plan, counted from the due date, passes unpaid and no automatic retry is pending; it is collected with the next successful charge, never as a separate charge, and the refund base excludes it. The fee amount is set by the admin in FR-029 (REQ-007B-099, REQ-007B-110)
- Money movement (Hairline as the seller on the card payment, refunds, chargebacks and Stripe fees, the clinic's share moving to its locked Stripe balance, the pull-back on cancellation or rescheduling, and the payout at release), commission calculation and payout timing are owned by FR-007 (REQ-007-090) and FR-017. FR-007B adds only that the plan is Completed when the final installment is paid, normally by the cutoff date, after which the share moves as FR-007 REQ-007-090 sets (REQ-007B-098, REQ-007B-070, REQ-007B-071, REQ-007B-049, REQ-007B-107)
- An admin date change keeps the due dates, count and amounts and recalculates the Final Payment Deadline from the new date when every remaining installment still fits the cutoff days; otherwise FR-006 blocks the change and nothing changes (REQ-007B-024, REQ-007B-060, REQ-007B-061, REQ-007B-062)
- Installment charges must be idempotent (prevent duplicate charges on retry) (REQ-007B-068)
- Installment schedule and amounts are immutable once confirmed (prevent tampering) (REQ-007B-069)
- Cancellation refund policy applies same percentages to installment plans as to single payments (REQ-007B-055)
- For a provider-selected promotion or patient-entered code, the first successful installment consumes the promotion use reserved at acceptance (an automatic promotion's use is consumed at acceptance per FR-019); installments never apply or remove a promotion (REQ-007B-048)
- Installment revenue tracked separately from one-time payments
- Installment due dates are timestamps stored in UTC; the charge, the Overdue flag and the late fee all use the calendar day in the clinic's timezone, as FR-007 does for the final payment, and dates are displayed in the patient's timezone; the schedule of the scheduled job that acts on them (hourly, with reminders at 9 AM clinic time, 3 days before the due date) is owned by FR-017 (REQ-017-183)
- Defaulted plans are flagged on the admin dashboard and notified to the admins (REQ-007B-020); no resolution deadline is set

### Admin Action & Audit Rules

Per Hairline Platform Constitution (Principle VI: Data Integrity & Audit Trail), all admin actions that modify installment plan state MUST be audited (REQ-007B-083):

**Admin Actions Requiring Justification & Audit Logging**:

- **Retry Charge**: Manually triggering a payment retry on a failed installment (requires justification minimum 20 characters; logged with timestamp, admin ID, action type, installment ID, retry attempt number) (REQ-007B-080, REQ-007B-084)
- **Mark as Resolved**: Marking an unpaid installment as resolved by a recorded bank transfer (requires justification minimum 20 characters and the approval of a second admin who holds the Resolve Installments permission; logged with timestamp, admin ID, action type, installment ID, amount, date, receiving account, reference and approving admin) (REQ-007B-081, REQ-007B-084, REQ-007B-109)
- **Cancelling a booking with an installment plan** is not a plan action: the admin uses the FR-006 Cancel Booking action, which stops the remaining installments and applies the refund (REQ-007B-023, REQ-007B-053, REQ-007B-057, REQ-007B-058)

**Audit Trail Requirements**:

- All admin actions documented in Screen 6 (Admin Booking Installment Plan Detail) MUST be logged to the immutable audit trail system (S-06: Audit Log Service) (REQ-007B-086)
- Audit log retention follows the system PRD, Platform-Wide Rules: One 10-year retention period (REQ-007B-087)
- Audit logs MUST include: timestamp (UTC), admin user ID, admin name, action type, affected entity IDs (installment plan ID, booking ID, patient ID), justification text, before/after state (if applicable), IP address (REQ-007B-088)
- Failed admin action attempts (e.g., insufficient permissions, validation errors) MUST also be logged (REQ-007B-089)
- Audit logs MUST be tamper-proof and queryable for compliance reporting (REQ-007B-086)
- Admin access to installment management logged with user ID and timestamp (REQ-007B-086)

**Access Control**:

- Only an admin who holds the matching permission can run an installment action: Retry Charge for Retry Charge, and Resolve Installments for Mark as Resolved and for approving it (FR-031) (REQ-007B-090)
- Role-based access control (RBAC) enforced per FR-031 (Admin Access Control & Permissions) (REQ-007B-091)
- All installment data access (read and write) is subject to RBAC validation (REQ-007B-091)

**Carried from dropped sections (original wording)**:

- **Failure handling**: Queue failed jobs for retry; alert admin if scheduling system unavailable
- **Provenance**: resolves the AcceptanceEvent, accepted parent quote and subquote IDs and versions through its booking (FR-007 REQ-007-019)
- **Entity 3 - Payment Method**: The single record of a patient's saved payment method, used by installment plans here and read by the FR-007 payment screens and the FR-016 patient payments view. The payment method it records is a card: a tokenized recurring payment method. Installments need a saved card and the first installment must use it; a bank transfer cannot pay an installment plan
- **Ownership**: FR-007B owns installment plans and payment methods; the Stripe account and the split-payment setting belong to FR-029

---

## Dependencies

Related FRs: FR-006 (installment plan tied to booking confirmation and procedure date), FR-007 (core payment infrastructure for processing installment charges; uses same payment gateway, security controls, receipt generation; installments extend deposit/final payment logic), FR-019 (the accepted promotion and any patient promotion code are already in the plan total), FR-017 (payout and fund release timing), FR-029 (installment, late fee and cancellation point settings), FR-031 (the Retry Charge, Resolve Installments and Issue Refunds permissions). Related modules: P-01 (only authenticated patients can enroll in installment plans), A-05 (admin oversight of installment plans and revenue reconciliation), S-03 (send installment reminders, confirmations, and failure notifications).

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
7. **Given** a booking with the procedure 50 days away and a 30-day cutoff, **When** patient views checkout, **Then** the installment option is not offered and only pay in full is offered
8. **Given** only the counts 5 and 9 are enabled and the procedure allows a maximum of 4, **When** patient views checkout, **Then** the installment option is not shown and only pay in full is offered
9. **Given** the installment option is offered, **When** patient views the plan before confirming, **Then** the late fee, the grace period and, when set, the cancellation point are shown, and the plan keeps those values after later FR-029 changes

---

### User Story 2 - Automatic Installment Charging and Reminders (Priority: P1)

System sends reminders at the times set in the FR-007 payment reminder setting, automatically charges payment method on due date, and confirms successful payment to patient.

**Why this priority**: Core automation that reduces manual work and ensures timely payments; essential for installment plans to function.

**Independent Test**: Set up installment plan with test dates; trigger reminders at the set times before due; trigger automatic charge on due date; verify payment processed and confirmation sent.

**Acceptance Scenarios**:

1. **Given** an installment due in 3 days and the default reminder setting, **When** reminder trigger executes, **Then** patient receives email and push notification with amount and date
2. **Given** installment due date arrives, **When** scheduled charge executes, **Then** payment method is charged automatically
3. **Given** installment charge succeeds, **When** payment confirmed, **Then** patient receives confirmation notification and installment marked as paid in booking details
4. **Given** an Active plan with scheduled installments, **When** patient uses Pay now, **Then** the next scheduled installment, or all remaining installments, is paid in due-date order and the due dates of unpaid installments do not change

---

### User Story 3 - Handle Failed Installment Payments (Priority: P1)

System detects failed installment charge, notifies patient immediately, executes 3 retry attempts with increasing delays when the failure is retryable (any failure except a hard decline), and flags plan as defaulted if all retries fail. After a hard decline there is no automatic retry; the patient must use Pay now or update the card, and the plan is Defaulted on day 11 after the due date if still unpaid.

**Why this priority**: Critical error handling to recover from payment failures and protect revenue; prevents silent failures.

**Independent Test**: Simulate failed installment charge; verify immediate patient notification; verify 3 retry attempts execute on schedule (waits of 1 day, 3 days, 7 days) after a retryable failure; verify a hard decline notifies the patient and triggers no automatic retry; verify admin notification if all retries fail.

**Acceptance Scenarios**:

1. **Given** scheduled installment charge fails, **When** failure detected, **Then** patient is notified immediately with clear error message and guidance
2. **Given** a retryable failure and the first retry attempt is due (1 day later), **When** retry executes and fails, **Then** system schedules second retry after a wait of 3 days
3. **Given** all 3 retry attempts fail, **When** retries exhausted, **Then** system flags installment plan as "Defaulted" and notifies the admin (for intervention), the patient and the provider
4. **Given** a later installment is defaulted, **When** admin reviews it, **Then** the booking is not moved to `Payment Window Expired` and the inquiry is not cancelled
5. **Given** the charge was hard declined, **When** failure detected, **Then** the patient is notified and must use Pay now or update the card, and no automatic retry is scheduled
6. **Given** a hard declined installment still unpaid on day 11 after its due date, **When** the day passes, **Then** the plan is flagged "Defaulted"
7. **Given** the cancellation point is set and the booking was confirmed after it was set, **When** that many days have passed since the first missed due date, **Then** the booking is handed to FR-006 Alternative Flow B8 even if retries are still pending, unless the support-required marker is on
8. **Given** the booking carries the support-required marker, **When** a due date or retry date arrives, **Then** nothing is charged, retried, reminded, flagged Overdue or Defaulted, and no late fee is added; the cancellation-point count pauses and no hand-off to FR-006 Alternative Flow B8 runs
9. **Given** a charge fails for insufficient funds, **When** failure detected, **Then** it is retried like a technical failure; a card that is expired, lost, stolen, invalid or fraud-flagged is a hard decline and is not retried
10. **Given** a retry returns a hard decline, **When** the result arrives, **Then** the retries still pending are cancelled and the plan is flagged "Defaulted" on day 11 after the due date if the installment is still unpaid
11. **Given** a retry on the day after the due date succeeds, **When** that day ends, **Then** no overdue notice is sent; if it fails, the overdue notice replaces that day's failure notice and states the cancellation date when the point is set
12. **Given** the grace period has passed while an automatic retry is still pending, **When** the retries end with the installment unpaid, **Then** the late fee is added once

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

**Independent Test**: Create defaulted installment plan; admin views flagged plan in dashboard; admin retries the charge or marks it resolved; verify payment processed or booking cancelled per admin decision.

**Acceptance Scenarios**:

1. **Given** an installment plan flagged as "Defaulted," **When** admin views installment management dashboard, **Then** defaulted plan appears with patient, booking, and overdue details
2. **Given** admin reviews defaulted plan, **When** admin contacts patient and resolves payment issue, **Then** admin can Retry Charge or Mark as Resolved
3. **Given** payment issue unresolved and the booking is `Accepted`, `Payment Window Expired` or `Confirmed`, **When** admin decides to cancel booking, **Then** system cancels booking, refunds per policy, and cancels remaining installments; once treatment has started the cancel route is closed and the plan is resolved by payment only
4. **Given** a Defaulted plan whose installment was settled by a bank transfer, **When** the admin enters the amount, date, receiving account and reference and a second admin who holds the Resolve Installments permission approves, **Then** the installment is Paid with payment source manual and the plan follows REQ-007B-108; without the second approval nothing changes
5. **Given** a Defaulted plan, **When** the patient pays the Failed installment with Pay now or a new card, **Then** the plan returns to Active (Completed when every installment is Paid) without an admin action
6. **Given** a plan returned to Active with later installments whose due dates passed while it was Defaulted, **When** the next daily run executes, **Then** each is charged once at its original amount with the normal failure handling, and none carried an Overdue flag, notice, reminder or late fee while paused

---

### User Story 6 - Patient Cancels Booking With Partial Installments Paid (Priority: P3)

Patient requests booking cancellation after paying 2 of 4 installments; admin reviews cancellation timing; system calculates refund per policy; refund processed and remaining installments cancelled.

**Why this priority**: Less frequent scenario (cancellations are minority of bookings); important for fairness but not core to happy path.

**Independent Test**: Create installment plan with 2 of 4 installments paid; patient requests cancellation 20 days before procedure; verify refund calculated as a percentage of the paid amount, excluding late fees, per the FR-029 refund ladder; verify remaining 2 installments cancelled.

**Acceptance Scenarios**:

1. **Given** patient has paid 2 of 4 installments, **When** patient requests cancellation 20 days before procedure, **Then** system calculates refund as a percentage of the paid amount, excluding late fees, per the FR-029 refund ladder
2. **Given** refund calculated, **When** admin approves cancellation, **Then** refund is processed to patient's original payment method
3. **Given** cancellation confirmed, **When** system updates booking status, **Then** remaining 2 installments are cancelled (not charged) and the plan is `Cancelled`

---

### Edge Cases

- What happens when patient's payment method expires mid-plan? (Charge is declined; no automatic retry; patient is notified and must use Pay now or update the card) (REQ-007B-018)
- How does system handle procedure date rescheduled after installment plan established? (The due dates stay and the Final Payment Deadline is recalculated when every remaining installment still fits; otherwise FR-006 blocks the change and nothing changes) (REQ-007B-024, REQ-007B-061, REQ-007B-062)
- What occurs if first installment fails at checkout? (Booking stays `Accepted` and not confirmed; patient may retry or use a different payment method only while the original FR-006 payment hold is active, per FR-007 REQ-007-017; when the hold expires the booking moves to `Payment Window Expired`, installment checkout is blocked, and recovery follows FR-006) (REQ-007B-026, REQ-007B-052)
- What if a later installment is missed? (B1 retry and default handling applies, with automatic retries only after a retryable failure; it never causes `Payment Window Expired` or inquiry cancellation) (REQ-007B-052, REQ-007B-018)
- What if the provider fails after acceptance? (Alternative Flow B4 and FR-006 Alternative Flow B5 apply) (REQ-007B-027, REQ-007B-063, REQ-007B-064, REQ-007B-096, REQ-007B-097)
- What if the quote, package or promotion is edited after acceptance? (No effect; the plan reads only the accepted snapshot)
- How to manage patient requesting fewer installments mid-plan? (Not supported; the patient can pay the next scheduled installment or all remaining installments early with Pay now, in due-date order, and the due dates of unpaid ones do not change) (REQ-007B-066, REQ-007B-112)
- What if the admin changes the cutoff window (for example from 30 to 45 days), the late fee, the grace period or the cancellation point via FR-029? (Applies only to plans confirmed afterwards; each plan keeps the values in force at confirmation) (REQ-007B-065, REQ-007B-111)
- How does system handle refund for partial installments if patient disputes charge? (Admin reviews the dispute; the refund is processed per the resolution through the FR-007 approval, never self-approved; the booking may be cancelled where its state allows it, or continue) (REQ-007B-059)
- What if a due date falls while a provider fault is pending? (No charge, retry, reminder, Overdue, Defaulted, late fee or hand-off to FR-006 Alternative Flow B8; the clocks pause, including the cancellation-point count; a replacement plan recalculates all dates, otherwise charges resume at the FR-006 Screen 10 submit) (REQ-007B-103)
- What if the final installment is paid after the cutoff date? (Retries and the grace period continue past the cutoff; the plan is Completed when the final installment is paid, after which the clinic's share moves as FR-007 REQ-007-090 sets) (REQ-007B-107)
- What if a charge is in flight when the booking is cancelled? (The void waits for it; a charge that still succeeds is added to the refund base) (REQ-007B-023)
- What if a Defaulted plan is paid by the patient rather than the admin? (The plan returns to Active and the paused installments follow REQ-007B-105) (REQ-007B-108)
- What if payment processor webhook fails to deliver charge status? (System polls payment status as fallback; ensures no missed confirmations or retries) (REQ-007B-067)

---

## Functional Requirements Summary

### Core Requirements

- **REQ-007B-001**: System MUST offer interest-free installment payment plans with 2-9 monthly payments
- **REQ-007B-002**: System MUST determine feasible installment options based on time until procedure, monthly frequency, and the cutoff days configured in FR-029 (minimum 30 days; the plan keeps the cutoff days it was created with); the maximum number of installments is (days until procedure - cutoff days) ÷ 30, rounded down, plus 1, so 60 days with a 30-day cutoff allows 2 installments; offered options are limited to enabled installment counts configured in FR-029 (2-9)
- **REQ-007B-003**: System MUST enforce the cutoff window: final installment must complete by the configured cutoff days before procedure date (minimum 30 days; configured in FR-029)
- **REQ-007B-004**: System MUST calculate installment amounts as equal shares: booking total (accepted price after promotion) ÷ number of installments, rounded down to the currency's smallest unit; the last installment is the total minus the sum of the others, so the amounts always sum to the total
- **REQ-007B-005**: System MUST charge the first installment at checkout; its success confirms the existing `Accepted` booking (FR-006)
- **REQ-007B-006**: System MUST schedule remaining installments at 30-day intervals

### Data Requirements

- **REQ-007B-007**: System MUST maintain installment schedule with amounts and due dates per booking
- **REQ-007B-008**: System MUST track installment payment status as one list: scheduled, retrying, paid, failed, cancelled; Overdue is a calculated flag, not a status
- **REQ-007B-009**: System MUST persist a patient's card securely for recurring charges (tokenized); installments need a saved card and the first installment MUST use it, so a bank transfer cannot pay an installment plan

### Security & Privacy Requirements

- **REQ-007B-010**: System MUST tokenize payment methods (never store full card numbers)
- **REQ-007B-011**: System MUST encrypt all installment payment records at rest and in transit
- **REQ-007B-012**: System MUST log every installment payment attempt and lifecycle event (scheduled, charged, failed, retried, refunded) with timestamp, amount, status, and user, in a tamper-evident audit trail

### Integration Requirements

- **REQ-007B-013**: System MUST integrate with payment processor for scheduled/recurring charges
- **REQ-007B-014**: System MUST send installment payment reminders at the times set in the FR-007 payment reminder setting (whole days 0 to 14 before the due date, up to 3 reminders, default 3 days before and on the due date)
- **REQ-007B-015**: System MUST automatically charge payment method on installment due date
- **REQ-007B-016**: System MUST send the patient a confirmation notification after a successful installment charge

### Error Handling Requirements

- **REQ-007B-017**: System MUST detect failed installment charges and notify patient immediately
- **REQ-007B-018**: System MUST execute 3 automatic retry attempts for an installment whose charge failed for a retryable reason (any failure except a hard decline, so a technical fault or insufficient funds), with waits of 1 day, 3 days and 7 days (retries fall on day 1, day 4 and day 11 after the failure). A hard decline is a refusal because the card is expired, lost, stolen, invalid or flagged for fraud. After a hard decline, or when a retry returns one, System MUST NOT retry automatically and MUST cancel the retries still pending; it MUST notify the patient, who must use Pay now or update the card, and the installment becomes Defaulted on day 11 after the due date if still unpaid. Admin retries do not count toward the 3 automatic retries
- **REQ-007B-019**: System MUST flag installment plan as "Defaulted" after 3 failed retry attempts, or on day 11 after the due date when the charge was hard declined and the installment is still unpaid
- **REQ-007B-020**: System MUST notify the admin (for intervention), the patient and the provider of a defaulted installment plan

### Cancellation & Refund Requirements

- **REQ-007B-021**: System MUST allow the patient to update the card of an active installment plan at any time before the next installment is charged; the new card applies to the remaining installments and to a Failed or Overdue one, which the update re-offers to charge, and the patient can charge it at once with Pay now. Neither happens while the support-required marker is on
- **REQ-007B-022**: System MUST show the admin the amount paid so far excluding late fees as the refund base. FR-006 and FR-007 compute the refund as a percentage of that amount per the cancellation refund ladder owned by FR-029 (or the provider-fault terms), and FR-007B only voids the unpaid installments and records the outcome
- **REQ-007B-023**: System MUST cancel remaining installments when booking is cancelled; the void is one step shared by the admin cancellation, the provider-fault cancellation and the unpaid-balance cancellation: it runs before the refund is computed, waits for any charge in flight, sets the plan Cancelled, and adds a charge that still succeeds to the refund base; stopping the installments and the refund happen inside the FR-006 Cancel Booking action, and installment plans have no separate cancel action
- **REQ-007B-024**: System MUST handle an admin date change by keeping the due dates, count and amounts and recalculating the Final Payment Deadline from the new date; when the remaining installments cannot all stay at least the cutoff days before it, System MUST return no feasible plan and FR-006 blocks the change

### Accepted Snapshot & Payment Window Requirements

- **REQ-007B-025**: System MUST copy the installment plan total, currency and exchange rate read-only from the FR-005 accepted snapshot through the FR-006 booking; the total already includes the accepted promotion and any patient promotion code; it MUST NOT be recomputed and MUST be shown with its currency on all installment screens
- **REQ-007B-026**: System MUST allow first-installment retries only within the original FR-006 payment hold; `Payment Window Expired` applies only to that first payment step, and missed later installments MUST NOT cause `Payment Window Expired` or inquiry cancellation; they cancel the booking only at the FR-029 Unpaid Balance Cancellation Point, when one is set
- **REQ-007B-027**: When the provider fails after acceptance (FR-006 Alternative Flows B4 and B5 only), System MUST cancel remaining installments with no patient cancellation fee. On a provider withdrawal, drop-out, suspension or deactivation, System MUST refund in full every installment already paid and any late fee already collected, and the replacement booking takes a new payment per FR-006 Alternative Flows B4 and B5. The FR-006 unpaid-balance cancellation does not take this path: it takes the refund ladder

### Overdue, Cancellation Point, Pending Fault, Defaulted Plan and Late Fee Requirements

- **REQ-007B-101**: An installment is Overdue from the day after its due date while it is unpaid, not Cancelled and not paused on a Defaulted plan; that day's retry runs first, and the patient gets one overdue notice, which replaces that day's failure notice and states the date on which the booking will be cancelled when the cancellation point is set, the billing admins one notice, and the provider sees the banner only until the plan is Defaulted
- **REQ-007B-102**: When the Unpaid Balance Cancellation Point saved on the plan is set (the booking was confirmed after FR-029 set it), System MUST hand the Confirmed booking to FR-006 Alternative Flow B8 that many days after the due date of the first missed installment, whatever the retry, grace period or Defaulted state; while the support-required marker is on the count pauses and nothing is handed over
- **REQ-007B-103**: While the booking carries the support-required marker (FR-006 REQ-006-081), System MUST NOT charge, retry, remind, flag Overdue or Defaulted, add a late fee or hand the booking to FR-006 Alternative Flow B8, and the retry, grace and cancellation-point clocks pause, not reset; a replacement plan recalculates all dates, otherwise charges resume at the FR-006 Screen 10 submit
- **REQ-007B-104**: The FR-006 Cancel Booking route is open only while the booking is Accepted, Payment Window Expired or Confirmed (In Progress only through the FR-006 provider-fault route); after treatment starts a Defaulted plan is resolved by payment only
- **REQ-007B-105**: Later installments on a Defaulted plan MUST stay paused until the plan returns to Active: they keep their dates and amounts, are not Overdue, and get no overdue notice, reminder or late fee. When the plan returns to Active, each paused installment whose due date has passed MUST be charged once at the next daily run, before any Overdue flag or notice that day, with the normal failure handling
- **REQ-007B-106**: System MUST offer the installment option only when installments are enabled, the booking total is at or above the FR-029 minimum (converted at the locked rate) and the days until the procedure are at least the cutoff days plus 30; the options offered are the enabled counts up to the maximum, and when none fits the installment option MUST NOT be shown
- **REQ-007B-107**: Retries and the grace period continue past the cutoff; the plan is Completed when the final installment is paid, after which the clinic's share moves as FR-007 REQ-007-090 sets
- **REQ-007B-108**: A Defaulted plan MUST return to Active when no installment is Failed or Overdue, whoever paid (the patient with Pay now or a new card, an admin Retry Charge, or Mark as Resolved), and MUST become Completed when every installment is Paid
- **REQ-007B-109**: Mark as Resolved MUST be used only for a bank transfer into Hairline's account. The admin MUST enter the amount, date, receiving account and reference, and a second admin who holds the Resolve Installments permission (FR-031) MUST approve it, never the same admin; only then is the installment Paid with payment source manual. FR-007 owns the manual payment record, the refund of a manual payment and the clinic-share movement for it
- **REQ-007B-110**: A fixed late fee MUST be converted at the plan's accepted exchange rate and a percentage fee MUST apply to the late installment amount. The fee MUST stay outside the clinic's share and commission (owned by FR-029 and FR-007). A fee still uncollected when the plan ends lapses. A provider-fault full refund (REQ-007B-027) returns a collected fee
- **REQ-007B-111**: Screen 1 MUST show the late fee, the grace period and, when set, the cancellation point before the patient confirms. The plan MUST keep the values in force at confirmation, as it keeps the cutoff days; a later FR-029 change applies only to plans confirmed afterwards
- **REQ-007B-112**: On an Active plan, Pay now MUST also let the patient pay the next scheduled installment, or all remaining installments at once, in due-date order; the due dates of unpaid installments do not change, and the plan is Completed when every installment is Paid

---

## Appendix: Change Log

| Date       | Version | Changes                 | Author |
|------------|---------|-------------------------|--------|
| 2026-11-22 | 1.13 | Requirements graph programme baseline: PRD compressed to the checklist structure (each rule stated once, field rows tagged with graph field ids, dropped classes removed). No rule changes. Earlier history (v1.0 to v1.12) and the change request CR-FR007B-20261016-01 (change-request-2026-10-16-mtg002-quote-model-alignment.md) are in `archived/prd-baseline-2026-11-08/` and in git history. | Product Owner / Documentation |
| 2026-11-23 | 1.14 | Independent compression review: four clauses from the dropped Dependencies and Key Entities sections restored in original wording under Business Rules (scheduler failure handling, installment plan provenance, payment method record, FR-007B and FR-029 ownership). No rule changes. | Controller |
| 2026-11-23 | 1.15 | Logic review of the installment flows. Overdue is now a calculated flag from the day after the due date with one patient notice and one billing-admin notice, and the provider sees a banner until the plan is Defaulted. An unpaid balance reaches the FR-029 cancellation point whatever the retry state, and a pending provider fault pauses charges, retries, reminders and fees. The cancel route and the Defaulted plan are guarded by booking state, and FR-006 and FR-007 compute the refund from the paid amount excluding late fees. A date change that leaves no feasible plan is blocked by FR-006 and the insufficient-time notice is removed. The provider-fault refund no longer applies to the unpaid-balance cancellation. Reminder timing follows the FR-007 setting, the installment threshold reads the cutoff days, a late fee is added once and collected with the next charge, a hard decline reaches Defaulted on day 11 and can be paid with Pay now, Mark as Resolved and Retry Charge have defined results, and installments need a card. Payout and commission timing point to FR-007 and FR-017, the rescheduling fee does not apply in V1, and the stray cross-reference lines carry their rule text. | Controller / Documentation |
| 2026-11-23 | 1.16 | Second logic review of the installment flows. A pending provider fault now also pauses the count toward the cancellation point and the hand-off to FR-006. Paused installments on a Defaulted plan carry no Overdue flag, notice, reminder or fee and are charged once at the next daily run when the plan returns to Active, which happens whoever pays. Mark as Resolved is limited to a recorded bank transfer that a second billing admin approves. The late fee has a currency and a base, sits outside the clinic's share and commission, waits until the retries end, lapses with the plan and is returned on a provider-fault refund. Screen 1 shows the late fee, grace period and cancellation point, the plan keeps them as confirmed, and the overdue notice states the cancellation date. A date change keeps the due dates and recalculates only the final payment deadline. Only enabled installment counts are offered. Pay now can pay early. The provider list covers plans of every status. The clinic's share follows the FR-007 timing. Insufficient funds is retried and hard declines are defined. One void step runs before the refund and sets the plan Cancelled. The schedule of the daily job is left to FR-017. The word cancelled is spelled one way. | Controller / Documentation |
| 2026-11-25 | 1.16 | Reference only, no version change: the Source line now names the canonical constitution file `local-docs/project-requirements/constitution.md`. | Product Owner |
| 2026-11-25 | 1.17 | Cross-FR alignment. Installment actions are gated by the FR-031 permissions (Retry Charge, Resolve Installments) instead of role names, and the second approver of Mark as Resolved holds Resolve Installments; refund approval names the Issue Refunds permission. The installment-charged and plan-completed notifications are stated as going to the patient. Completing the last installment is named as the moment the booking becomes Full paid, which FR-018 reads. The installment job schedule is pointed to FR-017. | Product Owner / Documentation |

---

## Appendix: Approvals

| Role            | Name   | Date   | Signature/Approval |
|-----------------|--------|--------|--------------------|
| Product Owner   | Product Owner | 2026-10-18 | Approved v1.5 via MTG-002 decision log (documentation only) |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0
**Based on**: FR-007B from system-prd.md (Split Payment / Installment Plans)
**Last Updated**: 2026-11-25
