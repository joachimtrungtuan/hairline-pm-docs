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
| A-02 | Provider commission and payout settings (Screen 3 Tab 7): view, validation, future-dated Scheduled Configuration, immediate change, payout frequency change, cancel scheduled change, history and activity log | FR-015 | B05 |
| PR-06 | Billing settings (Settings > Billing tab): masked bank details, Owner-only access, first bank account, bank detail validation, read-only Commission & Payout panel | FR-032 | B06 |

### 1.2 Out of Scope

- PR-05 advanced analytics and exports: FR-014 Screen 2 Performance & Conversion, Screen 3 Patient Analytics, Screen 5 Pricing & Benchmarks, Screen 6 Export Report Configuration, and provider CSV exports from Earnings Tracker and Payout History (Phase 4).
- A-08 platform analytics, FR-014 Screens 7–13 (Phase 4).
- Remaining PR-06 settings and help, remaining A-09 configuration and compliance, and advanced A-10 monitoring and support analytics (Phase 4).
- A-05 basic invoice, refund-tier, manual override, and reminder controls (tested in Phase 2; only their payout reconciliation effects are tested here).
- FR-029 central commission-settings screen (global default and shared provider scopes) and the FR-029 shared-scope split (B05 uses providers in single-provider scopes only). Provider-by-provider commission and payout frequency editing in FR-015 Tab 7 is in scope (B05).
- FR-032 billing settings S-02 validation failure (B11) and the Owner confirmation email, which cannot be triggered or observed reliably from the dashboard in Stripe test mode.
- The affiliate's own portal and activation screens (FR-018 Screens 9 and 10), which are not part of the provider or admin dashboards.
- Patient-side actions (quote acceptance, code entry, payment, refunds requested by patients); these are prepared by the team as setup data.

## 2. Entry and Exit Criteria

**Phase handoff** (the team completes these steps on the shared test environment after Phase 2 ends and before the Phase 3 setup starts; Phase 1 and Phase 2 data stays in place). Lead times count back from the first Phase 3 test session:

1. Reactivate `{V4}`, which ends Phase 1 and Phase 2 Suspended. Do this at least 5 weeks before the session, before its first B02 setup cycle (B02 Shared Preconditions, Lead time).
2. Confirm `{V3}` is Active (Phase 2 reactivated it after its B06) before its first B02 setup cycle, at least 5 weeks before the session.
3. Settle every provider earning left from Phase 1 and Phase 2 for `{V1}` to `{V4}` before the first B02 setup cycle: pay out or void any statement still in "Pending Approval", "Approved", "Overdue", or "Failed", and make sure no Phase 2 booking completes inside a B02 setup cycle unless B02 lists it. Otherwise extra bookings join the Phase 3 statements and change every expected amount.
4. Confirm `{S1}` is Active with the system role Clinical Staff in `{V1}`'s team (the base and end state of every phase). Phase 3 does not use `{S2}` (Phase 1 custom role "clinician-front-desk").
5. Confirm the currency setup. FR-029 Default Currency is GBP, with EUR and USD (the FR-018 affiliate currency) enabled, so every Phase 3 quote, package and treatment price, invoice, patient payment, and refund is in GBP for every provider; providers do not choose a quote currency. Payout currency is per provider: `{V1}` (Percentage 15%, Weekly), `{V3}`, and `{V4}` are paid out in GBP; `{V2}` (Flat Rate €150 with Flat Rate Currency EUR, Monthly) is paid out in EUR at each booking's locked rate. `{V1}` and `{V2}` have no Scheduled Configuration (B05). Prepare B02 setup item FX-1 (locked rate 1 GBP = 1.20 EUR) before any `{V2}` setup quote is accepted.
6. Use patients with no conflicting history for the Phase 3 setup items. FR-003 allows one active inquiry per patient, and `{P1}` to `{P11}` carry Phase 1 and Phase 2 bookings. End any of their inquiries still open, or create fresh patients for the affected setup items, and record each mapping in the setup reference list.
7. Prepare the batch setup items with these lead times: the B02 and B01 statements from at least 5 weeks before the session (`{V2}` from the start of the month two months before the session month); BK-19 marked "Completed" right after ST-15 is generated; AFP-6 and AFP-7 within the 30 days before the session; CA-1 on the day before or the day of the session; the B03 and B04 setup data, the `{A3}`, `{S3}`, `{S4}`, and affiliate accounts, and the B06 `{V3}` test bank details at least 2 working days before the session.

**End state for Phase 4:** FR-029 Default Currency GBP; `{V1}` to `{V4}` Active; `{V1}` 15% Weekly and `{V2}` €150 Monthly with no Scheduled Configuration (B05); `{V3}` has a bank account on file again (B06); `{S1}` Active, Clinical Staff. The Phase 3 statements, refunds, promotions, affiliates, and audit entries stay in place.

**Entry criteria** (all must hold before testing starts):

- Phase 2 exit gate passed and the Phase handoff steps above are done.
- Build deployed to the test environment; version recorded below.
- Test accounts `{A1}`, `{A3}`, `{S1}`, `{S3}`, `{S4}`, `{V1}` to `{V4}`, `{P1}` to `{P7}`, and `{AF1}` to `{AF12}` available and verified; the `{AF13}` mailbox available and unused.
- Stripe connected in test mode; payout and refund webhooks delivered to the test environment.
- Setup items listed in each batch's **Shared Preconditions** prepared by the team in the exact states stated there, through real bookings, payments, completed treatments, refunds, and payout runs (no database edits), and the setup reference list sent to the tester.

**Exit criteria** (phase passes when):

- Every High-priority case is Pass.
- No open bug (Bug status Found, Logged, Fixed - retest, or Reopened) on a High-priority case.
- Roadmap exit gate conditions verified, each listed below:
- Provider and admin financial screens show only live figures; no simulated, sample, or fallback values appear, and provider and admin totals for the same payout agree (B01, B02).
- Payout approval, bulk approval, unapproval, void, retry, and affiliate payout processing work only with password re-authentication and within their status rules (B02).
- Refunds made after a payout are deducted from the next payout and carried forward when larger than it (B01, B02).
- Every money-moving or status-changing action appears in the audit log with admin, before and after values, and IP address, and the Billing Viewer role cannot move money (B02).
- Promotion lifecycle (Draft, Active, Paused, Expired, Archived), adoption decisions, and redemption states behave the same on admin and provider sides; no fixture rows appear in the portfolio (B01, B03).
- Affiliate lifecycle (Pending, Active, Suspended, Inactive), one-code-per-affiliate generation, margin guard, and payout status match A-05 execution, with no fixture metrics (B02, B04).
- Provider commission and payout frequency changes need a reason and password re-authentication, are logged, and show read-only to the provider Owner; billing settings are Owner-only (B05, B06).

## 3. Test Environment and Accounts

| Item | Value |
|---|---|
| Provider dashboard URL | https://admin.hairline.app (shared origin with the admin dashboard; sign in with a provider account) |
| Admin dashboard URL | https://admin.hairline.app |
| Backend API base URL | https://backend.hairline.app/api |
| Build / release under test | {Record build or release identifier at test start} |
| Browser(s) | Chrome latest, desktop |
| Plan owner contact | Trung Dang (trung.dang@vantaymedia.com) |
| Setup reference list | Sent privately by the plan owner with the credentials: maps each setup item (BK-n, ST-n, QT-n, PROMO-n, RED-n, AFP-n, CA-1) to its real Booking Reference, Payout Reference, quote, or program name, and lists any patient swapped in the Phase handoff, the GBP to EUR rate locked on each `{V2}` booking (FX-1), the `{V1}` and `{V2}` starting commission Effective Dates, the `{V1}` last four account digits, and the `{V3}` test bank details (B05, B06) |

Accounts used (placeholders; credentials sent privately):

| Placeholder | Role | Used in batches |
|---|---|---|
| `{A1}` | Super admin | B01 (setup), B02, B03, B04, B05 |
| `{A3}` | Admin with the FR-031 Billing Viewer role (read-only billing), same account as Phase 2 | B02 |
| `{S1}` | Provider staff with the system role Clinical Staff at `{V1}` (base and end state of every phase) | B01, B06 |
| `{S3}` | Provider staff with the Manager role at `{V1}`, without financial permission; to be created by the team | B01, B06 |
| `{S4}` | Provider staff with the Billing Staff role at `{V1}`; to be created by the team | B01, B06 |
| `{V1}` | Provider owner, payout currency GBP, percentage commission (15%, Weekly) | B01, B02, B03, B05, B06 |
| `{V2}` | Provider owner, payout currency EUR, flat commission (€150, Flat Rate Currency EUR, Monthly); its quotes and bookings are in GBP like every provider's | B01, B02, B03, B05 |
| `{V3}` | Provider owner, payout currency GBP, Weekly; bank details removed by the team for B02 and added again by the tester in B06 | B01, B02, B06 |
| `{V4}` | Provider owner, payout currency GBP, Weekly, with statements for unapprove and the dispute booking; promotion target. Ends Phase 2 Suspended; reactivated in the Phase handoff | B02, B03 |
| `{P1}` to `{P7}` | Patients owning the prepared bookings (setup data only) | B01, B02, B03, B04 |
| `{AF1}` to `{AF12}` | Affiliates prepared in the states listed in B04 Shared Preconditions (`{AF9}` to `{AF12}` also hold the B02 affiliate payouts); to be created by the team | B02, B04 |
| `{AF13}` | Unused mailbox for the affiliate created during testing; to be created by the team | B04 |

## Team Setup Checklist

The team completes every item before the first Phase 3 test session. Item IDs (ST-n, BK-n, QT-n, PROMO-n, RED-n, AFP-n, CA-1, FX-1) are defined in the batch Shared Preconditions; Phase handoff steps are in section 2. Lead times count back from the first session.

| # | Item | Batches | Owner | Lead time | Done |
|---|---|---|---|---|---|
| 1 | Deploy the build under test and record its identifier in section 3 | All | Dev team | Before phase start | [ ] |
| 2 | Set or confirm FR-029 Default Currency = GBP, with EUR and USD enabled (Phase handoff step 5) | All | Dev team | Before the first B02 setup cycle (at least 9 weeks) | [ ] |
| 3 | Configure `{V2}`'s payout currency as EUR and confirm `{V1}`, `{V3}`, `{V4}` are paid out in GBP (Phase handoff step 5) | B01, B02 | Dev team | Before the first B02 setup cycle (at least 9 weeks) | [ ] |
| 4 | Prepare FX-1: GBP to EUR locked rate 1.20 for BK-8, BK-3, BK-4, BK-16; record each locked rate in the setup reference list | B01, B02 | Dev team | Before the first `{V2}` setup quote is accepted (at least 9 weeks) | [ ] |
| 5 | Stripe connected in test mode; payout, transfer (paid and failed), and refund webhooks delivered to the test environment | B01, B02, B04 | Dev team | Before phase start | [ ] |
| 6 | Reactivate `{V4}` (Phase handoff step 1) | B02, B03 | Dev team | At least 5 weeks | [ ] |
| 7 | Confirm `{V3}` is Active (Phase handoff step 2) | B01, B02, B06 | QA lead | At least 5 weeks | [ ] |
| 8 | Settle Phase 1 and Phase 2 provider earnings for `{V1}` to `{V4}` and keep unlisted bookings out of the B02 cycles (Phase handoff step 3) | B01, B02 | Dev team | Before the first B02 setup cycle (at least 9 weeks for `{V2}`, 5 weeks for the others) | [ ] |
| 9 | Confirm `{S1}` is Active with the system role Clinical Staff (Phase handoff step 4) | B01, B06 | QA lead | Before phase start | [ ] |
| 10 | Confirm `{V1}` 15% Weekly and `{V2}` €150 Monthly, no Scheduled Configuration, neither in a shared FR-029 scope; record both starting Effective Dates (Phase handoff step 5; B05 setup) | B05, B01, B02 | QA lead | Before the first B02 setup cycle | [ ] |
| 11 | End open inquiries of `{P1}` to `{P11}` or create fresh patients for the setup items, and record each mapping (Phase handoff step 6) | B01, B02, B03, B04 | Dev team | Before the setup item that uses the patient | [ ] |
| 12 | Create `{S3}` (Manager without financial permission) and `{S4}` (Billing Staff) at `{V1}`; confirm `{A3}` (Billing Viewer, from Phase 2) | B01, B02, B06 | Dev team | At least 2 working days | [ ] |
| 13 | Create `{AF1}` to `{AF12}` and supply the unused `{AF13}` mailbox | B02, B04 | Dev team | At least 2 working days (earlier where item 20 needs payout history) | [ ] |
| 14 | `{V1}` statements ST-5, ST-10, ST-7, ST-1, with the BK-6 refund between ST-10 and ST-7 | B02, B01 | Dev team | At least 5 weeks (4 weekly cycles) | [ ] |
| 15 | `{V2}` statements ST-8 (BK-8) and ST-2 (BK-3, BK-4) | B02, B01 | Dev team | From the start of the month two months before the session month (about 9 weeks) | [ ] |
| 16 | `{V3}` statements ST-9, ST-14, ST-13, ST-3, with the BK-13 refund and the removal of `{V3}`'s bank details before ST-3 | B02, B01, B06 | Dev team | At least 5 weeks (4 weekly cycles) | [ ] |
| 17 | `{V4}` statements ST-15, ST-6, ST-4 (ST-4 approved by the team) | B02 | Dev team | At least 5 weeks (4 weekly cycles) | [ ] |
| 18 | BK-19 marked "Completed" right after ST-15 is generated; confirm before the session that it is in no statement | B02 | Dev team | Same day as ST-15 generation; A05-FR017-35 and A05-FR017-36 run before the next `{V4}` statement generation that could include it | [ ] |
| 19 | CA-1 currency alert (GBP to EUR, BK-3 and BK-4) | B02 | Dev team | Day before or day of the session | [ ] |
| 20 | Affiliate states and payouts: `{AF1}` to `{AF8}` states, AFP-1 (month before last), AFP-2 (previous month), AFP-4 and AFP-5 (previous month), AFP-6 and AFP-7 (failed within the 30 days before the session) | B04, B02 | Dev team | AFP-1 from the month before last; AFP-6 and AFP-7 within the 30 days before the session; the rest at least 2 working days | [ ] |
| 21 | B01 items BK-15, BK-16, BK-17, BK-18 and admin campaigns PROMO-6, PROMO-7, PROMO-8 | B01, B03 | Dev team | Before phase start; BK-15 completed in the session week; PROMO-8 early enough for its Auto-Decline Window to pass | [ ] |
| 22 | B03 items PROMO-1 to PROMO-4, QT-1, QT-2, QT-4, QT-5 / RED-2, BK-20 / RED-1 | B03, B01 | Dev team | At least 2 working days (PROMO-1 and PROMO-2 Start 7 days before the session) | [ ] |
| 23 | `{V3}` Stripe test bank details and `{V1}`'s last four account digits in the setup reference list | B06 | Dev team | At least 2 working days | [ ] |
| 24 | Send the setup reference list (section 3) to the tester with the credentials | All | QA lead | Before phase start | [ ] |

## 4. Batches and Run Order

| Order | Batch | File | Module | FRs | Cases | Depends on |
|---|---|---|---|---|---|---|
| 1 | B03 | [B03-a06-promotions](batches/B03-a06-promotions.md) | A-06 | FR-019 | 15 | — |
| 2 | B04 | [B04-a07-affiliates](batches/B04-a07-affiliates.md) | A-07 | FR-018 | 16 | — |
| 3 | B02 | [B02-a05-reconciliation-payouts](batches/B02-a05-reconciliation-payouts.md) | A-05 | FR-017 | 23 | — |
| 4 | B01 | [B01-pr05-earnings-payouts-promotions](batches/B01-pr05-earnings-payouts-promotions.md) | PR-05 | FR-017, FR-014, FR-019 | 19 | B02 (`B02-a05-reconciliation-payouts.md` cases A05-FR017-26, for PR05-FR017-04, PR05-FR017-07, and PR05-FR014-04, and A05-FR017-25, for PR05-FR017-06 and PR05-FR014-02) |
| 5 | B05 | [B05-a02-commission-settings](batches/B05-a02-commission-settings.md) | A-02 | FR-015 | 5 | B01 (whole batch, so commission changes cannot affect B01 and B02 figures); A02-FR015-28 runs after B06 PR06-FR032-17 |
| 6 | B06 | [B06-pr06-billing-settings](batches/B06-pr06-billing-settings.md) | PR-06 | FR-032 | 4 | B05 (`B05-a02-commission-settings.md` case A02-FR015-26, for PR06-FR032-17); B02 and B01 complete before PR06-FR032-19 and PR06-FR032-20 add `{V3}`'s bank account |

**End-to-end journey:** Hairline first sets up its growth levers: admins create and publish promotions and send Both Fees campaigns to providers (B03), then onboard affiliates and give each its own code (B04). Patients book and pay using those promotions and codes (prepared by the team). When treatments complete, finance admins review, approve, and pay provider statements and affiliate commissions, handle refunds made after payout, settle disputes and currency alerts, and prove every action in the audit log (B02). B04 reads affiliate payout rows that the team prepares in their final states, so it does not wait for B02. The provider then checks that its earnings, payouts, and promotions match what Hairline did (B01). Last, an admin changes and schedules provider commission and payout frequency terms (B05), and the provider Owner sees those terms read-only next to its bank details, which only the Owner can manage (B06). B05 and B06 interleave: A02-FR015-26 schedules a change, B06 PR06-FR032-17 checks it on the provider side, and A02-FR015-28 cancels it.

## 5. Progress Summary

Update after each test session (the `manual-test-bug-sync` skill can refresh this).

| Batch | Total | Pass | Fail | Blocked | Not tested | Open bugs | Last tested |
|---|---|---|---|---|---|---|---|
| B01 | 19 | 0 | 0 | 0 | 19 | 0 | — |
| B02 | 23 | 0 | 0 | 0 | 23 | 0 | — |
| B03 | 15 | 0 | 0 | 0 | 15 | 0 | — |
| B04 | 16 | 0 | 0 | 0 | 16 | 0 | — |
| B05 | 5 | 0 | 0 | 0 | 5 | 0 | — |
| B06 | 4 | 0 | 0 | 0 | 4 | 0 | — |
| **Total** | **82** | **0** | **0** | **0** | **82** | **0** | **—** |
