# Design Layout Verification Report — FR-017

**Report Date**: 2026-04-20
**Report Type**: Design Layout Verification
**FR Scope**: FR-017 - Admin Billing & Financial Management
**Flow Scope**: Full FR check
**Layout Source**: `layout-temp/` (`financial-report/`, `provider-billing/`, `patient-billing/`, `discount-usage/`, `aff-billing/`, `transaction-search/`, `currency-alert/`, `provider-earnings/`)
**Platform**: Mixed (Admin Web + Provider Web)
**Status**: Completed

---

## Summary Dashboard

| # | Flow | Module | Screens Required | Screens Verified | Layout Status | Field Coverage |
|---|------|--------|-----------------|-----------------|---------------|----------------|
| F1 | Revenue Dashboard & Reporting | A-05: Billing & Financial Reconciliation | 1 | 1 | 🟢 COMPLETE | ~100% |
| F2 | Provider Payout Processing | A-05: Billing & Financial Reconciliation | 2 | 2 | 🟡 PARTIAL | ~93% |
| F3 | Patient Billing & Refund Management | A-05: Billing & Financial Reconciliation | 3 | 3 | 🟡 PARTIAL | ~91% |
| F4 | Discount Usage Tracking | A-05: Billing & Financial Reconciliation | 1 | 1 | 🟢 COMPLETE | ~100% |
| F5 | Affiliate Billing & Commission Payouts | A-05: Billing & Financial Reconciliation | 1 | 1 | 🟡 PARTIAL | ~100% |
| F6 | Transaction Search & Audit | A-05: Billing & Financial Reconciliation | 1 | 1 | 🟡 PARTIAL | ~94% |
| F7 | Currency Alert Response | A-05: Billing & Financial Reconciliation | 1 | 1 | 🟢 COMPLETE | ~100% |
| F8 | Provider Earnings & Payout History | PR-05: Financial Management & Reporting | 2 | 2 | 🟡 PARTIAL | ~96% |

**Overall**: 🟡 PARTIAL — Admin-side billing and investigation surfaces are mostly designed, several execution-critical mismatches remain, and the provider-facing financial scope is now covered for both screens, but Screen 10 is still incomplete at the payout-history list level.
**Screens**: 12/12 screens now have mapped design coverage, with partial gaps remaining on some flows

---

## Layout File Inventory

### Mapped to Spec Flows

| Layout File | Maps to Flow | Maps to Screen |
|-------------|-------------|----------------|
| `financial-report/Financial Reporting.jpg` | F1 | Screen 1 (Financial Reporting - Revenue Dashboard) |
| `financial-report/Financial Reporting - Compare to previous period.jpg` | F1 | Screen 1 (Financial Reporting - Revenue Dashboard) |
| `provider-billing/Full Table.jpg` | F2 | Screen 2 (Provider Billing - Upcoming Payments List) |
| `provider-billing/Filter.jpg` | F2 | Screen 2 (Provider Billing - Upcoming Payments List) |
| `provider-billing/Actions.jpg` | F2 | Screen 2 (Provider Billing - Upcoming Payments List) |
| `provider-billing/Approve All Selected Payouts.jpg` | F2 | Screen 3 (Batch Approval Confirmation Modal) |
| `provider-billing/Provider Payout Detail.jpg` | F2 | Screen 3 (Provider Payout Detail Modal) |
| `provider-billing/Approve Confirmation.jpg` | F2 | Screen 3 (Approve Confirmation Modal) |
| `provider-billing/Retry Failed Payout.jpg` | F2 | Screen 3 (Retry Payout Confirmation Modal) |
| `provider-billing/Payout Statement - Approved, Processing, Paid, Fail.jpg` | F2 | Screen 3 (Provider Payout Detail Modal) |
| `provider-billing/Payout statement - Processing, Paid, Fail.jpg` | F2 | Screen 3 (Provider Payout Detail Modal) |
| `provider-billing/Payout statement - Fail.jpg` | F2 | Screen 3 (Provider Payout Detail Modal) |
| `patient-billing/Patient Billing.jpg` | F3 | Screen 4 (Patient Billing - Invoice Management) |
| `patient-billing/Full Table - Patient Billing.jpg` | F3 | Screen 4 (Patient Billing - Invoice Management) |
| `patient-billing/Filter.jpg` | F3 | Screen 4 (Patient Billing - Invoice Management) |
| `patient-billing/Actions.jpg` | F3 | Screen 4 (Patient Billing - Invoice Management) |
| `patient-billing/Patient Invoice Detail.jpg` | F3 | Screen 4a (Patient Invoice Detail) |
| `patient-billing/Patient Invoice Detail - Having Refund.jpg` | F3 | Screen 4a (Patient Invoice Detail) |
| `patient-billing/Refund Confirmation.jpg` | F3 | Screen 4b (Refund Confirmation Modal) |
| `patient-billing/Refund Confirmation - Adjusted Refund Amount differs from Calculated Refund Amount.jpg` | F3 | Screen 4b (Refund Confirmation Modal) |
| `patient-billing/Override Status.jpg` | F3 | Screen 4a (Patient Invoice Detail) |
| `patient-billing/Send Reminder Confirmation.jpg` | F3 | Screen 4 (Patient Billing - Invoice Management) |
| `discount-usage/Discount Usage.jpg` | F4 | Screen 5 (Discount Usage Overview) |
| `discount-usage/Full Table.jpg` | F4 | Screen 5 (Discount Usage Overview) |
| `discount-usage/Filter.jpg` | F4 | Screen 5 (Discount Usage Overview) |
| `aff-billing/Affiliate Billing - Pending Payouts.jpg` | F5 | Screen 6 (Affiliate Billing - Commission Payouts) |
| `aff-billing/Affiliate Billing - Paid Payouts.jpg` | F5 | Screen 6 (Affiliate Billing - Commission Payouts) |
| `aff-billing/Full Table - Pending Payouts.jpg` | F5 | Screen 6 (Affiliate Billing - Commission Payouts) |
| `aff-billing/Full Table - Paid Payouts.jpg` | F5 | Screen 6 (Affiliate Billing - Commission Payouts) |
| `aff-billing/Table - Pending Payouts.jpg` | F5 | Screen 6 (Affiliate Billing - Commission Payouts) |
| `aff-billing/Table - Paid Payouts.jpg` | F5 | Screen 6 (Affiliate Billing - Commission Payouts) |
| `aff-billing/Affiliate Billing - Affiliate Billing Details.jpg` | F5 | Screen 6 (Referral Booking Sub-Table) |
| `aff-billing/Table - Referral Bookings Breakdown.jpg` | F5 | Screen 6 (Referral Booking Sub-Table) |
| `aff-billing/Full Table - Referral Bookings Breakdown.jpg` | F5 | Screen 6 (Referral Booking Sub-Table) |
| `aff-billing/Filter.jpg` | F5 | Screen 6 (Affiliate Billing - Commission Payouts) |
| `aff-billing/Actions.jpg` | F5 | Screen 6 (Affiliate Billing - Commission Payouts) |
| `aff-billing/Process Payout Confirmation Modal.jpg` | F5 | Screen 6 (Process Payout Confirmation Modal) |
| `aff-billing/Retry Payout Confirmation Modal.jpg` | F5 | Screen 6 (Retry Payout Confirmation Modal) |
| `aff-billing/State A — Initial (before submitting).jpg` | F5 | Screen 6 (Bulk Affiliate Payout Confirmation Modal) |
| `aff-billing/State B — Result Summary (after processing).jpg` | F5 | Screen 6 (Bulk Affiliate Payout Confirmation Modal) |
| `transaction-search/Transaction Search.jpg` | F6 | Screen 7 (Transaction Search tab) |
| `transaction-search/Table - Transaction Search.jpg` | F6 | Screen 7 (Transaction Search tab) |
| `transaction-search/Full Table - Transaction Search.jpg` | F6 | Screen 7 (Transaction Search tab) |
| `transaction-search/Filter.jpg` | F6 | Screen 7 (Transaction Search tab) |
| `transaction-search/Transaction Search - Dispute Resolution Panel.jpg` | F6 | Screen 7 (Dispute Resolution Panel) |
| `transaction-search/Audit Log.jpg` | F6 | Screen 7 (Audit Log tab) |
| `transaction-search/Table - Audit Log.jpg` | F6 | Screen 7 (Audit Log tab) |
| `transaction-search/Full Table - Audit Log.jpg` | F6 | Screen 7 (Audit Log tab) |
| `transaction-search/Transaction Search - No Results State.jpg` | F6 | Screen 7 (Transaction Search empty state) |
| `currency-alert/Currency Alert Detail Modal.jpg` | F7 | Screen 8 (Currency Alert Detail Modal) |
| `currency-alert/Table - Affected Bookings.jpg` | F7 | Screen 8 (Affected Bookings Table) |
| `currency-alert/Full Table - Affected Bookings.jpg` | F7 | Screen 8 (Affected Bookings Table) |
| `provider-earnings/Earnings Tracker.jpg` | F8 | Screen 9 (Provider Earnings Tracker) |
| `provider-earnings/Table - Earnings Tracker.jpg` | F8 | Screen 9 (Provider Earnings Tracker) |
| `provider-earnings/Full Table - Earnings Tracker.jpg` | F8 | Screen 9 (Provider Earnings Tracker) |
| `provider-earnings/Filter.jpg` | F8 | Screen 9 (Provider Earnings Tracker Filters) |
| `payout-history/Treatment Breakdown.jpg` | F8 | Screen 10 (Provider Payout History detail state) |
| `payout-history/Table - Treatment Breakdown.jpg` | F8 | Screen 10 (Treatment Breakdown sub-table) |
| `payout-history/Full Table - Treatment Breakdown.jpg` | F8 | Screen 10 (Treatment Breakdown sub-table) |

### Unmapped Files

| Layout File | Likely Purpose | Notes |
|-------------|---------------|-------|
| `provider-billing/Payout Statement - Full Table.jpg` | Provider payout detail variant | Appears redundant with Screen 3 detail/table variants; verify during F2 |
| `provider-billing/Financial Reporting.jpg` | Possible misplaced revenue dashboard variant | Located under `provider-billing/`; likely duplicate of Screen 1 or misfiled asset |

---

## Detailed Verification by Flow

---

### Flow F1: Revenue Dashboard & Reporting

**Status**: 🟢 COMPLETE — Dashboard layout covers the specified reporting KPIs, comparison mode, charts, and drill-down structures.
**Screens required**: 1
**Layout files**: `financial-report/Financial Reporting.jpg`, `financial-report/Financial Reporting - Compare to previous period.jpg`

#### Screen 1: Financial Reporting - Revenue Dashboard

**Layout**: `financial-report/Financial Reporting.jpg`, `financial-report/Financial Reporting - Compare to previous period.jpg`

##### Flow Context

- **User arrives from**: Admin Platform navigation under `Billing & Finance -> Financial Reporting`
- **Screen purpose**: Provide a financial command center for executive review, KPI drill-downs, and cross-module reporting
- **Entry point**: Present in both layouts via left-nav selection and page breadcrumb
- **Exit path**: Present through drill-down links (`View invoices`, `View alerts`, `Go to Provider Billing`) and persistent left navigation
- **Data continuity**: Correct; dashboard references downstream billing, alerts, provider payouts, affiliates, and discount usage consistently with FR-017
- **Flow context issues**: None identified from the static layouts

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Date Range Selector | Yes | ✅ | Present as period dropdown and visible selected date range in both layouts |
| Currency Selector | Yes | ✅ | Present as `Currency USD` dropdown in both layouts |
| Total Revenue | Yes | ✅ | Present as primary KPI card |
| Platform Commission | Yes | ✅ | Present as KPI card |
| Provider Payouts | Yes | ✅ | Present as KPI card |
| Affiliate Payouts | Yes | ✅ | Present as KPI card |
| At Risk Invoice Count | Yes | ✅ | Present as `At Risk Invoice` KPI card |
| Failed Payout Count | Yes | ✅ | Present as `Failed Payouts` KPI card |
| Active Currency Alerts | Yes | ✅ | Present as KPI card with alert count and action link |
| Refund Trend | Yes | ✅ | Present as line chart section |
| Outstanding Patient Invoices | Yes | ✅ | Present as KPI total above aging table |
| Overdue Aging Breakdown | Yes | ✅ | Present as bucket table with 0-30, 31-60, 60+ and `At Risk` rows |
| Pending Provider Payouts | Yes | ✅ | Present as side KPI panel with CTA to provider billing |
| Affiliate Payout Status Summary | Yes | ✅ | Present as summary table grouped by statuses |
| Revenue by Country | Yes | ✅ | Present as chart section |
| Revenue by Treatment Type | Yes | ✅ | Present as chart section |
| Revenue Trend | Yes | ✅ | Present as line chart section |
| Top Providers by Revenue | Yes | ✅ | Present as sortable-style table block |
| Discount Usage | Yes | ✅ | Present as summary table block |
| Conversion Rate | Yes | ✅ | Present as KPI card |

**Extra Elements**:

- Export Full Report CTA
- Compare-to-previous-period toggle, comparison banner, delta rows, and previous-period columns
- Anomaly/high-refund warning badges embedded into chart sections

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 20/20 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|

**Flow Coverage Gaps**:

- None from the provided layouts

---

### Flow F5: Affiliate Billing & Commission Payouts

**Status**: 🟡 PARTIAL — The affiliate payout flow is broadly designed and operationally rich, but the primary screen is mislabeled as provider billing and the bulk-payout total is internally inconsistent between list and modal states.
**Screens required**: 1
**Layout files**: `aff-billing/Affiliate Billing - Pending Payouts.jpg`, `aff-billing/Affiliate Billing - Paid Payouts.jpg`, `aff-billing/Full Table - Pending Payouts.jpg`, `aff-billing/Full Table - Paid Payouts.jpg`, `aff-billing/Table - Pending Payouts.jpg`, `aff-billing/Table - Paid Payouts.jpg`, `aff-billing/Affiliate Billing - Affiliate Billing Details.jpg`, `aff-billing/Table - Referral Bookings Breakdown.jpg`, `aff-billing/Full Table - Referral Bookings Breakdown.jpg`, `aff-billing/Filter.jpg`, `aff-billing/Actions.jpg`, `aff-billing/Process Payout Confirmation Modal.jpg`, `aff-billing/Retry Payout Confirmation Modal.jpg`, `aff-billing/State A — Initial (before submitting).jpg`, `aff-billing/State B — Result Summary (after processing).jpg`

#### Screen 6: Affiliate Billing - Commission Payouts

**Layout**: `aff-billing/Affiliate Billing - Pending Payouts.jpg`, `aff-billing/Affiliate Billing - Paid Payouts.jpg`, `aff-billing/Full Table - Pending Payouts.jpg`, `aff-billing/Full Table - Paid Payouts.jpg`, `aff-billing/Affiliate Billing - Affiliate Billing Details.jpg`, `aff-billing/Process Payout Confirmation Modal.jpg`, `aff-billing/Retry Payout Confirmation Modal.jpg`, `aff-billing/State A — Initial (before submitting).jpg`, `aff-billing/State B — Result Summary (after processing).jpg`

##### Flow Context

- **User arrives from**: Admin navigation under `Billing & Finance -> Affiliate Billing`
- **Screen purpose**: Review monthly affiliate commissions, process single or bulk payouts, inspect failed states, and reconcile payout detail by referral booking
- **Entry point**: Present through breadcrumb and active left-nav item for affiliate billing
- **Exit path**: Present through row actions, payout detail page, process/retry modals, report download, and tab switch between pending and paid states
- **Data continuity**: Strong; list values carry through to detail, booking breakdown, process modal, retry modal, and batch result summary
- **Flow context issues**: The page title is rendered as `Provider Billing` across the list views even though the breadcrumb and left navigation correctly identify `Affiliate Billing`

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Select | Conditional | ✅ | Checkboxes shown for eligible pending rows and bulk toolbar state |
| Affiliate Name | Yes | ✅ | Present in pending/paid lists and detail page |
| Affiliate ID | Yes | ✅ | Present in pending/paid lists and detail page |
| Payout Reference | Yes | ✅ | Present in full paid table and detail page |
| Discount Code(s) | Yes | ✅ | Present in full paid table and referral breakdown |
| Payout Period | Yes | ✅ | Present in list, detail page, and all payout modals |
| Total Referrals | Yes | ✅ | Present in list and reflected in referral breakdown count |
| Total Referral Revenue | Yes | ✅ | Present in pending/paid tables |
| Commission Rate | Yes | ✅ | Present in list and referral breakdown |
| Commission Earned | Yes | ✅ | Present in list, detail page, and process/retry modals |
| Payment Status | Yes | ✅ | Present with `Pending`, `Processing`, `Paid`, and failed/retry states represented across layouts |
| Payout Readiness | Yes | ✅ | Present in detail page and retry context |
| Payment Date | Conditional | ✅ | Present in full paid table |
| Processed At | Conditional | ✅ | Present in full paid table |
| Payment Method | Yes | ✅ | Present in full paid table and process modal |
| Payment Destination | Conditional | ✅ | Present in full paid table, process modal, and retry modal |
| Stripe Transfer ID | Conditional | ✅ | Present in full paid table |
| Failure Reason | Conditional | ✅ | Present in retry modal and full paid table failed column |
| Processed By | Conditional | ✅ | Present in full paid table |
| Actions | Yes | ✅ | Present via kebab actions and top-level CTAs on the detail page |

**Extra Elements**:

- Required two-tab split between `Pending Payouts` and `Paid Payouts`
- Failed / Requires Retry section pinned inside the pending tab
- Bulk payout toolbar with selected count, selected total, process-all CTA, and clear-selection CTA
- Bulk result summary state after processing
- Referral booking breakdown table with booking reference, patient name, amount, commission rate, commission earned, currency, and referral code
- Download Report CTA

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 20/20 (100%)
**Critical Issues**:

- The bulk-payout toolbar shows `Selected total: $18,460.00`, but the confirmation modal summarizes `2 affiliates totalling £11,572.00`; this is a money-value mismatch on a transfer-confirmation step
- The main page title is `Provider Billing` instead of `Affiliate Billing`, which creates a scope/ownership conflict inside an adjacent provider-billing module

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-17` The batch-selection toolbar total does not match the amount shown in the confirmation modal | Keep selected-count and selected-total values synchronized between the parent list and the modal |
| ⚠️ UX Improvement | Affiliate payout views retain a `Provider Billing` page title even though the screen is clearly under affiliate billing | Rename the page title to `Affiliate Billing` across list and modal-entry states so operators do not confuse the two payout domains |

**Flow Coverage Gaps**:

- No direct evidence of an `Add Note` interaction even though the FR requires it for all statuses

---

### Flow F6: Transaction Search & Audit

**Status**: 🟡 PARTIAL — The unified investigation surface, no-results state, dispute workflow, and audit log table are designed, but the dispute modal mislabels the mandatory internal-note field and that weakens a key compliance control.
**Screens required**: 1
**Layout files**: `transaction-search/Transaction Search.jpg`, `transaction-search/Table - Transaction Search.jpg`, `transaction-search/Full Table - Transaction Search.jpg`, `transaction-search/Filter.jpg`, `transaction-search/Transaction Search - Dispute Resolution Panel.jpg`, `transaction-search/Audit Log.jpg`, `transaction-search/Table - Audit Log.jpg`, `transaction-search/Full Table - Audit Log.jpg`, `transaction-search/Transaction Search - No Results State.jpg`

#### Screen 7: Transaction Search & Audit Log

**Layout**: `transaction-search/Transaction Search.jpg`, `transaction-search/Full Table - Transaction Search.jpg`, `transaction-search/Transaction Search - Dispute Resolution Panel.jpg`, `transaction-search/Audit Log.jpg`, `transaction-search/Full Table - Audit Log.jpg`, `transaction-search/Transaction Search - No Results State.jpg`

##### Flow Context

- **User arrives from**: Admin navigation under `Billing & Finance -> Transaction Search & Audit Log`
- **Screen purpose**: Search across invoices, payouts, installments, refunds, and affiliate commissions, then resolve disputes or review immutable audit history
- **Entry point**: Present via breadcrumb, page title, dual-tab layout, and search/filter controls
- **Exit path**: Present through result links, dispute-resolution modal, tab switch, and clear-search path for empty states
- **Data continuity**: Strong; a booking-linked payout result carries into the dispute modal with booking reference, provider, expected payout, prior inclusion status, target cycle, and save action
- **Flow context issues**: The dispute modal labels the internal-note textarea as `Target Payout Cycle`, which can mislead admins during a required audit-writing step

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Search By | Yes | ✅ | Present with `Booking Reference` example |
| Search Input | Yes | ✅ | Present in normal and no-results states |
| Record Type | Yes | ✅ | Present as multi-select summary control |
| Date Range | Optional | ✅ | Present |
| Status | Optional | ✅ | Present |
| Record Type Result | Yes | ✅ | Present as colored badge column |
| Reference / ID | Yes | ✅ | Present as clickable link column |
| Booking Reference | Conditional | ✅ | Present as clickable link column |
| Patient / Provider / Affiliate | Yes | ✅ | Present in results list |
| Date | Yes | ✅ | Present |
| Amount | Yes | ✅ | Present |
| Currency | Yes | ✅ | Present |
| Status | Yes | ✅ | Present |
| Empty State Message | Conditional | ✅ | Present with exact search-term interpolation behavior |
| Audit Timestamp | Yes | ✅ | Present |
| Audit Admin | Yes | ✅ | Present |
| Action Type | Yes | ✅ | Present in full audit table |
| Affected Entity | Yes | ✅ | Present as clickable field in full audit table |
| Before Value | Yes | ✅ | Present in full audit table |
| After Value | Yes | ✅ | Present in full audit table |
| IP Address | Yes | ✅ | Present |
| Notes | Yes | ✅ | Present |
| Resolution Action | Conditional | ✅ | Present in dispute modal |
| Target Payout Cycle | Conditional | ✅ | Present in dispute modal |
| Internal Note | Conditional | ✅ | Present as textarea, but mislabeled |
| Notify Provider | Conditional | ✅ | Present and auto-selected/disabled in the shown `Add to Next Payout` state |
| Save Resolution | Conditional | ✅ | Present |

**Extra Elements**:

- Two-tab split between `Transaction Search` and `Audit Log`
- Filter entry point on both tabs
- Clear button on the main search form
- No-results state with recovery CTA

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 27/27 (100%)
**Critical Issues**:

- The dispute modal’s mandatory note textarea is labeled `Target Payout Cycle` instead of `Internal Note`, which can lead to incorrect operator input and ambiguous audit entries

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | The final textarea in the dispute modal repeats the `Target Payout Cycle` label instead of identifying itself as the required internal note | Rename the textarea label to `Internal Note` and keep the payout-cycle selector as a separate control immediately above it |

**Flow Coverage Gaps**:

- None beyond the mislabeled mandatory note field

---

### Flow F7: Currency Alert Response

**Status**: 🟢 COMPLETE — The alert modal includes the required header metrics, affected-booking table, and admin decision controls needed to document a response.
**Screens required**: 1
**Layout files**: `currency-alert/Currency Alert Detail Modal.jpg`, `currency-alert/Table - Affected Bookings.jpg`, `currency-alert/Full Table - Affected Bookings.jpg`

#### Screen 8: Currency Alert Detail Modal

**Layout**: `currency-alert/Currency Alert Detail Modal.jpg`, `currency-alert/Full Table - Affected Bookings.jpg`

##### Flow Context

- **User arrives from**: Currency alert notification or linked alert context
- **Screen purpose**: Review rate movement, inspect at-risk bookings, and log an explicit operator decision with rationale
- **Entry point**: Present as an overlaid modal with alert header context
- **Exit path**: Present through `Confirm Decision` and `Close`
- **Data continuity**: Correct; the alert header, bookings table, and admin decision section all operate on the same GBP/EUR fluctuation scenario
- **Flow context issues**: None that block the intended response flow

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Alert Title | Yes | ✅ | Present as `Currency Fluctuation Alert` |
| Currency Pair | Yes | ✅ | Present |
| Fluctuation | Yes | ✅ | Present and highlighted |
| Alert Threshold | Yes | ✅ | Present |
| Alert Generated | Yes | ✅ | Present |
| Booking Reference | Yes | ✅ | Present |
| Provider | Yes | ✅ | Present |
| Treatment Date | Yes | ✅ | Present in full affected-bookings table |
| Booking Amount | Yes | ✅ | Present in full affected-bookings table |
| Patient Currency | Yes | ✅ | Present in full affected-bookings table |
| Provider Currency | Yes | ✅ | Present in full affected-bookings table |
| Locked Rate | Yes | ✅ | Present |
| Current Rate | Yes | ✅ | Present |
| Rate Difference | Yes | ✅ | Present and highlighted in red |
| Estimated Exposure | Yes | ✅ | Present |
| Payout Date | Yes | ✅ | Present |
| Decision | Yes | ✅ | Present with all three radio options |
| Notes | Yes | ✅ | Present as textarea |
| Confirm Decision button | Yes | ✅ | Present |
| Close button | Yes | ✅ | Present |

**Extra Elements**:

- Paging controls on the affected-bookings table
- Right-aligned `Payout within 14 days` context label above the table

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 20/20 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| 💡 UX Suggestion | The bookings section is titled `Payment History`, which is less precise than the FR’s `Affected Bookings` framing | Rename the section header to `Affected Bookings` to better match the alert-review purpose |

**Flow Coverage Gaps**:

- None from the provided layouts

### Flow F2: Provider Payout Processing

**Status**: 🟡 PARTIAL — Core payout list, detail, approval, and retry states are designed, but the batch approval state is internally inconsistent and the payout detail is implemented as a page rather than the specified modal.
**Screens required**: 2
**Layout files**: `provider-billing/Full Table.jpg`, `provider-billing/Filter.jpg`, `provider-billing/Actions.jpg`, `provider-billing/Approve All Selected Payouts.jpg`, `provider-billing/Provider Payout Detail.jpg`, `provider-billing/Approve Confirmation.jpg`, `provider-billing/Retry Failed Payout.jpg`, `provider-billing/Payout Statement - Approved, Processing, Paid, Fail.jpg`, `provider-billing/Payout statement - Processing, Paid, Fail.jpg`, `provider-billing/Payout statement - Fail.jpg`

#### Screen 2: Provider Billing - Upcoming Payments List

**Layout**: `provider-billing/Full Table.jpg`, `provider-billing/Filter.jpg`, `provider-billing/Actions.jpg`, `provider-billing/Approve All Selected Payouts.jpg`

##### Flow Context

- **User arrives from**: Admin navigation under `Billing & Finance -> Provider Billing`
- **Screen purpose**: Review payout statements by section, triage blockers, and trigger individual or bulk approval actions
- **Entry point**: Present via breadcrumb/page title and persistent left navigation
- **Exit path**: Present through row actions, filter drawer, export, and batch approval modal
- **Data continuity**: Correct; sections for `Overdue`, `Failed`, and `Upcoming / Pending Approval` align with the workflow branches in FR-017
- **Flow context issues**: Batch approval count in the toolbar does not match the count shown in the approval modal

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Select | Conditional | ✅ | Checkboxes shown for selectable rows in the list view and batch toolbar state |
| Provider Name | Yes | ✅ | Present in table rows with avatar and name |
| Provider ID | Yes | ✅ | Present beneath provider name in each row |
| Payout Reference | Yes | ✅ | Present as dedicated table column |
| Payment Schedule | Yes | ✅ | Present as badge column (`Weekly`, `2x a Month`, `Monthly`) |
| Next Payout Date | Yes | ✅ | Present as dedicated date column |
| Outstanding Earnings | Yes | ✅ | Present as table column |
| Commission | Yes | ✅ | Present as table column |
| Net Payout | Yes | ✅ | Present as table column |
| Bank Account | Yes | ✅ | Present as masked destination column |
| Payout Readiness | Yes | ✅ | Present as color-coded badge column |
| Status | Yes | ✅ | Present as color-coded badge column with all required statuses represented across the layouts |
| Blocked Reason | Conditional | ✅ | Present for failed and blocked rows |
| Actions | Yes | ✅ | Present via kebab menu; conditional states shown in `Actions.jpg` |
| Selected Statements | Yes | ❌⚠️ | `Approve All Selected Payouts.jpg` shows `3 selected` in the toolbar but `5` selected statements in the modal |
| Selected Net Total | Yes | ✅ | Present in batch toolbar and batch approval modal |
| Approve All Selected Payouts | Yes | ✅ | Present as toolbar CTA and modal confirm path |
| Clear Selection | Yes | ✅ | Present in toolbar |

**Extra Elements**:

- KPI summary cards for `Overdue`, `Failed / Pending Approval`, and `Total Net Payout (All)`
- Search input for provider name / ID
- Export CSV CTA

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 17/18 (~94%)
**Critical Issues**:

- Batch approval count is inconsistent between the parent toolbar and the confirmation modal, which would undermine trust in a money-moving action

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-17` CTA/summary state is unclear because the toolbar says `3 selected` while the approval modal summarizes `5` selected statements | Keep the selection count and combined net total synchronized between the parent list state and the confirmation modal |

#### Screen 3: Provider Payout Detail Modal

**Layout**: `provider-billing/Provider Payout Detail.jpg`, `provider-billing/Approve Confirmation.jpg`, `provider-billing/Retry Failed Payout.jpg`, `provider-billing/Payout Statement - Approved, Processing, Paid, Fail.jpg`, `provider-billing/Payout statement - Processing, Paid, Fail.jpg`, `provider-billing/Payout statement - Fail.jpg`

##### Flow Context

- **User arrives from**: `View Details` / approval actions on the provider billing list
- **Screen purpose**: Review payout contents, adjustments, and status metadata before approving, retrying, or documenting the statement
- **Entry point**: Present, but implemented as a routed detail page with breadcrumb rather than an in-context modal
- **Exit path**: Present through breadcrumbs, approval modal, retry modal, and download CTA
- **Data continuity**: Correct; list-state values carry through to payout statement metadata, treatment lines, adjustments, and payout summary
- **Flow context issues**: Container pattern does not match the FR, which explicitly defines this screen as a modal

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Provider Name | Yes | ✅ | Present in payout statement metadata and approval/retry modals |
| Provider ID | Yes | ✅ | Present in payout statement metadata |
| Payout Reference | Yes | ✅ | Present in metadata and approval modal |
| Statement Status | Yes | ✅ | Present across pending approval, approved, processing, and failed variants |
| Payout Period | Yes | ✅ | Present in metadata and approval modal |
| Payout Readiness | Yes | ✅ | Present in metadata and retry modal |
| Blocked Reason | Conditional | ✅ | Failure reason shown in failed variant and retry modal |
| Bank Account | Yes | ✅ | Present in metadata and modal destination summary |
| Treatment List | Yes | ✅ | Present as itemized booking table |
| Payout Adjustments | Conditional | ✅ | Present as adjustments table in payout detail layout |
| Total Revenue | Yes | ✅ | Present in payout summary card |
| Commission Configuration | Yes | ✅ | Present as metadata field |
| Commission Amount | Yes | ✅ | Present in payout summary card |
| Net Payout | Yes | ✅ | Present in payout summary and modal details |
| Approved By | Conditional | ✅ | Present in approved / processing / failed variants |
| Approved At | Conditional | ✅ | Present in approved / processing / failed variants |
| Processed At | Conditional | ✅ | Present in processing / failed variants |
| Stripe Transfer ID | Conditional | ✅ | Present in processing / failed variants |
| Failure Reason | Conditional | ✅ | Present in failed variant and retry modal |
| Internal Notes | No | ✅ | Present as textarea block in payout detail layout |

**Extra Elements**:

- Download Detailed Report CTA
- Payout Summary side card
- Warning icon treatment row treatment marker and explanatory footnote

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 20/20 (100%)
**Critical Issues**:

- Screen is specified as a modal in FR-017, but the provided layout is a full routed page with breadcrumb navigation; this changes the approval-review flow and return path

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `W-04` The design uses a routed page with breadcrumbs for a screen defined as a modal review step, which weakens the expected in-context return path from the list | Either redesign Screen 3 as a true modal/drawer launched from the list, or update the FR to explicitly approve a routed detail page pattern |

**Flow Coverage Gaps**:

- No evidence of the post-batch result summary state required after bulk approval; the provided batch modal stops at confirmation
- Screen 3 interaction container differs from the FR-defined modal behavior

---

### Flow F3: Patient Billing & Refund Management

**Status**: 🟡 PARTIAL — The invoice list, detail, and refund modal are largely designed, but the detail screen misses required warning/close elements and the required 0% refund state is not evidenced.
**Screens required**: 3
**Layout files**: `patient-billing/Patient Billing.jpg`, `patient-billing/Full Table - Patient Billing.jpg`, `patient-billing/Filter.jpg`, `patient-billing/Actions.jpg`, `patient-billing/Patient Invoice Detail.jpg`, `patient-billing/Patient Invoice Detail - Having Refund.jpg`, `patient-billing/Refund Confirmation.jpg`, `patient-billing/Refund Confirmation - Adjusted Refund Amount differs from Calculated Refund Amount.jpg`, `patient-billing/Override Status.jpg`, `patient-billing/Send Reminder Confirmation.jpg`

#### Screen 4: Patient Billing - Invoice Management

**Layout**: `patient-billing/Patient Billing.jpg`, `patient-billing/Full Table - Patient Billing.jpg`, `patient-billing/Actions.jpg`, `patient-billing/Override Status.jpg`, `patient-billing/Send Reminder Confirmation.jpg`

##### Flow Context

- **User arrives from**: Admin navigation under `Billing & Finance -> Patient Billing`
- **Screen purpose**: Triage patient invoices by risk/status, inspect balances, and launch reminders, refunds, downloads, or overrides
- **Entry point**: Present through page title, breadcrumb, search, and filter entry points
- **Exit path**: Present through row actions, filter drawer, CSV export, and bulk overdue reminder CTA
- **Data continuity**: Correct; invoice rows carry the invoice/patient/booking references needed to open detail or action modals
- **Flow context issues**: None beyond normal conditional-action behavior

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Invoice Number | Yes | ✅ | Present as leading column |
| Patient Name | Yes | ✅ | Present with patient record subtitle |
| Patient ID | Yes | ✅ | Present below patient name |
| Booking Reference | Yes | ✅ | Present as dedicated column |
| Invoice Date | Yes | ✅ | Present in full-table layout |
| Due Date | Yes | ✅ | Present in full-table layout |
| Total Amount | Yes | ✅ | Present in full-table layout |
| Amount Paid | Yes | ✅ | Present in full-table layout |
| Outstanding Balance | Yes | ✅ | Present as dedicated column |
| Currency | Yes | ✅ | Present as dedicated column |
| Payment Status | Yes | ✅ | Present with `Pending`, `Partial`, `Paid`, `Overdue`, `Refunded`, and `At Risk` examples |
| Payment Method | Yes | ✅ | Present as masked card/bank reference column |
| Installment Plan | No | ✅ | Present in full-table layout with progress and retry state |
| Actions | Yes | ✅ | Present in `Actions.jpg`; includes view, reminder, refund, download, and override actions |
| Send Reminder Confirmation Modal | Yes | ✅ | Present with invoice reference, balance, reminder type, delivery channel, and confirm/cancel CTAs |
| Override Status Modal | Yes | ✅ | Present with current status, new status selector, reason field, re-auth input, and disabled confirm state |

**Extra Elements**:

- Search box for patient name / ID, invoice, and booking reference
- Bulk CTA `Send Reminders (All Overdues)`
- CSV export action
- Section grouping for `At Risk`, `Overdue`, and `Others`

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 16/16 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|

#### Screen 4a: Patient Invoice Detail

**Layout**: `patient-billing/Patient Invoice Detail.jpg`, `patient-billing/Patient Invoice Detail - Having Refund.jpg`

##### Flow Context

- **User arrives from**: `View Details` action on the patient billing list
- **Screen purpose**: Provide a full audit trail for invoice header data, payment history, installment status, refunds, reminders, and manual overrides
- **Entry point**: Present through routed detail page with breadcrumb and explicit action buttons
- **Exit path**: Partial; breadcrumb path exists, but the explicit `Close` action required by the FR is not shown
- **Data continuity**: Strong; list identifiers carry through to invoice header, installment lines, refund history, reminder history, and override history
- **Flow context issues**: Required `At Risk` warning banner is not visible on the At Risk detail state

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Invoice Number | Yes | ✅ | Present in invoice header |
| Patient Name | Yes | ✅ | Present in invoice header |
| Patient ID | Yes | ✅ | Present in invoice header |
| Booking Reference | Yes | ✅ | Present in invoice header |
| Invoice Date | Yes | ✅ | Present in invoice header |
| Currency | Yes | ✅ | Present in invoice header |
| Total Amount | Yes | ✅ | Present in invoice header |
| Adjusted Total After Refund | Conditional | ✅ | Present in refund-applied variant and hidden/empty state in non-refund variant |
| Outstanding Balance | Yes | ✅ | Present in invoice header |
| Payment Status | Yes | ✅ | Present in invoice header |
| Discount Code Applied | Yes | ✅ | Present with `None — no discount applied` state |
| Payment History Table | Yes | ✅ | Present with payment type, dates, amount, method, payment intent, and status |
| Installment Schedule Table | Conditional | ✅ | Present with retry counts and next retry dates |
| Refund History Table | Conditional | ✅ | Present in refund-applied variant |
| Reminder History Table | Conditional | ✅ | Present |
| Status Override History Table | Conditional | ✅ | Present |
| Actions | Yes | ⚠️ | Detail actions shown for reminder, download, and override, but explicit `Close` action is not evidenced |
| At Risk Warning Banner | Yes | ❌ | At Risk invoice detail shows the badge only; the required prominent banner is not visible |

**Extra Elements**:

- Routed detail-page breadcrumb
- Top-right action cluster for `Download Invoice`, `Override Status`, and `Send Reminder`

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 16/18 (~89%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-02` / `U-19` The At Risk detail state lacks the required prominent warning banner, so the most urgent problem is not visually elevated above the routine invoice metadata | Add a high-visibility banner above the invoice header with the exact At Risk guidance from the FR |

#### Screen 4b: Refund Confirmation Modal

**Layout**: `patient-billing/Refund Confirmation.jpg`, `patient-billing/Refund Confirmation - Adjusted Refund Amount differs from Calculated Refund Amount.jpg`

##### Flow Context

- **User arrives from**: `Process Refund` action on Screen 4 or Screen 4a
- **Screen purpose**: Confirm refund calculations, require reason/re-authentication, and capture adjustment justification when the refund amount is changed
- **Entry point**: Present as modal over the invoice detail context
- **Exit path**: Present through close icon and cancel CTA
- **Data continuity**: Correct; modal carries invoice, patient, booking, treatment date, policy tier, refund amounts, and re-auth state from the parent invoice
- **Flow context issues**: No evidence of the required post-treatment / 0% refund disabled-confirm variant

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Invoice Number | Yes | ✅ | Present in modal summary block |
| Patient Name | Yes | ✅ | Present in modal summary block |
| Booking Reference | Yes | ✅ | Present in modal summary block |
| Treatment Date | Yes | ✅ | Present in modal summary block |
| Days Until/Since Treatment | Yes | ✅ | Present as `45 days` example |
| Cancellation Policy Applied | Yes | ✅ | Present with all three policy tiers and selected state |
| Original Invoice Amount | Yes | ✅ | Present |
| Calculated Refund Amount | Yes | ✅ | Present |
| Adjusted Refund Amount | Yes | ✅ | Present, including changed-value state |
| Final Refund Amount | Yes | ✅ | Present |
| Non-Refundable Amount | Yes | ✅ | Present as `Platform Fee (Non-Refundable)` |
| Reason | Yes | ✅ | Present as required textarea |
| Adjustment Justification | Conditional | ✅ | Present when adjusted amount differs from calculated amount |
| Re-authentication | Yes | ✅ | Present as secure input |
| Confirm Refund button | Yes | ✅ | Present with dynamic amount label |
| Cancel button | Yes | ✅ | Present |

**Extra Elements**:

- Plus/minus amount steppers on `Adjusted Refund Amount`
- Close icon in modal chrome

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 16/16 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|

**Flow Coverage Gaps**:

- No evidence of the required `0% refund — treatment has been completed` state with disabled confirm CTA
- Screen 4a does not show the required prominent At Risk banner
- Screen 4a does not evidence the explicit `Close` action described in the FR

---

### Flow F4: Discount Usage Tracking

**Status**: 🟢 COMPLETE — Read-only discount reconciliation layout covers the required columns, filter controls, and export/search utilities.
**Screens required**: 1
**Layout files**: `discount-usage/Discount Usage.jpg`, `discount-usage/Full Table.jpg`, `discount-usage/Filter.jpg`

#### Screen 5: Discount Usage Overview

**Layout**: `discount-usage/Discount Usage.jpg`, `discount-usage/Full Table.jpg`, `discount-usage/Filter.jpg`

##### Flow Context

- **User arrives from**: Admin navigation under `Billing & Finance -> Discount Usage`
- **Screen purpose**: Reconcile discount performance and cost allocation without exposing editing controls
- **Entry point**: Present through page title, breadcrumb, search, and filter controls
- **Exit path**: Present through table browsing and export; FR-019 deep-link is not explicitly shown in the sampled layouts
- **Data continuity**: Correct; rows combine code identity, campaign name, ownership type, cost split, revenue, date window, and status
- **Flow context issues**: None identified from the provided layouts

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Discount Code | Yes | ✅ | Present as leading column |
| Discount Name | Yes | ✅ | Present as campaign name column in full-table layout |
| Type | Yes | ✅ | Present as badge column (`Platform-Wide`, `Provider-Specific`, `Affiliate`) |
| Times Used | Yes | ✅ | Present in full-table layout |
| Total Discount Amount | Yes | ✅ | Present |
| Hairline Cost | Yes | ✅ | Present |
| Provider Cost | Conditional | ✅ | Present for provider-cost-sharing rows and blank/dash when not applicable |
| Revenue Generated | Yes | ✅ | Present |
| Active Window | Yes | ✅ | Present |
| Status | Yes | ✅ | Present with `Active`, `Expired`, and `Disabled` examples |

**Extra Elements**:

- Free-text search for discount code / campaign name
- Filter drawer for status, discount type, and active window
- Export CSV CTA

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 10/10 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|

**Flow Coverage Gaps**:

- None from the provided layouts

---

### Flow F5: Affiliate Billing & Commission Payouts

**Status**: 🟡 PARTIAL — The affiliate payout flow is broadly designed and operationally rich, but the primary screen is mislabeled as provider billing and the bulk-payout total is internally inconsistent between list and modal states.
**Screens required**: 1
**Layout files**: `aff-billing/Affiliate Billing - Pending Payouts.jpg`, `aff-billing/Affiliate Billing - Paid Payouts.jpg`, `aff-billing/Full Table - Pending Payouts.jpg`, `aff-billing/Full Table - Paid Payouts.jpg`, `aff-billing/Table - Pending Payouts.jpg`, `aff-billing/Table - Paid Payouts.jpg`, `aff-billing/Affiliate Billing - Affiliate Billing Details.jpg`, `aff-billing/Table - Referral Bookings Breakdown.jpg`, `aff-billing/Full Table - Referral Bookings Breakdown.jpg`, `aff-billing/Filter.jpg`, `aff-billing/Actions.jpg`, `aff-billing/Process Payout Confirmation Modal.jpg`, `aff-billing/Retry Payout Confirmation Modal.jpg`, `aff-billing/State A — Initial (before submitting).jpg`, `aff-billing/State B — Result Summary (after processing).jpg`

#### Screen 6: Affiliate Billing - Commission Payouts

**Layout**: `aff-billing/Affiliate Billing - Pending Payouts.jpg`, `aff-billing/Affiliate Billing - Paid Payouts.jpg`, `aff-billing/Full Table - Pending Payouts.jpg`, `aff-billing/Full Table - Paid Payouts.jpg`, `aff-billing/Affiliate Billing - Affiliate Billing Details.jpg`, `aff-billing/Process Payout Confirmation Modal.jpg`, `aff-billing/Retry Payout Confirmation Modal.jpg`, `aff-billing/State A — Initial (before submitting).jpg`, `aff-billing/State B — Result Summary (after processing).jpg`

##### Flow Context

- **User arrives from**: Admin navigation under `Billing & Finance -> Affiliate Billing`
- **Screen purpose**: Review monthly affiliate commissions, process single or bulk payouts, inspect failed states, and reconcile payout detail by referral booking
- **Entry point**: Present through breadcrumb and active left-nav item for affiliate billing
- **Exit path**: Present through row actions, payout detail page, process/retry modals, report download, and tab switch between pending and paid states
- **Data continuity**: Strong; list values carry through to detail, booking breakdown, process modal, retry modal, and batch result summary
- **Flow context issues**: The page title is rendered as `Provider Billing` across the list views even though the breadcrumb and left navigation correctly identify `Affiliate Billing`

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Select | Conditional | ✅ | Checkboxes shown for eligible pending rows and bulk toolbar state |
| Affiliate Name | Yes | ✅ | Present in pending/paid lists and detail page |
| Affiliate ID | Yes | ✅ | Present in pending/paid lists and detail page |
| Payout Reference | Yes | ✅ | Present in full paid table and detail page |
| Discount Code(s) | Yes | ✅ | Present in full paid table and referral breakdown |
| Payout Period | Yes | ✅ | Present in list, detail page, and all payout modals |
| Total Referrals | Yes | ✅ | Present in list and reflected in referral breakdown count |
| Total Referral Revenue | Yes | ✅ | Present in pending/paid tables |
| Commission Rate | Yes | ✅ | Present in list and referral breakdown |
| Commission Earned | Yes | ✅ | Present in list, detail page, and process/retry modals |
| Payment Status | Yes | ✅ | Present with `Pending`, `Processing`, `Paid`, and failed/retry states represented across layouts |
| Payout Readiness | Yes | ✅ | Present in detail page and retry context |
| Payment Date | Conditional | ✅ | Present in full paid table |
| Processed At | Conditional | ✅ | Present in full paid table |
| Payment Method | Yes | ✅ | Present in full paid table and process modal |
| Payment Destination | Conditional | ✅ | Present in full paid table, process modal, and retry modal |
| Stripe Transfer ID | Conditional | ✅ | Present in full paid table |
| Failure Reason | Conditional | ✅ | Present in retry modal and full paid table failed column |
| Processed By | Conditional | ✅ | Present in full paid table |
| Actions | Yes | ✅ | Present via kebab actions and top-level CTAs on the detail page |

**Extra Elements**:

- Required two-tab split between `Pending Payouts` and `Paid Payouts`
- Failed / Requires Retry section pinned inside the pending tab
- Bulk payout toolbar with selected count, selected total, process-all CTA, and clear-selection CTA
- Bulk result summary state after processing
- Referral booking breakdown table with booking reference, patient name, amount, commission rate, commission earned, currency, and referral code
- Download Report CTA

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 20/20 (100%)
**Critical Issues**:

- The bulk-payout toolbar shows `Selected total: $18,460.00`, but the confirmation modal summarizes `2 affiliates totalling £11,572.00`; this is a money-value mismatch on a transfer-confirmation step
- The main page title is `Provider Billing` instead of `Affiliate Billing`, which creates a scope/ownership conflict inside an adjacent provider-billing module

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-17` The batch-selection toolbar total does not match the amount shown in the confirmation modal | Keep selected-count and selected-total values synchronized between the parent list and the modal |
| ⚠️ UX Improvement | Affiliate payout views retain a `Provider Billing` page title even though the screen is clearly under affiliate billing | Rename the page title to `Affiliate Billing` across list and modal-entry states so operators do not confuse the two payout domains |

**Flow Coverage Gaps**:

- No direct evidence of an `Add Note` interaction even though the FR requires it for all statuses

---

### Flow F6: Transaction Search & Audit

**Status**: 🟡 PARTIAL — The unified investigation surface, no-results state, dispute workflow, and audit log table are designed, but the dispute modal mislabels the mandatory internal-note field and that weakens a key compliance control.
**Screens required**: 1
**Layout files**: `transaction-search/Transaction Search.jpg`, `transaction-search/Table - Transaction Search.jpg`, `transaction-search/Full Table - Transaction Search.jpg`, `transaction-search/Filter.jpg`, `transaction-search/Transaction Search - Dispute Resolution Panel.jpg`, `transaction-search/Audit Log.jpg`, `transaction-search/Table - Audit Log.jpg`, `transaction-search/Full Table - Audit Log.jpg`, `transaction-search/Transaction Search - No Results State.jpg`

#### Screen 7: Transaction Search & Audit Log

**Layout**: `transaction-search/Transaction Search.jpg`, `transaction-search/Full Table - Transaction Search.jpg`, `transaction-search/Transaction Search - Dispute Resolution Panel.jpg`, `transaction-search/Audit Log.jpg`, `transaction-search/Full Table - Audit Log.jpg`, `transaction-search/Transaction Search - No Results State.jpg`

##### Flow Context

- **User arrives from**: Admin navigation under `Billing & Finance -> Transaction Search & Audit Log`
- **Screen purpose**: Search across invoices, payouts, installments, refunds, and affiliate commissions, then resolve disputes or review immutable audit history
- **Entry point**: Present via breadcrumb, page title, dual-tab layout, and search/filter controls
- **Exit path**: Present through result links, dispute-resolution modal, tab switch, and clear-search path for empty states
- **Data continuity**: Strong; a booking-linked payout result carries into the dispute modal with booking reference, provider, expected payout, prior inclusion status, target cycle, and save action
- **Flow context issues**: The dispute modal labels the internal-note textarea as `Target Payout Cycle`, which can mislead admins during a required audit-writing step

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Search By | Yes | ✅ | Present with `Booking Reference` example |
| Search Input | Yes | ✅ | Present in normal and no-results states |
| Record Type | Yes | ✅ | Present as multi-select summary control |
| Date Range | Optional | ✅ | Present |
| Status | Optional | ✅ | Present |
| Record Type Result | Yes | ✅ | Present as colored badge column |
| Reference / ID | Yes | ✅ | Present as clickable link column |
| Booking Reference | Conditional | ✅ | Present as clickable link column |
| Patient / Provider / Affiliate | Yes | ✅ | Present in results list |
| Date | Yes | ✅ | Present |
| Amount | Yes | ✅ | Present |
| Currency | Yes | ✅ | Present |
| Status | Yes | ✅ | Present |
| Empty State Message | Conditional | ✅ | Present with exact search-term interpolation behavior |
| Audit Timestamp | Yes | ✅ | Present |
| Audit Admin | Yes | ✅ | Present |
| Action Type | Yes | ✅ | Present in full audit table |
| Affected Entity | Yes | ✅ | Present as clickable field in full audit table |
| Before Value | Yes | ✅ | Present in full audit table |
| After Value | Yes | ✅ | Present in full audit table |
| IP Address | Yes | ✅ | Present |
| Notes | Yes | ✅ | Present |
| Resolution Action | Conditional | ✅ | Present in dispute modal |
| Target Payout Cycle | Conditional | ✅ | Present in dispute modal |
| Internal Note | Conditional | ✅ | Present as textarea, but mislabeled |
| Notify Provider | Conditional | ✅ | Present and auto-selected/disabled in the shown `Add to Next Payout` state |
| Save Resolution | Conditional | ✅ | Present |

**Extra Elements**:

- Two-tab split between `Transaction Search` and `Audit Log`
- Filter entry point on both tabs
- Clear button on the main search form
- No-results state with recovery CTA

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 27/27 (100%)
**Critical Issues**:

- The dispute modal’s mandatory note textarea is labeled `Target Payout Cycle` instead of `Internal Note`, which can lead to incorrect operator input and ambiguous audit entries

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | The final textarea in the dispute modal repeats the `Target Payout Cycle` label instead of identifying itself as the required internal note | Rename the textarea label to `Internal Note` and keep the payout-cycle selector as a separate control immediately above it |

**Flow Coverage Gaps**:

- None beyond the mislabeled mandatory note field

---

### Flow F7: Currency Alert Response

**Status**: 🟢 COMPLETE — The alert modal includes the required header metrics, affected-booking table, and admin decision controls needed to document a response.
**Screens required**: 1
**Layout files**: `currency-alert/Currency Alert Detail Modal.jpg`, `currency-alert/Table - Affected Bookings.jpg`, `currency-alert/Full Table - Affected Bookings.jpg`

#### Screen 8: Currency Alert Detail Modal

**Layout**: `currency-alert/Currency Alert Detail Modal.jpg`, `currency-alert/Full Table - Affected Bookings.jpg`

##### Flow Context

- **User arrives from**: Currency alert notification or linked alert context
- **Screen purpose**: Review rate movement, inspect at-risk bookings, and log an explicit operator decision with rationale
- **Entry point**: Present as an overlaid modal with alert header context
- **Exit path**: Present through `Confirm Decision` and `Close`
- **Data continuity**: Correct; the alert header, bookings table, and admin decision section all operate on the same GBP/EUR fluctuation scenario
- **Flow context issues**: None that block the intended response flow

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Alert Title | Yes | ✅ | Present as `Currency Fluctuation Alert` |
| Currency Pair | Yes | ✅ | Present |
| Fluctuation | Yes | ✅ | Present and highlighted |
| Alert Threshold | Yes | ✅ | Present |
| Alert Generated | Yes | ✅ | Present |
| Booking Reference | Yes | ✅ | Present |
| Provider | Yes | ✅ | Present |
| Treatment Date | Yes | ✅ | Present in full affected-bookings table |
| Booking Amount | Yes | ✅ | Present in full affected-bookings table |
| Patient Currency | Yes | ✅ | Present in full affected-bookings table |
| Provider Currency | Yes | ✅ | Present in full affected-bookings table |
| Locked Rate | Yes | ✅ | Present |
| Current Rate | Yes | ✅ | Present |
| Rate Difference | Yes | ✅ | Present and highlighted in red |
| Estimated Exposure | Yes | ✅ | Present |
| Payout Date | Yes | ✅ | Present |
| Decision | Yes | ✅ | Present with all three radio options |
| Notes | Yes | ✅ | Present as textarea |
| Confirm Decision button | Yes | ✅ | Present |
| Close button | Yes | ✅ | Present |

**Extra Elements**:

- Paging controls on the affected-bookings table
- Right-aligned `Payout within 14 days` context label above the table

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 20/20 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| 💡 UX Suggestion | The bookings section is titled `Payment History`, which is less precise than the FR’s `Affected Bookings` framing | Rename the section header to `Affected Bookings` to better match the alert-review purpose |

**Flow Coverage Gaps**:

- None from the provided layouts

---

### Flow F8: Provider Earnings & Payout History

**Status**: 🟡 PARTIAL — Screen 9 is designed and aligned to the Stage 1 earnings-tracker spec, and Screen 10 now has a payout-detail design, but the higher-level payout-history list state is still not evidenced.
**Screens required**: 2
**Layout files**: `provider-earnings/Earnings Tracker.jpg`, `provider-earnings/Table - Earnings Tracker.jpg`, `provider-earnings/Full Table - Earnings Tracker.jpg`, `provider-earnings/Filter.jpg`, `payout-history/Treatment Breakdown.jpg`, `payout-history/Table - Treatment Breakdown.jpg`, `payout-history/Full Table - Treatment Breakdown.jpg`

#### Screen 9: Provider Earnings Tracker (Stage 1 — Treatment Income)

**Layout**: `provider-earnings/Earnings Tracker.jpg`, `provider-earnings/Full Table - Earnings Tracker.jpg`, `provider-earnings/Filter.jpg`

##### Flow Context

- **User arrives from**: Provider platform financial-management surface
- **Screen purpose**: Show per-treatment earnings awaiting payout with stage-1 payout visibility
- **Entry point**: Present through provider left navigation under `Financial Management -> Earnings Tracker`
- **Exit path**: Present through persistent left navigation and export/filter/search utilities
- **Data continuity**: Strong; list rows, payout-status states, summary bar, and refund-adjustment tooltip operate on the same earnings dataset
- **Flow context issues**: No detail drill-through is evidenced from booking references, even though the FR requires booking-reference links to the treatment case

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Booking Reference | Yes | ✅ | Present as leading column |
| Patient Name | Yes | ✅ | Present |
| Treatment Date | Yes | ✅ | Present |
| Treatment Type | Yes | ✅ | Present |
| Gross Amount | Yes | ✅ | Present |
| Commission | Yes | ✅ | Present with both percentage and flat-rate examples |
| Commission Deducted | Yes | ✅ | Present |
| Net Earning | Yes | ✅ | Present, including `£0.00` and negative deduction examples |
| Adjustment Marker | Conditional | ✅ | Present with `Partial Refund`, `Refunded`, and `Refunded — Deducted from Next Payout` examples |
| Currency | Yes | ✅ | Present |
| Treatment Status | Yes | ✅ | Present with `Completed` and `Aftercare` examples |
| Payout Status | Yes | ✅ | Present with `Pending Next Payout`, `Included in Payout — [Date]`, and `Payout Failed — [Date]` examples |
| Total Pending Earnings | Yes | ✅ | Present in summary bar |
| Next Payout Date | Yes | ✅ | Present in summary bar |
| Treatments This Period | Yes | ✅ | Present in summary bar |
| Filter by Treatment Status | Yes | ✅ | Present in filter drawer |
| Filter by Payout Status | Yes | ✅ | Present in filter drawer |
| Filter by Date Range | Yes | ✅ | Present in filter drawer |
| Export CSV | Yes | ✅ | Present as top-right CTA |

**Extra Elements**:

- Search box for booking reference and patient name
- Tooltip explanation for refund deduction carry-forward state

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 19/19 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | Booking references are displayed as plain text in the provided layouts; the FR specifies them as clickable links to the treatment case | Render booking references with an explicit linked state so providers can navigate from earnings rows to case details |

**Flow Coverage Gaps**:

- No evidence of the required sort controls for treatment date and net earning
- No evidence that the booking reference opens the treatment case detail as required

#### Screen 10: Provider Payout History (Stage 2 — Confirmed Payouts)

**Layout**: `payout-history/Treatment Breakdown.jpg`, `payout-history/Table - Treatment Breakdown.jpg`, `payout-history/Full Table - Treatment Breakdown.jpg`

##### Flow Context

- **User arrives from**: Provider platform confirmed-payout history surface
- **Screen purpose**: Show read-only payout history, payout-status states, invoice downloads, and per-payout treatment breakdown
- **Entry point**: Partially present; breadcrumb and left navigation confirm this state sits inside `Financial Management -> Payout History`, but the top-level payout-history list screen is not shown
- **Exit path**: Partial; navigation persists, but the parent list view is not evidenced
- **Data continuity**: Strong for the selected payout detail; failure banner, payout summary, treatment breakdown, and retry resolution history all operate on the same payout record
- **Flow context issues**: The delivered design covers a selected payout-detail state rather than the full payout-history list described in the FR

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Payout Reference | Yes | ✅ | Present in payout summary |
| Copy Reference | Yes | ✅ | Present as top-right CTA |
| Payout Date | Yes | ✅ | Present in payout summary |
| Transfer Confirmation Date | Conditional | ✅ | Present as `-` in the failed state |
| Payout Period | Yes | ✅ | Present in payout summary and failure banner |
| Treatment Count | Yes | ✅ | Present in payout summary |
| Gross Total | Yes | ✅ | Present |
| Commission Deducted | Yes | ✅ | Present |
| Net Payout | Yes | ✅ | Present |
| Payout Frequency | Yes | ✅ | Present as badge |
| Status | Yes | ✅ | Present as failed-state badge |
| Invoice | Conditional | ❌ | No invoice download control is evidenced in the provided payout-history detail layouts |
| Failure Reason | Conditional | ✅ | Present in the failed-state banner |
| Retry Resolution History | Conditional | ✅ | Present as timeline |
| Booking Reference | Yes | ✅ | Present in the treatment breakdown sub-table |
| Patient Name | Yes | ✅ | Present in full treatment-breakdown table |
| Treatment Date | Yes | ✅ | Present in full treatment-breakdown table |
| Treatment Type | Yes | ✅ | Present |
| Treatment Amount | Yes | ✅ | Present |
| Commission | Yes | ✅ | Present |
| Commission Deducted | Yes | ✅ | Present |
| Net Contribution | Yes | ✅ | Present |
| Currency | Yes | ✅ | Present |

**Extra Elements**:

- Export CTA is present, though labeled `Export CSV` rather than the FR wording `Export History`
- Failed-state provider guidance banner is prominently surfaced above the payout summary

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 22/23 (~96%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | The delivered Screen 10 layout opens on a payout-detail / treatment-breakdown state without evidencing the parent payout-history list that providers use to select a payout | Add the top-level payout-history list screen or clarify in the FR that this detail page is the primary entry surface |

**Flow Coverage Gaps**:

- No evidence of the parent payout-history list with multiple payout rows
- No evidence of filter controls for status/date range
- No evidence of sort controls for payout date or net payout amount
- No evidence of the `Invoice` download action in a paid-state variant

---

## Action Items

| Priority | Flow | Screen | Issue | Recommendation |
|----------|------|--------|-------|----------------|
| ⚠️ Important | F2 | Screen 2 | Batch approval count in the toolbar does not match the count shown in the confirmation modal | Synchronize selection count and totals across list and modal states |
| ⚠️ Important | F2 | Screen 3 | Payout detail is designed as a routed page instead of the FR-defined modal | Either redesign it as a modal/drawer or formally update the FR to approve a routed-detail pattern |
| ⚠️ Important | F3 | Screen 4a | Required `At Risk` warning banner is missing and the explicit `Close` action is not evidenced | Add the banner and the specified close control to the invoice detail state |
| ⚠️ Important | F5 | Screen 6 | Affiliate payout screen is mislabeled as `Provider Billing` and the bulk total is inconsistent between list and modal | Correct the page title and unify the transferred amount shown across states |
| ⚠️ Important | F6 | Screen 7 | The mandatory internal-note textarea is mislabeled as `Target Payout Cycle` in the dispute panel | Rename the textarea to `Internal Note` and preserve the existing target-cycle selector as a separate field |
| ⚠️ Important | F8 | Screen 9 | The earnings tracker does not evidence sortable controls for treatment date or net earning, and booking references do not appear as linked actions | Add visible sort affordances and ensure booking references open the treatment case |
| ⚠️ Important | F8 | Screen 10 | The new payout-history layouts cover the selected payout detail state, but the parent payout-history list, filters/sorting, and paid-state invoice action are still not evidenced | Add the top-level payout-history list and a paid-state variant with invoice download, filters, and sorting controls |
| 💡 UX Suggestion | F7 | Screen 8 | The affected-bookings section is titled `Payment History`, which blurs the alert context | Rename the section to `Affected Bookings` |

### Priority Legend

- **🔴 Critical**: Blocks flow progression, breaks data integrity, or causes security/legal risk. Must fix before development.
- **🔴 Critical UX**: Severe usability issue that would prevent users from completing the flow or cause significant confusion. Must fix before development.
- **⚠️ Important**: Functional discrepancy that could cause user confusion or require rework during development. Should fix before development.
- **⚠️ UX Improvement**: Usability or design quality issue that deviates from platform conventions or best practices. Should fix before development.
- **💡 Suggestion**: Cosmetic or minor improvement. Can fix anytime.
- **💡 UX Suggestion**: Minor design enhancement that would improve polish. Can fix anytime.

---

## Notes

- Requirement source: `local-docs/project-requirements/functional-requirements/fr017-admin-billing-finance/prd.md`
- Processing granularity fixed at flow-by-flow because the task scope covers the full FR
- Provider platform Screen 9 now maps to `layout-temp/provider-earnings/`; Screen 10 now maps to `layout-temp/payout-history/`, but only the payout-detail state is evidenced
