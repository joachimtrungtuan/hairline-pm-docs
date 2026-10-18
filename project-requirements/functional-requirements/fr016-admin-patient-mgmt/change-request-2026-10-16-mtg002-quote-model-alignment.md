# Change Request: Admin Booking Cancellation and Support-Routed Patient Requests

**Change Request ID**: CR-FR016-20261016-01
**Primary FR**: FR-016
**Triggering FR / Event**: SRC-MTG-002 quote model alignment, Product Owner decision log (2026-10-16) and final decisions (2026-10-18); FR-006 Screens 8 and 9, FR-003 stage list
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-16
**Decision Date**: 2026-10-18
**PRD Version Change**: v1.8 to v1.9 (v1.9 final audit corrections)
**Related Commit(s)**: Pending

---

## Decision Summary

The Product Owner decided that the patient can cancel in the app only while the inquiry is in the Inquiry or Quoted stage. After that the patient sees Contact Support, and only an admin can cancel the booking, from any booking state, with a mandatory reason and an audit entry (Q37). FR-006 sends `booking.rescheduled` to the patient and provider when an appointment changes (Q42). Every admin intervention needs its own screen with fields, validation, reason, confirmation, audit entry and notice (Q43). FR-016 had no place for support-routed requests, allowed booking changes outside FR-006, and used stage names that did not match FR-003.

## Baseline State

**Source version**: FR-016 v1.8, Main Flow, Alternative Flows A6 and A7, Screen 1: Patient List, Screen 7, Business Rules (Rule 7, Admin Editability), User Story 3, REQ-016-010, FR-006 dependency

The patient list used Scheduled, In-Progress and Complete as stages and listed Suspended as a journey stage. Account suspension cancelled active bookings with refund processing directly. Rule 7, User Story 3 and REQ-016-010 described a manual reschedule and cancel with refund, without naming the FR-006 actions or `booking.rescheduled`. There was no queue for patient cancellation or change requests raised through Contact Support.

## Approved State

**Target version**: FR-016 v1.9, same headings plus Alternative Flow A8, Screen 9: Booking Support Requests, REQ-016-031 and REQ-016-032

- Journey stage lists use the FR-003 stage list: Inquiry, Quoted, Accepted, Confirmed, In Progress, Aftercare, Completed, Cancelled. Suspended moves to a separate Account Status Filter (Active, Suspended, Deactivated).
- The Cancelled stage covers a patient cancellation in Inquiry or Quoted, an admin booking cancellation through FR-006, and a provider-caused cancellation.
- Flow A8 and Screen 9 list patient cancellation and change requests raised through Contact Support after acceptance. Each request opens the FR-006 Cancel Booking or Change Appointment action, or is declined with a reason; the outcome is audited and the patient is answered through the FR-034 support case (Q37, Q43).
- Admin booking cancellation and rescheduling happen only through the FR-006 actions, which notify the patient and provider through `booking.cancelled` or `booking.rescheduled` (Q42). This includes cancellations caused by patient account suspension.
- Refund amounts and cancellation fees follow the FR-006 payment placeholder.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Journey stage lists (Main Flow, Screen 1) | Scheduled, In-Progress, Complete and Suspended mixed into stages | FR-003 stage list; Suspended in a separate Account Status Filter | Alignment with FR-003 |
| Support-routed patient requests | No flow or screen | Flow A8 and Screen 9 with request fields, FR-006 actions, decline reason, outcome and audit entry | Q37, Q43 |
| Admin booking changes (A6, Rule 7, Admin Editability, User Story 3, REQ-016-010, FR-006 dependency) | Direct reschedule and cancel with refund | Only through FR-006 Change Appointment or Cancel Booking, with `booking.rescheduled` or `booking.cancelled` | Q37, Q42 |
| Functional requirements | REQ-016-001 to 030 | REQ-016-010 revised; REQ-016-031 and REQ-016-032 added | Q37, Q43 |

## Scope and Impact

### In Scope

- FR-016 stage wording, the support-routed request queue and the routing of admin booking changes to FR-006.

### Out of Scope

- Refund amounts, cancellation fees and payment movement (FR-006 payment placeholder).
- The FR-006 action screens themselves, which FR-006 owns.

### Affected Contracts

- **PRD owner**: `project-requirements/functional-requirements/fr016-admin-patient-mgmt/prd.md` — Main Flow; Alternative Flows A6 and A8; Screen 1; Screen 9; Rule 7; Admin Editability; User Story 3; REQ-016-010, REQ-016-031 and REQ-016-032; FR-006 dependency
- **Related FRs**: FR-003 (stage list and patient cancellation in Inquiry and Quoted only), FR-006 (Contact Support, Change Appointment Screen 8, Cancel Booking Screen 9), FR-020 and FR-030 (`booking.rescheduled` and `booking.cancelled`), FR-034 (support case for requests)
- **System documents**: `system-data-schema.md` (inquiry stage enum, support request link to booking)

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed
- **Required assessment**: Patient list stage filter and badges, account status filter, support request queue, routing to FR-006 actions, suspension cascade, audit logging, tests
- **Compatibility / rollout risk**: Stored stage values such as Scheduled or Complete need mapping to the FR-003 list
- **Data migration**: To be assessed

## Acceptance and Validation

- The patient list stage filter and badges show only the FR-003 stage list, and Suspended appears only in the Account Status Filter.
- A patient cancellation or change request raised through Contact Support after acceptance appears on Screen 9 and can be resolved only through the FR-006 action or declined with a reason.
- Every resolved or declined request has an audit entry, and the patient and provider receive `booking.cancelled` or `booking.rescheduled` when the booking changes.
- Suspending a patient account cancels active bookings only through the FR-006 Cancel Booking action.

## Approval and Traceability

- **Requested by**: Product Owner (MTG-002 quote model audit)
- **Approved by**: Product Owner, 2026-10-18, via `reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md` (documentation only)
- **Decision evidence**: SRC-MTG-002; final decisions Q37, Q42 and Q43 (2026-10-18); final audit stage-list and admin-intervention findings
- **Implementation reconciliation**: Required, not assessed
- **PRD change log**: v1.9 final audit corrections (2026-10-18)
- **Update log**: Combined 2026-10-16 MTG-002 log (controller-owned)
- **Supersedes**: None
- **Superseded by**: None
