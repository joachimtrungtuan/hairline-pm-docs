#!/usr/bin/env python3
"""Create Plane work items from implementation task markdown files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from plane_api_common import (
    UUID_RE,
    active_cycle,
    api_request,
    issue_key,
    load_config,
    load_values,
    lookup_id,
    normalize_priority,
    paginated_get,
    parse_tasks,
    project_path,
    replace_metadata_value,
    split_names,
)


PARENT_CACHE: dict[str, str] = {}
SEQUENCE_ID_CACHE: dict[int, str] | None = None


def metadata_value(task: dict[str, Any], key: str) -> str:
    return str(task["metadata"].get(key.lower(), "")).strip()


def lookup_name(values: dict[str, Any], section: str, item_id: str) -> str:
    if not item_id:
        return ""
    for item in values.get(section, []):
        if isinstance(item, dict) and item.get("id") == item_id:
            return str(item.get("name") or item_id)
    return item_id


def infer_labels(task_name: str, explicit: str, values: dict[str, Any]) -> list[str]:
    if explicit:
        return [lookup_id(values, "labels", name) for name in split_names(explicit)]
    if "[FE TASK]" in task_name:
        return [lookup_id(values, "labels", "FE Task")]
    if "[BE TASK]" in task_name:
        return [lookup_id(values, "labels", "BE Task")]
    if "[BUG]" in task_name:
        return [lookup_id(values, "labels", "Bugs")]
    if "[UX/UI TASK]" in task_name:
        return [lookup_id(values, "labels", "UX/UI")]
    return []


def display_label_names(values: dict[str, Any], label_ids: list[str]) -> str:
    if not label_ids:
        return "(none)"
    return ",".join(lookup_name(values, "labels", label_id) for label_id in label_ids)


def find_work_item_id_by_sequence(config, sequence_id: int) -> str:
    global SEQUENCE_ID_CACHE
    if SEQUENCE_ID_CACHE is None:
        items = paginated_get(
            config,
            project_path(config, "/work-items/?fields=id,sequence_id&per_page=100"),
        )
        SEQUENCE_ID_CACHE = {
            int(item["sequence_id"]): item["id"]
            for item in items
            if isinstance(item.get("sequence_id"), int)
            and isinstance(item.get("id"), str)
        }
    if sequence_id in SEQUENCE_ID_CACHE:
        return SEQUENCE_ID_CACHE[sequence_id]
    raise SystemExit(f"ERROR: Could not resolve HAIRL-{sequence_id} in this project")


def resolve_parent(config, raw: str) -> tuple[str, str]:
    value = raw.strip()
    if not value:
        return "", ""
    cache_key = value.lower()
    if cache_key in PARENT_CACHE:
        return PARENT_CACHE[cache_key], value
    if UUID_RE.match(value):
        PARENT_CACHE[cache_key] = value
        return value, value
    if value.upper().startswith("HAIRL-"):
        try:
            resolved = find_work_item_id_by_sequence(config, int(value.split("-", 1)[1]))
            PARENT_CACHE[cache_key] = resolved
            return resolved, value.upper()
        except (IndexError, ValueError):
            raise SystemExit(f"ERROR: Invalid parent task key: {value!r}") from None
    path = f"/workspaces/{config.workspace_slug}/work-items/{value}/"
    body, status = api_request(config, "GET", path)
    if status == 200 and isinstance(body, dict) and isinstance(body.get("id"), str):
        PARENT_CACHE[cache_key] = body["id"]
        return body["id"], value
    raise SystemExit(
        f"ERROR: Could not resolve parent task {value!r}. "
        "Use the internal Plane UUID if the readable key is not accessible by API."
    )


def resolve_cycle(task: dict[str, Any], values: dict[str, Any]) -> str:
    raw = metadata_value(task, "cycle")
    if raw:
        return lookup_id(values, "cycles", raw)
    cycle = active_cycle(values)
    return str(cycle.get("id", "")) if cycle else ""


def build_plan(task: dict[str, Any], config, values: dict[str, Any]) -> dict[str, Any]:
    existing_id = metadata_value(task, "plane task id")
    existing_key = metadata_value(task, "plane task key")
    labels = infer_labels(task["name"], metadata_value(task, "labels"), values)
    module_id = lookup_id(values, "modules", metadata_value(task, "plane module"))
    priority = normalize_priority(metadata_value(task, "priority") or config.default_priority)
    parent_id, parent_display = resolve_parent(config, metadata_value(task, "parent task"))
    issue_type_id = lookup_id(
        values,
        "issue_types",
        metadata_value(task, "issue type") or config.issue_type_id,
    )

    payload: dict[str, Any] = {
        "name": task["name"],
        "description_html": task["description"],
        "project": config.project_id,
        "state": config.state_id,
        "priority": priority,
        "type": issue_type_id,
    }
    if config.assignee_id:
        payload["assignees"] = [config.assignee_id]
    if labels:
        payload["labels"] = labels
    if parent_id:
        payload["parent"] = parent_id
    cycle_id = resolve_cycle(task, values)
    return {
        "task": task,
        "payload": payload,
        "cycle_id": cycle_id,
        "cycle_name": lookup_name(values, "cycles", cycle_id),
        "module_id": module_id,
        "module_name": lookup_name(values, "modules", module_id),
        "parent_id": parent_id,
        "parent_display": parent_display,
        "label_names": display_label_names(values, labels),
        "existing_id": existing_id,
        "existing_key": existing_key,
    }


def add_to_cycle(config, work_item_id: str, cycle_id: str) -> None:
    if not cycle_id:
        return
    path = project_path(config, f"/cycles/{cycle_id}/cycle-issues/")
    body, status = api_request(config, "POST", path, {"issues": [work_item_id]})
    if status >= 400 or status == 0:
        raise SystemExit(f"ERROR: Cycle assignment failed HTTP {status}: {body}")


def add_to_module(config, work_item_id: str, module_id: str) -> None:
    if not module_id:
        return
    path = project_path(config, f"/modules/{module_id}/module-issues/")
    body, status = api_request(config, "POST", path, {"issues": [work_item_id]})
    if status >= 400 or status == 0:
        raise SystemExit(f"ERROR: Module assignment failed HTTP {status}: {body}")


def set_parent(config, work_item_id: str, parent_id: str) -> None:
    if not parent_id:
        return
    body, status = api_request(
        config,
        "PATCH",
        project_path(config, f"/work-items/{work_item_id}/"),
        {"parent": parent_id},
    )
    if status >= 400 or status == 0 or not isinstance(body, dict) or not body.get("id"):
        raise SystemExit(f"ERROR: Parent assignment failed HTTP {status}: {body}")


def create_issue(config, payload: dict[str, Any]) -> dict[str, Any]:
    body, status = api_request(config, "POST", project_path(config, "/work-items/"), payload)
    if status not in (200, 201) or not isinstance(body, dict) or not body.get("id"):
        raise SystemExit(f"ERROR: Create failed HTTP {status}: {body}")
    return body


def task_slice(tasks: list[dict[str, Any]], skip: int, limit: int | None) -> list[dict[str, Any]]:
    selected = tasks[skip:]
    if limit is not None:
        selected = selected[:limit]
    return selected


def clear_plane_ids(content: str, tasks: list[dict[str, Any]]) -> tuple[str, int]:
    updated = content
    cleared = 0
    for task in tasks:
        if metadata_value(task, "plane task id") or metadata_value(task, "plane task key"):
            updated = replace_metadata_value(updated, task["name"], "Plane Task ID", "")
            updated = replace_metadata_value(updated, task["name"], "Plane Task Key", "")
            cleared += 1
    return updated, cleared


def print_plan_row(index: int, plan: dict[str, Any], status: str) -> None:
    parent = plan["parent_display"] or "(none)"
    if plan["parent_display"] and plan["parent_id"] and plan["parent_display"] != plan["parent_id"]:
        parent = f"{plan['parent_display']}->{plan['parent_id']}"
    module = plan["module_name"] or "(none)"
    cycle = plan["cycle_name"] or "(none)"
    print(
        f"{index}. {status} {plan['task']['name']} | "
        f"priority={plan['payload']['priority']} labels={plan['label_names']} "
        f"module={module} cycle={cycle} parent={parent}"
    )


def print_summary(plans: list[dict[str, Any]]) -> None:
    created = [p for p in plans if p["existing_id"]]
    pending = [p for p in plans if not p["existing_id"]]
    parent_counts: dict[str, int] = {}
    module_counts: dict[str, int] = {}
    cycle_counts: dict[str, int] = {}
    for plan in plans:
        parent_counts[plan["parent_display"] or "(none)"] = parent_counts.get(plan["parent_display"] or "(none)", 0) + 1
        module_counts[plan["module_name"] or "(none)"] = module_counts.get(plan["module_name"] or "(none)", 0) + 1
        cycle_counts[plan["cycle_name"] or "(none)"] = cycle_counts.get(plan["cycle_name"] or "(none)", 0) + 1
    print(
        f"Summary: total={len(plans)} already_created={len(created)} "
        f"to_create={len(pending)}"
    )
    print(f"Parents: {parent_counts}")
    print(f"Modules: {module_counts}")
    print(f"Cycles: {cycle_counts}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create Plane work items from task markdown.")
    parser.add_argument("--file", required=True, help="Path to implementation task markdown")
    parser.add_argument("--env", default=".env", help="Path to .env")
    parser.add_argument("--values", default="plane-values.json", help="Path to fetched Plane values JSON")
    parser.add_argument("--skip", type=int, default=0, help="Skip first N tasks")
    parser.add_argument("--limit", type=int, default=None, help="Create at most N tasks")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print planned payload summary only")
    parser.add_argument("--resume", action="store_true", help="Skip tasks with existing Plane Task ID and create only blank-ID tasks")
    parser.add_argument("--reset-local-ids", action="store_true", help="Clear local Plane Task ID and Plane Task Key values from selected tasks")
    parser.add_argument("--confirm-reset-local-ids", action="store_true", help="Required to actually clear local Plane ID fields")
    args = parser.parse_args()

    config = load_config(Path(args.env))
    for key, value in {
        "ASSIGNEE_ID": config.assignee_id,
        "STAGE_ID/STATE_ID": config.state_id,
        "ISSUE_TYPE_ID": config.issue_type_id,
    }.items():
        if not value:
            raise SystemExit(f"ERROR: Missing required config value {key}")

    values = load_values(Path(args.values))
    task_path = Path(args.file)
    if not task_path.exists():
        raise SystemExit(f"ERROR: File not found: {task_path}")
    content = task_path.read_text(encoding="utf-8")
    tasks = task_slice(parse_tasks(content), args.skip, args.limit)
    if not tasks:
        raise SystemExit("ERROR: No task blocks found for creation")

    if args.reset_local_ids:
        existing = [
            task for task in tasks
            if metadata_value(task, "plane task id") or metadata_value(task, "plane task key")
        ]
        print(f"Reset-local-ids selected tasks={len(tasks)} fields_to_clear={len(existing)}")
        for index, task in enumerate(existing, 1):
            print(
                f"{index}. clear {task['name']} | "
                f"id={metadata_value(task, 'plane task id') or '(blank)'} "
                f"key={metadata_value(task, 'plane task key') or '(blank)'}"
            )
        if args.dry_run:
            return
        if not args.confirm_reset_local_ids:
            raise SystemExit(
                "ERROR: --reset-local-ids requires --confirm-reset-local-ids. "
                "This only clears local IDs and does not delete Plane issues."
            )
        updated_content, cleared = clear_plane_ids(content, tasks)
        task_path.write_text(updated_content, encoding="utf-8")
        print(f"Cleared Plane ID fields from {cleared} task(s).")
        return

    project_identifier = str(values.get("project", {}).get("identifier") or "HAIRL")
    updated_content = content
    plans = [build_plan(task, config, values) for task in tasks]
    print(f"Found {len(plans)} task(s) to process")
    print_summary(plans)
    existing = [plan for plan in plans if plan["existing_id"]]
    if existing and not args.resume:
        for index, plan in enumerate(plans, 1):
            status = "already_created" if plan["existing_id"] else "to_create"
            print_plan_row(index, plan, status)
        raise SystemExit(
            "ERROR: selected tasks include existing Plane Task ID values. "
            "Use --resume to skip them, --skip/--limit to select a fresh range, "
            "or --reset-local-ids --dry-run to inspect a local reset."
        )
    for index, plan in enumerate(plans, 1):
        if plan["existing_id"]:
            print_plan_row(index, plan, "skip_existing")
            continue
        print_plan_row(index, plan, "to_create")
        if args.dry_run:
            continue
        response = create_issue(config, plan["payload"])
        work_item_id = str(response["id"])
        key = issue_key(project_identifier, response.get("sequence_id"))
        updated_content = replace_metadata_value(
            updated_content, plan["task"]["name"], "Plane Task ID", work_item_id
        )
        if key:
            updated_content = replace_metadata_value(
                updated_content, plan["task"]["name"], "Plane Task Key", key
            )
        task_path.write_text(updated_content, encoding="utf-8")
        print(f"   created id={work_item_id} key={key or '(none)'}")
        add_to_module(config, work_item_id, plan["module_id"])
        set_parent(config, work_item_id, plan["parent_id"])
        add_to_cycle(config, work_item_id, plan["cycle_id"])

    if not args.dry_run:
        task_path.write_text(updated_content, encoding="utf-8")
        print(f"Updated task file with Plane Task ID values: {task_path}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Interrupted")
