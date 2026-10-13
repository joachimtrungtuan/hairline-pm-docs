# FR-008 Confirmed Booking Travel Context

**Date**: 2026-09-29
**Status**: Approved documentation revision; consolidated verification and implementation reconciliation pending
**Decision owner**: Product Owner

## Summary

Revised FR-008 from flat quote/package travel references to a confirmed Booking TravelContext sourced from the immutable FR-005 accepted subquote. The accepted FR-004 Quote Option supplies the travel-inclusion snapshot; its paired Option/Date-Price Record supplies the appointment. FR-006 successful initial payment starts travel coordination. The Product Owner retained the binary Path A / Path B model and deferred per-service or hybrid submitter responsibility.

## Updated Contracts

- **FR-008 v2.5**: Added booking-confirmation trigger and idempotence, accepted-choice provenance, booking-owned TravelContext, booking-keyed API examples, screen context, cancellation/date-change safeguards, and requirements REQ-008-025–029.
- **CR-FR008-20260929-01**: Records the v2.4 baseline, approved v2.5 state, unchanged binary path, affected contracts, and implementation reconciliation boundary.
- **Path A / Path B**: Flight or hotel in the accepted option produces Path A; neither produces Path B, including transport-only. Path A provider submission is limited to included flight/hotel services. No mixed patient/provider flight or hotel submission was added.

## Boundaries

- FR-004, FR-005, FR-006, system documents, implementation source, APIs, migrations, and tests were not changed in this documentation pass.
- Existing `quote_id` travel data and deployed endpoints require implementation and migration assessment. The revised API examples state a target contract, not deployed behavior.
- The previously verified FR-008 baseline does not constitute verification of v2.5. Consolidated cross-FR verification remains pending.
- Unrelated September 29 release-phase planning documents and their update-log entry were preserved.

## Validation

- FR-008 trigger, path derivation, screens, requirements, API examples, and entities now refer to the accepted subquote and confirmed booking consistently.
- The binary travel rule and no-submitter-mixing boundary were checked against the former v2.4 rule and the Product Owner's 2026-09-29 decision.
- `git diff --check` and targeted Markdown/traceability checks were run for the edited documents.
