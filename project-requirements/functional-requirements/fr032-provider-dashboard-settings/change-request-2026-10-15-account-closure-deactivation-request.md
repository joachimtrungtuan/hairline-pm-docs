# Change Request: Provider Account Closure as an Admin-Processed Deactivation Request

**Change Request ID**: CR-FR032-20261015-02
**Primary FR**: FR-032
**Triggering FR / Event**: FR-015 v1.13 (sixth verification pass, Issue 1)
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-15
**Decision Date**: 2026-10-15
**PRD Version Change**: v1.7 to v1.8
**Related Commit(s)**: Pending

---

## Decision Summary

FR-032 let providers request account deletion, which on admin approval set a `Deleted` status. FR-015 owns provider account status and only defines Active, Suspended and Deactivated. FR-015 also says providers have no self-service deactivation. The Product Owner approved turning FR-032's Delete Account into an account-closure request. An admin processes the request in FR-015 by deactivating the provider through Screen 4, with the normal cascade. The `Deleted` status is removed, and so is the FR-032 rule that blocked requests while bookings or payouts were active.

## Baseline State

**Source version**: FR-032 v1.7. The following sections are affected:

- Main Flow "Request Account Deletion" and Alternative Flows A13, B13 and B14
- Screen 2 Delete Account card
- Privacy Rule 3, Audit Rule and GDPR Compliance
- Assumption 2
- User Story 7
- REQ-032-013, REQ-032-020 and REQ-032-023
- Entity 5

In the baseline, a provider submits a deletion request, and the system blocks it when bookings are active or payouts are pending. When an admin approves it, the account status becomes `Deleted`.

## Approved State

**Target version**: FR-032 v1.8. The following sections are updated:

- Main Flow "Request Account Closure"
- Alternative Flow A13
- Screen 2 Account Closure card
- Privacy Rule 3
- REQ-032-013 and REQ-032-023
- Entity 5 Provider Account Closure Request

**Paired FR**: FR-015 v1.14, Alternative Flow A7 "Admin Processes a Provider Account-Closure Request" and the matching edge case.

See the [FR-032 PRD](prd.md) and the [FR-015 PRD](../fr015-provider-management/prd.md) for the full contract.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Provider action | "Delete Account", which submits a deletion request | "Request account closure", which submits a closure request (status Pending Admin Review) | The provider cannot change their own status, and FR-015 owns status |
| Admin approval | Admin approves the deletion, and the status is set to `Deleted` | Admin deactivates the provider in FR-015 Screen 4 (immediate or scheduled). The normal deactivation cascade runs, and the status becomes Deactivated | Removes a status FR-015 does not define |
| Obligation checks | The request is blocked while bookings are active or payouts are pending (B13 and B14) | No blocking check. The FR-015 deactivation cascade cancels non-terminal cases, and FR-017 reconciles captured payments | The FR-015 cascade already handles open obligations |
| Account statuses | Adds `Deleted` | No new status. Only FR-015's Active, Suspended and Deactivated are used | One status owner |
| Entity 5 | Provider Account Deletion Request | Provider Account Closure Request. An approved request links to the FR-015 deactivation status event | Traceability |

## Scope and Impact

### In Scope

- Wording, flow, rules, requirements and the entity for the provider account-closure request in FR-032
- The FR-015 admin flow for processing a closure request

### Out of Scope

- Permanent erasure of provider data. Data is still archived for the FR-023 retention period.
- Any change to the FR-015 deactivation cascade itself

### Affected Contracts

- **PRD owner**: `functional-requirements/fr032-provider-dashboard-settings/prd.md`
- **Related FRs**:
  - FR-015 v1.14 (A7, Screen 4, Rule 4, edge cases)
  - FR-017 (post-deactivation payment reconciliation)
  - FR-020 (`provider.deactivated` email)
  - FR-023 (data retention)
- **System documents**: `system-data-schema.md` v1.5.0 adds §40 `provider_account_closure_requests` and confirms there is no `deleted` provider status (the schema never had one).

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed.
- **Required assessment**:
  - the provider account-closure UI and request API;
  - any implemented `Deleted` status or deletion-request table;
  - the admin request queue in Provider Management;
  - the link from an approved request to the FR-015 deactivation action.
- **Compatibility / rollout risk**: Medium. Any provider already stored as `Deleted` must be mapped to Deactivated.
- **Data migration**:
  - Map any existing `Deleted` provider status to Deactivated.
  - Rename or migrate deletion-request records to closure-request records.

## Acceptance and Validation

- A provider submits a closure request even while bookings are active, and the account stays Active until an admin acts.
- An admin deactivates the provider from the request. The status becomes Deactivated, the FR-015 cascade runs, the request becomes Approved, and the provider receives the deactivation email.
- No provider record can hold a `Deleted` status.
- Implementation evidence is required before reconciliation is marked Verified.

## Approval and Traceability

- **Requested by**: verify-fr pass on FR-015 v1.13
- **Approved by**: Product Owner (Joachim Trung Tuan), 2026-10-15
- **Decision evidence**: AskUserQuestion decisions and the "Yes" approval in the FR-015 sixth verification session
- **PRD change log**: FR-032 v1.8 row (2026-10-15); FR-015 v1.14 row
- **Update log**: [FR015_SIXTH_VERIFICATION_FIXES_2026-10-15.md](../../update-logs/2026-10-15/FR015_SIXTH_VERIFICATION_FIXES_2026-10-15.md)
- **Supersedes**: None
- **Superseded by**: None
