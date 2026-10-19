# B04 — A-07 Affiliate Operations

## Batch Control

| Field | Value |
|---|---|
| Batch | B04 |
| Phase / plan version | Phase 3 / v1.0 |
| Module | A-07 — Affiliate Program Management |
| FRs | FR-018 (primary); FR-017 and FR-019 cited where touched |
| PRD sources | [FR-018 › Business Workflows](../../../../../../project-requirements/functional-requirements/fr018-affiliate-management/prd.md#business-workflows); [FR-018 › Admin Platform Screens (A-07), Screens 1–8](../../../../../../project-requirements/functional-requirements/fr018-affiliate-management/prd.md#admin-platform-screens-a-07); [FR-018 › Business Rules](../../../../../../project-requirements/functional-requirements/fr018-affiliate-management/prd.md#business-rules) |
| Platform | Admin dashboard |
| Tester | |
| Build tested | |

## How to Fill In This File

1. Run cases in table order unless a case says otherwise.
2. Fill only: **Actual result / data**, **Result**, **Notes**, **Evidence**, **Bug status**, **Last tested**.
3. **Result** values: `Not tested`, `Pass`, `Fail`, `Blocked`. **Bug status** values: `—`, `Found`, `Logged`, `Fixed - retest`, `Closed`, `Reopened` (set `Found` when you see a bug; the team logs it in Plane).
4. Put usability observations in **Notes**: what you did, what happened, and why it was confusing or slow, even when the case passes.
5. Do not edit IDs, steps, or expected results, and do not use the vertical-bar character inside cells. Put questions in **Notes**.

## Flow Overview

This batch tests how Hairline admins run the affiliate (referral partner) program (FR-018).

- **Onboarding (FR-018 › Main Flow: affiliate onboarding).** An admin adds an affiliate with contact, bank, and commission details. The affiliate starts as "Pending" with Activation Status "Invited" and receives a one-time activation link valid for 24 hours; the admin can resend it (at most 3 times per hour). Payouts are fixed: monthly on the 7th.
- **Codes (Main Flow: code creation; Alternative Flows A1 and A4).** Each affiliate code belongs to exactly one affiliate and discounts only Hairline's fees. Admins create one code, or one distinct code per affiliate in bulk; bulk results show created, skipped, and failed rows and failed rows can be retried. A margin guard stops a discount plus commission from exceeding Hairline's own commission.
- **Changes and exits (A2, B3, B5).** Commission changes need an effective date and never change past commission. Suspension is temporary, disables codes, and holds pending commission. Deactivation is permanent and settles the final balance: pay if at least $50, forfeit if below $50, write off if negative.
- **Payout visibility (Screens 7 and 8).** FR-018 calculates monthly commission and shows payout status read-only; money is moved in A-05 (B02, FR-017 Screen 6).

The affiliate's own portal (FR-018 Screens 9 and 10) is outside this phase's admin and provider scope and is not tested here. The roadmap gap for A-07 is that the UI must use live billing, lifecycle, and bulk-code data with no fixture metrics; cases A07-FR018-01, -12, and -14 check this.

## Shared Preconditions

- Phase 2 exit gate passed; Admin dashboard reachable; `{A1}` can sign in and open Affiliates.
- The team has prepared affiliates and referral bookings listed in **Test Data Sets** through real onboarding and real paid, completed bookings (patient actions and affiliate activation done by the team as setup).
- Activation email delivery can be checked by the team in the test mailbox; the tester records what the team confirms.
- Hairline's commission for the `{V1}` bookings used here is 15% (for the margin guard).

## Test Data Sets

| Data set | Purpose | Values | Account |
|---|---|---|---|
| DS-A07-01 | New affiliate, valid | Affiliate Name "Phase3 Hair Influencer"; Contact Email a new unique test address provided by the team; Country/Region United Kingdom; Affiliate Type Influencer; Account Holder Name, Bank Name, Account Number, Routing / SWIFT Code from the team's test bank set; Commission Type Percentage; Commission Percentage 10 | `{A1}` |
| DS-A07-02 | Commission boundaries | Percentage 4 (invalid), 5 (valid), 21 (valid with warning "High commission rate - please confirm business approval"), 25 (valid), 26 (invalid). Fixed Amount $49.99 (invalid), $50.00 (valid) | `{A1}` |
| DS-A07-03 | Invalid affiliate input | Contact Email already used by another affiliate; Affiliate Name with special characters "Hair@Promo!"; invalid IBAN "GB00TEST"; empty Account Holder Name | `{A1}` |
| DS-A07-04 | Active eligible affiliates | Two affiliates prepared by the team with Status "Active", Activation Status "Active", complete bank details and Commission Percentage 10 ("Affiliate A", "Affiliate B") | `{A1}` |
| DS-A07-05 | Ineligible affiliate | DS-A07-01 affiliate still "Pending" / "Invited"; one Active affiliate with incomplete bank details | `{A1}` |
| DS-A07-06 | Single code | Campaign Name "Phase3 Launch"; Discount Code "p3launch" (lowercase, saved as "P3LAUNCH"); "P3" (3 characters, invalid); 21 characters (invalid); duplicate "P3LAUNCH" in other case "p3Launch"; Discount Percentage 4 (invalid), 5, 30 (valid), 31 (invalid); Fixed Amount $9.99 (invalid), $10.00 (valid) | `{A1}` |
| DS-A07-07 | Margin guard | Affiliate commission 10% plus Discount Percentage 10% (sum 20%, above Hairline's 15%, blocked with shortfall 5%); Discount Percentage 5% with commission 10% (sum 15%, allowed); Fixed Amount discount $100 (review warning) | `{A1}` |
| DS-A07-08 | Reasons | Suspend and offboard reasons: 19 characters (invalid); 20 characters "Breach of brand rule" (valid); 501 characters (invalid) | `{A1}` |
| DS-A07-09 | Commission change | Affiliate A: new Percentage 12 with Effective Date yesterday (invalid), then the first day of next month (valid) | `{A1}` |
| DS-A07-10 | Offboarding balances | Three affiliates prepared by the team: net final balance $120.00 (Pay final balance); $30.00 (Forfeit, below $50); -$40.00 (Write off) | `{A1}` |
| DS-A07-11 | Payout cycle and refund reversal | Affiliate B with last month's cycle: 3 completed referral bookings, commissions $100.00, $150.00, $120.00; one of those bookings refunded after payout (reversal -$120.00 carried to the next payout); one affiliate below $50 rolled over; one Failed payout from B02 | `{A1}` |

## Test Cases

| ID | Title | Priority | PRD flow ref | Preconditions | Test data | Steps | Expected result | Actual result / data | Result | Notes | Evidence | Bug ID | Bug status | Last tested |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A07-FR018-01 r1 | Affiliate dashboard lists live affiliates with default sort and status badges | High | FR-018 › Screen 1: Affiliate Management Dashboard, Acceptance Criterion 1 | Signed in as `{A1}` | DS-A07-04, DS-A07-05 | 1. Open the Affiliate Management Dashboard.<br>2. Check sort order, result count, and page size.<br>3. Read the status badges.<br>4. Open "View Details" on Affiliate A and compare Total Referrals, Total Revenue, Total Commissions Paid, and Pending Payout. | 1. Dashboard loads with real affiliates only; no sample or fixture metrics.<br>2. Sorted by Total Revenue, highest first; result count shown; 25 per page.<br>3. Pending amber, Active green, Suspended red, Inactive gray.<br>4. The values on Affiliate Detail match the dashboard row. | | Not tested | | | | — | |
| A07-FR018-02 r1 | Filters combine across types and search finds affiliates | Medium | FR-018 › Screen 1 Acceptance Criterion 2 | Signed in as `{A1}` | DS-A07-04, DS-A07-05 | 1. Filter Status "Active" and "Pending" together.<br>2. Add Country/Region "United Kingdom".<br>3. Add the payout setup filter for incomplete details.<br>4. Clear filters and search by part of an affiliate name. | 1. Affiliates in either status are shown (OR within a filter).<br>2. Only Active or Pending affiliates in the UK remain (AND across filters).<br>3. Only the affiliate with incomplete bank details remains.<br>4. Matching affiliate is found. | | Not tested | | | | — | |
| A07-FR018-03 r1 | Add an affiliate; it starts Pending and Invited | High | FR-018 › Main Flow (onboarding); Screen 2: Add/Edit Affiliate Form | Signed in as `{A1}` | DS-A07-01, DS-A07-02 | 1. Choose to add an affiliate and fill DS-A07-01.<br>2. Read the commission preview and Payout Schedule.<br>3. Save.<br>4. Open the new affiliate's detail and the Account Details panel. | 1. Form accepts the values.<br>2. Preview reads like "For a $1,000 booking at 10% of booking revenue, affiliate earns $100"; Payout Schedule shows "Monthly on the 7th" and cannot be edited.<br>3. Affiliate is created with Status "Pending" and Activation Status "Invited"; the team confirms an activation email with a one-time link was sent and contains no password.<br>4. Account Number shows only the last 4 digits. | | Not tested | | | | — | |
| A07-FR018-04 r1 | Commission percentage and fixed amount limits are enforced | High | FR-018 › Screen 2 Data Fields (Commission Percentage, Commission Fixed Amount) and Notes | Signed in as `{A1}`; add form open | DS-A07-02 | 1. Enter Percentage 4 and save.<br>2. Enter 5, then 25.<br>3. Enter 21.<br>4. Enter 26 and save.<br>5. Switch to Fixed Amount and enter $49.99, then $50.00. | 1. Blocked with a message that the range is 5–25%.<br>2. Both accepted.<br>3. Accepted with warning "High commission rate - please confirm business approval".<br>4. Blocked.<br>5. $49.99 is blocked with a minimum $50 message; $50.00 is accepted. | | Not tested | | | | — | |
| A07-FR018-05 r1 | Invalid affiliate details are rejected | High | FR-018 › Screen 2 Business Rules (Email Uniqueness, validation) | Signed in as `{A1}`; add form open | DS-A07-03 | 1. Enter the existing Contact Email and save.<br>2. Enter the name with special characters.<br>3. Enter the invalid IBAN.<br>4. Leave Account Holder Name empty and save.<br>5. Edit an existing affiliate and try to change Contact Email. | 1. Blocked with a message that the email is already registered.<br>2. Blocked with a name rule message.<br>3. Blocked with an IBAN format message.<br>4. Blocked; field is marked required.<br>5. Contact Email cannot be changed after creation. | | Not tested | | | | — | |
| A07-FR018-06 r1 | Resend activation is limited to invited affiliates and rate-limited | Medium | FR-018 › Alternative Flow A5; Screen 3 Business Rules (Resend Activation) | Signed in as `{A1}`; A07-FR018-03 passed | DS-A07-01, DS-A07-04 | 1. On the new affiliate's detail, check the "Invited — activation pending" indicator.<br>2. Click "Resend Activation Email" 3 times.<br>3. Click it a 4th time within the hour.<br>4. Open Affiliate A (Active) and check the action. | 1. Indicator is shown.<br>2. Each click shows a confirmation; the team confirms that only the newest link works.<br>3. Blocked with a message about the 3-per-hour limit.<br>4. "Resend Activation Email" is disabled. | | Not tested | | | | — | |
| A07-FR018-07 r1 | Commission change requires a future effective date | High | FR-018 › Alternative Flow A2; Screen 3.2: Edit Commission Structure | Signed in as `{A1}` | DS-A07-09 | 1. On Affiliate A open "Edit Commission Structure".<br>2. Enter 12% with yesterday's date; tick the confirm box; submit.<br>3. Set the first day of next month; check that Submit needs the confirm box; submit.<br>4. Open the Activity / Audit Panel.<br>5. Check commissions already shown for past bookings. | 1. Modal opens.<br>2. Blocked with "Effective date cannot be in the past".<br>3. Submit stays disabled until "I confirm this commission change" is ticked; change is saved.<br>4. Entry shows `{A1}`, old 10%, new 12%, effective date.<br>5. Past commission amounts are unchanged. | | Not tested | | | | — | |
| A07-FR018-08 r1 | Suspend and reinstate an affiliate | High | FR-018 › Alternative Flow B3; Screen 3.1: Suspend / Reinstate Affiliate | Signed in as `{A1}` | DS-A07-04, DS-A07-08 | 1. On Affiliate B choose Suspend.<br>2. Enter the 19-character reason; tick "I confirm this action".<br>3. Enter the 501-character reason.<br>4. Enter the valid reason, tick the box, submit.<br>5. Open Promo Code Management filtered to Affiliate B and the Upcoming Payout panel.<br>6. Choose Reinstate. | 1. Modal shows a required reason and the confirm box; Submit is disabled.<br>2. Submit stays disabled or shows a minimum 20 characters message.<br>3. Input is limited at 500 characters.<br>4. Status becomes "Suspended" (red).<br>5. Affiliate B codes are disabled; pending commission is shown as held.<br>6. Status returns to "Active". | | Not tested | | | | — | |
| A07-FR018-09 r1 | Offboarding settles the final balance by amount | High | FR-018 › Alternative Flow B5; Screen 3.3: Deactivate / Offboard Affiliate | Signed in as `{A1}` | DS-A07-10, DS-A07-08 | 1. On the $120.00 affiliate choose "Deactivate / Offboard"; read Final Balance Summary and Settlement Outcome.<br>2. Enter the valid reason, tick "I confirm this affiliate will be permanently deactivated", submit.<br>3. Repeat for the $30.00 and -$40.00 affiliates.<br>4. On any offboarded affiliate look for Reinstate.<br>5. Check the Activity / Audit Panel. | 1. Summary shows gross pending, reversals, and net $120.00; outcome "Pay final balance".<br>2. Status becomes "Inactive" (gray); all codes disabled; balance queued for payout.<br>3. Outcomes are "Forfeit (below $50)" and "Write off (negative)"; both become "Inactive".<br>4. No Reinstate is offered.<br>5. Forfeit and write-off each have an audit entry. | | Not tested | | | | — | |
| A07-FR018-10 r1 | Single code validates format, uniqueness, and discount range | High | FR-018 › Main Flow (code creation); Screen 4: Affiliate Code Generation | Signed in as `{A1}` | DS-A07-04, DS-A07-06 | 1. Open Generate Codes in Single Affiliate mode for Affiliate A.<br>2. Check Discount Type options.<br>3. Try Discount Code "P3" and the 21-character code.<br>4. Try Discount Percentage 4, then 31; Fixed Amount $9.99.<br>5. Enter "p3launch", Percentage 5, save.<br>6. Create another code "p3Launch" for Affiliate B. | 1. Form opens.<br>2. Only "Hairline Fees Only" is offered.<br>3. Both blocked with a 4–20 characters message.<br>4. Each blocked with a range message.<br>5. Code saved as "P3LAUNCH" and Promo Code Detail opens.<br>6. Blocked: code already exists (case-insensitive) and codes belong to one affiliate only. | | Not tested | | | | — | |
| A07-FR018-11 r1 | Margin guard blocks discounts that exceed Hairline's commission | High | FR-018 › Screen 4 Business Rules (Margin Guard, Rule 15); Acceptance Criterion 6 | Signed in as `{A1}`; Affiliate A commission 10% | DS-A07-07 | 1. Create a code with Discount Percentage 10 and save.<br>2. Change to 5 and save.<br>3. Create a code with Fixed Amount $100 and save. | 1. Save is blocked and the shortfall is shown.<br>2. Code is saved.<br>3. A review warning is shown instead of a block; record in Notes how the admin confirms. | | Not tested | | | | — | |
| A07-FR018-12 r1 | Bulk generation creates one code per eligible affiliate and retries failures only | High | FR-018 › Alternative Flows A4 and B4; Screen 1 Acceptance Criteria 3–4; Screen 4.1: Code Generation Results | Signed in as `{A1}` | DS-A07-04, DS-A07-05 | 1. On the dashboard select Affiliate A, Affiliate B, and both ineligible affiliates; click "Generate Codes".<br>2. Fill Campaign Name "Phase3 Bulk", Percentage 5, submit.<br>3. Read Screen 4.1.<br>4. If any row failed, click "Retry Failed Only".<br>5. Click "View Codes". | 1. Bulk mode opens with the selected count; ineligible affiliates are blocked or excluded with the reason (Pending, incomplete payout setup).<br>2. Generation runs.<br>3. Batch ID, Requested, Created, Skipped, Failed counts and a row per affiliate with reason; created green, skipped gray, failed red; each eligible affiliate has its own distinct code.<br>4. Only failed rows are retried; no duplicate codes appear.<br>5. Promo Code Management opens filtered to "Phase3 Bulk". | | Not tested | | | | — | |
| A07-FR018-13 r1 | Promo code list and detail show live usage and keep the affiliate fixed | Medium | FR-018 › Screen 5: Promo Code Management; Screen 6: Promo Code Detail | Signed in as `{A1}`; a code with prepared redemptions | DS-A07-06, DS-A07-11 | 1. Open Promo Code Management and filter by Affiliate B.<br>2. Read Applied / Completed and Conversion Rate.<br>3. Open the code from the list, then the same code from Affiliate B's detail.<br>4. Change Expiration Date and save; try to change the linked affiliate or the discount value.<br>5. Deactivate the code. | 1. Only Affiliate B codes are listed with a result count.<br>2. Conversion Rate equals completed divided by applied.<br>3. Both entry points show the same screen and actions.<br>4. Expiration change saves and appears in Audit / History; affiliate and discount value cannot be changed (message explains one code per affiliate).<br>5. Status becomes "Inactive" and the change is in Audit / History. | | Not tested | | | | — | |
| A07-FR018-14 r1 | Payout Status & History is read-only and matches A-05 execution | High | FR-018 › Screen 7: Affiliate Payout Status & History; FR-017 Screen 6 | Signed in as `{A1}`; B02 A05-FR017-33 and -34 run | DS-A07-11 | 1. Open Affiliate Payout Status & History for last month.<br>2. Read the Overview totals.<br>3. Open Current Cycle and look for process or retry buttons.<br>4. Find the Failed row.<br>5. Open Billing History and filter by Affiliate B. | 1. Screen loads for "Month YYYY".<br>2. Total owed, total paid, affiliate count, failed count match the rows.<br>3. No process or retry action exists; statuses Pending, Processing, Paid, Failed match FR-017 Screen 6; the affiliate below $50 is not listed for payout.<br>4. Row is red with the failure reason.<br>5. Affiliate B payouts are listed with amount, date, Transaction ID, and final status. | | Not tested | | | | — | |
| A07-FR018-15 r1 | Payout detail reconciles bookings to net commission | High | FR-018 › Screen 8: Payout / Transaction Detail; Payment Rule 2 | Signed in as `{A1}` | DS-A07-11 | 1. From Screen 7 choose "View Detail" on Affiliate B's payout.<br>2. Read Included Bookings and Commission Calculation.<br>3. Open the next payout that carries the refund reversal.<br>4. Click "Download Receipt".<br>5. Open the same payout from Affiliate B's Payout History List. | 1. Detail opens with header, period, payment details masked to last 4 digits, Transaction ID, and Status Timeline.<br>2. Bookings $100.00, $150.00, $120.00 add up to the net $370.00.<br>3. The reversal shows as a separate negative line of -$120.00 and the net is reduced by it.<br>4. A PDF receipt with the same net amount downloads.<br>5. The same shared screen opens. | | Not tested | | | | — | |
| A07-FR018-16 r1 | Affiliate Detail brings account, codes, payouts, and audit together | Medium | FR-018 › Screen 3: Affiliate Detail | Signed in as `{A1}`; cases A07-FR018-07 to -15 run | DS-A07-04 | 1. Open Affiliate B's detail.<br>2. Read header, summary metrics, and Upcoming Payout panel.<br>3. Click a code row, go back, click a payout row.<br>4. Read the Activity / Audit Panel.<br>5. Add an Internal Note over 1000 characters, then a valid one. | 1. Detail opens.<br>2. Header shows name, status, affiliate ID, type, country, activation status; metrics and next payout date are filled.<br>3. Promo Code Detail and Payout / Transaction Detail open with a way back to the affiliate.<br>4. Suspension, reinstatement, commission change, and code events from this session are listed in order and cannot be edited.<br>5. Over 1000 characters is blocked; the valid note saves. | | Not tested | | | | — | |

## Batch Summary

| Total | Pass | Fail | Blocked | Not tested | Open bugs |
|---|---|---|---|---|---|
| 16 | 0 | 0 | 0 | 16 | 0 |

## Case Change Log

| Case | Revision | Date | Change |
|---|---|---|---|
| A07-FR018-01 | r1 | 2026-10-19 | Created |
| A07-FR018-02 | r1 | 2026-10-19 | Created |
| A07-FR018-03 | r1 | 2026-10-19 | Created |
| A07-FR018-04 | r1 | 2026-10-19 | Created |
| A07-FR018-05 | r1 | 2026-10-19 | Created |
| A07-FR018-06 | r1 | 2026-10-19 | Created |
| A07-FR018-07 | r1 | 2026-10-19 | Created |
| A07-FR018-08 | r1 | 2026-10-19 | Created |
| A07-FR018-09 | r1 | 2026-10-19 | Created |
| A07-FR018-10 | r1 | 2026-10-19 | Created |
| A07-FR018-11 | r1 | 2026-10-19 | Created |
| A07-FR018-12 | r1 | 2026-10-19 | Created |
| A07-FR018-13 | r1 | 2026-10-19 | Created |
| A07-FR018-14 | r1 | 2026-10-19 | Created |
| A07-FR018-15 | r1 | 2026-10-19 | Created |
| A07-FR018-16 | r1 | 2026-10-19 | Created |
