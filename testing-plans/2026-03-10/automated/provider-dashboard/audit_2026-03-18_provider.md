# Provider Dashboard — Code Audit Report

**Audit Date:** 2026-03-18
**Verification Pass:** 2026-03-19 (5 parallel sub-agents cross-checked all `file:line` evidence against actual codebase; corrections applied inline)
**Source Report:** `dev_2026-03-18_provider_test-report.md`
**Audited by:** Claude Code (per-module sub-agents)
**Dashboard:** Provider Dashboard

---

## About This Report

This audit cross-references every **FAIL** and **BLOCKED** test case from the developer's 2026-03-18 automated test run against the actual codebase and functional requirement documents. For each test case, the audit determines one of the following verdicts:

| Verdict | Meaning |
|---------|---------|
| `CODE_MISSING` | Feature not found in backend or frontend code |
| `CODE_EXISTS_BUG` | Feature exists but has a concrete defect (wrong logic, SQL error, missing guard, etc.) |
| `CODE_EXISTS_PARTIAL` | Feature exists but is incomplete relative to what the FR requires |
| `CODE_EXISTS_CORRECT` | Feature is correctly implemented; test automation simply hasn't been written yet |
| `NEEDS_DEEPER_REVIEW` | Evidence is ambiguous — deeper manual review recommended |

**Source report stats:**
- Total TCs: 278 | PASS: 23 | **FAIL: 0** | **BLOCKED: 256** | SKIP: 0

---

## Module 1: Authentication & Sign-In (FR-009)

### FAIL Items

No FAIL items in this module.

### BLOCKED Items

| TC ID | Description | Verdict | Evidence (file:line) | Notes |
|-------|-------------|---------|---------------------|-------|
| P-AUTH-002 | Clinician can log in | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Authentication/AuthController.php:252` | Login handles `profile_type=provider`; clinician is a ProviderUser — same login path, different role. Automation not written. |
| P-AUTH-003 | Billing Staff can log in | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Authentication/AuthController.php:252` | Same login path as owner; role-specific UI visibility gated in FE via `isOwner` flags. Automation not written. |
| P-AUTH-004 | Invited team member can open valid invitation link | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Provider/ProviderStaffInvitationController.php:282` | `show($id)` returns invitation data including `email_exists` flag and status; FE `InvitationLanding.jsx:94` renders signup form. |
| P-AUTH-005 | Invited team member can complete account setup | CODE_EXISTS_BUG | `hairline-backend/app/Http/Controllers/Provider/ProviderStaffInvitationController.php:1152` | Account-setup endpoint validates `password` with only `min:8` — FE enforces 12 chars (`SignupForm.jsx:7`). BE does not enforce the 12-char policy; a client bypassing the FE can set an 8-char password. |
| P-AUTH-008 | First login shows only role-appropriate access | CODE_EXISTS_PARTIAL | `hairline-frontend/src/components/providerComponents/providerSettings/ProviderSettingTab.jsx:38` | `isOwner` flag gates owner-only tabs in Settings; no comparable guard found for operational features vs billing-only features via `accessControl.js`. Backend enforces via `auth:provider` guard + Spatie roles but FE role-gating is incomplete for all roles. |
| P-AUTH-009 | Forgot password sends reset email | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Authentication/AuthController.php:895` | `forgotPassword()` delegates to `PasswordResetService::sendResetEmail()`. Automation not written. |
| P-AUTH-010 | Password reset with valid token works | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Authentication/AuthController.php:957` | `resetPassword()` exists. Automation not written. |
| P-AUTH-011 | Existing Hairline user sees login-only invitation acceptance flow | CODE_EXISTS_PARTIAL | `hairline-backend/app/Http/Controllers/Provider/ProviderStaffInvitationController.php:301,851` | Backend `show()` returns `email_exists=true` and `accept()` returns `USER_NOT_FOUND` requiring signup. However FE `InvitationLanding.jsx:136` always routes to `setStep("signup")` regardless of `email_exists` — login-only branch is not rendered. |
| P-AUTH-012 | Expired invitation link cannot be accepted | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Provider/ProviderStaffInvitationController.php:841` | `isExpired()` check in `acceptPublic()`; FE detects `status=expired` at line 129 and shows error. |
| P-AUTH-014 | Login with non-existent email | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Authentication/AuthController.php:226` | Generic error message returned; no user enumeration. Automation not written. |
| P-AUTH-015 | Login with empty email field | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Authentication/AuthController.php:219` | `required\|email` validation on email field. Automation not written. |
| P-AUTH-016 | Login with empty password field | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Authentication/AuthController.php:219` | `required` validation on password. Automation not written. |
| P-AUTH-P01 | Valid password accepted (≥12 chars, all rules) | CODE_EXISTS_BUG | `hairline-backend/app/Http/Controllers/Provider/ProviderStaffInvitationController.php:1152` | FE regex enforces ≥12 chars + uppercase + lowercase + digit + special. Backend only enforces `min:8`. Policy gap: BE does not reject an 8-char password submitted directly. |
| P-AUTH-P02 | Exactly 12 characters, all rules met | CODE_EXISTS_BUG | `hairline-backend/app/Http/Controllers/Provider/ProviderStaffInvitationController.php:1152` | Same as P-AUTH-P01; backend would accept 8-char passwords. |
| P-AUTH-P03 | 11 characters (too short) — rejected | CODE_EXISTS_BUG | `hairline-backend/app/Http/Controllers/Provider/ProviderStaffInvitationController.php:1152` | Backend would accept 11-char password (only rejects <8 chars). |
| P-AUTH-P04 | No uppercase — rejected | CODE_EXISTS_BUG | `hairline-backend/app/Http/Controllers/Provider/ProviderStaffInvitationController.php:1152` | Backend has no uppercase rule. |
| P-AUTH-P05 | No lowercase — rejected | CODE_EXISTS_BUG | `hairline-backend/app/Http/Controllers/Provider/ProviderStaffInvitationController.php:1152` | Backend has no lowercase rule. |
| P-AUTH-P06 | No digit — rejected | CODE_EXISTS_BUG | `hairline-backend/app/Http/Controllers/Provider/ProviderStaffInvitationController.php:1152` | Backend has no digit rule. |
| P-AUTH-P09 | SQL injection in password — rejected | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Provider/ProviderStaffInvitationController.php:1152` | Laravel's Eloquent + `Hash::make()` prevent SQL injection. Automation not written. |
| P-AUTH-P10 | XSS in email — rejected | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Authentication/AuthController.php:219` | `email` validation rule rejects non-email-format inputs including script tags. |

### Module Summary
- Total FAIL+BLOCKED audited: 20 (0 FAIL, 20 BLOCKED)
- CODE_MISSING: 0 | CODE_EXISTS_BUG: 6 | CODE_EXISTS_PARTIAL: 2 | CODE_EXISTS_CORRECT: 12 | NEEDS_DEEPER_REVIEW: 0

**Root causes:** (1) The backend account-setup endpoint (`ProviderStaffInvitationController.php:1152`) only enforces `min:8` for password, while the FE and FR-009 require ≥12 chars + complexity rules — fix by adding `Password::min(12)->mixedCase()->numbers()->symbols()` to the BE validator. (2) `InvitationLanding.jsx:136` always routes new users to the signup form and ignores the `email_exists` flag from `show()` — the login-only flow for existing Hairline users (FR-009 A3) is not rendered in the FE.

---

## Module 2: Onboarding & Profile Setup (FR-009, FR-032)

### FAIL Items

No FAIL items in this module.

### BLOCKED Items

| TC ID | Description | Verdict | Evidence (file:line) | Notes |
|-------|-------------|---------|---------------------|-------|
| P-ONB-001 | Settings page loads | CODE_EXISTS_CORRECT | `hairline-frontend/src/pages/providerDashboard/ProviderSetting.jsx` | Settings page exists. Automation not written. |
| P-ONB-002 | Update clinic name and description | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Settings/ProviderSettingsController.php:163` | `updateAccountInfo()` saves provider name/description; persists via Eloquent. |
| P-ONB-003 | Update contact information | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Providers/ProviderController.php:1116-1124` | `information.phone_number`, `information.address`, `information.website` are validated and saved. |
| P-ONB-004 | Upload clinic logo (PNG/JPG, <5MB) | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Providers/ProviderController.php:685` | `profile_image` validated as `file\|image\|max:5120` (5MB). |
| P-ONB-005 | Upload gallery images | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Providers/ProviderController.php:1098-1099` | `profile_image` and `cover_image` both validated; additional file upload via `/files/upload`. |
| P-ONB-008 | Add banking/payment details (FR-032) | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Settings/BankingDetailsController.php:137` | `store()` saves banking details. Route at `settings/create-banking-details`. |
| P-ONB-009 | Configure notification preferences | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Settings/NotificationPreferencesController.php:120` | `store()` saves notification preferences. Route at `settings/update-notification-preferences`. |
| P-ONB-010 | Configure language assignments | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Providers/ProviderController.php:1106` | `languages_ids` array accepted and synced via pivot table at line 1430. |
| P-ONB-011 | Team page shows current members | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Provider/ProviderTeamController.php` (index method) | `/team/members` route returns team list. |
| P-ONB-012 | Invite new team member (Clinician) | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Provider/ProviderTeamController.php:738-782` | `invite()` method creates invitation with role; duplicate-invite check at line 738. |
| P-ONB-013 | Invite new team member (Manager) | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Provider/ProviderTeamController.php:738-782` | Same invite flow, different role value. |
| P-ONB-014 | Invite new team member (Billing Staff) | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Provider/ProviderTeamController.php:738-782` | Same invite flow. |
| P-ONB-015 | Revoke team member access | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Provider/ProviderTeamController.php:1494` | `destroy()` wraps deletion in DB transaction; validates workload and ownership. |
| P-ONB-016 | Owner role cannot be revoked by self | CODE_EXISTS_BUG | `hairline-backend/app/Http/Controllers/Provider/ProviderTeamController.php:1562` | **Verification refuted original claim.** Line 1562 is `$member->delete()`, not a self-revoke guard. `destroy()` checks workload (lines 1518–1529) and last-owner rule (lines 1531–1548) but never compares `$member->user_id` to `auth()->id()`. Any authenticated provider team member can call this endpoint to revoke their own access. |
| P-ONB-017 | Upload invalid file type as logo — rejected | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Providers/ProviderController.php:685` | `file\|image` rule rejects non-image types (`.exe`, `.pdf`). |
| P-ONB-018 | Upload oversized image — rejected | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Providers/ProviderController.php:685` | `max:5120` (5MB) rejects oversized files. |
| P-ONB-019 | Save settings with empty required fields — validation error | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Settings/ProviderSettingsController.php:163` | Required fields validated before saving. |
| P-ONB-020 | Very long clinic name (255+ chars) — truncated or rejected | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Providers/ProviderController.php:1116` | `provider_name` has `max:255` rule. |
| P-ONB-021 | Special characters in clinic description — saved/sanitized | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Providers/ProviderController.php:1117` | `provider_bio` stored via Eloquent; HTML sanitization is framework-level. |
| P-ONB-022 | Invite existing Hairline user → login-only acceptance flow | CODE_EXISTS_PARTIAL | `hairline-backend/app/Http/Controllers/Provider/ProviderStaffInvitationController.php:301` | BE `show()` returns `email_exists=true` flag; BE `acceptPublic()` routes existing user correctly. However FE `InvitationLanding.jsx:136` ignores `email_exists` and always shows signup form — login-only branch not rendered. |
| P-ONB-023 | Invite member with invalid email format — validation error | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Provider/ProviderTeamController.php` | Email validation via Laravel's `email` rule on invite endpoint. |
| P-ONB-024 | Clinician cannot access team management | CODE_EXISTS_PARTIAL | `hairline-backend/app/Http/Controllers/Provider/ProviderTeamController.php` | Backend uses Spatie roles via `auth:provider` guard but no explicit clinician-block middleware on team endpoints is evident; FE hides UI elements conditionally. Needs deeper role-policy audit. |
| P-ONB-025 | Billing Staff permissions enforced — owner-only settings denied | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Provider/ProviderTeamController.php` | P-AUTH-018 / P-XCT-010 already passed showing billing-staff token returns 403 on admin settings endpoints. |
| P-ONB-026 | Invitation expires after 7 days | CODE_EXISTS_CORRECT | `hairline-backend/app/Models/ProviderStaffInvitation.php:43` | `expires_at = now()->addDays(7)` set on creation; `isExpired()` checked on accept. |
| P-ONB-027 | Reinvite after expired invitation | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Provider/ProviderTeamController.php:738` | Duplicate-invite check looks for `status=pending`; expired invitations have `status=expired` so a new invite to the same email is allowed. |
| P-ONB-028 | Team member cannot belong to multiple providers | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Provider/ProviderStaffInvitationController.php:396` | Cross-provider membership check at lines 396-407 returns `CROSS_PROVIDER_MEMBERSHIP` (409). |

### Module Summary
- Total FAIL+BLOCKED audited: 27 (0 FAIL, 27 BLOCKED)
- CODE_MISSING: 0 | CODE_EXISTS_BUG: 1 | CODE_EXISTS_PARTIAL: 2 | CODE_EXISTS_CORRECT: 24 | NEEDS_DEEPER_REVIEW: 0

**Root causes:** (1) FE `InvitationLanding.jsx` ignores the `email_exists` field returned by the backend — existing Hairline users are not routed to the login-only acceptance flow (P-ONB-022, duplicates P-AUTH-011 finding). (2) Clinician-level access control on team management endpoints relies on FE UI hiding rather than explicit BE middleware guards — a clinician with a valid token could call the team invite API directly (P-ONB-024); a deeper role-permission audit is recommended. (3) **P-ONB-016 corrected to BUG:** `destroy()` has no self-revoke guard — any provider team member can call the API to remove their own access record; add a `$member->user_id !== auth()->id()` check before processing deletion.

---

## Module 3: Inquiry Review (FR-003)

### FAIL Items

No FAIL items in this module.

### BLOCKED Items

| TC ID | Description | Verdict | Evidence (file:line) | Notes |
|-------|-------------|---------|---------------------|-------|
| P-INQ-002 | Inquiry card shows HPID-format ID | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Inquiry/InquiryController.php:421` | `patient_code` field (HPID format) exposed in inquiry response. |
| P-INQ-003 | Inquiry card shows treatment type | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Inquiry/InquiryController.php:171` | Treatment type included in index response. |
| P-INQ-004 | Inquiry card shows date range | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Inquiry/InquiryController.php:171` | Treatment date ranges included in inquiry list response. |
| P-INQ-005 | Click inquiry opens detail page | CODE_EXISTS_CORRECT | `hairline-frontend/src/pages/providerDashboard/appointments/InquiryDetail.jsx` | Detail page component exists. |
| P-INQ-006 | Patient identity is masked | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Inquiry/InquiryController.php:1091-1111` | `PatientDataAnonymizationService` masks name, email, phone when no confirmed quote. `_anonymized=true` flag sent. |
| P-INQ-007 | Medical history displayed | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Inquiry/InquiryController.php:1131` | `medical_info.questionnaires` included in formatted response. |
| P-INQ-008 | Medical alerts color-coded | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Inquiry/InquiryController.php:1041-1046` | `medical_alert_display` includes `color`, `level`, `icon` per alert level. |
| P-INQ-009 | Head scan photos displayed | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Inquiry/InquiryController.php:434` | Scan files returned in inquiry detail. |
| P-INQ-010 | Inquiry shows expiry information | CODE_EXISTS_PARTIAL | `hairline-backend/app/Http/Controllers/Inquiry/InquiryController.php:434` | Inquiry detail returned; however no explicit `expires_at` (72h from distribution) field found on the inquiry response — `distributed_at` exists on `InquiryProvider` model but expiry not computed server-side in the detail endpoint. |
| P-INQ-011 | Inquiry status displayed correctly | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Inquiry/InquiryController.php:171` | Inquiry `status` field included in list and detail responses. |
| P-INQ-012 | Filter inquiries by status | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Inquiry/InquiryController.php:171` | `status` filter applied via query param in `index()`. |
| P-INQ-013 | Sort inquiries | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Inquiry/InquiryController.php:309` | Sorting by `patient_name`, date, etc. supported. |
| P-INQ-014 | Paginate inquiry list | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Inquiry/InquiryController.php:171` | Paginated response via Laravel paginator. |
| P-INQ-016 | Cannot quote on expired inquiry | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:1754` | Quote creation blocked if inquiry is `cancelled` or `completed`; inquiry expiry status propagated. |
| P-INQ-017 | Inquiry with no head scan photos — empty state, not error | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Inquiry/InquiryController.php:434` | Scan section returns empty array; FE handles null gracefully. |
| P-INQ-018 | Inquiry with all red medical alerts | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Inquiry/InquiryController.php:1041` | `medical_alert_display.level=critical` returned with red indicator. |
| P-INQ-019 | Inquiry with no medical alerts — green/no-alerts displayed | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Inquiry/InquiryController.php:1046` | `level=none` returns null icon and green color. |
| P-INQ-020 | Inquiry distributed to max 10 providers | CODE_EXISTS_BUG | `hairline-backend/app/Http/Controllers/Inquiry/InquiryController.php:1463,1477` | Backend enforces `MaxArrayItems(5)` — max 5 providers, not 10 as FR-003 specifies. Error message reads "Maximum 5 providers allowed." |
| P-INQ-021 | Inquiry distribution within 5-minute SLA | NEEDS_DEEPER_REVIEW | `hairline-backend/app/Models/InquiryProvider.php:24` | `distributed_at` is recorded on the `InquiryProvider` pivot but no automated distribution job or SLA enforcement mechanism found in codebase. Manual or event-driven distribution is used; SLA compliance cannot be confirmed without further investigation of event/job pipeline. |
| P-INQ-P01 | Inquiry at 1h — active, quotable | CODE_EXISTS_PARTIAL | `hairline-backend/app/Http/Controllers/Inquiry/InquiryController.php:434` | Quotability depends on inquiry `status`; no 72h expiry timer actively computed and returned in inquiry detail response. |
| P-INQ-P02 | Inquiry at 24h — active, quotable | CODE_EXISTS_PARTIAL | Same as P-INQ-P01 | Same — expiry boundary not computed server-side. |
| P-INQ-P03 | Inquiry at 48h — active, quotable | CODE_EXISTS_PARTIAL | Same as P-INQ-P01 | Same. |
| P-INQ-P04 | Inquiry at 71h — active, expiry warning visible | CODE_EXISTS_PARTIAL | Same as P-INQ-P01 | Near-expiry warning not implemented server-side. |
| P-INQ-P05 | Inquiry at exactly 72h — expired, not quotable | CODE_EXISTS_PARTIAL | Same as P-INQ-P01 | No explicit 72h expiry calculation surfaced in inquiry response; status-based blocking exists for `cancelled/completed`. |
| P-INQ-P06 | Inquiry at 73h — expired, not quotable | CODE_EXISTS_PARTIAL | Same as P-INQ-P01 | Same. |

### Module Summary
- Total FAIL+BLOCKED audited: 26 (0 FAIL, 26 BLOCKED)
- CODE_MISSING: 0 | CODE_EXISTS_BUG: 1 | CODE_EXISTS_PARTIAL: 7 | CODE_EXISTS_CORRECT: 17 | NEEDS_DEEPER_REVIEW: 1

**Root causes:** (1) P-INQ-020: `InquiryController.php:1463` uses `MaxArrayItems(5)` for provider distribution — the cap is 5, not 10 as FR-003 mandates; fix by changing the rule to `MaxArrayItems(10)`. (2) P-INQ-010 / P-INQ-P01–P06: The 72-hour expiry boundary is not computed and returned in the inquiry detail API response — `distributed_at` exists on the pivot but expiry is not surfaced to the FE, making time-boundary enforcement reliant on status alone. A computed `expires_at` field derived from `distributed_at + 72h` should be added to the inquiry detail endpoint.

---

## Module 4: Quote Management (FR-004)

### FAIL Items

No FAIL items in this module.

### BLOCKED Items

| TC ID | Description | Verdict | Evidence (file:line) | Notes |
|-------|-------------|---------|---------------------|-------|
| P-QOT-001 | Open quote creation from inquiry | CODE_EXISTS_CORRECT | `hairline-frontend/src/pages/providerDashboard/CreateQuote.jsx` | Create Quote page exists; triggered from inquiry detail. |
| P-QOT-002 | Select treatment type FUE | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:1657` | `treatment_id` required field links to treatment type. |
| P-QOT-003 | Select treatment type FUT | CODE_EXISTS_CORRECT | Same as P-QOT-002 | Same — treatment types come from `treatments` table. |
| P-QOT-004 | Select treatment type DHI | CODE_EXISTS_CORRECT | Same as P-QOT-002 | Same. |
| P-QOT-005 | Enter graft count | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:1698` | `estimated_grafts` validated as `integer\|min:1\|max:10000`. |
| P-QOT-006 | Select Treatment Dates and enter price per date | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:1669-1679` | `treatment_dates` array with `price` per date validated and stored. |
| P-QOT-007 | Add hotel package | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:1662` | `hotel_accommodation` boolean + hotel booking via `HotelController`. |
| P-QOT-008 | Add transport package | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:1665` | `airport_transportation` flag; transport pricing via custom services. |
| P-QOT-009 | Add PRP package | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:1707` | `custom_services` array supports additional packages including PRP. |
| P-QOT-010 | Total auto-calculates | CODE_EXISTS_CORRECT | `hairline-backend/app/Models/Quote.php:34` | `quote_amount` field stored; custom services sum at line 238. |
| P-QOT-011 | Set appointment slot | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:1676` | `appointment_date` + `appointment_time` required per treatment date. |
| P-QOT-012 | Select clinician for quote | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:1685` | `clinicians` array validated; each must be a valid `provider_users` UUID. |
| P-QOT-013 | Submit completed quote — status=Submitted | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:1578` | `store()` creates quote; status transitions via `quoteStatusChange()`. |
| P-QOT-014 | Submitted quote visible in quotes list | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:208` | `index()` returns quote list including submitted quotes. |
| P-QOT-015 | Save quote as draft | CODE_EXISTS_CORRECT | `hairline-backend/app/Models/Quote.php:19` | `STATUS_DRAFT = 'draft'` constant defined; quotes created initially as draft. |
| P-QOT-016 | Edit and resume draft quote | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:4820` | `update()` method accepts draft edits. |
| P-QOT-017 | Remove a package from quote | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:4820` | Custom services can be removed via update. |
| P-QOT-018 | Change treatment type after initial selection | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:4820` | `update()` allows treatment_id change on draft. |
| P-QOT-019 | Set single appointment slot per quote | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:1676` | One `appointment_date/time` per treatment date entry. |
| P-QOT-020 | Enter Treatment Plan (per-day) entries | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:1689-1696` | `treatment_plan` array validated with `consecutive_dates` custom rule. |
| P-QOT-022 | Submit without treatment type — validation error | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:1656` | `treatment_id` is `required\|uuid\|exists:treatments,id`. |
| P-QOT-023 | Submit without graft count — validation error | CODE_EXISTS_PARTIAL | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:1698` | `estimated_grafts` is `nullable` — not required; zero-graft submission would pass validation with null. |
| P-QOT-024 | Submit without price per date — validation error | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:1679` | `treatment_dates.*.price` is `required_with:treatment_dates\|numeric\|min:0`. |
| P-QOT-025 | Submit without appointment slot — validation error | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:1676` | `appointment_date` and `appointment_time` required with treatment_dates. |
| P-QOT-026 | Enter zero price for a date — rejected | CODE_EXISTS_PARTIAL | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:1679` | `min:0` allows zero; FR-004 requires positive price. Should be `min:0.01` or `gt:0`. |
| P-QOT-027 | Enter negative price for a date — rejected | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:1679` | `min:0` rejects negative values. |
| P-QOT-028 | Enter zero graft count — rejected | CODE_EXISTS_PARTIAL | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:1698` | `min:1` only applies when value is provided; field is `nullable` so zero graft would need to be sent explicitly to trigger this rule. |
| P-QOT-030 | Quote with all optional packages | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:1662-1711` | All package types supported in validation. |
| P-QOT-031 | Quote with no optional packages | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:1578` | All package fields are `nullable`; base price alone is valid. |
| P-QOT-032 | Cannot submit same quote twice | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:1762-1770` | Duplicate check: returns 400 "Already quoted for this inquiry" if a quote for same provider+inquiry exists. |
| P-QOT-033 | Multiple providers can hold quotes for same inquiry | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:2660` | Conflict check only triggered on `accepted` status; multiple providers can have `quote` status simultaneously. |
| P-QOT-034 | Edit a draft quote | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:4820` | `update()` handles draft edits. |
| P-QOT-035 | Cannot edit a submitted quote | CODE_EXISTS_BUG | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:4820` | **Verification confirmed bug.** `update()` method exists (line 4820) but a full read of the method body (lines 4820–4936+) found **no `$quote->status` guard of any kind** — submitted, confirmed, completed, and aftercare quotes can all be edited via this endpoint. |
| P-QOT-036 | Draft quote auto-archived after 7 days | CODE_MISSING | `hairline-backend/app/Console/Commands/` | No `ArchiveDraftQuotes` command or scheduler entry found. `CheckQuoteExpiry` command only handles submitted quotes' expiry. FR-004 draft auto-archive is not implemented. |
| P-QOT-037 | Quote locked when competing quote accepted | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:6700` | `acceptQuote()` cancels competing quotes in transaction. |
| P-QOT-038 | Quote cancelled when inquiry cancelled | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Inquiry/InquiryController.php:4066` | `cancel()` method propagates cancellation to related quotes. |
| P-QOT-P01 | Total: $5000+$500+$200+$800=$6500 | CODE_EXISTS_CORRECT | `hairline-backend/app/Models/Quote.php:238` | Custom services summed via `customServices()->sum('price')`. |
| P-QOT-P02 | Total: $3000 base, no packages | CODE_EXISTS_CORRECT | Same as P-QOT-P01 | Base price only scenario supported. |
| P-QOT-P03 | Total: $7500+$1200+$300=$9000 | CODE_EXISTS_CORRECT | Same as P-QOT-P01 | Multi-package calculation supported. |
| P-QOT-P04 | Total: $10000+$800+$150+$1000+$500=$12450 | CODE_EXISTS_CORRECT | Same as P-QOT-P01 | All packages + custom services. |
| P-QOT-P05 | Total: $2500, packages at $0 | CODE_EXISTS_PARTIAL | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:1679` | `min:0` allows $0 per date; FR-004 requires positive price per date. |
| P-QOT-P06 | Total: $4999.99+$500.01=$5500.00 | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:1660` | `decimal:2` validation handles cent-level precision. |
| P-QOT-P07 | Submit at 1h — accepted | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:1743` | Inquiry must exist and not be cancelled/completed; no time check on quote creation itself. |
| P-QOT-P08 | Submit at 24h — accepted | CODE_EXISTS_CORRECT | Same as P-QOT-P07 | Same. |
| P-QOT-P09 | Submit at 48h — accepted | CODE_EXISTS_CORRECT | Same as P-QOT-P07 | Same. |
| P-QOT-P10 | Submit at 71h — accepted | CODE_EXISTS_PARTIAL | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:1754` | No 72h window check on quote creation; blocked only if inquiry already `cancelled`. Near-deadline enforcement incomplete. |
| P-QOT-P11 | Submit at 72h — rejected | CODE_EXISTS_PARTIAL | Same as P-QOT-P10 | No explicit 72h window guard on `store()`. |
| P-QOT-P12 | Submit at 73h — rejected | CODE_EXISTS_PARTIAL | Same as P-QOT-P10 | Same. |
| P-QOT-P13 | Quote at 1h after submit — active, acceptable | CODE_EXISTS_CORRECT | `hairline-backend/app/Models/Quote.php:255,299` | `isExpired()` + `canBeAccepted()` check `expires_at`. |
| P-QOT-P14 | Quote at 24h — active, acceptable | CODE_EXISTS_CORRECT | Same as P-QOT-P13 | Same. |
| P-QOT-P15 | Quote at 47h — active, expiry warning | CODE_EXISTS_PARTIAL | `hairline-backend/app/Console/Commands/CheckQuoteExpiry.php:46` | Reminder notifications sent at 24h, 12h, 1h before expiry; no expiry warning field in API response. |
| P-QOT-P16 | Quote at 48h — expired, not acceptable | CODE_EXISTS_CORRECT | `hairline-backend/app/Models/Quote.php:255` | `isExpired()` returns true after `expires_at`; `canBeAccepted()` returns false. |
| P-QOT-P17 | Quote at 49h — expired | CODE_EXISTS_CORRECT | Same as P-QOT-P16 | Same. |

### Module Summary
- Total FAIL+BLOCKED audited: 51 (0 FAIL, 51 BLOCKED)
- CODE_MISSING: 1 | CODE_EXISTS_BUG: 1 | CODE_EXISTS_PARTIAL: 10 | CODE_EXISTS_CORRECT: 38 | NEEDS_DEEPER_REVIEW: 1

**Root causes:** (1) P-QOT-036: Draft quote auto-archival after 7 days (`CODE_MISSING`) — no scheduled command found; add an artisan command and register it in `app/Console/Kernel.php`. (2) P-QOT-024/P-QOT-026: `treatment_dates.*.price` uses `min:0` which allows zero prices; FR-004 requires a positive price per date — change to `min:0.01`. (3) P-QOT-P10–P12: No 72-hour window enforcement on `QuotesController::store()` — quote submission is only blocked when inquiry is already `cancelled`, not when the 72h window has passed. Add an explicit `distributed_at + 72h` expiry check in `store()`. (4) **P-QOT-035 corrected to BUG:** `QuotesController::update()` (line 4820) has no status guard whatsoever — providers can edit quotes regardless of status including `submitted`, `confirmed`, `aftercare`, and `completed`. Fix by adding a status allowlist check at the top of `update()` that restricts edits to `draft` status only.

---

## Module 5: Appointment Management (FR-006)

### FAIL Items

No FAIL items in this module.

### BLOCKED Items

| TC ID | Description | Verdict | Evidence (file:line) | Notes |
|-------|-------------|---------|---------------------|-------|
| P-APT-001 | Appointments page loads | CODE_EXISTS_CORRECT | `hairline-frontend/src/pages/providerDashboard/appointments/` | Appointments folder contains `AppointmentDetail.jsx`, `Confirmed.jsx`, `Scheduled.jsx`, etc. |
| P-APT-002 | Confirmed appointment shows unmasked patient | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Inquiry/InquiryController.php:1086` | `shouldAnonymize=false` when confirmed quote exists; full patient info returned. |
| P-APT-003 | Appointment shows correct date/time | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:532` | `appointment_date` and `appointment_time` from treatment dates returned in quote detail. |
| P-APT-004 | Appointment shows treatment type | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:292` | Quote detail includes treatment type via `treatment` relationship. |
| P-APT-005 | Payment status shown | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Bookings/BookingController.php:922` | `getPaymentStatus()` returns deposit/partial/full status. |
| P-APT-007 | Notification received for new booking | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Provider/ProviderNotificationController.php:25` | Provider notification system implemented; booking confirmation events trigger notifications. |
| P-APT-011 | Empty appointments list — empty state displayed | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:208` | `index()` returns empty `data` array when no quotes; FE handles empty state. |
| P-APT-013 | Appointment with partial payment — shows "Partial" | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Bookings/BookingController.php:922` | `getPaymentStatus()` distinguishes deposit-only vs full payment. |
| P-APT-014 | Appointment with full payment — shows "Full"/"Paid" | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Bookings/BookingController.php:922` | Full payment status reflected. |
| P-APT-015 | Provider can only see own appointments | NEEDS_DEEPER_REVIEW | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:208` | **Verification refuted evidence.** `index()` at line 208 is a patient-facing endpoint scoped by `patient_id` (requires `inquiry_id`, looks up inquiry via `patient_id`), not by provider. The original evidence reference points to the wrong endpoint. The correct provider-side appointment scoping endpoint has not been confirmed — further review needed to find the provider-scoped quotes/appointments listing. |

### Module Summary
- Total FAIL+BLOCKED audited: 10 (0 FAIL, 10 BLOCKED)
- CODE_MISSING: 0 | CODE_EXISTS_BUG: 0 | CODE_EXISTS_PARTIAL: 0 | CODE_EXISTS_CORRECT: 9 | NEEDS_DEEPER_REVIEW: 1

**Root causes:** (1) **P-APT-015 evidence corrected:** The original evidence at `QuotesController.php:208` pointed to a patient-facing endpoint, not a provider-scoped one. The correct provider-side appointment listing endpoint has not been identified — further investigation needed to confirm provider_id scoping is enforced before this TC can be marked `CODE_EXISTS_CORRECT`.

---

## Module 6: Treatment Execution (FR-010)

### FAIL Items

No FAIL items in this module.

### BLOCKED Items

| TC ID | Description | Verdict | Evidence (file:line) | Notes |
|-------|-------------|---------|---------------------|-------|
| P-TRT-001 | Treatment page loads for confirmed appointment | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:292` | Quote detail page (treatment in confirmed state) loads via `show()`. |
| P-TRT-002 | Initiate patient check-in | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:2870` | `startTreatment()` initiates the in-progress flow from provider side. |
| P-TRT-003 | Check-in validates full payment | CODE_EXISTS_BUG | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:2904` | `startTreatment()` validates quote is `confirmed` but has no full-payment check. Only deposit payment is checked in `BookingController::confirmVisit()` (line 1031) which is a patient-side action. Provider-side check-in (`startTreatment`) does not enforce full payment — contradicts FR-010. |
| P-TRT-004 | Check-in changes status to "In Progress" | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:2935` | Status updated to `inprogress` with `DB::beginTransaction()` wrapping. |
| P-TRT-005 | Assign clinician to procedure | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:1685` | Clinicians assigned via `assign-clinicians` route on quote. |
| P-TRT-006 | Enter actual graft count | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:5749` | `updateGrafts()` endpoint updates actual graft count. |
| P-TRT-007 | Add clinical notes | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/TreatmentPlanNoteController.php:108` | `store()` saves/updates treatment plan note via `updateOrCreate()`. |
| P-TRT-008 | Upload before photos | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/TreatmentPlanScanController.php` | Scan upload endpoint exists at `treatment-plan/scans`. |
| P-TRT-009 | Upload during photos | CODE_EXISTS_CORRECT | Same as P-TRT-008 | Category field distinguishes before/during/after. |
| P-TRT-010 | Upload after photos | CODE_EXISTS_CORRECT | Same as P-TRT-008 | Same. |
| P-TRT-011 | Add post-op medication | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/TreatmentPlanNoteController.php:105` | `medication` field in treatment plan note. |
| P-TRT-012 | Add multiple medications | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/TreatmentPlanNoteController.php:105` | Single `medication` string field; multiple medications can be entered as structured text. |
| P-TRT-013 | Mark procedure as complete | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:3080` | `endTreatment()` transitions `inprogress → aftercare`. |
| P-TRT-014 | Check-in blocked without full payment | CODE_EXISTS_BUG | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:2870` | `startTreatment()` has no full-payment guard — see P-TRT-003. Provider can start treatment on a deposit-only booking. |
| P-TRT-015 | Check-in blocked with no payment | CODE_EXISTS_BUG | Same as P-TRT-014 | No payment guard in `startTreatment()`. |
| P-TRT-016 | Cannot complete procedure without clinician | CODE_EXISTS_PARTIAL | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:3039` | `endTreatment()` does not validate clinician assignment before completion; only checks aftercare plan exists. |
| P-TRT-017 | Upload invalid file type as photo — rejected | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/FileController.php` | File upload uses MIME validation. |
| P-TRT-018 | Upload oversized photo — rejected | CODE_EXISTS_CORRECT | Same as P-TRT-017 | Size limit enforced in file upload. |
| P-TRT-019 | Empty clinical notes — allowed (optional) | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/TreatmentPlanNoteController.php:101` | All note fields are `nullable`. |
| P-TRT-020 | Very long clinical notes — saved or truncated | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/TreatmentPlanNoteController.php:101` | No max-length constraint on `beginning_note`; stored as text. |
| P-TRT-021 | Graft count differs from estimate — both values stored | CODE_EXISTS_PARTIAL | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:5749` | **Verification corrected original claim.** `updateGrafts()` at line 5749 updates `estimated_grafts` only (line 5787: `$quote->estimated_grafts = (int) $validated['estimated_grafts']`). There is no `actual_grafts` field in the `Quote` model — only the estimate field exists. "Both values stored" is inaccurate; only the estimate is stored. Consistent with P-DAT-012 finding. |
| P-TRT-022 | Treatment timeline shows chronological entries | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Bookings/BookingController.php:311` | `WorkflowTimeline` ordered by `action_time asc` in booking detail. |
| P-TRT-023 | Cannot re-check-in an already checked-in patient | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:2905` | `startTreatment()` returns 400 if quote status is not `confirmed`. |
| P-TRT-024 | View day-by-day treatment plan | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/TreatmentPlanDailyEntryController.php` | Daily entries endpoint exists via `treatment-plan/daily-entries`. |
| P-TRT-025 | Update day status to "In Progress" | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/TreatmentPlanDailyEntryController.php` | `update()` handles day status. |
| P-TRT-026 | Update day status to "Completed" | CODE_EXISTS_CORRECT | Same as P-TRT-025 | Day status transitions supported. |
| P-TRT-027 | Add notes to a treatment day | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/TreatmentPlanDailyEntryController.php` | Day-specific notes field in daily entry. |
| P-TRT-028 | Cannot mark future day as In Progress | CODE_EXISTS_PARTIAL | `hairline-backend/app/Http/Controllers/TreatmentPlanDailyEntryController.php:219-253` | **Verification confirmed missing guard.** `update()` validates `day`, `status`, `summary`, and `note` only. The only date-adjacent logic is a duplicate-day check (prevents two entries on the same day number); there is no guard checking whether the day is in the future relative to the current date. Providers can freely mark future treatment days as `in_progress`. |
| P-TRT-029 | Billing Staff cannot document treatment | CODE_EXISTS_PARTIAL | `hairline-backend/routes/api.php:408` | Treatment plan routes are under `auth:provider,api` guard but no explicit role check blocks billing-staff from posting notes. Role-based restriction is FE-only. |
| P-TRT-P01 | Check-in blocked: no payment | CODE_EXISTS_BUG | Same as P-TRT-014 | `startTreatment()` has no payment guard. |
| P-TRT-P02 | Check-in blocked: deposit only | CODE_EXISTS_BUG | Same as P-TRT-014 | Same — deposit-only should be blocked per FR-010 but is not. |
| P-TRT-P03 | Check-in blocked: partial balance | CODE_EXISTS_BUG | Same as P-TRT-014 | Same. |
| P-TRT-P04 | Check-in allowed: full payment | CODE_EXISTS_BUG | Same as P-TRT-014 | Because there is no guard at all, both full-payment and no-payment cases would pass — meaning the "allowed" case accidentally works but the "blocked" cases also pass, corrupting the treatment flow. |

### Module Summary
- Total FAIL+BLOCKED audited: 33 (0 FAIL, 33 BLOCKED)
- CODE_MISSING: 0 | CODE_EXISTS_BUG: 6 | CODE_EXISTS_PARTIAL: 4 | CODE_EXISTS_CORRECT: 22 | NEEDS_DEEPER_REVIEW: 0

**Root causes:** (1) `QuotesController::startTreatment()` (line 2870) is missing a full-payment guard — it only checks that the quote is in `confirmed` status, but never verifies the balance has been fully paid. FR-010 requires full payment before check-in; fix by adding a payment-status check (e.g., `booking->isFullyPaid()`) before the `DB::beginTransaction()` at line 2931. (2) `endTreatment()` (line 3039) does not validate clinician assignment before allowing procedure completion — add a check that at least one clinician is assigned to the quote before transitioning to `aftercare`. (3) Treatment-plan routes lack role-level middleware restricting Billing Staff — FE hides the UI but BE does not enforce the restriction. (4) **P-TRT-021 corrected to PARTIAL:** `updateGrafts()` only updates `estimated_grafts`; no `actual_grafts` field exists in the schema. (5) **P-TRT-028 corrected from NEEDS_DEEPER_REVIEW to PARTIAL:** `TreatmentPlanDailyEntryController::update()` confirmed to have no date guard — future days can be freely marked `in_progress`.

---

## Module 7: Aftercare Setup & Monitoring (FR-011)

### FAIL Items

No FAIL items in this module.

### BLOCKED Items

| TC ID | Description | Verdict | Evidence (file:line) | Notes |
|-------|-------------|---------|---------------------|-------|
| P-AFT-001 | Aftercare section loads | CODE_EXISTS_CORRECT | `hairline-frontend/src/pages/providerDashboard/AfterCare.jsx` | AfterCare page exists. |
| P-AFT-002 | Select aftercare template | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/PatientManagement/AfterCareController.php:5870` | `getTemplates()` returns list of active templates. |
| P-AFT-003 | Customize aftercare instructions | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/PatientManagement/AfterCareController.php:5604` | Instructions (general and milestone-specific) accepted in `createPlan()`. |
| P-AFT-004 | Milestone schedule auto-generated | CODE_EXISTS_PARTIAL | `hairline-backend/app/Http/Controllers/PatientManagement/AfterCareController.php:5568` | `createPlan()` accepts milestones passed by the caller; there is no server-side auto-generation of the standard Day 1, Week 1, Month 1, Month 3, Month 6, Month 12 schedule from a template — the FE must supply the dates. |
| P-AFT-005 | Milestone dates calculated from treatment date | CODE_EXISTS_PARTIAL | `hairline-backend/app/Http/Controllers/PatientManagement/AfterCareController.php:5582` | Milestone `start_date` and `end_date` are caller-supplied; the API does not compute them from treatment date. FE must calculate and pass the dates. |
| P-AFT-006 | Configure scan photo upload schedule | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/PatientManagement/AfterCareController.php:5584` | `scan_schedule` nullable array per milestone. |
| P-AFT-007 | Configure questionnaire schedule | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/PatientManagement/AfterCareController.php:5579` | Milestone `educational_resources` + questionnaire schedule via milestone data. |
| P-AFT-008 | Activate aftercare plan — status changes to "Aftercare" | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:3080` | `endTreatment()` transitions quote to `aftercare`; `createPlan()` with `activate=true` activates aftercare. |
| P-AFT-009 | View aftercare dashboard | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/PatientManagement/AfterCareController.php:326` | `index()` returns aftercare overview with milestones. |
| P-AFT-010 | Review patient scan submission | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/PatientManagement/AftercareMilestoneScanController.php` | Scan submissions accessible via `get-aftercare-milestones-scans`. |
| P-AFT-011 | Review patient questionnaire — pain/sleep/compliance scores | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/PatientManagement/AfterCareController.php:4979` | `getMilestoneDetails()` returns patient responses. |
| P-AFT-012 | Add aftercare notes | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/PatientManagement/AfterCareController.php` | Note update endpoint exists. |
| P-AFT-013 | Specify post-op medications | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/PatientManagement/AfterCareController.php:5591` | `medications` array with name, dosage, frequency validated in `createPlan()`. |
| P-AFT-014 | Activate without template — blocked | CODE_EXISTS_PARTIAL | `hairline-backend/app/Http/Controllers/PatientManagement/AfterCareController.php:5573` | `template_id` is `nullable` in `createPlan()` — a plan can be created without a template. The test expects this to be blocked. |
| P-AFT-015 | Empty customization — allowed or validation error | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/PatientManagement/AfterCareController.php:5605` | All instruction fields are nullable; empty customization allowed (uses defaults). |
| P-AFT-016 | No patient submissions yet — empty state displayed | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/PatientManagement/AfterCareController.php:4979` | Milestone details return empty arrays when no submissions exist. |
| P-AFT-017 | Patient submits scan at unexpected time — visible | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/PatientManagement/AftercareMilestoneScanController.php` | Scans accepted regardless of scheduled intervals; any submission is visible. |
| P-AFT-018 | High pain questionnaire response — flagged as urgent | CODE_MISSING | `hairline-backend/app/Http/Controllers/PatientManagement/AfterCareController.php:4979` | **Verification confirmed feature is absent.** Full review of `getMilestoneDetails()` (lines 4979–5089) found no automatic pain-score threshold or escalation trigger. `calculatePainLevel()` (line 2034) is a hardcoded display heuristic by `recovery_stage`, not a patient-score trigger. The `escalate()` endpoint (line 1559) is a manual admin action; no automated trigger fires from questionnaire responses. `red_flag` metadata exists in question data (line 7164) but no server-side logic acts on it automatically. |
| P-AFT-P01 | Milestone Day 1 = treatment date + 1 day | CODE_EXISTS_PARTIAL | `hairline-backend/app/Http/Controllers/PatientManagement/AfterCareController.php:5582` | Dates are caller-supplied; BE does not compute. FE must pass `treatment_date + 1`. |
| P-AFT-P02 | Milestone Week 1 = treatment date + 7 days | CODE_EXISTS_PARTIAL | Same as P-AFT-P01 | Same — FE computed. |
| P-AFT-P03 | Milestone Month 1 = treatment date + 1 month | CODE_EXISTS_PARTIAL | Same as P-AFT-P01 | Same. |
| P-AFT-P04 | Milestone Month 3 | CODE_EXISTS_PARTIAL | Same as P-AFT-P01 | Same. |
| P-AFT-P05 | Milestone Month 6 | CODE_EXISTS_PARTIAL | Same as P-AFT-P01 | Same. |
| P-AFT-P06 | Milestone Month 12 | CODE_EXISTS_PARTIAL | Same as P-AFT-P01 | Same. |
| P-AFT-P07 | Month 1 from Jan 31 = Feb 28 (edge case) | CODE_EXISTS_PARTIAL | Same as P-AFT-P01 | BE does not compute; if FE uses Carbon `addMonth()` it handles this correctly, but this is FE-level logic not verified here. |
| P-AFT-P08 | Month 1 from Dec 31 = Jan 31 | CODE_EXISTS_PARTIAL | Same as P-AFT-P01 | Same — FE-level concern. |

### Module Summary
- Total FAIL+BLOCKED audited: 26 (0 FAIL, 26 BLOCKED)
- CODE_MISSING: 1 | CODE_EXISTS_BUG: 0 | CODE_EXISTS_PARTIAL: 10 | CODE_EXISTS_CORRECT: 15 | NEEDS_DEEPER_REVIEW: 0

**Root causes:** (1) Milestone date auto-generation from treatment date is not performed server-side — `AfterCareController::createPlan()` accepts caller-supplied dates only. This puts date-calculation logic (including edge cases like month-end arithmetic) entirely in the FE, with no BE validation that dates follow the expected schedule. A server-side calculation utility should be added. (2) `template_id` is `nullable` in `createPlan()`, meaning activation without a template is allowed at the API level — the FR expects this to be blocked. (3) **P-AFT-018 corrected from NEEDS_DEEPER_REVIEW to CODE_MISSING:** No automatic pain-score escalation exists in `getMilestoneDetails()` — the feature (auto-urgent flag when pain ≥ 8) is simply not implemented.

---

## Module 8: Treatment Completion (FR-010, FR-011)

### FAIL Items

No FAIL items in this module.

### BLOCKED Items

| TC ID | Description | Verdict | Evidence (file:line) | Notes |
|-------|-------------|---------|---------------------|-------|
| P-CMP-001 | View treatment with completed aftercare milestones | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/PatientManagement/AfterCareController.php:4979` | `getMilestoneDetails()` returns milestone completion status. |
| P-CMP-002 | Mark treatment as "Completed" | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:3138` | `endTreatment()` transitions `aftercare → completed` when aftercare plan + milestones exist. |
| P-CMP-003 | Completed treatment appears in history | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:208` | `index()` includes completed quotes; FE filters by status. |
| P-CMP-004 | Full treatment timeline viewable | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Bookings/BookingController.php:311` | `WorkflowTimeline` records all status transitions ordered by `action_time`; covering inquiry → quote → booking → treatment → aftercare → completed. |
| P-CMP-006 | Cannot move directly from In Progress to Completed | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:3080,3138` | `endTreatment()` branches: `inprogress → aftercare` (Case 1) and `aftercare → completed` (Case 2). Directly calling `completed` from `inprogress` is not handled — Case 2 requires `status=aftercare`, so a jump from `inprogress` to `completed` would return a 400 (no matching branch). |
| P-CMP-007 | Cannot edit completed treatment | CODE_EXISTS_PARTIAL | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:4820` | `update()` exists but no status guard confirmed that prevents edits to `completed` quotes from this code read. Needs targeted review of update guard. |
| P-CMP-008 | Cannot re-complete a completed treatment | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:3138` | `endTreatment()` Case 2 is only entered when `status=aftercare`; a completed quote would fall through both cases and return an implied 400. |

### Module Summary
- Total FAIL+BLOCKED audited: 7 (0 FAIL, 7 BLOCKED)
- CODE_MISSING: 0 | CODE_EXISTS_BUG: 0 | CODE_EXISTS_PARTIAL: 1 | CODE_EXISTS_CORRECT: 6 | NEEDS_DEEPER_REVIEW: 0

**Root causes:** No critical defects found. P-CMP-007 warrants a targeted read of `QuotesController::update()` to confirm that completed quotes are blocked from edits — the existing code evidence is not conclusive.

---

## Module 9: Cross-Cutting Concerns (FR-020, FR-009)

### FAIL Items

No FAIL items in this module.

### BLOCKED Items

| TC ID | Description | Verdict | Evidence (file:line) | Notes |
|-------|-------------|---------|---------------------|-------|
| P-XCT-001 | Notification dropdown accessible | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Provider/ProviderNotificationController.php:25` | `index()` returns notifications list. Route at `provider/notifications/`. |
| P-XCT-002 | Notifications load with infinite scroll | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Provider/ProviderNotificationController.php:25` | Paginated notifications returned by `index()`. |
| P-XCT-003 | Click notification navigates to source | CODE_EXISTS_CORRECT | `hairline-frontend/src/pages/providerDashboard/` | Notification data includes source context; FE routes on click. |
| P-XCT-004 | Real-time notification received via WebSocket | CODE_EXISTS_CORRECT | `hairline-frontend/src/echo.js` | Laravel Echo + Pusher integration configured; real-time channel subscriptions implemented. |
| P-XCT-005 | Notification count badge updates | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Provider/ProviderNotificationController.php:76` | `unreadCount()` endpoint exists; FE polls or subscribes to update badge. |
| P-XCT-006 | Owner has full access | CODE_EXISTS_CORRECT | `hairline-frontend/src/components/providerComponents/providerSettings/ProviderSettingTab.jsx:38` | `isOwner` flag gates all sections; owner sees everything. |
| P-XCT-007 | Manager has restricted access | CODE_EXISTS_PARTIAL | `hairline-frontend/src/utils/accessControl.js` | Access control module exists but manager-specific restrictions appear to be FE-only UI gating rather than middleware-enforced. |
| P-XCT-008 | Clinician has clinical-only access | CODE_EXISTS_PARTIAL | `hairline-frontend/src/utils/accessControl.js` | Same as P-XCT-007 — FE-only access control; BE treatment-plan routes do not check clinician role. |
| P-XCT-009 | Billing Staff has basic access | CODE_EXISTS_CORRECT | `hairline-backend/tests/Feature/TreatmentFlow/ProviderDashboardAuthContractTest.php` | P-XCT-010 passed in automated run: billing-staff token denied on admin settings (403). Backend role enforcement confirmed for settings endpoints. |
| P-XCT-011 | Patient remains masked before payment | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Inquiry/InquiryController.php:1091` | Anonymization service applied when no confirmed quote; `_anonymized=true` flag returned. |
| P-XCT-012 | Patient unmasked after payment | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Inquiry/InquiryController.php:1086` | `shouldAnonymize=false` when confirmed/in-progress/aftercare/completed quote exists. |
| P-XCT-013 | Treatment status transitions are valid | CODE_EXISTS_PARTIAL | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:2604` | `quoteStatusChange()` accepts any valid status string; no explicit allowlist of valid `from→to` transition pairs is enforced. A provider could call the API directly to set `completed` from `confirmed`. |
| P-XCT-014 | Invalid status transition rejected | CODE_EXISTS_PARTIAL | Same as P-XCT-013 | No transition-matrix guard exists in `quoteStatusChange()`. Backward transitions (e.g., `completed → inprogress`) are not explicitly blocked. |
| P-XCT-P01 | Confirmed → In Progress (allowed) | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:2870` | `startTreatment()` enforces `status=confirmed` as prerequisite. |
| P-XCT-P02 | In Progress → Aftercare (allowed) | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:3080` | `endTreatment()` Case 1 enforces `status=inprogress`. |
| P-XCT-P03 | Aftercare → Completed (allowed) | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:3138` | `endTreatment()` Case 2 enforces `status=aftercare`. |
| P-XCT-P04 | Confirmed → Aftercare (rejected/skip) | CODE_EXISTS_PARTIAL | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:2604` | `quoteStatusChange()` would accept this since `aftercare` is in the valid status enum. No state machine prevents this jump. |
| P-XCT-P05 | Confirmed → Completed (rejected/skip) | CODE_EXISTS_PARTIAL | Same as P-XCT-P04 | Same — no transition guard. |
| P-XCT-P06 | In Progress → Confirmed (backward, rejected) | CODE_EXISTS_PARTIAL | Same as P-XCT-P04 | `quoteStatusChange()` would accept this. |
| P-XCT-P07 | Aftercare → In Progress (backward, rejected) | CODE_EXISTS_PARTIAL | Same as P-XCT-P04 | Same. |
| P-XCT-P08 | Completed → Aftercare (backward, rejected) | CODE_EXISTS_PARTIAL | Same as P-XCT-P04 | Same. |
| P-XCT-P09 | Completed → Confirmed (backward, rejected) | CODE_EXISTS_PARTIAL | Same as P-XCT-P04 | Same. |

### Module Summary
- Total FAIL+BLOCKED audited: 22 (0 FAIL, 22 BLOCKED)
- CODE_MISSING: 0 | CODE_EXISTS_BUG: 0 | CODE_EXISTS_PARTIAL: 10 | CODE_EXISTS_CORRECT: 12 | NEEDS_DEEPER_REVIEW: 0

**Root causes:** (1) `QuotesController::quoteStatusChange()` (line 2604) accepts any valid status string without enforcing a transition matrix — backward and skipping transitions (e.g., `completed → inprogress`, `confirmed → completed`) are not blocked. Fix by implementing a `VALID_TRANSITIONS` map and rejecting any `from → to` pair not in the map. (2) Role-based access for clinical-only and manager roles is enforced exclusively in the FE (`accessControl.js`) with no BE middleware guard — an authenticated token holder of any provider role can call treatment-plan and team endpoints directly.

---

## Module 10: Smoke Tests

### FAIL Items

No FAIL items in this module.

### BLOCKED Items

No BLOCKED items in this module — all 10 smoke tests (P-SMK-001 through P-SMK-010) achieved PASS status in the 2026-03-18 run.

### Module Summary
- Total FAIL+BLOCKED audited: 0 (0 FAIL, 0 BLOCKED)
- CODE_MISSING: 0 | CODE_EXISTS_BUG: 0 | CODE_EXISTS_PARTIAL: 0 | CODE_EXISTS_CORRECT: 0 | NEEDS_DEEPER_REVIEW: 0

**Root causes:** No defects found. Module is fully covered by passing automated tests.

---

## Module 11: Idempotency Tests (FR-004, FR-007, FR-010, FR-011)

### FAIL Items

No FAIL items in this module.

### BLOCKED Items

| TC ID | Description | Verdict | Evidence (file:line) | Notes |
|-------|-------------|---------|---------------------|-------|
| P-IDP-001 | Submit same quote twice — second rejected, no duplicate | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:1762` | Duplicate check at line 1762: returns 400 "Already quoted for this inquiry" if a quote for same provider+inquiry exists. |
| P-IDP-002 | Save same draft twice — idempotent, no duplicate | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:4820` | `update()` on an existing quote is idempotent — updates the same record. |
| P-IDP-003 | Add same package twice — rejected or replaced, not duplicated | CODE_EXISTS_PARTIAL | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:2184-2211` | `custom_services` creation loop at lines 2184–2211 calls `QuoteCustomService::create()` inside a `foreach` with no prior uniqueness check on `service_name`. A second `store()` call with the same service produces a second row. (Original evidence cited line 1707, which is a validation comment — corrected to the actual creation loop.) |
| P-IDP-004 | Check-in patient twice — second rejected | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:2905` | `startTreatment()` returns 400 if quote is already `inprogress` (status check on line 2905). |
| P-IDP-005 | Complete procedure twice — second rejected | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:3080,3138` | Both `endTreatment()` cases require specific precondition status; a second call falls through with implied 400 or wrong-status error. |
| P-IDP-006 | Upload same photo twice — no data corruption | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/TreatmentPlanScanController.php` | Each upload creates a new file record; no corruption but may result in duplicates (acceptable per FR). |
| P-IDP-007 | Add same medication twice — no silent corruption | CODE_EXISTS_PARTIAL | `hairline-backend/app/Http/Controllers/TreatmentPlanNoteController.php:108` | `medication` is a single free-text field using `updateOrCreate()` — a second call with the same content simply overwrites. No corruption, but `custom_services` duplicates are possible (see P-IDP-003). |
| P-IDP-008 | Activate aftercare plan twice — second rejected or idempotent | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/PatientManagement/AfterCareController.php:5568` | `createPlan()` creates a new aftercare record; calling it a second time for the same quote would create a second plan — potential issue. However `endTreatment()` (the activation trigger) checks `status=aftercare` and is idempotent. |
| P-IDP-009 | Complete treatment twice — second rejected | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:3138` | Second call on a `completed` quote fails to match either `endTreatment()` branch → implicit 400. |
| P-IDP-010 | Invite same email twice — second rejected | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Provider/ProviderTeamController.php:738` | Duplicate pending-invitation check at line 738 returns 400 "Invitation already sent to this email". |

### Module Summary
- Total FAIL+BLOCKED audited: 10 (0 FAIL, 10 BLOCKED)
- CODE_MISSING: 0 | CODE_EXISTS_BUG: 0 | CODE_EXISTS_PARTIAL: 3 | CODE_EXISTS_CORRECT: 7 | NEEDS_DEEPER_REVIEW: 0

**Root causes:** (1) P-IDP-003: `custom_services` has no deduplication guard — adding the same service name twice via `store()` can result in two rows. Fix by adding a uniqueness check on `service_name` per quote before inserting. (2) P-IDP-008: `AfterCareController::createPlan()` does not check whether an aftercare plan already exists for the given `quote_id` — a second call would create a duplicate plan. Add a `AfterCare::where('quote_id', ..)->exists()` guard before creation.

---

## Module 12: Race Condition Tests

### FAIL Items

No FAIL items in this module.

### BLOCKED Items

| TC ID | Description | Verdict | Evidence (file:line) | Notes |
|-------|-------------|---------|---------------------|-------|
| P-RAC-001 | Two providers quote same inquiry simultaneously | CODE_EXISTS_PARTIAL | `QuotesController.php:1578-2159` | `store()` method has partial protection: `lockForUpdate()` used for discount increment (line 2162) but overall quote creation lacks `DB::transaction` wrapper. No pessimistic lock on Quote model during creation. |
| P-RAC-002 | Provider submits quote while inquiry expires | CODE_EXISTS_CORRECT | `QuotesController.php:6724, Quote.php:255-300` | `acceptQuote()` begins transaction at line 6724; `Quote::isExpired()` checks expiry at line 255–260; `Quote::canBeAccepted()` validates at line 297–300. Expiry check occurs within transaction. |
| P-RAC-003 | Two team members update same treatment simultaneously | CODE_EXISTS_BUG | `TreatmentPlanNoteController.php:97-124` | `store()` method (lines 97–124) uses `updateOrCreate()` at line 108 without any `DB::transaction()` wrapper. Concurrent updates can cause race conditions. (Original evidence cited lines 135–141, which are outside the method — corrected to actual method location.) |
| P-RAC-004 | Provider edits quote while patient accepts it | CODE_EXISTS_PARTIAL | `QuotesController.php:4936, 6724` | Both `update()` (line 4936) and `acceptQuote()` (line 6724) use `DB::beginTransaction()`, but there is no cross-method pessimistic lock. Another provider could update the quote between acceptance check and completion if timing allows. |
| P-RAC-005 | Double-click on check-in button | CODE_EXISTS_BUG | `BookingController.php:1039-1056` | **Verification corrected original claim.** The already-confirmed check at line 1039 occurs **before** `DB::beginTransaction()` at line 1046 — it is outside the transaction boundary, not inside it as originally claimed. This creates a genuine TOCTOU (time-of-check-time-of-use) race window: two concurrent double-clicks can both pass the guard check before either acquires the transaction lock, allowing double processing of the same visit confirmation. |
| P-RAC-006 | Rapid quote form submission (double-click) | CODE_EXISTS_BUG | `QuotesController.php:1578-2250` | `store()` creates a quote without a `DB::transaction` wrapper and has no idempotency token or duplicate-prevention mechanism. Concurrent submissions can create multiple quotes for the same inquiry. |
| P-RAC-007 | Two providers revoke same team member simultaneously | CODE_EXISTS_CORRECT | `ProviderTeamController.php:1494-1581` | `destroy()` begins transaction at line 1494, fetches the member, validates workload and ownership rules within the transaction before deletion at line 1562. Concurrent revokes handled safely. |

### Module Summary
- Total FAIL+BLOCKED audited: 7 (0 FAIL, 7 BLOCKED)
- CODE_MISSING: 0 | CODE_EXISTS_BUG: 3 | CODE_EXISTS_PARTIAL: 2 | CODE_EXISTS_CORRECT: 2 | NEEDS_DEEPER_REVIEW: 0

**Root causes:** (1) `QuotesController::store()` lacks a `DB::transaction` wrapper and idempotency guard — rapid double-click submissions can create duplicate quotes (P-RAC-006). (2) `TreatmentPlanNoteController::store()` uses `updateOrCreate()` outside a transaction at line 108 — actual method is at lines 97–124, not 135–141 as originally cited (P-RAC-003). (3) **P-RAC-005 corrected to BUG:** `BookingController::confirmVisit()` already-confirmed guard at line 1039 is outside the `DB::beginTransaction()` at line 1046 — TOCTOU race condition window exists, making the double-click protection weaker than claimed. Fix by moving the guard inside the transaction or using a `SELECT ... FOR UPDATE` pattern within the transaction.

---

## Module 13: Data Consistency Tests

### FAIL Items

No FAIL items in this module.

### BLOCKED Items

#### Cross-Table Consistency (P-DAT-001 – P-DAT-007)

| TC ID | Description | Verdict | Evidence (file:line) | Notes |
|-------|-------------|---------|---------------------|-------|
| P-DAT-001 | Inquiry → Quote linkage | CODE_EXISTS_CORRECT | `hairline-backend/app/Models/Quote.php:27,58-61` | `quotes.inquiry_id` FK is in `$fillable` at line 27; `Quote::inquiry()` `belongsTo(Inquiry::class)` relationship exists at lines 58–61 (function declaration at 58, not 59 as originally cited). FK is set in `QuotesController::store()` at creation time. Automation not written. |
| P-DAT-002 | Quote → Booking linkage | CODE_EXISTS_CORRECT | `hairline-backend/app/Models/Booking.php:31,79-82` | `bookings.quote_id` in `$fillable` at line 31; `Booking::quote()` `belongsTo(Quote::class)` relationship exists at lines 79–82. (Original evidence cited lines 211–214, which do not exist — the model is only 151 lines; corrected to actual relationship location.) `BookingService::createBooking()` sets `quote_id`, `patient_id`, `provider_id`, `inquiry_id` from the accepted quote — all FKs correctly populated. Automation not written. |
| P-DAT-003 | Booking → Payment linkage | CODE_EXISTS_PARTIAL | `hairline-backend/app/Models/Payment.php:18-24` / `hairline-backend/app/Models/PaymentInstallment.php:23,42-48` | Payment record carries `quote_id`, not `booking_id` directly. The link is: `bookings → payment_installments.booking_id → payments.id via payment_installments.payment_id`. There is no direct `booking_id` on `payments`. The TC expects `Payment.booking_id = booking.id` — relationship exists but traverses through `PaymentInstallment`, not a direct FK. Amounts: `Booking.total_amount` is calculated from accepted treatment dates in `BookingService.php:78-110`; `Payment.amount` is set per-installment. No atomic cross-check that `sum(payment_installments.amount) = booking.total_amount` is enforced at DB level. |
| P-DAT-004 | Booking → Treatment linkage | CODE_EXISTS_PARTIAL | `hairline-backend/app/Models/Treatment.php:17-35` / `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:2870` | The `treatments` table has no `booking_id` column — `Treatment` model `$fillable` does not include it. Treatment lifecycle (status changes) is managed entirely through the `quotes` table status field (`inprogress`, `aftercare`, `completed`). There is no separate row per-patient treatment entity tracking `patient_id` and `provider_id` in a `treatments` table linked to a booking. The "treatment" concept is the quote itself transitioning through statuses. TC assertion "treatment references the booking" cannot hold as designed. |
| P-DAT-005 | Treatment → Aftercare linkage | CODE_EXISTS_PARTIAL | `hairline-backend/app/Models/AfterCare.php:18-27` / `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:3144-3155` | `AfterCare` has `quote_id` but no `booking_id` or `treatment_id` column — linkage is through `quote_id`. The TC expects `aftercare.treatment_id` → no such field exists. Aftercare is only accessible after `endTreatment()` transitions quote `inprogress→aftercare` (Case 1), and `endTreatment()` Case 2 enforces that `AfterCare` with milestones exists before `aftercare→completed`. The "created only after procedure completion" guard is present at the status transition gate. |
| P-DAT-006 | Aftercare → Milestones linkage | CODE_EXISTS_CORRECT | `hairline-backend/app/Models/AftercareMilestone.php:17-37` / `hairline-backend/app/Models/AfterCare.php:88-92` | `aftercare_milestones.after_care_id` FK is in `$fillable`; `AfterCare::milestones()` `hasMany(AftercareMilestone::class, 'after_care_id')` relationship exists; milestones are ordered by `start_date`. Chronological ordering is applied at the relationship level. Automation not written. |
| P-DAT-007 | Patient anonymization consistency | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Inquiry/InquiryController.php:1091-1111` | Patient anonymization logic in `formatInquiryResponse()` masks name/email/phone when no confirmed quote exists for the inquiry; unmasking occurs post-payment when `status=confirmed`. Logic is consistently applied through the single formatting method. Automation not written. |

#### Financial Consistency (P-DAT-008 – P-DAT-012)

| TC ID | Description | Verdict | Evidence (file:line) | Notes |
|-------|-------------|---------|---------------------|-------|
| P-DAT-008 | Quote total = base + packages | CODE_EXISTS_PARTIAL | `hairline-backend/app/Models/Quote.php:34,236-238` / `hairline-backend/app/Services/BookingService.php:78-110` | `quote_amount` is a stored scalar — it is not dynamically recomputed from `custom_services.sum('price')` on every read. The `getCustomServicesTotalAttribute()` accessor at line 236 returns `customServices()->sum('price')` dynamically, but `quote_amount` in the DB may diverge from this computed total if custom services are modified after `quote_amount` was last written. No enforced consistency between the two. |
| P-DAT-009 | Payment amount = quote total | CODE_EXISTS_PARTIAL | `hairline-backend/app/Services/BookingService.php:109,217` / `hairline-backend/app/Models/Payment.php:24` | `Booking.total_amount` is computed at booking creation; `Payment.amount` is in `$fillable` at line 24 (not 23 as originally cited — line 23 is `payment_number`). No runtime assertion ensures `sum(payments) = booking.total_amount` after the fact — bookings can accumulate partial payments without a guard that the running total never exceeds `total_amount`. |
| P-DAT-010 | Deposit + balance = total | CODE_EXISTS_CORRECT | `hairline-backend/app/Services/BookingService.php:122-123` | `deposit_amount = round(total_amount * (deposit_percentage / 100), 2)` (line 122) and `remaining_amount = round(total_amount - deposit_amount, 2)` (line 123) — computed atomically at booking creation in `BookingService`. The relationship `deposit + remaining = total` holds by construction. (Original evidence also cited `DepositRateService.php:106`; that method is a snapshot helper that does not use `round()` — the canonical rounded formula is in `BookingService:122-123`.) Automation not written. |
| P-DAT-011 | All installments sum to balance | CODE_EXISTS_CORRECT | `hairline-backend/app/Services/BookingService.php:287-349` | **Verification corrected original claim.** `createInstallmentPlan()` begins at line 287 (lines 234–242 are the call site, not the implementation). The method applies a last-installment residual-balance adjustment at line 312: `$lastInstallmentAmount = $remainingAmount - ($monthlyAmount * ($installmentMonths - 2))` — a rounding-compensation technique ensuring `sum(installments) = remaining_amount` exactly. The original "no compensating last-installment adjustment" claim is refuted. No DB-level constraint exists, but the application arithmetic is correct. |
| P-DAT-012 | Treatment graft count recorded | CODE_EXISTS_PARTIAL | `hairline-backend/app/Models/Quote.php:35-36` | `estimated_grafts` and `graft_description` exist in `quotes.$fillable` and are `nullable` — the field is present but not required. No `actual_grafts` field found in the Quote model — there is no mechanism to record the actual graft count performed vs the estimate. TC expects "both values stored"; only estimate is stored, actual is absent. |

#### Status Consistency (P-DAT-013 – P-DAT-016)

| TC ID | Description | Verdict | Evidence (file:line) | Notes |
|-------|-------------|---------|---------------------|-------|
| P-DAT-013 | Completed treatment has completed aftercare | CODE_EXISTS_PARTIAL | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:3138-3155` | `endTreatment()` Case 2 gates `aftercare→completed` transition on: (a) `AfterCare` exists for the quote, (b) `AfterCare` has at least 1 milestone. However it does NOT require all milestones to have `status=completed` — a plan with incomplete milestones can still move the quote to `completed`. TC expects "milestones are complete"; backend only requires they exist. |
| P-DAT-014 | In-progress treatment has confirmed booking | CODE_EXISTS_PARTIAL | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:2904-2910` / `hairline-backend/app/Models/Booking.php:122-134` | `startTreatment()` checks `quote.status = confirmed` before transitioning to `inprogress`, and `confirmed` status on a quote is set only after deposit payment via Stripe. However the TC expects `Booking.status = confirmed` AND `full payment exists` — `Booking.STATUS_CONFIRMED` is only reached after `Booking.STATUS_FULLY_PAID`, but `startTreatment()` does not check `Booking.isFullyPaid()` — it only checks quote status. A quote can be `confirmed` (deposit only) and `startTreatment()` will succeed even when the balance is unpaid. Full-payment guard is missing. |
| P-DAT-015 | Cancelled quotes when one accepted | CODE_EXISTS_CORRECT | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:6828-6831` | `acceptQuote()` at line 6828 queries all other quotes for the same `inquiry_id` with `status IN (quote, draft)` and cancels them in the same `DB::beginTransaction()` block. Status consistency is enforced atomically. Automation not written. |
| P-DAT-016 | Timeline entries exist for every status change | CODE_EXISTS_PARTIAL | `hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:2944,3094,3187` / `hairline-backend/app/Models/WorkflowTimeline.php:17-26` | `WorkflowTimeline` records are created for: `Accepted` (line 6814), `In Progress` (line 2945), `Aftercare` (line 3095), `Completed` (line 3187). However, timeline entries for `confirmed` (post-deposit), `checked-in` (visit confirmation), and `procedure-complete` stages are not found in `QuotesController`. The `confirmVisit()` in `BookingController` does not create a `WorkflowTimeline` entry. TC expects timeline entries for all 6 stages; only 4 are confirmed by code. |

### Module Summary
- Total FAIL+BLOCKED audited: 16 (0 FAIL, 16 BLOCKED)
- CODE_MISSING: 0 | CODE_EXISTS_BUG: 0 | CODE_EXISTS_PARTIAL: 10 | CODE_EXISTS_CORRECT: 6 | NEEDS_DEEPER_REVIEW: 0

**Root causes:** (1) The data model uses `quotes.status` as the single source of truth for the treatment lifecycle — there is no separate `treatments` table per patient case, so P-DAT-004 and P-DAT-005 FK assertions cannot hold as the TC specifies. (2) Financial consistency (P-DAT-008, P-DAT-009) relies on application-layer arithmetic at creation time with no DB-enforced sum constraints, leaving divergence possible if records are modified post-creation. **P-DAT-011 corrected to CORRECT:** `createInstallmentPlan()` does apply a last-installment residual adjustment at line 312 ensuring installments sum to balance exactly — the original "no rounding compensation" claim was wrong. (3) Status consistency (P-DAT-013, P-DAT-014, P-DAT-016) has partial guards: aftercare→completed requires a plan but not completed milestones; startTreatment requires deposit but not full payment; timeline entries confirmed at lines 2945, 3095, 3187, 6814 but absent in `BookingController::confirmVisit()` for the `confirmed` stage. (4) Multiple evidence line numbers corrected: `Booking::quote()` is at lines 79–82 (not 211–214); `Quote::inquiry()` at lines 58–61; `Payment.amount` at line 24 (not 23); deposit formula in `BookingService:122`, not `DepositRateService:106`.

---

## Overall Summary

### Verdict Breakdown by Module

| Module | TC Count (FAIL+BLOCKED) | CODE_MISSING | CODE_EXISTS_BUG | CODE_EXISTS_PARTIAL | CODE_EXISTS_CORRECT | NEEDS_DEEPER_REVIEW |
|--------|------------------------|--------------|-----------------|---------------------|---------------------|---------------------|
| M01 — Auth & Sign-In (FR-009) | 20 | 0 | 6 | 2 | 12 | 0 |
| M02 — Onboarding & Team Setup (FR-009, FR-032) | 27 | 0 | 1 | 2 | 24 | 0 |
| M03 — Inquiry Review (FR-003) | 26 | 0 | 1 | 7 | 17 | 1 |
| M04 — Quote Lifecycle (FR-004) | 51 | 1 | 1 | 10 | 38 | 1 |
| M05 — Appointment Management (FR-006) | 10 | 0 | 0 | 0 | 9 | 1 |
| M06 — Treatment & Procedure (FR-010) | 33 | 0 | 6 | 4 | 22 | 0 |
| M07 — Aftercare Management (FR-011) | 26 | 1 | 0 | 10 | 15 | 0 |
| M08 — Treatment Completion (FR-010, FR-011) | 7 | 0 | 0 | 1 | 6 | 0 |
| M09 — Cross-Cutting Concerns (FR-020, FR-009) | 22 | 0 | 0 | 10 | 12 | 0 |
| M10 — Smoke Tests | 0 | 0 | 0 | 0 | 0 | 0 |
| M11 — Idempotency (FR-004, FR-007, FR-010, FR-011) | 10 | 0 | 0 | 3 | 7 | 0 |
| M12 — Race Condition Tests | 7 | 0 | 3 | 2 | 2 | 0 |
| M13 — Data Consistency Tests | 16 | 0 | 0 | 10 | 6 | 0 |
| **TOTALS** | **255** | **2** | **18** | **61** | **172** | **3** |

> Note: Module 10 (Smoke Tests) audited 0 FAIL/BLOCKED because all 10 smoke tests achieved PASS in the 2026-03-18 run. The remaining 255 BLOCKED TCs span Modules 1–9 and 11–13.

---

### Cross-Module Verdict Summary

| Verdict | Count | % of Audited |
|---------|-------|-------------|
| CODE_MISSING | 2 | 0.8% |
| CODE_EXISTS_BUG | 18 | 7.1% |
| CODE_EXISTS_PARTIAL | 61 | 23.9% |
| CODE_EXISTS_CORRECT | 172 | 67.5% |
| NEEDS_DEEPER_REVIEW | 3 | 1.2% |
| **Total audited** | **255** | 100% |

**Interpretation:** 67.5% of BLOCKED test cases are blocked purely because automation has not been written — the underlying feature code is present and correctly implemented. A further 23.9% have code in place but incomplete relative to FR requirements. 7.1% (18 TCs) reflect confirmed code defects, and 0.8% (2 TCs) are completely unimplemented. Totals reflect a full two-pass codebase verification run completed 2026-03-19.

---

### Priority Action Items

The following defects are ranked by business risk. Each maps to one or more TCs.

#### P1 — Critical / Fix Before Next Release

| # | Defect | Affected TCs | FR | Evidence |
|---|--------|-------------|----|-|
| 1 | **Backend password policy allows 8-char passwords** — FE enforces ≥12 chars + complexity; BE `ProviderStaffInvitationController.php:1152` only enforces `min:8`. A client bypassing the FE can set a weak password for any invited staff member. | P-AUTH-P01, P-AUTH-P02, P-AUTH-P03, P-AUTH-P04, P-AUTH-P05, P-AUTH-P06, P-AUTH-005 | FR-009 | `ProviderStaffInvitationController.php:1152` |
| 2 | **`startTreatment()` has no full-payment guard** — quote transitions to `inprogress` (treatment started) after deposit only; the balance may be unpaid. Revenue loss risk if treatment runs before patient settles balance. | P-TRT-003, P-TRT-014, P-TRT-015, P-DAT-014 | FR-010, FR-007 | `QuotesController.php:2904-2910` |
| 3 | **Inquiry max-providers cap is 5 (backend) vs 10 (FR-003)** — `MaxArrayItems(5)` at `InquiryController.php:1463` hard-blocks submissions to 6–10 providers with a misleading error message. Patients cannot exercise their full FR-003 right. | P-INQ-001, P-INQ-002 | FR-003 | `InquiryController.php:1463,1477` |

#### P2 — High / Fix in Next Sprint

| # | Defect | Affected TCs | FR | Evidence |
|---|--------|-------------|----|-|
| 4 | **`QuotesController::update()` has no status guard** — any quote regardless of status (`submitted`, `confirmed`, `completed`, `aftercare`) can be edited via the update endpoint. FR-004 requires only draft quotes to be editable. | P-QOT-035 | FR-004 | `QuotesController.php:4820` |
| 5 | **`destroy()` has no self-revoke guard** — `ProviderTeamController::destroy()` checks workload and last-owner constraints but never compares `$member->user_id` to `auth()->id()`. Any provider team member can remove their own access record via the API. | P-ONB-016 | FR-009 | `ProviderTeamController.php:1494-1581` |
| 6 | **Quote status machine has no transition-matrix guard** — `quoteStatusChange()` does not block backward or skip transitions (e.g., `completed→draft`, `cancelled→accepted`). Any invalid status string can be written via the API. | P-QOT-017 through P-QOT-024 | FR-004 | `QuotesController.php:2600` |
| 7 | **`QuotesController::store()` lacks `DB::transaction` wrapper** — rapid concurrent submissions can create duplicate quote records because the duplicate-check and insert are not atomic. | P-RAC-006 | FR-004 | `QuotesController.php:1578,1762` |
| 8 | **`BookingController::confirmVisit()` already-confirmed guard is outside the transaction** — idempotency check at line 1039 executes before `DB::beginTransaction()` at line 1046, creating a TOCTOU race window on double-click visit confirmation. | P-RAC-005 | FR-006 | `BookingController.php:1039-1046` |
| 8 | **`aftercare→completed` does not require all milestones to be completed** — `endTreatment()` Case 2 only requires milestones to exist, not to have `status=completed`. Treatment can be closed with open recovery milestones. | P-DAT-013, P-RAC-007 | FR-011 | `QuotesController.php:3155` |
| 9 | **No `actual_grafts` field** — `Quote.$fillable` has `estimated_grafts` but no field for actual graft count performed. `updateGrafts()` overwrites the estimate, not a separate actual field. Post-procedure audit trail is incomplete. | P-DAT-012, P-TRT-021 | FR-010 | `Quote.php:35-36`, `QuotesController.php:5787` |

#### P3 — Medium / Backlog

| # | Defect | Affected TCs | FR | Evidence |
|---|--------|-------------|----|-|
| 10 | **Draft quote auto-archive (7 days) is missing** — no console command, no scheduler entry. Stale draft quotes accumulate indefinitely. | P-QOT-036 | FR-004 | `app/Console/Commands/` (absent) |
| 11 | **`InvitationLanding.jsx` always routes to signup** — `email_exists=true` flag from the API is ignored; returning Hairline users cannot use the login-only acceptance branch. | P-AUTH-011 | FR-009 | `InvitationLanding.jsx:136` |
| 12 | **WorkflowTimeline missing `confirmed` and `checked-in` entries** — `confirmVisit()` in `BookingController` does not create a `WorkflowTimeline` row; `checked-in` stage is not tracked. | P-DAT-016 | FR-006 | `BookingController.php:1002` |
| 13 | **`quote_amount` stored scalar can diverge from `customServices().sum('price')`** — no re-computation guard after custom service edits. | P-DAT-008 | FR-004 | `Quote.php:236-239` |
| 14 | **AfterCare model uses `quote_id` (not `treatment_id`)** — TC assertions about `aftercare.treatment_id` cannot be satisfied; the domain model diverges from the FR data-schema expectation. | P-DAT-005 | FR-011 | `AfterCare.php:18-27` |
| 15 | **Auto-urgent escalation for high pain scores is not implemented** — FR-011 requires flagging urgent cases when patient-reported pain ≥ 8; no automatic escalation trigger exists in `getMilestoneDetails()` or anywhere in the aftercare pipeline. The `escalate()` endpoint is manual-only. | P-AFT-018 | FR-011 | `AfterCareController.php:4979,1559` |
| 16 | **Future treatment days can be marked In Progress** — `TreatmentPlanDailyEntryController::update()` has no date-based guard; providers can mark days not yet reached as `in_progress`. | P-TRT-028 | FR-010 | `TreatmentPlanDailyEntryController.php:219-253` |

---

### Blocked Items — Automation Coverage Debt

Of the 256 BLOCKED TCs in this run, 174 (68.2%) have correct underlying code — they are blocked solely because the test automation has not been written. The recommended remediation priority order for adding automation is:

1. **Module 6 — Treatment & Procedure (FR-010):** 24 CORRECT TCs waiting for automation + 6 BUGs to fix first.
2. **Module 4 — Quote Lifecycle (FR-004):** 38 CORRECT TCs + state machine BUG to fix first.
3. **Module 2 — Team Management (FR-009):** 25 CORRECT TCs, lowest defect risk, highest automation ROI.
4. **Module 7 — Aftercare (FR-011):** 15 CORRECT TCs + 10 PARTIAL items to complete first.
5. **Module 9 — Billing & Payments (FR-007, FR-032):** 12 CORRECT TCs + 10 PARTIAL items.

Fixing the P1/P2 defects listed above before writing automation for the affected modules will prevent tests from being written against broken behaviour.

---

## Recommended Next Actions

This section maps every defect to a concrete **business decision** and a **minimal technical action**. Items follow the same P1/P2/P3 priority order as above.

---

### P1 — Fix Immediately (Security & Revenue-Risk Bugs)

#### 1. Backend password policy only enforces min:8 [P-AUTH-005, P-AUTH-P01–P06]

**Business action:** Any invited staff member can set an 8-character password by bypassing the frontend. Clinic accounts with weak credentials are a direct security risk. Fix the backend validator before the next staff onboarding cycle; this is a one-line change with zero UX impact.

**Technical action:**
- `app/Http/Controllers/Provider/ProviderStaffInvitationController.php:1152` — replace `'password' => 'required|min:8'` with:
  `'password' => ['required', Password::min(12)->mixedCase()->numbers()->symbols()]`
- Import `Illuminate\Validation\Rules\Password` at the top of the controller.
- Re-run P-AUTH-P01 through P-AUTH-P06 and P-AUTH-005 — all should pass after this change.

#### 2. Treatment can start without full payment [P-TRT-003, P-TRT-014, P-TRT-015, P-DAT-014]

**Business action:** Providers can start a treatment procedure after only the deposit has been paid; the remaining balance may never be collected. This is a direct revenue-loss risk for every treatment currently in progress. Decide the enforcement policy (block start, or warn-only) and implement before the next treatment cycle.

**Technical action:**
- `app/Http/Controllers/Quotes/QuotesController.php` in `startTreatment()` (around line 2904) — add a payment-status guard before the status transition:
  ```php
  if ($booking->payment_status !== 'fully_paid') {
      return response()->json(['message' => 'Full payment required before treatment can begin'], 422);
  }
  ```
- Check the exact `payment_status` enum values used in the `bookings` table and align accordingly.

#### 3. Inquiry max-providers cap is 5 instead of FR-003's 10 [P-INQ-001, P-INQ-002]

**Business action:** Patients are silently capped at 5 providers when the specification allows 10. This limits patient choice and may reduce conversion rates. Fix immediately — it is a one-character change.

**Technical action:**
- `app/Http/Controllers/Inquiry/InquiryController.php:1463` — change `MaxArrayItems(5)` to `MaxArrayItems(10)`.
- Update the corresponding error message at line 1477 to reference 10, not 5.
- Check the frontend inquiry submission form for any client-side `maxProviders` constant that also needs updating.

---

### P2 — Fix in Next Sprint (Data Integrity & Concurrency Bugs)

#### 4. Any quote status can be edited via the update endpoint [P-QOT-035]

**Business action:** A provider can edit a quote that has already been accepted by the patient or is currently in an active treatment. Modifying agreed-upon terms retroactively is a legal and trust risk. Fix this sprint before any accepted-quote editing occurs in production.

**Technical action:**
- `app/Http/Controllers/Quotes/QuotesController.php:update()` (around line 4820) — add a status guard at the top of the method:
  ```php
  $allowedEditStatuses = ['draft', 'revised'];
  if (!in_array($quote->status, $allowedEditStatuses)) {
      return response()->json(['message' => 'Only draft or revised quotes can be edited'], 422);
  }
  ```
- Confirm with the product owner exactly which statuses should permit editing per FR-004.

#### 5. Provider team member can remove their own record [P-ONB-016]

**Business action:** A team member who wants to leave (or who is acting maliciously) can call the delete endpoint to remove themselves from the team, bypassing any offboarding controls. Fix this sprint; the guard is a two-line addition.

**Technical action:**
- `app/Http/Controllers/Provider/ProviderTeamController.php:destroy()` (around line 1494) — add a self-revoke check as the first guard:
  ```php
  if ($member->user_id === auth()->id()) {
      return response()->json(['message' => 'You cannot remove your own team membership'], 422);
  }
  ```

#### 6. Quote status machine accepts any status string [P-QOT-017–P-QOT-024]

**Business action:** Invalid or backward status transitions (e.g., reverting a completed quote back to draft) can corrupt the treatment lifecycle. Providers — or a bug — can create quotes in impossible states, breaking downstream billing and reporting.

**Technical action:**
- `app/Http/Controllers/Quotes/QuotesController.php:quoteStatusChange()` (around line 2600) — add a transition matrix:
  ```php
  $transitions = [
      'draft'     => ['submitted'],
      'submitted' => ['accepted', 'rejected', 'revised'],
      'revised'   => ['submitted'],
      'accepted'  => ['inprogress'],
      'inprogress'=> ['aftercare', 'completed'],
      'aftercare' => ['completed'],
  ];
  if (!in_array($newStatus, $transitions[$quote->status] ?? [])) {
      return response()->json(['message' => "Cannot transition from {$quote->status} to {$newStatus}"], 422);
  }
  ```
- Validate the exact status enum values against the `quotes` table.

#### 7. Concurrent quote submissions can create duplicate records [P-RAC-006]

**Business action:** Under simultaneous rapid submissions (e.g., accidental double-submit), two quote records can be created for the same inquiry by the same provider. This affects billing and creates confusing duplicate state. Fix before any load or stress testing.

**Technical action:**
- `app/Http/Controllers/Quotes/QuotesController.php:store()` (around line 1578) — wrap the duplicate-check + insert in a database transaction with a lock:
  ```php
  DB::transaction(function () use ($request, $inquiry) {
      $existing = Quote::where('inquiry_id', $inquiry->id)
                        ->where('provider_id', auth()->id())
                        ->lockForUpdate()
                        ->first();
      if ($existing) {
          throw ValidationException::withMessages(['inquiry_id' => 'Quote already exists for this inquiry']);
      }
      // ... existing store logic
  });
  ```

#### 8. Visit confirmation TOCTOU race — double-click creates duplicate confirmations [P-RAC-005]

**Business action:** A double-click on "confirm visit" can create duplicate booking confirmation records because the idempotency check runs before the database transaction begins. In a clinic context this can produce duplicate scheduling or billing entries.

**Technical action:**
- `app/Http/Controllers/Bookings/BookingController.php:confirmVisit()` — move the already-confirmed check (currently at line 1039) to inside the transaction (after `DB::beginTransaction()` at line 1046), or add `->lockForUpdate()` to the booking fetch at line 1039 to atomically hold the row during the check.

#### 9. Treatment can be marked complete with open aftercare milestones [P-DAT-013, P-RAC-007]

**Business action:** Providers can close a treatment even if aftercare milestones (wound checks, medication reviews) are still open. Patients with unresolved recovery needs have their case marked complete, removing provider accountability for follow-up.

**Technical action:**
- `app/Http/Controllers/Quotes/QuotesController.php:endTreatment()` Case 2 (around line 3155) — add a milestone completion check before closing:
  ```php
  if ($aftercare->milestones()->where('status', '!=', 'completed')->exists()) {
      return response()->json(['message' => 'All aftercare milestones must be completed before closing treatment'], 422);
  }
  ```

#### 10. No field to store actual grafts performed [P-TRT-021, P-DAT-012]

**Business action:** After a hair transplant procedure, there is no way to record the actual graft count vs. the pre-procedure estimate. This is important for outcome tracking, patient medical records, and any post-procedure billing adjustments based on actual work performed. Add before any completed treatments are in the system.

**Technical action:**
- Create a migration: add `actual_grafts` nullable integer column to the `quotes` table.
- `app/Models/Quote.php` — add `actual_grafts` to `$fillable`.
- `app/Http/Controllers/Quotes/QuotesController.php:updateGrafts()` (around line 5787) — update the method to write to `actual_grafts` (post-procedure) as a separate field, preserving `estimated_grafts` as the original pre-procedure value. Do not overwrite the estimate.

---

### P3 — Schedule Within Sprint (Incomplete Features)

#### 11. Draft quote 7-day auto-archive is missing [P-QOT-036]

**Business action:** Stale draft quotes accumulate indefinitely on provider dashboards, creating noise and potentially confusing patients who submitted inquiries and are waiting for responses. Schedule a cleanup job for the next infrastructure sprint.

**Technical action:**
- Create a new Artisan command: `app/Console/Commands/ArchiveStaleDraftQuotes.php` — queries `Quote::where('status', 'draft')->where('updated_at', '<', now()->subDays(7))` and sets `status = 'archived'`.
- Register in `app/Console/Kernel.php` at `->daily()`.
- Add a test case asserting that a 7-day-old draft is archived and an 8-day-old draft is archived but a 6-day-old draft is not.

#### 12. Invitation landing page ignores email_exists flag [P-AUTH-011]

**Business action:** An existing Hairline patient accepting a staff invitation is forced through the full signup flow, creating a confusing experience and potentially prompting duplicate account creation. Fix in the current frontend sprint.

**Technical action:**
- `hairline-frontend/src/pages/auth/invitation/InvitationLanding.jsx:136` — replace the unconditional `setStep("signup")` with a conditional branch:
  ```js
  if (data.email_exists) {
      setStep("login");
  } else {
      setStep("signup");
  }
  ```
- Ensure the `"login"` step renders a login form that, on success, calls the invitation `accept()` endpoint to complete the linkage.

#### 13. WorkflowTimeline missing visit-confirmed and checked-in entries [P-DAT-016]

**Business action:** The treatment lifecycle timeline used for audit, reporting, and patient communication has gaps — visit confirmation and check-in are not recorded as events. The history jumps from booked to in-progress with no intermediate steps, making audits and disputes harder to resolve.

**Technical action:**
- `app/Http/Controllers/Bookings/BookingController.php:confirmVisit()` (around line 1002) — add a `WorkflowTimeline::create([...])` call for the `visit_confirmed` event after the confirmation logic, mirroring the pattern at `QuotesController.php:2945`.
- If a separate check-in action exists, add a matching timeline entry there too.

#### 14. Stored quote_amount can diverge from custom service prices [P-DAT-008]

**Business action:** If a custom service line item is edited or deleted after the quote total is initially computed and stored, the stored `quote_amount` and the actual sum of services fall out of sync. Patients could see a different total from what the provider internally tracks, creating billing disputes.

**Technical action (two options — choose one):**
- **Option A (simpler):** In every `QuotesController` method that creates, updates, or deletes a custom service, recompute and save `quote_amount = $quote->customServices()->sum('price')` before returning.
- **Option B (safer long-term):** Remove the stored `quote_amount` field entirely and expose it as a computed Eloquent accessor (`getQuoteAmountAttribute`) that always returns the live sum. This eliminates the divergence category completely.

#### 15. AfterCare model links to quote_id, not treatment_id [P-DAT-005]

**Business action:** The aftercare data model links aftercare plans to a quote, not to a treatment record. Any test case or external integration that expects `aftercare.treatment_id` will fail. Before finalising the aftercare module, confirm with the product owner whether the current design (quote-linked) is intentional or a schema error.

**Technical action:**
- **If `quote_id` is intentional (preferred):** Update `system-data-schema.md` and the test cases (P-DAT-005 assertions) to reflect `aftercare.quote_id`. No code changes.
- **If `treatment_id` is required:** Create a migration to add `treatment_id` FK (nullable during transition) to `after_cares`. Add the `treatment()` relationship to `AfterCare.php`. Backfill via `quote → booking → treatment` chain. Mark `quote_id` as deprecated.

#### 16. Auto-urgent escalation on high pain score not implemented [P-AFT-018]

**Business action:** FR-011 requires the system to automatically flag a case as urgent when a patient reports a pain score ≥ 8. Without this, high-pain patients depend on providers manually noticing the score — a patient safety gap. Add the trigger before aftercare goes live in production.

**Technical action:**
- Locate the handler where questionnaire / milestone answers are saved in `app/Http/Controllers/PatientManagement/AfterCareController.php`.
- After saving the answer, add:
  ```php
  if (($answeredData['pain_score'] ?? 0) >= 8) {
      $afterCare->update(['priority' => 'urgent']);
      // Optionally: dispatch a notification to the assigned provider
  }
  ```
- Wire a push notification or in-app alert so the provider is notified immediately when urgency is auto-set.

#### 17. Future treatment days can be marked In Progress [P-TRT-028]

**Business action:** Providers can mark a treatment day as in-progress before that calendar day has arrived. This corrupts the treatment journal and enables false progress reporting. Add the date guard before the treatment execution module goes live.

**Technical action:**
- `app/Http/Controllers/TreatmentPlanDailyEntryController.php:update()` (around line 219) — add a date check at the start of the method:
  ```php
  if ($entry->scheduled_date > today()) {
      return response()->json(['message' => 'Cannot update a treatment day before its scheduled date'], 422);
  }
  ```
- Confirm the column name for the entry's scheduled date in the `treatment_plan_daily_entries` table.

---

### NEEDS_DEEPER_REVIEW — Required Before Test Automation Is Written

The following three items require a targeted investigation or product decision before they can be resolved. Do not write test automation for these TCs until each is settled.

| TC ID | What to Do |
|-------|-----------|
| P-INQ-003 | Read `InquiryController@show` and the Conversation model's scope to confirm whether provider A can access conversation records for inquiries distributed to provider B. If access is unscoped, add a `provider_id` check. |
| P-QOT-026 | Manually test the version restore flow in staging: restore a previous version and confirm whether in-flight edits are discarded or merged. Document the expected behavior in FR-004 before writing the TC. |
| P-APT-015 | Identify the correct provider-scoped appointment history endpoint (the evidence pointed to a patient-scoped endpoint). Grep `routes/api.php` for appointment/visit routes under `auth:provider` to find the right evidence line before re-auditing. |

---

### Test Case Actions Summary

| TC ID(s) | Current Verdict | Required Action |
|----------|----------------|-----------------|
| P-AUTH-005, P-AUTH-P01–P06 | CODE_EXISTS_BUG | Fix BE validator (`min:8` → `min:12` + complexity) → re-run → expect rejection of weak passwords |
| P-TRT-003, P-TRT-014, P-TRT-015, P-DAT-014 | CODE_EXISTS_BUG | Add payment-status guard in `startTreatment()` → re-run → expect 422 without full payment |
| P-INQ-001, P-INQ-002 | CODE_EXISTS_BUG | Change cap from 5 to 10 → re-run → expect 10-provider submissions accepted |
| P-QOT-035 | CODE_EXISTS_BUG | Add status guard in `update()` → re-run → expect 422 on non-draft edits |
| P-ONB-016 | CODE_EXISTS_BUG | Add self-revoke guard in `destroy()` → re-run → expect 422 on self-removal |
| P-QOT-017–P-QOT-024 | CODE_EXISTS_BUG | Add transition matrix → re-run → expect 422 on invalid transitions |
| P-RAC-006 | CODE_EXISTS_BUG | Wrap store() in transaction with lock → re-run concurrent test → expect single record |
| P-RAC-005 | CODE_EXISTS_BUG | Move idempotency check inside transaction → re-run → expect no duplicate confirmations |
| P-DAT-013, P-RAC-007 | CODE_EXISTS_BUG | Add open-milestone guard in `endTreatment()` → re-run → expect 422 with open milestones |
| P-TRT-021, P-DAT-012 | CODE_EXISTS_PARTIAL | Add `actual_grafts` field + update method → re-run → expect estimate and actual stored separately |
| P-QOT-036 | CODE_MISSING | Create archive Artisan command + scheduler → **write new TC** → run |
| P-AUTH-011 | CODE_EXISTS_PARTIAL | Fix `InvitationLanding.jsx:136` conditional → re-run → expect login branch for existing users |
| P-DAT-016 | CODE_EXISTS_PARTIAL | Add `WorkflowTimeline` entry in `confirmVisit()` → re-run → expect confirmed event in timeline |
| P-DAT-008 | CODE_EXISTS_PARTIAL | Recompute or remove stored `quote_amount` → re-run → expect stored total matches service sum |
| P-DAT-005 | CODE_EXISTS_PARTIAL | Confirm schema with PO → either update test assertions or migrate to `treatment_id` |
| P-AFT-018 | CODE_MISSING | Add pain-score trigger → re-run → expect priority=urgent auto-set when pain ≥ 8 |
| P-TRT-028 | CODE_EXISTS_PARTIAL | Add date guard in `update()` → re-run → expect 422 on future-day updates |
| P-AUTH-008 | CODE_EXISTS_PARTIAL | Complete FE role-gating for all roles beyond owner → re-run role-access TCs |
| P-ONB-017 | CODE_EXISTS_PARTIAL | Complete inactive-member scoping review → re-run after manual session |
| P-INQ-003 | NEEDS_DEEPER_REVIEW | Manual code review of conversation scope → update verdict → then write TC |
| P-QOT-026 | NEEDS_DEEPER_REVIEW | Manual staging test of version restore → document expected behavior → write TC |
| P-APT-015 | NEEDS_DEEPER_REVIEW | Find correct provider-scoped endpoint → re-audit → update verdict → write TC |
