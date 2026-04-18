# FR-014 Code-Aligned Fixes

**Date**: 2026-04-17  
**Report Type**: FR-014 code-aligned fixes  
**Primary Document**: `local-docs/project-requirements/functional-requirements/fr014-provider-analytics-reporting/prd.md`

---

## Summary

Applied the user-approved FR-014 follow-up fixes after checking the implementation codebase to verify which dependency fields actually exist and where they are sourced from.

---

## What Changed

1. **Commission analytics made model-aware**
   - Replaced percentage-only commission formulas with effective commission logic that supports both provider commission models:
     - Percentage: percentage of completed payment amount
     - Flat Rate: fixed amount per completed booking/payment
   - Updated provider and admin financial sections plus `REQ-014-051`.

2. **Dependencies corrected to code-backed sources**
   - Replaced the stale `FR-015` dependency wording that implied `currency`, `payout_cadence`, and `sla_minutes` lived directly on the provider profile.
   - Documented the actual implementation-backed sources:
     - `providers.timezone`
     - `provider_commissions.type`, `price`, `payment_cycle`
     - `banking_details.currency`
     - `inquiry_providers.*` for inquiry distribution analytics
   - Documented that provider-team activity currently references `provider_users.last_login_at`, but that field is not yet established as a canonical schema field in `system-data-schema.md`.

3. **Admin analytics restored to responsive-web scope**
   - Removed the desktop-only/admin-non-responsive assumption.
   - Updated Screen 7 layout and assumptions to align with the constitution’s responsive-web requirement.

4. **SLA dependency clarified**
   - Reframed provider-specific SLA storage as an unresolved canonical-data dependency.
   - Renamed the aggregate entity field from `sla_minutes` to `effective_sla_minutes` to avoid implying a validated provider-profile column already exists.

---

## Evidence Basis

Key implementation evidence used for this update:

- Provider timezone exists on `providers.timezone`
- Provider currency is currently resolved from `banking_details.currency`
- Payout cadence is currently modeled through `provider_commissions.payment_cycle`
- Inquiry distribution records exist through `inquiry_providers`
- Current TTFQ implementation uses a platform-default SLA rather than a provider-specific persisted SLA source

---

## Impact

- FR-014 now matches the current code-backed ownership of financial, payout, currency, and inquiry-distribution dependencies more closely.
- The PRD no longer contradicts the supported flat-rate commission model.
- Admin analytics requirements are back in constitution-compliant responsive scope.

