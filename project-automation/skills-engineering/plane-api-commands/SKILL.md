---
name: plane-api-commands
description: Execute Plane API operations for Hairline task workflows. Use when asked to refresh Plane metadata values, list Plane resources, create Plane labels or milestones, create Plane work items from implementation task markdown files, update existing Plane work items, read the current state of work items by key, assign parent work items, or add reference links to Plane work item descriptions.
---

# Plane API Commands

## Purpose

Run Plane.so API workflows with reusable scripts. All credentials come from `local-docs/project-automation/task-creation/plane-api/.env`; never print, copy, or hardcode secrets.

## Hard Rules

- Do not create new script files while using this skill.
- Use only the reusable scripts in `scripts/`; if a script cannot support the request, stop and propose a script update instead of writing a one-off.
- Do not hardcode task-specific IDs, Figma URLs, issue ranges, labels, modules, cycles, or parent values into scripts.
- Treat `Plane Task ID` as the internal Plane UUID. Store readable keys such as `HAIRL-1131` in `Plane Task Key`.
- Prefer cached Plane values from `plane-values.json`. Run `fetch-plane-values.py` to refresh the cache when values may have changed.
- Do not use deprecated `/issues/` endpoints. Use `/work-items/`.

## Files

- Env: `local-docs/project-automation/task-creation/plane-api/.env`
- Metadata cache: `local-docs/project-automation/task-creation/plane-api/plane-values.json`
- Scripts: `local-docs/project-automation/skills-engineering/plane-api-commands/scripts/`

## Supported Modes

- `refresh-values`: fetch labels, modules, cycles, milestones, members (id and names only), states, issue types, priorities, and the currently active cycle into `plane-values.json`; optionally create missing labels and milestones first
- `create-work-item`: create new Plane work items from task markdown, write `Plane Task ID` / `Plane Task Key` back into the task file, and verify every field persisted
- `update-work-item`: update selected fields of existing work items from task markdown (description by default)
- `set-parent`: assign parent work items for existing Plane work items
- `add-reference-links`: add raw clickable reference links to existing work item descriptions
- `read-states`: read the current state name and state group of work items by readable key (read-only)

## Task File Contract

Preferred metadata block:

```markdown
## TASK_NAME_START
[FE TASK] Task Name
## TASK_NAME_END

**Status**: Drafted
**Plane Task ID**:
**Plane Task Key**:
**FR**: FR-###
**Product Module**: PR-05
**Labels**: FE Task
**Priority**: Medium
**State**:
**Assignees**:
**Start Date**:
**Due Date**:
**Plane Module**: [2] Dashboard > Provider
**Cycle**: 2026_May_C1
**Milestone**:
**Parent Task**:

## TASK_DESCRIPTION_START
<h2>Overview</h2>
...
## TASK_DESCRIPTION_END
```

Backward compatibility: creation and update scripts can parse older task blocks, but new tasks should use the preferred metadata.

Plane metadata is per task block. A single markdown file may legitimately contain different `Parent Task`, `Plane Module`, `Labels`, `Priority`, `State`, `Assignees`, dates, `Cycle`, and `Milestone` values across tasks.

## Field Rules

- `Plane Task ID`: internal UUID returned by Plane. Leave blank before creation. If populated, do not recreate the task.
- `Plane Task Key`: readable key such as `HAIRL-1131`; informational only.
- `Labels`: comma-separated Plane label names or UUIDs. If blank, creation infers one label from prefix: `[FE TASK]` -> `FE Task`, `[BE TASK]` -> `BE Task`, `[BUG]` -> `Bugs`, `[UX/UI TASK]` -> `UX/UI`, `[QA TASK]` -> `QA`. Use `none` for no label.
- `Priority`: default `Medium`; accepted values are `None`, `Low`, `Medium`, `High`, `Urgent`.
- `State`: Plane state name or UUID. If blank, the `.env` default state is used.
- `Assignees`: comma-separated member display names, full names, or UUIDs from the `members` cache. If blank, the `.env` `ASSIGNEE_ID` is used when set; use `none` for no assignee.
- `Start Date` / `Due Date`: `YYYY-MM-DD`; start must not be after due. Blank leaves the date unset.
- `Plane Module`: Plane module name or UUID. Leave blank if no matching Plane module is intended.
- `Cycle`: Plane cycle name or UUID. If blank, the script uses the cycle active on the run date (computed from the cached cycle dates); use `none` for no cycle.
- `Milestone`: Plane milestone title or UUID. Leave blank for no milestone. A work item belongs to at most one milestone; assigning another moves it.
- `Parent Task`: user may provide a readable key such as `HAIRL-1131`; the create script resolves it to the internal UUID before creation. Internal UUID is also accepted.

## Workflow

### 1. Refresh Plane values

Use when the user asks to check Plane values or when labels/modules/cycles may have changed.

```bash
cd "local-docs/project-automation/task-creation/plane-api" && \
python3 "../../skills-engineering/plane-api-commands/scripts/fetch-plane-values.py" \
  --env ".env" \
  --output "plane-values.json"
```

The script prints added/removed/changed values and the active cycle. The cache contains no secrets and no member emails.

To create missing values before the refresh, add repeatable `--ensure-label "NAME[=#hex]"` or `--ensure-milestone "TITLE[=YYYY-MM-DD]"` (an existing milestone gets its target date aligned when a date is given). Combine with `--dry-run` to preview.

### 2. Create Plane work items

Always dry-run first:

```bash
cd "local-docs/project-automation/task-creation/plane-api" && \
python3 "../../skills-engineering/plane-api-commands/scripts/create-plane-issues.py" \
  --file "/absolute/path/to/implementation-tasks-YYYY-MM-DD-001.md" \
  --env ".env" \
  --values "plane-values.json" \
  --dry-run
```

After user approval for live creation, rerun without `--dry-run`. The script writes internal UUIDs to `Plane Task ID` and readable keys to `Plane Task Key`.

Dry-run output must be reviewed per task. It prints resolved state, priority, labels, assignees, dates, module, cycle, milestone, and parent identity for each task, so mixed parent/module files are visible before live creation.

Creation enforcement order:

1. Create the work item
2. Immediately write `Plane Task ID` and `Plane Task Key` back into the task file so reruns cannot duplicate an already-created issue
3. Assign `Plane Module` through Plane's module work-item endpoint when present
4. Assign `Parent Task` through the work-item update endpoint when present
5. Assign `Cycle` through Plane's cycle work-item endpoint when present
6. Assign `Milestone` through Plane's v2 milestone work-items endpoint when present
7. Read the work item back and verify name, state, priority, type, assignees, labels, dates, parent, cycle, module, and milestone

If any required assignment fails or a field did not persist, the script exits with an error instead of reporting success; the task file will still contain the created issue UUID for recovery (fix with `update-plane-issues.py --fields`).

### 2A. Interrupted Or Partial Runs

If the task file contains a mix of blank and populated `Plane Task ID` fields, do not rerun live creation in strict mode.

Use one of these recovery paths:

- `--resume`: skip tasks that already have `Plane Task ID`, and create only tasks whose ID is blank.
- `--skip N` / `--limit N`: select a known contiguous range of uncreated tasks.
- `--reset-local-ids --dry-run`: inspect which local IDs would be cleared if the previous Plane issues were test issues, deleted, or intentionally abandoned.

Strict mode intentionally fails when any selected task already has `Plane Task ID`. This prevents duplicate Plane issues.

Resume example:

```bash
cd "local-docs/project-automation/task-creation/plane-api" && \
python3 "../../skills-engineering/plane-api-commands/scripts/create-plane-issues.py" \
  --file "/absolute/path/to/implementation-tasks-YYYY-MM-DD-001.md" \
  --env ".env" \
  --values "plane-values.json" \
  --resume \
  --dry-run
```

Reset is local-only and does not delete or archive Plane issues. Use it only when duplicate creation is intentional:

```bash
cd "local-docs/project-automation/task-creation/plane-api" && \
python3 "../../skills-engineering/plane-api-commands/scripts/create-plane-issues.py" \
  --file "/absolute/path/to/implementation-tasks-YYYY-MM-DD-001.md" \
  --env ".env" \
  --values "plane-values.json" \
  --reset-local-ids \
  --dry-run
```

To actually clear local IDs, add `--confirm-reset-local-ids`. After reset, live creation will create new Plane issues from scratch.

### 3. Update Plane work items

Use stored `Plane Task ID` values whenever possible:

```bash
cd "local-docs/project-automation/task-creation/plane-api" && \
python3 "../../skills-engineering/plane-api-commands/scripts/update-plane-issues.py" \
  --file "/absolute/path/to/implementation-tasks-YYYY-MM-DD-001.md" \
  --env ".env" \
  --values "plane-values.json" \
  --fields "description" \
  --dry-run
```

`--fields` takes a comma-separated list of `name`, `description`, `state`, `priority`, `type`, `assignees`, `labels`, `dates`, `parent`, `cycle`, `module`, `milestone`, or `all` (default `description`). Non-description fields are read back and verified after the update.

Remove `--dry-run` only after confirming the planned UUID mappings.

### 4. Set parents

Use `set-parent-by-sequence.py` only when the parent and children already exist and sequence IDs are known. Prefer adding parent metadata before creation for new tasks.

### 5. Add reference links

Use `add-reference-links-to-work-items.py` with `--link "Label=https://..."` or `--links-json`. The script has no built-in task-specific URLs.

### 6. Read work-item states

Read-only. Use it when another workflow (for example `manual-test-bug-sync`) needs the current state of known work items:

```bash
cd "local-docs/project-automation/task-creation/plane-api" && \
python3 "../../skills-engineering/plane-api-commands/scripts/fetch-work-item-states.py" \
  --env ".env" \
  --values "plane-values.json" \
  --keys "HAIRL-1600,HAIRL-1601" \
  --output "/session/scratchpad/states.json"
```

Output is `{"HAIRL-1600": {"state": "Finished", "group": "completed"}}`. The script exits with an error listing keys it cannot find (deleted, archived, or in another project), and warns when a state is missing from the values cache; refresh the cache and rerun in that case. Write the output to the session scratchpad, not under `local-docs/`.

## Validation

Before live writes:

1. Run `python3 -m py_compile scripts/*.py`
2. Run `fetch-plane-values.py --dry-run` or a real refresh if cache update is needed
3. Check whether selected tasks have existing `Plane Task ID` values
4. For fresh creation, confirm all selected `Plane Task ID` fields are blank
5. For partial recovery, use `--resume` or a targeted `--skip` / `--limit` range
6. Run create/update scripts with `--dry-run`
7. Confirm the per-task parent/module/cycle/milestone distribution, assignees, and dates before live writes
