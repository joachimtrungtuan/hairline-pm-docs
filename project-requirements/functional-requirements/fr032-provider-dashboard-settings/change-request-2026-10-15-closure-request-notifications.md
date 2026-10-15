# Change Request: Closure Request Notifications and Admin Marker

**Change Request ID**: CR-FR032-20261015-03
**Primary FR**: FR-032
**Triggering FR / Event**: FR-015 v1.15 eighth verification pass, Issue 2 (account closure follow-through)
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-15
**Decision Date**: 2026-10-15
**PRD Version Change**: v1.8 to v1.9
**Related Commit(s)**: Pending

---

## Decision Summary

FR-032 tells a provider who requests account closure: "You will receive an email once your account is deactivated." FR-015 A7 let the admin clear "Notify Provider", which could break that promise. Admins also had no defined event for a new request, and a rejected request sent the provider nothing. The Product Owner chose the full fix: lock "Notify Provider" on for closure deactivations, alert admins on submission, flag the provider in the FR-015 list, and email the provider on rejection.

## Baseline State

**Source version**: FR-032 v1.8, Main Flow: Request Account Closure, steps 10, 15, and 16

- Step 10 said "System sends closure request notification to admin team" with no FR-020 event behind it.
- Step 15 sent `provider.deactivated`, but FR-015 A7 allowed the admin to clear "Notify Provider", so the email was not guaranteed.
- Step 16 marked a rejected request Rejected with no provider notice.

## Approved State

**Target version**: [FR-032 v1.9](prd.md), Main Flow: Request Account Closure, steps 10, 15, and 16

- Step 10 sends FR-020 `provider.closure_requested` to admins (mandatory), and FR-015 Screen 1 shows a Closure Requested marker and filter.
- Step 15 always sends `provider.deactivated`, because FR-015 A7 locks "Notify Provider" on for closure deactivations.
- Step 16 sends FR-020 `provider.closure_rejected` to the provider with the admin review notes (mandatory); the provider may submit a new request later.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Admin alert on submission | Generic "notification to admin team", no event | FR-020 `provider.closure_requested` (mandatory) plus FR-015 Screen 1 marker and filter | Requests must not be missed within the 5-business-day target |
| Deactivation email | Sent only if admin kept "Notify Provider" | Always sent for closure deactivations | Keep the step 11 promise |
| Rejection notice | None | FR-020 `provider.closure_rejected` with review notes (mandatory) | Provider must learn the account stays Active |

## Scope and Impact

### In Scope

- FR-032 Request Account Closure steps 10, 15, and 16, and this Change Request.

### Out of Scope

- The closure dialog, request record, and one-pending-request rule (unchanged).
- FR-015 A7 processing and Screen 1 marker (owned by FR-015 v1.16).
- Event content and delivery (FR-020 and FR-030).

### Affected Contracts

- **PRD owner**: `functional-requirements/fr032-provider-dashboard-settings/prd.md`
- **Related FRs**:
  - FR-015 v1.16 (A7, Screen 1, Screen 4 Notify Provider, edge case)
  - FR-020 v2.6 ([CR-FR020-20261015-02](../fr020-notifications-alerts/change-request-2026-10-15-provider-closure-request-events.md))
  - FR-030 v1.11 ([CR-FR030-20261015-02](../fr030-notification-rules-config/change-request-2026-10-15-provider-closure-request-events.md))
- **System documents**: [System data schema](../../system-data-schema.md) v1.7.0 §38 and §40 closure request rules

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed.
- **Required assessment**:
  - whether submitting a closure request triggers any admin notification today;
  - whether the deactivation form can suppress the provider email for closure requests;
  - whether rejection sends any provider notice.
- **Compatibility / rollout risk**: Low.
- **Data migration**: None

## Acceptance and Validation

- Submitting a closure request sends `provider.closure_requested` to admins and shows the provider under the FR-015 Closure Requested filter.
- Deactivating from a closure request always sends `provider.deactivated`; "Notify Provider" cannot be cleared.
- Rejecting a closure request sends `provider.closure_rejected` with the review notes, and the account stays Active.

## Approval and Traceability

- **Requested by**: verify-fr pass on FR-015 v1.15
- **Approved by**: Product Owner (Joachim Trung Tuan), 2026-10-15
- **Decision evidence**: AskUserQuestion decisions and the "Yes" approval in the FR-015 eighth verification session
- **PRD change log**: FR-032 v1.9 row (2026-10-15); FR-015 v1.16 row
- **Update log**: [FR015_EIGHTH_VERIFICATION_FIXES_2026-10-15.md](../../update-logs/2026-10-15/FR015_EIGHTH_VERIFICATION_FIXES_2026-10-15.md)
- **Supersedes**: None
- **Superseded by**: None
