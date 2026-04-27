---
name: api-flow-register
description: >-
  Research, propose, confirm, and register Hairline API testing flow profiles
  and related endpoint profiles. Use when: (1) api-flow-testing encounters an
  unknown flow name and cannot proceed, (2) a flow or endpoint profile needs
  updating after a mid-run discrepancy, (3) the user explicitly asks to
  register, add, update, or document a flow or endpoint profile. Triggers on:
  "register this flow", "add flow to dictionary", "update flow definition",
  "document this flow", "record this testing flow", "the flow needs updating",
  "add endpoint profile", "update endpoint profile".
---

# API Flow Register

Researches the Hairline backend and PRDs, proposes a step-by-step testing flow plus any required endpoint profile updates, confirms with the user, then writes flow profiles under `api-flow-testing/references/flow-profiles/` and endpoint profiles under `api-testing/references/endpoint-profiles/`.

## Step 0: Upfront Input Collection

Ask ALL of the following before doing any research or writing. Do not proceed until all answers are resolved.

**1. Flow name?** (as it should appear in the dictionary, used for future lookups)

**2. Trigger type?**
- `new` — first-time registration of a flow that doesn't exist in the dictionary yet
- `update` — updating an existing flow entry (if update: describe what changed or what the discrepancy was)
- `endpoint-update` — updating or creating endpoint profile details without changing a flow

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

Also identify endpoint-level knowledge that belongs in endpoint profiles:
- Required/optional fields
- Dynamic ID resolvers
- Response captures
- Auth scope and role boundaries
- State effects
- Live route quirks or wrong endpoints to avoid

### Phase 2: Research (updates)

For update triggers:
1. Read `api-flow-testing/references/flow-index.md` and the relevant flow profile if migrated.
2. If not migrated, read the existing flow entry from `api-flow-testing/references/flow-dictionary.md`.
3. Read `api-testing/references/endpoint-index.md` and the affected endpoint profile.
4. Read the discrepancy description provided in Step 0.
5. Investigate only the affected steps (routes, controllers, Form Requests) to understand what changed.
6. Identify the specific flow profile, endpoint profile, and index rows that need modification.

For endpoint-only updates:
1. Read `api-testing/references/endpoint-index.md`.
2. Read the affected endpoint profile if it exists.
3. Read the discrepancy description provided in Step 0.
4. Investigate only the affected endpoint (routes, controllers, Form Requests) to understand what changed.
5. Identify the endpoint profile and index row changes needed.

For file/image upload endpoints, document the default bundled asset to use from `api-testing/assets/` and the exact multipart field names. Do not require future runs to rediscover sample upload files.

### Phase 3: Propose the flow

Present the proposed step sequence and endpoint profile changes to the user. **Do not write yet.**

Use the proposal format from [formats.md](references/formats.md). For update proposals, show only the changed steps with a before/after diff.

**Wait for explicit user confirmation before writing anything to the dictionary.**

Accept amendments. If the user modifies steps, update the proposal inline and ask for re-confirmation before writing.

---

### Phase 4: Write profiles and indexes

On user confirmation, write only the approved files.

**New flow:** create `api-flow-testing/references/flow-profiles/<flow-name>.md` and add a row to `api-flow-testing/references/flow-index.md`.

**Flow update:** update the flow profile and its row in `flow-index.md`. If the flow still only exists in `flow-dictionary.md`, either migrate it to a profile or patch the legacy entry only when the user requests that.

**Endpoint profile:** create or update `api-testing/references/endpoint-profiles/<method-path>.md` and add/update the row in `api-testing/references/endpoint-index.md`.

Use the profile formats from [formats.md](references/formats.md).

---

### Phase 5: Confirm and return

After writing:
1. Tell the user which flow and endpoint profiles were created or updated.
2. If triggered from `api-flow-testing` (because a flow was not found): instruct the user to re-run the flow test — it will now be found through `flow-index.md`.

---

## References

- [formats.md](references/formats.md) — proposal, flow profile, and endpoint profile formats; read during Phase 3 and Phase 4
- `api-flow-testing/references/flow-index.md` — flow lookup index this skill updates
- `api-flow-testing/references/flow-profiles/` — flow profiles this skill creates/updates
- `api-flow-testing/references/flow-dictionary.md` — legacy flow dictionary; read only for unmigrated flows
- `api-testing/references/endpoint-index.md` — endpoint lookup index this skill updates
- `api-testing/references/endpoint-profiles/` — endpoint profiles this skill creates/updates
- `main/hairline-backend/routes/api.php` — backend route list; read during Phase 1 research
- `main/hairline-backend/app/Http/Controllers/` — controller methods; read during Phase 1 research
- `main/hairline-backend/app/Http/Requests/` — Form Request validation rules; read during Phase 1 research
- `main/hairline-backend/app/Models/` — Eloquent models for state transitions; read during Phase 1 research
- `local-docs/project-requirements/functional-requirements/` — PRDs/FRs for business intent; search during Phase 1 research
