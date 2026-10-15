# FR-015 Sixth Verification Pass Fixes and FR-032, FR-020 Change Requests

**Date**: 2026-10-15
**Update Type**: Major requirement alignment (verification fixes, two new Change Requests)
**PRD Versions**: FR-015 v1.13 → v1.14; FR-032 v1.7 → v1.8; FR-020 v2.4 → v2.5; FR-030 v1.9 → v1.10; FR-009 v1.4 (proposed, minor alignment row); system data schema v1.4.0 → v1.5.0
**Decision Status**: Documentation approved by Product Owner (2026-10-15)
**Implementation Reconciliation**: Required — not assessed
**Change Requests**: CR-FR032-20261015-02, CR-FR020-20261015-01, CR-FR030-20261015-01

## Decision and Evidence

A sixth verify-fr pass on FR-015 v1.13 found 1 critical, 3 medium and 2 minor issues. The Product Owner chose the recommended option for each issue through AskUserQuestion and approved the proposed edits with "Yes". FR-032 and FR-020 gained new contracts, so each got a Change Request.

## Changes

- **Account closure (Issue 1, critical)**:
  - FR-032 "Delete Account" is now "Request account closure". An admin processes the request in FR-015 by deactivating the provider through Screen 4, and the normal cascade runs.
  - The `Deleted` status is removed, and so are the blocks for active bookings and pending payouts (the former B13 and B14 of the deletion flow).
  - FR-015 gains Alternative Flow A7, Admin Processes a Provider Account-Closure Request, and an updated closure edge case. FR-032 Entity 5 is renamed Provider Account Closure Request (CR-FR032-20261015-02).
- **Provider lifecycle emails (Issue 2)**:
  - FR-020 adds three provider events:
    - `provider.activation`: mandatory and cannot be disabled; sends the welcome email with the set-password link.
    - `provider.reactivated`.
    - `provider.scheduled_change_cancelled`.
  - `account.created` is now Patient only.
  - FR-015 Main Flow step 13, A1, A6, Screen 4 and the FR-020 dependency now reference these events (CR-FR020-20261015-01).
- **Seat requests (Issue 3)**: FR-015 Rule 7 and FR-009 (Screen 2 banner and invite form) now say that "Request more seats" opens an FR-034 support case, pre-filled as a seat-increase request. The admin then edits Seat Limit in FR-015 Tab 1.
- **Email uniqueness (Issue 4)**: Login Email and Contact Email must be unique among Active and Suspended providers only. Deactivated records are ignored, so a re-onboarded provider can reuse an email. The change covers:
  - FR-015 Rule 4, the Step 1 and Step 3 rows, the Tab 1 rows, REQ-015-014, Key Entities 1 and 3, and the duplicate-email edge cases;
  - the FR-032 Contact Email row.
- **Provider-side view (Issue 5)**: FR-015 Entry Points and User Story 1 scenario 2 now point to:
  - FR-032 Screen 4 Billing Settings, the Commission & Payout panel (Owner only);
  - FR-032 Tab 6 Documents;
  - the FR-032 Rule 6 status banner.
- **Minor (Issue 6)**:
  - Main Flow step 6 now lists Location City/Country, Contact Phone (Public) and Website URL.
  - The Step 3 "Clinic Phone" field is renamed Contact Phone (Public).
  - The commission attributes moved out of Key Entity 1 into a link note to FR-029 `provider_commissions`.
  - The reported stray trailing `activation_email` was not present in v1.13, so no change was needed.

## Files Updated

- [FR-015 PRD](../../functional-requirements/fr015-provider-management/prd.md): v1.14, A7, header CR links, Reconciliation boundary, change log, approvals
- [FR-032 PRD](../../functional-requirements/fr032-provider-dashboard-settings/prd.md): v1.8, Request Account Closure flow, Screen 2 card, rules, Assumption 2, User Story 7, REQ-032-013/020/023, Entity 5, Contact Email row, change log
- [CR-FR032-20261015-02](../../functional-requirements/fr032-provider-dashboard-settings/change-request-2026-10-15-account-closure-deactivation-request.md): new
- [FR-020 PRD](../../functional-requirements/fr020-notifications-alerts/prd.md): v2.5, event catalogue, Provider Lifecycle Notifications rule, FR-015 dependency, change log
- [CR-FR020-20261015-01](../../functional-requirements/fr020-notifications-alerts/change-request-2026-10-15-provider-lifecycle-events.md): new
- [FR-009 PRD](../../functional-requirements/fr009-provider-team-roles/prd.md): "Request more seats" routing in Screen 2, change log row

The Product Owner approved two follow-ups with "Yes for both questions":

- [FR-030 PRD](../../functional-requirements/fr030-notification-rules-config/prd.md): v1.10. Adds the three provider events to the source-of-truth catalog with locked toggles, makes `account.created` Patient only, and expands the FR-015 dependency. FR-020 gains REQ-020-015.
- [CR-FR030-20261015-01](../../functional-requirements/fr030-notification-rules-config/change-request-2026-10-15-provider-lifecycle-events.md): new
- [System data schema](../../system-data-schema.md): v1.5.0. `providers.email` uses a partial unique index (`active` and `suspended` only). Adds email-reuse rules for owner (§3) and team (§4) login emails, with the mechanism left to reconciliation. Confirms there is no `deleted` status. Adds a new §40 `provider_account_closure_requests` table.

## Follow-up

- The global UNIQUE on `users.email` and `provider_users.email` must be scoped so deactivated providers' login emails can be reused. The mechanism is decided during implementation reconciliation.
- Migration: map any stored `Deleted` provider status to Deactivated, and move any provider welcome email sent under `account.created` to `provider.activation`.
- Implementation reconciliation is required for everything listed above.

## Minor Follow-up: FR-009 Team-Member Email Uniqueness

- The Product Owner approved raising this as a separate fix ("Yes"). FR-009 Screen 2 said email uniqueness was "per org", which contradicted FR-009 A3, REQ-009-008 and the Key Entities (single-provider membership) and the schema §4 `provider_users.email` UNIQUE. The FR-009 invite-form Email row and business rule now say uniqueness is global: same-team duplicates get the View member / Resend invitation CTA, and other-team emails get the A3 blocking error. The schema already matched and is unchanged. No Change Request is needed because this is a wording clarification of the existing contract.
