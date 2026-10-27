# Change Request: Admin-Support Alert Recipients and Provider Status Email Timing

**Change Request ID**: CR-FR020-20261027-01
**Primary FR**: FR-020
**Triggering FR / Event**: FR-015 dev-team follow-up questions F6, F7 and F20, Product Owner decision 2026-10-27; reverses the FR-020 v2.11 recipient rule for `provider.status_cancellation_admin_support`
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-26
**Decision Date**: 2026-10-27
**PRD Version Change**: v2.11 to v2.12 (FR-016 v1.9 to v1.10; FR-015 v1.21 to v1.22; FR-030 v1.15 to v1.16)
**Related Commit(s)**: Pending

---

## Decision Summary

The Product Owner decided that the admin-support alert for provider-caused cancellations goes to the admins who can act on it. FR-020 v2.11 sent `provider.status_cancellation_admin_support` to admins with View Providers. The FR-016 list and its Resolve Support action belong to patient management, so an admin with only View Providers could receive an alert that they could not open or resolve.

The same decision fixes when and to whom provider status emails are sent:

- With "Notify Provider" checked, `provider.suspended` / `provider.deactivated` is sent when a scheduled change is created and again when it takes effect.
- Provider status emails go to the provider Owner only.

## Baseline State

**Source version**: FR-020 v2.11. The rules appear in Scope Boundaries (event catalog rows for the provider events), Business Rules (Provider Lifecycle Notifications), and REQ-020-014.

- `provider.status_cancellation_admin_support` went to admins with the FR-031 View Providers permission.
- `provider.suspended` / `provider.deactivated` were sent when "Notify Provider" was checked, with the effective date "if scheduled". The PRD did not say whether a scheduled change sends one email or two.
- The recipient of `provider.suspended`, `provider.deactivated`, `provider.reactivated` and `provider.scheduled_change_cancelled` was "Provider", without saying Owner or team.
- FR-016 did not name a permission for the Admin Support Required list or for Resolve Support, and still described a single Super Admin role.

## Approved State

**Target version**: FR-020 v2.12, same headings; FR-016 v1.10; FR-015 v1.22.

- `provider.status_cancellation_admin_support` goes to admins with the FR-031 Respond to Support permission (default roles Super Admin, Aftercare Specialist and Support Staff). Opening the FR-016 list also requires View Patients.
- In FR-016, the Admin Support Required list requires View Patients, and Resolve Support requires Respond to Support.
- With "Notify Provider" checked, `provider.suspended` / `provider.deactivated` is sent when a scheduled change is created (with its effective date) and again when it takes effect. With it unchecked, no provider email is sent at either point. Patient messages and admin-support alerts stay mandatory.
- `provider.suspended`, `provider.deactivated`, `provider.reactivated` and `provider.scheduled_change_cancelled` go to the provider Owner only. Team members learn of the status from the FR-032 Rule 6 banner or the deactivated-login message.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| `provider.status_cancellation_admin_support` recipients (FR-020 catalog, Business Rules, REQ-020-014) | Admins with View Providers (v2.11) | Admins with Respond to Support | The alert goes to admins who can open the FR-016 list and resolve the marker |
| Admin Support Required access (FR-016 Flow A7, Screen 2; FR-015 Screen 4, FR-016 dependency) | No permission named; single Super Admin role | List needs View Patients; Resolve Support needs Respond to Support | Follows the FR-031 role model |
| Scheduled suspension or deactivation email (FR-020 catalog, Business Rules, REQ-020-014; FR-015 Screen 4) | One email with the effective date "if scheduled"; timing not stated | Sent when the scheduled change is created and again when it takes effect, only with Notify Provider | The provider learns of the change in advance and when it applies |
| Provider status email recipient (FR-020 catalog, Business Rules, REQ-020-014; FR-015 Screen 4, Screen 5, A6) | "Provider" | Provider Owner only | Matches `provider.activation`; team members see the banner |

## Scope and Impact

### In Scope

- Recipients of the admin-support alert and of the four provider status emails.
- Timing of `provider.suspended` / `provider.deactivated` for scheduled changes.
- Permissions for the FR-016 Admin Support Required list and Resolve Support.

### Out of Scope

- Content, channels and mandatory status of these events, which are unchanged.
- `provider.closure_requested`, which still goes to admins with View Providers.
- FR-030 catalog wording. FR-030 should be checked for the same recipients and timing; this change does not edit it.

### Affected Contracts

- **PRD owner**: `project-requirements/functional-requirements/fr020-notifications-alerts/prd.md`: Scope Boundaries catalog rows, Business Rules (Provider Lifecycle Notifications), REQ-020-014.
- **Related FRs**:
  - FR-016 v1.10: Module Scope role model, Flow A7 Access, Screen 2 Resolve Support.
  - FR-015 v1.22: Screen 4 (Admin Support Required, Notification Email, Email timing, Email recipient, Cancel Scheduled Change), Screen 5 Notify Provider, A6, FR-016 dependency.
  - FR-031: owner of the Respond to Support and View Patients permissions and the default roles.
  - FR-030 v1.16: catalog rows for `provider.status_cancellation_admin_support`, `provider.suspended` / `provider.deactivated`, `provider.reactivated`, and `provider.scheduled_change_cancelled`, the Non-Disableable rules, and the FR-015 / FR-016 integration point mirror the new recipients and email timing.
- **System documents**: none.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed.
- **Required assessment**:
  - Recipient resolution for `provider.status_cancellation_admin_support`.
  - Permission checks on the FR-016 list and Resolve Support.
  - The scheduled-change job sending the second email when the change takes effect.
  - Owner-only recipient for the provider status emails.
  - Tests.
- **Compatibility / rollout risk**: Low. The current backend is a dev/test environment with no production data.
- **Data migration**: None.

## Acceptance and Validation

- When a provider suspension leaves a case marked Admin Support Required, an Aftercare Specialist and a Support Staff admin receive the alert, and a Billing Staff admin does not.
- An admin without Respond to Support can view the FR-016 list (with View Patients) but does not see Resolve Support.
- When an admin schedules a suspension with "Notify Provider" checked, the Owner receives `provider.suspended` at scheduling and again on the effective date. With it unchecked, the Owner receives neither.
- Team members of the provider receive none of the four provider status emails.

## Approval and Traceability

- **Requested by**: Dev team, via `FR015-BA-FOLLOWUP-QUESTIONS-2026-10-26.md` F6, F7 and F20.
- **Approved by**: Product Owner, Joachim Trung Tuan, 2026-10-27.
- **Decision evidence**: Product Owner decisions of 2026-10-27 on the FR-015 follow-up questions; [FR-015 dev-team questions answer report](../../../reports/2026-10-26/fr015-dev-questions-answers-2026-10-26.md), §7.
- **PRD change log**: [FR-020 Appendix: Change Log](prd.md#appendix-change-log), v2.12 dated 2026-10-27; FR-016 v1.10 and FR-015 v1.22 change log rows.
- **Update log**: [FR015_FOLLOWUP_QUESTIONS_RESOLUTION_2026-10-27.md](../../update-logs/2026-10-27/FR015_FOLLOWUP_QUESTIONS_RESOLUTION_2026-10-27.md).
- **Supersedes**: The FR-020 v2.11 recipient rule for `provider.status_cancellation_admin_support` (View Providers), which had no Change Request.
- **Superseded by**: None.
