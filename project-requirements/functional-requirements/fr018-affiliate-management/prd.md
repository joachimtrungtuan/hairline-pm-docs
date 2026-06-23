# FR-018 - Affiliate Management

**Module**: A-07: Affiliate Program Management
**Feature Branch**: `fr018-affiliate-management`
**Created**: 2025-11-12
**Status**: ✅ Verified & Approved
**Source**: FR-018 from system-prd.md, Hairline-AdminPlatform-Part1.txt (lines 125-409)

---

## Executive Summary

The Affiliate Management module enables Hairline to partner with external entities (influencers, clinics, organizations) who promote the platform in exchange for commission-based compensation. This module provides the infrastructure for onboarding affiliates, generating unique affiliate-bound promo codes, bulk-generating distinct codes for selected or filtered affiliate groups, monitoring referral performance, calculating commissions, and exposing monthly payout-cycle data to FR-017 / A-05 for execution. By creating a scalable affiliate program, Hairline can expand market reach, increase patient acquisition, and drive revenue growth through trusted third-party channels while maintaining full transparency and control over partnership economics.

**Key Value Proposition**:

- **For Affiliates**: Easy-to-use dashboard with real-time tracking of referrals, earnings, and payout history
- **For Admins**: Streamlined affiliate onboarding, bulk affiliate code generation, automated commission tracking, and simplified monthly payout-cycle review/handoff
- **For Business**: Cost-effective patient acquisition channel with performance-based compensation model

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-03)**: Patients apply affiliate discount codes at checkout to receive promotional offers
- **Provider Platform (PR-05)**: No direct provider interaction; providers see bookings with affiliate codes applied
- **Admin Platform (A-07)**: Full affiliate lifecycle management including onboarding, code creation, commission tracking, payout-cycle calculation, and read-only payout status/history
- **Affiliate Portal (scoped surface of A-07 / Admin tenant)**: External affiliate-facing self-service surface (Screens 9–10: dashboard, promo codes, payouts, profile, activation). Per the platform constitution (Principle I — Multi-Tenant Architecture), this is a **scoped external surface operated within the Admin Platform tenant boundary — not a separate tenant** — with its own authentication/authorization scope and affiliate-only data access
- **Shared Services (S-02 / S-03 / S-06)**: Payment Processing Service executes affiliate commission transfers when invoked by FR-017 / A-05; Notification Service sends payout confirmations; Audit Log Service records affiliate-related events

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
- **Discount Code Management**: Generate unique affiliate discount codes for one affiliate or bulk-generate one distinct code per affiliate for selected or filtered affiliate groups
- **Performance Tracking**: View real-time statistics on referral counts, booking conversions, revenue generated per affiliate
- **Commission Calculation**: System automatically calculates affiliate commissions based on completed bookings
- **Payout Data Handoff**: Monthly commission cycle calculation and read-only payout status/history; payout approval and Stripe transfer execution are owned by FR-017 / A-05
- **Reporting**: Generate affiliate performance reports for analysis and optimization

**Shared Services (S-02 / S-03 / S-06)**:

- **Payment Processing Service**: Executes affiliate commission payouts as Stripe transfers when invoked by FR-017 / A-05 (consistent with provider payouts)
- **Notification Service**: Sends payout confirmation emails to affiliates with transaction details
- **Audit Trail Service**: Logs all affiliate-related transactions (code usage, commission calculations, payouts)

### Communication Structure

**In Scope**:

- Email notifications to affiliates when discount codes are created or updated
- Email notifications to affiliates when monthly payouts are processed
- Admin-to-affiliate communication via notes in admin dashboard (internal only)
- System-generated payout confirmations with transaction breakdown
- Read-only access to externally hosted affiliate marketing materials (banners, templates, and campaign assets) from the affiliate portal

**Out of Scope**:

- Direct messaging between patients and affiliates (handled outside platform)
- Marketing material creation or asset hosting (affiliates use externally hosted materials linked from the portal)
- Affiliate training or onboarding calls (manual process outside platform)

### Entry Points

- **Admin-initiated**: Admins access Affiliate Management section in admin dashboard to onboard new affiliates
- **Admin bulk action**: Admins select affiliates manually or through filters, then generate one unique affiliate-bound promo code per selected affiliate
- **Affiliate-initiated**: After the admin creates their account, affiliates complete a one-time activation link to set their password, then log into the dedicated affiliate portal to view their performance dashboard
- **Patient-triggered**: Patients enter affiliate codes during booking checkout, triggering tracking and commission calculation
- **System-scheduled**: Automated monthly job generates payout reports on the 7th of each month (fixed schedule)

---

## Business Workflows

### Main Flow: Affiliate Onboarding and Code Creation

**Actors**: Admin, System, Affiliate
**Trigger**: Admin decides to partner with new affiliate organization
**Outcome**: Affiliate account created, unique discount code generated, affiliate completes activation and is granted access to dashboard

**Steps**:

1. Admin navigates to Admin Dashboard > Affiliate Management > Add New Affiliate
2. Admin enters affiliate details:
   - Affiliate name (organization/individual name)
   - Contact email (for login and payout notifications)
   - Bank account details for payouts (account holder name, bank name, account number, routing/SWIFT code, optional IBAN) — mirroring the provider bank details collected in FR-032; payouts are executed as Stripe transfers
   - Commission structure (percentage of booking revenue OR fixed amount per booking)
   - Payout schedule (fixed: monthly on the 7th — not configurable, per business policy)
3. System validates inputs (unique email, valid payment details format)
4. Admin submits affiliate onboarding form
5. System creates affiliate account with:
   - Generated unique affiliate ID
   - Initial status: "Pending" (account created, password not yet set); status flips to "Active" automatically once the affiliate completes the set-password activation step
   - A secure one-time activation link (set-password link, expires in 24 hours) sent to the affiliate's contact email — raw login credentials are never emailed
   - This mirrors the provider activation flow (FR-015) so onboarding behaves consistently across roles of the same nature
6. Admin creates discount code for affiliate:
   - Discount code name (e.g., "WINTER2025", "PARTNER10")
   - Discount type: Hairline fees only (deducted from Hairline's commission)
   - Discount amount: Percentage (e.g., 10%) OR fixed amount (e.g., $50)
   - Expiration date (optional)
   - Maximum usage count (optional, e.g., first 200 users)
   - Auto-apply vs. code-based (manual entry required)
7. System validates discount code (uniqueness, valid parameters)
8. System saves discount code and links to affiliate account
   - Each affiliate-bound code links to exactly one affiliate account
   - Shared codes across multiple affiliates are not supported because payout attribution must remain unambiguous
9. System sends the activation email to the affiliate containing:
   - Welcome message and platform introduction
   - Secure one-time "Set Password" link (expires in 24 hours)
   - The affiliate's contact email (used as the login username)
   - Instructions for first login and profile completion
10. Affiliate clicks the "Set Password" link; system displays the password creation form (strong password required: min 12 chars, uppercase, lowercase, number, special char)
11. Affiliate sets and confirms password; system validates strength, saves the encrypted password, and redirects to the Affiliate Portal login
12. Affiliate logs in and lands on the Affiliate Portal (Overview tab), where assigned discount code(s), commission structure, and payout schedule are shown; affiliate can review real-time stats and complete non-sensitive fields on the Profile tab

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

**A4: Bulk Affiliate Code Generation for Filtered Group**

- **Trigger**: Admin wants to launch an affiliate campaign for a selected affiliate group (e.g., all active affiliates in one country, all affiliates matching a performance tier, or a manually selected set)
- **Steps**:
  1. Admin opens Affiliate Management Dashboard
  2. Admin filters affiliates by criteria such as status, country/region, affiliate type, language, performance tier, campaign eligibility, or payout setup completeness
  3. Admin reviews the resulting affiliate list and selects all or specific affiliates
  4. Admin clicks "Generate Codes"
  5. Admin enters campaign-level code settings:
     - Campaign name
     - Code prefix or naming pattern
     - Discount amount type and value
     - Active date window
     - Total usage cap per generated code
     - Per-patient usage limit
     - Application method (code-based or auto-apply link)
  6. System generates one distinct unique promo code for each selected affiliate
  7. System validates every generated code against platform-wide uniqueness rules
  8. System links each generated code to exactly one affiliate account
  9. System publishes active codes to the corresponding affiliate dashboards and sends code-created notifications
- **Outcome**: Admin launches one campaign across many affiliates without creating a shared affiliate code; each affiliate receives their own trackable code under the same campaign settings

**A5: Affiliate Activation & Resend**

- **Trigger**: Affiliate did not receive the activation email, it went to spam, or the one-time set-password link expired (24 hours passed)
- **Steps**:
  1. Affiliate navigates to the Affiliate Portal login page
  2. Affiliate clicks "Didn't receive activation email?" below the login form
  3. System displays a resend form with an email address field
  4. Affiliate enters the email address the admin used during account creation
  5. Affiliate clicks "Resend Activation Email"
  6. System validates the email exists and the account is created but not yet activated (password not set)
  7. System generates a fresh one-time set-password link (expires in 24 hours) and invalidates the previous link
  8. System sends the new activation email and displays: "Activation email sent! Please check your inbox (and spam folder). The link expires in 24 hours."
  9. Affiliate completes password setup (Main Flow steps 10-12)
- **Outcome**: Affiliate receives a valid activation link and can complete password setup
- **Business Rules**:
  - Rate limited to 3 resend requests per hour per email address (prevents spam)
  - Previous activation links are invalidated when a new link is generated
  - If the email is not found or the account is already activated (password already set), system displays a generic message: "If an account exists with this email, an activation link will be sent." (security: do not reveal whether the email exists)
  - Admin can also resend the activation email from the Affiliate Detail screen (button: "Resend Activation Email"), mirroring FR-015

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

**B2: Payout Processing Failure (from FR-017 Execution)**

- **Trigger**: FR-017 / A-05 monthly payout execution encounters payment processing error using FR-018 affiliate commission data (invalid bank account, insufficient funds in Hairline account, etc.)
- **Steps**:

  1. FR-018 calculates commissions owed to each affiliate based on completed bookings from previous month
  2. FR-018 exposes the payout cycle data and readiness status to FR-017 / A-05
  3. FR-017 / A-05 attempts to process the payout as a Stripe transfer to the affiliate's bank account
  4. Stripe returns a transfer error (e.g., "Invalid bank account number")
  5. System logs error with affiliate ID, amount, and error message
  6. FR-017 marks payout as "Failed"; FR-018 displays the failed status in read-only payout views
  7. System sends alert notification to admin team with failed payout details
  8. Admin reviews error and contacts affiliate to resolve payment details
  9. Admin manually triggers retry from FR-017 once payment details corrected
  10. FR-017 re-processes payment and FR-018 displays "Paid" upon success
- **Outcome**: Failed payouts are flagged for admin review in A-05 and visible in FR-018 read-only history; manual intervention resolves payment issues; affiliate receives delayed payout with explanation

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
  8. System retains historical data (referrals, commissions, payouts) but prevents new activity (audit trail retained 10 years; financial records 7 years minimum)
  9. Pending unpaid commissions are held pending investigation
  10. Admin can reinstate account later by changing status to "Active"
- **Outcome**: Affiliate account suspended; discount codes deactivated; pending payouts held; full audit trail maintained

**B4: Bulk Code Generation Partial Failure**

- **Trigger**: Bulk code generation succeeds for some affiliates but fails for others (e.g., duplicate generated code, inactive affiliate, incomplete payout setup, email notification failure)
- **Steps**:
  1. System completes generation for valid affiliates
  2. System skips failed affiliates and records the failure reason per affiliate
  3. System displays a generation summary: created count, skipped count, and failed count
  4. Admin downloads or views the failed-row list
  5. Admin fixes the cause and retries only failed affiliates
- **Outcome**: Valid affiliate codes are not blocked by unrelated failures; admin has a clear retry path with no duplicate code creation

**B5: Affiliate Offboarding / Deactivation (End of Partnership)**

- **Trigger**: The partnership ends voluntarily or by mutual decision (affiliate leaves the program, contract not renewed, business closes). This is distinct from B3 Suspension: **Suspension is temporary/punitive and reversible with the balance held pending investigation; Deactivation (Inactive) is a permanent terminal state with final settlement.**
- **Actors**: Admin, System
- **Steps**:
  1. Admin navigates to the affiliate profile (Screen 3) and clicks "Deactivate / Offboard"
  2. System opens Screen 3.3 (Deactivate / Offboard Affiliate) and requires a reason (required field)
  3. Admin reviews the final-settlement summary the system computes: gross pending commission, minus any reversals/refunds, equals the net final balance
  4. System applies terminal settlement rules:
     - **If net final balance ≥ the minimum payout threshold ($50)**: the balance is queued for settlement in the next scheduled payout run (or an admin-initiated final payout), executed as a Stripe transfer like any other payout
     - **If net final balance is below the threshold ($50)**: the residual is **forfeited** on deactivation (it can no longer roll over because there will be no future earning months), recorded with an audit entry
     - **If net final balance is negative** (reversals exceed accrued commission, per Issue #8): the unrecoverable negative balance is **written off** on deactivation with an audit entry, since there are no future payouts to net it against
  5. Admin confirms; system sets affiliate `Status: Inactive`
  6. System disables all of the affiliate's discount codes (invalid at checkout), consistent with suspension
  7. System converts the affiliate's portal access to **read-only**: the affiliate can still log in to view historical performance, codes, and payout history, but cannot transact or trigger any new activity
  8. System retains all historical data (referrals, commissions, payouts, audit trail); the audit trail is retained 10 years and financial/payout records 7 years minimum
  9. System sends the affiliate an offboarding notification (with final-settlement outcome) and records the action in the audit log
- **Outcome**: Affiliate moved to the terminal Inactive state with codes disabled, final balance settled / forfeited / written off explicitly, portal access read-only, and a complete audit trail. Reinstating an Inactive affiliate is **not** the normal path; if a partnership resumes, the admin re-onboards (new activation) rather than silently reactivating, to keep settlement boundaries clean.

---

## Screen Specifications

> **Tenant scope**:
>
> - **Admin Platform (A-07)**: Screens 1-8 below, including sub-screens 3.1, 3.2, 3.3, and 4.1. Admin-facing affiliate onboarding, affiliate detail, suspend/reinstate and deactivate/offboard, code generation, system-wide promo code management, payout-cycle calculation/status review, and billing/audit handoff.
> - **Affiliate Platform**: Screen 9 below, with one screen per tab (9.1 Overview, 9.2 Promo Codes, 9.3 Payouts, 9.4 Profile) for assigned codes, referrals, earnings, payout status, and self-service profile; plus Screen 10 (with 10.1 Set Password, 10.2 Resend Activation, 10.3 Welcome / Get Started) for affiliate account onboarding/activation, mirroring the provider activation flow (FR-015).
> - **Patient Platform**: No patient-facing screens in this FR. Patient checkout code entry and validation are governed by FR-007 and FR-019.
> - **Provider Platform**: No provider-facing affiliate management screens in this FR. Provider-facing financial/payment visibility remains governed by FR-017 and related provider dashboard FRs.
>
> **Sub-screen notation**: Modals and tab screens use the parent screen's number with a decimal suffix (e.g., Screen 3.1 is a modal launched from Screen 3; Screen 9.1 is the first tab of the Screen 9 portal), consistent with the convention used in other FRs (e.g., FR-033).
>
> **Shared detail screens**: Screen 6 (Promo Code Detail) and Screen 8 (Payout / Transaction Detail) are each a single shared screen reached from two entry points — the global management list and the corresponding list inside Screen 3 (Affiliate Detail). Both entry points open the same screen with identical layout and capabilities.

---

### Admin Platform Screens (A-07)

#### Screen 1: Affiliate Management Dashboard (Overview)

**Purpose**: Provides admins with overview of all affiliates and their performance metrics, and the entry point into each affiliate's detail view

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Affiliate Name | text | Yes | Organization or individual name | Max 200 characters |
| Contact Email | email | Yes | Primary contact email for login and notifications | Valid email format, unique |
| Total Referrals | number | N/A | Count of all completed bookings with affiliate referral attribution (per Rule 11, attribution can be preserved separately from the final discount applied to price) | Read-only, system-calculated |
| Total Revenue | currency | N/A | Total booking value from affiliate referrals | Read-only, system-calculated |
| Total Commissions Paid | currency | N/A | Sum of all commissions paid to date | Read-only, system-calculated |
| Pending Payout | currency | N/A | Commission amount awaiting next payout cycle | Read-only, system-calculated |
| Status | select | Yes | Account status: Active, Suspended, Inactive (admin-selectable). "Pending" is a system-set initial state shown until activation and is not manually selectable | Admin dropdown: Active / Suspended / Inactive; Pending is read-only/system-set |
| Country/Region | select | No | Affiliate operating country or region | Uses supported country/region list |
| Affiliate Type | select | No | Influencer, clinic partner, organization, other | Dropdown with configured options |
| Performance Tier | status | N/A | System-calculated tier band (e.g., by revenue) | Read-only, system-calculated |
| Campaign Eligibility | status | N/A | Whether affiliate can receive bulk-generated codes | Read-only, system-calculated |
| Active Codes Count | number | N/A | Count of active codes assigned to affiliate | Read-only, system-calculated |
| Actions | buttons | N/A | View Details, Edit, Suspend, Generate Report | Context-dependent based on status |

**Business Rules**:

- **Sorting**: Default sort by "Total Revenue" descending (highest performers first)
- **Filtering**: Admin can filter by status, country/region, affiliate type, language, performance tier, campaign eligibility, and payout setup completeness; admin can also search by affiliate name/email
- **Pagination**: Display 25 affiliates per page with pagination controls
- **Quick Actions**: Inline "Generate Report" button exports affiliate performance to PDF
- **Status Indicators**: Color-coded status badges (Pending = amber, Active = green, Suspended = red, Inactive = gray)
- **Bulk Code Action**: Admin can select one or more affiliates from the filtered list and generate one distinct affiliate-bound code per selected affiliate

**Acceptance Criteria**:

1. Given admin opens Affiliate Management Dashboard, when the screen loads, then active, suspended, and inactive affiliates are listed with default Total Revenue descending sort and visible result count.
2. Given admin applies status, country/region, affiliate type, language, performance tier, campaign eligibility, and payout setup filters, then the list returns only affiliates matching all active filter types while multi-select values use OR within the same filter.
3. Given admin selects eligible affiliates from the filtered list, when admin clicks "Generate Codes", then Screen 4 (Affiliate Code Generation) opens in bulk mode with the selected affiliate count preserved.
4. Given admin selects ineligible affiliates, when admin clicks "Generate Codes", then system blocks or excludes those rows and displays the specific eligibility reason.
5. Given admin clicks "View Details" on an affiliate row, when the action fires, then Screen 3 (Affiliate Detail) opens for that affiliate.

**Notes**:

- Use data tables with sortable columns for easy performance comparison
- Highlight affiliates with pending payouts > $1000 with yellow background
- Show last payout date in tooltip on hover over "Total Commissions Paid"
- Bulk code generation should be available only after at least one eligible active affiliate is selected
- "View Details" opens Screen 3 (Affiliate Detail); "Edit" opens Screen 2; "Suspend" opens Screen 3.1 (Suspend / Reinstate)

---

#### Screen 2: Add/Edit Affiliate Form

**Purpose**: Allows admins to create new affiliate accounts or edit existing affiliate details

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Affiliate Name | text | Yes | Full name of organization or individual | Max 200 characters, no special characters |
| Contact Email | email | Yes | Email for login and notifications | Valid email format, unique across affiliates |
| Phone Number | tel | No | Contact phone with country code | Valid international phone format |
| Language(s) | multi-select | No | Spoken/operating language(s) for the affiliate | At least one if set; uses supported language list |
| Country/Region | select | No | Affiliate operating country or region | Uses supported country/region list |
| Affiliate Type | select | No | Influencer, clinic partner, organization, other | Dropdown with configured options |
| Tax / VAT / Business Reg ID | text | No | Tax, VAT, or business-registration identifier | Max 50 chars; format validated per country if set |
| Account Holder Name | text | Yes | Name on the affiliate's bank account | Required, max 200 characters |
| Bank Name | text | Yes | Name of the affiliate's bank | Required, max 200 characters |
| Account Number | text | Yes | Affiliate bank account number | Required, format valid for selected country, masked in UI (last 4 digits), encrypted at rest |
| Routing / SWIFT Code | text | Yes | Routing or SWIFT/BIC code | Required, SWIFT/routing format validated |
| IBAN | text | Conditional | IBAN where applicable | Valid IBAN format if provided |
| Commission Type | radio | Yes | Percentage of Booking Revenue OR Fixed Amount | One option must be selected |
| Commission Percentage | number | Conditional | % of booking revenue paid to affiliate | Required if "Percentage" selected, range 5-25% |
| Commission Fixed Amount | currency | Conditional | Fixed $ amount per completed booking | Required if "Fixed Amount" selected, min $50 |
| Payout Schedule | display | N/A | Monthly on the 7th (fixed) | Read-only; fixed schedule, not configurable |
| Performance Tier | status | N/A | System-calculated tier band (read-only) | Read-only, system-calculated, not admin-entered |
| Activation Status | status | N/A | Invited (password not set) / Active (password set) | Read-only, system-managed |
| Last Login | datetime | N/A | Timestamp of affiliate's last portal login | Read-only, system-recorded |
| Notes (Internal) | textarea | No | Admin notes about affiliate relationship | Max 1000 characters, not visible to affiliate |

**Business Rules**:

- **Email Uniqueness**: System validates email is not already registered as affiliate or admin user
- **Payment Masking**: Bank account number masked in UI after initial entry (show last 4 digits only) and encrypted at rest; S-02 validates bank-detail format on save (same handling as provider bank details in FR-032)
- **Stripe Payouts**: All affiliate payouts are executed as Stripe transfers to this bank account; there is no PayPal or other payout method (consistent with the rest of the system)
- **Commission Validation**: If percentage type, system calculates preview of commission for an example booking (e.g., "For a $1,000 booking at 15% of booking revenue, affiliate earns $150")
- **Default Values**: Payout schedule is fixed at "Monthly on the 7th" (not editable); commission type defaults to "Percentage"
- **Edit Restrictions**: Email cannot be changed after account creation (must create new account if email change needed)
- **Performance Tier**: Displayed read-only on edit; computed by the system (e.g., revenue band) and never set manually
- **Activation State**: On create, Status is "Pending" and Activation Status is "Invited" until the affiliate completes the set-password flow; completing it flips Status to "Active" and Activation Status to "Active" together (per Rule 12). An admin "Resend Activation Email" action is available while Activation Status is "Invited"

**Notes**:

- Collect the full bank-detail set (account holder name, bank name, account number, routing/SWIFT, optional IBAN), mirroring the provider billing details in FR-032; all payouts use Stripe transfers to this account (no PayPal)
- Display warning message if commission percentage > 20%: "High commission rate - please confirm business approval"
- Auto-save draft every 30 seconds to prevent data loss on accidental navigation away
- Commission changes on an existing affiliate are made via Screen 3.2 (Edit Commission Structure) so an effective date is captured

---

#### Screen 3: Affiliate Detail

**Purpose**: Single-affiliate workspace consolidating account details, assigned promo codes, and payout history/upcoming payout in one view. This is the per-affiliate hub admins land on from "View Details" on Screen 1.

**Layout**: Header (affiliate name, status badge, affiliate ID, type, country, activation status) + summary metric strip + sectioned/tabbed content panels below.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Affiliate Header | composite | N/A | Name, status badge, affiliate ID, type, country, activation status | Read-only, from affiliate record |
| Summary Metrics | composite | N/A | Total referrals, total revenue, commissions paid, pending payout, next payout date | Read-only, system-calculated |
| Account Details Panel | section | N/A | All Screen 2 fields in read view, with masked payment details | Read-only; "Edit" opens Screen 2 |
| Assigned Promo Codes List | list | N/A | Codes linked to this affiliate (code, campaign, status, applied/completed, conversion, revenue, commission) | Read-only; each row links to Screen 6 |
| Payout History List | list | N/A | Past payouts for this affiliate (month, amount, status, transaction ID, date) | Read-only; each row links to Screen 8 |
| Upcoming Payout Panel | section | N/A | Next payout amount, scheduled date, included completed bookings count | Read-only, system-calculated |
| Activity / Audit Panel | list | N/A | Chronological affiliate audit events (code created, commission calculated, payout processed, status change) | Read-only, append-only |
| Internal Notes | textarea | No | Admin notes about the affiliate (not visible to affiliate) | Max 1000 characters |
| Actions | buttons | N/A | Edit, Add New Discount Code, Generate Codes, Resend Activation Email, Suspend/Reinstate, Deactivate/Offboard, Generate Report | Context-dependent based on status |

**Business Rules**:

- **Single Source View**: All affiliate-scoped data (codes, payouts, audit) is read from the same records surfaced elsewhere; this screen aggregates, it does not duplicate
- **Shared Detail Navigation**: Selecting a promo code row opens Screen 6 (Promo Code Detail); selecting a payout row opens Screen 8 (Payout / Transaction Detail) — the same shared screens used from the global lists
- **Resend Activation**: "Resend Activation Email" is enabled only while Activation Status is "Invited" (password not yet set); it follows the A5 rate-limit and security rules
- **Status Actions**: "Suspend" / "Reinstate" open Screen 3.1 (temporary, reversible; suspension disables codes and holds pending payouts per B3). "Deactivate / Offboard" opens Screen 3.3 (permanent terminal Inactive state with final settlement per B5)
- **Commission Edits**: "Edit Commission Structure" opens Screen 3.2 (effective-date captured); historical commissions are never recalculated
- **Masking**: Payment details remain masked (last 4 digits) in the Account Details panel

**Acceptance Criteria**:

1. Given admin opens Affiliate Detail, when the screen loads, then the header, summary metrics, assigned codes, payout history, and upcoming payout for that affiliate are shown.
2. Given the affiliate has assigned codes, when admin clicks a code row, then Screen 6 (Promo Code Detail) opens for that code with the affiliate context preserved.
3. Given the affiliate has payouts, when admin clicks a payout row, then Screen 8 (Payout / Transaction Detail) opens for that payout.
4. Given the affiliate's Activation Status is "Invited", when admin clicks "Resend Activation Email", then a fresh one-time link is sent and the previous link is invalidated; when status is "Active", the action is disabled.
5. Given admin clicks "Suspend", when admin confirms in Screen 3.1 with a reason, then the affiliate is suspended, codes are disabled, and pending payouts are held.

**Notes**:

- Surface a clear "Invited — activation pending" indicator until first password set
- Order assigned codes by status then created date; allow quick filter by Active/Inactive/Expired
- Upcoming payout panel should show a tooltip listing the completed bookings contributing to it

---

#### Screen 3.1: Suspend / Reinstate Affiliate (Modal)

**Purpose**: Confirmation modal for changing an affiliate's status to Suspended (or back to Active), mirroring the FR-015 provider suspension pattern. Backs the B3 flow. Launched from Screen 1 ("Suspend") or Screen 3 ("Suspend"/"Reinstate").

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Action | display | N/A | Suspend or Reinstate (based on current status) | Read-only |
| Reason | textarea | Yes | Admin reason for suspension (required for suspend) | Min 20 chars, max 500 chars (suspend) |
| Confirm Checkbox | checkbox | Yes | "I confirm this action" | Must be checked to enable Submit |

**Business Rules**:

- **Suspension Effects**: On suspend, all of the affiliate's codes are disabled (invalid at checkout), pending unpaid commissions are held pending investigation, and historical data is retained
- **Reinstatement**: On reinstate, status returns to "Active"; held payouts resume per investigation outcome
- **Notification**: System emails the affiliate about suspension with the reason
- **Confirmation Gate**: "Submit" is disabled until the confirmation checkbox is checked (prevents accidental suspension)

**Acceptance Criteria**:

1. Given admin clicks "Suspend", when the modal opens, then a required reason field and a confirmation checkbox are shown and Submit is disabled until both are valid.
2. Given admin confirms suspension, then the affiliate status becomes "Suspended", codes are disabled, pending payouts are held, and a notification is sent.
3. Given a suspended affiliate, when admin reinstates, then status returns to "Active".

---

#### Screen 3.2: Edit Commission Structure (Modal)

**Purpose**: Modal to change an existing affiliate's commission with an effective date, ensuring no retroactive recalculation. Backs the A2 flow. Launched from Screen 2 or Screen 3.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Commission Type | radio | Yes | Percentage of Booking Revenue OR Fixed Amount | One option must be selected |
| Commission Percentage | number | Conditional | New % of booking revenue | Required if "Percentage", range 5-25% |
| Commission Fixed Amount | currency | Conditional | New fixed $ amount per booking | Required if "Fixed Amount", min $50 |
| Effective Date | date | Yes | Date the new structure applies from | Must be today or future (not in the past) |
| Confirm | checkbox | Yes | "I confirm this commission change" | Must be checked to enable Submit |

**Business Rules**:

- **Future-Only**: New rates apply only to bookings completed on/after the effective date; historical commissions are never recalculated
- **Past Date Blocked**: System rejects an effective date in the past with a clear error
- **Notification**: System emails the affiliate the old rate, new rate, and effective date
- **Audit**: Change is logged with admin user ID, timestamp, old and new values, and effective date

**Acceptance Criteria**:

1. Given admin edits commission and sets a future effective date, when saved, then the new rate applies only to bookings completed on/after that date.
2. Given admin sets an effective date in the past, then the system blocks the save with "Effective date cannot be in the past".
3. Given the change is saved, then the affiliate is notified with old rate, new rate, and effective date.

---

#### Screen 3.3: Deactivate / Offboard Affiliate (Modal)

**Purpose**: Confirmation modal to move an affiliate to the terminal **Inactive** state at the end of a partnership, with explicit final settlement. Backs the B5 flow. Launched from Screen 3 ("Deactivate / Offboard"). Distinct from Screen 3.1 (Suspend / Reinstate), which is temporary and reversible.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Reason | textarea | Yes | Admin reason for offboarding | Min 20 chars, max 500 chars |
| Final Balance Summary | display | N/A | Gross pending, reversals/refunds, and net final balance (USD), system-computed | Read-only |
| Settlement Outcome | display | N/A | System-determined: Pay final balance / Forfeit (below $50) / Write off (negative) | Read-only, system-calculated |
| Confirm Checkbox | checkbox | Yes | "I confirm this affiliate will be permanently deactivated" | Must be checked to enable Submit |

**Business Rules**:

- **Terminal State**: Sets `Status: Inactive`; this is a permanent end-of-partnership state, not a temporary hold
- **Final Settlement**: Net final balance ≥ $50 is queued for the next (or an admin-initiated final) payout; a residual below $50 is forfeited with an audit entry; a negative balance is written off with an audit entry (no future payouts exist to net against)
- **Code Disablement**: All of the affiliate's codes are disabled (invalid at checkout)
- **Portal Access**: Affiliate retains read-only portal access (historical views only); no new activity is possible
- **Data Retention**: Historical referrals, commissions, payouts, and audit trail are retained for the audit-retention period
- **No Silent Reactivation**: An Inactive affiliate is not reinstated via Screen 3.1; resuming a partnership requires re-onboarding (new activation)
- **Confirmation Gate**: "Submit" is disabled until the reason is valid and the confirmation checkbox is checked

**Acceptance Criteria**:

1. Given admin clicks "Deactivate / Offboard", when the modal opens, then the reason field, the system-computed final balance summary, and the settlement outcome are shown and Submit is disabled until the reason and checkbox are valid.
2. Given a net final balance ≥ $50, when admin confirms, then the balance is queued for final payout, the affiliate becomes Inactive, codes are disabled, portal access becomes read-only, and an offboarding notification is sent.
3. Given a net final balance below $50, when admin confirms, then the residual is forfeited with an audit entry and the affiliate becomes Inactive.
4. Given a negative net balance, when admin confirms, then the negative balance is written off with an audit entry and the affiliate becomes Inactive.

---

#### Screen 4: Affiliate Code Generation

**Purpose**: Creation tool for affiliate-bound discount codes for one affiliate, a manually selected set of affiliates, or a filtered affiliate segment. FR-018 owns affiliate-specific code generation and assignment; FR-019 owns the shared promotion validation, redemption, and applied/completed lifecycle. (System-wide browsing of existing codes lives on Screen 5; per-code detail lives on Screen 6.)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Linked Affiliate | select | Conditional | Affiliate account this code belongs to (Single mode) | Dropdown of active affiliates; required in Single mode |
| Generation Mode | radio | Yes | Single Affiliate / Selected Affiliates / Filtered Segment | One option must be selected |
| Affiliate Selection | multi-select | Conditional | Affiliates receiving generated codes | Required for Selected Affiliates mode |
| Filter Criteria | filter set | Conditional | Saved filter used to generate codes for a segment | Required for Filtered Segment mode |
| Campaign Name | text | Yes | Internal campaign name shared across generated codes | 3-120 characters |
| Code Pattern | text | Conditional | Prefix/suffix pattern used for generated codes | Uppercase alphanumeric pattern, uniqueness checked |
| Discount Code | text | Conditional | Unique code patients enter at checkout (Single mode) | Uppercase alphanumeric, 4-20 chars, unique; required in Single mode |
| Discount Type | select | Yes | Hairline Fees Only (deducted from platform commission) | Currently only one option (future: Both Fees) |
| Discount Amount Type | radio | Yes | Percentage OR Fixed Amount | One option must be selected |
| Discount Percentage | number | Conditional | % discount applied to booking total | Required if "Percentage" selected, range 5-30% |
| Discount Fixed Amount | currency | Conditional | Fixed $ discount applied to booking | Required if "Fixed Amount" selected, min $10 |
| Application Method | radio | Yes | Auto-apply OR Code-based (manual entry) | One option must be selected |
| Expiration Date | date | No | Date after which code is no longer valid | Must be future date if set |
| Maximum Usage Count | number | No | Max number of **completed (paid)** redemptions per generated code (applied-but-abandoned checkouts do not count) | Min 1 if set, unlimited if blank |
| Per-Patient Usage Limit | number | No | Max completed redemptions per patient for this code | Default 1 |
| Status | toggle | Yes | Active (enabled) / Inactive (disabled) | Toggle switch, default Active |

**Business Rules**:

- **Code Uniqueness**: System validates discount code is unique across all affiliates (case-insensitive check)
- **One Affiliate Per Code**: Every affiliate-bound code belongs to exactly one affiliate; the same affiliate payout code cannot be assigned to multiple affiliates
- **Bulk Generation**: Bulk generation creates one distinct unique code per selected affiliate using the same campaign settings
- **Bulk Filter Snapshot**: System records the selected affiliates at generation time; later filter membership changes do not retroactively add or remove codes
- **Code Format**: System automatically converts code to uppercase on save
- **Expiration Logic**: If expiration date set, system automatically deactivates code at midnight (UTC) on that date
- **Usage Limit**: The usage cap counts **"completed" (paid) redemptions only**; once completed redemptions reach the maximum, the system automatically deactivates the code. "Applied" (entered-but-not-paid) events never consume the cap; a separate soft rate limit on applied events guards against application spam (Rule 13)
- **Generation Outcome**: On submit, Selected Affiliates and Filtered Segment modes open Screen 4.1 (Code Generation Results) showing created/skipped/failed counts; Single mode confirms inline and routes to Screen 6
- **Margin Guard (Rule 15)**: System validates that the configured discount plus the affiliate's commission does not exceed Hairline's commission on the booking. Percentage configurations that breach the ceiling (`discount % + commission % > Hairline's commission %`) are **blocked** with the shortfall shown (override requires documented, audited business approval); fixed-amount configurations raise a **review warning** since the breach is booking-value dependent
- **Dashboard Visibility**: Active issued codes appear in the assigned affiliate's dashboard immediately after creation; inactive, expired, or revoked codes remain visible in historical views with status labels

**Acceptance Criteria**:

1. Given admin creates a code in Single Affiliate mode, when the code is saved, then system validates platform-wide uniqueness, links the code to exactly one affiliate, registers it with FR-019, and shows it on that affiliate's dashboard.
2. Given admin creates codes in Selected Affiliates mode, when generation completes, then system creates one distinct code per selected affiliate using the same campaign settings and opens Screen 4.1 with a created/skipped/failed summary.
3. Given admin creates codes in Filtered Segment mode, when generation starts, then system snapshots the matched affiliate IDs and uses that snapshot for the batch even if filter membership changes later.
4. Given admin attempts to reuse one affiliate payout code across multiple affiliates, when admin submits the form, then system rejects the action and explains that affiliate payout codes must be one code to one affiliate.
5. Given FR-019 rejects a generated code registration, when the batch completes, then that affiliate row is marked failed on Screen 4.1 and can be retried without duplicating successful codes.
6. Given admin configures a percentage discount plus commission whose sum exceeds Hairline's commission on the booking, when admin submits, then the system blocks the save and shows the shortfall (per Rule 15); a documented business-approval override is required to proceed and is audited. For fixed-amount configurations, the system shows a review warning instead of blocking.

**Notes**:

- Allow bulk code creation by selected affiliate set or filtered segment, e.g., "Create one SUMMER2026 code for every active UK affiliate"
- Do not support one shared affiliate payout code across multiple affiliates; use open Hairline-funded codes in FR-019 for non-attributed public marketing campaigns

---

#### Screen 4.1: Code Generation Results

**Purpose**: Outcome summary for a bulk (Selected Affiliates or Filtered Segment) generation run, giving admins a clear created/skipped/failed breakdown and a retry path. Backs the B4 partial-failure flow. A full screen (not a transient modal): the batch is persisted and revisitable from Screen 5. Launched from Screen 4 on submit.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Batch ID | text | N/A | Unique identifier for this generation run | Read-only, system-generated |
| Campaign Name | text | N/A | Campaign these codes belong to | Read-only |
| Requested Count | number | N/A | Number of affiliates targeted in this run | Read-only, system-calculated |
| Created Count | number | N/A | Codes successfully created | Read-only, system-calculated |
| Skipped Count | number | N/A | Affiliates skipped (e.g., ineligible) | Read-only, system-calculated |
| Failed Count | number | N/A | Affiliates whose code creation failed | Read-only, system-calculated |
| Result Rows | list | N/A | Per-affiliate row: affiliate, generated code (if any), outcome, reason | Read-only; failed rows selectable for retry |
| Actions | buttons | N/A | Retry Failed Only, Download Results (CSV), View Codes | Context-dependent on failed count |

**Business Rules**:

- **No Duplicate Creation**: Retrying failed rows never re-creates already-successful codes
- **Per-Row Reason**: Each skipped/failed row records a specific reason (duplicate generated code, inactive affiliate, incomplete payout setup, FR-019 registration failure, notification failure)
- **Idempotent Retry**: "Retry Failed Only" re-runs generation for the failed subset under the same campaign settings and snapshot
- **Export**: Results downloadable as CSV for record-keeping

**Acceptance Criteria**:

1. Given a bulk generation completes, when Screen 4.1 loads, then created/skipped/failed counts and a per-affiliate result list with reasons are shown.
2. Given some rows failed, when admin clicks "Retry Failed Only", then only the failed affiliates are re-attempted and successful codes are not duplicated.
3. Given admin clicks "View Codes", then Screen 5 (Promo Code Management) opens filtered to this batch's campaign.

**Notes**:

- Color-code outcomes: created (green), skipped (gray), failed (red)
- Persist the batch so admins can revisit results later from Screen 5

---

#### Screen 5: Promo Code Management

**Purpose**: System-wide registry of every affiliate-bound promo code across all affiliates. Admins browse, filter, and act on codes here; each row opens the shared Screen 6 (Promo Code Detail).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Discount Code | text | N/A | The code patients enter at checkout | Read-only |
| Campaign Name | text | N/A | Campaign the code belongs to | Read-only |
| Linked Affiliate | text | N/A | Affiliate the code is assigned to | Read-only; links to Screen 3 |
| Discount | text | N/A | Discount type and value (e.g., "10%" or "$50") | Read-only |
| Application Method | text | N/A | Auto-apply or Code-based | Read-only |
| Applied / Completed | text | N/A | Applied count and completed count | Read-only, system-calculated |
| Conversion Rate | percent | N/A | Completed / applied | Read-only, system-calculated |
| Revenue | currency | N/A | Revenue attributed to the code | Read-only, system-calculated |
| Commission | currency | N/A | Commission earned via the code | Read-only, system-calculated |
| Status | status | N/A | Active / Inactive / Expired / Revoked | Read-only badge |
| Created Date | date | N/A | When the code was generated | Read-only, system-recorded |
| Actions | buttons | N/A | View Detail, Activate/Deactivate | Context-dependent based on status |

**Business Rules**:

- **System-Wide Scope**: Lists codes across all affiliates, campaigns, and generation modes (single and bulk)
- **Filtering**: Filter by status, campaign, linked affiliate, discount type, application method, created date range; search by code text or campaign
- **Pagination**: Display 50 codes per page with pagination controls
- **Bulk Actions**: Admin can multi-select codes to bulk activate/deactivate (subject to status rules)
- **Detail Navigation**: "View Detail" opens the shared Screen 6; the same screen opens from the assigned-codes list inside Screen 3
- **Read-Through Counts**: Applied/completed and conversion stats are sourced from FR-019 redemption lifecycle

**Acceptance Criteria**:

1. Given admin opens Promo Code Management, when the screen loads, then codes from all affiliates are listed with status, linked affiliate, and performance columns.
2. Given admin filters by campaign or affiliate, then only matching codes are listed with a visible result count.
3. Given admin clicks a code row (or "View Detail"), then Screen 6 (Promo Code Detail) opens for that code.
4. Given admin opens Screen 6 from this list and another admin opens the same code from Screen 3, then both see the identical shared screen and capabilities.

**Notes**:

- Color-code status: Active (green), Expired (gray), usage-limit-reached (orange), Revoked (red)
- Display usage statistics inline, e.g., "125 applied / 87 completed (69.6% conversion rate)"

---

#### Screen 6: Promo Code Detail (Shared)

**Purpose**: Single-code workspace showing the code's settings, the affiliate it is assigned to, and its performance. This is a **shared screen** reached from two entry points: (a) Screen 5 (Promo Code Management) row, and (b) the assigned-codes list inside Screen 3 (Affiliate Detail). Both entry points open the same screen.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Code Header | composite | N/A | Code text, campaign, status badge, created date | Read-only |
| Linked Affiliate | link | N/A | The single affiliate this code belongs to | Read-only; links to Screen 3 |
| Code Settings Panel | section | N/A | Discount type/value, application method, expiration, max usage, per-patient limit | Read-only; editable subset per rules |
| Performance Panel | composite | N/A | Applied, completed, conversion rate, revenue, commission earned | Read-only, system-calculated |
| Usage Over Time | chart | N/A | Applications/completions trend | Read-only, system-calculated |
| Generation Source | text | N/A | Single or batch (with Batch ID link to Screen 4.1) | Read-only |
| Status Controls | buttons | N/A | Activate / Deactivate / Extend Expiration | Context-dependent based on status |
| Audit / History | list | N/A | Code lifecycle events (created, edited, deactivated) | Read-only, append-only |

**Business Rules**:

- **Single Shared Screen**: Identical layout and capabilities regardless of entry point (Screen 5 or Screen 3)
- **One Affiliate**: The linked affiliate is always exactly one; reassignment to another affiliate is not supported (create a new code instead)
- **Editable Subset**: Admin may edit expiration date, usage limits, and active/inactive status; discount value and linked affiliate are fixed after creation
- **Lifecycle Source**: Applied/completed/conversion and revenue/commission figures are read from FR-019 and commission calculation; this screen does not recompute them
- **Status Transitions**: Deactivation revokes checkout validity immediately; expired/revoked codes remain visible with status labels and cannot be copied as active codes

**Acceptance Criteria**:

1. Given admin opens Screen 6 from Screen 5, then the code header, linked affiliate, settings, and performance are shown.
2. Given admin opens the same code from the assigned-codes list in Screen 3, then the identical shared screen is shown.
3. Given admin edits the expiration date or toggles status, when saved, then the change is validated, applied, and recorded in the code audit history.
4. Given admin attempts to change the linked affiliate, then the system blocks it and explains codes are one-to-one with an affiliate.

**Notes**:

- Show the linked-affiliate name as a clear breadcrumb/back link to Screen 3 when opened from Affiliate Detail
- Surface the FR-019 redemption status alongside the FR-018 attribution to avoid confusion

---

#### Screen 7: Affiliate Payout Status & History

**Purpose**: Read-only admin workspace to review affiliate payout status, payout history, and reconciliation data calculated in FR-018 and executed in FR-017 / A-05. FR-018 does **not** initiate Stripe transfers or process payouts; affiliate billing and payout execution remain owned by FR-017 Screen 6.

**Sub-views**: Overview (overall performance) · Current Cycle (read-only payout status) · Billing History (audit, 7-year retention, CSV export).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Payout Month | month | Yes | Month for which payouts are being processed/viewed | Format: "November 2025" |
| Overall Totals | composite | N/A | Total owed this cycle, total paid, affiliate count, failed count | Read-only, system-calculated |
| Affiliate Name | text | N/A | Name of affiliate receiving payout | Read-only, from affiliate record |
| Total Completed Bookings | number | N/A | Count of completed bookings in payout period | Read-only, system-calculated |
| Total Commissions Owed | currency | N/A | Sum of commissions for completed bookings | Read-only, system-calculated |
| Payment Method | text | N/A | Stripe transfer to affiliate bank account, executed by FR-017 / A-05 | Read-only, from affiliate record |
| Payment Details | text | N/A | Masked affiliate bank account (last 4 digits) | Read-only, masked |
| Payout Status | status | N/A | Pending, Processing, Paid, Failed | Read-only, from FR-017 payout execution state |
| Transaction ID | text | N/A | Stripe transfer reference / ID (Billing History) | Read-only, from Stripe |
| Notes | textarea | No | Admin notes about payout | Max 500 characters |
| Actions | buttons | N/A | View Detail, Export CSV, Download Receipt | Read-only/export actions only |

**Business Rules**:

- **Automated Generation**: System automatically generates the payout list on the 7th of each month for the previous month's completed bookings and exposes the calculated amounts to FR-017 / A-05 for payout execution
- **Overview Sub-view**: Shows overall performance for the selected month (total owed, total paid, affiliate count, failed count) at the top
- **Current Cycle Sub-view**: Current cycle list is read-only in FR-018; payout processing actions are performed in FR-017 Screen 6 (Affiliate Billing - Commission Payouts)
- **Stripe Execution**: Payouts are executed by FR-017 / A-05 as Stripe transfers to each affiliate's stored bank account, using the Stripe accounts configured in FR-029 and the payout execution path shared with provider payouts; FR-018 displays the resulting status updates
- **Billing History Sub-view**: Permanent audit log of all payouts (affiliate, amount, date, transaction ID, final status) with full-text search, filter by affiliate/date/status, and CSV export; records retained for 7 years minimum
- **Status Workflow**: Pending → Processing (payment initiated by FR-017) → Paid (payment confirmed) OR Failed (payment error)
- **Retry Logic**: If a payout fails, retry is handled in FR-017 Screen 6; FR-018 displays the latest failed/retried status and failure reason
- **Email Notifications**: System automatically sends a payout confirmation email when status changes to "Paid" based on FR-017 payout status
- **Detail Navigation**: "View Detail" (in any sub-view) opens the shared Screen 8 (Payout / Transaction Detail)

**Acceptance Criteria**:

1. Given it is the 7th of the month, when the automated payout calculation runs, then the Current Cycle sub-view lists all affiliates with completed bookings in the previous month and the Overview shows the cycle totals.
2. Given payout data is generated in FR-018, when FR-017 reads the payout cycle, then the same affiliate count, amounts, threshold exclusions, and payout readiness data are available for A-05 execution.
3. Given a payout fails in FR-017, when FR-018 refreshes the Current Cycle sub-view, then the row is marked "Failed", surfaced in red, and the failure reason is visible.
4. Given admin opens the Billing History sub-view, then historical payouts are searchable, filterable, and exportable to CSV, with 7-year retention.
5. Given admin clicks "View Detail" on any payout row, then the shared Screen 8 opens for that payout.

**Notes**:

- Display total payout amount for the month at the top of the Overview sub-view
- Highlight failed payouts in red with the error message displayed
- Allow admin to add internal notes explaining payout delays (not visible to affiliate)

---

#### Screen 8: Payout / Transaction Detail (Shared)

**Purpose**: Single-payout workspace showing the full breakdown of one affiliate payout/transaction. This is a **shared screen** reached from two entry points: (a) Screen 7 (Payout Status & History, Current Cycle or Billing History sub-view), and (b) the payout list inside Screen 3 (Affiliate Detail). Both entry points open the same screen.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Payout Header | composite | N/A | Affiliate name, payout month, status badge, payout ID | Read-only |
| Affiliate Link | link | N/A | The affiliate this payout belongs to | Read-only; links to Screen 3 |
| Period | text | N/A | Payout period date range / month | Read-only |
| Included Bookings | list | N/A | Bookings contributing to this payout (booking ID, date, booking total, commission) | Read-only, system-calculated |
| Commission Calculation | composite | N/A | Total bookings count, gross commission, reversals/refunds, net amount | Read-only, system-calculated |
| Payment Method | text | N/A | Stripe transfer to affiliate bank account | Read-only, from affiliate record |
| Payment Details | text | N/A | Masked affiliate bank account (last 4 digits) | Read-only, masked |
| Transaction ID | text | N/A | Stripe transfer reference / ID | Read-only, from Stripe |
| Status Timeline | list | N/A | Pending → Processing → Paid/Failed with timestamps | Read-only, system-recorded |
| Failure Reason | text | N/A | Stripe transfer error message if status is Failed | Read-only, shown only when Failed |
| Notes | textarea | No | Admin internal notes for this payout | Max 500 characters |
| Actions | buttons | N/A | Download Receipt | Read-only/export action only |

**Business Rules**:

- **Single Shared Screen**: Identical layout and capabilities regardless of entry point (Screen 7 or Screen 3)
- **Breakdown Integrity**: The included-bookings list must reconcile to the net commission amount (gross minus reversals/refunds)
- **Refund Reversals**: Booking refunds processed after payout appear as reversals and carry forward per Payment Rule 2
- **Receipt**: "Download Receipt" generates a PDF receipt for the payout (affiliate records)
- **Retry Ownership**: Failed payout retry is performed in FR-017 Screen 6; this detail screen displays retry status and failure history read-only
- **Masking**: Payment details remain masked (last 4 digits)

**Acceptance Criteria**:

1. Given admin opens Screen 8 from Screen 7, then the payout header, included bookings, commission calculation, payment details, and status timeline are shown.
2. Given admin opens the same payout from the payout list in Screen 3, then the identical shared screen is shown.
3. Given the payout status is "Failed", when FR-017 retries the payout, then the read-only status timeline updates after FR-018 receives the latest payout status.
4. Given admin clicks "Download Receipt", then a PDF receipt reconciling to the net commission amount is generated.

**Notes**:

- Show a back link to the originating context (Payout Status & History vs. Affiliate Detail) for orientation
- Display reversals/refunds as distinct negative line items so the net is auditable

---

### Affiliate Platform Screens

#### Screen 9: Affiliate Portal

**Purpose**: Authenticated affiliate-facing portal — the container/shell for the four affiliate tabs, each of which is its own screen (Screens 9.1-9.4). Provides the shared header, tab navigation, session/auth, and refresh behavior. Patient identity is never exposed.

**Tabs (each a separate screen)**:

- **Screen 9.1 — Overview**: performance summary and trends (default landing tab)
- **Screen 9.2 — Promo Codes**: codes assigned to the affiliate, with per-code breakdown
- **Screen 9.3 — Payouts**: payout listing (history and upcoming), with per-payout detail
- **Screen 9.4 — Profile**: affiliate's own profile; self-edit of non-sensitive fields only

**Business Rules**:

- **Authentication**: Secure login (username/password, optional MFA — future / non-MVP, pending the shared MFA stack FR-026 / FR-031 per constitution Principle II); affiliates see only their own data (RBAC)
- **Default Tab**: Overview (Screen 9.1) is the landing tab on login
- **Real-Time Updates**: Portal data refreshes every 5 minutes (or on manual refresh)
- **Privacy**: Patient identity is never shown anywhere in the portal; only aggregated statistics are visible
- **Referral Link**: The affiliate's unique referral link (auto-apply code URL) is available with a one-click copy action

**Acceptance Criteria**:

1. Given an affiliate logs in, when the portal loads, then the four tabs (Overview, Promo Codes, Payouts, Profile) are available and Overview is shown by default.
2. Given an affiliate selects a tab, then the corresponding screen (9.1-9.4) is shown without exposing any other affiliate's data.

**Notes**:

- Each tab is specified as its own screen below (9.1-9.4) rather than combined into a single screen
- The portal mirrors the provider self-service model (FR-032) with a leaner field set matching the data collected for affiliates

---

#### Screen 9.1: Overview Tab

**Purpose**: Affiliate performance summary and trends — the default landing tab of the portal (Screen 9).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Total Referrals (All-Time) | number | N/A | Count of all completed bookings with affiliate referral attribution | Read-only, system-calculated |
| Referrals This Month | number | N/A | Count of completed bookings in current month | Read-only, system-calculated |
| Total Revenue Generated | currency | N/A | Sum of booking values from affiliate referrals | Read-only, system-calculated |
| Total Commissions Earned | currency | N/A | Sum of all commissions earned to date | Read-only, system-calculated |
| Commissions Paid | currency | N/A | Sum of commissions already paid out | Read-only, system-calculated |
| Pending Payout | currency | N/A | Commission awaiting next payout (unpaid balance) | Read-only, system-calculated |
| Next Payout Date | date | N/A | Date of next scheduled payout | Read-only, system-set (fixed: 7th of month) |
| Referral Link | text | N/A | Affiliate's unique auto-apply referral URL | Read-only, one-click copy |

**Business Rules**:

- **Payout Calculation**: "Pending Payout" includes commissions from completed bookings in previous month (not yet paid)
- **Conversion Funnel**: Overview shows the funnel Code Applied → Checkout Started → Payment Completed
- **Monthly Breakdown**: Affiliate can toggle between "All-Time" and "Current Month"
- **Export Report**: Affiliate can download a performance report as PDF

**Acceptance Criteria**:

1. Given an affiliate opens the Overview tab, then accurate referral count, revenue, commissions earned/paid, pending payout, and next payout date are shown.
2. Given a pending payout exists, then the "Pending Payout" amount is shown prominently with a countdown to the next payout date.

**Notes**:

- Use visual charts: line graph for referrals over time, pie chart for conversion funnel

---

#### Screen 9.2: Promo Codes Tab

**Purpose**: Lists the discount codes assigned to the affiliate, with a per-code performance breakdown.

**Data Fields**:

_List row (one per assigned code)_:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Discount Code | text | N/A | The code patients enter at checkout | Read-only; one-click copy |
| Campaign Name | text | N/A | Campaign the code belongs to | Read-only |
| Status | status | N/A | Active / Inactive / Expired / Revoked | Read-only badge |
| Active Window | date range | N/A | Start and end dates the code is valid | Read-only |
| Discount | text | N/A | Discount type and value (e.g., "10%" or "$50") | Read-only |
| Application Method | text | N/A | Auto-apply or Code-based | Read-only |
| Applied Count | number | N/A | Times the code was applied at checkout | Read-only, system-calculated |
| Completed Count | number | N/A | Applications that became completed bookings | Read-only, system-calculated |
| Conversion Rate | percent | N/A | Completed / applied | Read-only, system-calculated |
| Revenue Generated | currency | N/A | Booking revenue attributed to the code | Read-only, system-calculated |
| Commission Earned | currency | N/A | Commission earned via the code | Read-only, system-calculated |
| Created Date | date | N/A | When the code was generated | Read-only |

_Per-code detail (on selecting a row)_:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Code Header | composite | N/A | Code text, campaign, status, active window | Read-only |
| Discount Terms | text | N/A | Discount type/value, application method, per-patient limit, max usage | Read-only |
| Usage Over Time | chart | N/A | Applications and completions trend | Read-only, system-calculated |
| Applied / Completed | text | N/A | Applied count vs. completed count | Read-only, system-calculated |
| Conversion Rate | percent | N/A | Completed / applied | Read-only, system-calculated |
| Revenue / Commission | currency | N/A | Revenue generated and commission earned for the code | Read-only, system-calculated |
| Last Used Date | date | N/A | Most recent application of the code | Read-only, system-calculated |
| Copy / Share Action | button | N/A | Copy code text or the auto-apply referral link | N/A |
| Marketing Materials | link/list | N/A | Read-only links to externally hosted banners, templates, or campaign assets assigned to the code/campaign | Links only; FR-018 does not create or host assets |

**Business Rules**:

- **Issued Code Visibility**: All active codes generated for the affiliate through single or bulk admin actions appear here with campaign name, active window, and status
- **Historical Codes**: Expired or revoked codes remain visible with status labels but cannot be copied as active promotional codes
- **Read-Only Stats**: Applied/completed, conversion, revenue, and commission figures are sourced from FR-019 redemption lifecycle and commission calculation; affiliates cannot edit code parameters
- **Marketing Materials Access**: If a campaign has externally hosted marketing materials, affiliates can view/download those links from the relevant code detail. Asset creation, editing, approval, and hosting remain outside FR-018 scope.
- **Sorting/Filtering**: Affiliate can sort by performance (revenue/commission) and filter by status (Active / Inactive / Expired / Revoked)

**Acceptance Criteria**:

1. Given admin generates a new active code for an affiliate, when the affiliate refreshes this tab, then the code appears with campaign name, status, active window, and zero-referral initial state.
2. Given an affiliate has multiple active codes, when affiliate clicks one code, then per-code applied count, completed count, conversion rate, revenue, commission earned, usage-over-time, and last-used date are shown.
3. Given an affiliate has expired or revoked codes, when affiliate opens the historical code view, then those codes remain visible with status labels but cannot be copied as active promotional codes.
4. Given an affiliate clicks copy on an active code, then the code text (or auto-apply referral link) is copied to the clipboard.
5. Given a campaign has externally hosted marketing materials, when affiliate opens the code detail, then read-only material links are shown and can be opened/downloaded without allowing affiliate edits.

---

#### Screen 9.3: Payouts Tab

**Purpose**: Affiliate-facing payout listing (history and upcoming) with per-payout detail.

**Data Fields**:

_Upcoming payout panel (top of tab)_:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Next Payout Date | date | N/A | Date of the next scheduled payout | Read-only, system-set (fixed: 7th of month) |
| Pending Amount | currency | N/A | Commission awaiting the next payout (unpaid balance) | Read-only, system-calculated |
| Included Bookings Count | number | N/A | Completed bookings contributing to the pending payout | Read-only, system-calculated |
| Minimum Threshold Note | display | N/A | Note shown when pending is below the $50 threshold (rolls over) | Read-only, shown when applicable |

_Payout history list (one row per payout)_:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Payout Period | month | N/A | Month/period the payout covers | Read-only (e.g., "November 2025") |
| Net Amount | currency | N/A | Net commission paid in this payout | Read-only, system-calculated |
| Status | status | N/A | Pending / Processing / Paid / Failed | Read-only badge |
| Completed Bookings | number | N/A | Bookings included in this payout | Read-only, system-calculated |
| Payout Date | date | N/A | Date the payout was processed | Read-only |
| Transaction Reference | text | N/A | Stripe transfer reference / ID | Read-only, from Stripe |

_Per-payout detail (on selecting a row)_:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Payout Header | composite | N/A | Period, status, net amount, payout ID | Read-only |
| Period | text | N/A | Payout period date range | Read-only |
| Gross Commission | currency | N/A | Commission before reversals | Read-only, system-calculated |
| Reversals / Refunds | currency | N/A | Deductions from refunded bookings | Read-only, system-calculated |
| Net Amount | currency | N/A | Gross minus reversals (amount transferred) | Read-only, system-calculated |
| Included Bookings | list | N/A | Aggregated bookings contributing (count and value; no patient identity) | Read-only, system-calculated |
| Payment Method | text | N/A | Stripe transfer to the affiliate's bank account | Read-only |
| Bank Account | text | N/A | Masked affiliate bank account (last 4 digits) | Read-only, masked |
| Transaction Reference | text | N/A | Stripe transfer reference / ID | Read-only, from Stripe |
| Download Receipt | button | N/A | Download a PDF receipt for the payout | Available for Paid payouts |

**Business Rules**:

- **Upcoming Payout**: The next scheduled payout (amount, date, included bookings count) is shown at the top alongside the history list
- **Minimum Threshold**: When the pending amount is below the $50 minimum, the panel notes it will roll over to the next cycle (Payment Rule 3)
- **Read-Only**: Affiliates view payout status only; processing is admin-side (Screen 7) and execution is via Stripe transfer
- **Privacy**: Per-payout detail shows aggregated figures only; no individual patient identity is exposed
- **Receipt**: A PDF receipt is downloadable for each Paid payout

**Acceptance Criteria**:

1. Given an affiliate opens the Payouts tab, then the upcoming payout (date, pending amount, included bookings) and the payout history list are shown.
2. Given an affiliate clicks a payout, then its detail (period, gross commission, reversals, net amount, included bookings, payment method, masked bank account, transaction reference) is shown.
3. Given a payout has status "Paid", when the affiliate clicks "Download Receipt", then a PDF receipt reconciling to the net amount is generated.
4. Given the pending amount is below $50, then the upcoming payout panel notes it rolls over to the next cycle.

---

#### Screen 9.4: Profile Tab

**Purpose**: The affiliate's own profile, mirroring the provider profile (FR-032) with a leaner field set. Affiliates self-edit non-sensitive fields and manage their own account security only.

**Data Fields**:

_Account information_:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Affiliate Name | text | Read-only | Legal/payout name used for attribution and Stripe transfers | Read-only to affiliate (admin-controlled) |
| Contact Email | email | Read-only | Login username and notification address | Read-only (email change requires a new account) |
| Phone Number | tel | Editable | Contact phone with country code | Valid international phone format |
| Language(s) | multi-select | Editable | Spoken/operating language(s) | Uses supported language list |
| Country/Region | select | Read-only | Operating country or region | Read-only to affiliate (admin-controlled) |
| Affiliate Type | text | Read-only | Influencer / clinic partner / organization / other | Read-only to affiliate (admin-controlled) |
| Tax / VAT / Business Reg ID | text | Read-only | Tax/VAT/business-registration identifier | Read-only to affiliate (admin-controlled) |
| Member Since | date | Read-only | Account creation date | Read-only |
| Activation Status | status | Read-only | Invited (password not set) / Active | Read-only |

_Payout & commission (admin-controlled, read-only)_:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Bank Account | text | Read-only | Masked affiliate bank account (last 4 digits) | Read-only to affiliate (admin-controlled) |
| Bank Name | text | Read-only | Name of the affiliate's bank | Read-only to affiliate (admin-controlled) |
| Commission Structure | text | Read-only | Current commission type and value | Read-only to affiliate (admin-controlled) |
| Payout Schedule | text | Read-only | Payout frequency (e.g., Monthly on 7th) | Read-only to affiliate (admin-controlled) |
| Account Status | status | Read-only | Pending / Active / Suspended / Inactive | Read-only to affiliate |

_Account security (affiliate-managed)_:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Change Password | action | Editable | Update account password | Strong password (min 12 chars, upper, lower, number, special); current password required |
| MFA (optional) | toggle | Editable | Enable/disable multi-factor authentication | Optional; future / non-MVP (pending shared MFA stack FR-026 / FR-031 per constitution Principle II); mirrors platform auth options |

**Business Rules**:

- **Self-Service Edit**: Affiliate may edit non-sensitive fields (phone, language) and manage their own account security (password, optional MFA — future / non-MVP, pending FR-026 / FR-031); changes sync to the admin view (Screen 2 / Screen 3)
- **Admin-Controlled Fields**: Name (legal/payout name used for attribution and Stripe transfers), email, country/region, affiliate type, tax/VAT ID, bank details, commission structure, payout schedule, and status are read-only to the affiliate and changed only by admins
- **Email Immutable**: Contact email (login username) cannot be changed (a new account is required), consistent with admin Screen 2 rules
- **Masking**: Bank account number is shown masked (last 4 digits) and is never editable by the affiliate
- **Provider Parity**: Mirrors the provider self-service model in FR-032 with a leaner affiliate field set

**Acceptance Criteria**:

1. Given an affiliate edits a non-sensitive Profile field (phone, language), when saved, then the change persists and syncs to the admin view; the name field is admin-controlled and not editable by the affiliate.
2. Given an affiliate opens the Profile tab, then email, country/type, tax/VAT ID, bank details, commission, payout schedule, and status are visible but read-only (admin-controlled).
3. Given an affiliate uses "Change Password" with a valid current password and a strong new password, when saved, then the password is updated.
4. Given an affiliate attempts to change their email, then the field is not editable and a note explains a new account is required.

---

#### Screen 10: Affiliate Onboarding & Activation

**Purpose**: Affiliate-facing onboarding from account creation to first portal access, mirroring the provider activation flow (FR-015). Comprises Set Password (Screen 10.1), Resend Activation (Screen 10.2), and Welcome / Get Started (Screen 10.3). This flow precedes first access to the portal (Screen 9). Admin-side resend is available from Screen 3 (Affiliate Detail). Backs Main Flow steps 9-12 and Alternative Flow A5.

**Business Rules**:

- **Sequence**: Activation email → Set Password (10.1) → first login → Welcome / Get Started (10.3); Resend Activation (10.2) is reachable from the login page when the link is missing or expired
- **Token Handling**: One-time set-password link expires in 24 hours; generating a new link invalidates the previous one
- **Activation State**: Account is created with Status "Pending" and Activation Status "Invited" until the password is set; completing 10.1 flips Status to "Active" and Activation Status to "Active" (per Rule 12)

**Acceptance Criteria**:

1. Given an affiliate account is created, when the activation email is sent, then it contains a one-time "Set Password" link (24-hour expiry) and the affiliate's login email.
2. Given the affiliate completes activation, then they proceed through Set Password (10.1) and land on Welcome / Get Started (10.3) at first login.

---

#### Screen 10.1: Set Password (Activation Landing)

**Purpose**: Reached via the one-time activation link in the activation email; the affiliate creates a password to activate their account. Mirrors the provider set-password step (FR-015).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Activation Link Status | display | N/A | Whether the one-time link is valid or expired | Read-only, system-evaluated |
| Account Email | display | N/A | The invited email (login username) | Read-only |
| New Password | password | Yes | New account password | Min 12 chars, with uppercase, lowercase, number, special char |
| Confirm Password | password | Yes | Re-enter new password | Must match New Password |
| Password Strength Meter | display | N/A | Visual strength indicator | Read-only, reflects entered password |
| Set Password | button | N/A | Submit to set password and activate | Enabled only when both fields are valid |

**Business Rules**:

- **One-Time Token**: The link is single-use and expires 24 hours after generation
- **On Success**: System saves the encrypted password, flips Status from "Pending" to "Active" and Activation Status to "Active" (per Rule 12), and redirects to the Affiliate Portal login (Screen 9)
- **Expired / Used Link**: System shows an explanatory message and a link to request a new one (Screen 10.2)
- **Security**: Password strength is enforced server-side; the email field is fixed (cannot be changed here)

**Acceptance Criteria**:

1. Given a valid, unexpired link, when the affiliate enters a strong matching password and submits, then the password is saved (encrypted), Activation Status becomes "Active", and they are redirected to the portal login.
2. Given an expired or already-used link, when the affiliate opens it, then an explanatory message and a "Resend activation email" option (Screen 10.2) are shown.
3. Given a weak or mismatched password, when the affiliate submits, then the form blocks submission and explains the requirement.

---

#### Screen 10.2: Resend Activation Email

**Purpose**: Self-service "Didn't receive activation email?" form on the portal login page; lets an invited affiliate request a fresh activation link. Mirrors FR-015 Alternative Flow A1.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Email | email | Yes | The email the admin used during account creation | Valid email format |
| Resend Activation | button | N/A | Request a new one-time activation link | Subject to rate limiting |
| Confirmation Message | display | N/A | Generic confirmation shown after submit | Read-only |

**Business Rules**:

- **Rate Limit**: Maximum 3 resend requests per hour per email address
- **Link Invalidation**: A new link invalidates the previous one
- **Generic Messaging**: System always shows "If an account exists with this email, an activation link will be sent." regardless of whether the email exists or is already activated (does not reveal account existence)
- **Eligibility**: A link is only generated for accounts created but not yet activated (password not set)

**Acceptance Criteria**:

1. Given an invited affiliate enters their email and submits, then a fresh one-time link is sent, the previous link is invalidated, and the generic confirmation is shown.
2. Given more than 3 requests within an hour for the same email, then further requests are rate-limited.
3. Given an unknown or already-activated email, then the same generic confirmation is shown without revealing account status.

---

#### Screen 10.3: Welcome / Get Started (First Login)

**Purpose**: Shown once on the affiliate's first successful login after activation, mirroring the provider "Welcome to Hairline" onboarding. Introduces the program and prompts profile completion before entering the portal.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
| --- | --- | --- | --- | --- |
| Welcome Header | display | N/A | Welcome message and platform introduction | Read-only |
| Assigned Codes Summary | list | N/A | The affiliate's initial discount code(s) | Read-only |
| Commission Summary | display | N/A | The affiliate's commission structure | Read-only |
| Payout Schedule | display | N/A | Payout frequency and next payout date | Read-only |
| Referral Link | text | N/A | The affiliate's unique auto-apply referral URL | Read-only, one-click copy |
| Complete Profile CTA | button | N/A | Opens the Profile tab (Screen 9.4) to fill in details | N/A |
| Get Started CTA | button | N/A | Dismisses onboarding and opens Overview (Screen 9.1) | N/A |

**Business Rules**:

- **Shown Once**: Displayed only at first login; afterwards the affiliate lands directly on Overview (Screen 9.1). It is dismissible.
- **Profile Completion**: "Complete Profile" routes to Screen 9.4, where the affiliate can fill non-sensitive fields (phone, language)
- **Privacy**: Only the affiliate's own codes, commission, and payout schedule are shown

**Acceptance Criteria**:

1. Given the affiliate logs in for the first time after activation, then the Welcome / Get Started screen is shown with their assigned code(s), commission structure, payout schedule, and referral link.
2. Given the affiliate clicks "Complete Profile", then the Profile tab (Screen 9.4) opens.
3. Given the affiliate clicks "Get Started" (or returns later), then they land on the Overview tab (Screen 9.1) and the welcome screen is not shown again.

---

## Business Rules

### General Module Rules

- **Rule 1**: Affiliate commissions are ONLY calculated for completed bookings where payment is confirmed (not for quote requests or pending bookings)
- **Rule 2**: Affiliate discount codes apply ONLY to Hairline's commission (does NOT reduce provider payout)
- **Rule 3**: Only ONE discount code can be applied per booking (priority: Patient code > Provider code > Affiliate code)
- **Rule 4**: Affiliate commissions are deducted from Hairline's commission, NOT from provider's payout
- **Rule 5**: Payout processing occurs monthly on the 7th of each month (**fixed** schedule, per client policy — not admin-configurable) for the previous month's completed bookings
- **Rule 6**: Affiliates can have multiple active discount codes simultaneously for different campaigns
- **Rule 7**: FR-018 is the source of truth for affiliate-specific promo code generation and assignment; FR-019 provides the shared promotion rules, validation, redemption state lifecycle, and financial-impact logging
- **Rule 8**: Bulk affiliate code generation MUST create one distinct code per affiliate; assigning the same affiliate payout code to multiple affiliates is not supported
- **Rule 9**: Admins MAY create open Hairline-funded marketing codes in FR-019, but those codes do not create affiliate payout attribution unless they are generated or linked as affiliate-bound codes through FR-018
- **Rule 10**: Affiliate onboarding uses a one-time secure activation link (set password, expires 24 hours) mirroring the provider activation flow; raw credentials are never emailed
- **Rule 11 (Affiliate referral attribution is preserved separately from price discount priority)**: Affiliate commission and referral credit are earned when a valid affiliate-bound code or affiliate auto-apply referral link is captured for the patient's booking journey and the booking completes with payment confirmation, even if the final price discount applied at checkout is a higher-priority patient or provider promotion under Rule 3. The single-discount rule still controls the patient's price and provider/Hairline discount impact; it does **not** erase affiliate referral attribution. This protects affiliates from losing commission because a provider-side promotion is applied outside the patient's knowledge. FR-017 and FR-019 MUST consume the FR-018/FR-019 attribution result separately from the final applied discount line.
- **Rule 12 (Affiliate lifecycle states)**: An affiliate moves through **Pending** (account created, password not yet set) → **Active** (password set, transacting) and may then be **Suspended** (temporary, reversible, codes disabled, pending commissions held pending investigation — B3) or **Inactive** (permanent terminal end-of-partnership, codes disabled, portal read-only, final balance settled/forfeited/written off — B5). Active ⇄ Suspended is reversible via Screen 3.1; Active → Inactive is terminal via Screen 3.3 and is not silently reversed (resuming requires re-onboarding).
- **Rule 13 (Usage-limit basis)**: A code's `Maximum Usage Count` and `Per-Patient Usage Limit` are decremented on **"completed" (paid) redemptions only**, never on "applied" events — so abandoned or abusive checkouts cannot exhaust a code's cap. A separate soft anti-abuse **rate limit on "applied" events** (per patient / per IP / per time window) guards against application spam without consuming the usage cap.
- **Rule 14 (Commission base)**: Percentage commissions are calculated as a percentage of the **completed booking's revenue (booking total, in USD per the Currency Rule)** — **not** as a percentage of Hairline's net commission. Fixed-amount commissions are a flat USD amount per completed booking, independent of booking value. In both cases the commission is **funded from (deducted from) Hairline's commission, never the provider's payout** (Rule 4). The patient-facing affiliate discount (also Hairline-funded, Rule 2) and the affiliate commission are separate Hairline-borne costs against the same booking.
- **Rule 15 (Hairline-funded cost ceiling)**: On any single booking, the combined Hairline-funded cost — the patient-facing affiliate discount (Rule 2) plus the affiliate commission (Rule 14) — MUST NOT exceed Hairline's own commission earned on that booking; the affiliate program never makes a booking net-negative for Hairline. The system enforces this at affiliate code creation/generation (Screen 4): when both the discount and the commission are percentage-based, it validates that `discount % + commission % ≤ Hairline's commission % on the booking` and **blocks** the save with the shortfall shown; an admin with documented business approval may override with an audited confirmation. Fixed-amount configurations (where the ceiling depends on booking value) raise a **review warning** rather than a hard block, since the breach can only be evaluated per booking. This rule complements Assumption 4 (aggregate program cost ≤ 10% of Hairline commission revenue) by preventing per-booking negative margin.

### Affiliate Segmentation Rules (Performance Tier & Campaign Eligibility)

- **Performance Tier** (system-calculated, read-only): a band derived from the affiliate's **trailing-12-month revenue generated** (USD) by completed referrals, recalculated monthly. Default bands (admin-tunable): **Bronze** < $5,000 · **Silver** $5,000–$24,999 · **Gold** $25,000–$99,999 · **Platinum** ≥ $100,000. Tier is used for filtering/segmentation only and never changes commission automatically.
- **Campaign Eligibility** (system-calculated, read-only): an affiliate is **Eligible** for bulk/campaign code generation only when **all** of the following hold — Status = Active (not Pending, Suspended, or Inactive); Activation Status = Active (password set); and complete bank/payout details on file. Otherwise the affiliate is **Ineligible** and the specific failing reason is surfaced (e.g., "Pending activation", "Incomplete payout setup", "Suspended/Inactive"). These reasons are the same ones reported per row in bulk generation (B4) and drive Screen 1's eligibility gating.

### Data & Privacy Rules

- **Privacy Rule 1**: Patient identity is NEVER shared with affiliates (affiliates see only aggregated statistics, not individual patient names)
- **Privacy Rule 2**: Affiliate bank account numbers are masked in UI (show last 4 digits only)
- **Privacy Rule 3**: Affiliate dashboard access requires secure login (username/password + optional MFA — future / non-MVP, pending the shared MFA stack FR-026 / FR-031 per constitution Principle II)
- **Audit Rule**: All affiliate actions logged with timestamp, user ID, and action type (code usage, commission calculation, payout-cycle generation, payout status synchronization). The audit trail is immutable (append-only) and retained for **10 years** per the platform constitution (financial/payout records are retained 7 years minimum)
- **GDPR**: Affiliate personal data (contact info, payment details) can be deleted upon request (historical commission data retained for accounting)

### Admin Editability Rules

**Editable by Admin**:

- Affiliate account details (name, email, phone, language, country, type, tax/VAT ID, bank account details, commission structure)
- Discount code parameters (expiration date, usage limits, active/inactive status)
- Bulk code generation criteria (selected affiliates, filtered segment, code pattern, campaign settings)
- Commission percentage/fixed amount per affiliate (with effective date for changes, via Screen 3.2)
- Affiliate status (Active/Suspended/Inactive, via Screen 3.1)

**Editable by Affiliate (Self-Service)**:

- Non-sensitive profile fields only: phone, language(s)
- Affiliates CANNOT edit name (legal/payout name, admin-controlled), payment details, commission structure, status, or assigned codes (admin-controlled, read-only to affiliate)

**Fixed in Codebase (Not Editable)**:

- Affiliate commission calculation logic (percentage of booking revenue OR fixed amount per booking)
- One-affiliate-per-code attribution model
- Discount code uniqueness validation rules
- Payout workflow status transitions (Pending → Processing → Paid/Failed)
- Audit trail retention period (10 years, per constitution); financial/payout records retained 7 years minimum
- Activation link expiry (24 hours) and resend rate limit (3 per hour per email)
- Payout schedule (monthly on the 7th — fixed per client business policy; frequency and date are not configurable)

**Configurable with Restrictions**:

- Commission structure changes apply ONLY to future bookings (historical commissions cannot be retroactively modified)

### Payment & Billing Rules

- **Payment Rule 1**: Affiliate commissions calculated AFTER patient completes full payment for booking
- **Payment Rule 2**: If patient refunds booking, affiliate commission is reversed (deducted from next payout)
- **Payment Rule 3**: Minimum payout threshold: $50 (commissions below $50 roll over to next month)
- **Currency Rule**: All affiliate amounts (commission accrual, pending balances, thresholds, and payouts) are denominated in **USD — the platform base currency owned by FR-029 (Payment System Configuration)**. When a booking is transacted in a non-USD currency, its value is converted to USD using **FR-029's currency service, supported-currency list, and locked exchange-rate/markup logic — FR-018 never defines, caches, or overrides its own FX rate**. The conversion rate applied to a commission is the rate locked for that booking per FR-029 (no discrepancy with billing/finance figures). Affiliates are responsible for any onward conversion from USD on their side. **Note on client figures**: GBP amounts in the client transcription (e.g., "£50", "£200") are illustrative of intended incentive magnitudes; the platform base currency is USD (per FR-029), so this PRD's literal thresholds and minimums (e.g., the $50 minimum fixed commission and $50 payout threshold) are stated in USD and are not a direct GBP→USD conversion of those examples.
- **Billing Rule 1**: Payouts are processed as Stripe transfers to the affiliate's bank account, consistent with provider payouts (executed via FR-017 / S-02 using the Stripe accounts configured in FR-029); PayPal and other payout methods are not supported
- **Billing Rule 2**: Hairline covers Stripe payout/transfer fees (not deducted from affiliate commission)
- **Billing Rule 3**: Affiliates must provide complete bank details (account holder name, bank name, account number, routing/SWIFT code, optional IBAN) before a payout can be processed, mirroring provider billing setup in FR-032

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
- **SC-007**: Admins can bulk-generate distinct affiliate-bound codes for 100 selected affiliates in under 5 minutes
- **SC-008**: Automated payout-cycle calculation and FR-017 / A-05 handoff reduces admin preparation time by 80% compared to manual payout workflows
- **SC-009**: 100% of monthly payout-cycle data is generated and available to FR-017 / A-05 within 24 hours of the scheduled date (7th of month)
- **SC-010**: Admin support tickets related to affiliate payouts reduced by 70% through self-service affiliate dashboard

### Affiliate Experience Metrics

- **SC-011**: Affiliates can view real-time performance statistics without admin assistance (dashboard uptime 99.9%)
- **SC-012**: Affiliates receive payout confirmations within 24 hours of payment processing
- **SC-013**: Affiliate dashboard load time under 2 seconds for 95% of requests
- **SC-014**: 90%+ of affiliates report satisfaction with dashboard usability and data transparency

### System Performance Metrics

- **SC-015**: Discount code validation at checkout completes in under 500ms for 95% of requests
- **SC-016**: Affiliate commission calculations processed within 1 hour of booking completion
- **SC-017**: System supports 100+ active affiliates with 10,000+ code applications per month without performance degradation
- **SC-018**: Payout batch processing completes within 30 minutes for up to 100 affiliates per month

### Business Impact Metrics

- **SC-019**: Affiliate program generates 15%+ of total patient acquisition within 6 months of launch
- **SC-020**: Average cost per acquisition via affiliates is 30%+ lower than paid advertising channels
- **SC-021**: Affiliate-referred patients have 25%+ higher lifetime value (repeat bookings) compared to direct patients
- **SC-022**: 80%+ of active affiliates remain in program for 12+ months (low churn rate)
- **SC-023**: Affiliate program expands Hairline's reach to 5+ new geographic markets within 12 months

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **FR-007 / Module S-02: Payment Processing Service**
  - **Why needed**: Affiliate commission payouts require Stripe integration to process bank transfers to affiliates
  - **Integration point**: Payout processing workflow calls Payment Service API to initiate Stripe transfers with the affiliate's stored bank account details

- **FR-015 / Module A-02: Provider Management & Onboarding**
  - **Why needed**: Affiliate account activation and profile self-service reuse the provider activation and self-service patterns for consistency across roles of the same nature
  - **Integration point**: Activation email + one-time set-password link flow (and resend) mirrors FR-015; affiliate Profile tab mirrors the provider profile self-service model (FR-032) with a leaner field set

- **FR-017 / Module A-05: Admin Billing & Financial Management**
  - **Why needed**: Affiliate payout execution and reconciliation are owned by FR-017 / A-05 using payout-cycle data calculated by FR-018
  - **Integration point**: FR-018 exposes affiliate payout-cycle totals, readiness, threshold exclusions, and reconciliation metadata; FR-017 / A-05 initiates Stripe transfers and returns payout execution status for FR-018 read-only views

- **FR-019 / Module A-06: Discount & Promotion Management**
  - **Why needed**: Affiliate discount codes are a subset of platform-wide discount system
  - **Integration point**: FR-018 owns affiliate-specific code generation and assignment; generated codes are registered into FR-019 promotion services for validation, active windows, usage limits, applied/completed redemption lifecycle, and financial-impact logging

- **FR-029 / Module S-02: Payment System Configuration (Currency & FX)**
  - **Why needed**: Affiliate amounts are denominated in USD (platform base currency) and bookings may be transacted in other currencies; FR-029 is the single owner of the supported-currency list, base currency, conversion-rate sources, markup, and locked exchange rates
  - **Integration point**: FR-018 reads the USD-converted value and the booking's locked exchange rate from FR-029's currency service to compute commission; FR-018 never defines or overrides its own FX rate, ensuring no discrepancy with billing/finance figures (FR-017)

- **FR-006 / FR-007 / Module P-03: Booking & Scheduling and Payment Processing**
  - **Why needed**: Affiliate code application occurs during patient booking checkout flow
  - **Integration point**: Patient platform sends discount code to booking service for validation and application

- **FR-001 / Module P-01: Patient Authentication & Profile Management**
  - **Why needed**: Track which patients used affiliate codes (without exposing patient identity to affiliate)
  - **Integration point**: Booking records link patient ID to affiliate code for internal tracking (anonymized in affiliate dashboard)

### External Dependencies (APIs, Services)

- **External Service 1: Stripe Payment API (via FR-017 / S-02)**
  - **Purpose**: FR-017 processes affiliate commission payouts as Stripe transfers using affiliate bank account details and commission amounts from FR-018 (account configuration owned by FR-029)
  - **Integration**: FR-018 exposes calculated payout data and reads back payout execution status; FR-017 / S-02 initiates Stripe transfers and consumes `transfer.created` / `transfer.paid` / `transfer.failed` webhooks
  - **Failure handling**: If a transfer fails, FR-017 marks the payout "Failed", alerts admin for manual retry after resolving bank details, and FR-018 displays the latest status read-only

- **External Service 2: Email Service Provider (e.g., SendGrid)**
  - **Purpose**: Send activation, payout confirmation emails and discount code notifications to affiliates
  - **Integration**: SMTP or API-based email sending with templated messages
  - **Failure handling**: If email fails, system logs error and admin can manually resend via dashboard

- **External Service 3: PDF Generation Library (e.g., wkhtmltopdf, Puppeteer)**
  - **Purpose**: Generate downloadable performance reports and payout receipts for affiliates
  - **Integration**: Server-side PDF generation from HTML templates
  - **Failure handling**: If PDF generation fails, system displays HTML version and allows manual retry

- **External Service 4: Externally Hosted Marketing Materials**
  - **Purpose**: Provide read-only affiliate access to banners, templates, and campaign assets referenced by assigned campaigns
  - **Integration**: FR-018 stores or displays approved external URLs/asset references only; it does not create, edit, approve, or host marketing materials
  - **Failure handling**: If a material link is unavailable, the portal shows the unavailable state and keeps code/referral workflows functional

### Data Dependencies

- **Entity 1: Active Affiliate Accounts**
  - **Why needed**: Cannot create discount codes or prepare payout cycles without onboarded affiliate accounts
  - **Source**: Admin creates affiliate accounts via Affiliate Management module

- **Entity 2: Completed Bookings with Payment Confirmation**
  - **Why needed**: Affiliate commissions calculated only for completed bookings where patient has paid in full
  - **Source**: Booking & Payment Processing module P-03 (FR-006 Booking & Scheduling / FR-007 Payment Processing) provides booking completion events

- **Entity 3: Discount Code Catalog**
  - **Why needed**: System must validate affiliate codes at checkout against active discount code database
  - **Source**: Admin creates single or bulk affiliate-bound codes in FR-018; FR-019 stores and validates the shared promotion lifecycle

- **Entity 4: Affiliate Segment or Filter Result**
  - **Why needed**: Bulk generation requires a selected affiliate set or a saved filter snapshot
  - **Source**: Affiliate Management Dashboard filters and manual selection in FR-018

---

## Assumptions

### User Behavior Assumptions

- **Assumption 1**: Affiliates will check their dashboard at least once per week to monitor performance
- **Assumption 2**: Patients will correctly enter affiliate discount codes (uppercase/lowercase variations handled by system)
- **Assumption 3**: Affiliates prefer monthly payouts over weekly/bi-weekly schedules (fewer transactions, easier accounting)
- **Assumption 4**: Affiliates will primarily use code-based discounts (manual entry) rather than auto-apply links

### Technology Assumptions

- **Assumption 1**: Affiliates access dashboard via modern web browsers (Chrome, Safari, Firefox - last 2 versions)
- **Assumption 2**: Stripe supports batch transfer processing for multiple affiliates simultaneously
- **Assumption 3**: Email service provider has 99.9%+ deliverability rate for transactional emails
- **Assumption 4**: Server infrastructure can handle up to 1000 discount code validation requests per minute during peak periods

### Business Process Assumptions

- **Assumption 1**: Hairline will manually vet and approve affiliate partners before onboarding (no self-service affiliate signup)
- **Assumption 2**: Affiliate commission structure will remain stable (5-25% of booking revenue or $50-$200 fixed per booking)
- **Assumption 3**: Finance team will reconcile affiliate payouts within 48 hours of processing to detect errors
- **Assumption 4**: Affiliate program will not exceed 10% of Hairline's total commission revenue within first 12 months (cost control)

---

## Implementation Notes

### Technical Considerations

- **Architecture**: Affiliate module requires event-driven architecture to trigger commission calculations when bookings complete
- **Code ownership**: Affiliate-specific code generation, assignment, and dashboard display live in FR-018; FR-019 remains the reusable promotion engine for validation and redemption state
- **Technology**: Discount code validation should use in-memory caching (Redis) to minimize database queries during checkout
- **Performance**: Commission calculation jobs should run asynchronously to avoid blocking booking confirmation workflow
- **Storage**: Audit trail requires append-only data storage for all affiliate transactions (no deletions, only inserts)
- **Shared screens**: Promo Code Detail (Screen 6) and Payout / Transaction Detail (Screen 8) are implemented once and reused across both entry points; route params carry the originating context for breadcrumbs only, not for behavior changes

### Integration Points

- **Integration 1: Patient Booking Checkout → Affiliate Code Validation**
  - **Data format**: JSON payload with discount code, patient ID (anonymized), booking total
  - **Authentication**: Internal service-to-service API with JWT tokens
  - **Error handling**: If validation service unavailable, allow checkout to proceed without discount (prevent checkout failure)

- **Integration 1a: FR-018 Affiliate Code Generation → FR-019 Promotion Registration**
  - **Data format**: JSON payload with campaign name, affiliate ID, generated code text, discount type/value, active window, usage limits, application method, and attribution metadata
  - **Authentication**: Internal service-to-service API with admin user context for audit
  - **Error handling**: If FR-019 registration fails for a generated code, mark that affiliate row as failed and allow admin to retry without duplicating successful rows

- **Integration 2: Booking Completion Event → Commission Calculation**
  - **Data format**: Event payload with booking ID, affiliate attribution code/link (if captured), final discount applied, final payment amount, Hairline commission amount
  - **Authentication**: Internal event bus with message authentication
  - **Error handling**: If commission calculation fails, retry 3 times with exponential backoff; alert admin if all retries fail

- **Integration 3: FR-018 Payout Data → FR-017 Affiliate Billing Execution**
  - **Data format**: JSON payload/API response with affiliate ID, payout period, completed booking count, gross commission, reversals/refunds, net amount, threshold exclusion status, payout readiness, masked destination reference, and audit metadata
  - **Authentication**: Internal service-to-service API with A-05 admin context and immutable audit metadata; Stripe authentication is handled only by FR-017 / S-02
  - **Error handling**: If FR-017 payout execution fails, FR-017 marks the payout "Failed" and FR-018 reads back the latest status/failure reason for read-only display

### Scalability Considerations

- **Current scale**: Expected 20-30 active affiliates at launch, 500-1000 code applications per month
- **Growth projection**: Plan for 100+ affiliates within 12 months, 10,000+ code applications per month
- **Peak load**: Handle 100 simultaneous discount code validations during promotional campaigns
- **Data volume**: Expect 50,000+ affiliate transaction records per year (code applications, commission calculations, payouts)
- **Scaling strategy**: Horizontal scaling of API services; database partitioning by affiliate ID for transaction history

### Security Considerations

- **Authentication**: Affiliates access dashboard via username/password; support MFA (optional — future / non-MVP, pending the shared MFA stack FR-026 / FR-031 per constitution Principle II) for high-value affiliates
- **Authorization**: Role-based access control (RBAC): Affiliates view only their own data; Admins view all affiliate data
- **Encryption**: All affiliate bank account details encrypted at rest using AES-256; TLS 1.3 for data in transit
- **Audit trail**: Log all access to affiliate payment details with timestamp, user ID, and IP address
- **Threat mitigation**: Rate limiting on dashboard API (100 requests/minute/user) to prevent abuse; CAPTCHA on affiliate login after 3 failed attempts; activation link is one-time and expires in 24 hours
- **Compliance**: PCI-DSS compliance for handling affiliate bank account details; GDPR compliance for affiliate personal data (right to deletion)

---

## User Scenarios & Testing

### User Story 1 - Affiliate Onboarding and First Code Creation (Priority: P1)

Admin onboards new affiliate partner, creates discount code, and affiliate accesses dashboard to view initial setup.

**Why this priority**: Core functionality required for affiliate program to launch; without this, no affiliates can join or promote platform.

**Independent Test**: Can be fully tested by creating affiliate account, generating discount code, and verifying affiliate receives the activation link and can access dashboard after setting a password.

**Acceptance Scenarios**:

1. **Given** admin is logged into admin dashboard, **When** admin navigates to Affiliate Management and clicks "Add New Affiliate", **Then** system displays affiliate onboarding form with all required fields
2. **Given** admin fills affiliate details (name, email, bank account details, commission structure), **When** admin submits form, **Then** system creates affiliate account and sends an activation email with a one-time set-password link within 2 minutes
3. **Given** affiliate account is created, **When** admin creates discount code linked to affiliate, **Then** system validates code uniqueness and saves code with "Active" status
4. **Given** discount code is created, **When** affiliate completes the activation link, sets a password, and logs into the dashboard, **Then** system displays the Affiliate Portal Overview with discount code details and "0 referrals" initial state

---

### User Story 1a - Bulk Affiliate Code Generation (Priority: P1)

Admin generates unique promo codes for a filtered group of affiliates without creating shared attribution.

**Why this priority**: Bulk generation keeps affiliate campaign operations manageable as the program grows while preserving clear one-code-to-one-affiliate payout attribution.

**Independent Test**: Can be tested by creating multiple active affiliates, filtering/selecting them, generating one code per affiliate, and verifying every generated code appears in the correct affiliate dashboard.

**Acceptance Scenarios**:

1. **Given** admin filters Affiliate Management by country "United Kingdom" and status "Active", **When** admin selects all results and clicks "Generate Codes", **Then** system opens a bulk generation form with the selected affiliate count
2. **Given** admin enters campaign name, code pattern, discount value, active window, and usage limits, **When** admin confirms generation, **Then** system creates one unique affiliate-bound code per selected affiliate and links each code to exactly one affiliate
3. **Given** generated codes are active, **When** each affiliate logs into the dashboard, **Then** that affiliate sees only their own generated code(s), campaign name, status, active window, and zero-referral initial stats
4. **Given** one selected affiliate is no longer eligible during generation, **When** the batch runs, **Then** system skips that affiliate, reports the reason in the Code Generation Results screen, and does not block successful code creation for other affiliates

---

### User Story 1b - Affiliate Account Activation (Priority: P1)

Affiliate completes the one-time activation link to set a password and gain portal access, mirroring the provider activation flow.

**Why this priority**: Without completing activation, an onboarded affiliate cannot log in; consistency with the provider flow keeps onboarding predictable across roles.

**Independent Test**: Can be tested by creating an affiliate, opening the activation link, setting a password, and logging in; and by exercising the resend path for an expired link.

**Acceptance Scenarios**:

1. **Given** an affiliate account is created, **When** the affiliate opens the one-time "Set Password" link within 24 hours, **Then** system displays the password creation form and accepts a strong password
2. **Given** the affiliate sets a valid password, **When** they submit, **Then** system saves the encrypted password, marks Activation Status "Active", and redirects to the portal login
3. **Given** the activation link expired, **When** the affiliate requests a resend, **Then** system invalidates the old link, sends a fresh one, and rate-limits to 3 requests per hour
4. **Given** an unknown or already-activated email, **When** a resend is requested, **Then** system shows a generic message without revealing whether the email exists

---

### User Story 2 - Patient Applies Affiliate Code at Checkout (Priority: P1)

Patient discovers affiliate discount code, applies it during booking checkout, and receives discounted price.

**Why this priority**: Core user journey that drives affiliate referrals and patient conversions; essential for MVP.

**Independent Test**: Can be tested by creating test affiliate code, simulating patient checkout, and verifying discount is applied correctly.

**Acceptance Scenarios**:

1. **Given** patient is at booking checkout with $1000 total, **When** patient enters valid affiliate code "PARTNER10" (10% discount), **Then** system validates code and applies $100 discount (total becomes $900)
2. **Given** patient applies affiliate code, **When** patient completes payment, **Then** system records booking with affiliate code and triggers commission calculation for affiliate
3. **Given** patient attempts to apply expired affiliate code, **When** system validates code, **Then** system displays error message "This discount code is no longer valid" and checkout proceeds without discount
4. **Given** patient applies affiliate code that reached usage limit, **When** system validates code, **Then** system displays error message and prevents code application

---

### User Story 3 - Affiliate Views Real-Time Performance Dashboard (Priority: P2)

Affiliate logs into dashboard to check referral count, commission earnings, and upcoming payout details.

**Why this priority**: Critical for affiliate engagement and transparency; affiliates need visibility into earnings to stay motivated.

**Independent Test**: Can be tested by creating affiliate account with simulated referrals and verifying dashboard displays accurate statistics.

**Acceptance Scenarios**:

1. **Given** affiliate has 10 completed referrals generating $5000 total revenue, **When** affiliate logs into dashboard, **Then** system displays accurate statistics: 10 referrals, $5000 revenue, $750 commission earned (15% of the $5000 booking revenue)
2. **Given** affiliate has pending payout of $750, **When** affiliate views dashboard, **Then** system displays "Next payout: $750 on December 7, 2025"
3. **Given** affiliate has multiple discount codes, **When** affiliate clicks on individual code, **Then** system displays per-code breakdown: usage count, conversion rate, revenue, commission earned
4. **Given** affiliate wants performance report, **When** affiliate clicks "Download Report", **Then** system generates PDF report with all-time statistics and payout history

---

### User Story 4 - Admin Reviews Monthly Affiliate Payout Data for A-05 Execution (Priority: P1)

Admin reviews the automatically generated affiliate payout cycle on the 7th of the month and verifies that the calculated commission data is available to FR-017 / A-05 for payout execution.

**Why this priority**: Core handoff required to fulfill affiliate commission obligations; FR-018 calculates and exposes the payout data, while FR-017 / A-05 executes the money movement.

**Independent Test**: Can be tested by triggering monthly payout calculation, verifying FR-018 read-only payout status/history, and confirming FR-017 receives the same payout cycle totals, readiness, and threshold exclusions for execution.

**Acceptance Scenarios**:

1. **Given** it is December 7th, 2025, **When** automated payout calculation runs, **Then** FR-018 generates a payout list for all affiliates with completed bookings in November 2025
2. **Given** payout data lists 5 affiliates owed total $3500, **When** FR-017 requests the payout cycle, **Then** FR-018 exposes the same affiliate count, net amount, threshold exclusions, payout readiness, and reconciliation metadata
3. **Given** FR-017 payout processing completes successfully, **When** Stripe confirms the transfers in A-05, **Then** FR-018 displays the payout rows as "Paid" and affiliate-facing payout history reflects the transaction references
4. **Given** one payout fails due to invalid bank account, **When** FR-017 marks that payout "Failed", **Then** FR-018 displays the failed status and failure reason in read-only payout views

---

### User Story 5 - Affiliate Commission Calculation for Completed Booking (Priority: P1)

System automatically calculates affiliate commission when patient completes booking using affiliate code.

**Why this priority**: Core business logic that ensures affiliates are credited correctly; must be accurate to maintain trust.

**Independent Test**: Can be tested by simulating booking completion with affiliate code and verifying commission calculation matches expected formula.

**Acceptance Scenarios**:

1. **Given** patient books $1000 treatment using affiliate code "PARTNER10" (10% discount), **When** patient completes payment of $900, **Then** system calculates the affiliate commission as 15% of the $1000 booking revenue = $150, funded from Hairline's commission (not the provider payout)
2. **Given** affiliate has fixed commission structure of $50 per booking, **When** patient completes booking using affiliate code, **Then** system credits affiliate account with $50 commission regardless of booking value
3. **Given** booking is completed with affiliate code, **When** commission calculation completes, **Then** system updates affiliate dashboard with new referral count and commission earned in real-time
4. **Given** patient refunds booking after completion, **When** refund is processed, **Then** system reverses affiliate commission and deducts the $150 from affiliate's pending payout

---

### User Story 6 - Admin Edits Affiliate Commission Structure Mid-Program (Priority: P2)

Business negotiates new commission terms with affiliate; admin updates commission structure with effective date.

**Why this priority**: Important for business flexibility and affiliate relationship management; not required for MVP but needed for scaling.

**Independent Test**: Can be tested by editing affiliate commission structure and verifying new rates apply only to future bookings.

**Acceptance Scenarios**:

1. **Given** affiliate currently has 15% commission rate, **When** admin edits commission structure to 20% with effective date December 1, 2025 (via Screen 3.2), **Then** system saves new rate and applies to bookings completed on/after December 1st
2. **Given** affiliate has pending payout for November 2025 bookings, **When** admin changes commission rate in December, **Then** November payout is calculated using old 15% rate (no retroactive changes)
3. **Given** commission structure is updated, **When** system sends notification to affiliate, **Then** email includes old rate, new rate, and effective date for transparency
4. **Given** admin sets effective date in past, **When** system validates edit, **Then** system displays error: "Effective date cannot be in the past" and prevents save

---

### Edge Cases

- What happens when **affiliate has $45 pending payout (below $50 minimum threshold)**? System does NOT process payout; commission rolls over to next month until threshold is reached.
- How does system handle **duplicate discount codes across different affiliates**? System validates uniqueness across ALL affiliates; if code exists, displays error "Code already exists for affiliate [name]".
- What happens if **admin tries to assign the same code to multiple affiliates**? System blocks the action and requires one unique code per affiliate, or redirects admin to create a non-attributed open marketing code in FR-019.
- What happens if **bulk generation filter results change after code generation**? Existing generated codes remain tied to the original selected affiliates; admin must run a new bulk generation action for newly eligible affiliates.
- What occurs if **patient applies affiliate code but cancels booking before payment**? System tracks code as "applied" but NOT "completed"; no commission credited to affiliate.
- How to manage **affiliate account suspension while pending payout exists**? Pending commission is held pending investigation; if suspension is lifted, payout processes normally; if permanent ban, pending commission is forfeited.
- What happens when **the Stripe transfer API is down during payout processing**? System retries 3 times with exponential backoff; if all retries fail, marks payouts as "Failed" and alerts admin to retry manually next day.
- How does system handle **booking refund after affiliate payout has been processed**? System tracks negative balance for affiliate; deducts refunded commission from next payout (if next payout insufficient, carries negative balance forward).
- What happens when **affiliate's activation link expires before use**? Affiliate (or admin) requests a resend; the old link is invalidated and a fresh 24-hour link is sent, rate-limited to 3 per hour per email.
- What happens when **a partnership ends (affiliate offboarded)**? Admin deactivates via Screen 3.3 (B5): status → Inactive (terminal), codes disabled, portal read-only, historical data retained, and the net final balance is settled if ≥ $50, forfeited if below $50, or written off if negative — each audited.
- What happens when **an affiliate is offboarded while carrying a negative balance** (reversals exceeded accrued commission)? The unrecoverable negative balance is written off on deactivation with an audit entry, since no future payouts exist to net against.
- What happens when **a patient referred by an affiliate uses or receives a higher-priority patient/provider discount code instead**? The higher-priority discount controls the patient's final price under the one-discount rule, but the affiliate referral attribution is preserved internally if the affiliate-bound code/link was validly captured for the booking journey. When the booking completes with payment confirmation, affiliate commission and referral credit are still counted for that affiliate per Rule 11.

---

## Functional Requirements Summary

### Core Requirements

- **REQ-018-001**: System MUST allow admins to onboard affiliates with unique email, bank account details, and commission structure (percentage or fixed amount)
- **REQ-018-002**: System MUST generate unique affiliate discount codes with configurable parameters (discount amount, expiration date, usage limits)
- **REQ-018-003**: System MUST validate affiliate-bound codes/links during the patient booking journey, apply the affiliate discount from Hairline's commission when it is the final price discount, and preserve valid affiliate referral attribution for commission/reporting when another higher-priority discount controls the final price
- **REQ-018-004**: System MUST track discount code applications separately as "applied" (code entered) and "completed" (booking paid), and MUST decrement code usage caps (Maximum Usage Count, Per-Patient Usage Limit) on "completed" redemptions only, with a separate soft rate limit guarding "applied" events against spam
- **REQ-018-005**: System MUST calculate affiliate commission automatically when booking completes with payment confirmation
- **REQ-018-006**: System MUST provide affiliates with real-time dashboard showing referral count, revenue generated, commission earned, and pending payout
- **REQ-018-007**: System MUST generate monthly payout list automatically on 7th of each month for previous month's completed bookings
- **REQ-018-008**: System MUST expose affiliate commission payout data to FR-017 / A-05 for Stripe transfer execution to the affiliate's bank account (no PayPal or other payout method)
- **REQ-018-009**: System MUST send payout confirmation emails to affiliates with transaction details within 24 hours of payment processing
- **REQ-018-010**: System MUST enforce single discount code per booking rule for the patient's final price (priority: Patient code > Provider code > Affiliate code) while preserving valid affiliate referral attribution separately for commission and reporting when a provider-side or other higher-priority promotion supersedes the affiliate discount line
- **REQ-018-024**: System MUST allow admins to bulk-generate affiliate promo codes for selected affiliates or filtered affiliate segments
- **REQ-018-025**: System MUST create one distinct unique code per affiliate during bulk affiliate code generation; one shared affiliate payout code across multiple affiliates is not supported
- **REQ-018-026**: System MUST publish generated active affiliate codes to each assigned affiliate's dashboard immediately after successful creation
- **REQ-018-027**: System MUST provide an admin Affiliate Detail screen consolidating account details, assigned codes, and payout history/upcoming payout for a single affiliate
- **REQ-018-028**: System MUST provide a system-wide Promo Code Management list and a shared per-code Promo Code Detail screen (reachable from both the management list and the Affiliate Detail codes list) showing the assigned affiliate and code performance
- **REQ-018-029**: System MUST provide a shared Payout / Transaction Detail screen reachable from both the global payout list and an affiliate's payout list, with identical layout and capabilities from both entry points
- **REQ-018-030**: System MUST onboard affiliates via a one-time secure activation link (set password, expires 24 hours) mirroring the provider activation flow, including activation-email resend (self-service and admin-triggered) rate-limited to 3 requests per hour per email
- **REQ-018-031**: System MUST provide affiliates a portal with Overview, Promo Codes, Payouts, and Profile tabs, where affiliates can self-edit only non-sensitive profile fields (phone, language) while name (legal/payout name), payment details, commission, and status remain read-only/admin-controlled
- **REQ-018-032**: System MUST present a Code Generation Results view after bulk generation showing created/skipped/failed counts with per-row reasons and a retry-failed-only action that never duplicates successful codes
- **REQ-018-033**: System MUST provide a Suspend/Reinstate action (with required reason and confirmation) that disables the affiliate's codes and holds pending payouts on suspension
- **REQ-018-034**: System MUST capture an effective date for commission-structure changes and apply new rates only to bookings completed on/after that date (no retroactive recalculation)
- **REQ-018-035**: System MUST expose monthly affiliate payout cycle data to FR-017 / A-05, including total amount, affiliate count, threshold exclusions below $50, payout readiness, and reconciliation metadata before A-05 initiates Stripe transfers
- **REQ-018-038**: System MUST provide affiliate onboarding/activation screens — Set Password (activation landing), Resend Activation, and Welcome / Get Started (first login) — mirroring the provider activation flow (FR-015)
- **REQ-018-039**: System MUST provide an Offboarding / Deactivation action (Screen 3.3, with required reason and confirmation) that moves an affiliate to the terminal **Inactive** state: disabling all the affiliate's codes, converting portal access to read-only, retaining historical data, and performing explicit final settlement — pay net balance ≥ $50, forfeit a residual below $50, or write off a negative balance — each recorded in the audit trail. Inactive is distinct from Suspended (temporary, reversible) and is not silently reinstated
- **REQ-018-040**: System MUST denominate all affiliate amounts (commission, balances, thresholds, payouts) in USD (platform base currency) and MUST source every non-USD-to-USD conversion and exchange rate exclusively from FR-029 (Payment System Configuration) using the rate locked for the underlying booking — FR-018 MUST NOT define, cache, or override its own FX rate
- **REQ-018-041**: System MUST validate at affiliate code creation/generation that the combined Hairline-funded cost on a booking (patient-facing affiliate discount + affiliate commission) does not exceed Hairline's own commission on that booking (Rule 15); percentage breaches MUST be blocked (override requires documented, audited business approval) and fixed-amount configurations MUST raise a review warning
- **REQ-018-042**: System MUST provide affiliates read-only access to externally hosted marketing materials (banners, templates, campaign assets) linked to assigned codes/campaigns, while creation, editing, approval, and hosting of those materials remain outside FR-018 scope

### Data Requirements

- **REQ-018-011**: System MUST maintain affiliate account records with contact details, payment information (encrypted), commission structure, and status
- **REQ-018-012**: System MUST link discount codes to affiliate accounts with one-to-many relationship (one affiliate can have multiple codes)
- **REQ-018-013**: System MUST store booking records with affiliate code reference for commission tracking
- **REQ-018-014**: System MUST maintain payout history with transaction ID, date, amount, status for minimum 7 years (audit compliance)
- **REQ-018-036**: System MUST record affiliate activation state (Invited until password set, Active after) and last login timestamp
- **REQ-018-037**: System MUST collect affiliate bank details for payouts (account holder name, bank name, account number, routing/SWIFT code, optional IBAN), mirroring provider billing details (FR-032), with format validation via S-02, encryption at rest, and last-4 masking in the UI

### Security & Privacy Requirements

- **REQ-018-015**: System MUST encrypt affiliate bank account details at rest using AES-256
- **REQ-018-016**: System MUST mask affiliate bank account numbers in UI (display last 4 digits only)
- **REQ-018-017**: System MUST anonymize patient identity in affiliate dashboard (affiliates see only aggregated statistics, not patient names)
- **REQ-018-018**: System MUST log all affiliate-related transactions (code usage, commission calculations, payouts) with timestamp, user ID, and action type, in an immutable (append-only) audit trail retained for a minimum of 10 years (per constitution)
- **REQ-018-019**: System MUST require secure authentication for affiliate dashboard access (username/password with optional MFA — MFA is a future / non-MVP control pending the shared MFA stack FR-026 / FR-031 per constitution Principle II)

### Integration Requirements

- **REQ-018-020**: System MUST expose API for discount code validation during patient checkout (response time <500ms)
- **REQ-018-021**: System MUST integrate with FR-017 / A-05 payout execution status so FR-018 read-only payout views reflect Stripe transfer status, transaction references, and failure reasons without initiating transfers directly
- **REQ-018-022**: System MUST integrate with email service provider to send affiliate notifications (activation, onboarding, payouts, code creation)
- **REQ-018-023**: System MUST emit booking completion events to trigger affiliate commission calculation asynchronously

---

## Key Entities

- **Entity 1 - Affiliate Account**
  - **Key attributes**: Affiliate ID (unique), Name, Contact Email (unique), Phone Number, Language(s), Country/Region, Affiliate Type, Tax/VAT/Business Reg ID, Bank Account Details (account holder name, bank name, account number [encrypted], routing/SWIFT code, IBAN optional), Commission Type (Percentage/Fixed), Commission Value, Payout Schedule, Status (Pending/Active/Suspended/Inactive), Activation Status (Invited until password set / Active), Performance Tier (system-calculated), Last Login, Created Date
  - **Relationships**: One affiliate can have many discount codes; one affiliate can have many payouts; one affiliate can be linked to many bookings (via discount codes)

- **Entity 2 - Discount Code**
  - **Key attributes**: Code ID (unique), Code Text (unique, case-insensitive), Linked Affiliate ID (foreign key), Campaign Name, Generation Mode (Single Affiliate / Selected Affiliates / Filtered Segment), Discount Type (Hairline Fees Only), Discount Amount Type (Percentage/Fixed), Discount Value, Application Method (Auto-apply/Code-based), Expiration Date (optional), Max Usage Count (optional), Per-Patient Usage Limit, Current Usage Count, Marketing Material Links (optional external URLs), Status (Active/Inactive/Expired/Revoked), Created Date
  - **Relationships**: One code belongs to one affiliate; one code can be applied to many bookings

- **Entity 2a - Affiliate Code Generation Batch**
  - **Key attributes**: Batch ID (unique), Campaign Name, Admin User ID, Generation Mode, Filter Snapshot or Selected Affiliate IDs, Code Pattern, Requested Count, Created Count, Skipped Count, Failed Count, Created Date, Status (Completed/Partial/Failed)
  - **Relationships**: One batch creates many affiliate discount codes; each generated code still belongs to exactly one affiliate

- **Entity 3 - Booking with Affiliate Attribution**
  - **Key attributes**: Booking ID (unique), Patient ID (anonymized in affiliate views), Affiliate Attribution Code/Link (foreign key, if captured), Final Discount Applied (foreign key, may be patient/provider/affiliate), Booking Total, Discount Applied, Hairline Commission, Affiliate Commission Owed, Booking Status (Pending/Completed/Refunded), Completion Date
  - **Relationships**: One booking can preserve one affiliate attribution source (if captured); one booking has one final applied discount for price calculation; one booking belongs to one patient; one booking contributes to one payout

- **Entity 4 - Affiliate Payout**
  - **Key attributes**: Payout ID (unique), Affiliate ID (foreign key), Payout Month, Total Bookings Count, Total Commission Amount, Reversals/Refunds, Net Amount, Stripe Transfer ID, Payout Date, Status (Pending/Processing/Paid/Failed), Failure Reason, Admin Notes (internal), Created Date
  - **Relationships**: One payout belongs to one affiliate; one payout summarizes many bookings; one payout maps to one FR-017 / A-05 Stripe transfer record once execution begins

- **Entity 5 - Affiliate Transaction Log (Audit Trail)**
  - **Key attributes**: Log ID (unique), Affiliate ID (foreign key), Action Type (Code Created, Code Applied, Commission Calculated, Payout Processed, Status Changed, Activation Sent, etc.), Timestamp, User ID (admin or system), IP Address, Metadata (JSON with action details)
  - **Relationships**: One log entry belongs to one affiliate; many log entries track lifecycle of affiliate account

---

## Appendix: Change Log

| Date | Version | Changes | Author |
| --- | --- | --- | --- |
| 2025-11-12 | 1.0 | Initial PRD creation for FR-018 | Claude (AI) |
| 2026-06-22 | 1.1 | Added FR-018 ownership for affiliate promo code generation and assignment, including filtered bulk generation with one distinct code per affiliate; clarified FR-019 integration boundary, affiliate dashboard visibility, one-affiliate-per-code attribution, success criteria, requirements, entities, and testing coverage | Codex |
| 2026-06-22 | 1.2 | Restructured Screen Specifications by tenant/platform using verified PRD convention: Admin Platform screens and Affiliate Platform screens, with patient/provider scope clarified as out of this FR | Codex |
| 2026-06-22 | 1.3 | Expanded screen architecture: added Affiliate Detail (Screen 3), Code Generation Results (Screen 5), system-wide Promo Code Management (Screen 6), shared Promo Code Detail (Screen 7) and shared Payout/Transaction Detail (Screen 9), consolidated Payout Management with folded Billing History (Screen 8), and Modals A-C (Suspend/Reinstate, Edit Commission, Confirm Batch Payout); reframed code generation as Screen 4; restructured the affiliate portal into Overview/Promo Codes/Payouts/Profile tabs (Screen 10) with self-service profile; added affiliate activation flow mirroring FR-015 (one-time set-password link + resend); added Add/Edit fields (phone, language, tax/VAT ID, performance tier, activation status, last login); added REQ-018-027 through REQ-018-036 and related rules, entities, and testing | Claude (AI) |
| 2026-06-22 | 1.4 | Standardized affiliate payouts on Stripe (consistent with the rest of the system) and removed PayPal/Other payout methods; replaced the generic payment-method fields with a provider-mirrored bank-detail set (account holder name, bank name, account number, routing/SWIFT, optional IBAN) per FR-032, encrypted at rest and last-4 masked; aligned payout screens, workflows, business/billing rules, dependencies, integrations, security, entities, and testing to Stripe transfers (executed via FR-017 / S-02 using FR-029 Stripe accounts); added REQ-018-037 (bank-detail collection) | Claude (AI) |
| 2026-06-22 | 1.6 | Expanded affiliate portal tab screens (9.2 Promo Codes, 9.3 Payouts, 9.4 Profile) with full field lists (list-row + detail fields, editable vs admin-controlled, account-security); added the missing affiliate onboarding/activation screen group — Screen 10 (Affiliate Onboarding & Activation) with 10.1 Set Password, 10.2 Resend Activation, and 10.3 Welcome / Get Started — mirroring the provider activation flow (FR-015); added REQ-018-038 and updated the tenant-scope note; corrected REQ-018-035 wording to Stripe transfers | Claude (AI) |
| 2026-06-22 | 1.7 | Lifecycle-integrity pass from FR-018 verification: (1) added Affiliate Offboarding/Deactivation — workflow B5, Screen 3.3, Rule 12, REQ-018-039 — defining the terminal Inactive state (codes disabled, portal read-only, final balance settled/forfeited/written-off incl. negative-balance write-off); (2) standardized currency on USD with all FX/conversion sourced from FR-029 (Currency Rule rewrite, REQ-018-040, FR-029 dependency, all $→USD literals); (3) documented code-based attribution as accepted policy (Rule 11) — affiliate earns only when its code is the applied discount; corrected/superseded by v2.3, where valid captured affiliate attribution can earn commission even when a higher-priority discount controls the final price; (4) recognized the Affiliate Portal as a scoped external surface of the Admin tenant (Module Scope note + constitution Principle I amendment); (5) clarified usage caps decrement on completed redemptions only with a soft applied-event rate limit (Rule 13, REQ-018-004, code-config screen); (6) added Pending initial status; (7) made affiliate name (legal/payout name) admin-controlled, removed from affiliate self-service | Claude (Opus 4.8) |
| 2026-06-22 | 1.5 | Adopted decimal sub-screen notation (FR-033 convention): modals renumbered to sub-screens under their parent (Screen 3.1 Suspend/Reinstate, Screen 3.2 Edit Commission, Screen 7.1 Confirm Batch Payout); Code Generation Results confirmed as a full screen and renumbered Screen 4.1; sequentially renumbered the remaining admin screens (Promo Code Management 6→5, Promo Code Detail 7→6, Payout Management 8→7, Payout/Transaction Detail 9→8); split the affiliate portal (former Screen 10) into a portal shell (Screen 9) with one screen per tab (9.1 Overview, 9.2 Promo Codes, 9.3 Payouts, 9.4 Profile); updated all cross-references, tenant-scope note, Implementation Notes, and user stories accordingly | Claude (AI) |
| 2026-06-23 | 2.1 | Follow-up boundary cleanup from FR-018 verification Issue 1 / Option 1: replaced remaining FR-018 payout-execution wording with payout-cycle calculation, review, handoff, and read-only status/history language; removed the stale Screen 7.1 tenant-scope reference; aligned shared-service labels to S-02 / S-03 / S-06 | Codex |
| 2026-06-23 | 2.0 | Verification-fix pass 3 (FR-018 verify-fr): applied Product Owner decisions from the v1.9 follow-up — (1) moved affiliate payout execution out of FR-018 and made Screen 7 / Screen 8 read-only payout status/history surfaces, with FR-017 / A-05 owning approval, retry, and Stripe transfer execution; updated B2, Integration 3, User Story 4, REQ-018-008, REQ-018-021, REQ-018-035, and Entity 4 accordingly; (2) corrected Screen 3 table links so promo-code rows open Screen 6 and payout rows open Screen 8; (3) added read-only affiliate access to externally hosted marketing materials on Screen 9.2 plus REQ-018-042 and the Discount Code entity attribute | Codex |
| 2026-06-23 | 1.9 | Verification-fix pass 2 (FR-018 verify-fr): (1) reconciled the initial affiliate **Status = "Pending"** on account creation across Screen 2, Screen 10, and Screen 10.1 — previously these said "Active" on create, contradicting Main Flow, Screen 1, and Rule 12; activation now flips Status and Activation Status to "Active" together; (2) added **Rule 15 (Hairline-funded cost ceiling)**, Screen 4 Margin Guard rule + AC-6, and **REQ-018-041** — the combined patient discount + affiliate commission may not exceed Hairline's commission on a booking (percentage breaches blocked with audited override; fixed-amount raises a review warning), resolving the v1.8 Finance follow-up; (3) added a Currency Rule note clarifying that client GBP figures are illustrative and USD literals are not a direct GBP→USD conversion | Claude (Opus 4.8) |
| 2026-06-23 | 1.8 | Verification-fix pass (FR-018 verify-fr): (1) set audit-trail retention to 10 years per constitution (financial/payout records remain 7-year minimum) — Audit Rule, REQ-018-018, Fixed-in-codebase, B3/B5 retention notes; (2) redefined the percentage commission base as **% of booking revenue** (not % of Hairline commission), added Rule 14, corrected the Screen 2 preview and the User Story 3/5 worked examples ($150, not $22.50), and aligned the system-prd FR-018 requirement line; (3) tightened commission bounds to 5-25% and fixed-amount min $50 (warning threshold 20%) to match the business assumption and client intent; (4) defined Performance Tier bands and Campaign Eligibility criteria (new Affiliate Segmentation Rules subsection); (5) standardized bank-account masking wording to "last 4 digits"; (6) made the payout schedule fixed at monthly-on-the-7th per the client transcription (removed all "configurable" date language; moved to Fixed-in-codebase) | Claude (Opus 4.8) |
| 2026-06-23 | 2.2 | Verification-fix pass (FR-018 verify-fr): (1) marked every MFA reference as a future / non-MVP control pending the shared MFA stack (FR-026 / FR-031) per constitution Principle II — Screen 9, Screen 9.4 toggle + self-service rule, Privacy Rule 3, Security Considerations, REQ-018-019; (2) corrected the FR-015 dependency module from A-04 to A-02 (Provider Management & Onboarding); (3) repointed the mislabeled "FR-003 / Booking & Payment Processing" dependency to FR-006 (Booking & Scheduling) / FR-007 (Payment Processing) under module P-03; (4) aligned Screen 1 "Total Referrals" to completed bookings (consistent with Screen 9.1 and Rule 11); (5) resequenced REQ-018-042 to follow REQ-018-041 | Claude (Opus 4.8) |
| 2026-06-23 | 2.3 | Product Owner decision after FR-018 verification: separated final discount priority from affiliate referral attribution. A higher-priority patient/provider discount can control the patient's price, but a valid captured affiliate-bound code/link still earns affiliate referral credit and commission after payment-confirmed booking completion. Updated Rule 11, referral-count wording, REQ-018-010, the edge case, and Booking with Affiliate Attribution entity. | Codex |
| 2026-06-23 | 2.4 | Marked PRD status as ✅ Verified & Approved after final `verify-fr FR-018` pass; updated approvals table to template-aligned verified approval state | Codex |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
| --- | --- | --- | --- |
| Product Owner | [Name] | 2026-06-23 | ✅ Verified & Approved |
| Technical Lead | [Name] | 2026-06-23 | ✅ Verified & Approved |
| Stakeholder | [Name] | 2026-06-23 | ✅ Verified & Approved |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-017 Admin Billing & Financial Management PRD
**Last Updated**: 2026-06-23
