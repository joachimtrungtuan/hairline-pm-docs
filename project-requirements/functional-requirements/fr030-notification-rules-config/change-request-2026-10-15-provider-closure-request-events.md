# Change Request: Provider Closure Request Events in the Notification Catalog

**Change Request ID**: CR-FR030-20261015-02
**Primary FR**: FR-030
**Triggering FR / Event**: FR-015 v1.15 eighth verification pass, Issue 2; FR-020 v2.6 ([CR-FR020-20261015-02](../fr020-notifications-alerts/change-request-2026-10-15-provider-closure-request-events.md))
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-15
**Decision Date**: 2026-10-15
**PRD Version Change**: v1.10 to v1.11
**Related Commit(s)**: Pending

---

## Decision Summary

FR-030 is the source of truth for event coverage. FR-020 v2.6 adds two mandatory provider account-closure events, so the catalog must list them with locked toggles and note that closure deactivations always send `provider.deactivated`.

## Baseline State

**Source version**: FR-030 v1.10, Provider/Compliance catalog, Non-Disableable by Default rules, FR-015 dependency

- No `provider.closure_requested` or `provider.closure_rejected` entries.
- `provider.deactivated` was always optional via "Notify Provider".

## Approved State

**Target version**: [FR-030 v1.11](prd.md), Provider/Compliance catalog, Non-Disableable by Default, FR-015 dependency

- `provider.closure_requested` (Admin, Email + in-app) and `provider.closure_rejected` (Provider, email), both mandatory with toggles locked.
- `provider.suspended` / `provider.deactivated` entry notes that closure deactivations always send the email.
- The FR-015 dependency lists both new events.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Catalog | No closure request events | Two mandatory entries | Mirror FR-020 v2.6 |
| Toggle locks | Not applicable | Locked for both events | Requests and outcomes must always be communicated |
| `provider.deactivated` note | Optional via Notify Provider | Always sent for closure deactivations | FR-015 A7 locks Notify Provider on |

## Scope and Impact

### In Scope

- FR-030 catalog rows, Non-Disableable by Default rule, FR-015 dependency, and this Change Request.

### Out of Scope

- Event delivery and retry (FR-020) and the closure workflow (FR-015, FR-032).

### Affected Contracts

- **PRD owner**: `functional-requirements/fr030-notification-rules-config/prd.md`
- **Related FRs**:
  - FR-020 v2.6 (CR-FR020-20261015-02)
  - FR-015 v1.16 (A7)
  - FR-032 v1.9 ([CR-FR032-20261015-03](../fr032-provider-dashboard-settings/change-request-2026-10-15-closure-request-notifications.md))
- **System documents**: None

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed.
- **Required assessment**: the notification rules screen entries and toggle locks for both events.
- **Compatibility / rollout risk**: Low.
- **Data migration**: None

## Acceptance and Validation

- The FR-030 rules screen lists both events with locked toggles.
- The catalog matches FR-020 v2.6 for recipients, channels, and mandatory status.

## Approval and Traceability

- **Requested by**: verify-fr pass on FR-015 v1.15
- **Approved by**: Product Owner (Joachim Trung Tuan), 2026-10-15
- **Decision evidence**: AskUserQuestion decisions and the "Yes" approval in the FR-015 eighth verification session
- **PRD change log**: FR-030 v1.11 row (2026-10-15); FR-015 v1.16 row
- **Update log**: [FR015_EIGHTH_VERIFICATION_FIXES_2026-10-15.md](../../update-logs/2026-10-15/FR015_EIGHTH_VERIFICATION_FIXES_2026-10-15.md)
- **Supersedes**: None
- **Superseded by**: None
