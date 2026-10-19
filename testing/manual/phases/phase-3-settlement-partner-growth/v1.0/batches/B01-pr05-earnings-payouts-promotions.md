# B01 — PR-05 Earnings, Payouts, and Promotion Visibility

## Batch Control

| Field | Value |
|---|---|
| Batch | B01 |
| Phase / plan version | Phase 3 / v1.0 |
| Module | PR-05 — Financial Management & Analytics (provider) |
| FRs | FR-017 (provider earnings and payout history), FR-014 (Finance & Payouts essentials), FR-019 (provider promotion view) |
| PRD sources | [FR-017 › Provider Platform Screens (PR-05), Screens 9, 10](../../../../../../project-requirements/functional-requirements/fr017-admin-billing-finance/prd.md#provider-platform-screens-pr-05); [FR-014 › Screen 1 Section C and Screen 4: Finance & Payouts](../../../../../../project-requirements/functional-requirements/fr014-provider-analytics-reporting/prd.md#screen-4-finance--payouts); [FR-014 › Business Rules](../../../../../../project-requirements/functional-requirements/fr014-provider-analytics-reporting/prd.md#business-rules); [FR-019 › Provider Platform Screens, Screens 7–10](../../../../../../project-requirements/functional-requirements/fr019-promotions-discounts/prd.md#provider-platform-screens-pr-02--pr-05) |
| Platform | Provider dashboard |
| Tester | |
| Build tested | |

## How to Fill In This File

1. Run cases in table order unless a case says otherwise.
2. Fill only: **Actual result / data**, **Result**, **Notes**, **Evidence**, **Bug status**, **Last tested**.
3. **Result** values: `Not tested`, `Pass`, `Fail`, `Blocked`. **Bug status** values: `—`, `Found`, `Logged`, `Fixed - retest`, `Closed`, `Reopened` (set `Found` when you see a bug; the team logs it in Plane).
4. Put usability observations in **Notes**: what you did, what happened, and why it was confusing or slow, even when the case passes.
5. Do not edit IDs, steps, or expected results, and do not use the vertical-bar character inside cells. Put questions in **Notes**.

## Flow Overview

This batch tests what a provider clinic sees about its money and its promotions once Hairline settles with it.

- **Two-stage earnings view (FR-017 › Provider Platform Screens).** Stage 1, the Provider Earnings Tracker, lists every completed treatment and what the clinic earns from it after Hairline's commission, including refund adjustments. Stage 2, Provider Payout History, lists payouts only after Hairline has approved them and started the transfer, so statements still "Pending Approval" or "Approved" are never shown to the provider. A failed transfer shows a reassuring message and later the retry history.
- **Finance & Payouts essentials (FR-014 › Screen 4 and Screen 1 Section C).** The analytics area summarises revenue, commission and net revenue, refunds, and the payout schedule, in the provider's currency, using the same payout states as FR-017 (Upcoming, Processing, Paid, Failed; Voided is never shown). Only roles with financial access see it (FR-014 Business Rule 15F).
- **Promotion visibility (FR-019 › Screens 7–10).** The provider sees admin campaigns offered to it and accepts, declines, or revokes them; manages its own promotions; and sees which quotes and bookings used each promotion.

The numbers here must match the admin side tested in B02 (payouts) and B03 (promotions). Advanced analytics screens, benchmarks, and exports are Phase 4 and are not tested here.

## Shared Preconditions

- Phase 2 exit gate passed; Provider dashboard reachable; `{V1}` and `{V2}` (provider owners) and `{S1}` (clinician / front-desk staff of `{V1}`) can sign in.
- The team has prepared, through real completed treatments and real payments (patient actions done by the team as setup), the bookings, refunds, and payout statements listed in **Test Data Sets**. Payout states are reached through the admin payout workflow (B02) or prepared by the team before the session.
- `{V1}` currency is GBP with 15% commission; `{V2}` currency is EUR with a flat €150 commission.
- For promotion cases, `{A1}` has published an admin Both-Fees campaign targeting `{V1}` (from B03 or prepared by the team).

## Test Data Sets

| Data set | Purpose | Values | Account |
|---|---|---|---|
| DS-PR05-01 | Percentage commission earnings | `{V1}` completed treatment for `{P1}`: Gross Amount £2,000.00, Commission "15%", Commission Deducted £300.00, Net Earning £1,700.00, Treatment Status "Completed", Payout Status "Pending Next Payout" | `{V1}` |
| DS-PR05-02 | Flat commission earnings | `{V2}` completed treatment for `{P3}`: Gross Amount €2,400.00, Commission "€150 Flat", Commission Deducted €150.00, Net Earning €2,250.00 | `{V2}` |
| DS-PR05-03 | Refund before payout | `{V1}` completed treatment for `{P2}`, £1,500.00, fully refunded by the team before it was included in any payout | `{V1}` |
| DS-PR05-04 | Refund after payout | `{V1}` treatment for `{P5}` included in a Paid payout, then refunded £600.00 by the team; deduction applied in the next statement | `{V1}` |
| DS-PR05-05 | Payout states | `{V1}`: one Paid payout (with invoice), one Processing payout, one statement in "Pending Approval" and one "Approved" in admin (not yet transferred), one "Voided" statement. `{V2}`: one Failed payout, later retried by `{A1}` | `{V1}`, `{V2}` |
| DS-PR05-06 | Analytics period | Finance & Payouts with default period "Last 4 weeks"; a period that contains DS-PR05-01 and DS-PR05-04 | `{V1}` |
| DS-PR05-07 | Role without financial access | `{S1}` signed in to `{V1}`'s clinic (clinical staff role) | `{S1}` |
| DS-PR05-08 | Admin campaigns | Two admin campaigns for `{V1}` in Pending: "Campaign A" to accept, "Campaign B" to decline. One campaign whose Auto-Decline Window has passed (Auto-Declined) | `{V1}` |
| DS-PR05-09 | Comment boundaries | Empty; exactly 500 characters; 501 characters. Valid comment: "Clinic capacity is full for this period" | `{V1}` |
| DS-PR05-10 | Own promotion | Promotion Name "Spring PRP 10" (valid); 2-character name "AB" (invalid); 121-character name (invalid). Type Percentage, value 10, Applies To "Treatment cost". Code "SPRINGPRP10"; a code already used by an admin program in B03 (duplicate). Application Mode "Code-only" | `{V1}` |

## Test Cases

| ID | Title | Priority | PRD flow ref | Preconditions | Test data | Steps | Expected result | Actual result / data | Result | Notes | Evidence | Bug ID | Bug status | Last tested |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PR05-FR017-01 r1 | Earnings Tracker shows net earning after percentage commission | High | FR-017 › Screen 9: Provider Earnings Tracker; Business Rule 5 | Signed in as `{V1}` | DS-PR05-01 | 1. From the provider navigation open the Financial Management area and then the Earnings Tracker.<br>2. Find the `{P1}` booking row.<br>3. Read every column.<br>4. Look for any control that edits a row. | 1. Earnings Tracker loads with the provider's real treatments only.<br>2. The row is listed.<br>3. Booking Reference, Patient Name, Treatment Date, Treatment Type, Gross Amount £2,000.00, Commission "15%", Commission Deducted £300.00, Net Earning £1,700.00, Currency GBP, Treatment Status "Completed", Payout Status "Pending Next Payout".<br>4. The screen is read-only. | | Not tested | | | | — | |
| PR05-FR017-02 r1 | Earnings Tracker shows flat commission in provider currency | High | FR-017 › Screen 9 (Commission column); Commission rules (flat per completed procedure) | Signed in as `{V2}` | DS-PR05-02 | 1. Open the Earnings Tracker.<br>2. Find the `{P3}` booking row. | 1. Screen loads.<br>2. Commission shows "€150 Flat", Commission Deducted €150.00, Net Earning €2,250.00, Currency EUR. | | Not tested | | | | — | |
| PR05-FR017-03 r1 | Refund before payout zeroes the earning but keeps the row | High | FR-017 › Screen 9 Business Rules (refunded before payout) | Signed in as `{V1}` | DS-PR05-03, DS-PR05-01 | 1. Open the Earnings Tracker and find the `{P2}` row.<br>2. Hover the Adjustment Marker.<br>3. Read Total Pending Earnings in the Summary Bar. | 1. Row is still listed with Net Earning £0.00 shown with strikethrough styling and Adjustment Marker "Refunded".<br>2. Tooltip explains the refund.<br>3. Total Pending Earnings does not include the refunded treatment. | | Not tested | | | | — | |
| PR05-FR017-04 r1 | Refund after payout is shown as a deduction from the next payout | High | FR-017 › Screen 9 (Adjustment Marker); post-payout refund rule | Signed in as `{V1}`; `{A1}` view of the same statement checked in B02 A05-FR017-30 | DS-PR05-04 | 1. Find the `{P5}` row in the Earnings Tracker.<br>2. Hover the Adjustment Marker.<br>3. Compare the deducted amount with the next payout shown to the provider. | 1. Adjustment Marker reads "Refunded — Deducted from Next Payout" and the row stays listed.<br>2. Tooltip states the refund amount £600.00.<br>3. The next payout shows the same £600.00 deduction that the admin sees. | | Not tested | | | | — | |
| PR05-FR017-05 r1 | Summary Bar totals, filters, and sorting match the rows | Medium | FR-017 › Screen 9 (Summary Bar, filters, sort) | Signed in as `{V1}` | DS-PR05-01, DS-PR05-03, DS-PR05-06 | 1. Read Total Pending Earnings, Next Payout Date, Treatments This Period.<br>2. Add up Net Earning for rows with Payout Status "Pending Next Payout".<br>3. Filter by Payout Status, then by Treatment Status "Aftercare", then by a date range with no treatments.<br>4. Sort by Treatment Date. | 1. All three values are shown.<br>2. The sum equals Total Pending Earnings; Next Payout Date matches the provider's schedule.<br>3. Each filter shows only matching rows; the empty range shows an empty-state message, not an error.<br>4. Rows reorder by date. | | Not tested | | | | — | |
| PR05-FR017-06 r1 | Payout History hides statements that Hairline has not approved and transferred | High | FR-017 › Provider entry (Stage 2 visibility); Screen 10: Provider Payout History | Signed in as `{V1}` | DS-PR05-05 | 1. Open Payout History.<br>2. Look for the statements that are "Pending Approval", "Approved", or "Voided" in admin.<br>3. Read the Status values shown. | 1. Payout History loads.<br>2. None of those statements are listed.<br>3. Only "Processing", "Paid", or "Failed" appear. | | Not tested | | | | — | |
| PR05-FR017-07 r1 | Paid payout shows reference, breakdown, and invoice | High | FR-017 › Screen 10 (fields, Treatment Breakdown, Invoice) | Signed in as `{V1}` | DS-PR05-05 | 1. Find the Paid payout row and read every column.<br>2. Click "Copy Reference".<br>3. Click the row.<br>4. Click Invoice.<br>5. Find the Processing row and check its Invoice action. | 1. Payout Reference in the PAY-HP-PRV-xxxxx-YYYY-MM format, Payout Date, Transfer Confirmation Date, Payout Period, Treatment Count, Gross Total, Commission Deducted, Net Payout, Payout Frequency, Status "Paid"; Gross Total minus Commission Deducted and adjustments equals Net Payout.<br>2. A confirmation shows the reference was copied.<br>3. Treatment Breakdown opens and its rows add up to the totals.<br>4. Invoice PDF downloads and shows the same Net Payout.<br>5. Invoice is disabled while Processing. | | Not tested | | | | — | |
| PR05-FR017-08 r1 | Failed payout shows a clear message and the retry history | High | FR-017 › Screen 10 (Failed message, Failure Reason, Retry Resolution History) | Signed in as `{V2}`; `{A1}` retried the payout (B02 A05-FR017-27) | DS-PR05-05 | 1. Open Payout History and find the Failed payout.<br>2. Read the message.<br>3. After the admin retry, reopen the row. | 1. Row Status is "Failed".<br>2. Message reads "Your payout of [amount] for [period] could not be processed. Hairline is investigating. You will be notified once resolved." with the amount and period filled in.<br>3. Retry Resolution History lists the retry with date and the new status. | | Not tested | | | | — | |
| PR05-FR014-01 r1 | Finance & Payouts shows commission and net revenue in provider currency | High | FR-014 › Screen 4: Finance & Payouts (Widget 4, Widget 1); Business Rules 1 and currency rule | Signed in as `{V1}` | DS-PR05-06 | 1. Open Provider Analytics and then Finance & Payouts.<br>2. Check the default period.<br>3. Set the period to include DS-PR05-01 and DS-PR05-04.<br>4. Read the three tiles in Commission & Net Revenue.<br>5. Read the footer. | 1. Screen loads with skeleton placeholders while loading, then real data.<br>2. Default period is "Last 4 weeks".<br>3. Widgets refresh for the new period.<br>4. Net Revenue equals Gross minus Commission for the period, and the figures agree with the Earnings Tracker for the same treatments.<br>5. Amounts are in GBP and the footer reads "Historical exchange rates applied". | | Not tested | | | | — | |
| PR05-FR014-02 r1 | Payout History & Schedule uses FR-017 states and ignores treatment filters | High | FR-014 › Screen 4 Widget 8; Business Rule 5A | Signed in as `{V1}` | DS-PR05-05 | 1. Scroll to Payout History & Schedule.<br>2. Read the Status values in the table.<br>3. Compare amounts with Payout History (FR-017 Screen 10).<br>4. Apply a treatment filter on the screen. | 1. Column chart and paginated table are shown with Period, Amount, Status, Paid date, Cadence.<br>2. Statuses are only "Upcoming", "Processing", "Paid", "Failed"; the Pending Approval and Approved statements appear as "Upcoming"; the Voided statement is not shown.<br>3. Paid and Processing amounts match Payout History.<br>4. Widget values do not change and a note says it is not filtered by treatment. | | Not tested | | | | — | |
| PR05-FR014-03 r1 | Refund widget counts refunds without removing original revenue | Medium | FR-014 › Screen 4 Widget 5 and Widget 1 | Signed in as `{V1}`; period from PR05-FR014-01 | DS-PR05-03, DS-PR05-04, DS-PR05-06 | 1. Read the Refunds widget.<br>2. Read Revenue Trend for the week of the `{P2}` payment. | 1. Total refund amount includes the £1,500.00 and £600.00 refunds; refund rate is shown as a percentage.<br>2. The original £1,500.00 payment still counts as captured income in its week; the refund is shown separately. | | Not tested | | | | — | |
| PR05-FR014-04 r1 | Main Dashboard payout summary shows the right rows | Medium | FR-014 › Screen 1 Section C (C4 Payouts — History & Upcoming); Screen 4 Widget 7 | Signed in as `{V1}` | DS-PR05-05 | 1. Open the Main Dashboard and find the Financials section.<br>2. Read the Payouts inline table.<br>3. On Finance & Payouts, click the Cash-at-Risk summary. | 1. Section C shows Earnings Trend, Revenue by Treatment, Quote to Payment Aging, and Payouts.<br>2. Up to 3 rows: next Upcoming payout, any Processing or Failed payout, then the most recent Paid payout, with Type, Period, Amount, Scheduled Date, Cadence; no Voided row.<br>3. It links to the aging chart with buckets 0–24h, 1–3d, 4–7d, 8–14d, >14d. | | Not tested | | | | — | |
| PR05-FR014-05 r1 | Clinical staff cannot see financial screens | High | FR-014 › Business Rule 15F (role matrix) and Rule 15B | Signed in as `{S1}` | DS-PR05-07 | 1. Open Provider Analytics.<br>2. Look for Finance & Payouts in the navigation.<br>3. Open the Main Dashboard.<br>4. Paste the Finance & Payouts address copied from the `{V1}` session. | 1. Analytics opens for permitted screens.<br>2. Finance & Payouts is not in the navigation.<br>3. Section C Financials is not shown.<br>4. No financial figures are displayed (record in Notes whether the page redirects, shows an access message, or shows an empty page). | | Not tested | | | | — | |
| PR05-FR019-01 r1 | Provider accepts an admin campaign | High | FR-019 › Screen 7: Provider — Admin Campaigns; Acceptance Criterion 1 | Signed in as `{V1}` | DS-PR05-08 | 1. Open Admin Campaigns.<br>2. On the Pending tab read "Campaign A".<br>3. Click Accept and confirm.<br>4. Open the Active tab within 5 seconds. | 1. Tabs Pending, Active, Past are shown.<br>2. Card shows Program Name, Description, Discount Type / Value, Active Window, and Financial Impact Preview.<br>3. A success message is shown.<br>4. "Campaign A" is in the Active tab with a Decision Timestamp and is offered in quote creation. | | Not tested | | | | — | |
| PR05-FR019-02 r1 | Provider declines with a comment; past campaigns show their outcome | Medium | FR-019 › Screen 7 (Decline, Past tab, Auto-Decline) | Signed in as `{V1}` | DS-PR05-08, DS-PR05-09 | 1. Click Decline on "Campaign B".<br>2. Paste the 501-character comment.<br>3. Enter the valid comment and confirm.<br>4. Open the Past tab. | 1. Decline asks for an optional comment.<br>2. Input is limited to 500 characters with a visible message.<br>3. Decline is saved.<br>4. "Campaign B" shows Declined with its timestamp; the expired-window campaign shows Auto-Declined. | | Not tested | | | | — | |
| PR05-FR019-03 r1 | Provider revokes an adopted campaign | High | FR-019 › Screen 7 Acceptance Criterion 2 | Signed in as `{V1}`; PR05-FR019-01 passed | DS-PR05-08 | 1. On the Active tab click Revoke Adoption for "Campaign A".<br>2. Try to confirm without a reason, then enter a reason and confirm.<br>3. Open the Past tab.<br>4. Start a new quote and open the discount selection. | 1. A confirmation asks for a reason.<br>2. Confirm is blocked without a reason; with a reason it succeeds.<br>3. "Campaign A" shows Revoked-by-Provider.<br>4. "Campaign A" is no longer offered; quotes that already used it keep the discount. | | Not tested | | | | — | |
| PR05-FR019-04 r1 | My Promotions lists the provider's own promotions with filters | High | FR-019 › Screen 8: Provider — My Promotions (List) | Signed in as `{V1}`; at least one own promotion exists (or PR05-FR019-05 run first) | DS-PR05-10 | 1. Open My Promotions.<br>2. Read the columns.<br>3. Filter by each Status, then by keyword "Spring".<br>4. Click View Applications on a row. | 1. Only `{V1}`'s own promotions are listed; no sample rows.<br>2. Promotion Name, Code (or "—"), Type / Value, Applies To, Active Window, Status, Redemptions, Savings Issued, Row Actions.<br>3. Status filter offers Draft, Active, Paused, Expired, Archived and returns matching rows; keyword search finds "Spring PRP 10".<br>4. Promotion Analytics & Applications opens filtered to that promotion. | | Not tested | | | | — | |
| PR05-FR019-05 r1 | Creating a promotion validates name length, code rules, and uniqueness | High | FR-019 › Screen 9: Provider — Promotion Detail; Screen 8 Business Rules (platform-wide code uniqueness) | Signed in as `{V1}` | DS-PR05-10 | 1. Create a promotion with Promotion Name "AB" and save.<br>2. Use the 121-character name and save.<br>3. Use "Spring PRP 10", Application Mode "Code-only", leave Code empty, save.<br>4. Enter the duplicate admin code and save.<br>5. Enter "SPRINGPRP10" and save.<br>6. Pause, then Resume, then Archive the promotion. | 1. Save is blocked with a 3–120 character message.<br>2. Save is blocked.<br>3. Save is blocked; Code is required for Code-only.<br>4. Save is blocked with a message that the code is already in use.<br>5. Promotion saves; Funding shows Provider Only; no approval step is required.<br>6. Status changes Active, Paused, Active, Archived; an archived promotion offers no Resume. | | Not tested | | | | — | |
| PR05-FR019-06 r1 | Applications view is read-only and matches the accepted terms | Medium | FR-019 › Screen 10: Provider — Promotion Analytics & Applications | Signed in as `{V1}`; a booking that used one of `{V1}`'s promotions exists (team setup) | DS-PR05-10 | 1. Open Promotion Analytics & Applications.<br>2. Read the Overview tab.<br>3. Open the Applications tab and a row.<br>4. Look for remove or replace actions. | 1. Screen opens.<br>2. Figures reflect real redemptions only.<br>3. Discount amount matches the accepted quote snapshot.<br>4. No action exists to remove or replace the applied promotion. | | Not tested | | | | — | |

## Batch Summary

| Total | Pass | Fail | Blocked | Not tested | Open bugs |
|---|---|---|---|---|---|
| 19 | 0 | 0 | 0 | 19 | 0 |

## Case Change Log

| Case | Revision | Date | Change |
|---|---|---|---|
| PR05-FR017-01 | r1 | 2026-10-19 | Created |
| PR05-FR017-02 | r1 | 2026-10-19 | Created |
| PR05-FR017-03 | r1 | 2026-10-19 | Created |
| PR05-FR017-04 | r1 | 2026-10-19 | Created |
| PR05-FR017-05 | r1 | 2026-10-19 | Created |
| PR05-FR017-06 | r1 | 2026-10-19 | Created |
| PR05-FR017-07 | r1 | 2026-10-19 | Created |
| PR05-FR017-08 | r1 | 2026-10-19 | Created |
| PR05-FR014-01 | r1 | 2026-10-19 | Created |
| PR05-FR014-02 | r1 | 2026-10-19 | Created |
| PR05-FR014-03 | r1 | 2026-10-19 | Created |
| PR05-FR014-04 | r1 | 2026-10-19 | Created |
| PR05-FR014-05 | r1 | 2026-10-19 | Created |
| PR05-FR019-01 | r1 | 2026-10-19 | Created |
| PR05-FR019-02 | r1 | 2026-10-19 | Created |
| PR05-FR019-03 | r1 | 2026-10-19 | Created |
| PR05-FR019-04 | r1 | 2026-10-19 | Created |
| PR05-FR019-05 | r1 | 2026-10-19 | Created |
| PR05-FR019-06 | r1 | 2026-10-19 | Created |
