# Change Request: Provider Lifecycle Events in the Notification Event Catalog

**Change Request ID**: CR-FR030-20261015-01
**Primary FR**: FR-030
**Triggering FR / Event**: FR-020 v2.5 (CR-FR020-20261015-01) and FR-015 v1.14 sixth verification pass, Issue 2
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-15
**Decision Date**: 2026-10-15
**PRD Version Change**: v1.9 to v1.10
**Related Commit(s)**: Pending

---

## Decision Summary

FR-030 is the source of truth for notification event coverage. FR-020 v2.5 added three mandatory provider events for FR-015's activation, reactivation and scheduled-change cancellation emails. The Product Owner approved mirroring these events in the FR-030 catalog with locked toggles.

## Baseline State

**Source version**: FR-030 v1.9. The affected sections are the MVP Event Types table (Account/Auth and Provider/Compliance rows), "Non-Disableable by Default", and the FR-015 / FR-016 dependency.

The catalog's only provider-facing account events were `account.created` (Patient and Provider, optional), `provider.suspended` and `provider.deactivated`.

## Approved State

**Target version**: FR-030 v1.10. The changes are:

- three new catalog rows: `provider.activation`, `provider.reactivated` and `provider.scheduled_change_cancelled`;
- a new "Non-Disableable by Default" entry for those events;
- `account.created` limited to patients.

See the [FR-030 PRD](prd.md) for the full contract.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Event catalog | No provider activation, reactivation or scheduled-change-cancelled events | Adds the three events, each mapped to FR-015 triggers and FR-020 REQ-020-015 | Mirror FR-020 v2.5 |
| Toggle behavior | `account.created` could be disabled and covered provider onboarding | `provider.activation` is always locked. `provider.reactivated` and `provider.scheduled_change_cancelled` are locked, and they fire only when FR-015 "Notify Provider" applies | A disabled activation email blocks provider login |
| `account.created` | Patient and Provider | Patient only | Avoids a duplicate provider welcome email |

## Scope and Impact

### In Scope

- Catalog rows and the locked-toggle rule for the three provider events

### Out of Scope

- Template wording (configured in the Template Editor)
- SMS delivery

### Affected Contracts

- **PRD owner**: `functional-requirements/fr030-notification-rules-config/prd.md`
- **Related FRs**:
  - FR-020 v2.5 (CR-FR020-20261015-01, REQ-020-015)
  - FR-015 v1.14 (Main Flow step 13, A1, A6, Screens 4–5)
- **System documents**: None

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed
- **Required assessment**:
  - the seeded event catalog;
  - the toggle lock for the three events;
  - templates for each event;
  - moving any provider welcome email off `account.created`.
- **Compatibility / rollout risk**: Low
- **Data migration**: Seed the three event keys and templates

## Acceptance and Validation

- The Rules Dashboard lists the three events, and their toggles are locked.
- Disabling `account.created` does not stop provider activation emails.

## Approval and Traceability

- **Requested by**: verify-fr pass on FR-015 v1.13 (follow-up question approved with "Yes")
- **Approved by**: Product Owner (Joachim Trung Tuan), 2026-10-15
- **Decision evidence**: AskUserQuestion decisions, the "Yes" approval, and the follow-up "Yes for both questions" in the FR-015 sixth verification session
- **PRD change log**: FR-030 v1.10 row (2026-10-15)
- **Update log**: [FR015_SIXTH_VERIFICATION_FIXES_2026-10-15.md](../../update-logs/2026-10-15/FR015_SIXTH_VERIFICATION_FIXES_2026-10-15.md)
- **Supersedes**: None
- **Superseded by**: None
