# FR-014 - Provider Analytics & Reporting

**Module**: PR-05: Financial Management & Reporting | A-08: Analytics & Reporting
**Feature Branch**: `fr014-provider-analytics-reporting`
**Created**: 2025-11-11
**Version**: 3.7
**Status**: 🟡 Revised — Documentation Approved; Pending Consolidated Verification
**Source**: FR-014 from system-prd.md; SRC-MTG-002 (MTG-002-D03–D06 and O01 as refined by the Product Owner); FR-004, FR-005, and FR-006 approved quote/acceptance/booking contracts; Product Owner approval dated 2026-10-07
**Change Request**: [CR-FR014-20261007-01](change-request-2026-10-07-parent-quote-subquote-analytics.md) — implementation reconciliation required

---

## Executive Summary

The Provider Analytics & Reporting module delivers a **13-screen suite (12 analytical + 1 export config)** split across two tenants: provider and admin.

On the **provider side**, six screens cover the full operational picture — a locked cockpit dashboard for daily triage (Screen 1), four deeper analytical views for conversion performance, patient insights, financial health, and pricing/benchmarks (Screens 2–5), and an export configuration utility (Screen 6). Each screen has a single job and is accessed via the Analytics section of the provider portal.

On the **admin side**, seven screens (Screens 7–13) give Hairline visibility into platform-wide health, provider quality and engagement, patient acquisition, geographic supply/demand gaps, treatment outcomes, financial cashflow, and pricing landscape.

All metrics derive from operational records or calculations over those records. This PRD defines the approved target analytics contract; it does not establish that the current implementation already produces the revised metrics.

The counting boundary is the FR-004 Parent Quote, not its packages or date-price alternatives. Each provider may submit multiple parent quotes per inquiry; each parent contains Quote Options, and each option/date-price combination resolves to an FR-005 Subquote. Acceptance records the exact bottom-level choice in an immutable AcceptanceEvent. Inquiry funnels, parent-quote acceptance rates, accepted-price analytics, and confirmed-booking metrics therefore have distinct grains and MUST NOT be interchanged. See **Analytics Counting & Time Basis** for the shared definitions used by every screen and export.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-XX)**: No direct patient-facing features. Patient behaviour data (inquiry timing, booking patterns, location) feeds the analytics pipeline.
- **Provider Platform (PR-05)**: 6-screen suite (5 screens in the "Analytics" nav + Screen 1 as the platform landing page, not accessed via the Analytics nav section).
- **Admin Platform (A-08)**: 7-screen analytics suite accessible from the admin "Analytics" nav section.
- **Shared Services (S-XX)**: Analytics data pipeline service; report generation service.

### Provider Platform (PR-05) Scope

- Main Dashboard / Cockpit (Screen 1) — daily triage
- Performance & Conversion (Screen 2) — funnel efficiency and TTFQ trends
- Patient Analytics (Screen 3) — patient demographics, satisfaction, and journey
- Finance & Payouts (Screen 4) — revenue breakdown and payout schedule
- Pricing & Benchmarks (Screen 5) — pricing analysis and platform comparison
- Export Report Configuration (Screen 6) — generate PDF/CSV exports

### Admin Platform (A-08) Scope

- Platform Overview Dashboard (Screen 7) — platform health at a glance
- Provider Performance & Engagement (Screen 8) — provider quality and activity monitoring
- Patient Acquisition & Funnel (Screen 9) — how patients enter and move through the platform
- Geographic Intelligence (Screen 10) — demand vs. supply by country
- Treatment Outcomes (Screen 11) — satisfaction-based outcomes
- Financial Health & Cashflow (Screen 12) — platform financial risk and revenue health
- Pricing Intelligence (Screen 13) — pricing landscape across providers and treatments

### Communication Structure

**In Scope**:

- Email notifications for scheduled report delivery (provider-configured)
- In-app alerts when provider metrics fall below defined thresholds (TTFQ SLA breach)

**Out of Scope**:

- Channel attribution (organic, paid ads, social media) — not tracked in database
- Clinical outcome data (graft survival, hair density results) — not tracked in database
- Real-time collaborative dashboard viewing (future enhancement)

### Entry Points

- **Provider**: "Analytics" nav item → defaults to Screen 2 (Performance); Screen 1 (Main Dashboard) is the platform landing page, not the analytics section entry
- **Admin**: "Analytics" nav item → defaults to Screen 7 (Platform Overview)
- **Export**: "Export Report" button available on all provider analytics screens

---

## Business Workflows

### Main Flow: Provider Reviews Analytics Suite

**Actor**: Provider user with analytics access
**Trigger**: Provider clicks "Analytics" in the nav
**Outcome**: Provider navigates between the 6 provider screens (Screen 1 as landing page + Screens 2–6 via Analytics nav) to understand performance, patients, and financials

1. Provider lands on Performance & Conversion (Screen 2) — checks funnel health for the week
2. Provider navigates to Patient Analytics (Screen 3) — reviews patient location and satisfaction trends
3. Provider navigates to Finance & Payouts (Screen 4) — verifies this month's revenue and upcoming payout
4. Provider navigates to Pricing & Benchmarks (Screen 5) — checks positioning vs. platform median
5. Provider optionally generates a PDF/CSV export via Screen 6

### Main Flow: Admin Monitors Platform Health

**Actor**: Admin
**Trigger**: Admin clicks "Analytics" in admin nav
**Outcome**: Admin reviews platform health, flags issues, and takes action

1. Admin lands on Platform Overview (Screen 7) — checks TTFQ distribution and GMV summary
2. Admin navigates to Provider Performance & Engagement (Screen 8) — reviews underperforming and dormant providers
3. Admin navigates to Patient Acquisition & Funnel (Screen 9) — checks inquiry volume and funnel drop-offs
4. Admin navigates to Geographic Intelligence (Screen 10) — identifies underserved markets
5. Admin navigates to Treatment Outcomes (Screen 11) — reviews cancellation rates and aftercare activation
6. Admin navigates to Financial Health & Cashflow (Screen 12) — reviews payout obligations and cash-at-risk
7. Admin navigates to Pricing Intelligence (Screen 13) — checks for outlier providers on pricing
8. Admin takes action on flagged providers (links through to provider management in FR-015)

### Alternative Flows

**A1 — Drill-down from any chart**: Clicking a chart element (funnel stage, map region, table row, bar) opens the relevant filtered list in the corresponding operational module (Inquiries, Quotes, Bookings, Payments, Schedule).

**A2 — Export from any screen**: Provider clicks "Export" button → reaches Screen 6 pre-populated with the current screen's section selected.

**B1 — Analytics pipeline delay**: Non-blocking banner shown; cached data displayed with last-updated timestamp.

**B2 — Low sample (<30 inquiries for provider)**: Helper copy shown on affected widgets; partial data still rendered.

---

## Screen Specifications

---

### Provider Platform (PR-05)

#### Screen 1: Main Dashboard (Cockpit)

> **STATUS: LAYOUT LOCKED.** The Product Owner approved a formula/metric-label-only exception on 2026-10-07 through CR-FR014-20261007-01 for TTFQ, the booking funnel, and accepted-but-unpaid aging. The existing sections, widget count, chart types, filters, and responsive layout remain locked; this exception does not authorize a redesign.
> Design reference: Figma node 6358-111596

**Purpose**: Single scrollable page for daily triage. Three vertically stacked sections (A: Inbox, B: Performance, C: Financials). No tabs.

**Layout**: Header (filters) → Section A → Section B → Section C. Collapse to single-column on ≤1024px.

---

##### Header — Global Filters

| Field | Type | Default |
|-------|------|---------|
| Time range | Dropdown | Last 4 weeks (options: Today / This week / Last 4 weeks / Last 12 weeks / Custom) |
| Country | Multi-select dropdown | All countries |

**Global UX**: Cross-filtering — any widget selection updates all sections. Tooltips state metric definition + numerator/denominator + time basis. Localize dates/currencies/timezone. Skeletons on load.

---

##### Section A — Inbox

###### Tile 1: New Inquiries

- Value: Today count + This week count (dual display)
- Tap → Inquiries list (time filter applied)

###### Tile 2: Time to First Quote (TTFQ)

- Value: p50 and p90 vs SLA (compact dual-bullet)
- Color: Green (p50 ≤ SLA and p90 ≤ 2×SLA) · Amber (p50 ≤ SLA and p90 > 2×SLA) · Red (p50 > SLA)
- Tap → Inquiries list grouped by coordinator

**TTFQ formula**: earliest first-submission `Parent Quote.sent_at − inquiry.created_at` per `(providerId, inquiryId)` (elapsed wall time; display in provider timezone). Draft creation, option/date-price creation, later parent quotes, edits, and resends do not reset the first-response timestamp. Exclude auto-acks; calls/messages do not stop the clock.

###### Table: Inquiry Queue

| Column | Notes |
|--------|-------|
| Received | Relative time + SLA countdown timer |
| Patient | ID-masked (HP102589-0001 · "Aylin K****") |
| Age | Patient age |
| Problem | Treatment area |
| Country | Patient country |
| Actions | View link |

Row badges: `New` / `Needs Info` / `Awaiting Price`. Default sort: badge priority then received time ascending. 10 per page.

---

##### Section B — Performance (2×2 Grid)

###### B1: Inquiry → Booking Conversion

- Chart: Funnel chart
- Stages: Inquiries → Qualified → Quoted → Accepted → Confirmed booking
- Each stage: Count + Step % (stage ÷ previous stage)
- Footer: Overall booking conversion = Confirmed bookings ÷ Inquiries
- Qualified = not spam + mandatory fields present (age, problem, contact)
- Confirmed booking = successful deposit or first installment charge confirms the FR-006 Booking. `In Progress` means procedure started via FR-010 and is not the payment-confirmation label.
- Count distinct inquiry/provider pairs in a single inquiry cohort cumulatively through each reached stage, per Analytics Counting & Time Basis; multiple parent quotes and subquotes do not multiply the funnel.
- Drill-down: click stage → filtered Inquiries list

###### B2: TTFQ vs SLA

- Chart: Bullet chart (p50 + p90, SLA as target marker)
- Axis: 0 → max(3×SLA, 1.2×p90), units = minutes (render h:m)
- Color: Green/Amber/Red per TTFQ formula above
- Drill-down: click → Inquiries list grouped by coordinator

###### B3: Booking Intensity vs Monthly Average (Next 6 Weeks)

- Chart: Calendar heatmap (6 rows × 7 cols, Mon→Sun)
- Colored metric: Intensity Index = `(Bookings_on_day ÷ MonthlyDailyAvg_for_that_day's_month) × 100`
- Color scale: ≤50% Cool · 50–90% Below avg · 90–110% Neutral · 110–150% Above avg · >150% Hot
- Cell tooltip: `Bookings: N • Monthly avg: m/day • Index: X%`
- Drill-down: click cell → Schedule day view
- Baseline priority: 12-month same-month avg → current MTD → rolling 90-day
- Index clamped 0–300% for coloring; actual value in tooltip

###### B4: Patient Location Breakdown

- Chart: Donut (top 8 countries by inquiry share + Other)
- Center: total Inquiries in range
- Slice labels: `CC (ISO-2) • %`
- Slice border: thin/neutral <20% booked rate · medium/amber 20–40% · thick/green >40%
- Tooltip: `Country • Inquiries: N • Booked: B • Booked rate: R%`
- Drill-down: click slice → filtered Inquiries list

---

##### Section C — Financials (2×2 Grid)

###### C1: Earnings Trend

- Chart: Area line chart (weekly, X = ISO week start, Y = income in provider currency)
- Single series: Income only
- Drill-down: click week → Earnings report filtered to that week

###### C2: Revenue by Treatment

- Chart: Pareto bar chart (ranked bars + cumulative % line)
- X = treatment (dynamic), Y₁ = income, Y₂ = cumulative %
- Top N + Other; drill-down: click bar → Cases list filtered by treatment

###### C3: Quote → Payment Aging (Accepted but Unpaid)

- Chart: Stacked horizontal bar
- Buckets: 0–24h · 1–3d · 4–7d · 8–14d · >14d
- X = count of accepted selections awaiting successful initial payment; optional legend by treatment (top 3) or country
- Age = snapshot time − `AcceptanceEvent.acceptedAt`; count one pending Booking/AcceptanceEvent with a valid exclusive payment-window hold. Exclude cancelled selections, superseded acceptance events, expired holds, and `Payment Window Expired` bookings, even if a flat quote status still says Accepted.
- Drill-down: click bucket → Accepted Quotes list resolved to the exact accepted subquote and pending booking; retain the same chart and buckets. Older buckets may legitimately be empty with the default 48-hour hold; use the actual configured deadline, not an assumed fixed limit.

###### C4: Payouts — History & Upcoming

- Chart: Column bar (monthly, last 6–12 months) + inline table (2–3 rows)
- Inline table columns: Type, Period, Amount, Scheduled Date, Cadence
- Drill-down: click bar → Payout statements list (CSV/PDF export)

---

##### States

- Low sample (<30 inquiries): helper copy; still render counts
- Loading: skeletons for all tiles and charts
- Error: non-blocking banners + retry; log telemetry
- PII: patient names masked throughout

---

#### Screen 2: Performance & Conversion

**Purpose**: Deep analysis of how efficiently the provider converts inquiries to bookings, including TTFQ trends and benchmarking.

**Filters**: Time range (same options as Screen 1 global) + Country + Treatment type (multi-select)

---

##### Widget 1: Funnel Conversion Trend

| Property | Value |
|----------|-------|
| Chart type | Multi-line chart (one line per funnel stage) |
| X axis | Week or month (toggle) |
| Y axis | Conversion % to that stage from Inquiries |
| Lines | Qualified % · Quoted % · Accepted % · Confirmed booking % |
| Drill-down | Click a point → Inquiries list filtered to that stage + time period |

**Calculation**: Each stage % = distinct inquiry/provider pairs in the selected inquiry cohort that have reached that stage by the reporting cutoff ÷ all inquiry/provider pairs in that cohort. Counts are cumulative, not mutually exclusive highest-stage buckets. Use the shared cohort and cutoff definitions in Analytics Counting & Time Basis.

---

##### Widget 2: Conversion Breakdown by Treatment Type

| Property | Value |
|----------|-------|
| Chart type | Grouped bar chart |
| X axis | Treatment type (from catalog) |
| Y axis | Booking conversion % (Inquiries → Confirmed booking) |
| Groups per bar | Inquiries count, Quoted count, Confirmed booking count |
| Drill-down | Click bar → filtered Inquiries list for that treatment |

**Data source**: Parent Quote treatment context joined with the inquiry cohort and FR-005/FR-006 handoff. Deduplicate `(providerId, inquiryId, treatmentId)` within each treatment segment before counting stages; child options, date-price records, and quote revisions MUST NOT multiply counts. An inquiry may appear in more than one treatment segment, so segment counts are not additive.

---

##### Widget 3: Conversion Breakdown by Patient Country

| Property | Value |
|----------|-------|
| Chart type | Horizontal ranked bar chart |
| Y axis | Patient country (top 10 by inquiry volume) |
| X axis | Booking conversion % (Inquiries → Confirmed booking) |
| Secondary bar | Inquiry count (context for the rate) |
| Drill-down | Click bar → filtered Inquiries list for that country |

**Data source**: `inquiries.patient_id → patients.location_id → countries.name`, with temporary fallback to legacy `patients.location` only for unmigrated rows.

---

##### Widget 4: Quote Acceptance Rate Trend

| Property | Value |
|----------|-------|
| Chart type | Line chart |
| X axis | Week or month (toggle) |
| Y axis | Parent-quote acceptance rate = distinct accepted parent quotes ÷ distinct submitted parent quotes in the same first-submission cohort |
| Drill-down | Click point → parent Quotes list for that first-submission cohort, with accepted subquote provenance where present |

---

##### Widget 5: TTFQ Trend Over Time

| Property | Value |
|----------|-------|
| Chart type | Dual-line chart (p50 line + p90 line) |
| X axis | Week or month (toggle) |
| Y axis | Minutes (render as h:m) |
| Reference line | SLA target |
| Color band | Green/Amber/Red zones based on SLA thresholds |
| Drill-down | Click point → Inquiries list for that period sorted by TTFQ |

---

##### Widget 6: Cancellation & No-Show Rate

| Property | Value |
|----------|-------|
| Chart type | Two KPI tiles + trend sparklines |
| Tile 1 | Cancellation rate = cancelled (post-confirmed) ÷ confirmed bookings |
| Tile 2 | No-show rate = no-show ÷ confirmed bookings |
| Sparkline | Rate trend over selected period |
| Drill-down | Click tile → filtered Quotes/Bookings list |

**Data source**: FR-006 Booking lifecycle and no-show records, counted once per confirmed booking. Draft/quote expiry and `Payment Window Expired` before confirmation are not post-confirmation cancellations or no-shows. Historical acceptance remains recorded separately.

---

##### Widget 7: Platform Benchmarks (Anonymised)

| Property | Value |
|----------|-------|
| Chart type | Comparison table with variance indicators |
| Metrics | TTFQ p50 · Conversion rate · Quote acceptance rate · Avg rating |
| Columns | Provider value · Platform median · Variance (±%) · Percentile |
| Color | Green (above median) · Red (below median) |

**Business rule**: Platform median calculated from all active providers in the same quarter; fully anonymised. Requires minimum 5 providers in comparison pool; if insufficient, display "Benchmark unavailable — not enough providers in your segment."

---

**Business Rules**:

- All widgets share the same time range and country filter
- Treatment type filter applies to all conversion widgets (not to TTFQ)
- Low-sample handling follows the global Data Quality Rule 7 (<30 inquiries → helper copy, data still rendered); no widget-specific override applies

---

#### Screen 3: Patient Analytics

**Purpose**: Understanding who the provider's patients are, where they come from, how satisfied they are, and how long their journey takes.

**Filters**: Time range + Country

---

##### Widget 1: Full Patient Location Breakdown

| Property | Value |
|----------|-------|
| Chart type | Ranked table + donut chart (linked) |
| Table columns | Country · Inquiries · Booked · Booked rate · Avg rating |
| Table | All countries (not capped at 8); sortable by any column |
| Donut | Top 10 countries by inquiry volume + Other |
| Drill-down | Click row/slice → Inquiries list filtered to that country |

---

##### Widget 2: New vs. Returning Patients

| Property | Value |
|----------|-------|
| Chart type | Donut (current period split) + trend line over time |
| Definition | New = patient_id appearing for first time in inquiries table · Returning = patient_id with prior inquiry |
| Trend | New vs. Returning count per month over selected range |
| Drill-down | Click segment → Patient list filtered by type |

**Data source**: `inquiries.patient_id` — count distinct patient_ids with no prior `created_at` before the range start = New; all others = Returning.

---

##### Widget 3: Patient Journey Time

| Property | Value |
|----------|-------|
| Chart type | Two KPI tiles + distribution histogram |
| Tile 1 | Median days from inquiry → payment (p50) |
| Tile 2 | p90 days from inquiry → payment |
| Histogram | Distribution of journey durations in days (binned: 0–7d · 8–14d · 15–30d · 31–60d · >60d) |
| Drill-down | Click histogram bin → Inquiries list filtered to that journey-duration range |

**Calculation**: first successful initial-payment capture time that confirms the FR-006 Booking − `inquiry.created_at`, for bookings first confirmed within the selected range. Resolve the booking through its AcceptanceEvent and selected subquote; count the inquiry once. Payment-attempt creation, failed attempts, later installments, and retries of the same successful event MUST NOT add journey observations.

---

##### Widget 4: Review Sub-Scores by Treatment

| Property | Value |
|----------|-------|
| Chart type | Grouped bar chart |
| X axis | Treatment type |
| Y axis | Score (1–5) |
| Groups per bar | Overall · Results · Staff · Facility · Value |
| Data source | `reviews` table: `overall_rating`, `results_rating`, `staff_rating`, `facility_rating`, `value_rating` joined via `reviews.quote_id → quotes.treatment_id` |
| Drill-down | Click bar → Reviews list filtered to that treatment |

---

##### Widget 5: Treatment Preference Distribution

| Property | Value |
|----------|-------|
| Chart type | Horizontal ranked bar chart |
| Y axis | Treatment type |
| X axis | Inquiry count + Booking count (dual bars) |
| Purpose | What treatments patients request most vs. what actually gets booked |
| Drill-down | Click bar → filtered Inquiries or Bookings list |

**Data source**: `quotes.treatment_id` grouped by status (all inquiries vs. those reaching `inprogress`/`completed`).

---

##### Widget 6: Aftercare Activation Rate

| Property | Value |
|----------|-------|
| Chart type | KPI tile + trend sparkline |
| Value | Aftercare plans activated ÷ completed treatments |
| Drill-down | Click → Aftercare records list |

**Data source**: `aftercare` records created, joined to `quotes` with status `completed`.

---

**Business Rules**:

- Patient age distribution: only include if patient age is directly available in the data model. Do NOT estimate or derive from medical questionnaire free text. If unavailable, this widget is omitted.
- Returning patient definition: based on the same provider's patient base (not platform-wide repeat visits).
- PII: no patient names or identifiers shown; all aggregated.

---

#### Screen 4: Finance & Payouts

**Purpose**: Full financial picture — revenue breakdown, refunds, installment health, and complete payout history.

**Filters**: Time range + Country + Treatment type

---

##### Widget 1: Revenue Trend

| Property | Value |
|----------|-------|
| Chart type | Area line chart |
| X axis | Week / Month / Quarter (toggle) |
| Y axis | Income amount (provider currency) |
| Single series | Income (captured payments only) |
| Drill-down | Click period → Payments list filtered to that period |

**Calculation**: `SUM(payments.amount)` where `payment_status = 'completed'` and `payment_type ≠ 'refund'`, bucketed by `payments.created_at`.

---

##### Widget 2: Revenue by Treatment — Full Breakdown

| Property | Value |
|----------|-------|
| Chart type | Horizontal ranked bar chart (full list, paginated if >15) |
| Y axis | Treatment name (all, not capped) |
| X axis | Income amount |
| Secondary metric | % of total revenue |
| Drill-down | Click bar → Payments list filtered to that treatment |

---

##### Widget 3: Revenue by Patient Country

| Property | Value |
|----------|-------|
| Chart type | Horizontal ranked bar chart |
| Y axis | Patient country (top 10 + Other) |
| X axis | Income amount |
| Secondary metric | Patient count |
| Drill-down | Click bar → Payments list filtered to that country |

**Data source**: `payments.patient_id → patients.location_id → countries.name`, with temporary fallback to legacy `patients.location` only for unmigrated rows.

---

##### Widget 4: Commission & Net Revenue

| Property | Value |
|----------|-------|
| Chart type | Two KPI tiles + trend line (both on same chart) |
| Tile 1 | Total income (gross) |
| Tile 2 | Commission deducted |
| Trend | Gross income line + commission deducted area, stacked |

**Calculation**: Commission deducted = sum of the effective provider commission for each completed payment in range. Effective commission must respect the provider's configured commission model:

- Percentage model: `payments.amount × (effective_commission_percentage / 100)`
- Flat-rate model: `effective_commission_amount` per completed booking/payment

Gross and net are displayed in provider currency.

---

##### Widget 5: Refunds

| Property | Value |
|----------|-------|
| Chart type | Two KPI tiles + trend |
| Tile 1 | Total refund amount (period) |
| Tile 2 | Refund rate = refund count ÷ total completed payment count |
| Trend | Monthly refund rate over selected range |
| Drill-down | Click → Payments list filtered to refund type |

**Data source**: `payments.payment_type = 'refund'` or `payment_status = 'refunded'`.

---

##### Widget 6: Installment vs. Full Payment Split

| Property | Value |
|----------|-------|
| Chart type | Donut + KPI summary |
| Segments | Installment payments · Full payments |
| KPI | Avg number of installments for installment plans |
| Trend | Monthly installment adoption rate |
| Drill-down | Click segment → Payments list filtered by installment flag |

**Data source**: `payments.is_installment`.

---

##### Widget 7: Cash-at-Risk Summary

| Property | Value |
|----------|-------|
| Chart type | KPI tile + link to Main Dashboard Section C3 for full aging detail |
| Value | Sum of accepted subquote total prices for selections awaiting initial payment with a valid hold; label as potential accepted booking value, not captured revenue or outstanding installment debt |
| Count | Distinct pending bookings/AcceptanceEvents in each aging bucket, following Screen 1 C3 exclusions and deadline checks |
| Note | This is a summary view; the full aging stacked bar is in Screen 1 Section C3 |

---

##### Widget 8: Payout History & Schedule

| Property | Value |
|----------|-------|
| Chart type | Column bar chart (monthly, full history) + paginated table below |
| Bar chart | Last 12 months of disbursed payouts |
| Table columns | Period · Amount · Status (Disbursed / Upcoming / Scheduled) · Disbursed date · Cadence |
| All rows | Full history (not limited to last 2 as in the Main Dashboard widget) |
| Drill-down | Click bar or row → Payout statement detail (CSV/PDF export) |

---

**Business Rules**:

- Income = payments with `payment_status = 'completed'` and `payment_type ≠ 'refund'`
- Commission is calculated from the effective provider commission configuration, not from a single percentage-only field; provider screens must display a note clarifying whether the period includes percentage-based deductions, flat-rate deductions, or both
- All amounts in provider currency; FX rates locked at payment `created_at` date; footer note "Historical exchange rates applied"
- Payout history only shows payouts that have been processed (not projected future payouts beyond the next scheduled one)
- Aggregate each completed payment, refund, commission deduction, or payout once at its owning record grain before joining quote provenance. Unselected options and repeated booking/acceptance notifications MUST NOT multiply revenue or deductions; this revision does not change commission, installment, refund, or payout policy.

---

#### Screen 5: Pricing & Benchmarks

**Purpose**: Understand the prices patients actually accepted, their descriptive relationship with parent-quote acceptance rates, and the provider's position relative to platform peers. This screen does not measure the full offered-price market or establish that price causes conversion changes.

**Filters**: Time range + Country + Treatment type

---

##### Widget 1: Average Accepted Price by Treatment

| Property | Value |
|----------|-------|
| Chart type | Bar chart + trend line |
| X axis | Treatment type |
| Y axis | Average accepted subquote total price (provider reporting currency) |
| Trend overlay | Provider's own average accepted price over time, bucketed by AcceptanceEvent.acceptedAt |
| Drill-down | Click bar → Quotes list filtered to accepted selections for that treatment and acceptance period |

---

##### Widget 2: Accepted Price Distribution

| Property | Value |
|----------|-------|
| Chart type | Histogram |
| X axis | Accepted subquote total price (binned, e.g., 0–1k · 1k–2k · 2k–3k · 3k–5k · >5k; dynamic bins based on accepted-price range) |
| Y axis | Accepted selection count (one observation per accepted parent quote) |
| Reference lines | Median accepted price · Platform median accepted price (anonymised) |
| Drill-down | Click bin → Quotes list filtered to accepted selections in that price range and acceptance period |

---

##### Widget 3: Accepted Price vs. Parent-Quote Acceptance Rate

| Property | Value |
|----------|-------|
| Chart type | Scatter plot |
| X axis | Average accepted subquote price among accepted parents in the selected first-submission cohort, per treatment type |
| Y axis | Distinct accepted parent quotes ÷ all submitted parent quotes in that same cohort, per treatment type |
| Points | One point per treatment type (labelled) |
| Reference lines | Platform median X (average accepted price) and platform median Y (parent-quote acceptance rate), using the same cohort and reporting cutoff |
| Purpose | Descriptive comparison of accepted prices and acceptance rates across treatments; does not show conversion probability at an offered price or prove a causal price effect |

**Note**: A treatment needs a non-zero submitted-parent denominator and at least one accepted selection to have both coordinates. If fewer than 3 treatment types qualify, replace the chart with "Insufficient treatment variety to compare accepted prices and acceptance rates." Unaccepted parents remain in Y's denominator but contribute no amount to X; tooltips show both sample sizes and the first-submission cohort basis, which differs from acceptance-period pricing widgets.

---

##### Widget 4: Platform Benchmark Comparison

| Property | Value |
|----------|-------|
| Chart type | Comparison table |
| Rows (metrics) | TTFQ p50 · Overall booking conversion rate · Parent-quote acceptance rate · Average accepted price · Avg overall rating · Avg results rating |
| Columns | Provider value · Platform median · Variance (±%) · Percentile band (Bottom 25% / Mid 50% / Top 25%) |
| Color coding | Green = above median · Amber = within 10% below · Red = >10% below |
| Drill-down | Click metric row → corresponding detailed screen (e.g., TTFQ → Screen 2 Widget 5) |

**Business rule**: Benchmark pool = all active providers with ≥30 inquiries in the same rolling 12-month window. Minimum 5 providers in pool required. If pool is too small, display "Not enough peer providers to generate a meaningful benchmark yet."

---

**Business Rules**:

- Provider identity is fully anonymised in all benchmark calculations
- Benchmark data is refreshed weekly (not real-time)
- Amount metrics use only immutable accepted-selection prices, including the accepted promotion; never substitute a minimum, maximum, average, or sum of unaccepted alternatives. Historical acceptance remains an observation after later cancellation or hold expiry; those outcomes are measured separately.
- Standalone price widgets use the acceptance-time cohort. The scatter explicitly uses the parent first-submission cohort so both axes refer to the same offered parent population.
- Price displayed in provider reporting currency; preserve the accepted currency and locked exchange-rate provenance and apply Rule 10 for any additional reporting-currency conversion. Apply the same historical conversion basis to provider and peer amounts; current package prices or today's FX MUST NOT rewrite the accepted value.
- Price benchmarks include only peers with accepted-price observations; the existing minimum 5-provider benchmark pool still applies to that metric. Unaccepted parents are not zero-price observations.

---

#### Screen 6: Export Report Configuration

**Purpose**: Allow providers to generate PDF or CSV exports of any analytics screen's data.

**Data Fields**:

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Report type | Radio | Yes | PDF Summary or CSV Detailed |
| Screens to include | Checkboxes | Yes | Performance, Patient Analytics, Finance & Payouts, Pricing & Benchmarks (Screen 1 is excluded — it contains real-time operational data not suitable for static reports) |
| Date range | Date picker | Yes | Max 12-month span |
| Country filter | Dropdown | No | Optional |
| Treatment filter | Dropdown | No | Optional |
| Email delivery | Checkbox | No | Sends to provider's registered email |
| Schedule recurring | Checkbox | No | Weekly / Monthly / Quarterly |

**Business Rules**:

- PDF reports include provider logo sourced from `providers.profile_image`; no provider-specific color theming (platform default palette is used) — schema does not define brand color fields and this is intentional for v1
- Report generation <60 seconds; async queue for large datasets
- Generated reports stored 7 days for re-download from Report History section
- Email delivery: PDF attachment + secure link (expires 48 hours)
- Max 5 active recurring configurations per provider
- PDF and CSV MUST use the same counting units, cohorts, cutoff, accepted-price eligibility, and financial deduplication as the included screens. State the metric definition, sample size, reporting currency, FX basis, and data-as-of time. For detailed quote/acceptance rows, retain authorized inquiry/provider IDs, parent/option/date-price/subquote IDs, AcceptanceEvent and booking IDs where present, accepted aggregate versions, and immutable price/currency provenance; unaccepted parent rows have no accepted amount or accepted-choice IDs.

---

### Admin Platform (A-08)

#### Screen 7: Platform Overview Dashboard

**Purpose**: Platform health at a glance — one scrollable page with three sections mirroring the provider dashboard structure but aggregated across all providers.

**Filters**: Time range (same options) + Country + Provider (optional, defaults to All)

**Layout**: Three sections (A: Operations, B: Performance, C: Finance). Responsive layout required: multi-column on desktop, reduced-density stacked layout on tablet/mobile, with a single-column fallback on ≤1440px.

---

##### Section A — Operational Health

###### Tile 1: Active Providers

- Value: Count of providers with `status = active`
- Sub-value: New providers onboarded in period
- Tap → Provider Management (FR-015)

###### Tile 2: Total Inquiries

- Value: Platform-wide inquiry count in period
- Sub-value: % change vs. prior equivalent period
- Tap → Inquiries list (admin)

###### Tile 3: New Patients Registered

- Value: `patients.created_at` count in period
- Tap → Patient Management (FR-016)

###### Tile 4: Provider TTFQ Health Distribution

- Chart: Donut (Green / Amber / Red provider counts)
- Value: Count and % in each tier
- Tap → Screen 8 filtered to Red tier

###### Tile 5: Provider Engagement Rate

- Value: % of active providers who first submitted at least 1 parent quote in last 30 days
- Sub-value: Count of dormant providers (0 first-submitted parent quotes in last 30 days); drafts, child records, edits, and resends do not count as new submissions
- Tap → Screen 8 engagement section filtered to dormant

---

##### Section B — Performance Signals

###### B1: Platform-Wide Conversion Funnel

- Chart: Funnel chart (same 5 stages as provider funnel, but distinct platform inquiries, not summed provider funnels)
- Shows: Count + Step % for each stage
- Footer: Overall platform booking conversion = Confirmed booking inquiries ÷ Inquiries
- Drill-down: click stage → admin Inquiries list filtered to that stage

###### B2: Platform TTFQ Distribution

- Chart: Bullet chart (platform p50 + p90 vs SLA default target)
- Shows: Distribution across all providers
- Drill-down: click → Screen 8 (Provider Performance & Engagement) sorted by TTFQ

###### B3: Top Patient Origin Countries

- Chart: Donut (top 8 countries by inquiry volume + Other)
- Drill-down: click slice → Screen 9 filtered to that country

###### B4: Treatment Type Distribution

- Chart: Donut (inquiry share by treatment type)
- Drill-down: click slice → Screen 11 filtered to that treatment

---

##### Section C — Financial Summary

###### C1: Platform GMV (Period)

- Value: `SUM(payments.amount)` where `payment_status = 'completed'`, period
- Sub-value: % change vs. prior period
- Drill-down → Screen 12

###### C2: Commission Earned (Period)

- Value: Sum of effective provider commission deductions for completed payments in period, respecting each provider's configured commission model (`percentage` or `flat rate`)
- Sub-value: As % of GMV
- Drill-down → Screen 12

###### C3: Upcoming Provider Payout Obligations

- Value: Total payout amount due to providers in next 30 days
- Sub-value: Number of providers in next payout cycle
- Drill-down → Screen 12

###### C4: Platform Cash-at-Risk

- Value: Total accepted subquote value in active pending initial-payment holds, platform-wide; same eligibility as Screen 1 C3 and Screen 4 Widget 7
- Sub-value: Count of active pending selections >14 days aging (may be zero under the default 48-hour hold); expired windows are not active cash risk
- Drill-down → Screen 12

---

**Business Rules**:

- Default time range: Last 4 weeks (same as provider dashboard)
- Provider TTFQ health tiers use the platform-wide SLA target (admin-configurable, stored in admin settings); there are no per-provider SLA overrides in this version
- Section A tiles always show current snapshot (not historical); B and C sections respect the time range filter

---

#### Screen 8: Provider Performance & Engagement

**Purpose**: Two-section screen — Performance (conversion quality) and Engagement (activity/dormancy). These are distinct jobs: performance tells you how well a provider works; engagement tells you whether they're working at all.

**Filters**: Time range + Country + TTFQ health tier (All / Green / Amber / Red) + Engagement status (All / Active / At Risk / Dormant)

---

##### Section A — Performance

###### Widget 1: Provider League Table

| Column | Value |
|--------|-------|
| Provider | Name + country flag |
| TTFQ p50 | Value + color badge |
| Conversion rate | Distinct provider inquiry cohort → Confirmed booking % |
| Quote acceptance rate | Distinct accepted parent quotes ÷ distinct submitted parent quotes in the same first-submission cohort |
| Avg overall rating | Star rating (from reviews) |
| Quote response rate | Distinct distributed inquiries answered ÷ distinct inquiries distributed to this provider in the same distribution cohort |
| vs. Platform | Variance column for conversion rate (+/−%) |
| Status | Health color badge (Green / Amber / Red based on TTFQ + conversion composite) |

- Sortable by any column
- Default sort: TTFQ status (Red first) then conversion rate ascending
- Paginated: 20 per page
- Drill-down: click row → provider's own analytics view (read-only admin view of provider's Screen 2)

###### Widget 2: Performance Distribution

| Property | Value |
|----------|-------|
| Chart type | Scatter plot |
| X axis | TTFQ p50 (minutes) |
| Y axis | Conversion rate (%) |
| Points | One per provider (anonymised label: "Provider A", "Provider B", etc.) — except when admin is on provider detail view |
| Reference lines | Platform median TTFQ · Platform median conversion rate |
| Quadrants | Fast + High conversion (ideal) · Slow + Low conversion (needs support) |
| Drill-down | Click point → that provider's detail |

---

##### Section B — Engagement

###### Widget 3: Provider Activity Table

| Column | Value |
|--------|-------|
| Provider | Name + country |
| Last active | `MAX(action_at)` from `provider_activity_logs` for that `provider_id`; for last login specifically use `MAX(action_at) WHERE action_type = 'login'` |
| Quotes this month | Distinct parent quotes first submitted in current calendar month; no extra counts for options, date-price records, versions, or resends |
| Inquiry response rate | Distinct distributed inquiries answered ÷ distinct inquiries distributed to this provider (last 30-day distribution cohort) |
| Status | Active (activity in last 7d) · At Risk (7–30d) · Dormant (>30d no activity) |

- Filter by status (Active / At Risk / Dormant)
- Drill-down: click row → provider detail in FR-015

###### Widget 4: New Provider Ramp

| Property | Value |
|----------|-------|
| Chart type | Line chart (multiple series) |
| X axis | Days since onboarding (0–90 days) |
| Y axis | Cumulative distinct parent quotes first submitted |
| Series | Each provider onboarded in the selected period (one line each, anonymised) |
| Reference line | Platform average ramp curve |
| Purpose | Identify new providers who are struggling to get started |

**Data source**: Providers with `created_at` within the selected period; parent first-submission `sent_at − providers.created_at` for days-since-onboarding offset. Count each parent identity once, regardless of later versions, resends, or child record counts.

###### Widget 5: Engagement Health Summary

| Property | Value |
|----------|-------|
| Chart type | Three KPI tiles |
| Tile 1 | Active providers count (activity in last 7 days) |
| Tile 2 | At-risk providers count (7–30 days no activity) |
| Tile 3 | Dormant providers count (>30 days no activity) |

---

**Business Rules**:

- Provider identity is NOT anonymised to the admin (admin must be able to identify and contact providers)
- Last-activity data is sourced from `provider_activity_logs.action_at` (canonical activity log); last active = `MAX(action_at)` per provider; last login = `MAX(action_at) WHERE action_type = 'login'` per provider user. Do not use `provider_users.last_login_at` — this field does not exist in the schema.
- "Inquiry response rate" follows the shared distinct-inquiry distribution cohort definition and MUST stay between 0% and 100%. If authoritative distribution records are unavailable, display "Response rate unavailable — distribution data missing"; do not substitute parent quote count or total platform inquiries as the denominator.
- Engagement status thresholds (7d / 30d) are configurable by admin

---

#### Screen 9: Patient Acquisition & Funnel

**Purpose**: How patients enter the platform and move through the inquiry-to-booking funnel. Affiliate acquisition tracked where available.

**Filters**: Time range + Country + Treatment type

**Note**: Channel attribution (organic, paid, social) is NOT available — this screen covers volume trends, funnel efficiency, and affiliate-sourced traffic only.

---

##### Widget 1: Inquiry Volume Trend

| Property | Value |
|----------|-------|
| Chart type | Area line chart |
| X axis | Week or month (toggle) |
| Y axis | Inquiry count |
| Comparison overlay | Prior equivalent period (dashed line) |
| Drill-down | Click period → admin Inquiries list for that period |

---

##### Widget 2: Platform Funnel Trend Over Time

| Property | Value |
|----------|-------|
| Chart type | Multi-line chart (one line per stage) |
| X axis | Month |
| Y axis | Conversion % to that stage from Inquiries |
| Lines | Qualified % · Quoted % · Accepted % · Confirmed booking % |
| Purpose | Show whether platform-wide conversion is improving or declining |
| Drill-down | Click line point → admin Inquiries list filtered to that stage + month |

---

##### Widget 3: New vs. Returning Patients

| Property | Value |
|----------|-------|
| Chart type | Stacked bar chart (monthly) + KPI tiles |
| Bars | New patient count + Returning patient count per month |
| Tile 1 | New patient rate (period) |
| Tile 2 | Returning patient rate (period) |
| Definition | New = first inquiry ever · Returning = has prior inquiry on record |
| Drill-down | Click bar segment → Patient list filtered by type and period |

---

##### Widget 4: Patient Journey Time (Platform-Wide)

| Property | Value |
|----------|-------|
| Chart type | Two KPI tiles + distribution histogram |
| Tile 1 | Platform median days inquiry → payment (p50) |
| Tile 2 | Platform p90 days inquiry → payment |
| Histogram | Distribution across all converting patients (same bins as Screen 3 Widget 3) |

**Calculation**: Same first successful booking-confirming payment and one-observation-per-inquiry rule as Screen 3 Widget 3, across the platform; distribution to multiple providers or later installments does not multiply observations.

---

##### Widget 5: Inquiry Seasonality

| Property | Value |
|----------|-------|
| Chart type | Calendar heatmap (monthly view, intensity = inquiry count vs. monthly average) |
| Layout | 12 rows (months) × 7 columns (Mon→Sun) |
| Intensity | `inquiry count on day ÷ monthly daily average × 100` |
| Purpose | Identify seasonal peaks and campaign-worthy slow periods |
| Cell tooltip | `Inquiries: N • Daily avg: m • Index: X%` |

---

##### Widget 6: Affiliate Acquisition

| Property | Value |
|----------|-------|
| Chart type | Three KPI tiles + ranked table |
| Tile 1 | Affiliate-sourced bookings (count in period) |
| Tile 2 | Affiliate contribution rate = affiliate bookings ÷ total bookings |
| Tile 3 | Avg affiliate booking value |
| Table columns | Affiliate name · Bookings · Revenue · Commission owed · Conversion rate |
| Drill-down | Click affiliate row → affiliate detail in FR-018 |

**Data source**: `discounts` (affiliate codes) linked to `quotes/payments` via FR-018 `Booking with Affiliate Code` entity. Affiliate-sourced = booking where a valid affiliate discount code was applied at payment.

**Limitation note**: Affiliate tracking begins at the booking stage (when the discount code is applied), not at the inquiry stage. It is not possible to attribute an inquiry to an affiliate source.

---

**Business Rules**:

- Seasonality heatmap always shows a rolling 12-month view regardless of time range filter (for pattern recognition)
- Affiliate rows show only affiliates with at least 1 booking in the selected period; inactive affiliates are filtered out

---

#### Screen 10: Geographic Intelligence

**Purpose**: Strategic supply/demand view. Where is patient demand concentrated? Where does the platform have insufficient provider coverage? Used for expansion planning and targeted provider recruitment.

**Filters**: Time range (affects inquiry and booking data) + Treatment type

---

##### Widget 1: Patient Demand Map

| Property | Value |
|----------|-------|
| Chart type | Choropleth map OR ranked table with flag icons (implementation choice) |
| Value mapped | Inquiry count per patient country (in selected period) |
| Color scale | 5-bin scale from low (cool) to high (warm) |
| Tooltip | `Country · Inquiries: N · Booked: B · Conversion rate: R%` |
| Drill-down | Click country → filtered admin Inquiries list |

---

##### Widget 2: Provider Coverage by Country

| Property | Value |
|----------|-------|
| Chart type | Ranked horizontal bar chart |
| Y axis | Country (provider country) |
| X axis | Active provider count |
| Drill-down | Click bar → Provider list filtered to that country |

---

##### Widget 3: Demand vs. Supply Gap

| Property | Value |
|----------|-------|
| Chart type | Ranked table |
| Columns | Patient country · Inquiry count · Provider count (in that country) · Inquiries per provider · Gap flag |
| Gap flag | Flagged if inquiries per provider > platform median by ≥50% |
| Sort | Default: inquiries per provider descending (highest gap first) |
| Purpose | Identify countries to target for provider recruitment |

**Note**: "Provider country" = provider's registered location. The gap metric is an approximation — patients may travel internationally, so a high inquiries-per-provider ratio in one country does not necessarily mean patients cannot be served.

---

##### Widget 4: Conversion Rate by Patient Country

| Property | Value |
|----------|-------|
| Chart type | Horizontal ranked bar chart |
| Y axis | Patient country (top 15 by inquiry volume) |
| X axis | Booking conversion rate (Inquiries → Confirmed booking) |
| Secondary bar | Inquiry count (for context) |
| Reference line | Platform median conversion rate |
| Drill-down | Click bar → admin Inquiries list filtered to that country |

---

##### Widget 5: Emerging Patient Origins

| Property | Value |
|----------|-------|
| Chart type | Ranked table |
| Columns | Country · Inquiry count (current period) · Inquiry count (prior period) · Growth % |
| Filter | Countries with >10 inquiries in current period and >20% growth vs prior period |
| Purpose | Spot new markets before they become dominant |

---

**Business Rules**:

- Country data is sourced canonically from `patients.location_id → countries.name`; if `location_id` is null for legacy rows, the UI may temporarily fall back to `patients.location` until migration cleanup is complete. No IP-geolocation fallback is assumed in this version.
- Demand vs. Supply gap table only shows countries with ≥5 inquiries in the selected period to avoid statistical noise
- Map (if used) requires a separate map rendering library; ranked table is the functional fallback

---

#### Screen 11: Treatment Outcomes

**Purpose**: How treatments are performing operationally and in patient satisfaction. **Scope is strictly operational and satisfaction-based** — no clinical outcomes exist in the database (no graft survival rates, no hair density measurements, no complication data).

**Filters**: Time range + Country + Provider (optional) + Treatment type

---

##### Widget 1: Treatment Completion Rate

| Property | Value |
|----------|-------|
| Chart type | Bar chart |
| X axis | Treatment type |
| Y axis | Completion rate = quotes reaching `completed` ÷ quotes reaching `confirmed` |
| Reference line | Platform average completion rate |
| Drill-down | Click bar → admin Quotes list filtered to that treatment |

---

##### Widget 2: Cancellation & No-Show Rate by Treatment

| Property | Value |
|----------|-------|
| Chart type | Grouped bar chart |
| X axis | Treatment type |
| Y axis | Rate % |
| Groups | Cancellation rate · No-show rate |
| Drill-down | Click bar → admin Quotes list with relevant status filter |

---

##### Widget 3: Treatment Volume Trend

| Property | Value |
|----------|-------|
| Chart type | Stacked area chart |
| X axis | Month |
| Y axis | Booking count |
| Areas | One per treatment type (dynamic, top 5 + Other) |
| Purpose | Track which treatments are growing or declining in demand |
| Drill-down | Click area segment → admin Bookings list filtered to treatment + month |

---

##### Widget 4: Average Review Scores by Treatment

| Property | Value |
|----------|-------|
| Chart type | Grouped bar chart |
| X axis | Treatment type |
| Y axis | Score (1–5) |
| Groups | Overall · Results · Staff · Facility · Value |
| Data source | `reviews` sub-scores, joined via `reviews.quote_id → quotes.treatment_id` |
| Drill-down | Click bar → Reviews list filtered to that treatment |

---

##### Widget 5: Aftercare Activation Rate

| Property | Value |
|----------|-------|
| Chart type | KPI tile + trend line + bar by treatment type |
| KPI | Platform-wide aftercare activation rate = aftercare records created ÷ completed treatments |
| Bar chart | Activation rate broken down by treatment type |
| Drill-down | Click bar → Aftercare records list |

---

##### Widget 6: Provider Distribution by Treatment Specialisation

| Property | Value |
|----------|-------|
| Chart type | Stacked horizontal bar chart |
| Y axis | Treatment type |
| X axis | Provider count offering that treatment |
| Drill-down | Click bar → Provider list filtered to that treatment |

**Data source**: `quotes.treatment_id` grouped by `provider_id`; a provider "offers" a treatment if they have submitted at least 1 quote for it in the last 12 months.

---

**Business Rules**:

- Completion rate only calculated for providers with ≥5 confirmed bookings in the period to avoid single-event noise
- No-show is tracked via the quote status label; if no-show status is not explicitly implemented in the data model, this widget is replaced with "cancellation rate only"
- Do NOT add any clinical outcome metrics (graft count, hair density, success rates) — these are not in the database

---

#### Screen 12: Financial Health & Cashflow

**Purpose**: Platform financial risk monitoring and revenue health. The admin's question is: "Is money flowing correctly, what do we owe, and where are the risks?"

**Filters**: Time range + Country + Currency

---

##### Widget 1: Platform GMV & Net Revenue

| Property | Value |
|----------|-------|
| Chart type | Dual-line area chart |
| X axis | Month |
| Y₁ series | Platform GMV (gross payment volume) |
| Y₂ series | Net revenue (GMV minus total provider payout disbursements) |
| Drill-down | Click period → detailed payment records |

**Calculation**: GMV = `SUM(payments.amount)` where `payment_status = 'completed'`; Net revenue = GMV − total disbursed provider payouts in same period.

---

##### Widget 2: Commission Earned Trend

| Property | Value |
|----------|-------|
| Chart type | Bar chart (monthly) |
| X axis | Month |
| Y axis | Commission earned = sum of effective provider commission deductions for completed payments in period, respecting each provider's configured commission model (`percentage` or `flat rate`) |
| Reference line | Target monthly commission (admin-configurable) |
| Drill-down | Click bar → filtered payment records with commission breakdown |

---

##### Widget 3: Refund & Failed Payment Health

| Property | Value |
|----------|-------|
| Chart type | Four KPI tiles + trend |
| Tile 1 | Refund volume (amount, period) |
| Tile 2 | Refund rate = refund count ÷ total completed payments |
| Tile 3 | Failed payment count (period) |
| Tile 4 | Failed payment rate = failed ÷ total attempted payments |
| Trend | Monthly refund rate + failed rate (dual line) |
| Drill-down | Click tile → filtered Payments list |

---

##### Widget 4: Cash-at-Risk — Platform-Wide Aging

| Property | Value |
|----------|-------|
| Chart type | Stacked horizontal bar chart (same as provider C3, but all providers) |
| Buckets | 0–24h · 1–3d · 4–7d · 8–14d · >14d |
| X axis | Distinct accepted selections awaiting initial payment with a valid payment-window hold (all providers) |
| Optional legend | By provider country |
| Drill-down | Click bucket → admin Quotes list resolved to accepted subquote + pending booking and filtered by active hold + aging bucket |

**Calculation**: Age from immutable `AcceptanceEvent.acceptedAt`, using the actual configured hold deadline and the Screen 1 C3 exclusions. Expired, superseded, and cancelled selections are retained in lifecycle history but excluded from active cash risk.

---

##### Widget 5: Upcoming Provider Payout Obligations

| Property | Value |
|----------|-------|
| Chart type | KPI tile + table |
| KPI | Total upcoming payout amount (next 30 days) |
| Table columns | Provider · Amount · Payout date · Cadence · Status |
| Sort | Payout date ascending |
| Drill-down | Click row → provider payout detail in FR-017 |

---

##### Widget 6: Installment Plan Health

| Property | Value |
|----------|-------|
| Chart type | Donut + KPI |
| Segments | On-time · Overdue · Defaulted |
| KPI | Total outstanding installment balance |
| Data source | `installment_plans` table status |
| Drill-down | Click segment → Installment plans list filtered by status |

---

##### Widget 7: Affiliate Commission Obligations

| Property | Value |
|----------|-------|
| Chart type | KPI tile + upcoming table |
| KPI | Total affiliate commission owed (pending payout) |
| Table | Affiliate · Commission owed · Next payout date |
| Drill-down | Click row → FR-017 affiliate billing |

---

##### Widget 8: Revenue by Currency

| Property | Value |
|----------|-------|
| Chart type | Donut |
| Segments | Per currency code (`payments.currency`) |
| Value | GMV by currency |
| Purpose | FX exposure visibility — how much revenue is in non-base currencies |

---

**Business Rules**:

- All amounts converted to Hairline's base reporting currency (configured in admin settings) using daily FX rates; raw currency amounts shown in tooltips
- Net revenue calculation excludes payout amounts that are still in "Scheduled" status (not yet disbursed)
- This screen is only accessible to admin roles with financial data permissions
- Payment, refund, commission, installment, and payout metrics aggregate their owning records once before joining the accepted selection. The accepted quote amount is not captured revenue and MUST NOT replace actual financial transactions.

---

#### Screen 13: Pricing Intelligence

**Purpose**: Accepted-price landscape across providers and treatments. Helps Hairline understand the prices patients selected and identify descriptive outliers; it does not represent every offered alternative or measure offered-price conversion.

**Filters**: Time range + Country + Treatment type

---

##### Widget 1: Average Accepted Price by Treatment

| Property | Value |
|----------|-------|
| Chart type | Bar chart |
| X axis | Treatment type |
| Y axis | Average accepted subquote total price (platform base currency) |
| Error bars | p25–p75 range per treatment |
| Drill-down | Click bar → Quotes list filtered to accepted selections for that treatment and acceptance period |

---

##### Widget 2: Accepted Price Range per Treatment

| Property | Value |
|----------|-------|
| Chart type | Range bar chart (or box plot if supported) |
| X axis | Treatment type |
| Ranges shown | Min · p25 · Median · p75 · Max |
| Purpose | Show the observed spread of accepted selection prices for each treatment, not the full offered-price market |
| Reference line | Platform median per treatment |
| Drill-down | Click bar → Quotes list of accepted selections for that treatment sorted by accepted price |

---

##### Widget 3: Accepted Price by Provider Country

| Property | Value |
|----------|-------|
| Chart type | Grouped bar chart |
| X axis | Provider country |
| Y axis | Average accepted subquote total price |
| Groups | Per treatment type (top 3 by volume) |
| Purpose | Surface geographic pricing differences (e.g., Turkish providers vs. UK providers) |
| Drill-down | Click bar → Quotes list filtered to accepted selections by provider country + treatment |

---

##### Widget 4: Accepted Selections by Price Bracket

| Property | Value |
|----------|-------|
| Chart type | Bar chart |
| X axis | Accepted subquote total price bracket (dynamic bins based on accepted-price distribution) |
| Y axis | Accepted selection count; tooltip also shows share of all accepted selections in the filtered acceptance-time cohort |
| Reference line | None — this is a price distribution, not a conversion-rate chart |
| Purpose | Show which price brackets patients accepted, without assigning unaccepted parents an invented single price |
| Drill-down | Click bar → Quotes list filtered to accepted selections in that price bracket and acceptance period |

**Boundary**: Offered-price conversion by bracket is deferred. It requires a separately approved price attribution/denominator policy for multi-option parents; dividing accepted selections by accepted selections would misleadingly produce 100% and is prohibited.

---

##### Widget 5: Price Trend Over Time per Treatment

| Property | Value |
|----------|-------|
| Chart type | Multi-line chart |
| X axis | Month (last 12 months) |
| Y axis | Average accepted subquote total price |
| Lines | One per treatment type (top 5 by volume + Other as grey line) |
| Purpose | Track whether observed accepted prices are rising or falling |
| Drill-down | Click line point → Quotes list filtered to accepted selections for that treatment + acceptance month |

---

##### Widget 6: Price Outlier Providers

| Property | Value |
|----------|-------|
| Chart type | Ranked table |
| Columns | Provider · Treatment · Average accepted price · Platform accepted-price median · Variance % · Direction |
| Filter | Providers whose average accepted price is ≥30% above or below the platform accepted-price median for any treatment |
| Direction | "High" (priced above) or "Low" (priced below) |
| Purpose | Flag descriptive deviations in accepted prices for review; does not conclude that a provider is pricing itself out of the market |
| Drill-down | Click row → that provider's detail in FR-015 |

---

**Business Rules**:

- All accepted prices converted to platform base currency under Rule 10, preserving immutable accepted currency/locked-rate provenance; raw accepted amounts and sample sizes shown in tooltips
- Outlier threshold (30%) is admin-configurable
- Only accepted subquote prices from immutable AcceptanceEvents are included, one observation per accepted parent quote; current quote status or current package-library prices are not price sources. Use acceptance time for price ranges, trends, distributions, and outliers.
- Minimum 5 accepted selections per treatment per provider required to include that provider in outlier detection; unaccepted parents do not satisfy this amount-sample threshold
- Unaccepted parents still count once in parent response volume and parent acceptance-rate denominators; they MUST NOT be assigned zero or an arbitrary alternative's amount for price charts.

---

## Business Rules

### Analytics Counting & Time Basis

These definitions apply to all provider/admin widgets, drill-downs, aggregates, benchmarks, and exports. A chart's "Quoted" inquiry stage is not the same unit as a submitted-parent volume metric.

- **Parent response grain**: Count a stable FR-004 Parent Quote ID once on its first successful submission. Multiple parent quotes from one provider are separate responses; drafts, edits, resends, aggregate versions, Quote Options, and Option/Date-Price Records are not extra responses. Child-volume or comparison telemetry, when reported, MUST be separately labelled as Quote Option or Subquote counts and never substituted into parent metrics.
- **Acceptance grain**: FR-005's immutable AcceptanceEvent identifies the selected Subquote, its Quote Option and Option/Date-Price Record, inherited parent context, and accepted aggregate revision. Deduplicate redelivery of the same acceptance and count each accepted parent once. `acceptedSubquoteVersion = acceptedParentQuoteVersion`; neither a changed package preset nor an unselected alternative may replace the accepted snapshot. Historical acceptance measures patient selection and is retained after cancellation or payment-window expiry; it is not proof of a confirmed booking or captured revenue.
- **Parent-quote acceptance rate**: Numerator = distinct parents in the selected first-submission cohort with an AcceptanceEvent by the reporting cutoff. Denominator = all distinct submitted parents in that same cohort, including unaccepted, expired, withdrawn, or later-cancelled parents. Use the first `sent_at` to assign each parent to its cohort; do not divide acceptance events occurring in one period by unrelated submissions in another. This is a parent-level rate, not accepted subquotes divided by available subquotes.
- **Inquiry response rate**: Denominator = distinct `(providerId, inquiryId)` distribution records first assigned to that provider within the selected distribution period. Numerator = those same pairs with at least one submitted parent response by the cutoff. Retries of distribution and multiple parent responses do not multiply either side. Missing authoritative distribution data yields an unavailable metric, not a proxy based on platform inquiries or quote volume.
- **Inquiry funnel and booking conversion**: Use inquiry `created_at` to select the inquiry cohort. Provider views count distinct `(providerId, inquiryId)` pairs assigned to that provider; platform views count distinct Inquiry IDs across providers, not the sum of provider totals. Qualified follows the mandatory-field/spam rule; Quoted means at least one parent was submitted; Accepted means an AcceptanceEvent exists for that inquiry and, in provider views, that provider; Confirmed booking means FR-006 recorded successful deposit or first installment confirmation. Each inquiry contributes at most once to each reached stage and cumulatively to preceding stages. Treatment-segment stages must match the parent/accepted booking's treatment, with deduplication within each segment. Later cancellation does not erase a reached milestone; cancellation and no-show metrics remain separate. `In Progress` is a procedure-start milestone, never a synonym for payment confirmation.
- **Reporting cutoff and empty denominators**: Historical funnel/acceptance/response cohorts are evaluated through the earlier of the selected period end and the pipeline's data-as-of time. Current cohorts show that cutoff and indicate that outcomes may still be pending. A zero denominator is N/A, not 0% or 100%. Tooltips/exports state the unit, cohort timestamp, numerator/denominator, cutoff, and relevant sample sizes; rates based on these distinct-record sets cannot exceed 100%.
- **First response and journey**: TTFQ uses the same inquiry-created cohort and reporting cutoff as the funnel and contributes one observation per inquiry/provider pair whose first parent response occurred by that cutoff, from inquiry creation to earliest parent first submission. Unanswered inquiries remain in funnel/response denominators but have no completed TTFQ observation. Provider distributions pool those observations; platform p50/p90 pool the underlying observations, not provider percentile averages. Journey time instead uses the successful initial payment that first confirms a booking, selects the confirmation-time cohort, and counts the inquiry once. Later installments or failed payment attempts do not create new journey observations.
- **Accepted-price grain**: Count one immutable accepted total price per accepted parent, including the accepted package/date-price and promotion. Standalone price metrics use `AcceptanceEvent.acceptedAt` to select their cohort; Screen 5's scatter uses its expressly stated parent first-submission cohort. Unaccepted parents have a price range, not one amount, and remain excluded from all amount observations while included in parent volume/rate metrics. Cancellation, hold expiry, package-library edits, quote revisions, or later financial adjustments do not rewrite the historical acceptance-price observation. Show accepted selection counts and distinguish these statistics from captured revenue.
- **Active cash risk**: At the displayed snapshot time, include only Accepted FR-006 pending bookings with a non-superseded AcceptanceEvent, valid exclusive slot hold, and no successful initial payment. Scope the time filter by acceptance time, calculate age from immutable `acceptedAt`, and validate the actual configured hold deadline. Remove cancelled, expired-hold, and `Payment Window Expired` selections even before stale quote status caches update; do not restart age on payment retries. Sum each eligible accepted total price once as potential accepted booking value, not deposit receivables, captured revenue, or outstanding installment balances.
- **Financial record grain**: Payments, refunds, commission deductions, installments, and payouts retain their existing owning-record accounting rules. Aggregate those records before attaching read-only AcceptanceEvent/Booking/quote provenance; joining several packages or date options MUST NOT multiply financial totals. This change does not redefine fund release, fees, payout routing, or travel responsibility.

### Global Filter Rules

- **Rule 1**: Default time range on page load = **Last 4 weeks**, all countries
- **Rule 2**: Each screen maintains its own filter state (changing filters on Screen 2 does not affect Screen 3)
- **Rule 3**: Clicking a chart element opens the corresponding pre-filtered operational list in a new context (does not navigate away from the analytics screen)
- **Rule 4**: All screens use skeleton loading states; no full-page blocking spinners
- **Rule 5**: Localize all dates, currencies, and timezones to the user's configured locale (provider locale for provider screens; admin platform locale for admin screens)

### Data Quality Rules

- **Rule 6**: Analytics pipeline updates every 15 minutes; non-blocking banner shown when data is >20 minutes stale
- **Rule 7**: Low sample threshold = **<30 inquiries** for provider screens; helper copy shown but data still rendered
- **Rule 8**: Minimum sample requirements per widget are specified in each screen spec; below minimum, widgets show "Not enough data yet" with the threshold stated
- **Rule 9**: Benchmark pools require minimum 5 providers; if pool is insufficient, benchmark widgets show an explanatory message rather than blank state
- **Rule 10**: All currency amounts converted using daily FX rates cached from the currency conversion API; rates locked at the transaction date for historical data. On API failure, fall back to the previous day's cached rate up to a maximum of **48 hours**; beyond 48 hours, affected widgets show "FX data unavailable" instead of rendering with stale rates
  - Accepted-price observations preserve the FR-005 acceptance snapshot's original currency, total price, locked exchange rate, and acceptance time. If a different reporting currency needs an additional conversion, use a historical acceptance-date reporting rate and retain its provenance; do not replace the commercial locked rate with today's rate. Payment/payout records retain their own existing historical financial FX basis. Missing historical provenance yields an unavailable affected amount metric, not an inferred currency, current package price, or current FX value.

### PII & Privacy Rules

- **Rule 11**: Patient names masked in all provider-facing analytics (ID format only)
- **Rule 12**: Patient identities are never exposed to affiliates (aggregates only)
- **Rule 13**: Provider identities are anonymised in benchmark comparisons and platform-wide charts (providers cannot identify individual competitors)
- **Rule 14**: Admin can see individual provider identities in admin screens for operational support
- **Rule 15**: All analytics access logged with user ID, timestamp, screen accessed, and active filters (12-month retention)

### Access Control Rules

- **Rule 15A**: FR-014 consumes the existing role and permission model; it does not define new roles or expand access beyond the owning platform's permission system.
- **Rule 15B**: If a user lacks permission to view a widget's underlying data domain, the UI MUST not render that widget for that user, and the corresponding widget data MUST not be requested. Remaining widgets reflow within the existing responsive layout.

### Admin Editability Rules

**Editable by Admin**:

- SLA target (minutes) — platform-wide value used across all TTFQ color coding and benchmark charts; per-provider SLA overrides are out of scope for this version
- Benchmark refresh frequency
- Provider engagement status thresholds (Active/At Risk/Dormant day boundaries)
- Outlier detection threshold for Screen 13 (default 30%)
- Target monthly commission reference line on Screen 12 Widget 2

**Fixed in Codebase**:

- Dashboard section order (Screen 1: A → B → C)
- TTFQ formula and funnel stage definitions
- Booking Intensity Index formula
- Commission calculation logic: `IF provider_commissions.type = 'percentage' THEN payment.amount × (effective_rate / 100) ELSE effective_flat_amount` — the conditional is fixed; the rate/amount values are sourced from provider commission configuration

### Performance Rules

- **Rule 16**: All screens load within 3 seconds for 95th percentile (pre-aggregated metrics)
- **Rule 17**: Chart rendering completes within 1 second for ranges ≤12 weeks
- **Rule 18**: Export generation: PDF <60 seconds, CSV <30 seconds
- **Rule 19**: System supports 1,000 concurrent provider analytics sessions without degradation

---

## Success Criteria

### Provider Experience

- **SC-001**: Provider can identify TTFQ health status (Green/Amber/Red) within 3 seconds of opening Screen 1
- **SC-002**: Provider can answer "What is my conversion rate for FUE this month?" from Screen 2 in under 30 seconds
- **SC-003**: Provider can identify their top patient origin country from Screen 3 in under 20 seconds
- **SC-004**: Provider can verify their upcoming payout amount from Screen 4 in under 20 seconds
- **SC-005**: Provider understands their percentile position on at least 2 metrics from Screen 5 in under 1 minute

### Admin Experience

- **SC-006**: Admin can identify all Red-tier providers from Screen 8 in under 30 seconds
- **SC-007**: Admin can identify the top 3 countries with demand/supply gaps from Screen 10 in under 1 minute
- **SC-008**: Admin can verify total upcoming payout obligations from Screen 12 in under 30 seconds
- **SC-009**: Admin can identify pricing outlier providers for a given treatment from Screen 13 in under 2 minutes

### System Performance

- **SC-010**: Analytics pipeline maintains 15-minute update cycle with 99.5% reliability
- **SC-011**: All screens load within 3 seconds for 95% of requests
- **SC-012**: Zero data loss in analytics aggregation pipeline
- **SC-013**: Export generation completes within 60 seconds for 90% of requests

---

## Dependencies

### Internal

- **FR-003**: Inquiry data (`created_at`, `patient_id`, treatment type, spam flag) plus inquiry distribution records (`inquiry_providers.provider_id`, `source`, `status`, `distributed_at`) — feeds all funnel metrics and provider response/distribution analytics
- **FR-004**: Parent Quote identities, provider/inquiry/treatment context, first submission, aggregate versions, and Quote Option/Option-Date-Price hierarchy — feeds parent response volume, TTFQ, and first-submission cohorts; unaccepted price ranges are not amount observations. See FR-004 REQ-004-030.
- **FR-005**: AcceptanceEvent and immutable accepted Subquote snapshot, including parent/option/date-price/subquote IDs, equal accepted aggregate versions, acceptedAt, accepted total price/promotion/currency, locked exchange rate, appointment, and cancellation/supersession provenance — feeds patient selection, parent acceptance rate, and accepted-price statistics. See FR-005 REQ-005-017 through REQ-005-020.
- **FR-006**: Booking/AcceptanceEvent linkage, successful initial-payment confirmation, actual exclusive-hold deadline, terminal Payment Window Expired outcome, lifecycle, and appointment — feeds confirmed-booking funnels, journey time, active cash risk, booking intensity, and downstream treatment milestones
- **FR-007**: Payment data (`amount`, `currency`, `payment_status`, `payment_type`, `created_at`, `is_installment`) — feeds all financial widgets
- **FR-010**: Treatment execution status — feeds completion rate and aftercare activation
- **FR-011**: Aftercare records — feeds aftercare activation rate widgets
- **FR-013**: Reviews (`overall_rating`, `results_rating`, `staff_rating`, `facility_rating`, `value_rating`) — feeds satisfaction widgets
- **FR-015**: Provider master/profile data — provider location and timezone (`providers.country_id`, `providers.city_id`, `providers.timezone`) and effective commission settings (`provider_commissions.type`, `price`, `payment_cycle`) drive localization, commission analytics, and payout cadence
- **FR-017**: Payout records — feeds all payout history and obligation widgets
- **FR-018**: Affiliate records and discount codes — feeds affiliate acquisition widgets
- **FR-026**: Admin settings store — provides admin-configurable analytics values such as SLA target, benchmark refresh frequency, engagement thresholds, and target commission reference line
- **FR-031**: Access control and permissions — governs which admin analytics surfaces and data domains are visible to each authorized role
- **S-03**: Notification Service — handles scheduled export email delivery and secure-link notifications for Screen 6
- **S-05**: Media Storage Service — stores generated export artifacts for 7-day re-download retention and secure-link access
- **Provider Banking Details**: Provider display currency is derived from `banking_details.currency` via provider default-currency resolution; if absent, the current implementation falls back to USD
  - This is reporting-currency resolution only; it MUST NOT overwrite FR-004 system-configured quote currency or the immutable FR-005 accepted currency/locked rate. Reconcile any legacy fallback against the accepted snapshot before presenting historical amount metrics.
- **Provider Team / Auth Data**: Engagement views rely on `provider_activity_logs.action_at` as the canonical activity timestamp source (documented in system-data-schema.md). Last active = `MAX(action_at)` per provider. The previously referenced `provider_users.last_login_at` field does not exist in the schema and must not be used.

### External

- **Currency Conversion API**: Daily FX rates for multi-currency display; failure fallback = previous day's cached rates
- **PDF Generation Library**: For export reports (Screen 6)
- **Map Rendering Library** (optional): For Screen 10 choropleth map; ranked table is the functional fallback

### Analytics Data Contract and Legacy Compatibility

The revised analytics entities below are target reporting contracts, not evidence that corresponding tables, API payloads, or materialized aggregates have been migrated. Implementation reconciliation must map the approved FR-004/FR-005/FR-006 owners to each metric before replacing existing aggregates.

| Contract input | Where used | Canonical boundary / legacy constraint |
|----------------|------------|----------------------------------------|
| Parent Quote first-submission `sent_at` | Response volume, TTFQ, acceptance-rate cohorts, provider ramp | One immutable first submission per stable parent identity; legacy `quotes.sent_at` is usable only if it preserves this meaning, not draft creation or latest resend |
| AcceptanceEvent acceptedAt + accepted snapshot | Acceptance milestones, accepted prices, aging origin | FR-005 event is authoritative; legacy `quotes.accepted_at` alone cannot identify the chosen package/date price or establish an active hold |
| Parent/subquote IDs and accepted aggregate versions; Quote Option/Option-Date-Price IDs | Drill-downs, accepted-price observations, detailed exports | Resolve the exact accepted version and inherited context; require equal parent/subquote aggregate versions |
| Booking linkage, confirmation event, hold deadline, and lifecycle | Confirmed funnels, patient journey, pending-payment aging | FR-006 distinguishes Accepted, Confirmed, In Progress, Payment Window Expired, and Cancelled; flat quote status is insufficient |
| Original accepted total price/currency and locked FX provenance | Accepted-price aggregates, comparisons, exports | Preserve immutable acceptance value; any additional historical reporting conversion follows Rule 10 |
| Owning payment/refund/commission/payout records | Financial aggregates | Deduplicate before quote-hierarchy joins; selected price is not a substitute for captured transaction amounts |

Do not backfill an accepted amount by choosing a current alternative or consulting today's package library. If historical accepted-selection or cohort provenance cannot be recovered faithfully, show unavailable data for the affected metric and record the gap for implementation reconciliation. System-wide schema/spec updates and implementation migration are outside this FR-014 documentation change.

---

## Assumptions

- **Assumption 1**: Providers access the analytics section at least weekly; daily triage is via Screen 1 (Main Dashboard), not the analytics section
- **Assumption 2**: Admin analytics must remain responsive across desktop, tablet, and mobile viewports in accordance with the platform constitution; lower-width layouts may reduce density but must preserve the core workflows
- **Assumption 3**: Provider analytics screens are desktop-first (≥1024px), responsive single-column on ≤1024px
- **Assumption 4**: SLA target is configured as a single platform-wide value (in minutes) by the admin, stored in the admin settings store. Per-provider SLA overrides are out of scope for this version — all providers are measured against the same platform SLA target. Days would be too coarse for this domain (response times range from 30 min to 6+ hours); minutes is the correct unit.
- **Assumption 5**: Payout cadence (weekly/bi-weekly/monthly) is currently sourced from provider commission configuration (`provider_commissions.payment_cycle`), not from the provider profile record itself
- **Assumption 6**: Patient-country analytics resolve from `patients.location_id` referencing `countries.id`; during transition, legacy rows may still fall back to `patients.location` for display/grouping compatibility until data cleanup is complete
- **Assumption 7**: Channel attribution (organic vs. paid vs. social) is not in scope for any screen — only affiliate-sourced traffic is trackable from the current data model
- **Assumption 8**: Provider-side analytics widgets (TTFQ benchmarks, pricing scatter, patient journey, conversion breakdowns, etc.) are **PRD-derived, not transcription-derived**. Client transcriptions focus primarily on admin-side reporting; the provider analytics UX was product-designed to complement the admin view. This is an accepted design decision — future verification passes MUST NOT flag these widgets as discrepancies from client transcriptions.
- **Assumption 9**: FX rate fallback (previous day's cached rate) is capped at a maximum staleness of **48 hours**. Beyond 48 hours, affected financial widgets display a "FX data unavailable" state rather than rendering with stale rates.
- **Assumption 10**: Country widgets (Screens 3, 10) flag rows resolved via legacy `patients.location` fallback with a subtle UI indicator (tooltip or badge) until the `patients.location_id` backfill is complete, so users can distinguish canonical vs. transitional data.

---

## User Scenarios & Testing

These are required implementation/reconciliation cases, not a claim that the deployed analytics have passed them. Consolidated FR verification remains deferred until the controlled FR revisions are complete.

| Scenario | Required result |
|----------|-----------------|
| One inquiry distributed to one provider; two submitted parents, each with three packages and two applicable dates; one selected subquote | Two parent responses, six separately labelled Quote Options, twelve separately labelled Subquotes; inquiry response rate 100%, parent-quote acceptance rate 50%, and one Accepted inquiry. Only the selected subquote price contributes to amount statistics |
| Same inquiry distributed to two providers, both respond; one subquote is accepted and paid | Platform inquiry funnel counts the inquiry once, not twice; each provider's funnel includes its own distribution, and only the selected provider reaches Accepted/Confirmed booking. Parent response volume still counts both providers' distinct submitted parents |
| Draft creation, later quote edit/version, resend, or new date-price alternative after first response | No extra response count for drafts/versions/resends/children; TTFQ retains the earliest parent first-submission timestamp. An independently submitted second parent adds one response, not another inquiry response |
| Cohort contains unaccepted/expired parents, or numerator event belongs to another period | Unaccepted/expired parents remain in their original submission denominator; acceptance/response numerators reference only the same cohort through the stated cutoff. Empty denominators show N/A; missing distribution provenance shows unavailable |
| Initial payment fails then succeeds; later installments are captured | Failed attempts do not confirm the booking; the first successful initial charge creates one Confirmed milestone and one journey duration. Later installments add actual financial transactions but not more confirmations, journeys, or accepted-price observations; In Progress remains procedure start |
| Default 48-hour payment window expires, or acceptance is cancelled/superseded while quote cache still says Accepted | Active aging count/value drops to zero for that selection based on canonical hold/booking state. Historical AcceptanceEvent, parent acceptance, and accepted-price observation remain auditable; no parent/subquote reopening or age reset |
| Package preset, unselected price, reporting settings, or today's FX changes after acceptance | Accepted package/date-price, original total/currency, and locked FX remain unchanged. Historical reporting conversion retains its stated provenance; missing canonical history is unavailable, never reconstructed from current alternatives |
| Payment/acceptance event is redelivered or financial record joins multiple options | Accepted choice and pending aging row remain single observations; payment/refund/commission/payout totals count each owning record once. Detailed exports identify the accepted IDs and equal aggregate versions |
| Price-bracket widget and pricing outlier eligibility | Brackets show accepted counts/shares, not a conversion percentage based only on accepted rows. Outlier eligibility requires five accepted selections, not five unaccepted parents; scatter requires three treatments with both coordinates and makes no causal claim |

## Functional Requirements Summary

### Screen 1 — Main Dashboard (LOCKED)

- **REQ-014-001** through **REQ-014-032**: Screen 1 layout, sections, widget count, chart types, filters, and responsive behavior remain locked. Its TTFQ, five-stage Confirmed-booking funnel, and active accepted-but-unpaid aging MUST use the current Screen 1 definitions and shared analytics rules under the approved CR-FR014-20261007-01 metric-only exception; the v2.0 formulas are superseded where explicitly revised.

### Screen 2 — Performance & Conversion

- **REQ-014-033**: System MUST display cumulative distinct-inquiry funnel conversion trend ending in Confirmed booking as a multi-line chart with weekly/monthly toggle
- **REQ-014-034**: System MUST display conversion breakdown by treatment type as a grouped bar chart
- **REQ-014-035**: System MUST display conversion breakdown by patient country as a ranked horizontal bar
- **REQ-014-036**: System MUST display parent-quote acceptance rate trend using accepted parents and submitted parents from the same first-submission cohort
- **REQ-014-037**: System MUST display TTFQ p50 and p90 trend from earliest parent first submission per inquiry/provider pair with SLA reference line
- **REQ-014-038**: System MUST display cancellation and no-show rate KPI tiles with sparklines
- **REQ-014-039**: System MUST display an anonymised platform benchmark comparison table (TTFQ, booking conversion, parent-quote acceptance rate, avg rating) with percentile bands and the same per-metric counting definitions for provider and peer values
- **REQ-014-040**: Benchmark pool MUST require minimum 5 providers; display explanatory message if pool is insufficient

### Screen 3 — Patient Analytics

- **REQ-014-041**: System MUST display full patient location table (all countries, sortable) and linked donut chart
- **REQ-014-042**: System MUST display new vs. returning patient rate as donut and monthly trend line
- **REQ-014-043**: System MUST display patient journey time (p50 and p90 days inquiry → first successful booking-confirming payment) with distribution histogram, without failed-attempt or later-installment duplication
- **REQ-014-044**: System MUST display review sub-scores (overall, results, staff, facility, value) per treatment type
- **REQ-014-045**: System MUST display treatment preference distribution (inquiry count vs. booked count per treatment)
- **REQ-014-046**: System MUST display aftercare activation rate KPI with trend sparkline
- **REQ-014-047**: Patient age distribution widget MUST only be included if age is directly available in the data model; do NOT derive from free-text fields

### Screen 4 — Finance & Payouts

- **REQ-014-048**: System MUST display revenue trend with weekly/monthly/quarterly toggle
- **REQ-014-049**: System MUST display revenue by treatment type — full list (not capped at 8)
- **REQ-014-050**: System MUST display revenue by patient country
- **REQ-014-051**: System MUST display commission deducted per period using the provider's effective commission model for each completed payment/booking in range (`percentage` or `flat rate`)
- **REQ-014-052**: System MUST display refund volume and refund rate trend
- **REQ-014-053**: System MUST display installment vs. full payment split
- **REQ-014-054**: System MUST display cash-at-risk summary of distinct accepted selections awaiting initial payment under valid holds, linking to Screen 1 Section C3; expired/cancelled/superseded selections MUST be excluded
- **REQ-014-055**: System MUST display full payout history (column bar + paginated table covering all history)

### Screen 5 — Pricing & Benchmarks

- **REQ-014-056**: System MUST display average accepted subquote price by treatment type with acceptance-time trend overlay
- **REQ-014-057**: System MUST display accepted-price distribution histogram with provider and platform accepted-price median reference lines
- **REQ-014-058**: System MUST display a descriptive accepted-price vs. parent-quote acceptance-rate scatter using the same first-submission cohort for both axes (one point per treatment), without offered-price conversion or causal claims; replace with text insight if fewer than 3 treatment types have both coordinates
- **REQ-014-059**: System MUST display platform benchmark comparison table with percentile bands, consistent units/cohorts/FX basis, and accepted-price-only amount observations; require minimum 5 eligible providers for each benchmark metric

### Screen 6 — Export Report Configuration

- **REQ-014-060**: System MUST allow providers to select which analytics screens to include in the export
- **REQ-014-061**: System MUST support PDF and CSV exports using the same approved metric definitions, samples, eligibility, and cutoff as the included screens, with authorized accepted-selection provenance in detailed rows
- **REQ-014-062**: System MUST support scheduled recurring exports (weekly/monthly/quarterly)
- **REQ-014-063**: System MUST store generated reports for 7 days for re-download

### Screen 7 — Platform Overview

- **REQ-014-064**: System MUST display three-section overview (Operations, Performance, Finance) with platform-wide aggregations
- **REQ-014-065**: System MUST display provider TTFQ health distribution donut (Green/Amber/Red counts)
- **REQ-014-066**: System MUST display provider engagement rate and dormant provider count
- **REQ-014-067**: System MUST display a cumulative distinct-platform-inquiry Confirmed-booking funnel and TTFQ bullet chart computed from underlying inquiry/provider first-response observations, not summed provider funnels or averaged provider percentiles
- **REQ-014-068**: System MUST display platform GMV, commission earned, upcoming payout obligations, and cash-at-risk as financial summary tiles

### Screen 8 — Provider Performance & Engagement

- **REQ-014-069**: System MUST display provider league table (sortable by TTFQ, booking conversion, parent-quote acceptance rate, rating, distinct-inquiry response rate) with platform variance column
- **REQ-014-070**: System MUST display provider performance scatter plot (TTFQ vs. conversion rate, one point per provider)
- **REQ-014-071**: System MUST display provider activity table with last active date, distinct first-submitted parent quote count, distinct-inquiry response rate, and engagement status (Active/At Risk/Dormant)
- **REQ-014-072**: System MUST display new provider ramp chart (distinct parent first submissions vs. days since onboarding), not draft/option creation or version counts
- **REQ-014-073**: Engagement status thresholds MUST be admin-configurable

### Screen 9 — Patient Acquisition & Funnel

- **REQ-014-074**: System MUST display inquiry volume trend (area line with prior period overlay)
- **REQ-014-075**: System MUST display cumulative distinct-platform-inquiry funnel trend ending in Confirmed booking as a multi-line monthly chart
- **REQ-014-076**: System MUST display new vs. returning patient rate as stacked monthly bar + KPI tiles
- **REQ-014-077**: System MUST display platform patient journey time distribution (p50, p90, histogram) using one first successful booking-confirming payment per inquiry
- **REQ-014-078**: System MUST display inquiry seasonality calendar heatmap (rolling 12-month view)
- **REQ-014-079**: System MUST display affiliate acquisition KPI tiles and ranked table; display limitation note that tracking begins at booking stage, not inquiry stage

### Screen 10 — Geographic Intelligence

- **REQ-014-080**: System MUST display patient demand by country (choropleth map OR ranked table — implementation choice)
- **REQ-014-081**: System MUST display provider coverage by country (ranked bar)
- **REQ-014-082**: System MUST display demand vs. supply gap table with gap flag; only show countries with ≥5 inquiries in period
- **REQ-014-083**: System MUST display conversion rate by patient country (ranked bar with platform median reference)
- **REQ-014-084**: System MUST display emerging patient origins table (countries with >20% inquiry growth vs. prior period and >10 inquiries in current period)

### Screen 11 — Treatment Outcomes

- **REQ-014-085**: System MUST display treatment completion rate per type (bar chart with platform average reference)
- **REQ-014-086**: System MUST display cancellation and no-show rate per treatment type
- **REQ-014-087**: System MUST display treatment volume trend as stacked area chart (monthly)
- **REQ-014-088**: System MUST display average review sub-scores per treatment type (5 sub-scores)
- **REQ-014-089**: System MUST display aftercare activation rate per treatment type
- **REQ-014-090**: System MUST NOT include any clinical outcome metrics (graft survival, hair density, complication rates) — these are not in the database

### Screen 12 — Financial Health & Cashflow

- **REQ-014-091**: System MUST display platform GMV and net revenue as dual-line area chart (monthly)
- **REQ-014-092**: System MUST display commission earned trend with admin-configurable target reference line
- **REQ-014-093**: System MUST display refund volume/rate and failed payment rate as KPI tiles and monthly trend
- **REQ-014-094**: System MUST display active pending-initial-payment cash-at-risk aging from immutable AcceptanceEvent.acceptedAt (stacked horizontal bar, same buckets and exclusions as Screen 1 C3, platform-wide)
- **REQ-014-095**: System MUST display upcoming provider payout obligations table (amount, provider, date, cadence)
- **REQ-014-096**: System MUST display installment plan health donut (On-time / Overdue / Defaulted)
- **REQ-014-097**: System MUST display affiliate commission obligations table
- **REQ-014-098**: System MUST display revenue by currency donut

### Screen 13 — Pricing Intelligence

- **REQ-014-099**: System MUST display average accepted subquote price by treatment type (bar chart with p25–p75 error bars)
- **REQ-014-100**: System MUST display accepted-price range per treatment (range bar or box plot: min, p25, median, p75, max)
- **REQ-014-101**: System MUST display average accepted subquote price by provider country (grouped bar, top 3 treatments)
- **REQ-014-102**: System MUST display accepted selection count and share by accepted-price bracket, not an offered-price conversion rate
- **REQ-014-103**: System MUST display accepted-price trend per treatment over the last 12 acceptance months
- **REQ-014-104**: System MUST display accepted-price outlier provider table; outlier threshold configurable by admin (default 30%); require minimum 5 accepted selections per treatment per provider

### Shared Quote / Acceptance Analytics

- **REQ-014-105**: System MUST count each submitted Parent Quote once and keep Quote Option/Subquote volumes distinct; drafts, versions, edits, and resends MUST NOT inflate response volume.
- **REQ-014-106**: System MUST resolve every accepted amount and selection drill-down to the immutable FR-005 AcceptanceEvent and exact accepted parent/subquote aggregate version, with equal parent and subquote versions.
- **REQ-014-107**: System MUST calculate parent acceptance, inquiry response, and inquiry funnel rates from their specified distinct-record cohorts and cutoff, returning N/A for zero denominators and an unavailable response metric for missing distribution provenance.
- **REQ-014-108**: System MUST exclude unaccepted parents from amount observations without excluding them from submitted-parent volume or acceptance-rate denominators; accepted historical prices MUST NOT be overwritten by library changes, cancellation, hold expiry, or later financial adjustments.
- **REQ-014-109**: System MUST distinguish Accepted, payment-confirmed Booking, procedure In Progress, and Payment Window Expired; active cash risk MUST validate the actual hold deadline and exclude cancelled, expired, and superseded selections.
- **REQ-014-110**: System MUST aggregate financial records at their owning grain before quote-hierarchy joins, preventing duplicate payments, refunds, deductions, or payouts from repeated events or multiple alternatives.
- **REQ-014-111**: System MUST preserve accepted price/currency/locked-rate provenance and historical reporting-conversion provenance; missing canonical history MUST NOT be filled with an invented alternative price or today's package/FX value.
- **REQ-014-112**: System MUST apply the same revised contracts to provider/admin screens, benchmarks, drill-downs, cached aggregates, PDF/CSV, and scheduled exports without expanding existing permissions or redesigning the locked cockpit.

---

## Key Entities

- **Entity 1 — Analytics Metrics Aggregate** (provider-level, daily/cohort): `provider_id`, cohort start/end and timestamp basis, reporting cutoff/data-as-of, distinct inquiry-stage counts (inquiry, qualified, quoted, accepted, confirmed), separately labelled treatment-start count, distinct submitted/accepted parent counts, separately labelled Quote Option/Subquote counts, distribution-cohort assigned/responded inquiry counts, TTFQ observations/p50/p90, accepted-price sample count, effective SLA, income/commission totals, and reporting currency. Inquiry-stage counts MUST NOT be populated with quote/option counts; retain the source observations or equivalent mergeable data needed for longer-range distinct counts and percentiles rather than summing daily percentiles.

- **Entity 2 — Booking Intensity Record** (provider-level, daily): `provider_id`, `date`, `bookings_on_day`, `monthly_daily_avg`, `intensity_index`, `baseline_type`

- **Entity 3 — Accepted Selection Aging Snapshot** (provider-level, refreshed every 15 min): Booking/AcceptanceEvent/inquiry/provider IDs, accepted parent/subquote IDs and equal aggregate versions, Quote Option/Option-Date-Price IDs, immutable acceptedAt, actual hold deadline, booking/payment/hold eligibility, age hours/bucket, snapshot time, treatment/country, accepted total price/original currency/locked FX, and reporting amount/currency/FX provenance. One row per active pending booking; deadline/status checks prevent a stale Accepted quote from remaining in cash risk after hold expiry.

- **Entity 4 — Platform Analytics Aggregate** (platform-level, daily/cohort): reporting period/basis/cutoff, distinct platform inquiry-stage counts, separate submitted/accepted parent counts, accepted-price sample counts, active providers, pooled inquiry/provider TTFQ observations/p50/p90, Confirmed-booking conversion rate, deduplicated GMV/commission, new patients, and reporting/FX provenance. Provider funnel totals and percentile values are not directly additive platform aggregates.

- **Entity 5 — Provider Engagement Snapshot** (provider-level, daily): `provider_id`, `last_active_at` (sourced from `MAX(provider_activity_logs.action_at)` per provider), `last_login_at` (sourced from `MAX(provider_activity_logs.action_at WHERE action_type = 'login')` per provider), distinct parent first submissions in 30 days, distinct assigned/responded inquiry counts for the 30-day distribution cohort, response rate or unavailable reason, reporting cutoff, and engagement status.

- **Entity 6 — Benchmark Segment** (platform-level, weekly): `segment_id`, `segment_type`, eligible provider count per metric, metric medians, units/cohort/cutoff/sample basis, historical reporting-currency/FX basis, and calculation time. Accepted-price benchmarks require actual accepted-price samples; unaccepted parents are not zero values.

- **Entity 7 — Payout Record**: `payout_id`, `provider_id`, `period_start`, `period_end`, `amount`, `currency`, `status`, `disbursed_at`, `cadence`

- **Entity 8 — Export Report Configuration**: `config_id`, `provider_id`, `report_type`, `screens_included` (array), `date_range_type`, `recurring`, `frequency`, `email_recipients`, `last_generated_at`
  - Generated reports additionally retain the metric definitions/cohorts, reporting cutoff/data-as-of, sample sizes, currency/FX provenance, and authorized accepted-selection IDs/versions for detailed rows. Configuration and scheduling do not change screen metric semantics.

- **Entity 9 — Currency Exchange Rate**: `date`, `base_currency`, `target_currency`, `exchange_rate`, `fetched_at`

- **Entity 10 — Accepted Price Observation** (one per accepted parent): AcceptanceEvent/inquiry/provider IDs, accepted parent/subquote IDs and equal versions, Quote Option/Option-Date-Price IDs, treatment/package snapshot provenance, first-submitted parent time, acceptedAt, immutable accepted total price/promotion/original currency/locked FX, reporting amount/currency/historical FX provenance, and later lifecycle outcome. Cohorts use the documented timestamp; later outcomes do not rewrite the accepted observation.

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-11 | 1.0 | Initial PRD creation | AI Assistant |
| 2026-04-16 | 2.0 | Major rewrite: single-page cockpit design locked (Screen 1); global filters, cross-filtering, TTFQ spec, all Section A/B/C widgets specified | AI Assistant |
| 2026-04-16 | 3.0 | Full 12-screen expansion: Screens 2–6 (provider analytics suite + export config) and Screens 7–13 (admin analytics suite) added; all widgets verified against system-data-schema.md; data model gaps documented; 104 functional requirements; 9 key entities | AI Assistant |
| 2026-04-17 | 3.1 | Verification fixes: Screen 7 drill-downs corrected (Tiles 4/5 → Screen 8; B4 → Screen 11; C1–C4 → Screen 12); screen count corrected to 13 (12 analytical + 1 export config); `quotes.sent_at` and `quotes.accepted_at` resolved via schema addition; Screen 2 conversion-rate threshold unified under Rule 7; drill-down references standardised to number-only form; approvals marked pending review | AI Assistant |
| 2026-04-17 | 3.2 | Follow-up alignment after code review: commission analytics updated to support percentage and flat-rate provider commission models; dependency references corrected to code-backed sources (`provider_commissions.payment_cycle`, `banking_details.currency`, `inquiry_providers` distribution data, `providers.timezone`); admin analytics restored to responsive-web scope; provider-specific SLA storage called out as an unresolved canonical-data dependency | Codex |
| 2026-04-17 | 3.3 | Verification fixes (v2): commission formula corrected to conditional (percentage vs. flat-rate); last-activity source resolved to `provider_activity_logs.action_at` (confirmed against backend migrations — `provider_users.last_login_at` does not exist); SLA scoped to platform-wide target (per-provider overrides deferred); Screen 7 B2 drill-down fixed (Screen 7 self-link → Screen 8); Module Scope corrected to 6-screen provider suite; admin workflow extended to include Screens 11 and 13; Screen 6 export exclusion note added; REQ numbering resequenced (Screen 6 moved to REQ-014-060–063; Screens 7–13 shifted to REQ-014-064–104) | Claude Code |
| 2026-04-18 | 3.4 | Post-verification alignment after backend cross-check: patient-country provenance normalized to `patients.location_id → countries.name` with legacy `patients.location` fallback only for unmigrated rows; unsupported IP-geolocation fallback removed; system PRD SLA parameter aligned to platform-wide target; Screen 6 dependencies expanded to include S-03 Notification Service and S-05 Media Storage Service | Codex |
| 2026-04-18 | 3.5 | Verification fixes: Screen 6 PDF branding narrowed to `providers.profile_image` only (colors-from-profile removed — no schema field); FX fallback capped at 48 hours (Rule 10); Assumption 8 added to record that provider-side analytics widgets are PRD-derived (accepted design decision, not a transcription discrepancy); Assumption 9 (FX freshness cap) and Assumption 10 (legacy location UI indicator) added | Claude Code |
| 2026-04-18 | 3.6 | Status updated to Verified & Approved following completed verify-fr pass (v3.5); approvals signed off by Product Owner | Claude Code |
| 2026-10-07 | 3.7 | Approved Meeting 02 analytics alignment: distinct parent response and inquiry cohorts, immutable accepted-subquote prices/provenance, Confirmed-booking funnels and first-payment journey, valid-hold aging, accepted-price distribution replacing price-bracket conversion, financial deduplication, export/benchmark/entity contracts, and formula-only Screen 1 exception. CR-FR014-20261007-01 records the delta; implementation reconciliation and consolidated verification remain pending | Codex |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner — prior baseline v3.6 | Joachim Tung | 2026-04-18 | ✅ Approved (historical baseline) |
| Product Owner — documentation delta v3.7 | Joachim Trung Tuan | 2026-10-07 | ✅ Approved: "Please update as per your suggestions"; includes accepted-price distribution and metric-only Screen 1 exception. Not an implementation sign-off |
| Technical Lead | — | — | Pending review |
| Stakeholder | — | — | Pending review |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B
**Last Updated**: 2026-10-07
