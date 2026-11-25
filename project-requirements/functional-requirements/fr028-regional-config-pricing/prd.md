# FR-028 - Regional Configuration & Pricing

**Module**: A-09: System Settings & Configuration | P-02: Quote Request & Management | PR-02: Inquiry & Quote Management
**Feature Branch**: `fr028-regional-config-pricing`
**Created**: 2025-11-13
**Status**: ✅ Verified & Approved
**Source**: FR-028 from system-prd.md, Hairline-AdminPlatformPart2.txt transcription

---

## Executive Summary

The Regional Configuration & Pricing module enables Hairline administrators to control how treatment locations (countries) are presented to patients and set starting price estimates for different regions and currencies. This foundational configuration system directly influences the patient's initial experience when browsing treatment destinations and helps set appropriate pricing expectations based on their location and currency.

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

- Displays list of treatment destinations ordered by the patient's country, the first few shown and the rest behind "Show all destinations" (REQ-028-033, REQ-028-036)
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

- The save confirmation of any configuration change (grouping, starting price, default currency or system-wide default) is the on-screen message only; there is no separate notification (REQ-028-046)
- Configuration changes propagate to patient-facing APIs within 1 minute (cache refresh) (REQ-028-005)

**Out of Scope**:

- Patient notifications about pricing changes (handled by general notification system) (REQ-028-047)
- Provider notifications about regional configuration updates (providers unaffected by these settings) (REQ-028-047)
- Real-time pricing updates based on exchange rates (covered by FR-029: Payment System Configuration) (REQ-028-047)

### Entry Points

**Admin Entry Point**:

- Admin navigates to Settings > General Settings and opens the Location Presentation by Country tab, the Location Pricing tab or the Location Display Preview tab (Hairline app settings now live under General Settings) (REQ-028-049)
- The Location Display Preview tab is read-only and shows what a simulated patient country and currency will see from the saved configuration (Main Flow: Admin Previews Patient Location Display)
- Access requires the FR-031 permission "Manage App Data", which guards both regional groupings and starting prices (REQ-028-013)
- Configuration changes take effect immediately upon save (within 1-minute cache propagation)

**Patient Entry Point** (consumption only):

- Patient reaches "Choose Your Destination" screen during quote request flow (REQ-028-049)
- System reads the patient's country from the profile (required at registration) and matches it to a regional grouping (REQ-028-003)
- System applies appropriate regional configuration to order the destination list
- Starting prices are fetched and displayed in the patient's currency (REQ-028-004, REQ-028-038)

---

## Business Workflows

### Main Flow: Admin Configures Regional Location Presentation

**Actors**: Admin (with the "Manage App Data" permission, per FR-031)
**Trigger**: Admin wants to optimize location presentation for specific patient regions
**Outcome**: Regional grouping created with location ordering rules; changes visible to patients from target region within 1 minute

**Steps**:

1. Admin navigates to Settings > General Settings > Location Presentation by Country tab
2. Admin clicks "Add New Regional Grouping"
   - At the 51st active grouping the system warns that the limit of 50 is reached; the admin may continue; inactive and archived groupings do not count (REQ-028-030)
3. Admin enters grouping name (e.g., "Eastern Europe", "Middle East", "UK Only")
4. Admin selects countries that belong to this grouping from multi-select country list
   - System validates at least one country is selected
   - System blocks selection of countries that already exist in other active groupings and displays error: "Each country can only belong to one regional grouping. Remove it from the other grouping first." An inactive (archived) grouping does not hold its countries
5. Admin defines location presentation order for this grouping:
   - Drags and drops destination countries (countries from the FR-026 active country list; a country deactivated later stays in the order until an admin edits it, REQ-028-092) into preferred order
   - First position = shown first to patients, second position = shown second, etc.
   - Optionally sets how many destinations patients from this region see first (5 to 20, default 10); the rest sit behind "Show all destinations" (REQ-028-033)
   - System displays preview of how patients from this region will see destinations
6. Admin enters change reason (required)
7. Admin saves regional grouping
8. System validates configuration completeness, including change reason (10-500 chars)
9. System saves configuration to database
10. System clears location presentation cache
11. System displays success confirmation: "Regional grouping saved. Changes will be live for patients within 1 minute."
12. System logs configuration change in audit trail (REQ-028-014)
13. Admin can open the read-only "Change history" panel on this screen, which lists past grouping changes from the configuration change audit log with admin, time, change reason and old and new values (REQ-028-063, REQ-028-067)

### Alternative Flows

**A1: Admin Edits Existing Regional Grouping**:

- **Trigger**: Admin needs to update location ordering or country assignments for existing grouping
- **Steps**:
  1. Admin selects existing regional grouping from list
  2. System displays current configuration (countries, location order)
  3. Admin modifies countries or reorders destinations
     - System blocks removing a country from the grouping while a Stripe account is assigned to the grouping (FR-029); the screen names the account (REQ-028-091)
  4. Admin enters change reason (required)
  5. Admin saves changes
     - If another admin saved the same grouping since this admin opened it, the system warns "This grouping was modified by [Admin Name] at [Time]. Your changes will overwrite theirs. Continue?" (REQ-028-082)
  6. System validates, saves, clears cache, and confirms (same as main flow steps 8-12)
- **Outcome**: Regional grouping updated; patients from affected region see updated location ordering within 1 minute

**A2: Admin Deletes Regional Grouping**:

- **Trigger**: Admin needs to remove obsolete regional grouping
- **Steps**:
  1. Admin selects regional grouping to delete
  2. System displays warning: "Deleting this grouping will affect patients from [X countries]. They will fall back to proximity-based destination ordering. Continue?"
     - If a Stripe account is assigned to the grouping (FR-029), the deletion is blocked and the screen names the account (REQ-028-091)
  3. Admin enters change reason (required) and confirms deletion
  4. System archives grouping (soft delete), clears cache and logs the change in the audit trail (REQ-028-014)
  5. System displays confirmation: "Regional grouping archived. Patients from affected countries will now see proximity-based destination ordering."
- **Outcome**: Regional grouping archived (the same state as inactive, so its countries are released); patients from affected countries fall back to proximity-based ordering

**A7: Admin Sets a Regional Grouping Inactive or Back to Active**:

- **Trigger**: Admin wants to switch a grouping off without deleting it, or bring an inactive or archived grouping back
- **Steps**:
  1. Admin selects the grouping and switches its status to Inactive or back to Active
  2. When switching to Inactive, the system blocks the switch while a Stripe account is assigned to the grouping (FR-029); the screen names the account (REQ-028-091). When switching to Active, the system re-runs the one-country-one-grouping check and the unique grouping name check; the switch is blocked with the error of REQ-028-021 while a country of the grouping sits in another active grouping, and while another active grouping has the same name (REQ-028-025)
  3. Admin enters change reason (required)
  4. System saves the status, clears cache and logs the change in the audit trail
- **Outcome**: An inactive grouping is not applied to patients and releases its countries; an active grouping is applied again (REQ-028-029)

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

**Actors**: Admin (with the "Manage App Data" permission, per FR-031)
**Trigger**: Admin wants to set or update starting price estimates for treatment destinations
**Outcome**: Starting prices configured for destination per currency; prices visible to patients within 1 minute of save

**Steps**:

1. Admin navigates to Settings > General Settings > Location Pricing tab
   - Currency dropdown is populated from FR-029's supported currency list (Settings > Billing Settings > Currency Management)
2. Admin selects the destination country from the FR-026 active country list (e.g., Turkey, Poland, UK), the same key as treatment countries in an inquiry (REQ-028-086)
3. System displays current pricing configuration for selected location:
   - List of currencies with configured starting prices
   - Currencies without configured prices marked as "Not Set"
   - System shows the expiry banner and the missing-price banner for this tab (REQ-028-061, REQ-028-041)
4. Admin clicks "Add Currency" or "Edit" for existing currency
5. Admin selects currency from dropdown (GBP, EUR, USD, TRY, etc.)
6. Admin enters starting price amount for selected destination-currency combination
   - System validates amount is positive number
   - System displays format guidance: "Enter base starting price (e.g., 2500 for £2,500)"
   - System shows the entered amount formatted for its currency (for example £2,500) before the admin saves (REQ-028-008)
7. Admin optionally sets the price effective date and expiry date (dates are UTC and the expiry day is included). A future-dated change is saved as a new row for the same destination and currency; rows for the same destination and currency may not overlap in dates, so the new row ends the previous open row the day before its effective date (REQ-028-090)
8. Admin enters change reason (required)
9. Admin saves currency-price configuration
   - If another admin saved the same price since this admin opened it, the system warns "This price was modified by [Admin Name] at [Time]. Your changes will overwrite theirs. Continue?" (REQ-028-082)
10. System validates configuration:
    - Currency is supported (exists in system currency list)
    - Price is valid positive number
    - Decimal places match the currency's minor units in the FR-029 currency catalogue (REQ-028-055)
    - Expiry date, when set, is after the effective date
    - Change reason is present and within 10-500 chars
11. System saves pricing configuration to database and clears the location presentation cache (REQ-028-005)
12. System displays success confirmation: "Starting price for [Location] in [Currency] set to [Amount]."
13. System logs pricing change in audit trail (REQ-028-014)
14. Admin can open the read-only "Change history" panel on this screen, which lists past price, default currency and system-wide default changes from the configuration change audit log with admin, time, change reason and old and new values (REQ-028-063, REQ-028-067)

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
  7. System checks each fallback amount, decimals and currency as for any starting price (REQ-028-053, REQ-028-054, REQ-028-055), saves fallback configuration, clears cache and logs the change in the audit trail
  8. System confirms: "Fallback pricing enabled for [Location]. Patients from [Country] without specific pricing will see these prices."
- **Outcome**: Fallback pricing active; the fallback price shown to a patient is the one set for the patient's country, in the patient's currency (converted and marked approx. when the fallback row is in another currency, REQ-028-040)

**A4: Admin Bulk Updates Pricing Across Multiple Currencies**:

- **Trigger**: Admin needs to update pricing for all currencies proportionally (e.g., 10% increase across board)
- **Steps**:
  1. Admin selects destination location
  2. Admin clicks "Bulk Update Pricing"
  3. Admin selects update method (percentage increase/decrease or fixed amount adjustment)
  4. Admin enters adjustment value
  5. System displays preview of new prices for all currencies
  6. Admin enters change reason (required) and confirms or adjusts
  7. System checks every new price against the amount, decimals and currency rules (REQ-028-053, REQ-028-054, REQ-028-055); a bulk apply that would break them is blocked. Otherwise the system saves all currency price updates simultaneously, changing the row current today for each currency (REQ-028-090), clears cache and logs the change in the audit trail. If another admin saved one of the prices since the preview, the system gives the stale-edit warning (REQ-028-082)
  8. System confirms: "[X] currency prices updated for [Location]."
- **Outcome**: All currency prices for destination updated proportionally

**A8: Admin Sets the Default Currency of a Destination Location**:

- **Trigger**: Admin wants the destination's default currency to be used when a patient's currency has no price
- **Steps**:
  1. Admin selects the destination on the Location Pricing tab and opens its default currency setting
  2. Admin selects the location default currency from the FR-029 supported currency list; it is stored once for the destination, not on each price row (REQ-028-089)
  3. Admin enters change reason (required)
  4. System saves the default currency, clears cache, logs the change in the audit trail and shows an on-screen success message
- **Outcome**: The location default currency is set once per location

**A9: Admin Sets the System-Wide Default Starting Price**:

- **Trigger**: Admin wants one default starting price for patients whose country has no fallback price
- **Steps**:
  1. Admin opens the system-wide default starting price on the Location Pricing tab
  2. Admin enters the amount and selects its currency
  3. Admin enters change reason (required)
  4. System checks amount, decimals and currency as for any starting price, saves, clears cache, logs the change in the audit trail and shows an on-screen success message
- **Outcome**: The system-wide default starting price is available as a step of the price lookup chain (REQ-028-040, REQ-028-088)

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
**Outcome**: Patient sees location list ordered by their regional grouping, with appropriate starting prices in their currency

**Steps**:

1. Patient navigates to "Choose Your Destination" screen
2. System reads the patient's country from the profile (required at registration); there is no IP geolocation
3. System takes the profile country as the matching key
4. System queries active regional groupings to find the matching grouping for patient's country
5. System applies location presentation order from matched regional grouping
6. System lists destinations in configured order:
   - First location in regional config displayed first
   - Second location displayed second
   - Continue through configured order
   - Additional locations not in config appear at end ordered by proximity to the patient's country (REQ-028-036)
7. System applies the display cap: the first N destinations are shown first and the rest sit behind "Show all destinations", where N is the grouping's number of destinations shown (default 10 when the patient has no grouping) (REQ-028-033)
8. For each displayed location, system fetches starting price:
   - System identifies patient's currency: the profile preference, else the FR-029 system default currency; one currency for the whole list (REQ-028-038)
   - System follows the price lookup chain of REQ-028-040; the price is always shown in the patient's currency and a converted price is marked "approx."
9. System displays destination list to patient with:
   - Location name and flag
   - Starting price in patient's currency: "Starting from £2,500"
   - Brief location description
   - Provider count available in location (0 when the country has no provider; every active FR-026 country is listed, REQ-028-086)
10. Patient selects preferred destination(s) to proceed with quote request

**Alternative Flows**:

**A5: Patient's Location Not in Any Regional Grouping**:

- **Trigger**: Patient's country is not assigned to any regional grouping
- **Steps**:
  1. System detects no matching regional grouping
  2. System falls back to proximity-based location ordering from a fixed country-to-country distance table kept in the product code (REQ-028-035)
  3. System displays all destinations (every active FR-026 country) in default order, the first 10 first and the rest behind "Show all destinations" (REQ-028-033)
  4. Starting prices displayed by the price lookup chain of REQ-028-040
- **Outcome**: Patient sees destinations in default order with appropriate pricing

**A6: Patient's Currency Not Configured for Selected Location**:

- **Trigger**: Patient views location that doesn't have pricing configured for their currency
- **Steps**:
  1. System detects missing currency-specific pricing
  2. System checks for fallback pricing for the patient's country; a fallback row already in the patient's currency is preferred; when none is, the row in the location's default currency is used, else the row in the FR-029 system default currency, else the earliest created
  3. If fallback exists, display fallback price (converted and marked approx. when it is in another currency)
  4. If no fallback, display the system-wide default starting price (if an admin has set one; converted and marked approx. when it is in another currency)
  5. If there is no system-wide default, display the price in the location's default currency converted to the patient's currency and marked approx.: "Starting from approx. £2,500"
  6. Conversion uses the admin-configured conversion rate with markup from FR-029; a step whose price cannot be shown (no conversion rate, or no price row in that currency) passes to the next step of the chain (REQ-028-040)
  7. If the last step also fails (no price in the location's default currency, or no conversion rate), no price can be shown and the location shows "Price available on request" and the system logs an error for admin review (REQ-028-041)
- **Outcome**: Patient sees a price in their own currency, marked approx. when converted, or "Price available on request"

### Main Flow: Admin Previews Patient Location Display

**Actors**: Admin (with the "Manage App Data" permission, per FR-031)
**Trigger**: Admin wants to check what patients from a given country and currency will see
**Outcome**: Admin sees the grouping, destination order and prices applied for the simulated patient from the saved configuration, without changing anything

**Steps**:

1. Admin opens the Location Display Preview tab in Settings > General Settings
2. Admin selects the simulated patient country and currency; the currency defaults to the FR-029 system default currency (REQ-028-075)
3. System shows the matched regional grouping, the destination order, the starting prices with fallback indicators and the provider counts for the simulated patient (REQ-028-070, REQ-028-071, REQ-028-073)
4. Admin changes the country or currency, or refreshes, and the preview updates (REQ-028-069, REQ-028-074)
- **Outcome**: The preview never changes configuration and shows saved configuration only; unsaved changes are previewed in the Screen 1 preview pane and the Screen 2 formatted amount (REQ-028-008)

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
| Location Order | Drag-and-drop list | Yes | Ordered list of destination countries from the FR-026 active country list | At least 1 location must be ordered (REQ-028-023) | ENT-regional-grouping.location_order |
| Locations Displayed | Number | No | How many destinations patients from this grouping see first; the rest sit behind "Show all destinations" | Whole number from 5 to 20; default 10; otherwise the error "Destinations shown first must be a whole number from 5 to 20." (REQ-028-033) | ENT-regional-grouping.locations_displayed |
| Status | Toggle | Yes | Active/Inactive status | Active = applies to patients, Inactive = archived (one state) and releases its countries, and is blocked while a Stripe account is assigned (REQ-028-091); switching back to Active re-runs the country and name checks (REQ-028-029) | ENT-regional-grouping.status |
| Change Reason | Text | Yes | Reason for grouping change (create/update/archive) | 10-500 chars | ENT-configuration-change-audit-log.change_reason |
| Created Date | Date (read-only) | - | When grouping was created | Auto-generated | ENT-regional-grouping.created_at |
| Last Modified | Date (read-only) | - | When grouping was last updated | Auto-updated on save | ENT-regional-grouping.updated_at |
| Modified By | Text (read-only) | - | Admin user who last modified | Auto-populated | ENT-regional-grouping.updated_by_admin_id |
| Change History | Display (read-only) | - | Panel listing past grouping changes from the configuration change audit log: admin, time, change reason and old and new values (REQ-028-063) | - | ENT-configuration-change-audit-log.change_details |

**Business Rules**:

- **Unique Membership**: Each country can only belong to one active regional grouping at a time. If admin attempts to add a country that already exists in another active grouping, system blocks save and shows error with list of conflicting groupings. (REQ-028-006, REQ-028-021)
- **Default Fallback**: If no regional grouping matches, system orders destinations by proximity to the patient's country (REQ-028-035)
- **Cache Propagation**: See REQ-028-005.
- **Audit Trail**: See REQ-028-014.
- **Soft Delete**: Deleted groupings are archived, not permanently deleted, for audit trail purposes (REQ-028-028)
- **Stale Edit**: If another admin saved the grouping since this admin opened it, the system warns before the save (REQ-028-082)

**Notes**:

- Provide drag-and-drop interface for location ordering (intuitive reordering) (REQ-028-076)
- Display preview pane showing how patients from selected countries will see location list as the admin edits, before saving (REQ-028-076, REQ-028-008)
- Show country flags next to country names for visual clarity (REQ-028-076)
- Disable selection state or visually indicate countries already assigned to another grouping (e.g., greyed out with tooltip "Already assigned to [Grouping Name]") (REQ-028-076)
- Provide bulk actions: duplicate grouping, export configuration, import from template (REQ-028-077)

---

### Screen 2: Location Pricing Configuration (Admin)

**Purpose**: Allow admins to configure starting price estimates for each treatment destination per currency

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Destination Location | Select | Yes | Treatment destination: a country from the FR-026 active country list, the same key as treatment countries in an inquiry | Must be an active country in FR-026 when newly selected; an existing row of a deactivated country can still be saved (REQ-028-086, REQ-028-092) | ENT-location-starting-price.location_id |
| Location Default Currency | Select | No | Default currency for the selected destination; used when a patient's currency has no price and a converted price is shown | Must be supported currency; stored once per destination, not on each price row (REQ-028-089) | ENT-pricing-default.currency_code |
| Currency | Select | Yes | Currency for pricing (GBP, EUR, USD, etc.) | Must be supported currency | ENT-location-starting-price.currency_code |
| Starting Price | Number | Yes | Base starting price estimate | Positive number, decimals per the currency's minor units in the FR-029 currency catalogue (REQ-028-055) | ENT-location-starting-price.starting_price_amount |
| Price Effective Date | Date | No | When this pricing becomes active | Future date optional, defaults to immediate; UTC (REQ-028-090) | ENT-location-starting-price.effective_date |
| Price Expiry Date | Date | No | When this pricing expires | Must be after effective date if set; UTC, the expiry day is included (REQ-028-090) | ENT-location-starting-price.expiry_date |
| Bulk Update Pricing | Button/Action | No | Opens bulk update modal (percentage or fixed adjustment across all currencies for selected destination) | Visible on the pricing screen; enabled only when a destination is selected or at least one pricing row is checked; requires change reason inside modal before apply (REQ-028-059) | no graph field (control) |
| Fallback Price | Checkbox | No | Use as fallback for unconfigured patient locations (REQ-028-056) | - | ENT-location-starting-price.is_fallback_price |
| Fallback Patient Country | Select | Yes when Fallback Price is checked | Patient country this fallback price is shown to | Must be a valid country in system | ENT-location-starting-price.country_code |
| System-Wide Default Starting Price | Number and currency | No | One default starting price (one amount and its currency) shown when no specific or fallback price applies; before any converted price is used | Positive number, decimals per the FR-029 currency catalogue; empty until an admin sets it; change reason required to save; stored with its amount and currency (REQ-028-088) | ENT-pricing-default.amount |
| Last Updated | Date (read-only) | - | When price was last changed | Auto-updated | ENT-location-starting-price.updated_at |
| Updated By | Text (read-only) | - | Admin who updated price | Auto-populated | ENT-location-starting-price.updated_by_admin_id |
| Change Reason | Text | Yes | Reason for price change (for audit) | 10-500 chars | ENT-location-starting-price.change_reason |
| Change History | Display (read-only) | - | Panel listing past price, default currency and system-wide default changes from the configuration change audit log: admin, time, change reason and old and new values (REQ-028-063) | - | ENT-configuration-change-audit-log.change_details |

**Business Rules**:

- **Currency Validation**: Only supported currencies (configured in system) can be selected (REQ-028-053)
- **Decimal Precision**: System enforces the decimal places of the currency's minor units in the FR-029 currency catalogue (REQ-028-055)
- **Positive Values Only**: Starting prices must be positive numbers greater than 0 (REQ-028-054)
- **Fallback Priority**: The price lookup chain is stated once in REQ-028-040
- **Price Expiry**: After a starting price's expiry date passes, patients no longer see it and the next step of the lookup chain applies. A price with no expiry date stays active until an admin changes it (REQ-028-087)
- **Price History**: Price history is read from the configuration change audit log and shown in the read-only Change history panel of this screen (REQ-028-063)
- **Bulk Update**: Admins can apply percentage or fixed adjustments to multiple currency prices simultaneously through the bulk update modal (no CSV import or export) (REQ-028-057)
- **Preview Before Saving**: The entered amount shows formatted for its currency before the admin saves; how patients see saved prices is simulated on Screen 3 (REQ-028-008)
- **Effective Dating**: A future-dated change is a new row for the same destination and currency; rows for the same destination and currency (and patient country on a fallback row) may not overlap in dates; the lookup uses the row whose window contains the current day (REQ-028-060, REQ-028-090)
- **Expiry Warning**: A banner on this screen warns the admin 7 days before a price expiry date (REQ-028-061)
- **Missing Price Warning**: A banner on this screen names destinations whose patients see no price estimate (REQ-028-041)
- **Stale Edit**: If another admin saved the same price since this admin opened it, or since the bulk update preview, the system warns before the save (REQ-028-082)

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

**Purpose**: Allow admins to preview how location recommendations will appear to patients from different regions, from saved configuration

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Preview Patient Location | Select | Yes | Patient country to simulate | Must be valid country in system | ENT-regional-grouping.country_list |
| Preview Currency | Select | Yes | Patient currency preference | Defaults to the FR-029 system default currency (REQ-028-075) | ENT-location-starting-price.currency_code |
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
- Screen 3 shows saved configuration only; unsaved changes are previewed in the Screen 1 preview pane and the Screen 2 formatted amount (REQ-028-008)
- Display cache status indicator: shows when patient-facing data was last refreshed (REQ-028-081)

---

## Business Rules

### General Module Rules

- **Rule 1**: Active regional groupings MUST NOT overlap - each country can belong to at most one active grouping at a time. System enforces uniqueness and blocks saves that would assign a country to multiple active groupings. (REQ-028-006)
- **Rule 2**: Location ordering is strictly advisory for patient presentation - it does not restrict which locations patients can select or providers can serve. (REQ-028-042)
- **Rule 3**: Starting prices are estimates only and do not constrain provider quote pricing. Providers can quote higher or lower than starting prices. (REQ-028-043)
- **Rule 4**: All configuration changes propagate to patient-facing APIs within 1 minute via cache invalidation (cache TTL = 60 seconds). (REQ-028-005)
- **Rule 5**: At the 51st active regional grouping the Admin gets a warning and may continue; inactive and archived groupings do not count; the number 50 is fixed in code. (REQ-028-030)
- **Rule 6**: Inactive and archived regional groupings are one state: retained in system, not applied to patient location presentation, and their countries are released to other groupings. Switching back to Active re-runs the country and unique name checks. (REQ-028-029)
- **Rule 7**: All create/update/archive actions require a change reason (10-500 chars) (REQ-028-024)
- **Rule 8**: Setting a regional grouping Inactive, archiving it or removing a country from it is blocked while a Stripe account is assigned to it (FR-029); the screen names the account. (REQ-028-091)
- **Rule 9**: A country deactivated in FR-026 keeps applying in regional groupings and starting prices (destination rows and fallback rows) until an Admin edits them; the active check runs only when a country is newly selected, so an existing grouping or row of a deactivated country can still be saved, for example to set an expiry date. FR-026 warns before the deactivation and lists the regional groupings and fallback price rows that use the country (REQ-026-129). (REQ-028-092)
- **Error handling**: If regional configuration unavailable, fall back to default location ordering and "Price available on request" (REQ-028-085)
- **Error handling**: If country list unavailable, use cached country list (refreshed daily)

### Data & Privacy Rules

- **Privacy Rule 1**: Patient location data used for regional matching is stored in patient profile (already compliant with PHI encryption requirements per Principle II) (REQ-028-065)
- **Privacy Rule 2**: Starting price estimates are public data and not subject to encryption requirements (REQ-028-066)
- **Privacy Rule 3**: Pricing history includes admin user who made changes for accountability, but not patient-level pricing data (REQ-028-067)
- **Audit Rule**: All configuration changes (regional groupings, location ordering, starting prices, default currencies, the system-wide default price) are logged with admin user ID, timestamp, IP address, change reason, and full change details (old value to new value) (REQ-028-014)
- **Retention Rule**: Pricing history and configuration change audit logs are kept; retention follows the system PRD, Platform-Wide Rules: One 10-year retention period (REQ-028-064)
- **GDPR Compliance**: Patient location data handling follows existing GDPR requirements from FR-001 (no additional requirements) (REQ-028-068)
- **Data Protection**: Regional configuration data is not sensitive (public pricing estimates, location display rules) - no encryption at rest required (REQ-028-066)

### Admin Editability Rules

**Editable by Admin** (REQ-028-032):

- Regional grouping names, countries, and location ordering (full control)
- Starting price amounts for any location-currency combination
- Fallback pricing configuration per location
- Regional grouping active/inactive status
- Price effective dates and expiry dates
- Number of destinations displayed first per regional grouping (default 10, configurable range 5-20) (REQ-028-033)
- Location default currency per destination, and the system-wide default starting price (REQ-028-088, REQ-028-089)

**Fixed in Codebase (Not Editable)** (REQ-028-031):

- Cache propagation timing (1-minute TTL fixed for performance/consistency balance)
- Country-to-country distance table used for proximity ordering (kept in the product code, REQ-028-035)
- Maximum regional groupings limit (50 active groupings; the 51st triggers a warning)

**Configurable with Restrictions**:

- Fallback location ordering (when no regional grouping matches) is by proximity to the patient's country; there is no separate admin-editable default ordering list
- Currency support requires system-level configuration in FR-029 before location pricing can be configured (REQ-028-052)

### Payment & Billing Rules

- Not applicable to this module - FR-028 configures pricing display only, not actual payment processing (REQ-028-048)

**Carried from dropped sections (original wording)**:

- **None**: This module does not integrate with external services. Currency conversion rates are provided internally by FR-029.
- **Integration 1: Patient API to Regional Configuration Service**
- **Authentication**: Internal service-to-service authentication (OAuth2 client credentials)
- **Integration 2: Admin UI to Regional Configuration API**
- **Error handling**: Validation errors returned with specific field-level error messages; retry with exponential backoff on server errors
- **Integration 3: Regional Configuration Service to FR-026 Country List**
- **Authentication**: Internal service-to-service authentication
- **Cache Poisoning Protection**: Cache keys include version hash to prevent stale data serving after configuration changes

---

## Dependencies

- **FR-026 / Module A-09 (App Settings & Security Policies)**: Regional configuration requires FR-026's centralized country list; a destination is a country from the FR-026 active country list, the same key as the inquiry's treatment countries (FR-003). A country deactivated there keeps applying in groupings and starting prices here until an Admin edits it (REQ-028-092)
- **FR-001 / Module P-01 (Auth & Profile Management)**: The patient's country in the profile (required at registration) is the key that matches a regional grouping
- **FR-003 / Module P-02 (Inquiry Submission & Distribution)**: Inquiry flow consumes regional configuration for location presentation
- **FR-029 / Module S-02 (Payment System Configuration)**: Supplies currency conversion rates, the supported currency list with minor units, and the system default currency. FR-029 also consumes FR-028 regional groupings: a Stripe account assigned to a grouping blocks setting the grouping Inactive, archiving it or removing a country from it (REQ-028-091)
- **FR-031 / Module A-09 (Admin Access Control)**: The permission "Manage App Data" guards both regional groupings and starting prices

---

## User Scenarios & Testing

### User Story 1 - Admin Creates Regional Grouping for UK Patients (Priority: P1)

**Description**: As a Hairline admin, I need to configure location recommendations for UK patients so they see Turkey first (most popular), then Poland, then UK domestic options, maximizing conversion rates and matching patient travel preferences.

**Why this priority**: This is the most critical workflow - without regional groupings, all patients see the same generic location list. Properly configured regional groupings directly impact quote request conversion rates and patient decision time. UK is the primary launch market, making this P1 essential functionality.

**Independent Test**: Create a regional grouping "UK" with Turkey first, Poland second, UK third. Verify configuration saves successfully, then simulate a UK patient viewing destination list to confirm locations appear in configured order with appropriate starting prices.

**Acceptance Scenarios**:

1. **Given** admin is logged in with the Manage App Data permission, **When** admin navigates to Settings > General Settings > Location Presentation by Country tab, **Then** admin sees list of existing regional groupings and "Add New Regional Grouping" button
2. **Given** admin clicks "Add New Regional Grouping", **When** admin enters name "UK", selects "United Kingdom" from country list, and orders locations (Turkey 1st, Poland 2nd, UK 3rd), **Then** system displays preview showing UK patients will see Turkey first
3. **Given** admin has configured regional grouping with valid data, **When** admin clicks "Save", **Then** system validates configuration, saves to database, clears cache, and displays confirmation "Regional grouping saved. Changes will be live within 1 minute."
4. **Given** regional grouping has been saved for 60+ seconds, **When** UK patient reaches destination selection screen, **Then** patient sees Turkey as first location option, Poland as second, UK as third (matching configured order)
5. **Given** admin has created regional grouping, **When** admin opens the Change history panel on the same tab, **Then** the panel shows the configuration change with admin username, timestamp, and details (countries added, location order)

---

### User Story 2 - Admin Configures Starting Prices for Turkey in Multiple Currencies (Priority: P1)

**Description**: As a Hairline admin, I need to set starting price estimates for Turkey in GBP (£2,500), EUR (€2,800), and USD ($3,200) so patients from UK, Europe, and US see realistic pricing expectations in their local currency, improving quote acceptance rates.

**Why this priority**: Accurate starting prices are essential for setting patient expectations and reducing "price shock" when quotes arrive. Turkey is the most popular destination, and these three currencies cover 80% of initial target markets. Without currency-specific pricing, conversion rates suffer significantly.

**Independent Test**: Configure starting prices for Turkey in GBP, EUR, and USD. Verify prices save correctly, then simulate patients from UK, Germany, and US viewing Turkey destination to confirm appropriate currency and price displays.

**Acceptance Scenarios**:

1. **Given** admin is logged in with the Manage App Data permission, **When** admin navigates to Settings > General Settings > Location Pricing tab and selects "Turkey", **Then** admin sees pricing table with currencies as columns and current configured prices
2. **Given** admin clicks "Add Currency" for Turkey, **When** admin selects "GBP" and enters "2500", **Then** system validates amount is positive number, displays formatted price "£2,500" in preview, and enables save
3. **Given** admin has entered valid prices for GBP, EUR, and USD for Turkey, **When** admin clicks "Save", **Then** system saves all three currency prices, displays confirmation "Starting prices for Turkey updated for 3 currencies", and logs changes in audit trail
4. **Given** starting prices have been configured for Turkey, **When** UK patient (location=UK, currency=GBP) views destination list, **Then** patient sees Turkey with starting price "Starting from £2,500"
5. **Given** starting prices have been configured for Turkey, **When** German patient (location=Germany, currency=EUR) views destination list, **Then** patient sees Turkey with starting price "Starting from €2,800"

---

### User Story 3 - Patient from Unconfigured Region Sees Fallback Pricing (Priority: P2)

**Description**: As a patient from Australia (region without configured pricing), I need to see reasonable starting price estimates in my local currency (AUD) so I can make informed decisions about treatment destinations, even though my specific region hasn't been configured yet.

**Why this priority**: While P2 (not as critical as core regional configuration), this ensures platform gracefully handles patients from regions admins haven't configured yet. This becomes more important as platform expands globally. Without fallback pricing, patients from unconfigured regions see no pricing or confusing currency conversions, hurting conversion rates.

**Independent Test**: Configure fallback pricing for Turkey in USD for patients from Australia. Simulate Australian patient (no regional grouping, no AUD pricing configured) viewing Turkey. Verify patient sees the fallback USD price converted to AUD and marked approx.

**Acceptance Scenarios**:

1. **Given** admin has configured fallback pricing for Turkey in USD at $3,200 for patients from Australia, **When** Australian patient (no regional grouping, currency preference=AUD) views Turkey destination, **Then** patient sees "Starting from approx. A$4,800", the USD fallback converted to AUD and marked approx.
2. **Given** patient is from unconfigured region, **When** patient views destination list, **Then** patient sees locations ordered by proximity to the patient's country (REQ-028-035)
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

**Description**: As a Hairline admin, I need to see how regional grouping and pricing changes will appear to patients before saving them (the Screen 1 preview pane and the Screen 2 formatted amount) and how saved configuration appears to patients from different regions (Screen 3), so I can verify configurations are correct and avoid publishing errors to production.

**Why this priority**: P3 because preview is a quality-of-life feature for admins, not essential functionality. Admins can test configurations by saving and checking patient app directly, but preview improves admin confidence and reduces configuration errors. More valuable as system complexity grows.

**Independent Test**: Edit a regional grouping without saving and verify the Screen 1 preview pane updates in real time. Save it, open the Location Display Preview tab, select different patient countries and verify the preview shows the saved configuration.

**Acceptance Scenarios**:

1. **Given** admin is editing a regional grouping (unsaved changes), **When** admin reorders locations (e.g., moves Poland to 1st position), **Then** the preview pane on the same screen updates in real time to show Poland first for the selected patient countries
2. **Given** admin is entering a starting price (unsaved), **When** admin types the amount, **Then** Screen 2 shows the amount formatted for its currency before saving
3. **Given** configuration has been saved, **When** admin opens the Location Display Preview tab and selects a UK patient, **Then** admin sees the location ordering and pricing as a UK patient would see them from the saved configuration; changing the selection to "Germany" refreshes the preview (a different regional grouping may apply)
4. **Given** admin has just saved a change, **When** admin refreshes the Location Display Preview tab, **Then** the preview shows the saved configuration; the tab never shows unsaved changes

---

### Edge Cases

- **What happens when admin tries to assign a country to more than one regional grouping?** System blocks the change, shows error listing conflicting groupings, and requires admin to resolve by keeping the country in only one grouping. (REQ-028-021)

- **How does system handle location with no pricing configured for patient's currency?** System follows the price lookup chain of REQ-028-040: the fallback price for the patient's country, then the system-wide default starting price, then the location's default currency price; a step whose price cannot be shown (no conversion rate, or no price row in that currency) passes to the next step; a price in another currency is converted using the admin-configured conversion rate with markup (from FR-029) and shown in the patient's currency marked approx. ("Starting from approx. £2,500"). (REQ-028-040)

- **What occurs if admin deletes a regional grouping while patients are actively viewing destinations using that grouping?** Cached data serves existing sessions for up to 60 seconds (cache TTL). After cache expiration, patients see default location ordering. No errors displayed to patients - graceful degradation. (REQ-028-027, REQ-028-084)

- **How to manage concurrent admin edits to the same regional grouping, price row or bulk apply?** If another admin saved the same data since this admin opened it (or since the bulk update preview), the second save gets the warning "This [grouping or price] was modified by [Admin Name] at [Time]. Your changes will overwrite theirs. Continue?" and goes through only when the admin confirms. (REQ-028-082)

- **What happens when a country is deactivated in FR-026 while a regional grouping or price row references it?** The grouping and price rows keep applying until an admin edits them, and nothing is forced. The grouping edit screen warns "[Country] is deactivated. Remove from ordering?". An existing grouping or row of a deactivated country can still be saved, for example to set an expiry date; only a newly selected country must be active. FR-026 also warns the admin before the deactivation and lists the groupings and price rows that use the country (REQ-026-129). (REQ-028-083, REQ-028-092)

- **What happens when no step of the price lookup chain can show a price?** System displays location without starting price, shows generic text "Price available on request" to patient, and logs error for admin review. Screen 2 shows a banner: "[Location] missing fallback pricing - patients seeing no price estimate." (REQ-028-041)

- **What occurs if admin sets effective date for pricing but forgets to set expiry date?** Pricing remains active indefinitely until admin manually updates or sets expiry. System displays info note in pricing table: "No expiry set - pricing active indefinitely." No automatic expiration enforced. (When an expiry date is set and has passed, the price stops showing and the next step of the lookup chain shows instead.) (REQ-028-062)

---

## Functional Requirements Summary

### Core Requirements

- **REQ-028-001**: System MUST allow admins to create regional groupings by selecting group name, countries, and location presentation order
- **REQ-028-002**: System MUST allow admins to configure starting price estimates per location per currency
- **REQ-028-003**: System MUST apply regional grouping to the patient destination list based on the patient's country in the profile
- **REQ-028-004**: System MUST display starting prices in the patient's currency; where that currency has no price for the location, the lookup chain of REQ-028-040 applies
- **REQ-028-005**: System MUST propagate configuration changes to patient-facing APIs within 1 minute via cache invalidation
- **REQ-028-006**: System MUST prevent overlapping regional groupings by enforcing one-to-one mapping between country and active regional grouping at configuration time
- **REQ-028-007**: System MUST support fallback pricing for locations when patient's specific currency is not configured; the fallback price is chosen by the patient's country
- **REQ-028-008**: System MUST let admins preview configuration before saving (the Screen 1 preview pane for a grouping and the formatted amount on Screen 2 for a price); the Location Display Preview tab simulates saved configuration only
- **REQ-028-087**: After a starting price's expiry date has passed, patients MUST no longer see that price; the next step of the lookup chain (REQ-028-040) applies. Prices with no expiry date stay active until an admin changes them
- **REQ-028-088**: System MUST provide one system-wide default starting price, stored with its amount and currency, set by admins on the pricing screen; it is empty until an admin sets it
- **REQ-028-089**: System MUST let admins set a default currency for each destination location; it is stored once per destination, not on each price row
- **REQ-028-090**: A future-dated price change MUST be saved as a new row for the same destination and currency; the lookup picks the row whose window contains the current day, dates are UTC and the expiry day is included, and price history is read from the configuration change audit log. Rows for the same destination and currency (and patient country on a fallback row) MUST NOT overlap in dates: a new dated row ends the previous open row the day before its effective date, and a bulk update changes the row current today
- **REQ-028-091**: Setting a regional grouping Inactive, archiving it, or removing a country from it, MUST be blocked while a Stripe account is assigned to the grouping (FR-029), and the screen names the account
- **REQ-028-092**: A country deactivated in FR-026 MUST keep applying in regional groupings and starting prices (destination rows and fallback rows) until an admin edits them; the active check runs only when a country is newly selected, so an existing grouping or row of a deactivated country can still be saved, for example to set an expiry date; FR-026 warns before the deactivation and lists the regional groupings and fallback price rows that use the country (REQ-026-129)

### Data Requirements

- **REQ-028-009**: System MUST store regional grouping configuration with grouping name, country list, location ordering, number of destinations shown first, and status (active/inactive)
- **REQ-028-010**: System MUST store starting price configuration with location, currency, amount, effective date, expiry date, fallback flag, and (for a fallback price) the patient country it applies to

### Security & Privacy Requirements

- **REQ-028-013**: System MUST restrict regional configuration and pricing management to admin users with the FR-031 permission "Manage App Data"
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
| 2026-11-23 | 1.6 | Independent compression review: 10 clause(s) from dropped sections restored in original wording under Business Rules. No rule changes. | Product Team |
| 2026-11-24 | 1.61 | Logic review corrections: one price lookup chain in the patient's currency with approx. marking and a "Price available on request" end; destination cap becomes a display cap with "Show all destinations"; number of destinations shown first is a grouping field; Manage App Data permission; inactive and archived groupings are one state that releases countries; 51st-grouping warning; destinations are FR-026 active countries; profile country is the matching key (no IP geolocation); fixed distance table for proximity ordering; preview entry point and flow; effective and expiry dates, location default currency and system-wide default price flows; dated rows and UTC dates; audit and cache-clear on every save; save confirmation is on-screen only; admin screens belong to the configuration stage; Stripe-assigned groupings cannot be archived or lose a country; deactivated countries keep applying until edited; stale-edit warning covers prices and bulk apply; decimals come from the FR-029 currency catalogue; audit rules merged into REQ-028-014. | Product Team |
| 2026-11-24 | 1.62 | Final logic review corrections: setting a Stripe-assigned grouping Inactive is blocked like archiving it; a price lookup step that cannot show a price passes to the next step; price rows may not overlap in dates and the fallback tie-break is stated; deactivated countries keep applying in groupings and all starting-price rows and can still be saved; the Screen 2 banners are shown when the tab opens; read-only Change history panels on Screens 1 and 2; Screen 3 simulates saved configuration only; destination default currency and system-wide default price have a stored home; every active country is a destination (provider count 0 where none); the deactivated-country warning replaces the provider-location warning; patient currency is the profile preference, else the FR-029 system default currency; error text for destinations shown first; unique name check on reactivation; only active groupings count toward the 51st-grouping warning. | Product Team |
| 2026-11-25 | 1.63 | Cross-FR alignment: the unset-price and missing-region cases point to the FR-026 warning (REQ-026-129) in Rule 9, REQ-028-083 and REQ-028-092. | Product Owner / Documentation |

---

## Appendix: Approvals

Approved by the Product Owner as part of the requirements baseline of 2026-11-25. Record: `project-requirements/baseline-sign-off.md`. Changes after that date are listed in the Change Log above.

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-011 Aftercare & Recovery Management PRD
**Last Updated**: 2026-11-25
