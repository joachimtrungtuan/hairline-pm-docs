# FR-015 Eighth Verification Pass Fixes and FR-003, FR-020, FR-029, FR-030, FR-032 Change Requests

**Date**: 2026-10-15
**Update Type**: Major requirement alignment (verification fixes, five new Change Requests)
**PRD Versions**: FR-015 v1.15 → v1.16; FR-003 v2.7 → v2.8; FR-020 v2.5 → v2.6; FR-029 v1.9 → v1.10; FR-030 v1.10 → v1.11; FR-032 v1.8 → v1.9
**System Data Schema**: v1.6.0 → v1.7.0
**Decision Status**: Documentation approved by Product Owner (2026-10-15)
**Implementation Reconciliation**: Required — not assessed
**Change Requests**: CR-FR032-20261015-03, CR-FR020-20261015-02, CR-FR030-20261015-02, CR-FR029-20261015-02, CR-FR003-20261015-01

## Decision and Evidence

An eighth verify-fr pass on FR-015 v1.15 found 0 critical, 3 medium and 3 minor issues. The Product Owner chose the recommended option for each issue through AskUserQuestion and approved the edits with "Yes".

## Changes

- **Language list owner (Issue 1)**: Step 2 Languages Spoken, Tab 2 Supported Languages, and the Tab 2 notes now use the FR-021 central language catalog. Added an FR-021 dependency; the FR-026 dependency now lists only the country and Provider Specialties lists. No CR (wording).
- **Account closure follow-through (Issue 2)**:
  - FR-015 A7 and the Screen 4 Notify Provider row: "Notify Provider" is checked and locked for closure deactivations, so the email FR-032 promises is always sent.
  - Screen 1: new Closure Requested filter and marker for pending FR-032 requests.
  - New mandatory FR-020/FR-030 events: `provider.closure_requested` (admins, Email + in-app) and `provider.closure_rejected` (provider, email, with review notes). A7 rejection notes are now required (min 20 chars).
  - FR-032 steps 10, 15, and 16 use these events (CR-FR032-20261015-03, CR-FR020-20261015-02, CR-FR030-20261015-02).
- **Commission edit eligibility (Issue 3)**: Tab 7 edits are allowed for Active and Suspended providers; Deactivated providers are read-only. FR-029 step 10 and Screen 5 Selected Providers now accept Active or Suspended providers (CR-FR029-20261015-02).
- **Commission precision (Issue 4)**: Step 5 and Tab 7 Commission Value now follow FR-029: 0.1% for Percentage, currency minor units for Flat Rate.
- **No inquiries before password set (Issue 5)**: Main Flow steps 12 and 21, Rules 3 and 9, and the FR-003 dependency exclude providers with `password_set = false` from distribution. FR-003 Workflow 2, Rule 6, and REQ-003-019 apply the same rule, with no retroactive distribution (CR-FR003-20261015-01).
- **Integration 4 (Issue 6)**: Featured provider data is a REST call only; the public read-only endpoint is rate limited per the constitution rule for public-facing APIs.
- **System data schema reconciliation (v1.7.0)**:
  - §2 `providers`: new `password_set`, `activation_token_hash`, and `activation_token_expires_at` columns (REQ-015-011: one valid hashed token per provider, 24-hour expiry, overwritten on resend, cleared when the password is set) and (`status`, `password_set`) index; distribution eligibility rule (`active` and password set, no retroactive distribution); `provider_languages` reference the FR-021 `languages` catalog.
  - §2B `provider_commissions`: provider-specific rows writable only for `active` or `suspended` providers; `deactivated` is read-only.
  - §38 `provider_pending_status_changes`: a deactivation that processes a closure request must keep `notify_provider` = true.
  - §40 `provider_account_closure_requests` (already present): rejection notes required (min 20 chars) and sent in `provider.closure_rejected`; submission emits `provider.closure_requested`; Screen 1 marker reads the pending row; closure deactivations always notify; resubmission allowed after rejection.

## Files Updated

- [FR-015 PRD](../../functional-requirements/fr015-provider-management/prd.md): v1.16, header CR links, Main Flow, A7, Screens 1, 2, 3 (Tabs 2 and 7), and 4, Rules 3 and 9, dependencies, Integration 4, edge case, data dependency, change log, approvals
- [FR-003 PRD](../../functional-requirements/fr003-inquiry-submission/prd.md): v2.8, Workflow 2, Rule 6, REQ-003-019, change log
- [FR-020 PRD](../../functional-requirements/fr020-notifications-alerts/prd.md): v2.6, two catalog rows, deactivated row note, lifecycle rule, REQ-020-016, change log
- [FR-029 PRD](../../functional-requirements/fr029-payment-system-config/prd.md): v1.10, step 10, Selected Providers validation, change log
- [FR-030 PRD](../../functional-requirements/fr030-notification-rules-config/prd.md): v1.11, two catalog rows, deactivated row note, Non-Disableable rule, FR-015 dependency, change log
- [FR-032 PRD](../../functional-requirements/fr032-provider-dashboard-settings/prd.md): v1.9, Request Account Closure steps 10, 15, 16, change log
- New CRs:
  - [CR-FR032-20261015-03](../../functional-requirements/fr032-provider-dashboard-settings/change-request-2026-10-15-closure-request-notifications.md)
  - [CR-FR020-20261015-02](../../functional-requirements/fr020-notifications-alerts/change-request-2026-10-15-provider-closure-request-events.md)
  - [CR-FR030-20261015-02](../../functional-requirements/fr030-notification-rules-config/change-request-2026-10-15-provider-closure-request-events.md)
  - [CR-FR029-20261015-02](../../functional-requirements/fr029-payment-system-config/change-request-2026-10-15-suspended-provider-commission-scopes.md)
  - [CR-FR003-20261015-01](../../functional-requirements/fr003-inquiry-submission/change-request-2026-10-15-distribution-requires-password-set.md)
- [System data schema](../../system-data-schema.md): v1.7.0, §2, §2B, §38, §40, change log

## Follow-up

- Implementation reconciliation is required for everything listed above.
