# FR-029 - Payment System Configuration

**Module**: A-09: System Settings & Configuration
**Feature Branch**: `fr029-payment-system-config`
**Created**: 2025-11-13
**Status**: ✅ Verified & Approved
**Source**: FR-029 from system-prd.md (lines 1427-1455) + Hairline-AdminPlatformPart2.txt (lines 128-230)

---

## Executive Summary

The Payment System Configuration module empowers platform administrators to manage the complete payment infrastructure for the Hairline multi-tenant platform. This feature enables admins to configure and manage multiple Stripe accounts, map payment accounts to specific countries or regional groups, manage the platform’s enabled currency list (system-supported currencies), set up currency conversion rules with markup percentages, configure deposit rates (20-30% of total booking amount), configure platform commission rates (global default and provider-specific), and define split payment (installment) plans with cutoff rules.

This configuration layer is critical because Hairline operates across multiple countries with different currencies, banking systems, and regulatory requirements. Admins need the flexibility to assign different Stripe accounts to different regions, protect the platform against currency fluctuations through configurable markup rates, and offer patients flexible payment options (2-9 installments) while ensuring full payment completion before procedure dates.

The module delivers value by:

- Enabling multi-country payment operations with region-specific Stripe account management
- Making Stripe account assignments the rails for collecting patient payments (charges for deposits/installments) per region/country
- Protecting revenue through configurable currency conversion markup (e.g., 5% buffer)
- Increasing booking conversion rates by offering flexible deposit rates (20-30%) and installment plans
- Reducing manual administrative overhead through centralized payment configuration
- Ensuring compliance with regional payment regulations through proper account-to-region mapping

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-03)**: Uses configured payment settings during booking flow (deposit calculation, installment options)
- **Provider Platform (PR-05)**: No direct interaction (inherits region-based payment configuration; configuration is managed in Admin Platform)
- **Admin Platform (A-09)**: Full payment system configuration management interface
- **Shared Services (S-02)**: Payment Processing Service implements configured rules for Stripe integration, currency conversion, deposit/commission calculation, and installment rules

### Multi-Tenant Breakdown

**Patient Platform (P-03: Booking & Payment)**:

- Patients see deposit amount calculated based on admin-configured deposit rate (20-30%)
- Patients see available installment plan options (2-9 installments) filtered by cutoff date rule
- Patients see prices displayed in their selected currency using admin-configured conversion rates
- Patients cannot view or modify payment system configuration settings
- Patients experience seamless payment processing using the appropriate Stripe account for their region

**Provider Platform (PR-05: Financial Management & Reporting)**:

- Patient payments are collected into the Stripe account mapped to the patient’s region; provider payouts are later executed in FR-017 using those funds (provider bank details in FR-032). Providers do not configure Stripe accounts here.
- Providers have no direct interaction with payment system configuration
- Providers see booking payments processed according to deposit rates and installment rules
- Provider payout schedules follow the Stripe account’s settlement rules, but payout processing is handled in FR-017 (Admin Billing & Financial Management)

**Admin Platform (A-09: System Settings & Configuration)**:

- Admins manage multiple Stripe accounts with API key configuration
- Admins assign Stripe accounts to specific countries or regional groupings
- Admins enable/disable which currencies are available across the system (central supported currency list) and set the default currency
- Admins configure currency conversion rate sources (e.g., xe.com API integration)
- Admins set currency conversion markup percentages (e.g., 5-10%) to protect against rate fluctuations
- Admins configure deposit rate percentage (20-30%) globally or per provider
- Admins configure platform commission rates (15-25%) globally or per provider (used for payout and reconciliation calculations)
- Admins define split payment options (2-9 installments) and cutoff rules (e.g., 30 days before procedure)
- Admins monitor payment configuration health and receive alerts for rate protection thresholds
- Admins audit configuration change history for compliance

**Shared Services (S-02: Payment Processing Service)**:

- Payment Processing Service routes patient payment transactions (deposits/installments/finals) to the appropriate Stripe account based on patient location
- Currency conversion service fetches real-time rates and applies admin-configured markup
- Deposit calculation service applies configured deposit rate to booking totals
- Commission calculation service applies configured commission rate to booking totals for reconciliation and payout reporting
- Installment calculation service generates payment schedules based on configured options and cutoff dates
- Rate protection service monitors currency fluctuations and alerts admins when thresholds exceeded
- Payment audit logging service tracks all transactions for compliance and reconciliation

### Communication Structure

**In Scope**:

- Email notifications to admins when payment configuration changes are published
- System alerts when currency conversion rates exceed configured thresholds (rate protection)
- Admin dashboard notifications for Stripe account connection failures or API errors
- Audit log notifications for payment configuration changes requiring compliance review

**Out of Scope**:

- Patient notifications about payment configuration changes (handled by P-03: Booking & Payment module)
- Provider notifications about payout schedule changes (handled by separate provider payout module)
- SMS notifications for payment failures or processing issues (handled by S-03: Notification Service; **no SMS is sent in MVP and this channel is reserved for future implementation once S-03 SMS delivery is enabled**)
- In-app chat or support messaging (handled by separate support module)

### Entry Points

- **Admin-initiated**: Admin accesses "Payment Configuration" section from admin dashboard settings menu
- **System-triggered**: Payment Processing Service queries payment configuration during every booking transaction
- **API-accessed**: External integrations (if authorized) can query currency conversion rates via read-only API
- **Scheduled jobs**: Currency conversion rate sync runs on scheduled intervals (e.g., every 6 hours) to update cached rates
- **Alert-triggered**: Rate protection system alerts admins when currency fluctuations exceed configured thresholds

---

## Business Workflows

### Main Flow: Configure New Stripe Account

**Actors**: Admin, System, Stripe API
**Trigger**: Admin navigates to "Payment Configuration > Stripe Accounts" and clicks "Add New Account"
**Outcome**: New Stripe account added and mapped to specific countries/regions (regional groupings defined in FR-028), ready to process patient payments for those regions

**Steps**:

1. Admin clicks "Add New Account" button on Stripe Accounts configuration page
2. System displays Stripe account configuration form with required fields
3. Admin enters Stripe account details (account name, publishable key, secret key, webhook secret)
4. Admin selects "Test Mode" or "Live Mode" for the Stripe account
5. System validates Stripe API credentials by making test connection to Stripe API
6. Admin assigns countries or regional groupings (from FR-028) to this Stripe account (one account per country/grouping; overrides required to replace existing mappings)
7. Admin configures supported currencies for this Stripe account (e.g., USD, EUR, GBP)
8. Admin sets default currency for the account
9. Admin reviews configuration summary and clicks "Save & Activate"
10. System stores Stripe account configuration and marks as active
11. System propagates configuration to Payment Processing Service (S-02) with cache TTL of 5 minutes
12. System sends email notification to admin confirming Stripe account activation
13. System logs configuration change to audit trail with admin ID, timestamp, and change details

### Main Flow: Configure Currency Conversion Rules

**Actors**: Admin, System, Currency API (e.g., xe.com)
**Trigger**: Admin navigates to "Payment Configuration > Currency Conversion" to set up rate sources, global defaults, and currency pairs
**Outcome**: Currency conversion rules configured per pair with markup percentages to protect against unfavorable rates

**Steps**:

1. Admin clicks "Currency Conversion" tab on Payment Configuration page
2. System displays Screen 2A: global settings section, rate sources section, and currency pair list
3. Admin configures global defaults (Global Default Markup %, Global Default Sync Frequency, Rate Protection Threshold) and clicks "Save Global Settings"
4. Admin adds a rate source by clicking "Add Source": enters source name, selects provider type (xe.com, fixer.io), enters API key
5. System runs a test connection to validate the source API credentials; source is saved only if the test succeeds
6. Admin clicks "Add Pair" to navigate to Screen 2B
7. Admin selects the target currency (base is always USD) and chooses Rate Mode:
   - **Auto-fetch**: Admin selects a source from the configured sources, then clicks "Test Connection & Fetch Rate". System fetches the initial rate and displays it. Save is disabled until this test succeeds.
   - **Manual**: Admin enters the base rate directly in the Manual Base Rate field.
8. Admin optionally sets per-pair Markup % and Sync Frequency overrides (blank = inherit global defaults)
9. Admin reviews the Effective Rate preview (Base Rate × (1 + Markup %)) and clicks "Save"
10. System stores the pair configuration. For auto-fetch pairs, system schedules the first sync based on save timestamp + configured interval.
11. Admin repeats steps 6-10 for each additional currency pair
12. System propagates configuration to Payment Processing Service (S-02) with cache TTL of 5 minutes
13. System sends email notification to admin confirming currency conversion configuration
14. System logs all configuration changes to audit trail with admin ID, timestamp, and change details

### Main Flow: Configure Deposit Rate Rules

**Actors**: Admin, System
**Trigger**: Admin navigates to "Payment Configuration > Deposit Rates" to configure deposit percentage
**Outcome**: Deposit rate configured globally or per provider, applied to all new bookings

**Steps**:

1. Admin clicks "Deposit Rates" tab on Payment Configuration page
2. System displays current deposit rate configuration (global default and provider-specific overrides)
3. Admin selects configuration scope: "Global Default" or "Provider-Specific"
4. Admin sets deposit percentage (range: 20-30% with validation)
5. If provider-specific: Admin searches and selects provider(s) to apply custom rate
6. Admin reviews summary showing which bookings will be affected (new bookings only)
7. Admin clicks "Apply Deposit Rate"
8. System validates deposit percentage is within allowed range (20-30%)
9. System stores deposit rate configuration with effective date (now) and scope (global or provider IDs)
10. System propagates configuration to Payment Processing Service with cache TTL of 5 minutes
11. System displays confirmation message: "Deposit rate updated. New bookings will use [X]% deposit rate."
12. System logs configuration change to audit trail with admin ID, timestamp, scope, and rate value
13. System sends email notification to affected providers (if provider-specific change)

### Main Flow: Configure Commission Rate Rules

**Actors**: Admin, System
**Trigger**: Admin navigates to "Payment Configuration > Commission Rates" to configure platform commission percentage
**Outcome**: Commission rate configured globally or per provider, applied to all new bookings

**Steps**:

1. Admin clicks "Commission Rates" tab on Payment Configuration page
2. System displays current commission rate configuration (global default and provider-specific overrides)
3. Admin selects configuration scope: "Global Default" or "Provider-Specific"
4. Admin sets commission percentage (range: 15-25% with validation)
5. If provider-specific: Admin searches and selects provider(s) to apply custom rate
6. Admin reviews summary showing which bookings will be affected (new bookings only)
7. Admin clicks "Apply Commission Rate"
8. System validates commission percentage is within allowed range (15-25%)
9. System stores commission rate configuration with effective date (now) and scope (global or provider IDs)
10. System propagates configuration to Payment Processing Service with cache TTL of 5 minutes
11. System displays confirmation message: "Commission rate updated. New bookings will use [X]% commission rate."
12. System logs configuration change to audit trail with admin ID, timestamp, scope, and rate value

### Main Flow: Configure Split Payment (Installment) Plans

**Actors**: Admin, System
**Trigger**: Admin navigates to "Payment Configuration > Split Payment" to configure installment options and cutoff rules
**Outcome**: Installment plan options (2-9 installments) and cutoff date rules configured, available to patients during booking

**Steps**:

1. Admin clicks "Split Payment" tab on Payment Configuration page
2. System displays current split payment configuration showing enabled installment options and cutoff rules
3. Admin enables or disables specific installment options (checkboxes for 2, 3, 4, 5, 6, 7, 8, 9 installments)
4. Admin configures cutoff date rule (e.g., "Full payment must be completed 30 days before procedure date")
5. Admin sets minimum booking amount eligible for split payments (e.g., minimum $500 booking for installments)
6. Admin configures late payment grace period (0-14 days) before booking cancellation (i.e., how many days after a missed installment due date the system waits before canceling the booking for non-payment)
7. Admin reviews preview showing example installment schedules for different booking amounts and dates
8. Admin clicks "Save Split Payment Configuration"
9. System validates cutoff date is reasonable (e.g., minimum 30 days, maximum 90 days)
10. System stores split payment rules with enabled installment options and cutoff date
11. System propagates configuration to Payment Processing Service with cache TTL of 5 minutes
12. System calculates which installment options will be available to patients based on booking date and procedure date
13. System displays confirmation message: "Split payment options updated. Patients will see [X] installment options."
14. System logs configuration change to audit trail
15. System sends email notification to admin confirming split payment configuration

### Alternative Flows

**A1: Add Stripe Account with Regional Grouping Override**:

- **Trigger**: Admin wants to assign a Stripe account to a regional grouping that already has another account assigned
- **Steps**:
  1. Admin attempts to assign countries to new Stripe account that overlap with existing account
  2. System detects conflict and displays warning: "Countries [list] are already assigned to Stripe account [name]"
  3. Admin must choose "Override" to replace existing assignment (no secondary accounts; one account per country/regional grouping)
  4. Admin confirms override action
  5. System updates country-to-account mappings, replacing prior assignment with the new account
  6. System propagates updated mappings to Payment Processing Service
  7. System logs conflict resolution to audit trail
- **Outcome**: New Stripe account assigned to region, replacing or supplementing previous assignment

**A2: Configure Provider-Specific Deposit Rate**:

- **Trigger**: Admin wants to set custom deposit rate for specific provider(s) different from global default
- **Steps**:
  1. Admin selects "Provider-Specific" scope in deposit rate configuration
  2. Admin searches for provider by name or ID
  3. Admin selects one or more providers from search results
  4. Admin sets custom deposit rate percentage (20-30%) for selected providers
  5. System displays preview: "This will override global default [X]% for [Y] providers"
  6. Admin confirms provider-specific rate
  7. System stores provider-specific rate configuration with provider IDs
  8. System displays confirmation with list of affected providers
- **Outcome**: Selected providers have custom deposit rate, overriding global default

**A3: Switch Existing Pair from Manual to Auto-Fetch**:

- **Trigger**: Admin wants to switch a manually-managed currency pair to auto-fetch from an API source
- **Steps**:
  1. Admin opens an existing manual-mode pair from the pair list (Screen 2A) for editing (Screen 2B)
  2. Admin changes Rate Mode from "Manual" to "Auto-fetch"
  3. System shows the Source dropdown (populated from configured sources in Screen 2A Section 2)
  4. Admin selects a source and clicks "Test Connection & Fetch Rate"
  5. System fetches the current rate from the selected source for this pair
  6. If test succeeds: fetched rate replaces the manual rate; system displays the new base rate and effective rate preview
  7. If test fails: system displays error with details; admin must resolve before saving (e.g., try different source, fix source credentials)
  8. Admin optionally sets per-pair Sync Frequency override (or leaves blank to inherit global default)
  9. Admin clicks "Save"
  10. System stores updated pair configuration, schedules recurring sync from save timestamp, and logs change to audit trail
- **Outcome**: Currency pair now auto-fetches rates on schedule; manual rate is replaced by API-fetched rate

**A3b: Switch Existing Pair from Auto-Fetch to Manual**:

- **Trigger**: Admin wants to manually control a pair's rate instead of relying on API source
- **Steps**:
  1. Admin opens an existing auto-fetch pair for editing (Screen 2B)
  2. Admin changes Rate Mode from "Auto-fetch" to "Manual"
  3. System pre-fills the Manual Base Rate field with the last successfully fetched rate (so admin doesn't start from zero)
  4. Source and Sync Frequency fields are hidden
  5. Admin adjusts the manual rate if needed and clicks "Save"
  6. System removes the sync schedule for this pair, stores updated configuration, and logs change to audit trail
- **Outcome**: Currency pair is now manually managed; rate only changes when admin edits it

**A4: Configure Different Installment Options for Different Booking Amounts**:

- **Trigger**: Admin wants to offer more installment options for higher-value bookings
- **Steps**:
  1. Admin creates multiple split payment rule tiers based on booking amount ranges
  2. Admin sets tier 1: Bookings $500-$2,000 can use 2-4 installments
  3. Admin sets tier 2: Bookings $2,001-$5,000 can use 2-6 installments
  4. Admin sets tier 3: Bookings $5,001+ can use 2-9 installments
  5. System validates tier ranges don't overlap and are logically ordered
  6. System stores tiered split payment rules
  7. System applies appropriate installment options based on booking amount during checkout
- **Outcome**: Patients see installment options appropriate for their booking amount

**B1: Stripe API Credential Validation Fails**:

- **Trigger**: Admin enters invalid Stripe API credentials or Stripe API is unreachable
- **Steps**:
  1. Admin submits Stripe account configuration with API credentials
  2. System attempts to validate credentials by calling Stripe API
  3. Stripe API returns authentication error or connection timeout
  4. System displays error message: "Unable to connect to Stripe. Please verify API keys are correct and your Stripe account is active."
  5. System highlights fields with credential errors (publishable key, secret key, webhook secret)
  6. Admin corrects API credentials or troubleshoots connection issue
  7. Admin clicks "Retry Connection"
  8. System re-attempts validation
- **Outcome**: Admin corrects credentials and successfully adds Stripe account, or admin contacts support for assistance

**B2: Currency Conversion API Connection Failure (Per-Pair)**:

- **Trigger**: Scheduled sync for an auto-fetch currency pair fails due to API source downtime or network issue
- **Steps**:
  1. System scheduled sync job attempts to fetch the current rate for a specific pair (e.g., USD/EUR) from its assigned source (e.g., xe.com)
  2. Source API returns error (503 Service Unavailable) or connection timeout
  3. System logs sync failure with pair, source, and error details
  4. System continues using the pair's last successfully fetched rate (cached rate with timestamp)
  5. System updates the pair's status indicator to red/error on the pair list (Screen 2A)
  6. System sends alert notification to admin: "Sync failed for USD/EUR (source: xe.com). Using cached rate from [timestamp]."
  7. System retries sync after exponential backoff (e.g., retry in 15 minutes, then 30 minutes, then 1 hour)
  8. If source remains down, the source's status indicator on Screen 2A Section 2 also turns red, making it visible that multiple pairs may be affected
  9. Admin investigates source status, fixes credentials, or switches affected pairs to a different source or manual mode
- **Outcome**: System gracefully handles per-pair API failure by using cached rates, showing visual status cues, and alerting admin

**B3: Deposit Rate Outside Allowed Range**:

- **Trigger**: Admin attempts to set deposit rate below 20% or above 30%
- **Steps**:
  1. Admin enters deposit rate percentage (e.g., 15% or 35%) outside allowed range
  2. Admin clicks "Apply Deposit Rate"
  3. System validates deposit rate and detects out-of-range value
  4. System displays validation error: "Deposit rate must be between 20% and 30%. You entered [X]%."
  5. System highlights deposit rate input field with error state
  6. Admin corrects deposit rate to value within allowed range (20-30%)
  7. Admin resubmits configuration
  8. System accepts valid deposit rate
- **Outcome**: Admin sets deposit rate within allowed range, ensuring business rule compliance

**B4: Split Payment Cutoff Date Conflict**:

- **Trigger**: Admin configures cutoff date that would prevent any installment options from being offered
- **Steps**:
  1. Admin sets cutoff date to very aggressive value (e.g., 90 days before procedure)
  2. Admin enables multiple installment options (e.g., 2-9 installments)
  3. System calculates that most bookings won't have enough time for multiple installments before cutoff
  4. System displays warning: "Current cutoff date [X days] may prevent installment options from being offered for most bookings. Consider reducing cutoff to 30-45 days."
  5. Admin reviews warning and adjusts cutoff date or proceeds with aggressive cutoff
  6. Admin confirms configuration
  7. System stores configuration but logs warning to admin activity log
- **Outcome**: Admin is informed of potential issue and can adjust cutoff date or accept restrictive configuration

**B5: Currency Fluctuation Exceeds Rate Protection Threshold (Per-Pair)**:

- **Trigger**: Scheduled sync for an auto-fetch pair detects a rate change exceeding the global Rate Protection Threshold (e.g., 3% in 24 hours)
- **Steps**:
  1. System fetches the current rate for USD/EUR from its assigned source during the pair's scheduled sync
  2. System compares the new rate to the pair's previously cached rate
  3. System detects the USD/EUR rate changed by 4.5% in the last 24 hours (exceeds the 3% global threshold)
  4. System updates the pair's status indicator to yellow/warning on the pair list (Screen 2A)
  5. System sends urgent alert notification to admin: "Currency alert: USD/EUR rate changed 4.5% in 24 hours (threshold: 3%). Review markup for this pair."
  6. Admin sees the yellow warning badge on the pair list, clicks into the pair (Screen 2B) to review
  7. Admin reviews the current base rate, markup %, and effective rate
  8. Admin decides to increase the per-pair markup from 5% to 7% to protect against the unfavorable rate
  9. Admin saves the updated markup; system recalculates the effective rate and logs the change to audit trail
  10. The pair's status badge returns to green after the next sync shows the rate change is within threshold
- **Outcome**: Admin is alerted per-pair to significant rate fluctuations via both visual cues on the list and email notification, and can adjust the specific pair's markup to protect revenue

**B6: No Stripe Account Available for Patient Location**:

- **Trigger**: Patient from country with no assigned Stripe account attempts booking
- **Steps**:
  1. Patient selects country during booking flow (e.g., patient in South Africa)
  2. Payment Processing Service queries payment configuration for patient's country
  3. System finds no Stripe account assigned to South Africa
  4. System checks for a Stripe account marked as "Global Fallback"
  5. If Global Fallback exists: System uses that Stripe account and logs warning to admin
  6. If no fallback: System displays error to patient: "Payment processing not available for your location. Please contact support."
  7. System sends alert to admin: "Payment attempted from unsupported country: South Africa. Configure Stripe account for this region."
- **Outcome**: Patient uses fallback account (if configured) or is unable to complete booking, and admin is alerted to expand regional coverage

---

## Screen Specifications

### Screen 1: Stripe Accounts Management

**Purpose**: Allows admins to add, edit, and manage multiple Stripe accounts and assign them to countries or regional groupings

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Account Name | text | Yes | Friendly name for Stripe account (e.g., "US & Canada Account", "EU Account") | Max 100 chars, must be unique |
| Publishable Key | text | Yes | Stripe publishable API key (starts with pk_) | Must start with "pk_test_" or "pk_live_", max 200 chars |
| Secret Key | password | Yes | Stripe secret API key (starts with sk_) | Must start with "sk_test_" or "sk_live_", max 200 chars |
| Webhook Secret | password | Yes | Stripe webhook signing secret | Min 32 chars, max 200 chars |
| Account Mode | select | Yes | Test Mode or Live Mode | Must select one option |
| Global Fallback | toggle | No | If enabled, this Stripe account is used when no country/regional grouping mapping exists for the patient | At most 1 Stripe account can be marked as Global Fallback. If enabled: Assigned Countries must be empty and Account Status must be Active. |
| Assigned Countries | multi-select | Conditional | Countries **or** regional groupings served by this account (mutually exclusive per record: choose groups or countries, not both) | Required unless Global Fallback is enabled. Each country/grouping can map to only one Stripe account (overrides required to reassign). If a country mapping exists, it overrides any group-level account for that country. |
| Supported Currencies | multi-select | Yes | Currencies this Stripe account can process (e.g., USD, EUR, GBP) | Must select at least one currency |
| Default Currency | select | Yes | Default currency for this account | Must be one of selected supported currencies |
| Account Status | toggle | Yes | Active or Inactive | Boolean (active = enabled for processing) |

**Business Rules**:

- Stripe API credentials must be validated before account can be activated (test connection to Stripe API)
- One account per country/regional grouping (from FR-028); reassignments require explicit override
- Country-level assignment supersedes group-level assignment for any country already in that group (most-specific mapping wins)
- At most one Stripe account can be marked as Global Fallback; Global Fallback cannot have explicit country/regional grouping assignments
- Cannot delete Stripe account if it has processed transactions in last 90 days (archive instead)
- Admin can test Stripe connection at any time by clicking "Test Connection" button
- Webhook secret is required for payment event verification and cannot be left blank
- Supported currencies must be compatible with assigned countries (e.g., EUR for European countries)
- Changes to Stripe account configuration propagate to Payment Processing Service within 5 minutes (cache TTL)

**Notes**:

- Display last successful connection test timestamp below API credential fields
- Show warning icon if Stripe account hasn't been tested in over 30 days
- Provide inline help text explaining difference between Test Mode and Live Mode
- Display transaction count and total volume processed by each account (last 30 days) for admin reference
- Use password masking for Secret Key and Webhook Secret fields, with "Show" toggle button
- Include "Test Connection" action button that opens a modal/sub-screen:
  - Shows account name, mode (Test/Live), and endpoint being validated
  - On submit, system calls Stripe with provided keys/webhook secret; displays success/failure with error details
  - Logs test attempt (admin, timestamp, result) and updates "Last Tested" timestamp/status badge

---

### Screen 2A: Currency Conversion — Pair List & Global Settings

**Purpose**: Central dashboard for managing all currency conversion pairs, rate sources, and global defaults. This screen has two sections: Global Settings and Currency Pair List.

#### Section 1: Global Settings

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Global Default Markup % | number | Yes | Default markup percentage applied to any currency pair that does not have a per-pair override | Range: 0-20%, decimal precision: 0.01% |
| Global Default Sync Frequency | select | Yes | Default sync interval for auto-fetched pairs that do not have a per-pair override | Options: 1h, 3h, 6h, 12h, 24h |
| Rate Protection Threshold | number | Yes | Alert if any pair's rate changes more than this percentage within 24 hours | Range: 1-50%, decimal precision: 0.1% |

**Business Rules (Global Settings)**:

- Global Default Markup % is used as fallback when a currency pair does not specify its own markup percentage
- Global Default Sync Frequency is used as fallback when an auto-fetched pair does not specify its own sync interval
- Rate Protection Threshold applies to all auto-fetched pairs; system monitors each pair independently and flags those exceeding the threshold
- Rate protection alerts do not automatically stop payments; they surface visual cues and send admin notifications
- Any currency pair not configured in this module results in the system collecting payment in USD (no conversion attempted)

#### Section 2: Rate Sources

**Purpose**: Manage the list of external API providers used to auto-fetch exchange rates. Each source bundles its provider type with API credentials.

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Source Name | text | Yes | Admin-friendly label for this source (e.g., "xe.com — Production") | Max 100 chars, must be unique |
| Provider Type | select | Yes | API provider | Options: xe.com, fixer.io (extensible) |
| API Key | text | Yes | API key / credentials for this provider | Non-empty; masked after save (show last 4 chars) |
| Status | display-only | N/A | Connection health indicator | Auto-populated: green (healthy), yellow (degraded), red (down/error) |
| Last Tested | display-only | N/A | Timestamp of last successful connection test | Auto-populated by system |

**Actions**:

- **Add Source**: Opens inline form / modal to create a new source. Requires all fields above. System runs a test connection upon save; source is only persisted if the test succeeds.
- **Edit Source**: Admin can update source name, API key. System re-runs test connection on save.
- **Delete Source**: Admin can delete a source only if no currency pairs reference it. If pairs reference the source, system displays warning listing affected pairs and requires admin to reassign or switch those pairs to manual before deletion.
- **Test Connection**: Available per source at any time. Calls the provider API, updates Status and Last Tested.

**Business Rules (Rate Sources)**:

- API credentials are encrypted at rest (AES-256) and never logged in plain text (mask all but last 4 characters)
- A source cannot be saved without passing a test connection first
- Deleting a source that is referenced by existing pairs is blocked; admin must reassign or convert affected pairs to manual mode first. This is the graceful deletion pattern.
- System periodically checks source health during scheduled syncs and updates the Status indicator. If a source becomes unhealthy, all pairs using that source display a visual warning badge (yellow/red) on the pair list.

#### Section 3: Currency Pair List

**Purpose**: Table listing all configured currency pairs with their current mode, rate, source, markup, and status.

| Column | Description |
|--------|-------------|
| Pair | Always displayed as USD/{Target} (e.g., USD/EUR, USD/GBP). All pairs use USD as base. |
| Mode | "Auto" or "Manual" — indicates how the base rate is determined |
| Source | Name of the rate source (if auto-fetched); "—" if manual |
| Base Rate | The raw exchange rate (fetched from API or manually entered) |
| Markup % | Per-pair markup percentage; shows "(global)" suffix if using the global default |
| Effective Rate | Calculated: Base Rate × (1 + Markup %). This is the rate applied to patient-facing prices. |
| Sync Frequency | Per-pair sync interval; shows "(global)" suffix if using the global default (auto-fetch pairs only) |
| Last Updated | Timestamp of last rate update (auto-sync or manual save) |
| Status | Visual indicator: green checkmark (healthy), yellow warning (rate protection threshold breached or source degraded), red error (source down / fetch failed) |

**Actions on List**:

- **Add Pair**: Navigates to Screen 2B (Add/Edit Currency Pair) to create a new pair
- **Edit Pair**: Click row or edit icon to navigate to Screen 2B pre-populated with pair data
- **Delete Pair**: Remove a currency pair. System warns: "Deleting this pair means payments involving {Target} currency will fall back to USD. Continue?" Requires confirmation.
- **Sync Now (per pair)**: For auto-fetched pairs, triggers an immediate rate fetch outside the scheduled sync

**Business Rules (Pair List)**:

- All pairs MUST use USD as the base currency. Admin selects only the target currency when adding a pair.
- Currency pairs must reference currencies that are enabled in the Currency Management screen (Screen 6)
- If a pair is deleted or not configured for a target currency, the system collects payment in USD for transactions involving that currency (no conversion attempted). A note on this screen states: "Currency pairs not listed here will default to USD for payment collection."
- Each pair independently tracks its own status. A source failure affects only pairs using that source; manual pairs are unaffected.
- Status badges update automatically: green when last fetch succeeded and rate change is within threshold; yellow when rate protection threshold was breached in last 7 days or source is degraded; red when last fetch failed or source is down.

**Notes**:

- Display a prominent info banner: "Any currency not configured here will default to USD for payment. Configure all currencies your patients may use."
- Provide sorting/filtering on the pair list: by pair name, mode, status, last updated
- Display total pair count and counts by mode (e.g., "12 pairs: 9 auto, 3 manual")
- Show alert badge count in the tab/section header if any pair has yellow/red status

---

### Screen 2B: Add / Edit Currency Pair

**Purpose**: Form to create a new currency pair or edit an existing one. Controls the pair's rate mode (auto-fetch or manual), source assignment, markup, and sync frequency.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Base Currency | display-only | N/A | Always "USD" — not editable | Fixed: USD |
| Target Currency | select | Yes | The target currency for this pair (e.g., EUR, GBP, TRY) | Must be an enabled currency from Currency Management (Screen 6); cannot duplicate an existing pair |
| Rate Mode | radio | Yes | How the base rate is determined | Options: "Auto-fetch from source" or "Manual input" |
| Source | select | Conditional | Which rate source to use for auto-fetching | Required if Rate Mode = Auto-fetch. Populated from sources configured in Screen 2A Section 2. |
| Manual Base Rate | number | Conditional | The admin-entered base exchange rate (how many units of target currency per 1 USD) | Required if Rate Mode = Manual. Must be > 0, decimal precision: 6 digits. |
| Markup % | number | No | Per-pair markup percentage override. If left blank, the global default markup % from Screen 2A is used. | Range: 0-20%, decimal precision: 0.01%. Leave blank to inherit global default. |
| Sync Frequency | select | No | Per-pair sync frequency override. If left blank, the global default sync frequency from Screen 2A is used. Only applicable for auto-fetch mode. | Options: 1h, 3h, 6h, 12h, 24h. Leave blank to inherit global default. Ignored if Rate Mode = Manual. |
| Effective Rate | display-only | N/A | Calculated preview: Base Rate × (1 + Markup %) | Auto-calculated in real-time as admin edits Base Rate or Markup % |

**Actions**:

- **Test Connection & Fetch Rate** (auto-fetch mode only): Calls the selected source API for this specific pair. If successful, populates the Base Rate field with the fetched value and shows success confirmation with the fetched rate and effective rate preview. This action is **mandatory before saving** a new auto-fetch pair.
- **Save**: Validates all fields, persists the pair configuration, and returns to Screen 2A. For auto-fetch pairs, the first scheduled sync is calculated from the save timestamp (e.g., if saved at 12:36 with 6h interval, next sync at 18:36).
- **Cancel**: Discards changes and returns to Screen 2A.

**Business Rules (Add/Edit Pair)**:

- All pairs use USD as the base currency (non-negotiable, enforced by UI)
- Target currency dropdown is populated from enabled currencies in the Currency Management screen (Screen 6); cannot create a pair for a disabled currency
- Cannot create a duplicate pair (one pair per target currency; USD/EUR can only exist once)
- **Auto-fetch mode**:
  - Admin must select a source from the configured sources in Screen 2A Section 2
  - Admin **must run "Test Connection & Fetch Rate" before saving** to verify the source can provide a rate for this pair. Save button is disabled until test succeeds.
  - After the initial save, the system schedules recurring syncs. The schedule is calculated from the time the pair is saved: if saved at 12:36 with a 6-hour interval, the next sync runs at 18:36, then 00:36, etc.
  - If a scheduled fetch fails, the system keeps the last successfully fetched rate, marks the pair status as red/error on the list, and sends an alert notification to the admin
  - If the source assigned to this pair is later deleted, the pair gracefully switches to manual mode with the last fetched rate pre-filled as the manual base rate. Admin is notified of this change.
- **Manual mode**:
  - Admin enters the base rate directly in the Manual Base Rate field
  - No sync schedule is created; rate only changes when admin manually edits and saves
  - Source field is hidden / not applicable
  - Sync Frequency field is hidden / not applicable
- **Switching modes on an existing pair**:
  - Auto → Manual: System pre-fills Manual Base Rate with the last fetched rate so admin doesn't start from zero. Sync schedule is removed.
  - Manual → Auto: System requires admin to select a source and run "Test Connection & Fetch Rate" before saving. The fetched rate replaces the manual rate.
- **Markup % inheritance**: If Markup % is left blank, the pair uses the Global Default Markup % from Screen 2A. If specified, the per-pair value overrides the global default. The Effective Rate preview always shows the actual markup being applied (whether inherited or overridden).
- **Sync Frequency inheritance**: If Sync Frequency is left blank (auto-fetch mode), the pair uses the Global Default Sync Frequency. If specified, the per-pair value overrides. Display "(using global default: Xh)" hint text when blank.
- The Effective Rate preview updates in real-time as admin changes Base Rate or Markup %, giving immediate visibility into the patient-facing rate.

**Notes**:

- Show inline help text: "Base Rate = how many {Target} per 1 USD. Example: 0.92 means 1 USD = 0.92 EUR."
- For auto-fetch pairs, show the source's current status indicator (green/yellow/red) next to the source dropdown
- Show estimated conversion rate impact: "5% markup on 0.92 USD/EUR = 0.966 effective rate"
- Display last sync timestamp and next scheduled sync time (for auto-fetch pairs) below the form
- When editing an existing pair, show a "Rate History" link/section displaying rate changes over the last 30 days (chart + table)

---

### Screen 3: Deposit Rate Configuration

**Purpose**: Allows admins to configure deposit percentage for bookings, either globally or per provider

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Configuration Scope | radio | Yes | Global Default or Provider-Specific | Must select one option |
| Global Deposit Rate | number | Conditional | Default deposit percentage for all providers | Range: 20-30%, decimal precision: 0.1%, required if scope is Global |
| Provider Search | search | Conditional | Search for provider by name or ID | Required if scope is Provider-Specific |
| Selected Providers | list | Conditional | List of providers for custom deposit rate | Required if scope is Provider-Specific |
| Provider Deposit Rate | number | Conditional | Custom deposit percentage for selected providers | Range: 20-30%, decimal precision: 0.1%, required if scope is Provider-Specific |
| Effective Date | display-only | N/A | Shows when this rate takes effect (immediately for new bookings) | Auto-populated: current timestamp |
| Affected Bookings | display-only | N/A | Shows booking count that will use this rate (estimates based on historical data) | Auto-calculated by system |

**Business Rules**:

- Deposit rate must be between 20% and 30% (business rule enforced by system validation)
- Deposit rate changes apply to new bookings only (existing bookings retain original deposit rate)
- Provider-specific rates override global default rate for selected providers
- Admin can set multiple provider-specific rates (different rates for different providers)
- System calculates deposit amount by multiplying booking total by deposit rate percentage
- Deposit rate configuration propagates to Payment Processing Service within 5 minutes (cache TTL)
- Cannot delete provider-specific rate if provider has active bookings using that rate (archive instead)

**Notes**:

- Display preview calculation: "For $2,000 booking, 25% deposit = $500 due at booking time"
- Show list of providers with custom rates different from global default (sortable table)
- Provide bulk edit capability: select multiple providers and apply same deposit rate
- Display historical deposit rate changes in audit log below configuration form
- Show visual indicator (badge) next to providers with custom rates on provider list screens

---

### Screen 4: Split Payment (Installment) Configuration

**Purpose**: Allows admins to configure available installment plan options (2-9 installments) and cutoff date rules

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Enable Split Payments | toggle | Yes | Master switch to enable or disable split payment feature globally | Boolean (enabled = feature active) |
| Available Installments | checkbox-group | Yes | Select which installment options to offer (2, 3, 4, 5, 6, 7, 8, 9) | Must select at least one if feature enabled |
| Cutoff Days | number | Yes | Days before procedure date that full payment must be completed | Range: 30-90 days, integer only |
| Minimum Booking Amount | number | Yes | Minimum booking total required to qualify for installments (in USD) | Range: $100-$10,000, integer only |
| Installment Frequency | display-only | N/A | Payment schedule frequency | Fixed: Monthly (30-day intervals) |
| Late Payment Grace Period | number | Yes | Days after missed payment before booking cancellation | Range: 0-14 days, integer only |

**Business Rules**:

- Cutoff days ensures patients complete full payment before procedure date (default: 30 days)
- System automatically calculates available installment options based on booking date and procedure date
- If time between booking and procedure is insufficient for selected installments given cutoff, system offers fewer installments
- Installment amount calculation is always equal-split: booking total ÷ installment count (rounded to 2 decimal places; last installment absorbs rounding difference)
- Minimum booking amount prevents installments for low-value bookings (reduces administrative overhead)
- Late payment grace period allows patients short extension before booking cancellation (0 = no grace period)
- Split payment configuration propagates to Payment Processing Service within 5 minutes (cache TTL)
- Cannot modify split payment rules for bookings with active installment plans (changes apply to new bookings only)
- System enforces a minimum 30-day cutoff before procedure date (per system booking/payment rules); admins may increase the cutoff up to 90 days

**Notes**:

- Display preview calculator: "For $3,000 booking with 5 installments, 30-day cutoff, booking 210 days before procedure:"
  - 5 installments: $600.00 each, due monthly (every ~30 days)
  - Final installment due: 30 days before procedure date
- Show example scenarios for different booking amounts and installment options
- Provide "Preview Installment Schedule" button that generates detailed payment schedule
- Display warning if cutoff days is very aggressive (e.g., >60 days): "This may limit installment availability"
- Show statistics: "In last 30 days, 42% of bookings used installment plans (avg: 3.8 installments)"

---

### Screen 5: Commission Rate Configuration

**Purpose**: Allows admins to configure platform commission rates (global default and provider-specific overrides) used in billing, reconciliation, and provider payout calculations

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Configuration Scope | radio | Yes | Global Default or Provider-Specific | Must select one option |
| Global Commission Rate | number | Conditional | Default commission percentage applied platform-wide | Range: 15-25%, decimal precision: 0.1%, required if scope is Global |
| Provider Search | search | Conditional | Search for provider by name or ID | Required if scope is Provider-Specific |
| Selected Providers | list | Conditional | List of providers for custom commission rate | Required if scope is Provider-Specific |
| Provider Commission Rate | number | Conditional | Custom commission percentage for selected providers | Range: 15-25%, decimal precision: 0.1%, required if scope is Provider-Specific |
| Effective Date | display-only | N/A | Shows when this rate takes effect (applies to new bookings) | Auto-populated: current timestamp |

**Business Rules**:

- Commission rate changes apply to new bookings only (existing bookings retain the commission rate snapshot used at booking confirmation)
- Provider-specific commission rates override global default rate for selected providers
- System calculates commission amount by multiplying booking total by commission rate percentage (rounded to 2 decimal places; last payment absorbs rounding difference if needed)
- Commission configuration propagates to Payment Processing Service within 5 minutes (cache TTL)
- All commission rate changes must be logged to audit trail with before/after state

**Notes**:

- Display preview calculation: "For $2,000 booking, 20% commission = $400"
- Provide in-app link from reconciliation/payout screens to commission configuration (read-only for non-authorized roles)

---

### Screen 6: Currency Management (Central Supported Currency List)

**Purpose**: Allows admins to manage the *enabled* subset of currencies used throughout the platform (e.g., currency dropdowns for location pricing, Stripe account supported currencies, and currency conversion configuration). The master currency catalog (ISO 4217 code metadata such as symbol and minor units) is maintained by engineering; admins do not create arbitrary new currency codes.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Search | text | No | Filter currencies by code or name | Max 100 chars |
| Currency Code | display-only | - | ISO 4217 code (e.g., USD, EUR, GBP) | From master catalog |
| Currency Name | display-only | - | Human-readable currency name | From master catalog |
| Symbol | display-only | - | Currency symbol (e.g., $, €, £) | From master catalog |
| Minor Units | display-only | - | Decimal precision (e.g., 2 for USD/EUR/GBP, 0 for JPY/KRW) | From master catalog |
| Enabled | toggle | Yes | Whether this currency is available for selection across the system | Must keep at least 1 enabled currency |
| Default Currency | radio/select | Yes | Which enabled currency is the system default | Exactly 1 default; default must be enabled |

**Business Rules**:

- Currency codes are immutable and come from a system-maintained catalog; admins cannot add non-ISO or custom codes.
- At least one currency must remain enabled at all times.
- Exactly one enabled currency must be set as the system default.
- If an admin attempts to disable a currency currently referenced by system configuration (e.g., used in Stripe account supported currencies, location starting prices, or active pricing configs), the system MUST warn and provide a safe resolution path (e.g., update dependent configs first) before allowing the disable.
- Enabling/disabling currencies affects new configuration choices immediately; existing records retain their stored currency codes.

**Notes**:

- This screen is the source of truth for currency dropdowns across Admin/Provider/Patient experiences (where applicable).
- Provide quick actions: “Enable common set” (e.g., USD/EUR/GBP) and “Set Default” for an enabled currency.

---

## Business Rules

### General Module Rules

- **Rule 1**: Payment configuration changes apply to new transactions only (existing bookings, quotes, and active installment plans retain original configuration)
- **Rule 2**: All payment configuration changes must be logged to audit trail with admin ID, timestamp, and change details for compliance
- **Rule 3**: Configuration cache propagates to Payment Processing Service within 5 minutes maximum (cache TTL)
- **Rule 4**: System must gracefully handle payment processing when configuration data is unavailable (use last known good configuration)
- **Rule 5**: Admin cannot delete Stripe accounts, deposit rates, or split payment rules with active references (archive instead)

### Data & Privacy Rules

- **Privacy Rule 1**: Stripe API secret keys and webhook secrets must be encrypted at rest using AES-256 encryption
- **Privacy Rule 2**: Stripe secret keys must never be logged in plain text to audit logs or error logs (mask all but last 4 characters)
- **Privacy Rule 3**: Admin access to payment configuration must require elevated permissions (not available to standard admin users)
- **Privacy Rule 4**: Stripe webhook signatures must be verified for all incoming webhook events using the configured webhook secret
- **Audit Rule**: All payment configuration changes must be logged with before/after state for audit compliance
- **Compliance Rule**: Payment data handling must comply with PCI DSS requirements (no storage of full card numbers, CVVs, or PINs)
- **Data Retention**: Payment configuration audit history retained for 10 years for financial audit and compliance purposes

### Admin Editability Rules

**Editable by Admin**:

- Stripe account credentials, assigned countries, supported currencies, and active/inactive status
- Central supported currency list (enable/disable currencies) and system default currency
- Rate sources (add/edit/delete with provider type and API credentials)
- Currency pairs (add/edit/delete; per-pair rate mode, source assignment, manual base rate, markup % override, sync frequency override)
- Global currency conversion defaults (global markup %, global sync frequency, rate protection threshold)
- Deposit rate percentage (20-30% range) globally or per provider
- Commission rate percentage (15-25% range) globally or per provider
- Split payment available installment options (2-9), cutoff days (30-90), minimum booking amount ($100-$10,000)
- Late payment grace period for split payments (0-14 days)
- Rate protection alert threshold (global) for currency conversion monitoring

**Fixed in Codebase (Not Editable)**:

- Deposit rate allowed range (20-30% hard-coded business rule)
- Split payment installment range (2-9 installments hard-coded limit)
- Cutoff days allowed range (30-90 days hard-coded limits)
- Installment frequency (monthly; 30-day intervals)
- Encryption algorithms for Stripe secret keys (AES-256)
- Cache TTL for configuration propagation (5 minutes hard-coded)
- Payment audit logging requirements (always enabled, cannot be disabled)
- Currency master catalog (ISO 4217 metadata: name/symbol/minor units) used to populate the Currency Management screen

**Configurable with Restrictions**:

- Global and per-pair markup percentage for currency conversion (range: 0-20%, requires validation)
- Global and per-pair sync frequency for auto-fetch currency pairs (options: 1h, 3h, 6h, 12h, 24h)
- Rate protection threshold (range: 1-50%, requires validation); alerts always active for auto-fetch pairs
- Minimum booking amount for split payments (range: $100-$10,000, requires validation)

### Payment & Billing Rules

- **Payment Rule 1**: Payment Processing Service routes transactions to appropriate Stripe account based on patient's country location
- **Payment Rule 2**: If patient's country has no assigned Stripe account, system uses the Stripe account marked as Global Fallback (if configured) or blocks payment
- **Payment Rule 3**: Currency conversion markup applies to all transactions involving currency conversion (protects against bank rate differences)
- **Payment Rule 4**: Deposit amount calculated by multiplying booking total by configured deposit rate percentage (rounded to 2 decimal places)
- **Payment Rule 5**: Installment payment schedules calculated based on booking date, procedure date, cutoff days, and selected installment count
- **Payment Rule 6**: If patient misses installment payment deadline, system sends reminder notification during grace period, then cancels booking if not paid
- **Billing Rule 1**: Installments are equal-split: booking total ÷ installment count (rounded to 2 decimal places; last installment absorbs rounding difference)
- **Currency Rule 1**: Prices always displayed to patients in their selected currency using admin-configured conversion rates with markup
- **Currency Rule 2**: Currency conversion rate (including markup) MUST be locked at time of quote acceptance and stored per quote/booking/transaction; subsequent displays and deposit/installment/final payments use the locked rate (no rate fluctuation after quote acceptance)
- **Commission Rule**: Commission rate MUST be determined (global or provider-specific) at booking confirmation and stored per booking/transaction for payout and reconciliation consistency
- **Refund Rule**: Deposit refunds follow provider-specific cancellation policies (separate from payment configuration)

---

## Success Criteria

### Patient Experience Metrics

- **SC-001**: Patients can complete booking payment with deposit (20-30% of total) in under 60 seconds for 95% of transactions
- **SC-002**: Patients see available installment plan options that fit their booking timeline and cutoff date constraints with 100% accuracy
- **SC-003**: Patients see prices displayed in their selected currency with conversion rates updated within 6 hours of market changes
- **SC-004**: 90% of patients who select installment plans successfully complete all scheduled payments before cutoff date

### Provider Efficiency Metrics

- **SC-005**: Deposit payments are captured successfully upon booking confirmation with 99.5% reliability
- **SC-006**: Provider payout schedules align with Stripe account configuration for their region with zero discrepancies
- **SC-007**: Providers experience zero payment processing delays due to misconfigured Stripe accounts or currency conversion issues

### Admin Management Metrics

- **SC-008**: Admins can add and activate new Stripe account in under 5 minutes for 90% of configurations
- **SC-009**: Admins can configure or update currency conversion markup percentages in under 2 minutes for 95% of changes
- **SC-010**: Admins can set global or provider-specific deposit rates in under 3 minutes for 90% of configurations
- **SC-011**: Admins can configure split payment rules (installments, cutoff) in under 5 minutes for 95% of configurations
- **SC-012**: Admins receive rate protection alerts within 15 minutes of currency rate exceeding configured threshold for 100% of threshold breaches
- **SC-013**: Admins can audit complete payment configuration change history for any time period with 100% accuracy

### System Performance Metrics

- **SC-014**: Payment configuration changes propagate to Payment Processing Service within 5 minutes for 99% of updates
- **SC-015**: Currency conversion rate sync completes within 30 seconds for 95% of scheduled syncs
- **SC-016**: System routes payment to correct regional Stripe account based on patient location with 99.9% accuracy
- **SC-017**: Payment Processing Service applies correct deposit rate (global or provider-specific) with 100% accuracy
- **SC-018**: Installment schedule calculations account for cutoff date constraints with zero calculation errors
- **SC-019**: System handles currency conversion API failures gracefully by using cached rates with 100% uptime (no payment blocking)

### Business Impact Metrics

- **SC-020**: Booking conversion rate increases by 15% after enabling split payment installment options (measured over 90-day period)
- **SC-021**: Revenue protection from currency conversion markup prevents losses on 99% of transactions involving currency conversion
- **SC-022**: Multi-regional Stripe account configuration enables payment processing in 20+ countries with localized payment methods
- **SC-023**: Automated currency rate syncing reduces admin manual rate update overhead by 90% (measured in admin hours per month)
- **SC-024**: Provider-specific deposit rate flexibility increases provider satisfaction scores by 10% (measured via provider surveys)

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **FR-028 / Module A-09**: Regional Configuration & Pricing
  - **Why needed**: Stripe account assignments must align with regional groupings defined in FR-028
  - **Integration point**: Payment Configuration queries regional groupings to map Stripe accounts to countries/regions; FR-028 enforces one-country-to-one-grouping, so Stripe account mapping must respect that uniqueness (conflicts resolved via override)

- **FR-006 / Module P-03**: Booking & Scheduling
  - **Why needed**: Booking flow uses configured deposit rates and split payment rules to calculate deposit amount and determine feasible installment options at booking confirmation
  - **Integration point**: Booking service queries Payment Configuration API for deposit rate, commission rate, and split payment rules based on provider ID

- **FR-007 / Module S-02**: Payment Processing
  - **Why needed**: Payment Processing Service implements all payment configuration rules for transaction routing
  - **Integration point**: Payment service queries Payment Configuration API for Stripe account, currency pair effective rates, deposit rates, commission rates, and split payment rules

- **FR-007B / Module S-02**: Split Payment / Installment Plans
  - **Why needed**: Installment calculation logic uses configured installment options, cutoff days, and schedule rules
  - **Integration point**: Installment service queries Payment Configuration API for split payment rules

- **FR-001 / Module P-01**: Patient Authentication & Profile Management
  - **Why needed**: Patient location (country) from profile determines which Stripe account processes payments
  - **Integration point**: Payment service queries patient profile for country to route payment to correct Stripe account

- **FR-032 / Module PR-06**: Provider Dashboard Settings & Profile Management
  - **Why needed**: Provider identity and profile context supports provider-scoped payment configuration (deposit/commission overrides) and payout alignment
  - **Integration point**: Payment Configuration uses provider IDs for provider-specific deposit/commission assignment; payout settings are managed in FR-032 and payout execution in FR-017

### External Dependencies (APIs, Services)

- **External Service 1**: Stripe Payment API
  - **Purpose**: Processes all payment transactions using configured Stripe accounts
  - **Integration**: RESTful API calls for payment intent creation, charge capture, payout management
  - **Failure handling**: If Stripe API unavailable, queue payment transactions for retry with exponential backoff, notify admin of Stripe outage

- **External Service 2**: Currency Conversion Rate API (e.g., xe.com, fixer.io)
  - **Purpose**: Fetches real-time currency conversion rates for markup calculation
  - **Integration**: HTTP API calls to fetch current rates for configured currency pairs
  - **Failure handling**: If API unavailable, use last successfully cached rates and alert admin, retry sync with exponential backoff

- **External Service 3**: Admin Email Service
  - **Purpose**: Sends email notifications to admins for configuration changes and rate protection alerts
  - **Integration**: SMTP or transactional email API (e.g., SendGrid, AWS SES)
  - **Failure handling**: If email service unavailable, log notification failures and display in-app notification to admin, retry with queue

### Data Dependencies

- **Entity 1**: Active Provider Profiles with Region Data
  - **Why needed**: Cannot assign provider-specific deposit rates without provider IDs and regional context
  - **Source**: Provider Onboarding & Profile Management module (PR-01)

- **Entity 2**: Regional Groupings and Country Mappings
  - **Why needed**: Cannot map Stripe accounts to regions without defined regional groupings
  - **Source**: Regional Configuration & Pricing module (FR-028 / A-09), which enforces one country per grouping; Stripe mappings must honor that uniqueness

- **Entity 3**: Active Booking Records with Procedure Dates
  - **Why needed**: Cannot calculate installment schedules without knowing booking date and procedure date
  - **Source**: Booking & Scheduling module (FR-006 / P-03)

- **State 1**: Patient Country/Location Data
  - **Why needed**: Cannot route payments to correct regional Stripe account without patient location
  - **Source**: Patient Authentication & Profile Management module (FR-001 / P-01)

---

## Assumptions

### User Behavior Assumptions

- **Assumption 1**: Admins have Stripe account credentials available when configuring payment accounts (publishable key, secret key, webhook secret)
- **Assumption 2**: Admins understand currency conversion markup concept and can determine appropriate markup percentages for their business (typically 3-10%)
- **Assumption 3**: Admins will monitor rate protection alerts and respond within 24 hours to adjust markup if needed
- **Assumption 4**: Admins will configure at most one Stripe account as Global Fallback for countries without specific account assignment
- **Assumption 5**: Admins will test Stripe account connections after initial configuration to verify credentials are correct

### Technology Assumptions

- **Assumption 1**: Platform has secure storage infrastructure for encrypting Stripe API secret keys at rest (AES-256)
- **Assumption 2**: Admin web app accessed via modern browsers supporting password field masking and secure form submission (Chrome, Safari, Firefox - last 2 versions)
- **Assumption 3**: Payment Processing Service has reliable internet connectivity to Stripe API and currency conversion APIs
- **Assumption 4**: System has caching infrastructure to store payment configuration with 5-minute TTL (e.g., Redis, Memcached)
- **Assumption 5**: Currency conversion API providers (xe.com, fixer.io) have 99%+ uptime and provide rate data in standard JSON format

### Business Process Assumptions

- **Assumption 1**: Admins configure Stripe accounts before launching in new geographic regions (cannot process payments without configured account)
- **Assumption 2**: Admins review currency conversion rates at least weekly to ensure markup percentages are appropriate
- **Assumption 3**: Deposit rate percentage (20-30% range) is acceptable to both patients (affordability) and providers (cash flow)
- **Assumption 4**: 30-day cutoff before procedure date is standard business rule, but admins may adjust for specific business needs (30-90 day range)
- **Assumption 5**: Provider-specific deposit rates are exception rather than norm (most providers use global default rate)

---

## Implementation Notes

### Technical Considerations

- **Architecture**: Payment configuration data must be cached with 5-minute TTL to minimize database queries during high-volume payment processing
- **Technology**: Stripe API credentials (secret keys) must be encrypted at rest using AES-256 and never logged in plain text
- **Performance**: Currency conversion rate sync should run as background job on scheduled intervals (not synchronous during payment processing)
- **Storage**: Payment configuration history requires time-series storage for audit trail (10-year retention for financial compliance)
- **Concurrency**: Payment configuration updates must use optimistic locking to prevent race conditions when multiple admins edit simultaneously

### Integration Points

- **Integration 1**: Admin web app sends payment configuration updates to Payment Configuration API via REST
  - **Data format**: JSON payload with configuration type (Stripe account, rate sources, currency pairs, deposit rates, split payment rules)
  - **Authentication**: OAuth 2.0 bearer tokens with elevated admin permissions
  - **Error handling**: Validation errors returned with 400 Bad Request, server errors trigger retry with exponential backoff

- **Integration 2**: Payment Processing Service queries Payment Configuration API for transaction routing and calculation rules
  - **Data format**: RESTful API calls for Stripe account lookup (by country), currency conversion rates, deposit rates, installment rules
  - **Authentication**: Internal service authentication using API keys or mutual TLS
  - **Error handling**: If Configuration API unavailable, use last cached configuration and alert admin, retry with exponential backoff

- **Integration 3**: Per-pair currency conversion rate sync jobs fetch rates from the pair's assigned source (xe.com, fixer.io)
  - **Data format**: HTTP GET requests returning JSON with currency pair rates
  - **Authentication**: API key authentication per rate source (credentials stored in Rate Source entity)
  - **Error handling**: If source API unavailable, keep pair's last cached rate, mark pair status as error, mark source status as down, alert admin. Retry sync with exponential backoff (15 min, 30 min, 1 hour).

- **Integration 4**: Admin email notification service sends alerts for configuration changes and rate protection events
  - **Data format**: SMTP or transactional email API with HTML email templates
  - **Authentication**: SMTP credentials or API keys for email service
  - **Error handling**: If email service unavailable, log notification and display in-app alert to admin

### Scalability Considerations

- **Current scale**: Expected 1,000 payment transactions per day at launch across 10 countries with 3-5 Stripe accounts
- **Growth projection**: Plan for 10,000 transactions per day within 12 months, expanding to 30+ countries with 10-15 Stripe accounts
- **Peak load**: Handle 5x normal transaction volume during promotional campaigns or seasonal booking spikes
- **Configuration data volume**: Payment configuration data is relatively small (< 1MB), but audit log grows over time (estimate 10GB per year)
- **Scaling strategy**: Horizontal scaling of Payment Configuration API, distributed caching (Redis cluster), read replicas for audit log queries

### Security Considerations

- **Authentication**: Elevated admin permissions required to access payment configuration (role-based access control)
- **Authorization**: Only admins with "PaymentConfigAdmin" role can modify Stripe accounts, rate sources, currency pairs, deposit rates, split payment rules
- **Encryption**: Stripe secret keys and webhook secrets encrypted at rest using AES-256, decrypted only in memory during API calls
- **Audit trail**: All payment configuration changes logged with admin ID, timestamp, IP address, before/after state
- **Threat mitigation**: Rate limiting on Payment Configuration API (max 100 requests/minute per admin user) to prevent abuse
- **Compliance**: PCI DSS Level 1 compliance for payment data handling (no storage of full card numbers, CVVs, or PINs)
- **API security**: Payment Configuration API requires TLS 1.3 for all connections, no plain HTTP allowed
- **Secret rotation**: Support for Stripe API key rotation without downtime (configure new keys, test, then deactivate old keys)

---

## User Scenarios & Testing

<!--
  IMPORTANT: User stories prioritized as user journeys ordered by importance.
  Each user story is INDEPENDENTLY TESTABLE.
-->

### User Story 1 - Configure First Stripe Account for Single Region (Priority: P1)

As a platform administrator launching Hairline in the United States, I need to configure the first Stripe account and assign it to the US region so that patients in the US can complete booking payments.

**Why this priority**: This is the foundational capability required before any payment processing can occur. Without at least one configured Stripe account, the platform cannot accept payments.

**Independent Test**: Can be fully tested by adding Stripe account with US region assignment, then submitting test payment from US patient account and verifying payment routes to correct Stripe account.

**Acceptance Scenarios**:

1. **Given** I am an admin with elevated permissions, **When** I navigate to Payment Configuration > Stripe Accounts and click "Add New Account", **Then** I see the Stripe account configuration form with all required fields
2. **Given** I have Stripe API credentials for US account, **When** I enter publishable key, secret key, webhook secret, and select "United States" as assigned country, **Then** system validates credentials by testing Stripe API connection
3. **Given** Stripe API credentials are valid, **When** I click "Save & Activate", **Then** system stores Stripe account configuration and displays confirmation message "Stripe account activated for United States"
4. **Given** Stripe account is active for US, **When** US patient attempts booking payment, **Then** payment routes to correct US Stripe account and processes successfully
5. **Given** Stripe account is configured, **When** I view Stripe Accounts list, **Then** I see US account with status "Active" and last connection test timestamp

---

### User Story 2 - Configure Currency Conversion Sources and Pairs (Priority: P2)

As a platform administrator managing international payments, I need to configure rate sources, set global defaults, and add currency pairs (auto-fetch or manual) with markup percentages so that patients see accurate prices in their local currency and the platform is protected against unfavorable conversion rates.

**Why this priority**: Currency conversion is critical for international operations but can be configured after basic Stripe accounts. This enables multi-currency payment processing with revenue protection.

**Independent Test**: Can be fully tested by: (1) adding xe.com as a rate source with valid API key, (2) setting global defaults (5% markup, 6h sync, 3% rate protection), (3) adding USD/EUR pair in auto-fetch mode linked to xe.com source, (4) adding USD/TRY pair in manual mode with a manually entered rate, then verifying auto-fetch pair syncs on schedule and manual pair uses the entered rate, both with correct markup applied to patient-facing prices.

**Acceptance Scenarios**:

1. **Given** I am an admin, **When** I navigate to Payment Configuration > Currency Conversion, **Then** I see Screen 2A with global settings section, rate sources section, and currency pair list
2. **Given** I click "Add Source", enter "xe.com — Production" as name, select xe.com as provider, and enter API key, **When** system runs test connection, **Then** system validates credentials and saves the source with green status indicator
3. **Given** I set Global Default Markup to 5%, Global Default Sync Frequency to 6h, and Rate Protection Threshold to 3%, **When** I click "Save Global Settings", **Then** system stores global defaults
4. **Given** I click "Add Pair" and select EUR as target currency, choose "Auto-fetch" mode, and select the xe.com source, **When** I click "Test Connection & Fetch Rate", **Then** system fetches the current USD/EUR rate and displays it in the Base Rate field with effective rate preview
5. **Given** I leave Markup % blank (inheriting global 5%), **When** I click "Save", **Then** system stores the pair with "(global)" markup indicator, schedules first sync from save timestamp, and pair appears on the list with green status
6. **Given** I click "Add Pair" and select TRY as target currency, choose "Manual" mode, **When** I enter 34.50 as the base rate, **Then** system shows effective rate preview as 36.225 (34.50 × 1.05) and I can save the pair
7. **Given** USD/EUR auto-fetch pair has 6h sync frequency, **When** the scheduled sync runs, **Then** system fetches the latest rate from xe.com, applies 5% markup, and updates the pair's effective rate on the list
8. **Given** currency pairs are configured, **When** UK patient views US provider's $2,000 procedure, **Then** patient sees price in GBP using the USD/GBP pair's effective rate (or USD if no GBP pair is configured)

---

### User Story 3 - Configure Split Payment Installment Plans (Priority: P2)

As a platform administrator aiming to increase booking conversion rates, I need to configure split payment installment options (2-9 installments) with a 30-day cutoff rule so that patients can spread booking costs over time and are more likely to complete bookings.

**Why this priority**: Split payments significantly improve booking conversion by reducing upfront cost burden. This can be configured independently of other payment settings and delivers immediate business value.

**Independent Test**: Can be fully tested by enabling 2, 3, 4, 5, 6 installment options with 30-day cutoff, then submitting a test booking 210 days before procedure and verifying patient sees all enabled options, while a booking 90 days before procedure only shows feasible options (e.g., 2-3 installments).

**Acceptance Scenarios**:

1. **Given** I am an admin, **When** I navigate to Payment Configuration > Split Payment, **Then** I see configuration form for available installments, cutoff days, and minimum booking amount
2. **Given** I enable 2, 3, 4, 5, 6 installment options, **When** I set cutoff days to 30 and minimum booking amount to $500, **Then** system stores split payment rules
3. **Given** split payment is configured with 30-day cutoff, **When** patient books $2,000 procedure 210 days in advance, **Then** patient sees all enabled installment options (2-6 installments)
4. **Given** same configuration, **When** patient books $2,000 procedure 90 days in advance, **Then** patient sees only feasible installment options (e.g., 2-3 installments)
5. **Given** patient selects 3 installments for $2,000 booking, **When** patient completes booking, **Then** system calculates payment schedule:
   - 3 installments: $666.67 each (rounded; last installment absorbs rounding difference), due monthly (every ~30 days)
   - Final installment due: 30 days before procedure date
6. **Given** patient has active installment plan, **When** patient misses second installment payment deadline, **Then** system sends reminder notification during grace period, then cancels booking if not paid within grace period

---

### User Story 4 - Configure Provider-Specific Deposit Rates (Priority: P3)

As a platform administrator managing diverse provider needs, I need to configure custom deposit rates for specific providers (different from the global default 25%) so that providers with different cash flow requirements can have appropriate deposit percentages while most providers use the global default.

**Why this priority**: Provider-specific deposit rates add flexibility but are not critical for launch. Most providers can use global default, and this can be added after basic deposit rate configuration is working.

**Independent Test**: Can be fully tested by setting global deposit rate to 25%, then assigning custom 30% rate to specific provider, then verifying that provider's bookings use 30% deposit while other providers use 25% deposit.

**Acceptance Scenarios**:

1. **Given** I am an admin, **When** I navigate to Payment Configuration > Deposit Rates, **Then** I see configuration form with options for Global Default or Provider-Specific scope
2. **Given** I select Provider-Specific scope, **When** I search for provider "Dr. Smith Hair Clinic", **Then** system displays matching provider in search results
3. **Given** I select provider and set custom deposit rate to 30%, **When** I click "Apply Deposit Rate", **Then** system stores provider-specific rate and displays confirmation: "Custom deposit rate 30% applied to Dr. Smith Hair Clinic"
4. **Given** provider has custom 30% deposit rate, **When** patient books procedure with this provider (booking total $3,000), **Then** system calculates deposit as $900 (30% of $3,000)
5. **Given** different provider uses global default 25% rate, **When** patient books procedure with this provider (booking total $3,000), **Then** system calculates deposit as $750 (25% of $3,000)
6. **Given** provider-specific rate is configured, **When** I view Deposit Rates configuration page, **Then** I see list of providers with custom rates showing provider name, custom rate, and override indicator

---

### User Story 5 - Monitor and Respond to Currency Rate Protection Alerts (Priority: P3)

As a platform administrator managing international payments, I need to receive timely alerts when auto-fetch currency pairs fluctuate significantly (exceeding the global rate protection threshold) so that I can adjust per-pair markup percentages to protect the platform against unfavorable conversion rates and revenue loss.

**Why this priority**: Rate protection adds proactive monitoring but is not essential for launch. Admins can manually monitor rates initially, and this can be added as operational maturity improves.

**Independent Test**: Can be fully tested by configuring 3% global rate protection threshold, adding USD/EUR auto-fetch pair, simulating 4% rate change in test environment, then verifying: (a) the pair's status turns yellow/warning on the pair list, (b) admin receives alert email within 15 minutes, and (c) admin can adjust the pair's markup percentage in response.

**Acceptance Scenarios**:

1. **Given** I have configured global rate protection threshold at 3% and USD/EUR is an auto-fetch pair, **When** scheduled sync detects USD/EUR rate increased 4% in 24 hours, **Then** system marks the USD/EUR pair status as yellow/warning on the pair list (Screen 2A) and sends urgent alert email to admin: "Currency alert: USD/EUR rate changed 4% in 24 hours (threshold: 3%). Review markup for this pair."
2. **Given** I receive rate protection alert, **When** I navigate to Payment Configuration > Currency Conversion (Screen 2A), **Then** I see yellow warning badge on USD/EUR pair row with tooltip: "Rate change: +4% (24h)"
3. **Given** I click on the USD/EUR pair to edit (Screen 2B) and decide to increase markup, **When** I update USD/EUR per-pair markup from blank (global 5%) to 7% and click "Save", **Then** system applies new 7% markup to this pair, recalculates effective rate, and logs admin action to audit trail
4. **Given** markup is updated for USD/EUR, **When** next patient views price in EUR, **Then** price reflects new 7% per-pair markup instead of previous 5% global default
5. **Given** rate protection alert was triggered, **When** I view the pair's "Rate History" section in Screen 2B, **Then** chart shows rate spike and timestamp when alert was sent

---

### Edge Cases

- What happens when admin attempts to delete Stripe account that processed transactions in last 90 days? **System prevents deletion and displays error: "Cannot delete Stripe account with recent transactions. Archive instead."** System archives account, marking as inactive but retaining configuration for audit purposes.

- How does system handle a rate source being completely unavailable for 24+ hours? **For each auto-fetch pair using the affected source: system continues using the pair's last successfully cached rate, marks the pair's status as red/error on the pair list (Screen 2A), and marks the source's status as red in the Sources section.** System sends daily email digest to admin summarizing the source outage and listing all affected pairs. When the source recovers, the next scheduled sync for each affected pair fetches the latest rate and restores green status. Admin can also switch affected pairs to a different source or manual mode at any time during the outage.

- What occurs if admin configures cutoff date (e.g., 60 days) that prevents any installment options from being offered for most bookings? **System displays warning during configuration: "Current cutoff date [60 days] may prevent installment options for most bookings. Only bookings made 75+ days in advance will see installments."** Admin can choose to proceed with restrictive cutoff or adjust to more reasonable value (e.g., 30 days). System logs warning to admin activity log.

- How to manage patient attempting payment from country with no assigned Stripe account and no Global Fallback configured? **System checks patient country, finds no Stripe account assigned, checks for Global Fallback, finds none. System displays error to patient: "Payment processing not available for your location. Please contact support."** System sends urgent alert to admin: "Payment blocked for [Country]: No Stripe account configured. Expand regional coverage."** Payment attempt logged to admin dashboard for follow-up.

- What happens when patient books procedure 35 days before procedure date with 30-day cutoff enabled, and selects 3 installments? **System calculates time between booking date (35 days before) and cutoff date (30 days before) = 5 days available for installments. System determines 3 installments not feasible (would require payments every 1.67 days). System displays error: "Insufficient time for 3 installments. Please select 2 installments or pay in full."** Patient must select fewer installments or pay deposit + remaining balance immediately.

- How does system handle rapid currency fluctuation exceeding rate protection threshold multiple times in single day for one pair (e.g., USD/EUR changes 3% at 8am, another 3% at 2pm, another 3% at 8pm)? **System sends first alert at 8am when the pair's initial 3% threshold is crossed and marks the pair's status as yellow/warning on the pair list. System applies rate-limiting to alerts (maximum one alert per currency pair per 6 hours) to prevent alert fatigue. System accumulates rate changes and sends second alert at 2pm showing cumulative change: "USD/EUR increased 6% in 6 hours."** The pair's yellow/warning status persists on Screen 2A until the admin reviews and acknowledges. Admin receives summary of all rate changes across all pairs in daily digest email.

- What occurs if admin configures two different Stripe accounts for overlapping countries (e.g., Account A for US/Canada/Mexico, Account B for US/UK)? **System detects country overlap (US) during configuration and displays warning: "US is already assigned to Account A. Override assignment?"** Admin selects: "Override" (US moves to Account B, no longer uses Account A) or "Cancel" (keep current assignment). System logs conflict resolution to audit trail. If admin overrides, system uses most recently configured account for overlapping country (Account B for US in this example).

- How to manage admin accidentally entering incorrect Stripe secret key that initially validates but later fails during actual payment processing? **During configuration, system validates Stripe credentials by making test API call to Stripe. If credentials are syntactically correct but have insufficient permissions or are later revoked by Stripe, first payment attempt will fail. Payment Processing Service logs error: "Stripe authentication failed for account [name]."** System sends urgent alert to admin: "Stripe account [name] failed authentication. Verify API keys are active and have required permissions."** System temporarily routes payments to Global Fallback (if configured) and displays error banner to admin.

---

## Functional Requirements Summary

### Core Requirements

- **REQ-029-001**: System MUST allow admins to add, edit, and manage multiple Stripe accounts with API credentials (publishable key, secret key, webhook secret)
- **REQ-029-002**: System MUST allow admins to assign Stripe accounts to specific countries or regional groupings (multi-select assignment)
- **REQ-029-003**: System MUST validate Stripe API credentials by testing connection to Stripe API before activating account
- **REQ-029-004**: System MUST route payment transactions to appropriate Stripe account based on patient's country location
- **REQ-029-004b**: System MUST support an optional Stripe account marked as Global Fallback used only when no country/regional grouping mapping exists (at most 1 Global Fallback account)
- **REQ-029-005**: System MUST support multiple currencies per Stripe account and allow admins to configure supported currencies
- **REQ-029-006**: System MUST allow admins to manage rate sources (add, edit, delete) where each source bundles a provider type (xe.com, fixer.io) with its API credentials. Source creation requires a successful test connection before saving. Source deletion is blocked if currency pairs reference it; admin must reassign or convert affected pairs first.
- **REQ-029-006b**: System MUST allow admins to create and manage currency pairs (CRUD), where each pair has USD as the mandatory base currency and a configurable rate mode: auto-fetch (from a configured source) or manual input (admin-entered base rate).
- **REQ-029-007**: System MUST allow admins to set a global default markup percentage (0-20% range) and optionally override it per currency pair (0-20% range). If a pair has no per-pair markup, the global default applies.
- **REQ-029-007b**: System MUST allow admins to set a global default sync frequency (1h, 3h, 6h, 12h, 24h) and optionally override it per auto-fetch currency pair. If an auto-fetch pair has no per-pair sync frequency, the global default applies. Each pair's sync schedule is calculated from the time it was saved (e.g., saved at 12:36 with 6h interval → next sync at 18:36).
- **REQ-029-008**: System MUST fetch currency conversion rates automatically for each auto-fetch pair on its configured sync schedule (per-pair or inherited global frequency). Manual-mode pairs are not synced.
- **REQ-029-009**: System MUST calculate and display the effective rate for each pair as: Base Rate × (1 + Markup %). This effective rate is applied to patient-facing prices.
- **REQ-029-010**: System MUST allow admins to configure a global rate protection threshold (1-50% range). System monitors each auto-fetch pair independently and marks the pair's status as yellow/warning and sends an alert notification when the pair's rate changes more than the threshold within 24 hours.
- **REQ-029-011**: System MUST require a successful "Test Connection & Fetch Rate" action before saving any new auto-fetch currency pair. The Save button is disabled until this test succeeds.
- **REQ-029-011b**: For any currency not configured as a pair, the system MUST fall back to collecting payment in USD (no conversion attempted). The admin dashboard MUST display a note informing admins of this fallback behavior.
- **REQ-029-012**: System MUST gracefully handle per-pair rate source failures by keeping the last successfully fetched rate, marking the pair's status as red/error on the pair list, and alerting admin. If a source is deleted, all pairs referencing it MUST gracefully switch to manual mode with the last fetched rate pre-filled.
- **REQ-029-013**: System MUST allow admins to configure deposit rate percentage (20-30% range) globally for all providers
- **REQ-029-014**: System MUST allow admins to configure provider-specific deposit rates that override global default for selected providers
- **REQ-029-015**: System MUST apply deposit rate changes to new bookings only (existing bookings retain original deposit rate)
- **REQ-029-016**: System MUST calculate deposit amount by multiplying booking total by configured deposit rate percentage
- **REQ-029-017**: System MUST allow admins to enable or disable split payment (installment) feature globally
- **REQ-029-018**: System MUST allow admins to select available installment options (2-9 installments) via multi-select checkboxes
- **REQ-029-019**: System MUST allow admins to configure cutoff days (30-90 day range) requiring full payment completion before procedure date
- **REQ-029-020**: System MUST allow admins to configure minimum booking amount ($100-$10,000 range) required to qualify for installments
- **REQ-029-021**: System MUST automatically calculate available installment options based on booking date, procedure date, and cutoff days
- **REQ-029-022**: System MUST generate installment payment schedules using equal-split amounts: booking total ÷ installment count (rounded to 2 decimal places; last installment absorbs rounding difference)
- **REQ-029-023**: System MUST allow admins to configure late payment grace period (0-14 days) before booking cancellation
- **REQ-029-043**: System MUST allow admins to configure platform commission rates (global default and provider-specific overrides; allowed range 15-25%) applied to new bookings only (existing bookings retain the commission rate snapshot used at booking confirmation)
- **REQ-029-044**: System MUST lock currency conversion rates (including markup) at quote acceptance and store them per quote/booking/transaction (no rate fluctuation after quote acceptance)
- **REQ-029-045**: System MUST snapshot commission rate at booking confirmation and store it per booking/transaction for payout and reconciliation consistency

### Data Requirements

- **REQ-029-024**: System MUST persist all payment configuration data (Stripe accounts, rate sources, currency pairs, global conversion settings, deposit rates, commission rates, split payment rules) with full audit history
- **REQ-029-025**: System MUST log all payment configuration changes to audit trail with admin ID, timestamp, IP address, and before/after state
- **REQ-029-026**: System MUST cache payment configuration data with 5-minute TTL to minimize database queries during payment processing
- **REQ-029-027**: System MUST retain payment configuration audit history for minimum 10 years for financial compliance

### Security & Privacy Requirements

- **REQ-029-028**: System MUST encrypt Stripe API secret keys and webhook secrets at rest using AES-256 encryption
- **REQ-029-029**: System MUST never log Stripe secret keys in plain text to audit logs or error logs (mask all but last 4 characters)
- **REQ-029-030**: System MUST require elevated admin permissions ("PaymentConfigAdmin" role) to access payment configuration functionality
- **REQ-029-031**: System MUST use TLS 1.3 for all connections to Payment Configuration API (no plain HTTP allowed)
- **REQ-029-032**: System MUST comply with PCI DSS Level 1 requirements for payment data handling
- **REQ-029-046**: System MUST verify Stripe webhook signatures for all incoming webhook events using the configured webhook secret

### Integration Requirements

- **REQ-029-033**: System MUST provide RESTful API for Payment Processing Service to query payment configuration (Stripe accounts, currency pair effective rates, deposit rates, installment rules)
- **REQ-029-034**: System MUST integrate with external currency conversion rate APIs (xe.com, fixer.io) via HTTP GET requests, using credentials stored per rate source
- **REQ-029-035**: System MUST send email notifications to admins for payment configuration changes and rate protection alerts
- **REQ-029-036**: System MUST propagate payment configuration changes to Payment Processing Service within 5 minutes maximum (cache TTL)

### Validation & Error Handling Requirements

- **REQ-029-037**: System MUST validate deposit rate percentage is within allowed range (20-30%) and display error if out of range
- **REQ-029-038**: System MUST validate markup percentage is within allowed range (0-20%) and display error if out of range
- **REQ-029-039**: System MUST validate cutoff days is within allowed range (30-90 days) and display error if out of range
- **REQ-029-040**: System MUST prevent deletion of Stripe accounts with transactions in last 90 days (archive instead)
- **REQ-029-041**: System MUST prevent modification of deposit rates or split payment rules for bookings with active references (changes apply to new bookings only)
- **REQ-029-042**: System MUST display warning if admin configures aggressive cutoff date that may limit installment availability

---

## Key Entities

- **Entity 1 - Stripe Account Configuration**:
  - **Key attributes**: account_id, account_name, publishable_key, secret_key_encrypted, webhook_secret_encrypted, mode (test/live), is_global_fallback (boolean), assigned_countries[], supported_currencies[], default_currency, status (active/inactive), created_date, last_tested_date
  - **Relationships**: One Stripe account assigned to many countries; one country can map to one Stripe account. If no mapping exists for a patient country, the system uses the Stripe account marked as Global Fallback (if configured).

- **Entity 2a - Currency Conversion Global Settings**:
  - **Key attributes**: config_id, global_default_markup_percentage, global_default_sync_frequency, rate_protection_threshold, created_by_admin_id, updated_date
  - **Relationships**: One global settings record; provides defaults inherited by currency pairs that do not specify per-pair overrides

- **Entity 2b - Rate Source**:
  - **Key attributes**: source_id, source_name, provider_type (xe.com/fixer.io), api_key_encrypted, status (healthy/degraded/down), last_tested_timestamp, created_by_admin_id, created_date
  - **Relationships**: One source serves many currency pairs (auto-fetch mode); deleting a source requires reassigning or converting all referencing pairs first

- **Entity 2c - Currency Pair Configuration**:
  - **Key attributes**: pair_id, base_currency (always USD), target_currency, rate_mode (auto/manual), source_id (nullable; required if auto), manual_base_rate (nullable; required if manual), markup_percentage_override (nullable; if null, inherits global default), sync_frequency_override (nullable; if null, inherits global default; ignored if manual), current_base_rate, current_effective_rate, last_updated_timestamp, next_sync_timestamp (nullable; auto-fetch only), status (healthy/warning/error), created_by_admin_id, created_date
  - **Relationships**: One pair per target currency (unique constraint on target_currency); many quotes/bookings/transactions reference the pair's effective rate snapshot captured at quote acceptance; one pair references one source (if auto-fetch)

- **Entity 3 - Deposit Rate Configuration**:
  - **Key attributes**: config_id, scope (global/provider_specific), provider_id (null for global), deposit_percentage, effective_date, created_by_admin_id, created_date
  - **Relationships**: One global deposit rate; many provider-specific deposit rate overrides (one per provider); many bookings reference deposit rate configuration

- **Entity 4 - Split Payment Configuration**:
  - **Key attributes**: config_id, feature_enabled (boolean), available_installments[] (2-9), cutoff_days, minimum_booking_amount, late_payment_grace_period_days, effective_date, created_by_admin_id
  - **Relationships**: One split payment configuration (global); many bookings reference split payment rules; many installment schedules generated based on configuration

- **Entity 5 - Payment Configuration Audit Log**:
  - **Key attributes**: audit_id, config_type (stripe_account/currency_conversion/deposit_rate/commission_rate/split_payment), action (create/update/delete/archive), admin_id, timestamp, ip_address, before_state_json, after_state_json, change_summary
  - **Relationships**: Many audit log entries per payment configuration entity; one admin user creates many audit log entries

- **Entity 6 - Commission Rate Configuration**:
  - **Key attributes**: config_id, scope (global/provider_specific), provider_id (null for global), commission_percentage, effective_date, created_by_admin_id, created_date
  - **Relationships**: One global commission rate; many provider-specific commission rate overrides (one per provider); bookings and payouts reference the commission rate snapshot captured at booking confirmation

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-13 | 1.0 | Initial PRD creation for FR-029: Payment System Configuration | Claude (AI Assistant) |
| 2025-12-16 | 1.1 | Major revisions: Added commission rate configuration (global + provider-specific) and aligned split payment rules with cross-FR constraints (monthly cadence, 30+ day cutoff). Added Constitution compliance requirements (webhook signature verification, FX and commission snapshot at booking, audit retention 10 years). Fixed module code placeholders and corrected currency conversion example. | AI |
| 2025-12-16 | 1.2 | Status updated to Verified & Approved; All approvals completed | Product Team |
| 2026-01-14 | 1.3 | Added Currency Management screen (central supported currency list) and aligned admin editability rules | AI |
| 2026-02-10 | 1.4 | **Major redesign of Currency Conversion Configuration (Screen 2).** Replaced flat form with two-screen model: Screen 2A (pair list + global settings + rate sources) and Screen 2B (add/edit pair). Key changes: (1) Rate sources are now first-class entities bundling provider type with API credentials; (2) Each currency pair independently chooses auto-fetch or manual mode; (3) Markup % and sync frequency support global defaults with per-pair overrides; (4) Sync schedule per pair is calculated from pair save timestamp; (5) USD fallback for unconfigured currencies; (6) Graceful source deletion (pairs switch to manual with last rate pre-filled); (7) Visual status indicators per pair and per source. Updated Main Flow, Alternative Flows (A3/A3b), Boundary Flows (B2/B5), Edge Cases, User Stories 2 & 5, REQ-029-006 through REQ-029-012, Key Entities (2a/2b/2c), Admin Editability Rules, Integration Points, and Security references. | AI |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner |  | 2025-12-16 | ✅ Approved |
| Technical Lead |  | 2025-12-16 | ✅ Approved |
| Stakeholder |  | 2025-12-16 | ✅ Approved |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-029 from system-prd.md + Hairline-AdminPlatformPart2.txt transcription
**Last Updated**: 2026-02-10
