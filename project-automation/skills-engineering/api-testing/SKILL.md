---
name: api-testing
description: Test a SINGLE Hairline API endpoint with comprehensive reporting. Use for: (1) calling one specific endpoint and getting a detailed result, (2) investigating an issue at a single API level, (3) testing a specific scenario — happy path, edge case, error case, auth-boundary, or cross-tenant. Triggers on: "test endpoint", "call this API", "check response for", "what does [endpoint] return", "test single call", "investigate this endpoint", "call [X] endpoint". Does NOT run multi-step flows — for flows, use api-flow-testing instead.
---

# API Testing — Single Endpoint

Tests exactly one Hairline API endpoint per invocation. Returns a comprehensive report covering status, contract validation, state verification, anomalies, and backend cross-reference.

## Step 0: Upfront Input Collection

Ask ALL of the following before making any calls. Do not start execution until you have all answers.

**1. Which endpoint?** (name, path, or description of what you want to hit)

**2. Auth role?**
- `patient` / `provider` / `admin` / `none`

**3. Scenario type?**
- `happy-path` — valid complete data, expect success
- `edge-case` — boundary values, unusual but valid inputs (specify which)
- `error-case` — invalid data, missing fields, business rule violations (specify which)
- `auth-boundary` — wrong role, expired token, wrong profile_type (specify which)
- `cross-tenant` — Patient A using Patient B's IDs; testing IDOR (specify which)

**4. Test data:** After identifying the endpoint, run the test data selection workflow (see Test Data Management below) before asking anything else. Present the options to the user as part of this upfront phase.

Do not proceed to execution until all four items are resolved.

---

## Execution Model

**Always spawn a subagent for any Postman MCP tool invocation or HTTP request.** Never execute these in the main context.

- Subagent model: `haiku`
- Delegate to subagent: `runCollection`, `getCollectionRequest`, `getCollection`, `getCollectionFolder`, `getEnvironment`, and any direct HTTP calls
- Keep in main context: planning, data selection, analysis, report writing

**Pattern:**
1. Main agent resolves endpoint, auth, scenario, and test data
2. Main agent spawns subagent with a precise, self-contained prompt (endpoint details, token, body, what to capture)
3. Subagent executes and returns: status code, response headers, full response body, response time (ms)
4. Main agent produces the full report

---

## Authentication

Every authenticated request requires a valid token. Login first using credentials from `local-docs/testing-plans/testing-credentials/`.

```
POST {{HOST}}/auth/login
{ "email": "...", "password": "...", "profile_type": "patient|provider|admin" }
```

Login test scripts auto-set `PATIENT_TOKEN`, `PATIENT_ID`, `PROVIDER_TOKEN`, `PROVIDER_ID` in the Postman environment.

**Connection:**
- Collection ID: `33112351-a879f780-945c-4d62-8a0a-6432b86bb066`
- Environment ID: `33112351-abff0ede-b0ff-4e99-a7f1-aa27851b6656`

---

## Test Data Management

Test data is stored in `references/datasets.json`. Each entry is scoped to a specific endpoint + scenario type.

### Selection workflow (run during Step 0)

1. Read `references/datasets.json`
2. Filter entries by the target endpoint and scenario type
3. Present findings to the user:
   - **If matches found:** List them by name + description. Ask: reuse an existing one, or create a new one for variety?
   - **If no matches:** Inform the user, then offer to add a new dataset (see Adding a new dataset below)

### Adding a new dataset

When no matching data exists or the user wants a new one:

1. Fetch the endpoint's request structure:
   - First try Postman: `getCollectionRequest` with `populate: true`
   - If not in Postman: read the Form Request class at `main/hairline-backend/app/Http/Requests/`
2. Show the user the required fields, types, and validation rules
3. Propose a dataset payload that complies with the structure and fits the chosen scenario type
4. For edge/error/auth-boundary cases: propose data that deliberately triggers the target condition
5. Wait for user confirmation or amendments
6. On confirmation: append the new entry to `references/datasets.json` using the format below

### Dataset entry format

```json
{
  "id": "inquiry-happy-001",
  "endpoint": "POST /inquiries",
  "scenario": "happy-path",
  "description": "Standard inquiry with valid transplant area and hair photos",
  "body": {
    "transplant_area_id": "...",
    "notes": "..."
  },
  "file_refs": ["assets/sample-hair-photo.jpg"],
  "notes": "Requires active patient account. INQUIRY_ID will be captured."
}
```

### File uploads

For endpoints requiring image or file uploads, use assets from the `assets/` folder:
- `assets/sample-hair-photo.jpg` — default hair photo for inquiry creation
- `assets/sample-passport.png` — default passport for logistics flow

**If these files have not been populated yet:** warn the user and ask them to drop real JPG files into the `assets/` folder before running an upload-dependent test.

---

## Execution Steps

### Step 1: Locate the endpoint

1. Read [collection-map.md](references/collection-map.md) — search by keyword or path
2. If not found: grep `main/hairline-backend/routes/api.php` for the operation
3. If still not found: use Postman `getCollection` to browse the collection structure

### Step 2: Fetch full request details

Use `getCollectionRequest` with `populate: true` to retrieve URL, method, headers, body schema, and test scripts.

### Step 3: Capture pre-call state (state-changing endpoints only)

For endpoints that change entity status (create, update, accept, confirm, start, complete):
- Make a GET call first to capture current state of the relevant entity
- Record key field values (especially status fields) before the mutation

### Step 4: Execute

Spawn subagent. Provide: full endpoint details, auth token, request body from selected dataset, any dynamic values (IDs from context, env variables).

Subagent must return: HTTP status code, response headers (especially Content-Type), full response body, response time in ms.

### Step 5: Produce the report

```
## API Call Report — [METHOD] [endpoint]

**Scenario:** [scenario type]
**Dataset used:** [dataset id or "ad-hoc"]

### Request
- Method + URL: [value]
- Auth: [role] ([token prefix e.g. Bearer eyJ...])
- Payload: [body sent]

### Response
- Status: [actual] (expected: [expected]) ✓/✗
- Time: [N]ms
- Body: [full body or summary]

### Contract Validation
- [✓/✗] [field] — expected [type/value] → got [actual]
- ...

### State Verification
- Before: [state of entity before call, or N/A]
- After: [state of entity after call]

### Artifacts Captured
- [TOKEN_NAME / ID_NAME]: [value] — available for downstream use
- ...

### Anomalies
- [Unexpected nulls, wrong types, missing fields, wrong status codes]

### Backend Reference
- Route: [HTTP method + path]
- Controller: [ClassName@method]
- Relevant note: [brief note if investigation is warranted]

### Suggested Next Steps
- [Actionable items based on findings]
```

### Step 6: Backend analysis (errors and anomalies only)

**4xx/5xx responses:**
1. Read the error message in the response body
2. Find the controller at `main/hairline-backend/app/Http/Controllers/`
3. Read the Form Request validation rules
4. Report: what failed, what valid input looks like, suggested fix

**Data mismatch or missing fields:**
1. Check Eloquent model relationships at `main/hairline-backend/app/Models/`
2. Verify auth scope (patient accessing provider-only data, etc.)
3. Report: what is wrong and where the discrepancy originates

---

## Multi-Tenant Scenario Notes

Hairline has three distinct roles (Patient, Provider, Admin) each with its own permission boundary. For auth-boundary and cross-tenant scenario types, use these patterns:

| Scenario | What to do |
|----------|-----------|
| `auth-boundary: wrong role` | Use a Provider token on a Patient-only endpoint; expect 403 |
| `auth-boundary: no token` | Omit Authorization header; expect 401 |
| `auth-boundary: wrong profile_type` | Login with correct creds but wrong profile_type; expect 401/403 |
| `cross-tenant: IDOR` | Use Patient A's token but supply Patient B's resource ID; expect 403 or 404 |
| `cross-tenant: provider scope` | Use Provider A's token on Provider B's inquiry; expect 403 |

Always document the expected outcome in the report's Contract Validation section when running these scenarios.

---

## Endpoint Discovery

When the user describes a scenario but doesn't know which endpoint to call:

1. Read [collection-map.md](references/collection-map.md) — search by keyword
2. Grep `main/hairline-backend/routes/api.php` for the operation name or resource
3. Check Postman collection structure with `getCollection`
4. Cross-reference the controller to confirm the endpoint does what the user expects

For endpoints not yet in the Postman collection: construct the request from the route definition in `api.php` and the corresponding controller method.

---

## References

- [collection-map.md](references/collection-map.md) — Full endpoint-to-backend-route mapping
- [datasets.json](references/datasets.json) — Test data catalogue
- Test credentials: `local-docs/testing-plans/testing-credentials/` (patient-accounts.md, provider-accounts.md)
- Backend routes: `main/hairline-backend/routes/api.php`
- Controllers: `main/hairline-backend/app/Http/Controllers/`
- Models: `main/hairline-backend/app/Models/`
- Form Requests: `main/hairline-backend/app/Http/Requests/`
