# FR-017 Screen Completeness Audit Fixes — 2026-04-02

**Type**: Major Update  
**FR**: FR-017 Admin Billing & Financial Management  
**PRD Version**: 1.3 → 1.4  
**Files Modified**:
- `local-docs/project-requirements/functional-requirements/fr017-admin-billing-finance/prd.md`

---

## Summary

Full screen-by-screen audit of all 8 existing screens against workflows, business rules, key entities, and user scenarios. 18 gaps identified (4 critical, 8 important, 6 minor). All 18 resolved in this update.

---

## Changes by Screen

### Screen 1: Provider Billing — Upcoming Payments List
- **Added "Retry Payout" action** for statements with status "Failed"; initiates Stripe re-transfer; logged in audit trail
- **Added "Failed" section** to list layout (below "Overdue", above "Upcoming / Pending Approval"); highlighted in red
- **Added provider name/ID** to filter options (previously: status, schedule, date range only)

### Screen 2: Provider Payout Detail Modal
- **Added Approve Confirmation Modal spec**: shows payout amount, destination (last 4 digits), Yes/Cancel; resolves gap where Workflow step 9 described a confirmation dialog that had no screen specification

### Screen 3: Patient Billing — Invoice Management
- **Added "At Risk" to Payment Status enum**: triggered when all 3 installment retries are exhausted; booking requires admin intervention
- **Updated Installment Plan badge** to show retry state: "2/5 — Retry 2/3 in progress" when an installment is in active retry cycle
- **Added "At Risk" section** at top of invoice list (surfaced above Overdue)
- **"Process Refund" now links to Screen 3b** (Refund Confirmation Modal)
- **"View Details" now links to Screen 3a** (Patient Invoice Detail)

### Screen 3a: Patient Invoice Detail *(new)*
Sub-screen opened by "View Details" on Screen 3. Contains:
- **Invoice Header**: all summary fields including `discount_code_applied`
- **Payment History Table**: all payments (deposit, installments, final) with type, scheduled/paid dates, amounts, method, status
- **Installment Schedule Table** (conditional): per-installment status, `retry_count`, next retry date
- **Refund History Table** (conditional): each refund with date, amount, type, mandatory reason, processing admin, Stripe ID, status

### Screen 3b: Refund Confirmation Modal *(new)*
Triggered by "Process Refund" on Screen 3 or Screen 3a. Contains:
- Auto-calculated refund amount based on FR-006 cancellation policy tiers (>30 days = 90%, 15–30 = 50%, <15 = 0%)
- Non-refundable amount displayed as "Platform fee (non-refundable)"
- **Mandatory Reason field** (min 1 char, max 500) — Confirm button disabled until populated
- Confirm button disabled entirely if treatment date has already passed (0% applies; admin must use Override Status instead)
- Partial refund support: admin can adjust pre-calculated amount with justification in Reason field

### Screen 5: Financial Reporting — Revenue Dashboard
- **Added Overdue Aging Breakdown panel**: drill-down from "Outstanding Patient Invoices" KPI; shows three buckets (0–30 days, 31–60 days, 60+ days overdue) each with invoice count and total amount; "At Risk" shown as a separate row

### Screen 6: Affiliate Billing — Commission Payouts
- **Payment Method field description updated**: documented source as FR-018 affiliate onboarding (not orphaned)
- **Added Process Payout Confirmation Modal spec**: shows commission amount, payout period, payment method with confirmation prompt
- **Added date/period filter and affiliate name/ID filter** to Notes

### Screen 7: Provider Earnings Tracker
- **Defined refunded treatment display**: treatment row shows Net Earning as £0.00 with "Refunded" label and strikethrough on original amount; excluded from Total Pending Earnings; partial refunds recalculate Net Earning against adjusted booking amount
- **Added "Payout Failed — [Date]"** to Payout Status options; failed treatments revert to "Pending Next Payout" once retry succeeds

### Screen 8: Provider Payout History
- **Added "Failed" to Status options** alongside "Processing" and "Paid"
- **Added Failure Reason field** (conditional, shown when Status = "Failed")
- **Updated business rules**: payout entries now appear on first Stripe transfer initiation (not only on transfer.paid); "Failed" entries show provider-facing message explaining the situation

### Screen 9: Transaction Search & Audit Log *(new)*
New admin screen accessible from "Billing & Finance" navigation.
- **Tab 1 — Transaction Search**: search by Booking Reference, Invoice Number, Patient, Provider, or Affiliate; filter by record type, date range, status; results link to relevant detail screens; solves Workflow B1 dispute resolution requirement
- **Tab 2 — Audit Log**: full audit log viewer (Entity 5) with filtering by date, admin user, action type, affected entity; read-only; export to CSV; 7-year retention visible in UI

### Screen 10: Currency Alert Detail Modal *(new)*
Notification-triggered modal for Workflow B2 (currency fluctuation).
- **Affected Bookings Table**: shows booking reference, locked rate, current rate, rate difference %, estimated exposure, upcoming payout date
- **Admin Decision Panel**: three options (Accept Risk / Contact Providers / Adjust via FR-029); mandatory notes field; decision logged to audit trail as "Currency Alert Decision"

---

## Key Entity Updates

- **Entity 1 (Patient Invoice)** `payment_status`: added `"At Risk"`
- **Entity 6 (Affiliate Commission)** `payout_status`: added `"Processing"` (was missing despite UI showing it)
