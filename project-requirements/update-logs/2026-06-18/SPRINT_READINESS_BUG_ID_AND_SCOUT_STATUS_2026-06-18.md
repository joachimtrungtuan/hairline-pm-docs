# Sprint Readiness Bug ID & Scout Status

**Date:** 2026-06-18  
**Report Type:** Project Automation Workflow Update  
**Primary Documents Changed:**
- `local-docs/product-plans/template/sprint-readiness-fix-backlog-template.md`
- `local-docs/product-plans/2026-05-29/sprint-1-readiness-fix-backlog.md`
- `local-docs/product-plans/2026-06-05/sprint-2-readiness-fix-backlog.md`
- `local-docs/product-plans/2026-06-12/sprint-3-readiness-fix-backlog.md`
- `local-docs/product-plans/2026-06-19/sprint-4-readiness-fix-backlog.md`
- `local-docs/product-plans/2026-06-22/sprint-5-readiness-fix-backlog.md`
- `local-docs/project-automation/skills-engineering/sprint-readiness-reporting/`
- `local-docs/project-automation/skills-engineering/create-bug-tasks/`

## Summary

Updated the sprint readiness workflow to add stable source-row traceback for confirmed bugs and a new scouting status for prioritizing manual testing. `Bug ID` is now the first column in sprint-level and module-level readiness backlog tables, but IDs are assigned only to confirmed bug rows from `Recorded only` onward. A new `Scout flagged` task status captures PRD/code/API evidence that should be manually tested first without prematurely treating the row as a confirmed product bug.

## What Changed

- Added `Bug ID` as the first column in the sprint readiness backlog template and the five existing sprint readiness reports.
- Assigned stable IDs to the 50 currently confirmed Sprint 1 bug rows. Existing evidence-gap and placeholder rows in Sprint 1-5 remain blank because their status is `Review pending`.
- Added `Scout flagged` to the approved `Task Status` vocabulary for rows where scouting found a concrete risk signal but manual product testing has not confirmed a bug yet.
- Added explicit `Bug ID` rules: format `MODULE_CODE-###`, leave blank for `Review pending` and `Scout flagged`, and never renumber or reuse assigned IDs.
- Updated `create-bug-tasks` so generated bug task artifacts preserve source traceback using `Source Bug ID` in the metadata block and task description.

## Rationale

Issue titles were too weak as the only connection between sprint readiness rows, generated bug task artifacts, and Plane issues. Stable `Bug ID` values provide a durable source key after rows are reordered, split, resolved, or converted to Plane tasks. `Scout flagged` supports the new test strategy: scout feature-level PRD/code/API evidence first, prioritize risky areas for manual testing, and only assign a bug ID when the product review confirms the defect.

## Notes

- Skill files under `skills-engineering/` were edited under explicit user approval for this workflow change.
- The current ID assignment intentionally affects only confirmed Sprint 1 bug rows. Sprint 2-5 remain unassigned because their current rows are evidence gaps with `Review pending` status.
- The Sprint 1 backlog was then annotated using the new `Scout flagged` status for provider-first risk scouting, including cross-tenant questionnaire source-of-truth risk, deposit-state synchronization risk, media-access-control risk, Admin patient-oversight mock surfaces, and Provider team reassignment risk.
