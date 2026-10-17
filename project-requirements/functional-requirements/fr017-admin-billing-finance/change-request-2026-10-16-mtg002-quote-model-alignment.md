# Change Request: MTG-002 Quote Model Alignment (Billing Consumption)

**Change Request ID**: CR-FR017-20261016-01
**Primary FR**: FR-017
**Triggering FR / Event**: MTG-002 quote model audit and Product Owner decision log (2026-10-16); FR-005 v2.5, FR-006 v2.7 and FR-019 v2.2 acceptance-snapshot changes
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-16
**Decision Date**: 2026-10-16
**PRD Version Change**: v2.10 to v2.12
**Related Commit(s)**: Pending

> Created under plan decision P1: FR-017 implementation status is unknown, so this alignment is recorded as a Change Request to be safe.

---

## Decision Summary

The MTG-002 quote model makes the FR-005 acceptance snapshot the single money source after acceptance. FR-017 must consume it and nothing else: price, currency, locked exchange rate (with its timestamp) and promotion are read from the snapshot, never from the live quote, library or promotion settings. The Product Owner decided that a stale cached rate never pauses acceptance (D19), that promotions are frozen at acceptance and can no longer be entered at checkout (D8, D9, D11), and that commission uses the accepted price after promotion with named lock points (D12, M5). Provider suspension after acceptance now uses the FR-006 provider-fault transfer (M18, D6, D6-M).

## Baseline State

**Source version**: FR-017 v2.10 — Edge Cases, Payment & Billing Rules, General Module Rules (Rules 4, 12, 13), Screens 3, 4a, 8, 10, Data Dependencies (Entity 4), Key Entities 1, 4, 7, REQ-017-004 and REQ-017-014

- An edge case flagged the acceptance handoff for admin manual review when the cached rate was more than 24 hours old, a state FR-005 does not have.
- Patients applied discount codes at checkout; invoices used "recorded FR-019 applications" alongside a separately retained attached promotion, with no rule that the promotion is frozen at acceptance.
- Commission Rule 1 cited a "confirmation-time snapshot" with no stated base currency, and the Percentage calculation was applied after currency conversion.
- The rate lock was described as "booking acceptance" or "booking time"; Entity 7 kept an independent lock record with no AcceptanceEvent link.
- Currency alert workflow invited renegotiating "booking terms".
- Rule 13 said no rebooking is issued automatically after provider suspension or deactivation.

## Approved State

**Target version**: [FR-017 v2.12](prd.md) — same headings, plus REQ-017-030

- No acceptance-time manual review; FR-017 consumes the snapshot rate and timestamp and never fetches or relocks a rate. Stale-cache alerts are operational only.
- Invoice total, currency, locked rate and promotion come from the acceptance snapshot. The FR-019 application record is linked to the AcceptanceEvent and is provenance only. No promotion entry, removal, replacement or recalculation after acceptance; the only exception is the FR-006 provider-fault transfer's new linked acceptance record.
- Percentage commission base is the accepted price after promotion, in the quote currency, from the snapshot; exchange rate locked at subquote acceptance; commission model and value, with deposit and instalment settings, fixed at booking confirmation; nothing fixed at quote creation (REQ-017-030).
- The same commission base applies to every discount type, including Hairline Only discounts, so the provider bears part of such a discount.
- Rate-lock wording names subquote acceptance (FR-005 AcceptanceEvent); Entity 7 is a read-only projection with `acceptance_event_id` and the rate timestamp.
- Any change agreed with providers after a currency alert is a separate finance adjustment; the snapshot and AcceptanceEvent stay unchanged.
- Suspension or deactivation after acceptance: admin rehomes the patient through the FR-006 provider-fault transfer; paid money moves with the patient as credit, unused part refunded, no patient fee (placeholder only).

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Acceptance-time FX (Edge Cases, Integration 2) | Manual review if cached rate over 24 hours old | Acceptance proceeds on cached rate; snapshot records rate and timestamp; alert only | FR-017-1, D19 |
| Invoice amounts (Screen 4a, Rule 12, REQ-017-004, Entities 1 and 4) | Recorded FR-019 checkout applications plus attached promotion | Price, currency, rate and promotion from the acceptance snapshot; FR-019 application linked to the AcceptanceEvent; never recalculated | FR-019-2 (incl. FR-017-3), D8, D9, D11 |
| Checkout code entry (Multi-Tenant, Edge Cases, User Story 3) | Codes applied at checkout | Codes only before acceptance on one named subquote | D8, D9 |
| Commission (Screen 3, Commission Rule 1, REQ-017-030) | Confirmation-time snapshot; Percentage after conversion | Base is accepted price after promotion in quote currency; named lock points | S2-4 (incl. FR-017-2), D12, M5 |
| Rate-lock wording and Entity 7 | "Booking acceptance" or "booking time"; independent lock record | Subquote acceptance; read-only snapshot projection with acceptance_event_id | FR-017-4, FR-017-6 |
| Currency alert (Workflow B2, Screen 8) | Renegotiate booking terms | Separate finance adjustment; snapshot unchanged; config changes never alter confirmed bookings | FR-017-5, M5 |
| Provider suspension after acceptance (Rule 13, Edge Cases) | No automatic rebooking | FR-006 provider-fault transfer with placeholder money principle | M18, D6, D6-M |
| Discount types (Screen 5, Commission Rule 1, REQ-017-030) | Provider Cost shown only for Both Fees discounts | Commission on the price after promotion for every discount type; providers bear part of Hairline Only discounts too | Q5 |

## Scope and Impact

### In Scope

- How FR-017 reads price, currency, locked rate and promotion from the acceptance snapshot, and the commission base and lock points.

### Out of Scope

- Refunds, reversal mechanics, provider-fault payment reallocation, funding-split settlement, payouts and fund release (later payment pass). Reverse/Refund of completed promotion redemptions and FR-019 funding-split settlement are referenced only.
- Invoice handling of a capture after `Payment Window Expired` (observation FR-017-7, parked for the payment pass).

### Affected Contracts

- **PRD owner**: `prd.md` — Edge Cases, Payment & Billing Rules, General Module Rules 4, 12, 13, Screens 3, 4a, 6, 8, 10, Entities 1, 4, 7, REQ-017-004, REQ-017-014, REQ-017-030
- **Related FRs**: FR-005 (acceptance snapshot incl. rate timestamp and promotion), FR-006 (booking confirmation lock point, provider-fault transfer B5), FR-019 (application record linked to AcceptanceEvent; reservation and consumption), FR-015 and FR-029 (commission base and lock points), FR-007 / FR-007b (payment amounts from the snapshot)
- **System documents**: `system-prd.md`, `system-data-schema.md` (acceptance snapshot rate timestamp, promotion application `acceptance_event_id`, rate-lock projection), `system-technical-spec.md`

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed
- **Required assessment**: Invoice amount and promotion source, removal of any checkout code entry, commission base and currency, rate-lock storage and acceptance link, any manual-review state on acceptance
- **Compatibility / rollout risk**: Existing invoices built from live or checkout data may differ from the snapshot; compare before switching sources
- **Data migration**: To be assessed

## Acceptance and Validation

- No FR-017 text describes a manual-review or pending acceptance state for a stale rate.
- Invoice total, currency, rate and promotion are read from the acceptance snapshot; no FR-017 text allows a promotion change at checkout or after acceptance.
- Commission base and lock points match FR-006, FR-015, FR-029 and the schema (one base sentence).
- Commission Rule 1, REQ-017-030 and Screen 5 Provider Cost apply the price after promotion to every discount type, including Hairline Only discounts.
- Implementation evidence for the above before reconciliation is marked Verified.

## Approval and Traceability

- **Requested by**: Product Owner (MTG-002 quote model audit)
- **Approved by**: Product Owner, 2026-10-16, via `reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md` (documentation only)
- **Decision evidence**: SRC-MTG-002; decision log 2026-10-16 (D6, D6-M, D8, D9, D11, D12, D19, M5, M18, P1); findings FR-017-1, FR-019-2, S2-4, FR-017-4, FR-017-5, FR-017-6; Product Owner follow-up decision Q5
- **PRD change log**: v2.11 and v2.12 rows
- **Update log**: Combined 2026-10-16 MTG-002 log (controller-owned)
- **Supersedes**: None (CR-FR017-20261015-01 remains in force, except that Rule 13 now adds the provider-fault rehoming after acceptance)
- **Superseded by**: None
