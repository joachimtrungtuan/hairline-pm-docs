# Hairline Platform - Database Schema

**Version**: 1.11.0  
**Document Type**: System-Level Data Schema  
**Created**: 2025-10-23  
**Status**: Active  
**Last Updated**: 2026-10-18

---

## Executive Summary

This document provides a comprehensive overview of the Hairline Platform database schema, including all entities, relationships, constraints, and data types. The schema is implemented using **MySQL 8.0+** and follows Laravel migration conventions.

### Schema Overview

- **Total Tables**: 116 tables (see Complete Table List)
- **Primary Key Type**: UUID (string) for user-facing entities, auto-increment for system tables
- **Character Set**: utf8mb4_unicode_ci (supports emoji and international characters)
- **Storage Engine**: InnoDB (supports foreign keys and transactions)
- **Soft Deletes**: Enabled for critical entities (patients, providers, treatments). Quotes are not soft-deleted: once an acceptance record references a quote, the quote is retained permanently
- **Hard Deletes**: PROHIBITED for all medical, financial, and patient data (7-year minimum retention)

---

## Entity Relationship Overview

```markdown
┌─────────────────────────────────────────────────────────────────────┐
│                        CORE WORKFLOW                                │
│                                                                     │
│  ┌─────────┐      ┌─────────┐      ┌───────┐      ┌──────────┐      │
│  │ Patient │─────►│ Inquiry │─────►│ Quote │─────►│Treatment │      │
│  └─────────┘      └─────────┘      └───────┘      └──────────┘      │
│       │                 │               │               │           │
│       │                 │               │               ▼           │
│       │                 │               │         ┌──────────┐      │
│       │                 │               └────────►│AfterCare │      │
│       │                 │                         └──────────┘      │
│       │                 ▼                                           │
│       │           ┌──────────┐                                      │
│       └──────────►│  Medical │                                      │
│                   │ History  │                                      │
│                   └──────────┘                                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    PROVIDER ECOSYSTEM                               │
│                                                                     │
│  ┌──────────┐      ┌──────────┐      ┌───────────┐                  │
│  │ Provider │◄─────│ Provider │      │ Treatment │                  │
│  │          │      │   User   │      │ (Package) │                  │
│  └──────────┘      └──────────┘      └───────────┘                  │
│       │                  │                  │                       │
│       ├─────────────┬────┴────┬─────────────┘                       │
│       ▼             ▼         ▼                                     │
│  ┌────────┐   ┌──────────┐ ┌────────┐                               │
│  │Document│   │ Language │ │ Award  │                               │
│  └────────┘   └──────────┘ └────────┘                               │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    ADMIN & SUPPORT                                  │
│                                                                     │
│  ┌──────┐      ┌───────────┐      ┌──────────┐                      │
│  │ User │      │ Affiliate │      │ Location │                      │
│  └──────┘      └───────────┘      └──────────┘                      │
│     │                │                   │                          │
│     ▼                ▼                   ▼                          │
│  ┌──────┐      ┌──────────┐      ┌──────────┐                       │
│  │ Role │      │ Discount │      │ Starting │                       │
│  │      │      │   Code   │      │  Prices  │                       │
│  └──────┘      └──────────┘      └──────────┘                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Core Entities

### 1. Patients

**Table**: `patients`  
**Description**: End-users seeking hair transplant procedures

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique patient identifier |
| first_name | VARCHAR(255) | NOT NULL | Patient's first name |
| last_name | VARCHAR(255) | NOT NULL | Patient's last name |
| username | VARCHAR(255) | UNIQUE, NOT NULL | Unique username for login |
| patient_code | VARCHAR(255) | UNIQUE, NULLABLE | Human-readable patient code (e.g., PAT-001) |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Patient's email address |
| password | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| birthday | DATE | NULLABLE | Date of birth |
| gender | VARCHAR(255) | NULLABLE | Gender (male, female, other) |
| phone_number | VARCHAR(255) | NULLABLE | Phone number with country code |
| location | VARCHAR(255) | NULLABLE | City/Country |
| location_id | UUID | FOREIGN KEY, NULLABLE | References locations.id |
| profile_image | VARCHAR(255) | NULLABLE | S3 path to profile image |
| activation_code | VARCHAR(255) | NULLABLE | Email verification code |
| email_verified_at | TIMESTAMP | NULLABLE | Email verification timestamp |
| status | VARCHAR(255) | NULLABLE | Current patient status in workflow (inquiry, quote, accepted, etc.) |
| anonymization_level | VARCHAR(255) | DEFAULT 'full' | Anonymization level: full (before payment), partial (payment pending), none (payment completed) |
| remember_token | VARCHAR(100) | NULLABLE | Remember me token |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |
| deleted_at | TIMESTAMP | NULLABLE | Soft delete timestamp |

**Indexes**:

- PRIMARY: `id`
- UNIQUE: `email`, `username`, `patient_code`
- INDEX: `location_id`, `status`

**Relationships**:

- `hasMany` → `Inquiry`
- `hasMany` → `Review`
- `hasMany` → `Questionnaire`
- `hasMany` → `PatientConsent`
- `belongsTo` → `Location`

---

### 2. Providers

**Table**: `providers`  
**Description**: Clinics or hospitals offering hair transplant services

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique provider identifier |
| user_id | UUID | FOREIGN KEY, NULLABLE | References users.id (owner account) |
| provider_name | VARCHAR(255) | NOT NULL | Clinic/Hospital name (FR-015 `clinic_name`, 3-200 characters) |
| email | VARCHAR(255) | NOT NULL | Primary contact email (FR-015 `contact_email`); unique among `active` and `suspended` providers only (FR-015 v1.14 Rule 4) |
| phone_number | VARCHAR(255) | NULLABLE | Contact phone number |
| profile_image | VARCHAR(255) | NULLABLE | S3 path to logo/image |
| provider_bio | TEXT | NULLABLE | Provider description and credentials |
| specialty_id | UUID | FOREIGN KEY, NOT NULL | References provider_specialties.id (§39); FR-015 Specialty, chosen from active FR-026 Provider Specialties values |
| city | VARCHAR(255) | NOT NULL | City where provider is located |
| country | VARCHAR(255) | NOT NULL | Country where provider is located |
| status | VARCHAR(255) | DEFAULT 'active' | Provider account status: `active`, `suspended`, `deactivated` only (FR-015 v1.9). There is no `draft` status; a provider is created directly as `active` |
| password_set | BOOLEAN | NOT NULL, DEFAULT false | Whether the owner has set a password through the FR-015 activation link (FR-015 REQ-015-011); set to true when the password is first saved |
| activation_token_hash | VARCHAR(255) | NULLABLE, UNIQUE | Hash of the one-time password setup token sent in the FR-015 activation email (REQ-015-011); the raw token is never stored. NULL once the password is set |
| activation_token_expires_at | TIMESTAMP | NULLABLE | Token expiry, 24 hours after generation (REQ-015-011) |
| featured | BOOLEAN | DEFAULT false | Featured-provider flag; cleared automatically when the provider becomes `suspended` or `deactivated` and never restored by reactivation |
| payout_frequency | VARCHAR(255) | NOT NULL | Provider payout cadence: `weekly`, `twice_monthly`, `monthly`; required at creation (FR-015) |
| timezone | VARCHAR(255) | NULLABLE | Provider's timezone (e.g., Europe/Istanbul) |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |
| deleted_at | TIMESTAMP | NULLABLE | Soft delete timestamp |

**Indexes**:

- PRIMARY: `id`
- UNIQUE (partial): `email` WHERE `status` IN ('active', 'suspended')
- INDEX: `user_id`, `status`, `country`, `city`, `specialty_id`, `email`
- INDEX: (`status`, `password_set`) for inquiry distribution eligibility

**Business Rules (FR-015 v1.9, FR-029)**:

- Provider commission settings (model, value, Flat Rate currency, start date) are not stored on `providers`; they live in `provider_commissions` (§2B), which FR-015 Tab 7 and FR-029 Screen 5 read and write. `payout_frequency` stays on `providers`.
- The commission model, value, and Flat Rate currency are snapshotted onto the booking at confirmation (see §11A Bookings); later provider edits never change a confirmed booking.
- Every admin edit to provider data requires a change reason stored in the audit log (see Audit Trail).
- Status change to `suspended` or `deactivated` triggers the provider-status cancellation cascade (see Provider-Status Cancellation Fields under §5 Inquiries) and clears `featured`. Reactivation restores nothing.
- Retention: data of a `deactivated` provider is kept for at least 7 years and then archived; provider records are never hard-deleted.
- There is no `deleted` provider status. An approved FR-032 account-closure request (§40) is applied as an FR-015 deactivation (FR-015 v1.14, FR-032 v1.8).
- Email reuse: a `deactivated` provider's contact email does not block a new provider account; contact email uniqueness counts only `active` and `suspended` providers (FR-015 v1.15 Rule 4, REQ-015-014). Owner and team login emails follow the global provider email identity rule (FR-009 Rule 3, REQ-009-008; FR-015 v1.15 REQ-015-014) in §3 and §4. The deactivated record keeps its email unchanged.
- A future-dated suspension or deactivation is stored in `provider_pending_status_changes` (§38), not in `status`. Reactivation cancels any pending row (FR-015 v1.13).
- `specialty_id` must reference an active specialty when set or changed; a stored value whose specialty is later deactivated stays valid and still displays (FR-026 v1.11).
- Inquiry distribution eligibility (FR-015 v1.16 Rule 3, FR-003 v2.8 REQ-003-019): a provider receives allocations, explicit patient selections, and reassignments only when `status` = 'active' AND `password_set` = true. Turning `password_set` true does not re-send inquiries distributed earlier.
- Activation token (FR-015 REQ-015-011, A1): each provider holds at most one valid token. Generating a new token (creation, provider self-service resend, or admin Resend Activation Email) overwrites the hash and expiry, which invalidates the previous link. A token is accepted only when its hash matches, `activation_token_expires_at` is in the future, `password_set` = false, and `status` = 'active'. Saving the password sets `password_set` = true and clears both token columns. The 3-per-hour resend limit is enforced by the application, not stored here.
- Provider languages (`provider_languages`) reference the FR-021 central language catalog (`languages`), not an FR-026 list (FR-015 v1.16). A language later removed from the catalog still displays but cannot be newly selected.

**Relationships**:

- `belongsTo` → `User`
- `belongsTo` → `ProviderSpecialty`
- `hasMany` → `ProviderPendingStatusChange`
- `hasMany` → `ProviderUser` (team members)
- `hasMany` → `Quote`
- `hasMany` → `Treatment`
- `hasMany` → `ProviderDocument`
- `hasMany` → `ProviderCommission`
- `hasMany` → `ProviderAward`
- `hasMany` → `ProviderLanguage`
- `hasMany` → `ProviderMedia`
- `hasMany` → `Review`

---

### 2A. Provider Documents

**Table**: `provider_documents`  
**Description**: Credential and compliance documents uploaded for a provider by the provider or by an admin (FR-015)

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique document identifier |
| provider_id | UUID | FOREIGN KEY, NOT NULL | References providers.id |
| document_name | VARCHAR(255) | NOT NULL | Display name of the document |
| document_type | VARCHAR(255) | NOT NULL | `medical_license`, `board_certification`, `insurance`, `malpractice_insurance`, `business_license`, `other` |
| file_url | VARCHAR(500) | NOT NULL | S3 path to the stored file |
| file_format | VARCHAR(10) | NOT NULL | Allowed formats: PDF, JPG, PNG, DOCX, XLSX |
| uploader_type | VARCHAR(255) | NOT NULL | Who uploaded the document: `provider` or `admin` |
| uploader_id | UUID | NOT NULL | References provider_users.id when `uploader_type` is `provider`, users.id when `admin` |
| notes | TEXT | NULLABLE | Admin-only notes; never exposed to provider or patient views |
| uploaded_at | TIMESTAMP | NOT NULL | Upload date |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |
| deleted_at | TIMESTAMP | NULLABLE | Soft delete timestamp; documents are never hard-deleted |

**Indexes**:

- PRIMARY: `id`
- INDEX: `provider_id`, `document_type`, `deleted_at`

**Relationships**:

- `belongsTo` → `Provider`

---

### 2B. Provider Commissions

**Table**: `provider_commissions`  
**Description**: Commission rate configuration (FR-029 Entity 6). Holds the single active global default and provider-specific configurations; FR-015 Tab 7 and FR-029 Screen 5 manage the same provider-specific rows. Superseded rows are archived, which keeps the rate history

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique configuration identifier (FR-029 `config_id`) |
| scope | VARCHAR(255) | NOT NULL | `global` or `provider_specific` |
| provider_id | UUID | FOREIGN KEY, NULLABLE | References providers.id; NULL for `global`. An FR-029 multi-provider assignment writes one row per provider, so a provider belongs to at most one active provider-specific configuration |
| commission_model | VARCHAR(255) | NOT NULL, DEFAULT 'percentage' | `percentage` or `flat_rate`; `global` is always `percentage` |
| commission_percentage | DECIMAL(5,2) | NULLABLE | Percentage model only: 0-100% for provider scope (0.1% precision), 15-25% for the global default; NULL for `flat_rate` |
| flat_rate_amount | DECIMAL(10,2) | NULLABLE | `flat_rate` only: fixed amount > 0 deducted once per FR-010 completed procedure; NULL for `percentage` |
| flat_rate_currency | VARCHAR(3) | NULLABLE | `flat_rate` only: an FR-029 enabled currency, defaulting to the system currency; NULL for `percentage` |
| effective_date | DATE | NOT NULL | Date the terms take effect (FR-015 `commission_start_date`); today or later when set. Today applies immediately as `active`; a future date creates a `pending` row |
| status | VARCHAR(255) | NOT NULL, DEFAULT 'active' | `pending`, `active`, or `archived` |
| created_by_admin_id | UUID | FOREIGN KEY, NOT NULL | References users.id |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `scope`, `status`
- INDEX: `provider_id`, `status`, `effective_date`
- UNIQUE (partial): `provider_id` WHERE `status` = 'active' AND `scope` = 'provider_specific'
- UNIQUE (partial): `provider_id` WHERE `status` = 'pending' AND `scope` = 'provider_specific'

**Business Rules (FR-015 v1.12, FR-029 v1.9)**:

- At most one `active` row per provider and exactly one `active` `global` row. An edit archives the current row and inserts a new one, with the admin change reason in the audit log.
- At most one `pending` row per provider (CR-FR029-20261015-01). Saving a newer future-dated configuration archives the existing `pending` row; an admin cancel (reason and re-authentication) also archives it. Both are audit-logged.
- On its `effective_date`, a scheduled job archives the provider's `active` row and changes the `pending` row to `active`. FR-015 Tab 7, FR-029 Screen 5, and FR-032 Screen 4 read the `pending` row as the Scheduled Configuration.
- An FR-015 Tab 7 edit to a provider assigned through an FR-029 multi-provider configuration replaces only that provider's row (the split); other providers' rows are unchanged.
- A provider without an active provider-specific row uses the global default.
- Provider-specific rows can be inserted, scheduled, or archived only while `providers.status` is `active` or `suspended`. A `deactivated` provider's rows are read-only (FR-015 v1.16 Tab 7, FR-029 v1.10, CR-FR029-20261015-02).
- FR-015 `commission_value` maps to `commission_percentage` for `percentage` and to `flat_rate_amount` (with `flat_rate_currency`) for `flat_rate`.
- The model, value, and currency in effect at booking confirmation are snapshotted onto the booking (see §11A Bookings); later rows never change a confirmed booking.

**Relationships**:

- `belongsTo` → `Provider` (NULL for global)
- `belongsTo` → `User` (created_by_admin_id)

---

### 3. Users (Admin/Staff)

**Table**: `users`  
**Description**: Hairline admin team and provider owners

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique user identifier |
| username | VARCHAR(255) | UNIQUE, NOT NULL | Username for login |
| firstname | VARCHAR(255) | NOT NULL | First name |
| lastname | VARCHAR(255) | NOT NULL | Last name |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Email address |
| password | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| avatar | VARCHAR(255) | NULLABLE | S3 path to avatar image |
| role | VARCHAR(255) | NULLABLE | Legacy role field (deprecated in favor of Spatie permissions) |
| email_verified_at | TIMESTAMP | NULLABLE | Email verification timestamp |
| remember_token | VARCHAR(100) | NULLABLE | Remember me token |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- UNIQUE: `email`, `username`

**Business Rules (FR-015 v1.15, FR-009 v1.5)**:

- **Global provider email identity**: per the global provider email identity rule (FR-009 Rule 3, REQ-009-008; FR-015 v1.15 REQ-015-014), a login email belongs to at most one provider organization at a time, counted across provider owner accounts (`users` linked to a provider), team members (§4 `provider_users`), and pending invitations (`provider_staff_invitations`). Records of a `deactivated` provider do not count; their emails are freed for reuse, while the records stay archived and are not reactivated by reuse.
- The check runs on FR-015 provider creation, FR-015 owner login-email edits, and FR-009 staff invitations. Because the three tables are separate, a per-table UNIQUE index cannot enforce it alone: the system needs a shared application-level check (or a shared identity table) plus per-table indexes scoped to non-deactivated providers. The global UNIQUE on `users.email` must be scoped so archived owner accounts of deactivated providers do not block reuse; the mechanism (for example, a partial index, or releasing the email on deactivation while keeping it in the audit trail) is subject to implementation reconciliation.

**Relationships**:

- `hasMany` → `Provider`
- `hasMany` → `Treatment`
- `belongsToMany` → `Role` (via Spatie permissions)
- `belongsToMany` → `Permission` (via Spatie permissions)

---

### 4. Provider Users (Team Members)

**Table**: `provider_users`  
**Description**: Staff members working for a provider (doctors, coordinators, admins)

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique team member identifier |
| provider_id | UUID | FOREIGN KEY, NOT NULL | References providers.id |
| firstname | VARCHAR(255) | NOT NULL | First name |
| lastname | VARCHAR(255) | NOT NULL | Last name |
| title | VARCHAR(255) | NULLABLE | Job title (e.g., Surgeon, Coordinator) |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Email address |
| password | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| phone_number | VARCHAR(255) | NULLABLE | Contact phone |
| profile_image | VARCHAR(255) | NULLABLE | S3 path to profile image |
| status | VARCHAR(255) | DEFAULT 'active' | Account status (active, inactive, suspended) |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |
| deleted_at | TIMESTAMP | NULLABLE | Soft delete timestamp |

**Indexes**:

- PRIMARY: `id`
- UNIQUE: `email`
- INDEX: `provider_id`, `status`

**Business Rules (FR-015 v1.15, FR-009 v1.5)**:

- Team member emails follow the global provider email identity rule in §3: a `provider_users.email` must not match another non-deactivated provider's owner login, team member, or pending invitation. Team member and pending-invitation emails of a `deactivated` provider are freed for reuse (same reconciliation note as §3); the global UNIQUE on `email` must be scoped accordingly.

**Relationships**:

- `belongsTo` → `Provider`
- `belongsToMany` → `Role` (via Spatie permissions)

---

**Table**: `provider_activity_logs`
**Description**: Audit log of all provider team member actions (logins, role changes, invitations, etc.). Used as the canonical source for provider engagement analytics (last active timestamp).

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique log entry identifier |
| provider_id | UUID | FOREIGN KEY, NOT NULL | References providers.id |
| provider_user_id | UUID | FOREIGN KEY, INDEX | References provider_users.id |
| actor_id | UUID | NULLABLE, INDEX | ID of the actor performing the action |
| actor_type | VARCHAR(255) | NULLABLE | Actor type: provider, hairline, system |
| action_type | VARCHAR(100) | NOT NULL | Action performed (login, invitation.sent, role.updated, etc.) |
| description | VARCHAR(500) | NULLABLE | Human-readable description |
| related_entity_type | VARCHAR(100) | NULLABLE | Type of related entity |
| related_entity_id | VARCHAR(100) | NULLABLE | ID of related entity |
| metadata | JSON | NULLABLE | Additional context (IP, user agent, etc.) |
| action_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | When the action occurred |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `provider_user_id`
- INDEX: `actor_id`
- COMPOSITE: `(provider_id, action_at)`, `(provider_user_id, action_at)`

**Relationships**:

- `belongsTo` → `Provider`
- `belongsTo` → `ProviderUser`

**Analytics usage**: Last active date for a provider = `MAX(action_at)` from this table filtered by `provider_id`. Last login = `MAX(action_at) WHERE action_type = 'login'` filtered by `provider_user_id`.

---

### 5. Inquiries

**Table**: `inquiries`  
**Description**: Patient's request for treatment quotes from providers

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique inquiry identifier |
| patient_id | UUID | FOREIGN KEY, NOT NULL | References patients.id |
| problem | VARCHAR(255) | NOT NULL | Main hair loss concern |
| scan_url | VARCHAR(255) | NOT NULL | S3 path to head scan capture assets (V1 photo set; V2 3D scan) |
| treatment_schedule | JSON | NOT NULL | **Legacy** copy of the preferred treatment date ranges; each patient-requested range is stored with a stable ID in `inquiry_date_ranges` (§5B), which quotes reference |
| problem_details | TEXT | NOT NULL | Detailed description of concern |
| nature_of_concern | VARCHAR(255) | NULLABLE | Type of hair loss (genetic, alopecia, etc.) |
| duration_of_concern | VARCHAR(255) | NULLABLE | How long has problem existed |
| previous_treatments | VARCHAR(255) | NULLABLE | Past treatments attempted |
| symptom_severity | VARCHAR(255) | NULLABLE | Severity level (mild, moderate, severe) |
| lifestyle_factors | VARCHAR(255) | NULLABLE | Relevant lifestyle information |
| additional_files | VARCHAR(255) | NULLABLE | Additional photos/documents |
| additional_notes | VARCHAR(255) | NULLABLE | Extra notes from patient |
| status | VARCHAR(255) | NOT NULL, DEFAULT 'inquiry' | Inquiry stage (FR-003): `inquiry`, `quoted`, `accepted`, `confirmed`, `in_progress`, `aftercare`, `completed`, `cancelled` (displayed as Inquiry, Quoted, Accepted, Confirmed, In Progress, Aftercare, Completed, Cancelled; separate from quote statuses; see §7 Case lifecycle note) |
| cancelled_at | TIMESTAMP | NULLABLE | Set when the inquiry moves to `cancelled` (patient cancellation in Inquiry or Quoted, or admin booking cancellation after acceptance) |
| cancellation_reason | VARCHAR(255) | NULLABLE | Patient cancellation reason, or the mandatory admin reason when an admin cancels the booking |
| support_required | BOOLEAN | DEFAULT false | Independent `supportRequired` marker (not a status); cleared only by audited admin resolution |
| support_resolved_at | TIMESTAMP | NULLABLE | When an admin resolved the support marker |
| support_resolved_by | UUID | FOREIGN KEY, NULLABLE | References users.id (resolving admin) |
| support_resolution_reason | TEXT | NULLABLE | Mandatory admin resolution reason recorded when the marker is cleared |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `patient_id`, `created_at`
- INDEX: `status`
- INDEX: `support_required`

**Inquiry stages**: the stage values follow FR-003. Legacy values are retired: `requested` maps to `inquiry`, `offers` maps to `quoted`, and a row still in `scheduled` maps to the stage of its booking. From acceptance onward the patient cannot cancel in the app; only an admin cancels the booking, from any booking state, with a mandatory reason and an audit entry, and the inquiry then moves to `cancelled` while the accepted quote stays `accepted`.

**Provider-Status Cancellation (FR-015 v1.9)**: Provider suspension or deactivation never cancels an inquiry. The cause fields (`cancellation_cause`, `provider_status_event_id`, `provider_status_effective_at`, `prior_stage`) are stored on the affected provider participation in `inquiry_providers` (§5A), on the booking (§11A), and on standalone aftercare (§13). For an Accepted or Confirmed booking of that provider, the booking (§11A) is cancelled with the cause and `support_required = true`, the accepted quote stays `accepted`, and the inquiry is not cancelled: it stays open with `support_required = true` so that an admin can rehome the patient in the same inquiry through the FR-006 provider-fault transfer. The AcceptanceEvent is superseded only when the replacement acceptance is recorded (§7J). An In Progress booking of that provider is not cancelled automatically: it stays `in_progress` with `support_required = true`, and an admin decides the case on the FR-006 intervention screen (§11A). For a booking in Aftercare, the booking and treatment record stay and an admin reassigns the aftercare provider or team (§13). Quotes that were not accepted move to `cancelled_provider_status` with the cause in `quotes.cancellation_provenance` (§7). Rules:

- `support_required` is a boolean marker, not a status. It is cleared only by an admin resolution that records `support_resolution_reason`, `support_resolved_by`, and `support_resolved_at` in the audit trail.
- A `ProviderSuspended` cause is never overwritten when the provider is later deactivated; reactivation restores no cancelled case.
- Provider eligibility (status `active`) is revalidated at allocation, quote submission, quote acceptance, and booking-confirming payment.

**Relationships**:

- `belongsTo` → `Patient`
- `hasMany` → `InquiryProvider` (§5A)
- `hasMany` → `InquiryDateRange` (§5B)
- `hasMany` → `Quote`
- `hasOne` → `MedicalHistory`
- `hasMany` → `WorkflowTimeline`

---

### 5A. Inquiry Providers

**Table**: `inquiry_providers`
**Description**: One provider's participation in an inquiry (FR-003 ProviderInquiry). It holds the distribution time used by FR-014 and the provider-status cancellation of that provider's participation.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique participation identifier |
| inquiry_id | UUID | FOREIGN KEY, NOT NULL | References inquiries.id |
| provider_id | UUID | FOREIGN KEY, NOT NULL | References providers.id |
| source | VARCHAR(255) | NULLABLE | How the inquiry reached the provider (normal distribution or exclusive routing) |
| distributed_at | TIMESTAMP | NOT NULL | Set once when the inquiry is distributed to this provider, including release to normal distribution after an exclusive provider declines; retries and re-sends never overwrite it. Start point of FR-014 time to first quote and response rate and of the `inquiry.ttfq_sla_breached` alert |
| viewed_at | TIMESTAMP | NULLABLE | First time the provider viewed the inquiry |
| status | VARCHAR(255) | NOT NULL | Participation status; `cancelled` when only this provider's participation is cancelled by its suspension or deactivation (the record is retained and never reopened by reactivation) |
| cancellation_cause | VARCHAR(255) | NULLABLE | `ProviderSuspended` or `ProviderDeactivated`; a `ProviderSuspended` cause is never overwritten by a later deactivation |
| provider_status_event_id | UUID | NULLABLE | Reference to the provider status-change event |
| provider_status_effective_at | TIMESTAMP | NULLABLE | Effective time of that provider status change |
| prior_stage | VARCHAR(255) | NULLABLE | Inquiry stage when the participation was cancelled |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- UNIQUE: `(inquiry_id, provider_id)`
- INDEX: `provider_id`, `distributed_at`, `status`, `cancellation_cause`

**Relationships**:

- `belongsTo` → `Inquiry`
- `belongsTo` → `Provider`

---

### 5B. Inquiry Date Ranges

**Table**: `inquiry_date_ranges`
**Description**: One row per treatment date range requested by the patient on an inquiry (FR-003 `dateRanges[]`). The stable ID is what `quote_option_date_prices.source_inquiry_date_range_id` (§7C) references.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique date range identifier |
| inquiry_id | UUID | FOREIGN KEY, NOT NULL | References inquiries.id |
| start_date | DATE | NOT NULL | Range start |
| end_date | DATE | NOT NULL | Range end; not before `start_date` |
| sort_order | INTEGER | NOT NULL | Order in which the patient entered the range |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `inquiry_id`

**Business Rules**:

- Ranges are written when the inquiry is submitted and are not edited once a quote references them.

**Relationships**:

- `belongsTo` → `Inquiry`
- `hasMany` → `QuoteOptionDatePrice` (§7C)

---

### 6. Medical History

**Table**: `medical_histories`  
**Description**: Patient's medical information attached to inquiry

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique medical history identifier |
| inquiry_id | UUID | FOREIGN KEY, NOT NULL | References inquiries.id |
| age | INTEGER | NULLABLE | Patient's age |
| medical_conditions | TEXT | NULLABLE | Existing medical conditions |
| medications | TEXT | NULLABLE | Current medications |
| allergies | TEXT | NULLABLE | Known allergies |
| previous_surgeries | TEXT | NULLABLE | Past surgical procedures |
| smoking_status | VARCHAR(255) | NULLABLE | Smoking habits |
| alcohol_consumption | VARCHAR(255) | NULLABLE | Alcohol consumption |
| family_history | TEXT | NULLABLE | Family medical history |
| critical_conditions | JSON | NULLABLE | Critical conditions flagged (HIV, blood disorders, heart conditions, etc.) |
| alert_level | VARCHAR(255) | DEFAULT 'none' | Alert level: critical (red), standard (yellow), none (green) |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `inquiry_id`

**Relationships**:

- `belongsTo` → `Inquiry`

---

### 7. Quotes

**Table**: `quotes`  
**Description**: Provider's offer with pricing and treatment details

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique quote identifier |
| inquiry_id | UUID | FOREIGN KEY, NOT NULL | References inquiries.id |
| provider_id | UUID | FOREIGN KEY, NOT NULL | References providers.id |
| authored_by_type | VARCHAR(255) | NOT NULL, DEFAULT 'provider' | `provider` for a normal quote; `admin` for a replacement quote that an admin authors for the replacement provider during an FR-006 provider-fault transfer |
| authored_by_admin_id | UUID | FOREIGN KEY, NULLABLE | References users.id; the admin who authored a replacement quote; set only when `authored_by_type` is `admin` |
| replacement_for_acceptance_event_id | UUID | FOREIGN KEY, NULLABLE | References acceptance_events.id: the closed acceptance this replacement quote replaces; set only when `authored_by_type` is `admin` |
| treatment_id | UUID | FOREIGN KEY, NOT NULL | References `treatments.id` for the exact immutable Treatment selected under FR-024 |
| treatment_version | INTEGER | NOT NULL | Version metadata for the immutable record referenced by `treatment_id`; technique and other Treatment-owned data are loaded through this relationship rather than copied onto `quotes` |
| package_id | UUID | FOREIGN KEY, NULLABLE | References packages.id. **DEPRECATED (FR-004 v2.2)** — superseded by `quote_options.source_package_id`; retained until every consumer migrates |
| treatment_date | JSON | NOT NULL | Proposed treatment dates. **DEPRECATED (FR-004 v2.2)** — superseded by `quote_option_date_prices`; retained until every consumer migrates |
| discount_id | UUID | FOREIGN KEY, NULLABLE | References the legacy `discounts.id` (§25). **DEPRECATED (FR-004 v2.6)** — structured promotions are now attached through `quote_option_date_prices.promotion_id`; retained until every consumer migrates |
| commission | INTEGER | NULLABLE | **Legacy, deprecated** percentage-only commission value; new quotes leave it NULL, and it MUST NOT be read as the commission rule. The binding commission snapshot is stored on `bookings` (§11A) |
| commission_model | VARCHAR(255) | NULLABLE | Indicative commission model shown on the quote: `percentage` or `flat_rate` (FR-004, FR-029). Never binding; the binding snapshot is captured at booking confirmation on `bookings` (§11A) |
| commission_value | DECIMAL(10,2) | NULLABLE | Indicative value: percentage (0-100) for `percentage`, fixed amount (> 0) for `flat_rate`; never binding |
| commission_currency | VARCHAR(3) | NULLABLE | Indicative Flat Rate currency; NULL for `percentage` |
| quote_amount | DECIMAL(10,2) | NOT NULL | Total quote amount. **DEPRECATED (FR-004 v2.2)** — a quote has a price range derived from `quote_option_date_prices` until acceptance, then the accepted option/date price; retained until every consumer migrates |
| currency | VARCHAR(255) | NULLABLE | Quote currency code (USD, EUR, GBP, TRY, etc.). NULL on drafts; copied read-only at first send from the FR-026 Quote Configuration (the FR-029 Default Currency); never provider input (FR-004 REQ-004-025) |
| note | TEXT | NULLABLE | Additional notes from provider, shared by every quote option |
| estimated_grafts | INTEGER | NOT NULL | Graft estimate shared by every quote option (FR-004 REQ-004-020) |
| graft_description | TEXT | NULLABLE | System-generated from the approved template and `estimated_grafts`; read-only to providers (FR-004 REQ-004-028) |
| graft_visual_plan_url | VARCHAR(500) | NULLABLE | Uploaded graft visual plan image shared by every quote option (FR-004 Screen 1 Tab 3) |
| treatment_plan_validated | BOOLEAN | DEFAULT false | Set once every option's treatment plan passes validation at submit (FR-004 Screen 7) |
| expiry_calculated_at | TIMESTAMP | NULLABLE | When `expires_at` was last derived from `expiration_hours` |
| status | VARCHAR(255) | NOT NULL | Quote lifecycle status — see Status Values below. Stored as `sent` in the database but exposed as `quote` through the API (see API Divergence note). Distinct from the treatment case lifecycle, which lives on `inquiries.status` |
| expires_at | TIMESTAMP | NULLABLE | Quote expiration time; NULL on drafts; computed at first send from the send time and `expiration_hours` |
| expiration_hours | INTEGER | NULLABLE | Quote expiry window in hours, copied read-only from the FR-026 Quote Configuration at first send (default 48); NULL on drafts; never changed per quote and never extended |
| auto_accepted | BOOLEAN | DEFAULT false | Whether quote was auto-accepted with pre-scheduled appointment |
| appointment_pre_scheduled | BOOLEAN | DEFAULT false | Whether provider pre-scheduled appointment in quote |
| sent_at | TIMESTAMP | NULLABLE | Time of the latest send: set at first send and updated each time a new version is sent. MUST NOT feed TTFQ analytics; TTFQ (FR-014) ends at `first_sent_at` |
| accepted_at | TIMESTAMP | NULLABLE | Set when status transitions to `accepted`; feeds Quote→Payment aging analytics (FR-014) |
| cancellation_provenance | JSON | NULLABLE | Set with `cancelled_provider_status`: cause (`ProviderSuspended` or `ProviderDeactivated`), provider status event reference, effective time, prior status |
| version | INTEGER | NOT NULL, DEFAULT 1 | Aggregate quote version; one `quote_versions` row per sent version. Every FR-005 subquote of this quote uses this value as its version (`subquoteVersion = QuoteVersion.version`) |
| first_sent_at | TIMESTAMP | NULLABLE | NULL on drafts; set once at first send and never overwritten by later versions. The end point of TTFQ analytics (FR-014) |
| quote_config_version | VARCHAR(64) | NULLABLE | FR-026 Quote Configuration version used at first send (source of `currency` and `expiration_hours`); NULL on drafts. A Default Currency change creates a new Quote Configuration version, as does an expiry-hours change, so this version identifies both the hours and the currency used |
| accepted_total | DECIMAL(10,2) | NULLABLE | Read-only copy written at FR-005 acceptance: accepted subquote price after promotion, in the quote currency, from the acceptance snapshot. The snapshot (`acceptance_events`, §7G) is authoritative |
| terms_acknowledged_at | TIMESTAMP | NULLABLE | Read-only copy written at FR-005 acceptance from the acceptance snapshot |
| locked_exchange_rate_snapshot | JSON | NULLABLE | Read-only copy written at FR-005 acceptance: exchange rate and its timestamp from the acceptance snapshot |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `inquiry_id`, `provider_id`, `status`, `created_at`
- COMPOSITE: `(provider_id, status)`, `(inquiry_id, provider_id)`

**Note (FR-004 v2.2)**: `(inquiry_id, provider_id)` MUST NOT be unique — the same provider may submit multiple parent quotes for one inquiry, each with an independent lifecycle, expiry, version, and audit history.

**Replacement quote (FR-006 provider-fault transfer)**: once an inquiry has an acceptance, no new quote can be created or sent, with one exception. During an FR-006 provider-fault transfer an admin authors a quote for the replacement provider inside the same inquiry (`authored_by_type = admin`, `authored_by_admin_id`, `replacement_for_acceptance_event_id`). It has the normal options and option/date-price rows, so the replacement acceptance (§7G) references its quote, option, and date-price row like any other acceptance, and `acceptance_events` and `bookings` keep their NOT NULL quote links. Every admin action on the replacement quote is written to `quote_audits` (§7I). No automatic promotion attaches to a replacement quote and no promotion use is reserved at its send (§7M); the admin sets the replacement price directly, and the original acceptance's promotion use is returned or kept under the normal rules (§7L). A replacement quote that is not accepted expires like any other quote; the inquiry keeps `support_required = true`, and the admin may author another replacement quote or cancel the inquiry and booking. The inquiry is never cancelled automatically by that expiry.

**Spec Gap (FR-004 v2.3)**: REQ-004-020 requires a quote-level **common requirements** field shared by every option. No `common_requirements` column exists on `quotes` today and none is present in the implementation, so this is an open schema item, not a documented-but-missing column. It MUST be added as `common_requirements TEXT NULLABLE` before REQ-004-020 can be marked implemented.

**Relationships**:

- `belongsTo` → `Inquiry`
- `belongsTo` → `Provider`
- `belongsTo` → exact immutable `Treatment` version; `treatment_id` is the record reference and `treatment_version` retains its version metadata
- `belongsTo` → `Package` *(deprecated; package provenance now held per option)*
- `hasMany` → `QuoteOption` (one to five, ordered)
- `hasMany` → `QuoteVersion` (§7H) and `QuoteAudit` (§7I)
- `hasMany` → `AcceptanceEvent` as the accepted parent quote (§7G)
- `belongsTo` → `AcceptanceEvent` through `replacement_for_acceptance_event_id` (admin-authored replacement quote only)
- `belongsToMany` → `Clinician` (one or more shared clinicians, FR-004 REQ-004-027)
- Promotion relationships are owned by `QuoteOptionDatePrice.promotion_id`; the parent Quote has no new direct Promotion relationship
- `hasOne` → `Schedule`
- `hasOne` → `Treatment` (actual treatment execution record)
- `hasMany` → `Payment`
- `hasMany` → `Review`

**Status Values** (FR-004 v2.5 quote lifecycle):

- `draft`: Provider is still composing the quote; not visible to the patient
- `sent`: Quote submitted to the patient and awaiting a response (exposed to clients as `quote`)
- `expired`: Expiry window elapsed with no patient response
- `withdrawn`: Provider retracted the quote before the patient responded, or withdrew after acceptance (the case then passes to the FR-006 provider-fault transfer)
- `archived`: Retained for audit only; excluded from active provider and patient lists
- `accepted`: Patient accepted one subquote (one option and one date range) of this quote. The quote stays `accepted` after the booking reaches `Payment Window Expired`, after an admin cancels the booking, and after a provider suspension or deactivation that follows acceptance; it is never reopened or expired
- `cancelled_other_accepted`: Auto-cancelled because the patient accepted a subquote of a different quote for the same inquiry; also applied silently (no notice) to drafts
- `cancelled_inquiry_cancelled`: Auto-cancelled because the underlying inquiry was cancelled. Applies only to quotes that were not accepted
- `cancelled_provider_status`: Auto-cancelled because the provider was suspended or deactivated (labelled "Cancelled (Provider Status)" and shown to the patient as "Offer Unavailable", per FR-004); the cause is held in `cancellation_provenance`. Applies only to quotes that were not accepted

`confirmed` is not a quote status. Booking confirmation is an FR-006 booking status held on `bookings.status` (§11A).

**Status Triggers**:

- `draft` → `sent`: Provider first sends the quote (sets `sent_at` and `first_sent_at`, copies `currency` and `expiration_hours` and records `quote_config_version` from one FR-026 configuration response, computes `expires_at`, writes `quote_versions` version 1). First send is blocked when the configuration cannot be read
- `sent` → `sent` (new version): Any edit of a sent quote increments `version`, writes a new `quote_versions` row, and updates `sent_at` (never `first_sent_at`); edits are blocked once a subquote is accepted
- `sent` → `expired`: Expiry job runs after `expires_at`
- `sent` → `withdrawn`: Provider retracts before a patient response
- `sent` → `accepted`: Patient accepts one subquote (sets `accepted_at`, `accepted_total`, `terms_acknowledged_at`, `locked_exchange_rate_snapshot`; creates the `acceptance_events` row)
- `draft` or `sent` → `cancelled_other_accepted`: Patient accepts a subquote of another quote on the same inquiry (no notice for drafts)
- `draft`, `sent`, or `expired` → `cancelled_inquiry_cancelled`: The inquiry is cancelled (patient cancellation in Inquiry or Quoted)
- An accepted quote stays `accepted` when an admin cancels the booking and the inquiry moves to `cancelled`; the AcceptanceEvent and its snapshot are retained unchanged
- `accepted` → `withdrawn`: Provider withdraws after acceptance (FR-004 Workflow 6); the AcceptanceEvent is unchanged and the case passes to the FR-006 provider-fault transfer
- `draft` or `sent` → `cancelled_provider_status`: Provider suspension or deactivation becomes effective before acceptance (FR-015). After acceptance the quote stays `accepted`: an Accepted or Confirmed booking is cancelled with cause `ProviderSuspended` or `ProviderDeactivated`, and an admin rehomes the patient through the FR-006 provider-fault transfer (an In Progress booking is not cancelled automatically, see §11A); the AcceptanceEvent is superseded when the replacement acceptance is recorded
- any terminal state → `archived`: Retention job or provider archive action

**API Divergence (verified in source)**: the database column stores `sent`, while `Quote::getStatusAttribute()` maps it to `quote` on read and the matching mutator maps `quote` back to `sent` on write. Clients therefore see `quote` where the schema stores `sent`. Historical rows were converted by the `align_quote_statuses_with_prd` migration, which also split the legacy single `cancelled` value into `cancelled_other_accepted` and `cancelled_inquiry_cancelled`.

**Case lifecycle is separate**: `inquiry`, `quoted`, `accepted`, `confirmed`, `in_progress`, `aftercare`, `completed`, and `cancelled` are **inquiry stages** (FR-003) stored on `inquiries.status`, not quote statuses. A quote status change drives a case status change through the inquiry status map; the two enums MUST NOT be merged.

---

### 7A. Quote Options

**Table**: `quote_options`
**Description**: One to five ordered package-based options within a parent quote (FR-004 v2.2). Each option is a quote-local snapshot; inline customization never writes back to the FR-024 package library.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique quote option identifier; recorded by FR-005 acceptance |
| quote_id | UUID | FOREIGN KEY, NOT NULL | References quotes.id |
| source_package_id | UUID | FOREIGN KEY, NOT NULL | Stable package ID; with `source_package_version` references the exact `packages` (`id`, `version`) row that seeded the option, for provenance only |
| source_package_version | INTEGER | NOT NULL | Package library version captured at selection |
| display_order | SMALLINT | NOT NULL | Patient-facing comparison order; consecutive within the quote |
| package_name_snapshot | VARCHAR(255) | NOT NULL | Package name copied at selection |
| package_description_snapshot | TEXT | NULLABLE | Package description copied at selection |
| standard_price_snapshot | DECIMAL(10,2) | NOT NULL | Library price copied at selection; prefills offered prices |
| included_services | JSON | NULLABLE | Travel services included in this option (flight, hotel, transport, other); consumed by FR-008 |
| is_customized | BOOLEAN | DEFAULT false | Inline-customised flag: whether the quote-local copy was edited inline and differs from its source package version |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `quote_id`, `source_package_id`
- UNIQUE: `(quote_id, display_order)`

**Constraints**:

- A quote MUST have between one and five options; enforced in request validation and the quote domain service.
- Inline edits change only this quote-local copy (and its items and plan days). They never write back to the package library and never create a package version; library edits create a new package version (§9) and never change an existing option.

**Relationships**:

- `belongsTo` → `Quote`
- `belongsTo` → exact `Package` version (`source_package_id`, `source_package_version`; provenance only)
- `hasMany` → `QuoteOptionItem`
- `hasMany` → `QuoteOptionDatePrice`
- `hasMany` → `QuoteOptionPlanDay`

---

### 7B. Quote Option Items

**Table**: `quote_option_items`
**Description**: Quote-local inclusion snapshot for one option, including services created inline for this patient.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique item identifier |
| quote_option_id | UUID | FOREIGN KEY, NOT NULL | References quote_options.id |
| source_package_item_id | UUID | FOREIGN KEY, NULLABLE | References the library item copied; NULL when created inside the quote |
| item_type | VARCHAR(255) | NOT NULL | Controlled service type (medical, travel, accommodation, transport, flight, other) |
| name | VARCHAR(255) | NOT NULL | Patient-facing service name |
| description | TEXT | NULLABLE | Patient-facing service details |
| price | DECIMAL(10,2) | NULLABLE | Optional component price; does not replace the offered option/date price |
| is_included | BOOLEAN | NOT NULL | Explicit included or excluded state |
| display_order | SMALLINT | NOT NULL | Patient-facing order within the option |

**Indexes**:

- PRIMARY: `id`
- INDEX: `quote_option_id`
- UNIQUE: `(quote_option_id, display_order)`

**Relationships**:

- `belongsTo` → `QuoteOption`

---

### 7C. Quote Option Date Prices

**Table**: `quote_option_date_prices`
**Description**: One row per applicable option/date combination. This is the acceptance unit FR-005 selects and the only source of an accepted quote amount.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Stable identifier recorded by FR-005 acceptance |
| quote_option_id | UUID | FOREIGN KEY, NOT NULL | References quote_options.id |
| source_inquiry_date_range_id | UUID | FOREIGN KEY, NOT NULL | References `inquiry_date_ranges.id` (§5B), a patient-requested FR-003 date range of the quote's inquiry |
| start_date | DATE | NOT NULL | Copied from the selected inquiry range |
| end_date | DATE | NOT NULL | Copied from the selected inquiry range |
| appointment_at | TIMESTAMP | NOT NULL | Pre-scheduled appointment start; must fall inside the range |
| appointment_timezone | VARCHAR(64) | NOT NULL | IANA timezone for the appointment |
| price | DECIMAL(10,2) | NOT NULL, CHECK (price > 0) | Provider price as entered, before any promotion, in the quote currency; must be greater than 0 before send (a date range the clinic cannot do is left out of the option rather than priced at 0) |
| promotion_id | UUID | FOREIGN KEY, NULLABLE | References `promotion_programs.id` (§25A), the FR-019 promotion program, `REUSABLE` or `AD_HOC_QUOTE_BOUND`, selected by the provider or attached automatically at send |
| promotion_terms_snapshot | JSON | NULLABLE | Promotion terms copied at send into the sent quote version; consumers read these copied terms and never resolve live FR-019 terms for a sent quote |
| discount_amount | DECIMAL(10,2) | NULLABLE | Discount in the quote currency, copied at send with the terms |
| is_auto_attached_promotion | BOOLEAN | DEFAULT false | Whether the promotion was attached automatically at send |

**Indexes**:

- PRIMARY: `id`
- INDEX: `quote_option_id`, `promotion_id`
- UNIQUE: `(quote_option_id, source_inquiry_date_range_id)`
- CHECK: `price > 0`

**Acceptance state**: not stored on this table. FR-005 owns subquote identity and acceptance state (accepted, not selected, superseded); a subquote is one option/date-price row combined with its option, and any acceptance flag shown for a row is derived from `acceptance_events` (§7G). The former `is_accepted` column is removed. The unique `(quote_option_id, source_inquiry_date_range_id)` index keeps one row per option and date range; at most one non-superseded acceptance per inquiry is enforced by `acceptance_events`.

**Relationships**:

- `belongsTo` → `QuoteOption`
- `belongsTo` → `InquiryDateRange` (§5B) through `source_inquiry_date_range_id`
- `belongsTo` → `PromotionProgram` (§25A) through `promotion_id`

---

### 7D. Quote Option Plan Days

**Table**: `quote_option_plan_days`
**Description**: Per-option day-to-day treatment plan. Day numbers stay relative for the life of the record and are never persisted as calendar dates.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique plan day identifier |
| quote_option_id | UUID | FOREIGN KEY, NOT NULL | References quote_options.id |
| day_number | SMALLINT | NOT NULL | Relative day index; starts at 1, consecutive with no gaps |
| description | TEXT | NOT NULL | What happens on that relative treatment day |

**Indexes**:

- PRIMARY: `id`
- INDEX: `quote_option_id`
- UNIQUE: `(quote_option_id, day_number)`

**Relationships**:

- `belongsTo` → `QuoteOption`

**Migration Note (FR-004 v2.2)**: The option tables are additive. Existing single-package quotes migrate to a one-option quote whose snapshot is taken from `quotes.package_id`, whose single date-price row is taken from `quotes.treatment_date` and `quotes.quote_amount`, and the deprecated `quotes` columns stay readable through a compatibility adapter until every consumer moves to the option contract (CR-FR004-20260909-01).

---

### 7E. Quote Clinicians

**Table**: `quote_clinicians`
**Description**: Junction table assigning one or more clinicians to a parent quote. Clinicians are shared by every option of that quote (FR-004 REQ-004-027).

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique assignment identifier |
| quote_id | UUID | FOREIGN KEY, NOT NULL | References quotes.id |
| provider_user_id | UUID | FOREIGN KEY, NOT NULL | References provider_users.id (the clinician) |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `quote_id`, `provider_user_id`

**Relationships**:

- `belongsTo` → `Quote`
- `belongsTo` → `ProviderUser`

---

### 7F. Quote Documents

**Table**: `quote_documents`
**Description**: Attachments uploaded against a parent quote (treatment plans, consent forms, supporting images). Shared by every option of that quote.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique document identifier |
| quote_id | UUID | FOREIGN KEY, NOT NULL | References quotes.id (RESTRICT; documents are retained with the quote) |
| document_type | VARCHAR(255) | NOT NULL | Attachment category |
| file_name | VARCHAR(255) | NOT NULL | Original file name |
| file_path | VARCHAR(500) | NOT NULL | Stored file path |
| file_type | VARCHAR(255) | NOT NULL | MIME type |
| file_size | INTEGER | NOT NULL | Size in bytes |
| uploaded_by | UUID | NOT NULL | Uploader identifier |
| uploaded_by_type | VARCHAR(255) | NOT NULL | Uploader actor type (provider, admin) |
| description | TEXT | NULLABLE | Optional description |
| deleted_at | TIMESTAMP | NULLABLE | Soft delete timestamp |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `quote_id`

**Relationships**:

- `belongsTo` → `Quote`

---

### 7G. Acceptance Events

**Table**: `acceptance_events`
**Description**: Append-only record of one subquote acceptance (FR-005 AcceptanceEvent). It carries the immutable acceptance snapshot that every downstream module reads for money fields. Created in the same transaction as the slot hold and the `bookings` row (§11A).

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique acceptance event identifier |
| inquiry_id | UUID | FOREIGN KEY, NOT NULL | References inquiries.id |
| accepted_parent_quote_id | UUID | FOREIGN KEY, NOT NULL | References quotes.id |
| accepted_parent_quote_version | INTEGER | NOT NULL | Aggregate quote version accepted (`quote_versions.version`) |
| accepted_subquote_id | UUID | NOT NULL | FR-005 subquote ID, derived deterministically from `quote_option_id` and `option_date_price_id` |
| accepted_subquote_version | INTEGER | NOT NULL | MUST equal `accepted_parent_quote_version` |
| quote_option_id | UUID | FOREIGN KEY, NOT NULL | References quote_options.id |
| option_date_price_id | UUID | FOREIGN KEY, NOT NULL | References quote_option_date_prices.id |
| reserved_slot_id | UUID | NOT NULL | Identifier of the fixed slot hold keyed by provider, appointment date/time, and time zone; the hold fields live on the booking (§11A). Not an appointment record |
| actor_id | UUID | NOT NULL | Patient, or admin for a provider-fault replacement acceptance |
| actor_type | VARCHAR(255) | NOT NULL | `patient` or `admin` (admin only for a provider-fault replacement acceptance, which references the admin-authored replacement quote) |
| accepted_at | TIMESTAMP | NOT NULL | Acceptance time |
| acceptance_snapshot | JSON | NOT NULL | Immutable snapshot of the complete subquote and inherited parent context (FR-005 REQ-005-006): IDs and versions, source package ID and version, parent expiry, treatment ID and version, package and service snapshot, date range, appointment date/time and time zone, offered price, promotion and any patient-applied promotion code with the resulting discounted price, currency, exchange rate and its timestamp, treatment plan, grafts, visual plan, clinician IDs, notes, requirements, attachment IDs with versions, actor, and timestamp |
| offered_price | DECIMAL(10,2) | NOT NULL | Projection of the snapshot: provider price before promotion |
| accepted_price | DECIMAL(10,2) | NOT NULL | Projection of the snapshot: accepted subquote price after promotion (the booking total) |
| currency | VARCHAR(3) | NOT NULL | Projection of the snapshot: quote currency |
| date_range_start | DATE | NOT NULL | Projection of the snapshot: accepted date range start |
| date_range_end | DATE | NOT NULL | Projection of the snapshot: accepted date range end |
| appointment_at | TIMESTAMP | NOT NULL | Projection of the snapshot: accepted appointment start |
| appointment_timezone | VARCHAR(64) | NOT NULL | Projection of the snapshot: IANA time zone |
| promotion_id | UUID | FOREIGN KEY, NULLABLE | Projection of the snapshot: promotion program applied, if any; references `promotion_programs.id` (§25A) |
| promotion_code_id | UUID | FOREIGN KEY, NULLABLE | Projection of the snapshot: patient-applied promotion code, if any; references `promotion_codes.id` (§25B) |
| exchange_rate | DECIMAL(18,8) | NULLABLE | Projection of the snapshot: exchange rate locked at acceptance (a stale cached rate is accepted and recorded) |
| exchange_rate_at | TIMESTAMP | NULLABLE | Projection of the snapshot: timestamp of that rate |
| handoff_metadata | JSON | NULLABLE | FR-006 booking handoff context |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `inquiry_id`, `accepted_parent_quote_id`, `option_date_price_id`, `accepted_at`

**Business Rules**:

- Append-only: rows are never updated, deleted, soft-deleted, or restored. Projection columns are written once from the snapshot, and the snapshot is authoritative.
- Price, currency, date range, appointment, and promotion are the binding money fields; downstream modules (FR-006, FR-007, FR-007b, FR-008, FR-010, FR-017, FR-019, FR-029) read them from this record, never from live quote rows. The appointment here is the accepted baseline: an admin appointment change moves the booking's current appointment (§11A) and never edits this record, and booking notices read the booking's current appointment.
- At most one acceptance event per inquiry has no `acceptance_supersessions` row. The acceptance transaction locks the inquiry and rejects a second acceptance before any event, hold, or booking is created.
- Supersession and admin notes are separate linked records (§7J, §7K). A provider-fault transfer creates a new admin-authored event that references the admin-authored replacement quote (§7), its option, and its date-price row; the same transaction inserts the single `acceptance_supersessions` row that links the closed event to the new one.

**Relationships**:

- `belongsTo` → `Inquiry`
- `belongsTo` → `Quote` (accepted parent quote)
- `belongsTo` → `QuoteOption`, `QuoteOptionDatePrice`
- `hasOne` → `Booking`
- `hasOne` → `AcceptanceSupersession` (as superseded event)
- `hasMany` → `AcceptanceAnnotation`
- `hasOne` → `PromotionApplication`

---

### 7H. Quote Versions

**Table**: `quote_versions`
**Description**: One row per sent version of a parent quote (FR-004 QuoteVersion). The version is the version source for every subquote derived from the quote.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique version row identifier |
| quote_id | UUID | FOREIGN KEY, NOT NULL | References quotes.id |
| version | INTEGER | NOT NULL | Aggregate version number |
| changeset | JSON | NOT NULL | Snapshot of the full quote aggregate and all option-owned children, including the promotion terms copied at send |
| created_by | UUID | NOT NULL | Actor who sent the version |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |

**Indexes**:

- PRIMARY: `id`
- UNIQUE: `(quote_id, version)`

**Relationships**:

- `belongsTo` → `Quote`

---

### 7I. Quote Audits

**Table**: `quote_audits`
**Description**: Audit trail of quote actions (FR-004 QuoteAudit).

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique audit row identifier |
| quote_id | UUID | FOREIGN KEY, NOT NULL | References quotes.id |
| action | VARCHAR(255) | NOT NULL | Action performed |
| actor_id | UUID | NOT NULL | Actor |
| reason | TEXT | NULLABLE | Reason, where the action requires one |
| before | JSON | NULLABLE | Values before the action |
| after | JSON | NULLABLE | Values after the action |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `quote_id`, `created_at`

**Relationships**:

- `belongsTo` → `Quote`

---

### 7J. Acceptance Supersessions

**Table**: `acceptance_supersessions`
**Description**: Linked, append-only record that marks an AcceptanceEvent superseded by a replacement acceptance without editing it (FR-005 AcceptanceSupersession).

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique supersession identifier |
| superseded_acceptance_event_id | UUID | FOREIGN KEY, NOT NULL, UNIQUE | References acceptance_events.id |
| cause | VARCHAR(255) | NOT NULL | `ProviderFault`, `ProviderSuspended`, or `ProviderDeactivated`, copied from the closed booking's cancellation cause |
| replacement_acceptance_event_id | UUID | FOREIGN KEY, NOT NULL, UNIQUE | References the new admin-authored acceptance_events.id |
| actor_id | UUID | NOT NULL | Actor recording the supersession |
| reason | TEXT | NULLABLE | Reason |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |

**Indexes**:

- PRIMARY: `id`
- UNIQUE: `superseded_acceptance_event_id`
- UNIQUE: `replacement_acceptance_event_id`
- INDEX: `cause`

**Business Rules**:

- Append-only, single insert. The row is created once, at the replacement acceptance, in the same transaction as the new admin-authored AcceptanceEvent, and is never updated.
- Closing the original booking (FR-006 Alternative Flow B4) records the closure on the booking (`bookings.cancellation_reason`, `support_required`), not here. A booking cancelled without a replacement (for example an admin cancellation) has no supersession row.
- Handling of money already paid is out of scope here and follows the later payment documentation.

**Relationships**:

- `belongsTo` → `AcceptanceEvent` (superseded)
- `belongsTo` → `AcceptanceEvent` (replacement)

---

### 7K. Acceptance Annotations

**Table**: `acceptance_annotations`
**Description**: Audited, append-only admin note on an AcceptanceEvent (FR-005 AcceptanceAnnotation). It never alters the event, its snapshot, or any state.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique annotation identifier |
| acceptance_event_id | UUID | FOREIGN KEY, NOT NULL | References acceptance_events.id |
| author_id | UUID | FOREIGN KEY, NOT NULL | References users.id (admin) |
| type | VARCHAR(255) | NOT NULL | `note` or `correction` |
| text | TEXT | NOT NULL | Annotation text |
| reason | TEXT | NOT NULL | Reason |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `acceptance_event_id`

**Relationships**:

- `belongsTo` → `AcceptanceEvent`
- `belongsTo` → `User` (admin author)

---

### 7L. Promotion Applications

**Table**: `promotion_applications`
**Description**: Promotion redemption record (FR-019 Application), created only at subquote acceptance and linked to the AcceptanceEvent.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique application identifier |
| program_id | UUID | FOREIGN KEY, NOT NULL | References `promotion_programs.id` (§25A), the FR-019 promotion program |
| code_id | UUID | FOREIGN KEY, NULLABLE | References `promotion_codes.id` (§25B), when a code was used |
| source | VARCHAR(255) | NOT NULL | `provider_selected`, `auto_attached`, or `patient_code` |
| acceptance_event_id | UUID | FOREIGN KEY, NOT NULL | References acceptance_events.id |
| quote_id | UUID | FOREIGN KEY, NOT NULL | References quotes.id |
| quote_version | INTEGER | NOT NULL | Accepted aggregate quote version |
| quote_option_date_price_id | UUID | FOREIGN KEY, NOT NULL | References quote_option_date_prices.id (the accepted subquote) |
| booking_id | UUID | FOREIGN KEY, NULLABLE | References bookings.id |
| patient_id | UUID | FOREIGN KEY, NOT NULL | References patients.id |
| provider_id | UUID | FOREIGN KEY, NULLABLE | References providers.id; NULL for Hairline-Funded programs |
| state | VARCHAR(255) | NOT NULL | Lifecycle depends on `source` (see Business Rules). `APPLIED` at acceptance; `COMPLETED` at the first successful payment. For `auto_attached` the use was already reserved at send and is consumed at acceptance; for `provider_selected` and `patient_code` one use is reserved at acceptance and consumed at the first successful payment |
| status | VARCHAR(255) | NOT NULL, DEFAULT 'active' | `active`, `voided`, `superseded`, `reversed`, or `refunded` |
| supersedes_application_id | UUID | FOREIGN KEY, NULLABLE | References promotion_applications.id; set on a replacement created by a provider-fault transfer |
| terms_snapshot | JSON | NOT NULL | Type, value, applies-to, and funding model as fixed at send |
| currency | VARCHAR(3) | NOT NULL | Quote currency from the acceptance snapshot |
| discount_value | DECIMAL(10,2) | NOT NULL | Discount applied, in `currency` |
| funding_split | JSON | NULLABLE | `hairline_portion` and `provider_portion` |
| applied_at | TIMESTAMP | NOT NULL | Acceptance time |
| completed_at | TIMESTAMP | NULLABLE | First successful payment time |
| use_reservation_id | UUID | FOREIGN KEY, NULLABLE | References promotion_use_reservations.id; set for `auto_attached` applications (the send-time reservation consumed at acceptance) |
| use_returned_at | TIMESTAMP | NULLABLE | When the counted use was returned to the program limit (booking `Payment Window Expired` or cancelled before first payment); cleared if an admin revive takes it again |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `acceptance_event_id`, `program_id`, `code_id`, `booking_id`, `state`, `status`

**Business Rules**:

- Usage-limit lifecycle by `source`:
  - `auto_attached`: one use is reserved at send in `promotion_use_reservations` (at most one per parent quote) and consumed at acceptance, when this row is created with `use_reservation_id`. If the booking ends `Payment Window Expired` or is cancelled before the first successful payment, the use is returned to the limit (`use_returned_at` set). An admin revive takes the use again only if the limit has room (`use_returned_at` cleared); otherwise the revive is rejected (FR-006, FR-019).
  - `provider_selected` and `patient_code`: one use is reserved at acceptance and consumed at the first successful payment; the reservation is released on `Payment Window Expired` or cancellation before that payment, and reserved again on admin revive only if the limit has room (FR-019).
- The limit is checked against active reservations in `promotion_use_reservations` plus uses held by applications here that have not been returned, so it can never be exceeded.
- Promotions are frozen after acceptance: no provider remove or replace and no checkout or booking code entry. The only exception is the replacement application linked through `supersedes_application_id` in a provider-fault transfer.
- No automatic promotion attaches to an admin-authored replacement quote (`quotes.authored_by_type = admin`) and no new reservation is taken for it; the admin sets the replacement price directly.

**Relationships**:

- `belongsTo` → `PromotionProgram` (§25A, through `program_id`), `PromotionCode` (§25B, through `code_id`), `AcceptanceEvent`, `Quote`, `QuoteOptionDatePrice`, `Booking`, `Patient`, `Provider`

---

### 7M. Promotion Use Reservations

**Table**: `promotion_use_reservations`
**Description**: Send-time reservation of one use of an auto-attached promotion (FR-019), so the program's usage limit can never be exceeded between quote send and acceptance. `promotion_applications` is created only at acceptance and cannot hold this pre-acceptance state.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique reservation identifier |
| program_id | UUID | FOREIGN KEY, NOT NULL | References `promotion_programs.id` (§25A), the FR-019 promotion program whose usage limit is reserved against |
| quote_id | UUID | FOREIGN KEY, NOT NULL | References quotes.id (the sent parent quote carrying the auto-attached promotion) |
| quote_version | INTEGER | NOT NULL | Quote version whose send created the reservation (unchanged when later versions keep it) |
| state | VARCHAR(255) | NOT NULL, DEFAULT 'reserved' | `reserved` at send; `released` when the quote expires, is withdrawn, is not selected, is cancelled before acceptance, a resent version drops the promotion, or the accepted row does not carry the promotion; `consumed` when the accepted row carries the promotion |
| reserved_at | TIMESTAMP | NOT NULL | Send time |
| released_at | TIMESTAMP | NULLABLE | Release time |
| release_reason | VARCHAR(255) | NULLABLE | `expired`, `withdrawn`, `not_selected`, `dropped_on_resend`, `cancelled` (the quote was cancelled before acceptance because the inquiry was cancelled or the provider's status changed), or `not_applied` (a subquote of the quote was accepted but the accepted row does not carry the promotion) |
| consumed_at | TIMESTAMP | NULLABLE | Acceptance time |
| acceptance_event_id | UUID | FOREIGN KEY, NULLABLE | References acceptance_events.id; set when consumed |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `program_id`, `state`
- UNIQUE: `quote_id` for rows in state `reserved` (at most one active reservation per parent quote, whatever the promotion); MySQL has no partial unique index, so this is enforced through a unique index on a generated column that holds `quote_id` only while `state = 'reserved'` and NULL otherwise

**Business Rules**:

- A parent quote carries at most one automatic promotion. If several automatic programmes qualify, the FR-019 priority order picks one.
- Sending a quote that carries an auto-attached promotion reserves one use. If reserved plus consumed uses would exceed the program's usage limit, the promotion does not attach and the send proceeds without it, so the limit can never be exceeded.
- A parent quote holds at most one active reservation. Resending a new version of the same quote keeps the active reservation and never reserves a second use; it creates a reservation only if the new version newly carries the auto-attached promotion, and releases the active reservation (reason `dropped_on_resend`) if the new version no longer carries it.
- The reservation is released when the quote expires, is withdrawn, is not selected, or is cancelled before acceptance (reason `cancelled`, when the inquiry is cancelled or the provider is suspended or deactivated). When a subquote of that quote is accepted, the reservation is consumed if the accepted row carries the promotion, and released with reason `not_applied` (the use returns to the limit) if it does not. Released and consumed rows are terminal; after consumption, any return of the use to the limit, or the use being taken again on admin revive, is recorded on the linked `promotion_applications` row.

**Relationships**:

- `belongsTo` → `PromotionProgram` (§25A, through `program_id`), `Quote`, `AcceptanceEvent`

---

### 8. Treatments (Admin-Created Foundation)

**Table**: `treatments`  
**Description**: Treatment types created by admin - foundation that all providers select from (FUE, FUT, DHI, etc.)

**Purpose**: Ensures consistency - all providers offer the same treatments with standardized information and videos

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique treatment identifier |
| user_id | UUID | FOREIGN KEY, NOT NULL | References users.id (admin who created) |
| treatment_name | VARCHAR(255) | NOT NULL | Treatment name (e.g., "FUE - Follicular Unit Extraction") |
| treatment_type | VARCHAR(255) | NOT NULL | Type code (FUE, FUT, DHI, SAPPHIRE_FUE, ROBOTIC) |
| treatment_description | TEXT | NOT NULL | Detailed treatment description |
| technique_specifications | TEXT | NULLABLE | Standardized technique details loaded read-only by related quotes when documented |
| version | INTEGER | NOT NULL, DEFAULT 1 | Immutable version number; FR-024 treatment edits create a new version instead of changing a version referenced by a quote |
| thumbnail | VARCHAR(255) | NOT NULL | S3 path to thumbnail image |
| video | VARCHAR(255) | NULLABLE | S3 path to educational video |
| status | VARCHAR(255) | DEFAULT 'active' | Treatment status (active, inactive) |
| ended_at | TIMESTAMP | NULLABLE | When treatment was deactivated |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `user_id`, `status`, `treatment_type`

**Relationships**:

- `belongsTo` → `User` (admin creator)
- `hasMany` → `ProviderTreatmentPricing` (each provider sets their own pricing)
- `hasMany` → `TreatmentInclude` (what's included in treatment)
- `hasMany` → `Quote`

**Business Rules**:

- ONLY admins can create treatments
- Providers can ONLY select from this list (cannot create custom treatments)
- Providers set their own pricing for each treatment
- Once a Treatment version is referenced by a quote, edits create a new immutable Treatment record/version; the historical quote continues resolving Treatment-owned data through its original relationship

---

### 9. Packages (Versioned Provider Templates)

**Table**: `packages`  
**Description**: Versioned package templates in each provider's library (FR-024 Package). A package is a full template that seeds one Quote Option: included items, travel services, a relative-day plan, and a standard price. Date ranges, notes, and documents are never packaged. Each selected package becomes one alternative option on a quote (up to five); packages are never summed.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | NOT NULL | Stable package identifier, shared by all versions |
| version | INTEGER | NOT NULL, DEFAULT 1 | Version number; each library edit creates a new version row |
| provider_id | UUID | FOREIGN KEY, NOT NULL | References providers.id (owner of package) |
| name | VARCHAR(255) | NOT NULL | Package name |
| description | TEXT | NULLABLE | Package description |
| duration | VARCHAR(255) | NULLABLE | Package duration |
| standard_price | DECIMAL(10,2) | NOT NULL | Standard price in the system quote currency; prefills option prices. No package currency is stored |
| included_travel_services | JSON | NULLABLE | Included travel services (flight, hotel, transport, other) |
| image_urls | JSON | NULLABLE | Package images |
| terms_conditions | TEXT | NULLABLE | Package terms |
| status | VARCHAR(255) | DEFAULT 'active' | Package status (active, inactive) |
| created_by | UUID | NOT NULL | Provider user who created this version |
| created_at | TIMESTAMP | AUTO | Version creation timestamp |

**Indexes**:

- PRIMARY: `(id, version)`
- INDEX: `provider_id`, `status`

**Relationships**:

- `belongsTo` → `Provider` (package owner)
- `hasMany` → `PackageItem` and `PackagePlanDay` (per version)
- `hasMany` → `QuoteOption` (as provenance source via `source_package_id` and `source_package_version`)

**Business Rules**:

- Each provider creates their own packages. Earlier versions are read-only, and packages are never hard-deleted.
- A library edit creates a new version and never changes an existing Quote Option. Inline edits on a quote change only that quote-local option copy (§7A) and never write back to the library.
- Patient-facing package data on a quote is read from the option copy and its recorded source version, never from the latest library version.
- Usage Count counts Quote Options on open (draft or sent) quotes that reference the package.
- The legacy add-on package categories and the `quote_packages` and `quote_treatments` junctions are removed; FR-004 Quote Options hold package provenance and the quote-local copy, and legacy rows are handled by the FR-004 migration.

---

### 10. Package Items

**Table**: `package_items`  
**Description**: Items included in one package version (FR-024 PackageItem). FR-004 copies them into `quote_option_items` and records the source item ID.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique item identifier |
| package_id | UUID | NOT NULL | Stable package ID |
| package_version | INTEGER | NOT NULL | With `package_id`, references the `packages` (`id`, `version`) row |
| item_type | VARCHAR(255) | NOT NULL | medical, travel, accommodation, transport, flight, or other |
| name | VARCHAR(255) | NOT NULL | Item name |
| description | TEXT | NULLABLE | Item details |
| price | DECIMAL(10,2) | NULLABLE | Optional component price in the system quote currency |
| is_included | BOOLEAN | NOT NULL | Explicit included or excluded state |
| display_order | SMALLINT | NOT NULL | Order within the package version |

**Indexes**:

- PRIMARY: `id`
- INDEX: `(package_id, package_version)`

**Relationships**:

- `belongsTo` → `Package` version

---

### 10A. Package Plan Days

**Table**: `package_plan_days`  
**Description**: Relative-day plan of one package version (FR-024 PackagePlanDay). FR-004 copies these rows into `quote_option_plan_days`; days are never converted to calendar dates.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique plan day identifier |
| package_id | UUID | NOT NULL | Stable package ID |
| package_version | INTEGER | NOT NULL | With `package_id`, references the `packages` (`id`, `version`) row |
| day_number | SMALLINT | NOT NULL | Relative day index, starting at 1 |
| description | TEXT | NOT NULL | What happens on that relative day |

**Indexes**:

- PRIMARY: `id`
- UNIQUE: `(package_id, package_version, day_number)`

**Relationships**:

- `belongsTo` → `Package` version

---

### 11. Schedules

**Table**: `schedules`  
**Description**: Appointment record. Created only when the first payment succeeds and the booking (§11A) moves to `confirmed`; acceptance creates no schedule row, and the payment-window hold lives on `bookings`

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique schedule identifier |
| quote_id | UUID | FOREIGN KEY, NOT NULL | References quotes.id |
| booking_id | UUID | FOREIGN KEY, NULLABLE | References bookings.id; set for every appointment created from a confirmed booking |
| schedule_date | DATE | NOT NULL | Appointment date |
| schedule_time | TIME | NULLABLE | Appointment time |
| location | VARCHAR(255) | NULLABLE | Clinic location details |
| notes | TEXT | NULLABLE | Special instructions |
| status | VARCHAR(255) | DEFAULT 'pending' | Schedule status (pending, confirmed, cancelled) |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `quote_id`, `schedule_date`

**Relationships**:

- `belongsTo` → `Quote`

---

### 11A. Bookings

**Table**: `bookings`
**Description**: Booking derived from one accepted subquote and its inherited parent context (FR-006 Booking). Created with status `accepted` in the same transaction as the AcceptanceEvent and the slot hold. Payment-window hold fields live here; the appointment (`schedules`) is created only on the first successful payment.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique booking identifier |
| booking_reference | VARCHAR(255) | UNIQUE, NOT NULL | Patient-facing booking reference |
| inquiry_id | UUID | FOREIGN KEY, NOT NULL | References inquiries.id |
| patient_id | UUID | FOREIGN KEY, NOT NULL | References patients.id |
| provider_id | UUID | FOREIGN KEY, NOT NULL | References providers.id |
| acceptance_event_id | UUID | FOREIGN KEY, NOT NULL, UNIQUE | References acceptance_events.id; one booking per acceptance event |
| accepted_parent_quote_id | UUID | FOREIGN KEY, NOT NULL | References quotes.id |
| accepted_parent_quote_version | INTEGER | NOT NULL | Accepted aggregate quote version |
| accepted_subquote_id | UUID | NOT NULL | FR-005 subquote ID |
| accepted_subquote_version | INTEGER | NOT NULL | MUST equal `accepted_parent_quote_version` |
| status | VARCHAR(255) | NOT NULL, DEFAULT 'accepted' | `accepted`, `payment_window_expired`, `confirmed`, `in_progress`, `aftercare`, `completed`, `cancelled` (displayed as Accepted, Payment Window Expired, Confirmed, In Progress, Aftercare, Completed, Cancelled) |
| hold_appointment_at | TIMESTAMP | NOT NULL | Hold key: the booking's current appointment date/time. Set from the acceptance snapshot at acceptance and moved with the booking's appointment when an admin changes it (FR-006, which sends `booking.rescheduled` to patient and provider); the snapshot itself never changes. Booking notices read this current appointment |
| hold_appointment_timezone | VARCHAR(64) | NOT NULL | Hold key: IANA time zone of the booking's current appointment; set and moved together with `hold_appointment_at` |
| hold_started_at | TIMESTAMP | NOT NULL | Start of the current fixed hold (acceptance, or admin revive) |
| hold_expires_at | TIMESTAMP | NOT NULL | `hold_started_at` plus the FR-026 Slot-Hold Duration in effect when the hold was placed (default 48 hours); never extended or restarted by payment failure |
| hold_released_at | TIMESTAMP | NULLABLE | When the hold was released (expiry, cancellation, provider status cascade, or provider fault) |
| confirmed_at | TIMESTAMP | NULLABLE | First successful payment (deposit or first instalment); the appointment is created and the slot blocked at this point |
| booking_total | DECIMAL(10,2) | NOT NULL | Booking total: accepted subquote price after promotion, in the quote currency, copied read-only from the acceptance snapshot |
| currency | VARCHAR(3) | NOT NULL | Quote currency copied from the acceptance snapshot |
| commission_model | VARCHAR(255) | NULLABLE | Binding commission snapshot captured at booking confirmation: `percentage` or `flat_rate` (FR-029) |
| commission_value | DECIMAL(10,2) | NULLABLE | Snapshot value: percentage (0-100) for `percentage`, fixed amount (> 0, deducted once per FR-010 completed procedure) for `flat_rate` |
| commission_currency | VARCHAR(3) | NULLABLE | Snapshot Flat Rate currency; NULL for `percentage` |
| commission_config_id | UUID | FOREIGN KEY, NULLABLE | Source configuration ID: references provider_commissions.id (§2B) resolved at booking confirmation |
| commission_scope_type | VARCHAR(255) | NULLABLE | `global` or `provider_specific` |
| deposit_rate | DECIMAL(5,2) | NULLABLE | Deposit rate snapshot (percentage of `booking_total`) locked at booking confirmation from the FR-029 configuration in effect |
| installment_settings_snapshot | JSON | NULLABLE | Split payment (instalment) settings locked at booking confirmation from the FR-029 configuration in effect (allowed instalment counts and cutoff rule) |
| payment_config_id | UUID | NULLABLE | Source FR-029 deposit and instalment configuration resolved at booking confirmation |
| cancellation_reason | VARCHAR(255) | NULLABLE | Set with `cancelled`: the mandatory admin reason for an admin cancellation, the inquiry cancellation reason when the patient cancelled before acceptance, or cause `ProviderFault`, `ProviderSuspended`, or `ProviderDeactivated` |
| cancelled_at | TIMESTAMP | NULLABLE | When the booking moved to `cancelled` |
| cancelled_by | UUID | FOREIGN KEY, NULLABLE | References users.id: the admin who cancelled the booking; NULL for a system cascade |
| support_required | BOOLEAN | DEFAULT false | Marker, not a status; set for provider status and provider-fault closures and cleared only by audited admin resolution |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- UNIQUE: `booking_reference`, `acceptance_event_id`
- INDEX: `inquiry_id`, `provider_id`, `patient_id`, `status`, `hold_expires_at`
- UNIQUE (active hold key): at most one booking in `accepted`, `confirmed`, `in_progress`, or `aftercare` per (`provider_id`, `hold_appointment_at`, `hold_appointment_timezone`); enforced through a unique index on a generated column that is NULL for other statuses

**Status Triggers (FR-006)**:

- `accepted` → `confirmed`: First successful payment before `hold_expires_at`; sets `confirmed_at`, creates the `schedules` appointment, blocks the slot, and captures the commission snapshot
- `accepted` → `payment_window_expired`: The hold lapses before the first successful payment; the hold is released and no appointment exists
- `payment_window_expired` → `accepted`: Audited admin revive only; places a new fixed hold (new `hold_started_at` and `hold_expires_at`)
- `confirmed` → `in_progress` (FR-010) → `aftercare` (FR-011) → `completed`
- `accepted`, `payment_window_expired`, `confirmed`, `in_progress`, or `aftercare` → `cancelled`: Admin cancellation only, with a mandatory reason and an audit entry (sets `cancellation_reason`, `cancelled_at`, `cancelled_by`). The patient cannot cancel a booking in the app and is routed to admin support. The inquiry moves to `cancelled`, the accepted quote stays `accepted`, and any hold or calendar block is released. Refunds and fees follow the payment documentation
- `accepted` or `confirmed` → `cancelled` with cause `ProviderFault`, `ProviderSuspended`, or `ProviderDeactivated` and `support_required = true` (FR-006 Alternative Flow B4). The inquiry stays open; an admin then completes the FR-006 provider-fault transfer (Alternative Flow B5), which creates a new booking from an admin-authored replacement acceptance
- Provider fault, suspension, or deactivation while the booking is `in_progress`: the booking is not cancelled automatically. It stays `in_progress` with `support_required = true`, and an admin decides the case on the FR-006 intervention screen: either moves the booking to `aftercare` and reassigns the aftercare provider (§13), or cancels the booking with a mandatory reason through the admin cancellation above. No replacement acceptance is created
- Provider fault while the booking is `aftercare`: the booking and treatment record stay unchanged; an admin reassigns the aftercare provider or team (§13). No new acceptance, booking, or payment is created

**Business Rules**:

- Money fields come from the acceptance snapshot only. The booking total is the base for commission (FR-029); the exchange rate is locked at acceptance (`acceptance_events`), and the commission, deposit rate, and instalment settings are locked at booking confirmation in the snapshot columns above.
- The Payment Window Expired boundary applies to the first payment only.
- `confirmed` is a booking status only, never a quote status.

**Relationships**:

- `belongsTo` → `AcceptanceEvent`, `Inquiry`, `Patient`, `Provider`
- `belongsTo` → `Quote` (accepted parent quote)
- `hasOne` → `Schedule` (created at first successful payment)
- `hasOne` → `TravelContext`, `TreatmentRecord`

---

### 12. Payments

**Table**: `payments`  
**Description**: Payment transactions (deposits and final payments)

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique payment identifier |
| quote_id | UUID | FOREIGN KEY, NOT NULL | References quotes.id |
| patient_id | UUID | FOREIGN KEY, NOT NULL | References patients.id |
| provider_id | UUID | FOREIGN KEY, NOT NULL | References providers.id |
| amount | DECIMAL(10,2) | NOT NULL | Payment amount |
| currency | VARCHAR(255) | NOT NULL | Currency code |
| payment_type | VARCHAR(255) | NOT NULL | Payment type (deposit, final, refund) |
| payment_method | VARCHAR(255) | NOT NULL | Payment method (card, bank_transfer) |
| payment_status | VARCHAR(255) | NOT NULL | Status (pending, completed, failed, refunded, cancelled). `cancelled` is used only for unpaid scheduled installments stopped by provider suspension or deactivation (FR-017 v2.10) |
| stripe_payment_intent_id | VARCHAR(255) | NULLABLE | Stripe PaymentIntent ID |
| transaction_id | VARCHAR(255) | NULLABLE | External transaction reference |
| metadata | JSON | NULLABLE | Additional payment metadata |
| installment_plan_id | UUID | FOREIGN KEY, NULLABLE | References installment_plans.id |
| installment_number | INTEGER | NULLABLE | Current installment number (e.g., 1 of 5) |
| total_installments | INTEGER | NULLABLE | Total number of installments in plan |
| is_installment | BOOLEAN | DEFAULT false | Whether this is part of an installment plan |
| reconciliation_flag | VARCHAR(255) | NOT NULL, DEFAULT 'none' | `none` or `captured_after_provider_cancellation` (FR-017 Rule 14) |
| provider_status_event_id | UUID | NULLABLE | Provider status-change event that cancelled the booking; set when `reconciliation_flag` is not `none` |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `quote_id`, `patient_id`, `provider_id`, `payment_status`
- INDEX: `reconciliation_flag`

**Business Rules (FR-015 v1.13 Rule 9, FR-017 v2.10 Rules 14-16)**:

- A payment captured after its booking was cancelled with `ProviderSuspended` or `ProviderDeactivated` is stored as `completed` with `reconciliation_flag` = `captured_after_provider_cancellation`. It never confirms a booking or reopens the case, and it is excluded from provider earnings, payout, and commission until an admin resolves it through the existing refund or adjustment workflow (reason and audit entry required).
- When a booking is cancelled by provider suspension or deactivation, its `installment_payment_plans` row (§31) moves to `cancelled` and its unpaid scheduled installments move to `cancelled`; no further charges or retries run. Paid installments stay `completed` and go to admin resolution.

**Relationships**:

- `belongsTo` → `Quote`
- `belongsTo` → `Patient`
- `belongsTo` → `Provider`

---

### 13. After Care

**Table**: `after_cares`  
**Description**: Post-treatment aftercare tracking (treatment-linked and standalone)

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique aftercare identifier |
| quote_id | UUID | FOREIGN KEY, NULLABLE | References quotes.id (NULL for standalone aftercare) |
| provider_id | UUID | FOREIGN KEY, NOT NULL | References providers.id (assigned provider) |
| patient_id | UUID | FOREIGN KEY, NOT NULL | References patients.id |
| aftercare_type | VARCHAR(255) | NOT NULL | Type: treatment_linked, standalone |
| aftercare_template_id | UUID | FOREIGN KEY, NOT NULL | References aftercare_milestone_templates.id |
| recovery_stage | VARCHAR(255) | NOT NULL | Current recovery stage/milestone |
| recovery_percentage | INTEGER | DEFAULT 0 | Overall recovery progress (0-100) |
| status | VARCHAR(255) | DEFAULT 'active' | Aftercare status (active, completed, suspended, cancelled) |
| pricing_model | VARCHAR(255) | NULLABLE | For standalone: fixed, monthly_subscription |
| total_price | DECIMAL(10,2) | NULLABLE | For standalone: total price |
| currency | VARCHAR(3) | NULLABLE | For standalone: currency code |
| duration_months | INTEGER | NULLABLE | For standalone: duration (6, 12 months) |
| cancellation_cause | VARCHAR(255) | NULLABLE | Provider-status cascade cause: `ProviderSuspended` or `ProviderDeactivated` |
| support_required | BOOLEAN | DEFAULT false | Independent `supportRequired` marker (not a status); cleared only by audited admin resolution |
| provider_status_event_id | UUID | NULLABLE | Reference to the provider status-change event |
| provider_status_effective_at | TIMESTAMP | NULLABLE | Effective time of that provider status change |
| prior_stage | VARCHAR(255) | NULLABLE | Aftercare stage immediately before cancellation |
| support_resolved_at | TIMESTAMP | NULLABLE | When an admin resolved the support marker |
| support_resolved_by | UUID | FOREIGN KEY, NULLABLE | References users.id (resolving admin) |
| support_resolution_reason | TEXT | NULLABLE | Mandatory admin resolution reason |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `quote_id`, `patient_id`, `provider_id`, `aftercare_type`, `status`
- INDEX: `support_required`, `cancellation_cause`

**Relationships**:

- `belongsTo` → `Quote` (nullable for standalone)
- `belongsTo` → `Provider`
- `belongsTo` → `Patient`
- `belongsTo` → `AftercareMilestoneTemplate`
- `hasMany` → `AfterCareInstruction`
- `hasMany` → `AfterCareMedication`
- `hasMany` → `AftercareMilestone`

**Business Rules**:

- `treatment_linked`: quote_id is NOT NULL (linked to treatment booking)
- `standalone`: quote_id is NULL (purchased separately, assigned by admin)
- Provider fault, suspension, or deactivation during treatment-linked aftercare does not cancel the aftercare, the booking, or the treatment record: the row stays `active`, `support_required` is set, and an admin reassigns the aftercare provider or team by changing `provider_id` with a mandatory reason and an audit entry (previous provider, new provider, admin, time). The reassignment sends `aftercare.provider_reassigned` (FR-011) to the patient and the new aftercare provider; the notice is mandatory. No new acceptance, booking, or payment is created.
- Provider suspension or deactivation cancels standalone aftercare for that provider (`status` → `cancelled`) and sets the provider-status cancellation fields; rules as in §5 Inquiries

---

### 14. Aftercare Milestone Templates (Admin-Created)

**Table**: `aftercare_milestone_templates`  
**Description**: Admin-created milestone templates for aftercare plans (e.g., "Standard FUE Aftercare - 12 months")

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique template identifier |
| template_name | VARCHAR(255) | NOT NULL | Template name (e.g., "Standard FUE Aftercare - 12 months") |
| template_description | TEXT | NULLABLE | Template description |
| duration_months | INTEGER | NOT NULL | Total duration (6, 12, 18 months) |
| status | VARCHAR(255) | DEFAULT 'active' | Template status (active, inactive) |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `status`

**Relationships**:

- `hasMany` → `AftercareMilestoneDefinition` (milestone stages in template)
- `hasMany` → `AfterCare` (aftercare plans using this template)

---

### 15. Aftercare Milestone Definitions

**Table**: `aftercare_milestone_definitions`  
**Description**: Individual milestone stages within a template (e.g., "Post-Op Phase - 7 days")

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique definition identifier |
| template_id | UUID | FOREIGN KEY, NOT NULL | References aftercare_milestone_templates.id |
| milestone_name | VARCHAR(255) | NOT NULL | Milestone name (e.g., "Post-Op Phase", "Early Recovery") |
| duration_days | INTEGER | NOT NULL | Duration of this milestone (7, 30, 90 days) |
| order_index | INTEGER | NOT NULL | Order in sequence (1, 2, 3...) |
| scan_frequency_days | INTEGER | NULLABLE | How often to request scan/photo set (1=daily, 5=every 5 days, 7=weekly) |
| scan_count | INTEGER | NULLABLE | How many scans required in this milestone |
| questionnaire_frequency_days | INTEGER | NULLABLE | How often to request questionnaire (1=daily, 7=weekly) |
| activity_restrictions | JSON | NULLABLE | List of activity restrictions for this phase |
| resources | JSON | NULLABLE | Educational resources (video URLs, guide URLs) |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `template_id`, `order_index`

**Relationships**:

- `belongsTo` → `AftercareMilestoneTemplate`
- `hasMany` → `AftercareMilestoneDefinitionQuestionnaire` (linked questionnaires)

---

### 16. Aftercare Milestones (Patient-Specific)

**Table**: `aftercare_milestones`  
**Description**: Patient-specific milestone instances (generated from template definitions)

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique milestone identifier |
| after_care_id | UUID | FOREIGN KEY, NOT NULL | References after_cares.id |
| milestone_definition_id | UUID | FOREIGN KEY, NOT NULL | References aftercare_milestone_definitions.id |
| milestone_name | VARCHAR(255) | NOT NULL | Milestone name (copied from definition) |
| start_date | DATE | NOT NULL | Milestone start date |
| end_date | DATE | NOT NULL | Milestone end date |
| milestone_status | VARCHAR(255) | DEFAULT 'pending' | Status (pending, in_progress, completed, overdue) |
| completion_percentage | INTEGER | DEFAULT 0 | % complete based on scans + questionnaires |
| notes | TEXT | NULLABLE | Provider or patient notes |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `after_care_id`, `milestone_status`, `start_date`, `end_date`

**Relationships**:

- `belongsTo` → `AfterCare`
- `belongsTo` → `AftercareMilestoneDefinition`
- `hasMany` → `AftercareMilestoneScan` (scan uploads for this milestone; V1 photo set, V2 true 3D)
- `hasMany` → `AftercareQuestionnaireResponse` (questionnaire responses)

---

### 17. Aftercare Milestone Scans

**Table**: `aftercare_milestone_scans`  
**Description**: Scan uploads at recovery milestones (V1 photo set; V2 true 3D)

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique scan identifier |
| aftercare_milestone_id | UUID | FOREIGN KEY, NOT NULL | References aftercare_milestones.id |
| scan_url | VARCHAR(255) | NOT NULL | S3 path to scan media (V1 photo set image; V2 3D scan asset) |
| scan_type | VARCHAR(255) | NOT NULL | Type (front, top, sides, back, 3d_model) |
| scan_date | DATE | NOT NULL | Date scan was uploaded |
| is_overdue | BOOLEAN | DEFAULT false | Whether scan was submitted late |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `aftercare_milestone_id`, `scan_date`

**Relationships**:

- `belongsTo` → `AftercareMilestone`

---

### 18. Aftercare Questionnaires (Admin-Created)

**Table**: `aftercare_questionnaires`  
**Description**: Admin-created questionnaires for aftercare assessment (pain, sleep, compliance, etc.)

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique questionnaire identifier |
| questionnaire_name | VARCHAR(255) | NOT NULL | Questionnaire name (e.g., "Pain Assessment", "Sleep Quality") |
| questionnaire_description | TEXT | NULLABLE | Description |
| questionnaire_type | VARCHAR(255) | NOT NULL | Type: pain, sleep, compliance, symptom_check |
| questions | JSON | NOT NULL | Array of questions with type and options |
| status | VARCHAR(255) | DEFAULT 'active' | Questionnaire status (active, inactive) |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `questionnaire_type`, `status`

**Relationships**:

- `hasMany` → `AftercareMilestoneDefinitionQuestionnaire` (linked to milestone definitions)
- `hasMany` → `AftercareQuestionnaireResponse` (patient responses)

**Questions JSON Structure**:

```json
[
  {
    "question_id": "pain_level",
    "question_text": "On a scale of 1-10, how much pain are you experiencing?",
    "question_type": "visual_scale",
    "options": {"min": 1, "max": 10},
    "required": true
  },
  {
    "question_id": "pain_location",
    "question_text": "Where is the pain located?",
    "question_type": "text",
    "required": false
  }
]
```

---

### 19. Aftercare Milestone Definition Questionnaires (Junction)

**Table**: `aftercare_milestone_definition_questionnaires`  
**Description**: Links questionnaires to milestone definitions

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique link identifier |
| milestone_definition_id | UUID | FOREIGN KEY, NOT NULL | References aftercare_milestone_definitions.id |
| questionnaire_id | UUID | FOREIGN KEY, NOT NULL | References aftercare_questionnaires.id |
| frequency_days | INTEGER | NOT NULL | How often to request (1=daily, 7=weekly) |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `milestone_definition_id`, `questionnaire_id`

**Relationships**:

- `belongsTo` → `AftercareMilestoneDefinition`
- `belongsTo` → `AftercareQuestionnaire`

---

### 20. Aftercare Questionnaire Responses

**Table**: `aftercare_questionnaire_responses`  
**Description**: Patient responses to aftercare questionnaires

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique response identifier |
| aftercare_milestone_id | UUID | FOREIGN KEY, NOT NULL | References aftercare_milestones.id |
| questionnaire_id | UUID | FOREIGN KEY, NOT NULL | References aftercare_questionnaires.id |
| patient_id | UUID | FOREIGN KEY, NOT NULL | References patients.id |
| responses | JSON | NOT NULL | Patient's answers to all questions |
| response_date | DATE | NOT NULL | Date questionnaire was completed |
| is_overdue | BOOLEAN | DEFAULT false | Whether response was submitted late |
| flagged_urgent | BOOLEAN | DEFAULT false | Auto-flagged for urgent attention (high pain, concerning symptoms) |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `aftercare_milestone_id`, `questionnaire_id`, `patient_id`, `flagged_urgent`, `response_date`

**Relationships**:

- `belongsTo` → `AftercareMilestone`
- `belongsTo` → `AftercareQuestionnaire`
- `belongsTo` → `Patient`

**Responses JSON Structure**:

```json
{
  "pain_level": 3,
  "pain_location": "Donor area, mild discomfort",
  "sleep_hours": 7,
  "sleep_quality": "good",
  "medication_adherence": "yes",
  "symptoms": ["mild swelling", "no bleeding"]
}
```

---

### 21. Standalone Aftercare Requests

**Table**: `standalone_aftercare_requests`  
**Description**: Patient requests for standalone aftercare service (treatment done elsewhere)

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique request identifier |
| patient_id | UUID | FOREIGN KEY, NOT NULL | References patients.id |
| treatment_date | DATE | NOT NULL | When procedure was performed |
| clinic_name | VARCHAR(255) | NOT NULL | Where procedure was done |
| treatment_type | VARCHAR(255) | NOT NULL | Treatment type (FUE, FUT, DHI) |
| graft_count | INTEGER | NULLABLE | Number of grafts (if known) |
| current_concerns | TEXT | NULLABLE | Patient's current concerns or issues |
| photo_urls | JSON | NULLABLE | Uploaded photos (S3 paths) |
| surgeon_notes_url | VARCHAR(255) | NULLABLE | Uploaded surgeon notes (S3 path) |
| duration_months | INTEGER | NOT NULL | Requested duration (6, 12 months) |
| pricing_model | VARCHAR(255) | NOT NULL | Selected payment method (fixed, monthly_subscription) |
| total_price | DECIMAL(10,2) | NOT NULL | Total price |
| currency | VARCHAR(3) | NOT NULL | Currency code |
| request_status | VARCHAR(255) | DEFAULT 'pending' | Status: pending, assigned, activated, rejected |
| assigned_provider_id | UUID | FOREIGN KEY, NULLABLE | References providers.id (NULL until assigned) |
| assigned_by_admin_id | UUID | FOREIGN KEY, NULLABLE | References users.id (admin who assigned) |
| assigned_at | TIMESTAMP | NULLABLE | When provider was assigned |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `patient_id`, `request_status`, `assigned_provider_id`

**Relationships**:

- `belongsTo` → `Patient`
- `belongsTo` → `Provider` (assigned provider)
- `belongsTo` → `User` (admin who assigned)
- `hasOne` → `AfterCare` (created when activated)

**Note (FR-015 v1.9)**: Provider-status cancellation fields for standalone aftercare are stored on the activated `after_cares` row (§13), not on this request.

---

### 16. Reviews

**Table**: `reviews`  
**Description**: Patient reviews and ratings for providers

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique review identifier |
| patient_id | UUID | FOREIGN KEY, NOT NULL | References patients.id |
| provider_id | UUID | FOREIGN KEY, NOT NULL | References providers.id |
| quote_id | UUID | FOREIGN KEY, NULLABLE | References quotes.id |
| overall_rating | INTEGER | NOT NULL | Overall rating (1-5 stars) |
| facility_rating | INTEGER | NULLABLE | Facility cleanliness rating (1-5) |
| staff_rating | INTEGER | NULLABLE | Staff professionalism rating (1-5) |
| results_rating | INTEGER | NULLABLE | Results satisfaction rating (1-5) |
| value_rating | INTEGER | NULLABLE | Value for money rating (1-5) |
| review_text | TEXT | NULLABLE | Written review |
| is_published | BOOLEAN | DEFAULT false | Admin approval status |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `patient_id`, `provider_id`, `quote_id`, `is_published`

**Relationships**:

- `belongsTo` → `Patient`
- `belongsTo` → `Provider`
- `belongsTo` → `Quote`

---

### 17. Conversations

**Table**: `conversations`  
**Description**: Message threads between patients and providers

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique conversation identifier |
| inquiry_id | UUID | FOREIGN KEY, NULLABLE | References inquiries.id |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `inquiry_id`

**Relationships**:

- `belongsTo` → `Inquiry`
- `hasMany` → `Message`

---

### 18. Messages

**Table**: `messages`  
**Description**: Individual messages in conversations

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique message identifier |
| conversation_id | UUID | FOREIGN KEY, NOT NULL | References conversations.id |
| sender_id | UUID | NOT NULL | ID of sender (patient, provider, admin) |
| sender_type | VARCHAR(255) | NOT NULL | Sender model type (Patient, ProviderUser, User) |
| content | TEXT | NOT NULL | Message content |
| attachment_url | VARCHAR(255) | NULLABLE | S3 path to attachment |
| is_read | BOOLEAN | DEFAULT false | Read status |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `conversation_id`, `sender_id`, `sender_type`

**Relationships**:

- `belongsTo` → `Conversation`
- `morphTo` → `sender` (polymorphic)

---

### 19. Affiliates

**Table**: `affiliates`  
**Description**: Marketing partners and influencers

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique affiliate identifier |
| affiliate_name | VARCHAR(255) | NOT NULL | Affiliate name |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Contact email |
| phone_number | VARCHAR(255) | NULLABLE | Contact phone |
| company_name | VARCHAR(255) | NULLABLE | Company name |
| website | VARCHAR(255) | NULLABLE | Website URL |
| contact_person | VARCHAR(255) | NULLABLE | Contact person name |
| address | TEXT | NULLABLE | Physical address |
| city | VARCHAR(255) | NULLABLE | City |
| country | VARCHAR(255) | NULLABLE | Country |
| profile_image | VARCHAR(255) | NULLABLE | S3 path to profile image |
| status | ENUM | DEFAULT 'draft' | Status (draft, active, inactive, suspended) |
| commission_type | ENUM | DEFAULT 'percentage' | Commission type (percentage, fixed) |
| commission_value | DECIMAL(10,2) | DEFAULT 0 | Commission amount/percentage |
| payment_cycle | ENUM | DEFAULT 'monthly' | Payment cycle (weekly, monthly, quarterly) |
| start_date | DATE | NULLABLE | Partnership start date |
| end_date | DATE | NULLABLE | Partnership end date |
| notes | TEXT | NULLABLE | Internal notes |
| discount_codes | JSON | NULLABLE | Associated discount codes |
| feature_flag_enabled | BOOLEAN | DEFAULT true | Feature flag for affiliates module |
| facebook | VARCHAR(255) | NULLABLE | Facebook profile URL |
| instagram | VARCHAR(255) | NULLABLE | Instagram profile URL |
| tiktok | VARCHAR(255) | NULLABLE | TikTok profile URL |
| twitter | VARCHAR(255) | NULLABLE | Twitter profile URL |
| linkedin | VARCHAR(255) | NULLABLE | LinkedIn profile URL |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |
| deleted_at | TIMESTAMP | NULLABLE | Soft delete timestamp |

**Indexes**:

- PRIMARY: `id`
- UNIQUE: `email`
- INDEX: `status`

**Relationships**:

- `hasMany` → `AffiliateDiscountCode`
- `hasMany` → `AffiliateCommission`

---

### 20. Affiliate Discount Codes

**Table**: `affiliate_discount_codes`  
**Description**: Discount codes assigned to affiliates

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique discount code identifier |
| affiliate_id | UUID | FOREIGN KEY, NOT NULL | References affiliates.id |
| code | VARCHAR(255) | UNIQUE, NOT NULL | Discount code (e.g., "INFLUENCER10") |
| discount_type | ENUM | NOT NULL | Type (percentage, fixed) |
| discount_value | DECIMAL(10,2) | NOT NULL | Discount amount/percentage |
| usage_limit | INTEGER | NULLABLE | Maximum number of uses |
| usage_count | INTEGER | DEFAULT 0 | Current usage count |
| start_date | DATE | NULLABLE | Valid from date |
| end_date | DATE | NULLABLE | Valid until date |
| status | ENUM | DEFAULT 'active' | Status (active, inactive, expired) |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- UNIQUE: `code`
- INDEX: `affiliate_id`, `status`

**Relationships**:

- `belongsTo` → `Affiliate`

---

### 21. Locations

**Table**: `locations`  
**Description**: Physical clinic/office locations

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique location identifier |
| name | VARCHAR(200) | NOT NULL | Location name |
| address | TEXT | NOT NULL | Street address line 1 |
| address2 | TEXT | NULLABLE | Street address line 2 |
| address3 | TEXT | NULLABLE | Street address line 3 |
| address4 | TEXT | NULLABLE | Street address line 4 |
| address5 | TEXT | NULLABLE | Street address line 5 |
| city | VARCHAR(50) | NULLABLE | City |
| state | VARCHAR(50) | NULLABLE | State/Province |
| postal_code | VARCHAR(20) | NULLABLE | Postal/ZIP code |
| country | VARCHAR(50) | NULLABLE | Country |
| map_selector | TEXT | NULLABLE | Map coordinates/embed code |
| phone | VARCHAR(20) | NOT NULL | Contact phone |
| email | VARCHAR(255) | NOT NULL | Contact email |
| whatsapp_or_sms | VARCHAR(200) | NULLABLE | WhatsApp/SMS number |
| fax | TEXT | NULLABLE | Fax number |
| description | TEXT | NOT NULL | Location description |
| legal_name | VARCHAR(200) | NOT NULL | Legal entity name |
| tax | VARCHAR(100) | NOT NULL | Tax ID/VAT number |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `country`, `city`

**Relationships**:

- `hasMany` → `Patient`
- `hasMany` → `LocationStartingPrice`

---

### 22. Location Starting Prices

**Table**: `location_starting_prices`  
**Description**: Starting prices displayed for each location/country

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique price identifier |
| location_id | UUID | FOREIGN KEY, NULLABLE | References locations.id |
| country_name | VARCHAR(255) | NULLABLE | Country name |
| starting_price | DECIMAL(10,2) | NOT NULL | Starting price for this location |
| currency | VARCHAR(255) | NOT NULL | Currency code |
| description | TEXT | NULLABLE | Price description |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `location_id`, `country_name`

**Relationships**:

- `belongsTo` → `Location`

---

## Supporting Entities

### 23. Workflow Timeline

**Table**: `workflow_timelines`  
**Description**: Audit trail of workflow events for inquiries/quotes

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique timeline event identifier |
| inquiry_id | UUID | FOREIGN KEY, NOT NULL | References inquiries.id |
| event | VARCHAR(255) | NOT NULL | Event name (inquiry_created, quote_submitted, etc.) |
| metadata | JSON | NULLABLE | Event metadata |
| created_at | TIMESTAMP | AUTO | Event timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `inquiry_id`, `created_at`

**Relationships**:

- `belongsTo` → `Inquiry`

---

### 24. ProviderPreference

**Table**: `provider_preferences`  
**Description**: Provider notification preference settings (maps to FR-020 `ProviderPreference` entity)

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique preference identifier |
| provider_id | UUID | FOREIGN KEY, NOT NULL | References providers.id |
| quote_notification | BOOLEAN | DEFAULT true | Notify on new inquiries |
| schedule_notification | BOOLEAN | DEFAULT true | Notify on booking confirmations |
| start_treatment_notification | BOOLEAN | DEFAULT true | Notify on treatment start |
| after_care_notification | BOOLEAN | DEFAULT false | Notify on aftercare events |
| review_notification | BOOLEAN | DEFAULT false | Notify on new reviews |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `provider_id`

**Relationships**:

- `belongsTo` → `Provider`

---

### 25. Discounts (Legacy)

**Table**: `discounts`  
**Description**: **Legacy** discount table. It is not the FR-019 promotion program store: programmes live in `promotion_programs` (§25A) and codes in `promotion_codes` (§25B), which `quote_option_date_prices.promotion_id`, `acceptance_events.promotion_id` and `promotion_code_id`, `promotion_applications.program_id` and `code_id`, and `promotion_use_reservations.program_id` reference. `discounts` is retained only for the deprecated `quotes.discount_id` until every consumer migrates; no new program is written here

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique discount identifier |
| discount_code | VARCHAR(255) | UNIQUE, NULLABLE | **Legacy** discount code |
| discount_type | ENUM | NOT NULL | Type (percentage, fixed) |
| discount_value | DECIMAL(10,2) | NOT NULL | Discount amount/percentage |
| provider_id | UUID | FOREIGN KEY, NULLABLE | If provider-specific, references providers.id |
| usage_limit | INTEGER | NULLABLE | **Legacy** maximum uses |
| usage_count | INTEGER | DEFAULT 0 | **Legacy** counter; MUST NOT be used for any FR-019 usage-limit check |
| start_date | DATE | NULLABLE | Valid from |
| end_date | DATE | NULLABLE | Valid until |
| status | ENUM | DEFAULT 'active' | Status (active, inactive, expired) |
| requires_provider_approval | BOOLEAN | DEFAULT false | Whether discount affecting both fees requires provider approval |
| approval_status | VARCHAR(255) | DEFAULT 'pending' | Approval status (pending, approved, rejected) - for platform discounts |
| approved_by_provider_id | UUID | FOREIGN KEY, NULLABLE | References providers.id - provider who approved discount |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- UNIQUE: `discount_code`
- INDEX: `provider_id`, `status`

**Relationships**:

- `belongsTo` → `Provider` (if provider-specific)
- `hasMany` → `Quote` through the deprecated `discount_id`

---

### 25A. Promotion Programs

**Table**: `promotion_programs`  
**Description**: FR-019 PromotionProgram: a promotion defined by an admin or a provider, with its funding model, application mode, discount, limits, and lifecycle. Referenced by `quote_option_date_prices.promotion_id`, `acceptance_events.promotion_id`, `promotion_applications.program_id`, and `promotion_use_reservations.program_id`.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique program identifier |
| program_type | VARCHAR(255) | NOT NULL | `ADMIN_VIA_PROVIDER`, `PROVIDER_SELF`, or `HAIRLINE_FUNDED_DIRECT_ISSUED` |
| scope | VARCHAR(255) | NOT NULL, DEFAULT 'REUSABLE' | `REUSABLE` or `AD_HOC_QUOTE_BOUND` (`AD_HOC_QUOTE_BOUND` only for `PROVIDER_SELF`) |
| bound_quote_id | UUID | FOREIGN KEY, NULLABLE | References quotes.id; set only for `AD_HOC_QUOTE_BOUND` |
| bound_quote_option_date_price_id | UUID | FOREIGN KEY, NULLABLE | References quote_option_date_prices.id; set only for `AD_HOC_QUOTE_BOUND` |
| owner_type | VARCHAR(255) | NOT NULL | `admin` or `provider` |
| owner_id | UUID | NOT NULL | Admin user ID or provider ID that owns the program |
| name | VARCHAR(255) | NOT NULL | Program name |
| description | TEXT | NULLABLE | Program description |
| funding_model | VARCHAR(255) | NOT NULL | `both_fees`, `hairline_only`, or `provider_only`; derived from `program_type` and never set independently |
| hairline_share_percent | DECIMAL(5,2) | NULLABLE | Hairline share of the discount (0-100) that Hairline reimburses to the provider at payout, on top of the commission effect; required for `both_fees`, NULL otherwise. Payout mechanics follow FR-017 and the payment documentation |
| application_mode | VARCHAR(255) | NOT NULL | `auto`, `code_only`, `list_selection`, or `either` |
| discount_type | VARCHAR(255) | NOT NULL | `percentage`, `fixed_amount`, or `package_upgrade` |
| discount_value | DECIMAL(10,2) | NULLABLE | Percentage (0-100) or fixed amount; NULL for `package_upgrade` |
| discount_currency | VARCHAR(3) | NULLABLE | Currency of a `fixed_amount` value; NULL otherwise |
| upgrade_details | JSON | NULLABLE | What a `package_upgrade` adds; NULL otherwise |
| applies_to | VARCHAR(255) | NOT NULL | `whole_price`, `treatment`, `travel`, or `other` |
| starts_at | TIMESTAMP | NULLABLE | Start of the active window |
| ends_at | TIMESTAMP | NULLABLE | End of the active window |
| usage_limit | INTEGER | NULLABLE | Total usage limit; NULL means unlimited. Enforced against active `promotion_use_reservations` (§7M) plus `promotion_applications` (§7L) uses that have not been returned |
| per_user_usage_limit | INTEGER | NULLABLE | Maximum uses per patient; NULL means unlimited |
| targeting | JSON | NULLABLE | Eligibility and targeting rules |
| issuance_channel | VARCHAR(255) | NULLABLE | Issuance channel for Hairline-funded programs |
| lifecycle_state | VARCHAR(255) | NOT NULL, DEFAULT 'draft' | `draft`, `pending_approval`, `active`, `paused`, `expired`, or `archived` |
| created_by | UUID | NOT NULL | Creating admin or provider user |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `program_type`, `lifecycle_state`, `application_mode`
- INDEX: `owner_type`, `owner_id`
- INDEX: `bound_quote_id`

**Business Rules**:

- How a promotion reached a quote (`provider_selected`, `auto_attached`, or `patient_code`) is recorded per use on `promotion_applications.source` (§7L), not on the program.
- One automatic promotion per parent quote; if several automatic programs qualify, the FR-019 priority order picks one (§7M).
- Terms (type, value, currency, applies-to, funding model, Hairline share) are copied into the quote at send and frozen at acceptance; edits apply only to quotes sent afterwards.

**Relationships**:

- `hasMany` → `PromotionCode` (§25B), `PromotionApplication` (§7L), `PromotionUseReservation` (§7M)
- `hasMany` → `QuoteOptionDatePrice` (§7C) through `promotion_id`

---

### 25B. Promotion Codes

**Table**: `promotion_codes`  
**Description**: FR-019 PromotionCode: one code of a promotion program. A program can have many codes.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique code identifier |
| program_id | UUID | FOREIGN KEY, NOT NULL | References promotion_programs.id |
| code | VARCHAR(255) | NOT NULL, UNIQUE | Code text |
| recipient_binding_type | VARCHAR(255) | NOT NULL, DEFAULT 'open' | `open`, `affiliate`, `segment`, or `patient` |
| recipient_binding_id | UUID | NULLABLE | Affiliate, segment, or patient ID when bound |
| status | VARCHAR(255) | NOT NULL, DEFAULT 'unused' | `unused`, `in_progress` (a use is reserved by an accepted subquote and the first payment has not succeeded), `redeemed`, `revoked`, or `expired` |
| issued_at | TIMESTAMP | NOT NULL | Issue time |
| issued_by | UUID | NOT NULL | Issuing admin or provider user |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- UNIQUE: `code`
- INDEX: `program_id`, `status`

**Relationships**:

- `belongsTo` → `PromotionProgram` (§25A)
- `hasMany` → `PromotionApplication` (§7L) through `code_id`

---

### 26. Files

**Table**: `files`  
**Description**: Generic file storage for various entities

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique file identifier |
| fileable_id | UUID | NOT NULL | Related entity ID (polymorphic) |
| fileable_type | VARCHAR(255) | NOT NULL | Related entity type (polymorphic) |
| file_path | VARCHAR(255) | NOT NULL | S3 path to file |
| file_name | VARCHAR(255) | NOT NULL | Original file name |
| file_type | VARCHAR(255) | NOT NULL | MIME type |
| file_size | INTEGER | NOT NULL | File size in bytes |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `fileable_id`, `fileable_type`

**Relationships**:

- `morphTo` → `fileable` (polymorphic to any entity)

---

## Permission & Role Management (Spatie)

### 27. Roles

**Table**: `roles`  
**Description**: User roles (admin, provider owner, doctor, etc.)

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | Role identifier |
| name | VARCHAR(255) | NOT NULL | Role name |
| guard_name | VARCHAR(255) | NOT NULL | Guard name (api, provider, patient) |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- UNIQUE: `(name, guard_name)`

---

### 28. Permissions

**Table**: `permissions`  
**Description**: Granular permissions (create_quote, view_patient, etc.)

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | BIGINT | PRIMARY KEY, AUTO_INCREMENT | Permission identifier |
| name | VARCHAR(255) | NOT NULL | Permission name |
| guard_name | VARCHAR(255) | NOT NULL | Guard name |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- UNIQUE: `(name, guard_name)`

---

### 29. Model Has Roles

**Table**: `model_has_roles`  
**Description**: Junction table for user-role assignments

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| role_id | BIGINT | FOREIGN KEY, NOT NULL | References roles.id |
| model_type | VARCHAR(255) | NOT NULL | Model type (User, ProviderUser, Patient) |
| model_id | UUID | NOT NULL | Model ID |

**Indexes**:

- PRIMARY: `(role_id, model_id, model_type)`

---

### 30. Role Has Permissions

**Table**: `role_has_permissions`  
**Description**: Junction table for role-permission assignments

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| permission_id | BIGINT | FOREIGN KEY, NOT NULL | References permissions.id |
| role_id | BIGINT | FOREIGN KEY, NOT NULL | References roles.id |

**Indexes**:

- PRIMARY: `(permission_id, role_id)`

---

## OAuth & Authentication (Laravel Passport)

### 31. OAuth Access Tokens

**Table**: `oauth_access_tokens`  
**Description**: Access tokens for authenticated sessions

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(100) | PRIMARY KEY | Token identifier |
| user_id | UUID | NULLABLE | User ID |
| client_id | UUID | NOT NULL | OAuth client ID |
| name | VARCHAR(255) | NULLABLE | Token name |
| scopes | TEXT | NULLABLE | Token scopes |
| revoked | BOOLEAN | NOT NULL | Revoked status |
| created_at | TIMESTAMP | AUTO | Token creation timestamp |
| updated_at | TIMESTAMP | AUTO | Token update timestamp |
| expires_at | TIMESTAMP | NULLABLE | Token expiration timestamp |

---

### 32. OAuth Clients

**Table**: `oauth_clients`  
**Description**: OAuth client applications

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Client identifier |
| user_id | UUID | NULLABLE | Owner user ID |
| name | VARCHAR(255) | NOT NULL | Client name |
| secret | VARCHAR(100) | NULLABLE | Client secret |
| provider | VARCHAR(255) | NULLABLE | Provider (Google, Facebook, etc.) |
| redirect | TEXT | NOT NULL | Redirect URL |
| personal_access_client | BOOLEAN | NOT NULL | Is personal access client |
| password_client | BOOLEAN | NOT NULL | Is password client |
| revoked | BOOLEAN | NOT NULL | Revoked status |
| created_at | TIMESTAMP | AUTO | Client creation timestamp |
| updated_at | TIMESTAMP | AUTO | Client update timestamp |

---

## Database Constraints & Relationships Summary

### Foreign Key Constraints

All foreign keys are defined with **ON DELETE** rules to maintain referential integrity:

- **CASCADE**: Child records deleted when parent is deleted
  - `messages.conversation_id` → `conversations.id` (CASCADE)

- **SET NULL**: Child records set to NULL when parent is deleted
  - `quotes.discount_id` → `discounts.id` (SET NULL; legacy column)


- **RESTRICT**: Prevent parent deletion if children exist. Patients and providers are soft-deleted, never hard-deleted, so these rules never remove an append-only acceptance, booking, or promotion record
  - `inquiries.patient_id` → `patients.id` (RESTRICT)
  - `quotes.provider_id` → `providers.id` (RESTRICT; `provider_id` is NOT NULL and providers are soft-deleted)
  - `inquiry_providers.inquiry_id` → `inquiries.id`, `inquiry_date_ranges.inquiry_id` → `inquiries.id`, `quote_option_date_prices.source_inquiry_date_range_id` → `inquiry_date_ranges.id` (RESTRICT)
  - `acceptance_events.inquiry_id` → `inquiries.id`, `bookings.inquiry_id` → `inquiries.id`, `bookings.patient_id` → `patients.id`, `bookings.provider_id` → `providers.id` (RESTRICT)
  - `quote_documents.quote_id` → `quotes.id` (RESTRICT; quote documents are retained with the quote)
  - `promotion_applications.program_id`, `promotion_use_reservations.program_id`, `promotion_codes.program_id` → `promotion_programs.id`; `promotion_applications.code_id` → `promotion_codes.id`; `promotion_applications.booking_id` → `bookings.id`; `promotion_use_reservations.quote_id` → `quotes.id` (RESTRICT)
  - `quotes.replacement_for_acceptance_event_id` → `acceptance_events.id` (RESTRICT)
  - `quotes.inquiry_id` → `inquiries.id` (RESTRICT; quotes are never cascade-deleted, and accepted quotes referenced by acceptance records are retained)
  - `payments.quote_id` → `quotes.id` (RESTRICT - cannot delete quote with payments)
  - `quote_options.quote_id`, `quote_versions.quote_id`, `quote_audits.quote_id` → `quotes.id` (RESTRICT)
  - `quote_option_items.quote_option_id`, `quote_option_date_prices.quote_option_id`, `quote_option_plan_days.quote_option_id` → `quote_options.id` (RESTRICT)
  - `acceptance_events.accepted_parent_quote_id` → `quotes.id`, `acceptance_events.quote_option_id` → `quote_options.id`, `acceptance_events.option_date_price_id` → `quote_option_date_prices.id` (RESTRICT)
  - `acceptance_supersessions.superseded_acceptance_event_id` and `replacement_acceptance_event_id`, `acceptance_annotations.acceptance_event_id`, `promotion_applications.acceptance_event_id`, `bookings.acceptance_event_id` → `acceptance_events.id` (RESTRICT; acceptance records are append-only)
  - `schedules.booking_id`, `travel_contexts.booking_id`, `treatment_records.booking_id` → `bookings.id` (RESTRICT)
  - `passport_details.travel_context_id`, `hotels.travel_context_id`, `flights.travel_context_id` → `travel_contexts.id` (RESTRICT; superseded versions are retained)
  - `treatment_detail_changes.treatment_record_id` → `treatment_records.id` (RESTRICT)
  - `quote_options` (`source_package_id`, `source_package_version`), `package_items` and `package_plan_days` (`package_id`, `package_version`) → `packages` (`id`, `version`) (RESTRICT; packages are never hard-deleted)

### Unique Constraints

- **Patients**: `email`, `username`, `patient_code`
- **Providers**: `email` (per provider)
- **Provider Users**: `email`
- **Users**: `email`, `username`
- **Affiliates**: `email`
- **Discount Codes**: `code`
- **Promotion Codes**: `code`
- **Inquiry Providers**: `(inquiry_id, provider_id)`
- **Promotion Use Reservations**: `quote_id` while `state = 'reserved'` (unique index on a generated column)
- **Affiliate Discount Codes**: `code`
- **Quote Option Date Prices**: `(quote_option_id, source_inquiry_date_range_id)`
- **Quote Versions**: `(quote_id, version)`
- **Packages**: `(id, version)`
- **Acceptance Supersessions**: `superseded_acceptance_event_id`, `replacement_acceptance_event_id`
- **Bookings**: `booking_reference`, `acceptance_event_id`, active hold key (`provider_id`, `hold_appointment_at`, `hold_appointment_timezone`) for `accepted`, `confirmed`, `in_progress`, `aftercare`
- **Travel Contexts**: `booking_id`
- **Treatment Records**: `booking_id`, `acceptance_event_id`
- **Flights**: `(travel_context_id, leg_type, version)`

### Composite Indexes

Performance-optimized indexes for common query patterns:

```sql
-- Provider quote lookups
CREATE INDEX idx_quotes_provider_status ON quotes(provider_id, status);

-- Inquiry quote history
CREATE INDEX idx_quotes_inquiry_provider ON quotes(inquiry_id, provider_id);

-- Patient workflow tracking
CREATE INDEX idx_workflow_inquiry_created ON workflow_timelines(inquiry_id, created_at);

-- Payment reconciliation
CREATE INDEX idx_payments_provider_status ON payments(provider_id, payment_status);
```

---

## Data Types & Conventions

### UUID Format

UUIDs are stored as **CHAR(36)** in MySQL:

- Format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
- Generated via: Laravel `Str::uuid()`
- Example: `550e8400-e29b-41d4-a716-446655440000`

### Timestamps

All timestamps use MySQL **TIMESTAMP** type:

- Format: `YYYY-MM-DD HH:MM:SS`
- Timezone: UTC (server timezone)
- Laravel automatically manages `created_at` and `updated_at`

### JSON Columns

JSON columns used for:

- `treatment_schedule` (inquiries): `["2025-11-01", "2025-11-02"]`
- `discount_codes` (affiliates): `["CODE1", "CODE2"]`
- `metadata` (payments, workflow): `{"key": "value"}`

### Decimal Precision

Financial fields use **DECIMAL(10, 2)**:

- Supports values up to 99,999,999.99
- Prevents floating-point rounding errors
- Examples: quote_amount, commission_value, payment amounts

### ENUM Types

Status fields use **VARCHAR** (not native ENUM) for flexibility:

- Allows adding values without schema changes
- Defined as constants in Laravel models
- Examples:
  - Quote status: `draft`, `sent` (exposed as `quote`), `expired`, `withdrawn`, `archived`, `accepted`, `cancelled_other_accepted`, `cancelled_inquiry_cancelled`, `cancelled_provider_status` (no `confirmed`, no `rejected`)
  - Booking status: `accepted`, `payment_window_expired`, `confirmed`, `in_progress`, `aftercare`, `completed`, `cancelled`
  - Inquiry status: `inquiry`, `quoted`, `accepted`, `confirmed`, `in_progress`, `aftercare`, `completed`, `cancelled`
  - Acceptance supersession cause: `ProviderFault`, `ProviderSuspended`, `ProviderDeactivated`
  - Promotion use reservation state: `reserved`, `consumed`, `released`; release reason includes `not_applied`
  - Promotion program lifecycle: `draft`, `pending_approval`, `active`, `paused`, `expired`, `archived`
  - Treatment record status: `awaiting_check_in` (default), `in_progress`, `completed`, `cancelled`
  - Payment status: `pending`, `completed`, `failed`, `refunded`
  - Affiliate status: `draft`, `active`, `inactive`, `suspended`
  - Provider status: `active`, `suspended`, `deactivated` (no `draft`)
  - Provider document type: `medical_license`, `board_certification`, `insurance`, `malpractice_insurance`, `business_license`, `other`
  - Provider-status cancellation cause: `ProviderSuspended`, `ProviderDeactivated`

---

## Data Security & Privacy

### Encrypted Columns

Sensitive data encrypted using Laravel's `Encrypted` cast:

- `patients.medical_history`
- `patients.phone_number`
- `medical_histories.*` (all fields)

### PII (Personally Identifiable Information)

Fields containing PII:

- Patient: `first_name`, `last_name`, `email`, `phone_number`, `birthday`, `profile_image`
- Provider: `email`, `phone_number`
- Provider User: `firstname`, `lastname`, `email`, `phone_number`

**Privacy Measures**:

- Anonymized in provider-facing views until payment
- Excluded from analytics exports
- Subject to GDPR right to deletion

### Audit Trail

All critical entities maintain audit trail via:

- `created_at`, `updated_at` timestamps
- `workflow_timelines` for state transitions
- Model observers logging changes
- Soft deletes (`deleted_at`) for recoverability
- Admin edits of provider data require a change reason, stored with the audit entry (FR-015)
- Login as Provider sessions are audited with the admin's reason, re-authentication, and a 30-minute session timeout (FR-015)
- Provider status changes (suspension, deactivation, reactivation) and admin resolution of `support_required` markers are audited events
- `acceptance_events`, `acceptance_supersessions`, `acceptance_annotations`, `quote_versions`, `quote_audits`, and `treatment_detail_changes` are append-only: never updated, deleted, soft-deleted, or restored

---

## Migration Strategy

### Migration Execution Order

Migrations are executed in chronological order based on filename timestamps. Key dependencies:

1. **Core Users** (2014-2024)
   - `users`, `password_reset_tokens`

2. **OAuth** (2016)
   - `oauth_*` tables

3. **Roles & Permissions** (2024-01)
   - `roles`, `permissions`, `model_has_roles`, `role_has_permissions`

4. **Providers & Patients** (2024-01)
   - `providers`, `provider_users`, `patients`

5. **Inquiry & Quote Flow** (2024-02)
   - `promotion_programs`, `promotion_codes` (after `providers`; `bound_quote_id` and `bound_quote_option_date_price_id` foreign keys added after `quotes` and `quote_option_date_prices`)
   - `inquiries`, `inquiry_providers`, `inquiry_date_ranges`, `medical_histories`, `treatments`, `packages`, `package_items`, `package_plan_days`, `quotes` (after `treatments` and `packages`; `quotes.treatment_id` is NOT NULL)
   - `quote_options`, `quote_option_items`, `quote_option_date_prices`, `quote_option_plan_days`, `quote_versions`, `quote_audits`
   - `acceptance_events`, `acceptance_supersessions`, `acceptance_annotations`, `promotion_use_reservations` (after `acceptance_events`); `quotes.replacement_for_acceptance_event_id` foreign key added after `acceptance_events`

6. **Payments & Scheduling** (2024-03+)
   - `bookings`, `promotion_applications` (after `bookings`; references `booking_id`), `payments`, `schedules`, `after_cares`, `travel_contexts`, `treatment_records`, `treatment_detail_changes` (after `treatment_records`)
   - `passport_details`, `hotels`, `flights` (after `travel_contexts`; keyed by `travel_context_id`)

7. **Communication & Reviews** (2024-07+)
   - `conversations`, `messages`, `reviews`

8. **Recent Additions** (2025)
   - `affiliates`, `locations`, `provider_team_members`
   - `discounts` (legacy; kept for the deprecated `quotes.discount_id`, so it must exist before that foreign key is added)

### Rolling Back Migrations

All migrations implement `down()` method for rollback:

```bash
# Rollback last migration
php artisan migrate:rollback

# Rollback last 5 migrations
php artisan migrate:rollback --step=5

# Rollback all migrations
php artisan migrate:reset
```

### Fresh Database Setup

```bash
# Drop all tables and re-run all migrations
php artisan migrate:fresh

# With seeders
php artisan migrate:fresh --seed
```

---

## Database Seeding

### Seeder Classes

Located in `database/seeders/`:

- `DatabaseSeeder.php` - Master seeder
- `UserSeeder.php` - Admin users
- `ProviderSeeder.php` - Sample providers
- `PatientSeeder.php` - Sample patients
- `TreatmentSeeder.php` - Treatment packages
- `LocationSeeder.php` - Clinic locations
- `PermissionSeeder.php` - Roles and permissions

### Running Seeders

```bash
# Run all seeders
php artisan db:seed

# Run specific seeder
php artisan db:seed --class=ProviderSeeder

# Refresh database with seeders
php artisan migrate:fresh --seed
```

---

## Performance Optimization

### Query Optimization

**Eager Loading**:

```php
// Prevent N+1 queries
$quotes = Quote::with(['provider', 'inquiry.patient', 'treatment'])->get();
```

**Selective Column Loading**:

```php
// Only select needed columns
$patients = Patient::select('id', 'first_name', 'last_name', 'email')->get();
```

**Pagination**:

```php
// Paginate large result sets
$patients = Patient::paginate(20);
```

### Caching

**Cache Keys**:

- `provider:{id}:profile` - Provider profile data (1 hour)
- `location:{country}:providers` - Providers by country (6 hours)
- `treatment:{id}:package` - Treatment package details (24 hours)

**Cache Invalidation**:

- Model observers trigger cache invalidation on updates
- Manual flush for critical changes

### Index Recommendations

Analyze slow queries using:

```sql
-- Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;

-- Check index usage
EXPLAIN SELECT * FROM quotes WHERE provider_id = 'xxx' AND status = 'accepted';
```

---

### 31. Installment Payment Plans

**Table**: `installment_payment_plans`  
**Description**: Split payment plans for patients (interest-free installments)

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique plan identifier |
| quote_id | UUID | FOREIGN KEY, NOT NULL | References quotes.id |
| patient_id | UUID | FOREIGN KEY, NOT NULL | References patients.id |
| total_amount | DECIMAL(10,2) | NOT NULL | Total amount to be paid; read-only copy of the booking total from the accepted snapshot through the booking, never recomputed from a live quote |
| currency | VARCHAR(3) | NOT NULL | Read-only copy of the quote currency from the accepted snapshot; used for every instalment |
| exchange_rate | DECIMAL(18,8) | NULLABLE | Read-only copy of the exchange rate from the accepted snapshot |
| installment_amount | DECIMAL(10,2) | NOT NULL | Amount per installment |
| number_of_installments | INTEGER | NOT NULL | Total installments (2-9) |
| completed_installments | INTEGER | DEFAULT 0 | Number of completed payments |
| payment_frequency | VARCHAR(255) | DEFAULT 'monthly' | Frequency (weekly, monthly) |
| first_payment_date | DATE | NOT NULL | Date of first installment |
| final_payment_date | DATE | NOT NULL | Date of last installment (must be 30 days before procedure) |
| status | VARCHAR(255) | DEFAULT 'active' | Status (active, completed, cancelled, defaulted). Set to `cancelled` when the booking is cancelled by provider suspension or deactivation (FR-017 v2.10; see §12 business rules) |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `quote_id`, `patient_id`, `status`

**Relationships**:

- `belongsTo` → `Quote`
- `belongsTo` → `Patient`
- `hasMany` → `Payment`

---

### 32. Hotels (Travel Records — Provider Entry, Path A)

**Table**: `hotels`
**Description**: FR-008 HotelRecord. Hotel booking details entered by provider (Path A) or patient (Path B) for a confirmed booking, owned by its travel context. One current record per confirmed booking in MVP. Immutable after submission; admin corrections create a new versioned record.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique hotel record identifier |
| travel_context_id | UUID | FOREIGN KEY, NOT NULL | References travel_contexts.id (booking-owned travel anchor; accepted quote provenance is read from the travel context) |
| hotel_name | VARCHAR(255) | NOT NULL | Full name of the hotel/lodging |
| hotel_address | TEXT | NOT NULL | Full address |
| check_in_date | DATE | NOT NULL | Arrival date |
| check_in_time | TIME | NOT NULL | Expected check-in time |
| check_out_date | DATE | NOT NULL | Departure date (must be after check_in_date) |
| check_out_time | TIME | NOT NULL | Expected check-out time |
| reservation_number | VARCHAR(100) | NOT NULL | Booking/reservation reference |
| room_type | VARCHAR(255) | NOT NULL | Room category (Single, Double, Suite, etc.) |
| amenities | TEXT | NULLABLE | Gym, breakfast, parking, etc. |
| transportation | TEXT | NULLABLE | Airport pickup and transfer notes (canonical transport field in MVP) |
| special_request | TEXT | NULLABLE | Accessibility needs, preferences |
| contact_number | VARCHAR(50) | NULLABLE | Hotel contact phone |
| contact_email | VARCHAR(255) | NULLABLE | Hotel contact email |
| submitted_by | VARCHAR(50) | NOT NULL | Submitter role: `patient` or `provider` |
| submitted_by_id | UUID | NOT NULL | User ID of the submitter |
| submitted_at | TIMESTAMP | NOT NULL | Submission timestamp |
| version | INTEGER | DEFAULT 1 | Version number; incremented on admin correction |
| superseded_by | UUID | FOREIGN KEY, NULLABLE | References hotels.id of the corrected version |
| copied_from_hotel_id | UUID | FOREIGN KEY, NULLABLE | References hotels.id of the source record on the closed booking when copied by a provider-fault transfer |
| travel_date_review_required | BOOLEAN | NOT NULL, DEFAULT false | True on a provider-fault transfer copy until an admin confirms or corrects its dates |
| early_departure_acknowledged_by | UUID | NULLABLE | User who acknowledged the warning that check-out falls before the last treatment plan day |
| early_departure_acknowledged_at | TIMESTAMP | NULLABLE | When that warning was acknowledged; non-NULL shows the provider an early-departure flag |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `travel_context_id`, `submitted_by_id`, `version`

**Relationships**:

- `belongsTo` → `TravelContext` (`travel_context_id`)
- Shown in the FR-008 itinerary read view of the same travel context as its hotel record (no itineraries table)

**Business Rules**:

- Locked immediately after submission. No edits by patient or provider post-submission.
- Admin corrections write a new version (version + 1) and set `superseded_by` on the old record.
- One current (non-superseded) hotel record per travel context in MVP.
- On a provider-fault transfer, the current record is copied to the replacement travel context with `copied_from_hotel_id` set and `travel_date_review_required` true; the source stays read-only on the closed travel context. The admin travel-date review clears the flag.

---

### 33. Flights (Travel Records — Flight Legs)

**Table**: `flights`
**Description**: Flight leg details submitted by patient (Path B) or entered by provider (Path A). FR-008 FlightRecord, owned by the confirmed booking's travel context. Up to 2 current records per travel context (outbound + return). Immutable after submission.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique flight record identifier |
| travel_context_id | UUID | FOREIGN KEY, NOT NULL | References travel_contexts.id (booking-owned travel anchor; accepted quote provenance is read from the travel context) |
| leg_type | ENUM | NOT NULL | `outbound` or `return` |
| airline_name | VARCHAR(255) | NOT NULL | Name of the airline |
| flight_number | VARCHAR(20) | NOT NULL | Flight number |
| departure_airport | VARCHAR(255) | NOT NULL | IATA code + airport name |
| arrival_airport | VARCHAR(255) | NOT NULL | IATA code + airport name |
| departure_date | DATE | NOT NULL | Scheduled departure date |
| departure_time | TIME | NOT NULL | Scheduled departure time (HH:MM) |
| arrival_date | DATE | NOT NULL | Scheduled arrival date (must be ≥ departure_date) |
| arrival_time | TIME | NOT NULL | Scheduled arrival time (HH:MM) |
| ticket_confirmation_number | VARCHAR(100) | NOT NULL | Booking reference from airline |
| ticket_class | ENUM | NOT NULL | `Economy`, `Business`, or `First` |
| baggage_allowance | TEXT | NULLABLE | Checked + carry-on allowance details |
| special_request | TEXT | NULLABLE | Seat preference, meal preference, etc. |
| submitted_by | VARCHAR(50) | NOT NULL | Submitter role: `patient` or `provider` |
| submitted_by_id | UUID | NOT NULL | User ID of the submitter |
| submitted_at | TIMESTAMP | NOT NULL | Submission timestamp |
| version | INTEGER | DEFAULT 1 | Version number; incremented on admin correction |
| superseded_by | UUID | FOREIGN KEY, NULLABLE | References flights.id of the corrected version |
| copied_from_flight_id | UUID | FOREIGN KEY, NULLABLE | References flights.id of the source record on the closed booking when copied by a provider-fault transfer |
| travel_date_review_required | BOOLEAN | NOT NULL, DEFAULT false | True on a provider-fault transfer copy until an admin confirms or corrects its dates |
| early_departure_acknowledged_by | UUID | NULLABLE | Return leg only: user who acknowledged the warning that the flight departs before the last treatment plan day |
| early_departure_acknowledged_at | TIMESTAMP | NULLABLE | Return leg only: when that warning was acknowledged; non-NULL shows the provider an early-departure flag |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `travel_context_id`, `leg_type`, `submitted_by_id`
- UNIQUE: `travel_context_id`, `leg_type`, `version` (one record per leg per version within a travel context)

**Relationships**:

- `belongsTo` → `TravelContext` (`travel_context_id`)
- Shown in the FR-008 itinerary read view of the same travel context as its outbound or return flight (no itineraries table)

**Business Rules**:

- Maximum 2 current (non-superseded) flight records per travel context (one per leg_type).
- `total_price` is excluded; cost captured at package/quote level (FR-004/FR-007).
- Locked immediately after submission.
- On a provider-fault transfer, current records are copied to the replacement travel context with `copied_from_flight_id` set and `travel_date_review_required` true; the sources stay read-only on the closed travel context. The admin travel-date review clears the flag.

---

### 34. Passport Details

**Table**: `passport_details`
**Description**: FR-008 PassportRecord. Patient passport data captured for a Path A confirmed booking (provider-booked travel), owned by its travel context. Encrypted at rest. Immutable after submission. Not captured in Path B.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique passport record identifier |
| travel_context_id | UUID | FOREIGN KEY, NOT NULL | References travel_contexts.id (booking-owned travel anchor; accepted quote provenance is read from the travel context) |
| patient_id | UUID | FOREIGN KEY, NOT NULL | References patients.id |
| passport_name | VARCHAR(100) | NOT NULL | Full name as on passport |
| passport_number | VARCHAR(20) | NOT NULL, ENCRYPTED | Machine-readable passport number (AES-256 at rest) |
| passport_dob | DATE | NOT NULL | Date of birth as on passport |
| gender | VARCHAR(20) | NOT NULL | `Male`, `Female`, or `Other` |
| location | VARCHAR(255) | NOT NULL | Country of nationality |
| place_of_birth | VARCHAR(255) | NOT NULL | City/country of birth |
| passport_issue | DATE | NOT NULL | Passport issue date |
| passport_expiry | DATE | NOT NULL | Passport expiry date (must be future date at submission) |
| passport_image | VARCHAR(500) | NOT NULL | Secure storage reference path for passport photo |
| status | ENUM | DEFAULT 'pending' | `pending`, `complete`, `incomplete` |
| submitted_by_id | UUID | NOT NULL | Patient user ID |
| submitted_at | TIMESTAMP | NULLABLE | Submission timestamp (null until submitted) |
| version | INTEGER | DEFAULT 1 | Version number; incremented on admin correction |
| superseded_by | UUID | FOREIGN KEY, NULLABLE | References passport_details.id of corrected version |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `travel_context_id`, `patient_id`, `status`

**Relationships**:

- `belongsTo` → `TravelContext` (`travel_context_id`)
- `belongsTo` → `Patient`
- Shown in the FR-008 itinerary read view of the same travel context as its passport status (no itineraries table)

**Business Rules**:

- `passport_number` and `passport_image` encrypted at rest (AES-256). Access restricted to submitting patient, assigned provider, and admin.
- Displayed masked (`A1234****`) to patient; shown in full to assigned provider and admin only.
- Locked immediately after submission. Admin corrections create a new versioned record.
- One current (non-superseded) passport record per Path A travel context. Eligible prior details may be copied into a new locked record for a new travel context without changing the earlier source record; on a provider-fault transfer the current passport record carries over this way to the replacement travel context.
- Retained for 7 years (medical data retention per constitution). Audit log entries retained for 10 years.

---

### 34A. Travel Contexts

**Table**: `travel_contexts`
**Description**: One travel context per confirmed booking (FR-008 TravelContext), created idempotently from the booking's immutable AcceptanceEvent and accepted subquote snapshot when the booking moves to `confirmed`. Owns the booking's travel records and itinerary. The current appointment is read from the booking; the accepted baseline stays immutable here.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique travel context identifier |
| booking_id | UUID | FOREIGN KEY, NOT NULL, UNIQUE | References bookings.id |
| acceptance_event_id | UUID | FOREIGN KEY, NOT NULL | References acceptance_events.id |
| accepted_parent_quote_id | UUID | FOREIGN KEY, NOT NULL | References quotes.id |
| accepted_parent_quote_version | INTEGER | NOT NULL | Accepted aggregate quote version |
| accepted_subquote_id | UUID | NOT NULL | FR-005 subquote ID |
| accepted_subquote_version | INTEGER | NOT NULL | Same as `accepted_parent_quote_version` |
| quote_option_id | UUID | FOREIGN KEY, NOT NULL | References quote_options.id |
| option_date_price_id | UUID | FOREIGN KEY, NOT NULL | References quote_option_date_prices.id |
| accepted_appointment_date_time | TIMESTAMP | NOT NULL | Accepted appointment baseline from the snapshot |
| accepted_appointment_timezone | VARCHAR(64) | NOT NULL | IANA time zone of the baseline |
| accepted_date_range_start | DATE | NOT NULL | Accepted date range start from the snapshot |
| accepted_date_range_end | DATE | NOT NULL | Accepted date range end from the snapshot |
| included_services_snapshot | JSON | NULLABLE | Included travel services from the accepted option snapshot |
| travel_path | VARCHAR(255) | NOT NULL | `provider_included` or `patient_self_booked` |
| travel_required | BOOLEAN | NOT NULL, DEFAULT true | False means `no_travel_required` |
| travel_required_set_by | UUID | NULLABLE | Actor who last set `travel_required` (patient, or admin override) |
| travel_required_set_at | TIMESTAMP | NULLABLE | When `travel_required` was last set |
| status | VARCHAR(255) | NOT NULL, DEFAULT 'active' | `active`, `travel_date_review_required`, or `closed` |
| review_flagged_at | TIMESTAMP | NULLABLE | When a travel-date review was flagged |
| review_cleared_by | UUID | FOREIGN KEY, NULLABLE | References users.id (admin who cleared the review) |
| review_cleared_at | TIMESTAMP | NULLABLE | When the review was cleared |
| initialized_at | TIMESTAMP | NOT NULL | Creation on booking confirmation |
| initial_request_dispatched_at | TIMESTAMP | NULLABLE | When the initial patient travel request was sent |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- UNIQUE: `booking_id`
- INDEX: `acceptance_event_id`, `status`

**Business Rules**:

- Replayed confirmation events MUST NOT create another travel context or a duplicate initial request.
- The provider package-library ID and version are quote-option provenance, not a travel decision source.
- There is no `itineraries` table. The FR-008 itinerary is a read view assembled from the travel context, its current passport, flight and hotel records, and the booking.

**Relationships**:

- `belongsTo` → `Booking`, `AcceptanceEvent`

---

### 35. Treatment Records (Completion and Case Closure)

**Table**: `treatment_records`
**Description**: Per-booking treatment execution record (FR-010 Entity 1). This entry lists the columns that other modules read: completion and case closure. Day records, photos, and medication instructions are defined in FR-010. Documented from the FR-010 and FR-014 PRDs; implementation reconciliation pending.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique treatment record identifier |
| inquiry_id | UUID | FOREIGN KEY, NOT NULL | References inquiries.id (the confirmed booking's case). Not unique: a provider-fault transfer creates a second booking in the same inquiry, and each booking has its own treatment record |
| quote_id | UUID | FOREIGN KEY, NOT NULL | References quotes.id (accepted parent quote; source of treatment for analytics) |
| booking_id | UUID | FOREIGN KEY, NOT NULL, UNIQUE | References bookings.id; one treatment record per booking |
| acceptance_event_id | UUID | FOREIGN KEY, NOT NULL, UNIQUE | References acceptance_events.id; one treatment record per acceptance; the accepted snapshot is the original record and is never edited |
| accepted_parent_quote_version | INTEGER | NOT NULL | Accepted aggregate quote version |
| accepted_subquote_id | UUID | NOT NULL | FR-005 subquote ID |
| accepted_subquote_version | INTEGER | NOT NULL | Same as `accepted_parent_quote_version` |
| quote_option_id | UUID | FOREIGN KEY, NOT NULL | References quote_options.id |
| option_date_price_id | UUID | FOREIGN KEY, NOT NULL | References quote_option_date_prices.id |
| provider_id | UUID | FOREIGN KEY, NOT NULL | References providers.id |
| status | VARCHAR(255) | NOT NULL, DEFAULT 'awaiting_check_in' | FR-010 treatment status: `awaiting_check_in` (set at creation), `in_progress` (set at Check In), `completed`, or `cancelled` (displayed as Awaiting Check In, In Progress, Completed, Cancelled). `cancelled` is set when an admin cancels the booking before completion; the cause and `support_required` are held on the booking (§11A) |
| check_in_at | TIMESTAMP | NULLABLE | Set at patient Check In |
| completed_at | TIMESTAMP | NULLABLE | Set by Save (Complete Treatment); FR-014 completion and flat-rate commission recognition; FR-011 aftercare trigger |
| closure_reason | ENUM | NULLABLE | `no_show`, `patient_cancellation`, `medical`, `operational`, `other`; set when the provider uses Cancel/Close Case, which records a request and never changes `status` or the booking status by itself |
| closure_note | TEXT | NULLABLE | Provider free-text note for the closure |
| closure_requested_by | UUID | FOREIGN KEY, NULLABLE | References provider_users.id |
| closure_requested_at | TIMESTAMP | NULLABLE | When the closure was requested |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- UNIQUE: `booking_id`, `acceptance_event_id`
- INDEX: `inquiry_id`, `provider_id`, `status`, `completed_at`, `closure_reason`

**Relationships**:

- `belongsTo` → `Inquiry`
- `belongsTo` → `Quote`
- `belongsTo` → `Booking`, `AcceptanceEvent`
- `belongsTo` → `Provider`
- `hasMany` → `TreatmentDetailChange` (§35A)

**Business Rules**:

- The record is created when the booking moves to `confirmed` (first successful payment), so treatment-detail changes from `Confirmed` onward have a record to attach to (§35A). `status` is `awaiting_check_in` from creation until Check In.
- The current treatment plan (relative plan days seeded from the accepted option's plan days in the snapshot), assigned clinicians, and estimated graft count change only through the audited FR-010 treatment-detail change (§35A); money fields are read from the acceptance snapshot only.
- `completed_at` and `closure_reason` are mutually exclusive: a completed treatment has no closure reason, and a case with a closure request has no completion timestamp.
- A provider fault during Aftercare leaves the treatment record unchanged; only the aftercare provider is reassigned (§13).
- No-show is a closure reason (admin-managed case label), not a booking pipeline status. FR-014 counts a booking closed with `no_show` once, as a no-show.
- Admin handles any resulting booking change through the FR-006 governed actions (for example admin cancellation); financial reconciliation follows the payment documentation (FR-010 Workflow B4).

---

### 35A. Treatment Detail Changes

**Table**: `treatment_detail_changes`
**Description**: Append-only audit of post-acceptance treatment-detail changes made through FR-010 (FR-010 Treatment Detail Change). Never alters the accepted snapshot or any money field.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique change identifier |
| treatment_record_id | UUID | FOREIGN KEY, NOT NULL | References treatment_records.id |
| field_group | VARCHAR(255) | NOT NULL | `plan_days`, `clinicians`, or `estimated_graft_count` |
| before_values | JSON | NOT NULL | Values before the change |
| after_values | JSON | NOT NULL | Values after the change |
| reason | TEXT | NOT NULL | Mandatory reason |
| actor_id | UUID | NOT NULL | Actor user ID |
| actor_type | VARCHAR(255) | NOT NULL | `clinic` or `admin` |
| actor_role | VARCHAR(255) | NOT NULL | Actor role |
| notification_event_ref | VARCHAR(255) | NULLABLE | Notification event reference (`treatment.plan_changed`) |
| changed_at | TIMESTAMP | NOT NULL | Change time |

**Indexes**:

- PRIMARY: `id`
- INDEX: `treatment_record_id`, `changed_at`

**Business Rules**:

- No change is allowed while the booking is `accepted` (unpaid). From `confirmed`, clinic changes are allowed until Check In; admin changes are allowed at any time from `confirmed` onward, each with a mandatory reason, an audit entry, and `treatment.plan_changed`. At least one clinician must remain. Plan days stay relative day numbers and are never stored as calendar dates.

**Relationships**:

- `belongsTo` → `TreatmentRecord`

---

### 36. Analytics Configurations

**Table**: `analytics_configurations`
**Description**: Versioned admin settings consumed by FR-014 analytics (FR-026 Entity 12, Screen 5e). Each save inserts a new version; the highest version is active. Documented from the FR-026 PRD; implementation reconciliation pending.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique configuration identifier |
| version_number | INTEGER | NOT NULL, UNIQUE | Increments on every save |
| ttfq_sla_minutes | INTEGER | NOT NULL, DEFAULT 120 | Platform-wide TTFQ SLA target; positive whole minutes |
| at_risk_days | INTEGER | NOT NULL, DEFAULT 7 | Engagement At Risk boundary |
| dormant_days | INTEGER | NOT NULL, DEFAULT 30 | Engagement Dormant boundary; must be greater than `at_risk_days` |
| price_outlier_percent | INTEGER | NOT NULL, DEFAULT 30 | Price outlier threshold; whole percent 1–100 |
| benchmark_refresh_frequency | ENUM | NOT NULL, DEFAULT 'weekly' | `daily`, `weekly`, `monthly` |
| target_monthly_commission | DECIMAL(10,2) | NULLABLE | Optional reference line on FR-014 Screen 12 Widget 2; NULL hides the line |
| change_reason | TEXT | NOT NULL | Admin-entered reason for the change |
| created_by | UUID | FOREIGN KEY, NOT NULL | References users.id (admin) |
| created_at | TIMESTAMP | AUTO | Version creation timestamp (activation time) |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- UNIQUE: `version_number`

**Relationships**:

- `belongsTo` → `User` (created_by)

**Business Rules**:

- Rows are immutable after insert; a change creates a new version.
- FR-014 reads one version per calculation and stores that `version_number` with each analytics aggregate it produces.
- Recalculation: live dashboards recalculate every displayed period with the active version; generated exports are never rewritten (CR-FR026-20261013-01).
- Seeded with one version using the defaults above.

---

### 37. Export Report Configurations

**Table**: `export_report_configurations`
**Description**: Provider one-off and recurring analytics export settings (FR-014 Entity 8, Screen 6). Documented from the FR-014 PRD; implementation reconciliation pending.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique export configuration identifier |
| provider_id | UUID | FOREIGN KEY, NOT NULL | References providers.id |
| report_type | ENUM | NOT NULL | `pdf_summary`, `csv_detailed` |
| screens_included | JSON | NOT NULL | Array of FR-014 provider screen identifiers |
| date_range_type | ENUM | NOT NULL | `custom` (one-off) or `previous_full_period` (recurring) |
| custom_start | DATE | NULLABLE | One-off exports only |
| custom_end | DATE | NULLABLE | One-off exports only |
| recurring | BOOLEAN | NOT NULL, DEFAULT FALSE | Whether this is a scheduled configuration |
| frequency | ENUM | NULLABLE | `weekly`, `monthly`, `quarterly`; required when `recurring` is true |
| timezone | VARCHAR(64) | NULLABLE | IANA timezone copied from `providers.timezone`; defines period boundaries |
| status | ENUM | NOT NULL, DEFAULT 'active' | `active`, `paused` |
| email_recipients | JSON | NULLABLE | Registered provider email (always included) plus up to 5 provider_users IDs |
| next_run_at | TIMESTAMP | NULLABLE | Next scheduled run (06:00 provider local time on the first day after the period ends) |
| last_run_status | ENUM | NULLABLE | `success`, `retrying`, `failed` |
| last_generated_at | TIMESTAMP | NULLABLE | Last successful generation |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `provider_id`, `(recurring, status, next_run_at)`

**Relationships**:

- `belongsTo` → `Provider`

**Business Rules**:

- Maximum 5 active recurring configurations per provider.
- Recipients must be active provider team members permitted to view every included screen; recipients who lose access are dropped at the next run.
- A failed run is retried up to 3 times at 30-minute intervals, then `last_run_status` = `failed` with a manual retry in Report History. No partial report is emailed.
- Generated files are never rewritten after a configuration change.

---

### 38. Provider Pending Status Changes

**Table**: `provider_pending_status_changes`
**Description**: Future-dated provider suspension or deactivation scheduled through FR-015 Screen 4 (FR-015 Key Entity 4). Documented from the FR-015 PRD; implementation reconciliation pending.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique pending change identifier |
| provider_id | UUID | FOREIGN KEY, NOT NULL | References providers.id |
| change_type | VARCHAR(255) | NOT NULL | `suspend` or `deactivate` |
| effective_date | DATE | NOT NULL | Future date on which the midnight UTC job applies the change |
| reason | TEXT | NOT NULL | Admin reason, minimum 20 characters |
| notify_provider | BOOLEAN | DEFAULT true | Whether the provider was emailed about the scheduled change |
| scheduled_by_admin_id | UUID | FOREIGN KEY, NOT NULL | References users.id |
| state | VARCHAR(255) | NOT NULL, DEFAULT 'pending' | `pending`, `applied`, or `cancelled` |
| cancelled_by_admin_id | UUID | FOREIGN KEY, NULLABLE | References users.id |
| cancellation_reason | TEXT | NULLABLE | Admin reason for a manual cancel, or the reactivation reason when Screen 5 cancels it automatically |
| resolved_at | TIMESTAMP | NULLABLE | When the row was applied or cancelled |
| created_at | TIMESTAMP | AUTO | Record creation timestamp (scheduled at) |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `state`, `effective_date`
- UNIQUE (partial): `provider_id` WHERE `state` = 'pending'

**Business Rules (FR-015 v1.13)**:

- At most one `pending` row per provider. An immediate suspension or deactivation, a manual Cancel Scheduled Change, or a Screen 5 reactivation moves the pending row to `cancelled`.
- On `effective_date`, the job sets `providers.status`, runs the provider-status cancellation cascade, and moves the row to `applied`.
- Every state change is audit-logged and shown in FR-015 Tab 8.
- A `deactivate` row that processes an account-closure request (§40) must have `notify_provider` = true; FR-015 A7 locks Notify Provider on (FR-015 v1.16).

**Relationships**:

- `belongsTo` → `Provider`
- `belongsTo` → `User` (scheduled_by_admin_id, cancelled_by_admin_id)

---

### 39. Provider Specialties

**Table**: `provider_specialties`
**Description**: Centrally managed Provider Specialties list (FR-026 Entity 7a, Screen 5f), consumed by FR-015. Documented from the FR-026 PRD; implementation reconciliation pending.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique specialty identifier (FR-026 `specialty_id`) |
| specialty_name | VARCHAR(100) | NOT NULL | Display name; unique case-insensitive |
| display_order | INTEGER | NOT NULL, DEFAULT 999 | Sort order in FR-015 selectors |
| active | BOOLEAN | NOT NULL, DEFAULT true | Inactive values are hidden from new selection |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- UNIQUE: `specialty_name` (case-insensitive collation)
- INDEX: `active`, `display_order`

**Business Rules (FR-026 v1.11)**:

- Rows are never hard-deleted; at least one row must stay active. Changes require a reason and are audit-logged.
- Seed values: Hair Transplant Surgeon, Dermatologist, Trichologist, Plastic Surgeon, Other (display order 1-5).
- Migration: existing free-text provider specialty values must be mapped to a row before `providers.specialty_id` becomes NOT NULL.

**Relationships**:

- `hasMany` → `Provider`

---

### 40. Provider Account Closure Requests

**Table**: `provider_account_closure_requests`
**Description**: Provider-submitted account-closure requests (FR-032 Entity 5), processed by an admin as an FR-015 deactivation (FR-015 Alternative Flow A7). Documented from the FR-032 and FR-015 PRDs; implementation reconciliation pending.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique closure request identifier |
| provider_id | UUID | FOREIGN KEY, NOT NULL | References providers.id |
| requested_by | UUID | FOREIGN KEY, NOT NULL | References provider_users.id (the provider user who submitted) |
| reason | TEXT | NULLABLE | Optional provider-entered reason |
| status | VARCHAR(255) | NOT NULL, DEFAULT 'pending_admin_review' | `pending_admin_review`, `approved`, `rejected` |
| reviewed_by | UUID | FOREIGN KEY, NULLABLE | References users.id (admin) |
| reviewed_at | TIMESTAMP | NULLABLE | When the admin approved or rejected |
| review_notes | TEXT | NULLABLE | Admin notes; required on rejection (minimum 20 characters) and sent to the provider in FR-020 `provider.closure_rejected` |
| deactivation_event_id | UUID | NULLABLE | FR-015 deactivation status event that applied the request; set when `approved` |
| created_at | TIMESTAMP | AUTO | Request submission timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- UNIQUE (partial): `provider_id` WHERE `status` = 'pending_admin_review'
- INDEX: `provider_id`, `status`

**Business Rules (FR-032 v1.9, FR-015 v1.16)**:

- Submission is never blocked by active bookings or pending payouts; the provider stays `active` until an admin acts.
- Submission emits FR-020 `provider.closure_requested` to admins (mandatory). FR-015 Screen 1's Closure Requested marker and filter read the provider's `pending_admin_review` row; the marker clears when the row becomes `approved` or `rejected`.
- The deactivation that approves a request always notifies the provider (`provider.deactivated`); Notify Provider cannot be cleared, including on a scheduled §38 row.
- Rejection emits FR-020 `provider.closure_rejected` to the provider (mandatory). After a rejection the provider may submit a new request.
- Approval is recorded only when the admin deactivates the provider through FR-015 Screen 4 (immediate or scheduled; a scheduled deactivation uses §38). The request then links to the deactivation status event.
- There is no `deleted` provider status; provider data is retained per FR-023 (minimum 7 years). Requests are never hard-deleted and are audit-logged.

**Relationships**:

- `belongsTo` → `Provider`
- `belongsTo` → `ProviderUser` (requested_by)
- `belongsTo` → `User` (reviewed_by)

---

## Appendix

### Complete Table List

1. users
2. patients
3. providers
4. provider_users
5. provider_team_members
6. provider_documents
7. provider_awards
8. provider_languages
9. provider_media
10. provider_commissions
11. provider_discounts
12. provider_bills
13. provider_resources
14. inquiries
14a. inquiry_date_ranges
15. inquiry_providers
16. medical_histories
17. quotes
18. quote_clinicians
18a. quote_documents
18b. quote_options
18c. quote_option_items
18d. quote_option_date_prices
18e. quote_option_plan_days
18f. quote_versions
18g. quote_audits
18h. acceptance_events
18i. acceptance_supersessions
18j. acceptance_annotations
18k. promotion_applications
18l. promotion_use_reservations
19. treatments
20. packages
21. package_items
21a. package_plan_days
22. treatment_includes
23. treatment_customizes
24. schedules
24a. bookings
25. payments
26. payment_histories
27. installment_payment_plans
28. after_cares
29. after_care_instructions
30. after_care_medications
31. aftercare_resources
32. aftercare_milestones
33. aftercare_milestone_scans
34. aftercare_payments
35. aftercare_questions
36. aftercare_question_answers
37. aftercare_conversations
38. aftercare_conversation_participants
39. aftercare_messages
40. conversations
41. messages
42. reviews
43. affiliates
44. affiliate_discount_codes
45. affiliate_commissions
46. discounts (legacy)
46a. promotion_programs
46b. promotion_codes
47. fixed_discounts
48. locations
49. location_preferences
50. location_preferences_countries (junction)
51. location_starting_prices
52. languages
53. hotels
54. flights
55. passport_details
55a. travel_contexts
56. questionnaires
57. discovery_questions
58. patient_resources
59. patient_consents
60. notification_preferences
61. alerts_notifications
62. workflow_timelines
63. recovery_progress_logs
64. timelines
65. media
66. files
67. information
68. terms_and_conditions
69. banking_details
70. set_commissions
71. roles
72. permissions
73. model_has_roles (junction)
74. model_has_permissions (junction)
75. role_has_permissions (junction)
76. oauth_access_tokens
77. oauth_auth_codes
78. oauth_clients
79. oauth_personal_access_clients
80. oauth_refresh_tokens
81. password_reset_tokens
82. password_reset_tokens_for_all_users
83. personal_access_tokens
84. failed_jobs
85. provider_staff_invitations
86. aftercare_workflows
87. aftercare_workflow_steps
88. instruction_templates
89. medication_templates
90. aftercare_templates
91. aftercare_clinicians
92. treatment_records
92a. treatment_detail_changes
93. analytics_configurations
94. export_report_configurations
95. provider_pending_status_changes
96. provider_specialties
97. provider_account_closure_requests

### ERD Visualization

For a visual Entity Relationship Diagram, use tools like:

- **MySQL Workbench**: Reverse engineer database
- **dbdiagram.io**: Create ERD from schema
- **Laravel ER Diagram Generator**: `composer require beyondcode/laravel-er-diagram-generator`

### Schema Versioning

Schema version tracked via:

- Migration files (timestamp-based)
- `migrations` table records executed migrations
- Git version control for schema changes

### Document Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.1.0 | 2026-10-14 | Vân Tay Media | Aligned with FR-015 v1.9 verification decisions and FR-029 flat-rate commission: provider status without `draft`, payout and commission fields, `featured` auto-clear, retention rule; new §2A Provider Documents; provider-status cancellation fields on `inquiries` and `after_cares`; quote status `cancelled_provider_status` with `cancellation_provenance`; booking commission snapshot (model, value, currency); provider audit rules |
| 1.2.0 | 2026-10-14 | Vân Tay Media | Product Owner decisions: provider commission settings moved from `providers` to a new §2B `provider_commissions` table (FR-029 Entity 6, rate history kept by archiving); flat model renamed `flat_rate` everywhere; added the missing `inquiries.status` column with the documented treatment case statuses |
| 1.3.0 | 2026-10-15 | Vân Tay Media | §2B `provider_commissions` aligned with FR-015 v1.12 and CR-FR029-20261015-01: `pending` status for one scheduled configuration per provider (replace, cancel, and activation rules), partial unique indexes enforcing one active and one pending provider-specific row per provider, and the single-provider split rule |
| 1.4.0 | 2026-10-15 | Vân Tay Media | Aligned with FR-015 v1.13, FR-017 v2.10, and FR-026 v1.11 (CR-FR017-20261015-01, CR-FR026-20261015-01): new §38 `provider_pending_status_changes` (one pending row per provider, cancelled by reactivation); new §39 `provider_specialties` and `providers.specialty_id`; `payments.reconciliation_flag` and `provider_status_event_id`; `cancelled` payment status for stopped installments and plan cancellation on provider-status cancellation |
| 1.5.0 | 2026-10-15 | Vân Tay Media | Aligned with FR-015 v1.14 and FR-032 v1.8 (CR-FR032-20261015-02): `providers.email` unique only among `active` and `suspended` providers (partial index); email-reuse rules for owner (§3) and team (§4) login emails after deactivation, mechanism subject to reconciliation; confirmed no `deleted` provider status; new §40 `provider_account_closure_requests` (one pending request per provider, approved via FR-015 deactivation) |
| 1.6.0 | 2026-10-15 | Vân Tay Media | Aligned with FR-015 v1.15 and FR-009 v1.5 (proposed) (CR-FR009-20261015-02): global provider email identity rule in §3 and §4 (one provider organization per login email across owner accounts, `provider_users`, and pending `provider_staff_invitations`; deactivated providers' emails freed, records archived; enforced by a shared check, mechanism subject to reconciliation); §2 contact-email reuse note now separates contact email from login emails |
| 1.7.0 | 2026-10-15 | Vân Tay Media | Aligned with FR-015 v1.16, FR-003 v2.8, FR-029 v1.10, and FR-032 v1.9 (CR-FR003-20261015-01, CR-FR029-20261015-02, CR-FR032-20261015-03): §2 `providers.password_set` with the distribution eligibility rule (`active` and password set) and index; §2 `activation_token_hash` and `activation_token_expires_at` with the one-valid-token rule (FR-015 REQ-015-011); `provider_languages` reference the FR-021 `languages` catalog; §2B provider-specific rows writable only for `active` or `suspended` providers; §38 closure deactivations must notify the provider; §40 rejection notes required (min 20 chars), closure notification events, Screen 1 marker source, resubmission after rejection |
| 1.8.0 | 2026-10-16 | Vân Tay Media | MTG-002 quote model alignment with FR-004 v3.1, FR-005 v2.5, FR-006 v2.7, FR-007b, FR-008, FR-010, FR-019 v2.2, FR-022 v2.14, FR-024 v1.3, FR-026 v1.12, and FR-029 v1.11 (ESC-1 to ESC-6; S5-1, S5-3, S5-5, S5-6, S5-8, S5-11, FR-024-8, FR-026-4; decisions D4, D6, D6-M, D10, D12, D17, D18, D19, D23, D24, M4, M5, M10, M11, M12, M18): new §7G `acceptance_events` (append-only snapshot with money projections, exchange rate and timestamp, actor type), §7H `quote_versions`, §7I `quote_audits`, §7J `acceptance_supersessions` (causes InquiryCancelled, ProviderFault, ProviderSuspended, ProviderDeactivated), §7K `acceptance_annotations`, §7L `promotion_applications`, §11A `bookings` (hold key, fixed hold, Payment Window Expired, booking total, binding commission snapshot with config ID and scope type), §34A `travel_contexts`, §35A `treatment_detail_changes`, §10A `package_plan_days`; `quotes.version`, `first_sent_at`, `quote_config_version`, `accepted_total`, `terms_acknowledged_at`, `locked_exchange_rate_snapshot`; quote status `confirmed` removed and `rejected` dropped from the enum list; `accepted` → `cancelled_inquiry_cancelled` and `accepted` → `withdrawn` transitions; `cancelled_provider_status` limited to unaccepted quotes; quote commission columns now indicative only; `expiration_hours` copied at first send, not customisable; `quote_option_date_prices.is_accepted` removed and promotion terms snapshot, discount amount, auto-attached flag added; §9 and §10 rewritten to versioned package templates without currency; schedules created at first payment; instalment plan currency and exchange rate; treatment record acceptance identifiers; option tables added to the table list, constraints, and migration order; `passport_details`, `hotels` and `flights` re-keyed from `quote_id` to `travel_context_id` per FR-008 PassportRecord, HotelRecord and FlightRecord, undefined `Itinerary` relationship resolved to the travel context, and FK, unique and migration-order lists updated |
| 1.9.0 | 2026-10-16 | Vân Tay Media | Product Owner Q-series follow-up (Q3, Q6, Q14, Q15, Q17, Q18, Q21, Q29, Q30; Q2 alignment) with FR-006 v2.8, FR-008 v2.7, and FR-010 v2.3 (CR-FR006-20261016-01, CR-FR008-20261016-01, CR-FR010-20261016-01): §7C `quote_option_date_prices.price` CHECK (price > 0); new §7M `promotion_use_reservations` (reserved at send, at most one active reservation per parent quote kept across resent versions, created only when a new version newly qualifies and released when it drops the promotion; released on expiry, withdrawal or not selected; consumed at acceptance); §7L reconciled with §7M: usage-limit lifecycle stated by source (automatic promotion consumed at acceptance and returned to the limit on `Payment Window Expired` or cancellation before first payment, re-taken on revive only if the limit has room; provider-selected and patient-code promotions reserved at acceptance and consumed at first payment), new `use_reservation_id` and `use_returned_at`; §7 `quote_config_version` note that a Default Currency change creates a new Quote Configuration version; §7 `quotes.first_sent_at` confirmed as the column set once at first send and never changed (no edit); §32 `hotels` and §33 `flights` add `copied_from_*_id`, `travel_date_review_required`, and early-departure acknowledgement fields; §34 passport carry-over on provider-fault transfer; §34A note that there is no `itineraries` table (itinerary is a read view); §35A treatment-detail changes blocked while the booking is `accepted`. Q22 and Q23 confirmed with no change. |
| 1.10.0 | 2026-10-18 | Vân Tay Media | Consolidated verification corrections for the MTG-002 quote model (Q15, Q33; D4, D6, D11, M18; no Change Request, system document): §7 `quotes.sent_at` is the latest send time and no longer feeds TTFQ, which ends at `first_sent_at`; quotes removed from the soft-delete list, `quotes.inquiry_id` changed from CASCADE to RESTRICT, and accepted quotes referenced by acceptance records are retained; §5 provider-status note cancels bookings, not cases; §7M release reason `cancelled` added for quotes cancelled before acceptance by inquiry cancellation or provider status change; §7L revive wording uses "taken again" and a rejected revive when the limit has no room; FR-019 promotion programs stored in §25 `discounts` (Q33): `PromotionProgram` references now point to `discounts.id`, new `source` and `program_kind` columns, `discount_code` nullable for programs without a code, `usage_limit` enforced from reservations and applications, `usage_count` marked legacy; §11A hold key follows the booking's current appointment when an admin changes it; §35 `treatment_records` unique per booking and acceptance, `inquiry_id` no longer unique so a provider-fault transfer can create a second record in the same inquiry; migration order lists `treatments` and `packages` before `quotes`; change log rows sorted by version |
| 1.11.0 | 2026-10-18 | Vân Tay Media | Final audit corrections (Q31, Q35 to Q44; f1 F5, F6, F8, F10; f2 F2, F4, F5, F8, F10; f3 F5; f4 F3, F5, F6, F8, F9, F11, F13; no Change Request, system document). Revises the 1.10.0 decision that `discounts` stores promotion programs (Q38 supersedes Q33): new §25A `promotion_programs` and §25B `promotion_codes`, `discounts` marked legacy, and every promotion reference repointed. §5 inquiry `status` aligned to the FR-003 stages with `cancelled_at` and `cancellation_reason`; provider-status fields moved to new §5A `inquiry_providers` with `distributed_at`; new §5B `inquiry_date_ranges`. §7 quotes gain `authored_by_type`, `authored_by_admin_id`, and `replacement_for_acceptance_event_id` for the admin-authored replacement quote; an accepted quote stays accepted when an admin cancels the booking. §7J supersession is inserted once at the replacement acceptance, `InquiryCancelled` cause removed, replacement acceptance NOT NULL and unique. §7M adds `not_applied`, one automatic promotion per quote, and limit-full sends proceed without the promotion. §11A admin-only cancellation from any booking state after acceptance, provider-fault transfer limited to Accepted and Confirmed, deposit rate and instalment settings locked at confirmation, cancellation audit fields. §13 aftercare provider reassignment instead of cancellation for treatment-linked aftercare. §35 treatment status `in_progress`, `completed`, `cancelled` and creation at confirmation; §35A clinic changes until Check In and admin changes at any time from Confirmed. FK, unique, migration order, ENUM and table lists updated; total tables 116. Round-2 additions (Q45 to Q49): a provider fault, suspension, or deactivation on an In Progress booking no longer cancels it automatically; the booking stays `in_progress` with `support_required` and an admin either moves it to Aftercare with aftercare-provider reassignment or cancels it with a reason (§5, §7, §11A). §35 `treatment_records.status` is NOT NULL with default `awaiting_check_in` from creation at confirmation. §13 reassignment sends `aftercare.provider_reassigned` to the patient and the new aftercare provider. §7 and §7L: no automatic promotion or reservation on an admin-authored replacement quote, and an unaccepted replacement quote expires normally while the inquiry stays support-required |

---

**Document Status**: ✅ Complete  
**Next Steps**: Use this schema as reference for development and API design  
**Maintained By**: Database/Backend Team  
**Review Cycle**: Quarterly or upon significant schema changes
