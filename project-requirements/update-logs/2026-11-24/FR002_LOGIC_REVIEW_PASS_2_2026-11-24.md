# FR-002 Logic Review Pass 2 (2026-11-24)

**Scope**: FR-002 Medical History and 3D Scanning, PRD v1.6 to v1.7. Pass 2 of 2 of the logic review; 15 new findings, 14 fixed in FR-002, 1 left to the backlog. The seven partly fixed items of pass 1 are closed by the same fixes.
**Evidence**: reviewer report `plans/reports/tester-261124-fr002-logic-p2.md`; fixer report `plans/reports/docs-manager-261124-fr002-logic-p2-fixes.md`.
**Graph**: the change-set `local-docs/project-requirements/graph/changesets/2026-11-24-fr002-logic-p2-fixes.yaml` is prepared and NOT applied (the controller applies it).
**Owner default**: entry 76 in `plans/reports/owner-review-261123-1308-phase-10-defaults-applied.md` (provider media link lifetime and who keeps access).

## Changes to the PRD

- Audit scope: submit attempts (accepted and rejected) and media-only calls are audited; the derive-only and read calls write no audit entry. The A3 outcome now says no artifacts are persisted and an audit entry records the rejection (REQ-002-010, REQ-002-026).
- `alertTier` added to the submit and derive-only responses and to the stored result; `alerts` is required and never empty. Risk tag code is the questionId and label the question text; a Yes on a No Alert question produces no tag; "risk-tag rules" replaced by "severity flags" (REQ-002-002, REQ-002-004, REQ-002-019).
- Version check first, then validation of the answers and photos on every path including a prior version; no photo added to the A1 trigger; both error lists returned together. Any version that is or was designated Active for Inquiry is accepted; every other version is TEMPLATE_VERSION_UNKNOWN (REQ-002-037, new REQ-002-052).
- Landing per error code: questionnaire, reload of the Active set with the draft kept, or a submission-unavailable message with the draft kept (new REQ-002-053).
- processingId for every submit attempt, error item shape, set id in the audit entry (REQ-002-052).
- Idempotency key is the FR-003 draft id (the scan id for media-only calls); an identical retry returns the first result and a changed retry supersedes the earlier set, which is archived (REQ-002-045).
- Staging: keyed by draft id, readable only by the uploading patient and the engine, removed by S-05 on a schedule (new REQ-002-051, new Workflow 6); REQ-002-017 now says passive after processing except scheduled staging clean-up.
- Provider copy made by S-01 at promotion, returned as `providerCopyUri`; `storedUri` never sent to providers (REQ-002-048).
- Provider media link lives 15 minutes and is issued by the read call on each authorised open; access ends for providers who declined or were not selected once a quote is accepted and for everybody at inquiry cancellation; the booked provider keeps access while the booking is active (REQ-002-049, default 76).
- A photo item may be a stagedRef or an existing scanRef with photoIndex; a stored scan is copied, never moved or replaced (REQ-002-038).
- New Workflow 5 (media-only call) so REQ-002-047 has steps; Workflow 2 order is now read, build views, distribute, consume.
- Not changed in the PRD: the quality score definition (the lower of the brightness and blur scores, one FR-026 minimum per measure); it is a backlog item.

## Graph change-set (prepared, not applied)

- 9 new nodes (3 rules REQ-002-051 to REQ-002-053, 4 steps STP-002-026 to STP-002-029, 2 flows), 4 new fields, 39 node updates, 1 field update, 3 enum values, 7 edges removed, 67 edges added.
- Stage edges added for REQ-002-047 (aftercare, monitoring), REQ-002-043 and REQ-002-049 (quote, acceptance, booking).
- Steps added for the version-then-validation branch point, the media-only call and the staging clean-up; STP-002-011 now rejoins through the validation step.

## Cross-FR rows queued

FR-003, FR-011, FR-037, FR-025, FR-026 and FR-005: see the pass 2 section of `plans/reports/logic-review-ledger.md`.

## Follow-up (same day)

- REQ-002-038 and REQ-002-036: a scanRef photo item is accepted only for a scan stored under the same anonymizedPatientId as the request; otherwise the attempt is rejected with MEDIA_REF_NOT_OWNED and audited. Graph change-set `2026-11-24-fr002-scanref-ownership.yaml`.
