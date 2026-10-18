# Change Request: MTG-002 Quote Model Alignment for Treatment Execution

**Change Request ID**: CR-FR010-20261016-01
**Primary FR**: FR-010
**Triggering FR / Event**: SRC-MTG-002 quote model verification and Product Owner decision log (2026-10-16)
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-16
**Decision Date**: 2026-10-16
**PRD Version Change**: v2.1 to v2.5
**Related Commit(s)**: Pending

---

## Decision Summary

The MTG-002 quote model audit found that FR-010 read accepted treatment data from live FR-004 records instead of the accepted snapshot, listed inconsistent accepted-selection identifiers, showed a calendar "Scheduled Date" for relative plan days, let admins reassign the provider and edit the procedure date without a governed flow, and had no scenarios for the accepted-option handoff (FR-010-1 to FR-010-6). The Product Owner approved M2 (snapshot for money only; plan, clinicians and grafts change after acceptance only through FR-010, by clinic or admin, audited, patient notified, snapshot unchanged), R7-1, R7-2 (relative days only), D3, D6 and D6-M (provider fault after acceptance is an FR-006 admin direct transfer with a payment placeholder) and M18 (suspension or deactivation after acceptance uses the same transfer). This request records the resulting changes to the FR-010 contract.

## Baseline State

**Source version**: FR-010 v2.1, `Business Workflows`, `Screen Specifications`, `Business Rules`, `Dependencies`, `User Scenarios & Testing`, `Functional Requirements Summary`, `Key Entities`

Parent Quote data supplied treatment, estimated graft count and clinicians, and the accepted Quote Option was read from FR-004 records. Dependencies named the Quote Option ID and option/date-price ID while Entity 1 listed only the Quote Option ID. Screen 2 showed a calendar "Scheduled Date" with no source. Plan and clinicians were locked at Check In, with no defined path between acceptance and Check In. Screen 8 let admins reassign the provider, edit the procedure date, and edit "all day fields" with "no read-only restrictions". Alternative Flow B5 cancelled the case on provider suspension or deactivation with "no automatic clinical reassignment, refund, or rebooking". No scenario covered the accepted-option handoff.

## Approved State

**Target version**: FR-010 v2.5, same headings, plus Alternative Flows A2 and B6, Admin Screen 9, Rules 13 to 16, REQ-010-026 to REQ-010-031, User Story 7 and Entity 5

- Price, currency, date range, appointment and promotion are read only from the accepted snapshot through the booking's AcceptanceEvent; FR-010 never reads accepted data from live FR-004 records or edits the snapshot (M2, R7-1).
- Entity 1 carries the full accepted-selection identifier set: AcceptanceEvent ID, accepted subquote ID and version, Quote Option ID, option/date-price ID, parent quote ID and version.
- FR-010 is the only path for post-acceptance changes to plan days, clinician set and estimated graft count (Alternative Flow A2): from `Confirmed`, the clinic until Check In or an admin at any later time, reason required, audited with before/after values (Entity 5), patient notified through the FR-030 event `treatment.plan_changed`, snapshot unchanged, money fields never changed (M2).
- Treatment details are locked while the booking is `Accepted` (unpaid). Audited changes through Alternative Flow A2 start only at `Confirmed`: the clinic from `Confirmed` until Check In, an admin from `Confirmed` onward, each emitting `treatment.plan_changed` (Q2).
- Plan days are relative only; Screen 2 shows "Day N of M" and never a calendar date (R7-2).
- FR-010 never reassigns the provider. Provider withdrawal, drop-out or replacement after acceptance is handed to FR-006 Alternative Flow B5 (Alternative Flow B6). The FR-006 payment placeholder applies: paid amounts move with the patient as credit, any unused part is refunded, no cancellation fee (D3, D6, D6-M).
- Provider suspension or deactivation, withdrawal or drop-out while the case is In Progress does not cancel the case: the booking stays In Progress with `supportRequired`, provider documentation is blocked, and the admin decides case by case through FR-006 Alternative Flow B7 to move the booking to Aftercare and reassign the aftercare provider through FR-011 Screen 19, or to cancel it. The FR-006 B5 transfer applies only before Check In (M18, Q45).
- Admin procedure-date editing is removed; appointment changes follow FR-006. Procedure Date on every screen is the current FR-006 booking appointment (Rule 14).
- The provider-fault transfer notice (`booking.provider_fault_replacement`) goes to the patient and admin; the replacement provider learns through `quote.accepted` and the patient receives `booking.scheduled` (Q32, Q42). The replacement case seeds its details from the admin-authored replacement quote's acceptance snapshot (Q35).
- No FR-010 actor sets a booking or case status by hand. No-show, postponement, interruption and provider closure requests are resolved only through the FR-006 Change Appointment and Cancel Booking actions or the provider-fault transfer; Admin Screen 8 Case Status is read-only (Q37, Q43).
- New Admin Screen 9 (Change Treatment Details) lets an admin change treatment details at any time from `Confirmed` onward with fields, validation, mandatory reason, confirmation, audit entry and `treatment.plan_changed`; the clinic form closes at Check In (Q44).
- Treatment record states are Awaiting Check In, In Progress, Completed and Cancelled; the record is created at booking confirmation (first successful payment) in Awaiting Check In, so audited treatment-detail changes before Check In have a record to change (Rule 2, Entity 1; Q46).

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Accepted data source | Live FR-004 parent quote and Quote Option | Accepted snapshot via AcceptanceEvent; treatment details seeded from it | M2, FR-010-1 |
| Identifiers | Inconsistent lists in Dependencies and Entity 1 | One full identifier set | FR-010-2 |
| Post-acceptance treatment changes | Undefined before Check In; admin "full edit" after | Alternative Flow A2, Rule 13, REQ-010-027, Entity 5, `treatment.plan_changed` | M2, FR-010-1, FR-010-5 |
| Treatment-detail change window | Clinic could change details while the booking was `Accepted` or `Confirmed` | Locked while `Accepted`; changes allowed from `Confirmed` (clinic until Check In, admin onward), each emitting `treatment.plan_changed` | Q2 |
| Plan day display | Calendar "Scheduled Date" | Relative "Plan Day Position", Rule 15, REQ-010-028 | R7-2, FR-010-3 |
| Provider reassignment | Admin editable on Screen 8 | Removed; Alternative Flow B6, Rule 16, REQ-010-029 route to FR-006 B5 | D6, D6-M, FR-010-4 |
| Suspension cascade | Cancel only, no rebooking | Before Check In: cancel, then admin rehoming through FR-006 B5. In Progress: booking stays In Progress with `supportRequired`; admin moves it to Aftercare with an aftercare reassignment or cancels it (FR-006 B7) | M18, Q45 |
| Procedure date | Admin editable | Read-only from accepted snapshot through the booking | M2, FR-010-4 |
| Testability | No handoff scenarios | User Story 7 and three edge cases | FR-010-6 |
| Admin status handling | Admin manually transitioned case status (B1 to B4, Screen 8) | Read-only status; FR-006 Change Appointment, Cancel Booking or provider-fault transfer only; REQ-010-031 | Q37, Q43 |
| Admin treatment-change screen | Button only, no screen | Admin Screen 9 with fields, reason, confirmation, audit and notice; REQ-010-030 | Q44 |
| Treatment record states | In Progress, Completed, Cancelled; creation point undefined | Awaiting Check In, In Progress, Completed, Cancelled; created at booking confirmation | Final audit, Q46 |

## Scope and Impact

### In Scope

- FR-010 accepted-data reads, treatment-detail change path, relative-day display, provider-fault routing, scenarios, requirements and entities.
- Minor corrections: CR-FR010-20260909-01 affected-contract screen numbers (FR-010-7) and vocabulary (FR-010-8); CR-FR010-20260910-01 marked superseded in part.

### Out of Scope

- Refund, fund-release, payment-allocation override and later-instalment mechanics (payment pass; FR-007, FR-007B, FR-017).
- Product-code, API, database or UI implementation changes.

### Affected Contracts

- **PRD owner**: [`prd.md`](./prd.md) — Module Scope; Alternative Flows A2, B1 to B6; Screens 1, 2, 4, 5, 6, 7, 8, 9; Rules 1, 8, 11, 12 to 16; Currency Rule; Dependencies; Integration 1 and 3; User Story 7; Edge Cases; REQ-010-007A, 012, 025 to 031; Entities 1 and 5
- **Related FRs**: FR-004 (blocks quote edits after acceptance); FR-005 (AcceptanceEvent, snapshot, supersession, admin-authored replacement acceptance); FR-006 (Alternative Flow B5 provider-fault transfer and payment placeholder, `booking.provider_fault_replacement`, admin Change Appointment and Cancel Booking actions, Screen 6 link to FR-010 Screen 9); FR-015 (suspension cascade after acceptance); FR-020 and FR-030 (`treatment.plan_changed`, mandatory patient notice); FR-007, FR-007B, FR-017 (payment placeholder mechanics)
- **System documents**: `system-data-schema.md` (treatment record identifiers, current treatment details, treatment-detail change audit table, relative plan days, treatment record status values and creation point); `system-technical-spec.md` and `system-prd.md` (FR-010 snapshot read and change path)

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed
- **Required assessment**: Booking-to-treatment payload and identifiers, treatment record persistence, treatment-detail change API and audit, notification event, provider and admin screens (removed reassignment and date edit), relative-day display, regression tests
- **Compatibility / rollout risk**: Code reading live quote records or allowing admin provider reassignment would diverge from the accepted snapshot and bypass the FR-006 transfer
- **Data migration**: To be assessed

## Acceptance and Validation

- FR-010 contains no read of accepted data from live FR-004 records and no calendar conversion of plan days.
- Every post-acceptance plan, clinician or graft change is audited, notifies the patient through `treatment.plan_changed`, and leaves the snapshot and money fields unchanged.
- No clinic or admin can change plan, clinicians or graft estimate while the booking is `Accepted`; the same change succeeds once the booking is `Confirmed` and emits `treatment.plan_changed`.
- Provider withdrawal, drop-out, replacement, suspension and deactivation route to FR-006 Alternative Flow B5 before Check In and to FR-006 Alternative Flow B7 while In Progress; no In Progress case is cancelled automatically or given a replacement acceptance.
- A treatment record in Awaiting Check In exists for every `Confirmed` booking.
- No FR-010 screen or flow lets a user set a booking or case status by hand.
- An admin can change treatment details on Screen 9 for a `Confirmed`, `In Progress`, `Aftercare` or `Completed` booking, with reason, confirmation, audit entry and `treatment.plan_changed`.
- No FR-010 table cell contains a literal pipe character.
- Reconciliation stays `Required` until payload, persistence, UI, notification and regression evidence confirm the contract.

## Approval and Traceability

- **Requested by**: Product Owner
- **Approved by**: Product Owner, 2026-10-16 (documentation approval via the MTG-002 decision log: M2, R7-1, R7-2, R7-3, D3, D6, D6-M, M18). Implementation reconciliation: required, not assessed.
- **Decision evidence**: [`mtg002-quote-model-decisions-2026-10-16.md`](../../../reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md); Product Owner Q-series answer Q2 (same decision log, section "Post-execution open questions"); decisions Q32, Q35, Q37, Q42, Q43, Q44, Q45 and Q46 (2026-10-18); findings FR-010-1 to FR-010-8 in [`mtg002-quote-model-verification-2026-10-16.md`](../../../reports/2026-10-16/mtg002-quote-model-verification-2026-10-16.md)
- **PRD change log**: FR-010 v2.2 and v2.3; v2.4 consolidated verification corrections (2026-10-18); v2.5 final audit corrections (2026-10-18)
- **Update log**: Combined 2026-10-16 MTG-002 log (controller-owned)
- **Supersedes**: CR-FR010-20260910-01 (in part: accepted-data source)
- **Superseded by**: None
