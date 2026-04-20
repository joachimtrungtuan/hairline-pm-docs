#!/usr/bin/env python3
"""
Set parent work item for a list of issue sequence IDs.

Usage (from plane-api directory):
  python3 ../../skills-engineering/plane-api-commands/scripts/set-parent-by-sequence.py \
    --parent-sequence 1055 --child-sequences 1109,1112
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


def fetch_work_items_page(config: dict, cursor: str | None = None) -> tuple[list[dict], str | None]:
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


def patch_parent(config: dict, work_item_id: str, parent_id: str) -> bool:
    base = config["BASE_URL"]
    ws = config["WORKSPACE_SLUG"]
    proj = config["PROJECT_ID"]
    url = f"{base}/workspaces/{ws}/projects/{proj}/work-items/{work_item_id}/"
    # Plane accepts parent as internal UUID in "parent" field.
    code, resp = curl_json("PATCH", url, config["PLANE_API_KEY"], {"parent": parent_id})
    if code != 0:
        print(f"  PATCH failed: {resp}")
        return False
    if isinstance(resp, dict) and resp.get("id"):
        return True
    print(f"  PATCH unexpected response: {resp!r}")
    return False


def get_detail(config: dict, work_item_id: str) -> dict:
    base = config["BASE_URL"]
    ws = config["WORKSPACE_SLUG"]
    proj = config["PROJECT_ID"]
    url = f"{base}/workspaces/{ws}/projects/{proj}/work-items/{work_item_id}/"
    code, resp = curl_json("GET", url, config["PLANE_API_KEY"])
    if code != 0 or not isinstance(resp, dict):
        print(f"ERROR reading work item {work_item_id}: {resp}")
        sys.exit(1)
    return resp


def main() -> None:
    parser = argparse.ArgumentParser(description="Set parent for work items by sequence.")
    parser.add_argument("--env", default=".env", help="Path to .env (default: cwd .env)")
    parser.add_argument("--parent-sequence", required=True, type=int, help="Parent issue sequence_id")
    parser.add_argument("--child-sequences", required=True, help="Comma-separated child sequence_ids")
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
        child_sequences = {int(x.strip()) for x in args.child_sequences.split(",") if x.strip()}
    except ValueError:
        print("ERROR: --child-sequences must be comma-separated integers")
        sys.exit(1)

    targets = set(child_sequences)
    targets.add(args.parent_sequence)
    seq_to_id = find_issue_maps(config, targets)
    missing = targets - set(seq_to_id.keys())
    if missing:
        print(f"ERROR: Could not resolve sequence_ids: {sorted(missing)}")
        sys.exit(1)

    parent_id = seq_to_id[args.parent_sequence]
    print(f"Resolved parent HAIRL-{args.parent_sequence} -> {parent_id}")

    ok = 0
    for seq in sorted(child_sequences):
        child_id = seq_to_id[seq]
        detail = get_detail(config, child_id)
        current_parent = detail.get("parent")
        if isinstance(current_parent, dict):
            current_parent_id = current_parent.get("id")
        else:
            current_parent_id = current_parent
        if current_parent_id == parent_id:
            print(f"HAIRL-{seq}: parent unchanged")
            ok += 1
            continue
        print(f"HAIRL-{seq}: setting parent -> HAIRL-{args.parent_sequence}")
        if args.dry_run:
            ok += 1
            continue
        if patch_parent(config, child_id, parent_id):
            ok += 1
        else:
            print(f"  Failed HAIRL-{seq}")

    print(f"\nDone: {ok}/{len(child_sequences)} processed.")


if __name__ == "__main__":
    main()
