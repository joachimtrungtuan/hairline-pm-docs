# Change Request: MTG-002 Quote Model Alignment for Installment Plans

**Change Request ID**: CR-FR007B-20261016-01
**Primary FR**: FR-007B
**Triggering FR / Event**: MTG-002 quote-model verification and Product Owner decision log (2026-10-16)
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-16
**Decision Date**: 2026-10-16
**PRD Version Change**: v1.2 to v1.3
**Related Commit(s)**: Pending

> Create this document only for a major requirement event: a new or materially revised FR changes another verified or implemented FR, or an approved restructure substantially changes requirements, ownership, workflow, data, security, or integration contracts. Record small corrections only in the PRD change log and normal update log.

---

## Decision Summary

The MTG-002 quote-model verification found that FR-007B took the installment plan total from the "accepted quote", carried no currency or exchange-rate snapshot and no promotion basis, let a failed first installment be retried with no link to the FR-006 payment hold, and did not say whether missed later installments could cause `Payment Window Expired`. The Product Owner decisions of 2026-10-16 (M15, D1, D8, with D6, D6-M and M18) make the plan consume the accepted snapshot read-only and limit `Payment Window Expired` to the first payment step. This Change Request exists because FR-007B was Verified and these decisions change its data and integration contracts with FR-005, FR-006, FR-007 and FR-019.

**Status change**: FR-007B moves from ✅ Verified & Approved to 🟡 Revised — Pending Consolidated Verification.

## Baseline State

**Source version**: FR-007B v1.2, `Main Flow`, `Alternative Flows`, Screens 1, 2, 4, 6, `General Module Rules`, `Dependencies`, User Stories 1 and 3, `Edge Cases`, `Functional Requirements Summary`, `Key Entities`

- The plan total "matches accepted quote" and the data source was the "Quote acceptance flow (FR-005)".
- No currency, exchange rate or promotion basis on the plan, its screens or the Installment Plan entity.
- The first installment was charged "upon booking confirmation", and the booking was marked "Confirmed - Installment Plan Active" and later "Fully Paid".
- A failed first installment could be retried with no reference to the FR-006 hold or `Payment Window Expired`.
- No statement on whether missed later installments cause `Payment Window Expired`, and no provider-fault path.
- Admin reschedule "triggers installment plan recalculation" without saying the accepted snapshot is unchanged.

## Approved State

**Target version**: FR-007B v1.3, same headings plus Alternative Flow B4 and REQ-007b-025 to REQ-007b-027

The updated [FR-007B PRD](./prd.md) states:

- Plan total, currency and exchange rate are copied read-only from the FR-005 accepted snapshot through the FR-006 booking. The total already includes the accepted promotion and any patient promotion code. It is never recomputed, and the currency is shown on Screens 1, 2, 4 and 6.
- The first installment is charged at checkout; its success confirms the existing `Accepted` booking and consumes the promotion use reserved at acceptance (FR-019). Booking status follows FR-006 (`Confirmed`); the plan has its own status.
- A failed first installment can be retried only while the original FR-006 hold is active (FR-007 REQ-007-017). When the hold expires the booking moves to `Payment Window Expired`.
- `Payment Window Expired` applies only to the first payment step. Missed later installments never cause it or inquiry cancellation.
- Provider fault after acceptance follows FR-006 Alternative Flow B5 (new Alternative Flow B4): remaining installments are cancelled, paid amounts move as credit toward the replacement booking, any unused part is refunded and the patient pays no fee. Mechanics are deferred.
- Admin reschedule reads the updated booking date and never changes the accepted snapshot.
- The Installment Plan entity carries currency and exchange rate and resolves acceptance provenance through its booking.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Plan total source | "Accepted quote" via FR-005 | Read-only copy from the accepted snapshot through the FR-006 booking; includes accepted promotion and any patient code; never recomputed | M15, D8; findings FR-007b-2 (merged FR-007b-4, S1-7), FR-007b-1 |
| Currency and exchange rate | Absent | Copied read-only from the snapshot; shown on installment screens; on the Installment Plan entity | M15; finding FR-007b-2 |
| First installment and confirmation | Charged "upon booking confirmation" | Charged at checkout; success confirms the `Accepted` booking | Finding FR-007b-5 |
| Booking status labels | "Confirmed - Installment Plan Active", "Fully Paid" on booking | FR-006 `Confirmed`; plan status active or completed | Finding FR-007b-6 |
| First-installment retry | Unbounded | Only within the original FR-006 hold; then `Payment Window Expired` | D1; finding FR-007b-3 |
| Later installments | PWE scope unstated | Never cause `Payment Window Expired` or inquiry cancellation | D1 |
| Provider fault | No path | Alternative Flow B4 to FR-006 B5 with payment placeholder | D6, D6-M, M18 |
| Admin reschedule | Recalculation only | Reads updated booking date; snapshot unchanged | Observation FR-007b-7 |

## Scope and Impact

### In Scope

- FR-007B consumption of the accepted snapshot (total, currency, exchange rate, promotion basis), the first-payment boundary, the provider-fault handoff, and the related screens, rules, scenarios, requirements and entity.

### Out of Scope

- Installment economics, schedule calculation, retry/default handling of later installments, refunds, commission and payout timing (parked for the payment pass), including the "first installment type" FR-029 setting and the payout trigger on "Fully Paid".
- Exact credit, refund, fund-release and override mechanics of the provider-fault transfer (D6-M placeholder only).

### Affected Contracts

- **PRD owner**: [`prd.md`](./prd.md) — Main Flow steps 7, 9, 14; Alternative Flows B1, B3, B4; Screens 1, 2, 4, 6; General Module Rules; Dependencies; User Stories 1 and 3; Edge Cases; REQ-007b-005, REQ-007b-025 to REQ-007b-027; Key Entities (Installment Plan)
- **Related FRs**: FR-005 (AcceptanceEvent snapshot is the source), FR-006 (hold, `Payment Window Expired` first-payment boundary REQ-006-016, Alternative Flow B5, booking status enum), FR-007 (REQ-007-016 to REQ-007-019 accepted-selection contract and hold check), FR-019 (promotion use consumed at first successful payment), FR-017 (provider-fault money mechanics, later), FR-029 (installment configuration unchanged)
- **System documents**: `system-data-schema.md` (installment plan currency and exchange-rate columns copied from the acceptance snapshot), `system-prd.md` (FR-007B summary wording), `system-technical-spec.md` (installment checkout hold check and snapshot read)

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed.
- **Required assessment**: Source of the plan total, currency and exchange rate at plan creation; hold check on first-installment retry; booking status values written by the installment flow; cancellation of remaining installments on provider-fault transfer.
- **Compatibility / rollout risk**: Existing plans may hold totals or currencies read from a live quote; later installments may be converted at current rates.
- **Data migration**: To be assessed.

## Acceptance and Validation

- No plan amount is read from a live quote, sibling option or library price (General Module Rules; Screen 1; Data Dependencies; REQ-007b-025).
- The first-payment boundary is stated and referenced to FR-006 (General Module Rules; Alternative Flow B1 boundary; Edge Cases; REQ-007b-026).
- User Story 1 scenarios 4 to 6 and User Story 3 scenario 4 cover the snapshot total, fixed currency, rejected retry after hold expiry, and no PWE on later default.
- Cross-FR checks against FR-005, FR-006, FR-007, FR-019 and the schema pass in consolidated verification.

## Approval and Traceability

- **Requested by**: Product Owner (MTG-002 quote-model verification)
- **Approved by**: Product Owner — documentation approved 2026-10-16 via the decision log; implementation reconciliation required, not assessed
- **Decision evidence**: SRC-MTG-002; `reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md` (M15, D1, D6, D6-M, D8, M18); findings FR-007b-1, FR-007b-2, FR-007b-3, FR-007b-5, FR-007b-6, FR-007b-7
- **PRD change log**: FR-007B v1.3 row dated 2026-10-16
- **Update log**: `../../update-logs/2026-10-16/MTG002_QUOTE_MODEL_ALIGNMENT_2026-10-16.md`
- **Supersedes**: None
- **Superseded by**: None
