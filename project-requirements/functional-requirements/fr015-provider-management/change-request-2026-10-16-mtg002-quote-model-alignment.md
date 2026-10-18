# Change Request: MTG-002 Quote Model Alignment for Provider Management

**Change Request ID**: CR-FR015-20261016-01
**Primary FR**: FR-015
**Triggering FR / Event**: SRC-MTG-002 quote model verification and Product Owner decision log (2026-10-16)
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-16
**Decision Date**: 2026-10-16
**PRD Version Change**: v1.16 to v1.20 (v1.17 MTG-002 alignment; v1.18 Product Owner follow-up decision; v1.19 consolidated verification corrections; v1.20 final audit corrections)
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

**Target version**: FR-015 v1.20 (same headings; adds REQ-015-029)

- Commission Rule 2 uses the booking total, defined as the accepted price after promotion, in the quote currency, read from the FR-005 acceptance snapshot, multiplied by the rate fixed at booking confirmation.
- The same commission base applies to every discount type, including discounts funded only by Hairline.
- Before acceptance, the cascade cancels the provider's unaccepted Parent Quotes once each with FR-004 `cancelled_provider_status`.
- After acceptance, every non-terminal booking of the provider before treatment starts is closed through FR-006 Alternative Flow B4 and handed to the FR-006 Alternative Flow B5 provider-fault transfer. The accepted Parent Quote keeps `accepted`; the AcceptanceEvent is superseded through a linked FR-005 supersession record; the inquiry stays open; an admin assigns a replacement provider in the same inquiry; money follows the B5 payment placeholder. The admin starts the transfer from Start Provider-Fault Transfer on FR-006 Screen 6 (Screen 10) and authors the replacement quote (Q35).
- `Aftercare` bookings and FR-011 standalone aftercare cases assigned to the provider are not closed. They keep their status and treatment record, get the provider-status cause and support marker, and move to admin aftercare reassignment through FR-006 Alternative Flow B6 and the FR-011 aftercare reassignment screen, with no new acceptance and no new payment (Q36).
- `In Progress` bookings are not closed. They stay `In Progress` with the provider-status cause and `supportRequired`, and an admin decides case by case on FR-006 Screen 6 to move the booking to `Aftercare` with aftercare reassignment or to cancel it with a mandatory reason; there is no replacement acceptance.
- When an admin reassigns aftercare, FR-011 sends the mandatory `aftercare.provider_reassigned` notice to the patient and the new aftercare provider.
- Screen 4 links each affected record to the admin screen that resolves it (provider-fault transfer, aftercare reassignment, or the FR-016 Admin Support Required view), each with a mandatory reason, confirmation, and audit entry (Q43; REQ-015-029).
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
| Aftercare-stage cases (A5, Screen 4, Rules 9 and 10, dependencies, Assumption 4, US3, edge cases, REQ-015-017) | Aftercare bookings and FR-011 standalone aftercare cases closed or cancelled and sent to the B5 transfer | Not closed; keep status, get cause and support marker, and move to admin aftercare reassignment (FR-006 B6, FR-011) with no new acceptance or payment | Q36; final audit lifecycle finding F7 |
| A5 step 7 transfer entry point | Admin assigns a replacement provider through B5 | Admin opens Start Provider-Fault Transfer on FR-006 Screen 6 (Screen 10) and authors a replacement quote | Q35 |
| Screen 4 admin action links (new rule, REQ-015-029) | Affected records listed with links only | Each affected record links to its resolving admin screen with mandatory reason, confirmation, and audit | Q43 |
| Discount types (Commission Rule 2) | Base stated as price after promotion without naming discount types | Same base for every discount type, including Hairline-funded discounts | Q5 |
| In Progress bookings (A5 steps 3 to 5 and 7, Outcome, Deactivation, Screen 4, Rule 10, FR-010/FR-011 dependency, Assumption 4, REQ-015-017, scenarios) | In Progress bookings closed with the provider-status cause like bookings before treatment | Not closed; they stay `In Progress` with the cause and `supportRequired`, and an admin decides on FR-006 Screen 6 to move the booking to Aftercare with aftercare reassignment or cancel it with a reason; no replacement acceptance | Q45 |
| Aftercare reassignment patient notice (A5 step 5) | Deferred to FR-011 without naming an event | Named as the mandatory FR-011 event `aftercare.provider_reassigned` to the patient and the new aftercare provider | Q47 |

## Scope and Impact

### In Scope

- Commission base wording and lock point reference in FR-015.
- Provider-status cascade split between unaccepted quotes and accepted bookings, and the hand-off to FR-006.
- Patient notice content for closed accepted bookings.
- Aftercare-stage routing to aftercare reassignment and Screen 4 admin action links.

### Out of Scope

- Refund, fund-release, payment-allocation override, and later-instalment mechanics (payment pass; D6-M placeholder only).
- Flat Rate model and payout frequency behaviour.
- Notification catalogue entries themselves (owned by FR-030 and FR-020).

### Affected Contracts

- **PRD owner**: `fr015-provider-management/prd.md` — Alternative Flow A5, Screen 4, Rules 9 and 10, Payment & Billing Rules, Internal Dependencies, User Story 3, Edge Cases, REQ-015-017 to REQ-015-019, REQ-015-029, Assumption 4, Key Entities
- **Related FRs**: FR-003 (inquiry stays open after a provider-status closure of an accepted booking); FR-004 (`cancelled_provider_status` for unaccepted quotes only); FR-005 (supersession record with cause `ProviderSuspended` or `ProviderDeactivated`); FR-006 (Alternative Flows B4, B5, and B6; Screens 6 and 10); FR-011 (aftercare reassignment screen); FR-007, FR-007B, FR-017 (payment placeholder mechanics); FR-029 (commission base sentence and lock points); FR-020 and FR-030 (patient "admin will arrange a replacement provider" notice); FR-016 (support marker on open inquiries)
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
- Suspending a provider with an Aftercare booking keeps the booking in `Aftercare` with the cause and support marker, creates no new acceptance or payment, and lets an admin reassign aftercare through the FR-011 screen.
- Suspending a provider with an In Progress booking keeps it `In Progress` with the cause and support marker, closes nothing, and leaves the admin to move it to Aftercare with reassignment or cancel it (REQ-015-017).
- FR-015 names `aftercare.provider_reassigned` as the patient notice for an aftercare reassignment.
- Every affected record on Screen 4 links to its resolving admin screen, and each resolution records a reason, confirmation, and audit entry.

## Approval and Traceability

- **Requested by**: Product Owner (MTG-002 quote model audit)
- **Approved by**: Product Owner, 2026-10-16, via `reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md` (documentation only)
- **Decision evidence**: SRC-MTG-002; decision log 2026-10-16 (D6, D6-M, D12, M5, M18, P1); findings FR-015-1 to FR-015-4, FR-015-6; Product Owner follow-up decisions Q5, Q35, Q36, Q43, Q45, and Q47 (decided 2026-10-18); final audit lifecycle finding F7 and doc-control finding F2
- **Implementation reconciliation**: Required, not assessed
- **PRD change log**: v1.17 and v1.18 (2026-10-16); v1.19 and v1.20 (2026-10-18)
- **Update log**: Combined 2026-10-16 MTG-002 log (controller-owned)
- **Supersedes**: CR-FR015-20261013-01 in part (inquiry cancellation and accepted-quote cancellation after acceptance)
- **Superseded by**: None
