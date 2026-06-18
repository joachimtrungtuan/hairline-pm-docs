# Plane And Backlog Rules

Use this reference before setting task metadata, creating Plane issues, or updating a source backlog.

## Task Prefix

Always use `[BUG]` for bug fix tasks created by this skill.

## Task Name Traceability

Task names must carry a side prefix, then module and/or FR, immediately after `[BUG]`.

Side prefix:

- `[BUG][FE]` for frontend tasks
- `[BUG][BE]` for backend tasks
- `[BUG]` only when the side is untriageable (labeled `Bugs` only)

Preferred formats:

- `[BUG][FE] PR-06 - Provider treatment card primary detail access`
- `[BUG][BE] A-09a / FR-025 - Questionnaire set create does not persist`
- `[BUG][BE] FR-024 - Treatment creation submit blocked`

Use `MODULE_CODE / FR-###` when both are known and materially useful.

## Side Classification And Splitting

Every bug belongs to exactly one side per task. There is **no combined FE + BE task**.

- **FE-only** or **BE-only** bug -> one task with the matching side prefix and single side label.
- **Both** (spans UI and backend/data contract, persistence, API route, or server validation) -> split into **two** tasks: one `[BUG][FE]` and one `[BUG][BE]`. Each task restates the bug faithfully from the source and adds a `Scope Boundary` section (see `bug-task-format.md`).

## Label Selection

Set labels deliberately in every task. Each task carries exactly one side label (or none if untriageable).

| Label | Required when |
|---|---|
| `Bugs` | Always for every task from this skill |
| `FE Task` | UI behavior, route/view mismatch, visual state, form validation shown to user, local state, user interaction, frontend-only copy/UX |
| `BE Task` | Persistence, API route availability, server validation, backend lifecycle, returned data shape, auth/permission enforcement, data not saved or not fetched from authoritative source |
| `UX/UI` | Only when the task is design/wireframe/interaction-pattern work without confirmed implementation bug |

Allowed label sets:

- `Bugs, FE Task` for a frontend task (FE-only bug, or the FE half of a split bug).
- `Bugs, BE Task` for a backend task (BE-only bug, or the BE half of a split bug).
- `Bugs` alone only when evidence is insufficient to choose a side; add a note that technical ownership needs triage.

Never apply both `FE Task` and `BE Task` to a single task. A bug touching both sides must be split into two tasks (see "Side Classification And Splitting"), each carrying its own single side label.

## Plane Metadata

Use this block per task:

- `Status`: `Drafted`
- `Plane Task ID`: blank until Plane creation writes internal UUID
- `Plane Task Key`: blank until Plane creation writes readable key
- `FR`: `FR-###` or `TBD`
- `Product Module`: module code such as `PR-06`, `A-09a`, or `TBD`
- `Labels`: comma-separated label names
- `Priority`: `Urgent`, `High`, `Medium`, or `Low`
- `Plane Module`: name from `plane-values.json` when clear
- `Cycle`: target cycle name
- `Parent Task`: user-supplied readable key or blank

## Plane Module Selection

Choose the smallest clear Plane module:

- Provider dashboard bug -> `[2] Dashboard > Provider`
- Admin dashboard bug -> `[2] Dashboard > Admin`
- Mobile/patient bug -> use the matching mobile module from `plane-values.json` if available
- Shared service / backend-only bug -> leave blank unless a clear Plane module exists

Do not invent module names.

## Cycle And Deadline

If user gives a deadline:

1. Convert relative date to exact date using local timezone.
2. Read or refresh `plane-values.json`.
3. Select the cycle whose `start_date <= deadline < end_date`.
4. If no cycle matches, ask before choosing the nearest cycle.

If no deadline is given, use active cycle only after metadata refresh.

## Parent Task

Use parent keys only when:

- User provides explicit mapping, such as `PR-06 => HAIRL-1272`
- Source task file already includes parent mapping
- Plane values or a user-confirmed parent map clearly resolves it

Do not infer parent tasks from title similarity.

## Plane Creation

Follow `plane-api-commands`:

1. Compile scripts if making script changes; otherwise skip.
2. Run `create-plane-issues.py --dry-run`.
3. Review total, labels, module, cycle, and parent distribution.
4. Run live creation only after dry-run is clean and user intent is explicit.
5. Confirm the task file has one `Plane Task ID` and one `Plane Task Key` per task after creation.

## Source Backlog Status Updates

Update source backlog status only when user asks.

For sprint readiness backlogs, use only approved `Task Status` values (defined by the `sprint-readiness-reporting` skill):

- `Review pending`
- `Scout flagged`
- `Recorded only`
- `Task created (FE: HAIRL-123)` / `Task created (BE: HAIRL-123)` / `Task created (FE: HAIRL-123; BE: HAIRL-124)`
- `Resolved - pending re-test`
- `Resolved - verified YYYY-MM-DD`

After Plane creation, update each matching source row from `Recorded only` to `Task created (...)` with the created Plane key(s), side-labeled:

- A bug that produced one side's task -> `Task created (FE: HAIRL-1234)` or `Task created (BE: HAIRL-1234)`.
- A bug that was split into FE and BE tasks -> write **both** keys in the one cell, FE first then BE: `Task created (FE: HAIRL-1234; BE: HAIRL-1235)`.

When a single source bug row produced two tasks (FE + BE), keep it as one backlog row and record both keys in its `Task Status` cell. Preserve the row's `Bug ID` and copy the same value into both tasks as `Source Bug ID`; do not duplicate the row or add extra Plane-tracking columns.

Do not add Plane assignee, due date, or ownership columns to readiness backlog files.

## Update Logs

Task creation output files under `local-docs/project-automation/task-creation/` do not require update logs by themselves.

Updating source readiness backlogs is a significant document change. Append to a same-day relevant update log when one exists; otherwise create a same-day log and update `update-logs/README.md`.
