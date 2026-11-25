# Backlog clean-up and handover gaps closed

**Date**: 2026-11-25 (Asia/Saigon)
**Type**: Major update (cross-document alignment of the FR PRDs, the requirements graph and the developer guide; one new Draft PRD). No Change Request (requirements graph programme: new baseline).

## What changed

### Open-points backlog settled

`implementation-backlog.md` held 507 open points. Each was checked against the live PRDs and the graph.

| Result | Points | What was done |
|---|---|---|
| Already settled | 264 | Removed from the backlog; evidence kept in the working records |
| Filing or wording fix | 125 | Applied in the FR PRD and the graph, one commit per FR (`docs(fr-NNN): settle backlog filing points`) |
| Business decision | 83 | Nothing changed; listed for the Product Owner |
| Developer matter | 30 | Kept in the backlog |
| Fix owed in another FR document | 5 | 2 applied (`f3ae887`), 3 kept in the backlog |

Every edited PRD has a change-log row dated 2026-11-25 that begins "Backlog points settled:". The cross-FR pass (`f3ae887`, `daac290`) also added REQ-007-103 (the booking stores the balance due date and the FR-029 values locked at confirmation), aligned the FR-009 role-change timing with REQ-009-014, named FR-001 Screen 14 in REQ-026-112, and completed the Dependencies sections of FR-003, FR-012, FR-017 and FR-024.

`implementation-backlog.md` was rewritten. It now holds 131 points in four sections: waiting for a Product Owner decision (83), developer matters (30), fixes owed in another FR document (3), housekeeping of the graph and documents (15). The `[Bnnn]` tags are line numbers in the earlier version of the file.

### Handover gaps closed

- FR-037 and FR-038 are built with the clinical release (launch Phase 2), by Product Owner decision.
- `baseline-sign-off.md` is the one approval record: the Product Owner approved all requirement documents as they stood on 2026-11-25. Each PRD approval section points to it.
- `DEVELOPER-GUIDE.md` carries a short build-order summary, no longer names the API collection by file name, and describes the cleaned backlog and the constitution open items as developer choices.
- The eight unconnected hand-offs between FRs were connected in the graph.
- FR-023 and FR-025 received their missing standard sections (`2df2371`, `d377429`).
- `templates/prd-template.md` follows the constitution section list (`9102947`).

### FR-036 Draft PRD

`functional-requirements/fr036-admin-profile-settings/prd.md` was written from the FR-036 summary in `system-prd.md` (`1b5962e`): 15 rules, 4 screens, 7 flows. Status is Draft, version 0.1. It is not covered by the sign-off. Nine points the summary does not decide read "Not yet decided" and are listed in the PRD as open questions. The Notification Preferences screen and the timezone field are not in the graph until those questions are answered.

## Graph

One change-set per FR under `graph/changesets/2026-11-25-backlog-settle-frNNN.yaml`, plus `2026-11-25-backlog-settle-frmisc.yaml`, `2026-11-25-backlog-settle-frmisc-source.yaml` and `2026-11-25-fr036-draft-prd.yaml`. Lint stays at 24 findings (L17 x14, L12 x8, L03 x1, L09 x1).

## Open

- 95 questions wait for the Product Owner: 86 from the backlog and 9 from the FR-036 Draft. The list is a working record kept outside this repository.
- FR-036 needs Product Owner approval before it is built.
