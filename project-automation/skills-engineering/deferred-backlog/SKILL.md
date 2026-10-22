---
name: deferred-backlog
description: Keep the versioned record of issues the Hairline team decided not to fix now (local-docs/deferred-backlog/). Three actions — add (defer one or more gaps or bugs from any source, such as a code review report, a manual-test bug list, or a readiness backlog, with the reason, who decided, and a revisit trigger), resolve (close an item as fixed or dropped, or reopen it as a planned task), and cut (freeze the current version and start the next with open items carried forward and the delta counted). User-triggered only, never auto-fire. Use it whenever the user says "defer these gaps", "push this to the backlog", "we won't fix this now", "park FR-004/W3-G1", "mark DEF-007 resolved", "cut a new backlog version", "what is still deferred", or "show the backlog delta". Not for turning gaps into planned tasks (create-bug-tasks, create-implementation-tasks), code review itself (code-review-conformance), or Plane filing.
---

# Deferred Backlog

## Purpose

Most gaps and bugs become planned tasks. Some the team pushes back on: not the right time, too
costly for this release, or not needed yet. Those must not vanish, and they must not keep coming
back in every review as if new. This skill keeps them in one versioned register so each one can
be revisited, traced back to where it was first recorded, and closed with a reason.

## Files

- `local-docs/deferred-backlog/README.md`: points to the current version and holds the
  version table (one row per version with its counts).
- `local-docs/deferred-backlog/vNN-YYYY-MM-DD.md`: one file per version. Exactly one has
  `**State**: Current`; every other is `Frozen`. Format: see the current file; never invent new
  columns.

Read only the README and the current version file. Older versions are frozen history; open one
only when tracing an item's earlier state.

## Hard rules

- **Edit only the current version** and the README. A frozen version never changes, so its
  counts stay true.
- **DEF IDs are never reused or renumbered.** The next ID is one more than the highest DEF ID
  in any version (search the folder with `rg -o "DEF-[0-9]{3}" local-docs/deferred-backlog |
  sort -u | tail -1`).
- **Every item needs a deferral reason, who decided, and the date.** If the user did not say
  them, ask (one AskUserQuestion per call). Never write "TBD" for who decided; the point of the
  record is accountability.
- **Never resolve an item on inference.** Another skill (for example `code-review-conformance`
  Delta mode) may flag a candidate; only the user's explicit request resolves it.
- **Never edit the source documents** (code review reports, bug lists). Deferral lives here;
  Delta mode reads it.
- No literal pipe character inside a table cell; use `/`, commas, or `<br>`.

## Action: add

1. Collect the items: source document path and the source IDs (gap IDs, bug IDs, row IDs). For
   each source ID, read just its row in the source to get module/FR, severity, and a one-line
   summary. Do not read the whole source.
2. Group by root cause only when the user says to, or proposes it and the user agrees: one DEF
   item may list several source IDs.
3. Skip any source ID already listed in an Open item of the current version; tell the user which
   DEF item holds it.
4. Ask for anything missing, one question per call: deferral reason, who decided (a role or a
   name the user gives), the decision date (default today), and the revisit trigger (a phase,
   a date, a condition such as "after payments go live", or "none").
5. Append one row per item to the Open table:
   `| DEF-nnn | vNN | <source doc>: <IDs> | <module / FR> | <severity> | <summary> | <reason> | <who>, <date> | <trigger> | Open |`.
   - `vNN` (First recorded) is the current version: the one the item enters the backlog in.
     It never changes afterwards, which is what makes an item traceable to its origin.
   - The source doc is a path relative to `local-docs/`; separate several IDs with commas
     (`testing/.../report.md: FR-004/W3-G1, FR-004/W3-G2`). Items from two documents separate
     the documents with `<br>`.
   - Module / FR is written as the source gives it, for example `P-02 / FR-004`; use just the FR
     when the source names no module.
6. Update the counts. In the header's `**Delta**` line add n to `new` and to `open`; `carried`
   never changes after a cut. In the README row for the current version add n to `New`; leave
   `Frozen` and `Open at freeze` as `-` until the cut.

## Action: resolve

1. Find the DEF item in the current version's Open table. If it is not there, it is in a frozen
   version or already resolved; say so and stop.
2. Ask for the outcome if not given: `Resolved-fixed` (with the evidence: a commit, a report
   row marked Fixed, or a task ID), `Resolved-dropped` (the reason it is no longer needed), or
   `Reopened → task` (the task ID or plan it moves to).
3. Move the row from Open to the bottom of "Resolved in this version":
   `| DEF-nnn | vNN | <sources> | <summary> | <resolution and evidence> | <who>, <date> | <status> |`.
   `vNN` is the item's First recorded value, copied unchanged; sources and summary are copied
   from the Open row. Module/FR, severity, reason, and trigger are dropped here because the
   frozen version where the item was open still holds them.
4. To mark a revisit trigger as met without resolving, change the item's status in Open to
   `Revisit due` and leave it in place. Counts do not change.
5. Update the counts: in the Delta line add 1 to `resolved` and take 1 from `open` (leave
   `carried` and `new` as they are); in the README row add 1 to `Resolved`.

## Action: cut (on demand only)

Cut only when the user asks. A cut freezes the current version so later readers can see what
was deferred and resolved during that period.

1. Read the current file. Count open (rows in Open) and resolved (rows in Resolved in this
   version).
2. In the current file: set `**State**: Frozen <date>`. Recompute its Delta line from the
   tables, not from the old Delta line:
   - carried = rows in Open plus rows in Resolved whose First recorded is an earlier version;
   - new = rows in Open plus rows in Resolved whose First recorded is this version;
   - resolved = rows in Resolved; open = rows in Open.
   Check that open = carried + new - resolved, and that carried equals the previous version's
   `Open at freeze` in the README. Stop and report if either check fails.
3. Create `vMM-<today>.md` (MM = NN + 1, two digits; the date in the name is the cut date and
   is also its `**Opened**` value) with the same header field order and tables:
   `**Previous version**: vNN`, `**State**: Current`, `**Delta**: carried <open of vNN>, new 0,
   resolved 0, open <open of vNN>`. Copy every Open row unchanged (DEF ID, First recorded, and
   all fields stay as they were). The Resolved table starts empty.
4. In the README: fill the frozen version's `Frozen` (the date) and `Open at freeze` cells, add
   a row for the new version (`Opened` today, `Frozen` `-`, `Carried in` the open count, `New`
   0, `Resolved` 0, `Open at freeze` `-`), and point **Current** at the new file.
5. Report the cut: `vNN frozen: carried a, new b, resolved c, open d. vMM started with d open.`

Example: v01 records 5 items. v02 starts with 5 carried, adds 5, resolves 3, and freezes with 7
open. v03 starts with those 7, resolves 5, and freezes with 2, which carry into v04.

## Action: show

When the user asks what is deferred or what changed, answer from the current file's Delta line
and Open table (filter by module, FR, severity, or status if asked). For "where did DEF-nnn come
from", read the item's `First recorded` version and its source IDs.

## Update log

`add`, `resolve`, and `cut` change a project document, so the session that ran them appends an
update-log entry per project rules (a cut is a major update: new version file).
