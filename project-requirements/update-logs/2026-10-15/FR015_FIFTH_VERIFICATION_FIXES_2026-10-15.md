# FR-015 Fifth Verification Pass Fixes and FR-009, FR-017, FR-026 Change Requests

**Date**: 2026-10-15
**Update Type**: Major requirement alignment (verification fixes, three new Change Requests)
**PRD Versions**: FR-015 v1.12 → v1.13; FR-009 v1.3 → v1.4 (proposed); FR-017 v2.9 → v2.10; FR-026 v1.10 → v1.11; system data schema v1.3.0 → v1.4.0
**Decision Status**: Documentation approved by Product Owner (2026-10-15)
**Implementation Reconciliation**: Required — not assessed
**Change Requests**: CR-FR009-20261015-01, CR-FR017-20261015-01, CR-FR026-20261015-01

## Decision and Evidence

A fifth verify-fr pass on FR-015 v1.12 found 0 critical, 4 medium, and 3 minor issues. The Product Owner decided each issue through AskUserQuestion and approved the proposed edits with "Yes". FR-009, FR-017, and FR-026 gained new contracts, so each got a Change Request.

## Changes

- **Impersonation (Issue 1)**: FR-015 "Login as Provider" stays limited-write: admins can act for the provider but cannot change password, login email, or financial settings. FR-009 Impersonate was read-only; it now follows the FR-015 rules (CR-FR009-20261015-01).
- **Admin staff invite (Issue 2)**: FR-015 Tab 3 now shows only this provider's team, via the new FR-009 Screen 12: Provider Team (Admin, Single Provider). It adds Invite Staff Member. The invite is blocked at the Seat Limit or when the provider is Suspended or Deactivated, and needs FR-031 "Edit Providers". New requirements REQ-009-023 to REQ-009-025 (CR-FR009-20261015-01).
- **Reactivation vs scheduled change (Issue 3)**: Screen 5 reactivation now cancels any pending scheduled suspension or deactivation. Screen 5 warns first, and the cancellation is logged in Tab 8. Updated A6 and the Screen 4 rules. Added Key Entity 4: Pending Provider Status Change.
- **Payments after suspension (Issue 4)**: FR-015 Rule 9 now names FR-017 as the owner. FR-017 has a new Workflow B3, Rules 14-16, a Screen 4 Reconciliation Flag ("Captured after provider cancellation"), and REQ-017-028 and REQ-017-029. Late captures are recorded, never confirm a booking, and are held from payout until admin resolution. Remaining installments are cancelled. FR-007 is unchanged (CR-FR017-20261015-01). The FR-015 Reconciliation boundary now also lists FR-005, FR-006, FR-007, FR-009, FR-017, and FR-026.
- **Specialty list (Issue 5)**: FR-015 Specialty now uses the FR-026 Provider Specialties list (Settings → App Data, Screen 5f). The seed values are Hair Transplant Surgeon, Dermatologist, Trichologist, Plastic Surgeon, and Other. Values are deactivated, never deleted. Added REQ-026-012h and Entity 7a (CR-FR026-20261015-01).
- **Minor (Issues 6-7)**: SC-010 now says "create (Active)" and covers scheduled changes. SC-015 lists the real Screen 3 tabs. User Story 3 moved to P1.

## Files Updated

- [FR-015 PRD](../../functional-requirements/fr015-provider-management/prd.md) — v1.13, header CR links, change log, approvals
- [FR-009 PRD](../../functional-requirements/fr009-provider-team-roles/prd.md) — v1.4 (proposed), Screens 10-12, REQ-009-023 to 025, change log
- [CR-FR009-20261015-01](../../functional-requirements/fr009-provider-team-roles/change-request-2026-10-15-admin-staff-invite-impersonation.md) — new
- [FR-017 PRD](../../functional-requirements/fr017-admin-billing-finance/prd.md) — v2.10, Workflow B3, Rules 14-16, Screen 4, entities, REQ-017-028 and 029, change log
- [CR-FR017-20261015-01](../../functional-requirements/fr017-admin-billing-finance/change-request-2026-10-15-post-suspension-payment-reconciliation.md) — new
- [FR-026 PRD](../../functional-requirements/fr026-app-settings-security/prd.md) — v1.11, A9, Screen 5f, Entity 7a, REQ-026-012h, change log
- [CR-FR026-20261015-01](../../functional-requirements/fr026-app-settings-security/change-request-2026-10-15-provider-specialty-list.md) — new

- [System data schema](../../system-data-schema.md) — v1.4.0 (Product Owner follow-up "Yes"): new §38 `provider_pending_status_changes` (one pending row per provider; reactivation cancels it); new §39 `provider_specialties` and `providers.specialty_id`; §12 `payments.reconciliation_flag` and `provider_status_event_id`, `cancelled` payment status for stopped installments; §31 plan cancelled on provider-status cancellation. FR-017's invoice and installment entities map to `payments` and `installment_payment_plans`, because the schema has no separate invoice table.

## Follow-up

- Migration: existing free-text specialty values must be mapped to Provider Specialties list IDs.
- Implementation reconciliation is required for all of the above, plus limited-write impersonation and the admin invite path.
