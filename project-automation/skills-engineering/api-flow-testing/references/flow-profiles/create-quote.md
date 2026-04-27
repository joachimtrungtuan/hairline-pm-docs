# Flow: Create Quote

## Prerequisites

- A target inquiry exists and is not `cancelled` or `completed`.
- The provider account is active.
- The provider has not already submitted a quote for the target inquiry.
- The inquiry date ranges are known before constructing `treatment_dates`.
- If testing clinician assignment, resolve clinicians before quote creation using `GET /provider-user/get-all-clinicians` with the same provider token. Do not use `/provider/get-provider-staff` for this prerequisite.

## Roles

Provider.

## Endpoint Sequence

| Step | Endpoint | Endpoint Profile | Auth | Captures | Expected Status |
|---|---|---|---|---|---|
| 1 | `POST /auth/login` | `api-testing/references/endpoint-profiles/post-auth-login.md` | None | `PROVIDER_TOKEN`, `PROVIDER_ID`, `PROVIDER_USER_ID` | 200 |
| 2 | `GET /treatment/get-all-treatments-with-packages` | `api-testing/references/endpoint-profiles/get-treatment-get-all-treatments-with-packages.md` | Provider | `TREATMENT_ID`, optional `PACKAGE_ID` | 200 |
| 3 | `GET /provider-user/get-all-clinicians` | `api-testing/references/endpoint-profiles/get-provider-user-get-all-clinicians.md` | Provider | optional `CLINICIAN_IDS` | 200 |
| 4 | `POST /quote/create-quote` | `api-testing/references/endpoint-profiles/post-quote-create-quote.md` | Provider | `QUOTE_ID`, treatment date IDs | 200 |

## State Transitions

- Quote: none -> `quote`.
- Inquiry: `requested` -> `quoted` / `quote` when the first quote is created.

## Flow Rules

- Use the same provider token for treatment lookup, clinician lookup, and quote creation.
- Build `treatment_dates` inside the patient inquiry date ranges.
- For multi-provider tests, repeat the flow once per provider. Each provider can quote the inquiry once.
- For multi-date tests, put multiple date options in one quote payload for the same provider.
- If no active clinician exists for a provider, report that before deciding whether to omit clinicians or use an inactive ID.

## Known Live Notes

- Live testing on 2026-04-26 confirmed `/provider-user/get-all-clinicians` returns provider-scoped clinicians.
- Live testing on 2026-04-26 found `/provider/get-provider-staff` returned `Unauthenticated` for provider tokens and should not be used as the Create Quote clinician prerequisite.
- Provider `provider_test2@hairline.app` had one clinician, but it was `inactive` during the 2026-04-26 check.

## Related Endpoint Profiles

- `api-testing/references/endpoint-profiles/post-auth-login.md`
- `api-testing/references/endpoint-profiles/get-treatment-get-all-treatments-with-packages.md`
- `api-testing/references/endpoint-profiles/get-provider-user-get-all-clinicians.md`
- `api-testing/references/endpoint-profiles/post-quote-create-quote.md`
