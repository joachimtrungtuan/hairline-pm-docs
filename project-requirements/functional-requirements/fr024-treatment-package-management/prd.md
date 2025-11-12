# Product Requirements Document: Treatment & Package Management

**Module**: A-09: System Settings & Configuration | PR-06: Profile & Settings Management
**Feature Branch**: `fr024-treatment-package-management`
**Created**: 2025-11-12
**Status**: Draft
**Source**: FR-024 from system-prd.md

---

## Executive Summary

The Treatment & Package Management module establishes a two-tier content management system for medical procedures and service packages within the Hairline platform. This module defines clear content ownership boundaries: treatments (FUE, FUT, DHI, etc.) are centrally managed by admins to ensure consistency across all providers, while packages (hotel accommodations, transport, medications, etc.) are managed by individual providers to enable competitive differentiation. This separation creates a foundation for quote generation while providing flexibility for future platform-managed services.

This module directly impacts provider quote submission capabilities and ensures patients receive consistent treatment information regardless of which provider they choose. The architectural decision to separate treatments from packages supports the platform's long-term vision of transitioning provider-managed travel services to platform-managed services without disrupting the treatment catalog.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-XX)**: Views treatment information and package details within provider quotes
- **Provider Platform (PR-06)**: Manages their own packages and selects from admin-created treatments when building quotes
- **Admin Platform (A-09)**: Creates and manages the master treatment catalog available to all providers
- **Shared Services (S-XX)**: None specific to this module

### Multi-Tenant Breakdown

**Patient Platform (P-02: Quote Request & Management)**:

- Patients view treatment details (videos, descriptions, technique information) within provider quotes
- Patients see package options (hotel tiers, transport, medications) offered by each provider
- Patients compare treatment and package offerings across multiple provider quotes
- No direct treatment or package management actions available to patients

**Provider Platform (PR-06: Profile & Settings Management)**:

- Providers access the admin-created treatment catalog
- Providers cannot create custom treatments (ensures standardization)
- Providers configure pricing for each treatment type they offer
- Providers create and manage their own package catalog
- Providers define package types: hotel, transport, flights, medications, PRP, consultations
- Providers set pricing and availability for each package
- Providers can enable/disable treatments and packages without deleting them
- Providers select treatments and packages when creating quotes

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

- Admin navigates to "Settings > Treatment Catalog" in admin platform
- Admin selects "Create New Treatment" to add treatment type
- Admin edits existing treatment by selecting from treatment list

**Provider Entry Points**:

- Provider navigates to "Settings > Services" in provider platform
- Provider accesses "Treatment Pricing" to configure pricing for admin-created treatments
- Provider navigates to "Settings > Packages" to manage their package catalog
- Provider selects "Create Package" to add new package offering
- During quote creation, provider selects from available treatments and packages

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

1. Admin navigates to "Settings > Treatment Catalog" in admin platform
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
  1. Admin navigates to "Settings > Treatment Catalog"
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
  3. System checks if any active quotes or scheduled bookings use this treatment
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
  1. Provider navigates to "Settings > Services > Treatment Pricing"
  2. System displays list of all active treatments from admin catalog
  3. Provider selects treatment to configure
  4. Provider enters pricing details:
     - Base price for treatment
     - Price per graft (if applicable)
     - Currency selection
     - Minimum graft count
     - Maximum graft count
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
**Outcome**: New package available for provider to include in quotes

**Steps**:

1. Provider navigates to "Settings > Packages" in provider platform
2. Provider clicks "Create New Package" button
3. System displays package creation form
4. Provider selects package type from dropdown:
   - Hotel Package
   - Transport Package
   - Flight Assistance Package
   - Medication Package
   - PRP Therapy Add-On
   - Extended Consultation Package
   - Custom Package (other)
5. Provider enters package details:
   - Package name (e.g., "5-Star Hotel - 5 Nights")
   - Description (what's included)
   - Duration (days/nights if applicable)
   - Pricing (amount and currency)
   - Availability status: "Available" or "Unavailable"
6. Provider uploads package images (optional, max 3 images, 2MB each)
7. Provider adds package terms and conditions (optional, markdown supported)
8. Provider clicks "Save Package"
9. System validates inputs (name not empty, price > 0, currency valid)
10. System uploads images to S-05: Media Storage Service
11. System saves package record linked to provider account
12. System displays success message: "Package created successfully"
13. Package now appears in provider's package list and is selectable during quote creation

### Alternative Flows (Packages)

**A4: Provider Edits Existing Package**:

- **Trigger**: Provider needs to update package details (pricing, description, availability)
- **Steps**:
  1. Provider navigates to "Settings > Packages"
  2. Provider searches or filters for package to edit
  3. Provider clicks "Edit" on package card
  4. System displays package edit form with current values
  5. Provider modifies fields (price, description, images, availability)
  6. Provider clicks "Update Package"
  7. System creates new version of package (versioning for audit trail)
  8. System updates package record
  9. Existing quotes using this package remain unchanged (version locked)
  10. New quotes will use updated package version
- **Outcome**: Package updated, new quotes use latest version, historical quotes unaffected

**A5: Provider Deactivates Package**:

- **Trigger**: Provider no longer wants to offer a specific package (seasonal unavailability, cost changes)
- **Steps**:
  1. Provider navigates to "Settings > Packages"
  2. Provider clicks "Deactivate" on package card
  3. System checks if any active quotes include this package
  4. System displays warning: "X active quotes include this package"
  5. Provider confirms deactivation
  6. System changes package status to "Unavailable"
  7. System prevents provider from adding this package to new quotes
  8. Existing quotes with this package remain valid (version locked)
- **Outcome**: Package hidden from new quotes, existing commitments honored

**A6: Provider Clones Package**:

- **Trigger**: Provider wants to create similar package with slight variations (e.g., 3-night vs 5-night hotel)
- **Steps**:
  1. Provider navigates to "Settings > Packages"
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
     - Invalid currency code
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

### Screen 1: Admin Treatment Catalog (List View)

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

### Screen 2: Admin Treatment Creation/Edit Form

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

### Screen 3: Provider Treatment Pricing Configuration

**Purpose**: Allow provider to view admin-created treatments, configure pricing for treatments they want to offer, enable/disable treatments

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Treatment Name | text (read-only) | N/A | Name from admin catalog | Display only |
| Treatment Type | badge (read-only) | N/A | Category badge | Display only |
| Treatment Description | text (read-only, expandable) | N/A | Description from admin catalog | Display only |
| Treatment Video | video player | No | Video from admin catalog | Display only if available |
| Base Price | number | Yes (if offering) | Starting price for treatment | Must be > 0 |
| Price Per Graft | number | No | Additional cost per graft | Must be ≥ 0 |
| Currency | select | Yes (if offering) | Currency for pricing | Provider's default currency pre-selected |
| Minimum Graft Count | number | No | Minimum grafts for this treatment | Must be > 0 and < max |
| Maximum Graft Count | number | No | Maximum grafts for this treatment | Must be > min |
| Status Toggle | toggle | Yes | "Offered" or "Not Offered" | Default: Not Offered |

**Business Rules**:

- Provider can only view active treatments from admin catalog
- Inactive treatments are hidden from provider view
- If provider hasn't configured pricing, treatment shows "Not Configured" badge
- Provider must set base price to enable "Offered" status
- Currency defaults to provider's account currency but can be changed per treatment
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

### Screen 4: Provider Package Catalog (List View)

**Purpose**: Display all packages created by provider, allow filtering by package type, provide access to create/edit/deactivate packages

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Package Name | text | Yes | Display name of package | Max 100 chars |
| Package Type | badge | Yes | Category: Hotel, Transport, Flights, Medication, PRP, Consultation, Custom | Display as colored badge |
| Pricing | number | Yes | Package price | Format with currency symbol |
| Duration | text | No | e.g., "5 nights", "1 session" | Display if applicable |
| Availability | badge | Yes | "Available" (green) or "Unavailable" (gray) | Visual indicator |
| Usage Count | number | N/A | Number of quotes including this package | Calculated field |
| Last Updated | date | N/A | Timestamp of last modification | Auto-generated |
| Actions | buttons | N/A | Edit, Clone, Deactivate, View Details buttons | N/A |

**Business Rules**:

- Available packages appear at top of list, unavailable packages at bottom
- Search box filters by package name in real-time
- Filter dropdown allows filtering by package type
- "Create New Package" button always visible at top right
- Clone button creates copy of package for quick variations
- Deactivate button warns if package is in active quotes
- Usage count shows how many times package has been included in quotes
- Packages can be sorted by name, price, type, or usage count

**Notes**:

- Use card-based layout showing package thumbnail if image uploaded
- Display package type with color-coded badges (Hotel = blue, Transport = green, etc.)
- Show quick-edit pencil icon on hover for fast price updates
- Pagination: 20 packages per page
- Provide bulk actions: "Deactivate Selected", "Export to CSV"

---

### Screen 5: Provider Package Creation/Edit Form

**Purpose**: Allow provider to create new package or edit existing package details, upload package images, configure pricing and availability

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Package Name | text | Yes | Full name of package | Max 100 chars, must be unique per provider |
| Package Type | select | Yes | Category selection | Hotel, Transport, Flights, Medication, PRP, Consultation, Custom |
| Description | textarea (markdown) | Yes | What's included in package | Max 2,000 chars |
| Duration | text | No | e.g., "5 nights", "3 days", "1 session" | Max 50 chars |
| Price | number | Yes | Package price | Must be > 0 |
| Currency | select | Yes | Currency for pricing | Provider's default currency pre-selected |
| Package Images | file upload (multiple) | No | Photos of hotel, transport, etc. | JPEG/PNG, max 3 images, 2MB each |
| Terms & Conditions | textarea | No | Package-specific terms | Max 1,000 chars |
| Availability Status | toggle | Yes | Available (can be added to quotes) or Unavailable | Default: Available |

**Business Rules**:

- Package name must be unique within provider's package catalog (can duplicate across providers)
- Duration field format validated for common patterns: "X nights", "X days", "X hours", "X sessions"
- Price must be positive number with up to 2 decimal places
- Currency defaults to provider account currency but can be changed per package
- Image upload supports drag-and-drop or click-to-browse
- Markdown editor for description with preview pane
- Saving package makes it immediately available in quote creation
- Deactivating package requires confirmation if used in active quotes
- Cancel button discards changes and returns to package list

**Notes**:

- Provide package templates for common types (5-star hotel, airport transport, etc.)
- Auto-suggest package names based on type selection
- Show image thumbnails after upload with remove/reorder options
- Validate that at least one of: description or images is provided
- Display character count for description field
- Provide "Save as Draft" option to save incomplete package
- Show success message: "Package saved successfully"

---

### Screen 6: Quote Creation - Treatment & Package Selection (Provider)

**Purpose**: Allow provider to select treatment and packages when creating a quote for patient inquiry, display pricing summary

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Treatment Selection | dropdown/cards | Yes | Select one treatment from configured treatments | Must select exactly one |
| Treatment Price | number (read-only) | N/A | Base price for selected treatment | Display from configuration |
| Graft Count | number | Yes | Estimated graft count for patient | Must be between min/max for treatment |
| Graft Price | number (calculated) | N/A | Graft count × price per graft | Auto-calculated if applicable |
| Package Selection | checkbox list | No | Select zero or more packages to include | Multiple selection allowed |
| Package Prices | number (read-only) | N/A | Price for each selected package | Display from package configuration |
| Subtotal | number (calculated) | N/A | Treatment + graft + packages | Auto-calculated |
| Discount | number | No | Optional discount amount or percentage | Must be ≥ 0 and ≤ subtotal |
| Total Quote Amount | number (calculated) | Yes | Final amount after discount | Auto-calculated, read-only |

**Business Rules**:

- Only treatments configured with "Offered" status appear in selection
- Only packages with "Available" status appear in selection
- Treatment selection is required, package selection is optional
- Graft count must be within min/max range defined in treatment configuration
- If treatment has no graft-based pricing, graft count field is hidden
- Package selection shows package type icons for quick visual identification
- Discount field validates that discount doesn't exceed subtotal
- Total quote amount updates in real-time as selections change
- Selected treatment and packages are locked into quote version upon submission

**Notes**:

- Display treatment cards with video thumbnail and description preview
- Show package checkboxes with images and pricing
- Real-time pricing calculator on right sidebar
- Highlight recommended packages based on patient inquiry details
- Provide "Bundle Discount" option to apply discount to specific package combinations
- Display currency consistently throughout (based on provider account default)
- Save quote draft automatically every 30 seconds

---

## Business Rules

### General Module Rules

- **Rule 1**: All treatments are globally managed by admin and available to all active providers
- **Rule 2**: Each provider manages their own package catalog independently
- **Rule 3**: Treatment and package versions are immutable once included in a quote (changes create new versions)
- **Rule 4**: Deactivating treatments or packages does not affect existing quotes or bookings
- **Rule 5**: Pricing configuration is per-provider for treatments, per-package for packages
- **Rule 6**: All timestamps displayed in provider's local timezone
- **Rule 7**: Media files (videos, images) are served via CDN with caching for performance

### Data & Privacy Rules

- **Privacy Rule 1**: Provider package catalogs are private (not visible to other providers)
- **Privacy Rule 2**: Admin can view provider packages in read-only mode for support purposes only
- **Privacy Rule 3**: Treatment videos and images are publicly accessible via CDN (no authentication required)
- **Privacy Rule 4**: Package images are accessible only to patients viewing quotes from that provider
- **Audit Rule**: All treatment and package modifications logged with timestamp, user, and action
- **Data Retention**: Deactivated treatments and packages archived, not deleted (7-year retention for audit)

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
- Package type categories (enum values: Hotel, Transport, Flights, Medication, PRP, Consultation, Custom)

**Configurable with Restrictions**:

- Admin can deactivate treatments but cannot delete them (soft-delete only)
- Admin can view provider packages but cannot edit them (provider ownership enforced)

### Provider Editability Rules

**Editable by Provider**:

- Treatment pricing configuration (base price, price per graft, graft count ranges)
- Treatment offering status (offered/not offered per treatment)
- Complete package catalog for their clinic (create, edit, deactivate packages)
- Package pricing, descriptions, images, availability status

**Fixed in Codebase (Not Editable by Provider)**:

- Treatment catalog itself (cannot create custom treatments)
- Treatment names, descriptions, videos from admin catalog (read-only)
- Package versioning logic (automatic versioning on edit)
- Package image size limits (2MB per image)

**Business Rules for Providers**:

- Provider must configure pricing for a treatment before offering it in quotes
- Provider can disable treatment offering without deleting pricing configuration
- Provider can create unlimited packages (no platform-imposed limit)
- Provider cannot modify packages already included in submitted quotes (version locked)

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
  - **Integration point**: Quote creation workflow calls treatment/package APIs to fetch available options and pricing

- **FR-001 / Module P-01**: Auth & Profile Management
  - **Why needed**: Provider authentication required to access package management features
  - **Integration point**: Admin and provider authentication tokens used to authorize treatment and package operations

- **FR-009 / Module PR-01**: Auth & Team Management
  - **Why needed**: Role-based permissions determine which provider staff can manage packages
  - **Integration point**: Permission checks for package creation/editing based on staff role

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

- **Entity 2**: Currency Exchange Rates
  - **Why needed**: Display treatment prices in multiple currencies for international patients
  - **Source**: Payment system configuration (FR-029: Payment System Configuration)

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
- **Assumption 4**: Package types (hotel, transport, etc.) are relatively stable (infrequent addition of new types)
- **Assumption 5**: Provider package catalogs will grow over time as providers expand offerings
- **Assumption 6**: Treatment deactivation is rare (only for compliance or safety issues)

---

## Implementation Notes

### Technical Considerations

- **Architecture**: Treatment catalog uses centralized database table shared by all tenants, package catalog uses tenant-scoped tables
- **Versioning**: Implement immutable versioning for treatments and packages (new record on edit, not update-in-place)
- **Media Storage**: Use S3-compatible object storage with CDN integration for global delivery
- **Caching**: Cache treatment catalog aggressively (24-hour TTL), invalidate cache on admin edits
- **Performance**: Index treatment names, types, and status for fast filtering, index package names and types for provider searches

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
  - **Error handling**: Fallback to last-known-good pricing if API temporarily unavailable

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
- **Compliance**: GDPR compliance for EU providers (right to export package data, right to delete packages)
- **Input validation**: Sanitize all text inputs to prevent XSS, validate file types and sizes to prevent malicious uploads

---

## User Scenarios & Testing

### User Story 1 - Admin Creates Comprehensive Treatment (Priority: P1)

Admin adds a new treatment type (FUE) to the platform catalog with video, images, and detailed description so that providers can offer this treatment to patients.

**Why this priority**: Treatment catalog is foundation for entire quote system. Without treatments, providers cannot create quotes. This is the most critical workflow.

**Independent Test**: Can be fully tested by creating a treatment with all fields, verifying it appears in admin catalog, and confirming providers can view it in their treatment selection.

**Acceptance Scenarios**:

1. **Given** admin is logged into admin platform, **When** admin navigates to "Settings > Treatment Catalog" and clicks "Create New Treatment", **Then** system displays treatment creation form with all fields (name, type, description, video upload, image upload, technique specs)
2. **Given** admin fills out treatment form with valid data and uploads 50MB video, **When** admin clicks "Save Treatment", **Then** system uploads video to S3, generates CDN URL, saves treatment record with "Active" status, and displays success message
3. **Given** new treatment is saved, **When** provider navigates to "Settings > Treatment Pricing", **Then** provider sees new treatment in available treatment list and can configure pricing

---

### User Story 2 - Provider Configures Treatment Pricing (Priority: P1)

Provider views admin-created treatments and configures pricing for treatments they want to offer so they can include these treatments in quotes.

**Why this priority**: Without pricing configuration, providers cannot use treatments in quotes. This workflow must work before quote creation is possible.

**Independent Test**: Can be fully tested by selecting a treatment, entering pricing details, saving configuration, and verifying treatment appears in quote creation workflow.

**Acceptance Scenarios**:

1. **Given** provider is logged into provider platform, **When** provider navigates to "Settings > Services > Treatment Pricing", **Then** system displays list of all active treatments from admin catalog
2. **Given** provider selects treatment to configure, **When** provider enters base price (£2,500), price per graft (£2.00), graft range (1,000-5,000), and toggles status to "Offered", **Then** system saves pricing configuration and displays success message
3. **Given** provider has configured treatment pricing, **When** provider creates new quote and selects treatment, **Then** treatment appears in quote with configured pricing auto-populated

---

### User Story 3 - Provider Creates Hotel Package (Priority: P1)

Provider creates a hotel package offering (5-star hotel, 5 nights) with description, images, and pricing so they can include this package in quotes as an optional add-on.

**Why this priority**: Packages are essential for providers to differentiate their offerings and provide comprehensive quotes. Hotel packages are the most commonly offered package type.

**Independent Test**: Can be fully tested by creating a package with all details, verifying it appears in provider's package catalog, and confirming it can be selected during quote creation.

**Acceptance Scenarios**:

1. **Given** provider is logged into provider platform, **When** provider navigates to "Settings > Packages" and clicks "Create New Package", **Then** system displays package creation form
2. **Given** provider fills out package form (name: "5-Star Hotel - 5 Nights", type: Hotel, description, duration: "5 nights", price: £300, uploads 3 images), **When** provider clicks "Save Package", **Then** system uploads images to S3, saves package record, and displays success message
3. **Given** package is saved, **When** provider creates quote and views package selection, **Then** new package appears in available packages list with images and pricing displayed

---

### User Story 4 - Provider Selects Treatment and Packages in Quote (Priority: P2)

Provider creates a quote by selecting one treatment and multiple packages, system calculates total price dynamically so provider can review before submitting quote to patient.

**Why this priority**: This is the primary use case for treatments and packages, but depends on treatments and packages already being configured (P1 dependencies).

**Independent Test**: Can be fully tested by creating a quote with treatment + packages, verifying pricing calculations are correct, and confirming quote submission succeeds.

**Acceptance Scenarios**:

1. **Given** provider is creating quote for patient inquiry, **When** provider selects treatment (FUE) and enters graft count (3,000), **Then** system displays treatment base price (£2,500) + graft price (3,000 × £2.00 = £6,000) = subtotal £8,500
2. **Given** provider adds packages (hotel: £300, transport: £50, medications: £100), **When** packages are selected, **Then** system updates total to £8,950 (treatment + packages)
3. **Given** provider reviews quote with treatment and packages, **When** provider submits quote, **Then** system locks treatment and package versions, creates quote record, and notifies patient

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

1. **Given** provider navigates to package catalog, **When** provider clicks "Deactivate" on package with active quotes, **Then** system displays warning: "This package is included in 5 active quotes. Deactivating will hide it from new quotes but existing quotes will remain valid."
2. **Given** provider confirms deactivation, **When** system processes deactivation, **Then** package status changes to "Unavailable", package is hidden from quote creation workflow, and existing quotes retain package with locked version
3. **Given** package is deactivated, **When** provider creates new quote and views package selection, **Then** deactivated package does not appear in available packages list

---

### Edge Cases

- **What happens when admin uploads 100MB video exceeding 50MB limit?** System displays validation error: "Video file exceeds maximum size of 50MB. Please compress the video or upload a shorter version." Admin must compress video or split into shorter segments.

- **How does system handle provider creating package with name that already exists in their catalog?** System validates package name uniqueness per provider. If duplicate name detected, system displays error: "A package with this name already exists. Please choose a different name or edit the existing package."

- **What occurs if provider configures treatment pricing with maximum graft count less than minimum?** System validates that max > min during form submission. If validation fails, system displays error next to max field: "Maximum graft count must be greater than minimum graft count."

- **How to manage provider selecting deactivated treatment during quote creation?** Provider cannot select deactivated treatments. If treatment is deactivated while provider has draft quote open, system refreshes available treatments and displays warning: "Treatment [Name] is no longer available. Please select a different treatment."

- **What happens when media upload fails during treatment creation?** System retries upload 3 times with exponential backoff. If all retries fail, system saves treatment record with status "Pending Media Upload" and displays error: "Video upload failed. Treatment saved without media. You can upload the video later by editing the treatment." Admin can edit treatment to retry upload.

- **How does system handle currency conversion when provider changes treatment currency?** System locks exchange rate at time of pricing configuration save. If provider later changes currency, system prompts: "Changing currency will recalculate price using current exchange rate. This will affect new quotes but not existing quotes." Provider confirms and system updates pricing with locked exchange rate for future quotes.

- **What occurs if two admins simultaneously edit the same treatment?** System uses optimistic locking with version timestamps. When second admin attempts to save, system detects concurrent edit and displays error: "This treatment was modified by another admin. Please refresh and reapply your changes." Second admin must reload treatment and reapply edits.

---

## Functional Requirements Summary

### Core Requirements

- **FR-001**: System MUST allow admins to create treatments with name, type, description, video, images, and technique specifications
- **FR-002**: System MUST allow admins to edit existing treatments, creating new versions without modifying historical records
- **FR-003**: System MUST allow admins to activate or deactivate treatments, affecting availability for new quotes only
- **FR-004**: System MUST allow providers to view all active treatments from admin catalog
- **FR-005**: System MUST allow providers to configure pricing for treatments they want to offer (base price, price per graft, graft ranges)
- **FR-006**: System MUST allow providers to enable or disable treatment offerings without deleting pricing configuration
- **FR-007**: System MUST allow providers to create packages with name, type, description, pricing, images, and availability status
- **FR-008**: System MUST allow providers to edit existing packages, creating new versions without affecting active quotes
- **FR-009**: System MUST allow providers to deactivate packages, hiding them from new quotes while preserving existing quotes
- **FR-010**: System MUST allow providers to select one treatment and zero or more packages when creating quotes
- **FR-011**: System MUST calculate quote total dynamically based on selected treatment, graft count, and packages
- **FR-012**: System MUST lock treatment and package versions in quotes to prevent retroactive price changes

### Data Requirements

- **FR-013**: System MUST maintain versioned treatment records with immutable history (no update-in-place)
- **FR-014**: System MUST maintain versioned package records with immutable history
- **FR-015**: System MUST store media files (videos, images) in S3-compatible object storage with CDN delivery
- **FR-016**: System MUST track which providers offer which treatments (provider-treatment pricing configuration)
- **FR-017**: System MUST link packages to provider accounts (package ownership)
- **FR-018**: System MUST preserve treatment and package versions used in historical quotes and bookings

### Security & Privacy Requirements

- **FR-019**: System MUST restrict treatment creation/editing to admin users only
- **FR-020**: System MUST restrict package management to provider users (edit only their own packages)
- **FR-021**: System MUST serve media files via CDN over TLS 1.3 (HTTPS)
- **FR-022**: System MUST log all treatment and package modifications with timestamp, user ID, IP address, and old/new values
- **FR-023**: System MUST validate uploaded media files for type, size, and malicious content
- **FR-024**: System MUST prevent providers from viewing other providers' package catalogs

### Integration Requirements

- **FR-025**: System MUST expose REST API for treatment CRUD operations (admin access only)
- **FR-026**: System MUST expose REST API for package CRUD operations (provider access only)
- **FR-027**: System MUST integrate with S-05: Media Storage Service for video and image uploads
- **FR-028**: System MUST integrate with CDN service for media file delivery
- **FR-029**: System MUST integrate with PR-02: Inquiry & Quote Management for treatment and package selection during quote creation

---

## Key Entities

- **Entity 1 - Treatment**
  - **Key attributes**: treatment_id (UUID), name (string), type (enum), description (text), video_url (string), image_urls (array), technique_specifications (text), recovery_time (string), duration_hours (float), status (enum: active/inactive), version (integer), created_at (timestamp), updated_at (timestamp), created_by_admin_id (UUID)
  - **Relationships**: One treatment can have many provider pricing configurations (one-to-many). One treatment version can be referenced by many quotes (one-to-many).

- **Entity 2 - TreatmentPricingConfiguration**
  - **Key attributes**: pricing_id (UUID), provider_id (UUID), treatment_id (UUID), base_price (decimal), price_per_graft (decimal), currency (string), min_graft_count (integer), max_graft_count (integer), status (enum: offered/not_offered), created_at (timestamp), updated_at (timestamp)
  - **Relationships**: Belongs to one provider (many-to-one). Belongs to one treatment (many-to-one).

- **Entity 3 - Package**
  - **Key attributes**: package_id (UUID), provider_id (UUID), name (string), type (enum: hotel/transport/flights/medication/prp/consultation/custom), description (text), duration (string), price (decimal), currency (string), image_urls (array), terms_conditions (text), status (enum: available/unavailable), version (integer), created_at (timestamp), updated_at (timestamp)
  - **Relationships**: Belongs to one provider (many-to-one). One package version can be referenced by many quotes (one-to-many).

- **Entity 4 - QuoteTreatment** (linking entity)
  - **Key attributes**: quote_treatment_id (UUID), quote_id (UUID), treatment_id (UUID), treatment_version (integer), graft_count (integer), treatment_price (decimal), graft_price (decimal), total_treatment_cost (decimal)
  - **Relationships**: Belongs to one quote (many-to-one). References one treatment version (many-to-one, versioned).

- **Entity 5 - QuotePackage** (linking entity)
  - **Key attributes**: quote_package_id (UUID), quote_id (UUID), package_id (UUID), package_version (integer), package_price (decimal)
  - **Relationships**: Belongs to one quote (many-to-one). References one package version (many-to-one, versioned).

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-12 | 1.0 | Initial PRD creation for FR-024 Treatment & Package Management | AI Assistant |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | [Name] | [Date] | [Status] |
| Technical Lead | [Name] | [Date] | [Status] |
| Stakeholder | [Name] | [Date] | [Status] |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-011 Aftercare & Recovery Management PRD
**Last Updated**: 2025-11-12
