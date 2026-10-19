# B05 — A-04 Travel Oversight

## Batch Control

| Field | Value |
|---|---|
| Batch | B05 |
| Phase / plan version | Phase 2 / v1.0 |
| Module | A-04 — Travel oversight within confirmed bookings (admin dashboard) |
| FRs | FR-008 (admin Screens 11–12); FR-006 Change Appointment and Cancel Booking as triggers |
| PRD sources | [FR-008 PRD](../../../../../../project-requirements/functional-requirements/fr008-travel-booking-integration/prd.md) › Screens 11–12, Alternative Flow A2, Business Rules (travel-date review, closed context, early departure, record limits, passport visibility), Acceptance Scenarios 6–8 |
| Platform | Admin dashboard (one step checks the provider dashboard) |
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

This batch checks how a Hairline admin oversees travel for confirmed bookings. There is no separate travel dashboard: travel appears as a **Travel** section inside the admin booking detail (FR-008 › Screen 11), and the full records open in Screen 12 through **Apply Correction**.

1. **Two travel paths.**
   - **Path A (Provider-included):** the clinic arranges flights and hotel, and the patient only submits a passport.
   - **Path B (Patient self-booked):** the patient submits their own flights and hotel, and no passport is collected.
2. **Status and reminders.** Each record shows Awaiting, Submitted or Not included. The admin can send **Re-notify patient** only for items the patient still owes: the passport in Path A, or flights and hotel in Path B, unless the patient said no travel is needed.
3. **Corrections.** Submitted records are locked for the patient and the clinic. Only an admin can correct them. A correction needs a reason, creates a new locked version, keeps the old one as superseded, and notifies the patient and the clinic.
4. **Date changes and cancellations.**
   - When an admin moves the appointment (B02), the travel context needs a date review until the admin confirms or corrects the travel dates.
   - A return flight or hotel check-out before the last treatment day triggers an early-departure warning.
   - When a booking is cancelled, the travel context closes and becomes read-only.

These checks cover the travel part of the Phase 2 clinical acceptance tests.

**PRD gaps that affect this batch:**

- The roadmap describes "system-wide travel oversight", but FR-008 deliberately has no separate travel dashboard. These cases follow the PRD.
- FR-008 says an admin can override `no_travel_required` from Screen 11, but it does not name the control. A04-FR008-05 records the label.
- The text of the early-departure warning and of the confirmation shown after Confirm Travel Dates is not defined.
- FR-008 does not say which Passport Status follows an admin correction of an Incomplete passport, and it keeps the superseded passport version only in backend records (no on-screen version history). A04-FR008-07 records the status shown and checks the change through Audit & History.
- The admin menu path to the Bookings Management Dashboard is not named.

Record what you see.

## Shared Preconditions

- B02 has been run in full. {A1} is a super admin. "B01 run day" and "B02 run day" are the days those batches were run.
- Open bookings from the Bookings Management Dashboard (reach via the main menu; record the path you used in Notes), search the patient's full name and click View Details. The Travel section is on that page. Apply Correction opens Screen 12.
- Provider checks use the provider dashboard: Patient Management > Confirmed list > the booking.
- With the credentials, the plan owner gives the tester the full name of {P2}, {P3}, {P4}, {P5} and {P7}.
- The team prepared these setup items before B02 started:
  - TR-1: travel on TX-2 ({P2} with {V1}, 3-day plan, first booked for B01 run day + 5 days). Path B. Outbound flight submitted by {P2}: Turkish Airlines, Flight Number TK1980, London Heathrow (LHR) to Istanbul (IST), departing B01 run day + 4 days at 10:15. Hotel submitted by {P2}: check-in B01 run day + 4 days, check-out B01 run day + 8 days. Return flight not submitted.
  - TR-2: a Confirmed booking for {P5} with {V2}, appointment B02 run day + 40 days at 10:00. Path A (flights and hotel included by the clinic). Passport not submitted (Awaiting). {V2} entered the outbound flight: Turkish Airlines TK1972, LHR to IST, departing the day before the appointment at 09:00.
  - TR-3: a Confirmed booking for {P4} with {V2}, appointment B02 run day + 45 days at 10:00. Path A. Passport submitted by {P4} with Passport Number QA7654321, Date of Birth 15/01/1990, Nationality United Kingdom, Place of Birth London, Date of Issue 01/03/2020, Date of Expiry 01/03/2021 (wrong; {P4} later told support it is 01/03/2030) and a passport photo. Acting as an admin, the team then marked the passport Incomplete (FR-008 Screen 11: Incomplete is set by an admin, not by a missing field). {V2} entered the hotel.
  - TR-4: a Confirmed booking for {P7} with {V2}, appointment B02 run day + 50 days at 10:00. Path B. {P7} answered that no travel is required.
  - TR-5: travel on TX-3 ({P3} with {V1}). Path B. Outbound flight submitted by {P3}. TX-3 was cancelled in A01-FR006-08 (B02).
- After B02, TX-2's appointment is B02 run day + 14 days at 10:00 (A01-FR006-03), so its treatment days are B02 run day + 14, + 15 and + 16 days. The travel dates have not been confirmed since.

## Test Data Sets

| Data set | Purpose | Values | Account |
|---|---|---|---|
| DS-A04-01 | Path B with a moved appointment | TR-1 on TX-2 ({P2} with {V1}). Confirm Travel Dates reason: "Patient confirmed by phone that the booked flight and hotel remain their plan" | {A1} |
| DS-A04-02 | Path A with passport awaiting | TR-2 ({P5} with {V2}) | {A1} |
| DS-A04-03 | Path A with an incomplete passport | TR-3 ({P4} with {V2}). Correction: Date of Expiry 01/03/2021 to 01/03/2030; Reason for correction "Patient sent the expiry date to support by email". Change without a reason: Place of Birth "London" to "Londen" | {A1} |
| DS-A04-04 | No travel required | TR-4 ({P7} with {V2}) | {A1} |
| DS-A04-05 | Closed context | TR-5 on {P3}'s cancelled TX-3 with {V1} | {A1} |
| DS-A04-06 | Flight and hotel corrections | {P2}'s outbound flight: Flight Number TK1980 to TK1984, Departure Time 10:15 to 13:40; Reason for correction "Airline changed the flight number". {P2}'s hotel: Check-Out Date = B02 run day + 15 days (before treatment Day 3); Reason for correction "Patient moved hotel dates after appointment change". Soft delete of {P5}'s outbound flight with reason "Duplicate entry made by clinic" | {A1} |

## Test Cases

| ID | Title | Priority | PRD flow ref | Preconditions | Test data | Steps | Expected result | Actual result / data | Result | Notes | Evidence | Bug ID | Bug status | Last tested |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A04-FR008-01 r1 | Travel section shows Path B status and the date review after an appointment change | High | FR-008 › Screen 11; Business Rules (travel-date review); Acceptance Scenario 6 | Run after A01-FR006-03 (B02): TX-2 is moved to B02 run day + 14 days; travel dates not confirmed | DS-A04-01 | 1. Open {P2}'s TX-2 booking (View Details).<br>2. Scroll to the Travel section.<br>3. Check Booking and Accepted Choice, Travel Path and each status badge.<br>4. Check Travel Context Status and the actions shown. | 1. (step 2) The Travel section is inside the booking detail; there is no separate travel page.<br>2. (step 3) Booking and Accepted Choice shows the current appointment B02 run day + 14 days at 10:00 and the accepted baseline B01 run day + 5 days. Travel Path shows Patient self-booked (Path B), and Passport Status is not shown. Outbound Flight and Hotel show Submitted; Return Flight shows Awaiting.<br>3. (step 4) Travel Context Status shows Travel-date review required, with the baseline, the current appointment, and the flight (B01 run day + 4 days) and hotel dates flagged. Confirm Travel Dates is shown. | | Not tested | | | | — | |
| A04-FR008-02 r1 | Admin confirms travel dates and the review clears | High | FR-008 › Screen 11 (Confirm Travel Dates); Business Rules | Run after A04-FR008-01: TX-2 shows Travel-date review required | DS-A04-01 | 1. In {P2}'s Travel section, click Confirm Travel Dates, enter the reason from DS-A04-01 and confirm (if no reason field is shown, say so in Notes). Copy the message shown into Actual result.<br>2. Check Travel Context Status and the actions shown.<br>3. Open Audit & History on the booking. | 1. (step 1) A success message is shown.<br>2. (step 2) Travel Context Status shows Active, and Confirm Travel Dates is not shown.<br>3. (step 3) The audit records the travel-date confirmation with {A1}, the time (within 2 minutes of step 1), the reason and the outcome. | | Not tested | | | | — | |
| A04-FR008-03 r1 | Admin re-notifies a Path B patient about a missing return flight | Medium | FR-008 › Screen 11 (Re-notify patient) | Run after A04-FR008-02: TX-2 is Active; Return Flight is Awaiting | DS-A04-01 | 1. In {P2}'s Travel section, check the Return Flight row.<br>2. Click Re-notify patient for the return flight.<br>3. Open Audit & History.<br>4. Click Apply Correction and open the Flight Details tab. | 1. (step 1) Re-notify patient is offered for the return flight.<br>2. (step 2) A confirmation is shown.<br>3. (step 3) The re-notification is recorded with {A1} and the time.<br>4. (step 4) The Return section shows "Return flight not yet submitted." | | Not tested | | | | — | |
| A04-FR008-04 r1 | Path A: only the passport can be re-notified | Medium | FR-008 › Screens 11, 12 (Tab 1 Passport) | TR-2 is in its setup state | DS-A04-02 | 1. Open {P5}'s TR-2 booking and check the Travel section.<br>2. Check which rows offer Re-notify patient.<br>3. Click Re-notify patient on the passport row.<br>4. Click Apply Correction and open the Passport tab. | 1. (step 1) Travel Path shows Provider-included (Path A); Passport Status shows Awaiting; Outbound Flight shows Submitted.<br>2. (step 2) Only the passport row offers Re-notify patient; the flight and hotel rows do not.<br>3. (step 3) A confirmation is shown, and Audit & History records it.<br>4. (step 4) The Passport tab shows "Awaiting submission" and a Re-notify patient button. | | Not tested | | | | — | |
| A04-FR008-05 r1 | No re-notify when the patient said no travel is needed | Low | FR-008 › Screen 11; Business Rules (no_travel_required) | TR-4 is in its setup state | DS-A04-04 | 1. Open {P7}'s TR-4 booking with {V2} and check the Travel section.<br>2. Copy the label of every action control in the Travel section into Actual result. | 1. (step 1) The Travel section shows that no travel is required.<br>2. (step 2) Re-notify patient is not shown. A control to override the no-travel answer is shown (FR-008 Business Rules; label not named in the PRD). | | Not tested | | | | — | |
| A04-FR008-06 r1 | Passport tab shows the full record to the admin | High | FR-008 › Screen 12 Tab 1; Business Rules (passport visibility) | TR-3 is in its setup state (Passport Status Incomplete) | DS-A04-03 | 1. Open {P4}'s TR-3 booking with {V2} and click Apply Correction.<br>2. Check the Screen 12 header.<br>3. Open the Passport tab and review each field.<br>4. Click the passport photo and check the controls in the viewer. | 1. (step 2) The header shows Booking Reference, Accepted Subquote, Patient Name, Provider / Clinic, Appointment Date, Travel Path and Overall Status.<br>2. (step 3) The tab shows Full Name, Passport Number QA7654321 in full (not masked), Date of Birth 15/01/1990, Gender, Location (Nationality) United Kingdom, Place of Birth London, Date of Issue 01/03/2020, Date of Expiry 01/03/2021, Submitted By {P4} and Status Incomplete, and says an admin correction is needed.<br>3. (step 4) The photo opens for viewing, and no download control is shown. | | Not tested | | | | — | |
| A04-FR008-08 r1 | A correction without a reason is blocked | Medium | FR-008 › Screen 12 (Reason for correction) | Run after A04-FR008-06 and before A04-FR008-07 and A04-FR008-09. {P2}'s outbound Flight Number is TK1980 | DS-A04-03, DS-A04-06 | 1. On {P4}'s Passport tab, change Place of Birth to "Londen" and save with Reason for correction empty.<br>2. Cancel the change.<br>3. Open {P2}'s TX-2 booking, click Apply Correction, change the outbound Flight Number to TK1984 and save with Reason for correction empty.<br>4. Cancel the change and reopen both records. | 1. (step 1) Save is blocked with a message asking for a reason.<br>2. (step 3) Save is blocked with a message asking for a reason.<br>3. (step 4) Place of Birth shows London and Flight Number shows TK1980; Audit & History has no correction entry for either record. | | Not tested | | | | — | |
| A04-FR008-07 r1 | Admin corrects a passport with a reason and a new version is created | High | FR-008 › Screen 12 Tab 1 Business Rules; Screen 11 (Incomplete status); Alternative Flow A2 | Run after A04-FR008-06 and A04-FR008-08: {P4}'s passport is Incomplete with Place of Birth London and Date of Expiry 01/03/2021 | DS-A04-03 | 1. On {P4}'s Passport tab, change Date of Expiry to 01/03/2030.<br>2. Enter the Reason for correction and save.<br>3. Check the Passport tab status and fields.<br>4. Close Screen 12 and check the Travel section and Audit & History.<br>5. Sign out. Sign in as {V2} and open {P4}'s TR-3 booking. | 1. (step 2) The correction saves.<br>2. (step 3) Date of Expiry shows 01/03/2030 and has no patient or provider edit route. Copy the Status shown into Actual result (FR-008 does not state the status after a correction, and the previous version is kept only in backend records, so no version history is expected on screen).<br>3. (step 4) Passport Status matches the tab status. The audit shows {A1}, the time, the reason, and Date of Expiry before (01/03/2021) and after (01/03/2030).<br>4. (step 5) {V2} sees the corrected Date of Expiry and has no edit control on the passport. | | Not tested | | | | — | |
| A04-FR008-09 r1 | Admin corrects a Path B flight | Medium | FR-008 › Screen 12 Tab 2; Business Rules (max 2 current flight records) | Run after A04-FR008-03 and A04-FR008-08: {P2}'s outbound flight is TK1980 at 10:15 | DS-A04-06 | 1. Open {P2}'s TX-2 booking and click Apply Correction.<br>2. Check which tabs are shown.<br>3. On Flight Details, change the outbound Flight Number to TK1984 and Departure Time to 13:40, enter the Reason for correction and save.<br>4. Check the outbound flight shown and Audit & History. | 1. (step 2) No Passport tab is shown.<br>2. (step 3) The outbound flight saves as a new locked version showing TK1984 at 13:40.<br>3. (step 4) There is one current outbound flight record (TK1984). The audit shows {A1}, the time, the reason, and TK1980 at 10:15 before and TK1984 at 13:40 after (FR-008 Business Rules: both versions are kept in the audit log). | | Not tested | | | | — | |
| A04-FR008-10 r1 | Early check-out triggers a warning that must be acknowledged | High | FR-008 › Business Rules (early departure); Screen 12 Tab 3; Acceptance Scenario 8 | Run after A04-FR008-02: TX-2's treatment days are B02 run day + 14 to + 16 days | DS-A04-06 | 1. On {P2}'s Hotel Details tab, set Check-Out Date to B02 run day + 15 days.<br>2. Enter the Reason for correction and click save without acknowledging the warning.<br>3. Acknowledge the warning and save.<br>4. Sign out. Sign in as {V1} and open {P2}'s TX-2 booking. | 1. (step 1) A warning says check-out is before the last treatment day. Copy its text into Actual result.<br>2. (step 2) Save is blocked until the warning is acknowledged.<br>3. (step 3) The hotel record saves as a new version with check-out B02 run day + 15 days.<br>4. (step 4) {V1} sees an early-departure flag on the booking. | | Not tested | | | | — | |
| A04-FR008-11 r1 | A cancelled booking's travel is closed and read-only | High | FR-008 › Screen 11 (closed context); Acceptance Scenario 7 | Run after A01-FR006-08 (B02): TX-3 with {V1} is Cancelled | DS-A04-05 | 1. Search {P3}'s full name and open the cancelled TX-3 booking with {V1}.<br>2. Check Travel Context Status and the actions shown.<br>3. Open the outbound flight record and check its controls. | 1. (step 2) Travel Context Status shows Closed. Re-notify patient, Apply Correction and Confirm Travel Dates are not shown.<br>2. (step 3) The outbound flight details can be read, and no edit or delete control is shown. | | Not tested | | | | — | |
| A04-FR008-12 r1 | Admin soft-deletes a record with a reason | Medium | FR-008 › Screen 12 (soft delete) | Run after A04-FR008-04: {P5}'s outbound flight TK1972 is current | DS-A04-06 | 1. Open {P5}'s TR-2 booking and click Apply Correction.<br>2. On Flight Details, delete the outbound flight with the reason empty.<br>3. Delete it again with the reason.<br>4. Check the flight history, the Travel section and Audit & History. | 1. (step 2) Deleting is blocked with a message asking for a reason.<br>2. (step 3) The deletion succeeds.<br>3. (step 4) TK1972 is no longer a current record but is kept in history. Outbound Flight in the Travel section no longer shows Submitted. The audit records the deletion with {A1} and the reason. | | Not tested | | | | — | |

## Batch Summary

| Total | Pass | Fail | Blocked | Not tested | Open bugs |
|---|---|---|---|---|---|
| 12 | 0 | 0 | 0 | 12 | 0 |

## Case Change Log

| Case | Revision | Date | Change |
|---|---|---|---|
| A04-FR008-01 | r1 | 2026-10-19 | Created |
| A04-FR008-02 | r1 | 2026-10-19 | Created |
| A04-FR008-03 | r1 | 2026-10-19 | Created |
| A04-FR008-04 | r1 | 2026-10-19 | Created |
| A04-FR008-05 | r1 | 2026-10-19 | Created |
| A04-FR008-06 | r1 | 2026-10-19 | Created |
| A04-FR008-07 | r1 | 2026-10-19 | Created |
| A04-FR008-08 | r1 | 2026-10-19 | Created |
| A04-FR008-09 | r1 | 2026-10-19 | Created |
| A04-FR008-10 | r1 | 2026-10-19 | Created |
| A04-FR008-11 | r1 | 2026-10-19 | Created |
| A04-FR008-12 | r1 | 2026-10-19 | Created |
