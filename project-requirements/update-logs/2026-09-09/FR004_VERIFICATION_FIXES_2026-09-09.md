# FR-004 Verification Fixes and Upstream Reconciliation

**Date**: 2026-09-09
**Report Type**: FR verification follow-up and cross-document alignment
**Scope**: FR-004 v2.2 → v2.3, FR-010 v1.8 → v1.9, system PRD, system data schema, system technical spec
**Status**: Documentation approved; implementation reconciliation required

---

## 1. Why This Update Exists

FR-004 was re-verified after CR-FR004-20260909-01 restructured it into a parent-quote aggregate with one to five Quote Options. The verification found the FR internally sound and faithful to its sources, but exposed eight issues, most of them caused by the change request's blast radius not having been propagated outward.

The Product Owner triaged the findings on 2026-09-09. This log records what was fixed, what was deliberately left open, and where the record of each decision lives.

---

## 2. Decisions Applied

| # | Issue | Decision | Where it landed |
|---|-------|----------|-----------------|
| 1 | FR-005 and FR-006 still describe the pre-option acceptance handoff | **Deferred** — left open and unscheduled | Recorded as open in both change requests |
| 2 | FR-008 derives travel from a package-keyed quote field | **Deferred** — left open and unscheduled | Recorded as open in both change requests |
| 3 | FR-010 assumed a single assigned clinician while FR-004 sends `clinicianIds[]` | Make FR-010 clinicians plural | FR-010 v1.9 plus CR-FR010-20260909-01 |
| 4 | FR-004 promised relative plan days would be resolved to calendar dates | **Inverted** — the promise was the defect. Confirmed prior product decision: day numbers are never resolved to stored calendar dates | FR-004 v2.3 |
| 5 | System PRD, data schema, and technical spec still described the single-package quote | Reconcile all three now | All three system documents |
| 6 | `included_services` had no ownership statement | Add it to the Quote Data Ownership Matrix as a provider-edited option field | FR-004 v2.3 |
| 7 | Quote-amount analytics were undefined for an unaccepted quote | Accepted-price only | FR-004 v2.3 (REQ-004-030), system PRD, technical spec |
| 8 | CR-FR004-20260909-01 recorded v1.9 → v2.0 but three versions had shipped under one approval | Extend the existing change request to v2.2 rather than open a new one | CR-FR004-20260909-01 |

---

## 3. Document Changes

### FR-004 Quote Submission — v2.2 → v2.3

- Removed both statements promising that relative plan days are resolved to calendar dates; day numbers now stay relative for the life of the record, and FR-005 comparison and FR-010 In Progress present the plan by day number against the accepted appointment.
- Added an Ownership Matrix row for `included_services` as a provider-edited option field on Sub-screen 2A, stored only in the option snapshot.
- Added a business rule and **REQ-004-030** fixing quote-amount analytics to the accepted option/date price; an unaccepted quote has a price range, not an amount, and counts only in volume and conversion metrics. Quote Options are never counted as separate provider responses.
- Corrected the Approvals row to name FR-004 v2.2 as the approved state.
- Appended a v2.3 change-log entry.

### FR-010 Treatment Execution — v1.8 → v1.9

- `Assigned Clinician` became `Assigned Clinicians` across the treatment detail, plan, and admin surfaces; the admin control is now a multiselect with an at-least-one-remaining rule.
- The treatment plan lock now covers the assigned clinician set rather than a single clinician.
- Key entities and relationships now carry one or more clinician IDs sourced from quote `clinicianIds[]`, provider-locked after Check In and admin-overridable with reason and audit history.
- Clinician filters read "any assigned clinician".
- This supersedes the FR-010 v1.4 singular clinician model.

### System PRD

- The FR-004 section now describes one to five Quote Options, quote-local inline customization that must not create package-library records, and multiple parent quotes per inquiry.
- Quote currency is loaded from active system configuration and snapshotted on the quote; it is never provider input, and exchange conversion applies at acceptance.
- Pricing is stated per applicable option/date combination, with a derived price range before acceptance and a total only after FR-005 selection.
- Added the accepted-price-only analytics rule.

### System Data Schema

- Added `quote_options`, `quote_option_items`, `quote_option_date_prices`, and `quote_option_plan_days` as sections 7A through 7D, with columns, indexes, and relationships.
- Marked `quotes.package_id`, `quotes.treatment_date`, and `quotes.quote_amount` as deprecated pending consumer migration.
- Recorded that `estimated_grafts` and the generated `graft_description` are shared by every option, and that `currency` is a system-configured snapshot.
- Corrected the `quotes` relationships and added a note that `(inquiry_id, provider_id)` must not be unique.
- Added the additive-migration and compatibility-adapter note.

### System Technical Spec

- The quote and booking status flow now describes options and states that the acceptance unit is one option/date row, not the quote.
- Added the accepted-price-only analytics rule and the multiple-quotes-per-inquiry rule to the critical business logic.
- Added the option-aggregate indexes and annotated the illustrative quote migration and `QuoteService` snippets as pre-option compatibility code.

---

## 4. Deliberately Left Open

FR-005, FR-006, and FR-008 still describe the single-package quote contract. The Product Owner chose not to reconcile them in this pass. Both change requests record this as open and unscheduled, and it remains the largest integrity risk carried forward from CR-FR004-20260909-01.

---

## 5. Traceability

- `functional-requirements/fr004-quote-submission/prd.md` (v2.3)
- `functional-requirements/fr004-quote-submission/change-request-2026-09-09-quote-options-model.md` (CR-FR004-20260909-01, extended to v2.2)
- `functional-requirements/fr010-treatment-execution/prd.md` (v1.9)
- `functional-requirements/fr010-treatment-execution/change-request-2026-09-09-clinician-cardinality-alignment.md` (CR-FR010-20260909-01)
- `system-prd.md`, `system-data-schema.md`, `system-technical-spec.md`
- Source: `sources/meetings/meeting-02-launch-quote-options-fund-release-and-payments.md`
