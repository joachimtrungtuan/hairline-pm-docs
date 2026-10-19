#!/usr/bin/env python3
"""Read the current state of Plane work items by readable key. Read-only: GET requests only."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from plane_api_common import load_config, paginated_get, print_json, project_path


def parse_keys(raw: str, identifier: str) -> dict[int, str]:
    key_re = re.compile(rf"^{re.escape(identifier)}-(\d+)$", re.IGNORECASE)
    targets: dict[int, str] = {}
    for part in raw.split(","):
        key = part.strip()
        if not key:
            continue
        match = key_re.match(key)
        if not match:
            raise SystemExit(f"ERROR: Invalid key {key!r}; expected {identifier}-<number>")
        targets[int(match.group(1))] = f"{identifier}-{int(match.group(1))}"
    if not targets:
        raise SystemExit("ERROR: --keys is empty")
    return targets


def state_id_of(item: dict[str, Any]) -> str:
    state = item.get("state")
    if isinstance(state, dict):
        return str(state.get("id") or "")
    return str(state or "")


def main() -> None:
    parser = argparse.ArgumentParser(description="Read Plane work-item states by key (read-only).")
    parser.add_argument("--env", default=".env", help="Path to .env (default: cwd .env)")
    parser.add_argument("--values", default="plane-values.json", help="Plane values cache with project and states")
    parser.add_argument("--keys", required=True, help="Comma-separated keys, for example HAIRL-1600,HAIRL-1601")
    parser.add_argument("--output", help="Write the states JSON here instead of printing it")
    args = parser.parse_args()

    values = json.loads(Path(args.values).read_text(encoding="utf-8"))
    identifier = (values.get("project") or {}).get("identifier")
    if not identifier:
        raise SystemExit("ERROR: project identifier missing in values cache; run fetch-plane-values.py")
    states = {s["id"]: s for s in values.get("states", []) if s.get("id")}
    targets = parse_keys(args.keys, identifier)

    config = load_config(Path(args.env))
    items = paginated_get(config, project_path(config, "/work-items/?per_page=100"))

    result: dict[str, dict[str, Any]] = {}
    unknown_state_ids: set[str] = set()
    for item in items:
        seq = item.get("sequence_id")
        if seq not in targets:
            continue
        sid = state_id_of(item)
        state = states.get(sid)
        if state is None:
            unknown_state_ids.add(sid)
            result[targets[seq]] = {"state": sid, "group": None}
        else:
            result[targets[seq]] = {"state": state.get("name"), "group": state.get("group")}

    ordered = {targets[seq]: result[targets[seq]] for seq in sorted(targets) if targets[seq] in result}
    missing = [targets[seq] for seq in sorted(targets) if targets[seq] not in result]

    if args.output:
        Path(args.output).write_text(json.dumps(ordered, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print_json({"output": args.output, "found": len(ordered), "missing": missing,
                    "unknown_state_ids": sorted(unknown_state_ids)})
    else:
        print_json({"states": ordered, "missing": missing, "unknown_state_ids": sorted(unknown_state_ids)})
    if unknown_state_ids:
        print("WARNING: some state IDs are not in the values cache; run fetch-plane-values.py and retry")
    if missing:
        raise SystemExit(f"ERROR: {len(missing)} key(s) not found (deleted, archived, or another project): {missing}")


if __name__ == "__main__":
    main()
