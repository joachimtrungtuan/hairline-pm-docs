# POST /auth/login

## Purpose

Authenticate a patient, provider, or admin account and capture the bearer token for later requests.

## Auth

None.

## Request

JSON body:

| Field | Type | Required | Notes |
|---|---|---|---|
| `email` | string | Yes | Account email. |
| `password` | string | Yes | Account password. |
| `profile_type` | string | Yes | `patient`, `provider`, or `admin`. Provider staff and clinicians use `provider`. |

## Captures

| Capture | Source |
|---|---|
| `TOKEN` | `response.token` |
| `PATIENT_ID` | `response.data.id` for patient login |
| `PROVIDER_USER_ID` | `response.data.id` for provider login |
| `PROVIDER_ID` | `response.data.provider_id` for provider login |

## Known Errors

- Missing `profile_type` returns validation error.
- Wrong `profile_type` for valid credentials can return auth failure or role mismatch.

## Related Flows

- `api-flow-testing/references/flow-profiles/create-quote.md`
