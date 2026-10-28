# Change Request: Legacy Quote Status Value Migration

**Change Request ID**: CR-FR004-20261027-01
**Primary FR**: FR-004
**Triggering FR / Event**: FR-015 provider-status cascade release; backend follow-up questions F1 and F2 (`FR015-BA-FOLLOWUP-QUESTIONS-2026-10-26.md`); Product Owner decision 2026-10-27
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-26
**Decision Date**: 2026-10-27
**PRD Version Change**: None (records a value migration only; the PRD is current at v3.6)
**Related Commit(s)**: Pending

---

## Decision Summary

The quote status values in FR-004 and in the system data schema are unchanged. This Change Request formally records that the legacy implementation values on `quotes.status` are migrated in the release that ships the FR-015 provider-status cascade. Many of those legacy values are case stages, not quote statuses, so the migration also produces the booking status and the inquiry stage for the same case. It also records what legacy API routes return during the backward-compatibility window.

This is one of three linked Change Requests:

- [CR-FR003-20261027-01](../fr003-inquiry-submission/change-request-2026-10-27-legacy-status-value-migration.md): inquiry stages and `inquiry_providers` participation.
- CR-FR004-20261027-01 (this document): quote status, including the legacy stage values stored on `quotes.status`.
- [CR-FR006-20261027-01](../fr006-booking-scheduling/change-request-2026-10-27-legacy-status-value-migration.md): booking status.

## Baseline State

**Source version**: FR-004 v3.5, Workflow 3 (Quote Expiry & Status Transitions) and Key Entities; system data schema v1.12.0, §7 quote status and the ENUM Types list.

- The requirement quote statuses are `draft`, `sent` (exposed as `quote`), `expired`, `withdrawn`, `archived`, `accepted`, `cancelled_other_accepted`, `cancelled_inquiry_cancelled`, and `cancelled_provider_status`. There is no `confirmed` and no `rejected` quote status.
- The legacy implementation stores case stages on `quotes.status`: `scheduled`, `confirmed`, `inprogress`, `aftercare`, `completed`, `cancelled`, and `rejected`. A legacy `scheduled` quote may have no booking and no payment yet.
- No requirement document stated how these legacy values migrate.

## Approved State

**Target version**: FR-004 v3.6 (requirement values unchanged); system data schema v1.13.0, ENUM Types note.

### Old to new (data migration)

| Legacy `quotes.status` | New quote status | New booking status | New inquiry stage |
|---|---|---|---|
| `scheduled`, no paid deposit, payment-window hold still open | `accepted` | `accepted` | `accepted` |
| `scheduled`, no paid deposit, payment-window hold no longer open | `accepted` | `payment_window_expired` | `accepted` |
| `scheduled` with a paid deposit | `accepted` | `confirmed` | `confirmed` |
| `confirmed` | `accepted` | `confirmed` | `confirmed` |
| `inprogress` | `accepted` | `in_progress` | `in_progress` |
| `aftercare` | `accepted` | `aftercare` | `aftercare` |
| `completed` | `accepted` | `completed` | `completed` |
| `cancelled` on an accepted quote | `accepted` (kept for history) | `cancelled` | `cancelled` |
| `rejected` (patient declined), and the inquiry has another accepted quote | `cancelled_other_accepted` | None | Migrated by CR-FR003-20261027-01 |
| `rejected` (patient declined), and the inquiry has no other accepted quote | `expired` | None | Migrated by CR-FR003-20261027-01 |
| Any value not listed, including `cancelled` on a quote that was never accepted | The backend team lists it and the BA maps it before the migration runs | | |

Where a legacy `scheduled` quote has no booking row, the migration creates the booking with the status above. Booking-side rules are in CR-FR006-20261027-01.

### New to old (legacy `/api/v1` routes during the compatibility window)

- Quote values are returned in their legacy spelling. `sent` keeps the existing `quote` exposure.
- Where a legacy route returned the case stage on the quote, it derives that value from the booking with the booking mapping in CR-FR006-20261027-01.
- A quote value with no legacy spelling (for example `cancelled_provider_status`) is listed by the backend team and mapped by the BA before release.

### Compatibility window

- New values are returned only on new-version routes. Legacy routes keep returning legacy values for the backend deprecation window (backend ADR-003: 3 months).
- Before building, the backend team lists the endpoints whose returned values or structure change and need a new version, and confirms that list with the BA and the Product Owner.
- Internal tester builds count as consumers of legacy routes (Product Owner decision).

### Addendum 2026-10-28 (Product Owner)

This addendum extends the Approved State above; the 2026-10-27 tables are unchanged.

#### Legacy values not covered by the table

| Legacy `quotes.status` | New quote status | New booking status | New inquiry stage |
|---|---|---|---|
| `accepted` (treated like `scheduled` with no paid deposit), payment-window hold still open | `accepted` | `accepted` | `accepted` |
| `accepted` (treated like `scheduled` with no paid deposit), payment-window hold no longer open | `accepted` | `payment_window_expired` | `accepted` |
| `accepted` with a paid deposit (same as the legacy `confirmed` row; follow-up decision, 2026-10-28) | `accepted` | `confirmed` | `confirmed` |
| `cancelled` on a quote never accepted, and the inquiry was cancelled | `cancelled_inquiry_cancelled` | None | Migrated by CR-FR003-20261027-01 |
| `cancelled` on a quote never accepted, and another quote on the inquiry was accepted | `cancelled_other_accepted` | None | Migrated by CR-FR003-20261027-01 |
| `cancelled` on a quote never accepted, any other case | `withdrawn` | None | Migrated by CR-FR003-20261027-01 |

- A legacy quote with status `rejected`, or any other non-accepted value, that has an aftercare record is invalid data: aftercare can only be linked to an accepted quote whose booking reached Aftercare (system data schema v1.13.1 §13). The migration has no mapping logic for it. The dry-run report lists these rows, and they are cleaned up in the non-production cleanup.
- A legacy quote that migrates to `accepted` and has a treatment-linked aftercare record takes its booking and inquiry stage from the aftercare record's status (active or suspended aftercare gives `aftercare`, completed aftercare gives `completed`, cancelled aftercare goes to BA review). The rule and the dry-run listing are in the CR-FR006-20261027-01 Addendum 2026-10-28; they take precedence over the table rows above.

#### API versions

- Unversioned `/api/...` routes and `/api/v1/...` routes both serve legacy values. The new version is `v2`; the existing v2 accept-quote route joins it.
- New values are returned only by `v2` routes, and only once the endpoint list below is signed off.
- Webhook routes are excluded from the `v1` alias and keep their single registered URL.
- Endpoint list: the backend WS1 inventory §2 (38 methods across 20 controllers, from a controller-only scan) is accepted by the Product Owner as a first draft, not as final. To complete it:
  1. The backend team finishes the scan beyond controllers: API resources, services, models, transformers, data exports, and notification or push payloads that carry a status value.
  2. The list has one row per endpoint, giving the calling app (patient app, provider portal, or admin portal), the status field, the old value, the new value, and whether the request accepts a status value (for example a `?status=` filter).
  3. `v2` rules:
     - A read endpoint gets `v2` when its response returns a status value.
     - A write endpoint gets `v2` when its request accepts a status value or its response returns one. Otherwise it keeps its route, and only the stored values change internally.
     - An analytics or dashboard endpoint gets `v2` when any app shows, groups by, or filters by a status value. It does not get `v2` when the status is used only internally to compute a number.
  4. The BA reviews the completed list, and the BA and the Product Owner sign it off before any `v2` route or presentation layer is built.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Quote status values (FR-004 Workflow 3 and Key Entities; schema §7) | Requirement values defined; no migration rule for legacy stage values on `quotes.status` | Requirement values unchanged; each legacy value maps to a quote status, a booking status, and an inquiry stage | The legacy table mixes quote status and case stage; the schema keeps them separate |
| Legacy `rejected` quotes | Not defined | `cancelled_other_accepted` when another quote on the inquiry is accepted, otherwise `expired` | The requirement model has no `rejected` quote status |
| Legacy API responses | Not defined | Legacy routes return legacy values during the compatibility window; new values only on new-version routes | Already-built apps must not show wrong states or fail |

## Scope and Impact

### In Scope

- Data migration of legacy `quotes.status` values, including the booking and inquiry values they produce.
- What legacy routes return for quote values during the compatibility window.

### Out of Scope

- Any change to the FR-004 requirement values or lifecycle.
- The technical API versioning scheme, which the backend team owns.

### Affected Contracts

- **PRD owner**: `project-requirements/functional-requirements/fr004-quote-submission/prd.md`: Workflow 3 and Key Entities. No PRD text changes for this Change Request.
- **Related FRs**: FR-003 (CR-FR003-20261027-01), FR-006 (CR-FR006-20261027-01), FR-015 (the release that ships the provider-status cascade).
- **System documents**: `system-data-schema.md` v1.13.0, ENUM Types note and §5 Inquiry stages note.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed in source. The backend team reports the legacy `quotes.status` values listed in Baseline State.
- **Required assessment**: Migration script, booking creation for `scheduled` quotes without a booking, payment and hold checks used by the migration, legacy-route value translation, the endpoint list that needs a new version, and tests.
- **Compatibility / rollout risk**: A legacy app that receives a new value may show a wrong state or fail. The compatibility window removes this risk until legacy routes are retired.
- **Data migration**: Required.

## Acceptance and Validation

- After migration, no quote row holds `scheduled`, `confirmed`, `inprogress`, `aftercare`, `completed`, `cancelled`, or `rejected`.
- Every migrated accepted quote has exactly one booking with the status in the table above, and the inquiry stage matches it.
- No migrated quote is `confirmed` or `rejected`.
- During the compatibility window, legacy routes return only legacy values; new-version routes return the schema values.

## Approval and Traceability

- **Requested by**: Backend team, follow-up questions F1 and F2.
- **Approved by**: Product Owner, Joachim Trung Tuan, 2026-10-27.
- **Decision evidence**: Product Owner decisions dated 2026-10-27 on `FR015-BA-FOLLOWUP-QUESTIONS-2026-10-26.md` F1 and F2.
- **PRD change log**: [FR-004 Appendix: Change Log](prd.md#appendix-change-log), v3.6 dated 2026-10-27.
- **Update log**: [FR015_FOLLOWUP_QUESTIONS_RESOLUTION_2026-10-27.md](../../update-logs/2026-10-27/FR015_FOLLOWUP_QUESTIONS_RESOLUTION_2026-10-27.md). Addendum 2026-10-28: [FR015_BE_CONFIRMATIONS_RESOLUTION_2026-10-28.md](../../update-logs/2026-10-28/FR015_BE_CONFIRMATIONS_RESOLUTION_2026-10-28.md).
- **Supersedes**: None.
- **Superseded by**: None.
