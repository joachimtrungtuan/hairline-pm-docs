# Change Request: Multiple Assigned Clinicians from the Quote

**Change Request ID**: CR-FR010-20260909-01
**Primary FR**: FR-010
**Triggering FR / Event**: FR-004 v2.2 quote-option restructure (CR-FR004-20260909-01) and 2026-09-09 FR-004 verification
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-09-09
**Decision Date**: 2026-09-09
**PRD Version Change**: v1.8 to v1.9
**Related Commit(s)**: Pending

---

## Decision Summary

FR-010 adopts the multi-clinician assignment model introduced by FR-004 v2.2. A treatment record now inherits one or more clinicians from the accepted quote's `clinicianIds[]` instead of a single `clinicianId`. Provider locking at Check In and admin override with reason remain unchanged; the only new constraint is that at least one clinician must remain assigned after any admin edit.

## Baseline State

**Source version**: FR-010 v1.8, Patient Screen 3, Provider Screens 1 and 3, Admin Screen 2, Business Rule 8, Dependencies, and Entity 1

FR-010 v1.4 explicitly adopted a singular clinician model on the stated grounds that it was "aligned to FR-004 (singular clinicianId)". Entity 1 recorded "assigned clinician ID (singular, from quote)", the Check In lock rule referenced "assigned clinician (singular, from quote)", and the admin edit field was a single-value text input.

## Approved State

**Target version**: FR-010 v1.9, same headings

The quote supplies `clinicianIds[]` — one or more eligible clinicians shared by every Quote Option (FR-004 REQ-004-027). FR-010 displays the assigned clinician set read-only on patient and provider surfaces, filters by any assigned clinician, and lets admin add or remove clinicians after Check In with a mandatory reason and audit history, provided at least one remains.

## Requirement Delta

| Contract Area | Before | After | Reason |
| --- | --- | --- | --- |
| Clinician cardinality | One `clinicianId` inherited from the quote | One or more `clinicianIds[]` inherited from the accepted quote | FR-004 v2.2 made clinicians a plural shared parent-quote field |
| Patient and provider display | Single-value text field | Read-only list of assigned clinicians | Reflect the real assignment without exposing clinical detail |
| Admin edit surface | Single-value editable text | Multiselect add/remove | Support operational reassignment across a team |
| Admin edit constraint | Replace the single clinician | At least one clinician must remain | Prevent a treatment record with no responsible clinician |
| Check In lock | Locks the singular clinician | Locks the whole clinician set | Preserve the existing provider-lock intent under plural data |
| Filtering | Filter by assigned clinician | Filter by any assigned clinician | Keep list filters correct for set-valued data |

## Scope and Impact

### In Scope

- FR-010 display, filtering, locking, admin override, dependency notes, and Entity 1 attributes/relationships for clinician assignment.

### Out of Scope

- FR-004 changes; the plural model is already approved there.
- FR-005, FR-006, and FR-008 reconciliation of the quote-option acceptance contract, which remains open and separately owned.
- Clinician role differentiation (lead versus assisting); all assigned clinicians are peers in this change.
- Product-code, API, database, or UI implementation changes.

### Affected Contracts

- **PRD owner**: [`prd.md`](./prd.md) — Patient Screen 3, Provider Screens 1 and 3, Admin Screen 2, Business Rule 8, Dependencies, Entity 1
- **Related FRs**: FR-004 owns `clinicianIds[]`; FR-009 supplies eligible provider team members; FR-031 governs the roles permitted to edit
- **System documents**: system data schema requires a set-valued clinician association on the treatment record during the same reconciliation pass as the FR-004 quote-option tables

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed in this change. The FR-004 reconciliation already requires a review of quote aggregate models; the treatment record's clinician association must be included in that pass.
- **Required assessment**: Treatment record schema and model association; provider and admin treatment screens; clinician filters; Check In lock enforcement; admin override validation preserving at least one clinician; audit before/after values for set changes.
- **Compatibility / rollout risk**: Low relative to FR-004. A single-clinician record migrates to a one-element set without semantic loss.
- **Data migration**: Required but mechanical. Convert each existing singular clinician reference into a one-element assignment set and preserve audit history.

## Acceptance and Validation

- A treatment record created from an accepted quote carries every clinician on that quote.
- Patient and provider surfaces show all assigned clinicians and remain read-only.
- The clinician filter matches a treatment record when any assigned clinician matches.
- Providers cannot change the clinician set after Check In.
- Admin can add or remove clinicians after Check In with a mandatory reason; an attempt to remove the last clinician is rejected.
- Audit history records the before and after clinician sets for every admin change.
- No FR-010 surface or entity description continues to assert a singular clinician model.

## Approval and Traceability

- **Requested by**: 2026-09-09 FR-004 verification (dependency data-field conflict, Critical #3)
- **Approved by**: Product Owner, 2026-09-09
- **Decision evidence**: FR-004 REQ-004-027 and the Quote Data Ownership Matrix; [CR-FR004-20260909-01](../fr004-quote-submission/change-request-2026-09-09-quote-options-model.md); Product Owner selection of the "make FR-010 plural" option during the 2026-09-09 verification review
- **PRD change log**: FR-010 v1.9
- **Update log**: [`FR004_VERIFICATION_FIXES_2026-09-09.md`](../../update-logs/2026-09-09/FR004_VERIFICATION_FIXES_2026-09-09.md)
- **Supersedes**: FR-010 v1.4 item (7), "Singular clinician model"
- **Superseded by**: None
