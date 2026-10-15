# Change Request: Provider Status Cancellation Cascade — Admin Support Visibility

**Change Request ID**: CR-FR016-20261014-01
**Primary FR**: FR-016
**Triggering FR / Event**: [FR-015](../fr015-provider-management/prd.md) v1.9 provider suspension/deactivation cancellation cascade ([CR-FR015-20261013-01](../fr015-provider-management/change-request-2026-10-13-provider-lifecycle-subquote-contracts.md))
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-14
**Decision Date**: 2026-10-14
**PRD Version Change**: v1.5 to v1.6
**Related Commit(s)**: Pending — no commit requested for this change

> Create this document only for a major requirement event: a new or materially revised FR changes another verified or implemented FR, or an approved restructure substantially changes requirements, ownership, workflow, data, security, or integration contracts. Record small corrections only in the PRD change log and normal update log.

---

## Decision Summary

FR-015 now cancels all non-terminal Accepted, Confirmed, In Progress, and Aftercare cases when a provider is suspended or deactivated (causes `ProviderSuspended` / `ProviderDeactivated`) and sets an independent `supportRequired` ("Admin Support Required") marker. FR-016 is the admin workflow that must surface these records and own their audited resolution. This CR aligns verified FR-016 with that contract without adding automatic ticketing or changing FR-034.

## Baseline State

**Source version**: FR-016 v1.5 — Screen 1, Screen 2, Screen 3, Screen 7, General Module Rules, Dependencies, Requirements, Key Entities

- "Cancelled" meant patient-initiated inquiry cancellation only (FR-003 Workflow 5); Cancellation Reason came only from FR-026 Screen 5a.
- No provider-caused cancellation cause, support marker, filter, or resolution action existed.
- FR-015 and FR-034 were not listed as dependencies for cancellation support.

## Approved State

**Target version**: [FR-016 v1.6](prd.md) — Alternative Flow A7, Screens 1/2/3/7, Rule 8, Dependencies (FR-015, FR-034), REQ-016-028–030, User Story 9, Key Entity 1

- Provider-caused cancellations show their cause ("Cancelled — Provider Suspended" / "Cancelled — Provider Deactivated") and are never labelled patient cancellations.
- Screen 1 adds an Admin Support Required filter (All/Unresolved/Resolved) and an independent badge.
- Screen 2 lists Provider-Caused Impacts: inquiry/case reference, prior stage, cause, support state, linked FR-034 support case; "Resolve Support" requires a reason.
- Resolution logs an audit event before clearing the marker; the cause remains. An inquiry's marker stays while any linked provider-caused impact is unresolved.
- No automatic ticket creation; FR-034's workflow is unchanged. Cascade rules themselves remain owned by FR-015.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Cancellation identity | Cancelled = patient-initiated only | Patient cancellation plus provider-caused causes, shown distinctly | FR-015 REQ-015-018 |
| Admin identification | No support marker or filter | Admin Support Required filter and badge on patient list | Admins must find affected patients |
| Record detail | No provider-caused context | References, prior stage, cause, support state, linked FR-034 case | Support assistance needs full context |
| Resolution | Not defined | Reason + audit event before clearing; cause retained; inquiry marker persists while impacts unresolved | FR-015 Screen 4 "Admin Support Required" rule |
| Audit types | No provider-caused entries | Provider-Caused Cancellation (system) and Provider Support Resolution | Rule 1 audit completeness |

## Scope and Impact

### In Scope

- FR-016 display, filter, resolution, audit, dependency, requirement, and acceptance changes listed above.

### Out of Scope

- Cascade triggering, scope, and cause assignment (FR-015); notification content and delivery (FR-020).
- Automatic rebooking, refunds, clinical reassignment, or ticket creation; FR-034 workflow changes.
- System PRD, data schema, and technical specification edits.

### Affected Contracts

- **PRD owner**: [FR-016](prd.md) — Alternative Flow A7, Screens 1/2/3/7, Rule 8, REQ-016-028–030, User Story 9, Entity 1
- **Related FRs**: [FR-015](../fr015-provider-management/prd.md) supplies cause, marker, and affected references (A5, Screen 4, REQ-015-018/019); [FR-020](../fr020-notifications-alerts/prd.md) sends the admin-support alert that deep-links to FR-016 ([CR-FR020-20261014-01](../fr020-notifications-alerts/change-request-2026-10-14-provider-status-cancellation-cascade.md)); [FR-034](../fr034-support-center-ticketing/prd.md) linked support case only.
- **System documents**: None edited here; cancellation/support metadata storage is assessed during reconciliation.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed; no source code inspected.
- **Required assessment**: Admin patient list filter/badge, patient detail impacts list, resolution endpoint with audit, audit action types, stage labels for provider-caused causes.
- **Compatibility / rollout risk**: Existing "Cancelled by patient" labels must not be applied to provider-caused records; deploy with FR-015 cascade and FR-020 alerts.
- **Data migration**: To be assessed. Do not relabel existing terminal cases retrospectively.

## Acceptance and Validation

- Affected patients appear under Admin Support Required = Unresolved with the correct cause, never "Cancelled by patient".
- Detail shows references, prior stage, cause, and linked FR-034 case where present.
- Resolution requires a reason, logs an audit event, keeps the cause, and keeps an inquiry flagged while any linked impact is unresolved.
- No ticket is created automatically.
- Cross-FR verification with FR-015/FR-020 and implementation evidence required before reconciliation is Verified.

## Approval and Traceability

- **Requested by**: Product Owner, Joachim Trung Tuan
- **Approved by**: Product Owner, Joachim Trung Tuan, 2026-10-14 (FR-015 verification review, Issue 4 option 1)
- **Decision evidence**: FR-015 verification review 2026-10-14, Issue 4 option 1; [CR-FR015-20261013-01](../fr015-provider-management/change-request-2026-10-13-provider-lifecycle-subquote-contracts.md) Affected Contracts
- **PRD change log**: [FR-016 Appendix: Change Log](prd.md#appendix-change-log), v1.6 dated 2026-10-14
- **Update log**: [FR015_VERIFICATION_ALIGNMENT_2026-10-14.md](../../update-logs/2026-10-14/FR015_VERIFICATION_ALIGNMENT_2026-10-14.md)
- **Supersedes**: None
- **Superseded by**: None
