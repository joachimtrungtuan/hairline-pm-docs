# Change Request: Mandatory Provider Lifecycle Notification Events

**Change Request ID**: CR-FR020-20261015-01
**Primary FR**: FR-020
**Triggering FR / Event**: FR-015 v1.13 (sixth verification pass, Issue 2)
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-15
**Decision Date**: 2026-10-15
**PRD Version Change**: v2.4 to v2.5
**Related Commit(s)**: Pending

---

## Decision Summary

FR-015 sends three provider emails that had no FR-020 event:

- the account activation email with the set-password link (Main Flow step 13 and A1);
- the reactivation email (A6 and Screen 5);
- the notice that a scheduled suspension or deactivation was cancelled.

The closest event, `account.created`, is marked optional and can be disabled. If it were disabled, a new provider could never set a password. The Product Owner approved adding three mandatory provider events to FR-020.

## Baseline State

**Source version**: FR-020 v2.4, Event catalogue (Account/Auth and Provider/Compliance rows) and Business Rules.

Only `account.created` (optional), `provider.suspended` and `provider.deactivated` covered these provider account emails.

## Approved State

**Target version**: FR-020 v2.5, Event catalogue rows for `provider.activation`, `provider.reactivated` and `provider.scheduled_change_cancelled`, and the Business Rule "Provider Lifecycle Notifications (FR-015)".

See the [FR-020 PRD](prd.md) for the full contract.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Activation email | Implied by the optional `account.created` event | `provider.activation` sends the welcome email with the one-time set-password link (24-hour expiry). It is mandatory, cannot be disabled, and is re-sent on FR-015 A1 resend | Without it, the provider cannot log in |
| Reactivation email | No event | `provider.reactivated` is sent when "Notify Provider" is checked in FR-015 Screen 5. It is mandatory in FR-030 rules | The FR-015 A6 email had no event |
| Scheduled change cancelled | No event | `provider.scheduled_change_cancelled` is sent when an admin cancels a scheduled suspension or deactivation (FR-015 Screen 4) and the scheduled change had "Notify Provider" on. When reactivation cancels a scheduled change automatically, the note goes in `provider.reactivated` instead. It is mandatory in FR-030 rules | The provider was told about a future change but never told it was cancelled |
| `account.created` | Patient and Provider, optional | Patient only. Provider onboarding uses `provider.activation` | Avoids a duplicate welcome email |
| Requirements | REQ-020-001 to REQ-020-014 | Adds REQ-020-015 for the three provider lifecycle events | Testable acceptance |

## Scope and Impact

### In Scope

- Three provider event keys, their recipients, mandatory status and content in FR-020

### Out of Scope

- FR-030 template wording (FR-030 owns the templates)
- SMS delivery

### Affected Contracts

- **PRD owner**: `functional-requirements/fr020-notifications-alerts/prd.md`
- **Related FRs**:
  - FR-015 v1.14 (Main Flow step 13, A1, A6, Screens 4–5, FR-020 dependency)
  - FR-030 (event catalogue, the source of truth for event coverage)
- **System documents**: None

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed.
- **Required assessment**:
  - the provider activation email trigger and whether it can currently be disabled;
  - the reactivation email trigger;
  - the scheduled-change cancellation email;
  - the FR-030 catalogue entries.
- **Compatibility / rollout risk**: Low. Any provider welcome email currently sent under `account.created` must move to `provider.activation` so it is not sent twice.
- **Data migration**: None

## Acceptance and Validation

- Creating a provider always sends the activation email, even if `account.created` is disabled.
- Reactivating a provider with "Notify Provider" checked sends `provider.reactivated`.
- Cancelling a scheduled suspension or deactivation that had "Notify Provider" on sends `provider.scheduled_change_cancelled`.
- FR-030 v1.10 lists all three events with locked toggles (CR-FR030-20261015-01).

## Approval and Traceability

- **Requested by**: verify-fr pass on FR-015 v1.13
- **Approved by**: Product Owner (Joachim Trung Tuan), 2026-10-15
- **Decision evidence**: AskUserQuestion decisions and the "Yes" approval in the FR-015 sixth verification session
- **PRD change log**: FR-020 v2.5 row (2026-10-15); FR-015 v1.14 row
- **Update log**: [FR015_SIXTH_VERIFICATION_FIXES_2026-10-15.md](../../update-logs/2026-10-15/FR015_SIXTH_VERIFICATION_FIXES_2026-10-15.md)
- **Supersedes**: None
- **Superseded by**: None
