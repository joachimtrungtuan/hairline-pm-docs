# Change Request: Suspended Providers in Provider-Specific Commission Scopes

**Change Request ID**: CR-FR029-20261015-02
**Primary FR**: FR-029
**Triggering FR / Event**: FR-015 v1.15 eighth verification pass, Issue 3 (commission edit eligibility)
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-15
**Decision Date**: 2026-10-15
**PRD Version Change**: v1.9 to v1.10
**Related Commit(s)**: Pending

---

## Decision Summary

FR-015 Tab 7 had no provider-status rule for commission edits, while FR-029 Screen 5 accepted only active providers. The two surfaces must stay synchronized. The Product Owner decided that Active and Suspended providers may have their commission edited (so terms can be fixed before reactivation), and Deactivated providers are read-only.

## Baseline State

**Source version**: FR-029 v1.9, Workflow step 10, Screen 5 Selected Providers validation

- Step 10: "System validates selected providers are active".
- Selected Providers: "Minimum 1 active provider".
- FR-015 Tab 7 allowed edits regardless of status.

## Approved State

**Target version**: [FR-029 v1.10](prd.md), Workflow step 10, Screen 5 Selected Providers validation

- Providers with status Active or Suspended may be selected and edited.
- Deactivated providers cannot be selected; their existing scopes are read-only.
- FR-015 Tab 7 applies the same rule (FR-015 v1.16).

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Scope eligibility | Active providers only | Active or Suspended | Allow fixing terms before reactivation |
| Deactivated providers | Not stated | Cannot be selected; scopes read-only | Deactivation is terminal |
| FR-015 Tab 7 | No status rule | Same rule as FR-029 | Keep both surfaces synchronized |

## Scope and Impact

### In Scope

- FR-029 step 10, Screen 5 Selected Providers validation, and this Change Request.

### Out of Scope

- Commission models, precision, snapshot timing, and the one-scope-per-provider rule (unchanged).

### Affected Contracts

- **PRD owner**: `functional-requirements/fr029-payment-system-config/prd.md`
- **Related FRs**: FR-015 v1.16 (Tab 7 edit eligibility)
- **System documents**: [System data schema](../../system-data-schema.md) v1.7.0 §2B provider-specific row status rule

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed.
- **Required assessment**: the provider picker and server validation for provider-specific scopes, and the FR-015 Tab 7 edit guard.
- **Compatibility / rollout risk**: Low. A Suspended provider's new configuration applies only to bookings confirmed after reactivation, because Suspended providers cannot confirm bookings.
- **Data migration**: None

## Acceptance and Validation

- A Suspended provider can be added to a provider-specific scope and edited in FR-015 Tab 7.
- A Deactivated provider cannot be selected in Screen 5, and its Tab 7 is read-only.

## Approval and Traceability

- **Requested by**: verify-fr pass on FR-015 v1.15
- **Approved by**: Product Owner (Joachim Trung Tuan), 2026-10-15
- **Decision evidence**: AskUserQuestion decisions and the "Yes" approval in the FR-015 eighth verification session
- **PRD change log**: FR-029 v1.10 row (2026-10-15); FR-015 v1.16 row
- **Update log**: [FR015_EIGHTH_VERIFICATION_FIXES_2026-10-15.md](../../update-logs/2026-10-15/FR015_EIGHTH_VERIFICATION_FIXES_2026-10-15.md)
- **Supersedes**: None
- **Superseded by**: None
