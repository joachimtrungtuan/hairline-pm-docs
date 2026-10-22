# Delta Mode

Re-check an existing report after the PRDs or the code changed, without re-running every unit.
The report is updated in place: unchanged verdicts carry forward, only affected units are
re-checked, and gap IDs stay stable so tasks already filed from them still point to the right row.

## When to use

The user points at an existing complete report and asks to re-run, re-check, refresh, or update
it, or asks "what changed since the last review". For a crashed run that never finished, use
Resume mode instead. If the user wants a full re-review from scratch, run the normal workflow
into a new run-date folder.

## 1. Read the report (by section, never whole)

Read the header, the Summary table, the `## Unit baseline` section if present, and the Evidence
appendix lines for units you will need. Note the run date, plan version, scope, engine line,
repo commits, and the latest Revisions entry (its SHAs and date supersede the header's).

## 2. Detect what changed

Run the detection with no subagents; it is cheap and the user sees its result before anything
expensive starts.

**PRD side.** Re-derive the scope's units with `item-derivation.md`, exactly as on a first run.
Then compare with the report:

- **New unit**: an ID that is not in the Summary.
- **Gone unit**: a Summary ID that no longer derives. Before calling it Retired, check whether a
  new ID in the same FR has the same title and the same excerpt hash; positional IDs (`W3`,
  `E2`) shift when sections are inserted. If so, it is a renamed unit: keep the old row, update
  its ID in place, and note `renamed from <old ID>` in the Revisions entry. Otherwise it becomes
  `Retired <date>`.
- **Changed unit**: compute each derived unit's excerpt hash and compare with the baseline:

  ```bash
  { sed -n '<a>,<b>p' <prd.md>; sed -n '<c>,<d>p' <prd.md>; } | sed 's/[[:space:]]*$//' | shasum -a 256 | cut -c1-12
  ```

  (one `sed -n` per excerpt range, in derivation order). A different hash means changed.
- **Report without a baseline** (written before baselines existed): use the PRD history
  instead. Find the PRD commit at the run date
  (`git -C local-docs rev-list -1 --before="<run date> 23:59" HEAD -- <prd path>`), list the
  changed hunks (`git -C local-docs diff -U0 <that commit> -- <prd path>`), and mark a unit
  changed when a hunk overlaps its new excerpt range. Uncommitted PRD edits count too
  (`git diff` without a commit range includes them). If the PRD has no change since the run
  date, none of its units changed.

**Code side.** List the files changed since the recorded commits:
`git -C main/hairline-backend diff --name-only <old sha> HEAD` and the same for the frontend.
A unit is affected when any of its cited files changed. Cited files come from the baseline; for
a report without one, take the file paths from the unit's Evidence entries (gaps and conforming
pointers). A unit with no cited files (for example `Not checked`) is always re-queued.

**Deferred backlog.** Read `local-docs/deferred-backlog/README.md` to find the current version
file, then its Open table. Every open gap in the report whose Gap ID is listed as a source of an
Open DEF item is tagged `Deferred (DEF-nnn)` and is not re-raised. It is still re-checked when
its unit is re-checked, only to learn whether it was fixed.

## 3. Show the delta plan (preflight)

Ask, one AskUserQuestion per call, in this order:

1. **Delta plan**: counts of new, changed (PRD), affected (code), retired, renamed, and
   re-queued Not checked units, plus open gaps whose cited files changed and gaps to be tagged
   Deferred. Offer: run this plan; run it and also re-verify every open gap in the report
   (slower, catches fixes made in files the gap did not cite); or stop (dry run only).
2. **Engine and model** (same question as Step 3 of the main workflow).
3. **Concurrency** and 4. **Probes and staging writes**, as in the main workflow.

A dry run (the user asked for one, or chose stop) prints the plan, writes nothing, and ends.
After question 4, never block.

## 4. Re-check

Use the normal checker and verifier loop (Steps 5 and 6) for every new, changed, affected, and
re-queued unit. The checker gets no previous verdict or gap; a fresh look is the point. Then the
main agent reconciles each re-checked unit with its old gaps:

- **Same gap found again**: the new gap matches an old one when it is the same unit, the same
  requirement (same PRD section), and its evidence points to the same file. Keep the old Gap ID
  and replace the row's content with the new findings.
- **New gap**: give it the next unused number in that unit (`-G<max+1>`). Never reuse a number,
  even one whose gap was Refuted or Retired, so filed tasks never point to a different defect.
- **Old gap not found again**: spawn one verifier on the old gap as written. Refuted means the
  code now meets the requirement: set its status to `Fixed <date>` and add the verifier's
  evidence. Confirmed or Downgraded means the checker missed it: keep it open with the
  verifier's evidence.
- **Deferred gap**: keep the `Deferred (DEF-nnn)` status whatever the re-check says. If it now
  looks fixed, add `DEF-nnn: candidate to resolve (<evidence>)` to Unresolved questions. Never
  change the backlog from this skill; resolving is the `deferred-backlog` skill's job.

For a Retired unit, keep its Summary row with verdict `Retired <date> — <reason>`, set its open
gaps to `Retired <date>`, and add no new heading.

## 5. Write in place

As each unit settles: update its Summary row, its body rows (never delete a row that has a Gap
ID), its Evidence entries (new entries continue the `E-n` numbering), and its Unit baseline row
(new hash, new range, new cited files). New units get Summary rows in derivation order and body
headings where their FR sits. When the queue is empty, recount the header line
`Units planned / checked / not checked` over active (not Retired) units, append the Revisions
entry described in `output-structure.md`, and set `Run state: Complete`.

The final chat summary adds: re-checked count, fixed, retired, new gaps, still open, gaps tagged
Deferred, and any DEF items that look ready to resolve.
