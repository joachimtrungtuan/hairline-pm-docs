# Quote Comparison & Acceptance Module - Product Requirements Document

**Module**: P-02: Quote Request & Management | PR-02: Inquiry & Quote Management | A-01: Patient Management & Oversight  
**Feature Branch**: `fr005-quote-comparison-acceptance`  
**Created**: 2025-11-03  
**Status**: ✅ Verified & Approved  
**Source**: FR-005 from system-prd.md

---

## Executive Summary

The Quote Comparison & Acceptance module enables patients to review all provider quotes received for a submitted inquiry, compare details (treatment, dates, pricing, inclusions), and accept exactly one quote to proceed. Acceptance transitions the case from Quoted to Accepted and prepares the handoff to the subsequent Booking & Payment module. This module maintains strict privacy rules: provider access to patient full identity remains restricted until successful payment confirmation. The module preserves full auditability, honors quote expirations, and ensures non-selected quotes are automatically cancelled with appropriate notifications.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-02)**: Quote Request & Management  
- **Provider Platform (PR-02)**: Inquiry & Quote Management  
- **Admin Platform (A-01)**: Patient Management & Oversight  
- **Shared Services (S-03, S-06)**: Notification service, audit logging, retention/archival utilities

### Multi-Tenant Breakdown

**Patient Platform (P-02)**:

- View all quotes per inquiry within the Inquiry Dashboard (FR-003 Screen 8).  
- Inspect quote details via FR-004's patient quote detail screen (Screen 4) with added Accept functionality.  
- Accept exactly one quote (acceptance auto-cancels all other quotes for the same inquiry); see countdown to expiry.  
- Receive notifications for quote updates, expiries, and acceptance confirmation.  
- After acceptance, proceed to booking/payment flow entry point (next FR).

**Provider Platform (PR-02)**:

- Read-only visibility of acceptance outcome for their quotes.  
- Non-selected quotes auto-cancelled with reason “Other quote accepted”.  
- No patient PII is revealed by acceptance; full details remain locked until payment confirmation per constitution.

**Admin Platform (A-01)**:

- Global oversight of quote states and acceptance events across patients/providers.  
- Soft-delete/restore capabilities with audit trail.  
- Conflict resolution (rare): e.g., simultaneous accept attempts; manual remediation with rationale.

**Shared Services (S-03, S-06)**:

- Notifications for acceptance/expiry events and auto-cancellation of non-selected quotes.  
- Audit logging service for all state transitions.  
- Retention/archival utilities (soft delete only; no hard deletes).

### Communication Structure

**In Scope**:

- System → Patient: Quote update/expiry/acceptance notifications.  
- Patient → System: Accept action on eligible quotes (acceptance auto-cancels all other quotes).  
- Patient → Hairline Support: Ask questions about quotes via secure messaging (see FR-012; MVP channel: Patient ↔ Hairline Support).  
- System → Hairline Support: Notify support of patient quote questions within 5 minutes.  
- System → Provider: Acceptance outcome and auto-cancellation updates for non-selected quotes.  
- Admin → All: Oversight and policy-bound interventions.

**Out of Scope**:

- Direct patient-provider chat (see FR-012: Messaging & Communication).  
- Payment collection and invoice issuance (handled in Booking & Payment FR).  
- Revealing patient contact/identity to provider prior to payment confirmation.

### Entry Points

- Patient accesses from Inquiry Dashboard (FR-003 Screen 8) where quotes are displayed within the inquiry context, or via push/email notification.  
- Acceptance is available only while the target quote is non-expired and not withdrawn.  
- Upon acceptance, system locks competing quotes for the same inquiry and triggers booking handoff.

---

## Business Workflows

### Main Flow: Patient Accepts a Quote

**Actors**: Patient, System, Provider (notified), Admin (observer)
**Trigger**: Patient taps “Accept” on a valid, unexpired quote
**Outcome**: Inquiry transitions to Accepted; competing quotes auto-cancelled; booking handoff prepared

**Steps**:

1. Patient opens Inquiry Dashboard (FR-003 Screen 8) and views received quotes within the inquiry context.  
2. Patient taps "View Details" on a quote to open FR-004's patient quote detail screen (Screen 4).  
3. Patient reviews full quote details and taps "Accept" button (FR-005 enhancement to FR-004 Screen 4).  
4. Patient confirms acceptance with terms acknowledgment and summary confirmation modal.  
5. System validates eligibility (not expired, no prior acceptance for this inquiry).  
6. System sets chosen quote status to Accepted and inquiry stage to Accepted.  
7. System auto-cancels all other quotes for the same inquiry with reason "Other quote accepted."  
8. System sends notifications to patient and all affected providers.  
9. System prepares booking/payment handoff metadata to the next module (no payment collected here).  
10. System writes immutable audit entries for all state changes.

### Alternative Flows

**A1: Quote Expires During Review**:

- Trigger: Countdown reaches zero while patient is viewing details.  
- Steps: System disables Accept button; shows “Expired” badge and guidance to choose another quote.  
- Outcome: Patient can pick another available quote or await new quotes.

**A2: Simultaneous Acceptance Attempt**:

- Trigger: Patient attempts to accept a second quote after already accepting another (or after a race condition).  
- Steps: System prevents second acceptance; shows message referencing accepted quote.  
- Outcome: Exactly one accepted quote per inquiry is enforced.

**A3: Provider Withdraws Before Acceptance Completes**:

- Trigger: Provider withdraws quote just before patient confirms acceptance.  
- Steps: System re-validates eligibility at confirmation; if withdrawn, acceptance is blocked with explanation.  
- Outcome: Patient returns to inquiry dashboard to select another quote.

---

## Screen Specifications

### Patient Platform

#### Screen 1: Inquiry Dashboard with Quote Comparison (Enhanced from FR-003 Screen 8)

**Purpose**: Patient views submitted inquiry status, compares all received quotes, and accepts one quote

**Note**: This screen extends FR-003's Inquiry Dashboard (Screen 8) to include quote comparison and acceptance functionality. The quotes are displayed within the existing inquiry context.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Current Stage | badge | Yes | Inquiry stage (Inquiry/Quoted/Accepted/...) | Valid lifecycle value |
| Timeline | timeline | Yes | Chronological status changes | Timestamps present |
| Inquiry Summary | group | Yes | Read-only inquiry info | Complete and consistent |
| Quotes Received | list | Yes | Provider quotes with key highlights | Must list all non-archived quotes |
| Sort & Filter | controls | Yes | Sort/filter quotes (e.g., price, grafts, rating, date) | Criteria list must be defined |
| Compare Selection | checkbox | No | Select quotes to compare side-by-side (max 3) | Max 3 selected |
| Comparison View | panel | No | Side-by-side comparison of selected quotes | Renders only when ≥2 selected |
| Treatment | text | Yes | Treatment name from catalog | Read-only; per quote |
| Inclusions | chips | No | Package/customizations | Read-only; per quote |
| Included Services | checklist | No | Included services checklist | Derived from quote inclusions; per quote |
| Per-date Pricing | table | Yes | Price for each offered date | All dates priced; per quote |
| Appointment Slot (Pre-Scheduled) | datetime | Yes | Pre-scheduled appointment date/time for this quote | Read-only; sourced from FR-004 |
| Price per Graft | number | Yes | Derived unit price (total ÷ graft count) | Calculated; per quote |
| Provider Reviews | rating/number | No | Review rating and count | Read-only; sourced from FR-013 |
| Provider Credentials Summary | text | Yes | Licenses/certifications summary | Read-only; sourced from FR-015 |
| Estimated Travel Costs | currency | No | Estimated travel costs to destination | Derived from A-09 baseline travel estimate table (until FR-008 provides live estimates) |
| Expiry Timer | timer | Yes | Countdown until quote expiry | Derived from FR-004 settings; per quote |
| Medical Alerts | chips | Yes | Patient medical risk level | Read-only; from FR-003 |
| Actions | buttons | Yes | View Details, Accept, Ask Question | State-aware enabling; per quote; Ask Question routes to Hairline Support via FR-012 |
| Deadlines | datetime | Yes | Response/expiry deadlines | Future or past allowed |
| Next Actions | actions | Yes | Available user actions | Based on stage/permissions |

**Business Rules**:

- Quotes are displayed within the inquiry dashboard context (not a separate screen).  
- Expired/withdrawn quotes are visually disabled.  
- Exactly one acceptance permitted per inquiry.
- Patient can sort/filter quotes and compare up to 3 quotes side-by-side (criteria must include at least: total price, price per graft, graft count, review rating, soonest appointment slot).
- Patient can view quote details and accept directly from the dashboard.

#### Screen 2: Quote Detail with Accept Action (Extension of FR-004 Screen 4)

**Purpose**: Patient views full quote details and accepts quote

**Note**: This extends FR-004's Patient Platform Screen 4 (Quote Review) by adding the Accept button with terms acknowledgment and acceptance confirmation flow.

**Enhancements to FR-004 Screen 4**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Terms Acknowledgment | checkbox | Yes | Confirm understanding of policies | Required to proceed with acceptance |
| Accept Button | button | Yes | Accept this quote | State-aware (disabled if expired/withdrawn/already accepted) |
| Acceptance Confirmation Modal | modal | Yes | Summary confirmation before finalizing | Shows quote summary and next steps |

**Business Rules**:

- All quote details from FR-004 Screen 4 are displayed (read-only for patient).  
- Terms acknowledgment checkbox must be checked before Accept button is enabled.  
- Accept button is disabled if quote is expired, withdrawn, or another quote is already accepted.  
- Tapping Accept opens confirmation modal with quote summary and next steps.  
- Detail reflects latest provider edits (if any) and locks on acceptance.

#### Screen 3: Acceptance Confirmation Modal

**Purpose**: Confirm acceptance and show next steps before finalizing

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Quote Summary | group | Yes | Chosen quote summary (treatment, price, dates, provider) | Must reflect latest data |
| Terms Acknowledgment | checkbox | Yes | Confirm understanding (if not already acknowledged) | Required if not already checked |
| Next Steps | note | Yes | Booking & Payment handoff information | Read-only |
| Confirm | action | Yes | Finalize acceptance | Enabled when eligible |
| Cancel | action | Yes | Return to quote detail | Always available |

**Business Rules**:

- Modal appears after patient taps Accept button on quote detail screen (FR-004 Screen 4).  
- Confirmation is idempotent; duplicate confirmations do nothing.  
- Post-confirmation, modal closes and patient is directed to booking/payment entry.  
- Patient can cancel to return to quote detail screen.

### Provider Platform (Read-only in this module)

#### Screen 4: Quote Outcome Notification

**Purpose**: Inform provider of acceptance outcome

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Outcome | badge | Yes | Accepted/Expired/Cancelled (other accepted) | Enum validation |
| Reason | text | No | If auto-cancelled (other accepted) | Read-only |
| Audit Link | link | Yes | View version/audit history | Read-only |

### Admin Platform

#### Screen 5: Acceptance Oversight Dashboard

**Purpose**: Monitor acceptance events and manage exceptions

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Global Acceptance Table | table | Yes | All accept events with filters | Admin-only |
| Conflicts | badge | No | Flagged races or errors | Investigated by admin |
| Actions | actions | Yes | Soft delete/restore with reason | Audit enforced |

---

## Business Rules

### General Module Rules

1. A patient can accept exactly one quote per inquiry; subsequent acceptance attempts are blocked with guidance.  
2. Acceptance of one quote auto-cancels all competing quotes for the same inquiry with clear reasons and notifications.  
3. Acceptance does not reveal patient full identity to provider; full PII becomes accessible only after successful payment confirmation, per constitution.  
4. All acceptance-related state transitions are immutably audited (who, when, what, reason).  
5. Quotes that are expired, withdrawn, or archived are ineligible for acceptance.  
6. All deletes are soft deletes; no hard deletes permitted.

### Data & Privacy Rules

1. Patient identifiers remain anonymized to providers at this stage.  
2. All data in transit and at rest is protected according to platform policies.  
3. Audit logs must record acceptance event details and affected quotes.  
4. Retention: acceptance and related quote records retained ≥ 7 years.

### Admin Editability Rules

**Editable by Admin**:

- Resolve rare conflicts (e.g., simultaneous accept attempts) with reason.  
- Soft delete/restore acceptance records and quotes with justification (audited).  
- Configure notification behaviors via centralized settings (separate FR).

**Fixed in Codebase (Not Editable)**:

- Patient identity reveal policy: only post-payment confirmation.  
- Quote acceptance uniqueness constraint per inquiry.  
- Soft delete policy (no hard deletes).

**Configurable with Restrictions**:

- Acceptance confirmation copy/UX notes (content-managed); legal text controlled centrally.

### Payment & Billing Rules (for Handoff)

- Acceptance prepares booking/payment handoff; no funds are collected in this module.  
- Selected quote’s pre-scheduled appointment slot (date/time) and associated pricing feed the next module for payment intent creation.  
- On acceptance, the system MUST ensure the quote exchange rate is locked at the time of acceptance per FR-004 / System PRD pricing rules.  
- Pricing and discounts shown are those defined in FR-004; acceptance does not modify financial terms.
- Post-Acceptance Hold: After acceptance, the system reserves the pre-selected appointment slot for 48 hours to allow the patient to complete the initial payment (deposit or first installment) in FR-006. If payment is not completed within 48 hours, the reservation is released and the slot may be reallocated by the provider.

---

## Success Criteria

### Patient Experience Metrics

- **SC-001**: 95% of patients can compare and accept a quote within 3 minutes.  
- **SC-002**: <2% of acceptance attempts fail due to expired quotes (clear guidance shown).  
- **SC-003**: Patient satisfaction for quote review flow ≥ 4.5/5.

### Provider Efficiency Metrics

- **SC-004**: 100% of non-selected quotes auto-cancelled within 10 seconds of acceptance.  
- **SC-005**: 100% acceptance outcomes correctly reflected in provider dashboards.

### Admin Management Metrics

- **SC-006**: 100% acceptance events fully auditable with immutable logs.  
- **SC-007**: 95% of conflicts (if any) resolved within one business day.

### System Performance Metrics

- **SC-008**: Acceptance action completes in ≤ 2 seconds for 95th percentile.  
- **SC-009**: Notifications delivered within 30 seconds for 95% of events.  
- **SC-010**: Zero hard deletes; archival retrieval success = 100%.

### Business Impact Metrics

- **SC-011**: ≥ 30% of inquiries with quotes proceed to acceptance.  
- **SC-012**: ≥ 90% of accepted quotes proceed to booking initiation (next FR) within 48 hours.

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **FR-003 / P-02, PR-02, A-01**: Inquiry submission & distribution (source inquiry and medical context).  
- **FR-004 / PR-02**: Quote submission & lifecycle (quotes, expiry, withdrawal, audit).  
- **FR-020 / S-03**: Notifications & alerts (event delivery).  
- **FR-012 / P-06, A-10**: Messaging & communication (Patient ↔ Hairline Support quote questions).  
- **FR-013 / P-02, A-01**: Reviews & Ratings (source for provider review rating/count shown in comparison).  
- **FR-015 / A-02**: Provider Management & Onboarding (source for provider credentials/licenses/certifications summary).  
- **FR-008 / P-03** (or **A-09**): Travel cost data/estimation inputs for "Estimated Travel Costs" field.  
- **Upcoming FR / P-03, A-05**: Booking & Payment (payment intent, invoice, PII reveal post-payment).  
- **A-09**: System settings (legal copy, terms acknowledgment text).

### External Dependencies

- None specific beyond shared notification services and standard platform integrations.

### Data Dependencies

- Inquiry (from FR-003), Quotes (from FR-004), Notification endpoints (FR-020), Legal/policy text (A-09).

---

## Assumptions

### User Behavior Assumptions

- Patient has exactly one active inquiry for which quotes exist.  
- Patients do not have an explicit "decline" action; non-selected quotes are auto-cancelled on acceptance or expire by policy.  

### Technology Assumptions

- Providers have submitted valid, non-expired quotes per FR-004.  
- Booking & Payment module is available for immediate handoff post-acceptance.

### Business Process Assumptions

- Acceptance alone does not disclose patient full identity to provider; reveal occurs after successful payment confirmation.  
- Admin legal copy and acknowledgment text are centrally managed.  

---

## Implementation Notes

### Technical Considerations

- Idempotent acceptance: repeat requests do not create multiple accepted states.  
- Concurrency control to prevent race conditions on multiple quotes for same inquiry.  
- Append-only audit trail for acceptance and auto-cancellations.

### Integration Points

- Consumes quote data from FR-004; updates quote/inquiry states; triggers notification service; emits booking handoff payload.

### Scalability Considerations

- Support high-volume acceptance during peak times without delays to notification or state transitions.

### Security Considerations

- Enforce privacy rules: no PII reveal on acceptance; RBAC for all actors; full audit of state transitions; encryption at rest/in transit.

---

## User Scenarios & Testing

### User Story 1 - Accept a Quote (Priority: P1)

Patient compares received quotes and accepts one to proceed to booking.

**Independent Test**: Accept one quote; verify competing quotes auto-cancel; verify audit and notifications.

**Acceptance Scenarios**:

1. Given a valid, unexpired quote, when patient accepts, then the quote becomes Accepted and others auto-cancel.  
2. Given an already accepted inquiry, when patient attempts to accept another quote, then system blocks with guidance.  
3. Given acceptance success, when system prepares handoff, then booking entry is available without collecting payment in this step.

### User Story 2 - Handle Expired Quote (Priority: P2)

Patient attempts to accept a quote that has expired.

**Independent Test**: Confirm acceptance is blocked; display expiry; allow selection of other quotes.

**Acceptance Scenarios**:

1. Given an expired quote, when patient views FR-004 quote detail screen or taps Accept, then system shows "Expired" badge and disables Accept button.  
2. Given multiple quotes with one expired, when patient views the inquiry dashboard, then expired quote is visually distinguished and other quotes remain available for acceptance.

### Edge Cases

- Network loss during acceptance: system retries safely; no duplicate accept states.  
- Simultaneous accept attempts across devices: first valid acceptance wins; others see informative message.  
- Provider withdraws during confirmation: acceptance blocked with explanation; return to inquiry dashboard.  
- Admin restores mistakenly cancelled quote (with reason): does not override prior acceptance; remains read-only history.

---

## Functional Requirements Summary

### Core Requirements

- **REQ-005-001**: System MUST allow patients to view and compare all quotes for an inquiry within the Inquiry Dashboard (FR-003 Screen 8).  
- **REQ-005-002**: System MUST allow patients to accept exactly one valid quote per inquiry.  
- **REQ-005-003**: System MUST auto-cancel all non-selected quotes for the same inquiry with reason and notifications.  
- **REQ-005-004**: System MUST block acceptance of expired/withdrawn/archived quotes with clear messaging.  
- **REQ-005-005**: System MUST prepare booking/payment handoff upon acceptance without collecting funds in this module.

### Data Requirements

- **REQ-005-006**: System MUST preserve immutable audit logs for acceptance and auto-cancellation events.  
- **REQ-005-007**: System MUST retain acceptance and related quote records for ≥ 7 years.

### Security & Privacy Requirements

- **REQ-005-008**: System MUST keep patient identity masked to providers until payment confirmation.  
- **REQ-005-009**: System MUST encrypt data at rest and in transit and enforce RBAC for actions.

### Integration Requirements

- **REQ-005-010**: System MUST integrate with FR-004 for quote states and FR-020 for notifications.  
- **REQ-005-011**: System MUST emit booking handoff payload to the Booking & Payment module.
- **REQ-005-012**: System MUST allow patients to filter and sort quotes by defined comparison criteria.  
- **REQ-005-013**: System MUST support side-by-side comparison view of up to 3 quotes.  
- **REQ-005-014**: System MUST display comparison differentiators: price per graft, review rating/count, provider credentials summary, included services checklist, and estimated travel costs.
- **REQ-005-015**: Patients MUST be able to ask questions about quotes through secure messaging (see FR-012; MVP channel: Patient ↔ Hairline Support).  
- **REQ-005-016**: System MUST notify Hairline support of patient quote questions within 5 minutes.  
- **REQ-005-017**: System MUST lock quote exchange rate at time of patient acceptance (per FR-004 pricing rules).

---

## Key Entities

- **AcceptanceEvent**: inquiryId, acceptedQuoteId, actorId (patient), timestamp, metadata (handoff)  
  - metadata includes pre-scheduled appointment slot (datetime + timezone) and handoff payload identifiers  
  - Relationships: belongsTo Inquiry; belongsTo Quote  
- **Quote** (from FR-004): id, providerId, status (Accepted/Expired/Cancelled - other accepted), expiresAt  
- **AuditEntry**: entityType, entityId, action, actorId, reason, before, after, timestamp

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-03 | 1.0 | Initial PRD creation for FR-005 | Product & Engineering |
| 2025-11-04 | 1.1 | PRD reviewed and verified | Product Owner |
| 2025-11-04 | 1.2 | Template compliance: moved Multi-Tenant Architecture to Module Scope; added MTA bullets; renamed Entry Points; restructured Assumptions into subsections | Product & Engineering |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | [Name] | [Date] | [Status] |
| Technical Lead | [Name] | [Date] | [Status] |
| Stakeholder | [Name] | [Date] | [Status] |
