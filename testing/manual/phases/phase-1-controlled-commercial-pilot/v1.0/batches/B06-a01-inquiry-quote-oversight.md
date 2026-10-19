# B06 — A01 Admin Inquiry and Quote Oversight

## Batch Control

| Field | Value |
|---|---|
| Batch | B06 |
| Phase / plan version | Phase 1 / v1.0 |
| Module | A-01 — Patient Management & Oversight (inquiry and quote oversight only) |
| FRs | FR-003, FR-004, FR-016, FR-031 (admin role enforcement) |
| PRD sources | [FR-003 Inquiry Submission](../../../../../../project-requirements/functional-requirements/fr003-inquiry-submission/prd.md) (Workflow 2 Alternative Flow B1, Screens 11–12, Business Rules, Admin Editability); [FR-004 Quote Submission](../../../../../../project-requirements/functional-requirements/fr004-quote-submission/prd.md) (Workflow 3 Lifecycle, Workflow 5 Admin Oversight, Screens 5–7, Business Rules); [FR-016 Admin Patient Management](../../../../../../project-requirements/functional-requirements/fr016-admin-patient-mgmt/prd.md) (Patient List View, Patient Detail View tabs Overview, Treatment Journey, Medical Data; User Story 8); [FR-031 Admin Access Control](../../../../../../project-requirements/functional-requirements/fr031-admin-access-control/prd.md) (Error Flow B5, Screen 4 Quotes & Inquiries Oversight) |
| Platform | Admin dashboard (provider dashboard used only to confirm reassignment and admin edits reach the provider) |
| Tester | |
| Build tested | |

## How to Fill In This File

1. Run cases in table order unless a case says otherwise.
2. Fill only: **Actual result / data**, **Result**, **Notes**, **Evidence**, **Bug status**, **Last tested**.
3. **Result** values: `Not tested`, `Pass`, `Fail`, `Blocked`. **Bug status** values: `—`, `Found`, `Logged`, `Fixed - retest`, `Closed`, `Reopened` (set `Found` when you see a bug; the team logs it in Plane).
4. Put usability observations in **Notes**: what you did, what happened, and why it was confusing or slow, even when the case passes.
5. Do not edit IDs, steps, or expected results, and do not use the vertical-bar character inside cells. Put questions in **Notes**.

## Flow Overview

This batch checks that Hairline admins can see and correct every inquiry and quote in the pilot, and that what they see matches what providers saw in B05.

1. **Inquiry oversight (FR-003 › Screens 11–12).** Admins see all inquiries with full patient identity, current status, quote count and assigned providers. From the inquiry detail they can assign an unmatched inquiry (FR-003 › Workflow 2 › B1), reassign providers with an eligibility check, override the expiry, edit inquiry data, archive an inquiry, and review an exportable audit trail. Every action needs a reason and is audited.
2. **Quote oversight (FR-004 › Workflow 5; Screens 5–7).** Admins list quotes grouped by inquiry, switch between quotes of the same inquiry, edit draft or sent quotes inline with an audit reason, and archive or restore quotes. Accepted, expired and cancelled quotes cannot be edited, and accepted quotes cannot be archived.
3. **Quote-state consistency (FR-004 › Workflow 3).** After a patient accepts one quote or cancels the inquiry, every related quote shows the correct final status on both dashboards.
4. **Patient view (FR-016).** Admins find the patient, read the Treatment Journey, including the cancelled-inquiry card, and view medical data only after giving an access justification.
5. **Admin permissions (FR-031 › B5).** An admin with view-only oversight permissions cannot edit, reassign or override.

Booking, payment, treatment intervention, refunds, communication monitoring and replacement quotes are Phase 2 and are not tested here.

## Shared Preconditions

- B01–B05 are complete. The inquiry and quote IDs recorded in B05 **Notes** (INQ-1 to INQ-7) are available.
- {A1} is signed in to the admin dashboard as Super Admin.
- The pilot admin account created in B04 (A09-FR031-03 and 05) is Active with the role Pilot Ops Viewer (View Inquiries Overview and View Quote Details only).
- The team has prepared before the session:
  - INQ-8: submitted by {P7} for a country where no provider is eligible, so it has no matched providers.
  - {V4} is in Suspended status (set through A-02).
  - At least one sent quote from {V1} exists that is not accepted or cancelled (for example the INQ-1 quote from B05).

## Test Data Sets

| Data set | Purpose | Values | Account |
|---|---|---|---|
| DS-A01-01 | Inquiry overview filters | Patient ID of INQ-1; {P1}'s full name; Current Status: Quoted, then Cancelled; Assigned Provider: {V1} | {A1} |
| DS-A01-02 | Manual assignment and reassignment | Unmatched inquiry: INQ-8; Assign to: {V1}; Ineligible provider: {V4} (suspended); Duplicate: {V2} on INQ-1 (already assigned); Reason: Pilot test assignment; Blank reason | {A1} |
| DS-A01-03 | Expiry override | New expiry: yesterday with no justification; 7 days from today with Reason: Pilot test extension | {A1} |
| DS-A01-04 | Inquiry edit and archive | Field: an admin-editable inquiry field such as Requested Date Ranges on INQ-7, moved 7 days later; Reason: Pilot test correction; Archive Reason: Pilot test archive (use INQ-8 after DS-A01-02) | {A1} |
| DS-A01-05 | Admin inline quote edit | Quote: {V1}'s sent INQ-1 quote; Offered Price option 1: minus 100; Audit Reason: blank, then Pilot test price correction | {A1} |
| DS-A01-06 | Patient search | Search: 1 character, then {P4}'s Patient ID; Date Range: Start after End, then valid; Filter Status: Cancelled; Provider: {V1} | {A1} |
| DS-A01-07 | Medical data justification | Access Justification: 19 characters, then 20 characters (Pilot QA review INQ1) | {A1} |

## Test Cases

| ID | Title | Priority | PRD flow ref | Preconditions | Test data | Steps | Expected result | Actual result / data | Result | Notes | Evidence | Bug ID | Bug status | Last tested |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A01-FR003-01 r1 | Admin overview lists all inquiries with full identity and live status | High | FR-003 › Screen 11 Hairline Overview Dashboard | Signed in as {A1} | DS-A01-01 | 1. Open the admin inquiry overview.<br>2. Find INQ-1 to INQ-8.<br>3. Filter by Current Status Quoted, then Cancelled.<br>4. Filter by Assigned Provider {V1}.<br>5. Search by Patient ID and by full name. | 1. All eight inquiries are listed, including INQ-3 (only {V3}) and INQ-8 (no provider).<br>2. Patient names are shown in full (admins are not masked).<br>3. Current Status, Quotes Count and Assigned Providers match B05 (for example INQ-1 shows {V1} and {V2} and the right quote count).<br>4. Filters and search return only matching inquiries. | | Not tested | | | | — | |
| A01-FR003-02 r1 | Admin assigns an unmatched inquiry to an eligible provider | High | FR-003 › Workflow 2, Alternative Flow B1; Screen 12 Reassignment | Signed in as {A1}; INQ-8 has no assigned provider | DS-A01-02 | 1. Open INQ-8 and check the distribution or assigned providers area.<br>2. Start reassignment, search for {V1} and select it with a blank reason.<br>3. Enter the reason and confirm.<br>4. As {V1}, open the provider inquiry list. | 1. INQ-8 is clearly shown as needing manual assignment.<br>2. A blank reason blocks the action.<br>3. After confirming, {V1} is listed as assigned and an audit entry records the admin, time and reason.<br>4. {V1} now sees INQ-8 in the provider inquiry list, with the patient name masked. | | Not tested | | | | — | |
| A01-FR003-03 r1 | Reassignment rejects suspended and duplicate providers | High | FR-003 › Screen 12 Reassignment (eligibility check, no duplicates); Workflow 2, Alternative Flow B4 | Signed in as {A1}; {V4} suspended | DS-A01-02 | 1. Open INQ-1 and start reassignment.<br>2. Search for {V4} and try to add it.<br>3. Search for {V2}, already assigned, and try to add it again. | 1. {V4} is not offered, or the eligibility check refuses it with a clear reason.<br>2. {V2} cannot be added twice.<br>3. The assigned providers of INQ-1 stay unchanged. | | Not tested | | | | — | |
| A01-FR003-04 r1 | Expiry override cannot be set in the past without justification | Medium | FR-003 › Screen 12 Override Controls | Signed in as {A1}; INQ-2 open | DS-A01-03 | 1. Open the expiry override for INQ-2.<br>2. Enter yesterday's date with no justification and save.<br>3. Enter a date 7 days from today with the reason and save.<br>4. Open the inquiry audit trail. | 1. Step 2 is blocked with a message that a past expiry needs justification.<br>2. Step 3 saves; the new expiry is shown on the inquiry.<br>3. The audit trail records the old and new expiry, the admin and the reason. | | Not tested | | | | — | |
| A01-FR003-05 r1 | Admin edits inquiry data with a reason and the change is audited | Medium | FR-003 › Screen 12 Admin Actions (Edit); Admin Editability | Signed in as {A1}; INQ-7 open | DS-A01-04 | 1. Choose Edit on INQ-7 and change the field from DS-A01-04.<br>2. Save without a reason.<br>3. Enter the reason and save.<br>4. As {V1}, open INQ-7. | 1. Saving without a reason is blocked.<br>2. With a reason, the change saves and the audit trail shows the old value, new value, admin and reason.<br>3. {V1} sees the updated value. | | Not tested | | | | — | |
| A01-FR003-06 r1 | Soft-deleted inquiry becomes archived and read-only | Medium | FR-003 › Screen 12 Soft Delete | Signed in as {A1}; A01-FR003-02 done | DS-A01-04 | 1. Open INQ-8 and choose Soft Delete.<br>2. Confirm without a reason, then with the reason.<br>3. Reopen INQ-8 and try Edit or Reassign. | 1. A reason is required.<br>2. INQ-8 shows an "Archived" badge and stays listed for admins.<br>3. Edit and Reassign are unavailable; the inquiry is read-only.<br>4. The audit trail records the soft delete. | | Not tested | | | | — | |
| A01-FR003-07 r1 | Inquiry audit trail can be filtered and exported | Medium | FR-003 › Screen 12 Audit Trail | Cases A01-FR003-02 to 06 run | — | 1. Open the audit trail of INQ-8.<br>2. Filter by action type or date.<br>3. Export the audit trail and open the file. | 1. The trail lists the assignment and the soft delete with admin, timestamp and reason.<br>2. Filters narrow the entries correctly.<br>3. The export contains the same entries as on screen. | | Not tested | | | | — | |
| A01-FR004-01 r1 | Admin quote list groups quotes by inquiry and switches between them | High | FR-004 › Workflow 5; Screen 5 Admin Quote List; Screen 6 Quote Selector | Signed in as {A1} | — | 1. Open the admin quote list.<br>2. Find the INQ-1 group.<br>3. Filter by each Quote Status in turn.<br>4. Open one INQ-1 quote and use the Quote Selector. | 1. Quotes are grouped by inquiry with a Provider column; INQ-1 shows a multi-quote cue with {V1}'s two quotes and {V2}'s quote.<br>2. The status filter offers draft, sent, expired, withdrawn, archived, accepted and each cancelled status, and returns only matching quotes.<br>3. The Quote Selector switches between quotes of the same inquiry without going back to the list. | | Not tested | | | | — | |
| A01-FR004-02 r1 | Quote states are consistent after a patient accepts a quote | High | FR-004 › Workflow 3 (acceptance outcome); Screen 5 | Signed in as {A1}; INQ-5 prepared as in B05 | — | 1. Filter the admin quote list by INQ-5.<br>2. Open {V2}'s accepted quote and check every option.<br>3. Open {V1}'s quote.<br>4. Compare with what {V1} and {V2} saw in PR02-FR004-11. | 1. {V2}'s quote is Accepted; only the chosen option and date are accepted and the other options are not selected.<br>2. {V1}'s quote is Cancelled (Other Accepted).<br>3. Any draft on INQ-5 is cancelled.<br>4. Admin and provider views show the same statuses. | | Not tested | | | | — | |
| A01-FR004-03 r1 | Quote states are consistent after the patient cancels the inquiry | High | FR-004 › Workflow 3 (inquiry cancelled); FR-003 › Business Rules | Signed in as {A1}; PR02-FR004-10 done | — | 1. Open INQ-4 in the admin inquiry overview.<br>2. Open its quotes in the admin quote list.<br>3. Check whether the cancellation reason is shown to admins. | 1. INQ-4 shows status Cancelled.<br>2. Every INQ-4 quote, including the locked draft, shows Cancelled (Inquiry Cancelled).<br>3. Admins can see the cancellation reason (providers could not in B05). | | Not tested | | | | — | |
| A01-FR004-04 r1 | Admin edits a sent quote inline with an audit reason | High | FR-004 › Screen 7 Admin Inline Quote Edit; Workflow 2 (new version, expiry kept) | Signed in as {A1}; {V1}'s INQ-1 quote is Sent; its expiry noted | DS-A01-05 | 1. Open {V1}'s INQ-1 quote and start the inline edit.<br>2. Change the option 1 price and save with a blank Audit Reason.<br>3. Enter the reason and save.<br>4. Open the Version History and Audit Trail.<br>5. As {V1}, open the same quote. | 1. A blank Audit Reason blocks the save.<br>2. With a reason, the new price saves and the version increases.<br>3. The expiry is unchanged.<br>4. Version History shows both versions; the Audit Trail shows the admin, time and reason.<br>5. {V1} sees the new price. | | Not tested | | | | — | |
| A01-FR004-05 r1 | Admin cannot edit or archive locked quotes | High | FR-004 › Screen 5 (Restore and Archive hidden for accepted), Screen 7 (draft and sent only); Workflow 5 | Signed in as {A1} | — | 1. Open {V2}'s accepted INQ-5 quote and look for inline edit, Archive and Restore.<br>2. Open {V1}'s expired INQ-6 quote and look for inline edit.<br>3. Open a cancelled INQ-4 quote and look for inline edit. | 1. The accepted quote offers no inline edit, Archive or Restore.<br>2. The expired and cancelled quotes offer no inline edit, or editing is refused with a clear message.<br>3. No change is saved on any of them. | | Not tested | | | | — | |
| A01-FR004-06 r1 | Admin archives and restores a sent quote | Medium | FR-004 › Workflow 5 (soft delete and restore); Screen 5 Audit Trail modal | Signed in as {A1}; {V1}'s second INQ-1 quote is Sent | — | 1. Archive {V1}'s second INQ-1 quote and give a reason.<br>2. Check its status in the admin list and in {V1}'s Quote List.<br>3. Restore it with a reason.<br>4. Open the Audit Trail modal. | 1. The quote moves to Archived on both dashboards and is not removed permanently.<br>2. Restore returns it to its earlier status.<br>3. The audit trail shows both actions with admin, time and reason. | | Not tested | | | | — | |
| A01-FR016-01 r1 | Admin finds a patient with search and filters | Medium | FR-016 › Patient List View | Signed in as {A1}; Patients section open | DS-A01-06 | 1. Type 1 character in search.<br>2. Type {P4}'s Patient ID.<br>3. Set Date Range Start after End.<br>4. Set a valid range, Status Cancelled and Provider {V1}.<br>5. Search for a Patient ID that does not exist. | 1. One character does not start a search; at 2 or more characters results update after a short pause.<br>2. {P4} is found and shows the Cancelled stage.<br>3. Start after End is rejected.<br>4. Combined filters return only matching patients.<br>5. No match shows "No patients found matching your search criteria" with suggestions. | | Not tested | | | | — | |
| A01-FR016-02 r1 | Cancelled inquiry appears correctly in the patient Treatment Journey | Medium | FR-016 › Patient Detail View, Overview and Treatment Journey tabs; User Story 8 | Signed in as {A1}; {P4} found | — | 1. Open {P4}'s detail and read the Overview.<br>2. Open Treatment Journey and find the Inquiry Cancelled card.<br>3. Click "Open Case Detail". | 1. The Overview shows the Cancellation Reason and Timestamp, and no action to reverse the cancellation.<br>2. The card shows the reason, the timestamp, "Cancelled by Patient" and the number of quotes cancelled, matching A01-FR004-03.<br>3. The link opens the read-only cancelled inquiry. | | Not tested | | | | — | |
| A01-FR016-03 r1 | Medical data needs an access justification and is read-only | High | FR-016 › Patient Detail View, Medical Data tab; Business Rule 2 | Signed in as {A1}; {P1}'s detail open | DS-A01-07 | 1. Open the Medical Data tab.<br>2. Enter the 19-character justification and continue.<br>3. Enter the 20-character justification and continue.<br>4. Look for any edit control.<br>5. Check the patient's or admin's access log. | 1. Medical data is hidden until a justification is given; 19 characters are rejected and 20 are accepted.<br>2. The banner reads "Protected Health Information - Access Logged".<br>3. Questionnaire answers are read-only and coloured by severity (the Critical answer in red).<br>4. The access is logged with admin, time and justification. | | Not tested | | | | — | |
| A01-FR031-01 r1 | View-only oversight admin cannot change inquiries or quotes | High | FR-031 › Error Flow B5; Screen 4 Quotes & Inquiries Oversight (A-01) | Pilot admin signed in with role Pilot Ops Viewer; {A1} has copied the URL of an inline quote edit and an inquiry reassignment page | — | 1. As the pilot admin, open the inquiry overview and INQ-1.<br>2. Look for Edit, Reassign, Override and Soft Delete.<br>3. Open {V1}'s INQ-1 quote and look for inline edit.<br>4. Paste the copied edit and reassignment URLs. | 1. The pilot admin can view the overview, the inquiry and the quote details.<br>2. Edit, Reassign, Override, Soft Delete and inline edit are hidden.<br>3. The direct URLs show "Access Denied: You do not have permission to access this feature. Contact your administrator if you need access." and nothing changes. | | Not tested | | | | — | |
| A01-FR003-08 r1 | Usability: admin traces a patient's inquiry to its quotes | Low | FR-003 › Screens 11–12; FR-004 › Screens 5–6 | Signed in as {A1}; no instructions given beyond the task | DS-A01-01 | 1. Starting from the dashboard home, find INQ-1 by {P1}'s name.<br>2. From the inquiry, reach every quote sent for it.<br>3. Find out which provider offered the lowest price.<br>4. Record clicks, time taken and any confusing labels. | 1. The tester reaches INQ-1 and its quotes without help.<br>2. Quote statuses, providers and prices can be compared without opening each quote separately, or the Quote Selector makes it quick.<br>3. Usability notes are recorded. | | Not tested | | | | — | |

## Batch Summary

| Total | Pass | Fail | Blocked | Not tested | Open bugs |
|---|---|---|---|---|---|
| 18 | 0 | 0 | 0 | 18 | 0 |

## Case Change Log

| Case | Revision | Date | Change |
|---|---|---|---|
| A01-FR003-01 | r1 | 2026-10-19 | Created |
| A01-FR003-02 | r1 | 2026-10-19 | Created |
| A01-FR003-03 | r1 | 2026-10-19 | Created |
| A01-FR003-04 | r1 | 2026-10-19 | Created |
| A01-FR003-05 | r1 | 2026-10-19 | Created |
| A01-FR003-06 | r1 | 2026-10-19 | Created |
| A01-FR003-07 | r1 | 2026-10-19 | Created |
| A01-FR004-01 | r1 | 2026-10-19 | Created |
| A01-FR004-02 | r1 | 2026-10-19 | Created |
| A01-FR004-03 | r1 | 2026-10-19 | Created |
| A01-FR004-04 | r1 | 2026-10-19 | Created |
| A01-FR004-05 | r1 | 2026-10-19 | Created |
| A01-FR004-06 | r1 | 2026-10-19 | Created |
| A01-FR016-01 | r1 | 2026-10-19 | Created |
| A01-FR016-02 | r1 | 2026-10-19 | Created |
| A01-FR016-03 | r1 | 2026-10-19 | Created |
| A01-FR031-01 | r1 | 2026-10-19 | Created |
| A01-FR003-08 | r1 | 2026-10-19 | Created |
