# Provider Login E2E First Case Registration

**Date:** 2026-07-14
**Status:** Draft case implemented and controlled execution passed; activation pending Product Owner approval

## Summary

Registered the first real deterministic web E2E function under `PR-01: Auth & Team Management`:

- `PR-01-FN-001` — Provider login;
- `PR-01-TC-0001` — Active Provider successfully logs in;
- `PR-01-DS-0001` — registered active Provider credential recipe.

The browser flow starts at the shared role-selection page, selects the Provider role, submits the existing registered development credential through the live UI, observes the authentication response, and verifies arrival at the Provider Dashboard.

## Sources and Boundaries

- Requirement ownership references the live FR-009 and FR-015 PRDs without copying their requirements.
- The implemented UI and authentication request were inspected through Playwright MCP against `https://admin.hairline.app`.
- No file under `main/` was read, imported, or changed.
- No Playwright package or browser was installed; execution reused the global Playwright MCP runtime and installed system Chrome.
- The case remains `DRAFT`; controlled validation does not activate it.

## Validation

- Registry selection test passed.
- Full framework suite passed: 24 tests.
- Development preflight passed with the global Playwright runtime and system Chrome.
- Controlled command: `pnpm test:function PR-01 PR-01-FN-001 --case PR-01-TC-0001 --allow-draft`.
- Run `RUN-20260714T050551Z-99620d3e`: `PASSED / REVIEW_NOT_REQUIRED` on the initial attempt.
- Pending human review: 0.
- No screenshot or trace was retained for the clean pass.
- The canonical SQLite result database was created at `testing-automation/results/test-results.sqlite`.

## Next Gate

Obtain explicit Product Owner approval before changing `PR-01-TC-0001` from `DRAFT` to `ACTIVE`. Once active, the ordinary function command will no longer require `--allow-draft`.

## Manual Operations Runbook

Expanded `testing-automation/OPERATIONS.md` into the user-facing manual runbook for token-free terminal execution. It now covers prerequisites, registry/status lookup, preflight, focused visible or headless execution, SQLite and artifact locations, human review, and approved re-testing. The PR-01 module index also records the exact controlled-validation command while the case remains `DRAFT`.
