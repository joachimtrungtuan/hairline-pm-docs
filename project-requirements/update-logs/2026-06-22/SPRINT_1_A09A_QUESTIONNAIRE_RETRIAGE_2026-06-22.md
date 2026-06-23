# Sprint 1 A-09a Questionnaire Re-triage

**Date:** 2026-06-22  
**Report Type:** Sprint Readiness Report Update  
**Primary Document Updated:** `local-docs/product-plans/2026-05-29/sprint-1-readiness-fix-backlog.md`

## Summary

Re-triaged the Sprint 1 A-09a questionnaire backlog against the current PRD, source code, and live Postman MCP results. The earlier "catalog is still mock-only" picture is no longer accurate as-is: create/list/detail/version/audit endpoints are live, the historical create-persistence defect now has strong evidence of improvement, and the current highest-priority blocker has narrowed to Screen 2 access failures and post-create flow continuity. Existing bug-task rows were intentionally left open pending explicit task-level cross-check instead of being marked `Resolved`.

## What Changed

- Updated the `A-09a - Content & Treatment Management` review notes to reflect current 2026-06-22 evidence instead of the older 2026-06-12 questionnaire lifecycle assumptions.
- Rewrote `A-09A-003` with current evidence showing create persistence now appears fixed in product/source/API, but kept the row under its existing task-created state pending bug-task cross-check.
- Rewrote `A-09A-004` with current evidence showing duplicate no longer appears FE-local in source and was reported as working in the latest manual pass, but kept the row under its existing task-created state pending bug-task cross-check.
- Added `A-09A-009` for the current post-create flow defect: successful create closes the modal but does not transition the admin into Screen 2 question authoring.
- Added `A-09A-010` for the current highest-priority questionnaire blocker: `View` / `Edit` can still land on `Questionnaire set not found` even though the live detail API succeeds for the same set.
- Added a `Scout flagged` row for Version History / Audit Trail data fidelity because base endpoints are live but the frontend currently compresses richer audit metadata into generic display strings.

## Findings Captured

- FR-025 still expects questionnaire-set creation and question authoring to behave as one continuous admin workflow from Screen 1 into Screen 2.
- Current frontend create success only closes the modal and resets local form state; it does not navigate to the newly created set detail route.
- Current frontend catalog navigation and RTK Query wiring match the intended backend detail contract:
  - catalog actions navigate to `/settings/app-settings/questionnaire-catalog/${row.id}`
  - detail fetch uses `GET /settings/questionnaire-sets/{id}`
- Backend detail, version-history, and audit-log reads are live for persisted questionnaire sets:
  - `QuestionnaireSetController@show()` returns `QuestionnaireSetDetailResource`
  - `QuestionnaireSetService@getSetDetail()` uses `findOrFail($setId)` on the live model
  - Postman MCP successfully fetched list, detail, version history, and audit logs for `Sprint1 Inquiry Intake Core A`
- Because the backend succeeds for the same persisted set that the UI can fail to open, the current `Questionnaire set not found` defect is more consistent with frontend routing, stale row state, or wrong ID binding than with a general backend route outage.
- Version History / Audit Trail should remain a focused follow-up after Screen 2 access is fixed because the frontend currently converts some rich audit metadata such as `before` / `after` payloads into coarse text like `Metadata updated`.

## Evidence Basis

- PRD:
  - `local-docs/project-requirements/functional-requirements/fr025-medical-questionnaire-management/prd.md`
- Frontend code:
  - `main/hairline-frontend/src/pages/teamDashboard/settings/QuestionnaireCatalog.jsx`
  - `main/hairline-frontend/src/pages/teamDashboard/settings/questionnaireCatalog/useQuestionnaireCatalogData.js`
  - `main/hairline-frontend/src/pages/teamDashboard/settings/questionnaireCatalog/useVersionHistoryAuditData.js`
  - `main/hairline-frontend/src/features/hairlineTeam/settings/questionnaireCatalogApiSlice.jsx`
- Backend code:
  - `main/hairline-backend/app/Http/Controllers/Questionnaire/QuestionnaireSetController.php`
  - `main/hairline-backend/app/Services/QuestionnaireSetService.php`
  - `main/hairline-backend/app/Http/Resources/QuestionnaireSetDetailResource.php`
- Manual / live evidence:
  - user product review on 2026-06-22
  - `https://s.letweb.net/s/gl99x7`
  - Postman MCP live verification on 2026-06-22 for admin login, questionnaire-set list, detail, versions, and audit logs

## Files Changed

- `local-docs/product-plans/2026-05-29/sprint-1-readiness-fix-backlog.md`
- `local-docs/project-requirements/update-logs/2026-06-22/SPRINT_1_A09A_QUESTIONNAIRE_RETRIAGE_2026-06-22.md`
- `local-docs/project-requirements/update-logs/README.md`
