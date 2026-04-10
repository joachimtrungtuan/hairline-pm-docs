#!/usr/bin/env python3
"""
ui_pick.py — Extract center tap coordinates from ADB UI tree XML.

Usage:
  python ui_pick.py <xml_file> <search_term>

Arguments:
  xml_file     Path to UI tree XML (from uiautomator dump)
  search_term  Text to match against 'text', 'resource-id', or 'content-desc' attributes

Output:
  x,y          Center coordinates of the first matching element
               Prints error message and exits with code 1 if not found

Example:
  adb exec-out uiautomator dump /dev/tty > ui.xml
  python ui_pick.py ui.xml "Sign In"
  # Output: 540,960
  # Use with: adb shell input tap $(python ui_pick.py ui.xml "Sign In")
"""

import sys
import xml.etree.ElementTree as ET


def parse_bounds(bounds_str):
    """Parse '[x1,y1][x2,y2]' into center (cx, cy)."""
    try:
        bounds_str = bounds_str.strip()
        # Format: [x1,y1][x2,y2]
        parts = bounds_str.replace("][", ",").strip("[]").split(",")
        x1, y1, x2, y2 = int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        return cx, cy
    except (ValueError, IndexError):
        return None


def search_node(node, search_term):
    """Search node and children for matching element. Returns (cx, cy) or None."""
    search_lower = search_term.lower()
    for attr in ("text", "resource-id", "content-desc"):
        value = node.get(attr, "")
        if search_lower in value.lower():
            bounds = node.get("bounds", "")
            if bounds:
                coords = parse_bounds(bounds)
                if coords:
                    return coords

    for child in node:
        result = search_node(child, search_term)
        if result:
            return result

    return None


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <xml_file> <search_term>", file=sys.stderr)
        sys.exit(1)

    xml_file = sys.argv[1]
    search_term = sys.argv[2]

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

    result = search_node(root, search_term)

    if result:
        cx, cy = result
        print(f"{cx},{cy}")
    else:
        print(f"Error: No element found matching '{search_term}'", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
