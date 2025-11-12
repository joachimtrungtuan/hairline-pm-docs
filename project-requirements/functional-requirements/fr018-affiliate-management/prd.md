# Product Requirements Document: Affiliate Management

**Module**: A-07: Affiliate Program Management
**Feature Branch**: `fr018-affiliate-management`
**Created**: 2025-11-12
**Status**: Draft
**Source**: FR-018 from system-prd.md, Hairline-AdminPlatform-Part1.txt (lines 125-409)

---

## Executive Summary

The Affiliate Management module enables Hairline to partner with external entities (influencers, clinics, organizations) who promote the platform in exchange for commission-based compensation. This module provides the infrastructure for onboarding affiliates, generating unique tracking codes, monitoring referral performance, calculating commissions, and processing monthly payouts. By creating a scalable affiliate program, Hairline can expand market reach, increase patient acquisition, and drive revenue growth through trusted third-party channels while maintaining full transparency and control over partnership economics.

**Key Value Proposition**:
- **For Affiliates**: Easy-to-use dashboard with real-time tracking of referrals, earnings, and payout history
- **For Admins**: Streamlined affiliate onboarding, automated commission tracking, and simplified monthly payout processing
- **For Business**: Cost-effective patient acquisition channel with performance-based compensation model

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-03)**: Patients apply affiliate discount codes at checkout to receive promotional offers
- **Provider Platform (PR-05)**: No direct provider interaction; providers see bookings with affiliate codes applied
- **Admin Platform (A-07)**: Full affiliate lifecycle management including onboarding, code creation, commission tracking, and payout processing
- **Shared Services (S-02)**: Payment processing service handles affiliate commission payouts; notification service sends payout confirmations

### Multi-Tenant Breakdown

**Patient Platform (P-03)**:

- Patients can enter affiliate discount codes during booking checkout
- System validates affiliate codes and applies discounts automatically
- Booking confirmation shows affiliate discount applied (code name displayed)
- Patients do NOT see affiliate commission structure or payout information

**Provider Platform (PR-05)**:

- Providers see bookings with affiliate codes in their dashboard (read-only view)
- Providers understand that affiliate discounts come from Hairline's commission (not their payout)
- No provider action required for affiliate-referred bookings

**Admin Platform (A-07)**:

- **Affiliate Onboarding**: Create affiliate accounts with contact details, payment information, commission structure
- **Discount Code Management**: Generate unique affiliate discount codes with customizable parameters (percentage/fixed amount, expiration, usage limits)
- **Performance Tracking**: View real-time statistics on referral counts, booking conversions, revenue generated per affiliate
- **Commission Calculation**: System automatically calculates affiliate commissions based on completed bookings
- **Payout Processing**: Monthly batch payout workflow with approval and confirmation
- **Reporting**: Generate affiliate performance reports for analysis and optimization

**Shared Services (S-02)**:

- **Payment Processing Service**: Handles affiliate commission payouts via configured payment method (bank transfer, PayPal, etc.)
- **Notification Service**: Sends payout confirmation emails to affiliates with transaction details
- **Audit Trail Service**: Logs all affiliate-related transactions (code usage, commission calculations, payouts)

### Communication Structure

**In Scope**:

- Email notifications to affiliates when discount codes are created or updated
- Email notifications to affiliates when monthly payouts are processed
- Admin-to-affiliate communication via notes in admin dashboard (internal only)
- System-generated payout confirmations with transaction breakdown

**Out of Scope**:

- Direct messaging between patients and affiliates (handled outside platform)
- Marketing material creation (affiliates use externally hosted materials)
- Affiliate training or onboarding calls (manual process outside platform)

### Entry Points

- **Admin-initiated**: Admins access Affiliate Management section in admin dashboard to onboard new affiliates
- **Affiliate-initiated**: Affiliates log into dedicated affiliate portal to view performance dashboard
- **Patient-triggered**: Patients enter affiliate codes during booking checkout, triggering tracking and commission calculation
- **System-scheduled**: Automated monthly job generates payout reports on 7th of each month (configurable)

---

## Business Workflows

### Main Flow: Affiliate Onboarding and Code Creation

**Actors**: Admin, System, Affiliate
**Trigger**: Admin decides to partner with new affiliate organization
**Outcome**: Affiliate account created, unique discount code generated, affiliate granted access to dashboard

**Steps**:

1. Admin navigates to Admin Dashboard > Affiliate Management > Add New Affiliate
2. Admin enters affiliate details:
   - Affiliate name (organization/individual name)
   - Contact email (for login and payout notifications)
   - Payment method (bank account details, PayPal email, etc.)
   - Commission structure (percentage of Hairline commission OR fixed amount per booking)
   - Payout schedule (monthly on 7th - configurable date)
3. System validates inputs (unique email, valid payment details format)
4. Admin submits affiliate onboarding form
5. System creates affiliate account with:
   - Generated unique affiliate ID
   - Login credentials sent to affiliate email
   - Initial status: "Active"
6. Admin creates discount code for affiliate:
   - Discount code name (e.g., "WINTER2025", "PARTNER10")
   - Discount type: Hairline fees only (deducted from Hairline's commission)
   - Discount amount: Percentage (e.g., 10%) OR fixed amount (e.g., £50)
   - Expiration date (optional)
   - Maximum usage count (optional, e.g., first 200 users)
   - Auto-apply vs. code-based (manual entry required)
7. System validates discount code (uniqueness, valid parameters)
8. System saves discount code and links to affiliate account
9. System sends email to affiliate with:
   - Dashboard login credentials
   - Discount code(s) created for their promotion
   - Commission structure details
   - Payout schedule information
10. Affiliate receives credentials and accesses dashboard to view real-time stats

### Alternative Flows

**A1: Multiple Discount Codes Per Affiliate**

- **Trigger**: Admin wants to create multiple promotional campaigns for single affiliate (e.g., seasonal codes, region-specific codes)
- **Steps**:
  1. Admin navigates to existing affiliate profile
  2. Admin clicks "Add New Discount Code"
  3. System displays discount code creation form
  4. Admin configures new code with different parameters (different discount percentage, expiration, etc.)
  5. System validates and saves new code linked to same affiliate account
  6. System sends email notification to affiliate about new code availability
- **Outcome**: Single affiliate can promote multiple discount codes, all tracked under same affiliate account for commission calculation

**A2: Edit Affiliate Commission Structure**

- **Trigger**: Business negotiates new commission terms with existing affiliate
- **Steps**:
  1. Admin navigates to affiliate profile in admin dashboard
  2. Admin clicks "Edit Commission Structure"
  3. Admin modifies commission parameters (percentage/fixed amount)
  4. System prompts admin to confirm changes and effective date
  5. Admin confirms changes
  6. System updates affiliate record with new commission structure
  7. System applies new commission rates to bookings completed AFTER effective date (historical commissions remain unchanged)
  8. System sends email notification to affiliate about commission structure change
- **Outcome**: Affiliate commission structure updated with proper audit trail; future payouts calculated using new rates

**A3: Affiliate-Requested Payout Information**

- **Trigger**: Affiliate logs into dashboard to check payout status
- **Steps**:
  1. Affiliate logs into affiliate portal using credentials
  2. System displays affiliate dashboard with:
     - Total referrals count (all-time and current month)
     - Completed bookings count (bookings that generated commission)
     - Total revenue generated for Hairline (from affiliate referrals)
     - Total commissions earned (all-time and pending payout)
     - Upcoming payout amount and date
     - Payout history with transaction details
  3. Affiliate clicks on individual discount code to view breakdown
  4. System displays per-code statistics:
     - Code usage count (applied vs. completed checkouts)
     - Conversion rate (applied codes that resulted in bookings)
     - Revenue per code
     - Commission earned per code
  5. Affiliate reviews data and downloads PDF report if needed
- **Outcome**: Affiliate has full visibility into performance metrics and earnings without admin intervention

**B1: Invalid Discount Code Application**

- **Trigger**: Patient enters affiliate discount code that is expired, reached usage limit, or invalid
- **Steps**:
  1. Patient enters discount code at checkout
  2. System validates code against:
     - Expiration date (if set)
     - Usage limit (if set)
     - Active status
  3. System determines code is invalid/expired
  4. System displays error message: "This discount code is no longer valid. Please check the code or contact support."
  5. Patient can proceed with checkout without discount OR enter different valid code
  6. System does NOT track this as affiliate referral (no commission triggered)
- **Outcome**: Patient notified of invalid code; affiliate not credited for failed code application; checkout can still complete

**B2: Payout Processing Failure**

- **Trigger**: Monthly automated payout job encounters payment processing error (invalid bank account, insufficient funds in Hairline account, etc.)
- **Steps**:

  1. System initiates monthly payout batch on 7th of month
  2. System calculates commissions owed to each affiliate based on completed bookings from previous month
  3. System attempts to process payment via payment gateway
  4. Payment gateway returns error (e.g., "Invalid bank account number")
  5. System logs error with affiliate ID, amount, and error message
  6. System marks payout as "Failed" in admin dashboard
  7. System sends alert notification to admin team with failed payout details
  8. Admin reviews error and contacts affiliate to resolve payment details
  9. Admin manually triggers retry once payment details corrected
  10. System re-processes payment and marks as "Paid" upon success
- **Outcome**: Failed payouts flagged for admin review; manual intervention resolves payment issues; affiliate receives delayed payout with explanation

**B3: Affiliate Account Suspension**

- **Trigger**: Admin detects fraudulent activity or policy violation by affiliate (e.g., fake referrals, unauthorized promotion)
- **Steps**:
  1. Admin navigates to affiliate profile
  2. Admin clicks "Suspend Account"
  3. System prompts admin for suspension reason (required field)
  4. Admin enters reason and confirms suspension
  5. System updates affiliate status to "Suspended"
  6. System disables all discount codes associated with affiliate (codes no longer valid at checkout)
  7. System sends email notification to affiliate about suspension with reason
  8. System retains historical data (referrals, commissions, payouts) but prevents new activity
  9. Pending unpaid commissions are held pending investigation
  10. Admin can reinstate account later by changing status to "Active"
- **Outcome**: Affiliate account suspended; discount codes deactivated; pending payouts held; full audit trail maintained

---

## Screen Specifications

### Screen 1: Affiliate Management Dashboard (Admin)

**Purpose**: Provides admins with overview of all affiliates and their performance metrics

**Data Fields**:

| Field Name             | Type     | Required | Description                                        | Validation Rules                        |
|------------------------|----------|----------|----------------------------------------------------|-----------------------------------------|
| Affiliate Name         | text     | Yes      | Organization or individual name                    | Max 200 characters                      |
| Contact Email          | email    | Yes      | Primary contact email for login and notifications  | Valid email format, unique              |
| Total Referrals        | number   | N/A      | Count of all bookings using affiliate codes        | Read-only, system-calculated            |
| Total Revenue          | currency | N/A      | Total booking value from affiliate referrals       | Read-only, system-calculated            |
| Total Commissions Paid | currency | N/A      | Sum of all commissions paid to date                | Read-only, system-calculated            |
| Pending Payout         | currency | N/A      | Commission amount awaiting next payout cycle       | Read-only, system-calculated            |
| Status                 | select   | Yes      | Account status: Active, Suspended, Inactive        | Dropdown with 3 options                 |
| Actions                | buttons  | N/A      | View Details, Edit, Suspend, Generate Report       | Context-dependent based on status       |

**Business Rules**:

- **Sorting**: Default sort by "Total Revenue" descending (highest performers first)
- **Filtering**: Admin can filter by status (Active/Suspended/Inactive) or search by affiliate name/email
- **Pagination**: Display 25 affiliates per page with pagination controls
- **Quick Actions**: Inline "Generate Report" button exports affiliate performance to PDF
- **Status Indicators**: Color-coded status badges (Active = green, Suspended = red, Inactive = gray)

**Notes**:

- Use data tables with sortable columns for easy performance comparison
- Highlight affiliates with pending payouts > £1000 with yellow background
- Show last payout date in tooltip on hover over "Total Commissions Paid"

---

### Screen 2: Add/Edit Affiliate Form (Admin)

**Purpose**: Allows admins to create new affiliate accounts or edit existing affiliate details

**Data Fields**:

| Field Name                | Type     | Required | Description                                          | Validation Rules                                |
|---------------------------|----------|----------|------------------------------------------------------|-------------------------------------------------|
| Affiliate Name            | text     | Yes      | Full name of organization or individual              | Max 200 characters, no special characters       |
| Contact Email             | email    | Yes      | Email for login and notifications                    | Valid email format, unique across affiliates    |
| Payment Method            | select   | Yes      | Bank Transfer, PayPal, Other                         | Dropdown with 3 options                         |
| Bank Account Details      | text     | Conditional | Bank name, account number, sort code (UK)          | Required if "Bank Transfer" selected, masked in UI (show last 4 digits) |
| PayPal Email              | email    | Conditional | PayPal account email                                | Required if "PayPal" selected, valid email format |
| Commission Type           | radio    | Yes      | Percentage of Hairline Commission OR Fixed Amount    | One option must be selected                     |
| Commission Percentage     | number   | Conditional | % of Hairline's commission paid to affiliate        | Required if "Percentage" selected, range 5-50%  |
| Commission Fixed Amount   | currency | Conditional | Fixed £ amount per completed booking                | Required if "Fixed Amount" selected, min £10    |
| Payout Schedule           | select   | Yes      | Monthly on 7th (default)                             | Currently only monthly option available         |
| Notes (Internal)          | textarea | No       | Admin notes about affiliate relationship             | Max 1000 characters, not visible to affiliate   |

**Business Rules**:

- **Email Uniqueness**: System validates email is not already registered as affiliate or admin user
- **Payment Masking**: Bank account details masked in UI after initial entry (show last 4 digits only for security)
- **Commission Validation**: If percentage type, system calculates preview of commission for example booking (e.g., "For £1000 booking with 15% Hairline commission, affiliate earns £22.50")
- **Default Values**: Payout schedule defaults to "Monthly on 7th"; commission type defaults to "Percentage"
- **Edit Restrictions**: Email cannot be changed after account creation (must create new account if email change needed)

**Notes**:

- Use conditional rendering: Bank details field shown only if "Bank Transfer" selected; PayPal field shown only if "PayPal" selected
- Display warning message if commission percentage > 30%: "High commission rate - please confirm business approval"
- Auto-save draft every 30 seconds to prevent data loss on accidental navigation away

---

### Screen 3: Discount Code Management (Admin)

**Purpose**: Allows admins to create and manage discount codes linked to affiliate accounts

**Data Fields**:

| Field Name                | Type     | Required | Description                                          | Validation Rules                                |
|---------------------------|----------|----------|------------------------------------------------------|-------------------------------------------------|
| Linked Affiliate          | select   | Yes      | Affiliate account this code belongs to               | Dropdown of active affiliates                   |
| Discount Code             | text     | Yes      | Unique code patients enter at checkout               | Uppercase alphanumeric, 4-20 chars, unique      |
| Discount Type             | select   | Yes      | Hairline Fees Only (deducted from platform commission) | Currently only one option (future: Both Fees) |
| Discount Amount Type      | radio    | Yes      | Percentage OR Fixed Amount                           | One option must be selected                     |
| Discount Percentage       | number   | Conditional | % discount applied to booking total                 | Required if "Percentage" selected, range 5-30%  |
| Discount Fixed Amount     | currency | Conditional | Fixed £ discount applied to booking                 | Required if "Fixed Amount" selected, min £10    |
| Application Method        | radio    | Yes      | Auto-apply OR Code-based (manual entry)              | One option must be selected                     |
| Expiration Date           | date     | No       | Date after which code is no longer valid             | Must be future date if set                      |
| Maximum Usage Count       | number   | No       | Max number of times code can be used                 | Min 1 if set, unlimited if blank                |
| Current Usage Count       | number   | N/A      | Number of times code has been applied                | Read-only, system-calculated                    |
| Status                    | toggle   | Yes      | Active (enabled) / Inactive (disabled)               | Toggle switch, default Active                   |

**Business Rules**:

- **Code Uniqueness**: System validates discount code is unique across all affiliates (case-insensitive check)
- **Code Format**: System automatically converts code to uppercase on save
- **Expiration Logic**: If expiration date set, system automatically deactivates code at midnight (UTC) on that date
- **Usage Limit**: Once usage count reaches maximum, system automatically deactivates code
- **Applied vs. Completed**: System tracks "applied" (code entered at checkout) and "completed" (booking payment confirmed) separately
- **Commission Trigger**: Affiliate commission is ONLY calculated for "completed" bookings, not "applied" codes

**Notes**:

- Display usage statistics in real-time: "125 applied / 87 completed (69.6% conversion rate)"
- Show color-coded status: Active codes in green, expired codes in gray, usage-limit-reached codes in orange
- Allow bulk code creation: "Create 10 codes with prefix SUMMER2025-01, SUMMER2025-02, etc."

---

### Screen 4: Affiliate Performance Dashboard (Affiliate Portal)

**Purpose**: Provides affiliates with real-time visibility into referral performance and earnings

**Data Fields**:

| Field Name                | Type     | Required | Description                                          | Validation Rules                                |
|---------------------------|----------|----------|------------------------------------------------------|-------------------------------------------------|
| Total Referrals (All-Time) | number  | N/A      | Count of all completed bookings using affiliate codes | Read-only, system-calculated                   |
| Referrals This Month      | number   | N/A      | Count of completed bookings in current month         | Read-only, system-calculated                    |
| Total Revenue Generated   | currency | N/A      | Sum of booking values from affiliate referrals       | Read-only, system-calculated                    |
| Total Commissions Earned  | currency | N/A      | Sum of all commissions earned to date                | Read-only, system-calculated                    |
| Commissions Paid          | currency | N/A      | Sum of commissions already paid out                  | Read-only, system-calculated                    |
| Pending Payout            | currency | N/A      | Commission awaiting next payout (unpaid balance)     | Read-only, system-calculated                    |
| Next Payout Date          | date     | N/A      | Date of next scheduled payout                        | Read-only, system-configured (default: 7th)     |
| Discount Codes            | list     | N/A      | List of all discount codes assigned to affiliate     | Read-only, clickable for per-code breakdown     |

**Business Rules**:

- **Real-Time Updates**: Dashboard data refreshes every 5 minutes (or on manual refresh)
- **Payout Calculation**: "Pending Payout" includes commissions from completed bookings in previous month (not yet paid)
- **Conversion Funnel**: Dashboard shows conversion funnel: Code Applied → Checkout Started → Payment Completed
- **Monthly Breakdown**: Affiliate can toggle view between "All-Time" and "Current Month" statistics
- **Export Report**: Affiliate can download performance report as PDF for personal records

**Notes**:

- Use visual charts: Line graph for referrals over time, pie chart for conversion funnel
- Display prominent "Pending Payout" amount at top of dashboard with countdown to next payout date
- Show affiliate's unique referral link (auto-apply code URL) with one-click copy button

---

### Screen 5: Affiliate Payout Processing (Admin)

**Purpose**: Allows admins to review and process monthly affiliate commission payouts

**Data Fields**:

| Field Name                | Type     | Required | Description                                          | Validation Rules                                |
|---------------------------|----------|----------|------------------------------------------------------|-------------------------------------------------|
| Payout Month              | month    | Yes      | Month for which payouts are being processed          | Format: "November 2025"                         |
| Affiliate Name            | text     | N/A      | Name of affiliate receiving payout                   | Read-only, from affiliate record                |
| Total Completed Bookings  | number   | N/A      | Count of completed bookings in payout period         | Read-only, system-calculated                    |
| Total Commissions Owed    | currency | N/A      | Sum of commissions for completed bookings            | Read-only, system-calculated                    |
| Payment Method            | text     | N/A      | Bank transfer / PayPal (from affiliate record)       | Read-only, from affiliate payment details       |
| Payment Details           | text     | N/A      | Masked bank account or PayPal email                  | Read-only, masked (last 4 digits)               |
| Payout Status             | select   | Yes      | Pending, Processing, Paid, Failed                    | Dropdown, admin updates status                  |
| Notes                     | textarea | No       | Admin notes about payout (e.g., "Delayed due to bank holiday") | Max 500 characters                       |
| Actions                   | buttons  | N/A      | Confirm Payout, Mark as Paid, Retry Failed          | Context-dependent based on status               |

**Business Rules**:

- **Automated Generation**: System automatically generates payout list on 7th of each month for previous month's completed bookings
- **Batch Processing**: Admin can select multiple affiliates and click "Process Batch Payout" to pay all at once
- **Payment Gateway Integration**: System integrates with payment gateway API to initiate bank transfers or PayPal payments
- **Status Workflow**: Pending → Processing (payment initiated) → Paid (payment confirmed) OR Failed (payment error)
- **Retry Logic**: If payout fails, admin can click "Retry Failed" to re-attempt after resolving payment details
- **Email Notifications**: System automatically sends payout confirmation email to affiliate when status changes to "Paid"

**Notes**:

- Display total payout amount for month at top of screen (sum of all affiliate payouts)
- Highlight failed payouts in red with error message displayed
- Allow admin to add internal notes explaining payout delays or issues (not visible to affiliate)
- Show payout history: Admin can view past months' payouts by selecting different month from dropdown

---

### Screen 6: Affiliate Billing History (Admin)

**Purpose**: Provides admins with historical view of all affiliate payouts for auditing and reconciliation

**Data Fields**:

| Field Name                | Type     | Required | Description                                          | Validation Rules                                |
|---------------------------|----------|----------|------------------------------------------------------|-------------------------------------------------|
| Payout Date               | date     | N/A      | Date payout was processed                            | Read-only, system-recorded                      |
| Affiliate Name            | text     | N/A      | Name of affiliate who received payout                | Read-only, from affiliate record                |
| Payout Month              | month    | N/A      | Month period payout covers                           | Format: "November 2025"                         |
| Commission Amount         | currency | N/A      | Total commission paid in this payout                 | Read-only, system-calculated                    |
| Payment Method            | text     | N/A      | Bank transfer / PayPal                               | Read-only, from affiliate payment details       |
| Transaction ID            | text     | N/A      | Payment gateway transaction reference                | Read-only, from payment gateway                 |
| Status                    | text     | N/A      | Paid, Failed, Refunded                               | Read-only, final status                         |
| Actions                   | buttons  | N/A      | View Details, Download Receipt                       | View details opens modal with breakdown         |

**Business Rules**:

- **Audit Trail**: All payouts permanently logged with full details (affiliate, amount, date, transaction ID)
- **Filtering**: Admin can filter by affiliate, date range, payment status
- **Export**: Admin can export payout history to CSV for accounting/tax purposes
- **Retention**: Payout records retained for 7 years minimum (compliance requirement)
- **Search**: Full-text search on affiliate name, transaction ID, payout month

**Notes**:

- Use pagination for large datasets (50 records per page)
- Display monthly aggregates: Total payouts per month, number of affiliates paid
- Provide "Download Receipt" button to generate PDF receipt for each payout (for affiliate records)

---

## Business Rules

### General Module Rules

- **Rule 1**: Affiliate commissions are ONLY calculated for completed bookings where payment is confirmed (not for quote requests or pending bookings)
- **Rule 2**: Affiliate discount codes apply ONLY to Hairline's commission (does NOT reduce provider payout)
- **Rule 3**: Only ONE discount code can be applied per booking (priority: Patient code > Provider code > Affiliate code)
- **Rule 4**: Affiliate commissions are deducted from Hairline's commission, NOT from provider's payout
- **Rule 5**: Payout processing occurs monthly on 7th of each month (configurable) for previous month's completed bookings
- **Rule 6**: Affiliates can have multiple active discount codes simultaneously for different campaigns

### Data & Privacy Rules

- **Privacy Rule 1**: Patient identity is NEVER shared with affiliates (affiliates see only aggregated statistics, not individual patient names)
- **Privacy Rule 2**: Affiliate payment details (bank accounts, PayPal emails) are masked in UI (show last 4 characters only)
- **Privacy Rule 3**: Affiliate dashboard access requires secure login (username/password + optional MFA)
- **Audit Rule**: All affiliate actions logged with timestamp, user ID, and action type (code usage, commission calculation, payout processing)
- **GDPR**: Affiliate personal data (contact info, payment details) can be deleted upon request (historical commission data retained for accounting)

### Admin Editability Rules

**Editable by Admin**:

- Affiliate account details (name, email, payment method, commission structure)
- Discount code parameters (expiration date, usage limits, active/inactive status)
- Payout schedule date (default 7th of month, configurable to any date 1-28)
- Commission percentage/fixed amount per affiliate (with effective date for changes)

**Fixed in Codebase (Not Editable)**:

- Affiliate commission calculation logic (percentage of Hairline commission OR fixed amount per booking)
- Discount code uniqueness validation rules
- Payout workflow status transitions (Pending → Processing → Paid/Failed)
- Audit trail retention period (7 years minimum)

**Configurable with Restrictions**:

- Payout schedule can be changed but requires 30-day notice (cannot apply to current month's pending payouts)
- Commission structure changes apply ONLY to future bookings (historical commissions cannot be retroactively modified)

### Payment & Billing Rules

- **Payment Rule 1**: Affiliate commissions calculated AFTER patient completes full payment for booking
- **Payment Rule 2**: If patient refunds booking, affiliate commission is reversed (deducted from next payout)
- **Payment Rule 3**: Minimum payout threshold: £50 (commissions below £50 roll over to next month)
- **Currency Rule**: All affiliate payouts processed in GBP (affiliate responsible for currency conversion if needed)
- **Billing Rule 1**: Payouts processed via bank transfer (UK affiliates) or PayPal (international affiliates)
- **Billing Rule 2**: Hairline covers payment processing fees for payouts (not deducted from affiliate commission)

---

## Success Criteria

### Patient Experience Metrics

- **SC-001**: Patients can successfully apply affiliate discount codes at checkout with 95%+ success rate (valid codes accepted without errors)
- **SC-002**: Patients receive booking confirmation showing affiliate discount applied within 2 minutes of checkout completion
- **SC-003**: Patients who use affiliate codes have 20%+ higher conversion rate (quote-to-booking) compared to non-affiliate bookings

### Provider Efficiency Metrics

- **SC-004**: Providers can view affiliate code details for their bookings in provider dashboard without admin support
- **SC-005**: 100% of providers understand that affiliate discounts do NOT reduce their payout (clarity in payment breakdown)

### Admin Management Metrics

- **SC-006**: Admins can onboard new affiliates (account creation + discount code) in under 5 minutes per affiliate
- **SC-007**: Automated payout processing reduces admin time by 80% compared to manual payout workflows
- **SC-008**: 100% of monthly payouts processed within 24 hours of scheduled date (7th of month)
- **SC-009**: Admin support tickets related to affiliate payouts reduced by 70% through self-service affiliate dashboard

### Affiliate Experience Metrics

- **SC-010**: Affiliates can view real-time performance statistics without admin assistance (dashboard uptime 99.9%)
- **SC-011**: Affiliates receive payout confirmations within 24 hours of payment processing
- **SC-012**: Affiliate dashboard load time under 2 seconds for 95% of requests
- **SC-013**: 90%+ of affiliates report satisfaction with dashboard usability and data transparency

### System Performance Metrics

- **SC-014**: Discount code validation at checkout completes in under 500ms for 95% of requests
- **SC-015**: Affiliate commission calculations processed within 1 hour of booking completion
- **SC-016**: System supports 100+ active affiliates with 10,000+ code applications per month without performance degradation
- **SC-017**: Payout batch processing completes within 30 minutes for up to 100 affiliates per month

### Business Impact Metrics

- **SC-018**: Affiliate program generates 15%+ of total patient acquisition within 6 months of launch
- **SC-019**: Average cost per acquisition via affiliates is 30%+ lower than paid advertising channels
- **SC-020**: Affiliate-referred patients have 25%+ higher lifetime value (repeat bookings) compared to direct patients
- **SC-021**: 80%+ of active affiliates remain in program for 12+ months (low churn rate)
- **SC-022**: Affiliate program expands Hairline's reach to 5+ new geographic markets within 12 months

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **FR-007 / Module S-02: Payment Processing Service**
  - **Why needed**: Affiliate commission payouts require payment gateway integration to process bank transfers or PayPal payments
  - **Integration point**: Payout processing workflow calls Payment Service API to initiate transfers with affiliate payment details

- **FR-017 / Module A-05: Admin Billing & Financial Management**
  - **Why needed**: Affiliate discount code application must integrate with commission calculation and booking payment processing
  - **Integration point**: When patient applies affiliate code, system calculates discount from Hairline's commission and tracks for affiliate payout

- **FR-019 / Module A-06: Discount & Promotion Management**
  - **Why needed**: Affiliate discount codes are a subset of platform-wide discount system
  - **Integration point**: Affiliate codes follow same discount validation logic (expiration, usage limits, single-code-per-booking rule)

- **FR-003 / Module P-03: Booking & Payment Processing**
  - **Why needed**: Affiliate code application occurs during patient booking checkout flow
  - **Integration point**: Patient platform sends discount code to booking service for validation and application

- **FR-001 / Module P-01: Patient Authentication & Profile Management**
  - **Why needed**: Track which patients used affiliate codes (without exposing patient identity to affiliate)
  - **Integration point**: Booking records link patient ID to affiliate code for internal tracking (anonymized in affiliate dashboard)

### External Dependencies (APIs, Services)

- **External Service 1: Stripe Payment API (or equivalent payment gateway)**
  - **Purpose**: Process affiliate commission payouts via bank transfer or PayPal
  - **Integration**: RESTful API calls to initiate transfers with affiliate bank account/PayPal details
  - **Failure handling**: If payout fails, system marks as "Failed" status and alerts admin for manual retry after resolving payment details

- **External Service 2: Email Service Provider (e.g., SendGrid)**
  - **Purpose**: Send payout confirmation emails and discount code notifications to affiliates
  - **Integration**: SMTP or API-based email sending with templated messages
  - **Failure handling**: If email fails, system logs error and admin can manually resend via dashboard

- **External Service 3: PDF Generation Library (e.g., wkhtmltopdf, Puppeteer)**
  - **Purpose**: Generate downloadable performance reports and payout receipts for affiliates
  - **Integration**: Server-side PDF generation from HTML templates
  - **Failure handling**: If PDF generation fails, system displays HTML version and allows manual retry

### Data Dependencies

- **Entity 1: Active Affiliate Accounts**
  - **Why needed**: Cannot create discount codes or process payouts without onboarded affiliate accounts
  - **Source**: Admin creates affiliate accounts via Affiliate Management module

- **Entity 2: Completed Bookings with Payment Confirmation**
  - **Why needed**: Affiliate commissions calculated only for completed bookings where patient has paid in full
  - **Source**: Booking & Payment Processing module (FR-003) provides booking completion events

- **Entity 3: Discount Code Catalog**
  - **Why needed**: System must validate affiliate codes at checkout against active discount code database
  - **Source**: Admin creates discount codes linked to affiliate accounts

---

## Assumptions

### User Behavior Assumptions

- **Assumption 1**: Affiliates will check their dashboard at least once per week to monitor performance
- **Assumption 2**: Patients will correctly enter affiliate discount codes (uppercase/lowercase variations handled by system)
- **Assumption 3**: Affiliates prefer monthly payouts over weekly/bi-weekly schedules (fewer transactions, easier accounting)
- **Assumption 4**: Affiliates will primarily use code-based discounts (manual entry) rather than auto-apply links

### Technology Assumptions

- **Assumption 1**: Affiliates access dashboard via modern web browsers (Chrome, Safari, Firefox - last 2 versions)
- **Assumption 2**: Payment gateway supports batch payout processing for multiple affiliates simultaneously
- **Assumption 3**: Email service provider has 99.9%+ deliverability rate for transactional emails
- **Assumption 4**: Server infrastructure can handle up to 1000 discount code validation requests per minute during peak periods

### Business Process Assumptions

- **Assumption 1**: Hairline will manually vet and approve affiliate partners before onboarding (no self-service affiliate signup)
- **Assumption 2**: Affiliate commission structure will remain stable (5-25% of Hairline commission or £50-£200 fixed per booking)
- **Assumption 3**: Finance team will reconcile affiliate payouts within 48 hours of processing to detect errors
- **Assumption 4**: Affiliate program will not exceed 10% of Hairline's total commission revenue within first 12 months (cost control)

---

## Implementation Notes

### Technical Considerations

- **Architecture**: Affiliate module requires event-driven architecture to trigger commission calculations when bookings complete
- **Technology**: Discount code validation should use in-memory caching (Redis) to minimize database queries during checkout
- **Performance**: Commission calculation jobs should run asynchronously to avoid blocking booking confirmation workflow
- **Storage**: Audit trail requires append-only data storage for all affiliate transactions (no deletions, only inserts)

### Integration Points

- **Integration 1: Patient Booking Checkout → Affiliate Code Validation**
  - **Data format**: JSON payload with discount code, patient ID (anonymized), booking total
  - **Authentication**: Internal service-to-service API with JWT tokens
  - **Error handling**: If validation service unavailable, allow checkout to proceed without discount (prevent checkout failure)

- **Integration 2: Booking Completion Event → Commission Calculation**
  - **Data format**: Event payload with booking ID, affiliate code used, final payment amount, Hairline commission amount
  - **Authentication**: Internal event bus with message authentication
  - **Error handling**: If commission calculation fails, retry 3 times with exponential backoff; alert admin if all retries fail

- **Integration 3: Payout Processing → Payment Gateway API**
  - **Data format**: JSON payload with affiliate payment details (bank account/PayPal), payout amount, transaction metadata
  - **Authentication**: OAuth 2.0 or API key authentication with payment gateway
  - **Error handling**: If payment fails, mark as "Failed" status and alert admin; support manual retry after 24 hours

### Scalability Considerations

- **Current scale**: Expected 20-30 active affiliates at launch, 500-1000 code applications per month
- **Growth projection**: Plan for 100+ affiliates within 12 months, 10,000+ code applications per month
- **Peak load**: Handle 100 simultaneous discount code validations during promotional campaigns
- **Data volume**: Expect 50,000+ affiliate transaction records per year (code applications, commission calculations, payouts)
- **Scaling strategy**: Horizontal scaling of API services; database partitioning by affiliate ID for transaction history

### Security Considerations

- **Authentication**: Affiliates access dashboard via username/password; support MFA (optional) for high-value affiliates
- **Authorization**: Role-based access control (RBAC): Affiliates view only their own data; Admins view all affiliate data
- **Encryption**: All payment details (bank accounts, PayPal emails) encrypted at rest using AES-256; TLS 1.3 for data in transit
- **Audit trail**: Log all access to affiliate payment details with timestamp, user ID, and IP address
- **Threat mitigation**: Rate limiting on dashboard API (100 requests/minute/user) to prevent abuse; CAPTCHA on affiliate login after 3 failed attempts
- **Compliance**: PCI-DSS compliance for handling affiliate bank account details; GDPR compliance for affiliate personal data (right to deletion)

---

## User Scenarios & Testing

### User Story 1 - Affiliate Onboarding and First Code Creation (Priority: P1)

Admin onboards new affiliate partner, creates discount code, and affiliate accesses dashboard to view initial setup.

**Why this priority**: Core functionality required for affiliate program to launch; without this, no affiliates can join or promote platform.

**Independent Test**: Can be fully tested by creating affiliate account, generating discount code, and verifying affiliate receives login credentials and can access dashboard.

**Acceptance Scenarios**:

1. **Given** admin is logged into admin dashboard, **When** admin navigates to Affiliate Management and clicks "Add New Affiliate", **Then** system displays affiliate onboarding form with all required fields
2. **Given** admin fills affiliate details (name, email, payment method, commission structure), **When** admin submits form, **Then** system creates affiliate account and sends login credentials to affiliate email within 2 minutes
3. **Given** affiliate account is created, **When** admin creates discount code linked to affiliate, **Then** system validates code uniqueness and saves code with "Active" status
4. **Given** discount code is created, **When** affiliate logs into dashboard using credentials, **Then** system displays affiliate dashboard with discount code details and "0 referrals" initial state

---

### User Story 2 - Patient Applies Affiliate Code at Checkout (Priority: P1)

Patient discovers affiliate discount code, applies it during booking checkout, and receives discounted price.

**Why this priority**: Core user journey that drives affiliate referrals and patient conversions; essential for MVP.

**Independent Test**: Can be tested by creating test affiliate code, simulating patient checkout, and verifying discount is applied correctly.

**Acceptance Scenarios**:

1. **Given** patient is at booking checkout with £1000 total, **When** patient enters valid affiliate code "PARTNER10" (10% discount), **Then** system validates code and applies £100 discount (total becomes £900)
2. **Given** patient applies affiliate code, **When** patient completes payment, **Then** system records booking with affiliate code and triggers commission calculation for affiliate
3. **Given** patient attempts to apply expired affiliate code, **When** system validates code, **Then** system displays error message "This discount code is no longer valid" and checkout proceeds without discount
4. **Given** patient applies affiliate code that reached usage limit, **When** system validates code, **Then** system displays error message and prevents code application

---

### User Story 3 - Affiliate Views Real-Time Performance Dashboard (Priority: P2)

Affiliate logs into dashboard to check referral count, commission earnings, and upcoming payout details.

**Why this priority**: Critical for affiliate engagement and transparency; affiliates need visibility into earnings to stay motivated.

**Independent Test**: Can be tested by creating affiliate account with simulated referrals and verifying dashboard displays accurate statistics.

**Acceptance Scenarios**:

1. **Given** affiliate has 10 completed referrals generating £5000 total revenue, **When** affiliate logs into dashboard, **Then** system displays accurate statistics: 10 referrals, £5000 revenue, £750 commission earned (15% of Hairline commission)
2. **Given** affiliate has pending payout of £750, **When** affiliate views dashboard, **Then** system displays "Next payout: £750 on December 7, 2025"
3. **Given** affiliate has multiple discount codes, **When** affiliate clicks on individual code, **Then** system displays per-code breakdown: usage count, conversion rate, revenue, commission earned
4. **Given** affiliate wants performance report, **When** affiliate clicks "Download Report", **Then** system generates PDF report with all-time statistics and payout history

---

### User Story 4 - Admin Processes Monthly Affiliate Payouts (Priority: P1)

Admin reviews automatically generated payout list on 7th of month and processes batch payouts to all affiliates.

**Why this priority**: Core admin workflow required to fulfill affiliate commission obligations; without this, affiliates won't be paid.

**Independent Test**: Can be tested by triggering monthly payout job and verifying payouts are calculated correctly and processed successfully.

**Acceptance Scenarios**:

1. **Given** it is December 7th, 2025, **When** automated payout job runs, **Then** system generates payout list for all affiliates with completed bookings in November 2025
2. **Given** payout list displays 5 affiliates owed total £3500, **When** admin clicks "Process Batch Payout", **Then** system initiates payment gateway API calls to transfer funds to each affiliate's bank account/PayPal
3. **Given** payout processing completes successfully, **When** payment gateway confirms transactions, **Then** system marks all payouts as "Paid" and sends confirmation emails to affiliates with transaction details
4. **Given** one payout fails due to invalid bank account, **When** payment gateway returns error, **Then** system marks that payout as "Failed" and alerts admin with error message for manual resolution

---

### User Story 5 - Affiliate Commission Calculation for Completed Booking (Priority: P1)

System automatically calculates affiliate commission when patient completes booking using affiliate code.

**Why this priority**: Core business logic that ensures affiliates are credited correctly; must be accurate to maintain trust.

**Independent Test**: Can be tested by simulating booking completion with affiliate code and verifying commission calculation matches expected formula.

**Acceptance Scenarios**:

1. **Given** patient books £1000 treatment using affiliate code "PARTNER10" (10% discount), **When** patient completes payment of £900, **Then** system calculates Hairline commission (15% of £1000 = £150) and affiliate commission (15% of £150 = £22.50)
2. **Given** affiliate has fixed commission structure of £50 per booking, **When** patient completes booking using affiliate code, **Then** system credits affiliate account with £50 commission regardless of booking value
3. **Given** booking is completed with affiliate code, **When** commission calculation completes, **Then** system updates affiliate dashboard with new referral count and commission earned in real-time
4. **Given** patient refunds booking after completion, **When** refund is processed, **Then** system reverses affiliate commission and deducts £22.50 from affiliate's pending payout

---

### User Story 6 - Admin Edits Affiliate Commission Structure Mid-Program (Priority: P2)

Business negotiates new commission terms with affiliate; admin updates commission structure with effective date.

**Why this priority**: Important for business flexibility and affiliate relationship management; not required for MVP but needed for scaling.

**Independent Test**: Can be tested by editing affiliate commission structure and verifying new rates apply only to future bookings.

**Acceptance Scenarios**:

1. **Given** affiliate currently has 15% commission rate, **When** admin edits commission structure to 20% with effective date December 1, 2025, **Then** system saves new rate and applies to bookings completed on/after December 1st
2. **Given** affiliate has pending payout for November 2025 bookings, **When** admin changes commission rate in December, **Then** November payout is calculated using old 15% rate (no retroactive changes)
3. **Given** commission structure is updated, **When** system sends notification to affiliate, **Then** email includes old rate, new rate, and effective date for transparency
4. **Given** admin sets effective date in past, **When** system validates edit, **Then** system displays error: "Effective date cannot be in the past" and prevents save

---

### Edge Cases

- What happens when **affiliate has £45 pending payout (below £50 minimum threshold)**? System does NOT process payout; commission rolls over to next month until threshold is reached.
- How does system handle **duplicate discount codes across different affiliates**? System validates uniqueness across ALL affiliates; if code exists, displays error "Code already exists for affiliate [name]".
- What occurs if **patient applies affiliate code but cancels booking before payment**? System tracks code as "applied" but NOT "completed"; no commission credited to affiliate.
- How to manage **affiliate account suspension while pending payout exists**? Pending commission is held pending investigation; if suspension is lifted, payout processes normally; if permanent ban, pending commission is forfeited.
- What happens when **payment gateway API is down during payout processing**? System retries 3 times with exponential backoff; if all retries fail, marks payouts as "Failed" and alerts admin to retry manually next day.
- How does system handle **booking refund after affiliate payout has been processed**? System tracks negative balance for affiliate; deducts refunded commission from next payout (if next payout insufficient, carries negative balance forward).

---

## Functional Requirements Summary

### Core Requirements

- **FR-001**: System MUST allow admins to onboard affiliates with unique email, payment method, and commission structure (percentage or fixed amount)
- **FR-002**: System MUST generate unique affiliate discount codes with configurable parameters (discount amount, expiration date, usage limits)
- **FR-003**: System MUST validate affiliate discount codes at patient checkout and apply discount from Hairline's commission (not provider payout)
- **FR-004**: System MUST track discount code applications separately as "applied" (code entered) and "completed" (booking paid)
- **FR-005**: System MUST calculate affiliate commission automatically when booking completes with payment confirmation
- **FR-006**: System MUST provide affiliates with real-time dashboard showing referral count, revenue generated, commission earned, and pending payout
- **FR-007**: System MUST generate monthly payout list automatically on 7th of each month for previous month's completed bookings
- **FR-008**: System MUST integrate with payment gateway to process affiliate commission payouts via bank transfer or PayPal
- **FR-009**: System MUST send payout confirmation emails to affiliates with transaction details within 24 hours of payment processing
- **FR-010**: System MUST enforce single discount code per booking rule (priority: Patient code > Provider code > Affiliate code)

### Data Requirements

- **FR-011**: System MUST maintain affiliate account records with contact details, payment information (encrypted), commission structure, and status
- **FR-012**: System MUST link discount codes to affiliate accounts with one-to-many relationship (one affiliate can have multiple codes)
- **FR-013**: System MUST store booking records with affiliate code reference for commission tracking
- **FR-014**: System MUST maintain payout history with transaction ID, date, amount, status for minimum 7 years (audit compliance)

### Security & Privacy Requirements

- **FR-015**: System MUST encrypt affiliate payment details (bank accounts, PayPal emails) at rest using AES-256
- **FR-016**: System MUST mask affiliate payment details in UI (display last 4 characters only)
- **FR-017**: System MUST anonymize patient identity in affiliate dashboard (affiliates see only aggregated statistics, not patient names)
- **FR-018**: System MUST log all affiliate-related transactions (code usage, commission calculations, payouts) with timestamp, user ID, and action type
- **FR-019**: System MUST require secure authentication for affiliate dashboard access (username/password with optional MFA)

### Integration Requirements

- **FR-020**: System MUST expose API for discount code validation during patient checkout (response time <500ms)
- **FR-021**: System MUST integrate with payment gateway API to initiate affiliate payouts (bank transfer or PayPal)
- **FR-022**: System MUST integrate with email service provider to send affiliate notifications (onboarding, payouts, code creation)
- **FR-023**: System MUST emit booking completion events to trigger affiliate commission calculation asynchronously

---

## Key Entities

- **Entity 1 - Affiliate Account**
  - **Key attributes**: Affiliate ID (unique), Name, Contact Email (unique), Payment Method (Bank Transfer/PayPal), Payment Details (encrypted), Commission Type (Percentage/Fixed), Commission Value, Payout Schedule, Status (Active/Suspended/Inactive), Created Date
  - **Relationships**: One affiliate can have many discount codes; one affiliate can have many payouts; one affiliate can be linked to many bookings (via discount codes)

- **Entity 2 - Discount Code**
  - **Key attributes**: Code ID (unique), Code Text (unique, case-insensitive), Linked Affiliate ID (foreign key), Discount Type (Hairline Fees Only), Discount Amount Type (Percentage/Fixed), Discount Value, Application Method (Auto-apply/Code-based), Expiration Date (optional), Max Usage Count (optional), Current Usage Count, Status (Active/Inactive), Created Date
  - **Relationships**: One code belongs to one affiliate; one code can be applied to many bookings

- **Entity 3 - Booking with Affiliate Code**
  - **Key attributes**: Booking ID (unique), Patient ID (anonymized in affiliate views), Affiliate Code Used (foreign key), Booking Total, Discount Applied, Hairline Commission, Affiliate Commission Owed, Booking Status (Pending/Completed/Refunded), Completion Date
  - **Relationships**: One booking links to one affiliate code (if used); one booking belongs to one patient; one booking contributes to one payout

- **Entity 4 - Affiliate Payout**
  - **Key attributes**: Payout ID (unique), Affiliate ID (foreign key), Payout Month, Total Bookings Count, Total Commission Amount, Payment Method, Transaction ID (from payment gateway), Payout Date, Status (Pending/Processing/Paid/Failed), Admin Notes (internal), Created Date
  - **Relationships**: One payout belongs to one affiliate; one payout summarizes many bookings; one payout generates one transaction via payment gateway

- **Entity 5 - Affiliate Transaction Log (Audit Trail)**
  - **Key attributes**: Log ID (unique), Affiliate ID (foreign key), Action Type (Code Created, Code Applied, Commission Calculated, Payout Processed, etc.), Timestamp, User ID (admin or system), IP Address, Metadata (JSON with action details)
  - **Relationships**: One log entry belongs to one affiliate; many log entries track lifecycle of affiliate account

---

## Appendix: Change Log

| Date       | Version | Changes                                  | Author        |
|------------|---------|------------------------------------------|---------------|
| 2025-11-12 | 1.0     | Initial PRD creation for FR-018          | Claude (AI)   |

---

## Appendix: Approvals

| Role            | Name   | Date | Signature/Approval |
|-----------------|--------|------|--------------------|
| Product Owner   | [Name] | TBD  | Pending            |
| Technical Lead  | [Name] | TBD  | Pending            |
| Finance Lead    | [Name] | TBD  | Pending            |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-017 Admin Billing & Financial Management PRD
**Last Updated**: 2025-11-12
