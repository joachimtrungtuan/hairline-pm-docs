#!/usr/bin/env bash
#
# check-code-map-drift.sh — detect when main/ folder structure has drifted from
# what the curated semantic code maps document, so we know when to refresh them.
#
# Bundled with the `gen-code-map` skill. The maps at
# local-docs/project-notes/code-map-{backend,frontend,app}.md describe folder
# GROUPS and their purpose / module (P-,PR-,A-,S-) / FR relations. They are
# curated, not auto-generated, and age slowly — but when the dev team adds or
# removes folders a group may need updating. This script snapshots the directory
# structure (deps/build excluded) and diffs each run, so the map is refreshed only
# for what actually changed instead of re-reading code.
#
# This script does NOT read file contents and does NOT call an LLM — folder layout
# only. Refreshing the maps is the curated skill step (see ../SKILL.md).
#
# Usage:
#   check-code-map-drift.sh             # diff current dirs vs last snapshot (all)
#   check-code-map-drift.sh backend     # one codebase: backend | frontend | app
#   check-code-map-drift.sh accept      # save current dirs as new snapshot (all)
#   check-code-map-drift.sh accept app  # accept one codebase
#   check-code-map-drift.sh -h
#
# Exit codes:
#   0  no drift (or accept succeeded)
#   3  drift detected — added/removed folders printed (a signal, not a failure)
#   1  no snapshot yet for a codebase (run `accept` to seed it)
#
# Requires only POSIX find / sort / comm. (repomix is needed only for the optional
# on-demand signature command in each map's header — not by this script.)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# scripts/ -> gen-code-map -> skills-engineering -> project-automation -> local-docs -> repo root
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
SNAP_DIR="$REPO_ROOT/local-docs/project-notes/.code-map-snapshots"

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  sed -n '2,40p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
  exit 0
fi

# Scoped source roots per codebase (relative to repo root).
roots_for() {
  case "$1" in
    backend)  echo "main/hairline-backend/app main/hairline-backend/routes main/hairline-backend/database" ;;
    frontend) echo "main/hairline-frontend/src" ;;
    app)      echo "main/hairline-app/lib" ;;
    *) return 1 ;;
  esac
}

# Print sorted, repo-relative directory paths for a codebase, excluding deps/build dirs.
list_dirs() {
  local app="$1" root
  for root in $(roots_for "$app"); do
    [ -d "$REPO_ROOT/$root" ] || continue
    find "$REPO_ROOT/$root" \
      \( -name node_modules -o -name vendor -o -name storage -o -name build \
         -o -name .dart_tool -o -name dist -o -name .git -o -name coverage \) -prune \
      -o -type d -print
  done | sed "s#^$REPO_ROOT/##" | sort -u
}

mkdir -p "$SNAP_DIR"

accept_one() {
  local app="$1"
  list_dirs "$app" > "$SNAP_DIR/$app.dirs"
  printf "  accepted %s (%s folders)\n" "$app" "$(wc -l < "$SNAP_DIR/$app.dirs" | tr -d ' ')"
}

check_one() {
  local app="$1" snap="$SNAP_DIR/$1.dirs"
  if [ ! -f "$snap" ]; then
    echo "→ $app: no snapshot yet — run 'check-code-map-drift.sh accept' to seed it." >&2
    return 1
  fi
  local cur added removed
  cur="$(list_dirs "$app")"
  added="$(comm -13 "$snap" <(printf '%s\n' "$cur") || true)"
  removed="$(comm -23 "$snap" <(printf '%s\n' "$cur") || true)"
  if [ -z "$added" ] && [ -z "$removed" ]; then
    echo "→ $app: no drift."
    return 0
  fi
  echo "→ $app: DRIFT — refresh the affected groups in code-map-$app.md:"
  [ -n "$added" ]   && printf '%s\n' "$added"   | sed 's/^/    + /'
  [ -n "$removed" ] && printf '%s\n' "$removed" | sed 's/^/    - /'
  return 3
}

MODE="check"
if [ "${1:-}" == "accept" ]; then MODE="accept"; shift; fi
TARGET="${1:-all}"

case "$TARGET" in
  backend|frontend|app) APPS="$TARGET" ;;
  all) APPS="backend frontend app" ;;
  *) echo "ERROR: unknown target '$TARGET'. Use backend | frontend | app | all." >&2; exit 64 ;;
esac

rc=0
if [ "$MODE" == "accept" ]; then
  echo "Snapshotting current folder structure:"
  for a in $APPS; do accept_one "$a"; done
  echo "Done. Snapshots saved under ${SNAP_DIR#$REPO_ROOT/}/."
else
  for a in $APPS; do check_one "$a" || rc=$?; done
  [ "$rc" -eq 0 ] && echo "No drift across checked codebases." \
    || echo "Drift detected — update the flagged groups, then run 'check-code-map-drift.sh accept'."
fi
exit "$rc"
