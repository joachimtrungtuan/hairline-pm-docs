# MTG-002 Quote Model — Fix Plan (2026-10-16)

## 1. Header

| Field | Value |
|---|---|
| Status | Approved by Product Owner 2026-10-16 (revision 2). Executed 2026-10-16: Waves 0–4 and final light audit complete; Product Owner Q-series Q1–Q30 applied 2026-10-16; consolidated verification and final audit complete 2026-10-18 (Q31–Q44 applied). |
| Date | 2026-10-16 (Asia/Saigon) |
| Inputs | [Verification report](mtg002-quote-model-verification-2026-10-16.md) (sections 4, 5, 7, 8, Appendix B); [Decision log](mtg002-quote-model-decisions-2026-10-16.md) (authoritative: D1 to D24, D6-M, R7-1 to R7-4, M1 to M17, P1 to P3); project `CLAUDE.md` (Template and Requirement Change Control, Update Log Protocol, Navigation and Token Governance, File and Folder Rules) |
| Scope | Quote/subquote data model: parent quote, Quote Option, option × date-range price row (subquote), AcceptanceEvent and snapshot, slot hold, booking handoff, `Payment Window Expired` (PWE), and the consumers and system documents that read them |
| Edited paths | `functional-requirements/frNNN-*/prd.md`, one new CR beside each of 17 PRDs, existing CR status lines, `system-prd.md`, `system-data-schema.md`, `system-technical-spec.md`, one update log and its README |

**Non-goals.** Payment rails, fund release, refund mechanics, later-instalment handling, Meeting 03 and every item in report section 8 stay out. Two decided statements are in scope: the D6-M placeholder (paid money follows the patient as credit, unused money is refunded, no patient fees, mechanics TBD in the payment pass) and the D1 boundary (PWE applies only to acceptance → deposit or first instalment; missed later instalments never cause PWE or inquiry cancellation). Nothing under `main/`, `project-automation/` or `templates/` is edited.

**Where the decision log overrides the report.** D2 (audited admin revive with a fresh hold), D3 and D6 (provider fault after acceptance is an admin direct transfer in the same inquiry with a new linked acceptance record), D13 (commission field shows model and value), D17 and M1 (a package seeds one option; subquotes number up to options × date ranges), D22 (`quote.withdrawn` always mandatory), M2 (snapshot governs money fields only; treatment details stay correctable through FR-010) and M7 (no held figure in FR-014).

**Line citations.** Line numbers marked `fr006:661` were re-grepped on 2026-10-16. Locations marked "re-grep" could not be confirmed by phrase search and must be located by the fixer before editing.

## 2. Waves and parallelism

The order follows R7-4. Each wave ends with the section 4 checks.

| Wave | Files | Agents | Ordering inside the wave |
|---|---|---|---|
| 0 | Update log file (P3) | Controller | Create the combined log with links to the three reports before Wave 1. |
| 1 | FR-005, FR-006 | 2 | Parallel. |
| 2 | FR-004, FR-019, FR-024 | 3 | Parallel, against the Wave 1 result. |
| 3 | FR-007, FR-007b, FR-008, FR-010, FR-014, FR-015, FR-017, FR-020, FR-022, FR-026, FR-029, FR-030 | Up to 12 | Parallel, except FR-020 starts after FR-030 because it mirrors the FR-030 event catalogue. |
| 4 | `system-prd.md`, `system-data-schema.md`, `system-technical-spec.md` | 3 | Parallel; each reads the final FR text. |

**File ownership.** One agent owns one FR folder (its `prd.md`, its new CR and its existing CRs) or one system document. No two agents write to the same file. Cross-FR needs are passed by name in the handoff and fixed in the owning FR's package; for example, FR-006 in Wave 1 refers to "the FR-026 slot-hold duration setting", which FR-026 creates in Wave 3. Only the controller writes the update log and README.

**Standard steps for every FR package.** Before editing, list headings with `rg -n "^#{1,4} "` and re-grep every cited location. After editing, bump the PRD version, add one `## Appendix: Change Log` row citing finding and decision IDs, update the `**Status**` line (for FR-007b, FR-019, FR-022, FR-024 and FR-026, which are currently Verified, the status change is named in the CR), and create `change-request-2026-10-16-mtg002-quote-model-alignment.md` (ID `CR-FRNNN-20261016-01`) from `project-requirements/templates/change-request-template.md` with before state, after state, reason, affected contracts and approvals, keeping documentation approval separate from implementation reconciliation.

**CR rule.** All 17 FRs get a CR (P1). Twelve qualify under the CLAUDE.md major-event rule because they are Verified or change workflow, data, permission or integration contracts; FR-007, FR-008, FR-014, FR-015 and FR-017 get one because their implementation status is unknown (P1). System documents get no CR; the FR CRs list them as affected documents.

## 3. Per-FR work packages

Edit IDs are used in Appendix A.

### Wave 1

#### FR-005 Quote Comparison and Acceptance

**Targets:** `fr005-quote-comparison-acceptance/prd.md` (scope line fr005:47; admin actions fr005:290 and fr005:319; Rule 1 and the hold sentence, re-grep; A3, A4; AcceptanceEvent entity; scenarios); `change-request-2026-09-15-subquote-acceptance-model.md` line 62.

1. **E005-1.** Remove soft-delete and restore of acceptance, parent quote and subquote records (fr005:47, 290, 319) and the undefined "Resolve conflicts"; replace with an audited "Add note or correction" annotation that never alters the event (FR-005-4, D4).
2. **E005-2.** Restate Rule 1 as one patient acceptance per inquiry, with one exception: a D6 provider-fault transfer creates a new admin-authored acceptance record linked to the original. The original is marked superseded by a linked supersession record, not by editing the event (D6, D3, D1, S1-3).
3. **E005-3.** State the PWE recovery route: the accepted subquote is never reopened; the patient cancels and starts a new inquiry (A4 via FR-003) or contacts support for the FR-006 revive (S1-1, D1, D2).
4. **E005-4.** State that acceptance places one fixed hold for the FR-026 duration, keyed by provider, appointment date/time and time zone (S1-2, M3, M4, D14).
5. **E005-5.** Add the FX rate and its timestamp to the snapshot; a cached rate older than 24 hours is used and recorded, with no review state (FR-017-1, D19).
6. **E005-6.** Add the patient promotion-code step before acceptance on one named subquote; the discounted price is shown and frozen into the AcceptanceEvent and never written to the provider's promotion (FR-019-1, D8, D9).
7. **E005-7.** Define the snapshot scope per M2: price, currency, date range, appointment and promotion are the binding money fields; treatment details in the snapshot are the original record, and later changes are made only through FR-010 (M2).
8. **E005-8.** State that a parent quote offers up to options × date ranges subquotes, because providers may omit pairings (M1).
9. **E005-9.** Point A3 to FR-006 for withdrawal after acceptance (S1-3, D3).
10. **E005-10.** Add acceptance-outcome scenarios with FR-020 (FR-020-4, M16, D20, P2).
11. **E005-11.** Correct CR line 62 ("Reconciliation deferred") to reference this pass (R7-1).

**Checks:** no soft-delete or restore of acceptance records; Rule 1 names the D6 exception; snapshot lists the five money fields plus FX rate and timestamp.

#### FR-006 Booking and Scheduling

**Targets:** `fr006-booking-scheduling/prd.md` (settings fr006:657-661; REQ-006-005 fr006:902; admin actions fr006:608-609; fr006:785; PWE rules, B3, B4, Entity 2, REQ-006-010, re-grep); `change-request-2026-09-15-accepted-subquote-handoff.md` line 29.

1. **E006-1.** Replace the "Payment failure hold duration" setting (fr006:661) and REQ-006-005 (fr006:902) with one fixed hold that starts at acceptance and lasts the FR-026 duration (default 48 hours); payment failure never extends it. The setting is the FR-026 one, not "A-09" (S1-2, S2-5, M3, D14).
2. **E006-2.** Define the slot: acceptance places a temporary exclusive hold keyed by provider, appointment date/time and time zone that blocks other patients; the appointment record is created only on successful payment; on expiry the hold is released and no appointment exists (S1-6, M4).
3. **E006-3.** Add the D1 first-payment-only boundary (D1).
4. **E006-4.** Replace "a new current subquote or an audited admin intervention" with the D1 recovery route (S1-1, D1).
5. **E006-5.** Restrict Modify Status and Modify Appointment Date (fr006:608-609, now "Always"). Allowed: revive PWE → `Accepted` with mandatory reason, slot re-check, new hold of the configured duration, promotion re-reservation that fails if the limit is exhausted, audit entry, unchanged AcceptanceEvent, and a mandatory "booking revived" notice to patient (new payment deadline) and provider (slot held again). Date changes also need a slot check. No other status jumps (FR-006-3, D2, D11, M17).
6. **E006-6.** Add the "Provider fault after acceptance" flow modelled on B4: booking closes with cause "provider fault", hold released, AcceptanceEvent kept and superseded through a linked record; admin assigns a replacement provider in the same inquiry with audited elevated rights to adjust package and price, recorded as a new linked acceptance record. Covers withdrawal before treatment and drop-out during treatment (S1-3, D3, D6).
7. **E006-7.** Add the D6-M placeholder inside that flow (D6-M).
8. **E006-8.** Correct fr006:785 ("Discounts/commissions already resolved before booking stage"): promotion is frozen at acceptance, commission is fixed at booking confirmation on the D12 base, and the FR-004 figure is indicative (S2-4, D12, D13, M5).
9. **E006-9.** Name the FR-030 events FR-006 triggers: `quote.withdrawn`, hold expiring soon, PWE, booking revived (S4-1, S4-2, D22, M13, M17).
10. **E006-10.** Update CR line 29 ("An expired payment window is terminal") for the D2 exception.

**Checks:** zero hits for "after payment failure"; no "Always" on status or date edits; hold key names provider, date/time and time zone.

### Wave 2

#### FR-004 Quote Submission

**Targets:** `fr004-quote-submission/prd.md` (Workflow 6 fr004:162; Promotion rows fr004:441 and 526; QuoteOptionDatePrice fr004:673-674; ownership matrix, commission field, expiry capture, Screen 7, status enum, re-grep); `change-request-2026-09-09-quote-options-model.md` lines 95 and 135.

1. **E004-1.** Rewrite Workflow 6 so `accepted → withdrawn` hands over to the FR-006 provider-fault flow instead of re-routing inside FR-004 (S1-3, D3, D6).
2. **E004-2.** Replace the live `promotionId` reference (fr004:441, 526, 674) with promotion terms copied into the sent QuoteVersion at send; store the provider price as entered and the discount separately; the accepted price is post-promotion (FR-004-5, D10, D12, M14).
3. **E004-3.** On acceptance, set unsent draft parents to `cancelled_other_accepted` silently, with no notice (FR-020-2, D5, P2).
4. **E004-4.** Commission field shows model and value (percentage or Flat Rate), labelled "indicative, final at booking confirmation" (S2-4, D13).
5. **E004-5.** Capture expiry and currency at first send, copied read-only from the FR-026 setting; drafts carry neither; no per-quote extension (FR-026-2, D15, M11).
6. **E004-6.** Remove `confirmed` as a quote status (S5-6, D23).
7. **E004-7.** State that an accepted quote never reopens after PWE (S1-1, D1).
8. **E004-8.** Restate seeding: each selected package seeds one alternative option (maximum 5), never summed; the standard price prefills each date-range row; providers may omit a pairing; each option needs at least one range; subquotes number up to options × ranges (FR-024-2, D17, M1).
9. **E004-9.** Define the quote inline edit path: editing inside quote creation produces a quote-local mutated copy saved only on that quote, never written back; the option records source package, version and an inline-customised flag (FR-024-8, M10).
10. **E004-10.** State that after acceptance FR-004 Screen 7 blocks quote edits; treatment-detail changes go through FR-010 (M2, FR-004-4 Minor).
11. **E004-11.** Name the appointment fields (date/time and time zone) as the FR-006 hold key (S1-6, M4).
12. **E004-12.** Correct CR line 95 (system schema "reconciled", tech spec "still open") and line 135 ("remains open and unscheduled") to reference this pass, including the M12 schema additions (FR-004-8, M12, R7-1).

**Checks:** no live `promotionId` pricing; no re-routing in Workflow 6; D13 label exact; no `confirmed` quote status; library and inline edit paths both named.

#### FR-019 Promotions and Discounts

**Targets:** `fr019-promotions-discounts/prd.md` (fr019:21, 71, 126, 754; Application entity fr019:854; usage limits, re-grep); `change-request-2026-09-10-option-date-promotion-alignment.md`.

1. **E019-1.** Patient codes only before acceptance, on one named subquote, creating a patient-side application that never writes to the provider promotion; replace "at quote/booking" (fr019:21, 71) (FR-019-1, D8).
2. **E019-2.** Remove post-acceptance changes: provider swaps, checkout or booking-time code entry, "revalidation on booking" (fr019:754) and admin Void; the only exception is the D6 linked record (FR-019-2, D9).
3. **E019-3.** Promotion terms fixed at send (D10).
4. **E019-4.** Application created at acceptance and linked to the AcceptanceEvent; voided on not-selected, PWE or cancellation (FR-019-3).
5. **E019-5.** Usage limit reserved at acceptance, consumed at first successful payment, released on PWE or cancellation, re-reserved on D2 revive and failing if exhausted (FR-019-4, D11, D2).
6. **E019-6.** Automatic promotions attach at send to every eligible option × date-range row; provider price stays as entered, discount shown separately; add ACs for auto-attachment, acceptance-to-application provenance and rejecting a promotion on a row it was not attached to; add ACs for the CR items (FR-019-7, M14).
7. **E019-7.** Mark the 2026-09-10 CR as superseded in part.

**Checks:** no promotion-change path after acceptance; the four lifecycle verbs appear in one rule.

#### FR-024 Treatment and Package Management

**Targets:** `fr024-treatment-package-management/prd.md` (Usage Count fr024:608; QuoteTreatment entity fr024:961; REQ-024-010/011, US4, package entity, currency fields, Screen 5, re-grep); `change-request-2026-09-10-quote-option-provenance-alignment.md`.

1. **E024-1.** Redefine a package as a full template seeding one option: services with pricing, transport, hotel, flight and other travel services, and a relative-day plan; date range, notes and documents are per inquiry (FR-024-2, D17).
2. **E024-2.** Replace "one treatment plus summed packages" and add-on types with "each selected package is one alternative option, up to 5" (FR-024-2, D17, M1).
3. **E024-3.** Add an included-items/services list to the package entity (FR-024-1, D17).
4. **E024-4.** Remove package and treatment currency (FR-024-3, D18).
5. **E024-5.** Remove QuoteTreatment (fr024:961) as a current record (FR-024-5).
6. **E024-6.** Redefine Usage Count (fr024:608) as Quote Options copied from this package whose parent quote is draft or sent; deactivation warns "used in N open quotes"; remove `quote_packages` (FR-024-6, M8, M10).
7. **E024-7.** Define the library edit path: saving in package management creates a new package version (v1, v2), old versions are read-only, existing quotes never change; contrast it explicitly with the FR-004 inline edit path (FR-024-8, M10, D17).

**Checks:** zero hits for "add-on", `QuoteTreatment`, `quote_packages` except removal notes; versioning and inline paths both stated.

### Wave 3

#### FR-007 Payment Processing

**Target:** `fr007-payment-processing/prd.md` (fr007:148, 744, 987).

1. **E007-1.** Align the no-extension rules with one fixed hold from acceptance; a D2 revive creates a new hold, not an extension (S1-2, M3, D2).
2. **E007-2.** State that the appointment record is created on successful initial payment (M4).
3. **E007-3.** Add the D1 boundary cross-reference and read amount and currency from the snapshot (D1, M2, R7-1).

**Checks:** hold wording identical to FR-006.

#### FR-007b Payment Installments

**Target:** `fr007b-payment-installments/prd.md` (plan total and "accepted quote" wording, re-grep).

1. **E007b-1.** Copy plan total, currency and exchange rate read-only from the accepted snapshot through the booking; the total already includes the accepted promotion and any D8 code; never recomputed; currency shown on instalment screens (FR-007b-2, M15).
2. **E007b-2.** Add the D1 boundary (D1).

**Checks:** no plan amount read from a live quote.

#### FR-008 Travel Booking Integration

**Target:** `fr008-travel-booking-integration/prd.md` (travel-date review flag, re-grep; TravelContext attributes fr008:1042).

1. **E008-1.** Add the flag exit: an admin confirms or corrects travel details, the flag clears, and the action is audited (FR-008-2, D7).
2. **E008-2.** Read the appointment and date range from the snapshot (M2).

**Checks:** flag has an owner and an exit.

#### FR-010 Treatment Execution

**Targets:** `fr010-treatment-execution/prd.md` (fr010:240, 265; identifier lists, override and reassignment rules, scenarios, re-grep); `change-request-2026-09-10-quote-option-consumer-alignment.md`.

1. **E010-1.** Read price, currency, date range, appointment and promotion from the accepted snapshot; reconcile the two identifier lists (FR-010-1, FR-010-2 Minor, M2).
2. **E010-2.** Make FR-010 the only path for post-acceptance changes to plan, clinicians and grafts: clinic or admin only, each change audited, patient notified through an FR-030 event, snapshot unchanged, money fields never changed (FR-010-1, M2).
3. **E010-3.** Replace the "Scheduled Date" calendar column (fr010:265) with relative-day display (FR-010-3, R7-2).
4. **E010-4.** Route provider reassignment and drop-out through the FR-006 provider-fault flow; cite D6-M (FR-010-4, D6, D6-M).
5. **E010-5.** Add scenarios: money read from snapshot, audited treatment edit with patient notice, relative days, drop-out transfer (FR-010-6, M2).

**Checks:** no calendar conversion; treatment edits audited and notified.

#### FR-014 Provider Analytics

**Target:** `fr014-provider-analytics-reporting/prd.md` (fr014:197, 1782).

1. **E014-1.** `bookings_on_day` counts Confirmed and In Progress only; held, PWE and Cancelled never count; no held figure; rename "Booked" to "Confirmed bookings" (FR-014-2, M7).

#### FR-015 Provider Management

1. **E015-1.** Replace "Transaction Amount" with the D12 base (FR-015-1, D12).

#### FR-017 Admin Billing and Finance

**Target:** `fr017-admin-billing-finance/prd.md` (acceptance-time FX review, re-grep; locked rate fr017:492, 1033, 1158; invoice snapshot fr017:702).

1. **E017-1.** Remove any manual-review state for a stale FX rate at acceptance; use the snapshot rate and timestamp (FR-017-1, D19).
2. **E017-2.** Invoices never recalculate promotion after acceptance (FR-019-2, D9).
3. **E017-3.** Align commission base and lock points with D12 and M5 (S2-4).

#### FR-030 Notification Rules Configuration (before FR-020)

1. **E030-1.** Add `quote.withdrawn`, mandatory before and after acceptance (S4-1, D22).
2. **E030-2.** Add a patient "hold expiring soon" reminder (lead time from FR-026) and a mandatory PWE notice to patient and provider (S4-2, M13).
3. **E030-3.** Add a mandatory "booking revived" notice to patient and provider (M17).
4. **E030-4.** Add a patient notice for post-acceptance treatment-detail changes made through FR-010 (M2).
5. **E030-5.** Lock the selected and not-selected provider outcomes of `quote.accepted` (S4-3, D21).
6. **E030-6.** One provider notice per sent parent quote; drafts get none (FR-020-1, D20, P2).
7. **E030-7.** Money variables come from the snapshot; add allowlists (S4-5, M2).
8. **E030-8.** Replace `quote.total_amount` with "From" lowest subquote price, option count, treatment and expiry in the new-quote notice; exact prices only after acceptance, from the snapshot (FR-030-3, M9).

#### FR-020 Notifications and Alerts (after FR-030)

1. **E020-1.** Mirror E030-1 to E030-8 (S4-1, S4-2, S4-3, D20 to D22, M13, M17).
2. **E020-2.** Add the recipient matrix for a provider with several parents (FR-020-1, D20).
3. **E020-3.** State that D5-cancelled drafts trigger no notice (FR-020-2, P2).
4. **E020-4.** Add a user story: selected provider, same-provider sibling, competing provider without winner identity or price, and no `quote.declined` emitted (FR-020-4, M16).

#### FR-022 Search and Filtering

**Target:** `fr022-search-filtering/prd.md` (fr022:962; quote filters, re-grep).

1. **E022-1.** Quote filters use the exact FR-004 statuses, including Cancelled (Provider Status) (FR-022-2, M6).
2. **E022-2.** Booking filter uses the exact FR-006 states (Accepted, Payment Window Expired, Confirmed, In Progress, Aftercare, Completed, Cancelled); remove "Pending Payment" (FR-022-3, M6).
3. **E022-3.** No `confirmed` quote status (D23).

#### FR-026 App Settings and Security

**Target:** `fr026-app-settings-security/prd.md` (fr026:251-255, 352; Screen 5d fr026:619).

1. **E026-1.** Add a versioned, audited slot-hold duration (default 48 hours) and a "hold expiring soon" lead time (for example 12 hours) (S2-5, D14, M13).
2. **E026-2.** Replace "when a new parent Quote is created" (fr026:255): expiry and currency are copied read-only at first send; later changes never affect sent quotes (FR-026-2, D15, M11).
3. **E026-3.** Seed Quote Configuration with FR-029 Default Currency as the single setting (FR-026-3, D16).

#### FR-029 Payment System Configuration

**Target:** `fr029-payment-system-config/prd.md` (Rule 1 fr029:727; "booking total", re-grep).

1. **E029-1.** Rewrite Rule 1 with named lock points: exchange rate at subquote acceptance; commission and deposit/instalment settings at booking confirmation; nothing at quote creation (FR-029-1, M5).
2. **E029-2.** Define "booking total" as the D12 base (FR-029-2, D12).
3. **E029-3.** FR-004 shows an indicative model and value only (S2-4, D13).

FR-014, FR-015 and FR-017 checks: status lists match FR-006; base sentence matches FR-029.

### Wave 4

#### system-prd.md

1. **ESP-1.** Align the FR-004, FR-005, FR-006, FR-010, FR-019 and FR-024 sections with final FR wording: fixed hold and hold key, appointment at payment, D1 boundary, D2 revive, D6 transfer, D4, promotion lifecycle, D17/M1 package model, M2 snapshot scope, relative days (R7-1, R7-2, M2 to M4).

#### system-data-schema.md

1. **ESC-1.** Add `acceptance_events` (snapshot money fields, FX rate and timestamp, promotion, author type, supersession link and cause) and `bookings` (hold key, hold start, hold expiry, status; appointment created on payment) (S5-1, S5-3, D24, D6, D19, M4).
2. **ESC-2.** Add PWE and the `accepted → cancelled_inquiry_cancelled` transition (S5-3).
3. **ESC-3.** Add `quotes.version`, `quote_versions` and `quote_audits`, and accepted-total and locked-rate fields or a pointer to the snapshot (S5-5, M12).
4. **ESC-4.** Remove `confirmed`; reconcile `rejected` with FR-004 (S5-6, D23).
5. **ESC-5.** Rewrite section 9 "Packages (Provider-Created Add-Ons)" and section 10 to the versioned template model without currency; options record source package, version and inline flag (FR-024-8, D17, D18, M10).
6. **ESC-6.** Drop "customizable" from `expiration_hours` (FR-026-4, M11).

#### system-technical-spec.md

1. **ETS-1.** Line 148: acceptance holds the slot; the slot is blocked only after successful payment (S5-4, M3).
2. **ETS-2.** Lines 165-174: replace `$quote->treatment_date` and `$quote->quote_amount` with snapshot or booking money fields; instalment arithmetic stays parked (S5-2, M2).
3. **ETS-3.** Add hold and PWE handling; remove `confirmed` (S5-3, S5-6).

### Minors and Observations checklist (R7-3: verify before applying)

Each agent re-checks every item and skips wrong ones, recording the reason. IDs from report Appendix B and section 5.

- **FR-004:** FR-004-1, 4, 6, 7, 8 to 12, 14; FR-004-15 (O); FR-024-7; S4-6.
- **FR-005:** FR-005-7 to 11; FR-005-12, 13 (O); S1-4, S1-5, S1-10.
- **FR-006:** FR-006-5, 6, 7; FR-006-9, 10 (O); S1-9.
- **FR-007:** FR-007-3, 4. **FR-007b:** FR-007b-1, 3, 5, 6; FR-007b-7 (O).
- **FR-008:** FR-008-1, 3 to 8; FR-008-9 (O). **FR-010:** FR-010-7, 8; FR-010-9 (O).
- **FR-014:** FR-014-3; FR-014-4 (O). **FR-015:** FR-015-2 to 4; FR-015-5, 6 (O).
- **FR-017:** FR-017-4 to 6; FR-017-7 (O, payment part parked). **FR-019:** FR-019-6, 9; O1.
- **FR-020:** FR-020-7; FR-020-9 (O); S4-7, S4-13. **FR-022:** FR-022-1, 4 to 7; FR-022-8, 9 (O).
- **FR-024:** FR-024-4, 9 to 13; FR-024-14 (O). **FR-026:** FR-026-5 to 8; FR-026-9 (O); S2-6.
- **FR-029:** FR-029-4 to 6; FR-029-7, 8 (O). **FR-030:** FR-030-7; S4-8 to S4-12; S4-14 (O).
- **Cascade owners:** S3-6 to S3-8; S3-9 (O). **System docs:** S5-7 to S5-12; S2 O1, O2.

## 4. Cross-FR consistency checks (after each wave)

The controller runs these with `rg -n -m 20` on edited files only.

1. **C1 Hold.** One fixed hold from acceptance for the FR-026 duration, keyed by provider, date/time and time zone; never extended by payment failure; appointment created on payment. Zero hits for "after payment failure".
2. **C2 Snapshot scope (M2).** Downstream FRs read price, currency, date range, appointment and promotion from the snapshot only; plan, clinicians and grafts change only through FR-010 with audit and patient notice; the snapshot is never edited.
3. **C3 Status enums.** Quote statuses identical across FR-004, FR-005, FR-022, FR-030 and the schema, with no `confirmed`; booking states identical across FR-006, FR-014, FR-022 and the schema.
4. **C4 Subquote.** One option × date-range row; up to options × ranges; one package seeds one option; never summed.
5. **C5 Relative days.** No calendar-date conversion of plan days.
6. **C6 Promotion.** Fixed at send, frozen at acceptance; only the D6 linked record changes it.
7. **C7 Commission.** One D12 base sentence and the M5 lock points in FR-015, FR-017, FR-029 and the schema; FR-004 and FR-006 say "indicative".
8. **C8 PWE scope.** The D1 boundary is stated in FR-006 and referenced in FR-007 and FR-007b.
9. **C9 Provider fault.** FR-004, FR-005, FR-006, FR-010 and the schema describe the same D6 linked-record transfer and cite D6-M.
10. **C10 Events.** FR-020 and FR-030 list the same events, locks and grain, including hold expiring soon, PWE, booking revived and the FR-010 treatment-change notice.
11. **C11 Edit paths (M10).** FR-004, FR-024 and the schema distinguish library versioning from quote-local inline copies.

## 5. Update-log plan (P3)

One combined major log, `local-docs/project-requirements/update-logs/2026-10-16/MTG002_QUOTE_MODEL_ALIGNMENT_2026-10-16.md`, follows the `{REPORT_TYPE}_{YYYY-MM-DD}.md` pattern (for example `FR015_VERIFICATION_FIXES_2026-10-15.md`). In Wave 0 the controller creates it with links to the verification report, decision log and this plan. After each wave it appends the FR and system-document edits applied, skipped Minors with reasons, new CRs, and version and status changes. The README at `local-docs/project-requirements/update-logs/README.md` gets a 2026-10-16 date section, entries under the existing Quick Reference categories covering quotes and booking, promotions, notifications, settings and system documents, and a new "Last Updated". Later same-day corrections append bullets.

## 6. Final verification and definition of done

After Wave 4 the controller runs a light audit with one read-only agent per FR and per system document. Each gets the decision log, its edit list and checks C1 to C11, reads by section only, and reports Pass, Fail with location, or Skipped Minor with reason.

Done means: every edit ID is applied or skipped with a stated reason; C1 to C11 pass; every Critical and Major finding and every decision in Appendix A has an applied edit; 17 CRs exist, each PRD has a Change Log row and version bump; the stale CR lines in FR-004, FR-005, FR-006, FR-010 and FR-019 are corrected; the combined log and README entries are complete. Status lines stay at revised, pending consolidated verification, which is a separate step.

## 7. Risks and rollback

| Risk | Likelihood and impact | Mitigation |
|---|---|---|
| Cited locations have drifted (several report lines did not match on 2026-10-16) | High, low | Re-grep before every edit; "re-grep" locations flagged. |
| M2 read as "snapshot for everything" or "live for money" | Medium, high | E005-7, E010-1, E010-2 and check C2 name the five money fields. |
| FR-020 and FR-030 drift | Medium, high | FR-030 first, FR-020 mirrors, check C10. |
| "Marked superseded" mutates the AcceptanceEvent, breaking D4 | Medium, high | Linked supersession record in E005-2 and ESC-1. |
| Verified FRs lose Verified status | Certain, medium | Named in each CR. |
| A wrong Minor is applied | Medium, low | R7-3 verify-first and skip log. |
| Scope creep into payment mechanics | Medium, medium | Only D6-M and D1 statements allowed. |

**Rollback.** Before each wave the controller checkpoints the files that wave owns (a commit in the nested `local-docs` repository if the PO approves, otherwise a copy outside `backups/`). Each FR has one owner, its own CR and Change Log row, so one FR can be reverted alone; reverting a Wave 1 or 2 FR requires re-running C1 to C11 on its consumers.

## 8. Unresolved questions

1. The plan reads D6 "marked superseded" as a separate linked supersession record, so the original AcceptanceEvent is never edited (consistent with D4). The PO should confirm this reading during review; no other question remains open.

## Appendix A. Traceability

| Finding or decision | Edits |
|---|---|
| FR-004-5, D10 | E004-2, E019-3, ESC-3 |
| FR-005-4, D4 | E005-1 |
| FR-006-3, D2 | E006-5, E007-1, E019-5 |
| FR-007b-2, M15 | E007b-1 |
| FR-008-2, D7 | E008-1 |
| FR-010-1, FR-010-6, M2 | E010-1, E010-2, E010-5, E005-7, E004-10, E030-4, E008-2 |
| FR-010-3, R7-2 | E010-3 |
| FR-010-4, D6 | E010-4 |
| FR-014-2, M7 | E014-1 |
| FR-017-1, D19 | E005-5, E017-1, ESC-1 |
| FR-019-1, D8 | E005-6, E019-1 |
| FR-019-2, D9 | E019-2, E017-2 |
| FR-019-3, FR-019-4, D11 | E019-4, E019-5 |
| FR-019-7, M14 | E019-6, E004-2 |
| FR-020-1, D20 | E030-6, E020-2 |
| FR-020-2, D5, P2 | E004-3, E020-3, E030-6 |
| FR-020-4, M16 | E005-10, E020-4 |
| FR-030-3, M9 | E030-8 |
| FR-022-2, FR-022-3, M6 | E022-1, E022-2 |
| FR-024-1, FR-024-2, FR-024-5, D17, M1 | E024-1 to E024-3, E024-5, E004-8, E005-8, ESC-5 |
| FR-024-3, D18 | E024-4, ESC-5 |
| FR-024-6, M8 | E024-6 |
| FR-024-8, M10 | E024-7, E004-9, ESC-5 |
| FR-026-2, D15 | E004-5, E026-2 |
| FR-026-3, D16 | E026-3 |
| FR-026-4, M11 | E026-2, ESC-6 |
| FR-029-1, M5 | E029-1, E017-3, E006-8 |
| FR-029-2, D12 | E029-2, E015-1, E017-3 |
| S1-1, D1 | E005-3, E006-3, E006-4, E004-7, E007-3, E007b-2 |
| S1-2, M3, D14 | E005-4, E006-1, E007-1, E026-1 |
| S1-3, D3, D6, D6-M | E004-1, E005-2, E005-9, E006-6, E006-7, E010-4 |
| S1-6, M4 | E006-2, E004-11, E007-2, ESC-1 |
| S2-4, D13 | E004-4, E006-8, E029-3 |
| S2-5 | E006-1, E026-1 |
| S4-1, D22 | E030-1, E020-1, E006-9 |
| S4-2, M13 | E030-2, E026-1, E020-1 |
| S4-3, D21 | E030-5, E020-1 |
| S4-5, M2 | E030-7 |
| S5-1, S5-3, D24 | ESC-1, ESC-2, ETS-3 |
| S5-2, M2 | ETS-2 |
| S5-4, M3 | ETS-1 |
| S5-5, M12 | ESC-3, E004-12 |
| S5-6, D23 | E004-6, E022-3, ESC-4, ETS-3 |
| M17 | E006-5, E030-3, E020-1 |
| P1 | CR rule in section 2 (17 CRs) |
| P3 | Section 5, Wave 0 |
| R7-1 | E006-1 to E006-4, E022-1, E022-2, E007b-1, E029-1, E030-2, Wave 4, E005-10, E010-5, E019-6, E020-4, stale CR edits, Minors |
| R7-3, R7-4 | Minors checklist; wave order in section 2 |
