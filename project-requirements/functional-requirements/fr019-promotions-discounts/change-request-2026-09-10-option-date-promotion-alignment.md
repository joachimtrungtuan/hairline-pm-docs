# Change Request: Option-Date Promotion Alignment

**Change Request ID**: CR-FR019-20260910-01
**Primary FR**: FR-019
**Triggering FR / Event**: Approved FR-004 parent-quote/Quote Option restructure
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-09-10
**Decision Date**: 2026-09-10
**PRD Version Change**: v2.0 to v2.1
**Related Commit(s)**: Pending

---

## Decision Summary

FR-019 attaches a selected promotion to the applicable FR-004 option/date-price row rather than to the parent Quote. Ad-hoc quote-bound programs retain parent-quote containment and identify their single option/date-price target.

## Baseline State

**Source version**: FR-019 v2.0, Alternative Flow A1b, Screen 9, Dependencies, and Key Entities

The contract set `quote.promotionId` and recorded only `bound_quote_id`, which could not identify the priced option/date combination receiving the promotion.

## Approved State

**Target version**: FR-019 v2.1, Alternative Flow A1b, Screen 9, Dependencies, and Key Entities

The updated [FR-019 PRD](./prd.md) uses `QuoteOptionDatePrice.promotionId`, retains `bound_quote_id` for containment, and adds `bound_quote_option_date_price_id` for the application target.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Promotion attachment | Parent Quote | Option/date-price row | Each row has an independent offered price |
| Ad-hoc binding | Parent quote only | Parent quote plus one option/date-price row | Prevent ambiguous or cross-option application |
| Redemption provenance | Quote ID | Quote ID plus option/date-price ID | Preserve the accepted price source |

## Scope and Impact

### In Scope

- FR-019 quote-stage attachment, ad-hoc binding, dependency, and entity contracts.

### Out of Scope

- Promotion calculation policy, stacking, funding, payment settlement, and implementation changes.

### Affected Contracts

- **PRD owner**: [`prd.md`](./prd.md) — Alternative Flow A1b, Screen 9, Dependencies, Key Entities
- **Related FRs**: FR-004 supplies the parent Quote and option/date-price target; FR-005 preserves the accepted target later
- **System documents**: `system-data-schema.md` promotion relationship wording

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed.
- **Required assessment**: Promotion create/select APIs, option/date-price persistence, redemption records, authorization, and migration of direct quote promotion references.
- **Compatibility / rollout risk**: Legacy clients may still send a quote-level promotion ID; an additive adapter is required during consumer cutover.
- **Data migration**: To be assessed.

## Acceptance and Validation

- Every applied quote-stage promotion identifies one option/date-price row.
- Ad-hoc programs cannot apply outside their bound parent quote and row.
- Contract and integration tests prove selection, acceptance, and redemption provenance.

## Approval and Traceability

- **Requested by**: Product Owner
- **Approved by**: Product Owner, 2026-09-10
- **Decision evidence**: FR-004 v2.6 verification resolution
- **PRD change log**: FR-019 v2.1
- **Update log**: [`FR004_DEPENDENCY_AND_VERIFICATION_FIXES_2026-09-10.md`](../../update-logs/2026-09-10/FR004_DEPENDENCY_AND_VERIFICATION_FIXES_2026-09-10.md)
- **Supersedes**: None
- **Superseded by**: None
