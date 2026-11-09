# Checklist: FR completeness check

Version: 1.3 (2026-11-10)

## Purpose
Prove, line by line, that every requirement in one frozen FR PRD exists in the graph, and list what does not. The check is independent of the migration: the checker reads the PRD and the graph, not the migration agent's change-set or report, so a migration mistake cannot hide itself.

## Inputs
- The frozen PRD: `archived/prd-baseline-2026-11-08/frNNN-slug/prd.md` (project root; read-only; read in section ranges).
- The graph: `graph/graph.json` (current export) and `/usr/bin/python3 scripts/query.py fr FR-NNN --json` from `graph/`.
- `graph/schema.yaml` for node types.
- Do not read the migration report or `migrate-fr.md` before finishing the line table. Read the migration report afterwards only to fill the "Compared with migration report" section. Everything the check needs is in this file.
- After the line table: this FR's kind B and C rows in `plans/reports/review-queue-261109-0728-morning-queue-consolidated.md` (search the FR id in the FR column).

## Outputs
One report at the path given in the brief, in the format below.

## Steps
1. Re-read this checklist. Write the header: checklist path and version, FR id, PRD path, graph export timestamp (`changes[0].at` in graph.json) and node counts for the FR by type.
2. Walk the PRD section by section. For every line that states a requirement (does, shows, stores, allows, forbids, must, never, only, default, limit, when ... then), add one row to the line table. Group consecutive lines that state one requirement into one row with the line range.
3. For each row, find the graph node that carries it: Rule statement (search `graph.json` for the key phrase, or the REQ id), Field, enum value, Screen `shows` edge, Event, Setting, Actor `acts in`, Stage `reads`/`writes`, Step. Record the node id(s).
   Row granularity: one row per requirement, not per PRD line. On a screen, one row per field or per group of fields that share one `shows` target; a screen's Required column maps to the Entity field's `required` flag and its Validation column to a Rule, so they are checked there, not on the edge. In Key Entities, one row per entity; the note names any field or enum value the graph lacks. The Functional Requirements Summary gives one row per REQ id.
4. Status per row:
   - `landed`: a node's statement, field, enum value, edge or attribute carries the full meaning (text may be consolidated; meaning identical). Content found only in a Rule's `rationale` text is not landed.
   - `partial`: the node exists but a condition, value, message, actor, stage or enum value in the line is absent, or lives only in rationale text. Say which.
   - `missing`: no node carries it and it belongs to this FR.
   - `no node type`: the line belongs to a section the model does not store. These are: Executive Summary, Success Criteria, User Scenarios and Testing (user stories and acceptance scenarios), Glossary, Assumptions that are not rules, Implementation Notes (Technical Considerations, Integration Points, Scalability, Security mechanics), External Dependencies, Data Dependencies, Approvals, Change Log. Rules stated inside these sections are still rows with a normal status. Edge Cases, "Fixed in codebase" and "Configurable" lists are rules and settings, never no node type.
   - `cited`: the line belongs to another FR and the graph already holds it under that FR. Give the node id.
   - `unmigrated FR`: the line belongs to another FR (Internal Dependencies, handoff behaviour, another FR's notifications or payments) and that FR has no nodes yet. Name the FR. These rows are checked again when that FR migrates.
   Placement: a Rule row is `landed` only when the Rule also points at the objects the line names it acting on (`applies to` Actor, Screen, Entity, Field or Event; `applies at` Stage), or carries `scope: global` and the line states it platform-wide. A missing link is `partial` with the note "no applies to <object>". The checker may add the missing `applies to` edges in a change-set named in the report; it never adds `scope: global` itself, that goes under "Needs user decision". A line citing a Rule homed in another FR or the system PRD (`REQ-SYS-NNN`) is `cited` only when this FR has a `references` edge to it; otherwise `partial`.
   Flow steps: a numbered step of the Main Flow or a named Alternative Flow is `landed` only when a Step carries it with its `done by` Actor, `at` Stage, `on` Screen when the PRD names one, and `applies` edges to the Rules it checks, and its flow has a Flow node that reaches it through `starts at` and `next`. A missing piece is `partial` with the note naming it.
   An event the PRD fires at a stage with no `emits` edge from that stage is `partial` with the note "not emitted at <stage>"; an Event may have several emitting stages (D42).
   A line that cites a Product Owner decision code (D2, M7, Q35) is `landed` only when the Rule it states has a `decided by` edge to `SRC-PO-001-<code>`; otherwise `partial` with the note "no decided by SRC-PO-001-<code>".
   A PRD that contradicts itself (two lines, two readings): the row for each line gets `partial` with the note "contradicts line NNN; graph follows line MMM", plus one "Needs user decision" item.
5. Extra: list graph nodes owned by this FR that no PRD line supports under "Extra nodes". The count of extra nodes is reported on its own line below the row counts, because it counts nodes, not rows. An extra node is not a failure by itself, but the user must know it exists.
6. Needs user decision: list every row where the PRD contradicts itself, contradicts a source, or where the checker cannot tell landed from partial without a product judgement. Plain language, per `source-priority.md`.
7. Fix change-set (D37 review step 1): write one change-set, named in the report, that adds what the `partial` and `missing` rows need when the PRD states it plainly: Steps, `next` links, Flows, hand-off attributes and their linking edges per `migrate-fr.md` step 2 "Flow steps"; extra `emits` edges; `decided by` edges to `SRC-PO-001-<code>`; `applies to` edges. Never add `scope: global`, never change a Rule statement, and never create nodes owned by another FR. Validate it on a DB copy with `write.py --db` and run `lint.py --db <copy> --fr FR-NNN`; only L18 (open hand-offs, each listed in the report) may be new from L14 to L19. Re-mark the fixed rows as `landed`, with the note "fixed by <change-set>".
   A checker with no shell (the headless first pass, D43) cannot write or validate the file. It writes the operations instead under "## Draft fix change-set" in the report: one fenced YAML block in change-set format (`reason`, `by`, `operations`, one JSON object per operation line), and leaves the rows it would fix as `partial` with the note "fix drafted". The gate copies the block into the change-set file, corrects it, validates it, and re-marks the rows.
8. Queue rows: for each of this FR's kind B (ownership) and C (agent-created entity) rows in the review queue, write one line under "Needs user decision" or state the ruling the line table already supports (row number and node id). Do not edit the queue file.
9. Fill the counts, the pass or fail line, and the status line.

## Report format

```
# FR-NNN completeness check

Checklist: project-requirements/graph/checklists/completeness-check.md v1.3
PRD: archived/prd-baseline-2026-11-08/frNNN-slug/prd.md (N lines)
Graph: graph.json exported <timestamp>; FR-NNN owns R rules, E entities, F fields, V enum values, Ev events, S settings, Sc screens

## Line table

| PRD lines | Section | Requirement (short) | Node id(s) | Status | Note |
|---|---|---|---|---|---|
| 85-99 | Main Flow step 5 | Terms acknowledgment required before acceptance | REQ-005-035 | landed | |
| 561 | Edge Cases | Admin cancellation writes supersession record | REQ-005-042 | partial | contradicts lines 131, 374; graph follows them; see decision 1 |
| 143 | A6 | booking.provider_fault_replacement notice | none | unmigrated FR | FR-006 has no nodes yet |

## Counts

| Status | Rows |
|---|---|
| landed | |
| partial | |
| missing | |
| no node type | |
| cited | |
| unmigrated FR | |
| total rows | |

Extra graph nodes: N
Sections with no requirement lines (no row, not counted): <heading list>

## Extra nodes
- node id: why it has no PRD line

## Needs user decision
1. ...

## Fix change-set
Change-set file and validation result (gate), or the draft YAML block under "## Draft fix change-set" (no-shell first pass).

## Compared with migration report (filled last)
- Items the migration report lists as "not migrated" or "needs decision" that this check also found: ...
- Items this check found that the report does not mention: ...

Pass: yes / no (reason)
Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
Summary: ...
Concerns/Blockers: ...
```

Rows are in PRD order. The line table is the deliverable; do not shorten it to a sample.

## Pass condition
- Zero `missing` rows, or every `missing` row is also listed under "Needs user decision" with the question that blocks it.
- Zero `partial` rows without a note naming what is absent.
- Every numbered step of the Main Flow and each named Alternative Flow is `landed` on a Step, or listed under "Needs user decision".
- The fix change-set, if any, validates on a DB copy with exit 0.
- Every PRD heading appears in at least one row's Section column or in the single "Sections with no requirement lines" list under Counts.
- Status counts add up to the total rows; the extra-node count is separate.
- Header, counts, pass line and status line present.

When Phase 4 reruns the check after a follow-up change-set, the new report replaces the old one at the same path and states the previous counts in one line so the trend is visible.

## Stop and ask when
- The PRD and the graph disagree and both readings are plausible business rules.
- `missing` rows exceed 20 percent of the rows that are not `no node type`, `cited` or `unmigrated FR`: stop after the first full pass, report, and let the controller decide whether to re-migrate before continuing.
- `graph.json` is older than the latest change-set in `graph/changesets/` for this FR (export not refreshed): report NEEDS_CONTEXT, do not run the export yourself.

## Change log
- 1.0 (2026-11-08): first version. Statuses landed, partial, missing, no node type, cited, extra; pass condition zero unresolved missing.
- 1.1 (2026-11-08): after the FR-005 dry run (`plans/reports/tester-261108-fr005-completeness-dryrun.md`): no-node-type list inlined so the checker reads nothing else; row granularity defined; rationale-only content is partial; Required and Validation screen columns map to field flag and Rule; new status `unmigrated FR` removes the dependence on the migration report; extra nodes counted apart from rows; self-contradicting PRD lines handled; 20 percent rule given a denominator; no-row sections listed under Counts.
- 1.2 (2026-11-09): schema v5 (D38): a Rule row lands only with its `applies to` or `applies at` links, or `scope: global`; the checker may add missing `applies to` edges in a named change-set; `cited` requires a `references` edge; new step 7 rules on the FR's kind B and C review-queue rows (D40).
- 1.3 (2026-11-10): schema v6 (D42): flow-step rows land only on a Step with its Actor, Stage, Screen and Rules, reachable from a Flow; an event fired at a stage needs an `emits` edge from that stage; PRD lines citing a Product Owner decision code need `decided by` to `SRC-PO-001-<code>`; new step 7 writes the D37 review step 1 fix change-set (Steps, Flows, hand-offs, `emits`, `decided by`, `applies to`) and validates it on a copy. Same version, 2026-11-10 later (D43, no pass or fail change): a checker with no shell drafts the fix operations as a YAML block in the report for the gate to build; report format gains the fix change-set section; header example shows v1.3.
