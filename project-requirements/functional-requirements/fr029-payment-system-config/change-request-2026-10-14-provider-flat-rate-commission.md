# Change Request: Provider-Specific Flat Rate Commission Alignment with FR-015

**Change Request ID**: CR-FR029-20261014-01
**Primary FR**: FR-029
**Triggering FR / Event**: FR-015 verification (2026-10-14) found that FR-029 Screen 5 provider-specific commission was percentage-only with a 15-25% range, conflicting with FR-015 Tab 7 Percentage (0-100%) / Flat Rate models that FR-015 states are synchronized with FR-029 Screen 5
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-14
**Decision Date**: 2026-10-14
**PRD Version Change**: v1.7 to v1.8
**Related Commit(s)**: Pending — no commit requested for this change

---

## Decision Summary

FR-029 Screen 5 and FR-015 Tab 7 are both valid admin edit surfaces for the same provider-specific commission records, but they described different contracts. FR-015 supports a Percentage model (0-100%) and a Flat Rate model (fixed amount > 0, deducted once per completed procedure); FR-029 allowed only a 15-25% percentage. A synchronized record cannot satisfy both.

The Product Owner chose to change FR-029 to match FR-015. Provider-specific scopes in Screen 5 now carry a Commission Model (Percentage / Flat Rate, default Percentage) and a model-specific value. The platform global default stays percentage-only at 15-25%; that policy is unchanged. The FR-006 booking-confirmation commission snapshot already owned by FR-029 now records model and value for both models. Documentation approval is separate from implementation reconciliation and deferred consolidated verification.

## Baseline State

**Source version**: FR-029 v1.7, Module Scope, Main Flow: Configure Commission Rates, Screen 5, Admin Editability Rules, Payment & Billing Rules (Commission Rule), REQ-029-043/043b/045, and Key Entities Entity 6

- Global Commission Rate and Provider Commission Rate were both percentages with range 15-25% (0.1% precision).
- No commission model field existed; the Flat Rate model was not representable in Screen 5.
- Commission amount was always calculated as booking total × commission percentage.
- The booking-confirmation snapshot and Entity 6 stored only a commission percentage.

## Approved State

**Target version**: [FR-029 v1.8](prd.md), Main Flow: Configure Commission Rates, Screen 5, Admin Editability Rules, Commission Rule, REQ-029-043/043b/045/047, and Entity 6

- Provider-specific scopes select a Commission Model: Percentage or Flat Rate (default Percentage), matching FR-015 Tab 7.
- Percentage model: 0-100%, 0.1% precision; commission = booking total × snapshotted percentage.
- Flat Rate model: fixed amount > 0 in a Flat Rate Currency chosen from the Screen 6 enabled currency list (defaulting to the system default currency); deducted once per completed procedure at the FR-010 completion milestone, not per package, Subquote, or installment. No new currency conversion rule is introduced.
- Global default remains percentage-only, 15-25%, 0.1% precision.
- The effective configuration is resolved at FR-006 booking confirmation and its model, value, and (Flat Rate) currency are snapshotted per booking/transaction. Later edits affect newly confirmed bookings only.
- FR-015 and FR-029 remain synchronized for provider-specific commission model and value.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Screen 5 provider scope fields | Provider Commission Rate, percentage 15-25% | Commission Model (Percentage / Flat Rate), Provider Commission Value, Flat Rate Currency (Flat Rate only) | Represent the same provider record FR-015 edits |
| Provider Percentage range | 15-25% | 0-100%, 0.1% precision | Match FR-015 validation |
| Flat Rate model | Not supported | Fixed amount > 0 per completed procedure, enabled currency, default system currency | Match FR-015 Flat Rate model without inventing FX rules |
| Global default | Percentage 15-25% | Unchanged; explicitly percentage-only | Product Owner did not change global default policy |
| Calculation rule | Booking total × percentage for all scopes | Percentage: booking total × percentage. Flat Rate: one fixed deduction per FR-010 completed procedure | Preserve FR-015 Flat Rate milestone semantics |
| Booking snapshot | Commission rate (percentage) | Commission model, value, and Flat Rate currency | Snapshot must govern both models consistently |
| Validation / requirements | REQ-029-043 range 15-25% for both scopes | REQ-029-043 split ranges by scope and model; REQ-029-047 model-specific validation | Close percentage-only assumption |
| Entity 6 | commission_percentage only | commission_model, commission_percentage, flat_rate_amount, flat_rate_currency | Persist both models |

## Scope and Impact

### In Scope

- FR-029 commission configuration workflow, Screen 5 fields/rules/preview, editability rules, Commission Rule, REQ-029-043/043b/045/047, and Entity 6.
- This FR-local Change Request and the PRD change log row.

### Out of Scope

- FR-015 edits (FR-015 already defines the target contract), system PRD, data schema, technical specification, and update-log authoring in this change.
- Changing the global default range or adding Flat Rate to the global default.
- New currency conversion or FX rules for Flat Rate amounts; payout-cycle timing, fund-release rules, deposit, installment, or refund economics.
- Source code, API, or live configuration changes.

### Affected Contracts

- **PRD owner**: [FR-029](prd.md) — Main Flow: Configure Commission Rates, Screen 5, Admin Editability Rules, Commission Rule, REQ-029-043/043b/045/047, Entity 6.
- **Related FRs**: [FR-015](../fr015-provider-management/prd.md) Tab 7 is the synchronized single-provider edit surface and already defines both models. [FR-006](../fr006-booking-scheduling/prd.md) triggers the booking-confirmation snapshot. [FR-010](../fr010-treatment-execution/prd.md) owns the completed-procedure milestone at which a Flat Rate snapshot is deducted. [FR-017](../fr017-admin-billing-finance/prd.md) consumes the snapshot for payout and reconciliation and should be checked for percentage-only assumptions during downstream alignment.
- **System documents**: Unchanged here. Assess whether the system PRD, data schema, and technical specification describe commission as percentage-only during controlled downstream alignment.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed; no source code or runtime commission behavior was inspected or changed.
- **Required assessment**: Screen 5 provider-scope form and validation, FR-015 Tab 7 shared persistence, commission configuration storage (model/amount/currency), Payment Configuration API response, booking-confirmation snapshot fields, commission calculation at FR-010 completion for Flat Rate, FR-017 payout/reconciliation consumption, and audit logging.
- **Compatibility / rollout risk**: Existing provider scopes are percentages and remain valid; existing 15-25% values fit within 0-100%. Existing booking snapshots must not be recalculated. Flat Rate must not be deducted per package, Subquote, or installment.
- **Data migration**: To be assessed. Existing provider-specific records would default to the Percentage model; do not reconstruct historical snapshots from current configuration.

## Acceptance and Validation

- Screen 5 provider scope offers Percentage and Flat Rate models, defaulting to Percentage; Percentage accepts 0-100% (0.1% precision) and Flat Rate accepts an amount > 0 with an enabled currency.
- Global default remains percentage-only with 15-25% validation.
- A confirmed booking stores commission model, value, and (Flat Rate) currency; later configuration edits do not change it.
- A Flat Rate snapshot yields one deduction per FR-010 completed procedure regardless of procedure price, package count, Subquote, or installment count.
- A provider-specific model/value change in FR-015 appears in Screen 5 and vice versa.
- No FR-029 text assumes percentage-only provider commission; requirement IDs are unique and tables contain no stray column dividers. Cross-FR verification and implementation/regression proof remain required before reconciliation becomes Verified.

## Approval and Traceability

- **Requested by**: Product Owner, Joachim Trung Tuan, during FR-015 verification review.
- **Approved by**: Product Owner, Joachim Trung Tuan, 2026-10-14; FR-029 documentation delta only.
- **Decision evidence**: FR-015 verification review answer "Issue 1: option 1 ... but also add a change request" — option 1 being to change FR-029 to match FR-015.
- **PRD change log**: [FR-029 Appendix: Change Log](prd.md#appendix-change-log), v1.8 dated 2026-10-14.
- **Update log**: [FR015_VERIFICATION_ALIGNMENT_2026-10-14.md](../../update-logs/2026-10-14/FR015_VERIFICATION_ALIGNMENT_2026-10-14.md).
- **Supersedes**: None as a Change Request; replaces v1.7 wording that provider-specific commission is a 15-25% percentage.
- **Superseded by**: None.
