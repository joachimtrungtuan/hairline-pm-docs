# FR-025 Design Layout Verification

**Date**: 2026-03-23
**Scope**: FR-025 — Medical Questionnaire Management
**Artifact**: `local-docs/reports/2026-03-23/design-layout-verification-fr025.md`
**Type**: Major verification report

## Summary

Completed a full admin-dashboard design-layout verification for FR-025 against the approved PRD and the layout files in `layout-temp/`.

## Key Findings

- Workflow 1 is **blocked** because the supplied layouts do not include a dedicated questionnaire-set catalog (Screen 1) and omit the Context Type Reference screen (Screen 5).
- The delivered `Questionnaire` layouts behave as a question-centric tabbed module rather than the FR's set-level catalog and set-details model.
- Workflow 2 is **blocked** because the Question Editor lacks the required `Detail Prompt (Yes answer)` and `Alert Description` controls for severity-driven inquiry alerts.
- Workflow 4 is **blocked** because there is no design for `Set as Active for Inquiry`, no active-designation badge, and no unconfigured inquiry warning state.
- The strongest-aligned screen is Version History & Audit Trail (Screen 7), which covers most read-only audit fields but still omits snapshot/restore actions.

## Follow-Up Actions

1. Design the missing set-level catalog and inquiry-activation flow before frontend implementation begins.
2. Redesign the set-details page so set metadata, publish controls, and usage context are visible above the question list.
3. Expand the Question Editor to cover severity-alert configuration and patient/provider presentation settings.
4. Add the missing Context Type Reference and dual-view Preview capabilities.

## Traceability

- Requirement source: `local-docs/project-requirements/functional-requirements/fr025-medical-questionnaire-management/prd.md`
- Verification report: `local-docs/reports/2026-03-23/design-layout-verification-fr025.md`
