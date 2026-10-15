# FR-014 Fourth Verification Pass Fixes

**Date**: 2026-10-14
**Update Type**: Major requirement alignment (verification fixes, constitution alignment)
**PRD Versions**: FR-014 v3.11 → v3.12 → v3.13 → v3.14; system PRD FR-014 section synced (v3.12)
**Decision Status**: Documentation approved by Product Owner (2026-10-14)
**Implementation Reconciliation**: Required — not assessed
**Change Requests**: None. These are corrections and clarifications recorded in the PRD change log; no new or materially revised FR scope.

## Decision and Evidence

A fourth verify-fr pass on FR-014 v3.11 found 2 critical, 4 medium, and 3 minor issues. The Product Owner chose: Issue 1, option C; Issues 2–6, option A; Issue 7, add the dependencies; Issue 8, reword Rule 11; Issue 9, align the dates.

## Changes

- **Review rating trend (Issue 1)**: The system PRD required "review ratings and trends over time", but no FR-014 widget shows ratings over time. The system PRD now requires review ratings only (average overall rating, benchmark comparison, and per-treatment sub-scores). No widget was added.
- **Audit retention (Issue 2)**: Rule 15 said analytics access logs were kept for 12 months. The constitution (§II) requires tamper-proof audit trails that are immutable and retained for 10 years. Rule 15 and the system PRD now log analytics access to the S-06 Audit Log Service with 10-year immutable retention.
- **Refund source of truth (Issue 3)**: The `payments` schema allows both refund rows and an original payment flipped to `refunded`. That could remove a refund from gross figures and then subtract it again, and the old refund-rate source counted both records. A new Refund Source of Truth rule counts refunds only from completed `payment_type = 'refund'` rows. Refunded originals stay in gross income and GMV (`payment_status IN ('completed', 'refunded')`). Applied to Screen 4 Widgets 1 and 5, the Screen 4 business rules, Screen 7 C1, and Screen 12 Widgets 1 and 3.
- **Screen 7 Section A (Issue 4)**: The "always current snapshot" rule contradicted tiles that show period values. All sections now follow the time range filter, and each tile's period basis is defined; Tile 1 counts active providers at the end of the period.
- **Screen 1 click behaviour (Issue 5)**: A single click cross-filters. The drill-down opens from an explicit "View list" action in the element's tooltip or keyboard focus menu, and Rule 3 now carries this as a Screen 1 exception. The locked sections, widgets, chart types, filters, and layout are unchanged.
- **Widget-scoped exports (Issue 6)**: Exports contain only the widgets the generating user can see, so a Clinical Staff Screen 3 export holds only the satisfaction and aftercare widgets. Recipients and report-history access require permission for every included widget, and recurring runs re-check the owner's permissions at run time. Updated the Rule 15F matrix and the Screen 6 rules.
- **Dependencies (Issue 7)**: Added FR-009 (provider roles, Rule 15F, export recipients) and FR-016 (Screen 7 Tile 3).
- **Rule 11 (Issue 8)**: Reworded to the FR-003 masking format (patient ID plus a partially masked name; never full names or contact details), which matches the Screen 1 Inquiry Queue.
- **Dates (Issue 9)**: The v3.11 change log row and approval row now both state "approved 2026-10-13, applied 2026-10-14". The PRD Source line lists the 2026-10-14 approval.

## Files Updated

- [FR-014 PRD](../../functional-requirements/fr014-provider-analytics-reporting/prd.md) — v3.12 and v3.13, change log and approvals
- [System PRD](../../system-prd.md) — FR-014 provider rating requirement and analytics access-log retention

## Fifth Verification Pass (v3.12 → v3.13)

Minor clarifications approved by the Product Owner on 2026-10-14 (Issue 1 revised to provider-chosen treatment only, Issue 2 option 1, Issue 3 option 1, Issue 4 fix wording). No Change Request; Screen 1 layout unchanged.

- **Treatment-segment funnels (Issue 1)**: Inquiries that never received a parent quote had no treatment, so they dropped out of the per-treatment base and inflated conversion. The Product Owner confirmed that patients never choose a treatment in the inquiry (they describe their condition and pick a treatment area); the provider chooses the treatment in the parent quote. Treatment segments now start at Quoted: Screen 2 Widget 2 shows Quoted → Accepted → Confirmed booking per treatment, the Screen 2 treatment filter applies from Quoted onward (the Inquiries stage shows "—"), Screen 3 Widget 5 and Screen 7 B4 count quoted inquiries by treatment, and the counting rule, the Screen 6 export treatment filter, and the FR-003 dependency text were aligned. Unquoted inquiries appear only in all-treatments views.
- **Zero-provider countries (Issue 2)**: Screen 10 Widget 3 now flags countries with no active providers as "No coverage" and sorts them first, instead of showing N/A.
- **Calculation bases (Issue 3)**: Defined revenue-by-treatment attribution (Screen 4 Widget 2; Screen 1 C2 references it as a definition-only note), the failed payment rate denominator (Screen 12 Widget 3), average affiliate booking value (Screen 9 Widget 6), and how the Screen 11 five-booking minimum applies per bar. Low-volume providers stay in pooled rates; how low-sample bars look is left to the UX designer.
- **Payout rows (Issue 4)**: Screen 4 Widget 8 now refers to the 2–3 rows in the Screen 1 C4 inline table.

## Sixth Verification Pass (v3.13 → v3.14)

Minor clarifications approved by the Product Owner on 2026-10-14 (Issue 1 option 1, Issue 2 option 1, Issue 3 align wording, Issue 4 define both). No Change Request; Screen 1 layout unchanged.

- **Filter applicability (Issue 1)**: Screens 4, 9, and 10 offered a Treatment filter that some widgets cannot honour, because inquiries carry no treatment and payout statements are per provider period. New Global Filter Rule 5A says a filter applies only where the source records carry that dimension, keeps the Screen 2 "measure from Quoted" behaviour for funnels, and lists the widgets on Screens 4, 9, and 10 that render unfiltered with a note. Those three screens and the Screen 6 export treatment filter now reference Rule 5A.
- **Avg rating source (Issue 2)**: The Screen 3 Widget 1 Avg rating column is now defined as the average `overall_rating` of the provider's Published FR-013 reviews in range, grouped by the reviewing patient's country.
- **Wording alignment (Issue 3)**: REQ-014-045 now says quoted inquiry count, matching Screen 3 Widget 5. The system PRD SLA-breach alert now fires once per distributed inquiry/provider pair, timed from distribution, matching REQ-014-113 and FR-020/FR-030.
- **Definitions (Issue 4)**: The Screen 1 C4 "Type" column uses the Screen 4 Widget 8 provider payout statuses (definition only). The Screen 7 Tile 5 "active providers" means account status, not the Screen 8 activity-based Active status.

Files: [FR-014 PRD](../../functional-requirements/fr014-provider-analytics-reporting/prd.md) (v3.14, change log, approvals); [System PRD](../../system-prd.md) (FR-014 SLA-breach alert wording).
