# Change Request: FR-037 Monitoring Advice Questionnaire Reuse

**Change Request ID**: CR-FR025-20260820-01
**Primary FR**: FR-025
**Triggering FR / Event**: FR-037 provider-advice mode integration
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-08-20
**Decision Date**: 2026-08-20
**PRD Version Change**: v2.2 to v2.3
**Related Commit**: `7317cc4`

---

## Decision Summary

FR-037 provider-advice mode reuses FR-025's existing active Inquiry-context questionnaire. The monitoring flow does not create a new questionnaire context or Admin activation control.

## Baseline State

**Source version**: FR-025 v2.2, Entry Points and Questionnaire Context Types

The active Inquiry-context set was delivered during FR-003 inquiry submission. FR-025 had no monitoring-advice entry point or dependency.

## Approved State

**Target version**: FR-025 v2.3, System-Triggered Monitoring Advice entry point

FR-025 delivers the same active Inquiry-context set when an FR-037 patient activates provider-advice mode. Completed valid answers gate provider access to the monitoring case.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Trigger | FR-003 inquiry submission | FR-003 inquiry or FR-037 monitoring advice activation | Reuse the approved safety questionnaire |
| Context model | Inquiry and existing contexts | Unchanged | Avoid duplicate configuration and version drift |
| Provider access | No monitoring rule | Valid questionnaire required before FR-037 provider access | Protect medical review quality |

## Scope and Impact

### In Scope

- Delivery and response snapshot of the active Inquiry-context questionnaire for FR-037 advice mode.

### Out of Scope

- A new monitoring context type, questionnaire set, or Admin toggle.
- FR-037 self-monitoring mode.

### Affected Contracts

- **PRD owner**: [`prd.md`](./prd.md) — Entry Points and FR-037 dependency
- **Related FRs**: FR-037 provider-advice activation; FR-003 existing Inquiry-context consumer

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed by this documentation change.
- **Required assessment**: Context resolver, published-version snapshot, response reuse, validation, provider-access gate, audit, and handling when the active set changes.
- **Compatibility / rollout risk**: Monitoring must consume the existing active Inquiry set without changing FR-003 behavior or creating a second activation state.
- **Data migration**: To be assessed for monitoring cases created before questionnaire gating exists.

## Acceptance and Validation

- Advice-mode activation loads the current active Inquiry-context set.
- Provider access remains blocked until required answers are valid.
- No new context type or activation toggle appears in Admin.
- FR-003 continues consuming the same active set unchanged.

## Approval and Traceability

- **Requested by**: Product Owner
- **Approved by**: Product Owner, 2026-08-20
- **Decision evidence**: FR-037 verification resolution
- **PRD change log**: FR-025 v2.3
- **Update log**: [`FR037_CROSS_FR_VERIFICATION_SYNC_2026-08-20.md`](../../update-logs/2026-08-20/FR037_CROSS_FR_VERIFICATION_SYNC_2026-08-20.md)
- **Supersedes**: None
- **Superseded by**: None
