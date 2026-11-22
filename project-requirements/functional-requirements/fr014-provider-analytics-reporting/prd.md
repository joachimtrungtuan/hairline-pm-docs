# FR-014 - Provider Analytics & Reporting

**Module**: PR-05: Financial Management & Reporting | A-08: Analytics & Reporting
**Feature Branch**: `fr014-provider-analytics-reporting`
**Created**: 2025-11-11
**Version**: 3.20
**Status**: 🟡 Revised — Documentation Approved; Pending Consolidated Verification
**Source**: FR-014 from system-prd.md; SRC-MTG-002 (MTG-002-D03–D06 and O01 as refined by the Product Owner); FR-004, FR-005, and FR-006 approved quote/acceptance/booking contracts; Product Owner approvals dated 2026-10-07, 2026-10-13, and 2026-10-14

---

## Executive Summary

The Provider Analytics & Reporting module delivers a **13-screen suite (12 analytical + 1 export config)** split across two tenants: provider and admin.

On the **provider side**, six screens cover the full operational picture — a locked cockpit dashboard for daily triage (Screen 1), four deeper analytical views for conversion performance, patient insights, financial health, and pricing/benchmarks (Screens 2–5), and an export configuration utility (Screen 6). Each screen has a single job and is accessed via the Analytics section of the provider portal.

On the **admin side**, seven screens (Screens 7–13) give Hairline visibility into platform-wide health, provider quality and engagement, patient acquisition, geographic supply/demand gaps, treatment outcomes, financial cashflow, and pricing landscape.

All metrics derive from operational records or calculations over those records. This PRD defines the approved target analytics contract; it does not establish that the current implementation already produces the revised metrics.

The counting boundary is the FR-004 Parent Quote, not its packages or date-price alternatives, as defined in FR-004 REQ-004-030 and FR-005 REQ-005-020. Inquiry funnels, parent-quote acceptance rates, accepted-price analytics, and confirmed-booking metrics have distinct grains and MUST NOT be interchanged. See **Analytics Counting & Time Basis** for the shared definitions used by every screen and export.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-XX)**: No direct patient-facing features. Patient behaviour data (inquiry timing, booking patterns, location) feeds the analytics pipeline. (REQ-014-119)
- **Provider Platform (PR-05)**: 6-screen suite (5 screens in the "Analytics" nav + Screen 1 as the platform landing page, not accessed via the Analytics nav section). (REQ-014-120)
- **Admin Platform (A-08)**: 7-screen analytics suite accessible from the admin "Analytics" nav section. (REQ-014-121)
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
- In-app TTFQ SLA-breach alert (`inquiry.ttfq_sla_breached`, FR-020/FR-030 catalog): sent once per distributed inquiry/provider pair when that provider has not submitted a parent quote within the FR-026 SLA target from the inquiry's distribution to the provider. Recipients: provider users permitted to respond to inquiries (FR-009). Default channel: in-app notification dropdown; email/push are off by default and admin-configurable in FR-030. No alert is sent if the inquiry is cancelled, the distribution is withdrawn, or the provider responds before the SLA elapses; it is never repeated for the same pair. The alert does not change TTFQ metrics. (REQ-014-122)

**Out of Scope**:

- Channel attribution (organic, paid ads, social media) — not tracked in database (REQ-014-123)
- Clinical outcome data (graft survival, hair density results) — not tracked in database (REQ-014-124)
- Real-time collaborative dashboard viewing (future enhancement) (REQ-014-125)

### Entry Points

- **Provider**: "Analytics" nav item → defaults to Screen 2 (Performance); Screen 1 (Main Dashboard) is the platform landing page, not the analytics section entry (REQ-014-126)
- **Admin**: "Analytics" nav item → defaults to Screen 7 (Platform Overview) (REQ-014-126)
- **Export**: "Export Report" button available on all provider analytics screens (REQ-014-126)

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

**A2 — Export from any screen**: Provider clicks "Export" button → reaches Screen 6 pre-populated with the current screen's section selected. (REQ-014-127)

**B1 — Analytics pipeline delay**: Non-blocking banner shown; cached data displayed with last-updated timestamp. (REQ-014-128)

**B2 — Low sample (<30 inquiries for provider)**: Helper copy shown on affected widgets; partial data still rendered.

---

## Screen Specifications

---

### Provider Platform (PR-05)

#### Screen 1: Main Dashboard (Cockpit)

> **STATUS: LAYOUT LOCKED.** The Product Owner approved a formula/metric-label-only exception on 2026-10-07 through CR-FR014-20261007-01 for TTFQ, the booking funnel, and accepted-but-unpaid aging. The existing sections, widget count, chart types, filters, and responsive layout remain locked; this exception does not authorize a redesign. On 2026-10-13 the Product Owner approved one further exception, recorded as an amendment to the same CR: the Qualified stage is removed from the B1 funnel and B4 trend lines because FR-003 has no canonical spam or qualification data. B1 therefore has four stages; section count, widget count, chart types, filters, and responsive layout are unchanged. A second 2026-10-13 amendment to the same CR approved two further limited exceptions: TTFQ is measured from the inquiry's distribution to the provider (not inquiry creation), and the Inquiry Queue keeps only the `New` row badge because `Needs Info` and `Awaiting Price` have no source state in FR-003 or FR-004. Columns, pagination, section count, widget count, chart types, filters, and responsive layout are unchanged.
> Design reference: Figma node 6358-111596

**Purpose**: Single scrollable page for daily triage. Three vertically stacked sections (A: Inbox, B: Performance, C: Financials). No tabs.

**Layout**: Header (filters) → Section A → Section B → Section C. Collapse to single-column on ≤1024px.

---

##### Header — Global Filters (REQ-014-181)

| Field | Type | Default | Graph field |
|-------|------|---------|---|
| Time range | Dropdown | Last 4 weeks (options: Today / This week / Last 4 weeks / Last 12 weeks / Custom) | no graph field (control) |
| Country | Multi-select dropdown | All countries | no graph field (control) |

**Global UX**: Cross-filtering — a single click on a widget element applies it as a filter to all sections. Drill-down to the operational list opens only from an explicit "View list" action in that element's tooltip or keyboard focus menu, in a new context (Rule 3); each widget's "Drill-down" line names that list. This clarifies click behaviour only; sections, widgets, chart types, filters, and layout are unchanged. Tooltips state metric definition + numerator/denominator + time basis. Localize dates/currencies/timezone. Skeletons on load. (REQ-014-181)

---

##### Section A — Inbox

###### Tile 1: New Inquiries (REQ-014-182)

- Value: Today count + This week count (dual display)
- Tap → Inquiries list (time filter applied)

###### Tile 2: Time to First Quote (TTFQ) (REQ-014-183)

- Value: p50 and p90 vs SLA (compact dual-bullet)
- Color: Green (p50 ≤ SLA and p90 ≤ 2×SLA) · Amber (p50 ≤ SLA and p90 > 2×SLA) · Red (p50 > SLA)
- Tap → Inquiries list grouped by coordinator

**TTFQ formula**: `Parent Quote.first_sent_at` of the provider's earliest parent quote for the inquiry `− inquiry_providers.distributed_at` per `(providerId, inquiryId)` (elapsed wall time from the inquiry's distribution to that provider; display in provider timezone). This is the same clock as the FR-020/FR-030 `inquiry.ttfq_sla_breached` alert, so a provider who receives an inquiry later (for example after an FR-003 exclusive-provider decline releases it to normal distribution) is not penalised for time before distribution. Missing `distributed_at` yields no TTFQ observation for that pair, not a fallback to `inquiry.created_at`. `first_sent_at` is set by FR-004 on the parent quote's first send; a re-send or new version never changes it. Draft creation, option/date-price creation, later parent quotes, edits, and resends do not reset the first-response timestamp. Exclude auto-acks; calls/messages do not stop the clock. (REQ-014-184)

###### Table: Inquiry Queue (REQ-014-185)

| Column | Notes | Graph field |
|--------|-------|---|
| Received | Relative time + SLA countdown timer | ENT-provider-inquiry.distributed_at |
| Patient | ID-masked (HP102589-0001 · "Aylin K****") | ENT-patient.anonymized_id, ENT-patient.name |
| Age | Patient age | ENT-patient.age |
| Problem | Treatment area | ENT-inquiry.treatment_area_snapshot |
| Country | Patient country | ENT-patient.country |
| Actions | View link | no graph field (control) |

Row badge: `New` = inquiry distributed to this provider (FR-003 `inquiry_providers`) with no parent quote submitted by the provider yet (FR-004). Default sort: `New` rows first, then received time ascending. 10 per page. (REQ-014-185)

---

##### Section B — Performance (2×2 Grid)

###### B1: Inquiry → Booking Conversion (REQ-014-186)

- Chart: Funnel chart
- Stages: Inquiries → Quoted → Accepted → Confirmed booking
- Each stage: Count + Step % (stage ÷ previous stage)
- Footer: Overall booking conversion = Confirmed bookings ÷ Inquiries
- Confirmed booking = successful deposit or first installment charge confirms the FR-006 Booking. `In Progress` means procedure started via FR-010 and is not the payment-confirmation label.
- Count distinct inquiry/provider pairs in a single inquiry cohort cumulatively through each reached stage, per Analytics Counting & Time Basis; multiple parent quotes and subquotes do not multiply the funnel.
- Drill-down: click stage → filtered Inquiries list

###### B2: TTFQ vs SLA (REQ-014-187)

- Chart: Bullet chart (p50 + p90, SLA as target marker)
- Axis: 0 → max(3×SLA, 1.2×p90), units = minutes (render h:m)
- Color: Green/Amber/Red per TTFQ formula above
- Drill-down: click → Inquiries list grouped by coordinator

###### B3: Booking Intensity vs Monthly Average (Next 6 Weeks) (REQ-014-188)

- Chart: Calendar heatmap (6 rows × 7 cols, Mon→Sun)
- Colored metric: Intensity Index = `(Bookings_on_day ÷ MonthlyDailyAvg_for_that_day's_month) × 100`
- `Bookings_on_day` counts FR-006 Bookings whose appointment falls on that day and whose status is `Confirmed` or `In Progress`. Held bookings (`Accepted`), `Payment Window Expired` and `Cancelled` bookings never count, and no separate held figure is shown. The monthly average uses the same status filter.
- Color scale: ≤50% Cool · 50–90% Below avg · 90–110% Neutral · 110–150% Above avg · >150% Hot
- Cell tooltip: `Confirmed bookings: N • Monthly avg: m/day • Index: X%`
- Drill-down: click cell → Schedule day view
- Baseline priority: 12-month same-month avg → current MTD → rolling 90-day
- Index clamped 0–300% for coloring; actual value in tooltip

###### B4: Patient Location Breakdown (REQ-014-189)

- Chart: Donut (top 8 countries by inquiry share + Other)
- Center: total Inquiries in range
- Slice labels: `CC (ISO-2) • %`
- Slice border: thin/neutral <20% confirmed booking rate · medium/amber 20–40% · thick/green >40%
- Tooltip: `Country • Inquiries: N • Confirmed bookings: B • Confirmed booking rate: R%`
- Confirmed bookings and the confirmed booking rate use the inquiry cohort and Confirmed booking stage defined in Analytics Counting & Time Basis (rate = Confirmed bookings ÷ Inquiries).
- Drill-down: click slice → filtered Inquiries list

---

##### Section C — Financials (2×2 Grid)

###### C1: Earnings Trend (REQ-014-190)

- Chart: Area line chart (weekly, X = ISO week start, Y = income in provider currency)
- Single series: Income only
- Drill-down: click week → Earnings report filtered to that week

###### C2: Revenue by Treatment (REQ-014-191)

- Chart: Pareto bar chart (ranked bars + cumulative % line)
- X = treatment (dynamic), Y₁ = income, Y₂ = cumulative %
- Top N + Other; drill-down: click bar → Cases list filtered by treatment
- Treatment attribution follows Screen 4 Widget 2 (definition only; chart and layout unchanged)

###### C3: Quote → Payment Aging (Accepted but Unpaid) (REQ-014-192)

- Chart: Stacked horizontal bar
- Buckets: 0–24h · 1–3d · 4–7d · 8–14d · >14d
- X = count of accepted selections awaiting successful initial payment; optional legend by treatment (top 3) or country
- Age = snapshot time − `AcceptanceEvent.acceptedAt`; count one pending Booking/AcceptanceEvent with a valid exclusive payment-window hold. Exclude cancelled selections, superseded acceptance events, expired holds, and `Payment Window Expired` bookings, even if a flat quote status still says Accepted.
- Drill-down: click bucket → Accepted Quotes list resolved to the exact accepted subquote and pending booking; retain the same chart and buckets. Older buckets may legitimately be empty with the default 48-hour hold; use the actual configured deadline, not an assumed fixed limit.

###### C4: Payouts — History & Upcoming (REQ-014-193)

- Chart: Column bar (monthly, last 6–12 months) + inline table (2–3 rows)
- Inline table columns: Type, Period, Amount, Scheduled Date, Cadence
- Type = the provider display status from the Screen 4 Widget 8 FR-017 mapping (Upcoming / Processing / Paid / Failed; Voided is never shown). Rows: the next Upcoming payout, any Processing or Failed payout, then the most recent Paid payout, up to 3 rows. Scheduled Date = FR-017 scheduled payout date; for Paid rows it shows the paid date. Cadence = how the payout is released (see Assumption 5), not a per-clinic frequency. Definition only; columns and layout unchanged (REQ-014-177)
- Drill-down: click bar → Payout statements list (CSV/PDF export)

---

##### States

- Low sample (<30 inquiries): helper copy; still render counts
- Loading: skeletons for all tiles and charts
- Error: non-blocking banners + retry; log telemetry (REQ-014-194)
- PII: patient names masked throughout

---

#### Screen 2: Performance & Conversion

**Purpose**: Deep analysis of how efficiently the provider converts inquiries to bookings, including TTFQ trends and benchmarking.

**Filters**: Time range (same options as Screen 1 global) + Country + Treatment type (multi-select)

---

##### Widget 1: Funnel Conversion Trend (REQ-014-195)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Multi-line chart (one line per funnel stage) | no graph field (display) |
| X axis | Week or month (toggle) | no graph field (display) |
| Y axis | Conversion % to that stage from Inquiries | ENT-analytics-metrics-aggregate.funnel_trend_series |
| Lines | Quoted % · Accepted % · Confirmed booking % | no graph field (display) |
| Drill-down | Click a point → Inquiries list filtered to that stage + time period | no graph field (control) |

**Calculation**: Each stage % = distinct inquiry/provider pairs in the selected inquiry cohort that have reached that stage by the reporting cutoff ÷ all inquiry/provider pairs in that cohort. Counts are cumulative, not mutually exclusive highest-stage buckets. Use the shared cohort and cutoff definitions in Analytics Counting & Time Basis.

---

##### Widget 2: Conversion Breakdown by Treatment Type (REQ-014-196)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Grouped bar chart | no graph field (display) |
| X axis | Treatment type (from catalog) | no graph field (display) |
| Y axis | Quote-to-booking conversion % (Quoted → Confirmed booking) | ENT-analytics-metrics-aggregate.conversion_by_treatment |
| Groups per bar | Quoted count, Accepted count, Confirmed booking count | no graph field (display) |
| Drill-down | Click bar → filtered list of quoted inquiries for that treatment | no graph field (control) |

**Data source**: Patients do not choose a treatment in the FR-003 inquiry; the provider chooses it in the FR-004 Parent Quote. A treatment segment therefore starts at Quoted: the base is inquiries quoted with that treatment (Parent Quote treatment context), and Accepted and Confirmed booking stages follow the FR-005/FR-006 handoff for that treatment. Inquiries that were never quoted have no treatment and appear only in the all-treatments funnel (Widget 1). Deduplicate `(providerId, inquiryId, treatmentId)` within each treatment segment before counting stages; child options, date-price records, and quote revisions MUST NOT multiply counts. An inquiry may appear in more than one treatment segment, so segment counts are not additive.

---

##### Widget 3: Conversion Breakdown by Patient Country (REQ-014-197)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Horizontal ranked bar chart | no graph field (display) |
| Y axis | Patient country (top 10 by inquiry volume) | no graph field (display) |
| X axis | Booking conversion % (Inquiries → Confirmed booking) | ENT-analytics-metrics-aggregate.conversion_by_country |
| Secondary bar | Inquiry count (context for the rate) | no graph field (display) |
| Drill-down | Click bar → filtered Inquiries list for that country | no graph field (control) |

**Data source**: `inquiries.patient_id → patients.location_id → countries.name`, with temporary fallback to legacy `patients.location` only for unmigrated rows.

---

##### Widget 4: Quote Acceptance Rate Trend (REQ-014-198)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Line chart | no graph field (display) |
| X axis | Week or month (toggle) | no graph field (display) |
| Y axis | Parent-quote acceptance rate = distinct accepted parent quotes ÷ distinct submitted parent quotes in the same first-submission cohort | ENT-analytics-metrics-aggregate.acceptance_rate_trend, ENT-analytics-metrics-aggregate.parent_quote_acceptance_rate |
| Drill-down | Click point → parent Quotes list for that first-submission cohort, with accepted subquote provenance where present | no graph field (control) |

---

##### Widget 5: TTFQ Trend Over Time (REQ-014-199)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Dual-line chart (p50 line + p90 line) | no graph field (display) |
| X axis | Week or month (toggle) | no graph field (display) |
| Y axis | Minutes (render as h:m) | ENT-analytics-metrics-aggregate.ttfq_trend_series, ENT-analytics-metrics-aggregate.ttfq_p50_minutes, ENT-analytics-metrics-aggregate.ttfq_p90_minutes |
| Reference line | SLA target | no graph field (display) |
| Color band | Green/Amber/Red zones based on SLA thresholds | no graph field (display) |
| Drill-down | Click point → Inquiries list for that period sorted by TTFQ | no graph field (control) |

---

##### Widget 6: Cancellation & No-Show Rate (REQ-014-200)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Two KPI tiles + trend sparklines | no graph field (display) |
| Tile 1 | Cancellation rate = cancelled (post-confirmed) ÷ confirmed bookings | ENT-analytics-metrics-aggregate.cancellation_rate |
| Tile 2 | No-show rate = no-show ÷ confirmed bookings | ENT-analytics-metrics-aggregate.no_show_rate |
| Sparkline | Rate trend over selected period | no graph field (display) |
| Drill-down | Click Cancellation tile → Bookings list filtered to post-confirmation cancellations (FR-006); click No-show tile → Cases list filtered to FR-010 closure reason `No-show` | no graph field (control) |

**Data source**: Cancellations come from post-confirmation cancellations in the FR-006 Booking lifecycle. No-shows come from FR-010 case closures with closure reason `No-show`; No-show is an admin-managed case closure label, not a booking pipeline status. Each confirmed booking counts at most once, and a booking closed as No-show counts as a no-show, not a cancellation. Draft/quote expiry and `Payment Window Expired` before confirmation are not post-confirmation cancellations or no-shows. Historical acceptance remains recorded separately.

---

##### Widget 7: Platform Benchmarks (Anonymised) (REQ-014-201)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Comparison table with variance indicators | no graph field (display) |
| Metrics | TTFQ p50 · Conversion rate · Quote acceptance rate · Avg rating | ENT-benchmark-segment.metric_medians |
| Columns | Provider value · Platform median · Variance (±%) · Percentile band (Bottom 25% / Mid 50% / Top 25%) | ENT-analytics-metrics-aggregate.benchmark_variance |
| Color | Green / Amber / Red per the Shared Benchmark Rule (direction-aware; TTFQ lower is better) | no graph field (display) |

**Business rule**: Peer pool, minimum pool size, anonymisation, and colour follow the Shared Benchmark Rule in Analytics Counting & Time Basis. If the pool is insufficient, display "Benchmark unavailable — not enough providers in your segment." (REQ-014-142)

---

**Business Rules**:

- All widgets share the same time range and country filter (REQ-014-202)
- Treatment type filter applies to quote-stage and later metrics (Quoted, Accepted, Confirmed booking). Inquiries carry no treatment, so with a treatment selected the Inquiries stage and inquiry-based rates show "— (inquiries have no treatment)" and conversion is measured from Quoted. TTFQ is not treatment-filtered (REQ-014-203)
- Low-sample handling follows the global Data Quality Rule 7 (<30 inquiries → helper copy, data still rendered); no widget-specific override applies

---

#### Screen 3: Patient Analytics

**Purpose**: Understanding who the provider's patients are, where they come from, how satisfied they are, and how long their journey takes.

**Filters**: Time range + Country

---

##### Widget 1: Full Patient Location Breakdown (REQ-014-204)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Ranked table + donut chart (linked) | no graph field (display) |
| Table columns | Country · Inquiries · Confirmed bookings · Confirmed booking rate · Avg rating (Confirmed bookings and rate follow the inquiry cohort and Confirmed booking stage in Analytics Counting & Time Basis) | ENT-analytics-metrics-aggregate.patient_location_table |
| Table | All countries (not capped at 8); sortable by any column | no graph field (display) |
| Donut | Top 10 countries by inquiry volume + Other | no graph field (display) |
| Drill-down | Click row/slice → Inquiries list filtered to that country | no graph field (control) |

**Avg rating**: average `overall_rating` of this provider's Published FR-013 reviews published within the selected range, grouped by the reviewing patient's country (review → patient → `patients.location_id → countries.name`, with the same legacy `patients.location` fallback). Shows "—" when the country has no reviews in range; the review count appears in the tooltip.

---

##### Widget 2: New vs. Returning Patients (REQ-014-205)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Donut (current period split) + trend line over time | no graph field (display) |
| Definition | Provider-scoped: New = patient's first inquiry distributed to this provider · Returning = patient with an earlier inquiry distributed to this provider | no graph field (display) |
| Trend | New vs. Returning count per month over selected range | ENT-analytics-metrics-aggregate.new_patient_count, ENT-analytics-metrics-aggregate.returning_patient_count |
| Drill-down | Click segment → Patient list filtered by type | no graph field (control) |

**Data source**: `inquiries.patient_id` joined to this provider's `inquiry_providers` records — count distinct patient_ids whose earliest inquiry distributed to this provider falls in the range = New; patients in the range with an earlier inquiry distributed to this provider = Returning. Inquiries the patient sent only to other providers do not make them Returning.

---

##### Widget 3: Patient Journey Time (REQ-014-206)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Two KPI tiles + distribution histogram | no graph field (display) |
| Tile 1 | Median days from inquiry → payment (p50) | ENT-analytics-metrics-aggregate.journey_time_p50_days |
| Tile 2 | p90 days from inquiry → payment | ENT-analytics-metrics-aggregate.journey_time_p90_days |
| Histogram | Distribution of journey durations in days (binned: 0–7d · 8–14d · 15–30d · 31–60d · >60d) | ENT-analytics-metrics-aggregate.journey_time_histogram |
| Drill-down | Click histogram bin → Inquiries list filtered to that journey-duration range | no graph field (control) |

**Calculation**: first successful initial-payment capture time that confirms the FR-006 Booking − `inquiry.created_at`, for bookings first confirmed within the selected range. Resolve the booking through its AcceptanceEvent and selected subquote; count the inquiry once. Payment-attempt creation, failed attempts, later installments, and retries of the same successful event MUST NOT add journey observations.

---

##### Widget 4: Review Sub-Scores by Treatment (REQ-014-207)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Grouped bar chart | no graph field (display) |
| X axis | Treatment type | no graph field (display) |
| Y axis | Score (1–5) | no graph field (display) |
| Groups per bar | Overall · Results · Staff · Facility · Value | ENT-analytics-metrics-aggregate.review_subscores_by_treatment |
| Data source | FR-013 per-treatment sub-scores endpoint (REQ-013-023), keyed by `treatment_id`, Published reviews only; not joined through quote status | no graph field (display) |
| Drill-down | Click bar → Reviews list filtered to that treatment | no graph field (control) |

---

##### Widget 5: Treatment Preference Distribution (REQ-014-208)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Horizontal ranked bar chart | no graph field (display) |
| Y axis | Treatment type | no graph field (display) |
| X axis | Quoted inquiry count + Booking count (dual bars) | ENT-analytics-metrics-aggregate.treatment_preference |
| Purpose | What treatments the provider quotes most vs. what actually gets booked | no graph field (display) |
| Drill-down | Click bar → filtered Inquiries or Bookings list | no graph field (control) |

**Data source**: Quoted bars count distinct inquiries the provider quoted, by the treatment of the submitted Parent Quote (FR-004); inquiries have no treatment until quoted. Booking bars count Confirmed bookings (FR-006), by the treatment of the accepted parent quote (FR-005 AcceptanceEvent). Both follow Analytics Counting & Time Basis; quote statuses are not used.

---

##### Widget 6: Aftercare Activation Rate (REQ-014-209)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | KPI tile + trend sparkline | no graph field (display) |
| Value | Aftercare plans activated ÷ completed treatments | ENT-analytics-metrics-aggregate.aftercare_activation_rate |
| Drill-down | Click → Aftercare records list | no graph field (control) |

**Data source**: FR-011 aftercare records created for procedures completed in the period ÷ procedures completed in the period (FR-010 completion), by the accepted parent's treatment. Each completed procedure counts once.

---

**Business Rules**:

- No patient age distribution widget is included in this version.
- Returning patient definition: based on the same provider's patient base (not platform-wide repeat visits).
- PII: no patient names or identifiers shown; all aggregated. (REQ-014-210)

---

#### Screen 4: Finance & Payouts

**Purpose**: Full financial picture — revenue breakdown, refunds, installment health, and complete payout history.

**Filters**: Time range + Country + Treatment type (applicability per Rule 5A)

---

##### Widget 1: Revenue Trend (REQ-014-211)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Area line chart | no graph field (display) |
| X axis | Week / Month / Quarter (toggle) | no graph field (display) |
| Y axis | Income amount (provider currency) | ENT-analytics-metrics-aggregate.revenue_trend_series |
| Single series | Income (captured payments only) | no graph field (display) |
| Drill-down | Click period → Payments list filtered to that period | no graph field (control) |

**Calculation**: Gross captured income per the Refund Source of Truth rule — `SUM(payments.amount)` where `payment_type ≠ 'refund'` and `payment_status IN ('completed', 'refunded')`, bucketed by `payments.created_at`. A later refund does not remove the original payment from income.

---

##### Widget 2: Revenue by Treatment — Full Breakdown (REQ-014-212)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Horizontal ranked bar chart (full list, paginated if >15) | no graph field (display) |
| Y axis | Treatment name (all, not capped) | no graph field (display) |
| X axis | Income amount | ENT-analytics-metrics-aggregate.revenue_by_treatment |
| Secondary metric | % of total revenue | no graph field (display) |
| Drill-down | Click bar → Payments list filtered to that treatment | no graph field (control) |

**Data source**: Income per the Refund Source of Truth rule, attributed to a treatment through payment → FR-006 Booking → FR-005 AcceptanceEvent → accepted parent quote's treatment. Each payment is attributed once. Payments that cannot be resolved to an accepted parent are shown as "Unattributed", not dropped or assigned to a guessed treatment. Screen 1 C2 uses the same attribution.

---

##### Widget 3: Revenue by Patient Country (REQ-014-213)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Horizontal ranked bar chart | no graph field (display) |
| Y axis | Patient country (top 10 + Other) | no graph field (display) |
| X axis | Income amount | ENT-analytics-metrics-aggregate.revenue_by_country |
| Secondary metric | Patient count | no graph field (display) |
| Drill-down | Click bar → Payments list filtered to that country | no graph field (control) |

**Data source**: `payments.patient_id → patients.location_id → countries.name`, with temporary fallback to legacy `patients.location` only for unmigrated rows.

---

##### Widget 4: Commission & Net Revenue (REQ-014-214)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Three KPI tiles + trend line (both on same chart) | no graph field (display) |
| Tile 1 | Total income (gross) | ENT-analytics-metrics-aggregate.income_total |
| Tile 2 | Commission deducted | ENT-analytics-metrics-aggregate.commission_total |
| Tile 3 | Net income = Total income (gross) − Commission deducted, for the same period | ENT-analytics-metrics-aggregate.net_income |
| Trend | Gross income line + commission deducted area, stacked | no graph field (display) |

**Calculation**: Commission deducted = sum of percentage-model deductions for each completed payment in range plus flat-rate deductions for each procedure completed in range (FR-010 completion, per FR-015). Each deduction uses the booking's commission snapshot taken at booking confirmation (FR-015 REQ-015-022, FR-029), not the provider's current commission settings:

- Percentage model: `payments.amount × (snapshot_commission_percentage / 100)`
- Flat-rate model: `snapshot_commission_amount` once per completed procedure, regardless of procedure price, number of payments, or installments (FR-015)

Gross, commission, and net income are displayed in provider currency. Net income does not subtract refunds; refunds are reported separately in Widget 5.

---

##### Widget 5: Refunds (REQ-014-215)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Two KPI tiles + trend | no graph field (display) |
| Tile 1 | Total refund amount (period) | ENT-analytics-metrics-aggregate.refund_total_amount |
| Tile 2 | Refund rate = refund count ÷ captured payment count (both per the Refund Source of Truth rule) | ENT-analytics-metrics-aggregate.refund_rate |
| Trend | Monthly refund rate over selected range | no graph field (display) |
| Drill-down | Click → Payments list filtered to refund type | no graph field (control) |

**Data source**: Refund rows only — `payments.payment_type = 'refund'` with `payment_status = 'completed'` (Refund Source of Truth rule). The original payment's `refunded` status is not counted as a second refund. (REQ-014-141)

---

##### Widget 6: Installment vs. Full Payment Split (REQ-014-216)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Donut + KPI summary | no graph field (display) |
| Segments | Installment payments · Full payments | ENT-analytics-metrics-aggregate.installment_payment_share |
| KPI | Avg number of installments for installment plans | ENT-analytics-metrics-aggregate.avg_installment_count |
| Trend | Monthly installment adoption rate = bookings first confirmed in the month whose payment is an FR-007B installment plan ÷ all bookings first confirmed in the month (one observation per booking) | ENT-analytics-metrics-aggregate.installment_adoption_rate |
| Drill-down | Click segment → Payments list filtered by payment type | no graph field (control) |

**Data source**: the payment type (`payments.payment_type`, value `installment` versus full payment) for the payment split; FR-007B installment plan records for the average installment count and the adoption rate. The donut counts payment records; the adoption rate counts bookings, so the two values are not interchangeable.

---

##### Widget 7: Cash-at-Risk Summary (REQ-014-217)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | KPI tile + link to Main Dashboard Section C3 for full aging detail | no graph field (display) |
| Value | Sum of accepted subquote total prices for selections awaiting initial payment with a valid hold; label as potential accepted booking value, not captured revenue or outstanding installment debt | ENT-analytics-metrics-aggregate.cash_at_risk_amount |
| Count | Distinct pending bookings/AcceptanceEvents in each aging bucket, following Screen 1 C3 exclusions and deadline checks | no graph field (display) |
| Note | This is a summary view; the full aging stacked bar is in Screen 1 Section C3 | no graph field (display) |

---

##### Widget 8: Payout History & Schedule (REQ-014-218)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Column bar chart (monthly, full history) + paginated table below | no graph field (display) |
| Bar chart | Last 12 months of disbursed payouts | no graph field (display) |
| Table columns | Period · Amount · Status (Upcoming / Processing / Paid / Failed) · Paid date · Cadence (how the payout is released, see Assumption 5) | ENT-provider-payout.payout_period, ENT-payout.net_amount, ENT-payout.status, ENT-payout.executed_at, ENT-payout.payout_method (REQ-014-177) |
| All rows | Full history (not limited to the 2–3 rows shown in the Main Dashboard Section C4 inline table) | no graph field (display) |
| Drill-down | Click bar or row → Payout statement detail (CSV/PDF export) | no graph field (control) |

**Payout status mapping (FR-017)**:

| Provider display status | FR-017 payout statement status |
|---|---|
| Upcoming | No statement yet for the period, or Pending Approval, Approved, or Overdue (internal admin review states are not shown to providers) |
| Processing | Processing (Stripe transfer initiated) |
| Paid | Paid (`transfer.paid`); Paid date = webhook time |
| Failed | Failed (`transfer.failed`); returns to Processing when admin retries |
| *(not shown)* | Voided — excluded from the provider's payout chart, table, totals, and exports. Voided is an internal admin audit state; the period appears as Upcoming again once FR-017 re-generates a statement on the next payout cycle |

---

**Business Rules**:

- Income = payments with `payment_type ≠ 'refund'` and `payment_status IN ('completed', 'refunded')` (Refund Source of Truth rule); refunds are reported separately in Widget 5 (REQ-014-141)
- Commission is calculated from each booking's commission snapshot taken at booking confirmation (FR-015 REQ-015-022), not from a single percentage-only field or the provider's current settings; provider screens must display a note clarifying whether the period includes percentage-based deductions, flat-rate deductions, or both (REQ-014-219)
- All amounts in provider currency; FX rates locked at payment `created_at` date; footer note "Historical exchange rates applied" (REQ-014-220)
- Payout history shows each payout period with its provider display status (Upcoming, Processing, Paid or Failed) per the Payout status mapping above; future payouts beyond the next scheduled one are not projected (REQ-014-221)
- Aggregate each completed payment, refund, commission deduction, or payout once at its owning record grain before joining quote provenance. Unselected options and repeated booking/acceptance notifications MUST NOT multiply revenue or deductions; this revision does not change commission, installment, refund, or payout policy. (REQ-014-140)

---

#### Screen 5: Pricing & Benchmarks

**Purpose**: Understand the prices patients actually accepted, their descriptive relationship with parent-quote acceptance rates, and the provider's position relative to platform peers. This screen does not measure the full offered-price market or establish that price causes conversion changes.

**Filters**: Time range + Country + Treatment type

---

##### Widget 1: Average Accepted Price by Treatment (REQ-014-222)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Bar chart + trend line | no graph field (display) |
| X axis | Treatment type | no graph field (display) |
| Y axis | Average accepted subquote total price (provider reporting currency) | ENT-analytics-metrics-aggregate.avg_accepted_price_by_treatment |
| Trend overlay | Provider's own average accepted price over time, bucketed by AcceptanceEvent.acceptedAt | no graph field (display) |
| Drill-down | Click bar → Quotes list filtered to accepted selections for that treatment and acceptance period | no graph field (control) |

---

##### Widget 2: Accepted Price Distribution (REQ-014-223)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Histogram | no graph field (display) |
| X axis | Accepted subquote total price (binned, e.g., 0–1k · 1k–2k · 2k–3k · 3k–5k · >5k; dynamic bins based on accepted-price range) | ENT-analytics-metrics-aggregate.accepted_price_histogram |
| Y axis | Accepted selection count (one observation per accepted parent quote) | no graph field (display) |
| Reference lines | Median accepted price · Platform median accepted price (anonymised) | ENT-analytics-metrics-aggregate.accepted_price_median |
| Drill-down | Click bin → Quotes list filtered to accepted selections in that price range and acceptance period | no graph field (control) |

---

##### Widget 3: Accepted Price vs. Parent-Quote Acceptance Rate (REQ-014-224)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Scatter plot | no graph field (display) |
| X axis | Average accepted subquote price among accepted parents in the selected first-submission cohort, per treatment type | no graph field (display) |
| Y axis | Distinct accepted parent quotes ÷ all submitted parent quotes in that same cohort, per treatment type | no graph field (display) |
| Points | One point per treatment type (labelled) | ENT-analytics-metrics-aggregate.price_vs_acceptance_scatter |
| Reference lines | Platform median X (average accepted price) and platform median Y (parent-quote acceptance rate), using the same cohort and reporting cutoff | no graph field (display) |
| Purpose | Descriptive comparison of accepted prices and acceptance rates across treatments; does not show conversion probability at an offered price or prove a causal price effect | no graph field (display) |

**Note**: A treatment needs a non-zero submitted-parent denominator and at least one accepted selection to have both coordinates. If fewer than 3 treatment types qualify, replace the chart with "Insufficient treatment variety to compare accepted prices and acceptance rates." Unaccepted parents remain in Y's denominator but contribute no amount to X; tooltips show both sample sizes and the first-submission cohort basis, which differs from acceptance-period pricing widgets.

---

##### Widget 4: Platform Benchmark Comparison (REQ-014-225)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Comparison table | no graph field (display) |
| Rows (metrics) | TTFQ p50 · Overall booking conversion rate · Parent-quote acceptance rate · Average accepted price · Avg overall rating · Avg results rating | no graph field (display) |
| Columns | Provider value · Platform median · Variance (±%) · Percentile band (Bottom 25% / Mid 50% / Top 25%) | ENT-benchmark-segment.metric_medians |
| Color coding | Per the Shared Benchmark Rule: Green = at or better than median · Amber = up to 10% worse · Red = more than 10% worse; TTFQ lower is better; average accepted price has no colour | no graph field (display) |
| Drill-down | Click metric row → corresponding detailed screen (e.g., TTFQ → Screen 2 Widget 5) | no graph field (control) |

**Business rule**: Benchmark pool follows the Shared Benchmark Rule in Analytics Counting & Time Basis (≥30 inquiries, rolling 12 months, minimum 5 providers). If pool is too small, display "Not enough peer providers to generate a meaningful benchmark yet." (REQ-014-142)

---

**Business Rules**:

- Provider identity is fully anonymised in all benchmark calculations (REQ-014-156)
- Benchmark data refreshes at the FR-026 Analytics Configuration benchmark refresh frequency (default Weekly; not real-time) (REQ-014-226)
- Amount metrics use only immutable accepted-selection prices, including the accepted promotion; never substitute a minimum, maximum, average, or sum of unaccepted alternatives. Historical acceptance remains an observation after later cancellation or hold expiry; those outcomes are measured separately. (REQ-014-227)
- Standalone price widgets use the acceptance-time cohort. The scatter explicitly uses the parent first-submission cohort so both axes refer to the same offered parent population. (REQ-014-228)
- Price displayed in provider reporting currency; preserve the accepted currency and locked exchange-rate provenance and apply Rule 10 for any additional reporting-currency conversion. Apply the same historical conversion basis to provider and peer amounts; current package prices or today's FX MUST NOT rewrite the accepted value. (REQ-014-229)
- Price benchmarks include only peers with accepted-price observations; the existing minimum 5-provider benchmark pool still applies to that metric. Unaccepted parents are not zero-price observations. (REQ-014-230)

---

#### Screen 6: Export Report Configuration

**Purpose**: Allow providers to generate PDF or CSV exports of any analytics screen's data.

**Data Fields**: (REQ-014-231)

| Field | Type | Required | Notes | Graph field |
|-------|------|----------|-------|---|
| Report type | Radio | Yes | PDF Summary or CSV Detailed | ENT-export-report-config.report_type |
| Screens to include | Checkboxes | Yes | Performance, Patient Analytics, Finance & Payouts, Pricing & Benchmarks (Screen 1 is excluded — it contains real-time operational data not suitable for static reports) | ENT-export-report-config.screens_included |
| Date range | Date picker | Yes | Max 12-month span | ENT-export-report-config.custom_start, ENT-export-report-config.custom_end |
| Country filter | Dropdown | No | Optional | ENT-export-report-config.country_filter |
| Treatment filter | Dropdown | No | Optional; applies to quote-stage and later data only (Rule 5A) | ENT-export-report-config.treatment_filter |
| Email delivery | Checkbox | No | Sends to the selected recipients | ENT-export-report-config.email_delivery |
| Recipients | Multi-select | When email delivery is on | Provider's registered email (always included) plus up to 5 active provider team members (FR-009) who are permitted to view every widget included in the export (Rules 15A/15B) | ENT-export-report-config.email_recipients |
| Schedule recurring | Checkbox + select | No | Weekly / Monthly / Quarterly; when on, the date picker is replaced by "previous full period" | ENT-export-report-config.recurring, ENT-export-report-config.frequency |

**Business Rules**:

- Widget-level permission scope: an export contains only the widgets the generating user is permitted to see on each selected screen (Rules 15A, 15B and 15F); widgets the user cannot see are omitted, not shown empty or locked. Recurring runs re-resolve this scope against the configuration owner's permissions at run time. (REQ-014-232)
- PDF reports include provider logo sourced from `providers.profile_image`; no provider-specific color theming (platform default palette is used) — schema does not define brand color fields and this is intentional for v1 (REQ-014-233)
- Report generation <60 seconds; async queue for large datasets (REQ-014-169)
- Generated reports stored 7 days for re-download from Report History section
- Email delivery: PDF attachment + secure link (expires 48 hours), sent through S-03 as the FR-030 `analytics.export_ready` event (email + in-app) to each recipient (REQ-014-234)
- Max 5 active recurring configurations per provider (REQ-014-235)
- Recurring date range: each run covers the previous full period in the provider's timezone (`providers.timezone`): Monday–Sunday week, calendar month, or calendar quarter. Runs start at 06:00 provider local time on the first day after the period ends. (REQ-014-236)
- Recurring failures: a failed run is retried up to 3 times at 30-minute intervals; after the final failure the run shows as Failed in Report History with a manual retry action. No partial report is emailed. (REQ-014-237)
- Recurring management: providers can edit, pause, resume, or delete a recurring configuration; edits apply from the next run. Recipients who are deactivated or lose permission are dropped automatically at the next run. (REQ-014-238)
- PDF and CSV MUST use the same counting units, cohorts, cutoff, accepted-price eligibility, and financial deduplication as the included screens. State the metric definition, sample size, reporting currency, FX basis, and data-as-of time. For detailed quote/acceptance rows, retain authorized inquiry/provider IDs, parent/option/date-price/subquote IDs, AcceptanceEvent and booking IDs where present, accepted aggregate versions, and immutable price/currency provenance; unaccepted parent rows have no accepted amount or accepted-choice IDs. (REQ-014-239)

##### Report History & Recurring Exports

Added by [CR-FR014-20261013-02](change-request-2026-10-13-export-history-accessibility.md). Shown below the export form on Screen 6, as two tabs.

**Tab 1 — Generated Reports** (reports generated in the last 7 days, newest first, 20 per page): (REQ-014-240)

| Field | Type | Source | Notes | Graph field |
|-------|------|--------|-------|---|
| Generated at | Timestamp | System (generation job completion or failure time) | Provider timezone | ENT-analytics-generated-report.generated_at |
| Report type | Label | Export configuration (user input) | PDF Summary or CSV Detailed | ENT-analytics-generated-report.report_type |
| Screens included | Text list | Export configuration (user input) | | ENT-analytics-generated-report.screens_included |
| Period covered | Date range | Export configuration (user input; or "previous full period" for recurring runs) | | ENT-analytics-generated-report.period_covered |
| Trigger | Label | System | One-off or Recurring (shows the configuration's frequency) | ENT-analytics-generated-report.trigger |
| Status | Badge | System (generation job) | Queued / Generating / Ready / Failed | ENT-analytics-generated-report.status |
| Expires on | Date | System calculated: generated at + 7 days | Hidden for Failed rows | ENT-analytics-generated-report.expires_on |
| Actions | Buttons | — | Download (Ready only); Retry (Failed only; queues a new run with the same configuration) | no graph field (control) |

**Tab 2 — Recurring Exports** (all of the provider's recurring configurations, maximum 5 active): (REQ-014-241)

| Field | Type | Source | Notes | Graph field |
|-------|------|--------|-------|---|
| Frequency | Label | Export configuration (user input) | Weekly / Monthly / Quarterly | ENT-export-report-config.frequency |
| Report type and screens | Text | Export configuration (user input) | | ENT-export-report-config.report_type, ENT-export-report-config.screens_included |
| Recipients | Count + tooltip list | Export configuration (user input; FR-009 team members) | Dropped recipients are removed at the next run | ENT-export-report-config.email_recipients |
| Next run | Timestamp | System calculated (`next_run_at`, Entity 8) | Blank when paused | ENT-export-report-config.next_run_at |
| Last run status | Badge | System (`last_run_status`, Entity 8) | Ready / Failed / Not run yet | ENT-export-report-config.last_run_status |
| Status | Badge | Export configuration | Active / Paused | ENT-export-report-config.status |
| Actions | Buttons | — | Edit (opens the export form pre-filled; changes apply from the next run), Pause / Resume, Delete (confirmation required; already generated reports stay until they expire) | no graph field (control) |

- Only users permitted to view every widget in a report can see or download it (Rules 15A/15B); downloads use the same secure-link mechanism as email delivery. (REQ-014-242)
- Resuming a paused configuration does not back-fill runs missed while it was paused. (REQ-014-243)
- Empty states: "No reports generated in the last 7 days" and "No recurring exports set up". (REQ-014-244)

---

### Admin Platform (A-08)

#### Screen 7: Platform Overview Dashboard

**Purpose**: Platform health at a glance — one scrollable page with three sections mirroring the provider dashboard structure but aggregated across all providers.

**Filters**: Time range (same options) + Country + Provider (optional, defaults to All)

**Layout**: Three sections (A: Operations, B: Performance, C: Finance). Responsive layout required: multi-column on desktop, reduced-density stacked layout on tablet/mobile, with a single-column fallback on ≤1024px.

---

##### Section A — Operational Health

###### Tile 1: Active Providers (REQ-014-245)

- Value: Count of providers with `status = active` at the end of the selected period
- Sub-value: New providers onboarded in period
- Tap → Provider Management (FR-015)

###### Tile 2: Total Inquiries (REQ-014-246)

- Value: Platform-wide inquiry count in period
- Sub-value: % change vs. prior equivalent period
- Tap → Inquiries list (admin)

###### Tile 3: New Patients Registered (REQ-014-247)

- Value: `patients.created_at` count in period
- Tap → Patient Management (FR-016)

###### Tile 4: Provider TTFQ Health Distribution (REQ-014-248)

- Chart: Donut (Green / Amber / Red provider counts)
- Value: Count and % in each tier
- Tap → Screen 8 filtered to Red tier

###### Tile 5: Provider Engagement Rate (REQ-014-249)

- Value: % of active providers who first submitted at least 1 parent quote within the Dormant threshold window (FR-026 Analytics Configuration, default 30 days) ending at the period end. "Active providers" here means account `status = active` (the Tile 1 definition, FR-015), not the activity-based Active engagement status in Screen 8 Widget 3
- Sub-values: Dormant providers (engagement status from Screen 8 Widget 3, based on provider activity) and Non-responding providers (0 first-submitted parent quotes within the same Dormant threshold window; drafts, child records, edits, and resends do not count as new submissions). These are separate counts; a provider can be active but non-responding.
- Tap → Screen 8 engagement section filtered to dormant

---

##### Section B — Performance Signals

###### B1: Platform-Wide Conversion Funnel (REQ-014-250)

- Chart: Funnel chart (same 4 stages as provider funnel, but distinct platform inquiries, not summed provider funnels)
- Shows: Count + Step % for each stage
- Footer: Overall platform booking conversion = Confirmed booking inquiries ÷ Inquiries
- Drill-down: click stage → admin Inquiries list filtered to that stage

###### B2: Platform TTFQ Distribution (REQ-014-251)

- Chart: Bullet chart (platform p50 + p90 vs SLA default target)
- Shows: Distribution across all providers
- Drill-down: click → Screen 8 (Provider Performance & Engagement) sorted by TTFQ

###### B3: Top Patient Origin Countries (REQ-014-252)

- Chart: Donut (top 8 countries by inquiry volume + Other)
- Drill-down: click slice → Screen 9 filtered to that country

###### B4: Treatment Type Distribution (REQ-014-253)

- Chart: Donut (share of quoted inquiries by treatment type, from the FR-004 Parent Quote treatment; inquiries have no treatment until quoted)
- Drill-down: click slice → Screen 11 filtered to that treatment

---

##### Section C — Financial Summary

###### C1: Platform GMV (Period) (REQ-014-254)

- Value: `SUM(payments.amount)` where `payment_type ≠ 'refund'` and `payment_status IN ('completed', 'refunded')`, period (same GMV rule as Screen 12 Widget 1 and the Refund Source of Truth rule)
- Sub-value: % change vs. prior period
- Drill-down → Screen 12

###### C2: Commission Earned (Period) (REQ-014-255)

- Value: Sum of effective provider commission deductions in period, using each booking's confirmation-time commission snapshot (FR-015 REQ-015-022): percentage per completed payment; flat rate once per completed procedure (FR-015)
- Sub-value: As % of GMV
- Drill-down → Screen 12

###### C3: Upcoming Provider Payout Obligations (REQ-014-256)

- Value: Total payout amount due to providers in next 30 days
- Sub-value: Number of providers in next payout cycle
- Drill-down → Screen 12

###### C4: Platform Cash-at-Risk (REQ-014-257)

- Value: Total accepted subquote value in active pending initial-payment holds, platform-wide; same eligibility as Screen 1 C3 and Screen 4 Widget 7
- Sub-value: Count of active pending selections >14 days aging (may be zero under the default 48-hour hold); expired windows are not active cash risk
- Drill-down → Screen 12

---

**Business Rules**:

- Default time range: Last 4 weeks (same as provider dashboard)
- Provider TTFQ health tiers use the platform-wide SLA target (admin-configurable in the FR-026 Analytics Configuration, Screen 5e); there are no per-provider SLA overrides in this version (REQ-014-258)
- All three sections respect the time range filter. In Section A: Tile 1 shows providers with `status = active` at the end of the selected period plus those onboarded within it; Tiles 2 and 3 count records created within the period, compared with the prior equivalent period; Tile 4 tiers providers from TTFQ observations in the period; Tile 5 uses the trailing Dormant threshold window (default 30 days) ending at the period end, with engagement status as at the period end (REQ-014-259)

---

#### Screen 8: Provider Performance & Engagement

**Purpose**: Two-section screen — Performance (conversion quality) and Engagement (activity/dormancy). These are distinct jobs: performance tells you how well a provider works; engagement tells you whether they're working at all.

**Filters**: Time range + Country + TTFQ health tier (All / Green / Amber / Red) + Engagement status (All / Active / At Risk / Dormant)

---

##### Section A — Performance

###### Widget 1: Provider League Table (REQ-014-260)

| Column | Value | Graph field |
|--------|-------|---|
| Provider | Name + country flag | ENT-provider.name, ENT-provider.country |
| TTFQ p50 | Value + color badge | ENT-platform-analytics-aggregate.provider_league_table |
| Conversion rate | Distinct provider inquiry cohort → Confirmed booking % | ENT-platform-analytics-aggregate.provider_league_table |
| Quote acceptance rate | Distinct accepted parent quotes ÷ distinct submitted parent quotes in the same first-submission cohort | ENT-platform-analytics-aggregate.provider_league_table |
| Avg overall rating | Star rating (from reviews) | ENT-platform-analytics-aggregate.provider_league_table |
| Quote response rate | Distinct distributed inquiries answered ÷ distinct inquiries distributed to this provider in the same distribution cohort | ENT-platform-analytics-aggregate.provider_league_table |
| vs. Platform | Variance column for conversion rate (+/−%) | ENT-platform-analytics-aggregate.provider_league_table |
| Provider-fault replacements | Count of admin-authored replacement quotes created in the selected period for FR-006 provider-fault transfers away from this provider; shown on its own and never added to quote counts, conversion, or TTFQ | ENT-platform-analytics-aggregate.provider_league_table |
| Status | Health badge: Red if TTFQ tier is Red or conversion is more than 10% below platform median; Amber if TTFQ tier is Amber or conversion is up to 10% below median; otherwise Green. If the provider has <30 inquiries (Rule 7), the badge uses TTFQ only and shows a low-sample marker | ENT-platform-analytics-aggregate.provider_league_table |

- Sortable by any column
- Default sort: TTFQ status (Red first) then conversion rate ascending
- Paginated: 20 per page
- Drill-down: click row → provider's own analytics view (read-only admin view of provider's Screen 2)

###### Widget 2: Performance Distribution (REQ-014-261)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Scatter plot | no graph field (display) |
| X axis | TTFQ p50 (minutes) | no graph field (display) |
| Y axis | Conversion rate (%) | no graph field (display) |
| Points | One per provider, labelled with the provider name (admin view, Rule 14) | ENT-platform-analytics-aggregate.provider_performance_scatter |
| Reference lines | Platform median TTFQ · Platform median conversion rate | no graph field (display) |
| Quadrants | Fast + High conversion (ideal) · Slow + Low conversion (needs support) | no graph field (display) |
| Drill-down | Click point → that provider's detail | no graph field (control) |

---

##### Section B — Engagement

###### Widget 3: Provider Activity Table (REQ-014-262)

| Column | Value | Graph field |
|--------|-------|---|
| Provider | Name + country | ENT-provider.name, ENT-provider.country |
| Last active | `MAX(action_at)` from `provider_activity_logs` for that `provider_id`; for last login specifically use `MAX(action_at) WHERE action_type = 'login'` | ENT-provider-engagement-snapshot.last_active_at |
| Quotes this month | Distinct parent quotes first submitted in current calendar month; no extra counts for options, date-price records, versions, or resends | ENT-provider-engagement-snapshot.parent_first_submissions_this_month |
| Inquiry response rate | Distinct distributed inquiries answered ÷ distinct inquiries distributed to this provider (last 30-day distribution cohort) | ENT-provider-engagement-snapshot.response_rate |
| Status | Based on Last active: Active (activity within the At Risk threshold, default 7d) · At Risk (between the At Risk and Dormant thresholds, default 7–30d) · Dormant (no activity beyond the Dormant threshold, default 30d). Thresholds come from FR-026 Screen 5e | ENT-provider-engagement-snapshot.engagement_status |

- Filter by status (Active / At Risk / Dormant)
- Drill-down: click row → provider detail in FR-015

###### Widget 4: New Provider Ramp (REQ-014-263)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Line chart (multiple series) | no graph field (display) |
| X axis | Days since onboarding (0–90 days) | no graph field (display) |
| Y axis | Cumulative distinct parent quotes first submitted | ENT-platform-analytics-aggregate.new_provider_ramp_series |
| Series | Each provider onboarded in the selected period (one line each, labelled with provider name per Rule 14) | no graph field (display) |
| Reference line | Platform average ramp curve | no graph field (display) |
| Purpose | Identify new providers who are struggling to get started | no graph field (display) |

**Data source**: Providers with `created_at` within the selected period; parent `first_sent_at − providers.created_at` (`first_sent_at` is set by FR-004 on first send and never changed by a re-send) for days-since-onboarding offset. Count each parent identity once, regardless of later versions, resends, or child record counts.

###### Widget 5: Engagement Health Summary (REQ-014-264)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Three KPI tiles | no graph field (display) |
| Tile 1 | Active providers count (Screen 8 Widget 3 status; default activity in last 7 days) | ENT-platform-analytics-aggregate.engagement_active_provider_count |
| Tile 2 | At-risk providers count (Screen 8 Widget 3 status; default 7–30 days no activity) | ENT-platform-analytics-aggregate.engagement_at_risk_provider_count |
| Tile 3 | Dormant providers count (Screen 8 Widget 3 status; default >30 days no activity) | ENT-platform-analytics-aggregate.engagement_dormant_provider_count |

###### Widget 6: Provider Team Size & Role Distribution

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Table plus platform summary | no graph field (display) |
| Table columns | Provider (name + country) · Team size (active team members) · Members per clinic role (Owner, Manager, Clinical Staff, Billing Staff) | no graph field (display) |
| Platform summary | Distribution of providers by team size and of team members across the four clinic roles | no graph field (display) |
| Time basis | Snapshot at the end of the selected period | no graph field (display) |
| Drill-down | Click row → provider detail in FR-015 | no graph field (control) |

**Data source**: FR-009 provider team membership and role records. The widget shows counts only; it does not list individual team members. Provider identity is shown to the admin as on the rest of Screen 8 (Rule 14).

---

**Business Rules**:

- Provider identity is NOT anonymised to the admin (admin must be able to identify and contact providers) (REQ-014-157)
- Last-activity data is sourced from `provider_activity_logs.action_at` (canonical activity log); last active = `MAX(action_at)` per provider; last login = `MAX(action_at) WHERE action_type = 'login'` per provider user. Do not use `provider_users.last_login_at` — this field does not exist in the schema. (REQ-014-265)
- "Inquiry response rate" follows the shared distinct-inquiry distribution cohort definition and MUST stay between 0% and 100%. If authoritative distribution records are unavailable, display "Response rate unavailable — distribution data missing"; do not substitute parent quote count or total platform inquiries as the denominator. (REQ-014-266)
- Engagement status thresholds (7d / 30d) are configurable by admin
- Admin-authored replacement quotes are excluded from every quote count, conversion rate, and TTFQ figure on this screen and appear only in the Provider-fault replacements column, attributed to the provider at fault

---

#### Screen 9: Patient Acquisition & Funnel

**Purpose**: How patients enter the platform and move through the inquiry-to-booking funnel. Affiliate acquisition tracked where available.

**Filters**: Time range + Country + Treatment type (applicability per Rule 5A)

**Note**: Channel attribution (organic, paid, social) is NOT available — this screen covers volume trends, funnel efficiency, and affiliate-sourced traffic only.

---

##### Widget 1: Inquiry Volume Trend (REQ-014-267)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Area line chart | no graph field (display) |
| X axis | Week or month (toggle) | no graph field (display) |
| Y axis | Inquiry count | ENT-platform-analytics-aggregate.inquiry_volume_trend |
| Comparison overlay | Prior equivalent period (dashed line) | no graph field (display) |
| Drill-down | Click period → admin Inquiries list for that period | no graph field (control) |

---

##### Widget 2: Platform Funnel Trend Over Time (REQ-014-268)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Multi-line chart (one line per stage) | no graph field (display) |
| X axis | Month | no graph field (display) |
| Y axis | Conversion % to that stage from Inquiries | ENT-platform-analytics-aggregate.platform_funnel_trend |
| Lines | Quoted % · Accepted % · Confirmed booking % | no graph field (display) |
| Purpose | Show whether platform-wide conversion is improving or declining | no graph field (display) |
| Drill-down | Click line point → admin Inquiries list filtered to that stage + month | no graph field (control) |

---

##### Widget 3: New vs. Returning Patients (REQ-014-269)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Stacked bar chart (monthly) + KPI tiles | no graph field (display) |
| Bars | New patient count + Returning patient count per month | ENT-platform-analytics-aggregate.new_vs_returning_series |
| Tile 1 | New patient rate (period) | ENT-platform-analytics-aggregate.new_patient_rate |
| Tile 2 | Returning patient rate (period) | ENT-platform-analytics-aggregate.returning_patient_rate |
| Definition | New = first inquiry ever · Returning = has prior inquiry on record | no graph field (display) |
| Drill-down | Click bar segment → Patient list filtered by type and period | no graph field (control) |

---

##### Widget 4: Patient Journey Time (Platform-Wide) (REQ-014-270)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Two KPI tiles + distribution histogram | no graph field (display) |
| Tile 1 | Platform median days inquiry → payment (p50) | ENT-platform-analytics-aggregate.journey_time_p50_days |
| Tile 2 | Platform p90 days inquiry → payment | ENT-platform-analytics-aggregate.journey_time_p90_days |
| Histogram | Distribution across all converting patients (same bins as Screen 3 Widget 3) | ENT-platform-analytics-aggregate.journey_time_histogram |

**Calculation**: Same first successful booking-confirming payment and one-observation-per-inquiry rule as Screen 3 Widget 3, across the platform; distribution to multiple providers or later installments does not multiply observations.

---

##### Widget 5: Inquiry Seasonality (REQ-014-271)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Month × weekday heatmap (intensity = weekday average vs. monthly daily average) | no graph field (display) |
| Layout | 12 rows (months) × 7 columns (Mon→Sun) | no graph field (display) |
| Intensity | `average daily inquiries on that weekday in that month ÷ that month's overall daily average × 100` | ENT-platform-analytics-aggregate.inquiry_seasonality_index |
| Purpose | Identify seasonal peaks and campaign-worthy slow periods | no graph field (display) |
| Cell tooltip | `Inquiries on this weekday: N • Weekday avg: w • Month daily avg: m • Index: X%` | no graph field (display) |

---

##### Widget 6: Affiliate Acquisition (REQ-014-272)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Three KPI tiles + ranked table | no graph field (display) |
| Tile 1 | Affiliate-sourced bookings (count in period) | ENT-platform-analytics-aggregate.affiliate_booking_count |
| Tile 2 | Affiliate contribution rate = affiliate bookings ÷ total bookings | ENT-platform-analytics-aggregate.affiliate_contribution_rate |
| Tile 3 | Avg affiliate booking value = sum of FR-018 Entity 3 `Booking Total` for the affiliate-sourced bookings counted in Tile 1 ÷ that booking count, in platform base currency (USD, Rule 10) | ENT-platform-analytics-aggregate.avg_affiliate_booking_value |
| Table columns | Affiliate name · Bookings · Revenue · Commission owed · Conversion rate (FR-018 definition: checkouts where the code was applied and resulted in a booking ÷ checkouts where the code was applied) | ENT-platform-analytics-aggregate.affiliate_table |
| Drill-down | Click affiliate row → affiliate detail in FR-018 | no graph field (control) |

**Data source**: FR-018 Entity 3 `Booking with Affiliate Attribution`. Affiliate-sourced = payment-confirmed booking with a validly captured affiliate-bound code or affiliate auto-apply referral link, per FR-018 Rule 11. Attribution is counted even when a higher-priority patient or provider discount controlled the final price, so bookings, revenue, and commission owed reconcile with FR-018 referral credit. The final discount applied is not the attribution source.

**Limitation note**: Affiliate tracking begins when the affiliate code or referral link is captured in the booking journey, not at the inquiry stage. It is not possible to attribute an inquiry to an affiliate source.

---

**Business Rules**:

- Seasonality heatmap always shows a rolling 12-month view regardless of time range filter (for pattern recognition) (REQ-014-273)
- Affiliate rows show only affiliates with at least 1 booking in the selected period; inactive affiliates are filtered out (REQ-014-274)

---

#### Screen 10: Geographic Intelligence

**Purpose**: Strategic supply/demand view. Where is patient demand concentrated? Where does the platform have insufficient provider coverage? Used for expansion planning and targeted provider recruitment.

**Filters**: Time range (affects inquiry and booking data) + Treatment type (applicability per Rule 5A)

---

##### Widget 1: Patient Demand Map (REQ-014-275)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Choropleth map OR ranked table with flag icons (implementation choice) | no graph field (display) |
| Value mapped | Inquiry count per patient country (in selected period) | ENT-platform-analytics-aggregate.demand_by_country |
| Color scale | 5-bin scale from low (cool) to high (warm) | no graph field (display) |
| Tooltip | `Country · Inquiries: N · Confirmed bookings: B · Conversion rate: R%` (Confirmed booking stage per Analytics Counting & Time Basis) | no graph field (display) |
| Drill-down | Click country → filtered admin Inquiries list | no graph field (control) |

---

##### Widget 2: Provider Coverage by Country (REQ-014-276)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Ranked horizontal bar chart | no graph field (display) |
| Y axis | Country (provider country) | no graph field (display) |
| X axis | Active provider count | ENT-platform-analytics-aggregate.provider_coverage_by_country |
| Drill-down | Click bar → Provider list filtered to that country | no graph field (control) |

---

##### Widget 3: Demand vs. Supply Gap (REQ-014-277)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Ranked table | no graph field (display) |
| Columns | Patient country · Inquiry count · Provider count (in that country) · Inquiries per provider · Gap flag | ENT-platform-analytics-aggregate.demand_supply_gap |
| Gap flag | "No coverage" if the country has 0 active providers (inquiries per provider is shown as "—", not N/A); otherwise flagged if inquiries per provider > platform median by ≥50% | no graph field (display) |
| Sort | Default: "No coverage" countries first (by inquiry count descending), then inquiries per provider descending (highest gap first) | no graph field (display) |
| Purpose | Identify countries to target for provider recruitment | no graph field (display) |

**Note**: "Provider country" = provider's registered location. The gap metric is an approximation — patients may travel internationally, so a high inquiries-per-provider ratio in one country does not necessarily mean patients cannot be served.

---

##### Widget 4: Conversion Rate by Patient Country (REQ-014-278)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Horizontal ranked bar chart | no graph field (display) |
| Y axis | Patient country (top 15 by inquiry volume) | no graph field (display) |
| X axis | Booking conversion rate (Inquiries → Confirmed booking) | ENT-platform-analytics-aggregate.conversion_by_patient_country |
| Secondary bar | Inquiry count (for context) | no graph field (display) |
| Reference line | Platform median conversion rate | no graph field (display) |
| Drill-down | Click bar → admin Inquiries list filtered to that country | no graph field (control) |

---

##### Widget 5: Emerging Patient Origins (REQ-014-279)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Ranked table | no graph field (display) |
| Columns | Country · Inquiry count (current period) · Inquiry count (prior period) · Growth % | ENT-platform-analytics-aggregate.emerging_origins |
| Filter | Countries with >10 inquiries in current period and >20% growth vs prior period | no graph field (display) |
| Purpose | Spot new markets before they become dominant | no graph field (display) |

---

**Business Rules**:

- Country data is sourced canonically from `patients.location_id → countries.name`; if `location_id` is null for legacy rows, the UI may temporarily fall back to `patients.location` until migration cleanup is complete. No IP-geolocation fallback is assumed in this version. (REQ-014-280)
- Demand vs. Supply gap table only shows countries with ≥5 inquiries in the selected period to avoid statistical noise
- Map (if used) requires a separate map rendering library; ranked table is the functional fallback

---

#### Screen 11: Treatment Outcomes

**Purpose**: How treatments are performing operationally and in patient satisfaction. **Scope is strictly operational and satisfaction-based** — no clinical outcomes exist in the database (no graft survival rates, no hair density measurements, no complication data).

**Filters**: Time range + Country + Provider (optional) + Treatment type

---

##### Widget 1: Treatment Completion Rate (REQ-014-281)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Bar chart | no graph field (display) |
| X axis | Treatment type | no graph field (display) |
| Y axis | Completion rate = Confirmed bookings (FR-006) in the confirmation cohort whose procedure reached FR-010 completion by the reporting cutoff ÷ all Confirmed bookings in that cohort, by the accepted parent's treatment | ENT-platform-analytics-aggregate.completion_rate_by_treatment |
| Reference line | Platform average completion rate | no graph field (display) |
| Drill-down | Click bar → admin Bookings list filtered to that treatment | no graph field (control) |

---

##### Widget 2: Cancellation & No-Show Rate by Treatment (REQ-014-282)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Grouped bar chart | no graph field (display) |
| X axis | Treatment type | no graph field (display) |
| Y axis | Rate % | no graph field (display) |
| Groups | Cancellation rate · No-show rate | ENT-platform-analytics-aggregate.cancellation_no_show_by_treatment |
| Drill-down | Click Cancellation bar → admin Bookings list filtered to post-confirmation cancellations (FR-006) for that treatment; click No-show bar → admin Cases list filtered to FR-010 closure reason `No-show` for that treatment | no graph field (control) |

---

##### Widget 3: Treatment Volume Trend (REQ-014-283)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Stacked area chart | no graph field (display) |
| X axis | Month | no graph field (display) |
| Y axis | Booking count | ENT-platform-analytics-aggregate.treatment_volume_trend |
| Areas | One per treatment type (dynamic, top 5 + Other) | no graph field (display) |
| Purpose | Track which treatments are growing or declining in demand | no graph field (display) |
| Drill-down | Click area segment → admin Bookings list filtered to treatment + month | no graph field (control) |

---

##### Widget 4: Average Review Scores by Treatment (REQ-014-284)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Grouped bar chart | no graph field (display) |
| X axis | Treatment type | no graph field (display) |
| Y axis | Score (1–5) | no graph field (display) |
| Groups | Overall · Results · Staff · Facility · Value | ENT-platform-analytics-aggregate.review_subscores_by_treatment |
| Data source | FR-013 per-treatment sub-scores endpoint (REQ-013-023), keyed by `treatment_id`, Published reviews only | no graph field (display) |
| Provider filter | Required. The endpoint returns one provider's sub-scores, so the widget renders only when a single provider is selected; with "All providers" it shows "Select a provider to view review scores by treatment" | no graph field (display) |
| Drill-down | Click bar → Reviews list filtered to that provider and treatment | no graph field (control) |

---

##### Widget 5: Aftercare Activation Rate (REQ-014-285)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | KPI tile + trend line + bar by treatment type | no graph field (display) |
| KPI | Platform-wide aftercare activation rate = FR-011 aftercare records created for procedures completed in the period ÷ FR-010 completed procedures in the period, by the accepted parent's treatment | ENT-platform-analytics-aggregate.aftercare_activation_rate |
| Bar chart | Activation rate broken down by treatment type | ENT-platform-analytics-aggregate.aftercare_activation_by_treatment |
| Drill-down | Click bar → Aftercare records list | no graph field (control) |

---

##### Widget 6: Provider Distribution by Treatment Specialisation

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Stacked horizontal bar chart | no graph field (display) |
| Y axis | Treatment type | no graph field (display) |
| X axis | Provider count offering that treatment | ENT-platform-analytics-aggregate.provider_count_by_treatment |
| Drill-down | Click bar → Provider list filtered to that treatment | no graph field (control) |

**Data source**: Submitted parent quotes (FR-004) grouped by treatment and `provider_id`; a provider "offers" a treatment if they have first-submitted at least 1 parent quote for it in the last 12 months.

---

**Business Rules**:

- Completion rate needs at least 5 Confirmed bookings in the confirmation cohort for each bar, to avoid single-event noise. With a single provider selected, a treatment bar needs ≥5 of that provider's Confirmed bookings for the treatment. With all providers, each treatment bar and the platform average pool every provider's bookings and need ≥5 pooled bookings; low-volume providers are not dropped from the pooled rate. Below the minimum, the bar is marked as not enough data per Rule 8; the exact visual treatment of low-sample bars is a UX design decision (REQ-014-287)
- No-show rate uses FR-010 case closures with closure reason `No-show` (admin-managed case closure label, not a booking pipeline status) over confirmed bookings in the period; cancellation rate uses post-confirmation cancellations from the FR-006 Booking lifecycle. A booking closed as No-show counts as a no-show, not a cancellation (REQ-014-288)
- Do NOT add any clinical outcome metrics (achieved graft count, hair density, success rates). FR-004 Estimated Grafts is a provider's quote estimate, not a clinical outcome, and must not be presented as a result (REQ-014-289)

---

#### Screen 12: Financial Health & Cashflow

**Purpose**: Platform financial risk monitoring and revenue health. The admin's question is: "Is money flowing correctly, what do we owe, and where are the risks?"

**Filters**: Time range + Country + Currency

---

##### Widget 1: Platform GMV & Net Revenue (REQ-014-290)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Dual-line area chart | no graph field (display) |
| X axis | Month | no graph field (display) |
| Y₁ series | Platform GMV (gross payment volume) | ENT-platform-analytics-aggregate.gmv |
| Y₂ series | Net revenue (platform commission earned in period, accrual basis) | ENT-platform-analytics-aggregate.net_revenue |
| Tooltip | GMV · Refunds completed in period · Net GMV (GMV − refunds) · Net revenue | ENT-platform-analytics-aggregate.refunds_completed_amount, ENT-platform-analytics-aggregate.net_gmv |
| Drill-down | Click period → detailed payment records | no graph field (control) |

**Calculation**: GMV = `SUM(payments.amount)` where `payment_type ≠ 'refund'` and `payment_status IN ('completed', 'refunded')` (gross captured volume; refund rows are neither added nor subtracted, and a later refund does not remove the original payment). Net GMV = GMV − completed refund rows in the same period, per the Refund Source of Truth rule, so each refund is subtracted exactly once. Net revenue = platform commission earned in the period, using the Widget 2 formula (percentage per completed payment; flat rate once per completed procedure). Payout timing does not affect net revenue.

---

##### Widget 2: Commission Earned Trend (REQ-014-291)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Bar chart (monthly) | no graph field (display) |
| X axis | Month | no graph field (display) |
| Y axis | Commission earned = sum of effective provider commission deductions in period, using each booking's confirmation-time commission snapshot (FR-015 REQ-015-022): percentage per completed payment; flat rate once per completed procedure (FR-015) | ENT-platform-analytics-aggregate.commission_earned_monthly_series |
| Reference line | Target monthly commission (admin-configurable in FR-026; hidden until a target is set) | no graph field (display) |
| Drill-down | Click bar → filtered payment records with commission breakdown | no graph field (control) |

---

##### Widget 3: Refund & Failed Payment Health (REQ-014-292)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Four KPI tiles + trend | no graph field (display) |
| Tile 1 | Refund volume (amount, period) | ENT-platform-analytics-aggregate.refund_volume |
| Tile 2 | Refund rate = refund count ÷ captured payment count (both per the Refund Source of Truth rule) | ENT-platform-analytics-aggregate.refund_rate |
| Tile 3 | Failed payment count (period) | ENT-platform-analytics-aggregate.failed_payment_count |
| Tile 4 | Failed payment rate = failed ÷ total attempted payments. Attempted = non-refund `payments` rows (`payment_type ≠ 'refund'`) created in the period with `payment_status IN ('completed', 'refunded', 'failed')`; failed = those rows with `payment_status = 'failed'`. `pending` rows are excluded until resolved. Each row counts once, so a retry that creates a new payment row is a new attempt | ENT-platform-analytics-aggregate.failed_payment_rate |
| Trend | Monthly refund rate + failed rate (dual line) | no graph field (display) |
| Drill-down | Click tile → filtered Payments list | no graph field (control) |

---

##### Widget 4: Cash-at-Risk — Platform-Wide Aging (REQ-014-293)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Stacked horizontal bar chart (same as provider C3, but all providers) | no graph field (display) |
| Buckets | 0–24h · 1–3d · 4–7d · 8–14d · >14d | ENT-platform-analytics-aggregate.pending_selection_count_by_age_bucket |
| X axis | Distinct accepted selections awaiting initial payment with a valid payment-window hold (all providers) | no graph field (display) |
| Optional legend | By provider country | no graph field (display) |
| Drill-down | Click bucket → admin Quotes list resolved to accepted subquote + pending booking and filtered by active hold + aging bucket | no graph field (control) |

**Calculation**: Age from immutable `AcceptanceEvent.acceptedAt`, using the actual configured hold deadline and the Screen 1 C3 exclusions. Expired, superseded, and cancelled selections are retained in lifecycle history but excluded from active cash risk.

---

##### Widget 5: Upcoming Provider Payout Obligations (REQ-014-294)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | KPI tile + table | no graph field (display) |
| KPI | Total upcoming payout amount (next 30 days) | ENT-platform-analytics-aggregate.upcoming_payout_obligation_30d |
| Table columns | Provider · Amount · Payout date · Cadence (how the payout is released, see Assumption 5) · Status (FR-017: Pending Approval / Approved / Overdue / Processing) | ENT-platform-analytics-aggregate.upcoming_payout_table (REQ-014-177) |
| Sort | Payout date ascending | no graph field (display) |
| Drill-down | Click row → provider payout detail in FR-017 | no graph field (control) |

---

##### Widget 6: Installment Plan Health (REQ-014-295)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Donut + KPI | no graph field (display) |
| Segments | Active · Canceled · Completed · Defaulted (FR-007B Plan Status labels; Overdue is a flag on a plan, not a status segment) | ENT-platform-analytics-aggregate.installment_plan_status_counts |
| KPI | Total outstanding installment balance (Active plans, including those flagged Overdue, and Defaulted plans) | ENT-platform-analytics-aggregate.outstanding_installment_balance |
| Data source | `installment_plans` table status, using the FR-007B Plan Status values unchanged | no graph field (display) |
| Drill-down | Click segment → Installment plans list filtered by status | no graph field (control) |

---

##### Widget 7: Affiliate Commission Obligations (REQ-014-296)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | KPI tile + upcoming table | no graph field (display) |
| KPI | Total affiliate commission owed (pending payout) | ENT-platform-analytics-aggregate.affiliate_commission_owed |
| Table | Affiliate · Commission owed · Next payout date | ENT-platform-analytics-aggregate.affiliate_commission_table |
| Drill-down | Click row → FR-017 affiliate billing | no graph field (control) |

---

##### Widget 8: Revenue by Currency (REQ-014-297)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Donut | no graph field (display) |
| Segments | Per currency code (`payments.currency`) | no graph field (display) |
| Value | GMV by currency | ENT-platform-analytics-aggregate.gmv_by_currency |
| Purpose | FX exposure visibility — how much revenue is in non-base currencies | no graph field (display) |

---

**Business Rules**:

- All amounts converted to the platform base currency, USD, which is fixed by FR-029 / A-09 Currency Management (not admin-editable), using daily FX rates under Rule 10; raw currency amounts shown in tooltips (REQ-014-298)
- Net revenue is accrual-based (commission earned in the period) and does not depend on when payouts are disbursed (REQ-014-299)
- This screen is only accessible to admin roles with financial data permissions (REQ-014-300)
- Payment, refund, commission, installment, and payout metrics aggregate their owning records once before joining the accepted selection. The accepted quote amount is not captured revenue and MUST NOT replace actual financial transactions. (REQ-014-301)

---

#### Screen 13: Pricing Intelligence

**Purpose**: Accepted-price landscape across providers and treatments. Helps Hairline understand the prices patients selected and identify descriptive outliers; it does not represent every offered alternative or measure offered-price conversion.

**Filters**: Time range + Country + Treatment type

---

##### Widget 1: Average Accepted Price by Treatment (REQ-014-302)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Bar chart | no graph field (display) |
| X axis | Treatment type | no graph field (display) |
| Y axis | Average accepted subquote total price (platform base currency) | ENT-platform-analytics-aggregate.avg_accepted_price_by_treatment |
| Error bars | p25–p75 range per treatment | no graph field (display) |
| Drill-down | Click bar → Quotes list filtered to accepted selections for that treatment and acceptance period | no graph field (control) |

---

##### Widget 2: Accepted Price Range per Treatment (REQ-014-303)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Range bar chart (or box plot if supported) | no graph field (display) |
| X axis | Treatment type | no graph field (display) |
| Ranges shown | Min · p25 · Median · p75 · Max | ENT-platform-analytics-aggregate.accepted_price_range_by_treatment |
| Purpose | Show the observed spread of accepted selection prices for each treatment, not the full offered-price market | no graph field (display) |
| Reference line | Platform median per treatment | no graph field (display) |
| Drill-down | Click bar → Quotes list of accepted selections for that treatment sorted by accepted price | no graph field (control) |

---

##### Widget 3: Accepted Price by Provider Country (REQ-014-304)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Grouped bar chart | no graph field (display) |
| X axis | Provider country | no graph field (display) |
| Y axis | Average accepted subquote total price | ENT-platform-analytics-aggregate.accepted_price_by_provider_country |
| Groups | Per treatment type (top 3 by volume) | no graph field (display) |
| Purpose | Surface geographic pricing differences (e.g., Turkish providers vs. UK providers) | no graph field (display) |
| Drill-down | Click bar → Quotes list filtered to accepted selections by provider country + treatment | no graph field (control) |

---

##### Widget 4: Accepted Selections by Price Bracket (REQ-014-305)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Bar chart | no graph field (display) |
| X axis | Accepted subquote total price bracket (dynamic bins based on accepted-price distribution) | no graph field (display) |
| Y axis | Accepted selection count; tooltip also shows share of all accepted selections in the filtered acceptance-time cohort | ENT-platform-analytics-aggregate.accepted_selections_by_price_bracket |
| Reference line | None — this is a price distribution, not a conversion-rate chart | no graph field (display) |
| Purpose | Show which price brackets patients accepted, without assigning unaccepted parents an invented single price | no graph field (display) |
| Drill-down | Click bar → Quotes list filtered to accepted selections in that price bracket and acceptance period | no graph field (control) |

**Boundary**: Offered-price conversion by bracket is deferred. It requires a separately approved price attribution/denominator policy for multi-option parents; dividing accepted selections by accepted selections would misleadingly produce 100% and is prohibited.

---

##### Widget 5: Price Trend Over Time per Treatment (REQ-014-306)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Multi-line chart | no graph field (display) |
| X axis | Month (last 12 months) | no graph field (display) |
| Y axis | Average accepted subquote total price | ENT-platform-analytics-aggregate.accepted_price_trend |
| Lines | One per treatment type (top 5 by volume + Other as grey line) | no graph field (display) |
| Purpose | Track whether observed accepted prices are rising or falling | no graph field (display) |
| Drill-down | Click line point → Quotes list filtered to accepted selections for that treatment + acceptance month | no graph field (control) |

---

##### Widget 6: Price Outlier Providers (REQ-014-307)

| Property | Value | Graph field |
|----------|-------|---|
| Chart type | Ranked table | no graph field (display) |
| Columns | Provider · Treatment · Average accepted price · Platform accepted-price median · Variance % · Direction | ENT-platform-analytics-aggregate.price_outlier_providers |
| Filter | Providers whose average accepted price is ≥30% above or below the platform accepted-price median for any treatment | no graph field (display) |
| Direction | "High" (priced above) or "Low" (priced below) | no graph field (display) |
| Purpose | Flag descriptive deviations in accepted prices for review; does not conclude that a provider is pricing itself out of the market | no graph field (display) |
| Drill-down | Click row → that provider's detail in FR-015 | no graph field (control) |

---

**Business Rules**:

- All accepted prices converted to platform base currency under Rule 10, preserving immutable accepted currency/locked-rate provenance; raw accepted amounts and sample sizes shown in tooltips (REQ-014-308)
- Outlier threshold (30%) is admin-configurable
- Only accepted subquote prices from immutable AcceptanceEvents are included, one observation per accepted parent quote; current quote status or current package-library prices are not price sources. Use acceptance time for price ranges, trends, distributions, and outliers. (REQ-014-309)
- Minimum 5 accepted selections per treatment per provider required to include that provider in outlier detection; unaccepted parents do not satisfy this amount-sample threshold (REQ-014-310)
- Unaccepted parents still count once in parent response volume and parent acceptance-rate denominators; they MUST NOT be assigned zero or an arbitrary alternative's amount for price charts. (REQ-014-311)

---

## Business Rules

### Analytics Counting & Time Basis

These definitions apply to all provider/admin widgets, drill-downs, aggregates, benchmarks, and exports. A chart's "Quoted" inquiry stage is not the same unit as a submitted-parent volume metric. (REQ-014-129)

- **Parent response grain**: Governed by FR-004 REQ-004-030 (parent responses counted once; amounts only from the accepted price; Quote Options never counted as responses) and FR-005 REQ-005-020 (parent quote and subquote analytics stay distinct). Every FR-014 screen, drill-down, aggregate, benchmark and export applies that grain unchanged.
- **Admin-authored replacement quotes**: A quote that an admin authors for a replacement provider during an FR-006 provider-fault transfer (FR-004 Workflow 7, `authorType = admin`) is not a provider response. It is excluded from every provider quote count (parent response volume, inquiry response rate, parent-quote acceptance rate), from booking conversion and the inquiry funnel for the replacement provider, and from TTFQ, together with its replacement acceptance and booking. Admin views report these quotes only as a separate count of provider-fault replacements. (REQ-014-131)
- **Acceptance grain**: FR-005's immutable AcceptanceEvent identifies the selected Subquote, its Quote Option and Option/Date-Price Record, inherited parent context, and accepted aggregate revision. Deduplicate redelivery of the same acceptance and count each accepted parent once. `acceptedSubquoteVersion = acceptedParentQuoteVersion`; neither a changed package preset nor an unselected alternative may replace the accepted snapshot. Historical acceptance measures patient selection and is retained after cancellation or payment-window expiry; it is not proof of a confirmed booking or captured revenue. (REQ-014-132)
- **Parent-quote acceptance rate**: Numerator = distinct parents in the selected first-submission cohort with an AcceptanceEvent by the reporting cutoff. Denominator = all distinct submitted parents in that same cohort, including unaccepted, expired, withdrawn, or later-cancelled parents. Use the parent's `first_sent_at` (set by FR-004 on first send; never changed by a re-send) to assign each parent to its cohort; do not divide acceptance events occurring in one period by unrelated submissions in another. This is a parent-level rate, not accepted subquotes divided by available subquotes. (REQ-014-133)
- **Inquiry response rate**: Denominator = distinct `(providerId, inquiryId)` distribution records first assigned to that provider within the selected distribution period. Numerator = those same pairs with at least one submitted parent response by the cutoff. Retries of distribution and multiple parent responses do not multiply either side. Missing authoritative distribution data yields an unavailable metric, not a proxy based on platform inquiries or quote volume. (REQ-014-134)
- **Inquiry funnel and booking conversion**: Use inquiry `created_at` to select the inquiry cohort. Provider views count distinct `(providerId, inquiryId)` pairs assigned to that provider; platform views count distinct Inquiry IDs across providers, not the sum of provider totals. Quoted means at least one parent was submitted; Accepted means an AcceptanceEvent exists for that inquiry and, in provider views, that provider; Confirmed booking means FR-006 recorded successful deposit or first installment confirmation. Each inquiry contributes at most once to each reached stage and cumulatively to preceding stages. Inquiries have no treatment (the provider chooses it in the parent quote), so treatment segments start at Quoted and use the parent/accepted booking's treatment; unquoted inquiries count only in all-treatments views. Deduplicate within each segment. Later cancellation does not erase a reached milestone; cancellation and no-show metrics remain separate. `In Progress` is a procedure-start milestone, never a synonym for payment confirmation. (REQ-014-135)
- **Reporting cutoff and empty denominators**: Historical funnel/acceptance/response cohorts are evaluated through the earlier of the selected period end and the pipeline's data-as-of time. Current cohorts show that cutoff and indicate that outcomes may still be pending. A zero denominator is N/A, not 0% or 100%. Tooltips/exports state the unit, cohort timestamp, numerator/denominator, cutoff, and relevant sample sizes; rates based on these distinct-record sets cannot exceed 100%. (REQ-014-136)
- **First response and journey**: TTFQ uses the same inquiry-created cohort and reporting cutoff as the funnel, which differs on purpose from the distribution-period cohort of the inquiry response rate; screens that show both (such as Screen 8) and exports MUST state each metric's cohort basis in the tooltip and export definition. TTFQ contributes one observation per inquiry/provider pair whose first parent response occurred by that cutoff, from the inquiry's distribution to that provider (`inquiry_providers.distributed_at`) to the `first_sent_at` of the provider's earliest parent quote for the inquiry; a re-send or new version never changes it. Pairs without an authoritative distribution timestamp have no TTFQ observation. Unanswered inquiries remain in funnel/response denominators but have no completed TTFQ observation. Provider distributions pool those observations; platform p50/p90 pool the underlying observations, not provider percentile averages. Journey time instead uses the successful initial payment that first confirms a booking, selects the confirmation-time cohort, and counts the inquiry once. Later installments or failed payment attempts do not create new journey observations. (REQ-014-137)
- **Accepted-price grain**: Count one immutable accepted total price per accepted parent, including the accepted package/date-price and promotion. Standalone price metrics use `AcceptanceEvent.acceptedAt` to select their cohort; Screen 5's scatter uses its expressly stated parent first-submission cohort. Unaccepted parents have a price range, not one amount, and remain excluded from all amount observations while included in parent volume/rate metrics. Cancellation, hold expiry, package-library edits, quote revisions, or later financial adjustments do not rewrite the historical acceptance-price observation. Show accepted selection counts and distinguish these statistics from captured revenue. (REQ-014-138)
- **Active cash risk**: At the displayed snapshot time, include only Accepted FR-006 pending bookings with a non-superseded AcceptanceEvent, valid exclusive slot hold, and no successful initial payment. Scope the time filter by acceptance time, calculate age from immutable `acceptedAt`, and validate the actual configured hold deadline. Remove cancelled, expired-hold, and `Payment Window Expired` selections even before stale quote status caches update; do not restart age on payment retries. Sum each eligible accepted total price once as potential accepted booking value, not deposit receivables, captured revenue, or outstanding installment balances. (REQ-014-139)
- **Financial record grain**: Payments, refunds, commission deductions, installments, and payouts retain their existing owning-record accounting rules. Aggregate those records before attaching read-only AcceptanceEvent/Booking/quote provenance; joining several packages or date options MUST NOT multiply financial totals. This change does not redefine fund release, fees, payout routing, or travel responsibility. (REQ-014-140)
- **Refund source of truth**: Refunds are counted only from refund rows (`payments.payment_type = 'refund'` with `payment_status = 'completed'`); refund amount, refund count, and Net GMV use these rows alone. An original payment whose `payment_status` later becomes `refunded` stays in gross income/GMV and captured payment counts (`payment_type ≠ 'refund'` and `payment_status IN ('completed', 'refunded')`) and is never counted as a second refund. This prevents a refund from being removed from gross figures and subtracted again. (REQ-014-141)
- **Shared benchmark rule**: All provider benchmark comparisons (Screen 2 Widget 7 and Screen 5 Widget 4) use one peer pool: active providers with ≥30 inquiries in the same rolling 12-month window, minimum 5 eligible providers per metric (price metrics additionally require accepted-price observations). Provider identities stay anonymised (Rule 13). Colour is direction-aware: for higher-is-better metrics (conversion, parent-quote acceptance, ratings) Green = at or better than median, Amber = up to 10% worse, Red = more than 10% worse; for TTFQ p50 lower is better, so worse means above median. Average accepted price is neutral: variance and percentile are shown without colour. Benchmarks refresh at the FR-026 benchmark refresh frequency. (REQ-014-142)

### Global Filter Rules

- **Rule 1**: Default time range on page load = **Last 4 weeks**, all countries (REQ-014-143)
- **Rule 2**: Each screen maintains its own filter state (changing filters on Screen 2 does not affect Screen 3) (REQ-014-144)
- **Rule 3**: Clicking a chart element opens the corresponding pre-filtered operational list in a new context (does not navigate away from the analytics screen). Exception: on Screen 1, a single click applies the cross-filter, and the same drill-down opens from the element's explicit "View list" action (REQ-014-145)
- **Rule 4**: All screens use skeleton loading states; no full-page blocking spinners (REQ-014-146)
- **Rule 5**: Localize all dates, currencies, and timezones to the user's configured locale (provider locale for provider screens; admin platform locale for admin screens) (REQ-014-147)
- **Rule 5A — Filter applicability**: A filter applies only to widgets whose source records carry that dimension. Inquiries carry no treatment (the provider chooses it in the FR-004 Parent Quote), so the Treatment filter applies from Quoted onward: quoted inquiries, parent quotes, acceptances, bookings, accepted prices, payments and refunds attributed through the accepted parent (Screen 4 Widget 2 attribution), reviews, and aftercare. Funnel and conversion widgets with a treatment selected follow the Screen 2 rule: the Inquiries stage shows "— (inquiries have no treatment)" and conversion is measured from Quoted. Widgets built on inquiries, patient registrations, provider counts, or payout statements are not filtered by a dimension their records lack; they keep rendering unfiltered data with a visible note such as "Not filtered by treatment". This covers: (REQ-014-148)
  - Screen 4: Widget 8 payout history is filtered by neither treatment nor patient country, because payout statements are per provider period (likewise Screen 1 C4 for the country filter)
  - Screen 9: Widgets 1 (inquiry volume), 3 (new vs. returning), and 5 (seasonality) are not treatment-filtered; Widget 2 measures from Quoted; Widgets 4 (journey time) and 6 (affiliate bookings) filter by the accepted parent's treatment
  - Screen 10: Widgets 1 (demand map), 2 (provider coverage), 3 (demand vs. supply gap), and 5 (emerging origins) are not treatment-filtered; Widget 4 measures conversion from Quoted

### Data Quality Rules

- **Rule 6**: Analytics pipeline updates every 15 minutes; non-blocking banner shown when data is >20 minutes stale (REQ-014-149)
- **Rule 7**: Low sample threshold = **<30 inquiries** for provider screens; helper copy shown but data still rendered (REQ-014-150)
- **Rule 8**: Minimum sample requirements per widget are specified in each screen spec; below minimum, widgets show "Not enough data yet" with the threshold stated (REQ-014-151)
- **Rule 9**: Benchmark pools require minimum 5 providers; if pool is insufficient, benchmark widgets show an explanatory message rather than blank state (REQ-014-152)
- **Rule 10**: All currency amounts converted using the daily FX rates (the Currency Exchange Rate record owned by FR-029: one fetched rate per pair per day) cached from the currency conversion API; rates locked at the transaction date for historical data. On API failure, fall back to the previous day's cached rate up to a maximum of **48 hours**; beyond 48 hours, affected widgets show "FX data unavailable" instead of rendering with stale rates (REQ-014-153)
  - Accepted-price observations preserve the FR-005 acceptance snapshot's original currency, total price, locked exchange rate, and acceptance time. If a different reporting currency needs an additional conversion, use a historical acceptance-date reporting rate and retain its provenance; do not replace the commercial locked rate with today's rate. Payment/payout records retain their own existing historical financial FX basis. Missing historical provenance yields an unavailable affected amount metric, not an inferred currency, current package price, or current FX value. (REQ-014-153)

### PII & Privacy Rules

- **Rule 11**: Patient identity is masked in all provider-facing analytics: where a patient row is shown, display the patient ID plus a partially masked name in the FR-003 format (for example HP102589-0001 · "Aylin K****"); full names and contact details are never shown (REQ-014-154)
- **Rule 12**: Patient identities are never exposed to affiliates (aggregates only) (REQ-014-155)
- **Rule 13**: Provider identities are anonymised in benchmark comparisons and platform-wide charts (providers cannot identify individual competitors) (REQ-014-156)
- **Rule 14**: Admin can see individual provider identities in admin screens for operational support (REQ-014-157)
- **Rule 15**: All analytics access logged with user ID, timestamp, screen accessed, and active filters to the S-06 Audit Log Service as an immutable, tamper-proof audit trail retained for 10 years (constitution §II, Data Retention & Deletion) (REQ-014-158)

### Access Control Rules

- **Rule 15A**: FR-014 consumes the existing role and permission model; it does not define new roles or expand access beyond the owning platform's permission system. (REQ-014-159)
- **Rule 15B**: If a user lacks permission to view a widget's underlying data domain, the UI MUST not render that widget for that user, and the corresponding widget data MUST not be requested. Remaining widgets reflow within the existing responsive layout. (REQ-014-160)
- **Rule 15F**: Default provider-role access to the provider analytics screens, using the FR-009 roles. The matrix states the default data-domain grants only; actual visibility is always resolved through Rules 15A and 15B, so a role whose permissions are changed sees whatever its granted data domains allow. Screens or sections a role cannot see are hidden from navigation, not shown as locked. (REQ-014-161)

| Screen | Owner | Manager | Billing Staff | Clinical Staff |
|---|---|---|---|---|
| Screen 1 Main Dashboard — Sections A and B (inbox and performance) | Full | Full | Hidden | Hidden |
| Screen 1 Main Dashboard — Section C (financials) | Full | Only with financial permission | Full | Hidden |
| Screen 2 Performance & Conversion | Full | Full | Hidden | Hidden |
| Screen 3 Patient Analytics | Full | Full | Hidden | Satisfaction and aftercare widgets only |
| Screen 4 Finance & Payouts | Full | Only with financial permission | Full | Hidden |
| Screen 5 Pricing & Benchmarks | Full | Full | Full | Hidden |
| Screen 6 Export Report Configuration | Full | Exports limited to the screens and widgets the user can see | Exports limited to the screens and widgets the user can see | Exports limited to the screens and widgets the user can see (Screen 3 exports contain only the satisfaction and aftercare widgets) |

### Accessibility Rules

Added by [CR-FR014-20261013-02](change-request-2026-10-13-export-history-accessibility.md) to meet the constitution's WCAG 2.1 Level AA requirement for web platforms.

- **Rule 15C**: Colour is never the only signal. Every Green/Amber/Red tier, benchmark variance, health badge, aging bucket, heatmap cell, and gap/outlier flag MUST also carry a text label or icon (for example ✓ On target, ▲ Watch, ✕ Off target, or the tier name), and chart series MUST be distinguishable by label, pattern, or marker shape as well as colour. (REQ-014-162)
- **Rule 15D**: Text, data labels, and status badges MUST meet WCAG 2.1 AA contrast (4.5:1 for normal text, 3:1 for large text and for chart marks and UI components against their background) in the platform default palette. (REQ-014-163)
- **Rule 15E**: Every chart MUST have a text alternative: an accessible name and summary, plus keyboard-reachable tooltips/drill-downs, or a data-table view of the same values. Heatmaps and maps fall back to their ranked-table equivalents for screen readers. (REQ-014-164)

### Admin Editability Rules

**Editable by Admin**:

Values are owned by the FR-026 Analytics Configuration Manager (Screen 5e); FR-014 reads the active version at calculation time. Recalculation rule: live dashboards and benchmarks always use the configuration version active when they are calculated, including for past periods shown on screen. After a change, the next calculation recolours and re-buckets every period in view (for example, last month's TTFQ tiers after an SLA change); past periods are not frozen at older values. Each aggregate records the configuration version used. PDF/CSV exports and scheduled-export files already generated are never rewritten; they keep the values and version from their generation time. (REQ-014-165)

- SLA target (minutes, default 120) — platform-wide value used across all TTFQ color coding and benchmark charts; per-provider SLA overrides are out of scope for this version
- Benchmark refresh frequency (default Weekly)
- Provider engagement status thresholds (Active/At Risk/Dormant day boundaries; defaults At Risk 7 days, Dormant 30 days)
- Outlier detection threshold for Screen 13 (default 30%)
- Target monthly commission reference line on Screen 12 Widget 2 (optional; unset by default, and the line is hidden until set)

**Fixed in Codebase**: (REQ-014-166)

- Dashboard section order (Screen 1: A → B → C)
- TTFQ formula and funnel stage definitions
- Booking Intensity Index formula
- Commission calculation logic: `IF provider_commissions.type = 'percentage' THEN payment.amount × (effective_rate / 100) ELSE effective_flat_amount once per completed procedure` — percentage applies per completed payment, flat rate applies once per FR-010 completed procedure (FR-015); the conditional is fixed; the type and rate/amount values come from each booking's confirmation-time commission snapshot (`snapshot_commission_percentage` / `snapshot_commission_amount`, FR-015 REQ-015-022, FR-029), never from the provider's current commission configuration

### Performance Rules

- **Rule 16**: All screens load within 3 seconds for 95th percentile (pre-aggregated metrics) (REQ-014-167)
- **Rule 17**: Chart rendering completes within 1 second for ranges ≤12 weeks (REQ-014-168)
- **Rule 18**: Export generation: PDF <60 seconds, CSV <30 seconds (REQ-014-169)
- **Rule 19**: System supports 1,000 concurrent provider analytics sessions without degradation (REQ-014-170)

### Integration & Ownership Rules

- **FR-003**: `distributed_at` is defined in FR-003 Key Entities as the per-provider distribution timestamp and is the TTFQ and response-rate start point. See FR-003 REQ-003-118 and REQ-003-062
- **FR-006**: Booking/AcceptanceEvent linkage, successful initial-payment confirmation, actual exclusive-hold deadline, Payment Window Expired outcome and audited admin revive to `Accepted` with a fresh hold, lifecycle, and appointment — feeds confirmed-booking funnels, journey time, active cash risk, booking intensity, and downstream treatment milestones. See FR-006 REQ-006-017, REQ-006-016, REQ-006-060 and REQ-006-005
- **FR-017**: Voided statements are excluded from every provider-facing payout view and export; admin views follow FR-017. See FR-017 REQ-017-068 and REQ-017-040
- **FR-031**: Access control and permissions — governs which admin analytics surfaces and data domains are visible to each authorized role. See FR-031 REQ-031-110 and REQ-031-064
- **S-03**: Notification Service — handles scheduled export email delivery and secure-link notifications for Screen 6 through the `analytics.export_ready` event defined in FR-030 (REQ-030-105) and mirrored in FR-020
- **S-05**: Media Storage Service — stores generated export artifacts for 7-day re-download retention and secure-link access. See FR-002 REQ-002-024
- **Provider Banking Details**: Provider display currency is derived from `banking_details.currency` via provider default-currency resolution; if absent, the current implementation falls back to USD. See FR-004 REQ-004-025, REQ-004-084 and REQ-004-086, and FR-029 REQ-029-044 (locked exchange rate)
  - This is reporting-currency resolution only; it MUST NOT overwrite FR-004 system-configured quote currency or the immutable FR-005 accepted currency/locked rate. Reconcile any legacy fallback against the accepted snapshot before presenting historical amount metrics. (REQ-014-171)
- **Provider Team / Auth Data**: Engagement views rely on `provider_activity_logs.action_at` as the canonical activity timestamp source (documented in system-data-schema.md). Last active = `MAX(action_at)` per provider. The previously referenced `provider_users.last_login_at` field does not exist in the schema and must not be used. (REQ-014-172)
- **Assumption 2**: Admin analytics must remain responsive across desktop, tablet, and mobile viewports in accordance with the platform constitution; lower-width layouts may reduce density but must preserve the core workflows (REQ-014-175)
- **Assumption 3**: Provider analytics screens are desktop-first (≥1024px), responsive single-column on ≤1024px (REQ-014-176)
- **Assumption 5**: There is no per-clinic payout frequency. Payout cadence, wherever shown in this FR, means how the payout is released: automatic release on the Stripe Connect rail, or on the manual rail the single settlement-period setting owned by FR-029 (default weekly, Sunday cutoff, Wednesday payout) that applies to all manually paid clinics (REQ-014-177)
- **Assumption 10**: Country widgets (Screens 3, 10) flag rows resolved via legacy `patients.location` fallback with a subtle UI indicator (tooltip or badge) until the `patients.location_id` backfill is complete, so users can distinguish canonical vs. transitional data. (REQ-014-178)
- **Caching**: Aggregate reads are cached per provider and filter combination and invalidated when the next aggregation cycle completes or the FR-026 configuration version changes. Benchmark peer statistics are cached for the configured benchmark refresh frequency. Caches never hold data across provider tenants. (REQ-014-179)
- **Security and audit logging**: Every analytics request is scoped server-side to the caller's provider tenant and permitted data domains (Rules 15A, 15B and 15F); the client never filters restricted data. Access is logged per Rule 15. Export artifacts are stored in S-05 with secure links that expire after 48 hours, and benchmark outputs only expose anonymised peer statistics above the minimum peer count. (REQ-014-180)

### Analytics Data Contract and Legacy Compatibility

The revised analytics entities below are target reporting contracts, not evidence that corresponding tables, API payloads, or materialized aggregates have been migrated. Implementation reconciliation must map the approved FR-004/FR-005/FR-006 owners to each metric before replacing existing aggregates. (REQ-014-173)

| Contract input | Where used | Canonical boundary / legacy constraint |
|----------------|------------|----------------------------------------|
| Parent Quote first-submission `first_sent_at` | Response volume, TTFQ, acceptance-rate cohorts, provider ramp | One immutable first send per stable parent identity, set by FR-004 on first send and never changed by a re-send or new version; legacy `quotes.sent_at` is never used as a fallback for these metrics |
| AcceptanceEvent acceptedAt + accepted snapshot | Acceptance milestones, accepted prices, aging origin | FR-005 event is authoritative; legacy `quotes.accepted_at` alone cannot identify the chosen package/date price or establish an active hold |
| Parent/subquote IDs and accepted aggregate versions; Quote Option/Option-Date-Price IDs | Drill-downs, accepted-price observations, detailed exports | Resolve the exact accepted version and inherited context; require equal parent/subquote aggregate versions |
| Booking linkage, confirmation event, hold deadline, and lifecycle | Confirmed funnels, patient journey, pending-payment aging | FR-006 distinguishes Accepted, Confirmed, In Progress, Payment Window Expired, and Cancelled; flat quote status is insufficient |
| Original accepted total price/currency and locked FX provenance | Accepted-price aggregates, comparisons, exports | Preserve immutable acceptance value; any additional historical reporting conversion follows Rule 10 |
| Owning payment/refund/commission/payout records | Financial aggregates | Deduplicate before quote-hierarchy joins; selected price is not a substitute for captured transaction amounts |

Do not backfill an accepted amount by choosing a current alternative or consulting today's package library. If historical accepted-selection or cohort provenance cannot be recovered faithfully, show unavailable data for the affected metric and record the gap for implementation reconciliation. System-wide schema/spec updates and implementation migration are outside this FR-014 documentation change. (REQ-014-174)

### Aggregate and Entity Rules

- **Entity 1 — Analytics Metrics Aggregate**: Inquiry-stage counts MUST NOT be populated with quote/option counts; retain the source observations or equivalent mergeable data needed for longer-range distinct counts and percentiles rather than summing daily percentiles.
- **Entity 3 — Accepted Selection Aging Snapshot**: One row per active pending booking; deadline/status checks prevent a stale Accepted quote from remaining in cash risk after hold expiry.
- **Entity 6 — Benchmark Segment**: Accepted-price benchmarks require actual accepted-price samples; unaccepted parents are not zero values.
- **Entity 7 — Payout Record**: `amount` is the net payout the clinic receives after commission, not the gross booking value.
- **Entity 8 — Export Report Configuration**: Generated reports additionally retain the metric definitions/cohorts, reporting cutoff/data-as-of, sample sizes, currency/FX provenance, and authorized accepted-selection IDs/versions for detailed rows. Configuration and scheduling do not change screen metric semantics.

### Task-Time Limits

- **SC-001**: Provider can identify TTFQ health status (Green/Amber/Red) within 3 seconds of opening Screen 1
- **SC-002**: Provider can answer "What is my conversion rate for FUE this month?" from Screen 2 in under 30 seconds
- **SC-003**: Provider can identify their top patient origin country from Screen 3 in under 20 seconds
- **SC-004**: Provider can verify their upcoming payout amount from Screen 4 in under 20 seconds
- **SC-005**: Provider understands their percentile position on at least 2 metrics from Screen 5 in under 1 minute
- **SC-006**: Admin can identify all Red-tier providers from Screen 8 in under 30 seconds
- **SC-007**: Admin can identify the top 3 countries with demand/supply gaps from Screen 10 in under 1 minute
- **SC-008**: Admin can verify total upcoming payout obligations from Screen 12 in under 30 seconds
- **SC-009**: Admin can identify pricing outlier providers for a given treatment from Screen 13 in under 2 minutes
- **FR-004**: Parent Quote identities, provider/inquiry/treatment context, first submission, aggregate versions, and Quote Option/Option-Date-Price hierarchy — feeds parent response volume, TTFQ, and first-submission cohorts; unaccepted price ranges are not amount observations. See FR-004 REQ-004-030, which also carries the parent response grain and unaccepted-parent counting rules formerly restated in FR-014.
- **FR-005**: AcceptanceEvent and immutable accepted Subquote snapshot, including parent/option/date-price/subquote IDs, equal accepted aggregate versions, acceptedAt, accepted total price/promotion/currency, locked exchange rate, appointment, and cancellation/supersession provenance — feeds patient selection, parent acceptance rate, and accepted-price statistics. See FR-005 REQ-005-017 through REQ-005-020; REQ-005-020 also carries the parent-versus-subquote counting boundary formerly restated in FR-014.
- **FR-013**: Reviews (`overall_rating`, `results_rating`, `staff_rating`, `facility_rating`, `value_rating`) — feeds satisfaction widgets. The per-treatment sub-scores endpoint (REQ-013-023) is per provider, so Screen 11 Widget 4 requires a single-provider filter
- **FR-015**: Provider master/profile data — provider location and timezone (`providers.country_id`, `providers.city_id`, `providers.timezone`) drive localization; payout timing follows FR-017 and the single FR-029 settlement period (see Assumption 5). Commission analytics use the booking confirmation-time commission snapshot (REQ-015-022), not current `provider_commissions` values
- **Assumption 6**: Patient-country analytics resolve from `patients.location_id` referencing `countries.id`; during transition, legacy rows may still fall back to `patients.location` for display/grouping compatibility until data cleanup is complete
- **Pipeline and pre-aggregation**: Metrics are computed by a scheduled aggregation job on a 15-minute cycle (SC-010) into the provider-level and platform-level aggregates (Key Entities 1 and 4), each stamped with its reporting cutoff and FR-026 configuration version. Screens read aggregates, not live transactional tables, so the 3-second load target (Rule 16) does not depend on raw query volume. Late-arriving source events (refunds, closures, re-generated payout statements) are picked up on the next cycle and recalculate the affected periods.

---

## Dependencies

Related FRs: FR-003 (inquiry data and inquiry distribution records), FR-004 (Parent Quote identities and first submission), FR-005 (AcceptanceEvent and accepted Subquote snapshot; REQ-005-017 through REQ-005-020), FR-006 (Booking/AcceptanceEvent linkage and hold deadline), FR-007 (payment data; REQ-007-006, REQ-007-016, REQ-007-023), FR-007B (installment plan records and Plan Status; REQ-007B-033, REQ-007B-019, REQ-007B-095), FR-009 (provider team roles and permissions; REQ-009-002, REQ-009-011, REQ-009-163), FR-010 (treatment execution status and case closure reason; REQ-010-079, REQ-010-006, REQ-010-033, REQ-010-076), FR-011 (aftercare records; REQ-011-017, REQ-011-001, REQ-011-016), FR-013 (reviews), FR-015 (provider master/profile data), FR-016 (patient records; REQ-016-002, REQ-016-038 and FR-001 REQ-001-010), FR-017 (payout records), FR-018 (affiliate records; REQ-018-051, REQ-018-013), FR-026 (Analytics Configuration Manager; REQ-026-038), FR-029 (A-09 Currency Management; REQ-029-085, REQ-029-056, REQ-029-058), FR-031 (access control and permissions). System services: S-03 (Notification Service), S-05 (Media Storage Service).

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
| Inquiry is created at 09:00, released from an exclusive provider at 13:00, and first distributed to Provider B then; Provider B submits a parent quote at 14:00 | Provider B's TTFQ observation is 60 minutes (from distribution), not 300 minutes; no SLA-breach alert fires for Provider B under the default 120-minute target, and the TTFQ tier and alert agree |
| Payment/acceptance event is redelivered or financial record joins multiple options | Accepted choice and pending aging row remain single observations; payment/refund/commission/payout totals count each owning record once. Detailed exports identify the accepted IDs and equal aggregate versions |
| Price-bracket widget and pricing outlier eligibility | Brackets show accepted counts/shares, not a conversion percentage based only on accepted rows. Outlier eligibility requires five accepted selections, not five unaccepted parents; scatter requires three treatments with both coordinates and makes no causal claim |

## Functional Requirements Summary

### Screen 1 — Main Dashboard (LOCKED)

- **REQ-014-001**: Screen 1 layout, sections, widget count, chart types, filters, and responsive behavior remain locked. Its TTFQ, four-stage Confirmed-booking funnel, and active accepted-but-unpaid aging MUST use the current Screen 1 definitions and shared analytics rules under the approved CR-FR014-20261007-01 metric-only exception; the v2.0 formulas are superseded where explicitly revised.
- **REQ-014-002**: System MUST offer a time range filter in the Screen 1 header with options Today, This week, Last 4 weeks, Last 12 weeks and Custom, defaulting to Last 4 weeks
- **REQ-014-003**: System MUST offer a multi-select Country filter in the Screen 1 header, defaulting to all countries
- **REQ-014-004**: System MUST apply a single click on any Screen 1 widget element as a cross-filter on all sections
- **REQ-014-005**: System MUST open the operational list behind a Screen 1 element in a new context only from an explicit "View list" action in the element's tooltip or keyboard focus menu
- **REQ-014-006**: System MUST show in each Screen 1 tooltip the metric definition, numerator and denominator, and time basis, and MUST localize dates, currencies and timezone
- **REQ-014-007**: System MUST show skeletons while Screen 1 loads, helper copy with counts still rendered below 30 inquiries, non-blocking error banners with retry, and masked patient names throughout
- **REQ-014-008**: System MUST display Tile 1 (New Inquiries) as Today and This week counts, opening the Inquiries list with the time filter applied
- **REQ-014-009**: System MUST display Tile 2 (TTFQ) as p50 and p90 against the SLA in a compact dual bullet, coloured Green, Amber or Red by the Tile 2 thresholds, opening the Inquiries list grouped by coordinator
- **REQ-014-010**: System MUST measure TTFQ per the Tile 2 formula, from the inquiry's distribution to the provider to the first send of the provider's earliest parent quote, excluding auto-acknowledgements
- **REQ-014-011**: System MUST display the Inquiry Queue with columns Received (relative time and SLA countdown), Patient (ID-masked), Age, Problem, Country and Actions (View link)
- **REQ-014-012**: System MUST mark Inquiry Queue rows with the `New` badge until the provider submits a parent quote, sort `New` rows first then by received time ascending, and show 10 rows per page
- **REQ-014-013**: System MUST display B1 as a funnel (Inquiries, Quoted, Accepted, Confirmed booking) with count and step percentage per stage and overall booking conversion as footer
- **REQ-014-014**: System MUST count B1 as distinct inquiry/provider pairs in one inquiry cohort, cumulative through each reached stage, with Confirmed booking meaning a successful deposit or first installment confirms the FR-006 Booking; clicking a stage opens the filtered Inquiries list
- **REQ-014-015**: System MUST display B2 as a bullet chart of p50 and p90 with the SLA as target marker, coloured by the Tile 2 thresholds, opening the Inquiries list grouped by coordinator
- **REQ-014-016**: System MUST display B3 as a 6-row by 7-column Monday-to-Sunday calendar heatmap for the next 6 weeks, coloured by the Intensity Index (bookings on the day divided by that month's daily average, times 100)
- **REQ-014-017**: System MUST count B3 bookings only per REQ-014-116 (Confirmed and In Progress by appointment date)
- **REQ-014-018**: System MUST colour B3 cells Cool (50% or less), Below avg (50 to 90%), Neutral (90 to 110%), Above avg (110 to 150%) or Hot (over 150%), show the Confirmed bookings, monthly average and index in the cell tooltip, and open the Schedule day view on click
- **REQ-014-019**: System MUST choose the B3 baseline in the order 12-month same-month average, current month to date, rolling 90 days, and clamp the colour index to 0 to 300% while showing the actual value in the tooltip
- **REQ-014-020**: System MUST display B4 as a donut of the top 8 countries by inquiry share plus Other, with total inquiries in the centre and `CC (ISO-2) • %` slice labels
- **REQ-014-021**: System MUST style B4 slice borders by confirmed booking rate (thin/neutral under 20%, medium/amber 20 to 40%, thick/green over 40%) and show country, inquiries, Confirmed bookings and Confirmed booking rate in the tooltip
- **REQ-014-022**: System MUST compute B4 Confirmed bookings and rate from the inquiry cohort and Confirmed booking stage in Analytics Counting & Time Basis, and open the filtered Inquiries list on slice click
- **REQ-014-023**: System MUST display C1 as a weekly area line chart of income only in the provider currency, opening the Earnings report for the clicked week
- **REQ-014-024**: System MUST display C2 as a Pareto bar chart of income by treatment (top N plus Other, with cumulative percentage line), attributing treatment as Screen 4 Widget 2 does, opening the Cases list filtered by treatment
- **REQ-014-025**: System MUST display C3 as a stacked horizontal bar of accepted selections awaiting initial payment in the buckets 0-24h, 1-3d, 4-7d, 8-14d and over 14d, with an optional legend by treatment (top 3) or country
- **REQ-014-026**: System MUST compute C3 age from the immutable acceptance time and count only pending bookings with a valid exclusive payment-window hold, excluding cancelled selections, superseded acceptance events, expired holds and Payment Window Expired bookings
- **REQ-014-027**: System MUST open from a C3 bucket the Accepted Quotes list resolved to the exact accepted subquote and pending booking, using the actual configured hold deadline
- **REQ-014-028**: System MUST display C4 as a monthly column chart (last 6 to 12 months) with an inline table of 2 to 3 rows and columns Type, Period, Amount, Scheduled Date and Cadence
- **REQ-014-029**: System MUST set the C4 Type to the provider display status from the Screen 4 Widget 8 FR-017 mapping (Upcoming, Processing, Paid, Failed; Voided never shown), listing the next Upcoming payout, any Processing or Failed payout, then the most recent Paid payout, up to 3 rows
- **REQ-014-030**: System MUST show in C4 the FR-017 scheduled payout date (the paid date for Paid rows) and open the Payout statements list (CSV/PDF export) on bar click
- **REQ-014-031**: System MUST present Screen 1 as one scrollable page without tabs, ordered header filters, Section A (Inbox), Section B (Performance), Section C (Financials)
- **REQ-014-032**: System MUST collapse Screen 1 to a single column at 1024px width and below

### Screen 2 — Performance & Conversion

- **REQ-014-033**: System MUST display cumulative distinct-inquiry funnel conversion trend ending in Confirmed booking as a multi-line chart with weekly/monthly toggle
- **REQ-014-034**: System MUST display conversion breakdown by treatment type as a grouped bar chart
- **REQ-014-035**: System MUST display conversion breakdown by patient country as a ranked horizontal bar
- **REQ-014-036**: System MUST display parent-quote acceptance rate trend using accepted parents and submitted parents from the same first-submission cohort
- **REQ-014-037**: System MUST display TTFQ p50 and p90 trend, measured from the inquiry's distribution to the provider to the `first_sent_at` of the provider's earliest parent quote for the inquiry per inquiry/provider pair (never changed by a re-send or new version), with SLA reference line
- **REQ-014-038**: System MUST display cancellation and no-show rate KPI tiles with sparklines
- **REQ-014-039**: System MUST display an anonymised platform benchmark comparison table (TTFQ, booking conversion, parent-quote acceptance rate, avg rating) with percentile bands and the same per-metric counting definitions for provider and peer values
- **REQ-014-040**: Benchmark pool MUST require minimum 5 providers; display explanatory message if pool is insufficient

### Screen 3 — Patient Analytics

- **REQ-014-041**: System MUST display full patient location table (all countries, sortable) and linked donut chart
- **REQ-014-042**: System MUST display new vs. returning patient rate as donut and monthly trend line
- **REQ-014-043**: System MUST display patient journey time (p50 and p90 days inquiry → first successful booking-confirming payment) with distribution histogram, without failed-attempt or later-installment duplication
- **REQ-014-044**: System MUST display review sub-scores (overall, results, staff, facility, value) per treatment type
- **REQ-014-045**: System MUST display treatment preference distribution (quoted inquiry count vs. Confirmed booking count per treatment, by the parent quote's treatment)
- **REQ-014-046**: System MUST display aftercare activation rate KPI with trend sparkline
- **REQ-014-047**: *Removed in v3.11.* No patient age distribution widget is included in this version; the ID is kept so later numbering stays stable

### Screen 4 — Finance & Payouts

- **REQ-014-048**: System MUST display revenue trend with weekly/monthly/quarterly toggle
- **REQ-014-049**: System MUST display revenue by treatment type — full list (not capped at 8)
- **REQ-014-050**: System MUST display revenue by patient country
- **REQ-014-051**: System MUST display commission deducted and net income (gross income minus commission deducted) per period using each booking's confirmation-time commission snapshot: percentage per completed payment in range; flat rate once per procedure completed in range (FR-015 REQ-015-022)
- **REQ-014-052**: System MUST display refund volume and refund rate trend
- **REQ-014-053**: System MUST display installment vs. full payment split and a monthly installment adoption rate (bookings first confirmed in the month with an FR-007B installment plan divided by all bookings first confirmed in the month)
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
- **REQ-014-062**: System MUST support scheduled recurring exports (weekly/monthly/quarterly) covering the previous full period in the provider's timezone, with recipient limits, retry, and edit/pause/resume/delete as defined on Screen 6
- **REQ-014-063**: System MUST store generated reports for 7 days for re-download

### Screen 7 — Platform Overview

- **REQ-014-064**: System MUST display three-section overview (Operations, Performance, Finance) with platform-wide aggregations
- **REQ-014-065**: System MUST display provider TTFQ health distribution donut (Green/Amber/Red counts)
- **REQ-014-066**: System MUST display provider engagement rate, activity-based Dormant provider count, and separately labelled Non-responding provider count (0 first-submitted parent quotes within the Dormant threshold window)
- **REQ-014-067**: System MUST display a cumulative distinct-platform-inquiry Confirmed-booking funnel and TTFQ bullet chart computed from underlying inquiry/provider first-response observations, not summed provider funnels or averaged provider percentiles
- **REQ-014-068**: System MUST display platform GMV, commission earned, upcoming payout obligations, and cash-at-risk as financial summary tiles

### Screen 8 — Provider Performance & Engagement

- **REQ-014-069**: System MUST display provider league table (sortable by TTFQ, booking conversion, parent-quote acceptance rate, rating, distinct-inquiry response rate) with platform variance column
- **REQ-014-070**: System MUST display provider performance scatter plot (TTFQ vs. conversion rate, one point per provider)
- **REQ-014-071**: System MUST display provider activity table with last active date, distinct first-submitted parent quote count, distinct-inquiry response rate, and engagement status (Active/At Risk/Dormant)
- **REQ-014-072**: System MUST display new provider ramp chart (distinct parent first submissions vs. days since onboarding), not draft/option creation or version counts
- **REQ-014-073**: Engagement status thresholds MUST be admin-configurable
- **REQ-014-312**: System MUST display provider team size and role distribution across the platform (Screen 8 Widget 6), so admins can see how large each clinic team is and how team members are spread across the clinic roles

### Screen 9 — Patient Acquisition & Funnel

- **REQ-014-074**: System MUST display inquiry volume trend (area line with prior period overlay)
- **REQ-014-075**: System MUST display cumulative distinct-platform-inquiry funnel trend ending in Confirmed booking as a multi-line monthly chart
- **REQ-014-076**: System MUST display new vs. returning patient rate as stacked monthly bar + KPI tiles
- **REQ-014-077**: System MUST display platform patient journey time distribution (p50, p90, histogram) using one first successful booking-confirming payment per inquiry
- **REQ-014-078**: System MUST display inquiry seasonality month × weekday heatmap (rolling 12-month view; index = weekday average ÷ month daily average × 100)
- **REQ-014-079**: System MUST display affiliate acquisition KPI tiles and ranked table; display limitation note that tracking begins when the affiliate code or referral link is captured in the booking journey, not at the inquiry stage; attribution follows FR-018 Rule 11 even when another discount set the final price

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
- **REQ-014-088**: System MUST display average review sub-scores per treatment type (5 sub-scores) only when a single provider is selected; with no provider selected, show a prompt to select one
- **REQ-014-089**: System MUST display aftercare activation rate per treatment type
- **REQ-014-286**: System MUST display provider distribution by treatment specialisation as a stacked horizontal bar chart (Screen 11 Widget 6): provider count per treatment, where a provider offers a treatment if it first-submitted at least one parent quote for it in the last 12 months
- **REQ-014-090**: System MUST NOT include any clinical outcome metrics (graft survival, hair density, complication rates) — these are not in the database

### Screen 12 — Financial Health & Cashflow

- **REQ-014-091**: System MUST display platform GMV (gross) and accrual-based net revenue (commission earned) as dual-line area chart (monthly), with refunds and Net GMV in the tooltip
- **REQ-014-092**: System MUST display commission earned trend with admin-configurable target reference line
- **REQ-014-093**: System MUST display refund volume/rate and failed payment rate as KPI tiles and monthly trend
- **REQ-014-094**: System MUST display active pending-initial-payment cash-at-risk aging from immutable AcceptanceEvent.acceptedAt (stacked horizontal bar, same buckets and exclusions as Screen 1 C3, platform-wide)
- **REQ-014-095**: System MUST display upcoming provider payout obligations table (amount, provider, date, cadence as defined in Assumption 5)
- **REQ-014-096**: System MUST display installment plan health donut using FR-007B Plan Status labels (Active / Canceled / Completed / Defaulted); Overdue is a flag on a plan, not a status segment
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

- **REQ-014-105**: Merged into FR-005 REQ-005-020 (parent quote and subquote analytics stay distinct; each submitted Parent Quote counts once). FR-014 applies it on every screen and export; see Analytics Counting & Time Basis.
- **REQ-014-106**: System MUST resolve every accepted amount and selection drill-down to the immutable FR-005 AcceptanceEvent and exact accepted parent/subquote aggregate version, with equal parent and subquote versions.
- **REQ-014-107**: System MUST calculate parent acceptance, inquiry response, and inquiry funnel rates from their specified distinct-record cohorts and cutoff, returning N/A for zero denominators and an unavailable response metric for missing distribution provenance.
- **REQ-014-108**: Merged into FR-004 REQ-004-030 (unaccepted parents are excluded from amount metrics and still counted once in volume and conversion metrics). The rule that accepted historical prices are never overwritten moves to REQ-014-111.
- **REQ-014-109**: System MUST distinguish Accepted, payment-confirmed Booking, procedure In Progress, and Payment Window Expired; active cash risk MUST validate the actual hold deadline and exclude cancelled, expired, and superseded selections.
- **REQ-014-110**: System MUST aggregate financial records at their owning grain before quote-hierarchy joins, preventing duplicate payments, refunds, deductions, or payouts from repeated events or multiple alternatives.
- **REQ-014-111**: System MUST preserve accepted price/currency/locked-rate provenance and historical reporting-conversion provenance; accepted historical prices MUST NOT be overwritten by library changes, cancellation, hold expiry, or later financial adjustments; missing canonical history MUST NOT be filled with an invented alternative price or today's package/FX value.
- **REQ-014-112**: System MUST apply the same revised contracts to provider/admin screens, benchmarks, drill-downs, cached aggregates, PDF/CSV, and scheduled exports without expanding existing permissions or redesigning the locked cockpit.
- **REQ-014-113**: System MUST send the in-app TTFQ SLA-breach alert (`inquiry.ttfq_sla_breached`) once per distributed inquiry/provider pair when no parent quote is submitted within the FR-026 SLA target, suppressed for cancelled or withdrawn distributions and never repeated for the same pair
- **REQ-014-116**: System MUST count booking load and country booking figures (Screen 1 B3 and B4, Screen 3 Widget 1, Screen 10 Widget 1) from FR-006 Bookings in `Confirmed` or `In Progress` status only, label them "Confirmed bookings", and never count held (`Accepted`), `Payment Window Expired` or `Cancelled` bookings or show a separate held figure.
- **REQ-014-117**: System MUST exclude admin-authored replacement quotes (`authorType = admin`) and their replacement acceptances and bookings from provider quote counts, parent-quote acceptance rates, inquiry response rates, booking conversion, the inquiry funnel, and TTFQ on every provider and admin screen and export, and MUST report them to admins only as a separate count of provider-fault replacements per provider at fault (Screen 8 Widget 1).

### Report History & Accessibility (CR-FR014-20261013-02)

- **REQ-014-114**: System MUST provide a Report History & Recurring Exports area on Screen 6 listing reports generated in the last 7 days (download, retry failed) and all recurring configurations (edit, pause, resume, delete), as specified on Screen 6
- **REQ-014-115**: All provider and admin analytics screens MUST meet WCAG 2.1 Level AA per Accessibility Rules 15C–15E: no colour-only status signals, AA contrast for text and chart marks, and a text or table alternative for every chart

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-11-22 | 3.20 | Requirements graph programme baseline: PRD compressed to the checklist structure (each rule stated once, field rows tagged with graph field ids, dropped classes removed). No rule changes. Earlier history (v1.0 to v3.19) and the change requests (CR-FR014-20261007-01, file change-request-2026-10-07-parent-quote-subquote-analytics.md; CR-FR014-20261013-02, file change-request-2026-10-13-export-history-accessibility.md; CR-FR014-20261016-01, file change-request-2026-10-16-mtg002-quote-model-alignment.md) are in `archived/prd-baseline-2026-11-08/` and in git history. | Product Owner / Documentation |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner — documentation delta v3.18 | Joachim Trung Tuan | 2026-10-18 | ✅ Approved via MTG-002 decision log (documentation only): final audit corrections (CR-FR014-20261016-01) |
| Product Owner — prior baseline v3.6 | Joachim Trung Tuan | 2026-04-18 | ✅ Approved (historical baseline; approver name corrected 2026-10-13) |
| Product Owner — documentation delta v3.15 to v3.17 | Joachim Trung Tuan | 2026-10-16 | ✅ Approved: MTG-002 quote-model alignment via the 2026-10-16 decision log (CR-FR014-20261016-01); v3.17 consolidated verification correction on 2026-10-18 applies decision Q15. Implementation reconciliation required; not an implementation sign-off |
| Product Owner — documentation delta v3.14 | Joachim Trung Tuan | 2026-10-14 | ✅ Approved: sixth verify-fr pass resolutions (Issue 1 option 1 global filter rule, Issue 2 option 1 define rating source, Issue 3 align wording, Issue 4 define both). Not an implementation sign-off |
| Product Owner — documentation delta v3.13 | Joachim Trung Tuan | 2026-10-14 | ✅ Approved: fifth verify-fr pass resolutions (Issue 1 revised: treatment comes only from the provider's parent quote; Issue 2 option 1; Issue 3 option 1 with small clinics pooled and low-sample visuals left to UX; Issue 4 fix Screen 4 wording). Not an implementation sign-off |
| Product Owner — documentation delta v3.12 | Joachim Trung Tuan | 2026-10-14 | ✅ Approved: fourth verify-fr pass resolutions (Issue 1 option C, Issues 2–6 option A, Issue 7 add dependencies, Issue 8 reword Rule 11, Issue 9 align dates). Not an implementation sign-off |
| Product Owner — documentation delta v3.11 | Joachim Trung Tuan | 2026-10-13 | ✅ Approved: third verify-fr pass resolutions (11 decisions, including the provider-filter option for Screen 11 Widget 4); edits applied 2026-10-14. Not an implementation sign-off |
| Product Owner — documentation delta v3.10 | Joachim Trung Tuan | 2026-10-13 | ✅ Approved: second verify-fr pass resolutions (Issue 1 option 3, Issue 2 option 1, Issue 3 option 1, provider-scoped returning patients, FR-007B labels, global accessibility rule, Issues 7–10 recommended options) and CR-FR014-20261013-02. Not an implementation sign-off |
| Product Owner — documentation delta v3.9 | Joachim Trung Tuan | 2026-10-13 | ✅ Approved: verify-fr medium/minor resolutions (Issues 5–15, option 1 each). Not an implementation sign-off |
| Product Owner — documentation delta v3.8 | Joachim Trung Tuan | 2026-10-13 | ✅ Approved: verify-fr resolution choices (flat-rate per procedure, Qualified stage removed, FR-010 No-show source, FR-026 analytics settings owner). Not an implementation sign-off |
| Product Owner — documentation delta v3.7 | Joachim Trung Tuan | 2026-10-07 | ✅ Approved: "Please update as per your suggestions"; includes accepted-price distribution and metric-only Screen 1 exception. Not an implementation sign-off |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B
**Last Updated**: 2026-11-22
