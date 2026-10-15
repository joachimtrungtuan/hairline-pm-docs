# FR-015 Fourth Verification Pass Fixes, FR-029 Change Request, and FR-032 Clarification

**Date**: 2026-10-15
**Update Type**: Major requirement alignment (verification fixes, new Change Request)
**PRD Versions**: FR-015 v1.11 → v1.12; FR-029 v1.8 → v1.9; FR-032 v1.6 → v1.7 (clarification)
**Decision Status**: Documentation approved by Product Owner (2026-10-15)
**Implementation Reconciliation**: Required — not assessed
**Change Requests**: CR-FR029-20261015-01

## Decision and Evidence

A fourth verify-fr pass on FR-015 v1.11 found 1 critical, 2 medium, and 2 minor issues. The Product Owner decided each issue through AskUserQuestion and approved the proposed edits with "Yes". FR-029 is an already verified FR whose scope rules changed, so a Change Request was created. The FR-032 edit only clarifies an existing field and is recorded in its Change Log.

## Changes

- **Scheduled configuration source (Issue 1, critical)**: FR-032 Screen 4 "Scheduled Configuration" had no source in FR-015 Tab 7. Tab 7 now shows at most one pending future-dated configuration per provider. A newer future-dated edit replaces it (logged). It applies automatically on its Effective Date. An admin can cancel it with a reason and re-authentication.
- **Tab 1 commission duplication (Issue 2)**: Tab 1 now shows a read-only Commission Summary that links to Tab 7. Commission is edited only in Tab 7. The Tab 1 re-authentication rule now covers Seat Limit only.
- **Shared FR-029 scopes (Issue 3)**: A provider belongs to at most one active provider-specific scope. An FR-015 Tab 7 edit to a provider in a shared scope splits that provider into its own scope; the admin is warned first; the other providers are unchanged; the split is logged. FR-029 Screen 5 rejects a provider already in another active scope. Added REQ-029-048.
- **Standalone aftercare (Issue 4)**: A5 step 1 and the Screen 4 Suspension and Deactivation impact lists now include FR-011 standalone aftercare cases assigned to the provider.
- **Resend Activation Email (Issue 5)**: The Screen 3 button shows only when the password is not set and status = Active, matching Alternative Flow A1.

## Files Updated

- [FR-015 PRD](../../functional-requirements/fr015-provider-management/prd.md) — v1.12, change log, approvals
- [FR-029 PRD](../../functional-requirements/fr029-payment-system-config/prd.md) — v1.9, Screen 5 validation and business rules, REQ-029-048, change log
- [CR-FR029-20261015-01](../../functional-requirements/fr029-payment-system-config/change-request-2026-10-15-single-provider-scope-scheduled-commission.md) — new
- [System data schema](../../system-data-schema.md) — v1.3.0: §2B `provider_commissions` gets `pending` status, partial unique indexes (one active and one pending provider-specific row per provider), and replace, cancel, activation, and split rules
- [FR-032 PRD](../../functional-requirements/fr032-provider-dashboard-settings/prd.md) — v1.7 change log row; Screen 4 Scheduled Configuration description

## Follow-up

- Implementation reconciliation is required for scope membership uniqueness, the Tab 7 split path, pending-configuration storage and activation, and the Tab 1 read-only summary.
- FR-029 header now carries an explicit `**Version**: 1.9` line (follow-up, Product Owner approved).
