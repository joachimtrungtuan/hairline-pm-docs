# FR-004 Parent Quote and Package Options Model

**Date:** 2026-09-09
**Type:** Major functional-requirement revision and Change Request

## Summary

Revised FR-004 from a single-package quote contract to an approved parent-quote aggregate containing one to five package-based Quote Options. The same provider may create multiple independent parent quotes for an active inquiry.

Created `CR-FR004-20260909-01` to record the baseline, approved state, requirement deltas, implementation evidence, migration boundary, acceptance conditions, and downstream handoffs.

## Approved Contract

- Treatment, graft facts, visual treatment plan, clinicians, common notes, common requirements, currency, expiry, and lifecycle remain on the parent Quote.
- Each Quote contains one to five ordered Quote Options derived from provider package-library presets.
- Every option stores a quote-owned package and inclusion snapshot. Inline customization never updates or creates reusable package-library records.
- Applicable treatment ranges, appointment slots, prices, and structured promotions are recorded per option/date combination.
- Each option owns a separate consecutive relative-day treatment plan.
- Quote versions and audits cover the complete parent-and-options aggregate.
- FR-005 must later select a stable Quote Option and option/date-price identifier; FR-006 and other downstream consumers remain unchanged in this update.

### Same-day Screen 1 clarification (FR-004 v2.1)

Replaced the flat Quote Creation/Edit field inventory with seven ordered tabs:

1. Treatment Service
2. Package Options, including Sub-screen 2A: Inline Package Editor
3. Grafts & Visual Plan
4. Dates & Pricing, combining date-range selection and price setup in one package-driven matrix
5. Option Treatment Plans
6. Clinical Details & Notes
7. Review & Submit

Each tab now defines its purpose, editable fields, completion gate, validation ownership, and relevant behavior. The approved quote aggregate and Change Request remain unchanged.

### Same-day data completeness clarification (FR-004 v2.2)

Added a canonical Quote Data Ownership Matrix before the tabs and reconciled each matrix field into its editing or read-only surface. The refinement adds:

- complete option-item fields: source reference, controlled type, name, description, component price, inclusion state, order, metadata, add, and remove;
- quote-level attachments;
- one-or-more shared clinicians;
- read-only system-generated graft description;
- system-owned quote/inquiry/provider references, status, price summaries, accepted total, commission, affiliate attribution, terms acknowledgement, exchange-rate lock, cancellation/supersession provenance, travel responsibility, timestamps, option customization state, and version/audit metadata; and
- a read-only currency snapshot loaded from system configuration rather than entered in the quote.

The tabs remain an organization layer over this data contract. REQ-004-024 through REQ-004-029 enforce field ownership, configured currency, attachment handling, clinician cardinality, generated graft description, and protected system metadata.

## Implementation Reconciliation

Current backend inspection confirmed a material mismatch:

- `QuotesController::store()` blocks another quote from the same provider for the inquiry.
- Quote validation and `Quote` model ownership support one `package_id`.
- Inline customization creates new `Package` and `PackageItem` records.
- Treatment dates, custom services, selections, and day-plan entries are owned directly by Quote.
- Acceptance and booking consume accepted quote-level treatment dates.
- Quote version snapshots do not contain an option aggregate.

No product code, API, database, UI, FR-005, or FR-006 implementation was changed. Reconciliation remains `Required` and should use an additive migration with legacy single-option compatibility.

## Files Updated

- `project-requirements/functional-requirements/fr004-quote-submission/prd.md` — v1.9 to v2.0, followed by the approved Screen 1 clarification in v2.1 and data completeness clarification in v2.2
- `project-requirements/functional-requirements/fr004-quote-submission/change-request-2026-09-09-quote-options-model.md` — created
- `project-requirements/sources/meetings/meeting-02-launch-quote-options-fund-release-and-payments.md` — added the approved Product Owner clarification and FR-004 incorporation status
- `project-requirements/sources/source-register.md` — marked only SRC-MTG-002 D03–D06 and O01 as partially incorporated
- `project-requirements/sources/README.md` — clarified that approved PRDs and Change Requests become authority after item-level incorporation
- `project-requirements/update-logs/README.md` — added date and topic routing

## Traceability

- Source: `SRC-MTG-002`, items MTG-002-D03 through D06 and O01
- Clarification and approval: Product Owner, 2026-09-09 project task
- Change Request: `CR-FR004-20260909-01`
- PRD change log: FR-004 v2.0, v2.1, and v2.2

## Scope Boundary

- FR-005, FR-006, system PRD, system data schema, system technical specification, implementation tasks, and product code were not changed.
- Remaining SRC-MTG-002 operational, payment, fund-release, payout, cancellation, and localization items remain pending.
