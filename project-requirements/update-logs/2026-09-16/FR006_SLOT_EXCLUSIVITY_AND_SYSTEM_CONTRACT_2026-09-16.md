# FR-006 Slot Exclusivity and System Contract Alignment

**Date**: 2026-09-16
**Status**: Documentation findings resolved; implementation reconciliation and consolidated verification remain pending
**Decision owner**: Product Owner

## Summary

Applied the Product Owner-selected resolutions from the FR-006 v2.3 verification. Appointment conflict prevention now occurs when FR-005 creates the acceptance: acceptance and exclusive slot-hold acquisition are atomic, and a competing acceptance is rejected before an AcceptanceEvent, quote/inquiry state change, or booking handoff exists.

The follow-up FR-006 v2.5 verification resolution also makes every inherited accepted-snapshot field explicit on Patient Screen 1 and the Provider/Admin booking-detail screens, including visual plan, provider requirements, quote attachments, parent expiry, and AcceptanceEvent audit context.

## Updated Contracts

- **FR-005 v2.3**: Added the atomic slot-availability check, exclusive hold, unavailable-slot alternative flow, reservation provenance, requirement, and concurrency test boundary.
- **FR-006 v2.4**: Removed first-payment-wins wording; requires exclusive hold ownership before payment and conversion of that hold into the confirmed calendar block after successful payment.
- **FR-006 v2.5**: Completed field-level screen provenance for the accepted subquote and inherited parent snapshot across Patient Screen 1 and Provider/Admin booking details.
- **CR-FR006-20260915-01**: Extended the approved state and affected scope through v2.5 to record the selected acceptance-time conflict resolution and explicit inherited-snapshot screen provenance.
- **System PRD**: Added the exact AcceptanceEvent/version/slot linkage, acceptance-time exclusivity, terminal `Payment Window Expired` behavior, immutable no-reopen rule, and pending-versus-confirmed Booking definition.

## Boundaries

- FR-004, implementation source, schemas, APIs, migrations, and automated tests were not changed.
- FR-005 and FR-006 remain pending consolidated verification and implementation reconciliation.
- Existing unrelated workspace changes were preserved.

## Validation

- Targeted searches confirm no first-payment-wins or two-accepted-selections-for-one-slot wording remains in FR-006.
- FR-005, FR-006, the FR-006 Change Request, and the system PRD now assign appointment conflict prevention to the same atomic acceptance-time boundary.
- The system PRD now carries the terminal payment-expiry and pending Booking lifecycle required by FR-006 v2.4.
- Targeted table checks confirm Patient Screen 1 and both booking-detail screens explicitly source inherited provider, treatment, graft, clinician, note, visual-plan, requirement, attachment, expiry, version, and acceptance-audit context from the immutable snapshot.
- `git diff --check` passes for the `local-docs` repository.
