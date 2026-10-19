# Phase 1 Manual Test Plan — Controlled Commercial Pilot

## Document Control

| Field | Value |
|---|---|
| Phase | Phase 1 (P0) — Controlled Commercial Pilot |
| Plan version | 1.0 |
| Status | Draft |
| Scope source | [Admin and Provider Implementation Status and Release Roadmap › Release Roadmap, Phase 1](../../../../../reports/2026-09-06/admin-provider-implementation-status-and-release-roadmap.md) |
| Release objective | Conditional target for onboarding selected providers and completing inquiry-to-quote work |
| Exit gate | One authoritative API per flow; no production fixtures; live RBAC, session revocation, provider isolation, pre-payment identity privacy, quote-state consistency, and scheduling rules pass |
| Created | 2026-10-19 |
| Last updated | 2026-10-19 |
| Plan owner | Hairline QA / product team |
| Tester(s) | |

## Change Log

| Version | Date | Change | By |
|---|---|---|---|
| 1.0 | 2026-10-19 | Initial plan | Hairline QA |
| 1.0 | 2026-10-19 | Review fixes before issue: scheduled status change cases added to B01 (A02-FR015-21 to A02-FR015-23); per-provider currency (GBP for {V1}, EUR for {V2}); {S1} set to Clinical Staff and new account {S2} for the custom-role cases; provider dashboard URL; exit criteria aligned with the template; run-order timing and team lead times | Hairline QA |

## 1. Scope

### 1.1 In Scope

| Module | Function slice in this phase | FRs | Batch |
|---|---|---|---|
| A-02 Provider Management | Provider list, creation wizard, activation email and password setup, resend and expiry, basic-info, language and document administration, admin staff invitation, immediate and scheduled suspend and deactivate, Cancel Scheduled Change, reactivate (including automatic cancellation of a pending change), Activity Log, admin permission checks | FR-015; FR-009 Screen 12, FR-020, FR-026, FR-031, FR-032 | B01 |
| PR-01 Auth & Team Management | Provider sign-in, sign-out and lockout; team dashboard; invite, accept, resend; role change; remove and suspend with session revocation; role permissions; provider isolation | FR-009; FR-026, FR-031 | B02 |
| PR-06 Profile & Settings (essential) | Provider profile (clinic details, images, languages, awards, documents), treatment pricing, package catalog (create, validate, version, clone, deactivate), status and permission effects, catalog isolation | FR-032, FR-024; FR-015, FR-031 | B03 |
| A-09 System Settings (essential) | Admin access control and roles, provider login and security settings, and inquiry and quote configuration needed for the pilot | FR-031, FR-026, FR-025 | B04 |
| PR-02 Inquiry & Quote Management | Provider inquiry list and detail, quote authoring and submission, inquiry and quote search, role permissions | FR-003, FR-004, FR-022, FR-031; FR-005 and FR-006 as prepared setup states only | B05 |
| A-01 Patient Management & Oversight (inquiry and quote) | Admin oversight of inquiries and quotes and admin role enforcement | FR-003, FR-004, FR-016, FR-031 | B06 |

### 1.2 Out of Scope

- **Patient mobile app.** It is not tested in this plan. Patient-side data (inquiries submitted, quotes accepted) is prepared by the team as setup data and referenced by placeholder (for example "An inquiry submitted by {P5} exists").
- **A-02, deferred parts.**
  - Commission and financial editing (A-02 profile Tab 7) and payouts: Phase 3 (A-05, A-06).
  - The booking and treatment parts of the suspension cascade, and admin reassignment of bookings: Phase 2 (A-01 booking and treatment).
  - Featured provider management and the 10-provider cap, provider closure requests and "Login as Provider": Phase 4 or post-MVP.
- **PR-01.** Multi-factor authentication (FR-009 future improvement) and task transfer beyond the reassignment option in the removal modal.
- **PR-06, deferred parts.**
  - Billing settings: Phase 3 (PR-05 earnings and payout).
  - Account settings and password change, notification preferences, Help Centre, support cases, closure requests, review responses (FR-013), localization and promotions: Phase 4 (remaining PR-06 settings and help).
- **PR-03, PR-04, PR-07, A-03, A-04, basic A-10 and minimum A-05:** Phase 2.
- **PR-05 earnings and payout, A-05, A-06, A-07:** Phase 3.
- **Advanced PR-05 analytics, A-08, the rest of A-09 and advanced A-10:** Phase 4.
- **Direct API testing.** API behaviour is checked through the dashboards only. API-level and automated checks belong to the development team.

## 2. Entry and Exit Criteria

**Entry criteria** (all must hold before testing starts):

- The Phase 1 build is deployed to the test environment, and its build or release identifier is recorded in §3.
- All placeholder accounts in §3 exist, are verified by the team, and their credentials have been shared privately with the tester.
- The team-controlled mailboxes listed in §3 are fresh, never used on Hairline, and readable by the tester.
- The patient-side setup data that B05 and B06 need (submitted inquiries, quote states) has been prepared and listed in those batch files.
- The dev team has confirmed that production fixtures and fallback data have been removed from the build under test.
- The team-prepared setup items listed in §4 (Scheduling and team lead times) are ready by their lead times.

**Exit criteria** (phase passes when):

- Every High-priority case is Pass.
- No open bug (Bug status Found, Logged, Fixed - retest, or Reopened) on a High-priority case.
- Roadmap exit gate items for this phase, each verified:
  - **One authoritative API per flow.** The dev team confirms each tested flow (onboarding, team access, profile and catalog, configuration, inquiry and quote) calls one canonical API with no legacy fallback. The tester confirms that admin and provider views of the same record agree (for example provider status in B01, team membership in B02, quote state in B05 and B06).
  - **No production fixtures.** No tested screen shows demo, placeholder or fallback records. For example, the team and invitation lists in B02 show only real invitations.
  - **Live RBAC.** Permission cases pass: A02-FR015-20, PR01-FR009-12, PR01-FR009-17, PR06-FR024-17, and the role-permission cases in B04, B05 and B06. Changes take effect on the next page load without signing in again.
  - **Session revocation.** Removing, suspending or deactivating a user or provider ends active sessions at once and blocks sign-in: PR01-FR009-14, PR01-FR009-16 and A02-FR015-18 pass.
  - **Provider isolation.** No provider can see another provider's team, catalog, inquiries or quotes: PR01-FR009-07, PR01-FR009-18, PR06-FR024-18 and the isolation cases in B05 pass.
  - **Pre-payment identity privacy.** Patient identity stays masked to providers until payment, as checked by the identity-privacy cases in B05 and B06.
  - **Quote-state consistency.** Quote status is the same across provider and admin views and follows the allowed transitions, as checked by the quote-state cases in B05 and B06.
  - **Scheduling rules.** Quote date and scheduling rules are enforced, as checked by the scheduling cases in B05.

## 3. Test Environment and Accounts

| Item | Value |
|---|---|
| Provider dashboard URL | https://admin.hairline.app (shared origin with the admin dashboard; sign in with a provider account) |
| Admin dashboard URL | https://admin.hairline.app |
| Backend API base URL | https://backend.hairline.app/api |
| Build / release under test | {Record build or release identifier at test start} |
| Browser(s) | Chrome latest, desktop; a second browser or private window for two-session cases |
| Currency | Set per provider and read-only for providers: {V1} prices, packages and quotes are in GBP; {V2} prices and quotes are in EUR. The team confirms this setup before testing. The FR-024, FR-004 and FR-026 PRDs still describe one system quote currency; cases that read the currency record what is shown |
| Plan owner contact | {Plan owner contact} (the team supplies it before testing; send every mid-test request for team action, and every question, to this contact) |

Accounts used (placeholders; credentials sent privately):

| Placeholder | Role | Used in batches |
|---|---|---|
| {A1} | Super Admin | B01, B02 (Seat Limit change and restore in PR01-FR009-20), B03 (suspend and reactivate {V4} in PR06-FR032-16; admin read-only package check), B04, B05, B06 |
| {A2} | Admin with the Support Staff system role (FR-031 default: View Providers only; no Edit, Onboard or Suspend Providers). To be created by the team | B01 |
| {S1} | {V1} staff with the system role Clinical Staff as its base and end state of every phase; any custom-role test must restore it or use a different account. Phase 1 does not change its role (B02 PR01-FR009-16 suspends and reactivates it within the case). Setup item CS-ROLE (B02): the team confirms the Clinical Staff role has View Team Members, Invite Team Members, View Inquiries, Respond to Inquiries, Edit Profile and Manage Treatments not ticked, because FR-031 gives per-role permissions only as an example. End of Phase 1: Active, Clinical Staff | B01, B02, B03 |
| {S2} | {V1} team member with the custom provider role "clinician-front-desk" (FR-009 Rule 8). To be created by the team. The team records the role's base type, which must allow quote creation (FR-031 Custom Provider Role Protection), and confirms its permissions: View Inquiries and Respond to Inquiries ticked; View Team Members, Invite Team Members, Edit Profile and Manage Treatments not ticked. B04 A09-FR031-10 and B05 PR02-FR031-01 untick Respond to Inquiries and tick it again within the case. End of Phase 1: Active, custom role with Respond to Inquiries ticked | B04, B05 |
| {V1} | Provider owner, primary pilot provider | B01, B02, B03, B04, B05, B06 |
| {V2} | Provider owner, second provider for duplicate-email and isolation checks | B01, B02, B03, B05, B06 |
| {V3} | Provider owner; login-lockout case in B02; the provider located in Germany in B05 and B06 | B02, B05, B06 |
| {V4} | Provider owner reserved for status changes. B01 (including the scheduled-change cases A02-FR015-21 to A02-FR015-23) and B03 suspend and reactivate it and leave it Active. The team suspends it before B06 (setup item; A01-FR003-03 relies on it). End of Phase 1: Suspended. The Phase 2 handoff reactivates it | B01, B03, B04, B06 |
| {P1}–{P7} | Patients, referenced only as owners of prepared inquiry and quote setup data | B04 ({P7}), B05, B06 |
| {P8} | Patient with no other inquiry; owner of setup inquiry INQ-8 (destination USA, no eligible provider). To be created by the team | B06 |
| {Admin invite mailbox} | Team-controlled fresh mailbox, never used on Hairline, that receives the admin invitation. To be created by the team | B04 |
| {New provider mailbox 1} | Team-controlled fresh mailbox; login email of QA Pilot Clinic 01, created in B01 | B01 |
| {New provider mailbox 2} | Team-controlled fresh mailbox with plus-addressing; contact email of QA Pilot Clinic 01, and with "+clinic02" the contact email of QA Pilot Clinic 02 | B01, B03 |
| {New provider mailbox 3} | Team-controlled fresh mailbox; login email of QA Pilot Clinic 02, created in B01 | B01 |
| {Invite mailbox 1} | Team-controlled fresh mailbox; admin staff invitation for QA Pilot Clinic 01 (A02-FR015-15, A02-FR015-18) | B01 |
| {Invite mailbox 2} | Team-controlled fresh mailbox; the {V1} invitee QA InviteeOne | B02 |
| {Invite mailbox 3} | Team-controlled fresh mailbox with plus-addressing (+val, +rl01 to +rl11) for validation and rate-limit invitations | B02 |
| {Invite mailbox 4} | Team-controlled mailbox that receives setup invitation INV-EXP-1 (expired {V1} invitation). To be created by the team | B02 |

## 4. Batches and Run Order

| Order | Batch | File | Module | FRs | Cases | Depends on |
|---|---|---|---|---|---|---|
| 1 | B01 | [B01-a02-provider-onboarding](batches/B01-a02-provider-onboarding.md) | A-02 | FR-015; FR-009, FR-020, FR-026, FR-031, FR-032 | 23 | — |
| 2 | B02 | [B02-pr01-team-access](batches/B02-pr01-team-access.md) | PR-01 | FR-009; FR-026, FR-031 | 20 | B01 |
| 3 | B03 | [B03-pr06-profile-pricing-packages](batches/B03-pr06-profile-pricing-packages.md) | PR-06 | FR-032, FR-024; FR-015, FR-031 | 18 | B01, B02 |
| 4 | B04 | [B04-a09-access-inquiry-config](batches/B04-a09-access-inquiry-config.md) | A-09 | FR-031, FR-026, FR-025 | 19 | B01–B03 |
| 5 | B05 | [B05-pr02-inquiry-quote](batches/B05-pr02-inquiry-quote.md) | PR-02 | FR-003, FR-004, FR-022, FR-031 | 19 | B01–B04 |
| 6 | B06 | [B06-a01-inquiry-quote-oversight](batches/B06-a01-inquiry-quote-oversight.md) | A-01 | FR-003, FR-004, FR-016, FR-031 | 18 | B04, B05 |

**Scheduling and team lead times:**

- **B01 runs over two days.** A02-FR015-11 starts at least 25 hours after A02-FR015-10 ends. A02-FR015-22 schedules a suspension on Day 1 and is checked on Day 2 after 08:00 Asia/Saigon time (the scheduled-change job runs at 00:00 UTC); A02-FR015-23 follows on Day 2.
- **B05 and B06 run on consecutive days.** B06 must start within 48 hours of the send time recorded in B05 PR02-FR004-01, because A01-FR004-04 and A01-FR004-06 need the INQ-1 quotes still Sent.
- **Team-prepared setup, with lead times** (request each item from the team by the time shown):
  - At least 2 working days before B01: the accounts in §3 ({A2}, {S1} with setup item CS-ROLE, {S2} with its custom role, {P8}), the fresh mailboxes, the per-provider currency setup, and the B01 setup items (DOC-V1; GBP enabled).
  - At least 9 days before B02: INV-EXP-1, because the invitation must be sent at least 8 days before testing.
  - At least 1 working day before B03: TRT-V1.
  - At least 1 working day before B05: the B05 setup sheet (INQ-1 to INQ-7, PKG-1 to PKG-6 and the prepared quote states).
  - Between the end of B05 and the start of B06 (same or next day, inside the 48-hour window): QT-V2-1, INQ-8, {V4} suspended through A-02, and the record of the option {P5} accepted.
  - On call during B01 Day 2: check, and if needed trigger, the daily scheduled-change job for A02-FR015-22.

**End-to-end journey:** The pilot starts with a Hairline admin onboarding a clinic (B01): the provider is created, its owner activates the account and logs in, and the admin can suspend, reactivate or deactivate it, at once or on a scheduled date. The clinic owner then builds a team and controls what each person can do, and the checks confirm that permissions, session revocation and isolation from other clinics hold (B02). Next, the provider completes the public profile, prices its treatments and builds add-on packages to use in quotes (B03). The admin side then confirms the access roles, security settings and inquiry and quote configuration that govern the pilot (B04). With that in place, the provider receives patient inquiries (prepared as setup data), and its permitted team members prepare and send quotes while patient identity stays private before payment (B05). Finally, the admin oversees the same inquiries and quotes and confirms the states match what the provider sees (B06). Run the batches in order, because each one leaves the data the next one uses.

## 5. Progress Summary

Update after each test session (the `manual-test-bug-sync` skill can refresh this).

| Batch | Total | Pass | Fail | Blocked | Not tested | Open bugs | Last tested |
|---|---|---|---|---|---|---|---|
| B01 | 23 | 0 | 0 | 0 | 23 | 0 | — |
| B02 | 20 | 0 | 0 | 0 | 20 | 0 | — |
| B03 | 18 | 0 | 0 | 0 | 18 | 0 | — |
| B04 | 19 | 0 | 0 | 0 | 19 | 0 | — |
| B05 | 19 | 0 | 0 | 0 | 19 | 0 | — |
| B06 | 18 | 0 | 0 | 0 | 18 | 0 | — |
| **Total** | **117** | **0** | **0** | **0** | **117** | **0** | **—** |
