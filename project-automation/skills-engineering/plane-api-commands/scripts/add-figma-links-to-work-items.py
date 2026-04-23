#!/usr/bin/env python3
"""
Upsert Figma links inside the existing Reference section in Plane descriptions.

Usage (from plane-api directory):
  python3 ../../skills-engineering/plane-api-commands/scripts/add-figma-links-to-work-items.py \
    --sequences 1109-1126
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


SCREEN_LINKS = {
    "1": "https://www.figma.com/design/owSvN5vzSKnD60dA9GMBZe/-SD--Hairline---Admin-Dashboard?node-id=2471-87618",
    "2": "https://www.figma.com/design/owSvN5vzSKnD60dA9GMBZe/-SD--Hairline---Admin-Dashboard?node-id=90-67454",
    "3": "https://www.figma.com/design/owSvN5vzSKnD60dA9GMBZe/-SD--Hairline---Admin-Dashboard?node-id=90-67454",
    "4": "https://www.figma.com/design/owSvN5vzSKnD60dA9GMBZe/-SD--Hairline---Admin-Dashboard?node-id=90-67455",
    "4a": "https://www.figma.com/design/owSvN5vzSKnD60dA9GMBZe/-SD--Hairline---Admin-Dashboard?node-id=90-67455",
    "4b": "https://www.figma.com/design/owSvN5vzSKnD60dA9GMBZe/-SD--Hairline---Admin-Dashboard?node-id=90-67455",
    "5": "https://www.figma.com/design/owSvN5vzSKnD60dA9GMBZe/-SD--Hairline---Admin-Dashboard?node-id=90-67456",
    "6": "https://www.figma.com/design/owSvN5vzSKnD60dA9GMBZe/-SD--Hairline---Admin-Dashboard?node-id=2734-18919",
    "7": "https://www.figma.com/design/owSvN5vzSKnD60dA9GMBZe/-SD--Hairline---Admin-Dashboard?node-id=2771-260468",
    "8": "https://www.figma.com/design/owSvN5vzSKnD60dA9GMBZe/-SD--Hairline---Admin-Dashboard?node-id=2829-359253",
    "9": "https://www.figma.com/design/Krs1cGIozAJUedZnBaHkEv/-SD--Hairline---Provider-Dashboard?node-id=9-47590",
    "10": "https://www.figma.com/design/Krs1cGIozAJUedZnBaHkEv/-SD--Hairline---Provider-Dashboard?node-id=9-47591",
}


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


def parse_screen_tokens(text: str) -> list[str]:
    matches = re.findall(r"Screen\s+(\d+[a-zA-Z]?)", text, flags=re.IGNORECASE)
    ordered: list[str] = []
    for m in matches:
        token = m.lower()
        if token not in ordered and token in SCREEN_LINKS:
            ordered.append(token)
    return ordered


def infer_screens(name: str, description_html: str) -> list[str]:
    # FE tasks: prefer screen in task title.
    if "[FE TASK]" in name:
        from_name = parse_screen_tokens(name)
        if from_name:
            return from_name
    # BE tasks: infer from description content (supports Screen X, Screen Y...).
    from_desc = parse_screen_tokens(description_html)
    return from_desc


def build_figma_items(screens: list[str]) -> str:
    lines: list[str] = []
    for s in screens:
        lines.append(
            f'<li>Figma - Screen {s.upper()}: <a href="{SCREEN_LINKS[s]}">{SCREEN_LINKS[s]}</a></li>'
        )
    return "".join(lines)


def upsert_reference_links(html: str, figma_items: str) -> str:
    cleaned = html.strip()
    # Remove previously added Figma References block, if any.
    cleaned = re.sub(
        r"<h2>\s*Figma References\s*</h2>\s*<ul>[\s\S]*?</ul>",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    # Replace existing Figma list items if they are already inside Reference section.
    cleaned = re.sub(
        r"<li>\s*Figma\s*-\s*Screen\s*[\w]+\s*:\s*<a href=\"https://www\.figma\.com/design/[^\"]+\">https://www\.figma\.com/design/[^\"]+</a>\s*</li>",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    ref_pattern = re.compile(r"(<h2>\s*Reference\s*</h2>\s*<ul>)([\s\S]*?)(</ul>)", flags=re.IGNORECASE)
    match = ref_pattern.search(cleaned)
    if match:
        prefix, body, suffix = match.group(1), match.group(2), match.group(3)
        new_body = body.strip() + figma_items
        replacement = prefix + new_body + suffix
        return cleaned[: match.start()] + replacement + cleaned[match.end() :]

    # Fallback when no Reference section exists.
    return cleaned + "<h2>Reference</h2><ul>" + figma_items + "</ul>"


def patch_description(config: dict, work_item_id: str, description_html: str) -> bool:
    base = config["BASE_URL"]
    ws = config["WORKSPACE_SLUG"]
    proj = config["PROJECT_ID"]
    url = f"{base}/workspaces/{ws}/projects/{proj}/work-items/{work_item_id}/"
    code, resp = curl_json(
        "PATCH",
        url,
        config["PLANE_API_KEY"],
        {"description_html": description_html},
    )
    if code != 0:
        print(f"  PATCH failed: {resp}")
        return False
    return isinstance(resp, dict) and bool(resp.get("id"))


def parse_sequences(raw: str) -> set[int]:
    out: set[int] = set()
    for part in raw.split(","):
        p = part.strip()
        if not p:
            continue
        if "-" in p:
            start_str, end_str = p.split("-", 1)
            start = int(start_str)
            end = int(end_str)
            if end < start:
                start, end = end, start
            out.update(range(start, end + 1))
        else:
            out.add(int(p))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Add Figma links to Plane work item descriptions.")
    parser.add_argument("--env", default=".env", help="Path to .env (default: cwd .env)")
    parser.add_argument("--sequences", required=True, help="Comma/range list, e.g. 1109-1126")
    parser.add_argument("--dry-run", action="store_true", help="Show plan only")
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

    targets = parse_sequences(args.sequences)
    seq_to_id = find_issue_maps(config, targets)
    missing = targets - set(seq_to_id.keys())
    if missing:
        print(f"ERROR: Could not resolve sequence_ids: {sorted(missing)}")
        sys.exit(1)

    updated = 0
    skipped = 0
    for seq in sorted(targets):
        wid = seq_to_id[seq]
        detail = get_detail(config, wid)
        name = str(detail.get("name") or "")
        html = str(detail.get("description_html") or "")
        screens = infer_screens(name, html)
        if not screens:
            print(f"HAIRL-{seq}: no screen mapping found, skipped")
            skipped += 1
            continue
        new_html = upsert_reference_links(html, build_figma_items(screens))
        print(f"HAIRL-{seq}: screens={','.join(screens)}")
        if args.dry_run:
            updated += 1
            continue
        if patch_description(config, wid, new_html):
            updated += 1
        else:
            print(f"  Failed HAIRL-{seq}")

    print(f"\nDone: {updated}/{len(targets)} processed, skipped {skipped}.")


if __name__ == "__main__":
    main()
