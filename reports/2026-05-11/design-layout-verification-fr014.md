# Design Layout Verification Report — FR-014

**Report Date**: 2026-05-11
**Report Type**: Design Layout Verification
**FR Scope**: FR-014 - Provider Analytics & Reporting
**Flow Scope**: Provider and Admin analytics suites, Screens 2-13 only (Screen 1 already completed and excluded from this pass)
**Layout Source**: `layout-temp/`
**Platform**: Mixed (Provider Web + Admin Web)
**Status**: 🟡 PARTIAL - layout coverage is complete across the in-scope screens, with one functional labeling mismatch and several non-blocking UX improvements.

---

## Summary Dashboard

| # | Flow | Module | Screens Required | Screens Verified | Layout Status | Field Coverage |
|---|------|--------|-----------------|-----------------|---------------|----------------|
| PR-05 | Provider Reviews Analytics Suite | PR-05: Financial Management & Reporting | 5 | 5 | 🟢 COMPLETE | ~100% |
| A-08 | Admin Monitors Platform Health | A-08: Analytics & Reporting | 7 | 7 | 🟡 PARTIAL | ~98% |

**Overall**: 2 of 2 flows verified. Provider flow is COMPLETE; Admin flow is PARTIAL due to a Screen 11 labeling mismatch.
**Screens**: 12 of 12 specified screens have layouts (100% layout coverage for in-scope screens).

---

## Layout File Inventory

### Mapped to Spec Flows

| Layout File | Maps to Flow | Maps to Screen |
|-------------|-------------|----------------|
| `layout-temp/Performance & Conversion.jpg` | PR-05 | Screen 2 (Performance & Conversion) |
| `layout-temp/Patient Analytics.jpg` | PR-05 | Screen 3 (Patient Analytics) |
| `layout-temp/Finance & Payouts.jpg` | PR-05 | Screen 4 (Finance & Payouts) |
| `layout-temp/Pricing & Benchmarks.jpg` | PR-05 | Screen 5 (Pricing & Benchmarks) |
| `layout-temp/Export Report Config.jpg` | PR-05 | Screen 6 (Export Report Configuration) |
| `layout-temp/Platform Overview.jpg` | A-08 | Screen 7 (Platform Overview Dashboard) |
| `layout-temp/Provider Performance & Engagement.jpg` | A-08 | Screen 8 (Provider Performance & Engagement) |
| `layout-temp/Patient Acquisition & Funnel.jpg` | A-08 | Screen 9 (Patient Acquisition & Funnel) |
| `layout-temp/Geographic Intelligence.jpg` | A-08 | Screen 10 (Geographic Intelligence) |
| `layout-temp/Treatment Outcomes.jpg` | A-08 | Screen 11 (Treatment Outcomes) |
| `layout-temp/Financial Health & Cashflow.jpg` | A-08 | Screen 12 (Financial Health & Cashflow) |
| `layout-temp/Pricing Intelligence.jpg` | A-08 | Screen 13 (Pricing Intelligence) |
| `layout-temp/Full Table - Provider League Table.jpg` | A-08 | Screen 8 (Provider Performance & Engagement) |

### Unmapped Files

| Layout File | Likely Purpose | Notes |
|-------------|---------------|-------|
| None | - | All discovered layout files map to the in-scope FR-014 screens or a screen variant. |

---

## Detailed Verification by Flow

---

### Flow PR-05: Provider Reviews Analytics Suite

**Status**: 🟢 COMPLETE - All five in-scope provider analytics screens have matching layouts with only minor presentation differences.
**Screens required**: 5
**Layout files**: `Performance & Conversion.jpg`, `Patient Analytics.jpg`, `Finance & Payouts.jpg`, `Pricing & Benchmarks.jpg`, `Export Report Config.jpg`

#### Screen 2: Performance & Conversion

**Layout**: `layout-temp/Performance & Conversion.jpg`

##### Flow Context

- **User arrives from**: Provider Analytics nav entry / Screen 1 handoff
- **Screen purpose**: Review funnel health, quote conversion, and operational responsiveness
- **Entry point**: Present - Analytics nav item and breadcrumb align with the provider analytics flow.
- **Exit path**: Present - Adjacent analytics screens are available from the left nav and the export CTA routes onward to Screen 6.
- **Data continuity**: Correct - Shared filters and analytics naming remain consistent across the provider suite.
- **Flow context issues**: None visible in the static layout.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Time range, country, and treatment filters | Yes | ✅ | Present in the filter bar; treatment filter is available on the screen as required. |
| Funnel Conversion Trend | Yes | ✅ | Multi-line chart with four stage lines and Week/Month toggle is present. |
| Conversion Breakdown by Treatment Type | Yes | ✅ | Grouped bar chart is present with inquiry, quoted, and in-progress groupings. |
| Conversion Breakdown by Patient Country | Yes | ✅ | Horizontal ranked country chart is present with inquiry-count context on the right. |
| Quote Acceptance Rate Trend | Yes | ✅ | Trend chart is present in the lower-left panel. |
| TTFQ Trend Over Time | Yes | ✅ | Dual-line chart includes p50, p90, SLA target, and green/amber/red background bands. |
| Cancellation & No-Show Rate | Yes | ✅ | Two KPI cards with separate sparkline trends are present. |
| Platform Benchmarks (Anonymised) | Yes | ✅ | Benchmark comparison table includes provider value, platform median, variance, and percentile. |

**Extra Elements**:

- Top-right `Export Report` CTA is not specified in the Screen 2 widget list but aligns with alternative flow A2.

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 8/8 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: ui-ux-pro-max, web-design-guidelines

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| 💡 UX Suggestion | `U-03`, `W-08`: the page is extremely long and relies on vertical scrolling without a local section jump menu or sticky in-page index. | Consider adding a compact section index or sticky summary rail for faster scanning across the seven analytics widgets. |

#### Screen 3: Patient Analytics

**Layout**: `layout-temp/Patient Analytics.jpg`

##### Flow Context

- **User arrives from**: Screen 2 via Analytics nav
- **Screen purpose**: Review patient demographics, geography, and satisfaction trends
- **Entry point**: Present - reachable from the same Analytics nav group immediately after Screen 2.
- **Exit path**: Present - user can continue to Finance & Payouts from the left nav or export from the top-right CTA.
- **Data continuity**: Correct - Period and country filters remain consistent with the flow definition.
- **Flow context issues**: None visible in the static layout.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Time range and country filters | Yes | ✅ | Present in the filter bar. |
| Full Patient Location Breakdown | Yes | ✅ | Ranked table and linked donut are both present. |
| New vs. Returning Patients | Yes | ✅ | Donut split and trend line appear together as specified. |
| Patient Journey Time | Yes | ✅ | p50 tile, p90 tile, and duration distribution chart are present. |
| Review Sub-Scores by Treatment | Yes | ✅ | Grouped bar chart shows Overall, Results, Staff, Facility, and Value scores. |
| Treatment Preference Distribution | Yes | ✅ | Dual-bar ranked chart compares inquiries vs booking counts per treatment. |
| Aftercare Activation Rate | Yes | ✅ | KPI tile with sparkline trend is present. |

**Extra Elements**:

- Top-right `Export Report` CTA extends the documented export flow without conflicting with the screen spec.

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 7/7 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: ui-ux-pro-max, web-design-guidelines

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| 💡 UX Suggestion | `U-12`: several country names in the location table truncate with ellipsis (`United Kingd...`) and there is no visible affordance for full-value reveal in the static design. | Add tooltip, row expansion, or slightly wider first column so full country names are recoverable without guesswork. |

#### Screen 4: Finance & Payouts

**Layout**: `layout-temp/Finance & Payouts.jpg`

##### Flow Context

- **User arrives from**: Screen 3 via Analytics nav
- **Screen purpose**: Review revenue, payout status, and overdue financial actions
- **Entry point**: Present - listed in the provider Analytics nav and keeps the same breadcrumb/filter structure.
- **Exit path**: Present - next analytics destinations remain available from the nav and export CTA.
- **Data continuity**: Correct - period, country, and treatment filters persist, and the finance notes continue the provider-currency narrative from the spec.
- **Flow context issues**: None that block the workflow.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Time range, country, and treatment filters | Yes | ✅ | Present in the filter bar. |
| Revenue Trend | Yes | ✅ | Area line chart with Week/Month/Quarter toggle is present. |
| Revenue by Treatment - Full Breakdown | Yes | ✅ | Ranked bar chart is present with pagination for long lists. |
| Revenue by Patient Country | Yes | ✅ | Horizontal ranked chart is present with country labels and values. |
| Commission & Net Revenue | Yes | ✅ | Two KPI tiles plus combined trend chart are present. |
| Refunds | Yes | ✅ | Refund amount tile, refund-rate tile, and trend chart are present. |
| Installment vs. Full Payment Split | Yes | ✅ | Donut, average-installment KPI, and adoption trend are present. |
| Cash-at-Risk Summary | Yes | ✅ | Summary KPI and aging-bucket counts are present; the design exposes more detail than the spec minimum. |
| Payout History & Schedule | Yes | ✅ | Monthly chart and full table include Period, Amount, Status, Disbursed date, and Cadence. |

**Extra Elements**:

- The design includes an on-screen `Quotes per Aging Bucket` chart for cash-at-risk instead of relying only on a link back to Screen 1 Section C3.

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 9/9 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: ui-ux-pro-max, web-design-guidelines

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| 💡 UX Suggestion | `U-03`, `W-08`: Screen 4 carries a high density of charts, KPI cards, notes, and tables in one long page, which weakens scan speed despite all content being present. | Consider adding stronger section separators or collapsible subsections around finance, payout, and risk blocks. |

#### Screen 5: Pricing & Benchmarks

**Layout**: `layout-temp/Pricing & Benchmarks.jpg`

##### Flow Context

- **User arrives from**: Screen 4 via Analytics nav
- **Screen purpose**: Compare provider pricing to platform medians and benchmark bands
- **Entry point**: Present - accessible from the same provider Analytics nav set.
- **Exit path**: Present - export path remains available and the nav supports return to other analytics screens.
- **Data continuity**: Correct - shared filters are preserved, and benchmark metrics align with Screens 2-4 concepts.
- **Flow context issues**: None visible in the static layout.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Time range, country, and treatment filters | Yes | ✅ | Present in the filter bar. |
| Average Quote Amount by Treatment | Yes | ⚠️ | The required treatment comparison is present, but the provider's own over-time trend is separated into a KPI/sparkline card above the bars rather than overlaid on the same chart. |
| Quote Amount Distribution | Yes | ✅ | Histogram is present with provider and platform median reference lines. |
| Price vs. Conversion Rate | Yes | ✅ | Scatter plot is present with labelled treatment points and median reference lines. |
| Platform Benchmark Comparison | Yes | ✅ | Benchmark comparison table is present with provider value, platform median, variance, and percentile band. |

**Extra Elements**:

- Quadrant background shading and textual quadrant labels on the scatter plot provide helpful interpretation beyond the spec minimum.

**Screen Status**: 🟢 GOOD
**Field Coverage**: 4/4 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: ui-ux-pro-max, web-design-guidelines

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| 💡 UX Suggestion | `U-04`, `W-08`: the opening KPI/sparkline card and the bar chart for the same widget read as two separate components before the user understands they are one analytical story. | Tighten the visual grouping or add a sublabel to make the relationship between the KPI card and the treatment bars explicit. |

#### Screen 6: Export Report Configuration

**Layout**: `layout-temp/Export Report Config.jpg`

##### Flow Context

- **User arrives from**: Any provider analytics screen via Export action
- **Screen purpose**: Configure and generate PDF/CSV exports for analytics sections
- **Entry point**: Present - reachable from provider analytics via nav and from export actions on the analytical screens.
- **Exit path**: Present - primary CTA generates the report, and report history supports re-download.
- **Data continuity**: Correct - selected screens, date range, country, and treatment filters match the upstream analytics context.
- **Flow context issues**: None visible in the static layout.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Report type | Yes | ✅ | PDF Summary and CSV Detailed radio options are present. |
| Screens to include | Yes | ✅ | Checkbox list includes Performance, Patient Analytics, Finance & Payouts, and Pricing & Benchmarks only. |
| Date range | Yes | ✅ | Start/end date picker is present. |
| Country filter | No | ✅ | Optional dropdown is present. |
| Treatment filter | No | ✅ | Optional dropdown is present. |
| Email delivery | No | ✅ | Optional checkbox is present. |
| Schedule recurring | No | ✅ | Optional recurring schedule checkbox with Weekly/Monthly/Quarterly options is present. |

**Extra Elements**:

- `Report History` table is included below the form, supporting the business rule around stored exports and re-download.

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 7/7 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: ui-ux-pro-max, web-design-guidelines

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-01`, `U-17`: the page shows two green primary actions (`Generate Report` in the page header and again at the bottom of the form), which creates ambiguity about whether they perform the same action. | Keep a single primary CTA or clearly differentiate the header action from the form-submit action. |

**Flow Coverage Gaps**:

- None. All five in-scope provider screens have corresponding layouts and the core widget set is present across the suite.

---

### Flow A-08: Admin Monitors Platform Health

**Status**: 🟡 PARTIAL - All seven admin analytics screens have layouts, but Screen 11 contains a clear KPI labeling mismatch inside the aftercare section.
**Screens required**: 7
**Layout files**: `Platform Overview.jpg`, `Provider Performance & Engagement.jpg`, `Full Table - Provider League Table.jpg`, `Patient Acquisition & Funnel.jpg`, `Geographic Intelligence.jpg`, `Treatment Outcomes.jpg`, `Financial Health & Cashflow.jpg`, `Pricing Intelligence.jpg`

#### Screen 7: Platform Overview Dashboard

**Layout**: `layout-temp/Platform Overview.jpg`

##### Flow Context

- **User arrives from**: Admin Analytics nav entry
- **Screen purpose**: Review platform-wide operational health and top-level KPIs
- **Entry point**: Present - Admin Analytics nav and breadcrumb match the overview landing screen requirement.
- **Exit path**: Present - Section cards use arrow affordances and downstream screens are available from the analytics sidebar.
- **Data continuity**: Correct - Period, country, and provider filters are consistent with the flow and the three section model is preserved.
- **Flow context issues**: None blocking; responsive fallback cannot be verified from the static desktop layout.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Time range, country, and provider filters | Yes | ✅ | Present in the filter bar. |
| Section A - Operational Health tiles | Yes | ✅ | Active Providers, Total Inquiries, New Patients Registered, Provider TTFQ Health Distribution, and Provider Engagement Rate are all present. |
| Section B1 - Platform-Wide Conversion Funnel | Yes | ✅ | Funnel chart with stage counts and overall conversion footer is present. |
| Section B2 - Platform TTFQ Distribution | Yes | ✅ | p50/p90 bullet-style distribution against SLA is present. |
| Section B3 - Top Patient Origin Countries | Yes | ✅ | Donut chart is present with top-country labels and Other. |
| Section B4 - Treatment Type Distribution | Yes | ✅ | Donut chart is present in the lower-right of the performance section. |
| Section C1-C4 - Financial Summary KPIs | Yes | ✅ | GMV, Commission Earned, Upcoming Payout Obligations, and Platform Cash-at-Risk KPI cards are present. |

**Extra Elements**:

- A `Cash-at-Risk Aging Distribution` chart appears directly on Screen 7, providing more detail than the spec's KPI-only summary requirement.

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 7/7 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: ui-ux-pro-max, web-design-guidelines

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| 💡 UX Suggestion | `W-08`: the landing screen packs many dense sections onto a single scrolling page, which weakens fast executive scanning despite strong section headings. | Consider a compact sticky section navigator for Operations, Performance, and Finance on long desktop pages. |

#### Screen 8: Provider Performance & Engagement

**Layout**: `layout-temp/Provider Performance & Engagement.jpg`, `layout-temp/Full Table - Provider League Table.jpg`

##### Flow Context

- **User arrives from**: Screen 7 via Analytics nav
- **Screen purpose**: Review provider performance, identify outliers, and drill into provider league data
- **Entry point**: Present - linked from Screen 7 and visible in the analytics sidebar.
- **Exit path**: Present - drill-down destinations and adjacent analytics screens remain reachable from the sidebar.
- **Data continuity**: Correct - TTFQ-health and engagement filters align with the screen's two-part purpose.
- **Flow context issues**: None visible in the static layout.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Time range, country, TTFQ health, and engagement filters | Yes | ✅ | All four filters are present in the top bar. |
| Provider League Table | Yes | ✅ | The main layout plus the `Full Table - Provider League Table.jpg` variant together show Provider, TTFQ p50, Conversion Rate, Quote Acceptance Rate, Avg Overall Rating, Quote Response Rate, vs. Platform, and Status. |
| Performance Distribution | Yes | ✅ | Scatter plot with quadrant labels and platform median reference lines is present. |
| Provider Activity Table | Yes | ✅ | Activity table includes Provider, Last Active, Quotes This Month, Inquiry Response Rate, and Status. |
| New Provider Ramp | Yes | ✅ | Multi-series ramp chart with platform average curve is present. |
| Engagement Health Summary | Yes | ✅ | Active, At-Risk, and Dormant KPI tiles are present. |

**Extra Elements**:

- None.

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 5/5 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: ui-ux-pro-max, web-design-guidelines

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| 💡 UX Suggestion | `U-05`, `W-06`: this screen depends on a separate full-table variant to reveal all league-table columns clearly. | If possible, make the default screen viewport expose the complete table schema or add an in-UI horizontal-scroll cue. |

#### Screen 9: Patient Acquisition & Funnel

**Layout**: `layout-temp/Patient Acquisition & Funnel.jpg`

##### Flow Context

- **User arrives from**: Screen 8 via Analytics nav
- **Screen purpose**: Review inquiry volumes, conversion leak points, and acquisition efficiency
- **Entry point**: Present - available from the analytics sidebar and drill-down from Screen 7.
- **Exit path**: Present - drill-down intent is supported by the chart/table structures, and adjacent screens are reachable from the sidebar.
- **Data continuity**: Correct - filters and platform-wide wording stay consistent across acquisition widgets.
- **Flow context issues**: None visible in the static layout.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Time range, country, and treatment filters | Yes | ✅ | Present in the filter bar. |
| Inquiry Volume Trend | Yes | ✅ | Area line chart includes prior-period dashed comparison and Week/Month toggle. |
| Platform Funnel Trend Over Time | Yes | ✅ | Multi-line funnel-stage trend is present. |
| New vs. Returning Patients | Yes | ✅ | Stacked monthly bars and KPI tiles are present. |
| Patient Journey Time (Platform-Wide) | Yes | ✅ | p50 tile, p90 tile, and distribution histogram are present. |
| Inquiry Seasonality | Yes | ✅ | Calendar heatmap with intensity legend and tooltip is present. |
| Affiliate Acquisition | Yes | ✅ | Three KPI tiles and affiliate ranked table are present. |

**Extra Elements**:

- None.

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 7/7 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: ui-ux-pro-max, web-design-guidelines

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| 💡 UX Suggestion | `U-04`, `W-08`: the screen spans many analytic modes, and the affiliate block arrives far below the top funnel widgets with little sectional reinforcement beyond headings. | Increase sectional contrast or insert divider summaries so users can re-orient faster between acquisition, journey, seasonality, and affiliate analysis. |

#### Screen 10: Geographic Intelligence

**Layout**: `layout-temp/Geographic Intelligence.jpg`

##### Flow Context

- **User arrives from**: Screen 9 via Analytics nav
- **Screen purpose**: Identify underserved regions and geographic demand/supply patterns
- **Entry point**: Present - accessible from the analytics sidebar.
- **Exit path**: Present - country-focused structures support drill-down continuation and adjacent screens remain reachable from the sidebar.
- **Data continuity**: Correct - the screen preserves the strategic demand/supply framing and treatment filter scope from the spec.
- **Flow context issues**: None visible in the static layout.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Time range and treatment filters | Yes | ✅ | Present in the filter bar. |
| Patient Demand Map / ranked fallback | Yes | ✅ | The design uses the allowed ranked-table fallback instead of a choropleth map. |
| Provider Coverage by Country | Yes | ✅ | Horizontal ranked bar chart is present. |
| Demand vs. Supply Gap | Yes | ✅ | Ranked table with patient country, inquiry count, provider count, inquiries per provider, and gap flag is present. |
| Conversion Rate by Patient Country | Yes | ✅ | Ranked country conversion chart is present. |
| Emerging Patient Origins | Yes | ✅ | Ranked growth table is present. |

**Extra Elements**:

- None.

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 6/6 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: ui-ux-pro-max, web-design-guidelines

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| 💡 UX Suggestion | `U-23`: the table fallback labels use `Demand` bins while other widgets use explicit counts, rates, and gap statuses; the meaning is valid but slightly harder to interpret at a glance. | Add a brief helper note or legend near the demand table header that decodes what each demand bin represents. |

#### Screen 11: Treatment Outcomes

**Layout**: `layout-temp/Treatment Outcomes.jpg`

##### Flow Context

- **User arrives from**: Screen 10 via Analytics nav
- **Screen purpose**: Review clinical and operational outcome trends, cancellations, and aftercare activation
- **Entry point**: Present - available from the analytics sidebar.
- **Exit path**: Present - drill-down-oriented charts and tables remain aligned with the admin analytics flow.
- **Data continuity**: Mostly correct - filters and treatment-oriented metrics are present, but the aftercare section contains one mislabeled KPI.
- **Flow context issues**: One labeling issue in the aftercare section introduces cross-screen confusion.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Time range, country, provider, and treatment filters | Yes | ✅ | Present in the filter bar. |
| Treatment Completion Rate | Yes | ✅ | Bar chart with platform average reference line is present. |
| Cancellation & No-Show Rate by Treatment | Yes | ✅ | Grouped bar chart is present. |
| Treatment Volume Trend | Yes | ✅ | Stacked area chart is present. |
| Average Review Scores by Treatment | Yes | ✅ | Grouped bar chart with Overall, Results, Staff, Facility, and Value is present. |
| Aftercare Activation Rate | Yes | ❌⚠️ | The section exists, but the left KPI is labeled `New Patient Rate (Period)` instead of an aftercare activation metric, which conflicts with the Screen 11 purpose and widget definition. |
| Provider Distribution by Treatment Specialisation | Yes | ✅ | Stacked horizontal bar chart is present. |

**Extra Elements**:

- The aftercare section also shows an absolute activated-plan count card alongside the rate KPI, which is useful but secondary to the labeling mismatch.

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 6/6 (100%)
**Critical Issues**: Aftercare KPI label/content mismatch on Screen 11

##### UX/UI Design Evaluation

**Skills invoked**: ui-ux-pro-max, web-design-guidelines

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-23`: the aftercare card uses `New Patient Rate (Period)` wording inside the `Aftercare Activation Rate` section, creating a cross-screen terminology conflict and making the KPI look copied from Screen 9. | Replace the KPI title and helper copy with aftercare-specific wording so the section reads as a coherent treatment-outcomes module. |

#### Screen 12: Financial Health & Cashflow

**Layout**: `layout-temp/Financial Health & Cashflow.jpg`

##### Flow Context

- **User arrives from**: Screen 11 via Analytics nav
- **Screen purpose**: Review platform cash risk, payout obligations, and financial exposure
- **Entry point**: Present - accessible from the analytics sidebar and Screen 7 finance drill-downs.
- **Exit path**: Present - detailed tables and card structures support downstream operational follow-up.
- **Data continuity**: Correct - the currency filter and finance terminology remain consistent across all widgets.
- **Flow context issues**: None visible in the static layout.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Time range, country, and currency filters | Yes | ✅ | Present in the filter bar. |
| Platform GMV & Net Revenue | Yes | ✅ | Dual-line area chart is present. |
| Commission Earned Trend | Yes | ✅ | Monthly bar chart with target reference line is present. |
| Refund & Failed Payment Health | Yes | ✅ | Four KPI tiles and dual-line trend are present. |
| Cash-at-Risk - Platform-Wide Aging | Yes | ✅ | Stacked horizontal aging chart is present. |
| Upcoming Provider Payout Obligations | Yes | ✅ | KPI cards and provider payout table are present. |
| Installment Plan Health | Yes | ✅ | Donut with on-time/overdue/defaulted split and outstanding balance KPI is present. |
| Affiliate Commission Obligations | Yes | ✅ | KPI plus upcoming affiliate commission table is present. |
| Revenue by Currency | Yes | ✅ | Currency-segment donut is present. |

**Extra Elements**:

- None.

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 9/9 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: ui-ux-pro-max, web-design-guidelines

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| 💡 UX Suggestion | `W-08`: this is another very dense finance page where risk, payout, installment, FX, and affiliate obligations compete for attention on a single scroll. | Consider a compact sticky subsection rail or collapsible groups for Risk, Payouts, Installments, FX, and Affiliates. |

#### Screen 13: Pricing Intelligence

**Layout**: `layout-temp/Pricing Intelligence.jpg`

##### Flow Context

- **User arrives from**: Screen 12 via Analytics nav
- **Screen purpose**: Identify pricing outliers and platform pricing distribution
- **Entry point**: Present - reachable from the analytics sidebar.
- **Exit path**: Present - outlier table drill-downs align with provider-detail follow-up.
- **Data continuity**: Correct - treatment and country filters fit the market-pricing purpose, and every pricing widget is represented.
- **Flow context issues**: None visible in the static layout.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Time range, country, and treatment filters | Yes | ✅ | Present in the filter bar. |
| Average Quote Amount by Treatment | Yes | ✅ | Bar chart with p25-p75 error bars is present. |
| Price Range per Treatment | Yes | ✅ | Box-plot/range visualization is present. |
| Quote Amount by Provider Country | Yes | ✅ | Grouped bar chart by provider country is present. |
| Conversion Rate by Price Bracket | Yes | ✅ | Bracketed conversion bar chart with platform reference line is present. |
| Price Trend Over Time per Treatment | Yes | ✅ | Multi-line trend chart is present. |
| Price Outlier Providers | Yes | ✅ | Ranked outlier table includes Provider, Treatment, Avg Quote Amount, Platform Median, Variance %, and Direction. |

**Extra Elements**:

- None.

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 7/7 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: ui-ux-pro-max, web-design-guidelines

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| 💡 UX Suggestion | `U-04`, `W-08`: the screen is strong structurally, but the stacked sequence of five charts before the outlier table makes the final action-oriented block easy to miss. | Add a stronger transition treatment or a short subheading above `Price Outlier Providers` to emphasize it as the decision-making endpoint. |

**Flow Coverage Gaps**:

- Screen 11 aftercare section needs copy correction so the KPI language matches treatment-outcomes intent.

---

## Action Items

| Priority | Flow | Screen | Issue | Recommendation |
|----------|------|--------|-------|----------------|
| ⚠️ Important | A-08 | Screen 11 | `Aftercare Activation Rate` section uses `New Patient Rate (Period)` wording on the left KPI, which conflicts with the screen purpose and widget definition. | Replace the KPI title/helper copy with aftercare-specific terminology and verify the metric source matches activated aftercare records. |
| ⚠️ UX Improvement | PR-05 | Screen 6 | Two green primary CTAs (`Generate Report` in header and form footer) create ambiguity about the main submit action. | Keep one primary CTA or clearly differentiate the header action from the form-submit action. |
| 💡 Suggestion | PR-05 | Screen 5 | `Average Quote Amount by Treatment` splits the trend context into a separate KPI card instead of visually tying it to the treatment comparison chart. | Strengthen grouping or annotate the relationship between the KPI/sparkline and the treatment bars. |
| 💡 Suggestion | A-08 | Screen 8 | Default viewport does not clearly expose the full provider league-table schema without the separate full-table variant. | Add an in-UI horizontal-scroll cue or ensure the default table treatment communicates hidden columns. |
| 💡 Suggestion | PR-05 | Screen 3 | Country names truncate in the location table without a visible recovery affordance. | Add tooltip, wrap, or row expansion so full country names are readable. |

### Priority Legend

- **🔴 Critical**: Blocks flow progression, breaks data integrity, or causes security/legal risk. Must fix before development.
- **🔴 Critical UX**: Severe usability issue that would prevent users from completing the flow or cause significant confusion. Must fix before development.
- **⚠️ Important**: Functional discrepancy that could cause user confusion or require rework during development. Should fix before development.
- **⚠️ UX Improvement**: Usability or design quality issue that deviates from platform conventions or best practices. Should fix before development.
- **💡 Suggestion**: Cosmetic or minor improvement. Can fix anytime.
- **💡 UX Suggestion**: Minor design enhancement that would improve polish. Can fix anytime.

---

## Notes

- Verification compares FR-014 screen specifications in `local-docs/project-requirements/functional-requirements/fr014-provider-analytics-reporting/prd.md` against static layout images in `layout-temp/`.
- UX/UI findings are evaluated against `verify-design-layout/references/ux-ui-evaluation-rules.md` using Universal + Web checks.
- Static images cannot confirm interaction-only states such as hover, focus, keyboard accessibility, or runtime drill-down behavior unless explicitly visible.
- In-scope layout coverage is complete for Screens 2-13; Screen 1 was intentionally excluded because the user marked it as already done.
- Most gaps in this pass are presentation/copy issues rather than missing screens or missing widget structures.
