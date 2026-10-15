# Change Request: Inquiry Distribution Requires a Set Password

**Change Request ID**: CR-FR003-20261015-01
**Primary FR**: FR-003
**Triggering FR / Event**: FR-015 v1.15 eighth verification pass, Issue 5 (inquiries before password set)
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-15
**Decision Date**: 2026-10-15
**PRD Version Change**: v2.7 to v2.8
**Related Commit(s)**: Pending

---

## Decision Summary

FR-015 creates providers as Active before they set a password (`password_set = false`). Under FR-003 they were eligible for inquiries at once, so inquiries could reach a provider who cannot log in yet. The Product Owner decided to keep such providers out of distribution until the password is set.

## Baseline State

**Source version**: FR-003 v2.7, Workflow 2 matching, General Inquiry Rule 6, REQ-003-019

- Only `Suspended` or `Deactivated` status blocked allocation; an Active provider without a password was eligible.

## Approved State

**Target version**: [FR-003 v2.8](prd.md), Workflow 2 matching, Rule 6, REQ-003-019

- An Active provider with `password_set = false` is not eligible for allocation, explicit patient selection, or reassignment.
- It becomes eligible once the password is set; inquiries distributed before then are not re-sent to it.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Distribution eligibility | Status not Suspended or Deactivated | Active and `password_set = true` | Provider cannot respond before logging in |
| Late eligibility | Not applicable | No retroactive distribution | Keep distribution timestamps and caps stable |

## Scope and Impact

### In Scope

- FR-003 Workflow 2 matching node, Rule 6, REQ-003-019, and this Change Request.

### Out of Scope

- Activation email and password setup (FR-015, FR-020).
- Quote submission rules (FR-004), which already require an Active provider.

### Affected Contracts

- **PRD owner**: `functional-requirements/fr003-inquiry-submission/prd.md`
- **Related FRs**: FR-015 v1.16 (Main Flow steps 12 and 21, Rules 3 and 9, FR-003 dependency)
- **System documents**: [System data schema](../../system-data-schema.md) v1.7.0 §2 `providers.password_set` and distribution eligibility rule

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed.
- **Required assessment**: the distribution matcher, the explicit provider selection list on the patient app, and admin reassignment.
- **Compatibility / rollout risk**: Low. If a patient explicitly selects a provider who has not set a password, the inquiry goes to the other matched providers, or to admin manual assignment (B1) if none remain.
- **Data migration**: None

## Acceptance and Validation

- A provider created but without a set password receives no inquiries.
- After the password is set, the provider receives new inquiries only.

## Approval and Traceability

- **Requested by**: verify-fr pass on FR-015 v1.15
- **Approved by**: Product Owner (Joachim Trung Tuan), 2026-10-15
- **Decision evidence**: AskUserQuestion decisions and the "Yes" approval in the FR-015 eighth verification session
- **PRD change log**: FR-003 v2.8 row (2026-10-15); FR-015 v1.16 row
- **Update log**: [FR015_EIGHTH_VERIFICATION_FIXES_2026-10-15.md](../../update-logs/2026-10-15/FR015_EIGHTH_VERIFICATION_FIXES_2026-10-15.md)
- **Supersedes**: None
- **Superseded by**: None
