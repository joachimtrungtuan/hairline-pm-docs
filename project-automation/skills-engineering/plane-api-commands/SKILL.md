---
name: plane-api-commands
description: Execute Plane API operations for Hairline task workflows. Use when asked to refresh Plane metadata values, list Plane resources, create Plane work items from implementation task markdown files, update existing Plane work items, assign parent work items, or add reference links to Plane work item descriptions.
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

- `refresh-values`: fetch labels, modules, cycles, states, issue types, priorities, and the currently active cycle into `plane-values.json`
- `create-work-item`: create new Plane work items from task markdown and write `Plane Task ID` / `Plane Task Key` back into the task file
- `update-work-item`: update existing work item descriptions from task markdown
- `set-parent`: assign parent work items for existing Plane work items
- `add-reference-links`: add raw clickable reference links to existing work item descriptions

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
**Plane Module**: [2] Dashboard > Provider
**Cycle**: 2026_May_C1
**Parent Task**:

## TASK_DESCRIPTION_START
<h2>Overview</h2>
...
## TASK_DESCRIPTION_END
```

Backward compatibility: creation and update scripts can parse older task blocks, but new tasks should use the preferred metadata.

## Field Rules

- `Plane Task ID`: internal UUID returned by Plane. Leave blank before creation. If populated, do not recreate the task.
- `Plane Task Key`: readable key such as `HAIRL-1131`; informational only.
- `Labels`: comma-separated Plane label names or UUIDs. If blank, creation infers one label from prefix: `[FE TASK]` -> `FE Task`, `[BE TASK]` -> `BE Task`, `[BUG]` -> `Bugs`, `[UX/UI TASK]` -> `UX/UI`.
- `Priority`: default `Medium`; accepted values are `None`, `Low`, `Medium`, `High`, `Urgent`.
- `Plane Module`: Plane module name or UUID. Leave blank if no matching Plane module is intended.
- `Cycle`: Plane cycle name or UUID. If blank, the create script uses `active_cycle` from `plane-values.json`.
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

The script prints added/removed/changed values and the active cycle. The cache contains no secrets.

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

Creation enforcement order:

1. Create the work item
2. Immediately write `Plane Task ID` and `Plane Task Key` back into the task file so reruns cannot duplicate an already-created issue
3. Assign `Plane Module` through Plane's module work-item endpoint when present
4. Assign `Parent Task` through the work-item update endpoint when present
5. Assign `Cycle` through Plane's cycle work-item endpoint when present

If any required assignment fails, the script exits with an error instead of reporting success; the task file will still contain the created issue UUID for recovery.

### 3. Update Plane work items

Use stored `Plane Task ID` values whenever possible:

```bash
cd "local-docs/project-automation/task-creation/plane-api" && \
python3 "../../skills-engineering/plane-api-commands/scripts/update-plane-issues.py" \
  --file "/absolute/path/to/implementation-tasks-YYYY-MM-DD-001.md" \
  --env ".env" \
  --dry-run
```

Remove `--dry-run` only after confirming the planned UUID mappings.

### 4. Set parents

Use `set-parent-by-sequence.py` only when the parent and children already exist and sequence IDs are known. Prefer adding parent metadata before creation for new tasks.

### 5. Add reference links

Use `add-reference-links-to-work-items.py` with `--link "Label=https://..."` or `--links-json`. The script has no built-in task-specific URLs.

## Validation

Before live writes:

1. Run `python3 -m py_compile scripts/*.py`
2. Run `fetch-plane-values.py --dry-run` or a real refresh if cache update is needed
3. Run create/update scripts with `--dry-run`
4. Confirm `Plane Task ID` is blank before create, and UUID-shaped before update
