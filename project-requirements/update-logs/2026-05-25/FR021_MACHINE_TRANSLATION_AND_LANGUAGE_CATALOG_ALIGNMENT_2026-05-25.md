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
