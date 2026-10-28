# FR-015 Backend Confirmations Resolution — 2026-10-28

**Type**: Cross-document alignment (major)
**Trigger**: Backend confirmation questions on the 2026-10-27 FR-015 follow-up decisions (aftercare linkage, seat usage and invitation model, inactive provider messages, inquiry provider selection, last-save-wins scope, Owner login email notice, quote status on inquiry cancel, legacy migration gaps, API versions)
**Decisions**: Product Owner, 2026-10-28

## Documents Changed

| Document | Version | Change |
|---|---|---|
| [FR-003 PRD](../../functional-requirements/fr003-inquiry-submission/prd.md) | 2.12 → 2.13 | Screen 7a shows only eligible providers; on submit, an explicitly selected provider that has become ineligible returns a validation error naming the provider and the patient goes back to provider selection; nothing is skipped silently (REQ-003-019). |
| [FR-004 PRD](../../functional-requirements/fr004-quote-submission/prd.md) | 3.6 → 3.7 | Review follow-up: inquiry cancellation cancels only draft, sent, and expired quotes; other quotes keep status and cause; `quote.cancelled_inquiry` goes only to providers whose quotes were cancelled (Workflow 3, Alternative Flows, REQ-004-013). |
| [FR-005 PRD](../../functional-requirements/fr005-quote-comparison-acceptance/prd.md) | 2.8 → 2.9 | Alternative Flow A6 and the confirmation-modal edge case: inline patient copy before acceptance (Accept blocked) and after acceptance (payment blocked); on-screen errors localized through FR-021, not FR-020 notifications. |
| [FR-009 PRD](../../functional-requirements/fr009-provider-team-roles/prd.md) | 1.6 → 1.7 (proposed) | Invitation and team member model ("Invited" is only a badge for a Pending invitation; a member record is created on acceptance; member statuses Active, Suspended, Removed); seat usage counts Active and Suspended non-Owner members plus valid Pending invitations; a Suspended provider cannot send invitations (new Rules 9 and 10). |
| [FR-011 PRD](../../functional-requirements/fr011-aftercare-recovery-management/prd.md) | 1.6 → 1.7 | Entry Points: exactly two routes, treatment-linked and standalone; admin assignment is a step inside them. Workflow 2b creates treatment-linked aftercare linked to the accepted quote of the completed treatment. |
| [FR-015 PRD](../../functional-requirements/fr015-provider-management/prd.md) | 1.22 → 1.23 | Seat usage member statuses; saves apply only changed fields; Owner login email change sends `provider.login_email_changed` and validates the new address against REQ-015-014. |
| [FR-020 PRD](../../functional-requirements/fr020-notifications-alerts/prd.md) | 2.12 → 2.13 | New mandatory email event `provider.login_email_changed` to the old and the new Owner login address. |
| [FR-030 PRD](../../functional-requirements/fr030-notification-rules-config/prd.md) | 1.16 → 1.17 | Catalog sync with FR-020 v2.13 (`provider.login_email_changed`, toggle locked). |
| [FR-032 PRD](../../functional-requirements/fr032-provider-dashboard-settings/prd.md) | 1.13 → 1.14 | Concurrent Edits Rule: a save applies only changed fields, so last save wins only when two people change the same field. |
| [System technical spec](../../system-technical-spec.md) | 1.4.0 → 1.4.1 | Review follow-up: the Provider-Status Cancellation Cascade no longer cancels standalone aftercare; it moves to admin aftercare-provider reassignment (schema §13, FR-011 v1.6). |
| [System data schema](../../system-data-schema.md) | 1.13.0 → 1.13.1 | §13 `after_cares`: treatment-linked aftercare references the accepted, treated quote; standalone has no quote; the Workflow 2b add-on is treatment-linked. §7: inquiry cancellation moves only `draft`, `sent`, and `expired` quotes to `cancelled_inquiry_cancelled`. §4 `provider_users`: member row created on acceptance. Review follow-up: see below. |

## Review Follow-up (2026-10-28)

Product Owner follow-up decisions and review fixes after the independent review of this change set. Versions already bumped today were not bumped again; each document's 2026-10-28 change-log row was extended or a second same-version row added.

| Document | Version | Change |
|---|---|---|
| [System data schema](../../system-data-schema.md) | 1.13.1 (same) | §4 `provider_users.status` stores `active`, `suspended`, and `inactive`, where `inactive` means Removed and never takes a seat; legacy invitee rows (`inactive` or `pending`, never accepted) are migrated into invitations, Pending or Expired by their original link expiry, and the placeholder row is deleted. New §4A `provider_staff_invitations` definition derived from FR-009, with the `pending_send` delivery state and a backend reconciliation note; total table count unchanged (already listed). §4 Business Rules header cites FR-009 v1.7; changelog row no longer says "no Change Request". |
| [FR-009 PRD](../../functional-requirements/fr009-provider-team-roles/prd.md) | 1.7 (proposed, same) | Rule 9 stored statuses and legacy invitee migration; "Pending Send" is a delivery state of a Pending invitation that takes a seat (B4, External Dependencies, REQ-009-010, Key Entity 3); Rule 10 Suspended Provider Team Management: the Team page is view-only with the suspended message (Main Flow step 6, Screens 1 and 2, REQ-009-001), stated in FR-009 because FR-032 Rule 6 does not list team management. |
| [CR-FR009-20261028-01](../../functional-requirements/fr009-provider-team-roles/change-request-2026-10-28-invitation-member-model.md) | n/a | Requested Date 2026-10-28; stored statuses, legacy invitee migration, "Pending Send" delivery state, and Suspended Team page view-only added to the decision, Approved State, delta, reconciliation, and acceptance. |
| [FR-003 PRD](../../functional-requirements/fr003-inquiry-submission/prd.md) | 2.13 (same) | Inquiry cancellation cancels only draft, sent, and expired quotes (A4, Workflow 5, E3, REQ-003-013); flow diagram submit branch for a no-longer-eligible provider; Screen 8 provider-unavailable banner text with Contact Admin/Support (B4 step 4, Screen 8 Notes, REQ-003-021); admin reassignment picker shows only eligible providers and blocks the save for one that became ineligible (Workflow 4, Screen 12). |
| [FR-004 PRD](../../functional-requirements/fr004-quote-submission/prd.md) | 3.6 → 3.7 | Inquiry cancellation cascade limited to draft, sent, and expired quotes (see table above). |
| [FR-005 PRD](../../functional-requirements/fr005-quote-comparison-acceptance/prd.md) | 2.9 (same) | Action label renamed to Contact Admin/Support in A6 and the confirmation-modal edge case. |
| [FR-011 PRD](../../functional-requirements/fr011-aftercare-recovery-management/prd.md) | 1.7 (same) | Header Status line updated to the 2026-10-28 revision. |
| [FR-015 PRD](../../functional-requirements/fr015-provider-management/prd.md) | 1.23 (same) | `provider.login_email_changed` added to the FR-020 event lists in Internal and External Dependencies. |
| [FR-020 PRD](../../functional-requirements/fr020-notifications-alerts/prd.md) | 2.13 (same) | Pre-acceptance `provider.status_cancellation_patient` text names the clinic, matching the FR-003 Screen 8 banner; event names unchanged. |
| [FR-030 PRD](../../functional-requirements/fr030-notification-rules-config/prd.md) | 1.17 (same) | Catalog sync with the FR-020 text above. |
| [System technical spec](../../system-technical-spec.md) | 1.4.0 → 1.4.1 | Standalone aftercare no longer cancelled by the provider-status cascade (see table above). |
| [CR-FR004-20261027-01](../../functional-requirements/fr004-quote-submission/change-request-2026-10-27-legacy-status-value-migration.md) | n/a | Addendum: legacy `accepted` with a paid deposit maps to quote `accepted`, booking `confirmed`, inquiry `confirmed`; pointer to the aftercare-wins rule. |
| [CR-FR006-20261027-01](../../functional-requirements/fr006-booking-scheduling/change-request-2026-10-27-legacy-status-value-migration.md) | n/a | Addendum: aftercare-wins covers active (aftercare), completed (completed), and cancelled (BA review) aftercare, all listed in the dry-run; non-production cleanup deletes or recreates the whole case, never only the quote; hard-coded staging row count removed. |

Final Product Owner decisions (same day):

- [FR-032 PRD](../../functional-requirements/fr032-provider-dashboard-settings/prd.md) 1.14 (same): Rule 6 lists team management (FR-009 Rule 10) as view-only while Suspended.
- [CR-FR006-20261027-01](../../functional-requirements/fr006-booking-scheduling/change-request-2026-10-27-legacy-status-value-migration.md) and [CR-FR004-20261027-01](../../functional-requirements/fr004-quote-submission/change-request-2026-10-27-legacy-status-value-migration.md): suspended (paused) aftercare migrates like active aftercare; booking and inquiry become `aftercare` and the aftercare record keeps `suspended`.
- [System data schema](../../system-data-schema.md) §4A: confirmed as written: one `pending` invitation per email across non-deactivated providers, and a `pending` invitation past `expires_at` counts as expired immediately.
- [FR-003 PRD](../../functional-requirements/fr003-inquiry-submission/prd.md) Screen 8a warning: "All open quotes you've received will be cancelled".

## Change Requests

- New: [CR-FR009-20261028-01](../../functional-requirements/fr009-provider-team-roles/change-request-2026-10-28-invitation-member-model.md): invitation and team member model, seat usage, Suspended provider invitations (affects FR-015).
- Extended: [CR-FR015-20261027-01](../../functional-requirements/fr015-provider-management/change-request-2026-10-27-save-conflict-encryption-seat-usage.md) Approved State gains dated clarifications for changed-fields-only saves and the seat usage member statuses.
- Extended with "Addendum 2026-10-28 (Product Owner)":
  - [CR-FR004-20261027-01](../../functional-requirements/fr004-quote-submission/change-request-2026-10-27-legacy-status-value-migration.md): legacy quote `accepted`, legacy `cancelled` on a never-accepted quote, non-accepted quotes with aftercare as invalid data, and the API version and endpoint list rules.
  - [CR-FR006-20261027-01](../../functional-requirements/fr006-booking-scheduling/change-request-2026-10-27-legacy-status-value-migration.md): the aftercare record wins over a disagreeing legacy quote status; legacy rows with no acceptance data are removed or recreated in non-production, with no schema relaxation.
  - [CR-FR003-20261027-01](../../functional-requirements/fr003-inquiry-submission/change-request-2026-10-27-legacy-status-value-migration.md): a legacy `offers` inquiry whose quote has progressed takes the stage of its booking.

No Change Request was created for the new FR-020 event: FR-015 v1.22 already required notices to the old and the new address, and this decision names that notice as a catalog event.

## Open Items

1. V8 endpoint list: the backend WS1 inventory §2 is accepted as a first draft only. The backend team completes the endpoint list per the rules in the CR-FR004-20261027-01 Addendum 2026-10-28; BA and Product Owner sign-off is pending before any `v2` route or presentation layer is built.
2. The backend team confirms that the REQ-015-014 global email check runs on every Owner login email change.
3. The provider-status cascade is not built yet, so V4 situation 1 and V9 can be tested only with hand-made data.
4. The backend team reconciles the dry-run counts with the WS1 inventory: the dry-run reports 23 quotes while the inventory rows total 28, and V1.2 reports 3 aftercare conflicts while the inventory shows 6.
5. The backend team compares its actual invitation table with the new schema §4A `provider_staff_invitations` definition (CR-FR009-20261028-01).
