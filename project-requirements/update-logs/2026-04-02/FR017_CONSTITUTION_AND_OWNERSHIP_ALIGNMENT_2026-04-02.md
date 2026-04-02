# FR-017 Constitution and Ownership Alignment

**Date**: 2026-04-02  
**Scope**: Constitution, FR-017, FR-015, FR-029, constitution summary

## Summary

Applied the agreed documentation decisions following FR-017 verification:

1. Removed the constitution-level requirement for multi-person refund approval and replaced it with documented justification plus full audit-trail control.
2. Finalized the commission ownership split:
   - `FR-029 / A-09` owns the global commission default and booking-time snapshot policy.
   - `FR-015 / A-02` owns provider-specific commission overrides and payout frequency.
   - `FR-017 / A-05` consumes the effective commission snapshot in payout and reconciliation flows.
3. Normalized provider bank-detail ownership to `FR-032 / PR-06` Billing Settings and removed stale wording in `FR-017` that incorrectly implied `FR-015` stored payout bank details.

## Files Updated

- `.specify/memory/constitution.md`
- `local-docs/project-requirements/constitution-summary.md`
- `local-docs/project-requirements/functional-requirements/fr017-admin-billing-finance/prd.md`
- `local-docs/project-requirements/functional-requirements/fr015-provider-management/prd.md`
- `local-docs/project-requirements/functional-requirements/fr029-payment-system-config/prd.md`

## Key Decisions Captured

### Refund Control

- Constitution now requires documented justification and full audit trail for refunds.
- FR-017 remains aligned to single-operator refund execution with mandatory reason, re-authentication, and audit logging.

### Commission Ownership

- `FR-029` no longer claims provider-specific commission ownership.
- `FR-015` is the owner of provider-specific commission override and payout frequency.
- `FR-017` now explicitly routes commission-change decisions to `FR-015` or `FR-029` based on whether the change is provider-specific or global.

### Provider Bank Details

- `FR-017` now treats `FR-032` Billing Settings as the canonical source for provider payout destination details.
- Payout-readiness warnings and dependency text in `FR-017` were updated to reference `FR-032` instead of onboarding storage in `FR-015`.

## Result

Cross-document ownership is now consistent for the three verified problem areas:

- refund governance,
- commission configuration ownership,
- provider payout bank-detail ownership.

Follow-up refinement on 2026-04-02:

- Aligned `FR-017` Screen 1 so the financial-reporting currency selector initializes from `FR-029` Screen 6 system default currency, replacing the stale `GBP` default with the product decision to seed the MVP default as `USD`.
- Corrected `FR-017` screen grouping so the admin investigation/audit screens sit under an admin-only subsection ahead of the provider read-only section; no other screen ownership placement mismatch was found in the same audit pass.
- Renumbered the live `FR-017` screen model so admin screens are contiguous (`Screens 1–8`) and provider read-only screens shift to `Screens 9–10`; quick-reference update-log index entries were updated to the new numbering, while older detailed FR-017 reports remain as historical snapshots of the numbering used when they were written.
