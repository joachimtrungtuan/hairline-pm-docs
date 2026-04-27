# POST /inquiry/create-inquiry

## Purpose

Create a patient inquiry with concern details, date ranges, medical history, and at least one scan image.

## Auth

Patient bearer token.

## Request

Multipart form-data.

| Field | Type | Required | Notes |
|---|---|---|---|
| `problem` | string | Yes | `hair`, `beard`, or `both`. |
| `scan_url[0][view]` | string | Yes | Example: `front`. |
| `scan_url[0][image]` | file | Yes | Use `assets/sample-hair-photo.jpg` unless the user provides another image. |
| `date_ranges` | JSON string | Yes | JSON-encoded array; send as a string, not a native array. |
| `problem_details` | string | Yes | Concern text. |
| `nature_of_concern` | string | Yes | Concern category/details. |
| `duration_of_concern_id` | integer | Yes | Resolve from `GET /duration-options` when unknown. |
| `previous_treatments` | string | Yes | Prior treatments or `None`. |
| `symptom_severity` | integer | Yes | 1-10. |
| `medical_history` | JSON string | Yes | Use all-false JSON object for no conditions. |
| `providers` | JSON string | No | JSON-encoded provider UUID array. |

## File Uploads

- Default image: `api-testing/assets/sample-hair-photo.jpg`.
- Attach the image with field name `scan_url[0][image]`.
- Attach `scan_url[0][view]` with a matching view label such as `front`.
- Do not use a remote image URL for scan upload fields.

## Dynamic Resolvers

| Needed Value | Resolver |
|---|---|
| `duration_of_concern_id` | `GET /duration-options` |
| Provider IDs | Use known provider IDs or provider/admin lookup endpoints when targeting specific providers. |

## Captures

| Capture | Source | Notes |
|---|---|---|
| `INQUIRY_ID` | `data.id` | Required for quote flows. |

## State Effects

- Inquiry: none -> `requested`.

## Known Errors

- Sending `date_ranges` as a native array instead of a JSON string returns validation error.
- Sending `scan_url` as a URL instead of multipart files returns validation error.
- Dates fewer than 30 days from today return validation error.

## Related Flows

- `api-flow-testing/references/flow-dictionary.md` legacy Create Inquiry entry
