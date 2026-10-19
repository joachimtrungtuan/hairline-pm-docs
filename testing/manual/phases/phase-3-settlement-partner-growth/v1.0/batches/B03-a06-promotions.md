# B03 — A-06 Promotions and Discounts

## Batch Control

| Field | Value |
|---|---|
| Batch | B03 |
| Phase / plan version | Phase 3 / v1.0 |
| Module | A-06 — Discount & Promotion Management |
| FRs | FR-019 (primary); FR-017 and FR-018 cited where touched |
| PRD sources | [FR-019 › Business Workflows (Main Flow, Alternative Flows)](../../../../../../project-requirements/functional-requirements/fr019-promotions-discounts/prd.md#main-flow-admin-creates-platform-discount-bothfees); [FR-019 › Admin Platform Screens (A-06), Screens 1–6](../../../../../../project-requirements/functional-requirements/fr019-promotions-discounts/prd.md#admin-platform-screens-a-06); [FR-019 › Business Rules](../../../../../../project-requirements/functional-requirements/fr019-promotions-discounts/prd.md#general-module-rules) |
| Platform | Admin dashboard (provider dashboard used only to confirm the provider side) |
| Tester | |
| Build tested | |

## How to Fill In This File

1. Run cases in table order unless a case says otherwise.
2. Fill only: **Actual result / data**, **Result**, **Notes**, **Evidence**, **Bug status**, **Last tested**.
3. **Result** values: `Not tested`, `Pass`, `Fail`, `Blocked`. **Bug status** values: `—`, `Found`, `Logged`, `Fixed - retest`, `Closed`, `Reopened` (set `Found` when you see a bug; the team logs it in Plane).
4. Put usability observations in **Notes**: what you did, what happened, and why it was confusing or slow, even when the case passes.
5. Do not edit IDs, steps, or expected results, and do not use the vertical-bar character inside cells. Put questions in **Notes**.

## Flow Overview

This batch tests how Hairline admins run promotions across the marketplace (FR-019).

- **Three program types.** (1) Admin-via-Provider programs, where Hairline and the provider share the discount ("Both Fees"); providers must accept them before they can use them (FR-019 › Main Flow: Admin Creates Platform Discount). (2) Provider Self-Created programs, which admins can see and govern but not normally edit. (3) Hairline-Funded and Direct-Issued codes, which Hairline pays for alone and distributes as open, affiliate-bound, segment-bound, or individual codes.
- **Lifecycle.** A program moves forward only: Draft, Active, Paused, Expired, Archived. Pausing stops new use but keeps terms already sent on quotes. Terms are copied onto a quote when it is sent and frozen when the patient accepts it.
- **Adoption.** The Provider Adoption Manager shows each targeted provider's decision; admins can re-invite, force-revoke, or mark a provider exempt, always with a reason.
- **Applications.** Every use is tracked as Applied (accepted) and then Completed (first payment). Admins can only Reverse or Refund a Completed use, with a reason, and this feeds finance reconciliation (FR-017). Nothing can void or replace an Applied use.

Run this batch before B01 so the provider-side promotion cases have an admin campaign to act on. The roadmap gap for A-06 is that lifecycle and adoption actions must reach live contracts and the provider portfolio must not show fixture data; cases A06-FR019-06, -07, and -09 check this.

## Shared Preconditions

- Phase 2 exit gate passed; Admin dashboard reachable; `{A1}` can sign in and open Promotions.
- `{V1}` and `{V2}` are active providers; `{V1}` can sign in to the Provider dashboard to confirm provider-side effects.
- The team has prepared, as setup, at least one sent quote and one paid booking that used a promotion, so Applied and Completed rows exist (patient actions done by the team).
- At least two active affiliates exist (from B04 or prepared by the team) for affiliate-bound codes.

## Test Data Sets

| Data set | Purpose | Values | Account |
|---|---|---|---|
| DS-A06-01 | Valid Admin-via-Provider (Both Fees) program | Program Name "Phase3 Spring Both Fees"; Description up to 1000 characters; Discount Type Percentage; Value 20; Applies To "Treatment cost only"; Code "P3SPRING20"; Application Mode "Code-only entry"; Start today, End today plus 30 days; Total Usage Limit 50; Per-User Usage Limit 1; Hairline Share % 50; Target Providers explicit list `{V1}`, `{V2}`; Auto-Decline Window 3 days | `{A1}` |
| DS-A06-02 | Program Name and Description boundaries | Names: "AB" (2, invalid); "ABC" (3, valid); 120 characters (valid); 121 characters (invalid). Description: 1000 characters (valid); 1001 characters (invalid) | `{A1}` |
| DS-A06-03 | Invalid values | Hairline Share %: blank, -1, 101 (invalid); 0 and 100 (valid). End date one day before Start date (invalid). Total Usage Limit -1 (invalid), 0 (valid), blank (unlimited). Application Mode "Auto-applied" on Both Fees (invalid) | `{A1}` |
| DS-A06-04 | Duplicate code | "SPRINGPRP10" (created by `{V1}` in B01) or any existing provider or admin code | `{A1}` |
| DS-A06-05 | Hairline-Funded open code program | Program Name "Phase3 Open Welcome"; Fixed amount 50 in USD; Issuance Channel "Open code"; Code "P3WELCOME50"; Total Usage Limit 100 | `{A1}` |
| DS-A06-06 | Bulk generate quantities | 0 (invalid); 1 (valid); 25 (valid); 10,000 (upper boundary, valid where the program total limit allows); 10,001 (invalid) | `{A1}` |
| DS-A06-07 | Reasons | Empty (invalid); "Campaign ended early by marketing decision" (valid) | `{A1}` |
| DS-A06-08 | Redemptions | One Completed redemption (booking paid) and one Applied redemption (accepted, not yet paid), prepared by the team on a `{V1}` quote | `{A1}` |

## Test Cases

| ID | Title | Priority | PRD flow ref | Preconditions | Test data | Steps | Expected result | Actual result / data | Result | Notes | Evidence | Bug ID | Bug status | Last tested |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A06-FR019-01 r1 | Promotion Program Hub lists live programs with search and filters | High | FR-019 › Screen 1: Admin — Promotion Program Hub | Signed in as `{A1}` | DS-A06-01 | 1. Open the Promotion Program Hub.<br>2. Check the default sort and Result Count.<br>3. Type 1 character in search, then 2 characters.<br>4. Filter by Program Type, Status, and Funding Model one at a time.<br>5. Clear filters. | 1. Hub loads with real programs only; no sample or fixture rows.<br>2. Sorted by Last Updated, newest first; Result Count matches the rows.<br>3. Search starts only from 2 characters.<br>4. Each filter returns only matching programs and updates Result Count.<br>5. Full list returns. | | Not tested | | | | — | |
| A06-FR019-02 r1 | Create a Both Fees program and send it to target providers | High | FR-019 › Main Flow: Admin Creates Platform Discount (Both-Fees); Screen 2 Acceptance Criteria 1 and 5 | Signed in as `{A1}` | DS-A06-01 | 1. Create a new Admin-via-Provider program.<br>2. Check which fields are shown and the Funding Model value.<br>3. Fill DS-A06-01 and save.<br>4. Open the Audit Trail Panel.<br>5. Sign in as `{V1}` and open Admin Campaigns. | 1. Form opens.<br>2. Funding Model is set to "Both Fees" automatically and cannot be changed; Hairline Share %, Target Providers, Approval Routing, and Auto-Decline Window are shown; Issuance Channel is hidden.<br>3. Program saves and enters "Pending Approval"; a success message is shown.<br>4. Creation is listed with actor and timestamp, including Hairline Share % 50.<br>5. The program is in the Pending tab with its terms, including the Hairline share. | | Not tested | | | | — | |
| A06-FR019-03 r1 | Program form rejects invalid lengths, dates, limits, and shares | High | FR-019 › Screen 2 Common Data Fields and Acceptance Criterion 5 | Signed in as `{A1}`; new Admin-via-Provider form open | DS-A06-02, DS-A06-03 | 1. Try each invalid Program Name and Description value and save.<br>2. Try the valid boundary values.<br>3. Set End before Start and save.<br>4. Set Total Usage Limit -1, then 0, then blank.<br>5. Try Hairline Share % blank, -1, 101, then 0 and 100. | 1. Each invalid value is blocked with an inline message next to the field.<br>2. Boundary values are accepted.<br>3. Save is blocked; message says End must be on or after Start.<br>4. -1 is blocked; 0 is accepted; blank is accepted as unlimited.<br>5. Blank, -1, and 101 are blocked inline; 0 and 100 are accepted. | | Not tested | | | | — | |
| A06-FR019-04 r1 | Auto-applied mode is refused for Both Fees programs | High | FR-019 › Screen 2 Acceptance Criterion 4 | Signed in as `{A1}` | DS-A06-01, DS-A06-03 | 1. Open a new Admin-via-Provider program with DS-A06-01 values.<br>2. Set Application Mode "Auto-applied" and save. | 1. Form is filled.<br>2. Save is rejected with the inline message "Auto-applied is not permitted for Both-Fees programs." and entered values are kept. | | Not tested | | | | — | |
| A06-FR019-05 r1 | Codes must be unique across the platform | High | FR-019 › Screen 2 (Code(s) uniqueness); Screen 8 Business Rules | Signed in as `{A1}` | DS-A06-04 | 1. On a new program enter the existing provider code and save.<br>2. Enter it in a different letter case and save. | 1. Save is blocked with a message that the code is already in use.<br>2. Save is still blocked (record in Notes whether the check ignores case). | | Not tested | | | | — | |
| A06-FR019-06 r1 | Lifecycle moves forward only and pausing keeps sent terms | High | FR-019 › Screen 1 row actions; Screen 2 Lifecycle State; Screen 2 Acceptance Criterion 3 | Signed in as `{A1}`; an Active program with a quote already sent using it (DS-A06-08) | DS-A06-07, DS-A06-08 | 1. In the Hub choose Pause on the Active program.<br>2. Open the quote already sent with this program.<br>3. Choose Resume, then Archive.<br>4. Look for Resume or Activate on the Archived program.<br>5. Open the Audit Trail Panel. | 1. Status becomes "Paused" after confirmation.<br>2. The sent quote still shows the original discount terms.<br>3. Status returns to "Active", then becomes "Archived".<br>4. No action moves an Archived program backwards.<br>5. Each change is listed with actor, timestamp, and reason. | | Not tested | | | | — | |
| A06-FR019-07 r1 | Force-Revoke removes a program from a provider within 5 seconds | High | FR-019 › Screen 3: Admin — Provider Adoption Manager, Acceptance Criterion 1 | Signed in as `{A1}`; `{V1}` accepted the program (B01 PR05-FR019-01 or team setup) | DS-A06-01, DS-A06-07 | 1. Open View Adoptions for the program.<br>2. Read the `{V1}` and `{V2}` rows.<br>3. On `{V1}` choose Force-Revoke with an empty reason.<br>4. Enter the valid reason and confirm.<br>5. As `{V1}`, open the quote discount selection within 5 seconds. | 1. Adoption Manager opens with the Program Header.<br>2. Each row shows Provider, Status, Decided At, Decided By, Comment, Redemptions, Admin Actions.<br>3. Confirm is blocked; reason is required.<br>4. `{V1}` Status becomes "Revoked-by-Admin"; Decided By shows `{A1}`.<br>5. The program is no longer offered; quotes that already used it keep the discount. | | Not tested | | | | — | |
| A06-FR019-08 r1 | Re-invite a declined provider and mark a provider exempt | Medium | FR-019 › Screen 3 Business Rules (Re-invite, Mark Exempt) | Signed in as `{A1}`; `{V2}` Declined or Auto-Declined | DS-A06-07 | 1. On the `{V2}` row choose Re-invite and give a reason.<br>2. Sign in as `{V2}` and open Admin Campaigns.<br>3. Back as `{A1}`, choose Mark Exempt on a provider row with a reason. | 1. `{V2}` Status returns to "Pending".<br>2. The program is back in `{V2}`'s Pending tab.<br>3. Row shows the exempt outcome; the reason is in the audit trail. | | Not tested | | | | — | |
| A06-FR019-09 r1 | Provider Promotion Portfolio shows real records and allows governed pause | Medium | FR-019 › Screen 4: Admin — Provider Promotion Portfolio | Signed in as `{A1}`; `{V1}` has adopted and self-created programs; `{V2}` has no self-created programs | DS-A06-07 | 1. Open the portfolio for `{V1}`.<br>2. Read the KPI strip and filter Record Type "Self-Created".<br>3. Open a self-created program.<br>4. Pause it from the row action with an empty reason, then with the valid reason.<br>5. Open the portfolio for `{V2}`. | 1. Provider Header and Results Table load.<br>2. Adoption Rate, Self-Created Active Count, Total Redemptions, and Total Discount Issued are shown; only Self-Created rows remain.<br>3. Detail opens read-only.<br>4. Empty reason is blocked; with a reason the program becomes "Paused" and `{V1}` sees it as Paused.<br>5. An empty state is shown, with no sample programs. | | Not tested | | | | — | |
| A06-FR019-10 r1 | Create an open Hairline-funded code that providers never see | High | FR-019 › Screen 2 Acceptance Criterion 2; Screen 5 | Signed in as `{A1}` | DS-A06-05 | 1. Create a Hairline-Funded program with DS-A06-05 and publish it.<br>2. Check the fields shown on the form.<br>3. Open the Codes Manager for this program.<br>4. As `{V1}`, open Admin Campaigns. | 1. Program saves as Active.<br>2. Funding Model is "Hairline Only"; Issuance Channel is shown; Approval Routing and Hairline Share % are hidden.<br>3. Code "P3WELCOME50" is listed with Recipient Binding "Open" and Redemption Status "Unused".<br>4. The program does not appear in any tab. | | Not tested | | | | — | |
| A06-FR019-11 r1 | Bulk generate enforces the 1 to 10,000 range and creates unique codes | High | FR-019 › Screen 2 (Bulk Generate Codes) and Screen 5 | Signed in as `{A1}`; an Individually-issued Hairline-Funded program with no total limit | DS-A06-06 | 1. In the Codes Manager choose Bulk Generate with 0.<br>2. Try 10,001.<br>3. Generate 25.<br>4. Sort the Codes table by Code and check for duplicates.<br>5. Check Issued By and Issued At. | 1. Blocked with a range message.<br>2. Blocked with a range message.<br>3. 25 codes are created with a success message.<br>4. All 25 codes are different and status "Unused".<br>5. Issued By is `{A1}`; Issued At is the generation time. | | Not tested | | | | — | |
| A06-FR019-12 r1 | Bulk revoke needs a reason and keeps reserved uses | Medium | FR-019 › Screen 5 Business Rules (Bulk Revoke) | Signed in as `{A1}`; codes from A06-FR019-11, plus one In-Progress code prepared by the team | DS-A06-07 | 1. Select 3 Unused codes and the In-Progress code; choose Bulk Revoke with no reason.<br>2. Enter the valid reason and confirm.<br>3. Export the code list. | 1. Blocked; reason is required.<br>2. The Unused codes become "Revoked"; the In-Progress code keeps its reserved use (record exactly how it is shown).<br>3. The export lists the codes with their current Redemption Status. | | Not tested | | | | — | |
| A06-FR019-13 r1 | Applications log allows Reverse and Refund only on Completed rows | High | FR-019 › Screen 6 Tab 2 Acceptance Criteria 2 and 4; FR-017 reconciliation | Signed in as `{A1}` | DS-A06-08, DS-A06-07 | 1. Open Promotion Analytics & Applications, Applications tab.<br>2. Open the Applied row and check its actions.<br>3. On the Completed row choose Refund with no reason.<br>4. Enter the valid reason and confirm.<br>5. Search the FR-017 Audit Log (B02) for the booking. | 1. Rows show State, Status, Discount Value, Funding Split, Applied At, Completed At.<br>2. Only View Detail is offered; no void, remove, replace, or price change.<br>3. Blocked; reason is required.<br>4. Status becomes "Refunded"; accepted price and acceptance snapshot are unchanged.<br>5. A matching finance reconciliation record is visible. | | Not tested | | | | — | |
| A06-FR019-14 r1 | Overview KPIs reflect live redemptions and drill into Applications | Medium | FR-019 › Screen 6 Tab 1 (Overview) | Signed in as `{A1}` | DS-A06-08 | 1. Open the Overview tab.<br>2. Compare Total Redemptions for the last 30 days with the Applications tab count for the same range.<br>3. Click a KPI card. | 1. KPI cards load with real figures; no sample values.<br>2. Counts match.<br>3. The Applications tab opens filtered to that KPI. | | Not tested | | | | — | |
| A06-FR019-15 r1 | Admin can find, act, and recover in the promotion workflow | Low | FR-019 › Screens 1–3 (usability) | Signed in as `{A1}` | DS-A06-01, DS-A06-07 | 1. Without help, find which providers have not yet responded to "Phase3 Spring Both Fees".<br>2. Trigger one validation error on the program form and fix it.<br>3. Pause and resume a program and note the feedback shown. | 1. Path from the Hub to View Adoptions is clear; record clicks and time in Notes.<br>2. The error names the field and the rule; entered values are kept.<br>3. Each action shows a clear confirmation and the new status without a page reload. | | Not tested | | | | — | |

## Batch Summary

| Total | Pass | Fail | Blocked | Not tested | Open bugs |
|---|---|---|---|---|---|
| 15 | 0 | 0 | 0 | 15 | 0 |

## Case Change Log

| Case | Revision | Date | Change |
|---|---|---|---|
| A06-FR019-01 | r1 | 2026-10-19 | Created |
| A06-FR019-02 | r1 | 2026-10-19 | Created |
| A06-FR019-03 | r1 | 2026-10-19 | Created |
| A06-FR019-04 | r1 | 2026-10-19 | Created |
| A06-FR019-05 | r1 | 2026-10-19 | Created |
| A06-FR019-06 | r1 | 2026-10-19 | Created |
| A06-FR019-07 | r1 | 2026-10-19 | Created |
| A06-FR019-08 | r1 | 2026-10-19 | Created |
| A06-FR019-09 | r1 | 2026-10-19 | Created |
| A06-FR019-10 | r1 | 2026-10-19 | Created |
| A06-FR019-11 | r1 | 2026-10-19 | Created |
| A06-FR019-12 | r1 | 2026-10-19 | Created |
| A06-FR019-13 | r1 | 2026-10-19 | Created |
| A06-FR019-14 | r1 | 2026-10-19 | Created |
| A06-FR019-15 | r1 | 2026-10-19 | Created |
