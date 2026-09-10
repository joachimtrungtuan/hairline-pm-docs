# FR-004 Dependency and Verification Fixes

**Date**: 2026-09-10
**Type**: Approved verification follow-up and cross-FR contract reconciliation
**Scope**: FR-004 v2.6, FR-019 v2.1, FR-024 v1.2, FR-026 v1.8, their Change Requests, and the quote promotion relationship in the system data schema
**Trigger**: Product Owner selection of Option 1 for all three findings in the FR-004 v2.5 verification report

---

## Summary

The selected corrections preserve the approved parent-quote/Quote Option model while closing the immutable-audit wording defect, aligning three non-deferred dependency owners, and completing FR-004 validation, evidence, and approval metadata. FR-005, FR-006, FR-008, FR-014, and FR-015 remain intentionally deferred.

## Changes Applied

### 1. Immutable audit access

FR-004 Admin Workflow 5 now permits quote archive/restore actions and read-only access to immutable audit/version history. It no longer implies that an administrator can edit audit records.

### 2. Dependency-owner reconciliation

- FR-019 attaches promotions through `QuoteOptionDatePrice.promotionId` and records both parent-quote containment and the single option/date-price target for ad-hoc quote-bound programs.
- FR-024 supplies immutable Package ID/version provenance to FR-004 Quote Option snapshots and marks the direct `QuotePackage` link as legacy compatibility only.
- FR-026 owns a versioned Quote Configuration with one enabled ISO 4217 currency and positive whole-number expiry window, default 48 hours. FR-004 consumes both values from one configuration version for new quotes only.
- The system data schema now points the deprecated parent quote discount field to the option/date promotion relationship.

### 3. Verification completeness

- Completed FR-004 text/file validation limits using current schema and platform conventions.
- Populated the References section with corrected transcription ranges and approved subsequent-source evidence.
- Recorded Product Owner approval by name and marked absent Technical Lead/Stakeholder approvals as not recorded rather than leaving placeholders.

## Change Requests

- `CR-FR019-20260910-01`: option/date promotion attachment and redemption provenance.
- `CR-FR024-20260910-01`: Quote Option package provenance and legacy-link deprecation.
- `CR-FR026-20260910-01`: quote currency/expiry configuration ownership.

All three retain `Implementation Reconciliation: Required`; no product code was assessed or changed.

## Deferred Scope

FR-005, FR-006, FR-008, FR-014, and FR-015 were not edited. Product-code, API, database migration, and UI implementation remain outside this documentation update.

## Files Changed

- `project-requirements/functional-requirements/fr004-quote-submission/prd.md`
- `project-requirements/functional-requirements/fr004-quote-submission/change-request-2026-09-09-quote-options-model.md`
- `project-requirements/functional-requirements/fr019-promotions-discounts/prd.md`
- `project-requirements/functional-requirements/fr019-promotions-discounts/change-request-2026-09-10-option-date-promotion-alignment.md`
- `project-requirements/functional-requirements/fr024-treatment-package-management/prd.md`
- `project-requirements/functional-requirements/fr024-treatment-package-management/change-request-2026-09-10-quote-option-provenance-alignment.md`
- `project-requirements/functional-requirements/fr026-app-settings-security/prd.md`
- `project-requirements/functional-requirements/fr026-app-settings-security/change-request-2026-09-10-quote-configuration-ownership.md`
- `project-requirements/system-data-schema.md`
- `project-requirements/update-logs/README.md`

No source code under `main/` was modified.
