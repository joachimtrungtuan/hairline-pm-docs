# Change Request: Assign Global Custom Provider Roles

**Change Request ID**: CR-FR009-20260929-01  
**Primary FR**: FR-009  
**Triggering FR / Event**: Proposed FR-031 provider role creation and cloning  
**Decision Status**: Proposed  
**Implementation Reconciliation**: Required  
**Requested Date**: 2026-09-29  
**Decision Date**: Pending  
**PRD Version Change**: v1.2 to proposed v1.3  
**Related Commit(s)**: Pending

## Decision Summary

The proposed FR-031 custom provider roles need an assignment path in FR-009. Provider organizations may select active global custom roles for non-Owner staff; role creation and permission editing remain with Super Admins.

## Baseline State

**Source version**: FR-009 v1.2, Provider Role Model, invitation and role-change flows, and Business Rules.

The provider assignment controls enumerate Manager, Clinical Staff, and Billing Staff. Role-permission definitions are centrally configured, and the primary Owner cannot be reassigned through provider-facing flows.

## Approved State

**Target version**: Proposed FR-009 v1.3, Provider Role Model and assignment flows. **Approval is pending.**

Invitation and role-change controls include active global custom roles from FR-031. Each custom role carries a non-Owner base type and current permission grants. Provider organizations cannot create, clone, or modify the global role definition, and the primary Owner invariant remains intact.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Assignable roles | Non-Owner protected roles only | Non-Owner protected roles plus active global custom roles | Let clinics use centrally defined specialist roles |
| Role display and comparison | Fixed four-role labels | Display and compare the current role catalog and permission matrix | Avoid stale or misleading access summaries |
| Protected actions | Fixed role identity and permission checks | Non-Owner custom roles also require matching base-type eligibility and explicit grants | Preserve Owner and role-limited safeguards |

## Scope and Impact

### In Scope

- Invitation and role-change selection, role display, permission comparison, and enforcement for global custom provider roles.
- Alignment of provider team entities and requirements with FR-031 as the role-definition owner.

### Out of Scope

- Clinic-specific role creation or permission editing.
- Owner assignment, Owner cloning, custom-role deletion, or a new team-member lifecycle.
- Frontend or backend implementation in this documentation change.

### Affected Contracts

- **PRD owner**: `fr009-provider-team-roles/prd.md` — Provider Role Model, invitation and role-change flows, Business Rules, and REQ-009-002.
- **Related FR**: `fr031-admin-access-control/prd.md` — global custom role creation, cloning, and permission governance; see CR-FR031-20260929-01.
- **System documents**: `system-prd.md` — FR-009 summary.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed; `main/` was not read for this documentation change.
- **Required assessment**: Role catalog responses, invitation and assignment validation, current permission comparison, active-session changes, protected-action checks, audit records, and tests.
- **Existing cross-FR decision gap**: FR-009 REQ-009-005 allows Manager removal, while FR-031 marks Remove Team Members Owner-only. Keep the existing baseline wording pending a product decision; do not infer removal rights for custom Manager-base roles from cloning alone.
- **Compatibility / rollout risk**: Existing team members keep their current protected roles; a custom role must not be mistaken for Owner or gain a protected action from a permission string alone.
- **Data migration**: To be assessed if role assignments or invitations store fixed role names rather than role identifiers.

## Acceptance and Validation

- An active custom role appears for non-Owner staff invitation and role change across provider organizations.
- Assignment uses the current FR-031 permission matrix and preserves the primary Owner and base-type safeguards.
- Existing protected role assignments remain valid, with no access change solely from the catalog expansion.
- Implementation status remains unverified until source and tests are assessed.

## Approval and Traceability

- **Requested by**: User in the 2026-09-29 Codex conversation.
- **Approved by**: Pending product and security review.
- **Decision evidence**: User request to add provider role creation and cloning to FR-031; FR-009 assignment alignment follows from that proposal.
- **PRD change log**: Proposed v1.3 row in FR-009.
- **Update log**: `../../update-logs/2026-09-29/FR031_GLOBAL_CUSTOM_PROVIDER_ROLES_2026-09-29.md`.
- **Supersedes**: None.
- **Superseded by**: None.
