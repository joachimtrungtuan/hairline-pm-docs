# FR-021 Machine Translation and Language Catalog Alignment

**Date**: 2026-05-25
**Type**: Major PRD Alignment
**Author**: Codex

## Summary

Updated FR-021 and FR-032 to resolve localization verification follow-ups and clarify source-of-truth boundaries for language, currency, and machine translation workflows.

## Changes

- Added FR-021 Screen 10: Admin - Machine Translation Provider & Draft Generation.
- Added machine-translation provider credential management with notable starting providers: Google Cloud Translation, DeepL, Microsoft Azure Translator, and Amazon Translate.
- Added machine-translation draft generation modes:
  - Prefill Missing Keys for a selected non-English language.
  - Replace Entire Language for a selected non-English language, excluding English/source values.
- Added the missing alternative flow for machine-translation draft generation.
- Clarified that machine translation creates Review Needed drafts only and never publishes directly to runtime clients.
- Added machine-translation validation, privacy, audit, credential-security, data dependency, entity, requirement, user story, and edge-case coverage.
- Added FR-029 / S-02 ownership for currency conversion configuration, rate sources, markup, rate locking, and payment fallback behavior; FR-021 now consumes currency display outputs only.
- Updated FR-032 stale references so provider spoken-language capacity consumes the FR-021 language/locale catalog surfaced through settings, instead of treating FR-026 as the language-list owner.

## Files Updated

- `local-docs/project-requirements/functional-requirements/fr021-i18n-localization/prd.md`
- `local-docs/project-requirements/functional-requirements/fr032-provider-dashboard-settings/prd.md`
- `local-docs/project-requirements/update-logs/README.md`

## Rationale

FR-021 owns app/UI language, locale catalog, translation registry, fallback, bundle publishing, and language-readiness workflows. FR-032 owns provider profile spoken-language capacity but should consume the FR-021 catalog. FR-026 may surface settings navigation and shared app settings but should not be treated as the language semantics owner.

Currency conversion remains owned by FR-029 / S-02; FR-021 only describes localized display behavior.

---

# FR-021 Verification Fixes (v1.3)

**Date**: 2026-05-25
**Type**: Major PRD Update (verification issue resolution)
**Author**: AI

## Summary

Applied six targeted fixes to FR-021 (and FR-029, system PRD) resolving issues found during structured verification of the FR.

## Changes

**FR-021 PRD (`fr021-i18n-localization/prd.md`)**:
- **Issue 1 — Elevated authorization defined**: Added "Elevated Authorization Definition" note in Business Rules > Configurable with Restrictions, specifying Super Admin role (FR-031) as the required role for English source edits, default locale changes, publish, and rollback.
- **Issue 2 — Currency formatting ownership clarified**: Updated Currency Rule 2 to state that locale-aware number formatting (decimal separator, symbol position, digit grouping, RTL rendering) is owned by S-02 as a shared service capability consumed by FR-021.
- **Issue 3 — Timezone fallback specified**: Added rule to Screen 1 Business Rules: null/unset timezone preference falls back to device/browser-detected timezone, then UTC with a visible indicator.
- **Issue 4 — Cache stale window defined**: Added Rule 13 to General Module Rules requiring clients to revalidate via ETag/hash and capping the maximum stale window at a platform-configurable interval (≤5 minutes recommended) after publish or rollback.
- **Issue 6 — Preparation locale selector exclusion**: Added rule to Screen 4 Business Rules stating only Active locales appear in user-facing selectors; Inactive and Preparation locales are hidden.

**FR-029 PRD (`fr029-payment-system-config/prd.md`)**:
- **Issue 2 (reciprocal)**: Added FR-021 to FR-029 Internal Dependencies, documenting that S-02 owns locale-aware number formatting as a shared service and FR-021 consumes S-02 currency conversion and formatting outputs.

**System PRD (`system-prd.md`)**:
- **Issue 5 — Module list corrected**: Updated FR-021 module list from A-09 + S-02 to P-01 + PR-06 + A-09 + S-02 + S-03, matching the full FR-021 PRD header.

## Files Updated

- `local-docs/project-requirements/functional-requirements/fr021-i18n-localization/prd.md`
- `local-docs/project-requirements/functional-requirements/fr029-payment-system-config/prd.md`
- `local-docs/project-requirements/system-prd.md`

---

# FR-021 Verification Fixes (v1.4)

**Date**: 2026-05-25
**Type**: Minor PRD Update (verification issue resolution)
**Author**: AI

## Summary

Applied four targeted fixes to FR-021 resolving issues found during a second structured verification pass.

## Changes

**FR-021 PRD (`fr021-i18n-localization/prd.md`)**:
- **Issue 1 — FR-031 added as formal dependency**: Added FR-031 / Admin Access Control & Permissions to the Internal Dependencies section, documenting that FR-021's four protected operations (English source edit, default locale change, publish, rollback) must be registered as Super Admin-only permissions in the FR-031 permission matrix at implementation time.
- **Issue 2 — "Preview only" removed from Screen 8 Import mode**: Removed the "preview only" option from the Import mode field. The required auto-generated Validation preview panel already serves this purpose before any import confirmation; the separate "preview only" mode option was redundant and created ambiguous interaction with the Import decision field.
- **Issue 3 — SC-002 wording corrected**: Changed "within 2 seconds" to "< 2 seconds" in SC-002 to match constitution Principle IV wording exactly.
- **Issue 4 — HTTP 403 error handling specified**: Added to the Admin Platform localization management integration point that protected endpoints (publish, rollback, English source edit, default locale change) must return HTTP 403 with the platform-standard error format when called by a non-Super-Admin role.

## Files Updated

- `local-docs/project-requirements/functional-requirements/fr021-i18n-localization/prd.md`

---

# FR-021 Verification Passed (v1.5)

**Date**: 2026-05-25
**Type**: Minor Update (status change)
**Author**: AI

## Summary

verify-fr completed with no issues found (0 critical, 0 medium, 0 minor). Status updated to ✅ Verified & Approved. Approvals section populated.

## Files Updated

- `local-docs/project-requirements/functional-requirements/fr021-i18n-localization/prd.md`
