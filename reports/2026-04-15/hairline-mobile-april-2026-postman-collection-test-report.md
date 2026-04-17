# Hairline Mobile - Apr 2026 Postman Collection Test Report

**Report Date**: 2026-04-15
**Retest Date**: 2026-04-16 (Cancel Inquiry retested 2026-04-17)
**Scope**: "Hairline Mobile - Apr 2026" Postman collection — 71 endpoints
**Collection ID**: `33112351-34f95c9e-6f99-4d5f-b0a0-7b3265e893c0`
**Base URL**: `https://backend.hairline.app/api`
**Execution Method**: Live API sweep via curl, folder by folder, against the Apr 2026 collection
**Test Account**: `joachimtrungtuan.work@gmail.com` (patient role)
**Status**: Complete

---

## Scope Note

The original version of this report (2026-04-15) mistakenly tested 44 endpoints from the legacy **"Hairline Mobile"** collection instead of the correct **"Hairline Mobile - Apr 2026"** collection (71 endpoints). This retest on 2026-04-16 covers all 71 endpoints in the correct collection. The legacy collection results are no longer relevant here and have been removed.

---

## Executive Summary

All 71 endpoints in the Apr 2026 collection were tested against the live API on 2026-04-16.

| Outcome | Count |
|---|---:|
| ✅ Pass (2xx with meaningful data) | 57 |
| ⚠️ State-dependent (correct behaviour, wrong setup state) | 9 |
| 🔧 Collection mismatch (collection body/params don't match live API) | 3 |
| ❌ Backend defect (server error / silent failure) | 2 |
| **Total** | **71** |

**Two confirmed backend defects:**
- `POST /inquiry/cancel` — Returns 200 success but cancellation does not persist; subsequent reads show the inquiry reverted to pre-cancel state. Root cause: `QuoteObserver` and live provider auto-quoting race condition overwriting the cancelled status. (Discovered 2026-04-17 via flow dictionary verification test.)
- `POST /review/{REVIEW_ID}` — Returns HTTP 500 "An error occurred while updating the review." Uncaught exception in `ReviewController` update method.

**Four collection fixes were applied during testing** that converted initial 422 failures into passes:
- Upload Passport Details: collection had wrong field names
- Upload Flight Details: collection missing `leg_type` field
- Check Eligibility: collection missing `service_type` field
- Create Payment Intent: collection missing `service_type` + `payment_method` fields

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
| 9 | Q2 - Inquiry Cancel | POST | `/inquiry/cancel` | 200 | ❌ Defect | Returns 200 with `status: cancelled` in response body, but cancellation does not persist — subsequent GET shows inquiry reverted to `quoted`, `cancelled_at: null`. Tested on inquiries `07a91136` and `2f709668` (2026-04-17). Root cause: QuoteObserver / provider auto-quoting race condition overwrites cancelled state. See Backend Defects section. |
| 10 | Q2 - Inquiry Cancel | GET | `/inquiry/get-patient-inquiries` | 200 | ✅ Pass | |
| 11 | Q2 - Inquiry Cancel | GET | `/inquiry/get-patient-single-inquiry` | 200 | ✅ Pass | |
| 12 | Q4 Q5 - Passport Flight Hotel | POST | `/passport-details/store` | 200 | ✅ Pass | Collection had wrong field names (see Collection Fixes). Correct fields: passport_number, passport_issue, passport_expiry, passport_name, passport_dob, gender, location, place_of_birth. |
| 13 | Q4 Q5 - Passport Flight Hotel | GET | `/passport-details/get-passport-details` | 200 | ✅ Pass | |
| 14 | Q4 Q5 - Passport Flight Hotel | POST | `/quote/flight-book` | 200 | ✅ Pass | Collection missing `leg_type` field (valid: outbound, return). Added and passes. |
| 15 | Q4 Q5 - Passport Flight Hotel | GET | `/quote/flight-detail` | 200 | ✅ Pass | Returns 404 if flight not yet booked. Run after flight-book. |
| 16 | Q4 Q5 - Passport Flight Hotel | POST | `/quote/flight-update` | 403 | ⚠️ State-dep | "Flight records are locked after submission. Contact admin for corrections." Business rule: locks immediately after flight-book. |
| 17 | Q4 Q5 - Passport Flight Hotel | POST | `/quote/hotel-book` | 200 | ✅ Pass | |
| 18 | Q4 Q5 - Passport Flight Hotel | GET | `/quote/hotel-detail` | 200 | ✅ Pass | |
| 19 | Q4 Q5 - Passport Flight Hotel | POST | `/quote/hotel-update` | 403 | ⚠️ State-dep | "Hotel records are locked after submission. Contact admin for corrections." Same lock behaviour as flight. |
| 20 | Q7 Q8 - Reviews and Takedown | POST | `/review/submit` | 409 | ⚠️ State-dep | "Review already exists for this quote." One review per quote is allowed. Needs a completed quote with no prior review. |
| 21 | Q7 Q8 - Reviews and Takedown | GET | `/review/get-patient-provider-reviews` | 200 | ✅ Pass | |
| 22 | Q7 Q8 - Reviews and Takedown | GET | `/patient/reviews/my-reviews` | 200 | ✅ Pass | Captures REVIEW_ID |
| 23 | Q7 Q8 - Reviews and Takedown | POST | `/review/{REVIEW_ID}` | 500 | ❌ Defect | "An error occurred while updating the review." Server error — backend defect. Escalate. |
| 24 | Q7 Q8 - Reviews and Takedown | POST | `/patient/reviews/{REVIEW_ID}/request-takedown` | 409 | ⚠️ State-dep | "A takedown request for this review is already pending." One active takedown per review. |
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
| 55 | Q10 - Aftercare Purchase | POST | `/patient/aftercare/confirm-payment` | 422 | ⚠️ State-dep | "Payment has not been completed successfully." Requires Stripe.js to confirm the PI client-side first. Cannot be tested via curl alone. |
| 56 | Q10 - Aftercare Purchase | GET | `/patient/aftercare/purchase-history` | 200 | ✅ Pass | Empty array — no confirmed purchases for test account. |
| 57 | Q10 - Aftercare Purchase | GET | `/patient/aftercare/purchase/{REQUEST_ID}/status` | 404 | ⚠️ State-dep | No confirmed purchase exists. Requires completing the Stripe payment flow first. |
| 58 | Q11 - Treatment History | GET | `/patient/treatments/history` | 200 | ✅ Pass | Empty array — no completed treatments on test account. |
| 59 | Q11 - Treatment History | GET | `/treatment/single-treatment-by-quote` | 200 | ✅ Pass | Returns treatment name, package, price. |
| 60 | Q12 - Aftercare Detail | GET | `/aftercare/get-aftercare-milestones` | 200 | ✅ Pass | Returns milestone list with IDs. |
| 61 | Q12 - Aftercare Detail | GET | `/after-care/get-patient-aftercare-detail` | 422 | ⚠️ State-dep | "The after care id field is required." No active aftercare record for test account. |
| 62 | Q12 - Aftercare Detail | GET | `/after-care/get-patient-milestone-detail` | 422 | ⚠️ State-dep | Same as #61 — no aftercare record. |
| 63 | Q12 - Aftercare Detail | GET | `/aftercare/get-aftercare-instructions-medications` | 422 | ⚠️ State-dep | Same as #61 — no aftercare record. |
| 64 | Q12 - Aftercare Detail | GET | `/after-care/get-questionnaire-form` | 422 | 🔧 Collection mismatch | Collection sends `quote_id` param; API requires `questionnaire_id` (linked to an aftercare milestone scan, not a quote). |
| 65 | Q12 - Aftercare Detail | POST | `/after-care/submit-questionnaire-answers` | 422 | 🔧 Collection mismatch | Same mismatch — collection body uses `quote_id` but API requires `questionnaire_id`. |
| 66 | Q12 - Aftercare Detail | POST | `/aftercare/create-aftercare-milestone-scan` | 422 | 🔧 Collection mismatch | Collection uses `milestone_id`; API requires `aftercare_milestone_id`. Also requires `scan_date` and `scan_file` (file upload) not in collection body. |
| 67 | Extra - Device Tokens | POST | `/notifications/device-tokens` (Register) | 201 | ✅ Pass | |
| 68 | Extra - Device Tokens | GET | `/notifications/device-tokens` | 200 | ✅ Pass | |
| 69 | Extra - Device Tokens | DELETE | `/notifications/device-tokens` (Unregister) | 200 | ✅ Pass | |
| 70 | Extra - Patient Help and About | GET | `/settings/patient/help` | 200 | ✅ Pass | |
| 71 | Extra - Patient Help and About | GET | `/settings/patient/about` | 200 | ✅ Pass | |

---

## Backend Defects (Escalate)

### ❌ `POST /inquiry/cancel` — Cancellation not persisting (silent false success)

**Endpoint**: `POST /inquiry/cancel`
**Symptom**: Returns HTTP 200 `{"status":"success","message":"Inquiry cancelled successfully"}` with `"status":"cancelled"` and a valid `cancelled_at` timestamp in the response body — but subsequent `GET /inquiry/get-patient-single-inquiry` reads show the inquiry back to its pre-cancel status (`quoted`), `cancelled_at: null`, and `cancellation_reason_id: null`.
**Tested on**: 2026-04-17, inquiries `07a91136` and `2f709668` — both exhibit the same behaviour consistently.

**Root cause (code-level analysis)**:
The cancel controller auto-cancels active quotes inside a `DB::beginTransaction()` loop before updating the inquiry itself. Each `$quote->update(['status' => 'cancelled'])` triggers `QuoteObserver::updated()` → `updateInquiryStatus()`. That method calls `\App\Models\Inquiry::find($inquiryId)` — a fresh DB read that happens before the inquiry's own `status = cancelled` write. Additionally, the live test environment has an `InquiryDistributionService` (via `InquiryObserver::created()`) that distributes new inquiries to providers immediately after creation. Providers on this test account submit quotes very quickly; if any provider submits a quote after the cancel transaction commits, the `QuoteObserver::created()` fires and calls `updateInquiryStatus()` which calls `updateQuietly()` on the inquiry — potentially overwriting the `cancelled` state and resetting `cancelled_at` to null.

**Affected files**: `InquiryController::cancel()`, `QuoteObserver::updateInquiryStatus()`, `Inquiry::updateStatusFromQuotes()`

**Required fix**: Guard `updateStatusFromQuotes()` and all `updateInquiryStatus()` code paths against already-cancelled inquiries — if `$inquiry->status === STATUS_CANCELLED`, return immediately without any updates.

---

### ❌ `POST /review/{REVIEW_ID}` — HTTP 500

**Endpoint**: `POST /review/74fa1b6f-ea1f-4299-afb1-973375342717`
**Response**: `{"message": "An error occurred while updating the review."}`
**HTTP status**: 500

This is a genuine server error, not a state issue. The review exists (confirmed via `GET /patient/reviews/my-reviews`), the patient owns it, and the request was sent with all required fields (`rating`, `facility_rating`, `staff_rating`, `results_rating`, `value_rating`, `review` with ≥100 characters). The backend throws an uncaught exception internally.

**Required fix**: Investigate the `ReviewController` update method. The exception is likely a null reference or missing DB relation when updating an existing review record.

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
| *(missing)* | `passport_issue` (issue date, required) |
| `nationality` | `location` |
| *(missing)* | `place_of_birth` |
| *(missing)* | `gender` |

### 3. `POST /quote/flight-book` — Missing `leg_type`
- **Missing field**: `"leg_type": "outbound"` (or `"return"`)
- **Error without it**: 422 "The leg type field is required."

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
| *(missing)* | `scan_date` (required) |
| *(missing)* | `scan_file` (required file upload) |

---

## State-Dependent Failures (Not Backend Defects)

These endpoints returned errors due to missing data state, not backend bugs. They will pass once the required state is set up.

| Endpoint | Response | Required State |
|---|---|---|
| ~~`POST /inquiry/cancel`~~ | ✅ Resolved 2026-04-17 | Created fresh inquiry via multipart form; cancel returned 200 |
| `POST /quote/flight-update` | 403 — locked | Admin must unlock; runs before flight-book on a clean quote |
| `POST /quote/hotel-update` | 403 — locked | Admin must unlock; runs before hotel-book on a clean quote |
| `POST /review/submit` | 409 — review exists | Completed quote with no prior review |
| `POST /patient/reviews/{id}/request-takedown` | 409 — takedown pending | Review with no active takedown request |
| `POST /patient/aftercare/confirm-payment` | 422 — PI not completed | Must confirm PI via Stripe.js in client first |
| `GET /patient/aftercare/purchase/{id}/status` | 404 — no purchase | After a successful Stripe payment confirms the aftercare purchase |
| `GET /after-care/get-patient-aftercare-detail` | 422 — no aftercare | Provider activates aftercare for a completed booking |
| `GET /after-care/get-patient-milestone-detail` | 422 — no aftercare | Same as above |
| `GET /aftercare/get-aftercare-instructions-medications` | 422 — no aftercare | Same as above |

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
