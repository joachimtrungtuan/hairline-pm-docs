# FR-014 Provider Dashboard — Design Lock & PRD Alignment

**Date**: 2026-04-16
**Type**: Major Update
**Document Updated**: `local-docs/project-requirements/functional-requirements/fr014-provider-analytics-reporting/prd.md`
**PRD Version**: 1.0 → 2.0

---

## Summary

The Provider Main Dashboard design has been finalized (Figma: node 6358-111596). The FR-014 PRD has been rewritten to match the locked design. **This screen design is closed — do not reopen layout or widget-type decisions.**

---

## What Changed

### Structure

| Before (v1.0) | After (v2.0) |
|---------------|--------------|
| 5 separate screens (Dashboard, Funnel, Financial, Benchmarks, Export) | Single scrollable page, 3 stacked sections (A: Inbox, B: Performance, C: Financials) |
| Default filter: Last 30 days | Default filter: **Last 4 weeks + All countries** |
| No cross-filtering spec | Cross-filtering: any widget selection updates all sections |
| Low-sample threshold: <5 inquiries | Low-sample threshold: **<30 inquiries** |

### Section A — Inbox (New)

- **New**: TTFQ tile with p50/p90 vs SLA, color-coded Green/Amber/Red
- **New**: New Inquiries tile (Today + This week)
- **New**: Inquiry Queue table (Received + SLA timer, Patient ID-masked, Age, Problem, Country, Actions)
- **New**: Row badges: New / Needs Info / Awaiting Price
- **Defined**: TTFQ = `first_quote.sent_at − inquiry.created_at`; auto-acks excluded; calls/messages do not stop clock

### Section B — Performance (Updated)

| Widget | Before | After |
|--------|--------|-------|
| B1 Conversion | Generic metric | Funnel chart: Inquiries→Qualified→Quoted→Accepted→**In progress** |
| B2 Response Time | Generic "avg hours" metric | **Bullet chart**: p50 + p90 vs SLA target marker |
| B3 Capacity | Not present | **NEW: Calendar heatmap** — Booking Intensity Index (6 weeks × 7 days) |
| B4 Location | Pie chart in Financials section | **Donut chart in Performance** — inquiry share + booked-rate border encoding |

- Funnel "Qualified" stage defined: not spam + mandatory fields (age, problem, contact)
- Funnel final stage is "In progress" (payment captured), not "Completed"
- Intensity Index formula: `(Bookings_on_day ÷ MonthlyDailyAvg_for_that_day's_month) × 100`; clamped 0–300% for color; 3-tier fallback baseline

### Section C — Financials (Updated)

| Widget | Before | After |
|--------|--------|-------|
| C1 Earnings | Generic line chart | **Area line chart** (weekly, Income only — no Gross/Net toggle) |
| C2 Revenue | Bar chart / table | **Pareto bar chart** (ranked bars + cumulative % line) |
| C3 Aging | Not present | **NEW: Stacked horizontal bar** — aging buckets (0–24h, 1–3d, 4–7d, 8–14d, >14d) for accepted-but-unpaid quotes |
| C4 Payouts | Upcoming/previous payment tables | **Column bar** (monthly history) + **inline table** (next + last payout with cadence) |

---

## Design Reference

- Figma: https://www.figma.com/design/kPbnnJL2wPlVCDC9ygJHpH/-SD--Hairline-Dashboard?node-id=6358-111596

---

## What Was NOT Changed

- Module scope and multi-tenant architecture
- Export Report Configuration screen (Screen 3 in v2.0)
- Financial Reports deep-dive screen
- Admin requirements
- Security and privacy rules
- Dependencies on FR-003, FR-004, FR-006, FR-007, FR-010, FR-015
- Data retention (24 months)
- Analytics pipeline frequency (15 minutes)
