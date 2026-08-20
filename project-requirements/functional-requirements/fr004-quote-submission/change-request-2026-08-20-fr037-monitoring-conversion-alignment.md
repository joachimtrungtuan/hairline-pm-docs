# Change Request: FR-037 Restricted Initial Quote Recipient

**Change Request ID**: CR-FR004-20260820-01
**Primary FR**: FR-004
**Triggering FR / Event**: FR-037 monitoring-conversion integration
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-08-20
**Decision Date**: 2026-08-20
**PRD Version Change**: v1.8 to v1.9
**Related Commit**: `7317cc4`

---

## Decision Summary

FR-004 must honor the exclusive provider carried by an FR-037 or FR-038 monitoring conversion. Only that provider may create the initial quote while the restriction exists.

## Baseline State

**Source version**: FR-004 v1.8, Workflow 1 and Business Rules

Any provider receiving a distributed inquiry could open it and create the initial quote. FR-004 did not recognize monitoring-conversion routing provenance.

## Approved State

**Target version**: FR-004 v1.9, Workflow 1 Restricted Recipient Check and Restricted Recipient Mode

FR-004 verifies the inquiry's exclusive provider before initial quote creation and blocks every other provider. The later FR-037 v1.9 decline fallback is owned by FR-003; it does not change FR-004's existing quote-expiry contract.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Initial quote authorization | Based on ordinary inquiry distribution | Restricted to the monitoring-assigned provider when exclusive provenance exists | Keep FR-004 consistent with FR-003 routing |
| Unauthorized provider | No monitoring-specific block | Opening provider is rejected with a restricted-inquiry error | Prevent cross-provider quote creation |
| Quote expiry | Existing FR-004 rules | Unchanged | Decline fallback belongs to FR-003 before quote creation |

## Scope and Impact

### In Scope

- Authorization for opening and creating the first quote on an exclusive monitoring-conversion inquiry.

### Out of Scope

- Provider decline processing and redistribution, which FR-003 owns.
- Quote editing, withdrawal, expiry, and Admin oversight after quote creation.

### Affected Contracts

- **PRD owner**: [`prd.md`](./prd.md) — Workflow 1 and Restricted Recipient Mode
- **Related FRs**: FR-003 distribution and decline fallback; FR-037 conversion routing

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed by this documentation change.
- **Required assessment**: Inquiry authorization guard, provider-specific views, quote-create API, error response, and concurrent decline versus quote creation.
- **Compatibility / rollout risk**: The restriction must apply only when explicit monitoring-conversion provenance and an active exclusive provider are present.
- **Data migration**: None expected; confirm provenance availability.

## Acceptance and Validation

- The exclusive provider can create the initial quote.
- Any other provider is blocked before quote drafting or submission.
- Ordinary FR-003 inquiries retain existing quote behavior.
- Existing quote-expiry behavior remains unchanged.

## Approval and Traceability

- **Requested by**: Product Owner
- **Approved by**: Product Owner, 2026-08-20
- **Decision evidence**: FR-037 verification resolution
- **PRD change log**: FR-004 v1.9
- **Update log**: [`FR037_CROSS_FR_VERIFICATION_SYNC_2026-08-20.md`](../../update-logs/2026-08-20/FR037_CROSS_FR_VERIFICATION_SYNC_2026-08-20.md)
- **Supersedes**: None
- **Superseded by**: None
