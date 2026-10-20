#!/usr/bin/env python3
"""Fetch Plane project metadata into a reusable local values cache."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from plane_api_common import (
    PRIORITIES,
    active_cycle,
    api_request,
    find_active_cycle,
    iso_now,
    load_config,
    paginated_get,
    parse_date,
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


def split_spec(raw: str) -> tuple[str, str]:
    name, _, extra = raw.partition("=")
    if not name.strip():
        raise SystemExit(f"ERROR: Empty name in {raw!r}")
    return name.strip(), extra.strip()


def ensure_labels(config, specs: list[str], dry_run: bool) -> None:
    """Create each missing label (`NAME` or `NAME=#hex`); existing labels are left untouched."""
    existing = {str(x.get("name", "")).lower() for x in paginated_get(config, project_path(config, "/labels/"))}
    for spec in specs:
        name, color = split_spec(spec)
        if name.lower() in existing:
            print(f"Label exists: {name}")
            continue
        print(f"Label {'would be created' if dry_run else 'created'}: {name}")
        if dry_run:
            continue
        payload = {"name": name, **({"color": color} if color else {})}
        body, status = api_request(config, "POST", project_path(config, "/labels/"), payload)
        if status not in (200, 201):
            raise SystemExit(f"ERROR: Label create failed HTTP {status}: {body}")


def ensure_milestones(config, specs: list[str], dry_run: bool) -> None:
    """Create each missing milestone (`TITLE` or `TITLE=YYYY-MM-DD`); align target date when given."""
    existing = {
        str(x.get("title", "")).lower(): x
        for x in paginated_get(config, project_path(config, "/milestones/"))
    }
    for spec in specs:
        title, raw_date = split_spec(spec)
        target = parse_date(raw_date, "Milestone target date") if raw_date else None
        current = existing.get(title.lower())
        if current and (not target or current.get("target_date") == target):
            print(f"Milestone exists: {title}")
            continue
        verb = "updated" if current else "created"
        print(f"Milestone {'would be ' + verb if dry_run else verb}: {title} target={target or '(none)'}")
        if dry_run:
            continue
        if current:
            body, status = api_request(
                config, "PATCH", project_path(config, f"/milestones/{current['id']}/"), {"target_date": target}
            )
        else:
            payload = {"title": title, **({"target_date": target} if target else {})}
            body, status = api_request(config, "POST", project_path(config, "/milestones/"), payload)
        if status not in (200, 201):
            raise SystemExit(f"ERROR: Milestone {verb[:-1]} failed HTTP {status}: {body}")


def fetch_members(config) -> list[dict[str, Any]]:
    """Project members as id + names only (no emails) for Assignees name lookup."""
    rows = []
    for item in paginated_get(config, project_path(config, "/members/")):
        member = item.get("member") if isinstance(item.get("member"), dict) else item
        rows.append({
            "id": member.get("id") or item.get("member_id"),
            "display_name": member.get("display_name"),
            "first_name": member.get("first_name"),
            "last_name": member.get("last_name"),
        })
    return [row for row in rows if row["id"]]


def diff_by_id(old: list[dict[str, Any]], new: list[dict[str, Any]]) -> dict[str, list[str]]:
    old_by_id = {str(x.get("id")): x for x in old if x.get("id")}
    new_by_id = {str(x.get("id")): x for x in new if x.get("id")}
    added = [str(new_by_id[k].get("name") or new_by_id[k].get("title") or new_by_id[k].get("display_name") or k) for k in sorted(new_by_id.keys() - old_by_id.keys())]
    removed = [str(old_by_id[k].get("name") or old_by_id[k].get("title") or old_by_id[k].get("display_name") or k) for k in sorted(old_by_id.keys() - new_by_id.keys())]
    changed: list[str] = []
    for key in sorted(old_by_id.keys() & new_by_id.keys()):
        if old_by_id[key] != new_by_id[key]:
            changed.append(str(new_by_id[key].get("name") or key))
    return {"added": added, "removed": removed, "changed": changed}


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch Plane labels/modules/cycles/milestones/members/states into a cache file.")
    parser.add_argument("--env", default=".env", help="Path to .env")
    parser.add_argument(
        "--output",
        default="plane-values.json",
        help="Cache path to write (default: plane-values.json in cwd)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print fetched data and do not write")
    parser.add_argument(
        "--ensure-label", action="append", default=[], metavar="NAME[=#hex]",
        help="Create the label if missing (repeatable)",
    )
    parser.add_argument(
        "--ensure-milestone", action="append", default=[], metavar="TITLE[=YYYY-MM-DD]",
        help="Create the milestone if missing, or align its target date (repeatable)",
    )
    args = parser.parse_args()

    config = load_config(Path(args.env))
    ensure_labels(config, args.ensure_label, args.dry_run)
    ensure_milestones(config, args.ensure_milestone, args.dry_run)
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
    milestones = compact(
        paginated_get(config, project_path(config, "/milestones/")),
        "id",
        "title",
        "target_date",
    )
    members = fetch_members(config)
    issue_types = compact(
        paginated_get(config, project_path(config, "/issue-types/")),
        "id",
        "name",
        "is_default",
        "is_epic",
    )

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
        "active_cycle": find_active_cycle(cycles),
        "milestones": milestones,
        "members": members,
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
        "milestones": diff_by_id(old_values.get("milestones", []), milestones),
        "members": diff_by_id(old_values.get("members", []), members),
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
