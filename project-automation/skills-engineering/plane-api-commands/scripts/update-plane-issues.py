#!/usr/bin/env python3
"""Update existing Plane work item descriptions from task markdown files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from plane_api_common import (
    UUID_RE,
    api_request,
    load_config,
    paginated_get,
    parse_tasks,
    project_path,
)


def metadata_value(task: dict[str, Any], key: str) -> str:
    return str(task["metadata"].get(key.lower(), "")).strip()


def find_work_item_id_by_sequence(config, sequence_id: int) -> str:
    items = paginated_get(
        config,
        project_path(config, "/work-items/?fields=id,sequence_id&per_page=100"),
    )
    for item in items:
        if item.get("sequence_id") == sequence_id and isinstance(item.get("id"), str):
            return item["id"]
    raise SystemExit(f"ERROR: Could not resolve HAIRL-{sequence_id} in this project")


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


def update_description(config, work_item_id: str, description_html: str) -> None:
    body, status = api_request(
        config,
        "PATCH",
        project_path(config, f"/work-items/{work_item_id}/"),
        {"description_html": description_html},
    )
    if status >= 400 or status == 0 or not isinstance(body, dict) or not body.get("id"):
        raise SystemExit(f"ERROR: Update failed HTTP {status}: {body}")


def task_slice(tasks: list[dict[str, Any]], skip: int, limit: int | None) -> list[dict[str, Any]]:
    selected = tasks[skip:]
    if limit is not None:
        selected = selected[:limit]
    return selected


def main() -> None:
    parser = argparse.ArgumentParser(description="Update Plane work item descriptions from task markdown.")
    parser.add_argument("--file", required=True, help="Path to implementation task markdown")
    parser.add_argument("--env", default=".env", help="Path to .env")
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
    task_path = Path(args.file)
    if not task_path.exists():
        raise SystemExit(f"ERROR: File not found: {task_path}")
    tasks = task_slice(parse_tasks(task_path.read_text(encoding="utf-8")), args.skip, args.limit)
    if not tasks:
        raise SystemExit("ERROR: No task blocks found for update")

    print(f"Found {len(tasks)} task(s) to update")
    for index, task in enumerate(tasks):
        fallback_sequence = args.start_sequence + index if args.start_sequence is not None else None
        work_item_id = resolve_work_item_id(config, task, fallback_sequence)
        print(f"{index + 1}. {task['name']} -> {work_item_id}")
        if args.dry_run:
            continue
        update_description(config, work_item_id, task["description"])
        print("   updated")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Interrupted")
