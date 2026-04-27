# GET /treatment/get-all-treatments-with-packages

## Purpose

Resolve treatment and package IDs available to the authenticated provider. Quote creation needs a valid `treatment_id`.

## Auth

Provider bearer token.

## Request

No required query parameters.

## Response Notes

- Response shape observed live: object with `status` and `data`.
- `data[]` contains treatment records. Use `data[].id` as `treatment_id`.
- Treatment records can include `packages[]`.

## Captures

| Capture | Source | Notes |
|---|---|---|
| `TREATMENT_ID` | `data[0].id` or selected treatment ID | Verify treatment status before reuse. |
| `PACKAGE_ID` | `data[].packages[].id` | Optional for quote creation. |

## Live Notes

- On the live test environment, treatments can have `status=in_progress`; the quote creation guard accepts this as active.

## Related Flows

- `api-flow-testing/references/flow-profiles/create-quote.md`
