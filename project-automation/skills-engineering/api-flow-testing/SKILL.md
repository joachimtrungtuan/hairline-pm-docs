---
name: api-flow-testing
description: Run a named multi-step Hairline API testing flow end-to-end. Use when the user wants to test a complete business flow across multiple API calls — e.g., "test the inquiry creation flow", "run the quote acceptance flow", "test patient registration end-to-end", "test the full treatment journey". Each step is executed using api-testing skill logic. Looks up the flow in a registered dictionary — if the flow is not yet registered, halts and directs to api-flow-register first. Triggers on: "test the [X] flow", "run the [X] flow", "end-to-end test", "test complete journey", "multi-step test", "flow testing".
---

# API Flow Testing

Executes multi-step Hairline API testing flows end-to-end. Each individual step follows the `api-testing` single-endpoint pattern. Flow definitions are stored in `references/flow-dictionary.md`.

## Step 0: Upfront Input Collection

Ask ALL of the following before any execution. Do not start until all answers are resolved.

**1. Flow name?** (e.g., "inquiry creation", "quote acceptance", "patient registration")

**2. Scenario variant?**
- `happy-path` — standard, expected-success execution
- `edge-case` — specify which edge scenario
- `error-path` — specify which error condition to trigger
- `auth-boundary` — specify which role/permission boundary to probe
- `cross-tenant` — specify which cross-tenant scenario

**3. Starting state?**
- Does prerequisite data already exist? If yes, provide the relevant IDs (patient ID, inquiry ID, etc.)
- Or does the flow need to create everything from scratch?

**4. Per-step overrides?**
- Any specific values to use at a particular step, or use dictionary defaults for all?

**5. Test data:** After confirming the flow steps (from the dictionary), run the test data selection workflow for each step that needs a request body. Present all options upfront before starting execution. See Test Data below.

Do not proceed to execution until all five items are resolved.

---

## Execution Logic

### Phase 1: Flow lookup

Read `references/flow-dictionary.md`. Look up the flow by name (case-insensitive, partial match acceptable).

**If not found:**
- Stop. Do not attempt to improvise the flow.
- Tell the user: "The flow '[name]' is not registered in the dictionary."
- Instruct: "Run `api-flow-register` to research, propose, and register it. Then come back and re-run this flow."

**If found:** load the step sequence and continue to Phase 2.

### Phase 2: Test data coordination

Before starting any API calls, coordinate test data for all steps upfront:

For each step in the flow that requires a request body:
1. Check `api-testing/references/datasets.json` for entries matching that step's endpoint + scenario type
2. If matches found: present them and ask — reuse an existing one, or create a new one for variety?
3. If no match: offer to add a new dataset using the `api-testing` dataset addition workflow (research the endpoint's required structure, propose a compliant payload, confirm with user, write to datasets.json)

Collect all test data decisions before running any steps. Do not interrupt mid-flow to ask about data.

### Phase 3: Step-by-step execution

For each step in the sequence, apply the `api-testing` execution pattern:

1. Locate and fetch the endpoint details (collection-map or Postman `getCollectionRequest`)
2. For state-changing steps: capture state before the call
3. Spawn a subagent (`haiku` model) to execute the call
4. Capture tokens/IDs from the response and pass them to subsequent steps
5. Verify state transition where applicable
6. Note role switches explicitly (see Multi-Tenant Role Tracking below)

**Subagent delegation:** All Postman MCP calls and HTTP requests go to the subagent. Planning, state tracking, and report writing stay in the main context.

**Connection:**
- Collection ID: `33112351-a879f780-945c-4d62-8a0a-6432b86bb066`
- Environment ID: `33112351-abff0ede-b0ff-4e99-a7f1-aa27851b6656`

**On discrepancy detected mid-run:**
- A step fails in an unexpected way not covered by the flow definition
- Or the actual flow requires steps not listed in the dictionary entry

When this happens:
1. Pause execution
2. Report to the user: what was expected vs what actually happened
3. Ask: continue with a manual workaround, or trigger `api-flow-register` to update the flow definition first?
4. Wait for the user's decision before continuing

### Phase 4: Final summary

After all steps complete, present:

```
## Flow Test Summary — [Flow Name]

**Scenario:** [variant]
**Overall result:** PASS / PARTIAL / FAIL

| # | Endpoint                   | Role     | Status          | Result                       |
|---|----------------------------|----------|-----------------|------------------------------|
| 1 | POST /auth/login           | —        | 200 ✓           | PATIENT_TOKEN captured       |
| 2 | POST /inquiries            | Patient  | 201 ✓           | Inquiry ID: abc-123          |
| 3 | POST /auth/login           | —        | 200 ✓           | PROVIDER_TOKEN captured      |
| 4 | GET /inquiries/queue       | Provider | 200 ✓           | Inquiry visible              |

### Issues Found
- [Step N]: [description of anomaly, failure, or discrepancy]

### Artifacts
- PATIENT_ID: [value]
- INQUIRY_ID: [value]
- QUOTE_ID: [value]
- (list all captured IDs and tokens)

### Suggested Next Steps
- [Actions based on findings]
```

---

## Multi-Tenant Role Tracking

Hairline has three roles with distinct permission boundaries: Patient, Provider, Admin. Flows frequently span multiple roles. Track the active role at every step and annotate switches explicitly.

When the active role changes between steps, note:
```
[Role switch: Patient → Provider]
```

For auth-boundary and cross-tenant scenario variants, label the probe clearly:
```
[Auth probe: Provider token on Patient-only endpoint — expect 403]
[Cross-tenant probe: Patient A token with Patient B's inquiry ID — expect 403/404]
```

---

## References

- [flow-dictionary.md](references/flow-dictionary.md) — Registered flow definitions; read during Phase 1 flow lookup
- `api-testing` skill — single-endpoint execution and reporting logic; applied at every step in Phase 3
- `api-testing/references/datasets.json` — shared test data catalogue; read during Phase 2 test data coordination
- `api-testing/references/collection-map.md` — endpoint-to-route mapping; read during Phase 3 per-step execution when locating endpoints
- Test credentials: `local-docs/testing-plans/testing-credentials/`
- Backend routes: `main/hairline-backend/routes/api.php` — read only during error investigation in Phase 3
- Controllers: `main/hairline-backend/app/Http/Controllers/` — read only during error investigation in Phase 3
