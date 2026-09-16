# Change Request: Subquote Comparison and Acceptance Model

**Change Request ID**: CR-FR005-20260915-01
**Primary FR**: FR-005
**Triggering FR / Event**: Approved quote-options restructure from SRC-MTG-002 and Product Owner clarification
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-09-15
**Decision Date**: 2026-09-15
**PRD Version Change**: v1.5 to v2.0
**Related Commit(s)**: Pending

---

## Decision Summary

The patient accepts one subquote, not a parent quote. A patient may receive parent quotes from multiple providers, and the same provider may submit multiple parent quotes. Each parent quote may contain multiple subquotes. The subquote is the atomic comparison and acceptance unit because it represents the complete selected package, date range, appointment details, and price while inheriting provider and shared clinical context from its parent quote. For FR-004 interoperability, one subquote resolves one Quote Option plus one applicable Option/date-price record into that single patient-visible choice.

## Baseline State

**Source version**: FR-005 v1.5, `Main Flow: Patient Accepts a Quote`

FR-005 treated each provider quote as a flat comparison and acceptance item. Quote cards directly owned inclusions, appointment, and per-date pricing; `AcceptanceEvent` stored only `acceptedQuoteId`; and Booking received a selected quote-level appointment and price.

## Approved State

**Target version**: FR-005 v2.0, `Main Flow: Patient Accepts a Subquote`

FR-005 now groups subquotes under their parent quotes and makes each complete subquote the only patient-selectable acceptance item. The updated PRD owns the detailed comparison, acceptance, state-transition, snapshot, and downstream handoff contract.

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Acceptance target | Parent quote | Exactly one subquote per inquiry | The subquote is the complete commercial choice |
| Quote hierarchy | One flat quote per provider response | Multiple providers, multiple parent quotes per provider, multiple subquotes per parent quote | Preserve the approved quote hierarchy |
| Choice contents | Quote-level inclusions, appointment, and price | One subquote resolves one Quote Option plus one Option/date-price record and inherits upper-level context | Ensure the accepted item is complete and unambiguous |
| Comparison | Up to three parent quotes | Up to three subquotes across any parent/provider grouping | Compare what the patient can actually accept |
| Acceptance record | `acceptedQuoteId` | Accepted subquote and parent identifiers/versions plus immutable complete snapshot | Preserve the exact commercial and inherited terms |
| Non-selected outcomes | All other quotes auto-cancelled | Sibling subquotes become Not Selected; competing parent quotes auto-cancel | Distinguish alternatives inside one response from competing responses |
| Booking handoff | Selected quote appointment and price | Complete accepted subquote plus inherited parent context | Prevent reselection or ambiguity downstream |
| Analytics | Quote acceptance only | Parent-response and subquote-selection metrics remain distinct | Avoid inflated response/conversion counts |

## Scope and Impact

### In Scope

- FR-005 patient list, comparison, detail, confirmation, acceptance, and exception behavior.
- Subquote and parent-quote eligibility, state outcomes, immutable acceptance snapshot, notifications, audit, and Booking handoff.
- Meeting-source and documentation traceability for this approved decision.

### Out of Scope

- Changes to FR-004, FR-006, system documents, schemas, APIs, implementation, or tests.
- Payment collection, appointment reselection, cancellation economics, and implementation migration design.
- Consolidated verification of all six affected FRs, which the Product Owner deferred until their edits are complete.

### Affected Contracts

- **PRD owner**: `project-requirements/functional-requirements/fr005-quote-comparison-acceptance/prd.md` — `Main Flow: Patient Accepts a Subquote`, Screen 1 through Screen 3, Business Rules, requirements, and Key Entities.
- **Related FRs**: FR-004 supplies parent quote/subquote data and lifecycle; FR-006 must later consume the accepted subquote handoff without asking the patient to reselect its commercial details.
- **System documents**: Reconciliation deferred until the controlled cross-FR verification phase.

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed in this documentation phase.
- **Required assessment**: Patient UI grouping/comparison, acceptance API and concurrency guard, quote/subquote states, immutable snapshots, Booking payload, notification privacy, analytics, migrations, and regression coverage.
- **Compatibility / rollout risk**: High. A flat `acceptedQuoteId` contract can lose or ambiguously reconstruct the selected package/date/appointment/price combination.
- **Data migration**: To be assessed.

## Acceptance and Validation

- The patient can compare eligible subquotes across multiple providers, multiple parent quotes from one provider, and sibling subquotes within one parent quote.
- Acceptance targets exactly one current subquote and snapshots its complete commercial terms and inherited parent context.
- Sibling subquotes and competing parent quotes receive deterministic, distinct outcomes.
- FR-006 receives the accepted subquote without requiring package, date, appointment, or price reselection.
- Consolidated cross-FR verification is completed before FR-005 returns to Verified & Approved.

## Approval and Traceability

- **Requested by**: Product Owner
- **Approved by**: Product Owner
- **Decision evidence**: SRC-MTG-002 items D03–D06 and O01; Product Owner clarification dated 2026-09-15
- **PRD change log**: FR-005 v2.0 row dated 2026-09-15
- **Update log**: `../../update-logs/2026-09-15/FR005_SUBQUOTE_ACCEPTANCE_MODEL_2026-09-15.md`
- **Supersedes**: None
- **Superseded by**: None
