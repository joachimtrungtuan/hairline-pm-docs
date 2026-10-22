# Code Review Engine Choice, Delta and Jury Modes, and Deferred Backlog

**Date:** 2026-10-22
**Type:** Skill update and new skill plus new documentation folder (approved by the user, including edits to the frozen skill folder)

## Why

The first Phase 1 run (2026-10-21) showed four problems: subagents inherited the main session's model (Opus) and drained the usage quota; general-purpose subagents carried the full MCP tool catalog into every unit; a second run had no way to re-check only what changed; and there was no record for gaps the team decides not to fix now, so they would resurface in every review.

## What Changed

- **`code-review-conformance` skill** (`project-automation/skills-engineering/code-review-conformance/`):
  - Preflight gains an engine-and-model question: Claude `code-reviewer` on Sonnet (recommended), Haiku, or Opus; Codex headless; or OpenCode headless. Review subagents are always `code-reviewer` with the model passed explicitly, never `general-purpose`.
  - Checker and verifier briefs: no MCP, ToolSearch, or skill calls unless a finding needs that evidence; follow the brief, write no files; new probes on/off switch.
  - New `references/subagent-engines.md`: engine options, read-only and credential-blind rules for external engines, a canary before each run, and the Codex and OpenCode commands.
  - New Delta mode (`references/delta-mode.md`): re-derives units, detects PRD changes (excerpt hashes, or PRD git history for older reports) and code changes (files changed since the recorded commits), re-checks only affected units, keeps gap IDs stable, and updates the report in place. Replaces the `-r2` filename rule.
  - New Jury mode (`references/jury-mode.md`): an independent annotate-only judgment of passing units, open gaps, or both, with a juror brief; adds a `Jury` column and a `## Jury` section with disagreements; never changes original verdicts.
  - Rubric adds `Fixed`, `Retired`, `Deferred (DEF-nnn)` and jury outcomes. Output structure adds the Engine and Revisions header lines and a Unit baseline section.
  - Three new evals (engine question, Delta dry run, Jury).
- **New `deferred-backlog` skill** (`project-automation/skills-engineering/deferred-backlog/`): add, resolve, and cut actions for the versioned register, with evals.
- **New folder `deferred-backlog/`**: `README.md` and the first version `v01-2026-10-22.md` (empty).
- **INDEX.md**: task rows, skill directory rows, and folder map entry. **testing/code-review/README.md**: statuses, deferral, one report per scope with in-place Delta updates, and report sections.

## Verification

- Delta dry run on `testing/code-review/2026-10-21/code-review-v2-phase-1-all.md`: both repos at the recorded commits with clean working trees, no PRD change since 2026-10-21, no Not checked units, and an empty backlog, so 0 units would be re-checked and no verdict changes.
- Backlog cut test (scratch copy, not the live folder): add 5 items to v01, cut, add 5, resolve DEF-001 to DEF-003, cut again. v01 froze at "carried 0, new 5, resolved 0, open 5"; v02 froze at "carried 5, new 5, resolved 3, open 7"; v03 is Current with the 7 open rows copied unchanged; the README table and Current pointer were correct; no DEF ID was reused. The tester reported nine places where the skill left it guessing (First recorded meaning, multi-ID separator, Module / FR format, which README cells change on add, resolve and cut, where resolved rows go, and how carried is counted). `deferred-backlog/SKILL.md` now states each of these, and a cut recomputes the Delta from the tables and cross-checks carried against the previous version's open count.
- Skill links (user approved twice): `deferred-backlog` linked in `.claude/skills`, `.agents/skills` and `.opencode/skills`; `code-review-conformance`, previously linked only in `.claude/skills`, now also linked in `.agents/skills` and `.opencode/skills`. Each link resolves to its `SKILL.md`.
