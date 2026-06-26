# sprint-readiness-reporting — Token-Governance Alignment

**Date**: 2026-06-26
**Type**: FROZEN skill edit (token-optimization initiative)
**Scope**: `skills-engineering/sprint-readiness-reporting/SKILL.md` + `references/reporting-rules.md`

## Why

Audited the skill against the project's token principles. It was already well-behaved
(on-demand references, section-scoped reads, smallest-surface evidence, Flow 2/Flow 3 effort
tiering). Three gaps remained — all about not yet using the new navigation infrastructure, plus
an observed behavior where the agent read `update-logs/` while updating a backlog.

## Changes (with explicit user approval to edit the frozen skill)

1. **Source-code lookup → code maps (Flow 3 step 4).** Now instructs locating files via the code
   maps (`INDEX.md` §D → `code-map-{backend,frontend,app}.md`) before opening anything — "the maps
   are a locator, not evidence" — then confirming the finding in the named source. Prevents broad
   `main/` searching.
2. **PRD lookup → section maps (Flow 3 step 3).** Now points to `INDEX.md` §C section maps to jump
   to the exact PRD section instead of scanning the file.
3. **Update-log interaction is write-only (mitigation).** The agent was reading `update-logs/` for
   context when updating the backlog — unnecessary. Both the SKILL.md Hard Rule and
   `reporting-rules.md` "Update Log Rules" now state: do not read past update-log entries for
   context (the live report + launch plan are the source of truth); to find the same-day log, `ls`
   the date folder — never open/grep other entries or scan the folder for history. Aligns with the
   `CLAUDE.md` history-restraint rule.

## Note

Verdict on the broader audit: this skill was not a token offender. The audit of the remaining
skills under `skills-engineering/` was scoped by the user to this one only.
