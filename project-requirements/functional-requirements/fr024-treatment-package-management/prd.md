# FR-024 - Treatment & Package Management

**Module**: A-09: System Settings & Configuration | PR-06: Profile & Settings Management
**Feature Branch**: `fr024-treatment-package-management`
**Created**: 2025-11-12
**Status**: 🟡 Revised — Pending Consolidated Verification
**Source**: FR-024 from system-prd.md

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

- Patients view treatment details (videos, descriptions, technique information) within provider quotes (REQ-024-036)
- Patients see each provider's package-based quote options as alternatives, shown from the quote's own copy of the package
- Patients compare treatment and package offerings across multiple provider quotes
- No direct treatment or package management actions available to patients (REQ-024-036)

**Provider Platform (PR-06: Profile & Settings Management)**:

- Providers access the admin-created treatment catalog
- Providers cannot create custom treatments (ensures standardization)
- Providers configure pricing for each treatment type they offer
- Providers create and manage their own package catalog
- Providers build each package as a full quote template: included services with their prices, flight, hotel, transport, and other travel services, and a day-by-day relative treatment plan
- Providers set a standard price and an Active or Inactive status for each package
- Providers can enable/disable treatments and packages without deleting them
- Providers select one treatment per quote and one to five packages; each selected package seeds one alternative quote option in FR-004 (REQ-004-033; REQ-004-016)

**Admin Platform (A-09: System Settings & Configuration)**:

- Admins create and manage the master treatment catalog
- Admins manage the list of treatment types (initially FUE, FUT, DHI, Sapphire FUE, Robotic, and Other) on a screen
- Admins manage the medication templates and post-op instruction templates, which providers use in aftercare documentation
- Admins upload treatment videos, images, and detailed descriptions
- Admins document technique specifications for each treatment
- Admins can activate/deactivate treatments globally
- Admins have a read-only screen showing provider packages (for support purposes)
- Admins cannot modify individual provider packages

**Shared Services (S-XX)**:

- S-05: Media Storage Service handles treatment videos, images, and package assets
- All media files uploaded for treatments and packages stored securely with CDN delivery

### Communication Structure

**In Scope**:

- System notifications when admin saves a new treatment as Active (all active providers notified) (REQ-024-041)
- System notifications when admin deactivates treatments (providers who offer the treatment notified) (REQ-024-043)
- Provider receives confirmation when packages are successfully created/updated (REQ-024-044)

**Out of Scope**:

- Direct messaging between admins and providers about treatment content (handled by A-10: Communication Monitoring & Support)
- Patient inquiries about treatments or packages (handled by P-06: Communication)
- Marketing communications about new treatments (handled by S-03: Notification Service with A-06: Discount & Promotion Management)

### Entry Points

**Admin Entry Points**:

- Admin navigates to "Settings > Treatment Settings" in admin platform
- Admin selects "Create New Treatment" to add treatment type
- Admin edits existing treatment by selecting from treatment list
- Admin opens the treatment type list, the read-only provider packages view, and the aftercare templates from the same treatment settings area (REQ-024-037)

**Provider Entry Points**:

- Provider navigates to "Products & Services > Treatments" in provider platform
- Provider accesses "Treatment Pricing" to configure pricing for admin-created treatments
- Provider navigates to "Products & Services > Packages" to manage their package catalog
- Provider selects "Create Package" to add new package offering
- During quote creation, provider selects a treatment and one to five Active packages (REQ-024-037)

**Patient Entry Points** (View-Only):

- Patient views treatment details when reviewing provider quotes
- Patient sees package options within quote comparison interface
- No direct management access for patients (REQ-024-037)

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
   - Treatment type selection from the managed treatment type list (FUE, FUT, DHI, Sapphire FUE, Robotic, Other, and any type admins add)
   - Detailed description (markdown supported)
   - Technique specifications (extraction method, implantation method, anesthesia type)
   - Expected recovery time
   - Typical duration (hours)
5. Admin uploads treatment video (optional, MP4 format, max 50MB)
6. Admin uploads treatment images (optional, JPEG/PNG, max 5 images, 5MB each)
7. Admin uploads educational resources (optional, PDF documents)
8. Admin sets treatment status: "Active" or "Inactive" (default Active); "Save as Draft" keeps an unfinished treatment as Draft, and the form also auto-saves a draft every 30 seconds
9. Admin clicks "Save Treatment"
10. System validates all inputs (name uniqueness, required fields, file formats)
11. System uploads media files to S-05: Media Storage Service
12. System generates CDN URLs for video and images
13. System saves treatment record with the status the admin chose
14. Only when the treatment was saved as Active, system sends notification to all active providers: "New treatment available in catalog" (REQ-024-041)
15. Providers who receive the notification can now configure pricing for the new treatment

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
  9. System notifies providers who currently offer this treatment about the update (REQ-024-042)
  10. Existing provider quotes using this treatment remain unchanged (versioned)
- **Outcome**: Treatment information updated, providers notified, historical quotes unaffected

**A2: Admin Deactivates Treatment**:

- **Trigger**: Admin decides to retire a treatment type (outdated technique, compliance issue)
- **Steps**:
  1. Admin navigates to treatment in catalog
  2. Admin clicks "Deactivate Treatment"
  3. System checks if any open quotes (draft or sent) or open FR-006 bookings (Accepted, Confirmed, In Progress, Aftercare) use this treatment (REQ-024-051)
  4. System displays warning: "X providers currently offer this treatment, Y active quotes exist"
  5. Admin confirms deactivation
  6. System changes treatment status to "Inactive"
  7. System prevents providers from selecting this treatment in new quotes
  8. System sends notification to the providers who offer this treatment: "Treatment [Name] has been deactivated" (REQ-024-043)
  9. Sent quotes and bookings using this treatment continue unaffected; a draft quote that uses it must pick another treatment before it can be sent (REQ-024-052)
- **Outcome**: Treatment hidden from new quote creation, sent quotes and bookings honored

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
10. Provider sets the package status: "Active" or "Inactive" (default Active); "Save as Draft" keeps an unfinished package as Draft, and the form also auto-saves a draft every 30 seconds
11. Provider clicks "Save Package"
12. System validates inputs (name not empty, standard price > 0, at least one included item, plan days consecutive from Day 1)
13. System uploads images to S-05: Media Storage Service
14. System saves the package as version 1, linked to the provider account
15. System displays success message: "Package created successfully" (REQ-024-044)
16. Package now appears in provider's package list; its availability in quote creation follows FR-004

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
  10. New quote options copy the latest version (REQ-024-070)
- **Outcome**: Library package updated as a new version, earlier versions kept read-only, existing quotes unaffected
- **Note**: This is the only way to change the library package. Editing a package inside quote creation (FR-004 inline package editor) is a different path: it changes only that quote's copy and is never written back to the library (see "Package Edit Paths" in Business Rules).

**A5: Provider Deactivates Package**:

- **Trigger**: Provider no longer wants to offer a specific package (seasonal unavailability, cost changes)
- **Steps**:
  1. Provider navigates to "Products & Services > Packages"
  2. Provider clicks "Deactivate" on package card
  3. System counts the open quotes (status draft or sent) that contain a quote option copied from this package (see Usage Count in Field Calculation Rules)
  4. System displays warning: "This package is used in N open quotes. Deactivating hides it from new quotes; existing quotes are not changed." (REQ-024-072)
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
  3. System creates copy of package with "(Copy)" appended to name (REQ-024-073)
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

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---|
| Treatment Name | text | Yes | Display name of treatment (e.g., "FUE") | Max 100 chars | ENT-treatment.name |
| Treatment Type | select | Yes | Category from the managed treatment type list | Must select from the managed list | ENT-treatment.type |
| Status | badge | N/A | Visual indicator: "Draft", "Active" (green), "Inactive" (gray), or "Pending Media Upload" | Read-only display (REQ-024-048) | ENT-treatment.status |
| Video Thumbnail | image | No | Thumbnail of treatment video if available | Display CDN URL | ENT-treatment.video_thumbnail_url |
| Number of Providers | number | N/A | Count of providers currently offering this treatment | Calculated field (REQ-024-055) | ENT-treatment.provider_count |
| Last Updated | date | N/A | Timestamp of last modification | Auto-generated (REQ-024-056) | ENT-treatment.updated_at |
| Actions | buttons | N/A | Edit, Deactivate, View Details buttons | N/A | no graph field (control) |

**Business Rules**:

- Active treatments appear at top of list, inactive treatments at bottom (REQ-024-054)
- Search box filters by treatment name in real-time (REQ-024-054)
- Filter dropdown allows filtering by treatment type (REQ-024-054)
- "Create New Treatment" button always visible at top right (REQ-024-054)
- Deactivate button is always available; the confirmation warning shows how many providers and open quotes are affected (REQ-024-051; REQ-024-054)
- Edit button available for all treatments regardless of status (REQ-024-054)
- Number of providers shows count of providers who currently offer this treatment (status Offered) (REQ-024-055)

**Notes**:

- Use card-based layout for visual appeal
- Show video thumbnail as preview (hovering plays 3-second preview) (REQ-024-086)
- Display warning icon next to treatments used in active quotes when attempting deactivation (REQ-024-087)
- Pagination: 20 treatments per page (REQ-024-054)

---

#### Screen 2: Admin Treatment Creation/Edit Form

**Purpose**: Allow admin to create new treatment or edit existing treatment details, upload media assets, configure technique specifications

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---|
| Treatment Name | text | Yes | Full name of treatment | Max 100 chars, must be unique (REQ-024-046) | ENT-treatment.name |
| Treatment Type | select | Yes | Category selection from the managed treatment type list | Must select from the managed list (initial values FUE, FUT, DHI, Sapphire FUE, Robotic, Other) (REQ-024-039) | ENT-treatment.type |
| Description | textarea (markdown) | Yes | Detailed explanation of treatment | Max 5,000 chars (REQ-024-046) | ENT-treatment.description |
| Technique Specifications | textarea | No | Extraction method, implantation method, anesthesia | Max 2,000 chars (REQ-024-046) | ENT-treatment.technique_details |
| Expected Recovery Time | text | No | e.g., "7-10 days" | Max 50 chars (REQ-024-046) | ENT-treatment.recovery_time |
| Typical Duration | number | No | Procedure duration in hours | 0.5 to 12 hours (REQ-024-046) | ENT-treatment.duration_hours |
| Treatment Video | file upload | No | Educational video about treatment | MP4 format, max 50MB (REQ-024-045) | ENT-treatment.video_url |
| Treatment Images | file upload (multiple) | No | Photos showing technique or results | JPEG/PNG, max 5 images, 5MB each (REQ-024-045) | ENT-treatment.image_urls |
| Educational Resources | file upload (multiple) | No | PDF documents with additional info | PDF format, max 3 files, 10MB each (REQ-024-045) | ENT-treatment.educational_resource_urls |
| Status | select | Yes | Admin chooses Active (visible to providers) or Inactive on save; Draft is set by Save as Draft; Pending Media Upload is set by the system when a media upload fails | Default: Active (REQ-024-048) | ENT-treatment.status |

**Business Rules**:

- Treatment name must be unique across all treatments (REQ-024-046)
- Description is always required; video and images are optional (REQ-024-046; REQ-024-045)
- Video upload shows progress bar and supports resume on failure (REQ-024-088)
- Image upload allows drag-and-drop or click-to-browse (REQ-024-089)
- Markdown editor provides preview pane for description (REQ-024-090)
- Deactivating treatment triggers warning if providers currently offer it (REQ-024-051)
- Saving creates new version with timestamp (audit trail) (REQ-024-013)
- Cancel button discards changes and returns to treatment list (REQ-024-057)

**Notes**:

- Use WYSIWYG markdown editor for description field (REQ-024-090)
- Show video preview after upload (inline player) (REQ-024-091)
- Display image thumbnails after upload with remove option (REQ-024-092)
- Auto-save draft every 30 seconds to prevent data loss, and provide a "Save as Draft" button; a saved draft has status Draft and is visible to admins only (REQ-024-057)
- Provide tooltips explaining technique specifications format (REQ-024-093)
- CDN URLs generated automatically after media upload

---

#### Screen 6: Admin Treatment Types (Managed List)

**Purpose**: Allow admins to add and edit the treatment types (FUE, FUT, DHI, Sapphire FUE, Robotic, Other, and any new type) so that the Treatment Type field on Screens 1 and 2 always chooses from one managed list

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---|
| Type Name | text | Yes | Display name of the treatment type | Max 100 chars, must be unique | ENT-treatment.type |
| Last Updated | date | N/A | Timestamp of last modification | Auto-generated | no graph field |
| Actions | buttons | N/A | Add Type, Edit | N/A | no graph field (control) |

**Business Rules**:

- The list starts with FUE, FUT, DHI, Sapphire FUE, Robotic, and Other (REQ-024-039)
- Admins add new types and edit existing type names on this screen; no code change is needed to add a type (REQ-024-039)
- The Treatment Type field on Screens 1 and 2 shows exactly this list (REQ-024-039)

---

#### Screen 7: Admin Provider Packages (Read-Only View)

**Purpose**: Give admins a read-only view of a provider's package catalog for support purposes only

**Data Fields** (all display only):

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---|
| Provider Name | text (read-only) | N/A | Provider that owns the packages | Display only | ENT-provider.name |
| Package Name | text (read-only) | N/A | Display name of package | Display only | ENT-package.name |
| Included Items | text (read-only) | N/A | Short summary of the included items | Display only | ENT-package.included_items_summary |
| Standard Price | number (read-only) | N/A | Package standard price in the system quote currency | Display only | ENT-package.standard_price |
| Status | badge (read-only) | N/A | Draft, Active, or Inactive | Display only | ENT-package.status |
| Version | text (read-only) | N/A | Current library version | Display only | ENT-package.version |
| Usage Count | number (read-only) | N/A | Quote options copied from this package whose parent quote is still open | Calculated field (see Field Calculation Rules) (REQ-024-074) | ENT-package.usage_count |
| Last Updated | date (read-only) | N/A | Timestamp of last modification | Display only (REQ-024-056) | ENT-package.updated_at |
| Actions | buttons | N/A | View Details only | N/A | no graph field (control) |

**Business Rules**:

- Admin selects a provider to see that provider's packages (REQ-024-040)
- The screen offers no Edit, Clone, Deactivate, or bulk action; providers own their packages (REQ-024-040)
- View Details shows the full package version content (included items, travel services, plan, images, terms) read-only (REQ-024-040)
- The view is for support only (see Privacy Rule 2) (REQ-024-040)

---

#### Screen 8: Admin Aftercare Templates (Medication and Post-Op Instructions)

**Purpose**: Allow admins to create and edit the medication templates and the post-op instruction templates that providers use in aftercare documentation

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---|
| Template Type | select | Yes | Medication or Post-Op Instruction | Must select one | ENT-aftercare-content-template.template_type |
| Template Name | text | Yes | Display name of the template | Max 100 chars | ENT-aftercare-content-template.name |
| Template Content | textarea | Yes | For a medication: the common post-op medication preset. For an instruction: the standard instruction text providers can customize | Required | ENT-aftercare-content-template.content |
| Last Updated | date | N/A | Timestamp of last modification | Auto-generated | ENT-aftercare-content-template.updated_at |
| Actions | buttons | N/A | Add Template, Edit | N/A | no graph field (control) |

**Business Rules**:

- Only admins create and edit these templates (REQ-024-085)
- The medication templates are the one medication list providers pick from; providers cannot add medication outside this list (REQ-024-085)

---

### Provider Platform (PR-06: Profile & Settings Management)

#### Screen 3: Provider Treatment Pricing Configuration

**Purpose**: Allow provider to view admin-created treatments, configure pricing for treatments they want to offer, enable/disable treatments

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---|
| Treatment Name | text (read-only) | N/A | Name from admin catalog | Display only | ENT-treatment.name |
| Treatment Type | badge (read-only) | N/A | Category badge | Display only | ENT-treatment.type |
| Treatment Description | text (read-only, expandable) | N/A | Description from admin catalog | Display only | ENT-treatment.description |
| Treatment Video | video player | No | Video from admin catalog | Display only if available | ENT-treatment.video_url |
| Base Price | number | Yes (if offering) | Reference-only, non-binding price for the treatment; never a binding quote price and not the clinic starting price shown on provider cards | Must be > 0 (REQ-024-035; REQ-024-060) | ENT-treatment-pricing-config.base_price |
| Price Per Graft | number | No | Additional cost per graft | Must be ≥ 0 (REQ-024-060) | ENT-treatment-pricing-config.price_per_graft |
| Currency | calculated (read-only) | N/A | System quote currency from active system configuration | Display only; providers cannot choose a currency (REQ-024-032) | ENT-treatment-pricing-config.currency |
| Minimum Graft Count | number | No | Minimum grafts for this treatment | Must be > 0 and < max (REQ-024-060) | ENT-treatment-pricing-config.min_graft_count |
| Maximum Graft Count | number | No | Maximum grafts for this treatment | Must be > min (REQ-024-060) | ENT-treatment-pricing-config.max_graft_count |
| Status Toggle | toggle | Yes | "Offered" or "Not Offered" | Default: Not Offered | ENT-treatment-pricing-config.status |

**Business Rules**:

- Provider can only view active treatments from admin catalog (REQ-024-004; REQ-024-058)
- Inactive, Draft, and Pending Media Upload treatments are hidden from provider view and cannot be used (REQ-024-048)
- If provider hasn't configured pricing, treatment shows "Not Configured" badge (REQ-024-058)
- Provider must set base price to enable "Offered" status (REQ-024-059)
- See REQ-024-035 (clinic starting price: Screen 4 and Screen 5).
- See REQ-024-032.
- Maximum graft count must be greater than minimum graft count (REQ-024-060)
- Price per graft is optional (some treatments are fixed price, not graft-based) (REQ-024-060)
- Saving pricing configuration makes treatment available in quote creation (REQ-024-059)
- Provider can disable offering without deleting pricing configuration (re-enable later) (REQ-024-006)

**Notes**:

- Display treatments in card layout with expand/collapse for details (REQ-024-094)
- Show treatment video inline when card expanded (REQ-024-094)
- Provide "Quick Copy Pricing" option to copy pricing from another treatment (REQ-024-062)
- Highlight treatments not yet configured with banner at top (REQ-024-058)
- Save button becomes "Update" button when editing existing configuration (REQ-024-095)
- Display confirmation message: "Treatment pricing saved successfully" (REQ-024-044)

---

#### Screen 4: Provider Package Catalog (List View)

**Purpose**: Display all packages created by provider, allow filtering by status, provide access to create/edit/deactivate packages

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---|
| Package Name | text | Yes | Display name of package | Max 100 chars | ENT-package.name |
| Included Items | text | N/A | Short summary of the included items (e.g., "5-star hotel, airport transfer, PRP") | Show first 3 items and "+N more" (REQ-024-075) | ENT-package.included_items_summary |
| Standard Price | number | Yes | Package standard price in the system quote currency | Format with currency symbol | ENT-package.standard_price |
| Duration | text | No | e.g., "5 nights", "1 session" | Display if applicable | ENT-package.duration |
| Status | badge | Yes | "Draft", "Active" (green), or "Inactive" (grey) | Visual indicator | ENT-package.status |
| Version | text | N/A | Current library version (e.g., "v3") | Auto-generated | ENT-package.version |
| Usage Count | number | N/A | Number of quote options copied from this package whose parent quote is still open (draft or sent) | Calculated field (see Field Calculation Rules) (REQ-024-074) | ENT-package.usage_count |
| Last Updated | date | N/A | Timestamp of last modification | Auto-generated (REQ-024-056) | ENT-package.updated_at |
| Actions | buttons | N/A | Edit, Clone, Deactivate, View Details buttons | N/A | no graph field (control) |

**Business Rules**:

- Active packages appear at top of list, Inactive packages at bottom (REQ-024-076)
- Search box filters by package name in real-time (REQ-024-076)
- Filter dropdown allows filtering by status (REQ-024-076)
- "Create New Package" button always visible at top right (REQ-024-076)
- Clone button creates copy of package for quick variations (REQ-024-073)
- Deactivate button warns "used in N open quotes" when open quotes contain an option copied from this package (REQ-024-072)
- See REQ-024-074.
- Packages can be sorted by name, price, or usage count (REQ-024-076)

**Notes**:

- Use card-based layout showing package thumbnail if image uploaded
- Display status with badges (Active = green, Inactive = grey, Draft shown with its own label)
- Show quick-edit pencil icon on hover for fast price updates; a quick price edit is a library edit and saves a new package version (REQ-024-077)
- Pagination: 20 packages per page (REQ-024-076)
- Provide bulk actions: "Deactivate Selected", "Export to CSV" (REQ-024-077)

---

#### Screen 5: Provider Package Creation/Edit Form

**Purpose**: Allow provider to create a new package or edit an existing package in the library: the full quote option template of included items, travel services, relative-day plan, standard price, images, and status

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|---|
| Package Name | text | Yes | Full name of package | Max 100 chars, must be unique per provider (REQ-024-065; REQ-024-068) | ENT-package.name |
| Description | textarea (markdown) | Yes | Summary of the package | Max 2,000 chars (REQ-024-065) | ENT-package.description |
| Included Items | repeatable item list | Yes | Services the package includes. Each item has a service type (medical, travel, accommodation, transport, flight, or other), name, optional description, optional component price, and an included flag | At least one item; allowed service types only; component price ≥ 0 (REQ-024-063; REQ-024-065) | ENT-package-item.item_type, ENT-package-item.name, ENT-package-item.description, ENT-package-item.price, ENT-package-item.is_included |
| Included Travel Services | checklist | No | Flight, hotel, transport, and other travel services included in the package | Allowed values only (REQ-024-063) | ENT-package.included_travel_services |
| Relative-Day Treatment Plan | repeatable day list | No | Day number and description for each plan day | Consecutive days starting at Day 1; description required; no calendar dates (REQ-024-064; REQ-024-065) | ENT-package-plan-day.day_number, ENT-package-plan-day.description |
| Duration | text | No | e.g., "5 nights", "3 days", "1 session" | Max 50 chars (REQ-024-065) | ENT-package.duration |
| Standard Price | number | Yes | Default price that prefills each date-range price row of a quote option created from this package (FR-004) | Must be > 0; system quote currency shown read-only (REQ-024-065) | ENT-package.standard_price |
| Package Images | file upload (multiple) | No | Photos of hotel, transport, etc. | JPEG/PNG, max 3 images, 2MB each (REQ-024-067) | ENT-package.image_urls |
| Terms & Conditions | textarea | No | Package-specific terms | Max 1,000 chars (REQ-024-065) | ENT-package.terms_conditions |
| Status | select | Yes | Draft (unfinished, cannot be selected in quotes), Active (can be selected in quotes), or Inactive | Default: Active (REQ-024-057) | ENT-package.status |
| Version | text (read-only) | N/A | Current library version; saving an edit creates the next version | Auto-generated | ENT-package.version |

**Business Rules**:

- Package name must be unique within provider's package catalog (can duplicate across providers) (REQ-024-068)
- Duration field format validated for common patterns: "X nights", "X days", "X hours", "X sessions" (REQ-024-065)
- Price must be positive number with up to 2 decimal places (REQ-024-065)
- Prices are in the system quote currency from active system configuration; the form shows the currency read-only and there is no per-package currency (REQ-024-032)
- The date range, additional notes, and documents are not part of a package; providers enter them per inquiry in FR-004 (REQ-004-057)
- Image upload supports drag-and-drop or click-to-browse (REQ-024-089)
- Markdown editor for description with preview pane (REQ-024-090)
- A new package is saved as version 1, linked to the provider account; whether it can be used in quote creation follows FR-004 (REQ-024-069)
- See REQ-024-008.
- See REQ-024-072.
- Cancel button discards changes and returns to package list (REQ-024-057)

**Notes**:

- Provide starter examples (e.g., "Standard FUE with 5-night hotel and airport transfers") (REQ-024-096)
- Show image thumbnails after upload with remove/reorder options (REQ-024-092)
- Description is always required; images are optional (REQ-024-065)
- Display character count for description field (REQ-024-097)
- Auto-save a draft every 30 seconds to prevent data loss, and provide a "Save as Draft" option to save an incomplete package; a draft is a package status, is visible only to the provider's own team, and cannot be selected in a quote (REQ-024-057)
- Show success message: "Package saved successfully" (REQ-024-044)

---

## Business Rules

### General Module Rules

- **Rule 1**: All treatments are globally managed by admin and available to all active providers (REQ-024-038)
- **Rule 2**: Each provider manages their own package catalog independently
- **Rule 3**: Treatment and package versions are immutable once saved; every library edit creates a new version, and quotes keep the version they copied (REQ-024-013; REQ-024-014; REQ-024-018)
- **Rule 4**: Deactivating a package does not affect existing quotes or bookings. Deactivating a treatment does not affect sent quotes or bookings; a draft quote that uses it must pick another treatment before it can be sent (REQ-024-003; REQ-024-052)
- **Rule 5**: Pricing configuration is per-provider for treatments, per-package for packages; all library prices use the system quote currency and no treatment or package carries its own currency (REQ-024-032)
- **Rule 6**: All timestamps displayed in the user's local timezone (REQ-024-056)
- **Rule 7**: Media files (videos, images) are served via CDN with caching for performance
- **Rule 8**: A package is a full template for one quote option. It holds the included services and their prices, flight, hotel, transport, and other travel services, and the day-by-day relative treatment plan. The date range, additional notes, and documents are never packaged
- **Rule 9**: See REQ-004-033, REQ-004-016 and REQ-004-015.
- **Rule 10**: Packages are deactivated or archived, never hard-deleted, because quote options keep the source package ID and version (REQ-024-033)
- **Rule 11**: Every package field a patient can see (name, description, included items, travel services, plan, duration, images, and terms) comes from the quote option's own copy, never from the latest library version; FR-004 owns this (REQ-004-060)
- Providers have authority to set their own pricing without admin approval (REQ-024-061)
- There is no separate review step before activation: the admin who saves a treatment as Active is the approval (quality control)

### Package Edit Paths

There are two distinct ways a package's content can change. They must never be confused:

| Edit path | Where it happens | What it changes | Where it is saved | Effect on existing quotes |
|---|---|---|---|---|
| Library edit | Package management (Screen 5 in this module) | The library package | A new package version (v1, v2, and so on); earlier versions stay read-only | None. Existing quotes keep their own copy and recorded version |
| Inline edit | Quote creation (FR-004 inline package editor) | Only that quote option's copy | That quote only (quote-local copy) | None outside that quote. Never written back to the library and never creates a package version |

- A quote option records the source package ID, the source package version, and whether it was customised inline.
- FR-004 copies the package's included items, travel services, and relative-day plan into the option.
- There is no "save for future" action from an inline edit. To reuse a change, the provider repeats it as a library edit. (REQ-024-071)

### Data & Privacy Rules

- **Privacy Rule 1**: Provider package catalogs are private (not visible to other providers) (REQ-024-024)
- **Privacy Rule 2**: Admin can view provider packages in read-only mode for support purposes only (REQ-024-040)
- **Privacy Rule 3**: Treatment videos and images are served via CDN using time-limited, signed URLs (no unauthenticated bulk access) (REQ-024-080)
- **Privacy Rule 4**: Package images are accessible only to patients viewing quotes from that provider, and are resolved from the package version recorded on the quote option (REQ-024-079)
- **Audit Rule**: All treatment and package modifications logged with timestamp, user, and action (REQ-024-022)
- **Data Retention**: Deactivated treatments and packages archived, not deleted, with retention period governed by FR-023: Data Retention & Compliance (REQ-024-053)
- **Authentication**: JWT-based authentication for admin and provider platforms, tokens expire after 30 minutes
- **Encryption**: Media files encrypted at rest in S3 (AES-256), served over TLS 1.3 via CDN (REQ-024-021)
- **Compliance**: GDPR compliance for EU providers (right to export package data; package erasure requests follow FR-023 retention rules because quote history references package versions) (REQ-024-084)
- **Input validation**: Sanitize all text inputs to prevent XSS, validate file types and sizes to prevent malicious uploads (REQ-024-023)

### Integration and Operational Rules

- Cannot assign packages to providers without active provider accounts
- **Versioning**: Each treatment and package keeps one stable ID across all versions plus an integer version number. Provider pricing configuration references the stable treatment ID; FR-004 parent quotes reference treatment ID plus version, and quote options reference package ID plus version
- **Caching**: Cache treatment catalog aggressively (24-hour TTL), invalidate cache on admin edits
- Providers access platform via modern web browsers (Chrome, Firefox, Safari - last 2 versions)
- **External Service 1**: CDN (CloudFront, Cloudflare, or equivalent)
  - **Failure handling**: No fallback to direct S3 URLs; display placeholder image for failed loads (REQ-024-099)
- **External Service 2**: Media Processing Service (AWS MediaConvert or equivalent)
  - **Purpose**: Transcode uploaded treatment videos to multiple formats/resolutions for device compatibility
  - **Integration**: Trigger transcoding job on video upload, generate HLS/DASH streams for adaptive bitrate
  - **Failure handling**: Queue transcoding job for retry, notify admin if transcoding fails after 3 attempts
- **External Service 3**: Image Optimization Service (Cloudinary, imgix, or equivalent)
  - **Purpose**: Automatically resize, compress, and optimize treatment and package images
  - **Integration**: Upload original image, receive optimized versions for web/mobile display
  - **Failure handling**: Use original image if optimization fails, log error for admin review
- **Integration 1**: Admin platform sends treatment CRUD operations to shared treatment API
  - **Authentication**: Admin JWT token with elevated permissions
- **Integration 2**: Provider platform queries treatment catalog and manages packages via provider API
  - **Authentication**: Provider JWT token with clinic-scoped permissions
  - **Error handling**: Display user-friendly errors for validation failures, cache treatment catalog locally
- **Integration 3**: Quote creation workflow fetches treatment pricing and package details
  - **Error handling**: If the API is temporarily unavailable, package selection is blocked with a retry message; the system never seeds a quote option from cached data whose price or content does not match the package version it records (REQ-024-083)

### Admin Editability Rules

**Editable by Admin**:

- Complete treatment catalog (create, edit, deactivate treatments)
- Treatment names, descriptions, videos, images, technique specifications
- Treatment status (Active or Inactive on save; Draft through "Save as Draft"; Pending Media Upload is set by the system when a media upload fails) (REQ-024-048)
- Treatment types (a managed list maintained on the Treatment Types screen) (REQ-024-039)
- Medication templates and post-op instruction templates (Aftercare Templates screen) (REQ-024-085)
- Creation limits, as admin settings: treatment creation per admin per hour (default 10) and package creation per provider per hour (default 50); each is a whole number of 1 or more (REQ-024-098; REQ-024-078)

**Fixed in Codebase (Not Editable)**:

- Treatment versioning logic (automatic versioning on edit)
- Media file size limits (50MB video, 5MB images) (REQ-024-045)
- Media file format restrictions (MP4 for video, JPEG/PNG for images) (REQ-024-045)
- Package item service types (medical, travel, accommodation, transport, flight, other), aligned with FR-004 (REQ-024-063)

**Configurable with Restrictions**:

- Admin can deactivate treatments but cannot delete them (soft-delete only) (REQ-024-053)
- Admin can view provider packages but cannot edit them (provider ownership enforced) (REQ-024-040)

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
- Package image size limits (2MB per image) (REQ-024-067)

**Business Rules for Providers**:

- Provider must configure pricing for a treatment before offering it in quotes (REQ-024-059)
- See REQ-024-006.
- There is no total limit on how many packages a provider can create; package creation is limited to 50 per hour per provider by default (admin setting) (REQ-024-078)
- See REQ-024-008.
- Permission checks for package creation/editing based on staff role (REQ-024-082)

### Localization Rules

**Translatable Content** (uses i18n keys from FR-021):

- Treatment descriptions and technique specifications (REQ-024-081)
- Package names and descriptions
- All UI labels and error messages

Before production release, implementation must ensure all treatment- and package-related strings are registered with the translation management system defined in FR-021 (translation readiness checklist). (REQ-024-081)

**Non-Translatable Content** (remains in English for consistency):

- Treatment type codes (FUE, FUT, DHI, Sapphire FUE, Robotic) (REQ-024-081)
- Package item service type codes (medical, travel, accommodation, transport, flight, other)
- Media file names and CDN URLs

**Note**: This module depends on FR-021 (Multi-Language & Localization) for i18n infrastructure. FR-021 must be updated to include treatment and package content in its translation management scope.

### Field Calculation Rules

**Calculated Fields** (auto-generated, not user input):

- **Number of Providers** (Screen 1): `COUNT(provider_treatment_pricing WHERE treatment_id = X AND status = 'Offered')` (REQ-024-055)
- **Usage Count** (Screen 4): `COUNT(quote options WHERE source_package_id = X AND parent quote status IN ('draft', 'sent'))`. It counts the FR-004 quote options copied from any version of this package whose parent quote is still open. The deactivation warning "used in N open quotes" shows the number of distinct open parent quotes among them. Status values follow FR-004 (REQ-024-074)
- **Last Updated** (all screens): Database `updated_at` timestamp, displayed in user's local timezone (REQ-024-056)

---

## Dependencies

Related FRs:

- FR-004 (Module PR-02, Inquiry & Quote Management): providers select treatments and packages from this module when creating quotes
- FR-001 (Module P-01, Auth & Profile Management): provider authentication required to access package management features
- FR-009 (Module PR-01, Auth & Team Management): role-based permissions determine which provider staff can manage packages (REQ-009-003, role-based access control for provider features; REQ-009-011, provider role permissions are defined centrally in FR-031)
- FR-021 (Modules P-01, PR-06, A-09, S-02, S-03, Multi-Language & Localization): treatment descriptions, package names/descriptions require multi-language support
- FR-026 (Module A-09, App Settings & Security Policies, self-dependency): this module is part of A-09 and shares configuration infrastructure (same settings management UI patterns, audit logging, versioning mechanisms); active system configuration is the source of the system quote currency used by FR-004 for the parent quote currency
- FR-010 (Module PR-03, Treatment Execution & Documentation) and FR-011 (Module P-05, Aftercare & Progress Monitoring): providers prescribe medication and give post-op instructions from the templates this module owns; the medication templates and post-op instruction templates (REQ-024-085) are the lists those modules use, and FR-010 and FR-011 point here for ownership
- FR-029 (Payment System Configuration): exchange rates for the system quote currency

## User Scenarios & Testing

### User Story 1 - Admin Creates Comprehensive Treatment (Priority: P1)

Admin adds a new treatment type (FUE) to the platform catalog with video, images, and detailed description so that providers can offer this treatment to patients.

**Why this priority**: Treatment catalog is foundation for entire quote system. Without treatments, providers cannot create quotes. This is the most critical workflow.

**Independent Test**: Can be fully tested by creating a treatment with all fields, verifying it appears in admin catalog, and confirming providers can view it in their treatment selection.

**Acceptance Scenarios**:

1. **Given** admin is logged into admin platform, **When** admin navigates to "Settings > Treatment Settings" and clicks "Create New Treatment", **Then** system displays treatment creation form with all fields (name, type, description, video upload, image upload, technique specs)
2. **Given** admin fills out treatment form with valid data and uploads 50MB video, **When** admin clicks "Save Treatment", **Then** system uploads video to S3, generates CDN URL, saves the treatment with the status the admin chose (default Active), and displays success message
3. **Given** new treatment is saved, **When** provider navigates to "Products & Services > Treatments > Treatment Pricing", **Then** provider sees new treatment in available treatment list and can configure pricing

---

### User Story 2 - Provider Configures Treatment Pricing (Priority: P1)

Provider views admin-created treatments and configures pricing for treatments they want to offer so they can include these treatments in quotes.

**Why this priority**: Without pricing configuration, providers cannot use treatments in quotes. This workflow must work before quote creation is possible.

**Independent Test**: Can be fully tested by selecting a treatment, entering pricing details, saving configuration, and verifying treatment appears in quote creation workflow.

**Acceptance Scenarios**:

1. **Given** provider is logged into provider platform, **When** provider navigates to "Products & Services > Treatments > Treatment Pricing", **Then** system displays list of all active treatments from admin catalog
2. **Given** provider selects treatment to configure, **When** provider enters base price (£2,500), price per graft (£2.00), graft range (1,000-5,000), and toggles status to "Offered", **Then** system saves pricing configuration and displays success message
3. **Given** provider has configured treatment pricing, **When** provider creates new quote and selects treatment, **Then** the treatment appears in the quote; the configured Base Price is a reference only and may prefill a price row only where FR-004 allows (REQ-004-044)

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
2. **Given** the three options exist, **When** the system prefills prices, **Then** the prefill and the editing of date-range price rows follow FR-004 (REQ-004-033, REQ-004-044); package prices are never summed into one option
3. **Given** provider has selected five packages, **When** provider tries to select a sixth, **Then** the selection limit follows FR-004 (REQ-004-015)
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

- **What happens when admin uploads 100MB video exceeding 50MB limit?** System displays validation error: "Video file exceeds maximum size of 50MB. Please compress the video or upload a shorter version." Admin must compress video or split into shorter segments. (REQ-024-045)

- **How does system handle provider creating package with name that already exists in their catalog?** System validates package name uniqueness per provider. If duplicate name detected, system displays error: "A package with this name already exists. Please choose a different name or edit the existing package." (REQ-024-068)

- **What occurs if provider configures treatment pricing with maximum graft count less than minimum?** System validates that max > min during form submission. If validation fails, system displays error next to max field: "Maximum graft count must be greater than minimum graft count." (REQ-024-060)

- **How to manage provider selecting deactivated treatment during quote creation?** Provider cannot select deactivated treatments. If treatment is deactivated while provider has draft quote open, system refreshes available treatments and displays warning: "Treatment [Name] is no longer available. Please select a different treatment." (REQ-024-052)

- **What happens when media upload fails during treatment creation?** System retries upload 3 times with exponential backoff. If all retries fail, system saves treatment record with status "Pending Media Upload" and displays error: "Video upload failed. Treatment saved without media. You can upload the video later by editing the treatment." Providers do not see or use a treatment in Pending Media Upload status until media is added. Admin can edit treatment to retry upload. After a successful retry the treatment takes the status the admin picks on that save (Active or Inactive). (REQ-024-049; REQ-024-100)

- **What occurs if two admins simultaneously edit the same treatment?** See system PRD, Platform-Wide Rules: Concurrent admin edits: warn, then last save wins. If the admin continues, the save becomes the current version and the earlier version stays in the version history.

---

## Functional Requirements Summary

### Core Requirements

- **REQ-024-001**: System MUST allow admins to create treatments with name, type, description, video, images, and technique specifications
- **REQ-024-002**: System MUST allow admins to edit existing treatments, creating new versions without modifying historical records
- **REQ-024-003**: System MUST allow admins to activate or deactivate treatments, affecting availability for new quotes and draft quotes only; sent quotes and bookings are not affected
- **REQ-024-004**: System MUST allow providers to view all active treatments from admin catalog
- **REQ-024-005**: System MUST allow providers to configure pricing for treatments they want to offer (base price, price per graft, graft ranges)
- **REQ-024-006**: System MUST allow providers to enable or disable treatment offerings without deleting pricing configuration
- **REQ-024-007**: System MUST allow providers to create packages with name, description, included items, included travel services, relative-day treatment plan, standard price, images, and status (Draft, Active, or Inactive)
- **REQ-024-008**: System MUST allow providers to edit existing packages in the package library; each save MUST create a new package version (v1, v2, and so on), keep earlier versions read-only, and never change existing quotes
- **REQ-024-009**: System MUST allow providers to deactivate packages, hiding them from new quotes while preserving existing quotes
- Quote selection of one treatment and one to five Active packages, the one-alternative-option-per-package rule, the standard-price prefill, and the Treatment and Package ID/version kept on the quote are owned by FR-004: REQ-004-033 and REQ-004-016 (see also REQ-004-001 and REQ-004-015). Formerly REQ-024-010, REQ-024-011, and REQ-024-012
- Inline package edits made during quote creation stay in that quote only and are never written back to the library package: owned by FR-004, REQ-004-017 and REQ-004-034. Formerly REQ-024-030
- A package never stores a date range, additional notes, or documents; they are entered per inquiry in FR-004 (REQ-004-057). Formerly REQ-024-031
- **REQ-024-032**: System MUST use the system quote currency for all treatment and package library prices; providers MUST NOT choose a currency per treatment or package
- **REQ-024-033**: System MUST NOT hard-delete packages; packages are deactivated or archived only
- Patients see package content only from the quote option's own copy: owned by FR-004, REQ-004-060. Formerly REQ-024-034
- **REQ-024-035**: System MUST treat the provider treatment Base Price as a reference-only, non-binding value. It is not the clinic starting price: a clinic starting price is the lowest standard price among its active packages. Base Price MUST NOT be binding and MUST NOT be read after a quote is sent. Whether it prefills a new quote price row is owned by FR-004 (REQ-004-044)
- **REQ-024-085**: System MUST allow admins to manage the medication templates (common post-op medication presets that speed up prescribing) and the post-op instruction templates (standard instruction text that providers can customize). The medication templates are the one admin medication list providers pick medication from; the FR-011 medication catalogue is this same list

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

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-11-22 | 1.8 | Requirements graph programme baseline: PRD compressed to the checklist structure (each rule stated once, field rows tagged with graph field ids, dropped classes removed). No rule changes. Earlier history (v1.0 to v1.7) and the change requests CR-FR024-20261016-01 (change-request-2026-10-16-mtg002-quote-model-alignment.md) and change-request-2026-09-10-quote-option-provenance-alignment.md are in `archived/prd-baseline-2026-11-08/` and in git history. | Product Owner / Documentation |

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
**Last Updated**: 2026-11-22
