# FR-005 Subquote Acceptance Model

**Date**: 2026-09-15
**Change Request**: CR-FR005-20260915-01
**PRD Version**: FR-005 v1.5 to v2.0
**Implementation Reconciliation**: Required

## Summary

FR-005 now treats the subquote as the atomic patient comparison and acceptance unit. Patients may compare subquotes across multiple providers, multiple parent quotes from the same provider, or within one parent quote. Each accepted subquote contains one package, date range, appointment, and price selection and inherits the shared provider and clinical context above it.

## Changed Contracts

- Replaced flat parent-quote comparison and acceptance with grouped parent quotes and selectable subquotes.
- Added complete subquote list, comparison, detail, and confirmation fields.
- Changed acceptance uniqueness from one parent quote to one subquote per inquiry.
- Added immutable acceptance snapshots with parent/subquote versions and full inherited/commercial context.
- Distinguished sibling Not Selected outcomes from competing parent quote cancellation.
- Defined the accepted subquote as the complete FR-006 handoff unit.
- Preserved separate parent-response and subquote-selection analytics.
- Reset FR-005 status to pending consolidated verification.

## Files

- `project-requirements/functional-requirements/fr005-quote-comparison-acceptance/prd.md`
- `project-requirements/functional-requirements/fr005-quote-comparison-acceptance/change-request-2026-09-15-subquote-acceptance-model.md`
- `project-requirements/sources/meetings/meeting-02-launch-quote-options-fund-release-and-payments.md`
- `project-requirements/sources/source-register.md`
- `project-requirements/update-logs/README.md`

## Evidence and Boundaries

- Evidence: SRC-MTG-002 D03–D06 and O01 plus the Product Owner clarification recorded on 2026-09-15.
- FR-004 remains unchanged and temporarily complete pending the later consolidated six-FR verification.
- FR-006 and system-document reconciliation remain deferred.
- No implementation or schema assessment was performed.

## Follow-up — 2026-09-16

- Resolved the post-verification version-provenance finding by defining the owning FR-004 parent aggregate `QuoteVersion` as the sole subquote revision source; `subquoteVersion` and `acceptedSubquoteVersion` equal the corresponding parent quote version.
- Replaced FR-005's generic Upcoming FR dependency with the explicit FR-006 handoff inputs and ownership boundary.
- Updated FR-004 to declare the upstream version rule, FR-005 to enforce it during acceptance, FR-006 to consume it, and the system PRD to preserve the invariant. Consolidated verification and implementation reconciliation remain pending.
