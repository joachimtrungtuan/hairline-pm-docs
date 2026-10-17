# Change Request: MTG-002 Quote Model Alignment for Promotions

**Change Request ID**: CR-FR019-20261016-01
**Primary FR**: FR-019
**Triggering FR / Event**: MTG-002 quote-model verification and Product Owner decision log (2026-10-16)
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-16
**Decision Date**: 2026-10-16
**PRD Version Change**: v2.1 to v2.3
**Related Commit(s)**: Pending

> Create this document only for a major requirement event: a new or materially revised FR changes another verified or implemented FR, or an approved restructure substantially changes requirements, ownership, workflow, data, security, or integration contracts. Record small corrections only in the PRD change log and normal update log.

---

## Decision Summary

The MTG-002 quote-model verification found that FR-019 let a patient code write to a provider-owned promotion, allowed the accepted price to change after acceptance (provider remove/replace, code entry at booking, booking revalidation, admin Void), created redemptions with no link to the accepted subquote or AcceptanceEvent, left usage-limit consumption and release undefined, and gave automatic promotions no attachment target. The Product Owner decisions of 2026-10-16 (D8, D9, D10, D11, D12, M14, with D2 and D6) fix promotion terms at send, freeze them at acceptance, and define one usage lifecycle. This Change Request exists because FR-019 was Verified and these decisions change its workflow, data, permission, and integration contracts.

**Status change**: FR-019 moves from ✅ Verified & Approved to 🟡 Revised — Pending Consolidated Verification.

## Baseline State

**Source version**: FR-019 v2.1, `Executive Summary`, `Module Scope`, `Alternative Flows`, Screens 1, 2, 5, 6, 9, 10, 11, `General Module Rules`, `Dependencies`, `Implementation Notes`, User Story 3, `Functional Requirements Summary`, `Key Entities`

- Patients entered codes "at quote/booking"; validation ran at quote review and again at booking confirmation, with "revalidation on booking".
- Providers could remove or replace a discount until the booking was confirmed (Screen 10), and admins could Void an Applied redemption (Screen 6).
- An Application was "applied at checkout / quote" and linked only to the quote and option/date-price row.
- Usage limits were "enforced at validation time"; reservation, consumption, and release were undefined.
- Auto-applied programs had no rule for which rows they attach to or whether they change the provider's price.
- Admin edits to a program value applied to "redemptions from that point forward", including quotes already sent.

## Approved State

**Target version**: FR-019 v2.3, same headings plus Alternative Flows A3, A4, A5, B4, User Story 4, REQ-019-012 to REQ-019-016, and the UsageReservation entity

The updated [FR-019 PRD](./prd.md) states:

- Promotion terms are copied into the sent quote version at send; later program edits, pauses, or expiry do not change a sent row.
- Auto-applied programs attach at send to every eligible option/date-price row; the provider's price stays as entered and the discount is shown separately.
- A patient may enter a code only before acceptance, on one named subquote; it is recorded against the patient's selection and never written to the provider's promotion.
- The Application is created at acceptance, linked to the AcceptanceEvent, the parent quote and version, and the accepted row. Not-accepted rows never create one.
- For provider-selected promotions and patient codes, usage is reserved at acceptance, consumed at the first successful payment, released on `Payment Window Expired` or cancellation, and re-reserved on an FR-006 admin revive, which fails if the limit is exhausted.
- For auto-applied promotions, sending a quote reserves one use, and a sent quote holds at most one reserved use: re-sending a new version keeps it, creates one only if the new version newly qualifies, and releases it if the new version drops the promotion; the reservation is released when the quote expires, is withdrawn, or ends Not Selected or cancelled, and consumed at acceptance. If the booking reaches `Payment Window Expired` or is cancelled before the first payment, the consumed use returns to the limit; an admin revive takes it again if the limit has room, otherwise the revive is rejected (FR-006), so the accepted price never changes. Usage limits count reservations plus consumed uses, so a limit can never be exceeded.
- After acceptance the promotion and price are frozen; there is no removal, replacement, checkout or booking code entry, price-changing revalidation, or admin Void. The only exception is the FR-006 provider-fault transfer, which creates a new linked acceptance record; the original Application is marked Superseded and its use carries over.
- Commission is calculated on the accepted price after the promotion, in the quote currency, from the acceptance snapshot, for every discount type including Hairline-funded programs; a Hairline-funded discount reduces the provider's payout as well as Hairline's commission, and the provider bears most of it.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Patient code entry | At quote or booking, target row undefined | Before acceptance, on one named subquote, never written to the provider promotion | D8, finding FR-019-1 |
| Post-acceptance changes | Provider remove/replace, booking revalidation, booking code entry, admin Void | None; only the provider-fault transfer through a new linked record | D9, D6, findings FR-019-2 (merged FR-019-8, S2-1, FR-017-3) |
| Promotion terms | Live program value | Copied into the sent quote version at send | D10, finding FR-004-5 (merged FR-019-5) |
| Application creation and provenance | Applied at checkout/quote; quote and row IDs | Created at acceptance; linked to AcceptanceEvent, quote version, accepted row | Finding FR-019-3 |
| Usage limit | Enforced at validation time | Reserve at acceptance, consume at first successful payment, release on PWE or cancellation, re-reserve on revive | D11, D2, finding FR-019-4 |
| Automatic promotions | No attachment rule | Attach at send to every eligible row; price unchanged; discount shown separately | M14, finding FR-019-7 |
| Commission base | Not stated; Hairline-only discounts described as leaving providers unaffected | Accepted price after promotion, quote currency, from the snapshot, for every discount type including Hairline-funded programs (REQ-019-016) | D12, Q5 |
| Auto-applied promotion usage | Reserved only at acceptance, like other sources | One use reserved at send, at most one per sent quote across re-sent versions (kept on re-send, created only when newly qualifying, released when dropped); released on expiry, withdrawal, or Not Selected or cancelled outcomes; consumed at acceptance; limits count reservations plus consumed uses (REQ-019-015, UsageReservation) | Q6, Q29, Q30 |
| Fixed-amount currency | No currency | Fixed values carry a currency and are expressed in the quote currency at send; Application records currency | Finding FR-019-6 |
| Admin Void | Manual action on any redemption | Removed; Voided and Superseded set only by the system | D9 |
| Screen 11 | Apply Discount at Quote / Booking | Apply Discount Before Acceptance | D8, D9 |

## Scope and Impact

### In Scope

- FR-019 promotion attachment, patient code entry, freeze, Application provenance, usage lifecycle, and the related screens, rules, scenarios, requirements, and entities.

### Out of Scope

- Payment, refund, fund-release, and later-instalment mechanics, including the money side of the provider-fault transfer (parked for the payment pass under D6-M).
- Settlement of the Hairline/provider funding split (FR-017).
- The "Save as reusable program" toggle on inline promotions (observation only; no change).

### Affected Contracts

- **PRD owner**: [`prd.md`](./prd.md) — Alternative Flows A3, A4, A5, B4; Screens 2, 5, 6, 9, 10, 11; General Module Rules; User Stories 3 and 4; REQ-019-003, REQ-019-007, REQ-019-012 to REQ-019-014; Key Entities (PromotionCode, Application)
- **Related FRs**: FR-004 (copy row promotion terms into the sent quote version; admin promotion edits only before acceptance), FR-005 (Alternative Flow A8 patient code; AcceptanceEvent snapshot carries the discounted price and promotion), FR-006 (PWE and cancellation release; admin revive re-reserves; Alternative Flow B5 provider-fault transfer), FR-007 and FR-007b (first successful payment consumes the use; totals read from the snapshot), FR-015 and FR-029 (commission base after promotion), FR-017 (refund, reversal, and funding-split reconciliation), FR-018 (affiliate attribution unchanged), FR-020 and FR-030 (no new promotion events required by this change)
- **System documents**: `system-data-schema.md` (Application/redemption table with acceptance_event_id, quote_version, source, status values, currency, terms snapshot; row-level promotion terms in the sent quote version), `system-prd.md` (FR-019 summary wording), `system-technical-spec.md` (promotion service hooks at send, acceptance, and first payment)

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed.
- **Required assessment**: Promotion attach-at-send logic, patient code API on subquotes, acceptance transaction (Application creation and usage reservation), payment hook for consumption, PWE/cancellation release, revive re-reservation, removal of provider remove/replace and admin Void actions, redemption table fields.
- **Compatibility / rollout risk**: Existing Applied redemptions created at quote stage have no AcceptanceEvent link and may over-count usage; existing client paths for booking-time code entry must be closed.
- **Data migration**: To be assessed.

## Acceptance and Validation

- No path changes a promotion or price after acceptance except the FR-006 provider-fault transfer (FR-019 Screens 6, 10, 11; Alternative Flow B4; REQ-019-013).
- One rule states the reserve, consume, release, and re-reserve lifecycle (General Module Rules; REQ-019-014).
- Auto-applied promotions reserve at send, release on expiry, withdrawal, or Not Selected or cancelled outcomes, and consume at acceptance; no limit is exceeded when concurrent quotes compete for the last use (REQ-019-015; User Story 4 scenarios 9 and 10); a re-sent version never creates a second reservation for the same quote (User Story 4 scenario 11); a consumed auto-applied use returns to the limit on `Payment Window Expired` or cancellation before the first payment and is re-taken on revive only if room remains (User Story 4 scenario 12).
- No FR-019 text keeps commission on the price before promotion or states that a Hairline-funded discount leaves providers unaffected (REQ-019-016).
- User Story 4 scenarios cover auto-attachment, acceptance-to-Application provenance, rejection on a row the promotion was not attached to, and the usage lifecycle.
- Cross-FR checks against FR-004, FR-005, FR-006, FR-015, FR-029, and the schema pass in consolidated verification.

## Approval and Traceability

- **Requested by**: Product Owner (MTG-002 quote-model verification)
- **Approved by**: Product Owner — documentation approved 2026-10-16 via the decision log; implementation reconciliation required, not assessed
- **Decision evidence**: SRC-MTG-002; `reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md` (D2, D6, D6-M, D8, D9, D10, D11, D12, M14; Q-series Q5, Q6, Q29, Q30); findings FR-019-1, FR-019-2, FR-019-3, FR-019-4, FR-019-6, FR-019-7, FR-019-9
- **PRD change log**: FR-019 v2.2 and v2.3 rows dated 2026-10-16
- **Update log**: `../../update-logs/2026-10-16/MTG002_QUOTE_MODEL_ALIGNMENT_2026-10-16.md`
- **Supersedes**: CR-FR019-20260910-01, in part (redemption provenance and promotion changes after send or acceptance)
- **Superseded by**: None
