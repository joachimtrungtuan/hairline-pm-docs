---
description: Update a specific checklist row (Module+FR) by deriving core subflows from the FR PRD, cross-checking client transcriptions, and validating implementation progress in the codebase.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Required Inputs (Do Not Proceed Without These)

This prompt checks progress for exactly **one** `(MODULE_CODE, FR_CODE)` pair at a time.

The user must provide:

1. **Checklist file path** (the progress checklist to update)
2. **Module code** (e.g., `P-01`, `PR-02`, `A-04`, `S-03`)
3. **FR code** (e.g., `FR-001`, `FR-007B`)

If **ANY** of these is missing:

- **DO NOT** proceed with checking.
- Ask the user to re-confirm **all three** (checklist path + module code + FR code) in one message.

## Hard Rules

- **Row scope rule**: Each checklist row represents exactly one tenant context for a `(MODULE_CODE, FR_CODE)` pair. Do not mix tenants or modules.
- **Section integrity rule**: When reading the FR PRD, process sections strictly one-by-one; do not combine sections.
- **File rule**: Do **NOT** create any new files in this prompt. Only update the checklist file itself.
- If the user wants task generation, point them to: `local-docs/task-prompt/create-implementation-tasks.md`.

## Outline

1. Confirm inputs and locate the exact checklist row
2. Scan FR PRD structure (headers only)
3. Derive the core subflow list (section-by-section)
4. Cross-check the core subflow list with client transcriptions
5. Reconcile the checklist subflow items (append/update/remove)
6. Verify progress item-by-item in code (existence + correctness)
7. Compute progress % and update the checklist row

## Execution Flow

### Step 0: Todo Tracking (Mandatory)

**MUST** create and maintain a todo list so the agent stays on track and does not stray.

Create initial todos similar to:

1. Parse inputs (checklist + module + FR)
2. Locate matching checklist row
3. Locate FR PRD and extract structure
4. Analyze PRD sections one-by-one
5. Cross-check with transcriptions
6. Reconcile checklist subflow items
7. Verify each item in code (FE/BE)
8. Compute progress % and update row
9. Final consistency check and summary

### Step 1: Parse Inputs and Load Required Files

**MUST** extract from `$ARGUMENTS` or user prompt:

1. `CHECKLIST_FILE` (required)
2. `MODULE_CODE` (required)
3. `FR_CODE` (required)

**CRITICAL**: If only `MODULE_CODE` or only `FR_CODE` is provided, ask the user to provide the missing one and **re-confirm both** before proceeding.

**MUST** load these files (use absolute paths; convert relative paths to absolute):

1. `CHECKLIST_FILE` - Checklist to update - **REQUIRED**
2. `.specify/memory/constitution.md` - Module code definitions and architecture - **REQUIRED**
3. `local-docs/project-requirements/system-prd.md` - System-level requirements and FR definitions - **REQUIRED**
4. `local-docs/project-requirements/transcriptions/*.txt` - Client requirements (cross-check intent) - **REQUIRED**
5. **FR PRD** for `FR_CODE`: `local-docs/project-requirements/functional-requirements/fr###-*/prd.md` - **REQUIRED**

### Step 2: Determine Verification Scope From `MODULE_CODE`

**CRITICAL**: Scope depends on module tenant:

- **Patient (P-*)**:
  - **Flutter app frontend**: `main/hairline-app/`
  - **Backend API**: `main/hairline-backend/`
- **Provider (PR-*)**:
  - **Web frontend**: `main/hairline-frontend/`
  - **Backend API**: `main/hairline-backend/`
- **Admin (A-*)**:
  - **Web frontend**: `main/hairline-frontend/`
  - **Backend API**: `main/hairline-backend/`
- **Shared Services (S-*)**:
  - **Backend only**: `main/hairline-backend/`

### Step 3: Locate the Exact Checklist Row (Module + FR)

**MUST** find the table row in `CHECKLIST_FILE` matching:

- The exact `MODULE_CODE` cell (e.g., `P-02`)
- A Functional Requirements cell that contains `FR_CODE` (e.g., `FR-005`)

If no row matches, ask the user to confirm:

- The correct `MODULE_CODE`
- The correct `FR_CODE`
- Whether the checklist file is the correct version

If multiple rows match, treat them as separate tenants/contexts and ask the user which one to update (do not merge rows).

### Step 4: Status Symbols and Progress Calculation

Status definitions:

- ✅ **Completed** (≥90%): Fully implemented, functional, matches PRD, no critical bugs
- 🟨 **Partially Implemented** (≥50%): Core functionality exists but missing edge cases, validation, or non-critical features
- 🟥 **Not Yet Implemented** (<50%): Missing or mostly stubbed

Progress % calculation (for the row):

- Assign scores per item: ✅ = 1.0, 🟨 = 0.5, 🟥 = 0.0
- Progress % = `round( (sum(scores) / item_count) * 100 )`
- **Preserve** any additional markers already used in the checklist text (e.g., `⏳`) unless the user explicitly asks to change them.

### Step 5: Derive Core Subflows From the FR PRD (Section-By-Section)

This step produces the “analysis subflow list” for the specified `(MODULE_CODE, FR_CODE)` pair.

#### 5.1 Scan PRD Structure First (Headers Only)

- Locate the PRD file for `FR_CODE` (glob `local-docs/project-requirements/functional-requirements/fr###-*/prd.md`)
- Extract section headers (H2) without loading full content (e.g., `rg -n "^## " prd.md`)
- Add one todo per section and process in order

#### 5.2 Process Each PRD Section One-By-One (Integrity Rule)

For each section (in order):

1. Load only that section’s content (bounded by header line numbers)
2. Read the section once to understand intent and identify the main content
3. Extract candidate subflows/features:
   - Workflows / steps
   - Screens / UI behaviors
   - Core business requirements that must exist for the feature to work
4. Keep only items relevant to the specified `MODULE_CODE` tenant
5. Discard the section content before moving to the next section

At the end, produce a concise **core subflow list**:

- The minimum set of items required for the module+FR to work end-to-end
- Written in checklist-item style (short, testable)

### Step 6: Cross-Check Core Subflows Against Client Transcriptions

For each derived subflow item:

- Search `local-docs/project-requirements/transcriptions/*.txt` for supporting evidence
- Confirm it aligns with client intent (and isn’t contradicted elsewhere)
- If transcriptions introduce a must-have item missing from PRD, include it in the analysis list and mark it as “from transcription”

### Step 7: Reconcile With Existing Checklist Items (Update the Checklist List)

**MUST** compare:

- The derived core subflow list (Steps 5–6)
- The existing subflow items in the checklist row for `(MODULE_CODE, FR_CODE)`

Rules:

- Any **missing** item (in analysis but not in checklist) → **append** to checklist
- Any item in checklist but not in analysis → **evaluate**:
  - If far from PRD/transcriptions → remove or rewrite to fit
  - If similar but slightly different (**<10% difference**) → accept as-is
- Do not import items from other tenants/modules; keep this row strictly scoped to `(MODULE_CODE, FR_CODE)`

### Step 8: Verify Implementation Progress (Item-By-Item)

For each final subflow item, **MUST** create a small sub-todo list (so the agent stays on track per item), then verify:

1. **Presence**: relevant files/endpoints/components exist
2. **Correctness**: logic is implemented (not stubbed), handles key validation/edge cases, matches PRD intent
3. **Integration**: UI triggers the right actions; backend routes call the right controllers/services; data flows exist

Then set the correct status icon (✅/🟨/🟥) and update the evidence note in parentheses (e.g., `FE: <screen/file>` / `BE: <endpoint/controller>`).

### Step 9: Compute Progress % and Update the Checklist Row

After updating all item statuses in the row:

- Compute progress % using Step 4 formula
- Update the `Progress` column for that row

### Step 10: Output Summary (No New Files)

**MUST** output:

- Which checklist row was updated (Module + FR)
- What changed: items appended/removed/rewritten, status changes, new progress %
- Any critical caveats (missing PRD, ambiguous requirement, conflicting transcription evidence)

## Search Commands Reference

**Backend (Laravel)**:

```bash
rg -n "Route::" main/hairline-backend/routes
rg -n "function " main/hairline-backend/app/Http/Controllers
rg -n "class " main/hairline-backend/app/Models
```

**Web frontend (React, Provider/Admin)**:

```bash
rg -n "useQuery|useMutation|fetch\\(|axios" main/hairline-frontend/src
rg -n "route|navigate|router" main/hairline-frontend/src
```

**Patient app (Flutter)**:

```bash
rg -n "Widget|build\\(|Navigator\\.|GoRouter" main/hairline-app/lib
rg -n "dio|http|graphql|api" main/hairline-app/lib
```

**PRD structure scan**:

```bash
rg -n "^## " local-docs/project-requirements/functional-requirements/fr*/prd.md
```

**Transcriptions evidence search**:

```bash
rg -n "keyword" local-docs/project-requirements/transcriptions
```

## References

**GitHub Documentation**:

- System PRD: `https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/project-requirements/system-prd.md`
- FR PRDs: `https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/project-requirements/functional-requirements/fr###-*/prd.md`
- Client Transcriptions: `https://github.com/joachimtrungtuan/hairline-pm-docs/tree/main/project-requirements/transcriptions`
