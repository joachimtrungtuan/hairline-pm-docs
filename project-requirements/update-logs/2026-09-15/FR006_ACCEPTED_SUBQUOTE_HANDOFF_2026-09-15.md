# FR-006 Accepted Subquote Booking Handoff

**Date**: 2026-09-15
**Change Request**: CR-FR006-20260915-01
**PRD Version**: FR-006 v1.7 to v2.3
**Implementation Reconciliation**: Required

## Summary

FR-006 and the system PRD now consume the FR-005 accepted subquote as the atomic booking input. The handoff preserves the exact accepted package, date range, appointment, price, promotion, treatment plan, and inherited parent quote context without commercial reselection.

## Changed Contracts

- Replaced flat accepted-quote and quote-ID booking linkage with AcceptanceEvent, accepted parent/subquote identifiers and versions, and the immutable acceptance snapshot.
- Added explicit parent/subquote provenance to patient, provider, and admin booking screens.
- Prohibited package, date, appointment, and price reselection in FR-006.
- Changed payment-expiry and slot-conflict handling so it releases or blocks the slot without reopening a parent quote or rewriting the accepted selection.
- Bound `acceptedSubquoteVersion` and `acceptedParentQuoteVersion` to the same FR-004 aggregate `QuoteVersion`.
- Added terminal `Payment Window Expired` behavior when the configured hold expires; the slot releases and payment is permanently blocked against that accepted selection.
- Clarified that acceptance fixes the appointment and reserves its slot, while successful deposit or first-installment payment confirms the booking.
- Aligned system-level workflows, FR-005 requirements, exceptions, metrics, and glossary terminology.
- Reset FR-006 status to pending consolidated verification.

## Files

- `project-requirements/system-prd.md`
- `project-requirements/functional-requirements/fr006-booking-scheduling/prd.md`
- `project-requirements/functional-requirements/fr006-booking-scheduling/change-request-2026-09-15-accepted-subquote-handoff.md`
- `project-requirements/update-logs/README.md`

## Evidence and Boundaries

- Evidence: CR-FR005-20260915-01, FR-005 v2.2, and the Product Owner's reconciliation resolutions recorded on 2026-09-15 and 2026-09-16.
- FR-004 and FR-005 own their corresponding hierarchy, version, and acceptance contracts; their later reconciliation is tracked separately from this FR-006 update.
- No implementation, API, schema, migration, or automated-test assessment was performed.
- Consolidated FR-004/FR-005/FR-006 verification remains required before FR-006 returns to Verified & Approved.

## Follow-up — 2026-09-16

- Clarified that `acceptedSubquoteVersion` equals `acceptedParentQuoteVersion`, with both values sourced from the accepted FR-004 aggregate `QuoteVersion`.
- Applied the invariant to FR-006's handoff data, patient screen provenance, requirement, and Booking entity. No verification status or implementation claim changed.
- Added terminal `Payment Window Expired`: release the slot, block payment against the expired accepted selection, preserve the AcceptanceEvent/snapshot, and require a new current subquote or audited admin intervention without reopening prior records.
- Removed remaining wording that treated subquote acceptance as booking/slot confirmation; acceptance reserves the chosen slot and payment confirms the booking.
