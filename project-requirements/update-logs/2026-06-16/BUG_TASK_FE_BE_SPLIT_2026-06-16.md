# Bug Task FE/BE Split & Side-Labeled Task Status

**Date:** 2026-06-16  
**Report Type:** Project Automation Skill Update  
**Primary Documents Changed:**
- `local-docs/project-automation/skills-engineering/create-bug-tasks/` (SKILL.md, references/plane-and-backlog-rules.md, references/bug-task-format.md)
- `local-docs/project-automation/skills-engineering/sprint-readiness-reporting/` (references/reporting-rules.md, assets/sprint-readiness-fix-backlog-template.md)

## Summary

Updated the bug-tasking workflow so a single bug that spans both frontend and backend is no longer created as one combined task. Such bugs are now split into two cleanly separated tasks — one FE, one BE — because different people own each side of the system and a combined task blurs the boundary. To keep the sprint readiness backlog traceable to these split tasks, the `Task Status` column now stores **one or more side-labeled Plane keys** instead of a single key.

## What Changed

### `create-bug-tasks` skill

- **No combined FE + BE task.** Added a guardrail and a new workflow step (Step 5 — *Classify Side And Split*): each bug is classified FE-only, BE-only, or Both; Both bugs are split into one `[BUG][FE]` and one `[BUG][BE]` task. Subsequent workflow steps and the progress checklist were renumbered.
- **Task naming** now requires a side prefix: `[BUG][FE]` / `[BUG][BE]` (`[BUG]` alone only when the side is untriageable). A split pair shares the same module/FR/title and differs only by prefix.
- **Label Selection** rewritten in `plane-and-backlog-rules.md`: allowed sets are now only `Bugs, FE Task` or `Bugs, BE Task` (or `Bugs` alone if untriageable). The previous `Bugs, FE Task, BE Task` combination was removed and is explicitly forbidden.
- **Description schema** (`bug-task-format.md`): added a `Scope Boundary` section for split tasks only, with three fields — *This task covers* (FE/BE side), *Counterpart task* (sibling task name, cross-linked because Plane keys are unknown at draft time), and *Contract/handoff* (the shared API/data contract both sides depend on, in behavioral terms). Split tasks restate `Current Status`, `Steps to Reproduce`, `Evidence`, and `Notes` faithfully from the source; each task's `Expectation` covers only its own side.
- **Backlog write-back** now records side-labeled key(s) in the one `Task Status` cell, keeping a single backlog row per source bug.

### `sprint-readiness-reporting` skill

- **`Task Status` vocabulary** updated in `reporting-rules.md` and the bundled backlog template. The `Task created (...)` value is now side-labeled:
  - One side: `Task created (FE: HAIRL-123)` or `Task created (BE: HAIRL-123)`
  - Split bug (both sides): `Task created (FE: HAIRL-123; BE: HAIRL-124)` — FE first, then BE, `; `-separated, both keys in the same cell.
- Added the rule that a split bug stays in `Task created (...)` until both keys are present and resolves only when every listed task resolves. The "one row, both keys, no extra columns" constraint is preserved.

## Rationale

FE and BE work for the same bug is owned by different people. Cramming both into one task made the ownership boundary unclear. Splitting into two side-scoped tasks — each drawn faithfully from the same source bug report plus a `Scope Boundary` note and side-specific expectations — gives each owner a clean, self-contained task, while the side-labeled `Task Status` keeps the readiness backlog traceable to both.

## Notes

- Both edited skills live under `skills-engineering/` (FROZEN); changes were made under explicit user request for these specific files.
- Follow-up backlog write-back: updated the PR-06 `Recorded only` rows in `local-docs/product-plans/2026-05-29/sprint-1-readiness-fix-backlog.md` with side-labeled Plane task keys `HAIRL-1339` through `HAIRL-1353`.
