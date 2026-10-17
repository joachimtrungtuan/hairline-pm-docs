# MTG-002 Quote Model Alignment (Verification, Decisions and Fixes)

**Date**: 2026-10-16
**Update Type**: Major requirement alignment (cross-FR verification, Product Owner decisions, verification fixes, new Change Requests)
**Source**: [Meeting 02 (SRC-MTG-002)](../../sources/meetings/meeting-02-launch-quote-options-fund-release-and-payments.md)
**Decision Status**: Documentation approved by Product Owner (2026-10-16) through the decision log below
**Implementation Reconciliation**: Required — not assessed
**Change Requests**: Listed per wave below (17 planned, one per affected FR)

## Decision and Evidence

A concurrent verification of every FR updated for Meeting 02 checked the new quote data model (parent quote, Quote Option, option × date-range price row as subquote, AcceptanceEvent and snapshot, slot hold, booking handoff, `Payment Window Expired`) and its consumers. Payment and fund-release mechanics were reference only and are deferred to a separate payment pass. The audit found 4 Critical, 45 Major, 87 Minor and 24 Observation findings after adversarial verification. The Product Owner decided every Critical and Major finding through AskUserQuestion (D1 to D24, D6-M, R7-1 to R7-4, M1 to M17, P1 to P3).

## Reports

- [Verification report](../../../reports/2026-10-16/mtg002-quote-model-verification-2026-10-16.md) — findings register, themes, traceability
- [Decision log](../../../reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md) — authoritative Product Owner decisions
- [Fix plan](../../../reports/2026-10-16/mtg002-quote-model-fix-plan-2026-10-16.md) — waves, per-FR edits, Change Requests, cross-FR checks

## Changes

Appended per wave as fixes are applied.

### Wave 1 — Acceptance and booking (FR-005 v2.4 → v2.5, FR-006 v2.6 → v2.7)

- **Acceptance records (FR-005)**: AcceptanceEvents, accepted subquotes and their parent quotes can no longer be deleted or restored; admins add audited annotations only. Supersession is a separate append-only record (causes inquiry cancelled, provider fault, provider suspended, provider deactivated); the event itself is never edited.
- **One acceptance per inquiry (FR-005)**: The only exception is an admin provider-fault transfer, recorded as a new linked admin-authored acceptance record in the same inquiry.
- **Snapshot (FR-005)**: Price, currency, date range, appointment and promotion are the binding money fields, plus the exchange rate and its timestamp (a stale cached rate is used and recorded). Plan, clinicians and grafts change after acceptance only through FR-010. A parent quote offers up to options × date ranges subquotes.
- **Patient promotion code (FR-005)**: Entered before acceptance on one named subquote and frozen into the AcceptanceEvent.
- **Slot hold (FR-005, FR-006)**: One fixed hold from acceptance for the FR-026 duration (default 48 hours), keyed by provider, appointment date/time and time zone; payment failure never extends it; the appointment record is created only at successful payment.
- **Payment Window Expired (FR-005, FR-006)**: Applies only to the first payment step; missed later instalments never cause it. Recovery is cancel-and-new-inquiry or an audited admin revive (reason, slot re-check, fresh hold, promotion re-reservation, mandatory "booking revived" notice to patient and provider). Admin status and date edits are no longer unrestricted.
- **Provider fault after acceptance (FR-006 new flow B5)**: Provider withdrawal, drop-out, suspension or deactivation after acceptance closes the booking, releases the hold, supersedes the acceptance via a linked record, and an admin rehomes the patient to a replacement provider in the same inquiry. Paid money follows the patient as credit, unused money is refunded, no patient fees; mechanics deferred to the payment pass.
- **Commission and deposit (FR-006)**: Promotion frozen at acceptance; commission and deposit settings fixed at booking confirmation; FR-004 figure indicative.
- **Additional PO decision M18**: Provider suspension or deactivation after acceptance follows the provider-fault transfer instead of cancel-only.
- **Change Requests**: [CR-FR005-20261016-01](../../functional-requirements/fr005-quote-comparison-acceptance/change-request-2026-10-16-mtg002-quote-model-alignment.md), [CR-FR006-20261016-01](../../functional-requirements/fr006-booking-scheduling/change-request-2026-10-16-mtg002-quote-model-alignment.md). Stale lines corrected in CR-0915 for FR-005 (line 62) and FR-006 (line 29).

### Wave 2 — Quote, promotions and packages (FR-004 v3.0 → v3.1, FR-019 v2.1 → v2.2, FR-024 v1.2 → v1.3)

- **Quote versioning and audit (FR-004)**: Expiry and currency are captured at first send; every send creates a quote version and audit entry. `acceptedTotal`, terms-acknowledged time and locked exchange rate are read-only copies of the FR-005 snapshot; the duplicate `isAccepted` flag is removed. No quote edits after acceptance; treatment changes go through FR-010.
- **Quote outcomes (FR-004)**: Unsent drafts are cancelled silently when another subquote is accepted; one not-selected notice per sent parent quote. Provider suspension or deactivation cancels only unaccepted quotes; accepted quotes follow the FR-006 provider-fault transfer. `quote.withdrawn` is always mandatory. Commission shown at quote time is labelled "indicative, final at booking confirmation".
- **Option/date-price rows (FR-004)**: One row per option and date range, appointment in the future; zero-price policy left open for a product decision.
- **Promotions (FR-019)**: Terms are fixed at send and copied into the quote version; automatic promotions attach at send to eligible rows, with the price kept as entered and the discount shown separately. Patient codes apply before acceptance to one named subquote. The redemption record is created at acceptance and linked to the AcceptanceEvent; no promotion change after acceptance except the provider-fault transfer. One usage lifecycle: reserve, consume, release, re-reserve on revive.
- **Packages (FR-024)**: A package is a full template for one Quote Option (items, travel services, relative-day plan, standard price); each selected package is one alternative option, up to 5, never summed. Library edits create a new read-only version; inline edits inside a quote are quote-local and never written back. Add-on types, package currency, QuoteTreatment and QuotePackage removed. Usage Count counts options on open (draft or sent) quotes.
- **Change Requests**: [CR-FR004-20261016-01](../../functional-requirements/fr004-quote-submission/change-request-2026-10-16-mtg002-quote-model-alignment.md), [CR-FR019-20261016-01](../../functional-requirements/fr019-promotions-discounts/change-request-2026-10-16-mtg002-quote-model-alignment.md), [CR-FR024-20261016-01](../../functional-requirements/fr024-treatment-package-management/change-request-2026-10-16-mtg002-quote-model-alignment.md). Stale lines corrected in FR-004 CR-0909 and CR-1014 ("Superseded by"), FR-019 CR-0910 and FR-024 CR-0910.


### Wave 3 — Downstream consumers (FR-007 v1.7, FR-007b v1.3, FR-008 v2.6, FR-010 v2.2, FR-014 v3.15, FR-015 v1.17, FR-017 v2.11, FR-020 v2.7, FR-022 v2.14, FR-026 v1.12, FR-029 v1.11, FR-030 v1.12; cross-FR FR-003 v2.9, FR-016 v1.7)

- **Snapshot reads**: Payment (FR-007, FR-007b), travel (FR-008), treatment (FR-010), finance (FR-017) and analytics (FR-014) read price, currency, date range, appointment and promotion only from the accepted snapshot, never from the live quote.
- **Booking total and lock points (FR-029, FR-017)**: "Booking total" means the accepted subquote price after promotion, in the quote currency, from the snapshot. FX locks at acceptance; commission and deposit settings lock at booking confirmation; commission shown earlier is indicative.
- **Configuration (FR-026)**: Owns the quote expiry window (48h, copied at first send), quote-expiring-soon lead time, slot-hold duration (48h) and hold-expiring-soon lead time; the quote records the configuration version, and first send is blocked if the configuration cannot be read (also stated in FR-004).
- **Treatment changes (FR-010)**: The only audited, patient-notified route for post-acceptance changes to plan days, clinicians or graft estimate (`treatment.plan_changed`); plan days stay relative; provider drop-out goes to the FR-006 provider-fault transfer.
- **Provider status (FR-015, FR-003, FR-016)**: Suspension or deactivation after acceptance closes the booking and the admin rehomes the patient through the FR-006 provider-fault transfer; the inquiry stays open with the support marker. `provider.status_cancellation_patient` applies before acceptance only.
- **Notifications (FR-030, FR-020)**: Event registry aligned: `quote.submitted` ("From" price), `quote.expiring_soon`, `quote.withdrawn`, `quote.accepted` outcomes with locks, `booking.scheduled` (Booking Accepted — Slot Held), `booking.hold_expiring_soon`, `booking.payment_window_expired`, `booking.revived`, `booking.provider_fault_replacement`, `treatment.plan_changed`; `quote.declined` moved to Post-MVP; unsent drafts get no notice.
- **Search and analytics (FR-022, FR-014)**: Patient search, filter and sort work at subquote level; analytics count parent responses, options and accepted subquotes separately.
- **Controller alignment**: FR-006 REQ-006-011 now names the exact event keys and REQ-006-017 sends admin date changes to an FR-008 travel review; FR-005 CR lists FR-022. Older CRs CR-FR003-20261014-01, CR-FR004-20261014-01, CR-FR010-20260910-01 and CR-FR017-20261015-01 are marked superseded in part.
- **Change Requests**: [CR-FR003-20261016-01](../../functional-requirements/fr003-inquiry-submission/change-request-2026-10-16-mtg002-quote-model-alignment.md), [CR-FR007-20261016-01](../../functional-requirements/fr007-payment-processing/change-request-2026-10-16-mtg002-quote-model-alignment.md), [CR-FR007B-20261016-01](../../functional-requirements/fr007b-payment-installments/change-request-2026-10-16-mtg002-quote-model-alignment.md), [CR-FR008-20261016-01](../../functional-requirements/fr008-travel-booking-integration/change-request-2026-10-16-mtg002-quote-model-alignment.md), [CR-FR010-20261016-01](../../functional-requirements/fr010-treatment-execution/change-request-2026-10-16-mtg002-quote-model-alignment.md), [CR-FR014-20261016-01](../../functional-requirements/fr014-provider-analytics-reporting/change-request-2026-10-16-mtg002-quote-model-alignment.md), [CR-FR015-20261016-01](../../functional-requirements/fr015-provider-management/change-request-2026-10-16-mtg002-quote-model-alignment.md), [CR-FR017-20261016-01](../../functional-requirements/fr017-admin-billing-finance/change-request-2026-10-16-mtg002-quote-model-alignment.md), [CR-FR020-20261016-01](../../functional-requirements/fr020-notifications-alerts/change-request-2026-10-16-mtg002-quote-model-alignment.md), [CR-FR022-20261016-01](../../functional-requirements/fr022-search-filtering/change-request-2026-10-16-mtg002-quote-model-alignment.md), [CR-FR026-20261016-01](../../functional-requirements/fr026-app-settings-security/change-request-2026-10-16-mtg002-quote-model-alignment.md), [CR-FR029-20261016-01](../../functional-requirements/fr029-payment-system-config/change-request-2026-10-16-mtg002-quote-model-alignment.md), [CR-FR030-20261016-01](../../functional-requirements/fr030-notification-rules-config/change-request-2026-10-16-mtg002-quote-model-alignment.md)

### Wave 4 — System documents (system PRD, system data schema v1.7.0 → v1.8.0, system technical spec v1.1.1 → v1.2.0)

- **System PRD** (no change-log table; Last Updated 2026-10-16): Workflows 1 and 2 and the FR-003, FR-004, FR-005, FR-006, FR-010, FR-014, FR-019, FR-020 and FR-024 sections summarise the final FR wording. The patient-facing "Booked" step is now "Booking Accepted — Slot Held (Pending Payment)" (booking status `Accepted`); `Confirmed`, the appointment and the slot block come at first payment. Packages are versioned, currency-free option templates. Edge cases EC-001, EC-002 and EC-006 and the glossary are updated, and the FR-020 section lists the FR-030 event keys.
- **System data schema v1.8.0**: Adds `acceptance_events` (append-only, snapshot plus read-only money columns, FX rate and timestamp), `acceptance_supersessions` (four causes, replacement link), `acceptance_annotations`, `bookings` (hold key, fixed hold start and expiry, status incl. `payment_window_expired`, `booking_total`, binding commission snapshot), `quote_versions`, `quote_audits`, `package_plan_days`, `promotion_applications`, `travel_contexts` and `treatment_detail_changes`. Quotes gain `version`, `first_sent_at` and `quote_config_version`. Packages are versioned with no currency. Quote status `confirmed`, `rejected`, `is_accepted` and the `quote_packages` / `quote_treatments` link tables are removed. Hotels, flights and passport records are keyed by `travel_context_id`.
- **System technical spec v1.2.0**: Separate quote and booking status flows; acceptance holds the slot only, and the appointment is created at first payment; fixed hold, first-payment Payment Window Expired, admin revive, provider-fault transfer, snapshot reads, FR-026 configuration read at first send. Examples now read accepted money from `acceptance_events` and no longer accept a provider-supplied amount, currency or treatment date.

### Final light audit corrections (same day)

A read-only audit of all 19 FRs and 3 system documents confirmed every planned edit was applied and the schema quote and booking statuses match FR-004 and FR-006 exactly. Leftover gaps were corrected without new versions:

- **Header Change Request links** added to FR-005, FR-006, FR-007b, FR-008, FR-017, FR-019, FR-022, FR-024 and FR-026 (FR-019 Change Log row now links its CR too).
- **FR-003**: Inquiry entity no longer lists provider-status causes on the inquiry (they live on the provider participation and the booking); REQ-003-014 hold wording points to the FR-026 configured duration.
- **FR-004**: admin soft delete and restore are unavailable for `accepted` quotes (body and Screen 5 actions).
- **FR-006**: B5 boundary states B4 is the trigger for provider-status cases and B5 owns the transfer; CR Approved State now lists all six FR-030 events and the FR-008 travel-date review on admin date changes.
- **FR-007**: REQ-007-019 drops the stale "applications" wording; CR marked as superseding CR-FR007-20261013-01 in part.
- **FR-007b**: booking-status labels follow FR-006 ("Fully Paid" and "Canceled - Partial Refund" removed); duplicate A1 outcome removed; upstream context says subquote.
- **FR-010**: Procedure Date (Screens 3 and 8) and Rule 14 use the current FR-006 booking appointment, with the accepted snapshot appointment as baseline, so approved admin date changes reach the Check In gate.
- **FR-015**: lock points add "nothing is fixed at quote creation". **FR-016**: FR-015 dependency reflects the post-acceptance transfer.
- **FR-020**: User Story 5 test split into an unaccepted offer (`provider.status_cancellation_patient`) and an accepted booking (`booking.provider_fault_replacement`).
- **System PRD**: `Payment Window Expired` described as final except for the audited admin revive (no "terminal" or "permanently").
- **System data schema**: commission snapshot pointer now §11A Bookings; `promotion_applications` migrates after `bookings`.
- **System technical spec**: E2E example prices an option/date-price row with no currency input; instalment example reads the parent quote from the AcceptanceEvent; provider-status cascade closes bookings, hands accepted cases to the FR-006 B5 transfer, keeps the inquiry open, and cites §11A.
- Not changed (Product Owner question): FR-029 has no rule blocking a currency from being disabled while sent quotes or bookings use it.

### Product Owner open-question decisions (Q-series Q1–Q30, applied 2026-10-18 under the 2026-10-16 change set)

Decisions are recorded in `reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md`, section "Post-execution open questions". Q26 (admin cancellation after a missed later instalment) and Q27 (provider payout trigger) are deferred to the payment pass. Q1, Q9, Q16, Q19 and Q22 confirm existing text. Each existing 2026-10-16 CR was amended. FR-032 has a new CR, CR-FR032-20261016-01.

- **FR-004 v3.1 → v3.2**: option/date prices must be greater than 0 (Q3). A Default Currency change converts open drafts and shows a banner that must be acknowledged (Q4). Automatic promotions reserve one use per sent quote, the reservation is kept across re-sent versions, and the use is consumed at acceptance (Q6, Q29). `first_sent_at` (Q15). Base Price pre-fill (Q20). FR-004 owns `quote.updated`, labelled "quote revised (new version)" (Q24).
- **FR-024 v1.3 → v1.4**: Screen 3 Base Price is reference-only and non-binding (Q20).
- **FR-014 v3.15 → v3.16**: Time to First Quote ends at the earliest parent quote's `first_sent_at` (Q15).
- **FR-005 v2.5 → v2.6**: The approximate price sort across currencies is labelled (Q8). The patient receives only `booking.scheduled` at acceptance (Q10). A concurrent acceptance of the same slot shows "slot just taken" (Q23). Promotion consumption and return follow Q6, Q29 and Q30.
- **FR-022 v2.14 → v2.15**: Same price-sort rule for search (Q8).
- **FR-019 v2.2 → v2.3**: Commission is charged on the price after promotion for every discount type, and the wording that Hairline-only discounts leave providers unaffected is removed (Q5). Two promotion use lifecycles, split by source (Q6, Q29). An automatic use returns on Payment Window Expired or cancellation before first payment (Q30).
- **FR-020 v2.7 → v2.8, FR-030 v1.12 → v1.13**: `quote.accepted` goes to providers only (Q10). Admins get exception alerts only (Q11). `quote.cancelled_inquiry` is mandatory (Q12). `quote.updated` is relabelled (Q24).
- **FR-032 v1.9 → v1.10**: The Quote Notifications toggle can no longer suppress the inquiry-cancelled quote notice (Q12).
- **FR-026 v1.12 → v1.13**: New bounds for quote expiry, slot hold and reminder lead times (Q13). A Default Currency change creates a new quote-configuration version (Q14).
- **FR-029 v1.11 → v1.12**: Currency changes for drafts (Q4). Commission base (Q5). A currency cannot be disabled while records still use it (Q7). Configuration version (Q14). One booking total base (Q25).
- **FR-007 v1.7 → v1.8**: REQ-007-014 commission base reworded (Q28). The deposit uses the booking total (Q25).
- **FR-015 v1.17 → v1.18, FR-017 v2.11 → v2.12**: Commission is charged after promotion for every discount type. The FR-017 Screen 5 Provider Cost field is now required (Q5).
- **FR-006 v2.7 → v2.8**: Travel carries over to the replacement booking in a provider-fault transfer (Q18). Active-hold uniqueness and the "slot just taken" message (Q23).
- **FR-008 v2.6 → v2.7**: Early-departure soft warning (Q17). Provider-fault travel carry-over with the "travel-date review required" flag (Q18). The itinerary is a read view (Q21).
- **FR-010 v2.2 → v2.3**: Treatment details are locked while `Accepted`. Audited changes are allowed from `Confirmed` until Check In, and each emits `treatment.plan_changed` (Q2).
- **System data schema v1.8.0 → v1.9.0**: CHECK price > 0 (Q3). New `promotion_use_reservations` with one active reservation per quote, and lifecycles split by source (Q6, Q29, Q30). Configuration-version note (Q14). Travel copy-source and review-flag columns (Q17, Q18). No itineraries table (Q21).
