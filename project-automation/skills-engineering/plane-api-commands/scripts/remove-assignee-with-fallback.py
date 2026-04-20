#!/usr/bin/env python3
"""
Remove a user from Plane work item assignees. If no assignees remain, add fallback.

Usage (from plane-api directory):
  python3 ../../skills-engineering/plane-api-commands/scripts/remove-assignee-with-fallback.py \\
    --remove-user-id <uuid> --fallback-user-id <uuid> \\
    --sequences 1109,1110,1111
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def load_env(env_path: Path) -> dict:
    env_vars: dict[str, str] = {}
    if not env_path.exists():
        print(f"ERROR: .env file not found at {env_path}")
        sys.exit(1)
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                env_vars[key.strip()] = value.strip().strip('"').strip("'")
    return env_vars


def curl_json(method: str, url: str, api_key: str, data: dict | None = None) -> tuple[int, dict | list | str]:
    cmd = [
        "curl",
        "-sS",
        "-X",
        method,
        url,
        "-H",
        f"X-API-Key: {api_key}",
        "-H",
        "Content-Type: application/json",
    ]
    if data is not None:
        cmd.extend(["-d", json.dumps(data)])
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return result.returncode, result.stderr or "curl failed"
    try:
        return 0, json.loads(result.stdout) if result.stdout.strip() else {}
    except json.JSONDecodeError:
        return 0, result.stdout


def collect_assignee_ids(raw: object) -> list[str]:
    """Normalize assignees from Plane detail/list payload to a list of user UUID strings."""
    if raw is None:
        return []
    if isinstance(raw, list):
        out: list[str] = []
        for item in raw:
            if isinstance(item, str):
                out.append(item)
            elif isinstance(item, dict):
                uid = item.get("id") or item.get("member") or item.get("assignee")
                if isinstance(uid, dict):
                    uid = uid.get("id")
                if isinstance(uid, str):
                    out.append(uid)
        return out
    return []


def fetch_work_items_page(
    config: dict, cursor: str | None = None
) -> tuple[list[dict], str | None]:
    base = config["BASE_URL"]
    ws = config["WORKSPACE_SLUG"]
    proj = config["PROJECT_ID"]
    url = f"{base}/workspaces/{ws}/projects/{proj}/work-items/"
    if cursor:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}cursor={cursor}"
    code, resp = curl_json("GET", url, config["PLANE_API_KEY"])
    if code != 0:
        print(f"ERROR listing work items: {resp}")
        sys.exit(1)
    if not isinstance(resp, dict):
        print(f"ERROR unexpected list response: {resp!r}")
        sys.exit(1)
    results = resp.get("results") or resp.get("data") or []
    if not isinstance(results, list):
        results = []
    next_c = resp.get("next_page_results") or resp.get("next_cursor") or resp.get("cursor")
    if isinstance(next_c, str) and next_c:
        return results, next_c
    return results, None


def find_issue_maps(config: dict, target_sequences: set[int]) -> dict[int, str]:
    """Resolve sequence_id -> work item UUID by paging until all targets found."""
    seq_to_id: dict[int, str] = {}
    cursor: str | None = None
    pages = 0
    while len(seq_to_id) < len(target_sequences) and pages < 500:
        batch, cursor = fetch_work_items_page(config, cursor)
        pages += 1
        for item in batch:
            if not isinstance(item, dict):
                continue
            sid = item.get("sequence_id")
            iid = item.get("id")
            if isinstance(sid, int) and isinstance(iid, str) and sid in target_sequences:
                seq_to_id[sid] = iid
        if cursor is None or not batch:
            break
    return seq_to_id


def get_work_item_detail(config: dict, work_item_id: str) -> dict:
    base = config["BASE_URL"]
    ws = config["WORKSPACE_SLUG"]
    proj = config["PROJECT_ID"]
    url = f"{base}/workspaces/{ws}/projects/{proj}/work-items/{work_item_id}/"
    code, resp = curl_json("GET", url, config["PLANE_API_KEY"])
    if code != 0 or not isinstance(resp, dict):
        print(f"ERROR fetching work item {work_item_id}: {resp}")
        sys.exit(1)
    return resp


def patch_assignees(config: dict, work_item_id: str, assignee_ids: list[str]) -> bool:
    base = config["BASE_URL"]
    ws = config["WORKSPACE_SLUG"]
    proj = config["PROJECT_ID"]
    url = f"{base}/workspaces/{ws}/projects/{proj}/work-items/{work_item_id}/"
    code, resp = curl_json(
        "PATCH",
        url,
        config["PLANE_API_KEY"],
        {"assignees": assignee_ids},
    )
    if code != 0:
        print(f"  PATCH failed: {resp}")
        return False
    if isinstance(resp, dict) and resp.get("id"):
        return True
    print(f"  PATCH unexpected response: {resp!r}")
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Remove assignee; keep at least one via fallback.")
    parser.add_argument("--env", default=".env", help="Path to .env (default: cwd .env)")
    parser.add_argument("--remove-user-id", required=True, help="User UUID to remove from assignees")
    parser.add_argument(
        "--fallback-user-id",
        required=True,
        help="User UUID to add only when removal would leave zero assignees",
    )
    parser.add_argument(
        "--sequences",
        required=True,
        help="Comma-separated sequence_ids (e.g. 1109,1110)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print planned changes only")
    args = parser.parse_args()

    env_vars = load_env(Path(args.env))
    api_key = env_vars.get("PLANE_API_KEY", "")
    if not api_key:
        print("ERROR: PLANE_API_KEY missing in .env")
        sys.exit(1)

    config = {
        "PLANE_API_KEY": api_key,
        "WORKSPACE_SLUG": env_vars.get("WORKSPACE_SLUG", "samasu-digital"),
        "BASE_URL": env_vars.get("BASE_URL", "https://api.plane.so/api/v1"),
        "PROJECT_ID": env_vars.get("PROJECT_ID", ""),
    }
    if not config["PROJECT_ID"]:
        print("ERROR: PROJECT_ID missing in .env")
        sys.exit(1)

    try:
        targets = {int(x.strip()) for x in args.sequences.split(",") if x.strip()}
    except ValueError:
        print("ERROR: --sequences must be comma-separated integers")
        sys.exit(1)

    remove_id = args.remove_user_id.strip()
    fallback_id = args.fallback_user_id.strip()

    print(f"Resolving {len(targets)} work items by sequence_id...")
    seq_to_id = find_issue_maps(config, targets)
    missing = targets - set(seq_to_id.keys())
    if missing:
        print(f"ERROR: Could not resolve sequence_ids: {sorted(missing)}")
        sys.exit(1)

    ok = 0
    for seq in sorted(targets):
        wid = seq_to_id[seq]
        detail = get_work_item_detail(config, wid)
        current = collect_assignee_ids(detail.get("assignees"))
        if not current:
            current = collect_assignee_ids(detail.get("issue_assignee"))
        new_list = [u for u in current if u != remove_id]
        action = "remove only"
        if not new_list:
            new_list = [fallback_id]
            action = f"replace with fallback (was only {remove_id[:8]}…)"
        elif remove_id not in current:
            action = "unchanged (remove user not assigned)"
            new_list = current
        print(f"HAIRL-{seq}: assignees {len(current)} -> {len(new_list)} ({action})")
        if args.dry_run:
            ok += 1
            continue
        if new_list == current:
            ok += 1
            continue
        if patch_assignees(config, wid, new_list):
            ok += 1
        else:
            print(f"  Failed HAIRL-{seq}")

    print(f"\nDone: {ok}/{len(targets)} processed.")


if __name__ == "__main__":
    main()
