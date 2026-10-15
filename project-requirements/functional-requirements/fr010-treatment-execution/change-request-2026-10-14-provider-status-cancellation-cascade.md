# Change Request: Provider Status Cancellation Cascade for In Progress Cases

**Change Request ID**: CR-FR010-20261014-01
**Primary FR**: FR-010
**Triggering FR / Event**: CR-FR015-20261013-01 (FR-015 v1.8) and FR-015 v1.9 deactivation-scope decision
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-14
**Decision Date**: 2026-10-14
**PRD Version Change**: v2.0 to v2.1
**Related Commit(s)**: Pending — no commit requested for this change

---

## Decision Summary

FR-015 makes an effective provider suspension or deactivation automatically cancel that provider's non-terminal treatment cases, including In Progress cases. FR-010 was Verified & Approved with only the provider-requested Cancel/Close Case flow, which never auto-transitions status. This Change Request aligns FR-010 so In Progress cases are cancelled by the cascade while clinical records are preserved and clinical continuity is routed to admins. The 2026-10-14 decision extends the same scope to deactivation (cause `ProviderDeactivated`).

## Baseline State

**Source version**: FR-010 v2.0, Alternative Flows B4, General Module Rules 1 and 11, Edge Cases, Core Requirements, and Entity 1

- Rule 1 required strict Confirmed → In Progress → Aftercare → Completed progression with no exception for provider-status events.
- The only closure path was B4 provider-requested Cancel/Close Case: admin notified, no automatic status or financial action (Rule 11).
- No provider-caused cancellation cause, support marker, or treatment-record Cancelled status was defined.

## Approved State

**Target version**: [FR-010 v2.1](prd.md), Alternative Flow B5, Rules 1/11/12, Edge Cases, REQ-010-025, and Entity 1

- An effective provider suspension/deactivation cancels the provider's In Progress cases with cause `ProviderSuspended` or `ProviderDeactivated` and an independent `supportRequired` marker, per [FR-015 A5/Screen 4](../fr015-provider-management/prd.md#screen-4-provider-suspensiondeactivation-modal).
- Provider documentation is blocked; day records, clinical notes, photos, head scan photo sets, and any already recorded completion milestone are retained read-only.
- Clinical continuity, patient assistance, and financial resolution are routed to admins; no automatic reassignment, refund, or rebooking.
- B4 provider-requested Cancel/Close Case remains unchanged and distinct.
- Reactivation does not restore the case; a later deactivation does not overwrite an earlier `ProviderSuspended` cause.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Alternative flows | B4 provider-requested closure only | Added B5 provider-status cascade cancellation | FR-015 cascade includes In Progress cases |
| Status progression | Rule 1 had no exceptions | Rule 1 exception and Rule 12 for provider-status cancellation | Allow admin-authorized cascade without changing ordinary progression |
| Cancellation identity | No provider-caused cause or support marker | `ProviderSuspended` / `ProviderDeactivated` plus independent `supportRequired` | Distinguish from patient cancellation, B4 closure, and payment-window expiry |
| Record retention | Not addressed for cancellation | Clinical notes/photos and recorded completion milestone preserved | Admin clinical continuity and audit |
| Entity 1 status | In Progress, Completed | Adds Cancelled (provider-status cascade only) | Represent cascade outcome |

## Scope and Impact

### In Scope

- FR-010 B5, Rules 1/11/12, edge case, REQ-010-025, and Entity 1 status.
- This FR-local Change Request.

### Out of Scope

- Changes to B4 provider-requested Cancel/Close Case behavior.
- Automatic clinical reassignment, refunds, rebooking, or ticket creation.
- Notification content, admin filters, and financial resolution (owned by FR-015/FR-016/FR-020/FR-007/FR-017).
- Other PRDs, system documents, source code, and update logs.

### Affected Contracts

- **PRD owner**: [FR-010](prd.md) — Alternative Flow B5, Rules 1/11/12, REQ-010-025, Entity 1.
- **Related FRs**: [FR-015](../fr015-provider-management/prd.md) owns the cascade trigger, notifications, and support marker semantics; [FR-006](../fr006-booking-scheduling/prd.md) owns booking cancellation cause and payment guards; [FR-011](../fr011-aftercare-recovery-management/prd.md) owns aftercare continuity; [FR-016](../fr016-admin-patient-mgmt/prd.md) owns admin identification and resolution of `supportRequired`.
- **System documents**: None changed here; state transitions and cancellation/support metadata to be assessed in downstream system-document alignment.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed; no source code inspected.
- **Required assessment**: Provider-status event handling for In Progress cases; documentation write guards after cancellation; retention of day records/media; Cancelled treatment status; admin visibility of the support marker.
- **Compatibility / rollout risk**: Must deploy together with FR-006/FR-011/FR-015 cascade changes; an in-flight End Treatment save racing with suspension must not revive or complete a cancelled case.
- **Data migration**: To be assessed. Do not relabel existing terminal cases.

## Acceptance and Validation

- Suspension or deactivation of a provider cancels its In Progress cases with the correct cause and `supportRequired = true`.
- Saved clinical notes, photos, head scan photo sets, and any recorded completion milestone remain retrievable read-only.
- B4 Cancel/Close Case still does not auto-transition status.
- Reactivation does not restore the case; suspension followed by deactivation keeps `ProviderSuspended`.
- Cross-FR verification with FR-006/FR-011/FR-015/FR-016 and implementation/regression proof are required before reconciliation becomes Verified.

## Approval and Traceability

- **Requested by**: Product Owner, Joachim Trung Tuan.
- **Approved by**: Product Owner, Joachim Trung Tuan, 2026-10-14 (FR-015 verification review, Issue 4 option 1).
- **Decision evidence**: [CR-FR015-20261013-01](../fr015-provider-management/change-request-2026-10-13-provider-lifecycle-subquote-contracts.md) and the 2026-10-14 decision that deactivation matches suspension scope.
- **PRD change log**: [FR-010 Appendix: Change Log](prd.md#appendix-change-log), v2.1 dated 2026-10-14.
- **Update log**: [FR015_VERIFICATION_ALIGNMENT_2026-10-14.md](../../update-logs/2026-10-14/FR015_VERIFICATION_ALIGNMENT_2026-10-14.md).
- **Supersedes**: None.
- **Superseded by**: None.
