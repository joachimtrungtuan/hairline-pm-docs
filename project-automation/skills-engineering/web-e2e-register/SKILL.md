---
name: web-e2e-register
description: Use when the user explicitly asks to register, revise, activate, or reconcile Hairline dashboard Playwright test cases, datasets, function tests, module flows, selectors, or approved frontend changes.
---

# Web E2E Register

Register deterministic Hairline web tests while preserving Product Owner authority and minimizing discovery tokens.

## Required Boundaries

1. Start at `local-docs/INDEX.md`; locate before reading and read only targeted sections.
2. Read `local-docs/testing-automation/TESTING-CONSTITUTION.md` and `OPERATIONS.md` before any registration action.
3. Never read, import, edit, or depend on `main/`.
4. Never install Playwright or browsers. Reuse the global Playwright MCP runtime and installed browser defined by the testing framework.
5. Reference live PRDs; never copy their requirements into the registry.
6. Never activate, rewrite, or supersede a case without explicit human approval.

## Phase 1: PRD Flow Scout — Mandatory Stop

For a new function or flow:

1. Locate the owning module and PRD through `INDEX.md`.
2. Read only `Module Scope`, `Business Workflows`, and the smallest relevant requirement summary.
3. Return a concise outline containing actors, entry point, happy-path stages, major alternatives, and apparent module boundaries.
4. Ask the Product Owner to correct the real operational flow and approve detailed discovery.
5. Stop. Do not inspect screens, selectors, APIs, credentials, datasets, or edge cases before approval.

For an existing registered case, first summarize the requested revision and current registry status, then obtain approval before detailed rediscovery.

## Phase 2: Detailed Discovery

Proceed only after Phase 1 approval.

1. Read the specific PRD requirements and screen sections needed for the approved scope.
2. Inspect the development dashboard through the existing global Playwright runtime.
3. Observe live API requests where needed to prepare prerequisites or verify persistence.
4. Resolve accounts from `local-docs/testing-plans/testing-credentials/`; never print or copy secrets.
5. Record discrepancies as observations requiring human review. Do not decide whether the PRD, UI, API, or test is wrong.
6. Propose function/flow boundaries, case categories, dataset recipes, minimal UI actions, assertions, and regression tiers.
7. Stop for Product Owner approval of the proposed cases and realistic flow.

## Phase 3: Registration

After case approval:

1. Write under `local-docs/testing-automation/registry/<surface>/<module>/` using existing identifiers and templates.
2. Store Markdown flow/traceability, dataset TypeScript, and Playwright case code together under the owning function or flow.
3. Use API calls only for prerequisites. The browser must perform the action claimed by the case.
4. Generate retained synthetic data with run/correlation markers. Never use real patient data.
5. Keep cases `DRAFT` until live reference IDs, roles, selectors, assertions, and controlled execution are human-confirmed.
6. Run `pnpm test:unit`, `pnpm test:preflight`, then the narrowest controlled case with `--allow-draft` when authorized.
7. Do not install dependencies when validation fails; report the preflight blocker.
8. Present evidence and request explicit activation approval. Only then change status to `ACTIVE`.

## Frontend or Requirement Changes

A failed or non-running test never edits the registry automatically. Route it to human review. After a human confirms an intentional change, create a new case revision, update selectors/actions and last-confirmed dates, preserve prior results, then run affected regression tests.

## Completion

Update the testing registry documentation and required `local-docs/project-requirements/update-logs/` entry. Report changed files, registry status, validation results, unresolved human decisions, and the exact command for the next run.

## Stop Conditions

Stop and ask for direction when approval is missing, product intent is ambiguous, required synthetic-data authority is absent, a credential role is unconfirmed, or the work would touch `main/` or install Playwright.
