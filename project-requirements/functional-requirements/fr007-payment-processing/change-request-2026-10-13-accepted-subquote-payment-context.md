# Change Request: Accepted Subquote Payment Context

**Change Request ID**: CR-FR007-20261013-01
**Primary FR**: FR-007
**Triggering FR / Event**: Approved Meeting 02 quote restructure and FR-004/FR-005/FR-006 accepted-subquote handoff
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-13
**Decision Date**: 2026-10-13
**PRD Version Change**: v1.5 to v1.6
**Related Commit(s)**: Pending — no commit requested for this step

---

## Decision Summary

FR-007 consumes one accepted subquote through the FR-006 Booking and immutable FR-005 AcceptanceEvent, not an ambiguous parent quote or all its alternatives. This changes the previously verified payment-screen source and initial-payment eligibility contracts. Documentation approval does not prove implementation reconciliation.

## Baseline State

**Source version**: FR-007 v1.5 — Main Flow, Screen Specifications, Payment & Billing Rules, and Key Entities.

The PRD was marked Verified & Approved. Checkout allowed currency selection; provider/admin financial tables read pricing and multiple packages generically “from quote.” It linked payment to booking but did not specify accepted subquote/aggregate-version provenance or the exclusive acceptance hold. Implementation was not inspected in this step.

## Approved State

**Target version**: [FR-007 v1.6](./prd.md) — Main Flow, Shared Accepted-Selection Source Contract, and REQ-007-016 through REQ-007-019.

The booking resolves one package option plus one applicable option/date-price record and inherited parent context. Commercial facts remain in the accepted snapshot; existing FR-019 patient-code applications and authorized interventions remain separate auditable records. Initial charge validates the original FR-006 hold; subsequent payments use the confirmed booking without acquiring a new acceptance hold.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Payment target | Generic quote/booking, potentially ambiguous with multiple options | One FR-006 Booking resolves one AcceptanceEvent and accepted subquote/parent aggregate revision | Only the bottom-level complete commercial choice is accepted |
| Package and price displays | Packages/price read generically from quote | Accepted package/services and selected option/date price; optional itemization cannot be added again or sourced from the current library | Preserve quote-local customization and prevent sibling-price fan-out |
| Currency | Selectable at deposit/final checkout | Read-only accepted currency/exchange-rate snapshot | Payment must retain the accepted pricing context |
| Initial payment | Deposit confirmation without explicit accepted-hold guard | Validate inquiry/selection eligibility, accepted versions, and exclusive unexpired hold before processor submission; successful deposit/eligible first installment/full payment confirms the same booking | Preserve FR-005/FR-006 acceptance-to-payment contract |
| Failure and expiry | Generic retry/unconfirmed outcome | Retry uses the original snapshot/deadline; terminal Payment Window Expired blocks that handoff without reopening quotes | Released slots cannot remain payable through stale acceptance |
| Discounts | Generic quote discount displays | Accepted attached-promotion provenance plus separately recorded FR-019 applications; existing single-discount/replacement/attribution rules unchanged | Preserve both immutable acceptance and the existing checkout-code workflow |
| Financial history | Booking references without explicit accepted provenance | Receipt/invoice/payment/refund records resolve acceptance provenance through Booking | Disputes and historical billing must identify the actual accepted choice |

## Scope and Impact

### In Scope

- FR-007 checkout, provider/admin financial-detail and refund commercial context, currency display, accepted identifiers, initial-payment guards, requirements, and regression scenarios.
- FR-017's existing one-invoice-per-booking model is checked and clarified to consume the same recorded terms; its small clarification is recorded in its PRD change log and the normal update log, not a separate major-event Change Request.
- Meeting source incorporation/traceability and required update-log registration.

### Out of Scope

- Meeting 01, Meeting 03, the fund-release brief, and remaining Meeting 02 payment/payout/cancellation-economics questions.
- New deposit rates, commission models/values, installment eligibility/schedules, refund percentages, payout rails/timing, charges/fees, or promotion policies.
- Provider suspension/cancellation/admin-support dependency follow-ups.
- Implementation edits, API/schema migration work, consolidated FR verification, and commits/pushes.

### Affected Contracts

- **PRD owner**: [FR-007](./prd.md#functional-requirements-summary) — REQ-007-001/005 and new REQ-007-016–019; Screens 1–4, 5B, and 6; Booking/AcceptanceEvent provenance.
- **Related FRs**: [FR-004](../fr004-quote-submission/prd.md#quote-hierarchy) quote structure; [FR-005](../fr005-quote-comparison-acceptance/prd.md#key-entities) acceptance snapshot; [FR-006](../fr006-booking-scheduling/prd.md#key-entities) booking/hold; [FR-019](../fr019-promotions-discounts/prd.md#patient-platform-screens-p-03-overlay) existing patient-code application; [FR-017](../fr017-admin-billing-finance/prd.md#key-entities) financial consumption. No changes to these related quote/promotion owners in this step.
- **System documents**: No edits in this step. Consolidated system/schema/technical alignment remains a separate verification/reconciliation activity.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed; source code and runtime were not inspected or modified.
- **Required assessment**: Payment amount/currency inputs; booking-to-acceptance linkage; processor initiation and retry/callback guards; UI summaries; receipts/invoices/refund detail; existing FR-019 applications; historical-data compatibility; regression tests.
- **Compatibility / rollout risk**: Legacy records may lack accepted subquote/version provenance. Preserve their original financial history; do not fabricate a choice from current quotes/library data. Assess transition handling before rollout. Invalid/expired handoffs and late callbacks must not bypass FR-006 confirmation rules; financial reconciliation follows the existing owners, without introducing automatic refunds here.
- **Data migration**: To be assessed by implementation reconciliation; no migration performed or implied by this document.

## Acceptance and Validation

- Across multiple providers/parents/options/dates, checkout displays and pays only the accepted subquote's recorded commercial choice; library changes and sibling prices do not affect it.
- Optional components are informational; the complete offered price is not double-counted. FR-019's permitted patient-code behavior remains available and separately audited, including single-discount replacement and attribution.
- Initial payment rejects ineligible/mismatched/expired handoffs before processor submission; retry cannot restart the original hold or reopen quotes.
- Initial successful charge confirms the same booking exactly once; later payments retain its accepted context/currency and use its recorded balance without a new acceptance hold.
- FR-017 retains one invoice record per booking, updated for later payments; acceptance alone/unaccepted alternatives generate no invoice or revenue.
- Scoped document link/table/requirement and delta checks are recorded in the update log. Processor/runtime/regression proof and consolidated verification are still required before implementation reconciliation can be marked Verified.

## Approval and Traceability

- **Requested by**: Product Owner, Joachim Trung Tuan.
- **Approved by**: Product Owner, Joachim Trung Tuan, on 2026-10-13; documentation delta only.
- **Decision evidence**: [SRC-MTG-002 D03–D05](../../sources/meetings/meeting-02-launch-quote-options-fund-release-and-payments.md#mtg-002-d03-one-response-with-multiple-quote-options) and [O01 Product Owner clarifications](../../sources/meetings/meeting-02-launch-quote-options-fund-release-and-payments.md#mtg-002-o01-quote-option-contract). In this chat the Product Owner requested “Please help me make all those pending works” after the remaining scope was stated as FR-007 update and conditional FR-017 consistency alignment. Existing discount behavior is owned by FR-019, not a new Meeting 02 decision.
- **PRD change log**: [FR-007 v1.6](./prd.md#appendix-change-log).
- **Update log**: [FR007 accepted subquote payment and FR017 billing alignment](../../update-logs/2026-10-13/FR007_ACCEPTED_SUBQUOTE_PAYMENT_BILLING_ALIGNMENT_2026-10-13.md).
- **Supersedes**: None; completes the downstream payment consumer alignment without superseding the approved FR-004/005/006 model.
- **Superseded by**: None.
