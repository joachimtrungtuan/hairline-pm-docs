# Change Request: Global Custom Provider Roles

**Change Request ID**: CR-FR031-20260929-01  
**Primary FR**: FR-031  
**Triggering Event**: Product request to add provider role creation and cloning  
**Decision Status**: Proposed  
**Implementation Reconciliation**: Required  
**Requested Date**: 2026-09-29  
**Decision Date**: Pending  
**PRD Version Change**: v1.0.2 to proposed v1.1  
**Related Commit(s)**: Pending

## Decision Summary

The proposed revision lets Super Admins create and clone provider roles centrally while preserving the four protected roles and a single primary Owner per organization. Global role definitions keep permission governance in FR-031; provider organizations assign those roles through FR-009 without editing their definitions.

## Baseline State

**Source version**: FR-031 v1.0.2, Provider Roles and Business Rules.

Provider roles are the four system-defined roles. Super Admins may edit their permission matrices, but cannot add a provider role. The Provider Roles tab offers Edit Permissions and View Users only.

## Approved State

**Target version**: Proposed FR-031 v1.1, Provider Roles and Business Workflows. **Approval is pending.**

Super Admins can create global custom provider roles with a non-Owner base type and can clone non-Owner provider roles into independent custom roles. Owner cannot be cloned, and custom roles cannot acquire Owner-only capabilities. FR-031 remains the sole owner of provider role definitions and permissions.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Provider role catalog | Four protected roles only | Four protected roles plus global custom roles | Support specialized staff access without changing the protected roles |
| Creation and cloning | No provider role creation or clone action | Super Admin creates or clones a non-Owner custom role with a unique name, description, base type, and eligible permissions | Reuse a known permission set while retaining central governance |
| Owner protection | Exactly one primary Owner per organization | Owner remains uncloneable; custom roles cannot gain Owner-only capabilities or become primary Owner | Preserve ownership and high-risk account controls |
| Assignment handoff | FR-009 presents protected roles | FR-009 also presents active custom roles for non-Owner staff | Make new roles usable without clinic-side role-definition editing |

## Scope and Impact

### In Scope

- Global custom provider role creation and cloning by Super Admins.
- Non-Owner base types, permission selection, source snapshot independence, protected-action checks, audit trail, and propagation to FR-009 role assignment.

### Out of Scope

- Clinic-specific role definitions or clinic-side permission editing.
- Cloning or replacing Owner, deleting custom provider roles, or changing the primary Owner assignment flow.
- Backend or frontend implementation in this documentation change.

### Affected Contracts

- **PRD owner**: `fr031-admin-access-control/prd.md` — Provider Roles, Screen 4, Business Rules, and REQ-031-005.
- **Related FR**: `fr009-provider-team-roles/prd.md` — role model, invitation, role change, and role-permission consumption; see CR-FR009-20260929-01.
- **System documents**: `system-prd.md` — FR-009 and FR-031 summaries. `system-data-schema.md` Roles currently lacks explicit custom-role base-type metadata; storage design must be assessed before implementation.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed; `main/` was not read for this documentation change.
- **Required assessment**: Role storage and guard scoping, Super Admin authorization, create/clone API contracts, protected-action enforcement, provider invitation and reassignment catalogs, permission propagation, audit records, and regression tests.
- **Existing cross-FR decision gap**: FR-031 lists Remove Team Members as Owner-only, while FR-009 REQ-009-005 allows Owners and Managers to remove non-Owner members. This revision does not choose between those rules; resolve the actor policy before granting removal to any custom base type.
- **Compatibility / rollout risk**: Existing assignments must retain their role IDs and access. A new role must not grant Owner-only or base-type-restricted actions through copied permission names alone.
- **Data migration**: To be assessed for base-type metadata and existing role records.

## Acceptance and Validation

- A Super Admin can create a unique global custom provider role with a Manager, Clinical Staff, or Billing Staff base type and at least one eligible permission.
- Cloning a non-Owner role creates an independent non-system role; cloning Owner or granting Owner-only actions is rejected.
- An active custom role appears in non-Owner invitation and role-change choices across provider organizations, with current permissions enforced on subsequent API calls.
- FR-009 and the system PRD agree on assignment and Owner restrictions; implementation reconciliation remains unverified until code and tests are assessed.

## Approval and Traceability

- **Requested by**: User in the 2026-09-29 Codex conversation.
- **Approved by**: Pending product and security review.
- **Decision evidence**: User request to add provider role creation and cloning to FR-031; global scope and base-type model are proposed design details pending confirmation.
- **PRD change log**: Proposed v1.1 row in FR-031.
- **Update log**: `../../update-logs/2026-09-29/FR031_GLOBAL_CUSTOM_PROVIDER_ROLES_2026-09-29.md`.
- **Supersedes**: None.
- **Superseded by**: None.
