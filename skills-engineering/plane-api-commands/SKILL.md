---
name: plane-api-commands
description: Execute Plane API operations for listing workspace resources and creating work items from implementation task markdown files. Use when asked to run Plane list commands or bulk-create issues with Plane-compatible HTML descriptions.
---

# Plane API Commands

## Purpose

Run Plane.so API workflows for listing resources and bulk-creating work items from local task markdown files. All API credentials are loaded from environment files — never hardcode or expose API keys.

## Supported Operations

If user does not specify, ask them to choose:

- `list-users`
- `list-projects`
- `list-modules`
- `list-tags`
- `list-work-item-types`
- `list-stages`
- `create-work-item`

## Prerequisites

1. `.env` file at `local-docs/task-creation/plane-api/.env` with `PLANE_API_KEY`
2. System variables at `local-docs/plane-config/samasu-system-variables.md`
3. Tools: `python3`, `curl` (`jq` optional)

### Credential Handling (CRITICAL)

- **ALWAYS** load `PLANE_API_KEY` from the `.env` file
- **NEVER** hardcode, print, echo, log, or embed the API key in scripts, output, commit messages, or any generated content
- If `.env` is missing or the key is empty, ask the user to create/populate it
- If permission is denied reading `.env`, ask the user to grant file access — do not request the key in plain text

## Default Configuration

Load all IDs from `local-docs/plane-config/samasu-system-variables.md`. Fallback defaults:

| Parameter | Default |
|-----------|---------|
| `WORKSPACE_SLUG` | `samasu-digital` |
| `BASE_URL` | `https://api.plane.so/api/v1` |

For project, assignee, stage, priority, and issue type IDs: always reference `samasu-system-variables.md` for current values. Do not hardcode UUIDs in generated scripts.

## Task File Contract

When creating issues from markdown, require this block format:

```markdown
## TASK_NAME_START
[PREFIX] Task Name
## TASK_NAME_END

**Status**: Drafted

## TASK_DESCRIPTION_START
<h2>Overview</h2>
<p>...</p>
(HTML content)
## TASK_DESCRIPTION_END
```

Allowed prefixes: `[FE+BE TASK]`, `[FE TASK]`, `[BE TASK]`, `[BUG]`, `[UX/UI TASK]`

Allowed statuses: `Drafted`, `Confirmed`, `Added to Plane`

Description content must be valid HTML for Plane.so `description_html` field.

## Progress Tracking (Mandatory)

**Before starting work**, create a checklist of all workflow steps below. Mark each step in-progress when starting and completed when done. Use the platform's task/todo tracking tools (task lists, todo items, progress trackers). This prevents step-skipping and keeps the workflow auditable.

## Workflow: Creating Issues from Markdown

### 1. Load credentials

Read `.env` from `local-docs/task-creation/plane-api/.env`:

```python
env_path = "local-docs/task-creation/plane-api/.env"
env_vars = {}
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            env_vars[key.strip()] = value.strip().strip('"').strip("'")

api_key = env_vars.get("PLANE_API_KEY", "")
if not api_key:
    raise SystemExit("PLANE_API_KEY not found in .env")
```

### 2. Read and parse the markdown task file

Use the script at `scripts/create-plane-issues.py`. The script:

- Reads `.env` for API credentials (never hardcoded)
- Reads `samasu-system-variables.md` config values or accepts them from `.env`
- Parses `TASK_NAME_START/END` and `TASK_DESCRIPTION_START/END` blocks
- Builds JSON payloads with proper escaping via `json.dumps()`
- Posts each issue to Plane API sequentially
- Reports success/failure per task with issue IDs

### 3. Execute

```bash
cd "/Users/joachimtrungtuan/My Documents/Vân Tay Media/Products/Hairline/local-docs/task-creation/plane-api" && python3 "/Users/joachimtrungtuan/My Documents/Vân Tay Media/Products/Hairline/local-docs/skills-engineering/plane-api-commands/scripts/create-plane-issues.py" --file "/path/to/implementation-tasks-YYYY-MM-DD-XXX.md"
```

### 4. Report results

Output:

- Total tasks found and created
- Task name to Plane issue ID mapping
- Any errors with likely fixes

## Why Python First

- `json.dumps()` correctly escapes quotes, newlines, and HTML in multiline descriptions
- Lower failure rate than ad hoc bash string quoting
- Clearer error handling and summary output

## API Operations Reference

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List Users | GET | `/workspaces/{slug}/members/` |
| List Projects | GET | `/workspaces/{slug}/projects/` |
| List Modules | GET | `/workspaces/{slug}/projects/{id}/modules/` |
| List Tags | GET | `/workspaces/{slug}/projects/{id}/labels/` |
| List Issue Types | GET | `/workspaces/{slug}/projects/{id}/issue-types/` |
| List States | GET | `/workspaces/{slug}/projects/{id}/states/` |
| Create Issue | POST | `/workspaces/{slug}/projects/{id}/issues/` |

### Create Issue Payload

```json
{
  "name": "[FE TASK] Task Name",
  "description_html": "<h2>Overview</h2><p>...</p>",
  "project": "{project_id}",
  "assignees": ["{assignee_id}"],
  "state": "{state_id}",
  "priority": "medium",
  "issue_type": "{issue_type_id}"
}
```

## Error Handling

| Code | Meaning | Fix |
|------|---------|-----|
| 401 | Invalid/expired API key | Regenerate key in Plane settings, update `.env` |
| 400 | Validation error | Check required fields and HTML format |
| 404 | Invalid IDs | Verify workspace/project/state/type IDs in `samasu-system-variables.md` |
| 429 | Rate limit (60/min) | Add delay between requests |
| 5xx | Server error | Retry with backoff |

## References

- System IDs: `local-docs/plane-config/samasu-system-variables.md`
- Task artifacts: `local-docs/task-creation/YYYY-MM-DD/implementation-tasks-*.md`
- Plane API docs: https://developers.plane.so/api-reference/introduction
