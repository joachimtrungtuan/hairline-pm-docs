# Change Request: Accepted Quote Option Consumer Alignment

**Change Request ID**: CR-FR010-20260910-01
**Primary FR**: FR-010
**Triggering FR / Event**: CR-FR004-20260909-01 downstream consumer reconciliation
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-09-10
**Decision Date**: 2026-09-10
**PRD Version Change**: v1.9 to v2.0
**Related Commit(s)**: Pending

---

## Decision Summary

FR-010 consumes the exact Quote Option selected under FR-005 rather than a singular quote-level package or plan. The stable accepted Quote Option relationship supplies its package snapshot and relative plan days; the parent Quote continues to supply the Treatment relationship, graft estimate, and clinicians.

## Baseline State

**Source version**: FR-010 v1.9, Dependencies, Integration Points, Functional Requirements Summary, and Key Entities

FR-010 still referenced `quote.packageId` and a quote-level `plan`, which predated FR-004's approved parent-and-options aggregate.

## Approved State

**Target version**: FR-010 v2.0, Dependencies, Integration Points, REQ-010-007A, and Key Entities

The updated [FR-010 PRD](./prd.md) uses the accepted Quote Option ID and its `QuoteOptionPlanDay` records for package and treatment-plan data. It does not infer the patient's choice from the parent Quote.

## Requirement Delta

| Contract Area | Before | After | Reason |
| --- | --- | --- | --- |
| Package consumer | Singular `quote.packageId` | Accepted Quote Option package snapshot | Preserve the exact selected alternative |
| Plan consumer | Quote-level `plan` | Accepted option's relative `QuoteOptionPlanDay` records | Match FR-004 option ownership |
| Treatment record relationship | Quote-level plan reference | Stable accepted Quote Option reference | Prevent ambiguous downstream selection |

## Scope and Impact

### In Scope

- FR-010 display, sync payload, dependency, requirement, and entity references to accepted-option data.

### Out of Scope

- FR-005, FR-006, FR-008, FR-014, or FR-015 reconciliation.
- Product-code, API, database, or UI implementation changes.

### Affected Contracts

- **PRD owner**: [`prd.md`](./prd.md) — tenant scope, screens, Dependencies, Integration Points, REQ-010-007A, and Key Entities
- **Related FRs**: FR-004 supplies the parent Quote, accepted Quote Option, and relative option plan; FR-005 must record the stable accepted identifiers
- **System documents**: No additional system-document change required for this consumer correction

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed in this documentation update
- **Required assessment**: Booking-to-treatment payloads, treatment record relationships, provider/patient/admin screens, progress-sync events, compatibility handling, and regression tests
- **Compatibility / rollout risk**: Consumers that still read singular `packageId` or quote-level `plan` will select incomplete or ambiguous data
- **Data migration**: To be assessed with FR-004's additive quote-option migration

## Acceptance and Validation

- FR-010 contains no current dependency on singular `quote.packageId` or quote-level `plan`.
- Every treatment record can identify the exact accepted Quote Option.
- Day descriptions resolve only from that option's relative `QuoteOptionPlanDay` records.
- Implementation reconciliation remains `Required` until payload, persistence, UI, and regression evidence confirm the handoff.

## Approval and Traceability

- **Requested by**: Product Owner
- **Approved by**: Product Owner, 2026-09-10
- **Decision evidence**: Approved resolution of the FR-004 verification findings in the 2026-09-10 project task
- **PRD change log**: FR-010 v2.0
- **Update log**: [`FR004_FR010_VERIFICATION_RESOLUTION_2026-09-10.md`](../../update-logs/2026-09-10/FR004_FR010_VERIFICATION_RESOLUTION_2026-09-10.md)
- **Supersedes**: None
- **Superseded by**: None
