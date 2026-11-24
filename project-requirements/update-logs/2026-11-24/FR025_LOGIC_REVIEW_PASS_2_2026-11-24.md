# FR-025 logic review pass 2 - 2026-11-24

**Scope**: FR-025 Medical Questionnaire Management, PRD v2.6 to v2.7, and one prepared graph change-set. Last pass for this FR.
**Source**: `plans/reports/tester-261124-fr025-logic-p2.md` (16 findings, all accepted); per-finding detail in `plans/reports/docs-manager-261124-fr025-logic-p2-fixes.md`.
**Graph**: `local-docs/project-requirements/graph/changesets/2026-11-24-fr025-logic-p2-fixes.yaml` is prepared and test-applied on a scratch copy of `graph.db`; it is NOT applied to the live graph.
**Owner defaults taken**: 105 (archive discards the open Draft), 106 (category deleted only when no set at all is assigned), 107 (audit entries of a deleted set kept, no screen at launch).

## Changes in the PRD

- Workflow 1: a Draft or Archived set can be opened from the catalog; a question can be edited without re-choosing the type; the save box says an incomplete question is saved and keeps its status; the publish check and block cover the inactive category; the archive bullet says the open Draft is discarded and the confirmation warns of it.
- Archive and restore (REQ-025-045, REQ-025-038): archiving discards the open Draft; a restored set comes back as a new Draft built from the selected version, without the Inquiry designation and without the earlier draft, shows status Draft until published, and is Active again when published.
- Set as Active for Inquiry (REQ-025-051, REQ-025-050): hidden on the set that already carries the designation; every inquiry started after the change uses the new set, a resumed draft keeps its version (also REQ-025-056).
- Categories (REQ-025-028): delete only when no set of any status is assigned, otherwise deactivate.
- Delete a set (REQ-025-046): audit entries of a deleted set stay in storage and have no screen at launch.
- Save and publish (REQ-025-024): Save accepts an incomplete question; publish lists it.

## Changes in the graph change-set

- Step wiring: open a Draft or Archived set, restore of an Archived set, Set as Active for Inquiry from the catalog, publish cancel exit with exclusive branches, archive path through the archive rules with exclusive outcomes, edit of an existing question for every set type.
- Rule wiring: unfit Context Type and inactive category are applied by the publish steps; REQ-025-084 and REQ-025-017 are anchored at the inquiry stage again with one applying step each; REQ-025-066 no longer applies to the preview screen.
- Stage data flow: questionnaire writers and the publish event on the configuration stage; the stale FR-025 writes and emits removed from the inquiry, aftercare and monitoring stages.
- Statements and titles of REQ-025-024, 028, 038, 045, 046, 050, 051, 056 and the question status field description brought in step with the PRD.

## Open

- Applying the change-set to the live graph and regenerating the exports is a controller step.
