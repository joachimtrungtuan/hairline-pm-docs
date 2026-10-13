# Change Request: Confirmed Booking Travel Context

**Change Request ID**: CR-FR008-20260929-01
**Primary FR**: FR-008
**Triggering FR / Event**: Approved FR-004 quote-option, FR-005 subquote-acceptance, and FR-006 booking-handoff restructures; Product Owner binary-path decision
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-09-29
**Decision Date**: 2026-09-29
**PRD Version Change**: v2.4 to v2.5
**Related Commit(s)**: Pending

---

## Decision Summary

FR-008 now coordinates travel for a confirmed FR-006 Booking using the immutable FR-005 AcceptanceEvent and accepted subquote snapshot. One accepted subquote resolves one FR-004 Quote Option package snapshot and one Option/Date-Price Record. Its included services determine the travel path; the booking and appointment determine the operational travel context. The Product Owner explicitly chose to retain the existing binary provider-included (Path A) and patient-self-booked (Path B) model, including no mixed flight/hotel submitters. A per-service or hybrid path is deferred.

## Baseline State

**Source version**: FR-008 v2.4, `Automated Trigger on Confirmed Status`, `Travel Path Determination`, `Architecture Notes`, and `Key Entities`

Travel requests referred to an inquiry/appointment reaching Confirmed. Travel records and API examples used flat `quote_id`; `PackageTravelInclusion` treated an accepted package as the path source and described path derivation on quote save. These references could not identify the exact accepted option, date-price, and booking when an inquiry contains multiple parent quotes and subquotes.

## Approved State

**Target version**: FR-008 v2.5, `Automated Trigger on Confirmed Booking`, `Travel Path Determination`, `Travel Context and Booking Lifecycle`, and `TravelContext`

FR-008 initializes one booking-owned TravelContext only after successful initial payment makes the FR-006 Booking Confirmed. It derives the same binary path from the accepted Quote Option's immutable `included_services` snapshot, stores that path and snapshot with the booking, and dispatches the applicable request once. Passport, flight, hotel, and itinerary records belong to the TravelContext. The accepted quote hierarchy and package-library ID/version remain read-only provenance. The updated PRD owns the detailed screen, requirement, entity, and API target contracts.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Workflow trigger | Inquiry/appointment Confirmed wording | FR-006 Booking Confirmed after successful initial payment | Separate acceptance and payment hold from confirmed travel operations |
| Travel choice | Accepted package or flat quote inclusions | Accepted subquote's quote-owned option inclusion snapshot | Preserve inline quote-local customization and the exact patient choice |
| Travel path | Derived at quote save and persisted on accepted package | Same binary rule derived from the immutable accepted snapshot and stored in TravelContext at booking confirmation | Avoid mutable library or unselected option drift |
| Record ownership | `quote_id` on travel records and API examples | Unique `booking_id` on TravelContext and `travel_context_id` on records; API requests identify confirmed booking | Prevent records attaching to the wrong quote option or appointment |
| Provenance | Flat quote/package reference | AcceptanceEvent, parent/subquote IDs and aggregate versions, Quote Option ID, Option/Date-Price ID, appointment timezone, inclusion snapshot | Support audit and unambiguous downstream handoff |
| Repeated events | No explicit guard | Idempotent context initialization and initial patient request | Prevent duplicate workflows and notifications |
| Booking changes | Unspecified | Close pending tasks on cancellation; audit date revalidation after approved appointment change | Preserve travel history and prevent stale itinerary dates |
| Provider/patient submission | Binary Path A and Path B with no submitter mixing | Preserved exactly; Path A collects provider records only for included flight/hotel, Path B collects patient records, transport-only remains Path B | Maintain the approved existing model |

## Scope and Impact

### In Scope

- FR-008 workflows, screen context and actions, binary path derivation, record ownership, API examples, requirements, entities, and traceability.
- Booking-confirmation timing, replay safety, and the minimal cancellation/date-change handoff needed for travel coordination.

### Out of Scope

- A hybrid or per-service submitter model; non-included Path A flight/hotel information remains uncollected in MVP.
- FR-004, FR-005, FR-006, system PRD, data schema, technical specification, product code, migrations, tests, and deployed API changes in this documentation pass.
- External travel booking, automatic rebooking, refund calculations, and cancellation economics.

### Affected Contracts

- **PRD owner**: `project-requirements/functional-requirements/fr008-travel-booking-integration/prd.md` — `Automated Trigger on Confirmed Booking`, `Travel Path Determination`, Screens 1–12, REQ-008-005/005b/007/011/014/018/020/025–029, and `Key Entities`.
- **Related FRs**: FR-004 owns quote-local option inclusions; FR-005 owns the accepted subquote and immutable AcceptanceEvent; FR-006 owns Booking, payment-window outcomes, confirmation, and accepted appointment; FR-007 supplies the payment result consumed by FR-006.
- **System documents**: System PRD, data schema, and technical specification require later controlled reconciliation against this approved contract.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed in this documentation pass.
- **Required assessment**: Booking confirmation event or equivalent signal, quote-to-booking data migration, travel API payloads and authorization, record keys, notification idempotency, patient/provider/admin UI, cancellations, date changes, and regression tests.
- **Compatibility / rollout risk**: High. Existing records keyed only by `quote_id` may be ambiguous when one parent quote has multiple patient-selectable subquotes.
- **Data migration**: To be assessed; do not infer accepted subquotes from a parent quote alone.

## Acceptance and Validation

- A pending accepted subquote, payment failure, hold expiry, or pre-payment cancellation creates no travel context or initial request.
- Successful initial payment creates exactly one TravelContext and one path-appropriate initial patient request for the confirmed booking, even if confirmation is retried.
- The accepted option's flight/hotel inclusions determine Path A or Path B, including transport-only → Path B; no mixed patient/provider flight or hotel submission is introduced.
- Records and screens identify the confirmed booking and accepted subquote, use the accepted appointment timezone, and keep parent quote and source package IDs as read-only provenance.
- Cancellation preserves submitted records and closes pending requests; an approved date change requires audited travel-date revalidation.
- Consolidated documentation verification and implementation/migration evidence are required before FR-008 returns to Verified & Approved or implementation reconciliation becomes Verified.

## Approval and Traceability

- **Requested by**: Product Owner
- **Approved by**: Product Owner
- **Decision evidence**: SRC-MTG-002 items D03–D05 and Product Owner clarifications incorporated into FR-004/005/006; Product Owner instruction dated 2026-09-29 to proceed with FR-008 while preserving the binary travel model
- **PRD change log**: FR-008 v2.5 row dated 2026-09-29
- **Update log**: `../../update-logs/2026-09-29/FR008_CONFIRMED_BOOKING_TRAVEL_CONTEXT_2026-09-29.md`
- **Supersedes**: None
- **Superseded by**: None
