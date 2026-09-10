# FR-004 and FR-010 Verification Resolution

**Date**: 2026-09-10
**Type**: Approved verification follow-up and cross-FR contract reconciliation
**Scope**: FR-004 v2.5, FR-010 v2.0, CR-FR004-20260909-01, CR-FR010-20260910-01, system PRD, and system data schema
**Trigger**: Product Owner selection of the four resolution paths from the FR-004 v2.4 verification report

---

## Summary

The approved corrections preserve the FR-004 parent-and-options aggregate while removing four ambiguities: duplicated technique ownership, stale non-deferred dependencies, inconsistent Quote lifecycle labels, and incomplete verification-layer coverage. No deferred reconciliation was performed for FR-005, FR-006, FR-008, FR-014, or FR-015.

## Changes Applied

### 1. Technique remains Treatment-owned

FR-004 now records the exact immutable Treatment ID/version relationship. Treatment name, type, and technique details are loaded read-only through that relationship; optional FR-024 technique specifications display when documented and are not separate provider input or copied onto Quote. The system PRD and schema document the same ownership.

### 2. Non-deferred dependencies aligned

- Removed FR-038 from FR-004 restricted-recipient handling because FR-038 is self-service and converts only to FR-011.
- Updated FR-010 to consume the stable accepted Quote Option, its package snapshot, and its relative `QuoteOptionPlanDay` records instead of singular `packageId` or quote-level `plan` fields.
- Added approved Change Request CR-FR010-20260910-01; implementation reconciliation remains required.

### 3. Quote lifecycle terminology normalized

FR-004 workflows now use `accepted` for acceptance and `withdrawn` for provider withdrawal. Booking remains a downstream stage rather than an alternative Quote status.

### 4. Verification matrix added

FR-004 now defines the Constitution-required unit, integration, contract, end-to-end, security, and performance coverage, including minimum evidence for the aggregate, tenant boundaries, APIs, lifecycle, and audit behavior.

## Deferred Scope

FR-005, FR-006, FR-008, FR-014, and FR-015 remain intentionally untouched for later reconciliation. Product-code, API, database migration, and UI implementation were also outside this documentation update.

## Files Changed

- `project-requirements/functional-requirements/fr004-quote-submission/prd.md`
- `project-requirements/functional-requirements/fr004-quote-submission/change-request-2026-09-09-quote-options-model.md`
- `project-requirements/functional-requirements/fr010-treatment-execution/prd.md`
- `project-requirements/functional-requirements/fr010-treatment-execution/change-request-2026-09-10-quote-option-consumer-alignment.md`
- `project-requirements/system-prd.md`
- `project-requirements/system-data-schema.md`
- `project-requirements/update-logs/README.md`

No source code under `main/` was modified.
