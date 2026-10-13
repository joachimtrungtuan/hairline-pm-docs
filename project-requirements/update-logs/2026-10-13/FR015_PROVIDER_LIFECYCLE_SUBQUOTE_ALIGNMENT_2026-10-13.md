# FR-015 Provider Lifecycle and Accepted Subquote Alignment

**Date**: 2026-10-13
**Type**: Major requirement update
**Documentation decision**: Approved by Product Owner; FR-015 v1.7 → v1.8
**Consolidated verification**: Pending
**Implementation reconciliation**: Required; not assessed in this operation

## Summary

Updated FR-015 for the approved Parent Quote/Subquote model. The Product Owner separately directed automatic cancellation of all related non-terminal cases on provider suspension, patient contact with admins, and distinct special-support identification for affected cases/inquiries. The other reviewed FR-015 adjustments were approved.

## Changed Files

- [FR-015 PRD](../../functional-requirements/fr015-provider-management/prd.md): v1.8, A5; Screen 3 profile count/commission/activity log; Screen 4 impact/cancellation/support; eligibility/history rules; dependencies; requirements; scenarios; entities; approvals/change log.
- [CR-FR015-20261013-01](../../functional-requirements/fr015-provider-management/change-request-2026-10-13-provider-lifecycle-subquote-contracts.md): before/after, scope, affected contracts, Product Owner provenance, and required reconciliation.
- [Update-log index](../README.md): date section, topic references, and Last Updated.

## Requirement Changes

- Suspension cancels Accepted unpaid, Confirmed, In Progress, and Aftercare cases, revokes outstanding quote availability, releases reservations, and blocks further payment; terminal history is unchanged.
- ProviderSuspended/ProviderDeactivated and independent `supportRequired` distinguish provider-caused cancellations and support needs without adding a journey stage.
- Cancel accepted provider inquiry context while preserving unrelated offers in shared unaccepted inquiries. Retain accepted snapshots/versions, clinical/completion records, and payment history.
- Mandatory patient Contact Admin/Support messages and admin alerts are independent of provider-email preferences. Reactivation does not restore cases or clear unresolved support needs.
- Deactivation retains future pending/upcoming cancellation scope; ordinary ongoing-care closure remains with FR-010/FR-011.
- Commission is snapshotted at confirmation, separate from acceptance price/FX. Later edits do not reprice existing bookings; Percentage/Flat Rate models, flat-fee recognition, and payout cycles are unchanged.
- Completed Procedures replaces the misleading Total Bookings label and counts distinct FR-010 completions, including preserved completions after Aftercare cancellation.

## Evidence and Approval

- [SRC-MTG-002](../../sources/meetings/meeting-02-launch-quote-options-fund-release-and-payments.md), D03–D06/O01, and current FR-004/FR-005/FR-006 justify the hierarchy.
- Suspension cancellation/support is the Product Owner's current FR-015 decision, not a Meeting 02 statement. Other adjustments were accepted and "Please proceed" approved this documentation update.
- [FR-029](../../functional-requirements/fr029-payment-system-config/prd.md), Screen 5 and REQ-029-043/045, owns commission snapshot timing; FR-010/FR-014 own completion/counting semantics.

## Scope and Follow-Up

Only FR-015, its Change Request, and required log registration were edited by this operation. Pre-existing/concurrent work on other FRs/system documents is outside this change and was not overwritten.

Controlled follow-up: FR-003/FR-004/FR-005/FR-006 eligibility and cancellation cause; FR-010/FR-011 suspension-specific ongoing-care handling; FR-016/FR-020 support visibility and notifications; financial/configuration/reporting compatibility via FR-007/FR-017/FR-029/FR-014. FR-034 may link support context using its existing ticket workflow; automatic ticket creation is not introduced.

No new refund/fee, payout rail, fund-release rule, clinical-completion rule, or automatic reassignment/rebooking was incorporated. Consolidated verification and implementation remain pending.

## Validation

- Scoped checks passed: 24 unique FR-015 requirement definitions, 36 local document links/anchors, 17 Markdown tables, obsolete suspension/commission wording removal, version/approval metadata, date-index references/count, and whitespace. These are document checks, not formal cross-FR or implementation verification.
- Cross-FR verification, implementation tests, and runtime cancellation/payment evidence are not part of this documentation-only operation.
