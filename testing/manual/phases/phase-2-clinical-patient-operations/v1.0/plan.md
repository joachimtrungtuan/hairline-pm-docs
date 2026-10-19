# Phase 2 Manual Test Plan — Clinical and Patient Operations

## Document Control

| Field | Value |
|---|---|
| Phase | Phase 2 — Clinical and Patient Operations |
| Plan version | 1.0 |
| Status | Draft |
| Scope source | [Admin and provider implementation status and release roadmap](../../../../../reports/2026-09-06/admin-provider-implementation-status-and-release-roadmap.md) › Recommended four-phase release roadmap › P0 — Phase 2: Clinical and patient operations |
| Release objective | Safely execute paid treatment and aftercare |
| Exit gate | Billing uses current invoice routes; treatment and aftercare invariants pass; messaging uses real transport with quote eligibility and durable notifications; call functionality is either proven or excluded; clinical acceptance tests pass |
| Created | 2026-10-19 |
| Last updated | 2026-10-19 |
| Plan owner | QA lead |
| Tester(s) | TBD |

## Change Log

| Version | Date | Change | By |
|---|---|---|---|
| 1.0 | 2026-10-19 | Initial plan | QA lead |

## 1. Scope

### 1.1 In Scope

| Module | Function slice in this phase | FRs | Batch |
|---|---|---|---|
| PR-03 | Treatment execution in the provider dashboard: Check In gates, day documentation, End Treatment, change of treatment details, provider case closure | FR-010 | B01 |
| A-01 | Admin booking intervention (Bookings Management Dashboard, Change Appointment, Cancel Booking, Revive Booking, provider-fault transfer and resolution), admin treatment oversight, Booking Support Requests and provider-impact support resolution | FR-006, FR-010, FR-016 | B02 |
| PR-04 | Provider aftercare: setup wizard, paperwork-only option, standalone activation, case list, details, plan edit, progress tracking, escalation | FR-011 | B03 |
| A-03 | Admin aftercare oversight: all-provider case list and details, plan edit, reassignment to a clinic or the Hairline aftercare team, suspension effects, standalone requests, milestone templates | FR-011 | B04 |
| A-04 | Travel section inside the admin confirmed booking detail: status, re-notify, corrections, travel-date review, early-departure warning, closed context | FR-008 | B05 |
| A-05 | Minimum invoice and refund controls | FR-007, FR-017 | B06 |
| PR-07 | Provider messaging with real transport, quote eligibility and durable notifications; call functionality proven or excluded | FR-012, FR-020, FR-022 | B07 |
| A-10 | Admin support and messaging oversight (minimum slice) | FR-012, FR-034 | B08 |

### 1.2 Out of Scope

- PR-05 provider earnings, A-05 reconciliation and payouts beyond the minimum invoice and refund controls, A-06 promotions and A-07 affiliates (Phase 3).
- A-08 analytics, the remaining A-09 configuration and advanced A-10 functions (Phase 4).
- FR-011 Screen 17 Provider Performance Dashboard and Screen 18 Aftercare Progress Tracking (Admin View), which are in the backlog.
- The FR-008 provider-side travel screens. Provider travel data is used only as prepared setup data.
- Process Refund on bookings, which is tested in B06.
- The patient mobile app. Any patient action needed for a case is existing setup data prepared by the team.

## 2. Entry and Exit Criteria

**Entry criteria** (all must hold before testing starts):

- Phase 1 exit gate passed.
- Build deployed to the test environment, with the version recorded in section 3.
- Test accounts {A1}, {S1} and {V1}–{V4} are available and verified, and {S1} has the Clinical Staff role in {V1}'s team.
- The setup data in each batch's Test Data Sets and Shared Preconditions is in place, including:
  - The bookings for {P1}–{P7} in the stated statuses and payment states.
  - At least one active aftercare milestone template and an Aftercare questionnaire set.
  - The travel records for B05.
  - The {V4} aftercare cases, created before {V4} is suspended.

**Exit criteria** (phase passes when):

- Every High-priority case in B01–B08 is Pass.
- No open bug with Bug status Found, Logged, or Reopened at High priority.
- Billing uses current invoice routes: the B06 invoice and refund cases pass.
- Treatment invariants pass (B01, B02):
  - Check In is blocked before the procedure date, while a balance is outstanding, and for Billing Staff.
  - A patient has at most one In Progress treatment.
  - The plan locks at Check In.
  - Only the five day statuses exist.
  - End Treatment opens only when every day is final.
  - Completion data is required and becomes read-only.
  - Only the treating clinic sees the case.
  - Every admin change has a reason and an audit entry, and no status is ever set by hand.
- Aftercare invariants pass (B03, B04):
  - Only the assigned clinic sees and acts on a case.
  - Activation needs every setup step to be complete.
  - Plan changes carry a reason.
  - A reassignment keeps the booking in Aftercare and moves the history.
  - The previous clinic keeps read-only history and loses its actions.
  - A suspended clinic's standalone cases are cancelled and its treatment-linked cases are kept and flagged.
- Messaging uses real transport with quote eligibility and durable notifications (B07, B08).
- Call functionality is either proven by passing cases or formally excluded and recorded in this plan's Change Log (B07).
- Clinical acceptance tests pass: B01 through B05 have no open High-priority bug.

## 3. Test Environment and Accounts

| Item | Value |
|---|---|
| Provider dashboard URL | https://admin.hairline.app (shared origin with the admin dashboard; sign in with a provider account) |
| Admin dashboard URL | https://admin.hairline.app |
| Backend API base URL | https://backend.hairline.app/api |
| Build / release under test | TBD (record before the first session) |
| Browser(s) | Chrome latest, desktop |
| Plan owner contact | {Plan owner contact} |

Accounts used (placeholders; credentials sent privately):

| Placeholder | Role | Used in batches |
|---|---|---|
| {A1} | Super admin | B01 (checks), B02, B03 (check), B04, B05, B06, B07, B08 |
| {A3} | Admin with the Billing Viewer role; to be created by the team | B06 |
| {A4} | Restricted admin 1; to be created by the team | B08 |
| {A6} | Restricted admin 2; to be created by the team | B08 |
| {A7} | Second admin with the Support Staff role; to be created by the team | B08 |
| {S1} | Provider staff, Clinical Staff in {V1}'s team (clinician-front-desk) | B01 |
| {V1} | Provider (clinic Owner); main treating clinic | B01, B02 (checks), B03, B04, B05 (check), B06, B07, B08 |
| {V2} | Provider; second clinic used for isolation, replacement and reassignment | B01, B02, B03, B04, B05, B06, B07, B08 |
| {V3} | Provider; suspended once before B02 starts, during a live treatment (setup data for B02 AD-2 and B06 INV-11); reactivated after B06 | B02, B04 (check), B06 |
| {V4} | Provider; suspended before B02 starts, with live aftercare cases and an open inquiry (setup data, B02 AD-8) | B02, B04 |
| {P1}–{P7} | Patients; booking, aftercare and travel records are setup data only (no patient sign-in) | B01–B06; B07 ({P1}–{P4}); B08 ({P1}–{P5}) |
| {P8} | Patient; one Confirmed booking (B01 setup item TX-8), setup data only; to be created by the team | B01 |

Accounts for B06–B08 are also described in those batch files.

**{V3} suspension:** the team suspends {V3} once, before B02 starts. Before suspending, the team puts B02 setup item AD-2 ({P7} with {V3}) In Progress and starts the {P5} payment with {V3} that B06 setup item INV-11 needs. {V3} stays suspended through B06, which runs last, and the team reactivates it after B06 ends. No batch from B02 onward needs {V3} active: B04 expects it suspended (A03-FR011-05), and B03, B05, B07 and B08 do not use {V3}.

## 4. Batches and Run Order

| Order | Batch | File | Module | FRs | Cases | Depends on |
|---|---|---|---|---|---|---|
| 1 | B01 | [B01-pr03-treatment-execution](batches/B01-pr03-treatment-execution.md) | PR-03 | FR-010 | 19 | — |
| 2 | B02 | [B02-a01-booking-treatment-intervention](batches/B02-a01-booking-treatment-intervention.md) | A-01 | FR-006, FR-010, FR-016 | 19 | B01 |
| 3 | B05 | [B05-a04-travel](batches/B05-a04-travel.md) | A-04 | FR-008 | 12 | B02 |
| 4 | B03 | [B03-pr04-aftercare](batches/B03-pr04-aftercare.md) | PR-04 | FR-011 | 13 | B01, B02 |
| 5 | B04 | [B04-a03-aftercare-team](batches/B04-a03-aftercare-team.md) | A-03 | FR-011 | 14 | B01, B02, B03 |
| 6 | B07 | [B07-pr07-messaging](batches/B07-pr07-messaging.md) | PR-07 | FR-012, FR-020, FR-022 | 17 | — |
| 7 | B08 | [B08-a10-support](batches/B08-a10-support.md) | A-10 | FR-012, FR-034 | 17 | B07 |
| 8 | B06 | [B06-a05-invoice-refund-controls](batches/B06-a05-invoice-refund-controls.md) | A-05 | FR-007, FR-017 | 17 | B02 |

**End-to-end journey:** The batches follow a paid patient from the procedure day to recovery.

1. **B01:** a clinic checks the patient in, documents each treatment day and ends the treatment. The case moves to Aftercare.
2. **B02:** a Hairline admin oversees the same treatments. The admin handles the clinic's postponement and closure requests, reschedules, cancels, revives or transfers bookings, and resolves patient support requests.
3. **B05:** the appointment change from B02 is followed through to the travel records, where the admin confirms or corrects flights, hotel and passport.
4. **B03:** the clinic sets up and runs aftercare for the patients it treated, and for a standalone patient Hairline assigns to it.
5. **B04:** the admin oversees all aftercare, reassigns cases when a clinic withdraws or is suspended, and manages the templates the clinics use.
6. **B07 and B08:** check the messaging and support channels used throughout the journey.
7. **B06:** checks the invoices and refunds that the cancellations and rejections in the earlier batches produce.

## 5. Progress Summary

Update after each test session (the `manual-test-bug-sync` skill can refresh this).

| Batch | Total | Pass | Fail | Blocked | Not tested | Open bugs | Last tested |
|---|---|---|---|---|---|---|---|
| B01 | 19 | 0 | 0 | 0 | 19 | 0 | — |
| B02 | 19 | 0 | 0 | 0 | 19 | 0 | — |
| B05 | 12 | 0 | 0 | 0 | 12 | 0 | — |
| B03 | 13 | 0 | 0 | 0 | 13 | 0 | — |
| B04 | 14 | 0 | 0 | 0 | 14 | 0 | — |
| B07 | 17 | 0 | 0 | 0 | 17 | 0 | — |
| B08 | 17 | 0 | 0 | 0 | 17 | 0 | — |
| B06 | 17 | 0 | 0 | 0 | 17 | 0 | — |
| **Total** | **128** | **0** | **0** | **0** | **128** | **0** | **—** |
