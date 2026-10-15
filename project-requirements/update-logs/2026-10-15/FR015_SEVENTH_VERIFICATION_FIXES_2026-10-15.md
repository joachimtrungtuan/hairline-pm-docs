# FR-015 Seventh Verification Pass Fixes and FR-009 Change Request

**Date**: 2026-10-15
**Update Type**: Major requirement alignment (verification fixes, one new Change Request)
**PRD Versions**: FR-015 v1.14 → v1.15; FR-009 v1.4 (proposed) → v1.5 (proposed); system data schema v1.5.0 → v1.6.0
**Decision Status**: Documentation approved by Product Owner (2026-10-15)
**Implementation Reconciliation**: Required — not assessed
**Change Requests**: CR-FR009-20261015-02

## Decision and Evidence

A seventh verify-fr pass on FR-015 v1.14 found 1 critical, 2 medium and 4 minor issues. The Product Owner chose the recommended option for each issue through AskUserQuestion and approved the edits with "Apply all now". FR-009 gained a new identity contract, so it got a Change Request.

## Changes

- **Global provider email identity (Issue 1, critical)**: FR-015 checked login email only against Active and Suspended provider owners, while FR-009 checked only team members. An owner email could collide with another clinic's staff member or pending invitation.
  - FR-009 Rule 3 and REQ-009-008 now define one global rule: an email belongs to at most one provider organization at a time, as Owner, team member, or pending invitation.
  - When a provider is Deactivated, its Owner, staff, and pending-invitation emails are freed for reuse; old records stay archived.
  - FR-009 A3, Screen 2 and Screen 12 email validation, and the FR-015 dependency note now use this rule (CR-FR009-20261015-02).
  - FR-015 Screen 2 Step 1, Tab 1, Rule 4, REQ-015-014, Key Entity 1, and the duplicate-email edge cases point to the FR-009 rule. The Contact Email rule (Active and Suspended providers only) is unchanged.
- **Notification event names (Issue 2)**: FR-015 Integration 1 now uses `provider.activation` instead of "provider.activated". Data Dependency Entity 2 lists the FR-020 provider lifecycle events and drops the "provider_activation_email" template ID example; templates are configured in FR-030.
- **Tab 6 upload modal (Issue 3)**: Added Upload Document Modal Fields:
  - File: required; PDF/JPG/PNG/DOCX/XLSX; max 10MB.
  - Document Type: required; Medical License, Board Certification, Insurance (general), Malpractice Insurance, Business License, Other.
  - Notes: optional; max 500 chars.
- **Minor**:
  - Module placeholders replaced: P-02, PR-01 and PR-06, S-03, S-05 and S-06.
  - Provider-side "read-only" wording (FR-009 dependency, Integration 3, module overview) now says providers read A-02 data and edit allowed fields via FR-032.
  - Key Entity 2 gains `file_size`.
  - Data Dependency Entity 1 now matches the FR-031 matrix: all default roles have View Providers; only Super Admin has Edit, Onboard, and Suspend Providers by default.

## Files Updated

- [FR-015 PRD](../../functional-requirements/fr015-provider-management/prd.md): v1.15, header CR link, email rows, Rule 4, REQ-015-014, edge cases, Tab 6 modal, dependencies, integrations, entities, change log, approvals
- [FR-009 PRD](../../functional-requirements/fr009-provider-team-roles/prd.md): v1.5 (proposed), Rule 3, REQ-009-008, A3, Screens 2 and 12, FR-015 dependency, change log
- [CR-FR009-20261015-02](../../functional-requirements/fr009-provider-team-roles/change-request-2026-10-15-global-provider-email-identity.md): new

The Product Owner then asked to align the schema ("Please fix that in the system data schema too"):

- [System data schema](../../system-data-schema.md): v1.6.0. §3 `users` and §4 `provider_users` business rules now state the global provider email identity rule across owner accounts, team members, and pending `provider_staff_invitations`, with deactivated providers' emails freed and records archived. Enforcement needs a shared check across the three tables; the exact mechanism is left to reconciliation. The §2 note now separates contact-email reuse from login emails.

## Follow-up

- Choose the enforcement mechanism for the global rule during reconciliation (shared application check or shared identity table, plus scoped per-table indexes). `provider_staff_invitations` has no column spec in the schema yet.
- Audit existing data for cross-provider email conflicts before enforcing the rule.
- Implementation reconciliation is required for everything listed above.
