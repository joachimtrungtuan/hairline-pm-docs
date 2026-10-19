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
| 1.0 | 2026-10-19 | Review fixes: Phase handoff and Phase 3 end state; B07 uses team-created {P9}–{P11}; B08 adds FR-012 admin oversight cases A10-FR012-01 to A10-FR012-07; template exit criteria | QA lead |
| 1.0 | 2026-10-19 | Closing fixes: system default currency GBP for all quotes, invoices and refunds (FR-029), payout currency per provider; team-created patients {P12}–{P28} so no patient holds two active inquiries or bookings (FR-003); new cases PR03-FR010-20, PR03-FR010-21, PR04-FR011-14 and A04-FR008-13; PR03-FR010-05 retired; Team Setup Checklist; plan owner contact | QA lead |
| 1.0 | 2026-10-19 | Before first issue: system Default Currency set to USD (FR-029 seed); {V1} payout currency USD | Product / QA lead |
| 1.0 | 2026-10-19 | Before first issue: existing test accounts reused and remaining accounts and mailboxes created by the tester during the pass; seeded data may stay; evidence links from any file-sharing service | Product / QA lead |

## 1. Scope

### 1.1 In Scope

| Module | Function slice in this phase | FRs | Batch |
|---|---|---|---|
| PR-03 | Treatment execution in the provider dashboard: Check In gates, day documentation, End Treatment, change of treatment details, provider case closure, documentation reminders | FR-010 | B01 |
| A-01 | Admin booking intervention (Bookings Management Dashboard, Change Appointment, Cancel Booking, Revive Booking, provider-fault transfer and resolution), admin treatment oversight, Booking Support Requests and provider-impact support resolution | FR-006, FR-010, FR-016 | B02 |
| PR-04 | Provider aftercare: setup wizard, paperwork-only option, standalone activation, case list, details, plan edit, progress tracking, escalation, clinician assignment (observation) | FR-011 | B03 |
| A-03 | Admin aftercare oversight: all-provider case list and details, plan edit, reassignment to a clinic or the Hairline aftercare team, suspension effects, standalone requests, milestone templates | FR-011 | B04 |
| A-04 | Travel section inside the admin confirmed booking detail: status, re-notify, corrections, travel-date review, early-departure warning, closed context, carry-over after a provider-fault transfer | FR-008 | B05 |
| A-05 | Minimum invoice and refund controls | FR-017; FR-006, FR-007, FR-020 as dependencies | B06 |
| PR-07 | Provider messaging with real transport, quote eligibility and durable notifications; call functionality proven or excluded | FR-012; FR-003, FR-004, FR-020 as dependencies | B07 |
| A-10 | Admin support case management and admin message oversight (FR-012 Communication Monitoring Center, flags and emergency intervention) | FR-034, FR-012; FR-015, FR-016, FR-020, FR-031 as dependencies | B08 |

### 1.2 Out of Scope

- PR-05 provider earnings, A-05 reconciliation and payouts beyond the minimum invoice and refund controls, A-06 promotions and A-07 affiliates (Phase 3).
- A-08 analytics, the remaining A-09 configuration and advanced A-10 functions (Phase 4).
- FR-011 Screen 17 Provider Performance Dashboard and Screen 18 Aftercare Progress Tracking (Admin View), which are in the backlog.
- The FR-008 provider-side travel screens. Provider travel data is used only as prepared setup data.
- Process Refund on bookings, which is tested in B06.
- The patient mobile app. Any patient action needed for a case is existing setup data prepared by the team.

## 2. Entry and Exit Criteria

**Phase handoff** (the team completes steps 1 to 4 on the shared test environment after Phase 1 ends and before the entry criteria are checked; the tester completes step 5 at the start of the pass; Phase 1 data stays in place):

1. Reactivate `{V4}`. Phase 1 leaves it Suspended. The team suspends it again before B02 starts (section 3).
2. End every Phase 1 inquiry that is still open, because FR-003 allows one active inquiry per patient and the Phase 2 setups create new inquiries and bookings for `{P1}`–`{P8}`. Phase 1 setup items INQ-1 to INQ-8 belong to `{P1}`–`{P8}`. The team cancels each one still active as its patient (FR-003), and cancels the accepted INQ-5 quote of `{P5}` through the admin booking cancellation (FR-006) if it is still open. The team records the final status of INQ-1 to INQ-8 for the plan owner. Phase 2 names its own inquiries with the prefix P2- (for example P2-INQ-1) so they are not confused with Phase 1 items.
3. Confirm `{S1}` is Active with the system role Clinical Staff in `{V1}`'s team (Phase 1 base and end state). Phase 2 does not use `{S2}` (Phase 1 custom role "clinician-front-desk").
4. Confirm the quote and payment settings Phase 1 changed are back to their defaults, and that FR-029 Default Currency is USD with EUR enabled. Every quote, package and treatment price, invoice, patient payment and refund in Phase 2 is in USD for every provider. Confirm `{V1}`'s payout currency is USD and `{V2}`'s is EUR; EUR appears only in payout, earnings and statement screens.
5. The tester creates the patients `{P9}`–`{P28}` (section 3; Team Setup Checklist item 6) by registering them in the patient app, each with no inquiry, quote, booking or conversation, and shares their logins privately with the plan owner so the team can prepare the setup data. FR-003 allows one active inquiry per patient, and an inquiry stays active until it is Cancelled or Completed, including after it becomes a booking. The setups therefore give each patient at most one active inquiry or booking at a time: a second booking for `{P4}` (INV-10) or `{P5}` (INV-5) is created only after B02 cancels that patient's first booking, `{P9}`'s second inquiry (B07 P2-INQ-2) is submitted only after the first is cancelled, and every other setup that would add a second active record uses its own patient from `{P12}`–`{P28}`. Standalone aftercare requests and support cases are not FR-003 inquiries.

**End state for Phase 3:** `{V3}` Active (reactivated after B06); `{V4}` Suspended (suspended before B02; the Phase 3 handoff reactivates it if needed); `{S1}` Active, Clinical Staff; FR-029 Default Currency USD, `{V1}` payout currency USD and `{V2}` payout currency EUR unchanged. The B01 to B08 bookings, aftercare cases, conversations, support cases, invoices and refunds stay in place.

**Entry criteria** (all must hold before testing starts):

- Phase 1 exit gate passed and the Phase handoff steps above are done.
- Build deployed to the test environment, with the version recorded in section 3.
- The existing test accounts {A1}, {S1}, {V1}–{V4} and {P1}–{P7} are verified and their credentials shared privately, and {S1} has the Clinical Staff role in {V1}'s team. {P8} was created in Phase 1. The tester creates the remaining accounts ({A3}, {A4}, {A6}, {A7} and {P9}–{P28}) during the pass (Team Setup Checklist item 6).
- The setup data in each batch's Test Data Sets and Shared Preconditions is in place, including:
  - The bookings for {P1}–{P8} and {P12}–{P28} in the stated statuses and payment states, and, for B07, the patients {P9}–{P11} the tester created.
  - At least one active aftercare milestone template and an Aftercare questionnaire set.
  - The travel records for B05.
  - The {V4} aftercare cases, created before {V4} is suspended.

**Exit criteria** (phase passes when):

- Every High-priority case is Pass.
- No open bug (Bug status Found, Logged, Fixed - retest, or Reopened) on a High-priority case.
- Roadmap exit gate conditions verified, each listed below:
- Billing uses current invoice routes: the B06 invoice and refund cases pass.
- Treatment invariants pass (B01, B02):
  - Check In is blocked before the procedure date, while a balance is outstanding, and for Billing Staff.
  - A patient has at most one In Progress treatment. FR-003's one-active-inquiry rule prevents the second booking this check needs, so its case PR03-FR010-05 is retired and the rule is on the PO list.
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
- Messaging uses real transport with quote eligibility and durable notifications (B07), and admins can monitor, flag and intervene in conversations (B08, A10-FR012 cases).
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
| Plan owner contact | Trung Dang (trung.dang@vantaymedia.com) |

Accounts used (placeholders; credentials of the existing accounts are sent privately; the tester creates the other accounts during the pass and shares their logins privately with the plan owner, never in a batch file):

| Placeholder | Role | Used in batches |
|---|---|---|
| {A1} | Super admin | B01 (checks), B02, B03 (check), B04, B05, B06, B07, B08 |
| {A3} | Admin with the Billing Viewer role; created by the tester before B06 by admin invite from {A1} | B06 |
| {A4} | Restricted admin 1 (Support Center access without the "View Internal Notes" permission); created by the tester before B08 by admin invite from {A1} | B08 |
| {A6} | Restricted admin 2 (no Support Center access); created by the tester before B08 by admin invite from {A1} | B08 |
| {A7} | Second admin with the Support Staff role; created by the tester before B08 by admin invite from {A1}. Kept because B08 A10-FR034-12 reassigns a support case from {A1} to another admin, which needs a second admin who can own support cases | B08 |
| {S1} | Provider staff with the system role Clinical Staff in {V1}'s team (base and end state; Phase 2 does not change its role) | B01 |
| {V1} | Provider (clinic Owner); main treating clinic; payout currency USD | B01, B02 (checks), B03, B04, B05 (check), B06, B07, B08 |
| {V2} | Provider; second clinic used for isolation, replacement and reassignment; payout currency EUR | B01, B02, B03, B04, B05, B06, B07, B08 |
| {V3} | Provider; suspended once before B02 starts, during a live treatment (setup data for B02 AD-2 and B06 INV-11); reactivated after B06 | B02, B04 (check), B06 |
| {V4} | Provider; reactivated in the Phase handoff (section 2), then suspended before B02 starts, with live aftercare cases and an open inquiry (setup data, B02 AD-8); stays Suspended at the end of Phase 2 | B02, B04 |
| {P1}–{P7} | Patients; booking, aftercare and travel records are setup data only (no patient sign-in) | B01–B06; B08 ({P1}–{P5}) |
| {P8} | Patient created by the tester in Phase 1 (owner of Phase 1 INQ-8); one Confirmed booking (B01 setup item TX-8, also B07 setup item BKG-1), setup data only | B01, B07, B08 |
| {P9}–{P11} | Patients created by the tester for B07, with no earlier inquiry, quote, booking or conversation with {V1}; setup data only (no patient sign-in). B08 reads their conversations | B07, B08 |
| {P12} | Patient created by the tester for Phase 2 with no other inquiry or booking; holds B02 AD-1 ({V2}); setup data only | B02, B03 |
| {P13}, {P14} | Patients created by the tester for Phase 2; {P13} holds B02 AD-3 ({V1}, Payment Window Expired), {P14} holds B02 AD-8 ({V4} inquiry); setup data only | B02 |
| {P15} | Patient created by the tester for Phase 2; holds B03 AC-4 ({V1} aftercare case); setup data only | B03, B04 |
| {P16} | Patient created by the tester for Phase 2; holds B04 AT-2 ({V4} treatment-linked aftercare); setup data only | B04 |
| {P17}–{P19} | Patients created by the tester for Phase 2; hold B05 TR-2, TR-3 and TR-4 ({V2} bookings); setup data only | B05 |
| {P20}–{P28} | Patients created by the tester for Phase 2; hold B06 INV-1 to INV-4, INV-6 to INV-9 and INV-11 in that order; setup data only | B06 |

Accounts for B06–B08 are also described in those batch files.

**{V3} suspension:** the team suspends {V3} once, before B02 starts. Before suspending, the team puts B02 setup item AD-2 ({P7} with {V3}) In Progress and starts the {P28} payment with {V3} that B06 setup item INV-11 needs. {V3} stays suspended through B06, which runs last, and the team reactivates it after B06 ends. No batch from B02 onward needs {V3} active: B04 expects it suspended (A03-FR011-05), and B03, B05, B07 and B08 do not use {V3}.

## Team Setup Checklist

The team completes each item by its lead time and ticks Done; item 6 is the tester's. Item details are in the section or batch named; this table does not repeat them.

| # | Item | Batches | Owner | Lead time | Done |
|---|---|---|---|---|---|
| 1 | Deploy the build to the test environment and record its version in section 3 | All | Dev team | Before phase start | [ ] |
| 2 | Phase handoff step 1: reactivate {V4} (section 2) | B02, B04 | Dev team | Before phase start | [ ] |
| 3 | Phase handoff step 2: end the Phase 1 inquiries INQ-1 to INQ-8 still open and report their final status (section 2) | All | Dev team | Before phase start | [ ] |
| 4 | Phase handoff step 3: confirm {S1} is Active with Clinical Staff in {V1}'s team (section 2) | B01 | QA lead | Before phase start | [ ] |
| 5 | Phase handoff step 4: quote and payment settings at their defaults; FR-029 Default Currency USD with EUR enabled; {V1} payout currency USD, {V2} payout currency EUR (section 2) | All | Dev team | Before phase start | [ ] |
| 6 | Tester creates the accounts this phase needs through the normal product flows, each with a fresh mailbox the tester controls, and shares each login privately with the plan owner: patients {P9}–{P28} by registering in the patient app (setup data only; Phase handoff step 5); admins {A3} (Billing Viewer) and {A4}, {A6}, {A7} (roles in section 3) by admin invite from {A1} | B02–B08 | Tester | {P9}–{P28}: start of the pass, before the team setup items that use them; {A3}: before B06; {A4}, {A6}, {A7}: before B08 | [ ] |
| 7 | Send credentials privately, with the names, Patient IDs, booking references and case references each batch's Shared Preconditions lists | All | QA lead | Before each batch starts | [ ] |
| 8 | Supply the test upload files and long-text files named in each batch's data sets | B01–B05, B07, B08 | QA lead | Before each batch starts | [ ] |
| 9 | B01 setup: {V1} has Clinician 1 and Clinician 2; TX-1 to TX-4 and TX-6 to TX-8 in their stated states (TX-5 not used) | B01 | Dev team | Before the B01 run day starts | [ ] |
| 10 | B01 setup item RM-1: reminder settings at defaults; reminder job run at 12 and 24 hours after TX-4's check-in; give the check-in time | B01 | Dev team | At least 24 hours after TX-4's check-in, before B02 case A01-FR006-05 | [ ] |
| 11 | B04 setup items AT-1 and AT-2 ({V4} aftercare cases) | B04 | Dev team | Before {V4} is suspended (before B02) | [ ] |
| 12 | {V3} suspension sequence: AD-2 In Progress, INV-11 deposit started with the webhook held, suspend {V3}, release the webhook (section 3) | B02, B04, B06 | Dev team | Before B02 starts | [ ] |
| 13 | {V4} suspension: AD-8 quoted, then suspend {V4} | B02, B04 | Dev team | Before B02 starts, after item 11 | [ ] |
| 14 | B05 setup items TR-1 to TR-5 (travel records) | B02, B05 | Dev team | Before B02 starts | [ ] |
| 15 | B02 setup items AD-1 to AD-9 | B02 | Dev team | After B01 ends, before B02 starts | [ ] |
| 16 | Pay {P3}'s replacement booking as {P3} (B05 setup item TR-6) | B05 | Dev team | After B02 case A01-FR006-08, before B05 starts | [ ] |
| 17 | B03 setup items AC-1 to AC-5 | B03, B04 | Dev team | Before B03 starts | [ ] |
| 18 | B04 setup items AT-3 and AT-4 (AT-4 submitted the day before the B04 run day) | B04 | Dev team | Before B04 starts | [ ] |
| 19 | B07 setup: P2-INQ-1, P2-INQ-3, BKG-1 conversation on {P8}'s TX-8, CONV-4; keyword-flag list holds "WhatsApp"; message transport and FR-020 notifications live | B07, B08 | Dev team | Before B07 starts | [ ] |
| 20 | B07 run support: a team member acts as {P9} and {A1} on request, including cancelling P2-INQ-1 and submitting P2-INQ-2 between PR07-FR012-01 and PR07-FR012-02 | B07 | Dev team | During the B07 run, same day | [ ] |
| 21 | B08 setup: support cases SUP-1 to SUP-6; PRD default category and priority lists | B08 | Dev team | Before B08 starts, cases created within the 30 days before the run day | [ ] |
| 22 | B06 setup: Stripe test mode with payment and refund webhooks; invoices INV-1 to INV-10 through real paid bookings | B06 | Dev team | Before B06 starts; INV-4, INV-6 and INV-9 lead times as stated in B06; INV-5 after B02 case A01-FR016-04; INV-10 after B02 case A01-FR006-05 | [ ] |
| 23 | Reactivate {V3} (section 3) | B06 | Dev team | After B06 ends | [ ] |

## 4. Batches and Run Order

| Order | Batch | File | Module | FRs | Cases | Depends on |
|---|---|---|---|---|---|---|
| 1 | B01 | [B01-pr03-treatment-execution](batches/B01-pr03-treatment-execution.md) | PR-03 | FR-010 | 20 | — |
| 2 | B02 | [B02-a01-booking-treatment-intervention](batches/B02-a01-booking-treatment-intervention.md) | A-01 | FR-006, FR-010, FR-016 | 19 | B01 |
| 3 | B05 | [B05-a04-travel](batches/B05-a04-travel.md) | A-04 | FR-008 | 13 | B02 |
| 4 | B03 | [B03-pr04-aftercare](batches/B03-pr04-aftercare.md) | PR-04 | FR-011 | 14 | B01, B02 |
| 5 | B04 | [B04-a03-aftercare-team](batches/B04-a03-aftercare-team.md) | A-03 | FR-011 | 14 | B01, B02, B03 |
| 6 | B07 | [B07-pr07-messaging](batches/B07-pr07-messaging.md) | PR-07 | FR-012; FR-003, FR-004, FR-020 | 17 | — |
| 7 | B08 | [B08-a10-support](batches/B08-a10-support.md) | A-10 | FR-034, FR-012; FR-015, FR-016, FR-020, FR-031 | 24 | B07 |
| 8 | B06 | [B06-a05-invoice-refund-controls](batches/B06-a05-invoice-refund-controls.md) | A-05 | FR-017; FR-006, FR-007, FR-020 | 17 | B02 |

**End-to-end journey:** The batches follow a paid patient from the procedure day to recovery.

1. **B01:** a clinic checks the patient in, documents each treatment day and ends the treatment. The case moves to Aftercare.
2. **B02:** a Hairline admin oversees the same treatments. The admin handles the clinic's postponement and closure requests, reschedules, cancels, revives or transfers bookings, and resolves patient support requests.
3. **B05:** the appointment change and the provider-fault transfer from B02 are followed through to the travel records, where the admin confirms or corrects flights, hotel and passport.
4. **B03:** the clinic sets up and runs aftercare for the patients it treated, and for a standalone patient Hairline assigns to it.
5. **B04:** the admin oversees all aftercare, reassigns cases when a clinic withdraws or is suspended, and manages the templates the clinics use.
6. **B07 and B08:** check provider messaging, admin support cases and admin oversight of patient-provider conversations.
7. **B06:** builds its own invoice setups (INV-1 to INV-11) and checks the invoice and refund controls on them.

## 5. Progress Summary

Update after each test session (the `manual-test-bug-sync` skill can refresh this).

| Batch | Total | Pass | Fail | Blocked | Not tested | Open bugs | Last tested |
|---|---|---|---|---|---|---|---|
| B01 | 20 | 0 | 0 | 0 | 20 | 0 | — |
| B02 | 19 | 0 | 0 | 0 | 19 | 0 | — |
| B05 | 13 | 0 | 0 | 0 | 13 | 0 | — |
| B03 | 14 | 0 | 0 | 0 | 14 | 0 | — |
| B04 | 14 | 0 | 0 | 0 | 14 | 0 | — |
| B07 | 17 | 0 | 0 | 0 | 17 | 0 | — |
| B08 | 24 | 0 | 0 | 0 | 24 | 0 | — |
| B06 | 17 | 0 | 0 | 0 | 17 | 0 | — |
| **Total** | **138** | **0** | **0** | **0** | **138** | **0** | **—** |
