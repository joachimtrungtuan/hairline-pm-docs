# FR-006 - Booking & Scheduling

**Module**: P-03: Booking & Payment | PR-02: Inquiry & Quote Management | A-01: Patient Management & Oversight
**Feature Branch**: `fr006-booking-scheduling`
**Created**: 2025-11-04
**Status**: 🟡 Revised — Pending Consolidated Verification
**Source**: FR-006 from `system-prd.md`; SRC-MTG-002, CR-FR006-20260915-01 and CR-FR006-20261016-01; continuation from FR-004 (Quote Submission) and FR-005 v2.3 (Subquote Comparison & Acceptance); coordinated with FR-007/FR-007B (Payments)

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
- Pay in full or choose an installment plan within offered limits (the deposit is the first payment step); view booking confirmation and itinerary basics.
- View cancellation policy and refund outcomes.
- No in-app booking cancellation: from acceptance onward the patient sees a "Contact support" action, and an admin performs any cancellation (Alternative Flow B2).

**Provider Platform (PR-02)**:

- View accepted/confirmed bookings in table list format (no calendar view) (REQ-006-022); receive confirmation notifications; enforce check-in workflow on arrival (handoff to FR-010).
- View deposit state and payment status (no card details); apply cancellation policy outcomes.
- Monitor booking status transitions and patient arrival readiness.

**Admin Platform (A-01, A-05, A-09)**:

- Monitor booking pipeline, intervene in disputes, process exceptional modifications under audit.
- Perform the governed booking interventions from Screens 6 to 11: revive a `Payment Window Expired` booking, change the appointment, cancel a booking (including support-routed patient requests), run the provider-fault transfer with an admin-authored replacement quote, hand an Aftercare-stage provider fault to the FR-011 aftercare reassignment, resolve an `In Progress` provider fault or close an `In Progress` case early with no fault (Screen 11), and make an audited emergency edit of non-money booking details.
- Configure global cancellation policy schedule, booking confirmation templates, and notification preferences per constitution limits.
- View financials for deposits/refunds (FR-017) and commission impacts.

**Shared Services (S-02, S-03, S-05)**:

- S-02 Payment Processing: deposits, refunds, installments.
- S-03 Notification Service: confirmations, reminders, reschedule/cancellation notices.
- S-05 Media Storage: stores booking documents (confirmations, invoices) and itinerary files.

### Communication Structure

**In Scope**:

- Email/push confirmations for booking creation, payment receipt, reminders, reschedule outcomes, cancellation outcomes. (REQ-006-026)
- In-app notifications for booking state changes and reminders. (REQ-006-026)

**Out of Scope**:

- Direct patient↔provider chat (handled by FR-012 scope); SMS optionality is handled by S-03 settings and **does not exist in MVP (no SMS booking notifications are sent until a future phase explicitly enables SMS in S-03/FR-020/FR-030)**. (REQ-006-027)
- Travel booking details (handled by FR-008) beyond minimal itinerary placeholders.

### Entry Points

- Patient-initiated via mobile from the Accepted Subquote detail view. (REQ-006-021)
- Activation: Becomes available immediately after FR-005 subquote acceptance. (REQ-006-021)
- Confirmation: Occurs after successful deposit (or first installment) per FR-007/FR-007B, which also unmask patient identity and blocks provider calendar. (REQ-006-021)

---

## Business Workflows

### Main Flow: Subquote Acceptance → Booking Confirmation

**Actors**: Patient, Provider, Admin, Payment Service, Notification Service
**Trigger**: Patient accepts one subquote in FR-005; its appointment slot was pre-scheduled on the resolved FR-004 Option/date-price record
**Outcome**: Booking confirmed; deposit paid; provider calendar blocked; confirmations sent

**Booking Creation**: The booking record is created with status `Accepted` in the same transaction as the FR-005 AcceptanceEvent and the exclusive slot hold. The appointment record (`schedules`) is not created at acceptance; it is created only at the first successful payment (step 7). (REQ-006-028)

**Pre-Booking Validation**: Before entering the booking/payment flow, system MUST verify:

- The parent inquiry is NOT in "Cancelled" status (FR-003 Workflow 5). If cancelled, system blocks entry with message: "This inquiry has been cancelled. Booking is no longer available."
- The accepted subquote and parent quote are still in "Accepted" status, their versions match the FR-005 AcceptanceEvent, and the AcceptanceEvent owns the slot's valid exclusive payment-window hold. (REQ-006-029)

**Steps**:

1. Patient opens the Accepted Subquote detail view and reviews the immutable accepted selection and inherited parent context; no commercial or appointment field can be reselected.
2. Patient proceeds directly to payment screen (pay in full or in installments per FR-029 split payment configuration and FR-007B eligibility; the deposit is the first payment step).
3. System uses the FR-029 calculation for the first payment (REQ-029-016) and presents the cancellation policy through the full Cancellation Policy link (FR-027), with the refund ladder numbers from FR-029 (REQ-027-026). (REQ-006-030)
4. Patient confirms and submits payment.
5. Payment Service authorizes and captures deposit (or schedules installments).
6. System sets booking to Confirmed, unmasking patient identity to provider per constitution.
7. System creates the appointment record (`schedules`) from the held slot, converts the hold into a provider calendar block, and displays booking details in provider dashboard.
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
  3. While that hold is active, the slot remains reserved; patient can retry payment from the Accepted Subquote view. Ahead of expiry the system sends the patient the `booking.hold_expiring_soon` reminder at the lead time set in FR-026 (REQ-006-036), whether or not a payment has failed.
  4. If no payment succeeds before the hold expires, system releases the hold and blocks further payment against that slot. The booking record created at acceptance stays and moves to `Payment Window Expired`; the appointment record (`schedules`) was never created, because it is created only at the first successful payment. The FR-005 AcceptanceEvent and accepted snapshot remain immutable; the system MUST NOT reopen the parent quote or make the accepted subquote selectable again. Recovery follows the Payment Window Expired recovery route (see Payment & Billing Rules).
  5. System sends the mandatory Payment Window Expired notice to the patient and the provider (the provider learns the slot is free).
- **Outcome**: Booking transitions to `Payment Window Expired`; the hold is released, payment against that accepted selection is blocked, and both parties are notified. The FR-005 AcceptanceEvent and snapshot remain immutable; the prior parent quote and accepted subquote are not reopened. The patient contacts support; an admin either revives the booking (Screen 7) or cancels it (Alternative Flow B2, Screen 9), after which the patient may start a new inquiry.
- **Provider no longer eligible**: A `Payment Window Expired` booking is not touched by the provider-status cascade (Alternative Flow B4; FR-015 leaves it unchanged), and the provider-fault transfer (B5) starts only from `Accepted` or `Confirmed`. If its provider is suspended or deactivated, revive is blocked (REQ-006-020) and no replacement is offered for that booking: the admin cancels it through B2 and the patient starts a new inquiry.
- **Boundary**: B1 and `Payment Window Expired` apply only to the first payment step (acceptance to deposit or first installment). A missed later installment or final payment never causes `Payment Window Expired` or inquiry cancellation; it is handled by FR-007 and FR-007B. The one exception is the unpaid balance of a booking paid with the Installments option on Screen 1 (the "deposit plan" of REQ-006-016 and FR-029): when that balance is still unpaid at the cancellation point set in FR-029, counted in days after the due date of the first missed installment, the booking is cancelled through Alternative Flow B8. The rule is inactive until an admin sets that point in FR-029, which has no default, and it applies only to bookings confirmed after the value is set.

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
- **Allowed source states**: `Accepted`, `Payment Window Expired`, and `Confirmed` from the Cancel Booking action on Screen 6, and `In Progress` only through the Cancel route of Alternative Flow B7 (Screen 11 opens Screen 9). The action is not offered in `In Progress` or `Aftercare`; those stages use Screen 11 and Alternative Flow B6. `Cancelled` and `Completed` are terminal and cannot be cancelled again. (REQ-006-052)
- **Steps**:
  1. Admin opens Cancel Booking on Screen 6, which opens Screen 9, selects the request source (patient request through support, or admin decision), and enters a mandatory reason.
  2. Admin confirms the cancellation in a confirmation dialog that states the effects below.
  3. System transitions the booking to `Cancelled` with the admin's reason as the cancellation reason and the inquiry to `Cancelled`. The accepted parent quote stays `accepted` for history. The AcceptanceEvent and accepted snapshot stay unchanged; no supersession record is written.
  4. System releases any active hold or calendar block and blocks further payment against the accepted selection. (REQ-006-051)
  5. System writes an audit entry (admin, timestamp, source state, request source, reason) and sends `booking.cancelled` to the patient and the provider, including the cancellation reason.
  6. The refund follows REQ-006-053: a full refund with no cancellation fee when the provider withdraws, drops out, or is suspended or deactivated before treatment starts (Alternative Flows B4 and B5); the amount the admin set on Screen 11 when Screen 9 is opened from Alternative Flow B7 (the refund ladder does not apply); every other cancellation follows the refund ladder set in FR-029. A closure starts one refund only: the automatic refund and the admin action Process Refund on Screen 6 exclude each other (REQ-006-083). The refund step, its event, and the other money mechanics are owned by FR-007, FR-007B, and FR-017.
  7. The patient sees the cancellation fee and the refund in the support reply to the cancellation request; nothing forces the admin to include them.
- **Outcome**: Booking and inquiry are `Cancelled`; the accepted quote stays `accepted`; the action is audited; the slot is released back to the provider calendar.
- **Pending provider fault**: When an admin cancels a booking whose provider fault is still pending (the marker is set at the B5 trigger and the booking is not yet cancelled), the cancellation takes the cause `ProviderFault`, the full refund and no cancellation fee, whatever request source the admin selects, and the Screen 9 submit resolves the marker with an audited resolution. (REQ-006-081)
- **Patient account suspension**: When an admin suspends a patient account (FR-016), the suspension cascade cancels each of the patient's `Accepted`, `Payment Window Expired` and `Confirmed` bookings through this flow with the cause "Patient account suspended", request source Admin, and the acting admin carried from FR-016; the patient and the provider receive the fixed reason "Booking cancelled because the patient account was suspended", and the admin justification stays in the audit entry only. The refund follows the refund ladder set in FR-029, or the provider-fault terms where the provider is at fault (REQ-006-084, REQ-016-219).
- **Boundary**: Provider withdrawal of the accepted quote or provider drop-out after acceptance follows Alternative Flow B5, a provider fault while the booking is `In Progress` follows Alternative Flow B7, and a provider fault in the `Aftercare` stage follows Alternative Flow B6, not this flow, except for the pending-fault cancellation above. B2 is also the cancel route an admin chooses in Alternative Flow B7.

**B4: Provider Suspended or Deactivated (Admin-Initiated Cascade)**:

- **Trigger**: The provider's `Suspended` or `Deactivated` status becomes effective under [FR-015 Alternative Flow A5 and Screen 4](../fr015-provider-management/prd.md#screen-4-provider-suspensiondeactivation-modal).
- **Steps**:
  1. Every non-terminal booking of that provider before treatment starts (`Accepted` including unpaid within the payment hold, and `Confirmed`) transitions to `Cancelled` with cancellation cause `ProviderSuspended` or `ProviderDeactivated` and an independent `supportRequired` marker. The provider-status event itself authorizes the cascade; no per-booking approval is required. A booking in `In Progress` is not cancelled: it stays `In Progress`, receives the cause and the `supportRequired` marker, and follows Alternative Flow B7. A booking in `Aftercare` is not cancelled: it stays `Aftercare`, receives the cause and the `supportRequired` marker, and follows Alternative Flow B6. A `Payment Window Expired` booking is not part of the cascade (see the B1 "Provider no longer eligible" note).
  2. For each cancelled booking, System immediately releases any active appointment hold, reservation, or confirmed calendar slot and blocks further payment against the accepted selection, even if the original hold had time remaining. For a `Confirmed` booking the same step starts the full refund (REQ-006-053) and the cancellation of the remaining installments through FR-007 and FR-007B, the same money outcome as the B5 closure.
  3. The FR-005 AcceptanceEvent, accepted snapshot, and booking/payment history are kept unchanged. The closure is recorded on the booking as its cancellation cause; no supersession record is written at this point. The supersession record is written once, when the replacement acceptance is created in Alternative Flow B5.
  4. An admin rehomes each affected patient to a replacement provider in the same inquiry through the provider-fault transfer in Alternative Flow B5 (steps 4 to 6). The payment terms are the same as for a provider withdrawal or drop-out in Alternative Flow B5: the patient is refunded everything paid, pays no cancellation fee, and the replacement booking takes a new payment.
  5. Patient and admin notifications and the admin support handoff follow FR-015 Screen 4; FR-006 does not send a patient-cancellation or payment-retry message for these bookings. (REQ-006-055)
- **Outcome**: Bookings before treatment starts are cancelled with a provider-status cause, flagged for admin support, and rehomed by admin through Alternative Flow B5 in the same inquiry; `In Progress` bookings keep their status and wait for the admin decision in Alternative Flow B7; `Aftercare` bookings keep their status and move to aftercare reassignment through Alternative Flow B6.
- **Boundary**: B4 is the trigger for provider-status cases; the transfer itself follows B5, the `In Progress` decision follows B7, and the aftercare reassignment follows B6. Distinct from admin cancellation (B2/B3), provider-requested Cancel/Close Case (FR-010), and `Payment Window Expired` (B1). Provider reactivation never restores cancelled bookings, holds, or payment windows. A later deactivation does not overwrite an earlier `ProviderSuspended` cause.

**B5: Provider Fault After Acceptance (Admin Direct Transfer)**:

- **Trigger**: After subquote acceptance and before treatment starts (booking `Accepted` or `Confirmed`), the selected provider withdraws the accepted quote or drops out, or the provider's suspension or deactivation takes effect (entered from Alternative Flow B4). The transfer is limited to bookings before treatment starts: a provider fault while the booking is `In Progress` follows Alternative Flow B7, and a provider fault in the `Aftercare` stage follows Alternative Flow B6.
- **Steps**:
  1. At the trigger of a withdrawal or drop-out, System sets the `supportRequired` marker on the booking with the cause `ProviderFault`. The booking keeps its status. The original booking is cancelled at the admin submit on Screen 10 (step 5), not at the trigger (REQ-006-058): the booking transitions to `Cancelled` with cancellation cause `ProviderFault` and the `supportRequired` marker, and the closure is recorded on the booking as its cause; no supersession record is written before the replacement acceptance. A booking entered from B4 is already `Cancelled` with `ProviderSuspended` or `ProviderDeactivated` and the marker (B4 step 1), so the submit does not cancel it again.
  2. While the fault is pending, from the trigger to the submit, the booking keeps its hold or calendar block and the hold does not expire, but the patient cannot pay: payment and payment reminders (including `booking.hold_expiring_soon`) are blocked, and revive on Screen 7 is blocked (REQ-006-081). At the submit System releases any active hold or calendar block of the original provider and blocks further payment against the original accepted selection. Everything the patient paid on the original booking is refunded in full (REQ-006-053).
  3. The original FR-005 AcceptanceEvent and accepted snapshot are kept unchanged as history.
  4. An admin opens Start Provider-Fault Transfer on Screen 6 (Screen 10), selects a replacement provider, and authors a replacement quote for that provider inside the same inquiry through [FR-004 Workflow 7](../fr004-quote-submission/prd.md#workflow-7-admin-replacement-quote-provider-fault-transfer) and [FR-004 Screen 8](../fr004-quote-submission/prd.md#screen-8-admin-replacement-quote-authoring). This admin-authored replacement quote is the only exception to the FR-004 rule that no new quote is created once an inquiry has an acceptance. The admin may adjust the package and price on the replacement quote; every field set by the admin is audited with a mandatory reason.
  5. The admin selects one option and one date-price row of the replacement quote and confirms. On that submit System first re-checks the status of the original booking: only `Accepted`, `Confirmed`, or a `Cancelled` booking that still carries the marker from B4 proceed, and a booking that has reached `In Progress` is not transferred and goes to Alternative Flow B7 (REQ-006-081). It then applies steps 1 and 2 to the original booking and creates a new admin-authored AcceptanceEvent that points to that replacement quote, option, and date-price row like any other acceptance, so price, promotion, commission, and the acceptance snapshot work unchanged. In the same transaction System writes the single supersession record owned by FR-005 that links the closed original AcceptanceEvent to the new one (append-only single insert, cause taken from the original booking), and acquires the slot hold for the replacement appointment. The patient re-enters nothing.
  6. A replacement booking is created from the new acceptance and follows the main flow from that record: the patient pays on Screen 1 within the new hold, and the hold-expiring reminder and the Payment Window Expired path of Alternative Flow B1 apply to it like any other booking.
  7. Notifications: when the provider withdraws, FR-004 sends the mandatory `quote.withdrawn` notice and FR-006 does not send it again. When the provider drops out, the cancellation at step 1 sends the patient and the provider `booking.cancelled` with the provider-fault cause. A B4 closure is announced through FR-015 Screen 4 (REQ-006-055). The patient and admin are notified of the transfer through `booking.provider_fault_replacement` (FR-020 and FR-030). The replacement acceptance sends the patient the mandatory `booking.scheduled` notice with the replacement payment deadline, and the replacement provider learns of the booking through `quote.accepted` (outcome `selected_subquote_accepted`). The original provider is not notified by these events.
  8. Travel carries over through FR-008 only when the replacement booking's travel path (A or B) matches the original's: when the replacement booking's travel context is created, the patient's passport record carries over to it, and the flight and hotel records are copied to it and flagged "travel-date review required" for admin review. When the paths differ, nothing is carried over or copied and the replacement's own initial travel requests go out. The original travel records stay read-only on the closed booking, and the patient re-enters nothing that was carried over. (REQ-006-057)
- **Replacement quote not accepted**: If the admin does not record a replacement acceptance, the replacement quote expires under the normal FR-004 quote expiry, and FR-004 sends the `quote.expired` notice to the patient, so the patient is not left without word. FR-006 sends nothing more at that point. The inquiry stays flagged `supportRequired` and is not cancelled automatically. The admin may author another replacement quote through FR-004 Screen 8, or, when the booking is already `Cancelled` and still carries the marker, close the inquiry with the Close inquiry action on Screen 6: it sets the inquiry to `Cancelled`, clears the marker with an audited resolution, and sends the patient the admin-close variant of `inquiry.cancelled` (REQ-020-076) saying that no replacement will follow (REQ-006-082). A booking not yet cancelled (a pending fault) is cancelled through Alternative Flow B2 (Screen 9), which also cancels the inquiry.
- **Payment terms**: When the provider withdraws or drops out (cause `ProviderFault`), the patient is refunded everything paid and the replacement booking takes a new payment; the patient pays no cancellation fee because the fault is not theirs. The clinic is charged a fixed amount set by the admin, with no default value, deducted from its next payout. The patient-side terms also apply to the provider-status cancellation entered from B4 (Payment & Billing Rules, Provider-Status Cancellation); the clinic charge in this bullet is set for withdrawal or drop-out only and is not extended to B4. The in-treatment fault (B7) follows its own admin-set refund (REQ-006-053). Exact refund, fund-release, and payment-allocation override mechanics are defined in FR-007, FR-007B, and FR-017.
- **Outcome**: The patient keeps the same inquiry and moves to a replacement provider without a new patient acceptance. Every admin action in the transfer is audited.
- **Boundary**: For provider suspension or deactivation, Alternative Flow B4 is the trigger and closes the booking; this flow owns the transfer. Distinct from admin cancellation (B2/B3), aftercare reassignment (B6), the `In Progress` provider-fault decision (B7), and `Payment Window Expired` (B1).

**B6: Provider Fault During Aftercare (Aftercare Reassignment)**:

- **Trigger**: While the booking is `Aftercare` (treatment done), the provider withdraws or drops out of aftercare, or the provider's suspension or deactivation takes effect (entered from Alternative Flow B4).
- **Steps**:
  1. The booking stays `Aftercare` and the treatment record stays unchanged. No new quote, no new acceptance, and no new payment are created, and the AcceptanceEvent is not superseded. (REQ-006-056)
  2. When entered from B4, the booking carries the provider-status cause and the `supportRequired` marker; the original provider loses aftercare actions on the case. (REQ-006-056)
  3. An admin opens Reassign Aftercare on Screen 6, which links to the FR-011 aftercare reassignment screen, and reassigns the aftercare case to another provider or to the Hairline aftercare team, with a mandatory reason, confirmation, and audit entry, following FR-011.
  4. The admin's reassignment resolves the `supportRequired` marker with an audited resolution.
- **Outcome**: The patient continues aftercare with the new provider or team on the same booking.
- **Boundary**: The provider-fault transfer with a new acceptance (B5) applies only before treatment starts. Aftercare plan, milestone, and notification details are owned by FR-011.

**B7: Provider Fault While In Progress (Admin Decision)**:

- **Trigger**: While the booking is `In Progress` (after Check In and before treatment completion), the provider withdraws or drops out, or the provider's suspension or deactivation takes effect (entered from Alternative Flow B4).
- **Steps**:
  1. The booking stays `In Progress` and is not cancelled automatically. System sets the `supportRequired` marker, records the cause (`ProviderFault`, or `ProviderSuspended` / `ProviderDeactivated` when entered from B4), and holds the provider's payout for the booking. No replacement quote and no replacement acceptance are created, and the AcceptanceEvent is not superseded.
  2. An admin opens Resolve In-Progress Provider Fault on Screen 6 (Screen 11) and decides case by case, with a mandatory reason, the patient refund amount, and a confirmation:
     - **Move to Aftercare and reassign**: System moves the booking from `In Progress` to `Aftercare`, closing the treatment early at the decision date, keeps the treatment record as recorded, and opens the FR-011 aftercare reassignment screen (FR-011 Screen 19), where the admin assigns a new aftercare provider or the Hairline aftercare team following Alternative Flow B6. The decision date is the aftercare start date handed to FR-011.
     - **Cancel the booking**: System opens Screen 9 and the admin cancels the booking through Alternative Flow B2; the booking and inquiry become `Cancelled` and the accepted quote stays `accepted`. Screen 9 shows the refund amount set on Screen 11 read-only, and the refund ladder does not apply to this cancellation.
  3. System writes an audit entry (admin, timestamp, cause, chosen route, refund amount, reason). The decision itself only records the choice: the `supportRequired` marker and the payout hold are resolved once, when the chosen route completes, by the Screen 9 submit for Cancel or the FR-011 Screen 19 submit for Move to Aftercare, with an audited resolution. If the admin leaves Screen 9 or Screen 19 unfinished, the booking stays flagged and the payout stays held.
  4. System applies the admin-set refund through FR-007: for Cancel at the Screen 9 submit, for Move to Aftercare at the Screen 11 submit.
- **Payment terms**: Because the treatment had already started, an admin reviews each case and sets the patient refund amount, from zero up to the full amount paid, with a mandatory reason and an audit entry. The provider's payout for that booking is held from the fault until the chosen route completes, and the admin-set refund comes out of that held payout. If the payout was already released, the shortfall becomes a clinic balance entry that is applied to the clinic's next payout and carried forward until recovered (REQ-017-191). These terms apply to either resolution route and to every cause, including a cause entered from B4. Exact refund and fund-release mechanics are defined in FR-007, FR-007B, and FR-017.
- **Outcome**: The patient either continues on the same booking in `Aftercare` with a new aftercare provider or team, or the booking and inquiry are `Cancelled` with the admin's reason.
- **Boundary**: The provider-fault transfer with a new acceptance (B5) is never used for an `In Progress` booking. Distinct from the provider-requested Cancel/Close Case in FR-010; when the provider is not at fault, the admin closes that case early through Alternative Flow B9.

**B8: Unpaid Balance Cancellation (System)**:

- **Trigger**: A `Confirmed` booking paid with the Installments option on Screen 1 still has an unpaid balance at the cancellation point set in FR-029 (REQ-006-016): a number of days after the due date of the first missed installment. FR-029 gives that point no default, so this flow does not run until an admin sets it, and it applies only to bookings confirmed after the value is set; an unset value means no automatic cancellation.
- **Steps**:
  1. System transitions the booking to `Cancelled` with closure cause `UnpaidBalance` and the inquiry to `Cancelled`, as in B2. The accepted parent quote stays `accepted`, and the AcceptanceEvent and snapshot stay unchanged; no supersession record is written.
  2. System releases the calendar block and blocks further payment against the accepted selection (REQ-006-062). No `supportRequired` marker is set, because the cause is not a provider fault.
  3. System sends `booking.cancelled` to the patient and the provider with the cause (REQ-006-011).
  4. System voids the remaining unpaid installments through FR-007B, so no further installment is charged.
  5. The refund follows the refund ladder set in FR-029; the refund step and the other money mechanics are owned by FR-007, FR-007B, and FR-017.
- **Outcome**: The booking and inquiry are `Cancelled` without an admin action, and the slot returns to the provider's calendar.
- **Boundary**: Only the unpaid-balance case of REQ-006-016 runs here. A missed installment before that point is handled by FR-007 and FR-007B and never cancels the booking. Admin cancellation stays in B2.

**B9: Early Close of an In Progress Case With No Fault (Admin Decision)**:

- **Trigger**: An `In Progress` case cannot be completed and the provider is not at fault (patient stops, medical stop, no-show found after Check In, operational failure), usually flagged by the provider through Cancel/Close Case in FR-010 (REQ-010-079). The booking carries no `supportRequired` marker.
- **Steps**:
  1. An admin opens Close Case Early, No Fault on Screen 6, which opens Screen 11 with the route Move to Aftercare, no fault, and enters the patient refund amount (zero up to the full amount paid), a mandatory reason and a confirmation.
  2. On submit, System moves the booking from `In Progress` to `Aftercare` from the decision date (the aftercare start date handed to FR-011), records the closure cause `NoFaultEarlyClose`, sets no `supportRequired` marker and holds no payout, and writes an audit entry (admin, timestamp, cause, route, refund amount, reason).
  3. System applies the admin-set refund through FR-007 as an exception refund that follows the FR-007 approval rule, taken from what the patient paid; the provider's share (what is left after the refund and the Hairline commission) becomes eligible for payout on the decision date with no waiting window.
  4. System signals FR-010 to set the treatment record to Closed Early (stopping documentation reminders and the Overdue Documentation flag) and FR-011 so the aftercare team writes the post-op instructions; the admin never fills the clinic's End of Treatment fields (FR-010 Rule 17, REQ-010-116).
- **Outcome**: The patient continues on the same booking in `Aftercare`, and the Early Close Note shows on the patient booking detail (REQ-006-085).
- **Boundary**: Not used for a provider fault (B7), and not a cancellation: Cancel Booking is never offered in `In Progress` (REQ-006-052).

---

## Screen Specifications

### Patient Platform

#### Screen 1: Payment & Booking Confirmation (Patient)

**Purpose**: Review the accepted subquote and inherited parent context, view its pre-scheduled appointment slot, and proceed to payment without reselection

**Note**: This screen is accessed directly from FR-005's Accepted Subquote detail view. The FR-005 acceptance snapshot is the authoritative read-only source.

**Data Fields** (Continuation from FR-005):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Parent Quote Reference | text | Yes | Accepted parent quote identifier and version | Read-only; from AcceptanceEvent | ENT-booking.accepted_parent_quote_id, ENT-booking.accepted_parent_quote_version |
| Accepted Subquote Reference | text | Yes | Accepted subquote identifier and version | Read-only; from AcceptanceEvent; version MUST equal the accepted parent quote version | ENT-booking.accepted_subquote_id, ENT-booking.accepted_subquote_version |
| Accepted Selection Summary | group | Yes | Package, services, date range, appointment, price, promotion, and treatment plan plus inherited treatment context | Read-only; from acceptance snapshot | ENT-booking.acceptance_snapshot |
| Pre-Scheduled Appointment | datetime | Yes | Appointment selected by the accepted subquote | Read-only; the booking's current appointment (the accepted appointment unless an admin changed it on Screen 8) | ENT-booking.hold_appointment_at, ENT-booking.hold_appointment_timezone |
| Provider Name | text | Yes | Provider/clinic name | Read-only; inherited parent context | ENT-provider.name |
| Treatment Type | text | Yes | Accepted treatment and technique context | Read-only; inherited parent snapshot | ENT-quote.treatment_id |
| Estimated Graft Count | number | Yes | Accepted graft estimate | Read-only; inherited parent snapshot | ENT-quote.estimated_grafts |
| Clinician Assigned | text | Yes | Clinician attached to the accepted parent quote | Read-only; inherited parent snapshot | ENT-quote.clinician_ids |
| Provider Notes | text | No | Provider notes attached to the accepted parent quote | Read-only; inherited parent snapshot | ENT-quote.common_notes |
| Visual Plan | link/viewer | No | Accepted visual treatment plan | Read-only; inherited parent snapshot | ENT-quote.graft_visual_plan |
| Provider Requirements | group | No | Provider requirements attached to the accepted parent quote | Read-only; inherited parent snapshot | ENT-quote.common_requirements |
| Quote Attachments | links | No | Documents and media attached to the accepted parent quote | Read-only; inherited parent snapshot | ENT-quote.attachment_ids |
| Parent Quote Expiry | datetime | Yes | Expiry captured when the subquote was accepted | Read-only; inherited parent snapshot | ENT-quote.expires_at |
| Acceptance Audit Context | group | Yes | AcceptanceEvent reference, actor, timestamp, and source aggregate version | Read-only; from AcceptanceEvent and acceptance snapshot | ENT-acceptance-event.id, ENT-acceptance-event.accepted_at, ENT-acceptance-event.actor_id |
| Total Amount | number | Yes | Booking total: the accepted price after promotion | Read-only; from acceptance snapshot | ENT-subquote.price_after_promotion |
| Deposit Amount | number | Yes | Deposit from the FR-029 calculation | Read-only; within the bounds set in FR-029 | ENT-booking.deposit_amount |
| Deposit Percentage | text | Yes | Display deposit percentage used | Read-only; for transparency | ENT-booking.deposit_percentage |
| Remaining Balance | number | Yes | Total - Deposit | Calculated automatically (REQ-006-070) | ENT-booking.remaining_balance |
| Payment Option | select | Yes | Full payment or Installments (2–9) | Feasible installment options based on FR-029 split payment settings and FR-007B schedule rules (completion ≥30 days before procedure) | ENT-booking.payment_option |
| Installment Plan | select | Conditional | Number of installments if selected | Only shown if installment option selected (REQ-006-075) | ENT-booking.installment_count |
| Currency | text | Yes | Payment currency and locked exchange-rate context | Read-only; from acceptance snapshot | ENT-quote.currency_snapshot, ENT-quote.locked_exchange_rate_snapshot |
| Travel | link | Conditional | Entry to the FR-008 Travel Itinerary View (FR-008 Screen 5); it also leads to the passport, flight and hotel submission screens while an item is pending. FR-006 hosts the entry and FR-008 owns what it opens | Shown when travel is available for the booking (REQ-006-042) | no graph field (control) |
| Cancellation Policy | link | Yes | Link to the full Cancellation Policy document (FR-027, informational); the refund schedule numbers shown with it are the refund ladder set in FR-029, and the document does not restate them (REQ-027-026) | Read-only; admin-configured | no graph field |
| Cancellation Policy Ack | checkbox | Yes | User acknowledges policy; the Cancellation Policy version shown at the tick is stored with it | Must be checked before payment; the stored version is the published version the full policy link showed at the tick (REQ-006-038) | ENT-booking.cancellation_policy_acknowledged_at, ENT-booking.cancellation_policy_version_shown |
| Terms & Conditions Ack | checkbox | Yes | User acknowledges T&C | Must be checked before payment | ENT-booking.terms_acknowledged_at |
| Contact Support | button | Yes | Opens a support request to cancel or change the booking | Always shown; there is no in-app cancel action after acceptance | no graph field (control) |

**Blocked State (Inquiry Cancelled, Payment Window Expired, Booking Cancelled, or Provider Fault Pending)**:

If pre-booking validation fails (parent inquiry cancelled, by the patient before acceptance per FR-003 Workflow 5 or by an admin after acceptance), the booking is `Payment Window Expired` or `Cancelled`, or the booking carries a pending provider fault (Alternative Flow B5, REQ-006-081), this screen displays a read-only blocked state instead of the payment form:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Blocked Banner | banner | Yes | One text per cause: inquiry cancelled, "This inquiry has been cancelled. Booking is no longer available."; payment window expired, "The payment window for this booking has expired. Contact support to restore or cancel it."; cancelled by admin, "This booking has been cancelled" with the cancellation reason; provider withdrawal, fault, suspension or deactivation, including while the fault is pending, "Your provider can no longer take this booking. Hairline support will contact you about the next steps."; unpaid balance, "This booking was cancelled because the remaining balance was not paid by the due date." | Full-width, prominent styling; the text follows the booking status and closure cause (REQ-006-037) | ENT-booking.closure_cause |
| Accepted Selection Summary | group | Yes | Accepted subquote and inherited parent context | Read-only; greyed out | ENT-booking.acceptance_snapshot |
| Status Changed At | datetime | Yes | When the booking reached its present status; for an inquiry cancellation, when the inquiry was cancelled | Read-only; from the booking status history, or from the inquiry for an inquiry cancellation | ENT-booking.status_history, ENT-inquiry.cancelled_at |
| Contact Support | button | Yes | Opens a plain support request that carries the booking reference and has no request type; the patient says in the message whether to restore or cancel the booking or to ask about the refund | Shown for every cause; for an expired window it is the recovery route (REQ-006-005); only booking cancellation and booking change requests carry a request type (REQ-034-182, REQ-034-167) | no graph field (control) |
| Back to Dashboard | button | Yes | Returns patient to Inquiry Dashboard (FR-003 Screen 8) | Always enabled | no graph field (control) |

All payment fields and payment actions are hidden. Patient can view the blocked state, contact support, and navigate back.

**Business Rules**:

- All accepted subquote and inherited parent details from the FR-005 acceptance snapshot are displayed read-only.
- Appointment is already selected by the accepted subquote and its slot is held for payment; no selection is available here. The booking is confirmed only after successful payment.
- If parent inquiry is in "Cancelled" status, screen enters blocked state (see above) — payment form is hidden, blocked banner is displayed.
- If the booking is `Payment Window Expired`, carries a pending provider fault, or is `Cancelled` for any other cause (provider withdrawal or fault, provider suspension or deactivation), the screen shows the same read-only blocked layout with the banner text of that cause and the Contact Support button; all payment fields and payment actions are hidden. The Contact Support button opens a plain support request with the booking reference and no request type (REQ-034-182). (REQ-006-037)
- Deposit amount comes from the FR-029 calculation (REQ-029-016); FR-006 does not restate the percentage or the formula. The cancellation policy is presented through the full Cancellation Policy link (FR-027), with the refund ladder numbers from FR-029 (REQ-027-026). (REQ-006-030)
- Disable Pay button until all required acknowledgments (cancellation policy, T&C) are checked; the Cancellation Policy version shown at the tick is stored on the booking with the acknowledgment time. (REQ-006-038)
- The payment breakdown shown before payment (total amount, deposit amount, remaining balance, currency) is owned by FR-007 (REQ-007-033); FR-006 cites it and does not restate it.
- Display time zone relative labels and local time conversions for appointment slot.
- If installment plan selected, show installment schedule and completion date (must be ≥30 days before procedure).
- Only show installment options returned as feasible per FR-029 configuration + FR-007B schedule rules; if none are feasible, allow Pay-in-Full only with a clear explanation. (REQ-006-033)

**Notes**:

- This screen is a continuation of FR-005's Accepted Subquote flow.
- Package, date range, appointment, and price cannot be changed or reselected here.
- The full Cancellation Policy document is informational (FR-027) and opens from the Cancellation Policy link; its refund ladder numbers come from FR-029 and the document does not restate them. (REQ-006-030)

---

#### Screen 2: Booking Confirmation & Itinerary (Patient)

**Purpose**: Display confirmed booking, reference number, next steps, basic itinerary

**Data Fields** (Continuation from Screen 1):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Booking Reference | text | Yes | Unique booking reference number | Format per HPID/booking scheme | ENT-booking.booking_reference |
| Booking Status | badge | Yes | Current booking status: `Confirmed` right after payment, then `In Progress`, `Aftercare` or `Completed` as the booking advances | Read-only; the screen is reachable in these four statuses | ENT-booking.status |
| Early Close Note | group | Conditional | Status note "Treatment closed early" with the decision date and, when a refund greater than zero was issued, the refund amount | Read-only; shown only when the treatment record is Closed Early (booking in `Aftercare` or `Completed`); a zero or absent refund shows no amount line; no action and no new status (REQ-006-085) | ENT-treatment-record.status, ENT-booking.status_history, ENT-booking.refund_history |
| Parent Quote Reference | text | Yes | Accepted parent quote identifier/version | Read-only; from AcceptanceEvent | ENT-booking.accepted_parent_quote_id, ENT-booking.accepted_parent_quote_version |
| Accepted Subquote Reference | text | Yes | Accepted subquote identifier/version | Read-only; from AcceptanceEvent | ENT-booking.accepted_subquote_id, ENT-booking.accepted_subquote_version |
| Provider Name | text | Yes | Provider/clinic name | Read-only; inherited parent context | ENT-provider.name |
| Provider Contact | group | Yes | Clinic address, phone, email | Read-only; unmasked after payment | ENT-provider.address, ENT-provider.phone, ENT-provider.email |
| Procedure Date | datetime | Yes | Confirmed appointment slot | Read-only; the booking's current appointment (the accepted appointment unless an admin changed it on Screen 8) | ENT-booking.hold_appointment_at |
| Procedure Time | time | Yes | Appointment start time | Read-only; the booking's current appointment (the accepted appointment unless an admin changed it on Screen 8) | ENT-booking.hold_appointment_at |
| Treatment Type | text | Yes | Inherited treatment name (FUE, FUT, etc.) | Read-only; from parent snapshot | ENT-quote.treatment_id |
| Total Amount | number | Yes | Total booking amount | Read-only; from accepted subquote snapshot | ENT-subquote.price_after_promotion |
| Currency | text | Yes | Currency of the accepted price | Read-only; from acceptance snapshot | ENT-quote.currency_snapshot |
| Deposit Paid | number | Yes | Deposit amount paid | Read-only; from payment | ENT-booking.deposit_amount |
| Payment Status | badge | Yes | The single "Payment status" owned by FR-007: Unpaid, Deposit only, Installments active, Full paid, Refunded; At Risk is not a status and Overdue is a calculated flag, not a value (REQ-007-099) | Must reflect latest payment state; read from FR-007 | ENT-booking.payment_status |
| Remaining Balance | number | Yes | Amount remaining to pay | Calculated automatically | ENT-booking.remaining_balance |
| Next Payment Due | datetime | Conditional | Next installment due date | Only shown if installments active | ENT-booking.next_payment_due_at |
| Payment Method | text | Yes | Payment method used | Read-only; from payment | ENT-booking.payment_method |
| Cancellation Policy | link | Yes | Link to full cancellation policy | Read-only | no graph field |
| Contact Support | button | Yes | Opens a support request for cancellation or other booking changes | Always shown; there is no in-app cancel action after acceptance | no graph field (control) |

**Business Rules**:

- Trigger notifications to patient/provider upon display.
- Display all booking details clearly with appointment slot prominently shown.
- Show payment status and next steps (if installments, show schedule).
- Provide "Add to Calendar" functionality (ICS file download). (REQ-006-041)
- Link to travel booking (FR-008) when available: Screen 2 carries a Travel entry that opens the FR-008 patient itinerary view, Screen 4 hosts the FR-008 provider Travel section once the booking is `Confirmed`, and Screen 6 hosts the FR-008 admin Travel section for every confirmed booking; FR-008 defines what each shows. (REQ-006-042)

**Notes**:

- This screen appears immediately after successful payment and stays the patient's booking detail while the booking is `Confirmed`, `In Progress`, `Aftercare` or `Completed`.
- All data continues from the accepted subquote snapshot and the payment record.
- Include provider contact information (now unmasked after payment confirmation). (REQ-006-040)

---

### Provider Platform

#### Screen 3: Bookings Dashboard (Provider)

**Purpose**: View accepted and confirmed bookings in table list format; monitor booking status and payment state

**Note**: Provider dashboard uses table list format only (no calendar view). This is consistent with previous FRs (FR-004, FR-005) which use table-based interfaces.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Booking Reference | text | Yes | Unique booking reference | Sortable, filterable | ENT-booking.booking_reference |
| Patient Name | text | Yes | Anonymized (e.g., "Mark P. - PAT-00123") or full name once the booking has reached `Confirmed` | Unmask once the booking has reached `Confirmed`; stays unmasked afterwards, including after a later cancellation | ENT-patient.name |
| Patient Code | text | Yes | Patient identifier | Read-only | ENT-patient.anonymized_id |
| Inquiry Reference | text | Yes | Original inquiry HPID | Link to inquiry details | ENT-inquiry.reference |
| Accepted Subquote Reference | text | Yes | Accepted subquote identifier | Link to accepted selection details | ENT-booking.accepted_subquote_id |
| Parent Quote Reference | text | Yes | Source parent quote identifier | Link to parent quote audit details | ENT-booking.accepted_parent_quote_id |
| Booking Status | badge | Yes | Accepted / Payment Window Expired / Confirmed / In Progress / Aftercare / Completed / Cancelled | Filterable by status | ENT-booking.status |
| Appointment Date | datetime | Yes | Pre-scheduled appointment slot | Sortable by date | ENT-booking.hold_appointment_at |
| Treatment Type | text | Yes | Treatment name | Filterable | ENT-quote.treatment_id |
| Total Amount | number | Yes | Accepted price and currency | Sortable; from acceptance snapshot | ENT-subquote.price_after_promotion |
| Deposit Status | badge | Yes | Pending / Paid / Partial | Filterable | ENT-booking.deposit_status |
| Deposit Amount | number | Yes | Deposit amount (if paid) | Read-only | ENT-booking.deposit_amount |
| Payment Status | badge | Yes | The single "Payment status" list owned by FR-007 | Read-only; read from FR-007 | ENT-booking.payment_status |
| Created Date | datetime | Yes | Booking creation timestamp | Sortable | ENT-booking.created_at |
| Actions | buttons | Yes | View Details, Check In (when the FR-010 Check In rule allows it) | RBAC enforced | no graph field (control) |

**Business Rules**:

- Table list format only (no calendar view). (REQ-006-022)
- Auto-block appointment slot upon booking confirmation (enforced at database level). (REQ-006-068)
- Patient identity remains masked until the booking has reached `Confirmed` (payment success). Once unmasked it stays visible through `In Progress`, `Aftercare`, `Completed`, and a later `Cancelled`, because treatment, support, and records need it. A booking cancelled before it ever reached `Confirmed` stays masked. (REQ-006-008)
- Filtering options: Status, Date Range, Treatment Type, Payment Status. (REQ-006-044)
- Sorting options: Date, Amount, Status, Created Date. (REQ-006-044)
- Clicking on booking row opens booking detail view (Screen 4). (REQ-006-076)
- FR-005 prevents a second acceptance from acquiring a slot already held or blocked by another pending or confirmed booking. FR-006 revalidates exclusive hold ownership before payment initiation and, after successful payment, atomically creates the appointment record and converts that hold into the confirmed calendar block.

**Notes**:

- Consistent with provider interface patterns from FR-004 and FR-005.
- Show payment summary figures without revealing card details. (REQ-006-046)
- Appointment slot blocking is automatic and enforced - no manual calendar management needed.

---

#### Screen 4: Booking Detail View (Provider)

**Purpose**: View complete booking details with full context from inquiry, parent quote, accepted subquote, acceptance, and booking stages

**Data Fields** (Continuation from Screen 3, aggregating data from FR-003, FR-004, FR-005, FR-006):

**Section 1: Booking & Scheduling Information** (from FR-006):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Booking Reference | text | Yes | Unique booking reference | Read-only | ENT-booking.booking_reference |
| Booking Status | badge | Yes | Current status (Accepted/Payment Window Expired/Confirmed/In Progress/Aftercare/Completed/Cancelled) | Read-only | ENT-booking.status |
| Booking Created Date | datetime | Yes | Booking creation timestamp | Read-only | ENT-booking.created_at |
| Appointment Date | datetime | Yes | Appointment slot | Read-only; the booking's current appointment (the accepted appointment unless an admin changed it on Screen 8) | ENT-booking.hold_appointment_at |
| Appointment Time | time | Yes | Appointment start time | Read-only | ENT-booking.hold_appointment_at |

**Section 2: Patient Information** (from FR-003, unmasked once the booking has reached `Confirmed`):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Patient Anonymized ID | text | Yes | Patient code (always visible) | Read-only | ENT-patient.anonymized_id |
| Patient Name | text | Conditional | Full name (once the booking has reached `Confirmed`) or masked (e.g., "Mark P. - PAT-00123") | Unmask once the booking has reached `Confirmed`; stays unmasked afterwards, including after a later cancellation | ENT-patient.name |
| Patient Email | text | Conditional | Email address (once the booking has reached `Confirmed`) | Unmask once the booking has reached `Confirmed`; stays unmasked afterwards | ENT-patient.email |
| Patient Phone | text | Conditional | Phone number (once the booking has reached `Confirmed`) | Unmask once the booking has reached `Confirmed`; stays unmasked afterwards | ENT-patient.phone |
| Patient Location | text | Yes | Country/city | Read-only; from inquiry | ENT-patient.country, ENT-patient.city |
| Patient Age | number | Yes | Patient age | Read-only; from inquiry | ENT-patient.age |
| Patient Gender | text | Yes | Gender | Read-only; from inquiry | ENT-patient.gender |

**Section 3: Problem & Concern Information** (from FR-003):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Treatment Area Requested | text | Yes | The treatment area the patient requested | Read-only; from the inquiry treatment area snapshot | ENT-inquiry.treatment_area_snapshot |
| Problem/Concern Description | text | Yes | Patient's hair concern description | Read-only; from inquiry | ENT-inquiry.problem_concern |
| Duration of Concern | text | Yes | How long patient has had the concern | Read-only; from inquiry | ENT-inquiry.problem_duration |
| Previous Treatments | text | No | Previous treatments tried | Read-only; from inquiry | ENT-inquiry.previous_treatments |
| Symptom Severity | number | Yes | Severity rating (1-10) | Read-only; from inquiry | ENT-inquiry.symptom_severity |
| Lifestyle Factors | text | No | Relevant lifestyle information | Read-only; from inquiry | ENT-inquiry.lifestyle_factors |
| Additional Notes | text | No | Patient's additional notes | Read-only; from inquiry | ENT-inquiry.additional_notes |
| Media Files | links | No | Photos/videos uploaded by patient | Read-only; from inquiry | ENT-inquiry.media |
| 3D Scan | link/viewer | Yes | Link to patient 3D scan with viewer | Read-only; from inquiry | ENT-inquiry.scan_ref |

**Section 4: Medical Information** (from FR-003):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Medical Alerts | chips | Yes | Patient medical risk flags (Critical/Standard/None) | Read-only; color-coded | ENT-risk-tag.severity |
| Medical Questionnaire | link | Yes | Link to full medical questionnaire responses | Read-only; from inquiry | ENT-medical-questionnaire-response.answer |
| Allergies | text | No | Known allergies | Read-only; from questionnaire | ENT-medical-questionnaire-response.answer |
| Current Medications | text | No | Current medications | Read-only; from questionnaire | ENT-medical-questionnaire-response.answer |
| Chronic Conditions | text | No | Chronic health conditions | Read-only; from questionnaire | ENT-medical-questionnaire-response.answer |

**Section 5: Accepted Selection Information** (from FR-004 and FR-005):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Parent Quote Reference | text | Yes | Accepted parent quote identifier/version | Read-only; link to parent quote audit | ENT-booking.accepted_parent_quote_id, ENT-booking.accepted_parent_quote_version |
| Accepted Subquote Reference | text | Yes | Accepted subquote identifier/version | Read-only; link to AcceptanceEvent | ENT-booking.accepted_subquote_id, ENT-booking.accepted_subquote_version |
| Accepted Date | datetime | Yes | Subquote acceptance date | Read-only; from AcceptanceEvent | ENT-acceptance-event.accepted_at |
| Accepted Provider | text | Yes | Provider/clinic captured at acceptance | Read-only; inherited parent snapshot | ENT-booking.provider_id |
| Treatment Type | text | Yes | Selected treatment (FUE, FUT, DHI, etc.) | Read-only; inherited parent snapshot | ENT-quote.treatment_id |
| Estimated Graft Count | number | Yes | Estimated number of grafts | Read-only; inherited parent snapshot | ENT-quote.estimated_grafts |
| Technique Specifications | text | No | Technique details | Read-only; inherited parent snapshot | ENT-treatment.technique_details |
| Visual Plan | link/viewer | No | Accepted visual treatment plan | Read-only; inherited parent snapshot | ENT-quote.graft_visual_plan |
| Selected Package and Services | group | Yes | Exact package snapshot and included/custom services | Read-only; accepted subquote snapshot | ENT-subquote.package_snapshot, ENT-subquote.included_and_custom_services |
| Clinician Assigned | text | Yes | Clinician who will perform procedure | Read-only; inherited parent snapshot | ENT-quote.clinician_ids |
| Provider Notes | text | No | Provider's notes to patient | Read-only; inherited parent snapshot | ENT-quote.common_notes |
| Provider Requirements | group | No | Provider requirements attached to the accepted parent quote | Read-only; inherited parent snapshot | ENT-quote.common_requirements |
| Quote Attachments | links | No | Documents and media attached to the accepted parent quote | Read-only; inherited parent snapshot | ENT-quote.attachment_ids |
| Parent Quote Expiry | datetime | Yes | Expiry captured when the subquote was accepted | Read-only; inherited parent snapshot | ENT-quote.expires_at |
| Acceptance Audit Context | group | Yes | AcceptanceEvent reference, actor, timestamp, and source aggregate version | Read-only; from AcceptanceEvent and acceptance snapshot | ENT-acceptance-event.id, ENT-acceptance-event.accepted_at, ENT-acceptance-event.actor_id |
| Selected Date Range | date range | Yes | Accepted patient-requested range | Read-only; accepted subquote snapshot | ENT-subquote.date_range |
| Treatment Plan (per-day) | table | Yes | Day-by-day treatment plan shown as relative days (Day 1, Day 2...) | Read-only; accepted subquote snapshot; never converted to calendar dates | ENT-subquote.treatment_plan |

**Section 6: Pricing & Payment Information** (from FR-004, FR-006, FR-007):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Currency | text | Yes | Payment currency and locked exchange-rate context | Read-only; acceptance snapshot | ENT-quote.currency_snapshot |
| Offered Price | number | Yes | Offered price of the accepted subquote, as entered before any promotion | Read-only; acceptance snapshot | ENT-subquote.offered_price |
| Promotion Applied | group | No | Structured promotion included in the accepted price | Read-only; acceptance snapshot | ENT-subquote.promotion_snapshot |
| Accepted Price | number | Yes | Booking total: the accepted price after promotion | Read-only; acceptance snapshot | ENT-subquote.price_after_promotion |
| Deposit Percentage | text | Yes | Deposit percentage used | Read-only; admin-configured | ENT-booking.deposit_percentage |
| Deposit Amount | number | Yes | Deposit amount required/paid | Read-only | ENT-booking.deposit_amount |
| Deposit Status | badge | Yes | Pending/Paid/Partial | Read-only | ENT-booking.deposit_status |
| Deposit Paid Date | datetime | Conditional | Date deposit was paid | Read-only; if paid | ENT-booking.deposit_paid_at |
| Payment Method | text | Conditional | Payment method used | Read-only; if paid | ENT-booking.payment_method |
| Payment Status | badge | Yes | The single "Payment status" list owned by FR-007 | Read-only; read from FR-007 | ENT-booking.payment_status |
| Payment Schedule | table | Conditional | Installment schedule (if applicable) | Only shown if installments | ENT-booking.payment_schedule |
| Remaining Balance | number | Yes | Amount remaining to pay | Calculated | ENT-booking.remaining_balance |
| Final Payment Due Date | datetime | Conditional | Final payment due date | Read-only; if applicable | ENT-booking.final_payment_due_at |

**Section 7: Inquiry Context** (from FR-003):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Inquiry Reference | text | Yes | Original inquiry HPID | Read-only; link to inquiry | ENT-inquiry.reference |
| Requested Countries | list | Yes | Countries patient selected for treatment | Read-only; from inquiry | ENT-inquiry.treatment_countries |
| Requested Date Ranges | list | Yes | All date ranges patient requested | Read-only; from inquiry | ENT-inquiry-date-range.start_date, ENT-inquiry-date-range.end_date |

**Actions**:

| Action | Type | Condition | Description | Graph field |
|--------|------|-----------|-------------|-------------|
| Check In | button | Available only when the Check In rule owned by FR-010 allows it | Mark patient as arrived (handoff to FR-010) | no graph field (control) |
| View Inquiry | link | Always | Open full inquiry details (FR-003) | no graph field (control) |
| View Accepted Selection | link | Always | Open accepted subquote and AcceptanceEvent details (FR-005) | no graph field (control) |
| View Parent Quote | link | Always | Open source parent quote details (FR-004) | no graph field (control) |
| View 3D Scan | link | Always | Open 3D scan viewer | no graph field (control) |
| View Medical Questionnaire | link | Always | Open medical questionnaire | no graph field (control) |

**Business Rules**:

- Patient full identity is visible only once the booking has reached `Confirmed` (payment successful), and stays visible afterwards, including after a later cancellation.
- All booking data is read-only (cannot be edited by provider).
- The Check In button follows the Check In rule owned by FR-010 (a confirmed, fully paid booking); FR-006 does not restate its conditions.
- All sections display data from previous stages (inquiry → parent quote/subquote → acceptance → booking) in chronological order. (REQ-006-047)
- Links to the inquiry, accepted selection, and source parent quote provide full context and audit trail. (REQ-006-077)
- A collapsible Travel section sits at the bottom of this screen once the booking is `Confirmed`; FR-006 hosts it and FR-008 Screen 6 defines its content. (REQ-006-042)

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

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Booking Reference | text | Yes | Unique booking reference | Sortable, filterable, searchable | ENT-booking.booking_reference |
| Patient Name | text | Yes | Full patient name | Searchable | ENT-patient.name |
| Patient Email | text | Yes | Patient email | Searchable | ENT-patient.email |
| Provider Name | text | Yes | Provider/clinic name | Filterable | ENT-provider.name |
| Booking Status | badge | Yes | Accepted / Payment Window Expired / Confirmed / In Progress / Aftercare / Completed / Cancelled | Filterable | ENT-booking.status |
| Appointment Date | datetime | Yes | Appointment slot | Sortable, filterable by date range | ENT-booking.hold_appointment_at |
| Treatment Type | text | Yes | Treatment name | Filterable | ENT-quote.treatment_id |
| Total Amount | number | Yes | Accepted price and currency | Sortable; from acceptance snapshot | ENT-subquote.price_after_promotion |
| Deposit Status | badge | Yes | Pending / Paid / Partial | Filterable | ENT-booking.deposit_status |
| Payment Status | badge | Yes | The single "Payment status" list owned by FR-007 | Filterable; read from FR-007 | ENT-booking.payment_status |
| Created Date | datetime | Yes | Booking creation timestamp | Sortable | ENT-booking.created_at |
| Actions | buttons | Yes | View Details, Emergency Edit (appointment time on the same date and booking notes), Cancel (not offered in `In Progress` or `Aftercare`), Close inquiry, Process Refund | RBAC enforced; each action follows its condition on Screen 6 | no graph field (control) |

**Business Rules**:

- Full access to all booking data across all providers and patients.
- Search functionality: by booking reference, patient name, patient email, provider name. (REQ-006-045)
- Filtering: Status, Provider, Date Range, Treatment Type, Payment Status. (REQ-006-045)
- Admin can intervene in bookings only through the governed actions and the audited emergency edit of non-money booking details (REQ-006-074), with audit trail.
- Admin can process cancellations and refunds per policy.
- All admin actions require audit logging with reason/justification.

**Notes**:

- Admin has full visibility and the governed intervention actions, including the emergency edit, for dispute resolution.
- All actions are audited for compliance.

---

#### Screen 6: Booking Detail & Intervention (Admin)

**Purpose**: View complete booking details with full context from all stages, and perform administrative actions

**Data Fields** (Continuation from Screen 5, aggregating data from FR-003, FR-004, FR-005, FR-006):

**Section 1: Booking & Scheduling Information** (from FR-006):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Booking Reference | text | Yes | Unique booking reference | Read-only | ENT-booking.booking_reference |
| Booking Status | badge | Yes | Current status | Read-only; changed only through the governed intervention actions below (revive, cancel, provider-fault transfer, resolve an in-progress provider fault); never set by the emergency edit | ENT-booking.status |
| Closure Cause | text | Conditional | Why the booking was closed or is closing (`ProviderFault`, `ProviderSuspended`, `ProviderDeactivated`, `UnpaidBalance`, "Patient account suspended", `NoFaultEarlyClose`, or an admin cancellation) | Read-only; shown once a cause is recorded, including while a provider fault is pending | ENT-booking.closure_cause |
| Support Required | badge | Conditional | Whether the `supportRequired` marker is set (a marker, not a status) | Read-only; set at the provider-fault trigger or by the provider-status cascade; cleared only by an audited resolution | ENT-booking.support_required |
| Booking Created Date | datetime | Yes | Booking creation timestamp | Read-only | ENT-booking.created_at |
| Appointment Date | datetime | Yes | Current appointment slot | Read-only; changed only through Change Appointment (Screen 8) | ENT-booking.hold_appointment_at |
| Appointment Time | time | Yes | Current appointment start time | Read-only; changed through Change Appointment (Screen 8), or through the emergency edit for a different time on the same date | ENT-booking.hold_appointment_at |

**Section 2: Patient Information** (from FR-003, always visible to admin):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Patient ID | text | Yes | Patient code | Read-only | ENT-patient.anonymized_id |
| Patient Name | text | Yes | Full name | Read-only | ENT-patient.name |
| Patient Email | text | Yes | Email address | Read-only | ENT-patient.email |
| Patient Phone | text | Yes | Phone number | Read-only | ENT-patient.phone |
| Patient Address | text | No | Full address | Read-only; from profile | ENT-patient.address |
| Patient Location | text | Yes | Country/city | Read-only; from inquiry | ENT-patient.country, ENT-patient.city |
| Patient Age | number | Yes | Patient age | Read-only; from inquiry | ENT-patient.age |
| Patient Gender | text | Yes | Gender | Read-only; from inquiry | ENT-patient.gender |
| Patient Date of Birth | date | Yes | Date of birth | Read-only; from profile | ENT-patient.date_of_birth |

**Section 3: Problem & Concern Information** (from FR-003):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Treatment Area Requested | text | Yes | The treatment area the patient requested | Read-only; from the inquiry treatment area snapshot | ENT-inquiry.treatment_area_snapshot |
| Problem/Concern Description | text | Yes | Patient's hair concern description | Read-only; from inquiry | ENT-inquiry.problem_concern |
| Duration of Concern | text | Yes | How long patient has had the concern | Read-only; from inquiry | ENT-inquiry.problem_duration |
| Previous Treatments | text | No | Previous treatments tried | Read-only; from inquiry | ENT-inquiry.previous_treatments |
| Symptom Severity | number | Yes | Severity rating (1-10) | Read-only; from inquiry | ENT-inquiry.symptom_severity |
| Lifestyle Factors | text | No | Relevant lifestyle information | Read-only; from inquiry | ENT-inquiry.lifestyle_factors |
| Additional Notes | text | No | Patient's additional notes | Read-only; from inquiry | ENT-inquiry.additional_notes |
| Media Files | links | No | Photos/videos uploaded by patient | Read-only; from inquiry | ENT-inquiry.media |
| 3D Scan | link/viewer | Yes | Link to patient 3D scan with viewer | Read-only; from inquiry | ENT-inquiry.scan_ref |

**Section 4: Medical Information** (from FR-003):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Medical Alerts | chips | Yes | Patient medical risk flags (Critical/Standard/None) | Read-only; color-coded | ENT-risk-tag.severity |
| Medical Questionnaire | link | Yes | Link to full medical questionnaire responses | Read-only; from inquiry | ENT-medical-questionnaire-response.answer |
| Allergies | text | No | Known allergies | Read-only; from questionnaire | ENT-medical-questionnaire-response.answer |
| Current Medications | text | No | Current medications | Read-only; from questionnaire | ENT-medical-questionnaire-response.answer |
| Chronic Conditions | text | No | Chronic health conditions | Read-only; from questionnaire | ENT-medical-questionnaire-response.answer |
| Previous Surgeries | text | No | Previous surgical procedures | Read-only; from questionnaire | ENT-medical-questionnaire-response.answer |

**Section 5: Accepted Selection Information** (from FR-004 and FR-005):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Parent Quote Reference | text | Yes | Accepted parent quote identifier/version | Read-only; link to parent quote audit | ENT-booking.accepted_parent_quote_id, ENT-booking.accepted_parent_quote_version |
| Accepted Subquote Reference | text | Yes | Accepted subquote identifier/version | Read-only; link to AcceptanceEvent | ENT-booking.accepted_subquote_id, ENT-booking.accepted_subquote_version |
| Accepted Date | datetime | Yes | Subquote acceptance date | Read-only; from AcceptanceEvent | ENT-acceptance-event.accepted_at |
| Accepted Provider | text | Yes | Provider/clinic captured at acceptance | Read-only; inherited parent snapshot | ENT-booking.provider_id |
| Treatment Type | text | Yes | Selected treatment (FUE, FUT, DHI, etc.) | Read-only; inherited parent snapshot | ENT-quote.treatment_id |
| Estimated Graft Count | number | Yes | Estimated number of grafts | Read-only; inherited parent snapshot | ENT-quote.estimated_grafts |
| Technique Specifications | text | No | Technique details | Read-only; inherited parent snapshot | ENT-treatment.technique_details |
| Visual Plan | link/viewer | No | Accepted visual treatment plan | Read-only; inherited parent snapshot | ENT-quote.graft_visual_plan |
| Selected Package and Services | group | Yes | Exact package snapshot and included/custom services | Read-only; accepted subquote snapshot | ENT-subquote.package_snapshot, ENT-subquote.included_and_custom_services |
| Clinician Assigned | text | Yes | Clinician who will perform procedure | Read-only; inherited parent snapshot | ENT-quote.clinician_ids |
| Provider Notes | text | No | Provider's notes to patient | Read-only; inherited parent snapshot | ENT-quote.common_notes |
| Provider Requirements | group | No | Provider requirements attached to the accepted parent quote | Read-only; inherited parent snapshot | ENT-quote.common_requirements |
| Quote Attachments | links | No | Documents and media attached to the accepted parent quote | Read-only; inherited parent snapshot | ENT-quote.attachment_ids |
| Parent Quote Expiry | datetime | Yes | Expiry captured when the subquote was accepted | Read-only; inherited parent snapshot | ENT-quote.expires_at |
| Acceptance Audit Context | group | Yes | AcceptanceEvent reference, actor, timestamp, and source aggregate version | Read-only; from AcceptanceEvent and acceptance snapshot | ENT-acceptance-event.id, ENT-acceptance-event.accepted_at, ENT-acceptance-event.actor_id |
| Selected Date Range | date range | Yes | Accepted patient-requested range | Read-only; accepted subquote snapshot | ENT-subquote.date_range |
| Treatment Plan (per-day) | table | Yes | Day-by-day treatment plan shown as relative days (Day 1, Day 2...) | Read-only; accepted subquote snapshot; never converted to calendar dates | ENT-subquote.treatment_plan |

**Section 6: Provider Information** (from provider profile):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Provider Name | text | Yes | Provider/clinic name | Read-only | ENT-provider.name |
| Provider Contact | text | Yes | Clinic contact information | Read-only | ENT-provider.address, ENT-provider.phone, ENT-provider.email |
| Provider Address | text | Yes | Clinic address | Read-only | ENT-provider.address |
| Provider Email | text | Yes | Provider email | Read-only | ENT-provider.email |
| Provider Phone | text | Yes | Provider phone | Read-only | ENT-provider.phone |

**Section 7: Pricing & Payment Information** (from FR-004, FR-006, FR-007):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Currency | text | Yes | Payment currency and locked exchange-rate context | Read-only; acceptance snapshot | ENT-quote.currency_snapshot |
| Offered Price | number | Yes | Offered price of the accepted subquote, as entered before any promotion | Read-only; acceptance snapshot | ENT-subquote.offered_price |
| Promotion Applied | group | No | Structured promotion included in the accepted price | Read-only; acceptance snapshot | ENT-subquote.promotion_snapshot |
| Accepted Price | number | Yes | Booking total: the accepted price after promotion | Read-only; acceptance snapshot | ENT-subquote.price_after_promotion |
| Deposit Percentage | text | Yes | Deposit percentage used | Read-only; admin-configured | ENT-booking.deposit_percentage |
| Deposit Amount | number | Yes | Deposit amount required/paid | Read-only | ENT-booking.deposit_amount |
| Deposit Status | badge | Yes | Pending/Paid/Partial | Read-only | ENT-booking.deposit_status |
| Payment History | table | Yes | All payments (deposit, installments, final) with dates, amounts, methods | Read-only | ENT-booking.payment_history |
| Payment Status | badge | Yes | The single "Payment status" list owned by FR-007 | Read-only; read from FR-007 | ENT-booking.payment_status |
| Payment Schedule | table | Conditional | Installment schedule (if applicable) | Only shown if installments | ENT-booking.payment_schedule |
| Remaining Balance | number | Yes | Amount remaining to pay | Calculated | ENT-booking.remaining_balance |
| Final Payment Due Date | datetime | Conditional | Final payment due date | Read-only; if applicable | ENT-booking.final_payment_due_at |
| Refund History | table | Yes | All refunds processed with dates, amounts, reasons | Read-only | ENT-booking.refund_history |

**Section 8: Inquiry Context** (from FR-003):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Inquiry Reference | text | Yes | Original inquiry HPID | Read-only; link to inquiry | ENT-inquiry.reference |
| Requested Countries | list | Yes | Countries patient selected for treatment | Read-only; from inquiry | ENT-inquiry.treatment_countries |
| Requested Date Ranges | list | Yes | All date ranges patient requested | Read-only; from inquiry | ENT-inquiry-date-range.start_date, ENT-inquiry-date-range.end_date |

**Section 9: Audit & History**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Audit Log | table | Yes | All status changes and admin actions with timestamps, users, reasons | Read-only; immutable | ENT-audit-entry.action, ENT-audit-entry.actor_id, ENT-audit-entry.reason, ENT-audit-entry.timestamp |
| Status History | timeline | Yes | Chronological status changes | Read-only | ENT-booking.status_history |
| Internal Notes | table | Yes | Admin internal notes (not visible to patient/provider) | Editable by admin | ENT-booking.internal_notes |
| Version History | table | Yes | Parent quote and subquote version history captured at acceptance | Read-only | ENT-booking.accepted_parent_quote_version, ENT-booking.accepted_subquote_version |

**Intervention Actions**:

| Action | Type | Condition | Description | Graph field |
|--------|------|-----------|-------------|-------------|
| Revive Booking | button | Booking is `Payment Window Expired` and carries no `supportRequired` marker | Opens Screen 7; revives the booking to `Accepted` only (mandatory reason; guarded per Admin Status and Date Intervention rules) | no graph field (control) |
| Change Appointment | button | Booking is `Accepted` or `Confirmed` | Opens Screen 8; changes the appointment date/time (mandatory reason and slot availability check), sends `booking.rescheduled`, and triggers an FR-008 travel-date review for any linked travel records | no graph field (control) |
| Cancel Booking | button | Booking is `Accepted`, `Payment Window Expired`, or `Confirmed`; never offered in `In Progress` or `Aftercare` (REQ-006-052) | Opens Screen 9; cancels the booking on an admin decision or a support-routed patient request (mandatory reason). For a booking with a pending provider fault it takes the cause `ProviderFault`, the full refund and no fee (REQ-006-081) | no graph field (control) |
| Start Provider-Fault Transfer | button | Booking is `Accepted` or `Confirmed` with a provider fault (withdrawal, drop-out, or provider-status cancellation with `supportRequired`); never shown for `In Progress` or `Aftercare` | Opens Screen 10; at the submit re-checks the booking status, cancels the original booking with the provider-fault cause if not already cancelled, and assigns a replacement provider through an admin-authored replacement quote | no graph field (control) |
| Close inquiry | button | Booking is `Cancelled` and still carries the `supportRequired` marker, with the inquiry not yet `Cancelled` | Sets the inquiry to `Cancelled`, clears the marker with an audited resolution (mandatory reason), and sends the patient the admin-close variant of `inquiry.cancelled` (REQ-020-076) saying that no replacement will follow (REQ-006-082) | ENT-booking.support_required, ENT-inquiry.support_required |
| Resolve In-Progress Provider Fault | button | Booking is `In Progress` with a provider fault and `supportRequired` | Opens Screen 11; the admin either moves the booking to `Aftercare` and reassigns the aftercare provider through FR-011 Screen 19, or cancels the booking through Screen 9 (Alternative Flow B7) | no graph field (control) |
| Close Case Early, No Fault | button | Booking is `In Progress` and carries no `supportRequired` marker | Opens Screen 11 with the route Move to Aftercare, no fault, which moves the booking to `Aftercare` from the decision date with an admin-set refund (Alternative Flow B9) | no graph field (control) |
| Reassign Aftercare | link | Booking is `Aftercare` with a provider fault or `supportRequired` | Opens the FR-011 aftercare reassignment screen for this booking's aftercare case (Alternative Flow B6) | no graph field (control) |
| Change Treatment Details | link | Booking is `Confirmed`, `In Progress`, `Aftercare`, or `Completed` | Opens the FR-010 Change Treatment Details screen (FR-010 Screen 9) for plan days, clinician set, and estimated graft count; mandatory reason, audit entry, and `treatment.plan_changed` | no graph field (control) |
| Emergency Edit | button | Any booking | Opens the audited emergency edit (mandatory reason; full before and after history; changes only the fields listed under Emergency Edit Fields; never sets the booking status; payment records and money terms stay immutable; REQ-006-074) | no graph field (control) |
| Process Refund | button | Booking is `Cancelled` or eligible, and no automatic refund has started for the closure; unavailable once it has (REQ-006-083) | Process the refund that REQ-006-053 sets for the case: in full with no fee for a provider withdrawal, drop-out, suspension, or deactivation before treatment starts; the amount the admin set on Screen 11 for an in-treatment provider fault; the refund ladder set in FR-029 for every other cancellation. The refund step and its event are owned by FR-007 (mechanics in FR-007, FR-007B, and FR-017) | no graph field (control) |
| Add Internal Note | button | Always | Add admin-only note | no graph field (control) |
| View Inquiry | link | Always | Open full inquiry details (FR-003) | no graph field (control) |
| View Accepted Selection | link | Always | Open accepted subquote and AcceptanceEvent details (FR-005) | no graph field (control) |
| View Parent Quote | link | Always | Open source parent quote details (FR-004) | no graph field (control) |
| View 3D Scan | link | Always | Open 3D scan viewer | no graph field (control) |
| View Medical Questionnaire | link | Always | Open medical questionnaire | no graph field (control) |

**Emergency Edit Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Appointment Time | time | No | A different start time on the same appointment date | The date never changes here; a date change goes through Change Appointment (Screen 8); the slot availability check of Screen 8 applies | ENT-booking.hold_appointment_at |
| Booking Notes | text | No | Admin note on the booking | Admin-only; not visible to patient or provider | ENT-booking.internal_notes |
| Reason | text | Yes | Why the edit is made | Mandatory; the before and after values of every changed field are kept in the audit entry | ENT-audit-entry.reason |

The emergency edit never changes the price, the package, the provider, or the clinic, and never changes the booking status or any payment record (REQ-006-074). A change of the appointment time sends the mandatory `booking.rescheduled` notice to the patient and the provider, with the old and new time.

**Business Rules**:

- Admin has full visibility to all patient and provider information (no masking). (REQ-006-048)
- Admin can revive a `Payment Window Expired` booking, change an appointment, cancel a booking, start the provider-fault transfer, resolve an `In Progress` provider fault, and open the aftercare reassignment only through the actions above and under the Admin Status and Date Intervention rules, each with a mandatory reason. The emergency edit changes only the appointment time on the same date and the booking notes, with a mandatory reason and full before and after history. No other manual status change is allowed; the Booking Status field is never edited directly, including through the emergency edit.
- Dispute resolution uses only these governed actions and the emergency edit; there is no separate status-override action.
- All modifications are logged in audit trail with who/when/what/why.
- Admin can process refunds as REQ-006-053 sets them: in full for a provider withdrawal, drop-out, suspension, or deactivation before treatment starts, at the Screen 11 amount for an in-treatment provider fault, and per the refund ladder set in FR-029 otherwise.
- Admin can add internal notes to booking (not visible to patient/provider). (REQ-006-049)
- See REQ-006-047.
- See REQ-006-077.
- A Travel section sits on this screen for every confirmed booking, whatever the travel path; FR-006 hosts it and FR-008 Screen 11 defines its content. (REQ-006-042)

**Notes**:

- This screen aggregates all information from the complete patient journey (inquiry through booking).
- UI may use tabs or accordion sections to organize information by stage.
- Full administrative access for dispute resolution and exceptional cases.
- All actions require justification and are fully audited.
- Payment details shown without card information (PCI compliance).

#### Screen 7: Revive Booking (Admin Modal)

**Purpose**: Revive a `Payment Window Expired` booking to `Accepted` with a new slot hold, opened from Screen 6 Revive Booking.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Booking Reference | text | Yes | Booking being revived | Read-only | ENT-booking.booking_reference |
| Current Status | badge | Yes | Must be `Payment Window Expired` | Read-only; action unavailable for any other status | ENT-booking.status |
| Appointment | datetime | Yes | Booking's current appointment date/time and time zone | Read-only; slot availability is re-checked on confirm | ENT-booking.hold_appointment_at, ENT-booking.hold_appointment_timezone |
| Promotion Use Check | indicator | Conditional | Shown when the accepted promotion has a usage limit; states whether one use can be taken again | Read-only; revive blocked when the limit has no room | no graph field |
| New Payment Deadline | datetime | Yes | Revive time plus the FR-026 slot-hold duration | Read-only; calculated | ENT-slot-hold.hold_expires_at |
| Reason | textarea | Yes | Why the booking is revived | Mandatory; 10 to 500 characters (REQ-006-050) | ENT-audit-entry.reason |
| Confirm | checkbox | Yes | Admin confirms the revive and the new hold | Must be checked before submit (REQ-006-078) | no graph field (control) |

**Business Rules**:

- On submit, System checks that the booking's provider is `Active` (FR-015 Rule 9). If the provider is `Suspended` or `Deactivated`, the revive is blocked with the message "This provider is suspended or deactivated, so this booking cannot be revived. Cancel the booking instead." and nothing changes. (REQ-006-020)
- Revive is also blocked while the booking carries the `supportRequired` marker of a pending provider fault (Alternative Flow B5, REQ-006-081); Screen 6 does not offer the action then.
- On submit, System re-checks that the slot is free and that the promotion limit has room; if either check fails, the revive is rejected with the reason shown and nothing changes.
- On submit, System also checks that the booking's current appointment is later than the new payment deadline; if it is not, the revive is rejected with the reason shown and nothing changes. After the revive, Screen 1 offers only the installment options that are still feasible for the appointment (REQ-006-033), and pay in full when none is.
- On success, the booking returns to `Accepted`, a new hold of the FR-026 duration starts, and the AcceptanceEvent and snapshot stay unchanged. The revived booking counts again in the FR-014 pending-payment figures, aged from the start of its new hold (REQ-014-139).
- If the Settings API is unavailable when the new hold is placed, the revive is blocked and can be retried; no stale or guessed hold duration is used. (REQ-006-013)
- Audit entry: admin, timestamp, reason, old and new status, new hold expiry.
- Resulting notice: the mandatory `booking.revived` notice to the patient (with the new payment deadline) and the provider.

#### Screen 8: Change Appointment (Admin Modal)

**Purpose**: Change the appointment date/time of an `Accepted` or `Confirmed` booking, opened from Screen 6 Change Appointment.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Booking Reference | text | Yes | Booking being changed | Read-only | ENT-booking.booking_reference |
| Current Appointment | datetime | Yes | Booking's current appointment date/time and time zone | Read-only | ENT-booking.hold_appointment_at, ENT-booking.hold_appointment_timezone |
| Accepted Appointment | datetime | Yes | Appointment captured in the acceptance snapshot (the accepted subquote version, not a later version created by an admin edit of the accepted quote) | Read-only; never changed | ENT-subquote.appointment_at |
| New Appointment Date | date | Yes | New appointment date | Required; must differ from the current appointment; not in the past | ENT-audit-entry.after |
| New Appointment Time | time | Yes | New appointment start time | Required; in the provider's time zone | ENT-audit-entry.after |
| Reason | textarea | Yes | Why the appointment changes | Mandatory; 10 to 500 characters (REQ-006-050) | ENT-audit-entry.reason |
| Travel Review Notice | indicator | Conditional | Shown when travel records are linked; states that an FR-008 travel-date review will be raised | Read-only (REQ-006-079) | no graph field |
| Installment Plan Outcome | indicator | Conditional | Shown when the booking has an installment plan; states the FR-007B recalculation outcome for the new date | Read-only; the change is blocked when no plan is feasible for the new date (REQ-006-017) | no graph field |
| Confirm | checkbox | Yes | Admin confirms the change | Must be checked before submit (REQ-006-078) | no graph field (control) |

**Business Rules**:

- Available only while the booking is `Accepted` or `Confirmed`.
- Screen 8 is one of two routes for a date change; the other is the admin edit of the accepted quote date range or appointment (REQ-005-023). Both run the same checks (provider status, slot availability, FR-007B plan recalculation, the FR-008 travel review) and send `booking.rescheduled`. (REQ-006-017)
- On submit, System checks that the booking's provider is `Active` (FR-015 Rule 9). If the provider is `Suspended` or `Deactivated`, the change is blocked with the message "This provider is suspended or deactivated, so this appointment cannot be changed. Use the provider-fault transfer instead." and nothing changes. (REQ-006-020)
- For an `Accepted` booking, System also checks on submit that the new appointment is later than the booking's payment deadline (the hold expiry, which the change keeps); if it is not, the change is rejected with the reason shown and nothing changes. (REQ-006-017)
- On submit, System checks that the new provider date/time and time zone are free and rejects the change if not; the hold (for `Accepted`) or calendar block (for `Confirmed`) moves only on success. An `Accepted` booking keeps its original hold expiry. (REQ-006-059)
- The booking's current appointment is updated; the acceptance snapshot keeps the accepted appointment as the baseline. Booking notices read the booking's current appointment.
- The FR-029 rescheduling fee never applies to a change made here or through the accepted-quote edit: an admin-made change is not a patient reschedule, and patient rescheduling stays deferred to V2 (REQ-006-067).
- The installment plan is recalculated by FR-007B for the new date and shown read-only before submit; when no plan is feasible for the new date, the change is blocked and nothing changes.
- Audit entry: admin, timestamp, reason, old and new appointment.
- Resulting notice: the mandatory `booking.rescheduled` notice to the patient and the provider, with the old and new appointment. Linked travel records get an FR-008 travel-date review.
- Money: when the clinic's share has already moved, the appointment change pulls it back and moves it again later (Payment & Billing Rules, Money movement).

#### Screen 9: Cancel Booking (Admin Modal)

**Purpose**: Cancel a booking on an admin decision or on a patient request received through support, opened from Screen 6 Cancel Booking (Alternative Flows B2 and B3).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Booking Reference | text | Yes | Booking being cancelled | Read-only | ENT-booking.booking_reference |
| Current Status | badge | Yes | Source booking state | Read-only; must be `Accepted`, `Payment Window Expired`, or `Confirmed`, or `In Progress` when opened from Screen 11 (REQ-006-052) | ENT-booking.status |
| Request Source | select | Yes | Patient request through support, or admin decision | Required | ENT-booking.cancellation_request_source |
| Support Ticket Reference | text | Conditional | Support case that carries the patient's request | Required when Request Source is patient request | ENT-booking.support_ticket_reference |
| Reason | textarea | Yes | Cancellation reason shown to the patient and provider | Mandatory; 10 to 500 characters (REQ-006-050) | ENT-booking.cancellation_reason |
| Refund Amount | number | Conditional | Refund the admin set on Screen 11 | Shown only when Screen 9 is opened from Screen 11 (Alternative Flow B7); read-only; the refund ladder does not apply | no graph field |
| Effects Summary | text | Yes | States that the booking and inquiry become `Cancelled`, the accepted quote stays `accepted`, any hold or calendar block is released, and names the refund rule that applies: in full with no fee for a provider withdrawal, drop-out, suspension, or deactivation before treatment starts; the Screen 11 amount when opened from Screen 11; the refund ladder set in FR-029 otherwise | Read-only | no graph field |
| Confirm | checkbox | Yes | Admin confirms the cancellation | Must be checked before submit (REQ-006-078) | no graph field (control) |

**Business Rules**:

- Only an admin can cancel a booking; the patient has no in-app cancel action from acceptance onward.
- On submit, the booking becomes `Cancelled` with the reason as its cancellation reason, the inquiry becomes `Cancelled`, the accepted quote stays `accepted`, the AcceptanceEvent stays unchanged with no supersession record, and any hold or calendar block is released.
- Audit entry: admin, timestamp, source state, request source, support ticket reference, reason.
- Resulting notice: `booking.cancelled` to the patient and the provider, including the reason. The cancellation fee and the refund amount are filled in by the system from the refund that REQ-006-053 sets; the admin does not type them.
- The refund on this screen follows REQ-006-053: the amount set on Screen 11 when the screen is opened from Screen 11 (the refund ladder does not apply); in full with no fee when the cause is a provider withdrawal, drop-out, suspension, or deactivation before treatment starts; the refund ladder set in FR-029 for every other cancellation. Fees and money movement follow FR-007, FR-007B, and FR-017 (Payment & Billing Rules, Money movement).
- When the FR-016 patient suspension cascade cancels a booking, the cancellation takes the cause "Patient account suspended" with request source Admin, the acting admin carried from FR-016, and the fixed reason "Booking cancelled because the patient account was suspended"; the refund follows the refund ladder set in FR-029 (REQ-006-084).
- When opened from Screen 11, the submit also resolves the `supportRequired` marker with an audited resolution and ends the payout hold (Alternative Flow B7).
- When the booking carries a pending provider fault (Alternative Flow B5), the submit takes the cause `ProviderFault`, the full refund and no cancellation fee, whatever request source is selected, and resolves the `supportRequired` marker with an audited resolution. (REQ-006-081)
- The submit starts the one refund of the closure; Process Refund on Screen 6 is then unavailable (REQ-006-083).
- The patient also sees the cancellation fee and the refund in the support reply to a cancellation request; the notice above carries them regardless of what the admin writes in the reply.
- The support case that carries a patient request has a Ticket Source taken from the list owned by FR-034; FR-006 keeps no list of its own.

#### Screen 10: Provider-Fault Transfer and Replacement Quote (Admin)

**Purpose**: Move a patient to a replacement provider in the same inquiry after a provider fault, through an admin-authored replacement quote and a new admin-authored acceptance (Alternative Flow B5), opened from Screen 6 Start Provider-Fault Transfer.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Original Booking | text | Yes | Booking reference, provider, status, and cause | Read-only | ENT-booking.booking_reference, ENT-booking.closure_cause |
| Fault Type | select | Conditional | Provider withdrawal or provider drop-out | Required when the booking is not already cancelled by the provider-status cascade; prefilled as `ProviderSuspended` or `ProviderDeactivated` otherwise | ENT-booking.closure_cause |
| Replacement Provider | search select | Yes | Provider who takes over the patient | Required; must be active and not the original provider; status re-checked on submit | ENT-quote.provider_id |
| Replacement Quote | form | Yes | Quote for the replacement provider in the same inquiry, using the FR-004 quote fields (treatment, package, options, date-price rows with appointment, price, and currency) | Required; validated as an FR-004 quote; authored by the admin | no graph field |
| Selected Option and Date-Price Row | select | Yes | The option and date-price row that becomes the replacement acceptance | Required; exactly one; the appointment slot must be free | ENT-acceptance-event.quote_option_id, ENT-acceptance-event.option_date_price_id |
| Adjustment Reason | textarea | Yes | Why the package or price differs from the original accepted selection | Mandatory; 10 to 500 characters (REQ-006-050) | ENT-audit-entry.reason |
| Paid Amount on Original Booking | text | Yes | Amounts already paid on the original booking | Read-only; on a provider withdrawal or drop-out the patient is refunded everything paid and the replacement booking takes a new payment; a provider-status cancellation entered from B4 follows the same terms | ENT-booking.paid_amount |
| Confirm | checkbox | Yes | Admin confirms the transfer | Must be checked before submit (REQ-006-078) | no graph field (control) |

**Business Rules**:

- Available only for `Accepted` or `Confirmed` bookings with a provider fault, including bookings already cancelled by the provider-status cascade with `supportRequired`. An `In Progress` provider fault uses Screen 11 instead.
- On submit, System first re-checks the status of the original booking: only `Accepted`, `Confirmed`, or a `Cancelled` booking that still carries the marker from the provider-status cascade proceed. A booking that has reached `In Progress` in the meantime is not transferred: nothing changes and the admin is sent to Screen 11 (Alternative Flow B7). Any other status stops the submit with the reason shown. (REQ-006-081)
- The replacement quote is authored through FR-004 Workflow 7 and FR-004 Screen 8. If no replacement acceptance is recorded, the replacement quote expires under the normal FR-004 quote expiry; the inquiry stays `supportRequired` and is not cancelled automatically, and the admin may author another replacement quote or, for a booking already `Cancelled` with the marker, close the inquiry with Close inquiry on Screen 6 (REQ-006-082).
- On submit, System re-checks that the replacement provider is `Active` (FR-015 Rule 9). If it is `Suspended` or `Deactivated`, the acceptance is blocked with the message "This provider is suspended or deactivated, so this replacement quote cannot be accepted. Choose another replacement provider." and nothing changes. (REQ-006-020)
- If the original booking is not already `Cancelled`, the submit first cancels it with cause `ProviderFault` and releases its hold or calendar block; until this submit the original booking keeps its status and its hold, with payment, payment reminders and revive blocked (Alternative Flow B5 steps 1 and 2). (REQ-006-058, REQ-006-081)
- On submit, System saves the replacement quote, creates the admin-authored AcceptanceEvent that points to the selected replacement quote, option, and date-price row, writes the single FR-005 supersession record linking the original AcceptanceEvent to the new one, acquires the replacement slot hold, and creates the replacement booking in `Accepted`. The admin-authored replacement quote is the only quote that may be created after an inquiry has an acceptance.
- Audit entry: admin, timestamp, fault type, replacement provider, replacement quote reference, selected option and row, adjustment reason; the `supportRequired` marker is resolved with an audited resolution.
- Resulting notices: `booking.provider_fault_replacement` to the patient and admin; `booking.scheduled` to the patient with the replacement payment deadline; `quote.accepted` (outcome `selected_subquote_accepted`) to the replacement provider.

#### Screen 11: Resolve In-Progress Case (Admin Modal)

**Purpose**: Record the admin's decision for a booking that is `In Progress`, opened from Screen 6: the case-by-case decision for a provider fault (Alternative Flow B7, from Resolve In-Progress Provider Fault), or the early close with no fault (Alternative Flow B9, from Close Case Early, No Fault).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Booking Reference | text | Yes | Booking, provider, and current treatment day | Read-only | ENT-booking.booking_reference, ENT-booking.current_treatment_day |
| Current Status | badge | Yes | Source booking state | Read-only; must be `In Progress`, with `supportRequired` for a provider fault and without it for the early close with no fault | ENT-booking.status |
| Closure Cause | text | Yes | `ProviderFault`, `ProviderSuspended`, or `ProviderDeactivated` for a provider fault; `NoFaultEarlyClose` for the early close with no fault | Read-only; a provider-fault cause is read from the booking, and `NoFaultEarlyClose` is set at the submit of the no-fault route | ENT-booking.closure_cause |
| Resolution Route | radio | Yes | Move to Aftercare and reassign the aftercare provider, cancel the booking, or Move to Aftercare, no fault | Exactly one; with a provider fault only the first two are offered, and without one only Move to Aftercare, no fault; the no-fault choice is recorded as the closure cause, not as a marker resolution | ENT-booking.support_required_resolution |
| Paid Amount | text | Yes | Total amount the patient has paid on the booking | Read-only | ENT-booking.paid_amount |
| Patient Refund Amount | number | Yes | Refund the admin sets for the patient, from zero up to the full amount paid | Mandatory; zero to the Paid Amount, inclusive; applies to every route | no graph field |
| Reason | textarea | Yes | Why the admin chose this route and this refund amount | Mandatory; 10 to 500 characters (REQ-006-050) | ENT-audit-entry.reason |
| Effects Summary | text | Yes | For Move to Aftercare, no fault: the booking becomes `Aftercare` at the decision date (the aftercare start date), no `supportRequired` marker is set and no payout is held, the refund amount is applied as an exception refund, the provider's share is eligible for payout on the decision date, the treatment record becomes Closed Early, and FR-011 is signalled for the post-op instructions (REQ-006-086). For Move to Aftercare: the booking becomes `Aftercare` with the treatment closed early at the decision date, the treatment record is kept as recorded, the decision date is the aftercare start date, the refund amount is applied, and FR-011 Screen 19 opens for the reassignment. For Cancel: Screen 9 opens with the reason prefilled and this refund amount shown read-only, and the refund ladder does not apply | Read-only | no graph field |
| Confirm | checkbox | Yes | Admin confirms the decision | Must be checked before submit (REQ-006-078) | no graph field (control) |

**Business Rules**:

- After the admin submits a decision, the screen is read-only until the chosen route completes: the decision, the route and the refund amount cannot be edited or re-submitted, and the admin continues on Screen 9 or FR-011 Screen 19. If the route is left unfinished, the booking stays flagged and the payout stays held. (REQ-006-019)
- No replacement quote and no replacement acceptance are offered on this screen; the provider-fault transfer (Screen 10) is limited to bookings before treatment starts.
- Move to Aftercare: on submit, System moves the booking from `In Progress` to `Aftercare`, closing the treatment early at the decision date (the aftercare start date handed to FR-011), and opens FR-011 Screen 19, where the admin assigns the new aftercare provider or the Hairline aftercare team (Alternative Flow B6); FR-011 sends `aftercare.provider_reassigned` to the patient and the new aftercare provider.
- Move to Aftercare, no fault: offered for an `In Progress` booking with no `supportRequired` marker; the submit completes the decision, so no second screen follows and nothing stays open (Alternative Flow B9, REQ-006-086, FR-010 Rule 17).
- Cancel: on submit, System opens Screen 9; the cancellation follows Alternative Flow B2 with the refund amount set here, and sends `booking.cancelled`.
- Audit entry: admin, timestamp, closure cause, chosen route, patient refund amount, reason. The submit records the decision only; the `supportRequired` marker is resolved with an audited resolution once the chosen route completes, by the Screen 9 submit or the FR-011 Screen 19 submit (Alternative Flow B7).
- Money for a provider fault: the admin sets the patient refund amount, from zero up to the full amount paid, with the mandatory reason; the provider's payout for the booking is held from the fault until the chosen route completes, and the refund comes out of that held payout; if the payout was already released, the shortfall is deducted from the provider's next payout (FR-007, FR-007B, and FR-017 own the mechanics).

---

## Business Rules

### General Module Rules

- Booking is confirmed only after successful deposit or first installment charge.
- Appointment slot is selected by the accepted subquote and held for payment; no additional slot selection is permitted.
- Provider calendars must be accurate; confirmed bookings auto-block times at database level; overlapping appointments are prevented. (REQ-006-068)
- All timestamps shown in patient's local timezone; provider view shows both local and clinic time. (REQ-006-032)
- **Overlapping Appointment Prevention**: FR-005 atomically acquires an exclusive slot hold when acceptance is created. A second acceptance for a held or blocked slot is rejected before any AcceptanceEvent or booking handoff is created. Exclusivity is enforced by a uniqueness rule on active holds (provider, appointment date/time, and time zone), so a concurrent second acceptance for the same slot fails and the patient is told the slot was just taken. FR-006 verifies hold ownership before payment and converts the hold into a confirmed calendar block on payment success; stale or invalid handoffs are rejected before the payment gateway is called. (REQ-006-003)
- **Status values**: `Accepted` (subquote accepted, awaiting payment) → `Confirmed` (deposit paid) → `In Progress` (procedure started, via FR-010) → `Aftercare` (treatment complete, or closed early by an admin decision on Screen 11; aftercare active via FR-011) → `Completed` (FR-011 emits the aftercare completion event, whatever its outcome value: completed, paperwork only, cancelled by the patient, or cancelled by an admin; REQ-011-096, REQ-011-101). An `In Progress` booking with a provider fault moves to `Aftercare` only through the admin decision on Screen 11 (Alternative Flow B7), and the decision date is then the aftercare start date handed to FR-011. From `Accepted`, hold expiry transitions to `Payment Window Expired`. From `Payment Window Expired`, only the audited admin revive returns the booking to `Accepted` with a new hold. `Confirmed` is a booking status only, never a quote status. `supportRequired` is a marker, not a status. (REQ-006-060)
- **Cancelled entries** (source state, actor, cause): (1) `Accepted`, `Payment Window Expired`, or `Confirmed` → `Cancelled` by admin cancellation (Screen 9), including support-routed patient requests and the FR-016 patient suspension cascade (cause "Patient account suspended", REQ-006-084), with the admin's reason, and `In Progress` → `Cancelled` through the Cancel route of Screen 11; the inquiry also becomes `Cancelled` and the accepted quote stays `accepted` (Alternative Flows B2, B3, and B7). Cancel Booking is not offered in `In Progress` or `Aftercare` on Screen 6. A cancellation of a booking with a pending provider fault takes the cause `ProviderFault` (REQ-006-081). (2) `Accepted` or `Confirmed` → `Cancelled` at the admin submit of the provider-fault transfer, cause `ProviderFault` (Alternative Flow B5). (3) `Accepted` or `Confirmed` → `Cancelled` by the system on an effective provider suspension or deactivation, cause `ProviderSuspended` or `ProviderDeactivated` with `supportRequired = true` (Alternative Flow B4), followed by the B5 transfer. The inquiry of a booking closed through (2) or (3) stays open until the replacement acceptance, or until an admin closes it with Close inquiry (REQ-006-082). (4) `Confirmed` → `Cancelled` by the system, cause `UnpaidBalance`, when the unpaid balance of a booking paid with the Installments option is still unpaid at the cancellation point set in FR-029, counted in days after the due date of the first missed installment; the inquiry also becomes `Cancelled`, the remaining installments are voided, the refund ladder applies, and the rule is inactive until that point is set and applies only to bookings confirmed after it is set (Alternative Flow B8). A provider fault or provider-status event while `In Progress` does not cancel the booking; it stays `In Progress` with `supportRequired` until the admin moves it to `Aftercare` with an aftercare reassignment or cancels it through entry (1) (Alternative Flow B7). A provider fault or provider-status event during `Aftercare` does not cancel the booking; it stays `Aftercare` and follows the aftercare reassignment (Alternative Flow B6). `Completed` and `Cancelled` are terminal. (REQ-006-061)
- **Release triggers**: (1) Post-acceptance hold expiry without successful first payment (FR-026 duration, 48h default), (2) Admin cancellation during the hold period, including a support-routed patient request (immediate release per B3 flow), (3) Admin booking cancellation per B2 flow, (4) Provider suspension/deactivation cascade per B4 flow (immediate release, including holds with time remaining), (5) Provider fault before treatment starts per B5 flow, released at the admin submit on Screen 10 or at an admin cancellation of the pending fault, never earlier (the hold does not expire while the fault is pending), (6) Admin appointment change per Screen 8 or an admin edit of the accepted quote date (the hold or block moves to the new appointment), (7) System cancellation for an unpaid balance per B8 flow (the calendar block is released). (REQ-006-062)
- FR-006 keeps the booking status and cause only; every payment field of the booking (the single "Payment status", refund state, installment progress) is owned by FR-007 and is read from there.
- **Integration point**: Booking flow requires verified patient and profile data.
- Admins process edge-case cancellations within published SLAs.
- Idempotent booking creation with slot holds to prevent race conditions; atomic confirm and appointment-record creation on payment success. (REQ-006-069)
- Calendar conflict detection and prevention; status transitions auditable.
- Resilient to payment gateway latency; clear user states during processing.
- Patient app to booking API for payment initiation (slot is pre-scheduled and read-only).
  - Data: AcceptanceEvent ID, accepted parent quote ID/version, accepted subquote ID/version, immutable acceptance snapshot, pre-scheduled slot ID, payment choice, and acknowledgments. The accepted subquote and parent version values MUST be equal.
  - Auth: patient token; RBAC enforcing ownership.
  - Errors: validation feedback; recoverable payment failures.
- Provider calendar API for blocking/unblocking; admin oversight API for audit and dispute actions.

### Data & Privacy Rules

- Patient identity remains masked to provider until the booking has reached `Confirmed` (payment success); once unmasked it stays visible, including after a later cancellation.
- Booking, payment, and personal data are encrypted at rest and in transit; audit logs are immutable; retention follows the system PRD, Platform-Wide Rules: One 10-year retention period.
- Retention of booking and financial records follows the system PRD, Platform-Wide Rules: One 10-year retention period; hard deletes prohibited (soft-delete/archive only).
- MFA is a **planned mandatory control** for Admin and Provider tenants and MUST be treated as a future (non-MVP) requirement until the shared MFA stack is delivered (per Constitution / FR-026 / FR-031). Until then, enforce strong password policies, throttling, and re-authentication flows where appropriate; RBAC everywhere.
- TLS 1.3 in transit; AES-256 at rest; no storage of card PANs; webhook signature verification.
- Full audit trail on state changes and access; rate limiting and anti-abuse protections on booking/payment endpoints.

### Admin Editability Rules

**Editable by Admin** (via A-09: System Settings & Configuration):

- **Deposit Rate**: Owned by **FR-029: Payment System Configuration** (REQ-029-013 for the setting, REQ-029-015 for new bookings only, REQ-029-016 for the calculation); FR-006 does not restate it.
- Cancellation policy schedule (thresholds and refund percentages). The refund ladder setting is owned by **FR-029**; FR-006 points to it. (REQ-006-064)
- The clinic cancellation charge for a provider withdrawal or drop-out (Alternative Flow B5) is a fixed amount set by the admin, with no default value.
- Slot-hold duration and the "hold expiring soon" reminder lead time are owned by **FR-026** (versioned and audited; hold default 48 hours). FR-006 consumes them and has no separate hold setting. When the Settings API is unavailable as a hold is placed, at subquote acceptance or at an admin revive, the action is blocked and can be retried; no stale or guessed hold duration is used (REQ-026-144). (REQ-006-013)
- Notification templates for booking confirmations/reminders; booking confirmation content (configured via **FR-030: Notification Rules & Configuration**). (REQ-006-065)
- Commission settings (FR-029); commission is fixed at booking confirmation.

**Confirmed Booking Data Integrity (Admin Override)**:

- Confirmed bookings are **read-only for patients and providers**. (REQ-006-023)
- Admins MAY perform the guarded interventions in the Admin Status and Date Intervention rules below and the audited emergency edit of the appointment time and booking notes, but MUST do so as **append-only, versioned intervention events** (who/when/what/why) rather than overwriting historical records. (REQ-006-024)
- Financial transactions (payments/refunds) remain immutable once confirmed; admin actions reference the original transaction IDs and create new adjustment/refund events as needed. (REQ-006-025)

**Admin Status and Date Intervention Rules**:

- **Revive `Payment Window Expired`**: Admin MAY move a booking from `Payment Window Expired` back to `Accepted` only with a mandatory reason. The system re-checks that the slot (provider, appointment date/time, and time zone) is free and rejects the revive if it is not. On success, a new hold of the FR-026 slot-hold duration starts at the revive time. If the accepted promotion has a usage limit, the revive needs one use again: a provider-selected promotion or patient code re-reserves one use, and an automatic promotion takes one use again. The system rejects the revive if the limit has no room. The system also rejects the revive if the booking's appointment is not later than the new payment deadline, and while the booking carries the marker of a pending provider fault (REQ-006-081). The action is audited, the AcceptanceEvent and snapshot stay unchanged, and the system sends the mandatory "booking revived" notice to the patient (with the new payment deadline) and to the provider (slot held again). (REQ-006-017)
- **Change appointment date/time**: Allowed only for `Accepted` or `Confirmed` bookings with a mandatory reason, on Screen 8 or by the admin edit of the accepted quote's date range or appointment (REQ-005-023); both routes run the same checks and the same steps. The system checks that the booking's provider is `Active`, that the new provider date/time and time zone are free, that the FR-007B plan recalculation finds a feasible plan, and, for an `Accepted` booking, that the new appointment is later than the payment deadline, and rejects the change if any check fails; the hold or calendar block moves only on success. The booking's current appointment changes; the acceptance snapshot keeps the accepted appointment as the baseline, and booking notices read the booking's current appointment. The change is audited, sends the mandatory `booking.rescheduled` notice to the patient and the provider with the old and new appointment, and triggers an FR-008 travel-date review for any travel records already linked to the booking. The FR-029 rescheduling fee never applies to an admin-made change. (REQ-006-017)
- **Cancel booking**: Only an admin cancels a booking, from `Accepted`, `Payment Window Expired`, or `Confirmed` (and from `In Progress` only through the Cancel route of Screen 11), never from `Aftercare`, with a mandatory reason, a confirmation, and an audit entry (Screen 9; Alternative Flow B2). The booking and the inquiry become `Cancelled`, the accepted quote stays `accepted`, and `booking.cancelled` is sent to the patient and the provider. The refund follows REQ-006-053 (the Screen 11 amount when the cancellation is chosen on Screen 11), and a closure starts one refund only (REQ-006-083). Patient requests to cancel after acceptance reach the admin through support. (REQ-006-004)
- **Provider must be Active for admin booking actions** (FR-015 Rule 9): On submit, System checks the provider's status for each admin action below and, when the provider is `Suspended` or `Deactivated`, blocks the action, changes nothing, and shows the message for that action. (REQ-006-020)
  - Admin revive (Screen 7), for the booking's provider: "This provider is suspended or deactivated, so this booking cannot be revived. Cancel the booking instead."
  - Admin appointment change (Screen 8), for the booking's provider: "This provider is suspended or deactivated, so this appointment cannot be changed. Use the provider-fault transfer instead."
  - Admin-authored acceptance (the replacement acceptance in Alternative Flow B5, Screen 10), for the replacement provider, re-checked at acceptance even though it was `Active` when selected: "This provider is suspended or deactivated, so this replacement quote cannot be accepted. Choose another replacement provider."
- **Provider-fault transfer**: Only an admin starts the transfer and authors the replacement quote (Screen 10; Alternative Flow B5), with a mandatory reason and audit entry.
- **Pending provider fault**: From the trigger of a withdrawal or drop-out to the Screen 10 submit, the booking carries the `supportRequired` marker with the cause `ProviderFault`; payment, payment reminders, and revive are blocked, and the hold does not expire. Screen 10 re-checks the booking status at submit: only `Accepted` or `Confirmed` (or a `Cancelled` booking that still carries the marker from the provider-status cascade) proceed, and an `In Progress` booking goes to Alternative Flow B7. An admin cancellation during the pending period takes the cause `ProviderFault`, the full refund, and no cancellation fee. (REQ-006-081)
- **Close inquiry**: For a `Cancelled` booking that still carries the `supportRequired` marker, an admin MAY close the inquiry from Screen 6 with a mandatory reason: the inquiry becomes `Cancelled`, the marker is cleared with an audited resolution, and the patient is sent the admin-close variant of `inquiry.cancelled` (REQ-020-076). No provider is notified (REQ-020-020), and a draft replacement quote of the inquiry is cancelled without notice (REQ-004-111). (REQ-006-082)
- **One refund per closure**: A closure starts one refund. Process Refund is unavailable once the automatic refund of the closure has started, and the automatic refund is not started once Process Refund has been used. (REQ-006-083)
- **Aftercare reassignment**: A provider fault during `Aftercare` is handled by the FR-011 aftercare reassignment (Alternative Flow B6); the booking status does not change.
- **In-Progress provider fault**: A provider fault while the booking is `In Progress` keeps the booking `In Progress` with `supportRequired`; only an admin resolves it on Screen 11 (Alternative Flow B7), either by moving the booking to `Aftercare` and reassigning the aftercare provider through FR-011 Screen 19, or by cancelling the booking through Screen 9, with a mandatory reason, the patient refund amount, and an audit entry. The marker and the payout hold resolve once, when the chosen route completes. The refund comes out of the held payout; if the payout was already released, the shortfall is deducted from the provider's next payout. (REQ-006-019)
- **Emergency edit**: Besides the guarded actions above, an admin MAY change the appointment time on the same date and the booking notes through a separate audited emergency edit with a mandatory reason; every edit keeps its full before and after history. A change of date goes through Screen 8, and the price, the package, the provider, and the clinic are never changed by it. An emergency edit never sets the booking status, and payment records and money terms stay immutable. Revive, appointment change, cancellation, and the provider-fault transfer keep their own checks and cannot be bypassed through it (REQ-006-074).
- **No other status jumps**: Admin cannot set any other booking status manually, including through the emergency edit. All other transitions follow the governed flows (payment, admin cancellation, FR-010 treatment progress, provider-status cascade, provider-fault transfer, and the In-Progress provider-fault move to `Aftercare`).

**Fixed in Codebase (Not Editable)**:

- Password policy and OTP length; identity unmasking rule tied to payment confirmation.
- Audit logging enablement and retention guarantees.
- Overlapping appointment prevention logic (enforced at database level).

**Configurable with Restrictions**:

- Payment options availability per region/currency (cannot alter gateway compliance requirements); the setting is owned by FR-029. (REQ-006-066)

### Payment & Billing Rules

- **Deposit Rate**: The deposit percentage, its calculation, and the rule that a change applies to new bookings only are owned by FR-029 (REQ-029-013, REQ-029-015, REQ-029-016).
- Deposit required to confirm booking; final payment per FR-007 schedule.
- Installments must complete ≥30 days before procedure; failures trigger retries, then flag for admin. (REQ-006-034)
- **Post-Acceptance Hold**: Subquote acceptance places one temporary exclusive hold keyed by provider, appointment date/time, and time zone. The hold blocks other patients from that slot for the FR-026 slot-hold duration (default 48 hours), which starts at acceptance. The hold is fixed: payment failure or retry never extends or restarts it. The patient must complete the first payment step (deposit or first installment) before the hold expires. The appointment record is created only on successful payment; if the hold expires, it is released and no appointment exists. (REQ-006-005)
- **Hold Expiring Soon**: Before the hold expires, the patient receives the `booking.hold_expiring_soon` reminder; the lead time is set by admin in FR-026, and the notice details are in the notification Rule (REQ-020-086). No reminder is sent while a provider fault is pending on the booking. A lead time raised after the hold was placed applies only to reminders not yet sent; a reminder whose time has already passed is skipped, not sent late (REQ-026-031). (REQ-006-036)
- **Payment Window Expired**: Hold expiry moves the pending booking from `Accepted` to `Payment Window Expired`: the hold is released, payment is disabled, the AcceptanceEvent/snapshot remain immutable, neither the parent quote nor accepted subquote is reopened, and the mandatory Payment Window Expired notice goes to patient and provider. The outcome is final for that accepted selection except for the audited admin revive (Admin Status and Date Intervention Rules). (REQ-006-005)
- **Payment Window Expired Recovery**: The patient contacts support; an admin either performs the audited revive (Screen 7) or cancels the booking (Screen 9), after which the patient may start a new inquiry. One acceptance per inquiry still applies. (REQ-006-005)
- **First-Payment Boundary**: `Payment Window Expired` applies only to the first payment step (acceptance to deposit or first installment). A missed later installment or final payment never causes `Payment Window Expired`, booking cancellation, or inquiry cancellation; it is handled by FR-007 and FR-007B. The one exception is the unpaid balance of a booking paid with the Installments option on Screen 1 (the "deposit plan" of FR-029): when that balance is still unpaid at the cancellation point set in FR-029, counted in days after the due date of the first missed installment, the booking and the inquiry are cancelled with cause `UnpaidBalance`, the remaining installments are voided, and the refund ladder applies (Alternative Flow B8). The rule is inactive until an admin sets that point, which has no default, and it applies only to bookings confirmed after the value is set. (REQ-006-016)
- **Payment Failure Handling**:
  - If the first payment fails, Payment Service applies retry policy per FR-007 (exponential backoff) and surfaces failures for patient action when needed.
  - The patient can retry payment from the Accepted Subquote view only while the original hold is active. (REQ-006-035)
  - If no payment succeeds before the hold expires, the hold is released, further payment against it is blocked, and the booking becomes `Payment Window Expired`.
- A full refund applies when the provider withdraws, drops out, or is suspended or deactivated before treatment starts; an in-treatment provider fault takes an admin-set refund; every other cancellation follows the refund ladder set in FR-029. When the provider withdraws or drops out after acceptance and before treatment starts (Alternative Flow B5), or the booking is cancelled by a provider suspension or deactivation (Alternative Flow B4), the patient is refunded everything paid, pays no cancellation fee, and a replacement booking takes a new payment; the same terms apply to an admin cancellation of a booking with a pending provider fault. While `In Progress` the case follows Alternative Flow B7: the admin sets the patient refund amount from zero up to the full amount paid, with a mandatory reason and an audit entry, and the provider's payout for the booking is held from the fault until the chosen route completes; the refund comes out of the held payout, and if the payout was already released, the shortfall is deducted from the provider's next payout. (REQ-006-053)
- **Patient account suspension**: A booking cancelled by the FR-016 suspension cascade takes the cause "Patient account suspended" and is refunded by the refund ladder set in FR-029, or by the provider-fault terms where the provider is at fault (REQ-006-084).
- Refund processing SLA ≤ 3 business days for eligible cases.
- **Clinic cancellation charge**: A provider withdrawal or drop-out (Alternative Flow B5 only) charges the clinic a fixed amount set by the admin, with no default value, deducted from the clinic's next payout. It does not apply to the provider-status cancellation (Alternative Flow B4) or to an in-treatment provider fault (Alternative Flow B7).
- **Money movement (Stripe Connect)**: The product owner's Stripe Connect money-movement decisions replace the missing Payment Routing Spec. After the clinic's share has moved to the clinic's locked Stripe balance, an admin cancellation refunds the patient as REQ-006-053 sets (the refund ladder unless a provider-fault rule applies), pulls the share back from that balance, and deducts any shortfall from the clinic's next payout; an admin appointment change pulls the share back and moves it again 60 days before the new appointment (30 days for installments once fully paid). Mechanics are owned by FR-007 and FR-017.
- **Provider-Status Cancellation**: Bookings cancelled by an effective provider suspension/deactivation (Alternative Flow B4) are rehomed by admin to a replacement provider in the same inquiry through the Alternative Flow B5 transfer. The payment terms are the same as for a provider withdrawal or drop-out (Alternative Flow B5): the patient is refunded everything paid, pays no cancellation fee, and the replacement booking takes a new payment; exact mechanics are defined in FR-007, FR-007B, and FR-017. Provider eligibility is revalidated at booking-confirming payment (FR-015 Rule 9). A payment captured while suspension/deactivation becomes effective is recorded and treated as paid money, refunded in full under these B4 terms; it never confirms or revives the booking. (REQ-006-054)
- Prices shown in patient's currency; exchange rate locked in the subquote acceptance snapshot; payouts use that locked rate.
- **Promotion and Commission**: The promotion and accepted price are frozen at subquote acceptance and never change in FR-006, except through a new linked acceptance record in Alternative Flow B5. Commission is fixed at booking confirmation on the accepted price after promotion, in the quote currency, read from the acceptance snapshot (FR-029). The commission figure shown on the FR-004 quote screen is indicative only. (REQ-006-063)

### Rescheduling Rules

- **Rescheduling is deferred to V2**: The provider pre-schedules the appointment in the subquote; acceptance fixes the chosen appointment and reserves its slot, and successful payment confirms the booking. Rescheduling functionality will be evaluated for V2 based on business needs. (REQ-006-067)
- **Current Behavior**: The patient cannot reschedule. Date changes require the audited admin appointment change (Screen 8) or the admin edit of the accepted quote's date range or appointment (REQ-005-023), each of which sends `booking.rescheduled`, or an admin cancellation per cancellation policy. The FR-029 rescheduling fee does not apply to an admin-made change, because the admin, not the patient, initiates it. (REQ-006-067)

**Carried from dropped sections (original wording)**:

- **FR-029 / Module A-09**: Payment System Configuration; deposit, split payment, refund ladder, payment options per region and currency, and commission settings are managed here (deposit rate, its calculation, and the new-bookings-only rule: REQ-029-013, REQ-029-015, REQ-029-016; installment options and cutoff rules; commission default 15-25% range, per-provider or global settings).
- Payment processor for deposits/installments/refunds (PCI compliant); retry with backoff within the fixed post-acceptance hold; failure never extends the hold.

---

## Dependencies

Related FRs:

- FR-001: Auth & Profile; required for authenticated patient actions and identity unmasking post-payment.
- FR-004: Quote Submission; provides the Option/date-price records that carry the pre-scheduled appointment and price.
- FR-005: Subquote Comparison & Acceptance; supplies the immutable accepted subquote and inherited parent snapshot and triggers booking entry.
- FR-007 and FR-007B: Payments and Installments; deposit capture, schedules, refunds.
- FR-020: Notifications; confirmations, reminders, and alerts.
- FR-030: Notification Rules & Configuration; booking confirmation/reminder templates and notification policy rules.
- FR-026: App Settings & Security; owns the slot-hold duration and the "hold expiring soon" reminder lead time.
- FR-010: Post-confirmation treatment execution starts on arrival; owns the Check In rule.
- FR-011: Aftercare & Recovery Management; owns the aftercare reassignment screen.
- FR-029: Payment System Configuration; deposit, split payment, refund ladder, payment options per region and currency, and commission settings.

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

1. Given a confirmed booking and a patient cancellation request received through support, When an admin cancels the booking <15 days prior with a reason on Screen 9, Then the booking and inquiry become `Cancelled`, the accepted quote stays `accepted`, the action is audited, `booking.cancelled` is sent, and the refund follows the refund ladder set in FR-029.
2. Given a confirmed booking, When the patient opens the booking, Then no in-app cancel action is shown and a "Contact support" action is shown instead.
3. Given a confirmed booking, When the provider withdraws or drops out, Then the booking carries `supportRequired` with cause `ProviderFault` and payment, payment reminders, and revive are blocked, and at the admin submit of the transfer the booking is cancelled with cause `ProviderFault`; an admin can transfer the patient to a replacement provider in the same inquiry through an admin-authored replacement quote and a new admin-authored acceptance, the single supersession record linking the original AcceptanceEvent to the new one is written at the replacement acceptance, and the patient pays no cancellation fee.
4. Given an `Aftercare` booking, When the provider drops out of aftercare, Then the booking stays `Aftercare`, no new acceptance or payment is created, and an admin reassigns the aftercare provider or team through FR-011.
5. Given a confirmed booking whose provider is suspended or deactivated, When the status takes effect, Then the booking is cancelled with the provider-status cause, an admin rehomes the patient through the Alternative Flow B5 transfer, the patient is refunded everything paid, pays no cancellation fee, and the replacement booking takes a new payment.
6. Given an `In Progress` booking with a provider fault, When the admin resolves it on Screen 11, Then the admin sets the patient refund amount from zero up to the full amount paid with a mandatory reason, the decision is audited, the refund comes out of the held payout (or is deducted from the provider's next payout if it was already released), and the provider's payout for the booking stays held until the chosen route completes.
7. Given a `Cancelled` booking that still carries `supportRequired` and no replacement acceptance follows, When an admin uses Close inquiry on Screen 6, Then the inquiry becomes `Cancelled`, the marker is cleared with an audited resolution, and the patient receives the admin-close variant of `inquiry.cancelled` while no provider is notified.
8. Given a booking with a pending provider fault, When an admin cancels it on Screen 9, Then the booking and inquiry become `Cancelled` with cause `ProviderFault`, the patient is refunded in full with no cancellation fee, and the marker is resolved.

### Edge Cases

- Payment succeeds but confirmation email fails: confirmation must still be visible in-app; retry email (REQ-006-071).
- A stale or forged booking handoff references a slot not exclusively held by its AcceptanceEvent: reject it before payment initiation and leave the valid reservation unchanged.
- Installment plan default before deadline: flag booking, notify admin, patient and provider; apply policy (FR-007B REQ-007B-019 and REQ-007B-020). (REQ-006-080)
- The booking reaches `In Progress` while a provider fault is pending: the Screen 10 submit re-checks the status, transfers nothing, and sends the admin to Screen 11 (REQ-006-081).
- Provider emergency closure after acceptance: handled as provider fault; before treatment starts the admin transfers the patient to a replacement provider in the same inquiry (Alternative Flow B5); while `In Progress` the admin moves the booking to `Aftercare` with an aftercare reassignment or cancels it (Alternative Flow B7).
- Provider suspended or deactivated while the patient is paying: the booking-confirming payment step revalidates provider eligibility and rejects the payment before the gateway is called. If a capture still completes concurrently, record it, keep the booking `Cancelled` with the provider-status cause and `supportRequired`, and treat the captured amount as paid money refunded in full under the B4 payment terms (see Provider-Status Cancellation) while the admin rehomes the patient (Alternative Flows B4 and B5).
- Payment failure after subquote acceptance: the single hold that started at acceptance (FR-026 duration, default 48 hours) is never extended; retry is allowed only while it is active; on expiry, set `Payment Window Expired`, release the hold, block payment against that selection, and do not reopen the parent quote or accepted subquote.
- Two patients attempt to accept subquotes with the same slot simultaneously: the atomic acceptance transaction creates one exclusive hold and one AcceptanceEvent; the losing attempt receives a clear unavailable-slot error and creates no booking handoff.
- Patient submits payment while inquiry is being cancelled concurrently: system MUST perform atomic pre-booking validation at payment submission time (not just at screen entry). If inquiry transitions to "Cancelled" between screen load and payment submission, payment MUST be rejected with message "This inquiry has been cancelled" and no charge processed. Payment gateway must not be called if inquiry is cancelled (REQ-006-073).
- Patient is on Screen 1 when inquiry cancellation notification arrives: system SHOULD use real-time push (WebSocket/SSE) to transition Screen 1 to blocked state without requiring page refresh (REQ-006-072).

---

## Functional Requirements Summary

### Core Requirements

- **REQ-006-001**: Patients MUST be able to proceed to payment after accepting one subquote; FR-006 MUST consume its package, date range, appointment, price, promotion, and inherited parent context without reselection.
- **REQ-006-002**: System MUST confirm booking only after successful deposit/initial installment and unmask patient identity to provider.
- **REQ-006-003**: System MUST require an exclusive appointment hold, keyed by provider, appointment date/time, and time zone, created atomically with FR-005 acceptance; reject any handoff that does not own the valid hold before payment initiation; and create the appointment record and convert the hold into a provider calendar block only after successful payment confirmation.
- **REQ-006-004**: System MUST enforce the cancellation policy, with refunds following the refund ladder set in FR-029 (rescheduling deferred to V2). Apart from the unpaid-balance case in REQ-006-016, only an admin MAY cancel a booking, from `Accepted`, `Payment Window Expired`, or `Confirmed` (and from `In Progress` only through the Cancel route of Screen 11), never from `Aftercare`, with a mandatory reason, confirmation, and audit entry; the booking and inquiry MUST become `Cancelled`, the accepted quote MUST stay `accepted`, and `booking.cancelled` MUST be sent. The refund MUST follow REQ-006-053. The patient MUST NOT have an in-app cancel action from acceptance onward and MUST be offered "Contact support" instead.
- **REQ-006-005**: System MUST hold the accepted subquote's appointment slot with one fixed hold that starts at subquote acceptance and lasts the FR-026 slot-hold duration (default 48 hours); payment failure MUST NOT extend or restart it. If the hold expires before the first payment succeeds, System MUST set the booking to `Payment Window Expired`, release the hold, create no appointment record, block payment against that accepted selection, and preserve the immutable AcceptanceEvent/snapshot without reopening the prior parent quote or accepted subquote. The hold is keyed by provider, appointment date/time, and time zone. Recovery is by the audited admin revive, or by admin cancellation on a support request followed by a new inquiry; the patient is offered the "Contact support" route and has no in-app retry.
- **REQ-006-015**: When a provider's suspension or deactivation becomes effective, System MUST cancel that provider's `Accepted` and `Confirmed` bookings with cause `ProviderSuspended` or `ProviderDeactivated` and an independent `supportRequired` marker, release holds/reservations/slots, block further payment, revalidate provider eligibility at booking-confirming payment, treat any racing capture as paid money refunded in full under the B4 payment terms (see Provider-Status Cancellation), retain the accepted snapshot and booking/payment history, write the supersession record only at the replacement acceptance, and let an admin rehome the patient to a replacement provider in the same inquiry through Alternative Flow B5, without restoration on reactivation (Alternative Flow B4; FR-015 A5/Screen 4). `In Progress` and `Aftercare` bookings MUST keep their status and receive the cause and `supportRequired` (Alternative Flows B7 and B6).
- **REQ-006-016**: `Payment Window Expired` MUST apply only to the first payment step (acceptance to deposit or first installment). A missed later installment or final payment MUST NOT cause `Payment Window Expired`, booking cancellation, or inquiry cancellation. The one exception is the unpaid balance of a booking paid with the Installments option on Screen 1 (the "deposit plan" of FR-029): when that balance is still unpaid at the cancellation point set in FR-029, counted in days after the due date of the first missed installment, System MUST cancel the `Confirmed` booking with closure cause `UnpaidBalance`, cancel the inquiry as in Alternative Flow B2, release the calendar block, void the remaining installments, send `booking.cancelled`, and apply the refund ladder. The rule is inactive until an admin sets that point, which has no default, and it applies only to bookings confirmed after the value is set.
- **REQ-006-017**: Admin MAY revive a `Payment Window Expired` booking to `Accepted` only through Screen 7 with a mandatory reason, a slot availability re-check, a check that the appointment is later than the new payment deadline, a new hold of the FR-026 duration, one promotion use taken again where the accepted promotion has a usage limit (re-reserved for a provider-selected promotion or patient code, taken again for an automatic promotion; the revive is rejected if the limit has no room), an audit entry, an unchanged AcceptanceEvent, and a mandatory "booking revived" notice to patient and provider. A revived booking MUST count again in the FR-014 pending-payment figures, aged from the start of its new hold (REQ-014-139). A revive MUST be blocked while the booking carries the marker of a pending provider fault. A revive MUST NOT extend the expired hold; it starts a new one, and the initial payment then MUST pass the Initial Payment Guard (REQ-007-017) against that new hold. Appointment date changes MUST be made through Screen 8 or the admin edit of the accepted quote's date range or appointment (REQ-005-023), both running the same checks (provider `Active`, slot availability, a feasible FR-007B plan recalculation, and for an `Accepted` booking an appointment later than the payment deadline), MUST NOT apply the FR-029 rescheduling fee, MUST update the booking's current appointment while the acceptance snapshot keeps the accepted baseline, MUST send `booking.rescheduled`, and MUST trigger an FR-008 travel review for any travel records already linked to the booking. No other manual status change is allowed.
- **REQ-006-018**: When the provider withdraws or drops out after acceptance and before treatment starts, System MUST set the `supportRequired` marker with the cause `ProviderFault` at the trigger, MUST, at the admin submit on Screen 10, re-check the booking status and cancel the booking with cause `ProviderFault`, release the hold or calendar block, keep the AcceptanceEvent unchanged, and let an admin transfer the patient to a replacement provider in the same inquiry through an admin-authored replacement quote and a new admin-authored acceptance that points to that quote, option, and date-price row (Alternative Flow B5, Screen 10; FR-004 Workflow 7 and Screen 8). A replacement quote that is not accepted MUST expire under the normal quote expiry, the inquiry MUST stay `supportRequired` without automatic cancellation, and the admin MAY author another replacement quote or, for a `Cancelled` booking that still carries the marker, close the inquiry (REQ-006-082). System MUST write the single supersession record linking the original AcceptanceEvent to the new one at the replacement acceptance, as one append-only insert; the B4 or B5 closure is recorded on the booking as its cause. A provider fault during `Aftercare` MUST NOT create a new quote, acceptance, or payment; the booking stays `Aftercare` and an admin reassigns the aftercare provider or team through FR-011 (Alternative Flow B6); the replacement booking MUST receive the carried-over passport and copied flight and hotel records flagged "travel-date review required" per FR-008, with the originals kept read-only on the closed booking.
- **REQ-006-019**: When a provider fault occurs while the booking is `In Progress`, System MUST keep the booking `In Progress`, MUST NOT cancel it automatically or create a replacement quote or acceptance, and MUST flag it `supportRequired` with the cause. Only an admin MAY resolve it on Screen 11 (Alternative Flow B7), with a mandatory reason, confirmation, and audit entry, by either moving the booking to `Aftercare` and reassigning the aftercare provider or team through FR-011 Screen 19, or cancelling the booking through Screen 9. The admin MUST also set the patient refund amount, from zero up to the full amount paid, under the same mandatory reason and audit entry, and System MUST hold the provider's payout for that booking from the fault until the chosen route completes, MUST take the refund from that held payout, and MUST deduct any shortfall from the provider's next payout when the payout was already released. The decision records the choice only: System MUST resolve the `supportRequired` marker and end the payout hold once the chosen route completes, by the Screen 9 submit or the FR-011 Screen 19 submit.
- **REQ-006-020**: System MUST block an admin revive (Screen 7), an admin appointment change (Screen 8), and an admin-authored replacement acceptance (Screen 10) when the provider concerned is `Suspended` or `Deactivated` at submit, MUST change nothing, and MUST show the action-specific message that directs the admin to cancel the booking, to the provider-fault transfer, or to another replacement provider (Admin Status and Date Intervention Rules; FR-015 Rule 9). The messages are: revive, "This provider is suspended or deactivated, so this booking cannot be revived. Cancel the booking instead."; appointment change, "This provider is suspended or deactivated, so this appointment cannot be changed. Use the provider-fault transfer instead."; replacement acceptance, "This provider is suspended or deactivated, so this replacement quote cannot be accepted. Choose another replacement provider."
- **REQ-006-071**: After a successful payment, System MUST keep the booking confirmation visible in the app even when the confirmation email fails; retrying the failed delivery belongs to the notification service (REQ-030-008).
- **REQ-006-072**: When the parent inquiry is cancelled while the patient is on Screen 1, System MUST move Screen 1 to its blocked state at once, without a page refresh.
- **REQ-006-073**: System MUST check that the parent inquiry is not cancelled at the moment the payment is submitted, in one atomic step, not only when the screen is opened. If the inquiry has been cancelled, System MUST reject the payment with the message "This inquiry has been cancelled" and take no charge.
- **REQ-006-074**: An admin MAY make an audited emergency edit that changes only the appointment time on the same date and the booking notes, with a mandatory reason; System MUST keep the full before and after history of every emergency edit. An emergency edit MUST NOT change the appointment date, the price, the package, the provider, or the clinic, MUST NOT set the booking status, and MUST NOT change payment records or money terms, which stay immutable; revive, appointment change, cancellation, and the provider-fault transfer keep their own guarded steps and checks, and the acceptance snapshot stays unchanged.
- **REQ-006-081**: From the trigger of a provider withdrawal or drop-out until the admin submit on Screen 10, System MUST keep the booking in its status with the `supportRequired` marker and the cause `ProviderFault`, MUST block payment, payment reminders, and revive against it, and MUST NOT let its hold expire. At the Screen 10 submit System MUST re-check the booking status: only `Accepted`, `Confirmed`, or a `Cancelled` booking that still carries the marker from the provider-status cascade proceed, and a booking that has reached `In Progress` MUST go to Alternative Flow B7. An admin cancellation of a booking with a pending provider fault MUST take the cause `ProviderFault`, the full refund, and no cancellation fee, and MUST resolve the marker.
- **REQ-006-082**: An admin MAY close the inquiry of a `Cancelled` booking that still carries the `supportRequired` marker, through the Close inquiry action on Screen 6 with a mandatory reason; System MUST set the inquiry to `Cancelled`, clear the marker with an audited resolution, and send the patient the admin-close variant of `inquiry.cancelled` (REQ-020-076) saying that no replacement will follow. System MUST NOT notify any provider of the close (REQ-020-020) and MUST cancel any draft replacement quote of the inquiry without notice (REQ-004-111, REQ-003-127).
- **REQ-006-083**: System MUST start one refund per closure: Process Refund MUST be unavailable once the automatic refund of the closure has started, and the automatic refund MUST NOT start once Process Refund has been used for it.
- **REQ-006-084**: When the FR-016 suspension cascade cancels a patient's `Accepted`, `Payment Window Expired` or `Confirmed` booking, System MUST cancel it through the admin booking cancellation with the cause "Patient account suspended" (admin-initiated, request source Admin, the acting admin carried from FR-016) and the fixed reason "Booking cancelled because the patient account was suspended" sent to the patient and the provider, keep the admin justification in the audit entry only, and refund by the refund ladder set in FR-029, or by the provider-fault terms where the provider is at fault (REQ-016-219).
- **REQ-006-085**: When an admin has closed a treatment early with no fault (FR-010 Rule 17, REQ-010-116), System MUST show the patient, on the Screen 2 booking detail, a read-only note "Treatment closed early" with the decision date (the date the booking moved to `Aftercare`) and, only when a refund greater than zero was issued for the closure, the refund amount (a zero or absent refund shows no amount line); the note adds no patient action, no new booking status and no change to the closure flow.
- **REQ-006-086**: When an `In Progress` case cannot be completed and the provider is not at fault, an admin MAY close it early on Screen 11 with the route "Move to Aftercare, no fault" (Alternative Flow B9; FR-010 Rule 17, REQ-010-079, REQ-010-116), with a mandatory reason, confirmation and audit entry. System MUST move the booking to `Aftercare` from the decision date (the aftercare start date handed to FR-011), record the closure cause `NoFaultEarlyClose`, set no `supportRequired` marker and hold no payout, apply the admin-set patient refund amount (zero up to the full amount paid) as an exception refund under the FR-007 approval rule, make the provider's share (what is left after the refund and the Hairline commission) eligible for payout on the decision date with no waiting window, and signal FR-010 and FR-011 for the Closed Early record status and the post-op instructions.

### Data Requirements

- **REQ-006-006** (retired): Retention of booking, status history and audit records follows the system PRD, Platform-Wide Rules: One 10-year retention period; FR-006 does not restate it. Payment and refund state belong to FR-007.
- **REQ-006-007**: System MUST link each booking to exactly one FR-005 AcceptanceEvent, accepted parent quote identifier/version, accepted subquote identifier/version, immutable acceptance snapshot, and provider calendar slot. `acceptedSubquoteVersion` MUST equal `acceptedParentQuoteVersion`.

### Security & Privacy Requirements

- **REQ-006-008**: System MUST keep patient identity masked to the provider until the booking has reached `Confirmed` (payment confirmation), MUST keep it visible once unmasked, including after a later cancellation, and MUST encrypt PII at rest and in transit.
- **REQ-006-009**: System MUST log all booking state changes and accesses with user, timestamp, and reason.

### Integration Requirements

- **REQ-006-010**: System MUST integrate with Payment Service for deposits, installments, and refunds, and MUST use the exchange rate locked in the acceptance snapshot without relocking it.
- **REQ-006-011**: System MUST integrate with Notification Service for confirmations, reminders, and policy notices, and MUST trigger these FR-030 events: `booking.scheduled` (sent on patient acceptance and on an admin-authored replacement acceptance), `booking.rescheduled` (sent on an admin appointment change and on an emergency edit of the appointment time), `booking.cancelled` (sent on any booking cancellation with the reason or cause, and with the cancellation fee and the refund amount filled in by the system: an admin cancellation, a provider drop-out at the Screen 10 submit, and a system cancellation for an unpaid balance (cause `UnpaidBalance`, which an FR-007B installment plan that defaults and stays unpaid reaches at the cancellation point of Alternative Flow B8); not for a provider withdrawal, which FR-004 announces through `quote.withdrawn`), `booking.hold_expiring_soon`, `booking.payment_window_expired`, `booking.revived`, `booking.provider_fault_replacement` (sent to the patient and the admin at the admin submit of the provider-fault transfer; a withdrawal is announced before it by `quote.withdrawn`, a drop-out by `booking.cancelled` at the same submit, and a provider suspension or deactivation by this event only, REQ-030-044), `booking.confirmed` (sent when the first payment confirms the booking), and `booking.appointment_reminder` (sent twice by default, 7 days and 1 day before the appointment date, as FR-030 sets in REQ-030-048). The patient notice sent at Close inquiry is the admin-close variant of `inquiry.cancelled`, whose event and template are owned by FR-020 and FR-030 (REQ-020-076). Recipients, message content, and whether each notice is mandatory are owned by the notification Rules in FR-020 (for example REQ-020-021) and FR-030 and are not restated here. FR-004 is the only producer of `quote.withdrawn`; FR-006 does not emit it and reacts to it by starting the provider-fault transfer in Alternative Flow B5.

### Configuration Requirements

- **REQ-006-012** (retired): The deposit percentage setting, its calculation, and the rule that a change applies to new bookings only are owned by **FR-029: Payment System Configuration** (REQ-029-013, REQ-029-015, REQ-029-016); FR-006 does not restate them.
- **REQ-006-013**: System MUST read the slot-hold duration (default: 48 hours) and the "hold expiring soon" reminder lead time from FR-026 and MUST NOT keep a separate FR-006 hold setting. When the Settings API is unavailable as a hold is placed (subquote acceptance or admin revive), System MUST block the action so it can be retried and MUST NOT use a stale or guessed duration (REQ-026-144).
- **REQ-006-014**: System MUST verify the parent inquiry is not in "Cancelled" status before allowing entry to the booking/payment flow. If cancelled, system MUST block entry and display a read-only blocked state (Screen 1 blocked state) with clear messaging.

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-11-22 | 2.16 | Requirements graph programme baseline: PRD compressed to the checklist structure (each rule stated once, field rows tagged with graph field ids, dropped classes removed). No rule changes. Earlier history (v1.0 to v2.15) and the change requests CR-FR006-20260915-01, CR-FR006-20261016-01, CR-FR006-20261027-01 and CR-FR006-20261027-02 (also cited: CR-FR015-20261013-01) are in `archived/prd-baseline-2026-11-08/` and in git history. | Product Owner / Documentation |
| 2026-11-23 | 2.17 | Independent compression review: 2 clause(s) from dropped sections restored in original wording under Business Rules. No rule changes. | Product Owner / Documentation |
| 2026-11-23 | 2.18 | FR-005 r1 logic review, finding N8 and the owner ruling of 2026-11-23 (the admin edit of the accepted quote is kept): REQ-006-067 names the admin edit of the accepted quote's date range or appointment (REQ-005-023) beside the audited admin appointment change as a way to change the date. | Product Owner / Documentation |
| 2026-11-23 | 2.19 | FR-006 logic review, pass 1: one refund wording across B2, B4, B5, B7, Screens 6, 9, 10 and 11 (REQ-006-053); the Screen 11 refund is read-only on Screen 9, and the `supportRequired` marker and payout hold resolve once when the chosen route completes; `Aftercare` includes a treatment closed early on Screen 11, with the decision date as the aftercare start; B5 cancels the original booking at the Screen 10 submit; new Alternative Flow B8 (unpaid balance cancellation, cause `UnpaidBalance`); a date change through the accepted-quote edit runs the Screen 8 checks, the FR-029 rescheduling fee never applies, and Screen 8 blocks when no plan is feasible; Screen 7 checks the appointment against the new deadline; revive message for a suspended provider says to cancel; blocked Screen 1 keeps Contact Support and has one banner per cause; provider identity stays unmasked after `Confirmed`; `booking.cancelled` on any cancellation; Payment Window Expired under a suspended provider is cancelled through B2. | Product Owner / Documentation |
| 2026-11-23 | 2.20 | FR-006 logic review, pass 2: a provider withdrawal or drop-out now sets `supportRequired` with cause `ProviderFault` at the trigger, blocks payment, payment reminders and revive, keeps the hold until the Screen 10 submit, and Screen 10 re-checks the booking status at submit (`In Progress` goes to Alternative Flow B7) (REQ-006-081); an admin cancellation during that period takes cause `ProviderFault`, the full refund and no fee; new admin action Close inquiry for a `Cancelled` booking that still carries `supportRequired` (REQ-006-082); one refund per closure, so Process Refund and the automatic refund exclude each other (REQ-006-083); Cancel Booking on Screen 6 is not offered in `In Progress` or `Aftercare`; the B7 refund comes out of the held payout and any shortfall is deducted from the provider's next payout; the unpaid-balance cancellation point counts days after the due date of the first missed installment, applies only to bookings confirmed after it is set, and B8 voids the remaining installments; the emergency edit changes only the appointment time on the same date and the booking notes, with a field list on Screen 6; Screen 8 checks the new date against the payment deadline of an `Accepted` booking; the cancellation fee and refund amount are system-filled on `booking.cancelled`; Screen 11 is read-only after a decision until the route completes; stale wording removed (Screen 1 provider-cause banner, identity unmasking rule on Screen 4, the user story order and provider-fault scenario). | Product Owner / Documentation |
| 2026-11-25 | 2.21 | Cross-FR alignment. Screen 1 links to the full Cancellation Policy (FR-027) with the refund ladder numbers from FR-029 (REQ-006-030), and its Contact Support on blocked states opens a plain support request without a request type (REQ-006-037). Screens 2, 4 and 6 host the FR-008 Travel entry and sections, and a transfer carries travel over only when the replacement's travel path matches (REQ-006-042, REQ-006-057). The cause "Patient account suspended" is added for the FR-016 suspension cascade (REQ-006-084). Close inquiry sends the admin-close variant of `inquiry.cancelled` and notifies no provider (REQ-006-082). REQ-006-011 states the event each provider-fault case fires, the 7-day and 1-day appointment reminders and the unpaid-balance cause for a defaulted installment plan. A passed hold reminder is skipped after a raised lead time (REQ-006-036), a hold is not placed with the Settings API down (REQ-006-013), and a revived booking re-enters the FR-014 pending figures aged from its new hold (REQ-006-017). Completed follows the aftercare completion event whatever its outcome (REQ-006-060). The payout shortfall is a clinic balance entry, and the Payment Status list no longer shows At Risk (REQ-007-099). | Claude (AI Assistant) |
| 2026-11-25 | 2.22 | Owner ruling of 2026-11-25: a treatment closed early with no fault (FR-010 Rule 17) shows the patient a read-only status note "Treatment closed early" with the decision date and the refund amount when one was set, on the Screen 2 booking detail (new row Early Close Note, REQ-006-085). No new action, no new status, no flow change. | Claude (AI Assistant) |
| 2026-11-25 | 2.23 | Follow-up filing fixes: Screen 11 is now "Resolve In-Progress Case" and carries the early close with no fault as a third route (Alternative Flow B9, REQ-006-086, closure cause `NoFaultEarlyClose`, new Screen 6 action Close Case Early, No Fault), matching FR-010 Rule 17; Screen 2 Booking Status and Notes now list the statuses in which the screen is reachable (`Confirmed`, `In Progress`, `Aftercare`, `Completed`); the Early Close Note shows the refund amount only when a refund greater than zero was issued (REQ-006-085); the Cancellation Policy version shown at the tick is stored with the acknowledgment (REQ-006-038, new field `cancellation_policy_version_shown`). | Claude (AI Assistant) |

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
**Last Updated**: 2026-11-25
