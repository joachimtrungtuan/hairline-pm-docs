---
name: create-implementation-tasks
description: Generate date-stamped implementation task documents from FR verification gaps, checklist subflows, or FR PRD coverage. Use when asked to create Plane-ready implementation tasks for a specific FR scope with optional module scoping. Output to local-docs/project-automation/task-creation/YYYY-MM-DD.
---

# Create Implementation Tasks

## Purpose

Create business-focused implementation tasks for a requested FR scope. Produce one markdown file in `local-docs/project-automation/task-creation/YYYY-MM-DD/` with Plane-compatible HTML descriptions. Task content describes WHAT the system should do and WHY — never HOW to implement it technically.

## Required Inputs

1. `FR_CODE` (mandatory)
2. Optional `MODULE_CODE` for module-scoped tasking
3. Optional checklist file path
4. Optional pasted subflow list
5. Optional Figma link

If user requests module-FR tasking but omits `MODULE_CODE`, stop and ask for confirmation.

## Scope and Guardrails

- Write only task artifacts under `local-docs/project-automation/task-creation/YYYY-MM-DD/`
- Do not edit product code
- Do not modify checklist files unless explicitly asked
- If `MODULE_CODE` exists, scope strictly to `(MODULE_CODE, FR_CODE)`
- If `MODULE_CODE` is absent, scope to full `FR_CODE` (keep tenant/module contexts separate)

### Content Rules (CRITICAL)

**Task descriptions must focus exclusively on business requirements and functional needs.**

- Describe observable user-facing behavior, data fields, business rules, and acceptance criteria
- Data field lists are acceptable (field name, type, validation rules from a business perspective)
- **NEVER include**: database table designs, code architecture, class/function names, framework-specific patterns, API endpoint implementation details, or technology choices
- Developers should understand the business need and use their expertise for technical decisions

Each task description must be under 300 words.

## Progress Tracking (Mandatory)

**Before starting work**, create a checklist of all workflow steps below. Mark each step in-progress when starting and completed when done. Use the platform's task/todo tracking tools (task lists, todo items, progress trackers). This prevents step-skipping and keeps the workflow auditable.

## Workflow

### 1. Resolve date and report priority

1. Get `CURRENT_DATE` via `date +%Y-%m-%d`
2. Refresh active Plane cycle context by running `plane-api-commands` `refresh-values`, or read `plane-values.json` only if it was refreshed in this turn
3. Check `local-docs/project-automation/task-creation/${CURRENT_DATE}/verification-report-${CURRENT_DATE}-*.md`
4. Select matching report by scope:
   - With `MODULE_CODE`: require both module and FR match
   - Without `MODULE_CODE`: require FR match
5. If multiple match, pick highest numeric suffix

### 2. Select task basis (priority order)

Use first available:

1. Matching same-day verification report
2. Checklist subflow list or user-pasted subflow list
3. FR PRD-derived coverage from `local-docs/project-requirements/functional-requirements/fr###-*/prd.md`

### 3. Create output file with incremental suffix

1. Ensure `local-docs/project-automation/task-creation/${CURRENT_DATE}/` exists
2. Scan both filename patterns:
   - `implementation-tasks-${CURRENT_DATE}-*.md`
   - `verification-report-${CURRENT_DATE}-*.md`
3. Set `SEQ` to next 3-digit suffix (start at `001`)
4. Create `implementation-tasks-${CURRENT_DATE}-${SEQ}.md`

### 4. Draft tasks in Plane-ready format

For each missing or incomplete component, create a task.

**Allowed task prefixes:**

| Prefix | Use When |
|--------|----------|
| `[FE+BE TASK]` | Change spans both frontend UI and backend logic |
| `[FE TASK]` | Frontend-only (React or Flutter depending on module) |
| `[BE TASK]` | Backend-only |
| `[UX/UI TASK]` | Design/experience work — screen layouts, user flows, wireframes, interaction patterns |
| `[BUG]` | Fix incorrect existing behavior |

**Task metadata:**

- Plane metadata is per task block. Do not assume one parent, label, priority, Plane module, or cycle applies to the entire file.
- `**Status**: Drafted` by default; do not use status as the Plane creation signal
- `**Plane Task ID**:` blank until created on Plane; after creation this must contain Plane's internal UUID
- `**Plane Task Key**:` blank until created on Plane; after creation this may contain readable key such as `HAIRL-1131`
- `**FR**: FR-###` (always)
- `**Product Module**: P-##` or `TBD`
- `**Labels**:` blank by default unless the task nature is already certain; FE tasks should use `FE Task`, BE tasks should use `BE Task`, bug tasks should use `Bugs`, UX/UI tasks should use `UX/UI`
- `**Priority**: Medium` unless the user explicitly requests another priority
- `**Plane Module**:` Plane module name from `plane-values.json` when a clear module match exists; otherwise blank
- `**Cycle**:` active Plane cycle name from the metadata refresh for the current date
- `**Parent Task**:` blank unless the user provides a parent issue/key; readable keys such as `HAIRL-1131` are acceptable and resolved by the Plane creation script before assignment

**Task description must use HTML format** as documented in `references/task-format.md`. Read that file for the exact template, required sections, and formatting rules before drafting any task.

## Reference Link Rules

- Use GitHub links in task Reference section (not local file paths)
- Default: include only the FR PRD GitHub link per task
- Include Figma only when provided by user
- Add System PRD or transcription links only when they materially clarify that specific task
- Every link must be a raw-clickable link: write the label as plain text before the anchor, and make the anchor text the URL itself
  - Correct: `<li>FR PRD: <a href="https://example.com/prd.md">https://example.com/prd.md</a></li>`
  - Incorrect: `<li><a href="https://example.com/prd.md">FR PRD</a></li>`
- GitHub base: `https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/`
- **Path mapping**: The GitHub repo root corresponds to the contents **inside** `local-docs/`. When converting a local path to a GitHub URL, **strip the `local-docs/` prefix** before appending to the base.
  - Correct: `https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/project-requirements/functional-requirements/fr001-patient-authentication/prd.md`
  - Incorrect: `https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/local-docs/project-requirements/functional-requirements/fr001-patient-authentication/prd.md`

## Final Output Requirements

Include a summary at end of file:

- Module/FR categorization
- Priority distribution (P1/P2/P3)
- Status breakdown
- Total tasks and suggested next steps
