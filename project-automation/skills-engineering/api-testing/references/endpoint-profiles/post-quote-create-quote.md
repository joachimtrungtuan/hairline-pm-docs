# POST /quote/create-quote

## Purpose

Create one quote for an inquiry as the authenticated provider.

## Auth

Provider bearer token. The provider ID is inferred from the token and is not accepted from the request body.

## Request

JSON body or multipart/form-data.

| Field | Type | Required | Notes |
|---|---|---|---|
| `inquiry_id` | UUID | Yes | Must exist and not be cancelled or completed. |
| `treatment_id` | UUID | Yes | Resolve with `GET /treatment/get-all-treatments-with-packages`. |
| `currency` | string | Yes | Example: `USD`, `CAD`. |
| `quote_amount` | decimal string | No | Backend recalculates totals when treatment dates are present. |
| `note` | string | No | Max 2000 chars. |
| `estimated_grafts` | integer | No | 1-10000. |
| `treatment_dates` | array | No | Required for useful offer testing; see sub-fields. |
| `treatment_plan` | array | No | Day-by-day plan. |
| `custom_services` | array | No | Optional additional services. |
| `package_id` | UUID | No | Existing package ID. |
| `hotel_accommodation` | boolean | No | String booleans accepted in multipart. |
| `flight_arrangements` | boolean | No | String booleans accepted in multipart. |
| `clinicians` | UUID array | No | Use provider user IDs from `GET /provider-user/get-all-clinicians`. Prefer active clinicians. |

## Treatment Date Fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `start_date` | `YYYY-MM-DD` | Yes | Must fit within an inquiry date range. |
| `end_date` | `YYYY-MM-DD` | Yes | Must be on or after `start_date`. |
| `appointment_date` | `YYYY-MM-DD` | Yes | Must be within `start_date` and `end_date`. |
| `appointment_time` | `HH:mm` | Yes | 24-hour format. |
| `appointment_timezone` | IANA string | No | Example: `Asia/Ho_Chi_Minh`. |
| `location_id` | integer | Yes | Country/location ID. |
| `price` | decimal string | Yes | Price for that date option. |

## Dynamic Resolvers

| Needed Value | Resolver |
|---|---|
| Inquiry date ranges | Patient inquiry detail/list response; use `treatment_schedules` or date range fields from the target inquiry. |
| `treatment_id` | `GET /treatment/get-all-treatments-with-packages` with the same provider token. |
| `clinicians[]` | `GET /provider-user/get-all-clinicians` with the same provider token; use `data[].id`; prefer `status=active`. |

## State Effects

- Quote starts with status `quote`.
- First quote for an inquiry moves inquiry into `quoted` / `quote` stage.
- Each provider can create only one quote per inquiry.

## Known Errors

- Same provider quoting the same inquiry twice returns `400` with an already-quoted message.
- Treatment dates outside patient ranges return validation errors.
- `appointment_date` outside its treatment date window returns validation error.
- Missing `currency` returns validation error.
- Cancelled or completed inquiries cannot be quoted.

## Live Notes

- Multi-date quote creation is supported. Each `treatment_dates[]` entry becomes a patient-facing offer option.
- The clinician lookup prerequisite is easy to miss. Always resolve clinicians through `/provider-user/get-all-clinicians` if testing clinician assignment in quote creation.

## Related Flows

- `api-flow-testing/references/flow-profiles/create-quote.md`
