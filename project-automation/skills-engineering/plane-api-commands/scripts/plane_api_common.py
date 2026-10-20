#!/usr/bin/env python3
"""Shared Plane API helpers for Hairline task automation."""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_BASE_URL = "https://api.plane.so/api/v1"
DEFAULT_WORKSPACE_SLUG = "samasu-group"
PRIORITIES = {"none", "low", "medium", "high", "urgent"}
UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


@dataclass
class PlaneConfig:
    api_key: str
    workspace_slug: str
    project_id: str
    base_url: str
    assignee_id: str = ""
    state_id: str = ""
    issue_type_id: str = ""
    default_priority: str = "medium"


def load_env(env_path: Path) -> dict[str, str]:
    env_vars: dict[str, str] = {}
    if not env_path.exists():
        raise SystemExit(f"ERROR: .env file not found at {env_path}")
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                env_vars[key.strip()] = value.strip().strip('"').strip("'")
    return env_vars


def load_config(env_path: Path) -> PlaneConfig:
    env = load_env(env_path)
    api_key = env.get("PLANE_API_KEY", "")
    if not api_key:
        raise SystemExit("ERROR: PLANE_API_KEY missing in .env")
    project_id = env.get("PROJECT_ID", "")
    if not project_id:
        raise SystemExit("ERROR: PROJECT_ID missing in .env")
    return PlaneConfig(
        api_key=api_key,
        workspace_slug=env.get("WORKSPACE_SLUG", DEFAULT_WORKSPACE_SLUG),
        project_id=project_id,
        base_url=env.get("BASE_URL", DEFAULT_BASE_URL).rstrip("/"),
        assignee_id=env.get("ASSIGNEE_ID", ""),
        state_id=env.get("STATE_ID") or env.get("STAGE_ID", ""),
        issue_type_id=env.get("ISSUE_TYPE_ID", ""),
        default_priority=normalize_priority(env.get("PRIORITY", "medium")),
    )


def normalize_priority(raw: str | None) -> str:
    value = (raw or "medium").strip().lower()
    if value == "":
        return "medium"
    if value not in PRIORITIES:
        raise SystemExit(
            f"ERROR: Invalid priority {raw!r}; expected one of {sorted(PRIORITIES)}"
        )
    return value


def api_request(
    config: PlaneConfig,
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
    *,
    retry_429: bool = True,
) -> tuple[Any, int]:
    url = f"{config.base_url}{path}"
    data = None
    headers = {
        "X-API-Key": config.api_key,
        "Content-Type": "application/json",
        "User-Agent": "HairlinePlaneAutomation/1.0",
    }
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    delay = 2.0
    for attempt in range(6):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                raw = response.read().decode("utf-8")
                parsed = json.loads(raw) if raw else {}
                return parsed, response.status
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            try:
                parsed = json.loads(raw) if raw else {"detail": exc.reason}
            except json.JSONDecodeError:
                parsed = {"detail": raw[:1000] or exc.reason}
            if exc.code == 429 and retry_429 and attempt < 5:
                time.sleep(delay)
                delay = min(delay * 1.6, 30.0)
                continue
            return parsed, exc.code
        except urllib.error.URLError as exc:
            return {"detail": str(exc.reason)}, 0
    return {"detail": "retry guard exhausted"}, 0


def project_path(config: PlaneConfig, suffix: str) -> str:
    return (
        f"/workspaces/{config.workspace_slug}/projects/{config.project_id}"
        f"{suffix}"
    )


def paginated_get(config: PlaneConfig, path: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    cursor: str | None = None
    seen_cursors: set[str] = set()
    for _ in range(500):
        current_path = path
        if cursor:
            sep = "&" if "?" in current_path else "?"
            current_path = f"{current_path}{sep}cursor={urllib.parse.quote(cursor)}"
        body, status = api_request(config, "GET", current_path)
        if status >= 400 or status == 0:
            raise SystemExit(f"ERROR: GET {path} failed HTTP {status}: {body}")
        if isinstance(body, list):
            batch = body
            next_cursor = None
        elif isinstance(body, dict):
            batch = body.get("results") or body.get("data") or []
            next_cursor = (
                body.get("next_cursor")
                or body.get("next_page_results")
                or body.get("cursor")
            )
        else:
            batch = []
            next_cursor = None
        items.extend([x for x in batch if isinstance(x, dict)])
        if not next_cursor or not batch:
            break
        if str(next_cursor) in seen_cursors:
            break
        seen_cursors.add(str(next_cursor))
        cursor = str(next_cursor)
    return items


def clean_html(html: str) -> str:
    html = re.sub(r">\s+<", "><", html)
    html = re.sub(r"  +", " ", html)
    lines = [line.strip() for line in html.split("\n") if line.strip()]
    return "".join(lines)


def parse_metadata(block: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in block.splitlines():
        match = re.match(r"^\*\*(?P<key>[^*]+)\*\*:\s*(?P<value>.*)$", line.strip())
        if match:
            key = re.sub(r"\s+", " ", match.group("key").strip()).lower()
            metadata[key] = match.group("value").strip()
    return metadata


def parse_tasks(content: str) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    pattern = re.compile(
        r"## TASK_NAME_START\s*\n(?P<name>.*?)\n## TASK_NAME_END"
        r"(?P<meta>[\s\S]*?)"
        r"## TASK_DESCRIPTION_START\s*\n(?P<description>[\s\S]*?)\n## TASK_DESCRIPTION_END",
        re.MULTILINE,
    )
    for match in pattern.finditer(content):
        metadata = parse_metadata(match.group("meta"))
        tasks.append(
            {
                "name": match.group("name").strip(),
                "description": clean_html(match.group("description").strip()),
                "metadata": metadata,
                "start": match.start(),
                "end": match.end(),
            }
        )
    return tasks


def load_values(values_path: Path) -> dict[str, Any]:
    if not values_path.exists():
        raise SystemExit(
            f"ERROR: Plane values cache not found at {values_path}. "
            "Run fetch-plane-values.py first."
        )
    with open(values_path, encoding="utf-8") as f:
        return json.load(f)


def lookup_id(values: dict[str, Any], section: str, name_or_id: str) -> str:
    raw = name_or_id.strip()
    if not raw:
        return ""
    if UUID_RE.match(raw):
        return raw
    for item in values.get(section, []):
        if not isinstance(item, dict):
            continue
        item_name = item.get("name") or item.get("title") or ""
        if str(item_name).strip().lower() == raw.lower():
            item_id = item.get("id")
            if isinstance(item_id, str):
                return item_id
    raise SystemExit(f"ERROR: Unknown {section} value: {raw!r}")


def split_names(raw: str) -> list[str]:
    return [part.strip() for part in raw.split(",") if part.strip()]


def issue_key(project_identifier: str, sequence_id: Any) -> str:
    if sequence_id is None:
        return ""
    return f"{project_identifier}-{sequence_id}"


def active_cycle(values: dict[str, Any]) -> dict[str, Any] | None:
    active = values.get("active_cycle")
    return active if isinstance(active, dict) else None


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_dt(raw: str | None) -> datetime | None:
    if not raw:
        return None
    return datetime.fromisoformat(raw.replace("Z", "+00:00"))


def find_active_cycle(cycles: list[dict[str, Any]], now: datetime | None = None) -> dict[str, Any] | None:
    now = now or datetime.now().astimezone()
    for cycle in cycles:
        start = parse_dt(cycle.get("start_date"))
        end = parse_dt(cycle.get("end_date"))
        if start and end and start <= now <= end:
            return cycle
    return None


def v2_config(config: PlaneConfig) -> PlaneConfig:
    """Same credentials against the v2 API (milestone work-item membership lives there)."""
    return PlaneConfig(**{**config.__dict__, "base_url": re.sub(r"/api/v1$", "/api/v2", config.base_url)})


def is_none_value(raw: str) -> bool:
    return raw.strip().lower() in {"none", "(none)", "-"}


def parse_date(raw: str, field: str) -> str:
    value = raw.strip()
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise SystemExit(f"ERROR: {field} must be YYYY-MM-DD, got {raw!r}") from None
    return value


def ids_of(items: Any) -> list[str]:
    """Normalize Plane list fields that may come back as UUIDs or expanded objects."""
    out: list[str] = []
    for item in items or []:
        if isinstance(item, dict) and item.get("id"):
            out.append(str(item["id"]))
        elif isinstance(item, str):
            out.append(item)
    return sorted(out)


def lookup_member_id(values: dict[str, Any], name_or_id: str) -> str:
    raw = name_or_id.strip()
    if UUID_RE.match(raw):
        return raw
    wanted = raw.lower()
    for member in values.get("members", []):
        full_name = f"{member.get('first_name') or ''} {member.get('last_name') or ''}".strip()
        names = {str(member.get("display_name") or "").lower(), full_name.lower()}
        if wanted in names and isinstance(member.get("id"), str):
            return member["id"]
    raise SystemExit(
        f"ERROR: Unknown member value: {raw!r}. Refresh plane-values.json or use the member UUID."
    )


def member_name(values: dict[str, Any], member_id: str) -> str:
    for member in values.get("members", []):
        if member.get("id") == member_id:
            full_name = f"{member.get('first_name') or ''} {member.get('last_name') or ''}".strip()
            return full_name or str(member.get("display_name") or member_id)
    return member_id


def replace_metadata_value(content: str, task_name: str, key: str, value: str) -> str:
    escaped_name = re.escape(task_name)
    block_pattern = re.compile(
        r"(## TASK_NAME_START\s*\n"
        + escaped_name
        + r"\n## TASK_NAME_END(?P<meta>[\s\S]*?)"
        r"## TASK_DESCRIPTION_START)",
        re.MULTILINE,
    )
    match = block_pattern.search(content)
    if not match:
        raise SystemExit(f"ERROR: Could not locate task block for {task_name!r}")
    block = match.group(0)
    line_pattern = re.compile(rf"^\*\*{re.escape(key)}\*\*:\s*.*$", re.MULTILINE)
    replacement_line = f"**{key}**: {value}"
    if line_pattern.search(block):
        new_block = line_pattern.sub(replacement_line, block, count=1)
    else:
        insert_after = re.search(r"^\*\*Status\*\*:\s*.*$", block, re.MULTILINE)
        if not insert_after:
            raise SystemExit(f"ERROR: Task {task_name!r} has no Status metadata")
        pos = insert_after.end()
        new_block = block[:pos] + "\n" + replacement_line + block[pos:]
    return content[: match.start()] + new_block + content[match.end() :]


def print_json(data: Any) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


# --- Work-item field resolution, relations, and persistence checks ---------

_SEQUENCE_ID_CACHE: dict[int, str] | None = None
_PARENT_CACHE: dict[str, str] = {}


def metadata_value(task: dict[str, Any], key: str) -> str:
    return str(task["metadata"].get(key.lower(), "")).strip()


def lookup_name(values: dict[str, Any], section: str, item_id: str) -> str:
    if not item_id:
        return ""
    for item in values.get(section, []):
        if isinstance(item, dict) and item.get("id") == item_id:
            return str(item.get("name") or item.get("title") or item_id)
    return item_id


def find_work_item_id_by_sequence(config: PlaneConfig, sequence_id: int) -> str:
    global _SEQUENCE_ID_CACHE
    if _SEQUENCE_ID_CACHE is None:
        items = paginated_get(
            config,
            project_path(config, "/work-items/?fields=id,sequence_id&per_page=100"),
        )
        _SEQUENCE_ID_CACHE = {
            int(item["sequence_id"]): item["id"]
            for item in items
            if isinstance(item.get("sequence_id"), int) and isinstance(item.get("id"), str)
        }
    if sequence_id in _SEQUENCE_ID_CACHE:
        return _SEQUENCE_ID_CACHE[sequence_id]
    raise SystemExit(f"ERROR: Could not resolve HAIRL-{sequence_id} in this project")


def resolve_parent(config: PlaneConfig, raw: str) -> tuple[str, str]:
    value = raw.strip()
    if not value or is_none_value(value):
        return "", ""
    cache_key = value.lower()
    if cache_key in _PARENT_CACHE:
        return _PARENT_CACHE[cache_key], value
    if UUID_RE.match(value):
        _PARENT_CACHE[cache_key] = value
        return value, value
    if value.upper().startswith("HAIRL-"):
        try:
            resolved = find_work_item_id_by_sequence(config, int(value.split("-", 1)[1]))
        except (IndexError, ValueError):
            raise SystemExit(f"ERROR: Invalid parent task key: {value!r}") from None
        _PARENT_CACHE[cache_key] = resolved
        return resolved, value.upper()
    raise SystemExit(f"ERROR: Could not resolve parent task {value!r}; use HAIRL-N or the UUID.")


def infer_labels(task_name: str, explicit: str, values: dict[str, Any]) -> list[str]:
    if explicit:
        if is_none_value(explicit):
            return []
        return [lookup_id(values, "labels", name) for name in split_names(explicit)]
    for prefix, label in (
        ("[FE TASK]", "FE Task"),
        ("[BE TASK]", "BE Task"),
        ("[BUG]", "Bugs"),
        ("[UX/UI TASK]", "UX/UI"),
        ("[QA TASK]", "QA"),
    ):
        if prefix in task_name:
            return [lookup_id(values, "labels", label)]
    return []


def resolve_assignees(task: dict[str, Any], config: PlaneConfig, values: dict[str, Any]) -> list[str]:
    """Explicit `Assignees` wins; `none` clears; blank falls back to ASSIGNEE_ID from .env."""
    raw = metadata_value(task, "assignees")
    if not raw:
        return [config.assignee_id] if config.assignee_id else []
    if is_none_value(raw):
        return []
    return [lookup_member_id(values, name) for name in split_names(raw)]


def resolve_cycle(task: dict[str, Any], values: dict[str, Any]) -> str:
    """Explicit `Cycle` wins; `none` skips; blank uses the cycle active today (not the cached one)."""
    raw = metadata_value(task, "cycle")
    if raw:
        return "" if is_none_value(raw) else lookup_id(values, "cycles", raw)
    cycle = find_active_cycle(values.get("cycles", []))
    if not cycle:
        raise SystemExit(
            "ERROR: No Plane cycle is active today. Refresh plane-values.json, "
            "or set `Cycle` to a cycle name or `none`."
        )
    return str(cycle.get("id", ""))


def resolve_work_item_fields(task: dict[str, Any], config: PlaneConfig, values: dict[str, Any]) -> dict[str, Any]:
    """Resolve every supported metadata field into payload values and relation targets."""
    state_raw = metadata_value(task, "state")
    start_raw = metadata_value(task, "start date")
    due_raw = metadata_value(task, "due date")
    milestone_raw = metadata_value(task, "milestone")
    module_raw = metadata_value(task, "plane module")
    parent_id, parent_display = resolve_parent(config, metadata_value(task, "parent task"))
    payload: dict[str, Any] = {
        "name": task["name"],
        "description_html": task["description"],
        "state": lookup_id(values, "states", state_raw) if state_raw else config.state_id,
        "priority": normalize_priority(metadata_value(task, "priority") or config.default_priority),
        "type": lookup_id(values, "issue_types", metadata_value(task, "issue type") or config.issue_type_id),
        "assignees": resolve_assignees(task, config, values),
        "labels": infer_labels(task["name"], metadata_value(task, "labels"), values),
        "start_date": parse_date(start_raw, "Start Date") if start_raw and not is_none_value(start_raw) else None,
        "target_date": parse_date(due_raw, "Due Date") if due_raw and not is_none_value(due_raw) else None,
    }
    if payload["start_date"] and payload["target_date"] and payload["start_date"] > payload["target_date"]:
        raise SystemExit(f"ERROR: Start Date is after Due Date for {task['name']!r}")
    return {
        "payload": payload,
        "parent_id": parent_id,
        "parent_display": parent_display,
        "cycle_id": resolve_cycle(task, values),
        "module_id": "" if is_none_value(module_raw) else lookup_id(values, "modules", module_raw),
        "milestone_id": "" if is_none_value(milestone_raw) else lookup_id(values, "milestones", milestone_raw),
    }


def _require_ok(status: int, body: Any, action: str) -> None:
    if status >= 400 or status == 0:
        raise SystemExit(f"ERROR: {action} failed HTTP {status}: {body}")


def set_parent(config: PlaneConfig, work_item_id: str, parent_id: str) -> None:
    if not parent_id:
        return
    body, status = api_request(
        config, "PATCH", project_path(config, f"/work-items/{work_item_id}/"), {"parent": parent_id}
    )
    if status >= 400 or status == 0 or not isinstance(body, dict) or not body.get("id"):
        raise SystemExit(f"ERROR: Parent assignment failed HTTP {status}: {body}")


def add_to_cycle(config: PlaneConfig, work_item_id: str, cycle_id: str) -> None:
    if not cycle_id:
        return
    body, status = api_request(
        config, "POST", project_path(config, f"/cycles/{cycle_id}/cycle-issues/"), {"issues": [work_item_id]}
    )
    _require_ok(status, body, "Cycle assignment")


def add_to_module(config: PlaneConfig, work_item_id: str, module_id: str) -> None:
    if not module_id:
        return
    body, status = api_request(
        config, "POST", project_path(config, f"/modules/{module_id}/module-issues/"), {"issues": [work_item_id]}
    )
    _require_ok(status, body, "Module assignment")


def add_to_milestone(config: PlaneConfig, work_item_id: str, milestone_id: str) -> None:
    if not milestone_id:
        return
    body, status = api_request(
        v2_config(config),
        "POST",
        project_path(config, f"/milestones/{milestone_id}/work-items/"),
        {"add": [work_item_id]},
    )
    _require_ok(status, body, "Milestone assignment")


def _membership_ids(config: PlaneConfig, path: str) -> set[str]:
    ids: set[str] = set()
    for item in paginated_get(config, path):
        for key in ("issue", "work_item", "issue_id", "work_item_id", "id"):
            value = item.get(key)
            if isinstance(value, dict):
                value = value.get("id")
            if isinstance(value, str):
                ids.add(value)
                break
    return ids


def verify_work_item(config: PlaneConfig, work_item_id: str, resolved: dict[str, Any], fields: set[str] | None = None) -> list[str]:
    """Read the work item back and list every requested field that did not persist."""
    body, status = api_request(config, "GET", project_path(config, f"/work-items/{work_item_id}/"))
    if status != 200 or not isinstance(body, dict):
        return [f"read-back failed HTTP {status}"]
    payload = resolved["payload"]
    checks: dict[str, tuple[Any, Any]] = {
        "name": (body.get("name"), payload["name"]),
        "state": (body.get("state"), payload["state"]),
        "priority": (body.get("priority"), payload["priority"]),
        "type": (body.get("type_id") or body.get("type"), payload["type"]),
        "assignees": (ids_of(body.get("assignees")), sorted(payload["assignees"])),
        "labels": (ids_of(body.get("labels")), sorted(payload["labels"])),
        "start_date": (body.get("start_date"), payload["start_date"]),
        "target_date": (body.get("target_date"), payload["target_date"]),
    }
    if resolved["parent_id"]:
        checks["parent"] = (body.get("parent"), resolved["parent_id"])
    if resolved["cycle_id"]:
        checks["cycle"] = (body.get("cycle_id"), resolved["cycle_id"])
    problems = [
        f"{field}: expected {expected!r}, got {actual!r}"
        for field, (actual, expected) in checks.items()
        if (fields is None or field in fields) and actual != expected
    ]
    if resolved["module_id"] and (fields is None or "module" in fields):
        members = _membership_ids(config, project_path(config, f"/modules/{resolved['module_id']}/module-issues/?per_page=100"))
        if work_item_id not in members:
            problems.append("module: work item is not listed in the module")
    if resolved["milestone_id"] and (fields is None or "milestone" in fields):
        members = _membership_ids(config, project_path(config, f"/milestones/{resolved['milestone_id']}/work-items/?per_page=100"))
        if work_item_id not in members:
            problems.append("milestone: work item is not listed in the milestone")
    return problems
