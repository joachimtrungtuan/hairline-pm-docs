# FR-017 Verification Alignment — 2026-04-01

**Document**: `local-docs/project-requirements/functional-requirements/fr017-admin-billing-finance/prd.md`
**Status Before**: Draft
**Change Type**: Major alignment update after FR verification review

---

## Summary

Applied the accepted verification resolutions for FR-017:

- Discount creation and approval ownership removed from FR-017 and kept fully in `FR-019 / A-06`
- Provider commission source/model aligned to `FR-015 / A-02` as the canonical owner, including support for both `Percentage` and `Flat Rate`
- Provider payout approval clarified as a buffer-period approval action only; Stripe transfer now occurs on payout day for already approved statements
- Admin MFA wording corrected to match the constitution: MVP uses password re-authentication; MFA becomes mandatory once `FR-026 / FR-031` is delivered

---

## Changes Made

### 1. Discount Ownership Realigned to FR-019

- Replaced the old discount-creation user story in FR-017 with a read-only discount usage and ROI tracking story
- Updated `REQ-017-003` so FR-017 now covers discount analytics and financial visibility only
- Preserved Screen 4 as a reconciliation/reporting consumer of FR-019 data

### 2. Provider Commission Contract Realigned to FR-015

- Updated payout screens and dependency language to read commission data from `FR-015 / A-02`
- Removed the incorrect `FR-029` ownership for provider commission configuration
- Replaced percentage-only wording with a commission configuration model that supports both `Percentage` and `Flat Rate`
- Updated the provider payout entity shape to include `commission_model` and `commission_value`

### 3. Payout Timing Clarified

- Confirmed the intended operating model:
  - Admin approves statements during the buffer window
  - No payment is sent during approval
  - On payout day, Stripe automatically processes all statements already in `Approved`
- Updated payout screen rules, workflow wording, and User Story 1 acceptance criteria to match this behavior
- Preserved overdue approvals as an exception path that can process immediately after the normal payout day is missed

### 4. Constitution Compliance Fix

- Rewrote FR-017 security wording so MVP requires password re-authentication rather than immediate platform-wide MFA enforcement
- Added the future-state dependency on `FR-026 / FR-031` for MFA-based re-authentication

---

## Result

FR-017 now has a clean ownership boundary with `FR-019`, a correct dependency contract with `FR-015`, and a single unambiguous payout-processing model for the normal billing cycle.
