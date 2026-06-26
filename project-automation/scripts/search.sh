#!/usr/bin/env bash
#
# search.sh — capped ripgrep wrapper for the Hairline docs project.
#
# Purpose: enforce the project's token governance. A normal `rg` can dump
# hundreds of matches into an agent's context. This wrapper refuses to do that:
# if a query matches more than a hard cap (default 50), it prints ONLY a count
# and a refinement hint, then exits non-zero — forcing you to narrow the query
# (add a path, an anchor like ^, or a more exact term) instead of flooding
# context.
#
# Usage:
#   search.sh [-l] [-c N] PATTERN [PATH ...]
#
#   -l        files-with-matches mode (rg -l): list matching files only.
#   -c N      override the match cap for this run (default 50).
#   -h        show this help.
#
#   PATTERN   ripgrep pattern (required).
#   PATH ...  optional path(s) to search; defaults to current directory.
#
# The cap can also be set via the SEARCH_CAP environment variable; the -c flag
# takes precedence over it.
#
# Behavior:
#   - Normal output is numbered (rg -n) unless -l is used.
#   - Under-or-at cap  -> prints matches, exit 0.
#   - Over cap         -> prints "N matches — too many, refine your query
#                         (add a path, anchor, or exact term)", exit 2.
#   - No matches       -> exit 1 (same as rg).
#
# Examples:
#   search.sh "FR-0[0-9][0-9]" local-docs/project-requirements/system-prd.md
#   search.sh -l "transcription" local-docs/
#   search.sh -c 100 "TODO" local-docs/

set -euo pipefail

# ---- defaults -------------------------------------------------------------
CAP="${SEARCH_CAP:-50}"   # hard cap on number of matches
LIST_MODE=0               # -l: files-with-matches

usage() {
  # Print the comment header (everything from the first '# Usage' style block).
  sed -n '3,40p' "$0" | sed 's/^# \{0,1\}//'
  exit "${1:-0}"
}

# ---- arg parsing ----------------------------------------------------------
while getopts ":lc:h" opt; do
  case "$opt" in
    l) LIST_MODE=1 ;;
    c) CAP="$OPTARG" ;;
    h) usage 0 ;;
    :) echo "search.sh: option -$OPTARG requires an argument" >&2; exit 64 ;;
    \?) echo "search.sh: unknown option -$OPTARG" >&2; exit 64 ;;
  esac
done
shift $((OPTIND - 1))

if [ "$#" -lt 1 ]; then
  echo "search.sh: missing PATTERN" >&2
  usage 64
fi

# Validate cap is a positive integer.
case "$CAP" in
  ''|*[!0-9]*) echo "search.sh: cap must be a positive integer (got '$CAP')" >&2; exit 64 ;;
esac

PATTERN="$1"
shift
# Remaining args are paths (may be empty -> rg defaults to current dir).

# ---- count first, then decide --------------------------------------------
# We count matches without printing them, so an over-cap query never floods
# context. `rg -c` prints per-file counts; summing them gives the total.
# For list mode we count matching files instead.
# Note: rg exits non-zero when there are no matches. Under `set -e` (with
# pipefail) a failing pipeline inside an assignment would abort the script, so
# each counting pipeline is guarded with `|| true` — a zero count is a valid
# result we want to handle ourselves, not a fatal error.
if [ "$LIST_MODE" -eq 1 ]; then
  # Count of files with matches.
  total="$( { rg -l "$PATTERN" "$@" 2>/dev/null || true; } | wc -l | tr -d ' ')"
else
  # Sum per-file match counts. rg -c emits "file:count" lines; sum the counts.
  total="$( { rg -c "$PATTERN" "$@" 2>/dev/null || true; } \
    | awk -F: '{ s += $NF } END { print s + 0 }')"
fi

# No matches at all.
if [ "${total:-0}" -eq 0 ]; then
  echo "0 matches"
  exit 1
fi

# Over the cap: refuse to dump, force refinement.
if [ "$total" -gt "$CAP" ]; then
  echo "$total matches — too many, refine your query (add a path, anchor, or exact term)"
  exit 2
fi

# ---- within cap: emit the real output -------------------------------------
if [ "$LIST_MODE" -eq 1 ]; then
  rg -l "$PATTERN" "$@"
else
  rg -n "$PATTERN" "$@"
fi
