# FR-022 - Search & Filtering

**Module**: P-02: Quote Request & Management | PR-02: Inquiry & Quote Management | PR-03: Treatment Execution & Documentation | PR-04: Aftercare Participation | PR-05: Financial Management & Reporting | PR-06: Profile & Settings Management | A-01: Patient Management & Oversight | A-02: Provider Management & Onboarding | A-03: Aftercare Team Management | A-05: Billing & Financial Reconciliation | A-06: Discount & Promotion Management | A-07: Affiliate Program Management | A-08: Analytics & Reporting | A-09: System Settings & Configuration | A-10: Communication Monitoring & Support
**Feature Branch**: `fr022-search-filtering`
**Created**: 2025-11-12
**Status**: Draft
**Source**: FR-022 from system-prd.md

---

## Executive Summary

Search and filtering capabilities are critical for enabling users to efficiently navigate large datasets across the Hairline platform. This feature provides context-specific search and filter implementations across all three tenants.

The feature spans all three tenants:

- **Patient Platform**: Provider discovery during quote request flow; booking history navigation; messaging inbox; help center content browsing; support ticket filtering
- **Provider Platform**: Inquiry and quote list management; treatment and aftercare case navigation; analytics filtering; package/settings catalog management; support case tracking
- **Admin Platform**: Comprehensive patient, provider, and transaction search with advanced filtering across all operational modules

**Priority breakdown**:

- **P1 (MVP)**: Provider Platform (all modules PR-01 through PR-06) and Admin Platform (all modules A-01 through A-10) — these are essential for platform operations and day-to-day provider and admin workflows
- **P2 (Post-MVP)**: Patient-facing provider search (P-02 provider selection) — deferred until provider network is established and sufficient data makes filtering meaningful. All other Patient Platform list screens (bookings, messages, help center, support tickets) are P1.

> **Maintenance Convention**: This FR is the single source of truth for all search and filter criteria across the platform. When any source FR updates its filter or search field list, this document must be updated accordingly. See the Master Reference Table in the Screen Specifications section for the full inventory.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-02, P-03, P-06, P-08)**: Provider search for quote request (P2); booking list, messages inbox, help center, and support ticket filtering (P1 - MVP)
- **Provider Platform (PR-01, PR-02, PR-03, PR-04, PR-05, PR-06)**: Search and filtering across all provider workflows — team directory, inquiries, quotes, treatment cases, aftercare cases, analytics, packages, reviews, and support cases (P1 - MVP)
- **Admin Platform (A-01, A-02, A-03, A-05, A-06, A-07, A-08, A-09, A-10)**: Comprehensive search and filtering across all admin operations — patient management, provider management, aftercare oversight, billing, affiliates, analytics, system settings, help centre, and communication monitoring (P1 - MVP)
- **Shared Services**: None (search logic implemented within each tenant's backend)

### Multi-Tenant Breakdown

**Patient Platform** [Mixed Priority]:

- **P2 — Post-MVP**: Search providers by name, location, specialty; filter by country, rating, price range, experience (P-02 quote request flow)
- **P1 — MVP**: Filter booking list by status, date, treatment type, payment status (P-03); search and filter messages inbox by provider/content and read status (P-06); search help center content; filter support tickets by status (P-08)

**Provider Platform (PR-01, PR-02, PR-03, PR-04, PR-05, PR-06)** [P1 - MVP]:

- **Team Management (PR-01)**: Search and filter team directory by name, role, status; filter activity log by date and action type; filter work queue by status and priority
- **Inquiry & Quote Management (PR-02)**: Search and filter inquiries by patient ID, name, concern, date, alerts, location; search and filter quotes by status, concern, location, alerts
- **Treatment Execution (PR-03)**: Search and filter treatment cases by patient ID, name, booking reference; filter by date and clinician
- **Aftercare Participation (PR-04)**: Search and filter aftercare cases by patient; filter by milestone, status, date, specialist
- **Financial Management (PR-05)**: Filter analytics dashboard by date range and treatment type
- **Profile & Settings (PR-06)**: Search and filter package list by name and type; filter reviews by rating; search and filter support cases by case ID, keywords, status, type, and date

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

> **Maintenance Convention**: This section is the **single source of truth** for all search and filter criteria across the Hairline platform. Whenever a source FR is updated — adding, removing, or renaming search fields or filter criteria — the relevant screen entry below **must** be updated to reflect the change. This ensures FR-022 remains the definitive reference for all search and filtering behavior platform-wide. The same living-document protocol applies to FR-020 for notification events: when that catalog changes, FR-020 is updated; when any list screen's filters change, FR-022 is updated.

---

### Master Reference Table

The table below maps every platform screen that requires search and/or filter functionality, organized by tenant, module, and FR. Use screen codes (e.g., `P-02-001`) to navigate to the detailed spec below.

| Tenant | Module | FR | Screen Name | Screen Code | Search | Filter | Priority |
|--------|--------|----|-------------|-------------|--------|--------|----------|
| Patient | P-02 | FR-003 | Provider Selection | P-02-001 | ✓ | ✓ | P2 |
| Patient | P-02 | FR-005 | Quote Comparison List | P-02-002 | — | ✓ | P1 |
| Patient | P-03 | FR-006 | Patient Bookings List | P-03-001 | ✓ | ✓ | P1 |
| Patient | P-06 | FR-012 | Patient Messages Inbox | P-06-001 | ✓ | ✓ | P1 |
| Patient | P-08 | FR-035 | Help Center | P-08-001 | ✓ | ✓ | P1 |
| Patient | P-08 | FR-035 | My Support Tickets | P-08-002 | — | ✓ | P1 |
| Provider | PR-01 | FR-009 | Team Directory | PR-01-001 | ✓ | ✓ | P1 |
| Provider | PR-01 | FR-009 | Provider Activity Log | PR-01-002 | — | ✓ | P1 |
| Provider | PR-01 | FR-009 | Work Queue | PR-01-003 | — | ✓ | P1 |
| Provider | PR-02 | FR-003 | Provider Inquiry List | PR-02-001 | ✓ | ✓ | P1 |
| Provider | PR-02 | FR-004 | Provider Quote List | PR-02-002 | ✓ | ✓ | P1 |
| Provider | PR-03 | FR-010 | In Progress Cases | PR-03-001 | ✓ | ✓ | P1 |
| Provider | PR-04 | FR-011 | Aftercare Cases List | PR-04-001 | ✓ | ✓ | P1 |
| Provider | PR-05 | FR-014 | Provider Analytics Dashboard | PR-05-001 | — | ✓ | P1 |
| Provider | PR-06 | FR-024 | Provider Package List | PR-06-001 | ✓ | ✓ | P1 |
| Provider | PR-06 | FR-032 | Reviews Tab | PR-06-002 | — | ✓ | P1 |
| Provider | PR-06 | FR-032 | My Support Cases | PR-06-003 | ✓ | ✓ | P1 |
| Admin | A-01 | FR-003 | Global Inquiry Table | A-01-001 | ✓ | ✓ | P1 |
| Admin | A-01 | FR-004 | Global Quote Table | A-01-002 | ✓ | ✓ | P1 |
| Admin | A-01 | FR-005 | Quote Acceptance Table | A-01-003 | — | ✓ | P1 |
| Admin | A-01 | FR-006 | Admin Bookings Table | A-01-004 | ✓ | ✓ | P1 |
| Admin | A-01 | FR-007 | Patient Payment Progress Dashboard | A-01-005 | ✓ | ✓ | P1 |
| Admin | A-01 | FR-013 | Review Management Dashboard | A-01-006 | — | ✓ | P1 |
| Admin | A-01 | FR-016 | Patient Management List | A-01-007 | ✓ | ✓ | P1 |
| Admin | A-01 | FR-016 | Admin Actions Audit Log | A-01-008 | ✓ | ✓ | P1 |
| Admin | A-01 | FR-016 | Pending Data Requests | A-01-009 | ✓ | — | P1 |
| Admin | A-02 | FR-015 | Provider Management List | A-02-001 | ✓ | ✓ | P1 |
| Admin | A-02 | FR-015 | Provider Reviews Tab | A-02-002 | ✓ | ✓ | P1 |
| Admin | A-02 | FR-015 | Provider Documents List | A-02-003 | — | ✓ | P1 |
| Admin | A-03 | FR-011 | Admin Aftercare Cases List | A-03-001 | ✓ | ✓ | P1 |
| Admin | A-05 | FR-007b | Installment Plans List | A-05-001 | — | ✓ | P1 |
| Admin | A-05 | FR-017 | Patient Billing Invoices | A-05-002 | ✓ | ✓ | P1 |
| Admin | A-05 | FR-017 | Transaction Search | A-05-003 | ✓ | ✓ | P1 |
| Admin | A-05 | FR-017 | Billing Audit Log | A-05-004 | — | ✓ | P1 |
| Admin | A-05 | FR-018 | Affiliate Payout History | A-05-005 | ✓ | ✓ | P1 |
| Admin | A-06 | FR-019 | Discount Code List | A-06-001 | ⚠ Gap | ⚠ Gap | — |
| Admin | A-07 | FR-018 | Affiliate Management List | A-07-001 | ✓ | ✓ | P1 |
| Admin | A-08 | FR-014 | Analytics Reports Dashboard | A-08-001 | — | ✓ | P1 |
| Admin | A-09 | FR-024 | Admin Treatment Catalog | A-09-001 | ✓ | ✓ | P1 |
| Admin | A-09 | FR-025 | Questionnaire Catalog | A-09-002 | ✓ | ✓ | P1 |
| Admin | A-09 | FR-027 | Legal Documents List | A-09-003 | — | ✓ | P1 |
| Admin | A-09 | FR-027 | User Acceptance List | A-09-004 | ✓ | ✓ | P1 |
| Admin | A-09 | FR-029 | Provider Commission Search | A-09-005 | ✓ | — | P1 |
| Admin | A-09 | FR-029 | Currency Configuration | A-09-006 | ✓ | — | P1 |
| Admin | A-09 | FR-030 | Notification Rules Dashboard | A-09-007 | ✓ | ✓ | P1 |
| Admin | A-09 | FR-031 | Admin Users List | A-09-008 | ✓ | ✓ | P1 |
| Admin | A-09 | FR-031 | Roles & Permissions | A-09-009 | ✓ | ✓ | P1 |
| Admin | A-09 | FR-031 | Admin Activity Audit Trail | A-09-010 | — | ✓ | P1 |
| Admin | A-09 | FR-033 | FAQ Management | A-09-011 | ✓ | ✓ | P1 |
| Admin | A-09 | FR-033 | Article Management | A-09-012 | ✓ | ✓ | P1 |
| Admin | A-09 | FR-033 | Resource Management | A-09-013 | ✓ | ✓ | P1 |
| Admin | A-09 | FR-033 | Video Management | A-09-014 | ✓ | ✓ | P1 |
| Admin | A-10 | FR-012 | Communication Monitoring Center | A-10-001 | ✓ | ✓ | P1 |
| Admin | A-10 | FR-034 | Support Center Dashboard | A-10-002 | ✓ | ✓ | P1 |

> **⚠ A-06 Gap**: FR-019 (Promotions & Discounts) does not currently define a filterable Discount Code List screen. FR-022 module scope references A-06 as requiring search and filter for discount codes. When FR-019 is updated to add a Discount Code List screen, screen A-06-001 criteria must be defined in FR-019 and added here.

---

### Control Behavior Standards

The states below apply uniformly to every screen in this document. Individual screen entries list only the field/filter tables. Any screen-specific deviation is noted inline under that screen.

| State | View | Trigger | UI Behavior | System Behavior | Visual Indicator |
|-------|------|---------|-------------|-----------------|------------------|
| Search Inactive | Search | Default; no input in search field | Placeholder text shown; full default list visible | No query fired; list displays default results | Dimmed placeholder text; neutral input border |
| Search Active | Search | User types in search field | Typed text visible; clear (×) button appears | Debounced query fires (300–500ms per screen spec); list filters to matching results | Active input border; clear (×) button visible |
| Filter Inactive | Filter | Default; no filters applied | Filter button in neutral state; no filter chips visible | Default query runs; full result set shown | Neutral filter icon; no chips |
| Filter Active | Filter | One or more filter controls changed from default | Active filter chips shown below filter bar; filter button highlighted | AND-logic applied across all active filters; list narrows; result count updates | Highlighted filter icon; active chips visible |
| Reset Filter | Filter | User taps "Clear Filters" / "Reset" / selects default option | All filter controls return to their default values; chips cleared | All filter parameters cleared; default result set restored | Chips removed; filter icon returns to neutral |

---

### 1. Patient Platform Screens

---

#### Module P-02 — Quote Request & Management

##### FR-003 Inquiry Submission

---

###### Screen P-02-001: Provider Selection [P2 — Post-MVP]

**Purpose**: Patient searches for and selects providers during the quote request flow.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Max Length | Notes |
|-------|------|-------------|----------|------------|-------|
| Provider name / keyword | text | "Search providers…" | 500ms | 50 chars | Case-insensitive; matches provider name and specialty tags |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Country / Destination | Multi-select chips | Patient's previously selected destination countries | All selected countries | AND within selection |
| Rating | Star selector | All, 4+ stars, 4.5+ stars | All | Min threshold |
| Specialty | Dropdown | Hair Transplant, Beard Transplant, Both | All | Exact match |

---

##### FR-005 Quote Comparison & Acceptance

---

###### Screen P-02-002: Quote Comparison List [P1 — MVP]

**Purpose**: Patient sorts and filters received quotes for comparison before acceptance.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

> No search input on this screen — filtering and sorting only.

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Sort By | Dropdown | Price (Low–High), Price (High–Low), Graft Count, Rating, Quote Date | Quote Date (most recent) | Single selection |
| Date Range | Filter chips | Patient's submitted date ranges | All | Narrows to quotes covering that range |

---

#### Module P-03 — Booking & Scheduling

##### FR-006 Booking & Scheduling

---

###### Screen P-03-001: Patient Bookings List [P1 — MVP]

**Purpose**: Patient views and navigates their booking history with search and filter capabilities.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Max Length | Notes |
|-------|------|-------------|----------|------------|-------|
| Booking reference | text | "Search by booking reference…" | 500ms | 50 chars | Exact or partial match on booking reference code |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Status | Multi-select dropdown | All, Pending Payment, Confirmed, In Progress, Completed, Cancelled | All | AND |
| Date Range | Date range picker | Custom | All dates | Filters by booking date |
| Treatment Type | Dropdown | All, Hair Transplant, Beard Transplant, Both | All | Exact match |
| Payment Status | Dropdown | All, Unpaid, Deposit Paid, Fully Paid, Overdue | All | Exact match |

---

#### Module P-06 — Profile & Settings (Messaging)

##### FR-012 Secure Messaging

---

###### Screen P-06-001: Patient Messages Inbox [P1 — MVP]

**Purpose**: Patient searches and filters their conversation inbox to find specific messages or providers.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Min Length | Notes |
|-------|------|-------------|----------|------------|-------|
| Provider name / message content | text | "Search messages…" | 300ms | 2 chars | Searches across provider name and message body |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Read Status | Segmented control / tabs | All, Unread, Read | All | Single selection |

---

#### Module P-08 — Help & Support

##### FR-035 Patient Help & Support

---

###### Screen P-08-001: Help Center [P1 — MVP]

**Purpose**: Patient searches for help articles and browses content by type.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Notes |
|-------|------|-------------|----------|-------|
| Help content search | text | "Search help articles…" | 300ms | Full-text search across all patient-audience FAQs, articles, resources, and videos; auto-suggests results while typing |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Content Type | Segmented chips / cards | All, FAQs, Articles, Resources, Videos | All | Single selection |
| Article Subtype | Filter chips (conditional) | All, Tutorial Guides, Troubleshooting Tips | All | Shown only when "Articles" type is selected |

---

###### Screen P-08-002: My Support Tickets [P1 — MVP]

**Purpose**: Patient filters their support ticket list by status.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

> No search input on this screen — filtering only.

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Status | Segmented chips | All, Open, In Progress, Resolved, Closed | All | Single selection |

---

### 2. Provider Platform Screens

---

#### Module PR-01 — Provider Team

##### FR-009 Provider Team Roles

---

###### Screen PR-01-001: Team Directory [P1 — MVP]

**Purpose**: Provider searches for and filters team members within the clinic.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Notes |
|-------|------|-------------|----------|-------|
| Name / email / role / status | text | "Search team members…" | 500ms | Supports wildcard; case-insensitive |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Role | Multi-select | All roles defined in clinic (e.g., Surgeon, Coordinator, Aftercare Specialist) | All | AND |
| Status | Multi-select | Active, Inactive, Pending Invitation | All | AND |
| Role Compatibility | Context filter (conditional) | Shown during reassignment workflows only | — | Filters members eligible for role reassignment |

---

###### Screen PR-01-002: Provider Activity Log [P1 — MVP]

**Purpose**: Provider filters the clinic's activity log by date and action type.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

> No search input on this screen — filtering only.

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Date Range | Date range picker | Custom | Last 30 days | Filters by event date |
| Action Type | Multi-select | Login, Inquiry, Quote, Treatment, Patient Communication, Settings | All | AND |

---

###### Screen PR-01-003: Work Queue [P1 — MVP]

**Purpose**: Provider filters the work queue by status and priority.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

> No search input on this screen — filtering only.

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Status | Multi-select chips | Draft, Active, Completed, Overdue | Active + Overdue | AND |
| Priority | Multi-select chips | High, Medium, Low | All | AND |

---

#### Module PR-02 — Inquiry & Quote Management

##### FR-003 Inquiry Submission

---

###### Screen PR-02-001: Provider Inquiry List [P1 — MVP]

**Purpose**: Provider searches for and filters incoming patient inquiries.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Notes |
|-------|------|-------------|----------|-------|
| Patient ID / name | text | "Search by patient ID or name…" | 500ms | Case-insensitive; partial match |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Patient Age Range | Range slider | 18–100 | All ages | Min–Max range |
| Concern | Multi-select | Hair Transplant, Beard Transplant, Both | All | AND |
| Requested Date Range | Date range picker | Custom | All dates | Overlaps with inquiry dates |
| Medical Alerts | Multi-select chips | None, Standard, Critical | All | AND |
| Patient Location | Dropdown | All; country list from DB | All | Exact match |

---

##### FR-004 Quote Submission

---

###### Screen PR-02-002: Provider Quote List [P1 — MVP]

**Purpose**: Provider searches for and filters their submitted quotes across all patient inquiries.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Notes |
|-------|------|-------------|----------|-------|
| Patient / inquiry / treatment / date / status / location | text | "Search quotes…" | 500ms | Case-insensitive; partial match across all indexed fields |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Quote Status | Multi-select | Draft, Sent, Expired, Withdrawn, Archived, Accepted, Cancelled (Other Accepted), Cancelled (Inquiry Cancelled) | All | AND |
| Date Range | Date range picker | Custom | All dates | Filters by quote creation date |
| Concern | Multi-select | Hair Transplant, Beard Transplant, Both | All | AND |
| Patient Location | Dropdown | All; country list from DB | All | Exact match |
| Medical Alerts | Multi-select chips | None, Standard, Critical | All | AND |

---

#### Module PR-03 — Treatment Execution

##### FR-010 Treatment Execution

---

###### Screen PR-03-001: In Progress Cases [P1 — MVP]

**Purpose**: Provider searches for and filters active treatment cases by patient or clinician.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Notes |
|-------|------|-------------|----------|-------|
| Patient ID / name / booking reference | text | "Search cases…" | 500ms | Real-time filter; case-insensitive |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Procedure Date Range | Date range picker | Custom | All dates | Filters by treatment procedure date |
| Clinician | Dropdown | All; clinic's active clinicians | All | Exact match |

---

#### Module PR-04 — Aftercare Participation

##### FR-011 Aftercare Recovery Management

---

###### Screen PR-04-001: Aftercare Cases List [P1 — MVP]

**Purpose**: Provider searches for and filters patient aftercare cases managed by their clinic.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Notes |
|-------|------|-------------|----------|-------|
| Patient name / ID | text | "Search aftercare cases…" | 500ms | Debounced; case-insensitive |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Milestone | Dropdown | All; aftercare plan milestone names | All | Exact match |
| Case Status | Multi-select | Active, Overdue, Completed | All | AND |
| Date Range | Date range picker | Custom | All dates | Filters by aftercare start date |
| Clinician / Specialist | Dropdown | All; clinic's aftercare specialists | All | Exact match |

---

#### Module PR-05 — Financial Management & Reporting

##### FR-014 Provider Analytics & Reporting

---

###### Screen PR-05-001: Provider Analytics Dashboard [P1 — MVP]

**Purpose**: Provider filters analytics reports by date range and treatment type.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

> No search input on this screen — filtering only.

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Date Range | Segmented + custom picker | Last 7 days, Last 30 days, Last 90 days, Last 12 months, Custom | Last 30 days | Single selection |
| Treatment Type | Multi-select | All, FUE, FUT, DHI, Sapphire FUE, and other admin-defined types | All | AND |

---

#### Module PR-06 — Profile & Settings

##### FR-024 Treatment Package Management

---

###### Screen PR-06-001: Provider Package List [P1 — MVP]

**Purpose**: Provider searches for and filters their published treatment packages.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Notes |
|-------|------|-------------|----------|-------|
| Package name | text | "Search packages…" | 300ms | Real-time filter; case-insensitive |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Package Type | Dropdown | All; admin-defined package types | All | Exact match |

---

##### FR-032 Provider Dashboard Settings

---

###### Screen PR-06-002: Reviews Tab [P1 — MVP]

**Purpose**: Provider filters their patient reviews by star rating.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

> No search input on this screen — filtering only.

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Rating | Multi-select star chips | 5★, 4★, 3★, 2★, 1★ | All ratings | AND |

---

###### Screen PR-06-003: My Support Cases [P1 — MVP]

**Purpose**: Provider searches for and filters support cases they have submitted.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Min Length | Debounce | Notes |
|-------|------|-------------|-----------|----------|-------|
| Case ID / title / keywords | text | "Search cases…" | 3 chars | 300ms | Real-time search across Case ID, Title, Description, Message content |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Status | Multi-select | Open, In Progress, Resolved, Closed | Open + In Progress | AND |
| Type | Multi-select | Support Request, Feedback | All types | AND |
| Date Range | Date range picker | Custom | Last 90 days | Filters by case creation date |

---

### 3. Admin Platform Screens

---

#### Module A-01 — Patient Management & Oversight

##### FR-003 Inquiry Submission

---

###### Screen A-01-001: Global Inquiry Table [P1 — MVP]

**Purpose**: Admin searches for and filters all patient inquiries across all providers.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Notes |
|-------|------|-------------|----------|-------|
| Patient ID / name | text | "Search by patient ID or name…" | 500ms | Case-insensitive; partial match |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Patient Location | Dropdown | All; country list from DB | All | Exact match |
| Provider Location | Dropdown | All; country list from DB | All | Exact match |
| Inquiry Stage | Multi-select | Inquiry, Quoted, Accepted, Scheduled, Cancelled | All | AND |
| Payment Status | Dropdown | All, Paid, Unpaid, Partial | All | Exact match |
| Date Range | Date range picker | Custom | All dates | Filters by inquiry submission date |

---

##### FR-004 Quote Submission

---

###### Screen A-01-002: Global Quote Table [P1 — MVP]

**Purpose**: Admin searches for and filters all quotes across all providers and patients.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Notes |
|-------|------|-------------|----------|-------|
| Patient ID / name / provider / inquiry | text | "Search quotes…" | 500ms | Case-insensitive; partial match across all indexed fields |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Quote Status | Multi-select | Draft, Sent, Expired, Withdrawn, Archived, Accepted, Cancelled (Other Accepted), Cancelled (Inquiry Cancelled) | All | AND |
| Date Range | Date range picker | Custom | All dates | Filters by quote creation date |
| Concern | Multi-select | Hair Transplant, Beard Transplant, Both | All | AND |
| Patient Location | Dropdown | All; country list from DB | All | Exact match |
| Provider | Dropdown | All; provider list from DB | All | Exact match |
| Medical Alerts | Multi-select chips | None, Standard, Critical | All | AND |

---

##### FR-005 Quote Comparison & Acceptance

---

###### Screen A-01-003: Quote Acceptance Table [P1 — MVP]

**Purpose**: Admin filters the quote acceptance overview by acceptance status.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

> No search input on this screen — filtering only.

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Acceptance Status | Multi-select | Active, Superseded by Cancellation | Active | AND |

---

##### FR-006 Booking & Scheduling

---

###### Screen A-01-004: Admin Bookings Table [P1 — MVP]

**Purpose**: Admin searches for and filters all bookings across the platform.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Notes |
|-------|------|-------------|----------|-------|
| Booking reference / patient name / patient email / provider name | text | "Search bookings…" | 500ms | Case-insensitive; partial match |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Booking Status | Multi-select | All, Pending Payment, Confirmed, In Progress, Completed, Cancelled | All | AND |
| Provider | Dropdown | All; provider list from DB | All | Exact match |
| Date Range | Date range picker | Custom | All dates | Filters by booking date |
| Treatment Type | Dropdown | All, Hair Transplant, Beard Transplant, Both | All | Exact match |
| Payment Status | Multi-select | All, Unpaid, Deposit Paid, Fully Paid, Overdue | All | AND |

---

##### FR-007 Payment Processing

---

###### Screen A-01-005: Patient Payment Progress Dashboard [P1 — MVP]

**Purpose**: Admin searches for and filters payment records by booking, patient, and payment status.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Notes |
|-------|------|-------------|----------|-------|
| Booking ID / patient name | text | "Search by booking ID or patient name…" | 500ms | Case-insensitive; partial match |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Provider | Dropdown | All; provider list from DB | All | Exact match |
| Deposit Status | Multi-select | Pending, Paid, Partial | All | AND |
| Payment Status | Multi-select | Unpaid, Deposit Only, Installments Active, Full Paid, Overdue | All | AND |
| Final Payment Status | Multi-select | Not Due, Due, Paid, Overdue | All | AND |
| Overdue Flag | Toggle | Show overdue only | Off | Single flag |
| Date Range | Date range picker | Custom | All dates | Filters by booking date |

---

##### FR-013 Reviews & Ratings

---

###### Screen A-01-006: Review Management Dashboard [P1 — MVP]

**Purpose**: Admin filters all platform reviews by date, provider, rating, status, and flag.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

> No search input on this screen — filtering only.

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Date Range | Date range picker | Custom | All dates | Filters by review submission date |
| Provider | Dropdown | All; provider list from DB | All | Exact match |
| Rating | Multi-select star chips | 5★, 4★, 3★, 2★, 1★ | All | AND |
| Review Status | Multi-select | Pending Moderation, Published, Rejected | All | AND |
| Flagged | Toggle | Show flagged only | Off | Single flag |

---

##### FR-016 Admin Patient Management

---

###### Screen A-01-007: Patient Management List [P1 — MVP]

**Purpose**: Admin searches for and filters all registered patients across the platform.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Min Length | Notes |
|-------|------|-------------|----------|------------|-------|
| Name / email / patient code (HPID) / phone | text | "Search patients…" | 500ms | 2 chars | Case-insensitive; partial match |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Status | Multi-select | Inquiry, Quoted, Accepted, Scheduled, In-Progress, Aftercare, Completed, Cancelled, Suspended | All | AND |
| Date Range | Date range picker + type toggle | Custom; toggle: Registration Date / Last Activity | All dates — Registration Date | Filters by selected date type |
| Location | Dropdown | All; country list from DB | All | Exact match |
| Provider | Dropdown | All; provider list from DB | All | Exact match |

---

###### Screen A-01-008: Admin Actions Audit Log [P1 — MVP]

**Purpose**: Admin searches for and filters the patient data access and modification audit log.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Notes |
|-------|------|-------------|----------|-------|
| Patient name / email / HPID | text | "Search audit log…" | 500ms | Case-insensitive; debounced |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Action Type | Multi-select | View, Edit, Export, Access Request, Deletion Request, Override, and others per FR-016 | All | AND |
| Date Range | Date range picker | Custom | All dates | Filters by action timestamp |
| Admin User | Dropdown | All; admin user list | All | Exact match |

---

###### Screen A-01-009: Pending Data Requests [P1 — MVP]

**Purpose**: Admin searches the pending patient data access and deletion request queue.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Notes |
|-------|------|-------------|----------|-------|
| Patient name / email / HPID | text | "Search requests…" | 500ms | Debounced; case-insensitive; searches within Pending Admin Review queue |

> No additional filter controls — this screen is pre-filtered to Status = Pending Admin Review by default.

---

#### Module A-02 — Provider Management & Onboarding

##### FR-015 Provider Management

---

###### Screen A-02-001: Provider Management List [P1 — MVP]

**Purpose**: Admin searches for and filters all provider accounts.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Max Length | Notes |
|-------|------|-------------|----------|------------|-------|
| Provider name / clinic name / email / license number | text | "Search providers…" | 500ms | 200 chars | Case-insensitive; partial match |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Status | Multi-select | Draft, Active, Suspended, Deactivated | All | AND |
| Featured | Checkbox | Featured only | Off | Single flag |
| Commission Type | Dropdown | All, Percentage, Tier-based | All | Exact match |
| Date Range | Date range picker + type toggle | Custom; toggle: Creation Date / Last Activity | All dates — Creation Date | Filters by selected date type |

---

###### Screen A-02-002: Provider Reviews Tab [P1 — MVP]

**Purpose**: Admin searches for and filters reviews within a provider's profile.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Notes |
|-------|------|-------------|----------|-------|
| Review keyword | text | "Search reviews…" | 500ms | Partial match on review content |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Rating | Multi-select star chips | 5★, 4★, 3★, 2★, 1★ | All ratings | AND |

---

###### Screen A-02-003: Provider Documents List [P1 — MVP]

**Purpose**: Admin filters provider-submitted documents by type and uploader.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

> No search input on this screen — filtering only.

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Document Type | Dropdown | All; admin-defined document types (e.g., Medical License, Insurance, Certification) | All | Exact match |
| Uploaded By | Dropdown | All, Provider, Admin | All | Exact match |

---

#### Module A-03 — Aftercare Team Management

##### FR-011 Aftercare Recovery Management

---

###### Screen A-03-001: Admin Aftercare Cases List [P1 — MVP]

**Purpose**: Admin searches for and filters all aftercare cases across all providers.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Notes |
|-------|------|-------------|----------|-------|
| Case ID | text | "Search by case ID…" | 500ms | Searchable; sortable |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Provider | Dropdown | All; provider list from DB | All | Exact match |
| Milestone | Dropdown | All; milestone names from aftercare plan templates | All | Exact match |
| Case Status | Multi-select | Active, Overdue, Completed | All | AND |
| Date Range | Date range picker | Custom | All dates | Filters by aftercare start date |

---

#### Module A-05 — Billing & Financial Reconciliation

##### FR-007b Payment Installments

---

###### Screen A-05-001: Installment Plans List [P1 — MVP]

**Purpose**: Admin filters installment plans by plan status and procedure date range.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

> No search input on this screen — filtering only.

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Plan Status | Multi-select | Active, Completed, Overdue, Defaulted | All | AND |
| Procedure Date Range | Date range picker | Custom | All dates | Filters by procedure date; default sort is nearest upcoming first, overdue/defaulted at top |

---

##### FR-017 Admin Billing & Finance

---

###### Screen A-05-002: Patient Billing Invoices [P1 — MVP]

**Purpose**: Admin searches for and filters patient invoices by status and date.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Notes |
|-------|------|-------------|----------|-------|
| Patient name | text | "Search by patient name…" | 500ms | Case-insensitive; partial match |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Payment Status | Multi-select | Pending, Partial, Paid, Overdue, Refunded, At Risk | All | AND |
| Date Range | Date range picker | Custom | Last 30 days | Filters by invoice date |
| Currency | Dropdown | All; configured currency list | All | Exact match |
| Payment Method | Dropdown | All, Full Payment, Installment | All | Exact match |

---

###### Screen A-05-003: Transaction Search [P1 — MVP]

**Purpose**: Admin searches for any financial transaction using multiple lookup fields and narrows results by type, date, and status.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Notes |
|-------|------|-------------|----------|-------|
| Search By (type selector) | Dropdown | Booking Reference, Invoice Number, Patient Name/ID, Provider Name/ID, Affiliate Name/ID | Booking Reference | Determines search context |
| Search Input | text | Auto-updates per "Search By" selection | 500ms | Free-text; case-insensitive; scoped to selected type |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Record Type | Multi-select | Invoice, Provider Payout, Installment, Refund, Affiliate Commission | All | AND |
| Date Range | Date range picker | Custom | All dates | Filters by transaction date |
| Status | Multi-select | All applicable statuses per record type | All | AND |

---

###### Screen A-05-004: Billing Audit Log [P1 — MVP]

**Purpose**: Admin filters the billing action audit log by date, admin user, action type, and entity.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

> No search input on this screen — filtering only.

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Date Range | Date range picker | Custom | Last 30 days | Filters by action timestamp |
| Admin User | Dropdown | All; admin user list | All | Exact match |
| Action Type | Multi-select | Payout Approved, Payout Unapproved, Payout Voided, Payout Retried, Bulk Approval, Refund Processed, Invoice Generated, Status Overridden, Note Added, Installment Retry, Affiliate Payout Processed, Affiliate Payout Retried, Payout Added to Next Cycle, Reminder Sent, Currency Alert Decision, Re-authentication Verified | All | AND |
| Affected Entity | Multi-select | Invoice, Provider Payout, Installment, Affiliate Commission, Booking, Currency Alert | All | AND |
| Entity ID | text (optional) | "Filter by entity ID…" | 500ms | Optional free-text lookup |

---

##### FR-018 Affiliate Management

---

###### Screen A-05-005: Affiliate Payout History [P1 — MVP]

**Purpose**: Admin searches for and filters affiliate payout records.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Notes |
|-------|------|-------------|----------|-------|
| Affiliate name / transaction ID / payout month | text | "Search payout history…" | 500ms | Full-text search; case-insensitive |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Affiliate | Dropdown / autocomplete | All; affiliate list | All | Exact selection |
| Date Range | Date range picker | Custom | All dates | Filters by payout date |
| Payment Status | Multi-select | Pending, Paid, Failed, Cancelled | All | AND |

---

#### Module A-06 — Discount & Promotion Management

##### FR-019 Promotions & Discounts

> **⚠ Gap — Pending FR-019 Update**: FR-019 does not currently specify a searchable or filterable Discount Code List screen. FR-022 module scope references A-06 as requiring "search and filter discount codes by code, provider participation, status, usage, date range, ROI." When FR-019 is updated to add a Discount Code List screen, the search fields and filter criteria must be defined in FR-019 and added here as screen **A-06-001**.

---

#### Module A-07 — Affiliate Program Management

##### FR-018 Affiliate Management

---

###### Screen A-07-001: Affiliate Management List [P1 — MVP]

**Purpose**: Admin searches for and filters affiliate accounts.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Notes |
|-------|------|-------------|----------|-------|
| Affiliate name / email | text | "Search affiliates…" | 500ms | Case-insensitive; partial match |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Status | Multi-select | Active, Suspended, Inactive | All | AND |

---

#### Module A-08 — Analytics & Reporting

##### FR-014 Provider Analytics & Reporting

---

###### Screen A-08-001: Analytics Reports Dashboard [P1 — MVP]

**Purpose**: Admin filters analytics and reporting views by date range, treatment type, and dimension.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

> No search input on this screen — filtering only.

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Date Range | Segmented + custom picker | Last 7 days, Last 30 days, Last 90 days, Last 12 months, Custom | Last 30 days | Single selection |
| Treatment Type | Multi-select | All, FUE, FUT, DHI, Sapphire FUE, and admin-defined types | All | AND |
| Dimension | Dropdown | All, By Location, By Provider, By Treatment Type, By Time Period | All | Single selection |

---

#### Module A-09 — System Settings & Configuration

##### FR-024 Treatment Package Management

---

###### Screen A-09-001: Admin Treatment Catalog [P1 — MVP]

**Purpose**: Admin searches for and filters the global treatment catalog.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Notes |
|-------|------|-------------|----------|-------|
| Treatment name | text | "Search treatments…" | 300ms | Real-time filter; case-insensitive |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Treatment Type | Dropdown | All; admin-defined treatment types | All | Exact match |

---

##### FR-025 Medical Questionnaire Management

---

###### Screen A-09-002: Questionnaire Catalog [P1 — MVP]

**Purpose**: Admin searches for and filters the questionnaire set catalog.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Notes |
|-------|------|-------------|----------|-------|
| Set name keyword | text | "Search questionnaire sets…" | 500ms | Partial match on set name; case-insensitive |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Context Type | Dropdown | All, Inquiry, Aftercare, Multi-Context | All | Exact match |
| Status | Multi-select | Draft, Active, Archived | All | AND |
| Category | Dropdown | All; admin-defined categories (e.g., Allergies, Cardiovascular) | All | Exact match |

---

##### FR-027 Legal Content Management

---

###### Screen A-09-003: Legal Documents List [P1 — MVP]

**Purpose**: Admin filters the legal document catalog by type, status, and locale.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

> No search input on this screen — filtering only.

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Document Type | Dropdown | All; admin-defined legal document types (e.g., Terms of Service, Privacy Policy, Consent Form) | All | Exact match |
| Status | Multi-select | Draft, Published, Archived | All | AND |
| Locale | Dropdown | All; configured locale list | All | Exact match |

---

###### Screen A-09-004: User Acceptance List [P1 — MVP]

**Purpose**: Admin searches for and filters user acceptance records for legal documents.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Notes |
|-------|------|-------------|----------|-------|
| User name / email / user ID | text | "Search users…" | 500ms | Case-insensitive; partial match |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Acceptance Status | Multi-select | Accepted, Pending | All | AND |
| Locale | Dropdown | All; configured locale list | All | Exact match |

---

##### FR-029 Payment System Config

---

###### Screen A-09-005: Provider Commission Search [P1 — MVP]

**Purpose**: Admin searches for a specific provider when configuring provider-specific commission rates.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Notes |
|-------|------|-------------|----------|-------|
| Provider name / ID | text | "Search provider by name or ID…" | 500ms | Returns provider record for commission configuration |

> No filter controls — search-only functionality for provider selection.

---

###### Screen A-09-006: Currency Configuration [P1 — MVP]

**Purpose**: Admin searches for a currency by code or name when configuring platform currencies.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Max Length | Notes |
|-------|------|-------------|----------|------------|-------|
| Currency code / name | text | "Filter currencies by code or name…" | 300ms | 100 chars | Real-time filter of currency list |

> No filter controls — search/filter input only for narrowing the currency list.

---

##### FR-030 Notification Rules Config

---

###### Screen A-09-007: Notification Rules Dashboard [P1 — MVP]

**Purpose**: Admin searches for and filters notification rules by event category and rule status.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Max Length | Notes |
|-------|------|-------------|----------|------------|-------|
| Event name / template name / recipient type | text | "Search rules…" | 500ms | 100 chars | Case-insensitive; partial match |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Event Category | Dropdown | All, Account/Auth, Inquiry, Quote, Booking/Schedule, Treatment, Payment, Billing/Payouts, Messaging/Support, Aftercare, Reviews, Promotions/Discounts, Provider/Compliance, System/Operations | All | Exact match |
| Rule Status | Multi-select | Active, Paused, Draft | All | AND |

---

##### FR-031 Admin Access Control

---

###### Screen A-09-008: Admin Users List [P1 — MVP]

**Purpose**: Admin searches for and filters admin user accounts.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Notes |
|-------|------|-------------|----------|-------|
| Name / email | text | "Search admin users…" | 300ms | Real-time filter; case-insensitive |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Role | Dropdown | All Roles, Super Admin, Aftercare Specialist, Billing Staff, Support Staff | All Roles | Exact match |
| Status | Multi-select | Active, Suspended, Pending Invitation | All | AND |

---

###### Screen A-09-009: Roles & Permissions [P1 — MVP]

**Purpose**: Admin searches for permissions and filters by category or module.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Notes |
|-------|------|-------------|----------|-------|
| Permission name | text | "Search permissions…" | 300ms | Real-time filter on permission name |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Category | Dropdown | All; admin-defined permission categories | All | Exact match |
| Module | Dropdown | All; platform modules (Patient, Provider, Admin, System) | All | Exact match |

---

###### Screen A-09-010: Admin Activity Audit Trail [P1 — MVP]

**Purpose**: Admin filters the admin user activity log by action type, date, and outcome.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

> No search input on this screen — filtering only.

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Action Type | Multi-select | Platform-defined admin action types (per FR-031) | All | AND |
| Date Range | Date range picker | Custom | Last 30 days | Filters by action timestamp |
| Outcome | Multi-select | Success, Failed, Blocked | All | AND |

---

##### FR-033 Help Centre Management

---

###### Screen A-09-011: FAQ Management [P1 — MVP]

**Purpose**: Admin searches for and filters FAQ entries in the Help Centre.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Notes |
|-------|------|-------------|----------|-------|
| Question text | text | "Search FAQ questions…" | 500ms | Partial match on question content |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Topic | Dropdown | All; admin-defined FAQ topics | All | Exact match |
| Status | Multi-select | Draft, Published, Archived | All | AND |
| Audience | Dropdown | All, Patient, Provider | All | Exact match |

---

###### Screen A-09-012: Article Management [P1 — MVP]

**Purpose**: Admin searches for and filters help articles.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Notes |
|-------|------|-------------|----------|-------|
| Article title | text | "Search articles…" | 500ms | Partial match on title |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Article Type | Dropdown | All, Tutorial Guide, Troubleshooting Tip | All | Exact match |
| Category / Tags | Multi-select | Admin-defined article categories | All | AND |
| Status | Multi-select | Draft, Published, Archived | All | AND |
| Audience | Dropdown | All, Patient, Provider | All | Exact match |

---

###### Screen A-09-013: Resource Management [P1 — MVP]

**Purpose**: Admin searches for and filters downloadable help resources.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Notes |
|-------|------|-------------|----------|-------|
| Resource name | text | "Search resources…" | 500ms | Partial match on name |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Category | Dropdown | All; admin-defined resource categories | All | Exact match |
| File Type | Multi-select | PDF, Video, Image, Link, and others as configured | All | AND |
| Status | Multi-select | Draft, Published, Archived | All | AND |
| Audience | Dropdown | All, Patient, Provider | All | Exact match |

---

###### Screen A-09-014: Video Management [P1 — MVP]

**Purpose**: Admin searches for and filters help videos.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Debounce | Notes |
|-------|------|-------------|----------|-------|
| Video title | text | "Search videos…" | 500ms | Partial match on title |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Category / Tags | Multi-select | Admin-defined video categories | All | AND |
| Status | Multi-select | Draft, Published, Archived | All | AND |
| Source Type | Dropdown | All, Uploaded, YouTube, Vimeo, and other configured sources | All | Exact match |
| Audience | Dropdown | All, Patient, Provider | All | Exact match |

---

#### Module A-10 — Communication Monitoring & Support

##### FR-012 Secure Messaging

---

###### Screen A-10-001: Communication Monitoring Center [P1 — MVP]

**Purpose**: Admin searches for and filters all platform conversations for oversight and support.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Min Length | Debounce | Notes |
|-------|------|-------------|-----------|----------|-------|
| Patient / provider / keyword / inquiry ID | text | "Search conversations…" | 2 chars | 300ms | Searches across all four fields simultaneously |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Patient | Autocomplete | Matching patient names | None | Exact selection |
| Provider | Autocomplete | Matching provider names | None | Exact selection |
| Service Type | Multi-select | All; platform-defined service types | All | AND |
| Quote ID | text (optional) | "Filter by quote ID…" | — | Optional exact match |
| Inquiry ID | text (optional) | "Filter by inquiry ID…" | — | Optional exact match |
| Date Range | Date range picker + presets | Custom; Today, Last 7 days, Last 30 days, All | All | Filters by message date |
| Flag Type | Multi-select | Keyword Flagged, Manually Flagged, Intervened, No Flags | All | AND |
| Conversation Status | Multi-select | Active, Resolved, Escalated | All | AND |

---

##### FR-034 Support Center Ticketing

---

###### Screen A-10-002: Support Center Dashboard [P1 — MVP]

**Purpose**: Admin searches for and filters all support tickets from patients and providers.

_For UI state behaviors (inactive, active, reset), see [Control Behavior Standards](#control-behavior-standards) above. Document any screen-specific exceptions inline._

**Search View**

| Field | Type | Placeholder | Min Length | Debounce | Notes |
|-------|------|-------------|-----------|----------|-------|
| Case ID / patient name / provider name / email / title keywords | text | "Search support cases…" | 3 chars | 300ms | Real-time search across all listed fields |

**Filter View**

| Filter | Type | Options | Default | Logic |
|--------|------|---------|---------|-------|
| Status | Multi-select | Open, In Progress, Urgent, Unassigned | Open + In Progress | AND |
| Priority | Multi-select | High, Medium, Low | All | AND |
| Category | Dropdown | All; admin-defined ticket categories | All | Exact match |
| Ticket Source | Dropdown | All, Patient App, Provider App, Admin Portal | All | Exact match |
| Submitter Type | Dropdown | All, Patient, Provider | All | Exact match |
| Date Range | Date range picker | Custom | Last 30 days | Filters by ticket creation date |
| Assigned Admin | Dropdown | All; admin user list | All | Exact match |

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

An admin receives a patient support escalation/case (via Support Center; see FR-034) asking about quote status. The admin needs to quickly locate the patient's record to view their inquiry history and provide an update.

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

#### Admin Platform

- **REQ-022-001**: System MUST allow admins to search patients by name, email, phone number, and patient ID (HPID format)
- **REQ-022-002**: System MUST allow admins to filter patients by status, location, registration date range, provider, and treatment type
- **REQ-022-003**: System MUST allow admins to search providers by clinic name, email, and license number
- **REQ-022-004**: System MUST allow admins to filter providers by status, featured flag, commission type, and date range
- **REQ-022-009**: System MUST allow admins to export search results to CSV or Excel format where applicable
- **REQ-022-010**: System MUST display patient status, location, and last activity date in search results
- **REQ-022-011**: System MUST display provider status, location, rating, and active patient count in search results

#### Provider Platform

- **REQ-022-033**: System MUST allow providers to search their inquiry list by patient ID and name
- **REQ-022-034**: System MUST allow providers to filter inquiries by concern, age range, date range, medical alerts, and patient location
- **REQ-022-035**: System MUST allow providers to search their quote list across patient, inquiry, treatment, date, status, and location fields
- **REQ-022-036**: System MUST allow providers to filter quotes by status, date range, concern, patient location, and medical alerts
- **REQ-022-037**: System MUST allow providers to search treatment cases by patient ID, name, and booking reference
- **REQ-022-038**: System MUST allow providers to filter treatment cases by procedure date range and clinician
- **REQ-022-039**: System MUST allow providers to search and filter aftercare cases by patient name/ID, milestone, status, date range, and specialist
- **REQ-022-040**: System MUST allow providers to filter their analytics dashboard by date range and treatment type
- **REQ-022-041**: System MUST allow providers to search and filter their package list by name and package type
- **REQ-022-042**: System MUST allow providers to filter their reviews by star rating
- **REQ-022-043**: System MUST allow providers to search and filter support cases by case ID, keywords, status, type, and date range
- **REQ-022-044**: System MUST allow providers to search team members by name, email, role, and status
- **REQ-022-045**: System MUST allow providers to filter team activity log by date range and action type
- **REQ-022-046**: System MUST allow providers to filter work queue by status and priority

#### Patient Platform (P1 Screens)

- **REQ-022-047**: System MUST allow patients to search their booking list by booking reference
- **REQ-022-048**: System MUST allow patients to filter their booking list by status, date range, treatment type, and payment status
- **REQ-022-049**: System MUST allow patients to search their messages inbox by provider name and message content
- **REQ-022-050**: System MUST allow patients to filter their messages inbox by read/unread status
- **REQ-022-051**: System MUST allow patients to search help center content with full-text search and auto-suggest
- **REQ-022-052**: System MUST allow patients to filter help center by content type (FAQs, Articles, Resources, Videos)
- **REQ-022-053**: System MUST allow patients to filter their support tickets by status

#### Shared Behavior Rules

- **REQ-022-005**: System MUST return search results within 500ms for 95% of queries (p95 latency)
- **REQ-022-006**: System MUST paginate search results (default 25 results per page for admin/provider; 10 per page for patient mobile)
- **REQ-022-007**: System MUST support case-insensitive partial matching for all text search fields
- **REQ-022-008**: System MUST apply filters cumulatively using AND logic (all active criteria must match)
- **REQ-022-012**: System MUST implement search input debounce (300–500ms depending on screen) to reduce server load
- **REQ-022-054**: System MUST display a result count after every search or filter operation
- **REQ-022-055**: System MUST show active filter chips for every applied filter and allow individual chip removal
- **REQ-022-056**: System MUST provide a "Reset" or "Clear All" control to clear all active filters at once

### Enhanced Requirements (P2 - Post-MVP)

- **REQ-022-013**: System MUST allow patients to search providers by name, location, and specialty [P2 - Post-MVP]
- **REQ-022-014**: System MUST allow patients to filter providers by rating, price range, years of experience [P2 - Post-MVP]
- **REQ-022-015**: System MUST support autocomplete suggestions for location searches (max 10 suggestions) [P2 - Post-MVP]
- **REQ-022-016**: System MUST allow patients to sort providers by Recommended, Rating, Price, Experience [P2 - Post-MVP]
- **REQ-022-017**: System MUST limit patient provider selection to maximum 5 providers per quote request [P2 - Post-MVP]
- **REQ-022-018**: System MUST display provider card with name, location, rating, starting price, before/after photo [P2 - Post-MVP]
- **REQ-022-019**: System MUST support infinite scroll pagination for patient mobile app (10 results per page) [P2 - Post-MVP]
- **REQ-022-020**: System MUST prioritize admin-featured providers in "Recommended" sort order [P2 - Post-MVP]

### Security & Privacy Requirements

- **REQ-022-021**: System MUST require valid JWT authentication for all search endpoints
- **REQ-022-022**: System MUST enforce role-based access control (admin-only for patient/provider search)
- **REQ-022-023**: System MUST log all admin searches with user ID, timestamp, search terms, and result count
- **REQ-022-024**: System MUST sanitize all search inputs to prevent SQL injection and XSS attacks
- **REQ-022-025**: System MUST rate-limit search queries to 100 per hour per user
- **REQ-022-026**: System MUST anonymize patient names in search results if patient has not confirmed payment
- **REQ-022-027**: System MUST encrypt audit logs containing patient/provider search history

### Performance Requirements

- **REQ-022-028**: System MUST create database indexes on all searchable fields for query optimization
- **REQ-022-029**: System MUST cache autocomplete results for 5 minutes to reduce database load
- **REQ-022-030**: System MUST handle 100 concurrent admin searches without performance degradation
- **REQ-022-031**: System MUST handle 500 concurrent patient searches without performance degradation [P2 - Post-MVP]
- **REQ-022-032**: System MUST complete database queries in under 100ms for indexed searches

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
| 2026-04-03 | 2.0 | Major overhaul: Screen Specifications fully rewritten with three-tenant structure (Patient/Provider/Admin); master reference table added (Module → FR → Screen); Provider Platform screens added (PR-01 through PR-06) to match P1-MVP scope; control behaviors mini-tables added to all screen specs (search inactive/active, filter inactive/active, reset filter); maintenance convention note added; Executive Summary and Module Scope updated; Functional Requirements Summary expanded with Provider and Patient P1 REQs | Claude AI |

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
**Last Updated**: 2026-04-03
