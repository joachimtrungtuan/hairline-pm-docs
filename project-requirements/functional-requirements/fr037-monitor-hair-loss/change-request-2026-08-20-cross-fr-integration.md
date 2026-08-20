# Change Request: FR-037 Cross-FR Integration

**Change Request ID**: CR-FR037-20260820-01
**Primary FR**: FR-037
**Triggering FR / Event**: FR-037 verification findings and provider-decline clarification
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-08-20
**Decision Date**: 2026-08-20
**PRD Version Change**: v1.7 to v1.8 to v1.9
**Related Commits**: `7317cc4`, `935283e`

---

## Decision Summary

FR-037's cross-FR contracts are formalized as a major change event because they modify previously verified inquiry, quote, questionnaire, and notification requirements. The v1.8 alignment establishes those handoffs; v1.9 clarifies that an explicit exclusive-provider decline automatically returns the converted inquiry to normal FR-003 distribution.

## Baseline State

**Source version**: FR-037 v1.7 and the pre-alignment dependent FR versions

FR-037 described conversion routing, questionnaire reuse, and notification candidates locally, but the owning dependent FRs did not all contain matching contracts. The decline path required a patient release and combined explicit decline with expiry behavior.

## Approved State

**Target version**: FR-037 v1.9, Dependencies, Screen 7 handoff, Business Rule 7, User Story 3, and REQ-037-029

FR-003 owns exclusive conversion routing and explicit-decline fallback; FR-004 owns initial quote authorization; FR-025 owns questionnaire delivery; FR-030 and FR-020 own notification event configuration and delivery. FR-038 is recorded as the sibling monitoring type. Expiry remains separate from explicit decline.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Inquiry conversion | FR-037-only routing statement | FR-003 owns exclusive initial routing | Make both sides of the handoff explicit |
| Quote creation | No dependent restriction | FR-004 restricts initial quote to the assigned provider | Enforce routing at quote authorization |
| Questionnaire | Local requirement only | FR-025 reuses the active Inquiry-context set | Avoid duplicate questionnaire contexts |
| Notifications | Candidate events | FR-030 source catalog and FR-020 mirror | Establish deliverable event contracts |
| Provider decline | Patient release and mixed expiry rule | Explicit decline automatically invokes normal FR-003 distribution once | Prevent stranded inquiries and remove unnecessary patient action |
| Expiry | Coupled with decline | Existing FR-003/FR-004 expiry remains unchanged | Keep fallback scope precise |

## Scope and Impact

### In Scope

- Cross-FR ownership for conversion, quote authorization, questionnaire gating, monitoring notifications, sibling dependency, and explicit-provider-decline fallback.

### Out of Scope

- Automatic redistribution on expiry.
- Patient logging reminders or aftercare mechanics.
- A new questionnaire context or FR-037 chat surface.

### Affected Contracts

- **PRD owner**: [`prd.md`](./prd.md) — Dependencies, Screen 7, Business Rule 7, User Story 3, REQ-037-029
- **Related FRs**: FR-003, FR-004, FR-020, FR-025, FR-030, and FR-038
- **System document**: [`../../system-prd.md`](../../system-prd.md) — FR-037 requirements

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed by this documentation change.
- **Required assessment**: All affected FR implementation surfaces listed in their companion Change Requests, plus end-to-end conversion provenance and tenant handoffs.
- **Compatibility / rollout risk**: Deploying only one side of a cross-FR contract can strand inquiries, allow unauthorized quotes, omit medical gating, or silently lose notifications.
- **Data migration**: Cross-FR assessment required before implementation planning.

## Acceptance and Validation

- Every FR-037 handoff has a matching owner contract in the affected FR.
- A converted inquiry is exclusive initially and redistributes exactly once on explicit pre-quote decline.
- Questionnaire and notification contracts reuse their existing central owners.
- Documentation approval does not mark implementation reconciliation as complete.

## Approval and Traceability

- **Requested by**: Product Owner
- **Approved by**: Product Owner, 2026-08-20
- **Decision evidence**: FR-037 verification resolutions and provider-decline clarification
- **PRD change log**: FR-037 v1.8 and v1.9
- **Update logs**: [`FR037_CROSS_FR_VERIFICATION_SYNC_2026-08-20.md`](../../update-logs/2026-08-20/FR037_CROSS_FR_VERIFICATION_SYNC_2026-08-20.md), [`FR037_PROVIDER_DECLINE_FALLBACK_2026-08-20.md`](../../update-logs/2026-08-20/FR037_PROVIDER_DECLINE_FALLBACK_2026-08-20.md)
- **Supersedes**: None
- **Superseded by**: None
