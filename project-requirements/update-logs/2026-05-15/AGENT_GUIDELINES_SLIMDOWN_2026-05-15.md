# Agent Guidelines Slimdown — 2026-05-15

## Summary

Slimmed `CLAUDE.md` and `AGENTS.md` from 284 and 277 lines to **101 lines each** by removing redundant content and consolidating scattered file/folder governance into a single permission table. Each agent loads only its own file (`CLAUDE.md` for Claude Code, `AGENTS.md` for Codex), so per-turn context for agent guidelines now sits well under the ~200-line target.

## Motivation

Both guideline files were significantly over the ~200-line guidance promoted by official Claude and Codex documentation. Re-reading the files in context of recent project activity (FR verification, task creation, Plane sync, progress checks) surfaced sections that no longer carried unique signal — either they duplicated each other, restated generic agent hygiene already covered by platform behavior, or described one-time setup steps that are now stable.

## Changes Applied

### Sections deleted

1. **Skill Definitions and Locations table** — pure path map; paths follow a predictable pattern (`skills-engineering/<name>/SKILL.md`, `commands/<name>.md`, `workflows/<name>.md`) that any agent can derive on demand.
2. **Deployment Instructions** — one-time setup commands for Cursor / Antigravity / Codex skill deployment. All agents now share the same skill structure, so this is no longer a recurring need.
3. **General Skills tables** (Requirements, Planning, Execution, Documentation, Architecture, Code Quality, Deployment — 6 tables totalling ~64 lines) — agents auto-discover platform-provided skills via their own frontmatter `description:` fields, and the user can invoke any skill manually via `/skill-name`. A curated catalog only creates drift risk between this file and the skills' source-of-truth descriptions.
4. **Skill Enforcement Rules section** (8 numbered rules) — six of eight rules described generic agent hygiene (chain skills, no silent skips, no partial execution, progress tracking, etc.) that every modern agent already does. Rules 2 (general-skills mandate) and 8 (Context7 for libraries) were orphaned once the General Skills tables were removed and given that this project is document-focused rather than code-focused. The two genuinely project-specific rules — BLOCKING status for the 4 project skills, and "read `SKILL.md` end-to-end before running" — were folded into the existing "When to Invoke (STRICT)" block as two trailing lines, keeping the signal without the surrounding boilerplate.

### Sections consolidated

The same topic — what each folder is, who can edit it, and what loading discipline applies — was previously spread across six sections:

- Hard Boundaries
- Context Budget → Off-Limits Folders table
- Source Code Restraint for `main/`
- Smart File Selection
- "When a request requires non-`local-docs/` changes"
- File Structure (READ-ONLY / EDITABLE labels in directory tree)

These have been merged into a single **`## File & Folder Rules`** section with one permission table (path → permission → notes), followed by short loading-discipline and escalation lines. The File Structure section is retained but now contains only the `local-docs/` directory tree — the genuinely useful navigation map for the work area. Root-level config dirs, `main/` internals, and archive/backup listings are now covered by the permission table rather than re-described in tree form.

### Kept as-is (high signal, project-specific)

- Primary Focus
- Project-Specific Skills "When to Invoke (STRICT)" table (4 BLOCKING skills with trigger patterns)
- Update Log Protocol (Major / Minor distinction, README maintenance steps)
- Working Conventions
- `local-docs/` directory tree

## Result

| File | Before | After |
|---|---|---|
| `CLAUDE.md` | 284 lines | 101 lines |
| `AGENTS.md` | 277 lines | 101 lines |

Both files now mirror each other exactly except for the document title (`# Hairline Project Guidelines` vs `# Codex Guiding Principles (Hairline)`) and minor tool-name wording differences (`Grep/Glob` vs `search/grep`), which match each agent's native vocabulary.

## Files Modified

- `CLAUDE.md` (root)
- `AGENTS.md` (root)

## Files Created

- `local-docs/project-requirements/update-logs/2026-05-15/AGENT_GUIDELINES_SLIMDOWN_2026-05-15.md` (this report)

## Follow-up Adjustments

- Strengthened the last three rows of the **File & Folder Rules** table in both `CLAUDE.md` and `AGENTS.md` from soft "Read only" / "Do not load" language to explicit **NEVER EDIT** status, with `main/` clarified as the dev team's source code — used **only** as reference to clarify system logic, never edited by agents working in this repo. Added a new explanatory paragraph below the table requiring **two-step approval** (initial request + confirmation prompt naming the exact file) before any edit may be applied to those paths.
- Added a **Reading `main/`** subsection clarifying the three read-access tiers: (1) **free read** when the user explicitly says to go into the source code / frontend / backend to analyze something — agents may browse `main/hairline-app/`, `main/hairline-backend/`, `main/hairline-frontend/` freely in that case; (2) **targeted read** when a specific file/module/function is named or when `check-progress` requires it; (3) **default** — no speculative reads, prefer `local-docs/` doc summaries.
- Replaced the stale 4-skill BLOCKING enumeration with a category rule. The previous "When to Invoke (STRICT)" table only listed `verify-fr`, `create-implementation-tasks`, `check-progress`, and `plane-api-commands` — but the `skills-engineering/` folder now contains 11 skills (also includes `android-emulator-qa`, `android-flow-register`, `android-flow-test`, `api-flow-register`, `api-flow-testing`, `api-testing`, `verify-design-layout`). The new rule reads: *"All skills under `local-docs/project-automation/skills-engineering/` are BLOCKING — when a user request matches a skill's frontmatter triggers, load the SKILL.md and follow the workflow step-by-step."* This auto-scales as new skills are added and eliminates the drift risk between the enumeration and the actual skills folder.
