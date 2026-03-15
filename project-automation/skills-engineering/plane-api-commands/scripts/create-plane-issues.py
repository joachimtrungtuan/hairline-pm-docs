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


def load_label_ids(system_vars_path: Path) -> dict:
    """
    Best-effort parse of label IDs from samasu-system-variables.md.

    Supports lines like:
    - **UX/UI** - `uuid`
    - * UX/UI: `uuid`
    """
    if not system_vars_path.exists():
        return {}
    text = system_vars_path.read_text(encoding="utf-8")
    label_ids: dict[str, str] = {}

    patterns = [
        r"^\s*\d+\.\s*\*\*(?P<name>[^*]+)\*\*\s*-\s*`(?P<id>[a-f0-9-]{36})`",
        r"^\s*\*\s*(?P<name>[^:]+):\s*`(?P<id>[a-f0-9-]{36})`",
    ]
    for line in text.splitlines():
        for pat in patterns:
            m = re.match(pat, line.strip(), re.IGNORECASE)
            if m:
                name = m.group("name").strip()
                label_id = m.group("id").strip()
                label_ids[name] = label_id
                break

    return label_ids


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
        # Clean HTML to remove excessive spaces
        desc = clean_html(desc)
        tasks.append({"name": name, "description": desc})
    return tasks


def create_issue(task: dict, config: dict) -> dict:
    """Create one Plane work item via API."""
    labels: list[str] = []
    if "[UX/UI TASK]" in task["name"]:
        ux_label_id = config.get("LABEL_UX_UI_ID")
        if ux_label_id:
            labels.append(ux_label_id)

    payload = {
        "name": task["name"],
        "description_html": task["description"],
        "project": config["PROJECT_ID"],
        "assignees": [config["ASSIGNEE_ID"]],
        "state": config["STAGE_ID"],
        "priority": config.get("PRIORITY", "medium"),
        # Plane API v1 uses "type" for work item type
        "type": config["ISSUE_TYPE_ID"],
    }
    if labels:
        payload["labels"] = labels

    url = (
        f"{config['BASE_URL']}/workspaces/{config['WORKSPACE_SLUG']}"
        f"/projects/{config['PROJECT_ID']}/work-items/"
    )
    cmd = [
        "curl", "-sS", "-X", "POST", url,
        "-H", f"X-API-Key: {config['PLANE_API_KEY']}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload),
        "-w", "\n__HTTP_STATUS__:%{http_code}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return {"status": "error", "error": result.stderr.strip() or "curl failed"}

    body, _, status = result.stdout.rpartition("\n__HTTP_STATUS__:")
    status = status.strip() or "000"

    try:
        resp = json.loads(body) if body.strip() else {}
    except json.JSONDecodeError:
        resp = None

    if status.startswith("2") and isinstance(resp, dict):
        plane_id = (
            resp.get("sequence_id")
            or resp.get("identifier")
            or resp.get("id")
            or resp.get("uuid")
        )
        if plane_id is not None:
            return {
                "status": "success",
                "id": plane_id,
                "http_status": status,
            }

    response_text = body.strip()
    if isinstance(resp, dict) and resp:
        response_text = json.dumps(resp)
    return {
        "status": "error",
        "http_status": status,
        "response": response_text or "(empty response body)",
    }


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
    label_ids = load_label_ids(Path("samasu-system-variables.md"))
    config = {
        "PLANE_API_KEY": api_key,
        "WORKSPACE_SLUG": env_vars.get("WORKSPACE_SLUG", "samasu-digital"),
        "BASE_URL": env_vars.get("BASE_URL", "https://api.plane.so/api/v1"),
        "PROJECT_ID": env_vars.get("PROJECT_ID", ""),
        "ASSIGNEE_ID": env_vars.get("ASSIGNEE_ID", ""),
        "STAGE_ID": env_vars.get("STAGE_ID", ""),
        "PRIORITY": env_vars.get("PRIORITY", "medium"),
        "ISSUE_TYPE_ID": env_vars.get("ISSUE_TYPE_ID", ""),
        "LABEL_UX_UI_ID": env_vars.get("LABEL_UX_UI_ID", label_ids.get("UX/UI", "")),
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
            print(
                f"  Created — ID: {result['id']} "
                f"(HTTP {result.get('http_status', 'unknown')})\n"
            )
        else:
            http_status = result.get("http_status", "unknown")
            detail = result.get("response", result.get("error", "Unknown"))
            print(f"  FAILED — HTTP {http_status}: {detail}\n")

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
