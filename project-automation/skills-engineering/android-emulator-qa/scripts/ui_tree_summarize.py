#!/usr/bin/env python3
"""
ui_tree_summarize.py — Compact readable summary of ADB UI tree XML.

Filters to elements that have non-empty text, content-desc, or resource-id.
Output is indented to reflect nesting depth.

Usage:
  python ui_tree_summarize.py <xml_file>
  python ui_tree_summarize.py <xml_file> --bounds   # include bounds in output

Arguments:
  xml_file   Path to UI tree XML (from uiautomator dump)
  --bounds   Optional: include [x1,y1][x2,y2] bounds in output

Output:
  Indented text summary of meaningful UI elements

Example:
  adb exec-out uiautomator dump /dev/tty > ui.xml
  python ui_tree_summarize.py ui.xml
  # Output:
  #   [Button] "Sign In" (id: com.example:id/btn_signin)
  #     [TextView] "Enter your credentials"
"""

import sys
import xml.etree.ElementTree as ET


def summarize_node(node, depth=0, show_bounds=False):
    """Recursively summarize meaningful nodes. Returns list of strings."""
    lines = []
    indent = "  " * depth

    # Gather meaningful attributes
    text = node.get("text", "").strip()
    content_desc = node.get("content-desc", "").strip()
    resource_id = node.get("resource-id", "").strip()
    bounds = node.get("bounds", "")
    class_name = node.get("class", "").split(".")[-1]  # Short class name
    clickable = node.get("clickable", "false") == "true"
    scrollable = node.get("scrollable", "false") == "true"

    has_content = bool(text or content_desc or resource_id)

    if has_content:
        parts = []

        # Class tag
        tag = f"[{class_name}]" if class_name else "[View]"

        # Flags
        flags = []
        if clickable:
            flags.append("clickable")
        if scrollable:
            flags.append("scrollable")
        flag_str = f" ({', '.join(flags)})" if flags else ""

        # Text content
        if text:
            parts.append(f'"{text}"')
        if content_desc and content_desc != text:
            parts.append(f'desc="{content_desc}"')
        if resource_id:
            # Shorten resource-id (remove package prefix)
            short_id = resource_id.split("/")[-1] if "/" in resource_id else resource_id
            parts.append(f"id:{short_id}")

        content_str = " ".join(parts)
        bounds_str = f" {bounds}" if (show_bounds and bounds) else ""

        lines.append(f"{indent}{tag}{flag_str} {content_str}{bounds_str}")

    # Recurse into children
    for child in node:
        child_lines = summarize_node(child, depth + (1 if has_content else 0), show_bounds)
        lines.extend(child_lines)

    return lines


def main():
    show_bounds = "--bounds" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if len(args) != 1:
        print(f"Usage: {sys.argv[0]} <xml_file> [--bounds]", file=sys.stderr)
        sys.exit(1)

    xml_file = args[0]

    try:
        with open(xml_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
    except FileNotFoundError:
        print(f"Error: File not found: {xml_file}", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    if not content:
        print(f"Error: XML file is empty: {xml_file}", file=sys.stderr)
        sys.exit(1)

    try:
        root = ET.fromstring(content)
    except ET.ParseError as e:
        print(f"Error: Malformed XML: {e}", file=sys.stderr)
        sys.exit(1)

    lines = summarize_node(root, depth=0, show_bounds=show_bounds)

    if not lines:
        print("(no meaningful elements found — Flutter sparse tree; use coordinate-based interaction)")
    else:
        print("\n".join(lines))


if __name__ == "__main__":
    main()
