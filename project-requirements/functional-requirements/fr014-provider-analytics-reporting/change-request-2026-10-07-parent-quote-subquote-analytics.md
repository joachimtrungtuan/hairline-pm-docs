# Change Request: Parent Quote and Accepted Subquote Analytics

**Change Request ID**: CR-FR014-20261007-01
**Primary FR**: FR-014
**Triggering FR / Event**: SRC-MTG-002 quote-option decisions, refined FR-004/FR-005/FR-006 contracts, and approved FR-014 analytics restructure
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-06
**Decision Date**: 2026-10-07
**PRD Version Change**: v3.6 to v3.7
**Related Commit(s)**: Pending — no commit requested for this change

---

## Decision Summary

FR-014 now distinguishes parent provider responses, package/date-price Subquotes, inquiry-level conversion, immutable patient acceptance, and payment-confirmed bookings. Multiple parents from one provider are legitimate responses, but neither those additional parents nor their alternatives may inflate inquiry response rates or funnels. Amount analytics use only the exact accepted subquote price, as required by FR-004; pending-payment risk additionally requires a valid FR-006 hold.

The Product Owner approved replacing offered-price-bracket conversion with accepted-price distribution and allowing formula/metric-label-only corrections to the locked cockpit. Screen 1 layout, sections, widget count, chart types, filters, and responsive behavior remain locked. This request approves documentation, not implementation readiness or consolidated FR verification.

## Baseline State

**Source version**: FR-014 v3.6, Screen 1, Screen 2, Screen 5, Screen 8, Screen 12, Screen 13, Dependencies, and Key Entities

- Quote metrics assumed a flat quote amount and status. Parent responses were not distinguished from packages/date alternatives in the reporting contract.
- Provider response rate divided quotes submitted by inquiries distributed, allowing multiple parent responses to inflate the rate beyond 100%.
- Funnel wording called captured payment "In progress" and did not consistently distinguish inquiry, parent-quote, and booking grains. Patient journey used payment creation rather than the booking-confirming capture.
- Accepted-but-unpaid aging used flat quote accepted_at/status without the accepted selection or actual hold deadline.
- Price averages, benchmarks, outliers, and conversion by price bracket assumed one amount for every submitted quote, contradicting the revised FR-004 accepted-price-only rule.
- Dependencies omitted FR-005 AcceptanceEvent; aggregates, detailed exports, and financial joins lacked an explicit immutable selected-subquote boundary.

## Approved State

**Target version**: [FR-014 v3.7](prd.md), Analytics Counting & Time Basis, Screens 1–9/12–13 and Screen 10 conversion label, Analytics Data Contract and Legacy Compatibility, User Scenarios & Testing, Shared Quote / Acceptance Analytics, and Key Entities

The updated PRD owns the full metric definitions. Stable parent identities drive response volume and parent acceptance rate; distinct distributed inquiry/provider pairs drive provider response rate; platform funnels deduplicate inquiry IDs across providers. AcceptanceEvent owns the selected package/date-price snapshot and accepted aggregate versions. First successful initial payment defines Confirmed booking, and an active payment hold gates cash risk. Accepted-price observations exclude unaccepted parents but retain those parents in volume/rate denominators.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Response volume and acceptance rate | Undifferentiated quote count and Accepted/Quoted | Stable submitted Parent Quote counts and accepted-parent/submitted-parent rate in the same submission cohort; child counts separately labelled | Preserve multiple parent responses without option/version inflation |
| Inquiry response and funnels | Quote submissions divided by distributions; mixed stage units | Distinct distributed inquiry/provider response sets; cumulative inquiry milestones, distinct platform inquiry IDs, explicit cutoff and N/A/unavailable states | Prevent rates above 100% and duplicate provider-to-platform funnel counts |
| TTFQ and journey | First quote wording; payment.created_at journey | Earliest parent first submission per inquiry/provider pair; first successful booking-confirming initial payment per inquiry | Exclude draft/resend clocks, failed attempts, and repeated installment journeys |
| Booking milestone | In progress described captured payment | Existing fifth funnel stage labelled Confirmed booking; In Progress reserved for procedure start | Align FR-006 lifecycle without adding a new screen or funnel stage |
| Pending-payment risk | Flat accepted quote status, timestamp, and amount | Exact accepted selection linked to pending Booking and valid hold; acceptedAt age, actual deadline, accepted total price, cancellation/supersession/expiry exclusions | Prevent expired reservations and stale quote caches from appearing as active risk |
| Pricing and benchmarks | One amount for every submitted quote | Accepted subquote total price/promotion/currency from immutable snapshot; accepted-sample eligibility and historical FX provenance | Implement FR-004 REQ-004-030 without inventing unaccepted parent prices |
| Price-bracket conversion and scatter | Offered-price conversion and claims about price effects | Accepted counts/shares by price bracket; descriptive scatter of accepted prices vs parent acceptance rate, with matching cohort and no causal claim | Accepted-only prices cannot establish offered-price conversion probability |
| Financial joins | No explicit protection against hierarchy fan-out | Owning financial records counted once before read-only accepted-selection joins | Avoid multiplying revenue, refunds, deductions, or payouts |
| Reporting data and exports | Flat quote IDs and mixed aggregate fields | FR-005/FR-006 provenance, separate grains, equal accepted versions, immutable accepted-price observation, consistent PDF/CSV/scheduled definitions | Make dashboards and exports auditable against the exact patient selection |
| Screen 1 lock | Entire screen specification frozen | Product Owner metric-only exception for TTFQ, funnel and aging; layout and presentation structure still locked | Correct changed contracts while preserving the accepted cockpit design |

## Scope and Impact

### In Scope

- FR-014 metric definitions, affected screen labels/formulas, requirements summary, dependencies, target reporting entities, and acceptance scenarios.
- Accepted-price-only distributions/benchmarks/outliers and the approved replacement of Screen 13 Widget 4.
- Formula/metric-label-only cockpit exception; existing screen/widget structure and numerical sample/hold policies remain unchanged.
- FR-local Change Request, source-register incorporation note, and required update-log traceability.

### Out of Scope

- Product code, schema migrations, implementation tasks, live analytics QA, and commits/pushes.
- Further changes to FR-004/FR-005/FR-006 or FR-008, FR-015, and system PRD/schema/spec documents.
- Full offered-option price analytics or offered-price-bracket conversion; these need separate approval.
- Meeting 01, fund-release/payment-routing redesign, commission/fee/deposit/installment/payout policies, or binary travel-path changes.
- Cockpit redesign, additional screens/widgets, changed permissions, or a premature consolidated verification sign-off.

### Affected Contracts

- **PRD owner**: [FR-014](prd.md) — affected existing requirements and new REQ-014-105 through REQ-014-112.
- **Related FRs**: [FR-004](../fr004-quote-submission/prd.md) — parent/option hierarchy and REQ-004-030 accepted-price-only amounts; [FR-005](../fr005-quote-comparison-acceptance/prd.md) — immutable AcceptanceEvent, selected Subquote and REQ-005-017 through REQ-005-020; [FR-006](../fr006-booking-scheduling/prd.md) — confirmation, hold expiry and Booking lifecycle; FR-007/FR-017 retain financial ownership; FR-015 remains the provider drill-down destination.
- **System documents**: No edits in this step. Existing schema/spec reporting mappings must be assessed later; legacy flat fields alone do not establish compliance with the revised contract.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed in this documentation operation; the previous verified PRD baseline does not verify these new formulas or payloads.
- **Required assessment**: Analytics API queries, distinct/cohort aggregation, first-submission history, AcceptanceEvent and Booking linkage, confirmation/hold events, price/FX provenance, cached/materialized metrics, benchmarks, financial joins, drill-down filters, PDF/CSV, and scheduled exports.
- **Compatibility / rollout risk**: Changing metric units and accepted-only samples can alter historical charts and thresholds. Old/new aggregates must not be combined silently; recompute from canonical provenance or mark missing observations unavailable. Repeated events must be idempotent, and expired holds must disappear from active risk despite stale status caches.
- **Data migration**: To be assessed. Existing reporting aggregates or exports may need recomputation; historical accepted price must not be guessed from current package/alternative data. No migration or system-wide schema update is approved by this document alone.

## Acceptance and Validation

- Two parent responses containing six packages/twelve date-price Subquotes and one acceptance produce two responses, a 50% parent acceptance rate, a 100% inquiry response rate for one distributed inquiry, and one accepted-price observation.
- A platform inquiry distributed to multiple providers counts once per funnel stage; provider stages remain scoped to their own response/acceptance.
- Drafts, edits, resends, new alternatives, and redelivered events do not inflate first-response counts or observations; rates use matched cohorts and explicit cutoff/sample basis.
- Confirmed booking and journey require successful initial payment; procedure In Progress and later installments remain distinct.
- Active pending-payment risk excludes cancelled, superseded, expired-hold, and Payment Window Expired selections without deleting acceptance history or reopening quotes.
- Pricing uses immutable accepted package/date price, promotion, currency, and locked-rate provenance; unaccepted parents remain denominator/volume records but have no amount observation.
- Accepted-price brackets show distributions, not artificial 100% conversion; scatter text is descriptive, and outlier samples count accepted selections.
- Financial amounts remain owning-record totals, unaffected by alternative counts. Screens, benchmarks, drill-downs, and exports use the same metric contract.
- Documentation checks cover links, requirement IDs, Markdown tables, preserved cockpit structure, and the PRD/CR/source-register/update-log chain. Live/backend reconciliation tests are still required before Implementation Reconciliation can become Verified.

## Approval and Traceability

- **Requested by**: Product Owner, Joachim Trung Tuan.
- **Approved by**: Product Owner, Joachim Trung Tuan, 2026-10-07; documentation delta only.
- **Decision evidence**: [SRC-MTG-002](../../sources/meetings/meeting-02-launch-quote-options-fund-release-and-payments.md), MTG-002-D03–D06 and O01 with Product Owner refinements; FR-004 REQ-004-030; FR-005 REQ-005-020; FR-006 General Module Rules / Payment & Billing Rules / Booking entity. The Product Owner's approval was "Please update as per your suggestions," accepting the FR-014 proposal, accepted-price-bracket replacement, and metric-only cockpit exception.
- **PRD change log**: [FR-014 Appendix: Change Log](prd.md#appendix-change-log), v3.7 row dated 2026-10-07.
- **Update log**: [FR014_PARENT_QUOTE_SUBQUOTE_ANALYTICS_2026-10-07.md](../../update-logs/2026-10-07/FR014_PARENT_QUOTE_SUBQUOTE_ANALYTICS_2026-10-07.md).
- **Supersedes**: None as a Change Request; explicitly revised v3.6 analytics definitions are superseded by v3.7.
- **Superseded by**: None.
