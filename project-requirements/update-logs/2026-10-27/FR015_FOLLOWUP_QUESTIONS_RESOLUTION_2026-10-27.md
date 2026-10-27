# FR-015 Follow-up Questions Resolution — 2026-10-27

**Type**: Cross-document alignment (major)
**Trigger**: Dev-team follow-up questions F1–F21 on the 2026-10-26 FR-015 answer report (`FR015-BA-FOLLOWUP-QUESTIONS-2026-10-26.md`)
**Decisions**: Product Owner, 2026-10-27
**Answer report**: [reports/2026-10-26/fr015-dev-questions-answers-2026-10-26.md](../../../reports/2026-10-26/fr015-dev-questions-answers-2026-10-26.md), §7

## Documents Changed

| Document | Version | Change |
|---|---|---|
| [FR-003 PRD](../../functional-requirements/fr003-inquiry-submission/prd.md) | 2.11 → 2.12 | Workflow 2 Alternative Flow B4, Rule 6, Screen 8 notes, new REQ-003-021 and an edge case: automatic redistribution before acceptance when a provider-status cancellation leaves the patient no live offer, with patient confirmation first when the patient had selected that provider (F9). |
| [FR-004 PRD](../../functional-requirements/fr004-quote-submission/prd.md) | 3.5 → 3.6 | Workflow 3: the accepted quote keeps `accepted`; FR-005 writes the supersession record only when the admin accepts the replacement quote (F4). |
| [FR-006 PRD](../../functional-requirements/fr006-booking-scheduling/prd.md) | 2.10 → 2.11 | Main Flow "Booking Creation" and Alternative Flow B1 separate the booking from the appointment (F3). Screens 7, 8 and 10, the admin intervention rules and new REQ-006-020: admin revive, appointment change and replacement acceptance require an Active provider (F14). |
| [FR-009 PRD](../../functional-requirements/fr009-provider-team-roles/prd.md) | 1.5 → 1.6 (proposed) | Seat usage excludes the Owner and expired invitations (F13); impersonation blocked for Deactivated and read-only for Suspended providers (F12). |
| [FR-015 PRD](../../functional-requirements/fr015-provider-management/prd.md) | 1.21 → 1.22 | Cascade transaction and background job (F8), closure marker (F18), commission display and deactivation (F19), seat usage (F13), wizard leave prompt (F11), Resend Activation Email (F21.5), Login as Provider (F12), Owner email change (F16), Tab 8 CSV export (F21.4), suspended chat (F5), status email timing and Owner-only recipients (F6, F20), Respond to Support (F7), Rule 9 and REQ-015-020 admin actions (F14), encryption (F17), unified copy (F21.1, F21.2), last save wins (F15), FR-005 supersession wording (F21.3). |
| [FR-016 PRD](../../functional-requirements/fr016-admin-patient-mgmt/prd.md) | 1.9 → 1.10 | Resolve Support requires Respond to Support and the list requires View Patients (F7); the role-model line points to FR-031. |
| [FR-020 PRD](../../functional-requirements/fr020-notifications-alerts/prd.md) | 2.11 → 2.12 | Admin support alert goes to Respond to Support (F7); status emails at scheduling and on effect, Owner only (F6, F20); patient redistribution variants of `provider.status_cancellation_patient` (F9). |
| [FR-032 PRD](../../functional-requirements/fr032-provider-dashboard-settings/prd.md) | 1.12 → 1.13 | Rule 6 suspended chat (F5), Concurrent Edits Rule (F15), closure steps (F18); F10 noted as already explicit. |
| [System data schema](../../system-data-schema.md) | 1.12.0 → 1.13.0 | Legacy status value migration notes (F1, F2); §40 legacy table migration (F10) and scheduled-deactivation approval rule (F18). |

## Change Requests

- [CR-FR003-20261027-01](../../functional-requirements/fr003-inquiry-submission/change-request-2026-10-27-legacy-status-value-migration.md): inquiry stage and participation value migration.
- [CR-FR003-20261027-02](../../functional-requirements/fr003-inquiry-submission/change-request-2026-10-27-pre-acceptance-redistribution.md): automatic redistribution before acceptance.
- [CR-FR004-20261027-01](../../functional-requirements/fr004-quote-submission/change-request-2026-10-27-legacy-status-value-migration.md): quote status value migration, full old-to-new and new-to-old mapping.
- [CR-FR006-20261027-01](../../functional-requirements/fr006-booking-scheduling/change-request-2026-10-27-legacy-status-value-migration.md): booking status value migration.
- [CR-FR006-20261027-02](../../functional-requirements/fr006-booking-scheduling/change-request-2026-10-27-admin-actions-require-active-provider.md): admin booking actions require an Active provider.
- [CR-FR015-20261027-01](../../functional-requirements/fr015-provider-management/change-request-2026-10-27-save-conflict-encryption-seat-usage.md): last save wins, no application-level encryption, seat usage definition (affects FR-009, FR-032).
- [CR-FR020-20261027-01](../../functional-requirements/fr020-notifications-alerts/change-request-2026-10-27-admin-support-recipients-status-email-timing.md): admin support alert recipients, status email timing and recipients (affects FR-015, FR-016); partly supersedes the 2026-10-26 View Providers rule.

## Superseded 2026-10-26 Decisions

- Decision 15 (admin support alert to View Providers) is replaced by F7 (Respond to Support).
- Decision 16 (seat usage) is refined by F13 (Owner and expired invitations excluded).

## Later the Same Day: Open Items Settled

The seven open points in the answer report §7.4 were settled by the Product Owner. Same-day follow-ups extend the existing 2026-10-27 change-log rows instead of bumping versions again.

| Document | Version | Change |
|---|---|---|
| [System data schema](../../system-data-schema.md) | 1.13.0 (same day) | §5 `inquiries`: `redistribution_state`, `redistribution_state_at`, `redistribution_provider_status_event_id`; new rule and ENUM entry. |
| [FR-003 PRD](../../functional-requirements/fr003-inquiry-submission/prd.md) | 2.12 (same day) | Change log names the new schema columns; CR-FR003-20261027-02 affected contracts updated. |
| [FR-016 PRD](../../functional-requirements/fr016-admin-patient-mgmt/prd.md) | 1.10 (same day) | Single-Super-Admin and deferred-RBAC wording replaced with FR-031 permissions; medical data and scans require Manage Aftercare. |
| [FR-030 PRD](../../functional-requirements/fr030-notification-rules-config/prd.md) | 1.15 → 1.16 | Catalog, business rules and integration point mirror FR-020 v2.12; listed in CR-FR020-20261027-01. |

- FR-016 (same day, minor): REQ-016-020 and the High-Impact Actions list now apply enhanced confirmation to every account suspension, matching Rule 4. The old "> 30 days" wording excluded the 30-day option.

No open items remain.
