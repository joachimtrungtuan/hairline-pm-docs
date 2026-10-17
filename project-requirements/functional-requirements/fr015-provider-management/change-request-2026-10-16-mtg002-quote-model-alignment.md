# Change Request: MTG-002 Quote Model Alignment for Provider Management

**Change Request ID**: CR-FR015-20261016-01
**Primary FR**: FR-015
**Triggering FR / Event**: SRC-MTG-002 quote model verification and Product Owner decision log (2026-10-16)
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-16
**Decision Date**: 2026-10-16
**PRD Version Change**: v1.16 to v1.18
**Related Commit(s)**: Pending

> Created under plan decision P1: FR-015's implementation status is unknown, so a Change Request is recorded to be safe. The change also alters workflow, data, and integration contracts shared with FR-003, FR-004, FR-005, and FR-006.

---

## Decision Summary

MTG-002 fixed the quote model, the commission base, and how a provider failure after acceptance is handled. FR-015 must follow these decisions:

- The Percentage commission base is the accepted price after promotion, in the quote currency, read from the FR-005 acceptance snapshot (D12). Commission settings still lock at booking confirmation (M5).
- Provider suspension or deactivation that takes effect after acceptance no longer ends the patient's journey. The booking is closed and handed to the FR-006 provider-fault transfer: the hold is released, the AcceptanceEvent is kept and superseded through a linked FR-005 record with cause `ProviderSuspended` or `ProviderDeactivated`, and an admin rehomes the patient to a replacement provider in the same inquiry. Money follows the D6-M placeholder and is detailed in the payment pass (M18, D6, D6-M).
- Before acceptance, behaviour is unchanged: FR-004 cancels that provider's unaccepted quotes with `cancelled_provider_status`.

## Baseline State

**Source version**: FR-015 v1.16 (Alternative Flow A5, Screen 4, Business Rules, Dependencies, User Story 3, Edge Cases, REQ-015-017 to REQ-015-019, Key Entities)

- Commission Rule 2 computed the Percentage commission as `Transaction Amount * (Commission Rate / 100)` without naming the base.
- The A5/Screen 4 cascade cancelled the accepted Parent Quote/Subquote of each cancelled case and cancelled the inquiry whose accepted treatment belonged to the provider (REQ-015-018).
- Rebooking and refunds were left to "existing admin workflows rather than automatic reselection"; the A5 boundary said the cascade does not issue refunds or select another provider.
- Key Entities implied the confirmation-time commission configuration could sit on the AcceptanceEvent.

## Approved State

**Target version**: FR-015 v1.18 (same headings)

- Commission Rule 2 uses the booking total, defined as the accepted price after promotion, in the quote currency, read from the FR-005 acceptance snapshot, multiplied by the rate fixed at booking confirmation.
- The same commission base applies to every discount type, including discounts funded only by Hairline.
- Before acceptance, the cascade cancels the provider's unaccepted Parent Quotes once each with FR-004 `cancelled_provider_status`.
- After acceptance, every non-terminal booking of the provider is closed through FR-006 Alternative Flow B4 and handed to the FR-006 Alternative Flow B5 provider-fault transfer. The accepted Parent Quote keeps `accepted`; the AcceptanceEvent is superseded through a linked FR-005 supersession record; the inquiry stays open; an admin assigns a replacement provider in the same inquiry; money follows the B5 payment placeholder.
- The patient with a closed accepted booking is told that an admin will arrange a replacement provider within the same inquiry through the mandatory FR-020/FR-030 event `booking.provider_fault_replacement`. `provider.status_cancellation_patient` applies only before acceptance.
- The AcceptanceEvent keeps accepted IDs, versions, and snapshot; the confirmed Booking/financial record keeps the confirmation-time commission configuration.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Commission Rule 2 | `Transaction Amount * rate` | Booking total (accepted price after promotion, quote currency, from the acceptance snapshot) times the rate fixed at confirmation | D12, M5; finding FR-015-1 |
| A5 step 3 and Screen 4 cascade | Cancel non-terminal cases, unaccepted quotes, and the accepted Parent Quote/Subquote | Cancel unaccepted quotes (`cancelled_provider_status`); close bookings via FR-006 B4 and hand them to the B5 transfer; accepted parent keeps `accepted` | M18; finding FR-015-3 |
| Inquiry handling (A5 step 4, FR-003 dependency, REQ-015-018, Key Entities) | Inquiry with this provider's accepted treatment is cancelled | Inquiry stays open for the admin replacement-provider transfer | M18, D6 |
| Rebooking and money (A5 step 7, boundary, Cancellation Billing Rule, deactivation edge case) | Rebooking/refunds via existing admin workflows; no automatic refund or reselection | Admin rehomes the patient through FR-006 B5; paid amounts move as credit, unused part refunded, no patient fee; exact mechanics in the payment FRs | M18, D6-M; finding FR-015-4 |
| Patient communication (A5 step 5, Screen 4, REQ-015-019, US3) | Cancellation message with Contact Admin/Support | Adds the `booking.provider_fault_replacement` "admin will arrange a replacement provider" notice for closed accepted bookings | M18 |
| Rules 9 and 10 | Revalidation and cascade ownership only | Before/after-acceptance split; FR-006 B5 owns the replacement transfer | M18 |
| Key Entities lifecycle context | AcceptanceEvent/Booking hold accepted context and commission configuration | AcceptanceEvent holds accepted context only; confirmed booking/financial record holds commission configuration | Finding FR-015-2 |
| A5 step 1, Screen 4 | `Accepted` stage wording | Named as an FR-006 booking stage | Finding FR-015-6 |
| Discount types (Commission Rule 2) | Base stated as price after promotion without naming discount types | Same base for every discount type, including Hairline-funded discounts | Q5 |

## Scope and Impact

### In Scope

- Commission base wording and lock point reference in FR-015.
- Provider-status cascade split between unaccepted quotes and accepted bookings, and the hand-off to FR-006.
- Patient notice content for closed accepted bookings.

### Out of Scope

- Refund, fund-release, payment-allocation override, and later-instalment mechanics (payment pass; D6-M placeholder only).
- Flat Rate model and payout frequency behaviour.
- Notification catalogue entries themselves (owned by FR-030 and FR-020).

### Affected Contracts

- **PRD owner**: `fr015-provider-management/prd.md` — Alternative Flow A5, Screen 4, Rules 9 and 10, Payment & Billing Rules, Internal Dependencies, User Story 3, Edge Cases, REQ-015-017 to REQ-015-019, Key Entities
- **Related FRs**: FR-003 (inquiry stays open after a provider-status closure of an accepted booking); FR-004 (`cancelled_provider_status` for unaccepted quotes only); FR-005 (supersession record with cause `ProviderSuspended` or `ProviderDeactivated`); FR-006 (Alternative Flows B4 and B5); FR-007, FR-007B, FR-017 (payment placeholder mechanics); FR-029 (commission base sentence and lock points); FR-020 and FR-030 (patient "admin will arrange a replacement provider" notice); FR-016 (support marker on open inquiries)
- **System documents**: `system-prd.md`, `system-data-schema.md` (supersession cause list, commission base), `system-technical-spec.md`

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed
- **Required assessment**: Provider-status cascade service, quote status transitions, booking cancellation causes, supersession records, inquiry status handling, commission calculation base, patient notifications
- **Compatibility / rollout risk**: Any implemented cascade that cancels the inquiry or moves an accepted quote to a cancelled status must change before release
- **Data migration**: To be assessed

## Acceptance and Validation

- Suspending a provider with an accepted booking closes the booking with `ProviderSuspended`, keeps the parent quote `accepted`, supersedes the AcceptanceEvent through a linked record, keeps the inquiry open, and lets an admin assign a replacement provider in the same inquiry.
- Suspending a provider before acceptance cancels only that provider's unaccepted quotes with `cancelled_provider_status`.
- Percentage commission equals the accepted price after promotion, in the quote currency, times the rate fixed at booking confirmation.
- Commission Rule 2 applies the price after promotion to every discount type, including Hairline-funded discounts.
- FR-015, FR-017, FR-029, and the schema state the same commission base and lock points; FR-004, FR-005, FR-006, and FR-015 describe the same provider-fault transfer.

## Approval and Traceability

- **Requested by**: Product Owner (MTG-002 quote model audit)
- **Approved by**: Product Owner, 2026-10-16, via `reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md` (documentation only)
- **Decision evidence**: SRC-MTG-002; decision log 2026-10-16 (D6, D6-M, D12, M5, M18, P1); findings FR-015-1 to FR-015-4, FR-015-6; Product Owner follow-up decision Q5
- **Implementation reconciliation**: Required, not assessed
- **PRD change log**: v1.17 and v1.18 (2026-10-16)
- **Update log**: Combined 2026-10-16 MTG-002 log (controller-owned)
- **Supersedes**: CR-FR015-20261013-01 in part (inquiry cancellation and accepted-quote cancellation after acceptance)
- **Superseded by**: None
