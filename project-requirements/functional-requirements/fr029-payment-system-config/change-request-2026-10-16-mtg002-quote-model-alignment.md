# Change Request: Quote model alignment — configuration lock points and booking total

**Change Request ID**: CR-FR029-20261016-01
**Primary FR**: FR-029
**Triggering FR / Event**: MTG-002 quote/subquote model verification and Product Owner decision log (2026-10-16)
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-16
**Decision Date**: 2026-10-16
**PRD Version Change**: v1.10 to v1.12
**Related Commit(s)**: Pending

> Create this document only for a major requirement event: a new or materially revised FR changes another verified or implemented FR, or an approved restructure substantially changes requirements, ownership, workflow, data, security, or integration contracts. Record small corrections only in the PRD change log and normal update log.

---

## Decision Summary

MTG-002 moved acceptance to the subquote level and fixed commission at booking confirmation. FR-029 Rule 1 still said existing quotes keep their original configuration, which contradicted the Commission Rule, and the commission base "booking total" was undefined. The Product Owner approved named lock points (M5), a single commission base (D12), and an indicative-only commission display on the FR-004 quote screen (D13). This CR records the resulting change to FR-029's configuration-consumption contract. Payment rails are out of scope.

## Baseline State

**Source version**: FR-029 v1.10 — Business Rules (General Module Rules Rule 1; Payment & Billing Rules)

- Rule 1: configuration changes apply to new transactions only, and existing bookings, quotes, and active installment plans keep their original configuration.
- Currency Rule 2, REQ-029-044 and Entity 2c: the conversion rate is locked "at quote acceptance" and stored "per quote/booking/transaction".
- "Booking total" is used as the base for Percentage commission, deposit, and installments but is not defined.
- The commission snapshot stores model, value, and Flat Rate currency only.
- No rule covers a commission shown before booking confirmation, and no user story covers commission resolution.

## Approved State

**Target version**: FR-029 v1.12 — Screen 6, Business Rules, Dependencies, User Story 6, Functional Requirements Summary, Key Entities

- Rule 1 names each lock point: exchange rate at FR-005 subquote acceptance (stored in the acceptance snapshot); commission, deposit rate, and split payment settings at FR-006 booking confirmation; nothing frozen at quote creation or sending.
- New Booking Total Rule: booking total is the accepted subquote price after promotion, in the quote currency, read from the acceptance snapshot and never recomputed from the live quote. It is the base for Percentage commission, deposit, and installments.
- New Indicative Commission Rule: a pre-confirmation commission (including FR-004) shows model and value labelled "indicative, final at booking confirmation"; only the booking snapshot is authoritative.
- The commission snapshot also records source configuration ID and scope type; an accepted-but-unpaid subquote has not yet fixed its commission.
- New User Story 6 and REQ-029-049 to REQ-029-051; FR-004 and FR-005 added to Internal Dependencies.
- The booking total (accepted price after promotion, from the acceptance record) is the single base for deposit percentage, instalment amounts, and commission.
- Commission is on the price after promotion for every discount type, including discounts funded only by Hairline (REQ-029-054).
- Disabling a currency is blocked while any non-terminal sent quote, unpaid accepted booking, or open booking or instalment plan uses it; the admin sees the count of blocking records (REQ-029-052).
- A Default Currency change creates a new FR-026 Quote Configuration version; open drafts keep typed numbers, switch to the new currency, and need a must-acknowledge banner before send, on the FR-004 quote screen (REQ-029-053).

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Rule 1 lock points | Existing quotes, bookings, and plans keep original configuration | FX at subquote acceptance; commission, deposit, and split payment at booking confirmation; nothing at quote creation | FR-029-1, M5 |
| Booking total | Undefined | Accepted subquote price after promotion, quote currency, from acceptance snapshot | FR-029-2, D12 |
| Pre-confirmation commission | Not addressed | Indicative model and value only; booking snapshot is authoritative | S2-4, D13 |
| FX lock vocabulary | Quote acceptance, per quote | Subquote acceptance, stored in acceptance snapshot, copied to booking and transactions | FR-029-5 |
| Commission snapshot | Model, value, Flat Rate currency | Adds source configuration ID and scope type | FR-029-6 |
| Testability | No commission user story | User Story 6 (scheduled activation, model switch, re-acceptance after Payment Window Expired, promotion base, shared-scope split) | FR-029-4, FR-029-7 |
| Discount types | Not stated per discount type | Commission on the price after promotion for every discount type, including Hairline-funded discounts | Q5 |
| Currency disable | Warn and offer a resolution path for configuration references only | Also blocked while any non-terminal sent quote, unpaid accepted booking, or open booking or instalment plan uses the currency; count of blocking records shown | Q7 |
| Default Currency change | No effect on quote configuration or drafts stated | New FR-026 Quote Configuration version; open drafts keep typed numbers, switch currency, and require an acknowledged banner before send (FR-004 screen) | Q4, Q14 |
| Single base | Booking total base for commission, deposit, installments | Confirmed unchanged: one booking total for deposit percentage, instalment amounts, and commission | Q25 |

## Scope and Impact

### In Scope

- How FR-029 configuration is consumed: lock points, commission base, indicative display, snapshot provenance.

### Out of Scope

- Payment rails, Stripe routing, fund release, refunds, later instalment handling, and Flat Rate currency conversion timing (parked for the payment pass).
- Effective Date time zone and activation instant (Observation FR-029-8; locale-safe dates are record-only).

### Affected Contracts

- **PRD owner**: `prd.md` — General Module Rules Rule 1; Payment & Billing Rules (Booking Total Rule, Currency Rule 2, Commission Rule, Indicative Commission Rule); Screen 5 business rules; REQ-029-044, REQ-029-045, REQ-029-049 to REQ-029-051; Entities 2c and 6; User Story 6
- **Related FRs**: FR-004 (commission field shows model and value, labelled indicative); FR-005 (acceptance snapshot holds locked FX rate, price after promotion, quote currency); FR-006 (commission, deposit, and split payment locked at booking confirmation); FR-007 and FR-007b (deposit and installments use the booking total); FR-015 and FR-017 (same commission base sentence and lock points); FR-019 (promotion amount feeds the base)
- **System documents**: `system-data-schema.md` (booking commission snapshot source configuration ID and scope type; FX rate on the acceptance snapshot), `system-technical-spec.md`, `system-prd.md`

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed
- **Required assessment**: Commission snapshot fields and base calculation, FX lock storage location, deposit/installment base, quote-screen commission display
- **Compatibility / rollout risk**: Bookings confirmed before this change may have a commission base before promotion; reconciliation must not recompute them
- **Data migration**: To be assessed

## Acceptance and Validation

- FR-029 Rule 1 names three lock points and nothing is frozen at quote creation.
- One booking total definition is used for commission, deposit, and installments.
- The Booking Total Rule and REQ-029-054 apply the price after promotion to every discount type, including Hairline-funded discounts.
- Screen 6 blocks a currency disable while in-use quotes, bookings, or instalment plans exist and shows their count (REQ-029-052).
- Screen 6 and REQ-029-053 state the new Quote Configuration version and the draft banner on Default Currency change; FR-004 and FR-026 carry matching statements.
- FR-004 and FR-006 describe the pre-confirmation commission as indicative; FR-015, FR-017, and the schema carry the same base and lock points.

## Approval and Traceability

- **Requested by**: Product Owner (MTG-002 quote model verification)
- **Approved by**: Product Owner, 2026-10-16, via `reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md` (M5, D12, D13). Documentation approval only; implementation reconciliation is required and not yet assessed.
- **Decision evidence**: `project-requirements/sources/meetings/meeting-02-launch-quote-options-fund-release-and-payments.md`; decision log above; verification report `reports/2026-10-16/mtg002-quote-model-verification-2026-10-16.md`; Product Owner follow-up decisions Q4, Q5, Q7, Q14, Q25 in `reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md`
- **PRD change log**: v1.11 and v1.12 rows, 2026-10-16
- **Update log**: Pending (controller-owned)
- **Supersedes**: None
- **Superseded by**: None
