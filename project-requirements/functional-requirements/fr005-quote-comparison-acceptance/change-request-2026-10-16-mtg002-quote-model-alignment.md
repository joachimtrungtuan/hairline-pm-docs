# Change Request: MTG-002 Quote Model Alignment for Acceptance

**Change Request ID**: CR-FR005-20261016-01
**Primary FR**: FR-005
**Triggering FR / Event**: MTG-002 quote-model verification and Product Owner decision log (2026-10-16)
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-16
**Decision Date**: 2026-10-16
**PRD Version Change**: v2.4 to v2.6
**Related Commit(s)**: Pending

> Create this document only for a major requirement event: a new or materially revised FR changes another verified or implemented FR, or an approved restructure substantially changes requirements, ownership, workflow, data, security, or integration contracts. Record small corrections only in the PRD change log and normal update log.

---

## Decision Summary

The MTG-002 quote-model verification found that FR-005 allowed admins to soft-delete and restore acceptance records, did not define recovery after `Payment Window Expired`, did not name the hold key or owner, omitted the exchange-rate timestamp and patient promotion codes from the acceptance snapshot, and had no provider-fault path after acceptance. The Product Owner decisions of 2026-10-16 make the AcceptanceEvent strictly append-only, define a single provider-fault exception through a linked record, fix the hold at acceptance, and bind the money fields of the snapshot. This Change Request exists because these decisions change FR-005 workflow, data, permission, and integration contracts consumed by FR-004, FR-006, FR-007, FR-010, FR-019, FR-020, and FR-026.

## Baseline State

**Source version**: FR-005 v2.4, `Business Rules`, `Admin Editability Rules`, `Payment & Billing Rules (for Handoff)`, and `Key Entities`

- Admins could soft-delete and restore acceptance, parent quote, and subquote records, and could "resolve conflicts" with no defined outcome.
- The AcceptanceEvent carried a mutable `supersededByCancellation` flag and had no `id`.
- Rule 1 allowed one acceptance per inquiry with no defined exception, and withdrawal after acceptance was unhandled.
- The hold used an FR-006 configurable duration with no key, and the appointment creation point was not stated.
- The snapshot omitted the exchange-rate timestamp, patient promotion codes, and several inherited fields, and did not say which fields bind downstream modules.
- No acceptance-outcome or exception scenarios existed.

## Approved State

**Target version**: FR-005 v2.6, same headings plus Alternative Flows A7 and A8, User Stories 4 and 5, and REQ-005-023 to REQ-005-029

The updated PRD owns the detail. In summary: acceptance records are annotated only; one patient acceptance per inquiry, with a provider-fault transfer creating a new linked admin-authored record; one fixed hold from acceptance for the FR-026 duration keyed by provider, appointment date/time, and time zone, with the appointment created only on first payment; a defined recovery route after `Payment Window Expired`; patient promotion codes frozen at acceptance; and a snapshot whose money fields bind downstream modules while treatment details change only through FR-010. The v2.6 Q-series additions: price sort converts to the display currency for ordering only and is labelled approximate when currencies are mixed; the auto-applied promotion use reserved at send is consumed at acceptance and released for quotes that end Not Selected or auto-cancelled; the patient receives only `booking.scheduled` at acceptance; and a concurrent second acceptance fails on the existing active hold with a "slot was just taken" message.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Admin actions on acceptance | Soft-delete/restore of acceptance, parent quote, and subquote; undefined conflict resolution | Audited "Add note or correction" annotation only; no delete, restore, or edit; first valid acceptance stands | D4 (FR-005-4) |
| Supersession | Mutable `supersededByCancellation` flag | Linked append-only AcceptanceSupersession record (inquiry cancelled or provider fault) | D6, FR-005-11, S1-13 |
| Rule 1 exception | None | Provider-fault transfer (FR-006) creates a new admin-authored acceptance record linked to the original; paid money moves as credit, details in the payment pass | D6, D6-M, D3, S1-3 |
| Payment Window Expired | Recovery route undefined | Accepted subquote never reopened; patient cancels and starts a new inquiry or contacts support for the FR-006 revive; applies only to the first payment | D1, D2, S1-1 |
| Slot hold | FR-006 duration, no key, no appointment rule | One fixed hold from acceptance for the FR-026 duration, keyed by provider, appointment date/time, and time zone; never extended; appointment created at first payment | M3, M4, D14, S1-2, S1-6 |
| Exchange rate | Locked at acceptance | Rate and timestamp recorded; a stale cached rate proceeds and is recorded with no review state | D19, FR-017-1 |
| Promotion code | Not supported | Patient code on one named subquote before acceptance; discounted price frozen into the snapshot; no change after acceptance | D8, D9, FR-019-1 |
| Snapshot scope | Partial field list; no binding rule | Full field list; price, currency, date range, appointment, and promotion bind downstream; treatment details change only through FR-010 with audit and patient notice | M2, S1-4 |
| Subquote count and identity | Unstated | Up to options × date ranges; FR-005 owns subquote ID (derived from option and date-price IDs) and state; AcceptanceEvent carries `id`, `quoteOptionId`, `optionDatePriceId` | M1, S1-5, S1-10 |
| Withdrawal after acceptance | Unhandled | A3 points to the FR-006 provider-fault case | D3, S1-3 |
| Provider suspension or deactivation after acceptance | Accepted quote and inquiry cancelled; patient contacts support | Provider-fault transfer: booking closes with cause ProviderSuspended or ProviderDeactivated (FR-006 B4 to B5), hold released, AcceptanceEvent superseded through the linked record with that cause, admin rehomes the patient in the same inquiry, paid-money placeholder applies; before acceptance unchanged | M18, D6, D6-M |
| Price sort across currencies | Unstated | Converted to the patient display currency at the current rate for ordering only; cards keep their own currency; mixed-currency order labelled approximate (REQ-005-027) | Q8 |
| Auto-applied promotion use | Unstated | Use reserved at send (at most one per sent quote across re-sent versions) is consumed at acceptance; reservations of Not Selected or auto-cancelled quotes released; consumed use returns to the limit on Payment Window Expired or cancellation before first payment (REQ-005-028) | Q6, Q29, Q30 |
| Patient notice at acceptance | Notifications to the patient unspecified | Patient receives only `booking.scheduled`; `quote.accepted` goes to providers only (REQ-005-029) | Q10 |
| Concurrent slot acceptance | Patient told the appointment is no longer available | Second acceptance fails because an active hold exists; error state "This appointment slot was just taken"; no Accepted state (A5, Screen 3, REQ-005-021) | Q23 |
| Acceptance-outcome tests | None | User Story 4 (one notice per parent quote, no winner identity or price, no notice for cancelled drafts, no `quote.declined`) and User Story 5 (exceptions) | M16, D20, P2, FR-020-4, FR-005-10 |

## Scope and Impact

### In Scope

- FR-005 admin actions, Rule 1, alternative flows A3, A4, A7, A8, Screens 1, 2, 4 and 5, payment handoff rules, dependencies, user stories, requirements, and Key Entities.
- Minor corrections: currency and promotion in comparison and provider outcome, `acceptedTotal` write, compare-panel refresh, approvals row, and change-log order.
- Correction of the stale system-documents line in CR-FR005-20260915-01.

### Out of Scope

- Payment rails, refund and fund-release mechanics, admin payment-allocation overrides, and later instalments (payment pass; the D6-M placeholder only is recorded).
- The FR-006 provider-fault transfer and admin revive procedures, which FR-006 owns.
- Implementation, API, and migration changes.

### Affected Contracts

- **PRD owner**: `project-requirements/functional-requirements/fr005-quote-comparison-acceptance/prd.md` — Admin Editability Rules, General Module Rules 1 and 6, Payment & Billing Rules, Alternative Flows A3, A7, A8, User Stories 4 and 5, REQ-005-006, REQ-005-017, REQ-005-018, REQ-005-020, REQ-005-023 to REQ-005-026, Key Entities.
- **Related FRs**: FR-004 (`acceptedTotal`, silent draft cancellation, subquote state ownership), FR-006 (provider-fault transfer and linked records, including Alternative Flows B4 and B5 for provider suspension or deactivation after acceptance, `Payment Window Expired` boundary and admin revive, appointment created at first payment, supersession record), FR-007 and FR-007b (snapshot money fields), FR-010 (only route for post-acceptance treatment changes), FR-017 (stale FX rate recording), FR-019 (patient code validation, usage limits), FR-020 and FR-030 (one notice per parent quote, no `quote.declined`), FR-022 (subquote-level search, filter and price sort for patients), FR-026 (slot-hold duration owner).
- **System documents**: `system-prd.md`, `system-data-schema.md` (dedicated `acceptance_events` table with `id`, option IDs, and linked supersession and annotation records), and `system-technical-spec.md` (hold at acceptance, appointment at payment).

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed in this documentation phase.
- **Required assessment**: Admin acceptance actions (removal of delete/restore), AcceptanceEvent storage and supersession linkage, hold key and expiry handling, appointment creation point, promotion-code entry and snapshot freeze, FX timestamp, notification grain, and regression coverage.
- **Compatibility / rollout risk**: High. Existing soft-deleted or restored acceptance records and the mutable superseded flag may need migration to linked records.
- **Data migration**: To be assessed.

## Acceptance and Validation

- No soft-delete, restore, or edit path exists for acceptance records; annotation only.
- Rule 1 names the provider-fault linked-record exception and nothing else; it covers provider withdrawal, drop-out, suspension, and deactivation after acceptance.
- The snapshot lists price, currency, date range, appointment, and promotion as binding money fields, plus the exchange rate and its timestamp.
- The hold is one fixed hold from acceptance for the FR-026 duration, keyed by provider, appointment date/time, and time zone, and the appointment is created only at first payment.
- Price sort orders by converted display-currency value, cards show their own currency, and mixed-currency order is labelled approximate.
- The reserved auto-applied promotion use is consumed for the accepted quote and released for every quote that ends Not Selected or auto-cancelled.
- The patient receives only `booking.scheduled` at acceptance; no `quote.accepted` reaches the patient.
- A concurrent second acceptance for the same slot fails on the existing active hold, shows the "slot was just taken" message, and creates no Accepted state.
- Cross-FR checks against FR-006, FR-010, FR-019, FR-020, and FR-026 pass in consolidated verification.
- Observation recorded: CR-FR005-20260915-01 predates the v2.3 slot-hold atomicity and the v2.4 provider-status cascade; both are clarifications covered by the PRD change log and need no separate CR.

## Approval and Traceability

- **Requested by**: Product Owner (MTG-002 quote-model verification)
- **Approved by**: Product Owner — documentation approved 2026-10-16 via the decision log; implementation reconciliation required, not assessed
- **Decision evidence**: SRC-MTG-002; `reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md` (D1, D2, D3, D4, D6, D6-M, D8, D9, D14, D19, D20, M1, M2, M3, M4, M16, M18, P2, R7-1, R7-3; Q-series Q6, Q8, Q10, Q23, Q29, Q30)
- **PRD change log**: FR-005 v2.5 and v2.6 rows dated 2026-10-16
- **Update log**: `../../update-logs/2026-10-16/MTG002_QUOTE_MODEL_ALIGNMENT_2026-10-16.md`
- **Supersedes**: None
- **Superseded by**: None
