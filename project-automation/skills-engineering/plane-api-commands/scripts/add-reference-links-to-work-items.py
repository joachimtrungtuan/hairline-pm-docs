#!/usr/bin/env python3
"""Add reusable reference links to existing Plane work item descriptions."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from plane_api_common import api_request, load_config, paginated_get, project_path


def parse_sequences(raw: str) -> set[int]:
    out: set[int] = set()
    for part in raw.split(","):
        token = part.strip()
        if not token:
            continue
        if "-" in token:
            start_s, end_s = token.split("-", 1)
            start, end = int(start_s), int(end_s)
            if end < start:
                start, end = end, start
            out.update(range(start, end + 1))
        else:
            out.add(int(token))
    return out


def load_links(args) -> list[tuple[str, str]]:
    links: list[tuple[str, str]] = []
    if args.links_json:
        data = json.loads(Path(args.links_json).read_text(encoding="utf-8"))
        if isinstance(data, dict):
            for title, url in data.items():
                links.append((str(title), str(url)))
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    links.append((str(item["title"]), str(item["url"])))
    for raw in args.link:
        if "=" not in raw:
            raise SystemExit("--link must use title=url format")
        title, url = raw.split("=", 1)
        links.append((title.strip(), url.strip()))
    if not links:
        raise SystemExit("ERROR: Provide at least one --link or --links-json")
    for title, url in links:
        if not title or not url.startswith(("http://", "https://")):
            raise SystemExit(f"ERROR: Invalid link {title!r}={url!r}")
    return links


def find_sequence_ids(config, targets: set[int]) -> dict[int, str]:
    fields = "fields=id,sequence_id&per_page=100"
    items = paginated_get(config, project_path(config, f"/work-items/?{fields}"))
    seq_to_id: dict[int, str] = {}
    for item in items:
        seq = item.get("sequence_id")
        item_id = item.get("id")
        if isinstance(seq, int) and isinstance(item_id, str) and seq in targets:
            seq_to_id[seq] = item_id
    return seq_to_id


def get_detail(config, work_item_id: str) -> dict:
    body, status = api_request(config, "GET", project_path(config, f"/work-items/{work_item_id}/"))
    if status >= 400 or not isinstance(body, dict):
        raise SystemExit(f"ERROR: Could not read work item {work_item_id}: HTTP {status} {body}")
    return body


def link_items_html(links: list[tuple[str, str]]) -> str:
    return "".join(f'<li>{title}: <a href="{url}">{url}</a></li>' for title, url in links)


def upsert_reference_links(html: str, links: list[tuple[str, str]]) -> str:
    new_items = link_items_html(links)
    cleaned = html.strip()
    ref_pattern = re.compile(r"(<h2>\s*Reference\s*</h2>\s*<ul>)([\s\S]*?)(</ul>)", re.I)
    match = ref_pattern.search(cleaned)
    if match:
        prefix, body, suffix = match.group(1), match.group(2), match.group(3)
        for title, url in links:
            body = re.sub(
                rf"<li>\s*{re.escape(title)}:\s*<a href=\"[^\"]+\">[^<]+</a>\s*</li>",
                "",
                body,
                flags=re.I,
            )
        return cleaned[: match.start()] + prefix + body.strip() + new_items + suffix + cleaned[match.end() :]
    return cleaned + "<h2>Reference</h2><ul>" + new_items + "</ul>"


def patch_description(config, work_item_id: str, html: str) -> None:
    body, status = api_request(
        config,
        "PATCH",
        project_path(config, f"/work-items/{work_item_id}/"),
        {"description_html": html},
    )
    if status >= 400 or not isinstance(body, dict) or not body.get("id"):
        raise SystemExit(f"ERROR: Patch failed HTTP {status}: {body}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Add reference links to Plane work item descriptions.")
    parser.add_argument("--env", default=".env", help="Path to .env")
    parser.add_argument("--sequences", required=True, help="Comma/range sequence list, e.g. 1109-1126")
    parser.add_argument("--link", action="append", default=[], help="Reference link in title=url format")
    parser.add_argument("--links-json", help="JSON object {title:url} or list of {title,url}")
    parser.add_argument("--dry-run", action="store_true", help="Show planned changes only")
    args = parser.parse_args()

    config = load_config(Path(args.env))
    links = load_links(args)
    targets = parse_sequences(args.sequences)
    seq_to_id = find_sequence_ids(config, targets)
    missing = targets - set(seq_to_id)
    if missing:
        raise SystemExit(f"ERROR: Could not resolve sequence IDs: {sorted(missing)}")

    for seq in sorted(targets):
        work_item_id = seq_to_id[seq]
        detail = get_detail(config, work_item_id)
        html = str(detail.get("description_html") or "")
        new_html = upsert_reference_links(html, links)
        print(f"HAIRL-{seq}: add {len(links)} reference link(s)")
        if not args.dry_run:
            patch_description(config, work_item_id, new_html)
    print(f"Done: {len(targets)} processed.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Interrupted")
