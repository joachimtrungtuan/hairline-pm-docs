# Change Request: MTG-002 Quote Model Alignment for Search and Filtering

**Change Request ID**: CR-FR022-20261016-01
**Primary FR**: FR-022
**Triggering FR / Event**: MTG-002 quote-model verification and Product Owner decision log (2026-10-16)
**Decision Status**: Approved
**Implementation Reconciliation**: Required
**Requested Date**: 2026-10-16
**Decision Date**: 2026-10-16
**PRD Version Change**: v2.13 to v2.15
**Related Commit(s)**: Pending

> Create this document only for a major requirement event: a new or materially revised FR changes another verified or implemented FR, or an approved restructure substantially changes requirements, ownership, workflow, data, security, or integration contracts. Record small corrections only in the PRD change log and normal update log.

---

## Decision Summary

MTG-002 fixed the canonical quote and booking state lists and redefined a package as a full template with an Active or Inactive status and no package types. FR-022 was **✅ Verified & Approved** at v2.13, and its admin and provider filters used stale state lists and a removed package-type filter. This request aligns the filter contracts with FR-004 v3.1, FR-006 v2.7 and FR-024 v1.3, and resets the FR-022 status to **🟡 Revised — Pending Consolidated Verification**.

## Baseline State

**Source version**: FR-022 v2.13, Screen Specifications (FR-004 / Screen 2, FR-004 / Screen 5, FR-006 / Screen 5, FR-024 / Screen 4, FR-005 / Screen 1) and REQ-022-041

- Quote Status filters listed Draft, Sent, Expired, Withdrawn, Archived, Accepted, Cancelled (Other Accepted) and Cancelled (Inquiry Cancelled), without Cancelled (Provider Status).
- The admin Booking Status filter listed All, Pending Payment, Confirmed, In Progress, Completed and Cancelled, which is not the FR-006 state list.
- The provider package list filtered by an admin-defined Package Type, and REQ-022-041 required filtering by package type.
- The FR-005 subquote price sort basis, tie-break order, ineligible-subquote placement and result unit were not defined; provider and admin quote lists did not state their row or count unit.

## Approved State

**Target version**: FR-022 v2.15 (same headings)

- Quote Status filters use the exact FR-004 quote statuses, including Cancelled (Provider Status). `confirmed` is not a quote status.
- The admin Booking Status filter uses the exact FR-006 booking states: Accepted, Payment Window Expired, Confirmed, In Progress, Aftercare, Completed, Cancelled. "Pending Payment" is removed.
- The provider package list filters by package status (Active, Inactive); REQ-022-041 is updated to match.
- FR-005 / Screen 1 price sorts use the complete offered price with promotion included; ties are ordered by parent quote send date, option order and date range start; ineligible subquotes stay listed, disabled, after eligible ones; each result is one subquote. User Story 5 tests this behaviour (REQ-022-057).
- FR-004 / Screen 2 and Screen 5 rows and result counts are parent quotes.
- Patient-facing price sorts and price filters convert each price to the patient's display currency at the current rate for ordering only; each card keeps its own quote currency, and mixed-currency order is labelled approximate (General Module Rule 9, REQ-022-058).

## Requirement Delta

| Contract Area | Before | After | Reason |
|---|---|---|---|
| Quote Status filter (FR-004 / Screen 2 and Screen 5) | Eight statuses, no Cancelled (Provider Status) | Exact FR-004 status list, including Cancelled (Provider Status); no `confirmed` | MTG-002 decisions M6 and D23; findings FR-022-2 |
| Booking Status filter (FR-006 / Screen 5) | All, Pending Payment, Confirmed, In Progress, Completed, Cancelled | Accepted, Payment Window Expired, Confirmed, In Progress, Aftercare, Completed, Cancelled | MTG-002 decision M6; finding FR-022-3 |
| Package filter (FR-024 / Screen 4, REQ-022-041) | Package Type, admin-defined types | Package status, Active or Inactive | MTG-002 decision D17 (package types removed) via FR-024 v1.3 |
| Subquote sort and filter (FR-005 / Screen 1) | Sort basis, tie-break and ineligible placement undefined | Promotion-inclusive offered price; defined tie-break; ineligible subquotes last; result unit is the subquote; User Story 5 added | R7-3 minors FR-022-1, FR-022-4, FR-022-5 |
| Quote list row and count unit (FR-004 / Screen 2 and Screen 5) | Implicit | One row and one counted result per parent quote | R7-3 minor FR-022-6 |
| Price sort across currencies (FR-005 / Screen 1 and any patient-facing price sort or filter) | Unstated | Converted to the display currency at the current rate for ordering only; cards keep their own currency; mixed-currency order labelled approximate (Rule 9, REQ-022-058) | Q8 |

## Scope and Impact

### In Scope

- Filter option lists and the related REQ text listed above, User Story 5, change log, status and footer metadata.

### Out of Scope

- Payment, fund release, refunds and later instalment states; FR-006 owns booking states and FR-007/FR-007b own payment status.
- Currency handling when subquotes under one inquiry carry different quote currency snapshots (not decided; raised as an open question).
- A package filter on the patient subquote list (not required by the baseline).

### Affected Contracts

- **PRD owner**: `prd.md` — FR-004 / Screen 2, FR-004 / Screen 5, FR-005 / Screen 1, FR-006 / Screen 5, FR-024 / Screen 4, REQ-022-041, User Story 5
- **Related FRs**: FR-004 (quote status list, owner), FR-005 (subquote states and Screen 1 sort controls), FR-006 (booking state list, owner), FR-024 (package status), FR-014 and FR-030 (must use the same quote and booking lists)
- **System documents**: `system-data-schema.md` (quote status enum without `confirmed`, booking status enum)

### Implementation Reconciliation

- **Existing implementation evidence**: Not assessed
- **Required assessment**: Admin and provider filter option sources, booking status filter query mapping, package list filter, subquote list sort query
- **Compatibility / rollout risk**: Saved filters or queries using "Pending Payment" or package type need mapping or removal
- **Data migration**: To be assessed

## Acceptance and Validation

- Quote Status options on both FR-004 screens equal the FR-004 status enum and contain Cancelled (Provider Status) and no Confirmed.
- Booking Status options equal the FR-006 state list; "Pending Payment" appears nowhere in FR-022.
- The package list filter offers only All, Active and Inactive.
- User Story 5 scenarios pass on FR-005 / Screen 1.
- A mixed-currency subquote list sorts by converted display-currency value, cards show their own currency, and the order is labelled approximate.

## Approval and Traceability

- **Requested by**: Product Owner (MTG-002 quote-model verification)
- **Approved by**: Product Owner — documentation approved 2026-10-16 via the decision log; implementation reconciliation required, not assessed
- **Decision evidence**: SRC-MTG-002; `reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md` (M6, D23, D17, R7-3; Q-series Q8)
- **PRD change log**: FR-022 v2.14 and v2.15 rows dated 2026-10-16
- **Update log**: `../../update-logs/2026-10-16/MTG002_QUOTE_MODEL_ALIGNMENT_2026-10-16.md`
- **Supersedes**: None
- **Superseded by**: None
