# B05 — A-02 Commission and Payout Settings

## Batch Control

| Field | Value |
|---|---|
| Batch | B05 |
| Phase / plan version | Phase 3 / v1.0 |
| Module | A-02 — Provider Management (Admin) |
| FRs | FR-015 Screen 3 Tab 7 (primary); FR-029 and FR-032 cited where touched |
| PRD sources | [FR-015 › Tab 7: Commission & Financials (Admin-Only)](../../../../../../project-requirements/functional-requirements/fr015-provider-management/prd.md#tab-7-commission--financials-admin-only); [FR-015 › Tab 8: Activity Log (Admin-Only)](../../../../../../project-requirements/functional-requirements/fr015-provider-management/prd.md#tab-8-activity-log-admin-only); [FR-015 › Screen 3: Provider Profile Details (Tabbed View)](../../../../../../project-requirements/functional-requirements/fr015-provider-management/prd.md#screen-3-provider-profile-details-tabbed-view) (Admin change reason rule); [FR-032 › Screen 4: Billing Settings (Owner Role Only)](../../../../../../project-requirements/functional-requirements/fr032-provider-dashboard-settings/prd.md#screen-4-billing-settings-owner-role-only) |
| Platform | Admin dashboard |
| Tester | |
| Build tested | |

## How to Fill In This File

1. One tester runs a batch at a time; do not share a batch file with another tester during a run. Before starting, add your entry to **Tester** (`Name (YYYY-MM-DD)`) and **Build tested** (`<build> (YYYY-MM-DD)`) in Batch Control. Entries accumulate, separated by `; `, for example `Linh (2026-10-20); Minh (2026-11-02)`. Replace the `{...}` placeholder on the first run; never delete earlier entries.
2. Run cases in table order unless a case says otherwise.
3. In each case row, fill only these columns:
   - **Actual result / data**: what you observed and the exact values you entered, for example "Saved; status shows Draft; total 2,450 GBP".
   - **Result**: `Not tested`, `Pass`, `Fail`, or `Blocked` (give the reason in Notes). `Retired` is set by the plan owner only.
   - **Notes**: usability observations (what you did, what happened, why it was confusing or slow), even when the case passes, plus any questions.
   - **Evidence**: links to your screenshots or recordings, separated by `, `. Upload each file to the evidence folder the team shares with you, named `<case base ID>-<YYYYMMDD>-<n>.<ext>` (run date, then a counter), for example `PR02-FR004-03-20261019-1.png`, so a retest never overwrites earlier files. Record only the links; do not send files with the batch.
   - **Bug status**: set `Found` when you see a bug; otherwise leave `—`.
   - **Last tested**: the date you ran the case, `YYYY-MM-DD`.
4. The team fills **Bug ID** and moves Bug status to `Logged`, `Fixed - retest`, `Closed`, or `Reopened`. When you retest a `Fixed - retest` case, update only the result columns.
5. Do not edit IDs (keep the ` r1` suffix), titles, preconditions, test data, steps, or expected results, and do not use the vertical-bar character inside cells. Put questions or proposed changes in **Notes**.
6. Keep each case row on one physical line. For a line break inside a cell, type `<br>`; pressing Enter splits the row and the file is rejected.

## Flow Overview

- **View (FR-015 › Tab 7).** The admin opens a provider in Provider Management and selects the Commission & Financials tab. The current design may label this tab "Affiliate Pay Details"; the PRD calls this a legacy label, so either label is acceptable. The tab shows Commission Model, Commission Value, Payout Frequency, Flat Rate Currency (Flat Rate only), Effective Date, Featured Provider (display only), a Current Configuration summary that says existing bookings keep their confirmation-time snapshot, a Scheduled Configuration (hidden when none is pending), and Commission History.
- **Edit (FR-015 › Tab 7 Business Rules; Screen 3 Admin change reason).** Editing needs a "Reason for change" of 10 to 500 characters and password re-entry (MVP re-authentication). Commission Value is 0 to 100 with 0.1% precision for Percentage, or greater than 0 for Flat Rate. The Effective Date is DD-MM-YYYY and must be today or later. An Effective Date of today applies at once. A future date is saved as the single Scheduled Configuration, and the Current Configuration stays as it is. A Payout Frequency change takes effect from the next billing cycle. Every change is logged in Commission History (date, admin user, old value, new value, reason) and in Tab 8 Activity Log.
- **Cancel scheduled change.** "Cancel Scheduled Configuration" needs a change reason and re-authentication. Afterwards the Scheduled Configuration is hidden.
- **Provider view (FR-032 › Screen 4).** The provider Owner sees these values read-only in the Billing tab's Commission & Payout panel. B06 checks this between A02-FR015-26 and A02-FR015-28.

## Shared Preconditions

- Run this batch after B01, so its commission changes cannot affect B01 and B02 figures. B02 and B01 statements are already generated and keep their booking-time snapshot.
- Run A02-FR015-24 to A02-FR015-27 first, then B06 PR06-FR032-17, then A02-FR015-28.
- Sign in as `{A1}` (super admin). Keep the `{A1}` password ready for re-authentication.
- **Team-prepared setup (before the session):**
  - `{V1}` is Active with Percentage 15%, Payout Frequency Weekly, and no Scheduled Configuration.
  - `{V2}` is Active with Flat Rate €150 (Flat Rate Currency EUR, an enabled currency per FR-029 Screen 5), Payout Frequency Monthly, and no Scheduled Configuration. Its quotes and bookings are in GBP, the system default currency; EUR is its payout currency and the currency of its Flat Rate only.
  - Neither `{V1}` nor `{V2}` is in an FR-029 commission scope shared with other providers, so no split warning appears. Record each provider's starting Effective Date in the setup reference list.
- **End state (restore before closing the batch):** `{V1}` 15% Weekly and `{V2}` €150 Monthly, with no Scheduled Configuration on either. A02-FR015-27 and A02-FR015-28 restore these values; the tester confirms them in the last step of A02-FR015-28.

## Test Data Sets

| Data set | Purpose | Values | Account |
|---|---|---|---|
| P3-DS-A02-01 | Invalid edits that must not save | Commission Value 100.1, then -1; Effective Date yesterday's date; Reason "Too short" (9 characters), then a reason of 501 characters; valid reason "Checking validation on the commission form" with a wrong password "WrongPass-123" | `{A1}` on `{V1}` |
| P3-DS-A02-02 | Future-dated change | Commission Model Percentage; Commission Value 12; Effective Date today + 30 days (DD-MM-YYYY); Reason "Scheduled rate review agreed with the provider for next month" | `{A1}` on `{V1}` |
| P3-DS-A02-03 | Immediate Flat Rate change and restore | Commission Value €175, Effective Date today, Reason "Temporary flat fee test on the admin commission form"; then €150, Effective Date today, Reason "Restore the agreed flat fee after the commission test" | `{A1}` on `{V2}` |
| P3-DS-A02-04 | Payout Frequency change and restore | Payout Frequency "2x a Month", Reason "Provider asked to be paid twice a month from next cycle"; then "Monthly", Reason "Restore the monthly payout schedule after the test" | `{A1}` on `{V2}` |
| P3-DS-A02-05 | Cancel the scheduled change | Reason "Scheduled rate review withdrawn after the provider call" | `{A1}` on `{V1}` |

## Test Cases

| ID | Title | Priority | PRD flow ref | Preconditions | Test data | Steps | Expected result | Actual result / data | Result | Notes | Evidence | Bug ID | Bug status | Last tested |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A02-FR015-24 r1 | Admin views commission and payout settings for a percentage and a flat-rate provider | High | FR-015 › Tab 7 Data Fields and Business Rules | Signed in as `{A1}`; team setup for `{V1}` and `{V2}` in place | `{V1}` (15%, Weekly); `{V2}` (€150, Monthly) | 1. Go to Provider Management and open `{V1}`.<br>2. Select the Commission & Financials tab (may be labelled "Affiliate Pay Details").<br>3. Read every field, the Current Configuration, and Commission History.<br>4. Open `{V2}` and repeat steps 2 and 3. | 1. (after step 1) `{V1}`'s details open.<br>2. (after step 2) The tab opens; no affiliate data is shown.<br>3. (after step 3) Commission Model "Percentage", Commission Value 15%, Payout Frequency "Weekly", Effective Date in DD-MM-YYYY matching the setup reference list, Featured Provider shown as display only, Current Configuration like "15% · Paid Weekly (Mon–Sun)" with a note that existing bookings keep their confirmation-time snapshot. No Scheduled Configuration is shown. Commission History entries show date, admin user, old value, new value, and reason.<br>4. (after step 4) `{V2}` shows Commission Model "Flat Rate", Commission Value €150, Flat Rate Currency EUR, Payout Frequency "Monthly", and a Current Configuration like "€150 per completed procedure · Paid Monthly". | | Not tested | | | | — | |
| A02-FR015-25 r1 | Invalid commission edits are rejected and nothing is saved | High | FR-015 › Tab 7 Data Fields (Commission Value, Effective Date); Business Rules (re-authentication); Screen 3 Admin change reason | Run after A02-FR015-24. Signed in as `{A1}` on `{V1}`'s Commission & Financials tab | P3-DS-A02-01 | 1. Start editing the commission settings. Enter Commission Value 100.1 with a valid reason and Effective Date today, then try to save.<br>2. Change Commission Value to -1 and try to save.<br>3. Set Commission Value 15, set Effective Date to yesterday, and try to save.<br>4. Set Effective Date to today and Reason "Too short", then try to save.<br>5. Paste a 501-character reason and try to save.<br>6. Enter the valid reason, try to save, and enter "WrongPass-123" when asked for the password.<br>7. Leave without saving and reload the tab. | 1. (after step 1) The value is rejected (Commission Value must be 0 to 100); nothing is saved. Note the message shown.<br>2. (after step 2) The value is rejected; nothing is saved. Note the message shown.<br>3. (after step 3) A past Effective Date is rejected; nothing is saved. Note the message shown.<br>4. (after step 4) The reason is rejected for being under 10 characters. Note the message shown.<br>5. (after step 5) The reason is rejected or cut off at 500 characters. Note which.<br>6. (after step 6) A password prompt appears; the wrong password is refused and nothing is saved. Note the message shown.<br>7. (after step 7) Values are unchanged (15%, Weekly), no Scheduled Configuration appears, and Commission History has no new entry. | | Not tested | | | | — | |
| A02-FR015-26 r1 | Future-dated commission change is saved as the Scheduled Configuration | High | FR-015 › Tab 7 Business Rules (Scheduled configuration; re-authentication; history) | Run after A02-FR015-25. Signed in as `{A1}` on `{V1}`'s Commission & Financials tab | P3-DS-A02-02 | 1. Start editing. Enter Commission Value 12, Effective Date today + 30 days, and the reason, then save.<br>2. Enter the `{A1}` password when asked.<br>3. Read the Current Configuration, Scheduled Configuration, and Commission History.<br>4. Open Tab 8 Activity Log and find the newest entry. | 1. (after step 1) A password prompt appears.<br>2. (after step 2) The change saves. Note the message shown.<br>3. (after step 3) Current Configuration still shows 15% · Paid Weekly. Scheduled Configuration shows Percentage 12% from the entered Effective Date, with a "Cancel Scheduled Configuration" action. Commission History has a new entry with today's date, `{A1}`, old value 15%, new value 12% with its Effective Date, and the reason.<br>4. (after step 4) A commission change entry shows the timestamp, `{A1}`, the changed fields, and an IP address. Leave the Scheduled Configuration in place for B06 PR06-FR032-17. | | Not tested | | | | — | |
| A02-FR015-27 r1 | Immediate flat-rate and payout frequency changes apply, are logged, and are restored | High | FR-015 › Tab 7 Business Rules (Effective Date today applies immediately; payout frequency from next cycle; history); Tab 8 | Run after A02-FR015-26. Signed in as `{A1}` | P3-DS-A02-03; P3-DS-A02-04 | 1. Open `{V2}`'s Commission & Financials tab. Change Commission Value to 175 with Effective Date today and the first P3-DS-A02-03 reason; save and enter the password.<br>2. Read the Current Configuration and Scheduled Configuration.<br>3. Change Commission Value back to 150 with Effective Date today and the restore reason; save and enter the password.<br>4. Change Payout Frequency to "2x a Month" with the first P3-DS-A02-04 reason; save and enter the password.<br>5. Change Payout Frequency back to "Monthly" with the restore reason; save and enter the password.<br>6. Read Commission History and Tab 8 Activity Log. | 1. (after step 1) The change saves after the password.<br>2. (after step 2) Current Configuration shows €175 per completed procedure; no Scheduled Configuration is shown, because a change dated today applies at once.<br>3. (after step 3) Current Configuration shows €150 per completed procedure.<br>4. (after step 4) Payout Frequency shows "2x a Month". Note any message about the change starting from the next billing cycle.<br>5. (after step 5) Payout Frequency shows "Monthly" and Current Configuration reads like "€150 per completed procedure · Paid Monthly".<br>6. (after step 6) Commission History has four new entries in order (150 to 175, 175 to 150, Monthly to 2x a Month, 2x a Month to Monthly), each with today's date, `{A1}`, old and new values, and its reason. Tab 8 has a matching entry for each change with an IP address. | | Not tested | | | | — | |
| A02-FR015-28 r1 | Admin cancels the scheduled commission change with reason and re-authentication | High | FR-015 › Tab 7 Data Fields (Scheduled Configuration, cancel action); Business Rules | Run after B06 PR06-FR032-17. Signed in as `{A1}` on `{V1}`'s Commission & Financials tab; Scheduled Configuration from A02-FR015-26 shown | P3-DS-A02-05 | 1. Select "Cancel Scheduled Configuration" and confirm without entering a reason.<br>2. Enter the reason and confirm.<br>3. Enter the `{A1}` password when asked.<br>4. Read the tab and Commission History.<br>5. Open `{V2}`'s tab and read its values. | 1. (after step 1) The cancel is not accepted without a reason. Note the message shown.<br>2. (after step 2) A password prompt appears.<br>3. (after step 3) The cancel completes. Note the message shown.<br>4. (after step 4) The Scheduled Configuration is no longer shown. Current Configuration still shows 15% · Paid Weekly. Commission History has an entry for the cancellation with `{A1}`, the cancelled 12% configuration, and the reason.<br>5. (after step 5) `{V2}` shows €150, Monthly, and no Scheduled Configuration. The end state matches Shared Preconditions. | | Not tested | | | | — | |

## Batch Summary

| Total | Pass | Fail | Blocked | Not tested | Open bugs |
|---|---|---|---|---|---|
| 5 | 0 | 0 | 0 | 5 | 0 |

## Case Change Log

| Case | Revision | Date | Change |
|---|---|---|---|
| A02-FR015-24 | r1 | 2026-10-19 | Created |
| A02-FR015-25 | r1 | 2026-10-19 | Created |
| A02-FR015-26 | r1 | 2026-10-19 | Created |
| A02-FR015-27 | r1 | 2026-10-19 | Created |
| A02-FR015-28 | r1 | 2026-10-19 | Created |
