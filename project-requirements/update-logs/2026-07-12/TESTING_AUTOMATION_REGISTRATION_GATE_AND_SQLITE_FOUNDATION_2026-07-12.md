# Testing Automation Registration Gate and SQLite Foundation

**Date:** 2026-07-12
**Change type:** Major testing-automation governance and implementation update
**Primary area:** `local-docs/testing-automation/`

## Summary

Added a mandatory low-token registration gate and completed the second RED-GREEN runtime foundation batch.

## Registration Workflow Amendment

- Promoted the testing constitution from v1.0 to approved v1.1.
- New registration begins with a narrow PRD scout limited to module scope and overall business workflows.
- The agent must return a concise flow outline and stop for Product Owner corrections, operational input, and approval.
- Detailed screens, UI/API implementation, datasets, roles, edge cases, and case generation are prohibited before that approval.
- Aligned the registry README, case checklist, and future `web-e2e-register` responsibility in the architecture.

## Runtime Foundation

- Added versioned result-envelope validation.
- Added recursive secret redaction and stable payload checksums.
- Selected Node's built-in `node:sqlite` for the pilot's single canonical writer.
- Added initial internal migrations for runs, case executions, attempts, and review events.
- Added atomic execution writes and idempotent duplicate replay detection.
- Added automatic `NEEDS_HUMAN_REVIEW` event creation, review-queue queries, run summaries, and terminal summary formatting.

## Verification

- RED: the two new suites failed because `envelope.ts` and `result-store.ts` did not exist.
- GREEN: `pnpm test:unit` completed with 15 passed, 0 failed.
- SQLite integration tests used temporary databases and removed them after execution.
- No canonical result database, Playwright case, API mutation, screenshot, trace, or agent skill was created.

## Next Gate

Implement and prove the first PR-02 vertical slice: deterministic API data preparation, Playwright configuration and specs, canonical result persistence, and controlled pass/failure/flaky runs.

## PR-02 Runtime Implementation Continuation

- Reused the existing global `@playwright/mcp` package and installed system Chrome; no Playwright package or browser was installed in the project.
- Removed automation references to `main/`; runtime and documentation now depend only on live PRDs, development UI/API behavior, and `local-docs/testing-automation/`.
- Added secure V1/P1/S1 credential lookup from the existing testing-credential registry with optional environment overrides.
- Added the PR-02 API dataset builder, three browser case implementations, four-attempt runner with five-second waits, rolling screenshot manager, preflight command, and read-only review-queue command.
- Added `OPERATIONS.md` and environment-variable template with no secret values.
- Expanded TDD coverage from 15 to 21 passing tests.
- Created the canonical SQLite database through controlled execution `RUN-20260712T141310Z-f4cdd553`.
- The controlled case was correctly recorded as `BLOCKED / NEEDS_HUMAN_REVIEW` because `HAIRLINE_DURATION_OF_CONCERN_ID` is not yet registered; no browser screenshot was created.
- PR-02 cases remain `DRAFT` until live reference IDs, editable-field choice, restricted-role behavior, and browser proofs receive human confirmation.

## Agent Skills

- Added user-triggered `web-e2e-register` as the governed workflow for low-token PRD scouting, Product Owner approval gates, detailed live UI/API discovery, test registration, revisions, activation, and approved frontend changes.
- Added user-triggered `web-e2e-review` for SQLite review-queue evidence packets, mandatory human classification, append-only decisions, and approved re-test coordination.
- Both skills prohibit `main/` access/dependencies and project-local Playwright/browser installation.
- Added both skills to `local-docs/INDEX.md` §A.2 and linked their single frozen source into the project-root agent skill directories.

## MVP Setup Completion

- Added SQLite persistence for execution datasets and artifact metadata.
- Added Playwright trace retention for potential issues and flaky recoveries while preserving the approved screenshot policy.
- Added the explicit `pnpm test:review` command for append-only human classification and re-test marking without changing the automated outcome.
- Raised framework coverage to 23 unit tests.
- Declared module/flow/regression selectors and advanced PRD section hashing incremental additions rather than initial setup blockers.
- Final controlled run `RUN-20260712T143749Z-70b0b141` persisted `PR-02-DS-0001 / failed` beside `BLOCKED / NEEDS_HUMAN_REVIEW`, returned non-zero, and retained zero browser artifacts because setup stopped before browser execution.

## Clean Registration Reset

- Removed the PR-02 pilot proposal, draft module/function registry, API dataset code, browser case code, controlled SQLite database, and empty product registry directories.
- Replaced the hardcoded PR-02 runner import with generic registered automation-module loading.
- Reset the product case registry to an empty list and changed unit fixtures to clearly synthetic `P-99` identifiers.
- Removed PR-02-specific environment placeholders and refreshed current-status documentation.
- Preserved the reusable framework, templates, contracts, skills, and 23 unit tests so the first `web-e2e-register` run starts cleanly without rebuilding the setup.
