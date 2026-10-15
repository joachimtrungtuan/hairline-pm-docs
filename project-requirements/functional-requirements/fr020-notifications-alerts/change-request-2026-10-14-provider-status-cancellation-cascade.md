# Change Request: Provider Status Cancellation Cascade — Notifications

**Change Request ID**: CR-FR020-20261014-01
**Primary FR**: FR-020
**Triggering FR / Event**: [FR-015](../fr015-provider-management/prd.md) v1.9 provider suspension/deactivation cancellation cascade ([CR-FR015-20261013-01](../fr015-provider-management/change-request-2026-10-13-provider-lifecycle-subquote-contracts.md))
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-14
**Decision Date**: 2026-10-14
**PRD Version Change**: v2.3 to v2.4
**Related Commit(s)**: Pending — no commit requested for this change

> Create this document only for a major requirement event: a new or materially revised FR changes another verified or implemented FR, or an approved restructure substantially changes requirements, ownership, workflow, data, security, or integration contracts. Record small corrections only in the PRD change log and normal update log.

---

## Decision Summary

FR-015 provider suspension and deactivation now cancel all non-terminal Accepted, Confirmed, In Progress, and Aftercare cases (causes `ProviderSuspended` / `ProviderDeactivated`) and require patient and admin handoffs (REQ-015-019). FR-020 adds the provider-caused patient notice, the mandatory admin-support alert, and the provider suspension/deactivation email to its event catalog, with retry/de-duplication and privacy rules.

## Baseline State

**Source version**: FR-020 v2.3 — Scope Boundaries event catalog, Business Rules, Dependencies, User Scenarios, Functional Requirements Summary

- No provider-caused cancellation or offer-unavailability event; existing cancellation events were patient-initiated or generic booking/treatment cancellations.
- No mandatory admin-support alert for provider-status impacts and no provider suspension/deactivation email event.

## Approved State

**Target version**: [FR-020 v2.4](prd.md) — event catalog (Provider/Compliance rows), Business Rules, Dependencies (FR-015, FR-016), User Story 5, REQ-020-013/014

- `provider.status_cancellation_patient`: per affected inquiry/case; reference + Contact Admin/Support action; never says patient cancelled, never instructs payment, never exposes confidential reasons; mandatory.
- `provider.status_cancellation_admin_support`: mandatory admin alert per affected record, deep-linking to FR-016's Admin Support Required filter.
- Both sent regardless of FR-015's "Notify Provider" checkbox; retries de-duplicated per provider-status event + affected record + recipient, without restoring cancelled records.
- `provider.suspended` / `provider.deactivated`: provider email only when "Notify Provider" is checked, with action, reason, effective date, and support contact.
- Channels follow FR-020's existing rules (Email/Push/in-app); SMS remains future.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Patient notice | None for provider-caused cancellation | Mandatory provider-caused cancellation/offer-unavailability notice | FR-015 REQ-015-019 |
| Admin alert | None | Mandatory admin-support alert linking to FR-016 | Admins must assist affected patients |
| Provider email | Not catalogued | Suspended/Deactivated email gated by "Notify Provider" | FR-015 Screen 4 Notification Email rule |
| Delivery integrity | Generic retry (Flow B2) | Retry without duplicates per status event + record + recipient | Avoid duplicate outcomes on retries |
| Privacy | Patient-reason privacy only | No patient-cancelled wording, no payment instruction, no confidential provider reason | FR-015 Screen 4 Patient communication rule |

## Scope and Impact

### In Scope

- FR-020 catalog rows, business rule, dependencies, user story, and REQ-020-013/014.

### Out of Scope

- Cascade logic and cause assignment (FR-015); admin filter/resolution (FR-016); ticket creation (FR-034 unchanged).
- Template copy authoring (FR-030 editor); SMS delivery.
- System PRD, data schema, and technical specification edits.

### Affected Contracts

- **PRD owner**: [FR-020](prd.md) — Scope Boundaries catalog, Business Rules, Dependencies, User Story 5, REQ-020-013/014
- **Related FRs**: [FR-015](../fr015-provider-management/prd.md) emits the trigger (A5, Screen 4, REQ-015-019); [FR-016](../fr016-admin-patient-mgmt/prd.md) is the alert target ([CR-FR016-20261014-01](../fr016-admin-patient-mgmt/change-request-2026-10-14-provider-status-cancellation-cascade.md)); [FR-030](../fr030-notification-rules-config/prd.md) is the catalog source of truth and must add the three new event keys and templates during controlled alignment.
- **System documents**: None edited here.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed; no source code inspected.
- **Required assessment**: Event emission from the provider-status cascade, templates and privacy allowlist, mandatory-event enforcement, de-duplication key, retry handling, provider email gating.
- **Compatibility / rollout risk**: Until FR-030 mirrors these events, its "FR-030 prevails" rule leaves them unconfigured; align FR-030 before implementation.
- **Data migration**: None.

## Acceptance and Validation

- Each affected patient receives one privacy-safe provider-caused notice per affected record with Contact Admin/Support action.
- Admins receive one support alert per affected record, even with "Notify Provider" unchecked.
- Failed attempts retry without duplicate notices and without restoring cancelled records.
- Provider email is sent only when "Notify Provider" is checked and includes action, reason, effective date, and support contact.
- FR-030 catalog alignment and implementation evidence required before reconciliation is Verified.

## Approval and Traceability

- **Requested by**: Product Owner, Joachim Trung Tuan
- **Approved by**: Product Owner, Joachim Trung Tuan, 2026-10-14 (FR-015 verification review, Issue 4 option 1)
- **Decision evidence**: FR-015 verification review 2026-10-14, Issue 4 option 1; [CR-FR015-20261013-01](../fr015-provider-management/change-request-2026-10-13-provider-lifecycle-subquote-contracts.md) Affected Contracts
- **PRD change log**: [FR-020 Appendix: Change Log](prd.md#appendix-change-log), v2.4 dated 2026-10-14
- **Update log**: [FR015_VERIFICATION_ALIGNMENT_2026-10-14.md](../../update-logs/2026-10-14/FR015_VERIFICATION_ALIGNMENT_2026-10-14.md)
- **Supersedes**: None
- **Superseded by**: None
