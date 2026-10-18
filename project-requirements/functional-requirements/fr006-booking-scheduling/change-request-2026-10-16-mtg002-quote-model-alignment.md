# Change Request: MTG-002 Quote Model Alignment for Booking and Scheduling

**Change Request ID**: CR-FR006-20261016-01
**Primary FR**: FR-006
**Triggering FR / Event**: SRC-MTG-002 quote model verification and Product Owner decision log (2026-10-16)
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-16
**Decision Date**: 2026-10-16
**PRD Version Change**: v2.6 to v2.10
**Related Commit(s)**: Pending

---

## Decision Summary

The MTG-002 quote model audit found that FR-006 contradicted itself on when the slot hold starts and whether payment failure extends it, gave no workable recovery route after `Payment Window Expired`, allowed unrestricted admin status and date edits, and had no flow for provider fault after acceptance. The Product Owner approved decisions D1, D2, D3, D6, D6-M, D11, D12, D13, D14, D22, D23, M3, M4, M5, M13, M17 and M18. This request records the resulting changes to the FR-006 booking contract.

## Baseline State

**Source version**: FR-006 v2.6, `Business Workflows`, `Business Rules`, `Functional Requirements Summary`, `Key Entities`

FR-006 held the slot for 48 hours "after payment failure" through its own A-09 setting while also saying the hold starts at acceptance. The slot was not keyed explicitly, and it was unclear when the appointment record existed. `Payment Window Expired` was terminal, with recovery by "a new current subquote or an audited admin intervention", which FR-005 Rule 1 made impossible. Admin "Modify Status" and "Modify Appointment Date" were available "Always". Provider cancellation meant a full refund with no transfer path. The assumptions said discounts and commissions were "already resolved before booking stage".

## Approved State

**Target version**: FR-006 v2.10, same headings, plus `Alternative Flows` B5, B6 and B7, admin Screens 7 to 11, and `Admin Status and Date Intervention Rules`

- One fixed hold starts at subquote acceptance and lasts the FR-026 slot-hold duration (default 48 hours). Payment failure never extends or restarts it (M3, D14).
- The hold is a temporary exclusive hold keyed by provider, appointment date/time and time zone. The appointment record is created only on successful payment. On expiry the hold is released and no appointment exists (M4).
- `Payment Window Expired` applies only to the first payment step. Missed later instalments never cause it or inquiry cancellation (D1).
- Recovery after `Payment Window Expired`: the patient contacts support, and an admin either revives the booking or cancels it so the patient can start a new inquiry (D1, Q37).
- Admin revive moves a `Payment Window Expired` booking back to `Accepted` with a mandatory reason, a slot re-check, a new hold, one promotion use taken again where the promotion has a usage limit (re-reserved for a provider-selected promotion or patient code, taken again for an automatic promotion; rejected if the limit has no room), an audit entry, an unchanged AcceptanceEvent and a mandatory "booking revived" notice. Date changes need a slot check and trigger an FR-008 travel-date review (Q30). No other manual status jumps (D2, D11, M17).
- New Alternative Flow B5: provider fault in `Accepted` or `Confirmed` cancels the booking with cause `ProviderFault` and releases the hold. An admin authors a replacement quote for the replacement provider inside the same inquiry (the only exception to the FR-004 no-new-quote rule), and the new admin-authored AcceptanceEvent points to that quote, option and date-price row. The single supersession record is written once, at the replacement acceptance; the closure itself is recorded on the booking as its cause. Payment mechanics are a placeholder only (D3, D6, D6-M, Q35).
- The B5 replacement quote is authored through FR-004 Workflow 7 and Screen 8. A replacement quote that is not accepted expires under the normal quote expiry; the inquiry stays `supportRequired` and is not cancelled automatically, and the admin may author another replacement quote or cancel the inquiry and booking (Q49).
- New Alternative Flow B7 and admin Screen 11: a provider fault while `In Progress` keeps the booking `In Progress` with `supportRequired` and no automatic cancellation; the admin decides case by case to move the booking to `Aftercare` and reassign the aftercare provider through FR-011 Screen 19, or to cancel it through Screen 9. No replacement acceptance; money stays with the payment placeholder. The B5 transfer is limited to bookings before treatment starts (Q45).
- New Alternative Flow B6: provider fault during `Aftercare` keeps the booking and treatment record and reassigns only the aftercare provider or team through FR-011, with no new acceptance or payment (Q36).
- Cancellation from acceptance onward is admin-only (B2, Screen 9): the patient sees Contact Support, and an admin cancels from `Accepted`, `Payment Window Expired`, `Confirmed`, `In Progress` or `Aftercare` with a mandatory reason, confirmation and audit entry. The booking and inquiry become `Cancelled`, the accepted quote stays `accepted`, and refunds follow the payment placeholder (Q37).
- Screen 6 Booking Status and appointment fields are read-only; each intervention (revive, change appointment, cancel booking, provider-fault transfer and replacement quote, aftercare reassignment link) has its own admin screen with fields, validation, mandatory reason, confirmation, audit entry and notice (Screens 7 to 10) (Q43).
- Provider suspension or deactivation after acceptance (B4) closes `Accepted` and `Confirmed` bookings with the provider-status cause recorded on the booking, releases the hold and hands off to the B5 transfer with the same payment placeholder; `In Progress` bookings follow B7 and `Aftercare` bookings follow B6 (Q45); reactivation restores nothing (M18, Q35, Q36).
- Cancellation during the post-acceptance hold (B3) is support-routed and performed by an admin; the AcceptanceEvent stays unchanged and no supersession record is written, because supersession is written only at a provider-fault replacement acceptance (Q37).
- Promotion is frozen at acceptance; commission is fixed at booking confirmation on the accepted price after promotion; the FR-004 figure is indicative (D12, D13, M5).
- FR-006 triggers the FR-030 events `booking.scheduled`, `booking.hold_expiring_soon`, `booking.payment_window_expired`, `booking.revived` and `booking.provider_fault_replacement`, with admin as an exception-alert recipient of the hold-expiring, Payment Window Expired and provider-fault events. FR-004 is the only producer of `quote.withdrawn`; FR-006 reacts to it by starting the B5 transfer (D22, M13, M17, M18, Q11, Q31).
- The provider-fault transfer notice goes to the patient and admin; the replacement provider learns through `quote.accepted`, and the original provider is not notified by this event (Q32, Q42).
- FR-006 is the producer of `booking.rescheduled` (mandatory, patient and provider) on an admin appointment change, with the old and new appointment as variables; booking notices read the booking's current appointment while the snapshot keeps the baseline. `booking.scheduled` goes to the patient only, is mandatory, and fires on patient acceptance and on the admin replacement acceptance. Admin cancellation sends `booking.cancelled` (Q42).
- Provider cancellation after acceptance is not a B2 cancellation; it follows the B5 transfer, and refund amounts stay under the B5 payment placeholder (D6, D6-M).
- The booking total shown on Screen 1 and on Screens 4 and 6 is the accepted price after promotion, from the acceptance snapshot; the offered price is shown separately as entered before any promotion (Q25, D12).
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
| Notification events | Generic | `booking.scheduled`, `booking.hold_expiring_soon`, `booking.payment_window_expired`, `booking.revived`, `booking.provider_fault_replacement` with admin exception recipients; `quote.withdrawn` produced by FR-004 only | D22, M13, M17, Q11, Q31, Q32 |
| Booking total on screens | Accepted subquote offered price | Accepted price after promotion; offered price shown separately | Q25, D12 |
| B2 cancellation trigger | Patient or provider | Admin only, from any non-terminal booking state, on a support-routed patient request or admin decision; provider withdrawal or drop-out follows B5 | D6, D6-M, Q37 |
| Provider-fault travel carry-over | Not stated | B5 step 7 and REQ-006-018: travel carried over per FR-008 with review flag | Q18 |
| Concurrent acceptance | Second acceptance rejected; mechanism and patient message not stated | Active-hold uniqueness rule; patient told the slot was just taken | Q23 |
| Provider-fault replacement | Linked acceptance record with no quote; supersession written at closure | Admin-authored replacement quote in the same inquiry; single supersession insert at replacement acceptance; closure recorded on the booking | Q35 |
| Provider fault in Aftercare | Booking cancelled | Booking and treatment record kept; aftercare provider reassigned through FR-011 | Q36 |
| Provider fault while In Progress | Followed the B5 transfer pending Product Owner confirmation | Booking stays `In Progress` with `supportRequired`; admin moves it to `Aftercare` with an FR-011 reassignment or cancels it (Alternative Flow B7, Screen 11); B5 limited to before treatment | Q45 |
| Replacement quote not accepted | Not stated | Normal quote expiry; inquiry stays `supportRequired`; admin may author another replacement quote or cancel | Q49 |
| Admin appointment change notice | Not produced | `booking.rescheduled` produced by FR-006 to patient and provider; `booking.scheduled` patient-only, also on replacement acceptance | Q42 |
| Admin intervention screens | Screen 6 actions only | Screens 7 to 11 and the FR-011 reassignment link, each with fields, reason, confirmation, audit and notice | Q43 |
| Requirements | REQ-006-001 to 015 | REQ-006-003, 004, 005, 010, 011, 013, 015, 017, 018 revised; REQ-006-016 to 019 added | Above decisions |

## Scope and Impact

### In Scope

- FR-006 hold, Payment Window Expired, admin intervention, provider-fault transfer, promotion/commission wording and triggered events.
- Minor corrections: booking cancelled in B3, snapshot wording, currency and source on amount fields, exchange-rate consumption, relative plan days.

### Out of Scope

- Payment rails, fund release, refunds and later instalment handling (payment pass), apart from the provider-fault placeholder.

### Affected Contracts

- **PRD owner**: `prd.md` — Alternative Flows B1, B2, B3, B4, B5, B6, B7; Screens 1 to 11; Admin Editability Rules; Payment & Billing Rules; Dependencies; User Story 4; REQ-006-003, 005, 010, 011, 013, 015, 016, 017, 018, 019; Key Entities 1 and 2
- **Related FRs**: FR-005 (supersession record, linked acceptance record, recovery route), FR-004 (indicative commission, quote withdrawal), FR-007 and FR-007B (first-payment boundary, provider-fault money), FR-010 (provider drop-out), FR-014 and FR-022 (booking states), FR-017 and FR-029 (commission lock point), FR-019 (promotion use re-reserved or taken again on revive, by promotion source), FR-020 and FR-030 (events), FR-026 (slot-hold duration and reminder lead time), FR-015 (suspension/deactivation cascade hands off to the transfer; `Aftercare` bookings stay `Aftercare`), FR-011 (aftercare reassignment screen), FR-003 and FR-016 (patient cancel limited to Inquiry and Quoted; admin cancel)
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
- No FR-006 text lists `quote.withdrawn` as an event FR-006 triggers, and no text says both providers are notified of the transfer.
- No FR-006 text routes provider cancellation after acceptance to a full refund; it routes to Alternative Flow B5.
- After a provider-fault transfer, the replacement booking shows the carried-over passport and the copied, flagged flight and hotel records.
- A concurrent second acceptance for a held slot fails and that patient sees a slot-just-taken message.
- No patient-facing FR-006 screen offers booking cancellation after acceptance; Contact Support is shown instead.
- Only one supersession record is written per provider-fault transfer, at the replacement acceptance, and the replacement AcceptanceEvent names a quote, option and date-price row.
- A provider fault during `Aftercare` leaves the booking in `Aftercare`.
- A provider fault while `In Progress` leaves the booking `In Progress` with `supportRequired`; Screen 11 offers only Move to Aftercare and reassign, or Cancel, and the B5 transfer is not offered.
- A replacement quote that is not accepted expires normally and the inquiry stays `supportRequired`.
- No admin cancellation writes a supersession record.
- An admin appointment change sends `booking.rescheduled` to the patient and provider.
- Every Screen 6 intervention action opens a screen with a mandatory reason, confirmation and audit entry.
- FR-005, FR-007, FR-007B, FR-010, FR-026 and FR-030 describe the same contract after their own fix packages.

## Approval and Traceability

- **Requested by**: Product Owner (MTG-002 quote model audit)
- **Approved by**: Product Owner, 2026-10-16, via `reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md` (documentation only)
- **Decision evidence**: SRC-MTG-002; decision log 2026-10-16 (D1, D2, D3, D6, D6-M, D11, D12, D13, D14, D22, D23, M3, M4, M5, M13, M17, M18; Q-series Q11, Q18, Q23, Q25, Q30); decisions 2026-10-18 (Q31, Q32, Q35, Q36, Q37, Q42, Q43, Q45, Q49); findings S1-1, S1-2, S1-3, S1-6, S2-4, S2-5, S4-1, S4-2, FR-006-3
- **Implementation reconciliation**: Required, not assessed
- **PRD change log**: v2.7 and v2.8 (2026-10-16); v2.9 consolidated verification corrections (2026-10-18); v2.10 final audit corrections (2026-10-18)
- **Update log**: Combined 2026-10-16 MTG-002 log (controller-owned)
- **Supersedes**: CR-FR006-20260915-01 in part
- **Superseded by**: None
