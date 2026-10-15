# FR-015 Third Verification Pass Fixes and FR-032 Alignment

**Date**: 2026-10-15
**Update Type**: Major requirement alignment (verification fixes, new Change Request)
**PRD Versions**: FR-015 v1.10 → v1.11; FR-032 v1.5 → v1.6
**Decision Status**: Documentation approved by Product Owner (2026-10-15)
**Implementation Reconciliation**: Required — not assessed
**Change Requests**: CR-FR032-20261015-01

## Decision and Evidence

A third verify-fr pass on FR-015 v1.10 found 2 critical, 3 medium, and 4 minor issues. The Product Owner decided each issue through AskUserQuestion and approved the proposed edits. FR-032 is Verified & Approved, so its change has a Change Request.

## Changes

- **Provider commission view (Issue 1)**: FR-032 Screen 4 gets a read-only Commission & Payout panel (Owner only, in Billing Settings). FR-015 Module Scope and Tab 7 point to it.
- **Last Activity Date (Issue 2)**: Defined as the most recent of the last FR-004 Parent Quote submission and FR-006 booking confirmation. Providers without one are excluded when filtering by it.
- **Permissions (Issue 3)**: The undefined Provider Manager and Read-Only Admin roles were replaced with FR-031 View, Onboard, Edit, and Suspend Providers. Login as Provider is Super Admin only. A-01 was corrected to FR-031 / A-09.
- **Suspended banner (Issue 4)**: New FR-032 Rule 6 covers Suspended (banner with admin reason, view-only with listed exceptions), Deactivated (login blocked), and Reactivated behavior. FR-015 references it.
- **Commission sort (Issue 5)**: Grouped by model. Percentage is sorted by value; Flat Rate by currency and then amount. Amounts in different currencies are never compared.
- **Minor**: Status Count Tiles on Screen 1 (SC-012); server-side filtering and sorting; a blank or today Effective Date applies immediately; Rule 2 includes the conditional Flat Rate Currency.

## Files Updated

- [FR-015 PRD](../../functional-requirements/fr015-provider-management/prd.md) — v1.11, change log, approvals
- [FR-032 PRD](../../functional-requirements/fr032-provider-dashboard-settings/prd.md) — v1.6: Screen 4 panel, Rule 6, REQ-032-029 and REQ-032-030, FR-015 dependency
- [CR-FR032-20261015-01](../../functional-requirements/fr032-provider-dashboard-settings/change-request-2026-10-15-provider-commission-panel-suspension-banner.md)
