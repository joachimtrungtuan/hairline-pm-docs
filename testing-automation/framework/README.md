# Testing Framework

**Status:** MVP framework complete; product registry empty and ready for first registration
**Governing document:** `local-docs/testing-automation/TESTING-CONSTITUTION.md`

This folder will contain reusable deterministic Playwright infrastructure such as API clients, authentication helpers, data builders, fixtures, reusable page interactions, reporters, and runtime configuration.

It must not contain copied requirements or module-specific business rules merely for convenience. A helper begins within its owning module and moves here only after genuine cross-module reuse is demonstrated.

The framework reuses the globally installed `@playwright/mcp` package and system Chrome. It never installs Playwright and has no dependency on `main/`. It provides credential-registry resolution, API support, dynamic registered-case loading, four-attempt retry orchestration, rolling screenshots/traces, canonical SQLite writes, and a human review queue.

Contract:

- `RUNNER-CONTRACT.md` — deterministic command, lifecycle, envelope, reporter, review-queue, and TDD boundaries.
- `src/identifiers.ts` — module-first function/case/dataset ID validation.
- `src/retry-outcome.ts` — one initial attempt plus three retries, delay orchestration, outcome and review-status derivation.
- `src/evidence-policy.ts` — clean, potential-issue, and flaky artifact-retention decisions.
- `src/envelope.ts` — result-envelope validation, recursive secret redaction, and stable checksums.
- `src/result-store.ts` — built-in Node SQLite migrations, atomic/idempotent execution writes, human-review queue, and summary formatting.
- `src/runtime-config.ts` — global runtime, browser, endpoint, and secure account resolution.
- `src/api-client.ts` — sanitized development API setup client.
- `src/artifact-manager.ts` — rolling final-failure and flaky before/after screenshot retention.
- `src/run-function.ts` — function-level deterministic CLI runner.
- `src/preflight.ts` — global package/browser and dashboard availability check.
- `src/review-cli.ts` — explicit append-only human classification command.
