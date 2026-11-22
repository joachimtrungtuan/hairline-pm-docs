# FR-015 - Provider Management (Admin-Initiated)

**Module**: A-02: Provider Management & Onboarding
**Feature Branch**: `fr015-provider-management`
**Created**: 2025-11-11
**Version**: 1.26
**Status**: Revised 2026-11-22 (owner ruling: provider-status cancellation payment terms); previously revised 2026-11-20 (requirements graph programme baseline: owner rulings applied); previously revised 2026-10-28 (backend confirmations: seat usage member statuses, changed-fields-only saves, Owner login email change notice); previously revised 2026-10-27 (dev-team follow-up question resolution: save conflicts, data encryption, seat usage, impersonation, notification timing and recipients, cascade timing), pending consolidated verification; implementation reconciliation pending
**Source**: FR-015 from system-prd.md (§ FR-015: Provider Management (Admin-Initiated))

---

## Executive Summary

The Provider Management module enables administrators to onboard and manage hair transplant providers who will serve patients through the Hairline platform. This module is strictly admin-initiated—there is no self-service provider registration. Admins manually create provider accounts using a wizard-style interface, upload required documentation (for record-keeping), configure commission structures (Percentage or Flat Rate), and manage provider lifecycle status. The module also includes featured provider designation to control visibility in the patient-facing application. This module operates as the foundational gateway for the provider network, ensuring that all providers have valid profiles and agreed-upon commission terms before accepting bookings.

**Cross-Module Integration:** Providers can manage their own profile information (Bio, Languages, Awards, Logo) through **FR-032: Provider Dashboard Settings & Profile Management**. Changes made by providers in their dashboard automatically sync with the admin view, ensuring data consistency across platforms.

**Quote-model and lifecycle alignment:** One provider may submit multiple FR-004 Parent Quotes for one inquiry. Each parent contains package options that FR-005 resolves into patient-visible Subquotes; FR-006 books exactly one accepted Subquote. FR-015 manages provider eligibility, not quote/package editing. Provider suspension or deactivation automatically cancels that provider's unaccepted quotes and closes every non-terminal booking of that provider. A closed accepted booking enters the FR-006 provider-fault transfer, in which an admin moves the patient to a replacement provider within the same inquiry. Affected cases and inquiries are flagged for admin support. Current provider-profile and commission edits must not rewrite immutable accepted selections or historical booking commission snapshots.

**Note:** Document verification is performed externally; the system treats uploaded documents as pre-verified records and does not block account activation based on document status.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-02)**: Views featured provider listings (data consumed from A-02). **[P2 - Post-MVP]**: patient-facing display ships with FR-022 patient provider search; the admin featured flag and 10-provider cap are MVP. (REQ-015-046)
- **Provider Platform (PR-01, PR-06)**: Providers sign in via PR-01 (FR-009) and view their profile status and uploaded documents in PR-06 (FR-032). They read data managed by A-02 and edit the allowed fields via FR-032. **Fields must align with FR-032**.
- **Admin Platform (A-02)**: Full provider lifecycle management including creation, document upload (record-keeping), commission configuration, and status changes.
- **Shared Services (S-03, S-05, S-06)**: S-03 (Notification Service) for provider lifecycle emails; S-05 (Media Storage) for profile images and document storage; S-06 (Audit Log Service) for creation and status-change logs.

### Multi-Tenant Breakdown

**Patient Platform (P-02)**:

- Display featured providers in provider discovery/search interfaces **[P2 - Post-MVP, via FR-022 patient provider search]**.
- Show provider bio, languages, awards, and clinic location.

**Provider Platform (PR-01, PR-06)**:

- Providers view their own profile (synced with A-02). (REQ-015-047)
- Providers see uploaded documents (for reference). (REQ-015-047)
- Providers view configured commission rates (read-only) in the FR-032 Screen 4 Commission & Payout panel. (REQ-015-047)
- **Note**: Providers can edit profile fields (Bio, Languages, Awards, Profile Picture, Contact details) via **FR-032: Provider Dashboard Settings & Profile Management**, which updates the A-02 record. All editable fields must align between FR-015 and FR-032 to ensure consistency.

**Admin Platform (A-02)**:

- Create new provider accounts with complete profile setup (Wizard Flow).
- Upload provider documents (Medical License, etc.) for internal records.
- Configure commission structures (Percentage or Flat Rate).
- Manage provider status (Active, Suspended, Deactivated).
- Toggle featured provider designation.

**Shared Services (S-03, S-05, S-06)**:

- **S-03 (Notification Service)**: Sends welcome emails with login credentials.
- **S-05 (Media Storage Service)**: Stores uploaded provider documents and profile images.
- **S-06 (Audit Log Service)**: Logs creation and status changes.

### Communication Structure

**In Scope**:

- Email notifications to providers when account is created/activated.
- Notification to providers when their account is suspended/deactivated.
- Mandatory cancellation notifications to affected patients and support alerts to admins when provider status changes cancel cases. Patient messages must explain the provider-related cancellation and direct the patient to contact admins; the optional provider-email checkbox does not disable these notifications. (REQ-015-019)

**Out of Scope**:

- Document verification workflow (documents are for record-keeping only)
- "Save as Draft" functionality

### Entry Points

- **Admin-Initiated**: Admin accesses "Provider Management" section in Admin Platform dashboard → selects "Add New Provider" to initiate provider creation workflow (REQ-015-051)
- **Admin Oversight**: Admin opens "Providers" list view to see all providers across all statuses (active, suspended, deactivated) with filtering and search
- **Provider Profile Access (Provider-Side)**: Provider logs into Provider Platform → views account status (FR-032 Rule 6 banner when Suspended), uploaded documents (FR-032 Tab 6: Documents), and commission configuration read-only in FR-032 Screen 4: Billing Settings (Commission & Payout panel, Owner role only) (REQ-015-054)

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
   - Bio/Description (50-500 chars)
   - Seat Limit (default: 100, range 1-500, optional - can be adjusted later)
5. Admin enters professional details (Step 2):
   - Specialty (from the centrally managed Provider Specialties list, FR-026 Screen 5f)
   - Medical license number
   - Years of experience
   - Languages Spoken (at least 1 required)
   - Awards & Recognition (optional)
6. Admin enters clinic/practice information (Step 3):
   - Clinic name
   - Clinic address (street, city, state/province, postal code, country)
   - Clinic contact email (public, required)
   - Location city and country (public display, optional; pre-filled from the clinic address)
   - Contact phone (public, optional)
   - Website URL (optional)
   - Operating hours (optional)
7. Admin uploads required documents (Step 4):
   - Medical license (PDF, JPG, PNG, DOCX or XLSX file, required to complete the wizard)
   - Board certifications (same formats, optional)
   - Malpractice insurance certificate (same formats, optional)
   - Documents are stored for internal record-keeping only; their authenticity or status is never checked by the system and never gates activation
8. Admin configures commission structure (Step 5):
   - Selects commission model: "Percentage" or "Flat Rate"
   - Enters value (e.g., "15%" or "150"); for Flat Rate, selects the Flat Rate Currency (FR-029 enabled currency list; defaults to the system default currency)
   - Chooses the payout method ("Stripe Connect" or "Manual bank transfer"; required); the clinic completes Stripe's own sign-up itself, and creation does not wait for it
   - Sets commission start date (required; today or a future date); this is the configuration's FR-029 Effective Date for newly confirmed bookings
9. Admin reviews all entered information in summary view (Step 6).
10. Admin clicks "Create Provider" button.
11. System validates every field marked Required in the Screen 2 wizard tables (see Rule 2).
12. System creates provider record with status = "Active" and initializes provider credentials with `password_set = false`. Until the password is set, the provider is excluded from inquiry distribution (Rule 3). The admin sees the success message: "Provider [Clinic Name] created successfully. An activation email has been sent to [email]."
13. System sends the account activation email (FR-020 `provider.activation`; mandatory and cannot be disabled) to the provider with a secure one-time link to set the password (expires in 24 hours). The rest of its content is defined in the FR-030 notification catalogue.
14. Provider receives email and clicks "Set Password" link.
15. System displays password creation form (the password policy is in the system PRD, Platform-Wide Rules: Password and one-time-code policy).
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
21. Because `password_set = true` (step 17), the provider is now eligible for FR-003 inquiry distribution and can receive quote requests from patients.

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
  8. System sends new activation email (FR-020 `provider.activation`) to provider with fresh link.
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
  1. Admin enters fixed amount (e.g., 200) and selects its Flat Rate Currency (e.g., GBP).
  2. System saves configuration.
  3. Commission is calculated as a fixed deduction per completed procedure, regardless of procedure price.
- **Outcome**: Flat rate commission configured.

**A3: Admin Marks Provider as Featured**:

- **Trigger**: Admin wants to highlight a high-quality provider.
- **Steps**:
  1. Admin toggles "Featured Provider" switch (or uses the Provider-list "Set Featured" quick action).
  2. System verifies the provider is Active and fewer than 10 providers are featured (Rule 8), then updates `provider.featured = true`.
  3. Provider appears in "Featured" lists in Patient App once FR-022 patient provider search (P2 - Post-MVP) is delivered; in MVP the flag is stored and enforced but not yet displayed to patients.
- **Outcome**: Provider visibility boosted.

**A4: Admin Updates Provider Documents**:

- **Trigger**: Admin receives updated license/insurance from provider.
- **Steps**:
  1. Admin navigates to provider profile → "Documents" tab.
  2. Admin uploads the newly received file as a new admin-uploaded document (e.g., type "Medical License"). If the outdated file was itself admin-uploaded, the admin may use "Replace" on it instead; provider-uploaded files can only be replaced or deleted by the provider via FR-032.
  3. System stores the new file, archives any replaced file (soft delete), and logs the action in Tab 8.
  4. No approval workflow required; document is immediately available for record.
- **Outcome**: Document record updated.

**A5: Provider Suspension Cancels Cases and Requires Admin Support**:

- **Trigger**: An admin confirms suspension, or a previously scheduled suspension (or, for deactivation, scheduled deactivation) becomes effective.
- **Steps**:
  1. Before confirmation, show the affected provider's outstanding quotes and treatment cases, grouped by current FR-006 booking stage. Include `Accepted`, `Confirmed`, `In Progress`, and `Aftercare`, including FR-011 standalone aftercare cases assigned to this provider; exclude already terminal cases.
  2. When suspension becomes effective, set provider status to `Suspended` and block new inquiry allocations, quote submissions, patient acceptances, and further payment against affected selections. The status change itself authorizes the cancellation cascade; no separate case-by-case cancellation approval is required. The status change and its Provider Status Event (Key Entity 5) are written in one transaction. The cancellation cascade (steps 3 to 6) then runs as an idempotent background job, with a target completion within 5 minutes of the effective time. New activity is blocked immediately, because every eligibility check reads the current provider status (Rule 9). A reactivation does not stop a cascade that is still running for the earlier status event, and nothing that cascade cancels is restored.
  3. Cancel that provider's currently available unaccepted Parent Quotes once each with the FR-004 status `cancelled_provider_status`; their package/date alternatives become unavailable. Close every non-terminal booking of that provider before treatment starts (FR-006 booking stages `Accepted`, including unpaid within the payment hold, and `Confirmed`) through FR-006 Alternative Flow B4, which releases any active appointment hold or reservation and hands the booking to the provider-fault transfer in FR-006 Alternative Flow B5. A booking in the FR-006 `In Progress` stage is not closed: it stays `In Progress`, keeps its treatment record, and receives the provider-status cause and the support marker. An admin decides case by case through FR-006 Alternative Flow B7 on FR-006 Screen 6 whether to move the booking to `Aftercare` and reassign the aftercare provider (FR-006 Alternative Flow B6 then covers only that aftercare reassignment) or to cancel the booking with a mandatory reason; there is no replacement acceptance. On either route the admin sets the patient refund amount, from zero up to the full amount paid, with a mandatory reason and an audit entry, and the provider's payout for that booking is held until the admin decides (FR-006 Alternative Flow B7 payment terms). A booking in the FR-006 `Aftercare` stage is not closed: it keeps its status and treatment record, receives the provider-status cause and the support marker, and moves to the aftercare reassignment in FR-006 Alternative Flow B6, with no new acceptance and no new payment. An accepted Parent Quote keeps its `accepted` status and is never moved to a cancelled quote status. The FR-005 AcceptanceEvent and accepted snapshot stay unchanged and are superseded only through a linked FR-005 supersession record. FR-011 standalone aftercare cases assigned to this provider have no accepted Subquote; they are not cancelled either; they receive the same cause and support marker, and an admin reassigns them through the FR-011 aftercare reassignment screen. Accepted quote history belonging to Completed/already-terminal cases is not reclassified.
  4. Record `cancellationReason = ProviderSuspended` and `supportRequired = true` on affected cases and inquiry context. If the inquiry's accepted booking belongs to this provider, the inquiry is not cancelled; before treatment starts it stays open so that an admin can rehome the patient to a replacement provider in the same inquiry through FR-006 Alternative Flow B5, and for an `In Progress` booking it stays open for the admin decision described in step 3. If the inquiry is still comparing providers, cancel only the suspended provider's participation/quotes and flag the inquiry for support; unrelated providers' offers remain available.
  5. Notify affected patients that the provider is unavailable. A patient whose unaccepted offer was cancelled is told the offer is no longer available and is given a Contact Admin/Support action (FR-020 `provider.status_cancellation_patient`, used only before acceptance). A patient whose accepted booking was closed is told that an admin will arrange a replacement provider within the same inquiry (FR-020 `booking.provider_fault_replacement`). A patient whose `In Progress` or `Aftercare` booking stays open keeps the booking; when the admin reassigns aftercare, FR-011 sends the mandatory `aftercare.provider_reassigned` notice to the patient and the new aftercare provider (FR-020). Alert admins and make the affected records identifiable in the existing patient-management/support workflow.
  6. Record the provider status event, affected record identifiers, prior stages, cancellation reason, slot release, support marker, and notification outcomes in the audit trail. Repeated processing must not duplicate cancellations or support alerts for the same event/case.
  7. For each closed accepted booking, an admin opens Start Provider-Fault Transfer on FR-006 Screen 6 (which opens FR-006 Screen 10), selects a replacement provider in the same inquiry, and authors a replacement quote through FR-006 Alternative Flow B5; the confirmed selection is recorded as a new admin-authored acceptance record linked to the original; the patient re-enters nothing. Money follows the FR-006 Alternative Flow B5 payment terms: the patient is refunded in full everything paid, pays no cancellation fee, and the replacement booking takes a new payment; exact mechanics belong to the payment FRs. Clinical continuity and other patient assistance use the existing owning FRs. For each `In Progress` booking, an admin opens the booking on FR-006 Screen 6 and either moves it to `Aftercare` with an aftercare reassignment or cancels it with a mandatory reason (FR-006 Alternative Flow B7). For each Aftercare booking, an admin opens Reassign Aftercare on FR-006 Screen 6, which links to the FR-011 aftercare reassignment screen, and assigns another provider or the Hairline aftercare team with a mandatory reason, confirmation, and audit entry (FR-006 Alternative Flow B6). Cancelled cases and quotes are not automatically restored if the provider is later reactivated.
- **Outcome**: The suspended provider's unaccepted quotes are cancelled, its bookings before treatment starts are closed and handed to the FR-006 provider-fault transfer, its `In Progress` bookings stay open for an admin decision (move to Aftercare with reassignment, or cancel), its Aftercare bookings and FR-011 standalone aftercare cases move to admin aftercare reassignment, further payment to that provider is blocked, and affected patients/inquiries are marked for special admin support. Clinical documentation, completed-procedure facts, accepted snapshots, and payment history remain retained.
- **Boundary**: This admin-triggered suspension cascade is distinct from patient inquiry cancellation, normal payment-window expiry, and FR-010's provider-requested Cancel/Close Case flow. The replacement provider is chosen by an admin through FR-006 Alternative Flow B5, not selected automatically. This flow defines no refund or fund-release mechanics and does not erase completed care.
- **Deactivation**: Deactivation runs this same cascade with the same case scope (`Accepted`, `Confirmed`, `In Progress`, `Aftercare`, with In Progress cases kept open for an admin decision and Aftercare cases moving to aftercare reassignment as for suspension) using `cancellationReason = ProviderDeactivated`, and additionally disables provider login (see Screen 4). Records already cancelled by an earlier suspension keep `ProviderSuspended`.

**A6: Admin Reactivates a Suspended Provider**:

- **Trigger**: Admin decides a suspended provider may resume activity (e.g., policy violation resolved).
- **Steps**:
  1. Admin opens the provider profile (or the Provider-list "Reactivate" quick action) and clicks "Reactivate".
  2. System displays Screen 5: Provider Reactivation Modal with the current suspension reason and date.
  3. Admin enters a reason (min 20 chars), re-authenticates (password re-entry in MVP), and confirms.
  4. System sets status = Active, cancels any pending scheduled suspension or deactivation (the Screen 5 warning shows it before confirmation), records the status event and any cancelled scheduled change with the reason in the audit trail, and notifies the provider Owner by email (FR-020 `provider.reactivated`) if "Notify Provider" is checked.
- **Outcome**: Provider can receive new eligible inquiries and submit quotes, and no scheduled status change remains pending. Per Screen 4 Reactivation rules, cancelled cases/quotes, holds, payment windows, unresolved support markers, and the Featured flag are not restored.

**A7: Admin Processes a Provider Account-Closure Request**:

- **Trigger**: Provider submits an account-closure request from FR-032 (Settings → Account Settings → Request account closure), or contacts admin to close the account. There is no self-service deactivation. Admins are alerted by FR-020 `provider.closure_requested`, and the provider shows the Closure Requested marker in Screen 1.
- **Steps**:
  1. Admin opens the pending closure request (provider, reason, request date) from the provider profile.
  2. Admin clicks "Deactivate Provider", which opens Screen 4 with Deactivate selected and the reason pre-filled as "Provider requested account closure on [date]" (editable, min 20 chars).
  3. Admin chooses immediate or scheduled deactivation, re-authenticates, and confirms. "Notify Provider" is checked and locked, because FR-032 promised the provider an email once the account is deactivated.
  4. System applies the Screen 4 deactivation (immediately or on the Effective Date): status = Deactivated, standard cascade for non-terminal cases, patient and admin-support notifications, FR-017 payment reconciliation.
  5. When the deactivation takes effect, the system marks the FR-032 closure request Approved, links it to the deactivation status event, and logs both in Tab 8. If the admin scheduled the deactivation for a future Effective Date, the request stays Pending Admin Review until that date, and the Screen 1 marker reads "Closure requested, deactivation scheduled DD-MM-YYYY". If the scheduled deactivation is cancelled before it takes effect, the request stays Pending Admin Review, the marker returns to "Closure Requested", and no rejection email is sent.
  6. If the admin rejects the request instead (e.g., the provider withdraws it), the admin enters review notes (required, min 20 chars); the request is marked Rejected, the provider stays Active, the Closure Requested marker clears, and the provider receives the FR-020 `provider.closure_rejected` email with the review notes (mandatory).
- **Outcome**: The provider is Deactivated through the normal lifecycle with no separate "Deleted" status; data is retained per FR-023. Re-onboarding requires a new account (Rule 4).

---

## Screen Specifications

### Screen 1: Provider Management Dashboard

**Purpose**: Provides admins with comprehensive overview of all providers across all statuses with filtering, search, and quick actions

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------ | --- |
| Search Bar | text | No | Free-text search by provider name, clinic name, email, license number | Max 200 chars | no graph field (control) |
| Status Filter | multi-select dropdown | No | Filter providers by status (Active, Suspended, Deactivated) | Multiple selections allowed | ENT-provider.status |
| Featured Filter | checkbox | No | Filter to show only featured providers | Boolean toggle | ENT-provider.featured |
| Commission Type Filter | select | No | Filter by commission structure (Percentage, Flat Rate, All) | Single selection | ENT-commission-rate-config.commission_model |
| Closure Requested Filter | checkbox | No | Show only providers with a pending FR-032 account-closure request (status Pending Admin Review) | Boolean toggle | no graph field (control) |
| Date Range Filter | date range picker | No | Filter by provider creation date or Last Activity Date. Last Activity Date is system-derived: the most recent of the provider's last FR-004 Parent Quote submission and last FR-006 booking confirmation (empty if neither has occurred) | Valid date range required; providers with no Last Activity Date are excluded when filtering by it (REQ-015-093) | ENT-provider.created_at, ENT-provider.last_activity_date |
| Status Count Tiles | display | N/A | Counts of Active, Suspended, and Deactivated providers shown above the table (SC-012) | System calculated from provider status; counts all providers regardless of active filters; refresh with real-time status updates (REQ-015-094) | ENT-provider.status |
| Provider List Table | data table | N/A | Displays provider rows with columns: Name, Clinic, Status, Featured, Commission Rate, Created Date, Actions | Paginated (50 rows per page) | ENT-provider.name, ENT-provider-profile.clinic_name, ENT-provider.status, ENT-provider.featured, ENT-commission-rate-config.commission_model, ENT-commission-rate-config.commission_percentage, ENT-commission-rate-config.flat_rate_amount, ENT-commission-rate-config.flat_rate_currency, ENT-provider.created_at |

**Business Rules**:

- **Default View**: Dashboard displays all providers with status = "Active" by default on initial load (REQ-015-089)
- **Search**: Search queries match against provider name, clinic name, email, medical license number (case-insensitive) (REQ-015-089)
- **Status Badge Colors**: Active (green), Suspended (yellow), Deactivated (red) (REQ-015-095)
- **Featured Badge**: Gold star icon displayed next to provider name if featured = true (REQ-015-095)
- **Quick Actions**: Each row includes action buttons: "View Profile", "Edit", "Set Featured" (if active and not featured), "Unset Featured" (if featured), "Suspend" (if active), "Reactivate" (if suspended; opens Screen 5), "Deactivate" (if active/suspended), "Cancel Scheduled Change" (if a scheduled suspension/deactivation is pending) (REQ-015-090, REQ-015-122)
- **Closure Requested Marker**: Rows with a pending FR-032 account-closure request show a "Closure Requested — DD-MM-YYYY" badge (request date) next to the status badge, linking to the request in the provider profile (A7). While a deactivation scheduled from the request is pending, the badge reads "Closure requested, deactivation scheduled DD-MM-YYYY" (Effective Date). The marker clears when the request is Approved (the deactivation has taken effect) or Rejected (REQ-015-088, REQ-015-087)
- **Scheduled Change Marker**: Rows with a pending scheduled status change show "Scheduled: Suspend on DD-MM-YYYY" or "Scheduled: Deactivate on DD-MM-YYYY" next to the status badge
- **Sorting**: Table columns sortable by name (alphabetical), created date (chronological), and commission rate. Commission rate sorting groups by model: all Percentage providers first, ordered by percentage value, then all Flat Rate providers, ordered by Flat Rate Currency (ISO code) and then amount. Descending order reverses the value order within each group; amounts in different currencies are never compared. A provider on the FR-029 global default sorts by the default value, in the group of the default model (REQ-015-091)
- **Commission Rate Column**: Shows the provider's current effective commission. A provider on the FR-029 global default shows the default rate with "(Default)", for example "15% (Default)". A provider whose only provider-specific configuration is future-dated shows its current effective rate (the global default until the Effective Date) plus a "Scheduled" tag (REQ-015-092)
- **Pagination**: Display 50 providers per page, with page navigation controls (REQ-015-095)

**Notes**:

- Use color-coded status badges for quick visual scanning
- Featured providers should have prominent visual indicator (star icon)
- Ensure "Add New Provider" button prominently displayed in top-right corner
- Implement real-time status updates (e.g., if provider status changes, table refreshes without full page reload)

---

### Screen 2: Provider Creation Wizard

**Purpose**: Allows admins to create new provider accounts through a structured, multi-step wizard process. The wizard interface is used for creation; editing uses the tabbed interface (Screen 3).

**Cross-Module Alignment**: This screen's data structure aligns with **FR-032: Provider Dashboard Settings & Profile Management**. All profile fields (Bio, Languages, Awards, Profile Picture, Contact details) must stay synchronized between Admin (A-02) and Provider (PR-06) platforms. When providers edit these fields via FR-032, changes are immediately reflected in the admin view. Throughout this PRD, "immediately" and "real-time" for synchronization with FR-032 mean as soon as the sync completes, at most 1 minute (the same limit as the document sync rule).

**Wizard Steps**:

#### Step 1: Basic Information

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------ | --- |
| Profile Picture / Logo | file upload | No | Provider's photo or clinic logo (aligns with FR-032 Tab 1) | Max 5MB, JPEG/PNG, min 200x200px, recommended 500x500px | ENT-provider-profile.logo_url |
| Cover Image | file upload | No | Large banner image for clinic profile (aligns with FR-032 Tab 1) | Max 10MB, JPEG/PNG, recommended 1920x300px | ENT-provider-profile.cover_image_url |
| First Name | text | Yes | Provider's legal first name | Max 50 chars (REQ-015-096) | ENT-provider.first_name |
| Last Name | text | Yes | Provider's legal last name | Max 50 chars | ENT-provider.last_name |
| Email Address | email | Yes | Primary email (login ID) | Valid email; must satisfy the FR-009 global provider email identity rule (Rule 3, REQ-009-008): not used by another provider organization as Owner, team member, or pending invitation; Deactivated providers' emails are freed for reuse | ENT-provider.email |
| Phone Number | phone | Yes | Contact phone with country code | Valid format (REQ-015-129) | ENT-provider.phone |
| Bio / Description | textarea | Yes | Public-facing provider biography (aligns with FR-032 Tab 1 "About/Description") | Max 500 chars, min 50 chars (REQ-015-096) | ENT-provider.bio |
| Seat Limit | number | No | Maximum number of team members (staff) the provider can invite (aligns with FR-009 team management). Seat usage counts non-Owner team members with status Active or Suspended plus invitations with status Pending that are not past expiry; the Owner, Removed members, and Expired, Cancelled, or Accepted invitations do not count (FR-009 Rule 6, CR-FR009-20261028-01) | Integer, range 1-500, default: 100. Can be adjusted later by admin if provider requests increase | ENT-provider.seat_limit |

#### Step 2: Professional Details

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------ | --- |
| Specialty | select | Yes | Primary medical specialty | Values from the centrally managed Provider Specialties list (FR-026 Screen 5f); active values only (REQ-015-097) | ENT-provider.specialty |
| Medical License Number | text | Yes | License identifier (for record) | Max 50 chars | ENT-provider.medical_license_number |
| Years of Experience | number | Yes | Years practicing | Numeric, 0-60 | ENT-provider.years_experience |
| Languages Spoken | multi-select chip/pill | Yes | Languages spoken at clinic (aligns with FR-032 Tab 2) | At least 1 language required; consumes the central language catalog owned by FR-021 (Multi-Language & Localization) (REQ-015-098) | ENT-provider-profile.supported_languages |
| Awards & Recognition | dynamic list | No | List of awards (aligns with FR-032 Tab 4) | Each award: name (max 100 chars), issuer/organization (max 150 chars, optional), description (max 300 chars), year (1900-current), award image (max 2MB, JPEG/PNG) | ENT-provider.awards |

#### Step 3: Clinic Information

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------ | --- |
| Clinic Name | text | Yes | Name of practice/clinic (aligns with FR-032 Tab 1) | Min 3, max 200 chars | ENT-provider-profile.clinic_name |
| Clinic Address | address | Yes | Full physical address (admin-only record) | Google Places or manual entry | ENT-provider-profile.address_fields |
| Contact Email | email | Yes | Public clinic contact email shown on provider profile (aligns with FR-032 Tab 1 "Contact Email") | Valid email format; unique among Active and Suspended providers (Deactivated records ignored) | ENT-provider-profile.contact_email |
| Location - City | text | No | Public display city shown to patients (aligns with FR-032 Tab 1); pre-filled from Clinic Address and editable separately | Max 100 chars | ENT-provider-profile.city |
| Location - Country | dropdown | No | Public display country shown to patients (aligns with FR-032 Tab 1); pre-filled from Clinic Address and editable separately | Values from centrally managed country list (FR-026) | ENT-provider-profile.country |
| Contact Phone (Public) | phone | No | Public clinic phone number (aligns with FR-032 "Contact Phone (Public)") | Contains Country Code (dropdown, FR-026) and Number (numeric only, length validated per country code) (REQ-015-129) | ENT-provider-profile.public_phone |
| Website URL | url | No | Public-facing clinic website (aligns with FR-032 Tab 1) | Valid URL format (http/https); auto-prepends https:// if protocol missing | ENT-provider-profile.website_url |
| Operating Hours | text | No | e.g., "Mon-Fri 9am-5pm" | Free text | ENT-provider-profile.operating_hours |

#### Step 4: Documents (Record Keeping)

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------ | --- |
| Medical License | file upload | Yes | Copy of license (stored as document type "Medical License", uploaded by Admin) | PDF, JPG, PNG, DOCX, XLSX; Max 10MB (same as FR-032 Tab 6) | ENT-provider-document.document_type, ENT-provider-document.file_url |
| Board Certification | file upload | No | Copy of certification (type "Board Certification") | PDF, JPG, PNG, DOCX, XLSX; Max 10MB | ENT-provider-document.document_type, ENT-provider-document.file_url |
| Insurance Certificate | file upload | No | Proof of malpractice insurance (type "Malpractice Insurance") | PDF, JPG, PNG, DOCX, XLSX; Max 10MB | ENT-provider-document.document_type, ENT-provider-document.file_url |

*Note: The Medical License file is required to complete the wizard as a record-keeping baseline. Documents are pre-verified outside the system; the system never checks document authenticity or status, and later document changes never alter provider status.* (REQ-015-045)

#### Step 5: Commission & Settings

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------ | --- |
| Commission Model | radio | Yes | "Percentage" or "Flat Rate" | Default: Percentage | ENT-commission-rate-config.commission_model |
| Commission Value | number | Yes | % or Fixed Currency Amount | 0-100 with 0.1% precision (if %) or >0 in the Flat Rate Currency's minor units (if Flat), per FR-029 (REQ-015-100) | ENT-commission-rate-config.commission_percentage, ENT-commission-rate-config.flat_rate_amount |
| Flat Rate Currency | select | Conditional | Currency of the Flat Rate amount (aligns with FR-029 Screen 5 "Flat Rate Currency") | Required when Commission Model = Flat Rate; values from the FR-029 enabled currency list; defaults to the system default currency; hidden for Percentage | ENT-commission-rate-config.flat_rate_currency |
| Payout Method | radio | Yes | How the clinic's share is paid out, chosen by the admin: "Stripe Connect" or "Manual bank transfer". The clinic cannot choose it and completes Stripe's own sign-up itself; creation does not wait for payout readiness | One of: "Stripe Connect", "Manual bank transfer"; no preselected value | ENT-provider.payout_method |
| Commission Start Date | date | Yes | Effective date of this commission configuration for newly confirmed bookings; stored as the FR-029 provider-specific commission Effective Date (`effective_date`) | Format: DD-MM-YYYY; today (current UTC date) or a future date | ENT-commission-rate-config.effective_date |
| Featured Provider | toggle | No | Highlight in patient search | Default: Off; subject to the 10-provider cap (Rule 8) | ENT-provider.featured |

#### Step 6: Review & Create

- **Read-only Summary**: Displays all entered data for final review.
- **Actions**:
  - "Back": Navigate to previous steps.
  - "Create Provider": Finalizes creation and sets status to **Active**.

**Leaving the wizard**: The wizard does not save drafts. If the admin has entered any data and tries to leave the wizard before "Create Provider" succeeds (in-app navigation, browser Back, or closing/reloading the tab), the system shows the FR-032 unsaved-changes message text, "You have unsaved changes. Are you sure you want to leave?", with only "Stay" and "Leave" actions. The FR-032 Save option is not offered, because the wizard has no drafts. "Leave" discards all entered data; for tab close or reload the browser's native leave-page prompt is used. (REQ-015-099)

**Upload error messages**: Every admin file upload in this FR (wizard Steps 1, 2 and 4, the profile images and award images on the provider detail tabs, and the Tab 6 Upload Document modal and Replace) validates the file before saving it and shows one inline message under the field. The file is not saved. (REQ-015-064)
- Wrong format: "Unsupported file type. Allowed: {types}." ({types} is the field's list, e.g. "JPEG, PNG" or "PDF, JPG, PNG, DOCX, XLSX")
- Too large: "File is too large. Maximum size is {limit} MB." ({limit}: Profile Picture / Logo 5, Cover Image 10, award image 2, documents 10)
- Below the minimum dimensions (Profile Picture / Logo only): "Image is too small. Minimum size is 200 × 200 pixels."

The English text is the source copy; other languages follow the normal translation process.

---

### Screen 3: Provider Profile Details (Tabbed View)

**Purpose**: Comprehensive view of a provider's account, organized by tabs for manageability. This view is used for editing existing provider records.

**Cross-Module Alignment**: Tab structure and field definitions align with **FR-032: Provider Dashboard Settings & Profile Management** to ensure consistency between admin and provider views. Screen 3 includes all 6 tabs from FR-032 (Basic Information, Languages, Staff List, Awards, Reviews, Documents) plus additional admin-only tabs (Commission & Financials, Activity Log).

**Header Area**:

- **Provider Name / Status Badge** (Active/Suspended/etc.)
- **Quick Actions**:
  - "Edit Profile" (opens all tabs in edit mode) (REQ-015-122)
  - "Resend Activation Email" (requires the FR-031 Edit Providers permission; visible only if password not yet set and status = Active, so it is hidden for Suspended and Deactivated providers, matching Alternative Flow A1; sends new one-time password setup link) (REQ-015-058)
  - "Suspend/Deactivate" (status management; opens Screen 4)
  - "Reactivate" (visible only if Suspended; opens Screen 5)
  - "Cancel Scheduled Change" (visible only if a scheduled suspension/deactivation is pending; see Screen 4)
  - "Login as Provider" (Super Admin only, for support/debugging; available when the provider is Active or Suspended, not when Deactivated)

**Login as Provider rules**:

- Login as Provider is allowed when the provider is Active or Suspended. It is blocked when the provider is Deactivated, with the message: "Login as Provider is not available for a deactivated provider." These rules apply both to impersonating the Owner and to impersonating a team member (FR-009 REQ-009-023). (REQ-015-121)
- During a session for a Suspended provider, the admin is limited to the same read-only rules as the provider (FR-032 Rule 6); the write actions allowed below apply only to an Active provider.
- Before starting, the Super Admin must enter a reason (min 20 chars) and re-authenticate (password re-entry in MVP; MFA once the FR-026 / FR-031 MFA stack is delivered).
- The impersonated Provider Platform session shows a persistent banner: "You are viewing as [Provider Name] — admin session by [Admin Name]" with an "End Session" action.
- While impersonating, the admin cannot change the provider's password or login email, and cannot change payout/bank or financial settings.
- Session start (with reason), end, and every write action performed during the session are logged in Tab 8: Activity Log, attributed to the admin user acting as the provider.
- The impersonation session opens in a new browser tab; the admin's own Admin Platform tab stays open.
- The impersonation session ends when the admin clicks "End Session" or automatically after the standard 30-minute admin inactivity timeout. There is no absolute session cap.

**Tabs**:

#### Tab 1: Basic Information (Profile Overview)

**Purpose**: Display and edit core clinic profile information. Mirrors FR-032 Tab 1 structure with additional admin-only settings.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Admin/Provider Editable | Graph field |
|------------|------|----------|-------------|------------------|------------------------ | --- |
| Profile Picture / Logo | image upload | No | Clinic branding image | Max 5MB, JPEG/PNG, min 200x200px, recommended 500x500px | Both (Provider via FR-032) | ENT-provider-profile.logo_url |
| Cover Image | image upload | No | Large banner image for clinic profile | Max 10MB, JPEG/PNG, recommended 1920x300px | Both (Provider via FR-032) | ENT-provider-profile.cover_image_url |
| First Name | text | Yes | Provider's legal first name | Max 50 chars | Admin only | ENT-provider.first_name |
| Last Name | text | Yes | Provider's legal last name | Max 50 chars | Admin only | ENT-provider.last_name |
| Email Address | email | Yes | Primary email (login ID) | Valid email; must satisfy the FR-009 global provider email identity rule (Rule 3, REQ-009-008) (re-checked whenever changed); Deactivated providers' emails are freed for reuse | Admin only | ENT-provider.email |
| Phone Number | phone | Yes | Primary contact phone | Valid format with country code | Admin only | ENT-provider.phone |
| Bio / Description | textarea | Yes | Public-facing provider biography | Max 500 chars, min 50 chars | Both (Provider via FR-032) | ENT-provider.bio |
| Specialty | select | Yes | Primary medical specialty | Values from the centrally managed Provider Specialties list (FR-026 Screen 5f); a stored value later deactivated in FR-026 still displays but cannot be newly selected | Admin only | ENT-provider.specialty |
| Medical License Number | text | Yes | License identifier (for record) | Max 50 chars | Admin only | ENT-provider.medical_license_number |
| Years of Experience | number | Yes | Years practicing | Numeric, 0-60 | Admin only | ENT-provider.years_experience |
| Clinic Name | text | Yes | Name of practice/clinic | Min 3, max 200 chars | Both (Provider via FR-032) | ENT-provider-profile.clinic_name |
| Clinic Address | address | Yes | Full physical address | Google Places or manual entry | Admin only | ENT-provider-profile.address_fields |
| Location - City | text | No | City where clinic is located | Max 100 chars | Both (Provider via FR-032) | ENT-provider-profile.city |
| Location - Country | dropdown | No | Country where clinic is located | Values from FR-026 country list | Both (Provider via FR-032) | ENT-provider-profile.country |
| Contact Phone (Public) | phone | No | Public clinic phone number | Country Code dropdown + Number | Both (Provider via FR-032) | ENT-provider-profile.public_phone |
| Contact Email | email | Yes | Public clinic contact email (captured in Screen 2 Step 3) | Valid email format; unique among Active and Suspended providers, Deactivated records ignored (re-checked whenever changed, per FR-032) | Both (Provider via FR-032) | ENT-provider-profile.contact_email |
| Website URL | url | No | Public-facing clinic website | Valid URL, auto-prepends https:// | Both (Provider via FR-032) | ENT-provider-profile.website_url |
| Operating Hours | text | No | Operating hours (e.g., "Mon-Fri 9am-5pm") | Free text | Admin only | ENT-provider-profile.operating_hours |
| Seat Limit | number | No | Maximum team members (staff) capacity. Seat usage counts non-Owner team members with status Active or Suspended plus invitations with status Pending that are not past expiry; the Owner, Removed members, and Expired, Cancelled, or Accepted invitations do not count (FR-009 Rule 6, CR-FR009-20261028-01) | Integer, range 1-500, default 100 | Admin only | ENT-provider.seat_limit |
| Commission Summary | display | N/A | Read-only summary of the current commission configuration (model, value, Flat Rate Currency when applicable, Effective Date), with a "Manage in Commission & Financials" link to Tab 7. A provider on the FR-029 global default shows the default rate with "(Default)", for example "15% (Default)"; a provider whose only provider-specific configuration is future-dated shows its current effective rate plus a "Scheduled" tag | Retrieved from Tab 7 (FR-029 provider-specific configuration or global default); not editable in this tab | Read-only | ENT-commission-rate-config.commission_model, ENT-commission-rate-config.commission_percentage, ENT-commission-rate-config.flat_rate_amount, ENT-commission-rate-config.flat_rate_currency, ENT-commission-rate-config.effective_date |
| Featured Provider | toggle | No | Admin-only control, positioned at the bottom of Basic Information, to highlight in patient search | Boolean, default: Off; maximum 10 featured providers; only for Active providers; cleared automatically on suspension or deactivation (Rule 6) | Admin only | ENT-provider.featured |
| Status | badge/display | Yes | Provider account status | Enum: Active, Suspended, Deactivated | Admin only | ENT-provider.status |
| Completed Procedures | display | No | Count of distinct procedures that reached FR-010 treatment completion for this provider | One count per completed procedure, not per Parent Quote, option, date alternative, or installment | Read-only | ENT-provider.completed_procedures_count |
| Average Rating | display | No | Average rating from patient reviews | Read-only, format: X.X/5.0 stars | Read-only | ENT-provider-review-summary.average_rating |
| Starting Price | display | N/A | Calculated, not typed in: the lowest standard price among the provider's active packages (FR-024), converted to the patient's currency | Read-only; changes when the provider's active packages or their standard prices change | Read-only | ENT-provider.starting_price |

**Business Rules**:

- Fields marked "Both" can be edited by provider via FR-032 and changes sync to admin view in real-time (REQ-015-123)
- Fields marked "Admin only" can only be edited by admin users with provider management permissions (REQ-015-039)
- Profile changes logged in audit trail with timestamp, user, and changed fields (REQ-015-038)
- **Changed fields only**: An admin save (FR-015) or provider save (FR-032) applies only the fields the user changed; untouched fields are not rewritten. Last save wins only when two people change the same field. There is no conflict check and no conflict message. (REQ-015-112)
- **Admin change reason**: When an admin saves changes to any provider data (Tabs 1, 2, 4, 6 notes, and 7), the system requires a "Reason for change" (min 10 chars, max 500 chars) before saving. The reason is stored with the audit entry and shown in Tab 8. Provider self-edits via FR-032 do not require a reason. Exception: the Featured Provider toggle (and the Provider-list Set/Unset Featured quick actions) never asks for a reason; the change is still logged in Tab 8.
- Current profile edits must not alter an FR-005 accepted snapshot, historical appointment/price/package context, or an FR-006 booking commission snapshot. This does not prevent normal current-profile synchronization with FR-032. (REQ-015-113)
- Completed Procedures uses the FR-010 treatment-completion milestone, not acceptance, payment confirmation, or final aftercare completion. Cancellation during Aftercare must not erase an already recorded completed procedure; no new procedure-completion rule is introduced here.
- Commission is edited only in Tab 7; Tab 1 shows it read-only.
- **Owner login email change**: Changing the Email Address (the Owner's login ID) requires admin password re-authentication and a reason (the admin change reason above). The new address is validated against the FR-009 global provider email identity rule (REQ-015-014) before saving. The Owner does not confirm the new address. On save, the system: (REQ-015-114)
  - sends FR-020 `provider.login_email_changed` (mandatory security notice) to the old address, saying the login email was changed to the new address (partly masked) by a Hairline admin, with the date and time and a prompt to contact support if unexpected, and to the new address, saying it is now the login email for the clinic;
  - signs the Owner out of all sessions and revokes the Owner's tokens;
  - if `password_set` is false, invalidates the pending activation link and sends a new activation email (FR-020 `provider.activation`) to the new address.
- Seat Limit changes require admin re-authentication for security. In MVP this is implemented as password re-entry; once the shared MFA stack from FR-026 / FR-031 is delivered, these actions MUST use MFA-based re-authentication and any MFA references in this FR are to be understood as future (non-MVP) behavior. (REQ-015-111)

**Notes**:

- Admin view includes all provider profile fields plus admin-only settings (Seat Limit, Status) and a read-only Commission Summary
- Provider-editable fields sync bidirectionally with FR-032
- Admin can override any provider changes if needed (logged in audit trail)

---

#### Tab 2: Languages

**Purpose**: View and manage languages spoken at the clinic. Mirrors FR-032 Tab 2 structure.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Admin/Provider Editable | Graph field |
|------------|------|----------|-------------|------------------|------------------------ | --- |
| Supported Languages | chip/pill list | Yes | Languages spoken at clinic | At least 1 language required; consumes the central language catalog owned by FR-021 (Multi-Language & Localization) | Both (Provider via FR-032) | ENT-provider-profile.supported_languages |

**Business Rules**:

- Languages displayed as removable chips/pills with X button on each chip
- Admin can add/remove languages; provider can also manage via FR-032 Tab 2
- At least 1 language must be selected (validation prevents removing last language); attempting to save with none shows: "At least one language is required." (REQ-015-098)
- Changes logged in audit trail with timestamp and user
- Language list consumed from the FR-021 central language catalog; chips mean languages spoken at the clinic, not UI language

**Notes**:

- Admin view identical to FR-032 Tab 2 (same interface, same functionality)
- Changes made by provider in FR-032 reflect immediately in admin view
- Drag-and-drop reordering supported to prioritize languages (REQ-015-130)

---

#### Tab 3: Staff List

**Purpose**: View and manage this provider's clinic staff members and team roles (admin view), including inviting new staff.

**Implementation**: This tab embeds **FR-009: Provider Team & Roles Management > Screen 12: Provider Team (Admin, Single Provider)**, filtered to this provider only. Team members of other providers are never shown here; the cross-provider directory remains FR-009 Screen 10.

**Business Rules**:

- Lists this provider's team members with name, email, role, ownership flag, status, and last login (fields and actions per FR-009).
- "Invite Staff Member": admin enters an email and selects one of the provider's existing roles (not Owner); the invitation uses FR-009's normal invitation email, acceptance, and expiry flow. (REQ-015-116)
- Invite is blocked when the provider's Seat Limit (Rule 7) is reached and when provider status is Suspended or Deactivated. (REQ-015-116)
- Requires the FR-031 "Edit Providers" permission; the invite and the inviting admin are logged in FR-009's audit trail and Tab 8. (REQ-015-069)
- Existing FR-009 admin actions (force suspend member, reset invitation, view audit log, impersonate) remain available.

---

#### Tab 4: Awards

**Purpose**: View and manage clinic awards, certifications, and recognitions. Mirrors FR-032 Tab 4 structure.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Admin/Provider Editable | Graph field |
|------------|------|----------|-------------|------------------|------------------------ | --- |
| Awards List | card/list | No | Clinic awards, certifications, recognitions | Each award: name (max 100 chars), issuer/organization (max 150 chars, optional), description (max 300 chars), year (1900-current year), award image (max 2MB, JPEG/PNG) | Both (Provider via FR-032) | ENT-provider.awards |

**Business Rules**:

- Awards displayed as cards with: award image thumbnail, name, issuer, year, description
- Admin can add/edit/delete awards; provider can also manage via FR-032 Tab 4
- Awards support drag-and-drop reordering to prioritize most important awards (REQ-015-131)
- Award image upload supports drag-and-drop; max 2MB, JPEG/PNG only (REQ-015-131)
- Changes logged in audit trail with timestamp and user

**Notes**:

- Admin view identical to FR-032 Tab 4 (same interface, same functionality)
- Changes made by provider in FR-032 reflect immediately in admin view
- Empty state: "No awards added yet. Click '+ Add Award' to showcase achievements."

---

#### Tab 5: Reviews

**Purpose**: Browse this provider's reviews with filtering and sorting, and launch FR-013 admin review management actions (insert authenticated off-platform reviews, edit, remove) for this provider. Display mirrors FR-032 Tab 5; review management behavior is owned by **FR-013: Reviews & Ratings**.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Admin/Provider Editable | Graph field |
|------------|------|----------|-------------|------------------|------------------------ | --- |
| Overall Rating Summary | display | No | Average rating and total review count | Read-only; calculated from Reviews service | Read-only | ENT-provider-review-summary.average_rating, ENT-provider-review-summary.review_count |
| Rating Distribution | bar chart | No | Percentage/count visualization for 5★ through 1★ reviews | Read-only; calculated from Reviews service | Read-only | no graph field (display) |
| Review List | list | No | List of individual patient reviews with rating, comment, date, patient name | Read-only; sourced from Reviews service | Read-only | no graph field (display) |
| Rating Filters | checkbox/pill | No | Filter reviews by rating (5★, 4★, 3★, 2★, 1★) | Multiple selections allowed | Interactive filter | no graph field (control) |
| Add Review Button | button | No | Opens FR-013 Screen 8 (Admin – Review Detail, Insert & Edit) in insert mode, pre-scoped to this provider, to add an authenticated off-platform review | Admin users with review management permission | Admin only | no graph field (control) |
| Review Actions | button group | No | Per review: "Edit" or "Remove" opens FR-013 Screen 8 for that review | Rules, validation, and audit owned by FR-013 | Admin only | no graph field (control) |

**Business Rules**:

- Reviews displayed with: star rating, patient name (anonymized if requested), date, review text
- Admin can filter by rating, search by keyword, sort by date/rating
- Admin insert, edit, and remove actions follow FR-013 (including the "Verified Off-platform" label, verification source/date, and audit trail); FR-015 does not define its own review editing rules (REQ-015-117)
- Providers cannot edit or delete reviews; they can only respond via FR-013 Screen 6
- Review data sourced from Reviews service (FR-013)

**Notes**:

- Review display matches FR-032 Tab 5; admin-only actions are added on top
- Reviews help admin assess provider quality and patient satisfaction
- Seeding reviews for newly onboarded providers is a client requirement (Admin Platform transcription); the full admin list is FR-013 Screen 7

---

#### Tab 6: Documents

**Purpose**: View and manage provider documents (license, certification, insurance) for oversight and record-keeping. Providers manage their own documents via FR-032; admins can view all documents and upload additional documents received via external channels (email, postal mail, in-person).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Admin/Provider Editable | Graph field |
|------------|------|----------|-------------|------------------|------------------------ | --- |
| Upload Document Button | button | No | Admin action to upload additional documents | Opens the Upload Document modal (fields below) | Admin only | no graph field (control) |
| Document List | list/cards | No | List of all provider and admin-uploaded documents | Displays: document name, type, upload date, file size, uploaded by (Provider/Admin) | View-only for admin; sortable/filterable (REQ-015-132) | ENT-provider-document.document_name, ENT-provider-document.document_type, ENT-provider-document.uploaded_at, ENT-provider-document.file_size, ENT-provider-document.uploaded_by |
| Document Name | text (display) | N/A | Filename of uploaded document | Auto-generated from file; max 200 chars | Display only | ENT-provider-document.document_name |
| Document Type | badge (display) | N/A | Type of document | Enum: Medical License, Board Certification, Insurance (general), Malpractice Insurance, Business License, Other | Display only (REQ-015-063) | ENT-provider-document.document_type |
| Upload Date | datetime (display) | N/A | When document was uploaded | Auto-generated timestamp; format: "MMM DD, YYYY HH:mm" | Display only | ENT-provider-document.uploaded_at |
| Uploaded By | badge (display) | N/A | Who uploaded document: "Provider" or "Admin [Name]" | Badge displays "Provider" for provider uploads, "Admin - [admin name]" for admin uploads | Display only | ENT-provider-document.uploaded_by |
| File Size | text (display) | N/A | Document file size | Format: "X.X MB" or "X KB" | Display only | ENT-provider-document.file_size |
| Notes | text (display/edit) | No | Optional notes about document | Max 500 chars; admin can add/edit notes | Admin editable (via "Edit Notes" action) | ENT-provider-document.notes |
| Actions | button group | No | View, Download, Replace, Delete actions | Context menu or action buttons per document | Admin only (view/download/replace/delete) | no graph field (control) |

**Upload Document Modal Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------ | --- |
| File | file upload | Yes | Document file received from the provider via an external channel | Formats: PDF, JPG, PNG, DOCX, XLSX; max 10MB | ENT-provider-document.file_url |
| Document Type | dropdown | Yes | Type of document (admin selects) | Enum: Medical License, Board Certification, Insurance (general), Malpractice Insurance, Business License, Other (REQ-015-063) | ENT-provider-document.document_type |
| Notes | textarea | No | Optional notes about the document | Max 500 chars | ENT-provider-document.notes |

On save, Document Name, File Size, Upload Date, and Uploaded By ("Admin - [admin name]") are set by the system.

**Business Rules**:

- **Provider Document Management**: Providers upload, replace, delete their documents via **FR-032 Tab 6: Documents**. Provider-uploaded documents sync to FR-015 within 1 minute (REQ-015-061)
- **Admin Oversight**: Admins can view all provider-uploaded documents for compliance and oversight purposes
- **Admin Additional Uploads**: Admins can upload additional documents received externally (e.g., documents sent via email, postal mail, scanned at in-person meeting). These admin-uploaded documents display "Admin - [admin name]" badge
- **Document Permissions**:
  - Provider-uploaded documents: Admin can view, download, add notes, but **cannot replace or delete** (only provider can via FR-032) (REQ-015-059)
  - Admin-uploaded documents: Admin has full control (view, download, replace, delete, add notes) (REQ-015-059)
  - **Replace**: Replacing a document uploads the new file as the current version and archives the old file (soft-deleted and retained per the Soft Delete rule, logged in Tab 8). Replace does not require an admin change reason
- **Document Requirements**: A Medical License file is required once, when completing the Screen 2 wizard. After creation, the absence, replacement, or deletion of any document never changes provider status or blocks activity (REQ-015-045)
- **Audit Logging**: All document actions (upload/view/download/replace/delete/note edits) logged in Tab 8: Activity Log with timestamp, user (admin/provider), action type, and IP address (REQ-015-062)
- **Soft Delete**: Deleted documents (by provider or admin) retained in archive for compliance; visible in Activity Log but not in main document list (REQ-015-060)
- **File Validation**: Same as FR-032 - Accepted formats: PDF, JPG, PNG, DOCX, XLSX; Max 10MB per file
- **Sort/Filter Options**: (REQ-015-132)
  - Sort by: Upload Date (newest first - default), Document Type, Uploaded By (REQ-015-132)
  - Filter by: Document Type, Uploaded By (Provider/Admin) (REQ-015-132)

**Notes**:

- **Primary Document Management**: Providers manage their documents via FR-032 Tab 6; admins use FR-015 Tab 6 for oversight and supplementary uploads
- **Use Case for Admin Uploads**: Admin receives provider's license via email → Admin uploads to FR-015 Tab 6 → Document visible to provider in FR-032 with "Admin" badge
- **Document Sync**: Provider uploads in FR-032 → Syncs to FR-015 within 1 minute. Admin uploads in FR-015 → Syncs to FR-032 within 1 minute (REQ-015-061)
- **Empty State**: If no documents uploaded yet, display message: "No documents on file yet. Provider can upload documents via their dashboard, or you can upload documents received externally."
- **Document Verification**: Performed externally; system treats all documents as pre-verified records
- Document cards/rows display icon based on file type (PDF icon, image icon, doc icon) and "Uploaded By" badge (green for Provider, blue for Admin)

---

#### Tab 7: Commission & Financials (Admin-Only)

**Purpose**: View and manage commission configuration and financial history. This tab is admin-only and not visible in FR-032.

**Scope**: This tab covers provider commission and payout configuration only. The same amount-or-percentage pattern applies to affiliates in FR-018 (Percentage or Fixed Amount, monthly-only payout per the client), not here.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Admin/Provider Editable | Graph field |
|------------|------|----------|-------------|------------------|------------------------ | --- |
| Commission Model | radio (display/edit) | Yes | "Percentage" or "Flat Rate" | Default: Percentage | Admin only (edit) | ENT-commission-rate-config.commission_model |
| Commission Value | number (display/edit) | Yes | % or Fixed Currency Amount | 0-100 with 0.1% precision (if %) or >0 in the Flat Rate Currency's minor units (if Flat), per FR-029 | Admin only (edit) (REQ-015-100) | ENT-commission-rate-config.commission_percentage, ENT-commission-rate-config.flat_rate_amount |
| Payout Method | radio (display/edit) | Yes | How this clinic's share is paid out: "Stripe Connect" or "Manual bank transfer" (set in Screen 2 Step 5). The clinic sees it read-only | One of: "Stripe Connect", "Manual bank transfer" | Admin only (edit); the clinic asks Hairline for a change | ENT-provider.payout_method |
| Payout Readiness | display | N/A | The state of the clinic's own Stripe payout setup, one of four states: Not started, In progress, Ready, Restricted; shown for Stripe Connect clinics. The clinic completes the Stripe sign-up itself and sees the same status read-only | Read-only | Display only (REQ-015-135) | no graph field (display) |
| Flat Rate Currency | select (display/edit) | Conditional | Currency of the Flat Rate amount (aligns with FR-029 Screen 5) | Required when Commission Model = Flat Rate; FR-029 enabled currency list; defaults to the system default currency | Admin only (edit) | ENT-commission-rate-config.flat_rate_currency |
| Commission Start Date / Effective Date | date (display/edit) | Yes | Date from which the commission configuration applies to newly confirmed bookings (FR-029 `effective_date`). First set in Screen 2 Step 5; every later model, value, or currency edit sets its own Effective Date | Format: DD-MM-YYYY; today or a future date, where "today" is the current UTC date | Admin only (edit, with change reason) | ENT-commission-rate-config.effective_date |
| Featured Provider | display | N/A | Current featured status; managed from the Provider-list quick action or the Basic Information toggle | Read-only | Display only | ENT-provider.featured |
| Current Configuration | display | N/A | Summary of commission configuration applicable to newly confirmed bookings | Examples: "15%" or "£200 per completed procedure"; indicate that existing bookings retain their confirmation-time snapshot | Display only | ENT-commission-rate-config.commission_model, ENT-commission-rate-config.commission_percentage, ENT-commission-rate-config.flat_rate_amount, ENT-commission-rate-config.flat_rate_currency |
| Scheduled Configuration | display | N/A | The pending future-dated commission configuration (model, value, Flat Rate Currency, Effective Date), if one exists, with a "Cancel Scheduled Configuration" action | Hidden when none is pending; at most one per provider; cancellation requires a change reason and re-authentication | Display only (cancel: Admin only) | ENT-commission-rate-config.commission_model, ENT-commission-rate-config.commission_percentage, ENT-commission-rate-config.flat_rate_amount, ENT-commission-rate-config.flat_rate_currency, ENT-commission-rate-config.effective_date |
| Commission History | list | No | Audit log of past commission and payout setting changes | Each entry: date, admin user, old value, new value, reason | Display only | no graph field (display) |

**Business Rules**:

- Commission configuration displayed prominently with current model and value
- **Edit eligibility**: Commission settings can be edited for Active and Suspended providers (so terms can be fixed before reactivation). For Deactivated providers Tab 7 is read-only; history stays visible. FR-029 Screen 5 applies the same rule (CR-FR029-20261015-02). When a deactivation takes effect, the system automatically cancels any pending Scheduled Configuration and logs the cancellation in Commission History (REQ-015-102)
- Admin can edit commission settings (requires re-authentication). In MVP this is implemented as password re-entry; once the shared MFA stack from FR-026 / FR-031 is delivered, these actions MUST use MFA-based re-authentication and any MFA references in this FR are to be understood as future (non-MVP) behavior. (REQ-015-110)
- FR-029 / A-09 owns the central commission-settings screen (global default + provider-specific commission scopes) and the booking-time snapshot policy; this tab remains the single-provider management surface for provider-specific commission configuration (REQ-015-108)
- Commission edits apply to bookings confirmed after the configuration becomes effective, not to every later payment transaction. Resolve the effective provider-specific configuration (or global default) and snapshot its model/value (and Flat Rate currency) at FR-006 booking confirmation under FR-029. Until a new configuration's Effective Date, the previous configuration remains effective. Existing confirmed bookings retain that snapshot for subsequent installments, deductions, and payout reconciliation. (REQ-015-109)
- Patient price/currency/exchange-rate context is locked at FR-005 acceptance; commission is locked at booking confirmation; nothing is fixed at quote creation. An accepted-but-unpaid selection has not yet fixed its commission snapshot. The Percentage and Flat Rate models remain unchanged; a flat fee remains one deduction per completed procedure, not one per package, Subquote, or installment.
- **Scheduled configuration**: "Today" means the current UTC date (the same calendar used by the midnight UTC jobs). An edit with an Effective Date of today applies immediately to newly confirmed bookings. An edit with a future Effective Date is stored as the provider's Scheduled Configuration; at most one may be pending per provider. Saving another future-dated edit replaces the pending one (the replacement is logged in Commission History with both values). On its Effective Date the scheduled configuration becomes the current configuration automatically. The pending configuration is shown read-only to the provider in the FR-032 Screen 4 Commission & Payout panel. (REQ-015-103)
- **Payout method**: Only an admin sets or changes the clinic's payout method (Payout Method Rule); the clinic sees the method and its payout readiness read-only and completes Stripe's own sign-up itself. Clinic activation does not wait for payout readiness, and a share due to move while the clinic is not Ready stays with Hairline until it is Ready (Payout Readiness Rule)
- Changes made to provider-specific commission values here MUST stay synchronized with the provider-specific commission data shown in FR-029 Screen 5 for the same provider (REQ-015-107)
- **Shared FR-029 scopes**: A provider belongs to at most one active provider-specific commission scope. If this provider is currently covered by an FR-029 scope shared with other providers, saving a commission edit here removes this provider from that shared scope and creates a single-provider scope for it with the new values; the other providers in the shared scope are unchanged. The tab warns the admin before saving, and the split is logged in Commission History and the FR-029 audit trail. (REQ-015-104)
- All changes to commission and payout settings logged in history with timestamp, admin user, old/new values (REQ-015-106)
- Provider can view commission model, value, Flat Rate Currency, and Effective Date read-only in the FR-032 Screen 4 Commission & Payout panel (but not edit); the provider also sees its payout method and payout readiness read-only in its own dashboard (FR-032)

**Notes**:

- This tab is admin-only; provider sees commission rate read-only in the FR-032 Screen 4 Commission & Payout panel
- Commission and payout setting changes require admin justification (logged in audit trail)
- Use FR-015 when the admin is working provider-by-provider; use FR-029 for central or bulk commission-scope administration

---

#### Tab 8: Activity Log (Admin-Only)

**Purpose**: View chronological audit trail of all provider account actions. This tab is admin-only and not visible in FR-032.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Admin/Provider Editable | Graph field |
|------------|------|----------|-------------|------------------|------------------------ | --- |
| Activity Log List | list | No | Chronological list of account actions | Each entry: timestamp, user (admin or provider), action type, changed fields, IP address | Read-only | ENT-provider-activity-log-entry.occurred_at, ENT-provider-activity-log-entry.user_id, ENT-provider-activity-log-entry.action_type, ENT-provider-activity-log-entry.changed_fields, ENT-provider-activity-log-entry.ip_address, ENT-provider-activity-log-entry.reason |

**Business Rules**:

- Activity log displays all actions: profile edits, status changes, document uploads, logins, commission changes (REQ-015-118)
- Each log entry includes: timestamp, user (admin or provider via FR-032), action type, changed fields, IP address (REQ-015-118)
- Logs are immutable (cannot be edited or deleted)
- Suspension/deactivation entries must link the affected case/inquiry references, prior stages, cancellation causes, support markers, slot-release results, and notification outcomes. Display `Admin Support Required` for unresolved provider-caused cancellations with a link to the existing FR-016 patient intervention/support context; do not add a case-management editor to this tab. (REQ-015-119)
- Admin can filter by action type, date range, user
- Admin can export the activity log for compliance reporting as a CSV file of the rows matching the current filters. Export is available to every admin who can view Tab 8 (FR-031 View Providers). IP addresses are included unmasked. The export action itself is logged in Tab 8 (REQ-015-120)

**Notes**:

- This tab is admin-only and provides full transparency of provider account changes
- Logs help with compliance, security investigations, and dispute resolution

---

### Screen 4: Provider Suspension/Deactivation Modal

**Purpose**: Captures the admin reason and affected-case impact before suspending/deactivating a provider, with accountable cancellation and patient/admin support handoffs

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------ | --- |
| Action Type | text (display only) | N/A | Shows "Suspend Provider" or "Deactivate Provider" as modal title | Display only | ENT-pending-provider-status-change.change_type |
| Provider Name | text (display only) | N/A | Confirms which provider is being suspended/deactivated | Display only | ENT-provider.name |
| Affected Cases & Quotes | read-only summary/list | N/A | Shows outstanding Parent Quotes and affected cases with links, prior stages, and the cancellation/support impact of the selected action | Suspension and deactivation both include Accepted, Confirmed, In Progress, and Aftercare (In Progress cases are shown as staying open for an admin decision and Aftercare cases as moving to aftercare reassignment; neither is closed); terminal history is not reclassified; revalidate at effective time (REQ-015-084) | no graph field (display) |
| Reason | textarea | Yes | Admin must provide detailed reason for suspension/deactivation | Min 20 chars, max 500 chars | ENT-pending-provider-status-change.reason |
| Notify Provider | checkbox | No | Option to send notification email to provider with reason | Default checked (true); checked and locked when deactivating from an account-closure request (A7); does not disable mandatory patient cancellation messages or admin support alerts (REQ-015-086) | ENT-pending-provider-status-change.notify_provider |
| Effective Date | date picker | No | Optional. Blank or today applies the change immediately on submit; a future date schedules it | Must be today or future date; "today" is the current UTC date | ENT-pending-provider-status-change.effective_date |
| Admin Password | password | Yes | Re-authentication before the status change (MFA once FR-026 / FR-031 MFA stack is delivered) | Must match the acting admin's password | no graph field (control) |
| Confirm Action | checkbox | Yes | Admin must check "I confirm this action" before submitting | Must be checked to enable submit button | no graph field (control) |

**Business Rules**:

- **Required Reason**: Admin cannot suspend or deactivate provider without providing detailed reason (minimum 20 characters) (REQ-015-081)
- **Suspension vs. Deactivation**:
  - **Suspension**: Temporary status change; provider account remains in system and can be reactivated later
    - Block new inquiry allocations, quote submissions, patient acceptances, and further payment against this provider's affected selections as soon as suspension is effective.
    - Automatically cancel this provider's outstanding unaccepted quotes (FR-004 `cancelled_provider_status`) and close all related non-terminal bookings in the FR-006 booking stages `Accepted` or `Confirmed`, using Alternative Flow A5. `In Progress` bookings are not closed; they stay `In Progress` with the support marker until an admin decides them through FR-006 Alternative Flow B7: move to `Aftercare` with aftercare reassignment, or cancel with a reason. Closed accepted bookings enter the FR-006 provider-fault transfer (Alternative Flows B4 and B5), where an admin rehomes the patient to a replacement provider in the same inquiry. `Aftercare` bookings and FR-011 standalone aftercare cases assigned to this provider are not closed; they move to aftercare reassignment (FR-006 Alternative Flow B6 and FR-011). Existing upcoming bookings do not remain active with this provider.
    - Record `ProviderSuspended` as the cancellation reason and `supportRequired = true`; display `Cancelled — Provider Suspended` with a separate `Admin Support Required` marker on affected cases and affected inquiries. In Progress and Aftercare cases keep their status and show the `Admin Support Required` marker with the provider-status cause. An inquiry with a closed accepted booking stays open for the replacement-provider transfer and is not cancelled. For shared unaccepted inquiries, preserve the inquiry's normal stage and other providers' offers while flagging the suspended provider's participation and support need. (REQ-015-018)
    - Provider can still log in to Provider Platform but sees "Account Suspended" banner; the same applies to all of the provider's FR-009 team members. The banner and the suspended read-only behavior are specified in FR-032 (Rule 6). Read-only includes `In Progress` bookings: the suspended provider cannot check in, end treatment, or edit the treatment plan; the admin decides the case through FR-006 Alternative Flow B7. The suspended provider may still chat with patients on its open `In Progress` and `Aftercare` cases. Clinical notes, photos, and aftercare answers and actions stay blocked until the admin reassigns or decides the case (REQ-015-077)
  - **Deactivation**: Permanent status change; provider account cannot be reactivated (final removal from platform)
    - Automatically cancel this provider's outstanding unaccepted quotes and close all related non-terminal bookings in `Accepted` (including accepted-but-unpaid selections) or `Confirmed`, using the same Alternative Flow A5 cascade as suspension, including the hand-off of accepted bookings to the FR-006 provider-fault transfer; `In Progress` bookings stay open for the admin decision as for suspension; `Aftercare` bookings and FR-011 standalone aftercare cases move to aftercare reassignment as for suspension. Block new inquiry allocations, quote submissions, acceptances, and payment; release active reservations and retain accepted snapshots.
    - Use `ProviderDeactivated` as the cancellation reason and the same separate admin-support marker and patient/admin notification handoff. In Progress bookings awaiting the admin decision and Aftercare reassignments must reach admins for clinical continuity and recovery support (FR-010/FR-011 admin workflows). Deactivation must not overwrite the reason on cases already cancelled by suspension.
    - Provider login disabled immediately for the provider account and all of its FR-009 team members (REQ-015-076)
    - Provider data retained for audit/legal purposes but marked as deactivated
- **History and care continuity**: `Completed`, already `Cancelled`, and `Payment Window Expired` cases are not relabelled as new suspension or deactivation cancellations. Retain clinical notes, photos, completion milestones, accepted identifiers/versions, and payment/refund history. In Progress bookings awaiting the admin decision and Aftercare reassignments caused by suspension or deactivation must reach admins for clinical continuity and recovery support; automatic lifecycle cancellation does not itself transfer care or settle money; the admin replacement-provider transfer and its payment terms (full refund, no cancellation fee, new payment on the replacement booking) follow FR-006 Alternative Flow B5, and the aftercare reassignment follows FR-006 Alternative Flow B6 with no new acceptance or payment. (REQ-015-085)
- **Admin action links**: Each affected record in Affected Cases & Quotes links to the admin screen that resolves it: a closed booking before treatment starts links to Start Provider-Fault Transfer on FR-006 Screen 6 (FR-006 Screen 10); an `In Progress` booking links to FR-006 Screen 6, where the admin moves it to `Aftercare` with reassignment or cancels it; an Aftercare booking links to Reassign Aftercare on FR-006 Screen 6, which opens the FR-011 aftercare reassignment screen; an FR-011 standalone aftercare case links to the FR-011 aftercare reassignment screen; flagged inquiries and cases link to the FR-016 Admin Support Required view. Each of those screens records a mandatory reason, confirmation, and audit entry as its owning FR defines.
- **Admin Support Required**: This is an independent support marker, not a new patient journey stage or provider account status. Affected cases/inquiries must be identifiable and filterable through FR-016's admin workflow, with mandatory admin alerts through FR-020. The FR-020 admin-support alert goes to admins with the FR-031 Respond to Support permission. Opening the FR-016 list requires FR-031 View Patients, and Resolve Support requires Respond to Support. Admin resolution records a reason and audit event before clearing the marker; the cancellation cause remains. An inquiry's marker stays set while any linked provider-caused impact is unresolved. If an FR-034 support case is created/linked during assistance, retain its existing Open → In Progress → Resolved → Closed workflow. Automatic ticket creation is not introduced here. (REQ-015-078)
- **Patient communication**: Every affected patient is notified: `provider.status_cancellation_patient` for a cancelled unaccepted offer (before acceptance only), and `booking.provider_fault_replacement` (mandatory) for a closed accepted booking. Recipients, content and variants are defined in the FR-030 notification catalogue. Notification failures are retried without restoring cancelled cases.
- **Reactivation**: Performed through Screen 5 (Suspended providers only). Reactivation cancels any pending scheduled suspension or deactivation and permits new eligible activity only. It must not restore cancelled quotes/cases, reopen accepted selections, reinstate old reservations, restart payment windows, clear unresolved support markers, or restore the Featured flag. (REQ-015-021, REQ-015-079)
- **Featured flag**: When suspension or deactivation becomes effective, the system clears `featured` automatically (freeing a slot under Rule 8) and logs it in Tab 8.
- **Notification Email**: If "Notify Provider" checkbox enabled (default), system sends email (FR-020 `provider.suspended` or `provider.deactivated`). Its content is defined in the FR-030 notification catalogue.
- **Email timing**: For an immediate change the email is sent once. For a scheduled change with "Notify Provider" checked, the email is sent when the scheduled change is created (with the Effective Date) and again when it takes effect. If "Notify Provider" is unchecked, no provider email is sent at either point; patient messages and admin-support alerts are still mandatory. (REQ-015-050)
- **Email recipient**: Recipients of the provider status emails (`provider.suspended`, `provider.deactivated`, `provider.reactivated`, and `provider.scheduled_change_cancelled`) are set in the FR-030 notification catalogue. Team members learn of the status through the FR-032 Rule 6 banner or the deactivated-login message. (REQ-015-049)
- **Scheduled Status Change**: A blank or today's Effective Date is treated as immediate and is never queued for the midnight UTC job. If admin selects a future Effective Date, the suspension or deactivation is stored as pending and applied automatically on that date (job processes scheduled suspensions and deactivations daily at midnight UTC), recalculating affected records at that time (A5). Until then the provider keeps its current status, and Screen 1 and the Screen 3 header show "Scheduled: Suspend/Deactivate on DD-MM-YYYY". Only one pending change per provider is allowed; an immediate suspension or deactivation replaces any pending change. Reactivating a provider through Screen 5 cancels any pending change automatically (logged in Tab 8 with the reactivation reason). (REQ-015-082)
- **Cancel Scheduled Change**: Before the Effective Date, an admin can cancel the pending change from Screen 1 or the Screen 3 header by entering a reason (min 20 chars) and re-authenticating. Scheduling, cancellation, and application are logged in Tab 8; the provider Owner is emailed about the cancellation (FR-020 `provider.scheduled_change_cancelled`) if they were notified of the scheduled change. (REQ-015-083)
- **Confirmation Requirement**: Admin must explicitly check "I confirm this action" checkbox before "Submit" button enabled (prevents accidental suspension/deactivation) (REQ-015-081)

**Notes**:

- Use prominent warning styling (red border, caution icon) to emphasize severity of action
- Display clear differentiation between suspension (temporary, reversible) and deactivation (permanent, irreversible)
- Provide example reasons to guide admin (e.g., "Repeated unresolved patient complaints", "Violation of platform terms", "Provider requested account closure")
- Include "Cancel" button to abort action and return to provider profile view

---

### Screen 5: Provider Reactivation Modal

**Purpose**: Captures the admin reason and re-authentication before returning a Suspended provider to Active (Alternative Flow A6)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------ | --- |
| Provider Name | text (display only) | N/A | Confirms which provider is being reactivated | Display only | ENT-provider.name |
| Current Suspension | text (display only) | N/A | Suspension date and the reason recorded in Screen 4 | Retrieved from the latest suspension status event | ENT-provider-status-event.effective_at, ENT-provider-status-event.reason |
| Pending Scheduled Change | warning (display only) | N/A | Shown only when a scheduled suspension or deactivation is pending: "Reactivating will cancel the scheduled [Suspension/Deactivation] on DD-MM-YYYY" | Retrieved from the Pending Provider Status Change record (Key Entity 4) | ENT-pending-provider-status-change.change_type, ENT-pending-provider-status-change.effective_date |
| Unresolved Support Items | number (display only) | N/A | Count of this provider's affected inquiries and cases (bookings, In Progress/Aftercare cases, standalone aftercare) still marked Admin Support Required; each affected record counts once, matching the FR-020 `provider.status_cancellation_admin_support` unit (one per affected inquiry/case). Links to the FR-016 list filtered to this provider and Admin Support Required | Calculated from cancellation/support context; informational, does not block reactivation (REQ-015-134) | no graph field (display) |
| Reason | textarea | Yes | Why the provider is being reactivated | Min 20 chars, max 500 chars | ENT-provider-status-event.reason |
| Notify Provider | checkbox | No | Send reactivation email to the provider Owner including the reason | Default checked (true) | ENT-provider-status-event.notify_provider |
| Admin Password | password | Yes | Re-authentication before the status change (MFA once FR-026 / FR-031 MFA stack is delivered) | Must match the acting admin's password | no graph field (control) |
| Confirm Action | checkbox | Yes | "I confirm this action" | Must be checked to enable submit button | no graph field (control) |

**Business Rules**:

- Available only when provider status = Suspended; Deactivated providers can never be reactivated (Rule 4) (REQ-015-080)
- On submit, status changes to Active immediately; the status event (reason, admin, timestamp) is logged in Tab 8
- Reactivation follows the Screen 4 Reactivation rule: nothing cancelled by the suspension is restored, and the Featured flag stays cleared
- On submit, any pending scheduled suspension or deactivation is cancelled automatically; the cancellation is logged in Tab 8 with the reactivation reason and admin, and the reactivation email states that the scheduled change no longer applies (if the provider had been notified of it)

---

## Business Rules

### General Module Rules

- **Rule 1**: All provider accounts must be created by admins—no self-service provider registration allowed.
- **Rule 2**: Provider creation (and therefore activation) requires every field marked Required in the Screen 2 wizard: First Name, Last Name, Email, Phone Number, Bio/Description (50-500 chars), Specialty, Medical License Number, Years of Experience, at least 1 Language, Clinic Name, Clinic Address, Contact Email, Medical License file, Commission Model and Value, Flat Rate Currency (when Commission Model = Flat Rate), Payout Method, and Commission Start Date. The Medical License file is a record-keeping baseline only; document authenticity or later document changes never block activation or change status. Payout readiness (the clinic's own Stripe sign-up being Ready) is not required for creation or activation (Payout Readiness Rule). A field marked "Required" in a screen table means it is needed to submit or save that screen only; it does not by itself make the stored provider attribute mandatory. (REQ-015-030)
- **Rule 3**: Provider statuses are Active, Suspended, and Deactivated (there is no Draft status). Providers are created as Active when all required fields are complete. Allowed transitions: Active → Suspended (Screen 4), Suspended → Active (Screen 5), Active or Suspended → Deactivated (Screen 4). "Password not yet set" is tracked by `password_set = false`, not by a separate status. An Active provider with `password_set = false` is excluded from FR-003 inquiry distribution (including explicit patient selection and reassignment) until the password is set; it may still be featured or edited by admins. (REQ-015-031, REQ-015-052)
- **Rule 4**: Deactivation is permanent—deactivated providers cannot be reactivated; admin must create new provider account if re-onboarding required. Deactivation frees the provider's emails: Contact Email uniqueness counts only Active and Suspended providers, and login Email follows the FR-009 global provider email identity rule (Rule 3, REQ-009-008), under which the Owner, team member, and pending-invitation emails of a Deactivated provider are freed. The new account may reuse those emails; the deactivated record and its history are retained unchanged. (REQ-015-032, REQ-015-070)
- **Rule 5**: Commission configuration applies at booking confirmation under FR-029; later configuration edits never replace an existing confirmed booking's commission snapshot.
- **Rule 6**: Featured provider designation only available for providers with status = "Active". When suspension or deactivation becomes effective, the system clears the Featured flag automatically; it is not restored on reactivation. (REQ-015-033)
- **Rule 7**: Seat limit (maximum team members) defaults to 100 and can be adjusted by admin (range 1-500). Providers request seat limit increases via FR-009 "Request more seats", which opens an FR-034 support case pre-filled as a seat-increase request; if approved, the admin edits Seat Limit in Screen 3 Tab 1. Seat limit blocks staff invitations when reached (enforced by FR-009). (REQ-015-035)
- **Rule 8**: At most 10 active providers may be featured. Admin can set or unset featured status from the Provider-list quick action or the Basic Information toggle. A request to feature an eleventh provider must be rejected without changing data and must clearly tell the admin to unfeature another provider first, using the message: "Maximum of 10 featured providers reached. Unfeature another provider first." Featuring or unfeaturing does not require an admin change reason (Tab 8 still logs it). This limit must be enforced server-side for every write path. (REQ-015-034)
- **Rule 9**: Provider-status eligibility must be revalidated at inquiry allocation (which also requires `password_set = true`, Rule 3), quote submission, Subquote acceptance, booking-confirming payment, and three FR-006 admin actions: admin Revive Booking, admin appointment change (reschedule), and admin acceptance of a replacement quote (FR-006 B5). Each of these requires the provider to be Active; FR-006 REQ-006-020 owns the blocking message ([CR-FR006-20261027-02](../../../../archived/prd-baseline-2026-11-08/fr006-booking-scheduling/change-request-2026-10-27-admin-actions-require-active-provider.md)). Once suspension/deactivation is effective, an in-flight request or delayed callback must not create an eligible quote, revive a cancelled case, or confirm a new booking for that provider. Any payment actually captured must remain recorded and reach admin financial reconciliation, not be hidden or treated as a successful new booking. FR-007 records such late captures; FR-017 owns flagging them for admin reconciliation, holding them from provider payout, and cancelling remaining scheduled installments on provider-cancelled bookings ([CR-FR017-20261015-01](../../../../archived/prd-baseline-2026-11-08/fr017-admin-billing-finance/change-request-2026-10-15-post-suspension-payment-reconciliation.md)). Before acceptance, the status change cancels the provider's unaccepted quotes (FR-004 `cancelled_provider_status`). After acceptance, the booking is closed and handed to the FR-006 provider-fault transfer (Alternative Flows B4 and B5), where an admin rehomes the patient to a replacement provider in the same inquiry; the inquiry is not cancelled. An `Aftercare` booking is not closed and moves to aftercare reassignment (FR-006 Alternative Flow B6).
- **Rule 10**: Screen 4 and Alternative Flow A5 own provider-status cancellation and support effects; FR-006 Alternative Flow B5 owns the replacement-provider transfer for accepted bookings before treatment starts, FR-006 Alternative Flow B7 (on Screen 6) owns the admin decision for `In Progress` bookings (move to Aftercare with reassignment, or cancel), and FR-006 Alternative Flow B6 with FR-011 owns only the aftercare reassignment. The cascade is provider-scoped, preserves immutable accepted context, and must not count alternatives as independent treatments or cancel unrelated providers' unaccepted offers. (REQ-015-036)
- Admins must be authenticated and hold the FR-031 Provider Management (A-02) permissions: View Providers (Screen 1 and Screen 3 read access), Onboard Providers (Screen 2), Edit Providers (Screen 3 edits, documents, commission, seat limit, featured flag, Resend Activation Email), and Suspend Providers (Screens 4-5: suspension, deactivation, reactivation, scheduled-change cancellation). Login as Provider is restricted to Super Admin; re-authentication for suspend/deactivate/reactivate/Login as Provider uses the admin's credentials (REQ-015-069)
- all default roles (Super Admin, Aftercare Specialist, Billing Staff, Support Staff) have View Providers; by default only Super Admin has Edit Providers, Onboard Providers, and Suspend Providers, which custom roles may also be granted per FR-031
- P-02 queries A-02 provider data filtered by (status = "Active" AND featured = true) to populate featured provider listings; includes provider name, clinic, specialty, profile photo
- The `provider.*` Events named in this FR are owned by FR-030 (notification catalogue), which holds their recipients, content and switch-off rules; FR-015 only says when each one fires. FR-020 owns delivery and recipient-scoped payloads, and the FR-030 retry rule applies to failed deliveries; provider-caused cancellation must not use FR-003's patient-cancellation message or expose confidential suspension reasons to patients.
- Preserve the AcceptanceEvent, selected identifiers, equal accepted aggregate versions, and quote-local package snapshot; do not modify the reusable package library.
- cancellation excludes a selection from active pending-payment exposure without deleting historical acceptance/price observations.
- FR-032 owns field validation (Clinic Name 3-200 chars, unique Contact Email, document formats PDF/JPG/PNG/DOCX/XLSX) that FR-015 reuses.
- No SMS delivery is available in MVP.
- If email delivery fails, S-03 retries under the FR-030 notification retry rule; A-02 displays warning to admin: "Notification queued but not yet delivered." The same warning applies to activation emails and provider status emails (REQ-015-048)
- If upload fails, A-02 displays error to admin: "Document upload failed. Please retry." Document upload retries automatically up to 3 times before failing (REQ-015-133)
- A-02 retries upload up to 3 times with exponential backoff before failing (REQ-015-133)
- Admins access Admin Platform via desktop/laptop computers (not mobile devices) due to complexity of provider creation forms and document review workflows
- Providers access Provider Platform to view profile status via both desktop and mobile devices (responsive design required for provider profile view)
- Providers will proactively provide updated documents when renewals occur without system-prompted reminders
- Deactivated providers' data is retained for legal/audit purposes (retention follows the system PRD, Platform-Wide Rules: One 10-year retention period), then archived; it is never hard-deleted. GDPR/data deletion requests are handled via separate data privacy workflows (not in-scope for A-02) (REQ-015-068)
- Document upload functionality should support chunked/resumable uploads for large files (up to 10MB) to handle unreliable admin connections
- Commission rate validation enforced at both client-side (immediate feedback) and server-side (security) to prevent invalid configurations. (REQ-015-100)
- A-02 returns empty array if no featured providers available; P-02 displays "No featured providers at this time" message
- Revalidate eligibility during concurrent acceptance/payment; retry incomplete cascade processing without duplicate outcomes, and do not report a fully completed cascade while affected cases remain unprocessed. (REQ-015-072)
- A-02 reads the active lists at form load and validates saved values against them.
- A-02 reads active catalog languages at form load and validates saved values against them; a stored language later removed from the catalog still displays but cannot be newly selected. (REQ-015-098)
- A-02 logs notification failures and displays warning to admin
- No in-system document status workflow is tracked in this FR.
- Affected inquiry/case owners retain the provider-status event reference, cancellation reason, and `supportRequired` marker with resolution audit.

### Data & Privacy Rules

- **Privacy Rule 1**: Provider contact information (email, phone) visible only to admins; patients see clinic phone/email. (REQ-015-037)
- **Privacy Rule 2**: Uploaded provider documents (licenses, certifications, insurance) encrypted at rest using AES-256.
- **Audit Rule**: All provider management actions logged with timestamp, admin user ID, action details, and the admin's reason or justification (Screen 3 Tab 1 admin change reason, Screens 4-5 status reasons, Login as Provider reason). Provider-status cancellation records include the triggering status event, effective time, affected inquiry/quote/booking/treatment identifiers, prior stage, cancellation cause, support marker, slot-release outcome, and notification outcome. Sensitive suspension reasons remain admin/provider context rather than patient notification content.
- S-05 returns secure download URLs accessible only to authorized admins
- A-02 sends audit log events to S-06 API with structured data (timestamp, admin user ID, action type, entity ID, before/after values); S-06 persists logs and provides query interface for admin reporting
- 100% of provider management actions logged with timestamp, admin user ID, IP address, and action details; audit logs immutable (cannot be edited or deleted by admins)
- Service-to-service authentication via API key in request header
- OAuth 2.0 service account token for S-05 API access
- OAuth 2.0 provider user token validated by A-02 API; provider can only access their own profile data (not other providers)
- Public read-only REST endpoint (no authentication required for featured provider listings); returns only the public fields listed above and is rate limited, as the constitution requires for all public-facing APIs
- Provider sensitive data (email, phone, medical license number) is stored in the database protected by database/disk encryption at rest, HTTPS/TLS in transit, and access control. It is not encrypted at application level, so the Screen 1 partial search and the login email uniqueness check keep working (REQ-015-067)
- All API communication via HTTPS/TLS 1.3 (no unencrypted HTTP allowed)
- Rate limiting on provider creation API (max 10 provider creations per admin per hour) to prevent bulk account creation abuse (REQ-015-066)
- File upload validation (max 10MB per file, only PDF, JPG, PNG, DOCX, and XLSX allowed, matching FR-032; malware scanning via antivirus integration before storage) (REQ-015-065)
- Input sanitization on all form fields (prevent SQL injection, XSS attacks)
- Confidential handling of provider medical licenses and certifications (professional records, not patient PHI) with the same encryption and access controls
- GDPR compliance for provider personal data (name, email, phone) with data retention following the system PRD, Platform-Wide Rules: One 10-year retention period (deactivated providers' data is then archived; never hard-deleted)
- SOC 2 Type II audit trail requirements met via S-06 Audit Log Service integration
- **Integration point**: FR-006 Alternative Flow B4 applies the provider-status cancellation cause, releases valid holds/reservations, blocks further payment, and retains all booking/payment history; FR-006 Alternative Flow B5 then performs the admin replacement-provider transfer in the same inquiry with its payment terms (full refund, no cancellation fee, new payment on the replacement booking). FR-006 Alternative Flow B7 (Provider Fault While In Progress, Admin Decision) decides an `In Progress` booking; FR-006 Alternative Flow B6 handles only the aftercare reassignment, both for `Aftercare` bookings (which are not closed) and for an `In Progress` booking the admin moves to `Aftercare`. Provider suspension is cancellation, not `Payment Window Expired`; exact payment mechanics retain their existing owners.
- **Integration point**: Snapshot the effective model/value at booking confirmation, preserve existing booking snapshots, and keep provider-specific edits synchronized. Payout-cycle timing and fund-release rules are not redesigned here; the settlement period for manual-rail clinics is the one platform-wide FR-029 setting (REQ-015-128). FR-029 Screen 5 accepts the same provider-specific Percentage (0-100%) or Flat Rate model defined here ([CR-FR029-20261014-01](../../../../archived/prd-baseline-2026-11-08/fr029-payment-system-config/change-request-2026-10-14-provider-flat-rate-commission.md)).
- Supply cancellation cause, affected case/inquiry references, prior stage, and support marker to FR-016 and FR-020. Patient messages provide Contact Admin/Support; confidential investigation details remain restricted. Support handling may link an existing/manual FR-034 case, but this change does not create a new automated ticket source or another ticket lifecycle.

### Admin Editability Rules

**Editable by Admin**: (REQ-015-039)

- Provider basic information (name, specialty, bio, languages, awards)
- Clinic information (name, address, phone, logo, contact email)
- Commission configuration (Model: Percentage/Flat, Value, Flat Rate Currency, Effective Date)
- Payout method (Stripe Connect or Manual bank transfer; admin only, at creation and afterwards)
- Seat limit (maximum team members, range 1-500, default 100)
- Document uploads (Add; Replace/Remove admin-uploaded documents only; provider-uploaded documents are managed by the provider via FR-032)
- Provider status (Active, Suspended, Deactivated)
- Featured provider designation

**Editable by Provider (via FR-032)**:

- Profile Picture/Logo
- Cover Image
- Bio/Description
- Languages Spoken
- Awards & Recognition (add/edit/delete with images)
- Clinic Name
- Contact Phone (Public)
- Contact Email
- Location (City, Country)
- Website URL
- Time zone (in FR-032 account settings)

**Fixed in Codebase**:

- Deactivation finality rule
- Encryption standards
- Commission calculation logic

### Payment & Billing Rules

- **Commission Rule 1**: Commissions apply to all provider earnings from patient bookings. (REQ-015-040)
- **Commission Rule 2**: **Percentage Model**: Calculated as `Booking Total * (Commission Rate / 100)`. The booking total is the accepted price after promotion, in the quote currency, read from the FR-005 acceptance snapshot; commission never reads the live quote or option record. The same base applies to every discount type, including discounts funded only by Hairline. The rate is the one fixed at booking confirmation (Commission Rule 4). (REQ-015-041)
- **Commission Rule 3**: **Flat Rate Model**: Fixed amount deducted per completed procedure (e.g., £150 flat fee). (REQ-015-042)
- **Commission Rule 4**: Resolve and snapshot the effective commission model/value when a booking is confirmed. Changes affect newly confirmed bookings only; existing snapshots govern later payments and commission recognition. Locking configuration at confirmation does not move the Flat Rate deduction away from its existing completed-procedure milestone.
- **Cancellation Billing Rule**: Suspension or deactivation closes affected bookings and blocks further patient payment to that provider, but payment/refund/commission records remain intact. For a closed accepted booking, money follows the FR-006 Alternative Flow B5 payment terms: the patient is refunded in full everything paid, pays no cancellation fee, and the replacement booking takes a new payment. For an `In Progress` booking (treatment already started), an admin reviews each case and sets the patient refund amount, from zero up to the full amount paid, with a mandatory reason and an audit entry, and the provider's payout for that booking is held until the admin decides (FR-006 Alternative Flow B7 payment terms). Exact refund, fund-release, and allocation mechanics belong to FR-007, FR-007B, and FR-017; no new refund percentage or fee is defined here, and the payout method and payout-readiness rules below concern only a clinic's payout setup. (REQ-015-043)
- **Billing Rule 1**: There is no per-clinic payout frequency. On the Stripe Connect rail, release to the clinic is automatic through FR-017. A clinic paid by manual bank transfer follows the one settlement-period setting owned by FR-029 (default weekly, Sunday cutoff, Wednesday payout), which applies to all manually paid clinics. (REQ-015-044)
- **Payout Method Rule**: The admin chooses the clinic's payout method (Stripe Connect or Manual bank transfer) when creating the clinic (Screen 2 Step 5). The clinic sees its payout method and payout readiness read-only in its own dashboard (FR-032) and completes Stripe's own sign-up itself. After go-live only an admin changes the payout method (Tab 7); the clinic asks Hairline.
- **Payout Readiness Rule**: Clinic activation does not wait for payout readiness. If a Stripe Connect clinic's payout setup is not Ready when a booking's share is due to move to the clinic, the share stays with Hairline, the clinic and the admin are told, and the share moves when the clinic becomes Ready. Nothing is paid out before then, even after treatment.

**Carried from dropped sections (original wording)**:

- **SC-003**: Patients see only active providers in search results (no suspended/deactivated providers visible), ensuring trust and booking reliability
- **Relationships**: One provider has many status events (append-only; never updated after creation). This is the "provider status event" referenced by REQ-015-024 and by the `provider_status_event_id` / `deactivation_event_id` columns on the owning inquiry, booking, aftercare, payment, and closure-request records (`provider_status_events` in system-data-schema.md). Tab 8 displays it but the Tab 8 activity log is not the event record.

---

## Dependencies

Related FRs: FR-031 (admin permissions: View, Onboard, Edit, Suspend Providers), FR-009 (provider login, Seat Limit enforcement), FR-022 (featured listing; patient provider search is P2), FR-020 (provider lifecycle email events), FR-003 (distribute inquiries only to Active providers with password_set = true), FR-004 (unaccepted quotes cancelled with cancelled_provider_status), FR-005 (accepted selection; supersession on admin replacement acceptance), FR-006 (provider-fault transfer, Alternative Flows B4 to B7), FR-007 (payment mechanics; late captures recorded), FR-010 (In Progress bookings not cancelled automatically), FR-011 (aftercare reassignment), FR-014 (Completed Procedures counts), FR-016 (admin patient management; affected case references), FR-034 (support case linking), FR-029 (commission snapshot at booking confirmation), FR-017 (consumes commission snapshots; payout holds), FR-032 (provider self-edit and documents; shared records), FR-024 (starting price: lowest standard price among active packages), FR-013 (Tab 5 reviews; admin review actions), FR-026 (country and Provider Specialties lists; MFA and re-authentication), FR-021 (language catalog). Shared services without a dedicated FR: S-05 Media Storage Service, S-06 Audit Log Service.

---

## User Scenarios & Testing

### User Story 1 - Admin Onboards New Provider from Scratch (Priority: P1)

Admin receives provider application materials (resume, licenses, certifications, insurance) and creates complete provider profile in Admin Platform, uploads documents, configures commission, and activates account. Provider receives email notification and can immediately log into Provider Platform.

**Why this priority**: Core functionality enabling platform provider network growth; without this, no providers can be onboarded and platform cannot function.

**Independent Test**: Admin completes full provider onboarding workflow from provider creation form to activation; verify provider receives activation email, can log into Provider Platform, and views correct profile data (name, clinic, commission rate).

**Acceptance Scenarios**:

1. **Given** admin is logged into Admin Platform with the FR-031 Onboard Providers permission, **When** admin navigates to Provider Management → "Add New Provider" → completes every wizard field marked Required (name, email, phone, license, clinic and contact email, Medical License file, commission model/value, payout method, commission start date) → clicks "Create Provider", **Then** system creates provider with status = "Active", sends activation email to provider, and displays success message: "Provider [Clinic Name] created successfully. An activation email has been sent to [email]."
2. **Given** provider receives the activation email with a one-time password setup link, **When** provider opens the link within 24 hours, sets a password that meets the platform policy, and logs in, **Then** provider successfully logs into Provider Platform and sees account status = "Active" (no FR-032 Rule 6 banner), uploaded documents in FR-032 Tab 6, and, as Owner, the read-only commission configuration in FR-032 Screen 4: Billing Settings (Commission & Payout panel)
3. **[P2 - Post-MVP, validated once FR-022 patient provider search ships]** **Given** admin activates provider with featured = true, **When** patient opens Patient Platform provider search, **Then** newly activated provider appears in "Featured Providers" section with gold star badge

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

### User Story 3 - Admin Suspends Provider Due to Policy Violation (Priority: P1)

Admin identifies provider violating platform terms (e.g., fraudulent reviews, inappropriate conduct, non-response to patient inquiries) and suspends provider account temporarily to investigate.

**Why this priority**: Important for platform integrity and patient safety, but less urgent than core provider onboarding workflows.

**Independent Test**: Admin suspends a provider with outstanding quotes, an Accepted unpaid case, a Confirmed booking, an In Progress case, and an Aftercare case. Verify outstanding unaccepted quotes become `cancelled_provider_status`, the Accepted and Confirmed bookings are closed with `ProviderSuspended` and `supportRequired = true` and enter the FR-006 provider-fault transfer, the In Progress booking stays `In Progress` with the cause and support marker for an admin decision, the Aftercare booking keeps its status with the cause and support marker and moves to aftercare reassignment, inquiries with accepted bookings stay open, reservations are released, new activity/payment is blocked, patients/admins are notified, and historical snapshots/clinical/payment records remain retained.

**Acceptance Scenarios**:

1. **Given** admin views provider with policy violations, **When** admin confirms suspension with a valid reason, **Then** the provider becomes Suspended, new allocation/submission/acceptance/payment is blocked, the A5 cancellation cascade runs, and all affected outcomes are audited.
2. **Given** provider has 3 upcoming confirmed appointments, **When** admin opens suspension, **Then** the warning explains that those appointments will automatically be cancelled and patients will be directed to admins. On confirmation, all 3 bookings are Cancelled with `ProviderSuspended` and `Admin Support Required`, their inquiries stay open, and each enters the FR-006 provider-fault transfer so an admin can rehome the patient to a replacement provider; no separate manual cancellation is needed.
3. **Given** suspended provider attempts to log into Provider Platform, **When** provider enters credentials and submits login, **Then** system allows login but displays prominent "Account Suspended" banner with message "Your account is temporarily suspended. Reason: [admin-provided reason]. Contact <support@hairlineapp.com> for assistance." Provider can view profile and documents but cannot accept new inquiries. Banner and read-only behavior follow FR-032 Rule 6.
4. **Given** admin resolves the policy violation, **When** admin reactivates the provider with a reason, **Then** status becomes Active and new eligible inquiry/quote activity is permitted, but cancelled cases/quotes, old payment windows, and unresolved support markers are not restored or cleared automatically.
5. **Given** an accepted Subquote still has time left in its payment hold, **When** its provider is suspended, **Then** the pending case is Cancelled immediately, payment is disabled, the hold is released, the parent quote keeps `accepted`, and accepted IDs/versions, package, appointment, and price snapshot remain unchanged. It is not labelled Payment Window Expired, and the patient is told that an admin will arrange a replacement provider in the same inquiry.
6. **Given** the same provider has In Progress and Aftercare cases plus a Completed historical case, **When** suspension becomes effective, **Then** the In Progress case stays `In Progress`, is flagged for admin clinical support, and waits for the admin to move it to Aftercare with reassignment or cancel it, and the Aftercare case keeps its status, is flagged, and moves to admin aftercare reassignment with no new acceptance or payment. Existing clinical records and completed-procedure milestones remain, and the Completed case is unchanged.
7. **Given** an inquiry has unaccepted offers from several providers, **When** one provider is suspended, **Then** only that provider's participation/quotes become cancelled/ineligible, the inquiry is flagged for admin support, and other providers' offers are not cancelled by this event.
8. **Given** Notify Provider is unchecked, **When** suspension cancels cases, **Then** affected patient messages and admin-support alerts are still mandatory. Clearing a support marker requires an audited admin resolution; the cancellation reason remains.

---

### User Story 4 - Admin Configures Flat Rate Commission (Priority: P2)

Admin configures a provider account with a fixed commission fee (e.g., £200 per procedure) instead of a percentage.

**Why this priority**: Supports flexible business models with different clinics.

**Independent Test**: Admin creates/edits provider, selects "Flat Rate" commission, enters value "200"; verify calculations for bookings use the flat rate deduction.

**Acceptance Scenarios**:

1. **Given** admin is editing provider commission settings, **When** admin selects "Flat Rate" and enters "200", **Then** system saves the configuration.
2. **Given** a provider has a £200 flat rate, **When** a £3000 booking is completed, **Then** system calculates Platform Commission as £200 (not a percentage).
3. **Given** a booking was confirmed with a £200 flat-fee snapshot, **When** the provider's configured fee becomes £250 before a later installment or procedure completion, **Then** that booking still uses £200 once per completed procedure. A newly confirmed booking uses the effective £250 configuration; quote alternatives/installments do not multiply the fee.
4. **Given** an unpaid accepted selection predates a commission edit, **When** its valid initial payment later confirms the booking, **Then** commission is snapshotted from the configuration effective at confirmation while the accepted patient price/FX remains unchanged. Subsequent edits do not replace that snapshot.

---

**Note**: Provider-side user stories (viewing/editing profile, managing settings) are documented in **FR-032: Provider Dashboard Settings & Profile Management**. FR-015 focuses exclusively on admin-initiated provider management actions.

### Edge Cases

- What happens when **admin attempts to create provider with email already used by another provider**? Login email follows the FR-009 global provider email identity rule (Rule 3, REQ-009-008); Deactivated providers' emails are freed (see Rule 4). If another provider organization uses the email as Owner, team member, or pending invitation, system displays validation error: "Email address already in use by another provider (Provider Name: [existing provider]). Please use a different email or edit the existing provider." Provider creation blocked until unique email provided. (REQ-015-070)
- How does system handle **provider document upload fails mid-upload (network interruption)**? System supports resumable uploads; if upload interrupted, admin can retry upload (system may resume from last successful chunk if implemented, otherwise restarts upload). (REQ-015-133)
- What occurs if **admin activates provider but notification email delivery fails (email service down)**? System retries the delivery under the FR-030 notification retry rule; admin sees warning message: "Notification queued but not yet delivered." Admin can manually resend via the "Resend Activation Email" button in Screen 3. (REQ-015-048)
- How to manage **two admins, or an admin and the provider, editing the same provider profile at the same time**? The last save wins, and only for a field that both people changed: a save applies only the fields the user changed and does not rewrite untouched fields. There is no conflict check and no conflict message, for admin saves (FR-015) and provider saves (FR-032) alike. Every save is logged in Tab 8 with its changed fields, so an overwritten value can be traced. (REQ-015-112)
- What happens when **admin deactivates provider with 10 upcoming patient bookings and active treatment/aftercare cases**? The impact modal lists all non-terminal Accepted, Confirmed, In Progress, and Aftercare cases. On confirmation, the Accepted and Confirmed cases are cancelled with `ProviderDeactivated` (same cascade as suspension), In Progress cases stay `In Progress` with the cause and support marker for an admin decision, reservations released, further payment blocked, patients notified to contact admins, and affected records flagged for support. Historical selections remain. Aftercare cases keep their status with the `ProviderDeactivated` cause and move to admin aftercare reassignment (FR-006 Alternative Flow B6). Each affected inquiry stays open, and an admin rehomes each patient to a replacement provider through the FR-006 provider-fault transfer (Alternative Flow B5), with each patient refunded in full everything paid, charged no cancellation fee, and taking a new payment on the replacement booking.
- What happens if **admin attempts to create provider without filling required fields**? System validates every field marked Required in the Screen 2 wizard tables on each step (see Rule 2). System displays error: "Please complete all required fields before proceeding" and highlights missing fields in red. (REQ-015-055)
- What occurs if **admin attempts to set invalid commission rate (e.g., negative percentage or zero flat rate)**? System displays client-side validation error immediately: "Percentage must be between 0-100%" or "Flat rate must be greater than 0." Server-side validation also enforces rules; the API returns a 422 validation error whose field message uses the same PRD wording if an invalid rate is submitted. (REQ-015-100)
- How to manage **provider requests account closure (wants to be deactivated)**? Provider submits an account-closure request in FR-032 (Request account closure) or contacts admin; there is no self-service deactivation. Admin processes it per Alternative Flow A7: opens the provider profile → clicks "Deactivate Provider" → enters reason: "Provider requested account closure on [date]" → confirms deactivation. System deactivates account, cancels all non-terminal cases under the Screen 4 cascade, marks any FR-032 closure request Approved, and sends the deactivation email (FR-020 `provider.deactivated`; "Notify Provider" is locked on for closure deactivations). If the admin rejects the request, the provider stays Active and receives FR-020 `provider.closure_rejected` with the review notes. (REQ-015-086, REQ-015-087)
- What happens if **admin sets seat limit below current team size**? System validates seat limit against current team size, meaning FR-009 seat usage (non-Owner team members with status Active or Suspended plus invitations with status Pending that are not past expiry; the Owner, Removed members, and Expired, Cancelled, or Accepted invitations do not count (FR-009 Rule 6, CR-FR009-20261028-01)). If seat limit is set below current count (e.g., provider has 50 staff but admin sets limit to 30), system displays warning: "Current team size (50) exceeds new seat limit (30). Existing team members will not be removed, but no new invitations can be sent until limit is increased or team size is reduced." Admin must confirm to proceed. Existing team members remain active; only new invitations are blocked. (REQ-015-115)
- What happens if **provider doesn't receive activation email**? Provider can click "Didn't receive activation email?" link on login page, enter their email, and request resend. System generates new one-time password setup link (expires 24 hours), invalidates previous link, and sends new email. Rate limited to 3 resend requests per hour per email. Admin can also manually resend from provider profile in FR-015 by clicking "Resend Activation Email" button in Quick Actions (visible only if password not yet set). (REQ-015-016, REQ-015-057, REQ-015-053)
- What happens if **activation link expires (24 hours passed)**? Provider can request new activation email via login page resend flow or contact admin. Admin can manually resend from provider profile. When provider clicks expired link, system displays: "This activation link has expired. Request a new activation email or contact support." (REQ-015-057)
- What happens if **provider tries to request activation resend but already activated account**? System displays generic message: "If an account exists with this email, an activation link will be sent." (doesn't reveal if account already activated for security). No email sent. This prevents email enumeration attacks. (REQ-015-056)
- What happens if **admin accidentally creates duplicate provider with same email**? System validates the login email against the FR-009 global provider email identity rule (Rule 3, REQ-009-008) during provider creation. If an Active or Suspended provider already uses the email as its Owner login, system displays error: "Email address already in use by another provider (Provider Name: [existing provider]). Please use a different email or edit the existing provider." Creation blocked until unique email provided. (REQ-015-070)
- What happens if **acceptance or initial payment races with suspension**? Eligibility must be checked against the effective provider status. No cancelled selection may be confirmed or revived; any real captured payment remains recorded and is routed to admin financial resolution. (REQ-015-071)
- What happens if **a scheduled suspension or deactivation becomes effective after more cases were created**? Recalculate affected records at effective time rather than using the old preview. The scheduled rule does not delay cancellation until each patient requests support.
- What happens if **cancellation/support notifications fail or cascade processing retries**? Keep provider eligibility revoked and cancelled records cancelled. Retry incomplete work using the same status event/case references without duplicate cancellations, alerts, or slot releases; retain visible unresolved processing failures for admins. (REQ-015-072)
- What happens if **a quote contains five packages with several date alternatives**? They remain alternatives of the same Parent Quote. Cancel its availability once; do not create a treatment or support item per unselected alternative. (REQ-015-073)
- What happens if **a provider is deactivated after suspension already cancelled cases**? Do not overwrite ProviderSuspended or create another cancellation for terminal records; retain unresolved support markers and the original audit chain. (REQ-015-075)
- What happens if **suspension affects an Aftercare case after the procedure was completed**? The case is not cancelled. It keeps its status, the FR-010 completion milestone, and its single Completed Procedures count; an admin reassigns aftercare to another provider or the Hairline aftercare team through the FR-011 aftercare reassignment screen. Performed care and payment history are not erased. (REQ-015-074)

---

## Functional Requirements Summary

### Core Requirements

- **REQ-015-001**: System MUST allow admins to create new provider accounts via a multi-step wizard, including profile (Bio, Languages, Awards), clinic details, seat limit (team member capacity), and commission settings.
- **REQ-015-002**: System MUST enforce admin-initiated provider creation only (no self-service registration).
- **REQ-015-003**: System MUST support provider status lifecycle with statuses Active, Suspended, and Deactivated only (no Draft): Active → Suspended (Screen 4), Suspended → Active via the Screen 5 reactivation modal, and Active or Suspended → Deactivated (Screen 4). Every transition requires a reason and admin re-authentication.
- **REQ-015-004**: System MUST allow providers to upload and manage their documents (license, certification, insurance) via FR-032. System MUST also allow admins to upload supplementary documents received externally. Documents are for record-keeping and do not block activation.
- **REQ-015-005**: System MUST log all provider management actions (creation, edits, status changes) in an immutable audit trail.
- **REQ-015-006**: System MUST send account activation email with one-time password setup link (expires 24 hours) when provider account is created. System MUST support activation email resend via self-service (provider login page) and admin manual resend (provider profile Quick Actions), with rate limiting (3 requests per hour per email) and automatic invalidation of previous links.
- **REQ-015-017**: Effective provider suspension MUST automatically cancel the provider's unaccepted Parent Quotes with the FR-004 status `cancelled_provider_status` and close all related non-terminal Accepted and Confirmed cases under A5/Screen 4, while an accepted Parent Quote keeps `accepted`; release active reservations and block further payment. Closed accepted bookings MUST enter the FR-006 provider-fault transfer instead of cancelling their inquiry. In Progress bookings MUST NOT be closed automatically; they MUST stay `In Progress` with the cause and support marker until an admin moves them to `Aftercare` with aftercare reassignment or cancels them with a reason. Aftercare bookings and FR-011 standalone aftercare cases assigned to that provider MUST NOT be closed; they MUST keep their status, receive the cause and support marker, and move to admin aftercare reassignment with no new acceptance or payment. Effective deactivation MUST apply the same cascade scope with the `ProviderDeactivated` cause, without overwriting an earlier `ProviderSuspended` cause.
- **REQ-015-018**: System MUST distinguish ProviderSuspended and ProviderDeactivated cancellation causes from patient cancellation and payment-window expiry, and set an independent `supportRequired` marker on affected cases/inquiries. Shared unaccepted inquiries MUST retain unrelated providers' offers; an inquiry whose accepted booking is closed by the cascade MUST stay open for the FR-006 provider-fault transfer and MUST NOT be cancelled.
- **REQ-015-019**: System MUST notify affected patients and alert admins when a provider status change cancels or flags their cases, regardless of the optional Notify Provider checkbox. Recipients, content, variants and whether a notice can be switched off are defined once, in the FR-030 notification catalogue (`provider.status_cancellation_patient`, `booking.provider_fault_replacement`, `provider.status_cancellation_admin_support`). Support resolution MUST be audited before clearing the marker.
- **REQ-015-020**: System MUST revalidate provider eligibility at allocation, submission, acceptance, booking confirmation, and the FR-006 admin actions admin Revive Booking, admin appointment change (reschedule), and admin acceptance of a replacement quote (FR-006 B5) (each requires an Active provider, per FR-006 REQ-006-020), prevent in-flight operations/callbacks from reviving cancelled cases, and deduplicate cascade processing by provider-status event and affected record. The status change and its provider status event MUST be written in one transaction; the cascade MUST run as an idempotent background job with a target completion within 5 minutes, and a reactivation MUST NOT stop a running cascade for the earlier event.
- **REQ-015-021**: Suspension, deactivation, or reactivation MUST NOT rewrite accepted snapshots/versions, erase clinical or financial history, or automatically reopen cancelled quotes/cases/payment windows. Admin support MUST retain access to the records needed for clinical continuity and financial resolution.
- **REQ-015-025**: Admin saves to provider profile data (Screen 3 Tabs 1, 2, 4, 6 notes, and 7) MUST require a change reason of 10-500 characters that is stored in the Tab 8 audit entry; provider self-edits via FR-032 and Featured Provider set/unset actions are exempt.
- **REQ-015-026**: Login as Provider MUST require a reason (min 20 characters) and admin re-authentication, show a persistent impersonation banner, block password/email/financial changes, log every action in Tab 8, and end after 30 minutes of inactivity. It MUST be blocked for a Deactivated provider and MUST be limited to the FR-032 Rule 6 read-only rules for a Suspended provider, whether the admin impersonates the Owner or a team member.
- **REQ-015-027**: System MUST clear the Featured flag automatically when suspension or deactivation becomes effective and MUST NOT restore it on reactivation.
- **REQ-015-028**: System MUST support scheduled suspension and deactivation: store at most one pending change per provider, show a "Scheduled" marker on Screen 1 and the Screen 3 header, allow admins to cancel it with a reason and re-authentication before the Effective Date, apply it automatically on that date with the A5 cascade recalculated at effective time, and log scheduling, cancellation, and application in Tab 8.
- **REQ-015-029**: Screen 4 MUST link each affected record to the admin screen that resolves it (provider-fault transfer, aftercare reassignment, or the FR-016 Admin Support Required view), and each of those actions MUST record a mandatory reason, confirmation, and audit entry.
- **REQ-015-124**: The admin MUST choose the clinic's payout method (Stripe Connect or Manual bank transfer) when creating the clinic in Screen 2 Step 5. The clinic sees its payout method and payout readiness read-only and completes Stripe's own sign-up itself.
- **REQ-015-125**: After go-live, only an admin MUST be able to change a clinic's payout method (Tab 7); a clinic that wants a change asks Hairline.
- **REQ-015-126**: Clinic creation and activation MUST NOT wait for payout readiness; a clinic can go live before its Stripe payout setup is Ready.
- **REQ-015-127**: When a booking's share is due to move to a clinic whose Stripe payout setup is not Ready, the share MUST stay with Hairline, the clinic and the admin MUST be told, and the share MUST move once the clinic becomes Ready. Nothing is paid out to the clinic before then, even after treatment.
- **REQ-015-128**: There MUST be no per-clinic payout frequency. On the manual bank transfer rail, one settlement-period setting owned by FR-029 (default weekly, Sunday cutoff, Wednesday payout) applies to all manually paid clinics; on the Stripe Connect rail, release is automatic.

### Data Requirements

- **REQ-015-007**: System MUST maintain provider profile data aligned with FR-032 (Bio, Languages, Awards, Profile Picture, Contact details, etc.). Changes made by providers in FR-032 must sync to admin view in real-time.
- **REQ-015-008**: System MUST store uploaded provider documents in secure cloud storage (AES-256).
- **REQ-015-009**: System MUST store commission configuration (Model: Percentage/Flat, Value, Flat Rate Currency, Effective Date) per provider in the FR-029 provider-specific commission record.
- **REQ-015-010**: System MUST store seat limit (maximum team members) per provider with default value of 100, adjustable range 1-500. Seat limit must be enforced by FR-009 when providers invite staff members.
- **REQ-015-011**: System MUST store activation token (one-time password setup link), token expiry timestamp (24 hours from generation), and the password_set status of the provider owner's login, all on the Provider record. System MUST invalidate previous tokens when new token is generated.
- **REQ-015-022**: Effective commission configuration MUST be snapshotted at booking confirmation under FR-029 and retained for later transactions; edits in FR-015/FR-029 MUST stay synchronized without replacing existing booking snapshots. Percentage/Flat Rate models and the once-per-completed-procedure flat-fee rule remain unchanged.
- **REQ-015-023**: Provider-profile Completed Procedures MUST count distinct FR-010 treatment completions, not quotes, options, accepted selections, payments, or final aftercare status. Later cancellation MUST NOT erase a recorded completion.
- **REQ-015-024**: System MUST retain provider-status event/effective-time references, affected record identifiers and prior stages, cancellation cause, support marker/resolution audit, slot-release outcome, and notification outcome for lifecycle impact and admin follow-up; storage remains with the existing owning entities rather than duplicating accepted data in Provider.

### Security & Privacy Requirements

- **REQ-015-012**: System MUST encrypt provider documents at rest and in transit.
- **REQ-015-013**: System MUST restrict document access to authenticated users (providers can access their own documents, admins can access all provider documents) with role-based permissions (providers can edit their own uploads, admins can edit admin uploads only).
- **REQ-015-014**: System MUST validate provider login Email against the FR-009 global provider email identity rule (Rule 3, REQ-009-008) on creation and on every change (blocking emails used by another provider organization as Owner, team member, or pending invitation), and MUST validate Contact Email uniqueness among Active and Suspended providers; Deactivated providers' emails are freed so a re-onboarded provider can reuse them.
- **REQ-015-015**: System MUST enforce the platform-wide password policy (see system PRD, Platform-Wide Rules: Password and one-time-code policy). Passwords MUST be hashed using bcrypt with a minimum cost factor of 12.
- **REQ-015-016**: System MUST rate limit activation email resend requests to 3 per hour per email address to prevent abuse and email flooding.

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-11-22 | 1.26 | Requirements graph programme baseline: PRD compressed to the checklist structure (each rule stated once, field rows tagged with graph field ids, dropped classes removed). No rule changes. Earlier history (versions 1.0 to 1.25) and the change requests (CR-FR015-20261013-01, CR-FR015-20261016-01, CR-FR015-20261027-01, CR-FR009-20261028-01, CR-FR032-20261015-01, CR-FR029-20261014-01, CR-FR029-20261015-01, CR-FR009-20261015-01, CR-FR017-20261015-01, CR-FR026-20261015-01, CR-FR032-20261015-02, CR-FR020-20261015-01, CR-FR030-20261015-01, CR-FR009-20261015-02, CR-FR032-20261015-03, CR-FR020-20261015-02, CR-FR030-20261015-02, CR-FR029-20261015-02, CR-FR003-20261015-01, CR-FR020-20261027-01, CR-FR006-20261027-02) are in `archived/prd-baseline-2026-11-08/` and in git history. | Product Owner / Documentation |
| 2026-11-23 | 1.27 | Independent compression review: 2 clause(s) from dropped sections restored in original wording under Business Rules. No rule changes. | Product Owner / Documentation |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | Joachim Trung Tuan | 2025-12-08 | ✅ Approved |
| Technical Lead | Claude (AI Assistant) | 2025-12-08 | ✅ Verified |
| Stakeholder | Vân Tay Media | 2025-12-08 | ✅ Approved |
| Product Owner | Joachim Trung Tuan | 2026-10-13 | Approved FR-015 v1.8 documentation changes and CR-FR015-20261013-01 via "Please proceed"; implementation reconciliation and consolidated verification pending |
| Product Owner | Joachim Trung Tuan | 2026-10-14 | Approved FR-015 v1.9 verification fixes (Issues 1-11 and minor issues) and the related downstream Change Requests; implementation reconciliation remains required |
| Product Owner | Joachim Trung Tuan | 2026-10-14 | Approved FR-015 v1.10 re-verification decisions (Issues 1-7 and minor fixes) via AskUserQuestion and "Yes"; implementation reconciliation remains required |
| Product Owner | Joachim Trung Tuan | 2026-10-15 | Approved FR-015 v1.11 third verification decisions (Issues 1-6) via AskUserQuestion and "Yes", including CR-FR032-20261015-01; implementation reconciliation remains required |
| Product Owner | Joachim Trung Tuan | 2026-10-15 | Approved FR-015 v1.12 fourth verification decisions (Issues 1-5) via AskUserQuestion and "Yes", including CR-FR029-20261015-01; implementation reconciliation remains required |
| Product Owner | Joachim Trung Tuan | 2026-10-15 | Approved FR-015 v1.13 fifth verification decisions (Issues 1-7) via AskUserQuestion and "Yes", including CR-FR009-20261015-01, CR-FR017-20261015-01, and CR-FR026-20261015-01; implementation reconciliation remains required |
| Product Owner | Joachim Trung Tuan | 2026-10-15 | Approved FR-015 v1.14 sixth verification decisions (Issues 1-6) via AskUserQuestion and "Yes", including CR-FR032-20261015-02 and CR-FR020-20261015-01; implementation reconciliation remains required |
| Product Owner | Joachim Trung Tuan | 2026-10-15 | Approved FR-015 v1.15 seventh verification decisions (Issues 1-3 and minor fixes) via AskUserQuestion ("Apply all now"), including CR-FR009-20261015-02; implementation reconciliation remains required |
| Product Owner | Joachim Trung Tuan | 2026-10-15 | Approved FR-015 v1.16 eighth verification decisions (Issues 1-6) via AskUserQuestion and "Yes", including CR-FR032-20261015-03, CR-FR020-20261015-02, CR-FR030-20261015-02, CR-FR029-20261015-02, and CR-FR003-20261015-01; implementation reconciliation remains required |
| Product Owner | Joachim Trung Tuan | 2026-10-16 | Approved FR-015 v1.17 MTG-002 quote model alignment through the 2026-10-16 decision log (D6, D6-M, D12, M5, M18, P1), including CR-FR015-20261016-01; consolidated verification and implementation reconciliation remain required |
| Product Owner | Joachim Trung Tuan | 2026-10-16 | Approved FR-015 v1.18 commission-base clarification for all discount types through the 2026-10-16 Product Owner follow-up decisions; implementation reconciliation pending |
| Product Owner | Joachim Trung Tuan | 2026-10-26 | Approved FR-015 v1.21 dev-team question decisions via AskUserQuestion (documentation only); implementation reconciliation pending |
| Product Owner | Joachim Trung Tuan | 2026-10-18 | Approved FR-015 v1.19 and v1.20 via MTG-002 decision log (documentation only), including [CR-FR015-20261016-01](../../../../archived/prd-baseline-2026-11-08/fr015-provider-management/change-request-2026-10-16-mtg002-quote-model-alignment.md) |
| Product Owner | Joachim Trung Tuan | 2026-10-27 | Approved FR-015 v1.22 dev-team follow-up decisions (documentation only), including CR-FR015-20261027-01; implementation reconciliation pending |
| Product Owner | Joachim Trung Tuan | 2026-10-28 | Approved FR-015 v1.23 backend confirmations (documentation only), with CR-FR009-20261028-01; implementation reconciliation pending |

Historical verification above applies to the prior baseline, not the new v1.8 cancellation/support contracts. The Product Owner's "all related treatment" scope is documented as all non-terminal Accepted, Confirmed, In Progress, and Aftercare cases; completed and already-terminal history remains unchanged. Other owning PRDs require separate controlled alignment before this change is considered cross-FR verified.

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B
**Based on**: system-prd.md (§ FR-015: Provider Management (Admin-Initiated))
**Last Updated**: 2026-11-22
