# Hairline Mobile — Postman Collection Map

Maps every Postman folder/request to its backend route and controller. Use this to quickly find the right endpoint for any testing scenario.

## Table of Contents

- [Connection Details](#connection-details)
- [Environment Variables](#environment-variables)
- [Patient](#patient)
- [Location Starting Price](#location-starting-price)
- [Patient Inquiry to Provider Quote](#patient-inquiry-to-provider-quote)
- [Dashboard (Offers)](#dashboard-offers)
- [Provider](#provider)
- [Hairline Team](#hairline-team)
- [Dashboard (Confirmed)](#dashboard-confirmed)
- [Common](#common)
- [Full Flow](#full-flow)
- [FR-035 (Support & Help Centre)](#fr-035)
- [FR-013 (Reviews)](#fr-013)

## Connection Details

| Key | Value |
|-----|-------|
| Base URL | `https://backend.hairline.app/api` |
| Postman Collection ID | `33112351-a879f780-945c-4d62-8a0a-6432b86bb066` |
| Postman Environment ID | `33112351-abff0ede-b0ff-4e99-a7f1-aa27851b6656` |
| Postman `{{HOST}}` variable | `https://backend.hairline.app/api` |

## Environment Variables

| Variable | Purpose | Set by |
|----------|---------|--------|
| `HOST` | Base API URL | Manual — set to `https://backend.hairline.app/api` |
| `PATIENT_TOKEN` | Bearer token for patient requests | Auto — set by Patient Login test script |
| `PATIENT_ID` | Logged-in patient's UUID | Auto — set by Patient Login test script |
| `PROVIDER_TOKEN` | Bearer token for provider requests | Auto — set by Provider Login test script |
| `PROVIDER_ID` | Logged-in provider's UUID | Auto — set by Provider Login test script |
| `INQUIRY_ID` | Current inquiry UUID | Auto — set by Create Inquiry |
| `QUOTE_ID` | Current quote UUID | Auto — set by Create Quote |
| `distributed_provider_id` | Provider assigned via auto-distribution | Auto — set by Verify Auto-Distribution |

## Patient

| # | Postman Request | Method | Route | Controller | Auth |
|---|----------------|--------|-------|------------|------|
| 1 | Patient Register | POST | `/auth/patient-register` | `Patients\PatientController@patientRegister` | None |
| 2 | Patient Activate | POST | `/auth/activate-patient` | `Patients\PatientController@patientActivation` | None |
| 3 | Patient Login | POST | `/auth/login` | `Authentication\AuthController@login` | None |
| 4 | Patient Onboarding | POST | `/auth/update-onboarding-status` | `Authentication\AuthController@updateOnboardingStatus` | Patient |
| 5 | Update Patient Profile | POST | `/patient/update-profile` | `Patients\PatientController@updateProfile` | Patient |
| - | Get Discounts By Patients | GET | `/discounts/patient` | `Discounts\DiscountController@getByPatient` | Patient |
| - | Assign Patient Discounts | POST | `/discounts/assign` | `Discounts\DiscountController@assign` | Admin |

## Location Starting Price

| Postman Request | Method | Route | Controller | Auth |
|----------------|--------|-------|------------|------|
| Get All Location Starting Prices | GET | `/locations` | `LocationController@index` | None |
| Create Location Starting Price | POST | `/locations` | `LocationController@store` | None |
| Delete Location Starting Price | DELETE | `/locations/{id}` | `LocationController@destroy` | None |
| Update Location Starting Price | PUT | `/locations/{id}` | `LocationController@update` | None |

## Patient Inquiry to Provider Quote

This is the core business flow. Patient creates inquiry -> system distributes to providers -> provider creates quote -> patient views/accepts.

| # | Postman Request | Method | Route | Controller | Auth |
|---|----------------|--------|-------|------------|------|
| 1 | Create Inquiry | POST | `/patient/inquiry/create-inquiry` | `Inquiry\InquiryController@store` | Patient |
| 2 | Verify Auto-Distribution | GET | `/inquiry/{inquiryId}/distribution` | `Inquiry\InquiryController@getInquiryDistribution` | Provider/Admin |
| 3 | Provider Get Inquiry Queue | GET | `/inquiry/get-single-inquiry` | `Inquiry\InquiryController@show` | Provider |
| 4 | Provider View Inquiry Details | GET | `/inquiry/get-single-inquiry` | `Inquiry\InquiryController@show` | Provider |
| 5.1 | Get All Treatments With Packages | GET | `/treatment/get-all-treatments-with-packages` | `Packages\TreatmentController@getAllTreatmentsWithPackages` | Provider |
| 5.2 | Get Available Clinicians | GET | `/provider-user/get-all-clinicians` | `Providers\ProviderUserController@getAllClinicians` | Provider |
| 5.3 | Create Quote (Full data) | POST | `/quote/schedule-quote` | `Quotes\ScheduleController@store` | Provider |
| 6 | Patient View Quotes | GET | `/quote/get-quote-list` | `Quotes\QuotesController@quotesList` | Patient |
| 7 | Update Quote Status (Confirm) | POST | `/quote/{id}/update` | `Quotes\QuotesController@update` | Provider/Admin |
| 8 | Provider View Inquiry (De-anonymized) | GET | `/inquiry/get-single-inquiry` | `Inquiry\InquiryController@show` | Provider |

> Live correction: For quote clinician IDs, use `GET /provider-user/get-all-clinicians` with the same provider token. Do not use `/provider/get-provider-staff` for Create Quote clinician lookup; it returned `Unauthenticated` in live testing with provider tokens on 2026-04-26.

## Dashboard (Offers)

| Postman Request | Method | Route | Controller | Auth |
|----------------|--------|-------|------------|------|
| Get all offers of inquiry | GET | `/quote/get-quote-list` | `Quotes\QuotesController@quotesList` | Patient |
| Get Patient Single Quote | GET | `/quote/get-single-quote/{id}` | `Quotes\QuotesController@show` | Patient |
| Quote Apply Discount | POST | `/discounts/apply` | `Discounts\DiscountController@apply` | Patient |
| Accept Quote | POST | `/quote/{id}/update` | `Quotes\QuotesController@update` | Patient |
| Patient Get Provider Details | GET | `/provider/get-single-provider` | `Providers\ProviderController@getProviderProfile` | Provider/Patient |
| Get Treatment Single | GET | `/treatment/single-treatment-by-quote` | `Packages\TreatmentController@getSingleTreatmentByQuoteId` | Provider/Patient |
| Patient Creates PaymentIntent | POST | `/billing/create-payment-intent` | `Billing\PaymentController@createPaymentIntent` | Patient |
| Get Treatment Dates By Quote Id | GET | `/quote/get-schedule-details` | `Quotes\ScheduleController@quoteDetailForScheduled` | Provider/Patient |

## Provider

| Postman Request | Method | Route | Controller | Auth |
|----------------|--------|-------|------------|------|
| Provider Login | POST | `/auth/login` | `Authentication\AuthController@login` | None |
| Update Treatment | POST | `/treatment/update-treatment` | `Packages\TreatmentController@update` | Provider |
| Update Provider Profile | POST | `/settings/update-provider-profile` | `Providers\ProviderController@updateProviderProfileByProvider` | Provider |

## Hairline Team

| Postman Request | Method | Route | Controller | Auth |
|----------------|--------|-------|------------|------|
| Hairline Team Login | POST | `/auth/login` | `Authentication\AuthController@login` | None (profile_type: "admin") |
| Get All Providers | GET | `/get-all-providers` | `Providers\ProviderController@index` | Admin |
| Get All Discounts | GET | `/discounts` | `Discounts\DiscountController@index` | Admin |

## Dashboard (Confirmed)

| # | Postman Request | Method | Route | Controller | Auth |
|---|----------------|--------|-------|------------|------|
| 1 | Hotel & flight provide by patient | POST | `/patient/travel-info` | `Patients\PatientController@updateTravelInfo` | Patient |
| 2.1 | Provider List confirmed appointments | GET | `/quote/get-quote-list` | `Quotes\QuotesController@quotesList` | Provider |
| 2.2 | Provider Get Confirmed Appointment Detail | GET | `/quote/get-confirmed-appointment-detail` | `Quotes\QuotesController@getConfirmedAppointmentDetail` | Provider |

## Common

| Postman Request | Method | Route | Controller | Auth |
|----------------|--------|-------|------------|------|
| Get Transplant Areas | GET | `/transplant-areas` | `Inquiry\InquiryController@getTransplantAreas` | None |
| Get Duration Options | GET | `/duration-options` | `Inquiry\InquiryController@getDurationOptions` | None |
| Get Cities By Country Id | GET | `/localization/get-cities/{country}` | `Essentials\CountriesCitiesController@getCitiesByCountry` | None |

## Full Flow

The "Full Flow" folder mirrors the complete patient journey end-to-end. Each sub-folder maps to a dashboard state. For multi-step flow testing sequences, use the `api-flow-testing` skill with registered flows from `api-flow-testing/references/flow-dictionary.md`.

### Sub-folders

| Sub-folder | Endpoints | Description |
|------------|-----------|-------------|
| Login | Patient Login | Patient authentication |
| Forgot Password | Forgot Password, Verify OTP, Reset Password | Password recovery flow |
| Create new user | Register, Activate, Resend OTP | Patient registration |
| Onboarding | Patient Onboarding | First-time setup |
| Dashboard (Without any request) | Get Countries, Let's address your concern, Get Popular Providers, Create Inquiry | Initial dashboard + inquiry creation |
| Dashboard (Requested) | Get Patient Inquiries, Get Patient Inquiry Details | Post-inquiry state |
| Dashboard (Offers) | Get Dashboard, Offer Details, All offers, Treatment Single, Discount, Accept, Provider Details, Request single | Quote review + acceptance |
| Dashboard (Offer Accepted) | Dashboard, Offer Details, Offer single, Request single, PaymentIntent, Stripe Webhook, Check Payment | Payment flow |
| Dashboard (Confirmed) | Dashboard, Hotel & flight, Passport Info, Hotel/Flight Booking, Start treatment | Pre-treatment logistics |
| Dashboard (In Progress) | Dashboard, Quote tabs, Update Daily Entry, End of Treatment | Active treatment |
| Dashboard (Aftercare) | Dashboard, Create Aftercare, Aftercare tabs, Milestone, Questionnaire forms | Post-treatment care |
| Dashboard (Completed) | Dashboard, Submit Review, End treatment status | Treatment completion |
| Support Centre | Supporter login/chat, Chat Support, Chat With Providers, Call (initiate/join/end) | Communication channels |
| Profile | Get Profile, Update Profile | Patient profile management |
| Review | Get Patient Reviews | Review history |
| Provider | Create Quote, Confirmed appointments, Login, Update Treatment/Profile | Provider-side operations |
| Hairline Team | Login, Update Treatment, Get Providers/Discounts | Admin operations |
| Common | Providers by Inquiry, Treatments with Packages, Clinicians, Treatment Dates, Discounts | Shared lookup endpoints |

## FR-035

Support ticket system and help centre.

| Sub-folder | Postman Request | Method | Route | Auth |
|------------|----------------|--------|-------|------|
| Authentication | Patient Login | POST | `/auth/login` | None |
| Patient Support Tickets | Create Support Ticket | POST | `/patient/support-tickets` | Patient |
| | List Patient's Tickets | GET | `/patient/support-tickets` | Patient |
| | List Tickets (Open) | GET | `/patient/support-tickets?status=open` | Patient |
| | List Tickets (Resolved) | GET | `/patient/support-tickets?status=resolved` | Patient |
| | List Tickets (Closed) | GET | `/patient/support-tickets?status=closed` | Patient |
| | View Ticket Detail | GET | `/patient/support-tickets/{id}` | Patient |
| | Reply to Ticket | POST | `/patient/support-tickets/{id}/reply` | Patient |
| Content Feedback | Submit Feedback (Helpful) | POST | `/help-centre/content-feedback` | Patient |
| | Submit Feedback (Not Helpful) | POST | `/help-centre/content-feedback` | Patient |
| Help Center | List FAQs | GET | `/help-centre/faqs` | Provider/Patient |
| | List Articles | GET | `/help-centre/tutorial-guides` | Provider/Patient |
| | List Resources | GET | `/help-centre/resource-library` | Provider/Patient |
| | List Videos | GET | `/help-centre/video-tutorials` | Provider/Patient |

## FR-013

Review system for patients, providers, and admin.

| Sub-folder | Postman Request | Method | Route | Auth |
|------------|----------------|--------|-------|------|
| Patient Reviews | Get My Reviews | GET | `/patient/reviews` | Patient |
| | Request Takedown | POST | `/patient/reviews/{id}/takedown` | Patient |
| | Get My Takedown Requests | GET | `/patient/reviews/takedown-requests` | Patient |
| | Submit Review (Form-Data) | POST | `/patient/reviews` | Patient |
| | Update Review | PUT | `/patient/reviews/{id}` | Patient |
| Provider Reviews | Get My Reviews (Screen 3) | GET | `/provider/reviews` | Provider |
| | Post Response to Review | POST | `/provider/reviews/{id}/respond` | Provider |
| Admin Reviews | Get All Reviews (Dashboard) | GET | `/admin/reviews` | Admin |
| | Remove Review | DELETE | `/admin/reviews/{id}` | Admin |
| | Redact Review Content | PATCH | `/admin/reviews/{id}/redact` | Admin |
| | Flag Review | PATCH | `/admin/reviews/{id}/flag` | Admin |
| | Unflag Review | PATCH | `/admin/reviews/{id}/unflag` | Admin |
| | Get Review Audit Trail | GET | `/admin/reviews/{id}/audit-trail` | Admin |
| Admin Takedown | Get All Takedown Requests | GET | `/admin/reviews/takedown-requests` | Admin |
| | Approve Takedown | PATCH | `/admin/reviews/takedown-requests/{id}/approve` | Admin |
| | Reject Takedown | PATCH | `/admin/reviews/takedown-requests/{id}/reject` | Admin |
| Public Reviews | Get Reviews by Provider (Public) | GET | `/provider/get-reviews-by-provider-id/{id}` | None/Patient |
| | Get Patient Provider Reviews | GET | `/patient/provider-reviews` | Patient |
