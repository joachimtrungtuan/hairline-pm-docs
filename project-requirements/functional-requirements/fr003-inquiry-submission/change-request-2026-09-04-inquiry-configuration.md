# Change Request: Configurable Inquiry Areas and Lead Time

**Change Request ID**: CR-FR003-20260904-01
**Primary FR**: FR-003
**Triggering FR / Event**: Approved client requirement for configurable inquiry creation
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-09-04
**Decision Date**: 2026-09-04
**PRD Version Change**: v2.1 to v2.2; amended to v2.3
**Related Commit(s)**: Pending

---

## Decision Summary

Inquiry creation must no longer depend on a fixed Hair/Beard/Both enum or a fixed 30-day earliest-date rule. Admin owns an active treatment-area catalog with display assets and an integer blocked window in days. The approved default lead time is 3 days until an Admin changes it.

## Baseline State

**Source version**: FR-003 v2.1, Screen 1 and Screen 5

Treatment areas were fixed to Hair, Beard, and Both. Preferred date ranges had a fixed minimum of 30 days from inquiry creation. Neither value had an Admin configuration contract or a required patient-facing configuration payload.

## Approved State

**Target version**: FR-003 v2.3, Screen 1, Screen 5, Inquiry Configuration Rules, REQ-003-017/018, and Key Entities

FR-003 consumes the active FR-026 treatment-area catalog and minimum inquiry lead time. Each inquiry retains a treatment-area snapshot so future catalog changes do not change historical records. The patient calendar and submission validation use the same current lead-time setting.

## Requirement Delta

| Contract Area | Before | After | Reason |
| --- | --- | --- | --- |
| Treatment-area choices | Fixed Hair/Beard/Both labels | Admin-managed ordered catalog with ID, label, and image/icon URL | Support client-specific future choices without hard-coded options |
| Date eligibility | Fixed 30-day minimum | Admin-configured blocked window, default 3 days | Allow client-controlled lead time |
| Historical display | Config lookup only | Inquiry stores selected-option snapshot | Preserve the meaning of already submitted inquiries |
| Patient integration | No dynamic contract required | Patient retrieves active catalog and lead time from backend | Keep the source of truth in Admin configuration |

## Scope and Impact

### In Scope

- FR-003 patient inquiry selection and date eligibility contracts.
- FR-026 Admin configuration ownership, audit, versioning, and API propagation.

### Out of Scope

- Location pricing and destination pricing APIs.
- Any assertion that the existing mobile client already supports arbitrary dynamic options.
- Changes to the two-year date horizon, non-overlap rule, or provider-availability validation.

### Affected Contracts

- **PRD owner**: [`prd.md`](./prd.md) — Screen 1, Screen 5, Inquiry Configuration Rules, REQ-003-017/018
- **Related FRs**: FR-026 owns configuration; FR-002/S-05 supplies managed image/icon assets
- **System documents**: `system-prd.md` FR-003 and FR-026 summaries

### Implementation Reconciliation

- **Existing implementation evidence**: Backend scout found fixed configuration and a fixed 30-day validator; no implementation change is claimed by this document update.
- **Required assessment**: Admin CRUD and audit storage; settings/configuration read API; date-picker consumption; backend validator; dynamic option rendering; image/icon delivery; cache invalidation; historical snapshot persistence; authorization and tests.
- **Compatibility / rollout risk**: A client that renders only the current three static options cannot satisfy the release-free expectation. Confirm response compatibility before relying on configuration-only changes.
- **Data migration**: Required for catalog/policy storage and existing inquiry snapshot treatment; exact migration design to be assessed.

## Acceptance and Validation

- Admin can manage active treatment-area options and their display assets with audit/version history.
- New inquiry sessions receive active options and the configured lead time; inactive options cannot be submitted.
- A lead time of 3 on 2026-09-04 makes 2026-09-07 the earliest eligible start date in both calendar and submission validation.
- Existing inquiries retain their originally selected treatment-area label and asset reference.
- Dynamic-client compatibility is evidenced before declaring that no app release is required.

## Approval and Traceability

- **Requested by**: Product Owner
- **Approved by**: Product Owner, 2026-09-04
- **Decision evidence**: Client-requirement clarification in this task; Product Owner correction on 2026-09-04 set the default lead time to 3 days.
- **PRD change log**: FR-003 v2.2 and v2.3
- **Update log**: [`INQUIRY_CONFIGURATION_CHANGE_REQUEST_2026-09-04.md`](../../update-logs/2026-09-04/INQUIRY_CONFIGURATION_CHANGE_REQUEST_2026-09-04.md)
- **Supersedes**: None
- **Superseded by**: None
