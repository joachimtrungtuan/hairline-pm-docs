# Automated E2E Testing Architecture

**Date:** 2026-07-11
**Change type:** Major documentation addition
**Primary artifact:** `local-docs/testing-automation/ARCHITECTURE.md`

## Summary

Created the approved architecture for a long-term Provider/Admin web E2E testing system. The design separates a source-linked Markdown test registry, reusable Playwright framework, SQLite execution history, and filesystem evidence artifacts.

The architecture is stored in the permanent `local-docs/testing-automation/` area rather than a dated `testing-plans/` folder because it governs a living automation system. `local-docs/INDEX.md` now routes automated web E2E work to that area while retaining dated/manual QA work under `testing-plans/`.

## Key Decisions

- Normal execution is deterministic Playwright/TypeScript invoked with `pnpm`; no AI agent is required.
- Tests are classified primarily by existing Hairline module IDs, with one primary owner for cross-module flows.
- System and functional PRDs remain authoritative and are referenced rather than copied.
- Focused tests use deterministic development API calls to create synthetic prerequisites; generated data is retained and traced by run ID.
- SQLite is the canonical execution/review store; screenshots and traces remain external artifacts referenced by path.
- Each case receives one initial attempt plus three retries, separated by at least five seconds after failure.
- Every non-pass or recovered-after-retry result receives `NEEDS_HUMAN_REVIEW`; only humans may confirm bugs or approve test changes.
- Clean passes retain no screenshots/traces; consistent failures retain the final screenshot/trace; flaky cases retain failed and passing screenshots plus trace.
- Proposed `web-e2e-register` and `web-e2e-review` skills support human-approved maintenance and human-triggered investigation, but never normal execution or automated decisions.

## Scope Boundary

The initial pass added the design document and documentation log only. A follow-up approved pass created the documentation-only governance scaffold:

- `local-docs/testing-automation/TESTING-CONSTITUTION.md` as `0.1-draft` for human review;
- boundary READMEs under `registry/`, `framework/`, and `results/`;
- architecture status and next-gate alignment.

The follow-up does not create a SQLite database, schema, Playwright scripts, package configuration, registered test cases, generated artifacts, or agent skills.

## Constitution Review Adjustment

- Narrowed test requirement authority to the system PRD, functional PRDs, and relevant product plans.
- Removed the system technical specification and system data schema from the authoritative testing-source list because implementation-level technical decisions may legitimately differ.
- Clarified that live development APIs are implementation evidence and deterministic data-preparation inputs; they do not automatically override PRD-defined expected behavior.

## Constitution Approval and Contract Definitions

- Promoted `TESTING-CONSTITUTION.md` from `0.1-draft` to approved version `1.0`, while preserving evidence-driven amendments behind explicit human approval.
- Added `registry/IDENTIFIERS.md` with module-first stable IDs, revision rules, allocation, file naming, and supersession behavior.
- Added `registry/CASE-TEMPLATE.md` as the initial source-linked function/flow registry template.
- Added `results/SQLITE-SCHEMA.md` with the conceptual relational model, required indexes, serialized writes, JSON recovery envelopes, and redaction boundaries; no database was created.
- Added `framework/RUNNER-CONTRACT.md` covering pnpm commands, deterministic phases, retries, evidence, result envelopes, reporter behavior, review-queue output, failure boundaries, and the TDD implementation order; no runtime code was created.

## Development Dashboard and Playwright MCP Verification

- Recorded `https://admin.hairline.app` as the shared development dashboard origin for Provider and Admin.
- Recorded `/auth/provider/login` and `/auth/hairline-team/login` as the current login routes, confirmed against frontend routing.
- Confirmed that the Playwright MCP is callable in the current Codex session and can navigate, authenticate with the existing test-account reference, and inspect the live Provider Quotes page.
- The older local helper path could not auto-detect servers because its standalone Playwright dependency is not installed; this does not affect Playwright MCP access.

## PR-02 Pilot Proposal

- Added `local-docs/testing-automation/pilot-plans/PR-02-EDIT-SENT-QUOTE-PILOT.md` as a human-reviewable proposal, not an active registry entry.
- Proposed `PR-02-FN-001`, cases `PR-02-TC-0001` through `0003`, and datasets `PR-02-DS-0001` through `0003` for sent-quote editing, expired-state gating, and role-based edit denial.
- Recorded the live dashboard, frontend/backend implementation mapping, API-assisted prerequisite needs, runtime acceptance gates, and environment observations.
- Recorded quote withdrawal as a human-review discovery lead because the current frontend action is a placeholder and the inspected backend transition contract does not support the PRD-defined withdrawal behavior; no bug was confirmed.
- Added `pilot-plans/` to the architecture so discovery proposals remain separate from approved active registry cases.

## PR-02 Pilot Approval and First TDD Foundation

- Recorded Product Owner approval for PR-02, `PR-02-FN-001`, cases `PR-02-TC-0001` through `0003`, datasets `PR-02-DS-0001` through `0003`, and the first limited runtime foundation batch.
- Created the draft PR-02 module registry and function case collection; cases remain `DRAFT` until datasets, Playwright scripts, and targeted validation are complete.
- Added a pnpm/Node package boundary with no third-party runtime dependencies in this batch.
- Followed RED-GREEN TDD for stable ID validation, four-attempt retry/outcome behavior, mandatory review status, and evidence-retention decisions.
- Verified 9/9 unit tests passing through `pnpm test:unit`.
- Added generated-output exclusions for `node_modules`, SQLite files, recovery envelopes, Playwright reports, test results, and runtime artifacts.
- No SQLite database, API mutation, Playwright case, reporter, review queue, or agent skill was created.
