# Sprint 1 A-09a Questionnaire Create Bug

**Date:** 2026-06-12  
**Report Type:** Sprint Readiness Report Update  
**Primary Document Updated:** `local-docs/product-plans/2026-05-29/sprint-1-readiness-fix-backlog.md`

## Summary

Recorded confirmed Sprint 1 A-09a defects across questionnaire catalog lifecycle issues and a separate FR-024 admin treatment-wizard mismatch against the PRD ownership/field model.

## What Changed

- Updated the `A-09a - Content & Treatment Management` section in the Sprint 1 readiness backlog.
- Expanded the targeted review note to cover both:
  - Admin Questionnaire Catalog lifecycle behavior against FR-025, and
  - Admin `Add New Treatment` wizard structure against FR-024 field and ownership rules.
- Added a confirmed `Recorded only` defect row for:
  - `Admin Treatment Settings -> Add New Treatment Wizard`
- Added a confirmed `Recorded only` defect row for:
  - `Questionnaire Catalog -> Create New Questionnaire Set`
- Appended a second confirmed `Recorded only` defect row for:
  - `Questionnaire Catalog -> Duplicate Questionnaire Set`
- Appended a third confirmed `Recorded only` defect row for:
  - `Questionnaire Set Detail -> Publish Draft Set`
- Appended a fourth confirmed `Recorded only` defect row for:
  - `Questionnaire Catalog -> Set as Active for Inquiry on Draft Set`
- Appended a fifth confirmed `Recorded only` defect row for:
  - `Questionnaire Catalog -> Archive Questionnaire Set`
- Appended a sixth confirmed `Recorded only` defect row for:
  - `Archived Questionnaire Set -> Recovery / Reuse Lifecycle`

## Finding Captured

- The current Admin `Add New Treatment` wizard is structurally misaligned with FR-024.
- The observed wizard omits treatment fields that the PRD explicitly defines for admin treatment management, while also introducing an admin-side `Packages` step that conflicts with FR-024's provider-owned package model.
- Frontend code evidence confirms this is not just a labeling issue: the wizard state and submit path explicitly couple admin treatment creation with package creation.
- The Admin create-set modal accepts input and closes on `Save`, but no questionnaire-set record is created or persisted.
- Refreshing the page still shows only the existing seeded catalog rows.
- Frontend evidence shows the modal submit handler only closes the modal and the catalog data source is mock-driven.
- Live API verification on 2026-06-12 found the expected FR-025 questionnaire-set list routes returning route-not-found on the deployed backend.
- The Admin duplicate action briefly inserts a copied questionnaire set row and shows a success toast, but the copied row disappears after refresh.
- Frontend evidence shows the duplicate path is also local-state-only: it clones the selected row and prepends it to current rows without any backend mutation or persisted refetch.
- The draft-set publish flow from the detail screen shows success in-session but does not persist after refresh because the detail `publishSet` path is also local-state-only.
- The current catalog `Set as Active for Inquiry` path can incorrectly promote a draft set straight to `Published + Active Inquiry` in-session, which violates the FR-025 requirement that publish and inquiry activation remain separate steps.
- The Admin archive action briefly changes the status to `Archived` in-session, but refresh removes that state because the archive path is also local-state-only.
- PRD review clarified that archived sets should not be directly activated while still archived; instead, FR-025 requires a `Restore as New Draft` recovery path through Version History before re-publish and later inquiry activation.
- Current FE/BE lifecycle surfaces do not provide that PRD-defined archived-set recovery flow.
- The Admin treatment-create wizard also has a separate runtime blocker at submit time: even after the user completes the visible steps, `POST /api/treatment/create-treatment` fails with `422 Unprocessable Content`.
- Screenshot evidence on 2026-06-12 shows toast text `The selected treatment type is invalid. (and 2 more errors)` after submit: `https://s.letweb.net/s/g0oopn`.
- Frontend evidence shows Step 1 exposes only treatment-type values `hair` and `beard`, and the submit path posts `thumbnail` while treating `video` as optional.
- Backend validation instead accepts only `FUE`, `FUT`, `DHI`, `Sapphire FUE`, `Robotic`, and `Other`, and also requires `video` plus an `image[]` array.
- Result: the current admin treatment wizard is not just structurally misaligned with FR-024; it also has no valid FE/BE submission path for creating a treatment in staging.

## Evidence Basis

- Screenshot evidence:
  - `https://s.letweb.net/s/g5xxvp`
  - `https://s.letweb.net/s/e6jjwr`
  - `https://s.letweb.net/s/d7kkwq`
  - `https://s.letweb.net/s/g8yyxj`
  - `https://s.letweb.net/s/e9yy3p`
  - `https://s.letweb.net/s/dqvvq9`
  - `https://s.letweb.net/s/gryyw4`
  - `https://s.letweb.net/s/evqqv3`
  - `https://s.letweb.net/s/dw77qk`
  - `https://s.letweb.net/s/eykkq1`
  - `https://s.letweb.net/s/dz66q4`
  - `https://s.letweb.net/s/g0oopn`
- Code evidence:
  - `main/hairline-frontend/src/pages/teamDashboard/treatments/CreateTreatment.jsx`
  - `main/hairline-frontend/src/components/teamComponents/treatmentComponents/TreatmentStep1.jsx`
  - `main/hairline-frontend/src/pages/teamDashboard/settings/QuestionnaireCatalog.jsx`
  - `main/hairline-frontend/src/pages/teamDashboard/settings/questionnaireCatalog/useQuestionnaireCatalogData.js`
  - `main/hairline-frontend/src/pages/teamDashboard/settings/QuestionnaireSetDetails.jsx`
  - `main/hairline-frontend/src/pages/teamDashboard/settings/questionnaireSetDetails/useQuestionnaireSetDetailsData.js`
  - `main/hairline-frontend/src/pages/teamDashboard/settings/questionnaireSetDetails/mockData.js`
  - `main/hairline-backend/routes/api.php`
  - `main/hairline-backend/app/Http/Controllers/Packages/TreatmentController.php`
  - `main/hairline-backend/app/Http/Controllers/Questionnaire/QuestionnaireSetController.php`
  - `main/hairline-backend/app/Services/QuestionnaireSetService.php`
- Runtime evidence:
  - live API checks against `/api/admin/questionnaire-sets`, `/api/questionnaire-sets`, `/api/questionnaire-sets/test-id/archive`, and `/api/questionnaire-sets/test-id/activate-inquiry` on 2026-06-12

## Follow-up Task Creation

- Created Plane work items for the A-09a FR-024 admin treatment rows and FR-025 questionnaire lifecycle rows, then updated their readiness backlog `Task Status` values from `Recorded only` to `Task created`: `HAIRL-1331`, `HAIRL-1332`, `HAIRL-1333`, `HAIRL-1334`, `HAIRL-1335`, `HAIRL-1336`, `HAIRL-1337`, and `HAIRL-1338`.
