# Plane And Backlog Rules

Use this reference before setting task metadata, creating Plane issues, or updating a source backlog.

## Task Prefix

Always use `[BUG]` for bug fix tasks created by this skill.

## Task Name Traceability

Task names must include module and/or FR immediately after `[BUG]`.

Preferred formats:

- `[BUG] PR-06 - Provider treatment card primary detail access`
- `[BUG] A-09a / FR-025 - Questionnaire set create does not persist`
- `[BUG] FR-024 - Treatment creation submit blocked`

Use `MODULE_CODE / FR-###` when both are known and materially useful.

## Label Selection

Set labels deliberately in every task.

| Label | Required when |
|---|---|
| `Bugs` | Always for every task from this skill |
| `FE Task` | UI behavior, route/view mismatch, visual state, form validation shown to user, local state, user interaction, frontend-only copy/UX |
| `BE Task` | Persistence, API route availability, server validation, backend lifecycle, returned data shape, auth/permission enforcement, data not saved or not fetched from authoritative source |
| `UX/UI` | Only when the task is design/wireframe/interaction-pattern work without confirmed implementation bug |

Use combinations:

- `Bugs, FE Task` for frontend-only interaction/display bugs.
- `Bugs, BE Task` for backend-only failures with no UI change expected.
- `Bugs, FE Task, BE Task` when the bug spans UI and backend/data contract, persistence, API route, or validation mismatch.

If evidence is insufficient to choose FE/BE, use `Bugs` only and add a note that technical ownership needs triage.

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

For sprint readiness backlogs, use only approved `Task Status` values:

- `Review pending`
- `Recorded only`
- `Task created (HAIRL-123)`
- `Resolved - pending re-test`
- `Resolved - verified YYYY-MM-DD`

After Plane creation, update each matching source row from `Recorded only` to `Task created (HAIRL-1234)`.

Do not add Plane assignee, due date, or ownership columns to readiness backlog files.

## Update Logs

Task creation output files under `local-docs/project-automation/task-creation/` do not require update logs by themselves.

Updating source readiness backlogs is a significant document change. Append to a same-day relevant update log when one exists; otherwise create a same-day log and update `update-logs/README.md`.
