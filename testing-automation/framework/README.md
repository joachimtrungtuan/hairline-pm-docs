# Testing Framework

**Status:** MVP framework complete; Provider login active; Team directory and invitation-management suite draft; interactive registry console available
**Governing document:** `local-docs/testing-automation/TESTING-CONSTITUTION.md`

This folder will contain reusable deterministic Playwright infrastructure such as API clients, authentication helpers, data builders, fixtures, reusable page interactions, reporters, and runtime configuration.

It must not contain copied requirements or module-specific business rules merely for convenience. A helper begins within its owning module and moves here only after genuine cross-module reuse is demonstrated.

The framework reuses the globally installed `@playwright/mcp` package and system Chrome. It never installs Playwright and has no dependency on `main/`. It provides credential-registry resolution, API support, dynamic registered-case loading, an interactive registry console, four-attempt retry orchestration, rolling screenshots/traces, canonical SQLite writes, and a human review queue.

Contract:

- `RUNNER-CONTRACT.md` — deterministic command, lifecycle, envelope, reporter, review-queue, and TDD boundaries.
- `../status-taxonomy.json` — sole machine-readable enum authority for registry, execution, review, evidence, and CLI-visible scope values.
- `src/status-taxonomy.ts` — taxonomy loader, integrity checks, active/inactive validation, and checksum generation.
- `src/identifiers.ts` — module-first function/case/dataset ID validation.
- `src/retry-outcome.ts` — one initial attempt plus three retries, delay orchestration, outcome and review-status derivation.
- `src/evidence-policy.ts` — clean, potential-issue, and flaky artifact-retention decisions.
- `src/envelope.ts` — result-envelope validation, recursive secret redaction, and stable checksums.
- `src/result-store.ts` — built-in Node SQLite migrations, atomic/idempotent execution writes, human-review queue, and summary formatting.
- `src/migrations/v2-status-taxonomy-and-timestamps.ts` — synchronized SQLite enum validation plus additive run, attempt, and dataset timing fields.
- `src/runtime-config.ts` — global runtime, browser, endpoint, and secure account resolution.
- `src/api-client.ts` — sanitized development API setup client.
- `src/artifact-manager.ts` — rolling final-failure and flaky before/after screenshot retention.
- `src/run-function.ts` — function-level deterministic CLI runner.
- `src/test-menu-support.ts` — registry-driven module/scope catalog and safe command construction.
- `src/test-menu.ts` — interactive module/function/flow selection, preflight, execution, summaries, and review-queue entry point.
- `src/preflight.ts` — global package/browser and dashboard availability check.
- `src/review-cli.ts` — explicit append-only human classification command.
