# Plane Handoff

How this skill hands rows to `create-bug-tasks` and `plane-api-commands`, and how results come back. Load the sibling skill's `SKILL.md` and follow it when you reach its part; this file only covers the seams.

## 1. Rows To `create-bug-tasks`

Run `bugs` and use each approved `to_log` row as one pasted bug for `create-bug-tasks` (its "General Bug Sources" path). Map fields as follows:

| Batch row or context | Bug field for `create-bug-tasks` |
|---|---|
| `case` (full ID with revision, for example `PR01-FR002-03 r1`) | Source Bug ID; also add it to Reference and Notes |
| `Title` | Short bug title basis |
| `context.module` and the case ID's FR (`FR002` becomes `FR-002`) | Product Module and FR |
| `PRD flow ref` and `context.prd_sources` | PRD reference (`create-bug-tasks` converts `local-docs/` paths to GitHub links) |
| `batch_file` (as a `local-docs/testing/manual/phases/...` path) | Source report link |
| `context.phase_version`, `context.batch`, `context.build_tested`, `context.platform` | Notes (traceability and environment) |
| `Preconditions`, `Test data`, `Steps` | Steps to Reproduce (keep data-set IDs and account placeholders such as `{V1}`; never resolve credentials) |
| `Actual result / data` | Current Status |
| `Expected result` | Expectation (Suggestion) |
| `Evidence` | Evidence: each file name with its folder `local-docs/testing/manual/phases/<phase-folder>/v<major>.0/evidence/<batch>/`, or the shared-drive link |
| `Notes` | Notes (usability context) |
| `Priority` | Source priority |

Tell `create-bug-tasks` that the user has asked for the source status write-back in this run, so step 4 below is in scope.

## 2. Create In Plane

Use `plane-api-commands` mode `create-work-item`: run `create-plane-issues.py --dry-run` on the task file, show the per-task labels, module, cycle, and parent, and create live only after the user confirms. The script writes `Plane Task ID` and `Plane Task Key` into the task file.

## 3. Map Keys Back

From the task file, read each task's `Source Bug ID` and `Plane Task Key`. Group keys by Source Bug ID (FE and BE splits share one), then write a `set-bug` updates file in the session scratchpad:

```json
[
  {"case": "PR01-FR002-07 r1", "status": "Logged", "bug_id": "HAIRL-1600, HAIRL-1601"}
]
```

Dry-run `set-bug --batch <hub file> --updates <file>`, show the planned changes, then add `--apply`. One `set-bug` call per batch file.

## 4. Read Plane States

`apply-states` needs a JSON object mapping each key to its state, in either form:

```json
{"HAIRL-1600": "Finished", "HAIRL-1601": {"state": "Waiting for Deployment", "group": "completed"}}
```

Get the states through `plane-api-commands`. Its hard rules forbid one-off scripts, and as of 2026-10-19 its `scripts/` folder has no read-only work-item state command. So:

1. Check `plane-api-commands/SKILL.md` and its `scripts/` for a mode that reads work-item states by key. If one exists, use it and convert its output to the JSON above.
2. If none exists, stop this step and tell the user. Offer two options:
   - Approve a script update to `plane-api-commands` (a frozen folder, so it needs the user's explicit approval). Proposed shape: `fetch-work-item-states.py --env .env --values plane-values.json --keys HAIRL-1600,HAIRL-1601 --output <states.json>`, read-only GET of `/work-items/` by sequence ID, output in the format above.
   - Paste the current states from Plane (key and state name). Write them to the states file and continue.

Save the states file in the session scratchpad, not under `local-docs/`. Then dry-run `apply-states` with `--values local-docs/project-automation/task-creation/plane-api/plane-values.json`.
