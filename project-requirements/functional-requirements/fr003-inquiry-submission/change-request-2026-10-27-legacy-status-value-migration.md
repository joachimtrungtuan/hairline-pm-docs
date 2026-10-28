# Change Request: Legacy Inquiry Stage and Participation Value Migration

**Change Request ID**: CR-FR003-20261027-01
**Primary FR**: FR-003
**Triggering FR / Event**: FR-015 provider-status cascade release; backend follow-up questions F1 and F2 (`FR015-BA-FOLLOWUP-QUESTIONS-2026-10-26.md`); Product Owner decision 2026-10-27
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-26
**Decision Date**: 2026-10-27
**PRD Version Change**: None (records a value migration only; the PRD is current at v2.12)
**Related Commit(s)**: Pending

---

## Decision Summary

The inquiry stage values in FR-003 and in the system data schema are unchanged. This Change Request formally records that the legacy implementation values are migrated to those values in the release that ships the FR-015 provider-status cascade. It also records how legacy API routes keep returning legacy values to already-built apps during a backward-compatibility window.

The backend team asked for a formal record (F1) and a full two-way mapping (F2). Until now the decision existed only in a delivery report, and the schema gave only a partial mapping.

This is one of three linked Change Requests:

- CR-FR003-20261027-01 (this document): inquiry stages and `inquiry_providers` participation.
- [CR-FR004-20261027-01](../fr004-quote-submission/change-request-2026-10-27-legacy-status-value-migration.md): quote status, including the legacy stage values stored on `quotes.status`.
- [CR-FR006-20261027-01](../fr006-booking-scheduling/change-request-2026-10-27-legacy-status-value-migration.md): booking status.

## Baseline State

**Source version**: FR-003 v2.11, Key Entities (Inquiry status enum, ProviderInquiry status); system data schema v1.12.0, §5 Inquiry stages and §5A `inquiry_providers`.

- The requirement stage values are `inquiry`, `quoted`, `accepted`, `confirmed`, `in_progress`, `aftercare`, `completed`, and `cancelled`.
- The legacy implementation stores `requested`, `offers`, and `scheduled` on `inquiries.status`. The schema said only that `requested` maps to `inquiry`, `offers` maps to `quoted`, and `scheduled` maps to the stage of its booking.
- `inquiry_providers.status = cancelled` (participation cancelled by a provider suspension or deactivation) is a new value. Already-built apps do not know it.

## Approved State

**Target version**: FR-003 v2.12 (requirement values unchanged); system data schema v1.13.0, §5 Inquiry stages note.

### Old to new (data migration)

| Legacy `inquiries.status` | Migrated inquiry stage |
|---|---|
| `requested` | `inquiry` |
| `offers` | `quoted` |
| `scheduled` | The stage of its booking, derived from the booking migration in CR-FR006-20261027-01 and the quote migration in CR-FR004-20261027-01. A booking in `payment_window_expired` leaves the inquiry at `accepted`, because the inquiry stage list has no expired value. |
| Any value not listed | The backend team lists it and the BA maps it before the migration runs. |

Existing `inquiry_providers` participation rows keep their values. `cancelled` is written only by the provider-status cascade after release.

### New to old (legacy `/api/v1` routes during the compatibility window)

| New value | What a legacy route returns |
|---|---|
| Inquiry `inquiry` | `requested` |
| Inquiry `quoted` | `offers` |
| Other inquiry stages | Their legacy spelling (for example `in_progress` becomes `inprogress`). A value with no legacy spelling is listed by the backend team and mapped by the BA before release. |
| `inquiry_providers.status = cancelled` | That provider is hidden from the legacy provider list for the inquiry. |

### Compatibility window

- New values are returned only on new-version routes. Legacy routes keep returning legacy values for the backend deprecation window (backend ADR-003: 3 months).
- Before building, the backend team lists the endpoints whose returned values or structure change and need a new version, and confirms that list with the BA and the Product Owner.
- Internal tester builds count as consumers of legacy routes (Product Owner decision).

### Addendum 2026-10-28 (Product Owner)

This addendum extends the Approved State above; the 2026-10-27 tables are unchanged.

#### Legacy `offers` inquiry whose quote has progressed

| Legacy `inquiries.status` | Migrated inquiry stage |
|---|---|
| `offers`, and a quote of the inquiry has already progressed (legacy quote status `accepted`, `confirmed`, `inprogress`, `aftercare`, or `completed`) | The stage of its booking after migration, as for the `scheduled` row (CR-FR006-20261027-01, CR-FR004-20261027-01) |

#### API versions

The API version rules (legacy values on unversioned `/api/...` and `/api/v1/...` routes, new values only on `v2` routes, webhook routes excluded from the `v1` alias) and the endpoint list completion rules are in the CR-FR004-20261027-01 Addendum 2026-10-28; they apply to inquiry stage values as well.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Inquiry stage values (FR-003 Key Entities; schema §5) | Requirement values defined; legacy migration recorded only as a partial schema note | Requirement values unchanged; full two-way mapping and release timing recorded here | Backend needs a formal, approved record of what changes and when |
| Legacy API responses | Not defined | Legacy routes return legacy values during the compatibility window; new values only on new-version routes | Already-built apps must not show wrong states or fail |
| `inquiry_providers` cancelled participation on legacy routes | Not defined | The cancelled provider is hidden from the legacy list | Legacy apps have no value for a cancelled participation |

## Scope and Impact

### In Scope

- Data migration of legacy `inquiries.status` values.
- What legacy routes return for inquiry stages and cancelled participation during the compatibility window.

### Out of Scope

- Any change to the FR-003 requirement values or lifecycle.
- The technical API versioning scheme, which the backend team owns.
- Quote and booking value mappings, which are in the two linked Change Requests.

### Affected Contracts

- **PRD owner**: `project-requirements/functional-requirements/fr003-inquiry-submission/prd.md`: Key Entities (Inquiry, ProviderInquiry). No PRD text changes.
- **Related FRs**: FR-004 (CR-FR004-20261027-01), FR-006 (CR-FR006-20261027-01), FR-015 (the release that ships the provider-status cascade).
- **System documents**: `system-data-schema.md` v1.13.0, §5 Inquiry stages note.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed in source. The backend team reports legacy values `requested`, `offers`, and `scheduled` on inquiries, and that chat reads `inquiry_providers.status` as an invitation status.
- **Required assessment**: Migration script, legacy-route value translation, the endpoint list that needs a new version, patient inquiry list, dashboard overview, chat, and tests.
- **Compatibility / rollout risk**: A legacy app that receives a new value may show a wrong state or fail. The compatibility window removes this risk until legacy routes are retired.
- **Data migration**: Required.

## Acceptance and Validation

- After migration, no inquiry row holds `requested`, `offers`, or `scheduled`.
- Every migrated `scheduled` inquiry has the stage of its migrated booking, or `accepted` when that booking is `payment_window_expired`.
- During the compatibility window, legacy routes return only legacy values, and a provider with cancelled participation does not appear in the legacy provider list.
- New-version routes return the schema values.
- The backend endpoint list is confirmed by the BA and the Product Owner before the build starts.

## Approval and Traceability

- **Requested by**: Backend team, follow-up questions F1 and F2.
- **Approved by**: Product Owner, Joachim Trung Tuan, 2026-10-27.
- **Decision evidence**: Product Owner decisions dated 2026-10-27 on `FR015-BA-FOLLOWUP-QUESTIONS-2026-10-26.md` F1 and F2.
- **PRD change log**: [FR-003 Appendix: Change Log](prd.md#appendix-change-log), v2.12 dated 2026-10-27.
- **Update log**: [FR015_FOLLOWUP_QUESTIONS_RESOLUTION_2026-10-27.md](../../update-logs/2026-10-27/FR015_FOLLOWUP_QUESTIONS_RESOLUTION_2026-10-27.md). Addendum 2026-10-28: [FR015_BE_CONFIRMATIONS_RESOLUTION_2026-10-28.md](../../update-logs/2026-10-28/FR015_BE_CONFIRMATIONS_RESOLUTION_2026-10-28.md).
- **Supersedes**: None.
- **Superseded by**: None.
