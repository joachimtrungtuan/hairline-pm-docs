# Change Request: MTG-002 Quote Model Event Alignment

**Change Request ID**: CR-FR030-20261016-01
**Primary FR**: FR-030
**Triggering FR / Event**: MTG-002 quote model decisions (2026-10-16) applied to FR-004, FR-005, FR-006 and FR-010
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-16
**Decision Date**: 2026-10-16
**PRD Version Change**: v1.11 to v1.13 (v1.12 MTG-002 alignment; v1.13 Product Owner follow-up decisions)
**Related Commit(s)**: Pending

---

## Decision Summary

MTG-002 replaced the single-price quote with parent quotes holding option and date-range subquotes, made the accepted snapshot the money record, and added hold expiry, admin revive and provider-fault transfer flows. FR-030 is the source-of-truth event catalogue, so it must register the events those flows produce, lock the ones the Product Owner made mandatory, and stop offering a single quote total. Decisions: D20, D21, D22, M2, M9, M13, M17, M18 (decision log `reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md`).

## Baseline State

**Source version**: v1.11, "Admin-Configurable Notification Event Catalog (Preset by Backend)" and "Admin Editability Rules"

- No event for quote withdrawal, slot-hold expiry reminder, Payment Window Expired, booking revive, provider fault after acceptance, or post-acceptance treatment-detail changes.
- `quote.accepted` could be fully disabled; notice grain per parent quote and the draft rule were undefined.
- `quote.submitted` template example used `{{quote.total_amount}}`, and the note claimed the event starts the expiry timer.
- No rule that post-acceptance money variables read the accepted snapshot; FR-004, FR-005, FR-006 and FR-010 were missing from dependencies.
- `quote.declined` shown in the MVP catalogue without a producer; "Quote Received" and "Payment Confirmed" used instead of catalogue names.

## Approved State

**Target version**: v1.13, same headings plus new "Quote, Booking and Treatment-Change Event Rules"

See the updated PRD. Registered event keys: `quote.withdrawn`, `booking.hold_expiring_soon`, `booking.payment_window_expired`, `booking.revived`, `booking.provider_fault_replacement`, `treatment.plan_changed`; updated `quote.submitted`, `quote.expiring_soon`, `quote.accepted`, `booking.scheduled`, `provider.status_cancellation_patient`.

v1.13 follow-up: at acceptance the patient receives only `booking.scheduled`, and `quote.accepted` goes to the accepted and not-selected providers only, with no patient or admin recipient. Admins are alerted only for exceptions: `booking.hold_expiring_soon`, `booking.payment_window_expired` and `booking.provider_fault_replacement` now list Admin as a recipient. `quote.cancelled_inquiry` is mandatory and cannot be suppressed by FR-032 provider preferences. `quote.updated` is Quote Revised (New Version), produced by FR-004 when a new version of a sent quote is re-sent. `booking.provider_fault_replacement` and `treatment.plan_changed` stay mandatory, and lead times stay in FR-026.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| `quote.withdrawn` | Not in catalogue | Patient and Admin, FR-004 producer, mandatory before and after acceptance | D22 |
| `quote.accepted` | Fully configurable; grain undefined | One provider notice per sent parent quote, siblings listed in the selected notice, no notice for drafts; selected and not-selected provider outcomes locked | D20, D21 |
| `quote.submitted` | Single quote amount; claimed to start expiry timer | "From" lowest subquote price, option count, treatment and expiry; expiry owned by FR-004 | M9 |
| `quote.expiring_soon` | Expiry window wording, no producer | FR-004 producer, FR-026 lead time, once per sent parent quote | M13 handoff from FR-004 |
| Hold expiring soon | Not in catalogue | `booking.hold_expiring_soon`, Patient, FR-006 producer, FR-026 lead time, configurable | M13 |
| Payment Window Expired | Not in catalogue | `booking.payment_window_expired`, Patient and Provider, mandatory, first payment step only | M13, D22, D1 boundary |
| Booking revived | Not in catalogue | `booking.revived`, Patient and Provider, mandatory | M17 |
| Provider fault after acceptance | Not in catalogue; patient got status cancellation notice | `booking.provider_fault_replacement`, Patient, mandatory, covers suspension or deactivation after acceptance | D6, M18 |
| Treatment detail change | Not in catalogue | `treatment.plan_changed`, Patient, FR-010 producer, mandatory, no money change | M2 |
| Variable sourcing | No rule | Pre-acceptance parent-level variables only; post-acceptance money from the accepted snapshot | M2, M9 |
| `booking.scheduled`, `quote.declined`, event names | Drifted names; declined in MVP | Renamed display; declined moved to Post-MVP; catalogue names used | Minor fixes |
| Acceptance recipients | Patient received `quote.accepted` as well as `booking.scheduled`; admin receipt of `quote.accepted` optional | Patient receives only `booking.scheduled` at acceptance; `quote.accepted` goes to the accepted provider and not-selected providers only; no admin notification for an acceptance | Q10, Q11 |
| Admin exception alerts | No admin recipient on the slot-hold reminder, Payment Window Expired or provider-fault notices | Admin added as exception-alert recipient of `booking.hold_expiring_soon`, `booking.payment_window_expired` and `booking.provider_fault_replacement`; these are the only admin alerts on the quote-to-booking path | Q11 |
| `quote.cancelled_inquiry` preferences | Mandatory in FR-030 but described as subject to FR-032 provider preference toggles | Mandatory; not subject to FR-030 toggles or FR-032 preferences; FR-032 offers no toggle for it | Q12 |
| `quote.updated` | Quote Updated / Revised; meaningful changes, no producer detail | Quote Revised (New Version); FR-004 producer; emitted when a new version of an already-sent parent quote is re-sent | Q24 |
| Mandatory flags and lead times | `booking.provider_fault_replacement` and `treatment.plan_changed` mandatory; lead times from FR-026 | Confirmed unchanged | Q9, Q13 |

## Scope and Impact

### In Scope

- Event catalogue rows, mandatory locks, variable-sourcing rules, dependencies, examples and user story text in FR-030.

### Out of Scope

- Payment rails, fund release, refunds and later instalments (payment pass); `payment.*` recipient changes.
- Rule Editor screen layout for per-outcome locks.

### Affected Contracts

- **PRD owner**: `fr030-notification-rules-config/prd.md` — event catalogue, Quote, Booking and Treatment-Change Event Rules, Admin Editability Rules, Internal Dependencies, User Story 2
- **Related FRs**: FR-020 (mirror catalogue, locks and grain), FR-004 (producer of quote events), FR-005 (`quote.accepted` outcomes), FR-006 (booking events), FR-010 (`treatment.plan_changed`), FR-015 (status cancellation before acceptance only), FR-026 (lead-time settings), FR-032 (no provider preference toggle for `quote.cancelled_inquiry`)
- **System documents**: `system-prd.md`, `system-data-schema.md`, `system-technical-spec.md` (event keys and payload identifiers)

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed
- **Required assessment**: Event catalogue API, S-03 payload schemas and allowlists, locked toggles, de-duplication keys, templates using `quote.total_amount`
- **Compatibility / rollout risk**: Existing templates referencing a single quote total will fail validation
- **Data migration**: To be assessed

## Acceptance and Validation

- Every new event shows producer, recipients and mandatory or configurable status in the catalogue.
- FR-020 lists the same events, locks and grain.
- No `quote.total_amount` remains in FR-030.
- `quote.accepted` lists Provider as its only recipient; the patient receives only `booking.scheduled` at acceptance.
- Admin appears as a recipient only on the exception events `booking.hold_expiring_soon`, `booking.payment_window_expired` and `booking.provider_fault_replacement` on the quote-to-booking path.
- `quote.cancelled_inquiry` is locked and is not described as subject to FR-032 preferences.
- `quote.updated` names FR-004 as producer and describes a re-sent new version.

## Approval and Traceability

- **Requested by**: Product Owner (MTG-002 quote model audit)
- **Approved by**: Product Owner, 2026-10-16, via the MTG-002 decision log (documentation approval); implementation reconciliation required, not assessed
- **Decision evidence**: `reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md`; findings S4-1, S4-2, S4-3, S4-5, FR-020-1, FR-030-3, FR-030-7, S4-8, S4-9, S4-14; Post-execution open questions Q9, Q10, Q11, Q12, Q13, Q24
- **PRD change log**: v1.12 and v1.13 rows (2026-10-16)
- **Update log**: Combined 2026-10-16 MTG-002 log (controller-owned)
- **Supersedes**: None
- **Superseded by**: None
