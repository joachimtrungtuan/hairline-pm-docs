# FR-024 - Treatment & Package Management

**Module**: A-09: System Settings & Configuration | PR-06: Profile & Settings Management
**Feature Branch**: `fr024-treatment-package-management`
**Created**: 2025-11-12
**Status**: 🟡 Revised — Pending Consolidated Verification
**Source**: FR-024 from system-prd.md
**Change Request**: [CR-FR024-20261016-01 — MTG-002 quote model alignment](change-request-2026-10-16-mtg002-quote-model-alignment.md)

---

## Executive Summary

The Treatment & Package Management module establishes a two-tier content management system for medical procedures and service packages within the Hairline platform. This module defines clear content ownership boundaries: treatments (FUE, FUT, DHI, etc.) are centrally managed by admins to ensure consistency across all providers, while packages (reusable quote templates that preset the included services and their prices, flight, hotel, transport, and other travel services, and a relative-day treatment plan) are managed by individual providers to enable competitive differentiation. This separation creates a foundation for quote generation while providing flexibility for future platform-managed services.

This module directly impacts provider quote submission capabilities and ensures patients receive consistent treatment information regardless of which provider they choose. The architectural decision to separate treatments from packages supports the platform's long-term vision of transitioning provider-managed travel services to platform-managed services without disrupting the treatment catalog.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-02)**: Views treatment information and package details within provider quotes
- **Provider Platform (PR-06)**: Manages their own packages and selects from admin-created treatments when building quotes
- **Admin Platform (A-09)**: Creates and manages the master treatment catalog available to all providers
- **Shared Services (S-05)**: Media storage and CDN delivery for treatment/package assets

### Multi-Tenant Breakdown

**Patient Platform (P-02: Quote Request & Management)**:

- Patients view treatment details (videos, descriptions, technique information) within provider quotes
- Patients see each provider's package-based quote options as alternatives, shown from the quote's own copy of the package
- Patients compare treatment and package offerings across multiple provider quotes
- No direct treatment or package management actions available to patients

**Provider Platform (PR-06: Profile & Settings Management)**:

- Providers access the admin-created treatment catalog
- Providers cannot create custom treatments (ensures standardization)
- Providers configure pricing for each treatment type they offer
- Providers create and manage their own package catalog
- Providers build each package as a full quote template: included services with their prices, flight, hotel, transport, and other travel services, and a day-by-day relative treatment plan
- Providers set a standard price and an Active or Inactive status for each package
- Providers can enable/disable treatments and packages without deleting them
- Providers select one treatment per quote and one to five packages; each selected package seeds one alternative quote option in FR-004

**Admin Platform (A-09: System Settings & Configuration)**:

- Admins create and manage the master treatment catalog
- Admins define treatment types: FUE, FUT, DHI, Sapphire FUE, Robotic, etc.
- Admins upload treatment videos, images, and detailed descriptions
- Admins document technique specifications for each treatment
- Admins can activate/deactivate treatments globally
- Admins have read-only view of provider packages (for support purposes)
- Admins cannot modify individual provider packages

**Shared Services (S-XX)**:

- S-05: Media Storage Service handles treatment videos, images, and package assets
- All media files uploaded for treatments and packages stored securely with CDN delivery

### Communication Structure

**In Scope**:

- System notifications when admin adds new treatments to catalog (providers notified)
- System notifications when admin deactivates treatments (providers with active usage notified)
- Provider receives confirmation when packages are successfully created/updated

**Out of Scope**:

- Direct messaging between admins and providers about treatment content (handled by A-10: Communication Monitoring & Support)
- Patient inquiries about treatments or packages (handled by P-06: Communication)
- Marketing communications about new treatments (handled by S-03: Notification Service with A-06: Discount & Promotion Management)

### Entry Points

**Admin Entry Points**:

- Admin navigates to "Settings > Treatment Settings" in admin platform
- Admin selects "Create New Treatment" to add treatment type
- Admin edits existing treatment by selecting from treatment list

**Provider Entry Points**:

- Provider navigates to "Products & Services > Treatments" in provider platform
- Provider accesses "Treatment Pricing" to configure pricing for admin-created treatments
- Provider navigates to "Products & Services > Packages" to manage their package catalog
- Provider selects "Create Package" to add new package offering
- During quote creation, provider selects a treatment and one to five Active packages

**Patient Entry Points** (View-Only):

- Patient views treatment details when reviewing provider quotes
- Patient sees package options within quote comparison interface
- No direct management access for patients

---

## Business Workflows

### Main Flow: Admin Creates Treatment

**Actors**: Admin, System, Providers (notified)
**Trigger**: Admin decides to add a new treatment type to the platform catalog
**Outcome**: New treatment available for all providers to offer and configure pricing

**Steps**:

1. Admin navigates to "Settings > Treatment Settings" in admin platform
2. Admin clicks "Create New Treatment" button
3. System displays treatment creation form
4. Admin enters treatment details:
   - Treatment name (e.g., "FUE - Follicular Unit Extraction")
   - Treatment type selection (FUE, FUT, DHI, Sapphire FUE, Robotic, Other)
   - Detailed description (markdown supported)
   - Technique specifications (extraction method, implantation method, anesthesia type)
   - Expected recovery time
   - Typical duration (hours)
5. Admin uploads treatment video (optional, MP4 format, max 50MB)
6. Admin uploads treatment images (optional, JPEG/PNG, max 5 images, 5MB each)
7. Admin uploads educational resources (optional, PDF documents)
8. Admin sets treatment status: "Active" or "Inactive"
9. Admin clicks "Save Treatment"
10. System validates all inputs (name uniqueness, required fields, file formats)
11. System uploads media files to S-05: Media Storage Service
12. System generates CDN URLs for video and images
13. System saves treatment record with "Active" status
14. System sends notification to all active providers: "New treatment available in catalog"
15. Providers receive notification and can now configure pricing for the new treatment

### Alternative Flows

**A1: Admin Edits Existing Treatment**:

- **Trigger**: Admin needs to update treatment information (video, description, technique details)
- **Steps**:
  1. Admin navigates to "Settings > Treatment Settings"
  2. Admin searches or filters for the treatment to edit
  3. Admin clicks "Edit" on the treatment card
  4. System displays treatment edit form with current values pre-filled
  5. Admin modifies fields (description, video, images, technique specifications)
  6. Admin clicks "Update Treatment"
  7. System creates new version of treatment record (versioning for audit trail)
  8. System updates CDN URLs if media files changed
  9. System notifies providers who currently offer this treatment about the update
  10. Existing provider quotes using this treatment remain unchanged (versioned)
- **Outcome**: Treatment information updated, providers notified, historical quotes unaffected

**A2: Admin Deactivates Treatment**:

- **Trigger**: Admin decides to retire a treatment type (outdated technique, compliance issue)
- **Steps**:
  1. Admin navigates to treatment in catalog
  2. Admin clicks "Deactivate Treatment"
  3. System checks if any open quotes (draft or sent) or open FR-006 bookings (Accepted, Confirmed, In Progress, Aftercare) use this treatment
  4. System displays warning: "X providers currently offer this treatment, Y active quotes exist"
  5. Admin confirms deactivation
  6. System changes treatment status to "Inactive"
  7. System prevents providers from selecting this treatment in new quotes
  8. System sends notification to providers: "Treatment [Name] has been deactivated"
  9. Existing quotes and bookings using this treatment continue unaffected
- **Outcome**: Treatment hidden from new quote creation, existing commitments honored

**A3: Provider Configures Treatment Pricing**:

- **Trigger**: Provider wants to offer a new treatment or update pricing for existing treatment
- **Steps**:
  1. Provider navigates to "Products & Services > Treatments > Treatment Pricing"
  2. System displays list of all active treatments from admin catalog
  3. Provider selects treatment to configure
  4. Provider enters pricing details:
     - Base price for treatment
     - Price per graft (if applicable)
     - Minimum graft count
     - Maximum graft count
     - Prices are entered in the system quote currency, which the screen shows read-only
  5. Provider sets treatment status: "Offered" or "Not Offered"
  6. Provider clicks "Save Pricing"
  7. System validates pricing (no negative values, max > min)
  8. System saves provider-specific treatment pricing configuration
  9. Treatment now available for provider to select when creating quotes
- **Outcome**: Provider can now offer this treatment in quotes with configured pricing

**B1: Treatment Creation Validation Error**:

- **Trigger**: Admin submits treatment with missing required fields or invalid data
- **Steps**:
  1. Admin fills out treatment creation form incompletely
  2. Admin clicks "Save Treatment"
  3. System validates inputs
  4. System detects errors:
     - Missing treatment name
     - Invalid video format (not MP4)
     - Image file exceeds 5MB limit
     - Description exceeds 5,000 characters
  5. System displays error messages next to invalid fields
  6. Admin corrects errors
  7. Admin resubmits form
  8. System validates successfully and creates treatment
- **Outcome**: Treatment creation fails until validation passes, admin guided to fix errors

**B2: Media Upload Failure**:

- **Trigger**: Network interruption or storage service unavailable during media upload
- **Steps**:
  1. Admin uploads treatment video during creation
  2. Upload to S-05: Media Storage Service fails
  3. System retries upload up to 3 times
  4. If all retries fail, system displays error: "Media upload failed, please try again"
  5. System saves treatment record without media (marked as "Pending Media Upload")
  6. Admin can retry media upload separately
  7. Once media successfully uploaded, system updates treatment record
- **Outcome**: Treatment created but media upload deferred, admin can complete later

---

### Main Flow: Provider Creates Package

**Actors**: Provider, System
**Trigger**: Provider wants to create a new package offering for their quotes
**Outcome**: New package available for provider to use as a quote option template

**Steps**:

1. Provider navigates to "Products & Services > Packages" in provider platform
2. Provider clicks "Create New Package" button
3. System displays package creation form
4. Provider enters package details:
   - Package name (e.g., "Premium FUE - 5-Star Hotel, 5 Nights")
   - Description (summary of the package)
   - Duration (days/nights if applicable)
   - Standard price, entered in the system quote currency (shown read-only; providers do not choose a currency)
5. Provider builds the included-items list. Each item has a service type (medical, travel, accommodation, transport, flight, or other), a name, an optional description, an optional component price, and an included flag
6. Provider ticks the included travel services: flight, hotel, transport, and other travel services
7. Provider builds the day-by-day treatment plan using relative days (Day 1, Day 2, and so on), each with a description; the plan never holds calendar dates
8. Provider uploads package images (optional, max 3 images, 2MB each)
9. Provider adds package terms and conditions (optional, markdown supported)
10. Provider sets the package status: "Active" or "Inactive"
11. Provider clicks "Save Package"
12. System validates inputs (name not empty, standard price > 0, at least one included item, plan days consecutive from Day 1)
13. System uploads images to S-05: Media Storage Service
14. System saves the package as version 1, linked to the provider account
15. System displays success message: "Package created successfully"
16. Package now appears in provider's package list and, when Active, is selectable during quote creation

**Not packaged**: The date range, additional notes, and documents are entered per inquiry during quote creation (FR-004). They are never stored on a package.

**How a package is used in a quote**: Each package the provider selects in FR-004 becomes one alternative quote option, with at most five options per parent quote. Packages are never added together into one option. The standard price prefills every date-range price row of that option, and the provider may edit each row or leave out a date range the option cannot offer.

### Alternative Flows (Packages)

**A4: Provider Edits Existing Package (library edit)**:

- **Trigger**: Provider needs to update a package in the package library (price, included items, travel services, plan, description, images, or status)
- **Steps**:
  1. Provider navigates to "Products & Services > Packages"
  2. Provider searches or filters for package to edit
  3. Provider clicks "Edit" on package card
  4. System displays package edit form with the values of the current version
  5. Provider modifies fields (standard price, included items, travel services, relative-day plan, description, images, terms, or status)
  6. Provider clicks "Update Package"
  7. System saves the changes as a new version of the same package (v1, v2, v3, and so on); the package ID stays the same
  8. The previous version becomes read-only: it can be viewed but never edited again
  9. Existing quotes never change, whether they are drafts, sent, or accepted; each quote option keeps its own copy and the version it recorded
  10. New quote options copy the latest version
- **Outcome**: Library package updated as a new version, earlier versions kept read-only, existing quotes unaffected
- **Note**: This is the only way to change the library package. Editing a package inside quote creation (FR-004 inline package editor) is a different path: it changes only that quote's copy and is never written back to the library (see "Package Edit Paths" in Business Rules).

**A5: Provider Deactivates Package**:

- **Trigger**: Provider no longer wants to offer a specific package (seasonal unavailability, cost changes)
- **Steps**:
  1. Provider navigates to "Products & Services > Packages"
  2. Provider clicks "Deactivate" on package card
  3. System counts the open quotes (status draft or sent) that contain a quote option copied from this package (see Usage Count in Field Calculation Rules)
  4. System displays warning: "This package is used in N open quotes. Deactivating hides it from new quotes; existing quotes are not changed."
  5. Provider confirms deactivation
  6. System changes package status to "Inactive"
  7. System prevents provider from adding this package to new quotes
  8. Existing quote options copied from this package keep their own copy and remain valid
- **Outcome**: Package hidden from new quotes, existing commitments honored

**A6: Provider Clones Package**:

- **Trigger**: Provider wants to create similar package with slight variations (e.g., 3-night vs 5-night hotel)
- **Steps**:
  1. Provider navigates to "Products & Services > Packages"
  2. Provider clicks "Clone" on existing package
  3. System creates copy of package with "(Copy)" appended to name
  4. Provider modifies cloned package details (name, duration, price)
  5. Provider saves cloned package
  6. System creates new package record
- **Outcome**: New package created quickly using existing package as template

**B3: Package Creation Validation Error**:

- **Trigger**: Provider submits package with invalid data
- **Steps**:
  1. Provider fills out package form with errors:
     - Empty package name
     - Negative price
     - No included items
     - Image file exceeds 2MB limit
  2. Provider clicks "Save Package"
  3. System validates inputs
  4. System displays error messages for invalid fields
  5. Provider corrects errors
  6. Provider resubmits form
  7. System validates successfully and creates package
- **Outcome**: Package creation prevented until validation passes

---

## Screen Specifications

### Admin Platform (A-09: System Settings & Configuration)

#### Screen 1: Admin Treatment Catalog (List View)

**Purpose**: Display all treatments in the platform catalog, allow filtering and searching, provide access to create/edit/deactivate treatments

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Treatment Name | text | Yes | Display name of treatment (e.g., "FUE") | Max 100 chars |
| Treatment Type | select | Yes | Category: FUE, FUT, DHI, Sapphire FUE, Robotic, Other | Must select from enum |
| Status | badge | N/A | Visual indicator: "Active" (green) or "Inactive" (gray) | Read-only display |
| Video Thumbnail | image | No | Thumbnail of treatment video if available | Display CDN URL |
| Number of Providers | number | N/A | Count of providers currently offering this treatment | Calculated field |
| Last Updated | date | N/A | Timestamp of last modification | Auto-generated |
| Actions | buttons | N/A | Edit, Deactivate, View Details buttons | N/A |

**Business Rules**:

- Active treatments appear at top of list, inactive treatments at bottom
- Search box filters by treatment name in real-time
- Filter dropdown allows filtering by treatment type
- "Create New Treatment" button always visible at top right
- Deactivate button disabled if no active quotes exist using this treatment
- Edit button available for all treatments regardless of status
- Number of providers shows count of providers who have configured pricing for this treatment

**Notes**:

- Use card-based layout for visual appeal
- Show video thumbnail as preview (hovering plays 3-second preview)
- Display warning icon next to treatments used in active quotes when attempting deactivation
- Pagination: 20 treatments per page

---

#### Screen 2: Admin Treatment Creation/Edit Form

**Purpose**: Allow admin to create new treatment or edit existing treatment details, upload media assets, configure technique specifications

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Treatment Name | text | Yes | Full name of treatment | Max 100 chars, must be unique |
| Treatment Type | select | Yes | Category selection | FUE, FUT, DHI, Sapphire FUE, Robotic, Other |
| Description | textarea (markdown) | Yes | Detailed explanation of treatment | Max 5,000 chars |
| Technique Specifications | textarea | No | Extraction method, implantation method, anesthesia | Max 2,000 chars |
| Expected Recovery Time | text | No | e.g., "7-10 days" | Max 50 chars |
| Typical Duration | number | No | Procedure duration in hours | 0.5 to 12 hours |
| Treatment Video | file upload | No | Educational video about treatment | MP4 format, max 50MB |
| Treatment Images | file upload (multiple) | No | Photos showing technique or results | JPEG/PNG, max 5 images, 5MB each |
| Educational Resources | file upload (multiple) | No | PDF documents with additional info | PDF format, max 3 files, 10MB each |
| Status | toggle | Yes | Active (visible to providers) or Inactive | Default: Active |

**Business Rules**:

- Treatment name must be unique across all treatments
- At least one of: description, video, or images must be provided
- Video upload shows progress bar and supports resume on failure
- Image upload allows drag-and-drop or click-to-browse
- Markdown editor provides preview pane for description
- Deactivating treatment triggers warning if providers currently offer it
- Saving creates new version with timestamp (audit trail)
- Cancel button discards changes and returns to treatment list

**Notes**:

- Use WYSIWYG markdown editor for description field
- Show video preview after upload (inline player)
- Display image thumbnails after upload with remove option
- Auto-save draft every 30 seconds to prevent data loss
- Provide tooltips explaining technique specifications format
- CDN URLs generated automatically after media upload

---

### Provider Platform (PR-06: Profile & Settings Management)

#### Screen 3: Provider Treatment Pricing Configuration

**Purpose**: Allow provider to view admin-created treatments, configure pricing for treatments they want to offer, enable/disable treatments

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Treatment Name | text (read-only) | N/A | Name from admin catalog | Display only |
| Treatment Type | badge (read-only) | N/A | Category badge | Display only |
| Treatment Description | text (read-only, expandable) | N/A | Description from admin catalog | Display only |
| Treatment Video | video player | No | Video from admin catalog | Display only if available |
| Base Price | number | Yes (if offering) | Reference-only, non-binding "starting from" price for the treatment; never a binding quote price | Must be > 0 |
| Price Per Graft | number | No | Additional cost per graft | Must be ≥ 0 |
| Currency | text (read-only) | N/A | System quote currency from active system configuration | Display only; providers cannot choose a currency |
| Minimum Graft Count | number | No | Minimum grafts for this treatment | Must be > 0 and < max |
| Maximum Graft Count | number | No | Maximum grafts for this treatment | Must be > min |
| Status Toggle | toggle | Yes | "Offered" or "Not Offered" | Default: Not Offered |

**Business Rules**:

- Provider can only view active treatments from admin catalog
- Inactive treatments are hidden from provider view
- If provider hasn't configured pricing, treatment shows "Not Configured" badge
- Provider must set base price to enable "Offered" status
- Base Price is a reference-only, non-binding "starting from" value. It may prefill new FR-004 quote option/date-price rows only where no other standard value exists, such as a package standard price, and may feed a future post-MVP starting price on provider cards. It is never binding and is never read after a quote is sent
- Treatment prices are entered in the system quote currency; there is no per-treatment currency
- Maximum graft count must be greater than minimum graft count
- Price per graft is optional (some treatments are fixed price, not graft-based)
- Saving pricing configuration makes treatment available in quote creation
- Provider can disable offering without deleting pricing configuration (re-enable later)

**Notes**:

- Display treatments in card layout with expand/collapse for details
- Show treatment video inline when card expanded
- Provide "Quick Copy Pricing" option to copy pricing from another treatment
- Highlight treatments not yet configured with banner at top
- Save button becomes "Update" button when editing existing configuration
- Display confirmation message: "Treatment pricing saved successfully"

---

#### Screen 4: Provider Package Catalog (List View)

**Purpose**: Display all packages created by provider, allow filtering by status, provide access to create/edit/deactivate packages

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Package Name | text | Yes | Display name of package | Max 100 chars |
| Included Items | text | N/A | Short summary of the included items (e.g., "5-star hotel, airport transfer, PRP") | Show first 3 items and "+N more" |
| Standard Price | number | Yes | Package standard price in the system quote currency | Format with currency symbol |
| Duration | text | No | e.g., "5 nights", "1 session" | Display if applicable |
| Status | badge | Yes | "Active" (green) or "Inactive" (grey) | Visual indicator |
| Version | text | N/A | Current library version (e.g., "v3") | Auto-generated |
| Usage Count | number | N/A | Number of quote options copied from this package whose parent quote is still open (draft or sent) | Calculated field (see Field Calculation Rules) |
| Last Updated | date | N/A | Timestamp of last modification | Auto-generated |
| Actions | buttons | N/A | Edit, Clone, Deactivate, View Details buttons | N/A |

**Business Rules**:

- Active packages appear at top of list, Inactive packages at bottom
- Search box filters by package name in real-time
- Filter dropdown allows filtering by status
- "Create New Package" button always visible at top right
- Clone button creates copy of package for quick variations
- Deactivate button warns "used in N open quotes" when open quotes contain an option copied from this package
- Usage count shows how many open quote options were copied from this package
- Packages can be sorted by name, price, or usage count

**Notes**:

- Use card-based layout showing package thumbnail if image uploaded
- Display status with colour-coded badges (Active = green, Inactive = grey)
- Show quick-edit pencil icon on hover for fast price updates; a quick price edit is a library edit and saves a new package version
- Pagination: 20 packages per page
- Provide bulk actions: "Deactivate Selected", "Export to CSV"

---

#### Screen 5: Provider Package Creation/Edit Form

**Purpose**: Allow provider to create a new package or edit an existing package in the library: the full quote option template of included items, travel services, relative-day plan, standard price, images, and status

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Package Name | text | Yes | Full name of package | Max 100 chars, must be unique per provider |
| Description | textarea (markdown) | Yes | Summary of the package | Max 2,000 chars |
| Included Items | repeatable item list | Yes | Services the package includes. Each item has a service type (medical, travel, accommodation, transport, flight, or other), name, optional description, optional component price, and an included flag | At least one item; allowed service types only; component price ≥ 0 |
| Included Travel Services | checklist | No | Flight, hotel, transport, and other travel services included in the package | Allowed values only |
| Relative-Day Treatment Plan | repeatable day list | No | Day number and description for each plan day | Consecutive days starting at Day 1; description required; no calendar dates |
| Duration | text | No | e.g., "5 nights", "3 days", "1 session" | Max 50 chars |
| Standard Price | number | Yes | Default price that prefills each date-range price row of a quote option created from this package (FR-004) | Must be > 0; system quote currency shown read-only |
| Package Images | file upload (multiple) | No | Photos of hotel, transport, etc. | JPEG/PNG, max 3 images, 2MB each |
| Terms & Conditions | textarea | No | Package-specific terms | Max 1,000 chars |
| Status | toggle | Yes | Active (can be selected in quotes) or Inactive | Default: Active |
| Version | text (read-only) | N/A | Current library version; saving an edit creates the next version | Auto-generated |

**Business Rules**:

- Package name must be unique within provider's package catalog (can duplicate across providers)
- Duration field format validated for common patterns: "X nights", "X days", "X hours", "X sessions"
- Price must be positive number with up to 2 decimal places
- Prices are in the system quote currency from active system configuration; the form shows the currency read-only and there is no per-package currency
- The date range, additional notes, and documents are not part of a package; providers enter them per inquiry in FR-004
- Image upload supports drag-and-drop or click-to-browse
- Markdown editor for description with preview pane
- Saving an Active package makes it immediately available in quote creation
- Saving an edit to an existing package creates a new version; earlier versions become read-only and existing quotes never change
- Deactivating package requires confirmation if used in open quotes
- Cancel button discards changes and returns to package list

**Notes**:

- Provide starter examples (e.g., "Standard FUE with 5-night hotel and airport transfers")
- Show image thumbnails after upload with remove/reorder options
- Validate that at least one of: description or images is provided
- Display character count for description field
- Provide "Save as Draft" option to save incomplete package
- Show success message: "Package saved successfully"

---

## Business Rules

### General Module Rules

- **Rule 1**: All treatments are globally managed by admin and available to all active providers
- **Rule 2**: Each provider manages their own package catalog independently
- **Rule 3**: Treatment and package versions are immutable once saved; every library edit creates a new version, and quotes keep the version they copied
- **Rule 4**: Deactivating treatments or packages does not affect existing quotes or bookings
- **Rule 5**: Pricing configuration is per-provider for treatments, per-package for packages; all library prices use the system quote currency and no treatment or package carries its own currency
- **Rule 6**: All timestamps displayed in provider's local timezone
- **Rule 7**: Media files (videos, images) are served via CDN with caching for performance
- **Rule 8**: A package is a full template for one quote option. It holds the included services and their prices, flight, hotel, transport, and other travel services, and the day-by-day relative treatment plan. The date range, additional notes, and documents are never packaged
- **Rule 9**: Each package selected in FR-004 seeds exactly one alternative quote option, with at most five options per parent quote. Package prices are never summed into one option, and the standard price prefills each date-range price row of that option
- **Rule 10**: Packages are deactivated or archived, never hard-deleted, because quote options keep the source package ID and version
- **Rule 11**: Every package field a patient can see (name, description, included items, travel services, plan, duration, images, and terms) is read from the quote option's own copy or from the exact package version that option records, never from the latest library version

### Package Edit Paths

There are two distinct ways a package's content can change. They must never be confused:

| Edit path | Where it happens | What it changes | Where it is saved | Effect on existing quotes |
|---|---|---|---|---|
| Library edit | Package management (Screen 5 in this module) | The library package | A new package version (v1, v2, and so on); earlier versions stay read-only | None. Existing quotes keep their own copy and recorded version |
| Inline edit | Quote creation (FR-004 inline package editor) | Only that quote option's copy | That quote only (quote-local copy) | None outside that quote. Never written back to the library and never creates a package version |

- A quote option records the source package ID, the source package version, and whether it was customised inline.
- There is no "save for future" action from an inline edit. To reuse a change, the provider repeats it as a library edit.

### Data & Privacy Rules

- **Privacy Rule 1**: Provider package catalogs are private (not visible to other providers)
- **Privacy Rule 2**: Admin can view provider packages in read-only mode for support purposes only
- **Privacy Rule 3**: Treatment videos and images are served via CDN using time-limited, signed URLs (no unauthenticated bulk access)
- **Privacy Rule 4**: Package images are accessible only to patients viewing quotes from that provider, and are resolved from the package version recorded on the quote option
- **Audit Rule**: All treatment and package modifications logged with timestamp, user, and action
- **Data Retention**: Deactivated treatments and packages archived, not deleted, with retention period governed by FR-023: Data Retention & Compliance

### Admin Editability Rules

**Editable by Admin**:

- Complete treatment catalog (create, edit, deactivate treatments)
- Treatment names, descriptions, videos, images, technique specifications
- Treatment status (active/inactive)
- Treatment type categories (can add new types to enum)

**Fixed in Codebase (Not Editable)**:

- Treatment versioning logic (automatic versioning on edit)
- Media file size limits (50MB video, 5MB images)
- Media file format restrictions (MP4 for video, JPEG/PNG for images)
- Package item service types (medical, travel, accommodation, transport, flight, other), aligned with FR-004

**Configurable with Restrictions**:

- Admin can deactivate treatments but cannot delete them (soft-delete only)
- Admin can view provider packages but cannot edit them (provider ownership enforced)

### Provider Editability Rules

**Editable by Provider**:

- Treatment pricing configuration (base price, price per graft, graft count ranges)
- Treatment offering status (offered/not offered per treatment)
- Complete package catalog for their clinic (create, edit, deactivate packages)
- Package standard price, descriptions, included items, travel services, relative-day plan, images, and status

**Fixed in Codebase (Not Editable by Provider)**:

- Treatment catalog itself (cannot create custom treatments)
- Treatment names, descriptions, videos from admin catalog (read-only)
- Package versioning logic (automatic versioning on edit)
- Package image size limits (2MB per image)

**Business Rules for Providers**:

- Provider must configure pricing for a treatment before offering it in quotes
- Provider can disable treatment offering without deleting pricing configuration
- Provider can create unlimited packages (no platform-imposed limit)
- Each package edit creates a new version; versions already copied into quotes are read-only and never change

### Localization Rules

**Translatable Content** (uses i18n keys from FR-021):

- Treatment descriptions and technique specifications
- Package names and descriptions
- All UI labels and error messages

Before production release, implementation must ensure all treatment- and package-related strings are registered with the translation management system defined in FR-021 (translation readiness checklist).

**Non-Translatable Content** (remains in English for consistency):

- Treatment type codes (FUE, FUT, DHI, Sapphire FUE, Robotic)
- Package item service type codes (medical, travel, accommodation, transport, flight, other)
- Media file names and CDN URLs

**Note**: This module depends on FR-021 (Multi-Language & Localization) for i18n infrastructure. FR-021 must be updated to include treatment and package content in its translation management scope.

### Field Calculation Rules

**Calculated Fields** (auto-generated, not user input):

- **Number of Providers** (Screen 1): `COUNT(provider_treatment_pricing WHERE treatment_id = X AND status = 'Offered')`
- **Usage Count** (Screen 4): `COUNT(quote options WHERE source_package_id = X AND parent quote status IN ('draft', 'sent'))`. It counts the FR-004 quote options copied from any version of this package whose parent quote is still open. The deactivation warning "used in N open quotes" shows the number of distinct open parent quotes among them. Status values follow FR-004
- **Last Updated** (all screens): Database `updated_at` timestamp, displayed in user's local timezone

---

## Success Criteria

### Patient Experience Metrics

- **SC-001**: Patients can view comprehensive treatment details (video, description, technique) within 2 seconds of opening provider quote
- **SC-002**: Patients comparing multiple provider quotes can clearly distinguish treatment types and package offerings
- **SC-003**: 90% of patients report that treatment information helped them make informed decision

### Provider Efficiency Metrics

- **SC-004**: Providers can configure pricing for a new treatment in under 2 minutes
- **SC-005**: Providers can create a new package in under 3 minutes with all details and images
- **SC-006**: Providers can select treatment and packages during quote creation in under 1 minute
- **SC-007**: Provider time spent on quote creation reduces by 40% compared to manual process

### Admin Management Metrics

- **SC-008**: Admin can add new treatment to platform catalog in under 5 minutes
- **SC-009**: Admin can update treatment video or description in under 3 minutes
- **SC-010**: 100% of treatment catalog changes propagate to provider platforms within 1 minute
- **SC-011**: Admin can monitor which providers offer which treatments via real-time dashboard

### System Performance Metrics

- **SC-012**: Treatment catalog loads in under 1 second for admin view (50+ treatments)
- **SC-013**: Provider treatment selection during quote creation loads in under 500ms
- **SC-014**: Package catalog loads in under 1 second for provider view (100+ packages)
- **SC-015**: Media file uploads complete within 30 seconds for 50MB video files on standard connection
- **SC-016**: CDN delivers treatment videos with < 2 second buffering time for 95% of requests

### Business Impact Metrics

- **SC-017**: Treatment standardization reduces patient confusion, increasing quote acceptance rate by 15%
- **SC-018**: Provider package differentiation enables competitive positioning without undercutting treatment prices
- **SC-019**: Platform achieves 100% provider adoption of standardized treatment catalog within 3 months
- **SC-020**: 80% of providers create at least 5 packages within first month of onboarding

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **FR-004 / Module PR-02**: Inquiry & Quote Management
  - **Why needed**: Providers select treatments and packages from this module when creating quotes
  - **Integration point**: Quote creation calls treatment/package APIs, retains the exact Treatment ID/version on the parent Quote, and captures each selected Package ID/version as provenance on an FR-004 Quote Option snapshot. Each selected package seeds one alternative Quote Option (at most five per parent quote); FR-004 copies the package's included items, travel services, and relative-day plan into the option, and the standard price prefills each date-range price row. Quote-local inline customization never writes back to this package library and never creates a package version.

- **FR-001 / Module P-01**: Auth & Profile Management
  - **Why needed**: Provider authentication required to access package management features
  - **Integration point**: Admin and provider authentication tokens used to authorize treatment and package operations

- **FR-009 / Module PR-01**: Auth & Team Management
  - **Why needed**: Role-based permissions determine which provider staff can manage packages
  - **Integration point**: Permission checks for package creation/editing based on staff role

- **FR-021 / Module A-09 + S-02**: Multi-Language & Localization
  - **Why needed**: Treatment descriptions, package names/descriptions require multi-language support
  - **Integration point**: Uses i18n service to store/retrieve translated content for treatment and package text fields
  - **Action required**: FR-021 must be updated to include treatment and package content types in translation management scope

- **FR-026 / Module A-09**: App Settings & Configuration (Self-Dependency)
  - **Why needed**: This module is part of A-09 and shares configuration infrastructure
  - **Integration point**: Uses same settings management UI patterns, audit logging, versioning mechanisms

### External Dependencies (APIs, Services)

- **External Service 1**: CDN (CloudFront, Cloudflare, or equivalent)
  - **Purpose**: Serve treatment videos and images with low latency globally
  - **Integration**: Upload media to S3, generate CDN URLs, serve via CDN edge locations
  - **Failure handling**: Fallback to direct S3 URLs if CDN unavailable, display placeholder image for failed loads

- **External Service 2**: Media Processing Service (AWS MediaConvert or equivalent)
  - **Purpose**: Transcode uploaded treatment videos to multiple formats/resolutions for device compatibility
  - **Integration**: Trigger transcoding job on video upload, generate HLS/DASH streams for adaptive bitrate
  - **Failure handling**: Queue transcoding job for retry, notify admin if transcoding fails after 3 attempts

- **External Service 3**: Image Optimization Service (Cloudinary, imgix, or equivalent)
  - **Purpose**: Automatically resize, compress, and optimize treatment and package images
  - **Integration**: Upload original image, receive optimized versions for web/mobile display
  - **Failure handling**: Use original image if optimization fails, log error for admin review

### Data Dependencies

- **Entity 1**: Active Provider Accounts
  - **Why needed**: Cannot assign packages to providers without active provider accounts
  - **Source**: Provider onboarding module (A-02: Provider Management & Onboarding)

- **Entity 2**: System Quote Currency
  - **Why needed**: All treatment and package library prices are entered and shown in the system quote currency; providers do not choose a currency
  - **Source**: Active system configuration used by FR-004 for the parent quote currency (FR-026: App Settings & Security Policies; exchange rates from FR-029: Payment System Configuration)

- **State 3**: Media Storage Service Availability
  - **Why needed**: Cannot upload treatment videos or package images without storage service
  - **Source**: S-05: Media Storage Service

---

## Assumptions

### User Behavior Assumptions

- **Assumption 1**: Admins will create comprehensive treatment catalog before provider onboarding begins
- **Assumption 2**: Providers will configure pricing for treatments they specialize in (not all treatments)
- **Assumption 3**: Providers will create packages that reflect their actual service capabilities (not aspirational)
- **Assumption 4**: Patients will watch treatment videos when comparing quotes (video content must be high quality)
- **Assumption 5**: Providers will update package pricing seasonally (hotel rates change, transport costs vary)

### Technology Assumptions

- **Assumption 1**: Admins have access to desktop computers with reliable internet for uploading large video files
- **Assumption 2**: Providers access platform via modern web browsers (Chrome, Firefox, Safari - last 2 versions)
- **Assumption 3**: CDN infrastructure supports global distribution with < 100ms latency to edge locations
- **Assumption 4**: Video transcoding completes within 5 minutes for 50MB source video file
- **Assumption 5**: Mobile patients can stream treatment videos on 4G/LTE connections without buffering

### Business Process Assumptions

- **Assumption 1**: Admin team reviews and approves treatment content before activation (quality control)
- **Assumption 2**: Providers have authority to set their own pricing without admin approval
- **Assumption 3**: Treatments will be added incrementally (not all at once during launch)
- **Assumption 4**: Package item service types (medical, travel, accommodation, transport, flight, other) are relatively stable (infrequent addition of new types)
- **Assumption 5**: Provider package catalogs will grow over time as providers expand offerings
- **Assumption 6**: Treatment deactivation is rare (only for compliance or safety issues)

---

## Implementation Notes

### Technical Considerations

- **Architecture**: Treatment catalog uses centralized database table shared by all tenants, package catalog uses tenant-scoped tables
- **Versioning**: Implement immutable versioning for treatments and packages. Each treatment and package keeps one stable ID across all versions plus an integer version number; each edit stores a new immutable version (with its included items and plan days for packages) rather than updating in place. Provider pricing configuration references the stable treatment ID; FR-004 parent quotes reference treatment ID plus version, and quote options reference package ID plus version
- **Media Storage**: Use S3-compatible object storage with CDN integration for global delivery
- **Caching**: Cache treatment catalog aggressively (24-hour TTL), invalidate cache on admin edits
- **Performance**: Index treatment names, types, and status for fast filtering, index package names and status for provider searches

### Integration Points

- **Integration 1**: Admin platform sends treatment CRUD operations to shared treatment API
  - **Data format**: JSON payload with treatment fields, multipart/form-data for media uploads
  - **Authentication**: Admin JWT token with elevated permissions
  - **Error handling**: Display validation errors inline, retry media uploads on failure

- **Integration 2**: Provider platform queries treatment catalog and manages packages via provider API
  - **Data format**: JSON responses with paginated treatment list, package CRUD via JSON payloads
  - **Authentication**: Provider JWT token with clinic-scoped permissions
  - **Error handling**: Display user-friendly errors for validation failures, cache treatment catalog locally

- **Integration 3**: Quote creation workflow fetches treatment pricing and package details
  - **Data format**: Combined JSON response with treatment + packages + pricing for specific provider
  - **Authentication**: Provider JWT token
  - **Error handling**: If the API is temporarily unavailable, package selection is blocked with a retry message; the system never seeds a quote option from cached data whose price or content does not match the package version it records

### Scalability Considerations

- **Current scale**: Expected 50 treatments in catalog at launch, 20 packages per provider, 100 providers
- **Growth projection**: Plan for 200 treatments within 2 years, 50 packages per provider, 1,000 providers
- **Peak load**: Handle 100 concurrent admins editing treatments, 500 concurrent providers managing packages
- **Data volume**: Expect 5GB of treatment media (videos + images) per year, 2GB of package images per year
- **Scaling strategy**: Horizontal scaling of API servers, CDN for media delivery, database read replicas for treatment catalog queries

### Security Considerations

- **Authentication**: JWT-based authentication for admin and provider platforms, tokens expire after 30 minutes
- **Authorization**: Role-based access control - admin can edit all treatments, providers can edit only their packages
- **Encryption**: Media files encrypted at rest in S3 (AES-256), served over TLS 1.3 via CDN
- **Audit trail**: Log all treatment and package modifications with timestamp, user ID, IP address, old/new values
- **Threat mitigation**: Rate limit treatment creation (max 10 per hour per admin), rate limit package creation (max 50 per hour per provider)
- **Compliance**: GDPR compliance for EU providers (right to export package data; package erasure requests follow FR-023 retention rules because quote history references package versions)
- **Input validation**: Sanitize all text inputs to prevent XSS, validate file types and sizes to prevent malicious uploads

---

## User Scenarios & Testing

### User Story 1 - Admin Creates Comprehensive Treatment (Priority: P1)

Admin adds a new treatment type (FUE) to the platform catalog with video, images, and detailed description so that providers can offer this treatment to patients.

**Why this priority**: Treatment catalog is foundation for entire quote system. Without treatments, providers cannot create quotes. This is the most critical workflow.

**Independent Test**: Can be fully tested by creating a treatment with all fields, verifying it appears in admin catalog, and confirming providers can view it in their treatment selection.

**Acceptance Scenarios**:

1. **Given** admin is logged into admin platform, **When** admin navigates to "Settings > Treatment Settings" and clicks "Create New Treatment", **Then** system displays treatment creation form with all fields (name, type, description, video upload, image upload, technique specs)
2. **Given** admin fills out treatment form with valid data and uploads 50MB video, **When** admin clicks "Save Treatment", **Then** system uploads video to S3, generates CDN URL, saves treatment record with "Active" status, and displays success message
3. **Given** new treatment is saved, **When** provider navigates to "Settings > Treatment Pricing", **Then** provider sees new treatment in available treatment list and can configure pricing

---

### User Story 2 - Provider Configures Treatment Pricing (Priority: P1)

Provider views admin-created treatments and configures pricing for treatments they want to offer so they can include these treatments in quotes.

**Why this priority**: Without pricing configuration, providers cannot use treatments in quotes. This workflow must work before quote creation is possible.

**Independent Test**: Can be fully tested by selecting a treatment, entering pricing details, saving configuration, and verifying treatment appears in quote creation workflow.

**Acceptance Scenarios**:

1. **Given** provider is logged into provider platform, **When** provider navigates to "Products & Services > Treatments > Treatment Pricing", **Then** system displays list of all active treatments from admin catalog
2. **Given** provider selects treatment to configure, **When** provider enters base price (£2,500), price per graft (£2.00), graft range (1,000-5,000), and toggles status to "Offered", **Then** system saves pricing configuration and displays success message
3. **Given** provider has configured treatment pricing, **When** provider creates new quote and selects treatment, **Then** treatment appears in quote with configured pricing auto-populated

---

### User Story 3 - Provider Creates Package Template (Priority: P1)

Provider creates a package template (for example, "Premium FUE - 5-Star Hotel, 5 Nights") with included items, travel services, a relative-day plan, images, and a standard price so the package can seed a quote option.

**Why this priority**: Packages save providers from re-entering the same services, travel arrangements, and treatment plan for every quote, and let them offer clear alternatives.

**Independent Test**: Can be fully tested by creating a package with all details, verifying it appears in provider's package catalog, and confirming it can be selected during quote creation.

**Acceptance Scenarios**:

1. **Given** provider is logged into provider platform, **When** provider navigates to "Products & Services > Packages" and clicks "Create New Package", **Then** system displays package creation form
2. **Given** provider fills out package form (name: "Premium FUE - 5-Star Hotel, 5 Nights", included items: 5-star hotel 5 nights, airport transfer, PRP session; travel services: hotel and transport; plan Day 1 to Day 3; standard price: £3,200; uploads 3 images), **When** provider clicks "Save Package", **Then** system uploads images to S3, saves package version 1, and displays success message
3. **Given** package is saved, **When** provider creates quote and views package selection, **Then** new package appears in available packages list with its included items, images, and standard price displayed
4. **Given** the package form is open, **When** provider enters the standard price, **Then** the price is shown in the system quote currency, no currency selector is offered, and no date range, notes, or documents fields exist on the package
5. **Given** package version 2 has been copied into a sent quote, **When** provider edits the package in package management and saves, **Then** system creates version 3, version 2 becomes read-only, and the sent quote's option still shows the version 2 content

---

### User Story 4 - Provider Selects Treatment and Packages in Quote (Priority: P2)

Provider creates a quote by selecting one treatment for the parent quote and one to five packages. Each package becomes one alternative quote option that the patient compares; package prices are never added together.

**Why this priority**: This is the primary use case for treatments and packages, but depends on treatments and packages already being configured (P1 dependencies).

**Independent Test**: Can be fully tested by creating a quote with one treatment and three packages, verifying that three separate quote options exist, each prefilled from its own package, and that no combined package total is calculated.

**Acceptance Scenarios**:

1. **Given** provider is creating a quote for an inquiry with two date ranges, **When** provider selects treatment (FUE, 3,000 grafts) and three packages (Standard £2,900, Premium £3,200, VIP £3,900), **Then** system creates three alternative quote options, one per package, and the treatment appears once on the parent quote
2. **Given** the three options exist, **When** the system prefills prices, **Then** each option's date-range price rows are prefilled with that package's standard price, the provider may edit any row or leave out a date range an option cannot offer, and the quote holds up to six priced subquotes (3 options × 2 date ranges); package prices are never summed
3. **Given** provider has selected five packages, **When** provider tries to select a sixth, **Then** system blocks the selection: "A quote can have at most 5 options."
4. **Given** provider reviews a quote with treatment and package options, **When** provider submits the quote, **Then** system retains the exact Treatment ID/version on the parent Quote, captures each Package ID/version on its Quote Option snapshot, and notifies the patient
5. **Given** provider customises one option inline during quote creation (for example, adds a translator item), **When** the quote is saved, **Then** only that quote option's copy changes, the option records that it was customised inline, and the library package keeps the same content and version

---

### User Story 5 - Admin Updates Treatment Video (Priority: P2)

Admin needs to replace outdated treatment video with updated version, system creates new treatment version and notifies providers who offer this treatment.

**Why this priority**: Treatment updates are important for maintaining content quality but are less critical than initial creation. This can be tested independently after treatment creation (P1) is working.

**Independent Test**: Can be fully tested by editing a treatment, uploading new video, verifying new version is created, and confirming providers receive notification.

**Acceptance Scenarios**:

1. **Given** admin navigates to treatment catalog, **When** admin clicks "Edit" on existing treatment (FUE), **Then** system displays edit form with current values pre-filled including current video
2. **Given** admin uploads new video file (replacing old video), **When** admin clicks "Update Treatment", **Then** system creates new treatment version (v2), uploads new video to S3, generates new CDN URL, and preserves old version for historical quotes
3. **Given** treatment update is saved, **When** system processes update, **Then** system sends notification to all providers who currently offer this treatment: "Treatment [FUE] video has been updated"

---

### User Story 6 - Provider Deactivates Package (Priority: P3)

Provider needs to temporarily stop offering a package (seasonal hotel unavailability), system deactivates package but preserves it for existing quotes.

**Why this priority**: Package lifecycle management is important for long-term operations but not critical for initial launch. This workflow can be tested independently after package creation (P1) is working.

**Independent Test**: Can be fully tested by deactivating a package, verifying it's hidden from new quotes, and confirming existing quotes with this package remain valid.

**Acceptance Scenarios**:

1. **Given** provider navigates to package catalog, **When** provider clicks "Deactivate" on a package copied into options of 5 open (draft or sent) quotes, **Then** system displays warning: "This package is used in 5 open quotes. Deactivating hides it from new quotes; existing quotes are not changed."
2. **Given** provider confirms deactivation, **When** system processes deactivation, **Then** package status changes to "Inactive", package is hidden from quote creation workflow, and existing quote options keep their own copy and recorded version
3. **Given** package is deactivated, **When** provider creates new quote and views package selection, **Then** deactivated package does not appear in available packages list

---

### Edge Cases

- **What happens when admin uploads 100MB video exceeding 50MB limit?** System displays validation error: "Video file exceeds maximum size of 50MB. Please compress the video or upload a shorter version." Admin must compress video or split into shorter segments.

- **How does system handle provider creating package with name that already exists in their catalog?** System validates package name uniqueness per provider. If duplicate name detected, system displays error: "A package with this name already exists. Please choose a different name or edit the existing package."

- **What occurs if provider configures treatment pricing with maximum graft count less than minimum?** System validates that max > min during form submission. If validation fails, system displays error next to max field: "Maximum graft count must be greater than minimum graft count."

- **How to manage provider selecting deactivated treatment during quote creation?** Provider cannot select deactivated treatments. If treatment is deactivated while provider has draft quote open, system refreshes available treatments and displays warning: "Treatment [Name] is no longer available. Please select a different treatment."

- **What happens when media upload fails during treatment creation?** System retries upload 3 times with exponential backoff. If all retries fail, system saves treatment record with status "Pending Media Upload" and displays error: "Video upload failed. Treatment saved without media. You can upload the video later by editing the treatment." Admin can edit treatment to retry upload.

- **What occurs if two admins simultaneously edit the same treatment?** System uses optimistic locking with version timestamps. When second admin attempts to save, system detects concurrent edit and displays error: "This treatment was modified by another admin. Please refresh and reapply your changes." Second admin must reload treatment and reapply edits.

---

## Functional Requirements Summary

### Core Requirements

- **REQ-024-001**: System MUST allow admins to create treatments with name, type, description, video, images, and technique specifications
- **REQ-024-002**: System MUST allow admins to edit existing treatments, creating new versions without modifying historical records
- **REQ-024-003**: System MUST allow admins to activate or deactivate treatments, affecting availability for new quotes only
- **REQ-024-004**: System MUST allow providers to view all active treatments from admin catalog
- **REQ-024-005**: System MUST allow providers to configure pricing for treatments they want to offer (base price, price per graft, graft ranges)
- **REQ-024-006**: System MUST allow providers to enable or disable treatment offerings without deleting pricing configuration
- **REQ-024-007**: System MUST allow providers to create packages with name, description, included items, included travel services, relative-day treatment plan, standard price, images, and status (Active or Inactive)
- **REQ-024-008**: System MUST allow providers to edit existing packages in the package library; each save MUST create a new package version (v1, v2, and so on), keep earlier versions read-only, and never change existing quotes
- **REQ-024-009**: System MUST allow providers to deactivate packages, hiding them from new quotes while preserving existing quotes
- **REQ-024-010**: System MUST allow providers to select one treatment for the parent quote and one to five Active packages when creating quotes, where each selected package seeds exactly one alternative quote option
- **REQ-024-011**: System MUST prefill each date-range price row of a package-seeded quote option with that package's standard price and MUST NOT sum package prices into one option total
- **REQ-024-012**: System MUST retain the exact Treatment ID/version on the parent Quote and each selected Package ID/version as provenance on its Quote Option snapshot to prevent retroactive changes
- **REQ-024-030**: System MUST keep inline package edits made during quote creation in that quote only and MUST NOT write them back to the library package or create a new package version
- **REQ-024-031**: System MUST NOT store a date range, additional notes, or documents on a package; these are entered per inquiry in FR-004
- **REQ-024-032**: System MUST use the system quote currency for all treatment and package library prices; providers MUST NOT choose a currency per treatment or package
- **REQ-024-033**: System MUST NOT hard-delete packages; packages are deactivated or archived only
- **REQ-024-034**: System MUST show patients package content only from the quote option's own copy or from the exact package version that option records, never from the latest library version
- **REQ-024-035**: System MUST treat the provider treatment Base Price as a reference-only, non-binding "starting from" value. It MAY prefill new FR-004 quote option/date-price rows only where no other standard value exists and MAY feed a future post-MVP starting price on provider cards; it MUST NOT be binding and MUST NOT be read after a quote is sent

### Data Requirements

- **REQ-024-013**: System MUST maintain versioned treatment records with immutable history (no update-in-place)
- **REQ-024-014**: System MUST maintain versioned package records with immutable history, including each version's included items, travel services, and relative-day plan
- **REQ-024-015**: System MUST store media files (videos, images) in S3-compatible object storage with CDN delivery
- **REQ-024-016**: System MUST track which providers offer which treatments (provider-treatment pricing configuration)
- **REQ-024-017**: System MUST link packages to provider accounts (package ownership)
- **REQ-024-018**: System MUST preserve the exact Treatment version and Quote Option package snapshots used in historical quotes and bookings

### Security & Privacy Requirements

- **REQ-024-019**: System MUST restrict treatment creation/editing to admin users only
- **REQ-024-020**: System MUST restrict package management to provider users (edit only their own packages)
- **REQ-024-021**: System MUST serve media files via CDN over TLS 1.3 (HTTPS)
- **REQ-024-022**: System MUST log all treatment and package modifications with timestamp, user ID, IP address, and old/new values
- **REQ-024-023**: System MUST validate uploaded media files for type, size, and malicious content
- **REQ-024-024**: System MUST prevent providers from viewing other providers' package catalogs

### Integration Requirements

- **REQ-024-025**: System MUST expose REST API for treatment CRUD operations (admin access only)
- **REQ-024-026**: System MUST expose REST API for package create, read, update (new version), and deactivate operations, with no hard delete (provider access only)
- **REQ-024-027**: System MUST integrate with S-05: Media Storage Service for video and image uploads
- **REQ-024-028**: System MUST integrate with CDN service for media file delivery
- **REQ-024-029**: System MUST integrate with PR-02: Inquiry & Quote Management for treatment and package selection during quote creation

---

## Key Entities

- **Entity 1 - Treatment**
  - **Key attributes**: treatment_id (UUID, stable across versions), name (string), type (enum), description (text), video_url (string), image_urls (array), technique_specifications (text), recovery_time (string), duration_hours (float), status (enum: active/inactive), version (integer), created_at (timestamp), updated_at (timestamp), created_by_admin_id (UUID)
  - **Relationships**: One treatment can have many provider pricing configurations (one-to-many), which reference the stable treatment_id. One treatment version (treatment_id plus version) can be referenced by many parent Quotes (one-to-many).

- **Entity 2 - TreatmentPricingConfiguration**
  - **Key attributes**: pricing_id (UUID), provider_id (UUID), treatment_id (UUID), base_price (decimal, system quote currency), price_per_graft (decimal, system quote currency), min_graft_count (integer), max_graft_count (integer), status (enum: offered/not_offered), created_at (timestamp), updated_at (timestamp)
  - `base_price` is a reference-only, non-binding "starting from" value; FR-004 never reads it after a quote is sent.
  - **Relationships**: Belongs to one provider (many-to-one). Belongs to one treatment (many-to-one).

- **Entity 3 - Package**
  - **Key attributes**: package_id (UUID, stable across versions), version (integer), provider_id (UUID), name (string), description (text), duration (string), standard_price (decimal, system quote currency), included_travel_services (array: flight/hotel/transport/other), image_urls (array), terms_conditions (text), status (enum: active/inactive), created_at (timestamp), created_by (UUID)
  - **Relationships**: Belongs to one provider (many-to-one). Each package version has many PackageItems and PackagePlanDays. Earlier versions are read-only. One package version can be the provenance source for many FR-004 Quote Options (one-to-many); each option records the source package ID, version, and whether it was customised inline, and quote-local option copies remain independent from later package edits. Packages are never hard-deleted.

- **Entity 4 - QuoteTreatment** (removed): No longer a record of this module. The FR-004 parent Quote holds the treatment ID, treatment version, and graft facts; prices live on FR-004 option date-range rows.

- **Entity 5 - QuotePackage** (removed): No longer a record of this module. FR-004 Quote Options hold package provenance (`sourcePackageId`, `sourcePackageVersion`) and the quote-local copy. Legacy rows are handled by the FR-004 migration.

- **Entity 6 - PackageItem**
  - **Key attributes**: package_item_id (UUID), package_id (UUID), package_version (integer), item_type (enum: medical/travel/accommodation/transport/flight/other), name (string), description (text), price (decimal, optional, system quote currency), is_included (boolean), display_order (integer)
  - **Relationships**: Belongs to one package version (many-to-one). FR-004 copies items into its quote option items and records the source item ID.

- **Entity 7 - PackagePlanDay**
  - **Key attributes**: plan_day_id (UUID), package_id (UUID), package_version (integer), day_number (integer, relative, starting at 1), description (text)
  - **Relationships**: Belongs to one package version (many-to-one). FR-004 copies plan days into the quote option's relative-day plan; days are never converted to calendar dates.

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-12 | 1.0 | Initial PRD creation for FR-024 Treatment & Package Management | AI Assistant |
| 2025-11-28 | 1.1 | Updated navigation paths, localization scope, and marked PRD as verified | AI Assistant |
| 2026-09-10 | 1.2 | FR-004 v2.6 reconciliation: package versions now provide provenance to Quote Option snapshots rather than a direct reusable-package relationship on new parent Quotes; the legacy QuotePackage link is explicitly deprecated. See [Change Request](./change-request-2026-09-10-quote-option-provenance-alignment.md). | Product Owner / Documentation |
| 2026-10-16 | 1.3 | MTG-002 quote-model alignment: a package is a full template that seeds one Quote Option (included items, travel services, relative-day plan, standard price; date range, notes, and documents never packaged); each selected package is one alternative option, up to 5, never summed; add-on package types removed; PackageItem and PackagePlanDay added; package and treatment currency removed; QuoteTreatment and QuotePackage removed; Usage Count counts Quote Options on open (draft or sent) quotes; library-edit versioning and inline quote-local edit paths stated separately; stable IDs plus versions, no hard delete, patient fields from the recorded version, no stale-price fallback. Findings FR-024-1, -2, -3, -4, -5, -6, -8, -9 to -14; decisions D17, D18, M1, M8, M10, R7-3. See [Change Request](./change-request-2026-10-16-mtg002-quote-model-alignment.md) (CR-FR024-20261016-01). | Product Owner / Documentation |
| 2026-10-16 | 1.4 | Product Owner Q-series follow-up (Q20; CR-FR024-20261016-01): Screen 3 treatment Base Price defined as a reference-only, non-binding "starting from" value that may prefill new quote rows only where no other standard value exists and may feed a future post-MVP starting price on provider cards; never binding and never read after a quote is sent. New REQ-024-035. Status remains pending consolidated verification. | Product Owner / Documentation |
| 2026-10-18 | 1.5 | Consolidated verification corrections (CR-FR024-20261016-01; decision M6): Alternative Flow A2 step 3 now checks open quotes (draft or sent) and open FR-006 bookings (Accepted, Confirmed, In Progress, Aftercare) instead of "scheduled bookings", which is not an FR-006 booking state. Approvals row refreshed to v1.4. | AI |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | Hairline Product Team | 2025-11-28 | ✅ Approved |
| Technical Lead | Hairline Engineering | 2025-11-28 | ✅ Approved |
| Stakeholder | Hairline Leadership | 2025-11-28 | ✅ Approved |
| Product Owner | Hairline Product Team | 2026-10-16 | ✅ Documentation approved through v1.4 via the MTG-002 decision log (CR-FR024-20261016-01); v1.5 consolidated verification correction on 2026-10-18 applies decision M6; implementation reconciliation required |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-011 Aftercare & Recovery Management PRD
**Last Updated**: 2026-10-18
