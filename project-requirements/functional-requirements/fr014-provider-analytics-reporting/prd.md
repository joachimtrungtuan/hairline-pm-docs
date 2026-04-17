# FR-014 - Provider Analytics & Reporting

**Module**: PR-05: Financial Management & Reporting | A-08: Analytics & Reporting
**Feature Branch**: `fr014-provider-analytics-reporting`
**Created**: 2025-11-11
**Status**: Draft
**Source**: FR-014 from system-prd.md

---

## Executive Summary

The Provider Analytics & Reporting module delivers a **12-screen analytics suite** split across two tenants: provider and admin.

On the **provider side**, five screens cover the full operational picture — a locked cockpit dashboard for daily triage (Screen 1), plus four deeper analytical views for conversion performance, patient insights, financial health, and pricing/benchmarks. Each screen has a single job and is accessed via the Analytics section of the provider portal.

On the **admin side**, seven screens give Hairline visibility into platform-wide health, provider quality and engagement, patient acquisition, geographic supply/demand gaps, treatment outcomes, financial cashflow, and pricing landscape.

All data shown across every screen is sourced directly from the operational database or derived by calculation. Nothing is aspirational or dependent on external integrations unless explicitly noted.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-XX)**: No direct patient-facing features. Patient behaviour data (inquiry timing, booking patterns, location) feeds the analytics pipeline.
- **Provider Platform (PR-05)**: 5-screen analytics suite accessible from the "Analytics" nav section.
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

**Actor**: Provider (Owner/Admin role)
**Trigger**: Provider clicks "Analytics" in the nav
**Outcome**: Provider navigates between 5 analytical screens to understand performance, patients, and financials

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
5. Admin navigates to Financial Health & Cashflow (Screen 12) — reviews payout obligations and cash-at-risk
6. Admin takes action on flagged providers (links through to provider management in FR-015)

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

> **STATUS: LOCKED — do not modify this screen specification.**
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

**TTFQ formula**: `first_quote.sent_at − inquiry.created_at` (wall time, provider timezone). Exclude auto-acks. Calls/messages do not stop the clock.

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
- Stages: Inquiries → Qualified → Quoted → Accepted → In progress
- Each stage: Count + Step % (stage ÷ previous stage)
- Footer: Overall conversion = In progress ÷ Inquiries
- Qualified = not spam + mandatory fields present (age, problem, contact)
- In progress = payment captured within range
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
- X = count of accepted-but-unpaid quotes; optional legend by treatment (top 3) or country
- Age = now − `quote.accepted_at`; exclude cancelled/expired
- Drill-down: click bucket → Accepted Quotes list

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
| Lines | Qualified % · Quoted % · Accepted % · In progress % |
| Drill-down | Click a point → Inquiries list filtered to that stage + time period |

**Calculation**: Each stage % = count of inquiries reaching that stage in the period ÷ total inquiries in period. Inquiry counted at highest stage reached within the selected range.

---

##### Widget 2: Conversion Breakdown by Treatment Type

| Property | Value |
|----------|-------|
| Chart type | Grouped bar chart |
| X axis | Treatment type (from catalog) |
| Y axis | Conversion % (Inquiries → In progress) |
| Groups per bar | Inquiries count, Quoted count, In progress count |
| Drill-down | Click bar → filtered Inquiries list for that treatment |

**Data source**: `quotes.treatment_id → treatments.name` joined with funnel stage counts.

---

##### Widget 3: Conversion Breakdown by Patient Country

| Property | Value |
|----------|-------|
| Chart type | Horizontal ranked bar chart |
| Y axis | Patient country (top 10 by inquiry volume) |
| X axis | Conversion % (Inquiries → In progress) |
| Secondary bar | Inquiry count (context for the rate) |
| Drill-down | Click bar → filtered Inquiries list for that country |

**Data source**: `inquiries.patient_id → patients.country` joined with payment records.

---

##### Widget 4: Quote Acceptance Rate Trend

| Property | Value |
|----------|-------|
| Chart type | Line chart |
| X axis | Week or month (toggle) |
| Y axis | Quote acceptance rate = Accepted ÷ Quoted |
| Drill-down | Click point → Quotes list filtered to that period |

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

**Data source**: `quotes.status = 'cancelled'` after reaching `confirmed`/`inprogress`; no-show tracked via status label.

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
- Minimum 10 inquiries required to display conversion rate (not a hard lock — counts still shown below threshold)

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

**Calculation**: `payment.created_at − inquiry.created_at` for inquiries that resulted in a completed payment within the selected range.

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

**Data source**: `payments.patient_id → patients.country`.

---

##### Widget 4: Commission & Net Revenue

| Property | Value |
|----------|-------|
| Chart type | Two KPI tiles + trend line (both on same chart) |
| Tile 1 | Total income (gross) |
| Tile 2 | Commission deducted |
| Trend | Gross income line + commission deducted area, stacked |

**Calculation**: Commission = `SUM(payments.amount × (quotes.commission / 100))` for completed payments. Gross and net displayed in provider currency.

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
| Value | Total amount of accepted-but-unpaid quotes |
| Count | Number of quotes in each aging bucket |
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
- Commission is calculated, not stored as a field; commission displayed with note "Calculated at quote rate"
- All amounts in provider currency; FX rates locked at payment `created_at` date; footer note "Historical exchange rates applied"
- Payout history only shows payouts that have been processed (not projected future payouts beyond the next scheduled one)

---

#### Screen 5: Pricing & Benchmarks

**Purpose**: Understand pricing strategy — whether the provider's quote amounts are competitive, how price affects conversion, and where they stand relative to platform peers.

**Filters**: Time range + Country + Treatment type

---

##### Widget 1: Average Quote Amount by Treatment

| Property | Value |
|----------|-------|
| Chart type | Bar chart + trend line |
| X axis | Treatment type |
| Y axis | Average quote amount (provider currency) |
| Trend overlay | Provider's own avg quote amount over time (line on same chart) |
| Drill-down | Click bar → Quotes list filtered to that treatment |

---

##### Widget 2: Quote Amount Distribution

| Property | Value |
|----------|-------|
| Chart type | Histogram |
| X axis | Quote amount (binned, e.g., 0–1k · 1k–2k · 2k–3k · 3k–5k · >5k; dynamic bins based on data range) |
| Y axis | Quote count |
| Reference lines | Median quote amount · Platform median quote amount (anonymised) |
| Drill-down | Click bin → Quotes list filtered to that amount range |

---

##### Widget 3: Price vs. Conversion Rate

| Property | Value |
|----------|-------|
| Chart type | Scatter plot |
| X axis | Average quote amount per treatment type |
| Y axis | Conversion rate (Accepted ÷ Quoted) per treatment type |
| Points | One point per treatment type (labelled) |
| Reference lines | Platform median X (avg quote) and platform median Y (conversion rate) |
| Purpose | Shows whether higher-priced quotes convert less for this provider |

**Note**: If provider has fewer than 3 treatment types with data, this chart is replaced with a text insight ("Insufficient treatment variety to display price-conversion scatter").

---

##### Widget 4: Platform Benchmark Comparison

| Property | Value |
|----------|-------|
| Chart type | Comparison table |
| Rows (metrics) | TTFQ p50 · Overall conversion rate · Quote acceptance rate · Avg quote amount · Avg overall rating · Avg results rating |
| Columns | Provider value · Platform median · Variance (±%) · Percentile band (Bottom 25% / Mid 50% / Top 25%) |
| Color coding | Green = above median · Amber = within 10% below · Red = >10% below |
| Drill-down | Click metric row → corresponding detailed screen (e.g., TTFQ → Screen 2 Widget 5) |

**Business rule**: Benchmark pool = all active providers with ≥30 inquiries in the same rolling 12-month window. Minimum 5 providers in pool required. If pool is too small, display "Not enough peer providers to generate a meaningful benchmark yet."

---

**Business Rules**:

- Provider identity is fully anonymised in all benchmark calculations
- Benchmark data is refreshed weekly (not real-time)
- Price displayed in provider currency; benchmark amounts converted to provider currency using the same daily FX rate

---

#### Screen 6: Export Report Configuration

**Purpose**: Allow providers to generate PDF or CSV exports of any analytics screen's data.

**Data Fields**:

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Report type | Radio | Yes | PDF Summary or CSV Detailed |
| Screens to include | Checkboxes | Yes | Performance, Patient Analytics, Finance & Payouts, Pricing & Benchmarks |
| Date range | Date picker | Yes | Max 12-month span |
| Country filter | Dropdown | No | Optional |
| Treatment filter | Dropdown | No | Optional |
| Email delivery | Checkbox | No | Sends to provider's registered email |
| Schedule recurring | Checkbox | No | Weekly / Monthly / Quarterly |

**Business Rules**:

- PDF reports include provider branding (logo, colors from profile)
- Report generation <60 seconds; async queue for large datasets
- Generated reports stored 7 days for re-download from Report History section
- Email delivery: PDF attachment + secure link (expires 48 hours)
- Max 5 active recurring configurations per provider

---

### Admin Platform (A-08)

#### Screen 7: Platform Overview Dashboard

**Purpose**: Platform health at a glance — one scrollable page with three sections mirroring the provider dashboard structure but aggregated across all providers.

**Filters**: Time range (same options) + Country + Provider (optional, defaults to All)

**Layout**: Three sections (A: Operations, B: Performance, C: Finance). Single column on ≤1440px (this is an admin view, desktop-only).

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
- Tap → Provider Performance screen (Screen 7) filtered to Red tier

###### Tile 5: Provider Engagement Rate

- Value: % of active providers who submitted at least 1 quote in last 30 days
- Sub-value: Count of dormant providers (0 quotes in last 30 days)
- Tap → Screen 7 engagement section filtered to dormant

---

##### Section B — Performance Signals

###### B1: Platform-Wide Conversion Funnel

- Chart: Funnel chart (same 5 stages as provider funnel, but platform-wide totals)
- Shows: Count + Step % for each stage
- Footer: Overall platform conversion = In progress ÷ Inquiries
- Drill-down: click stage → admin Inquiries list filtered to that stage

###### B2: Platform TTFQ Distribution

- Chart: Bullet chart (platform p50 + p90 vs SLA default target)
- Shows: Distribution across all providers
- Drill-down: click → Screen 7 sorted by TTFQ

###### B3: Top Patient Origin Countries

- Chart: Donut (top 8 countries by inquiry volume + Other)
- Drill-down: click slice → Screen 9 filtered to that country

###### B4: Treatment Type Distribution

- Chart: Donut (inquiry share by treatment type)
- Drill-down: click slice → Screen 10 filtered to that treatment

---

##### Section C — Financial Summary

###### C1: Platform GMV (Period)

- Value: `SUM(payments.amount)` where `payment_status = 'completed'`, period
- Sub-value: % change vs. prior period
- Drill-down → Screen 11

###### C2: Commission Earned (Period)

- Value: `SUM(payments.amount × quotes.commission / 100)` for completed payments
- Sub-value: As % of GMV
- Drill-down → Screen 11

###### C3: Upcoming Provider Payout Obligations

- Value: Total payout amount due to providers in next 30 days
- Sub-value: Number of providers in next payout cycle
- Drill-down → Screen 11

###### C4: Platform Cash-at-Risk

- Value: Total amount in accepted-but-unpaid quotes, platform-wide
- Sub-value: Count of quotes >14 days aging
- Drill-down → Screen 11

---

**Business Rules**:

- Default time range: Last 4 weeks (same as provider dashboard)
- Provider TTFQ health tiers use the individual provider's configured SLA; for platform-wide display, the default SLA is used if no provider SLA is set
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
| Conversion rate | Inquiries → In progress % |
| Quote acceptance rate | Accepted ÷ Quoted % |
| Avg overall rating | Star rating (from reviews) |
| Quote response rate | Quotes submitted ÷ inquiries distributed |
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
| Last active | Date of last login (`users.last_login_at`) |
| Quotes this month | Count of quotes submitted in current calendar month |
| Inquiry response rate | Quotes submitted ÷ inquiries distributed (last 30 days) |
| Status | Active (activity in last 7d) · At Risk (7–30d) · Dormant (>30d no activity) |

- Filter by status (Active / At Risk / Dormant)
- Drill-down: click row → provider detail in FR-015

###### Widget 4: New Provider Ramp

| Property | Value |
|----------|-------|
| Chart type | Line chart (multiple series) |
| X axis | Days since onboarding (0–90 days) |
| Y axis | Cumulative quotes submitted |
| Series | Each provider onboarded in the selected period (one line each, anonymised) |
| Reference line | Platform average ramp curve |
| Purpose | Identify new providers who are struggling to get started |

**Data source**: Providers with `created_at` within the selected period; `quotes.created_at − providers.created_at` for days-since-onboarding offset.

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
- Last login data requires `users.last_login_at` to be maintained in the users table
- "Inquiry response rate" = quotes submitted ÷ inquiries distributed to that provider in the same period; if no distribution tracking exists, use quotes submitted ÷ total platform inquiries in period as a proxy (flag this as lower fidelity)
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
| Lines | Qualified % · Quoted % · Accepted % · In progress % |
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
| X axis | Conversion rate (Inquiries → In progress) |
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

- Country data sourced from `patients.country`; if null, falls back to IP geolocation (flagged "Estimated" in tooltip)
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
| Y axis | Commission earned = `SUM(payments.amount × quotes.commission / 100)` |
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
| X axis | Count of accepted-but-unpaid quotes (all providers) |
| Optional legend | By provider country |
| Drill-down | Click bucket → admin Quotes list filtered to accepted status + aging bucket |

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

---

#### Screen 13: Pricing Intelligence

**Purpose**: Strategic pricing landscape across all providers and treatments. Helps Hairline understand market pricing, identify outliers, and inform provider guidance and benchmark targets.

**Filters**: Time range + Country + Treatment type

---

##### Widget 1: Average Quote Amount by Treatment

| Property | Value |
|----------|-------|
| Chart type | Bar chart |
| X axis | Treatment type |
| Y axis | Average quote amount (platform base currency) |
| Error bars | p25–p75 range per treatment |
| Drill-down | Click bar → Quotes list filtered to that treatment |

---

##### Widget 2: Price Range per Treatment

| Property | Value |
|----------|-------|
| Chart type | Range bar chart (or box plot if supported) |
| X axis | Treatment type |
| Ranges shown | Min · p25 · Median · p75 · Max |
| Purpose | Show the full spread of prices in the market for each treatment |
| Reference line | Platform median per treatment |
| Drill-down | Click bar → Quotes list for that treatment sorted by amount |

---

##### Widget 3: Quote Amount by Provider Country

| Property | Value |
|----------|-------|
| Chart type | Grouped bar chart |
| X axis | Provider country |
| Y axis | Average quote amount |
| Groups | Per treatment type (top 3 by volume) |
| Purpose | Surface geographic pricing differences (e.g., Turkish providers vs. UK providers) |
| Drill-down | Click bar → Quotes list filtered to provider country + treatment |

---

##### Widget 4: Conversion Rate by Price Bracket

| Property | Value |
|----------|-------|
| Chart type | Bar chart |
| X axis | Quote amount bracket (dynamic bins based on data distribution) |
| Y axis | Conversion rate (Accepted ÷ Quoted) for quotes in that bracket |
| Reference line | Overall platform conversion rate |
| Purpose | Show whether higher-priced quotes convert less platform-wide |
| Drill-down | Click bar → Quotes list filtered to that price bracket |

---

##### Widget 5: Price Trend Over Time per Treatment

| Property | Value |
|----------|-------|
| Chart type | Multi-line chart |
| X axis | Month (last 12 months) |
| Y axis | Average quote amount |
| Lines | One per treatment type (top 5 by volume + Other as grey line) |
| Purpose | Track whether market prices are rising or falling |
| Drill-down | Click line point → Quotes list for that treatment + month |

---

##### Widget 6: Price Outlier Providers

| Property | Value |
|----------|-------|
| Chart type | Ranked table |
| Columns | Provider · Treatment · Avg quote amount · Platform median · Variance % · Direction |
| Filter | Providers whose avg quote is ≥30% above or below the platform median for any treatment |
| Direction | "High" (priced above) or "Low" (priced below) |
| Purpose | Flag providers who may be pricing themselves out of the market or undervaluing their services |
| Drill-down | Click row → that provider's detail in FR-015 |

---

**Business Rules**:

- All quote amounts converted to platform base currency for comparison; raw amounts shown in tooltips
- Outlier threshold (30%) is admin-configurable
- Only quotes with `status ≠ 'inquiry'` (i.e., actually submitted quotes) are included in pricing calculations
- Minimum 5 quotes per treatment per provider required to include that provider in outlier detection

---

## Business Rules

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
- **Rule 10**: All currency amounts converted using daily FX rates cached from the currency conversion API; rates locked at the transaction date for historical data

### PII & Privacy Rules

- **Rule 11**: Patient names masked in all provider-facing analytics (ID format only)
- **Rule 12**: Patient identities are never exposed to affiliates (aggregates only)
- **Rule 13**: Provider identities are anonymised in benchmark comparisons and platform-wide charts (providers cannot identify individual competitors)
- **Rule 14**: Admin can see individual provider identities in admin screens for operational support
- **Rule 15**: All analytics access logged with user ID, timestamp, screen accessed, and active filters (12-month retention)

### Admin Editability Rules

**Editable by Admin**:

- SLA target (minutes) per provider (used across TTFQ color coding and benchmark charts)
- Benchmark refresh frequency
- Provider engagement status thresholds (Active/At Risk/Dormant day boundaries)
- Outlier detection threshold for Screen 13 (default 30%)
- Target monthly commission reference line on Screen 12 Widget 2

**Fixed in Codebase**:

- Dashboard section order (Screen 1: A → B → C)
- TTFQ formula and funnel stage definitions
- Booking Intensity Index formula
- Commission calculation formula (`payment.amount × quote.commission / 100`)

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

- **FR-003**: Inquiry data (`created_at`, `patient_id`, treatment type, spam flag) — feeds all funnel metrics
- **FR-004**: Quote data (`status`, `quote_amount`, `commission`, `treatment_id`, `sent_at`, `accepted_at`) — feeds TTFQ, acceptance rate, pricing widgets
- **FR-006**: Booking data (status transitions, `start_date`) — feeds booking intensity heatmap and completion rates
- **FR-007**: Payment data (`amount`, `currency`, `payment_status`, `payment_type`, `created_at`, `is_installment`) — feeds all financial widgets
- **FR-010**: Treatment execution status — feeds completion rate and aftercare activation
- **FR-011**: Aftercare records — feeds aftercare activation rate widgets
- **FR-013**: Reviews (`overall_rating`, `results_rating`, `staff_rating`, `facility_rating`, `value_rating`) — feeds satisfaction widgets
- **FR-015**: Provider profile (`country`, `timezone`, `currency`, `payout_cadence`, `sla_minutes`) — drives localization and TTFQ thresholds
- **FR-017**: Payout records — feeds all payout history and obligation widgets
- **FR-018**: Affiliate records and discount codes — feeds affiliate acquisition widgets

### External

- **Currency Conversion API**: Daily FX rates for multi-currency display; failure fallback = previous day's cached rates
- **PDF Generation Library**: For export reports (Screen 6)
- **Map Rendering Library** (optional): For Screen 10 choropleth map; ranked table is the functional fallback

### Data Model Gaps to Resolve Before Implementation

The following fields are referenced in widget calculations but are not explicitly present as dedicated columns in the current schema. These require either dedicated timestamp columns or a status history/audit table:

| Field needed | Where used | Recommended resolution |
|-------------|------------|----------------------|
| `quotes.sent_at` | TTFQ calculation (Screens 1, 2, 7, 8) | Add `sent_at TIMESTAMP` to `quotes` table, populated when `status` transitions from `inquiry` → `quote` |
| `quotes.accepted_at` | Quote→Payment Aging (Screens 1, 4, 12) | Add `accepted_at TIMESTAMP` to `quotes` table, populated when `status` transitions to `accepted` |

*The user has indicated that a quote timeline/activity system may already record status-change events with timestamps. If so, these fields can be derived from that timeline. Confirm with the development team before implementation.*

---

## Assumptions

- **Assumption 1**: Providers access the analytics section at least weekly; daily triage is via Screen 1 (Main Dashboard), not the analytics section
- **Assumption 2**: Admin analytics access is desktop-only (≥1440px); responsive layouts are not required for admin screens
- **Assumption 3**: Provider analytics screens are desktop-first (≥1024px), responsive single-column on ≤1024px
- **Assumption 4**: SLA minutes per provider are configured and maintained in the provider profile (FR-015); if not set, a platform default SLA is used
- **Assumption 5**: Payout cadence (weekly/bi-weekly/monthly) is configured per provider in provider profile
- **Assumption 6**: `patients.country` contains the patient's registered country; where missing, IP-based geolocation is used as a fallback (flagged "Estimated" in UI)
- **Assumption 7**: Channel attribution (organic vs. paid vs. social) is not in scope for any screen — only affiliate-sourced traffic is trackable from the current data model

---

## Functional Requirements Summary

### Screen 1 — Main Dashboard (LOCKED)

- **REQ-014-001** through **REQ-014-032**: See v2.0 spec (unchanged). Screen 1 is frozen.

### Screen 2 — Performance & Conversion

- **REQ-014-033**: System MUST display funnel conversion trend as a multi-line chart with weekly/monthly toggle
- **REQ-014-034**: System MUST display conversion breakdown by treatment type as a grouped bar chart
- **REQ-014-035**: System MUST display conversion breakdown by patient country as a ranked horizontal bar
- **REQ-014-036**: System MUST display quote acceptance rate trend over time
- **REQ-014-037**: System MUST display TTFQ p50 and p90 trend over time with SLA reference line
- **REQ-014-038**: System MUST display cancellation and no-show rate KPI tiles with sparklines
- **REQ-014-039**: System MUST display an anonymised platform benchmark comparison table (TTFQ, conversion, acceptance rate, avg quote, avg rating) with percentile bands
- **REQ-014-040**: Benchmark pool MUST require minimum 5 providers; display explanatory message if pool is insufficient

### Screen 3 — Patient Analytics

- **REQ-014-041**: System MUST display full patient location table (all countries, sortable) and linked donut chart
- **REQ-014-042**: System MUST display new vs. returning patient rate as donut and monthly trend line
- **REQ-014-043**: System MUST display patient journey time (p50 and p90 days inquiry → payment) with distribution histogram
- **REQ-014-044**: System MUST display review sub-scores (overall, results, staff, facility, value) per treatment type
- **REQ-014-045**: System MUST display treatment preference distribution (inquiry count vs. booked count per treatment)
- **REQ-014-046**: System MUST display aftercare activation rate KPI with trend sparkline
- **REQ-014-047**: Patient age distribution widget MUST only be included if age is directly available in the data model; do NOT derive from free-text fields

### Screen 4 — Finance & Payouts

- **REQ-014-048**: System MUST display revenue trend with weekly/monthly/quarterly toggle
- **REQ-014-049**: System MUST display revenue by treatment type — full list (not capped at 8)
- **REQ-014-050**: System MUST display revenue by patient country
- **REQ-014-051**: System MUST display commission deducted per period (calculated as `payment.amount × quote.commission / 100`)
- **REQ-014-052**: System MUST display refund volume and refund rate trend
- **REQ-014-053**: System MUST display installment vs. full payment split
- **REQ-014-054**: System MUST display cash-at-risk summary KPI linking to Screen 1 Section C3 for full aging detail
- **REQ-014-055**: System MUST display full payout history (column bar + paginated table covering all history)

### Screen 5 — Pricing & Benchmarks

- **REQ-014-056**: System MUST display average quote amount by treatment type with trend overlay
- **REQ-014-057**: System MUST display quote amount distribution histogram with provider median and platform median reference lines
- **REQ-014-058**: System MUST display price vs. conversion rate scatter plot (one point per treatment); replace with text insight if fewer than 3 treatment types have data
- **REQ-014-059**: System MUST display platform benchmark comparison table with percentile bands; require minimum 5 providers in benchmark pool

### Screen 6 — Export Report Configuration

- **REQ-014-101**: System MUST allow providers to select which analytics screens to include in the export
- **REQ-014-102**: System MUST support PDF and CSV export formats
- **REQ-014-103**: System MUST support scheduled recurring exports (weekly/monthly/quarterly)
- **REQ-014-104**: System MUST store generated reports for 7 days for re-download

### Screen 7 — Platform Overview

- **REQ-014-060**: System MUST display three-section overview (Operations, Performance, Finance) with platform-wide aggregations
- **REQ-014-061**: System MUST display provider TTFQ health distribution donut (Green/Amber/Red counts)
- **REQ-014-062**: System MUST display provider engagement rate and dormant provider count
- **REQ-014-063**: System MUST display platform-wide conversion funnel and TTFQ bullet chart
- **REQ-014-064**: System MUST display platform GMV, commission earned, upcoming payout obligations, and cash-at-risk as financial summary tiles

### Screen 8 — Provider Performance & Engagement

- **REQ-014-065**: System MUST display provider league table (sortable by TTFQ, conversion, acceptance rate, rating, response rate) with platform variance column
- **REQ-014-066**: System MUST display provider performance scatter plot (TTFQ vs. conversion rate, one point per provider)
- **REQ-014-067**: System MUST display provider activity table with last active date, monthly quote count, and engagement status (Active/At Risk/Dormant)
- **REQ-014-068**: System MUST display new provider ramp chart (quotes submitted vs. days since onboarding)
- **REQ-014-069**: Engagement status thresholds MUST be admin-configurable

### Screen 9 — Patient Acquisition & Funnel

- **REQ-014-070**: System MUST display inquiry volume trend (area line with prior period overlay)
- **REQ-014-071**: System MUST display platform funnel trend as multi-line monthly chart
- **REQ-014-072**: System MUST display new vs. returning patient rate as stacked monthly bar + KPI tiles
- **REQ-014-073**: System MUST display patient journey time distribution (p50, p90, histogram)
- **REQ-014-074**: System MUST display inquiry seasonality calendar heatmap (rolling 12-month view)
- **REQ-014-075**: System MUST display affiliate acquisition KPI tiles and ranked table; display limitation note that tracking begins at booking stage, not inquiry stage

### Screen 10 — Geographic Intelligence

- **REQ-014-076**: System MUST display patient demand by country (choropleth map OR ranked table — implementation choice)
- **REQ-014-077**: System MUST display provider coverage by country (ranked bar)
- **REQ-014-078**: System MUST display demand vs. supply gap table with gap flag; only show countries with ≥5 inquiries in period
- **REQ-014-079**: System MUST display conversion rate by patient country (ranked bar with platform median reference)
- **REQ-014-080**: System MUST display emerging patient origins table (countries with >20% inquiry growth vs. prior period and >10 inquiries in current period)

### Screen 11 — Treatment Outcomes

- **REQ-014-081**: System MUST display treatment completion rate per type (bar chart with platform average reference)
- **REQ-014-082**: System MUST display cancellation and no-show rate per treatment type
- **REQ-014-083**: System MUST display treatment volume trend as stacked area chart (monthly)
- **REQ-014-084**: System MUST display average review sub-scores per treatment type (5 sub-scores)
- **REQ-014-085**: System MUST display aftercare activation rate per treatment type
- **REQ-014-086**: System MUST NOT include any clinical outcome metrics (graft survival, hair density, complication rates) — these are not in the database

### Screen 12 — Financial Health & Cashflow

- **REQ-014-087**: System MUST display platform GMV and net revenue as dual-line area chart (monthly)
- **REQ-014-088**: System MUST display commission earned trend with admin-configurable target reference line
- **REQ-014-089**: System MUST display refund volume/rate and failed payment rate as KPI tiles and monthly trend
- **REQ-014-090**: System MUST display cash-at-risk aging (stacked horizontal bar, same buckets as Screen 1 C3, platform-wide)
- **REQ-014-091**: System MUST display upcoming provider payout obligations table (amount, provider, date, cadence)
- **REQ-014-092**: System MUST display installment plan health donut (On-time / Overdue / Defaulted)
- **REQ-014-093**: System MUST display affiliate commission obligations table
- **REQ-014-094**: System MUST display revenue by currency donut

### Screen 13 — Pricing Intelligence

- **REQ-014-095**: System MUST display average quote amount by treatment type (bar chart with p25–p75 error bars)
- **REQ-014-096**: System MUST display price range per treatment (range bar or box plot: min, p25, median, p75, max)
- **REQ-014-097**: System MUST display average quote amount by provider country (grouped bar, top 3 treatments)
- **REQ-014-098**: System MUST display conversion rate by price bracket
- **REQ-014-099**: System MUST display price trend per treatment over last 12 months
- **REQ-014-100**: System MUST display price outlier provider table; outlier threshold configurable by admin (default 30%); require minimum 5 quotes per treatment per provider

---

## Key Entities

- **Entity 1 — Analytics Metrics Aggregate** (provider-level, daily): `provider_id`, `date`, `inquiry_count`, `qualified_count`, `quoted_count`, `accepted_count`, `in_progress_count`, `ttfq_p50_minutes`, `ttfq_p90_minutes`, `sla_minutes`, `weekly_income`, `commission_deducted`, `currency`

- **Entity 2 — Booking Intensity Record** (provider-level, daily): `provider_id`, `date`, `bookings_on_day`, `monthly_daily_avg`, `intensity_index`, `baseline_type`

- **Entity 3 — Quote Aging Snapshot** (provider-level, refreshed every 15 min): `quote_id`, `provider_id`, `accepted_at`, `age_hours`, `aging_bucket`, `treatment_type`, `country`, `amount`, `currency`

- **Entity 4 — Platform Analytics Aggregate** (platform-level, daily): `date`, `total_inquiries`, `total_providers_active`, `platform_ttfq_p50`, `platform_ttfq_p90`, `platform_conversion_rate`, `platform_gmv`, `platform_commission`, `new_patients`

- **Entity 5 — Provider Engagement Snapshot** (provider-level, daily): `provider_id`, `last_login_at`, `quotes_submitted_30d`, `inquiry_response_rate_30d`, `engagement_status`

- **Entity 6 — Benchmark Segment** (platform-level, weekly): `segment_id`, `segment_type`, `provider_count`, `metric_medians` (JSON), `calculated_date`

- **Entity 7 — Payout Record**: `payout_id`, `provider_id`, `period_start`, `period_end`, `amount`, `currency`, `status`, `disbursed_at`, `cadence`

- **Entity 8 — Export Report Configuration**: `config_id`, `provider_id`, `report_type`, `screens_included` (array), `date_range_type`, `recurring`, `frequency`, `email_recipients`, `last_generated_at`

- **Entity 9 — Currency Exchange Rate**: `date`, `base_currency`, `target_currency`, `exchange_rate`, `fetched_at`

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-11 | 1.0 | Initial PRD creation | AI Assistant |
| 2026-04-16 | 2.0 | Major rewrite: single-page cockpit design locked (Screen 1); global filters, cross-filtering, TTFQ spec, all Section A/B/C widgets specified | AI Assistant |
| 2026-04-16 | 3.0 | Full 12-screen expansion: Screens 2–6 (provider analytics suite + export config) and Screens 7–13 (admin analytics suite) added; all widgets verified against system-data-schema.md; data model gaps documented; 104 functional requirements; 9 key entities | AI Assistant |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | [Name] | [Date] | [Status] |
| Technical Lead | [Name] | [Date] | [Status] |
| Stakeholder | [Name] | [Date] | [Status] |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B
**Last Updated**: 2026-04-16
