# Flow Dictionary

Registered testing flows for the Hairline API. Managed by the `api-flow-register` skill.

Each entry defines: prerequisites, roles involved, step sequence (endpoint + auth + expected inputs + expected output), known state transitions, and known edge cases.

> **This dictionary starts empty.** Flows are registered one at a time as they are first tested. Run `api-flow-register` to research and register a new flow before running it with `api-flow-testing`.

---

## Flow: Create Inquiry

**Registered:** 2026-04-17
**Last updated:** 2026-04-17 (date_ranges rules clarified; Step 3 status corrected to 201; duration option labels corrected from live API)
**Prerequisites:** Active patient account exists. No prior inquiry state required — can be run from scratch.
**Roles involved:** Patient

### Steps

| Step | Endpoint | Auth | Key Inputs | Expected Output | Expected Status |
|------|----------|------|------------|-----------------|-----------------|
| 1 | `POST /auth/login` | None | `email`, `password`, `profile_type: "patient"` | `PATIENT_TOKEN` captured from `response.token` | 200 |
| 2 | `GET /duration-options` | None | *(none — public endpoint)* | Duration ID list; IDs are integers 1–4 (1 = "Less than 6 months", 2 = "6 months - 1 year", 3 = "1-2 years", 4 = "Above 1 year") | 200 |
| 3 | `POST /inquiry/create-inquiry` | Patient | Multipart form — see field table below | Inquiry created; `INQUIRY_ID` from `response.data.id`; inquiry status = `requested` | 201 |

**Step 3 — Full input list (multipart/form-data):**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `problem` | string | Yes | Enum: `hair`, `beard`, `both` |
| `scan_url[0][view]` | string | Yes | Enum: `front`, `back`, `left`, `right`, `crown` |
| `scan_url[0][image]` | file | Yes | JPEG/PNG/WebP, max 10MB per file, max 5 scans total |
| `date_ranges` | JSON string | Yes | JSON-encoded array of date range objects. Up to **10 ranges**. Each: `{"start_date":"YYYY-MM-DD","end_date":"YYYY-MM-DD"}`. Rules: (1) `start_date` must be **at least 30 days from today** (not 1 month — exactly 30 days); (2) no range may exceed 2 years from today; (3) ranges must not overlap; (4) `end_date` ≥ `start_date`. Must be sent as a JSON string, not a native array. |
| `problem_details` | string | Yes | Max 2000 chars |
| `medical_history` | JSON string | Yes | `{}` = no conditions; if any key is truthy, a matching `{key}_details` key is required |
| `nature_of_concern` | string | Yes | Max 1000 chars |
| `duration_of_concern_id` | integer | Yes | Integer from Step 2 (not a string — `1`, not `"1"`) |
| `previous_treatments` | string | Yes | Max 2000 chars |
| `symptom_severity` | integer | Yes | 1–10 |
| `transplant_area_id` | integer | No | nullable |
| `providers` | JSON string | No | JSON-encoded array of up to 5 provider UUIDs |
| `chosen_countries` | JSON string | No | JSON-encoded array of up to 10 country strings |
| `lifestyle_factors` | string | No | Max 2000 chars |
| `additional_notes` | string | No | Max 2000 chars |
| `photos[]` | file | No | JPG/PNG/MP4/MOV/AVI, max 5 files, 20MB each, videos max 30s |
| `additional_files[]` | file | No | Any type, max 5 files, 10MB each |

### State Transitions

- Inquiry: *(none)* → `requested`

### Multi-Tenant Notes

- Only authenticated patients (`Auth::guard('patient')`) can create inquiries. Provider or admin tokens receive 422 "You must be authenticated as a patient."

### Known Edge Cases

- **Medical history with conditions**: if any medical history key is truthy (e.g., `{"is_diabetes": true}`), a corresponding `_details` key is required. The key resolution order is: `{field}_details`, then `{field-without-is/any-prefix}_details`. All-false values (`{}` or every key set to `false`/`0`) require no details.
- **Legacy scan format**: the backend also accepts a legacy file array format (`scan_url[]`) without `view`/`image` keys, but the new structured format (`scan_url[0][view]` + `scan_url[0][image]`) is preferred.

### Known Error Paths

- **Missing `profile_type` at login**: omitting `profile_type: "patient"` → 422 "The profile type field is required."
- **Invalid `problem` enum**: any value other than `hair`/`beard`/`both` → 422 "The selected problem is invalid."
- **`scan_url` as URL string**: passing a URL string instead of a multipart file upload → 422 "The scan url must be an array."
- **`date_ranges` as array**: passing a raw array instead of a JSON-encoded string → 422 validation error on `date_ranges`.
- **`date_ranges` start_date too soon**: any range with `start_date` fewer than 30 days from today → 422 "Date range #N must be at least 30 days from today (minimum date: YYYY-MM-DD)."
- **`date_ranges` too far ahead**: any date more than 2 years from today → 422 "Date range #N cannot be more than 2 years in the future."
- **`date_ranges` overlapping**: two or more ranges whose date windows intersect → 422 "Date ranges #N and #M overlap."
- **`date_ranges` end before start**: `end_date` earlier than `start_date` in any range → 422 "Date range #N: end_date must be on or after start_date."
- **`date_ranges` exceeds 10 entries**: more than 10 ranges in the array → 422 "The date_ranges cannot have more than 10 date ranges."
- **`medical_history` as array**: must be a JSON-encoded string, not a native array → 422 validation error.
- **Medical condition truthy without details**: e.g., `{"is_diabetes": true}` with no `diabetes_details` key → 422 "Please provide details for the following medical conditions: is_diabetes"
- **`duration_of_concern_id` as string**: `"1"` instead of `1` → 422 "Duration of concern ID must be an integer."
- **`symptom_severity` out of range**: value < 1 or > 10 → 422 "Symptom severity must be at most 10."
- **Not authenticated as patient**: missing or wrong-role token → 422 "You must be authenticated as a patient."

### Notes

- Step 2 (`GET /duration-options`) is a public endpoint — no auth needed. Skip it if `duration_of_concern_id` is already known.
- The `INQUIRY_ID` captured in Step 3 is required as a prerequisite for the **Cancel Inquiry** flow.
- Confirmed working on 2026-04-17 using a 1×1 pixel JPEG test file for `scan_url`.

---

## Flow: Cancel Inquiry

**Registered:** 2026-04-17
**Last updated:** 2026-04-17 (backend defect documented — cancellation does not persist)
**Prerequisites:** A patient account exists with at least one inquiry in `requested` status that has no active quotes (all quotes must be in `cancelled` or `rejected` status — or no quotes at all). If no such inquiry exists, run **Create Inquiry** first to produce a fresh one.
**Roles involved:** Patient

### Steps

| Step | Endpoint | Auth | Key Inputs | Expected Output | Expected Status |
|------|----------|------|------------|-----------------|-----------------|
| 1 | `POST /auth/login` | None | `email`, `password`, `profile_type: "patient"` | `PATIENT_TOKEN` captured from `response.token` | 200 |
| 2 | `GET /inquiry/cancellation-reasons` | Patient | *(none)* | `REASON_ID` captured from response list | 200 |
| 3 | `POST /inquiry/cancel` | Patient | `inquiry_id`, `cancellation_reason_id` — see field table below | Inquiry status → `cancelled`; `cancelled_quotes_count` in response | 200 |

**Step 3 — Full input list (JSON body):**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `inquiry_id` | UUID | Yes | Must belong to the authenticated patient; must be in a cancellable state |
| `cancellation_reason_id` | UUID | Yes | From Step 2 |
| `cancellation_reason_text` | string | Conditional | Required when the selected reason is "Other" (enforced by `RequiredIfCancellationReasonOther` rule); max 1000 chars |
| `cancellation_additional_notes` | string | No | Max 2000 chars |
| `cancellation_optional_feedback` | string | No | Max 2000 chars |

### State Transitions

- Inquiry: `requested` → `cancelled`
- Side effect: any active quotes (status ≠ `cancelled` / `rejected`) are auto-cancelled → `cancelled` and providers are notified

### Multi-Tenant Notes

- The authenticated patient must own the inquiry (`inquiry.patient_id === authenticated patient ID`). Attempting to cancel another patient's inquiry returns 403.

### Known Edge Cases

- **Inquiry with active quotes**: the backend auto-cancels active quotes as a side effect if the inquiry itself is cancellable. However, if a quote has a non-cancellable status (e.g., `confirmed`, `in_progress`), `isCancellable()` returns false and the whole request returns 400 — no partial cancellation occurs.
- **Re-running after success**: running cancel a second time on the same inquiry returns 400 — the inquiry is already `cancelled`.

### Known Error Paths

- **Inquiry has active quotes**: any quote with status not in `cancelled`/`rejected` → 400 "This inquiry cannot be cancelled. It may have active quotes or already be cancelled/completed."
- **Inquiry already cancelled**: status = `cancelled` → 400 same message.
- **Inquiry completed**: status = `completed` → 400 same message.
- **Wrong patient (ownership mismatch)**: authenticated patient doesn't own the inquiry → 403 "You do not have permission to cancel this inquiry"
- **Invalid `inquiry_id`**: not a valid UUID or not found in DB → 422 validation error.
- **Invalid `cancellation_reason_id`**: UUID not found in `inquiry_cancellation_reasons` table → 422 validation error.
- **"Other" reason without text**: `cancellation_reason_id` maps to the "Other" reason but `cancellation_reason_text` is absent → 422 (enforced by `RequiredIfCancellationReasonOther` rule).

### Notes

- The most common blocker is running this against an inquiry that already has quotes (even a single non-rejected quote blocks cancellation). Always use a freshly created inquiry with no quotes.
- ⚠️ **Known backend defect (discovered 2026-04-17)**: The cancel endpoint returns HTTP 200 with `"status": "cancelled"` and a valid `cancelled_at` timestamp, but the cancellation **does not persist**. Subsequent `GET /inquiry/get-patient-single-inquiry` reads show the inquiry reverted to its pre-cancel status (`quoted`), with `cancelled_at: null` and `cancellation_reason_id: null`. Tested consistently on inquiries `07a91136` and `2f709668`. Root cause: the live test environment distributes new inquiries to providers immediately via `InquiryDistributionService`; providers auto-submit quotes quickly; the `QuoteObserver::updateInquiryStatus()` is not guarded against already-cancelled inquiries and can overwrite the `cancelled` state. **Required fix**: add a `STATUS_CANCELLED` guard at the top of `updateStatusFromQuotes()` and all `updateInquiryStatus()` code paths.

---

## Flow: Create Quote

**Registered:** 2026-04-23
**Last updated:** 2026-04-23
**Prerequisites:** An inquiry exists in `requested` status (produced by the **Create Inquiry** flow). The provider must not have already submitted a quote for the same inquiry. Provider account is active.
**Roles involved:** Provider

### Steps

| Step | Endpoint | Auth | Key Inputs | Expected Output | Expected Status |
|------|----------|------|------------|-----------------|-----------------|
| 1 | `POST /auth/login` | None | `email`, `password`, `profile_type: "provider"` | `PROVIDER_TOKEN` captured from `response.token` | 200 |
| 2 | `GET /treatment/get-all-treatments-with-packages` | Provider | *(none)* | Treatment + package list; capture `TREATMENT_ID` | 200 |
| 3 | `POST /quote/create-quote` | Provider | See field table below | Quote created; `QUOTE_ID` from `response.data.id`; quote status = `quote` | 200 |

> **Note on Step 2**: Optional if `TREATMENT_ID` is already known from a prior run. Skip it only if you have a verified active treatment UUID.

**Step 3 — Input fields (JSON body or multipart/form-data):**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `inquiry_id` | UUID | Yes | Must exist in DB and not be `cancelled` or `completed` |
| `treatment_id` | UUID | Yes | Must reference an active treatment |
| `currency` | string | Yes | e.g., `"USD"` |
| `quote_amount` | decimal string | No | Overall quote total (e.g., `"9200.00"`); recalculated from treatment dates if provided |
| `note` | string | No | Max 2000 chars |
| `estimated_grafts` | integer | No | 1–10000 |
| `treatment_dates` | JSON array | No | Array of date option objects; see sub-table below |
| `treatment_plan` | JSON array | No | Day-by-day plan; each entry: `day` (int), `date` (YYYY-MM-DD), optional `description` |
| `custom_services` | JSON array | No | Each entry: `service_name` (required), `service_description`, `price` (decimal string) |
| `package_id` | UUID | No | Existing package to attach; nullable |
| `hotel_accommodation` | boolean | No | String booleans `"true"`/`"false"` accepted in multipart |
| `flight_arrangements` | boolean | No | Same as above |
| `clinicians` | UUID array | No | Array of `provider_users.id` UUIDs belonging to this provider |

**`treatment_dates` sub-fields (per entry):**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `start_date` | YYYY-MM-DD | Yes (if using treatment_dates) | Must fall within one of the patient's inquiry `date_ranges` |
| `end_date` | YYYY-MM-DD | Yes | ≥ `start_date` |
| `appointment_date` | YYYY-MM-DD | Yes | Must be within this entry's `start_date` – `end_date` range |
| `appointment_time` | HH:mm | Yes | 24-hour format |
| `appointment_timezone` | IANA string | No | e.g., `"Asia/Ho_Chi_Minh"`; falls back to provider timezone, then UTC |
| `location_id` | integer | Yes | Country ID from `countries` table (e.g., `1` = Vietnam) |
| `price` | decimal string | Yes | Treatment date price (e.g., `"9200.00"`) |

### State Transitions

- Quote: *(none)* → `quote` (initial status on creation)
- Inquiry: `requested` → `quoted` (triggered automatically via `QuoteObserver` when the first quote is submitted for an inquiry)

### Multi-Tenant Notes

- Only authenticated providers (`auth:provider`) can call `POST /quote/create-quote`. Patient or admin tokens return 422.
- The `provider_id` is resolved from the bearer token — it is not accepted from the request body.
- A provider can only submit one quote per inquiry. A second attempt by the same provider returns 400 "Already quoted for this inquiry."

### Known Edge Cases

- **Multiple treatment date options**: the flow supports submitting multiple `treatment_dates` entries (different date windows + prices) in a single quote. The patient later selects one.
- **Auto-quoting on test environment**: in the live test environment, the `InquiryDistributionService` distributes new inquiries to providers immediately. The provider under test may see the inquiry already distributed; this is expected and does not block quote creation.

### Known Error Paths

- **Inquiry cancelled/completed**: → 400 "Cannot create quote for cancelled/completed inquiry"
- **Provider already quoted**: same provider submitting a second quote for the same inquiry → 400 "Already quoted for this inquiry"
- **Inactive treatment**: → 422 "Cannot create quote with inactive treatment. Treatment status: [status]"
- **`appointment_date` outside date range**: → 422 "The appointment date must be within the treatment date range (YYYY-MM-DD to YYYY-MM-DD)"
- **`treatment_dates` outside inquiry date_ranges**: custom `within_patient_ranges` validator → 422 with range mismatch message
- **Missing `currency`**: → 422 validation error on `currency` field
- **Not authenticated as provider**: missing or wrong-role token → 422

### Notes

- The `QUOTE_ID` captured in Step 3 is required as a prerequisite for downstream flows (e.g., Accept Quote, Schedule Quote, Flight/Hotel booking).
- `treatment_dates` dates must fall within the patient's original inquiry `date_ranges` — use those ranges as the outer bounds when constructing test dates.
- The `quote_amount` field in the response will differ from the submitted value — the backend calls `recalculateQuoteTotal()` after saving treatment dates, which applies the provider's commission rate. This is expected behaviour, not a bug.
- All treatments on the test environment have status `in_progress`; the `isActive()` guard accepts this status, so these treatments can be used for quote creation.
- Confirmed working on 2026-04-23 via live API test (INQUIRY_ID: `c8672e74-988f-4dec-b4a0-158707a15966`, QUOTE_ID: `b1a04677-aaba-4743-9f80-a009094e14cf`).

---
