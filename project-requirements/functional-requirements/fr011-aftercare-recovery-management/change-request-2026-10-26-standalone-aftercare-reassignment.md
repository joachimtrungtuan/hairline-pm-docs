# Change Request: Standalone Aftercare Reassignment on Provider Suspension or Deactivation

**Change Request ID**: CR-FR011-20261026-01
**Primary FR**: FR-011
**Triggering FR / Event**: FR-015 dev-team question resolution (BA question Q4), Product Owner decision 2026-10-26; aligns FR-011 with FR-015 v1.20/v1.21 A5 and CR-FR015-20261016-01
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-26
**Decision Date**: 2026-10-26
**PRD Version Change**: v1.5 to v1.6
**Related Commit(s)**: Pending

---

## Decision Summary

The Product Owner decided that a provider suspension or deactivation does **not** cancel that provider's standalone aftercare cases. Like treatment-linked cases, they keep their status, get the provider-status cause and `supportRequired`, and are reassigned by an admin on Screen 19.

The FR-011 v1.5 rule, from CR-FR011-20261016-01, still cancelled standalone cases. That conflicted with FR-015, where standalone cases already go to admin reassignment, and with the system data schema §13. The dev team raised the conflict as Q4.

## Baseline State

**Source version**: FR-011 v1.5. The rule appears in Workflow 4 (Admin Aftercare Management) D4, General Module Rule 4, REQ-011-014, and the Edge Cases entry for a provider suspended mid-aftercare.

On an effective provider suspension or deactivation:
- standalone aftercare cases were cancelled, with cause `ProviderSuspended` or `ProviderDeactivated` and `supportRequired`;
- treatment-linked cases stayed active and were reassigned on Screen 19.

The schema §13 rule matched this cancellation, and the standalone intake status was expected to need a `cancelled` value.

## Approved State

**Target version**: FR-011 v1.6, same headings.

- On an effective suspension or deactivation, **every** non-terminal aftercare case of the provider stays in its current status. This covers both standalone and treatment-linked cases. Each case records the cause (`ProviderSuspended` or `ProviderDeactivated`), the provider-status event, and `supportRequired`.
- An admin reassigns the case on [Screen 19: Reassign Aftercare Provider (Admin)](prd.md). The reason, confirmation, audit and `aftercare.provider_reassigned` notice rules are unchanged from v1.5.
- The `after_cares` row is the source of truth for the case. The standalone intake record (`standalone_aftercare_requests`) does not need a `cancelled` value.
- A later deactivation does not overwrite an earlier `ProviderSuspended` cause, and reactivation does not reassign the case automatically. Both rules are unchanged.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Standalone aftercare on provider suspension or deactivation (D4, Rule 4, REQ-011-014, Edge Cases) | Cancelled with the cause and `supportRequired` | Not cancelled; status kept, with the cause, the status event and `supportRequired`; reassigned on Screen 19 | Matches FR-015 A5; the patient's recovery continues with a new provider instead of ending |
| Standalone aftercare status values | Cancellation expected on the case and the intake request | No `cancelled` value needed on `standalone_aftercare_requests`; the case status is kept | Reassignment replaces cancellation |
| Data model (schema §13) | Standalone cases cancelled by the cascade | Standalone cases follow the treatment-linked reassignment rule; `provider_status_event_id` references `provider_status_events` (§41) | Schema v1.12.0 alignment |

## Scope and Impact

### In Scope

- What the provider-status cascade does to standalone aftercare cases in FR-011, and the matching rule in the data schema.

### Out of Scope

- The Screen 19 reassignment fields, validation, notices and audit, which are unchanged from v1.5.
- Treatment-linked aftercare behaviour, which is unchanged.
- Refunds or money movement, which follow the FR-006 payment placeholder.

### Affected Contracts

- **PRD owner**: `project-requirements/functional-requirements/fr011-aftercare-recovery-management/prd.md`: Workflow 4 D4, General Module Rule 4, REQ-011-014, Edge Cases.
- **Related FRs**:
  - FR-015 (A5 and Screen 4) already routes standalone cases to admin reassignment, so no change is needed there.
  - FR-016 lists the case under Admin Support Required.
  - FR-020 sends the per-case admin alert `provider.status_cancellation_admin_support`.
- **System documents**: `system-data-schema.md` v1.12.0, §13 `after_cares` standalone rule and §41 `provider_status_events`.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed. The backend currently keeps standalone intake in `standalone_aftercare_requests` (pending, assigned, active, completed, rejected), linked to `after_care_id`.
- **Required assessment**:
  - The cascade job's handling of standalone cases.
  - Admin Support Required listing.
  - Screen 19 entry for standalone cases.
  - Provider read-only access after suspension.
  - Tests.
- **Compatibility / rollout risk**: Standalone cases cancelled under the old rule would need an admin review. The current backend is a dev/test environment with no production data, so none are expected.
- **Data migration**: None expected.

## Acceptance and Validation

- When a provider with an active standalone aftercare case is suspended:
  - the case keeps its status;
  - the cause, the status event and `supportRequired` are recorded;
  - the case appears in the FR-016 Admin Support Required list.
- An admin can reassign the standalone case on Screen 19, and the patient and the new provider receive `aftercare.provider_reassigned`.
- The suspended provider can view the case but cannot act on it.
- No standalone aftercare case or intake request is set to `cancelled` by the provider-status cascade.

## Approval and Traceability

- **Requested by**: Dev team, via `FR015-BA-QUESTIONS-2026-10-22.md` Q4.
- **Approved by**: Product Owner, Joachim Trung Tuan, 2026-10-26.
- **Decision evidence**: [FR-015 dev-team questions answer report](../../../reports/2026-10-26/fr015-dev-questions-answers-2026-10-26.md), §1.5 and Q4.
- **PRD change log**: [FR-011 Appendix: Change Log](prd.md#appendix-change-log), v1.6 dated 2026-10-26.
- **Update log**: [FR015_DEV_QUESTIONS_RESOLUTION_2026-10-26.md](../../update-logs/2026-10-26/FR015_DEV_QUESTIONS_RESOLUTION_2026-10-26.md).
- **Supersedes**: CR-FR011-20261016-01 in part (cancellation of standalone aftercare cases on provider suspension or deactivation). It also completes the partial supersession of CR-FR011-20261014-01.
- **Superseded by**: None.
