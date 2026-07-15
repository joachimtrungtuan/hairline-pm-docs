# E2E Complete Case Coverage and Provider Login Suite

**Date:** 2026-07-15
**Status:** Constitution v1.2 approved; Provider login function suite active

## Summary

Updated the deterministic web E2E workflow so Product Owner approval is required for the function boundary and canonical happy path, while unambiguous non-happy cases are derived from the applicable PRDs without case-by-case approval. Every new function or flow must map all applicable normative requirements to executable cases or governed coverage gaps and document category applicability.

Expanded `PR-01-FN-001` from one happy-path case to six active cases executed together:

- active Provider login;
- missing username validation;
- missing password validation;
- both fields empty;
- unknown credentials rejected;
- Provider credentials rejected on the Hairline Team route.

## Coverage Boundaries

The registry records four open requirements rather than treating them as passing coverage:

- suspended Provider login and restriction banner;
- deactivated Provider login rejection;
- removed team-member access revocation;
- configured user lockout and fixed IP throttling.

These require dedicated account-state fixtures or safe reset/IP-isolation controls before deterministic execution can be activated.

## Workflow and Documentation

- Promoted Testing Constitution v1.2 as the active baseline.
- Updated the registry template with requirement and category coverage matrices.
- Made the function-wide command the normal manual execution path; `--case` remains a diagnostic selector.
- Preserved mandatory human review for every non-clean result and prohibited automated AI bug decisions.
- Continued referencing live PRDs without copying requirement narratives.

## Validation

- Focused registry/dataset tests passed: 5 tests.
- Full framework unit suite passed: 26 tests.
- Development preflight passed with the existing global Playwright runtime and installed system Chrome.
- Controlled complete-function run: `pnpm test:function PR-01 PR-01-FN-001 --allow-draft`.
- Run `RUN-20260714T215851Z-40eaa16c`: all six cases passed on the initial attempt.
- Ordinary active-suite run: `pnpm test:function PR-01 PR-01-FN-001`.
- Run `RUN-20260714T220554Z-028ca2ef`: all six active cases passed on the initial attempt with no draft override.
- Pending human review: 0.
- No screenshot or trace was retained for the clean pass.
- No Playwright package or browser was installed, and no dependency on `main/` was introduced.

## Manual Command

From `local-docs/testing-automation/`, run:

```bash
pnpm test:function PR-01 PR-01-FN-001
```

This executes all six active Provider login cases in one deterministic, token-free browser run.

## Interactive Test Console

Added executable `testing-automation/test.sh` as the centralized, token-free entry point. It opens a registry-driven terminal menu for module and function/flow selection, full-scope or diagnostic-case execution, visible/headless browser choice, all-active execution, preflight, the pending human-review queue, and the latest SQLite run summary.

The Bash launcher contains no copied test catalog. Its TypeScript menu reads active modules, functions/flows, cases, display metadata, and governed gap counts from the existing machine-readable registry, then invokes the existing pnpm commands. Draft execution remains unavailable through the normal menu.

Console validation completed with:

- Bash syntax validation passed;
- full framework suite passed: 30 tests;
- interactive module, function, scope, browser-mode, and confirmation menus verified;
- menu-selected headless diagnostic run `RUN-20260714T222340Z-e08098f0` passed on the initial attempt;
- latest-run summary correctly returned that run;
- pending human-review queue remained at 0;
- no screenshot or trace was retained for the clean pass.
