# Change Request: FR-037 Monitoring Conversion Distribution

**Change Request ID**: CR-FR003-20260820-01
**Primary FR**: FR-003
**Triggering FR / Event**: FR-037 verification and monitoring-conversion integration
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-08-20
**Decision Date**: 2026-08-20
**PRD Version Change**: v1.9 to v2.0 to v2.1
**Related Commits**: `7317cc4`, `935283e`

---

## Decision Summary

FR-003 now accepts inquiries converted from FR-037 with a distinct provider-routing rule. An active monitoring provider receives the inquiry exclusively at first. If that provider explicitly declines before quote creation, FR-003 removes the restriction and executes normal distribution exactly once. This preserves the monitoring relationship without leaving a declined inquiry stranded.

## Baseline State

**Source version**: FR-003 v1.9, Workflow 2 and Workflow 3

All submitted inquiries entered the normal country, patient-selection, matching, and provider-cap distribution path. FR-003 had no monitoring-conversion provenance, exclusive-provider route, or decline-triggered return to normal distribution.

## Approved State

**Target version**: FR-003 v2.1, Workflow 2 Alternative Flow B3, Workflow 3 Alternative Flow C2, Screen 10, Distribution Rules, and REQ-003-016

Monitoring conversions may bypass normal matching for the assigned provider. An explicit pre-quote decline requires a reason, immutable audit evidence, removal of exclusive routing, and idempotent normal redistribution. Expiry remains on FR-003 and FR-004's existing configured paths.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Initial distribution | All inquiries used normal matching | Monitoring conversion may route only to its assigned provider | Preserve provider continuity from FR-037 |
| Provider action | Review, clarify, or create quote | Exclusive provider may also decline with a reason | Provide an explicit recovery trigger |
| Decline outcome | Undefined | Remove restriction and run normal distribution exactly once | Prevent stranded or duplicate inquiries |
| Expiry | Existing configurable expiry | Unchanged and separate from explicit decline | Avoid silently expanding the approved fallback |

## Scope and Impact

### In Scope

- Monitoring-conversion provenance and exclusive routing.
- Provider decline confirmation, reason, audit event, and idempotent redistribution.

### Out of Scope

- Automatic redistribution on inquiry or quote expiry.
- Changes to normal matching rules or the provider cap.

### Affected Contracts

- **PRD owner**: [`prd.md`](./prd.md) — Workflow 2, Workflow 3, Screen 10, Distribution Rules, REQ-003-016
- **Related FRs**: FR-004 restricted initial quote creation; FR-037 source conversion and fallback decision
- **System document**: [`../../system-prd.md`](../../system-prd.md) — FR-037 requirements

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed by this documentation change.
- **Required assessment**: Inquiry provenance, exclusive-provider authorization, decline endpoint/action, audit payload, distribution idempotency, notifications, provider views, and race handling with quote creation.
- **Compatibility / rollout risk**: Existing inquiries must retain their current routing unless explicitly identified as monitoring conversions; duplicate decline delivery must not create repeated distributions.
- **Data migration**: To be assessed for routing provenance and decline audit fields.

## Acceptance and Validation

- A converted inquiry with an assigned monitoring provider initially reaches only that provider.
- A confirmed pre-quote decline records the provider and reason, clears exclusive routing, and runs normal distribution once.
- Repeated decline requests return the committed result without duplicate views or notifications.
- Expiry without a decline does not invoke this fallback.

## Approval and Traceability

- **Requested by**: Product Owner
- **Approved by**: Product Owner, 2026-08-20
- **Decision evidence**: FR-037 verification resolution and provider-decline clarification
- **PRD change log**: FR-003 v2.0 and v2.1
- **Update logs**: [`FR037_CROSS_FR_VERIFICATION_SYNC_2026-08-20.md`](../../update-logs/2026-08-20/FR037_CROSS_FR_VERIFICATION_SYNC_2026-08-20.md), [`FR037_PROVIDER_DECLINE_FALLBACK_2026-08-20.md`](../../update-logs/2026-08-20/FR037_PROVIDER_DECLINE_FALLBACK_2026-08-20.md)
- **Supersedes**: None
- **Superseded by**: None
