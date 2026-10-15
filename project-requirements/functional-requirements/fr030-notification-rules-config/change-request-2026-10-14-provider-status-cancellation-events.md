# Change Request: Provider Status Cancellation Events — Notification Catalog

**Change Request ID**: CR-FR030-20261014-01
**Primary FR**: FR-030
**Triggering FR / Event**: [FR-015](../fr015-provider-management/prd.md) v1.9 provider suspension/deactivation cancellation cascade; [FR-020](../fr020-notifications-alerts/prd.md) v2.4 event additions ([CR-FR020-20261014-01](../fr020-notifications-alerts/change-request-2026-10-14-provider-status-cancellation-cascade.md))
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-14
**Decision Date**: 2026-10-14
**PRD Version Change**: v1.8 to v1.9
**Related Commit(s)**: Pending — no commit requested for this change

> Create this document only for a major requirement event: a new or materially revised FR changes another verified or implemented FR, or an approved restructure substantially changes requirements, ownership, workflow, data, security, or integration contracts. Record small corrections only in the PRD change log and normal update log.

---

## Decision Summary

FR-020 v2.4 added three provider-status notification events for the FR-015 suspension/deactivation cancellation cascade. FR-020 mirrors FR-030, and FR-030 prevails on any mismatch, so FR-030 (the source-of-truth event catalog) now contains the same events, marks the two cancellation events as non-disableable, and records the FR-015/FR-016 dependency.

## Baseline State

**Source version**: FR-030 v1.8 — Admin-Configurable Notification Event Catalog, Admin Editability Rules (Non-Disableable by Default), Internal Dependencies

- Provider/Compliance catalog contained only `provider.onboarding_requested` and `provider.document_expiration_warning`.
- No provider-caused cancellation event, admin-support alert, or provider suspension/deactivation email was configurable; under the "FR-030 prevails" rule the FR-020 v2.4 events would remain unconfigured.
- Non-disableable events were limited to Account/Auth events and `quote.cancelled_inquiry`.

## Approved State

**Target version**: [FR-030 v1.9](prd.md) — event catalog (Provider/Compliance rows), Non-Disableable by Default, Internal Dependencies

- `provider.status_cancellation_patient` (Patient): one per affected inquiry/case; reference + Contact Admin/Support action; never says the patient cancelled, never instructs payment, never exposes confidential reasons; mandatory; MVP default channels Email + Push + in-app.
- `provider.status_cancellation_admin_support` (Admin): mandatory alert per affected record with patient, reference, prior stage, cause, and FR-016 Admin Support Required deep link; pinned critical; no automatic FR-034 ticket.
- `provider.suspended` / `provider.deactivated` (Provider): email only when FR-015 "Notify Provider" is checked, with action, reason, effective date, and support contact.
- Both cancellation events are sent regardless of "Notify Provider", have locked toggles, and retry without duplicates per provider-status event + affected record + recipient, never restoring cancelled records.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Event catalog | No provider-status cancellation or suspension/deactivation events | Three Provider/Compliance rows matching FR-020 v2.4 | FR-030 is the catalog source of truth |
| Non-disableable events | Account/Auth and `quote.cancelled_inquiry` | Adds `provider.status_cancellation_patient` and `provider.status_cancellation_admin_support` | FR-020 REQ-020-013 mandatory delivery |
| Retry integrity | Generic retry configuration | De-duplication per provider-status event + affected record + recipient for cancellation events | FR-020 REQ-020-014 |
| Dependencies | No FR-015/FR-016 dependency | FR-015 trigger and FR-016 alert target recorded | Traceability |

## Scope and Impact

### In Scope

- FR-030 catalog rows, Non-Disableable by Default rule, Internal Dependencies, change log, and status.

### Out of Scope

- Cascade logic and cause assignment (FR-015); admin filter/resolution (FR-016); ticket creation (FR-034 unchanged).
- Template copy authoring; SMS delivery (future).
- System PRD, data schema, and technical specification edits.

### Affected Contracts

- **PRD owner**: [FR-030](prd.md) — Admin-Configurable Notification Event Catalog, Admin Editability Rules, Internal Dependencies
- **Related FRs**: [FR-020](../fr020-notifications-alerts/prd.md) defines delivery semantics (REQ-020-013/014); [FR-015](../fr015-provider-management/prd.md) emits the trigger (A5, Screen 4); [FR-016](../fr016-admin-patient-mgmt/prd.md) is the admin alert target ([CR-FR016-20261014-01](../fr016-admin-patient-mgmt/change-request-2026-10-14-provider-status-cancellation-cascade.md)).
- **System documents**: None edited here.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed; no source code inspected.
- **Required assessment**: Event catalog API exposes the three keys; locked toggles for both cancellation events; recipient-scoped template variable allowlist excludes confidential suspension/deactivation reasons from patient templates; de-duplication key on retries.
- **Compatibility / rollout risk**: Events are unconfigurable until the backend catalog exposes these keys.
- **Data migration**: None.

## Acceptance and Validation

- The three event keys appear in `Settings → Alerts & Notifications` under Provider/Compliance with the recipients above.
- Admins cannot disable `provider.status_cancellation_patient` or `provider.status_cancellation_admin_support`.
- Patient templates cannot reference confidential suspension/deactivation reasons or payment instructions.
- Provider suspension/deactivation email is gated by "Notify Provider".
- Catalog semantics match FR-020 v2.4; implementation evidence required before reconciliation is Verified.

## Approval and Traceability

- **Requested by**: Product Owner, Joachim Trung Tuan
- **Approved by**: Product Owner, Joachim Trung Tuan, 2026-10-14 (FR-015 verification review)
- **Decision evidence**: FR-015 verification review 2026-10-14; [CR-FR020-20261014-01](../fr020-notifications-alerts/change-request-2026-10-14-provider-status-cancellation-cascade.md) Affected Contracts (FR-030 must add the three event keys)
- **PRD change log**: [FR-030 Appendix: Change Log](prd.md#appendix-change-log), v1.9 dated 2026-10-14
- **Update log**: [FR015_VERIFICATION_ALIGNMENT_2026-10-14.md](../../update-logs/2026-10-14/FR015_VERIFICATION_ALIGNMENT_2026-10-14.md)
- **Supersedes**: None
- **Superseded by**: None
