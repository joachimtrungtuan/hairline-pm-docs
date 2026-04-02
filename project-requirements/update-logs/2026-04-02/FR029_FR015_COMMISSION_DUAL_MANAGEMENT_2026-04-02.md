# FR-029 / FR-015 Commission Dual Management Alignment

**Date**: 2026-04-02  
**Scope**: FR-029, FR-015, FR-017

## Summary

Updated the commission-configuration ownership model to match the implemented admin design.

This change supersedes the commission split adopted earlier on 2026-04-02 where `FR-029` was reduced to global-default-only commission management.

## Decision Applied

1. `FR-029 / A-09` again manages both:
   - the platform global commission default
   - provider-specific commission scopes in the central Commission Rate screen
2. `FR-015 / A-02` remains a valid admin management surface for single-provider commission updates inside the provider profile, and continues to own payout frequency.
3. `FR-017 / A-05` now treats provider commission as a shared effective configuration resolved from `FR-015` and `FR-029`, while preserving booking-time snapshot behavior.

## Files Updated

- `local-docs/project-requirements/functional-requirements/fr029-payment-system-config/prd.md`
- `local-docs/project-requirements/functional-requirements/fr015-provider-management/prd.md`
- `local-docs/project-requirements/functional-requirements/fr017-admin-billing-finance/prd.md`

## What Changed

### FR-029

- Restored the Commission Rate workflow to include both:
  - Global Default
  - Provider Specific commission scopes
- Updated Screen 5 to match the implemented design pattern with selected providers, provider commission rate, effective date, and edit/archive actions.
- Added an explicit synchronization requirement so provider-specific commission values remain aligned between `FR-029` Screen 5 and `FR-015` Tab 7.
- Expanded dependencies, requirements, and entity definitions so provider-specific commission scopes are part of the live payment-configuration model again.

### FR-015

- Reframed Tab 7 as the single-provider commission management surface that stays synchronized with `FR-029` Screen 5.
- Preserved `FR-015` ownership of payout frequency.
- Added operational guidance: use `FR-015` for provider-by-provider work and `FR-029` for central or bulk commission-scope administration.

### FR-017

- Replaced the old wording that treated `FR-015` as the only provider-specific commission source.
- Updated payout, provider-history, and currency-alert wording to consume the shared effective commission configuration.
- Adjusted dependency text so `FR-029` now includes the central provider-scope commission screen, while `FR-015` remains the single-provider surface plus payout-frequency owner.

## Result

The three live PRDs are now aligned to the implemented commission-management design:

- `FR-029` = central commission settings screen
- `FR-015` = single-provider commission + payout-frequency screen
- `FR-017` = downstream consumer of the effective commission snapshot
