# Design Layout Verification Report — FR-014

**Report Date**: 2026-05-06
**Report Type**: Design Layout Verification
**FR Scope**: FR-014 - Provider Analytics & Reporting
**Flow Scope**: Provider tenant only, Screen 2 through Screen 6 (Screen 1 skipped per user instruction and FR lock)
**Layout Source**: `layout-temp/`
**Platform**: Provider Web
**Status**: 🟡 PARTIAL

---

## Summary Dashboard

| # | Flow | Module | Screens Required | Screens Verified | Layout Status | Field Coverage |
|---|------|--------|-----------------|-----------------|---------------|----------------|
| PR-05-F1 | Provider Reviews Analytics Suite | PR-05: Financial Management & Reporting / A-08: Analytics & Reporting | 5 | 5 | 🟡 PARTIAL | ~96% |

**Overall**: 1 of 1 flows verified. The provider analytics suite is structurally complete, but 2 of 5 screens still contain spec or continuity gaps that should be corrected before implementation handoff.
**Screens**: 5 of 5 specified screens have layouts (100% layout coverage). 3 screens are `🟢 COMPLETE`; 2 screens are `🟡 PARTIAL`.

---

## Layout File Inventory

### Mapped to Spec Flows

| Layout File | Maps to Flow | Maps to Screen |
|-------------|-------------|----------------|
| `layout-temp/Performance & Conversion.jpg` | PR-05-F1 | Screen 2 (Performance & Conversion) |
| `layout-temp/Patient Analytics.jpg` | PR-05-F1 | Screen 3 (Patient Analytics) |
| `layout-temp/Finance & Payouts.jpg` | PR-05-F1 | Screen 4 (Finance & Payouts) |
| `layout-temp/Pricing & Benchmarks.jpg` | PR-05-F1 | Screen 5 (Pricing & Benchmarks) |
| `layout-temp/Export Report Config.jpg` | PR-05-F1 | Screen 6 (Export Report Configuration) |

### Unmapped Files

| Layout File | Likely Purpose | Notes |
|-------------|---------------|-------|
| None | N/A | All files found in `layout-temp/` map to in-scope provider screens. |

---

## Detailed Verification by Flow

---

### Flow PR-05-F1: Provider Reviews Analytics Suite

**Status**: 🟡 PARTIAL
**Screens required**: 5
**Layout files**: `Performance & Conversion.jpg`, `Patient Analytics.jpg`, `Finance & Payouts.jpg`, `Pricing & Benchmarks.jpg`, `Export Report Config.jpg`

#### Screen 2: Performance & Conversion

**Layout**: `layout-temp/Performance & Conversion.jpg`

##### Flow Context

- **User arrives from**: `Analytics` nav default entry for provider users
- **Screen purpose**: Deep analysis of conversion efficiency, TTFQ trends, and benchmarking
- **Entry point**: Present. The left navigation highlights `Analytics > Performance & Conversion`, matching the FR entry point where provider users land on Screen 2 after clicking `Analytics`.
- **Exit path**: Present. The left analytics navigation exposes onward movement to `Patient Analytics`, `Finance & Payout`, `Pricing & Benchmarks`, and `Export Report Config`, and the page-level `Export Report` CTA supports Alternative Flow A2.
- **Data continuity**: Correct. Shared filters for period, country, and treatment type are visible at the top and appear to scope all widgets on the page.
- **Flow context issues**: None in the provided layout.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Page title (`Performance & Conversion`) | Yes | ✅ | Visible as the primary page heading in `layout-temp/Performance & Conversion.jpg`, matching the screen spec title. |
| Filter: Time range | Yes | ✅ | `Last 4 weeks` dropdown is visible in the filter bar and aligns with the required period filter. |
| Filter: Country | Yes | ✅ | `All countries` dropdown is visible and matches the required country filter. |
| Filter: Treatment type | Yes | ✅ | `All treatments` dropdown is visible and matches the required multi-select treatment filter. |
| Widget 1: Funnel Conversion Trend | Yes | ✅ | Visible as a multi-line chart with week/month toggle and four series: Qualified, Quoted, Accepted, In progress. |
| Widget 2: Conversion Breakdown by Treatment Type | Yes | ✅ | Visible as a grouped bar chart by treatment type with three grouped bars per treatment. |
| Widget 3: Conversion Breakdown by Patient Country | Yes | ✅ | Visible as a horizontal ranked bar chart by country with a secondary inquiry-count label at right. |
| Widget 4: Quote Acceptance Rate Trend | Yes | ✅ | Visible as a dedicated line chart titled `Quote Acceptance Rate Trend` with week/month toggle. |
| Widget 5: TTFQ Trend Over Time | Yes | ✅ | Visible as a dual-line chart with `P50`, `P90`, and `SLA Target`, plus color-banded background zones. |
| Widget 6: Cancellation & No-Show Rate | Yes | ✅ | Visible as two KPI tiles with sparklines for `Cancellation Rate` and `No-Show Rate`. |
| Widget 7: Platform Benchmarks (Anonymised) | Yes | ✅ | Visible as a comparison table with columns for metric, provider value, platform median, variance, and percentile. |
| Low-sample helper copy state | Conditional | ✅ | Not required in the default state shown; the FR only requires helper copy when the low-sample condition is triggered. |
| Loading skeleton state | Conditional | ⚠️ | Cannot verify from the static default-state image whether skeletons exist during loading. |
| Error banner + retry state | Conditional | ⚠️ | Cannot verify from the static default-state image whether the non-blocking error banner state exists. |

**Extra Elements**:

- Breadcrumb `Analytics / Performance & Conversion` — intentional navigational enhancement beyond the widget list.
- Global `Export Report` CTA — aligns with Alternative Flow A2, even though it is not listed in the screen's field table.
- Full provider portal sidebar and top utility icons — surrounding shell chrome, not a screen-spec violation.

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 11/11 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| None | No evidence-backed UX/UI rule violations identified from the provided static layout. | No change required from this static design review. |

#### Screen 3: Patient Analytics

**Layout**: `layout-temp/Patient Analytics.jpg`

##### Flow Context

- **User arrives from**: Screen 2 via provider analytics navigation
- **Screen purpose**: Understand patient origins, satisfaction, and journey duration
- **Entry point**: Present. The analytics side navigation highlights `Patient Analytics`, matching the provider flow step after Screen 2.
- **Exit path**: Present. The same analytics navigation exposes onward movement to `Finance & Payout`, `Pricing & Benchmarks`, and `Export Report Config`, and the page-level `Export Report` CTA supports Alternative Flow A2.
- **Data continuity**: Correct. Shared analytics filters for period and country are visible and consistently placed above the screen content.
- **Flow context issues**: None in the provided layout.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Page title (`Patient Analytics`) | Yes | ✅ | Visible as the primary page heading in `layout-temp/Patient Analytics.jpg`, matching the screen spec title. |
| Filter: Time range | Yes | ✅ | `Last 4 weeks` dropdown is visible in the filter bar and matches the required period filter. |
| Filter: Country | Yes | ✅ | `All countries` dropdown is visible and matches the required country filter. |
| Widget 1: Full Patient Location Breakdown | Yes | ✅ | Visible as a ranked table plus linked donut chart with country, inquiries, booked, booked rate, and average rating. |
| Widget 2: New vs. Returning Patients | Yes | ✅ | Visible as a donut split paired with a trend line over time. |
| Widget 3: Patient Journey Time | Yes | ✅ | Visible as two KPI tiles (`Median Journey Time (p50)` and `p90 Journey Time`) plus a distribution histogram with the expected bins. |
| Widget 4: Review Sub-Scores by Treatment | Yes | ✅ | Visible as a grouped bar chart with five visible series: Overall, Results, Staff, Facility, Value. |
| Widget 5: Treatment Preference Distribution | Yes | ✅ | The chart is present and the second legend label now reads `Booking count`, so the dual-bar meaning is correctly communicated. |
| Widget 6: Aftercare Activation Rate | Yes | ✅ | Visible as a KPI tile with a trend sparkline and explanatory subtitle. |
| Patient age distribution omitted when unavailable | Conditional | ✅ | No age widget is shown, which is allowed by the business rule when age is not directly available. |

**Extra Elements**:

- Breadcrumb `Analytics / Patient Analytics` — intentional navigational enhancement beyond the widget list.
- Global `Export Report` CTA — aligns with Alternative Flow A2, even though it is not listed in the screen's field table.
- Full provider portal sidebar and top utility icons — surrounding shell chrome, not a screen-spec violation.

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 8/8 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| None | No evidence-backed UX/UI rule violations identified from the updated static layout. | No change required from this static design recheck. |

#### Screen 4: Finance & Payouts

**Layout**: `layout-temp/Finance & Payouts.jpg`

##### Flow Context

- **User arrives from**: Screen 3 via provider analytics navigation
- **Screen purpose**: Review revenue, refunds, installment health, and payout history
- **Entry point**: Present. The analytics side navigation highlights `Finance & Payout`, matching the expected next step from Screen 3.
- **Exit path**: Present. The analytics navigation exposes `Pricing & Benchmarks` and `Export Report Config`, and the page-level `Export Report` CTA supports Alternative Flow A2.
- **Data continuity**: Correct. The filter bar retains period, country, and treatment type controls across the page.
- **Flow context issues**: None in the provided layout.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Page title (`Finance & Payouts`) | Yes | ✅ | Visible as the primary page heading in `layout-temp/Finance & Payouts.jpg`. |
| Filter: Time range | Yes | ✅ | `Last 4 weeks` dropdown is visible and matches the required period filter. |
| Filter: Country | Yes | ✅ | `All countries` dropdown is visible and matches the required country filter. |
| Filter: Treatment type | Yes | ✅ | `All treatments` dropdown is visible and matches the required treatment filter. |
| Widget 1: Revenue Trend | Yes | ✅ | Visible as an area line chart with week/month/quarter toggle and income series. |
| Widget 2: Revenue by Treatment — Full Breakdown | Yes | ✅ | Visible as a horizontal ranked bar chart with treatment names and percentage share labels. |
| Widget 3: Revenue by Patient Country | Yes | ✅ | The chart is present and the secondary labels at right now show patient-count values rather than percentage shares, matching the required secondary metric. |
| Widget 4: Commission & Net Revenue | Yes | ✅ | Visible as two KPI tiles with a combined trend chart for `Total Income (Gross)` and `Commission Deducted`. |
| Widget 5: Refunds | Yes | ✅ | Visible as two KPI tiles with a trend chart for refund rate over time. |
| Widget 6: Installment vs. Full Payment Split | Yes | ✅ | Visible as a donut plus KPI summary and adoption-rate trend line. |
| Widget 7: Cash-at-Risk Summary | Yes | ✅ | Visible as a total cash-at-risk KPI plus a bucketed quote-aging chart with counts by bucket. |
| Widget 8: Payout History & Schedule | Yes | ✅ | Visible as a monthly payout bar chart and a paginated table with period, amount, status, disbursed date, and cadence. |
| Commission model clarification note | Yes | ❌ | The visible layout does not show the required explanatory note clarifying whether the period includes percentage deductions, flat-rate deductions, or both. |
| Historical FX note | Yes | ❌ | The visible layout does not show the required footer note `Historical exchange rates applied`. |

**Extra Elements**:

- Breadcrumb `Analytics / Finance & Payouts` — intentional navigational enhancement beyond the widget list.
- Global `Export Report` CTA — aligns with Alternative Flow A2, even though it is not listed in the screen's field table.
- Full provider portal sidebar and top utility icons — surrounding shell chrome, not a screen-spec violation.

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 11/13 (85%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| None | No evidence-backed UX/UI rule violations identified from the updated static layout beyond the remaining missing disclosure notes, which are tracked as functional content gaps above. | No additional UX/UI change required from this static design recheck. |

#### Screen 5: Pricing & Benchmarks

**Layout**: `layout-temp/Pricing & Benchmarks.jpg`

##### Flow Context

- **User arrives from**: Screen 4 via provider analytics navigation
- **Screen purpose**: Compare quote pricing and conversion against platform peers
- **Entry point**: Present. The analytics side navigation highlights `Pricing & Benchmarks`, matching the expected next step from Screen 4.
- **Exit path**: Present. The page retains access to `Export Report Config` through the analytics nav and the page-level `Export Report` CTA.
- **Data continuity**: Correct. Period, country, and treatment type filters remain visible and consistent with earlier analytics screens.
- **Flow context issues**: None in the provided layout.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Page title (`Pricing & Benchmarks`) | Yes | ✅ | Visible as the primary page heading in `layout-temp/Pricing & Benchmarks.jpg`. |
| Filter: Time range | Yes | ✅ | `Last 4 weeks` dropdown is visible and matches the required period filter. |
| Filter: Country | Yes | ✅ | `All countries` dropdown is visible and matches the required country filter. |
| Filter: Treatment type | Yes | ✅ | `All treatments` dropdown is visible and matches the required treatment filter. |
| Widget 1: Average Quote Amount by Treatment | Yes | ✅ | Visible as a treatment bar chart with a provider trend sparkline in the summary card above it. |
| Widget 2: Quote Amount Distribution | Yes | ✅ | Visible as a histogram with two reference lines labeled for provider median and platform median quote amounts. |
| Widget 3: Price vs. Conversion Rate | Yes | ✅ | Visible as a labeled scatter plot with median X/Y reference lines and quadrant guidance text. |
| Widget 4: Platform Benchmark Comparison | Yes | ✅ | Visible as a comparison table with the required metrics, provider/platform values, variance, and percentile band. |
| Small-pool benchmark fallback text | Conditional | ✅ | Not required in the populated default state shown; the FR only requires fallback text when the comparison pool is too small. |

**Extra Elements**:

- Breadcrumb `Analytics / Pricing & Benchmarks` — intentional navigational enhancement beyond the widget list.
- Global `Export Report` CTA — aligns with Alternative Flow A2, even though it is not listed in the screen's field table.
- Full provider portal sidebar and top utility icons — surrounding shell chrome, not a screen-spec violation.

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 8/8 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| None | No evidence-backed UX/UI rule violations identified from the provided static layout. | No change required from this static design review. |

#### Screen 6: Export Report Configuration

**Layout**: `layout-temp/Export Report Config.jpg`

##### Flow Context

- **User arrives from**: Export action from any provider analytics screen with current section pre-selected
- **Screen purpose**: Configure PDF or CSV export for provider analytics data
- **Entry point**: Partially present. The analytics side navigation highlights `Export Report Config`, but the form does not show any pre-selected screen from the originating analytics page.
- **Exit path**: Present. A prominent `Generate Report` CTA is visible both in the page header and at the bottom of the form.
- **Data continuity**: Partial. Filters and export options are present, but the expected carry-over selection from the originating analytics screen is not visible.
- **Flow context issues**: The layout does not demonstrate the required pre-population behavior from Alternative Flow A2.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Page title (`Export Report Config`) | Yes | ✅ | Visible as the primary page heading in `layout-temp/Export Report Config.jpg`. |
| Report type | Yes | ✅ | Radio options for `PDF Summary` and `CSV Detailed` are visible. |
| Screens to include | Yes | ❌⚠️ | The checkbox list is present, but no screen is visibly pre-selected even though Alternative Flow A2 requires the current analytics section to be pre-populated on entry. |
| Date range | Yes | ✅ | Start and end date inputs are visible in a single date-range control. |
| Country filter | No | ✅ | Optional country dropdown is visible. |
| Treatment filter | No | ✅ | Optional treatment dropdown is visible. |
| Email delivery | No | ✅ | Optional email-delivery checkbox is visible with provider-email helper text. |
| Schedule recurring | No | ✅ | Optional recurring checkbox is visible with weekly/monthly/quarterly options. |
| Generate report action | Yes | ✅ | Clear `Generate Report` action is visible in both header and footer positions. |

**Extra Elements**:

- `Report History` table with prior generated exports — useful enhancement beyond the FR field list.
- Breadcrumb `Analytics / Export Report Config` — intentional navigational enhancement beyond the form fields.
- Full provider portal sidebar and top utility icons — surrounding shell chrome, not a screen-spec violation.

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 8/8 (100%)
**Critical Issues**: No visible pre-selection for the originating analytics screen, despite Alternative Flow A2 requiring Screen 6 to open pre-populated with the current section.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-23 Terminology consistency`: the flow says this screen is entered from an `Export` action with the current section pre-populated, but the static layout presents all screen checkboxes in an unselected state, which weakens continuity from the prior analytics screen. | Pre-check the originating analytics section when the user arrives from an export shortcut, and visually indicate that the form was seeded from that screen. |

**Flow Coverage Gaps**:

- Screen 4 omits the required commission-model clarification note and the `Historical exchange rates applied` footer note.
- Screen 6 does not visibly pre-select the originating analytics screen on entry, despite Alternative Flow A2 requiring pre-population.

---

## Action Items

| Priority | Flow | Screen | Issue | Recommendation |
|----------|------|--------|-------|----------------|
| ⚠️ Important | PR-05-F1 | Screen 4 | Required financial disclosure notes are missing from the page. | Add the commission-model clarification note and the `Historical exchange rates applied` footer note. |
| ⚠️ Important | PR-05-F1 | Screen 6 | Export configuration screen does not show the current analytics section pre-selected on entry. | Pre-populate the originating screen selection when arriving from an export CTA on Screens 2–5. |

### Priority Legend

- **🔴 Critical**: Blocks flow progression, breaks data integrity, or causes security/legal risk. Must fix before development.
- **🔴 Critical UX**: Severe usability issue that would prevent users from completing the flow or cause significant confusion. Must fix before development.
- **⚠️ Important**: Functional discrepancy that could cause user confusion or require rework during development. Should fix before development.
- **⚠️ UX Improvement**: Usability or design quality issue that deviates from platform conventions or best practices. Should fix before development.
- **💡 Suggestion**: Cosmetic or minor improvement. Can fix anytime.
- **💡 UX Suggestion**: Minor design enhancement that would improve polish. Can fix anytime.

---

## Notes

- Requirement source: `local-docs/project-requirements/functional-requirements/fr014-provider-analytics-reporting/prd.md`
- Scope excludes Screen 1 because the user requested it skipped and the FR marks it as locked.
- Provider workflow context sourced from `Main Flow: Provider Reviews Analytics Suite` and alternatives `A2`, `B1`, `B2`.
- This verification used only the provider tenant layouts currently present in `layout-temp/` on 2026-05-06.
