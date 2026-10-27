# FR-015 - Provider Management (Admin-Initiated)

**Module**: A-02: Provider Management & Onboarding
**Feature Branch**: `fr015-provider-management`
**Created**: 2025-11-11
**Version**: 1.22
**Status**: Revised 2026-10-27 (dev-team follow-up question resolution: save conflicts, data encryption, seat usage, impersonation, notification timing and recipients, cascade timing), pending consolidated verification; implementation reconciliation pending
**Source**: FR-015 from system-prd.md (§ FR-015: Provider Management (Admin-Initiated))
**Change Request**: [CR-FR015-20261013-01 — Provider lifecycle and accepted subquote contracts](change-request-2026-10-13-provider-lifecycle-subquote-contracts.md)
**Change Request**: [CR-FR015-20261016-01 — MTG-002 quote model alignment](change-request-2026-10-16-mtg002-quote-model-alignment.md)
**Change Request**: [CR-FR015-20261027-01 — Last-save-wins edits, at-rest encryption of provider contact data, and seat usage](change-request-2026-10-27-save-conflict-encryption-seat-usage.md)
**Related Change Request**: [CR-FR032-20261015-01](../fr032-provider-dashboard-settings/change-request-2026-10-15-provider-commission-panel-suspension-banner.md) — FR-032 Commission & Payout panel and provider account-status banner
**Related Change Request**: [CR-FR029-20261014-01 — Provider-specific Flat Rate commission in FR-029](../fr029-payment-system-config/change-request-2026-10-14-provider-flat-rate-commission.md)
**Related Change Request**: [CR-FR029-20261015-01 — Single-provider scope edits and scheduled commission configuration](../fr029-payment-system-config/change-request-2026-10-15-single-provider-scope-scheduled-commission.md)
**Related Change Request**: [CR-FR009-20261015-01 — Admin per-provider staff invite and limited-write impersonation](../fr009-provider-team-roles/change-request-2026-10-15-admin-staff-invite-impersonation.md)
**Related Change Request**: [CR-FR017-20261015-01 — Post-suspension payment reconciliation](../fr017-admin-billing-finance/change-request-2026-10-15-post-suspension-payment-reconciliation.md)
**Related Change Request**: [CR-FR026-20261015-01 — Managed Provider Specialties list](../fr026-app-settings-security/change-request-2026-10-15-provider-specialty-list.md)
**Related Change Request**: [CR-FR032-20261015-02 — Account closure as an admin-processed deactivation request](../fr032-provider-dashboard-settings/change-request-2026-10-15-account-closure-deactivation-request.md)
**Related Change Request**: [CR-FR020-20261015-01 — Mandatory provider lifecycle events](../fr020-notifications-alerts/change-request-2026-10-15-provider-lifecycle-events.md)
**Related Change Request**: [CR-FR030-20261015-01 — Provider lifecycle events in the notification catalog](../fr030-notification-rules-config/change-request-2026-10-15-provider-lifecycle-events.md)
**Related Change Request**: [CR-FR009-20261015-02 — Global provider email identity rule](../fr009-provider-team-roles/change-request-2026-10-15-global-provider-email-identity.md)
**Related Change Request**: [CR-FR032-20261015-03 — Closure request notifications and admin marker](../fr032-provider-dashboard-settings/change-request-2026-10-15-closure-request-notifications.md)
**Related Change Request**: [CR-FR020-20261015-02 — Provider closure request events](../fr020-notifications-alerts/change-request-2026-10-15-provider-closure-request-events.md)
**Related Change Request**: [CR-FR030-20261015-02 — Provider closure request events in the notification catalog](../fr030-notification-rules-config/change-request-2026-10-15-provider-closure-request-events.md)
**Related Change Request**: [CR-FR029-20261015-02 — Suspended providers in provider-specific commission scopes](../fr029-payment-system-config/change-request-2026-10-15-suspended-provider-commission-scopes.md)
**Related Change Request**: [CR-FR003-20261015-01 — Distribution requires a set password](../fr003-inquiry-submission/change-request-2026-10-15-distribution-requires-password-set.md)
**Related Change Request**: [CR-FR020-20261027-01 — Admin-support alert recipients and provider status email timing](../fr020-notifications-alerts/change-request-2026-10-27-admin-support-recipients-status-email-timing.md)

---

## Executive Summary

The Provider Management module enables administrators to onboard and manage hair transplant providers who will serve patients through the Hairline platform. This module is strictly admin-initiated—there is no self-service provider registration. Admins manually create provider accounts using a wizard-style interface, upload required documentation (for record-keeping), configure commission structures (Percentage or Flat Rate), and manage provider lifecycle status. The module also includes featured provider designation to control visibility in the patient-facing application. This module operates as the foundational gateway for the provider network, ensuring that all providers have valid profiles and agreed-upon commission terms before accepting bookings.

**Cross-Module Integration:** Providers can manage their own profile information (Bio, Languages, Awards, Logo) through **FR-032: Provider Dashboard Settings & Profile Management**. Changes made by providers in their dashboard automatically sync with the admin view, ensuring data consistency across platforms.

**Quote-model and lifecycle alignment:** One provider may submit multiple FR-004 Parent Quotes for one inquiry. Each parent contains package options that FR-005 resolves into patient-visible Subquotes; FR-006 books exactly one accepted Subquote. FR-015 manages provider eligibility, not quote/package editing. Provider suspension or deactivation automatically cancels that provider's unaccepted quotes and closes every non-terminal booking of that provider. A closed accepted booking enters the FR-006 provider-fault transfer, in which an admin moves the patient to a replacement provider within the same inquiry. Affected cases and inquiries are flagged for admin support. Current provider-profile and commission edits must not rewrite immutable accepted selections or historical booking commission snapshots.

**Note:** Document verification is performed externally; the system treats uploaded documents as pre-verified records and does not block account activation based on document status.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-02)**: Views featured provider listings (data consumed from A-02). **[P2 - Post-MVP]**: patient-facing display ships with FR-022 patient provider search; the admin featured flag and 10-provider cap are MVP.
- **Provider Platform (PR-01, PR-06)**: Providers sign in via PR-01 (FR-009) and view their profile status and uploaded documents in PR-06 (FR-032). They read data managed by A-02 and edit the allowed fields via FR-032. **Fields must align with FR-032**.
- **Admin Platform (A-02)**: Full provider lifecycle management including creation, document upload (record-keeping), commission configuration, and status changes.
- **Shared Services (S-03, S-05, S-06)**: S-03 (Notification Service) for provider lifecycle emails; S-05 (Media Storage) for profile images and document storage; S-06 (Audit Log Service) for creation and status-change logs.

### Multi-Tenant Breakdown

**Patient Platform (P-02)**:

- Display featured providers in provider discovery/search interfaces **[P2 - Post-MVP, via FR-022 patient provider search]**.
- Show provider bio, languages, awards, and clinic location.

**Provider Platform (PR-01, PR-06)**:

- Providers view their own profile (synced with A-02).
- Providers see uploaded documents (for reference).
- Providers view configured commission rates and payout frequency (read-only) in the FR-032 Screen 4 Commission & Payout panel.
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
- Mandatory cancellation notifications to affected patients and support alerts to admins when provider status changes cancel cases. Patient messages must explain the provider-related cancellation and direct the patient to contact admins; the optional provider-email checkbox does not disable these notifications.

**Out of Scope**:

- Document verification workflow (documents are for record-keeping only)
- "Save as Draft" functionality

### Entry Points

- **Admin-Initiated**: Admin accesses "Provider Management" section in Admin Platform dashboard → selects "Add New Provider" to initiate provider creation workflow
- **Admin Oversight**: Admin opens "Providers" list view to see all providers across all statuses (active, suspended, deactivated) with filtering and search
- **Provider Profile Access (Provider-Side)**: Provider logs into Provider Platform → views account status (FR-032 Rule 6 banner when Suspended), uploaded documents (FR-032 Tab 6: Documents), and commission configuration read-only in FR-032 Screen 4: Billing Settings (Commission & Payout panel, Owner role only)

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
   - Selects payout frequency (Weekly, 2x a Month, or Monthly; required)
   - Sets commission start date (required; today or a future date); this is the configuration's FR-029 Effective Date for newly confirmed bookings
9. Admin reviews all entered information in summary view (Step 6).
10. Admin clicks "Create Provider" button.
11. System validates every field marked Required in the Screen 2 wizard tables (see Rule 2).
12. System creates provider record with status = "Active" and initializes provider credentials with `password_set = false`. Until the password is set, the provider is excluded from inquiry distribution (Rule 3). The admin sees the success message: "Provider [Clinic Name] created successfully. An activation email has been sent to [email]."
13. System sends the account activation email (FR-020 `provider.activation`; mandatory and cannot be disabled) to provider with:
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
  3. Cancel that provider's currently available unaccepted Parent Quotes once each with the FR-004 status `cancelled_provider_status`; their package/date alternatives become unavailable. Close every non-terminal booking of that provider before treatment starts (FR-006 booking stages `Accepted`, including unpaid within the payment hold, and `Confirmed`) through FR-006 Alternative Flow B4, which releases any active appointment hold or reservation and hands the booking to the provider-fault transfer in FR-006 Alternative Flow B5. A booking in the FR-006 `In Progress` stage is not closed: it stays `In Progress`, keeps its treatment record, and receives the provider-status cause and the support marker. An admin decides case by case on FR-006 Screen 6 whether to move the booking to `Aftercare` and reassign the aftercare provider (FR-006 Alternative Flow B6) or to cancel the booking with a mandatory reason; there is no replacement acceptance, and money stays with the payment FRs. A booking in the FR-006 `Aftercare` stage is not closed: it keeps its status and treatment record, receives the provider-status cause and the support marker, and moves to the aftercare reassignment in FR-006 Alternative Flow B6, with no new acceptance and no new payment. An accepted Parent Quote keeps its `accepted` status and is never moved to a cancelled quote status. The FR-005 AcceptanceEvent and accepted snapshot stay unchanged and are superseded only through a linked FR-005 supersession record. FR-011 standalone aftercare cases assigned to this provider have no accepted Subquote; they are not cancelled either; they receive the same cause and support marker, and an admin reassigns them through the FR-011 aftercare reassignment screen. Accepted quote history belonging to Completed/already-terminal cases is not reclassified.
  4. Record `cancellationReason = ProviderSuspended` and `supportRequired = true` on affected cases and inquiry context. If the inquiry's accepted booking belongs to this provider, the inquiry is not cancelled; before treatment starts it stays open so that an admin can rehome the patient to a replacement provider in the same inquiry through FR-006 Alternative Flow B5, and for an `In Progress` booking it stays open for the admin decision described in step 3. If the inquiry is still comparing providers, cancel only the suspended provider's participation/quotes and flag the inquiry for support; unrelated providers' offers remain available.
  5. Notify affected patients that the provider is unavailable. A patient whose unaccepted offer was cancelled is told the offer is no longer available and is given a Contact Admin/Support action (FR-020 `provider.status_cancellation_patient`, used only before acceptance). A patient whose accepted booking was closed is told that an admin will arrange a replacement provider within the same inquiry (FR-020 `booking.provider_fault_replacement`). A patient whose `In Progress` or `Aftercare` booking stays open keeps the booking; when the admin reassigns aftercare, FR-011 sends the mandatory `aftercare.provider_reassigned` notice to the patient and the new aftercare provider (FR-020). Alert admins and make the affected records identifiable in the existing patient-management/support workflow.
  6. Record the provider status event, affected record identifiers, prior stages, cancellation reason, slot release, support marker, and notification outcomes in the audit trail. Repeated processing must not duplicate cancellations or support alerts for the same event/case.
  7. For each closed accepted booking, an admin opens Start Provider-Fault Transfer on FR-006 Screen 6 (which opens FR-006 Screen 10), selects a replacement provider in the same inquiry, and authors a replacement quote through FR-006 Alternative Flow B5; the confirmed selection is recorded as a new admin-authored acceptance record linked to the original; the patient re-enters nothing. Money follows the FR-006 Alternative Flow B5 payment placeholder (paid amounts move with the patient as credit toward the replacement booking, any unused part is refunded, and the patient pays no fee); exact mechanics belong to the payment FRs. Clinical continuity and other patient assistance use the existing owning FRs. For each `In Progress` booking, an admin opens the booking on FR-006 Screen 6 and either moves it to `Aftercare` with an aftercare reassignment or cancels it with a mandatory reason. For each Aftercare booking, an admin opens Reassign Aftercare on FR-006 Screen 6, which links to the FR-011 aftercare reassignment screen, and assigns another provider or the Hairline aftercare team with a mandatory reason, confirmation, and audit entry (FR-006 Alternative Flow B6). Cancelled cases and quotes are not automatically restored if the provider is later reactivated.
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

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Search Bar | text | No | Free-text search by provider name, clinic name, email, license number | Max 200 chars |
| Status Filter | multi-select dropdown | No | Filter providers by status (Active, Suspended, Deactivated) | Multiple selections allowed |
| Featured Filter | checkbox | No | Filter to show only featured providers | Boolean toggle |
| Commission Type Filter | select | No | Filter by commission structure (Percentage, Flat Rate, All) | Single selection |
| Closure Requested Filter | checkbox | No | Show only providers with a pending FR-032 account-closure request (status Pending Admin Review) | Boolean toggle |
| Date Range Filter | date range picker | No | Filter by provider creation date or Last Activity Date. Last Activity Date is system-derived: the most recent of the provider's last FR-004 Parent Quote submission and last FR-006 booking confirmation (empty if neither has occurred) | Valid date range required; providers with no Last Activity Date are excluded when filtering by it |
| Status Count Tiles | display | N/A | Counts of Active, Suspended, and Deactivated providers shown above the table (SC-012) | System calculated from provider status; counts all providers regardless of active filters; refresh with real-time status updates |
| Provider List Table | data table | N/A | Displays provider rows with columns: Name, Clinic, Status, Featured, Commission Rate, Created Date, Actions | Paginated (50 rows per page) |

**Business Rules**:

- **Default View**: Dashboard displays all providers with status = "Active" by default on initial load
- **Search**: Search queries match against provider name, clinic name, email, medical license number (case-insensitive)
- **Status Badge Colors**: Active (green), Suspended (yellow), Deactivated (red)
- **Featured Badge**: Gold star icon displayed next to provider name if featured = true
- **Quick Actions**: Each row includes action buttons: "View Profile", "Edit", "Set Featured" (if active and not featured), "Unset Featured" (if featured), "Suspend" (if active), "Reactivate" (if suspended; opens Screen 5), "Deactivate" (if active/suspended), "Cancel Scheduled Change" (if a scheduled suspension/deactivation is pending)
- **Closure Requested Marker**: Rows with a pending FR-032 account-closure request show a "Closure Requested — DD-MM-YYYY" badge (request date) next to the status badge, linking to the request in the provider profile (A7). While a deactivation scheduled from the request is pending, the badge reads "Closure requested, deactivation scheduled DD-MM-YYYY" (Effective Date). The marker clears when the request is Approved (the deactivation has taken effect) or Rejected
- **Scheduled Change Marker**: Rows with a pending scheduled status change show "Scheduled: Suspend on DD-MM-YYYY" or "Scheduled: Deactivate on DD-MM-YYYY" next to the status badge
- **Sorting**: Table columns sortable by name (alphabetical), created date (chronological), and commission rate. Commission rate sorting groups by model: all Percentage providers first, ordered by percentage value, then all Flat Rate providers, ordered by Flat Rate Currency (ISO code) and then amount. Descending order reverses the value order within each group; amounts in different currencies are never compared. A provider on the FR-029 global default sorts by the default value, in the group of the default model
- **Commission Rate Column**: Shows the provider's current effective commission. A provider on the FR-029 global default shows the default rate with "(Default)", for example "15% (Default)". A provider whose only provider-specific configuration is future-dated shows its current effective rate (the global default until the Effective Date) plus a "Scheduled" tag
- **Pagination**: Display 50 providers per page, with page navigation controls

**Notes**:

- Use color-coded status badges for quick visual scanning
- Featured providers should have prominent visual indicator (star icon)
- Ensure "Add New Provider" button prominently displayed in top-right corner
- Implement real-time status updates (e.g., if provider status changes, table refreshes without full page reload)

---

### Screen 2: Provider Creation Wizard

**Purpose**: Allows admins to create new provider accounts through a structured, multi-step wizard process. The wizard interface is used for creation; editing uses the tabbed interface (Screen 3).

**Cross-Module Alignment**: This screen's data structure aligns with **FR-032: Provider Dashboard Settings & Profile Management**. All profile fields (Bio, Languages, Awards, Profile Picture, Contact details) must stay synchronized between Admin (A-02) and Provider (PR-06) platforms. When providers edit these fields via FR-032, changes are immediately reflected in the admin view.

**Wizard Steps**:

#### Step 1: Basic Information

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Profile Picture / Logo | file upload | No | Provider's photo or clinic logo (aligns with FR-032 Tab 1) | Max 5MB, JPEG/PNG, min 200x200px, recommended 500x500px |
| Cover Image | file upload | No | Large banner image for clinic profile (aligns with FR-032 Tab 1) | Max 10MB, JPEG/PNG, recommended 1920x300px |
| First Name | text | Yes | Provider's legal first name | Max 50 chars |
| Last Name | text | Yes | Provider's legal last name | Max 50 chars |
| Email Address | email | Yes | Primary email (login ID) | Valid email; must satisfy the FR-009 global provider email identity rule (Rule 3, REQ-009-008): not used by another provider organization as Owner, team member, or pending invitation; Deactivated providers' emails are freed for reuse |
| Phone Number | phone | Yes | Contact phone with country code | Valid format |
| Bio / Description | textarea | Yes | Public-facing provider biography (aligns with FR-032 Tab 1 "About/Description") | Max 500 chars, min 50 chars |
| Seat Limit | number | No | Maximum number of team members (staff) the provider can invite (aligns with FR-009 team management). Seat usage counts accepted non-Owner team members plus invitations still pending; the Owner and expired invitations do not count | Integer, range 1-500, default: 100. Can be adjusted later by admin if provider requests increase |

#### Step 2: Professional Details

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Specialty | select | Yes | Primary medical specialty | Values from the centrally managed Provider Specialties list (FR-026 Screen 5f); active values only |
| Medical License Number | text | Yes | License identifier (for record) | Max 50 chars |
| Years of Experience | number | Yes | Years practicing | Numeric, 0-60 |
| Languages Spoken | multi-select chip/pill | Yes | Languages spoken at clinic (aligns with FR-032 Tab 2) | At least 1 language required; consumes the central language catalog owned by FR-021 (Multi-Language & Localization) |
| Awards & Recognition | dynamic list | No | List of awards (aligns with FR-032 Tab 4) | Each award: name (max 100 chars), issuer/organization (max 150 chars, optional), description (max 300 chars), year (1900-current), award image (max 2MB, JPEG/PNG) |

#### Step 3: Clinic Information

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Clinic Name | text | Yes | Name of practice/clinic (aligns with FR-032 Tab 1) | Min 3, max 200 chars |
| Clinic Address | address | Yes | Full physical address (admin-only record) | Google Places or manual entry |
| Contact Email | email | Yes | Public clinic contact email shown on provider profile (aligns with FR-032 Tab 1 "Contact Email") | Valid email format; unique among Active and Suspended providers (Deactivated records ignored) |
| Location - City | text | No | Public display city shown to patients (aligns with FR-032 Tab 1); pre-filled from Clinic Address and editable separately | Max 100 chars |
| Location - Country | dropdown | No | Public display country shown to patients (aligns with FR-032 Tab 1); pre-filled from Clinic Address and editable separately | Values from centrally managed country list (FR-026) |
| Contact Phone (Public) | phone | No | Public clinic phone number (aligns with FR-032 "Contact Phone (Public)") | Contains Country Code (dropdown, FR-026) and Number (numeric only, length validated per country code) |
| Website URL | url | No | Public-facing clinic website (aligns with FR-032 Tab 1) | Valid URL format (http/https); auto-prepends https:// if protocol missing |
| Operating Hours | text | No | e.g., "Mon-Fri 9am-5pm" | Free text |

#### Step 4: Documents (Record Keeping)

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Medical License | file upload | Yes | Copy of license (stored as document type "Medical License", uploaded by Admin) | PDF, JPG, PNG, DOCX, XLSX; Max 10MB (same as FR-032 Tab 6) |
| Board Certification | file upload | No | Copy of certification (type "Board Certification") | PDF, JPG, PNG, DOCX, XLSX; Max 10MB |
| Insurance Certificate | file upload | No | Proof of malpractice insurance (type "Malpractice Insurance") | PDF, JPG, PNG, DOCX, XLSX; Max 10MB |

*Note: The Medical License file is required to complete the wizard as a record-keeping baseline. Documents are pre-verified outside the system; the system never checks document authenticity or status, and later document changes never alter provider status.*

#### Step 5: Commission & Settings

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Commission Model | radio | Yes | "Percentage" or "Flat Rate" | Default: Percentage |
| Commission Value | number | Yes | % or Fixed Currency Amount | 0-100 with 0.1% precision (if %) or >0 in the Flat Rate Currency's minor units (if Flat), per FR-029 |
| Flat Rate Currency | select | Conditional | Currency of the Flat Rate amount (aligns with FR-029 Screen 5 "Flat Rate Currency") | Required when Commission Model = Flat Rate; values from the FR-029 enabled currency list; defaults to the system default currency; hidden for Percentage |
| Payout Frequency | radio | Yes | How often the provider is paid out (definitions in Screen 3 Tab 7) | One of: "Weekly", "2x a Month", "Monthly"; no preselected value |
| Commission Start Date | date | Yes | Effective date of this commission configuration for newly confirmed bookings; stored as the FR-029 provider-specific commission Effective Date (`effective_date`). Payout cycles follow the Payout Frequency period definitions, not this date | Format: DD-MM-YYYY; today (current UTC date) or a future date |
| Featured Provider | toggle | No | Highlight in patient search | Default: Off; subject to the 10-provider cap (Rule 8) |

#### Step 6: Review & Create

- **Read-only Summary**: Displays all entered data for final review.
- **Actions**:
  - "Back": Navigate to previous steps.
  - "Create Provider": Finalizes creation and sets status to **Active**.

**Leaving the wizard**: The wizard does not save drafts. If the admin has entered any data and tries to leave the wizard before "Create Provider" succeeds (in-app navigation, browser Back, or closing/reloading the tab), the system shows the FR-032 unsaved-changes message text, "You have unsaved changes. Are you sure you want to leave?", with only "Stay" and "Leave" actions. The FR-032 Save option is not offered, because the wizard has no drafts. "Leave" discards all entered data; for tab close or reload the browser's native leave-page prompt is used.

**Upload error messages**: Every admin file upload in this FR (wizard Steps 1, 2 and 4, the profile images and award images on the provider detail tabs, and the Tab 6 Upload Document modal and Replace) validates the file before saving it and shows one inline message under the field. The file is not saved.
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
  - "Edit Profile" (opens all tabs in edit mode)
  - "Resend Activation Email" (requires the FR-031 Edit Providers permission; visible only if password not yet set and status = Active, so it is hidden for Suspended and Deactivated providers, matching Alternative Flow A1; sends new one-time password setup link)
  - "Suspend/Deactivate" (status management; opens Screen 4)
  - "Reactivate" (visible only if Suspended; opens Screen 5)
  - "Cancel Scheduled Change" (visible only if a scheduled suspension/deactivation is pending; see Screen 4)
  - "Login as Provider" (Super Admin only, for support/debugging; available when the provider is Active or Suspended, not when Deactivated)

**Login as Provider rules**:

- Login as Provider is allowed when the provider is Active or Suspended. It is blocked when the provider is Deactivated, with the message: "Login as Provider is not available for a deactivated provider." These rules apply both to impersonating the Owner and to impersonating a team member (FR-009 REQ-009-023).
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

| Field Name | Type | Required | Description | Validation Rules | Admin/Provider Editable |
|------------|------|----------|-------------|------------------|------------------------|
| Profile Picture / Logo | image upload | No | Clinic branding image | Max 5MB, JPEG/PNG, min 200x200px, recommended 500x500px | Both (Provider via FR-032) |
| Cover Image | image upload | No | Large banner image for clinic profile | Max 10MB, JPEG/PNG, recommended 1920x300px | Both (Provider via FR-032) |
| First Name | text | Yes | Provider's legal first name | Max 50 chars | Admin only |
| Last Name | text | Yes | Provider's legal last name | Max 50 chars | Admin only |
| Email Address | email | Yes | Primary email (login ID) | Valid email; must satisfy the FR-009 global provider email identity rule (Rule 3, REQ-009-008) (re-checked whenever changed); Deactivated providers' emails are freed for reuse | Admin only |
| Phone Number | phone | Yes | Primary contact phone | Valid format with country code | Admin only |
| Bio / Description | textarea | Yes | Public-facing provider biography | Max 500 chars, min 50 chars | Both (Provider via FR-032) |
| Specialty | select | Yes | Primary medical specialty | Values from the centrally managed Provider Specialties list (FR-026 Screen 5f); a stored value later deactivated in FR-026 still displays but cannot be newly selected | Admin only |
| Medical License Number | text | Yes | License identifier (for record) | Max 50 chars | Admin only |
| Years of Experience | number | Yes | Years practicing | Numeric, 0-60 | Admin only |
| Clinic Name | text | Yes | Name of practice/clinic | Min 3, max 200 chars | Both (Provider via FR-032) |
| Clinic Address | address | Yes | Full physical address | Google Places or manual entry | Admin only |
| Location - City | text | No | City where clinic is located | Max 100 chars | Both (Provider via FR-032) |
| Location - Country | dropdown | No | Country where clinic is located | Values from FR-026 country list | Both (Provider via FR-032) |
| Contact Phone (Public) | phone | No | Public clinic phone number | Country Code dropdown + Number | Both (Provider via FR-032) |
| Contact Email | email | Yes | Public clinic contact email (captured in Screen 2 Step 3) | Valid email format; unique among Active and Suspended providers, Deactivated records ignored (re-checked whenever changed, per FR-032) | Both (Provider via FR-032) |
| Website URL | url | No | Public-facing clinic website | Valid URL, auto-prepends https:// | Both (Provider via FR-032) |
| Operating Hours | text | No | Operating hours (e.g., "Mon-Fri 9am-5pm") | Free text | Admin only |
| Seat Limit | number | No | Maximum team members (staff) capacity. Seat usage counts accepted non-Owner team members plus invitations still pending; the Owner and expired invitations do not count | Integer, range 1-500, default 100 | Admin only |
| Commission Summary | display | N/A | Read-only summary of the current commission configuration (model, value, Flat Rate Currency when applicable, Effective Date) and payout frequency, with a "Manage in Commission & Financials" link to Tab 7. A provider on the FR-029 global default shows the default rate with "(Default)", for example "15% (Default)"; a provider whose only provider-specific configuration is future-dated shows its current effective rate plus a "Scheduled" tag | Retrieved from Tab 7 (FR-029 provider-specific configuration or global default); not editable in this tab | Read-only |
| Featured Provider | toggle | No | Admin-only control, positioned at the bottom of Basic Information, to highlight in patient search | Boolean, default: Off; maximum 10 featured providers; only for Active providers; cleared automatically on suspension or deactivation (Rule 6) | Admin only |
| Status | badge/display | Yes | Provider account status | Enum: Active, Suspended, Deactivated | Admin only |
| Completed Procedures | display | No | Count of distinct procedures that reached FR-010 treatment completion for this provider | One count per completed procedure, not per Parent Quote, option, date alternative, or installment | Read-only |
| Average Rating | display | No | Average rating from patient reviews | Read-only, format: X.X/5.0 stars | Read-only |

**Business Rules**:

- Fields marked "Both" can be edited by provider via FR-032 and changes sync to admin view in real-time
- Fields marked "Admin only" can only be edited by admin users with provider management permissions
- Profile changes logged in audit trail with timestamp, user, and changed fields
- **Admin change reason**: When an admin saves changes to any provider data (Tabs 1, 2, 4, 6 notes, and 7), the system requires a "Reason for change" (min 10 chars, max 500 chars) before saving. The reason is stored with the audit entry and shown in Tab 8. Provider self-edits via FR-032 do not require a reason. Exception: the Featured Provider toggle (and the Provider-list Set/Unset Featured quick actions) never asks for a reason; the change is still logged in Tab 8.
- Current profile edits must not alter an FR-005 accepted snapshot, historical appointment/price/package context, or an FR-006 booking commission snapshot. This does not prevent normal current-profile synchronization with FR-032.
- Completed Procedures uses the FR-010 treatment-completion milestone, not acceptance, payment confirmation, or final aftercare completion. Cancellation during Aftercare must not erase an already recorded completed procedure; no new procedure-completion rule is introduced here.
- Commission is edited only in Tab 7; Tab 1 shows it read-only.
- **Owner login email change**: Changing the Email Address (the Owner's login ID) requires admin password re-authentication and a reason (the admin change reason above). The Owner does not confirm the new address. On save, the system:
  - sends a notice to the old address saying the login email was changed, and a notice to the new address;
  - signs the Owner out of all sessions and revokes the Owner's tokens;
  - if `password_set` is false, invalidates the pending activation link and sends a new activation email (FR-020 `provider.activation`) to the new address.
- Seat Limit changes require admin re-authentication for security. In MVP this is implemented as password re-entry; once the shared MFA stack from FR-026 / FR-031 is delivered, these actions MUST use MFA-based re-authentication and any MFA references in this FR are to be understood as future (non-MVP) behavior.

**Notes**:

- Admin view includes all provider profile fields plus admin-only settings (Seat Limit, Status) and a read-only Commission Summary
- Provider-editable fields sync bidirectionally with FR-032
- Admin can override any provider changes if needed (logged in audit trail)

---

#### Tab 2: Languages

**Purpose**: View and manage languages spoken at the clinic. Mirrors FR-032 Tab 2 structure.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Admin/Provider Editable |
|------------|------|----------|-------------|------------------|------------------------|
| Supported Languages | chip/pill list | Yes | Languages spoken at clinic | At least 1 language required; consumes the central language catalog owned by FR-021 (Multi-Language & Localization) | Both (Provider via FR-032) |

**Business Rules**:

- Languages displayed as removable chips/pills with X button on each chip
- Admin can add/remove languages; provider can also manage via FR-032 Tab 2
- At least 1 language must be selected (validation prevents removing last language); attempting to save with none shows: "At least one language is required."
- Changes logged in audit trail with timestamp and user
- Language list consumed from the FR-021 central language catalog; chips mean languages spoken at the clinic, not UI language

**Notes**:

- Admin view identical to FR-032 Tab 2 (same interface, same functionality)
- Changes made by provider in FR-032 reflect immediately in admin view
- Drag-and-drop reordering supported to prioritize languages

---

#### Tab 3: Staff List

**Purpose**: View and manage this provider's clinic staff members and team roles (admin view), including inviting new staff.

**Implementation**: This tab embeds **FR-009: Provider Team & Roles Management > Screen 12: Provider Team (Admin, Single Provider)**, filtered to this provider only. Team members of other providers are never shown here; the cross-provider directory remains FR-009 Screen 10.

**Business Rules**:

- Lists this provider's team members with name, email, role, ownership flag, status, and last login (fields and actions per FR-009).
- "Invite Staff Member": admin enters an email and selects one of the provider's existing roles (not Owner); the invitation uses FR-009's normal invitation email, acceptance, and expiry flow.
- Invite is blocked when the provider's Seat Limit (Rule 7) is reached and when provider status is Suspended or Deactivated.
- Requires the FR-031 "Edit Providers" permission; the invite and the inviting admin are logged in FR-009's audit trail and Tab 8.
- Existing FR-009 admin actions (force suspend member, reset invitation, view audit log, impersonate) remain available.

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

**Purpose**: Browse this provider's reviews with filtering and sorting, and launch FR-013 admin review management actions (insert authenticated off-platform reviews, edit, remove) for this provider. Display mirrors FR-032 Tab 5; review management behavior is owned by **FR-013: Reviews & Ratings**.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Admin/Provider Editable |
|------------|------|----------|-------------|------------------|------------------------|
| Overall Rating Summary | display | No | Average rating and total review count | Read-only; calculated from Reviews service | Read-only |
| Rating Distribution | bar chart | No | Percentage/count visualization for 5★ through 1★ reviews | Read-only; calculated from Reviews service | Read-only |
| Review List | list | No | List of individual patient reviews with rating, comment, date, patient name | Read-only; sourced from Reviews service | Read-only |
| Rating Filters | checkbox/pill | No | Filter reviews by rating (5★, 4★, 3★, 2★, 1★) | Multiple selections allowed | Interactive filter |
| Add Review Button | button | No | Opens FR-013 Screen 8 (Admin – Review Detail, Insert & Edit) in insert mode, pre-scoped to this provider, to add an authenticated off-platform review | Admin users with review management permission | Admin only |
| Review Actions | button group | No | Per review: "Edit" or "Remove" opens FR-013 Screen 8 for that review | Rules, validation, and audit owned by FR-013 | Admin only |

**Business Rules**:

- Reviews displayed with: star rating, patient name (anonymized if requested), date, review text
- Admin can filter by rating, search by keyword, sort by date/rating
- Admin insert, edit, and remove actions follow FR-013 (including the "Verified Off-platform" label, verification source/date, and audit trail); FR-015 does not define its own review editing rules
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

| Field Name | Type | Required | Description | Validation Rules | Admin/Provider Editable |
|------------|------|----------|-------------|------------------|------------------------|
| Upload Document Button | button | No | Admin action to upload additional documents | Opens the Upload Document modal (fields below) | Admin only |
| Document List | list/cards | No | List of all provider and admin-uploaded documents | Displays: document name, type, upload date, file size, uploaded by (Provider/Admin) | View-only for admin; sortable/filterable |
| Document Name | text (display) | N/A | Filename of uploaded document | Auto-generated from file; max 200 chars | Display only |
| Document Type | badge (display) | N/A | Type of document | Enum: Medical License, Board Certification, Insurance (general), Malpractice Insurance, Business License, Other | Display only |
| Upload Date | datetime (display) | N/A | When document was uploaded | Auto-generated timestamp; format: "MMM DD, YYYY HH:mm" | Display only |
| Uploaded By | badge (display) | N/A | Who uploaded document: "Provider" or "Admin [Name]" | Badge displays "Provider" for provider uploads, "Admin - [admin name]" for admin uploads | Display only |
| File Size | text (display) | N/A | Document file size | Format: "X.X MB" or "X KB" | Display only |
| Notes | text (display/edit) | No | Optional notes about document | Max 500 chars; admin can add/edit notes | Admin editable (via "Edit Notes" action) |
| Actions | button group | No | View, Download, Replace, Delete actions | Context menu or action buttons per document | Admin only (view/download/replace/delete) |

**Upload Document Modal Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| File | file upload | Yes | Document file received from the provider via an external channel | Formats: PDF, JPG, PNG, DOCX, XLSX; max 10MB |
| Document Type | dropdown | Yes | Type of document (admin selects) | Enum: Medical License, Board Certification, Insurance (general), Malpractice Insurance, Business License, Other |
| Notes | textarea | No | Optional notes about the document | Max 500 chars |

On save, Document Name, File Size, Upload Date, and Uploaded By ("Admin - [admin name]") are set by the system.

**Business Rules**:

- **Provider Document Management**: Providers upload, replace, delete their documents via **FR-032 Tab 6: Documents**. Provider-uploaded documents sync to FR-015 within 1 minute
- **Admin Oversight**: Admins can view all provider-uploaded documents for compliance and oversight purposes
- **Admin Additional Uploads**: Admins can upload additional documents received externally (e.g., documents sent via email, postal mail, scanned at in-person meeting). These admin-uploaded documents display "Admin - [admin name]" badge
- **Document Permissions**:
  - Provider-uploaded documents: Admin can view, download, add notes, but **cannot replace or delete** (only provider can via FR-032)
  - Admin-uploaded documents: Admin has full control (view, download, replace, delete, add notes)
  - **Replace**: Replacing a document uploads the new file as the current version and archives the old file (soft-deleted and retained per the Soft Delete rule, logged in Tab 8). Replace does not require an admin change reason
- **Document Requirements**: A Medical License file is required once, when completing the Screen 2 wizard. After creation, the absence, replacement, or deletion of any document never changes provider status or blocks activity
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

> **Note on screen label**: This tab appears under the heading **"Affiliate Pay Details"** in the current design screen. This is a legacy mislabeling — the correct scope is provider commission and payout schedule configuration. It does not relate to affiliates. The admin transcript (Hairline-AdminPlatform-Part1) describes this payout-frequency and amount-or-percentage pattern for both providers and affiliates; Product Owner decision (2026-10-14): it applies to both — providers here, and affiliates in FR-018 (Percentage or Fixed Amount, monthly-only payout per the client).

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Admin/Provider Editable |
|------------|------|----------|-------------|------------------|------------------------|
| Commission Model | radio (display/edit) | Yes | "Percentage" or "Flat Rate" | Default: Percentage | Admin only (edit) |
| Commission Value | number (display/edit) | Yes | % or Fixed Currency Amount | 0-100 with 0.1% precision (if %) or >0 in the Flat Rate Currency's minor units (if Flat), per FR-029 | Admin only (edit) |
| Payout Frequency | radio (display/edit) | Yes | How often this provider receives payouts (set in Screen 2 Step 5). Period definitions: **Weekly** = Monday to Sunday; **2x a Month** = 1st–15th then 16th–last day of month; **Monthly** = full calendar month | One of: "Weekly", "2x a Month", "Monthly" | Admin only (edit) |
| Flat Rate Currency | select (display/edit) | Conditional | Currency of the Flat Rate amount (aligns with FR-029 Screen 5) | Required when Commission Model = Flat Rate; FR-029 enabled currency list; defaults to the system default currency | Admin only (edit) |
| Commission Start Date / Effective Date | date (display/edit) | Yes | Date from which the commission configuration applies to newly confirmed bookings (FR-029 `effective_date`). First set in Screen 2 Step 5; every later model, value, or currency edit sets its own Effective Date. Payout cycles follow Payout Frequency, not this date | Format: DD-MM-YYYY; today or a future date, where "today" is the current UTC date | Admin only (edit, with change reason) |
| Featured Provider | display | N/A | Current featured status; managed from the Provider-list quick action or the Basic Information toggle | Read-only | Display only |
| Current Configuration | display | N/A | Summary of commission configuration applicable to newly confirmed bookings and current payout frequency | Examples: "15% · Paid Weekly (Mon–Sun)" or "£200 per completed procedure · Paid Weekly (Mon–Sun)"; indicate that existing bookings retain their confirmation-time snapshot | Display only |
| Scheduled Configuration | display | N/A | The pending future-dated commission configuration (model, value, Flat Rate Currency, Effective Date), if one exists, with a "Cancel Scheduled Configuration" action | Hidden when none is pending; at most one per provider; cancellation requires a change reason and re-authentication | Display only (cancel: Admin only) |
| Commission History | list | No | Audit log of past commission and payout setting changes | Each entry: date, admin user, old value, new value, reason | Display only |

**Business Rules**:

- Commission configuration displayed prominently with current model, value, and payout frequency
- **Edit eligibility**: Commission settings and payout frequency can be edited for Active and Suspended providers (so terms can be fixed before reactivation). For Deactivated providers Tab 7 is read-only; history stays visible. FR-029 Screen 5 applies the same rule (CR-FR029-20261015-02). When a deactivation takes effect, the system automatically cancels any pending Scheduled Configuration and logs the cancellation in Commission History
- Admin can edit commission settings and payout frequency (requires re-authentication). In MVP this is implemented as password re-entry; once the shared MFA stack from FR-026 / FR-031 is delivered, these actions MUST use MFA-based re-authentication and any MFA references in this FR are to be understood as future (non-MVP) behavior.
- FR-029 / A-09 owns the central commission-settings screen (global default + provider-specific commission scopes) and the booking-time snapshot policy; this tab remains the single-provider management surface for provider-specific commission configuration and owns payout frequency used by FR-017
- Commission edits apply to bookings confirmed after the configuration becomes effective, not to every later payment transaction. Resolve the effective provider-specific configuration (or global default) and snapshot its model/value (and Flat Rate currency) at FR-006 booking confirmation under FR-029. Until a new configuration's Effective Date, the previous configuration remains effective. Existing confirmed bookings retain that snapshot for subsequent installments, deductions, and payout reconciliation.
- Patient price/currency/exchange-rate context is locked at FR-005 acceptance; commission is locked at booking confirmation; nothing is fixed at quote creation. An accepted-but-unpaid selection has not yet fixed its commission snapshot. The Percentage and Flat Rate models remain unchanged; a flat fee remains one deduction per completed procedure, not one per package, Subquote, or installment.
- **Scheduled configuration**: "Today" means the current UTC date (the same calendar used by the midnight UTC jobs). An edit with an Effective Date of today applies immediately to newly confirmed bookings. An edit with a future Effective Date is stored as the provider's Scheduled Configuration; at most one may be pending per provider. Saving another future-dated edit replaces the pending one (the replacement is logged in Commission History with both values). On its Effective Date the scheduled configuration becomes the current configuration automatically. The pending configuration is shown read-only to the provider in the FR-032 Screen 4 Commission & Payout panel.
- Payout frequency changes take effect from the next billing cycle — the current in-progress cycle is not affected
- Changes made to provider-specific commission values here MUST stay synchronized with the provider-specific commission data shown in FR-029 Screen 5 for the same provider
- **Shared FR-029 scopes**: A provider belongs to at most one active provider-specific commission scope. If this provider is currently covered by an FR-029 scope shared with other providers, saving a commission edit here removes this provider from that shared scope and creates a single-provider scope for it with the new values; the other providers in the shared scope are unchanged. The tab warns the admin before saving, and the split is logged in Commission History and the FR-029 audit trail.
- All changes to commission and payout frequency logged in history with timestamp, admin user, old/new values
- Provider can view commission model, value, Flat Rate Currency, Effective Date, and payout frequency read-only in the FR-032 Screen 4 Commission & Payout panel (but not edit)
- FR-017 reads the payout frequency set here to determine when to generate payout statements for this provider

**Notes**:

- This tab is admin-only; provider sees commission rate and payout frequency read-only in the FR-032 Screen 4 Commission & Payout panel
- Commission and payout frequency changes require admin justification (logged in audit trail)
- Use FR-015 when the admin is working provider-by-provider; use FR-029 for central or bulk commission-scope administration

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
- Suspension/deactivation entries must link the affected case/inquiry references, prior stages, cancellation causes, support markers, slot-release results, and notification outcomes. Display `Admin Support Required` for unresolved provider-caused cancellations with a link to the existing FR-016 patient intervention/support context; do not add a case-management editor to this tab.
- Admin can filter by action type, date range, user
- Admin can export the activity log for compliance reporting as a CSV file of the rows matching the current filters. Export is available to every admin who can view Tab 8 (FR-031 View Providers). IP addresses are included unmasked. The export action itself is logged in Tab 8

**Notes**:

- This tab is admin-only and provides full transparency of provider account changes
- Logs help with compliance, security investigations, and dispute resolution

---

### Screen 4: Provider Suspension/Deactivation Modal

**Purpose**: Captures the admin reason and affected-case impact before suspending/deactivating a provider, with accountable cancellation and patient/admin support handoffs

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Action Type | text (display only) | N/A | Shows "Suspend Provider" or "Deactivate Provider" as modal title | Display only |
| Provider Name | text (display only) | N/A | Confirms which provider is being suspended/deactivated | Display only |
| Affected Cases & Quotes | read-only summary/list | N/A | Shows outstanding Parent Quotes and affected cases with links, prior stages, and the cancellation/support impact of the selected action | Suspension and deactivation both include Accepted, Confirmed, In Progress, and Aftercare (In Progress cases are shown as staying open for an admin decision and Aftercare cases as moving to aftercare reassignment; neither is closed); terminal history is not reclassified; revalidate at effective time |
| Reason | textarea | Yes | Admin must provide detailed reason for suspension/deactivation | Min 20 chars, max 500 chars |
| Notify Provider | checkbox | No | Option to send notification email to provider with reason | Default checked (true); checked and locked when deactivating from an account-closure request (A7); does not disable mandatory patient cancellation messages or admin support alerts |
| Effective Date | date picker | No | Optional. Blank or today applies the change immediately on submit; a future date schedules it | Must be today or future date; "today" is the current UTC date |
| Admin Password | password | Yes | Re-authentication before the status change (MFA once FR-026 / FR-031 MFA stack is delivered) | Must match the acting admin's password |
| Confirm Action | checkbox | Yes | Admin must check "I confirm this action" before submitting | Must be checked to enable submit button |

**Business Rules**:

- **Required Reason**: Admin cannot suspend or deactivate provider without providing detailed reason (minimum 20 characters)
- **Suspension vs. Deactivation**:
  - **Suspension**: Temporary status change; provider account remains in system and can be reactivated later
    - Block new inquiry allocations, quote submissions, patient acceptances, and further payment against this provider's affected selections as soon as suspension is effective.
    - Automatically cancel this provider's outstanding unaccepted quotes (FR-004 `cancelled_provider_status`) and close all related non-terminal bookings in the FR-006 booking stages `Accepted` or `Confirmed`, using Alternative Flow A5. `In Progress` bookings are not closed; they stay `In Progress` with the support marker until an admin moves them to `Aftercare` with aftercare reassignment or cancels them with a reason. Closed accepted bookings enter the FR-006 provider-fault transfer (Alternative Flows B4 and B5), where an admin rehomes the patient to a replacement provider in the same inquiry. `Aftercare` bookings and FR-011 standalone aftercare cases assigned to this provider are not closed; they move to aftercare reassignment (FR-006 Alternative Flow B6 and FR-011). Existing upcoming bookings do not remain active with this provider.
    - Record `ProviderSuspended` as the cancellation reason and `supportRequired = true`; display `Cancelled — Provider Suspended` with a separate `Admin Support Required` marker on affected cases and affected inquiries. In Progress and Aftercare cases keep their status and show the `Admin Support Required` marker with the provider-status cause. An inquiry with a closed accepted booking stays open for the replacement-provider transfer and is not cancelled. For shared unaccepted inquiries, preserve the inquiry's normal stage and other providers' offers while flagging the suspended provider's participation and support need.
    - Provider can still log in to Provider Platform but sees "Account Suspended" banner; the same applies to all of the provider's FR-009 team members. The banner and the suspended read-only behavior are specified in FR-032 (Rule 6). Read-only includes `In Progress` bookings: the suspended provider cannot check in, end treatment, or edit the treatment plan; the admin decides the case through FR-006 Alternative Flow B7. The suspended provider may still chat with patients on its open `In Progress` and `Aftercare` cases. Clinical notes, photos, and aftercare answers and actions stay blocked until the admin reassigns or decides the case
  - **Deactivation**: Permanent status change; provider account cannot be reactivated (final removal from platform)
    - Automatically cancel this provider's outstanding unaccepted quotes and close all related non-terminal bookings in `Accepted` (including accepted-but-unpaid selections) or `Confirmed`, using the same Alternative Flow A5 cascade as suspension, including the hand-off of accepted bookings to the FR-006 provider-fault transfer; `In Progress` bookings stay open for the admin decision as for suspension; `Aftercare` bookings and FR-011 standalone aftercare cases move to aftercare reassignment as for suspension. Block new inquiry allocations, quote submissions, acceptances, and payment; release active reservations and retain accepted snapshots.
    - Use `ProviderDeactivated` as the cancellation reason and the same separate admin-support marker and patient/admin notification handoff. In Progress bookings awaiting the admin decision and Aftercare reassignments must reach admins for clinical continuity and recovery support (FR-010/FR-011 admin workflows). Deactivation must not overwrite the reason on cases already cancelled by suspension.
    - Provider login disabled immediately for the provider account and all of its FR-009 team members
    - Provider data retained for audit/legal purposes but marked as deactivated
- **History and care continuity**: `Completed`, already `Cancelled`, and `Payment Window Expired` cases are not relabelled as new suspension or deactivation cancellations. Retain clinical notes, photos, completion milestones, accepted identifiers/versions, and payment/refund history. In Progress bookings awaiting the admin decision and Aftercare reassignments caused by suspension or deactivation must reach admins for clinical continuity and recovery support; automatic lifecycle cancellation does not itself transfer care or settle money; the admin replacement-provider transfer and its payment placeholder follow FR-006 Alternative Flow B5, and the aftercare reassignment follows FR-006 Alternative Flow B6 with no new acceptance or payment.
- **Admin action links**: Each affected record in Affected Cases & Quotes links to the admin screen that resolves it: a closed booking before treatment starts links to Start Provider-Fault Transfer on FR-006 Screen 6 (FR-006 Screen 10); an `In Progress` booking links to FR-006 Screen 6, where the admin moves it to `Aftercare` with reassignment or cancels it; an Aftercare booking links to Reassign Aftercare on FR-006 Screen 6, which opens the FR-011 aftercare reassignment screen; an FR-011 standalone aftercare case links to the FR-011 aftercare reassignment screen; flagged inquiries and cases link to the FR-016 Admin Support Required view. Each of those screens records a mandatory reason, confirmation, and audit entry as its owning FR defines.
- **Admin Support Required**: This is an independent support marker, not a new patient journey stage or provider account status. Affected cases/inquiries must be identifiable and filterable through FR-016's admin workflow, with mandatory admin alerts through FR-020. The FR-020 admin-support alert goes to admins with the FR-031 Respond to Support permission. Opening the FR-016 list requires FR-031 View Patients, and Resolve Support requires Respond to Support. Admin resolution records a reason and audit event before clearing the marker; the cancellation cause remains. An inquiry's marker stays set while any linked provider-caused impact is unresolved. If an FR-034 support case is created/linked during assistance, retain its existing Open → In Progress → Resolved → Closed workflow. Automatic ticket creation is not introduced here.
- **Patient communication**: Every affected patient receives a message with the affected inquiry/case reference and a clear Contact Admin/Support action. For a cancelled unaccepted offer, the message (`provider.status_cancellation_patient`, before acceptance only) says the offer is no longer available. For a closed accepted booking, the message (`booking.provider_fault_replacement`, mandatory) says that an admin will arrange a replacement provider within the same inquiry. It must not say the patient cancelled or instruct payment against a cancelled selection; do not expose confidential provider-investigation details. Notification failures are retried without restoring cancelled cases.
- **Reactivation**: Performed through Screen 5 (Suspended providers only). Reactivation cancels any pending scheduled suspension or deactivation and permits new eligible activity only. It must not restore cancelled quotes/cases, reopen accepted selections, reinstate old reservations, restart payment windows, clear unresolved support markers, or restore the Featured flag.
- **Featured flag**: When suspension or deactivation becomes effective, the system clears `featured` automatically (freeing a slot under Rule 8) and logs it in Tab 8.
- **Notification Email**: If "Notify Provider" checkbox enabled (default), system sends email (FR-020 `provider.suspended` or `provider.deactivated`) to the provider Owner with:
  - Action taken (Suspended or Deactivated)
  - Reason provided by admin
  - Effective date (if scheduled)
  - Contact information for admin support if provider has questions
- **Email timing**: For an immediate change the email is sent once. For a scheduled change with "Notify Provider" checked, the email is sent when the scheduled change is created (with the Effective Date) and again when it takes effect. If "Notify Provider" is unchecked, no provider email is sent at either point; patient messages and admin-support alerts are still mandatory.
- **Email recipient**: Provider status emails (`provider.suspended`, `provider.deactivated`, `provider.reactivated`, and `provider.scheduled_change_cancelled`) go to the provider Owner only. Team members learn of the status through the FR-032 Rule 6 banner or the deactivated-login message.
- **Scheduled Status Change**: A blank or today's Effective Date is treated as immediate and is never queued for the midnight UTC job. If admin selects a future Effective Date, the suspension or deactivation is stored as pending and applied automatically on that date (job processes scheduled suspensions and deactivations daily at midnight UTC), recalculating affected records at that time (A5). Until then the provider keeps its current status, and Screen 1 and the Screen 3 header show "Scheduled: Suspend/Deactivate on DD-MM-YYYY". Only one pending change per provider is allowed; an immediate suspension or deactivation replaces any pending change. Reactivating a provider through Screen 5 cancels any pending change automatically (logged in Tab 8 with the reactivation reason).
- **Cancel Scheduled Change**: Before the Effective Date, an admin can cancel the pending change from Screen 1 or the Screen 3 header by entering a reason (min 20 chars) and re-authenticating. Scheduling, cancellation, and application are logged in Tab 8; the provider Owner is emailed about the cancellation (FR-020 `provider.scheduled_change_cancelled`) if they were notified of the scheduled change.
- **Confirmation Requirement**: Admin must explicitly check "I confirm this action" checkbox before "Submit" button enabled (prevents accidental suspension/deactivation)

**Notes**:

- Use prominent warning styling (red border, caution icon) to emphasize severity of action
- Display clear differentiation between suspension (temporary, reversible) and deactivation (permanent, irreversible)
- Provide example reasons to guide admin (e.g., "Repeated unresolved patient complaints", "Violation of platform terms", "Provider requested account closure")
- Include "Cancel" button to abort action and return to provider profile view

---

### Screen 5: Provider Reactivation Modal

**Purpose**: Captures the admin reason and re-authentication before returning a Suspended provider to Active (Alternative Flow A6)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Provider Name | text (display only) | N/A | Confirms which provider is being reactivated | Display only |
| Current Suspension | text (display only) | N/A | Suspension date and the reason recorded in Screen 4 | Retrieved from the latest suspension status event |
| Pending Scheduled Change | warning (display only) | N/A | Shown only when a scheduled suspension or deactivation is pending: "Reactivating will cancel the scheduled [Suspension/Deactivation] on DD-MM-YYYY" | Retrieved from the Pending Provider Status Change record (Key Entity 4) |
| Unresolved Support Items | number (display only) | N/A | Count of this provider's affected inquiries and cases (bookings, In Progress/Aftercare cases, standalone aftercare) still marked Admin Support Required; each affected record counts once, matching the FR-020 `provider.status_cancellation_admin_support` unit (one per affected inquiry/case). Links to the FR-016 list filtered to this provider and Admin Support Required | Calculated from cancellation/support context; informational, does not block reactivation |
| Reason | textarea | Yes | Why the provider is being reactivated | Min 20 chars, max 500 chars |
| Notify Provider | checkbox | No | Send reactivation email to the provider Owner including the reason | Default checked (true) |
| Admin Password | password | Yes | Re-authentication before the status change (MFA once FR-026 / FR-031 MFA stack is delivered) | Must match the acting admin's password |
| Confirm Action | checkbox | Yes | "I confirm this action" | Must be checked to enable submit button |

**Business Rules**:

- Available only when provider status = Suspended; Deactivated providers can never be reactivated (Rule 4)
- On submit, status changes to Active immediately; the status event (reason, admin, timestamp) is logged in Tab 8
- Reactivation follows the Screen 4 Reactivation rule: nothing cancelled by the suspension is restored, and the Featured flag stays cleared
- On submit, any pending scheduled suspension or deactivation is cancelled automatically; the cancellation is logged in Tab 8 with the reactivation reason and admin, and the reactivation email states that the scheduled change no longer applies (if the provider had been notified of it)

---

## Business Rules

### General Module Rules

- **Rule 1**: All provider accounts must be created by admins—no self-service provider registration allowed.
- **Rule 2**: Provider creation (and therefore activation) requires every field marked Required in the Screen 2 wizard: First Name, Last Name, Email, Phone Number, Bio/Description (50-500 chars), Specialty, Medical License Number, Years of Experience, at least 1 Language, Clinic Name, Clinic Address, Contact Email, Medical License file, Commission Model and Value, Flat Rate Currency (when Commission Model = Flat Rate), Payout Frequency, and Commission Start Date. The Medical License file is a record-keeping baseline only; document authenticity or later document changes never block activation or change status.
- **Rule 3**: Provider statuses are Active, Suspended, and Deactivated (there is no Draft status). Providers are created as Active when all required fields are complete. Allowed transitions: Active → Suspended (Screen 4), Suspended → Active (Screen 5), Active or Suspended → Deactivated (Screen 4). "Password not yet set" is tracked by `password_set = false`, not by a separate status. An Active provider with `password_set = false` is excluded from FR-003 inquiry distribution (including explicit patient selection and reassignment) until the password is set; it may still be featured or edited by admins.
- **Rule 4**: Deactivation is permanent—deactivated providers cannot be reactivated; admin must create new provider account if re-onboarding required. Deactivation frees the provider's emails: Contact Email uniqueness counts only Active and Suspended providers, and login Email follows the FR-009 global provider email identity rule (Rule 3, REQ-009-008), under which the Owner, team member, and pending-invitation emails of a Deactivated provider are freed. The new account may reuse those emails; the deactivated record and its history are retained unchanged.
- **Rule 5**: Commission configuration applies at booking confirmation under FR-029; later configuration edits never replace an existing confirmed booking's commission snapshot.
- **Rule 6**: Featured provider designation only available for providers with status = "Active". When suspension or deactivation becomes effective, the system clears the Featured flag automatically; it is not restored on reactivation.
- **Rule 7**: Seat limit (maximum team members) defaults to 100 and can be adjusted by admin (range 1-500). Providers request seat limit increases via FR-009 "Request more seats", which opens an FR-034 support case pre-filled as a seat-increase request; if approved, the admin edits Seat Limit in Screen 3 Tab 1. Seat limit blocks staff invitations when reached (enforced by FR-009).
- **Rule 8**: At most 10 active providers may be featured. Admin can set or unset featured status from the Provider-list quick action or the Basic Information toggle. A request to feature an eleventh provider must be rejected without changing data and must clearly tell the admin to unfeature another provider first, using the message: "Maximum of 10 featured providers reached. Unfeature another provider first." Featuring or unfeaturing does not require an admin change reason (Tab 8 still logs it). This limit must be enforced server-side for every write path.
- **Rule 9**: Provider-status eligibility must be revalidated at inquiry allocation (which also requires `password_set = true`, Rule 3), quote submission, Subquote acceptance, booking-confirming payment, and three FR-006 admin actions: admin Revive Booking, admin appointment change (reschedule), and admin acceptance of a replacement quote (FR-006 B5). Each of these requires the provider to be Active; FR-006 REQ-006-020 owns the blocking message ([CR-FR006-20261027-02](../fr006-booking-scheduling/change-request-2026-10-27-admin-actions-require-active-provider.md)). Once suspension/deactivation is effective, an in-flight request or delayed callback must not create an eligible quote, revive a cancelled case, or confirm a new booking for that provider. Any payment actually captured must remain recorded and reach admin financial reconciliation, not be hidden or treated as a successful new booking. FR-007 records such late captures; FR-017 owns flagging them for admin reconciliation, holding them from provider payout, and cancelling remaining scheduled installments on provider-cancelled bookings ([CR-FR017-20261015-01](../fr017-admin-billing-finance/change-request-2026-10-15-post-suspension-payment-reconciliation.md)). Before acceptance, the status change cancels the provider's unaccepted quotes (FR-004 `cancelled_provider_status`). After acceptance, the booking is closed and handed to the FR-006 provider-fault transfer (Alternative Flows B4 and B5), where an admin rehomes the patient to a replacement provider in the same inquiry; the inquiry is not cancelled. An `Aftercare` booking is not closed and moves to aftercare reassignment (FR-006 Alternative Flow B6).
- **Rule 10**: Screen 4 and Alternative Flow A5 own provider-status cancellation and support effects; FR-006 Alternative Flow B5 owns the replacement-provider transfer for accepted bookings before treatment starts, FR-006 Screen 6 owns the admin decision for `In Progress` bookings (move to Aftercare with reassignment, or cancel), and FR-006 Alternative Flow B6 with FR-011 owns the aftercare reassignment. The cascade is provider-scoped, preserves immutable accepted context, and must not count alternatives as independent treatments or cancel unrelated providers' unaccepted offers.

### Data & Privacy Rules

- **Privacy Rule 1**: Provider contact information (email, phone) visible only to admins; patients see clinic phone/email.
- **Privacy Rule 2**: Uploaded provider documents (licenses, certifications, insurance) encrypted at rest using AES-256.
- **Audit Rule**: All provider management actions logged with timestamp, admin user ID, action details, and the admin's reason or justification (Screen 3 Tab 1 admin change reason, Screens 4-5 status reasons, Login as Provider reason). Provider-status cancellation records include the triggering status event, effective time, affected inquiry/quote/booking/treatment identifiers, prior stage, cancellation cause, support marker, slot-release outcome, and notification outcome. Sensitive suspension reasons remain admin/provider context rather than patient notification content.

### Admin Editability Rules

**Editable by Admin**:

- Provider basic information (name, specialty, bio, languages, awards)
- Clinic information (name, address, phone, logo, contact email)
- Commission configuration (Model: Percentage/Flat, Value, Flat Rate Currency, Effective Date)
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

**Fixed in Codebase**:

- Deactivation finality rule
- Encryption standards
- Commission calculation logic

### Payment & Billing Rules

- **Commission Rule 1**: Commissions apply to all provider earnings from patient bookings.
- **Commission Rule 2**: **Percentage Model**: Calculated as `Booking Total * (Commission Rate / 100)`. The booking total is the accepted price after promotion, in the quote currency, read from the FR-005 acceptance snapshot; commission never reads the live quote or option record. The same base applies to every discount type, including discounts funded only by Hairline. The rate is the one fixed at booking confirmation (Commission Rule 4).
- **Commission Rule 3**: **Flat Rate Model**: Fixed amount deducted per completed procedure (e.g., £150 flat fee).
- **Commission Rule 4**: Resolve and snapshot the effective commission model/value when a booking is confirmed. Changes affect newly confirmed bookings only; existing snapshots govern later payments and commission recognition. Locking configuration at confirmation does not move the Flat Rate deduction away from its existing completed-procedure milestone.
- **Cancellation Billing Rule**: Suspension or deactivation closes affected bookings and blocks further patient payment to that provider, but payment/refund/commission records remain intact. For a closed accepted booking, money follows the FR-006 Alternative Flow B5 payment placeholder: paid amounts move with the patient as credit toward the replacement booking, any unused part is refunded, and the patient pays no fee. Exact refund, fund-release, and allocation mechanics belong to FR-007, FR-007B, and FR-017; no new refund percentage, fee, payout rail, or fund-release rule is defined here.
- **Billing Rule 1**: Provider payouts are calculated per the provider's Payout Frequency (Weekly, 2x a Month, or Monthly; Tab 7) and transferred to the provider's bank account through FR-017.

---

## Success Criteria

### Patient Experience Metrics

- **SC-001** **[P2 - Post-MVP, with FR-022 patient provider search]**: Patients can discover and view featured provider profiles in Patient Platform within 1 second of search query (data sourced from A-02 featured providers)
- **SC-002**: 100% of patient-facing provider information (name, clinic, specialty) displays accurately and matches admin-configured data in A-02 with no discrepancies
- **SC-003**: Patients see only active providers in search results (no suspended/deactivated providers visible), ensuring trust and booking reliability

### Provider Efficiency Metrics

- **SC-004**: Providers receive account activation notification within 1 minute of admin activating their account, enabling immediate platform access
- **SC-005**: Providers can view their uploaded documents list and commission configuration in Provider Platform within 2 seconds of navigation
- **SC-006**: 90% of providers successfully log in and access their profile on first attempt after receiving activation credentials (low login failure rate)

### Admin Management Metrics

- **SC-007**: Admins can create a complete provider profile (all sections filled, documents uploaded, commission configured) in under 10 minutes on average
- **SC-008**: Admins can filter and search provider list (1000+ providers) and retrieve results in under 2 seconds, enabling efficient provider oversight
- **SC-009**: Providers and admins can upload and manage documents in under 30 seconds per document, streamlining record-keeping workflows. Document changes sync between FR-032 and FR-015 within 1 minute
- **SC-010**: 100% of provider status changes (create as Active, suspend, reactivate via Screen 5, deactivate, schedule or cancel a scheduled change) and admin profile edits logged in audit trail with timestamp, admin user, and the mandatory reason (full accountability)
- **SC-011**: System maintains complete audit trail of all document uploads, replacements, and deletions with 100% accuracy
- **SC-012**: Admin dashboard displays real-time provider status counts (active, suspended, deactivated) with <1 second refresh latency

### System Performance Metrics

- **SC-013**: Provider creation/edit form submission completes within 3 seconds for 95% of requests (excluding large document uploads)
- **SC-014**: Document upload (up to 10MB per file) completes within 10 seconds for 90% of uploads on standard broadband connections
- **SC-015**: Provider profile page loads (all tabs: Basic Information, Languages, Staff List, Awards, Reviews, Documents, Commission & Financials, Activity Log) within 2 seconds for 95% of requests
- **SC-016**: System supports 100 concurrent admin users managing providers without performance degradation
- **SC-017**: 99.9% uptime for provider management functionality (excluding scheduled maintenance)

### Business Impact Metrics

- **SC-018**: Provider onboarding time reduced by 60% compared to manual/offline provider onboarding processes (baseline: 5 hours manual → target: 2 hours in-system)
- **SC-019**: Provider document management errors reduced by 80% through structured upload validation and clear file type requirements
- **SC-020**: 95% of providers have complete profiles (all required fields filled, commission configured) within 48 hours of initial account creation
- **SC-021** **[P2 - Post-MVP, with FR-022 patient provider search]**: Featured provider designation increases patient booking conversion rate by 25% compared to non-featured providers (measured in Patient Platform analytics)

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **[FR-031: Admin Access Control & Permissions](../fr031-admin-access-control/prd.md) / Module A-09: System Settings & Configuration**
  - **Why needed**: Admins must be authenticated and hold the FR-031 Provider Management (A-02) permissions: View Providers (Screen 1 and Screen 3 read access), Onboard Providers (Screen 2), Edit Providers (Screen 3 edits, documents, commission, seat limit, featured flag, Resend Activation Email), and Suspend Providers (Screens 4-5: suspension, deactivation, reactivation, scheduled-change cancellation). Login as Provider is restricted to Super Admin; re-authentication for suspend/deactivate/reactivate/Login as Provider uses the admin's credentials
  - **Integration point**: A-02 verifies admin user session token and role permissions before allowing provider management actions; API endpoints protected by role-based access control (RBAC)

- **[FR-009: Provider Team & Role Management](../fr009-provider-team-roles/prd.md) / Module PR-01: Auth & Team Management**
  - **Why needed**: Providers created in A-02 must be able to log into Provider Platform to view their profile status, uploaded documents, and commission configuration (all sourced from A-02/FR-032).
  - **Integration point**: A-02 creates provider user account credentials (email/password) and passes to PR-01 authentication service; providers authenticate via PR-01 to read profile data managed by A-02 and edit the allowed fields via FR-032. FR-009 also enforces the Seat Limit set in Screen 2 Step 1 when providers invite team members

- **[FR-022: Search & Filtering](../fr022-search-filtering/prd.md) / Module P-02: Quote Request & Management (provider discovery and featured listing)**
  - **Why needed**: Featured providers designated in A-02 must be displayed prominently in Patient Platform search and discovery interfaces. FR-022 patient provider search is P2 (Post-MVP); in MVP, FR-015 maintains the featured flag and cap only
  - **Integration point**: P-02 queries A-02 provider data filtered by (status = "Active" AND featured = true) to populate featured provider listings; includes provider name, clinic, specialty, profile photo

- **FR-020 / Module S-03: Notifications & Alerts**
  - **Why needed**: Provider account events, mandatory patient cancellation messages, and admin-support alerts must be delivered with appropriate recipient privacy; SMS remains a future channel.
  - **Integration point**: A-02 supplies the provider status event and affected record references. Provider account emails use FR-020 events `provider.activation` (mandatory, cannot be disabled; Main Flow step 13 and A1), `provider.suspended` / `provider.deactivated` (Screen 4), `provider.reactivated` (A6, Screen 5), and `provider.scheduled_change_cancelled` (Screen 4 Cancel Scheduled Change) per CR-FR020-20261015-01. Account-closure requests (A7) use `provider.closure_requested` (to admins, on FR-032 submission) and `provider.closure_rejected` (to the provider, on rejection), both mandatory, per CR-FR020-20261015-02. FR-020 owns delivery/retry and recipient-scoped payloads; provider-caused cancellation must not use FR-003's patient-cancellation message or expose confidential suspension reasons to patients.

- **Shared Service S-05: Media Storage Service** (platform service; no dedicated FR)
  - **Why needed**: Provider documents (licenses, certifications, insurance) must be securely stored with encryption and access controls
  - **Integration point**: A-02 uploads documents to S-05 API with metadata (provider ID, document type, uploader type and ID); S-05 returns secure download URLs accessible only to authorized admins

- **Shared Service S-06: Audit Log Service** (platform service; no dedicated FR)
  - **Why needed**: All provider management actions (creation, edits, status changes, and document-related actions) must be logged for compliance and audit trails
  - **Integration point**: A-02 sends audit log events to S-06 API with structured data (timestamp, admin user ID, action type, entity ID, before/after values); S-06 persists logs and provides query interface for admin reporting

- **[FR-003: Inquiry Submission](../fr003-inquiry-submission/prd.md)**
  - **Why needed**: Distinguish provider-caused cancellation from patient cancellation and avoid cancelling unrelated responses to a shared inquiry.
  - **Integration point**: Distribute inquiries only to Active providers with `password_set = true` (CR-FR003-20261015-01). An inquiry whose accepted booking is closed by the cascade stays open for the FR-006 provider-fault transfer and is not cancelled; for an inquiry still comparing providers, cancel the affected ProviderInquiry participation/quotes only. Retain `ProviderSuspended` or `ProviderDeactivated` cause and the separate support marker in affected inquiry context.

- **[FR-004: Quote Submission](../fr004-quote-submission/prd.md) / [FR-005: Quote Comparison & Acceptance](../fr005-quote-comparison-acceptance/prd.md)**
  - **Why needed**: Multiple Parent Quotes from one provider and their package/date alternatives all depend on provider eligibility; only a Subquote is accepted.
  - **Integration point**: Block ineligible submissions/acceptances and cancel affected unaccepted parents with FR-004 `cancelled_provider_status`; an accepted parent keeps `accepted` and its AcceptanceEvent stays unchanged; FR-005 writes the linked supersession record only when the admin accepts the replacement quote (FR-006 Alternative Flow B5). Preserve the AcceptanceEvent, selected identifiers, equal accepted aggregate versions, and quote-local package snapshot; do not modify the reusable package library.

- **[FR-006: Booking & Scheduling](../fr006-booking-scheduling/prd.md) / [FR-007: Payment Processing](../fr007-payment-processing/prd.md)**
  - **Why needed**: Accepted selections may still be awaiting initial payment, while other cases are confirmed or already undergoing treatment.
  - **Integration point**: FR-006 Alternative Flow B4 applies the provider-status cancellation cause, releases valid holds/reservations, blocks further payment, and retains all booking/payment history; FR-006 Alternative Flow B5 then performs the admin replacement-provider transfer in the same inquiry with its payment placeholder. FR-006 Alternative Flow B6 handles `Aftercare` bookings through aftercare reassignment without closing them. Provider suspension is cancellation, not `Payment Window Expired`; exact payment mechanics retain their existing owners.

- **[FR-010: Treatment Execution](../fr010-treatment-execution/prd.md) / [FR-011: Aftercare & Recovery Management](../fr011-aftercare-recovery-management/prd.md)**
  - **Why needed**: Suspension includes In Progress and Aftercare cases without deleting care already delivered.
  - **Integration point**: Apply the provider-status cause and support marker, preserve clinical records/completion milestones, and route clinical continuity to admins. `In Progress` bookings are not cancelled automatically; an admin either moves them to `Aftercare` with aftercare reassignment or cancels them with a reason through FR-006. Aftercare bookings and FR-011 standalone aftercare cases are not cancelled; an admin reassigns them through the FR-011 aftercare reassignment screen (FR-006 Alternative Flow B6). FR-010's ordinary provider-requested Cancel/Close Case remains distinct.

- **[FR-014: Provider Analytics & Reporting](../fr014-provider-analytics-reporting/prd.md)**
  - **Why needed**: Provider-profile counts and reporting must not multiply one treatment by its quote alternatives or erase historical milestones after cancellation.
  - **Integration point**: Completed Procedures counts distinct actual FR-010 completions; cancellation excludes a selection from active pending-payment exposure without deleting historical acceptance/price observations.

- **[FR-016: Admin Patient Management](../fr016-admin-patient-mgmt/prd.md) / [FR-034: Support Center & Ticketing](../fr034-support-center-ticketing/prd.md)**
  - **Why needed**: Provider-related cancellations require identifiable, filterable special admin support rather than an ordinary patient cancellation.
  - **Integration point**: Surface affected inquiry/case references, cancellation cause, `supportRequired`, and any linked support case. The FR-016 list requires FR-031 View Patients, and Resolve Support requires Respond to Support, the same permission that receives the FR-020 admin-support alert. Admins record assistance/resolution; linked tickets use FR-034's existing status workflow. No automatic ticket creation is added.

- **[FR-029: Payment System Configuration](../fr029-payment-system-config/prd.md) / [FR-017: Admin Billing & Finance](../fr017-admin-billing-finance/prd.md)**
  - **Why needed**: FR-029 owns commission snapshot timing; FR-015 owns synchronized provider-specific configuration and payout frequency consumed by FR-017.
  - **Integration point**: Snapshot the effective model/value at booking confirmation, preserve existing booking snapshots, and keep provider-specific edits synchronized. Payout-cycle timing and fund-release rules are not redesigned. FR-029 Screen 5 accepts the same provider-specific Percentage (0-100%) or Flat Rate model defined here ([CR-FR029-20261014-01](../fr029-payment-system-config/change-request-2026-10-14-provider-flat-rate-commission.md)).

- **[FR-032: Provider Dashboard Settings](../fr032-provider-dashboard-settings/prd.md) / Module PR-06: Profile & Settings Management**
  - **Why needed**: Providers self-edit the profile fields listed under Admin Editability Rules and manage their own documents; FR-032 owns field validation (Clinic Name 3-200 chars, unique Contact Email, document formats PDF/JPG/PNG/DOCX/XLSX) that FR-015 reuses.
  - **Integration point**: A-02 and FR-032 read and write the same provider, clinic, and document records; changes from either side sync within 1 minute and are logged in Tab 8. FR-032 Screen 4 shows the Tab 7 commission configuration and payout frequency read-only, and FR-032 Rule 6 owns the Suspended/Deactivated account-status banner ([CR-FR032-20261015-01](../fr032-provider-dashboard-settings/change-request-2026-10-15-provider-commission-panel-suspension-banner.md)).

- **[FR-013: Reviews & Ratings](../fr013-reviews-ratings/prd.md)**
  - **Why needed**: Tab 5 shows provider reviews; admin insert, edit, and removal of reviews is owned by FR-013.
  - **Integration point**: Tab 5 reads review data and opens FR-013 Screen 8 for admin review actions; moderation rules follow FR-013 Screens 6-8.

- **[FR-026: App Settings & Security Policies](../fr026-app-settings-security/prd.md) / Module A-09**
  - **Why needed**: Supplies the managed country and Provider Specialties lists used in the wizard and Tab 1, and the admin security policies (MFA, re-authentication) applied to status changes and Login as Provider.
  - **Integration point**: A-02 reads the active lists at form load and validates saved values against them.

- **[FR-021: Multi-Language & Localization](../fr021-i18n-localization/prd.md)**
  - **Why needed**: Owns the central language catalog used for Languages Spoken (Screen 2 Step 2) and Supported Languages (Tab 2).
  - **Integration point**: A-02 reads active catalog languages at form load and validates saved values against them; a stored language later removed from the catalog still displays but cannot be newly selected.

**Reconciliation boundary**: These are the FR-015 target handoffs. Downstream alignment for the suspension/deactivation cascade and the Flat Rate commission model is tracked by the 2026-10-14 Change Requests beside FR-003, FR-004, FR-010, FR-011, FR-016, FR-020, and FR-029, with change-log alignment in FR-005 and FR-006. Payments captured after suspension/deactivation are recorded by FR-007 and reconciled by FR-017 (CR-FR017-20261015-01). Admin per-provider staff invites and limited-write impersonation are aligned in FR-009 (CR-FR009-20261015-01), and the Provider Specialty list in FR-026 (CR-FR026-20261015-01). Provider account-closure requests are aligned in FR-032 (CR-FR032-20261015-02), and the provider lifecycle email events in FR-020 and FR-030 (CR-FR020-20261015-01, CR-FR030-20261015-01). Closure request notifications and the admin marker are aligned in FR-032, FR-020, and FR-030 (CR-FR032-20261015-03, CR-FR020-20261015-02, CR-FR030-20261015-02); Suspended-provider commission edits in FR-029 (CR-FR029-20261015-02); and the set-password distribution gate in FR-003 (CR-FR003-20261015-01). System documents and implementation remain subject to reconciliation.

### External Dependencies (APIs, Services)

- **External Service 1: Email Delivery Service (e.g., SendGrid, AWS SES)**
  - **Purpose**: Sends provider notification emails (account activation and status changes)
  - **Integration**: S-03 Notification Service integrates with email delivery API via REST/SMTP; A-02 does not directly call external email service
  - **Failure handling**: If email delivery fails, S-03 retries up to 3 times with exponential backoff; A-02 displays warning to admin: "Notification queued but not yet delivered." The same warning applies to activation emails and provider status emails

- **External Service 2: SMS Delivery Service (e.g., Twilio, AWS SNS)**
  - **Purpose**: (Future) Sends SMS notifications to providers for critical status changes (account suspended, deactivated, or reactivated) once S-03 SMS support is implemented
  - **Integration**: S-03 integrates with SMS API; A-02 would trigger SMS notifications via S-03 for high-priority events in a later phase
  - **Failure handling**: SMS failures logged in S-03; A-02 fallback sends email notification if SMS delivery fails. **No SMS delivery is available in MVP.**

- **External Service 3: Cloud File Storage (e.g., AWS S3, Google Cloud Storage)**
  - **Purpose**: Stores uploaded provider documents (licenses, certifications, insurance) with encryption at rest
  - **Integration**: S-05 Media Storage Service uploads documents to cloud storage via SDK/API with server-side encryption (AES-256)
  - **Failure handling**: If upload fails, A-02 displays error to admin: "Document upload failed. Please retry." Document upload retries automatically up to 3 times before failing

### Data Dependencies

- **Entity 1: Admin User Roles and Permissions**
  - **Why needed**: A-02 must verify admin has "Provider Management" permission before allowing provider creation, editing, or status changes
  - **Source**: FR-031 Admin Access Control & Permissions (Module A-09) provides role-based access control (RBAC); all default roles (Super Admin, Aftercare Specialist, Billing Staff, Support Staff) have View Providers; by default only Super Admin has Edit Providers, Onboard Providers, and Suspend Providers, which custom roles may also be granted per FR-031

- **Entity 2: Notification Templates (Email/SMS)**
  - **Why needed**: Standardized notification messages for the FR-020 provider lifecycle events (`provider.activation`, `provider.suspended`, `provider.deactivated`, `provider.reactivated`, `provider.scheduled_change_cancelled`, `provider.closure_requested`, `provider.closure_rejected`) must exist; in MVP only email templates are used, with SMS templates reserved for future phases
  - **Source**: Notification templates pre-configured in S-03 Notification Service; A-02 triggers the FR-020 event; the template for each event is configured in FR-030. SMS templates, if configured later, would be used only once SMS delivery is enabled.

- **Entity 3: Document Type Configuration**
  - **Why needed**: System must know which document types are required to be stored for each provider (medical license, board certification, malpractice insurance)
  - **Source**: Document type definitions configured in admin settings or hardcoded in A-02 codebase; document types are Medical License, Board Certification, Insurance (general), Malpractice Insurance, Business License, and Other, with FR-032 validation rules (max 10MB; PDF, JPG, PNG, DOCX, XLSX). No in-system document status workflow is tracked in this FR.

- **Accepted selection and booking context**: FR-005/FR-006 own the accepted Parent Quote/Subquote identifiers, versions, package/date/appointment/price snapshot, booking stage, and reservation. FR-015 references them for lifecycle impact and audit rather than copying a mutable quote into the Provider record.
- **Cancellation/support context**: Affected inquiry/case owners retain the provider-status event reference, cancellation reason, and `supportRequired` marker with resolution audit. FR-016/FR-034 consume this context for assistance; commission snapshots remain on the confirmed booking/financial records, not on the current Provider profile alone.

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
- **Assumption 4**: Effective suspension or deactivation automatically closes all related non-terminal cases before treatment starts, with special admin support; In Progress cases are not cancelled automatically and wait for an admin decision (move to Aftercare with reassignment, or cancel), and Aftercare cases are not cancelled and move to admin aftercare reassignment. Existing completed history is retained; account reactivation does not restore cancelled cases.
- **Assumption 5**: Deactivated providers' data is retained for a minimum of 7 years for legal/audit purposes, then archived; it is never hard-deleted. GDPR/data deletion requests are handled via separate data privacy workflows (not in-scope for A-02)

---

## Implementation Notes

### Technical Considerations

- **Architecture**: Provider Management module follows admin-initiated CRUD (Create, Read, Update, Delete) pattern with state machine for status lifecycle (Active → Suspended → Active via Screen 5 reactivation, or → Deactivated; Active → Deactivated also allowed; no Draft status)
- **Technology**: Document upload functionality should support chunked/resumable uploads for large files (up to 10MB) to handle unreliable admin connections
- **Performance**: Provider list dashboard with 1000+ providers requires server-side pagination, filtering, and sorting, with indexing on status/created_date columns, for responsive UI
- **Storage**: Provider documents stored in cloud object storage (S3-compatible) with server-side encryption (AES-256); document metadata (filename, upload date, document type, uploaded by) stored in relational database
- **Validation**: Commission rate validation enforced at both client-side (immediate feedback) and server-side (security) to prevent invalid configurations. Percentage model: 0-100%; Flat Rate model: > 0 with a Flat Rate Currency from the FR-029 enabled currency list
- **State Machine**: Provider status transitions implemented as finite state machine with validation rules (e.g., cannot transition from Deactivated to any other status; must include reason and admin re-authentication for Suspend/Deactivate/Reactivate transitions)

### Integration Points

- **Integration 1: Admin Platform (A-02) → Notification Service (S-03)**
  - **Data format**: JSON payload with event type (an FR-020 provider lifecycle event, e.g., `provider.activation`), provider ID, recipient (provider email/phone), template ID, and dynamic variables (e.g., provider name, login URL)
  - **Authentication**: Service-to-service authentication via API key in request header
  - **Error handling**: S-03 returns 202 Accepted (notification queued) or 4xx/5xx error; A-02 logs notification failures and displays warning to admin

- **Integration 2: Admin Platform (A-02) → Media Storage Service (S-05)**
  - **Data format**: Multipart form-data for document uploads with metadata (provider ID, document type, uploader type and ID)
  - **Authentication**: OAuth 2.0 service account token for S-05 API access
  - **Error handling**: S-05 returns 200 OK with document URL or 4xx/5xx error; A-02 retries upload up to 3 times with exponential backoff before failing

- **Integration 3: Provider Platform (PR-01) → Provider Data (A-02 Database)**
  - **Data format**: REST API calls from PR-01 to fetch provider profile data for display in provider's profile view; edits to allowed fields go through FR-032
  - **Authentication**: OAuth 2.0 provider user token validated by A-02 API; provider can only access their own profile data (not other providers)
  - **Error handling**: A-02 API returns 200 OK with provider data or 403 Forbidden if provider attempts to access unauthorized data

- **Integration 4: Patient Platform (P-02) → Featured Provider Data (A-02 Database)** **[P2 - Post-MVP]**
  - **Data format**: REST API call (GET) from P-02 to fetch featured providers (status = Active AND featured = true) with fields: name, clinic, specialty, profile photo URL
  - **Authentication**: Public read-only REST endpoint (no authentication required for featured provider listings); returns only the public fields listed above and is rate limited, as the constitution requires for all public-facing APIs
  - **Error handling**: A-02 returns empty array if no featured providers available; P-02 displays "No featured providers at this time" message

- **Integration 5: Provider lifecycle → inquiry, quote, booking, and care owners**
  - Use the provider status event and effective time to revoke eligibility, identify affected records, apply the Screen 4 cancellation scope, and release reservations. Retain immutable accepted context and clinical/payment history. Revalidate eligibility during concurrent acceptance/payment; retry incomplete cascade processing without duplicate outcomes, and do not report a fully completed cascade while affected cases remain unprocessed.
- **Integration 6: Cancellation → admin support and notifications**
  - Supply cancellation cause, affected case/inquiry references, prior stage, and support marker to FR-016 and FR-020. Patient messages provide Contact Admin/Support; confidential investigation details remain restricted. Support handling may link an existing/manual FR-034 case, but this change does not create a new automated ticket source or another ticket lifecycle.
- **Integration 7: Commission/profile data → confirmed bookings and reporting**
  - Follow FR-029 for effective configuration and confirmation-time commission snapshots; FR-017 consumes those snapshots and the existing payout-frequency setting. Current provider-profile edits cannot rewrite historical selections, and Completed Procedures follows the distinct FR-010 completion milestone with FR-014 counting semantics.

### Scalability Considerations

- **Current scale**: Expected 100-200 providers onboarded in first 6 months (10-30 provider creations per month)
- **Growth projection**: Plan for 1,000+ providers within 2 years as platform expands to new geographic markets
- **Peak load**: Admin dashboard must support 100 concurrent admin users (SC-016) during provider onboarding campaigns without performance degradation
- **Data volume**: Expect 300MB of provider documents uploaded per month (3 documents × 10MB avg per provider × 10 providers/month); plan for 10GB storage per year
- **Scaling strategy**:
  - Database indexing on provider.status, provider.created_at, provider.featured for fast dashboard queries
  - Document storage in cloud object storage (S3) with CDN for admin document preview (reduces server load)
  - Pagination and lazy loading in provider dashboard (load 50 providers per page) to minimize initial page load time
  - Async document upload processing (upload to S-05 asynchronously, update database when complete) to prevent blocking admin UI

### Security Considerations

- **Authentication**: Only authenticated admins holding at least the FR-031 View Providers permission can access A-02 provider management features; enforced via role-based access control (RBAC) middleware
- **Authorization**: Each action checks its FR-031 permission: View Providers (read-only access), Onboard Providers (create), Edit Providers (profile, documents, commission, seat limit, featured flag), Suspend Providers (all status changes). Resend Activation Email requires Edit Providers. Login as Provider is Super Admin only. Roles are defined in FR-031, not in this FR
- **Encryption**:
  - Provider documents encrypted at rest in cloud storage (AES-256 server-side encryption)
  - Provider sensitive data (email, phone, medical license number) is stored in the database protected by database/disk encryption at rest, HTTPS/TLS in transit, and access control. It is not encrypted at application level, so the Screen 1 partial search and the login email uniqueness check keep working
  - All API communication via HTTPS/TLS 1.3 (no unencrypted HTTP allowed)
- **Audit trail**: 100% of provider management actions logged with timestamp, admin user ID, IP address, and action details; audit logs immutable (cannot be edited or deleted by admins)
- **Threat mitigation**:
  - Rate limiting on provider creation API (max 10 provider creations per admin per hour) to prevent bulk account creation abuse
  - File upload validation (max 10MB per file, only PDF, JPG, PNG, DOCX, and XLSX allowed, matching FR-032; malware scanning via antivirus integration before storage)
  - Input sanitization on all form fields (prevent SQL injection, XSS attacks)
- **Compliance**:
  - Confidential handling of provider medical licenses and certifications (professional records, not patient PHI) with the same encryption and access controls
  - GDPR compliance for provider personal data (name, email, phone) with data retention policies (deactivated providers' data retained for a minimum of 7 years, then archived; never hard-deleted)
  - SOC 2 Type II audit trail requirements met via S-06 Audit Log Service integration

---

## User Scenarios & Testing

### User Story 1 - Admin Onboards New Provider from Scratch (Priority: P1)

Admin receives provider application materials (resume, licenses, certifications, insurance) and creates complete provider profile in Admin Platform, uploads documents, configures commission, and activates account. Provider receives email notification and can immediately log into Provider Platform.

**Why this priority**: Core functionality enabling platform provider network growth; without this, no providers can be onboarded and platform cannot function.

**Independent Test**: Admin completes full provider onboarding workflow from provider creation form to activation; verify provider receives activation email, can log into Provider Platform, and views correct profile data (name, clinic, commission rate).

**Acceptance Scenarios**:

1. **Given** admin is logged into Admin Platform with the FR-031 Onboard Providers permission, **When** admin navigates to Provider Management → "Add New Provider" → completes every wizard field marked Required (name, email, phone, license, clinic and contact email, Medical License file, commission model/value, payout frequency, commission start date) → clicks "Create Provider", **Then** system creates provider with status = "Active", sends activation email to provider, and displays success message: "Provider [Clinic Name] created successfully. An activation email has been sent to [email]."
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

- What happens when **admin attempts to create provider with email already used by another provider**? Login email follows the FR-009 global provider email identity rule (Rule 3, REQ-009-008); Deactivated providers' emails are freed (see Rule 4). If another provider organization uses the email as Owner, team member, or pending invitation, system displays validation error: "Email address already in use by another provider. Please use a different email." Provider creation blocked until unique email provided.
- How does system handle **provider document upload fails mid-upload (network interruption)**? System supports resumable uploads; if upload interrupted, admin can retry upload (system may resume from last successful chunk if implemented, otherwise restarts upload).
- What occurs if **admin activates provider but notification email delivery fails (email service down)**? System queues notification for retry (up to 3 attempts over 1 hour); admin sees warning message: "Notification queued but not yet delivered." Admin can manually resend via the "Resend Activation Email" button in Screen 3.
- How to manage **two admins, or an admin and the provider, editing the same provider profile at the same time**? The last save wins. There is no conflict check and no conflict message, for admin saves (FR-015) and provider saves (FR-032) alike. Every save is logged in Tab 8 with its changed fields, so an overwritten value can be traced.
- What happens when **admin deactivates provider with 10 upcoming patient bookings and active treatment/aftercare cases**? The impact modal lists all non-terminal Accepted, Confirmed, In Progress, and Aftercare cases. On confirmation, the Accepted and Confirmed cases are cancelled with `ProviderDeactivated` (same cascade as suspension), In Progress cases stay `In Progress` with the cause and support marker for an admin decision, reservations released, further payment blocked, patients notified to contact admins, and affected records flagged for support. Historical selections remain. Aftercare cases keep their status with the `ProviderDeactivated` cause and move to admin aftercare reassignment (FR-006 Alternative Flow B6). Each affected inquiry stays open, and an admin rehomes each patient to a replacement provider through the FR-006 provider-fault transfer (Alternative Flow B5), with money following its payment placeholder.
- What happens if **admin attempts to create provider without filling required fields**? System validates every field marked Required in the Screen 2 wizard tables on each step (see Rule 2). System displays error: "Please complete all required fields before proceeding" and highlights missing fields in red.
- What occurs if **admin attempts to set invalid commission rate (e.g., negative percentage or zero flat rate)**? System displays client-side validation error immediately: "Percentage must be between 0-100%" or "Flat rate must be greater than 0." Server-side validation also enforces rules; the API returns a 422 validation error whose field message uses the same PRD wording if an invalid rate is submitted.
- How to manage **provider requests account closure (wants to be deactivated)**? Provider submits an account-closure request in FR-032 (Request account closure) or contacts admin; there is no self-service deactivation. Admin processes it per Alternative Flow A7: opens the provider profile → clicks "Deactivate Provider" → enters reason: "Provider requested account closure on [date]" → confirms deactivation. System deactivates account, cancels all non-terminal cases under the Screen 4 cascade, marks any FR-032 closure request Approved, and sends the deactivation email (FR-020 `provider.deactivated`; "Notify Provider" is locked on for closure deactivations). If the admin rejects the request, the provider stays Active and receives FR-020 `provider.closure_rejected` with the review notes.
- What happens if **admin sets seat limit below current team size**? System validates seat limit against current team size, meaning FR-009 seat usage (accepted non-Owner team members plus invitations still pending; the Owner and expired invitations do not count). If seat limit is set below current count (e.g., provider has 50 staff but admin sets limit to 30), system displays warning: "Current team size (50) exceeds new seat limit (30). Existing team members will not be removed, but no new invitations can be sent until limit is increased or team size is reduced." Admin must confirm to proceed. Existing team members remain active; only new invitations are blocked.
- What happens if **provider doesn't receive activation email**? Provider can click "Didn't receive activation email?" link on login page, enter their email, and request resend. System generates new one-time password setup link (expires 24 hours), invalidates previous link, and sends new email. Rate limited to 3 resend requests per hour per email. Admin can also manually resend from provider profile in FR-015 by clicking "Resend Activation Email" button in Quick Actions (visible only if password not yet set).
- What happens if **activation link expires (24 hours passed)**? Provider can request new activation email via login page resend flow or contact admin. Admin can manually resend from provider profile. When provider clicks expired link, system displays: "This activation link has expired. Request a new activation email or contact support."
- What happens if **provider tries to request activation resend but already activated account**? System displays generic message: "If an account exists with this email, an activation link will be sent." (doesn't reveal if account already activated for security). No email sent. This prevents email enumeration attacks.
- What happens if **admin accidentally creates duplicate provider with same email**? System validates the login email against the FR-009 global provider email identity rule (Rule 3, REQ-009-008) during provider creation. If an Active or Suspended provider already uses the email as its Owner login, system displays error: "Email address already in use by another provider (Provider Name: [existing provider]). Please use a different email or edit the existing provider." Creation blocked until unique email provided.
- What happens if **acceptance or initial payment races with suspension**? Eligibility must be checked against the effective provider status. No cancelled selection may be confirmed or revived; any real captured payment remains recorded and is routed to admin financial resolution.
- What happens if **a scheduled suspension or deactivation becomes effective after more cases were created**? Recalculate affected records at effective time rather than using the old preview. The scheduled rule does not delay cancellation until each patient requests support.
- What happens if **cancellation/support notifications fail or cascade processing retries**? Keep provider eligibility revoked and cancelled records cancelled. Retry incomplete work using the same status event/case references without duplicate cancellations, alerts, or slot releases; retain visible unresolved processing failures for admins.
- What happens if **a quote contains five packages with several date alternatives**? They remain alternatives of the same Parent Quote. Cancel its availability once; do not create a treatment or support item per unselected alternative.
- What happens if **a provider is deactivated after suspension already cancelled cases**? Do not overwrite ProviderSuspended or create another cancellation for terminal records; retain unresolved support markers and the original audit chain.
- What happens if **suspension affects an Aftercare case after the procedure was completed**? The case is not cancelled. It keeps its status, the FR-010 completion milestone, and its single Completed Procedures count; an admin reassigns aftercare to another provider or the Hairline aftercare team through the FR-011 aftercare reassignment screen. Performed care and payment history are not erased.

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
- **REQ-015-019**: System MUST send affected patients cancellation/offer-unavailability messages with Contact Admin/Support instructions (`provider.status_cancellation_patient` before acceptance; for a closed accepted booking, the mandatory `booking.provider_fault_replacement` notice that an admin will arrange a replacement provider within the same inquiry) and alert admins for special support, regardless of the optional Notify Provider checkbox. Support resolution MUST be audited before clearing the marker; confidential investigation details MUST NOT appear in patient messages.
- **REQ-015-020**: System MUST revalidate provider eligibility at allocation, submission, acceptance, booking confirmation, and the FR-006 admin actions admin Revive Booking, admin appointment change (reschedule), and admin acceptance of a replacement quote (FR-006 B5) (each requires an Active provider, per FR-006 REQ-006-020), prevent in-flight operations/callbacks from reviving cancelled cases, and deduplicate cascade processing by provider-status event and affected record. The status change and its provider status event MUST be written in one transaction; the cascade MUST run as an idempotent background job with a target completion within 5 minutes, and a reactivation MUST NOT stop a running cascade for the earlier event.
- **REQ-015-021**: Suspension, deactivation, or reactivation MUST NOT rewrite accepted snapshots/versions, erase clinical or financial history, or automatically reopen cancelled quotes/cases/payment windows. Admin support MUST retain access to the records needed for clinical continuity and financial resolution.
- **REQ-015-025**: Admin saves to provider profile data (Screen 3 Tabs 1, 2, 4, 6 notes, and 7) MUST require a change reason of 10-500 characters that is stored in the Tab 8 audit entry; provider self-edits via FR-032 and Featured Provider set/unset actions are exempt.
- **REQ-015-026**: Login as Provider MUST require a reason (min 20 characters) and admin re-authentication, show a persistent impersonation banner, block password/email/financial changes, log every action in Tab 8, and end after 30 minutes of inactivity. It MUST be blocked for a Deactivated provider and MUST be limited to the FR-032 Rule 6 read-only rules for a Suspended provider, whether the admin impersonates the Owner or a team member.
- **REQ-015-027**: System MUST clear the Featured flag automatically when suspension or deactivation becomes effective and MUST NOT restore it on reactivation.
- **REQ-015-028**: System MUST support scheduled suspension and deactivation: store at most one pending change per provider, show a "Scheduled" marker on Screen 1 and the Screen 3 header, allow admins to cancel it with a reason and re-authentication before the Effective Date, apply it automatically on that date with the A5 cascade recalculated at effective time, and log scheduling, cancellation, and application in Tab 8.
- **REQ-015-029**: Screen 4 MUST link each affected record to the admin screen that resolves it (provider-fault transfer, aftercare reassignment, or the FR-016 Admin Support Required view), and each of those actions MUST record a mandatory reason, confirmation, and audit entry.

### Data Requirements

- **REQ-015-007**: System MUST maintain provider profile data aligned with FR-032 (Bio, Languages, Awards, Profile Picture, Contact details, etc.). Changes made by providers in FR-032 must sync to admin view in real-time.
- **REQ-015-008**: System MUST store uploaded provider documents in secure cloud storage (AES-256).
- **REQ-015-009**: System MUST store commission configuration (Model: Percentage/Flat, Value, Flat Rate Currency, Effective Date) per provider in the FR-029 provider-specific commission record.
- **REQ-015-010**: System MUST store seat limit (maximum team members) per provider with default value of 100, adjustable range 1-500. Seat limit must be enforced by FR-009 when providers invite staff members.
- **REQ-015-011**: System MUST store activation token (one-time password setup link), token expiry timestamp (24 hours from generation), and the password_set status of the provider owner's login (stored on the owner's team-member record). System MUST invalidate previous tokens when new token is generated.
- **REQ-015-022**: Effective commission configuration MUST be snapshotted at booking confirmation under FR-029 and retained for later transactions; edits in FR-015/FR-029 MUST stay synchronized without replacing existing booking snapshots. Percentage/Flat Rate models and the once-per-completed-procedure flat-fee rule remain unchanged.
- **REQ-015-023**: Provider-profile Completed Procedures MUST count distinct FR-010 treatment completions, not quotes, options, accepted selections, payments, or final aftercare status. Later cancellation MUST NOT erase a recorded completion.
- **REQ-015-024**: System MUST retain provider-status event/effective-time references, affected record identifiers and prior stages, cancellation cause, support marker/resolution audit, slot-release outcome, and notification outcome for lifecycle impact and admin follow-up; storage remains with the existing owning entities rather than duplicating accepted data in Provider.

### Security & Privacy Requirements

- **REQ-015-012**: System MUST encrypt provider documents at rest and in transit.
- **REQ-015-013**: System MUST restrict document access to authenticated users (providers can access their own documents, admins can access all provider documents) with role-based permissions (providers can edit their own uploads, admins can edit admin uploads only).
- **REQ-015-014**: System MUST validate provider login Email against the FR-009 global provider email identity rule (Rule 3, REQ-009-008) on creation and on every change (blocking emails used by another provider organization as Owner, team member, or pending invitation), and MUST validate Contact Email uniqueness among Active and Suspended providers; Deactivated providers' emails are freed so a re-onboarded provider can reuse them.
- **REQ-015-015**: System MUST enforce the platform-wide password policy defined in the Hairline Platform Constitution and shared authentication spec: passwords MUST be at least 12 characters long and include at least 1 uppercase letter, 1 lowercase letter, 1 number, and 1 special character from !@#$%^&(),.?\":{}|<>. This policy is centrally defined and NOT configurable per FR. Passwords MUST be hashed using bcrypt with a minimum cost factor of 12.
- **REQ-015-016**: System MUST rate limit activation email resend requests to 3 per hour per email address to prevent abuse and email flooding.

---

## Key Entities

- **Entity 1 - Provider**
  - **Key attributes**: provider_id (UUID), first_name, last_name, email (login email; FR-009 global provider email identity rule), phone, bio, languages (JSON), awards (JSON), medical_license_number, specialty, years_experience, status (enum: active, suspended, deactivated), featured (boolean), seat_limit (integer, default 100, range 1-500), payout_frequency (enum: weekly, twice_monthly, monthly; required at creation), password_hash (bcrypt hash), password_set (boolean, default false), activation_token (UUID, nullable), activation_token_expiry (timestamp, nullable), activation_email_sent_count (integer, for rate limiting), last_activation_email_sent_at (timestamp), created_at, updated_at.
  - **Relationships**: One provider has many documents, status history records, and FR-004 Parent Quotes (including several for the same inquiry); one provider has one clinic and many FR-006 bookings, each linked to one accepted FR-005 Subquote/AcceptanceEvent. Seat limit is enforced by FR-009. Commission model, value, Flat Rate Currency, and start date (the FR-029 `effective_date`) are not Provider attributes; they are stored as the provider's FR-029 commission configuration (`provider_commissions`), captured in Step 5 and edited in Tab 7. Quote-owned package snapshots and historical booking commission snapshots are not mutable fields of the current Provider profile.

- **Entity 2 - Provider Document**
  - **Key attributes**: document_id (UUID), provider_id (foreign key), document_name, document_type (enum: medical_license, board_certification, insurance, malpractice_insurance, business_license, other), file_url, file_format (PDF, JPG, PNG, DOCX, XLSX), file_size (bytes; max 10MB), upload_date, uploader_type (enum: provider, admin), uploader_id, notes (admin-only), deleted (boolean for soft delete), deleted_at (timestamp).
  - **Relationships**: Many documents belong to one provider.

- **Entity 3 - Clinic Information**
  - **Key attributes**: clinic_id, provider_id, clinic_name (3-200 chars), contact_email (unique among active and suspended providers), logo_url (profile picture), cover_image_url, address_fields, location_city, location_country, contact_phone, website_url, operating_hours.
  - **Relationships**: One clinic belongs to one provider (one-to-one).

- **Entity 4 - Pending Provider Status Change**
  - **Key attributes**: pending_change_id (UUID), provider_id (foreign key), change_type (enum: suspend, deactivate), effective_date (date, future), reason (min 20 chars), notify_provider (boolean), scheduled_by (admin ID), scheduled_at (timestamp), state (enum: pending, applied, cancelled), cancelled_by (admin ID, nullable), cancellation_reason (nullable; includes automatic cancellation on reactivation), resolved_at (timestamp, nullable).
  - **Relationships**: At most one pending record per provider; an immediate suspension/deactivation or a Screen 5 reactivation cancels it. Every state change is written to the provider's status history and Tab 8.

- **Entity 5 - Provider Status Event**
  - **Key attributes**: status_event_id (UUID), provider_id (foreign key), from_status, to_status (enum: active, suspended, deactivated), cause (enum: ProviderSuspended, ProviderDeactivated, ProviderReactivated), reason (admin reason), effective_at (timestamp, UTC), admin_id, notify_provider (boolean), pending_change_id (nullable; set when a Key Entity 4 scheduled change was applied), closure_request_id (nullable; A7), created_at.
  - **Relationships**: One provider has many status events (append-only; never updated after creation). This is the "provider status event" referenced by REQ-015-024 and by the `provider_status_event_id` / `deactivation_event_id` columns on the owning inquiry, booking, aftercare, payment, and closure-request records (`provider_status_events` in system-data-schema.md). Tab 8 displays it but the Tab 8 activity log is not the event record.

**Cross-module lifecycle context (not a new Provider-owned case table)**: Inquiry/ProviderInquiry and Booking/Treatment owners retain the applicable cancellation reason (`ProviderSuspended` or `ProviderDeactivated`), `supportRequired`, triggering provider-status event, effective time, previous stage, and resolution audit. An inquiry with a closed accepted booking stays open while an admin rehomes the patient through the FR-006 provider-fault transfer; an unaccepted shared inquiry retains its normal stage and only the affected provider participation is cancelled. Optional linked FR-034 support-case references retain the existing ticket workflow. The AcceptanceEvent retains the historical accepted IDs, equal aggregate versions, and snapshot, and is superseded only through a linked FR-005 supersession record. The confirmed Booking/financial record retains the confirmation-time commission configuration.

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-11 | 1.0 | Initial PRD creation for FR-015 Provider Management (Admin-Initiated) | Claude (AI Assistant) |
| 2025-12-07 | 1.1 | **Major alignment update with FR-032:** <br>• Added cross-module integration notes linking to FR-032 (Provider Dashboard Settings) in Executive Summary and Module Scope<br>• Removed all document expiration date fields and related workflows (documents are for record-keeping only)<br>• Removed all out-of-scope items: Save Draft functionality, Tier-based commission references, Document verification workflow (approve/reject)<br>• Aligned all profile fields with FR-032: Profile Picture (5MB, 200x200px min), Cover Image (10MB, 1920x300px), Bio/Description (500 chars, min 50), Languages (multi-select chips from FR-026), Awards (with issuer, description, year, image), Contact Phone, Location (City, Country), Website URL<br>• Clarified activation logic: only required fields block activation (First Name, Last Name, Email, Clinic Name, Bio min 50 chars, at least 1 Language); documents do NOT block activation<br>• Updated Success Criteria to remove verification/expiration references and focus on record-keeping approach<br>• Updated Business Workflows, Screen Specifications (Wizard Steps and Tabbed View), User Stories, Edge Cases, and Entity definitions<br>• Added Admin Editability Rules section distinguishing admin-only vs provider-editable fields (via FR-032)<br>• Updated document entity to include document_type, uploaded_by, soft delete fields<br>• **Added Seat Limit field** to Screen 2 Step 1 (Basic Information): Maximum team members (staff) capacity per provider, default 100, range 1-500, adjustable by admin. Aligns with FR-009 team management enforcement. Added to Business Rules (Rule 7), Entity definitions, Functional Requirements (REQ-015-009), and Edge Cases<br>• **Completely restructured Screen 3** to table format matching FR-032 structure with all 5 tabs: (1) Basic Information, (2) Languages, (3) Staff List, (4) Awards, (5) Reviews, plus admin-only tabs: (6) Documents, (7) Commission & Financials, (8) Activity Log. All fields now documented in table format with Admin/Provider editability clearly marked<br>• **Added provider onboarding workflow** to Main Flow: Secure password setup via one-time email link (expires 24 hours), first login prompts profile completion via FR-032, changes sync to admin view<br>• **Added activation email resend functionality** (Alternative Flow A1): Provider self-service resend via login page + Admin manual resend via Quick Actions button in Screen 3. Rate limited to 3 requests/hour, previous tokens invalidated, secure handling of expired links. Added to Edge Cases, Functional Requirements (REQ-015-006, REQ-015-011, REQ-015-015, REQ-015-016), and Entity definitions with activation_token fields<br>• **Enhanced User Story 3** with detailed suspension workflow scenarios including existing appointments handling, suspended login experience, and reactivation process<br>• **Removed redundant User Stories 5 & 6** (provider-side actions) as these are fully covered in FR-032 User Story 1 | Claude (AI Assistant) |
| 2025-12-07 | 1.2 | **Major cross-module update - Document management redesign:** Completely restructured Tab 6: Documents to reflect new document management model. Removed "Admin-Only" designation. Providers now manage their own documents via FR-032 Tab 6 (upload, replace, delete); admin role shifted to oversight and supplementary uploads. Updated tab to display all documents with "Uploaded By" badge (Provider/Admin); Admin can view all documents, upload additional documents received externally (email, postal mail), and add notes, but cannot replace/delete provider-uploaded documents (only provider can via FR-032); Admin-uploaded documents show "Admin - [name]" badge and admin has full control over these. Added bidirectional document sync (FR-032 ↔ FR-015 within 1 minute); Updated Business Rules to clarify provider primary management vs. admin oversight model; Added sort/filter options, audit logging enhancements, and comprehensive use case notes. Aligns with FR-032 v1.2 which added full document management capabilities for providers | Claude (AI Assistant) |
| 2025-12-08 | 1.3 | **Constitution & System PRD alignment update:** <br>• Updated REQ-015-015 to reference the platform-wide password policy from the Hairline Platform Constitution and shared authentication spec (minimum 12 characters, required character classes, bcrypt with minimum cost factor 12, not configurable per FR)<br>• Clarified that sensitive actions (Commission and Seat Limit changes, Commission editing) require admin re-authentication via password in MVP, and MUST transition to MFA-based re-authentication once the shared MFA stack from FR-026 / FR-031 is delivered (all MFA references in this FR are future, non-MVP behavior)<br>• Aligned high-level system behaviour with system-prd.md FR-015 by explicitly reflecting the record-keeping-only document model and Percentage/Flat Rate commission configuration (tier-based commissions deferred to a future FR) | Claude (AI Assistant) |
| 2026-04-02 | 1.4 | Clarified ownership split with FR-029 and FR-017: FR-029 / A-09 remains owner of the global platform commission default and booking-time snapshot policy, while FR-015 / A-02 owns provider-specific commission overrides and payout frequency consumed by FR-017 payout workflows | Codex |
| 2026-04-02 | 1.5 | Restored dual management for provider-specific commission settings: FR-015 remains the single-provider commission and payout-frequency screen, while FR-029 Screen 5 now also manages provider-specific commission scopes centrally; the two admin surfaces are documented as synchronized for the same provider commission data | Codex |
| 2026-04-12 | 1.6 | Cross-FR cleanup: corrected Screen 1 Provider Management Dashboard commission filter from stale "Tier-based" to "Flat Rate" so the list filter matches the module-wide Percentage/Flat Rate commission model and FR-022 search/filter alignment | Codex |
| 2026-08-11 | 1.7 | Aligned featured-provider management with the Sprint 1 A-02 readiness finding: added `Set Featured` / `Unset Featured` Provider-list quick actions, made the Basic Information toggle the existing-provider edit control, changed Commission & Financials to read-only featured-status display, and added the maximum-10 featured-provider rule with required rejection feedback and server-side enforcement | Vân Tay Media |
| 2026-10-13 | 1.8 | Documentation-approved provider lifecycle/subquote alignment through CR-FR015-20261013-01: suspension automatically cancels non-terminal cases with ProviderSuspended and a separate admin-support marker; clarified future-booking deactivation, immutable accepted history, eligibility/payment guards, patient/admin notifications, and no automatic restoration. Aligned commission changes with confirmation-time snapshots and renamed the completed-procedure profile count. Added affected-owner dependencies, requirements, and validation scenarios; related-PRD alignment, consolidated verification, and implementation reconciliation remain pending. | Vân Tay Media |
| 2026-10-14 | 1.9 | FR-015 verification fixes (Product Owner decisions, 2026-10-14):<br>• Commission: FR-029 Screen 5 aligned to the FR-015 provider Percentage (0-100%) or Flat Rate model via CR-FR029-20261014-01<br>• Wizard and entities: added Contact Email (required, unique), Payout Frequency, and Commission Start Date to Screen 2 and Key Entities; Clinic Name 3-200 chars; required set equals the wizard's Required fields, Medical License file required at creation only (Rule 2)<br>• Lifecycle: removed Draft status everywhere; added Screen 5 Provider Reactivation Modal and Alternative Flow A6; deactivation now cancels all non-terminal Accepted, Confirmed, In Progress, and Aftercare cases with `ProviderDeactivated` (downstream CRs beside FR-003, FR-004, FR-010, FR-011, FR-016, FR-020; FR-005 and FR-006 change-log alignment)<br>• Admin controls: mandatory admin change reason (REQ-015-025); Login as Provider reason, re-authentication, banner, restrictions, audit (REQ-015-026); automatic unfeaturing on suspend/deactivate (Rule 6, REQ-015-027)<br>• Documents: FR-032 formats (PDF, JPG, PNG, DOCX, XLSX); 6-type enum; A4 limited to admin-uploaded documents; uploader_type/uploader_id<br>• Reviews: Tab 5 linked to FR-013 Screens 6-8 for admin insert/edit/remove<br>• Dependencies: FR-001/A-01 replaced by FR-031; FR-XXX placeholders resolved (FR-009, FR-022, shared S-05/S-06); added FR-032, FR-013, FR-026<br>• Cascade scope includes FR-011 standalone aftercare (REQ-015-017)<br>• Minor: retention minimum 7 years then archive, never hard-delete; optimistic locking without last-write-wins; concurrency figure aligned to 100; section-name source references<br>• Follow-up (Product Owner, 2026-10-14): flat model named `flat_rate`; commission settings stored in FR-029 `provider_commissions` | Vân Tay Media |
| 2026-10-14 | 1.10 | FR-015 re-verification fixes (Product Owner decisions, 2026-10-14):<br>• Commission: added Flat Rate Currency (FR-029 enabled currency list, default system currency) to Step 5, Tab 1, Tab 7, A2, Key Entities, REQ-015-009 and validation, matching FR-029 Screen 5 and `flat_rate_currency`; snapshot includes the currency<br>• Commission Start Date is the FR-029 provider-specific `effective_date` for newly confirmed bookings; each later commission edit sets its own Effective Date; payout cycles follow Payout Frequency (FR-017 wording aligned)<br>• Screen 4: added Admin Password re-authentication (REQ-015-003 consistency)<br>• Scheduled status changes: pending marker, Cancel Scheduled Change with reason and re-authentication, scheduled deactivation covered (REQ-015-028)<br>• Featured: admin flag and cap stay MVP; patient-facing display, SC-001, SC-021, Integration 4 and US1 scenario 3 marked P2 with FR-022 patient provider search<br>• Removed the undefined Screen 1 Documents Status column<br>• Tab 7 note: payout-frequency and amount-or-percentage pattern applies to providers (FR-015) and affiliates (FR-018, already monthly-only)<br>• Minor: removed residual verification wording (SC-003, Screen 4 example reason), Billing Rule 1 follows Payout Frequency, password_hash is a bcrypt hash, provider licences not labelled PHI, Clinic Address vs public City/Country clarified, Screen 1 "Activate" renamed "Reactivate", suspension/deactivation effect on FR-009 team logins stated | Vân Tay Media |
| 2026-10-15 | 1.11 | FR-015 third verification pass fixes (Product Owner decisions, 2026-10-15):<br>• Provider commission visibility: provider-side read-only commission and payout frequency now point to the FR-032 Screen 4 Commission & Payout panel ([CR-FR032-20261015-01](../fr032-provider-dashboard-settings/change-request-2026-10-15-provider-commission-panel-suspension-banner.md))<br>• Suspended banner: FR-032 Rule 6 owns the Account Suspended banner and read-only behavior<br>• Screen 1: defined Last Activity Date (latest FR-004 Parent Quote submission or FR-006 booking confirmation); added Status Count Tiles (SC-012); commission sort grouped by model, then currency and value<br>• Permissions: replaced undefined Provider Manager and Read-Only Admin roles with FR-031 View, Onboard, Edit, and Suspend Providers permissions; corrected A-01 to FR-031 / A-09<br>• Screen 4: blank or today Effective Date applies immediately<br>• Rule 2: added conditional Flat Rate Currency; Implementation Notes: server-side filtering and sorting | Claude |
| 2026-10-15 | 1.12 | FR-015 fourth verification pass fixes (Product Owner decisions, 2026-10-15):<br>• Tab 7: added Scheduled Configuration (at most one pending future-dated commission configuration per provider; a new future-dated edit replaces it; cancellable with reason and re-authentication; applied automatically on its Effective Date), giving the FR-032 Screen 4 "Scheduled Configuration" field its source<br>• Tab 1: commission fields replaced by a read-only Commission Summary linking to Tab 7; Tab 7 is the only FR-015 commission edit surface<br>• Shared FR-029 scopes: a provider belongs to at most one active provider-specific scope; a Tab 7 edit splits the provider into its own single-provider scope without changing the others ([CR-FR029-20261015-01](../fr029-payment-system-config/change-request-2026-10-15-single-provider-scope-scheduled-commission.md))<br>• A5 and Screen 4: cascade text explicitly includes FR-011 standalone aftercare cases, matching REQ-015-017<br>• Screen 3: admin "Resend Activation Email" shown only when password is not set and status = Active, matching A1 | Claude |
| 2026-10-15 | 1.13 | FR-015 fifth verification pass fixes (Product Owner decisions, 2026-10-15):<br>• Login as Provider: FR-015 limited-write rules kept; FR-009 Impersonate aligned to them ([CR-FR009-20261015-01](../fr009-provider-team-roles/change-request-2026-10-15-admin-staff-invite-impersonation.md))<br>• Tab 3 Staff List: shows only this provider's team and adds Invite Staff Member within the Seat Limit (same CR)<br>• Reactivation: Screen 5 cancels any pending scheduled suspension/deactivation after a warning; logged in Tab 8 (A6, Screen 4, Screen 5); added Key Entity 4 Pending Provider Status Change<br>• Rule 9: FR-017 owns reconciliation of payments captured after suspension/deactivation and stopping remaining installments ([CR-FR017-20261015-01](../fr017-admin-billing-finance/change-request-2026-10-15-post-suspension-payment-reconciliation.md)); Reconciliation boundary lists FR-005, FR-006, FR-007, FR-009, FR-017, FR-026<br>• Specialty: values from the FR-026 managed Provider Specialties list ([CR-FR026-20261015-01](../fr026-app-settings-security/change-request-2026-10-15-provider-specialty-list.md))<br>• Minor: SC-010 says create (Active) and covers scheduled changes; SC-015 lists the real tabs; User Story 3 raised to P1 | Claude |
| 2026-10-15 | 1.14 | FR-015 sixth verification pass fixes (Product Owner decisions, 2026-10-15):<br>• Account closure: added A7 Admin Processes a Provider Account-Closure Request; FR-032 Delete Account becomes a closure request processed as Screen 4 deactivation, with no "Deleted" status ([CR-FR032-20261015-02](../fr032-provider-dashboard-settings/change-request-2026-10-15-account-closure-deactivation-request.md)); closure edge case updated<br>• Notifications: Main Flow step 13, A1, A6, Screen 4 and the FR-020 dependency reference the new mandatory FR-020 events `provider.activation`, `provider.reactivated`, `provider.scheduled_change_cancelled` ([CR-FR020-20261015-01](../fr020-notifications-alerts/change-request-2026-10-15-provider-lifecycle-events.md))<br>• Rule 7: seat-limit increases come from FR-009 "Request more seats" as an FR-034 support case; admin edits Seat Limit in Tab 1<br>• Email uniqueness: login Email and Contact Email are unique among Active and Suspended providers only (Rule 4, Step 1, Step 3, Tab 1, REQ-015-014, Key Entities 1 and 3, duplicate-email edge cases)<br>• Provider-side view: Entry Points and User Story 1 scenario 2 point to FR-032 Screen 4 Billing Settings (Owner only), Tab 6 and the Rule 6 banner<br>• Minor: Main Flow step 6 lists Location City/Country, Contact Phone (Public), Website URL; Step 3 field renamed Contact Phone (Public); commission attributes moved out of Key Entity 1 into a FR-029 `provider_commissions` link note | Claude |
| 2026-10-15 | 1.15 | FR-015 seventh verification pass fixes (Product Owner decisions, 2026-10-15):<br>• Login email: Screen 2 Step 1, Tab 1, Rule 4, REQ-015-014, Key Entity 1, and the duplicate-email edge cases now follow the FR-009 global provider email identity rule (Owners, team members, and pending invitations across all providers; Deactivated providers' emails freed) ([CR-FR009-20261015-02](../fr009-provider-team-roles/change-request-2026-10-15-global-provider-email-identity.md)); Contact Email rule unchanged<br>• Notifications: Integration 1 and Data Dependency Entity 2 use the FR-020 provider lifecycle events (`provider.activation` and others); removed the template ID example<br>• Tab 6: added Upload Document Modal Fields (File, Document Type, Notes)<br>• Minor: module placeholders replaced (P-02, PR-01/PR-06, S-03/S-05/S-06); provider-side "read-only" wording now says providers edit allowed fields via FR-032; Key Entity 2 gains file_size; Data Dependency Entity 1 matches the FR-031 default permission matrix | Claude |
| 2026-10-15 | 1.16 | FR-015 eighth verification pass fixes (Product Owner decisions, 2026-10-15):<br>• Languages: Step 2 and Tab 2 now use the FR-021 central language catalog; added FR-021 dependency; FR-026 dependency no longer claims the language list<br>• Account closure: Notify Provider locked on for closure deactivations (A7, Screen 4, edge case); Screen 1 Closure Requested filter and marker; new FR-020 events `provider.closure_requested` (admins) and `provider.closure_rejected` (provider) ([CR-FR032-20261015-03](../fr032-provider-dashboard-settings/change-request-2026-10-15-closure-request-notifications.md), [CR-FR020-20261015-02](../fr020-notifications-alerts/change-request-2026-10-15-provider-closure-request-events.md), [CR-FR030-20261015-02](../fr030-notification-rules-config/change-request-2026-10-15-provider-closure-request-events.md))<br>• Commission: Tab 7 edits allowed for Active and Suspended providers, read-only for Deactivated ([CR-FR029-20261015-02](../fr029-payment-system-config/change-request-2026-10-15-suspended-provider-commission-scopes.md)); Step 5 and Tab 7 Commission Value precision follows FR-029 (0.1% or currency minor units)<br>• Distribution: providers with `password_set = false` are excluded from inquiry distribution (Main Flow steps 12 and 21, Rules 3 and 9, FR-003 dependency; [CR-FR003-20261015-01](../fr003-inquiry-submission/change-request-2026-10-15-distribution-requires-password-set.md))<br>• Integration 4: REST only, public read-only endpoint with rate limiting | Claude |
| 2026-10-16 | 1.17 | MTG-002 quote model alignment ([CR-FR015-20261016-01](change-request-2026-10-16-mtg002-quote-model-alignment.md)):<br>• Commission Rule 2: the Percentage base is the booking total, defined as the accepted price after promotion, in the quote currency, read from the FR-005 acceptance snapshot; commission settings still lock at booking confirmation (FR-015-1; D12, M5)<br>• Provider suspension or deactivation after acceptance: A5, Screen 4, Rule 9, Rule 10, Cancellation Billing Rule, FR-003/FR-004/FR-005/FR-006 dependencies, US3, the deactivation edge case, REQ-015-017 to REQ-015-019, and Key Entities now hand closed accepted bookings to the FR-006 B4/B5 provider-fault transfer; the inquiry stays open, the accepted parent quote keeps `accepted`, the AcceptanceEvent is superseded through a linked FR-005 record, an admin rehomes the patient to a replacement provider, and money follows the B5 payment placeholder; removed inquiry cancellation and the "no automatic refund or reselection" wording. Before acceptance, unaccepted quotes are still cancelled with `cancelled_provider_status` (M18, D6, D6-M; FR-015-3, FR-015-4)<br>• Patient notice for closed accepted bookings: an admin will arrange a replacement provider via FR-020/FR-030 `booking.provider_fault_replacement`; `provider.status_cancellation_patient` now applies only before acceptance (M18)<br>• Key Entities: the AcceptanceEvent keeps accepted IDs, versions and snapshot; the confirmed booking/financial record keeps the confirmation-time commission configuration (FR-015-2)<br>• A5 and Screen 4 name `Accepted` as an FR-006 booking stage (FR-015-6)<br>• CR-FR015-20261016-01 added (P1) | Claude (AI Assistant) |
| 2026-10-16 | 1.18 | Product Owner follow-up decision ([CR-FR015-20261016-01](change-request-2026-10-16-mtg002-quote-model-alignment.md)):<br>• Commission Rule 2: states that commission is on the price after promotion for every discount type, including Hairline-funded discounts (Q5). | Product Owner / Documentation |
| 2026-10-18 | 1.19 | Consolidated verification corrections ([CR-FR015-20261016-01](change-request-2026-10-16-mtg002-quote-model-alignment.md)): REQ-015-017 now cancels only the provider's unaccepted Parent Quotes with `cancelled_provider_status` and closes non-terminal bookings, and states that an accepted Parent Quote keeps `accepted` (M18). | Product Owner / Documentation |
| 2026-10-26 | 1.21 | Dev-team question resolution (Product Owner decisions, 2026-10-26):<br>• Added Key Entity 5 Provider Status Event (dedicated append-only table `provider_status_events`) as the target of every `provider_status_event_id` / `deactivation_event_id` reference<br>• Screen 5 Unresolved Support Items counts affected inquiries and cases (one per record, matching the FR-020 admin-support alert unit)<br>• Suspended providers are read-only on `In Progress` bookings; the admin decides via FR-006 B7<br>• "Today" for Screen 4 and Tab 7 Effective Dates is the current UTC date<br>• Login as Provider opens in a new tab and ends on End Session or 30-minute inactivity (no absolute cap)<br>• Screen 2 leave-wizard prompt reuses the FR-032 unsaved-changes text (no drafts); creation success message; Tab 2 empty-language message; Rule 8 featured-cap message<br>• Featured toggle and document Replace need no change reason; Replace archives the old file<br>• Invalid commission rate returns 422 with PRD wording (was 400)<br>• Review follow-up: Step 5 Commission Start Date "today" is the UTC date; seat-limit team size is FR-009 seat usage (members plus pending invitations)<br>• Open-item follow-up: upload error messages (wrong format, too large, below minimum dimensions) added after the wizard steps; REQ-015-011 `password_set` belongs to the owner's login | Claude (AI Assistant) |
| 2026-10-18 | 1.20 | Final audit corrections ([CR-FR015-20261016-01](change-request-2026-10-16-mtg002-quote-model-alignment.md)):<br>• A5, Screen 4, Rules 9 and 10, dependencies, Assumption 4, User Story 3, edge cases, and REQ-015-017: `Aftercare` bookings and FR-011 standalone aftercare cases are no longer closed; they keep their status, get the cause and support marker, and move to admin aftercare reassignment through FR-006 Alternative Flow B6 and FR-011, with no new acceptance or payment (Q36).<br>• A5 step 7: the transfer starts from Start Provider-Fault Transfer on FR-006 Screen 6 (Screen 10) with an admin-authored replacement quote (Q35).<br>• Screen 4: new Admin action links rule and REQ-015-029 linking each affected record to its resolving admin screen (Q43).<br>• Later the same day: an `In Progress` booking under a provider-status event is no longer closed; it stays `In Progress` with `supportRequired` and an admin decides on FR-006 Screen 6 to move it to Aftercare with aftercare reassignment or cancel it (Alternative Flow A5 steps 3 to 5 and 7, Outcome, Deactivation, Screen 4, Rule 10, FR-010/FR-011 dependency, Assumption 4, REQ-015-017, User Story scenarios) (Q45). The aftercare reassignment patient notice is named as the FR-011 event `aftercare.provider_reassigned` (Q47). | Product Owner / Documentation |
| 2026-10-27 | 1.22 | Dev-team follow-up question resolution (Product Owner decisions, 2026-10-27; [CR-FR015-20261027-01](change-request-2026-10-27-save-conflict-encryption-seat-usage.md)):<br>• Concurrent edits: removed optimistic locking; the last save wins for admin (FR-015) and provider (FR-032) saves, with no conflict message (CR)<br>• Security: provider email, phone, and medical license number are protected by database/disk encryption at rest, HTTPS/TLS, and access control instead of application-level encryption, so partial search and email uniqueness keep working (CR)<br>• Seat usage: accepted non-Owner team members plus pending invitations; the Owner and expired invitations do not count (Seat Limit fields and edge case; CR, with FR-009)<br>• Login as Provider: allowed for Active and Suspended providers, blocked for Deactivated; read-only per FR-032 Rule 6 for a Suspended provider; applies to the Owner and team members (REQ-015-026)<br>• Rule 9 and REQ-015-020: admin Revive Booking, admin appointment change (reschedule), and admin acceptance of a replacement quote (FR-006 B5) also require an Active provider (FR-006 REQ-006-020, [CR-FR006-20261027-02](../fr006-booking-scheduling/change-request-2026-10-27-admin-actions-require-active-provider.md))<br>• Tab 1: Owner login email change requires password re-authentication and a reason, notifies the old and new addresses, signs the Owner out and revokes tokens, and re-sends a pending activation link to the new address<br>• Screen 4: provider status emails are sent when a scheduled change is created and again when it takes effect (only with Notify Provider), and go to the Owner only; a suspended provider may still chat with patients on open In Progress and Aftercare cases<br>• A5 and REQ-015-020: status change and status event in one transaction; the cascade runs as an idempotent background job (target 5 minutes); reactivation does not stop a running cascade<br>• Tab 7, Screen 1, Tab 1: deactivation cancels a pending scheduled commission configuration; global default shown as "(Default)"; future-only configuration shows a "Scheduled" tag<br>• A7 and Screen 1: a closure request with a scheduled deactivation stays pending until the deactivation takes effect; cancelling the scheduled change leaves it pending<br>• Admin-support alert and Resolve Support follow FR-031 Respond to Support; the FR-016 list needs View Patients (aligned with [CR-FR020-20261027-01](../fr020-notifications-alerts/change-request-2026-10-27-admin-support-recipients-status-email-timing.md))<br>• Wording: one creation success message (User Story 1), one email-delay warning, FR-005 supersession only when the admin accepts the replacement quote, Tab 8 CSV export rules, Resend Activation Email permission, wizard leave prompt without Save | Product Owner / Documentation |

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
| Product Owner | Joachim Trung Tuan | 2026-10-18 | Approved FR-015 v1.19 and v1.20 via MTG-002 decision log (documentation only), including [CR-FR015-20261016-01](change-request-2026-10-16-mtg002-quote-model-alignment.md) |
| Product Owner | Joachim Trung Tuan | 2026-10-27 | Approved FR-015 v1.22 dev-team follow-up decisions (documentation only), including CR-FR015-20261027-01; implementation reconciliation pending |

Historical verification above applies to the prior baseline, not the new v1.8 cancellation/support contracts. The Product Owner's "all related treatment" scope is documented as all non-terminal Accepted, Confirmed, In Progress, and Aftercare cases; completed and already-terminal history remains unchanged. Other owning PRDs require separate controlled alignment before this change is considered cross-FR verified.

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B
**Based on**: system-prd.md (§ FR-015: Provider Management (Admin-Initiated))
**Last Updated**: 2026-10-27
