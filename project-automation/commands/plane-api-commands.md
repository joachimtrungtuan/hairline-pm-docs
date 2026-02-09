---
description: Run Plane.so API operations for listing workspace resources and bulk-creating issues from implementation task markdown files. Trigger when user asks to create Plane issues, list Plane resources, or push tasks to Plane.
globs:
alwaysApply: false
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

**Before starting work**, create a checklist of all workflow steps below. Mark each step in-progress when starting and completed when done. This prevents step-skipping and keeps the workflow auditable.

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

### 2. Recreate the issue-creation script

Before executing, write the following script **exactly** to `local-docs/project-automation/skills-engineering/plane-api-commands/scripts/create-plane-issues.py`. Do not modify the script logic — recreate it verbatim to ensure consistent behavior across runs.

```python
#!/usr/bin/env python3
"""
Create Plane.so issues from implementation task markdown files.

Usage:
    python3 create-plane-issues.py --file <path-to-tasks.md>

Credentials are loaded from .env in the current working directory.
NEVER hardcode API keys in this script or its output.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def load_env(env_path: Path) -> dict:
    """Load variables from a .env file."""
    env_vars = {}
    if not env_path.exists():
        print(f"ERROR: .env file not found at {env_path}")
        print("Create it with PLANE_API_KEY and configuration values.")
        sys.exit(1)
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                env_vars[key.strip()] = value.strip().strip('"').strip("'")
    return env_vars


def parse_tasks(content: str) -> list:
    """Extract tasks from markdown using TASK_NAME/DESCRIPTION markers."""
    tasks = []
    pattern = (
        r"## TASK_NAME_START\n(.*?)\n## TASK_NAME_END"
        r"[\s\S]*?"
        r"## TASK_DESCRIPTION_START\n([\s\S]*?)\n## TASK_DESCRIPTION_END"
    )
    for match in re.finditer(pattern, content):
        name = match.group(1).strip()
        desc = match.group(2).strip()
        tasks.append({"name": name, "description": desc})
    return tasks


def create_issue(task: dict, config: dict) -> dict:
    """Create one Plane issue via API."""
    payload = {
        "name": task["name"],
        "description_html": task["description"],
        "project": config["PROJECT_ID"],
        "assignees": [config["ASSIGNEE_ID"]],
        "state": config["STAGE_ID"],
        "priority": config.get("PRIORITY", "medium"),
        "issue_type": config["ISSUE_TYPE_ID"],
    }
    url = (
        f"{config['BASE_URL']}/workspaces/{config['WORKSPACE_SLUG']}"
        f"/projects/{config['PROJECT_ID']}/issues/"
    )
    cmd = [
        "curl", "-s", "-X", "POST", url,
        "-H", f"X-API-Key: {config['PLANE_API_KEY']}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        try:
            resp = json.loads(result.stdout)
            if "id" in resp:
                return {"status": "success", "id": resp["id"]}
            return {"status": "error", "response": result.stdout}
        except json.JSONDecodeError:
            return {"status": "error", "response": result.stdout}
    return {"status": "error", "error": result.stderr}


def main():
    parser = argparse.ArgumentParser(
        description="Create Plane issues from markdown task files."
    )
    parser.add_argument(
        "--file", required=True, help="Path to implementation tasks markdown file"
    )
    parser.add_argument(
        "--env", default=".env", help="Path to .env file (default: .env in cwd)"
    )
    args = parser.parse_args()

    # Load credentials from .env
    env_path = Path(args.env)
    env_vars = load_env(env_path)

    api_key = env_vars.get("PLANE_API_KEY", "")
    if not api_key:
        print("ERROR: PLANE_API_KEY not found in .env file.")
        print("Add it to your .env: PLANE_API_KEY=plane_api_...")
        sys.exit(1)

    # Build config from env
    config = {
        "PLANE_API_KEY": api_key,
        "WORKSPACE_SLUG": env_vars.get("WORKSPACE_SLUG", "samasu-digital"),
        "BASE_URL": env_vars.get("BASE_URL", "https://api.plane.so/api/v1"),
        "PROJECT_ID": env_vars.get("PROJECT_ID", ""),
        "ASSIGNEE_ID": env_vars.get("ASSIGNEE_ID", ""),
        "STAGE_ID": env_vars.get("STAGE_ID", ""),
        "PRIORITY": env_vars.get("PRIORITY", "medium"),
        "ISSUE_TYPE_ID": env_vars.get("ISSUE_TYPE_ID", ""),
    }

    # Validate required config
    missing = [
        k for k in ["PROJECT_ID", "ASSIGNEE_ID", "STAGE_ID", "ISSUE_TYPE_ID"]
        if not config[k]
    ]
    if missing:
        print(f"ERROR: Missing required config in .env: {', '.join(missing)}")
        print("Reference: local-docs/project-automation/task-creation/plane-api/samasu-system-variables.md")
        sys.exit(1)

    # Read and parse tasks
    task_file = Path(args.file)
    if not task_file.exists():
        print(f"ERROR: File not found: {args.file}")
        sys.exit(1)

    content = task_file.read_text()
    tasks = parse_tasks(content)
    print(f"Found {len(tasks)} tasks to create\n")

    if not tasks:
        print("No tasks found. Verify the file uses TASK_NAME_START/END "
              "and TASK_DESCRIPTION_START/END markers.")
        sys.exit(0)

    # Create issues
    results = []
    for i, task in enumerate(tasks, 1):
        print(f"Task {i}: {task['name']}")
        result = create_issue(task, config)
        result["name"] = task["name"]
        results.append(result)
        if result["status"] == "success":
            print(f"  Created — ID: {result['id']}\n")
        else:
            detail = result.get("response", result.get("error", "Unknown"))
            print(f"  FAILED — {detail}\n")

    # Summary
    success = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] != "success"]
    print(f"\n{'=' * 60}")
    print(f"Summary: {len(success)} of {len(tasks)} tasks created successfully")
    if failed:
        print(f"Failed: {len(failed)}")
    print(f"{'=' * 60}")

    if success:
        print("\nTask ID Mapping:")
        for r in success:
            print(f"  {r['name'][:70]}")
            print(f"    ID: {r['id']}")


if __name__ == "__main__":
    main()
```

### 3. Execute

```bash
cd "local-docs/project-automation/task-creation/plane-api" && python3 "local-docs/project-automation/skills-engineering/plane-api-commands/scripts/create-plane-issues.py" --file "/path/to/implementation-tasks-YYYY-MM-DD-XXX.md"
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

- System IDs: `local-docs/project-automation/task-creation/plane-api/samasu-system-variables.md`
- Task artifacts: `local-docs/project-automation/task-creation/YYYY-MM-DD/implementation-tasks-*.md`
- Plane API docs: https://developers.plane.so/api-reference/introduction

## Deployment

Copy this file to `.cursor/rules/plane-api-commands.mdc` for Cursor to detect it.
