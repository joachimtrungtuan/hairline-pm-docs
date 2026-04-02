# FR-017 Screen Operational Hardening — 2026-04-02

**Type**: Major Update  
**FR**: FR-017 Admin Billing & Financial Management  
**PRD Version**: 1.4 → 1.5  
**Files Modified**:
- `local-docs/project-requirements/functional-requirements/fr017-admin-billing-finance/prd.md`

---

## Summary

Applied the screen-model hardening pass after the targeted screen/field review. This update closes the remaining operational gaps around bulk actions, dispute handling, payout readiness, affiliate payout failure states, reconciliation metadata, and financial re-authentication.

---

## Changes by Screen

### Screen 1: Provider Billing — Upcoming Payments List
- Added row selection, payout reference, payout readiness, and blocked reason fields
- Added Batch Approval Toolbar with selected count, selected net total, approve-all action, and clear-selection control
- Added business rules for batch eligibility, batch confirmation, batch result summary, and bank-detail blocking states

### Screen 2: Provider Payout Detail Modal
- Added payout reconciliation metadata: payout reference, statement status, payout readiness, blocked reason, approved by/at, processed at, Stripe transfer ID, and failure reason
- Expanded treatment list with commission deducted and net contribution per treatment
- Added re-authenticated Approve Payout confirmation and Retry Payout confirmation modal specs

### Screen 3: Patient Billing — Invoice Management
- Tightened Payment Method display to masked values only for consistency with the privacy requirement

### Screen 3a: Patient Invoice Detail
- Added adjusted total after refund to the invoice header
- Added Stripe payment intent ID to payment history rows
- Added Reminder History table and Status Override History table with visibility rules

### Screen 3b: Refund Confirmation Modal
- Replaced the conflicting read-only refund model with calculated refund amount, adjusted refund amount, final refund amount, and adjustment justification fields
- Added re-authentication field and confirm-button gating rules
- Clarified when manual adjustment is allowed and how justification is captured

### Screen 5: Financial Reporting — Revenue Dashboard
- Added At Risk Invoice Count, Failed Payout Count, Refund Trend, and Affiliate Payout Status Summary
- Added business rules for failed payout counting and refund-trend drill-down behavior

### Screen 6: Affiliate Billing — Commission Payouts
- Added payout reference, payout readiness, processed-at, payment destination, Stripe transfer ID, failure reason, processed-by, and retry action
- Expanded payment status to include Failed
- Added re-authenticated Process Payout and Retry Payout confirmation modals
- Clarified two-tab behavior so failed affiliate payouts remain visible in Pending with a dedicated retry section

### Screen 7: Provider Earnings Tracker
- Added adjustment marker for refunded, partially refunded, and manually adjusted earnings
- Added provider-facing tooltip behavior so providers understand why a value changed without exposing admin-only notes

### Screen 8: Provider Payout History
- Added copy-reference button, transfer confirmation timestamp, and retry resolution history timeline
- Clarified that retry history remains visible even after a payout later resolves successfully

### Screen 9: Transaction Search & Audit Log
- Added Dispute Resolution Panel with Add to Next Payout support, target payout cycle, note capture, and optional provider notification
- Expanded audit log action filters to include affiliate payout actions, reminder events, currency alert decisions, payout-added-to-next-cycle, and re-authentication verification

---

## Requirements & Entity Alignment

### Functional Requirements Summary
- Updated `REQ-017-001` to include `At Risk` in the invoice filtering status set
- Updated `REQ-017-009` to explicitly include affiliate payout failure/retry visibility

### Key Entities
- Expanded **Entity 1 - Patient Invoice** with adjusted refund total and override-tracking attributes
- Expanded **Entity 2 - Provider Payout** with payout reference, readiness state, approval metadata, processing metadata, and failure reason
- Expanded **Entity 5 - Transaction Audit Log** with the new operational action types and affected entity types
- Expanded **Entity 6 - Affiliate Commission** with payout reference, readiness state, processing metadata, destination, failure reason, and `Failed` status

---

## Rationale

These changes do not add a new top-level screen area. They harden the existing FR-017 screen model so finance staff can:

- execute batch approvals safely,
- resolve payout disputes without leaving the module logic undefined,
- handle affiliate payout failures at parity with provider payouts,
- trace Stripe-side records during reconciliation,
- enforce re-authentication on money-moving actions,
- and explain exception states to both admins and providers.

---

## Minor Follow-up Alignment (2026-04-02)

- Added explicit `Payout Adjustments` support to Screen 3 so refund deductions from already-paid bookings appear as separate statement line items with carry-forward visibility when the current cycle cannot absorb the full amount
- Expanded Screen 7 adjustment handling so post-payout refunds can show a negative provider earning state with the marker `Refunded — Deducted from Next Payout`
- Made provider notification mandatory for Screen 9 dispute resolutions that use `Add to Next Payout`, while preserving optional notification for the other resolution actions
- Synchronized Screen 9 audit filtering and Entity 5 affected-entity typing so `Installment`, `Booking`, and `Currency Alert` records can all be represented consistently
