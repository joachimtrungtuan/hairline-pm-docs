# Product Requirements Document: Search & Filtering

**Module**: P-02: Quote Request & Management | PR-02: Inquiry & Quote Management | PR-03: Treatment Execution & Documentation | PR-04: Aftercare Participation | PR-05: Financial Management & Reporting | PR-06: Profile & Settings Management | A-01: Patient Management & Oversight | A-02: Provider Management & Onboarding | A-03: Aftercare Team Management | A-05: Billing & Financial Reconciliation | A-06: Discount & Promotion Management | A-07: Affiliate Program Management | A-08: Analytics & Reporting | A-09: System Settings & Configuration | A-10: Communication Monitoring & Support
**Feature Branch**: `fr022-search-filtering`
**Created**: 2025-11-12
**Status**: Draft
**Source**: FR-022 from system-prd.md

---

## Executive Summary

Search and filtering capabilities are critical for enabling users to efficiently navigate large datasets across the Hairline platform. This feature provides patients with tools to discover and evaluate providers based on relevant criteria, while admins gain powerful oversight capabilities to search, filter, and manage both patient and provider records.

The feature spans multiple tenants with context-specific implementations:

- **Patient Platform**: Provider discovery and selection based on location, ratings, pricing, and credentials
- **Admin Platform**: Comprehensive patient and provider search with advanced filtering for oversight and support

This PRD prioritizes the **Admin Platform search & filtering capabilities (P1 - MVP)**, as these are essential for platform operations and oversight. Patient-facing provider search is designated as **P2 (Enhanced)** and will be implemented post-MVP once the provider network is established and there's sufficient data to make filtering meaningful.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-02)**: Provider search and filtering for quote request submission (P2 - Enhanced)
- **Provider Platform (PR-02, PR-03, PR-04, PR-05, PR-06)**: Search and filtering across all provider workflows - inquiries, quotes, treatments, aftercare cases, financial records, and settings (P1 - MVP)
- **Admin Platform (A-01, A-02, A-03, A-05, A-06, A-07, A-08, A-09, A-10)**: Comprehensive search and filtering across all admin operations - patient management, provider management, aftercare oversight, billing, discounts, affiliates, analytics, system settings, and communication monitoring (P1 - MVP)
- **Shared Services**: None (search logic implemented within each tenant's backend)

### Multi-Tenant Breakdown

**Patient Platform (P-02)** [P2 - Post-MVP]:

- Search providers by name, location, specialty
- Filter providers by country, city, rating, price range, experience
- View provider profiles with credentials, reviews, and pricing
- Select providers for quote request submission
- Autocomplete for location searches

**Provider Platform (PR-02, PR-03, PR-04, PR-05, PR-06)** [P1 - MVP]:

- **Inquiry & Quote Management (PR-02)**: Search and filter inquiries by patient details, location, date range, status, medical alerts; filter quotes by status, amount, treatment type
- **Treatment Execution (PR-03)**: Search and filter treatment cases by patient, date, clinician, status, graft count
- **Aftercare Participation (PR-04)**: Search and filter aftercare cases by patient, milestone status, risk level, completion rate
- **Financial Management (PR-05)**: Search and filter financial records, reports, payouts by date range, amount, status, transaction type
- **Profile & Settings (PR-06)**: Search and filter treatment catalogs, packages, pricing by availability, type, date range

**Admin Platform (A-01, A-02, A-03, A-05, A-06, A-07, A-08, A-09, A-10)** [P1 - MVP]:

- **Patient Search & Filtering (A-01)**: Search patients by name, email, phone, patient ID (HPID format); filter by status, location, registration date, treatment type; export results
- **Provider Search & Filtering (A-02)**: Search providers by name, clinic name, location, credentials; filter by status, location, specialties, performance metrics; export results
- **Aftercare Team Management (A-03)**: Search and filter aftercare cases by patient, milestone status, risk level, specialist assignment, completion rate
- **Billing & Financial Reconciliation (A-05)**: Search and filter transactions, payouts, invoices by date range, amount, provider, status, currency; filter discount codes by usage, ROI, status
- **Discount & Promotion Management (A-06)**: Search and filter discount codes by code, provider participation, status, usage, date range, ROI
- **Affiliate Program Management (A-07)**: Search and filter affiliates by name, code, referral count, commission amount, payout status, performance metrics
- **Analytics & Reporting (A-08)**: Search and filter reports by type, date range, provider, patient segment; filter metrics by dimension (location, treatment type, time period)
- **System Settings & Configuration (A-09)**: Search and filter settings by category, version, change history, admin user; filter configurations by module, status, effective date
- **Communication Monitoring & Support (A-10)**: Search and filter conversations by participant, tag, severity, date range, agent assignment, status

**Shared Services**:

- Search functionality implemented within each tenant's backend
- No shared search service required for MVP

### Communication Structure

**In Scope**:

- None - this feature is data query and display only

**Out of Scope**:

- Notifications for saved searches or alerts (future enhancement)
- Real-time search suggestions via messaging (future enhancement)

### Entry Points

**Patient Platform** [P2 - Post-MVP]:

- Accessed when patient begins quote request flow and needs to select destination/providers
- Triggered from "Choose Destination" or "Select Providers" screens
- Available throughout quote request journey for comparison

**Admin Platform** [P1 - MVP]:

- **Global Search**: Always available via global search bar in admin navigation (searches across all modules)
- **Module-Specific Search**: Each admin module (A-01 through A-10) provides context-specific search and filtering within its own interface
- **Cross-Module Search**: Search results can link to related records across modules (e.g., patient search results link to their inquiries, bookings, aftercare cases)

---

## Business Workflows

### Main Flow 1: Admin Patient Search (P1 - MVP)

**Actors**: Admin, System
**Trigger**: Admin needs to find patient record for support, inquiry status check, or booking modification
**Outcome**: Admin finds relevant patient(s) and views details

**Steps**:

1. Admin navigates to Patients module or uses global search
2. Admin enters search term (patient name, email, phone, patient ID)
3. System performs real-time search across patient database
4. System returns matching patients with key information (name, ID, status, location, recent activity)
5. Admin applies filters if needed (status, location, date range, treatment type)
6. System narrows results based on filter criteria
7. Admin selects patient from results
8. System displays full patient details (profile, medical history, quotes, bookings, payments)
9. Admin performs required action (view details, modify booking, contact patient, etc.)

### Main Flow 2: Admin Provider Search (P1 - MVP)

**Actors**: Admin, System
**Trigger**: Admin needs to find provider for onboarding verification, performance review, or billing
**Outcome**: Admin finds relevant provider(s) and views details

**Steps**:

1. Admin navigates to Providers module
2. Admin enters search term (clinic name, location, certification)
3. System performs real-time search across provider database
4. System returns matching providers with key information (name, location, status, rating, active patients)
5. Admin applies filters if needed (status, location, specialties, performance metrics)
6. System narrows results based on filter criteria
7. Admin selects provider from results
8. System displays full provider details (profile, staff, certifications, reviews, financials, performance)
9. Admin performs required action (review credentials, approve onboarding, adjust commission, etc.)

### Main Flow 3: Patient Provider Search [P2 - Post-MVP]

**Actors**: Patient, System
**Trigger**: Patient begins quote request and needs to select destination and/or specific providers
**Outcome**: Patient discovers and selects providers for quote request

**Steps**:

1. Patient taps "Choose Destination" during quote request flow
2. System displays list of countries with starting prices
3. Patient selects country/countries of interest
4. System filters providers by selected location(s)
5. Patient optionally applies filters (rating, price range, experience, reviews)
6. System narrows provider list based on criteria
7. Patient taps provider card to view details
8. System displays provider profile (credentials, reviews, facilities, before/after photos)
9. Patient selects provider(s) for quote request (max 5 providers)
10. System adds selected providers to quote request recipients

### Alternative Flows

**A1: Admin uses multiple search criteria simultaneously**:

- **Trigger**: Admin needs highly specific patient/provider match
- **Steps**:
  1. Admin enters search term in main search field
  2. Admin applies multiple filters (status + location + date range)
  3. System performs AND-based filtering (all criteria must match)
  4. System returns refined results
  5. Admin views results and selects record
- **Outcome**: Admin finds exact record efficiently

**A2: Admin searches by partial information**:

- **Trigger**: Admin has incomplete patient information (partial name, phone fragment)
- **Steps**:
  1. Admin enters partial search term (e.g., "Mark P" instead of full name)
  2. System performs fuzzy matching and returns potential matches
  3. Admin reviews multiple potential matches
  4. Admin identifies correct patient by cross-referencing ID, location, or treatment date
  5. Admin selects correct patient record
- **Outcome**: Admin finds patient despite incomplete information

**A3: Patient uses autocomplete for location search** [P2 - Post-MVP]

- **Trigger**: Patient begins typing country/city name
- **Steps**:
  1. Patient types first few letters of destination (e.g., "Tur")
  2. System provides autocomplete suggestions (Turkey, Turkmenistan, etc.)
  3. Patient selects from suggestions
  4. System populates location field and filters providers
- **Outcome**: Faster search input with reduced typos

**B1: Search returns no results**:

- **Trigger**: Search term doesn't match any records
- **Steps**:
  1. Admin/Patient enters search term
  2. System finds no matches
  3. System displays "No results found" message with suggestions:
     - Check spelling
     - Try different keywords
     - Remove some filters
     - Contact support (admin platform)
  4. Admin/Patient adjusts search criteria or contacts support
- **Outcome**: Clear feedback guides user to refine search

**B2: Search returns too many results (>100)**:

- **Trigger**: Search term too generic (e.g., searching "John" in patient database)
- **Steps**:
  1. Admin enters broad search term
  2. System finds 500+ matches
  3. System displays first 100 results with message: "Too many results. Please refine your search."
  4. System suggests applying filters (status, location, date range)
  5. Admin applies filters to narrow results
  6. System returns refined results (<100)
- **Outcome**: User guided to use more specific criteria

**B3: Search system unavailable (database connection failure)**:

- **Trigger**: Backend database connection fails during search
- **Steps**:
  1. Admin/Patient enters search term
  2. System attempts to query database
  3. Database connection fails
  4. System displays error message: "Search temporarily unavailable. Please try again."
  5. System logs error and alerts engineering team
  6. Admin/Patient retries after brief wait
- **Outcome**: Graceful error handling with retry capability

---

## Screen Specifications

### Screen 1: Admin Patient Search & Filter (A-01)

**Purpose**: Enable admins to search and filter patient records for support, oversight, and operations

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Search Input | text | No | Global search across name, email, phone, patient ID | Max 100 chars, alphanumeric + @.+- |
| Status Filter | multi-select dropdown | No | Filter by patient journey stage | Options: All, Inquiry, Quoted, Scheduled, In Progress, Aftercare, Complete |
| Location Filter | select dropdown | No | Filter by patient country | Options: All, [country list from DB] |
| Registration Date Range | date range picker | No | Filter by account creation date | Start date ≤ End date, Max 2 years range |
| Treatment Type Filter | select dropdown | No | Filter by requested treatment | Options: All, Hair Transplant, Beard Transplant, Both |
| Results Display | table/list | - | Shows matching patients | Paginated, 25 results per page |
| Export Button | button | - | Export results to CSV/Excel | - |

**Business Rules**:

- Search is performed in real-time with debounce (500ms delay to avoid excessive queries)
- Search queries patient name (full or partial), email, phone number, and patient ID (HPID format)
- Filters are applied cumulatively (AND logic - all criteria must match)
- Results display patient ID, name (or anonymized name if pre-payment), status, location, last activity date
- Clicking a patient row opens full patient detail view
- Export includes all fields visible in results table plus additional metadata
- Search results automatically refresh when filters change
- Admin can clear all filters with "Reset" button

**Notes**:

- Use server-side search to avoid loading entire patient database to client
- Implement pagination to handle large result sets efficiently
- Consider caching recent searches for better performance
- Display loading indicator during search execution
- Show result count: "Showing 1-25 of 347 results"

---

### Screen 2: Admin Provider Search & Filter (A-02)

**Purpose**: Enable admins to search and filter provider records for onboarding, oversight, and billing

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Search Input | text | No | Global search across clinic name, location, credentials | Max 100 chars, alphanumeric + .,- |
| Status Filter | multi-select dropdown | No | Filter by provider account status | Options: All, Active, Suspended, Pending Onboarding |
| Location Filter | select dropdown | No | Filter by provider country | Options: All, [country list from DB] |
| Specialty Filter | multi-select dropdown | No | Filter by treatment specialties | Options: All, FUE, FUT, DHI, Sapphire FUE, etc. |
| Experience Filter | range slider | No | Filter by years in practice | Range: 0-40 years |
| Rating Filter | range slider | No | Filter by average patient rating | Range: 0-5 stars, 0.5 increments |
| Results Display | table/list | - | Shows matching providers | Paginated, 25 results per page |
| Export Button | button | - | Export results to CSV/Excel | - |

**Business Rules**:

- Search is performed in real-time with debounce (500ms delay)
- Search queries clinic name, city, country, certification names, staff names
- Filters are applied cumulatively (AND logic)
- Results display clinic name, location, status, rating, active patients, total procedures
- Clicking a provider row opens full provider detail view
- Export includes all fields visible in results table plus additional metadata
- Search results automatically refresh when filters change
- Admin can clear all filters with "Reset" button

**Notes**:

- Server-side search required for performance
- Implement pagination for large result sets
- Display loading indicator during search
- Show result count and current page
- Consider adding "Featured Provider" badge for admin-curated providers

---

### Screen 3: Patient Provider Search (Mobile) [P2 - Post-MVP]

**Purpose**: Enable patients to discover and select providers for quote request

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Country Selection | multi-select chips | Yes | Select destination countries | Max 10 countries |
| Search Input | text | No | Search providers by name or location | Max 50 chars |
| Sort By | dropdown | No | Sort results by criteria | Options: Recommended, Rating, Price (Low-High), Experience |
| Rating Filter | star selector | No | Minimum rating filter | Options: All, 4+, 4.5+ |
| Price Range Filter | dual slider | No | Filter by starting price range | Currency-specific, patient's local currency |
| Experience Filter | checkbox group | No | Filter by years of experience | Options: All, 5+ years, 10+ years, 15+ years |
| Results Display | card list | - | Shows matching providers | Scroll pagination, 10 results per load |
| Provider Selection | checkbox | - | Select providers for quote request | Max 5 selections |

**Business Rules**:

- Country selection is required before provider search is available
- Search defaults to showing all providers in selected countries, sorted by "Recommended"
- "Recommended" sort prioritizes admin-featured providers + high ratings + fast response time
- Filters are applied cumulatively (AND logic)
- Results display provider card with: name, location, rating, review count, starting price, before/after photo
- Tapping provider card opens provider detail view
- Patient can select up to 5 providers for quote request
- Selected providers displayed at bottom of screen with "Continue to Quote Request" button
- Search is performed on backend, results delivered in pages of 10

**Notes**:

- Mobile-optimized UI with touch-friendly controls
- Implement infinite scroll for results (load next 10 on scroll)
- Cache search results to avoid redundant queries
- Display loading skeleton while fetching results
- Show "No providers available" message if country has no active providers

---

### Screen 4: Patient Provider Profile View [P2 - Post-MVP]

**Purpose**: Display comprehensive provider information for patient evaluation

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Provider Name | text (display) | - | Clinic name | - |
| Location | text (display) | - | City, Country | - |
| Rating | star display | - | Average rating (1-5 stars) | - |
| Review Count | text (display) | - | Number of verified reviews | - |
| Starting Price | text (display) | - | Lowest treatment price | Currency-based on patient location |
| Years of Experience | text (display) | - | Years in practice | - |
| Specialties | chip display | - | Treatment types offered | - |
| Certifications | list display | - | Medical licenses and certifications | - |
| Staff Profiles | card carousel | - | Photos and credentials of surgeons | - |
| Before/After Gallery | image carousel | - | Patient results (anonymized) | - |
| Patient Reviews | list | - | Verified patient reviews with ratings | - |
| Facility Photos | image carousel | - | Clinic facility images | - |
| Select Provider Button | button | - | Add provider to quote request | - |

**Business Rules**:

- All information displayed is provider-submitted and admin-verified
- Before/after photos must be anonymized (no patient faces unless consented)
- Reviews are verified (only patients who completed treatment can review)
- Provider can only be selected if patient hasn't reached max 5 selections
- If provider already selected, button shows "Selected" with checkmark
- Provider profile includes "About Us" section with clinic description
- Staff profiles show specialties, years of experience, and certifications

**Notes**:

- Implement image gallery with swipe gestures
- Load images lazily to improve performance
- Show "Featured Provider" badge if admin-curated
- Display "Fast Response" badge if provider has <24hr average quote response time
- Allow patient to tap "Read More" on long reviews to expand

---

## Business Rules

### General Module Rules

- **Rule 1**: All search queries MUST be case-insensitive to improve match rate
- **Rule 2**: Search functionality MUST support partial matching (e.g., "Mark P" matches "Mark Patterson")
- **Rule 3**: Search results MUST be paginated to prevent performance degradation with large datasets
- **Rule 4**: Filter selections MUST persist during user session (cleared on logout)
- **Rule 5**: Admin search results MUST display patient/provider status prominently for quick context
- **Rule 6**: Search input fields MUST have debounce (500ms) to reduce server load from rapid typing
- **Rule 7**: Autocomplete suggestions MUST be limited to 10 results to avoid overwhelming user
- **Rule 8**: Search history MUST NOT be stored (privacy consideration for admin platform)

### Data & Privacy Rules

- **Privacy Rule 1**: Patient names MUST be anonymized in provider-facing search until booking is confirmed and paid
- **Privacy Rule 2**: Admin search logs MUST be retained for audit purposes (who searched for whom, when)
- **Privacy Rule 3**: Patient contact information MUST NOT be indexed for public search (admin only)
- **Privacy Rule 4**: Provider financial data MUST NOT be searchable by other providers (admin only)
- **Audit Rule**: All admin searches for patient/provider records MUST be logged with admin user ID, timestamp, and search terms

### Admin Editability Rules

**Editable by Admin**:

- Maximum search results per page (default: 25, range: 10-100)
- Default sort order for provider search (Recommended, Rating, Price, Experience)
- Featured provider designation (manually curated list)
- Provider visibility status (active providers appear in search, suspended do not)

**Fixed in Codebase (Not Editable)**:

- Search debounce timing (500ms)
- Autocomplete result limit (10 suggestions)
- Maximum providers selectable per quote request (5 providers)
- Search query max length (100 chars for admin, 50 for patient)

**Configurable with Restrictions**:

- Admin can temporarily disable provider from search results (suspension) but cannot delete provider record
- Admin can feature/unfeature providers in patient search, affecting "Recommended" sort order

### Search Performance Rules

- **Performance Rule 1**: Search queries MUST complete within 500ms for p95 of requests
- **Performance Rule 2**: Database indexes MUST exist on all searchable fields (name, email, phone, location, status)
- **Performance Rule 3**: Search results MUST use pagination to prevent loading excessive data to client
- **Performance Rule 4**: Autocomplete queries MUST be cached for 5 minutes to reduce database load
- **Performance Rule 5**: Complex filters (multi-criteria) MUST execute in single database query (no N+1 queries)

---

## Success Criteria

### Admin Experience Metrics

- **SC-001**: Admins can locate a patient record in under 10 seconds for 90% of searches
- **SC-002**: Admin search returns relevant results in first 25 results for 85% of queries
- **SC-003**: Admins successfully use filters to narrow results in under 3 clicks for 80% of complex searches
- **SC-004**: Admin search interface receives 4.5+ satisfaction rating in internal feedback surveys

### Patient Experience Metrics [P2 - Post-MVP]

- **SC-005**: Patients can discover and select providers in under 2 minutes for 80% of quote requests
- **SC-006**: Patient provider search returns satisfactory options within first 10 results for 75% of searches
- **SC-007**: Patients successfully apply filters to refine provider choices for 60% of searches
- **SC-008**: Patient provider selection process receives 4+ satisfaction rating in post-booking surveys

### System Performance Metrics

- **SC-009**: Search queries complete in under 300ms for 95% of requests (p95 latency)
- **SC-010**: Search system handles 100 concurrent admin searches without degradation
- **SC-011**: Search system handles 500 concurrent patient searches without degradation [P2 - Post-MVP]
- **SC-012**: Autocomplete suggestions return in under 200ms for 95% of requests
- **SC-013**: Database query performance remains under 100ms for indexed searches
- **SC-014**: Zero full table scans on large tables (patients, providers) during search operations

### Operational Efficiency Metrics

- **SC-015**: Admin support response time improves by 40% due to faster patient lookup
- **SC-016**: Admin overhead for patient/provider management reduced by 30% through efficient search
- **SC-017**: Admin search usage grows to 200+ searches per day within first month
- **SC-018**: Filtered exports generate accurate reports for 95% of admin queries

### Business Impact Metrics [P2 - Post-MVP]

- **SC-019**: Patient quote request completion rate increases by 20% with improved provider discovery
- **SC-020**: Average providers selected per quote request increases from 2 to 3.5 (improved comparison)
- **SC-021**: Patient-selected providers convert at 25% higher rate than auto-assigned providers
- **SC-022**: Provider search engagement (filters used, profiles viewed) correlates with 15% higher booking rate

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **FR-001 / Module P-01**: Requires patient authentication from P-01: Auth & Profile Management
  - **Why needed**: Search must verify admin authentication before displaying patient PII
  - **Integration point**: Uses admin session tokens to verify search access permissions

- **FR-015 / Module A-02**: Depends on A-02: Provider Management & Onboarding for provider data
  - **Why needed**: Provider search queries provider profiles, credentials, and status
  - **Integration point**: Searches provider database table with joins to staff, certifications, reviews

- **FR-016 / Module A-01**: Depends on A-01: Patient Management & Oversight for patient data
  - **Why needed**: Patient search queries patient profiles, medical history, and booking status
  - **Integration point**: Searches patient database table with joins to inquiries, quotes, bookings

- **FR-003 / Module P-02**: Integrates with P-02: Quote Request & Management for provider selection [P2]
  - **Why needed**: Selected providers from search are added to quote request recipients
  - **Integration point**: Patient app sends selected provider IDs to quote request API

### External Dependencies (APIs, Services)

- **External Service 1**: None required for MVP
  - Admin search operates entirely on internal database
  - No third-party search engines (Elasticsearch, Algolia) required for initial launch

- **Future Enhancement**: Elasticsearch or Algolia integration for advanced search [P3]
  - **Purpose**: Improve search relevance with fuzzy matching, synonyms, typo tolerance
  - **Integration**: Sync patient/provider data to search index, query search engine instead of database
  - **Failure handling**: Fallback to database search if search service unavailable

### Data Dependencies

- **Entity 1**: Active patient records with complete profiles
  - **Why needed**: Cannot search patients if no patient data exists
  - **Source**: Patient registration module (P-01)

- **Entity 2**: Active provider records with complete profiles, credentials, and performance data
  - **Why needed**: Cannot search providers if no provider data exists
  - **Source**: Provider onboarding module (A-02)

- **Entity 3**: Database indexes on searchable fields
  - **Why needed**: Search performance degrades without indexes on large tables
  - **Source**: Database migration scripts (create indexes on patients.name, patients.email, providers.clinic_name, etc.)

---

## Assumptions

### User Behavior Assumptions

- **Assumption 1**: Admins will use search functionality 10-20 times per day for support, oversight, and operations
- **Assumption 2**: Admins will primarily search by patient name or ID, less frequently by email or phone
- **Assumption 3**: Patients will browse 3-5 provider profiles before selecting providers for quote request [P2 - Post-MVP]
- **Assumption 4**: Patients will primarily sort by "Recommended" and filter by rating, less frequently by price [P2 - Post-MVP]
- **Assumption 5**: Admins will use filters for complex queries (e.g., "all aftercare patients in Turkey") 30% of the time

### Technology Assumptions

- **Assumption 1**: Admin platform accessed via modern browsers (Chrome, Firefox, Safari - last 2 versions)
- **Assumption 2**: Patient mobile app has stable internet connection for search queries [P2 - Post-MVP]
- **Assumption 3**: Database supports full-text search indexes (MySQL FULLTEXT, PostgreSQL TSVECTOR)
- **Assumption 4**: Backend API can handle 100 concurrent search queries without performance degradation
- **Assumption 5**: Client-side pagination and infinite scroll supported by mobile app framework [P2 - Post-MVP]

### Business Process Assumptions

- **Assumption 1**: Admin searches are for legitimate support/oversight purposes (audit logs deter abuse)
- **Assumption 2**: Provider data is kept up-to-date by providers and verified by admin (search reflects accurate info)
- **Assumption 3**: Patient searches for providers occur during quote request flow, not as standalone exploration [P2]
- **Assumption 4**: Admin will export search results for reporting and analytics 5-10 times per week
- **Assumption 5**: Provider "Featured" status manually curated by admin based on performance, quality, and partnerships

---

## Implementation Notes

### Technical Considerations

- **Database Indexing**: Create indexes on all searchable fields to ensure query performance:
  - `patients`: name, email, phone, patient_id, status, location, created_at
  - `providers`: clinic_name, location, status, specialty, rating, years_experience
- **Query Optimization**: Use query builder with prepared statements to prevent SQL injection
- **Pagination**: Implement cursor-based or offset-based pagination depending on dataset size
- **Caching**: Cache autocomplete results and frequently accessed search queries (5-minute TTL)
- **Debouncing**: Implement client-side debounce (500ms) to reduce server load from rapid typing
- **Full-Text Search**: Consider MySQL FULLTEXT or PostgreSQL TSVECTOR for fuzzy matching

### Integration Points

- **Integration 1**: Admin web app sends search queries to backend API via REST
  - **Data format**: JSON payload with search term, filters, pagination params
  - **Authentication**: Admin JWT bearer token in Authorization header
  - **Error handling**: Display user-friendly error messages, retry on network failure

- **Integration 2**: Patient mobile app sends provider search queries to backend API via REST [P2 - Post-MVP]
  - **Data format**: JSON payload with location, filters, sort order, pagination cursor
  - **Authentication**: Patient JWT bearer token
  - **Error handling**: Display loading state, retry on failure, cache results for offline viewing

- **Integration 3**: Search results exported to CSV/Excel via backend report generation
  - **Data format**: CSV file with headers, exported fields, timestamp
  - **Authentication**: Admin JWT required to trigger export
  - **Error handling**: Display error message if export fails, log error for debugging

### Scalability Considerations

- **Current scale**: Expected 50-100 admin searches per day at launch
- **Growth projection**: Anticipate 500+ searches per day within 6 months (as platform grows)
- **Peak load**: Handle 50 concurrent admin searches during business hours
- **Data volume**: Patient database may grow to 100,000+ records within 12 months; provider database to 500+ records
- **Scaling strategy**: Database read replicas for search queries, application-level caching, consider Elasticsearch for >100k records

### Security Considerations

- **Authentication**: All search endpoints require valid JWT authentication (admin or patient session)
- **Authorization**: Role-based access control enforces admin-only access to patient/provider search
- **Audit trail**: Log all admin searches with user ID, timestamp, search terms, and result count
- **Input validation**: Sanitize all search inputs to prevent SQL injection, XSS attacks
- **Rate limiting**: Limit search queries to 100 per hour per user to prevent abuse/scraping
- **Data masking**: Patient PII (email, phone) displayed only to authorized admins with proper permissions

---

## User Scenarios & Testing

### User Story 1 - Admin Patient Lookup for Support (Priority: P1)

An admin receives a support ticket from a patient asking about their quote status. The admin needs to quickly locate the patient's record to view their inquiry history and provide an update.

**Why this priority**: Critical for customer support operations and platform oversight. Admins must be able to find patient records quickly to resolve issues.

**Independent Test**: Can be fully tested by searching for a known patient by name/ID and verifying correct record returned with relevant details.

**Acceptance Scenarios**:

1. **Given** an admin is logged into the Admin Platform, **When** they enter a patient's full name in the search field, **Then** the system returns matching patient(s) with ID, status, location, and last activity date
2. **Given** an admin searches for a patient by patient ID (HPID format), **When** they enter the exact ID, **Then** the system returns the single matching patient record
3. **Given** an admin searches for a patient by partial email, **When** they enter "mark@", **Then** the system returns all patients with emails starting with "mark@"
4. **Given** an admin applies a status filter "Quoted", **When** they perform a search, **Then** the system returns only patients currently in "Quoted" status
5. **Given** search returns multiple results, **When** admin clicks on a patient row, **Then** the system displays full patient details (profile, medical history, quotes, bookings)

---

### User Story 2 - Admin Provider Verification (Priority: P1)

An admin needs to verify a new provider's credentials during onboarding. They search for the provider by clinic name to review submitted licenses, certifications, and insurance documents.

**Why this priority**: Essential for provider onboarding workflow. Admins must efficiently access provider records for verification and approval.

**Independent Test**: Can be tested by searching for a known provider by clinic name and verifying all credentials/documents are accessible from search results.

**Acceptance Scenarios**:

1. **Given** an admin is reviewing pending provider onboarding applications, **When** they search for a provider by clinic name, **Then** the system returns matching provider(s) with location, status, and onboarding progress
2. **Given** an admin searches for a provider by location "Istanbul", **When** they enter "Istanbul" in the search field, **Then** the system returns all providers located in Istanbul
3. **Given** an admin applies a status filter "Pending Onboarding", **When** they perform a search, **Then** the system returns only providers awaiting onboarding approval
4. **Given** search returns a provider, **When** admin clicks on the provider row, **Then** the system displays full provider details including credentials, certifications, staff, and documents
5. **Given** an admin wants to approve a provider, **When** they view provider details from search results, **Then** they can access "Approve" action directly from the detail view

---

### User Story 3 - Admin Filters for Aftercare Patients in Specific Location (Priority: P2)

An admin needs to generate a report of all patients currently in aftercare in Turkey to assign additional aftercare specialists due to high volume.

**Why this priority**: Important for operational oversight and resource allocation, but not as urgent as basic search functionality.

**Independent Test**: Can be tested by applying filters (status: "Aftercare", location: "Turkey") and verifying results match expected criteria.

**Acceptance Scenarios**:

1. **Given** an admin needs to filter patients by status and location, **When** they select "Aftercare" status and "Turkey" location filters, **Then** the system returns only patients in aftercare stage located in Turkey
2. **Given** filtered results are displayed, **When** the admin clicks "Export to CSV", **Then** the system generates a CSV file with all filtered patient records
3. **Given** an admin applies multiple filters (status, location, date range), **When** filters are applied, **Then** the system uses AND logic to return only records matching all criteria
4. **Given** an admin wants to clear filters, **When** they click "Reset Filters" button, **Then** all filters are cleared and full unfiltered results are displayed

---

### User Story 4 - Patient Provider Discovery by Location [P2 - Post-MVP] (Priority: P2)

A patient from the UK wants to find providers in Turkey for a hair transplant. They select "Turkey" as the destination and want to view the highest-rated providers with before/after photos.

**Why this priority**: Enhances patient experience and quote request quality, but MVP can function with manual provider selection by admins.

**Independent Test**: Can be tested by selecting Turkey as destination, sorting by rating, and verifying providers are displayed with correct information.

**Acceptance Scenarios**:

1. **Given** a patient is submitting a quote request, **When** they select "Turkey" as the destination country, **Then** the system displays all active providers in Turkey with starting prices in patient's local currency
2. **Given** providers are displayed, **When** the patient sorts by "Rating", **Then** providers are ordered from highest to lowest rating
3. **Given** a patient wants to filter by minimum rating, **When** they select "4.5+ stars" filter, **Then** only providers with 4.5+ average rating are displayed
4. **Given** a patient views provider list, **When** they tap on a provider card, **Then** the system displays full provider profile with credentials, reviews, facility photos, and before/after gallery
5. **Given** a patient selects a provider, **When** they tap "Select Provider" button, **Then** the provider is added to quote request recipients (max 5 selections)

---

### User Story 5 - Admin Export Search Results for Reporting (Priority: P2)

An admin needs to generate a monthly report of all scheduled patients for billing reconciliation. They search for patients with status "Scheduled" and export results to Excel.

**Why this priority**: Useful for reporting and analytics, but not essential for day-to-day operations.

**Independent Test**: Can be tested by searching with filters, clicking export, and verifying CSV/Excel file contains correct data.

**Acceptance Scenarios**:

1. **Given** an admin applies a status filter "Scheduled", **When** they click "Export to Excel", **Then** the system generates an Excel file with all scheduled patients including ID, name, treatment, provider, booking date, payment status
2. **Given** an exported file is generated, **When** the admin opens the file, **Then** all columns are properly formatted with headers and data matches search results
3. **Given** search results are paginated, **When** admin clicks export, **Then** ALL matching results are exported, not just the current page

---

### Edge Cases

- **Edge Case 1**: What happens when a patient searches for providers in a country with no active providers?
  - **Handling**: Display "No providers available in [country]. Please try another location or contact support." with link to support chat.

- **Edge Case 2**: How does the system handle an admin searching for a patient with a very common name (e.g., "John Smith")?
  - **Handling**: Return first 100 matches with message "Too many results (500+). Please refine search by adding filters like location, status, or patient ID."

- **Edge Case 3**: What occurs if a patient's search query contains special characters or SQL syntax?
  - **Handling**: Input sanitization removes/escapes special characters; query runs safely without SQL injection risk; user sees results or "No matches found."

- **Edge Case 4**: How does search handle diacritics or accented characters (e.g., "José" vs "Jose")?
  - **Handling**: Search performs accent-insensitive matching (José matches Jose); database collation set to utf8mb4_unicode_ci for MySQL or equivalent for PostgreSQL.

- **Edge Case 5**: What happens if database index is missing on a searchable field, causing slow queries?
  - **Handling**: Search times out after 10 seconds; error message displayed: "Search taking too long. Please try again or contact support."; error logged for engineering team to investigate.

- **Edge Case 6**: How does the system handle concurrent searches from multiple admins querying the same patient?
  - **Handling**: Database read locks prevent conflicts; each admin sees consistent snapshot of patient data; audit logs capture each admin's search independently.

- **Edge Case 7**: What happens if a patient has multiple accounts with same name/email?
  - **Handling**: Search returns all matching accounts; admin reviews each record to identify correct patient using patient ID, location, or registration date; duplicate account detection flagged in results.

---

## Functional Requirements Summary

### Core Requirements (P1 - MVP)

- **FR-001**: System MUST allow admins to search patients by name, email, phone number, and patient ID (HPID format)
- **FR-002**: System MUST allow admins to filter patients by status, location, registration date range, and treatment type
- **FR-003**: System MUST allow admins to search providers by clinic name, location, and certifications
- **FR-004**: System MUST allow admins to filter providers by status, location, specialties, years of experience, and rating
- **FR-005**: System MUST return search results within 500ms for 95% of queries (p95 latency)
- **FR-006**: System MUST paginate search results (25 results per page for admin platform)
- **FR-007**: System MUST support case-insensitive partial matching for search terms
- **FR-008**: System MUST apply filters cumulatively using AND logic (all criteria must match)
- **FR-009**: System MUST allow admins to export search results to CSV or Excel format
- **FR-010**: System MUST display patient status, location, and last activity date in search results
- **FR-011**: System MUST display provider status, location, rating, and active patient count in search results
- **FR-012**: System MUST implement search input debounce (500ms) to reduce server load

### Enhanced Requirements (P2 - Post-MVP)

- **FR-013**: System MUST allow patients to search providers by name, location, and specialty [P2 - Post-MVP]
- **FR-014**: System MUST allow patients to filter providers by rating, price range, years of experience [P2 - Post-MVP]
- **FR-015**: System MUST support autocomplete suggestions for location searches (max 10 suggestions) [P2 - Post-MVP]
- **FR-016**: System MUST allow patients to sort providers by Recommended, Rating, Price, Experience [P2 - Post-MVP]
- **FR-017**: System MUST limit patient provider selection to maximum 5 providers per quote request [P2 - Post-MVP]
- **FR-018**: System MUST display provider card with name, location, rating, starting price, before/after photo [P2 - Post-MVP]
- **FR-019**: System MUST support infinite scroll pagination for patient mobile app (10 results per page) [P2 - Post-MVP]
- **FR-020**: System MUST prioritize admin-featured providers in "Recommended" sort order [P2 - Post-MVP]

### Security & Privacy Requirements

- **FR-021**: System MUST require valid JWT authentication for all search endpoints
- **FR-022**: System MUST enforce role-based access control (admin-only for patient/provider search)
- **FR-023**: System MUST log all admin searches with user ID, timestamp, search terms, and result count
- **FR-024**: System MUST sanitize all search inputs to prevent SQL injection and XSS attacks
- **FR-025**: System MUST rate-limit search queries to 100 per hour per user
- **FR-026**: System MUST anonymize patient names in search results if patient has not confirmed payment
- **FR-027**: System MUST encrypt audit logs containing patient/provider search history

### Performance Requirements

- **FR-028**: System MUST create database indexes on all searchable fields for query optimization
- **FR-029**: System MUST cache autocomplete results for 5 minutes to reduce database load
- **FR-030**: System MUST handle 100 concurrent admin searches without performance degradation
- **FR-031**: System MUST handle 500 concurrent patient searches without performance degradation [P2 - Post-MVP]
- **FR-032**: System MUST complete database queries in under 100ms for indexed searches

---

## Key Entities

- **Entity 1 - Patient Search Record**:
  - **Key attributes**: patient_id (HPID), name, email, phone, status, location, registration_date, last_activity_date, treatment_type
  - **Relationships**: Patient record links to inquiries, quotes, bookings, payments

- **Entity 2 - Provider Search Record**:
  - **Key attributes**: provider_id, clinic_name, location (city, country), status, specialties, rating, review_count, years_experience, active_patients, total_procedures
  - **Relationships**: Provider record links to staff, certifications, reviews, treatments, bookings

- **Entity 3 - Search Audit Log**:
  - **Key attributes**: log_id, admin_user_id, search_type (patient/provider), search_term, filters_applied, result_count, timestamp
  - **Relationships**: Audit log links to admin user who performed search

- **Entity 4 - Database Index** (Technical Entity):
  - **Key attributes**: table_name, indexed_column, index_type (BTREE, FULLTEXT, etc.)
  - **Relationships**: Indexes applied to patient and provider tables to optimize search queries

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-12 | 1.0 | Initial PRD creation for FR-022 | Claude AI |

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
**Based on**: FR-022 from system-prd.md
**Last Updated**: 2025-11-12
