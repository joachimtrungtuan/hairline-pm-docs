# Change Request: Provider Status Cancellation Cascade for Aftercare Cases

**Change Request ID**: CR-FR011-20261014-01
**Primary FR**: FR-011
**Triggering FR / Event**: CR-FR015-20261013-01 (FR-015 v1.8) and FR-015 v1.9 deactivation-scope decision
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-14
**Decision Date**: 2026-10-14
**PRD Version Change**: v1.3 to v1.4
**Related Commit(s)**: Pending — no commit requested for this change

---

## Decision Summary

FR-015 makes an effective provider suspension or deactivation automatically cancel that provider's non-terminal treatment cases, including Aftercare cases. FR-011 was Verified & Approved with only admin-reviewed provider withdrawal (D1) and manual reassignment. This Change Request aligns FR-011 so Aftercare cases are cancelled by the cascade, retain the completion milestone and records, and route recovery continuity to admins, who keep using FR-011's existing reassignment/recovery workflow. The 2026-10-14 decision extends the same scope to deactivation (cause `ProviderDeactivated`).

## Baseline State

**Source version**: FR-011 v1.3, Workflow 4 Alternative Flows D1–D3, General Module Rules, Core Requirements, Edge Cases, and AftercarePlan entity

- Provider unavailability was handled only through D1 provider withdrawal or D2 performance reassignment, both admin-initiated.
- No automatic cancellation on provider status change, provider-caused cancellation cause, or support marker was defined.

## Approved State

**Target version**: [FR-011 v1.4](prd.md), Workflow 4 D4, General Module Rule 4, REQ-011-014, Edge Cases, and AftercarePlan entity

- An effective provider suspension/deactivation cancels the provider's non-terminal Aftercare cases with cause `ProviderSuspended` or `ProviderDeactivated` and an independent `supportRequired` marker, per [FR-015 A5/Screen 4](../fr015-provider-management/prd.md#screen-4-provider-suspensiondeactivation-modal).
- The FR-010 completion milestone and all aftercare records are retained read-only.
- Recovery continuity is routed to admins, who use the existing Workflow 4 reassignment/recovery tools; no automatic reassignment.
- Reactivation does not restore the case; a later deactivation does not overwrite an earlier `ProviderSuspended` cause.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Admin workflow | D1–D3 admin-initiated reassignment only | Added D4 provider-status cascade cancellation with admin recovery | FR-015 cascade includes Aftercare cases |
| Business rules | No provider-status rule | General Module Rule 4 Provider Status Cancellation | Define cause, retention, and admin-owned recovery |
| Cancellation identity | Cancel with free reason only | `ProviderSuspended` / `ProviderDeactivated` plus independent `supportRequired` on AftercarePlan | Distinguish from patient cancellation and D1 withdrawal |
| Record retention | Not addressed for cancellation | Completion milestone and aftercare records preserved | Recovery continuity and completed-procedure counting |

## Scope and Impact

### In Scope

- FR-011 Workflow 4 D4, General Module Rule 4, REQ-011-014, edge case, and AftercarePlan attributes.
- This FR-local Change Request.

### Out of Scope

- Changes to the existing admin reassignment/recovery workflow, D1–D3, or aftercare templates.
- Automatic reassignment, refunds, or restoration on reactivation.
- Notification content, admin filters, and financial resolution (owned by FR-015/FR-016/FR-020/FR-007/FR-017).
- Other PRDs, system documents, source code, and update logs.

### Affected Contracts

- **PRD owner**: [FR-011](prd.md) — Workflow 4 D4, General Module Rule 4, REQ-011-014, AftercarePlan.
- **Related FRs**: [FR-015](../fr015-provider-management/prd.md) owns the cascade trigger, notifications, and support marker semantics; [FR-010](../fr010-treatment-execution/prd.md) owns the completion milestone; [FR-006](../fr006-booking-scheduling/prd.md) owns booking status/cause; [FR-016](../fr016-admin-patient-mgmt/prd.md) owns admin identification and resolution of `supportRequired`.
- **System documents**: None changed here; aftercare cancellation/support metadata to be assessed in downstream system-document alignment.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed; no source code inspected.
- **Required assessment**: Provider-status event handling for Aftercare cases; provider action guards after cancellation; record retention; AftercarePlan cancellation cause and support marker; admin reassignment from a cancelled case.
- **Compatibility / rollout risk**: Must deploy together with FR-006/FR-010/FR-015 cascade changes. Standalone aftercare services (Workflow 2) are in cascade scope; the Product Owner confirmed this on 2026-10-14 and D4 states it.
- **Data migration**: To be assessed. Do not relabel existing terminal cases.

## Acceptance and Validation

- Suspension or deactivation of a provider cancels its non-terminal Aftercare cases with the correct cause and `supportRequired = true`.
- Completion milestone, plan, milestones, scans, questionnaires, medications, and communications remain retrievable.
- No case is automatically reassigned; admins can reassign or assign to the Hairline aftercare team through Workflow 4 and record audited resolution.
- Reactivation does not restore the case; suspension followed by deactivation keeps `ProviderSuspended`.
- Cross-FR verification with FR-006/FR-010/FR-015/FR-016 and implementation/regression proof are required before reconciliation becomes Verified.

## Approval and Traceability

- **Requested by**: Product Owner, Joachim Trung Tuan.
- **Approved by**: Product Owner, Joachim Trung Tuan, 2026-10-14 (FR-015 verification review, Issue 4 option 1).
- **Decision evidence**: [CR-FR015-20261013-01](../fr015-provider-management/change-request-2026-10-13-provider-lifecycle-subquote-contracts.md) and the 2026-10-14 decision that deactivation matches suspension scope.
- **PRD change log**: [FR-011 Appendix: Change Log](prd.md#appendix-change-log), v1.4 dated 2026-10-14.
- **Update log**: [FR015_VERIFICATION_ALIGNMENT_2026-10-14.md](../../update-logs/2026-10-14/FR015_VERIFICATION_ALIGNMENT_2026-10-14.md).
- **Supersedes**: None.
- **Superseded by**: None.
