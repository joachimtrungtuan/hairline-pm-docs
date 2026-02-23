# Hairline Platform - Database Schema

**Version**: 1.0.0  
**Document Type**: System-Level Data Schema  
**Created**: 2025-10-23  
**Status**: Active  
**Last Updated**: 2025-10-23

---

## Executive Summary

This document provides a comprehensive overview of the Hairline Platform database schema, including all entities, relationships, constraints, and data types. The schema is implemented using **MySQL 8.0+** and follows Laravel migration conventions.

### Schema Overview

- **Total Tables**: 97 tables (6 new aftercare-related tables added)
- **Primary Key Type**: UUID (string) for user-facing entities, auto-increment for system tables
- **Character Set**: utf8mb4_unicode_ci (supports emoji and international characters)
- **Storage Engine**: InnoDB (supports foreign keys and transactions)
- **Soft Deletes**: Enabled for critical entities (patients, providers, quotes, treatments)
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
| provider_name | VARCHAR(255) | NOT NULL | Clinic/Hospital name |
| email | VARCHAR(255) | NOT NULL | Primary contact email |
| phone_number | VARCHAR(255) | NULLABLE | Contact phone number |
| profile_image | VARCHAR(255) | NULLABLE | S3 path to logo/image |
| provider_bio | TEXT | NULLABLE | Provider description and credentials |
| city | VARCHAR(255) | NOT NULL | City where provider is located |
| country | VARCHAR(255) | NOT NULL | Country where provider is located |
| status | VARCHAR(255) | DEFAULT 'active' | Provider account status (active, inactive, suspended) |
| timezone | VARCHAR(255) | NULLABLE | Provider's timezone (e.g., Europe/Istanbul) |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |
| deleted_at | TIMESTAMP | NULLABLE | Soft delete timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `user_id`, `status`, `country`, `city`

**Relationships**:

- `belongsTo` → `User`
- `hasMany` → `ProviderUser` (team members)
- `hasMany` → `Quote`
- `hasMany` → `Treatment`
- `hasMany` → `ProviderDocument`
- `hasMany` → `ProviderAward`
- `hasMany` → `ProviderLanguage`
- `hasMany` → `ProviderMedia`
- `hasMany` → `Review`

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

**Relationships**:

- `belongsTo` → `Provider`
- `belongsToMany` → `Role` (via Spatie permissions)

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
| scan_url | VARCHAR(255) | NOT NULL | S3 path to 3D scan or photos |
| treatment_schedule | JSON | NOT NULL | Preferred treatment dates (range) |
| problem_details | TEXT | NOT NULL | Detailed description of concern |
| nature_of_concern | VARCHAR(255) | NULLABLE | Type of hair loss (genetic, alopecia, etc.) |
| duration_of_concern | VARCHAR(255) | NULLABLE | How long has problem existed |
| previous_treatments | VARCHAR(255) | NULLABLE | Past treatments attempted |
| symptom_severity | VARCHAR(255) | NULLABLE | Severity level (mild, moderate, severe) |
| lifestyle_factors | VARCHAR(255) | NULLABLE | Relevant lifestyle information |
| additional_files | VARCHAR(255) | NULLABLE | Additional photos/documents |
| additional_notes | VARCHAR(255) | NULLABLE | Extra notes from patient |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `patient_id`, `created_at`

**Relationships**:

- `belongsTo` → `Patient`
- `hasMany` → `InquiryProvider` (junction table)
- `hasMany` → `Quote`
- `hasOne` → `MedicalHistory`
- `hasMany` → `WorkflowTimeline`

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
| treatment_id | UUID | FOREIGN KEY, NOT NULL | References treatments.id (package template) |
| package_id | UUID | FOREIGN KEY, NULLABLE | References packages.id |
| treatment_date | JSON | NOT NULL | Proposed treatment dates |
| discount_id | UUID | FOREIGN KEY, NULLABLE | References discounts.id |
| commission | INTEGER | NOT NULL | Platform commission percentage |
| quote_amount | DECIMAL(10,2) | NOT NULL | Total quote amount |
| currency | VARCHAR(255) | NOT NULL | Currency code (USD, EUR, GBP, TRY, etc.) |
| note | TEXT | NULLABLE | Additional notes from provider |
| status | VARCHAR(255) | NOT NULL | Quote status (inquiry, quote, accepted, confirmed, inprogress, aftercare, completed, rejected, cancelled) |
| expires_at | TIMESTAMP | NULLABLE | Quote expiration date |
| expiration_hours | INTEGER | DEFAULT 48 | Hours until quote expires (customizable, default 48) |
| auto_accepted | BOOLEAN | DEFAULT false | Whether quote was auto-accepted with pre-scheduled appointment |
| appointment_pre_scheduled | BOOLEAN | DEFAULT false | Whether provider pre-scheduled appointment in quote |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `inquiry_id`, `provider_id`, `status`, `created_at`
- COMPOSITE: `(provider_id, status)`, `(inquiry_id, provider_id)`

**Relationships**:

- `belongsTo` → `Inquiry`
- `belongsTo` → `Provider`
- `belongsTo` → `Treatment`
- `belongsTo` → `Package`
- `belongsTo` → `Discount`
- `hasOne` → `Schedule`
- `hasOne` → `Treatment` (actual treatment execution record)
- `hasMany` → `Payment`
- `hasMany` → `Review`

**Status Values**:

- `inquiry`: Patient inquiry submitted, waiting for provider quotes
- `quote`: Quote submitted by provider, waiting for patient response
- `accepted`: Patient accepted quote and appointment scheduled (merged accepted + scheduled)
- `confirmed`: Payment completed, booking confirmed
- `inprogress`: Patient arrives at clinic, treatment in progress (provider can update real-time progress)
- `aftercare`: Treatment completed, in aftercare phase (6-12 months recovery)
- `completed`: Final review and rating submitted by patient
- `rejected`: Patient rejected quote
- `cancelled`: Quote/booking cancelled

**Status Triggers**:

- `inquiry` → `quote`: Provider submits quote
- `quote` → `accepted`: Patient accepts quote (auto-schedules appointment)
- `accepted` → `confirmed`: Patient completes payment
- `confirmed` → `inprogress`: Patient arrives at clinic
- `inprogress` → `aftercare`: Treatment completed
- `aftercare` → `completed`: Final review submitted

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

---

### 9. Packages (Provider-Created Add-Ons)

**Table**: `packages`  
**Description**: Optional add-ons created by each provider - supplements the treatment (hotels, transport, medications, PRP, etc.)

**Purpose**: Allows providers to differentiate their offerings - each provider has their own package list

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique package identifier |
| provider_id | UUID | FOREIGN KEY, NOT NULL | References providers.id (owner of package) |
| package_name | VARCHAR(255) | NOT NULL | Package name (e.g., "5-Star Hotel Package") |
| package_price | DECIMAL(10,2) | NOT NULL | Package price |
| currency | VARCHAR(255) | NOT NULL | Currency code |
| package_description | TEXT | NULLABLE | Package description |
| package_category | VARCHAR(255) | NOT NULL | Category: hotel, transport, flight, medication, prp_therapy, consultation |
| status | VARCHAR(255) | DEFAULT 'active' | Package status (active, inactive) |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record creation timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `provider_id`, `package_category`, `status`

**Relationships**:

- `belongsTo` → `Provider` (package owner)
- `hasMany` → `PackageItem` (items included in package)
- `belongsToMany` → `Quote` (via quote_packages junction)

**Business Rules**:

- Each provider creates their own packages
- Packages are optional (not required for quote)
- Providers can have different packages (unlike treatments which are standardized)
- Package categories: hotel, transport, flight_assistance, medications, prp_therapy, extended_consultation

---

### 10. Package Items

**Table**: `package_items`  
**Description**: Individual items included in a package

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique item identifier |
| package_id | UUID | FOREIGN KEY, NOT NULL | References packages.id |
| item_name | VARCHAR(255) | NOT NULL | Item name (e.g., "Grafts", "Medications") |
| item_value | VARCHAR(255) | NOT NULL | Item value/quantity |
| item_price | DECIMAL(10,2) | NOT NULL | Item price |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `package_id`

**Relationships**:

- `belongsTo` → `Package`

---

### 11. Schedules

**Table**: `schedules`  
**Description**: Appointment scheduling details

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique schedule identifier |
| quote_id | UUID | FOREIGN KEY, NOT NULL | References quotes.id |
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
| payment_status | VARCHAR(255) | NOT NULL | Status (pending, completed, failed, refunded) |
| stripe_payment_intent_id | VARCHAR(255) | NULLABLE | Stripe PaymentIntent ID |
| transaction_id | VARCHAR(255) | NULLABLE | External transaction reference |
| metadata | JSON | NULLABLE | Additional payment metadata |
| installment_plan_id | UUID | FOREIGN KEY, NULLABLE | References installment_plans.id |
| installment_number | INTEGER | NULLABLE | Current installment number (e.g., 1 of 5) |
| total_installments | INTEGER | NULLABLE | Total number of installments in plan |
| is_installment | BOOLEAN | DEFAULT false | Whether this is part of an installment plan |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `quote_id`, `patient_id`, `provider_id`, `payment_status`

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
| status | VARCHAR(255) | DEFAULT 'active' | Aftercare status (active, completed, suspended) |
| pricing_model | VARCHAR(255) | NULLABLE | For standalone: fixed, monthly_subscription |
| total_price | DECIMAL(10,2) | NULLABLE | For standalone: total price |
| currency | VARCHAR(3) | NULLABLE | For standalone: currency code |
| duration_months | INTEGER | NULLABLE | For standalone: duration (6, 12 months) |
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `quote_id`, `patient_id`, `provider_id`, `aftercare_type`, `status`

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
| scan_frequency_days | INTEGER | NULLABLE | How often to request 3D scan (1=daily, 5=every 5 days, 7=weekly) |
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
- `hasMany` → `AftercareMilestoneScan` (3D scans for this milestone)
- `hasMany` → `AftercareQuestionnaireResponse` (questionnaire responses)

---

### 17. Aftercare Milestone Scans

**Table**: `aftercare_milestone_scans`  
**Description**: 3D scans and photos uploaded at recovery milestones

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique scan identifier |
| aftercare_milestone_id | UUID | FOREIGN KEY, NOT NULL | References aftercare_milestones.id |
| scan_url | VARCHAR(255) | NOT NULL | S3 path to 3D scan or photo |
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

### 25. Discounts

**Table**: `discounts`  
**Description**: Platform-wide and provider-specific discount codes

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique discount identifier |
| discount_code | VARCHAR(255) | UNIQUE, NOT NULL | Discount code |
| discount_type | ENUM | NOT NULL | Type (percentage, fixed) |
| discount_value | DECIMAL(10,2) | NOT NULL | Discount amount/percentage |
| provider_id | UUID | FOREIGN KEY, NULLABLE | If provider-specific, references providers.id |
| usage_limit | INTEGER | NULLABLE | Maximum uses |
| usage_count | INTEGER | DEFAULT 0 | Current usage count |
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
  - `inquiries.patient_id` → `patients.id` (CASCADE)
  - `quotes.inquiry_id` → `inquiries.id` (CASCADE)
  - `messages.conversation_id` → `conversations.id` (CASCADE)

- **SET NULL**: Child records set to NULL when parent is deleted
  - `quotes.discount_id` → `discounts.id` (SET NULL)
  - `quotes.provider_id` → `providers.id` (SET NULL for soft-deleted providers)

- **RESTRICT**: Prevent parent deletion if children exist
  - `payments.quote_id` → `quotes.id` (RESTRICT - cannot delete quote with payments)

### Unique Constraints

- **Patients**: `email`, `username`, `patient_code`
- **Providers**: `email` (per provider)
- **Provider Users**: `email`
- **Users**: `email`, `username`
- **Affiliates**: `email`
- **Discount Codes**: `code`
- **Affiliate Discount Codes**: `code`

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
  - Quote status: `quote`, `accepted`, `rejected`, etc.
  - Payment status: `pending`, `completed`, `failed`, `refunded`
  - Affiliate status: `draft`, `active`, `inactive`, `suspended`

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
   - `inquiries`, `medical_histories`, `quotes`, `treatments`, `packages`

6. **Payments & Scheduling** (2024-03+)
   - `payments`, `schedules`, `after_cares`

7. **Communication & Reviews** (2024-07+)
   - `conversations`, `messages`, `reviews`

8. **Recent Additions** (2025)
   - `affiliates`, `locations`, `provider_team_members`

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
| total_amount | DECIMAL(10,2) | NOT NULL | Total amount to be paid |
| installment_amount | DECIMAL(10,2) | NOT NULL | Amount per installment |
| number_of_installments | INTEGER | NOT NULL | Total installments (2-9) |
| completed_installments | INTEGER | DEFAULT 0 | Number of completed payments |
| payment_frequency | VARCHAR(255) | DEFAULT 'monthly' | Frequency (weekly, monthly) |
| first_payment_date | DATE | NOT NULL | Date of first installment |
| final_payment_date | DATE | NOT NULL | Date of last installment (must be 30 days before procedure) |
| status | VARCHAR(255) | DEFAULT 'active' | Status (active, completed, cancelled, defaulted) |
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
**Description**: Hotel booking details entered by provider (Path A) or patient (Path B) for a confirmed appointment. One record per appointment in MVP. Immutable after submission; admin corrections create a new versioned record.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique hotel record identifier |
| quote_id | UUID | FOREIGN KEY, NOT NULL | References quotes.id (appointment anchor) |
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
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `quote_id`, `submitted_by_id`, `version`

**Relationships**:

- `belongsTo` → `Quote`
- `belongsTo` → `Itinerary`

**Business Rules**:

- Locked immediately after submission. No edits by patient or provider post-submission.
- Admin corrections write a new version (version + 1) and set `superseded_by` on the old record.
- One active hotel record per appointment in MVP.

---

### 33. Flights (Travel Records — Flight Legs)

**Table**: `flights`
**Description**: Flight leg details submitted by patient (Path B) or entered by provider (Path A). Up to 2 records per appointment (outbound + return). Immutable after submission.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique flight record identifier |
| quote_id | UUID | FOREIGN KEY, NOT NULL | References quotes.id (appointment anchor) |
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
| created_at | TIMESTAMP | AUTO | Record creation timestamp |
| updated_at | TIMESTAMP | AUTO | Record update timestamp |

**Indexes**:

- PRIMARY: `id`
- INDEX: `quote_id`, `leg_type`, `submitted_by_id`
- UNIQUE: `quote_id`, `leg_type`, `version` (one active record per leg per appointment)

**Relationships**:

- `belongsTo` → `Quote`
- `belongsTo` → `Itinerary`

**Business Rules**:

- Maximum 2 active flight records per appointment (one per leg_type).
- `total_price` is excluded; cost captured at package/quote level (FR-004/FR-007).
- Locked immediately after submission.

---

### 34. Passport Details

**Table**: `passport_details`
**Description**: Patient passport data captured for Path A appointments (provider-booked travel). Encrypted at rest. Immutable after submission. Not captured in Path B.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique passport record identifier |
| quote_id | UUID | FOREIGN KEY, NOT NULL | References quotes.id |
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
- INDEX: `quote_id`, `patient_id`, `status`

**Relationships**:

- `belongsTo` → `Quote`
- `belongsTo` → `Patient`

**Business Rules**:

- `passport_number` and `passport_image` encrypted at rest (AES-256). Access restricted to submitting patient, assigned provider, and admin.
- Displayed masked (`A1234****`) to patient; shown in full to assigned provider and admin only.
- Locked immediately after submission. Admin corrections create a new versioned record.
- Retained for 7 years (medical data retention per constitution). Audit log entries retained for 10 years.

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
15. inquiry_providers (junction)
16. medical_histories
17. quotes
18. quote_clinicians
19. treatments
20. packages
21. package_items
22. treatment_includes
23. treatment_customizes
24. schedules
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
46. discounts
47. fixed_discounts
48. locations
49. location_preferences
50. location_preferences_countries (junction)
51. location_starting_prices
52. languages
53. hotels
54. flights
55. passport_details
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

---

**Document Status**: ✅ Complete  
**Next Steps**: Use this schema as reference for development and API design  
**Maintained By**: Database/Backend Team  
**Review Cycle**: Quarterly or upon significant schema changes
