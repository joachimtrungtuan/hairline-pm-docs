# FR-014 Parent Quote and Accepted Subquote Analytics

**Date**: 2026-10-07
**Update Type**: Major requirement alignment
**PRD Version**: FR-014 v3.6 → v3.7
**Decision Status**: Documentation approved by Product Owner
**Implementation Reconciliation**: Required — not assessed
**Consolidated Verification**: Pending the remaining controlled FR revisions
**Change Request**: [CR-FR014-20261007-01](../../functional-requirements/fr014-provider-analytics-reporting/change-request-2026-10-07-parent-quote-subquote-analytics.md)

## Decision and Evidence

The Product Owner approved the FR-014 proposal with "Please update as per your suggestions." The decision includes accepted-price distribution replacing offered-price-bracket conversion and a formula/metric-label-only exception to Screen 1's lock; its existing layout, sections, chart types, filters, and widget count remain unchanged.

Evidence owners are [Meeting 02](../../sources/meetings/meeting-02-launch-quote-options-fund-release-and-payments.md), MTG-002-D03–D06 and O01 with Product Owner refinements; [FR-004](../../functional-requirements/fr004-quote-submission/prd.md), REQ-004-030; [FR-005](../../functional-requirements/fr005-quote-comparison-acceptance/prd.md), REQ-005-017 through REQ-005-020 and AcceptanceEvent; and [FR-006](../../functional-requirements/fr006-booking-scheduling/prd.md), General Module Rules, Payment & Billing Rules, and Booking lifecycle.

## Changes

- Parent responses count stable first-submitted parent IDs; alternatives and revisions do not inflate volume. Parent acceptance, distinct-inquiry response, and inquiry funnel metrics have separate matched cohorts, cutoffs, and denominator rules.
- Funnels retain five stages but identify successful initial payment as Confirmed booking, not procedure In Progress. TTFQ and patient journey use first submission and first successful booking-confirming payment respectively.
- Active pending-payment aging uses immutable AcceptanceEvent time, selected price, Booking state, and actual hold deadline; cancellation, supersession, hold expiry, and Payment Window Expired remove active risk without deleting historical selection.
- Price means the immutable accepted package/date total, including accepted promotion/currency/FX provenance. Unaccepted parents remain in response/rate metrics, not amount statistics. Price-bracket widgets show accepted distributions; scatter and outliers are descriptive and use accepted samples.
- Reporting contracts add FR-005 provenance, equal accepted aggregate versions, distinct-grain aggregates, immutable accepted-price observations, financial-record deduplication, and consistent benchmarks/drill-downs/PDF/CSV/scheduled exports.
- Required reconciliation scenarios cover multiple parents/providers/alternatives, event retries, cohort boundaries, failed initial payments, hold expiry, immutable historical prices, and sample eligibility. Current deployment compliance is not asserted.

## Files Changed

- [FR-014 PRD](../../functional-requirements/fr014-provider-analytics-reporting/prd.md)
- [FR-014 Change Request](../../functional-requirements/fr014-provider-analytics-reporting/change-request-2026-10-07-parent-quote-subquote-analytics.md)
- [Source register](../../sources/source-register.md) — records only this analytics incorporation
- [Update-log index](../README.md) and this entry

## Validation and Boundaries

- Focused documentation validation passed across the five changed files: 27 local links/anchors resolve; 70 Markdown tables have consistent columns; requirements 033–112 are unique and complete, with the existing Screen 1 range 001–032 preserved. All 13 screens remain present, and comparison against the task's PRD diff confirms the cockpit's headings, chart types, aging buckets, layout, global UX, and filter definitions are unchanged. Active superseded formulas were checked; `git diff --check` is clean. These are structural/contract checks, not deployed analytics proof.
- No implementation code, schema migration, other FR PRDs, or system PRD/schema/spec edited for this change.
- No commits or pushes requested or performed. Existing unrelated pending changes are preserved.
- The documentation-maintenance workflow kept the owning PRD, Change Request, source traceability, and required log synchronized; it did not invoke a consolidated verify-fr pass.
- Implementation reconciliation must assess queries, event/cohort mappings, cached aggregates, historical accepted/FX provenance, financial joins, exports, and regressions before status can become Verified. Missing history must be surfaced rather than reconstructed from mutable alternatives.
