---
name: api-testing
description: Test Hairline API endpoints via Postman MCP during manual testing sessions. Use when the user needs to (1) investigate API issues — error codes, data mismatches, missing responses, (2) test a specific flow or endpoint, (3) push a flow forward by calling backend APIs manually, (4) check what data the server is returning for a given request. Triggers on phrases like "test API", "call endpoint", "check response", "investigate API issue", "run flow", "test the backend", "API testing", "Postman test", "what does the server return".
---

# API Testing

Test Hairline backend endpoints via the Postman MCP to investigate issues and push flows forward during manual testing.

## Execution Model

**Always spawn a subagent for any API call, HTTP request, or Postman MCP tool invocation.** Do not execute these directly in the main context.

Rationale:
- Keeps response payloads out of the main context window
- Uses a low-cost model for mechanical work, saving tokens

Agent configuration:
- **Claude**: use `haiku` model (pass `model: "haiku"` to the Agent tool)
- **Other agents**: use the lowest available thinking-effort model

What to delegate to the subagent:
- All `runCollection`, `getCollectionRequest`, `getCollection`, `getCollectionFolder`, `getEnvironment` Postman MCP calls
- Any direct HTTP request execution

What to keep in the main context:
- Planning, analysis, root-cause investigation, and final reporting (Steps 1, 4, 5)

**Pattern:**
1. Main agent plans which endpoints to call and with what parameters
2. Main agent spawns a subagent with a precise, self-contained prompt describing exactly what to call
3. Subagent executes the calls and returns structured results (status, body, key fields)
4. Main agent receives the summary and continues analysis

## Workflow

### Step 1: Understand the request

Determine what the user needs:

- **Test a specific flow** (e.g., "test the quote creation flow") → Read [flow-guides.md](references/flow-guides.md) for step sequence
- **Test a specific endpoint** (e.g., "call the login endpoint") → Read [collection-map.md](references/collection-map.md) for endpoint details
- **Investigate an issue** (e.g., "quotes not showing up") → Identify which endpoints are involved, then test them

### Step 2: Authenticate

Every flow starts with login. Use credentials from `local-docs/testing-plans/testing-credentials/`:

**Patient Login:**
```json
POST {{HOST}}/auth/login
{
  "email": "<from patient-accounts.md>",
  "password": "<from patient-accounts.md>",
  "profile_type": "patient"
}
```

**Provider Login:**
```json
POST {{HOST}}/auth/login
{
  "email": "<from provider-accounts.md>",
  "password": "<from provider-accounts.md>",
  "profile_type": "provider"
}
```

**Admin Login:**
```json
POST {{HOST}}/auth/login
{
  "email": "<admin email>",
  "password": "<admin password>",
  "profile_type": "admin"
}
```

Use the Postman MCP `runCollection` tool with the Hairline environment to execute requests. The login test scripts auto-set `PATIENT_TOKEN`, `PATIENT_ID`, `PROVIDER_TOKEN`, `PROVIDER_ID` in the environment.

**Connection details:**
- Collection ID: `33112351-a879f780-945c-4d62-8a0a-6432b86bb066`
- Environment ID: `33112351-abff0ede-b0ff-4e99-a7f1-aa27851b6656`

### Step 3: Execute and record

For each endpoint call:

1. **Fetch the request details** from Postman using `getCollectionRequest` with `populate: true`
2. **Review the request** — check URL, method, headers, body; fill in dynamic values (IDs, tokens)
3. **Execute** via `runCollection` or guide the user to call it
4. **Record the response** — capture full response body, status code, headers
5. **Present a summary** to the user:
   - Status code + message
   - Key data points relevant to the investigation
   - Any anomalies (unexpected nulls, wrong status, missing fields)

### Step 4: Analyze (for investigation tasks)

When the user reports an issue, follow this analysis pattern:

**For error responses (4xx/5xx):**
1. Check the HTTP status code meaning
2. Read the error message in the response body
3. Cross-reference with the backend controller — find the controller in `main/hairline-backend/app/Http/Controllers/` using the route from [collection-map.md](references/collection-map.md)
4. Check validation rules in the corresponding Form Request
5. Report: what went wrong, what input is expected, suggested fix

**For data mismatch / missing data:**
1. Check the response structure against what the frontend/mobile expects
2. Look at the Eloquent model relationships in `main/hairline-backend/app/Models/`
3. Check if the data exists at all (call related endpoints to verify)
4. Check if auth scope is correct (patient seeing provider-only data, etc.)
5. Report: what data is missing/wrong, where the discrepancy originates

**For empty or meaningless responses:**
1. Verify the entity exists (call a GET endpoint with the ID)
2. Check if the status/state is correct for the operation
3. Verify the authenticated user has permission to see the data
4. Report: why the response is empty and what prerequisites are missing

### Step 5: Report findings

Present results in this format:

```
## API Test Result

**Endpoint:** POST /auth/login
**Status:** 200 OK | 401 Unauthorized | 422 Validation Error
**Time:** (if available)

### Response Summary
- Key field 1: value
- Key field 2: value

### Issues Found (if any)
- Issue description
- Root cause (from backend code analysis)
- Suggested action

### Tokens/IDs Captured
- PATIENT_TOKEN: Bearer eyJ...
- PATIENT_ID: uuid-here
```

When testing a multi-step flow, present a summary table at the end:

```
| # | Endpoint | Status | Result |
|---|----------|--------|--------|
| 1 | Patient Login | 200 | Token captured |
| 2 | Create Inquiry | 201 | Inquiry ID: xxx |
| 3 | Verify Distribution | 200 | 2 providers matched |
```

## Ad-Hoc Requests

The predefined flows in [flow-guides.md](references/flow-guides.md) cover the main journeys but are not exhaustive. When the user has an ad-hoc request that doesn't match a predefined flow:

1. **Listen to the user's goal** — what are they trying to achieve or investigate?
2. **Discover endpoints dynamically** — use the collection map, backend routes, and Postman MCP to find relevant endpoints
3. **Build a custom sequence** — chain the right endpoints together on the fly
4. **Apply the same record-and-analyze pattern** from Steps 3-5 above

Examples of ad-hoc requests:
- "Check if this patient has any active discounts" → find discount endpoints, call with patient ID
- "Why is this provider not receiving inquiries?" → check provider profile, distribution config, inquiry matching
- "Manually change this quote to confirmed status" → find the status update endpoint, call with correct params
- "What does the aftercare data look like for quote X?" → call aftercare detail endpoints with the quote ID
- "Test this new endpoint that was just deployed" → get the route from the backend code, construct the request manually

For truly novel endpoints not in the Postman collection yet, construct the request from the backend route definition in `main/hairline-backend/routes/api.php` and the corresponding controller.

## Endpoint Discovery

When the user describes a scenario but doesn't know which endpoint to use:

1. Read [collection-map.md](references/collection-map.md) — search by keyword
2. Search the backend routes in `main/hairline-backend/routes/api.php` — grep for the operation
3. Check the Postman collection structure using `getCollection` MCP tool
4. Cross-reference the controller to confirm the endpoint does what the user expects

## Browsing Postman Requests

Use these Postman MCP tools:

| Tool | When |
|------|------|
| `getCollection` | Browse collection structure, find request IDs |
| `getCollectionRequest` (with `populate: true`) | Get full request details (URL, body, headers, test scripts) |
| `getCollectionFolder` | Browse requests within a specific folder |
| `getEnvironment` | Check current environment variable values |
| `runCollection` | Execute requests against the live server |

## References

- [collection-map.md](references/collection-map.md) — Full endpoint-to-backend-route mapping for the entire Hairline Mobile collection
- [flow-guides.md](references/flow-guides.md) — 13 step-by-step testing flows covering the complete patient journey
- Test credentials: `local-docs/testing-plans/testing-credentials/` (patient-accounts.md, provider-accounts.md)
- Backend routes: `main/hairline-backend/routes/api.php`
- Controllers: `main/hairline-backend/app/Http/Controllers/`
- Models: `main/hairline-backend/app/Models/`
