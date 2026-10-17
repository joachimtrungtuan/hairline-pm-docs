# Change Request: MTG-002 Quote Model Alignment for Notifications

**Change Request ID**: CR-FR020-20261016-01
**Primary FR**: FR-020
**Triggering FR / Event**: MTG-002 quote model (meeting 02) and FR-030 v1.12 (CR-FR030-20261016-01)
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-16
**Decision Date**: 2026-10-16
**PRD Version Change**: v2.6 to v2.8 (v2.7 MTG-002 alignment; v2.8 Product Owner follow-up decisions)
**Related Commit(s)**: Pending

> Create this document only for a major requirement event: a new or materially revised FR changes another verified or implemented FR, or an approved restructure substantially changes requirements, ownership, workflow, data, security, or integration contracts. Record small corrections only in the PRD change log and normal update log.

---

## Decision Summary

MTG-002 replaced the single quote total with a parent quote holding subquotes (option × date range), a fixed slot hold from acceptance, a first-payment Payment Window Expired outcome, admin revive, and a provider-fault replacement transfer. FR-030 v1.12 updated the source-of-truth event catalogue. FR-020 mirrors that catalogue and adds the dispatch rules, recipient matrix and acceptance-outcome scenarios. This CR exists because the change adds mandatory events and changes notification payload, grain and lock contracts.

## Baseline State

**Source version**: FR-020 v2.6, Scope Boundaries event table, Business Rules, User Scenarios & Testing, Functional Requirements Summary, Key Entities

- `quote.submitted` "starts quote expiry timer"; no rule on which price it shows.
- No `quote.withdrawn`, hold-expiring-soon, Payment Window Expired, booking revived, provider-fault replacement or treatment-change events.
- `quote.accepted` outcomes named, but no recipient grain, no same-provider matrix, no rule for unsent drafts, and no locks.
- `quote.declined` listed as an MVP event.
- `booking.scheduled` shown as "Booking Scheduled (Pending Payment)".
- Key Entities used `outcomeCode`; FR-030 uses `outcome`.
- No user story for acceptance outcomes.

## Approved State

**Target version**: FR-020 v2.8, same headings plus User Story 6, REQ-020-017, REQ-020-018, REQ-020-019 and REQ-020-020

See the updated PRD. Summary in the delta below. The v2.8 follow-up mirrors FR-030 v1.13: the patient receives only `booking.scheduled` at acceptance, `quote.accepted` goes to providers only, admins are alerted only for the slot hold expiring while unpaid, Payment Window Expired and provider fault, `quote.cancelled_inquiry` cannot be suppressed by FR-032 preferences, and `quote.updated` is the FR-004 re-send of a new quote version.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| `quote.submitted` content | Starts expiry timer; price unspecified | "From" lowest subquote price with currency, option count, treatment, expiry; no single quote total; FR-004 owns expiry | MTG-002, M9 |
| `quote.expiring_soon` | Policy-bound window | Once per sent parent quote at the FR-026 lead time; never for drafts or closed quotes | MTG-002, S4-8 alignment with FR-030 |
| `quote.withdrawn` | Absent | Patient and Admin; mandatory before and after acceptance | D22, S4-1 |
| `quote.accepted` grain and locks | Outcome codes only | One provider notice per sent parent quote; siblings listed in the selected notice; other parents (including the selected provider's) get a not-selected notice; drafts get none; selected and not-selected outcomes locked; no patient or admin recipient; de-duplicated on acceptance record + parent quote + recipient | D20, D21, D5, P2, FR-020-1, FR-020-2, S4-3 |
| Booking events | `booking.scheduled` only before payment | Renamed Booking Accepted — Slot Held (Pending Payment); added `booking.hold_expiring_soon` (configurable), `booking.payment_window_expired` (mandatory, first payment only), `booking.revived` (mandatory), `booking.provider_fault_replacement` (mandatory, includes suspension or deactivation after acceptance) | M13, M17, S4-2, D6 |
| `provider.status_cancellation_patient` | Any provider-status cancellation | Pre-acceptance only; accepted cases use `booking.provider_fault_replacement` | D6, alignment with FR-030 |
| `treatment.plan_changed` | Absent | Mandatory patient notice for audited FR-010 changes; no money changes | M2 |
| Money variables | Unspecified | Post-acceptance money from the accepted snapshot only | M2, S4-5 |
| `quote.declined` | MVP event | Post-MVP / hidden | S4-14 alignment with FR-030 |
| `quote.cancelled_inquiry` row | No lock or variable list | Mandatory provider receipt and variable list mirrored from FR-030 | S4-13 |
| Key Entities | `outcomeCode` | `outcome` | FR-020-7 |
| Testing | No acceptance-outcome scenarios | User Story 6 covers selected provider, sibling, same-provider other parent, competing provider privacy, draft silence, locks and no `quote.declined` | M16, FR-020-4 |
| Acceptance recipients | Patient received `quote.accepted` as well as `booking.scheduled`; admin receipt of `quote.accepted` optional | Patient receives only `booking.scheduled` at acceptance; `quote.accepted` goes to the accepted provider and not-selected providers only; no admin notification for an acceptance | Q10, Q11 |
| Admin exception alerts | No admin recipient on the slot-hold reminder, Payment Window Expired or provider-fault notices | Admin added as exception-alert recipient of `booking.hold_expiring_soon`, `booking.payment_window_expired` and `booking.provider_fault_replacement`; these are the only admin alerts on the quote-to-booking path | Q11 |
| `quote.cancelled_inquiry` preferences | Mandatory in FR-030 but described as subject to FR-032 provider preference toggles | Mandatory; not subject to FR-030 toggles or FR-032 preferences; FR-032 offers no toggle for it | Q12 |
| `quote.updated` | Quote Updated / Revised; meaningful changes, no producer detail | Quote Revised (New Version); FR-004 producer; emitted when a new version of an already-sent parent quote is re-sent | Q24 |
| Mandatory flags and lead times | `booking.provider_fault_replacement` and `treatment.plan_changed` mandatory; lead times from FR-026 | Confirmed unchanged | Q9, Q13 |
| Testing (follow-up) | User Story 4 scenario 3 suppressed `quote.cancelled_inquiry` when FR-032 quote notifications were off | Scenario 3 delivers it regardless; User Story 6 scenario 8 checks the patient gets only `booking.scheduled` and admins get no acceptance notice; REQ-020-019 and REQ-020-020 added | Q10, Q11, Q12 |

## Scope and Impact

### In Scope

- Event catalogue mirror, dispatch rules, recipient matrix, requirements, entity field name and acceptance scenarios listed above.

### Out of Scope

- Payment rails, fund release, refunds and later instalments (only the first-payment Payment Window Expired boundary is stated).
- Changes to `quote.updated` significance (owned by FR-004 and FR-030).
- Template wording, which FR-030 owns.

### Affected Contracts

- **PRD owner**: `fr020-notifications-alerts/prd.md` — Scope Boundaries, Business Rules (Quote, Booking and Treatment-Change Notifications; recipient matrix), Dependencies, User Story 6, REQ-020-012, REQ-020-017, REQ-020-018, Key Entities.
- **Related FRs**: FR-030 (source of truth, CR-FR030-20261016-01), FR-004 (quote events, draft cancellation), FR-005 (acceptance outcomes, accepted snapshot), FR-006 (hold, PWE, revive, provider-fault transfer), FR-010 (treatment-change notice), FR-015 (suspension or deactivation after acceptance), FR-026 (lead times), FR-032 (no provider preference toggle for `quote.cancelled_inquiry`).
- **System documents**: `system-prd.md`, `system-data-schema.md` (notification event `outcome` field), `system-technical-spec.md`.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed.
- **Required assessment**: Notification event keys, template variables, de-duplication key, rule locks, and payload allowlists.
- **Compatibility / rollout risk**: Templates using a single quote total or `outcomeCode` must move to the new variables and field name.
- **Data migration**: To be assessed.

## Acceptance and Validation

- FR-020 and FR-030 list the same events, locks and grain (cross-FR check C10).
- User Story 6 scenarios pass, including no `quote.declined` emission.
- No FR-020 table row breaks column count.
- User Story 6 scenario 8 passes: the patient receives only `booking.scheduled` at acceptance and no admin notification is sent.
- User Story 4 scenario 3 passes: `quote.cancelled_inquiry` is delivered even when the provider has turned off quote notifications in FR-032.
- Admin is a recipient only of `booking.hold_expiring_soon`, `booking.payment_window_expired` and `booking.provider_fault_replacement` on the quote-to-booking path; `quote.updated` names FR-004 and a re-sent new version.

## Approval and Traceability

- **Requested by**: Product Owner
- **Approved by**: Product Owner, 2026-10-16, via the MTG-002 decision log (documentation approval). Implementation reconciliation: required, not assessed.
- **Decision evidence**: `reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md` (D5, D20, D21, D22, M2, M9, M13, M16, M17, P2); findings FR-020-1, FR-020-2, FR-020-4, FR-020-7, S4-1, S4-2, S4-3, S4-5, S4-13, S4-14; Post-execution open questions Q9, Q10, Q11, Q12, Q13, Q24.
- **PRD change log**: v2.7 and v2.8 rows (2026-10-16)
- **Update log**: Pending (controller writes the combined MTG-002 log)
- **Supersedes**: None. Note: the v2.1 quote-outcome change (2026-09-16) had no FR-020 CR; it was approved as FR-005 alignment and is now superseded in substance by this CR.
- **Superseded by**: None
