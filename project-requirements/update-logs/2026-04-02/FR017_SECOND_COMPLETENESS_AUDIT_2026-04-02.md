# FR-017 Second Completeness Audit Fixes — 2026-04-02

**Type**: Major Update  
**FR**: FR-017 Admin Billing & Financial Management  
**PRD Version**: 1.7 → 1.8  
**Files Modified**:
- `local-docs/project-requirements/functional-requirements/fr017-admin-billing-finance/prd.md`

---

## Summary

Second-pass screen and entity audit following the v1.4 completeness fixes. 13 gaps identified across entity schemas, screen interaction flows, missing action specs, and one operational edge case. All 13 resolved in this update.

---

## Changes by Category

### Entity Schema Fixes

#### Entity 3 — Installment Payment
- **Added `next_retry_date`** to key attributes. Field was already shown in Screen 4a's Installment Schedule Table but was absent from the entity definition.

#### Entity 2 — Provider Payout
- **Added `voided_by_admin_id`, `voided_at`, `void_reason`** to key attributes to support the new Void Statement action.
- **Added "Voided"** to `payout_status` enum alongside existing statuses.

#### Entity 5 — Transaction Audit Log
- **Added 6 missing action_type values**: `"Status Overridden"`, `"Note Added"`, `"Installment Retry"`, `"Bulk Approval"`, `"Payout Unapproved"`, `"Payout Voided"`.
- These were referenced in Screen 9 Tab 2 filters but absent from the entity definition — a direct inconsistency that would break audit log queries.
- Screen 9 Tab 2 filter list synchronized to match (added `"Payout Unapproved"`, `"Payout Voided"`; removed stray sort order).

---

### Screen 1: Financial Reporting — Revenue Dashboard
- **Added "Active Currency Alerts" KPI**: count of unacknowledged currency fluctuation alerts (triggered by FR-029). Clicking links to the notification list filtered to unresolved alerts; each links to Screen 10. Badge hidden when count = 0.
- **Added business rule**: alert count resets to 0 once all active alerts have a confirmed admin decision via Screen 10.

---

### Screen 2: Provider Billing — Upcoming Payments List
- **Added "Unapprove" action**: available ONLY for statements in "Approved" status before the payout-day cron runs. Requires mandatory reason (max 500 chars); reverts statement to "Pending Approval"; logged as `"Payout Unapproved"`.
- **Added "Void Statement" action**: available for "Pending Approval" and "Overdue" statements. Requires mandatory reason; permanently marks statement as "Voided" and removes it from auto-processing. Voided statements remain visible for audit history.
- **Added "Voided" to Status badge enum**.
- **Formally specified Batch Approval Confirmation Modal**: previously only described in prose. Now documented as an element table (Summary line, Selected count, Selected net total, Warning, Re-authentication, Confirm button, Cancel button, Result Summary) — consistent with Screen 3's individual approval modal format.

---

### Screen 3: Provider Payout Detail Modal
- **Added "Voided" to Statement Status badge enum**.

---

### Screen 4: Patient Billing — Invoice Management
- **Added Send Reminder Confirmation Modal**: previously "Send Reminder" was listed as a button with no interaction spec. New modal includes: patient name, invoice reference + outstanding balance, auto-selected Reminder Type (Upcoming Due / Overdue / At Risk based on invoice status), channel display ("Email + Push"), Confirm and Cancel buttons.
- **Added business rules for Send Reminder**: reminder content/template determined by FR-020; Reminder History updated on confirm; success/error toast shown to admin; manual reminder does not interfere with automated schedule.
- **Added re-authentication requirement to Override Status**: explicitly clarified that Override Status REQUIRES financial re-authentication before Confirm is enabled, consistent with the module-level RBAC rule covering all actions that change a financial status.

---

### Screen 5: Discount Usage Overview
- **Added filter controls**: by Status (Active / Expired / Disabled), Discount Type (Platform-Wide / Provider-Specific / Affiliate), and Active Window date range. Free-text search by discount code or campaign name.
- **Added CSV export** for finance reconciliation.
- Previously the only list screen in the module without filter/search/export capability.

---

### Screen 6: Affiliate Billing — Commission Payouts
- **Added "Add Note" action**: affiliate payouts now have the same internal notes capability as provider payouts (admin-only, max 500 chars, logged as `"Note Added"` in audit trail). Previously this parity was missing.
- **Added Select checkbox** to data fields for bulk selection.
- **Added formal Bulk Payout Toolbar**: element table with Selected Payouts count, Selected Total, "Process All Selected Payouts" button, Clear Selection button.
- **Added Bulk Affiliate Payout Confirmation Modal**: formal element table with summary line, payout period, destination warning, re-authentication, Confirm/Cancel buttons, and Result Summary state.
- **Added bulk payout business rules**: selection restricted to Status = "Pending", past due date, Payout Readiness = "Ready"; processing is sequential; failures do not block other affiliates.

---

### Screen 9: Transaction Search & Audit Log
- **Tab 2 filter synchronized**: `"Payout Unapproved"` and `"Payout Voided"` added to Action Type filter. Existing entries reordered for logical grouping.
- **"Target Payout Cycle" field type clarified**: changed from ambiguous `text` to `select` — dropdown of the affected provider's upcoming payout cycles displayed as "[Provider Name] — [Payout Date]". Only cycles in "Pending Approval" or future-scheduled state are selectable.

---

### Dependencies
- **Removed duplicate FR-006 entry**: FR-006 appeared twice in Internal Dependencies. Both descriptions merged into a single comprehensive entry covering both the booking confirmation → invoice trigger and the cancellation policy → refund calculation integration points.

---

### Edge Cases
- **Added refund-after-payout scenario**: patient refunded after provider has already received a completed Stripe transfer.
  - Refund returned to patient via Stripe; provider payout NOT immediately clawed back
  - Equivalent amount deducted from provider's NEXT payout cycle as a labelled line item in the payout statement
  - Screen 7 shows treatment with Adjustment Marker "Refunded — Deducted from Next Payout"
  - If deduction exceeds next cycle amount, carries forward to subsequent cycles (never silently absorbed)
  - Full audit trail recorded
