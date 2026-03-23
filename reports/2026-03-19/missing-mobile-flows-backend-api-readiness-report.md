# Missing Mobile Flows Backend API Readiness Report

**Report Date**: 2026-03-19  
**Scope**: Patient mobile flows from `local-docs/reports/2026-02-05/missing-mobile-flows-design-complement.md` audited against `main/hairline-backend/`  
**Audit Type**: Backend endpoint readiness and gap analysis  
**Method**: Source-flow review, route/controller/doc inspection, and concurrent sub-agent audits by flow group

## Executive Summary

- Audited all 15 missing mobile flows defined in the design complement report.
- Deployed 4 concurrent sub-agents to audit flow groups in parallel: Auth/Profile, Quote Management, Booking/Travel, and Aftercare/Notifications/Support.
- Result: `0 Ready`, `13 Partial`, `2 Missing`.
- Highest-risk gaps:
  - No patient saved-payment-method management API for `P03.1`.
  - No patient-owned review management API for `P05.3`.
  - Patient notification inbox APIs are missing; only device-token registration exists for `P06.1`.
  - Patient help-center access is incomplete because many help-content routes are not exposed on patient middleware for `P08.1`.

## Status Dashboard

| Flow | Module | Overall Status | Key Verdict |
| --- | --- | --- | --- |
| P01.1 Delete Account | P-01 | Partial | Core delete-request endpoint exists, but reason capture, patient status/history, and delete-flow OTP support are incomplete |
| P01.2 Settings Screen | P-01 | Partial | Preferences/device-token APIs exist, but patient legal-content APIs and MVP notification-toggle contract are incomplete |
| P01.3 Change Password | P-01 | Partial | Change-password and reset endpoints exist, but token revocation, generic errors, reuse-history, and throttling are incomplete |
| P02.1 Compare Offers Side-by-Side | P-02 | Partial | Quote list/detail/compare/accept endpoints exist, but expiry exposure and manual compare validation are incomplete |
| P02.2 Cancel Inquiry | P-02 | Partial | Cancel endpoint exists, but allowed-stage behavior, structured reasons, privacy handling, and slot-release evidence are incomplete |
| P02.3 Expired Offers/Quotes | P-02 | Partial | Expiry prevention exists, but expired state data is not consistently exposed to patient list APIs |
| P02.4 Legal/Policy Screens | P-02 | Partial | Quote detail returns inline legal copy, but there is no patient FR-027 legal-document API with version metadata |
| P03.1 Payment Methods Management | P-03 | Missing | No patient saved-payment-method CRUD/default-management API was found |
| P04.1 Passport Submission | P-04 | Partial | Passport submit/read APIs exist, but record locking, booking/path scoping, masking, and validation are incomplete |
| P04.2 Flight & Hotel Submission | P-04 | Partial | Travel read/write APIs exist, but no `no_travel_required`, no per-leg flight model, and no record locking |
| P05.1 Day-to-Day Treatment Progress | P-05 | Partial | Patient quote/aftercare detail APIs expose related data, but no dedicated treatment-progress/completed-summary API exists |
| P05.2 Previous Treatments List | P-05 | Partial | Patient inquiry/quote APIs can support fragments, but no aggregate “My Treatments” API exists |
| P05.3 Submitted Reviews List | P-05 | Missing | Only review creation exists; no patient “my reviews” list/detail/edit/takedown APIs were found |
| P06.1 Notification Listing & Bubble | P-06 | Partial | Push-token infrastructure exists, but patient inbox/unread/read APIs are missing |
| P08.1 Help & Support | P-08 | Partial | Patient articles and support email endpoint exist, but patient ticket lifecycle APIs and patient access to most help content are incomplete |

## Detailed Findings

### P01.1 Delete Account

**Expected backend capabilities**: active-care/payment blocking, optional reason, password or OTP re-auth, deletion request creation, open-inquiry auto-close, and patient status updates.

| Endpoint | Controller | Status | Notes |
| --- | --- | --- | --- |
| `POST /api/patient/account/delete-request` | `Patients\PatientAccountController@requestAccountDeletion` | Partial | Creates a deletion request, validates password-or-OTP re-auth, and uses `PatientAccountDeletionService` for blocking checks and inquiry auto-close. Missing optional reason capture, patient status/history retrieval, patient confirmation email/status-update flow, and dedicated delete-flow OTP send/resend support. |
| `POST /api/auth/forgot-password` | `Authentication\AuthController@forgotPassword` | Partial | Generic password-reset OTP entry point only; not modeled as delete-flow verification. |
| `POST /api/auth/verify-otp` | `Authentication\AuthController@verifyOtp` | Partial | Generic OTP verification exists, but not delete-flow-specific and has request-contract inconsistency with docs. |
| `POST /api/auth/resend-password-reset-otp` | `Authentication\AuthController@resendPasswordResetOtp` | Partial | Generic reset resend endpoint only; no dedicated delete-flow resend endpoint found. |

**Evidence**:
- Route: `main/hairline-backend/routes/api.php:1453`
- Controller: `main/hairline-backend/app/Http/Controllers/Patients/PatientAccountController.php:87`
- Blocking/inquiry auto-close service: `main/hairline-backend/app/Services/PatientAccountDeletionService.php:21`

### P01.2 Settings Screen

**Expected backend capabilities**: patient preferences, MVP global Email/Push toggles, patient legal content (privacy/terms), and support entry points.

| Endpoint | Controller | Status | Notes |
| --- | --- | --- | --- |
| `GET /api/settings/patient/preferences` | `Settings\PatientSettingsController@getPreferences` | Partial | Patient settings read endpoint exists, but it does not expose the required MVP global Email/Push toggle contract. |
| `POST /api/settings/patient/preferences` | `Settings\PatientSettingsController@updatePreferences` | Partial | Update endpoint exists, but it updates granular settings/privacy values instead of the design’s global Email/Push toggles. |
| `GET /api/settings/patient/help` | `Settings\PatientSettingsController@getHelpContent` | Partial | Returns static help links only; not the full P08 support capability set. |
| `GET /api/settings/patient/about` | `Settings\PatientSettingsController@getAboutInfo` | Partial | Returns static URLs for privacy/terms, not the legal-document content/version metadata required by the flow. |
| `POST /api/notifications/device-tokens` | `Notifications\DeviceTokenController@register` | Partial | Supports push-delivery registration only. |
| `GET /api/notifications/device-tokens` | `Notifications\DeviceTokenController@index` | Partial | Lists device tokens, not notification preferences or inbox items. |
| `DELETE /api/notifications/device-tokens` | `Notifications\DeviceTokenController@unregister` | Partial | Supports device-token removal only. |
| Patient privacy-policy endpoint | — | Missing | No patient-facing FR-027 privacy document API was found. Existing legal routes are under non-patient middleware. |
| Patient terms-and-conditions endpoint | — | Missing | No patient-facing FR-027 terms document API was found. Existing routes are under non-patient middleware. |

**Evidence**:
- Patient settings routes: `main/hairline-backend/routes/api.php:1373`
- Patient settings controller: `main/hairline-backend/app/Http/Controllers/Settings/PatientSettingsController.php:20`
- Legal routes under non-patient middleware: `main/hairline-backend/routes/api.php:892`

### P01.3 Change Password

**Expected backend capabilities**: in-session password change, generic failure messages, password history checks, throttling/lockout, current-session preservation, and prior-refresh-token revocation.

| Endpoint | Controller | Status | Notes |
| --- | --- | --- | --- |
| `POST /api/auth/change-password` | `Authentication\AuthController@changePassword` | Partial | Supports authenticated password change and strong-password validation, but no evidence of last-5-password reuse checks, prior-refresh-token revocation, or throttle/lockout middleware. Error message is overly specific (`Old Password is incorrect!`). |
| `POST /api/auth/forgot-password` | `Authentication\AuthController@forgotPassword` | Ready | Basic forgot-password entry point exists. |
| `POST /api/auth/verify-otp` | `Authentication\AuthController@verifyOtp` | Partial | Endpoint exists, but docs/controller field naming is inconsistent (`otp` vs `code`). |
| `POST /api/auth/reset-password` | `Authentication\AuthController@resetPassword` | Ready | Password-reset completion endpoint exists. |
| `POST /api/auth/resend-password-reset-otp` | `Authentication\AuthController@resendPasswordResetOtp` | Ready | Reset resend endpoint exists with cooldown logic in service layer. |

**Evidence**:
- Route: `main/hairline-backend/routes/api.php:84`
- Controller: `main/hairline-backend/app/Http/Controllers/Authentication/AuthController.php:805`
- Password reset service: `main/hairline-backend/app/Services/PasswordResetService.php:23`

### P02.1 Compare Offers Side-by-Side

**Expected backend capabilities**: inquiry dashboard, quote list, compare up to 3 eligible quotes, quote detail, accept one quote, and exclude expired/withdrawn quotes from compare/accept.

| Endpoint | Controller | Status | Notes |
| --- | --- | --- | --- |
| `GET /api/inquiry/get-patient-single-inquiry` | `Inquiry\InquiryController@patientSingleInquiry` | Partial | Supports inquiry-detail context, but not sufficient by itself for compare rules. |
| `GET /api/inquiry/get-all-offers` | `Inquiry\InquiryController@getAllOffersByInquiry` | Partial | Returns offer data, but does not verify inquiry ownership and does not expose `expires_at`/`is_expired` fields needed to disable expired offers in the main dashboard. |
| `GET /api/quote/get-patient-single-quote` | `Quotes\QuotesController@singleQuote` | Ready | Quote detail endpoint exists and supports quote-detail view. |
| `GET /api/quote/compare-quotes` | `Quotes\QuotesController@compareQuotes` | Partial | Supports compare up to 3 quotes and excludes expired quotes in auto mode, but manual `quote_ids[]` mode does not explicitly reject expired quotes. |
| `POST /api/quote/accept-quote` | `Quotes\QuotesController@acceptQuote` | Ready | Accept flow exists and includes auto-cancel of competing quotes. |

**Evidence**:
- Routes: `main/hairline-backend/routes/api.php:1301`, `main/hairline-backend/routes/api.php:1311`
- Compare logic: `main/hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:8536`
- Accept logic: `main/hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:6700`

### P02.2 Cancel Inquiry

**Expected backend capabilities**: cancellation in Inquiry/Quoted/Accepted stages, required reason selection, inquiry cancel cascade, quote cancel cascade, provider notifications without exposing patient reason, and accepted-slot release.

| Endpoint | Controller | Status | Notes |
| --- | --- | --- | --- |
| `POST /api/inquiry/cancel` | `Inquiry\InquiryController@cancel` | Partial | Patient cancellation endpoint exists and cancels related quotes, but current cancellability rules block active-quote cases the design expects to allow, request shape is free-text not structured reasons, provider notification includes patient reason, and no slot-release evidence was found. |

**Evidence**:
- Route: `main/hairline-backend/routes/api.php:1301`
- Controller: `main/hairline-backend/app/Http/Controllers/Inquiry/InquiryController.php:4066`
- Cancellability model: `main/hairline-backend/app/Models/Inquiry.php:230`

### P02.3 Expired Offers/Quotes

**Expected backend capabilities**: quote expiry detection, patient notifications, disabled acceptance, expired state in list/detail/compare, and “all quotes expired” support.

| Endpoint | Controller | Status | Notes |
| --- | --- | --- | --- |
| `GET /api/inquiry/get-all-offers` | `Inquiry\InquiryController@getAllOffersByInquiry` | Partial | Main offer-list endpoint does not expose expiry fields needed to render expired cards or derive an all-expired state. |
| `GET /api/quote/get-patient-single-quote` | `Quotes\QuotesController@singleQuote` | Partial | Quote detail exposes `status`, `expires_at`, and `days_until_expiry`, which is enough for detail-view expiry handling. |
| `GET /api/quote/compare-quotes` | `Quotes\QuotesController@compareQuotes` | Partial | Auto mode excludes expired quotes; manual mode does not fully guard against expired IDs. |
| `POST /api/quote/accept-quote` | `Quotes\QuotesController@acceptQuote` | Ready | Explicitly rejects expired quotes. |

**Supporting backend process**:
- `quotes:check-expiry` (`CheckQuoteExpiry`) exists and sends expiry reminders/expired notifications, but evidence does not show quote status being updated to `expired`.

**Evidence**:
- Expiry command: `main/hairline-backend/app/Console/Commands/CheckQuoteExpiry.php:32`
- Quote model helpers: `main/hairline-backend/app/Models/Quote.php:244`

### P02.4 Legal/Policy Screens (Quote Context)

**Expected backend capabilities**: patient can open current legal documents by type with published-version metadata.

| Endpoint | Controller | Status | Notes |
| --- | --- | --- | --- |
| `GET /api/quote/get-patient-single-quote` | `Quotes\QuotesController@singleQuote` | Partial | Returns inline `cancellation_policy`, `privacy_commitment`, and `terms_of_service` strings, but not FR-027-backed document metadata, locale fallback, or version details. |
| Patient legal-document API by type | — | Missing | No patient-facing FR-027 document endpoint was found. Existing legal routes are under non-patient middleware and `cancellation_policy` is not a defined `LegalDocument` type. |

**Evidence**:
- Quote detail legal fields: `main/hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:4733`
- Legal routes under non-patient middleware: `main/hairline-backend/routes/api.php:913`

### P03.1 Payment Methods Management

**Expected backend capabilities**: saved payment-method list/add/edit/remove, tokenization metadata, default method, remove-block rules for active payment obligations, and installment/default-method handling.

| Endpoint | Controller | Status | Notes |
| --- | --- | --- | --- |
| `POST /api/booking/create-payment-intent` | `Bookings\BookingController@createPaymentIntent` | Partial | Supports payment collection during booking, not saved payment-method management. |
| `POST /api/booking/pay-deposit` | `Bookings\BookingController@payDeposit` | Partial | Supports deposit payment, not payment-method CRUD/default management. |
| `GET /api/booking/{id}/payment-status` | `Bookings\BookingController@getPaymentStatus` | Partial | Supports booking payment status only. |
| Saved payment-method CRUD/default endpoints | — | Missing | No patient-facing routes, controller, or model for tokenized saved payment methods were found. |

**Evidence**:
- Booking payment routes: `main/hairline-backend/routes/api.php:1332`
- Installment model stores payment execution data, not saved methods: `main/hairline-backend/app/Models/PaymentInstallment.php:22`

### P04.1 Passport Submission (Path A)

**Expected backend capabilities**: patient submits passport data and image for a booking/path, data becomes locked/read-only after submit, patient sees masked confirmation view, and correction flows through admin.

| Endpoint | Controller | Status | Notes |
| --- | --- | --- | --- |
| `POST /api/passport-details/store` | `Essentials\PassportDetailsController@store` | Partial | Passport submit endpoint exists, but it uses `updateOrCreate` by `patient_id`, so records remain rewritable instead of locked. Validation does not enforce all required image/expiry constraints. |
| `GET /api/passport-details/get-passport-details` | `Essentials\PassportDetailsController@getPassportDetails` | Partial | Read endpoint exists, but returns raw passport number/image URL instead of masked/no-photo confirmation shape. |
| `GET /api/quote/confirmed-detail` | `Quotes\QuotesController@confirmedDetail` | Partial | Surfaces passport data inside broader booking detail, but not as a dedicated locked patient confirmation screen. |
| `GET /api/booking/{id}` | `Bookings\BookingController@getBooking` | Partial | Also surfaces passport data, but without the path-specific locking/confirmation behavior. |

**Evidence**:
- Routes: `main/hairline-backend/routes/api.php:1388`
- Passport controller: `main/hairline-backend/app/Http/Controllers/Essentials/PassportDetailsController.php:64`

### P04.2 Flight & Hotel Submission (Path B)

**Expected backend capabilities**: travel-needed choice including `no_travel_required`, outbound/return flight submissions, hotel submission, locked submitted records, read-only itinerary, and admin-only correction path.

| Endpoint | Controller | Status | Notes |
| --- | --- | --- | --- |
| `GET /api/quote/flight-detail` | `Quotes\FlightController@show` | Partial | Read endpoint exists, but model is not per-leg and does not enforce the design’s outbound/return structure. |
| `GET /api/quote/hotel-detail` | `Quotes\HotelController@show` | Partial | Hotel read endpoint exists. |
| `POST /api/quote/flight-book` | `Quotes\FlightController@store` | Partial | Create endpoint exists, but flight schema lacks `leg_type`, so outbound/return independence is not modeled. Also still requires passport data, which conflicts with Path B. |
| `POST /api/quote/hotel-book` | `Quotes\HotelController@store` | Partial | Create endpoint exists, but also depends on passport presence even though Path B should not. |
| `POST /api/quote/flight-update` | `Quotes\FlightController@update` | Partial | Update endpoint proves submitted records are editable, which conflicts with the lock-after-submit design. |
| `POST /api/quote/hotel-update` | `Quotes\HotelController@update` | Partial | Same lock conflict as flight. |
| `GET /api/quote/confirmed-detail` | `Quotes\QuotesController@confirmedDetail` | Partial | Can support parts of itinerary view. |
| `GET /api/booking/{id}` | `Bookings\BookingController@getBooking` | Partial | Can support parts of itinerary view. |
| `no_travel_required` endpoint | — | Missing | No endpoint or model field was found for the patient’s “No travel required” decision. |

**Evidence**:
- Patient read routes: `main/hairline-backend/routes/api.php:1326`
- Mixed-auth write routes: `main/hairline-backend/routes/api.php:399`
- Flight controller: `main/hairline-backend/app/Http/Controllers/Quotes/FlightController.php:142`
- Hotel controller: `main/hairline-backend/app/Http/Controllers/Quotes/HotelController.php:145`

### P05.1 Day-to-Day Treatment Progress

**Expected backend capabilities**: patient sees active treatment timeline/day statuses and, after completion, sees final graft count, conclusion note, prescription/advice/medication, and media.

| Endpoint | Controller | Status | Notes |
| --- | --- | --- | --- |
| `GET /api/quote/get-patient-single-quote` | `Quotes\QuotesController@singleQuote` | Partial | Loads provider, clinicians, treatment timeline context, and `treatmentPlanDailyEntries`, which can support parts of the in-progress screen. No dedicated patient progress-screen contract exists. |
| `GET /api/quote/confirmed-detail` | `Quotes\QuotesController@confirmedDetail` | Partial | Returns `treatment_plan_note` with `beginning_note`, `conclusion_notes`, `prescription`, `advice`, and `medication`, but not a dedicated completed-treatment summary contract with actual graft count/media semantics. |
| `GET /api/after-care/get-patient-aftercare-detail` | `PatientManagement\AfterCareController@getPatientAftercareDetail` | Partial | Aftercare detail exists after transition, but this is not the same as the in-progress treatment screen and does not cover the whole completed-treatment view. |

**Evidence**:
- `singleQuote`: `main/hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:4133`
- `confirmedDetail`: `main/hairline-backend/app/Http/Controllers/Quotes/QuotesController.php:7731`
- Patient aftercare detail: `main/hairline-backend/app/Http/Controllers/PatientManagement/AfterCareController.php:6597`

### P05.2 Previous Treatments List

**Expected backend capabilities**: patient aggregate treatment-history list across cases with filters/search/sort, status/progress/outcome fields, and review eligibility.

| Endpoint | Controller | Status | Notes |
| --- | --- | --- | --- |
| `GET /api/inquiry/get-patient-inquiries` | `Inquiry\InquiryController@getInquiriesByPatients` | Partial | Provides a patient aggregate list with derived stage/status and selected quote references, but it is inquiry-centric and does not expose the treatment-history card contract the flow expects. |
| `GET /api/quote/get-quotes` | `Quotes\QuotesController@index` | Partial | Inquiry-scoped quote list only; not a cross-case patient treatment-history endpoint. |
| `GET /api/quote/get-patient-single-quote` | `Quotes\QuotesController@singleQuote` | Partial | Can support the tapped case detail screen. |
| Aggregate `My Treatments` endpoint | — | Missing | No patient endpoint was found for a unified all-treatment history list with patient search/filter/sort/review-eligibility support. |

**Evidence**:
- Patient inquiries route: `main/hairline-backend/routes/api.php:1304`
- Inquiry aggregation: `main/hairline-backend/app/Http/Controllers/Inquiry/InquiryController.php:1758`

### P05.3 Submitted Reviews List

**Expected backend capabilities**: patient-owned review list/detail, edit, takedown request, status/removal reason, and provider-response visibility.

| Endpoint | Controller | Status | Notes |
| --- | --- | --- | --- |
| `POST /api/review/submit` | `ReviewController@submitReview` | Partial | Review creation exists for completed quotes, but it is only the submission entry point. |
| `GET /api/review/get-patient-provider-reviews` | `ReviewController@getPatientProviderReviews` | Partial | Provider review-browsing endpoint exists, but it is not a “My Reviews” list/detail API for the authenticated patient’s own submissions. |
| Patient `my reviews` list/detail/edit/takedown endpoints | — | Missing | No patient-owned review management endpoints were found. |

**Evidence**:
- Review routes: `main/hairline-backend/routes/api.php:1437`
- Review controller: `main/hairline-backend/app/Http/Controllers/ReviewController.php:99`

### P06.1 Notification Listing & Bubble

**Expected backend capabilities**: patient notification inbox list, unread bubble count, mark-one/mark-all-read, filtering/search/pagination, and deep-link metadata.

| Endpoint | Controller | Status | Notes |
| --- | --- | --- | --- |
| `POST /api/notifications/device-tokens` | `Notifications\DeviceTokenController@register` | Partial | Push-delivery infrastructure only. |
| `GET /api/notifications/device-tokens` | `Notifications\DeviceTokenController@index` | Partial | Device-token list only. |
| `DELETE /api/notifications/device-tokens` | `Notifications\DeviceTokenController@unregister` | Partial | Device-token removal only. |
| Patient inbox list/unread/read endpoints | — | Missing | No patient equivalents of provider/admin notification inbox APIs were found. |

**Evidence**:
- Patient notification routes: `main/hairline-backend/routes/api.php:1381`
- Provider/admin-only inbox routes: `main/hairline-backend/routes/api.php:517`, `main/hairline-backend/routes/api.php:716`

### P08.1 Help & Support

**Expected backend capabilities**: patient help hub, FAQs/articles/resources/videos, support form submission, patient ticket list/detail/reply lifecycle.

| Endpoint | Controller | Status | Notes |
| --- | --- | --- | --- |
| `GET /api/help-centre/patient-articles` | `Patients\HelpCentre\PatientHelpCentreArticleController@index` | Partial | Patient article browsing exists and is patient-accessible. |
| `GET /api/help-centre/patient-articles/featured` | `Patients\HelpCentre\PatientHelpCentreArticleController@featured` | Partial | Featured patient articles exist. |
| `GET /api/help-centre/patient-articles/category/{categoryId}` | `Patients\HelpCentre\PatientHelpCentreArticleController@getByCategory` | Partial | Patient article category browse exists. |
| `GET /api/help-centre/patient-articles/{articleId}` | `Patients\HelpCentre\PatientHelpCentreArticleController@getArticle` | Partial | Patient article detail exists. |
| `POST /api/help-centre/patient-articles/search` | `Patients\HelpCentre\PatientHelpCentreArticleController@search` | Partial | Patient article search exists. |
| `GET /api/help-centre/contact-patient-support` | `HelpCentre\ContactSupportController@patientSupport` | Partial | Patient-accessible support email endpoint exists, but it is only an email/contact stub. |
| `GET /api/help-centre/overview` | `HelpCentre\HelpCentreController@overview` | Partial | Help-centre overview exists in code, but route is under non-patient middleware. |
| `GET /api/help-centre/faqs` | `HelpCentre\FAQController@index` | Partial | FAQ endpoint exists in code, but route is under non-patient middleware. |
| `POST /api/help-centre/contact-support/submit` | `HelpCentre\ContactSupportController@submit` | Partial | Support-ticket creation exists in code, but route is under non-patient middleware and does not cover patient ticket lifecycle APIs. |
| `GET /api/help-centre/resource-library` | `HelpCentre\ResourceLibraryController@index` | Partial | Resource browsing exists in code, but route is under non-patient middleware. |
| `GET /api/help-centre/video-tutorials` | `HelpCentre\VideoTutorialsController@index` | Partial | Video browsing exists in code, but route is under non-patient middleware. |
| Patient support-ticket list/detail/reply endpoints | — | Missing | No patient ticket list, ticket detail/thread, reply, reopen, or ticket-count endpoints were found. |

**Evidence**:
- Patient help routes: `main/hairline-backend/routes/api.php:1459`
- Shared help-content routes under non-patient middleware: `main/hairline-backend/routes/api.php:319`
- Patient articles tests: `main/hairline-backend/tests/Feature/Patients/HelpCentre/PatientArticleTest.php:31`

## Cross-Flow Findings

### Present But Not Patient-Facing

These capabilities exist in `main/hairline-backend`, but the routes are not exposed on patient middleware, so they do not satisfy the patient mobile flows as designed:

- FR-027 legal document management routes under `/api/settings/legal-documents`
- Terms-and-conditions management/version routes under `/api/settings/terms-and-conditions/*`
- Help-centre overview / FAQs / resources / videos / contact-support submit routes under `/api/help-centre/*`
- Notification inbox list/read APIs for admin and provider only

### Flows With No Matching Patient API Surface

- `P03.1 Payment Methods Management`
- `P05.3 Submitted Reviews List`
- Patient notification inbox/read APIs needed by `P06.1`
- Patient ticket lifecycle APIs needed by `P08.1`

## Recommended Next Steps

1. Add dedicated patient APIs for saved payment methods, including default selection and active-obligation delete guards.
2. Add patient legal-content read APIs backed by FR-027 published documents and version metadata.
3. Add patient notification inbox endpoints: list, unread count, mark-one-read, mark-all-read.
4. Add patient support-ticket lifecycle endpoints: list, detail/thread, reply, reopen, count.
5. Tighten existing travel/passport contracts around booking scoping, lock-after-submit, and Path A vs Path B rules.
6. Add dedicated patient “My Treatments” and “My Reviews” APIs instead of relying on inquiry/provider-browsing endpoints.
