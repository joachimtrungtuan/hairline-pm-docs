---
name: manual-test-bug-sync
description: Create Hairline manual test runs from the batch scaffolds, merge external tester results into the run's result files, and run the manual-testing bug lifecycle with Plane. Use when the user starts a test run or retest run for a phase, hands back filled batch files from the tester (or the tester's AI agent), asks to intake, validate, or merge manual test results, log Fail or Found rows as Plane bugs, sync Plane bug status into result files, list cases waiting for retest, process retest results, or refresh Batch Summary and run summary Progress Summary tables under testing/manual/v<N>/phases. Use it even when the user only says "the tester sent results back", "update the test progress", or "which bugs are fixed and need retesting".
---

# Manual Test Bug Sync

## Purpose

Keep the result files of the latest run, `local-docs/testing/manual/v<N>/phases/<phase>/results/run-<NN>-<YYYY-MM-DD>/`, the single, structure-safe record of manual test results and bug status. Each run is created from the scaffolds in `batches/` (never filled in) by `new-run`; the result file a tester copy merges into is the **hub**. Earlier runs are frozen. Results are never pasted by hand: a deterministic script validates the tester's copy, previews every change, and merges only after the user confirms. The contract is `local-docs/testing/TEST-STRATEGY.md`; this skill enforces it.

The skill orchestrates two existing skills for Plane work: `create-bug-tasks` (draft bug tasks) and `plane-api-commands` (create work items, read state). The bundled script never talks to Plane.

## Hard Rules

- Never fill in a scaffold in `batches/`, and never write to an earlier run unless the user explicitly asks (`--allow-frozen`).
- Never hand-edit result cells, Bug IDs, bug statuses, or summary tables. Every write goes through `scripts/batch-sync.py`, which preserves table structure and writes atomically.
- Never merge before the user has seen the per-case preview and confirmed. `merge --apply` requires `--expect-sha` from the confirmed preview, so a hub file that changed in between is refused.
- Definition edits by the tester (IDs, titles, steps, expected results, data sets, other sections), unknown cases, revision mismatches, and version mismatches are never merged. Report them to the user as proposals for the plan owner.
- Every Plane write (create, update) needs explicit user confirmation after a dry-run.
- Never set `Closed` from Plane state. Only a retest Pass sets `Closed`.
- Do not edit templates, `TEST-STRATEGY.md`, or the sibling skills. Write only run folders created by `new-run` (result files and `summary.md`), and the task file that `create-bug-tasks` produces.
- Follow token governance in the project `CLAUDE.md`: read the script's JSON or Markdown output, not whole batch files.

## Script

`scripts/batch-sync.py` (Python stdlib only). Always run it with the isolated interpreter and quoted absolute paths, because the workspace path contains spaces and Vietnamese characters. Paths below are relative to the workspace root (the folder that contains `local-docs/`):

```bash
SYNC="$PWD/local-docs/project-automation/skills-engineering/manual-test-bug-sync/scripts/batch-sync.py"
python3 -I "$SYNC" <command> --help
```

| Command | Writes | Use |
|---|---|---|
| `new-run --phase local-docs/testing/manual/v<N>/phases/<phase> [--date D] [--type full/retest] [--apply]` | New run folder | Copy every scaffold to `results/run-<NN>-<date>/`, carry Bug ID and Bug status forward from the previous run, write `summary.md` |
| `find-hub --tester F --root local-docs/testing/manual` | No | Locate the hub (result file in the latest run) by Batch ID + plan version + phase |
| `validate --hub H --tester F` | No | Errors and warnings only |
| `diff --hub H --tester F [--resolve CASE=tester/hub/reopen] [--format md]` | No | Per-case preview, conflicts, `hub_sha256` |
| `merge --hub H --tester F [--partial] [--resolve ...] --apply --expect-sha SHA` | Hub result file | Merge confirmed changes and refresh the Batch Summary |
| `bugs --batch H` or `--run R` | No | Rows to log (`Found`), Fail rows without a flag, Fail rows on a `Closed` bug (`fail_on_closed_bug`), notes to review |
| `set-bug --batch H --updates U.json [--apply]` | Hub result file | Write Bug ID and Bug status with transition checks |
| `apply-states --run R --states S.json --values plane-values.json [--apply]` | Result files | Map Plane states to `Fixed - retest` |
| `retest-list --root local-docs/testing/manual [--format md]` | No | Cases with `Fixed - retest`, plus `needs_reopen` (Fail on a `Closed` bug) |
| `summary --run R [--apply]` | Result files + `summary.md` | Recompute Batch Summary and the run summary Progress Summary. Exits 2 without writing when the run has no result files |

`R` is a run folder `results/run-<NN>-<YYYY-MM-DD>/`; `--root local-docs/testing/manual` covers the latest run of every phase in the newest plan version. Write commands are dry-run unless `--apply` is passed and refuse scaffolds and earlier runs. Exit code 2 with a JSON `error` on stderr means nothing was written.

## References

Load only what the current step needs:

- `references/validation-and-merge-rules.md`: what blocks a file, what rejects a case, conflict rules, and resolutions. Load before step 1.
- `references/bug-status-lifecycle.md`: allowed status transitions, Plane state mapping, multi-key Bug IDs. Load before steps 2 to 4.
- `references/plane-handoff.md`: how to hand rows to `create-bug-tasks`, write keys back, and read Plane states. Load before steps 2 and 3.

## Workflow

Create a progress checklist with only the steps the user asked for (start a run, intake, log bugs, sync status, retest list, summaries). Mark steps in progress and complete as you go. Get today's date with `TZ=Asia/Saigon date +%Y-%m-%d`.

### 0. Start a run

1. Before the tester starts (a full pass, or a retest of the cases on the retest list), dry-run `new-run --phase <phase folder> --date <start date> --type full` (or `retest`). Show the run name, previous run, files, and carried-forward bugs.
2. After the user confirms, run it with `--apply`. Send the tester the phase `test-guide.md` and the result files in the new run folder, never the scaffolds.
3. Tester copies made before 2026-10-20 (old Batch Control row `Phase / plan version`) still merge: if no run exists yet, create `run-01` dated the day testing started, then intake them into it.

### 1. Intake tester results

1. For each returned file, run `find-hub`. Continue only on status `ok`. For `minor_version_mismatch`, explain it and ask whether to proceed with `--allow-minor-mismatch` (case revisions are still checked one by one). For `not_found` (no run yet: offer step 0), `ambiguous`, `major_version_mismatch`, `superseded_run`, or `frozen_version`, stop for that file and report.
2. Run `diff --format md` and show the user the preview: file-level errors, tester proposals, Batch Control updates, and the per-case table.
3. Resolve before writing:
   - File-level errors (broken table, changed header, version mismatch): nothing merges. Tell the user what to fix in the tester copy.
   - Rejected cases: explain each (definition edit, bad enum, bad date, missing Last tested, retired case). Offer `--partial` to merge the clean cases now and leave rejected ones for a corrected copy.
   - Conflicts: show hub and tester values side by side and ask per case: `tester`, `hub`, or `reopen` (only for `closed_bug_failed_again`). Re-run `diff` with the `--resolve` answers.
4. After the user confirms the final preview, run `merge --apply --expect-sha <hub_sha256 from that preview>` with the same flags. The script also refreshes that result file's Batch Summary.
5. Evidence stays in the file-sharing service the tester chose; the batch keeps only the links (TEST-STRATEGY §5). Never store evidence files in the repository. For each `evidence_not_link` warning, ask the tester to upload the files and send the links.
6. Report updated, skipped, and proposal items. Tester proposals (definition edits, new cases, edited sections) go to the user as a list for the plan owner; never apply them here.

Retest returns use the same path, into the retest run's result files. When the hub row is `Fixed - retest` (carried forward by `new-run`) and the tester's run is newer, the merge sets `Closed` on Pass and `Reopened` on Fail, keeping the same Bug ID.

### 2. Log bugs

1. Run `bugs` for the merged result files (`--run R`). `to_log` rows (`Found`) are the candidates. Ask the user about `fail_on_closed_bug` rows (set `Reopened` with `set-bug`, or log a new bug), about `fail_without_bug_flag` rows and about `notes_to_review` rows whose Notes describe a usability problem; add only the ones the user approves.
2. Follow `references/plane-handoff.md` to hand the rows to `create-bug-tasks` (load and follow its `SKILL.md`). It drafts the task file and may split one bug into FE and BE tasks.
3. Through `plane-api-commands`, dry-run creation, show the per-task result, and create live only after the user confirms.
4. Build the `set-bug` updates file from the task file's `Source Bug ID` and `Plane Task Key` values, dry-run `set-bug`, show it, then `--apply`. Rows become `Logged` with their Plane key(s).

### 3. Sync Plane status

1. Collect Bug IDs for rows in `Logged`, `Reopened`, or `Fixed - retest` (`bugs` output or the batch rows via `retest-list` and `apply-states` dry-run).
2. Get each key's current Plane state as described in `references/plane-handoff.md` and save it as a states JSON file in the session scratchpad.
3. Dry-run `apply-states`, show `set_fixed_retest`, `ask_user`, and `no_change`. For `plane_cancelled` (cancelled or won't fix), `plane_state_unknown`, and `plane_moved_back_after_fix`, ask the user what to record; apply any agreed manual change with `set-bug`.
4. Run `apply-states --apply` after the user confirms.

### 4. Retest list

Run `retest-list --format md` (latest run of every phase with `--root`, one run with `--run`) and give the table to the user. Start a retest run (step 0, `--type retest`) and send its result files with the list; results come back through step 1.

### 5. Refresh summaries

Run `summary --run <run folder>` for each touched run, show the totals and any `unmatched_rows` or `added` batches, then run with `--apply`.

## Output To The User

End each run with a short report:

- Runs created (run folder, carried-forward bugs)
- Files merged and per-file counts (updated, unchanged, rejected, conflicts resolved)
- Tester proposals awaiting the plan owner
- Bugs created (case to Plane key), statuses changed, and items needing a decision
- Retest list (if requested) and refreshed totals
- Whether an update-log entry is needed: result and bug-status merges are record updates that do not bump versions, so ask the user rather than creating one by default
