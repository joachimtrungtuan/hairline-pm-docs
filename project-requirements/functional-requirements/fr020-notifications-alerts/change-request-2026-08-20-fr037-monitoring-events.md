# Change Request: FR-037 Monitoring Notification Events

**Change Request ID**: CR-FR020-20260820-01
**Primary FR**: FR-020
**Triggering FR / Event**: FR-037 monitoring lifecycle integration
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-08-20
**Decision Date**: 2026-08-20
**PRD Version Change**: v1.9 to v2.0
**Related Commit**: `7317cc4`

---

## Decision Summary

FR-020 now exposes the approved monitoring lifecycle notifications required by FR-037 and FR-038, mirroring FR-030's source-of-truth event catalog.

## Baseline State

**Source version**: FR-020 v1.9, Notification Event Catalog

The notification catalog contained no monitoring category or event contracts for assignment, advice, completion, export, or conversion.

## Approved State

**Target version**: FR-020 v2.0, Monitoring event catalog rows and FR-037/FR-038 dependency

The catalog includes assignment pending, provider assigned, provider withdrawn, provider reassigned, advice posted, case completed, export ready, and converted-to-inquiry events with defined recipient roles.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Event category | No Monitoring category | Monitoring category mirrors FR-030 | Make FR-037 lifecycle events deliverable |
| Recipients | Undefined | Patient, Provider, and Admin recipients vary by event | Preserve tenant-specific communication |
| Dependency | No FR-037 or FR-038 link | Both monitoring FRs are explicit dependencies | Establish event ownership traceability |

## Scope and Impact

### In Scope

- Notification-facing monitoring event names, meanings, and recipient roles.

### Out of Scope

- Monitoring workflow logic and notification copy.
- Patient logging reminders, which FR-037 excludes.

### Affected Contracts

- **PRD owner**: [`prd.md`](./prd.md) — Notification Event Catalog
- **Related FRs**: FR-030 source catalog; FR-037 and FR-038 publishers

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed by this documentation change.
- **Required assessment**: Event publishers, S-03 consumers, templates, recipient resolution, preferences, delivery audit, retries, and deep links.
- **Compatibility / rollout risk**: FR-020 and FR-030 catalogs must remain identical for monitoring events; missing consumers must fail visibly rather than discard events.
- **Data migration**: None expected.

## Acceptance and Validation

- Every documented monitoring event is present with the same identifier and meaning in FR-020 and FR-030.
- Each event resolves only its documented recipient roles.
- Delivery attempts and failures follow existing notification audit and retry rules.

## Approval and Traceability

- **Requested by**: Product Owner
- **Approved by**: Product Owner, 2026-08-20
- **Decision evidence**: FR-037 verification resolution
- **PRD change log**: FR-020 v2.0
- **Update log**: [`FR037_CROSS_FR_VERIFICATION_SYNC_2026-08-20.md`](../../update-logs/2026-08-20/FR037_CROSS_FR_VERIFICATION_SYNC_2026-08-20.md)
- **Supersedes**: None
- **Superseded by**: None
