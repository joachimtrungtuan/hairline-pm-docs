# Review checklists

Version: 1.5 (2026-11-10)

Every repeated review or migration task in the requirements graph programme runs from a checklist file in this folder. The checklists exist so that quality does not depend on what is still in a conversation: an agent that has lost its context after compaction or a handoff re-reads the file and continues with the same rules.

## Files

| File | Used for | Used by phase |
|---|---|---|
| `migrate-fr.md` | Line-by-line migration of one frozen FR PRD into the graph as a change-set | 4 (and 3 for the dedup step) |
| `completeness-check.md` | Per-FR report that proves every PRD line landed in the graph | 4, 7 |
| `source-priority.md` | Which source wins when sources disagree, and how to write up an unclear point | 4, 8 |
| `prd-audit.md` | Per-section content-class audit of a PRD (input to `prd-structure.md`) | 6 |
| `prd-structure.md` | What a compressed PRD keeps, how compression is done, and its three pass checks; also the flow alignment check | 6 (criteria), 8 (flow alignment), 9 (compression) |
| `agent-brief-template.md` | The brief every subagent receives: task, files, checklist, report path, status line | every phase that delegates |

## Rules for using a checklist

1. **Point, do not paste.** A subagent prompt names the checklist by path and version (`checklists/migrate-fr.md v1.0`). The prompt body never restates the checklist; a shortened copy in a prompt drifts from the file and defeats the purpose.
2. **Re-read at every batch start.** Before each FR, batch, or after any compaction, the agent re-reads the checklist it is following, in full. The files are short on purpose.
3. **Report cites the checklist.** Every report opens with the checklist path and version it followed. A report without that line is incomplete.
4. **Pass condition is in the file.** An agent does not decide for itself when a task is done; it checks the "Pass condition" section of the checklist.
5. **Stop and ask when the file says so.** Each checklist has a "Stop and ask when" section. Hitting one of those conditions means writing the question into the report in plain language and ending with `Status: NEEDS_CONTEXT` or `DONE_WITH_CONCERNS`, not guessing.

## Versioning

- Each checklist carries `Version: X.Y (date)` under its title and a `## Change log` section at the end.
- A change that alters what counts as pass or fail, adds or removes a step, or changes a mapping rule bumps the minor version (1.0 to 1.1) and adds a change-log line. Wording fixes do not bump the version.
- Reports name the version they ran against, so a finding can be traced to the rules in force at the time.
- Checklist edits are significant document changes: add a bullet to the day's update log (`project-requirements/update-logs/`).

## Standing rules these checklists implement

From `plans/261108-1040-requirements-graph-programme/plan.md`: the DB is the only data store; never drop a business requirement; boundaries are recorded as they are during migration; source priority follows D29 (see `source-priority.md`); only the user decides overrides and clarifications. Decisions live in `plans/reports/advise-261105-0843-graph-model-decisions.md` (D1 to D35).

## Change log

- 1.0 (2026-11-08): first version of the set (Phase 1 of the programme).
- 1.1 (2026-11-08): `completeness-check.md` and `agent-brief-template.md` to 1.1 after the FR-005 dry run; `migrate-fr.md` and `source-priority.md` stay at 1.0.
- 1.2 (2026-11-09): `migrate-fr.md` to 1.1 (CRs no longer read during migration; PRD is the only source).
- 1.3 (2026-11-09): `prd-audit.md` and `prd-structure.md` listed; `prd-structure.md` approved at 1.0 (compressed PRD model, D35).
- 1.4 (2026-11-09): `migrate-fr.md` and `completeness-check.md` to 1.2 for schema v5 (D38): `applies to` links, `scope: global`, `references`, system PRD home FR-SYS.
- 1.5 (2026-11-10): `migrate-fr.md` and `completeness-check.md` to 1.3 for schema v6 (D42): flow Steps, Flows and hand-offs; several emitting stages per Event; Product Owner decision Sources; the completeness check writes the D37 review step 1 fix change-set.
