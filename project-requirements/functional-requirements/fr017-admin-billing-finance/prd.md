# FR-017 - Admin Billing & Financial Management

**Module**: A-05: Billing & Financial Reconciliation | PR-05: Financial Management & Reporting
**Feature Branch**: `fr017-admin-billing-finance`
**Created**: 2025-11-12
**Status**: Draft
**Source**: FR-017 from system-prd.md

---

## Executive Summary

The Admin Billing & Financial Management module provides Hairline administrators with comprehensive tools to manage the platform's financial operations across all stakeholders (patients, providers, and affiliates). This module centralizes transaction monitoring, provider payout processing, discount code management, multi-currency revenue reporting, and financial reconciliation across the three-tenant architecture.

This module serves as the financial control center for the platform, ensuring timely payments, accurate commission calculations, transparent billing, and complete audit trails for all financial transactions. It enables Hairline to scale its medical tourism operations while maintaining financial integrity and regulatory compliance.

**Key Capabilities**:

- View and manage all patient billing and payment transactions
- Process provider payouts with automated commission calculations
- Manage affiliate commission tracking and payments
- Create and track discount codes (platform-wide and provider-specific)
- Generate multi-currency financial reports and analytics
- Reconcile payments across multiple Stripe accounts
- Monitor outstanding balances and payment schedules
- Audit all financial transactions with complete traceability

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-03)**: Patients initiate payments through booking flow; invoices and receipts generated
- **Provider Platform (PR-05)**: Providers view upcoming payouts, earnings history, and commission structure
- **Admin Platform (A-05)**: Admins manage all financial operations, billing, and reconciliation
- **Shared Services (S-02)**: Payment Processing Service handles Stripe integration and transaction processing

### Multi-Tenant Breakdown

**Patient Platform (P-03: Booking & Payment)**:

- Patients make payments (deposit, installments, final payment) through integrated Stripe checkout
- Patients view invoice history and payment receipts
- Patients apply discount codes at checkout
- Payment data flows to admin platform for processing and reconciliation

**Provider Platform (PR-05: Financial Management & Reporting)**:

- Providers view upcoming payment schedule (weekly, bi-weekly, or monthly)
- Providers view payment history and earnings analytics
- Providers download invoices for completed payouts
- Providers view commission structure and breakdown per booking
- Providers cannot modify financial data (read-only view)

**Admin Platform (A-05: Billing & Financial Reconciliation)**:

- **Patient Billing**: View all patient invoices, payment status, process refunds, manage installment plans
- **Provider Billing**: View provider payment schedules, approve/process payouts, reconcile payments, generate invoices
- **Affiliate Billing**: View affiliate commissions, process monthly payouts, track referral revenue
- **Discount Management**: Create platform-wide and provider-specific discount codes, track usage and ROI
- **Financial Reporting**: Generate revenue analytics, commission breakdowns, outstanding balance reports
- **Stripe Account Management**: Configure multiple Stripe accounts per region/currency, manage currency conversion rates
- **Audit & Compliance**: Complete transaction logs, payment reconciliation, dispute resolution

**Shared Services (S-02: Payment Processing Service)**:

- Stripe API integration for payment processing (charges, refunds, transfers)
- Multi-currency payment support with locked exchange rates
- Installment payment scheduling and automated charging
- Commission calculation engine
- Payment retry logic for failed transactions
- Webhook handling for Stripe events (successful payments, failed charges, disputes)

### Communication Structure

**In Scope**:

- Email notifications for payment confirmations (patient, provider, admin)
- Email notifications for payout processing (provider, admin)
- Email notifications for failed payments and retry attempts
- Invoice generation and delivery via email (PDF attachments)
- Payment reminder emails for installment plans
- Admin internal notifications for outstanding payouts and failed reconciliations

**Out of Scope**:

- SMS notifications for payment events (handled by S-03: Notification Service if enabled; **no SMS payment notifications are available in MVP and will only be enabled in a future phase once S-03 SMS support is live**)
- In-app chat for payment disputes (handled by A-10: Communication Monitoring & Support)
- Provider-patient direct communication about payments (routed through admin support)

### Entry Points

**Admin Access**:

- Admin logs into Admin Platform → navigates to "Billing & Finance" section
- Dashboard displays: upcoming payouts, outstanding patient invoices, pending provider payments, affiliate commissions due

**Automated Triggers**:

- Treatment completion triggers provider payout eligibility calculation
- Scheduled cron jobs check for upcoming installment payments (daily at 3 AM UTC)
- Scheduled cron jobs generate monthly affiliate payout summaries (1st of each month)
- Stripe webhook events trigger real-time transaction status updates
- Failed payment events trigger admin alerts and retry mechanisms

**Provider Access**:

- Provider logs into Provider Platform → navigates to "Financial Management" section
- Providers view upcoming payouts based on configured schedule (weekly/bi-weekly/monthly)
- Providers download invoices after successful payouts

---

## Business Workflows

### Main Flow: Provider Payout Processing

**Actors**: Admin, Provider, System (Payment Processing Service), Stripe
**Trigger**: Admin navigates to "Provider Billing" → "Upcoming Payments" screen
**Outcome**: Provider receives payout; invoice generated; transaction logged

**Steps**:

1. Admin views "Upcoming Payments" list (filtered by payout schedule: weekly/bi-weekly/monthly)
2. System displays providers with earnings awaiting payout, grouped by scheduled payment date
3. Admin selects a provider from the list
4. System displays payout summary:
   - Total treatment revenue (sum of completed treatments since last payout)
   - Platform commission percentage (configured per provider)
   - Platform commission amount (revenue × commission %)
   - Provider net payout (revenue - commission)
   - Treatment breakdown (itemized list of bookings included in payout)
   - Bank account details (provider's registered payout account)
5. Admin reviews payout details and clicks "Approve Payout"
6. System prompts admin to confirm:
   - Payout amount: £X,XXX.XX
   - Destination: Provider Bank Account (last 4 digits shown)
   - Confirm: Yes / No
7. Admin clicks "Confirm"
8. System initiates Stripe transfer to provider's connected account
9. Stripe processes transfer (typically 1-2 business days)
10. System receives Stripe webhook confirming successful transfer
11. System updates payout status: "Pending" → "Paid"
12. System generates invoice PDF with itemized breakdown
13. System sends email notification to provider with invoice attachment
14. Provider receives payout in bank account within 1-2 business days
15. Admin sees confirmation message: "Payout processed successfully"
16. System logs transaction in audit trail (admin ID, timestamp, payout amount, provider ID)

### Alternative Flows

**A1: Admin Adds Note to Payout**:

- **Trigger**: Admin needs to document special payout circumstances (e.g., delayed payment due to bank issue)
- **Steps**:
  1. At step 5 (payout summary screen), admin clicks "Add Note" button
  2. System displays note entry modal: "Internal Note (not visible to provider)"
  3. Admin enters note text (max 500 characters): "Payment delayed due to provider bank maintenance window"
  4. Admin clicks "Save Note"
  5. System saves note and attaches to payout record
  6. Admin continues with payout approval (returns to step 6)
- **Outcome**: Note saved for internal reference; visible in payout history

**A2: Bulk Payout Processing (Multiple Providers)**:

- **Trigger**: Admin wants to process all weekly payouts at once (e.g., every Friday)
- **Steps**:
  1. At step 2 (upcoming payments list), admin clicks "Select All" checkbox
  2. System selects all providers with payouts due (batch selection)
  3. Admin clicks "Approve All Selected Payouts" button
  4. System displays batch confirmation modal with total payout amount across all providers
  5. Admin reviews summary and clicks "Confirm Batch"
  6. System processes payouts sequentially (steps 8-14 for each provider)
  7. System displays progress indicator: "Processing 15 of 47 payouts..."
  8. After all payouts processed, system displays summary:
     - Total payouts: 47
     - Successful: 45
     - Failed: 2 (with error details)
  9. Admin reviews failed payouts and retries individually
- **Outcome**: Batch payout processed; failed transactions flagged for manual review

**A3: Provider Payment Schedule Change**:

- **Trigger**: Provider requests to change payout frequency (e.g., weekly → monthly)
- **Steps**:
  1. Admin navigates to "Provider Management" → selects provider → "Financial Settings"
  2. Admin changes "Payment Schedule" dropdown: "Weekly" → "Monthly"
  3. System displays warning: "Changing schedule will delay next payout. Current outstanding balance: £X,XXX will be paid on [new schedule date]"
  4. Admin confirms change
  5. System updates provider payment schedule
  6. System recalculates next payout date based on new schedule
  7. System sends notification to provider: "Your payment schedule has been updated to monthly. Next payout: [date]"
- **Outcome**: Payment schedule updated; provider notified; next payout rescheduled

**B1: Payout Fails Due to Invalid Bank Account**:

- **Trigger**: Stripe returns error "Invalid bank account" during payout processing (step 8)
- **Steps**:
  1. System receives Stripe error webhook: "Transfer failed: Invalid bank account"
  2. System updates payout status: "Pending" → "Failed"
  3. System flags payout with error reason: "Bank account verification required"
  4. System sends admin notification: "Payout failed for [Provider Name]: Invalid bank account"
  5. Admin views failed payout in "Provider Billing" → "Failed Payments" tab
  6. Admin contacts provider via A-10: Communication Monitoring & Support
  7. Provider updates bank account details in PR-06: Profile & Settings Management
  8. Admin verifies new bank account details and retries payout
  9. System re-initiates payout with updated bank account
- **Outcome**: Payout retried after bank account correction; transaction logged as "retry attempt"

**B2: Provider Disputes Payout Amount**:

- **Trigger**: Provider claims missing booking revenue in payout calculation
- **Steps**:
  1. Provider contacts admin via support ticket: "Missing payment for booking #HP25110234"
  2. Admin opens dispute investigation in A-05: Billing & Financial Reconciliation
  3. Admin searches for booking #HP25110234 in transaction history
  4. System displays booking details:
     - Treatment date: 2025-10-15
     - Treatment amount: £2,500
     - Commission: £500 (20%)
     - Expected payout: £2,000
     - Status: "Completed" → "Aftercare"
  5. Admin checks payout history for provider during booking completion date range
  6. Admin discovers booking was NOT included in previous payout (status was "In Progress" at payout time)
  7. Admin manually adds booking to next scheduled payout with note: "Missed booking #HP25110234 - added retroactively"
  8. Admin notifies provider: "Booking included in next payout [date]"
  9. System logs dispute resolution in audit trail
- **Outcome**: Dispute resolved; missing booking added to next payout; provider notified

**B3: Currency Conversion Rate Protection Triggers Alert**:

- **Trigger**: System detects exchange rate fluctuation exceeding configured threshold
- **Steps**:
  1. System monitors currency conversion rates via external API (hourly checks)
  2. System detects GBP/TRY rate fluctuation: 5% increase in 24 hours (exceeds 3% threshold)
  3. System flags pending bookings with locked rates approaching payout
  4. System sends admin alert: "Currency fluctuation alert: GBP/TRY +5% in 24h. Review payouts for potential loss exposure."
  5. Admin reviews alert and checks affected bookings
  6. Admin reviews locked exchange rates vs. current rates
  7. Admin decides: Accept currency risk OR contact providers to renegotiate OR adjust commission structure
  8. Admin documents decision in financial notes
- **Outcome**: Admin alerted to currency risk; decision documented; potential loss mitigated

---

## Screen Specifications

### Screen 1: Provider Billing - Upcoming Payments List

**Purpose**: Display all providers with earnings awaiting payout, grouped by payment schedule

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Provider Name | text | Yes | Clinic/provider name | Display only |
| Provider ID | text | Yes | Unique provider identifier (e.g., "HP-PRV-00123") | Display only |
| Payment Schedule | select | Yes | Frequency: Weekly, Bi-Weekly, Monthly | Display only |
| Next Payment Date | date | Yes | Scheduled payout date | Format: DD-MM-YYYY |
| Outstanding Earnings | currency | Yes | Total revenue pending payout | Format: £X,XXX.XX |
| Commission (%) | number | Yes | Platform commission percentage | Range: 15-25% |
| Net Payout | currency | Yes | Provider payout after commission | Auto-calculated |
| Bank Account | text | Yes | Bank account last 4 digits (masked) | Display: ****1234 |
| Status | badge | Yes | "Pending Approval", "Processing", "Paid", "Failed" | Color-coded |
| Actions | buttons | Yes | "View Details", "Approve Payout", "Add Note" | Conditional visibility |

**Business Rules**:

- Providers appear in list ONLY if they have completed treatments since last payout
- Payout amount MUST include all treatments with status "Completed" or "Aftercare" (treatment delivered)
- Treatments with status "Scheduled", "In Progress", or "Cancelled" are NOT included in payout
- Providers with status "Suspended" or "Deactivated" do NOT appear in payout list
- Commission percentage is provider-specific (configured in A-02: Provider Management & Onboarding)
- Bank account details shown ONLY if provider has valid bank account on file
- "Approve Payout" button enabled ONLY if status is "Pending Approval"
- "Add Note" button available for all payouts (even after processing) for audit documentation

**Notes**:

- List should support filtering by: payment schedule (weekly/bi-weekly/monthly), date range, provider status
- List should support sorting by: next payment date, outstanding earnings (ascending/descending)
- Export to CSV functionality for batch processing and accounting reconciliation

---

### Screen 2: Provider Payout Detail Modal

**Purpose**: Display itemized breakdown of provider payout with treatment-level details

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Provider Name | text | Yes | Clinic name | Display only |
| Provider ID | text | Yes | Unique provider identifier | Display only |
| Payout Period | daterange | Yes | Date range covered by payout | Format: DD-MM-YYYY to DD-MM-YYYY |
| Bank Account | text | Yes | Destination bank account (masked) | Display: ****1234 |
| Payment Schedule | text | Yes | Configured schedule | Display: Weekly/Bi-Weekly/Monthly |
| Treatment List | table | Yes | Itemized list of included bookings | See sub-table below |
| Total Revenue | currency | Yes | Sum of treatment amounts | Auto-calculated |
| Commission Percentage | number | Yes | Platform commission rate | Display: X% |
| Commission Amount | currency | Yes | Commission deducted | Auto-calculated |
| Net Payout | currency | Yes | Provider receives this amount | Auto-calculated |
| Internal Notes | textarea | No | Admin notes (not visible to provider) | Max 500 characters |

**Treatment List Sub-Table** (nested within payout detail):

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Booking ID | text | Yes | Unique booking identifier (e.g., "HPID2511234") | Clickable link |
| Patient Name | text | Yes | Full patient name (revealed post-payment) | Display only |
| Treatment Date | date | Yes | Date treatment was performed | Format: DD-MM-YYYY |
| Treatment Type | text | Yes | FUE, FUT, DHI, etc. | Display only |
| Treatment Amount | currency | Yes | Total booking amount (inc. packages) | Display only |
| Currency | text | Yes | Original booking currency | Display: GBP, EUR, USD, etc. |
| Exchange Rate | number | No | Locked rate at booking time (if multi-currency) | Display: 1 GBP = 1.17 EUR |
| Status | badge | Yes | "Completed", "Aftercare" | Color-coded |

**Business Rules**:

- Payout MUST include ALL treatments with status "Completed" or "Aftercare" within the payout period
- Payout period determined by payment schedule:
  - **Weekly**: Last 7 days
  - **Bi-Weekly**: Last 14 days
  - **Monthly**: Last 30 days (or calendar month if configured)
- Commission percentage applied AFTER currency conversion (if applicable)
- Exchange rates locked at time of patient booking acceptance (no fluctuation risk to provider during payout)
- Internal notes visible ONLY to admins (never exposed to provider)
- "Approve Payout" button triggers Stripe transfer to provider connected account
- After approval, payout status changes to "Processing" → "Paid" (after Stripe confirmation webhook)

**Notes**:

- Clicking on "Booking ID" opens booking detail view in A-01: Patient Management & Oversight
- Provide "Download Detailed Report" button to export payout breakdown as PDF for provider records
- Highlight any bookings with special conditions (refunds, partial payments) with warning icon

---

### Screen 3: Patient Billing - Invoice Management

**Purpose**: Admin view of all patient invoices with filtering, search, and bulk actions

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Invoice Number | text | Yes | Unique invoice ID (e.g., "INV-2511-00456") | Clickable link |
| Patient Name | text | Yes | Full patient name | Searchable |
| Patient ID | text | Yes | Unique patient identifier (e.g., "HP-PAT-00789") | Clickable link |
| Booking ID | text | Yes | Associated booking identifier | Clickable link |
| Invoice Date | date | Yes | Date invoice generated | Format: DD-MM-YYYY |
| Due Date | date | Yes | Payment due date | Format: DD-MM-YYYY |
| Total Amount | currency | Yes | Total invoice amount | Display: £X,XXX.XX |
| Amount Paid | currency | Yes | Amount paid so far (for installment plans) | Display: £X,XXX.XX |
| Outstanding Balance | currency | Yes | Remaining amount due | Auto-calculated |
| Currency | text | Yes | Invoice currency | Display: GBP, EUR, USD, etc. |
| Payment Status | badge | Yes | "Pending", "Partial", "Paid", "Overdue", "Refunded" | Color-coded |
| Payment Method | text | Yes | Stripe payment method | Display: Card/Bank Transfer/etc. |
| Installment Plan | badge | No | If applicable: "2/5 installments paid" | Display format |
| Actions | buttons | Yes | "View Details", "Send Reminder", "Process Refund", "Download Invoice" | Conditional |

**Business Rules**:

- Invoice generated automatically when patient completes booking payment (deposit or full)
- Invoices with installment plans display: "X of Y installments paid"
- "Overdue" status triggered if outstanding balance remains 7 days after due date
- "Send Reminder" button available ONLY for invoices with status "Pending" or "Overdue"
- "Process Refund" button available ONLY for invoices with status "Paid" or "Partial"
- Refunds require admin approval and follow cancellation policy (FR-006: Booking & Scheduling)
- Clicking "Download Invoice" generates PDF with Hairline branding, itemized breakdown, and payment instructions

**Notes**:

- Implement advanced filtering: date range, payment status, currency, installment vs. full payment
- Support bulk actions: "Send reminders to all overdue invoices", "Export selected invoices to CSV"
- Display warning icon for installments with upcoming payment dates (within 7 days)

---

### Screen 4: Discount Management - Create Discount Code

**Purpose**: Allow admin to create platform-wide or provider-specific discount codes with approval workflow

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Discount Name | text | Yes | Internal name for discount (e.g., "Summer Sale 2025") | Max 100 characters |
| Discount Code | text | Conditional | Code patients enter at checkout (e.g., "SUMMER25") | Alphanumeric, max 20 chars, unique |
| Discount Type | select | Yes | "Platform-Wide", "Provider-Specific", "Affiliate" | Single selection |
| Affected Fees | select | Yes | "Hairline Only", "Both Fees" (Hairline + Provider) | Single selection |
| Discount Value Type | select | Yes | "Percentage", "Fixed Amount" | Single selection |
| Discount Value | number | Yes | Percentage (1-100) OR Fixed amount (e.g., £50) | Min: 1, Max: 100% or £10,000 |
| Currency | select | Conditional | If "Fixed Amount": GBP, EUR, USD, etc. | Required if fixed amount |
| Automatic Application | checkbox | Yes | If checked: auto-applied; If unchecked: requires code entry | Boolean |
| Valid From | date | Yes | Discount activation date | Format: DD-MM-YYYY |
| Valid Until | date | Yes | Discount expiration date | Must be > Valid From |
| Maximum Uses | number | No | Limit total uses (e.g., first 200 bookings) | Min: 1, Max: 100,000 |
| Applicable Providers | multiselect | Conditional | If "Provider-Specific": select providers | Searchable dropdown |
| Require Provider Approval | checkbox | Conditional | If "Both Fees": requires provider acceptance | Auto-checked if "Both Fees" |
| Status | badge | Yes | "Draft", "Active", "Expired", "Disabled" | Auto-managed |

**Business Rules**:

- **Discount Code** field required ONLY if "Automatic Application" is unchecked
- **Affected Fees**:
  - "Hairline Only": Discount deducted from Hairline commission (provider receives full amount)
  - "Both Fees": Discount split between Hairline and provider (requires provider approval)
- **Automatic Application**:
  - If checked: Discount applied automatically to all eligible bookings (no code entry needed)
  - If unchecked: Patients must enter discount code at checkout
- **Provider Approval Workflow** (if "Both Fees" selected):
  1. Admin creates discount code with status "Draft"
  2. System sends notification to applicable providers: "New discount proposed: [Name]. Review and approve."
  3. Providers review discount details in PR-06: Profile & Settings Management
  4. Providers can "Accept" or "Decline" participation
  5. Discount status changes to "Active" ONLY after ALL selected providers accept
  6. If ANY provider declines, discount status remains "Draft" (admin must revise or remove declined providers)
- **Maximum Uses**: If specified, discount auto-disables after reaching limit
- **Expiration**: Discount auto-expires after "Valid Until" date (status changes to "Expired")

**Notes**:

- Provide "Preview Discount" button to simulate discount application on sample booking
- Display warning if creating high-value discount (>50% or >£500) requiring secondary admin approval
- Support bulk provider selection for "Platform-Wide" discounts (e.g., "Select all providers in Turkey")

---

### Screen 5: Financial Reporting - Revenue Dashboard

**Purpose**: Executive overview of platform financial performance with filterable analytics

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Date Range Selector | daterange | Yes | Filter reports by date range | Default: Last 30 days |
| Currency Selector | select | Yes | View amounts in selected currency | Default: GBP |
| Total Revenue | currency (large) | Yes | Sum of all patient payments | Auto-calculated |
| Platform Commission | currency | Yes | Total Hairline commission earned | Auto-calculated |
| Provider Payouts | currency | Yes | Total paid to providers | Auto-calculated |
| Affiliate Payouts | currency | Yes | Total paid to affiliates | Auto-calculated |
| Outstanding Patient Invoices | currency | Yes | Pending patient payments | Auto-calculated |
| Pending Provider Payouts | currency | Yes | Provider earnings awaiting payout | Auto-calculated |
| Revenue by Country | chart | Yes | Geographic breakdown of patient bookings | Interactive pie/bar chart |
| Revenue by Treatment Type | chart | Yes | Breakdown by FUE, FUT, DHI, etc. | Interactive bar chart |
| Revenue Trend | chart | Yes | Line chart showing revenue over time | Interactive time series |
| Top Providers by Revenue | table | Yes | Highest-earning providers | Sortable table |
| Discount Usage | table | Yes | Most-used discount codes with ROI | Sortable table |
| Conversion Rate | percentage | Yes | (Bookings / Inquiries) × 100 | Display: X.X% |

**Business Rules**:

- All currency amounts displayed in selected currency (with real-time conversion if multi-currency)
- "Outstanding Patient Invoices" includes ONLY invoices with status "Pending", "Partial", or "Overdue"
- "Pending Provider Payouts" includes treatments with status "Completed" or "Aftercare" not yet paid
- Revenue by Country based on patient location (not provider location)
- Revenue by Treatment Type excludes refunded bookings
- Top Providers table sortable by: revenue, booking count, average booking value
- Discount Usage table shows: code name, times used, total discount amount, estimated ROI (bookings generated vs. discount cost)
- Charts interactive: clicking segment filters dashboard to that subset (e.g., click "Turkey" → filters to Turkey bookings)

**Notes**:

- Provide "Export Full Report" button to download PDF/CSV with all dashboard data
- Support comparison mode: "Compare to previous period" (e.g., last 30 days vs. previous 30 days)
- Display warning icons for anomalies: sudden revenue drop, high refund rate, unusual currency fluctuations

---

### Screen 6: Affiliate Billing - Commission Payouts

**Purpose**: Manage affiliate commission tracking and monthly payout processing

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Affiliate Name | text | Yes | Affiliate partner name (individual or company) | Display only |
| Affiliate ID | text | Yes | Unique affiliate identifier (e.g., "HP-AFF-00012") | Display only |
| Discount Code(s) | text | Yes | Assigned discount codes (comma-separated if multiple) | Display only |
| Payout Period | daterange | Yes | Date range for commission calculation | Format: DD-MM-YYYY to DD-MM-YYYY |
| Total Referrals | number | Yes | Number of bookings via affiliate code | Display only |
| Total Referral Revenue | currency | Yes | Sum of booking amounts from affiliate referrals | Auto-calculated |
| Commission Rate | number | Yes | Percentage or fixed amount per booking | Display: X% or £X |
| Commission Earned | currency | Yes | Total affiliate commission | Auto-calculated |
| Payment Status | badge | Yes | "Pending", "Processing", "Paid" | Color-coded |
| Payment Date | date | Conditional | Date payout processed (if paid) | Format: DD-MM-YYYY |
| Payment Method | text | Yes | Bank transfer, PayPal, etc. | Display only |
| Actions | buttons | Yes | "View Details", "Process Payout", "Download Report" | Conditional |

**Business Rules**:

- Affiliate payouts processed MONTHLY (default: 7th of each month for previous month's earnings)
- Commission calculated ONLY on completed bookings (status "Completed" or "Aftercare")
- Commission rate determined by affiliate agreement (configured during onboarding in A-07: Affiliate Program Management)
- Payouts with status "Pending" become eligible for processing on scheduled payout date
- "Process Payout" button enabled ONLY for payouts with status "Pending" and past due date
- Affiliates can track their own earnings via Affiliate Platform (read-only dashboard)
- Multiple discount codes per affiliate supported (e.g., influencer with seasonal codes)

**Notes**:

- Clicking "View Details" shows itemized list of referral bookings (similar to provider payout breakdown)
- "Download Report" generates PDF summary for affiliate records
- Support bulk payout processing for all affiliates due on same date

---

## Business Rules

### General Module Rules

- **Rule 1**: All financial transactions MUST be logged with timestamp, admin user ID, transaction amount, and affected parties (patient/provider/affiliate)
- **Rule 2**: All payment processing MUST use Stripe API (PCI-DSS compliant); NO direct credit card storage
- **Rule 3**: Currency exchange rates locked at time of patient booking acceptance; NO rate changes during payout cycle
- **Rule 4**: Provider payouts processed ONLY after treatment status changes to "Completed" or "Aftercare"
- **Rule 5**: Installment payments MUST complete 30 days before scheduled treatment date (FR-007B: Split Payment / Installment Plans)
- **Rule 6**: Refunds follow graduated cancellation policy (FR-006: Booking & Scheduling): >30 days = 90%, 15-30 days = 50%, <15 days = 0%
- **Rule 7**: All discount codes MUST have expiration dates; no perpetual discounts
- **Rule 8**: Platform-wide discounts affecting "Both Fees" REQUIRE provider approval before activation
- **Rule 9**: Affiliate commissions calculated ONLY on net revenue (after discounts and refunds)
- **Rule 10**: Multi-currency bookings display amounts in patient's selected currency; providers receive payouts in their configured currency

### Data & Privacy Rules

- **Privacy Rule 1**: Patient full names and contact details visible in financial records ONLY after booking payment confirmation
- **Privacy Rule 2**: Provider bank account details masked in UI (show last 4 digits only); full details stored encrypted at rest
- **Privacy Rule 3**: Financial transaction logs MUST include masked payment method (e.g., "Visa ending in 1234") NOT full card numbers
- **Audit Rule**: All admin actions in financial module MUST be logged with admin ID, timestamp, action type, and affected records
- **Data Retention**: Financial transaction records MUST be retained for minimum 7 years (healthcare and tax compliance)
- **GDPR/Compliance**: Patient data deletion requests MUST result in PII anonymization while preserving financial records for audit (replace name with "Patient #ID")

### Admin Editability Rules

**Editable by Admin**:

- Provider payment schedule (weekly, bi-weekly, monthly)
- Provider commission percentage (within range: 15-25%)
- Discount code creation, activation, deactivation, expiration dates
- Discount maximum usage limits
- Currency conversion markup percentage (default: 5%, range: 0-10%)
- Payment reminder schedule (default: 3 days before installment due, 7 days if overdue)
- Payout approval and processing (manual trigger)
- Internal notes on payouts and invoices (admin-only visibility)
- Refund initiation and approval (subject to cancellation policy)

**Fixed in Codebase (Not Editable)**:

- Platform commission range boundaries (15-25% enforced by business logic)
- Installment cutoff date (30 days before treatment - hardcoded business rule)
- Currency exchange API source (xe.com or equivalent configured in environment variables)
- Stripe account connection parameters (API keys managed via secrets vault)
- Invoice PDF template structure (branding and layout fixed)
- Audit log retention period (7 years - compliance requirement)
- Payment retry logic (3 attempts with exponential backoff - hardcoded)

**Configurable with Restrictions**:

- Admin can manually adjust payout amounts ONLY with documented justification (audit trail required)
- Admin can override discount approval ONLY for "Hairline Only" discounts (cannot force provider participation)
- Admin can process emergency refunds ONLY with secondary admin approval (2-person authorization)

### Payment & Billing Rules

- **Payment Rule 1**: Patient deposits (20-30% of total) REQUIRED for booking confirmation; held until treatment completion
- **Payment Rule 2**: Final payment due 7 days before treatment date OR last installment 30 days before treatment (whichever is configured)
- **Payment Rule 3**: Failed installment payments trigger 3 automatic retry attempts (day 1, day 3, day 7); if all fail, booking flagged for admin review
- **Billing Rule 1**: Invoices generated immediately upon successful payment (deposit, installment, or final)
- **Billing Rule 2**: Provider invoices generated after payout processing (itemized breakdown with treatment details)
- **Billing Rule 3**: Affiliate invoices generated monthly (1st of each month for previous month's commissions)
- **Currency Rule 1**: Patients charged in their selected currency; providers paid in their configured currency; Hairline absorbs currency conversion costs
- **Currency Rule 2**: Exchange rates locked at booking acceptance; NO fluctuation risk to patient or provider during booking lifecycle
- **Commission Rule 1**: Platform commission calculated AFTER discount application and BEFORE provider payout
- **Commission Rule 2**: Affiliate commissions deducted from Hairline's commission (does not reduce provider payout)

---

## Success Criteria

### Patient Experience Metrics

- **SC-001**: Patients receive invoice within 30 seconds of successful payment completion
- **SC-002**: 95% of installment payments processed automatically without manual intervention
- **SC-003**: Patients receive payment reminder 3 days before installment due date for 100% of installment plans
- **SC-004**: Refund processing completes within 5-7 business days for 90% of refund requests

### Provider Efficiency Metrics

- **SC-005**: Providers receive payout within 2 business days of admin approval for 95% of payouts
- **SC-006**: Provider payout summaries include itemized treatment breakdown for 100% of payouts
- **SC-007**: Providers can download invoice PDFs immediately after payout completion for self-service accounting

### Admin Management Metrics

- **SC-008**: Admins can process provider payouts in under 2 minutes per provider (single payout)
- **SC-009**: Admins can process bulk payouts (50+ providers) in under 15 minutes
- **SC-010**: 100% of financial transactions logged with complete audit trail (admin ID, timestamp, action, affected records)
- **SC-011**: Financial dashboard loads within 3 seconds for date ranges up to 1 year
- **SC-012**: Discount code approval workflow completes within 24 hours for 80% of provider responses
- **SC-013**: Outstanding invoice identification and follow-up reduces overdue invoices by 60%

### System Performance Metrics

- **SC-014**: Payment processing API response time <2 seconds for 95% of transactions
- **SC-015**: Installment payment scheduling accuracy: 99.9% (installments charged on correct dates)
- **SC-016**: Failed payment retry mechanism success rate: 70% (failed payments recovered within 3 attempts)
- **SC-017**: Currency conversion rate updates occur hourly with <5 minute staleness
- **SC-018**: Financial report generation completes within 10 seconds for reports covering 90 days of data
- **SC-019**: System supports 500+ concurrent admin users managing financial operations without performance degradation

### Business Impact Metrics

- **SC-020**: Discount code usage increases booking conversion rate by 25%
- **SC-021**: Installment payment plans increase booking completion rate by 40% (compared to full upfront payment)
- **SC-022**: Automated payout processing reduces admin workload by 70% (compared to manual bank transfers)
- **SC-023**: Financial reporting provides real-time insights enabling revenue optimization decisions within 24 hours
- **SC-024**: Affiliate program generates 15% of total platform bookings within 6 months of launch
- **SC-025**: Platform commission revenue tracking accuracy: 99.5% (discrepancies <0.5% of total revenue)

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **FR-001 / Module P-01: Auth & Profile Management**
  - **Why needed**: Patient account required for billing; payment methods linked to patient profiles
  - **Integration point**: Patient billing records linked to patient accounts; invoices accessible via patient dashboard

- **FR-003 / Module P-02: Quote Request & Management**
  - **Why needed**: Quote acceptance triggers initial invoice generation
  - **Integration point**: Quote acceptance locks pricing and exchange rates used for all billing calculations

- **FR-004 / Module PR-02: Inquiry & Quote Management**
  - **Why needed**: Provider quote submission determines treatment pricing and packages included in billing
  - **Integration point**: Quote data flows to booking confirmation; itemized breakdown appears in invoices

- **FR-005 / Module P-03: Booking & Payment**
  - **Why needed**: Patient payment processing initiates all billing workflows
  - **Integration point**: Stripe payment intents created via P-03 trigger invoice generation and payout eligibility tracking in A-05

- **FR-007 / Module S-02: Payment Processing Service**
  - **Why needed**: All payment transactions processed via Stripe integration
  - **Integration point**: S-02 handles Stripe API calls, webhook processing, and payment retry logic; A-05 consumes transaction events

- **FR-010 / Module PR-03: Treatment Execution & Documentation**
  - **Why needed**: Treatment completion status triggers provider payout eligibility
  - **Integration point**: Status change "In Progress" → "Aftercare" signals completed treatment; triggers payout calculation in A-05

- **FR-015 / Module A-02: Provider Management & Onboarding**
  - **Why needed**: Provider bank account details and commission structure configured during onboarding
  - **Integration point**: A-02 stores bank account and commission percentage; A-05 retrieves for payout processing

- **FR-019 / Module A-06: Discount & Promotion Management**
  - **Why needed**: Discount codes created in A-06 affect invoice amounts and commission calculations
  - **Integration point**: A-06 manages discount code creation and approval; A-05 tracks discount usage and financial impact

- **FR-020 / Module S-03: Notification Service**
  - **Why needed**: Email notifications for payment confirmations, payout notifications, payment reminders
  - **Integration point**: A-05 triggers notification events (payment success, payout processed, installment due); S-03 sends emails

### External Dependencies (APIs, Services)

- **External Service 1: Stripe Payment API**
  - **Purpose**: Process credit card payments, bank transfers, refunds; manage connected accounts for provider payouts
  - **Integration**: RESTful API calls for payment intents, transfers, refunds; webhooks for real-time event notifications
  - **Failure handling**: Retry failed transactions with exponential backoff (1 hour, 6 hours, 24 hours); flag for manual review after 3 failures

- **External Service 2: Currency Exchange API (xe.com or equivalent)**
  - **Purpose**: Fetch real-time currency conversion rates for multi-currency bookings and payouts
  - **Integration**: RESTful API calls (hourly) to retrieve exchange rates; cache rates for 1 hour
  - **Failure handling**: If API unavailable, use last cached rate; flag admin if cache >24 hours stale

- **External Service 3: PDF Generation Library (e.g., wkhtmltopdf, LaTeX, or SaaS like PDFShift)**
  - **Purpose**: Generate invoice PDFs with Hairline branding and itemized breakdowns
  - **Integration**: Server-side PDF rendering from HTML templates
  - **Failure handling**: If PDF generation fails, provide HTML invoice via email; retry PDF generation asynchronously

### Data Dependencies

- **Entity 1: Booking Records (from P-03: Booking & Payment)**
  - **Why needed**: Invoices link to bookings; payout calculations aggregate completed bookings
  - **Source**: Booking module creates booking records upon quote acceptance; financial module consumes booking data

- **Entity 2: Treatment Completion Status (from PR-03: Treatment Execution & Documentation)**
  - **Why needed**: Provider payouts released ONLY after treatment marked "Completed" or "Aftercare"
  - **Source**: Provider platform updates treatment status; financial module monitors status changes

- **Entity 3: Provider Commission Structure (from A-02: Provider Management & Onboarding)**
  - **Why needed**: Commission percentage determines platform revenue and provider payout split
  - **Source**: Configured during provider onboarding; stored in provider profile

- **Entity 4: Discount Code Data (from A-06: Discount & Promotion Management)**
  - **Why needed**: Discount codes affect invoice amounts, commission calculations, and affiliate attribution
  - **Source**: Discount codes created in A-06; applied at checkout; tracked in A-05 for financial reporting

- **Entity 5: Payment Method Tokens (from Stripe)**
  - **Why needed**: Installment payments require stored payment methods for recurring charges
  - **Source**: Payment methods tokenized during initial payment; tokens stored in Stripe (not in Hairline database)

---

## Assumptions

### User Behavior Assumptions

- **Assumption 1**: Admins process provider payouts manually on scheduled dates (weekly/bi-weekly/monthly); no fully automated payout system required for MVP
- **Assumption 2**: Providers check payment status weekly via provider platform; no daily monitoring expected
- **Assumption 3**: Patients review invoices primarily via email (PDF attachments); in-app invoice access is secondary
- **Assumption 4**: Affiliates accept monthly payout schedule; no demand for more frequent payouts

### Technology Assumptions

- **Assumption 1**: Stripe API availability: 99.9% uptime; rare outages handled via retry mechanisms
- **Assumption 2**: Currency exchange API updates hourly; rates stable enough for 1-hour caching without significant risk
- **Assumption 3**: Admin platform accessed via modern browsers (Chrome, Firefox, Safari, Edge - latest 2 versions); no IE11 support
- **Assumption 4**: PDF generation completes within 10 seconds for invoices with <50 line items
- **Assumption 5**: Financial reports covering 12 months of data can be generated within 30 seconds (database optimized with indexes)

### Business Process Assumptions

- **Assumption 1**: Provider bank account verification completed during onboarding (A-02); no re-verification required for each payout
- **Assumption 2**: Discount code approval workflow (providers review and accept/decline) completes within 48 hours; no urgent same-day discounts
- **Assumption 3**: Affiliate commission rates remain constant for 12-month contract periods; no mid-cycle rate changes
- **Assumption 4**: Refund requests reviewed manually by admin; no automated refund approvals (fraud prevention)
- **Assumption 5**: Currency conversion costs absorbed by platform; no pass-through to patients or providers
- **Assumption 6**: Payment disputes rare (<1% of transactions); manual resolution acceptable for MVP
- **Assumption 7**: Financial audit requirements met via database transaction logs; no separate audit trail system required initially

---

## Implementation Notes

### Technical Considerations

- **Architecture**: Financial module requires high data integrity; use database transactions (BEGIN/COMMIT/ROLLBACK) for all payment processing
- **Concurrency**: Prevent race conditions in payout processing; use row-level locking when calculating provider earnings
- **Idempotency**: All Stripe API calls MUST be idempotent (unique idempotency keys per transaction to prevent duplicate charges/transfers)
- **Async Processing**: Use job queues (Redis Queue, AWS SQS) for background tasks: invoice PDF generation, payment retries, payout processing
- **Caching**: Cache currency exchange rates for 1 hour; cache financial dashboard data for 5 minutes (balance between freshness and performance)
- **Error Handling**: Implement comprehensive error logging for Stripe API failures; categorize errors (retryable vs. permanent) for appropriate handling
- **Decimal Precision**: Use DECIMAL(19,4) for currency amounts to prevent floating-point rounding errors (critical for financial calculations)

### Integration Points

- **Integration 1: Stripe Payment Intents API**
  - **Data format**: JSON payload with payment method ID, amount, currency, customer ID
  - **Authentication**: Stripe secret API key (stored in secrets vault, never in code)
  - **Error handling**: Retry on 5xx errors; log 4xx errors for manual review; implement webhook signature verification

- **Integration 2: Stripe Transfers API (Provider Payouts)**
  - **Data format**: JSON payload with destination (provider connected account ID), amount, currency, metadata (booking IDs)
  - **Authentication**: Stripe secret API key with `transfer_funds` permission
  - **Error handling**: Retry failed transfers up to 3 times; flag for manual review if all retries fail

- **Integration 3: Stripe Webhooks (Real-Time Event Processing)**
  - **Events subscribed**: `payment_intent.succeeded`, `payment_intent.failed`, `transfer.created`, `transfer.failed`, `charge.refunded`
  - **Authentication**: Verify webhook signatures using Stripe webhook secret
  - **Error handling**: Return 200 OK immediately; process events asynchronously; retry failed webhook processing

- **Integration 4: Currency Exchange API**
  - **Data format**: JSON response with exchange rates for supported currency pairs
  - **Authentication**: API key (if required)
  - **Error handling**: Use cached rates if API unavailable; alert admin if cache >24 hours stale

- **Integration 5: Admin Dashboard to Provider Dashboard (Read-Only Access)**
  - **Data format**: Provider platform queries shared database for payout history (read-only views)
  - **Authentication**: Provider session tokens validated against shared auth service
  - **Error handling**: Graceful degradation if admin database temporarily unavailable; display cached data with staleness warning

### Scalability Considerations

- **Current scale**: Expected 500 bookings per month at launch; 50 providers; 10 affiliates
- **Growth projection**: 5,000 bookings per month within 12 months; 500 providers; 100 affiliates
- **Peak load**: End-of-month provider payouts (500 payouts processed within 4-hour window)
- **Data volume**: 60,000 invoices per year; 6,000 provider payout records per year
- **Scaling strategy**:
  - Horizontal scaling: Add API servers behind load balancer for admin platform
  - Database optimization: Partition financial transaction tables by year; index on frequently queried columns (booking_id, provider_id, payment_date)
  - Batch processing: Process provider payouts in batches of 50 to prevent API rate limiting
  - Caching: Implement Redis caching for financial dashboard queries (5-minute TTL)

### Security Considerations

- **Authentication**: Require admin multi-factor authentication (MFA) for all financial operations (payouts, refunds)
- **Authorization**: Role-based access control (RBAC) with granular permissions:
  - **Billing Admin**: Full access (view, approve payouts, process refunds)
  - **Billing Viewer**: Read-only access (cannot approve payouts or refunds)
  - **Super Admin**: Full access with secondary approval capability for high-value transactions (>£10,000)
- **Encryption**: Encrypt provider bank account details at rest using AES-256; decrypt only during payout processing
- **Audit trail**: Log ALL financial actions with admin ID, timestamp, IP address, action type, before/after values
- **Fraud prevention**:
  - Flag sudden high-value discount codes for review (>50% off or >£500)
  - Flag provider payouts exceeding 2x average payout amount for manual review
  - Implement rate limiting on refund API endpoints (max 10 refunds per admin per hour)
- **PCI-DSS Compliance**: NO credit card data stored in Hairline database; all payment data handled by Stripe (PCI-compliant processor)
- **Data retention**: Financial records retained for 7 years (compliance requirement); soft-delete only (no hard deletes)
- **Sensitive data masking**: Mask payment methods in UI (show "Visa ending in 1234" not full card number)

---

## User Scenarios & Testing

### User Story 1 - Weekly Provider Payout Processing (Priority: P1)

An admin processes weekly provider payouts every Friday for providers who have completed treatments in the past 7 days, ensuring timely payments and accurate commission calculations.

**Why this priority**: Core financial operation; providers depend on regular payouts for cash flow; delays damage provider relationships and platform reputation.

**Independent Test**: Can be fully tested by creating completed bookings for multiple providers, navigating to "Provider Billing" → "Upcoming Payments", selecting providers, and processing payouts. Verify Stripe transfer initiated, provider notified, and invoice generated.

**Acceptance Scenarios**:

1. **Given** admin is logged into Admin Platform AND navigates to "Provider Billing" → "Upcoming Payments"
   **When** admin filters by "Payment Schedule: Weekly" AND views list of providers with earnings
   **Then** system displays all providers with completed treatments in past 7 days, showing: provider name, outstanding earnings, commission %, net payout, bank account last 4 digits

2. **Given** admin selects a provider from "Upcoming Payments" list AND clicks "View Details"
   **When** payout detail modal opens
   **Then** system displays itemized breakdown: treatment list (booking IDs, patient names, treatment dates, amounts), total revenue, commission amount, net payout, bank account details

3. **Given** admin reviews payout details AND clicks "Approve Payout" AND confirms payout amount
   **When** system initiates Stripe transfer
   **Then** payout status changes to "Processing", Stripe transfer API call succeeds, admin sees confirmation message "Payout processed successfully"

4. **Given** Stripe transfer completes successfully (webhook received)
   **When** system processes webhook event
   **Then** payout status updates to "Paid", invoice PDF generated, email sent to provider with invoice attachment, transaction logged in audit trail

5. **Given** multiple providers (10+) have payouts due on same date
   **When** admin uses "Select All" AND clicks "Approve All Selected Payouts"
   **Then** system processes payouts in batch, displays progress indicator, completes all successful payouts within 5 minutes, flags any failures for manual review

---

### User Story 2 - Patient Installment Payment Management (Priority: P1)

Patients book treatments with split payment plans (2-9 monthly installments), and the system automatically charges installments on schedule, sends reminders, and handles failed payments.

**Why this priority**: Installment plans increase booking conversion by 40%; critical for affordability and patient acquisition; automated processing reduces admin workload.

**Independent Test**: Create booking with 5-month installment plan, advance system date to trigger installment charges, verify automatic charging, reminders sent, and failed payment retries.

**Acceptance Scenarios**:

1. **Given** patient accepts quote AND selects "Split Payment: 5 months" at checkout
   **When** patient completes first installment payment
   **Then** system calculates remaining 4 installments (equal amounts), schedules charges for days 30, 60, 90, 120, generates invoice with installment schedule, confirms booking

2. **Given** installment payment due in 3 days
   **When** scheduled reminder job runs daily at 9 AM
   **Then** system sends email reminder to patient: "Your next payment of £XXX is due on [date]. Your card ending in 1234 will be charged automatically."

3. **Given** installment payment due date arrives
   **When** scheduled charge job runs at 12 AM (midnight)
   **Then** system charges patient's stored payment method via Stripe, generates receipt, sends confirmation email, updates invoice "2 of 5 installments paid"

4. **Given** installment payment fails (insufficient funds)
   **When** Stripe webhook notifies payment failure
   **Then** system logs failure, schedules retry attempt #1 (in 24 hours), sends email to patient: "Payment failed. We'll retry in 24 hours. Please ensure sufficient funds."

5. **Given** all 3 retry attempts fail
   **When** final retry fails
   **Then** system flags booking as "Payment Failed", sends admin alert, sends email to patient: "Payment unsuccessful after 3 attempts. Please update payment method or contact support.", booking moves to "At Risk" status

---

### User Story 3 - Discount Code Creation with Provider Approval (Priority: P2)

An admin creates a platform-wide discount code for a marketing campaign, requiring provider approval before activation, and tracks usage and ROI.

**Why this priority**: Discount codes drive marketing campaigns and seasonal promotions; provider approval ensures buy-in and prevents unilateral margin reduction.

**Independent Test**: Admin creates discount code with "Both Fees" option, providers receive approval request, accept/decline, discount activates, patients apply code at checkout, admin tracks usage.

**Acceptance Scenarios**:

1. **Given** admin navigates to "Discount Management" → "Create Discount Code"
   **When** admin fills form: Name "Summer Sale", Code "SUMMER25", Type "Platform-Wide", Affected Fees "Both Fees", Value "15%", Valid From "2025-06-01", Valid Until "2025-08-31", Maximum Uses "500"
   **Then** system creates discount with status "Draft", sends notification to all active providers: "New discount proposed: Summer Sale. Review and approve by [date]."

2. **Given** provider receives discount approval notification
   **When** provider logs into Provider Platform → navigates to "Settings" → "Discount Approvals"
   **Then** provider sees discount details (name, code, discount amount, date range, impact on earnings), options: "Accept" or "Decline"

3. **Given** provider clicks "Accept"
   **When** system records provider approval
   **Then** provider added to "Approved Providers" list, if ALL providers approve, discount status changes to "Active", admin notified "Discount SUMMER25 is now active"

4. **Given** discount status is "Active" AND patient submits booking
   **When** patient enters discount code "SUMMER25" at checkout
   **Then** system validates code (not expired, usage < max), applies 15% discount to total amount, displays: "Discount applied: £XXX saved", updates invoice with discount line item

5. **Given** discount has been used 50 times
   **When** admin views "Discount Management" → "Active Discounts" → clicks "SUMMER25"
   **Then** system displays usage stats: times used (50), total discount amount (£X,XXX), bookings generated (50), estimated ROI (revenue gained vs. discount cost)

---

### User Story 4 - Multi-Currency Booking with Locked Exchange Rates (Priority: P1)

A patient from the UK books a treatment in Turkey, pays in GBP, while the provider receives payout in EUR, with exchange rates locked at booking time to protect both parties from currency fluctuations.

**Why this priority**: Multi-currency support essential for international medical tourism platform; locked rates prevent disputes and financial losses from rate fluctuations.

**Independent Test**: Create booking with patient currency GBP and provider currency EUR, verify exchange rate locked at booking, advance time, verify payout uses locked rate regardless of current market rate.

**Acceptance Scenarios**:

1. **Given** patient (UK) accepts quote from provider (Turkey) with treatment price £2,000 GBP
   **When** patient confirms booking and completes payment
   **Then** system locks exchange rate at booking time (e.g., 1 GBP = 1.17 EUR), stores locked rate in booking record, displays on invoice: "Exchange rate locked: 1 GBP = 1.17 EUR"

2. **Given** booking completed and treatment marked "Aftercare" (ready for payout)
   **When** admin processes provider payout (2 weeks after booking)
   **Then** system uses LOCKED exchange rate (1 GBP = 1.17 EUR) for payout calculation, provider receives £2,000 × 1.17 = €2,340 (minus commission), NOT current market rate

3. **Given** current market exchange rate has changed (1 GBP = 1.22 EUR) after booking
   **When** admin views payout detail modal
   **Then** system displays: "Booking Amount: £2,000 GBP", "Exchange Rate (Locked): 1.17 EUR", "Provider Payout: €2,340 EUR", "Note: Exchange rate locked at booking time"

4. **Given** provider views payout history in Provider Platform
   **When** provider clicks on payout record
   **Then** provider sees itemized breakdown with locked exchange rate details, confirming payout amount matches booking expectations

---

### User Story 5 - Financial Dashboard for Executive Reporting (Priority: P2)

Hairline executives and finance team view real-time financial dashboard to monitor platform revenue, provider payouts, outstanding invoices, and key metrics for business decision-making.

**Why this priority**: Executive visibility into financial health critical for strategic planning; real-time data enables rapid response to revenue trends.

**Independent Test**: Generate test data (100 bookings, 20 providers, 5 affiliates) across 90 days, navigate to financial dashboard, verify all charts and metrics display correctly, test filtering by date range and currency.

**Acceptance Scenarios**:

1. **Given** admin navigates to "Financial Reporting" → "Revenue Dashboard"
   **When** dashboard loads with default date range (last 30 days)
   **Then** system displays: Total Revenue (£XXX,XXX), Platform Commission (£XX,XXX), Provider Payouts (£XX,XXX), Outstanding Patient Invoices (£X,XXX), Pending Provider Payouts (£XX,XXX)

2. **Given** admin changes date range to "Last 90 days" AND currency to "EUR"
   **When** system recalculates metrics
   **Then** all currency amounts converted to EUR, charts update to show 90-day data, dashboard loads within 3 seconds

3. **Given** admin views "Revenue by Country" pie chart
   **When** admin clicks on "Turkey" segment (40% of revenue)
   **Then** dashboard filters to show only Turkey bookings, all metrics recalculate for Turkey subset, breadcrumb displays "Filtered: Turkey"

4. **Given** admin views "Top Providers by Revenue" table
   **When** admin sorts by "Booking Count" (descending)
   **Then** table reorders to show providers with most bookings at top, displaying: provider name, booking count, total revenue, average booking value

5. **Given** admin clicks "Export Full Report" button
   **When** system generates PDF report
   **Then** PDF includes all dashboard data (charts as images, tables, metrics), downloads within 10 seconds, filename: "Hairline_Financial_Report_[date_range].pdf"

---

### User Story 6 - Refund Processing with Approval Workflow (Priority: P2)

A patient requests refund due to cancellation, admin reviews request against cancellation policy, processes partial or full refund, and system updates all financial records.

**Why this priority**: Refund handling impacts customer satisfaction and platform reputation; automated workflow ensures policy compliance and audit trail.

**Independent Test**: Create confirmed booking, simulate cancellation request at different timeframes (>30 days, 15-30 days, <15 days), process refund, verify correct amount calculated per policy, Stripe refund initiated, invoice updated.

**Acceptance Scenarios**:

1. **Given** patient cancels booking 45 days before treatment date
   **When** admin navigates to "Patient Billing" → searches for patient invoice → clicks "Process Refund"
   **Then** system calculates refund amount per cancellation policy (90% of total = £1,800 for £2,000 booking), displays: "Refund Amount: £1,800 (90% per policy)", "Platform Fee (non-refundable): £200"

2. **Given** admin reviews refund details AND clicks "Approve Refund"
   **When** system prompts for secondary approval (high-value transaction >£1,000)
   **Then** system sends notification to senior admin: "Refund approval required: £1,800 for Booking #HP25110234", senior admin reviews and approves

3. **Given** secondary approval received
   **When** system initiates Stripe refund
   **Then** Stripe refund API call succeeds, refund status "Processing", admin sees confirmation "Refund initiated. Funds will return to patient card within 5-7 business days"

4. **Given** Stripe refund completes (webhook received)
   **When** system processes webhook event
   **Then** invoice updated: "Status: Refunded", "Refund Amount: £1,800", "Refund Date: [date]", patient receives email: "Your refund of £1,800 has been processed", provider payout adjusted (if not yet processed)

5. **Given** provider payout not yet processed (treatment was upcoming)
   **When** refund completes
   **Then** system removes booking from provider's upcoming payout calculation, provider does NOT receive payment for cancelled booking

---

### Edge Cases

- **What happens when** patient's card expires before installment payment due?
  - System attempts charge, receives "expired card" error from Stripe
  - System sends email to patient: "Payment method expired. Please update card to continue installment plan."
  - Patient updates card via P-01: Auth & Profile Management → Payment Methods
  - System retries charge with updated card on next scheduled attempt

- **How does system handle** provider payout when provider's bank account is closed?
  - Stripe transfer fails with "invalid bank account" error
  - System flags payout as "Failed", sends admin alert
  - Admin contacts provider via support system to request updated bank account
  - Provider updates bank account in PR-06: Profile & Settings Management
  - Admin verifies new account and manually retries payout

- **What occurs if** discount code reaches maximum usage limit mid-checkout?
  - Patient enters discount code "SUMMER25" at checkout (usage: 499/500)
  - Another patient simultaneously applies same code (usage: 500/500)
  - First patient completes checkout: discount applied successfully
  - Second patient completes checkout: system displays "Discount code no longer available (maximum uses reached)"
  - System prevents race condition using database row locking on discount code record

- **How to manage** currency exchange rate API downtime during booking?
  - Patient initiates booking requiring EUR → GBP conversion
  - System attempts to fetch latest exchange rate from API, receives timeout error
  - System uses cached exchange rate (refreshed 1 hour ago) with warning notification to admin: "Using cached rate (1 hour old) due to API unavailability"
  - System flags booking for manual review if cached rate >24 hours old
  - Admin reviews and approves rate OR contacts patient to confirm acceptable rate

- **What happens when** affiliate discount code and provider discount code both applied?
  - Patient enters both "AFFILIATE10" (10% affiliate code) AND "PROVIDER15" (15% provider code) at checkout
  - System applies discount priority rule: Patient code > Provider code > Affiliate code (only ONE discount per booking)
  - System displays: "AFFILIATE10 discount applied (10%). PROVIDER15 not applicable (only one discount per booking)."
  - System attributes booking to affiliate for commission calculation

- **How does system handle** partial refund (patient cancels add-on packages but keeps base treatment)?
  - Patient booked treatment (£2,000) + hotel package (£500) + PRP add-on (£200), total £2,700
  - Patient cancels hotel and PRP, keeps base treatment
  - Admin processes partial refund: £500 + £200 = £700
  - System initiates Stripe refund for £700, updates invoice: "Partial Refund: £700", "New Total: £2,000"
  - Provider payout adjusted: original commission calculated on £2,700, recalculated on £2,000

---

## Functional Requirements Summary

### Core Requirements

- **REQ-017-001**: System MUST allow admins to view all patient invoices with filtering by payment status (Pending, Partial, Paid, Overdue, Refunded)
- **REQ-017-002**: System MUST allow admins to view all provider payment schedules (weekly, bi-weekly, monthly) and process payouts with itemized treatment breakdowns
- **REQ-017-003**: System MUST allow admins to create discount codes (platform-wide, provider-specific, affiliate) with approval workflows for "Both Fees" discounts
- **REQ-017-004**: System MUST automatically generate invoices (PDF) immediately upon successful patient payment (deposit, installment, final)
- **REQ-017-005**: System MUST automatically schedule and charge installment payments on configured dates, with 3 retry attempts for failed charges
- **REQ-017-006**: System MUST calculate provider payouts based on completed treatments (status "Completed" or "Aftercare"), deducting platform commission
- **REQ-017-007**: System MUST lock currency exchange rates at time of booking acceptance for all multi-currency transactions
- **REQ-017-008**: System MUST generate financial dashboard with real-time metrics: total revenue, platform commission, provider payouts, outstanding invoices
- **REQ-017-009**: System MUST track affiliate commissions based on discount code usage and process monthly payouts
- **REQ-017-010**: System MUST send payment reminder emails 3 days before installment due date and 7 days if overdue

### Data Requirements

- **REQ-017-011**: System MUST maintain complete transaction history for all payments, refunds, and payouts with timestamp, amount, currency, and affected parties
- **REQ-017-012**: System MUST store provider bank account details encrypted at rest (AES-256) and display masked (last 4 digits only) in UI
- **REQ-017-013**: System MUST track discount code usage with metrics: times used, total discount amount, bookings generated, ROI
- **REQ-017-014**: System MUST store locked exchange rates per booking for multi-currency transactions (rate never changes after booking)
- **REQ-017-015**: System MUST maintain separate payout records for providers and affiliates with status tracking (Pending, Processing, Paid, Failed)

### Security & Privacy Requirements

- **REQ-017-016**: System MUST require admin multi-factor authentication (MFA) for all financial operations (payout approval, refund processing)
- **REQ-017-017**: System MUST implement role-based access control (RBAC) with granular permissions: Billing Admin (full access), Billing Viewer (read-only), Super Admin (secondary approval)
- **REQ-017-018**: System MUST log ALL financial actions with audit trail: admin ID, timestamp, IP address, action type, before/after values
- **REQ-017-019**: System MUST mask patient payment methods in UI (display "Visa ending in 1234" NOT full card number)
- **REQ-017-020**: System MUST soft-delete financial records (no hard deletion); retain records for minimum 7 years (compliance requirement)
- **REQ-017-021**: System MUST encrypt provider bank account details at rest using AES-256; decrypt ONLY during payout processing
- **REQ-017-022**: System MUST verify Stripe webhook signatures to prevent spoofing and ensure event authenticity

### Integration Requirements

- **REQ-017-023**: System MUST integrate with Stripe Payment API for payment intents, transfers, refunds, and webhook event processing
- **REQ-017-024**: System MUST integrate with Currency Exchange API (xe.com or equivalent) with hourly rate updates and 1-hour caching
- **REQ-017-025**: System MUST use idempotent Stripe API calls (unique idempotency keys per transaction) to prevent duplicate charges/transfers
- **REQ-017-026**: System MUST process Stripe webhook events asynchronously via job queue (Redis Queue or AWS SQS)
- **REQ-017-027**: System MUST provide read-only API for Provider Platform to query payout history and earnings analytics

---

## Key Entities

- **Entity 1 - Patient Invoice**
  - **Key attributes**: invoice_id, patient_id, booking_id, invoice_date, due_date, total_amount, amount_paid, outstanding_balance, currency, payment_status (Pending, Partial, Paid, Overdue, Refunded), payment_method, installment_plan_id (if applicable), discount_code_applied
  - **Relationships**: One invoice per booking; one patient can have many invoices; one invoice can have many installment payments

- **Entity 2 - Provider Payout**
  - **Key attributes**: payout_id, provider_id, payout_period (date_range), total_revenue, commission_percentage, commission_amount, net_payout, bank_account_id, payout_status (Pending, Processing, Paid, Failed), payout_date, stripe_transfer_id, invoice_pdf_url
  - **Relationships**: One payout includes many completed bookings; one provider has many payouts over time

- **Entity 3 - Installment Payment**
  - **Key attributes**: installment_id, invoice_id, installment_number, installment_amount, scheduled_date, payment_status (Pending, Paid, Failed), retry_count, paid_date, stripe_payment_intent_id
  - **Relationships**: One invoice can have many installments (2-9); one installment linked to one invoice

- **Entity 4 - Discount Code**
  - **Key attributes**: discount_code_id, discount_code, discount_name, discount_type (Platform-Wide, Provider-Specific, Affiliate), affected_fees (Hairline Only, Both Fees), discount_value_type (Percentage, Fixed Amount), discount_value, currency (if fixed amount), valid_from, valid_until, max_uses, current_uses, status (Draft, Active, Expired, Disabled), approval_required (boolean), approval_status
  - **Relationships**: One discount code can be applied to many bookings; one booking has at most one discount code

- **Entity 5 - Transaction Audit Log**
  - **Key attributes**: log_id, admin_user_id, timestamp, action_type (Payout Approved, Refund Processed, Invoice Generated), affected_entity_type (Invoice, Payout, Booking), affected_entity_id, before_value, after_value, ip_address, notes
  - **Relationships**: One admin action generates one log entry; one entity (invoice/payout) can have many log entries over time

- **Entity 6 - Affiliate Commission**
  - **Key attributes**: commission_id, affiliate_id, booking_id, discount_code_id, booking_amount, commission_rate, commission_amount, payout_period (month), payout_status (Pending, Paid), payout_date
  - **Relationships**: One booking generates one affiliate commission (if booked via affiliate code); one affiliate has many commissions over time

- **Entity 7 - Currency Exchange Rate Lock**
  - **Key attributes**: rate_lock_id, booking_id, source_currency, target_currency, locked_rate, lock_timestamp
  - **Relationships**: One booking has one currency rate lock (if multi-currency); rate used for all calculations related to that booking

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-12 | 1.0 | Initial PRD creation | Claude Code (AI) |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | [Name] | [Date] | [Status] |
| Technical Lead | [Name] | [Date] | [Status] |
| Finance Lead | [Name] | [Date] | [Status] |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-011 Aftercare & Recovery Management PRD
**Last Updated**: 2025-11-12
