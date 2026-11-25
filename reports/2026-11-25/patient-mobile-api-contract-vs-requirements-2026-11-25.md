# Patient mobile API collection versus the business requirements

Date: 2026-11-25. For: the backend API team. From: the product team.

Compared: the Postman collection `PATIENT-MOBILE-handoff` (96 requests, listed in the Appendix) against the current FR PRDs and the requirements graph. Paths below are relative to the root of the docs repository. Rule ids (`REQ-…`) lead to the owning PRD in `project-requirements/functional-requirements/`.

## 1. Purpose and the one rule to keep

The mobile team starts building against this collection now, while the backend is reworked. That only works if the collection stays a stable contract.

**Rule: do not rename or remove any path, request field, response field or status value in the 96 requests. Correct by adding.** Where a correction cannot be made by adding, it is listed in section 3 and needs an agreed decision before it changes. A change that must break the contract gets a new version of the request (as was done with `/v2/accept-quote`), and the old version keeps working until the app has moved.

Two things the collection itself needs first:

1. **Example responses for every request.** The collection has none. Response shape is known only from the field names the test scripts check, so neither team can verify that response objects stay the same.
2. **Remove stored secrets.** The collection variables hold account passwords and a payment key. Replace them with empty variables before the file is shared further.

How to read the requirement side: the PRDs state business behaviour, not wire names. Where this report says a field is "needed", the name is yours to choose; the behaviour is not.

## 2. What already matches the requirements

No action needed; keep as is.

- **Quote model**: quote, quote option, option date-price row, one row per subquote. Subquote states available, accepted, not_selected, expired, withdrawn, cancelled. Quote statuses `cancelled_other_accepted` and `cancelled_provider_status` (shown to the patient as Offer Unavailable).
- **Discount**: preview that saves nothing; the code is checked again and frozen at acceptance; `PROMOTION_*` errors (REQ-005-026).
- **Acceptance and payment errors**: `SLOT_HELD`, `SLOT_TAKEN`, `INQUIRY_CANCELLED` with refund (REQ-007-096), `CARD_DECLINED`, `INSTALLMENT_NOT_ALLOWED`.
- **Offers list**: the six sort options.
- **Travel**: "no travel required"; the passport fields except the photo.
- **Account**: login, token refresh, re-authentication status, resend code, forgot password (first step), logout.
- **Reads**: profile, notification settings, locale, saved cards, deletion check and reasons, help centre FAQs and articles, support request list, notifications list, unread count, mark read, conversations and messages, aftercare plan, milestone and questionnaire.

## 3. Differences that need an agreed decision before they change

These cannot be corrected by adding alone. Until each is agreed, the mobile team does not build the screen behind it.

| No. | Requests | The collection today | The requirement | Proposed way to keep the contract |
|---|---|---|---|---|
| 1 | `travel/status`, `travel/itinerary`, `passport-details/store`, `quote/flight-detail`, `quote/hotel-detail`, `travel/no-travel-required` | Identified by `quote_id` | One travel record per booking, identified by the booking; `quote_id` must not be the only key (REQ-008-025) | Keep accepting `quote_id` and resolve the booking on the server. Add `booking_id` to the responses. |
| 2 | `quote/flight-detail` | One flight | Two flights, outbound and return; each flight and the hotel can be marked Not needed one at a time (REQ-008-083) | Agree a response that carries both flights before the travel screens are built. |
| 3 | `quote/compare-quotes` | Takes the inquiry only and returns quotes | The patient picks two or three subquotes, from the same or different providers, and compares those (REQ-005-013, REQ-005-047, REQ-005-014) | Add an optional list of selected subquote rows to the request; return one entry per subquote. |
| 4 | `booking/pay-deposit-with-saved-card` | `payment_plan_type: "full"` | Three payment options: pay in full now, deposit now and balance later, installments 2 to 9 (REQ-007-098) | Publish the full value list now. Requirement names are `full_payment`, `deposit_and_final`, `installments`, plus an installment count. |
| 5 | `passport-details/get-passport-details`, `after-care/create-aftercare-milestone-scan` | The app sends `patient_id` | A patient reaches only their own records (REQ-011-021) | Keep the field in the request, ignore its value, and use the signed-in patient. This is a security correction on the server. |
| 6 | `chat/start-support-conversation` | Opens a chat with Hairline support | Chat with support is not in scope; the patient uses the support request form (FR-012 Module Scope, REQ-012-030; FR-035) | Decided by the product owner on 2026-11-25: the support request form is the only route. The mobile app will not call this request. Leave it in place and unused, or retire it; do not extend it. |
| 7 | `aftercare/medications/{id}/taken` | Marks a medication as taken | The patient marks each dose, not the medication (FR-011 Screen 4) | Add a dose identifier to the request before the aftercare screens are built. |

## 4. Corrections that do not break the app

**Values and counts**

- `inquiry/get-patient-inquiries`: the test script checks the stage value `quote`; the requirement value is `quoted`. The full stage list is inquiry, quoted, accepted, confirmed, in_progress, aftercare, completed, cancelled. Confirm which value the server returns and correct the collection.
- `responses_count`: the collection describes it as each provider quote counted once. The requirement counts the providers who have quoted or declined (REQ-003-129). Same field, corrected number.
- `total_offers`: no requirement defines this number. Product owner decision of 2026-11-25: the app does not show it and shows `responses_count` only. Keep the field so nothing breaks.
- Subquote state `superseded` exists in the requirements and is missing from the collection's list. Add it to the documented values.
- `patient/destinations`: the app sends country and currency. The requirement reads the country from the patient's profile (FR-028). Keep the parameters as optional; the server uses the profile.

**Fields to add to existing requests**

| Request | To add | Requirement |
|---|---|---|
| `v2/accept-quote` | Errors for: the quote changed since the patient opened it; the provider is suspended; the inquiry already has an acceptance; the patient has not accepted the current legal documents | REQ-005-019, REQ-005-022, REQ-005-024, REQ-005-066 |
| Payment requests | The cancellation policy tick, stored with the policy version shown and the time; the terms tick; the payment option and installment count | REQ-006-038, REQ-007-098 |
| `quote/confirmed-detail`, `booking/{id}` | "Treatment closed early" note with the decision date and, when above zero, the refund amount; the time the status last changed; the blocked-state banner | REQ-006-085 |
| `passport-details/store` | The passport photo | FR-008 passport screen |
| `auth/patient-register` | Acceptance of the current Terms and Privacy Policy. Add as optional first; making it mandatory later breaks the current request, so agree the date with the mobile team | REQ-001-043, REQ-027-062 |
| `patients/support-tickets` (create) | Priority (default Medium), attachments, booking reference, the eight fixed categories | FR-035 Screen 5 |
| `chat/send` | Attachments: images, video and PDF, up to five per message | REQ-012-009 |
| `notifications` (list) | Filter by category and search | REQ-020-062, REQ-020-065 |
| `inquiry/get-all-offers` | Date Range filter | FR-022 patient offers list |
| `after-care/submit-questionnaire-answers` | Answer types checked per question; save as draft | REQ-011-060 |
| `after-care/create-aftercare-milestone-scan` | A photo set per scan, not one file | REQ-011-059, REQ-011-095 |

**Requests with no requirement behind them.** Product owner decision of 2026-11-25: none of these is required, and the mobile app will not use them: `DELETE /notifications/{id}`, `patient/account/active-sessions`, `patient/head-photos/summary-by-month`, and the price and rating filters on `inquiry/get-all-offers`. Leave them in place so nothing breaks; do not extend them.

**Push platforms.** The patient app registers for push on iOS and Android only (REQ-020-002). The device registration request needs no other platform value.

## 5. Patient actions the requirements need that the collection does not list

Each action was checked against the backend route file (`routes/api.php`, read only, 2026-11-25). Result for 69 single actions: 42 already have a route, 21 have none, 6 need your confirmation. Paths are relative to the API base.

### 5.1 Already in the backend: add these to the collection

They then fall under the same freeze as the 96.

| Area | Action | Existing request |
|---|---|---|
| Legal documents | Accept a newly published Terms or Privacy Policy at sign-in | `POST /settings/legal-documents/{id}/accept` |
| Registration | Complete profile; discovery answer | `POST /onboarding/patient-onboarding`, `POST /onboarding/patient-discovery` |
| Registration | Re-authentication verify | `POST /patient/reauth` |
| Password | Verify the reset code; set the new password; change password while signed in | `POST /auth/verify-otp`, `POST /auth/reset-password`, `POST /auth/change-password` |
| Profile and settings | Edit profile and photo | `POST /settings/update-patient-profile` |
| Profile and settings | Change email: request the code, confirm | `POST /patient/email/request`, `POST /patient/email/verify` |
| Profile and settings | Update the email and push switches; update language | `POST /settings/patient/notifications`, `PUT /patient/me/locale-preference` |
| Account deletion | Submit the request; extra verification send and resend | `POST /patient/account/delete-request`, `POST /patient/account/deletion/request-otp`, `POST /patient/account/deletion/resend-otp` |
| Inquiry | Create and submit, with photos, head scan and provider choice in the same request | `POST /inquiry/create-inquiry` |
| Inquiry | Cancel with a reason; confirm or decline redistribution | `POST /inquiry/cancel`, `GET /inquiry/cancellation-reasons`, `POST /inquiry/redistribution/confirm`, `POST /inquiry/redistribution/decline` |
| Payment | Choose the payment option | `POST /booking/create` (see section 3 row 4 for the value names) |
| Travel | Patient enters or edits a flight or a hotel | `POST /quote/flight-book`, `POST /quote/flight-update`, `POST /quote/hotel-book`, `POST /quote/hotel-update` |
| Aftercare | Standalone aftercare and add-on purchase, with checkout | `POST /patient/aftercare/check-eligibility`, `GET /patient/aftercare/services/{template_id}`, `GET /patient/aftercare/calculate-total`, `POST /patient/aftercare/create-payment-intent`, `POST /patient/aftercare/confirm-payment`, `POST /patient/aftercare/purchase-with-saved-card`, `GET /patient/aftercare/purchase/{request_id}/status` |
| Reviews | Submit, edit, request takedown | `POST /review/submit`, `POST /review/{review_id}`, `POST /patient/reviews/{review_id}/request-takedown` |
| Support | Support request detail; replies with attachments; helpful feedback | `GET /patients/support-tickets/{id}`, `POST /patients/support-tickets/{id}/reply`, `POST /patients/support-tickets/content-feedback` |
| Help | Search, resources, videos | `POST /help-centre/patient-articles/search`, `POST /help-centre/faqs/search`, `GET /help-centre/resource-library`, `GET /help-centre/video-tutorials` |

### 5.2 No route found: to build

| Area | Action | Requirement |
|---|---|---|
| Legal documents | Record acceptance of the Privacy Policy and consent at registration (today only the Terms are recorded, by the server, with no field from the app) | REQ-001-043, REQ-027-062 |
| Legal documents | Acceptance check before accepting a quote and before paying | REQ-005-066, REQ-027-033 |
| Legal documents | Public Cancellation Policy page | FR-027 |
| Registration | Service choice; re-authentication send and resend of the code | FR-001 |
| Profile and settings | Change email: resend and cancel | FR-001 |
| Account deletion | Read the status of the deletion request | FR-001, FR-023 |
| Inquiry | Save a draft (today the inquiry is created in one request, with no draft) | FR-003 |
| Payment | List the installment choices; pay a later installment; pay the final balance; receipts; payment history | FR-007, FR-007B (REQ-007-029) |
| Booking | Add to calendar | REQ-006-041 |
| Travel | Mark one flight or the hotel Not needed (today only the whole trip can be marked) | REQ-008-083 |
| Aftercare | Cancel a subscription | REQ-011-097 |
| Aftercare | Educational resources (today only a count is returned) | FR-011 Screen 5 |
| Aftercare | Send a text message to the aftercare team from the dashboard, and list the messages with the team's replies; the reply also raises the `aftercare.team_message` push and email notification | REQ-011-102, REQ-011-103 |
| Reviews | Check eligibility before the review form opens (today the check runs only on submit) | FR-013 |

### 5.3 Please confirm

| Item | What we saw | Question |
|---|---|---|
| Bank transfer | `POST /booking/pay-deposit` accepts a bank transfer value, and marks the first installment as paid without a real payment | Is bank transfer finished? The requirement needs transfer details and a confirmation step before anything is marked paid (REQ-007-002). |
| Medication history | Medications come inside `GET /after-care/get-patient-aftercare-detail` | Does it include past doses taken and missed? |
| Monitoring, FR-037 and FR-038 | Only head-photo requests exist (`/patient/head-photos`, day summary and day detail) | Do these carry the monitoring features, or is monitoring still to build? |
| Terms at registration | The server records Terms acceptance by itself when the account is activated | The requirement needs the patient's own tick, sent by the app, for each document. |

## 6. What we ask of the backend team

1. Confirm the freeze in section 1 for the 96 requests in the Appendix.
2. Add example responses to the collection and remove the stored secrets.
3. Answer section 3, rows 1 to 5 and 7, with the proposed or an alternative way that keeps the contract. Row 6 is decided.
4. Apply section 4 as additions.
5. Add the section 5.1 requests to the collection, build section 5.2 in the order the mobile team needs the screens, and answer section 5.3.

Limits of this comparison: of the backend source, only the route file was read (for section 5), and a few handlers where a route name was unclear. Response contents were not visible. Statements about what a response lacks are to be confirmed by you.

## Appendix: the 96 requests under the freeze

Paths are relative to the API base address. The two payment-provider calls are made by the app directly and are listed only for completeness.

**Auth**

- `POST /auth/login`
- `POST /auth/login`
- `POST /auth/login`
- `POST /auth/refresh-token`
- `GET /patient/reauth/status`

**01 Onboarding & Register**

- `POST /auth/patient-register`
- `POST /auth/activate-patient`
- `POST /auth/resend-otp`
- `POST /auth/forgot-password`
- `GET /localization/get-countries`
- `GET /patient/destinations`
- `GET /transplant-areas`
- `GET /onboarding/discovery-options`
- `GET /inquiry/get-medical-history-form`

**02 Dashboard (Offers)**

- `GET /inquiry/get-patient-inquiries`
- `GET /inquiry/get-patient-single-inquiry`
- `GET /inquiry/get-providers`

**03 Offers**

- `GET /inquiry/get-all-offers`
- `GET /inquiry/get-all-offers`
- `GET /quote/get-quotes`
- `GET /quote/get-quotes`
- `GET /quote/compare-quotes`

**04 Offer single, Provider, Treatment**

- `GET /quote/get-patient-single-quote`
- `GET /provider/get-provider-details`
- `GET /review/get-patient-provider-reviews`
- `GET /treatment/get-treatment-single/{treatment_id}`
- `GET /treatment/single-treatment-by-quote`
- `GET /public/legal-pages/terms-of-use`
- `GET /public/legal-pages/privacy-policy`

**05 Discount & Accept offer**

- `POST /quote/subquote/validate-discount`
- `POST /v2/accept-quote`
- `POST /v2/accept-quote`

**06 Booking & Payment**

- `GET /quote/confirmed-detail`
- `POST /booking/create-payment-intent`
- `POST /patient/payment-methods/setup-intent`
- `POST https://api.stripe.com/v1/payment_methods`
- `POST https://api.stripe.com/v1/setup_intents/{setup_intent_id}/confirm`
- `POST /patient/payment-methods`
- `POST /booking/pay-deposit-with-saved-card`
- `POST /booking/confirm-payment-success`
- `GET /booking/{booking_id}`
- `GET /booking/{booking_id}/payment-status`
- `GET /booking/{booking_id}/schedule`

**07 Travel & Logistics**

- `GET /travel/status`
- `GET /travel/itinerary`
- `GET /passport-details/get-passport-details`
- `POST /passport-details/store`
- `GET /quote/flight-detail`
- `GET /quote/hotel-detail`
- `POST /travel/no-travel-required`

**08 In Progress & Treatments**

- `GET /patient/treatments/history`
- `GET /patient/treatments/history`
- `GET /quote/get-treatment-dates`

**09 Aftercare**

- `GET /after-care/get-patient-aftercare-detail`
- `GET /after-care/get-patient-milestone-detail`
- `GET /after-care/get-questionnaire-form`
- `POST /after-care/submit-questionnaire-answers`
- `POST /after-care/create-aftercare-milestone-scan`
- `POST /aftercare/medications/{medication_id}/taken`
- `GET /patient/head-photos/summary-by-month`
- `GET /patient/aftercare/available-services`
- `GET /patient/aftercare/purchase-history`

**10 Notification**

- `GET /notifications`
- `GET /notifications`
- `GET /notifications/types`
- `GET /notifications/unread-count`
- `POST /notifications/{notification_id}/mark-read`
- `POST /notifications/mark-all-read`
- `DELETE /notifications/{notification_id}`
- `POST /notifications/device-tokens`

**11 Message**

- `GET /chat/conversations`
- `GET /chat/messages/{conversation_id}`
- `POST /chat/send`
- `POST /chat/mark-read/{conversation_id}`
- `POST /chat/start-support-conversation`
- `GET /calls/history`

**12 Profile & Settings**

- `GET /settings/get-patient-profile`
- `GET /settings/patient/notifications`
- `GET /settings/patient/preferences`
- `GET /patient/locale/active`
- `GET /patient/me/locale-preference`
- `GET /patient/payment-methods`
- `POST /patient/payment-methods/setup-intent`
- `POST /patient/payment-methods/{payment_method_id}/set-default`
- `GET /patient/reviews/my-reviews`
- `GET /patient/reviews/{review_id}`
- `GET /patient/account/can-delete`
- `GET /patient/account/deletion/reasons`
- `GET /patient/account/active-sessions`
- `POST /patient/account/deletion/request-otp`

**13 Help & Support**

- `GET /help-centre/overview`
- `GET /help-centre/faqs`
- `GET /help-centre/patient-articles`
- `GET /patients/support-tickets`
- `POST /patients/support-tickets`

**99 Logout**

- `POST /auth/logout`
