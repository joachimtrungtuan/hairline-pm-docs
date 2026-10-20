#!/usr/bin/env python3
"""Create Plane work items from implementation task markdown files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from plane_api_common import (
    add_to_cycle,
    add_to_milestone,
    add_to_module,
    api_request,
    issue_key,
    load_config,
    load_values,
    lookup_name,
    member_name,
    metadata_value,
    project_path,
    parse_tasks,
    replace_metadata_value,
    resolve_work_item_fields,
    set_parent,
    verify_work_item,
)


def display_label_names(values: dict[str, Any], label_ids: list[str]) -> str:
    if not label_ids:
        return "(none)"
    return ",".join(lookup_name(values, "labels", label_id) for label_id in label_ids)


def build_plan(task: dict[str, Any], config, values: dict[str, Any]) -> dict[str, Any]:
    resolved = resolve_work_item_fields(task, config, values)
    payload = resolved["payload"]
    return {
        "task": task,
        "resolved": resolved,
        "payload": {**payload, "project": config.project_id},
        "cycle_name": lookup_name(values, "cycles", resolved["cycle_id"]),
        "module_name": lookup_name(values, "modules", resolved["module_id"]),
        "milestone_name": lookup_name(values, "milestones", resolved["milestone_id"]),
        "state_name": lookup_name(values, "states", payload["state"]),
        "assignee_names": ",".join(member_name(values, m) for m in payload["assignees"]) or "(none)",
        "parent_id": resolved["parent_id"],
        "parent_display": resolved["parent_display"],
        "label_names": display_label_names(values, payload["labels"]),
        "existing_id": metadata_value(task, "plane task id"),
        "existing_key": metadata_value(task, "plane task key"),
    }


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
    milestone = plan["milestone_name"] or "(none)"
    payload = plan["payload"]
    dates = f"{payload['start_date'] or '-'}..{payload['target_date'] or '-'}"
    print(
        f"{index}. {status} {plan['task']['name']} | "
        f"state={plan['state_name']} priority={payload['priority']} labels={plan['label_names']} "
        f"assignees={plan['assignee_names']} dates={dates} "
        f"module={module} cycle={cycle} milestone={milestone} parent={parent}"
    )


def print_summary(plans: list[dict[str, Any]]) -> None:
    created = [p for p in plans if p["existing_id"]]
    pending = [p for p in plans if not p["existing_id"]]
    parent_counts: dict[str, int] = {}
    module_counts: dict[str, int] = {}
    cycle_counts: dict[str, int] = {}
    milestone_counts: dict[str, int] = {}
    for plan in plans:
        milestone_counts[plan["milestone_name"] or "(none)"] = milestone_counts.get(plan["milestone_name"] or "(none)", 0) + 1
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
    print(f"Milestones: {milestone_counts}")


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
        resolved = plan["resolved"]
        add_to_module(config, work_item_id, resolved["module_id"])
        set_parent(config, work_item_id, resolved["parent_id"])
        add_to_cycle(config, work_item_id, resolved["cycle_id"])
        add_to_milestone(config, work_item_id, resolved["milestone_id"])
        problems = verify_work_item(config, work_item_id, resolved)
        if problems:
            raise SystemExit(
                f"ERROR: {key or work_item_id} created but fields did not persist: " + "; ".join(problems)
            )
        print("   verified all fields persisted")

    if not args.dry_run:
        task_path.write_text(updated_content, encoding="utf-8")
        print(f"Updated task file with Plane Task ID values: {task_path}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Interrupted")
