# Change Request: MTG-002 Quote Model Alignment for Inquiry Submission and Distribution

**Change Request ID**: CR-FR003-20261016-01
**Primary FR**: FR-003
**Triggering FR / Event**: SRC-MTG-002 quote model verification and Product Owner decision log (2026-10-16); cross-FR check against FR-006 and FR-015
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-16
**Decision Date**: 2026-10-16
**PRD Version Change**: v2.8 to v2.9
**Related Commit(s)**: Pending

---

## Decision Summary

The Product Owner decided that a provider suspended or deactivated after acceptance follows the FR-006 provider-fault transfer: the booking is closed and an admin rehomes the patient to a replacement provider in the same inquiry. FR-003 still cancelled the whole inquiry in that case, which would leave no inquiry to rehome into. FR-003 now keeps the inquiry open.

## Baseline State

**Source version**: FR-003 v2.8, Workflow 2 Alternative Flow B4, business rules on provider status, REQ-003-020

When a provider became `Suspended` or `Deactivated`, an inquiry whose accepted treatment belonged to that provider (stage Accepted, Confirmed, In Progress, or Aftercare) moved to `Cancelled` with cause `ProviderSuspended` or `ProviderDeactivated` and `supportRequired = true`.

## Approved State

- The inquiry is not cancelled. It keeps its current stage and is flagged `supportRequired = true`.
- FR-006 Alternative Flow B4 closes the affected booking with cause `ProviderSuspended` or `ProviderDeactivated`.
- An admin rehomes the patient to a replacement provider in the same inquiry through FR-006 Alternative Flow B5, recorded as a linked admin-authored acceptance record.
- Behaviour for inquiries still comparing providers (stage Inquiry or Quoted) is unchanged: only the affected provider's participation and quotes are cancelled.

## Requirement Delta

- Workflow 2 Alternative Flow B4: step 2 and Outcome rewritten.
- Business rule on provider status (accepted-treatment bullet) rewritten.
- REQ-003-020: first clause changed from "MUST cancel each inquiry" to "MUST NOT cancel"; keeps the inquiry open for the FR-006 transfer.

## Scope and Impact

### Affected Contracts

- **PRD owner**: `project-requirements/functional-requirements/fr003-inquiry-submission/prd.md`
- **Related FRs**: FR-006 (Alternative Flows B4 and B5, provider-fault transfer and payment placeholder), FR-015 (Alternative Flow A5 and Screen 4, cascade owner), FR-004 (`cancelled_provider_status` for unaccepted quotes), FR-020 and FR-030 (`booking.provider_fault_replacement` for accepted cases; `provider.status_cancellation_patient` before acceptance only)
- **System documents**: `system-prd.md` and `system-data-schema.md` (inquiry stays open with `supportRequired`; the booking carries the provider-caused cause)

### Out of Scope

Refund, credit transfer and fund-release mechanics (payment pass); the FR-006 placeholder applies.

## Acceptance and Validation

- No FR-003 text cancels an inquiry because the provider of its accepted booking was suspended or deactivated.
- FR-003, FR-006 and FR-015 describe the same post-acceptance route.

## Approval and Traceability

- **Requested by**: Product Owner (MTG-002 quote model audit)
- **Approved by**: Product Owner, 2026-10-16, via `reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md` (documentation only)
- **Decision evidence**: SRC-MTG-002; decision log 2026-10-16 (M18, D6, D6-M)
- **Implementation reconciliation**: Required, not assessed
- **PRD change log**: v2.9 (2026-10-16)
- **Update log**: Combined 2026-10-16 MTG-002 log
- **Supersedes**: CR-FR003-20261014-01 in part
- **Superseded by**: None
