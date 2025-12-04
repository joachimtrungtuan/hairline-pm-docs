# Product Requirements Document: Provider Management (Admin-Initiated)

**Module**: A-02: Provider Management & Onboarding
**Feature Branch**: `fr015-provider-management`
**Created**: 2025-11-11
**Status**: Draft
**Source**: FR-015 from system-prd.md (lines 1013-1041)

---

## Executive Summary

The Provider Management module enables administrators to onboard, verify, and manage hair transplant providers who will serve patients through the Hairline platform. This module is strictly admin-initiated—there is no self-service provider registration. Admins manually create provider accounts, upload and verify required documentation (medical licenses, certifications, insurance), configure commission structures, and manage provider lifecycle status from draft through active, suspended, and deactivated states. The module also includes featured provider designation to control visibility in the patient-facing application, enabling admins to highlight high-quality providers for patient discovery and booking. This module operates as the foundational gateway that determines which providers can participate in the platform ecosystem, establishing the trusted provider network that patients will access for consultations, quotes, and treatment bookings.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-XX)**: Views featured provider listings (data consumed from A-02), no direct interaction with provider management workflows
- **Provider Platform (PR-XX)**: Providers view their own profile status and documentation verification progress (read-only access to data managed by A-02)
- **Admin Platform (A-02)**: Full provider lifecycle management including creation, document verification, commission configuration, status changes, and featured designation
- **Shared Services (S-XX)**: S-03 (Notification Service) for provider status change notifications; S-04 (File Storage) for document uploads

### Multi-Tenant Breakdown

**Patient Platform (P-XX)**:

- Display featured providers in provider discovery/search interfaces
- Show verified provider badges and basic profile information (name, specialties, clinic location)
- No ability to view or modify provider management data

**Provider Platform (PR-XX)**:

- Providers view their own account status (draft, active, suspended, deactivated)
- Providers see document verification status (pending, approved, rejected) for licenses, certifications, insurance
- Providers view configured commission rates (read-only)
- Providers cannot self-register, edit commission rates, or change their own status

**Admin Platform (A-02)**:

- Create new provider accounts with complete profile setup
- Upload and verify provider documentation (medical licenses, board certifications, malpractice insurance)
- Configure commission structures (percentage-based or tier-based)
- Transition provider status through lifecycle (Draft → Active → Suspended → Deactivated)
- Toggle featured provider designation to control patient app visibility
- Manage document expiration reminders and re-verification workflows
- View comprehensive audit logs of all provider management actions

**Shared Services (S-XX)**:

- **S-03 (Notification Service)**: Sends email notifications to providers when status changes (account activated, documents approved/rejected, account suspended). SMS notifications are envisioned for future phases once S-03 SMS support is enabled, but **no SMS is sent in MVP**.
- **S-05 (Media Storage Service)**: Stores uploaded provider documents with secure access controls and encryption
- **S-06 (Audit Log Service)**: Logs all provider management actions (creation, edits, status changes, document verifications) for compliance and oversight

### Communication Structure

**In Scope**:

- Email notifications to providers when admin activates their account
- Email alerts to providers when documents are approved or rejected (SMS alerts are future, not MVP)
- Automated reminders to admins when provider documents approaching expiration (30 days before expiry)
- Notification to providers when their account is suspended or deactivated with reason provided
- In-app notifications to providers (within Provider Platform) for status changes

**Out of Scope**:

- Direct messaging between admin and provider (handled by separate communication module if needed)
- Provider onboarding welcome sequences beyond initial account activation notification (handled by provider onboarding communication flows)
- Patient notifications about new providers joining platform (handled by P-XX marketing notification flows)

### Entry Points

- **Admin-Initiated**: Admin accesses "Provider Management" section in Admin Platform dashboard → selects "Add New Provider" to initiate provider creation workflow
- **Admin Oversight**: Admin opens "Providers" list view to see all providers across all statuses (draft, active, suspended, deactivated) with filtering and search
- **Document Verification**: Admin navigates to individual provider profile → "Documents" tab to review, approve, or reject uploaded licenses, certifications, and insurance
- **Provider Profile Access (Provider-Side)**: Provider logs into Provider Platform → views "My Profile" section to see account status, document verification progress, and commission configuration (read-only)

---

## Business Workflows

### Main Flow: Admin Creates and Activates New Provider

**Actors**: Admin, System, Provider (receives notifications)
**Trigger**: Admin decides to onboard a new hair transplant provider to the platform
**Outcome**: Provider account created with "Active" status, provider notified and can log into Provider Platform

**Steps**:

1. Admin navigates to Admin Platform → "Provider Management" section
2. Admin clicks "Add New Provider" button
3. System displays Provider Creation Form with sections: Basic Information, Contact Details, Clinic/Practice Information, Document Upload, Commission Configuration
4. Admin enters provider basic information:
   - Full name (first, last, middle initial)
   - Medical license number
   - Specialty (e.g., "Hair Transplant Surgeon", "Dermatologist")
   - Years of experience
5. Admin enters contact details:
   - Email address (will be used for provider login)
   - Phone number (with country code)
   - Secondary contact email (optional)
6. Admin enters clinic/practice information:
   - Clinic name
   - Clinic address (street, city, state/province, postal code, country)
   - Clinic phone number
   - Operating hours
7. Admin uploads required documents:
   - Medical license (PDF/image file, must include expiration date)
   - Board certifications (PDF/image, expiration date)
   - Malpractice insurance certificate (PDF/image, expiration date)
   - System extracts expiration dates from documents or prompts admin to enter manually
8. Admin configures commission structure:
   - Selects commission type: "Percentage-based" or "Tier-based"
   - If percentage-based: enters percentage rate (5-30%, system validates range)
   - If tier-based: defines tiers (e.g., 0-10 procedures = 20%, 11-50 procedures = 15%, 51+ procedures = 10%)
9. Admin reviews all entered information in summary view
10. Admin clicks "Create Provider (Draft)" button
11. System validates all required fields, creates provider record with status = "Draft"
12. System generates temporary password and sends welcome email to provider with login instructions
13. Admin navigates to newly created provider profile → clicks "Activate Provider" button
14. System prompts admin to confirm: "Are you sure you want to activate [Provider Name]? Provider will be able to log in and receive patient bookings."
15. Admin confirms activation
16. System changes provider status from "Draft" to "Active"
17. System sends "Account Activated" email notification to provider with login credentials and onboarding instructions
18. Provider can now log into Provider Platform and accept patient consultations/bookings

### Alternative Flows

**A1: Admin Saves Provider as Draft for Later Completion**:

- **Trigger**: Admin does not have all required information during provider creation session
- **Steps**:
  1. Admin enters partial provider information in creation form
  2. Admin clicks "Save as Draft" button (instead of "Create Provider (Draft)")
  3. System saves partial provider record with status = "Draft" and marks incomplete fields
  4. Admin can return later to "Providers (Draft)" list, select incomplete provider, and continue editing
  5. When all required fields complete, admin finalizes creation and optionally activates provider
- **Outcome**: Provider record saved as draft, admin can complete later without data loss

**A2: Admin Configures Tier-Based Commission Structure**:

- **Trigger**: Admin selects "Tier-based" commission type during provider creation
- **Steps**:
  1. System displays tier configuration interface with fields: "Tier Name", "Procedure Count Range (From - To)", "Commission Rate (%)"
  2. Admin adds multiple tiers (minimum 2 tiers required):
     - Tier 1: "Starter" | 0-10 procedures | 20% commission
     - Tier 2: "Standard" | 11-50 procedures | 15% commission
     - Tier 3: "Premium" | 51+ procedures | 10% commission
  3. System validates tier ranges do not overlap and cover all procedure counts sequentially
  4. Admin saves tier configuration
  5. System calculates provider's current tier based on completed procedure count (initially Tier 1 for new providers)
- **Outcome**: Tier-based commission structure configured, provider commission rate adjusts automatically as procedure count increases

**A3: Admin Marks Provider as Featured for Patient App Visibility**:

- **Trigger**: Admin wants to highlight a high-quality provider in patient discovery interfaces
- **Steps**:
  1. Admin navigates to active provider profile
  2. Admin opens "Visibility Settings" section
  3. Admin toggles "Featured Provider" switch to ON
  4. System prompts: "Featured providers appear prominently in patient search results and homepage. Confirm?"
  5. Admin confirms
  6. System sets provider.featured = true
  7. Provider profile now appears in "Featured Providers" section of Patient Platform with badge
  8. System logs featured status change in audit trail
- **Outcome**: Provider designated as featured, visible in patient app's prominent provider sections

**A4: Admin Approves Uploaded Provider Documents**:

- **Trigger**: Admin reviews provider documents that were uploaded during creation or by provider later
- **Steps**:
  1. Admin navigates to provider profile → "Documents" tab
  2. System displays list of uploaded documents with status: "Pending Review"
  3. Admin clicks on document (e.g., "Medical License") to view full-screen preview
  4. Admin verifies document authenticity, expiration date, and issuing authority
  5. Admin clicks "Approve Document" button
  6. System updates document verification status to "Approved" and records admin ID, timestamp
  7. System sends notification to provider: "Your [Document Type] has been verified and approved"
  8. If all required documents approved, system enables "Activate Provider" button (if provider still in Draft status)
- **Outcome**: Document verified and approved, provider can proceed toward activation

**B1: Admin Rejects Provider Document with Reason**:

- **Trigger**: Admin identifies issue with uploaded provider document (expired, illegible, incorrect document type)
- **Steps**:
  1. Admin reviews document in provider profile → "Documents" tab
  2. Admin identifies issue (e.g., medical license expired 6 months ago)
  3. Admin clicks "Reject Document" button
  4. System prompts admin to enter rejection reason: "License expired on [date]. Please upload current valid license."
  5. Admin enters reason and clicks "Confirm Rejection"
  6. System updates document status to "Rejected", stores rejection reason and timestamp
  7. System sends email notification to provider: "Your [Document Type] was not approved. Reason: [rejection reason]. Please upload a corrected document."
  8. Provider receives in-app notification to re-upload document
  9. System prevents provider activation until all required documents approved
- **Outcome**: Document rejected with clear reason, provider notified to correct and re-upload

**B2: Admin Attempts to Activate Provider with Incomplete Documentation**:

- **Trigger**: Admin tries to activate provider before all required documents are approved
- **Steps**:
  1. Admin navigates to provider profile with status = "Draft"
  2. Admin clicks "Activate Provider" button
  3. System validates provider record:
     - Checks if medical license approved: NO (status = "Pending Review")
     - Checks if board certification approved: YES
     - Checks if malpractice insurance approved: NO (status = "Rejected")
  4. System displays error message: "Cannot activate provider. Missing required documents: Medical License (pending review), Malpractice Insurance (rejected - re-upload required)."
  5. Admin must approve pending documents and ensure rejected documents are corrected before activation allowed
- **Outcome**: Activation blocked, admin directed to resolve documentation issues before proceeding

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
- **Status Badge Colors**: Draft (gray), Active (green), Suspended (yellow), Deactivated (red)
- **Featured Badge**: Gold star icon displayed next to provider name if featured = true
- **Documents Status Column**: Shows "Complete" (all approved), "Pending" (some pending review), "Rejected" (some rejected), "Incomplete" (some missing)
- **Quick Actions**: Each row includes action buttons: "View Profile", "Edit", "Suspend" (if active), "Activate" (if draft/suspended), "Deactivate" (if active/suspended)
- **Sorting**: Table columns sortable by name (alphabetical), created date (chronological), commission rate (numerical)
- **Pagination**: Display 50 providers per page, with page navigation controls

**Notes**:

- Use color-coded status badges for quick visual scanning
- Featured providers should have prominent visual indicator (star icon)
- Ensure "Add New Provider" button prominently displayed in top-right corner
- Implement real-time status updates (e.g., if provider status changes, table refreshes without full page reload)

---

### Screen 2: Provider Creation/Edit Form

**Purpose**: Allows admins to create new provider accounts or edit existing provider information with comprehensive profile setup

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| First Name | text | Yes | Provider's legal first name | Max 50 chars, letters only |
| Last Name | text | Yes | Provider's legal last name | Max 50 chars, letters only |
| Middle Initial | text | No | Provider's middle initial | 1 char, letter only |
| Medical License Number | text | Yes | Government-issued medical license identifier | Max 50 chars, alphanumeric |
| Specialty | select dropdown | Yes | Provider's medical specialty | Options: "Hair Transplant Surgeon", "Dermatologist", "Plastic Surgeon", "Other" |
| Years of Experience | number | Yes | Total years practicing medicine | Range: 1-60 |
| Email Address | email | Yes | Provider's primary email (used for login) | Valid email format, unique in system |
| Phone Number | phone | Yes | Provider's contact phone with country code | Valid phone format, country code required |
| Secondary Email | email | No | Alternate contact email | Valid email format |
| Clinic Name | text | Yes | Name of provider's clinic/practice | Max 100 chars |
| Clinic Address | address | Yes | Full clinic address (street, city, state, postal, country) | All address fields required |
| Clinic Phone | phone | Yes | Clinic's main phone number | Valid phone format |
| Operating Hours | text | No | Clinic operating hours (e.g., "Mon-Fri 9AM-5PM") | Max 200 chars |
| Medical License Upload | file upload | Yes | PDF or image of medical license | Max 10MB, PDF/JPEG/PNG only |
| License Expiration Date | date | Yes | Expiration date of medical license | Must be future date |
| Board Certification Upload | file upload | Yes | PDF or image of board certification | Max 10MB, PDF/JPEG/PNG only |
| Certification Expiration | date | Yes | Expiration date of certification | Must be future date |
| Malpractice Insurance Upload | file upload | Yes | PDF or image of insurance certificate | Max 10MB, PDF/JPEG/PNG only |
| Insurance Expiration | date | Yes | Expiration date of insurance | Must be future date |
| Commission Type | radio button | Yes | Commission structure type | Options: "Percentage-based", "Tier-based" |
| Commission Percentage | number | Conditional (if Percentage-based) | Commission rate percentage | Range: 5-30, decimal allowed (e.g., 12.5) |
| Tier Configuration | dynamic form | Conditional (if Tier-based) | Define tiers with ranges and rates | Minimum 2 tiers, ranges sequential, rates 5-30% |

**Business Rules**:

- **Email Uniqueness**: System must validate provider email does not already exist in database before allowing creation
- **Document Upload**: All three document types (license, certification, insurance) required before provider can be activated
- **Expiration Date Validation**: System must ensure all expiration dates are in the future (cannot create provider with expired documents)
- **Commission Type Conditional Logic**: If "Percentage-based" selected, show single percentage input field; if "Tier-based" selected, show tier configuration interface
- **Tier Validation**: For tier-based commissions, system must validate:
  - Minimum 2 tiers defined
  - Tier procedure count ranges are sequential with no gaps or overlaps (e.g., 0-10, 11-50, 51+)
  - Commission rates within 5-30% range for all tiers
- **Save vs. Activate**: Form includes two submit buttons:
  - "Save as Draft": Creates provider with status = "Draft" (can be edited later)
  - "Save and Activate": Creates provider with status = "Active" (requires all required fields complete and documents uploaded)
- **Edit Mode**: When editing existing provider, form pre-populates with current values; "Save Changes" button replaces creation buttons

**Notes**:

- Implement file preview for uploaded documents (inline viewer or modal)
- Show file upload progress indicator for large documents
- Provide clear error messages for validation failures (e.g., "Email already in use by another provider")
- For tier-based commissions, include "Add Tier" and "Remove Tier" buttons for dynamic tier management
- Include "Cancel" button that discards unsaved changes and returns to provider dashboard

---

### Screen 3: Provider Profile Details View

**Purpose**: Displays comprehensive view of individual provider's profile, documents, status history, and allows admin actions (activate, suspend, deactivate, edit)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Provider Name | text (read-only) | N/A | Full name displayed prominently at top | Display format: "Dr. [First] [Last]" |
| Status Badge | visual indicator | N/A | Current status with color-coded badge | Draft (gray), Active (green), Suspended (yellow), Deactivated (red) |
| Featured Toggle | toggle switch | No | Admin can toggle featured status on/off | Only editable if provider status = Active |
| Basic Information Section | read-only display | N/A | Shows: Specialty, License Number, Years of Experience, Email, Phone | Display only, edit via "Edit Profile" button |
| Clinic Information Section | read-only display | N/A | Shows: Clinic Name, Address, Phone, Operating Hours | Display only |
| Commission Configuration | read-only display | N/A | Shows commission type (Percentage/Tier-based) and current rate or tier breakdown | Display only |
| Documents Tab | tabbed interface | N/A | Lists all uploaded documents with status: Medical License, Board Certification, Malpractice Insurance | Each document shows: filename, upload date, verification status, expiration date, admin actions (Approve/Reject/View) |
| Status History Tab | tabbed interface | N/A | Chronological log of status changes | Shows: Date, Previous Status, New Status, Admin (who made change), Reason (if applicable) |
| Activity Log Tab | tabbed interface | N/A | Comprehensive audit trail of all provider-related actions | Shows: Timestamp, Action Type, Admin User, Details |
| Action Buttons | button group | N/A | Context-sensitive actions based on current status | Options: Edit Profile, Activate Provider, Suspend Provider, Deactivate Provider, Send Notification |

**Business Rules**:

- **Status-Based Action Visibility**:
  - If status = "Draft": Show "Edit Profile", "Activate Provider" buttons
  - If status = "Active": Show "Edit Profile", "Suspend Provider", "Deactivate Provider", "Toggle Featured" buttons
  - If status = "Suspended": Show "Reactivate Provider", "Deactivate Provider" buttons
  - If status = "Deactivated": No action buttons (deactivation is final, must create new provider if re-onboarding needed)
- **Featured Toggle**: Only enabled if provider status = "Active"; disabled for draft/suspended/deactivated providers
- **Document Approval**: Each document row in Documents tab includes:
  - "Approve" button (if status = Pending or Rejected)
  - "Reject" button (if status = Pending or Approved) — opens modal to enter rejection reason
  - "View Document" button — opens full-screen document viewer
- **Expiration Warnings**: System displays warning badge next to documents expiring within 30 days: "Expires in [X] days"
- **Status History**: Automatically logged whenever provider status changes; includes admin who made change, timestamp, and optional reason (required for suspension/deactivation)
- **Activity Log**: Captures all actions: profile edits, document uploads/approvals/rejections, status changes, commission configuration changes, featured status toggles

**Notes**:

- Use tabbed interface to organize information (Profile, Documents, Status History, Activity Log) without overwhelming single view
- Implement confirmation modals for critical actions (Activate, Suspend, Deactivate) with required reason input for suspension/deactivation
- Display document expiration dates prominently with visual indicators (green = >30 days, yellow = 7-30 days, red = <7 days or expired)
- Include "Send Notification" button to manually trigger emails to provider (e.g., remind to update expiring documents)

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

- **Rule 1**: All provider accounts must be created by admins—no self-service provider registration allowed (enforced at application and API level)
- **Rule 2**: Provider cannot be activated until all required documents (medical license, board certification, malpractice insurance) are uploaded and approved by admin
- **Rule 3**: Provider status transitions follow strict lifecycle: Draft → Active → Suspended → (Reactivated to Active OR Deactivated)
- **Rule 4**: Deactivation is permanent—deactivated providers cannot be reactivated; admin must create new provider account if re-onboarding required
- **Rule 5**: Commission rates apply to all transactions processed after rate configuration; retroactive rate changes do not affect past transactions
- **Rule 6**: System automatically sends reminder notifications to admins 30 days before provider document expiration dates
- **Rule 7**: Featured provider designation only available for providers with status = "Active"; suspended/deactivated providers automatically unfeatured

### Data & Privacy Rules

- **Privacy Rule 1**: Provider contact information (email, phone) visible only to admins; patients see clinic phone/email (not provider's personal contact)
- **Privacy Rule 2**: Uploaded provider documents (licenses, certifications, insurance) encrypted at rest using AES-256 and accessible only to admins with document verification permissions
- **Privacy Rule 3**: Provider medical license numbers and sensitive credentials masked in activity logs (e.g., "License Number: ****1234") to prevent unauthorized exposure
- **Audit Rule**: All provider management actions logged with timestamp, admin user ID, IP address, and action details for compliance and dispute resolution
- **HIPAA/GDPR Compliance**: Provider personal data (name, email, phone, documents) subject to data retention policies; deactivated providers' data retained for 7 years for legal/regulatory compliance, then eligible for deletion
- **Data Access Control**: Only admins with "Provider Management" role permission can create, edit, or change provider status; read-only admins can view but not modify

### Admin Editability Rules

**Editable by Admin**:

- Provider basic information (name, specialty, years of experience, contact details)
- Clinic information (name, address, phone, operating hours)
- Commission configuration (percentage rate or tier structure)
- Document uploads (can replace existing documents, request re-upload)
- Provider status (Draft, Active, Suspended, Deactivated) with required reason for suspension/deactivation
- Featured provider designation (toggle on/off for active providers)
- Document verification status (Approve, Reject with reason)

**Fixed in Codebase (Not Editable)**:

- Provider status lifecycle flow (Draft → Active → Suspended → Deactivated/Reactivated) — cannot skip states or reverse deactivation
- Commission rate range constraints (5-30% for percentage-based, 5-30% per tier for tier-based)
- Required document types (medical license, board certification, malpractice insurance) — cannot be changed or made optional
- Document expiration reminder timing (30 days before expiry) — hardcoded in notification service
- Deactivation finality rule (deactivated providers cannot be reactivated) — enforced at database and application layers
- Encryption standards for document storage (AES-256) — cannot be downgraded

**Configurable with Restrictions**:

- Document file size limits (default 10MB per file; admin can configure up to 50MB via system settings, but cannot exceed 50MB hard limit)
- Provider dashboard pagination (default 50 rows per page; admin can configure 25/50/100 via user preferences)
- Commission rate adjustment frequency (admin can change provider commission rates anytime, but changes apply only to future transactions, not retroactively)

### Payment & Billing Rules

- **Commission Rule 1**: Commission rates configured in this module apply to all provider earnings from patient bookings (consultations, procedures, aftercare services)
- **Commission Rule 2**: Percentage-based commissions calculated as: Provider Payout = Transaction Amount × (1 - Commission Rate)
  - Example: $1000 procedure, 15% commission → Provider receives $850, platform retains $150
- **Commission Rule 3**: Tier-based commissions calculated based on provider's cumulative completed procedure count in current billing period (monthly)
  - Provider's tier automatically updated at end of each month based on procedures completed in that month
  - Example: Provider completes 12 procedures in January → moves from Tier 1 (20% commission) to Tier 2 (15% commission) for February
- **Commission Rule 4**: Commission configuration changes take effect immediately for new transactions; in-progress transactions use commission rate active at time of booking
- **Billing Rule 1**: Provider payouts calculated weekly and transferred to provider's registered bank account (configured separately in provider financial settings, not in this module)
- **Billing Rule 2**: Admins can view provider commission history and earnings reports in separate "Provider Financials" module (out of scope for FR-015)

---

## Success Criteria

### Patient Experience Metrics

- **SC-001**: Patients can discover and view featured provider profiles in Patient Platform within 1 second of search query (data sourced from A-02 featured providers)
- **SC-002**: 100% of patient-facing provider information (name, clinic, specialty) displays accurately and matches admin-configured data in A-02 with no discrepancies
- **SC-003**: Patients see only verified, active providers in search results (no draft/suspended/deactivated providers visible), ensuring trust and booking reliability

### Provider Efficiency Metrics

- **SC-004**: Providers receive account activation notification within 1 minute of admin activating their account, enabling immediate platform access
- **SC-005**: Providers can view their document verification status and commission configuration in Provider Platform within 2 seconds of navigation
- **SC-006**: 90% of providers successfully log in and access their profile on first attempt after receiving activation credentials (low login failure rate)

### Admin Management Metrics

- **SC-007**: Admins can create a complete provider profile (all sections filled, documents uploaded, commission configured) in under 10 minutes on average
- **SC-008**: Admins can filter and search provider list (1000+ providers) and retrieve results in under 2 seconds, enabling efficient provider oversight
- **SC-009**: Admins can approve or reject a provider document in under 30 seconds per document, streamlining verification workflows
- **SC-010**: 100% of provider status changes (activate, suspend, deactivate) logged in audit trail with timestamp, admin user, and reason (full accountability)
- **SC-011**: Admins receive automated reminder notifications 30 days before provider document expiration for 100% of expiring documents (no manual tracking needed)
- **SC-012**: Admin dashboard displays real-time provider status counts (draft, active, suspended, deactivated) with <1 second refresh latency

### System Performance Metrics

- **SC-013**: Provider creation/edit form submission completes within 3 seconds for 95% of requests (excluding large document uploads)
- **SC-014**: Document upload (up to 10MB per file) completes within 10 seconds for 90% of uploads on standard broadband connections
- **SC-015**: Provider profile page loads (all tabs: profile, documents, status history, activity log) within 2 seconds for 95% of requests
- **SC-016**: System supports 100 concurrent admin users managing providers without performance degradation
- **SC-017**: 99.9% uptime for provider management functionality (excluding scheduled maintenance)

### Business Impact Metrics

- **SC-018**: Provider onboarding time reduced by 60% compared to manual/offline provider onboarding processes (baseline: 5 hours manual → target: 2 hours in-system)
- **SC-019**: Provider document verification errors reduced by 80% through structured validation and expiration tracking (fewer expired/invalid documents accepted)
- **SC-020**: 95% of providers have complete, verified profiles (all documents approved, commission configured) within 48 hours of initial account creation
- **SC-021**: Featured provider designation increases patient booking conversion rate by 25% compared to non-featured providers (measured in Patient Platform analytics)

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **FR-001 / Module A-01: Admin Authentication & Authorization**
  - **Why needed**: Admins must be authenticated and have "Provider Management" role permissions to access provider creation, editing, and status management features
  - **Integration point**: A-02 verifies admin user session token and role permissions before allowing provider management actions; API endpoints protected by role-based access control (RBAC)

- **FR-XXX / Module PR-01: Provider Authentication & Profile Management**
  - **Why needed**: Providers created in A-02 must be able to log into Provider Platform to view their profile status and document verification progress
  - **Integration point**: A-02 creates provider user account credentials (email/password) and passes to PR-01 authentication service; providers authenticate via PR-01 to access read-only profile data sourced from A-02

- **FR-XXX / Module P-02: Provider Discovery & Search (Patient-Facing)**
  - **Why needed**: Featured providers designated in A-02 must be displayed prominently in Patient Platform search and discovery interfaces
  - **Integration point**: P-02 queries A-02 provider data filtered by (status = "Active" AND featured = true) to populate featured provider listings; includes provider name, clinic, specialty, profile photo

- **FR-XXX / Module S-03: Notification Service**
  - **Why needed**: Providers must receive email notifications when admins activate accounts, approve/reject documents, or suspend/deactivate accounts; SMS may be added later for critical events
  - **Integration point**: A-02 triggers notification events to S-03 API with templates (e.g., "account_activated", "document_rejected") and provider contact details; S-03 sends templated emails asynchronously. SMS, if enabled in future, would also be orchestrated by S-03.

- **FR-XXX / Module S-05: Media Storage Service**
  - **Why needed**: Provider documents (licenses, certifications, insurance) must be securely stored with encryption and access controls
  - **Integration point**: A-02 uploads documents to S-05 API with metadata (provider ID, document type, expiration date); S-05 returns secure download URLs accessible only to authorized admins

- **FR-XXX / Module S-06: Audit Log Service**
  - **Why needed**: All provider management actions (creation, edits, status changes, document verifications) must be logged for compliance and audit trails
  - **Integration point**: A-02 sends audit log events to S-06 API with structured data (timestamp, admin user ID, action type, entity ID, before/after values); S-06 persists logs and provides query interface for admin reporting

### External Dependencies (APIs, Services)

- **External Service 1: Email Delivery Service (e.g., SendGrid, AWS SES)**
  - **Purpose**: Sends provider notification emails (account activation, document verification, status changes)
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
  - **Why needed**: Standardized notification messages for provider account lifecycle events (activation, document verification, suspension) must exist; in MVP only email templates are used, with SMS templates reserved for future phases
  - **Source**: Notification templates pre-configured in S-03 Notification Service; A-02 references email template IDs (e.g., "provider_activation_email") when triggering notifications. SMS templates, if configured later, would be used only once SMS delivery is enabled.

- **Entity 3: Document Type Configuration**
  - **Why needed**: System must know which document types are required for provider verification (medical license, board certification, malpractice insurance)
  - **Source**: Document type definitions configured in admin settings or hardcoded in A-02 codebase; includes required fields (expiration date), validation rules (file size, format), and verification status options (pending, approved, rejected)

---

## Assumptions

### User Behavior Assumptions

- **Assumption 1**: Admins have direct access to provider documentation (licenses, certifications) either physically or digitally before initiating provider creation (e.g., provider sends documents via email or postal mail to admin)
- **Assumption 2**: Admins will verify provider document authenticity manually (e.g., cross-reference medical license number with state medical board database) before approving in system
- **Assumption 3**: Providers check their email regularly (at least daily) to receive account activation and document verification notifications
- **Assumption 4**: Admins will proactively monitor document expiration dates and follow up with providers to obtain updated documents before expiry (reminder notifications assist but do not replace manual follow-up)

### Technology Assumptions

- **Assumption 1**: Admins access Admin Platform via desktop/laptop computers (not mobile devices) due to complexity of provider creation forms and document review workflows
- **Assumption 2**: Admins have reliable broadband internet connectivity for uploading provider documents (up to 10MB per file)
- **Assumption 3**: Providers access Provider Platform to view profile status via both desktop and mobile devices (responsive design required for provider profile view)
- **Assumption 4**: Cloud file storage (S-04) provides 99.99% availability for document uploads and retrieval

### Business Process Assumptions

- **Assumption 1**: Provider onboarding is admin-initiated only—providers cannot register themselves; admins control provider network quality through manual vetting
- **Assumption 2**: Commission rate configuration occurs at provider creation time, but admins can adjust rates later as provider performance changes (e.g., reward high-performing providers with lower commission rates)
- **Assumption 3**: Document expiration reminders (30 days before expiry) provide sufficient lead time for providers to obtain and upload renewed documents
- **Assumption 4**: Suspended providers' existing bookings remain active (admin must manually cancel if needed); suspension only prevents new bookings
- **Assumption 5**: Deactivated providers' data retained indefinitely for legal/audit purposes; GDPR/data deletion requests handled via separate data privacy workflows (not in-scope for A-02)

---

## Implementation Notes

### Technical Considerations

- **Architecture**: Provider Management module follows admin-initiated CRUD (Create, Read, Update, Delete) pattern with state machine for status lifecycle (Draft → Active → Suspended → Deactivated)
- **Technology**: Document upload functionality should support chunked/resumable uploads for large files (up to 10MB) to handle unreliable admin connections
- **Performance**: Provider list dashboard with 1000+ providers requires pagination, indexing on status/created_date columns, and client-side filtering/sorting for responsive UI
- **Storage**: Provider documents stored in cloud object storage (S3-compatible) with server-side encryption (AES-256); document metadata (filename, upload date, verification status) stored in relational database
- **Validation**: Commission rate validation (5-30% range) enforced at both client-side (immediate feedback) and server-side (security) to prevent invalid configurations
- **State Machine**: Provider status transitions implemented as finite state machine with validation rules (e.g., cannot transition from Deactivated to any other status; must include reason for Suspend/Deactivate transitions)

### Integration Points

- **Integration 1: Admin Platform (A-02) → Notification Service (S-03)**
  - **Data format**: JSON payload with event type (e.g., "provider.activated"), provider ID, recipient (provider email/phone), template ID, and dynamic variables (e.g., provider name, login URL)
  - **Authentication**: Service-to-service authentication via API key in request header
  - **Error handling**: S-03 returns 202 Accepted (notification queued) or 4xx/5xx error; A-02 logs notification failures and displays warning to admin

- **Integration 2: Admin Platform (A-02) → File Storage Service (S-04)**
  - **Data format**: Multipart form-data for document uploads with metadata (provider ID, document type, expiration date)
  - **Authentication**: OAuth 2.0 service account token for S-04 API access
  - **Error handling**: S-04 returns 200 OK with document URL or 4xx/5xx error; A-02 retries upload up to 3 times with exponential backoff before failing

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
  - Async document upload processing (upload to S-04 asynchronously, update database when complete) to prevent blocking admin UI

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
2. **Given** provider receives activation email with login credentials, **When** provider clicks login link and enters credentials, **Then** provider successfully logs into Provider Platform and sees profile page with status = "Active", document verification statuses (all approved), and commission rate displayed
3. **Given** admin activates provider with featured = true, **When** patient opens Patient Platform provider search, **Then** newly activated provider appears in "Featured Providers" section with gold star badge

---

### User Story 2 - Admin Reviews and Approves Provider Documents (Priority: P1)

Admin reviews uploaded provider documents (medical license, board certification, malpractice insurance) in provider profile, verifies authenticity and expiration dates, and approves all documents. Provider receives notification that documents are verified.

**Why this priority**: Document verification is critical gate-keeping function ensuring only qualified, licensed providers onboarded; without document approval, providers cannot be activated.

**Independent Test**: Admin navigates to provider profile → Documents tab, clicks on each document to preview, verifies details, and clicks "Approve Document" for all three required documents; verify provider receives "Documents Approved" email notification.

**Acceptance Scenarios**:

1. **Given** provider has status = "Draft" with three documents uploaded (license, certification, insurance) with status = "Pending Review", **When** admin navigates to provider profile → Documents tab → clicks "View Document" on medical license → verifies details → clicks "Approve Document", **Then** system updates license verification status to "Approved", logs action in audit trail, and sends notification to provider: "Your Medical License has been verified and approved"
2. **Given** admin approves all three required documents (license, certification, insurance), **When** admin returns to provider profile page, **Then** system displays "Activate Provider" button enabled (was disabled while documents pending)
3. **Given** admin identifies expired license (expiration date in past), **When** admin clicks "Reject Document" → enters reason: "License expired on [date]. Please upload current valid license." → clicks "Confirm Rejection", **Then** system updates document status to "Rejected", stores reason, sends rejection email to provider, and keeps "Activate Provider" button disabled

---

### User Story 3 - Admin Suspends Provider Due to Policy Violation (Priority: P2)

Admin identifies provider violating platform terms (e.g., patient complaint, fraudulent billing) and suspends provider account with detailed reason. Provider receives suspension notification and cannot receive new bookings but can log in to view suspension notice.

**Why this priority**: Essential for platform trust and safety; admins must be able to quickly suspend problematic providers to protect patients and platform reputation.

**Independent Test**: Admin navigates to active provider profile, clicks "Suspend Provider", enters detailed reason, confirms action; verify provider status changes to "Suspended", provider receives suspension email, and provider cannot appear in patient search results.

**Acceptance Scenarios**:

1. **Given** provider has status = "Active" with featured = true, **When** admin clicks "Suspend Provider" → enters reason: "Multiple patient complaints regarding unprofessional conduct. Under investigation." → checks "Notify Provider" → clicks "Confirm Suspension", **Then** system changes status to "Suspended", sends suspension email to provider with reason, automatically sets featured = false, and removes provider from patient-facing search results
2. **Given** provider is suspended, **When** provider logs into Provider Platform, **Then** provider sees "Account Suspended" banner at top of page with message: "Your account has been suspended. Reason: [admin reason]. Contact support for assistance."
3. **Given** suspended provider has 5 upcoming patient bookings, **When** admin reviews bookings in separate booking management module, **Then** admin sees list of affected bookings and can manually cancel/reassign (suspension does not automatically cancel bookings)

---

### User Story 4 - Admin Configures Tier-Based Commission for High-Volume Provider (Priority: P2)

Admin creates provider account with tier-based commission structure to incentivize high procedure volumes. Commission rate automatically adjusts as provider completes more procedures each month.

**Why this priority**: Important for provider incentive alignment and platform economics; tier-based commissions encourage provider growth and loyalty but not critical for basic provider onboarding.

**Independent Test**: Admin creates provider with tier-based commission (3 tiers: 0-10 procedures = 20%, 11-50 = 15%, 51+ = 10%); verify tiers are saved, provider sees tier structure in their profile, and commission calculation reflects current tier based on procedure count.

**Acceptance Scenarios**:

1. **Given** admin is creating new provider, **When** admin selects commission type = "Tier-based" → adds Tier 1 (0-10 procedures, 20%) → adds Tier 2 (11-50 procedures, 15%) → adds Tier 3 (51+ procedures, 10%) → clicks "Save as Draft", **Then** system validates tier ranges (sequential, no gaps/overlaps), saves tier configuration, and displays tiers in provider profile commission section
2. **Given** provider created with tier-based commission starting at Tier 1 (20%), **When** provider completes 12 procedures in current month (crosses into Tier 2), **Then** system automatically updates provider's current tier to Tier 2 (15% commission) at end of month, applies new rate to next month's transactions, and sends notification to provider: "Congratulations! You've moved to Tier 2 (15% commission) based on 12 procedures completed."
3. **Given** admin edits existing provider's tier configuration (changes Tier 2 range from 11-50 to 11-30), **When** admin saves changes, **Then** system validates new tier ranges, updates configuration, applies changes to future transactions only (does not recalculate past commissions), and logs change in audit trail

---

### User Story 5 - Admin Receives Document Expiration Reminder and Requests Renewal (Priority: P3)

System automatically sends reminder to admin 30 days before provider's medical license expires. Admin contacts provider to request renewed license, provider uploads new document, admin reviews and approves.

**Why this priority**: Important for compliance and provider qualification maintenance, but not critical for initial onboarding; can be handled manually if automated reminders not yet implemented.

**Independent Test**: Set provider medical license expiration date to 30 days from today; verify admin receives automated reminder email with provider name and expiring document type; admin navigates to provider profile, requests renewal, provider uploads new license, admin approves.

**Acceptance Scenarios**:

1. **Given** provider's medical license has expiration date = 30 days from today, **When** system runs daily document expiration check (cron job at midnight UTC), **Then** system sends email to admin: "Reminder: Provider [Name]'s Medical License expires in 30 days on [date]. Please follow up to obtain renewed license."
2. **Given** admin receives expiration reminder, **When** admin navigates to provider profile → Documents tab, **Then** system displays yellow warning badge next to medical license: "Expires in 30 days" and highlights row in yellow
3. **Given** admin manually sends notification to provider requesting license renewal, **When** provider uploads new license with future expiration date, **Then** system updates document, sets status = "Pending Review", admin receives notification to review new document, and expiration warning clears after admin approves new license

---

### User Story 6 - Provider Views Own Profile Status in Provider Platform (Priority: P3)

Provider logs into Provider Platform after admin activates account and views profile information including account status, document verification statuses, commission configuration, and clinic details. Provider cannot edit any data (read-only view).

**Why this priority**: Useful for provider transparency and reducing support inquiries, but not critical for core provider onboarding workflow; providers can function without self-service profile view if admins communicate status manually.

**Independent Test**: Provider logs into Provider Platform after account activation, navigates to "My Profile" section; verify provider sees current status (Active), document verification statuses (all approved), commission rate (read-only), and clinic information; verify provider cannot edit any fields.

**Acceptance Scenarios**:

1. **Given** provider account status = "Active" with all documents approved, **When** provider logs into Provider Platform → navigates to "My Profile", **Then** provider sees profile page with status badge = "Active" (green), document verification statuses (Medical License: Approved, Board Certification: Approved, Malpractice Insurance: Approved), and commission rate (e.g., "15% per transaction")
2. **Given** provider has one document rejected (malpractice insurance), **When** provider views profile, **Then** provider sees rejected document highlighted in red with rejection reason displayed: "Insurance expired. Please upload current policy." and call-to-action button: "Upload New Document"
3. **Given** provider attempts to edit clinic name in profile view, **When** provider clicks on clinic name field, **Then** field remains read-only (not editable), tooltip displays: "Contact admin to update clinic information"

---

### Edge Cases

- What happens when **admin attempts to create provider with email already used by another provider**? System displays validation error: "Email address already in use by another provider. Please use a different email." Provider creation blocked until unique email provided.
- How does system handle **provider document upload fails mid-upload (network interruption)**? System supports resumable uploads; if upload interrupted, admin can retry from last successful chunk (does not restart entire 10MB upload from beginning).
- What occurs if **admin activates provider but notification email delivery fails (email service down)**? System queues notification for retry (up to 3 attempts over 1 hour); admin sees warning message: "Provider activated but notification email not yet delivered. Email delivery in progress." Admin can manually resend notification via "Send Notification" button.
- How to manage **two admins simultaneously editing same provider profile (concurrent edits)**? System implements optimistic locking; second admin to save receives error: "Provider profile was modified by another admin. Please refresh and re-enter your changes." Last-write-wins conflict resolution prevents data loss.
- What happens when **admin deactivates provider with 10 upcoming patient bookings**? System displays confirmation modal: "This provider has 10 upcoming bookings. Deactivation will automatically cancel all future bookings and notify affected patients. Continue?" If admin confirms, system cancels bookings, sends cancellation notifications to patients, and offers rebooking options.
- How does system handle **provider document expiration date passes while status = Draft (not yet activated)**? System does not send expiration reminders for draft providers (only active/suspended); when admin attempts to activate provider with expired document, system blocks activation: "Cannot activate provider. Medical License expired on [date]. Please upload renewed license."
- What occurs if **admin attempts to set commission rate outside 5-30% range (e.g., 35%)**? System displays client-side validation error immediately: "Commission rate must be between 5% and 30%." Server-side validation also enforces range; API returns 400 Bad Request if invalid rate submitted.
- How to manage **provider requests account closure (wants to be deactivated)**? Provider contacts admin (no self-service deactivation); admin navigates to provider profile → clicks "Deactivate Provider" → enters reason: "Provider requested account closure on [date]" → confirms deactivation. System deactivates account, cancels future bookings, sends confirmation email to provider.

---

## Functional Requirements Summary

### Core Requirements

- **FR-001**: System MUST allow admins to create new provider accounts with complete profile setup including basic information (name, email, license, specialty, experience), contact details, clinic information, document uploads (license, certification, insurance), and commission configuration (percentage or tier-based)
- **FR-002**: System MUST enforce admin-initiated provider creation only—no self-service provider registration allowed; provider creation restricted to authenticated admins with "Provider Management" role permission
- **FR-003**: System MUST support provider status lifecycle: Draft → Active → Suspended → (Reactivated OR Deactivated), with validation preventing invalid state transitions (e.g., cannot transition from Deactivated to any other status)
- **FR-004**: System MUST require all three document types (medical license, board certification, malpractice insurance) uploaded and approved before allowing provider activation
- **FR-005**: System MUST log all provider management actions (creation, edits, status changes, document approvals/rejections) in immutable audit trail with timestamp, admin user ID, IP address, and action details

### Data Requirements

- **FR-006**: System MUST maintain provider profile data including personal information (name, email, phone), clinic details (name, address, operating hours), document verification statuses (pending, approved, rejected), commission configuration (percentage or tier-based), and featured designation (true/false)
- **FR-007**: System MUST track provider document expiration dates and automatically send reminder notifications to admins 30 days before expiry
- **FR-008**: System MUST store uploaded provider documents (licenses, certifications, insurance) in secure cloud storage with encryption at rest (AES-256) and generate secure access URLs for admin document preview
- **FR-009**: System MUST record provider status change history with fields: previous status, new status, change date, admin user who made change, and reason (required for suspension/deactivation)

### Security & Privacy Requirements

- **FR-010**: System MUST encrypt provider documents at rest (AES-256) and in transit (TLS 1.3) to protect sensitive credentials and personal information
- **FR-011**: System MUST restrict provider document access to authenticated admins with "Provider Management" or "Document Verification" role permissions; providers can view their own documents only
- **FR-012**: System MUST mask provider medical license numbers in audit logs and activity reports (display last 4 digits only, e.g., "****1234") to prevent unauthorized credential exposure
- **FR-013**: System MUST validate provider email uniqueness across platform before allowing account creation (prevent duplicate provider accounts with same email)
- **FR-014**: System MUST retain deactivated provider data for 7 years minimum for legal/audit compliance, then mark eligible for deletion per GDPR/data retention policies

### Integration Requirements

- **FR-015**: System MUST trigger notification events to S-03 Notification Service when provider account activated, documents approved/rejected, or status changes (suspended/deactivated), including provider email/phone and notification template ID
- **FR-016**: System MUST upload provider documents to S-05 Media Storage Service with metadata (provider ID, document type, expiration date) and receive secure download URLs for admin access
- **FR-017**: System MUST expose read-only API endpoint for Provider Platform (PR-01) to fetch individual provider's own profile data (authenticated via provider user token, cannot access other providers' data)
- **FR-018**: System MUST expose public API endpoint for Patient Platform (P-02) to fetch featured provider listings (filtered by status = Active AND featured = true) with fields: name, clinic, specialty, profile photo URL
- **FR-019**: System MUST send structured audit log events to S-06 Audit Log Service for all provider management actions with event type, entity ID, admin user, timestamp, and before/after values

### Functional Requirements Needing Clarification

- **FR-020**: System MUST validate commission rate configuration with range 5-30% for percentage-based, 5-30% per tier for tier-based [NEEDS CLARIFICATION: Should system allow commission rates outside this range for special cases with admin override?]
- **FR-021**: System MUST prevent provider activation if any required document expired [NEEDS CLARIFICATION: Should system allow activation with expired documents if admin provides justification/override reason?]
- **FR-022**: System MUST automatically unfeatured suspended/deactivated providers [NEEDS CLARIFICATION: Should system automatically re-feature providers when reactivated from suspended status, or require manual admin action?]

---

## Key Entities

- **Entity 1 - Provider**
  - **Key attributes**: provider_id (UUID), first_name, last_name, email (unique), phone, medical_license_number, specialty, years_experience, status (enum: draft, active, suspended, deactivated), featured (boolean), commission_type (enum: percentage, tier), commission_percentage (decimal, nullable), created_at, updated_at, created_by_admin_id
  - **Relationships**: One provider has many documents (one-to-many); one provider has one commission configuration (one-to-one if tier-based); one provider has many status history records (one-to-many); one provider has many audit log entries (one-to-many)

- **Entity 2 - Provider Document**
  - **Key attributes**: document_id (UUID), provider_id (foreign key), document_type (enum: medical_license, board_certification, malpractice_insurance), file_url (secure cloud storage URL), upload_date, expiration_date, verification_status (enum: pending, approved, rejected), verified_by_admin_id (nullable), verified_at (nullable), rejection_reason (text, nullable)
  - **Relationships**: Many documents belong to one provider (many-to-one); one document verified by one admin user (many-to-one)

- **Entity 3 - Clinic Information**
  - **Key attributes**: clinic_id (UUID), provider_id (foreign key), clinic_name, street_address, city, state_province, postal_code, country, clinic_phone, operating_hours (text)
  - **Relationships**: One clinic belongs to one provider (one-to-one); one provider has one clinic (one-to-one)

- **Entity 4 - Commission Tier (for tier-based commission only)**
  - **Key attributes**: tier_id (UUID), provider_id (foreign key), tier_name, procedure_count_min (integer), procedure_count_max (integer, nullable for open-ended top tier), commission_rate_percentage (decimal)
  - **Relationships**: Many tiers belong to one provider (many-to-one with provider if tier-based commission selected)

- **Entity 5 - Provider Status History**
  - **Key attributes**: history_id (UUID), provider_id (foreign key), previous_status (enum), new_status (enum), changed_at (timestamp), changed_by_admin_id (foreign key), reason (text, nullable but required for suspend/deactivate)
  - **Relationships**: Many status history records belong to one provider (many-to-one); one status change made by one admin (many-to-one)

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-11 | 1.0 | Initial PRD creation for FR-015 Provider Management (Admin-Initiated) | Claude (AI Assistant) |

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
