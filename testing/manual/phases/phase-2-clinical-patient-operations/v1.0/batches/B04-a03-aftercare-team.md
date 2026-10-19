# B04 — A-03 Aftercare Team (Admin)

## Batch Control

| Field | Value |
|---|---|
| Batch | B04 |
| Phase / plan version | Phase 2 / v1.0 |
| Module | A-03 — Aftercare team and aftercare oversight (admin dashboard) |
| FRs | FR-011 (admin side); FR-006 Aftercare booking status and FR-015 provider status as touchpoints |
| PRD sources | [FR-011 PRD](../../../../../../project-requirements/functional-requirements/fr011-aftercare-recovery-management/prd.md) › Workflow 2 (steps 3, B2, B3), Workflow 4 (D1, D4, D5), Screens 11, 13–16, 19, Business Rules |
| Platform | Admin dashboard (two steps check the provider dashboard) |
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

This batch checks how Hairline admins and the aftercare team oversee aftercare for every clinic (FR-011 › Workflow 4).

1. **Oversight.** The admin sees all aftercare cases (Screen 13) and opens a case in four tabs (Screen 14). From there the admin can edit the plan, escalate, add internal notes and review the change history.
2. **Reassignment** (Alternative Flows D1 and D5, Screen 19). When a clinic withdraws or can no longer continue, the admin moves the aftercare to another active clinic or to the Hairline aftercare team. The booking stays in Aftercare, the plan and history move with the case, and the old clinic keeps read-only history but loses all actions.
3. **Suspended clinic** (Alternative Flow D4). When a clinic is suspended:
   - Its standalone aftercare cases are cancelled automatically.
   - Its treatment-linked cases stay in Aftercare.
   - Both kinds of case are flagged "support required" for an admin.
4. **Standalone requests** (Workflow 2, Screen 15). Paid requests from patients treated elsewhere wait for an admin. The admin assigns a clinic, rejects the request with a reason (which triggers a refund), or holds it until a clinic is available.
5. **Templates** (Screen 16). The admin builds the milestone templates that clinics use, including optional pricing when a template can be bought.

These are the aftercare invariants in the Phase 2 exit gate.

**PRD gaps that affect this batch:**

- Workflow 2 B3 names the state "Awaiting provider availability", but Screen 15's Request Status list (Pending, Assigned, Active, Rejected) does not include it. A03-FR011-10 expects Workflow 2 B3.
- Screen 11 does not define which changes count as major, or which control approves or rejects a pending change. Screen 16 does not name the control that holds a change to an active template for approval.
- The Escalate Case form has no defined fields.
- The admin menu paths to the Aftercare Cases List, Standalone Aftercare Requests and Milestone Template Management are not named.

Record what you see.

## Shared Preconditions

- B01, B02 and B03 have been run in full. {A1} is a super admin. "Run day" is the day you run B04.
- These earlier setup items are in this state when B04 starts:
  - TX-1: {P1}'s aftercare case with {V1}; plan active on template "QA FUE Aftercare 12 months" (PR04-FR011-05); Current Milestone "Early recovery"; "Growth phase" 351 days.
  - AC-4: {P5}'s aftercare case with {V1}; Overdue; escalation raised by {V1} (PR04-FR011-12); custom instruction change saved and duration change on "Growth phase" to 380 days with Approval Status Pending (PR04-FR011-10).
  - AC-5: {P3}'s standalone case with {V1}; plan active (PR04-FR011-13).
  - AD-2: {P7}'s aftercare case, moved from {V3} to {V1} in A01-FR006-09 (B02).
  - {V3} and {V4} are suspended (B02 setup items AD-2 and AD-8). {V1} and {V2} are active.
- The team prepares these setup items:
  - AT-1: a standalone aftercare case for {P2} with {V4}, active before {V4} was suspended (B02 setup item AD-8); paid £400.00 GBP. The suspension cancelled it with cause ProviderSuspended and the Admin Support Required marker.
  - AT-2: a treatment-linked aftercare case for {P6} with {V4}, on a separate {P6} booking in Aftercare status, with an active plan, created before the {V4} suspension. It is kept with cause ProviderSuspended and the Admin Support Required marker.
  - AT-3: an active Hairline aftercare team member, called Team Member 1 here.
  - AT-4: three standalone aftercare requests with Payment Status Paid, Request Status Pending, Submission Date = run day − 1 day (inside the 7-day expiry), Treatment Type FUE and Requested Duration 6 months: one from {P4}, one from {P7} and one from {P2}. {V2} is listed as available for each.
- With the credentials, the plan owner gives the tester the full name of {P1}–{P7} and the name of Team Member 1.
- Test upload files listed in the data sets are supplied with this batch by the team. Long texts (201, 501, 1001 characters) are supplied as text files with the batch.
- Admin aftercare screens are reached via the main menu; record the path you used in Notes the first time.

## Test Data Sets

| Data set | Purpose | Values | Account |
|---|---|---|---|
| DS-A03-01 | Cases across clinics | TX-1, AC-4, AC-5 and AD-2 (all {V1}); AT-1 and AT-2 ({V4}). Internal note "Patient asked about scan schedule; follow up next week"; escalation text "Admin review requested after missed scans" | {A1} |
| DS-A03-02 | Admin plan edit | TX-1's plan: "Growth phase" Milestone Duration 351 to 358 days; Change Reason "Surgeon requested a longer growth phase" | {A1} |
| DS-A03-03 | Reassign to another clinic | TX-1's case from {V1} to {V2}; Reassignment Reason "Clinic asked to hand over aftercare due to capacity". Invalid reasons: "Too short" (9 characters) and a text of 1001 characters | {A1} |
| DS-A03-04 | Reassign to Hairline team | AC-4 from {V1} to Team Member 1; Reassignment Reason "Clinic withdrew from aftercare for this patient" | {A1} |
| DS-A03-05 | Suspended clinic cases | AT-1 and AT-2; reassign AT-2 to {V1} with reason "Original clinic suspended; continuing aftercare with new clinic" | {A1} |
| DS-A03-06 | Standalone requests | AT-4: {P4}'s request (assign to {V2}), {P7}'s request (reject), {P2}'s request (hold). Rejection Reason "Treatment documents do not show a hair transplant procedure"; a Rejection Reason of 501 characters | {A1} |
| DS-A03-07 | Template Management | New Template Name "QA Phase 2 FUE Recovery 6 months"; duplicate name "QA FUE Aftercare 12 months"; Template Name of 201 characters; Template Description of 1001 characters, then "Six-month FUE recovery with weekly scans"; Treatment Type FUE; milestones "Healing check" (14 days) and "Month one review" (30 days), each with 3D Scan Frequency Weekly, Questionnaire Set "QA Aftercare Check-in", Questionnaire Frequency Weekly. Pricing: Service Description of 501 characters, then "Six-month guided recovery with scan reviews"; Currency USD, Fixed Price 300.00, Monthly Subscription Price 60.00. Resources: guide.pdf (PDF, 5 MB, Resource Title "Recovery guide", valid) and video-large.mp4 (MP4, 101 MB, Resource Title "Recovery video", over the 100 MB limit). Active template edit: "Early recovery" in "QA FUE Aftercare 12 months" from 14 to 21 days | {A1} |

## Test Cases

| ID | Title | Priority | PRD flow ref | Preconditions | Test data | Steps | Expected result | Actual result / data | Result | Notes | Evidence | Bug ID | Bug status | Last tested |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A03-FR011-01 r1 | Admin Aftercare Cases List shows every clinic's cases | High | FR-011 › Screen 13 | Signed in as {A1}; DS-A03-01 cases in their Shared Preconditions state | DS-A03-01 | 1. Open the admin Aftercare Cases List (reach via the main menu; record the path you used in Notes).<br>2. Check the columns.<br>3. Search by the Case ID shown in {P1}'s row.<br>4. Clear the search. Filter Provider = {V1}; clear it and filter Aftercare Type = Standalone; clear it and filter Status = Overdue; clear it and filter Date range = B03 run day − 31 days to B03 run day − 29 days (AC-4's Aftercare Start Date was set from the B03 run day; ask the plan owner for the B03 run day if you did not run B03).<br>5. Clear the filters and open the Action menu on {P1}'s row. | 1. (step 1) Cases from {V1} and {V4} are listed, with both Treatment-linked and Standalone in Aftercare Type.<br>2. (step 2) Columns: Case ID, Patient Name, Phone Number, Age, Problem, Treatment & Package, Provider, Aftercare Type, Start Date, Current Milestone, Progress, Med Alerts, Status, Action.<br>3. (step 3) Only {P1}'s case is listed.<br>4. (step 4) Provider {V1}: {P1}, {P3}, {P5} and {P7}, no {V4} case. Standalone: every row is Standalone and {P3} is listed. Overdue: every row is Overdue and {P5} is listed. Date range: {P5} is listed and {P1} is not.<br>5. (step 5) Action offers View, Edit, Reassign and Escalate. | | Not tested | | | | — | |
| A03-FR011-02 r1 | Case details show all four tabs including the clinic's escalation | Medium | FR-011 › Screen 14 | Run after A03-FR011-01. AC-4 has {V1}'s escalation and plan changes | DS-A03-01 | 1. Click View on {P5}'s case.<br>2. Open Tab 1 Case Overview, Tab 2 Progress Tracking, Tab 3 Communication Log and Tab 4 Admin Actions in turn. | 1. (step 2) Each tab loads {P5}'s data with no error. Tab 3 Escalation History shows {V1}'s escalation "Patient reports persistent redness at donor area after 30 days". Tab 4 shows Edit Aftercare Plan, Reassign Provider, Escalate Case and Add Notes, and Change History with Change Date, Changed By and Change Reason, including {V1}'s custom instruction change and duration request. | | Not tested | | | | — | |
| A03-FR011-03 r1 | Admin edits a plan with a reason and sees admin-only controls | Medium | FR-011 › Screen 11 (admin); Workflow 4 step 2 | Run after A03-FR011-01. TX-1's "Growth phase" is 351 days; AC-4 has a Pending duration change | DS-A03-01, DS-A03-02 | 1. Open {P1}'s case and click Edit Aftercare Plan.<br>2. Check the actions offered.<br>3. Change "Growth phase" to 358 days and save with Change Reason empty.<br>4. Enter the Change Reason and save.<br>5. Open {P5}'s case, click Edit Aftercare Plan and find the duration change from {V1}. Do not approve or reject it. | 1. (step 2) Change Milestone Structure, Modify Template Assignment, Override Settings and Reassign Provider are shown.<br>2. (step 3) Save is blocked with an error on Change Reason.<br>3. (step 4) "Growth phase" shows 358 days, and Change History lists the change with {A1}, the time and the reason.<br>4. (step 5) The change ("Growth phase" to 380 days) shows Approval Status Pending, with one control to approve and one to reject. Copy their labels into Actual result. | | Not tested | | | | — | |
| A03-FR011-04 r1 | Admin reassigns aftercare to another clinic | High | FR-011 › Workflow 4 D1 and D5; Screen 19 | Run after A03-FR011-03: TX-1's case is with {V1} | DS-A03-03 | 1. In {P1}'s case, open Tab 4 Admin Actions and click Reassign Provider.<br>2. Check Case Reference, Current Aftercare Provider or Team, and Provider Status and Cause.<br>3. Select Reassignment Target Type = another provider, New Provider = {V2}, and enter the Reassignment Reason.<br>4. Read the Confirmation Summary and click Confirm Reassignment.<br>5. Check the Provider shown on the case, the booking status in the Bookings Management Dashboard and Change History.<br>6. Sign out. Sign in as {V2} and open {P1}'s case from the provider Aftercare Cases List.<br>7. Sign out. Sign in as {V1} and open {P1}'s case. | 1. (step 2) Current Aftercare Provider shows {V1}, and Provider Status shows Active.<br>2. (step 4) The summary names {V1} to {V2} and the reason; a success confirmation appears.<br>3. (step 5) The case shows {V2}; TX-1's Booking Status is still Aftercare; Change History records {V1}, {V2}, the reason and {A1}.<br>4. (step 6) {V2} sees the plan with "Growth phase" 358 days, Paracetamol and the earlier history, and Adjust Plan is shown.<br>5. (step 7) {V1} can open the case history read-only; Adjust Plan, Request Additional Scan and Escalate Case are not shown. | | Not tested | | | | — | |
| A03-FR011-05 r1 | Reassignment rejects invalid targets and reasons | Medium | FR-011 › Screen 19 validation | Run after A03-FR011-01: AC-4 is with {V1} | DS-A03-03, DS-A03-04 | 1. In {P5}'s case, click Reassign Provider.<br>2. Select Reassignment Target Type = another provider and open New Provider.<br>3. Select {V2} and enter Reassignment Reason "Too short".<br>4. Paste the 1001-character reason.<br>5. Clear New Provider, enter a valid reason and check Confirm Reassignment.<br>6. Click Cancel. | 1. (step 2) {V2} is offered; {V1} (current), {V3} and {V4} (suspended) are not.<br>2. (step 3) The reason is rejected as under 10 characters.<br>3. (step 4) The reason is rejected or cut off at 1000 characters.<br>4. (step 5) Confirm Reassignment is disabled.<br>5. (step 6) The case still shows {V1}. | | Not tested | | | | — | |
| A03-FR011-06 r1 | Admin hands a case to the Hairline aftercare team | Medium | FR-011 › Workflow 4 D1; Screen 19 | Run after A03-FR011-05: AC-4 is with {V1} | DS-A03-04 | 1. In {P5}'s case, click Reassign Provider.<br>2. Select Reassignment Target Type = Hairline aftercare team.<br>3. Select New Aftercare Team Member = Team Member 1, enter the Reassignment Reason and click Confirm Reassignment.<br>4. Check the case and Change History.<br>5. Sign out. Sign in as {V1} and open {P5}'s case. | 1. (step 2) New Aftercare Team Member appears and New Provider is not shown.<br>2. (step 3) A success confirmation appears.<br>3. (step 4) The case shows Team Member 1 as assignee; the booking is still Aftercare; Change History records the move with the reason.<br>4. (step 5) {V1} can read the history; Adjust Plan, Request Additional Scan and Escalate Case are not shown. | | Not tested | | | | — | |
| A03-FR011-07 r1 | Suspended clinic: standalone case cancelled, treatment-linked case kept and reassigned | High | FR-011 › Workflow 4 D4 and D5; Screen 19 (Resolve Support Marker); Screen 14 | AT-1 is cancelled and AT-2 is kept, both with cause ProviderSuspended. Signed in as {A1} | DS-A03-05 | 1. Open {P2}'s standalone case AT-1.<br>2. Check its status, cause, marker, intake and payment, and the actions on Tab 4.<br>3. Open {P6}'s treatment-linked case AT-2.<br>4. Check its status, cause, marker and the booking status.<br>5. Click Reassign Provider and check Provider Status and Cause and Resolve Support Marker.<br>6. Select another provider, New Provider = {V1}, enter the reason and click Confirm Reassignment.<br>7. Check AT-2 and Change History. | 1. (step 2) AT-1 is cancelled with cause ProviderSuspended and shows support required; intake data and the £400.00 payment are still shown; Reassign Provider is not shown.<br>2. (step 4) AT-2 is not cancelled; its booking is still Aftercare; it shows cause ProviderSuspended and support required.<br>3. (step 5) Provider Status and Cause show suspended, ProviderSuspended; Resolve Support Marker is shown and ticked.<br>4. (step 6) A success confirmation appears.<br>5. (step 7) AT-2 shows {V1} as provider and the support marker is resolved; Change History records the reassignment with {A1} and the reason. | | Not tested | | | | — | |
| A03-FR011-08 r1 | Admin assigns a standalone request to a clinic | High | FR-011 › Workflow 2 step 3; Screen 15 | AT-4 requests are Pending. Signed in as {A1} | DS-A03-06 | 1. Open Standalone Aftercare Requests (reach via the main menu; record the path you used in Notes).<br>2. Open {P4}'s request and check its details.<br>3. Check Assign Provider before selecting a provider.<br>4. Select {V2} in Available Providers and click Assign Provider.<br>5. Sign out. Sign in as {V2} and open the provider Aftercare Cases List. | 1. (step 2) The request shows Request ID, Submission Date (run day − 1 day), Patient Name, Email and Phone, Treatment Date, Treatment Type FUE, Treatment Clinic, Requested Duration 6 months, Payment Method, Payment Status Paid and Request Status Pending. Available Providers shows Provider Name, Specialization and Availability.<br>2. (step 3) Assign Provider is disabled.<br>3. (step 4) Request Status shows Assigned.<br>4. (step 5) {P4}'s standalone case is listed with no plan yet. | | Not tested | | | | — | |
| A03-FR011-09 r1 | Admin rejects a standalone request with a reason | Medium | FR-011 › Workflow 2 B2; Screen 15 | {P7}'s AT-4 request is Pending. Signed in as {A1} | DS-A03-06 | 1. Open {P7}'s request and click Reject Request.<br>2. Submit with Rejection Reason empty.<br>3. Paste the 501-character reason and submit.<br>4. Enter the valid reason and submit.<br>5. Check Request Status, the stored reason and Payment Status. | 1. (step 2) Submission is blocked with an error on Rejection Reason.<br>2. (step 3) The reason is rejected or cut off at 500 characters.<br>3. (step 4) A success confirmation appears.<br>4. (step 5) Request Status is Rejected and shows the reason. The request shows that a refund was started, with no manual refund step; copy what is shown into Actual result. | | Not tested | | | | — | |
| A03-FR011-10 r1 | Admin holds a request while no clinic is available | Low | FR-011 › Workflow 2 B3 | {P2}'s AT-4 request is Pending. Signed in as {A1} | DS-A03-06 | 1. Open {P2}'s request and copy the label of every action control into Actual result.<br>2. Click the control that marks the request "Awaiting provider availability" and confirm.<br>3. Return to Standalone Aftercare Requests and find {P2}'s request. | 1. (step 1) A control to mark the request "Awaiting provider availability" is shown (Workflow 2 B3).<br>2. (step 2) The request shows "Awaiting provider availability" and has no assigned provider.<br>3. (step 3) The list shows {P2}'s request in that state. | | Not tested | | | | — | |
| A03-FR011-11 r1 | Admin creates a milestone template with valid fields | Medium | FR-011 › Screen 16 (Template Editor) | Signed in as {A1}; "QA FUE Aftercare 12 months" exists | DS-A03-07 | 1. Open Milestone Template Management (reach via the main menu; record the path you used in Notes) and start a new template.<br>2. Paste the 201-character Template Name; then enter "QA FUE Aftercare 12 months" and try to save.<br>3. Paste the 1001-character Template Description.<br>4. Enter the new name and valid description, select Treatment Type FUE and add the two milestones from DS-A03-07, opening the Questionnaire Set list on the first.<br>5. Save.<br>6. Check the template list. | 1. (step 2) The 201-character name is rejected or cut off at 200; the duplicate name is rejected with a message.<br>2. (step 3) The description is rejected or cut off at 1000 characters.<br>3. (step 4) Questionnaire Set offers "QA Aftercare Check-in" and not "QA Inquiry Intake".<br>4. (step 5) A success confirmation appears.<br>5. (step 6) "QA Phase 2 FUE Recovery 6 months" is listed with Number of Milestones 2 and Usage Count 0. | | Not tested | | | | — | |
| A03-FR011-12 r1 | Purchase pricing fields become required when a template is for sale | Medium | FR-011 › Screen 16 (Pricing Configuration) | Run after A03-FR011-11: "QA Phase 2 FUE Recovery 6 months" exists and is not for sale | DS-A03-07 | 1. Edit the new template and tick Enable for Purchase.<br>2. Save with Service Description and Pricing Model empty.<br>3. Paste the 501-character Service Description, then replace it with the valid one.<br>4. Select Pricing Model = Both, add Currency USD with Fixed Price 300.00 only, and save.<br>5. Add Monthly Subscription Price 60.00 and save with Default Payment Method empty.<br>6. Select the first Default Payment Method option (copy it into Actual result) and save. | 1. (step 2) Save is blocked with errors on Service Description, Pricing Model and Multi-Currency Pricing.<br>2. (step 3) The 501-character text is rejected or cut off at 500; the valid text is accepted.<br>3. (step 4) Save is blocked with an error on Monthly Subscription Price.<br>4. (step 5) Save is blocked with an error on Default Payment Method.<br>5. (step 6) A success confirmation appears and the template shows as available for purchase at USD 300.00 fixed and USD 60.00 monthly. | | Not tested | | | | — | |
| A03-FR011-13 r1 | Templates in use cannot be deleted and resource files are size-limited | Medium | FR-011 › Screen 16 Business Rules | Run after A03-FR011-11. "QA FUE Aftercare 12 months" has Usage Count above 0 | DS-A03-07 | 1. On "QA Phase 2 FUE Recovery 6 months", add a resource: Resource Title "Recovery guide", Resource Type PDF, file guide.pdf; save.<br>2. Add a resource: Resource Title "Recovery video", Resource Type video, file video-large.mp4.<br>3. Click delete on "QA FUE Aftercare 12 months" and confirm.<br>4. Edit "QA FUE Aftercare 12 months", change "Early recovery" from 14 to 21 days and save.<br>5. Reopen "QA FUE Aftercare 12 months". | 1. (step 1) The 5 MB PDF uploads and is listed.<br>2. (step 2) The 101 MB file is rejected with a message about the 100 MB limit.<br>3. (step 3) Deletion is blocked with a message that the template is in use; the template is still listed.<br>4. (step 4) A message says the change needs approval.<br>5. (step 5) "Early recovery" still shows 14 days, and the change is shown as pending approval (record the label). | | Not tested | | | | — | |
| A03-FR011-14 r1 | Admin adds an internal note and escalates a case | Medium | FR-011 › Screen 14 Tab 4 | Run after A03-FR011-01. AC-5 ({P3}) is with {V1} | DS-A03-01 | 1. Open {P3}'s case and go to Tab 4 Admin Actions.<br>2. Click Add Notes, enter the internal note and save.<br>3. Click Escalate Case. Enter the escalation text in the free-text field; for any choice field select the first option. Copy every field label and chosen value into Actual result. Submit.<br>4. Check Change History and Tab 3 Communication Log.<br>5. Sign out. Sign in as {V1} and open {P3}'s case from the Aftercare Cases List. | 1. (step 2) The note is saved and shown with {A1} and the time.<br>2. (step 3) A confirmation appears.<br>3. (step 4) Change History lists the note and the escalation; Escalation History on Tab 3 shows the escalation text.<br>4. (step 5) {V1} does not see the internal note text anywhere on the case. | | Not tested | | | | — | |

## Batch Summary

| Total | Pass | Fail | Blocked | Not tested | Open bugs |
|---|---|---|---|---|---|
| 14 | 0 | 0 | 0 | 14 | 0 |

## Case Change Log

| Case | Revision | Date | Change |
|---|---|---|---|
| A03-FR011-01 | r1 | 2026-10-19 | Created |
| A03-FR011-02 | r1 | 2026-10-19 | Created |
| A03-FR011-03 | r1 | 2026-10-19 | Created |
| A03-FR011-04 | r1 | 2026-10-19 | Created |
| A03-FR011-05 | r1 | 2026-10-19 | Created |
| A03-FR011-06 | r1 | 2026-10-19 | Created |
| A03-FR011-07 | r1 | 2026-10-19 | Created |
| A03-FR011-08 | r1 | 2026-10-19 | Created |
| A03-FR011-09 | r1 | 2026-10-19 | Created |
| A03-FR011-10 | r1 | 2026-10-19 | Created |
| A03-FR011-11 | r1 | 2026-10-19 | Created |
| A03-FR011-12 | r1 | 2026-10-19 | Created |
| A03-FR011-13 | r1 | 2026-10-19 | Created |
| A03-FR011-14 | r1 | 2026-10-19 | Created |
