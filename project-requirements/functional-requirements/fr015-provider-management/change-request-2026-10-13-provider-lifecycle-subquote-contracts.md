# Change Request: Provider Lifecycle and Accepted Subquote Contracts

**Change Request ID**: CR-FR015-20261013-01
**Primary FR**: FR-015
**Triggering FR / Event**: SRC-MTG-002 quote-model refinements incorporated into FR-004/FR-005/FR-006, existing FR-029 commission snapshot policy, and Product Owner's provider-suspension decision
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-13
**Decision Date**: 2026-10-13
**PRD Version Change**: v1.7 to v1.8
**Related Commit(s)**: Pending — no commit requested for this change

---

## Decision Summary

FR-015 now consumes the approved Parent Quote → package/date Subquote → accepted Booking model for provider eligibility and lifecycle impact. It does not add quote/package editing screens to provider management.

The Product Owner rejected keeping unpaid selections or existing upcoming appointments active after suspension: suspension automatically cancels all related non-terminal treatment cases, patients must contact admins, and affected cases/inquiries must be distinguishable for special admin support. The target contract uses a provider-specific cancellation cause plus an independent `supportRequired` marker, not one combined cancellation/support journey stage.

This update also aligns commission edits with booking-confirmation snapshots, clarifies deactivation's existing future-booking cancellation policy, preserves historical data, and renames the completed-procedure profile count. Documentation approval is separate from implementation reconciliation and deferred consolidated verification.

## Baseline State

**Source version**: FR-015 v1.7, Screen 3 Tabs 1/7/8, Screen 4, General Module Rules, Payment & Billing Rules, Business Process Assumptions, User Story 3, and Key Entities

- Suspension blocked new bookings but left upcoming appointments active unless individually cancelled. Accepted-but-unpaid holds, multiple Parent Quotes, and ongoing care stages were not defined.
- Deactivation cancelled future bookings without explicit accepted-selection, reservation, or support handoffs.
- Commission changes applied to new transactions, conflicting with FR-029's confirmation-time snapshot policy.
- Total Bookings actually counted completed procedures, without distinguishing quote alternatives and completion milestones.
- No distinct provider-cancellation support marker or mandatory patient/admin handoff was specified in FR-015.

## Approved State

**Target version**: [FR-015 v1.8](prd.md), Alternative Flow A5, Screen 3 Tabs 1/7/8, Screen 4, Rules 5/9/10, and REQ-015-017–024

- Effective suspension cancels Accepted, Confirmed, In Progress, and Aftercare cases of that provider, revokes outstanding quote availability, releases active reservations, and blocks further payment. Completed/already-terminal history is unchanged. This is the documented interpretation of the Product Owner's all-related-treatment scope.
- Affected cases use Cancelled with ProviderSuspended and a separate Admin Support Required marker. Accepted inquiry context follows its cancelled case. Shared unaccepted inquiries retain unrelated providers' offers while affected provider participation is cancelled and the inquiry flagged for support.
- Deactivation retains cancellation of future pending/upcoming bookings with ProviderDeactivated and the same reservation/history/support handoffs. Its ongoing-care policy is not broadened here.
- Patients receive cancellation/offer-unavailability notices directing them to admins; admins can identify/filter unresolved affected records. Notify Provider does not disable mandatory patient/admin notifications.
- Reactivation does not restore cancelled cases/quotes, restart holds, or clear unresolved support markers. Admins resolve care continuity, rebooking, and finances through existing owners.
- Commission model/value is fixed at booking confirmation; later edits do not reprice existing bookings' installments/deductions. Patient price/FX remains fixed at acceptance; Flat Rate remains once per completed procedure.
- Completed Procedures counts distinct FR-010 completions, including preserved completions after later Aftercare cancellation.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Suspension lifecycle | Upcoming appointments remained active; unpaid/ongoing care unspecified | Cancel non-terminal Accepted, Confirmed, In Progress, and Aftercare cases at effective suspension | Product Owner requires automatic cancellation, not individual manual cancellation |
| Quote/inquiry scope | No multiple-parent or shared-inquiry impact contract | Revoke affected provider's parents/alternatives and accepted case/inquiry context, preserving unrelated unaccepted offers | Respect FR-004/FR-005 hierarchy and provider-scoped authority |
| Cancellation/support identity | No provider-related support marker | ProviderSuspended or ProviderDeactivated plus supportRequired and audited resolution | Separate cancellation cause, support progress, and patient cancellation |
| Deactivation | Future bookings cancelled without pending-payment/reservation detail | Include future Accepted/Confirmed cases; block payment, release reservations, preserve history, and route support | Close pending-selection gap without broadening existing deactivation policy |
| Notifications and recovery | Optional provider email; no special patient/admin path | Mandatory patient/admin handoff, safe retries, no automatic restoration/financial settlement | Keep affected patients visible for assistance |
| Commission applicability | Changed configuration could apply to later transactions | Confirmation-time model/value snapshot governs existing bookings; acceptance price lock remains distinct | Match FR-029 and avoid later installment repricing |
| Profile count | Total Bookings meant completed procedures | Completed Procedures counts distinct actual completions, not quote/payment alternatives | Preserve intended measure with accurate label and grain |
| Audit/data references | Status history without accepted-case handoff | Link status event, affected IDs/prior stages, cause, support marker, and slot/notification results; retain immutable history | Accountable cancellation without duplicating mutable quote data in Provider |

## Scope and Impact

### In Scope

- FR-015 lifecycle, commission applicability, profile count, audit/support references, dependencies, requirements, and acceptance scenarios.
- This FR-local Change Request and required update-log registration.
- Suspension scope includes ongoing treatment and Aftercare; clinical records and completed-care facts remain retained for admin assistance.

### Out of Scope

- Other PRD/system-document edits, source code/API changes, and live provider/case operations.
- Onboarding/profile/document/featured-provider/seat-limit redesign, quote/package editing screens, or package-library policy changes.
- New commission models/ranges, refund amounts/fees, installment economics, fund-release/payout rails, and payout-cycle changes.
- Automatic rebooking, clinical reassignment, refunds, or ticket creation; FR-034 retains its existing ticket workflow/sources.
- Remaining Meeting 02 payment/fund-release decisions, Meeting 01/03, and the separate fund-release brief.
- Claiming implementation readiness or completing postponed consolidated verification.

### Affected Contracts

- **PRD owner**: [FR-015](prd.md) — A5, Screen 3 Tabs 1/7/8, Screen 4, Rules 5/9/10, REQ-015-017–024, and Key Entities lifecycle context.
- **Quote/inquiry/booking owners**: [FR-003](../fr003-inquiry-submission/prd.md), [FR-004](../fr004-quote-submission/prd.md), [FR-005](../fr005-quote-comparison-acceptance/prd.md), and [FR-006](../fr006-booking-scheduling/prd.md) require controlled provider-eligibility, cancellation-cause, accepted-inquiry, hold-release, and immutable-provenance alignment. This is not patient cancellation or Payment Window Expired.
- **Care owners**: [FR-010](../fr010-treatment-execution/prd.md) and [FR-011](../fr011-aftercare-recovery-management/prd.md) require explicit suspension cancellation/support alignment. FR-010's current provider-requested Cancel/Close Case does not auto-transition status; that ordinary flow remains distinct from this admin-authorized event. FR-011 retains ownership of admin reassignment/recovery support.
- **Support/notification owners**: [FR-016](../fr016-admin-patient-mgmt/prd.md) and [FR-020](../fr020-notifications-alerts/prd.md) need marker/filter visibility, provider-caused messages, and mandatory admin alerts. [FR-034](../fr034-support-center-ticketing/prd.md) may link support context without a new automated ticket source/status.
- **Financial/reporting owners**: [FR-007](../fr007-payment-processing/prd.md), [FR-017](../fr017-admin-billing-finance/prd.md), and [FR-029](../fr029-payment-system-config/prd.md) retain payment/refund/deduction accounting, payout ownership, and commission snapshots. [FR-014](../fr014-provider-analytics-reporting/prd.md) retains historical acceptance/price milestones while excluding cancelled selections from active payment exposure. FR-029's percentage-only configuration prose must not be assumed to already cover the unchanged FR-015 Flat Rate model; that compatibility remains for reconciliation.
- **System documents**: System PRD, data schema, and technical specification are unchanged here. Assess cancellation/support metadata, state transitions, and historical references during controlled downstream alignment.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed; no source code or runtime cancellation/payment behavior was inspected or changed.
- **Required assessment**: Provider-status paths/scheduling; eligibility guards; quote/booking/care transitions; reservation release; payment callbacks; cancellation/support storage; admin filters/visibility; notification privacy/retries/deduplication; immutable acceptance/commission references; metric counting.
- **Compatibility / rollout risk**: Reconcile FR-003/FR-006/FR-010/FR-011 and patient/admin support before deployment, then test paid/unpaid/ongoing cases together. A captured payment racing with suspension remains recorded for admin resolution, never hidden or used to revive a cancelled booking.
- **Data migration**: To be assessed. Do not retrospectively relabel existing terminal cases or reconstruct historical snapshots from current package/profile/configuration data.

## Acceptance and Validation

- Suspension cancels Accepted unpaid, Confirmed, In Progress, and Aftercare cases; release/payment guards apply even when the original valid hold had time remaining.
- Completed/terminal history and clinical/payment/completion records remain retained; accepted IDs, equal aggregate versions, and package/date/appointment/price snapshots do not change.
- Shared unaccepted inquiries preserve unrelated offers; cancelled accepted provider cases carry their inquiry context and special support marker.
- Patients receive Contact Admin/Support instructions; admins can identify affected records and audit resolution. Notify Provider unchecked and retries do not remove these obligations or duplicate outcomes.
- Reactivation/later deactivation do not reopen cases, restart holds, clear support markers, or overwrite the original cancellation cause.
- Existing confirmed bookings retain commission model/value through later installments and once-per-completed-procedure flat-fee recognition; new confirmations use effective configuration.
- Completed Procedures counts one FR-010 completion, not quotes, alternatives, captures, or final aftercare statuses.
- Validate links/anchors, unique requirement IDs, tables, and removal of obsolete active-bookings/new-transaction commission wording. Cross-FR verification and implementation/regression proof remain required before reconciliation becomes Verified.

## Approval and Traceability

- **Requested by**: Product Owner, Joachim Trung Tuan.
- **Approved by**: Product Owner, Joachim Trung Tuan, 2026-10-13; FR-015 documentation delta only. Final instruction: "Please proceed."
- **Quote-model evidence**: [SRC-MTG-002](../../sources/meetings/meeting-02-launch-quote-options-fund-release-and-payments.md), D03–D06/O01 with Product Owner refinements, and current FR-004/FR-005/FR-006. These sources justify the hierarchy, not the new suspension policy.
- **Suspension/support evidence**: In this review, the Product Owner stated "suspension of the provider automatically cancel all related treatment"; patients must contact admins and cancelled cases/inquiries need a distinct status/marker for special support. The Product Owner approved the other proposals and then instructed "Please proceed." This is a separate Product Owner decision, not attributed to Meeting 02. The all-related-treatment scope is explicitly interpreted as non-terminal cases including In Progress/Aftercare, with completed history retained.
- **Compatibility evidence**: FR-029 Screen 5 and REQ-029-043/045 own commission snapshot timing; FR-010/FR-014 own existing completion/counting semantics. No new fee or clinical-completion economics are inferred.
- **PRD change log**: [FR-015 Appendix: Change Log](prd.md#appendix-change-log), v1.8 dated 2026-10-13.
- **Update log**: [FR015_PROVIDER_LIFECYCLE_SUBQUOTE_ALIGNMENT_2026-10-13.md](../../update-logs/2026-10-13/FR015_PROVIDER_LIFECYCLE_SUBQUOTE_ALIGNMENT_2026-10-13.md).
- **Supersedes**: None as a Change Request; replaces v1.7 wording that suspension leaves upcoming bookings active and commission edits apply to new transactions.
- **Superseded by**: Partially amended by FR-015 v1.9 (2026-10-14), see below.

## Amendment — 2026-10-14 (FR-015 v1.9)

The Product Owner's FR-015 verification decisions (2026-10-14, Issues 4 and 8) broaden the deactivation policy recorded above. Effective deactivation now applies the same cascade scope as suspension: all non-terminal Accepted, Confirmed, In Progress, and Aftercare cases are cancelled with `ProviderDeactivated` and the separate `supportRequired` marker; an earlier `ProviderSuspended` cause is not overwritten. The statement "Its ongoing-care policy is not broadened here" no longer applies. FR-015 v1.9 also adds the Screen 5 reactivation modal; reactivation still restores nothing.

The downstream follow-ups listed under Affected Contracts were run under these Change Requests:

- [CR-FR003-20261014-01](../fr003-inquiry-submission/change-request-2026-10-14-provider-status-cancellation-cascade.md), [CR-FR004-20261014-01](../fr004-quote-submission/change-request-2026-10-14-provider-status-cancellation-cascade.md), [CR-FR010-20261014-01](../fr010-treatment-execution/change-request-2026-10-14-provider-status-cancellation-cascade.md), [CR-FR011-20261014-01](../fr011-aftercare-recovery-management/change-request-2026-10-14-provider-status-cancellation-cascade.md), [CR-FR016-20261014-01](../fr016-admin-patient-mgmt/change-request-2026-10-14-provider-status-cancellation-cascade.md), [CR-FR020-20261014-01](../fr020-notifications-alerts/change-request-2026-10-14-provider-status-cancellation-cascade.md)
- [CR-FR029-20261014-01](../fr029-payment-system-config/change-request-2026-10-14-provider-flat-rate-commission.md) resolves the FR-029 percentage-only compatibility gap noted under Affected Contracts.
- FR-005 (v2.4) and FR-006 (v2.6) were aligned through their change logs only, because they are already pending consolidated verification.
- Update log: [FR015_VERIFICATION_ALIGNMENT_2026-10-14.md](../../update-logs/2026-10-14/FR015_VERIFICATION_ALIGNMENT_2026-10-14.md).
