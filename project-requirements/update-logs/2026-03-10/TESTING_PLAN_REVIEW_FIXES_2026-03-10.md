# Testing Plan Review Fixes

**Date**: 2026-03-10
**Type**: Testing plan/documentation corrections
**Scope**: `local-docs/testing-plans/2026-03-10/`

## Summary

Applied post-review fixes to the March 10 testing-plan set so the folder no longer mixes corrected automated checklists with stale manual-auth assumptions or missing traceability references.

## Updated Documents

- `local-docs/testing-plans/2026-03-10/manual/admin-dashboard-manual-testing-plan.md`
- `local-docs/testing-plans/2026-03-10/manual/provider-dashboard-manual-testing-plan.md`
- `local-docs/testing-plans/2026-03-10/automated/admin-dashboard/test-requirements.md`
- `local-docs/testing-plans/2026-03-10/automated/provider-dashboard/test-requirements.md`

## Changes Made

### 1. Corrected stale manual-auth scope

- Replaced admin manual references to `FR-001` and admin self-registration with `FR-031` team-access validation
- Replaced provider manual self-registration and OTP flow with the approved access model:
  - provider owner account provisioned by admin (`FR-015`)
  - team-member access via invitation acceptance (`FR-009`)
  - password policy traceability via `FR-026`

### 2. Clarified which docs are the developer handoff artifact

- Marked both manual plans as reference walkthroughs only
- Added explicit usage notes pointing developers to the automated `test-checklist-report.md` files as the canonical handoff and result-report artifacts
- Added concise manual-run summary sections so any exploratory run can still capture business gaps, blocked items, and risks

### 3. Closed remaining traceability gaps in automated requirements

- Added `FR-026` to provider automated test requirements for password-policy-backed account setup/reset coverage
- Added `FR-029` to admin automated test requirements for deposit-range and payment-configuration coverage

## Outcome

The March 10 testing-plan folder now has:

- corrected auth and access assumptions
- clearer separation between manual reference walkthroughs and developer-facing reporting checklists
- stronger FR traceability for password-policy and payment-configuration tests
