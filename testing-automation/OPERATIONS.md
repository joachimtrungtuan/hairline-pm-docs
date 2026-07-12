# Web E2E Operations

**Status:** MVP setup complete; product test registry intentionally empty
**Runtime:** Existing global `@playwright/mcp` package plus installed system Chrome
**Package manager:** pnpm only

## 1. Non-Negotiable Boundaries

- Do not install Playwright or browsers from this project.
- Do not read from, import from, write to, or otherwise depend on `main/`.
- Use live PRDs as requirement authority and the development UI/API as implementation evidence.
- Every non-pass enters `NEEDS_HUMAN_REVIEW`; no AI or runner confirms bugs.
- Retain generated development records.

## 2. Runtime Inputs

The runner resolves V1, P1, and S1 from `local-docs/testing-plans/testing-credentials/` by default. Environment variables may select another registered account or override credentials without copying them into source or results.

See `.env.example` for optional settings. Export values in the shell; do not commit a populated environment file.

## 3. Commands

From `local-docs/testing-automation/`:

```bash
pnpm test:unit
pnpm test:preflight
pnpm test:function <module-id> <function-id>
pnpm test:function <module-id> <function-id> --case <case-id>
pnpm test:review-queue
pnpm test:review <execution-id> --classification <human-decision> --reviewer <name-or-role> --notes <text> [--retest-required]
```

Before the first registration, function selection intentionally reports `Unknown function`. Ordinary execution rejects draft cases. During a human-approved implementation proof only, append `--allow-draft`; this does not activate or approve the registry entry.

`HAIRLINE_HEADLESS=true` enables headless execution. The default is visible browser execution.

## 4. Result Interpretation

- `PASSED`: initial attempt passed; no screenshot retained.
- `FLAKY_OR_TRANSIENT`: a retry passed; latest failed and passing screenshots retained; human review required.
- `POTENTIAL_ISSUE`: four equivalent failures, at least five seconds apart; only the rolling final screenshot retained; human review required.
- `INCONSISTENT_FAILURE`: four failures with different signatures; final screenshot retained; human review required.
- `BLOCKED`: preflight or API dataset preparation prevented browser execution; no UI screenshot is fabricated; human review required.

Canonical results are stored in `results/test-results.sqlite`. Screenshots are stored beneath `results/artifacts/<run-id>/<module>/<case-id>/` and are excluded from source control.

The review command is intentionally explicit and human-controlled. It appends the decision and changes the queue status to `REVIEWED`; it never changes the original automated outcome.

## 5. MVP Boundary

The initial setup supports function-level execution, retained datasets, screenshots/traces, SQLite review data, and human decisions. Add module, cross-module flow, regression selectors, and PRD section hashing when the first registered cases require them; they are not setup blockers.

## 6. Registration and Frontend Changes

Registration always begins with a narrow scout of the live PRD's module scope and overall workflows. The agent returns only a concise outline and stops for Product Owner approval and operational corrections. Detailed UI/API scouting and case creation begin only after approval.

A UI discrepancy never causes automatic test rewriting. The execution enters human review. After a human confirms an intentional frontend change, the registration workflow updates selectors/actions, records a new case revision, and re-runs affected regression tests.
