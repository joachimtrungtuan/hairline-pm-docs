# Change Request: Single-Provider Scope Edits and Scheduled Commission Configuration

**Change Request ID**: CR-FR029-20261015-01
**Primary FR**: FR-029
**Triggering FR / Event**: FR-015 fourth verification pass (2026-10-15) found that FR-029 provider-specific scopes can cover several providers while FR-015 Tab 7 edits one provider at a time, with no rule for which one changes; and that the future-dated (scheduled) commission configuration shown in FR-032 Screen 4 had no defined limit or replacement rule
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-15
**Decision Date**: 2026-10-15
**PRD Version Change**: v1.8 to v1.9
**Related Commit(s)**: Pending — no commit requested for this change

---

## Decision Summary

FR-029 Screen 5 and FR-015 Tab 7 edit the same provider-specific commission data, but FR-029 scopes may group several providers and FR-015 edits a single provider. FR-029 also allowed a future Effective Date without saying how many pending configurations a provider may have.

The Product Owner chose: (1) a provider belongs to at most one active provider-specific scope; (2) an FR-015 Tab 7 edit to a provider in a shared scope splits that provider into its own single-provider scope, leaving the shared scope and its other providers unchanged; (3) each provider has at most one pending future-dated configuration, and a newer one replaces it.

## Baseline State

**Source version**: FR-029 v1.8, Screen 5 data fields and business rules, REQ-029-043 to REQ-029-047

- A provider-specific scope could cover one or several providers; nothing prevented a provider from appearing in two active scopes.
- FR-015 Tab 7 and Screen 5 were declared synchronized, but the effect of a single-provider edit on a shared scope was undefined.
- Effective Date accepted today or a future date, with no rule on multiple pending configurations.

## Approved State

**Target version**: [FR-029 v1.9](prd.md), Screen 5 (Selected Providers validation, business rules), REQ-029-048

- Selected Providers rejects a provider already in another active provider-specific scope.
- An FR-015 Tab 7 edit to a provider in a shared scope removes it from that scope and creates a single-provider scope with the new values; the split is audit-logged.
- At most one pending future-dated configuration per provider; saving another replaces it (logged); it becomes active automatically on its Effective Date. FR-015 Tab 7 and Screen 5 show the same pending configuration; FR-032 Screen 4 shows it read-only.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Scope membership | A provider could be in several active scopes | At most one active provider-specific scope per provider | Effective configuration at booking confirmation must be unambiguous |
| FR-015 single-provider edit | Undefined for shared scopes | Splits the provider into its own scope; others unchanged | Product Owner decision; avoids side effects on other providers |
| Pending configurations | Unlimited future-dated configurations implied | At most one per provider; a newer one replaces it | Gives FR-032 Screen 4 "Scheduled Configuration" a single defined source |
| Requirements | REQ-029-043 to 047 | Added REQ-029-048 | Make the rules testable |

## Scope and Impact

### In Scope

- FR-029 Screen 5 Selected Providers validation and business rules, REQ-029-048, and the PRD change log row.
- This FR-local Change Request.

### Out of Scope

- Global default commission policy, Flat Rate semantics, booking-confirmation snapshot timing, payout timing, and currency conversion.
- System PRD and technical specification updates.
- Source code, API, or live configuration changes.

### Affected Contracts

- **PRD owner**: [FR-029](prd.md) — Screen 5, REQ-029-048.
- **Related FRs**: [FR-015](../fr015-provider-management/prd.md) v1.12 Tab 7 (Scheduled Configuration, shared-scope split). [FR-032](../fr032-provider-dashboard-settings/prd.md) Screen 4 displays the pending configuration read-only. [FR-017](../fr017-admin-billing-finance/prd.md) consumes the booking snapshots, unchanged.
- **System documents**: [System data schema](../../system-data-schema.md) v1.3.0 §2B `provider_commissions` aligned on 2026-10-15 (`pending` status and partial unique indexes for one active and one pending row per provider). System PRD and technical specification unchanged.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed; no source code or runtime behavior was inspected or changed.
- **Required assessment**: Scope membership storage and uniqueness check, FR-015 Tab 7 save path (split behavior), pending-configuration storage and daily activation, Screen 5 and Tab 7 display of the pending configuration, audit logging.
- **Compatibility / rollout risk**: Existing data may already place a provider in more than one active scope or hold several future-dated configurations; these must be resolved before the new validation is enforced.
- **Data migration**: To be assessed. Do not recalculate existing booking snapshots.

## Acceptance and Validation

- Selecting a provider who is already in another active scope is rejected with a clear message.
- Editing commission in FR-015 Tab 7 for a provider in a three-provider scope leaves the other two providers on the original values and gives the edited provider its own scope.
- Saving a second future-dated configuration for a provider replaces the first; only one is shown in Screen 5, FR-015 Tab 7, and FR-032 Screen 4.
- On its Effective Date, the pending configuration becomes active for newly confirmed bookings; existing snapshots are unchanged.

## Approval and Traceability

- **Requested by**: Product Owner, Joachim Trung Tuan, during FR-015 verification review.
- **Approved by**: Product Owner, Joachim Trung Tuan, 2026-10-15; FR-029 documentation delta only.
- **Decision evidence**: FR-015 verification AskUserQuestion answers "One pending, replaceable" (Issue 1) and "Split into own setting" (Issue 3), confirmed with "Yes".
- **PRD change log**: [FR-029 Appendix: Change Log](prd.md#appendix-change-log), v1.9 dated 2026-10-15.
- **Update log**: [FR015_FOURTH_VERIFICATION_FIXES_2026-10-15.md](../../update-logs/2026-10-15/FR015_FOURTH_VERIFICATION_FIXES_2026-10-15.md).
- **Supersedes**: None.
- **Superseded by**: None.
