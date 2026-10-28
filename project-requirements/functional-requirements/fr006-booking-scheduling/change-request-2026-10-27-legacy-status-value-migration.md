# Change Request: Legacy Booking Status Value Migration

**Change Request ID**: CR-FR006-20261027-01
**Primary FR**: FR-006
**Triggering FR / Event**: FR-015 provider-status cascade release; backend follow-up questions F1 and F2 (`FR015-BA-FOLLOWUP-QUESTIONS-2026-10-26.md`); Product Owner decision 2026-10-27
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-26
**Decision Date**: 2026-10-27
**PRD Version Change**: None (records a value migration only; the PRD is current at v2.11)
**Related Commit(s)**: Pending

---

## Decision Summary

The booking status values in FR-006 and in the system data schema are unchanged. This Change Request formally records that legacy implementation data is migrated to those values in the release that ships the FR-015 provider-status cascade. It also records what legacy API routes return to already-built apps for the new booking values during a backward-compatibility window.

This is one of three linked Change Requests:

- [CR-FR003-20261027-01](../fr003-inquiry-submission/change-request-2026-10-27-legacy-status-value-migration.md): inquiry stages and `inquiry_providers` participation.
- [CR-FR004-20261027-01](../fr004-quote-submission/change-request-2026-10-27-legacy-status-value-migration.md): quote status, including the legacy stage values stored on `quotes.status`.
- CR-FR006-20261027-01 (this document): booking status.

## Baseline State

**Source version**: FR-006 v2.10, Main Flow and Alternative Flows B1 to B7; system data schema v1.12.0, §11A `bookings` and the ENUM Types list.

- The requirement booking statuses are `accepted`, `payment_window_expired`, `confirmed`, `in_progress`, `aftercare`, `completed`, and `cancelled`. The booking is created as `accepted` at acceptance.
- The legacy implementation keeps the case stage on `quotes.status`, and a legacy `scheduled` quote may have no booking yet. Already-built apps do not know `accepted` as a booking value, `payment_window_expired`, or provider-status cancellation causes.
- No requirement document stated how legacy data becomes booking values or what legacy routes return for the new values.

## Approved State

**Target version**: FR-006 v2.11 (requirement values unchanged); system data schema v1.13.0, ENUM Types note.

### Old to new (data migration)

Booking statuses are derived from the legacy stage values on `quotes.status`. The full table, including the matching quote status and inquiry stage, is in CR-FR004-20261027-01. In short:

| Legacy value on `quotes.status` | New booking status |
|---|---|
| `scheduled`, no paid deposit, payment-window hold still open | `accepted` |
| `scheduled`, no paid deposit, payment-window hold no longer open | `payment_window_expired` |
| `scheduled` with a paid deposit, or `confirmed` | `confirmed` |
| `inprogress` | `in_progress` |
| `aftercare` | `aftercare` |
| `completed` | `completed` |
| `cancelled` on an accepted quote | `cancelled` (the inquiry also becomes `cancelled`; the quote stays `accepted`) |
| Any value not listed | The backend team lists it and the BA maps it before the migration runs. |

Where no booking row exists, the migration creates it with the status above. The appointment record (`schedules`) exists only where a first payment succeeded, as in FR-006 Main Flow.

### New to old (legacy `/api/v1` routes during the compatibility window)

| New booking value | What a legacy route returns |
|---|---|
| `accepted` | `pending_deposit` |
| `payment_window_expired` | `cancelled`, with the reason "Payment window expired" |
| `cancelled` by a provider suspension or deactivation (cause `ProviderSuspended` or `ProviderDeactivated`) | `cancelled`, with the cause as the reason |
| Other values | Their legacy spelling (for example `in_progress` becomes `inprogress`). A value with no legacy spelling is listed by the backend team and mapped by the BA before release. |

### Compatibility window

- New values are returned only on new-version routes. Legacy routes keep returning legacy values for the backend deprecation window (backend ADR-003: 3 months).
- Before building, the backend team lists the endpoints whose returned values or structure change and need a new version, and confirms that list with the BA and the Product Owner.
- Internal tester builds count as consumers of legacy routes (Product Owner decision).

### Addendum 2026-10-28 (Product Owner)

This addendum extends the Approved State above; the 2026-10-27 tables are unchanged.

#### Legacy quote status and aftercare record disagree

- When a legacy quote that migrates to quote status `accepted` has a treatment-linked aftercare record, the aftercare record's status decides the booking and inquiry, whatever the legacy `quotes.status` says (follow-up decision, 2026-10-28):
  - active aftercare: the booking and the inquiry become `aftercare`;
  - suspended (paused) aftercare: the booking and the inquiry become `aftercare`, and the aftercare record keeps its `suspended` status;
  - completed aftercare: the booking and the inquiry become `completed`;
  - cancelled aftercare: the row is listed for BA review, and the BA decides it before the migration runs.
- The quote becomes `accepted` in each case. Every such row is listed in the dry-run report.
- A non-accepted legacy quote with an aftercare record remains invalid data under the CR-FR004-20261027-01 Addendum 2026-10-28.

#### Legacy rows with no acceptance data

- Some legacy rows have no quote options, no option date prices, and no AcceptanceEvent (rows on staging). The schema is not relaxed for them: `acceptance_event_id`, the NOT NULL hold fields (`hold_appointment_at`, `hold_appointment_timezone`, `hold_started_at`, `hold_expires_at`), and `booking_total` (copied from the acceptance snapshot) stay NOT NULL.
- In non-production environments (`backend.hairline.app` is a dev/test environment with no real patient data), these rows are deleted, or recreated through the current flow, before the migration runs.
- Cleanup deletes or recreates the whole case together: the inquiry, its quotes, the booking, appointments and schedules, payments, and aftercare. It never deletes only the quote, so no remaining record points at a deleted one. The dry-run report lists the dependent records of each case before cleanup. This cleanup applies to non-production environments only.
- If such rows ever appear in production data, the BA decides each row before the migration runs.

#### API versions

The API version rules (legacy values on unversioned `/api/...` and `/api/v1/...` routes, new values only on `v2` routes, webhook routes excluded from the `v1` alias) and the endpoint list completion rules are in the CR-FR004-20261027-01 Addendum 2026-10-28; they apply to booking values as well.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Booking status values (FR-006; schema §11A) | Requirement values defined; no migration rule from legacy data | Requirement values unchanged; legacy stage values map to booking statuses, and missing booking rows are created | The legacy implementation kept the case stage on the quote |
| Legacy API responses | Not defined | `accepted` shows as `pending_deposit`, `payment_window_expired` and provider-status cancellations show as `cancelled` with a reason, other values in legacy spelling | Already-built apps must not show wrong states or fail |

## Scope and Impact

### In Scope

- Booking status values produced by the data migration.
- What legacy routes return for booking values during the compatibility window.

### Out of Scope

- Any change to the FR-006 requirement values or lifecycle.
- The technical API versioning scheme, which the backend team owns.
- An admin revive on a legacy app: the legacy `cancelled` shown for `payment_window_expired` does not change the admin revive rules in FR-006.

### Affected Contracts

- **PRD owner**: `project-requirements/functional-requirements/fr006-booking-scheduling/prd.md`: Main Flow, Alternative Flows B1 and B4, Key Entities. No PRD text changes for this Change Request.
- **Related FRs**: FR-003 (CR-FR003-20261027-01), FR-004 (CR-FR004-20261027-01), FR-015 (the release that ships the provider-status cascade).
- **System documents**: `system-data-schema.md` v1.13.0, ENUM Types note.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed in source. The backend team reports that stage is held on `quotes.status` and that dashboard overview endpoints return values such as `inprogress` and `aftercare`.
- **Required assessment**: Migration script, booking creation for cases without a booking, payment and hold checks, legacy-route value translation, the endpoint list that needs a new version, and tests.
- **Compatibility / rollout risk**: A legacy app that receives a new value may show a wrong state or fail. The compatibility window removes this risk until legacy routes are retired.
- **Data migration**: Required.

## Acceptance and Validation

- Every migrated accepted case has one booking with the status in the table above.
- During the compatibility window, legacy routes return `pending_deposit` for `accepted`, `cancelled` with the reason "Payment window expired" for `payment_window_expired`, and `cancelled` with the cause as the reason for provider-status cancellations.
- New-version routes return the schema values.

## Approval and Traceability

- **Requested by**: Backend team, follow-up questions F1 and F2.
- **Approved by**: Product Owner, Joachim Trung Tuan, 2026-10-27.
- **Decision evidence**: Product Owner decisions dated 2026-10-27 on `FR015-BA-FOLLOWUP-QUESTIONS-2026-10-26.md` F1 and F2.
- **PRD change log**: [FR-006 Appendix: Change Log](prd.md#appendix-change-log), v2.11 dated 2026-10-27.
- **Update log**: [FR015_FOLLOWUP_QUESTIONS_RESOLUTION_2026-10-27.md](../../update-logs/2026-10-27/FR015_FOLLOWUP_QUESTIONS_RESOLUTION_2026-10-27.md). Addendum 2026-10-28: [FR015_BE_CONFIRMATIONS_RESOLUTION_2026-10-28.md](../../update-logs/2026-10-28/FR015_BE_CONFIRMATIONS_RESOLUTION_2026-10-28.md).
- **Supersedes**: None.
- **Superseded by**: None.
