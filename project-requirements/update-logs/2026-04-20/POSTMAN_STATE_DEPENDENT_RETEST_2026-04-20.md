# Postman State-Dependent Retest

- **Date**: 2026-04-20
- **Report updated**: `local-docs/reports/2026-04-20/hairline-mobile-april-2026-postman-collection-test-report.md`
- **Scope**: Completed the `State-Dependent Failures` section using live Postman MCP retests against the correct Apr 2026 collection (`33112351-34f95c9e-6f99-4d5f-b0a0-7b3265e893c0`).

## What Changed

- Replaced the placeholder state-dependent table entries with retest-backed notes for:
  - `POST /quote/flight-update`
  - `POST /quote/hotel-update`
  - `POST /review/submit`
  - `POST /patient/aftercare/confirm-payment`
  - `GET /patient/aftercare/purchase/{id}/status`
  - `GET /after-care/get-patient-aftercare-detail`
  - `GET /after-care/get-patient-milestone-detail`
  - `GET /aftercare/get-aftercare-instructions-medications`
- Added exact response messages and the concrete retest context where available:
  - confirmed quote `c82502bc-96f0-4caf-9809-97010224b85e`
  - provider `57a44ac5-f96b-46b3-8db6-12d4782bf08d`
  - completed quote `e9a1556b-a292-4c0e-9c88-0f9b9ffbc035`

## Key Retest Outcomes

- Travel update endpoints still behave as locked-state business rules, not backend defects:
  - `flight-update` returned 403 with the locked-after-submission message.
  - `hotel-update` returned 403 with the locked-after-submission message.
- `POST /review/submit` still returns duplicate-review protection (`409`) when run against the known completed quote on the main patient account.
- Aftercare payment flow remains blocked at the expected Stripe boundary:
  - `create-payment-intent` still succeeds and returns a real PI.
  - `confirm-payment` still returns 422 because the PI remains in `requires_payment_method` without Stripe.js client confirmation.
- Purchase status remains state-blocked:
  - `purchase-history` is still empty for the main test account.
  - `purchase/{id}/status` returns 404 when queried with a placeholder UUID because no confirmed purchase exists yet.
- Aftercare-detail happy-path state is still unavailable across the tested patient accounts.
  - The detail endpoints cannot be meaningfully exercised without a real `AFTERCARE_ID`.
  - The instructions/medications route additionally returned HTML 404 on the documented path during the Postman MCP recheck, so that path should be revalidated once a real aftercare case exists.
