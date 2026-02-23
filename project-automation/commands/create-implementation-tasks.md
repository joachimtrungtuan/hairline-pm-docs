---
description: Generate implementation task documents from FR verification gaps or PRD coverage. Trigger when user asks to create tasks, generate Plane issues, or produce implementation task files.
globs:
alwaysApply: false
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

**Before starting work**, create a checklist of all workflow steps below. Mark each step in-progress when starting and completed when done. This prevents step-skipping and keeps the workflow auditable.

## Workflow

### 1. Resolve date and report priority

1. Get `CURRENT_DATE` via `date +%Y-%m-%d`
2. Check `local-docs/project-automation/task-creation/${CURRENT_DATE}/verification-report-${CURRENT_DATE}-*.md`
3. Select matching report by scope:
   - With `MODULE_CODE`: require both module and FR match
   - Without `MODULE_CODE`: require FR match
4. If multiple match, pick highest numeric suffix

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
| `[FE TASK]` | Frontend-only (React in `hairline-frontend` or Flutter in `hairline-app`) |
| `[BE TASK]` | Backend-only (`hairline-backend`) |
| `[UX/UI TASK]` | Design/experience work — screen layouts, user flows, wireframes, interaction patterns |
| `[BUG]` | Fix incorrect existing behavior |

**Task metadata:**

- `**Status**: Drafted` (default), `Confirmed`, or `Added to Plane`
- `**FR**: FR-###` (always)
- `**Module**: P-##` or `TBD`

**Task block format (inline from references/task-format.md):**

```markdown
## TASK_NAME_START
[PREFIX] Descriptive Task Name
## TASK_NAME_END

**Status**: Drafted
**FR**: FR-###
**Module**: P-## (or TBD)

## TASK_DESCRIPTION_START
<h2>Overview</h2>
<p>[Business problem and expected outcome — 2-3 sentences as a single paragraph. Describe WHAT and WHY, not HOW.]</p>
<h2>Reference</h2>
<ul>
<li><a href="[GitHub FR PRD link with section anchor]">FR PRD</a></li>
</ul>
<h2>Current Status</h2>
<ul>
<li>[What currently exists or doesn't — observable behavior only]</li>
</ul>
<h2>Expectation (Suggestion)</h2>
<p><strong>Note:</strong> The requirements below describe business needs and functional expectations. Developers should use their expertise to choose the most beneficial and optimized implementation approach.</p>
<ul>
<li>[Business requirement item]</li>
</ul>
<h2>Acceptance Criteria</h2>
<ol>
<li>[Testable criterion from a user/reviewer perspective]</li>
</ol>
## TASK_DESCRIPTION_END
```

### HTML Formatting Rules (inline from references/task-format.md)

- Use `<h2>` for section headers
- Use `<p>` for **single paragraphs only** — never use multiple `<p>` tags for a list of items
- Use `<ul>` or `<ol>` with `<li>` for multiple items
- Use `<strong>`, `<code>`, `<a>` as needed
- No excessive whitespace or blank lines between tags

### Section Length Limits

- Current Status: prefer ≤5 `<li>` items
- Expectation: prefer ≤7 `<li>` items
- Acceptance Criteria: prefer ≤5 `<li>` items
- Full description: under 300 words

### Content What-to-Include / What-to-NEVER-Include (inline from references/task-format.md)

**Include**: Business requirements, user-facing outcomes, data field lists (name, type/format, business validation), business rules, success/failure scenarios from user perspective.

**NEVER include**: Database schema/table names, class/function names, code snippets, framework patterns (e.g., "use a Laravel migration"), API endpoint paths as implementation instructions, technology choices.

Data fields as business data (e.g., "Patient must provide: full name, email, phone number") not as DB columns (e.g., "Create patients table with varchar(255) name column").

## Reference Link Rules

- Use GitHub links in task Reference section (not local file paths)
- Default: include only the FR PRD GitHub link per task
- Include Figma only when provided by user — omit `<li>` entirely when no Figma link available
- Add System PRD or transcription links only when they materially clarify that specific task
- GitHub base: `https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/`
- **Path mapping**: Strip `local-docs/` prefix when converting local paths to GitHub URLs
  - Correct: `https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/project-requirements/functional-requirements/fr001-patient-authentication/prd.md`
  - Incorrect: `https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/local-docs/project-requirements/...`

## Final Output Requirements

Include a summary at end of file:

- Module/FR categorization
- Priority distribution (P1/P2/P3)
- Status breakdown
- Total tasks and suggested next steps

## Deployment

Copy this file to `.cursor/rules/create-implementation-tasks.md` for Cursor to detect it.
