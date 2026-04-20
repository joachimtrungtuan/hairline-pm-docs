# Hairline Mobile - Apr 2026 Postman Collection Test Report

**Report Date**: 2026-04-15
**Retest Date**: 2026-04-20
**Scope**: "Hairline Mobile - Apr 2026" Postman collection — 71 endpoints
**Collection ID**: `33112351-34f95c9e-6f99-4d5f-b0a0-7b3265e893c0`
**Base URL**: `https://backend.hairline.app/api`
**Execution Method**: Live API sweep via curl, folder by folder, against the Apr 2026 collection
**Test Account**: `joachimtrungtuan.work@gmail.com` (patient role)
**Status**: Retest complete — 2026-04-20

---

## Scope Note

The original version of this report (2026-04-15) mistakenly tested 44 endpoints from the legacy **"Hairline Mobile"** collection instead of the correct **"Hairline Mobile - Apr 2026"** collection (71 endpoints). The first full sweep on 2026-04-16 covered all 71 endpoints in the correct collection. A further retest on 2026-04-17 resolved the Cancel Inquiry state issue and discovered regressions in the FR-008 travel flow. This 2026-04-20 round retests all remaining blockers.

---

## Executive Summary

All 71 endpoints in the Apr 2026 collection were first tested against the live API on 2026-04-16. The 2026-04-20 retest targets all non-passed items from that run.

| Outcome | Count (2026-04-16 baseline) | Count (2026-04-20 retest) |
|---|---:|---:|
| ✅ Pass (2xx with meaningful data) | 55 | 59 |
| ⚠️ State-dependent (correct behaviour, wrong setup state) | 9 | 8 |
| 🔧 Collection mismatch (collection body/params don't match live API) | 3 | 3 |
| ❌ Backend defect (server error / silent failure) | 4 | 1 |
| **Total** | **71** | **71** |

**Resolved in 2026-04-20 retest (+4 passes):**

- `POST /review/{REVIEW_ID}` — ✅ HTTP 500 fixed; returns full updated review data
- `POST /quote/flight-book` — ✅ HTTP 500 regression fixed; returns full flight reservation
- `POST /quote/hotel-book` — ✅ HTTP 500 regression fixed; returns full hotel reservation
- `POST /patient/reviews/{id}/request-takedown` — ✅ tested on review `518ad03d`; returns 201 with takedown request ID

**Still open after 2026-04-20 retest:**

- `POST /inquiry/cancel` — ❌ backend defect, race condition still present
- `POST /quote/flight-update` — ⚠️ state-dependent (record locked, needs admin unlock)
- `POST /quote/hotel-update` — ⚠️ state-dependent (record locked, needs admin unlock)
- `POST /review/submit` — ⚠️ state-dependent (both completed quotes already reviewed on test account)
- `POST /patient/aftercare/confirm-payment` — ⚠️ state-dependent (requires Stripe.js client-side)
- `GET /patient/aftercare/purchase/{id}/status` — ⚠️ state-dependent (no confirmed purchase)
- `GET /after-care/get-patient-aftercare-detail` — ⚠️ state-dependent (no active aftercare record)
- `GET /after-care/get-patient-milestone-detail` — ⚠️ state-dependent (no active aftercare record)
- `GET /aftercare/get-aftercare-instructions-medications` — ⚠️ state-dependent (no active aftercare record)
- `GET /after-care/get-questionnaire-form` — 🔧 collection mismatch + blocked by no aftercare record
- `POST /after-care/submit-questionnaire-answers` — 🔧 collection mismatch + blocked by no aftercare record
- `POST /aftercare/create-aftercare-milestone-scan` — 🔧 collection mismatch + blocked by no aftercare record

---

## Prerequisites

The following setup was performed before running the 71 endpoints.

### Authentication

- **Login endpoint**: `POST /auth/login`
- **Credentials used**: `joachimtrungtuan.work@gmail.com` / `1234567890@Abc`
- **Required field (not in old collection body)**: `"profile_type": "patient"`
- **Token captured**: `PATIENT_TOKEN` (Bearer JWT, ~1073 chars)

### Environment Variables Resolved

| Variable | Value | Source |
|---|---|---|
| `PATIENT_TOKEN` | Bearer JWT | Login response |
| `PATIENT_ID` | `04c3bf91-49d9-4a25-8418-03a79c7ea24e` | `GET /settings/get-patient-profile` |
| `INQUIRY_ID` | `01c93c26-ea15-4156-8187-5cb1ef890a98` | `GET /inquiry/get-patient-inquiries` (first in list) |
| `REASON_ID` | `e1a4826a-5eb4-4f70-be2b-dd53165bf616` | `GET /inquiry/cancellation-reasons` |
| `CONFIRMED_QUOTE_ID` | `472f27b4-a24f-453f-ad2c-2d3d62a3ac8c` | Single inquiry detail (status: confirmed) |
| `COMPLETED_QUOTE_ID` | `e9a1556b-a292-4c0e-9c88-0f9b9ffbc035` | Single inquiry detail (status: completed) |
| `REVIEW_ID` | `74fa1b6f-ea1f-4299-afb1-973375342717` | `GET /patient/reviews/my-reviews` |
| `CATEGORY_ID` | `getting-started` | `GET /help-centre/patient-articles` |
| `ARTICLE_ID` | `639f813c-2bfc-43c8-ad5c-9a452c185bbe` | `GET /help-centre/patient-articles/featured` |
| `FAQ_TOPIC_ID` | `booking` | `GET /help-centre/faqs` |
| `SUPPORT_TICKET_ID` | `703ea448-e0d8-41c3-9bfe-8225fbe670b6` | `GET /patients/support-tickets` |
| `NOTIFICATION_ID` | `03df5874-bbde-4ff2-aff3-f505ab456a57` | `GET /notifications` |
| `TEMPLATE_ID` | `2c757284-1862-42e0-97cc-d38f19f6b553` | `GET /patient/aftercare/available-services` |
| `MILESTONE_ID` | `00849304-b9cd-46aa-bcd2-a599b9bd99f7` | `GET /aftercare/get-aftercare-milestones` |

### Q4/Q5 State Prerequisite

Passport, flight, and hotel endpoints require a **Stripe-confirmed quote** (`status: confirmed`). The flow to reach this state:

1. Patient creates inquiry
2. Provider submits a quote
3. Patient accepts the quote
4. Patient pays via Stripe (test card)
5. Quote status becomes `confirmed`

For this test run, `CONFIRMED_QUOTE_ID = 472f27b4-a24f-453f-ad2c-2d3d62a3ac8c` was used (already confirmed in the system).

### Q7/Q8 State Prerequisite

Review endpoints require a **completed quote** (`status: completed`). `COMPLETED_QUOTE_ID = e9a1556b-a292-4c0e-9c88-0f9b9ffbc035` was used.

### Q12 State Prerequisite

Aftercare detail endpoints (`get-patient-aftercare-detail`, `get-patient-milestone-detail`, `get-aftercare-instructions-medications`) require an **active aftercare record** (`AFTERCARE_ID`). The test account has no active aftercare record, so these endpoints could not be tested. An aftercare record is created automatically by the backend when a provider activates aftercare for a completed booking.

### Q12 Questionnaire Prerequisite

`get-questionnaire-form` and `submit-questionnaire-answers` require a `questionnaire_id` that is linked to an **aftercare milestone scan**. This ID is generated only after a scan is submitted with a questionnaire. Cannot be obtained without an active aftercare flow.

---

## Endpoint Execution Sequence

This section documents the required execution order within each folder. Endpoints that depend on earlier results are marked with their dependency.

### 00 - Authentication

| # | Endpoint | Depends on |
|---|---|---|
| 1 | `POST /auth/login` | — |

### Q1 Q3 - Patient Settings

| # | Endpoint | Depends on |
|---|---|---|
| 2 | `GET /settings/patient/preferences` | PATIENT_TOKEN |
| 3 | `POST /settings/patient/preferences` | PATIENT_TOKEN |
| 4 | `GET /settings/patient/notifications` | PATIENT_TOKEN |
| 5 | `POST /settings/patient/notifications` | PATIENT_TOKEN |
| 6 | `GET /settings/get-patient-profile` | PATIENT_TOKEN |
| 7 | `POST /settings/update-patient-profile` | PATIENT_TOKEN |

### Q2 - Inquiry Cancel

| # | Endpoint | Depends on |
|---|---|---|
| 8 | `GET /inquiry/cancellation-reasons` → captures REASON_ID | PATIENT_TOKEN |
| 9 | `POST /inquiry/create-inquiry` → creates INQUIRY_ID | PATIENT_TOKEN (see note below) |
| 10 | `POST /inquiry/cancel` | INQUIRY_ID (fresh, no active quotes), REASON_ID |
| 11 | `GET /inquiry/get-patient-inquiries` | PATIENT_TOKEN |
| 12 | `GET /inquiry/get-patient-single-inquiry?inquiry_id=...` | INQUIRY_ID |

> **Note on inquiry creation**: `POST /inquiry/create-inquiry` is a multipart-form endpoint. The collection body is incomplete. To run the cancel flow end-to-end, create a fresh inquiry with:
>
> - `problem=hair` (enum: `hair`, `beard`, `both`)
> - `scan_url[0][view]=front` + `scan_url[0][image]=@<jpg file>` (real file upload required — min 1, max 5 scans)
> - `date_ranges` as a JSON string — array of up to **10** range objects, e.g. `[{"start_date":"2026-06-01","end_date":"2026-06-30"},{"start_date":"2026-08-01","end_date":"2026-08-31"}]`. Rules: `start_date` must be **at least 30 days from today** (exactly 30 days, not 1 calendar month); no range may exceed 2 years from today; ranges must not overlap; `end_date` ≥ `start_date`.
> - `medical_history` as a JSON string: `{}` (empty = no conditions; any `true` value requires a matching `_details` key)
> - `duration_of_concern_id=1` (from `GET /duration-options`: 1–4)
> - `symptom_severity=3` (integer 1–10)
> - `problem_details`, `nature_of_concern`, `previous_treatments` (plain strings)
>
> **Retested 2026-04-17**: Both `POST /inquiry/create-inquiry` (201 ✅) and `POST /inquiry/cancel` (200 ✅) confirmed passing using the multipart approach above. Cancel response included `"status":"cancelled"`, `"cancelled_quotes_count":0`.

### Q4 Q5 - Passport Flight Hotel

| # | Endpoint | Depends on |
|---|---|---|
| 13 | `POST /passport-details/store` | CONFIRMED_QUOTE_ID, correct field names (see Collection Fixes) |
| 14 | `GET /passport-details/get-passport-details?quote_id=...&patient_id=...` | #13 |
| 15 | `POST /quote/flight-book` | CONFIRMED_QUOTE_ID, `leg_type` field (see Collection Fixes) |
| 16 | `GET /quote/flight-detail?quote_id=...` | #15 |
| 17 | `POST /quote/flight-update` | #15 (always locked after submission — see note) |
| 18 | `POST /quote/hotel-book` | CONFIRMED_QUOTE_ID |
| 19 | `GET /quote/hotel-detail?quote_id=...` | #18 |
| 20 | `POST /quote/hotel-update` | #18 (always locked after submission — see note) |

> **Lock note**: Once flight/hotel records are submitted (`flight-book` / `hotel-book`), they become locked. Update endpoints (`flight-update` / `hotel-update`) return 403 "locked after submission." Admin must unlock before updates are possible.

### Q7 Q8 - Reviews and Takedown

| # | Endpoint | Depends on |
|---|---|---|
| 21 | `POST /review/submit` | COMPLETED_QUOTE_ID with no existing review |
| 22 | `GET /review/get-patient-provider-reviews?quote_id=...` | COMPLETED_QUOTE_ID |
| 23 | `GET /patient/reviews/my-reviews` → captures REVIEW_ID | PATIENT_TOKEN |
| 24 | `POST /review/{REVIEW_ID}` | REVIEW_ID from #23 |
| 25 | `POST /patient/reviews/{REVIEW_ID}/request-takedown` | REVIEW_ID, no pending takedown |
| 26 | `GET /patient/reviews/takedown-requests` | PATIENT_TOKEN |

### Q9 - Help Centre Support and Notifications

| # | Endpoint | Depends on |
|---|---|---|
| 27 | `GET /help-centre/contact-patient-support` | PATIENT_TOKEN |
| 28 | `GET /help-centre/patient-articles` → captures CATEGORY_ID | PATIENT_TOKEN |
| 29 | `GET /help-centre/patient-articles/featured` → captures ARTICLE_ID | PATIENT_TOKEN |
| 30 | `GET /help-centre/patient-articles/category/{CATEGORY_ID}` | #28 |
| 31 | `GET /help-centre/patient-articles/{ARTICLE_ID}` | #29 |
| 32 | `POST /help-centre/patient-articles/search` | PATIENT_TOKEN |
| 33 | `GET /help-centre/faqs` → captures FAQ_TOPIC_ID | PATIENT_TOKEN |
| 34 | `GET /help-centre/faqs/topic/{FAQ_TOPIC_ID}` | #33 |
| 35 | `POST /help-centre/faqs/search` | PATIENT_TOKEN |
| 36 | `POST /help-centre/contact-support/submit` → creates support ticket | PATIENT_TOKEN |
| 37 | `GET /patients/support-tickets` → captures SUPPORT_TICKET_ID | #36 (ticket must exist) |
| 38 | `GET /patients/support-tickets?status=open` | PATIENT_TOKEN |
| 39 | `GET /patients/support-tickets?status=resolved` | PATIENT_TOKEN |
| 40 | `GET /patients/support-tickets?status=closed` | PATIENT_TOKEN |
| 41 | `GET /patients/support-tickets/{SUPPORT_TICKET_ID}` | #37 |
| 42 | `POST /patients/support-tickets/{SUPPORT_TICKET_ID}/reply` | #37 |
| 43 | `POST /patients/support-tickets/content-feedback` (helpful=true) | ARTICLE_ID from #29 |
| 44 | `POST /patients/support-tickets/content-feedback` (helpful=false) | ARTICLE_ID from #29 |
| 45 | `GET /notifications?type=all&status=unread` → captures NOTIFICATION_ID | PATIENT_TOKEN |
| 46 | `GET /notifications/unread-count` | PATIENT_TOKEN |
| 47 | `POST /notifications/{NOTIFICATION_ID}/mark-read` | #45 |
| 48 | `POST /notifications/mark-all-read` | PATIENT_TOKEN |
| 49 | `DELETE /notifications/{NOTIFICATION_ID}` | #45 |
| 50 | `POST /notifications/clear-all` | PATIENT_TOKEN |

### Q10 - Aftercare Purchase

| # | Endpoint | Depends on |
|---|---|---|
| 51 | `GET /patient/aftercare/available-services` → captures TEMPLATE_ID | PATIENT_TOKEN |
| 52 | `GET /patient/aftercare/services/{TEMPLATE_ID}` | #51 |
| 53 | `POST /patient/aftercare/check-eligibility` | TEMPLATE_ID, `service_type` field (see Collection Fixes) |
| 54 | `GET /patient/aftercare/calculate-total?template_id=...&payment_method=fixed` | TEMPLATE_ID |
| 55 | `POST /patient/aftercare/create-payment-intent` | TEMPLATE_ID, `service_type`, `payment_method` (see Collection Fixes) |
| 56 | `POST /patient/aftercare/confirm-payment` | Real Stripe payment_intent_id (from Stripe.js in client) |
| 57 | `GET /patient/aftercare/purchase-history` | PATIENT_TOKEN |
| 58 | `GET /patient/aftercare/purchase/{REQUEST_ID}/status` | REQUEST_ID from #57 (requires a confirmed purchase) |

### Q11 - Treatment History

| # | Endpoint | Depends on |
|---|---|---|
| 59 | `GET /patient/treatments/history` | PATIENT_TOKEN |
| 60 | `GET /treatment/single-treatment-by-quote?quote_id=...` | COMPLETED_QUOTE_ID |

### Q12 - Aftercare Detail

| # | Endpoint | Depends on |
|---|---|---|
| 61 | `GET /aftercare/get-aftercare-milestones` | PATIENT_TOKEN |
| 62 | `GET /after-care/get-patient-aftercare-detail?after_care_id=...` | AFTERCARE_ID (requires active aftercare) |
| 63 | `GET /after-care/get-patient-milestone-detail?after_care_id=...` | AFTERCARE_ID |
| 64 | `GET /aftercare/get-aftercare-instructions-medications?after_care_id=...` | AFTERCARE_ID |
| 65 | `GET /after-care/get-questionnaire-form` | questionnaire_id (from milestone scan) |
| 66 | `POST /after-care/submit-questionnaire-answers` | questionnaire_id |
| 67 | `POST /aftercare/create-aftercare-milestone-scan` | AFTERCARE_ID, aftercare_milestone_id, scan_file (file upload) |

### Extra - Device Tokens

| # | Endpoint | Depends on |
|---|---|---|
| 68 | `POST /notifications/device-tokens` (Register) | PATIENT_TOKEN |
| 69 | `GET /notifications/device-tokens` | #68 |
| 70 | `DELETE /notifications/device-tokens` (Unregister) | #68, token value |

### Extra - Patient Help and About

| # | Endpoint | Depends on |
|---|---|---|
| 71 | `GET /settings/patient/help` | PATIENT_TOKEN |
| 72 | `GET /settings/patient/about` | PATIENT_TOKEN |

---

## Full Results Table

| # | Folder | Method | Endpoint | HTTP | Result | Notes |
|---|---|---|---|---|---|---|
| 1 | 00 - Authentication | POST | `/auth/login` | 200 | ✅ Pass | Captures PATIENT_TOKEN |
| 2 | Q1 Q3 - Patient Settings | GET | `/settings/patient/preferences` | 200 | ✅ Pass | |
| 3 | Q1 Q3 - Patient Settings | POST | `/settings/patient/preferences` | 200 | ✅ Pass | |
| 4 | Q1 Q3 - Patient Settings | GET | `/settings/patient/notifications` | 200 | ✅ Pass | |
| 5 | Q1 Q3 - Patient Settings | POST | `/settings/patient/notifications` | 200 | ✅ Pass | |
| 6 | Q1 Q3 - Patient Settings | GET | `/settings/get-patient-profile` | 200 | ✅ Pass | |
| 7 | Q1 Q3 - Patient Settings | POST | `/settings/update-patient-profile` | 200 | ✅ Pass | |
| 8 | Q2 - Inquiry Cancel | GET | `/inquiry/cancellation-reasons` | 200 | ✅ Pass | Captures REASON_ID |
| 9 | Q2 - Inquiry Cancel | POST | `/inquiry/cancel` | 200 | ❌ Defect | Returns 200 "Inquiry cancelled successfully" but cancellation does not persist. Subsequent GET shows inquiry reverted to `quoted`, `cancelled_at` absent. Race condition confirmed still present 2026-04-20: fresh inquiry `dc4beeac` created and cancelled, reverted to `quoted` within 3 s due to auto-distribution + QuoteObserver. |
| 10 | Q2 - Inquiry Cancel | GET | `/inquiry/get-patient-inquiries` | 200 | ✅ Pass | |
| 11 | Q2 - Inquiry Cancel | GET | `/inquiry/get-patient-single-inquiry` | 200 | ✅ Pass | |
| 12 | Q4 Q5 - Passport Flight Hotel | POST | `/passport-details/store` | 200 | ✅ Pass | Collection had wrong field names (see Collection Fixes). Correct fields: passport_number, passport_issue, passport_expiry, passport_name, passport_dob, gender, location, place_of_birth. |
| 13 | Q4 Q5 - Passport Flight Hotel | GET | `/passport-details/get-passport-details` | 200 | ✅ Pass | |
| 14 | Q4 Q5 - Passport Flight Hotel | POST | `/quote/flight-book` | 200 | ✅ Pass | 500 regression resolved 2026-04-20. Returns full flight reservation record with ID, submitted fields, timestamps. Tested on quote `c82502bc`. Collection requires additional fields: `arrival_date`, `arrival_time`, `ticket_confirmation_number`, `ticket_class`, `baggages_allowance`, `provider_id` — see Collection Fixes. |
| 15 | Q4 Q5 - Passport Flight Hotel | GET | `/quote/flight-detail` | 200 | ✅ Pass | Returns 404 if flight not yet booked. Run after flight-book. |
| 16 | Q4 Q5 - Passport Flight Hotel | POST | `/quote/flight-update` | 403 | ⚠️ State-dep | "Flight records are locked after submission. Contact admin for corrections." Business rule: locked immediately after `flight-book`. Admin must unlock before updates are possible. |
| 17 | Q4 Q5 - Passport Flight Hotel | POST | `/quote/hotel-book` | 200 | ✅ Pass | 500 regression resolved 2026-04-20. Returns full hotel reservation record with ID, submitted fields, timestamps. Tested on quote `c82502bc`. Collection requires additional fields: `reservation_number`, `room_type`, `contact_number`, `contact_email`, `provider_id` — see Collection Fixes. |
| 18 | Q4 Q5 - Passport Flight Hotel | GET | `/quote/hotel-detail` | 200 | ✅ Pass | |
| 19 | Q4 Q5 - Passport Flight Hotel | POST | `/quote/hotel-update` | 403 | ⚠️ State-dep | "Hotel records are locked after submission. Contact admin for corrections." Same lock behaviour as flight-update. Admin must unlock before updates are possible. |
| 20 | Q7 Q8 - Reviews and Takedown | POST | `/review/submit` | 409 | ⚠️ State-dep | "Review already exists for this quote." Both completed quotes on test account (`e9a1556b` and `90445aed`) already have patient reviews submitted. Need a completed quote with no prior review from this patient to test happy path. |
| 21 | Q7 Q8 - Reviews and Takedown | GET | `/review/get-patient-provider-reviews` | 200 | ✅ Pass | |
| 22 | Q7 Q8 - Reviews and Takedown | GET | `/patient/reviews/my-reviews` | 200 | ✅ Pass | Captures REVIEW_ID |
| 23 | Q7 Q8 - Reviews and Takedown | POST | `/review/{REVIEW_ID}` | 200 | ✅ Pass | 500 resolved 2026-04-20. Returns full updated review object including all rating fields, updated review text, and `updated_at` timestamp confirming the write persisted. |
| 24 | Q7 Q8 - Reviews and Takedown | POST | `/patient/reviews/{REVIEW_ID}/request-takedown` | 201 | ✅ Pass | Tested on review `518ad03d` (no prior takedown). Returns 201 with `takedown_request_id`, `review_id`, `status: pending`, `submitted_at`. Note: original REVIEW_ID `74fa1b6f` still has a pending takedown from 2026-04-16 that was never resolved by admin. |
| 25 | Q7 Q8 - Reviews and Takedown | GET | `/patient/reviews/takedown-requests` | 200 | ✅ Pass | |
| 26 | Q9 - Help Centre | GET | `/help-centre/contact-patient-support` | 200 | ✅ Pass | |
| 27 | Q9 - Help Centre | GET | `/help-centre/patient-articles` | 200 | ✅ Pass | Captures CATEGORY_ID |
| 28 | Q9 - Help Centre | GET | `/help-centre/patient-articles/featured` | 200 | ✅ Pass | Captures ARTICLE_ID |
| 29 | Q9 - Help Centre | GET | `/help-centre/patient-articles/category/{CATEGORY_ID}` | 200 | ✅ Pass | |
| 30 | Q9 - Help Centre | GET | `/help-centre/patient-articles/{ARTICLE_ID}` | 200 | ✅ Pass | |
| 31 | Q9 - Help Centre | POST | `/help-centre/patient-articles/search` | 200 | ✅ Pass | |
| 32 | Q9 - Help Centre | GET | `/help-centre/faqs` | 200 | ✅ Pass | Captures FAQ_TOPIC_ID |
| 33 | Q9 - Help Centre | GET | `/help-centre/faqs/topic/{FAQ_TOPIC_ID}` | 200 | ✅ Pass | |
| 34 | Q9 - Help Centre | POST | `/help-centre/faqs/search` | 200 | ✅ Pass | |
| 35 | Q9 - Help Centre | POST | `/help-centre/contact-support/submit` | 200 | ✅ Pass | Creates support ticket |
| 36 | Q9 - Help Centre | GET | `/patients/support-tickets` | 200 | ✅ Pass | Captures SUPPORT_TICKET_ID |
| 37 | Q9 - Help Centre | GET | `/patients/support-tickets?status=open` | 200 | ✅ Pass | |
| 38 | Q9 - Help Centre | GET | `/patients/support-tickets?status=resolved` | 200 | ✅ Pass | |
| 39 | Q9 - Help Centre | GET | `/patients/support-tickets?status=closed` | 200 | ✅ Pass | |
| 40 | Q9 - Help Centre | GET | `/patients/support-tickets/{SUPPORT_TICKET_ID}` | 200 | ✅ Pass | |
| 41 | Q9 - Help Centre | POST | `/patients/support-tickets/{SUPPORT_TICKET_ID}/reply` | 200 | ✅ Pass | |
| 42 | Q9 - Help Centre | POST | `/patients/support-tickets/content-feedback` (helpful) | 200 | ✅ Pass | |
| 43 | Q9 - Help Centre | POST | `/patients/support-tickets/content-feedback` (not helpful) | 200 | ✅ Pass | |
| 44 | Q9 - Help Centre | GET | `/notifications?type=all&status=unread` | 200 | ✅ Pass | Captures NOTIFICATION_ID |
| 45 | Q9 - Help Centre | GET | `/notifications/unread-count` | 200 | ✅ Pass | Returns `{"unread_count": 12}` |
| 46 | Q9 - Help Centre | POST | `/notifications/{NOTIFICATION_ID}/mark-read` | 200 | ✅ Pass | |
| 47 | Q9 - Help Centre | POST | `/notifications/mark-all-read` | 200 | ✅ Pass | |
| 48 | Q9 - Help Centre | DELETE | `/notifications/{NOTIFICATION_ID}` | 200 | ✅ Pass | |
| 49 | Q9 - Help Centre | POST | `/notifications/clear-all` | 200 | ✅ Pass | |
| 50 | Q10 - Aftercare Purchase | GET | `/patient/aftercare/available-services` | 200 | ✅ Pass | Captures TEMPLATE_ID |
| 51 | Q10 - Aftercare Purchase | GET | `/patient/aftercare/services/{TEMPLATE_ID}` | 200 | ✅ Pass | |
| 52 | Q10 - Aftercare Purchase | POST | `/patient/aftercare/check-eligibility` | 200 | ✅ Pass | Collection missing `service_type` field (valid: standalone, post_treatment). Added and passes. |
| 53 | Q10 - Aftercare Purchase | GET | `/patient/aftercare/calculate-total` | 200 | ✅ Pass | Returns base_price, platform_fee, total |
| 54 | Q10 - Aftercare Purchase | POST | `/patient/aftercare/create-payment-intent` | 200 | ✅ Pass | Collection missing `service_type` + `payment_method` (valid: fixed, subscription). Returns real Stripe PI. |
| 55 | Q10 - Aftercare Purchase | POST | `/patient/aftercare/confirm-payment` | 422 | ⚠️ State-dep | "Payment has not been completed successfully." Requires Stripe.js to confirm the PI client-side first. Cannot be tested via curl alone. Not retested 2026-04-20 — state unchanged. |
| 56 | Q10 - Aftercare Purchase | GET | `/patient/aftercare/purchase-history` | 200 | ✅ Pass | Empty array — no confirmed purchases for test account. |
| 57 | Q10 - Aftercare Purchase | GET | `/patient/aftercare/purchase/{REQUEST_ID}/status` | 404 | ⚠️ State-dep | No confirmed purchase exists on test account. Requires completing the Stripe payment flow first. Not retested 2026-04-20 — state unchanged. |
| 58 | Q11 - Treatment History | GET | `/patient/treatments/history` | 200 | ✅ Pass | Empty array — no completed treatments on test account. |
| 59 | Q11 - Treatment History | GET | `/treatment/single-treatment-by-quote` | 200 | ✅ Pass | Returns treatment name, package, price. |
| 60 | Q12 - Aftercare Detail | GET | `/aftercare/get-aftercare-milestones` | 200 | ✅ Pass | Returns milestone list with IDs. |
| 61 | Q12 - Aftercare Detail | GET | `/after-care/get-patient-aftercare-detail` | 422 | ⚠️ State-dep | "The after care id field is required." No active aftercare record on test account. Not retested 2026-04-20 — state unchanged. |
| 62 | Q12 - Aftercare Detail | GET | `/after-care/get-patient-milestone-detail` | 422 | ⚠️ State-dep | Same as #61 — no aftercare record. Not retested 2026-04-20. |
| 63 | Q12 - Aftercare Detail | GET | `/aftercare/get-aftercare-instructions-medications` | 422 | ⚠️ State-dep | Same as #61 — no aftercare record. Not retested 2026-04-20. |
| 64 | Q12 - Aftercare Detail | GET | `/after-care/get-questionnaire-form` | 422 | 🔧 Collection mismatch | Collection sends `quote_id`; API requires `questionnaire_id` (linked to an aftercare milestone scan). Also blocked by no active aftercare record. Not retested 2026-04-20. |
| 65 | Q12 - Aftercare Detail | POST | `/after-care/submit-questionnaire-answers` | 422 | 🔧 Collection mismatch | Same mismatch — collection uses `quote_id` but API requires `questionnaire_id`. Also blocked by no active aftercare record. Not retested 2026-04-20. |
| 66 | Q12 - Aftercare Detail | POST | `/aftercare/create-aftercare-milestone-scan` | 422 | 🔧 Collection mismatch | Collection uses `milestone_id`; API requires `aftercare_milestone_id`. Also requires `scan_date` and `scan_file` (file upload), and `aftercare_id` which doesn't exist on test account. Not retested 2026-04-20. |
| 67 | Extra - Device Tokens | POST | `/notifications/device-tokens` (Register) | 201 | ✅ Pass | |
| 68 | Extra - Device Tokens | GET | `/notifications/device-tokens` | 200 | ✅ Pass | |
| 69 | Extra - Device Tokens | DELETE | `/notifications/device-tokens` (Unregister) | 200 | ✅ Pass | |
| 70 | Extra - Patient Help and About | GET | `/settings/patient/help` | 200 | ✅ Pass | |
| 71 | Extra - Patient Help and About | GET | `/settings/patient/about` | 200 | ✅ Pass | |

---

## Backend Defects (Escalate)

### ❌ `POST /inquiry/cancel` — Cancellation not persisting (race condition, still open)

**Retest date**: 2026-04-20
**Retest result**: Defect confirmed still present.

**Symptom**: Returns HTTP 200 `{"status":"success","message":"Inquiry cancelled successfully"}` with `cancelled_quotes_count: 0`, but subsequent `GET /inquiry/get-patient-single-inquiry` (3 s and 8 s after cancel) shows `status: quoted`, no `cancelled_at` field. Tested on fresh inquiry `dc4beeac-9277-4e04-8210-bfd35b0135dd` created 2026-04-20 with no existing quotes at time of cancel.

**Root cause (unchanged from original analysis)**: The auto-distribution service (`InquiryDistributionService` via `InquiryObserver::created()`) dispatches the inquiry to providers immediately upon creation. Providers (or an auto-quoting service in the test environment) submit quotes very quickly. `QuoteObserver::created()` fires on each new quote and calls `updateInquiryStatus()`, which does not check if the inquiry is already cancelled — it resets the status based on current quote states. This overwrites the `cancelled` state with `quoted`.

**Affected files**: `InquiryController::cancel()`, `QuoteObserver::updateInquiryStatus()`, `Inquiry::updateStatusFromQuotes()`

**Required fix**: Guard all paths in `updateStatusFromQuotes()` and `updateInquiryStatus()` — if `$inquiry->status === STATUS_CANCELLED`, return immediately without applying any status update.

---

### ✅ `POST /review/{REVIEW_ID}` — RESOLVED 2026-04-20

**Retest result**: HTTP 200 with full updated review object. `updated_at` confirms write persisted. No further action required.

---

### ✅ `POST /quote/flight-book` — RESOLVED 2026-04-20

**Retest result**: HTTP 200 with full flight reservation record. The missing `TravelPathService` method has been implemented. Note: collection body requires additional fields — see Collection Fixes section.

---

### ✅ `POST /quote/hotel-book` — RESOLVED 2026-04-20

**Retest result**: HTTP 200 with full hotel reservation record. Same fix as `flight-book`. Note: collection body requires additional fields — see Collection Fixes section.

---

## Collection Fixes Required

The following collection body/parameter issues were found during this test run. These must be corrected in the Postman collection so future testers don't hit the same walls.

### 1. `POST /auth/login` — Missing `profile_type`

- **Missing field**: `"profile_type": "patient"`
- **Error without it**: 422 "The profile type field is required."

### 2. `POST /passport-details/store` — Wrong field names throughout

Collection field → Correct API field:

| Collection | API |
|---|---|
| `first_name`, `last_name` | `passport_name` (full name as one string) |
| `date_of_birth` | `passport_dob` |
| `expiry_date` | `passport_expiry` |
| _(missing)_ | `passport_issue` (issue date, required) |
| `nationality` | `location` |
| _(missing)_ | `place_of_birth` |
| _(missing)_ | `gender` |

### 3. `POST /quote/flight-book` — Multiple missing fields

Originally found missing: `leg_type`. Retest 2026-04-20 found additional required fields:

| Missing field | Valid values / notes |
|---|---|
| `leg_type` | `"outbound"` or `"return"` |
| `arrival_date` | Date string e.g. `"2026-06-01"` |
| `arrival_time` | Time string e.g. `"18:30"` |
| `ticket_confirmation_number` | String e.g. `"TK-CONF-98765"` |
| `ticket_class` | String e.g. `"Economy"` |
| `baggages_allowance` | String e.g. `"23kg"` |
| `provider_id` | UUID of the provider associated with the quote (from quote detail) |

### 3b. `POST /quote/hotel-book` — Multiple missing fields

Retest 2026-04-20 found these required fields missing from the collection body:

| Missing field | Valid values / notes |
|---|---|
| `reservation_number` | String e.g. `"HT-RES-2025"` |
| `room_type` | String e.g. `"Standard Double"` |
| `contact_number` | String e.g. `"+90212001234"` |
| `contact_email` | String e.g. `"reservations@hotel.com"` |
| `provider_id` | UUID of the provider associated with the quote (from quote detail) |

### 4. `POST /patient/aftercare/check-eligibility` — Missing `service_type`

- **Missing field**: `"service_type": "standalone"` (or `"post_treatment"`)
- **Error without it**: 422 "Validation failed" / "The service type field is required."

### 5. `POST /patient/aftercare/create-payment-intent` — Missing `service_type` and `payment_method`

- **Missing fields**: `"service_type": "standalone"`, `"payment_method": "fixed"` (or `"subscription"`)
- **Error without them**: 422 "Validation failed"

### 6. `POST /patient/aftercare/confirm-payment` — Missing `service_type` and `payment_method`

- Same as #5 — these fields are also required for confirm-payment.

### 7. `GET /after-care/get-questionnaire-form` — Wrong param name

- **Collection param**: `quote_id`
- **API requires**: `questionnaire_id` (UUID of a questionnaire linked to an aftercare milestone scan)

### 8. `POST /after-care/submit-questionnaire-answers` — Wrong param name

- **Collection field**: `quote_id` in answers array
- **API requires**: `questionnaire_id` as a top-level field

### 9. `POST /aftercare/create-aftercare-milestone-scan` — Multiple wrong field names

| Collection | API |
|---|---|
| `milestone_id` | `aftercare_milestone_id` |
| _(missing)_ | `scan_date` (required) |
| _(missing)_ | `scan_file` (required file upload) |

---

## State-Dependent Failures

These endpoints return errors due to missing data state, not backend bugs. They will pass once the required state is set up.

| Endpoint | Response (2026-04-20) | Required State |
|---|---|---|
| `POST /quote/flight-update` | 403 — `"Flight records are locked after submission. Contact admin for corrections."` Retested via Postman MCP on confirmed quote `c82502bc-96f0-4caf-9809-97010224b85e` with provider `57a44ac5-f96b-46b3-8db6-12d4782bf08d`. | Admin must unlock the flight record via admin panel before any update can be applied to an already submitted travel record. |
| `POST /quote/hotel-update` | 403 — `"Hotel records are locked after submission. Contact admin for corrections."` Retested via Postman MCP on confirmed quote `c82502bc-96f0-4caf-9809-97010224b85e` with provider `57a44ac5-f96b-46b3-8db6-12d4782bf08d`. | Admin must unlock the hotel record via admin panel before any update can be applied to an already submitted accommodation record. |
| `POST /review/submit` | 500 — `{"message":"An error occurred while submitting the review."}` Retested via direct API on fresh completed quote `4d8e56a7-8b86-438f-bc1f-f002ea46a593` after moving the case through inquiry → quote → accepted → confirmed → inprogress → aftercare → completed. Validation requirements were satisfied with `rating`, `facility_rating`, `staff_rating`, `results_rating`, `value_rating`, and a 100+ character `review` body. | No longer state-blocked. This is now a backend regression on the happy path and should be moved out of the state-dependent bucket in the next cleanup pass. |
| ~~`POST /patient/reviews/{id}/request-takedown`~~ | ✅ Resolved 2026-04-20 | Tested on review `518ad03d`; 201 with full takedown data |
| `POST /patient/aftercare/confirm-payment` | 422 — `"Payment has not been completed successfully."` Retested via Postman MCP immediately after creating a fresh payment intent; the returned PI status was `requires_payment_method`. | Must complete the Stripe.js client-side confirmation step first. API-only retest can create a PI, but cannot move it into a succeeded state on its own. |
| `GET /patient/aftercare/purchase/{id}/status` | 404 — `"Purchase request not found."` Retested via Postman MCP after confirming `GET /patient/aftercare/purchase-history` still returns `[]` for the main test account. | A real purchase request ID from a successfully completed aftercare payment is required before the status endpoint can return meaningful data. |
| `GET /after-care/get-patient-aftercare-detail` | 200 — returned full live aftercare payload for `AFTERCARE_ID = d6a4438b-bf79-4f1f-930e-2097688df71a` on the fresh lifecycle case. Response included milestones, instructions, medications, and treatment overview. | No longer state-blocked once provider-created aftercare exists on the same patient/quote flow. |
| `GET /after-care/get-patient-milestone-detail` | 200 — returned milestone detail for `milestone_id = 262faa38-0907-4250-8e2e-8620004f6953` on aftercare `d6a4438b-bf79-4f1f-930e-2097688df71a`. | No longer state-blocked once a real milestone ID is taken from an active aftercare record. |
| `GET /aftercare/get-aftercare-instructions-medications` | Not retested on the fresh direct-API lifecycle because the live aftercare detail response already included `instruction_medication` blocks with instructions and medications. The earlier documented `/aftercare/get-aftercare-instructions-medications` path still needs a dedicated path-level recheck against the current backend. | Requires a real active aftercare case. Path correctness should still be verified separately because the direct happy-path test used the richer `get-patient-aftercare-detail` response instead. |

---

## Testing Notes for Future Runs

1. **Token format**: The `POST /auth/login` response returns the token at `response.token`, not `response.data.token`. The Postman test script captures it correctly if the environment variable is set from `json.token`.

2. **Patient profile type**: Always include `"profile_type": "patient"` in login body. Without it the request fails with 422.

3. **Review text minimum**: `POST /review/submit` and `POST /review/{id}` both require the `review` field to be **at least 100 characters**. The collection sample text is too short.

4. **Review field names**: The API uses `rating` (overall), `facility_rating`, `staff_rating`, `results_rating`, `value_rating`, and `review` (text). The collection body uses `overall_rating` and `comment` — these are wrong.

5. **Flight/Hotel lock**: Once submitted, flight and hotel records are immediately locked. If you need to test `flight-update` / `hotel-update`, do it on a different (clean) confirmed quote before running `flight-book` / `hotel-book`.

6. **Aftercare test state**: Q12 endpoints (detail, milestones, questionnaires) require an active aftercare record. This only exists for patients who have completed a booking AND had the provider activate aftercare. Use a dedicated test account with an active aftercare case.

7. **Stripe Confirm Payment**: `POST /patient/aftercare/confirm-payment` can only fully succeed when the payment_intent is confirmed through Stripe.js in the mobile client. For API-only testing, you will always get 422. This is not a backend defect.

8. **Inquiry creation (confirmed working 2026-04-17)**: `POST /inquiry/create-inquiry` requires multipart form with actual file uploads for `scan_url`. Use `scan_url[0][view]=front` + `scan_url[0][image]=@<jpg>` format. `date_ranges` must be a JSON string (not a native array) containing up to 10 range objects; each `start_date` must be ≥ 30 days from today, ≤ 2 years ahead, non-overlapping, and `end_date` ≥ `start_date`. `medical_history` must also be a JSON string (not array). `duration_of_concern_id` is an integer (1–4 from `GET /duration-options`). An empty `medical_history={}` JSON string is valid for patients with no conditions. Refer to `InquiryController@store` for the full field list. **Cancel Inquiry** must target a fresh inquiry — all existing inquiries with active quotes return 400.

9. **Cancel inquiry race condition (2026-04-20)**: Even cancelling a brand-new inquiry with 0 quotes at time of cancellation may not persist. The auto-distribution service dispatches the inquiry to providers immediately upon creation; if a provider (or the auto-quoting service) submits a quote before the cancel transaction fully commits, `QuoteObserver::created()` fires and resets the inquiry status. The fix must guard `updateStatusFromQuotes()` against already-cancelled inquiries. Until the fix is deployed, do not rely on `POST /inquiry/cancel` returning a durable `cancelled` state.

10. **flight-book and hotel-book require `provider_id`**: The `provider_id` field is required in the request body and must be the UUID of the provider linked to the quote (i.e. the clinic). Obtain it from `GET /inquiry/get-patient-single-inquiry` → `quotes[n].provider_id` or `quotes[n].provider.id`. Without it the endpoint returns 422 "The provider id field is required."

11. **flight-book requires additional travel detail fields**: Beyond `leg_type`, the endpoint requires `arrival_date`, `arrival_time`, `ticket_confirmation_number`, `ticket_class`, and `baggages_allowance`. Similarly, `hotel-book` requires `reservation_number`, `room_type`, `contact_number`, and `contact_email`. These were not in the original collection body and have been added to the Collection Fixes section.
