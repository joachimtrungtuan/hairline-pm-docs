# Change Request: Quote Option Package Provenance Alignment

**Change Request ID**: CR-FR024-20260910-01
**Primary FR**: FR-024
**Triggering FR / Event**: Approved FR-004 parent-quote/Quote Option restructure
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-09-10
**Decision Date**: 2026-09-10
**PRD Version Change**: v1.1 to v1.2
**Related Commit(s)**: Pending

---

## Decision Summary

FR-024 remains the reusable provider package-library owner. FR-004 records a selected Package ID/version as provenance on a quote-owned Quote Option snapshot; new quotes do not use a direct reusable-package relationship on the parent Quote.

## Baseline State

**Source version**: FR-024 v1.1, FR-004 integration, requirements, and Key Entities

Package versions were described as directly referenced by Quotes through `QuotePackage`.

## Approved State

**Target version**: FR-024 v1.2, FR-004 integration, requirements, and Key Entities

The updated [FR-024 PRD](./prd.md) points to FR-004 Quote Option provenance and marks `QuotePackage` as a legacy compatibility link.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Package relationship | Package version to parent Quote | Package version to Quote Option provenance | Support one to five independent option snapshots |
| QuotePackage | Current linking entity | Deprecated compatibility link | Prevent competing aggregate models |
| Customization | Implicit quote link | FR-004-owned option snapshot | Keep patient-specific edits out of the library |

## Scope and Impact

### In Scope

- FR-024 package-version provenance and FR-004 integration wording.

### Out of Scope

- Package-library CRUD, pricing rules, quote UI, and implementation changes.

### Affected Contracts

- **PRD owner**: [`prd.md`](./prd.md) — Dependencies, requirements, Key Entities
- **Related FRs**: FR-004 owns Quote Option snapshots and inline customization
- **System documents**: Existing FR-004 quote-option schema remains authoritative

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed.
- **Required assessment**: Package APIs, quote-option snapshot persistence, legacy `QuotePackage` consumers, and historical reads.
- **Compatibility / rollout risk**: Removing the legacy link before consumer migration would break older quote reads.
- **Data migration**: Required for legacy single-package quotes under the FR-004 migration.

## Acceptance and Validation

- New Quote Options retain immutable Package ID/version provenance and quote-owned item snapshots.
- Inline option changes never alter reusable Package records.
- Legacy quotes remain readable during migration.

## Approval and Traceability

- **Requested by**: Product Owner
- **Approved by**: Product Owner, 2026-09-10
- **Decision evidence**: FR-004 v2.6 verification resolution
- **PRD change log**: FR-024 v1.2
- **Update log**: [`FR004_DEPENDENCY_AND_VERIFICATION_FIXES_2026-09-10.md`](../../update-logs/2026-09-10/FR004_DEPENDENCY_AND_VERIFICATION_FIXES_2026-09-10.md)
- **Supersedes**: None
- **Superseded by**: None
