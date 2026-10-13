# FR-031 Global Custom Provider Roles — Proposed PRD Revision

**Date**: 2026-09-29  
**Status**: Proposed; product and security approval pending  
**Implementation reconciliation**: Required; source code not assessed

## Summary

FR-031 v1.1 proposes global custom provider roles that Super Admins can create or clone from non-Owner roles. Each custom role has a Manager, Clinical Staff, or Billing Staff base type and explicit permission grants. The protected Owner role cannot be cloned, replaced, or granted through a custom role.

FR-009 v1.3 proposes offering active custom roles in non-Owner invitation and role-change flows. The system PRD summaries for FR-009 and FR-031 now point to the same global role model. Neither provider organizations nor their staff gain permission-definition controls.

## Contract and Approval

- [FR-031 PRD](../../functional-requirements/fr031-admin-access-control/prd.md) and [CR-FR031-20260929-01](../../functional-requirements/fr031-admin-access-control/change-request-2026-09-29-global-custom-provider-roles.md) own role creation, cloning, permissions, and Owner protection.
- [FR-009 PRD](../../functional-requirements/fr009-provider-team-roles/prd.md) and [CR-FR009-20260929-01](../../functional-requirements/fr009-provider-team-roles/change-request-2026-09-29-custom-provider-role-assignment.md) own provider team assignment and enforcement handoff.
- The user requested provider role creation and cloning in the 2026-09-29 Codex conversation. The global scope and base-type design are proposed details pending confirmation; prior PRD approvals are not extended to these revisions.

## Remaining Reconciliation

- Confirm product and security approval for global scope and base-type eligibility.
- Assess role storage, create/clone APIs, provider invitation catalogs, guard-scoped uniqueness, permission propagation, audit logs, and Owner-only enforcement against implementation.
- Resolve the existing FR-009 Manager-removal versus FR-031 Owner-only removal mismatch before specifying removal rights for custom roles.
- Keep existing protected-role assignments valid during rollout. Implementation and testing are not claimed by this document update.
