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
