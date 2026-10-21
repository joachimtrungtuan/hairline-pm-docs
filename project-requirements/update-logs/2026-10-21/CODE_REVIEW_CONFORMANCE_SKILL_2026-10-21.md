# Code Review Conformance Skill and Code Map Refresh

**Date:** 2026-10-21
**Type:** New project skill, testing hub addition, code map refresh
**Brief:** [project-automation/plans/code-review-conformance-skill-plan.md](../../../project-automation/plans/code-review-conformance-skill-plan.md)

## Why

Manual testing cannot see defects that live in code (fixture data, missing authorization, broken state transitions, API/dashboard contract mismatches, unbuilt PRD branches, untested screens). The new skill reviews `main/` source against the FR PRDs per launch-plan phase, unattended, and produces a gaps-only report that `create-bug-tasks` can ingest.

## What Changed

### New skill (created on explicit user request under the frozen `skills-engineering/` path)

- `project-automation/skills-engineering/code-review-conformance/`: `SKILL.md`, `agents/openai.yaml`, `evals/evals.json` (prompts only, not run), and references `item-derivation.md`, `rubric.md`, `checker-brief.md`, `verifier-brief.md`, `output-structure.md`.
- Behaviour: preflight resolves plan, phase, modules and FRs; derives a frozen unit list (use cases, user stories, main and alternative flows, edge cases, uncovered provider/admin screens, phase exit gates); asks all approvals up front through AskUserQuestion (scope, frozen list, concurrency, staging writes) and never blocks afterwards; one fresh checker subagent per unit and one refuting verifier per gap; the main agent writes each result into the report as it arrives; planned and completed counts are reconciled at the end; resume mode.
- Code scope: `hairline-backend` (including patient APIs the app calls) and `hairline-frontend` (provider and admin dashboards). `hairline-app` source is excluded. Code is the source of truth; code maps are a locator only.

### Skill registration

- Symlink `.claude/skills/code-review-conformance` created (user-approved root config change) so Claude Code can invoke the skill.

### Testing hub and index

- New `testing/code-review/README.md`. Reports go to `testing/code-review/<YYYY-MM-DD>/code-review-v<plan>-<phase>-<scope>.md`.
- `INDEX.md`: new rows in §A and §A.2; `code-review/` added to the testing line in §B.
- `testing/README.md`: one row for the code review folder.

### Code maps (`gen-code-map` run)

- All three maps refreshed after the drift check (new folders: backend 3, frontend 13, app 43; none removed). Snapshots re-accepted; drift check is clean.
- Frontend map adds Affiliate Portal (A-07/FR-018), Provider Activation (FR-015), Localization runtime (FR-021) and `contractAudit` tooling groups. App map adds `head_scan` (P-07/P-05; FR-002, FR-037), library and dummy groups.
- Each map header now records the commit SHA and refresh date: backend `fd7ded98`, frontend `3e16aae6`, app `5516c18`.

### Follow-up changes (user-approved, same day)

- Bug-task handoff: `create-bug-tasks` stays unchanged. Instead, the code review report now gives each gap a "Steps to reproduce (from PRD)" column, built from the PRD flow with section references, and each FR section gets a `PRD source:` line telling the executor to re-read the cited PRD sections (`references/output-structure.md`, `references/checker-brief.md` return field `repro`, `SKILL.md` Report consumers).
- `gen-code-map`: `scripts/check-code-map-drift.sh` now exports `LC_ALL=C` so `sort` and `comm` use the same byte order under any locale. Existing snapshots re-sorted in C order; drift check passes with no drift on all three codebases.

### Probe target (resolved)

- `https://backend.hairline.app/api` is the dev/test backend (user-confirmed 2026-10-21: the project is in the dev phase, there is no production yet and no real patient data). The only Hairline Postman environment ("Hairline Testing - Travel Flow") points at it. Staging writes may be approved per run; the skill still asks at preflight and states the base URL so a future production host is caught.
