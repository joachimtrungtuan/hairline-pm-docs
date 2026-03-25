# Aftercare FR-010 / FR-011 Relationship Audit

**Date**: 2026-03-24
**Type**: Design layout verification follow-up
**Scope**: Cross-check the current Aftercare-related mobile layouts against FR-011 patient flows, the FR-010 treatment-completion handoff, and the mobile complement flows `P05.1` to `P05.3`
**Source Spec**: `local-docs/project-requirements/functional-requirements/fr011-aftercare-recovery-management/prd.md`, `local-docs/project-requirements/functional-requirements/fr010-treatment-execution/prd.md`, `local-docs/reports/2026-02-05/missing-mobile-flows-design-complement.md`
**Platform**: Patient Mobile App

## Summary

Created a broader Aftercare relationship audit that maps the current layout set across `layout-temp/aftercare/`, `layout-temp/in progress/`, and `layout-temp/reviews/` back to the approved FR sources and the mobile complement report.

## Outputs Created

- `local-docs/reports/2026-03-24/design-layout-verification-fr011-patient-mobile.md` *(renamed on 2026-03-25 after the report was narrowed to FR-011 patient mobile scope only)*

## Verification Outcome

- Flow verdicts: `FR011-W2 🔴 BLOCKED`, `FR011-W2b 🔴 BLOCKED`, `FR011-W3 🔴 BLOCKED`, `P05.1 🔴 BLOCKED`, `P05.2 🟢 COMPLETE`, `P05.3 🟡 PARTIAL`
- Screen coverage: `14 / 15` specified screens with mapped layouts
- Key blockers:
  - FR-011 checkout screens still lack billing-address and card-entry coverage
  - FR-011 questionnaire and educational-resource screens omit required metadata/progress fields
  - `P05.1-S2 Day Details Popup` has no mapped layout
  - `P05.3-S1` introduces an off-spec `Submitted` review status

## Key Findings

- The current Aftercare layouts are not confined to `layout-temp/aftercare/`; the strongest mappings for `P05.1` and `P05.2` are in `layout-temp/in progress/`, and `P05.3` is implemented in `layout-temp/reviews/`
- `FR-011` purchase and activity flows are only partially represented by the current design set and still contain implementation-blocking gaps
- `P05.2 Previous Treatments List` is the only fully design-ready flow in the broader Aftercare relationship audit

## Impact

- The Aftercare design set should not be treated as fully aligned to the approved specs yet
- Any implementation that depends on FR-011 checkout, questionnaire, or educational-resource flows still needs either design completion or explicit spec/design reconciliation
- The new report should be used as the current source of truth for answering “which Aftercare screens map to which FR/report source?”
