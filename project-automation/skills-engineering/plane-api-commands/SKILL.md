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

## Available Scripts

Two Python scripts are available for Plane operations:

### 1. `create-plane-issues.py` - Create New Issues

Creates new Plane issues from markdown task files. Use for first-time task creation.

**Key Features:**
- Cleans HTML descriptions (removes excessive whitespace)
- Validates all required configuration
- Reports success/failure per task with issue IDs
- Supports `--skip N` to skip first N tasks in the file

**Usage:**
```bash
cd "local-docs/project-automation/task-creation/plane-api" && \
python3 "../../skills-engineering/plane-api-commands/scripts/create-plane-issues.py" \
--file "/path/to/implementation-tasks-YYYY-MM-DD-XXX.md" \
[--skip N]
```

### 2. `update-plane-issues.py` - Update Existing Issues

Updates existing Plane issues with cleaned HTML descriptions. Use when issues already exist but need description cleanup.

**Key Features:**
- Updates only the `description_html` field
- Cleans HTML to remove excessive whitespace
- Maps task file order to sequential issue identifiers
- Supports `--skip N` parameter for partial file processing

**Usage:**
```bash
cd "local-docs/project-automation/task-creation/plane-api" && \
python3 "../../skills-engineering/plane-api-commands/scripts/update-plane-issues.py" \
--file "/path/to/implementation-tasks-YYYY-MM-DD-XXX.md" \
--start-issue "HAIRL-XXX" \
[--skip N]
```

**Example Scenarios:**

1. **Create all tasks in a new file:**
   ```bash
   python3 create-plane-issues.py --file "implementation-tasks-2026-02-13-001.md"
   ```

2. **Update existing issues HAIRL-877 to HAIRL-892 with cleaned HTML:**
   ```bash
   python3 update-plane-issues.py \
   --file "implementation-tasks-2026-02-13-002.md" \
   --start-issue "HAIRL-877" \
   --skip 2
   ```
   (Skips first 2 tasks, updates starting from HAIRL-877)

3. **Create tasks from a subset of a file:**
   ```bash
   python3 create-plane-issues.py \
   --file "implementation-tasks-2026-02-13-002.md" \
   --skip 5
   ```
   (Skips first 5 tasks, creates remaining ones)

## Workflow: Creating Issues from Markdown

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

### 2. Recreate the script with HTML cleaning

Before executing, write the script **exactly** to `scripts/create-plane-issues.py` or `scripts/update-plane-issues.py`. The scripts include:

- HTML cleaning function to remove excessive whitespace
- Proper credential loading from `.env`
- Configuration validation
- Clear error reporting
- Skip parameter support for partial file processing

**Critical: HTML Cleaning Function**

Both scripts must include this function to ensure clean Plane descriptions:

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

This function must be called in `parse_tasks()` before returning task descriptions.

### 3. Execute the appropriate script

Choose based on whether issues already exist:

**For NEW issues:**
```bash
cd "local-docs/project-automation/task-creation/plane-api" && \
python3 "../../skills-engineering/plane-api-commands/scripts/create-plane-issues.py" \
--file "/path/to/implementation-tasks-YYYY-MM-DD-XXX.md"
```

**For UPDATING existing issues:**
```bash
cd "local-docs/project-automation/task-creation/plane-api" && \
python3 "../../skills-engineering/plane-api-commands/scripts/update-plane-issues.py" \
--file "/path/to/implementation-tasks-YYYY-MM-DD-XXX.md" \
--start-issue "HAIRL-XXX"
```

### 4. Report results

Output:

- Total tasks found and created/updated
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

**Note:** The update script fetches issue UUIDs by querying all issues and matching `sequence_id` (e.g., HAIRL-892 → sequence_id: 892).

## Error Handling

| Code | Meaning | Fix |
|------|---------|-----|
| 401 | Invalid/expired API key | Regenerate key in Plane settings, update `.env` |
| 400 | Validation error | Check required fields and HTML format |
| 404 | Invalid IDs | Verify workspace/project/state/type IDs in `samasu-system-variables.md` |
| 429 | Rate limit (60/min) | Add delay between requests |
| 5xx | Server error | Retry with backoff |

## References

- System IDs: `local-docs/project-automation/task-creation/plane-api/samasu-system-variables.md`
- Task artifacts: `local-docs/project-automation/task-creation/YYYY-MM-DD/implementation-tasks-*.md`
- Plane API docs: https://developers.plane.so/api-reference/introduction
