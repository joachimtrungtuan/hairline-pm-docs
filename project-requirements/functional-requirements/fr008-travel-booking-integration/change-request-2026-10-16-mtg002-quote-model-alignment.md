# Change Request: MTG-002 Quote Model Alignment for Travel Coordination

**Change Request ID**: CR-FR008-20261016-01
**Primary FR**: FR-008
**Triggering FR / Event**: MTG-002 quote model audit and Product Owner decision log of 2026-10-16 (decisions D7, M2, P1)
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-16
**Decision Date**: 2026-10-16
**PRD Version Change**: v2.5 to v2.7
**Related Commit(s)**: Pending

> Created under decision P1: the implementation status of FR-008 is unknown, so a Change Request is recorded to keep documentation approval separate from implementation reconciliation.

---

## Decision Summary

The MTG-002 quote model verification found that the FR-008 travel-date review flag had an entry trigger but no exit or owner (finding FR-008-2), and that FR-008 did not say where the appointment and date range come from after acceptance. The Product Owner decided that an admin confirms or corrects the travel details and the flag then clears (D7), and that downstream modules read price, currency, date range, appointment and promotion from the accepted snapshot only, while treatment plan, clinicians and grafts change only through FR-010 (M2). Related Minor findings FR-008-1 and FR-008-3 to FR-008-8 were verified against the current text and applied.

## Baseline State

**Source version**: FR-008 v2.5, `Travel Path Determination`, `Travel Context and Booking Lifecycle`, Screens 2, 3, 5, 6, 8 and 11, REQ-008-008 and REQ-008-026 to REQ-008-029, `TravelContext`, `Itinerary`

- `travel-date-review-required` was set when an admin changed the appointment date, but nothing said who clears it or how, so a TravelContext could stay in review indefinitely.
- The Option/Date-Price Record "supplied" the appointment and date range without saying that FR-008 reads them from the accepted snapshot; TravelContext stored the accepted appointment but not the accepted date range.
- Flight date validation referred to an undefined "appointment window" and a "procedure start date".
- After a confirmed booking was cancelled, the API rejection rule and Re-notify eligibility did not cover the closed TravelContext.
- Some text still referred to "package" travel inclusions, `included_services_snapshot` was stored on both TravelContext and Itinerary, the `no_travel_required` decision had no owning field, the Path B rule did not mention other travel services, and there were no acceptance scenarios.

## Approved State

**Target version**: FR-008 v2.7, same headings plus `Acceptance Scenarios`, Alternative Flow B2 and REQ-008-030 to REQ-008-033

- Travel-date review is admin-owned. From Screen 11 the admin confirms the existing flight and hotel dates or corrects them through Screen 12; either action returns the TravelContext to `active` and is audited. Patients and providers see the review state but cannot clear it.
- FR-008 reads the accepted appointment and date range from the FR-005 accepted snapshot, never from the live quote, and stores the accepted date range on TravelContext. Relative treatment plan days are never converted to calendar dates. Later FR-010 changes to plan, clinicians or grafts do not change the TravelContext.
- Travel-date validation is anchored to the current booking appointment, which equals the accepted snapshot appointment unless an admin-approved change exists.
- A closed TravelContext rejects new travel records, re-notification and admin corrections; its records stay read-only.
- Wording refers to the accepted option; inclusion data has one owner (TravelContext); `travel_required` with actor and time records the Path B "no travel" decision; Path B covers transport-only and other-services-only options; seven acceptance scenarios cover the lifecycle.
- A return flight or hotel check-out before the last treatment plan day raises a soft warning that must be acknowledged; the record still saves and the provider sees an early-departure flag. The last plan day date is derived only for this warning and is not stored (Q17).
- On an FR-006 provider-fault transfer, the passport carries over to the replacement booking, flight and hotel records are copied to it with a copy-source reference and flagged "travel-date review required", and the originals stay read-only on the closed booking (Q18).
- The itinerary is a read view assembled from the TravelContext, the current travel records and the Booking; no itinerary table or stored record exists (Q21).

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Travel-date review | Flag set on admin appointment change; no exit or owner | Admin confirms or corrects; flag clears to `active`; audited (REQ-008-030, Screen 11) | D7, finding FR-008-2 |
| Appointment and date range source | Option/Date-Price Record "supplies" them | Read from the FR-005 accepted snapshot; accepted date range stored on TravelContext | M2 |
| Plan days | Not stated | Relative days, never converted to calendar dates; FR-010 changes do not alter TravelContext | M2 |
| Date validation | Undefined "appointment window" | Outbound arrival on or before, return departure after, the current booking appointment; hotel dates checked the same way | Finding FR-008-1 |
| Closed TravelContext | Not covered by API rejection or Re-notify | Rejects writes, re-notification and corrections; records read-only | Finding FR-008-3 |
| Vocabulary and ownership | Package wording; duplicated inclusion snapshot; no field for `no_travel_required` | Accepted-option wording; TravelContext sole owner; `travel_required` with actor and time | Findings FR-008-4, FR-008-5, FR-008-6 |
| Path B scope | Transport only or empty | Transport, other travel services, or empty | Finding FR-008-7 |
| Early departure | Return flight or check-out before the last plan day not addressed | Soft warning, acknowledged, record saves, provider flag (REQ-008-008, REQ-008-031) | Q17 |
| Provider-fault transfer | Travel records stayed on the closed booking only | Passport carried over; flight and hotel copied with source reference and review flag; originals read-only (Alternative Flow B2, REQ-008-032) | Q18 |
| Itinerary storage | Stored Itinerary entity with record IDs | Read view only, no table (REQ-008-014, REQ-008-033) | Q21 |
| Testability | No scenarios | Seven Given/When/Then acceptance scenarios | Finding FR-008-8 |

## Scope and Impact

### In Scope

- Travel-date review exit and owner, snapshot source of appointment and date range, validation anchor, closed-context guard, and the Minor clean-ups listed above.

### Out of Scope

- Payment rails, fund release, refunds, later instalments, and payment-driven booking states (installment default, dispute, refund-driven cancellation); these stay with the payment pass.
- Provider-fault transfer effects on travel coordination (FR-006 and FR-005 own the transfer; any travel follow-up is to be assessed at consolidated verification).
- Changes to the binary Path A / Path B model.

### Affected Contracts

- **PRD owner**: `prd.md` — `Travel Path Determination`, `Travel Context and Booking Lifecycle`, REQ-008-008, REQ-008-026, REQ-008-028 to REQ-008-030, `TravelContext`, `Itinerary`, Screens 2, 3, 5, 6, 8, 11, `Acceptance Scenarios`
- **Related FRs**: FR-005 (accepted snapshot fields, including date range), FR-006 (admin appointment-date change triggers review), FR-004 (travel items as Quote Option items; optional wording alignment "at FR-006 booking confirmation"), FR-010 (plan, clinicians and grafts changes do not affect TravelContext), FR-024 (packages seed travel items)
- **System documents**: `system-data-schema.md` (travel context fields: accepted date range, `travel_required` with actor and time, review cleared by/at; drop itinerary `included_services_snapshot`), `system-technical-spec.md` (closed-context rejection)

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed
- **Required assessment**: travel APIs (closed-context rejection, date validation), data model (new TravelContext fields), admin UI (Confirm Travel Dates action, status badge), patient and provider screens (review and closed states), audit logging
- **Compatibility / rollout risk**: Existing travel contexts need the accepted date range backfilled from the acceptance snapshot
- **Data migration**: To be assessed

## Acceptance and Validation

- A TravelContext in travel-date review returns to `active` only after an admin confirm or correct action, with an audit entry.
- TravelContext appointment and date range match the accepted snapshot; no plan day is stored as a calendar date, and the derived last plan day is used only for the early-departure warning.
- A return flight or check-out before the last plan day saves only after the warning is acknowledged, and the provider sees the flag.
- After a provider-fault transfer, the replacement booking shows the carried-over passport and the copied, flagged flight and hotel records; the closed booking's originals are read-only.
- No itinerary table exists; the itinerary view is built from TravelContext, travel records and Booking.
- Writes against a closed TravelContext are rejected.
- Cross-FR check: FR-005 snapshot and system schema carry the accepted date range and the TravelContext fields named above.

## Approval and Traceability

- **Requested by**: Product Owner (MTG-002 quote model audit)
- **Approved by**: Product Owner, 2026-10-16, via the decision log `reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md` (documentation approval only)
- **Decision evidence**: `reports/2026-10-16/mtg002-quote-model-verification-2026-10-16.md`, `reports/2026-10-16/mtg002-quote-model-fix-plan-2026-10-16.md`; Product Owner Q-series answers Q17, Q18 and Q21 in `reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md`
- **PRD change log**: v2.6 and v2.7 rows dated 2026-10-16
- **Update log**: Combined 2026-10-16 MTG-002 update log (controller-owned)
- **Supersedes**: None (extends CR-FR008-20260929-01)
- **Superseded by**: None
