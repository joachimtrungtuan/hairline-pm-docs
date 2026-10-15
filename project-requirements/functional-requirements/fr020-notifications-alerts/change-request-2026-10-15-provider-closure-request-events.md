# Change Request: Provider Closure Request Events

**Change Request ID**: CR-FR020-20261015-02
**Primary FR**: FR-020
**Triggering FR / Event**: FR-015 v1.15 eighth verification pass, Issue 2 (account closure follow-through)
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-15
**Decision Date**: 2026-10-15
**PRD Version Change**: v2.5 to v2.6
**Related Commit(s)**: Pending

---

## Decision Summary

FR-032 sends a closure request to admins, and FR-015 A7 lets an admin approve (deactivate) or reject it. FR-020 had no event for the request or the rejection, and `provider.deactivated` depended on an optional "Notify Provider" checkbox even though FR-032 promises the provider an email. The Product Owner approved two new mandatory events and a guaranteed deactivation email for closure deactivations.

## Baseline State

**Source version**: FR-020 v2.5, Notification Types table (Provider/Compliance), Provider Lifecycle Notifications rule, REQ-020-014/015

- No event for a submitted closure request or a rejected one.
- `provider.deactivated` was sent only when "Notify Provider" was checked, including for closure deactivations.

## Approved State

**Target version**: [FR-020 v2.6](prd.md), Notification Types table, Provider Lifecycle Notifications rule, REQ-020-016

- `provider.closure_requested` (Admin, Email + in-app, mandatory): sent when a provider submits an FR-032 closure request, with a deep link to the request in FR-015.
- `provider.closure_rejected` (Provider, email, mandatory): sent when an admin rejects the request, with the review notes and a statement that the account stays Active.
- `provider.deactivated` is always sent for a deactivation that processes a closure request, because FR-015 locks "Notify Provider" on.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Closure request alert | None | `provider.closure_requested` to admins, mandatory | FR-032 step 10 had no event |
| Closure rejection | None | `provider.closure_rejected` to provider, mandatory | Provider must learn the outcome |
| Closure deactivation email | Optional via Notify Provider | Always sent | FR-032 step 11 promise |

## Scope and Impact

### In Scope

- FR-020 Notification Types rows, Provider Lifecycle Notifications rule, `provider.suspended` / `provider.deactivated` row note, REQ-020-016, and this Change Request.

### Out of Scope

- FR-030 catalog and toggle locks (CR-FR030-20261015-02).
- Closure request workflow (FR-032) and admin processing (FR-015 A7).

### Affected Contracts

- **PRD owner**: `functional-requirements/fr020-notifications-alerts/prd.md`
- **Related FRs**:
  - FR-015 v1.16 (A7, Screen 4, FR-020 dependency)
  - FR-032 v1.9 ([CR-FR032-20261015-03](../fr032-provider-dashboard-settings/change-request-2026-10-15-closure-request-notifications.md))
  - FR-030 v1.11 ([CR-FR030-20261015-02](../fr030-notification-rules-config/change-request-2026-10-15-provider-closure-request-events.md))
- **System documents**: None

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed.
- **Required assessment**:
  - whether any admin notification fires on closure request submission today;
  - whether rejection sends any provider message;
  - the event keys and templates in the notification service.
- **Compatibility / rollout risk**: Low.
- **Data migration**: None

## Acceptance and Validation

- A closure request submission sends `provider.closure_requested` to admins with View Providers permission.
- A rejection sends `provider.closure_rejected` to the provider with the review notes.
- A closure deactivation always sends `provider.deactivated`.
- None of these can be disabled by FR-030 toggles or FR-032 category preferences.

## Approval and Traceability

- **Requested by**: verify-fr pass on FR-015 v1.15
- **Approved by**: Product Owner (Joachim Trung Tuan), 2026-10-15
- **Decision evidence**: AskUserQuestion decisions and the "Yes" approval in the FR-015 eighth verification session
- **PRD change log**: FR-020 v2.6 row (2026-10-15); FR-015 v1.16 row
- **Update log**: [FR015_EIGHTH_VERIFICATION_FIXES_2026-10-15.md](../../update-logs/2026-10-15/FR015_EIGHTH_VERIFICATION_FIXES_2026-10-15.md)
- **Supersedes**: None
- **Superseded by**: None
