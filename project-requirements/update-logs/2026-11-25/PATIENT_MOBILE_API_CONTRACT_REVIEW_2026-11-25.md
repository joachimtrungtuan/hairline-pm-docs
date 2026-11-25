# Patient mobile API contract review

**Date**: 2026-11-25
**Type**: Major (cross-document alignment, new report, developer guide section)

## What changed

- **New report** `reports/2026-11-25/patient-mobile-api-contract-vs-requirements-2026-11-25.md` for the backend API team: the Postman collection `PATIENT-MOBILE-handoff` (96 requests) compared with the FR PRDs and the requirements graph. It states the freeze rule (correct by adding), seven differences that need an agreed decision, corrections that do not break the app, patient actions with no request, and the list of the 96 requests.
- **`DEVELOPER-GUIDE.md`**: new section 9, "Patient mobile API: endpoints to keep stable", for developers reworking the backend.
- **Three inconsistencies inside the PRDs settled** (found during the comparison):
  - FR-006 PRD (version 2.25): Screen 1 Payment Option row listed two options; it now lists the three of REQ-007-098 (full payment, deposit and balance, installments 2 to 9).
  - FR-011 PRD (version 1.15): new rule REQ-011-102. Contact Support on the patient Aftercare Dashboard sends a text message to the aftercare team, recorded as an aftercare communication entry; it is not an FR-012 conversation.
  - FR-012 PRD (version 2.19): the out-of-scope notes now say where the patient goes today for support help (FR-035 and FR-034) and for the aftercare team (REQ-011-102).
- **Requirements graph**: change-set `changesets/2026-11-25-api-comparison-doc-fixes.yaml` (REQ-012-030 statement updated, REQ-011-102 added with its edges).

## Checks

- Graph lint unchanged at 28; export regenerated.
- Every rule id cited in the report resolves in the graph.
- The backend source code was not read; the report says so.

## Open

- How the aftercare team's reply reaches the patient is not yet defined (REQ-011-102 covers the patient's message only).
- Product owner decisions pending: patient chat with support; requests with no requirement (delete a notification, active sessions, head-photo monthly summary, price and rating filters).
