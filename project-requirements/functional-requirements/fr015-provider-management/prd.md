# Product Requirements Document: Provider Management (Admin-Initiated)

**Module**: A-02: Provider Management & Onboarding
**Feature Branch**: `fr015-provider-management`
**Created**: 2025-11-11
**Status**: Draft
**Source**: FR-015 from system-prd.md (lines 1013-1041)

---

## Executive Summary

The Provider Management module enables administrators to onboard and manage hair transplant providers who will serve patients through the Hairline platform. This module is strictly admin-initiated—there is no self-service provider registration. Admins manually create provider accounts using a wizard-style interface, upload required documentation (for record-keeping), configure commission structures (Percentage or Flat Rate), and manage provider lifecycle status. The module also includes featured provider designation to control visibility in the patient-facing application. This module operates as the foundational gateway for the provider network, ensuring that all providers have valid profiles and agreed-upon commission terms before accepting bookings.

**Cross-Module Integration:** Providers can manage their own profile information (Bio, Languages, Awards, Logo) through **FR-032: Provider Dashboard Settings & Profile Management**. Changes made by providers in their dashboard automatically sync with the admin view, ensuring data consistency across platforms.

**Note:** Document verification is performed externally; the system treats uploaded documents as pre-verified records and does not block account activation based on document status.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-XX)**: Views featured provider listings (data consumed from A-02).
- **Provider Platform (PR-XX)**: Providers view their own profile status and uploaded documents (read-only access to data managed by A-02). **Fields must align with FR-032**.
- **Admin Platform (A-02)**: Full provider lifecycle management including creation, document upload (record-keeping), commission configuration, and status changes.
- **Shared Services (S-XX)**: S-03 (Notification Service) for account creation emails; S-05 (Media Storage) for profile images and document storage.

### Multi-Tenant Breakdown

**Patient Platform (P-XX)**:

- Display featured providers in provider discovery/search interfaces.
- Show provider bio, languages, awards, and clinic location.

**Provider Platform (PR-XX)**:

- Providers view their own profile (synced with A-02).
- Providers see uploaded documents (for reference).
- Providers view configured commission rates (read-only).
- **Note**: Providers can edit profile fields (Bio, Languages, Awards, Profile Picture, Contact details) via **FR-032: Provider Dashboard Settings & Profile Management**, which updates the A-02 record. All editable fields must align between FR-015 and FR-032 to ensure consistency.

**Admin Platform (A-02)**:

- Create new provider accounts with complete profile setup (Wizard Flow).
- Upload provider documents (Medical License, etc.) for internal records.
- Configure commission structures (Percentage or Flat Rate).
- Manage provider status (Active, Suspended, Deactivated).
- Toggle featured provider designation.

**Shared Services (S-XX)**:

- **S-03 (Notification Service)**: Sends welcome emails with login credentials.
- **S-05 (Media Storage Service)**: Stores uploaded provider documents and profile images.
- **S-06 (Audit Log Service)**: Logs creation and status changes.

### Communication Structure

**In Scope**:

- Email notifications to providers when account is created/activated.
- Notification to providers when their account is suspended/deactivated.

**Out of Scope**:

- Document verification workflow (documents are for record-keeping only)
- "Save as Draft" functionality

### Entry Points

- **Admin-Initiated**: Admin accesses "Provider Management" section in Admin Platform dashboard → selects "Add New Provider" to initiate provider creation workflow
- **Admin Oversight**: Admin opens "Providers" list view to see all providers across all statuses (draft, active, suspended, deactivated) with filtering and search
- **Provider Profile Access (Provider-Side)**: Provider logs into Provider Platform → views "My Profile" section to see account status, list of uploaded documents, and commission configuration (read-only)

---

## Business Workflows

### Main Flow: Admin Creates and Activates New Provider

**Actors**: Admin, System, Provider (receives notifications)
**Trigger**: Admin decides to onboard a new hair transplant provider to the platform
**Outcome**: Provider account created with "Active" status, provider notified and can log into Provider Platform

**Steps**:

1. Admin navigates to Admin Platform → "Provider Management" section
2. Admin clicks "Add New Provider" button
3. System displays Provider Creation Form with sections: Basic Information, Professional Details, Clinic Information, Document Upload, Commission Configuration
4. Admin enters provider basic information (Step 1):
   - Profile Picture/Logo (optional)
   - Cover Image (optional)
   - Full name (first, last)
   - Email address (will be used for provider login)
   - Phone number (with country code)
   - Bio/Description (min 50 chars)
   - Seat Limit (default: 100, range 1-500, optional - can be adjusted later)
5. Admin enters professional details (Step 2):
   - Specialty (e.g., "Hair Transplant Surgeon", "Dermatologist")
   - Medical license number
   - Years of experience
   - Languages Spoken (at least 1 required)
   - Awards & Recognition (optional)
6. Admin enters clinic/practice information (Step 3):
   - Clinic name
   - Clinic address (street, city, state/province, postal code, country)
   - Clinic phone number
   - Operating hours
7. Admin uploads required documents (Step 4):
   - Medical license (PDF/image file, required)
   - Board certifications (PDF/image, optional)
   - Malpractice insurance certificate (PDF/image, optional)
   - Documents are stored for internal record-keeping only and do NOT block activation
8. Admin configures commission structure (Step 5):
   - Selects commission model: "Percentage" or "Flat Rate"
   - Enters value (e.g., "15%" or "£150")
9. Admin reviews all entered information in summary view (Step 6).
10. Admin clicks "Create Provider" button.
11. System validates all required fields (First Name, Last Name, Email, Clinic Name, Bio min 50 chars, at least 1 Language).
12. System creates provider record with status = "Active" and initializes provider credentials.
13. System sends account activation email to provider with:
    - Welcome message and platform introduction
    - Secure one-time link to set password (expires in 24 hours)
    - Provider's email address (login username)
    - Instructions for first login and profile completion
14. Provider receives email and clicks "Set Password" link.
15. System displays password creation form (requires strong password: min 12 chars, uppercase, lowercase, number, special char).
16. Provider creates password and confirms.
17. System validates password strength, saves encrypted password, and redirects to Provider Platform login.
18. Provider logs in with email and new password.
19. System displays "Welcome to Hairline" onboarding screen prompting provider to complete profile (via FR-032):
    - Upload clinic logo and cover image
    - Review and enhance Bio/Description
    - Add languages if only 1 set by admin
    - Add awards and certifications
    - Review contact information
20. Provider completes profile setup via FR-032 (changes sync to admin view in FR-015).
21. Provider can now receive quote requests from patients.

### Alternative Flows

**A1: Provider Requests Activation Email Resend**:

- **Trigger**: Provider didn't receive activation email, email went to spam, or activation link expired (24 hours passed).
- **Steps**:
  1. Provider navigates to Provider Platform login page.
  2. Provider clicks "Didn't receive activation email?" link below login form.
  3. System displays email resend form with provider's email address field.
  4. Provider enters their email address (the one admin used during account creation).
  5. Provider clicks "Resend Activation Email" button.
  6. System validates email exists in provider database and account status = "Active" (account created but password not set).
  7. System generates new one-time password setup link (expires in 24 hours, invalidates previous link).
  8. System sends new activation email to provider with fresh link.
  9. System displays success message: "Activation email sent! Please check your inbox (and spam folder). The link expires in 24 hours."
  10. Provider receives email and proceeds with password setup (Main Flow steps 14-21).
- **Outcome**: Provider receives new activation email with valid link and can complete password setup.
- **Business Rules**:
  - Rate limited to 3 resend requests per hour per email address (prevents spam).
  - Previous activation links are invalidated when new link is generated.
  - If provider email not found or account already activated (password already set), system displays generic message: "If an account exists with this email, an activation link will be sent." (security: don't reveal if email exists).
  - Admin can also manually resend activation email from provider profile in FR-015 (button: "Resend Activation Email").

**A2: Admin Configures Flat Rate Commission**:

- **Trigger**: Admin selects "Flat Rate" commission model.
- **Steps**:
  1. Admin enters fixed amount (e.g., £200).
  2. System saves configuration.
  3. Commission is calculated as a fixed deduction per completed procedure, regardless of procedure price.
- **Outcome**: Flat rate commission configured.

**A3: Admin Marks Provider as Featured**:

- **Trigger**: Admin wants to highlight a high-quality provider.
- **Steps**:
  1. Admin toggles "Featured Provider" switch.
  2. System updates `provider.featured = true`.
  3. Provider appears in "Featured" lists in Patient App.
- **Outcome**: Provider visibility boosted.

**A4: Admin Updates Provider Documents**:

- **Trigger**: Admin receives updated license/insurance from provider.
- **Steps**:
  1. Admin navigates to provider profile → "Documents" tab.
  2. Admin uploads new file for "Medical License".
  3. System replaces old file (or archives it) and updates timestamp.
  4. No approval workflow required; document is immediately available for record.
- **Outcome**: Document record updated.

---

## Screen Specifications

### Screen 1: Provider Management Dashboard

**Purpose**: Provides admins with comprehensive overview of all providers across all statuses with filtering, search, and quick actions

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Search Bar | text | No | Free-text search by provider name, clinic name, email, license number | Max 200 chars |
| Status Filter | multi-select dropdown | No | Filter providers by status (Draft, Active, Suspended, Deactivated) | Multiple selections allowed |
| Featured Filter | checkbox | No | Filter to show only featured providers | Boolean toggle |
| Commission Type Filter | select | No | Filter by commission structure (Percentage, Tier-based, All) | Single selection |
| Date Range Filter | date range picker | No | Filter by provider creation date or last activity date | Valid date range required |
| Provider List Table | data table | N/A | Displays provider rows with columns: Name, Clinic, Status, Featured, Commission Rate, Documents Status, Created Date, Actions | Paginated (50 rows per page) |

**Business Rules**:

- **Default View**: Dashboard displays all providers with status = "Active" by default on initial load
- **Search**: Search queries match against provider name, clinic name, email, medical license number (case-insensitive)
- **Status Badge Colors**: Active (green), Suspended (yellow), Deactivated (red)
- **Featured Badge**: Gold star icon displayed next to provider name if featured = true
- **Documents Status Column**: Shows "Complete" (all required documents uploaded) or "Incomplete" (some required documents missing)
- **Quick Actions**: Each row includes action buttons: "View Profile", "Edit", "Suspend" (if active), "Activate" (if suspended), "Deactivate" (if active/suspended)
- **Sorting**: Table columns sortable by name (alphabetical), created date (chronological), commission rate (numerical)
- **Pagination**: Display 50 providers per page, with page navigation controls

**Notes**:

- Use color-coded status badges for quick visual scanning
- Featured providers should have prominent visual indicator (star icon)
- Ensure "Add New Provider" button prominently displayed in top-right corner
- Implement real-time status updates (e.g., if provider status changes, table refreshes without full page reload)

---

### Screen 2: Provider Creation Wizard

**Purpose**: Allows admins to create new provider accounts through a structured, multi-step wizard process. The wizard interface is used for creation; editing uses the tabbed interface (Screen 3).

**Cross-Module Alignment**: This screen's data structure aligns with **FR-032: Provider Dashboard Settings & Profile Management**. All profile fields (Bio, Languages, Awards, Profile Picture, Contact details) must stay synchronized between Admin (A-02) and Provider (PR-XX) platforms. When providers edit these fields via FR-032, changes are immediately reflected in the admin view.

**Wizard Steps**:

#### Step 1: Basic Information

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Profile Picture / Logo | file upload | No | Provider's photo or clinic logo (aligns with FR-032 Tab 1) | Max 5MB, JPEG/PNG, min 200x200px, recommended 500x500px |
| Cover Image | file upload | No | Large banner image for clinic profile (aligns with FR-032 Tab 1) | Max 10MB, JPEG/PNG, recommended 1920x300px |
| First Name | text | Yes | Provider's legal first name | Max 50 chars |
| Last Name | text | Yes | Provider's legal last name | Max 50 chars |
| Email Address | email | Yes | Primary email (login ID) | Valid email, unique |
| Phone Number | phone | Yes | Contact phone with country code | Valid format |
| Bio / Description | textarea | Yes | Public-facing provider biography (aligns with FR-032 Tab 1 "About/Description") | Max 500 chars, min 50 chars |
| Seat Limit | number | No | Maximum number of team members (staff) the provider can invite (aligns with FR-009 team management) | Integer, range 1-500, default: 100. Can be adjusted later by admin if provider requests increase |

#### Step 2: Professional Details

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Specialty | select | Yes | Primary medical specialty | List: "Hair Transplant", "Dermatology", etc. |
| Medical License Number | text | Yes | License identifier (for record) | Max 50 chars |
| Years of Experience | number | Yes | Years practicing | Numeric, 0-60 |
| Languages Spoken | multi-select chip/pill | Yes | Languages spoken at clinic (aligns with FR-032 Tab 2) | At least 1 language required; consumes centrally managed language list from FR-026 |
| Awards & Recognition | dynamic list | No | List of awards (aligns with FR-032 Tab 4) | Each award: name (max 100 chars), issuer/organization (max 150 chars, optional), description (max 300 chars), year (1900-current), award image (max 2MB, JPEG/PNG) |

#### Step 3: Clinic Information

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Clinic Name | text | Yes | Name of practice/clinic | Max 100 chars |
| Clinic Address | address | Yes | Full physical address | Google Places or manual entry |
| Location - City | text | No | City where clinic is located (aligns with FR-032 Tab 1) | Max 100 chars |
| Location - Country | dropdown | No | Country where clinic is located (aligns with FR-032 Tab 1) | Values from centrally managed country list (FR-026) |
| Clinic Phone | phone | No | Public clinic phone number (aligns with FR-032 "Contact Phone (Public)") | Contains Country Code (dropdown, FR-026) and Number (numeric only, length validated per country code) |
| Website URL | url | No | Public-facing clinic website (aligns with FR-032 Tab 1) | Valid URL format (http/https); auto-prepends https:// if protocol missing |
| Operating Hours | text | No | e.g., "Mon-Fri 9am-5pm" | Free text |

#### Step 4: Documents (Record Keeping)

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Medical License | file upload | Yes | Copy of license | PDF/Image, Max 10MB |
| Board Certification | file upload | No | Copy of certification | PDF/Image, Max 10MB |
| Insurance Certificate | file upload | No | Proof of malpractice insurance | PDF/Image, Max 10MB |

*Note: Documents are for internal record-keeping only and are pre-verified outside the system. Documents do NOT block account activation.*

#### Step 5: Commission & Settings

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Commission Model | radio | Yes | "Percentage" or "Flat Rate" | Default: Percentage |
| Commission Value | number | Yes | % or Fixed Currency Amount | 0-100 (if %) or >0 (if Flat) |
| Featured Provider | toggle | No | Highlight in patient search | Default: Off |

#### Step 6: Review & Create

- **Read-only Summary**: Displays all entered data for final review.
- **Actions**:
  - "Back": Navigate to previous steps.
  - "Create Provider": Finalizes creation and sets status to **Active**.

---

### Screen 3: Provider Profile Details (Tabbed View)

**Purpose**: Comprehensive view of a provider's account, organized by tabs for manageability. This view is used for editing existing provider records.

**Cross-Module Alignment**: Tab structure and field definitions align with **FR-032: Provider Dashboard Settings & Profile Management** to ensure consistency between admin and provider views. Screen 3 includes all 6 tabs from FR-032 (Basic Information, Languages, Staff List, Awards, Reviews, Documents) plus additional admin-only tabs (Commission & Financials, Activity Log).

**Header Area**:

- **Provider Name / Status Badge** (Active/Suspended/etc.)
- **Quick Actions**:
  - "Edit Profile" (opens all tabs in edit mode)
  - "Resend Activation Email" (visible only if password not yet set; sends new one-time password setup link)
  - "Suspend/Deactivate" (status management)
  - "Login as Provider" (Super Admin only, for support/debugging)

**Tabs**:

#### Tab 1: Basic Information (Profile Overview)

**Purpose**: Display and edit core clinic profile information. Mirrors FR-032 Tab 1 structure with additional admin-only settings.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Admin/Provider Editable |
|------------|------|----------|-------------|------------------|------------------------|
| Profile Picture / Logo | image upload | No | Clinic branding image | Max 5MB, JPEG/PNG, min 200x200px, recommended 500x500px | Both (Provider via FR-032) |
| Cover Image | image upload | No | Large banner image for clinic profile | Max 10MB, JPEG/PNG, recommended 1920x300px | Both (Provider via FR-032) |
| First Name | text | Yes | Provider's legal first name | Max 50 chars | Admin only |
| Last Name | text | Yes | Provider's legal last name | Max 50 chars | Admin only |
| Email Address | email | Yes | Primary email (login ID) | Valid email, unique | Admin only |
| Phone Number | phone | Yes | Primary contact phone | Valid format with country code | Admin only |
| Bio / Description | textarea | Yes | Public-facing provider biography | Max 500 chars, min 50 chars | Both (Provider via FR-032) |
| Specialty | select | Yes | Primary medical specialty | List: "Hair Transplant", "Dermatology", etc. | Admin only |
| Medical License Number | text | Yes | License identifier (for record) | Max 50 chars | Admin only |
| Years of Experience | number | Yes | Years practicing | Numeric, 0-60 | Admin only |
| Clinic Name | text | Yes | Name of practice/clinic | Max 100 chars | Both (Provider via FR-032) |
| Clinic Address | address | Yes | Full physical address | Google Places or manual entry | Admin only |
| Location - City | text | No | City where clinic is located | Max 100 chars | Both (Provider via FR-032) |
| Location - Country | dropdown | No | Country where clinic is located | Values from FR-026 country list | Both (Provider via FR-032) |
| Contact Phone (Public) | phone | No | Public clinic phone number | Country Code dropdown + Number | Both (Provider via FR-032) |
| Contact Email | email | Yes | Public clinic contact email | Valid email format | Both (Provider via FR-032) |
| Website URL | url | No | Public-facing clinic website | Valid URL, auto-prepends https:// | Both (Provider via FR-032) |
| Operating Hours | text | No | Operating hours (e.g., "Mon-Fri 9am-5pm") | Free text | Admin only |
| Seat Limit | number | No | Maximum team members (staff) capacity | Integer, range 1-500, default 100 | Admin only |
| Commission Model | radio | Yes | "Percentage" or "Flat Rate" | Default: Percentage | Admin only |
| Commission Value | number | Yes | % or Fixed Currency Amount | 0-100 (if %) or >0 (if Flat) | Admin only |
| Featured Provider | toggle | No | Highlight in patient search | Boolean, default: Off | Admin only |
| Status | badge/display | Yes | Provider account status | Enum: Active, Suspended, Deactivated | Admin only |
| Total Bookings | display | No | Count of completed procedures | Read-only, calculated | Read-only |
| Average Rating | display | No | Average rating from patient reviews | Read-only, format: X.X/5.0 stars | Read-only |

**Business Rules**:

- Fields marked "Both" can be edited by provider via FR-032 and changes sync to admin view in real-time
- Fields marked "Admin only" can only be edited by admin users with provider management permissions
- Profile changes logged in audit trail with timestamp, user, and changed fields
- Commission and Seat Limit changes require admin re-authentication for security. In MVP this is implemented as password re-entry; once the shared MFA stack from FR-026 / FR-031 is delivered, these actions MUST use MFA-based re-authentication and any MFA references in this FR are to be understood as future (non-MVP) behavior.

**Notes**:

- Admin view includes all provider profile fields plus admin-only settings (Seat Limit, Commission, Status)
- Provider-editable fields sync bidirectionally with FR-032
- Admin can override any provider changes if needed (logged in audit trail)

---

#### Tab 2: Languages

**Purpose**: View and manage languages spoken at the clinic. Mirrors FR-032 Tab 2 structure.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Admin/Provider Editable |
|------------|------|----------|-------------|------------------|------------------------|
| Supported Languages | chip/pill list | Yes | Languages spoken at clinic | At least 1 language required; consumes centrally managed language list from FR-026 | Both (Provider via FR-032) |

**Business Rules**:

- Languages displayed as removable chips/pills with X button on each chip
- Admin can add/remove languages; provider can also manage via FR-032 Tab 2
- At least 1 language must be selected (validation prevents removing last language)
- Changes logged in audit trail with timestamp and user
- Language list consumed from FR-026 (centrally managed)

**Notes**:

- Admin view identical to FR-032 Tab 2 (same interface, same functionality)
- Changes made by provider in FR-032 reflect immediately in admin view
- Drag-and-drop reordering supported to prioritize languages

---

#### Tab 3: Staff List

**Purpose**: View and manage provider's clinic staff members and team roles (admin view).

**Implementation**: This tab displays **FR-009: Provider Team & Roles Management > Screen 10** (Admin view of provider team).

See FR-009 Screen 10 for complete field specifications, business rules, and team management functionality from the admin perspective.

---

#### Tab 4: Awards

**Purpose**: View and manage clinic awards, certifications, and recognitions. Mirrors FR-032 Tab 4 structure.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Admin/Provider Editable |
|------------|------|----------|-------------|------------------|------------------------|
| Awards List | card/list | No | Clinic awards, certifications, recognitions | Each award: name (max 100 chars), issuer/organization (max 150 chars, optional), description (max 300 chars), year (1900-current year), award image (max 2MB, JPEG/PNG) | Both (Provider via FR-032) |

**Business Rules**:

- Awards displayed as cards with: award image thumbnail, name, issuer, year, description
- Admin can add/edit/delete awards; provider can also manage via FR-032 Tab 4
- Awards support drag-and-drop reordering to prioritize most important awards
- Award image upload supports drag-and-drop; max 2MB, JPEG/PNG only
- Changes logged in audit trail with timestamp and user

**Notes**:

- Admin view identical to FR-032 Tab 4 (same interface, same functionality)
- Changes made by provider in FR-032 reflect immediately in admin view
- Empty state: "No awards added yet. Click '+ Add Award' to showcase achievements."

---

#### Tab 5: Reviews

**Purpose**: Browse all patient reviews with filtering and sorting capabilities (read-only). Mirrors FR-032 Tab 5 structure.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Admin/Provider Editable |
|------------|------|----------|-------------|------------------|------------------------|
| Overall Rating Summary | display | No | Average rating and total review count | Read-only; calculated from Reviews service | Read-only |
| Rating Distribution | bar chart | No | Percentage/count visualization for 5★ through 1★ reviews | Read-only; calculated from Reviews service | Read-only |
| Review List | list | No | List of individual patient reviews with rating, comment, date, patient name | Read-only; sourced from Reviews service | Read-only |
| Rating Filters | checkbox/pill | No | Filter reviews by rating (5★, 4★, 3★, 2★, 1★) | Multiple selections allowed | Interactive filter |

**Business Rules**:

- Reviews displayed with: star rating, patient name (anonymized if requested), date, review text
- Admin can filter by rating, search by keyword, sort by date/rating
- Admin cannot edit or delete reviews (data integrity); only flag for review if inappropriate
- Reviews are read-only for both admin and provider
- Review data sourced from Reviews service (handled by separate FR module)

**Notes**:

- Admin view identical to FR-032 Tab 5 (same interface, same functionality)
- Reviews help admin assess provider quality and patient satisfaction
- Admin can flag inappropriate reviews for further investigation

---

#### Tab 6: Documents

**Purpose**: View and manage provider documents (license, certification, insurance) for oversight and record-keeping. Providers manage their own documents via FR-032; admins can view all documents and upload additional documents received via external channels (email, postal mail, in-person).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Admin/Provider Editable |
|------------|------|----------|-------------|------------------|------------------------|
| Upload Document Button | button | No | Admin action to upload additional documents | Opens upload modal | Admin only |
| Document List | list/cards | No | List of all provider and admin-uploaded documents | Displays: document name, type, upload date, file size, uploaded by (Provider/Admin) | View-only for admin; sortable/filterable |
| Document Name | text (display) | N/A | Filename of uploaded document | Auto-generated from file; max 200 chars | Display only |
| Document Type | badge (display) | N/A | Type of document | Enum: Medical License, Board Certification, Insurance, Malpractice Insurance, Business License, Other | Display only |
| Upload Date | datetime (display) | N/A | When document was uploaded | Auto-generated timestamp; format: "MMM DD, YYYY HH:mm" | Display only |
| Uploaded By | badge (display) | N/A | Who uploaded document: "Provider" or "Admin [Name]" | Badge displays "Provider" for provider uploads, "Admin - [admin name]" for admin uploads | Display only |
| File Size | text (display) | N/A | Document file size | Format: "X.X MB" or "X KB" | Display only |
| Notes | text (display/edit) | No | Optional notes about document | Max 500 chars; admin can add/edit notes | Admin editable (via "Edit Notes" action) |
| Actions | button group | No | View, Download, Replace, Delete actions | Context menu or action buttons per document | Admin only (view/download/replace/delete) |

**Business Rules**:

- **Provider Document Management**: Providers upload, replace, delete their documents via **FR-032 Tab 6: Documents**. Provider-uploaded documents sync to FR-015 within 1 minute
- **Admin Oversight**: Admins can view all provider-uploaded documents for compliance and oversight purposes
- **Admin Additional Uploads**: Admins can upload additional documents received externally (e.g., documents sent via email, postal mail, scanned at in-person meeting). These admin-uploaded documents display "Admin - [admin name]" badge
- **Document Permissions**:
  - Provider-uploaded documents: Admin can view, download, add notes, but **cannot replace or delete** (only provider can via FR-032)
  - Admin-uploaded documents: Admin has full control (view, download, replace, delete, add notes)
- **Document Requirements**: At least one Medical License document recommended but not enforced (documents do NOT block provider activation)
- **Audit Logging**: All document actions (upload/view/download/replace/delete/note edits) logged in Tab 8: Activity Log with timestamp, user (admin/provider), action type, and IP address
- **Soft Delete**: Deleted documents (by provider or admin) retained in archive for compliance; visible in Activity Log but not in main document list
- **File Validation**: Same as FR-032 - Accepted formats: PDF, JPG, PNG, DOCX, XLSX; Max 10MB per file
- **Sort/Filter Options**:
  - Sort by: Upload Date (newest first - default), Document Type, Uploaded By
  - Filter by: Document Type, Uploaded By (Provider/Admin)

**Notes**:

- **Primary Document Management**: Providers manage their documents via FR-032 Tab 6; admins use FR-015 Tab 6 for oversight and supplementary uploads
- **Use Case for Admin Uploads**: Admin receives provider's license via email → Admin uploads to FR-015 Tab 6 → Document visible to provider in FR-032 with "Admin" badge
- **Document Sync**: Provider uploads in FR-032 → Syncs to FR-015 within 1 minute. Admin uploads in FR-015 → Syncs to FR-032 within 1 minute
- **Empty State**: If no documents uploaded yet, display message: "No documents on file yet. Provider can upload documents via their dashboard, or you can upload documents received externally."
- **Document Verification**: Performed externally; system treats all documents as pre-verified records
- Document cards/rows display icon based on file type (PDF icon, image icon, doc icon) and "Uploaded By" badge (green for Provider, blue for Admin)

---

#### Tab 7: Commission & Financials (Admin-Only)

**Purpose**: View and manage commission configuration and financial history. This tab is admin-only and not visible in FR-032.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Admin/Provider Editable |
|------------|------|----------|-------------|------------------|------------------------|
| Commission Model | radio (display/edit) | Yes | "Percentage" or "Flat Rate" | Default: Percentage | Admin only (edit) |
| Commission Value | number (display/edit) | Yes | % or Fixed Currency Amount | 0-100 (if %) or >0 (if Flat) | Admin only (edit) |
| Current Configuration | display | N/A | Summary of active commission settings | Display format: "15% per transaction" or "£200 flat rate" | Display only |
| Commission History | list | No | Audit log of past commission changes | Each entry: date, admin user, old value, new value, reason | Display only |

**Business Rules**:

- Commission configuration displayed prominently with current model and value
- Admin can edit commission settings (requires re-authentication). In MVP this is implemented as password re-entry; once the shared MFA stack from FR-026 / FR-031 is delivered, these actions MUST use MFA-based re-authentication and any MFA references in this FR are to be understood as future (non-MVP) behavior.
- Commission changes take effect immediately for new transactions
- All commission changes logged in history with timestamp, admin user, old/new values
- Provider can view commission rate read-only via FR-032 (but not edit)

**Notes**:

- This tab is admin-only; provider sees commission rate read-only in their dashboard (FR-032)
- Commission changes require admin justification (logged in audit trail)

---

#### Tab 8: Activity Log (Admin-Only)

**Purpose**: View chronological audit trail of all provider account actions. This tab is admin-only and not visible in FR-032.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Admin/Provider Editable |
|------------|------|----------|-------------|------------------|------------------------|
| Activity Log List | list | No | Chronological list of account actions | Each entry: timestamp, user (admin or provider), action type, changed fields, IP address | Read-only |

**Business Rules**:

- Activity log displays all actions: profile edits, status changes, document uploads, logins, commission changes
- Each log entry includes: timestamp, user (admin or provider via FR-032), action type, changed fields, IP address
- Logs are immutable (cannot be edited or deleted)
- Admin can filter by action type, date range, user
- Admin can export activity log for compliance reporting

**Notes**:

- This tab is admin-only and provides full transparency of provider account changes
- Logs help with compliance, security investigations, and dispute resolution

---

### Screen 4: Provider Suspension/Deactivation Modal

**Purpose**: Captures admin reason for suspending or deactivating a provider, ensuring accountability and clear communication to provider

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Action Type | text (display only) | N/A | Shows "Suspend Provider" or "Deactivate Provider" as modal title | Display only |
| Provider Name | text (display only) | N/A | Confirms which provider is being suspended/deactivated | Display only |
| Reason | textarea | Yes | Admin must provide detailed reason for suspension/deactivation | Min 20 chars, max 500 chars |
| Notify Provider | checkbox | No | Option to send notification email to provider with reason | Default checked (true) |
| Effective Date | date picker | No | Optional: schedule suspension/deactivation for future date | Must be today or future date |
| Confirm Action | checkbox | Yes | Admin must check "I confirm this action" before submitting | Must be checked to enable submit button |

**Business Rules**:

- **Required Reason**: Admin cannot suspend or deactivate provider without providing detailed reason (minimum 20 characters)
- **Suspension vs. Deactivation**:
  - **Suspension**: Temporary status change; provider account remains in system and can be reactivated later
    - Provider cannot receive new bookings while suspended
    - Existing upcoming bookings remain active (admin must manually cancel if needed)
    - Provider can still log in to Provider Platform but sees "Account Suspended" banner
  - **Deactivation**: Permanent status change; provider account cannot be reactivated (final removal from platform)
    - All future bookings automatically cancelled (system sends notifications to affected patients)
    - Provider login disabled immediately
    - Provider data retained for audit/legal purposes but marked as deactivated
- **Notification Email**: If "Notify Provider" checkbox enabled (default), system sends email to provider with:
  - Action taken (Suspended or Deactivated)
  - Reason provided by admin
  - Effective date (if scheduled)
  - Contact information for admin support if provider has questions
- **Scheduled Suspension**: If admin selects future effective date, suspension occurs automatically on that date (cron job processes scheduled suspensions daily at midnight UTC)
- **Confirmation Requirement**: Admin must explicitly check "I confirm this action" checkbox before "Submit" button enabled (prevents accidental suspension/deactivation)

**Notes**:

- Use prominent warning styling (red border, caution icon) to emphasize severity of action
- Display clear differentiation between suspension (temporary, reversible) and deactivation (permanent, irreversible)
- Provide example reasons to guide admin (e.g., "Document verification failed", "Violation of platform terms", "Provider requested account closure")
- Include "Cancel" button to abort action and return to provider profile view

---

## Business Rules

### General Module Rules

- **Rule 1**: All provider accounts must be created by admins—no self-service provider registration allowed.
- **Rule 2**: Provider activation requires mandatory profile fields to be complete: First Name, Last Name, Email, Clinic Name, Bio/Description (min 50 chars), and at least 1 Language. Document uploads are for record-keeping and do NOT block activation.
- **Rule 3**: Provider status transitions follow lifecycle: Active → Suspended → (Reactivated OR Deactivated). Providers are created as Active when all required fields are complete.
- **Rule 4**: Deactivation is permanent—deactivated providers cannot be reactivated; admin must create new provider account if re-onboarding required.
- **Rule 5**: Commission rates apply to all transactions processed after rate configuration.
- **Rule 6**: Featured provider designation only available for providers with status = "Active".
- **Rule 7**: Seat limit (maximum team members) defaults to 100 and can be adjusted by admin (range 1-500). Providers can request seat limit increases through support, which must be approved by admin. Seat limit blocks staff invitations when reached (enforced by FR-009).

### Data & Privacy Rules

- **Privacy Rule 1**: Provider contact information (email, phone) visible only to admins; patients see clinic phone/email.
- **Privacy Rule 2**: Uploaded provider documents (licenses, certifications, insurance) encrypted at rest using AES-256.
- **Audit Rule**: All provider management actions logged with timestamp, admin user ID, and action details.

### Admin Editability Rules

**Editable by Admin**:

- Provider basic information (name, specialty, bio, languages, awards)
- Clinic information (name, address, phone, logo, contact email)
- Commission configuration (Model: Percentage/Flat, Value)
- Seat limit (maximum team members, range 1-500, default 100)
- Document uploads (Add/Replace/Remove)
- Provider status (Active, Suspended, Deactivated)
- Featured provider designation

**Editable by Provider (via FR-032)**:

- Profile Picture/Logo
- Cover Image
- Bio/Description
- Languages Spoken
- Awards & Recognition (add/edit/delete with images)
- Contact Phone (Public)
- Contact Email
- Location (City, Country)
- Website URL

**Fixed in Codebase**:

- Deactivation finality rule
- Encryption standards
- Commission calculation logic

### Payment & Billing Rules

- **Commission Rule 1**: Commissions apply to all provider earnings from patient bookings.
- **Commission Rule 2**: **Percentage Model**: Calculated as `Transaction Amount * (Commission Rate / 100)`.
- **Commission Rule 3**: **Flat Rate Model**: Fixed amount deducted per completed procedure (e.g., £150 flat fee).
- **Commission Rule 4**: Commission changes take effect immediately for new transactions.
- **Billing Rule 1**: Provider payouts calculated weekly (or per agreement) and transferred to provider's bank account.

---

## Success Criteria

### Patient Experience Metrics

- **SC-001**: Patients can discover and view featured provider profiles in Patient Platform within 1 second of search query (data sourced from A-02 featured providers)
- **SC-002**: 100% of patient-facing provider information (name, clinic, specialty) displays accurately and matches admin-configured data in A-02 with no discrepancies
- **SC-003**: Patients see only verified, active providers in search results (no draft/suspended/deactivated providers visible), ensuring trust and booking reliability

### Provider Efficiency Metrics

- **SC-004**: Providers receive account activation notification within 1 minute of admin activating their account, enabling immediate platform access
- **SC-005**: Providers can view their uploaded documents list and commission configuration in Provider Platform within 2 seconds of navigation
- **SC-006**: 90% of providers successfully log in and access their profile on first attempt after receiving activation credentials (low login failure rate)

### Admin Management Metrics

- **SC-007**: Admins can create a complete provider profile (all sections filled, documents uploaded, commission configured) in under 10 minutes on average
- **SC-008**: Admins can filter and search provider list (1000+ providers) and retrieve results in under 2 seconds, enabling efficient provider oversight
- **SC-009**: Providers and admins can upload and manage documents in under 30 seconds per document, streamlining record-keeping workflows. Document changes sync between FR-032 and FR-015 within 1 minute
- **SC-010**: 100% of provider status changes (activate, suspend, deactivate) logged in audit trail with timestamp, admin user, and reason (full accountability)
- **SC-011**: System maintains complete audit trail of all document uploads, replacements, and deletions with 100% accuracy
- **SC-012**: Admin dashboard displays real-time provider status counts (draft, active, suspended, deactivated) with <1 second refresh latency

### System Performance Metrics

- **SC-013**: Provider creation/edit form submission completes within 3 seconds for 95% of requests (excluding large document uploads)
- **SC-014**: Document upload (up to 10MB per file) completes within 10 seconds for 90% of uploads on standard broadband connections
- **SC-015**: Provider profile page loads (all tabs: profile, documents, status history, activity log) within 2 seconds for 95% of requests
- **SC-016**: System supports 100 concurrent admin users managing providers without performance degradation
- **SC-017**: 99.9% uptime for provider management functionality (excluding scheduled maintenance)

### Business Impact Metrics

- **SC-018**: Provider onboarding time reduced by 60% compared to manual/offline provider onboarding processes (baseline: 5 hours manual → target: 2 hours in-system)
- **SC-019**: Provider document management errors reduced by 80% through structured upload validation and clear file type requirements
- **SC-020**: 95% of providers have complete profiles (all required fields filled, commission configured) within 48 hours of initial account creation
- **SC-021**: Featured provider designation increases patient booking conversion rate by 25% compared to non-featured providers (measured in Patient Platform analytics)

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **FR-001 / Module A-01: Admin Authentication & Authorization**
  - **Why needed**: Admins must be authenticated and have "Provider Management" role permissions to access provider creation, editing, and status management features
  - **Integration point**: A-02 verifies admin user session token and role permissions before allowing provider management actions; API endpoints protected by role-based access control (RBAC)

- **FR-XXX / Module PR-01: Auth & Team Management**
  - **Why needed**: Providers created in A-02 must be able to log into Provider Platform to view their profile status, uploaded documents, and commission configuration (all sourced from A-02/FR-032).
  - **Integration point**: A-02 creates provider user account credentials (email/password) and passes to PR-01 authentication service; providers authenticate via PR-01 to access read-only profile data sourced from A-02

- **FR-XXX / Module P-02: Provider Discovery & Search (Patient-Facing)**
  - **Why needed**: Featured providers designated in A-02 must be displayed prominently in Patient Platform search and discovery interfaces
  - **Integration point**: P-02 queries A-02 provider data filtered by (status = "Active" AND featured = true) to populate featured provider listings; includes provider name, clinic, specialty, profile photo

- **FR-XXX / Module S-03: Notification Service**
  - **Why needed**: Providers must receive email notifications when admins activate accounts or suspend/deactivate accounts; SMS may be added later for critical events
  - **Integration point**: A-02 triggers notification events to S-03 API with templates (e.g., "account_activated", "account_suspended") and provider contact details; S-03 sends templated emails asynchronously. SMS, if enabled in future, would also be orchestrated by S-03.

- **FR-XXX / Module S-05: Media Storage Service**
  - **Why needed**: Provider documents (licenses, certifications, insurance) must be securely stored with encryption and access controls
  - **Integration point**: A-02 uploads documents to S-05 API with metadata (provider ID, document type, expiration date); S-05 returns secure download URLs accessible only to authorized admins

- **FR-XXX / Module S-06: Audit Log Service**
  - **Why needed**: All provider management actions (creation, edits, status changes, and document-related actions) must be logged for compliance and audit trails
  - **Integration point**: A-02 sends audit log events to S-06 API with structured data (timestamp, admin user ID, action type, entity ID, before/after values); S-06 persists logs and provides query interface for admin reporting

### External Dependencies (APIs, Services)

- **External Service 1: Email Delivery Service (e.g., SendGrid, AWS SES)**
  - **Purpose**: Sends provider notification emails (account activation and status changes)
  - **Integration**: S-03 Notification Service integrates with email delivery API via REST/SMTP; A-02 does not directly call external email service
  - **Failure handling**: If email delivery fails, S-03 retries up to 3 times with exponential backoff; A-02 displays warning to admin: "Notification queued but not yet delivered"

- **External Service 2: SMS Delivery Service (e.g., Twilio, AWS SNS)**
  - **Purpose**: (Future) Sends SMS notifications to providers for critical status changes (account suspended, document rejected) once S-03 SMS support is implemented
  - **Integration**: S-03 integrates with SMS API; A-02 would trigger SMS notifications via S-03 for high-priority events in a later phase
  - **Failure handling**: SMS failures logged in S-03; A-02 fallback sends email notification if SMS delivery fails. **No SMS delivery is available in MVP.**

- **External Service 3: Cloud File Storage (e.g., AWS S3, Google Cloud Storage)**
  - **Purpose**: Stores uploaded provider documents (licenses, certifications, insurance) with encryption at rest
  - **Integration**: S-05 Media Storage Service uploads documents to cloud storage via SDK/API with server-side encryption (AES-256)
  - **Failure handling**: If upload fails, A-02 displays error to admin: "Document upload failed. Please retry." Document upload retries automatically up to 3 times before failing

### Data Dependencies

- **Entity 1: Admin User Roles and Permissions**
  - **Why needed**: A-02 must verify admin has "Provider Management" permission before allowing provider creation, editing, or status changes
  - **Source**: Admin authentication module (A-01) provides role-based access control (RBAC); admin roles (e.g., "Super Admin", "Provider Manager", "Read-Only Admin") defined with granular permissions

- **Entity 2: Notification Templates (Email/SMS)**
  - **Why needed**: Standardized notification messages for provider account lifecycle events (activation and suspension) must exist; in MVP only email templates are used, with SMS templates reserved for future phases
  - **Source**: Notification templates pre-configured in S-03 Notification Service; A-02 references email template IDs (e.g., "provider_activation_email") when triggering notifications. SMS templates, if configured later, would be used only once SMS delivery is enabled.

- **Entity 3: Document Type Configuration**
  - **Why needed**: System must know which document types are required to be stored for each provider (medical license, board certification, malpractice insurance)
  - **Source**: Document type definitions configured in admin settings or hardcoded in A-02 codebase; includes required fields (e.g., expiration date for offline checks) and validation rules (file size, format). No in-system document status workflow is tracked in this FR.

---

## Assumptions

### User Behavior Assumptions

- **Assumption 1**: Admins have direct access to provider documentation (licenses, certifications) either physically or digitally before initiating provider creation (e.g., provider sends documents via email or postal mail to admin)
- **Assumption 2**: Admins will verify provider document authenticity manually (e.g., cross-reference medical license number with state medical board database) before or during provider onboarding
- **Assumption 3**: Providers check their email regularly (at least daily) to receive account activation notifications
- **Assumption 4**: Admins will proactively communicate with providers regarding document updates and renewals as needed through direct contact

### Technology Assumptions

- **Assumption 1**: Admins access Admin Platform via desktop/laptop computers (not mobile devices) due to complexity of provider creation forms and document review workflows
- **Assumption 2**: Admins have reliable broadband internet connectivity for uploading provider documents (up to 10MB per file)
- **Assumption 3**: Providers access Provider Platform to view profile status via both desktop and mobile devices (responsive design required for provider profile view)
- **Assumption 4**: Media Storage Service (S-05) provides 99.99% availability for document uploads and retrieval

### Business Process Assumptions

- **Assumption 1**: Provider onboarding is admin-initiated only—providers cannot register themselves; admins control provider network quality through manual vetting
- **Assumption 2**: Commission rate configuration occurs at provider creation time, but admins can adjust rates later as provider performance changes (e.g., reward high-performing providers with lower commission rates)
- **Assumption 3**: Providers will proactively provide updated documents when renewals occur without system-prompted reminders
- **Assumption 4**: Suspended providers' existing bookings remain active (admin must manually cancel if needed); suspension only prevents new bookings
- **Assumption 5**: Deactivated providers' data retained indefinitely for legal/audit purposes; GDPR/data deletion requests handled via separate data privacy workflows (not in-scope for A-02)

---

## Implementation Notes

### Technical Considerations

- **Architecture**: Provider Management module follows admin-initiated CRUD (Create, Read, Update, Delete) pattern with state machine for status lifecycle (Draft → Active → Suspended → Deactivated)
- **Technology**: Document upload functionality should support chunked/resumable uploads for large files (up to 10MB) to handle unreliable admin connections
- **Performance**: Provider list dashboard with 1000+ providers requires pagination, indexing on status/created_date columns, and client-side filtering/sorting for responsive UI
- **Storage**: Provider documents stored in cloud object storage (S3-compatible) with server-side encryption (AES-256); document metadata (filename, upload date, document type, uploaded by) stored in relational database
- **Validation**: Commission rate validation enforced at both client-side (immediate feedback) and server-side (security) to prevent invalid configurations. Percentage model: 0-100%; Flat Rate model: > 0
- **State Machine**: Provider status transitions implemented as finite state machine with validation rules (e.g., cannot transition from Deactivated to any other status; must include reason for Suspend/Deactivate transitions)

### Integration Points

- **Integration 1: Admin Platform (A-02) → Notification Service (S-03)**
  - **Data format**: JSON payload with event type (e.g., "provider.activated"), provider ID, recipient (provider email/phone), template ID, and dynamic variables (e.g., provider name, login URL)
  - **Authentication**: Service-to-service authentication via API key in request header
  - **Error handling**: S-03 returns 202 Accepted (notification queued) or 4xx/5xx error; A-02 logs notification failures and displays warning to admin

- **Integration 2: Admin Platform (A-02) → Media Storage Service (S-05)**
  - **Data format**: Multipart form-data for document uploads with metadata (provider ID, document type, expiration date)
  - **Authentication**: OAuth 2.0 service account token for S-05 API access
  - **Error handling**: S-05 returns 200 OK with document URL or 4xx/5xx error; A-02 retries upload up to 3 times with exponential backoff before failing

- **Integration 3: Provider Platform (PR-01) → Provider Data (A-02 Database)**
  - **Data format**: REST API calls from PR-01 to fetch provider profile data (read-only) for display in provider's profile view
  - **Authentication**: OAuth 2.0 provider user token validated by A-02 API; provider can only access their own profile data (not other providers)
  - **Error handling**: A-02 API returns 200 OK with provider data or 403 Forbidden if provider attempts to access unauthorized data

- **Integration 4: Patient Platform (P-02) → Featured Provider Data (A-02 Database)**
  - **Data format**: GraphQL query or REST API call from P-02 to fetch featured providers (status = Active AND featured = true) with fields: name, clinic, specialty, profile photo URL
  - **Authentication**: Public API endpoint (no authentication required for featured provider listings)
  - **Error handling**: A-02 returns empty array if no featured providers available; P-02 displays "No featured providers at this time" message

### Scalability Considerations

- **Current scale**: Expected 100-200 providers onboarded in first 6 months (10-30 provider creations per month)
- **Growth projection**: Plan for 1,000+ providers within 2 years as platform expands to new geographic markets
- **Peak load**: Admin dashboard must support 50 concurrent admin users during provider onboarding campaigns without performance degradation
- **Data volume**: Expect 300MB of provider documents uploaded per month (3 documents × 10MB avg per provider × 10 providers/month); plan for 10GB storage per year
- **Scaling strategy**:
  - Database indexing on provider.status, provider.created_at, provider.featured for fast dashboard queries
  - Document storage in cloud object storage (S3) with CDN for admin document preview (reduces server load)
  - Pagination and lazy loading in provider dashboard (load 50 providers per page) to minimize initial page load time
  - Async document upload processing (upload to S-05 asynchronously, update database when complete) to prevent blocking admin UI

### Security Considerations

- **Authentication**: Only authenticated admins with "Provider Management" role permission can access A-02 provider management features; enforced via role-based access control (RBAC) middleware
- **Authorization**: Admins with "Read-Only" role can view provider profiles but cannot create, edit, or change status; "Provider Manager" role has full CRUD access; "Super Admin" role has all permissions
- **Encryption**:
  - Provider documents encrypted at rest in cloud storage (AES-256 server-side encryption)
  - Provider sensitive data (email, phone, medical license number) encrypted in database using application-level encryption
  - All API communication via HTTPS/TLS 1.3 (no unencrypted HTTP allowed)
- **Audit trail**: 100% of provider management actions logged with timestamp, admin user ID, IP address, and action details; audit logs immutable (cannot be edited or deleted by admins)
- **Threat mitigation**:
  - Rate limiting on provider creation API (max 10 provider creations per admin per hour) to prevent bulk account creation abuse
  - File upload validation (max 10MB per file, only PDF/JPEG/PNG allowed, malware scanning via antivirus integration before storage)
  - Input sanitization on all form fields (prevent SQL injection, XSS attacks)
- **Compliance**:
  - HIPAA-compliant data handling for provider medical licenses and certifications (PHI data)
  - GDPR compliance for provider personal data (name, email, phone) with data retention policies (deactivated providers' data retained 7 years, then eligible for deletion)
  - SOC 2 Type II audit trail requirements met via S-06 Audit Log Service integration

---

## User Scenarios & Testing

### User Story 1 - Admin Onboards New Provider from Scratch (Priority: P1)

Admin receives provider application materials (resume, licenses, certifications, insurance) and creates complete provider profile in Admin Platform, uploads documents, configures commission, and activates account. Provider receives email notification and can immediately log into Provider Platform.

**Why this priority**: Core functionality enabling platform provider network growth; without this, no providers can be onboarded and platform cannot function.

**Independent Test**: Admin completes full provider onboarding workflow from provider creation form to activation; verify provider receives activation email, can log into Provider Platform, and views correct profile data (name, clinic, commission rate).

**Acceptance Scenarios**:

1. **Given** admin is logged into Admin Platform with "Provider Management" role, **When** admin navigates to Provider Management → "Add New Provider" → fills all required fields (name, email, license, clinic, documents, commission) → clicks "Save and Activate", **Then** system creates provider with status = "Active", sends activation email to provider, and displays success message: "Provider [Name] activated successfully"
2. **Given** provider receives activation email with login credentials, **When** provider clicks login link and enters credentials, **Then** provider successfully logs into Provider Platform and sees profile page with status = "Active", list of uploaded documents, and commission rate displayed
3. **Given** admin activates provider with featured = true, **When** patient opens Patient Platform provider search, **Then** newly activated provider appears in "Featured Providers" section with gold star badge

---

### User Story 2 - Admin Uploads Provider Documents for Record Keeping (Priority: P1)

Admin uploads provider documents (medical license, board certification, insurance) to the provider profile for compliance records. Documents are for record-keeping only; no verification workflow is involved.

**Why this priority**: Critical for maintaining compliance records and regulatory documentation.

**Independent Test**: Admin navigates to provider profile → Documents tab, uploads a PDF; verify document appears in the list with timestamp, document type, and download link.

**Acceptance Scenarios**:

1. **Given** admin is on the "Documents" tab of a provider profile, **When** admin uploads a "Medical License" file, **Then** system stores the file securely and displays it in the document list immediately with type "Medical License", upload date, and uploaded by admin name.
2. **Given** a document is uploaded, **When** admin clicks "Download", **Then** the file opens/downloads correctly.
3. **Given** an incorrect file was uploaded, **When** admin clicks "Delete/Remove", **Then** system displays confirmation dialog, and upon confirmation, removes the file from the list (soft delete with audit log entry).

---

### User Story 3 - Admin Suspends Provider Due to Policy Violation (Priority: P2)

Admin identifies provider violating platform terms (e.g., fraudulent reviews, inappropriate conduct, non-response to patient inquiries) and suspends provider account temporarily to investigate.

**Why this priority**: Important for platform integrity and patient safety, but less urgent than core provider onboarding workflows.

**Independent Test**: Admin selects active provider, clicks "Suspend", enters reason "Multiple patient complaints about unprofessional conduct - under investigation"; verify provider status changes to "Suspended", provider cannot receive new quotes, and provider receives suspension notification email.

**Acceptance Scenarios**:

1. **Given** admin views provider with multiple policy violations (e.g., 5 patient complaints), **When** admin clicks "Suspend Provider", enters reason "Under investigation for patient complaints", enables "Notify Provider" checkbox, clicks "Submit", **Then** system changes provider status to "Suspended", blocks new quote requests, sends notification email to provider with suspension reason, and logs action in audit trail.
2. **Given** provider has 3 upcoming confirmed appointments when suspended, **When** admin suspends provider, **Then** system displays warning "Provider has 3 upcoming appointments. Suspending will block new quotes but existing appointments remain active. Cancel appointments manually if needed." Admin confirms suspension, and existing appointments remain active (admin must manually cancel if required).
3. **Given** suspended provider attempts to log into Provider Platform, **When** provider enters credentials and submits login, **Then** system allows login but displays prominent "Account Suspended" banner with message "Your account is temporarily suspended. Reason: [admin-provided reason]. Contact <support@hairlineapp.com> for assistance." Provider can view profile and documents but cannot accept new inquiries.
4. **Given** admin investigates and resolves policy violation, **When** admin clicks "Reactivate Provider" on suspended account, enters reason "Investigation complete - no violations found", **Then** system changes status to "Active", provider can receive new quotes again, sends reactivation email to provider, and logs action in audit trail.

---

### User Story 4 - Admin Configures Flat Rate Commission (Priority: P2)

Admin configures a provider account with a fixed commission fee (e.g., £200 per procedure) instead of a percentage.

**Why this priority**: Supports flexible business models with different clinics.

**Independent Test**: Admin creates/edits provider, selects "Flat Rate" commission, enters value "200"; verify calculations for bookings use the flat rate deduction.

**Acceptance Scenarios**:

1. **Given** admin is editing provider commission settings, **When** admin selects "Flat Rate" and enters "200", **Then** system saves the configuration.
2. **Given** a provider has a £200 flat rate, **When** a £3000 booking is completed, **Then** system calculates Platform Commission as £200 (not a percentage).

---

**Note**: Provider-side user stories (viewing/editing profile, managing settings) are documented in **FR-032: Provider Dashboard Settings & Profile Management**. FR-015 focuses exclusively on admin-initiated provider management actions.

### Edge Cases

- What happens when **admin attempts to create provider with email already used by another provider**? System displays validation error: "Email address already in use by another provider. Please use a different email." Provider creation blocked until unique email provided.
- How does system handle **provider document upload fails mid-upload (network interruption)**? System supports resumable uploads; if upload interrupted, admin can retry upload (system may resume from last successful chunk if implemented, otherwise restarts upload).
- What occurs if **admin activates provider but notification email delivery fails (email service down)**? System queues notification for retry (up to 3 attempts over 1 hour); admin sees warning message: "Provider activated but notification email not yet delivered. Email delivery in progress." Admin can manually resend notification via "Send Notification" button.
- How to manage **two admins simultaneously editing same provider profile (concurrent edits)**? System implements optimistic locking; second admin to save receives error: "Provider profile was modified by another admin. Please refresh and re-enter your changes." Last-write-wins conflict resolution prevents data loss.
- What happens when **admin deactivates provider with 10 upcoming patient bookings**? System displays confirmation modal: "This provider has 10 upcoming bookings. Deactivation will automatically cancel all future bookings and notify affected patients. Continue?" If admin confirms, system cancels bookings, sends cancellation notifications to patients, and offers rebooking options.
- What happens if **admin attempts to create provider without filling required fields**? System validates required fields on each wizard step: First Name, Last Name, Email, Clinic Name, Bio (min 50 chars), and at least 1 Language. System displays error: "Please complete all required fields before proceeding" and highlights missing fields in red.
- What occurs if **admin attempts to set invalid commission rate (e.g., negative percentage or zero flat rate)**? System displays client-side validation error immediately: "Percentage must be between 0-100%" or "Flat rate must be greater than 0." Server-side validation also enforces rules; API returns 400 Bad Request if invalid rate submitted.
- How to manage **provider requests account closure (wants to be deactivated)**? Provider contacts admin (no self-service deactivation); admin navigates to provider profile → clicks "Deactivate Provider" → enters reason: "Provider requested account closure on [date]" → confirms deactivation. System deactivates account, cancels future bookings, sends confirmation email to provider.
- What happens if **admin sets seat limit below current team size**? System validates seat limit against current team member count from FR-009. If seat limit is set below current count (e.g., provider has 50 staff but admin sets limit to 30), system displays warning: "Current team size (50) exceeds new seat limit (30). Existing team members will not be removed, but no new invitations can be sent until limit is increased or team size is reduced." Admin must confirm to proceed. Existing team members remain active; only new invitations are blocked.
- What happens if **provider doesn't receive activation email**? Provider can click "Didn't receive activation email?" link on login page, enter their email, and request resend. System generates new one-time password setup link (expires 24 hours), invalidates previous link, and sends new email. Rate limited to 3 resend requests per hour per email. Admin can also manually resend from provider profile in FR-015 by clicking "Resend Activation Email" button in Quick Actions (visible only if password not yet set).
- What happens if **activation link expires (24 hours passed)**? Provider can request new activation email via login page resend flow or contact admin. Admin can manually resend from provider profile. When provider clicks expired link, system displays: "This activation link has expired. Request a new activation email or contact support."
- What happens if **provider tries to request activation resend but already activated account**? System displays generic message: "If an account exists with this email, an activation link will be sent." (doesn't reveal if account already activated for security). No email sent. This prevents email enumeration attacks.
- What happens if **admin accidentally creates duplicate provider with same email**? System validates email uniqueness during provider creation. If email already exists, system displays error: "Email address already in use by another provider (Provider Name: [existing provider]). Please use a different email or edit the existing provider." Creation blocked until unique email provided.

---

## Functional Requirements Summary

### Core Requirements

- **REQ-015-001**: System MUST allow admins to create new provider accounts via a multi-step wizard, including profile (Bio, Languages, Awards), clinic details, seat limit (team member capacity), and commission settings.
- **REQ-015-002**: System MUST enforce admin-initiated provider creation only (no self-service registration).
- **REQ-015-003**: System MUST support provider status lifecycle: Active → Suspended → (Reactivated OR Deactivated).
- **REQ-015-004**: System MUST allow providers to upload and manage their documents (license, certification, insurance) via FR-032. System MUST also allow admins to upload supplementary documents received externally. Documents are for record-keeping and do not block activation.
- **REQ-015-005**: System MUST log all provider management actions (creation, edits, status changes) in an immutable audit trail.
- **REQ-015-006**: System MUST send account activation email with one-time password setup link (expires 24 hours) when provider account is created. System MUST support activation email resend via self-service (provider login page) and admin manual resend (provider profile Quick Actions), with rate limiting (3 requests per hour per email) and automatic invalidation of previous links.

### Data Requirements

- **REQ-015-007**: System MUST maintain provider profile data aligned with FR-032 (Bio, Languages, Awards, Profile Picture, Contact details, etc.). Changes made by providers in FR-032 must sync to admin view in real-time.
- **REQ-015-008**: System MUST store uploaded provider documents in secure cloud storage (AES-256).
- **REQ-015-009**: System MUST store commission configuration (Model: Percentage/Flat, Value) per provider.
- **REQ-015-010**: System MUST store seat limit (maximum team members) per provider with default value of 100, adjustable range 1-500. Seat limit must be enforced by FR-009 when providers invite staff members.
- **REQ-015-011**: System MUST store activation token (one-time password setup link), token expiry timestamp (24 hours from generation), and password_set status per provider. System MUST invalidate previous tokens when new token is generated.

### Security & Privacy Requirements

- **REQ-015-012**: System MUST encrypt provider documents at rest and in transit.
- **REQ-015-013**: System MUST restrict document access to authenticated users (providers can access their own documents, admins can access all provider documents) with role-based permissions (providers can edit their own uploads, admins can edit admin uploads only).
- **REQ-015-014**: System MUST validate provider email uniqueness across the platform.
- **REQ-015-015**: System MUST enforce the platform-wide password policy defined in the Hairline Platform Constitution and shared authentication spec: passwords MUST be at least 12 characters long and include at least 1 uppercase letter, 1 lowercase letter, 1 number, and 1 special character from !@#$%^&(),.?\":{}|<>. This policy is centrally defined and NOT configurable per FR. Passwords MUST be hashed using bcrypt with a minimum cost factor of 12.
- **REQ-015-016**: System MUST rate limit activation email resend requests to 3 per hour per email address to prevent abuse and email flooding.

---

## Key Entities

- **Entity 1 - Provider**
  - **Key attributes**: provider_id (UUID), first_name, last_name, email (unique), phone, bio, languages (JSON), awards (JSON), medical_license_number, specialty, years_experience, status (enum: active, suspended, deactivated), featured (boolean), seat_limit (integer, default 100, range 1-500), commission_model (enum: percentage, flat), commission_value (decimal), password_hash (encrypted), password_set (boolean, default false), activation_token (UUID, nullable), activation_token_expiry (timestamp, nullable), activation_email_sent_count (integer, for rate limiting), last_activation_email_sent_at (timestamp), created_at, updated_at.
  - **Relationships**: One provider has many documents; one provider has one clinic; one provider has many status history records; seat_limit enforced by FR-009 when providers invite team members.

- **Entity 2 - Provider Document**
  - **Key attributes**: document_id (UUID), provider_id (foreign key), document_name, document_type (enum: medical_license, board_certification, insurance), file_url, upload_date, uploaded_by (admin_user_id), deleted (boolean for soft delete), deleted_at (timestamp).
  - **Relationships**: Many documents belong to one provider.

- **Entity 3 - Clinic Information**
  - **Key attributes**: clinic_id, provider_id, clinic_name, logo_url (profile picture), cover_image_url, address_fields, location_city, location_country, contact_phone, website_url, operating_hours.
  - **Relationships**: One clinic belongs to one provider (one-to-one).

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-11 | 1.0 | Initial PRD creation for FR-015 Provider Management (Admin-Initiated) | Claude (AI Assistant) |
| 2025-12-07 | 1.1 | **Major alignment update with FR-032:** <br>• Added cross-module integration notes linking to FR-032 (Provider Dashboard Settings) in Executive Summary and Module Scope<br>• Removed all document expiration date fields and related workflows (documents are for record-keeping only)<br>• Removed all out-of-scope items: Save Draft functionality, Tier-based commission references, Document verification workflow (approve/reject)<br>• Aligned all profile fields with FR-032: Profile Picture (5MB, 200x200px min), Cover Image (10MB, 1920x300px), Bio/Description (500 chars, min 50), Languages (multi-select chips from FR-026), Awards (with issuer, description, year, image), Contact Phone, Location (City, Country), Website URL<br>• Clarified activation logic: only required fields block activation (First Name, Last Name, Email, Clinic Name, Bio min 50 chars, at least 1 Language); documents do NOT block activation<br>• Updated Success Criteria to remove verification/expiration references and focus on record-keeping approach<br>• Updated Business Workflows, Screen Specifications (Wizard Steps and Tabbed View), User Stories, Edge Cases, and Entity definitions<br>• Added Admin Editability Rules section distinguishing admin-only vs provider-editable fields (via FR-032)<br>• Updated document entity to include document_type, uploaded_by, soft delete fields<br>• **Added Seat Limit field** to Screen 2 Step 1 (Basic Information): Maximum team members (staff) capacity per provider, default 100, range 1-500, adjustable by admin. Aligns with FR-009 team management enforcement. Added to Business Rules (Rule 7), Entity definitions, Functional Requirements (REQ-015-009), and Edge Cases<br>• **Completely restructured Screen 3** to table format matching FR-032 structure with all 5 tabs: (1) Basic Information, (2) Languages, (3) Staff List, (4) Awards, (5) Reviews, plus admin-only tabs: (6) Documents, (7) Commission & Financials, (8) Activity Log. All fields now documented in table format with Admin/Provider editability clearly marked<br>• **Added provider onboarding workflow** to Main Flow: Secure password setup via one-time email link (expires 24 hours), first login prompts profile completion via FR-032, changes sync to admin view<br>• **Added activation email resend functionality** (Alternative Flow A1): Provider self-service resend via login page + Admin manual resend via Quick Actions button in Screen 3. Rate limited to 3 requests/hour, previous tokens invalidated, secure handling of expired links. Added to Edge Cases, Functional Requirements (REQ-015-006, REQ-015-011, REQ-015-015, REQ-015-016), and Entity definitions with activation_token fields<br>• **Enhanced User Story 3** with detailed suspension workflow scenarios including existing appointments handling, suspended login experience, and reactivation process<br>• **Removed redundant User Stories 5 & 6** (provider-side actions) as these are fully covered in FR-032 User Story 1 | Claude (AI Assistant) |
| 2025-12-07 | 1.2 | **Major cross-module update - Document management redesign:** Completely restructured Tab 6: Documents to reflect new document management model. Removed "Admin-Only" designation. Providers now manage their own documents via FR-032 Tab 6 (upload, replace, delete); admin role shifted to oversight and supplementary uploads. Updated tab to display all documents with "Uploaded By" badge (Provider/Admin); Admin can view all documents, upload additional documents received externally (email, postal mail), and add notes, but cannot replace/delete provider-uploaded documents (only provider can via FR-032); Admin-uploaded documents show "Admin - [name]" badge and admin has full control over these. Added bidirectional document sync (FR-032 ↔ FR-015 within 1 minute); Updated Business Rules to clarify provider primary management vs. admin oversight model; Added sort/filter options, audit logging enhancements, and comprehensive use case notes. Aligns with FR-032 v1.2 which added full document management capabilities for providers | Claude (AI Assistant) |
| 2025-12-08 | 1.3 | **Constitution & System PRD alignment update:** <br>• Updated REQ-015-015 to reference the platform-wide password policy from the Hairline Platform Constitution and shared authentication spec (minimum 12 characters, required character classes, bcrypt with minimum cost factor 12, not configurable per FR)<br>• Clarified that sensitive actions (Commission and Seat Limit changes, Commission editing) require admin re-authentication via password in MVP, and MUST transition to MFA-based re-authentication once the shared MFA stack from FR-026 / FR-031 is delivered (all MFA references in this FR are future, non-MVP behavior)<br>• Aligned high-level system behaviour with system-prd.md FR-015 by explicitly reflecting the record-keeping-only document model and Percentage/Flat Rate commission configuration (tier-based commissions deferred to a future FR) | Claude (AI Assistant) |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | [Name] | [Date] | [Status] |
| Technical Lead | [Name] | [Date] | [Status] |
| Stakeholder | [Name] | [Date] | [Status] |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B
**Based on**: system-prd.md FR-015 (lines 1013-1041)
**Last Updated**: 2025-11-11
