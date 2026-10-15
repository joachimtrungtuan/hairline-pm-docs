# FR-015 Verification Fixes and Downstream Cascade Alignment

**Date**: 2026-10-14
**Update Type**: Major requirement alignment (verification fixes, cross-FR alignment, new Change Requests)
**PRD Versions**: FR-015 v1.8 → v1.9 → v1.10; FR-029 → v1.8; FR-003 v2.6 → v2.7; FR-004 v2.9 → v3.0; FR-005 v2.3 → v2.4; FR-006 → v2.6; FR-010 v2.0 → v2.1; FR-011 v1.3 → v1.4; FR-016 v1.5 → v1.6; FR-020 v2.3 → v2.4; FR-030 v1.8 → v1.9; FR-017 v2.7 → v2.8 → v2.9; system PRD FR-015 status line; system data schema and technical spec v1.0.0 → v1.1.0
**Decision Status**: Documentation approved by Product Owner (2026-10-14)
**Implementation Reconciliation**: Required — not assessed
**Change Requests**: CR-FR029-20261014-01, CR-FR003-20261014-01, CR-FR004-20261014-01, CR-FR010-20261014-01, CR-FR011-20261014-01, CR-FR016-20261014-01, CR-FR020-20261014-01, CR-FR030-20261014-01; amendment note on CR-FR015-20261013-01

## Decision and Evidence

A verify-fr pass on FR-015 v1.8 found 4 critical, 7 medium, and 5 minor issues. The Product Owner chose option 1 for Issues 1–4, removed the Draft status (Issue 5), and decided Issues 6–11 and the minor issues one by one. Change Requests were created beside the affected FRs that are already Verified and Approved; FR-005 and FR-006 are already pending verification, so they carry change-log entries only. FR-015 is not yet re-verified, so it carries an amendment note on its existing CR instead of a new one.

## Changes

- **Commission model (Issue 1)**: FR-029 Screen 5 now accepts the FR-015 provider-specific Percentage (0–100%) or Flat Rate model. The global default stays percentage-only at 15–25%, and the booking-confirmation snapshot records model, value, and currency (CR-FR029-20261014-01).
- **Orphaned fields (Issue 2)**: Contact Email (required, unique), Payout Frequency (required, no default), and Commission Start Date (required, today or later) were added to the Screen 2 wizard and Key Entities.
- **Admin edit reason and reactivation (Issue 3)**: Admin profile saves require a 10–500 character reason (REQ-015-025). The new Screen 5 Provider Reactivation Modal and Alternative Flow A6 require a reason and re-authentication and restore nothing.
- **Downstream cascade (Issues 4 and 8)**: Deactivation now applies the same cascade as suspension: all non-terminal Accepted, Confirmed, In Progress, and Aftercare cases are cancelled with `ProviderDeactivated` and the `supportRequired` marker. FR-003, FR-004, FR-005, FR-006, FR-010, FR-011, FR-016, and FR-020 were aligned.
- **Draft status (Issue 5)**: Removed everywhere in FR-015 and in the system PRD. Statuses are Active, Suspended, and Deactivated.
- **Required fields (Issue 6)**: Rule 2 now equals the wizard's Required fields; the Medical License file is required at creation only.
- **Documents (Issue 7)**: FR-032 formats (PDF, JPG, PNG, DOCX, XLSX), a 6-type enum, A4 limited to admin-uploaded documents, and `uploader_type`/`uploader_id`.
- **Dependencies (Issue 9)**: FR-001/A-01 replaced by FR-031; FR-XXX placeholders resolved (FR-009, FR-022, shared S-05/S-06); FR-032, FR-013, and FR-026 added.
- **Reviews (Issue 10)**: Tab 5 links to FR-013 Screens 6–8 for admin insert, edit, and removal.
- **FR-032 rules (Issue 11)**: Clinic Name 3–200 characters, unique Contact Email, Clinic Name provider-editable.
- **Minor issues**: retention minimum 7 years then archive, never hard-delete; optimistic locking without last-write-wins; Login as Provider controls (REQ-015-026); automatic unfeaturing on suspension or deactivation (REQ-015-027); concurrency aligned to 100 admins; section-name source references.

## Files Updated

- [FR-015 PRD](../../functional-requirements/fr015-provider-management/prd.md) — v1.9, change log, approvals
- [CR-FR015-20261013-01](../../functional-requirements/fr015-provider-management/change-request-2026-10-13-provider-lifecycle-subquote-contracts.md) — amendment note
- [FR-029 PRD](../../functional-requirements/fr029-payment-system-config/prd.md) and [CR-FR029-20261014-01](../../functional-requirements/fr029-payment-system-config/change-request-2026-10-14-provider-flat-rate-commission.md)
- [FR-003 PRD](../../functional-requirements/fr003-inquiry-submission/prd.md) and [CR-FR003-20261014-01](../../functional-requirements/fr003-inquiry-submission/change-request-2026-10-14-provider-status-cancellation-cascade.md)
- [FR-004 PRD](../../functional-requirements/fr004-quote-submission/prd.md) and [CR-FR004-20261014-01](../../functional-requirements/fr004-quote-submission/change-request-2026-10-14-provider-status-cancellation-cascade.md)
- [FR-005 PRD](../../functional-requirements/fr005-quote-comparison-acceptance/prd.md) — change log only
- [FR-006 PRD](../../functional-requirements/fr006-booking-scheduling/prd.md) — change log only
- [FR-010 PRD](../../functional-requirements/fr010-treatment-execution/prd.md) and [CR-FR010-20261014-01](../../functional-requirements/fr010-treatment-execution/change-request-2026-10-14-provider-status-cancellation-cascade.md)
- [FR-011 PRD](../../functional-requirements/fr011-aftercare-recovery-management/prd.md) and [CR-FR011-20261014-01](../../functional-requirements/fr011-aftercare-recovery-management/change-request-2026-10-14-provider-status-cancellation-cascade.md)
- [FR-016 PRD](../../functional-requirements/fr016-admin-patient-mgmt/prd.md) and [CR-FR016-20261014-01](../../functional-requirements/fr016-admin-patient-mgmt/change-request-2026-10-14-provider-status-cancellation-cascade.md)
- [FR-020 PRD](../../functional-requirements/fr020-notifications-alerts/prd.md) and [CR-FR020-20261014-01](../../functional-requirements/fr020-notifications-alerts/change-request-2026-10-14-provider-status-cancellation-cascade.md)
- [System PRD](../../system-prd.md) — FR-015 provider status requirement
- [FR-030 PRD](../../functional-requirements/fr030-notification-rules-config/prd.md) and [CR-FR030-20261014-01](../../functional-requirements/fr030-notification-rules-config/change-request-2026-10-14-provider-status-cancellation-events.md) — three FR-020 events added to the catalog; both cancellation events non-disableable
- [FR-017 PRD](../../functional-requirements/fr017-admin-billing-finance/prd.md) — v2.8, change log only (already pending verification): commission model/value from the confirmation snapshot, Flat Rate once per completed procedure, payout frequency Weekly / 2x a Month / Monthly, new Rule 13 for provider-status cancellations (no automatic refund; captured payments go to admin financial resolution)
- [System data schema](../../system-data-schema.md) — v1.1.0: provider status without draft, commission/payout/featured columns, new Provider Documents section, cascade fields on inquiries and after_cares, quote `cancelled_provider_status` and commission snapshot fields
- [System technical spec](../../system-technical-spec.md) — v1.1.0: cascade, eligibility revalidation, commission model, and a Provider Lifecycle & Admin Controls subsection

## Follow-up Decisions (Product Owner, 2026-10-14)

- Kept the proposed names: FR-004 quote status `cancelled_provider_status`, the three FR-020 event keys, and the FR-029 Flat Rate currency selector defaulting to the system default currency (USD).
- Standalone aftercare (FR-011 Workflow 2) is inside the cascade scope; FR-011 D4, CR-FR011-20261014-01, and FR-015 REQ-015-017 updated.
- Aligned FR-030, FR-017, the system data schema, and the system technical spec (listed above).

- The flat commission model is named `flat_rate` everywhere (FR-015 Entity 1, schema providers notes and quotes snapshot, FR-029 Entity 6).
- Provider commission settings live in a new `provider_commissions` table (schema §2B, from FR-029 Entity 6); the five commission columns were removed from `providers`, and `payout_frequency` stays there. FR-015 `commission_start_date` maps to `effective_date`; edits archive the old row to keep rate history.
- Added the missing `inquiries.status` column (default `requested`) with the eight documented treatment case statuses, plus an index.
- Versions: system data schema v1.2.0, system technical spec v1.1.1 (change log only), FR-015 v1.9 change-log note.

## Second Verification Pass (v1.9 → v1.10)

A second verify-fr pass on FR-015 v1.9 found 1 critical, 6 medium, and 5 minor issues. The Product Owner chose the options below (2026-10-14). These are corrections and clarifications inside FR-015, so no new Change Request was created.

- **Flat Rate currency (Issue 1, critical)**: A flat amount had no currency. Added a required Flat Rate Currency field to the wizard Step 5, Tab 1, Tab 7, A2, Key Entities (`flat_rate_currency`), REQ-015-009, validation, and the quote commission snapshot. The system data schema already had `flat_rate_currency`.
- **Admin password on Screen 4 (Issue 2)**: Added an Admin Password row so the admin can set the provider owner's first password.
- **Commission Start Date (Issue 3)**: Commission Start Date is the FR-029 `effective_date`. Each later edit sets its own Effective Date, and payout cycles follow Payout Frequency rather than this date.
- **Featured providers (Issue 4)**: The patient-facing featured display is tagged P2 in Module Scope, A3, SC-001, SC-021, the FR-022 dependency, Integration 4, and User Story 1 scenario 3.
- **Documents Status column (Issue 5)**: Removed from the provider list.
- **Scheduled suspension and deactivation (Issue 6)**: Added Scheduled Status Change and Cancel Scheduled Change rules, markers on Screen 1 and the Screen 3 header, and new REQ-015-028.
- **Affiliates (Issue 7)**: A Tab 7 note says both provider and affiliate commission settings apply. FR-018 already supports percentage or fixed amount with monthly payouts on the 7th, which matches the client transcript, so FR-018 was not changed.
- **Minor fixes**: SC-003 verification wording, example reason, Billing Rule 1, bcrypt wording, PHI wording, Clinic Address versus City/Country, "Reactivate" naming, and the effect of suspension on FR-009 team logins.
- **FR-017 v2.9**: The commission start date wording now matches (it is the FR-029 Effective Date, not a payout-cycle anchor).
- **Already aligned**: `system-data-schema.md` (`flat_rate_currency`, `effective_date`) and `system-technical-spec.md` (`commission_start_date` today or later) needed no change.
- **Files updated**: `functional-requirements/fr015-provider-management/prd.md` (v1.10, change log and approval rows), `functional-requirements/fr017-admin-billing-finance/prd.md` (v2.9 change log).
- **Implementation reconciliation**: Required — not assessed.
- **System PRD sync (2026-10-15)**: The `system-prd.md` FR-015 section now matches v1.10. It covers the Flat Rate currency, Commission Start Date as the FR-029 Effective Date, Payout Frequency in the admin workflow, the featured flag in MVP with the patient-facing display at P2, and scheduled suspension or deactivation that can be cancelled. Last Updated is set to 2026-10-15.
