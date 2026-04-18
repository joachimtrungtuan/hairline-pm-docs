# FR-014 Verification Fixes — 2026-04-17

**Scope**: Apply verification report fixes to FR-014 PRD v3.0, system-prd.md FR-014 entry, and system-data-schema.md `quotes` table.

**Trigger**: `/verify-fr FR-014` verification report (2026-04-17) identified 3 critical, 3 medium, and 2 minor issues. User selected fixes for all except Issue #6 (admin scope retained as intended).

---

## Changes Applied

### 1. FR-014 PRD v3.0 → v3.1 (`local-docs/project-requirements/functional-requirements/fr014-provider-analytics-reporting/prd.md`)

**Screen 7 drill-down corrections (Critical — Issue #1, Option 1)**

- Tile 4 (Provider TTFQ Health Distribution): `Screen 7 filtered to Red tier` → `Screen 8 filtered to Red tier`
- Tile 5 (Provider Engagement Rate): `Screen 7 engagement section filtered to dormant` → `Screen 8 engagement section filtered to dormant`
- B4 (Treatment Type Distribution): `Screen 10 filtered to that treatment` → `Screen 11 filtered to that treatment`
- C1 (Platform GMV), C2 (Commission Earned), C3 (Upcoming Payout Obligations), C4 (Platform Cash-at-Risk): all `Drill-down → Screen 11` → `Drill-down → Screen 12`

**Executive Summary screen count (Medium — Issue #4, Option 1)**

- Updated "12-screen analytics suite" → "13-screen suite (12 analytical + 1 export config)"
- Updated "five screens" on provider side → "six screens" (with explicit breakdown of Screen 1 cockpit, Screens 2–5 analytical, Screen 6 export config)
- Added explicit Screen 7–13 range for admin side

**Screen 2 low-sample rule unified (Medium — Issue #5, Option 2)**

- Removed Screen 2 per-widget rule: "Minimum 10 inquiries required to display conversion rate"
- Replaced with reference to global Data Quality Rule 7 (<30 inquiries threshold)

**Schema gap resolved (Critical — Issue #2, Option 1)**

- Renamed "Data Model Gaps to Resolve Before Implementation" → "Data Model Additions (Resolved)"
- Removed "confirm with development team" caveat
- Noted that columns now exist in `system-data-schema.md`

**Drill-down reference form standardised (Minor — Issue #7, Option 2)**

- All drill-downs on Screen 7 now reference `Screen N` only (no inline screen name). Tile 4's "Provider Performance screen (Screen 7)" parenthetical removed.

**Approvals block (Minor — Issue #8, Option 2)**

- Placeholder `[Name]/[Date]/[Status]` rows replaced with `— / — / Pending review` for all three approver rows.

**Change log**

- Added v3.1 entry dated 2026-04-17 summarising the above fixes. Last Updated timestamp bumped.

### 2. System PRD (`local-docs/project-requirements/system-prd.md`)

**FR-014 admin requirements added (Critical — Issue #3, Option 1)**

- Added Scope sentence summarising the 13-screen split.
- Split Requirements into "Provider Requirements" (original 7 bullets unchanged) and "Admin Requirements" (12 new bullets covering platform overview, provider performance/engagement, patient acquisition, geographic intelligence, treatment outcomes, financial health & cashflow, pricing intelligence, anonymisation rules, admin-configurable parameters, audit logging).

### 3. System Data Schema (`local-docs/project-requirements/system-data-schema.md`)

**Quotes table — new columns**

- Added `sent_at TIMESTAMP NULLABLE` — populated on `inquiry → quote` status transition; feeds TTFQ analytics.
- Added `accepted_at TIMESTAMP NULLABLE` — populated on `→ accepted` status transition; feeds Quote→Payment aging analytics.

---

## Deferred / Not Applied

- **Issue #6 (Client alignment on admin analytics scope)**: Skipped at user direction. Admin-side screens (Provider League Table, Performance Scatter, New Provider Ramp, Inquiry Seasonality, Emerging Patient Origins, Price Outlier Detection, etc.) are intentional additions by the product owner.

---

## Downstream Impact

- **Backend (Laravel)**: `quotes` table migration required to add `sent_at`, `accepted_at` columns plus a status-transition trigger/service hook to populate them. Existing rows require no backfill (analytics will simply have NULL TTFQ for pre-migration quotes).
- **FR-014 task generation**: Can now proceed without blocking on timestamp-derivation design question.
- **System PRD governance**: Admin analytics scope now traceable from system-prd.md FR-014 down to individual REQ-014-060 through REQ-014-094 in the PRD.

---

## Files Changed

- `local-docs/project-requirements/functional-requirements/fr014-provider-analytics-reporting/prd.md`
- `local-docs/project-requirements/system-prd.md`
- `local-docs/project-requirements/system-data-schema.md`
