# B06 — PR-06 Billing Settings

## Batch Control

| Field | Value |
|---|---|
| Batch | B06 |
| Phase / plan version | Phase 3 / v1.0 |
| Module | PR-06 — Profile & Settings (Provider), billing settings slice |
| FRs | FR-032 Screen 4 (primary); FR-015 Tab 7 and FR-009 cited where touched |
| PRD sources | [FR-032 › Main Flow: Manage Billing Settings (Owner Role Only)](../../../../../../project-requirements/functional-requirements/fr032-provider-dashboard-settings/prd.md#main-flow-manage-billing-settings-owner-role-only); [FR-032 › Alternative Flows A9, B9, B10](../../../../../../project-requirements/functional-requirements/fr032-provider-dashboard-settings/prd.md#main-flow-manage-billing-settings-owner-role-only); [FR-032 › Screen 4: Billing Settings (Owner Role Only)](../../../../../../project-requirements/functional-requirements/fr032-provider-dashboard-settings/prd.md#screen-4-billing-settings-owner-role-only); [FR-015 › Tab 7: Commission & Financials (Admin-Only)](../../../../../../project-requirements/functional-requirements/fr015-provider-management/prd.md#tab-7-commission--financials-admin-only) |
| Platform | Provider dashboard |
| Tester | |
| Build tested | |

## How to Fill In This File

1. Before starting, fill **Tester** and **Build tested** in Batch Control.
2. Run cases in table order unless a case says otherwise.
3. In each case row, fill only these columns:
   - **Actual result / data**: what you observed and the exact values you entered, for example "Saved; status shows Draft; total 2,450 GBP".
   - **Result**: `Not tested`, `Pass`, `Fail`, or `Blocked` (give the reason in Notes). `Retired` is set by the plan owner only.
   - **Notes**: usability observations (what you did, what happened, why it was confusing or slow), even when the case passes, plus any questions.
   - **Evidence**: screenshot or recording file names, named `<case ID>-<n>`, for example `PR02-FR004-03-1.png`. Send the files with the batch.
   - **Bug status**: set `Found` when you see a bug; otherwise leave `—`.
   - **Last tested**: the date you ran the case, `YYYY-MM-DD`.
4. The team fills **Bug ID** and moves Bug status to `Logged`, `Fixed - retest`, `Closed`, or `Reopened`. When you retest a `Fixed - retest` case, update only the result columns.
5. Do not edit IDs (keep the ` r1` suffix), titles, preconditions, test data, steps, or expected results, and do not use the vertical-bar character inside cells. Put questions or proposed changes in **Notes**.

## Flow Overview

- **Access (FR-032 › Screen 4; B9).** Billing settings are at Settings & Support > Settings > Billing tab. Only the Owner can see the tab. For Manager, Clinical Staff, and Billing Staff roles it is hidden from navigation.
- **View and edit (FR-032 › Main Flow: Manage Billing Settings).** The Owner sees Account Holder Name, Bank Name, Account Number masked like ●●●●●●1234, Routing/SWIFT Code, and IBAN when applicable. "Edit Bank Account Details" opens an editable form with the account number unmasked. "Save Bank Account" validates the details (S-02) and shows "Bank account details saved successfully".
- **First bank account (A9).** With no bank account on file, the tab shows "No bank account on file. Add your bank account details to receive payouts." After a valid save it shows "Bank account added successfully. You will now receive payouts to this account."
- **Validation (Screen 4 Data Fields; B10).** Account Holder Name is required (letters and spaces only, at most 200 characters). SWIFT is 8 to 11 characters and US routing is 9 digits. An invalid Turkish IBAN "TR1234" shows "Invalid IBAN format. Turkey IBAN must be 26 characters (e.g., TR12 0001 0012 3456 7890 1234 56)".
- **Commission & Payout panel (Screen 4).** A read-only panel shows Commission Model, Commission Value, Effective Date, Scheduled Configuration (hidden when none is pending), and Payout Frequency, set by admins in FR-015 Tab 7. It says existing confirmed bookings keep their confirmation-time commission snapshot, and that changes go through support.

## Shared Preconditions

- Run PR06-FR032-17 after B05 A02-FR015-26 (the `{V1}` Scheduled Configuration must exist) and before B05 A02-FR015-28. Run the other cases after B01 and B02.
- `{V1}` has a saved bank account (it receives payouts in B02). Its last four account digits are in the setup reference list.
- `{V3}` has no bank account on file. This is the B02 setup for ST-3, and PR06-FR032-20 adds it, so run PR06-FR032-19 and PR06-FR032-20 only after B02 and B01 are complete.
- `{S1}` (Clinical Staff), `{S3}` (Manager), and `{S4}` (Billing Staff) are staff at `{V1}` and can sign in.
- **Team-prepared setup (before the session):** valid Stripe test-mode bank details for `{V3}` (Account Holder Name in letters and spaces only, Bank Name, Account Number, Routing/SWIFT Code, and IBAN if the bank country needs one), listed in the setup reference list.
- **End state:** `{V3}` has a bank account on file. `{V1}`'s bank account is unchanged.

## Test Data Sets

| Data set | Purpose | Values | Account |
|---|---|---|---|
| P3-DS-PR06-01 | Invalid bank details that must not save | IBAN "TR1234"; Account Holder Name empty; SWIFT "ABC"; Account Holder Name "Clinic 24" | `{V3}` owner |
| P3-DS-PR06-02 | Valid first bank account | The team-supplied `{V3}` Stripe test bank details from the setup reference list | `{V3}` owner |

## Test Cases

| ID | Title | Priority | PRD flow ref | Preconditions | Test data | Steps | Expected result | Actual result / data | Result | Notes | Evidence | Bug ID | Bug status | Last tested |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PR06-FR032-17 r1 | Owner views masked bank details and the read-only commission panel with a scheduled change | High | FR-032 › Main Flow: Manage Billing Settings, steps 1 to 5; Screen 4 Business Rules and Commission & Payout panel; FR-015 › Tab 7 Business Rules (Scheduled configuration) | Run after B05 A02-FR015-26 and before A02-FR015-28. Signed in as the `{V1}` owner | `{V1}` last four account digits from the setup reference list; B05 Scheduled Configuration 12% from today + 30 days | 1. Go to Settings & Support > Settings and select the Billing tab.<br>2. Read the bank account details.<br>3. Select "Edit Bank Account Details" and read the Account Number.<br>4. Leave the form without saving, then reopen the Billing tab.<br>5. Read the Commission & Payout panel and try to change any of its values. | 1. (after step 1) The Billing tab opens with the saved bank account.<br>2. (after step 2) Account Holder Name, Bank Name, Routing/SWIFT Code, and IBAN (if used) are shown. The Account Number is masked like ●●●●●●1234 with the expected last four digits.<br>3. (after step 3) An editable form opens with the full Account Number unmasked.<br>4. (after step 4) The saved details are unchanged and the Account Number is masked again. Note how the form is closed without saving and any message shown.<br>5. (after step 5) The panel shows Commission Model "Percentage", Commission Value 15%, the Effective Date in DD-MM-YYYY, Scheduled Configuration 12% with its Effective Date, and Payout Frequency "Weekly" (Mon–Sun). It notes that existing confirmed bookings keep their commission snapshot and that changes go through support. None of the panel values can be edited. | | Not tested | | | | — | |
| PR06-FR032-18 r1 | Non-Owner staff roles cannot see the Billing tab | High | FR-032 › B9: Non-Owner Role Attempts to Access Billing Settings; Screen 4 Business Rules | Run after PR06-FR032-17. `{S1}`, `{S3}`, and `{S4}` can sign in | `{S1}` Clinical Staff; `{S3}` Manager; `{S4}` Billing Staff | 1. Sign in as `{S1}` and go to Settings & Support > Settings.<br>2. Sign out, sign in as `{S3}`, and repeat step 1.<br>3. Sign out, sign in as `{S4}`, and repeat step 1. | 1. (after step 1) No Billing tab is shown and no bank account details are visible.<br>2. (after step 2) No Billing tab is shown.<br>3. (after step 3) No Billing tab is shown, even though `{S4}` can see the financial screens in B01. | | Not tested | | | | — | |
| PR06-FR032-19 r1 | First-time empty state and invalid bank details are rejected | High | FR-032 › A9 steps 1 and 2; B10: Invalid Bank Account Format; Screen 4 Data Fields | Run after B02 and B01. Signed in as the `{V3}` owner; `{V3}` has no bank account on file | P3-DS-PR06-01; P3-DS-PR06-02 | 1. Go to Settings & Support > Settings and select the Billing tab.<br>2. Fill every field with the P3-DS-PR06-02 values, but enter IBAN "TR1234", then select "Save Bank Account".<br>3. Restore the valid IBAN (or clear it if the bank does not need one), clear Account Holder Name, and save.<br>4. Restore Account Holder Name, enter SWIFT "ABC", and save.<br>5. Restore the SWIFT or routing code, enter Account Holder Name "Clinic 24", and save.<br>6. Leave the form without saving and reopen the Billing tab. | 1. (after step 1) An empty billing form shows "No bank account on file. Add your bank account details to receive payouts."<br>2. (after step 2) The error "Invalid IBAN format. Turkey IBAN must be 26 characters (e.g., TR12 0001 0012 3456 7890 1234 56)" is shown and nothing is saved.<br>3. (after step 3) The form shows that Account Holder Name is required and nothing is saved. Note the message shown.<br>4. (after step 4) The SWIFT code is rejected (8 to 11 characters) and nothing is saved. Note the message shown.<br>5. (after step 5) The name is rejected (letters and spaces only) and nothing is saved. Note the message shown.<br>6. (after step 6) The "No bank account on file" message is still shown. | | Not tested | | | | — | |
| PR06-FR032-20 r1 | Owner adds a first bank account and sees it masked | High | FR-032 › A9: Provider Owner Adds Bank Account for First Time; Main Flow steps 8 to 13; Screen 4 Business Rules | Run after PR06-FR032-19. Signed in as the `{V3}` owner | P3-DS-PR06-02 | 1. On the Billing tab, enter all P3-DS-PR06-02 values and select "Save Bank Account".<br>2. Reload the page and reopen the Billing tab. | 1. (after step 1) "Bank account added successfully. You will now receive payouts to this account." is shown.<br>2. (after step 2) The saved details are shown, with the Account Number masked like ●●●●●●1234 and the correct last four digits. The "No bank account on file" message no longer appears. | | Not tested | | | | — | |

## Batch Summary

| Total | Pass | Fail | Blocked | Not tested | Open bugs |
|---|---|---|---|---|---|
| 4 | 0 | 0 | 0 | 4 | 0 |

## Case Change Log

| Case | Revision | Date | Change |
|---|---|---|---|
| PR06-FR032-17 | r1 | 2026-10-19 | Created |
| PR06-FR032-18 | r1 | 2026-10-19 | Created |
| PR06-FR032-19 | r1 | 2026-10-19 | Created |
| PR06-FR032-20 | r1 | 2026-10-19 | Created |
