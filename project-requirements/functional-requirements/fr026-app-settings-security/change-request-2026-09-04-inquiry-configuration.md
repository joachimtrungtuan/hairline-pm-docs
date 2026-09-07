# Change Request: Inquiry Configuration Ownership

**Change Request ID**: CR-FR026-20260904-01
**Primary FR**: FR-026
**Triggering FR / Event**: Approved client requirement for configurable inquiry creation
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-09-04
**Decision Date**: 2026-09-04
**PRD Version Change**: v1.4 to v1.5; amended to v1.6
**Related Commit(s)**: Pending

---

## Decision Summary

FR-026 becomes the configuration owner for the treatment-area catalog and the minimum inquiry lead-time policy consumed by FR-003. The settings follow the existing change-reason, versioning, auditing, propagation, and cache-invalidation rules.

## Baseline State

**Source version**: FR-026 v1.4, App Data setting groups

FR-026 centrally managed countries, discovery questions, cancellation reasons, and deletion reasons, but not inquiry treatment-area choices or the inquiry date blocked window.

## Approved State

**Target version**: FR-026 v1.6, App Data, Workflow A6, Screen 5c, Admin Editability Rules, Integration Requirements, and Key Entities

Admin can manage treatment-area options with display assets and set a whole-day minimum inquiry lead time. The active response includes the catalog and `minimum_inquiry_lead_days`; all changes are versioned and audited. The approved default is 3 days.

## Requirement Delta

| Contract Area | Before | After | Reason |
| --- | --- | --- | --- |
| App Data ownership | No owner for inquiry choices or lead time | FR-026 Inquiry Configuration Manager | Centralize client-controlled inquiry settings |
| Treatment-area data | Fixed backend config with labels only | Managed option records with image/icon URL, order, and active state | Support future choices and display assets |
| Lead time | Fixed application rule | Versioned whole-day setting, default 3 | Make blocked window configurable |
| Patient propagation | No required payload | Active catalog and lead time exposed through settings/configuration API | Keep inquiry UI and server validation aligned |

## Scope and Impact

### In Scope

- Admin setting screen, audit/version behavior, active filtering, and patient configuration response.
- FR-003 integration for treatment-area selection and date validation.

### Out of Scope

- Regional/location pricing configuration.
- Automatic mobile client updates beyond its verified API compatibility.
- Retrospective changes to submitted inquiries.

### Affected Contracts

- **PRD owner**: [`prd.md`](./prd.md) — App Data, Workflow A6, Screen 5c, requirements, and entities
- **Related FRs**: FR-003 consumes the configuration; FR-002/S-05 owns media-storage behavior
- **System documents**: `system-prd.md` FR-003 and FR-026 summaries

### Implementation Reconciliation

- **Existing implementation evidence**: Backend scout found the current treatment areas in static configuration and a fixed 30-day validator; no Admin configuration surface was identified.
- **Required assessment**: Data model and migrations; Admin authorization; CRUD, activation, ordering, asset upload/reference, audit/version records, client read contract, cache invalidation, and settings propagation.
- **Compatibility / rollout risk**: Do not deactivate the final available option. Preserve snapshots for historical inquiry readability. Confirm that current mobile UI can render dynamic labels/assets before calling a configuration change release-free.
- **Data migration**: Required; exact persistence and backfill plan to be assessed.

## Acceptance and Validation

- Admin can create, edit, reorder, activate, and deactivate options; referenced options cannot be deleted.
- Saving records a reason and version/audit history and invalidates the configuration cache.
- The active client response contains ordered option IDs, labels, image/icon URLs, and the configured lead time.
- FR-003 rejects a submitted inactive option or a date before the configured threshold.

## Approval and Traceability

- **Requested by**: Product Owner
- **Approved by**: Product Owner, 2026-09-04
- **Decision evidence**: Client-requirement clarification in this task; Product Owner correction on 2026-09-04 set the default lead time to 3 days.
- **PRD change log**: FR-026 v1.5 and v1.6
- **Update log**: [`INQUIRY_CONFIGURATION_CHANGE_REQUEST_2026-09-04.md`](../../update-logs/2026-09-04/INQUIRY_CONFIGURATION_CHANGE_REQUEST_2026-09-04.md)
- **Supersedes**: None
- **Superseded by**: None
