# Hairline Mobile April 2026 Postman Collection Test

**Date**: 2026-04-15  
**Type**: API testing report and validation log  
**Scope**: `local-docs/reports/2026-04-15/hairline-mobile-april-2026-postman-collection-test-report.md`

## Summary

Created the Hairline Mobile April 2026 API test report after a live sweep of the collection routes.

### Highlights

- 44 original endpoints were tested in the initial sweep
- 29 original endpoints/flows are confirmed meaningful after follow-up validation
- 7 original endpoints returned successful but sparse payloads and need product confirmation
- 8 original endpoints remain unresolved failures
- 25 follow-up validations were executed separately to clear ambiguity, and none of them returned a 5xx
- A focused retry confirmed that `GET /localization/get-cities/CAN` returns `200`; the city lookup uses the ISO alpha-3 country code format
- Additional spot checks for `USA`, `GBR`, `AUS`, `IND`, and `JPN` also returned `200`, confirming the ISO-3 format works consistently across multiple countries
- Inquiry-dependent endpoints were rerun against shared inquiry `e0a630a8-5fd0-4ef1-9c07-f88f31c7105b`; both `GET /quote/get-quotes` and `GET /inquiry/get-single-inquiry` returned `200`
- A second validation on quote-bearing inquiry `2cc9f016-17a7-443f-a420-1d0ca0f52370` confirmed the returned payloads are meaningful and include real quote/inquiry data
- Brute-force review of the patient inquiry list identified 10 inquiry IDs with quotes; each returned a non-empty `quote/get-quotes` payload and matched the expected quote count
- Added a sparse-payload review list covering empty results for login roles, patient discounts, support tickets, takedown requests, and the new inquiry/distribution flow
- Re-ran `GET /provider/get-provider-staff` against the sweep's provider token and confirmed the exact live response is `401` with `{"message":"Unauthenticated."}`
- Re-ran `GET /provider/get-reviews-by-provider-id/{provider_id}` with no auth, patient token, and provider token against `provider_id=57a44ac5-f96b-46b3-8db6-12d4782bf08d`; all three returned `{"message":"Unauthenticated."}`, so the blocker appears to be auth/guard gating rather than a missing `patient_id`
- Re-ran `POST /settings/update-provider-profile` with the provider profile ID in the payload and confirmed success: the endpoint returned `200` with the updated provider record and nested provider metadata
- Re-ran `POST /treatment/update-treatment` against treatment `7e976142-1de9-442b-8e59-7b464b0510da` with the full pricing/content payload and confirmed success: the endpoint returned `200` with the updated treatment record and attached media/package data
- Re-ran `POST /quote/create-quote` with the documented provider quote payload shape and confirmed the remaining blocker is `quote_amount` precision (`422`, "The quote amount field must have 2 decimal places.")
- Re-ran `POST /quote/create-quote` with `quote_amount=1500.00` and confirmed success: quote `a45808b1-81b1-4b68-923c-086adbeb736a` was created, `compare-quotes` returned populated comparison data, `get-quote-list` returned the provider quote list, and `get-patient-single-quote` returned a meaningful patient-facing quote payload
- Expanded the report’s Endpoint Corrections section into a retry guide covering ISO-3 city lookup, provider profile updates, treatment update payload requirements, and quote decimal-precision handling
- Added the quote decimal-precision rule to the retry guide so future reruns use `quote_amount` values with exactly 2 decimal places
- Kept `GET /provider/get-reviews-by-provider-id/{provider_id}` out of the retry-guide table because the retries still only returned `{"message":"Unauthenticated."}`; it remains documented as an unresolved auth/guard failure in the failures section

### Notes

- No 5xx response was captured in the sweep.
- Several failures were intentionally left unclassified as backend defects because they still have a plausible non-backend explanation and may need one more focused rerun.
- The report now captures the two endpoints that need your preference before I rerun them with a different execution context.
- The country-city lookup correction was verified separately after the initial sweep.
- The city lookup endpoint now has multi-country confirmation, not just the original Canada example.
- The inquiry-dependent flow now has a shared-record confirmation and should not be treated as a backend defect.
- The `inquiry_id` routes also have meaningful payload confirmation on a quote-bearing inquiry, not only a status-code pass.
- The quote endpoint has brute-force confirmation across ten quote-bearing inquiries, so empty results appear to be inquiry-specific rather than systemic.
- Several successful endpoints still return empty arrays or sparse payload fields and need product confirmation before being treated as normal.
