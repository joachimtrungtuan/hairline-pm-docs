---
name: api-flow-register
description: Research, propose, confirm, and register API testing flow definitions into the api-flow-testing flow dictionary. Use when: (1) api-flow-testing encounters an unknown flow name and cannot proceed, (2) a flow needs updating after a mid-run discrepancy is detected, (3) the user explicitly asks to register, add, or update a flow in the dictionary. Triggers on: "register this flow", "add flow to dictionary", "update flow definition", "flow not found — register it", "document this flow", "record this testing flow", "the flow needs updating".
---

# API Flow Register

Researches the Hairline backend and PRDs, proposes a step-by-step testing flow, confirms with the user, then writes the flow definition into `api-flow-testing/references/flow-dictionary.md`.

## Step 0: Upfront Input Collection

Ask ALL of the following before doing any research or writing. Do not proceed until all answers are resolved.

**1. Flow name?** (as it should appear in the dictionary, used for future lookups)

**2. Trigger type?**
- `new` — first-time registration of a flow that doesn't exist in the dictionary yet
- `update` — updating an existing flow entry (if update: describe what changed or what the discrepancy was)

**3. Starting conditions?**
- What state must exist before step 1? (e.g., "an active patient account exists", "an accepted quote exists", "starts from scratch")

**4. Scenario coverage?**
- Register happy-path steps only to start?
- Or also include known edge case and error path variants now?

Do not proceed to research until all four items are resolved.

---

## Execution

### Phase 1: Research (new registrations)

Using the flow name and starting conditions as context, investigate the following sources:

1. **Backend routes** — Read `main/hairline-backend/routes/api.php` to identify all routes involved in this flow
2. **Controllers** — Read the relevant controller methods to understand what each endpoint does, what inputs it requires, and what state it changes
3. **Form Requests** — Read the Form Request classes at `main/hairline-backend/app/Http/Requests/` to capture validation rules and required fields
4. **Eloquent models** — Read relevant models at `main/hairline-backend/app/Models/` to understand status fields, relationships, and state transitions
5. **PRDs / FRs** — Search `local-docs/project-requirements/functional-requirements/` for the relevant feature requirement document(s) to cross-check business intent

Goal: trace the complete sequence of API calls that constitute this flow — which role performs each step, what input is needed, and what state is expected before and after.

### Phase 2: Research (updates)

For update triggers:
1. Read the existing flow entry from `api-flow-testing/references/flow-dictionary.md`
2. Read the discrepancy description provided in Step 0
3. Investigate only the affected steps (routes, controllers, Form Requests) to understand what changed
4. Identify the specific steps that need modification

### Phase 3: Propose the flow

Present the proposed step sequence to the user. **Do not write to the dictionary yet.**

Use the proposal format from [formats.md](references/formats.md). For update proposals, show only the changed steps with a before/after diff.

**Wait for explicit user confirmation before writing anything to the dictionary.**

Accept amendments. If the user modifies steps, update the proposal inline and ask for re-confirmation before writing.

---

### Phase 4: Write to the dictionary

On user confirmation, write to `api-flow-testing/references/flow-dictionary.md`.

**New flow:** append the entry after the last existing entry (or replace the "_No flows registered yet._" placeholder if it's the first).

**Update:** find the existing entry by flow name and replace it in place. Bump the `Last updated` date.

Use the dictionary entry format from [formats.md](references/formats.md).

---

### Phase 5: Confirm and return

After writing:
1. Tell the user the flow is now registered under the name they provided
2. If triggered from `api-flow-testing` (because a flow was not found): instruct the user to re-run the flow test — it will now be found in the dictionary

---

## References

- [formats.md](references/formats.md) — proposal and dictionary entry formats; read during Phase 3 and Phase 4
- `api-flow-testing/references/flow-dictionary.md` — the dictionary this skill writes to; read during Phase 2 (updates) and Phase 4
- `main/hairline-backend/routes/api.php` — backend route list; read during Phase 1 research
- `main/hairline-backend/app/Http/Controllers/` — controller methods; read during Phase 1 research
- `main/hairline-backend/app/Http/Requests/` — Form Request validation rules; read during Phase 1 research
- `main/hairline-backend/app/Models/` — Eloquent models for state transitions; read during Phase 1 research
- `local-docs/project-requirements/functional-requirements/` — PRDs/FRs for business intent; search during Phase 1 research
