---
description: Run Plane.so API operations — list workspace resources or bulk-create issues from implementation task markdown files.
---

# Plane API Commands

Run Plane.so API workflows for listing resources and bulk-creating work items from local task markdown files. All credentials loaded from environment files — never hardcode or expose API keys.

## Supported Operations

Ask user to choose if not specified: `list-users`, `list-projects`, `list-modules`, `list-tags`, `list-work-item-types`, `list-stages`, `create-work-item`

## Prerequisites

- `.env` at `local-docs/project-automation/task-creation/plane-api/.env` with `PLANE_API_KEY`
- System variables at `local-docs/project-automation/task-creation/plane-api/samasu-system-variables.md`
- Tools: `python3`, `curl` (`jq` optional)

## Credential Rules (CRITICAL)

- ALWAYS load `PLANE_API_KEY` from `.env` file
- NEVER hardcode, print, echo, log, or embed the API key in scripts, output, or commits
- If `.env` missing or key empty, ask user to create/populate it
- If permission denied, ask user to grant file access — do not request key in plain text

## Default Configuration

Load IDs from `samasu-system-variables.md`. Defaults: `WORKSPACE_SLUG=samasu-digital`, `BASE_URL=https://api.plane.so/api/v1`. For project/assignee/stage/priority/issue type IDs: always reference config file, never hardcode UUIDs.

## Task File Contract

Required block format for creating issues:

```
## TASK_NAME_START
[PREFIX] Task Name
## TASK_NAME_END

**Status**: Drafted

## TASK_DESCRIPTION_START
<h2>Overview</h2>
<p>...</p>
## TASK_DESCRIPTION_END
```

Prefixes: `[FE+BE TASK]`, `[FE TASK]`, `[BE TASK]`, `[BUG]`, `[UX/UI TASK]`
Statuses: `Drafted`, `Confirmed`, `Added to Plane`
Description must be valid HTML for Plane.so `description_html` field.

## Steps

1. Ask user which operation to run (list or create).

// turbo
2. Load credentials using Python (not bash source):
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
```

3. For **list operations**: run curl against `https://api.plane.so/api/v1/workspaces/samasu-digital/...` with API key header. Display formatted results.

4. For **create-work-item**: ask user for implementation task file path. Before executing, write the following script **exactly** to `local-docs/project-automation/skills-engineering/plane-api-commands/scripts/create-plane-issues.py`. Do not modify — recreate verbatim for consistent results.

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

    env_path = Path(args.env)
    env_vars = load_env(env_path)

    api_key = env_vars.get("PLANE_API_KEY", "")
    if not api_key:
        print("ERROR: PLANE_API_KEY not found in .env file.")
        print("Add it to your .env: PLANE_API_KEY=plane_api_...")
        sys.exit(1)

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

    missing = [
        k for k in ["PROJECT_ID", "ASSIGNEE_ID", "STAGE_ID", "ISSUE_TYPE_ID"]
        if not config[k]
    ]
    if missing:
        print(f"ERROR: Missing required config in .env: {', '.join(missing)}")
        print("Reference: local-docs/project-automation/task-creation/plane-api/samasu-system-variables.md")
        sys.exit(1)

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

// turbo
5. Execute:
```bash
cd "local-docs/project-automation/task-creation/plane-api" && python3 "local-docs/project-automation/skills-engineering/plane-api-commands/scripts/create-plane-issues.py" --file "/path/to/implementation-tasks-YYYY-MM-DD-XXX.md"
```

6. Report results: total tasks found/created, task-to-issue-ID mapping, any errors with fixes.

## Why Python (not bash)

`json.dumps()` correctly escapes quotes, newlines, and HTML in multiline descriptions. Lower failure rate than bash string quoting. Clearer error handling.

## API Reference

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

## Error Reference

| Code | Meaning | Fix |
|------|---------|-----|
| 401 | Invalid/expired key | Regenerate in Plane settings, update `.env` |
| 400 | Validation error | Check fields and HTML format |
| 404 | Invalid IDs | Verify in `samasu-system-variables.md` |
| 429 | Rate limit (60/min) | Add delay |
| 5xx | Server error | Retry with backoff |

## References

- System IDs: `local-docs/project-automation/task-creation/plane-api/samasu-system-variables.md`
- Task artifacts: `local-docs/project-automation/task-creation/YYYY-MM-DD/implementation-tasks-*.md`
- Plane API docs: https://developers.plane.so/api-reference/introduction

## Deployment

Copy this file to `.agent/workflows/plane-api-commands.md` for Antigravity to detect it.
