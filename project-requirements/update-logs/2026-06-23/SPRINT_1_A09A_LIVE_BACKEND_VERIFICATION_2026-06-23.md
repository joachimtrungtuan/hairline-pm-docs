# Sprint 1 A-09a Live Backend Verification

**Date:** 2026-06-23  
**Report Type:** Sprint Readiness Report Update  
**Primary Document Updated:** `local-docs/product-plans/2026-05-29/sprint-1-readiness-fix-backlog.md`

## Summary

Updated the Sprint 1 A-09a questionnaire backlog after a deeper live backend verification pass. This pass confirms that the questionnaire catalog is no longer just "partially real" in a vague sense: the live backend now serves questionnaire-set list/detail, category picker, context-type reference, version-history, and audit-log data. The highest-priority current failures are therefore frontend continuity/access problems around Screen 2, not a broad backend outage or a fully mocked questionnaire module.

## What Changed

- Refreshed the `A-09a - Content & Treatment Management` review notes with 2026-06-23 live backend evidence.
- Strengthened `A-09A-009` with confirmation that the create modal is fed by real backend category/context data, while the post-save UX still stops on Screen 1.
- Strengthened `A-09A-010` with direct live verification that the same set ID shown in the failing UI route (`d131620f-44bf-49bc-b7e1-153a8e1171c8`) exists in the live catalog and returns a valid detail payload from the backend.
- Reframed the Version History / Audit Trail scouting row so it now clearly distinguishes "real but sparse backend data" from "mock data": current draft sets have empty version arrays because they have not been published yet, and they each expose one real `create_set` audit row with timestamp and IP.
- Added explicit blocked-follow-up handling so the report now says the remaining Screen 2-dependent questionnaire lifecycle checks should be deferred until `A-09A-010` is fixed, and preserved that re-test work as a `Review pending` checkpoint row.
- Same-day tasking addendum: created Plane work items `HAIRL-1378` for `A-09A-009` and `HAIRL-1379` for `A-09A-010` from `implementation-tasks-2026-06-23-002.md`, then updated the sprint backlog `Task Status` cells from `Recorded only` to `Task created (FE: ...)`.

## Findings Captured

- Live backend catalog currently returns two persisted draft inquiry sets:
  - `Sprint1 Inquiry Intake Core B` (`d131620f-44bf-49bc-b7e1-153a8e1171c8`) in category `Chronic Conditions`
  - `Sprint1 Inquiry Intake Core A` (`e661fac2-c710-48f5-8b93-9f87cd7d809f`) in category `General Health`
- `active_inquiry_set_id` is currently `null`, which matches the warning banner shown in the catalog UI and the user report that no inquiry set is active.
- Category Management is backed by live data, including persisted Active/Inactive status and total-set counts.
- The create form category picker and context-type picker are also live-backed.
- Context Type Reference is correctly read-only and currently returns backend-defined integration metadata for `Inquiry`, `Aftercare`, and `Multi-Context`.
- Version History / Audit Trail is backed by live endpoints, but current persisted sets are still draft-only:
  - version arrays are empty
  - audit logs contain one real `create_set` row per set
  - current audit rows include timestamp and IP `86.48.10.218`
- Because the backend succeeds for the exact same set ID that the UI can fail to open, the current `Questionnaire set not found` behavior is best recorded as a frontend access/state issue until contrary runtime evidence appears.

## Evidence Basis

- PRD:
  - `local-docs/project-requirements/functional-requirements/fr025-medical-questionnaire-management/prd.md`
- Frontend code:
  - `main/hairline-frontend/src/pages/teamDashboard/settings/QuestionnaireCatalog.jsx`
  - `main/hairline-frontend/src/pages/teamDashboard/settings/questionnaireCatalog/useVersionHistoryAuditData.js`
  - `main/hairline-frontend/src/features/hairlineTeam/settings/questionnaireCatalogApiSlice.jsx`
- Backend code:
  - `main/hairline-backend/routes/api.php`
  - `main/hairline-backend/app/Http/Controllers/Questionnaire/QuestionnaireSetController.php`
  - `main/hairline-backend/app/Services/QuestionnaireSetService.php`
- Manual / live evidence:
  - user product review on 2026-06-22
  - `https://s.letweb.net/s/dkmmx3`
  - `https://s.letweb.net/s/gl99x7`
  - `https://s.letweb.net/s/ejnn33`
  - live backend API verification on 2026-06-23 for admin login, questionnaire-set list/detail, version history, audit logs, categories, category picker, context types, and context-type picker

## Files Changed

- `local-docs/product-plans/2026-05-29/sprint-1-readiness-fix-backlog.md`
- `local-docs/project-requirements/update-logs/2026-06-23/SPRINT_1_A09A_LIVE_BACKEND_VERIFICATION_2026-06-23.md`
- `local-docs/project-requirements/update-logs/README.md`
