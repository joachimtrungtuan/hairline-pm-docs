# Product Requirements Document: Booking & Scheduling (FR-006)

**Module**: P-03: Booking & Payment | PR-02: Inquiry & Quote Management | A-01: Patient Management & Oversight
**Feature Branch**: `fr006-booking-scheduling`
**Created**: 2025-11-04
**Status**: Draft
**Source**: FR-006 from `system-prd.md`; aligned with Constitution (`constitution-summary.md`, `.specify/memory/constitution.md`); client transcriptions in `transcriptions/`; continuation from FR-004 (Quote Submission) and FR-005 (Quote Comparison & Acceptance); coordinated with FR-007/FR-007B (Payments)

---

## Executive Summary

Enable patients to convert accepted quotes into confirmed procedure bookings by selecting provider pre-scheduled time slots and paying deposits, while ensuring calendars are blocked, confirmations are issued, and rescheduling/cancellations follow clear rules. This module operationalizes the handoff from quote acceptance (auto-scheduled) to confirmed booking, enforcing deposit collection, provider calendar integrity, and patient/admin notifications.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-03)**: Booking confirmation flow and payment initiation after quote acceptance.
- **Provider Platform (PR-02)**: Calendar exposure and blocking, booking visibility, reschedule approvals.
- **Admin Platform (A-01/A-05/A-09)**: Oversight, policy configuration, financial reconciliation, notifications governance.
- **Shared Services (S-02/S-03/S-05)**: Payments, notifications, document storage.

### Multi-Tenant Breakdown

**Patient Platform (P-03)**:

- Review accepted quote details, pre-scheduled appointment slots, and select/confirm the slot.
- Pay deposit or choose installment plan within offered limits; view booking confirmation and itinerary basics.
- Request reschedule (≥14 days before procedure) and view cancellation policy/refund outcomes.

**Provider Platform (PR-02)**:

- Maintain and expose appointment availability pre-scheduled during quote creation; calendar auto-block on confirmed bookings.
- View accepted/confirmed bookings; receive confirmation notifications; enforce check-in workflow on arrival (handoff to FR-010).
- Approve/decline reschedule requests; apply cancellation policy outcomes; view deposit state (no card details).

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

- Direct patient↔provider chat (handled by FR-012 scope); SMS optionality is handled by S-03 settings.
- Travel booking details (handled by FR-008) beyond minimal itinerary placeholders.

### Entry Points

- Patient-initiated via mobile from the Accepted Quote detail view.
- Activation: Becomes available immediately after FR-005 quote acceptance.
- Confirmation: Occurs after successful deposit (or first installment) per FR-007/FR-007B, which also unmask patient identity and blocks provider calendar.

---

## Business Workflows

### Main Flow: Quote Acceptance → Booking Confirmation

**Actors**: Patient, Provider, Admin, Payment Service, Notification Service
**Trigger**: Patient accepts a quote (FR-005) with pre-scheduled time slot(s)
**Outcome**: Booking confirmed; deposit paid; provider calendar blocked; confirmations sent

**Steps**:

1. Patient opens Accepted Quote and reviews embedded appointment slot options pre-scheduled by provider.
2. Patient selects a slot and proceeds to payment (deposit or installment plan per FR-007B eligibility).
3. System calculates required deposit (20–30% range) and presents cancellation policy.
4. Patient confirms and submits payment.
5. Payment Service authorizes and captures deposit (or schedules installments).
6. System sets booking to Confirmed, unmasking patient identity to provider per constitution.
7. Provider calendar auto-blocks the confirmed slot and displays booking details.
8. Notification Service sends confirmations to patient and provider; Admin dashboard updates.

### Alternative Flows

**A1: Installment Plan Selected**:

- **Trigger**: Patient chooses an eligible installment plan.
- **Steps**:
  1. System computes max installments based on time until procedure; ensures completion ≥30 days before procedure.
  2. Schedule installment charges and reminders; mark booking Confirmed upon successful initial charge.
- **Outcome**: Booking confirmed; payment schedule tracked; reminders enabled.

**A2: Reschedule Request (Patient-Initiated)**:

- **Trigger**: Patient requests a new date ≥14 days before procedure.
- **Steps**:
  1. Patient submits reschedule request with alternative ranges.
  2. Provider proposes available slots; patient selects; deposit transfers to new booking.
- **Outcome**: New slot confirmed; notifications sent; calendar updated.

**B1: Payment Failure**:

- **Trigger**: Deposit payment fails.
- **Steps**:
  1. System retries up to 3 times and holds booking for 24 hours for retry.
  2. If still unsuccessful, release the slot; notify both parties.
- **Outcome**: Booking not confirmed; patient may retry; provider notified.

**B2: Late Reschedule/Cancellation**:

- **Trigger**: Request <14 days before procedure.
- **Steps**: System applies cancellation policy; provider/admin review required for exceptions.
- **Outcome**: Refunds per policy; status updated; audit logged.

---

## Screen Specifications

### Screen 1: Booking Details & Slot Selection (Patient)

**Purpose**: Review accepted quote, select provider-pre-scheduled slot, proceed to payment

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Selected Slot | select | Yes | One of provider pre-scheduled times | Must be available; not expired |
| Deposit Amount | number | Yes | 20–30% of total | Within configured bounds |
| Payment Option | select | Yes | Full or Installments (2–9) | Max installments based on date buffer |
| Cancellation Policy Ack | checkbox | Yes | User acknowledges policy | Must be checked before payment |

**Business Rules**:

- Show price breakdown (treatment + packages + fees) with deposit calculation.
- Disable Pay button until required acknowledgments are checked.
- Mask patient full identity until payment success; reveal only after confirmation.

**Notes**:

- Show time zone relative labels and local time conversions.
- Display slot expiry timer if quote/slot nearing expiration.

---

### Screen 2: Booking Confirmation & Itinerary (Patient)

**Purpose**: Display confirmed booking, reference number, next steps, basic itinerary

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Booking Reference | text | Yes | Unique reference | Format per HPID/booking scheme |
| Procedure Date | datetime | Yes | Confirmed slot | Must match provider calendar |
| Payment Status | badge | Yes | Deposit paid/installments scheduled | Must reflect latest payment state |
| Itinerary Summary | text | Yes | High-level pre-op steps | N/A |

**Business Rules**:

- Trigger notifications to patient/provider upon display.
- Provide reschedule option if within allowed window.

**Notes**:

- Include add-to-calendar links; link to travel booking (FR-008) when available.

---

### Screen 3: Bookings Dashboard (Provider)

**Purpose**: View accepted and confirmed bookings; manage reschedules and cancellations

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Calendar View | calendar | Yes | Booked/available slots | No overlaps on confirmed |
| Booking List | table | Yes | Status, patient anonymized/real name | Unmask only after payment |
| Actions | buttons | Yes | Confirm reschedule, apply policy | RBAC enforced |

**Business Rules**:

- Auto-block calendar upon confirmation; enforce no manual double-booking.
- Reschedule approvals required; audit all actions.

**Notes**:

- Show payment summary figures without revealing card data.

---

## Business Rules

### General Module Rules

- Booking is confirmed only after successful deposit or first installment charge.
- Provider calendars must be accurate; confirmed bookings auto-block times; no overlaps allowed.
- All timestamps shown in patient's local timezone; provider view shows both local and clinic time.

### Data & Privacy Rules

- Patient identity remains masked to provider until booking is Confirmed (payment success).
- Booking, payment, and personal data are encrypted at rest and in transit; audit logs are immutable.
- Retain booking and financial records ≥7 years; hard deletes prohibited (soft-delete/archive only).

### Admin Editability Rules

**Editable by Admin**:

- Cancellation policy schedule (thresholds and refund percentages) and reschedule cutoffs.
- Notification templates for booking confirmations/reminders; booking confirmation content.
- Commission settings and deposit range constraints within policy.

**Fixed in Codebase (Not Editable)**:

- Password policy and OTP length; identity unmasking rule tied to payment confirmation.
- Audit logging enablement and retention guarantees.

**Configurable with Restrictions**:

- Payment options availability per region/currency (cannot alter gateway compliance requirements).

### Payment & Billing Rules

- Deposit required to confirm booking (20–30% of total); final payment per FR-007 schedule.
- Installments must complete ≥30 days before procedure; failures trigger retries, then flag for admin.
- Refunds per cancellation policy example in `system-prd.md`; provider cancellations require admin approval and full refund.
- Prices shown in patient’s currency; exchange rate locked at acceptance; payouts per locked rate.

---

## Success Criteria

### Patient Experience Metrics

- **SC-001**: Patients can confirm a booking in ≤3 minutes from accepted quote.
- **SC-002**: 90% of patients complete deposit on first attempt.
- **SC-003**: Booking confirmation and receipts delivered within 1 minute of payment.

### Provider Efficiency Metrics

- **SC-004**: Calendar auto-block occurs within 10 seconds of booking confirmation.
- **SC-005**: 0% double-bookings due to system-enforced conflicts.
- **SC-006**: 95% of reschedule requests processed within 48 hours.

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

- **SC-014**: 85% of accepted quotes convert to confirmed bookings (aligned with system targets).
- **SC-015**: Deposit capture rate ≥ 80% within 24 hours of quote acceptance.
- **SC-016**: Refund disputes < 2% of total bookings.

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **FR-001 / Module P-01**: Auth & Profile; required for authenticated patient actions and identity unmasking post-payment.
  - **Integration point**: Booking flow requires verified patient and profile data.
- **FR-004 / Module PR-02**: Quote Submission; provides pre-scheduled slots and quote breakdown.
- **FR-005 / Module P-02**: Quote Comparison & Acceptance; triggers booking entry point.
- **FR-007 & FR-007B / Modules P-03, S-02**: Payments and Installments; deposit capture, schedules, refunds.
- **FR-020 / S-03**: Notifications; confirmations, reminders, and alerts.
- **FR-010 / PR-03**: Post-confirmation treatment execution starts on arrival.

### External Dependencies (APIs, Services)

- Payment processor for deposits/installments/refunds (PCI compliant); retry with backoff, hold booking for 24 hours on failure.
- Calendar/ICS generation for add-to-calendar links.

### Data Dependencies

- Active provider calendars with pre-scheduled slots from quotes (PR-02).
- Accepted quote with itemized pricing, currency, and discount applications (FR-004/019).
- Patient verified profile and medical status flags (P-01/P-02) for provider readiness.

---

## Assumptions

### User Behavior Assumptions

- Patients act within 24–72 hours after quote acceptance to book.
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

- Patient app to booking API for slot selection and payment initiation.
  - Data: accepted quote ID, slot ID, payment choice, acknowledgments.
  - Auth: patient token; RBAC enforcing ownership.
  - Errors: validation feedback; recoverable payment failures.
- Provider calendar API for blocking/unblocking; admin oversight API for audit and dispute actions.

### Scalability Considerations

- Expect hundreds of concurrent bookings during campaigns; ensure slot-hold locking performs under load.
- Background jobs for reminders and installment schedules; horizontal scaling for booking endpoints.

### Security Considerations

- MFA enforced for provider/admin tenants; RBAC everywhere.
- TLS 1.3 in transit; AES-256 at rest; no storage of card PANs; webhook signature verification.
- Full audit trail on state changes and access; rate limiting and anti-abuse protections on booking/payment endpoints.

---

## User Scenarios & Testing

### User Story 1 - Confirm Booking with Deposit (Priority: P1)

Patient confirms a booking from an accepted quote by selecting a pre-scheduled slot and paying the deposit.

**Why this priority**: Core conversion event from interest to revenue.

**Independent Test**: Accept a quote, select slot, pay deposit, verify confirmation, calendar block, and notifications.

**Acceptance Scenarios**:

1. Given an accepted quote with valid slots, When patient pays deposit, Then booking status is Confirmed and provider sees unmasked identity.
2. Given a confirmed booking, When confirmation is generated, Then both parties receive it within 1 minute.
3. Given confirmation, When viewing provider calendar, Then slot is blocked and non-overlapping.

---

### User Story 2 - Reschedule Before Deadline (Priority: P2)

Patient reschedules a confirmed booking ≥14 days before procedure; provider approves a new slot; deposit transfers.

**Why this priority**: Reduces churn and improves experience.

**Independent Test**: Submit reschedule, provider proposes new slot, patient confirms, verify updates and notifications.

**Acceptance Scenarios**:

1. Given a confirmed booking, When patient requests reschedule ≥14 days prior, Then provider proposes slots and upon selection booking updates.
2. Given a rescheduled booking, When deposit exists, Then deposit carries forward without penalty.

---

### User Story 3 - Apply Cancellation Policy (Priority: P3)

Late cancellation applies refund schedule; provider cancellation triggers full refund and admin approval flow.

**Why this priority**: Protects trust and platform economics.

**Independent Test**: Trigger patient late cancellation and provider cancellation; verify refund outcomes and audit logs.

**Acceptance Scenarios**:

1. Given a confirmed booking, When patient cancels <15 days prior, Then refund is computed per policy and logged.
2. Given a confirmed booking, When provider cancels with admin approval, Then patient receives full refund immediately and provider penalty tracked.

### Edge Cases

- Payment succeeds but confirmation email fails: confirmation must still be visible in-app; retry email.
- Simultaneous selection of the last slot: enforce atomic slot hold and first-success wins.
- Installment plan default before deadline: flag booking, notify admin and patient; apply policy.
- Provider emergency closure: admin-approved cancellation, full refund, suggest alternatives.

---

## Functional Requirements Summary

### Core Requirements

- **FR-006.1**: Patients MUST be able to select from provider pre-scheduled appointment slots and confirm booking.
- **FR-006.2**: System MUST confirm booking only after successful deposit/initial installment and unmask patient identity to provider.
- **FR-006.3**: System MUST auto-block provider calendar for confirmed bookings and prevent overlaps.
- **FR-006.4**: System MUST support rescheduling requests ≥14 days prior with provider approval.
- **FR-006.5**: System MUST enforce cancellation policy with scheduled refunds per policy.

### Data Requirements

- **FR-006.6**: System MUST store booking reference, slot, status history, payment state, refund state, and audit trail ≥7 years.
- **FR-006.7**: System MUST link bookings to accepted quotes, treatments, packages, and provider calendars.

### Security & Privacy Requirements

- **FR-006.8**: System MUST keep patient identity masked until payment confirmation; encrypt PII at rest and in transit.
- **FR-006.9**: System MUST log all booking state changes and accesses with user, timestamp, and reason.

### Integration Requirements

- **FR-006.10**: System MUST integrate with Payment Service for deposits, installments, refunds, and lock exchange rate.
- **FR-006.11**: System MUST integrate with Notification Service for confirmations, reminders, and policy notices.

### Marking Unclear Requirements

None.

---

## Key Entities

- **Entity 1 - Booking**: Represents a confirmed or pending booking derived from an accepted quote.
  - **Key attributes**: booking reference, quote ID, provider ID, patient ID, slot, status, payment state, refund state.
  - **Relationships**: One booking links to one accepted quote; one provider calendar entry; one patient.

- **Entity 2 - Calendar Slot**: Represents a provider’s pre-scheduled appointment time.
  - **Key attributes**: provider ID, start/end, capacity, hold/blocked flags, expiration.
  - **Relationships**: One slot can be held or blocked by at most one booking.

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-04 | 1.0 | Initial PRD creation | AI |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner |  |  |  |
| Technical Lead |  |  |  |
| Stakeholder |  |  |  |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-011 Aftercare & Recovery Management PRD
**Last Updated**: 2025-11-04
