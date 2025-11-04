# Inquiry Submission & Distribution Module - Product Requirements Document

**Module**: P-02: Quote Request & Management | PR-02: Inquiry & Quote Management | A-01: Patient Management & Oversight  
**Feature Branch**: `fr003-inquiry-submission`  
**Created**: 2025-10-23  
**Status**: ✅ Verified & Approved  
**Source**: FR-003 from system-prd.md

## Executive Summary

The Inquiry Submission & Distribution module enables patients to submit comprehensive treatment requests through the mobile app, which are then automatically distributed to relevant providers based on location and availability. The module supports multi-country selection, detailed medical questionnaires, 3D head scanning, and comprehensive inquiry management across all platform tenants.

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-02)**: Quote Request & Management
- **Provider Platform (PR-02)**: Inquiry & Quote Management  
- **Admin Platform (A-01)**: Patient Management & Oversight

### Multi-Tenant Breakdown

**Patient Platform (P-02)**:

- Create and manage inquiries on mobile (service selection, destinations, medical questionnaire, media upload, date ranges)
- Resume drafts; view inquiry dashboard and status timeline
- Review anonymized provider responses (quotes handled by FR-004)

**Provider Platform (PR-02)**:

- View distributed inquiries with anonymized patient info and medical alerts
- Review inquiry details including 3D scans and questionnaire
- Manage inquiry status prior to quote creation (quote creation in FR-004)

**Admin Platform (A-01)**:

- Global oversight of all inquiries across lifecycle stages
- Edit/override inquiry details; reassign providers; soft-delete with audit
- Configure distribution rules and expirations aligned with system PRD

**Shared Services (S-XX)**:

- Notification service for distribution and status changes
- Media/scanning service for secure storage and retrieval of 3D scans
- Audit logging, anonymization and soft delete utilities

### Communication Structure

**In Scope**:

- Patient → System: Inquiry submission with comprehensive data
- System → Provider: Automatic inquiry distribution and notifications
- Provider → System: Inquiry management prior to quote (quotes in FR-004)
- Admin → All Parties: Oversight, edit, and management actions
- Structured Updates: System-generated notifications and status updates

**Out of Scope**:

- Direct patient-provider chat (moved to backlog; future FR-012)

### Entry Points

1. **Patient-Initiated**: Primary flow through mobile app inquiry creation
2. **Admin-Managed**: Direct inquiry creation and management by admin team
3. **Provider-Viewed**: Provider access to distributed inquiries

## Business Workflows

### Workflow 1: Patient Inquiry Creation (Primary Flow)

**Actors**: Patient, System, Medical Questionnaire Engine, 3D Scan Service

**Main Flow**:

1. **Service Selection**
   - Patient opens mobile app and selects "Get a Hair Transplant"
   - Patient chooses treatment type (Hair, Beard, Both)
   - System validates patient eligibility

2. **Destination Selection**
   - Patient selects preferred countries/locations (max 10 countries)
   - System displays starting prices for each location
   - Patient can select multiple destinations
   - System suggests nearest countries to patient's location first

3. **Detailed Information Collection**
   - Patient provides detailed hair concerns:
     - Nature of concern (text field)
     - Duration of concern (dropdown enum)
     - Previous treatments (text field)
     - Symptom severity (1-10 slider)
     - Lifestyle factors (optional text)
     - Additional notes (optional text)
   - Patient uploads visual evidence (max 5 photos/videos)
     - Photos: JPG/PNG ≤ 2MB each
     - Videos: MP4 ≤ 30s, ≤ 20MB each

4. **3D Head Scan Capture**
   - Patient receives scan instructions
   - Patient captures 3D head scan using mobile camera
   - System validates scan quality
   - Scan data stored for provider review

5. **Treatment Date Selection**
   - Patient selects preferred treatment dates (max 10 date ranges)
   - Date ranges can be up to 2 years in the future
   - Patient can select multiple non-overlapping ranges
   - System validates date availability

6. **Medical Questionnaire Completion**
   - Patient completes comprehensive medical questionnaire
   - Questions cover: allergies, medications, chronic diseases, previous surgeries, etc.
   - Each question requires Yes/No answer
   - Detailed explanation required for "Yes" answers
   - System applies 3-tier medical alert system:
     - Critical alerts (red - high risk conditions)
     - Standard alerts (yellow/amber - moderate concerns)  
     - No alerts (green - no medical concerns)

7. **Inquiry Review & Submission**
   - Patient reviews complete inquiry summary
   - Patient confirms all information accuracy
   - Patient selects preferred providers (max 5 providers)
   - System suggests providers based on positive reviews and admin curation
   - Patient submits inquiry to system
   - System generates unique inquiry ID (HPID format)

**Alternative Flows**:

- **A1**: Patient abandons inquiry mid-process
  - System saves draft automatically
  - Patient can resume from last completed step
  - Draft expires after 7 days of inactivity

- **A2**: Patient has existing incomplete inquiry
  - System shows "continue with your request" option
  - Patient can resume from last completed step
  - Patient can modify existing inquiry if still in "Inquiry" stage
  - System displays inquiry status as "incomplete" or "pending"

- **A3**: Medical questionnaire reveals critical conditions
  - System flags inquiry with critical medical alerts (red indicators)
  - Providers are alerted to high-risk conditions
  - Admin can review and provide guidance to providers
  - **Note**: Medical alerts are for provider awareness, not patient rejection

### Workflow 2: Inquiry Distribution (System Flow)

**Actors**: System, Providers, Admin

**Main Flow**:

1. **Inquiry Processing**
   - System receives completed patient inquiry
   - System validates all required data completeness
   - System generates inquiry ID and timestamps

2. **Provider Matching**
   - System identifies providers in patient-selected countries
   - System includes providers explicitly selected by patient
   - System creates provider-specific inquiry views
   - **Note**: Provider capacity management will be handled in a separate FR

3. **Inquiry Distribution**
   - System distributes inquiry to all matching providers
   - Providers receive notification of new inquiry
   - Inquiry appears in provider dashboard
   - System tracks distribution timestamps

4. **Provider Access Control**
   - Providers see anonymized patient information until quote acceptance
   - Patient names partially masked (e.g., "John D*****")
   - Contact details hidden until payment confirmation
   - Medical alerts prominently displayed

**Alternative Flows**:

- **B1**: No providers available in selected countries
  - System notifies admin of unmatched inquiry
  - Admin can manually assign providers
  - Patient notified of potential delay

- **B2**: Provider capacity exceeded
  - **Note**: Provider capacity management will be handled in a separate FR

### Workflow 3: Provider Inquiry Management (Provider Flow)

**Actors**: Provider, System, Admin

**Main Flow**:

1. **Inquiry Review**
   - Provider accesses inquiry list in dashboard
   - Provider views inquiry details with medical alerts
   - Provider reviews patient 3D scan and medical questionnaire
   - Provider assesses treatment feasibility

2. **Inquiry Status Management**
   - Provider can review inquiry details
   - System tracks provider response time
   - **Note**: Quote creation process handled in FR-004

**Alternative Flows**:

- **C1**: Provider cannot accommodate patient dates
  - Provider can decline inquiry with reason
  - System logs provider response
  - Provider cannot suggest alternative dates (handled in FR-004)

- **C2**: Provider needs additional information
  - Provider can request clarification through admin
  - Admin facilitates communication
  - Inquiry remains in "Inquiry" stage until resolved

### Workflow 4: Admin Inquiry Management (Admin Flow)

**Actors**: Admin, System, Providers, Patients

**Main Flow**:

1. **Inquiry Oversight**
   - Admin views all inquiries across all stages
   - Admin monitors inquiry distribution and response rates
   - Admin tracks provider performance metrics
   - Admin identifies system-wide issues

2. **Inquiry Management**
   - Admin can edit inquiry details (with caution warnings)
   - Admin can reassign inquiries to different providers
   - Admin can override quote expiration periods
   - Admin can escalate urgent cases

3. **System Configuration**
   - Admin manages medical questionnaire content
   - Admin configures country/location lists
   - Admin sets inquiry expiration rules
   - Admin manages provider availability settings

**Alternative Flows**:

- **D1**: Admin needs to delete inquiry
  - Admin performs soft delete (archival)
  - System logs deletion with reason
  - Patient notified of inquiry cancellation

- **D2**: Inquiry requires manual intervention
  - Admin identifies problematic inquiries
  - Admin contacts patient or provider directly
  - Admin resolves issues and updates inquiry status

## Screen Specifications

### Patient Platform Screens

#### Screen 1: Service Selection

**Purpose**: Patient selects desired hair transplant service

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Service Option | select (single) | Yes | Primary service selection | Must select one |
| Treatment Type | checkbox (multi) | Yes | Hair/Beard/Both | At least one selected |

**Notes**:

- Service Options:
  - "Get a Hair Transplant" (primary option)
  - "Monitor Hair Loss" (secondary - different workflow)
  - "Aftercare: Monitor Transplant Progress" (secondary - different workflow)
  - "Aftercare for Transplant" (secondary - different workflow)
- Treatment Type Selection:
  - Hair (checkbox)
  - Beard (checkbox)
  - Both (checkbox)

**Business Rules**:

- Patient must select at least one treatment type
- Primary focus on "Get a Hair Transplant" option
- Other services are secondary features

#### Screen 2: Destination Selection

**Purpose**: Patient selects preferred treatment locations

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Countries | multiselect | Yes | Up to 10 preferred countries | Max 10; ordered by proximity |
| Price Display | derived | No | Starting price per country | Fallback currency support |

**Notes**:

- Country List:
  - Show country name with starting price
  - Order by proximity to patient location
  - Support fallback currency/pricing display
- Price Display:
  - Starting price per country
  - Currency based on patient location
  - Price range indicators

**Business Rules**:

- Maximum 10 countries selectable
- Countries ordered by proximity to patient location
- Starting prices displayed for transparency
- Fallback pricing for unsupported currencies

#### Screen 3: Detailed Information Form

**Purpose**: Patient provides comprehensive hair concern details

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Nature of concern | text | Yes | Patient description | Max length; not empty |
| Duration | select | Yes | Duration enum | Must select one |
| Previous treatments | text | Yes | Prior treatments | Max length |
| Symptom severity | slider (1-10) | Yes | Severity index | Integer 1-10 |
| Lifestyle factors | text | No | Optional context | Max length |
| Additional notes | text | No | Optional notes | Max length |
| Photos | file (image) | No | Up to 5 images | JPG/PNG ≤ 2MB each; total ≤ 5 |
| Videos | file (video) | No | Up to 5 videos | MP4 ≤ 30s, ≤ 20MB each |

**Notes**:

- Visual Evidence:
  - Photo upload: max 5 files (JPG/PNG ≤ 2MB each)
  - Video upload: max 5 files (MP4 ≤ 30s, ≤ 20MB each)
  - Enforce file size/format and total file count

**Business Rules**:

- All required fields must be completed
- Visual evidence limited to 5 files total
- Photos: JPG/PNG ≤ 2MB each
- Videos: MP4 ≤ 30s, ≤ 20MB each
- Text fields have character limits

#### Screen 4: 3D Head Scan Capture

**Purpose**: Patient captures 3D head scan for provider assessment

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| 3D Scan | capture | Yes | 3D head scan data | Quality threshold must pass |
| Quality Indicators | derived | Yes | Real-time quality feedback | Retake if below threshold |

**Notes**:

- Scan Instructions:
  - Visual guidance for positioning
  - Quality indicators and feedback
  - Retake options available
- Scan Data:
  - 3D model capture
  - Quality validation and storage confirmation

**Business Rules**:

- Scan must meet minimum quality threshold
- Patient can retake scan if quality poor
- Scan data encrypted and stored securely
- Scan accessible to providers for assessment

#### Screen 5: Treatment Date Selection

**Purpose**: Patient selects preferred treatment dates

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Date Ranges | date range (multi) | Yes | Up to 10 ranges | Max 10; non-overlapping; ≤ 2 years out |

**Notes**:

- Date Range Selection:
  - Multiple pickers (max 10)
  - Calendar with availability
  - Non-overlapping validation
- Date Constraints:
  - Max 2 years in future
  - Min 30 days from inquiry date
  - Consider provider availability

**Business Rules**:

- Maximum 10 date ranges selectable
- Date ranges cannot overlap
- Dates limited to 2 years in future
- System validates provider availability

#### Screen 6: Medical Questionnaire

**Purpose**: Patient completes comprehensive medical history assessment

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Question | enum | Yes | Medical question item | Must answer Yes/No |
| Answer | boolean | Yes | Yes/No | Required |
| Details | text | Cond. | Required if Answer = Yes | Non-empty when required |
| Alert Level | derived | No | Critical/Standard/None | Derived from rules |

**Notes**:

- Question List:
  - Allergies to medications (Yes/No + details)
  - Other allergies (Yes/No + details)
  - Respiratory conditions (Yes/No + details)
  - Cardiovascular disease (Yes/No + details)
  - Hypertension (Yes/No + details)
  - Diabetes (Yes/No + details)
  - Implanted medical devices (Yes/No + details)
  - Hepatitis B/C (Yes/No + details)
  - HIV/AIDS (Yes/No + details)
  - Arthritis (Yes/No + details)
  - Neurological disorders (Yes/No + details)
  - Other medical conditions (Yes/No + details)
  - Bleeding disorders (Yes/No + details)
  - Kidney disease (Yes/No + details)
  - Cancer history (Yes/No + details)
  - Digestive diseases (Yes/No + details)
  - Mental health disorders (Yes/No + details)
  - Blood clots/DVT (Yes/No + details)
  - Previous surgeries (Yes/No + details)
  - Pregnancy status (Yes/No + details)
  - Regular medications (Yes/No + details)
- Alert System:
  - Critical (red)
  - Standard (amber)
  - None (green)

**Business Rules**:

- All questions require Yes/No answers
- Detailed explanations required for "Yes" answers
- Medical alerts generated automatically
- Questionnaire managed by admin (not hard-coded)

#### Screen 7: Inquiry Summary & Submission

**Purpose**: Patient reviews complete inquiry before submission

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Section Summary | group | Yes | Read-only summary of prior steps | Must reflect latest data |
| Terms Acceptance | checkbox | Yes | Accept T&C before submission | Required to submit |

**Notes**:

- Summary includes: treatment type, countries with prices, concern details, media, 3D scan, date ranges, questionnaire summary
- Submission Controls: per-section Edit, Submit button, T&C acceptance

**Business Rules**:

- Patient must review all sections
- Patient can edit any section before submission
- Terms and conditions must be accepted
- Submission generates unique inquiry ID

#### Screen 8: Inquiry Dashboard (Post-Submission)

**Purpose**: Patient views submitted inquiry status and details

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Current Stage | badge | Yes | Inquiry stage (Inquiry/Quoted/Accepted/...) | Valid lifecycle value |
| Timeline | timeline | Yes | Chronological status changes | Timestamps present |
| Responses Count | number | Yes | Number of provider responses | Non-negative integer |
| Inquiry Summary | group | Yes | Read-only inquiry info | Complete and consistent |
| Quotes Received | list | No | Provider quotes (from FR-004) | Read-only links |
| Deadlines | datetime | Yes | Response/expiry deadlines | Future or past allowed |
| Next Actions | actions | Yes | Available user actions | Based on stage/permissions |

**Notes**:

- Dashboard shows: full inquiry summary, provider responses, deadlines, and context-aware next actions

**Business Rules**:

- Patient can only have one active inquiry at a time
- Patient can modify inquiry if still in "Inquiry" stage
- Patient receives notifications for status changes
- Inquiry data persists for 7 years minimum

### Provider Platform Screens

#### Screen 9: Inquiry List Dashboard

**Purpose**: Provider views all distributed inquiries

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Patient ID | column | Yes | HPID + YY + MM + 4-digit sequence | Sortable; searchable |
| Patient Name | column | Yes | Partially masked name | Mask until acceptance |
| Age | column | No | Patient age | Number; sortable |
| Problem/Concern | column | No | Primary concern enum | Filterable |
| Requested Date Ranges | column | Yes | Primary + tooltip for others | Non-overlap; tooltip expansion |
| Location | column | No | Patient country | Filterable |
| Medical Alerts | column | Yes | Color-coded chips | Critical/Standard/None |
| Inquiry Date | column | Yes | Created timestamp | Relative formatting rules |
| Action | column | Yes | View/Create Quote buttons | State-aware actions |
| Search | control | No | Keyword search (ID, Name) | Debounced; case-insensitive |
| Filters | control | No | Age range, Concern, Date range, Alerts, Location | Valid ranges/enums |

**Notes**:

- Requested Date Ranges: primary displayed; all ranges via tooltip
- Patient Name: masked until acceptance
- Time Display: relative for recent; formatted for older
- Empty States: Loading, Error, No permission

**Business Rules**:

- Only shows inquiries for provider's countries OR explicitly selected by patient
- Patient names partially masked until quote acceptance
- Medical alerts prominently displayed with color coding
- Inquiry expiration configurable by admin
- Date ranges display primary range with tooltip for additional ranges
- Time display: relative for recent ("X minutes ago"), specific for older ("Sep 22, 2025")
- Empty states: Loading, Error, No permission

#### Screen 10: Inquiry Detailed View

**Purpose**: Provider reviews comprehensive inquiry details

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Inquiry ID | text | Yes | Unique ID and current stage | Read-only |
| Timestamps | group | Yes | Created/updated/activity times | ISO 8601 |
| Patient (masked) | group | Yes | Partially masked identity | Reveal post-acceptance |
| Countries | list | Yes | Selected treatment countries | Non-empty |
| Problem Details | group | Yes | Concern text, duration, previous treatments | Complete |
| Media | gallery | No | Photos/videos previews | File constraints enforced |
| 3D Scan | viewer | No | Special viewer for 3D scan | Available if captured |
| Date Ranges | list | Yes | All selected date ranges | Non-overlapping |
| Medical Questionnaire | group | Yes | Full Q&A responses | Completed |
| Medical Alerts | chips | Yes | Tiered alert indicators | Critical/Standard/None |

**Notes**:

- Inquiry Metadata:
  - Inquiry ID (HPID + YY + MM + 4-digit sequence)
  - Current stage (Inquiry/Quoted/Accepted/...)
  - Created at, Updated at, Last activity timestamps (ISO 8601)
- Patient (Masked):
  - Display name: First name + last initial + asterisks (e.g., "John D*****")
  - Age, Gender, Country (contact details masked until payment)
  - Anonymized patient identifier everywhere except admin
- Countries:
  - Full list of selected treatment countries (ISO country + display name)
  - Primary country highlighted; remaining listed in order selected
- Problem Details:
  - Nature of concern (required)
  - Duration (enum)
  - Previous treatments (required)
  - Symptom severity (1–10)
  - Lifestyle factors (optional)
  - Additional notes (optional)
- Media:
  - Photos (JPG/PNG ≤ 2MB each, max 5): show thumbnails with modal preview
  - Videos (MP4 ≤ 30s, ≤ 20MB each, max 5): show poster frame with player
  - Validation messages for any file policy violations
- 3D Scan:
  - Special viewer control (orbit/zoom)
  - Quality score and capture metadata if available
  - Retake indicator if replaced after initial capture
- Date Ranges:
  - Display all selected ranges, non-overlapping
  - Primary range shown first; additional ranges listed below
  - Server-side validation notes for overlaps and max count (10)
- Medical Questionnaire:
  - Full Q&A list (Yes/No + required details for Yes)
  - Derived medical alerts: Critical (red), Standard (amber), None (green)
  - Link to audit trail of questionnaire version used
- Timeline:
  - Creation, distribution to providers, provider views, status changes
  - Sorted descending by time with relative and absolute timestamps

**Business Rules**:

- Full patient details visible only after quote acceptance
- Medical alerts color-coded by severity
- 3D scan requires special viewer
- All data editable by admin
- Provider can review inquiry details
- **Note**: Quote creation functionality handled in FR-004

### Admin Platform Screens

#### Screen 12: Hairline Overview Dashboard

**Purpose**: Admin monitors all inquiries across all stages

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Patient ID | column | Yes | HPID + YY + MM + 4-digit sequence | Sortable; searchable |
| Full Patient Name | column | Yes | Unmasked name | Admin only |
| Age | column | No | Patient age | Number; sortable |
| Problem/Concern | column | No | Primary concern enum | Filterable |
| Requested Date Ranges | column | Yes | Primary + tooltip for others | Non-overlap; tooltip expansion |
| Location | column | No | Patient country | Filterable |
| Medical Alerts | column | Yes | Color-coded chips | Critical/Standard/None |
| Inquiry Date | column | Yes | Created timestamp | Relative date logic |
| Current Status | column | Yes | Lifecycle stage | Enum validation |
| Quotes Count | column | No | Number of quotes | Non-negative integer |
| Payment Status | column | No | Payment indicator | Enum validation |
| Last Active | column | No | Last activity timestamp | ISO 8601 |
| Assigned Providers | column | No | Provider(s) assigned | List formatting |
| Action | column | Yes | Action buttons | State-aware actions |
| Advanced Filters | control | No | Patient/Provider locations, Stage, Payment, Date ranges | Valid enums/ranges |

**Business Rules**:

- Shows all inquiries in all lifecycle stages
- Admin has full visibility of all data
- Advanced filtering capabilities
- Bulk actions available
- Real-time status updates

#### Screen 13: Inquiry Detailed Management (Admin)

**Purpose**: Admin manages individual inquiry with full control

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Full Inquiry | group | Yes | All patient and inquiry data | Admin-only visibility |
| Admin Actions | actions | Yes | Edit, reassign, override, soft delete | Reason required; audited |
| Override Controls | form | No | Expiry/distribution overrides | Confirmation + reason required |
| Reassignment | control | No | Assign/reassign providers | Validation on provider eligibility |
| Soft Delete | control | No | Archive inquiry | Requires reason; reversible view-only |
| Audit Trail | log | Yes | Full change history | Immutable; timestamped |

**Notes**:

- Full Inquiry (read-only groups):
  - Patient (unmasked for admin): name, contact, country
  - Inquiry metadata: ID, stage, created/updated/activity times
  - Countries, Problem details, Media, 3D scan viewer, Date ranges
  - Medical questionnaire Q&A and derived alerts
- Admin Actions:
  - Edit inquiry details with caution banners and field-level audit
  - Reassign providers (single/multi) with eligibility checks
  - Override expiry/distribution windows with required reason
  - Soft delete (archive) with reason; read-only view after deletion
  - Add admin notes (time-stamped; visible to admins only)
  - Trigger re-notifications when impactful fields change
- Override Controls:
  - Expiry: set new deadline (cannot be in the past without justification)
  - Distribution: re-run matching; include/exclude specific providers
  - All overrides require confirmation and reason entry
- Reassignment:
  - Search providers by country/specialty; multi-select
  - Validation: avoid duplicates; respect provider capacity policies (if enabled)
  - Optional note sent to provider(s) upon assignment
- Soft Delete:
  - Requires reason; retains data for audit; prevents further edits
  - Display badge "Archived" across all admin views
- Audit Trail:
  - Records: who, when, what changed (old → new), reason, IP (if available)
  - Filterable by field, user, date range
  - Exportable (CSV/JSON) for compliance

**Business Rules**:

- Admin can edit any inquiry data
- All changes require reason documentation
- Soft delete only (no hard deletes)
- Visual warnings for data modification
- Complete audit trail maintained

**Note**: Medical questionnaire and system configuration management will be handled in a separate FR for centralized settings management.

## Business Rules

### General Inquiry Rules

1. **Submission Rules**
   - Patient must complete medical questionnaire before submission
   - Patient can only have one active inquiry at a time
   - Inquiry automatically expires if unquoted (configurable timeframe)
   - Patient can modify inquiry if still in "Inquiry" stage

2. **Distribution Rules**
   - System distributes inquiry to providers in selected countries OR explicitly selected by patient
   - Providers must respond within 48 hours (configurable)
   - Provider capacity limits affect distribution
   - Admin can manually assign inquiries
   - Patient can select maximum 5 preferred providers
   - Provider suggestions based on positive reviews and admin curation

3. **Data Access Rules**
   - Patient data anonymized until quote acceptance
   - Provider access limited to assigned inquiries
   - Admin has full access to all inquiry data
   - All data access logged for audit trail

### Medical Data Rules

1. **Medical Alert System**
   - 3-tier color-coded alert system:
     - Critical alerts (red - high risk conditions)
     - Standard alerts (yellow/amber - moderate concerns)
     - No alerts (green - no medical concerns)
   - Alerts generated automatically from questionnaire
   - Alerts prominently displayed to providers

2. **Questionnaire Management**
   - Medical questionnaire managed by admin through FR-025 (not hard-coded)
   - Questions require Yes/No answers
   - Detailed explanations required for "Yes" answers
   - Questionnaire content versioned and auditable
   - **Note**: Centralized questionnaire management handled in FR-025

### Data and Privacy Rules

1. **Data Retention**
   - Inquiry data retained for 7 years minimum
   - 3D scans retained for 2 years after inquiry completion
   - Medical questionnaire responses retained for 7 years
   - All data encrypted at rest and in transit

2. **Data Access**
   - Patient data anonymized until payment confirmation
   - Provider access limited to assigned inquiries
   - Admin access logged for audit trail
   - Cross-tenant data access through authenticated APIs only

3. **Data Security**
   - All inquiry data encrypted at rest and in transit
   - 3D scans watermarked with patient ID
   - Access attempts logged and monitored
   - Soft deletes only (no hard deletes allowed)

### Admin Editability Rules

1. **Full Admin Override**
   - Admin can edit ALL inquiry data in the system
   - Admin can modify any patient's inquiry details
   - Admin can reassign inquiries to different providers
   - Admin can override any system-calculated settings

2. **Edit Capabilities**
   - **Inquiry Data**: Modify all patient-submitted information
   - **Patient Data**: Edit patient information, contact details
   - **Provider Data**: Modify provider assignments and settings
   - **System Data**: Override expiration rules, capacity limits
   - **Medical Data**: Edit questionnaire responses and alerts

3. **Edit Tracking**
   - All admin edits logged with timestamp and admin identification
   - Change reason required for all modifications
   - Edit history maintained for audit trail
   - Patient and provider notified of significant changes
   - Visual warnings displayed for data modification

### UI/UX Display Rules

1. **Date Range Display**
   - Primary date range displayed prominently
   - Additional ranges shown as "[+ X other ranges]" with tooltip expansion
   - Tooltip shows all date ranges with full details

2. **Time Display Logic**
   - Recent inquiries: Relative format ("X minutes ago", "X hours ago")
   - Previous day: Specific format ("Yesterday at 3:45 PM")
   - Older inquiries: Date format ("Sep 22, 2025")

3. **Patient ID Format**
   - Format: HPID + YY + MM + 4-digit sequence
   - Example: HPID2501001 (HPID + 25 + 01 + 0001)

4. **Medical Alert Display**
   - Critical alerts: Red color-coded chips
   - Standard alerts: Yellow/amber color-coded chips
   - No alerts: Green color-coded chips

5. **Patient Name Masking**
   - Format: First name + last initial + asterisks (e.g., "John D*****")
   - Full name revealed only after quote acceptance

### Validation and Constraints

1. **Input Validation**
   - Country selection limited to 10 countries maximum
   - Date ranges limited to 2 years in future
   - Visual evidence limited to 5 files total
   - File size and format validation enforced
   - Text field character limits enforced

2. **Business Logic Validation**
   - Date ranges cannot overlap
   - Provider capacity validation
   - Medical questionnaire completeness validation
   - 3D scan quality validation
   - Inquiry uniqueness validation

## Success Criteria

### Patient Experience Metrics

- **SC-001**: 95% of patients can complete inquiry submission in under 15 minutes
- **SC-002**: 90% of patients successfully upload 3D scans on first attempt
- **SC-003**: 85% of patients complete medical questionnaire without assistance
- **SC-004**: Patient satisfaction score of 4.5+ stars for inquiry process

### Provider Efficiency Metrics

- **SC-005**: Providers can review inquiry details in under 5 minutes
- **SC-006**: 90% of providers respond to inquiries within 24 hours
- **SC-007**: Provider inquiry review completion rate of 95%
- **SC-008**: Provider quote creation time under 10 minutes

### Admin Management Metrics

- **SC-009**: Admin can manage all inquiries from single dashboard
- **SC-010**: 95% of inquiries processed without admin intervention
- **SC-011**: Admin dashboard loads with all data in under 3 seconds
- **SC-012**: Admin can edit inquiry data with full audit trail

### System Performance Metrics

- **SC-013**: Inquiry submission completes in under 30 seconds
- **SC-014**: Inquiry distribution to providers in under 2 minutes
- **SC-015**: System supports 1000+ concurrent inquiry submissions
- **SC-016**: 99.5% uptime for inquiry module during business hours

### Business Impact Metrics

- **SC-017**: 80% of submitted inquiries receive provider quotes
- **SC-018**: 25% conversion rate from inquiry to quote acceptance
- **SC-019**: 50% reduction in inquiry-related support tickets
- **SC-020**: 30% improvement in provider response times

## Functional Requirements Summary

### Core Requirements

- **FR-001**: System MUST allow patients to create and submit inquiries with destinations, media, date ranges, 3D scan, and medical questionnaire.
- **FR-002**: System MUST distribute completed inquiries to matching providers in selected countries and those explicitly chosen by the patient.
- **FR-003**: Providers MUST see anonymized patient data and tiered medical alerts until payment/acceptance per system PRD.
- **FR-004**: System MUST support draft autosave and resume with 7-day inactivity expiry for incomplete inquiries.
- **FR-005**: Admin MUST be able to view, edit (with warnings), reassign, soft delete, and override distribution/expiration with full audit trail.

### Data Requirements

- **FR-006**: System MUST retain inquiry data for at least 7 years; scan retention per system policy.
- **FR-007**: System MUST link inquiries to patients, providers, locations, 3D scans, and questionnaire responses.

### Security & Privacy Requirements

- **FR-008**: System MUST anonymize patient identifiers and mask names prior to acceptance.
- **FR-009**: System MUST encrypt all inquiry-related data at rest and in transit, and maintain immutable audit logs.

### Integration Requirements

- **FR-010**: System MUST integrate with Shared Services for notifications and media/scan handling.
- **FR-011**: System MUST expose internal APIs required by FR-004 (quote) to consume inquiry data without mutation.

### Marking Unclear Requirements

- **FR-012**: Provider capacity management is referenced but handled by a separate FR (TBD); integration expectations remain.

## Key Entities

- **Inquiry**: patientId, destinations[], problem details, media[], scanRef, dateRanges[], questionnaireSummary, status, createdAt
  - Relationships: belongsTo Patient; hasMany ProviderInquiry; hasOne Scan; hasMany MedicalAlert
- **ProviderInquiry**: inquiryId, providerId, distributionAt, viewedAt, status
  - Relationships: belongsTo Inquiry; belongsTo Provider
- **MedicalQuestionnaireResponse**: inquiryId, questionId, answer, details
  - Relationships: belongsTo Inquiry
- **MedicalAlert**: inquiryId, level (critical/standard/none), reason
  - Relationships: belongsTo Inquiry
- **Scan**: inquiryId, storageUrl, qualityScore, metadata
  - Relationships: belongsTo Inquiry

## Dependencies

### Internal Dependencies

- **FR-001**: Patient Authentication & Profile Management (patient registration)
- **FR-002**: Medical History & 3D Scanning (scan capture technology)
- **FR-004**: Quote Submission & Management (provider quote creation)
- **FR-020**: Notifications & Alerts (inquiry notifications)
- **FR-025**: Medical Questionnaire Management (centralized settings)
- **Future FR**: Provider Capacity Management (provider availability)

### External Dependencies

- **3D Scanning SDK**: ARKit (iOS) and ARCore (Android) for mobile scan capture
- **Cloud Storage**: Secure storage for 3D scans and documents
- **Geolocation Services**: Country/location detection and mapping
- **Currency APIs**: Real-time exchange rates for pricing

### Data Dependencies

- **Patient Data**: From patient registration and profile management
- **Provider Data**: From provider onboarding and location management
- **Location Data**: From admin-configured country/location lists
- **Medical Data**: From admin-configured questionnaire templates

## Assumptions

1. **Patient Engagement**: Patients will actively complete comprehensive inquiries and provide accurate medical information
2. **Provider Participation**: Providers will respond to distributed inquiries within specified timeframes
3. **Technology Access**: Patients have access to smartphones with camera capabilities for 3D scanning
4. **Internet Connectivity**: Patients have reliable internet access for inquiry submission
5. **Medical Compliance**: Patients will provide honest and complete medical information
6. **Provider Capacity**: Sufficient provider capacity exists to handle inquiry volume (capacity management handled separately)
7. **Admin Resources**: Admin team has capacity to manage inquiry operations and system configuration
8. **Data Quality**: 3D scans and questionnaire responses will be of sufficient quality for medical assessment
9. **System Performance**: Infrastructure can handle concurrent inquiry operations without degradation
10. **Regulatory Compliance**: Medical data handling meets healthcare compliance requirements
11. **Medical Alerts**: Medical questionnaire alerts are for provider awareness, not patient rejection
12. **Incomplete Inquiries**: Patients can have incomplete inquiries and continue them from where they left off

## Implementation Notes

### Technical Considerations

- **Real-time Distribution**: Inquiry distribution requires real-time processing
- **File Management**: 3D scan storage and retrieval must be optimized for performance
- **Mobile Optimization**: Patient screens must work seamlessly on mobile devices
- **Offline Capability**: Core inquiry features should work with limited connectivity

### Integration Points

- **Patient Module**: Seamless integration with patient authentication and profile
- **Provider Module**: Integration with provider dashboard and quote management
- **Admin Module**: Integration with admin oversight and system configuration
- **Notification Module**: Automated notifications for inquiry status changes

### Scalability Considerations

- **Database Design**: Efficient querying for large numbers of inquiries
- **File Storage**: Scalable storage solution for 3D scans and documents
- **Distribution Logic**: Automated distribution algorithms for high-volume inquiries
- **Provider Assignment**: Intelligent provider matching based on capacity and specialization

### Security Considerations

- **Data Encryption**: All inquiry data encrypted at rest and in transit
- **Access Control**: Strict role-based access to inquiry data
- **Audit Logging**: Comprehensive logging of all inquiry activities
- **Compliance**: Healthcare data protection regulations compliance

---

**Document Status**: ✅ Complete  
**Next Steps**: Technical specification and implementation planning  
**Maintained By**: Product & Engineering Teams  
**Review Cycle**: Monthly or upon major changes

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-10-23 | 1.0 | Initial PRD creation | Product & Engineering |
| 2025-11-03 | 1.1 | Template normalization; added tenant breakdown, field tables, FR summary, entities, appendices | Product & Engineering |

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | [Name] | [Date] | [Status] |
| Technical Lead | [Name] | [Date] | [Status] |
| Stakeholder | [Name] | [Date] | [Status] |
