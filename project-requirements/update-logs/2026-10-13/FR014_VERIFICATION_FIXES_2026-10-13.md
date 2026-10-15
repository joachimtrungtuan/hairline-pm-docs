# FR-014 Verification Fixes and FR-026 Analytics Configuration

**Date**: 2026-10-13
**Update Type**: Major requirement alignment (verification fixes)
**PRD Versions**: FR-014 v3.7 → v3.8 → v3.9 → v3.10 → v3.11; FR-026 v1.8 → v1.9 → v1.10; FR-030 v1.6 → v1.7 → v1.8; FR-020 v2.1 → v2.2 → v2.3; FR-003 v2.5 → v2.6; system PRD FR-014 section synced
**Decision Status**: Documentation approved by Product Owner
**Implementation Reconciliation**: Required — not assessed
**Change Requests**: [CR-FR014-20261007-01](../../functional-requirements/fr014-provider-analytics-reporting/change-request-2026-10-07-parent-quote-subquote-analytics.md) (amended twice); [CR-FR014-20261013-02](../../functional-requirements/fr014-provider-analytics-reporting/change-request-2026-10-13-export-history-accessibility.md) (new); [CR-FR026-20261013-01](../../functional-requirements/fr026-app-settings-security/change-request-2026-10-13-analytics-configuration.md) (new)

## Decision and Evidence

A verify-fr pass on FR-014 v3.7 found four critical issues. The Product Owner chose a resolution for each: Issue 1, option 1; Issue 2, option 3 (also amend the latest CR); Issue 3, option 1; Issue 4, option 2. The Product Owner also set the default TTFQ SLA target to 120 minutes and chose to keep the target monthly commission line hidden until a target is set. In a second pass the Product Owner chose option 1 for every medium and minor issue (5–15), asked for the FR-026 Screen 1 gap to be fixed, asked for the recalculation rule to be defined in the change request, and asked for the 4-stage funnel to be synced into the system PRD.

## Changes

- **Flat-rate commission (Issue 1)**: Flat-rate commission is now recognised once per completed procedure (FR-010 completion), regardless of price, number of payments, or installments, matching FR-015. Percentage commission stays per completed payment. Updated Screen 4 calculation, Screen 7 C2, Screen 12 Widget 2, the fixed commission logic, REQ-014-051, and the FR-010 dependency.
- **Qualified stage removed (Issue 2)**: FR-003 and the schema have no spam or qualification data. The provider and platform funnels are now Inquiries → Quoted → Accepted → Confirmed booking, and the trend charts drop Qualified %. Updated Screen 1 B1/B4 (a further lock exception; section and widget counts unchanged), Screen 7 B1, Screen 9 trend, counting rules, FR-003 dependency, REQ-014-001, and Entity 1. Recorded as a 2026-10-13 amendment to CR-FR014-20261007-01.
- **No-show source (Issue 3)**: Screens 2 and 11 now take no-shows from FR-010 case closures with closure reason `No-show` and cancellations from post-confirmation FR-006 cancellations. A booking closed as No-show counts once, as a no-show. The "cancellation rate only" fallback is removed.
- **Analytics settings owner (Issue 4)**: FR-026 now owns a versioned Analytics Configuration (Screen 5e, workflow A8, User Story 9, REQ-026-012g, REQ-026-028, REQ-026-029, Entity 12, seeding). Defaults: SLA 120 minutes, At Risk 7 days, Dormant 30 days, price outlier 30%, benchmark refresh Weekly, commission target unset. FR-014 Admin Editability Rules, Assumption 4, Screen 12 Widget 2, and the FR-026 dependency point to it.

### Medium and minor fixes (FR-014 v3.9)

- **Grain (Issue 5)**: Screens 3 and 11 no longer use quote statuses. Completion = FR-010 completed procedures ÷ FR-006 Confirmed bookings by the accepted parent's treatment; aftercare activation joins FR-011 to FR-010 completion; review sub-scores come from FR-013 REQ-013-018a by `treatment_id`.
- **Benchmarks (Issue 6)**: one Shared Benchmark Rule (≥30 inquiries, rolling 12 months, at least 5 providers; direction-aware Green/Amber/Red; TTFQ lower is better; average accepted price uncoloured) used by Screen 2 Widget 7 and Screen 5.
- **Dormant vs. non-responding (Issue 7)**: engagement status stays activity-based with FR-026 thresholds; Screen 7 Tile 5 shows a separate Non-responding count; REQ-014-066 updated.
- **Finance (Issue 8)**: GMV gross, Net GMV = GMV − refunds, net revenue = commission earned (accrual); FR-017 payout status mapping on provider Screen 4 ("Paid date"); Screen 12 Widget 5 uses FR-017 statuses; REQ-014-091 updated.
- **Recurring exports (Issue 9)**: recipients (registered email plus up to 5 permitted team members), previous full period in provider timezone, 3 retries then Failed with manual retry, edit/pause/resume/delete; Entity 8 and REQ-014-062 updated.
- **SLA-breach alert (Issue 11)**: `inquiry.ttfq_sla_breached` (Inquiry, Provider, in-app default) specified in FR-014 and REQ-014-113, registered in FR-030 (source of truth) and mirrored in FR-020.
- **Admin identity and badge (Issue 12)**: Screen 8 scatter and ramp chart show provider names (Rule 14); composite health badge defined, TTFQ-only with low-sample marker under 30 inquiries.
- **Definitions (Issue 13)**: affiliate conversion follows FR-018; seasonality heatmap = weekday average ÷ month daily average × 100.
- **Wording (Issues 10, 14, 15)**: system PRD FR-014 section synced (4-stage funnel, accepted-price metrics, flat-rate commission, FR-026 settings with defaults, net revenue, SLA alert); Estimated Grafts described as a quote estimate, not a clinical outcome; approver name corrected to Joachim Trung Tuan.

### Second verify-fr pass (FR-014 v3.10)

The Product Owner chose: Issue 1 option 3, Issue 2 option 1, Issue 3 option 1, provider-scoped counting (Issue 4), FR-007B labels (Issue 5), a global icons/labels plus contrast rule (Issue 6), and the recommended option for Issues 7–10. New screens or requirements go in a new Change Request.

- **Screen 1 (CR-FR014-20261007-01, amendment 2)**: TTFQ now runs from `inquiry_providers.distributed_at` (matching the SLA-breach alert) across Screen 1, Screen 2, benchmarks, admin TTFQ, the counting rules, and REQ-014-037; a late-distribution scenario was added. The Inquiry Queue keeps only the `New` badge, because `Needs Info` and `Awaiting Price` had no source state.
- **GMV**: Screen 7 C1 and Screen 12 Widget 1 exclude `payment_type = 'refund'` rows.
- **New vs. Returning**: Screen 3 Widget 2 is provider-scoped.
- **Installment health**: Screen 12 Widget 6 and REQ-014-096 use the FR-007B Plan Status labels (Active, Completed, Overdue, Defaulted); FR-007B dependency added.
- **Wording**: Screen 7 single-column breakpoint ≤1024px; benchmark refresh and SLA wording cite FR-026; Screen 12 base currency is the fixed USD base from FR-029 (dependency added); cancellation/no-show drill-downs go to Bookings and Cases lists (Screens 2 and 11); Screen 4 Widget 8 table repaired.
- **New scope (CR-FR014-20261013-02)**: Screen 6 Report History & Recurring Exports sub-section (REQ-014-114) and Accessibility Rules 15C–15E for WCAG 2.1 AA (REQ-014-115).

### Third verify-fr pass (FR-014 v3.11, applied 2026-10-14)

The Product Owner approved 11 decisions on 2026-10-13. For Screen 11 Widget 4, they chose the provider-filter option over the recommended one. The edits were applied on 2026-10-14.

- **Commission**: Commission, net income, and the admin commission charts (Screen 7 C2, Screen 12 Widget 2) use each booking's confirmation-time commission snapshot (FR-015 REQ-015-022, FR-029). Current `provider_commissions` values are used only for payout cadence.
- **Affiliate attribution**: Screen 9 Widget 6 and REQ-014-079 follow the FR-018 `Booking with Affiliate Attribution` entity (Rule 11). A captured affiliate code or referral link counts even when another discount set the final price.
- **Screen 11 Widget 4**: Shows review sub-scores only when one provider is selected, because the FR-013 REQ-013-018a endpoint returns one provider at a time; REQ-014-088 updated. FR-013 was not changed.
- **Payouts**: FR-017 Voided statements are hidden from every provider-facing payout view and export.
- **TTFQ start point**: FR-003 v2.6 now defines `inquiry_providers.distributed_at`.
- **Export delivery**: New `analytics.export_ready` event (System/Operations, Provider, email + in-app) in FR-030 v1.8, mirrored in FR-020 v2.3. FR-014 Screen 6 and S-03 now reference it.
- **Access control**: Rule 15F adds a default role-by-screen matrix (Screens 1–6) for the FR-009 provider roles, on top of Rules 15A and 15B.
- **Scope**: REQ-014-047 and the Screen 3 age conditional were removed; the requirement ID is kept.
- **Finance widgets**: Screen 4 adds a net income tile. The installment adoption rate is now defined at booking level (REQ-014-051, REQ-014-053).
- **Benchmarks**: Percentile bands are shown on both Screen 2 Widget 7 and Screen 5.
- **Completeness**: New Implementation Notes section (pipeline, caching, security and audit, scalability) and business-impact criteria SC-014 to SC-016.

### FR-026 follow-up (v1.10)

- Screen 1 App Data list now includes Quote Configuration (active ISO 4217 currency, default expiry hours).
- Explicit recalculation rule in Screen 5e, REQ-026-029, FR-014 Admin Editability Rules, and CR-FR026-20261013-01: live views recalculate every displayed period with the active version (past periods are not frozen); aggregates record the version; generated exports are never rewritten.

## Files Changed

- [FR-014 PRD](../../functional-requirements/fr014-provider-analytics-reporting/prd.md) — v3.8, v3.9, v3.10, and v3.11, change log and approvals
- [CR-FR014-20261007-01](../../functional-requirements/fr014-provider-analytics-reporting/change-request-2026-10-07-parent-quote-subquote-analytics.md) — Qualified-stage amendment; amendment 2 (TTFQ distribution clock, Inquiry Queue badge)
- [CR-FR014-20261013-02](../../functional-requirements/fr014-provider-analytics-reporting/change-request-2026-10-13-export-history-accessibility.md) — new; Report History UI and accessibility rules
- [FR-026 PRD](../../functional-requirements/fr026-app-settings-security/prd.md) — v1.9 and v1.10
- [CR-FR026-20261013-01](../../functional-requirements/fr026-app-settings-security/change-request-2026-10-13-analytics-configuration.md) — new; amended with the Screen 1 fix and Recalculation Rule
- [FR-030 PRD](../../functional-requirements/fr030-notification-rules-config/prd.md) — v1.7 `inquiry.ttfq_sla_breached`; v1.8 `analytics.export_ready`
- [FR-020 PRD](../../functional-requirements/fr020-notifications-alerts/prd.md) — v2.2 and v2.3, catalog mirrors
- [FR-003 PRD](../../functional-requirements/fr003-inquiry-submission/prd.md) — v2.6, `inquiry_providers.distributed_at` definition
- [System PRD](../system-prd.md) — FR-014 section synced; Last Updated 2026-10-13
- [System Data Schema](../system-data-schema.md) — added entities 35 `treatment_records` (completion and closure reason), 36 `analytics_configurations`, 37 `export_report_configurations`; table list and Last Updated 2026-10-13

## Open Items

- None for documentation. The Product Owner confirmed the recalculation rule (live views recalculate all displayed periods; past periods are not frozen). The three new schema entities are documented from the PRDs and still need implementation reconciliation.
