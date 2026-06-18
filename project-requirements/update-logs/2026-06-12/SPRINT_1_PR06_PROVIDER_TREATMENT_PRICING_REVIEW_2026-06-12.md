# Sprint 1 PR-06 Provider Treatment Pricing Review

**Date:** 2026-06-12  
**Report Type:** Sprint Readiness Report Update  
**Primary Document Updated:** `local-docs/product-plans/2026-05-29/sprint-1-readiness-fix-backlog.md`

## Summary

Recorded confirmed PR-06 provider-treatment issues covering treatment card interaction, wrong detail-surface routing, provider pricing structure/status semantics, stale list pricing after save, hardcoded currency behavior, and an unwired deactivate action.

## What Changed

- Updated the `PR-06 - Profile & Settings Management` section in the Sprint 1 readiness backlog.
- Expanded `Review Notes` to include provider treatment list/detail/pricing-config review in addition to the earlier staff-surface findings.
- Added confirmed `Recorded only` defect rows for:
  - `Provider Treatments List -> Open Treatment Detail`
  - `Provider Treatment Detail -> Wrong Surface / Structure`
  - `Provider Treatment Pricing -> Step Structure And Status Semantics`
  - `Provider Treatment Pricing -> Save Success But List Price Stays Stale`
  - `Provider Treatment Pricing -> Currency Source Mismatch`
  - `Provider Treatments List -> Deactivate Action Unwired`

## Findings Captured

- Provider treatment cards do not expose an obvious primary path into detail; users must discover `View` inside the three-dot menu.
- Provider `/treatments/:id` is routed to a shared admin/team-style treatment detail component that shows unrelated status and action patterns such as `in progress` and `End Treatment`.
- FR-024 defines provider treatment control as pricing configuration plus an `Offered / Not Offered` toggle, but the current provider pricing flow is implemented as a four-step admin-like wizard and also shows a misleading disabled `Active treatment` switch on Step 1.
- Provider pricing save appears to succeed, but the list view still renders old price data because the card reads top-level treatment pricing fields rather than the provider-specific `pricing` payload returned by the provider treatment list API.
- The provider pricing currency selector is hardcoded in the frontend and does not pre-select the provider's default currency when no prior pricing exists, which conflicts with FR-024.
- The provider treatment-card `Deactivate` action is dead code at the UI level and does not map cleanly to the PRD's `Offered / Not Offered` provider-status model.

## Evidence Basis

- Screenshot evidence:
  - `https://s.letweb.net/s/ejnnvw`
  - `https://s.letweb.net/s/dkmm0o`
  - `https://s.letweb.net/s/gl9949`
  - `https://s.letweb.net/s/emooqj`
  - `https://s.letweb.net/s/ejnnvv`
  - `https://s.letweb.net/s/dkmm03`
  - `https://s.letweb.net/s/gl994l`
  - `https://s.letweb.net/s/emooqy`
- Code evidence:
  - `main/hairline-frontend/src/pages/providerDashboard/treatments/Treatments.jsx`
  - `main/hairline-frontend/src/components/providerDetailsComponents/Treatment.jsx`
  - `main/hairline-frontend/src/pages/providerDashboard/treatments/pricingConfig/ProviderTreatmentPricingConfig.jsx`
  - `main/hairline-frontend/src/pages/providerDashboard/treatments/pricingConfig/steps/TreatmentStep.jsx`
  - `main/hairline-frontend/src/pages/providerDashboard/treatments/pricingConfig/steps/PriceStep.jsx`
  - `main/hairline-frontend/src/pages/providerDashboard/treatments/pricingConfig/steps/SummaryStep.jsx`
  - `main/hairline-frontend/src/App.jsx`
  - `main/hairline-frontend/src/pages/teamDashboard/treatments/TreatmentDetails.jsx`
  - `main/hairline-backend/app/Http/Controllers/Packages/TreatmentController.php`
  - `main/hairline-backend/app/Http/Requests/StoreProviderTreatmentPricingRequest.php`
  - `main/hairline-backend/app/Http/Requests/UpdateProviderTreatmentPricingRequest.php`

## Follow-up Task Creation

- Created Plane work items for all six PR-06 provider treatment-pricing rows and updated their readiness backlog `Task Status` values from `Recorded only` to `Task created`: `HAIRL-1325`, `HAIRL-1326`, `HAIRL-1327`, `HAIRL-1328`, `HAIRL-1329`, and `HAIRL-1330`.

## 2026-06-15 Follow-up

- Extended the same `PR-06 - Profile & Settings Management` readiness section with direct Provider `Settings -> Account Information` findings from live product review.
- Added a `Review Notes` update confirming that account-settings behavior is now directly tested, not only left as a generic evidence gap.
- Recorded new `Recorded only` PR-06 rows for:
  - Owner `Account name` sync using the wrong provider field and falling back to personal first name
  - Provider-side phone country-code re-parse corruption after save/reload (`+44` becoming `+4477`)
  - Generic `Unauthenticated.` password-error messaging on invalid password input
  - Password change failure even when all visible requirements are met
  - Missing first/last-name validation for digits and special characters
  - Divergent display-name mappings across Account Information, Provider Profile staff cards, and the top navbar identity
- Captured supporting code evidence that the Owner account-name path reads `$provider->name` while provider profile uses `provider_name`, the phone parser uses a greedy `+\\d{1,4}` split, and navbar identity comes from stale Redux auth user data instead of refreshed account-settings state.
- Refined the remaining `Provider clinic profile and package catalog` `Review pending` row so it no longer treats `Account Information` as an untouched evidence gap after direct testing already covered that tab.
- Added PR-06 pass coverage notes that provider account timezone save, `Cancel` reset behavior, and single-field / multi-field account-info saves appear to work normally; the remaining account-settings defects stay focused on mapping, validation, and password behavior.
- Extended the same PR-06 section with direct `Notification Preferences` coverage notes confirming basic toggle persistence, `Enable All`, `Disable All` warning, and save/reload behavior.
- Recorded new `Recorded only` PR-06 rows for:
  - notification-type expand/collapse disclosure being under-signaled and interactionally ambiguous relative to the row toggle
  - missing unsaved-changes indicator parity between `Notification Preferences` and `Account Information`
- Narrowed the remaining `Provider clinic profile and package catalog` `Review pending` row again so it now tracks only the PR-06 areas still unreviewed after direct `Notification Preferences` coverage.
- Extended the same PR-06 section with direct `Billing` coverage notes confirming Dataset A create/save/reload works, existing bank details can be edited and persisted, `Cancel` resets to last saved data, and the visible 200-character caps on account-holder and bank-name fields are enforced.
- Recorded new `Recorded only` PR-06 rows for:
  - missing unsaved-changes indicator / leave-warning parity between `Billing` and `Notification Preferences`
  - missing `Account Holder Name` validation against the PRD's alphabetic-and-spaces rule
  - inconsistent validation timing / visual feedback across billing fields (`Routing/SWIFT`, `IBAN`, and field-length feedback)
- Narrowed the remaining `Provider clinic profile and package catalog` `Review pending` row again so it now tracks only the PR-06 areas still unreviewed after direct `Billing` coverage.
- Cleaned a markdown-table parsing defect in the Sprint 1 readiness backlog by removing a literal `|` from table-cell prose, and mirrored the new no-literal-pipe-in-table-cells rule into the root guidance files `CLAUDE.md` and `AGENTS.md`.
