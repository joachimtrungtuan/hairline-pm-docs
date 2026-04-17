# FR-014 Provider Analytics & Reporting — 12-Screen Expansion

**Date**: 2026-04-16
**Type**: Major Update
**Document Updated**: `local-docs/project-requirements/functional-requirements/fr014-provider-analytics-reporting/prd.md`
**PRD Version**: 2.0 → 3.0

---

## Summary

The FR-014 PRD has been expanded from a single-screen provider cockpit to a full 13-screen analytics suite covering both the Provider and Admin tenants. The expansion was driven by the need to avoid cramping multiple analytical jobs into single screens and to ensure each screen has a clear, single purpose. All widget data was verified against `system-data-schema.md` before being included.

**Screen 1 (Provider Main Dashboard) remains LOCKED** — the v2.0 design lock is preserved; this change adds new screens only.

---

## What Changed

### Screen Count

| Before (v2.0) | After (v3.0) |
|---------------|--------------|
| 3 screens (Main Dashboard, Financial Reports deep-dive, Export Config) | 13 screens (5 Provider + 7 Admin + 1 Export Config) |
| Provider-only scope | Provider + Admin tenant coverage |
| ~32 functional requirements | 104 functional requirements (REQ-014-001 through REQ-014-104) |

---

### New Provider Screens (Screens 2–5)

#### Screen 2 — Performance & Conversion Deep-Dive
- Full conversion funnel with stage-by-stage drop-off rates and time-in-stage medians
- Response time distribution histogram (bucket breakdown across all inquiries)
- Qualified inquiry rate trend (weekly, last 12 weeks)
- Quote acceptance rate trend (weekly, last 12 weeks)
- Lost inquiry reasons breakdown (Donut chart — expired, declined, no response, withdrew)
- Inquiry volume trend (daily/weekly, stacked by status)
- Widgets source: `inquiries`, `quotes`, `payments` tables + quote timeline activity

#### Screen 3 — Patient Analytics
- New patient vs. returning patient ratio (Donut chart)
- Patient country breakdown (Ranked bar chart — inquiry volume by country)
- Patient age distribution (Histogram — 5-year age brackets)
- Repeat inquiry rate trend (monthly, last 12 months)
- Lead source breakdown (Donut — direct/search/referral/affiliate) — **booking-level only**; inquiry-level source not in schema
- Top patient questions/problems (Ranked list — top 10 by volume)
- Widgets source: `patients`, `inquiries`, `payments`, `bookings_with_affiliate_code` tables

#### Screen 4 — Finance & Payouts Deep-Dive
- Monthly revenue breakdown table (treatment-level detail, sortable)
- Commission deduction breakdown (calculated: `payment.amount × (quotes.commission / 100)`)
- Installment plan tracker (total owed, paid, outstanding per booking)
- Payout history table (full history, paginated, exportable)
- Currency exposure (gross revenue by currency, FX rate applied)
- Refund & cancellation impact (cancelled/refunded payment totals by month)
- Widgets source: `payments`, `quotes`, `bookings_with_affiliate_code`, `treatment_packages` tables

#### Screen 5 — Pricing & Benchmarks
- Own quote amount distribution (Box plot by treatment — min/p25/median/p75/max)
- Treatment price vs. conversion rate scatter (each treatment as a data point)
- Platform benchmark comparison (own p50 vs. platform p50 per treatment) — anonymised, ≥5 providers in pool, weekly refresh
- Price trend over time (line chart — median quoted price per treatment, monthly)
- Widgets source: `quotes`, `treatments`, `treatment_packages`, aggregated platform benchmarks

---

### New Admin Screens (Screens 6–12)

#### Screen 6 — Platform Overview (Admin)
- Total inquiries, active providers, active patients (KPI tiles — today + delta vs. prior period)
- Platform-wide inquiry volume trend (daily/weekly)
- New provider registrations trend (monthly)
- New patient registrations trend (monthly)
- Platform conversion funnel (aggregate across all providers — same 5 stages as provider funnel)
- Widgets source: `inquiries`, `providers`, `patients`, `quotes`, `payments` tables

#### Screen 7 — Provider Performance & Engagement
- Provider engagement status breakdown (Active / At Risk / Dormant — Donut chart)
  - Active: activity within last 7 days; At Risk: 7–30 days; Dormant: >30 days
- Per-provider TTFQ ranking table (sortable, filterable by country/treatment)
- Per-provider quote acceptance rate ranking table
- Provider response time distribution (stacked bar — all providers bucketed)
- Provider conversion rate ranking (Pareto-style bar chart)
- Widgets source: `providers`, `quotes`, `inquiries`, `payments`, provider activity log

#### Screen 8 — Patient Acquisition & Funnel
- Patient acquisition channels (Donut — booking-level source: direct/search/referral/affiliate)
- Affiliate performance table (affiliate code → inquiry count → booking count → revenue)
- Patient acquisition trend (monthly new patients by channel)
- Funnel drop-off by patient country (heatmap — stage reached vs. country)
- Patient LTV distribution (Histogram — total payment value per patient)
- Widgets source: `patients`, `inquiries`, `payments`, `bookings_with_affiliate_code`, `affiliates`

#### Screen 9 — Geographic Intelligence
- Demand map (patient country → inquiry volume — choropleth or ranked bar)
- Supply map (provider country → provider count, active provider count)
- Demand vs. supply gap table (country pair: patient country, nearest/preferred provider country, gap score)
- Top routing paths (patient country → provider country, by booking volume)
- Widgets source: `patients`, `providers`, `inquiries`, `payments` (country fields)

#### Screen 10 — Treatment Outcomes (Satisfaction Proxy)
- Average rating by treatment (Bar chart — `reviews.results_rating` as primary proxy)
- Rating breakdown by dimension (overall / results / staff / facility / value — Radar chart)
- Rating trend over time (line chart — monthly average overall rating)
- Review volume trend (monthly)
- Low-rated treatment alerts (treatments with avg results_rating < 3.0 — flagged list)
- **Note**: No clinical outcome data exists in DB. All "outcome" metrics are satisfaction-based from the `reviews` table. True clinical outcomes deferred to future scope.
- Widgets source: `reviews`, `treatments`, `payments`

#### Screen 11 — Financial Health & Cashflow
- Platform GMV trend (monthly — total payment volume across all providers)
- Platform net revenue trend (monthly — total commission collected: `Σ payment.amount × commission / 100`)
- GMV by treatment category (Pareto bar)
- Payout obligation calendar (upcoming payout totals per date — grouped by cadence)
- Refund & dispute rate trend (monthly — refunded / total payments)
- Outstanding revenue (accepted-but-unpaid quotes aging — platform aggregate stacked horizontal bar)
- Widgets source: `payments`, `quotes`, `providers`, `payouts`

#### Screen 12 — Pricing Intelligence
- Quote price distribution by treatment (Box plot — all providers, same as provider Screen 5 but platform-wide)
- Outlier providers (providers with median quote ≥ 2× or ≤ 0.5× platform median per treatment — flagged table)
- Price vs. conversion scatter (platform-wide — each provider-treatment pair as a point)
- Price range evolution (monthly — min/max/median per treatment)
- Currency pricing divergence (same treatment, different currencies — FX-normalised comparison)
- Widgets source: `quotes`, `treatments`, `providers`, `payments`

---

### Screen 13 — Export Report Configuration (Unchanged)

Screen 13 (Export Config) is carried forward from v2.0 without modification.

---

## Data Constraints & Notes

| Constraint | Impact |
|------------|--------|
| `quotes` has no `created_by`/`staff_id` | No team-level or coordinator-level TTFQ breakdown |
| `inquiries` has no `source` field | Lead source (Screen 3, Screen 8) is booking-level only via `bookings_with_affiliate_code` |
| `quotes.sent_at` / `quotes.accepted_at` tracked via quote timeline activity | Confirm with dev team that these timestamps are reliably extractable for TTFQ and aging calculations |
| `payments.commission_amount` not stored | Commission is always calculated: `payment.amount × (quotes.commission / 100)` |
| `reviews` contains satisfaction ratings only | No clinical outcome data — Screen 10 is satisfaction proxy only |
| Platform benchmarks: minimum 5 providers in pool | Benchmarks suppressed if pool < 5 providers for a given treatment |

---

## What Was NOT Changed

- Screen 1 (Provider Main Dashboard) design — **LOCKED** at v2.0
- Module scope and multi-tenant architecture
- Security and privacy rules
- Dependencies on FR-003, FR-004, FR-006, FR-007, FR-010, FR-015, FR-018
- Data retention (24 months)
- Analytics pipeline frequency (15 minutes)
- Admin requirements baseline
