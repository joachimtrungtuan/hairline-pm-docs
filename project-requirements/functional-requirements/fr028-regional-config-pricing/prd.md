# FR-028 - Regional Configuration & Pricing

**Module**: A-09: System Settings & Configuration | P-02: Quote Request & Management | PR-02: Inquiry & Quote Management
**Feature Branch**: `fr028-regional-config-pricing`
**Created**: 2025-11-13
**Status**: ✅ Verified & Approved
**Source**: FR-028 from system-prd.md, Hairline-AdminPlatformPart2.txt transcription

---

## Executive Summary

The Regional Configuration & Pricing module enables Hairline administrators to control how treatment locations (countries/cities) are presented to patients and set starting price estimates for different regions and currencies. This foundational configuration system directly influences the patient's initial experience when browsing treatment destinations and helps set appropriate pricing expectations based on their location and currency.

### Purpose

This module provides the administrative infrastructure to:

1. **Define regional groupings** - Group countries into logical regions (e.g., "Eastern Europe", "Middle East", "UK only") for consistent presentation
2. **Configure location display order** - Control which treatment destinations appear first based on patient location (e.g., UK patients see Turkey first, then Poland, then UK)
3. **Set starting price estimates** - Configure baseline pricing per destination and currency to give patients realistic cost expectations before requesting quotes
4. **Support multi-currency pricing** - Allow different starting prices for the same destination based on patient's currency (GBP, EUR, USD, etc.)

### Business Value

- **Improved conversion rates** - Patients see most relevant destinations first, reducing decision fatigue
- **Regional optimization** - Tailor destination recommendations based on patient location, travel patterns, and market preferences
- **Pricing transparency** - Accurate starting price estimates reduce quote shock and improve quote acceptance rates
- **Operational flexibility** - Admins can quickly adjust pricing and location ordering as market conditions change
- **Multi-market support** - Enables expansion into new geographic markets with localized pricing

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-02)**: Consumes regional configuration to display location options and starting prices during quote request flow
- **Provider Platform (PR-02)**: Indirectly benefits from better-qualified inquiries due to accurate patient expectations
- **Admin Platform (A-09)**: Full configuration interface for managing regional groupings, location ordering, and starting prices
- **Shared Services**: None (configuration data served directly from database)

### Multi-Tenant Breakdown

**Patient Platform (P-02: Quote Request & Management)**:

- Displays list of treatment destinations filtered and ordered by patient location (REQ-028-036)
- Shows starting price estimates for each destination in patient's local currency (REQ-028-037)
- Uses regional configuration to personalize the destination selection experience
- No direct editing capabilities - purely consumption of admin-configured data (REQ-028-044)

**Provider Platform (PR-02: Inquiry & Quote Management)**:

- Indirectly benefits from regional configuration through improved inquiry quality
- Providers receive inquiries from patients with realistic pricing expectations
- No direct interaction with regional configuration settings (REQ-028-044)
- Quote submission pricing is provider-controlled, not constrained by starting prices (REQ-028-043)

**Admin Platform (A-09: System Settings & Configuration)**:

- Create and manage regional groupings (e.g., "Eastern Europe", "Middle East", "UK", "Germany Only") (REQ-028-026)
- Assign countries to regional groupings
- Define location presentation order per regional grouping (which destinations show first, second, third, etc.)
- Configure starting prices per destination per currency
- Set fallback pricing for locations without preset configurations
- Future phase: Enable/disable specific destinations for specific patient regions (REQ-028-045)
- Preview how configurations will appear to patients from different locations

**Shared Services**:

- None - this is pure configuration data stored in database and served via existing API infrastructure

### Communication Structure

**In Scope**:

- The admin who saves a regional grouping change or a starting price change receives a system notification that the save went through (REQ-028-046)
- Configuration changes propagate to patient-facing APIs within 1 minute (cache refresh) (REQ-028-005)

**Out of Scope**:

- Patient notifications about pricing changes (handled by general notification system) (REQ-028-047)
- Provider notifications about regional configuration updates (providers unaffected by these settings) (REQ-028-047)
- Real-time pricing updates based on exchange rates (covered by FR-029: Payment System Configuration) (REQ-028-047)

### Entry Points

**Admin Entry Point**:

- Admin navigates to Settings > General Settings and opens the Location Presentation by Country tab or the Location Pricing tab (Hairline app settings now live under General Settings) (REQ-028-049)
- Access requires admin role with "System Configuration" permissions (per FR-031)
- Configuration changes take effect immediately upon save (within 1-minute cache propagation)

**Patient Entry Point** (consumption only):

- Patient reaches "Choose Your Destination" screen during quote request flow (REQ-028-049)
- System automatically determines patient's location from profile or IP geolocation
- System applies appropriate regional configuration to filter and order destination list
- Starting prices are fetched and displayed in patient's preferred currency (REQ-028-038)

---

## Business Workflows

### Main Flow: Admin Configures Regional Location Presentation

**Actors**: Admin (System Settings Configuration Role)
**Trigger**: Admin wants to optimize location presentation for specific patient regions
**Outcome**: Regional grouping created with location ordering rules; changes visible to patients from target region within 1 minute

**Steps**:

1. Admin navigates to Settings > General Settings > Location Presentation by Country tab
2. Admin clicks "Add New Regional Grouping"
3. Admin enters grouping name (e.g., "Eastern Europe", "Middle East", "UK Only")
4. Admin selects countries that belong to this grouping from multi-select country list
   - System validates at least one country is selected
   - System blocks selection of countries that already exist in other groupings and displays error: "Each country can only belong to one regional grouping. Remove it from the other grouping first."
5. Admin defines location presentation order for this grouping:
   - Drags and drops destination countries into preferred order
   - First position = shown first to patients, second position = shown second, etc.
   - System displays preview of how patients from this region will see destinations
6. Admin enters change reason (required)
7. Admin saves regional grouping
8. System validates configuration completeness, including change reason (10-500 chars)
9. System saves configuration to database
10. System clears location presentation cache
11. System displays success confirmation: "Regional grouping saved. Changes will be live for patients within 1 minute."
12. System logs configuration change in audit trail (admin user, timestamp, change reason, change details)

### Alternative Flows

**A1: Admin Edits Existing Regional Grouping**:

- **Trigger**: Admin needs to update location ordering or country assignments for existing grouping
- **Steps**:
  1. Admin selects existing regional grouping from list
  2. System displays current configuration (countries, location order)
  3. Admin modifies countries or reorders destinations
  4. Admin enters change reason (required)
  5. Admin saves changes
  6. System validates, saves, clears cache, and confirms (same as main flow steps 8-12)
- **Outcome**: Regional grouping updated; patients from affected region see updated location ordering within 1 minute

**A2: Admin Deletes Regional Grouping**:

- **Trigger**: Admin needs to remove obsolete regional grouping
- **Steps**:
  1. Admin selects regional grouping to delete
  2. System displays warning: "Deleting this grouping will affect patients from [X countries]. They will fall back to proximity-based destination ordering. Continue?"
  3. Admin enters change reason (required) and confirms deletion
  4. System archives grouping (soft delete) and clears cache
  5. System displays confirmation: "Regional grouping archived. Patients from affected countries will now see proximity-based destination ordering."
- **Outcome**: Regional grouping archived; patients from affected countries fall back to proximity-based ordering

**B1: Admin Attempts to Save Regional Grouping Without Countries**:

- **Trigger**: Admin tries to save grouping with no countries selected
- **Steps**:
  1. Admin attempts to save
  2. System displays validation error: "At least one country must be selected for this regional grouping."
  3. Admin selects countries or cancels
- **Outcome**: Configuration not saved until validation passes

**B2: Admin Attempts to Save Regional Grouping Without Location Order**:

- **Trigger**: Admin tries to save grouping without defining destination order
- **Steps**:
  1. Admin attempts to save
  2. System displays validation error: "At least one destination must be ordered for this regional grouping."
  3. Admin adds destination ordering or cancels
- **Outcome**: Configuration not saved until validation passes

**B3: Admin Attempts to Save Without Change Reason**:

- **Trigger**: Admin attempts to save a regional grouping change without providing a change reason
- **Steps**:
  1. Admin attempts to save
  2. System displays validation error: "Change reason is required (10-500 characters)."
  3. Admin enters change reason or cancels
- **Outcome**: Configuration not saved until validation passes

---

### Main Flow: Admin Configures Starting Prices Per Location

**Actors**: Admin (System Settings Configuration Role)
**Trigger**: Admin wants to set or update starting price estimates for treatment destinations
**Outcome**: Starting prices configured for destination per currency; prices visible to patients within 1 minute of save

**Steps**:

1. Admin navigates to Settings > General Settings > Location Pricing tab
   - Currency dropdown is populated from FR-029's supported currency list (Settings > Billing Settings > Currency Management)
2. Admin selects destination location (e.g., Turkey, Poland, UK)
3. System displays current pricing configuration for selected location:
   - List of currencies with configured starting prices
   - Currencies without configured prices marked as "Not Set"
4. Admin clicks "Add Currency" or "Edit" for existing currency
5. Admin selects currency from dropdown (GBP, EUR, USD, TRY, etc.)
6. Admin enters starting price amount for selected destination-currency combination
   - System validates amount is positive number
   - System displays format guidance: "Enter base starting price (e.g., 2500 for £2,500)"
7. Admin enters change reason (required)
8. Admin saves currency-price configuration
9. System validates configuration:
   - Currency is supported (exists in system currency list)
   - Price is valid positive number
   - Decimal places appropriate for currency (2 for GBP/EUR/USD, 0 for JPY)
   - Change reason is present and within 10-500 chars
10. System saves pricing configuration to database
11. System displays success confirmation: "Starting price for [Location] in [Currency] set to [Amount]."
12. System logs pricing change in audit trail (admin user, timestamp, change reason, change details)

**Alternative Flows**:

**A3: Admin Sets Fallback Pricing for Region**:

- **Trigger**: Admin wants to provide default pricing for patients from a country that doesn't have preset pricing
- **Steps**:
  1. Admin navigates to Location Pricing > Fallback Pricing
  2. Admin selects destination location
  3. Admin enables fallback pricing option
  4. Admin selects the patient country the fallback price applies to
  5. Admin enters fallback price per currency
  6. Admin enters change reason (required)
  7. System saves fallback configuration
  8. System confirms: "Fallback pricing enabled for [Location]. Patients from [Country] without specific pricing will see these prices."
- **Outcome**: Fallback pricing active; the fallback price shown to a patient is the one set for the patient's country

**A4: Admin Bulk Updates Pricing Across Multiple Currencies**:

- **Trigger**: Admin needs to update pricing for all currencies proportionally (e.g., 10% increase across board)
- **Steps**:
  1. Admin selects destination location
  2. Admin clicks "Bulk Update Pricing"
  3. Admin selects update method (percentage increase/decrease or fixed amount adjustment)
  4. Admin enters adjustment value
  5. System displays preview of new prices for all currencies
  6. Admin enters change reason (required) and confirms or adjusts
  7. System saves all currency price updates simultaneously
  8. System confirms: "[X] currency prices updated for [Location]."
- **Outcome**: All currency prices for destination updated proportionally

**B4: Admin Attempts to Set Invalid Price**:

- **Trigger**: Admin enters non-numeric or negative value for price
- **Steps**:
  1. Admin attempts to save invalid price
  2. System displays validation error: "Starting price must be a positive number."
  3. Admin corrects value or cancels
- **Outcome**: Invalid pricing not saved

**B5: Admin Attempts to Set Price for Unsupported Currency**:

- **Trigger**: Admin selects currency not configured in system
- **Steps**:
  1. Admin attempts to save price for unsupported currency
  2. System displays error: "[Currency] is not currently supported. Add currency to system first via Currency Management."
  3. Admin navigates to Settings > Billing Settings > Currency Management (FR-029) or cancels
- **Outcome**: Price not saved for unsupported currency

**B6: Admin Attempts to Save Pricing Without Change Reason**:

- **Trigger**: Admin attempts to save a pricing change without providing a change reason
- **Steps**:
  1. Admin attempts to save
  2. System displays validation error: "Change reason is required (10-500 characters)."
  3. Admin enters change reason or cancels
- **Outcome**: Pricing not saved until validation passes

---

### Main Flow: Patient Views Personalized Location Recommendations

**Actors**: Patient, System
**Trigger**: Patient reaches "Choose Your Destination" screen during quote request flow
**Outcome**: Patient sees location list filtered and ordered by their regional grouping, with appropriate starting prices in their currency

**Steps**:

1. Patient navigates to "Choose Your Destination" screen
2. System retrieves patient's location from profile (stored during signup) or determines via IP geolocation if not set
3. System identifies patient's country
4. System queries regional groupings to find matching grouping for patient's country
5. System applies location presentation order from matched regional grouping
6. System filters destination list to show locations in configured order:
   - First location in regional config displayed first
   - Second location displayed second
   - Continue through configured order
   - Additional locations not in config appear at end ordered by proximity to patient location
7. For each displayed location, system fetches starting price:
   - System identifies patient's currency preference (from profile or location default)
   - System queries pricing configuration for [Location + Currency] combination
   - If specific pricing exists, display that price
   - If no specific pricing, display the fallback price for location chosen by the patient's country (if configured)
   - If no fallback, display the system-wide default starting price (if an admin has set one)
8. System displays destination list to patient with:
   - Location name and flag
   - Starting price in patient's currency: "Starting from £2,500"
   - Brief location description
   - Provider count available in location
9. Patient selects preferred destination(s) to proceed with quote request

**Alternative Flows**:

**A5: Patient's Location Not in Any Regional Grouping**:

- **Trigger**: Patient's country is not assigned to any regional grouping
- **Steps**:
  1. System detects no matching regional grouping
  2. System falls back to proximity-based location ordering (FR-003 default behavior)
  3. System displays all available destinations in default order
  4. Starting prices displayed using fallback pricing or system defaults
- **Outcome**: Patient sees all destinations in default order with appropriate pricing

**A6: Patient's Currency Not Configured for Selected Location**:

- **Trigger**: Patient views location that doesn't have pricing configured for their currency
- **Steps**:
  1. System detects missing currency-specific pricing
  2. System checks for fallback pricing for the patient's country
  3. If fallback exists, display fallback price
  4. If no fallback, display the system-wide default starting price (if an admin has set one)
  5. If there is no system-wide default, display price in location's default currency with conversion note: "Starting from €2,200 (approx. £2,500)"
  6. Conversion uses the admin-configured conversion rate with markup from FR-029
- **Outcome**: Patient sees estimated pricing with currency conversion note

---

## Screen Specifications

### Screen 1: Regional Grouping Management (Admin)

**Purpose**: Allow admins to create and manage regional groupings that control location presentation order for different patient regions

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Grouping Name | Text | Yes | Name of regional grouping (e.g., "Eastern Europe", "UK Only") | Max 100 chars, must be unique (REQ-028-025) | ENT-regional-grouping.grouping_name |
| Description | Text | No | Internal description of grouping purpose | Max 500 chars | ENT-regional-grouping.description |
| Countries | Multi-select | Yes | List of countries that belong to this grouping | At least 1 country must be selected (REQ-028-022) | ENT-regional-grouping.country_list |
| Location Order | Drag-and-drop list | Yes | Ordered list of destination locations to display | At least 1 location must be ordered (REQ-028-023) | ENT-regional-grouping.location_order |
| Locations Displayed | Number | No | How many destinations patients from this grouping see in the list | Whole number from 5 to 20; default 10 | no graph field (setting SET-locations-displayed-per-grouping) |
| Status | Toggle | Yes | Active/Inactive status | Active = applies to patients, Inactive = archived | ENT-regional-grouping.status |
| Change Reason | Text | Yes | Reason for grouping change (create/update/archive) | 10-500 chars | ENT-configuration-change-audit-log.change_reason |
| Created Date | Date (read-only) | - | When grouping was created | Auto-generated | ENT-regional-grouping.created_at |
| Last Modified | Date (read-only) | - | When grouping was last updated | Auto-updated on save | ENT-regional-grouping.updated_at |
| Modified By | Text (read-only) | - | Admin user who last modified | Auto-populated | ENT-regional-grouping.updated_by_admin_id |

**Business Rules**:

- **Unique Membership**: Each country can only belong to one regional grouping at a time. If admin attempts to add a country that already exists in another grouping, system blocks save and shows error with list of conflicting groupings. (REQ-028-006, REQ-028-021)
- **Default Fallback**: If no regional grouping matches, system orders destinations by proximity to patient location (FR-003 default behavior) (REQ-028-035)
- **Cache Propagation**: See REQ-028-005.
- **Audit Trail**: All changes logged with timestamp, admin user, and change details (added/removed countries, reordered locations) (REQ-028-011)
- **Soft Delete**: Deleted groupings are archived, not permanently deleted, for audit trail purposes (REQ-028-028)

**Notes**:

- Provide drag-and-drop interface for location ordering (intuitive reordering) (REQ-028-076)
- Display preview pane showing how patients from selected countries will see location list (REQ-028-076)
- Show country flags next to country names for visual clarity (REQ-028-076)
- Disable selection state or visually indicate countries already assigned to another grouping (e.g., greyed out with tooltip "Already assigned to [Grouping Name]") (REQ-028-076)
- Provide bulk actions: duplicate grouping, export configuration, import from template (REQ-028-077)

---

### Screen 2: Location Pricing Configuration (Admin)

**Purpose**: Allow admins to configure starting price estimates for each treatment destination per currency

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Destination Location | Select | Yes | Treatment destination (country/city) | Must be valid location in system (REQ-028-086) | ENT-location-starting-price.location_id |
| Location Default Currency | Select | No | Default currency for the selected destination; used when a patient's currency has no price and a converted price is shown | Must be supported currency; set per destination | ENT-location-starting-price.location_default_currency |
| Currency | Select | Yes | Currency for pricing (GBP, EUR, USD, etc.) | Must be supported currency | ENT-location-starting-price.currency_code |
| Starting Price | Number | Yes | Base starting price estimate | Positive number, decimals per currency rules | ENT-location-starting-price.starting_price_amount |
| Price Effective Date | Date | No | When this pricing becomes active | Future date optional, defaults to immediate | ENT-location-starting-price.effective_date |
| Price Expiry Date | Date | No | When this pricing expires | Must be after effective date if set | ENT-location-starting-price.expiry_date |
| Bulk Update Pricing | Button/Action | No | Opens bulk update modal (percentage or fixed adjustment across all currencies for selected destination) | Visible on the pricing screen; enabled only when a destination is selected or at least one pricing row is checked; requires change reason inside modal before apply (REQ-028-059) | no graph field (control) |
| Fallback Price | Checkbox | No | Use as fallback for unconfigured patient locations (REQ-028-056) | - | ENT-location-starting-price.is_fallback_price |
| Fallback Patient Country | Select | Yes when Fallback Price is checked | Patient country this fallback price is shown to | Must be a valid country in system | ENT-location-starting-price.country_code |
| System-Wide Default Starting Price | Number and currency | No | One default starting price (one amount and its currency) shown when no specific or fallback price applies; before any converted price is used | Positive number, decimals per currency rules; empty until an admin sets it; change reason required to save | no graph field (setting SET-system-wide-default-starting-price) |
| Last Updated | Date (read-only) | - | When price was last changed | Auto-updated | ENT-location-starting-price.updated_at |
| Updated By | Text (read-only) | - | Admin who updated price | Auto-populated | ENT-location-starting-price.updated_by_admin_id |
| Change Reason | Text | Yes | Reason for price change (for audit) | 10-500 chars | ENT-location-starting-price.change_reason |

**Business Rules**:

- **Currency Validation**: Only supported currencies (configured in system) can be selected (REQ-028-053)
- **Decimal Precision**: System enforces currency-appropriate decimal places (2 for GBP/EUR/USD, 0 for JPY/KRW) (REQ-028-055)
- **Positive Values Only**: Starting prices must be positive numbers greater than 0 (REQ-028-054)
- **Fallback Priority**: Fallback prices apply when patient's specific location-currency combination is not configured; the fallback price shown is the one set for the patient's country, and the system-wide default starting price applies next, before any converted price (REQ-028-039)
- **Price Expiry**: After a starting price's expiry date passes, patients no longer see it; they see the fallback price for their country, then the system-wide default starting price. A price with no expiry date stays active until an admin changes it (REQ-028-087)
- **Price History**: System maintains history of all price changes for audit and trend analysis (REQ-028-063)
- **Bulk Update**: Admins can apply percentage or fixed adjustments to multiple currency prices simultaneously through the bulk update modal (no CSV import or export) (REQ-028-057)
- **Preview Mode**: Admins can preview how prices appear to patients before saving (REQ-028-008)
- **Effective Dating**: If effective date is future, current pricing remains active until effective date (REQ-028-060)
- **Expiry Warning**: System warns admin 7 days before price expiry date (REQ-028-061)

**Notes**:

- Action bar: "Bulk Update Pricing" primary button visible on the pricing screen, enabled when a destination is selected (or when at least one row is checked in pricing table) (REQ-028-059)
- Display pricing table with locations as rows, currencies as columns for quick overview (REQ-028-078)
- Highlight cells without configured pricing in yellow (missing pricing) (REQ-028-051, REQ-028-078)
- Show "Last Updated" timestamp and admin name on hover for each price (REQ-028-078)
- Display exchange rate reference for admin guidance (from FR-029 currency service) (REQ-028-080)
- Include calculator tool: enter price in one currency, auto-suggest prices for other currencies based on exchange rates (REQ-028-080)
- Currency list is read-only from FR-029 Payment System Configuration; add/edit currencies via Settings > Billing Settings > Currency Management (REQ-028-052)
- Currency dropdown on this screen is populated from FR-029's supported currency list; no inline currency creation here (REQ-028-052)
- Bulk Update modal (triggered by "Bulk Update Pricing") includes (REQ-028-058):
  - Method selector: percentage increase/decrease or fixed amount adjustment
  - Adjustment value input with validation (numeric, allows negative for decrease)
  - Optional rounding rule (e.g., round to nearest 5/10/50 of currency unit)
  - Preview table showing current vs. new prices per currency before applying
  - Required change reason text field (logged in audit trail)
  - Confirmation banner: "[X] currency prices updated for [Location]" after apply (REQ-028-050)

---

### Screen 3: Location Display Preview (Admin)

**Purpose**: Allow admins to preview how location recommendations will appear to patients from different regions

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Preview Patient Location | Select | Yes | Patient country to simulate | Must be valid country in system | ENT-regional-grouping.country_list |
| Preview Currency | Select | Yes | Patient currency preference | Defaults to location's default currency (REQ-028-075) | ENT-location-starting-price.currency_code |
| Location List | Display (read-only) | - | Shows ordered location list as patient would see | - | ENT-regional-grouping.location_order |
| Starting Prices | Display (read-only) | - | Shows starting prices in preview currency | - | ENT-location-starting-price.starting_price_amount |
| Applied Regional Grouping | Display (read-only) | - | Shows which regional grouping was applied | - | ENT-regional-grouping.grouping_name |
| Fallback Indicators | Display (read-only) | - | Highlights locations using fallback pricing | - | ENT-location-starting-price.is_fallback_price |

**Business Rules**:

- **Real-Time Preview**: Preview updates immediately when admin selects different patient location or currency (REQ-028-069)
- **Applied Config Display**: System shows which regional grouping and pricing rules were applied (REQ-028-070)
- **Fallback Highlighting**: Locations using fallback pricing are visually distinguished (e.g., italic text, info icon) (REQ-028-071)
- **Missing Price Warning**: If any locations have no pricing for preview currency, system displays warning (REQ-028-072)
- **Provider Count Display**: Preview shows number of available providers per location (actual counts from provider database) (REQ-028-073)
- **Refresh Button**: Admin can manually refresh preview to see latest data after configuration changes (REQ-028-074)

**Notes**:

- Display side-by-side comparison: select two patient locations to compare how location lists differ (REQ-028-081)
- Show explanation tooltips: hover over location to see why it's in that position (regional grouping rule) (REQ-028-081)
- Provide "Test Mode" toggle: see how changes will appear without saving them (REQ-028-081)
- Display cache status indicator: shows when patient-facing data was last refreshed (REQ-028-081)

---

## Business Rules

### General Module Rules

- **Rule 1**: Regional groupings MUST NOT overlap - each country can belong to at most one grouping at a time. System enforces uniqueness and blocks saves that would assign a country to multiple groupings. (REQ-028-006)
- **Rule 2**: Location ordering is strictly advisory for patient presentation - it does not restrict which locations patients can select or providers can serve. (REQ-028-042)
- **Rule 3**: Starting prices are estimates only and do not constrain provider quote pricing. Providers can quote higher or lower than starting prices. (REQ-028-043)
- **Rule 4**: All configuration changes propagate to patient-facing APIs within 1 minute via cache invalidation (cache TTL = 60 seconds). (REQ-028-005)
- **Rule 5**: Maximum of 50 regional groupings to prevent administrative complexity (soft limit with admin warning). (REQ-028-030)
- **Rule 6**: Inactive regional groupings are retained in system but not applied to patient location presentation. (REQ-028-029)
- **Rule 7**: All create/update/archive actions require a change reason (10-500 chars) (REQ-028-024)
- **Error handling**: If regional configuration unavailable, fall back to default location ordering and pricing (REQ-028-085)
- **Error handling**: If country list unavailable, use cached country list (refreshed daily)

### Data & Privacy Rules

- **Privacy Rule 1**: Patient location data used for regional matching is stored in patient profile (already compliant with PHI encryption requirements per Principle II) (REQ-028-065)
- **Privacy Rule 2**: Starting price estimates are public data and not subject to encryption requirements (REQ-028-066)
- **Privacy Rule 3**: Pricing history includes admin user who made changes for accountability, but not patient-level pricing data (REQ-028-067)
- **Audit Rule**: All configuration changes (regional groupings, location ordering, starting prices) logged with timestamp, admin user, change reason, and full change details (REQ-028-011)
- **Retention Rule**: Pricing history and configuration change audit logs are kept; retention follows the system PRD, Platform-Wide Rules: One 10-year retention period (REQ-028-064)
- **GDPR Compliance**: Patient location data handling follows existing GDPR requirements from FR-001 (no additional requirements) (REQ-028-068)
- **Data Protection**: Regional configuration data is not sensitive (public pricing estimates, location display rules) - no encryption at rest required (REQ-028-066)
- **Audit Trail**: All configuration changes logged with admin user ID, timestamp, IP address, and full change details (old value → new value) (REQ-028-014)

### Admin Editability Rules

**Editable by Admin** (REQ-028-032):

- Regional grouping names, countries, and location ordering (full control)
- Starting price amounts for any location-currency combination
- Fallback pricing configuration per location
- Regional grouping active/inactive status
- Price effective dates and expiry dates
- Number of locations displayed per regional grouping (default 10, configurable range 5-20) (REQ-028-033)

**Fixed in Codebase (Not Editable)** (REQ-028-031):

- Cache propagation timing (1-minute TTL fixed for performance/consistency balance)
- Currency decimal precision rules (2 decimals for major currencies, 0 for yen/won)
- Maximum regional groupings limit (50 groupings)

**Configurable with Restrictions**:

- Fallback location ordering (when no regional grouping matches) is by proximity to the patient's location; there is no separate admin-editable default ordering list
- Currency support requires system-level configuration in FR-029 before location pricing can be configured (REQ-028-052)

### Payment & Billing Rules

- Not applicable to this module - FR-028 configures pricing display only, not actual payment processing (REQ-028-048)

---

## Dependencies

- **FR-026 / Module A-09 (App Settings & Security Policies)**: Regional configuration requires FR-026's centralized country list and country calling code management
- **FR-001 / Module P-01 (Auth & Profile Management)**: Patient location data stored in profile during registration
- **FR-003 / Module P-02 (Inquiry Submission & Distribution)**: Inquiry flow consumes regional configuration for location presentation
- **FR-029 / Module S-02 (Payment System Configuration)**: Currency conversion rates and supported currency list
- **FR-031 / Module A-09 (Admin Access Control)**: Role-based permissions for system configuration

---

## User Scenarios & Testing

### User Story 1 - Admin Creates Regional Grouping for UK Patients (Priority: P1)

**Description**: As a Hairline admin, I need to configure location recommendations for UK patients so they see Turkey first (most popular), then Poland, then UK domestic options, maximizing conversion rates and matching patient travel preferences.

**Why this priority**: This is the most critical workflow - without regional groupings, all patients see the same generic location list. Properly configured regional groupings directly impact quote request conversion rates and patient decision time. UK is the primary launch market, making this P1 essential functionality.

**Independent Test**: Create a regional grouping "UK" with Turkey first, Poland second, UK third. Verify configuration saves successfully, then simulate a UK patient viewing destination list to confirm locations appear in configured order with appropriate starting prices.

**Acceptance Scenarios**:

1. **Given** admin is logged in with System Configuration permissions, **When** admin navigates to Settings > General Settings > Location Presentation by Country tab, **Then** admin sees list of existing regional groupings and "Add New Regional Grouping" button
2. **Given** admin clicks "Add New Regional Grouping", **When** admin enters name "UK", selects "United Kingdom" from country list, and orders locations (Turkey 1st, Poland 2nd, UK 3rd), **Then** system displays preview showing UK patients will see Turkey first
3. **Given** admin has configured regional grouping with valid data, **When** admin clicks "Save", **Then** system validates configuration, saves to database, clears cache, and displays confirmation "Regional grouping saved. Changes will be live within 1 minute."
4. **Given** regional grouping has been saved for 60+ seconds, **When** UK patient reaches destination selection screen, **Then** patient sees Turkey as first location option, Poland as second, UK as third (matching configured order)
5. **Given** admin has created regional grouping, **When** admin views audit log, **Then** log shows configuration change with admin username, timestamp, and details (countries added, location order)

---

### User Story 2 - Admin Configures Starting Prices for Turkey in Multiple Currencies (Priority: P1)

**Description**: As a Hairline admin, I need to set starting price estimates for Turkey in GBP (£2,500), EUR (€2,800), and USD ($3,200) so patients from UK, Europe, and US see realistic pricing expectations in their local currency, improving quote acceptance rates.

**Why this priority**: Accurate starting prices are essential for setting patient expectations and reducing "price shock" when quotes arrive. Turkey is the most popular destination, and these three currencies cover 80% of initial target markets. Without currency-specific pricing, conversion rates suffer significantly.

**Independent Test**: Configure starting prices for Turkey in GBP, EUR, and USD. Verify prices save correctly, then simulate patients from UK, Germany, and US viewing Turkey destination to confirm appropriate currency and price displays.

**Acceptance Scenarios**:

1. **Given** admin is logged in with System Configuration permissions, **When** admin navigates to Settings > General Settings > Location Pricing tab and selects "Turkey", **Then** admin sees pricing table with currencies as columns and current configured prices
2. **Given** admin clicks "Add Currency" for Turkey, **When** admin selects "GBP" and enters "2500", **Then** system validates amount is positive number, displays formatted price "£2,500" in preview, and enables save
3. **Given** admin has entered valid prices for GBP, EUR, and USD for Turkey, **When** admin clicks "Save", **Then** system saves all three currency prices, displays confirmation "Starting prices for Turkey updated for 3 currencies", and logs changes in audit trail
4. **Given** starting prices have been configured for Turkey, **When** UK patient (location=UK, currency=GBP) views destination list, **Then** patient sees Turkey with starting price "Starting from £2,500"
5. **Given** starting prices have been configured for Turkey, **When** German patient (location=Germany, currency=EUR) views destination list, **Then** patient sees Turkey with starting price "Starting from €2,800"

---

### User Story 3 - Patient from Unconfigured Region Sees Fallback Pricing (Priority: P2)

**Description**: As a patient from Australia (region without configured pricing), I need to see reasonable starting price estimates in my local currency (AUD) so I can make informed decisions about treatment destinations, even though my specific region hasn't been configured yet.

**Why this priority**: While P2 (not as critical as core regional configuration), this ensures platform gracefully handles patients from regions admins haven't configured yet. This becomes more important as platform expands globally. Without fallback pricing, patients from unconfigured regions see no pricing or confusing currency conversions, hurting conversion rates.

**Independent Test**: Configure fallback pricing for Turkey in USD for patients from Australia. Simulate Australian patient (no regional grouping, no AUD pricing configured) viewing Turkey. Verify patient sees fallback USD price with currency conversion note.

**Acceptance Scenarios**:

1. **Given** admin has configured fallback pricing for Turkey in USD at $3,200 for patients from Australia, **When** Australian patient (no regional grouping, currency preference=AUD) views Turkey destination, **Then** patient sees "Starting from $3,200 (approx. A$4,800)" with conversion note
2. **Given** patient is from unconfigured region, **When** patient views destination list, **Then** patient sees locations ordered by proximity to patient location (FR-003 default behavior)
3. **Given** admin views preview tool, **When** admin selects "Australia" as preview location, **Then** preview shows fallback indicator (e.g., info icon tooltip "Using fallback pricing - AUD pricing not configured for this location")

---

### User Story 4 - Admin Bulk Updates Pricing Across All Currencies (Priority: P2)

**Description**: As a Hairline admin, I need to increase starting prices for Turkey by 10% across all currencies due to exchange rate shifts and provider cost increases, without manually updating each currency individually, saving time and ensuring consistency.

**Why this priority**: P2 because while not essential for launch, bulk updates significantly improve admin efficiency and reduce errors when market conditions require pricing adjustments. Without this, admins must update 5-10 currencies per location individually, taking 10x longer and risking inconsistencies.

**Independent Test**: Configure pricing for Turkey in 5 currencies. Use bulk update tool to increase all prices by 10%. Verify all currency prices updated proportionally and audit log shows bulk change with admin user and reason.

**Acceptance Scenarios**:

1. **Given** admin has configured pricing for Turkey in GBP, EUR, USD, AUD, and CAD, **When** admin selects Turkey and clicks "Bulk Update Pricing", **Then** system displays bulk update modal with options (percentage increase/decrease, fixed amount adjustment)
2. **Given** admin selects "Percentage Increase" and enters "10", **When** system calculates new prices, **Then** preview shows all 5 currencies with current price → new price (e.g., GBP £2,500 → £2,750)
3. **Given** admin reviews bulk update preview and confirms, **When** admin clicks "Apply Bulk Update", **Then** system saves all 5 currency prices simultaneously, displays confirmation "5 currency prices updated for Turkey", and logs bulk change in audit trail with reason "10% increase due to exchange rate shift"
4. **Given** bulk update completed, **When** patient views Turkey destination within 1 minute, **Then** patient sees updated starting price reflecting 10% increase

---

### User Story 5 - Admin Previews Configuration Before Applying Changes (Priority: P3)

**Description**: As a Hairline admin, I need to preview how regional grouping and pricing changes will appear to patients from different regions before saving them, so I can verify configurations are correct and avoid publishing errors to production.

**Why this priority**: P3 because preview mode is a quality-of-life feature for admins, not essential functionality. Admins can test configurations by saving and checking patient app directly, but preview mode improves admin confidence and reduces configuration errors. More valuable as system complexity grows.

**Independent Test**: Create or edit regional grouping in preview mode (unsaved changes). Select different patient locations in preview tool. Verify preview updates in real-time to show how unsaved configuration will appear. Verify saving applies changes and refreshing preview.

**Acceptance Scenarios**:

1. **Given** admin is editing regional grouping (unsaved changes), **When** admin toggles "Preview Mode" on, **Then** admin sees side panel with preview tool (select patient location, view resulting location order)
2. **Given** preview mode is active, **When** admin reorders locations in configuration panel (e.g., moves Poland to 1st position), **Then** preview panel updates in real-time to show Poland now appears first for selected patient region
3. **Given** admin views preview for UK patient, **When** admin changes preview selection to "Germany", **Then** preview refreshes to show location ordering and pricing as German patient would see (different regional grouping may apply)
4. **Given** admin has verified configuration in preview mode, **When** admin clicks "Save and Apply", **Then** system saves configuration and preview updates to show "Live Configuration" (no longer preview mode)

---

### Edge Cases

- **What happens when admin tries to assign a country to more than one regional grouping?** System blocks the change, shows error listing conflicting groupings, and requires admin to resolve by keeping the country in only one grouping. (REQ-028-021)

- **How does system handle location with no pricing configured for patient's currency?** System falls back to the fallback price for the patient's country (if configured), then to the system-wide default starting price (if set), then converts from location's default currency using the admin-configured conversion rate with markup (from FR-029), displaying converted price with note: "Starting from €2,200 (approx. £2,500)". (REQ-028-040)

- **What occurs if admin deletes a regional grouping while patients are actively viewing destinations using that grouping?** Cached data serves existing sessions for up to 60 seconds (cache TTL). After cache expiration, patients see default location ordering. No errors displayed to patients - graceful degradation. (REQ-028-027, REQ-028-084)

- **How to manage concurrent admin edits to same regional grouping?** System uses optimistic locking - if two admins edit simultaneously, last save wins. System displays warning if configuration changed since admin opened edit screen: "This grouping was modified by [Admin Name] at [Time]. Your changes will overwrite theirs. Continue?" (REQ-028-082)

- **What happens when provider location is added or removed while regional groupings reference it?** System maintains location references even if provider deactivated (preserves configuration). If provider reactivates, location ordering still applies. If location permanently removed from system, admin sees warning in regional grouping edit screen: "[Location] is no longer active. Remove from ordering?" (REQ-028-083)

- **How does system handle fallback pricing when no fallback or system-wide default is configured and currency conversion unavailable?** System displays location without starting price, shows generic text "Price available on request" to patient, and logs error for admin review. Admin sees warning in dashboard: "[Location] missing fallback pricing - patients seeing no price estimate." (REQ-028-041)

- **What occurs if admin sets effective date for pricing but forgets to set expiry date?** Pricing remains active indefinitely until admin manually updates or sets expiry. System displays info note in pricing table: "No expiry set - pricing active indefinitely." No automatic expiration enforced. (When an expiry date is set and has passed, the price stops showing and the fallback price, then the system-wide default, shows instead.) (REQ-028-062)

---

## Functional Requirements Summary

### Core Requirements

- **REQ-028-001**: System MUST allow admins to create regional groupings by selecting group name, countries, and location presentation order
- **REQ-028-002**: System MUST allow admins to configure starting price estimates per location per currency
- **REQ-028-003**: System MUST apply regional grouping to patient destination list based on patient's location from profile or IP geolocation
- **REQ-028-004**: System MUST display starting prices in patient's preferred currency; if the specific currency is not configured, it falls back to the fallback price for the patient's country, then to the system-wide default starting price, then to the price in the location's default currency with conversion
- **REQ-028-005**: System MUST propagate configuration changes to patient-facing APIs within 1 minute via cache invalidation
- **REQ-028-006**: System MUST prevent overlapping regional groupings by enforcing one-to-one mapping between country and regional grouping at configuration time
- **REQ-028-007**: System MUST support fallback pricing for locations when patient's specific currency is not configured; the fallback price is chosen by the patient's country
- **REQ-028-008**: System MUST allow admins to preview how configurations will appear to patients from different regions before saving
- **REQ-028-087**: After a starting price's expiry date has passed, patients MUST no longer see that price; they see the fallback price for their country, then the system-wide default starting price. Prices with no expiry date stay active until an admin changes them
- **REQ-028-088**: System MUST provide one system-wide default starting price (one amount and its currency), set by admins on the pricing screen; it is empty until an admin sets it
- **REQ-028-089**: System MUST let admins set a default currency for each destination location

### Data Requirements

- **REQ-028-009**: System MUST store regional grouping configuration with grouping name, country list, location ordering, and status (active/inactive)
- **REQ-028-010**: System MUST store starting price configuration with location, currency, amount, effective date, expiry date, fallback flag, and (for a fallback price) the patient country it applies to
- **REQ-028-011**: System MUST maintain audit trail of all configuration changes with admin user, timestamp, change reason, and change details

### Security & Privacy Requirements

- **REQ-028-013**: System MUST restrict regional configuration and pricing management to admin users with "System Configuration" role (per FR-031)
- **REQ-028-014**: System MUST log all configuration changes with admin user ID, timestamp, IP address, change reason, and full change details for audit trail
- **REQ-028-015**: System MUST validate all admin inputs server-side (country codes, currency codes, positive pricing amounts) to prevent invalid configurations
- Rate limiting of the admin configuration API is owned by the system PRD (one shared Rule for all admin settings APIs).

### Integration Requirements

- **REQ-028-017**: System MUST integrate with FR-026 country list API for country selection in regional grouping configuration
- **REQ-028-018**: System MUST integrate with FR-029 currency API for currency validation and conversion rate retrieval
- **REQ-028-019**: System MUST provide REST API for patient apps to fetch regional configuration (location ordering + starting prices) based on patient location and currency
- **REQ-028-020**: System MUST expose admin configuration API for CRUD operations on regional groupings and starting prices with role-based access control

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-11-22 | 1.5 | Requirements graph programme baseline: PRD compressed to the checklist structure (each rule stated once, field rows tagged with graph field ids, dropped classes removed). No rule changes. Earlier history (v1.0 to v1.4) and the change requests (the PRD names none) are in `archived/prd-baseline-2026-11-08/` and in git history. | Product Team |

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
**Based on**: FR-011 Aftercare & Recovery Management PRD
**Last Updated**: 2026-11-22
