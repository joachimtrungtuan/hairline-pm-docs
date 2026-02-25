# FR-025 Medical Questionnaire Management — Verification Updates

**Date**: 2026-02-25
**Triggered By**: FR-025 verification (verify-fr skill)
**Files Modified**: `fr025-medical-questionnaire-management/prd.md`, `system-prd.md`

---

## Summary

FR-025 was verified against the constitution, system PRD, and client transcriptions. Seven issues were identified; all resolved in this update.

---

## Changes to FR-025 PRD

### 1. Inquiry Question Type Constraint — Soft Warning (was Critical → resolved)

**Before**: Context Type table stated "Yes/No only" for Inquiry; Business Rule said "publish warning" — contradiction.
**After**: Inquiry context recommends Yes/No questions. If admin adds non-Yes/No questions to an Inquiry set, the system displays a warning at publish time. Admin may confirm and proceed. Not a hard block.

**Rationale**: Inquiry questionnaires are primarily Yes/No for medical screening, but the system should not hard-code this restriction to allow future flexibility.

### 2. Visual Scale 1–5 Removed — Replaced by Visual Scale 1–10 (was Medium → resolved)

**Before**: System-defined types included both "Visual Scale 1–5" and (after initial fix) "Visual Scale 1–10".
**After**: Only "Visual Scale 1–10" exists. Final type list: Yes/No, Visual Scale 1–10, Numeric Scale 1–10, Multi-select, Free Text.

**Rationale**: The agreed scale is 10-point. The 5-point variant was never confirmed. Aligns with FR-011's "Visual scale (1-10)" for pain assessment.

### 3. FR-002 Dependency Removed (was Medium → resolved)

**Before**: FR-002 (Medical History & 3D Scanning) listed as internal dependency with "medical data integration".
**After**: Removed. No actual data flow or integration point exists between FR-025 and FR-002.

### 4. FR-020 Alert Event Integration Note Added (was Minor → resolved)

**Before**: FR-020 listed as dependency but no integration detail in business rules.
**After**: Added to Provider Platform Integration rules: "FR-025 generates structured alert events (containing inquiry ID, alert level, triggering question IDs, and response summary) that are published to FR-020's notification engine for delivery to providers via their configured notification channels."

---

## Changes to System PRD (`system-prd.md`)

### 5. Bulk Operations Deferred to V2

**Before**: `Admin MUST be able to import/export questionnaire templates`
**After**: `Admin SHOULD be able to import/export questionnaire templates — deferred to V2; not requested by client in transcriptions`

**Evidence**: Searched all 7 transcription files for "import", "export", "bulk", "csv", "json", "spreadsheet" — no client mention of questionnaire import/export.

### 6. Question Templates Deferred to V2

**Before**: `System MUST provide pre-built question templates for common medical conditions`
**After**: `System SHOULD provide pre-built question templates for common medical conditions — deferred to V2; not requested by client in transcriptions`

**Evidence**: Searched all 7 transcription files for "template", "pre-built", "pre-made", "starter", "seed", "default question" — all "template" matches refer to aftercare templates or email templates, not questionnaire question templates.

### 7. Question Grouping Aligned to Set-Level Categorisation

**Before**: `Admin MUST be able to organize questions into categories (Allergies, Cardiovascular, etc.)`
**After**: `Admin MUST be able to organise questionnaire sets into categories (Allergies, Cardiovascular, etc.) for catalog filtering — categories apply at the set level, not individual question level (per FR-025 PRD)`

**Rationale**: Question-level categorisation within a set is not practical. FR-025 PRD implements categories at the set level (Screen 4: Category Management), which is the correct granularity.

### 8. Question Types Updated

**Before**: `question type (Yes/No)`
**After**: Full system-defined type list (Yes/No, Visual Scale 1–10, Numeric Scale 1–10, Multi-select, Free Text) with note that Inquiry context recommends Yes/No but allows other types after admin confirms warning.

---

## Verification Outcome

| Check | Result |
|-------|--------|
| Constitution Compliance | Pass |
| Client Alignment | Pass — all transcription requirements traced |
| Screen Field Provenance | Pass — all 7 screens verified |
| Dependency Integrity | Pass (after fixes) |
| Cross-Document Consistency | Pass (after system PRD alignment) |
