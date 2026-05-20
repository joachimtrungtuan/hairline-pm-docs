# FR-021 Localization Management Revision - 2026-05-19

## Summary

Major revision of `local-docs/project-requirements/functional-requirements/fr021-i18n-localization/prd.md` to tighten the localization-management operating model and close logic gaps around admin-managed translation content.

The revised FR keeps the client-backed multilingual requirement as the anchor, while adding product-defined implementation rules where the transcriptions did not specify the technical approach.

---

## Key Changes

- Reframed FR-021 around a hybrid localization-management model:
  - canonical translation registry as source of truth
  - table/grid editing for precise admin updates
  - JSON import/export for translator handoff and bulk updates
  - draft changes separated from published runtime bundles
  - immutable published versions and rollback support
- Added tenant-specific language-change locations:
  - Patient App: Settings > Language & Region
  - Provider Dashboard: top-bar language selector
  - Admin Platform: top-bar language selector
- Reconciled the PRD structure with `.specify/templates/prd-template.md` and verified PRD conventions:
  - Multi-Tenant Architecture
  - Multi-Tenant Breakdown
  - Communication Structure
  - template-style Business Rules, Success Criteria, Dependencies, Assumptions, Implementation Notes, User Scenarios, Functional Requirements Summary, and Key Entities
- Rebuilt Screen Specifications into tenant sections:
  - Patient Platform
  - Provider Platform
  - Admin Platform
- Expanded Admin Platform screens instead of cramming all localization controls into one screen:
  - Supported Locales
  - Translation Registry
  - Translation Key Detail Editor
  - JSON Import
  - JSON Export
  - Publish & Version History
  - Coverage & Missing Translations
- Added explicit draft/publish behavior:
  - inline edits and imports save draft changes only
  - runtime clients consume published bundles only
  - publish creates a versioned bundle
  - rollback creates a new version restoring a prior bundle
- Added source-locale protection:
  - English remains the initial source/default locale
  - English edits require elevated authorization, reason capture, and audit logging
  - source meaning changes mark dependent translations as Review Needed
- Added import/export validation rules:
  - JSON syntax
  - known keys
  - duplicate keys
  - placeholder parity
  - ICU syntax
  - target locale compatibility
- Clarified related-FR ownership:
  - FR-030 owns notification template authoring
  - FR-027 owns legal content versioning
  - FR-024 registers treatment/package translatable content
  - FR-032 uses language catalog for provider spoken languages, separate from UI language preference
- Expanded Functional Requirements Summary from 7 requirements to 20 requirements.
- Expanded Key Entities to include `TranslationKey`, `TranslationValue`, `TranslationImport`, `TranslationVersion`, `TranslationBundle`, and `TranslationAuditLog`.
- Normalized Markdown table separator syntax to `| --- | --- |` style.

---

## Rationale

The previous FR-021 covered multilingual behavior, fallback, timezone, and currency at a high level, but did not define how Admin would manage translation text across Patient, Provider, and Admin tenants.

The new version closes the main operational gaps:

- Admin edits are controlled and auditable instead of immediately live.
- Translation releases are recoverable through version history and rollback.
- English/default text is protected because downstream translations depend on it.
- Table editing and JSON import/export are both supported, balancing flexibility and traceability.
- Runtime clients have a clear contract: they fetch published bundles, not draft values.

---

## Files Updated

- `local-docs/project-requirements/functional-requirements/fr021-i18n-localization/prd.md`

---

## Follow-Up Considerations

- FR-030 may need a future light sync if notification-template screens need to reference FR-021's publish/version behavior more explicitly.
- FR-026/FR-032 references to centrally managed language lists should remain aligned with FR-021 as the canonical locale/language catalog owner.
- Technical API naming is intentionally not fixed in FR-021; implementation can choose endpoint names as long as the documented workflows and constraints are met.
