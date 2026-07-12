---
name: web-e2e-review
description: Use when the user explicitly asks to inspect, triage, classify, reconcile, or re-test Hairline web E2E results, blockers, flaky executions, potential issues, screenshots, SQLite review queues, or frontend/test discrepancies.
---

# Web E2E Review

Turn deterministic execution evidence into a human-controlled decision without allowing the agent or runner to declare product truth.

## Required Boundaries

1. Start at `local-docs/INDEX.md` and read `local-docs/testing-automation/TESTING-CONSTITUTION.md` plus `OPERATIONS.md`.
2. Never read, import, edit, or depend on `main/`.
3. Never install Playwright or browsers.
4. Treat every non-pass as unresolved until a human classifies it.
5. Never change a case, review status, bug record, or product document merely because an automated result suggests it.
6. Preserve all result rows and retained artifacts; review events are append-only.

## Phase 1: Select Evidence

1. Run `pnpm test:review-queue` from `local-docs/testing-automation/` or query the canonical SQLite database read-only with narrow filters.
2. Confirm the execution ID, run ID, case ID/revision, module/function, outcome, review status, and attempt count.
3. Inspect only artifacts referenced by that execution. Do not browse unrelated result folders.
4. Retrieve the registered case and its live PRD references without copying the PRD text.

## Phase 2: Evidence Summary

Present a concise human-review packet:

- expected registered behavior;
- dataset/setup status and retained record IDs;
- attempt timeline and whether signatures were consistent;
- final observed browser state;
- console/network observations when recorded;
- screenshot/trace links;
- source-hash or UI-discrepancy observations;
- affected function, module, and regression scope;
- missing evidence or limitations.

Use neutral language such as “potential issue,” “setup blocker,” or “registered-case discrepancy.” Do not call it a confirmed bug or confirmed test defect.

## Phase 3: Mandatory Human Decision

Ask the human to choose or supply the classification. Suggested options may include:

- confirmed product bug;
- intentional frontend/API change requiring registry revision;
- test implementation defect;
- test-data or environment blocker;
- flaky/transient behavior requiring monitoring or re-test;
- duplicate of an existing reviewed item;
- insufficient evidence.

Do not infer the selection from silence. Do not let AI confidence, repeated failures, or a matching PRD replace human approval.

## Phase 4: Apply the Approved Decision

Only after explicit classification:

1. Append a review event with previous/new status, human classification, reviewer, notes, timestamp, and re-test requirement.
2. Preserve the preliminary automated outcome; never overwrite execution history.
3. If the human confirms an intentional UI/API change, stop and ask them to invoke `web-e2e-register` for a new case revision.
4. If the human confirms a product bug and requests a bug task, use `create-bug-tasks` as a separate explicitly invoked workflow, preserving the source case/execution IDs.
5. If a fix or blocker resolution is ready, run only the approved affected test scope first, then broader regression tiers as directed.
6. Link re-test executions and report whether human review is still pending. Never auto-close the issue from a passing re-test.

## Evidence Rules

- Clean initial pass: no screenshot or trace.
- Four failed attempts: inspect only the final rolling screenshot and relevant trace.
- Flaky recovery: inspect both the latest failed screenshot and passing screenshot plus trace.
- Setup blocker: expect no UI screenshot because browser execution did not begin.
- Missing required evidence is itself review information, not permission to guess.

## Completion

Report the human classification, appended review event, linked bug/test revision/re-test IDs, remaining pending-review count, and exact next command. Update the required `local-docs/project-requirements/update-logs/` entry for significant documentation changes.

## Stop Conditions

Stop when no human classification is available, evidence belongs to another case, credentials or sensitive patient data appear, a requested action would alter `main/`, or the requested decision exceeds the reviewer’s stated authority.
