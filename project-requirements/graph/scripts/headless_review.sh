#!/usr/bin/env bash
# Run one checklist-driven review of a frozen FR PRD through a headless OpenCode
# model with restricted permissions: no shell, no network, writes only to the
# output folder, reads anywhere. The controller pre-computes the graph query so
# the model never needs to execute anything. Inputs are symlinked into <output-dir>/in
# because OpenCode's external_directory permission is denied; the only writable file is report.md.
#
# Usage: scripts/headless_review.sh <model> <FR-id> <checklist-path> <output-dir> [timeout-seconds]
#   model          e.g. opencode-go/glm-5.3-flash
#   FR-id          e.g. FR-005
#   checklist-path path relative to the project root, e.g. local-docs/project-requirements/graph/checklists/completeness-check.md
#   output-dir     folder that will receive report.md and status.json (created)
#   timeout        default 600
# Exit codes: 0 report written, 124 timeout, other = opencode failure. status.json always written.
set -u
MODEL="$1"; FR="$2"; CHECKLIST="$3"; OUT="$4"; TIMEOUT="${5:-600}"
GRAPH_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ROOT="$(cd "$GRAPH_DIR/../../.." && pwd)"
PY="${GRAPH_PY:-/usr/bin/python3}"   # system python with PyYAML; override with GRAPH_PY
mkdir -p "$OUT"; OUT="$(cd "$OUT" && pwd)"
slug=$(ls "$ROOT/archived/prd-baseline-2026-11-08" | grep -i "^$(echo "$FR" | tr 'A-Z' 'a-z' | tr -d '-')-" | head -1)
PRD="$ROOT/archived/prd-baseline-2026-11-08/$slug/prd.md"
[ -f "$PRD" ] || { echo "{\"status\":\"error\",\"reason\":\"PRD not found for $FR\"}" > "$OUT/status.json"; exit 2; }
PRD_LINES=$(wc -l < "$PRD" | tr -d ' ')
mkdir -p "$OUT/in"
ln -sfn "$PRD" "$OUT/in/prd.md"
ln -sfn "$ROOT/$CHECKLIST" "$OUT/in/checklist.md"
rm -f "$OUT/in/graph.json"; cp "$GRAPH_DIR/graph.json" "$OUT/in/graph.json"   # snapshot: the controller may re-export mid-run
ln -sfn "$GRAPH_DIR/schema.yaml" "$OUT/in/schema.yaml"
ln -sfn "$GRAPH_DIR/checklists/migrate-fr.md" "$OUT/in/migrate-fr.md"
( cd "$GRAPH_DIR" && "$PY" scripts/query.py fr "$FR" --json ) > "$OUT/in/fr-nodes.json" 2>"$OUT/query.err" || true
rm -f "$OUT/report.md"
EXPORTED=$("$PY" -c "import json,sys;d=json.load(open(sys.argv[1]));print(d.get('changes',[{}])[0].get('at',''))" "$GRAPH_DIR/graph.json" 2>/dev/null)

cat > "$OUT/opencode.json" <<JSON
{
  "\$schema": "https://opencode.ai/config.json",
  "permission": {
    "bash": "deny",
    "webfetch": "deny",
    "websearch": "deny",
    "task": "deny",
    "skill": "deny",
    "question": "deny",
    "external_directory": "deny",
    "read": "allow",
    "glob": "allow",
    "grep": "allow",
    "list": "allow",
    "edit": { "*": "deny", "report.md": "allow" }
  }
}
JSON

PROMPT="You are a documentation reviewer. Work only by reading files and writing one output file; you have no shell and no network.
Task: run the checklist at '$ROOT/$CHECKLIST' for $FR, from beginning to end, and write the report it specifies to '$OUT/report.md'. Nothing else may be written.
Inputs:
- Checklist (read it fully first; it is authoritative, including the report format): $OUT/in/checklist.md (it is $CHECKLIST)
- Frozen PRD ($PRD_LINES lines; read it in ranges of at most 200 lines; cite line numbers): $OUT/in/prd.md (it is $PRD)
- Graph export: $OUT/in/graph.json (large; search it for key phrases and ids rather than reading it whole)
- Pre-computed result of 'query.py fr $FR --json' (the nodes $FR owns): $OUT/in/fr-nodes.json
- Node types: $OUT/in/schema.yaml
- Graph export timestamp for the header: $EXPORTED
- Flow-step and change-set rules: $OUT/in/migrate-fr.md (read it only after the line table is complete, as the checklist says; you need step 2 'Flow steps' and step 5 'Write the change-set')
Change-set operations are one JSON object per line, for example:
  - {\"op\": \"add_node\", \"id\": \"STP-005-001\", \"type\": \"Step\", \"title\": \"Patient opens quote list\", \"owner_fr\": \"FR-005\", \"attrs\": {\"prd_ref\": \"Main Flow step 1\"}}
  - {\"op\": \"add_edge\", \"from\": \"STP-005-001\", \"verb\": \"next\", \"to\": \"STP-005-002\", \"attrs\": {\"label\": \"quote accepted\"}}
  - {\"op\": \"add_node\", \"id\": \"FLW-005-main\", \"type\": \"Flow\", \"title\": \"Quote comparison main flow\", \"attrs\": {\"kind\": \"main\", \"prd_ref\": \"Main Flow\"}}
You have no shell, so you cannot validate a change-set: follow the checklist step 7 rule for a checker with no shell and put the draft YAML block in the report.
Rules: all inputs are inside $OUT/in; you cannot read or write anywhere else. The only file you may write is $OUT/report.md. Do not read any migration report or migrate-fr.md before the line table is complete; the checklist says when you may. Never guess between two business readings; record a 'Needs user decision' item instead. Finish by writing the complete report to $OUT/report.md, ending with the Status line the checklist requires."

START=$(date +%s)
( cd "$OUT" && timeout "$TIMEOUT" opencode run --model "$MODEL" --archived --format json --title "headless-$FR-$(date +%H%M%S)" "$PROMPT" > "$OUT/opencode.jsonl" 2> "$OUT/opencode.err" )
RC=$?
END=$(date +%s)
REPORT_LINES=0; [ -f "$OUT/report.md" ] && REPORT_LINES=$(wc -l < "$OUT/report.md" | tr -d ' ')
STATUS="ok"; [ $RC -eq 124 ] && STATUS="timeout"; { [ $RC -ne 0 ] && [ $RC -ne 124 ]; } && STATUS="error"
[ "$REPORT_LINES" -eq 0 ] && [ "$STATUS" = "ok" ] && STATUS="no-report"
DENIED=$(grep -c '"permission' "$OUT/opencode.jsonl" 2>/dev/null || echo 0)
USAGE=$("$PY" "$GRAPH_DIR/scripts/opencode_usage.py" "$OUT/opencode.jsonl" 2>/dev/null || echo '{}')
cat > "$OUT/status.json" <<JSON
{"fr":"$FR","model":"$MODEL","checklist":"$CHECKLIST","status":"$STATUS","exit_code":$RC,"seconds":$((END-START)),"report_lines":$REPORT_LINES,"permission_events":$DENIED,"prd_lines":$PRD_LINES,"graph_exported":"$EXPORTED","usage":$USAGE}
JSON
cat "$OUT/status.json"
[ "$STATUS" = "ok" ] && exit 0
[ "$STATUS" = "timeout" ] && exit 124
exit 1
