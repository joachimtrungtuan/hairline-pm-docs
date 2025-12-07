# Product Requirements Document: Travel Booking Integration

**Module**: P-04: Travel & Logistics | A-04: Travel Management | S-04: Travel API Gateway
**Feature Branch**: `fr008-travel-booking-integration`
**Created**: 2025-11-10
**Status**: Draft | ✅ Pending Approval | ✅ Verified & Approved
**Source**: FR-008 from system-prd.md; cross-checked with transcriptions (HairlineApp-Part1/2, AdminPlatform Part1)

---

## Executive Summary

Enable patients to search and book travel (flights and hotels) related to their procedure directly within the platform, surface real-time pricing to inform scheduling decisions, and consolidate all confirmed travel into a unified itinerary. This module also tracks platform commissions on completed bookings and provides basic admin oversight for travel settings.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-04)**: Flight search, hotel selection, booking initiation, itinerary view
- **Provider Platform (PR-XX)**: No direct booking; can recommend hotels and share travel guidance
- **Admin Platform (A-04)**: Configure travel settings, manage provider-recommended hotels, monitor commissions
- **Shared Services (S-04)**: Travel API Gateway for external provider aggregation and pricing

### Multi-Tenant Breakdown

**Patient Platform (P-04)**:

- Search roundtrip flights by origin, destination, and date range
- View real-time price ranges during inquiry date selection (cheapest and average)
- Select provider-recommended hotels and proceed to booking
- Review and manage unified travel itinerary (flights, hotel, transport when available)

**Provider Platform (PR-XX)**:

- Maintain curated list of recommended hotels per clinic/location
- Provide travel guidance (arrival windows, airport preferences) surfaced to patients
- View read-only itinerary details post-booking for coordination (no access to payment data)

**Admin Platform (A-04)**:

- Configure preferred flight and hotel providers
- Set commission parameters and reporting views for travel bookings
- Manage system-wide travel settings (search constraints, supported markets)

**Shared Services (S-04)**:

- Aggregates external APIs (flight, hotel) behind a stable contract
- Normalizes pricing/availability responses and handles rate limiting and caching
- Sends booking confirmations and updates itinerary records

### Communication Structure

**In Scope**:

- Patient-facing flight search and hotel selection
- Real-time pricing preview during inquiry
- Booking confirmations (email + in-app)
- Itinerary aggregation (flights + hotels)

**Out of Scope**:

- Direct SMS notifications (handled by S-03 Notification Service; **no SMS travel notifications are sent in MVP and this channel is a future enhancement owned by S-03/FR-020/FR-030**)
- In-app messaging features (covered by communication modules)
- Real-time airport transport booking in MVP (future enhancement)

### Entry Points

Patients access travel via the mobile app after selecting procedure dates (inquiry/booking flows). Admins access travel settings via the Admin console. The feature becomes available when a clinic location is chosen and dates are selected.

- Patient-initiated via mobile app flow
- Admin-managed via Admin Platform settings

---

## Business Workflows

### Main Flow: Flight Search and Booking

**Actors**: Patient, System, External Flight Provider
**Trigger**: Patient selects location and tentative dates during inquiry or booking
**Outcome**: Flight booked and confirmation added to itinerary

**Steps**:

1. Patient enters origin, destination (clinic city/airport), and date range
2. System validates inputs and queries external flight provider for pricing/availability
3. System displays options with cheapest and average price indicators
4. Patient selects flight option and proceeds to booking confirmation
5. System confirms booking with provider and records booking details
6. System sends confirmation to patient and updates unified itinerary

### Alternative Flows

**A1: Multiple Date Options**:

- **Trigger**: Patient explores different date ranges to compare price ranges
- **Steps**:
  1. Patient adjusts date range
  2. System refreshes price preview and search results
- **Outcome**: Patient selects dates with favorable pricing

**A2: Recommended Hotel Selection**:

- **Trigger**: Patient opts to choose a hotel from provider-recommended list
- **Steps**:
  1. System presents curated hotel options with key amenities
  2. Patient selects a hotel and proceeds to booking
- **Outcome**: Hotel booked and added to itinerary

**B1: Price Changed During Checkout**:

- **Trigger**: External provider returns updated price on confirmation
- **Steps**:
  1. System displays updated price and requests patient confirmation
  2. Patient confirms or selects a different option
- **Outcome**: Booking completes with acknowledged price or patient reselects

**B2: No Availability**:

- **Trigger**: Search returns no available flights/hotels for selected dates
- **Steps**:
  1. System prompts patient to adjust dates or filters
  2. Patient modifies inputs and retries search
- **Outcome**: Alternative dates/options presented or patient exits flow

---

## Screen Specifications

  Include web pages (provider/admin) and mobile screens (patient)

### Screen 1: Flight Search & Results

**Purpose**: Allow patients to search for roundtrip flights and view real-time pricing to inform date selection and booking

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Origin Airport | select | Yes | Departure airport (user’s origin) | Must be valid IATA airport code |
| Destination | select | Yes | Clinic city/airport | Must match clinic location options |
| Depart Date | date | Yes | Outbound date | Cannot be in the past |
| Return Date | date | Yes | Inbound date | Must be after Depart Date |
| Passengers | number | Yes | Number of passengers | 1–6 |

**Business Rules**:

- Show cheapest and average price indicators for selected date range
- Disable Search until required inputs are valid
- Persist last search to help patients compare dates
- Do not display any payment details or PII from external providers

**Notes**:

- Use autocomplete for airport selection
- Display loading and empty states with clear guidance
- Provide quick date range adjustments (±3 days) for price comparison

---

### Screen 2: Hotel Selection

**Purpose**: Allow patients to select a hotel from provider-recommended options and proceed to booking

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Check-in Date | date | Yes | Hotel arrival date | Cannot be in the past |
| Check-out Date | date | Yes | Hotel departure date | Must be after Check-in |
| Guests | number | Yes | Number of guests | 1–4 |
| Hotel Option | select | Yes | Recommended hotel choice | Must be from curated list |

**Business Rules**:

- Only display hotels curated by provider/admin for the destination
- Show total estimated price for selected dates before booking

**Notes**:

- Include amenity badges (breakfast, transport, rating)

---

---

## Business Rules

### General Module Rules

- All prices shown during search are estimates and may change at confirmation
- All times displayed in the user's local timezone and destination timezone where relevant
- One active itinerary per appointment; edits create new entries and mark old ones superseded

### Data & Privacy Rules

- Patient PII is never shared with travel providers beyond booking requirements displayed to the user
- No payment card data is stored by the platform; bookings handled by compliant providers
- Booking confirmations and itinerary data retained for 2 years for support and accounting
- All booking lifecycle events logged with timestamp and user ID
- Adhere to GDPR/HIPAA-equivalent standards; explicit consent where required

### Admin Editability Rules

**Editable by Admin**:

- Preferred providers for flights/hotels and commission ranges
- Curated hotel lists per clinic/destination
- Regional availability of travel search features

**Fixed in Codebase (Not Editable)**:

- Timezone handling rules and date validation constraints
- Itinerary structure and event logging requirements
- Maximum passengers per booking (policy-limited)

**Configurable with Restrictions**:

- Admin can enable/disable travel providers but cannot edit external provider policies

### Payment & Billing Rules *(if applicable)*

- Payments for travel occur on the external provider’s side; platform records confirmation only
- Refunds and changes follow the external provider’s policy; platform reflects status updates
- Commissions are calculated on completed bookings and reported monthly
- Prices displayed in patient’s selected currency where supported by provider

---

## Success Criteria

### Patient Experience Metrics

- **SC-001**: 90% of patients can complete a flight search with price preview in under 60 seconds
- **SC-002**: 85% of patients successfully complete a hotel selection and booking without errors
- **SC-003**: 95% of patients see a combined itinerary within 10 seconds after confirmation

### Provider Efficiency Metrics

- **SC-004**: Providers spend 0 minutes managing travel bookings (self-serve by patients) while seeing itinerary context
- **SC-005**: Support tickets about travel logistics reduced by 40% after release
- **SC-006**: 90% of provider-recommended hotel lists have at least 3 options per destination

### Admin Management Metrics

- **SC-007**: Admins can view monthly travel commission totals with 100% booking reconciliation
- **SC-008**: 100% of travel booking confirmations captured and stored against itineraries
- **SC-009**: 100% of travel lifecycle events are logged for audit

### System Performance Metrics

- **SC-010**: Flight search results display within 3 seconds for 95% of queries
- **SC-011**: Supports 500 concurrent travel searches without degraded user experience
- **SC-012**: 99.9% uptime for travel search and itinerary features
- **SC-013**: Zero loss of confirmed booking records and confirmations

### Business Impact Metrics

- **SC-014**: Travel commission revenue achieves £X per month within 3 months of launch (set target in planning)
- **SC-015**: 30% of inquiries progress to booking after travel cost preview
- **SC-016**: 80% of completed appointments have an attached itinerary within 6 months

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- **FR-001 / Module P-01**: Requires patient authentication (P-01: Auth & Profile Management)
  - **Why needed**: Only verified patients can search and book travel
  - **Integration point**: Uses patient profile (home airport, preferences)

- **FR-006 / Module P-03**: Booking & Scheduling linkage
  - **Why needed**: Travel dates depend on procedure dates; itinerary ties to appointment
  - **Integration point**: Reads selected dates; posts itinerary to booking details

- **FR-XXX / Module S-03**: Notification Service
  - **Why needed**: Send confirmations and updates
  - **Integration point**: Sends email/in-app confirmations upon booking

### External Dependencies (APIs, Services)

- **Flight Provider API (e.g., Amadeus or Skyscanner)**
  - **Purpose**: Search pricing and book flights
  - **Integration**: Via S-04 Travel API Gateway
  - **Failure handling**: Show fallback message and allow date adjustments/retry

- **Hotel Provider API (e.g., Booking.com or Expedia)**
  - **Purpose**: Search curated hotels and book stays
  - **Integration**: Via S-04 Travel API Gateway
  - **Failure handling**: Suggest alternative hotels or dates; allow retry

### Data Dependencies

- **Clinic Location Details**
  - **Why needed**: Determines destination airport/city
  - **Source**: Provider profile (PR-01)

- **Procedure Dates (selected or tentative)**
  - **Why needed**: Anchors flight and hotel date ranges
  - **Source**: Booking & Scheduling (P-03)

---

## Assumptions

### User Behavior Assumptions

- **Assumption 1**: Patients will compare date options if prices vary significantly
- **Assumption 2**: Patients expect confirmations immediately after booking

### Operational Assumptions

- External providers offer stable search/booking endpoints with predictable quotas
- Commission statements for travel are available for reconciliation monthly

### Scope Assumptions

- Airport transport booking is excluded from MVP (informational guidance only)
- One travel itinerary per appointment; updates append entries rather than overwrite
- **Assumption 3**: [Usage context - e.g., "Majority of patients will submit quote requests from mobile devices"]

### Technology Assumptions

- **Assumption 1**: [Platform/device - e.g., "Patients use smartphones with camera capabilities"]
- **Assumption 2**: [Browser/OS - e.g., "Provider web app accessed via modern browsers (Chrome, Safari, Firefox - last 2 versions)"]
- **Assumption 3**: [Connectivity - e.g., "Patients have intermittent internet connectivity (support offline mode)"]
- **Assumption 4**: [Infrastructure - e.g., "Cloud storage available for uploaded medical images"]

### Business Process Assumptions

- **Assumption 1**: [Workflow - e.g., "Providers check quote requests at least twice daily during business hours"]
- **Assumption 2**: [Organizational - e.g., "Providers have dedicated staff to handle quote request responses"]
- **Assumption 3**: [Business rule - e.g., "Quote prices provided by providers are binding for 30 days"]
- **Assumption 4**: [Process - e.g., "Admin approval not required for standard quote requests under $10,000"]

---

## Implementation Notes

### Technical Considerations

  Avoid specifying frameworks/languages - focus on architectural needs

- **Architecture**: [High-level structure - e.g., "Requires asynchronous processing for image uploads to prevent blocking"]
- **Technology**: [Considerations - e.g., "Image processing should support HEIC/JPEG formats common on smartphones"]
- **Performance**: [Requirements - e.g., "Image uploads should support resumable transfers for unreliable connections"]
- **Storage**: [Needs - e.g., "Medical images require long-term archival storage with retrieval SLA of <5 seconds"]

### Integration Points

- **Integration 1**: [Connection - e.g., "Patient app sends quote requests to Provider API via REST"]
  - **Data format**: [e.g., "JSON payload with patient ID, procedure codes, image URLs"]
  - **Authentication**: [e.g., "OAuth 2.0 bearer tokens"]
  - **Error handling**: [e.g., "Retry with exponential backoff on 5xx errors"]

- **Integration 2**: [Another connection - e.g., "Admin dashboard polls quote request status from shared database"]
  - **Data format**: [Format]
  - **Authentication**: [Method]
  - **Error handling**: [Approach]

### Scalability Considerations

- **Current scale**: [Baseline - e.g., "Expected 500 quote requests per day at launch"]
- **Growth projection**: [Future - e.g., "Plan for 5,000 requests per day within 12 months"]
- **Peak load**: [Spikes - e.g., "Handle 10x normal load during promotional campaigns"]
- **Data volume**: [Storage - e.g., "Expect 50GB of medical images per month"]
- **Scaling strategy**: [Approach - e.g., "Horizontal scaling of API servers, CDN for image delivery"]

### Security Considerations

- **Authentication**: [Requirements - e.g., "Multi-factor authentication required for provider access to patient medical images"]
- **Authorization**: [Access control - e.g., "Role-based access: patients view own data, providers view paid requests only, admins view all"]
- **Encryption**: [Data protection - e.g., "All patient data encrypted in transit (TLS 1.3) and at rest (AES-256)"]
- **Audit trail**: [Logging - e.g., "Log all access to patient medical images with timestamp, user, and IP address"]
- **Threat mitigation**: [Security measures - e.g., "Rate limiting on API endpoints to prevent abuse (max 100 requests/hour/user)"]
- **Compliance**: [Standards - e.g., "HIPAA-compliant data handling for U.S. patients, GDPR for EU patients"]

---

## User Scenarios & Testing

### User Story 1 - Search Flights with Price Preview (Priority: P1)

Patients can search for flights tied to their selected procedure dates and see cheapest and average prices to make informed scheduling choices.

**Why this priority**: Directly supports inquiry date selection and improves conversion by reducing travel uncertainty.

**Independent Test**: Perform a search with a valid origin/destination and date range; verify price preview appears and results can be browsed.

**Acceptance Scenarios**:

1. Given valid origin/destination and dates, When patient searches, Then system shows cheapest and average price indicators.
2. Given a search result list, When patient changes date range by ±3 days, Then system refreshes results and price preview.
3. Given results, When no availability found, Then system clearly prompts for alternative dates.

---

### User Story 2 - Book Recommended Hotel (Priority: P2)

Patients can select from a provider-recommended hotel list and complete a booking for their stay.

**Why this priority**: Ensures quality and proximity while generating commission revenue.

**Independent Test**: Choose clinic location and dates; select a recommended hotel; verify booking confirmation and itinerary update.

**Acceptance Scenarios**:

1. Given a curated hotel list, When patient selects dates and a hotel, Then total cost is shown before confirmation.
2. Given a pending booking, When confirmation is received, Then system sends a confirmation and updates itinerary.

---

### User Story 3 - Unified Itinerary Management (Priority: P3)

Patients can view all confirmed travel (flights and hotels) in a single itinerary linked to their appointment.

**Why this priority**: Reduces confusion and support burden by centralizing travel details.

**Independent Test**: Complete a flight and hotel booking; verify both appear in itinerary with dates aligned to procedure.

**Acceptance Scenarios**:

1. Given confirmed bookings, When patient opens itinerary, Then flight and hotel details are displayed with dates and references.

---

### Edge Cases

- Booking price changes at confirmation: system must request re-confirmation.
- Provider-recommended hotel becomes unavailable: show alternates or prompt date adjustment.
- Search quota exceeded or provider timeout: display friendly retry guidance.

---

## Functional Requirements Summary

  Each requirement should be testable and traceable to user stories/workflows

### Core Requirements (FR-008)

- **REQ-008-001**: The system MUST integrate with a flight booking provider to search and book flights.
- **REQ-008-002**: The system MUST integrate with a hotel booking provider to search curated hotels and book stays.
- **REQ-008-003**: Patients MUST be able to search flights by origin/destination and date range with real-time pricing.
- **REQ-008-004**: Patients MUST be able to select and book provider-recommended hotels.
- **REQ-008-005**: The system MUST aggregate all confirmed bookings into a unified itinerary per appointment.

### Price Preview Requirements

- **REQ-008-006**: During inquiry date selection, the system MUST display estimated flight costs (cheapest and average) for the chosen date range.
- **REQ-008-007**: The system MUST refresh price preview when dates change.
- **REQ-008-008**: The system MUST clearly indicate when prices are estimates vs final at checkout.

### Confirmation & Notifications

- **REQ-008-009**: The system MUST send booking confirmations for flights and hotels (in-app and email).
- **REQ-008-010**: The system MUST reflect booking changes (cancellations/changes) in the itinerary.

### Commission Tracking

- **REQ-008-011**: The system MUST track platform commissions on completed bookings separately from procedure commissions.
- **REQ-008-012**: The system SHOULD support commission ranges: flights (3–5%), hotels (10–15%), configurable by admin.

### Security & Privacy

- **REQ-008-013**: The system MUST avoid storing any payment card data; payments occur via external, compliant providers.
- **REQ-008-014**: The system MUST log all booking events for audit (who, when, what changed).

### Admin & Config

- **REQ-008-015**: Admins MUST be able to configure preferred providers (flight/hotel) and commission parameters.
- **REQ-008-016**: Admins MUST be able to manage provider-recommended hotel lists.

### [NEEDS CLARIFICATION]

- **REQ-008-017**: Preferred flight provider? [NEEDS CLARIFICATION: Amadeus vs Skyscanner]
- **REQ-008-018**: Preferred hotel provider? [NEEDS CLARIFICATION: Booking.com vs Expedia]
- **REQ-008-019**: Booking payment flow? [NEEDS CLARIFICATION: In-app redirect vs deep link vs voucher]

---

## Key Entities

  This helps understand what data this feature manages

- **Entity 1 - FlightSearch**: Patient-initiated search context for flights
  - **Key attributes**: origin, destination, date range, passenger count, price preview (cheapest, average)
  - **Relationships**: Linked to appointment inquiry context; produces FlightBooking on confirmation

- **Entity 2 - FlightBooking**: Confirmed flight details
  - **Key attributes**: airline, flight numbers, depart/return times, booking reference, status
  - **Relationships**: Included in Itinerary; associated with commission record

- **Entity 3 - HotelBooking**: Confirmed hotel reservation details
  - **Key attributes**: hotel name, check-in/out dates, room type, booking reference, total price
  - **Relationships**: Included in Itinerary; associated with commission record

- **Entity 4 - Itinerary**: Aggregated view of travel for an appointment
  - **Key attributes**: appointment reference, items (flights, hotel), confirmations, updates
  - **Relationships**: One itinerary per appointment; composed of booking items

- **Entity 5 - CommissionRecord**: Platform earnings for bookings
  - **Key attributes**: booking ref, type (flight/hotel), base amount, commission rate, commission amount, posted date
  - **Relationships**: Linked to FlightBooking or HotelBooking; visible in admin reporting

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-10 | 1.0 | Initial PRD creation | AI |
| 2025-11-10 | 1.1 | Added clarifications and success criteria | AI |

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
**Last Updated**: 2025-11-03
