# Phase 3 Manual Test Plan — Settlement and Partner Growth

## Document Control

| Field | Value |
|---|---|
| Phase | Phase 3 — Settlement and Partner Growth |
| Plan version | 1.0 |
| Status | Draft |
| Scope source | [Admin and provider implementation status and release roadmap › Recommended four-phase release roadmap, Phase 3 row](../../../../../reports/2026-09-06/admin-provider-implementation-status-and-release-roadmap.md) |
| Release objective | Reconcile money and activate scalable partner acquisition |
| Exit gate | Financial UI uses authoritative APIs with no simulated or fallback values; payout, refund, re-authentication, and audit rules pass; promotion and affiliate lifecycle contracts align |
| Created | 2026-10-19 |
| Last updated | 2026-10-19 |
| Plan owner | Product / QA lead, Vân Tay Media |
| Tester(s) | |

## Change Log

| Version | Date | Change | By |
|---|---|---|---|
| 1.0 | 2026-10-19 | Initial plan | Product / QA lead |

## 1. Scope

### 1.1 In Scope

| Module | Function slice in this phase | FRs | Batch |
|---|---|---|---|
| PR-05 | Earnings and payout essentials (Earnings Tracker, Payout History, Finance & Payouts screen, dashboard Financials section, financial role visibility) and promotion visibility (admin campaigns, own promotions, applications) | FR-017, FR-014, FR-019 | B01 |
| A-05 | Provider payout reconciliation and execution (approve, bulk approve, unapprove, void, retry, notes), post-payout refund deduction, affiliate payout execution, revenue dashboard, transaction search, dispute resolution, currency alert decisions, audit log, Billing Viewer read-only | FR-017 | B02 |
| A-06 | Promotion program hub, program create and lifecycle, provider adoption manager, provider promotion portfolio, Hairline-funded codes, promotion analytics and applications | FR-019 | B03 |
| A-07 | Affiliate onboarding, commission rules and changes, suspend, reinstate, offboard with settlement, single and bulk code generation, margin guard, promo code management, payout status and detail | FR-018 | B04 |

### 1.2 Out of Scope

- PR-05 advanced analytics and exports: FR-014 Screen 2 Performance & Conversion, Screen 3 Patient Analytics, Screen 5 Pricing & Benchmarks, Screen 6 Export Report Configuration, and provider CSV exports from Earnings Tracker and Payout History (Phase 4).
- A-08 platform analytics, FR-014 Screens 7–13 (Phase 4).
- Remaining PR-06 settings and help, remaining A-09 configuration and compliance, and advanced A-10 monitoring and support analytics (Phase 4).
- A-05 basic invoice, refund-tier, manual override, and reminder controls (tested in Phase 2; only their payout reconciliation effects are tested here).
- Commission and payout schedule configuration owned by FR-015 and FR-029 (used as existing setup only).
- The affiliate's own portal and activation screens (FR-018 Screens 9 and 10), which are not part of the provider or admin dashboards.
- Patient-side actions (quote acceptance, code entry, payment, refunds requested by patients); these are prepared by the team as setup data.

## 2. Entry and Exit Criteria

**Entry criteria** (all must hold before testing starts):

- Phase 2 exit gate passed.
- Build deployed to the test environment; version recorded below.
- Test accounts `{A1}`, `{S1}`, `{V1}` to `{V4}`, `{P1}` to `{P7}`, and the Billing Viewer admin account available and verified.
- Stripe connected in test mode; payout and refund webhooks delivered to the test environment.
- Setup data listed in each batch's **Test Data Sets** prepared by the team through real bookings, payments, completed treatments, and payout runs (no database edits).

**Exit criteria** (phase passes when):

- Every High-priority case is Pass.
- No open bug with Bug status Found, Logged, or Reopened at High priority.
- Provider and admin financial screens show only live figures; no simulated, sample, or fallback values appear, and provider and admin totals for the same payout agree (B01, B02).
- Payout approval, bulk approval, unapproval, void, retry, and affiliate payout processing work only with password re-authentication and within their status rules (B02).
- Refunds made after a payout are deducted from the next payout and carried forward when larger than it (B01, B02).
- Every money-moving or status-changing action appears in the audit log with admin, before and after values, and IP address, and the Billing Viewer role cannot move money (B02).
- Promotion lifecycle (Draft, Active, Paused, Expired, Archived), adoption decisions, and redemption states behave the same on admin and provider sides; no fixture rows appear in the portfolio (B01, B03).
- Affiliate lifecycle (Pending, Active, Suspended, Inactive), one-code-per-affiliate generation, margin guard, and payout status match A-05 execution, with no fixture metrics (B02, B04).

## 3. Test Environment and Accounts

| Item | Value |
|---|---|
| Provider dashboard URL | {Provider dashboard URL} |
| Admin dashboard URL | https://admin.hairline.app |
| Backend API base URL | https://backend.hairline.app/api |
| Build / release under test | |
| Browser(s) | Chrome latest, desktop |

Accounts used (placeholders; credentials sent privately):

| Placeholder | Role | Used in batches |
|---|---|---|
| `{A1}` | Super admin | B01 (setup), B02, B03, B04 |
| Billing Viewer admin (no placeholder yet) | Admin with FR-031 Billing Viewer role | B02 |
| `{S1}` | Provider staff (clinician / front desk) at `{V1}` | B01 |
| `{V1}` | Provider owner, GBP, percentage commission | B01, B02, B03 |
| `{V2}` | Provider owner, EUR, flat commission | B01, B02, B03 |
| `{V3}` | Provider with missing bank details | B02 |
| `{V4}` | Provider with statements for unapprove and void | B02 |
| `{P1}` to `{P7}` | Patients owning the prepared bookings (setup data only) | B01, B02, B03, B04 |

## 4. Batches and Run Order

| Order | Batch | File | Module | FRs | Cases | Depends on |
|---|---|---|---|---|---|---|
| 1 | B03 | [B03-a06-promotions](batches/B03-a06-promotions.md) | A-06 | FR-019 | 15 | — |
| 2 | B04 | [B04-a07-affiliates](batches/B04-a07-affiliates.md) | A-07 | FR-018 | 16 | B02 for cases A07-FR018-14 and -15 |
| 3 | B02 | [B02-a05-reconciliation-payouts](batches/B02-a05-reconciliation-payouts.md) | A-05 | FR-017 | 23 | B04 (affiliates exist) |
| 4 | B01 | [B01-pr05-earnings-payouts-promotions](batches/B01-pr05-earnings-payouts-promotions.md) | PR-05 | FR-017, FR-014, FR-019 | 19 | B02, B03 |

**End-to-end journey:** Hairline first sets up its growth levers: admins create and publish promotions and send Both Fees campaigns to providers (B03), then onboard affiliates and give each its own code (B04). Patients book and pay using those promotions and codes (prepared by the team). When treatments complete, finance admins review, approve, and pay provider statements and affiliate commissions, handle refunds made after payout, settle disputes and currency alerts, and prove every action in the audit log (B02); the affiliate payout cases in B04 are completed after B02 has moved the money. Finally, the provider checks that its earnings, payouts, and promotions match what Hairline did (B01).

## 5. Progress Summary

Update after each test session (the `manual-test-bug-sync` skill can refresh this).

| Batch | Total | Pass | Fail | Blocked | Not tested | Open bugs | Last tested |
|---|---|---|---|---|---|---|---|
| B01 | 19 | 0 | 0 | 0 | 19 | 0 | — |
| B02 | 23 | 0 | 0 | 0 | 23 | 0 | — |
| B03 | 15 | 0 | 0 | 0 | 15 | 0 | — |
| B04 | 16 | 0 | 0 | 0 | 16 | 0 | — |
| **Total** | 73 | 0 | 0 | 0 | 73 | 0 | — |
