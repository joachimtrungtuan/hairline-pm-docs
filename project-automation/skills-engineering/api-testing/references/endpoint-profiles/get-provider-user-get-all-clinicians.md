# GET /provider-user/get-all-clinicians

## Purpose

Resolve clinician IDs scoped to the authenticated provider. Use these IDs for quote `clinicians[]` and clinician assignment calls.

## Auth

Provider bearer token. The backend scopes results with `request.user().provider_id`.

## Request

No required query parameters.

## Response Notes

Response shape:

```json
{
  "status": "success",
  "data": [
    {
      "id": "provider-user-uuid",
      "provider_id": "provider-uuid",
      "email": "clinician@example.com",
      "first_name": "Clinician",
      "last_name": "Name",
      "designation": "clinical-staff",
      "status": "active"
    }
  ]
}
```

Use `data[].id` as the clinician ID.

## Live Notes

- This is the correct clinician resolver for quote creation.
- Do not use `/provider/get-provider-staff` for quote clinician lookup. That legacy endpoint requires `provider_id` and returned `Unauthenticated` in live testing with provider tokens on 2026-04-26.
- Prefer clinicians with `status=active`. If a provider only has inactive clinicians, report the constraint before using the inactive ID.

## Verified Provider Results

| Provider Account | Provider ID | Clinician Notes |
|---|---|---|
| `provider_test1@hairline.app` | `57a44ac5-f96b-46b3-8db6-12d4782bf08d` | 3 active clinicians. |
| `provider_test2@hairline.app` | `da99eecb-160f-4b4b-b707-b709df1c320c` | 1 clinician, status `inactive`. |
| `test_provider3@clinic.com` | `e4893814-817a-4565-a41f-795ad0ba609e` | 1 active clinician. |
| `provider_test4@hairline.app` | `ba9e7bb4-d597-491c-8b0d-cbaf9fb9f37c` | 3 active clinicians. |

## Related Flows

- `api-flow-testing/references/flow-profiles/create-quote.md`
