# Sprint 1 Provider Onboarding Review - 2026-06-08

**Update Type:** Sprint readiness backlog update  
**Date:** 2026-06-08  
**Primary File:** `local-docs/product-plans/2026-05-29/sprint-1-readiness-fix-backlog.md`  
**Evidence Source:** Uploaded screenshot links, API/code evidence, and user-reported Admin/provider review behavior

---

## Summary

Updated the Sprint 1 readiness backlog with the first provider-focused product review findings for Admin A-02 Provider Management & Onboarding and the shared provider/admin phone-input experience. The sprint report and template were also given a `Task Status` column in their `Remaining Fixes` tables so backlog items can be marked `Recorded only` or `Task created` without changing the existing report structure.

The review confirms only partial A-02 progress: a new provider (`Hairline Test Clinic 1010`, `joachimtrungtuan.work+1010@gmail.com`) was created through the Admin wizard and appears in the provider list. Provider activation, password setup, Owner-role login, resend activation, suspension/deactivation, and audit-trail behavior remain unverified.

---

## Findings Added

- A-02 provider onboarding note changed from unreviewed evidence gap to partial verification with remaining activation/Owner-login checks; same-session refinement moved this out of the `Remaining Fixes` table because it is an open verification checkpoint, not a confirmed product bug.
- Added A-02 notification defect: clicking the new `Provider - Onboarding requested` notification has no visible routing behavior.
- Added A-02 admin support impersonation defect: `Login as Provider` is visible but has no response; FR-015/FR-009 expect a Super Admin-only/read-only troubleshooting action or a clear unavailable state.
- Added A-02/PR-06 provider profile media sync defect: Admin edit can save distinct avatar/profile and cover images, but Provider portal profile renders the avatar/profile image as the cover image; code evidence points to frontend `ProfileBanner.jsx` binding cover display to `profile_image` despite backend storing/returning `cover_image` separately.
- Added A-02 phone-capture UX defect: country-code selectors expose only numeric calling codes and display raw international numbers, making country association and validation hard to verify.
- Added A-02 document-preview defect: uploaded provider documents/images appear as broken preview/hash-like filename fragments in review/detail display.
- Checked code evidence for A-02 activation, notification routing, and phone-code UX so the report lines up with source behavior instead of screenshot-only observations. Same-session follow-up clarified that `Active` is the provider lifecycle status while Owner password setup is tracked separately through `password_set` and activation-token state.
- Expanded the A-02 phone-input finding after Admin create/edit testing showed pasted phone numbers with spaces or punctuation are rejected at input time instead of normalized. PR-06 remains a regression target only because provider settings consume the same phone-input pattern.
- Added A-02 address-map parity finding: backend and create-provider flow keep clinic address and Google map link as separate `information.address` / `information.map` fields, but Admin provider edit Basic info exposes only one combined address/map field.
- Added Admin A-02 / shared edit-component language-selector parity finding: Admin provider edit language picker does not reliably support typed filtering in the observed UI and both create/edit consume raw unsorted language API order. Code check confirmed Admin `/edit-provider/:id` and Provider edit profile share `ProfileSettingsTab`, so fixes need regression coverage on both tenants.
- Added A-02 awards save-idempotency finding: Admin edit UI can keep stale pre-save awards state after `Save changes`, so saving again without refresh/back navigation appends duplicate award records. Reviewer reproduced this by creating `Test 1`, saving twice without reload, then seeing duplicate `Test 1` awards (`https://s.letweb.net/s/e6jx3k`). Code evidence shows frontend refetches after save but intentionally avoids updating awards from refetch, then stores current form awards as initial state, while backend creates new awards when submitted rows lack stable IDs.
- Added the first confirmed PR-01 Provider Team defect: Admin provider detail shows existing staff for `test_provider3@clinic.com`, including a Clinical Staff member, but the Provider dashboard `Team` page renders `No data` for the same tenant. Code review confirmed the current provider team UI reads from `provider_team_members`, while Admin staff management and older onboarding/invitation flows still read/write `provider_users`, creating a cross-surface roster mismatch.
- Added a second confirmed PR-01 invitation defect: Provider `Invitations` correctly records pending staff invites, but the invitation email uses `/accept-invitation/{id}` while the working frontend landing page and dashboard copy-link use `/invitation/{id}`. As a result, the email button and raw fallback link send invited staff to a 404 path instead of the account-setup page.
- Added a PR-01 invitation account-setup UX finding: the public invitation page uses a single strict phone text box instead of the more consistent country-code-plus-number pattern used elsewhere, and it rejects pasted phone numbers containing spaces such as `+1 647 555 0101`.
- Added a third PR-01 invitation lifecycle defect: after a manager invitation was accepted successfully and the account appeared in the Provider `Team` list, the same email still remained visible in `Invitations` with status `ACCEPTED` instead of disappearing from the operational queue or moving to history.
- Added a P0 PR-01 RBAC containment defect: a newly accepted Provider Manager account can reach Hairline admin/team-dashboard routes such as `/providers` and `/settings/app-settings`. Code review indicates this is not a one-off setup mistake: invitation signup creates a `User` + `api` token for provider staff, frontend route access falls back open for `profile_type = provider` when no path-permission model is present, and some provider-management APIs are exposed to both `provider` and `api` guards.
- Live API check for `test_provider3@clinic.com` confirmed current stored parity for city (`East Wellington`), separate profile/cover images, separate address/map fields, provider languages, staff, and document payload; this narrowed the cover issue to frontend rendering and address/map issue to edit-form exposure.
- Added sprint scaffold guidance that screenshot evidence must use persistent uploaded URLs; local screenshot paths, clipboard-only image references, or temporary file links should not be used in `Evidence Link`.
- Added sprint scaffold guidance to use `<br>` line breaks inside long Markdown table cells, especially reproduction steps, actual outcome, expected outcome, and notes.

---

## Requirement Anchors

- `FR-015 Provider Management`: admin-created provider accounts, activation email/password setup, provider documents for record-keeping, and provider status lifecycle.
- `FR-009 Provider Team Roles`: single Owner account followed by role-based team invitation.
- `FR-026 App Settings & Security Policies`: country/calling-code list with country name, ISO code, calling code, flag/display order, and active status.
- `FR-032 Provider Dashboard Settings`: provider phone/account settings and public clinic phone fields consuming FR-026 calling-code data.

---

## Files Changed

- Updated `local-docs/product-plans/2026-05-29/sprint-1-readiness-fix-backlog.md`
- Updated `local-docs/product-plans/template/sprint-readiness-fix-backlog-template.md`
- Created this update log entry
- Updated `local-docs/project-requirements/update-logs/README.md`

## Minor Updates

- Refined the sprint backlog scaffold guidance so `Task Status` can store the created Plane key inline, using a short format such as `Task created (HAIRL-123)`, instead of introducing a separate Plane tracking column.
- Refined the sprint backlog scaffold and active Sprint 1 backlog so `Task Status` now distinguishes `Review pending` placeholder/evidence-gap rows from `Recorded only` confirmed findings, while still keeping `Task created (HAIRL-xxx)` for Plane-linked items.
- Updated PR-01 review notes so the backlog now preserves which parts of the clinic staff invite flow are already working in staging: invitation creation reaches `Invitations`, dashboard `Copy Link` opens the valid public invitation page, invited staff can complete account setup, accepted staff can log in, and accepted accounts appear in the Provider `Team` list. The same pass also broadened the P0 RBAC containment note to reflect reviewer confirmation that the admin-surface exposure is affecting invited `Manager`, `Clinical Staff`, and `Billing Staff` accounts, not just the first manager test account.
- Replaced the older PR-01 `Team`-empty symptom with a more current cross-surface roster-parity finding after four invited staff were created successfully. Provider `Team` and accepted `Invitations` now show the four invited staff, but Provider profile/detail, Provider edit-profile `Staff list`, Admin provider detail `Staff list`, and Admin edit-provider `Staff list` still remain pinned to the legacy two-member roster. Live API checks on 2026-06-08 confirmed the same split: `provider/get-single-provider`, `provider/get-provider-staff`, and `admin/provider-management/providers/{id}/staff` each still return only the two old `provider_users` rows for `test_provider3@clinic.com`.
- Added confirmed shared-component crash evidence for `Add New Staff` in profile-edit `Staff list`: both Provider and Admin edit-profile flows can blank the page with `TypeError: h.map is not a function`, and code review traced this to `StaffModal.jsx` mapping `roleData` as an array even though `team/roles` returns `{ status, data }`.
- Added three more confirmed PR-01 team-management findings from direct staff-lifecycle testing: the Provider `Team` list uses `Active` / `Inactive` terminology that drifts from FR-009's `remove or suspend` language, the staff detail page does not show key account-setup information such as phone number, and toggling a member from `Inactive` back to `Active` still does not restore login access. Code review tied the action-model inconsistency to the generic `PUT team/members/{id}` update path, while the dedicated suspend path uses a different lifecycle implementation.
- Added another confirmed PR-01 suspend-lifecycle finding from the staff detail page: the `Remove or Suspend` modal is exposed, but clicking `Suspend Team Member` only shows the toast `Suspend flow not yet connected to API`. Code review confirmed this is currently hardcoded in `pages/providerDashboard/team/TeamMemberDetail.jsx`, so the dedicated suspend UI is still a dead-end even though a backend suspend endpoint exists separately.
- Added a confirmed PR-01 `Role & Permission` modal defect for invitation-created staff: the current role renders as `—`, and clicking `Change role` returns server error. Code review traced this to the mixed identity model in the invite flow: staff created from invitation are stored as `User` records with provider roles assigned onto `model_has_roles`, while the detail modal and role-change flow still expect `ProviderUser`-style role/designation payloads and provider-guard role mutation behavior.
- Added a Provider dashboard breadcrumb cleanup note for the staff detail page: the `Members` breadcrumb segment routes to a 404 and does not provide a useful navigation target, so the detail view should keep only the back path to `Team` unless a real members list route is added.
- Added a deeper structural provider-account finding after live API re-check: invited clinic staff are not just missing from the clinic's canonical admin staff set; `provider/get-all-providers` now returns them as standalone provider records with personal-name `provider_name`, `staff_count = 1`, and no owner/location metadata, while Admin `Staff list` and `Ownership Override` still operate only on the old `ProviderUser` roster under the original clinic. The backlog now explicitly records the required contract from `system-data-schema.md`: `providers` must remain clinic entities and `provider_users` must remain staff belonging to a clinic.
- Expanded the A-02 provider activation row so Admin recovery requirements now explicitly include a dashboard-level `Copy activation link` action, in addition to email delivery and resend behavior.
- Added the uploaded screenshot `https://s.letweb.net/s/dkmoqv` to the PR-01 invitation phone-input finding so the validation-error evidence is preserved with a persistent URL.
- Added a minor PR-01 invite-flow copy issue: the Invite staff modal email placeholder uses the misspelling `Email addresse` instead of `Email address`.

## Minor Tracking Updates

- Updated `local-docs/product-plans/2026-05-29/sprint-1-readiness-fix-backlog.md` Task Status values from `Task created` to `Task drafted` for 25 PR-01, PR-06, and A-02 bug rows after creating the Plane-ready draft bug task artifact `local-docs/project-automation/task-creation/2026-06-08/implementation-tasks-2026-06-08-001.md`.
