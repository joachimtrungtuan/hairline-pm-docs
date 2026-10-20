#!/usr/bin/env python3
"""Update existing Plane work items from task markdown files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from plane_api_common import (
    UUID_RE,
    add_to_cycle,
    add_to_milestone,
    add_to_module,
    api_request,
    find_work_item_id_by_sequence,
    load_config,
    load_values,
    metadata_value,
    parse_tasks,
    project_path,
    resolve_work_item_fields,
    set_parent,
    verify_work_item,
)

# Field name -> work-item payload keys sent by PATCH. Relation fields use their own endpoints.
PATCH_FIELDS = {
    "name": ["name"],
    "description": ["description_html"],
    "state": ["state"],
    "priority": ["priority"],
    "type": ["type"],
    "assignees": ["assignees"],
    "labels": ["labels"],
    "dates": ["start_date", "target_date"],
}
RELATION_FIELDS = {"parent", "cycle", "module", "milestone"}
ALL_FIELDS = set(PATCH_FIELDS) | RELATION_FIELDS
# Verification names for each field option (description is checked by the PATCH response).
VERIFY_NAMES = {"dates": {"start_date", "target_date"}}


def resolve_work_item_id(config, task: dict[str, Any], fallback_sequence: int | None) -> str:
    explicit_id = metadata_value(task, "plane task id")
    if explicit_id:
        if not UUID_RE.match(explicit_id):
            raise SystemExit(
                f"ERROR: Plane Task ID must be the internal UUID, got {explicit_id!r}"
            )
        return explicit_id
    if fallback_sequence is None:
        raise SystemExit(
            f"ERROR: Task has no Plane Task ID and no --start-sequence was provided: {task['name']}"
        )
    return find_work_item_id_by_sequence(config, fallback_sequence)


def parse_fields(raw: str) -> set[str]:
    fields = {part.strip().lower() for part in raw.split(",") if part.strip()}
    if "all" in fields:
        return set(ALL_FIELDS)
    unknown = fields - ALL_FIELDS
    if unknown:
        raise SystemExit(f"ERROR: Unknown --fields value(s): {sorted(unknown)}. Allowed: {sorted(ALL_FIELDS)} or all")
    return fields


def update_work_item(config, work_item_id: str, resolved: dict[str, Any], fields: set[str]) -> None:
    payload = resolved["payload"]
    patch = {key: payload[key] for field in fields & set(PATCH_FIELDS) for key in PATCH_FIELDS[field]}
    if patch:
        body, status = api_request(
            config, "PATCH", project_path(config, f"/work-items/{work_item_id}/"), patch
        )
        if status >= 400 or status == 0 or not isinstance(body, dict) or not body.get("id"):
            raise SystemExit(f"ERROR: Update failed HTTP {status}: {body}")
    if "parent" in fields:
        set_parent(config, work_item_id, resolved["parent_id"])
    if "cycle" in fields:
        add_to_cycle(config, work_item_id, resolved["cycle_id"])
    if "module" in fields:
        add_to_module(config, work_item_id, resolved["module_id"])
    if "milestone" in fields:
        add_to_milestone(config, work_item_id, resolved["milestone_id"])


def task_slice(tasks: list[dict[str, Any]], skip: int, limit: int | None) -> list[dict[str, Any]]:
    selected = tasks[skip:]
    if limit is not None:
        selected = selected[:limit]
    return selected


def main() -> None:
    parser = argparse.ArgumentParser(description="Update Plane work items from task markdown.")
    parser.add_argument("--file", required=True, help="Path to implementation task markdown")
    parser.add_argument("--env", default=".env", help="Path to .env")
    parser.add_argument("--values", default="plane-values.json", help="Path to fetched Plane values JSON")
    parser.add_argument(
        "--fields",
        default="description",
        help=f"Comma-separated fields to push: {','.join(sorted(ALL_FIELDS))}, or all (default: description)",
    )
    parser.add_argument("--skip", type=int, default=0, help="Skip first N tasks")
    parser.add_argument("--limit", type=int, default=None, help="Update at most N tasks")
    parser.add_argument(
        "--start-sequence",
        type=int,
        default=None,
        help="Fallback first HAIRL sequence when task blocks do not have Plane Task ID UUID",
    )
    parser.add_argument("--dry-run", action="store_true", help="Validate only")
    args = parser.parse_args()

    config = load_config(Path(args.env))
    fields = parse_fields(args.fields)
    values = load_values(Path(args.values)) if fields != {"description"} else {}
    task_path = Path(args.file)
    if not task_path.exists():
        raise SystemExit(f"ERROR: File not found: {task_path}")
    tasks = task_slice(parse_tasks(task_path.read_text(encoding="utf-8")), args.skip, args.limit)
    if not tasks:
        raise SystemExit("ERROR: No task blocks found for update")

    verify_fields = set().union(*(VERIFY_NAMES.get(f, {f}) for f in fields))
    print(f"Found {len(tasks)} task(s) to update; fields={','.join(sorted(fields))}")
    for index, task in enumerate(tasks):
        fallback_sequence = args.start_sequence + index if args.start_sequence is not None else None
        work_item_id = resolve_work_item_id(config, task, fallback_sequence)
        if fields == {"description"}:
            resolved = {"payload": {"description_html": task["description"]}}
        else:
            resolved = resolve_work_item_fields(task, config, values)
        print(f"{index + 1}. {task['name']} -> {work_item_id}")
        if args.dry_run:
            continue
        update_work_item(config, work_item_id, resolved, fields)
        if fields != {"description"}:
            problems = verify_work_item(config, work_item_id, resolved, verify_fields)
            if problems:
                raise SystemExit(f"ERROR: {work_item_id} updated but fields did not persist: " + "; ".join(problems))
        print("   updated")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Interrupted")
