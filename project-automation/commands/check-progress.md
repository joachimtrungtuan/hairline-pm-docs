---
description: Verify implementation progress for one module+FR pair by checking codebase against FR PRD and transcriptions. Trigger when user asks to check progress, update checklist, or verify implementation status.
globs:
alwaysApply: false
---

# Check Progress

## Purpose

Verify implementation progress for one `(MODULE_CODE, FR_CODE)` pair by comparing the codebase against the FR PRD and client transcriptions. Update the checklist row with accurate status per subflow item and produce a verification report with evidence-backed insights.

## Required Inputs

All three are mandatory — do not proceed if any is missing:

1. Checklist file path
2. `MODULE_CODE` (e.g., `P-01`, `PR-02`, `A-04`, `S-03`)
3. `FR_CODE` (e.g., `FR-001`, `FR-007B`)

If any is missing, request all three in one message before continuing.

## Hard Rules

- One `(MODULE_CODE, FR_CODE)` pair per run — do not mix tenants or modules
- Process FR PRD sections strictly one-by-one — never merge or combine sections
- Only update the checklist file and create one verification report file — no other file changes

## Progress Tracking (Mandatory)

**Before starting work**, create a checklist of all workflow steps below. Mark each step in-progress when starting and completed when done. This prevents step-skipping and keeps the workflow auditable.

## Workflow

### 1. Parse inputs and load documents

Extract `CHECKLIST_FILE`, `MODULE_CODE`, `FR_CODE` from user input.

Load all required documents:

- Checklist file
- `.specify/memory/constitution.md`
- `local-docs/project-requirements/system-prd.md`
- `local-docs/project-requirements/transcriptions/*.txt`
- FR PRD at `local-docs/project-requirements/functional-requirements/fr###-*/prd.md`

### 2. Resolve module scope to code locations

| Module prefix | Frontend | Backend |
|---------------|----------|---------|
| `P-*` (Patient) | `main/hairline-app/` (Flutter) | `main/hairline-backend/` (Laravel) |
| `PR-*` (Provider) | `main/hairline-frontend/` (React) | `main/hairline-backend/` |
| `A-*` (Admin) | `main/hairline-frontend/` (React) | `main/hairline-backend/` |
| `S-*` (Shared Services) | — | `main/hairline-backend/` only |

### 3. Locate exact checklist row

Find one row matching exact `MODULE_CODE` and containing `FR_CODE`.

- No match: ask user to confirm file, module, and FR
- Multiple matches: ask user which row (do not merge)

### 4. Derive core subflows from PRD

1. Scan H2 headers first (do not load full content)
2. Process each section one-by-one:
   - Load only that section
   - Extract workflows, screens, business requirements relevant to `MODULE_CODE`
   - Discard section content before moving to next
3. Produce a concise, testable core subflow list

### 5. Cross-check against transcriptions

For each subflow item, search transcriptions for supporting evidence. Add must-have items from transcriptions if absent from PRD (mark source as "from transcription").

### 6. Reconcile checklist items

Compare derived subflow list against existing checklist row items:

- Missing from checklist: append
- In checklist but not in analysis: remove or rewrite if far from PRD; accept as-is if <10% different
- Never import items across tenants/modules

### 7. Verify implementation progress item-by-item

For each subflow item, verify in the codebase:

1. **Presence**: files, endpoints, components exist
2. **Correctness**: logic implemented (not stubbed), handles validation and edge cases, matches PRD
3. **Integration**: FE triggers correct actions, BE routes call correct controllers/services, data flows end-to-end

Assign status per item:

| Icon | Status | Score | Criteria |
|------|--------|-------|----------|
| ✅ | Completed | 1.0 | Fully implemented, functional, matches PRD, no critical bugs |
| 🟨 | Partial | 0.5 | Core functionality exists but missing edge cases, validation, or non-critical features |
| 🟥 | Not implemented | 0.0 | Missing or mostly stubbed |

Add evidence notes in parentheses (e.g., `FE: screens/login.dart` / `BE: AuthController@verify`).

Preserve any existing special markers (e.g., `⏳`) unless user explicitly asks to change them.

### 8. Compute progress and update row

```
Progress % = round((sum(item_scores) / item_count) * 100)
```

Update the row's progress column and all item statuses.

### 9. Create verification report

1. `CURRENT_DATE=$(date +%Y-%m-%d)`
2. Ensure `local-docs/project-automation/task-creation/${CURRENT_DATE}/` exists
3. Compute next 3-digit suffix (`SEQ`) from both patterns:
   - `verification-report-${CURRENT_DATE}-*.md`
   - `implementation-tasks-${CURRENT_DATE}-*.md`
4. Create `verification-report-${CURRENT_DATE}-${SEQ}.md`

Report rules (under 500 words):

- **Header lines** (required):
  - `**Checklist**: {CHECKLIST_FILE}`
  - `**Module**: {MODULE_CODE}`
  - `**FR**: {FR_CODE}`
- Items appended/removed/rewritten
- Status changes and new progress %
- Key evidence anchors (short file paths and endpoints)
- Caveats (missing PRD sections, ambiguity, conflicting transcription signals)

### 10. Output summary

Return:

- Updated checklist row identity (Module + FR)
- Report file path
- Brief summary of changes and new progress %

## Search Commands Reference

**Backend (Laravel)**:

```
rg -n "Route::" main/hairline-backend/routes
rg -n "function " main/hairline-backend/app/Http/Controllers
rg -n "class " main/hairline-backend/app/Models
```

**Web frontend (React — Provider/Admin)**:

```
rg -n "useQuery|useMutation|fetch\(|axios" main/hairline-frontend/src
rg -n "route|navigate|router" main/hairline-frontend/src
```

**Patient app (Flutter)**:

```
rg -n "Widget|build\(|Navigator\.|GoRouter" main/hairline-app/lib
rg -n "dio|http|graphql|api" main/hairline-app/lib
```

**PRD structure scan**:

```
rg -n "^## " local-docs/project-requirements/functional-requirements/fr*/prd.md
```

**Transcription evidence search**:

```
rg -n "keyword" local-docs/project-requirements/transcriptions
```

## Deployment

Copy this file to `.cursor/rules/check-progress.md` for Cursor to detect it.
