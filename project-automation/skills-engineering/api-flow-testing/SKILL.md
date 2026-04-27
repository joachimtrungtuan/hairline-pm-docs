---
name: api-flow-testing
description: >-
  Run a named multi-step Hairline API testing flow end-to-end. Use when the
  user wants to test a complete business flow across multiple API calls — e.g.,
  "test the inquiry creation flow", "run the quote acceptance flow", "test
  patient registration end-to-end", "test the full treatment journey". Each
  step uses api-testing endpoint profiles and execution logic. Looks up
  migrated flows through flow-index.md and flow-profiles/ with
  flow-dictionary.md as legacy fallback. Triggers on: "test the [X] flow",
  "run the [X] flow", "end-to-end test", "test complete journey",
  "multi-step test", "flow testing".
---

# API Flow Testing

Executes multi-step Hairline API testing flows end-to-end. Each individual step follows the `api-testing` single-endpoint pattern. Migrated flow definitions are indexed in `references/flow-index.md` and stored in `references/flow-profiles/`. `references/flow-dictionary.md` is legacy fallback only.

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

**5. Test data:** After confirming the flow steps from the flow profile, run the test data selection workflow for each step that needs a request body. Present all options upfront before starting execution. See Test Data below.

Do not proceed to execution until all five items are resolved.

---

## Execution Logic

### Phase 1: Flow lookup

1. Read `references/flow-index.md`.
2. Look up the flow by name, purpose, or tag (case-insensitive, partial match acceptable).
3. Open only the matching file in `references/flow-profiles/`.
4. Open each endpoint profile referenced by the flow from `api-testing/references/endpoint-profiles/`.
5. If the flow is not in `flow-index.md`, check `references/flow-dictionary.md` as legacy fallback.

**If not found:**
- Stop. Do not attempt to improvise the flow.
- Tell the user: "The flow '[name]' is not registered in the dictionary."
- Instruct: "Run `api-flow-register` to research, propose, and register it. Then come back and re-run this flow."

**If found:** load the step sequence and continue to Phase 2.

### Phase 2: Test data coordination

Before starting any API calls, coordinate test data for all steps upfront:

For each step in the flow that requires a request body:
1. Read that step's endpoint profile for required fields and dynamic resolvers.
2. Check `api-testing/references/datasets.json` for entries matching that step's endpoint + scenario type.
3. If matches found: present them and ask — reuse an existing one, or create a new one for variety?
4. If no match: offer to add a new dataset using the `api-testing` dataset addition workflow (research the endpoint's required structure, propose a compliant payload, confirm with user, write to datasets.json).
5. For file/image upload steps, use `api-testing/assets/` files referenced by the endpoint profile or dataset unless the user explicitly provides a different file.

Collect all test data decisions before running any steps. Do not interrupt mid-flow to ask about data.

### Phase 3: Step-by-step execution

For each step in the sequence, apply the `api-testing` execution pattern:

1. Use the endpoint profile referenced by the flow step.
2. Run prerequisite resolver endpoints before payload construction when the flow or endpoint profile requires them.
3. For state-changing steps: capture state before the call.
4. Spawn a subagent (`haiku` model) to execute the call.
5. Capture tokens/IDs from the response and pass them to subsequent steps.
6. Verify state transition where applicable.
7. Note role switches explicitly (see Multi-Tenant Role Tracking below).

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

**Learning capture:** After any successful workaround or confirmed discrepancy, propose updates to the relevant flow profile, endpoint profile, and index row. Write them only after user confirmation.

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

- [flow-index.md](references/flow-index.md) — First-pass flow lookup; read during Phase 1
- `references/flow-profiles/` — Migrated flow definitions; open only the matched profile
- [flow-dictionary.md](references/flow-dictionary.md) — Legacy flow definitions; fallback while migration is incomplete
- `api-testing` skill — single-endpoint execution and reporting logic; applied at every step in Phase 3
- `api-testing/references/datasets.json` — shared test data catalogue; read during Phase 2 test data coordination
- `api-testing/references/endpoint-index.md` — endpoint profile lookup and concise live notes
- `api-testing/references/endpoint-profiles/` — endpoint-level fields, resolvers, response expectations, and live notes
- `api-testing/references/collection-map.md` — endpoint-to-route mapping; fallback when a profile is missing
- Test credentials: `local-docs/testing-plans/testing-credentials/`
- Backend routes: `main/hairline-backend/routes/api.php` — read only during error investigation in Phase 3
- Controllers: `main/hairline-backend/app/Http/Controllers/` — read only during error investigation in Phase 3
