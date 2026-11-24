# FR-025 Logic Review Pass 1 (2026-11-24)

**Scope**: FR-025 Medical Questionnaire Management, PRD v2.5 to v2.6. Pass 1 of the logic review; 21 findings, all fixed on the FR-025 side, with the neighbour halves queued to FR-003 and FR-011.
**Evidence**: reviewer report `plans/reports/tester-261124-fr025-logic-p1.md`; fixer report `plans/reports/docs-manager-261124-fr025-logic-p1-fixes.md`.
**Graph**: the change-set `local-docs/project-requirements/graph/changesets/2026-11-24-fr025-logic-p1-fixes.yaml` is prepared and NOT applied (the controller applies, lints, exports and commits).
**Owner defaults**: P1-05 (94, a designation history kept on the version) and P1-08 (95, a milestone-assigned set cannot be archived). Rulings from the controller settled the other findings.

## Changes to the PRD

- The alert tier is computed by the FR-002 engine (REQ-002-002); FR-025 owns only the mapping from Severity Flag to tier. Workflow 2 and 3 boxes, REQ-025-063, 064 and 065 and the Provider Platform Integration lines now point to the engine. Green means no Yes answer on a Critical or Standard question (REQ-025-064).
- Preview colours each answer by its own severity flag and shows no overall tier; Alert Description is an optional Admin-only note shown in the editor and Preview, and providers see the question text (REQ-025-017).
- Publishing archives the previous Active version as a version-level event; the Inquiry designation belongs to the set and carries over; REQ-025-048 applies only to the Archive action on the set (REQ-025-031, 048). Screen 7 gains the read-only field Was Designated for Inquiry, and REQ-025-057 accepts a submission on an older version that is or was designated.
- A patient starting gets the current designated version; a resumed draft keeps its version; the version is recorded at submit. No designated set blocks every submission, resumed drafts included, keeps the draft and shows the submission-unavailable message (REQ-025-052, 053, 057, 058).
- Context Type is read-only on the Active version and editable only in an open Draft; publish is blocked with the list of uses when the type no longer fits (REQ-025-033).
- Archive and delete: a designated set can only be archived; a milestone-assigned set can be neither deleted nor archived until reassigned; Archived is terminal (Restore as New Draft, then publish); Delete only for a never-published set with no usages (REQ-025-045, 046). Category deletion needs the sets reassigned first (REQ-025-028).
- Inactive, soft-deleted and hidden questions: new REQ-025-084; status `Deleted` for a soft-deleted question; Visible to Patient is not offered in Inquiry or Multi-Context sets.
- Every change to an Active set goes to its single open Draft; Restore is refused while one exists; a stale save is refused with a reload message; the control is hidden or filtered and the block message appears only for a stale screen (REQ-025-032, 038, 051, 073).
- Every Multi-Context set may be assigned to a milestone, no flag; a draft response keeps its version (REQ-025-071, 072).
- Audit: five new action types, session ID on Screen 7, category changes in the platform Admin audit log (FR-031, REQ-031-008), milestone audit left to FR-011; Screen 7 holds Admin actions only, the answers and tier belong to the inquiry record (FR-003) and the version to the FR-002 intake audit entry (REQ-025-041, 043, 059).
- Publish confirmation after validation shows the new version number and changes summary; the button is Publish; the copy is named `<source name> (copy)` and made unique before the first save (REQ-025-034, 008).
- Workflow 1 gains one line each for category management, version history and Restore, archive and delete. Change Log row added.

## Graph change-set (prepared, not applied)

- 309 operations: 2 new fields (`ENT-questionnaire-version.was_inquiry_designated`, `ENT-questionnaire-audit-entry.session_id`), 6 enum values, 6 new nodes (REQ-025-084 and steps STP-025-056 to 060), 128 edges added, 131 removed (mostly the stage moves), 36 node updates (28 rules, 8 steps).
- Seven screens, the admin rules and the unconfigured event moved to STG-admin-01-configuration; the patient order is now submit, record version, alert, log.
- Test-applied on a scratch copy of the graph (applied cleanly, 355 change rows); the scratch copy was deleted. Lint and export were not run.

## Cross-FR rows queued

FR-003 (wording of STP-003-010 and STP-003-056), FR-011 (REQ-011-071 wording, a version field on the aftercare response, audit of milestone assignment); see the FR-025 section of `plans/reports/logic-review-ledger.md`.
