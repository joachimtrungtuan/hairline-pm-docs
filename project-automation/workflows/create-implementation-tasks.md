---
description: Generate Plane-ready implementation task documents from FR verification gaps, checklists, or PRD coverage. Output to task-creation folder.
---

# Create Implementation Tasks

Create business-focused implementation tasks for an FR scope. Produce one markdown file in `local-docs/project-automation/task-creation/YYYY-MM-DD/` with Plane-compatible HTML descriptions. Tasks describe WHAT and WHY — never HOW.

## Inputs

- `FR_CODE` (required, e.g., FR-001)
- `MODULE_CODE` (optional, e.g., P-01) — if user requests module-FR tasking but omits, stop and ask
- Checklist file path (optional)
- Pasted subflow list (optional)
- Figma link (optional)

## Scope and Guardrails

- Write only task artifacts under `local-docs/project-automation/task-creation/YYYY-MM-DD/`
- Do not edit product code or modify checklist files unless explicitly asked
- If `MODULE_CODE` exists, scope strictly to `(MODULE_CODE, FR_CODE)`
- If absent, scope to full FR_CODE (keep tenant/module contexts separate)

## Content Rules (CRITICAL)

- Describe observable user-facing behavior, data fields, business rules, acceptance criteria
- Data field lists acceptable (field name, type, business validation rules)
- **NEVER include**: database designs, code architecture, class/function names, framework patterns, API implementation details, technology choices
- Developers should understand business need and use their expertise for technical decisions
- Each task description under 300 words

## Steps

// turbo
1. Get the current date: `date +%Y-%m-%d`

2. Check for matching same-day verification report at `local-docs/project-automation/task-creation/${CURRENT_DATE}/verification-report-*.md`. Select by scope (module+FR or FR only). If multiple match, pick highest numeric suffix. If none found, use checklist subflows or derive from FR PRD.

// turbo
3. Create output directory: `mkdir -p "local-docs/project-automation/task-creation/${CURRENT_DATE}"`

4. Scan both `implementation-tasks-*` and `verification-report-*` patterns. Set `SEQ` to next 3-digit suffix (start `001`). Create `implementation-tasks-${CURRENT_DATE}-${SEQ}.md`.

5. For each gap or missing component, draft a task using this exact block format:

```
## TASK_NAME_START
[PREFIX] Descriptive Task Name
## TASK_NAME_END

**Status**: Drafted
**FR**: FR-###
**Module**: P-## or TBD

## TASK_DESCRIPTION_START
<h2>Overview</h2>
<p>[Business problem — 2-3 sentences as single paragraph. WHAT and WHY, not HOW.]</p>
<h2>Reference</h2>
<ul>
<li><a href="[GitHub FR PRD link]">FR PRD</a></li>
</ul>
<h2>Current Status</h2>
<ul>
<li>[Observable behavior — prefer ≤5 items]</li>
</ul>
<h2>Expectation (Suggestion)</h2>
<p><strong>Note:</strong> Requirements describe business needs. Developers choose implementation.</p>
<ul>
<li>[Business requirement — prefer ≤7 items]</li>
</ul>
<h2>Acceptance Criteria</h2>
<ol>
<li>[Testable criterion — prefer ≤5 items]</li>
</ol>
## TASK_DESCRIPTION_END
```

Allowed prefixes: `[FE+BE TASK]`, `[FE TASK]` (React/Flutter), `[BE TASK]`, `[UX/UI TASK]`, `[BUG]`

Allowed statuses: `Drafted`, `Confirmed`, `Added to Plane`

### HTML Rules

- `<h2>` for section headers, `<p>` for single paragraphs only (never multiple `<p>` for lists)
- `<ul>`/`<ol>` with `<li>` for lists; `<strong>`, `<code>`, `<a>` as needed
- No excessive whitespace between tags
- Data as business fields (e.g., "Patient provides: full name, email") not DB columns

6. Reference links: GitHub base `https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/` — strip `local-docs/` prefix from local paths. Include only FR PRD link by default. Add Figma only when provided. Add System PRD/transcription only when they materially clarify that task.
   - Correct: `https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/project-requirements/functional-requirements/fr001-patient-authentication/prd.md`
   - Incorrect: `https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/local-docs/project-requirements/functional-requirements/fr001-patient-authentication/prd.md`

7. Add summary at end: module/FR categorization, priority distribution (P1/P2/P3), status breakdown, total tasks and suggested next steps.

## Deployment

Copy this file to `.agent/workflows/create-implementation-tasks.md` for Antigravity to detect it.
