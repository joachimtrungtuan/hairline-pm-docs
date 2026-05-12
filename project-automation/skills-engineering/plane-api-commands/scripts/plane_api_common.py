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
DEFAULT_WORKSPACE_SLUG = "samasu-digital"
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
        if str(item.get("name", "")).strip().lower() == raw.lower():
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
