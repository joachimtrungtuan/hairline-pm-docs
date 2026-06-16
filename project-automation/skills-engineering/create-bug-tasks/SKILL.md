---
name: create-bug-tasks
description: Create Plane-ready Hairline bug fix task markdown files from bug reports, sprint readiness backlogs, pasted bug lists, or rows marked Recorded only. Use when asked to draft implementation tasks for confirmed bugs, convert bug backlog rows into [BUG] tasks, create tasks from sprint-1-readiness-fix-backlog.md-style tables, or prepare Plane issue creation artifacts with FR/module traceability, labels, priority, parent, cycle, references, evidence, and optional post-create backlog status updates.
---

# Create Bug Tasks

## Purpose

Create one date-stamped markdown task artifact under `local-docs/project-automation/task-creation/YYYY-MM-DD/` containing Plane-ready `[BUG]` tasks. This skill is for confirmed bug fixes, especially bug rows from sprint readiness backlogs.

Use self-contained references in this skill. Do not depend on reference files from sibling skills.

## Required Inputs

At least one of:

1. Source bug file path, such as `local-docs/product-plans/.../sprint-*-readiness-fix-backlog.md`
2. Pasted bug list or bug report content
3. Explicit task scope such as `Recorded only` rows in a named backlog file

Optional:

- Parent task mapping, such as `PR-06 => HAIRL-1272`
- Target deadline or cycle instruction, such as `next Monday => set matching cycle`
- Figma/design link
- Request to create tasks live on Plane after drafting
- Request to update source backlog status after Plane creation

If source rows lack enough information to identify one bug, steps, actual outcome, and expected outcome, stop and ask for the missing evidence.

## Scope And Guardrails

- Write task artifacts only under `local-docs/project-automation/task-creation/YYYY-MM-DD/`.
- Do not modify product code.
- Do not modify source bug/backlog files unless the user explicitly asks for status updates after task creation.
- Do not edit Plane live before running and reviewing a dry-run with `plane-api-commands`.
- When updating sprint readiness backlog statuses, follow `sprint-readiness-reporting` status rules.
- Do not copy tracking-only columns such as `Task Status` into task descriptions.
- Keep bug tasks single-minded: one task should represent one fixable bug on one side of the system.
- Never produce a combined FE + BE task. A bug that spans both sides must be split into one FE task and one BE task (see Step 6).

## References To Load

Load only the needed reference files:

- `references/bug-task-format.md` before drafting any task file.
- `references/source-row-mapping.md` before converting backlog rows or pasted bug reports.
- `references/plane-and-backlog-rules.md` before setting labels, priority, cycle, parent, or updating source backlog statuses.

## Workflow

### 1. Track Progress

Before starting, create a checklist for:

1. Resolve source and date
2. Extract eligible bugs
3. Resolve PRD/document/design references
4. Classify each bug as FE / BE / Both and split Both into two tasks
5. Resolve Plane metadata
6. Draft task file
7. Validate task file
8. Optional Plane dry-run and live creation
9. Optional source backlog status update

Mark steps in progress and complete as work proceeds.

### 2. Resolve Date And Source

1. Get `CURRENT_DATE` with `date +%Y-%m-%d`.
2. Resolve the source bug file or pasted input.
3. If using a sprint readiness backlog, resolve the launch-plan file only when needed for sprint scope or expected behavior.
4. If the user asks for `Recorded only`, select only rows whose `Task Status` is exactly `Recorded only`.
5. If the user asks for general bug tasks, select only rows or inputs that describe confirmed bugs, not evidence gaps or placeholders.

### 3. Extract Bug Fields

For each bug, capture:

- Priority from source, such as `P0`, `P1`, `P2`, `P3`
- Flow / Story or Area
- Issue
- Steps to Reproduce
- Actual Outcome
- Expected Outcome
- Evidence Link
- Notes
- FR code and Product Module when available or inferable from the section/module

Preserve source wording closely when the source is a structured backlog row. Rewrite only for clarity and Plane format.

For direct user input, rewrite into a clear bug task with one focused issue, concrete steps, actual outcome, expected outcome, evidence, and acceptance criteria. Do not invent requirements not present in the input.

### 4. Resolve References Early

Every task description must include a `Reference` section immediately after `Overview`.

For each bug:

1. Find the matching FR PRD when the bug mentions or implies an FR code.
   - Search `local-docs/project-requirements/functional-requirements/fr###-*/prd.md`.
   - If multiple candidates exist, choose the PRD whose title/module/screen context matches the bug.
   - If no PRD can be confidently matched, use the source backlog/report link and note the PRD as unresolved in the task notes.
2. Include source backlog/report GitHub link.
3. Include Figma/design link when provided or when the bug source contains a stable design link.
4. Include system PRD, transcription, or launch-plan links only when they materially clarify that specific bug.

Use GitHub links, not local file paths, in task descriptions. Convert `local-docs/...` to `https://github.com/joachimtrungtuan/hairline-pm-docs/blob/main/...` by stripping the `local-docs/` prefix.

### 5. Classify Side And Split

Determine which side of the system each bug belongs to before drafting. Load `references/plane-and-backlog-rules.md` "Label Selection" for the FE/BE signal table.

1. Classify each bug as one of:
   - **FE-only** — UI behavior, route/view mismatch, visual state, client-side validation/copy/UX, local state, user interaction.
   - **BE-only** — persistence, API route availability, server validation, returned data shape, auth/permission enforcement, data not saved or not fetched from the authoritative source.
   - **Both** — the bug spans UI and backend/data contract, persistence, API route, or server validation at the same time.
2. For FE-only or BE-only bugs, produce **one** task with the single matching side label.
3. For **Both** bugs, **split into two separate tasks** — one FE, one BE. Never emit a combined FE + BE task.
   - Each task must restate the bug faithfully from the source report: the same `Current Status`, `Steps to Reproduce`, `Evidence`, and `Notes` carry to both tasks.
   - Each task's `Expectation (Suggestion)` states **only that side's** expected behavior.
   - Each task adds a `Scope Boundary` section (see `references/bug-task-format.md`) declaring the side it covers, the counterpart task name, and the shared contract/handoff between the two sides.
   - The two tasks cross-link each other by task name in `Scope Boundary > Counterpart task`.
4. If evidence is insufficient to decide the side, do not split. Emit one task labeled `Bugs` only and note that technical ownership needs triage.

### 6. Resolve Plane Metadata

1. Refresh Plane values with `plane-api-commands` `refresh-values`, or use `plane-values.json` only if refreshed in the current turn.
2. If the user gives a deadline, convert relative date to an exact date and choose the Plane cycle whose date range covers it.
3. Set Plane module per task from `plane-values.json` when the module clearly maps:
   - Provider dashboard bugs -> `[2] Dashboard > Provider`
   - Admin dashboard bugs -> `[2] Dashboard > Admin`
   - Patient/mobile bugs -> matching mobile module if present; otherwise leave blank.
4. Apply parent task mapping supplied by the user. Do not invent parent keys.

### 7. Draft Task File

1. Ensure `local-docs/project-automation/task-creation/${CURRENT_DATE}/` exists.
2. Scan both patterns:
   - `implementation-tasks-${CURRENT_DATE}-*.md`
   - `verification-report-${CURRENT_DATE}-*.md`
3. Use the next 3-digit suffix and create `implementation-tasks-${CURRENT_DATE}-${SEQ}.md`.
4. Add one task per side per bug: one task for each FE-only or BE-only bug, and two tasks (FE + BE) for each Both bug.
5. Include a summary with:
   - Module/FR categorization
   - Source priority distribution
   - Plane priority distribution
   - Status breakdown
   - Total tasks and suggested next steps

## Task Naming

Task names must carry a side marker and traceability after `[BUG]`.

Every task gets a side prefix:

- `[BUG][FE]` for frontend tasks
- `[BUG][BE]` for backend tasks
- `[BUG]` only when the side is untriageable (evidence insufficient; labeled `Bugs` only)

Then append traceability using one of these formats:

- `[BUG][FE] MODULE_CODE - Short bug title`
- `[BUG][BE] MODULE_CODE / FR-### - Short bug title`
- `[BUG][FE] FR-### - Short bug title` only when module is unknown

For a split (Both) bug, the FE and BE tasks share the same module/FR/title and differ only by the side prefix.

Examples:

- `[BUG][FE] PR-06 - Provider treatment card primary detail access`
- `[BUG][BE] A-09a / FR-025 - Questionnaire set create does not persist`
- Split pair: `[BUG][FE] A-09a / FR-025 - Questionnaire set create does not persist` and `[BUG][BE] A-09a / FR-025 - Questionnaire set create does not persist`

Do not use vague names such as `[BUG] Fix questionnaire issue`.

## Live Plane Creation And Backlog Updates

When the user asks to create tasks on Plane:

1. Run `create-plane-issues.py --dry-run`.
2. Confirm per-task labels, priority, module, cycle, and parent.
3. Run live creation only after dry-run is clean and user intent is clear.
4. Let the script write `Plane Task ID` and `Plane Task Key` back into the task file.
5. If the user asks to update a sprint readiness backlog, update only the matching source rows from `Recorded only` to `Task created (...)` with side-labeled Plane key(s): `Task created (FE: HAIRL-1234)` / `Task created (BE: HAIRL-1234)` for one side, or `Task created (FE: HAIRL-1234; BE: HAIRL-1235)` when the bug was split into FE and BE tasks. Keep one backlog row per source bug and record both keys in its single `Task Status` cell.
6. Add or append an update log when the source backlog is significantly changed.

Do not remove assignees or set deadlines unless the user explicitly asks for that post-create action.
