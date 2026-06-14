# Create Bug Tasks Skill

**Date:** 2026-06-12  
**Report Type:** Project Automation Skill Creation  
**Primary Document Added:** `local-docs/project-automation/skills-engineering/create-bug-tasks/SKILL.md`

## Summary

Created a project-local `create-bug-tasks` skill for converting confirmed bug reports and sprint readiness backlog rows into Plane-ready `[BUG]` implementation task artifacts.

## What Changed

- Added `local-docs/project-automation/skills-engineering/create-bug-tasks/`.
- Added a self-contained `SKILL.md` covering:
  - General bug task creation from bug reports or pasted bug input.
  - `Recorded only` mode for sprint readiness backlog rows.
  - Required task naming traceability with module/FR codes.
  - PRD/document/design reference lookup and placement near the top of the task description.
  - Explicit label, priority, Plane module, cycle, parent, and backlog status rules.
  - Plane dry-run/live creation and optional source backlog update workflow.
- Added self-contained references:
  - `references/bug-task-format.md`
  - `references/source-row-mapping.md`
  - `references/plane-and-backlog-rules.md`
- Added `agents/openai.yaml` metadata for the skill.

## Validation

- Ran `quick_validate.py` against `local-docs/project-automation/skills-engineering/create-bug-tasks`.
- Result: `Skill is valid!`
