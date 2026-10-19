# Registered Function: `PR-01-FN-001` Provider Login

**Primary module:** `PR-01`
**Participating modules:** None
**Registry status:** `ACTIVE`
**Coverage status:** Six executable cases active; four governed account-state/security gaps remain open
**Last UI-confirmed date:** 2026-07-15

> This registry entry references live PRDs and records only the test-specific interpretation needed for deterministic execution.

## 1. Registry Control

| Field | Value |
| --- | --- |
| Function ID | `PR-01-FN-001` |
| Test level | `function` |
| Primary module | `PR-01` |
| Human owner | Product Owner |
| Happy-path approval | Approved 2026-07-15 |
| Derived-case authority | Testing Constitution v1.2 |
| Registry status | `ACTIVE` |
| Created | 2026-07-14 |
| Last approved revision | `v1` |
| Supersedes | None |

## 2. Live Source References

Hashes are SHA-256 values for the referenced source sections at approval time.

| Reference ID | Source path | Requirement / heading | Approved hash |
| --- | --- | --- | --- |
| `PR-01-TC-0001-SRC-01` | `local-docs/project-requirements/functional-requirements/fr009-provider-team-roles/prd.md` | Module Scope — Provider Auth Service | `59c8b3b2ba00d4d6eb2496833645e6a9a22bd469a499a3051164cbae8e712c61` |
| `PR-01-TC-0001-SRC-02` | `local-docs/project-requirements/functional-requirements/fr015-provider-management/prd.md` | Business Workflows — activated Provider login | `63a5e004d33ca2a2390e0b6e983110f3fbd5039d05c047357daaa7c883ed093e` |
| `PR-01-TC-0002-SRC-01` | `local-docs/project-requirements/functional-requirements/fr009-provider-team-roles/prd.md` | Module Scope — Provider login | `59c8b3b2ba00d4d6eb2496833645e6a9a22bd469a499a3051164cbae8e712c61` |
| `PR-01-TC-0003-SRC-01` | `local-docs/project-requirements/functional-requirements/fr009-provider-team-roles/prd.md` | Module Scope — Provider login | `59c8b3b2ba00d4d6eb2496833645e6a9a22bd469a499a3051164cbae8e712c61` |
| `PR-01-TC-0004-SRC-01` | `local-docs/project-requirements/functional-requirements/fr009-provider-team-roles/prd.md` | Module Scope — Provider login | `59c8b3b2ba00d4d6eb2496833645e6a9a22bd469a499a3051164cbae8e712c61` |
| `PR-01-TC-0005-SRC-01` | `local-docs/project-requirements/functional-requirements/fr009-provider-team-roles/prd.md` | Module Scope — credential validation and session creation | `59c8b3b2ba00d4d6eb2496833645e6a9a22bd469a499a3051164cbae8e712c61` |
| `PR-01-TC-0006-SRC-01` | `local-docs/project-requirements/functional-requirements/fr009-provider-team-roles/prd.md` | Module Scope and Provider Role Model | `59c8b3b2ba00d4d6eb2496833645e6a9a22bd469a499a3051164cbae8e712c61` |
| `GAP-01-SRC-01` | `local-docs/project-requirements/functional-requirements/fr015-provider-management/prd.md` | Screen 4 — suspended and deactivated Provider login rules | `a74660e69a15d3757a72121403d83065fd74b64231caaba429e250d14dfcb83b` |
| `GAP-02-SRC-01` | `local-docs/project-requirements/functional-requirements/fr009-provider-team-roles/prd.md` | Remove Team Member — access revocation | `358b2de8fdd07fad9e67089fb7848ee7636b81cdc3acafe23aa9f31b352ef866` |
| `GAP-03-SRC-01` | `local-docs/project-requirements/functional-requirements/fr026-app-settings-security/prd.md` | Module Scope — Provider authentication throttling | `dc1c5dc8efc08b63beb5ef0c78a05aca6c8590c879663d4e68a79992c8bc5c99` |
| `GAP-03-SRC-02` | `local-docs/project-requirements/functional-requirements/fr026-app-settings-security/prd.md` | Business Rules — user and IP lockout controls | `7bea491ecc6ceac558a07e8a80d99f5aac581d7891bdbc284e25d336266b072c` |

## 3. Current Implementation Mapping

| Surface | Current route / API | Mapping status | Last confirmed | Notes |
| --- | --- | --- | --- | --- |
| Role selection | `/auth` | Confirmed | 2026-07-15 | Provider and Hairline Team choices are visible |
| Provider login | `/auth/provider/login` | Confirmed | 2026-07-15 | Username, password, validation, and authentication submission |
| Hairline Team login | `/auth/hairline-team/login` | Confirmed | 2026-07-15 | Used to verify Provider credential isolation |
| Provider Dashboard | `/` | Confirmed | 2026-07-15 | Successful Provider landing route |
| Authentication API | `POST /api/auth/login` | Confirmed | 2026-07-15 | Browser-submitted implementation evidence |

## 4. Requirement and Category Coverage

### Requirement Coverage Matrix

| Requirement or rule | Category | Case / gap | Coverage |
| --- | --- | --- | --- |
| Active Provider authenticates and reaches Provider Platform | Happy path | `PR-01-TC-0001` | Complete |
| Username is required before authentication submission | Validation | `PR-01-TC-0002`, `PR-01-TC-0004` | Complete |
| Password is required before authentication submission | Validation | `PR-01-TC-0003`, `PR-01-TC-0004` | Complete |
| Unknown credentials do not create a Provider session | Negative | `PR-01-TC-0005` | Complete |
| Provider identity cannot authenticate through Hairline Team role | Permission / role | `PR-01-TC-0006` | Complete |
| Suspended Provider logs in and sees suspension restriction | State transition | `GAP-01` | Open — no dedicated suspended credential |
| Deactivated Provider login is disabled | State transition | `GAP-01` | Open — no dedicated deactivated credential or safe reversible setup |
| Removed team member cannot authenticate and receives revoked-access message | State transition / permission | `GAP-02` | Open — no dedicated removed-member credential |
| Configured user lockout and fixed IP throttling are enforced | Boundary / security | `GAP-03` | Open — ordinary retries could lock shared accounts or test IP; no reset/isolation control |

### Category Applicability

| Category | Status | Notes |
| --- | --- | --- |
| Happy path | Covered | Active Provider login |
| Negative / validation | Covered | Missing inputs and unknown credentials |
| Boundary / edge | Partially covered | Empty-field boundary covered; throttling remains `GAP-03` |
| Permission / role | Covered | Provider identity rejected on Hairline Team route |
| State transition | Gap | Suspended, deactivated, and removed-member states need dedicated accounts |
| Idempotency | Not applicable | No PRD-defined repeated-submit outcome for this function |
| Concurrency-sensitive | Not applicable | No PRD-defined concurrent login behavior for this function |
| Data consistency | Covered by happy path | Provider session reaches the Provider-only navigation surface |

Password reset, activation resend, logout, and long-term session persistence are separate PR-01 functions and are not silently folded into this login function.

## 5. Dataset Recipes

| Dataset ID | Revision | Scenario purpose | Builder reference | Retention marker |
| --- | --- | --- | --- | --- |
| `PR-01-DS-0001` | `v1` | Valid active Provider | `datasets.ts#buildProviderLoginDataset` | Run ID plus dataset ID |
| `PR-01-DS-0002` | `v1` | Missing username | `datasets.ts#buildProviderLoginDataset` | Run ID plus dataset ID |
| `PR-01-DS-0003` | `v1` | Missing password | `datasets.ts#buildProviderLoginDataset` | Run ID plus dataset ID |
| `PR-01-DS-0004` | `v1` | Both credentials empty | `datasets.ts#buildProviderLoginDataset` | Run ID plus dataset ID |
| `PR-01-DS-0005` | `v1` | Fresh synthetic unknown credentials | `datasets.ts#buildProviderLoginDataset` | Run ID plus dataset ID |
| `PR-01-DS-0006` | `v1` | Valid secondary Provider on Hairline Team route | `datasets.ts#buildProviderLoginDataset` | Run ID plus dataset ID |

Credential values remain in the credential registry/runtime environment and are never stored in this file, SQLite, artifacts, or terminal summaries.

## 6. Active Test Cases

All cases use revision `v1`, status `ACTIVE`, automation module `tests.spec.ts`, and the constitutional retry/evidence policy.

### `PR-01-TC-0001` — Active Provider successfully logs in

- **Category / priority:** Happy path, `P0`, smoke/affected/module/full.
- **Actions:** Open role selection, choose Provider, enter registered active Provider credentials, and submit.
- **Assertions:** Authentication returns HTTP `200`; route becomes `/`; `Dashboard` and `Provider Profile` navigation are visible.

### `PR-01-TC-0002` — Provider login requires a username

- **Category / priority:** Validation, `P1`, smoke/affected/module/full.
- **Actions:** Choose Provider, leave username empty, enter a non-submitted validation password, and submit.
- **Assertions:** Username-required message is visible; no authentication request is sent; route remains Provider login.

### `PR-01-TC-0003` — Provider login requires a password

- **Category / priority:** Validation, `P1`, smoke/affected/module/full.
- **Actions:** Choose Provider, enter a fresh synthetic username, leave password empty, and submit.
- **Assertions:** Password-required message is visible; no authentication request is sent; route remains Provider login.

### `PR-01-TC-0004` — Provider login reports both required fields when empty

- **Category / priority:** Validation and boundary, `P1`, smoke/affected/module/full.
- **Actions:** Choose Provider and submit with both credential fields empty.
- **Assertions:** Both required messages are visible; no authentication request is sent; route remains Provider login.

### `PR-01-TC-0005` — Unknown Provider credentials are rejected safely

- **Category / priority:** Negative, `P1`, smoke/affected/module/full.
- **Actions:** Choose Provider, enter fresh synthetic unknown credentials, and submit.
- **Assertions:** Authentication returns HTTP `403`; the generic rejection message is visible; no redirect or session occurs.

### `PR-01-TC-0006` — Provider credentials cannot authenticate as Hairline Team

- **Category / priority:** Permission / role, `P0`, smoke/affected/module/full.
- **Actions:** Choose Hairline Team, enter registered secondary Provider credentials, and submit.
- **Assertions:** Authentication returns HTTP `403`; the generic rejection message is visible; route remains Hairline Team login.

## 7. Runtime Evidence Requirements

- Apply one initial attempt plus three retries with at least five seconds between failures.
- Retain no screenshot or trace for an initial pass.
- Route every non-clean result to `NEEDS_HUMAN_REVIEW`.
- A negative case passes only when the expected rejection and absence of an authenticated transition are both observed.

## 8. Revision Log

| Revision | Date | Status | Reason | Approved by / authority | Originating result |
| --- | --- | --- | --- | --- | --- |
| `v1` | 2026-07-14 | Draft | Initial happy-path registration | Product Owner | None |
| `v1` | 2026-07-15 | Active | Happy path explicitly approved; five PRD-derived cases registered and activated after controlled pass | Product Owner plus Constitution v1.2 delegated authority | `RUN-20260714T215851Z-40eaa16c` |
| `v1` | 2026-07-15 | Active verified | Ordinary function command executed all six active cases with no draft override, review item, or retained artifact | Constitution v1.2 verification | `RUN-20260714T220554Z-028ca2ef` |

## 9. Registration Checklist

- [x] Product Owner approved the function boundary and canonical happy path.
- [x] Applicable source requirements were mapped without copying PRD narratives.
- [x] Every executable case has stable IDs, deterministic data, UI actions, assertions, and regression tiers.
- [x] All six executable cases completed controlled validation.
- [x] All six executable cases are `ACTIVE`.
- [x] Credentials, tokens, secrets, and real patient data are absent.
- [ ] Dedicated suspended and deactivated Provider test accounts are available.
- [ ] A dedicated removed-member test account is available.
- [ ] A safe lockout/reset and isolated-IP mechanism is available for throttling coverage.
