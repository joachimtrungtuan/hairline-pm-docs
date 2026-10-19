---
name: manual-test-bug-sync
description: Merge external tester results back into Hairline manual test batch files and run the manual-testing bug lifecycle with Plane. Use when the user hands back filled batch files from the tester (or the tester's AI agent), asks to intake, validate, or merge manual test results, log Fail or Found rows as Plane bugs, sync Plane bug status into batch files, list cases waiting for retest, process retest results, or refresh Batch Summary and phase plan Progress Summary tables under testing/manual/phases. Use it even when the user only says "the tester sent results back", "update the test progress", or "which bugs are fixed and need retesting".
---

# Manual Test Bug Sync

## Purpose

Keep the hub batch files under `local-docs/testing/manual/phases/**` the single, structure-safe record of manual test results and bug status. Results are never pasted by hand: a deterministic script validates the tester's copy, previews every change, and merges only after the user confirms. The contract is `local-docs/testing/TEST-STRATEGY.md`; this skill enforces it.

The skill orchestrates two existing skills for Plane work: `create-bug-tasks` (draft bug tasks) and `plane-api-commands` (create work items, read state). The bundled script never talks to Plane.

## Hard Rules

- Never hand-edit result cells, Bug IDs, bug statuses, or summary tables. Every write goes through `scripts/batch-sync.py`, which preserves table structure and writes atomically.
- Never merge before the user has seen the per-case preview and confirmed. `merge --apply` requires `--expect-sha` from the confirmed preview, so a hub file that changed in between is refused.
- Definition edits by the tester (IDs, titles, steps, expected results, data sets, other sections), unknown cases, revision mismatches, and version mismatches are never merged. Report them to the user as proposals for the plan owner.
- Every Plane write (create, update) needs explicit user confirmation after a dry-run.
- Never set `Closed` from Plane state. Only a retest Pass sets `Closed`.
- Do not edit templates, `TEST-STRATEGY.md`, or the sibling skills. Write only hub batch files, phase `plan.md` Progress Summary tables, and the task file that `create-bug-tasks` produces.
- Follow token governance in the project `CLAUDE.md`: read the script's JSON or Markdown output, not whole batch files.

## Script

`scripts/batch-sync.py` (Python stdlib only). Always run it with the isolated interpreter and quoted absolute paths, because the workspace path contains spaces and Vietnamese characters. Paths below are relative to the workspace root (the folder that contains `local-docs/`):

```bash
SYNC="$PWD/local-docs/project-automation/skills-engineering/manual-test-bug-sync/scripts/batch-sync.py"
python3 -I "$SYNC" <command> --help
```

| Command | Writes | Use |
|---|---|---|
| `find-hub --tester F --root local-docs/testing/manual/phases` | No | Locate the hub file by Batch ID + phase/plan version |
| `validate --hub H --tester F` | No | Errors and warnings only |
| `diff --hub H --tester F [--resolve CASE=tester/hub/reopen] [--format md]` | No | Per-case preview, conflicts, `hub_sha256` |
| `merge --hub H --tester F [--partial] [--resolve ...] --apply --expect-sha SHA` | Hub batch | Merge confirmed changes and refresh the Batch Summary |
| `bugs --batch H` or `--plan P` | No | Rows to log (`Found`), Fail rows without a flag, Fail rows on a `Closed` bug (`fail_on_closed_bug`), notes to review |
| `set-bug --batch H --updates U.json [--apply]` | Hub batch | Write Bug ID and Bug status with transition checks |
| `apply-states --plan P --states S.json --values plane-values.json [--apply]` | Hub batch | Map Plane states to `Fixed - retest` |
| `retest-list --root local-docs/testing/manual/phases [--format md]` | No | Cases with `Fixed - retest`, plus `needs_reopen` (Fail on a `Closed` bug) |
| `summary --plan P [--apply]` | Batches + plan | Recompute Batch Summary and plan Progress Summary. Exits 2 without writing when the plan has no batch files yet |

Write commands are dry-run unless `--apply` is passed. Exit code 2 with a JSON `error` on stderr means nothing was written.

## References

Load only what the current step needs:

- `references/validation-and-merge-rules.md`: what blocks a file, what rejects a case, conflict rules, and resolutions. Load before step 1.
- `references/bug-status-lifecycle.md`: allowed status transitions, Plane state mapping, multi-key Bug IDs. Load before steps 2 to 4.
- `references/plane-handoff.md`: how to hand rows to `create-bug-tasks`, write keys back, and read Plane states. Load before steps 2 and 3.

## Workflow

Create a progress checklist with only the steps the user asked for (intake, log bugs, sync status, retest list, summaries). Mark steps in progress and complete as you go. Get today's date with `TZ=Asia/Saigon date +%Y-%m-%d`.

### 1. Intake tester results

1. For each returned file, run `find-hub`. Continue only on status `ok`. For `minor_version_mismatch`, explain it and ask whether to proceed with `--allow-minor-mismatch` (case revisions are still checked one by one). For `not_found`, `ambiguous`, `major_version_mismatch`, or `frozen_version`, stop for that file and report.
2. Run `diff --format md` and show the user the preview: file-level errors, tester proposals, Batch Control updates, and the per-case table.
3. Resolve before writing:
   - File-level errors (broken table, changed header, version mismatch): nothing merges. Tell the user what to fix in the tester copy.
   - Rejected cases: explain each (definition edit, bad enum, bad date, missing Last tested, retired case). Offer `--partial` to merge the clean cases now and leave rejected ones for a corrected copy.
   - Conflicts: show hub and tester values side by side and ask per case: `tester`, `hub`, or `reopen` (only for `closed_bug_failed_again`). Re-run `diff` with the `--resolve` answers.
4. After the user confirms the final preview, run `merge --apply --expect-sha <hub_sha256 from that preview>` with the same flags. The script also refreshes that batch's Batch Summary.
5. Evidence stays in the file-sharing service the tester chose; the batch keeps only the links (TEST-STRATEGY §5). Never store evidence files in the repository. For each `evidence_not_link` warning, ask the tester to upload the files and send the links.
6. Report updated, skipped, and proposal items. Tester proposals (definition edits, new cases, edited sections) go to the user as a list for the plan owner; never apply them here.

Retest returns use the same path. When the hub row is `Fixed - retest` and the tester's run is newer, the merge sets `Closed` on Pass and `Reopened` on Fail, keeping the same Bug ID.

### 2. Log bugs

1. Run `bugs` for the merged batches. `to_log` rows (`Found`) are the candidates. Ask the user about `fail_on_closed_bug` rows (set `Reopened` with `set-bug`, or log a new bug), about `fail_without_bug_flag` rows and about `notes_to_review` rows whose Notes describe a usability problem; add only the ones the user approves.
2. Follow `references/plane-handoff.md` to hand the rows to `create-bug-tasks` (load and follow its `SKILL.md`). It drafts the task file and may split one bug into FE and BE tasks.
3. Through `plane-api-commands`, dry-run creation, show the per-task result, and create live only after the user confirms.
4. Build the `set-bug` updates file from the task file's `Source Bug ID` and `Plane Task Key` values, dry-run `set-bug`, show it, then `--apply`. Rows become `Logged` with their Plane key(s).

### 3. Sync Plane status

1. Collect Bug IDs for rows in `Logged`, `Reopened`, or `Fixed - retest` (`bugs` output or the batch rows via `retest-list` and `apply-states` dry-run).
2. Get each key's current Plane state as described in `references/plane-handoff.md` and save it as a states JSON file in the session scratchpad.
3. Dry-run `apply-states`, show `set_fixed_retest`, `ask_user`, and `no_change`. For `plane_cancelled` (cancelled or won't fix), `plane_state_unknown`, and `plane_moved_back_after_fix`, ask the user what to record; apply any agreed manual change with `set-bug`.
4. Run `apply-states --apply` after the user confirms.

### 4. Retest list

Run `retest-list --format md` (whole tree with `--root`, one phase with `--plan`) and give the table to the user for the tester. Retest results come back through step 1.

### 5. Refresh summaries

Run `summary --plan <phase plan.md>` for each touched phase version, show the totals and any `unmatched_rows` or `added` batches, then run with `--apply`.

## Output To The User

End each run with a short report:

- Files merged and per-file counts (updated, unchanged, rejected, conflicts resolved)
- Tester proposals awaiting the plan owner
- Bugs created (case to Plane key), statuses changed, and items needing a decision
- Retest list (if requested) and refreshed totals
- Whether an update-log entry is needed: result and bug-status merges are record updates that do not bump versions, so ask the user rather than creating one by default
