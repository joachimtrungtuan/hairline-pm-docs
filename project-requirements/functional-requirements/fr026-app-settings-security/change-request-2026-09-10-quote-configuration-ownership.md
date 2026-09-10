# Change Request: Quote Configuration Ownership

**Change Request ID**: CR-FR026-20260910-01
**Primary FR**: FR-026
**Triggering FR / Event**: Approved FR-004 parent-quote/Quote Option restructure
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-09-10
**Decision Date**: 2026-09-10
**PRD Version Change**: v1.7 to v1.8
**Related Commit(s)**: Pending

---

## Decision Summary

FR-026/A-09 owns one versioned Quote Configuration containing the active ISO 4217 currency and default quote-expiry hours. FR-004 consumes one configuration version when creating a parent Quote, snapshots the currency, and computes expiry without retroactively changing existing quotes.

## Baseline State

**Source version**: FR-026 v1.7, App Data screens, Dependencies, requirements, and Key Entities

FR-004 named FR-026/A-09 as the configuration owner, but FR-026 exposed neither quote currency nor quote expiry.

## Approved State

**Target version**: FR-026 v1.8, Workflow A7, Screen 5d, Dependencies, User Story 8, requirements, and Entity 11

The updated [FR-026 PRD](./prd.md) defines the versioned source and authenticated Settings API contract consumed by FR-004.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Quote currency | No FR-026 owner | Enabled ISO 4217 configuration, snapshotted on creation | Prevent provider-entered currency drift |
| Quote expiry | No FR-026 owner | Positive whole hours, default 48 | Give FR-004 one policy source |
| Change effect | Undefined | New quotes only | Preserve historical prices and deadlines |

## Scope and Impact

### In Scope

- FR-026 quote-configuration UI, versioning, API, dependency, and entity contracts.

### Out of Scope

- Currency conversion and exchange rates (FR-029), quote creation UI (FR-004), and implementation changes.

### Affected Contracts

- **PRD owner**: [`prd.md`](./prd.md) — Workflow A7, Screen 5d, Dependencies, User Story 8, requirements, Entity 11
- **Related FRs**: FR-004 consumes configuration; FR-029 owns conversion and exchange-rate locking
- **System documents**: FR-004/system schema quote currency and expiry fields

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed.
- **Required assessment**: Settings UI/API/storage, cache invalidation, quote-creation read consistency, permissions, and regression tests.
- **Compatibility / rollout risk**: Quote creation must fail safely or use the last valid cached configuration if the Settings API is unavailable.
- **Data migration**: Seed one active configuration version; existing quotes remain unchanged.

## Acceptance and Validation

- Admin can version and audit both values with a reason.
- FR-004 receives both values from one configuration version and snapshots/derives them once.
- Existing Quote currency and expiry values never change after a configuration update.

## Approval and Traceability

- **Requested by**: Product Owner
- **Approved by**: Product Owner, 2026-09-10
- **Decision evidence**: FR-004 v2.6 verification resolution
- **PRD change log**: FR-026 v1.8
- **Update log**: [`FR004_DEPENDENCY_AND_VERIFICATION_FIXES_2026-09-10.md`](../../update-logs/2026-09-10/FR004_DEPENDENCY_AND_VERIFICATION_FIXES_2026-09-10.md)
- **Supersedes**: None
- **Superseded by**: None
