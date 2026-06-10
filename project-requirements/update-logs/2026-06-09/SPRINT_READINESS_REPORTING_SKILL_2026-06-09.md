# Sprint Readiness Reporting Skill

- Date: 2026-06-09
- Scope: `local-docs/project-automation/skills-engineering/sprint-readiness-reporting/`

## Summary

Created a new `sprint-readiness-reporting` skill to standardize Hairline sprint readiness-report work. The skill now covers context resolution for the active readiness-report file and launch-plan file, scaffold creation from a bundled readiness-backlog template, basic vs advanced update routing, evidence and status rules, and blocked-follow-up handling for re-test after earlier blockers are fixed.

## Files Added

- `local-docs/project-automation/skills-engineering/sprint-readiness-reporting/SKILL.md`
- `local-docs/project-automation/skills-engineering/sprint-readiness-reporting/agents/openai.yaml`
- `local-docs/project-automation/skills-engineering/sprint-readiness-reporting/assets/sprint-readiness-fix-backlog-template.md`
- `local-docs/project-automation/skills-engineering/sprint-readiness-reporting/references/context-resolution.md`
- `local-docs/project-automation/skills-engineering/sprint-readiness-reporting/references/flow-basic-vs-advanced.md`
- `local-docs/project-automation/skills-engineering/sprint-readiness-reporting/references/reporting-rules.md`
- `local-docs/project-automation/skills-engineering/sprint-readiness-reporting/references/blocked-follow-up.md`

## Notes

- The skill keeps the reusable backlog template inside `assets/` so new sprint reports can be scaffolded without re-reading the live template file every time.
- The skill explicitly preserves the existing readiness-report conventions around `Review pending`, `Recorded only`, `Task created (HAIRL-xxx)`, persistent evidence URLs, and blocked follow-up checkpoints.
