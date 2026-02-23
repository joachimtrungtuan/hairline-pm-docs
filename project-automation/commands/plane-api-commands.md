---
description: Run Plane.so API operations for listing workspace resources and bulk-creating/updating issues from implementation task markdown files. Trigger when user asks to create Plane issues, update Plane issues, list Plane resources, or push tasks to Plane.
globs:
alwaysApply: false
---

# Plane API Commands

## Purpose

Run Plane.so API workflows for listing resources, creating new issues, and updating existing issues from local task markdown files. All API credentials are loaded from environment files — never hardcode or expose API keys.

## Supported Operations

If user does not specify, ask them to choose:

- `list-users`
- `list-projects`
- `list-modules`
- `list-tags`
- `list-work-item-types`
- `list-stages`
- `create-work-item` (create new Plane issues)
- `update-work-item` (update existing Plane issues with cleaned HTML)

## Prerequisites

1. `.env` file at `local-docs/project-automation/task-creation/plane-api/.env` with `PLANE_API_KEY`
2. System variables at `local-docs/project-automation/task-creation/plane-api/samasu-system-variables.md`
3. Tools: `python3`, `curl` (`jq` optional)

### Credential Handling (CRITICAL)

- **ALWAYS** load `PLANE_API_KEY` from the `.env` file
- **NEVER** hardcode, print, echo, log, or embed the API key in scripts, output, commit messages, or any generated content
- If `.env` is missing or the key is empty, ask the user to create/populate it
- If permission is denied reading `.env`, ask the user to grant file access — do not request the key in plain text

## Default Configuration

Load all IDs from `local-docs/project-automation/task-creation/plane-api/samasu-system-variables.md`. Fallback defaults:

| Parameter | Default |
|-----------|---------|
| `WORKSPACE_SLUG` | `samasu-digital` |
| `BASE_URL` | `https://api.plane.so/api/v1` |

For project, assignee, stage, priority, and issue type IDs: always reference `samasu-system-variables.md` for current values. Do not hardcode UUIDs in generated scripts.

## Task File Contract

When creating or updating issues from markdown, require this block format:

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

**Before starting work**, create a checklist of all workflow steps below. Mark each step in-progress when starting and completed when done. This prevents step-skipping and keeps the workflow auditable.

## Available Scripts

Two Python scripts are available:

### 1. `create-plane-issues.py` - Create New Issues

**Use when:** Creating issues for the first time

**Features:**
- Cleans HTML descriptions (removes excessive whitespace)
- Validates all required configuration
- Reports success/failure per task with issue IDs
- Supports `--skip N` to skip first N tasks in the file

**Location:** `local-docs/project-automation/skills-engineering/plane-api-commands/scripts/create-plane-issues.py`

### 2. `update-plane-issues.py` - Update Existing Issues

**Use when:** Issues already exist but need description cleanup (e.g., removing excessive spaces)

**Features:**
- Updates only the `description_html` field (preserves all other fields)
- Cleans HTML to remove excessive whitespace
- Maps task file order to sequential issue identifiers
- Supports `--skip N` parameter for partial file processing

**Location:** `local-docs/project-automation/skills-engineering/plane-api-commands/scripts/update-plane-issues.py`

## Workflow: Creating New Issues

### 1. Load credentials

Read `.env` from `local-docs/project-automation/task-creation/plane-api/.env`:

```python
env_path = "local-docs/project-automation/task-creation/plane-api/.env"
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

### 2. Ensure the script includes HTML cleaning

Both scripts MUST include this function to clean HTML descriptions:

```python
def clean_html(html: str) -> str:
    """Clean HTML by removing excessive whitespace while preserving structure."""
    # Remove excessive spaces between tags
    html = re.sub(r'>\s+<', '><', html)
    # Normalize multiple spaces to single space within text content
    html = re.sub(r'  +', ' ', html)
    # Remove leading/trailing whitespace from each line
    lines = [line.strip() for line in html.split('\n') if line.strip()]
    # Join with no extra newlines
    return ''.join(lines)
```

The current scripts at `local-docs/project-automation/skills-engineering/plane-api-commands/scripts/` already include this function. Verify it's present before executing.

### 3. Execute create script

```bash
cd "local-docs/project-automation/task-creation/plane-api" && \
python3 "../../skills-engineering/plane-api-commands/scripts/create-plane-issues.py" \
--file "/absolute/path/to/implementation-tasks-YYYY-MM-DD-XXX.md"
```

**With skip parameter (if needed):**
```bash
cd "local-docs/project-automation/task-creation/plane-api" && \
python3 "../../skills-engineering/plane-api-commands/scripts/create-plane-issues.py" \
--file "/absolute/path/to/implementation-tasks-YYYY-MM-DD-XXX.md" \
--skip 2
```

### 4. Report results

Output:
- Total tasks found and created
- Task name to Plane issue ID mapping
- Any errors with likely fixes

## Workflow: Updating Existing Issues

**Use this workflow when:**
- Issues already exist in Plane
- Need to clean up HTML descriptions (remove excessive spaces)
- Want to update descriptions without changing other fields

### 1. Determine starting issue number

Ask user or check Plane to find the first issue identifier (e.g., `HAIRL-877`)

### 2. Determine skip count

If the task file contains tasks that were already processed or don't need updating, calculate how many to skip from the beginning.

**Example:** Task file has 18 tasks, but only tasks 3-18 correspond to HAIRL-877 onwards → use `--skip 2`

### 3. Execute update script

```bash
cd "local-docs/project-automation/task-creation/plane-api" && \
python3 "../../skills-engineering/plane-api-commands/scripts/update-plane-issues.py" \
--file "/absolute/path/to/implementation-tasks-YYYY-MM-DD-XXX.md" \
--start-issue "HAIRL-877" \
--skip 2
```

### 4. Report results

Output:
- Total tasks found and updated
- Task identifier to issue mapping
- Any errors with likely fixes

## Why Python First

- `json.dumps()` correctly escapes quotes, newlines, and HTML in multiline descriptions
- Lower failure rate than ad hoc bash string quoting
- Clearer error handling and summary output
- Consistent HTML cleaning across all tasks

## API Operations Reference

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List Users | GET | `/workspaces/{slug}/members/` |
| List Projects | GET | `/workspaces/{slug}/projects/` |
| List Modules | GET | `/workspaces/{slug}/projects/{id}/modules/` |
| List Tags | GET | `/workspaces/{slug}/projects/{id}/labels/` |
| List Issue Types | GET | `/workspaces/{slug}/projects/{id}/issue-types/` |
| List States | GET | `/workspaces/{slug}/projects/{id}/states/` |
| List Issues | GET | `/workspaces/{slug}/projects/{id}/issues/` |
| Create Issue | POST | `/workspaces/{slug}/projects/{id}/issues/` |
| Update Issue | PATCH | `/workspaces/{slug}/projects/{id}/issues/{issue_id}/` |

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

### Update Issue Payload

```json
{
  "description_html": "<h2>Overview</h2><p>...</p>"
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

## Common Issues and Solutions

### Issue: "ERROR: Access to '\.env' is blocked by security policy"

**Cause:** The script is trying to access `.env` file but sandbox security is blocking it.

**Solution:** Run the command in an external terminal where the `.env` file is accessible, or grant file access permissions when prompted.

### Issue: Excessive whitespace in Plane issue descriptions

**Cause:** HTML descriptions contain multiple spaces between tags or within text.

**Solution:** Use the `update-plane-issues.py` script to clean existing issue descriptions, or ensure `create-plane-issues.py` includes the `clean_html()` function.

### Issue: Tasks created in wrong order or with wrong issue numbers

**Cause:** Not using the `--skip` parameter when some tasks in the file should not be processed.

**Solution:** Calculate which tasks to skip from the beginning of the file and use `--skip N` parameter.

## References

- System IDs: `local-docs/project-automation/task-creation/plane-api/samasu-system-variables.md`
- Task artifacts: `local-docs/project-automation/task-creation/YYYY-MM-DD/implementation-tasks-*.md`
- Plane API docs: https://developers.plane.so/api-reference/introduction

## Deployment

This file should be deployed to `.cursor/rules/plane-api-commands.md` for Cursor to detect it.
