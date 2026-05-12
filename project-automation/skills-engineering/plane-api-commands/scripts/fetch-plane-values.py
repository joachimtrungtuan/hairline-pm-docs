#!/usr/bin/env python3
"""Fetch Plane project metadata into a reusable local values cache."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from plane_api_common import (
    PRIORITIES,
    active_cycle,
    api_request,
    iso_now,
    load_config,
    paginated_get,
    print_json,
    project_path,
)


def compact(items: list[dict[str, Any]], *fields: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for item in items:
        row: dict[str, Any] = {}
        for field in fields:
            if field in item:
                row[field] = item.get(field)
        out.append(row)
    return out


def parse_dt(raw: str | None) -> datetime | None:
    if not raw:
        return None
    return datetime.fromisoformat(raw.replace("Z", "+00:00"))


def find_active_cycle(cycles: list[dict[str, Any]], now: datetime) -> dict[str, Any] | None:
    for cycle in cycles:
        start = parse_dt(cycle.get("start_date"))
        end = parse_dt(cycle.get("end_date"))
        if start and end and start <= now <= end:
            return cycle
    return None


def diff_by_id(old: list[dict[str, Any]], new: list[dict[str, Any]]) -> dict[str, list[str]]:
    old_by_id = {str(x.get("id")): x for x in old if x.get("id")}
    new_by_id = {str(x.get("id")): x for x in new if x.get("id")}
    added = [str(new_by_id[k].get("name") or k) for k in sorted(new_by_id.keys() - old_by_id.keys())]
    removed = [str(old_by_id[k].get("name") or k) for k in sorted(old_by_id.keys() - new_by_id.keys())]
    changed: list[str] = []
    for key in sorted(old_by_id.keys() & new_by_id.keys()):
        if old_by_id[key] != new_by_id[key]:
            changed.append(str(new_by_id[key].get("name") or key))
    return {"added": added, "removed": removed, "changed": changed}


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch Plane labels/modules/cycles/states into a cache file.")
    parser.add_argument("--env", default=".env", help="Path to .env")
    parser.add_argument(
        "--output",
        default="plane-values.json",
        help="Cache path to write (default: plane-values.json in cwd)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print fetched data and do not write")
    args = parser.parse_args()

    config = load_config(Path(args.env))
    project_body, project_status = api_request(
        config,
        "GET",
        project_path(config, "/"),
    )
    if project_status >= 400 or not isinstance(project_body, dict):
        raise SystemExit(f"ERROR: Project fetch failed HTTP {project_status}: {project_body}")

    labels = compact(
        paginated_get(config, project_path(config, "/labels/")),
        "id",
        "name",
        "color",
        "description",
    )
    modules = compact(
        paginated_get(config, project_path(config, "/modules/")),
        "id",
        "name",
        "status",
        "start_date",
        "end_date",
    )
    cycles = compact(
        paginated_get(config, project_path(config, "/cycles/")),
        "id",
        "name",
        "start_date",
        "end_date",
        "status",
    )
    states = compact(
        paginated_get(config, project_path(config, "/states/")),
        "id",
        "name",
        "group",
        "color",
    )
    issue_types = compact(
        paginated_get(config, project_path(config, "/issue-types/")),
        "id",
        "name",
        "is_default",
        "is_epic",
    )

    now = datetime.now().astimezone()
    values = {
        "fetched_at": iso_now(),
        "workspace_slug": config.workspace_slug,
        "project": {
            "id": config.project_id,
            "identifier": project_body.get("identifier", "HAIRL"),
            "name": project_body.get("name", "Hairline"),
        },
        "priorities": sorted(PRIORITIES),
        "labels": labels,
        "modules": modules,
        "cycles": cycles,
        "active_cycle": find_active_cycle(cycles, now),
        "states": states,
        "issue_types": issue_types,
    }

    output = Path(args.output)
    old_values: dict[str, Any] = {}
    if output.exists():
        old_values = json.loads(output.read_text(encoding="utf-8"))

    diffs = {
        "labels": diff_by_id(old_values.get("labels", []), labels),
        "modules": diff_by_id(old_values.get("modules", []), modules),
        "cycles": diff_by_id(old_values.get("cycles", []), cycles),
        "states": diff_by_id(old_values.get("states", []), states),
        "issue_types": diff_by_id(old_values.get("issue_types", []), issue_types),
        "active_cycle": {
            "old": (active_cycle(old_values) or {}).get("name"),
            "new": (values["active_cycle"] or {}).get("name"),
        },
    }

    print("Plane values fetched.")
    print_json({"diffs": diffs, "active_cycle": values["active_cycle"]})
    if args.dry_run:
        return
    output.write_text(json.dumps(values, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
