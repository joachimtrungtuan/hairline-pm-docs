---
description: Verify implementation progress for one module+FR pair by checking codebase against FR PRD and transcriptions. Updates checklist row.
---

# Check Progress

Verify implementation progress for one `(MODULE_CODE, FR_CODE)` pair. Compare codebase against FR PRD and transcriptions. Update checklist row and produce a verification report with evidence-backed insights.

## Inputs (All Required)

- Checklist file path
- `MODULE_CODE` (e.g., P-01, PR-02, A-04, S-03)
- `FR_CODE` (e.g., FR-001, FR-007B)

If any is missing, ask for all three before proceeding.

## Hard Rules

- One (MODULE_CODE, FR_CODE) pair per run — do not mix tenants or modules
- Process FR PRD sections strictly one-by-one — never merge or combine
- Only update checklist file and create one verification report — no other changes
- Never import items across tenants/modules

## Module Scope

| Prefix | Frontend | Backend |
|--------|----------|---------|
| P-* (Patient) | `main/hairline-app/` (Flutter) | `main/hairline-backend/` (Laravel) |
| PR-* (Provider) | `main/hairline-frontend/` (React) | `main/hairline-backend/` |
| A-* (Admin) | `main/hairline-frontend/` (React) | `main/hairline-backend/` |
| S-* (Shared) | — | `main/hairline-backend/` only |

## Steps

1. Parse inputs: extract checklist file, MODULE_CODE, FR_CODE. Load all required documents: checklist file, `.specify/memory/constitution.md`, `local-docs/project-requirements/system-prd.md`, `local-docs/project-requirements/transcriptions/*.txt`, FR PRD at `local-docs/project-requirements/functional-requirements/fr###-*/prd.md`.

2. Find the exact checklist row matching MODULE_CODE and FR_CODE. No match → ask user. Multiple → ask which row (do not merge).

3. Derive core subflows from PRD: scan H2 headers first (do not load full content). Process each section one-by-one — load only that section, extract workflows/screens/business requirements relevant to MODULE_CODE, discard before next. Produce concise, testable subflow list.

4. Cross-check subflows against transcriptions. Search for supporting evidence per subflow. Add must-have items from transcriptions if absent from PRD (mark source as "from transcription").

5. Reconcile: append missing items to checklist, remove/rewrite items far from PRD, accept if <10% different. Never import across tenants/modules.

6. Verify implementation item-by-item in the codebase:
   - **Presence**: files, endpoints, components exist
   - **Correctness**: logic implemented (not stubbed), handles validation and edge cases, matches PRD
   - **Integration**: FE triggers correct actions, BE routes call correct controllers/services, data flows end-to-end

   Status per item:

   | Icon | Status | Score | Criteria |
   |------|--------|-------|----------|
   | ✅ | Completed | 1.0 | Fully implemented, functional, matches PRD, no critical bugs |
   | 🟨 | Partial | 0.5 | Core exists but missing edge cases, validation, non-critical features |
   | 🟥 | Not implemented | 0.0 | Missing or mostly stubbed |

   Add evidence notes (e.g., `FE: screens/login.dart` / `BE: AuthController@verify`). Preserve existing special markers (e.g., ⏳) unless user asks to change.

7. Compute progress: `round((sum(scores) / count) * 100)%`. Update the checklist row's progress column and all item statuses.

// turbo
8. Create verification report directory: `mkdir -p "local-docs/project-automation/task-creation/$(date +%Y-%m-%d)"`

9. Compute next 3-digit suffix from both `verification-report-*` and `implementation-tasks-*`. Create `verification-report-${DATE}-${SEQ}.md`. Report (under 500 words) must include:
   - Header lines: `**Checklist**: {file}`, `**Module**: {code}`, `**FR**: {code}`
   - Items appended/removed/rewritten
   - Status changes and new progress %
   - Evidence anchors (short file paths and endpoints)
   - Caveats (missing PRD sections, ambiguity, conflicting transcription signals)

10. Output summary: updated row identity (Module + FR), report file path, brief summary of changes, new progress %.

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

**PRD / Transcriptions**:
```
rg -n "^## " local-docs/project-requirements/functional-requirements/fr*/prd.md
rg -n "keyword" local-docs/project-requirements/transcriptions
```

## Deployment

Copy this file to `.agent/workflows/check-progress.md` for Antigravity to detect it.
