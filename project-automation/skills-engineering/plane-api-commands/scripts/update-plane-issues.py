#!/usr/bin/env python3
"""
Update existing Plane.so issues with cleaned HTML descriptions.

Usage:
    python3 update-plane-issues.py --file <path-to-tasks.md> --start-issue <HAIRL-XXX>

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


def get_issue_id(issue_identifier: str, config: dict) -> str:
    """Get the internal UUID for an issue from its identifier (e.g., HAIRL-892)."""
    url = (
        f"{config['BASE_URL']}/workspaces/{config['WORKSPACE_SLUG']}"
        f"/projects/{config['PROJECT_ID']}/issues/?fields=id,sequence_id"
    )
    cmd = [
        "curl", "-s", "-X", "GET", url,
        "-H", f"X-API-Key: {config['PLANE_API_KEY']}",
        "-H", "Content-Type: application/json",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        try:
            resp = json.loads(result.stdout)
            # Extract the sequence number from identifier (e.g., "HAIRL-892" -> 892)
            seq_num = int(issue_identifier.split("-")[1])
            # Find the issue with matching sequence_id
            for issue in resp.get("results", []):
                if issue.get("sequence_id") == seq_num:
                    return issue.get("id")
        except (json.JSONDecodeError, ValueError, IndexError):
            pass
    return None


def update_issue(issue_identifier: str, task: dict, config: dict) -> dict:
    """Update one Plane issue via API."""
    # Get the internal UUID for the issue
    issue_id = get_issue_id(issue_identifier, config)
    if not issue_id:
        return {
            "status": "error",
            "error": f"Could not find issue {issue_identifier}"
        }
    
    payload = {
        "description_html": task["description"],
    }
    url = (
        f"{config['BASE_URL']}/workspaces/{config['WORKSPACE_SLUG']}"
        f"/projects/{config['PROJECT_ID']}/issues/{issue_id}/"
    )
    cmd = [
        "curl", "-s", "-X", "PATCH", url,
        "-H", f"X-API-Key: {config['PLANE_API_KEY']}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        try:
            resp = json.loads(result.stdout)
            if "id" in resp:
                return {
                    "status": "success",
                    "identifier": issue_identifier,
                    "id": resp["id"]
                }
            return {"status": "error", "response": result.stdout}
        except json.JSONDecodeError:
            return {"status": "error", "response": result.stdout}
    return {"status": "error", "error": result.stderr}


def main():
    parser = argparse.ArgumentParser(
        description="Update existing Plane issues with cleaned HTML descriptions."
    )
    parser.add_argument(
        "--file", required=True, help="Path to implementation tasks markdown file"
    )
    parser.add_argument(
        "--start-issue",
        required=True,
        help="Starting issue identifier (e.g., HAIRL-880)"
    )
    parser.add_argument(
        "--skip",
        type=int,
        default=0,
        help="Number of tasks to skip from the beginning of the file (default: 0)"
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
    }

    # Validate required config
    if not config["PROJECT_ID"]:
        print("ERROR: Missing PROJECT_ID in .env")
        sys.exit(1)

    # Read and parse tasks
    task_file = Path(args.file)
    if not task_file.exists():
        print(f"ERROR: File not found: {args.file}")
        sys.exit(1)

    content = task_file.read_text()
    all_tasks = parse_tasks(content)
    
    # Skip tasks if requested
    if args.skip > 0:
        if args.skip >= len(all_tasks):
            print(f"ERROR: Cannot skip {args.skip} tasks, only {len(all_tasks)} tasks found")
            sys.exit(1)
        tasks = all_tasks[args.skip:]
        print(f"Found {len(all_tasks)} tasks, skipping first {args.skip}, updating {len(tasks)} tasks\n")
    else:
        tasks = all_tasks
        print(f"Found {len(tasks)} tasks to update\n")

    if not tasks:
        print("No tasks to update after skipping.")
        sys.exit(0)

    # Parse starting issue number
    try:
        project_prefix = args.start_issue.split("-")[0]
        start_num = int(args.start_issue.split("-")[1])
    except (IndexError, ValueError):
        print(f"ERROR: Invalid issue identifier format: {args.start_issue}")
        print("Expected format: HAIRL-XXX")
        sys.exit(1)

    # Update issues
    results = []
    for i, task in enumerate(tasks):
        issue_identifier = f"{project_prefix}-{start_num + i}"
        print(f"Updating {issue_identifier}: {task['name']}")
        result = update_issue(issue_identifier, task, config)
        result["name"] = task["name"]
        result["identifier"] = issue_identifier
        results.append(result)
        
        if result["status"] == "success":
            print(f"  ✓ Updated successfully\n")
        else:
            detail = result.get("response", result.get("error", "Unknown"))
            print(f"  ✗ FAILED — {detail}\n")

    # Summary
    success = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] != "success"]
    print(f"\n{'=' * 60}")
    print(f"Summary: {len(success)} of {len(tasks)} tasks updated successfully")
    if failed:
        print(f"Failed: {len(failed)}")
        for r in failed:
            print(f"  - {r.get('identifier', 'Unknown')}: {r['name'][:50]}")
    print(f"{'=' * 60}")

    if success:
        print("\nUpdated Issues:")
        for r in success:
            print(f"  {r['identifier']}: {r['name'][:70]}")


if __name__ == "__main__":
    main()
