# Change Request: MTG-002 Quote Model Alignment for Booking and Scheduling

**Change Request ID**: CR-FR006-20261016-01
**Primary FR**: FR-006
**Triggering FR / Event**: SRC-MTG-002 quote model verification and Product Owner decision log (2026-10-16)
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-16
**Decision Date**: 2026-10-16
**PRD Version Change**: v2.6 to v2.8
**Related Commit(s)**: Pending

---

## Decision Summary

The MTG-002 quote model audit found that FR-006 contradicted itself on when the slot hold starts and whether payment failure extends it, gave no workable recovery route after `Payment Window Expired`, allowed unrestricted admin status and date edits, and had no flow for provider fault after acceptance. The Product Owner approved decisions D1, D2, D3, D6, D6-M, D11, D12, D13, D14, D22, D23, M3, M4, M5, M13, M17 and M18. This request records the resulting changes to the FR-006 booking contract.

## Baseline State

**Source version**: FR-006 v2.6, `Business Workflows`, `Business Rules`, `Functional Requirements Summary`, `Key Entities`

FR-006 held the slot for 48 hours "after payment failure" through its own A-09 setting while also saying the hold starts at acceptance. The slot was not keyed explicitly, and it was unclear when the appointment record existed. `Payment Window Expired` was terminal, with recovery by "a new current subquote or an audited admin intervention", which FR-005 Rule 1 made impossible. Admin "Modify Status" and "Modify Appointment Date" were available "Always". Provider cancellation meant a full refund with no transfer path. The assumptions said discounts and commissions were "already resolved before booking stage".

## Approved State

**Target version**: FR-006 v2.8, same headings, plus `Alternative Flows` B5 and `Admin Status and Date Intervention Rules`

- One fixed hold starts at subquote acceptance and lasts the FR-026 slot-hold duration (default 48 hours). Payment failure never extends or restarts it (M3, D14).
- The hold is a temporary exclusive hold keyed by provider, appointment date/time and time zone. The appointment record is created only on successful payment. On expiry the hold is released and no appointment exists (M4).
- `Payment Window Expired` applies only to the first payment step. Missed later instalments never cause it or inquiry cancellation (D1).
- Recovery after `Payment Window Expired`: the patient cancels the inquiry and starts a new one, or contacts support for the admin revive (D1).
- Admin revive moves a `Payment Window Expired` booking back to `Accepted` with a mandatory reason, a slot re-check, a new hold, promotion usage re-reservation (rejected if exhausted), an audit entry, an unchanged AcceptanceEvent and a mandatory "booking revived" notice. Date changes need a slot check. No other manual status jumps (D2, D11, M17).
- New Alternative Flow B5: provider fault after acceptance cancels the booking with cause `ProviderFault`, releases the hold, supersedes the AcceptanceEvent through a linked record, and lets an admin transfer the patient in the same inquiry through a new admin-authored linked acceptance record. Payment mechanics are a placeholder only (D3, D6, D6-M).
- Provider suspension or deactivation after acceptance (B4) closes the booking with the provider-status cause, releases the hold, supersedes the AcceptanceEvent through a linked record and hands off to the B5 transfer with the same payment placeholder; reactivation restores nothing (M18).
- Patient inquiry cancellation (B3) supersedes the AcceptanceEvent through a linked FR-005 record with cause `InquiryCancelled`, never by editing the event.
- Promotion is frozen at acceptance; commission is fixed at booking confirmation on the accepted price after promotion; the FR-004 figure is indicative (D12, D13, M5).
- FR-006 triggers the FR-030 events `quote.withdrawn`, `booking.scheduled`, `booking.hold_expiring_soon`, `booking.payment_window_expired`, `booking.revived` and `booking.provider_fault_replacement` (D22, M13, M17, M18).
- An admin date change after confirmation triggers an FR-008 travel-date review for travel records already linked to the booking (REQ-006-017; cross-FR alignment with FR-008).
- `Confirmed` is a booking status only (D23).
- In Alternative Flow B5 the replacement booking receives the carried-over passport and copied flight and hotel records flagged "travel-date review required" per FR-008; originals stay read-only on the closed booking (Q18).
- A concurrent second acceptance for the same slot fails on the active-hold uniqueness rule (provider, appointment date/time, time zone) and the patient is told the slot was just taken (Q23).

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Hold start and duration | 48 hours after payment failure, FR-006 A-09 setting | One fixed hold from acceptance, FR-026 duration, never extended | M3, D14 |
| Slot and appointment | Slot hold with unclear key; appointment timing unclear | Exclusive hold keyed by provider, date/time and time zone; appointment record created on payment | M4 |
| Payment Window Expired scope | Not scoped | First payment step only; later instalments excluded | D1 |
| Recovery | New current subquote or admin intervention | Cancel inquiry and start a new one, or audited admin revive | D1, D2 |
| Admin status/date edits | Always available | Revive and guarded date change only | D2, D11, M17 |
| Provider fault | Full refund, no transfer | Alternative Flow B5 linked-record transfer with payment placeholder | D3, D6, D6-M |
| Provider suspension/deactivation after acceptance | Cancel only; no automatic refund or rebooking | Close and hand off to the B5 transfer with the payment placeholder | M18 |
| Promotion and commission | Resolved before booking | Promotion frozen at acceptance; commission fixed at confirmation; FR-004 figure indicative | D12, D13, M5 |
| Notification events | Generic | `quote.withdrawn`, hold expiring soon, Payment Window Expired, booking revived | D22, M13, M17 |
| Provider-fault travel carry-over | Not stated | B5 step 7 and REQ-006-018: travel carried over per FR-008 with review flag | Q18 |
| Concurrent acceptance | Second acceptance rejected; mechanism and patient message not stated | Active-hold uniqueness rule; patient told the slot was just taken | Q23 |
| Requirements | REQ-006-001 to 015 | REQ-006-003, 005, 010, 011, 013, 015 revised; REQ-006-016 to 018 added | Above decisions |

## Scope and Impact

### In Scope

- FR-006 hold, Payment Window Expired, admin intervention, provider-fault transfer, promotion/commission wording and triggered events.
- Minor corrections: booking cancelled in B3, snapshot wording, currency and source on amount fields, exchange-rate consumption, relative plan days.

### Out of Scope

- Payment rails, fund release, refunds and later instalment handling (payment pass), apart from the provider-fault placeholder.

### Affected Contracts

- **PRD owner**: `prd.md` — Alternative Flows B1, B2, B3, B4, B5; Screens 1 to 6; Admin Editability Rules; Payment & Billing Rules; REQ-006-003, 005, 010, 011, 013, 015, 016, 017, 018; Key Entities 1 and 2
- **Related FRs**: FR-005 (supersession record, linked acceptance record, recovery route), FR-004 (indicative commission, quote withdrawal), FR-007 and FR-007B (first-payment boundary, provider-fault money), FR-010 (provider drop-out), FR-014 and FR-022 (booking states), FR-017 and FR-029 (commission lock point), FR-019 (promotion re-reservation on revive), FR-020 and FR-030 (events), FR-026 (slot-hold duration and reminder lead time), FR-015 (suspension/deactivation cascade hands off to the transfer)
- **System documents**: `system-prd.md`, `system-data-schema.md` (bookings and acceptance_events tables, hold fields), `system-technical-spec.md`
- Supersedes in part: CR-FR006-20260915-01 (terminal expiry statement amended for the revive exception)

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed
- **Required assessment**: booking API, hold and appointment creation, admin intervention actions, notification triggers, permissions, tests
- **Compatibility / rollout risk**: existing holds that were extended after payment failure; existing unrestricted admin status edits
- **Data migration**: To be assessed

## Acceptance and Validation

- No FR-006 text extends the hold after payment failure.
- No admin status or date action is available "Always".
- The hold key names provider, appointment date/time and time zone.
- After a provider-fault transfer, the replacement booking shows the carried-over passport and the copied, flagged flight and hotel records.
- A concurrent second acceptance for a held slot fails and that patient sees a slot-just-taken message.
- FR-005, FR-007, FR-007B, FR-010, FR-026 and FR-030 describe the same contract after their own fix packages.

## Approval and Traceability

- **Requested by**: Product Owner (MTG-002 quote model audit)
- **Approved by**: Product Owner, 2026-10-16, via `reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md` (documentation only)
- **Decision evidence**: SRC-MTG-002; decision log 2026-10-16 (D1, D2, D3, D6, D6-M, D11, D12, D13, D14, D22, D23, M3, M4, M5, M13, M17, M18; Q-series Q18, Q23); findings S1-1, S1-2, S1-3, S1-6, S2-4, S2-5, S4-1, S4-2, FR-006-3
- **Implementation reconciliation**: Required, not assessed
- **PRD change log**: v2.7 and v2.8 (2026-10-16)
- **Update log**: Combined 2026-10-16 MTG-002 log (controller-owned)
- **Supersedes**: CR-FR006-20260915-01 in part
- **Superseded by**: None
