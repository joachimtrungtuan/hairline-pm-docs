# Change Request: FR-037 Monitoring Event Configuration

**Change Request ID**: CR-FR030-20260820-01
**Primary FR**: FR-030
**Triggering FR / Event**: FR-037 monitoring lifecycle integration
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-08-20
**Decision Date**: 2026-08-20
**PRD Version Change**: v1.4 to v1.5
**Related Commit**: `7317cc4`

---

## Decision Summary

FR-030's source-of-truth notification catalog now includes the monitoring events required by FR-037 and FR-038. FR-020 mirrors these contracts for delivery behavior.

## Baseline State

**Source version**: FR-030 v1.4, Event Catalog

Admin notification rules had no monitoring event category, so monitoring lifecycle events could not be configured through the established catalog.

## Approved State

**Target version**: FR-030 v1.5, Monitoring event catalog and dependency

The source catalog defines assignment pending, provider assigned, provider withdrawn, provider reassigned, advice posted, case completed, export ready, and converted-to-inquiry events.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Source catalog | No monitoring events | Eight monitoring event contracts | Make monitoring notifications configurable |
| FR-020 mirror | No matching rows | Identical event identifiers and meanings | Prevent configuration and delivery drift |
| Dependency | No monitoring publisher | FR-037 and FR-038 publish through P-05 and S-03 | Establish integration ownership |

## Scope and Impact

### In Scope

- Monitoring event registration in the notification-rules source catalog.

### Out of Scope

- Monitoring workflow state transitions and logging reminders.
- Final notification copy and channel-specific design.

### Affected Contracts

- **PRD owner**: [`prd.md`](./prd.md) — Event Catalog and FR-037/FR-038 integration
- **Related FRs**: FR-020 delivery mirror; FR-037 and FR-038 event publishers

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed by this documentation change.
- **Required assessment**: Event registry, Admin rule configuration, template availability, channel eligibility, FR-020 mirror integrity, and deployment order.
- **Compatibility / rollout risk**: Configuration must not reference events before publishers and delivery consumers are ready; catalog identifiers must remain stable.
- **Data migration**: Seed or configuration migration may be required for new event types.

## Acceptance and Validation

- FR-030 and FR-020 expose identical monitoring event identifiers and meanings.
- Admin configuration can resolve each event without inventing an unsupported context.
- Existing notification categories remain unchanged.

## Approval and Traceability

- **Requested by**: Product Owner
- **Approved by**: Product Owner, 2026-08-20
- **Decision evidence**: FR-037 verification resolution
- **PRD change log**: FR-030 v1.5
- **Update log**: [`FR037_CROSS_FR_VERIFICATION_SYNC_2026-08-20.md`](../../update-logs/2026-08-20/FR037_CROSS_FR_VERIFICATION_SYNC_2026-08-20.md)
- **Supersedes**: None
- **Superseded by**: None
