"""Sum token use and cost from an OpenCode `run --format json` log.

Each finished model step in the log carries a `tokens` object and a `cost`. This prints one JSON
object: steps, input, output, reasoning, cache_read, cache_write, cost. Lines that are not JSON,
and events without usage, are skipped, so a partial log from a timed-out run still gives a total.

Usage: opencode_usage.py <opencode.jsonl>
"""
import json
import sys

KEYS = ("input", "output", "reasoning", "cache_read", "cache_write")


def _usage_parts(obj):
    """Yield every dict in obj that holds a `tokens` dict (OpenCode puts it on the step part)."""
    if isinstance(obj, dict):
        if isinstance(obj.get("tokens"), dict):
            yield obj
            return
        for value in obj.values():
            yield from _usage_parts(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from _usage_parts(value)


def summarise(lines):
    total = {"steps": 0, **{k: 0 for k in KEYS}, "cost": 0.0}
    for line in lines:
        try:
            event = json.loads(line)
        except ValueError:
            continue
        for part in _usage_parts(event):
            tokens = part["tokens"]
            cache = tokens.get("cache") if isinstance(tokens.get("cache"), dict) else {}
            total["steps"] += 1
            total["input"] += int(tokens.get("input") or 0)
            total["output"] += int(tokens.get("output") or 0)
            total["reasoning"] += int(tokens.get("reasoning") or 0)
            total["cache_read"] += int(cache.get("read") or 0)
            total["cache_write"] += int(cache.get("write") or 0)
            total["cost"] += float(part.get("cost") or 0)
    total["cost"] = round(total["cost"], 6)
    return total


def main(argv):
    if len(argv) != 2:
        print(__doc__.strip().splitlines()[-1], file=sys.stderr)
        return 2
    with open(argv[1], encoding="utf-8", errors="replace") as handle:
        print(json.dumps(summarise(handle)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
