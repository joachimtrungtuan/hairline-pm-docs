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

1. **Define regional groupings** - Group countries into logical regions (e.g., "Europe", "Eastern Europe", "UK only") for consistent presentation
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

- Displays list of treatment destinations filtered and ordered by patient location
- Shows starting price estimates for each destination in patient's local currency
- Uses regional configuration to personalize the destination selection experience
- No direct editing capabilities - purely consumption of admin-configured data

**Provider Platform (PR-02: Inquiry & Quote Management)**:

- Indirectly benefits from regional configuration through improved inquiry quality
- Providers receive inquiries from patients with realistic pricing expectations
- No direct interaction with regional configuration settings
- Quote submission pricing is provider-controlled, not constrained by starting prices

**Admin Platform (A-09: System Settings & Configuration)**:

- Create and manage regional groupings (e.g., "Europe", "Eastern Europe", "UK", "Germany Only")
- Assign countries to regional groupings
- Define location presentation order per regional grouping (which destinations show first, second, third, etc.)
- Configure starting prices per destination per currency
- Set fallback pricing for locations without preset configurations
- Enable/disable specific destinations for specific patient regions
- Preview how configurations will appear to patients from different locations

**Shared Services**:

- None - this is pure configuration data stored in database and served via existing API infrastructure

### Communication Structure

**In Scope**:

- Admin receives system notifications when regional configuration changes are saved
- Configuration changes propagate to patient-facing APIs within 1 minute (cache refresh)

**Out of Scope**:

- Patient notifications about pricing changes (handled by general notification system)
- Provider notifications about regional configuration updates (providers unaffected by these settings)
- Real-time pricing updates based on exchange rates (covered by FR-029: Payment System Configuration)

### Entry Points

**Admin Entry Point**:

- Admin navigates to Settings > General Settings > Location Presentation & Pricing tab (Hairline app settings now live under General Settings)
- Access requires admin role with "System Configuration" permissions (per FR-031)
- Configuration changes take effect immediately upon save (within 1-minute cache propagation)

**Patient Entry Point** (consumption only):

- Patient reaches "Choose Your Destination" screen during quote request flow
- System automatically determines patient's location from profile or IP geolocation
- System applies appropriate regional configuration to filter and order destination list
- Starting prices are fetched and displayed in patient's preferred currency

---

## Business Workflows

### Main Flow: Admin Configures Regional Location Presentation

**Actors**: Admin (System Settings Configuration Role)
**Trigger**: Admin wants to optimize location presentation for specific patient regions
**Outcome**: Regional grouping created with location ordering rules; changes visible to patients from target region within 1 minute

**Steps**:

1. Admin navigates to Settings > General Settings > Location Presentation by Country tab
2. Admin clicks "Add New Regional Grouping"
3. Admin enters grouping name (e.g., "Europe", "Eastern Europe", "UK Only")
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
**Outcome**: Starting prices configured for destination per currency; prices visible to patients immediately upon next request

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

- **Trigger**: Admin wants to provide default pricing for patients whose location doesn't have preset pricing
- **Steps**:
  1. Admin navigates to Location Pricing > Fallback Pricing
  2. Admin selects destination location
  3. Admin enables fallback pricing option
  4. Admin enters fallback price per currency
  5. Admin enters change reason (required)
  6. System saves fallback configuration
  7. System confirms: "Fallback pricing enabled for [Location]. Patients from unconfigured countries will see these prices."
- **Outcome**: Fallback pricing active; patients without specific regional pricing see fallback prices

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

**B3: Admin Attempts to Set Invalid Price**:

- **Trigger**: Admin enters non-numeric or negative value for price
- **Steps**:
  1. Admin attempts to save invalid price
  2. System displays validation error: "Starting price must be a positive number."
  3. Admin corrects value or cancels
- **Outcome**: Invalid pricing not saved

**B4: Admin Attempts to Set Price for Unsupported Currency**:

- **Trigger**: Admin selects currency not configured in system
- **Steps**:
  1. Admin attempts to save price for unsupported currency
  2. System displays error: "[Currency] is not currently supported. Add currency to system first via Currency Management."
  3. Admin navigates to Settings > Billing Settings > Currency Management (FR-029) or cancels
- **Outcome**: Price not saved for unsupported currency

**B5: Admin Attempts to Save Pricing Without Change Reason**:

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
   - If no specific pricing, display fallback price for location (if configured)
   - If no fallback, display default starting price (system-wide default)
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
  2. System checks for fallback pricing in patient's currency
  3. If fallback exists, display fallback price
  4. If no fallback, display price in location's default currency with conversion note: "Starting from €2,200 (approx. £2,500)"
  5. Conversion uses real-time exchange rate from FR-029 currency service
- **Outcome**: Patient sees estimated pricing with currency conversion note

---

## Screen Specifications

### Screen 1: Regional Grouping Management (Admin)

**Purpose**: Allow admins to create and manage regional groupings that control location presentation order for different patient regions

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Grouping Name | Text | Yes | Name of regional grouping (e.g., "Europe", "UK Only") | Max 100 chars, must be unique |
| Description | Text | No | Internal description of grouping purpose | Max 500 chars |
| Countries | Multi-select | Yes | List of countries that belong to this grouping | At least 1 country must be selected |
| Location Order | Drag-and-drop list | Yes | Ordered list of destination locations to display | At least 1 location must be ordered |
| Status | Toggle | Yes | Active/Inactive status | Active = applies to patients, Inactive = archived |
| Change Reason | Text | Yes | Reason for grouping change (create/update/archive) | 10-500 chars |
| Created Date | Date (read-only) | - | When grouping was created | Auto-generated |
| Last Modified | Date (read-only) | - | When grouping was last updated | Auto-updated on save |
| Modified By | Text (read-only) | - | Admin user who last modified | Auto-populated |

**Business Rules**:

- **Unique Membership**: Each country can only belong to one regional grouping at a time. If admin attempts to add a country that already exists in another grouping, system blocks save and shows error with list of conflicting groupings.
- **Default Fallback**: If no regional grouping matches, system orders destinations by proximity to patient location (FR-003 default behavior)
- **Cache Propagation**: Configuration changes propagate to patient-facing APIs within 1 minute via cache invalidation
- **Audit Trail**: All changes logged with timestamp, admin user, and change details (added/removed countries, reordered locations)
- **Soft Delete**: Deleted groupings are archived, not permanently deleted, for audit trail purposes

**Notes**:

- Provide drag-and-drop interface for location ordering (intuitive reordering)
- Display preview pane showing how patients from selected countries will see location list
- Show country flags next to country names for visual clarity
- Disable selection state or visually indicate countries already assigned to another grouping (e.g., greyed out with tooltip "Already assigned to [Grouping Name]")
- Provide bulk actions: duplicate grouping, export configuration, import from template

---

### Screen 2: Location Pricing Configuration (Admin)

**Purpose**: Allow admins to configure starting price estimates for each treatment destination per currency

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Destination Location | Select | Yes | Treatment destination (country/city) | Must be valid location in system |
| Currency | Select | Yes | Currency for pricing (GBP, EUR, USD, etc.) | Must be supported currency |
| Starting Price | Number | Yes | Base starting price estimate | Positive number, decimals per currency rules |
| Price Effective Date | Date | No | When this pricing becomes active | Future date optional, defaults to immediate |
| Price Expiry Date | Date | No | When this pricing expires | Must be after effective date if set |
| Bulk Update Pricing | Button/Action | No | Opens bulk update modal (percentage or fixed adjustment across all currencies for selected destination) | Enabled only when a destination is selected (or pricing rows are selected); requires change reason inside modal before apply |
| Fallback Price | Checkbox | No | Use as fallback for unconfigured patient locations | - |
| Last Updated | Date (read-only) | - | When price was last changed | Auto-updated |
| Updated By | Text (read-only) | - | Admin who updated price | Auto-populated |
| Change Reason | Text | Yes | Reason for price change (for audit) | 10-500 chars |

**Business Rules**:

- **Currency Validation**: Only supported currencies (configured in system) can be selected
- **Decimal Precision**: System enforces currency-appropriate decimal places (2 for GBP/EUR/USD, 0 for JPY/KRW)
- **Positive Values Only**: Starting prices must be positive numbers greater than 0
- **Fallback Priority**: Fallback prices apply when patient's specific location-currency combination is not configured
- **Price History**: System maintains history of all price changes for audit and trend analysis
- **Bulk Update**: Admins can apply percentage or fixed adjustments to multiple currency prices simultaneously
- **Preview Mode**: Admins can preview how prices appear to patients before saving
- **Effective Dating**: If effective date is future, current pricing remains active until effective date
- **Expiry Warning**: System warns admin 7 days before price expiry date

**Notes**:

- Action bar: "Bulk Update Pricing" primary button visible when a destination is selected (or when at least one row is checked in pricing table)
- Display pricing table with locations as rows, currencies as columns for quick overview
- Highlight cells without configured pricing in yellow (missing pricing)
- Show "Last Updated" timestamp and admin name on hover for each price
- Provide CSV import/export for bulk pricing updates
- Display exchange rate reference for admin guidance (from FR-029 currency service)
- Include calculator tool: enter price in one currency, auto-suggest prices for other currencies based on exchange rates
- Currency list is read-only from FR-029 Payment System Configuration; add/edit currencies via Settings > Billing Settings > Currency Management
- Currency dropdown on this screen is populated from FR-029's supported currency list; no inline currency creation here
- Bulk Update modal (triggered by "Bulk Update Pricing") includes:
  - Method selector: percentage increase/decrease or fixed amount adjustment
  - Adjustment value input with validation (numeric, allows negative for decrease)
  - Optional rounding rule (e.g., round to nearest 5/10/50 of currency unit)
  - Preview table showing current vs. new prices per currency before applying
  - Required change reason text field (logged in audit trail)
  - Confirmation banner: "[X] currency prices updated for [Location]" after apply

---

### Screen 3: Location Display Preview (Admin)

**Purpose**: Allow admins to preview how location recommendations will appear to patients from different regions

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Preview Patient Location | Select | Yes | Patient country to simulate | Must be valid country in system |
| Preview Currency | Select | Yes | Patient currency preference | Defaults to location's default currency |
| Location List | Display (read-only) | - | Shows ordered location list as patient would see | - |
| Starting Prices | Display (read-only) | - | Shows starting prices in preview currency | - |
| Applied Regional Grouping | Display (read-only) | - | Shows which regional grouping was applied | - |
| Fallback Indicators | Display (read-only) | - | Highlights locations using fallback pricing | - |

**Business Rules**:

- **Real-Time Preview**: Preview updates immediately when admin selects different patient location or currency
- **Applied Config Display**: System shows which regional grouping and pricing rules were applied
- **Fallback Highlighting**: Locations using fallback pricing are visually distinguished (e.g., italic text, info icon)
- **Missing Price Warning**: If any locations have no pricing for preview currency, system displays warning
- **Provider Count Display**: Preview shows number of available providers per location (actual counts from provider database)
- **Refresh Button**: Admin can manually refresh preview to see latest data after configuration changes

**Notes**:

- Display side-by-side comparison: select two patient locations to compare how location lists differ
- Show explanation tooltips: hover over location to see why it's in that position (regional grouping rule)
- Provide "Test Mode" toggle: see how changes will appear without saving them
- Display cache status indicator: shows when patient-facing data was last refreshed

---

## Business Rules

### General Module Rules

- **Rule 1**: Regional groupings MUST NOT overlap - each country can belong to at most one grouping at a time. System enforces uniqueness and blocks saves that would assign a country to multiple groupings.
- **Rule 2**: Location ordering is strictly advisory for patient presentation - it does not restrict which locations patients can select or providers can serve.
- **Rule 3**: Starting prices are estimates only and do not constrain provider quote pricing. Providers can quote higher or lower than starting prices.
- **Rule 4**: All configuration changes propagate to patient-facing APIs within 1 minute via cache invalidation (cache TTL = 60 seconds).
- **Rule 5**: Maximum of 50 regional groupings to prevent administrative complexity (soft limit with admin warning).
- **Rule 6**: Inactive regional groupings are retained in system but not applied to patient location presentation.
- **Rule 7**: All create/update/archive actions require a change reason (10-500 chars)

### Data & Privacy Rules

- **Privacy Rule 1**: Patient location data used for regional matching is stored in patient profile (already compliant with PHI encryption requirements per Principle II)
- **Privacy Rule 2**: Starting price estimates are public data and not subject to encryption requirements
- **Privacy Rule 3**: Pricing history includes admin user who made changes for accountability, but not patient-level pricing data
- **Audit Rule**: All configuration changes (regional groupings, location ordering, starting prices) logged with timestamp, admin user, change reason, and full change details
- **Retention Rule**: Pricing history and configuration change audit logs retained for 10 years (Constitution compliance)
- **GDPR Compliance**: Patient location data handling follows existing GDPR requirements from FR-001 (no additional requirements)

### Admin Editability Rules

**Editable by Admin**:

- Regional grouping names, countries, and location ordering (full control)
- Starting price amounts for any location-currency combination
- Fallback pricing configuration per location
- Regional grouping active/inactive status
- Price effective dates and expiry dates
- Number of locations displayed per regional grouping (default 10, configurable range 5-20)

**Fixed in Codebase (Not Editable)**:

- Cache propagation timing (1-minute TTL fixed for performance/consistency balance)
- Currency decimal precision rules (2 decimals for major currencies, 0 for yen/won)
- Maximum regional groupings limit (50 groupings)

**Configurable with Restrictions**:

- Default location ordering (fallback when no regional grouping matches) is editable, but must include all active provider locations
- Currency support requires system-level configuration in FR-029 before location pricing can be configured

### Payment & Billing Rules

- Not applicable to this module - FR-028 configures pricing display only, not actual payment processing

---

## Success Criteria

### Patient Experience Metrics

- **SC-001**: Patients from configured regional groupings see their most relevant treatment destinations in top 3 positions 100% of the time
- **SC-002**: Starting price estimates displayed to patients are within 20% of average actual quoted prices for that location-currency combination (measured quarterly)
- **SC-003**: 90% of patients select a destination from the top 5 recommended locations (indicates effective regional configuration)
- **SC-004**: Patient destination selection screen loads in under 2 seconds with all location data and pricing (p95)

### Provider Efficiency Metrics

- **SC-005**: Inquiries received by providers show 30% reduction in "price shock" rejections (patients declining quotes due to price expectations mismatch) compared to pre-implementation baseline
- **SC-006**: Provider quote acceptance rates improve by 15% due to better-aligned patient expectations from accurate starting prices

### Admin Management Metrics

- **SC-007**: Admins can create or modify a regional grouping (including location ordering) in under 3 minutes
- **SC-008**: Admins can update starting prices for a location across all currencies in under 2 minutes using bulk update feature
- **SC-009**: Configuration changes propagate to patient-facing app within 1 minute of admin save action (100% of changes)
- **SC-010**: Zero configuration conflicts at runtime related to overlapping regional groupings (system prevents overlaps at configuration time by enforcing unique country-to-grouping assignment)

### System Performance Metrics

- **SC-011**: Location presentation configuration queries complete in under 50ms (p95)
- **SC-012**: Starting price lookups complete in under 30ms per location (p95)
- **SC-013**: Cache invalidation propagates across all API servers within 60 seconds of configuration change
- **SC-014**: System supports 10,000 concurrent patient location requests without degradation (load testing target)

### Business Impact Metrics

- **SC-015**: Quote request conversion rates (inquiry to quote acceptance) increase by 20% within 3 months of implementing accurate starting price estimates
- **SC-016**: Average time patients spend on destination selection screen decreases by 25% due to optimized location ordering (less decision fatigue)
- **SC-017**: Platform can launch in new geographic markets 50% faster by rapidly configuring regional groupings and starting prices for new patient regions
- **SC-018**: Pricing adjustment response time improves by 75% - admins can respond to market changes (competitor pricing, exchange rate shifts) and update starting prices platform-wide within 5 minutes

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **FR-026 / Module A-09 (App Settings & Security Policies)**: Regional configuration requires FR-026's centralized country list and country calling code management
  - **Why needed**: Regional groupings select from the shared country list maintained in FR-026
  - **Integration point**: Regional grouping configuration screen uses country list API from FR-026

- **FR-001 / Module P-01 (Auth & Profile Management)**: Patient location data stored in profile during registration
  - **Why needed**: System uses patient's stored location to determine which regional grouping applies
  - **Integration point**: Regional configuration service queries patient profile for location field

- **FR-003 / Module P-02 (Inquiry Submission & Distribution)**: Inquiry flow consumes regional configuration for location presentation
  - **Why needed**: Destination selection screen displays locations in regionally configured order with starting prices
  - **Integration point**: Quote request API fetches regional configuration based on patient location

- **FR-029 / Module S-02 (Payment System Configuration)**: Currency conversion rates and supported currency list
  - **Why needed**: Starting prices must use supported currencies, and fallback pricing may require currency conversion
  - **Integration point**: Location pricing configuration validates currencies against FR-029's supported currency list; uses conversion rates for preview tool

- **FR-031 / Module A-09 (Admin Access Control)**: Role-based permissions for system configuration
  - **Why needed**: Only authorized admin users with "System Configuration" role can modify regional groupings and starting prices
  - **Integration point**: Regional configuration screens check admin permissions via FR-031 authorization service

### External Dependencies (APIs, Services)

- **None**: This module does not integrate with external services. Currency conversion rates are provided internally by FR-029.

### Data Dependencies

- **Entity 1: Provider Locations**: Active provider locations with service coverage
  - **Why needed**: Location ordering configuration requires list of available treatment destinations (provider locations)
  - **Source**: Provider onboarding module (PR-01) maintains list of provider locations

- **Entity 2: Country Master List**: Centrally managed list of countries with codes and names
  - **Why needed**: Regional groupings select countries from this master list
  - **Source**: FR-026 provides centralized country list management

- **Entity 3: Currency Master List**: Supported currencies with codes and decimal rules
  - **Why needed**: Starting price configuration requires list of supported currencies
  - **Source**: FR-029 provides currency configuration and validation rules

---

## Assumptions

### User Behavior Assumptions

- **Assumption 1**: Admins will configure regional groupings for major patient markets (UK, US, Europe, Middle East) within first month of platform launch
- **Assumption 2**: Admins will update starting prices quarterly or when market conditions change significantly (exchange rate shifts >10%, competitor pricing changes)
- **Assumption 3**: Patients trust starting price estimates as rough guidance but understand actual quotes may vary
- **Assumption 4**: Patients from regions without configured pricing (fallback pricing) are less sensitive to price variations and accept broader ranges

### Technology Assumptions

- **Assumption 1**: Patient location can be reliably determined from profile data or IP geolocation with 90%+ accuracy
- **Assumption 2**: Caching infrastructure (Redis or equivalent) can propagate configuration changes to all API servers within 60 seconds
- **Assumption 3**: Admin interface accessed via modern browsers (Chrome, Firefox, Safari, Edge - last 2 versions) with JavaScript enabled
- **Assumption 4**: Database performance sufficient to handle 10,000+ concurrent patient location configuration queries without degradation

### Business Process Assumptions

- **Assumption 1**: Regional pricing strategies will vary significantly by patient location (e.g., UK patients see higher starting prices than Middle Eastern patients for same destination)
- **Assumption 2**: Starting price estimates are set conservatively (slightly higher than minimum expected quotes) to avoid patient disappointment
- **Assumption 3**: Location ordering priorities will change over time based on provider network growth and patient preferences
- **Assumption 4**: Admins will use bulk pricing tools for major pricing adjustments (not updating each location-currency combination individually)
- **Assumption 5**: Pricing history will be audited quarterly by finance team for compliance and trend analysis

---

## Implementation Notes

### Technical Considerations

- **Architecture**: Regional configuration data requires fast read access with infrequent writes - ideal for caching layer
- **Caching Strategy**: Use Redis or equivalent with 60-second TTL; cache invalidation on configuration changes
- **Database Indexing**: Index on `patient_location` and `currency` for fast regional grouping and pricing lookups
- **Query Optimization**: Pre-compute location ordering and cache per regional grouping to avoid sorting on every request
- **Scalability**: Regional configuration queries are read-heavy (10,000:1 read:write ratio) - optimize for read performance

### Integration Points

- **Integration 1: Patient API to Regional Configuration Service**
  - **Data format**: REST API request with patient location (country code) and currency code; returns ordered location list with starting prices
  - **Authentication**: Internal service-to-service authentication (OAuth2 client credentials)
  - **Error handling**: If regional configuration unavailable, fall back to default location ordering and pricing

- **Integration 2: Admin UI to Regional Configuration API**
  - **Data format**: REST API for CRUD operations on regional groupings and starting prices; JSON request/response
  - **Authentication**: Admin user JWT tokens with role-based permissions validation
  - **Error handling**: Validation errors returned with specific field-level error messages; retry with exponential backoff on server errors

- **Integration 3: Regional Configuration Service to FR-026 Country List**
  - **Data format**: Shared database access or internal API call to fetch country list
  - **Authentication**: Internal service-to-service authentication
  - **Error handling**: If country list unavailable, use cached country list (refreshed daily)

### Scalability Considerations

- **Current scale**: Expected 50 regional groupings, 500 location-currency pricing combinations
- **Growth projection**: Regional groupings may grow to 100-150 as platform expands to new markets; pricing combinations to 2,000-3,000
- **Peak load**: 10,000 concurrent patient location requests during marketing campaigns or seasonal peaks
- **Data volume**: Regional configuration data is small (<1 MB total) - caching entire dataset in memory is feasible
- **Scaling strategy**: Horizontal scaling of API servers with shared Redis cache; configuration data replicated across all cache instances

### Security Considerations

- **Authentication**: Admin configuration access requires authenticated session with admin role and "System Configuration" permission (per FR-031)
- **Authorization**: Role-based access control enforced on all configuration endpoints - read-only roles cannot modify regional groupings or pricing
- **Data Protection**: Regional configuration data is not sensitive (public pricing estimates, location display rules) - no encryption at rest required
- **Audit Trail**: All configuration changes logged with admin user ID, timestamp, IP address, and full change details (old value → new value)
- **Input Validation**: All admin inputs validated server-side - country codes checked against master list, pricing validated as positive numbers with appropriate decimals
- **Rate Limiting**: Admin configuration API rate-limited to 100 requests/minute per admin user to prevent abuse
- **Cache Poisoning Protection**: Cache keys include version hash to prevent stale data serving after configuration changes

---

## User Scenarios & Testing

### User Story 1 - Admin Creates Regional Grouping for UK Patients (Priority: P1)

**Description**: As a Hairline admin, I need to configure location recommendations for UK patients so they see Turkey first (most popular), then Poland, then UK domestic options, maximizing conversion rates and matching patient travel preferences.

**Why this priority**: This is the most critical workflow - without regional groupings, all patients see the same generic location list. Properly configured regional groupings directly impact quote request conversion rates (SC-015) and patient decision time (SC-016). UK is the primary launch market, making this P1 essential functionality.

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

**Why this priority**: Accurate starting prices are essential for setting patient expectations and reducing "price shock" when quotes arrive (SC-005). Turkey is the most popular destination, and these three currencies cover 80% of initial target markets. Without currency-specific pricing, conversion rates suffer significantly.

**Independent Test**: Configure starting prices for Turkey in GBP, EUR, and USD. Verify prices save correctly, then simulate patients from UK, Germany, and US viewing Turkey destination to confirm appropriate currency and price displays.

**Acceptance Scenarios**:

1. **Given** admin is logged in with System Configuration permissions, **When** admin navigates to Settings > General Settings > Location Pricing tab and selects "Turkey", **Then** admin sees pricing table with currencies as columns and current configured prices
2. **Given** admin clicks "Add Currency" for Turkey, **When** admin selects "GBP" and enters "2500", **Then** system validates amount is positive number, displays formatted price "£2,500" in preview, and enables save
3. **Given** admin has entered valid prices for GBP, EUR, and USD for Turkey, **When** admin clicks "Save", **Then** system saves all three currency prices, displays confirmation "Starting prices for Turkey updated for 3 currencies", and logs changes in audit trail
4. **Given** starting prices have been configured for Turkey, **When** UK patient (location=UK, currency=GBP) views destination list, **Then** patient sees Turkey with starting price "Starting from £2,500"
5. **Given** starting prices have been configured for Turkey, **When** German patient (location=Germany, currency=EUR) views destination list, **Then** patient sees Turkey with starting price "Starting from €2,800"
6. **Given** admin has configured multiple currency prices, **When** admin exports pricing configuration to CSV, **Then** CSV includes all location-currency combinations with prices and last updated timestamps

---

### User Story 3 - Patient from Unconfigured Region Sees Fallback Pricing (Priority: P2)

**Description**: As a patient from Australia (region without configured pricing), I need to see reasonable starting price estimates in my local currency (AUD) so I can make informed decisions about treatment destinations, even though my specific region hasn't been configured yet.

**Why this priority**: While P2 (not as critical as core regional configuration), this ensures platform gracefully handles patients from regions admins haven't configured yet. This becomes more important as platform expands globally. Without fallback pricing, patients from unconfigured regions see no pricing or confusing currency conversions, hurting conversion rates.

**Independent Test**: Configure fallback pricing for Turkey in USD (as international default). Simulate Australian patient (no regional grouping, no AUD pricing configured) viewing Turkey. Verify patient sees fallback USD price with currency conversion note.

**Acceptance Scenarios**:

1. **Given** admin has configured fallback pricing for Turkey in USD at $3,200, **When** Australian patient (no regional grouping, currency preference=AUD) views Turkey destination, **Then** patient sees "Starting from $3,200 (approx. A$4,800)" with conversion note
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

- **What happens when admin tries to assign a country to more than one regional grouping?** System blocks the change, shows error listing conflicting groupings, and requires admin to resolve by keeping the country in only one grouping.

- **How does system handle location with no pricing configured for patient's currency?** System falls back to location's fallback pricing (if configured), then converts from location's default currency using real-time exchange rate (from FR-029), displaying converted price with note: "Starting from €2,200 (approx. £2,500)".

- **What occurs if admin deletes a regional grouping while patients are actively viewing destinations using that grouping?** Cached data serves existing sessions for up to 60 seconds (cache TTL). After cache expiration, patients see default location ordering. No errors displayed to patients - graceful degradation.

- **How to manage concurrent admin edits to same regional grouping?** System uses optimistic locking - if two admins edit simultaneously, last save wins. System displays warning if configuration changed since admin opened edit screen: "This grouping was modified by [Admin Name] at [Time]. Your changes will overwrite theirs. Continue?"

- **What happens when provider location is added or removed while regional groupings reference it?** System maintains location references even if provider deactivated (preserves configuration). If provider reactivates, location ordering still applies. If location permanently removed from system, admin sees warning in regional grouping edit screen: "[Location] is no longer active. Remove from ordering?"

- **How does system handle fallback pricing when no fallback is configured and currency conversion unavailable?** System displays location without starting price, shows generic text "Price available on request" to patient, and logs error for admin review. Admin sees warning in dashboard: "[Location] missing fallback pricing - patients seeing no price estimate."

- **What occurs if admin sets effective date for pricing but forgets to set expiry date?** Pricing remains active indefinitely until admin manually updates or sets expiry. System displays info note in pricing table: "No expiry set - pricing active indefinitely." No automatic expiration enforced.

---

## Functional Requirements Summary

### Core Requirements

- **REQ-028-001**: System MUST allow admins to create regional groupings by selecting group name, countries, and location presentation order
- **REQ-028-002**: System MUST allow admins to configure starting price estimates per location per currency
- **REQ-028-003**: System MUST apply regional grouping to patient destination list based on patient's location from profile or IP geolocation
- **REQ-028-004**: System MUST display starting prices in patient's preferred currency, falling back to location's default currency with conversion if specific currency not configured
- **REQ-028-005**: System MUST propagate configuration changes to patient-facing APIs within 1 minute via cache invalidation
- **REQ-028-006**: System MUST prevent overlapping regional groupings by enforcing one-to-one mapping between country and regional grouping at configuration time
- **REQ-028-007**: System MUST support fallback pricing for locations when patient's specific currency is not configured
- **REQ-028-008**: System MUST allow admins to preview how configurations will appear to patients from different regions before saving

### Data Requirements

- **REQ-028-009**: System MUST store regional grouping configuration with grouping name, country list, location ordering, and status (active/inactive)
- **REQ-028-010**: System MUST store starting price configuration with location, currency, amount, effective date, expiry date, and fallback flag
- **REQ-028-011**: System MUST maintain audit trail of all configuration changes with admin user, timestamp, change reason, and change details
- **REQ-028-012**: System MUST retain pricing history for 3 years for trend analysis and compliance audit

### Security & Privacy Requirements

- **REQ-028-013**: System MUST restrict regional configuration and pricing management to admin users with "System Configuration" role (per FR-031)
- **REQ-028-014**: System MUST log all configuration changes with admin user ID, timestamp, IP address, change reason, and full change details for audit trail
- **REQ-028-015**: System MUST validate all admin inputs server-side (country codes, currency codes, positive pricing amounts) to prevent invalid configurations
- **REQ-028-016**: System MUST rate-limit admin configuration API to 100 requests/minute per admin user to prevent abuse

### Integration Requirements

- **REQ-028-017**: System MUST integrate with FR-026 country list API for country selection in regional grouping configuration
- **REQ-028-018**: System MUST integrate with FR-029 currency API for currency validation and conversion rate retrieval
- **REQ-028-019**: System MUST provide REST API for patient apps to fetch regional configuration (location ordering + starting prices) based on patient location and currency
- **REQ-028-020**: System MUST expose admin configuration API for CRUD operations on regional groupings and starting prices with role-based access control

---

## Key Entities

- **Entity 1 - Regional Grouping**: Represents a logical grouping of patient countries with specific location presentation rules
  - **Key attributes**: grouping_id (PK), grouping_name, description, country_list (array), location_order (array), status (active/inactive), created_at, updated_at, created_by_admin_id, updated_by_admin_id
  - **Relationships**: One regional grouping has many countries (one-to-many); one regional grouping orders many locations (one-to-many); one admin user creates/updates many regional groupings (many-to-one)

- **Entity 2 - Location Starting Price**: Represents starting price estimate for a specific destination location in a specific currency
  - **Key attributes**: price_id (PK), location_id (FK), currency_code, starting_price_amount, is_fallback_price (boolean), effective_date, expiry_date, created_at, updated_at, updated_by_admin_id, change_reason
  - **Relationships**: One location has many starting prices (one per currency) (one-to-many); one currency is used for many location starting prices (one-to-many); one admin user updates many starting prices (many-to-one)

- **Entity 3 - Configuration Change Audit Log**: Tracks all changes to regional configuration and pricing for compliance and troubleshooting
  - **Key attributes**: audit_id (PK), entity_type (regional_grouping/starting_price), entity_id (FK), admin_user_id (FK), change_timestamp, change_reason, change_details (JSON with old_value/new_value), ip_address
  - **Relationships**: One audit log entry references one regional grouping or starting price (polymorphic FK); one admin user creates many audit log entries (many-to-one)

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-13 | 1.0 | Initial PRD creation from FR-028 system-prd.md and Hairline-AdminPlatformPart2.txt transcription | Claude (Sonnet 4.5) |
| 2025-12-16 | 1.1 | Verification updates: Constitution-compliant 10-year audit retention; resolved destination ordering with FR-003 (regional config + proximity fallback); removed overlapping grouping priority logic; required change reason for all config writes; updated status to Verified & Approved | Product Team |
| 2026-01-14 | 1.2 | Documentation alignment: Updated Currency Management navigation reference to live under Billing Settings (FR-029) | AI |

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
**Last Updated**: 2026-01-14
