# Sprint 1 Readiness & Fix Backlog

---

## Document Control & Sprint Summary

| Field | Value |
|---|---|
| Sprint | Sprint 1 |
| Theme | Core: Inquiry, Quote & Treatment |
| Dates | May 19 (Tue) - May 29 (Fri), 2026; kickoff ceremony May 20 (Wed) |
| Working days | 9 |
| Goal | Complete and verify the core clinical journey from patient registration through inquiry, quoting, booking, and treatment execution across all three tenants simultaneously. Aftercare modules move to Sprint 2 where they are grouped with the configuration and template setup they depend on. |
| Definition of Done | All Sprint 1 modules pass QA on staging; no open critical P0/P1 bugs on any Sprint 1 module; the core commercial journey from registration through inquiry, quote acceptance, booking, and deposit is testable end-to-end on staging; treatment execution is verified against a fully-paid staging booking fixture in Sprint 1 while the patient final-balance path that unlocks real check-in is completed in Sprint 2; Apple Developer Program and Google Play Console accounts are created and verified. |
| Source launch plan | `local-docs/product-plans/2026-05-13/launch-plan.md` |
| Prepared by | Codex AI agent |
| Prepared date | 2026-05-29 |
| Product review date(s) | Not performed in this pass; this report prepares the Sprint 1 scope and readiness backlog from the launch plan. |
| Product environment(s) checked | No staging, production, local build, or app build was checked in this pass. |
| Review scope boundary | Source review only. Scope, DoD, modules, stories, deferrals, and readiness gaps are derived from the Sprint 1 section of the launch plan. Product defects must be added after real staging/product review with evidence links. |

<!--
AI agent guidance: Keep this guidance hidden from Markdown preview. It exists only to preserve the intended workflow for future agents editing this report.

## How To Use This Template

- Section 1 mirrors the launch plan. Do not add new scope, reinterpret the sprint, or silently move work between sprints.
- Section 2 is the working fix backlog. Capture issues found from real product review in enough detail that the dev team can reproduce and fix them quickly. Rows marked as evidence gaps are not confirmed product bugs; they are required product-review checks that must be backed by staging evidence before Sprint 1 can be treated as complete.
- Section 3 is for findings that should not distract the current sprint. Use it to prevent out-of-scope issues from being treated as sprint commitments.
- Do not include Plane ticket IDs, assignees, estimates, or ownership fields. Those belong to the later Plane-ticket creation workflow.

### Priority Scale

| Priority | Meaning |
|---|---|
| P0 | Blocks sprint completion, staging validation, or a core end-to-end journey. |
| P1 | Major required feature gap or broken required flow for this sprint. |
| P2 | Required but contained issue that does not block the whole sprint. |
| P3 | Minor UX, copy, polish, or cleanup issue that should not block sprint completion. |

-->

# 1. Sprint Scope From Launch Plan

## 1.1 Modules In Scope

| Surface | Module | FR / Scope Notes | Launch Plan Reference |
|---|---|---|---|
| Patient Mobile | P-01 Auth & Profile Management | FR-001 Patient Authentication; FR-026 App Settings & Security consumer behavior only. Policy/reason lists are managed in A-09a. | Sprint 1 Modules |
| Patient Mobile | P-02 Quote Request & Management | FR-003 Inquiry Submission; FR-004 Quote Submission; FR-005 Quote Comparison & Acceptance; FR-022 quote comparison filter P1. | Sprint 1 Modules |
| Patient Mobile | P-03a Booking & Payment | FR-006 Booking & Scheduling; FR-007 core deposit/base-currency portion only. Payment sub-features move to Sprint 2. | Sprint 1 Modules |
| Patient Mobile | P-07 Head-Scan Photo Capture & Viewing | FR-002 V1 standardized 2D photo-set capture/viewing; true 3D deferred. | Sprint 1 Modules |
| Provider Web | PR-01 Auth & Team Management | FR-009 Provider Team Roles. | Sprint 1 Modules |
| Provider Web | PR-02 Inquiry, Quote & Booking Management | FR-003 provider-side inquiry handling; FR-004 provider-side quote submission; FR-006 provider-side booking management; includes PR-02b quote withdrawal and confirmed-booking list/detail. | Sprint 1 Modules |
| Provider Web | PR-03 Treatment Execution & Documentation | FR-010 Treatment Execution. | Sprint 1 Modules |
| Provider Web | PR-06 Profile & Settings Management | FR-032 Provider Dashboard Settings; FR-024 Treatment Package Management provider tier. | Sprint 1 Modules |
| Admin Web | A-01 Patient Management & Booking Oversight | FR-016 Admin Patient Management; admin oversight for FR-003, FR-004, FR-005, and FR-006. | Sprint 1 Modules |
| Admin Web | A-02 Provider Management & Onboarding | FR-015 Provider Management. | Sprint 1 Modules |
| Admin Web | A-09a Content & Treatment Management | FR-024 admin treatment/package catalog; FR-025 questionnaire publication; FR-026 configuration owner; FR-027 legal content management. | Sprint 1 Modules |
| Shared Service | S-01 Head Scan Media Processing Service | FR-002 media intake, validation, and alert classification. | Sprint 1 Modules |
| Shared Service | S-02 Payment Processing Service | FR-007 core deposit infrastructure. | Sprint 1 Modules |
| Shared Service | S-05 Media Storage Service | FR-002 encrypted media storage layer; FR-023 retention alignment later in launch. | Sprint 1 Modules |

## 1.2 User Stories In Scope

### Patient

- As a new patient, I want to register with email OTP verification and build my health and preference profile, so clinics can match me with suitable treatments.
- As a patient, I want to browse treatments, complete inquiry details, upload a standardized head-scan photo set, and select preferred providers from the available list before final inquiry submission.
- As a patient, I want to cancel an inquiry and have related open quotes and held slots released.
- As a patient, I want to receive and compare quotes sorted by price, graft count, rating, or date.
- As a patient, I want to accept a quote with its provider-pre-scheduled treatment date, pay a base-currency deposit, and keep the slot only while the payment window is valid.
- As a patient, I want refund eligibility explained before payment without expecting a Sprint 1 refund-management UI.
- As a patient, I want to see treatment status and day-by-day clinical updates after provider check-in.

### Provider

- As a provider team member, I want secure login with role-based permissions and task reassignment when a colleague is suspended.
- As a provider, I want to receive anonymized pre-payment inquiries, review questionnaire/head-scan data, and submit a tailored quote with a pre-scheduled slot.
- As a provider, I want to withdraw a submitted quote with a reason logged.
- As a provider, I want to document treatment day-by-day with status, notes, prescription, actual graft count, and final head scan.
- As a provider, I want to manage clinic profile, languages, staff, awards, reviews display, documents, account settings, notification preferences, billing settings, and package catalog.

### Admin

- As an admin, I want a patient management dashboard with all eight tabs connected to live data.
- As an admin, I want to see stuck inquiries, delayed quotes, zero-quote cases, quote acceptance context, and booking exceptions so I can intervene where the core journey is blocked.
- As an admin, I want to onboard providers through a guided wizard and suspend/deactivate providers with audit logging.
- As an admin, I want to manage inquiry/aftercare/multi-context questionnaire sets with version history and MVP Yes/No constraint enforcement where required.
- As an admin, I want to draft, preview, and publish legal documents with version history and acceptance coverage.
- As an admin, I want to configure OTP behavior, country/calling-code lists, cancellation/deletion reason lists, and OTP email template content.

### Shared Services / Platform Foundations

- As any platform user, I want secure, fast, persistent login across devices.
- As a patient or provider, I want inquiry received, quote ready, and booking confirmed events recorded and visible in the relevant surfaces during Sprint 1, with full push/email/in-app delivery verified later in Sprint 3 under S-03.
- As the platform, I need head-scan media ingested, validated, classified for medical alerts, and stored encrypted with signed-URL access.
- As the platform, I need deposit charges to flow through Stripe with audit logging and refund eligibility computed from shared policy logic.

### Affiliate / Partner

- No affiliate or partner module is assigned to Sprint 1.

## 1.3 Explicitly Deferred / Out Of Scope

| Item | Launch Plan Reason / Destination | Notes |
|---|---|---|
| P-05 Aftercare & Progress Monitoring | Deferred to Sprint 2 | Grouped with aftercare template and configuration setup. |
| PR-04 Aftercare Participation | Deferred to Sprint 2 | Grouped with aftercare template and configuration setup. |
| A-03 Aftercare Team Management | Deferred to Sprint 2 | Grouped with aftercare template and configuration setup. |
| P-03b Payment sub-features | Deferred to Sprint 2 | Installments, multi-currency display, payment confirmation reference, and refund request are not Sprint 1 scope. |
| Patient final-balance path that unlocks real provider check-in | Deferred to Sprint 2 | Sprint 1 verifies treatment execution against a fully-paid staging booking fixture. |
| Patient/provider travel workflows and shared travel gateway | Deferred to Sprint 2 | Patient-side, provider-side, and S-04 travel integration are Sprint 2 scope. |
| Admin embedded travel oversight | Deferred to Sprint 4 | Admin travel oversight is not Sprint 1 scope. |
| Full push/email/in-app notification delivery verification | Deferred to Sprint 3 under S-03 | Sprint 1 records visible product events/states; delivery-channel verification is later. |
| Provider payout overview and admin refund-processing UI | Deferred to PR-05/A-05 where mapped | Not S-02 UI scope in Sprint 1. |
| True V2 3D head-scan viewing | Out of launch scope unless separately approved | Sprint 1 uses V1 standardized 2D photo-set capture/viewing. |
| Affiliate/partner launch surfaces | Later launch scope | FR-018 is launch scope, but no affiliate/partner Sprint 1 module is assigned. |

---

# 2. Sprint Fix Backlog

## 2.1 Sprint-Level Blockers

| Priority | Area | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|
| P0 | Sprint QA evidence | Sprint 1 cannot be closed from this report alone because no staging QA evidence is attached for all Sprint 1 modules. | 1. Open this report. 2. Review Document Control and module sections. 3. Check for staging/build evidence links. | No product environment was checked in this pass. | Each Sprint 1 module has staging QA evidence and clear pass/fail status. | TBD | Recorded only | Readiness blocker, not a confirmed product defect. |
| P0 | Core commercial journey | End-to-end staging proof is still required for registration -> inquiry -> quote acceptance -> booking/deposit. | 1. Run the core journey on staging with patient, provider, and admin access. 2. Capture screenshots/logs for every state transition. | No end-to-end staging evidence is attached in this report. | Journey is testable end-to-end on staging with provider/admin state visibility and audit/payment records. | TBD | Recorded only | Direct Sprint 1 DoD gate. |
| P1 | Treatment execution fixture | Fully-paid staging booking fixture proof is still required before PR-03 treatment execution can satisfy Sprint 1 DoD. | 1. Create or identify a fully-paid confirmed booking fixture. 2. Provider checks in patient. 3. Provider documents treatment and completes end-of-treatment fields. | Fixture was not checked in this pass. | Treatment execution is verified against a fully-paid staging booking fixture; real patient final-balance path remains Sprint 2. | TBD | Recorded only | Prevents overclaiming treatment readiness. |
| P1 | App Store account setup | Apple Developer Program and Google Play Console account verification evidence is still required. | 1. Confirm Apple account status. 2. Confirm Google Play Console account status. 3. Attach account-ready evidence. | Account status was not checked in this pass. | Both store accounts are created and verified for the release path. | TBD | Recorded only | Non-dev Sprint 1 milestone due May 25 in launch plan. |
| P1 | A-09a dependency risk | A-09a questionnaire/catalog/settings readiness is a high-risk Sprint 1 dependency because inquiry testing depends on published active sets and policy/reason configuration. | 1. Review A-09a staging screens/API. 2. Publish active inquiry questionnaire set. 3. Validate patient inquiry consumes active set. | No A-09a product evidence is attached in this report. | Questionnaire catalog, active set publication, legal content, and required settings are ready enough for Sprint 1 inquiry flow QA. | TBD | Recorded only | Launch plan risk register explicitly calls out A-09a at 30% completion as high risk. |

## 2.2 Module Fix Backlog

## P-01 - Auth & Profile Management

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging mobile review for signup, OTP, login, recovery, profile editing, password policy, and account deletion request flow.

### Remaining Fixes

| Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|
| P1 | Patient registration and profile setup | Evidence gap: P-01 Sprint 1 behavior has not been verified in staging for this report. | Run patient signup, email OTP verification, login, password recovery, profile edit, password policy validation, and account deletion request. | Not reviewed in this pass. | All P-01 launch-plan outcomes work on staging. | TBD | Recorded only | Add confirmed bugs here after product review. |

## P-02 - Quote Request & Management

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires full patient inquiry, provider selection, quote comparison, quote-specific question, cancellation cascade, and 48-hour payment-window review.

### Remaining Fixes

| Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|
| P0 | Inquiry -> quote acceptance | Evidence gap: the critical patient inquiry and quote-management path has not been verified in staging for this report. | Submit inquiry through all launch-plan steps, select providers, receive quotes, sort/filter comparison, ask quote question, accept quote, and test cancellation cascade where applicable. | Not reviewed in this pass. | Inquiry, provider selection, quote comparison, quote question, acceptance, cancellation cascade, and 48-hour payment-window behavior match Sprint 1 scope. | TBD | Recorded only | Core journey blocker until evidence is attached. |

## P-03a - Booking & Payment

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires base-currency deposit payment, released-slot validation, payment-failure hold, and booking confirmation review.

### Remaining Fixes

| Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|
| P0 | Booking and core deposit | Evidence gap: booking and deposit flow has not been verified in staging for this report. | Accept quote with provider-pre-scheduled slot, pay base-currency deposit, test failed-payment retry window, and open confirmation/itinerary view. | Not reviewed in this pass. | Deposit is captured, booking state updates correctly, stale/released slots are blocked, and confirmation/remaining-balance display is visible. | TBD | Recorded only | P-03b sub-features remain Sprint 2. |

## P-07 - Head-Scan Photo Capture & Viewing

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires mobile photo-set capture and post-processing viewing review.

### Remaining Fixes

| Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|
| P1 | Head-scan photo set | Evidence gap: V1 photo-set capture/viewing has not been verified in staging for this report. | Capture required 2D photo angles, upload set, wait for S-01 processing, and view returned media from patient record/profile. | Not reviewed in this pass. | Client validation, upload, processing callback, and viewing path work for V1 standardized 2D photo sets. | TBD | Recorded only | True 3D viewing is out of launch scope unless separately approved. |

## PR-01 - Auth & Team Management

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires provider login, invite, role assignment, permission inheritance, suspension, session revocation, and task transfer review.

### Remaining Fixes

| Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|
| P1 | Provider team access | Evidence gap: PR-01 provider auth and team-management behavior has not been verified in staging for this report. | Log in, invite team member, assign each clinic role, verify inherited permissions, suspend/remove a member, complete task transfer, and confirm session revocation. | Not reviewed in this pass. | Owner, Manager, Clinical Staff, and Billing Staff roles behave according to Sprint 1 scope. | TBD | Recorded only | Educational tour is optional UI polish, not a launch acceptance requirement. |

## PR-02 - Inquiry, Quote & Booking Management

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires provider inquiry receipt, anonymization/de-anonymization, quote build/edit/submit/withdraw, status lifecycle, booking list/detail, and check-in blocking review.

### Remaining Fixes

| Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|
| P0 | Provider quote and booking management | Evidence gap: provider-side inquiry, quote, and confirmed-booking workflow has not been verified in staging for this report. | Receive inquiry, confirm pre-payment anonymization, submit quote with appointment slot, withdraw quote with reason, accept quote from patient side, then inspect confirmed booking list/detail and check-in block state. | Not reviewed in this pass. | All eight quote statuses, quote withdrawal, booking context, de-anonymization after deposit, and check-in blocking rules work. | TBD | Recorded only | Core cross-tenant blocker until verified. |

## PR-03 - Treatment Execution & Documentation

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires fully-paid confirmed booking fixture and provider treatment documentation review.

### Remaining Fixes

| Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|
| P1 | Treatment execution fixture | Evidence gap: treatment execution has not been verified against a fully-paid staging booking fixture in this report. | Use a fully-paid confirmed booking fixture, check in patient when appointment date is due, update day statuses, capture notes, open end-of-treatment modal, and save conclusion notes, prescription, actual graft count, and final head scan link. | Not reviewed in this pass. | Treatment documentation works for Not Started, In Progress, Finished, Need Caution/Attention, Cancelled/Deferred, and required end-of-treatment data. | TBD | Recorded only | Real final-balance path is Sprint 2; do not block Sprint 1 on that deferred patient path. |

## PR-06 - Profile & Settings Management

### Review Notes

- Checked areas: Launch-plan scope only. Provider dashboard PR-06 product behavior has not been directly tested in this review pass.
- Current state: No confirmed PR-06 product defect is recorded from provider-dashboard testing yet. Admin A-02 edit-provider testing did identify issues in components that are shared with Provider edit profile.
- Code evidence checked: Admin route `/edit-provider/:id` renders `EditProfile isTeam`, which calls `ProfileSettingsTab`; Provider edit profile also uses the same `ProfileSettingsTab`. Child tabs include shared `Profile`, `Language`, `Staff`, `AwardsTab`, `Reviews`, and `Documents` components, so fixes to Admin edit controls should regression-test Provider PR-06 surfaces.
- Review limits: Requires direct provider-dashboard review for profile/settings/package catalog, including account settings, notification settings, billing settings, package catalog, staff CRUD, language ordering/search behavior, and confirmation whether duplicate awards in API are expected test data or an update bug.

### Remaining Fixes

| Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|
| P1 | Provider clinic profile and package catalog | Evidence gap: PR-06 profile, settings, language, and package catalog behavior has not been verified in staging for this report. | Edit all six clinic profile tabs, update spoken languages, verify account/notification/billing settings sections, configure role/permission settings, and create/edit provider package catalog entries. | Not reviewed in this pass. | Provider can maintain international-facing clinic profile and package catalog according to Sprint 1 scope. | TBD | Recorded only | Languages tab is critical for international scope. |

## A-01 - Patient Management & Booking Oversight

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires admin patient, inquiry, quote, booking, manual intervention, support action, and audit-trail review.

### Remaining Fixes

| Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|
| P1 | Admin patient and booking oversight | Evidence gap: A-01 oversight surfaces have not been verified in staging for this report. | Open Patient List/Detail all eight tabs, inspect inquiry/quote/booking context, perform allowed intervention with mandatory reason, and verify audit trail before/after state. | Not reviewed in this pass. | Admin can monitor and intervene only where PRD-supported, with mandatory reason and audit trail. | TBD | Recorded only | Silent quote mutation must remain unsupported. |

## A-02 - Provider Management & Onboarding

### Review Notes

- Checked areas: Launch-plan scope; FR-015 provider creation wizard; FR-026 country/calling-code dependency; uploaded screenshot links and user-provided review evidence from 2026-06-08.
- Current state: Admin created `Hairline Test Clinic 1010` with `joachimtrungtuan.work+1010@gmail.com`; provider appears in the provider list. Activation email is present, but the body only exposes button-like text with no usable link fallback, and the admin resend action does not visibly fire. Provider-side password setup and Owner login are not yet tested.
- Code evidence checked: provider creation stores provider lifecycle `status = active` while owner `password_set = false` and activation token remains pending; `NotificationService::sendActivationEmail()` builds and forwards `activation_url`; `ProviderDetails.jsx` renders `Resend Activation Email` with no handler; `AdminNotificationDropdown.jsx` only routes when `onNotificationClick` and `related_url` are present; `PhoneInput` and provider settings country-code selectors show `+code` labels without country names.
- API parity checked for existing provider `test_provider3@clinic.com` / `e4893814-817a-4565-a41f-795ad0ba609e`: API returns city `East Wellington`, country `Canada`, separate `profile_image` and `cover_image`, separate `provider_information.address` and `provider_information.map`, languages `Vietnamese`, `English`, `French`, two staff users, and one uploaded document. This means the observed cover-image issue is a frontend render bug, and the address/map issue is an Admin edit-form parity/exposure issue rather than a backend storage gap.
- Code evidence checked: Admin `/edit-provider/:id` and Provider edit profile share `ProfileSettingsTab` and its child components, so A-02 edit-profile fixes can affect PR-06 provider profile editing and should be regression-tested on both tenants.
- Blocked follow-up checks: provider activation link, password setup form, first Owner login, post-activation login state, and admin resend confirmation cannot be completed until the activation email link/resend wiring issue is fixed. Re-test these items after the P1 activation row is resolved.
- Open verification checkpoint: Activation email/link, password setup, Owner-role login, resend activation, suspension/deactivation, and audit-trail behavior remain unverified. This is not a confirmed bug unless one of those checks fails.
- Review limits: Requires activation email/link, provider password setup, Owner login, resend activation, provider detail/status actions, suspension/deactivation, and audit-trail review.

### Remaining Fixes

| Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|
| P1 | Provider activation email / resend activation | Activation email has no usable link fallback, and the admin resend activation action is not wired. | 1. Create a provider in Admin dashboard.<br>2. Open the activation email.<br>3. Try to click the `Set Your Password` text/button or copy a raw fallback link.<br>4. Return to Admin provider detail and click `Resend Activation Email`. | The email contains button-like text only; there is no raw fallback URL to copy.<br>Clicking resend in Admin produces no visible change.<br>Provider list/detail can already show lifecycle status `Active` while Owner password setup is still pending, which is technically consistent with FR-015 but ambiguous for admin review. | Activation email should include a real clickable password-setup link and a raw URL fallback.<br>Admin resend should send or queue a new activation email.<br>Admin UI should distinguish provider lifecycle status from Owner activation/password setup state, using the stored `password_set`/activation-token state where available. | https://s.letweb.net/s/eyk3yj; https://s.letweb.net/s/dz6l13 | Recorded only | Blocks activation recovery path when the button link fails.<br>`Active` alone should not be treated as proof that Owner login is ready. |
| P1 | Provider onboarding notification | New provider onboarding notification does not navigate to User Management / Providers when clicked. | 1. Create a new provider in Admin dashboard.<br>2. Open the notification dropdown.<br>3. Click the `Provider - Onboarding requested` notification for the new provider. | Notification is shown, but clicking it has no visible reaction.<br>It does not route to User Management / Providers. | Notification should deep-link to User Management / Providers.<br>Preferably the relevant provider should be visible, filtered, or highlighted so admin can continue onboarding/review. | https://s.letweb.net/s/evqyp0 | Recorded only | Required as part of admin workflow feedback after provider creation. |
| P2 | Admin support impersonation | `Login as Provider` quick action is visible on provider detail but does not respond when clicked. | 1. Open Admin dashboard provider detail for an active provider.<br>2. Click `Login as Provider` in the Action panel. | No visible response, navigation, modal, read-only impersonation session, or error feedback occurs.<br>Code evidence: the button is rendered without an `onClick` handler, and no clear impersonation API route was found in the current code search. | Per FR-015, `Login as Provider` should be a Super Admin-only support/debugging action.<br>Per FR-009, impersonation should be read-only for troubleshooting and enabled based on admin permissions, with appropriate audit/security handling.<br>If not implemented, the action should be hidden or disabled with clear unavailable-state messaging. | User report on 2026-06-08 | Recorded only | Does not block provider activation.<br>Visible dead action degrades admin support workflow and can mislead QA. |
| P2 | Provider profile media sync | Admin edit can update clinic name, avatar/profile image, and cover image, but Provider portal profile displays the avatar/profile image as the cover image instead of the saved cover. | 1. In Admin provider edit, update clinic name, profile/avatar image, and cover image.<br>2. Save changes.<br>3. Log into the provider portal for that clinic.<br>4. Open Provider Profile. | Provider portal reflects the updated clinic/profile information.<br>The cover area uses the profile/avatar image rather than the distinct cover image uploaded in Admin.<br>Code evidence: backend model/API store and return `profile_image` and `cover_image` separately, but `ProfileBanner.jsx` renders the cover image from `data?.profile_image`. | FR-015 and FR-032 require profile picture/logo and cover image as separate synchronized fields.<br>Provider portal should render cover from `cover_image`/`cover_image_url` and avatar/logo from `profile_image`/`profile_image_url`.<br>Fallback behavior should remain correct when either field is missing. | https://s.letweb.net/s/d1q0p4; https://s.letweb.net/s/g2xorj | Recorded only | Cross-tenant sync/display issue between Admin A-02 edit and Provider PR-06 profile display. |
| P2 | Provider phone capture | Admin provider creation/edit phone fields expose country code as numbers only, store/display poorly formatted international numbers, and reject pasted numbers with common separators. | 1. In Add Provider or Edit Provider, enter provider and clinic phone using country-code dropdown and local number.<br>2. Paste a phone number with spaces or dots into the number field.<br>3. Review the final Review & Create screen and provider detail/list displays. | Country-code selector does not show country names.<br>Pasted numbers containing spaces/dots are rejected by the shared phone input instead of normalized.<br>Review/detail displays raw strings such as `+8491234567890`, making country association and number validity hard to verify.<br>Code evidence: shared `PhoneInput` only updates when the number field matches `/^[0-9]*$/`; options render only the calling code while `optionLabelProp` uses the raw value. | Phone fields should show country name plus calling code during selection.<br>They should accept and normalize pasted phone numbers by stripping common separators before validation.<br>They should validate against the selected country and display normalized international format with readable spacing. | https://s.letweb.net/s/dw7nrw; User report on 2026-06-08 | Recorded only | Confirmed in Admin A-02 create/edit provider flow.<br>PR-06 should be regression-tested after the shared phone-control fix, but this row is not evidence that Provider dashboard was directly tested. |
| P2 | Admin provider edit address / map parity | Admin provider edit Basic info combines clinic address and Google map link into one visible field, while create-provider and backend API keep address and map as separate fields. | 1. Open Add Provider and inspect Clinic Information fields.<br>2. Open Admin provider edit Basic info for `test_provider3@clinic.com`.<br>3. Compare Clinic Address and Google map inputs.<br>4. Save address/map data and inspect API payload. | Create-provider has `information.address` and a separate `information.map` input.<br>Admin edit-provider shows only `information.address` under `Clinic Address / Google map link`.<br>API still stores and returns `provider_information.address` and `provider_information.map` separately.<br>Code evidence: Admin `/edit-provider/:id` shares `ProfileSettingsTab` with Provider edit profile. | Admin edit-provider should expose separate Clinic Address and Google Map Link controls, or otherwise clearly preserve and display both fields without forcing two data concepts into one input.<br>Because the component is shared, Provider edit-profile should be regression-tested after the fix. | https://s.letweb.net/s/e3xvw5 | Recorded only | API payload confirms `address = 45 Overlea Boulevard...` and `map = https://maps.google.com/?q=...`.<br>Current bug is Admin edit-form parity/discoverability, with shared-component regression risk. |
| P2 | Admin provider edit language selector | Admin provider edit `Languages` tab is not consistent with the create-provider language picker: typing in the dropdown does not reliably filter, and the language list appears unsorted/non-alphabetical. | 1. Open Admin dashboard provider edit for `test_provider3@clinic.com`.<br>2. Go to `Languages`.<br>3. Open the language selector.<br>4. Type a language name to filter.<br>5. Compare with the create-provider language selector. | Dropdown opens with a mixed order such as `English`, `Cornish`, `Korean`, `Malayalam`, `Kikuyu; Gikuyu`, etc.<br>Typing does not provide the expected searchable dropdown behavior in the observed UI.<br>Code evidence: create and edit both map the raw `get-languages` API order without alphabetic sorting; Admin edit and Provider edit share `ProfileSettingsTab` / `Language`. | Language selection should consume the centrally managed FR-021/FR-026 language catalog.<br>It should be searchable by typing.<br>It should use a predictable alphabetic or configured display order.<br>It should behave consistently between create-provider and Admin edit-provider flows.<br>Because the component is shared, Provider edit-profile should be regression-tested after the fix. | https://s.letweb.net/s/d4rxy9 | Recorded only | Found in Admin A-02 edit provider screen, not from Provider dashboard testing.<br>Shared-component regression risk only for PR-06 until Provider dashboard is directly tested. |
| P2 | Admin provider edit awards save idempotency | Admin provider edit Awards tab can keep stale pre-save award state after `Save changes`, so a second save without leaving/reloading can append duplicate award records. | 1. Open Admin provider edit for `test_provider3@clinic.com`.<br>2. Go to `Awards`.<br>3. Add a new award, for example `Test 1` / `Test awards` / `2026`.<br>4. Click `Save changes`.<br>5. Stay on the same edit page without refreshing or navigating away.<br>6. Click `Save changes` again, or edit another field and save again.<br>7. Open Admin provider detail Awards section for the same provider.<br>8. Call `provider/get-single-provider?provider_id=e4893814-817a-4565-a41f-795ad0ba609e` and inspect `data.provider_awards`. | Admin edit form does not visibly reload/reconcile Awards state after save.<br>Provider detail shows duplicate awards; reviewer test created `Test 1` once, saved twice without reload, and then saw two `Test 1` awards.<br>Live API check on 2026-06-08 returns `awards_count = 5` for the provider after earlier repeated saves.<br>Existing duplicated awards have different `award_id` values, confirming separate persisted records. | After a successful save, Admin edit state should reconcile with backend response/refetch so newly created awards receive stable IDs in form state.<br>Saving again without changes must be idempotent and must not create duplicate backend records.<br>Existing awards should be updated by stable award ID, not re-created.<br>Admin edit UI, Admin provider detail, and API should represent the same award set after save. | https://s.letweb.net/s/e6jx3k; Live API check on 2026-06-08 | Recorded only | Code evidence: backend creates a new award when `awards[index][id]` is missing or cannot be matched. Frontend refetches after save but explicitly avoids updating awards from the refetch, then sets `initialAwards` from current form values; this can leave newly created awards without backend `award_id`, causing the next save to send them as new again.<br>Confirmed in Admin A-02 edit flow; Provider PR-06 should be regression-tested because the edit component is shared. |
| P2 | Provider document preview | Uploaded provider document/image preview is broken in the review/detail display. | 1. Upload a provider document during A-02 wizard.<br>2. Proceed to Review & Create or provider detail view.<br>3. Inspect the Documents section. | Document area shows broken image/file placeholders and hash-like filename fragments instead of a readable document preview/list item. | Uploaded records should display stable file metadata.<br>Use type icon/preview where supported.<br>Expose view/download/remove controls as appropriate for record-keeping. | https://s.letweb.net/s/gxj9wp | Recorded only | FR-015 documents are record-keeping and do not block activation.<br>They must remain visible and auditable. |

## A-09a - Content & Treatment Management

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires high-priority review because launch plan risk register identifies A-09a completion as a high Sprint 1 risk.

### Remaining Fixes

| Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|
| P1 | Questionnaire, legal content, and settings configuration | Evidence gap: A-09a content/settings readiness has not been verified in staging for this report. | Manage questionnaire catalog and active set, publish legal documents, verify acceptance coverage, update OTP config, country/calling-code list, cancellation/deletion reasons, and OTP email template. | Not reviewed in this pass. | Active questionnaire/settings/legal content support Sprint 1 inquiry, auth, account lifecycle, and compliance flows. | TBD | Recorded only | Treat as hard readiness check due to risk-register callout. |

## S-01 - Head Scan Media Processing Service

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires media-processing API/service evidence tied to patient upload flow.

### Remaining Fixes

| Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|
| P1 | Media intake and alert classification | Evidence gap: S-01 processing behavior has not been verified in staging for this report. | Upload head-scan photo set, inspect processing job, verify normalized payload, media URI, and alert classification result. | Not reviewed in this pass. | Processing handles concurrent intake within target latency and returns trusted media/classification output. | TBD | Recorded only | Required for provider review and downstream clinical record. |

## S-02 - Payment Processing Service

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires Stripe deposit charge, webhook, status, audit, and refund-eligibility service review.

### Remaining Fixes

| Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|
| P0 | Core deposit infrastructure | Evidence gap: S-02 deposit infrastructure has not been verified in staging for this report. | Pay deposit through Stripe, observe pending/completed/failed status, trigger webhook handling, inspect booking/payment state update, and verify immutable audit entries. | Not reviewed in this pass. | Deposit charge, payment status, webhook update, audit log, and refund eligibility calculation work for Sprint 1. | TBD | Recorded only | Refund UI is not Sprint 1 scope. |

## S-05 - Media Storage Service

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires encrypted bucket, signed URL, access-control, and lifecycle-policy evidence.

### Remaining Fixes

| Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|
| P1 | Encrypted media storage | Evidence gap: S-05 media storage behavior has not been verified in staging for this report. | Upload media, inspect storage target, test signed URL access, test unauthorized access denial, and confirm lifecycle policy configuration. | Not reviewed in this pass. | Media is encrypted, access is controlled through signed URLs, and retention/lifecycle policies are configured for later compliance alignment. | TBD | Recorded only | Supports FR-002 media storage layer. |

---

# 3. Not For This Sprint

| Item | Why It Is Not In This Sprint | Follow-Up Notes |
|---|---|---|
| Aftercare activation journey | Deferred to Sprint 2 with P-05, PR-04, A-03, A-09b, and related configuration. | Keep out of Sprint 1 fix backlog unless a Sprint 1 treatment-completion dependency prevents Sprint 2 activation. |
| Payment installments, multi-currency display, receipt/reference UX, refund request UI | Deferred to Sprint 2 under P-03b and payment-rule configuration. | Sprint 1 validates core base-currency deposit only. |
| Final-balance patient payment path | Deferred to Sprint 2. | Sprint 1 PR-03 uses a fully-paid staging booking fixture for treatment execution verification. |
| Travel and logistics | Patient/provider workflows and S-04 gateway are Sprint 2; admin embedded oversight is Sprint 4. | Do not treat missing travel surfaces as Sprint 1 bugs. |
| Full notification delivery-channel verification | Deferred to Sprint 3 under S-03. | Sprint 1 still needs visible event/state recording where relevant. |
| Affiliate/partner workflows | Later launch scope, not assigned to Sprint 1. | FR-018 is launch-scope but not Sprint 1 module scope. |
| True 3D head-scan viewing | Out of launch scope unless separately approved. | Sprint 1 validates V1 standardized 2D photo sets only. |
