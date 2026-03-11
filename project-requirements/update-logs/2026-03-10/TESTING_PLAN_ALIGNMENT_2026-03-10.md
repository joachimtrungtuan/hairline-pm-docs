# Testing Plan Alignment Updates

**Date**: 2026-03-10
**Type**: Testing plan/documentation alignment
**Scope**: `local-docs/testing-plans/2026-03-10/automated/`

## Summary

Aligned the March 10 automated testing-plan documents with approved FR/system PRD scope so developers can write test scripts without inheriting unsupported or ambiguous business requirements.

## Updated Documents

- `local-docs/testing-plans/2026-03-10/automated/provider-dashboard/test-requirements.md`
- `local-docs/testing-plans/2026-03-10/automated/provider-dashboard/test-checklist-report.md`
- `local-docs/testing-plans/2026-03-10/automated/admin-dashboard/test-requirements.md`
- `local-docs/testing-plans/2026-03-10/automated/admin-dashboard/test-checklist-report.md`

## Changes Made

### 1. Corrected FR traceability

- Replaced provider auth references to `FR-001` with `FR-009`
- Corrected provider profile/settings references to include `FR-032`
- Corrected admin auth references to `FR-031`
- Corrected admin provider-management references to `FR-015`
- Fixed source paths where requirements exist only in `system-prd.md` and not in a dedicated FR PRD yet

### 2. Removed unsupported registration assumptions

- Removed provider self-registration expectations from provider auth checklist
- Replaced provider registration flow with invite-acceptance/account-setup flow from `FR-009`
- Removed admin self-registration / OTP-verification expectations from admin auth checklist
- Replaced admin auth coverage with provisioned-account and revoked-access scenarios aligned to admin access-control scope

### 3. Converted ambiguous expectations into assertable outcomes

- Quote submission without appointment slot now explicitly fails validation
- Provider auth expired-token scenario now explicitly requires re-authentication before protected data is returned
- Provider clinical note requirement now explicitly reflects optional day-note behavior
- Provider completion edge case now explicitly enforces the `Confirmed -> In Progress -> Aftercare -> Completed` sequence
- Admin expired-token, deposit-range, and provider-status idempotency expectations now use single deterministic outcomes

### 4. Tightened handoff quality for developer-authored tests

- Kept the checklist/report structure intact for tester fill-in
- Preserved concise result-entry guidance
- Improved scriptability by removing `check FR`, `if supported`, and similar loophole phrasing from the reviewed problem areas

## Outcome

The automated testing-plan set is now materially closer to the approved business requirements and safer to hand off as the source document for test-script development.
