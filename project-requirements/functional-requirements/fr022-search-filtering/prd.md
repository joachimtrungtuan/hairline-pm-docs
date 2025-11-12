# Product Requirements Document: [FEATURE NAME]

**Module**: [Module codes - e.g., P-05: Aftercare & Progress Monitoring | PR-04: Aftercare Participation]
**Feature Branch**: `fr[###]-[module-name]`
**Created**: [DATE]
**Status**: Draft | ✅ Pending Approval | ✅ Verified & Approved
**Source**: [Source reference - e.g., FR-011 from system-prd.md, User request, Client transcription]

---

## Executive Summary

<!--
  ACTION REQUIRED: Provide clear module purpose and scope
  - What is the primary purpose of this feature/module?
  - What problem does it solve for users?
  - What value does it deliver to the business?
-->

[Clear description of module purpose and scope]

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-XX)**: [Patient-facing capability summary]
- **Provider Platform (PR-XX)**: [Provider-facing capability summary]
- **Admin Platform (A-XX)**: [Admin oversight/configuration summary]
- **Shared Services (S-XX)**: [Shared services used by this module]

### Multi-Tenant Breakdown

**Patient Platform (P-XX)**:

- [What functionality exists in patient mobile app]
- [What data patients can view/edit]
- [What actions patients can perform]

**Provider Platform (PR-XX)**:

- [What functionality exists in provider web app]
- [What data providers can view/edit]
- [What actions providers can perform]

**Admin Platform (A-XX)**:

- [What functionality exists in admin web app]
- [What oversight/management capabilities admins have]
- [What configuration options admins control]

**Shared Services (S-XX)**:

- [Any shared/reusable backend services this feature requires]
- [APIs that serve multiple tenants]
- [Background processing or scheduled jobs]

### Communication Structure

**In Scope**:

- [Explicit list of communication features INCLUDED in this module]
- [e.g., "Email notifications for aftercare task completion"]
- [e.g., "In-app messages between patient and provider"]

**Out of Scope**:

- [Explicit list of communication features NOT included in this module]
- [e.g., "Video calls between patient and provider (handled by separate module)"]
- [e.g., "SMS notifications (handled by S-03: Notification Service)"]

### Entry Points

[Describe how users/systems access this feature and what triggers its availability]

- [e.g., "Patient-initiated via mobile app flow"]
- [e.g., "Provider opens dashboard module"]
- [e.g., "Admin publishes configuration to activate feature"]

---

## Business Workflows

### Main Flow: [Workflow Name]

**Actors**: [List all involved parties - e.g., Patient, Provider, Admin, System]
**Trigger**: [What initiates this workflow - e.g., "Patient taps 'Request Quote' button"]
**Outcome**: [Expected result - e.g., "Quote request submitted and provider notified"]

**Steps**:

1. [Actor] [performs action - e.g., "Patient enters treatment details"]
2. System [response - e.g., "validates inputs and checks for required fields"]
3. [Actor] [next action - e.g., "Patient reviews and confirms submission"]
4. System [processes - e.g., "creates quote request record and notifies provider"]
5. [Continue step-by-step until workflow completes]

### Alternative Flows

<!--
  ACTION REQUIRED: Document all alternative paths and variations
  Use naming convention: A1, A2, B1, B2, etc.
  A = Alternative happy path
  B = Error/exception path
-->

**A1: [Alternative scenario name - e.g., "Patient selects multiple procedures"]**

- **Trigger**: [When this alternative occurs]
- **Steps**:
  1. [Modified flow from main path]
  2. [How it differs from main flow]
- **Outcome**: [How this path resolves]

**A2: [Another alternative - e.g., "Provider requests clarification"]**

- **Trigger**: [When this alternative occurs]
- **Steps**:
  1. [Modified flow]
- **Outcome**: [Result]

**B1: [Error scenario name - e.g., "Required field missing"]**

- **Trigger**: [What causes this error]
- **Steps**:
  1. System [error handling - e.g., "displays validation message"]
  2. [Actor] [recovery action]
- **Outcome**: [How system recovers or how user can retry]

**B2: [Another error scenario - e.g., "Network connection lost"]**

- **Trigger**: [Error condition]
- **Steps**: [Error handling flow]
- **Outcome**: [Recovery path]

[Add more alternative flows as needed: A3, A4, B3, B4, etc.]

---

## Screen Specifications

<!--
  ACTION REQUIRED: Document all screens/views in this module
  Include web pages (provider/admin) and mobile screens (patient)
-->

### Screen 1: [Screen Name - e.g., "Quote Request Form"]

**Purpose**: [What this screen accomplishes - e.g., "Allows patient to submit treatment quote request"]

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| [field1] | text/number/date/select/checkbox | Yes/No | [Purpose and usage] | [e.g., "Max 500 chars"] |
| [field2] | [type] | Yes/No | [Purpose] | [Validation] |
| [field3] | [type] | Yes/No | [Purpose] | [Validation] |

**Business Rules**:

- [Specific rule governing screen behavior - e.g., "Procedure field pre-populated if patient has prior consultation"]
- [Validation rule - e.g., "At least one procedure must be selected"]
- [State change rule - e.g., "Submit button disabled until all required fields complete"]
- [Data privacy rule - e.g., "Provider identity hidden until payment confirmed"]

**Notes**:

- [Implementation guidance - e.g., "Use autocomplete for clinic selection"]
- [UX considerations - e.g., "Show progress indicator for multi-step form"]
- [Technical constraints - e.g., "Maximum 5 procedure images uploadable"]

---

### Screen 2: [Screen Name]

**Purpose**: [What this screen accomplishes]

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| [field] | [type] | Yes/No | [Purpose] | [Validation] |

**Business Rules**:

- [Rule 1]
- [Rule 2]

**Notes**:

- [Note 1]

---

[Repeat for all screens in this module]

---

## Business Rules

### General Module Rules

<!--
  ACTION REQUIRED: Define overarching rules that apply to the entire module
-->

- **Rule 1**: [General rule applicable to entire module - e.g., "All quote requests expire after 30 days if no provider response"]
- **Rule 2**: [Another general rule - e.g., "Maximum 3 active quote requests per patient at any time"]
- **Rule 3**: [Cross-cutting concern - e.g., "All timestamps displayed in user's local timezone"]

### Data & Privacy Rules

<!--
  ACTION REQUIRED: Define data access restrictions and privacy requirements
  Reference Principle II from constitution: Medical Data Privacy & Security
-->

- **Privacy Rule 1**: [Data access restriction - e.g., "Provider identity anonymized until patient confirms payment"]
- **Privacy Rule 2**: [Encryption requirement - e.g., "Patient medical images encrypted at rest using AES-256"]
- **Privacy Rule 3**: [Data retention - e.g., "Quote requests archived after 90 days, permanently deleted after 2 years"]
- **Audit Rule**: [Logging requirement - e.g., "All access to patient medical data must be logged with timestamp and user ID"]
- **HIPAA/GDPR**: [Compliance notes if applicable - e.g., "Patient consent required before sharing data with provider"]

### Admin Editability Rules

<!--
  ACTION REQUIRED: Explicitly state what admins CAN and CANNOT edit
  Reference Principle VIII from constitution: Admin-Editable Content
-->

**Editable by Admin**:

- [What admins can modify - e.g., "Quote expiration period (default 30 days, range 7-90 days)"]
- [Configuration options - e.g., "Maximum active quote requests per patient (default 3, range 1-10)"]
- [Content management - e.g., "Procedure catalog and pricing templates"]

**Fixed in Codebase (Not Editable)**:

- [What is hard-coded - e.g., "Encryption algorithms (AES-256)"]
- [Security parameters - e.g., "Password requirements (min 8 chars, 1 uppercase, 1 number)"]
- [System limits - e.g., "Maximum image upload size (10MB per file)"]

**Configurable with Restrictions**:

- [Semi-editable items - e.g., "Admin can disable certain payment methods but cannot modify payment gateway integration"]

### Payment & Billing Rules *(if applicable)*

<!--
  ACTION REQUIRED: Define payment-related rules if this module involves transactions
  Delete this section if not applicable
-->

- **Payment Rule 1**: [Payment flow rule - e.g., "Payment required before provider contact information revealed"]
- **Payment Rule 2**: [Refund policy - e.g., "Full refund if provider doesn't respond within 48 hours"]
- **Billing Rule 1**: [Invoicing rule - e.g., "Invoice generated immediately upon successful payment"]
- **Currency Rule**: [Multi-currency handling - e.g., "Prices displayed in patient's selected currency"]

---

## Success Criteria

<!--
  ACTION REQUIRED: Define measurable, technology-agnostic success metrics
  These should be testable without knowing implementation details
-->

### Patient Experience Metrics

- **SC-001**: [Measurable patient-facing outcome - e.g., "Patients can submit a complete quote request in under 3 minutes"]
- **SC-002**: [User satisfaction metric - e.g., "90% of patients successfully complete quote request on first attempt without errors"]
- **SC-003**: [Engagement metric - e.g., "Patients receive initial provider response within 24 hours for 80% of requests"]

### Provider Efficiency Metrics

- **SC-004**: [Provider workflow improvement - e.g., "Providers can review and respond to quote requests in under 2 minutes per request"]
- **SC-005**: [Time savings metric - e.g., "Average time to quote generation reduced by 50% compared to manual process"]
- **SC-006**: [Productivity metric - e.g., "Providers handle 30% more quote requests per day"]

### Admin Management Metrics

- **SC-007**: [Administrative efficiency gain - e.g., "Admins can monitor all active quote requests across all providers in real-time"]
- **SC-008**: [Support reduction - e.g., "Support tickets related to quote request issues reduced by 60%"]
- **SC-009**: [Oversight metric - e.g., "100% of quote request lifecycle events logged for audit purposes"]

### System Performance Metrics

- **SC-010**: [Response time target - e.g., "Quote request submission completes within 2 seconds for 95% of requests"]
- **SC-011**: [Scalability target - e.g., "System supports 1000 concurrent quote request submissions without degradation"]
- **SC-012**: [Reliability target - e.g., "99.9% uptime for quote request functionality"]
- **SC-013**: [Data integrity - e.g., "Zero data loss for submitted quote requests"]

### Business Impact Metrics

- **SC-014**: [Revenue impact - e.g., "Quote request conversion rate to booked procedures increases by 25%"]
- **SC-015**: [User engagement - e.g., "70% of patients who request quotes proceed to booking within 7 days"]
- **SC-016**: [Market expansion - e.g., "Quote request feature enables entry into 5 new geographic markets"]

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

<!--
  ACTION REQUIRED: List all dependencies on other modules in this system
  Use module codes from constitution (P-01, PR-02, A-03, etc.)
-->

- **FR-XXX / Module P-01**: [Dependency description - e.g., "Requires patient authentication from P-01: Auth & Profile Management"]
  - **Why needed**: [Reason - e.g., "Cannot submit quote request without verified patient account"]
  - **Integration point**: [How they connect - e.g., "Uses patient profile data to pre-fill form fields"]

- **FR-YYY / Module S-03**: [Another dependency - e.g., "Requires S-03: Notification Service for provider alerts"]
  - **Why needed**: [Reason]
  - **Integration point**: [Connection]

### External Dependencies (APIs, Services)

<!--
  ACTION REQUIRED: List all third-party services, APIs, or external systems
-->

- **External Service 1**: [Service name - e.g., "Stripe Payment API"]
  - **Purpose**: [What it does - e.g., "Processes quote request payment transactions"]
  - **Integration**: [How integrated - e.g., "RESTful API calls for payment processing"]
  - **Failure handling**: [What happens if unavailable - e.g., "Queue payment for retry, notify user of delay"]

- **External Service 2**: [Another service - e.g., "Google Maps API"]
  - **Purpose**: [Usage]
  - **Integration**: [Method]
  - **Failure handling**: [Fallback]

### Data Dependencies

<!--
  ACTION REQUIRED: List data that must exist for this feature to function
-->

- **Entity 1**: [Required data - e.g., "Active provider profiles with accepted service areas"]
  - **Why needed**: [Reason - e.g., "Cannot route quote requests without knowing provider service coverage"]
  - **Source**: [Where it comes from - e.g., "Provider onboarding module (PR-01)"]

- **State 2**: [System state prerequisite - e.g., "Procedure catalog with pricing information"]
  - **Why needed**: [Reason]
  - **Source**: [Origin]

---

## Assumptions

### User Behavior Assumptions

<!--
  ACTION REQUIRED: Document assumptions about how users will interact with the system
-->

- **Assumption 1**: [User behavior - e.g., "Patients have access to photos of their current hair condition"]
- **Assumption 2**: [User pattern - e.g., "Patients will upload photos immediately rather than saving draft requests"]
- **Assumption 3**: [Usage context - e.g., "Majority of patients will submit quote requests from mobile devices"]

### Technology Assumptions

<!--
  ACTION REQUIRED: Document platform, browser, device, connectivity assumptions
-->

- **Assumption 1**: [Platform/device - e.g., "Patients use smartphones with camera capabilities"]
- **Assumption 2**: [Browser/OS - e.g., "Provider web app accessed via modern browsers (Chrome, Safari, Firefox - last 2 versions)"]
- **Assumption 3**: [Connectivity - e.g., "Patients have intermittent internet connectivity (support offline mode)"]
- **Assumption 4**: [Infrastructure - e.g., "Cloud storage available for uploaded medical images"]

### Business Process Assumptions

<!--
  ACTION REQUIRED: Document workflow and organizational assumptions
-->

- **Assumption 1**: [Workflow - e.g., "Providers check quote requests at least twice daily during business hours"]
- **Assumption 2**: [Organizational - e.g., "Providers have dedicated staff to handle quote request responses"]
- **Assumption 3**: [Business rule - e.g., "Quote prices provided by providers are binding for 30 days"]
- **Assumption 4**: [Process - e.g., "Admin approval not required for standard quote requests under $10,000"]

---

## Implementation Notes

### Technical Considerations

<!--
  ACTION REQUIRED: Provide technical guidance (but NOT technology prescriptions)
  Avoid specifying frameworks/languages - focus on architectural needs
-->

- **Architecture**: [High-level structure - e.g., "Requires asynchronous processing for image uploads to prevent blocking"]
- **Technology**: [Considerations - e.g., "Image processing should support HEIC/JPEG formats common on smartphones"]
- **Performance**: [Requirements - e.g., "Image uploads should support resumable transfers for unreliable connections"]
- **Storage**: [Needs - e.g., "Medical images require long-term archival storage with retrieval SLA of <5 seconds"]

### Integration Points

<!--
  ACTION REQUIRED: Describe how this module integrates with other systems
-->

- **Integration 1**: [Connection - e.g., "Patient app sends quote requests to Provider API via REST"]
  - **Data format**: [e.g., "JSON payload with patient ID, procedure codes, image URLs"]
  - **Authentication**: [e.g., "OAuth 2.0 bearer tokens"]
  - **Error handling**: [e.g., "Retry with exponential backoff on 5xx errors"]

- **Integration 2**: [Another connection - e.g., "Admin dashboard polls quote request status from shared database"]
  - **Data format**: [Format]
  - **Authentication**: [Method]
  - **Error handling**: [Approach]

### Scalability Considerations

<!--
  ACTION REQUIRED: Address expected load and growth
-->

- **Current scale**: [Baseline - e.g., "Expected 500 quote requests per day at launch"]
- **Growth projection**: [Future - e.g., "Plan for 5,000 requests per day within 12 months"]
- **Peak load**: [Spikes - e.g., "Handle 10x normal load during promotional campaigns"]
- **Data volume**: [Storage - e.g., "Expect 50GB of medical images per month"]
- **Scaling strategy**: [Approach - e.g., "Horizontal scaling of API servers, CDN for image delivery"]

### Security Considerations

<!--
  ACTION REQUIRED: Document security requirements and threat mitigations
  Reference Principle II: Medical Data Privacy & Security
-->

- **Authentication**: [Requirements - e.g., "Multi-factor authentication required for provider access to patient medical images"]
- **Authorization**: [Access control - e.g., "Role-based access: patients view own data, providers view paid requests only, admins view all"]
- **Encryption**: [Data protection - e.g., "All patient data encrypted in transit (TLS 1.3) and at rest (AES-256)"]
- **Audit trail**: [Logging - e.g., "Log all access to patient medical images with timestamp, user, and IP address"]
- **Threat mitigation**: [Security measures - e.g., "Rate limiting on API endpoints to prevent abuse (max 100 requests/hour/user)"]
- **Compliance**: [Standards - e.g., "HIPAA-compliant data handling for U.S. patients, GDPR for EU patients"]

---

## User Scenarios & Testing

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality.
-->

### User Story 1 - [Brief Title] (Priority: P1)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently - e.g., "Can be fully tested by submitting a quote request and verifying provider receives notification"]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]
3. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 2 - [Brief Title] (Priority: P2)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 3 - [Brief Title] (Priority: P3)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

[Add more user stories as needed, each with assigned priority]

### Edge Cases

<!--
  ACTION REQUIRED: Document boundary conditions and error scenarios
-->

- What happens when [boundary condition - e.g., "patient uploads 100 images"]?
- How does system handle [error scenario - e.g., "provider doesn't respond within 7 days"]?
- What occurs if [edge case - e.g., "patient deletes account while quote request active"]?
- How to manage [concurrency - e.g., "two providers respond simultaneously to same request"]?

---

## Functional Requirements Summary

<!--
  ACTION REQUIRED: Consolidate all MUST-have requirements from above sections
  Each requirement should be testable and traceable to user stories/workflows
-->

### Core Requirements

- **FR-001**: System MUST [specific capability derived from workflows - e.g., "allow patients to submit quote requests with medical images"]
- **FR-002**: System MUST [capability - e.g., "notify providers within 1 minute of quote request submission"]
- **FR-003**: Users MUST be able to [key interaction - e.g., "track quote request status in real-time"]
- **FR-004**: System MUST [data requirement - e.g., "persist quote request data for minimum 2 years"]
- **FR-005**: System MUST [behavior - e.g., "log all quote request lifecycle events for audit trail"]

### Data Requirements

- **FR-006**: System MUST [entity management - e.g., "maintain quote request history for each patient"]
- **FR-007**: System MUST [relationship - e.g., "link quote requests to specific procedures from catalog"]

### Security & Privacy Requirements

- **FR-008**: System MUST [security - e.g., "anonymize provider identity until payment confirmed"]
- **FR-009**: System MUST [privacy - e.g., "encrypt patient medical images at rest and in transit"]
- **FR-010**: System MUST [compliance - e.g., "obtain explicit patient consent before sharing data with provider"]

### Integration Requirements

- **FR-011**: System MUST [API requirement - e.g., "expose RESTful API for quote request submissions"]
- **FR-012**: System MUST [external service - e.g., "integrate with payment gateway for request processing fees"]

### Marking Unclear Requirements

*Example of flagging ambiguities:*

- **FR-013**: System MUST authenticate users via [NEEDS CLARIFICATION: auth method not specified - email/password, SSO, OAuth, biometric?]
- **FR-014**: System MUST retain quote request data for [NEEDS CLARIFICATION: retention period not specified - 1 year, 2 years, indefinitely?]

---

## Key Entities

<!--
  ACTION REQUIRED: Define main data entities (high-level, not database schema)
  This helps understand what data this feature manages
-->

- **Entity 1 - [Name]**: [What it represents - e.g., "Quote Request"]
  - **Key attributes** (conceptual, not database fields): [e.g., "patient ID, requested procedures, status, submitted date"]
  - **Relationships**: [e.g., "One patient can have many quote requests; one quote request relates to one or more procedures"]

- **Entity 2 - [Name]**: [What it represents]
  - **Key attributes**: [Attributes]
  - **Relationships**: [Relationships to other entities]

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| [DATE] | 1.0 | Initial PRD creation | [Name/AI] |
| [DATE] | 1.1 | [Description of changes] | [Name] |

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
