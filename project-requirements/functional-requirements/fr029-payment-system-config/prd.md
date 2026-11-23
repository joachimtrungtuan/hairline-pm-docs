# FR-029 - Payment System Configuration

**Module**: A-09: System Settings & Configuration
**Feature Branch**: `fr029-payment-system-config`
**Created**: 2025-11-13
**Version**: 1.18
**Status**: 🟡 Revised — Pending Consolidated Verification
**Source**: FR-029 from system-prd.md (lines 1427-1455) + Hairline-AdminPlatformPart2.txt (lines 128-230)
**Change Request**: [CR-FR029-20261014-01 — Provider-specific Flat Rate commission alignment with FR-015](../../../../archived/prd-baseline-2026-11-08/fr029-payment-system-config/change-request-2026-10-14-provider-flat-rate-commission.md)
**Change Request**: [CR-FR029-20261015-01 — Single-provider scope edits and scheduled commission configuration](../../../../archived/prd-baseline-2026-11-08/fr029-payment-system-config/change-request-2026-10-15-single-provider-scope-scheduled-commission.md)
**Change Request**: [CR-FR029-20261015-02 — Suspended providers in provider-specific commission scopes](../../../../archived/prd-baseline-2026-11-08/fr029-payment-system-config/change-request-2026-10-15-suspended-provider-commission-scopes.md)
**Change Request**: [CR-FR029-20261016-01 — Quote model alignment: configuration lock points and booking total](../../../../archived/prd-baseline-2026-11-08/fr029-payment-system-config/change-request-2026-10-16-mtg002-quote-model-alignment.md)

---

## Executive Summary

The Payment System Configuration module empowers platform administrators to manage the complete payment infrastructure for the Hairline multi-tenant platform. This feature enables admins to configure and manage multiple Stripe accounts, map payment accounts to specific countries or regional groups, manage the platform’s enabled currency list (system-supported currencies), set up currency conversion rules with markup percentages, configure deposit rates (20-30% of total booking amount), configure commission settings with both a platform global default and provider-specific commission scopes, and define split payment (installment) plans with cutoff rules.

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
- Patients cannot view or modify payment system configuration settings (REQ-029-061)
- Patients experience seamless payment processing using the appropriate Stripe account for their region

**Provider Platform (PR-05: Financial Management & Reporting)**:

- Patient payments are collected into the Stripe account mapped to the patient’s region; provider payouts are later executed in FR-017 using those funds (provider bank details in FR-032). Providers do not configure Stripe accounts here. (REQ-029-062)
- Providers have no direct interaction with payment system configuration (REQ-029-061)
- Providers see booking payments processed according to deposit rates and installment rules
- Payout to a clinic follows its payout rail: automatic release on the Stripe Connect rail, or the one platform-wide settlement period set in this module for manually paid clinics; payout processing is handled in FR-017 (Admin Billing & Financial Management)

**Admin Platform (A-09: System Settings & Configuration)**:

- Admins manage multiple Stripe accounts with API key configuration
- Admins assign Stripe accounts to specific countries or regional groupings
- Admins enable/disable which currencies are available across the system (central supported currency list) and set the default currency
- Admins configure currency conversion rate sources (e.g., xe.com API integration)
- Admins set currency conversion markup percentages (e.g., 5-10%) to protect against rate fluctuations
- Admins configure deposit rate percentage (20-30%) globally or per provider
- Admins configure commission settings: a platform global default percentage (15-25%) plus provider-specific commission scopes for selected providers using either the Percentage model (0-100%) or the Flat Rate model (fixed amount > 0 per completed procedure); FR-015 exposes the same provider-specific commission data inside the provider profile for single-provider management
- Admins define split payment options (2-9 installments) and cutoff rules (e.g., 30 days before procedure)
- Admins set the refund ladder (refund percentage by days before the procedure date), the late payment fee and the rescheduling fee, the balance due days for the deposit-and-balance option and the unpaid balance cancellation point, Hairline's share of a patient cancellation fee, the fixed deduction applied to a clinic that cancels, the patient confirmation window and the weekly settlement days for manually paid clinics, and turn payment methods on or off per region and currency
- Admins monitor payment configuration health and receive alerts for rate protection thresholds
- Admins audit configuration change history for compliance

**Shared Services (S-02: Payment Processing Service)**:

- Payment Processing Service routes patient payment transactions (deposits/installments/finals) to the appropriate Stripe account based on the country on the patient's profile
- Currency conversion service fetches real-time rates and applies admin-configured markup
- Deposit calculation service applies configured deposit rate to booking totals
- Commission calculation service applies the effective commission snapshot captured at booking confirmation, using an active provider-specific commission configuration when one exists for the provider or the FR-029 global default otherwise
- Installment calculation service generates payment schedules based on configured options and cutoff dates
- Rate protection service monitors currency fluctuations and alerts admins when thresholds exceeded
- Payment audit logging service tracks all transactions for compliance and reconciliation

### Communication Structure

**In Scope**:

- Email notifications to admins when payment configuration changes are published (REQ-029-063)
- System alerts when currency conversion rates exceed configured thresholds (rate protection) (REQ-029-063)
- Admin dashboard notifications for Stripe account connection failures or API errors (REQ-029-063)
- Audit log notifications for payment configuration changes requiring compliance review (REQ-029-063)

**Out of Scope**:

- Patient notifications about payment configuration changes (handled by P-03: Booking & Payment module) (REQ-029-064)
- Provider notifications about payout schedule changes (handled by separate provider payout module) (REQ-029-064)
- SMS notifications for payment failures or processing issues (handled by S-03: Notification Service; **no SMS is sent in MVP and this channel is reserved for future implementation once S-03 SMS delivery is enabled**) (REQ-029-064)
- In-app chat or support messaging (handled by separate support module) (REQ-029-064)

### Entry Points

- **Admin-initiated**: Admin accesses "Payment Configuration" section from admin dashboard settings menu (REQ-029-060)
- **System-triggered**: Payment Processing Service queries payment configuration during every booking transaction (REQ-029-060)
- **API-accessed**: External integrations (if authorized) can query currency conversion rates via read-only API (REQ-029-060)
- **Scheduled jobs**: Currency conversion rate sync runs on scheduled intervals (e.g., every 6 hours) to update cached rates (REQ-029-060)
- **Alert-triggered**: Rate protection system alerts admins when currency fluctuations exceed configured thresholds (REQ-029-060)

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
11. System displays confirmation message: "Deposit rate updated. New bookings will use [X]% deposit rate." (REQ-029-066)
12. System logs configuration change to audit trail with admin ID, timestamp, scope, and rate value
13. System sends email notification to affected providers (if provider-specific change) (REQ-029-065)

### Main Flow: Configure Commission Rates

**Actors**: Admin, System
**Trigger**: Admin navigates to "Payment Configuration > Commission Rates" to configure the platform global default and provider-specific commission scopes
**Outcome**: Commission settings configured for new bookings, with FR-029 and FR-015 staying aligned on provider-specific commission data

**Steps**:

1. Admin clicks "Commission Rates" tab on Payment Configuration page
2. System displays Screen 5 with a Global Default section and a Provider Specific section
3. Admin may update the global commission percentage (range: 15-25% with validation)
4. Admin clicks "Save Setting" for the global default
5. System validates the global commission percentage is within allowed range (15-25%) and stores it with effective date = now
6. Admin may click "Add new provider scope" or edit an existing provider-specific commission scope
7. System displays a provider-scope modal with Selected Providers, Commission Model (Percentage / Flat Rate; default Percentage), Provider Commission Value, Flat Rate Currency (Flat Rate only), Effective Date, and a preview calculation
8. Admin searches for and selects one or more providers
9. Admin selects the commission model, enters the provider-specific commission value (and currency for Flat Rate), and sets the effective date
10. System validates selected providers have status Active or Suspended (Deactivated providers cannot be selected; their existing scopes are read-only) and the commission value matches the selected model: Percentage 0-100% (0.1% precision); Flat Rate amount > 0 in an enabled currency (REQ-029-117)
11. Admin confirms the add or edit action
12. System stores the provider-specific commission scope with provider IDs and effective date
13. System propagates updated commission configuration to Payment Processing Service with cache TTL of 5 minutes
14. System displays confirmation message: "Commission settings updated. New bookings will use the new effective commission configuration." (REQ-029-066)
15. System logs each global-default or provider-scope change to audit trail with admin ID, timestamp, scope, and before/after state
16. If the affected provider is opened in FR-015, the Commission & Financials tab reflects the updated provider-specific commission model and value

### Main Flow: Configure Split Payment (Installment) Plans

**Actors**: Admin, System
**Trigger**: Admin navigates to "Payment Configuration > Split Payment" to configure installment options and cutoff rules
**Outcome**: Installment plan options (2-9 installments) and cutoff date rules configured, available to patients during booking

**Steps**:

1. Admin clicks "Split Payment" tab on Payment Configuration page
2. System displays current split payment configuration showing enabled installment options and cutoff rules
3. Admin enables or disables specific installment options (checkboxes for 2, 3, 4, 5, 6, 7, 8, 9 installments); each checkbox shows the minimum lead time that count needs (cutoff + 30 days x (count - 1))
4. Admin configures cutoff date rule (e.g., "The last installment is due on or before 30 days before procedure date")
5. Admin sets minimum booking amount eligible for split payments (e.g., minimum $500 booking for installments)
6. Admin configures late payment grace period (0-14 days, starting at 0), counted from the installment due date. The late fee is charged once, after the grace period has passed with the installment still unpaid and the automatic retries have ended, and is collected with the next successful charge. A missed payment is cancelled by the Unpaid Balance Cancellation Point on Screen 7, not by this setting
7. Admin reviews preview showing the computed installment schedule (due dates and maximum count) for a sample booking amount and procedure date
8. Admin clicks "Save Split Payment Configuration"
9. System validates cutoff date is reasonable (minimum 30 days, maximum 90 days) and, when the Unpaid Balance Cancellation Point is set, that the cancellation point stays smaller than the new cutoff; it also warns, without refusing the save, when a set cancellation point falls before the day the late payment fee would be charged
10. System stores split payment rules with enabled installment options and cutoff date
11. System propagates configuration to Payment Processing Service with cache TTL of 5 minutes
12. System shows the minimum lead time (cutoff + 30 days) and the installment options a sample booking would be offered
13. System displays confirmation message: "Split payment options updated. Patients will see [X] installment options." (REQ-029-066)
14. System logs configuration change to audit trail
15. System sends email notification to admin confirming split payment configuration

### Main Flow: Configure Refund, Fees and Settlement

**Actors**: Admin, System
**Trigger**: Admin navigates to "Payment Configuration > Refund, Fees and Settlement" (Screen 7)
**Outcome**: The refund ladder, fees, cancellation point, fee shares, confirmation window and settlement days are saved as one global record and read by FR-006, FR-007, FR-007B, FR-015 and FR-017

**Steps**:

1. Admin opens Screen 7
2. System displays the current record; the late payment fee, the rescheduling fee, the cancellation point, Hairline's share and the clinic cancellation deduction show "Not set" until an admin sets them
3. Admin edits any of the fields (refund ladder, late and rescheduling fees, balance due days, cancellation point, Hairline share, clinic cancellation deduction, confirmation window, settlement cutoff and payout day)
4. Admin reviews the ladder preview, which shows the refund amount per band for an example booking total
5. Admin clicks "Save"
6. System validates every changed field against the ranges on Screen 7. Balance due days must be 1 to 30. A set cancellation point must be 1 to 30 and smaller than both the balance due days and the installment cutoff (Screen 4). The settlement cutoff day and payout day must differ. Each fixed fee amount that is set must be above 0. When the system default currency has changed since the last save, every fixed amount that is set (late payment fee, rescheduling fee, clinic cancellation deduction) must have been re-entered in the new currency
7. If a check fails, the system refuses the whole save and names the field and the rule that failed; no field is stored
8. System stores the record; saving does not require every "Not set" field to be filled. If a set cancellation point falls before the day the late payment fee would be charged (Screen 4), the system saves and shows a warning that a booking cancelled at the point never pays the late fee (REQ-029-157)
9. System displays confirmation: "Refund, fees and settlement settings saved. Locked values stay with existing bookings; the other values apply from the next event."
10. System logs the change to the audit trail with admin ID, timestamp and before/after state
11. System sends an email to the admin confirming the change
12. System propagates the record to Payment Processing Service within 5 minutes (cache TTL)
13. While Hairline's share is "Not set", Hairline keeps the whole patient cancellation fee and holders of the Screen 7 permission see a banner on the admin dashboard asking them to set it, which clears when the share is saved. While the late payment fee or the rescheduling fee is "Not set", that fee is not charged. While the cancellation point is "Not set", no unpaid booking is cancelled for non-payment. While the clinic cancellation deduction is "Not set", no deduction is applied

### Main Flow: Manage Supported Currencies

**Actors**: Admin, System
**Trigger**: Admin navigates to "Payment Configuration > Currencies" (Screen 6) to enable, disable or set the default of a currency
**Outcome**: The central supported-currency list is updated and the dropdowns that read it follow

**Steps**:

1. Admin opens Screen 6 and searches or scrolls to a currency
2. Admin turns a currency on or off, or sets an enabled currency as the system default
3. When disabling, the system checks the currency against the block rules: a currency still used by an open quote, an unpaid accepted booking, an open booking or an instalment plan, being the Default Currency of an active Stripe account, or being the Fee Currency of fixed fee amounts stored on Screen 7, cannot be disabled; the system shows the count or the account name. A currency referenced only by configuration (for example a location starting price) shows a warning with the dependent items to update first
4. Admin confirms in a dialog that names the dependent items, if any
5. System stores the change; it affects new configuration choices at once and existing records keep their stored currency code
6. If the default changed, the system creates a new FR-026 Quote Configuration version and shows a banner on Screen 7 asking the admin to re-enter the fixed fee amounts; Screen 7 cannot be saved until each fixed amount that is set has been re-entered in the new currency, and the stored amounts stay in the old currency until then
7. System logs the change to the audit trail and sends an email to the admin confirming it
8. System propagates the list to Payment Processing Service within 5 minutes (cache TTL)

### Alternative Flows

**A1: Add Stripe Account with Regional Grouping Override**:

- **Trigger**: Admin wants to assign a Stripe account to a regional grouping that already has another account assigned
- **Steps**:
  1. Admin attempts to assign countries to new Stripe account that overlap with existing account
  2. System detects conflict and displays warning: "Countries [list] are already assigned to Stripe account [name]"
  3. Admin must choose "Override" to replace existing assignment (no secondary accounts; one account per country/regional grouping) (REQ-029-068)
  4. Admin confirms override action
  5. System checks that the override leaves no other account, apart from the Global Fallback, without assigned countries; if it would, the system refuses with "Account [name] would have no countries. Assign it other countries, or set it Inactive or Archived, first" and changes nothing (REQ-029-152)
  6. System updates country-to-account mappings, replacing prior assignment with the new account
  7. System propagates updated mappings to Payment Processing Service
  8. System logs conflict resolution to audit trail
- **Outcome**: New Stripe account assigned to region, replacing the previous assignment

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

**A2b: Reset Provider-Specific Deposit Rate to Global Default**:

- **Trigger**: Admin wants a provider to follow the global deposit rate again
- **Steps**:
  1. Admin selects a provider from the list of providers with custom rates (Screen 3)
  2. Admin chooses "Reset to global default"
  3. System asks the admin to confirm, showing the provider and the global rate that will apply
  4. System removes the provider-specific rate, logs the change to the audit trail and shows a confirmation; existing bookings keep their own deposit rate (REQ-029-158)
- **Outcome**: The provider follows the global default for new bookings

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
  10. System stores updated pair configuration, schedules recurring sync from save timestamp, and logs change to audit trail; no rate protection comparison runs for the next 24 hours
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

**B1: Stripe API Credential Validation Fails**:

- **Trigger**: Admin enters invalid Stripe API credentials or Stripe API is unreachable
- **Steps**:
  1. Admin submits Stripe account configuration with API credentials
  2. System attempts to validate credentials by calling Stripe API
  3. Stripe API returns authentication error or connection timeout
  4. System displays error message: "Unable to connect to Stripe. Please verify API keys are correct and your Stripe account is active." (REQ-029-067)
  5. System highlights fields with credential errors (publishable key, secret key, webhook secret) (REQ-029-067)
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
  7. System retries sync after exponential backoff (e.g., retry in 15 minutes, then 30 minutes, then 1 hour) (REQ-029-095)
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
  1. Admin sets cutoff date to a high value (e.g., 90 days before procedure)
  2. Admin enables multiple installment options (e.g., 2-9 installments)
  3. System shows the minimum lead time for installments on Screen 4 at all times: cutoff + 30 days (e.g., 120 days for a 90-day cutoff), and the minimum lead time for each enabled count
  4. When the cutoff is above 60 days, the system also displays warning: "With a cutoff of [X] days, only bookings made [X + 30] or more days before the procedure can use installments. Consider lowering the cutoff."
  5. Admin reviews warning and adjusts cutoff date or proceeds with the high cutoff
  6. Admin confirms configuration
  7. System stores configuration but logs warning to admin activity log
- **Outcome**: Admin is informed of potential issue and can adjust cutoff date or accept restrictive configuration

**B5: Currency Fluctuation Exceeds Rate Protection Threshold (Per-Pair)**:

- **Trigger**: Scheduled sync for an auto-fetch pair detects a rate change exceeding the global Rate Protection Threshold (e.g., 3% in 24 hours)
- **Steps**:
  1. System fetches the current rate for USD/EUR from its assigned source during the pair's scheduled sync
  2. System compares the new rate to the pair's rate 24 hours earlier (or, after an Acknowledge, to the rate at the acknowledgement; see step 10)
  3. System detects the USD/EUR rate changed by 4.5% in the last 24 hours (exceeds the 3% global threshold) (REQ-029-096)
  4. System updates the pair's status indicator to yellow/warning on the pair list (Screen 2A)
  5. System sends urgent alert notification to admin: "Currency alert: USD/EUR rate changed 4.5% in 24 hours (threshold: 3%). Review markup for this pair."
  6. Admin sees the yellow warning badge on the pair list, clicks into the pair (Screen 2B) to review
  7. Admin reviews the current base rate, markup %, and effective rate
  8. Admin decides to increase the per-pair markup from 5% to 7% to protect against the unfavorable rate (REQ-029-096)
  9. Admin saves the updated markup; system recalculates the effective rate and logs the change to audit trail
  10. The yellow badge stays until an admin clicks "Acknowledge" on the pair (Screen 2B); a markup change alone does not clear it, and the next sync does not clear it either. The acknowledgement is logged to the audit trail with admin ID and timestamp. After the acknowledgement the pair is compared with the rate at that moment, until the change against the rate 24 hours earlier is again within the threshold; the badge returns, with a new alert (at most one alert per pair every 6 hours), only if the rate moves above the threshold from the acknowledged rate
- **Outcome**: Admin is alerted per-pair to significant rate fluctuations via both visual cues on the list and email notification, and can adjust the specific pair's markup to protect revenue

**B6: No Stripe Account Available for Patient Location**:

- **Trigger**: Patient whose profile country has no assigned Stripe account attempts to pay
- **Steps**:
  1. Payment Processing Service reads the country on the patient's profile (not the patient's physical location), e.g., South Africa
  2. If the profile has no country, the system asks the patient to add one before payment; no account is chosen and no alert is sent
  3. System finds no Stripe account assigned to South Africa (a country held only by an Inactive or Archived account counts as unassigned)
  4. System checks for an Active Stripe account marked as "Global Fallback" in the mode of the deployment (Live on production, Test elsewhere)
  5. If Global Fallback exists: System uses that Stripe account and logs warning to admin
  6. If no fallback: System displays error to patient: "Payment processing not available for your location. Please contact support."
  7. System sends alert to admin: "Payment attempted from unsupported country: South Africa. Configure Stripe account for this region." The alert is sent once per country per day, however many patients try
  8. Once a payment succeeds, the booking keeps the account used for every later charge and refund
- **Outcome**: Patient uses fallback account (if configured) or is unable to complete payment, and admin is alerted to expand regional coverage

---

## Screen Specifications

### Screen 1: Stripe Accounts Management

**Purpose**: Allows admins to add, edit, and manage multiple Stripe accounts and assign them to countries or regional groupings

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Account Name | text | Yes | Friendly name for Stripe account (e.g., "US & Canada Account", "EU Account") | Max 100 chars, must be unique | ENT-stripe-account.account_name (REQ-029-131) |
| Publishable Key | text | Yes | Stripe publishable API key (starts with pk_) | Must start with "pk_test_" or "pk_live_", max 200 chars | ENT-stripe-account.publishable_key (REQ-029-132) |
| Secret Key | password | Yes | Stripe secret API key (starts with sk_) | Must start with "sk_test_" or "sk_live_", max 200 chars | ENT-stripe-account.secret_key_encrypted (REQ-029-133) |
| Webhook Secret | password | Yes | Stripe webhook signing secret | Min 32 chars, max 200 chars | ENT-stripe-account.webhook_secret_encrypted (REQ-029-134) |
| Account Mode | select | Yes | Test Mode or Live Mode | Must select one option | ENT-stripe-account.mode |
| Global Fallback | toggle | No | If enabled, this Stripe account is used when no country/regional grouping mapping exists for the patient, or when the mapped account fails authentication | At most 1 Stripe account can be marked as Global Fallback. If enabled: Assigned Countries must be empty, Account Status must be Active and Account Mode must be Live on a production deployment and Test elsewhere (see Business Rules). The flag must be moved to another account before this account can be set Inactive or Archived. | ENT-stripe-account.is_global_fallback (REQ-029-139) |
| Assigned Countries | multi-select | Conditional | Countries **or** regional groupings served by this account (mutually exclusive per record: choose groups or countries, not both) | Required unless Global Fallback is enabled or the account is Inactive or Archived (such an account may hold no countries, and any it holds are ignored for routing). Each country/grouping can map to only one Stripe account (overrides required to reassign). If a country mapping exists, it overrides any group-level account for that country. | ENT-stripe-account.assigned_countries (REQ-029-071) |
| Supported Currencies | multi-select | Yes | Currencies this Stripe account can process (e.g., USD, EUR, GBP) | Must select at least one currency | ENT-stripe-account.supported_currencies |
| Default Currency | select | Yes | Default currency for this account | Must be one of selected supported currencies | ENT-stripe-account.default_currency (REQ-029-135) |
| Account Status | select | Yes | Active, Inactive or Archived. Active takes new bookings. Inactive and Archived take no new bookings; an Archived account is also hidden from the default list. Neither status stops charges and refunds for bookings that already use the account. The countries of an Inactive or Archived account are treated as unassigned, so those patients pay through the Global Fallback or, with none, are blocked (Boundary Flow B6) | One of the three values; an Archived account can be deleted only when no open booking or active installment plan uses it | ENT-stripe-account.status |
| Enabled Payment Methods | multi-select | Yes | Payment methods offered to patients for the regions and currencies this account serves. The method records are owned by FR-007B; this setting only turns each method on or off | Must select at least one method; a method can be offered only in a currency the account supports, checked against the charge currency (USD when the USD fallback applies) | no graph field (setting SET-supported-payment-methods) |

**Business Rules**:

- Payment methods are enabled or disabled per region and currency; FR-007 offers a patient only the methods enabled for the patient's region and the charge currency (the booking currency, or USD when the USD fallback below applies, checked after the fallback)
- Stripe API credentials must be validated before account can be activated (test connection to Stripe API)
- One account per country/regional grouping (from FR-028); reassignments require explicit override
- Country-level assignment supersedes group-level assignment for any country already in that group (most-specific mapping wins) (REQ-029-069)
- At most one Stripe account can be marked as Global Fallback; Global Fallback cannot have explicit country/regional grouping assignments (REQ-029-070)
- A Stripe account cannot be deleted while any open booking or active installment plan uses it; set it to Archived instead. The 90-day transaction test no longer applies. Deposit rates and the single global split payment record are configuration values, not accounts, and are not deleted by this rule
- A booking keeps the Stripe account that took its first payment for every later charge and refund; reassigning countries, a profile-country change or an override changes only new bookings (stored on the booking by FR-007)
- On a production deployment, country routing and Global Fallback consider Live-mode accounts only; elsewhere they consider Test-mode accounts only. The Global Fallback account must be Live on a production deployment and Test elsewhere. When the mapped account fails authentication, new bookings go to the Global Fallback, and routing returns to the mapped account when its next Test Connection passes; if the failing account is the Global Fallback itself, or none exists, payment is blocked with the Boundary Flow B6 error and alert
- An override (Alternative Flow A1) that would leave an account with no assigned countries, and that is not the Global Fallback, is blocked until the admin assigns other countries to that account or sets it Inactive or Archived. Countries stored on an Inactive or Archived account are kept but ignored for routing
- If the routed account does not support the booking currency, the charge is made in USD, converted at the quote-to-USD rate in the rate set locked at quote acceptance with the markup (Payment Rule 3), the same fallback as a missing currency pair (Screen 2A)
- Admin can test Stripe connection at any time by clicking "Test Connection" button (REQ-029-073)
- Webhook secret is required for payment event verification and cannot be left blank
- Supported currencies must be compatible with assigned countries (e.g., EUR for European countries) (REQ-029-072)
- Changes to Stripe account configuration propagate to Payment Processing Service within 5 minutes (cache TTL)

**Notes**:

- Display last successful connection test timestamp below API credential fields (ENT-stripe-account.last_tested_date)
- Show warning icon if Stripe account hasn't been tested in over 30 days (REQ-029-073)
- Provide inline help text explaining difference between Test Mode and Live Mode
- Display transaction count and total volume processed by each account (last 30 days) for admin reference
- Use password masking for Secret Key and Webhook Secret fields, with "Show" toggle button
- Include "Test Connection" action button that opens a modal/sub-screen:
  - Shows account name, mode (Test/Live), and endpoint being validated
  - On submit, system calls Stripe with provided keys/webhook secret; displays success/failure with error details
  - Logs test attempt (admin, timestamp, result) and updates "Last Tested" timestamp/status badge (REQ-029-073)

---

### Screen 2A: Currency Conversion — Pair List & Global Settings

**Purpose**: Central dashboard for managing all currency conversion pairs, rate sources, and global defaults. This screen has two sections: Global Settings and Currency Pair List.

#### Section 1: Global Settings

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Global Default Markup % | number | Yes | Default markup percentage applied to any currency pair that does not have a per-pair override | Range: 0-20%, decimal precision: 0.01% | ENT-currency-conversion-settings.global_default_markup_percentage |
| Global Default Sync Frequency | select | Yes | Default sync interval for auto-fetched pairs that do not have a per-pair override | Options: 1h, 3h, 6h, 12h, 24h | ENT-currency-conversion-settings.global_default_sync_frequency |
| Rate Protection Threshold | number | Yes | Alert if any pair's rate differs from its rate 24 hours earlier by more than this percentage | Range: 1-50%, decimal precision: 0.1% | ENT-currency-conversion-settings.rate_protection_threshold |

**Business Rules (Global Settings)**:

- Global Default Markup % is used as fallback when a currency pair does not specify its own markup percentage
- Global Default Sync Frequency is used as fallback when an auto-fetched pair does not specify its own sync interval
- Rate Protection Threshold applies to all auto-fetched pairs; system monitors each pair independently and flags those exceeding the threshold. The comparison base is the rate 24 hours earlier; after an admin acknowledges a warning it is the rate at the acknowledgement until the change against the rate 24 hours earlier is again within the threshold, and no comparison runs for 24 hours after a pair is created or switched between manual and auto-fetch mode
- Rate protection alerts do not automatically stop payments; they surface visual cues and send admin notifications (REQ-029-082)
- Any currency with no pair in this module results in the system collecting payment in USD, converted at the quote-to-USD rate in the rate set locked at quote acceptance, with the markup per Payment Rule 3

#### Section 2: Rate Sources

**Purpose**: Manage the list of external API providers used to auto-fetch exchange rates. Each source bundles its provider type with API credentials.

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Source Name | text | Yes | Admin-friendly label for this source (e.g., "xe.com — Production") | Max 100 chars, must be unique | ENT-rate-source.source_name (REQ-029-131) |
| Provider Type | select | Yes | API provider | Options: xe.com, fixer.io (extensible) | ENT-rate-source.provider_type |
| API Key | text | Yes | API key / credentials for this provider | Non-empty; masked after save (show last 4 chars) | ENT-rate-source.api_key_encrypted |
| Status | display-only | N/A | Connection health indicator | Auto-populated: green (healthy), yellow (degraded), red (down/error) | ENT-rate-source.status |
| Last Tested | display-only | N/A | Timestamp of last successful connection test | Auto-populated by system | ENT-rate-source.last_tested_timestamp |

**Actions**:

- **Add Source**: Opens inline form / modal to create a new source. Requires all fields above. System runs a test connection upon save; source is only persisted if the test succeeds.
- **Edit Source**: Admin can update source name, API key. System re-runs test connection on save. (REQ-029-078)
- **Delete Source**: Admin can delete a source only if no currency pairs reference it. If pairs reference the source, system displays warning listing affected pairs and requires admin to reassign or switch those pairs to manual before deletion.
- **Test Connection**: Available per source at any time. Calls the provider API, updates Status and Last Tested. (REQ-029-079)

**Business Rules (Rate Sources)**:

- API credentials are encrypted at rest (AES-256) and never logged in plain text (mask all but last 4 characters) (REQ-029-080)
- A source cannot be saved without passing a test connection first
- Deleting a source that is referenced by existing pairs is blocked; admin must reassign or convert affected pairs to manual mode first. This is the graceful deletion pattern. (REQ-029-091)
- System periodically checks source health during scheduled syncs and updates the Status indicator. If a source becomes unhealthy, all pairs using that source display a visual warning badge (yellow/red) on the pair list. (REQ-029-081)

#### Section 3: Currency Pair List

**Purpose**: Table listing all configured currency pairs with their current mode, rate, source, markup, and status.

| Column | Description | Graph field |
|--------|-------------|-------------|
| Pair | Always displayed as USD/{Target} (e.g., USD/EUR, USD/GBP). All pairs use USD as base. | ENT-currency-pair.target_currency |
| Mode | "Auto" or "Manual" — indicates how the base rate is determined | ENT-currency-pair.rate_mode |
| Source | Name of the rate source (if auto-fetched); "—" if manual | ENT-currency-pair.source_id |
| Base Rate | The raw exchange rate (fetched from API or manually entered) | ENT-currency-pair.current_base_rate |
| Markup % | Per-pair markup percentage; shows "(global)" suffix if using the global default | ENT-currency-pair.markup_percentage_override |
| Effective Rate | Calculated: Base Rate × (1 + Markup %). This is the rate applied to patient-facing prices. | ENT-currency-pair.current_effective_rate |
| Sync Frequency | Per-pair sync interval; shows "(global)" suffix if using the global default (auto-fetch pairs only) | ENT-currency-pair.sync_frequency_override |
| Last Updated | Timestamp of last rate update (auto-sync or manual save) | ENT-currency-pair.last_updated_timestamp |
| Status | Visual indicator: green checkmark (healthy), yellow warning (rate protection threshold breached or source degraded), red error (source down / fetch failed) | ENT-currency-pair.status |

**Actions on List**:

- **Add Pair**: Navigates to Screen 2B (Add/Edit Currency Pair) to create a new pair
- **Edit Pair**: Click row or edit icon to navigate to Screen 2B pre-populated with pair data
- **Delete Pair**: Remove a currency pair. System warns: "Deleting this pair means payments involving {Target} currency will fall back to USD. Continue?" Requires confirmation. (REQ-029-086)
- **Sync Now (per pair)**: For auto-fetched pairs, triggers an immediate rate fetch outside the scheduled sync (REQ-029-089)

**Business Rules (Pair List)**:

- All pairs MUST use USD as the base currency. Admin selects only the target currency when adding a pair. (REQ-029-085)
- Currency pairs must reference currencies that are enabled in the Currency Management screen (Screen 6) (REQ-029-083)
- A booking's locked rate survives deletion of its pair: deleting a pair affects only bookings that have no locked rate yet
- A price shown in a currency that is neither the quote currency nor USD is derived via USD, with the markup applied once, on the pair for the shown currency. Installment eligibility (minimum booking amount) uses the base rate without markup
- If a pair is deleted or not configured for a target currency, the system collects payment in USD for transactions involving that currency, converted at the quote-to-USD rate in the rate set locked at quote acceptance, with the markup per Payment Rule 3. A note on this screen states: "Currency pairs not listed here will default to USD for payment collection."
- Each pair independently tracks its own status. A source failure affects only pairs using that source; manual pairs are unaffected. (REQ-029-088)
- Status badges update automatically: green when last fetch succeeded and rate change is within threshold; yellow when the last sync breached the rate protection threshold or the source is degraded; red when last fetch failed or source is down. A yellow rate-protection badge clears only when an admin clicks "Acknowledge" on the pair; a later normal sync does not clear it, and after the acknowledgement the badge returns only if the rate moves above the threshold from the acknowledged rate. A yellow badge caused by a degraded source clears when the source is healthy again. (REQ-029-087)

**Notes**:

- Display a prominent info banner: "Any currency not configured here will default to USD for payment. Configure all currencies your patients may use."
- Provide sorting/filtering on the pair list: by pair name, mode, status, last updated
- Display total pair count and counts by mode (e.g., "12 pairs: 9 auto, 3 manual")
- Show alert badge count in the tab/section header if any pair has yellow/red status

---

### Screen 2B: Add / Edit Currency Pair

**Purpose**: Form to create a new currency pair or edit an existing one. Controls the pair's rate mode (auto-fetch or manual), source assignment, markup, and sync frequency.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Base Currency | display-only | N/A | Always "USD" — not editable | Fixed: USD | ENT-currency-pair.base_currency |
| Target Currency | select | Yes | The target currency for this pair (e.g., EUR, GBP, TRY) | Must be an enabled currency from Currency Management (Screen 6); cannot duplicate an existing pair | ENT-currency-pair.target_currency |
| Rate Mode | radio | Yes | How the base rate is determined | Options: "Auto-fetch from source" or "Manual input" | ENT-currency-pair.rate_mode |
| Source | select | Conditional | Which rate source to use for auto-fetching | Required if Rate Mode = Auto-fetch. Populated from sources configured in Screen 2A Section 2. | ENT-currency-pair.source_id |
| Manual Base Rate | number | Conditional | The admin-entered base exchange rate (how many units of target currency per 1 USD) | Required if Rate Mode = Manual. Must be > 0, decimal precision: 6 digits. | ENT-currency-pair.manual_base_rate (REQ-029-136) |
| Markup % | number | No | Per-pair markup percentage override. If left blank, the global default markup % from Screen 2A is used. | Range: 0-20%, decimal precision: 0.01%. Leave blank to inherit global default. | ENT-currency-pair.markup_percentage_override |
| Sync Frequency | select | No | Per-pair sync frequency override. If left blank, the global default sync frequency from Screen 2A is used. Only applicable for auto-fetch mode. | Options: 1h, 3h, 6h, 12h, 24h. Leave blank to inherit global default. Ignored if Rate Mode = Manual. | ENT-currency-pair.sync_frequency_override |
| Effective Rate | display-only | N/A | Calculated preview: Base Rate × (1 + Markup %) | Auto-calculated in real-time as admin edits Base Rate or Markup % | ENT-currency-pair.current_effective_rate |

**Actions**:

- **Test Connection & Fetch Rate** (auto-fetch mode only): Calls the selected source API for this specific pair. If successful, populates the Base Rate field with the fetched value and shows success confirmation with the fetched rate and effective rate preview. This action is **mandatory before saving** a new auto-fetch pair.
- **Save**: Validates all fields, persists the pair configuration, and returns to Screen 2A. For auto-fetch pairs, the first scheduled sync is calculated from the save timestamp (e.g., if saved at 12:36 with 6h interval, next sync at 18:36).
- **Acknowledge** (shown only while the pair has a rate-protection warning): the admin confirms having reviewed the rate change. This is the only way to clear the yellow rate-protection badge. The system logs the admin ID and timestamp, and compares the pair with the rate at that moment afterwards (Screen 2A rules)
- **Cancel**: Discards changes and returns to Screen 2A.

**Business Rules (Add/Edit Pair)**:

- All pairs use USD as the base currency (non-negotiable, enforced by UI)
- Target currency dropdown is populated from enabled currencies in the Currency Management screen (Screen 6); cannot create a pair for a disabled currency
- Cannot create a duplicate pair (one pair per target currency; USD/EUR can only exist once) (REQ-029-084)
- **Auto-fetch mode**:
  - Admin must select a source from the configured sources in Screen 2A Section 2
  - Admin **must run "Test Connection & Fetch Rate" before saving** to verify the source can provide a rate for this pair. Save button is disabled until test succeeds.
  - After the initial save, the system schedules recurring syncs. The schedule is calculated from the time the pair is saved: if saved at 12:36 with a 6-hour interval, the next sync runs at 18:36, then 00:36, etc.
  - If a scheduled fetch fails, the system keeps the last successfully fetched rate, marks the pair status as red/error on the list, and sends an alert notification to the admin
  - A source assigned to this pair cannot be deleted while the pair references it. To remove the source, the admin first reassigns the pair to another source or converts it to manual mode, which pre-fills the last fetched rate as the manual base rate. No pair switches to manual mode automatically.
- **Manual mode**:
  - Admin enters the base rate directly in the Manual Base Rate field (REQ-029-092)
  - No sync schedule is created; rate only changes when admin manually edits and saves (REQ-029-092)
  - Source field is hidden / not applicable
  - Sync Frequency field is hidden / not applicable
- **Switching modes on an existing pair**:
  - Auto → Manual: System pre-fills Manual Base Rate with the last fetched rate so admin doesn't start from zero. Sync schedule is removed. (REQ-029-093)
  - Manual → Auto: System requires admin to select a source and run "Test Connection & Fetch Rate" before saving. The fetched rate replaces the manual rate. (REQ-029-093)
- **Markup % inheritance**: If Markup % is left blank, the pair uses the Global Default Markup % from Screen 2A. If specified, the per-pair value overrides the global default. The Effective Rate preview always shows the actual markup being applied (whether inherited or overridden).
- **Sync Frequency inheritance**: If Sync Frequency is left blank (auto-fetch mode), the pair uses the Global Default Sync Frequency. If specified, the per-pair value overrides. Display "(using global default: Xh)" hint text when blank.
- The Effective Rate preview updates in real-time as admin changes Base Rate or Markup %, giving immediate visibility into the patient-facing rate. (REQ-029-094)
- The rate protection warning compares the pair's current rate with its rate 24 hours earlier, against the Rate Protection Threshold on Screen 2A. It clears only when an admin acknowledges it; changing the markup does not clear it. After the acknowledgement the badge returns only if the rate moves above the threshold from the acknowledged rate

**Notes**:

- Show inline help text: "Base Rate = how many {Target} per 1 USD. Example: 0.92 means 1 USD = 0.92 EUR."
- For auto-fetch pairs, show the source's current status indicator (green/yellow/red) next to the source dropdown
- Show estimated conversion rate impact: "5% markup on 0.92 USD/EUR = 0.966 effective rate"
- Display last sync timestamp and next scheduled sync time (for auto-fetch pairs) below the form (ENT-currency-pair.last_updated_timestamp, ENT-currency-pair.next_sync_timestamp)
- When editing an existing pair, show a "Rate History" link/section displaying rate changes over the last 30 days (chart + table) (REQ-029-099)

---

### Screen 3: Deposit Rate Configuration

**Purpose**: Allows admins to configure deposit percentage for bookings, either globally or per provider

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Configuration Scope | radio | Yes | Global Default or Provider-Specific | Must select one option | ENT-deposit-rate-config.scope |
| Global Deposit Rate | number | Conditional | Default deposit percentage for all providers | Range: 20-30%, decimal precision: 0.1%, required if scope is Global | ENT-deposit-rate-config.deposit_percentage |
| Provider Search | search | Conditional | Search for provider by name or ID | Required if scope is Provider-Specific | no graph field (control) |
| Selected Providers | list | Conditional | List of providers for custom deposit rate | Required if scope is Provider-Specific | ENT-deposit-rate-config.provider_id |
| Provider Deposit Rate | number | Conditional | Custom deposit percentage for selected providers | Range: 20-30%, decimal precision: 0.1%, required if scope is Provider-Specific | ENT-deposit-rate-config.deposit_percentage |
| Effective Date | display-only | N/A | Shows when this rate takes effect (immediately for new bookings) | Auto-populated: current timestamp | ENT-deposit-rate-config.effective_date |
| Affected Bookings | display-only | N/A | Shows booking count that will use this rate (estimates based on historical data) | Auto-calculated by system | ENT-deposit-rate-config.affected_bookings_estimate |

**Business Rules**:

- Deposit rate must be between 20% and 30% (business rule enforced by system validation)
- Deposit rate changes apply to new bookings only (existing bookings retain original deposit rate)
- Provider-specific rates override global default rate for selected providers
- Admin can set multiple provider-specific rates (different rates for different providers)
- System calculates deposit amount by multiplying booking total by deposit rate percentage
- Deposit rate configuration propagates to Payment Processing Service within 5 minutes (cache TTL)
- A provider-specific rate is removed by the admin action "Reset to global default" (Alternative Flow A2b): the provider then follows the global rate for new bookings, and existing bookings keep their own rate (General Module Rule 1)

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

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Enable Split Payments | toggle | Yes | Master switch to enable or disable split payment feature globally | Boolean (enabled = feature active) | ENT-split-payment-config.feature_enabled |
| Available Installments | checkbox-group | Yes | Select which installment options to offer (2, 3, 4, 5, 6, 7, 8, 9) | Must select at least one if feature enabled | ENT-split-payment-config.available_installments |
| Cutoff Days | number | Yes | Days before the procedure date by which the last installment must be due. The first installment is due on the booking day and the next ones every 30 days, so a plan of n installments needs at least cutoff + 30 x (n - 1) days between booking and procedure | Range: 30-90 days, integer only; when the Unpaid Balance Cancellation Point is set it must stay smaller than this value | ENT-split-payment-config.cutoff_days |
| Minimum Booking Amount | number | Yes | Minimum booking total required to qualify for installments (in USD) | Range: $100-$10,000, integer only | ENT-split-payment-config.minimum_booking_amount |
| Installment Frequency | display-only | N/A | Payment schedule frequency | Fixed: Monthly (30-day intervals) | ENT-split-payment-config.installment_frequency |
| Late Payment Grace Period | number | Yes | Days counted from the installment due date. The late fee is charged once, when the grace period has passed with the installment still unpaid and the automatic retries have ended. Starts at 0 days | Range: 0-14 days, integer only | ENT-split-payment-config.late_payment_grace_period_days |

**Business Rules**:

- Cutoff days is the date by which the last installment is due (default: 30 days before the procedure). Retries, the grace period and a pause by the support-required marker run from each due date and can carry an unpaid payment past the cutoff; the Unpaid Balance Cancellation Point (Screen 7) decides when an unpaid booking is cancelled, and a support-required pause stops that count (the marker is owned by FR-007B)
- The installment minimum lead time is cutoff + 30 days: below it no installment option is offered. Screen 4 always shows this figure, and the maximum count for a booking is floor((days before procedure - cutoff) / 30) + 1; the schedule itself is owned by FR-007B
- System automatically calculates available installment options based on booking date and procedure date
- If time between booking and procedure is insufficient for an installment count given the cutoff, that count is not offered; if even 2 installments do not fit, the patient sees the other payment options only (REQ-029-109)
- Installment amount calculation is always equal-split: booking total ÷ installment count (rounded to each currency's own minor units; last installment absorbs rounding difference)
- Minimum booking amount prevents installments for low-value bookings (reduces administrative overhead); it is stated in USD, and a booking total in another currency is converted to USD with the quote-to-USD base rate in the rate set locked at FR-005 subquote acceptance before the comparison
- The late payment fee set on Screen 7 is charged once, at the later of the end of the grace period (counted from the due date) and the end of the automatic retries; with a grace period of 0 it still waits for the retries. It is collected with the next successful charge and stays outside the clinic share and the refund base, and no fee is charged while the late payment fee is Not set (Screen 7). The preview shows the day it falls due, taking the day the last automatic retry runs from FR-007B (REQ-007B-018); after a hard decline there are no retries, so the fee falls on the end of the grace period. When the cancellation point (Screen 7) is smaller than that day, a booking is cancelled before the fee is charged and the fee never applies; Screens 4 and 7 warn about this on save and do not block it (REQ-029-157)
- A missed payment is cancelled by the Unpaid Balance Cancellation Point on Screen 7, which wins over pending retries and the Defaulted state; it does nothing while it is not set
- This is one global configuration: there are no tiers, and no separate installment plan by booking amount or by region
- Split payment configuration propagates to Payment Processing Service within 5 minutes (cache TTL)
- Cannot modify split payment rules for bookings with active installment plans (changes apply to new bookings only)
- System enforces a minimum 30-day cutoff before procedure date (per system booking/payment rules); admins may increase the cutoff up to 90 days (REQ-029-108)

**Notes**:

- Display preview calculator, computed from the schedule rule above: "For $3,000 booking with 5 installments, 30-day cutoff, booking 210 days before procedure:"
  - 5 installments: $600.00 each, due 210, 180, 150, 120 and 90 days before the procedure
  - The most this booking could use is 7 installments (floor((210 - 30) / 30) + 1), the last due 30 days before the procedure; choosing 5 leaves the last payment 90 days out
  - At 35 days before the procedure with a 30-day cutoff, no installment option is offered (minimum lead time 60 days)
- Show example scenarios for different booking amounts and installment options
- Provide "Preview Installment Schedule" button that generates detailed payment schedule
- Display the minimum lead time (cutoff + 30 days) at all times, and a warning when the cutoff is above 60 days: "Only bookings made [cutoff + 30] or more days before the procedure can use installments"
- Show statistics: "In last 30 days, 42% of bookings used installment plans (avg: 3.8 installments)"

---

### Screen 5: Commission Rate Configuration

**Purpose**: Allows admins to configure central commission settings: a platform global default plus provider-specific commission scopes used in billing, reconciliation, and provider payout calculations. FR-015 remains the synchronized single-provider edit surface for the same provider-specific commission data.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Global Commission Rate | number | Yes | Default commission percentage applied platform-wide when no provider-specific commission configuration exists for a provider | Range: 15-25%, decimal precision: 0.1% | ENT-commission-rate-config.commission_percentage |
| Global Last Updated | display-only | N/A | Shows when the global default was last changed | Auto-populated timestamp | ENT-commission-rate-config.updated_date |
| Selected Providers | async multi-select / chips | Yes | Provider list covered by a provider-specific commission scope | Minimum 1 provider with status Active or Suspended (Deactivated providers cannot be selected; FR-015 Tab 7 applies the same rule); a provider already in another active provider-specific scope cannot be selected (it must first be removed from that scope) | ENT-commission-rate-config.provider_ids |
| Commission Model | radio | Yes | Provider-specific commission model for the selected provider scope: "Percentage" or "Flat Rate" (same models as FR-015 Tab 7) | Default: Percentage | ENT-commission-rate-config.commission_model |
| Provider Commission Value | number | Yes | Percentage model: commission percentage of the booking total. Flat Rate model: fixed amount deducted once per completed procedure | Percentage: 0-100%, decimal precision: 0.1%. Flat Rate: amount > 0, precision per the currency's minor units (Screen 6) | ENT-commission-rate-config.commission_percentage, ENT-commission-rate-config.flat_rate_amount |
| Flat Rate Currency | select | Conditional | Currency of the Flat Rate amount; shown only when Commission Model = Flat Rate | Required for Flat Rate; must be an enabled currency from Screen 6; defaults to the system default currency | ENT-commission-rate-config.flat_rate_currency (REQ-029-137) |
| Effective Date | date | Yes | Date when the provider-specific scope becomes active for new bookings | Today or future date | ENT-commission-rate-config.effective_date (REQ-029-138) |
| Scope Status | badge | Yes | State of the provider-specific commission scope | Active / Archived | ENT-commission-rate-config.status |
| Actions | menu | Yes | Scope-level actions | Edit, Archive | no graph field (control) |

**Business Rules**:

- Commission changes apply to new bookings only (existing bookings retain the commission model and value snapshot captured at FR-006 booking confirmation)
- Provider-specific commission scopes take precedence over the global default at booking confirmation (REQ-029-113)
- FR-029 Screen 5 is the central commission-settings screen; FR-015 / A-02 Tab 7 remains a synchronized single-provider edit surface for the same provider-specific commission data
- Changes made in FR-015 to a provider-specific commission model or value MUST be reflected in Screen 5 for that provider, and changes made in Screen 5 MUST be reflected in FR-015
- A provider-specific commission scope may cover one or multiple providers and may be archived when no longer needed (REQ-029-114)
- **One active scope per provider**: A provider belongs to at most one active provider-specific commission scope, so the effective configuration at booking confirmation is never ambiguous.
- **Single-provider edit from FR-015**: When an admin edits commission in FR-015 Tab 7 for a provider covered by a scope shared with other providers, the system removes that provider from the shared scope and creates a single-provider scope for it with the new values; the shared scope and its other providers are unchanged. The split is audit-logged with before/after state. (REQ-029-115)
- **Scheduled configuration**: Each provider has at most one pending future-dated configuration. Saving another future-dated configuration for the same provider replaces the pending one (logged); on its Effective Date the pending configuration becomes the active one automatically. Screen 5 and FR-015 Tab 7 show the same pending configuration, which FR-032 Screen 4 displays read-only to the provider. (REQ-029-116)
- The global default is percentage-only; the Flat Rate model is available for provider-specific scopes only (REQ-029-121)
- **Percentage model** (global default or provider scope): commission amount = booking total (the accepted subquote price after promotion, in the quote currency, from the acceptance snapshot) × snapshotted commission percentage (rounded to the quote currency's own minor units; last payment absorbs rounding difference if needed) (REQ-029-118)
- **Flat Rate model** (provider scope only): commission amount = the snapshotted fixed amount, deducted once per completed procedure (FR-010 completion milestone), regardless of procedure price; it is not charged per package, per Subquote, or per installment (REQ-029-119)
- Flat Rate amounts are stored and snapshotted in their configured currency; this screen introduces no new currency conversion rule, and any conversion follows the existing FR-029 currency configuration and downstream FR-017 reconciliation handling (REQ-029-120)
- Commission configuration propagates to Payment Processing Service within 5 minutes (cache TTL)
- All commission configuration changes (model, value, currency, providers, effective date, status) must be logged to audit trail with before/after state

**Notes**:

- Display preview calculation per model: Percentage — "For $2,000 booking, 20% commission = $400"; Flat Rate — "$200 per completed procedure, regardless of booking total"
- Provide "Add new provider scope", "Edit", and "Archive" actions matching the admin commission-screen design
- Use FR-029 for global and bulk provider-scope updates; use FR-015 when the admin is already working inside a single provider profile

---

### Screen 6: Currency Management (Central Supported Currency List)

**Purpose**: Allows admins to manage the *enabled* subset of currencies used throughout the platform (e.g., currency dropdowns for location pricing, Stripe account supported currencies, and currency conversion configuration). The master currency catalog (ISO 4217 code metadata such as symbol and minor units) is maintained by engineering; admins do not create arbitrary new currency codes.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Search | text | No | Filter currencies by code or name | Max 100 chars | no graph field (control) |
| Currency Code | display-only | - | ISO 4217 code (e.g., USD, EUR, GBP) | From master catalog | ENT-currency.code |
| Currency Name | display-only | - | Human-readable currency name | From master catalog | ENT-currency.name |
| Symbol | display-only | - | Currency symbol (e.g., $, €, £) | From master catalog | ENT-currency.symbol |
| Minor Units | display-only | - | Decimal precision (e.g., 2 for USD/EUR/GBP, 0 for JPY/KRW) | From master catalog | ENT-currency.minor_units |
| Enabled | toggle | Yes | Whether this currency is available for selection across the system | Must keep at least 1 enabled currency; cannot be turned off while quotes, bookings, or instalment plans still use the currency, while it is the Default Currency of an active Stripe account, or while it is the Fee Currency of fixed fee amounts stored on Screen 7 (see Business Rules) | ENT-currency.enabled |
| Default Currency | radio/select | Yes | Which enabled currency is the system default | Exactly 1 default; default must be enabled | ENT-currency.is_default |

**Business Rules**:

- Currency codes are immutable and come from a system-maintained catalog; admins cannot add non-ISO or custom codes. (REQ-029-122)
- At least one currency must remain enabled at all times. (REQ-029-123)
- Exactly one enabled currency must be set as the system default. (REQ-029-123)
- If an admin attempts to disable a currency referenced only by configuration items (e.g., used in Stripe account supported currencies, location starting prices, or active pricing configs), the system MUST warn and provide a safe resolution path (e.g., update dependent configs first) before allowing the disable. A currency still used by quotes, bookings or instalment plans is not a warning case: it is blocked by the rule below. (REQ-029-124)
- Enabling/disabling currencies affects new configuration choices immediately; existing records retain their stored currency codes. (REQ-029-125)
- Disabling a currency is blocked while any sent quote that is not yet in a terminal state, any accepted booking that is not yet paid, or any open booking or instalment plan uses that currency. The admin sees the count of records still using it, and can disable the currency only when that count reaches zero.
- Disabling a currency is also blocked while it is the Default Currency of an active Stripe account (Screen 1); the admin sees the account name and changes the account first
- Disabling a currency is also blocked while it is the Fee Currency of fixed fee amounts stored on Screen 7; the admin re-enters those amounts in another currency first
- Changing the Default Currency does not reinterpret the fixed fee amounts stored on Screen 7: they stay in their own Fee Currency until an admin re-enters each of them in the new currency, and Screen 7 cannot be saved before that, which a banner on Screen 7 asks for
- Changing the Default Currency creates a new FR-026 Quote Configuration version, so the configuration version recorded on a quote identifies both the quote hours and the currency used. Quotes already sent keep the currency copied onto them at first send.
- When the Default Currency changes, open quote drafts keep the numbers the provider typed and switch to the new currency without conversion. Before the provider can send such a draft, the quote screen (owned by FR-004) shows a "currency changed, check your prices" banner that the provider must acknowledge.

**Notes**:

- This screen is the source of truth for currency dropdowns across Admin/Provider/Patient experiences (where applicable). (REQ-029-126)
- FR-017 Screen 1 ("Financial Reporting - Revenue Dashboard") initializes its reporting currency selector from this system default currency; the MVP seed value is USD unless an admin changes it later. (REQ-029-126)
- Provide quick actions: “Enable common set” (e.g., USD/EUR/GBP) and “Set Default” for an enabled currency.

---

### Screen 7: Refund, Fees and Settlement Settings

**Purpose**: Allows admins to set the platform's refund ladder, the late payment fee, the rescheduling fee, the balance due days and the unpaid balance cancellation point, Hairline's share of a patient cancellation fee, the fixed deduction applied to a clinic that cancels, the patient confirmation window and the weekly settlement days for manually paid clinics in one place. These are one global record, not set per provider, per region or per currency. FR-006, FR-007, FR-007B, FR-015 and FR-017 read this record; the late payment grace period stays on Screen 4. The admin steps are in the main flow "Configure Refund, Fees and Settlement".

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Refund Ladder | band table | Yes | Refund percentage by how many days before the procedure date the booking is cancelled. Launch default: more than 30 days, 90 percent; 15 to 30 days, 50 percent; under 15 days, 0 percent. Locked at booking confirmation | Percentage 0-100 per band; every number of days before the procedure date falls in exactly one band | ENT-refund-fee-settings.refund_ladder |
| Late Payment Fee Type | radio | No | How the late payment fee is calculated: fixed amount or percentage. Not set until a value is set; required once a value is set | Fixed amount / Percentage | ENT-refund-fee-settings.late_payment_fee_type |
| Late Payment Fee Value | number | No | Value of the late payment fee, charged once when the late payment grace period (Screen 4, counted from the due date) has passed unpaid and the automatic retries have ended; collected with the next successful charge and kept outside the clinic share and the refund base. Starts as Not set; while it is not set no late fee is charged. Locked at booking confirmation, a fixed amount together with its currency code; a booking confirmed while it is not set keeps no late fee | Blank (Not set), or a fixed amount above 0 stated in the Fee Currency (precision per its minor units, converted via USD with the rate set locked at quote acceptance when the patient pays in another currency), or a percentage above 0 and up to 100 of the late installment | ENT-refund-fee-settings.late_payment_fee_value |
| Rescheduling Fee Type | radio | No | How the fee for rescheduling a booking is calculated: fixed amount or percentage. Not set until a value is set; required once a value is set | Fixed amount / Percentage | ENT-refund-fee-settings.rescheduling_fee_type |
| Rescheduling Fee Value | number | No | Value of the rescheduling fee. Starts as Not set; while it is not set no rescheduling fee is charged. Locked at booking confirmation, a fixed amount together with its currency code; a booking confirmed while it is not set keeps no rescheduling fee. The fee never applies to a change an admin makes in V1 (FR-006) | Blank (Not set), or a fixed amount above 0 stated in the Fee Currency (precision per its minor units, converted via USD with the rate set locked at quote acceptance), or a percentage above 0 and up to 100; the amount a percentage applies to is decided together with patient-side rescheduling | ENT-refund-fee-settings.rescheduling_fee_value |
| Fee Currency | display-only | N/A | The currency in which the fixed late payment fee, the fixed rescheduling fee and the clinic cancellation deduction are stated. It is set to the system default currency when the first fixed amount is saved, and every stored fixed amount keeps its own currency code from then on | After a Default Currency change it moves to the new default only in a save in which every fixed amount that is set has been re-entered in the new currency; until then Screen 7 cannot be saved and the stored amounts keep the old currency. A currency in use as the Fee Currency cannot be disabled on Screen 6 | ENT-refund-fee-settings.fee_currency |
| Balance Due Days | number | Yes | For the deposit-now, balance-later option (FR-007): how many days before the procedure date the balance is due. Default: 7 days. A booking confirmed with this many days left, or fewer, gets full payment only. Locked at booking confirmation: FR-007 stores the balance due date on the booking then, so a later change never moves it | Whole number, 1 to 30 days | ENT-refund-fee-settings.deposit_plan_balance_due_days |
| Unpaid Balance Cancellation Point | number | No | Days after the oldest unpaid due date (the due date of the oldest installment or balance that is unpaid right now; paying it late restarts the count from the next unpaid one) at which a booking that still has an unpaid balance is cancelled for non-payment (FR-006 Boundary). It applies to any unpaid balance, whether the deposit and balance option or installments, and only to bookings confirmed after it is set. Locked at booking confirmation. It wins over pending retries and the Defaulted state. A separate setting from the balance due date; "Not set" is allowed, has no default, and while it is not set nothing is cancelled for non-payment | Blank (Not set) or a whole number of days, 1 to 30; must be smaller than Balance Due Days and smaller than the installment cutoff (Screen 4); a save that breaks either check is refused | ENT-refund-fee-settings.unpaid_balance_cancellation_point |
| Hairline Share of Patient Cancellation Fee | number | No | The percentage of a patient cancellation fee kept by Hairline; the rest goes to the clinic (FR-007 REQ-007-092). "Not set" is allowed and has no starting value; while it is not set Hairline keeps the whole fee and holders of the Screen 7 permission see a banner on the admin dashboard asking them to set it, which clears when the share is saved. Applies on the day of the cancellation | Blank (Not set) or a percentage 0-100 | ENT-refund-fee-settings.hairline_cancellation_fee_share |
| Clinic Cancellation Deduction | number | No | The fixed amount deducted from a clinic's next payout when the clinic cancels a booking (FR-017 Release Rule). It is stated in the Fee Currency and has no starting value; while it is not set no deduction is applied. Applies on the day of the cancellation | Blank (Not set) or a fixed amount above 0, precision per the Fee Currency minor units | ENT-refund-fee-settings.clinic_cancellation_deduction |
| Patient Confirmation Window | number | Yes | Days after a clinic marks a procedure complete during which the patient may raise a problem before the clinic share is released (FR-007 Fund Release & Money Routing Rules). Default: 7 days. Applies on the day of the event | Whole number of days, 1 to 30 | ENT-refund-fee-settings.patient_confirmation_window_days |
| Settlement Period | display-only | N/A | The one settlement period that applies to all manually paid clinics (manual bank transfer rail). Weekly only in V1, because FR-017 runs a weekly cycle | Fixed: weekly; no per-clinic value exists | ENT-refund-fee-settings.settlement_period |
| Settlement Cutoff Day | selection | Yes | The day the settlement period closes. Default: Sunday | Day of the week; must differ from the Settlement Payout Day | ENT-refund-fee-settings.settlement_cutoff_day |
| Settlement Payout Day | selection | Yes | The day the settlement statement is paid out. Default: Wednesday | Day of the week; must differ from the Settlement Cutoff Day | ENT-refund-fee-settings.settlement_payout_day |
| Last Updated | display-only | N/A | When the record was last saved and by which admin | Auto-populated | ENT-refund-fee-settings.updated_date |

**Business Rules**:

- Lock points: the refund ladder, the rescheduling fee, the late payment fee (a fixed amount together with its currency code; Not set stays Not set), the grace period, the balance due days (kept as a balance due date stored on the booking), the unpaid balance cancellation point and the installment cutoff lock at booking confirmation and a booking keeps them (General Module Rule 1). Hairline's share, the clinic cancellation deduction and the patient confirmation window are read on the day the event happens, so a change reaches bookings that are already confirmed. The settlement days apply from the next settlement run
- Hairline keeps the late payment fee and the rescheduling fee; neither changes a provider payout. The rescheduling fee never applies to a change an admin makes in V1 (FR-006)
- The settlement period is one setting for all manually paid clinics: there is no per-clinic payout frequency. On the Stripe Connect rail release to the clinic is automatic, so the settlement period does not apply. FR-015 and FR-017 point to this setting; affiliate payouts are a separate matter owned by FR-018
- The settlement period is weekly only in V1; an admin can edit the cutoff day and the payout day, and the two must differ. The patient confirmation window is 1 to 30 days
- The balance of the deposit-now, balance-later option is due 7 days before the procedure date by default, within 1 to 30 days; an admin can edit it. The unpaid balance cancellation point is its own setting, 1 to 30 days after the oldest unpaid due date, smaller than the balance due days and the installment cutoff, with no default. Screen 7 refuses a save that breaks either comparison
- Hairline's share of a patient cancellation fee and the cancellation point may be "Not set"; saving does not require them. While the share is not set Hairline keeps the whole fee and holders of the Screen 7 permission see a dashboard banner that clears when the share is saved; while the cancellation point is not set nothing is cancelled for non-payment
- The late payment fee and the rescheduling fee start as "Not set", and no such fee is charged while it is not set; the grace period (Screen 4) starts at 0 days. A fixed fee amount must be above 0 and is stored and locked together with its currency code. After a Default Currency change, a save must carry every fixed amount that is set (the two fees and the clinic cancellation deduction) re-entered in the new currency; until then the stored amounts keep their old currency and Screen 7 cannot be saved
- The clinic cancellation deduction is a fixed amount in the Fee Currency with no starting value; FR-017 reads it, and no deduction is made while it is not set
- Every save is logged to the audit trail with before/after state
- Configuration propagates to Payment Processing Service within 5 minutes (cache TTL)

**Notes**:

- Show a preview of the ladder with an example booking total so the admin sees the refund amount for each band
- The base amount the refund percentage is applied to is not defined here (see the Refund Rule)

---

## Business Rules

### General Module Rules

- **Rule 1**: Payment configuration changes never alter a value that has already been locked. Each configuration is locked at a named point: (a) the currency conversion rate set (base rates and markups, each with its timestamp) is locked when the patient accepts a subquote in FR-005 and is stored in the acceptance snapshot (Currency Rule 2); (b) the effective commission configuration, the deposit rate, and the split payment (installment) settings are locked at FR-006 booking confirmation and stored with the booking; (c) no payment configuration is frozen when a parent quote or subquote is created or sent in FR-004; (d) the refund ladder, the rescheduling fee, the late payment fee (a fixed amount together with its currency code; Not set stays Not set), the late payment grace period, the balance due days (kept as a balance due date stored on the booking), the unpaid balance cancellation point and the installment cutoff are locked at FR-006 booking confirmation, while Hairline's share of a patient cancellation fee, the clinic cancellation deduction and the patient confirmation window are read on the day the event happens and are not locked; (e) the Stripe account that takes a booking's first payment is stored with the booking and used for every later charge and refund of that booking; (f) a locked rate set survives the deletion of any of its currency pairs. Before its lock point, a quote or accepted-but-unconfirmed subquote follows the configuration that is effective at that moment, and an active installment plan keeps the settings locked at its booking confirmation. When FR-019 expresses a fixed-amount promotion in the quote currency at quote send, it uses the currency conversion rate (including markup) in effect at send; this sets the promotion amount on the quote only and does not lock the conversion rate for payment, which stays locked at acceptance under (a). (REQ-029-101)
- **Rule 2**: All payment configuration changes must be logged to audit trail with admin ID, timestamp, and change details for compliance
- **Rule 3**: Configuration cache propagates to Payment Processing Service within 5 minutes maximum (cache TTL)
- **Rule 4**: System must gracefully handle payment processing when configuration data is unavailable (use last known good configuration) (REQ-029-102)
- **Rule 5**: Admin cannot delete a Stripe account that an open booking or an active installment plan still uses; the account is set to Archived instead (Screen 1). Deposit rates are edited or reset to the global default, never deleted, and the single split payment record is edited, so this rule does not apply to them

### Data & Privacy Rules

- **Privacy Rule 1**: Stripe API secret keys and webhook secrets must be encrypted at rest using AES-256 encryption
- **Privacy Rule 2**: Stripe secret keys must never be logged in plain text to audit logs or error logs (mask all but last 4 characters)
- **Privacy Rule 3**: Admin access to payment configuration must require elevated permissions (not available to standard admin users)
- **Privacy Rule 4**: Moved to the system PRD. See system PRD, Platform-Wide Rules: No card numbers stored (includes webhook signature verification) (REQ-SYS-005)
- **Audit Rule**: All payment configuration changes must be logged with before/after state for audit compliance
- **Compliance Rule**: See system PRD, Platform-Wide Rules: No card numbers stored (PCI DSS compliance through the payment processor) (REQ-SYS-005)
- **Data Retention**: Payment configuration audit history is kept; retention follows the system PRD, Platform-Wide Rules: One 10-year retention period (REQ-SYS-002)

### Admin Editability Rules

**Editable by Admin**:

- Stripe account credentials, assigned countries, supported currencies, and Active, Inactive or Archived status
- Central supported currency list (enable/disable currencies) and system default currency
- Rate sources (add/edit/delete with provider type and API credentials)
- Currency pairs (add/edit/delete; per-pair rate mode, source assignment, manual base rate, markup % override, sync frequency override)
- Global currency conversion defaults (global markup %, global sync frequency, rate protection threshold)
- Deposit rate percentage (20-30% range) globally or per provider, and a provider-specific rate can be reset to the global default
- Commission global default percentage (15-25% range)
- Provider-specific commission model and value: Percentage (0-100%) or Flat Rate (fixed amount > 0 per completed procedure, in an enabled currency)
- Split payment available installment options (2-9), cutoff days (30-90), minimum booking amount ($100-$10,000)
- Late payment grace period for split payments (0-14 days, starting at 0)
- Rate protection alert threshold (global) for currency conversion monitoring
- Refund ladder (refund percentage by days before the procedure date; default 90, 50 and 0 percent), late payment fee and rescheduling fee (each a fixed amount or a percentage, plus the value; both start as Not set), all on Screen 7
- Enabled payment methods per region and currency (Screen 1)
- Balance due days for the deposit-now, balance-later option (1 to 30, default 7), the unpaid balance cancellation point (1 to 30 days after the oldest unpaid due date, may be Not set), Hairline's share of a patient cancellation fee (may be Not set), the clinic cancellation deduction (fixed amount, may be Not set), the patient confirmation window (1 to 30 days, default 7), and the settlement cutoff day and payout day for manually paid clinics (weekly only; default Sunday cutoff, Wednesday payout), all on Screen 7

**Fixed in Codebase (Not Editable)**:

- Deposit rate allowed range (20-30% hard-coded business rule) (REQ-029-112)
- Split payment installment range (2-9 installments hard-coded limit) (REQ-029-112)
- Cutoff days allowed range (30-90 days hard-coded limits) (REQ-029-112)
- Installment frequency (monthly; 30-day intervals) (REQ-029-112)
- Encryption algorithms for Stripe secret keys (AES-256)
- Cache TTL for configuration propagation (5 minutes hard-coded)
- Payment audit logging requirements (always enabled, cannot be disabled) (REQ-029-112)
- Currency master catalog (ISO 4217 metadata: name/symbol/minor units) used to populate the Currency Management screen

**Configurable with Restrictions**:

- Global and per-pair markup percentage for currency conversion (range: 0-20%, requires validation)
- Global and per-pair sync frequency for auto-fetch currency pairs (options: 1h, 3h, 6h, 12h, 24h)
- Rate protection threshold (range: 1-50%, requires validation); alerts always active for auto-fetch pairs
- Minimum booking amount for split payments (range: $100-$10,000 in USD, requires validation; compared in USD per the Minimum Booking Conversion Rule)

### Payment & Billing Rules

- **Payment Rule 1**: Payment Processing Service routes transactions to the appropriate Stripe account based on the country on the patient's profile (not the patient's current physical location); the account chosen for a booking's first payment stays with that booking for every later charge and refund (REQ-029-004)
- **Payment Rule 2**: If patient's country has no assigned Stripe account, system uses the Stripe account marked as Global Fallback (if configured) or blocks payment. Routing considers Live-mode accounts only on a production deployment and Test-mode accounts only elsewhere; a country held by an Inactive or Archived account counts as unassigned; when the mapped account fails authentication, new bookings use the Global Fallback. If the routed account does not support the booking currency, the charge is made in USD at the quote-to-USD rate in the booking's locked rate set, with the markup (Payment Rule 3), and payment methods are checked against the charge currency
- **Payment Rule 3**: Currency conversion markup applies to all transactions involving currency conversion, including the USD fallback charge (protects against bank rate differences). A price shown in a currency that is neither the quote currency nor USD is derived via USD with the markup applied once, on the pair for the shown currency (REQ-029-103)
- **Booking Total Rule**: Throughout this FR, "booking total" means the accepted subquote price after any promotion, in the quote currency, read from the FR-005 acceptance snapshot. The same rule applies to every discount type, including discounts funded only by Hairline: commission is always calculated on the price after promotion. It is never recomputed from the live quote, option, or date-range price. This single figure is the base for the Percentage commission, the deposit amount, and the installment split; any display or charge in another currency uses the rate set locked under Currency Rule 2. (REQ-029-100)
- **Payment Rule 4**: Deposit amount calculated by multiplying booking total by configured deposit rate percentage (rounded to each currency's own minor units)
- **Payment Rule 5**: Installment payment schedules are owned by FR-007B and calculated from booking date, procedure date, cutoff days and the selected installment count: the first installment is due on the booking day, then one falls due every 30 days, and the last is due on or before the cutoff
- **Settlement Period Rule**: There is no per-clinic payout frequency. On the manual bank transfer rail, one settlement setting owned by FR-029 applies to all manually paid clinics: the period is weekly only in V1, with an admin-editable cutoff day (default Sunday) and payout day (default Wednesday) that must differ; on the Stripe Connect rail release is automatic. FR-015 and FR-017 point to this setting
- **Payment Rule 6**: A missed installment is followed by reminders and automatic payment retries (timing owned by FR-007B); when the retries have failed, an admin is flagged to follow up. The late payment fee is charged once, after the grace period and the retries have ended (Late Fee Rule). A booking whose balance is still unpaid at the unpaid balance cancellation point (Screen 7, counted in days after the oldest unpaid due date) is cancelled: this wins over pending retries and the Defaulted state, covers any unpaid balance (deposit and balance, or installments), applies only to bookings confirmed after the point was set, and does nothing while the point is not set (REQ-029-105)
- **Billing Rule 1**: Installments are equal-split: booking total ÷ installment count (rounded to each currency's own minor units; last installment absorbs rounding difference)
- **Currency Rule 1**: Prices always displayed to patients in their selected currency using admin-configured conversion rates with markup; a price in a currency that is neither the quote currency nor USD goes via USD with the markup applied once (REQ-029-104)
- **Currency Rule 2**: The currency conversion rate set MUST be locked at FR-005 subquote acceptance and stored in that acceptance snapshot, then copied to the booking and its transactions. Every pair is against USD, so the set holds, for the quote currency, for the currency shown to the patient and for the Fee Currency (Screen 7), the base rate and the markup, each with its timestamp. Every later conversion reads this set and nothing else: displays and deposit, installment and final payments in the shown currency (base rate with markup), the USD charge (Payment Rule 2), the installment eligibility check (base rate only, Minimum Booking Conversion Rule), and fixed fees stated in the Fee Currency (via USD, Payment Rule 3). There is no rate fluctuation after subquote acceptance. The parent quote never owns a locked rate. If a cached rate is older than 24 hours, acceptance still proceeds. The locked set stays valid after any of its currency pairs is deleted or changed.
- **Commission Rule**: The effective commission configuration (global default or provider-specific) MUST be resolved at FR-006 booking confirmation and its model (Percentage or Flat Rate), value, currency (Flat Rate), source configuration ID, and scope type (global or provider-specific) stored per booking/transaction for payout and reconciliation consistency; a Flat Rate snapshot is deducted once at the FR-010 completed-procedure milestone, not per package, Subquote, or installment. The Percentage model applies to the booking total defined in the Booking Total Rule. An accepted-but-unpaid subquote has not yet fixed its commission, so a configuration that becomes effective before booking confirmation applies to it.
- **Indicative Commission Rule**: Any commission shown before booking confirmation, including the FR-004 quote screen, is indicative only. It shows the model and value (percentage or flat amount) from the configuration effective at the time of display, labelled "indicative, final at booking confirmation". Only the booking-confirmation snapshot is authoritative for payout, invoicing, and reconciliation.
- **Refund Rule**: Refunds on a cancelled booking follow the refund ladder set on Screen 7 and locked at booking confirmation: the refund percentage depends on how many days before the procedure date the booking is cancelled. The launch default is more than 30 days, 90 percent; 15 to 30 days, 50 percent; under 15 days, 0 percent. It is one global setting that FR-006, FR-007, FR-007B and FR-017 read; each provider's own cancellation terms do not replace it (REQ-029-110)
- **Minimum Booking Conversion Rule**: The Minimum Booking Amount for installments is stated in USD. A booking total in another currency is converted to USD with the quote-to-USD base rate in the rate set locked at FR-005 subquote acceptance (Currency Rule 2) before it is compared with the minimum. The conversion uses the base rate without markup, so the markup never shifts who qualifies
- **Late Fee Rule**: The late payment fee set on Screen 7 is charged once, when the late payment grace period (counted from the due date) has passed with the installment unpaid and the automatic retries have ended; it is collected with the next successful charge and stays outside the clinic share and the refund base. No fee is charged while the late payment fee is Not set, or when the booking is cancelled at the cancellation point first. A fixed fee stated in the Fee Currency converts via USD with the rate set locked at quote acceptance (Currency Rule 2, Payment Rule 3); a percentage fee is a percentage of the late installment. Hairline keeps the late payment fee and the rescheduling fee; neither changes a provider payout. The rescheduling fee never applies to a change an admin makes in V1

### Failure Handling and Operational Rules

- **Failure handling**: If Stripe API unavailable, queue payment transactions for retry with exponential backoff, notify admin of Stripe outage (REQ-029-076)
- **Failure handling**: If email service unavailable, log notification failures and display in-app notification to admin, retry with queue (REQ-029-128)
- **Error handling**: If Configuration API unavailable, use last cached configuration and alert admin, retry with exponential backoff (REQ-029-102)
- **Secret rotation**: Support for Stripe API key rotation without downtime (configure new keys, test, then deactivate old keys) (REQ-029-077)
- **Encryption**: Stripe secret keys and webhook secrets encrypted at rest using AES-256, decrypted only in memory during API calls
- **Concurrency**: See system PRD, Platform-Wide Rules: Concurrent admin edits: warn, then last save wins (REQ-SYS-012)
- **Threat mitigation**: See system PRD, Platform-Wide Rules: Admin API rate limit (REQ-SYS-008)
- S-02 also owns locale-aware number formatting (decimal separator, symbol position, digit grouping, and RTL currency rendering) as a shared service capability consumed by FR-021. (REQ-021-053)
- **Integration point**: Payment Configuration queries regional groupings to map Stripe accounts to countries/regions; FR-028 enforces one-country-to-one-grouping, so Stripe account mapping must respect that uniqueness (conflicts resolved via override)
- **Integration point**: Booking service queries Payment Configuration API for deposit rate, effective commission configuration, and split payment rules; provider-specific commission may be authored in FR-029 Screen 5 or FR-015 Tab 7, but the booking flow resolves a single effective record before storing the booking-time commission snapshot
- **Integration point**: Payment Configuration uses provider IDs for provider-specific deposit assignment and provider-specific commission scopes; FR-015 provides the single-provider commission edit surface, payout destination details are managed in FR-032, and payout execution is handled in FR-017

**Carried from dropped sections (original wording)**:

- **Integration 2**: Payment Processing Service queries Payment Configuration API for transaction routing and calculation rules
- **Authentication**: Internal service authentication using API keys or mutual TLS
- **Entity 3 - Deposit Rate Configuration**:
- **Relationships**: One global deposit rate; many provider-specific deposit rate overrides (one per provider); many bookings reference deposit rate configuration
- **Entity 7 - Currency Exchange Rate**:
- **Relationships**: Rates are recorded by date and currency pair. FR-029 owns this entity (moved in from FR-014); FR-014 reads the daily rates and does not define the entity.

---

## Dependencies

Related FRs: FR-001, FR-004, FR-005, FR-006, FR-007, FR-007B, FR-015, FR-017, FR-021, FR-028, FR-032.

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
   - 3 installments: $666.67 each (rounded; last installment absorbs rounding difference); for a booking made 90 days before the procedure they are due 90, 60 and 30 days before the procedure
   - The last installment is due on or before the cutoff date
6. **Given** patient has active installment plan, **When** patient misses second installment payment deadline, **Then** system sends reminders and retries the payment; the late payment fee is charged once after the grace period (counted from the due date) and the retries have ended, and is collected with the next successful charge; an admin is flagged to follow up after the retries
7. **Given** the unpaid balance cancellation point is set before the booking was confirmed, **When** the oldest unpaid installment is still unpaid that many days after its due date, **Then** the booking is cancelled, even if retries are pending; if the cancellation point is not set, nothing is cancelled for non-payment

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
3. **Given** I click on the USD/EUR pair to edit (Screen 2B) and decide to increase markup, **When** I update USD/EUR per-pair markup from blank (global 5%) to 7% and click "Save", **Then** system applies new 7% markup to this pair, recalculates effective rate, and logs admin action to audit trail; the yellow badge stays
4. **Given** markup is updated for USD/EUR, **When** next patient views price in EUR, **Then** price reflects new 7% per-pair markup instead of previous 5% global default
5. **Given** rate protection alert was triggered, **When** I view the pair's "Rate History" section in Screen 2B, **Then** chart shows rate spike and timestamp when alert was sent
6. **Given** the yellow rate-protection badge is showing on USD/EUR, **When** I click "Acknowledge" on the pair, **Then** the badge clears and the acknowledgement is logged with my admin ID and timestamp; a later sync brings the badge back only if the rate has moved above the threshold from the rate at my acknowledgement

### User Story 6 - Commission Resolution at Booking Confirmation (Priority: P2)

As a platform administrator managing provider commission, I need the commission for each booking to be resolved once, at booking confirmation, from the configuration effective at that moment and applied to the accepted price after promotion, so that payouts and reconciliation never depend on when a quote was created or what the quote screen showed.

**Why this priority**: Commission drives provider payouts and platform revenue. Without one named lock point and one base, two implementations can charge different amounts for the same booking.

**Independent Test**: Can be fully tested by accepting a subquote, scheduling a provider-specific scope change that becomes effective before payment, completing the first payment, and checking the booking snapshot's model, value, base, source configuration ID, and scope type.

**Acceptance Scenarios**:

1. **Given** a provider is on the 20% global default and a provider-specific 18% scope is scheduled to become effective on Day 7, **When** the patient accepts a subquote on Day 6 and booking confirmation happens on Day 8, **Then** the booking snapshot stores 18% with the provider-specific scope's configuration ID and scope type, and the quote screen had shown 20% labelled "indicative, final at booking confirmation".
2. **Given** a provider's scope switches from Percentage to Flat Rate after a subquote is accepted but before booking confirmation, **When** booking confirmation happens, **Then** the booking snapshot stores the Flat Rate model, amount, and currency, and the commission is deducted once at the FR-010 completed-procedure milestone.
3. **Given** an accepted subquote reaches Payment Window Expired and an admin later revives the booking through FR-006, **When** the revived booking is confirmed, **Then** commission, deposit rate, and split payment settings are resolved from the configuration effective at that confirmation, and so are the Screen 7 values that lock at confirmation (refund ladder, rescheduling fee, late payment fee, grace period, balance due days, unpaid balance cancellation point and installment cutoff; the cancellation point applies only if it was set before that confirmation), and the currency conversion rate set stays the one locked in the original acceptance snapshot, because a revive keeps the original acceptance unchanged. If the patient instead starts a new inquiry, that inquiry's own acceptance locks its own rate. (REQ-029-130)
4. **Given** an accepted subquote of $3,000 with a $300 promotion in the quote currency and a 20% Percentage commission, **When** booking confirmation happens, **Then** the commission is $540 (20% of the $2,700 booking total), and the deposit and installments use the same $2,700 base.
5. **Given** a provider is covered by a shared provider-specific scope, **When** an admin edits that provider's commission in FR-015 Tab 7 before a pending booking is confirmed, **Then** the provider moves to its own single-provider scope and the booking snapshot records that new scope's configuration ID.

---

### Edge Cases

- What happens when admin attempts to delete a Stripe account that an open booking or active installment plan still uses? **System prevents deletion and displays error: "Cannot delete a Stripe account that open bookings still use. Set it to Archived instead."** An Archived account takes no new bookings, stays hidden from the default list, and keeps serving charges and refunds of the bookings that already use it; it can be deleted once no open booking or active installment plan uses it.

- How does system handle a rate source being completely unavailable for 24+ hours? **For each auto-fetch pair using the affected source: system continues using the pair's last successfully cached rate, marks the pair's status as red/error on the pair list (Screen 2A), and marks the source's status as red in the Sources section.** System sends daily email digest to admin summarizing the source outage and listing all affected pairs. When the source recovers, the next scheduled sync for each affected pair fetches the latest rate and restores green status. Admin can also switch affected pairs to a different source or manual mode at any time during the outage. (REQ-029-098)

- What occurs if admin configures a high cutoff (e.g., 90 days)? **Screen 4 shows the minimum lead time at all times (cutoff + 30 days, here 120 days) and, because the cutoff is above 60 days, displays warning: "With a cutoff of [90 days], only bookings made [120] or more days before the procedure can use installments."** Admin can choose to proceed or adjust to a lower value (e.g., 30 days). System logs warning to admin activity log. (REQ-029-129)

- How to manage patient attempting payment from country with no assigned Stripe account and no Global Fallback configured? **System checks the country on the patient's profile, finds no Stripe account assigned, checks for Global Fallback, finds none. System displays error to patient: "Payment processing not available for your location. Please contact support."** System sends urgent alert to admin: "Payment blocked for [Country]: No Stripe account configured. Expand regional coverage." at most once per country per day. A patient with no country on the profile is asked to add one first, with no alert. Payment attempt logged to admin dashboard for follow-up. (REQ-029-074)

- What happens when a patient books 35 days before the procedure with a 30-day cutoff enabled? **The installment schedule starts on the booking day and then falls due every 30 days, so 2 installments need at least 60 days (cutoff + 30) and none fits at 35 days.** No installment option is offered; the patient sees the other payment options (pay in full now, or deposit now and balance later) and no message offers installments. The same booking would be offered installments only from 60 days out (2 installments), 90 days (3), and so on. (REQ-029-106)

- How does system handle rapid currency fluctuation exceeding rate protection threshold multiple times in single day for one pair (e.g., USD/EUR changes 3% at 8am, another 3% at 2pm, another 3% at 8pm)? **System compares each sync with the pair's rate 24 hours earlier. It sends the first alert at 8am when the 3% threshold is crossed and marks the pair's status as yellow/warning on the pair list. System applies rate-limiting to alerts (maximum one alert per currency pair per 6 hours) to prevent alert fatigue, and sends the second alert at 2pm showing the change against the rate 24 hours earlier: "USD/EUR changed 6% in 24 hours."** The yellow badge stays until an admin clicks Acknowledge; a later normal sync does not clear it. After the acknowledgement the pair is compared with the rate at that moment until the 24-hour change is again within the threshold. Admin receives summary of all rate changes across all pairs in daily digest email. (REQ-029-097)

- What occurs if admin configures two different Stripe accounts for overlapping countries (e.g., Account A for US/Canada/Mexico, Account B for US/UK)? **System detects country overlap (US) during configuration and displays warning: "US is already assigned to Account A. Override assignment?"** Admin selects: "Override" (US moves to Account B, no longer uses Account A) or "Cancel" (keep current assignment). System logs conflict resolution to audit trail. If admin overrides, system uses most recently configured account for overlapping country (Account B for US in this example) for new bookings; a booking already taken on Account A keeps Account A for its later charges and refunds. An override that would leave Account A with no countries (and no Global Fallback flag) is blocked.

- How to manage admin accidentally entering incorrect Stripe secret key that initially validates but later fails during actual payment processing? **During configuration, system validates Stripe credentials by making test API call to Stripe. If credentials are syntactically correct but have insufficient permissions or are later revoked by Stripe, first payment attempt will fail. Payment Processing Service logs error: "Stripe authentication failed for account [name]."** System sends urgent alert to admin: "Stripe account [name] failed authentication. Verify API keys are active and have required permissions."** System temporarily routes new bookings to Global Fallback (if configured) and displays error banner to admin; a booking already taken on the failing account keeps that account and its charges are retried once the keys are fixed. Routing returns to the account when its next Test Connection passes; if the failing account is the Global Fallback itself, or no fallback exists, payment is blocked with the Boundary Flow B6 error and alert. (REQ-029-075)

---

## Functional Requirements Summary

### Core Requirements

- **REQ-029-001**: System MUST allow admins to add, edit, and manage multiple Stripe accounts with API credentials (publishable key, secret key, webhook secret)
- **REQ-029-002**: System MUST allow admins to assign Stripe accounts to specific countries or regional groupings (multi-select assignment)
- **REQ-029-003**: System MUST validate Stripe API credentials by testing connection to Stripe API before activating account
- **REQ-029-004**: System MUST route payment transactions to appropriate Stripe account based on the country on the patient's profile, and a booking MUST keep the account that took its first payment for every later charge and refund
- **REQ-029-004b**: System MUST support an optional Stripe account marked as Global Fallback used when no country/regional grouping mapping exists, or when the mapped account fails authentication (at most 1 Global Fallback account) (REQ-029-055)
- **REQ-029-005**: System MUST support multiple currencies per Stripe account and allow admins to configure supported currencies
- **REQ-029-006**: System MUST allow admins to manage rate sources (add, edit, delete) where each source bundles a provider type (xe.com, fixer.io) with its API credentials. Source creation requires a successful test connection before saving. Source deletion is blocked if currency pairs reference it; admin must reassign or convert affected pairs first.
- **REQ-029-006b**: System MUST allow admins to create and manage currency pairs (CRUD), where each pair has USD as the mandatory base currency and a configurable rate mode: auto-fetch (from a configured source) or manual input (admin-entered base rate). (REQ-029-056)
- **REQ-029-007**: System MUST allow admins to set a global default markup percentage (0-20% range) and optionally override it per currency pair (0-20% range). If a pair has no per-pair markup, the global default applies.
- **REQ-029-007b**: System MUST allow admins to set a global default sync frequency (1h, 3h, 6h, 12h, 24h) and optionally override it per auto-fetch currency pair. If an auto-fetch pair has no per-pair sync frequency, the global default applies. Each pair's sync schedule is calculated from the time it was saved (e.g., saved at 12:36 with 6h interval → next sync at 18:36). (REQ-029-057)
- **REQ-029-008**: System MUST fetch currency conversion rates automatically for each auto-fetch pair on its configured sync schedule (per-pair or inherited global frequency). Manual-mode pairs are not synced.
- **REQ-029-009**: System MUST calculate and display the effective rate for each pair as: Base Rate × (1 + Markup %). This effective rate is applied to patient-facing prices.
- **REQ-029-010**: System MUST allow admins to configure a global rate protection threshold (1-50% range). System monitors each auto-fetch pair independently and marks the pair's status as yellow/warning and sends an alert notification when the pair's rate differs from its rate 24 hours earlier by more than the threshold. The warning clears only when an admin acknowledges it. After an acknowledgement the pair is compared with the rate at that moment until the change against the rate 24 hours earlier is again within the threshold, and no comparison runs for 24 hours after a pair is created or switched between modes
- **REQ-029-011**: System MUST require a successful "Test Connection & Fetch Rate" action before saving any new auto-fetch currency pair. The Save button is disabled until this test succeeds.
- **REQ-029-011b**: For any currency not configured as a pair, the system MUST fall back to collecting payment in USD, converted at the quote-to-USD rate in the rate set locked at quote acceptance, with the markup per Payment Rule 3. The admin dashboard MUST display a note informing admins of this fallback behavior. (REQ-029-058)
- **REQ-029-012**: System MUST gracefully handle per-pair rate source failures by keeping the last successfully fetched rate, marking the pair's status as red/error on the pair list, and alerting admin. Deleting a rate source MUST be blocked while any pair still references it; the admin must first reassign those pairs to another source or convert them to manual mode (with the last fetched rate pre-filled), and no pair switches to manual mode automatically.
- **REQ-029-013**: System MUST allow admins to configure deposit rate percentage (20-30% range) globally for all providers
- **REQ-029-014**: System MUST allow admins to configure provider-specific deposit rates that override global default for selected providers
- **REQ-029-015**: System MUST apply deposit rate changes to new bookings only (existing bookings retain original deposit rate). Once a booking has been confirmed, its installment settings are locked: later changes to installment configuration never alter that booking
- **REQ-029-016**: System MUST calculate deposit amount by multiplying booking total by configured deposit rate percentage
- **REQ-029-017**: System MUST allow admins to enable or disable split payment (installment) feature globally
- **REQ-029-018**: System MUST allow admins to select available installment options (2-9 installments) via multi-select checkboxes
- **REQ-029-019**: System MUST allow admins to configure cutoff days (30-90 day range): the last installment is due on or before the cutoff date
- **REQ-029-020**: System MUST allow admins to configure minimum booking amount ($100-$10,000 range) required to qualify for installments
- **REQ-029-021**: System MUST automatically calculate available installment options based on booking date, procedure date, and cutoff days, with a minimum lead time of cutoff + 30 days, and MUST show the minimum lead time on the configuration screen
- **REQ-029-022**: System MUST generate installment payment schedules using equal-split amounts: booking total ÷ installment count (rounded to each currency's own minor units; last installment absorbs rounding difference)
- **REQ-029-023**: System MUST allow admins to configure the late payment grace period (0-14 days, starting at 0), counted from the installment due date. The late fee is charged once, after the grace period and the automatic retries have ended
- **REQ-029-043**: System MUST allow admins to configure both the platform commission global default (percentage only, allowed range 15-25%) and provider-specific commission scopes (Percentage model 0-100% or Flat Rate model with a fixed amount > 0 per completed procedure) in Screen 5; changes apply to new bookings only and existing bookings retain the commission snapshot captured at booking confirmation
- **REQ-029-043b**: System MUST keep provider-specific commission models and values synchronized between FR-029 Screen 5 and FR-015 Tab 7 because both screens are valid admin management surfaces for the same provider-specific commission data (REQ-029-059)
- **REQ-029-044**: System MUST lock currency conversion rates (including markup) at FR-005 subquote acceptance, store them with their timestamp in the acceptance snapshot, and copy them to the booking and its transactions (no rate fluctuation after subquote acceptance). If the cached rate is older than 24 hours, acceptance still proceeds and the snapshot records the rate and its timestamp
- **REQ-029-045**: System MUST snapshot the effective commission model and value (and Flat Rate currency), with the source configuration ID and scope type, at booking confirmation and store it per booking/transaction for payout and reconciliation consistency; Flat Rate snapshots are deducted once per completed procedure

### Data Requirements

- **REQ-029-024**: System MUST persist all payment configuration data (Stripe accounts, rate sources, currency pairs, global conversion settings, deposit rates, commission global default, provider-specific commission scopes, split payment rules) with full audit history
- **REQ-029-025**: System MUST log all payment configuration changes to audit trail with admin ID, timestamp, IP address, and before/after state
- **REQ-029-026**: System MUST cache payment configuration data with 5-minute TTL to minimize database queries during payment processing
- **REQ-029-027**: System MUST retain payment configuration audit history; retention follows the system PRD, Platform-Wide Rules: One 10-year retention period

### Security & Privacy Requirements

- **REQ-029-028**: System MUST encrypt Stripe API secret keys and webhook secrets at rest using AES-256 encryption
- **REQ-029-029**: System MUST never log Stripe secret keys in plain text to audit logs or error logs (mask all but last 4 characters)
- **REQ-029-030**: System MUST require elevated admin permissions ("PaymentConfigAdmin" role) to access payment configuration functionality
- **REQ-029-031**: Moved to the system PRD. See system PRD, Platform-Wide Rules: Encryption in transit and at rest; TLS 1.3 for connections to the Payment Configuration API is recorded once in the [system PRD](../../system-prd.md), which this module follows (REQ-SYS-004)
- **REQ-029-032**: Moved to the system PRD. See system PRD, Platform-Wide Rules: No card numbers stored; PCI DSS compliance for payment data handling is recorded once in the [system PRD](../../system-prd.md), which this module follows (REQ-SYS-005)
- **REQ-029-046**: Retired. Moved to the system PRD. See system PRD, Platform-Wide Rules: No card numbers stored (includes webhook signature verification), which this module follows (REQ-SYS-005)

### Integration Requirements

- **REQ-029-033**: System MUST provide RESTful API for Payment Processing Service to query payment configuration (Stripe accounts, currency pair effective rates, deposit rates, effective commission settings, installment rules)
- **REQ-029-034**: System MUST integrate with external currency conversion rate APIs (xe.com, fixer.io) via HTTP GET requests, using credentials stored per rate source
- **REQ-029-035**: System MUST send email notifications to admins for payment configuration changes and rate protection alerts
- **REQ-029-036**: System MUST propagate payment configuration changes to Payment Processing Service within 5 minutes maximum (cache TTL)

### Validation & Error Handling Requirements

- **REQ-029-037**: System MUST validate deposit rate percentage is within allowed range (20-30%) and display error if out of range
- **REQ-029-038**: System MUST validate markup percentage is within allowed range (0-20%) and display error if out of range
- **REQ-029-039**: System MUST validate cutoff days is within allowed range (30-90 days) and, when the unpaid balance cancellation point is set, that the cutoff stays larger than it; display an error if either check fails
- **REQ-029-040**: System MUST prevent deletion of a Stripe account that an open booking or active installment plan still uses (set it to Archived instead)
- **REQ-029-041**: System MUST prevent modification of deposit rates or split payment rules for bookings with active references (changes apply to new bookings only)
- **REQ-029-042**: System MUST always show the installment minimum lead time (cutoff + 30 days) on the split payment screen and display a warning when the cutoff is above 60 days
- **REQ-029-047**: System MUST validate commission values by model: global default and provider Percentage within allowed ranges (15-25% global, 0-100% provider) and provider Flat Rate amount greater than 0 with an enabled currency, displaying an error and rejecting the save otherwise (client-side and server-side)
- **REQ-029-048**: System MUST keep each provider in at most one active provider-specific commission scope with at most one pending future-dated configuration (a new one replaces it); an FR-015 Tab 7 edit to a provider in a shared scope MUST split that provider into its own single-provider scope without changing the other providers
- **REQ-029-049**: System MUST lock payment configuration only at its named lock points: the currency conversion rate set at FR-005 subquote acceptance; the commission configuration, deposit rate, split payment settings, refund ladder, rescheduling fee, late payment fee (a fixed amount with its currency code), grace period, balance due days (as a balance due date stored on the booking), unpaid balance cancellation point and installment cutoff at FR-006 booking confirmation; nothing at quote creation or sending. Hairline's share of a cancellation fee, the clinic cancellation deduction and the patient confirmation window apply on the day of the event
- **REQ-029-050**: System MUST calculate the Percentage commission, deposit amount, and installment split from the booking total, defined as the accepted subquote price after promotion, in the quote currency, read from the acceptance snapshot and never recomputed from the live quote
- **REQ-029-051**: System MUST present any pre-confirmation commission (including the FR-004 quote screen) as an indicative model and value labelled "indicative, final at booking confirmation"; only the booking-confirmation snapshot is authoritative. The binding commission is fixed at booking confirmation on the accepted price after promotion, in the quote currency, from the acceptance snapshot
- **REQ-029-052**: System MUST block disabling a currency while any non-terminal sent quote, unpaid accepted booking, or open booking or instalment plan uses it, or while it is the Default Currency of an active Stripe account, and MUST show the admin the count of records still using that currency (or the account name).
- **REQ-029-053**: System MUST create a new FR-026 Quote Configuration version whenever the Default Currency changes; open quote drafts MUST keep their typed numbers, switch to the new currency without conversion, and require the provider to acknowledge a banner reading "currency changed, check your prices" (FR-004 quote screen) before send.
- **REQ-029-054**: System MUST calculate commission on the accepted price after the promotion, in the quote currency and read from the acceptance snapshot, for every discount type, including discounts funded only by Hairline; no program keeps commission on the price before the promotion.
- **REQ-029-140**: System MUST compare the booking total with the Minimum Booking Amount for installments in USD: a booking total in another currency is converted to USD with the quote-to-USD base rate in the rate set locked at FR-005 subquote acceptance, without markup, before the comparison.
- **REQ-029-141**: System MUST allow admins to enable or disable the payment methods offered to patients, per region and currency (Screen 1); FR-007 reads this setting, and FR-007B owns the payment-method records.
- **REQ-029-142**: System MUST allow admins to edit the refund ladder (refund percentage by how many days before the procedure date the booking is cancelled) on Screen 7. The launch default is: more than 30 days, 90 percent; 15 to 30 days, 50 percent; under 15 days, 0 percent. The ladder is locked at booking confirmation. FR-006, FR-007, FR-007B and FR-017 read this setting.
- **REQ-029-143**: System MUST allow admins to set a late payment fee and a rescheduling fee on Screen 7. For each fee the admin chooses the type (fixed amount or percentage) and enters the value; both fees start as Not set, and no such fee is charged while it is not set. A fixed amount must be above 0, is stated in the Fee Currency and is converted via USD with the rate set locked at quote acceptance; the late fee percentage is of the late installment. Both fees are locked at booking confirmation (a fixed amount with its currency code; a booking confirmed while a fee is Not set keeps no such fee). Hairline keeps both fees; they change no provider payout. The rescheduling fee never applies to a change an admin makes in V1.
- **REQ-029-144**: System MUST charge the late payment fee once, when the late payment grace period (counted from the due date) has passed with the installment unpaid and the automatic retries have ended; it is collected with the next successful charge and stays outside the clinic share and the refund base. No fee is charged while the late payment fee is Not set.
- **REQ-029-145**: System MUST allow admins to set the settlement cutoff day and payout day for all manually paid clinics on Screen 7. The period is weekly only in V1, defaulting to a Sunday cutoff and a Wednesday payout; the two days must differ. There is no per-clinic payout frequency; on the Stripe Connect rail release is automatic. FR-015 and FR-017 point to this setting.
- **REQ-029-146**: System MUST treat the balance of the deposit-now, balance-later option as due 7 days before the procedure date by default, MUST allow admins to edit it on Screen 7 within 1 to 30 days, and MUST lock it at booking confirmation as a balance due date stored on the booking (FR-007), so a later change never moves it. A booking confirmed with this many days left, or fewer, gets full payment only.
- **REQ-029-147**: System MUST allow admins to set, on Screen 7, the unpaid balance cancellation point: 1 to 30 days after the oldest unpaid due date (the due date of the oldest installment or balance that is unpaid right now; paying it late restarts the count from the next unpaid one), at which a booking with any unpaid balance (deposit and balance, or installments) is cancelled. It applies only to bookings confirmed after it is set, wins over pending retries and the Defaulted state, and does nothing while it is not set. It must be smaller than the balance due days and smaller than the installment cutoff.
- **REQ-029-148**: System MUST allow admins to set Hairline's share of a patient cancellation fee on Screen 7. It has no starting value and may be Not set; while it is not set Hairline keeps the whole fee and holders of the Screen 7 permission see a banner on the admin dashboard asking them to set it, which clears when the share is saved.
- **REQ-029-149**: System MUST allow admins to set the patient confirmation window on Screen 7 (1 to 30 days, default 7).
- **REQ-029-150**: System MUST allow admins to set the clinic cancellation deduction on Screen 7: a fixed amount above 0 in the Fee Currency with no starting value, which FR-017 reads; no deduction is made while it is not set.
- **REQ-029-151**: System MUST refuse a Screen 7 save, naming the field, when balance due days are outside 1 to 30, when a set cancellation point is outside 1 to 30 or is not smaller than both the balance due days and the installment cutoff, when the confirmation window is outside 1 to 30, or when the settlement cutoff day and payout day are the same.
- **REQ-029-152**: System MUST consider only Live-mode Stripe accounts for routing on a production deployment and only Test-mode accounts elsewhere. The Global Fallback account MUST be Active and Live on production (Test elsewhere) and cannot be set Inactive or Archived. A country held by an Inactive or Archived account MUST be treated as unassigned for routing, and such an account may hold no countries. An override that would leave a non-fallback account with no countries MUST be refused at the confirmation step of Alternative Flow A1.
- **REQ-029-153**: System MUST charge a booking in USD when the routed Stripe account does not support the booking currency, converting at the quote-to-USD rate in the booking's locked rate set with the markup per Payment Rule 3, and MUST check the payment methods against the charge currency after that fallback.
- **REQ-029-154**: System MUST derive a price shown in a currency that is neither the quote currency nor USD via USD, applying the markup once on the pair for the shown currency, and MUST keep a booking's locked rate valid after its currency pair is deleted.
- **REQ-029-155**: System MUST let an admin acknowledge a pair's rate-protection warning on Screen 2B, log the acknowledgement, and clear the warning only by that action; afterwards the pair is compared with the rate at that moment until the change against the rate 24 hours earlier is again within the threshold.
- **REQ-029-156**: System MUST state each fixed fee amount on Screen 7 (late payment fee, rescheduling fee, clinic cancellation deduction) in the Fee Currency, store and lock it together with its currency code, and MUST NOT reinterpret it when the Default Currency changes: after a Default Currency change Screen 7 cannot be saved until each fixed amount that is set has been re-entered in the new currency, and a currency in use as the Fee Currency cannot be disabled.
- **REQ-029-157**: System MUST warn, without blocking the save, on Screen 4 and on Screen 7 when a set unpaid balance cancellation point is smaller than the day the late payment fee would be charged (the later of the end of the grace period and the day the last automatic retry runs, as set by FR-007B), because a booking cancelled at the point never pays the fee.
- **REQ-029-158**: System MUST let an admin remove a provider-specific deposit rate with the action "Reset to global default" on Screen 3, with a confirmation and an audit entry; the provider then follows the global rate for new bookings and existing bookings keep their own rate.

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-11-22 | 1.15 | Requirements graph programme baseline: PRD compressed to the checklist structure (dropped classes removed, field rows tagged with graph field ids, rule citations added). No rule changes. Earlier history (v1.0 to v1.14) and the four change requests (CR-FR029-20261014-01, CR-FR029-20261015-01, CR-FR029-20261015-02, CR-FR029-20261016-01; their files stay beside this PRD) are in `archived/prd-baseline-2026-11-08/fr029-payment-system-config/` and in git history. | Product Owner / Documentation |
| 2026-11-23 | 1.16 | Independent compression review: 6 clause(s) from dropped sections restored in original wording under Business Rules. No rule changes. | Product Owner / Documentation |
| 2026-11-23 | 1.17 | Logic review corrections. A missed installment is now cancelled by the unpaid balance cancellation point, and the late fee waits for the retries; the installment minimum lead time is cutoff + 30 days and the examples follow the 30-day schedule. Screen 7 gains ranges, "Not set" states, the clinic cancellation deduction, a fee currency and lock points, with an admin flow for Screens 6 and 7. Stripe routing keeps one account per booking, uses live accounts only and has an Archived status. Currency rules cover third-currency prices, unsupported account currencies and the rate protection Acknowledge action. | Product Owner / Documentation |
| 2026-11-23 | 1.18 | Second logic review corrections. Fixed fee amounts are re-entered when the default currency changes and are locked with their currency code; the late fee, the rescheduling fee and the grace period get starting values; balance due days lock at confirmation; the cancellation point counts from the oldest unpaid due date and is warned about when it falls before the late fee day. The rate set stored at quote acceptance is named and the USD fallback converts from it. Countries of Inactive or Archived accounts are treated as unassigned, the Global Fallback follows the deployment mode, and payment methods are checked against the charge currency. Provider-specific deposit rates are reset instead of deleted, and Acknowledge on a rate warning moves the comparison base. | Product Owner / Documentation |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner |  | 2025-12-16 | ✅ Approved |
| Technical Lead |  | 2025-12-16 | ✅ Approved |
| Stakeholder |  | 2025-12-16 | ✅ Approved |
| Product Owner | Joachim Trung Tuan | 2026-10-18 | Approved FR-029 v1.11 to v1.14 via MTG-002 decision log (documentation only), including CR-FR029-20261016-01 |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-029 from system-prd.md + Hairline-AdminPlatformPart2.txt transcription
**Last Updated**: 2026-11-23
