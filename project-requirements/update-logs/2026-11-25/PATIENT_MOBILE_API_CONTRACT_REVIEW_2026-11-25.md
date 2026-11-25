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
- Section 5 of the report was checked against the backend route file (read only): of 69 actions, 42 exist, 21 have no route, 6 need the backend team to confirm.

## Owner rulings of 2026-11-25 applied

- **Support chat**: the support request form stays the only route; no patient chat with Hairline support (FR-012 unchanged). The report tells the backend team the app will not call that request.
- **Aftercare contact**: REQ-011-102 confirmed. New rule REQ-011-103 (FR-011 PRD version 1.16): the aftercare team's messages and replies appear in a Messages list on the patient Aftercare Dashboard, with a push and email notification.
- **New notification event** `aftercare.team_message`: FR-030 PRD version 1.30 (REQ-030-295) and the FR-020 mirror row (version 2.21).
- **Push platforms**: iOS and Android only (REQ-020-002, FR-020 PRD version 2.21).
- **Backend extras with no requirement** (delete a notification, active sessions, head-photo monthly summary, price and rating filters) and the `total_offers` number: not required; no requirement added; the app does not use them.
- **Requirements graph**: change-set `changesets/2026-11-25-api-comparison-owner-rulings.yaml`; lint unchanged at 28.
- **Report**: section 5 gains a per-action "exists / to build" check against the backend route files (read only, with the owner's permission).
