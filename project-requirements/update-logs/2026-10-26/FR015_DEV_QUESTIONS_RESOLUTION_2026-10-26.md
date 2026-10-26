# FR-015 Dev-Team Questions Resolution — 2026-10-26

**Type**: Cross-document alignment (major)
**Trigger**: Two dev-team question documents (2026-10-22): the per-task BE/PM decision list for FR-015 (HAIRL tasks) and the BA questions on the cascade, scheduled changes, and Admin Support Required (Q1–Q14)
**Decisions**: Product Owner via AskUserQuestion, 2026-10-26
**Answer report**: [reports/2026-10-26/fr015-dev-questions-answers-2026-10-26.md](../../../reports/2026-10-26/fr015-dev-questions-answers-2026-10-26.md)

## Documents Changed

| Document | Version | Change |
|---|---|---|
| [FR-015 PRD](../../functional-requirements/fr015-provider-management/prd.md) | 1.20 → 1.21 | New Key Entity 5 Provider Status Event. The Screen 5 Unresolved Support Items count is now one per affected inquiry/case. Suspended providers are read-only on `In Progress` bookings. "Today" means the current UTC date (Screen 4, Tab 7). Login as Provider opens in a new tab and ends on End Session or 30-minute inactivity, with no absolute cap. Screen 2 has a leave-wizard prompt (FR-032 text, no drafts). Added messages for creation success, the empty language list, and the featured cap. Featured set/unset and document Replace need no change reason, and Replace archives the old file. Invalid commission now returns 422 with the PRD wording instead of 400. Updated REQ-015-025, the change log, and approvals. |
| [FR-011 PRD](../../functional-requirements/fr011-aftercare-recovery-management/prd.md) | 1.5 → 1.6 | D4, General Module Rule 4, REQ-011-014 and the mid-aftercare edge case: standalone aftercare is no longer cancelled by provider suspension or deactivation. It gets the provider-status cause and `supportRequired` and moves to Screen 19 reassignment, matching FR-015. |
| [System data schema](../../system-data-schema.md) | 1.11.0 → 1.12.0 | New §41 `provider_status_events` (append-only). The `provider_status_event_id` and `deactivation_event_id` columns now reference it. The §13 standalone-aftercare rule changes from cancel to reassignment, and `standalone_aftercare_requests` needs no `cancelled` value. Table list updated (117). |

## Change Requests

- **Created** [CR-FR011-20261026-01](../../functional-requirements/fr011-aftercare-recovery-management/change-request-2026-10-26-standalone-aftercare-reassignment.md). The standalone-aftercare change reverses the verified FR-011 v1.5 cascade contract (cancel becomes reassign), so it meets the Change Request threshold.
- **Marked partially superseded**: CR-FR011-20261016-01 (standalone cancellation) and CR-FR011-20261014-01 (cancellation of all aftercare cases).
- The PRD header and the v1.6 change log row now cite the new Change Request.

## Product Owner Decisions

1. Provider status event: a dedicated `provider_status_events` table, not the Tab 8 activity-log row.
2. Standalone aftercare: reassign, don't cancel.
3. Booking timing: FR-006 booking-at-acceptance must be implemented before the FR-015 cascade ships.
4. Legacy status values: migrate to the schema values in this release. BE documents the mapping for the FE and Flutter devs.
5. Suspended provider on an `In Progress` booking: read-only. The admin decides via FR-006 B7.
6. Unresolved Support Items: one per affected inquiry/case.
7. "Today" is the UTC date everywhere.
8. Validation errors return 422 with the PRD wording.
9. A draft quote cancelled by suspension is silent to the patient.
10. Login as Provider: opens in a new tab; inactivity timeout only.
11. Document Replace: the old file is archived; no reason required.
12. Featured toggle: no change reason.
13. Leave-wizard prompt: reuses the FR-032 text and is added to the PRD.
14. UI copy for creation success, the featured cap, and the empty language list: approved and added to the PRD.

## Not Changed

- FR-006, FR-020, and FR-032 already match these decisions; no edits were needed.
- FR-015: no Change Request. The FR-015 decisions clarify existing contracts (status event entity, UI copy, timing, validation) and do not reverse an approved contract. CR-FR015-20261016-01 already routes standalone aftercare to admin reassignment.
- Implementation reconciliation is pending.
