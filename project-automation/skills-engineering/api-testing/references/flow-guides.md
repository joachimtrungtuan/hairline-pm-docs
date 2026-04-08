# Flow Guides — Step-by-Step Testing Sequences

Each flow lists the exact Postman requests in order, which role to authenticate as, and what to check at each step.

## Table of Contents

- [Flow 1: Patient Registration + Onboarding](#flow-1-patient-registration--onboarding)
- [Flow 2: Inquiry Creation + Auto-Distribution](#flow-2-inquiry-creation--auto-distribution)
- [Flow 3: Provider Quote Submission](#flow-3-provider-quote-submission)
- [Flow 4: Patient Reviews + Accepts Quote](#flow-4-patient-reviews--accepts-quote)
- [Flow 5: Payment](#flow-5-payment)
- [Flow 6: Confirmed — Logistics (Hotel/Flight/Passport)](#flow-6-confirmed--logistics)
- [Flow 7: In-Progress Treatment](#flow-7-in-progress-treatment)
- [Flow 8: Aftercare](#flow-8-aftercare)
- [Flow 9: Completed + Review](#flow-9-completed--review)
- [Flow 10: Support Tickets (FR-035)](#flow-10-support-tickets)
- [Flow 11: Review Management (FR-013)](#flow-11-review-management)
- [Flow 12: Forgot Password](#flow-12-forgot-password)
- [Flow 13: Chat + Calls (Support Centre)](#flow-13-chat--calls)

---

## Flow 1: Patient Registration + Onboarding

**Roles needed:** None (public) -> Patient

| Step | Request | Auth | Key checks |
|------|---------|------|------------|
| 1 | Patient Register | None | `message` = success, check for OTP sent |
| 2 | Patient Activate | None | Use OTP from email/test; `message` = activated |
| 3 | Patient Login | None | `token` returned; `data.id` present |
| 4 | Patient Onboarding | Patient token | `onboarding_status` updated |

**Common issues:**
- Registration fails with 422 → duplicate email
- Activation fails → OTP expired (resend with Resend OTP endpoint)
- Login returns 401 → account not activated yet

---

## Flow 2: Inquiry Creation + Auto-Distribution

**Roles needed:** Patient, then Provider/Admin to verify

| Step | Request | Auth | Key checks |
|------|---------|------|------------|
| 1 | Patient Login | None | Save `PATIENT_TOKEN` and `PATIENT_ID` |
| 2 | Get Transplant Areas | None | Verify available areas for inquiry body |
| 3 | Create Inquiry | Patient | `data.id` = new inquiry UUID; status = `pending` |
| 4 | Provider Login | None | Save `PROVIDER_TOKEN` |
| 5 | Verify Auto-Distribution | Provider | Check `distributed_providers` array; verify target provider is included |
| 6 | Provider Get Inquiry Queue | Provider | New inquiry appears in provider's queue |

**Common issues:**
- Create Inquiry returns 422 → missing required fields (transplant_area_id, photos)
- Distribution empty → no matching providers for patient's criteria (location/treatment type)
- Provider doesn't see inquiry → provider not in distribution; check auto-distribution logic

---

## Flow 3: Provider Quote Submission

**Roles needed:** Provider

**Prerequisite:** Inquiry exists and is distributed to this provider (Flow 2)

| Step | Request | Auth | Key checks |
|------|---------|------|------------|
| 1 | Provider Login | None | Save `PROVIDER_TOKEN` |
| 2 | Provider Get Inquiry Queue | Provider | Find the inquiry to quote |
| 3 | Get All Treatments With Packages | Provider | Get treatment IDs for quote body |
| 4 | Get Available Clinicians | Provider | Get clinician IDs for quote body |
| 5 | Create Quote (Full data) | Provider | `data.id` = new quote UUID; status = `pending` |

**Common issues:**
- Create Quote 422 → missing treatment_dates, clinician_ids, or price fields
- Create Quote 403 → provider not authorized for this inquiry (not in distribution)
- Treatment/clinician IDs invalid → re-fetch from steps 3-4

---

## Flow 4: Patient Reviews + Accepts Quote

**Roles needed:** Patient

**Prerequisite:** At least one quote submitted (Flow 3)

| Step | Request | Auth | Key checks |
|------|---------|------|------------|
| 1 | Patient Login | None | Save `PATIENT_TOKEN` |
| 2 | Patient View Quotes | Patient | List quotes for inquiry; check `status`, `price`, `provider` data |
| 3 | Get Patient Single Quote | Patient | Full quote detail; verify treatment_dates, clinician info |
| 4 | Get Treatment Single | Patient | Treatment package details match quote |
| 5 | Patient Get Provider Details | Patient | Provider profile, reviews, location |
| 6 | (Optional) Quote Apply Discount | Patient | Verify discount applied to correct treatment_date |
| 7 | Accept Quote | Patient | Quote status changes to `accepted` |

**Common issues:**
- No quotes returned → inquiry not distributed, or provider hasn't submitted
- Accept fails 422 → quote already accepted/expired
- Discount code invalid → check discount existence and patient eligibility

---

## Flow 5: Payment

**Roles needed:** Patient

**Prerequisite:** Quote accepted (Flow 4)

| Step | Request | Auth | Key checks |
|------|---------|------|------------|
| 1 | Patient Login | None | Save `PATIENT_TOKEN` |
| 2 | Patient Creates PaymentIntent | Patient | `client_secret` returned from Stripe |
| 3 | (Simulate) Stripe Webhook | None | POST to `/webhook/stripe` with test event |
| 4 | Check Payment Status | Patient | Quote status = `confirmed` after successful payment |

**Common issues:**
- PaymentIntent fails → Stripe configuration issue; check admin payment configurations
- Webhook doesn't fire → webhook URL not configured in Stripe dashboard
- Status stuck on `accepted` → payment not completed or webhook failed

---

## Flow 6: Confirmed — Logistics

**Roles needed:** Patient + Provider

**Prerequisite:** Payment completed (Flow 5)

| Step | Request | Auth | Key checks |
|------|---------|------|------------|
| 1 | Patient Login | None | |
| 2 | Hotel & flight provide by patient | Patient | Patient submits travel preferences |
| 3 | Get Passport Information | Patient | Check if passport already on file |
| 4 | Create Or Update Passport Details | Patient | Passport data saved |
| 5 | Provider Login | None | |
| 6 | Provider - Create Hotel Booking | Provider | Hotel booking created for quote |
| 7 | Provider - Create Flight Booking | Provider | Flight booking created |
| 8 | Get Hotel Information | Patient/Provider | Verify booking details |
| 9 | Get Flight Information | Patient/Provider | Verify booking details |
| 10 | Provider - Start treatment | Provider | Quote status -> `in_progress` |

**Common issues:**
- Hotel/Flight creation 422 → missing dates or booking reference
- Start treatment fails → quote not in `confirmed` status
- Patient can't see bookings → check quote_id parameter

---

## Flow 7: In-Progress Treatment

**Roles needed:** Provider

**Prerequisite:** Treatment started (Flow 6 step 10)

| Step | Request | Auth | Key checks |
|------|---------|------|------------|
| 1 | Provider Login | None | |
| 2 | Dashboard (In Progress) | Provider | Quote appears with `in_progress` status |
| 3 | Get Patient Single Quote (4 tabs) | Provider/Patient | All tabs populated (overview, treatment plan, daily entries, scans) |
| 4 | Provider - Update Daily Entry Status | Provider | Daily entry updated with notes/photos |
| 5 | Provider End Of Treatment | Provider | Quote status -> `aftercare` |

**Common issues:**
- Daily entry update fails → invalid entry_id or wrong quote
- End treatment fails → not all required daily entries completed (depends on treatment duration)

---

## Flow 8: Aftercare

**Roles needed:** Provider + Patient

**Prerequisite:** Treatment ended (Flow 7)

| Step | Request | Auth | Key checks |
|------|---------|------|------------|
| 1 | Provider Login | None | |
| 2 | Provider - Create Aftercare | Provider | Aftercare created with milestones |
| 3 | Patient Login | None | |
| 4 | Dashboard (Aftercare) | Patient | Aftercare entry visible |
| 5 | Aftercare single (3 Tabs) | Patient | Overview, milestones, questionnaires |
| 6 | Get Patient Milestone Detail | Patient | Milestone details + progress |
| 7 | Get Questionnaire Form | Patient | Form structure returned |
| 8 | Create Questionnaire Answers | Patient | Submit answers (various types: visual scale, text, choice, pain level) |

**Common issues:**
- Create aftercare 422 → missing milestone definitions
- Questionnaire form empty → admin hasn't configured questionnaire template
- Answer submission fails → invalid question_id or answer format mismatch

---

## Flow 9: Completed + Review

**Roles needed:** Provider + Patient

**Prerequisite:** Aftercare period finished (Flow 8)

| Step | Request | Auth | Key checks |
|------|---------|------|------------|
| 1 | Provider Login | None | |
| 2 | Change quote status to completed | Provider | Quote status -> `completed` |
| 3 | Patient Login | None | |
| 4 | Dashboard (Completed) | Patient | Completed entries listed |
| 5 | Submit Review | Patient | Review created with rating + text |

**Common issues:**
- Complete status change fails → aftercare milestones not all resolved
- Review submit 422 → missing rating or review text; duplicate review

---

## Flow 10: Support Tickets

**Roles needed:** Patient

| Step | Request | Auth | Key checks |
|------|---------|------|------------|
| 1 | Patient Login | None | |
| 2 | Create Support Ticket | Patient | Ticket created with `open` status |
| 3 | List Patient's Tickets | Patient | New ticket appears |
| 4 | View Ticket Detail | Patient | Full ticket with messages |
| 5 | Reply to Ticket | Patient | Message added to ticket |
| 6 | List Tickets (filter: Open/Resolved/Closed) | Patient | Filters work correctly |

---

## Flow 11: Review Management

**Roles needed:** Patient + Provider + Admin

| Step | Request | Auth | Key checks |
|------|---------|------|------------|
| 1 | Patient Login → Submit Review | Patient | Review created |
| 2 | Provider Login → Get My Reviews | Provider | Review visible |
| 3 | Provider → Post Response to Review | Provider | Response attached |
| 4 | Admin Login → Get All Reviews | Admin | All reviews with moderation status |
| 5 | Admin → Flag Review | Admin | Review flagged |
| 6 | Patient → Request Takedown | Patient | Takedown request created |
| 7 | Admin → Get All Takedown Requests | Admin | Request visible |
| 8 | Admin → Approve/Reject Takedown | Admin | Request resolved |

---

## Flow 12: Forgot Password

**Roles needed:** None (all public)

| Step | Request | Auth | Key checks |
|------|---------|------|------------|
| 1 | Forgot Password | None | OTP sent to email |
| 2 | Verify OTP | None | OTP validated, reset token returned |
| 3 | Reset Password | None | Password changed successfully |

---

## Flow 13: Chat + Calls (Support Centre)

**Roles needed:** Patient + Provider/Supporter

| Step | Request | Auth | Key checks |
|------|---------|------|------------|
| 1 | Patient Login | None | |
| 2 | Support Team (Get contact support) | Patient | Support team info returned |
| 3 | Patient Get all conversations | Patient | Existing conversations listed |
| 4 | Send a message | Patient | Message sent |
| 5 | Get all messages in conversation | Patient | Message history |
| 6 | Supporter Login | None | |
| 7 | Get Conversations With Patients | Supporter | Patient conversations listed |
| 8 | Support User Reply | Supporter | Reply sent |
| 9 | Initiate Call | Patient/Provider | Call room created |
| 10 | Join Call | Other party | Joined call room |
| 11 | End Call | Either | Call ended, logged in history |

**Common issues:**
- Start conversation fails → conversation already exists between parties
- Call initiate fails → Twilio credentials not configured
- Messages not appearing → check conversation_id parameter
