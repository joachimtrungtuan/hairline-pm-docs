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
| `Evidence` | Evidence: the links from the case row's Evidence cell |
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

Get the states through `plane-api-commands` mode `read-states` (load and follow its `SKILL.md`): pass every key from the batch files' Bug ID cells as `--keys` and write `--output` to the session scratchpad. Its output is already in the second form above. If it reports missing keys, ask the user whether each bug was deleted or moved and record the agreed status with `set-bug`. If Plane cannot be reached, ask the user to paste the current states (key and state name) and write them to the states file.

Save the states file in the session scratchpad, not under `local-docs/`. Then dry-run `apply-states` with `--values local-docs/project-automation/task-creation/plane-api/plane-values.json`.
