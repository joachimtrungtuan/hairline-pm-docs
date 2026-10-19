# B03 — PR-04 Aftercare (Provider)

## Batch Control

| Field | Value |
|---|---|
| Batch | B03 |
| Phase / plan version | Phase 2 / v1.0 |
| Module | PR-04 — Aftercare (provider dashboard) |
| FRs | FR-011 (provider side); FR-010 completion handoff as entry point |
| PRD sources | [FR-011 PRD](../../../../../../project-requirements/functional-requirements/fr011-aftercare-recovery-management/prd.md) › Workflow 1 (Main Flow, A1), Workflow 2 steps 3–4, Screens 8–12, Business Rules |
| Platform | Provider dashboard |
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

This batch checks how a clinic looks after a patient once the treatment is finished.

1. **Setting up aftercare** (FR-011 › Workflow 1, Screen 10). When the clinic saves the End of Treatment Modal (B01), the booking moves to Aftercare and the clinic is asked to set up an aftercare plan. A five-step wizard walks the clinic through it:
   1. Template Selection: pick an admin-made template.
   2. Milestone Customization: adjust milestones, scan and questionnaire frequency, restrictions.
   3. Medication Setup.
   4. Custom Instructions.
   5. Review and Confirm, then Activate Plan.

   A clinic that offers no aftercare can choose "Paperwork only - no aftercare service" instead (Alternative Flow A1).
2. **Standalone aftercare** (Workflow 2 steps 3–4). A patient treated elsewhere buys aftercare. Hairline assigns the request to a clinic, which then activates a plan through the same wizard.
3. **Running aftercare** (Screens 8, 9, 11, 12). The clinic sees only its own aftercare patients. From each patient it can follow progress and overdue tasks, adjust the plan with a reason, request scans and escalate.

This batch also checks the aftercare invariants in the Phase 2 exit gate:

- Only the assigned clinic sees and acts on a case.
- Activation needs every wizard step to be complete.
- Medication dates are valid.
- Every plan change carries a reason and is recorded.
- Clinics cannot use admin-only plan controls.

Admin oversight, reassignment and suspension effects are in B04.

**PRD gaps that affect this batch:**

- FR-011 gives no screen fields for "Paperwork only - no aftercare service" (A1), for "Assign to Hairline aftercare team" (A2), or for the Escalate Case form. PR04-FR011-06 and PR04-FR011-12 tell you exactly what to enter; record the field labels you see.
- Screen 11 says "major changes require admin approval" but does not define which changes are major.
- The PRD does not name the provider menu path to the aftercare setup prompt, the Aftercare Cases List or Aftercare Progress Tracking, or the admin path to the Aftercare Cases List.

Record what you see.

## Shared Preconditions

- B01 and B02 have been run in full. "Run day" is the day you run B03.
- These earlier setup items are in this state when B03 starts:
  - TX-1: {P1} with {V1}; Aftercare after PR03-FR010-15 (B01); treatment type FUE; no aftercare plan yet.
  - AD-1: {P6} with {V2}; Aftercare after A01-FR010-06 (B02); no aftercare plan yet.
  - AD-2: {P7}'s case, moved to {V1} in A01-FR006-09 (B02); not used in this batch.
- The team prepares these setup items before B03 starts:
  - AC-1: active milestone template "QA FUE Aftercare 12 months"; Treatment Type FUE; 2 milestones: "Early recovery" (14 days) and "Growth phase" (351 days); each milestone has 3D Scan Frequency Weekly, Questionnaire Set "QA Aftercare Check-in" and Questionnaire Frequency Weekly.
  - AC-2: questionnaire set "QA Aftercare Check-in" in the Aftercare category, and questionnaire set "QA Inquiry Intake" in a non-Aftercare category.
  - AC-3: the medication catalog contains Paracetamol.
  - AC-4: an active treatment-linked aftercare case for {P5} with {V1}, on a separate {P5} booking in Aftercare status; template AC-1; Aftercare Start Date = run day − 30 days; Current Milestone "Growth phase"; 10 tasks in total, 3 Completed (so Overall Progress 30%); one 3D scan task due on run day − 3 days and not done (overdue by more than 48 hours); no escalation yet.
  - AC-5: a paid standalone aftercare request from {P3}, assigned to {V1} by the team, Treatment Type FUE; no aftercare plan yet.
- With the credentials, the plan owner gives the tester the full name and Patient ID of {P1}, {P3}, {P5} and {P6}.
- Test upload files listed in the data sets are supplied with this batch by the team. Long texts (201, 501, 1001 and 2001 characters) are supplied as text files with the batch.
- Provider aftercare screens are reached via the provider dashboard main menu; record the path you used in Notes the first time.

## Test Data Sets

| Data set | Purpose | Values | Account |
|---|---|---|---|
| DS-PR04-01 | Treatment-linked setup | TX-1; template AC-1 | {V1} |
| DS-PR04-02 | Milestone Customization limits | Milestone Name of 201 characters; Milestone Duration 0, then -5, then 2.5, then 14; Activity Restrictions of 501 characters; Custom Instructions of 1001 characters. Valid values: Milestone Names "Early recovery" and "Growth phase", durations 14 and 351, Activity Restrictions "No heavy lifting or swimming", Custom Instructions "Wash gently with the provided shampoo" | {V1} |
| DS-PR04-03 | Medication Setup | Medication Paracetamol; Dosage "1 tablet 500mg"; Frequency "2x daily"; Start Date = run day; End Date = run day + 7 days; Special Instructions "Take after meals". Invalid: Start Date = run day − 1 day; End Date = Start Date; Special Instructions of 501 characters | {V1} |
| DS-PR04-04 | Custom Instructions | General Instructions of 2001 characters, then "Keep the scalp dry for 3 days and avoid direct sun for 2 weeks"; Emergency Contact of 201 characters, then "Clinic front desk, available 9:00 to 18:00"; Special Considerations of 1001 characters, then "None"; Milestone Instructions "Attend the day 14 review" | {V1} |
| DS-PR04-05 | Paperwork only | AD-1; aftercare-instructions.pdf (PDF, 1 MB, the clinic's written aftercare instructions) | {V2} |
| DS-PR04-06 | Running case with overdue tasks | AC-4. Escalation text "Patient reports persistent redness at donor area after 30 days" | {V1} |
| DS-PR04-07 | Plan edit | Custom Instructions update "Resume light exercise from week 6"; Change Reason "Patient reported mild swelling at day 30 review"; a Change Reason of 501 characters. Duration change: "Growth phase" from 351 to 380 days, reason "Clinic recommends a longer growth review period" | {V1} |
| DS-PR04-08 | Standalone case | AC-5; template AC-1 with the DS-PR04-02 to DS-PR04-04 valid values | {V1} |

## Test Cases

| ID | Title | Priority | PRD flow ref | Preconditions | Test data | Steps | Expected result | Actual result / data | Result | Notes | Evidence | Bug ID | Bug status | Last tested |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PR04-FR011-01 r1 | Clinic is prompted to set up aftercare and selects a template | High | FR-011 › Workflow 1 steps 1–2; Screen 10 Step 1 | Signed in as {V1}; TX-1 is Aftercare with no plan | DS-PR04-01 | 1. Open {P1}'s booking TX-1 (reach via the main menu; record the path you used in Notes).<br>2. Start aftercare setup from the prompt.<br>3. Review Available Templates and open the Template Preview of "QA FUE Aftercare 12 months".<br>4. Click the continue control without selecting a template.<br>5. Select "QA FUE Aftercare 12 months" and click Select Template. | 1. (step 1) TX-1 shows Aftercare and a prompt to set up an aftercare plan.<br>2. (step 3) Each template shows Template Name, Template Description, Treatment Type, Duration and Milestone Count; the preview shows the two milestones "Early recovery" and "Growth phase".<br>3. (step 4) The wizard stays on Step 1 with a message asking for a template.<br>4. (step 5) The wizard moves to Step 2: Milestone Customization and the progress indicator shows step 2. | | Not tested | | | | — | |
| PR04-FR011-02 r1 | Milestone Customization enforces field limits | Medium | FR-011 › Screen 10 Step 2 | Run after PR04-FR011-01: the wizard is on Step 2 | DS-PR04-02 | 1. On milestone 1, paste the 201-character Milestone Name.<br>2. Enter Milestone Duration 0, then -5, then 2.5, then 14, moving out of the field after each.<br>3. Paste the 501-character Activity Restrictions and the 1001-character Custom Instructions.<br>4. Open the Questionnaire Set list on milestone 1 and read the options. Clear the selection and click the continue control.<br>5. Enter the DS-PR04-02 valid values on both milestones, select "QA Aftercare Check-in" on both and continue. | 1. (step 1) The name is rejected or cut off at 200 characters.<br>2. (step 2) 0, -5 and 2.5 each show an error; 14 is accepted.<br>3. (step 3) Each text is rejected or cut off at 500 and 1000 characters.<br>4. (step 4) The list offers "QA Aftercare Check-in" and not "QA Inquiry Intake". With no set selected the wizard stays on Step 2 with an error on Questionnaire Set.<br>5. (step 5) The wizard moves to Step 3: Medication Setup. | | Not tested | | | | — | |
| PR04-FR011-03 r1 | Medication Setup validates dates and enables Add Medication only when complete | High | FR-011 › Screen 10 Step 3; Workflow 1 step 3 | Run after PR04-FR011-02: the wizard is on Step 3 | DS-PR04-03 | 1. Select Paracetamol and fill Dosage and Frequency only.<br>2. Check Add Medication.<br>3. Enter Start Date = run day − 1 day.<br>4. Enter Start Date = run day and End Date = run day.<br>5. Paste the 501-character Special Instructions.<br>6. Enter the valid values and click Add Medication.<br>7. Check Medication List and Medication Timeline, then continue. | 1. (step 2) Add Medication is disabled.<br>2. (step 3) The past Start Date is rejected or cannot be picked.<br>3. (step 4) The End Date is rejected as not after the Start Date.<br>4. (step 5) The text is rejected or cut off at 500 characters.<br>5. (step 6) Paracetamol, 1 tablet 500mg, 2x daily is added to the Medication List.<br>6. (step 7) The Medication Timeline shows it from run day to run day + 7 days. The wizard moves to Step 4: Custom Instructions. | | Not tested | | | | — | |
| PR04-FR011-04 r1 | Custom Instructions limits and going back keep entered data | Medium | FR-011 › Screen 10 Step 4; Business Rules (go back to previous steps) | Run after PR04-FR011-03: the wizard is on Step 4 | DS-PR04-04 | 1. Paste the 2001-character General Instructions, the 201-character Emergency Contact and the 1001-character Special Considerations.<br>2. Replace them with the valid values and enter the Milestone Instructions.<br>3. Go back to Step 2, then to Step 3.<br>4. Go forward to Step 4. | 1. (step 1) Each text is rejected or cut off at 2000, 200 and 1000 characters.<br>2. (step 2) The valid values are accepted with no error.<br>3. (step 3) Step 2 still shows "Early recovery" 14 days and "Growth phase" 351 days; Step 3 still lists Paracetamol.<br>4. (step 4) Step 4 still shows the valid instructions. | | Not tested | | | | — | |
| PR04-FR011-05 r1 | Plan activates only when every step is complete | High | FR-011 › Screen 10 Step 5; Workflow 1 step 4 | Run after PR04-FR011-04: Steps 1–4 are complete | DS-PR04-01 to DS-PR04-04 | 1. Continue to Step 5: Review and Confirm and check Plan Summary, Patient Information and Provider Information.<br>2. Go back to Step 2, clear milestone 1's Milestone Name and go forward to Step 5.<br>3. Check Activate Plan and click it.<br>4. Go back to Step 2, enter "Early recovery" again, go forward to Step 5 and click Activate Plan.<br>5. Open the Aftercare Cases List (reach via the main menu; record the path you used in Notes). | 1. (step 1) Plan Summary shows template "QA FUE Aftercare 12 months", both milestones, Paracetamol and the instructions entered; Patient Information shows {P1}; Provider Information shows {V1}.<br>2. (step 3) Activate Plan is disabled, or clicking it shows a message about the missing name; no plan is activated.<br>3. (step 4) A confirmation is shown.<br>4. (step 5) {P1} is listed with Current Milestone "Early recovery" and Progress 0%. | | Not tested | | | | — | |
| PR04-FR011-06 r1 | Clinic chooses paperwork only and the booking completes | Medium | FR-011 › Workflow 1 Alternative Flow A1 | Signed in as {V2}; AD-1 is Aftercare with no plan | DS-PR04-05 | 1. Open {P6}'s booking AD-1 (reach via the main menu; record the path you used in Notes) and start aftercare setup from the prompt.<br>2. Select "Paperwork only - no aftercare service".<br>3. Upload aftercare-instructions.pdf and click the confirm control (record its label).<br>4. Reload AD-1 and check its status. Open the Aftercare Cases List. | 1. (step 2) The option "Paperwork only - no aftercare service" is offered and an upload field for the instructions document appears.<br>2. (step 3) The upload succeeds and a confirmation is shown.<br>3. (step 4) AD-1's status is Completed, and {P6} is not listed in the Aftercare Cases List. | | Not tested | | | | — | |
| PR04-FR011-07 r1 | Aftercare Cases List shows only this clinic's patients | High | FR-011 › Screen 8 | Run after PR04-FR011-05: {P1}'s plan is active. Signed in as {V1} | DS-PR04-01, DS-PR04-06 | 1. Open the Aftercare Cases List.<br>2. Check the columns.<br>3. Type {P5}'s Patient ID in search, stop typing and wait 2 seconds. Clear it and do the same with {P5}'s full name.<br>4. Clear the search. Set Milestone = "Growth phase". Clear it and set Date range = run day − 31 days to run day − 29 days.<br>5. Clear the filters, check {P5}'s row and open its Action menu. | 1. (step 1) {P1} and {P5} are listed; {P6} is not listed.<br>2. (step 2) Columns: Patient ID, Patient Name, Phone Number, Age, Problem, Treatment & Package, Aftercare Start Date, Current Milestone, Progress, Med Alerts, Last Activity, Action.<br>3. (step 3) Within 2 seconds of the last keystroke each search lists {P5} only.<br>4. (step 4) Milestone "Growth phase" lists {P5} and not {P1}; the date range lists {P5} and not {P1}.<br>5. (step 5) {P5}'s row has an amber overdue indicator and shows Progress 30%; Action offers View, Edit, Message and Escalate. | | Not tested | | | | — | |
| PR04-FR011-08 r1 | Another clinic cannot see or open this clinic's aftercare case | High | FR-011 › Business Rules (access); Screen 8 | Run after PR04-FR011-05: {P1}'s plan is active. Signed in as {V1} | DS-PR04-01 | 1. Open {P1}'s case from the Aftercare Cases List, copy the URL from the address bar and sign out.<br>2. Sign in as {V2}, open the Aftercare Cases List and search for {P1}'s full name.<br>3. Paste the copied URL into the address bar and press Enter.<br>4. Sign out. | 1. (step 2) {P1} is not listed.<br>2. (step 3) An access-denied or not-found page is shown with no patient name, Patient ID or plan data. | | Not tested | | | | — | |
| PR04-FR011-09 r1 | Patient Aftercare Details shows full history and actions | Medium | FR-011 › Screen 9 | Signed in as {V1}; AC-4 has 3 of 10 tasks Completed | DS-PR04-06 | 1. Open {P5}'s Patient Aftercare Details from the Aftercare Cases List.<br>2. Check Treatment Details, Assigned Template, Current Milestone, Overall Progress, Milestone Timeline and Upcoming Tasks.<br>3. Check 3D Scan History, Questionnaire Responses, Medication Adherence History and Communication Log.<br>4. Check the actions offered.<br>5. Click Request Additional Scan and confirm. | 1. (step 2) Treatment Details shows {P5}'s treatment (not N/A); Assigned Template "QA FUE Aftercare 12 months"; Current Milestone "Growth phase"; Overall Progress 30% (3 of 10 tasks); Upcoming Tasks are sorted by due date, earliest first.<br>2. (step 3) Each history list is in date order.<br>3. (step 4) Adjust Plan, Request Additional Scan, Contact Aftercare Team and Escalate Case are shown.<br>4. (step 5) A confirmation is shown and the scan request appears in Upcoming Tasks or the Communication Log with today's date. | | Not tested | | | | — | |
| PR04-FR011-10 r1 | Clinic edits a plan with a reason and cannot use admin-only controls | High | FR-011 › Screen 11; Business Rules | Signed in as {V1}; AC-4 is active | DS-PR04-06, DS-PR04-07 | 1. From {P5}'s details click Adjust Plan.<br>2. Check the actions offered.<br>3. Click Update Custom Instructions, enter the update and save with Change Reason empty.<br>4. Paste the 501-character Change Reason and save.<br>5. Enter the valid Change Reason and save.<br>6. Click Request Duration Change on "Growth phase", enter 380 days and the duration reason, and submit.<br>7. Check Change History. | 1. (step 2) Modify Medication Schedule, Update Custom Instructions, Add Milestone Notes and Request Duration Change are shown. Change Milestone Structure, Modify Template Assignment, Override Settings and Reassign Provider are not shown.<br>2. (step 3) Save is blocked with an error on Change Reason.<br>3. (step 4) The reason is rejected or cut off at 500 characters.<br>4. (step 5) A confirmation is shown and the new custom instruction is displayed.<br>5. (step 6) The duration change shows Approval Status Pending; "Growth phase" still shows 351 days.<br>6. (step 7) Change History lists both changes with time, {V1} and reason. | | Not tested | | | | — | |
| PR04-FR011-11 r1 | Progress tracking highlights overdue tasks | Medium | FR-011 › Screen 12 | Signed in as {V1}; AC-4's 3D scan task due run day − 3 days is not done | DS-PR04-06 | 1. Open Aftercare Progress Tracking for {P5} (reach via the case details or main menu; record the path you used in Notes).<br>2. Check the Overdue Tasks Indicator, 3D Scan Status and Questionnaire Status.<br>3. Check the actions offered. | 1. (step 2) The Overdue Tasks Indicator is red and counts at least 1. 3D Scan Status shows Overdue for the task due run day − 3 days. Every status shown is Completed, Pending or Overdue.<br>2. (step 3) Request Additional Scan, Send Message to Patient, Schedule Consultation and Escalate Case are shown. | | Not tested | | | | — | |
| PR04-FR011-12 r1 | Clinic escalates a case and the escalation is recorded | Medium | FR-011 › Screen 9 (Escalate Case); Workflow 4 | Signed in as {V1}; AC-4 has no escalation yet | DS-PR04-06 | 1. From {P5}'s details click Escalate Case.<br>2. Enter the escalation text in the free-text field. For any choice field, select the first option. Copy every field label and chosen value into Actual result. Submit.<br>3. Check the Communication Log.<br>4. Sign out. Sign in as {A1}, open the admin Aftercare Cases List (reach via the main menu; record the path you used in Notes), open {P5}'s case and open Tab 3 Communication Log. | 1. (step 2) A confirmation is shown.<br>2. (step 3) The Communication Log has a new entry with Message Type escalation, the text and the time.<br>3. (step 4) Escalation History on Tab 3 shows {V1}'s escalation with the text. | | Not tested | | | | — | |
| PR04-FR011-13 r1 | Clinic activates an assigned standalone aftercare case | High | FR-011 › Workflow 2 steps 3–4; Screens 9, 10 | Signed in as {V1}; AC-5 is assigned to {V1} with no plan | DS-PR04-08 | 1. Open the Aftercare Cases List and find {P3}'s standalone case.<br>2. Open Patient Aftercare Details.<br>3. Start setup, select "QA FUE Aftercare 12 months", complete Steps 2 to 4 with the valid values from DS-PR04-02 to DS-PR04-04 and click Activate Plan.<br>4. Check the case in the Aftercare Cases List. | 1. (step 1) {P3}'s standalone case is listed.<br>2. (step 2) Treatment Details shows N/A, and only the aftercare intake data is shown.<br>3. (step 3) Each step shows the same fields as in PR04-FR011-01 to PR04-FR011-04, and a confirmation is shown after Activate Plan.<br>4. (step 4) {P3}'s case shows Current Milestone "Early recovery" and Progress 0%. | | Not tested | | | | — | |

## Batch Summary

| Total | Pass | Fail | Blocked | Not tested | Open bugs |
|---|---|---|---|---|---|
| 13 | 0 | 0 | 0 | 13 | 0 |

## Case Change Log

| Case | Revision | Date | Change |
|---|---|---|---|
| PR04-FR011-01 | r1 | 2026-10-19 | Created |
| PR04-FR011-02 | r1 | 2026-10-19 | Created |
| PR04-FR011-03 | r1 | 2026-10-19 | Created |
| PR04-FR011-04 | r1 | 2026-10-19 | Created |
| PR04-FR011-05 | r1 | 2026-10-19 | Created |
| PR04-FR011-06 | r1 | 2026-10-19 | Created |
| PR04-FR011-07 | r1 | 2026-10-19 | Created |
| PR04-FR011-08 | r1 | 2026-10-19 | Created |
| PR04-FR011-09 | r1 | 2026-10-19 | Created |
| PR04-FR011-10 | r1 | 2026-10-19 | Created |
| PR04-FR011-11 | r1 | 2026-10-19 | Created |
| PR04-FR011-12 | r1 | 2026-10-19 | Created |
| PR04-FR011-13 | r1 | 2026-10-19 | Created |
