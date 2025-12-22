# Quote Submission & Management Module - Product Requirements Document

**Module**: PR-02: Inquiry & Quote Management | A-01: Patient Management & Oversight
**Feature Branch**: `fr004-quote-submission-management`
**Created**: 2025-10-30
**Status**: ✅ Verified & Approved
**Source**: FR-004 from system-prd.md

## Executive Summary

The Quote Submission & Management module empowers providers to receive distributed patient inquiries and create, edit, submit, and manage detailed quotes, as well as manage quote lifecycle (status changes, expiry, withdrawal/cancellation) in a compliant, auditable manner. All patient-facing interactions—including quote status acknowledgment and soft delete handling—are workflow-driven and designed for regulatory transparency and minimum friction, as per UI/UX design diagrams and system PRD rules.

## Module Scope

### Multi-Tenant Architecture

- **Provider Platform (PR-02)**: Core quote management and submission
- **Patient Platform (P-02)**: Quote review/acceptance/cancellation (read-only for submission)
- **Admin Platform (A-01)**: Audit, visibility, and override authority on all quote objects

### Multi-Tenant Breakdown

**Patient Platform (P-02)**:

- View quotes per inquiry; accept/decline; see expiry timers and status
- Receive notifications for quote creation/updates/expiry

**Provider Platform (PR-02)**:

- Create, edit, submit quotes; manage lifecycle (draft, sent, expired, withdrawn, archived)
- See inquiry context (append-only)

**Admin Platform (A-01)**:

- Oversight of all quotes; inline edit (policy-bound), soft delete/restore; full audit trail
- Configure expiry window and manage exceptional withdrawals

**Shared Services (S-XX)**:

- Notification service; audit logging; retention/soft-delete utilities

### Communication Structure

**In Scope**:

- System → Provider: New inquiry notifications and time-bound updates
- Provider → System: Draft, edit, status transitions, soft delete/archive
- System → Patient: Quote creation/expiry/status notifications
- Admin → All Parties: Oversight, intervention, audit logging

**Out of Scope**:

- Direct patient-provider chat (handled by FR-012)

### Entry Points

1. Provider receives auto-distributed inquiry from FR-003
2. Provider opens Quote Management dashboard (new, draft, sent, history, archive bins)
3. Provider creates and edits quote using dedicated, field-driven quote entry screens
4. Patient receives and views quote(s) in patient app
5. Admin can access, search, or override quote status from admin platform

## Business Workflows

### Workflow 1: Provider Quote Creation (Primary Flow)

**Actors**: Provider, System, Admin (observer/audit)

**Trigger**: Provider opens a distributed inquiry and starts composing a quote

**Outcome**: Valid quote is created and delivered to the patient; audit entry recorded

- Provider receives inquiry and opens details
- Provider fills required quote fields (treatment, pricing, scheduling, packages)
- Provider submits quote (system validates required/optional fields)
- System delivers quote to patient and logs audit entry

### Workflow 2: Quote Editing

**Actors**: Provider, System, Admin (observer/audit)

**Trigger**: Provider opens an existing draft or sent (pre-expiry) quote to modify fields

**Outcome**: Changes are saved with versioning/audit; patient notified if significant and not yet accepted

- Provider may edit draft or sent (pre-expiry) quotes (field, price, package edits)
- All changes are versioned/audited
- Edits on expired/withdrawn/archived quote are prohibited
- Patient auto-notified of significant edits if not yet accepted

### Workflow 3: Quote Expiry & Status Transitions

**Actors**: System, Provider, Patient, Admin (observer)

**Trigger**: Time-based expiry reached; patient accepts a quote; or provider initiates withdrawal/archive

**Outcome**: Quote transitions to correct status; notifications sent; audit recorded

- Each quote has an explicit expiry date (admin-controlled). Default expiry window is 48 hours; providers cannot modify this window and only see the computed expiry timestamp.
- Upon expiry, system updates quote to "expired" status; quote can no longer be accepted
- Provider may withdraw or archive quotes pre-acceptance
- Patient acceptance auto-moves quote to "accepted"/"booked" status
- All state transitions are logged and result in notifications as appropriate

### Workflow 4: Quote Deletion (Soft Delete)

**Actors**: Provider, System, Admin

**Trigger**: Provider chooses to remove an ineligible or obsolete quote prior to acceptance

**Outcome**: Quote becomes Archived with rationale; remains visible in audit/archive; only admin can restore

- Provider may soft-delete a quote before acceptance (removes from provider listing, not from audit/archive or patient record)
- System sets status = Archived with rationale
- Soft-deletes are fully auditable and revertible only by admin

### Workflow 5: Admin Oversight

**Actors**: Admin, System

**Trigger**: Admin monitors quotes or intervenes per policy or escalation

**Outcome**: Administrative action applied; full audit trail preserved; re-notifications triggered if needed

- Admin dashboard lists all provider quotes, searchable/filterable by state/date/provider/inquiry
- Admin can perform soft delete or restore; view/edit audit trail and full quote history

### Workflow 6: Provider Withdrawal After Acceptance

**Actors**: Provider, Admin, Patient, System

**Trigger**: Provider requests withdrawal after a patient has accepted the quote

**Outcome**: Quote moves to provider-withdrawn pending admin action; system notifies stakeholders; admin resolves path

- In rare cases, provider may withdraw from giving treatment after patient acceptance.
- Provider submits a withdrawal request with reason; quote status transitions to "provider-withdrawn" pending admin action.
- System notifies patient and admin; admin must resolve: re-route case to alternate provider, offer reschedule, or cancel with refund per policy.
- All actions audited. Note: This flow may be extracted into a separate FR if policy complexity (refunds/penalties/SLAs) increases.

### Alternative Flows

- Provider starts draft but abandons (system retains drafts for 7 days then auto-archives)
- Provider attempts late edit or deletion (system disallows and shows user message)
- Patient declines all quotes (system expires all open quotes automatically)
- Another provider's quote is accepted → System marks all other quotes for the same inquiry as "cancelled (other accepted)" and notifies their providers.
- While a provider is drafting a quote, if another quote is accepted → drafting provider is notified immediately; drafting quote is locked with banner referencing the accepted quote and case status updates.

## Screen Specifications

### Provider Platform

#### Screen 1: Quote Creation/Edit

**Purpose**: Provider creates/edits a quote with full inquiry context

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Treatment | select | Yes | Admin-curated treatment | Must select one |
| Package | select | No | Provider-bounded package | Optional per quote |
| Package Customization | checklist | No | Per-quote inclusions | Free add-ons allowed (logged) |
| Custom Services | repeater | No | Provider-defined services (name/desc/cost) | Each item validated; logged |
| Estimated Grafts | number | Yes | Estimated graft count | Positive integer |
| 3D Markup | drawing | No | Draw on 3D image | Stored with audit |
| Treatment Dates | multiselect (dates) | Yes | Subset of patient-requested ranges | Non-overlapping; from FR-003 ranges |
| Price per Date | repeater | Yes | Price for each selected date | Currency rules; one-to-one with dates |
| Appointment Slot (Pre-Scheduled) | datetime | Yes | Pre-scheduled appointment date/time (start) | Must map to one of the selected Treatment Dates; timezone required |
| Promotion | select/text | No | Optional promotion | Valid code or text note |
| Clinician | select | Yes | Responsible clinician | Must be active/eligible |
| Treatment Plan (per-day) | repeater | Yes | Consecutive per-day plan entries | No date gaps; sequential dates |
| Note | textarea | No | Additional note | Max length enforced |
| Summary (read-only) | group | Yes | Read-only summary of inputs | Must reflect latest data |
| Expiry (read-only) | datetime | Yes | Derived deadline | From admin-configured window |

**Notes**:

- Package Customization examples: Medical consultation, Max grafts, PRP injection, Day-3 wash, Lifetime warranty, Language translator
- Travel & accommodation add-ons: Hotel (star level), Facility–hotel transport, Airport–hotel transport, Flight (class)
- Price must be specified per each selected treatment date
- Providers may add Custom Services as needed (name, description, optional price); all custom items are audited
- Treatment Plan must cover consecutive calendar days without skipping; validation blocks gaps or overlaps

Notes:

- Treatment vs Package: Treatment is admin-controlled and compulsory; Package is provider-bounded and optional. Package customization is per quote instance.

#### Screen 2: Quote List (Unified; no tabs)

**Purpose**: Provider views all quotes in a single unified list

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Patient ID | column | Yes | Anonymized ID | Searchable |
| Name | column | Yes | Partly censored name | Masking applies |
| Age | column | No | Patient age | Number; sortable |
| Problem/Concern | column | No | Primary concern | Filterable |
| Treatment & Package | column | Yes | Selected treatment/package | Read-only |
| Date Ranges Quoted | column | Yes | Provider-chosen subset | Tooltip for all ranges |
| Price | column | Yes | Prices mapped per date | Currency formatting |
| Location | column | No | Patient country | Filterable |
| Medical Alerts | column | Yes | Alert chips | Severity colors |
| Quoted Date | column | Yes | Quote created date | Relative formatting rules |
| Action | column | Yes | Edit, Soft Delete, View Details | State-aware |
| Search/Filters | control | No | Patient/Inquiry/Treatment/Date/Status/Location/Alerts | Valid enums/ranges |

**Notes**:

- Unified list (no tabs) to reflect global case statuses

#### Screen 3: Quote Details Screen

**Purpose**: Inspect full quote details and act (patient-first continuation from inquiry)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Patient (Anonymized) | group | Yes | Anonymized ID, masked name, age, location | Contact hidden until payment |
| Inquiry Context | group | Yes | Continuation data from FR-003 | Read-only |
|  • Countries | list | Yes | Selected treatment countries | From inquiry |
|  • Problem Details | group | Yes | Concern, duration, previous treatments | From inquiry |
|  • Medical Alerts | chips | Yes | Critical/Standard/None | Derived from questionnaire |
|  • Requested Date Ranges | list | Yes | All patient-requested ranges | Read-only |
|  • Media/Scan | links/viewer | No | Photos/videos/3D scan viewer | Read-only |
| Quote Summary | group | Yes | Treatment, package, custom services, per-day plan | Read-only |
| Dates & Prices | table | Yes | Each selected date with price | One-to-one mapping; currency rules |
| Appointment Slot (Pre-Scheduled) | datetime | Yes | Pre-scheduled appointment date/time (start) | Read-only; timezone required |
| Custom Services | list | No | Provider-defined services | Name/desc/cost shown |
| Estimated Grafts | number | Yes | Estimated graft count | Positive integer |
| Promotion | text/select | No | Promotion applied | Code or description |
| Clinician | text | Yes | Responsible clinician | Must be eligible |
| Treatment Plan (per-day) | table | Yes | Consecutive per-day entries | No gaps/overlaps |
| 3D Markup | viewer | No | Drawings over 3D image | Read-only snapshot |
| Note | text | No | Provider note | Read-only |
| Expiry | datetime | Yes | Computed deadline | From admin window |
| Provider Info | group | Yes | Provider/practice info | Read-only per policy |
| Actions | actions | Yes | Edit / Soft Delete (if eligible) | State policy enforced |
| Audit/Version | modal | Yes | Version history and audit log | Immutable audit |

**Notes**:

- UI may use a tabbed interface defaulting to Patient tab, then Inquiry, then Quote, then Audit
- Patient-first ordering ensures natural continuation from inquiry to quote data

### Patient Platform (Read-only for this module)

#### Screen 4: Quote Review

**Purpose**: Patient reviews and accepts/declines quotes

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Quote List | list | Yes | Quotes grouped by inquiry | Read-only |
| Treatment | text | Yes | Selected treatment | Read-only |
| Price Breakdown | table | Yes | Per-date pricing | Currency rules |
| Add-ons | list | No | Customizations/add-ons | Read-only |
| Status | badge | Yes | Pending/Accepted/Expired | Enum validation |
| Expiration Timer | timer | Yes | Countdown to expiry | From admin window |
| Provider Info | group | Yes | Allowed provider details | Privacy rules |
| Actions | actions | Yes | Accept/Decline | State & confirmation rules |
| Notifications | note | No | New/updated/expired indicators | Read-only |

**Governance Note**: This screen’s field/visual specification is defined here in FR-004, but the end-to-end patient quote comparison and acceptance flows (including edge cases, blocking rules, and booking handoff) are governed primarily by **FR-005: Quote Comparison & Acceptance (P-02)**. FR-005 may extend or refine the actions on this screen while preserving the privacy constraints and data structure specified in FR-004.

### Admin Platform

#### Screen 5: Quote List (Admin)

**Purpose**: Admin lists and filters all quotes (multiple providers per inquiry)

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Global Quote Table | table | Yes | All quotes with columns & filters | Admin-only |
| Patient ID | column | Yes | Anonymized ID | Searchable |
| Name | column | Yes | Partly censored name | Masking applies |
| Age | column | No | Patient age | Number; sortable |
| Problem/Concern | column | No | Primary concern | Filterable |
| Treatment & Package | column | Yes | Selected treatment/package | Read-only |
| Date Ranges Quoted | column | Yes | Provider-chosen subset | Tooltip for all ranges |
| Price | column | Yes | Prices mapped per date | Currency formatting |
| Location | column | No | Patient country | Filterable |
| Medical Alerts | column | Yes | Alert chips | Severity colors |
| Quoted Date | column | Yes | Quote created date | Relative formatting rules |
| Provider | column | Yes | Provider/clinic | Filterable |
| Actions | column | Yes | Restore/Archive/View Detail | State-aware |
| Search/Filters | control | No | Patient/Inquiry/Treatment/Date/Status/Location/Alerts/Provider | Valid enums/ranges |
| Inquiry Grouping | control | Yes | Default: grouped by inquiry | Toggle grouping |
| Multi-Quote Cue | badge/icon | No | Visual cue for multiple quotes in inquiry | Shows count or indicator |
| Audit Trail | modal | Yes | Per-quote audit (who/what/when/prev value) | Immutable |
| Version History | modal | Yes | Full version history | Immutable |

#### Screen 6: Quote Detail (Admin)

**Purpose**: Admin views complete quote with inquiry continuation

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Quote Selector | dropdown/list | Yes | Switch between quotes for this inquiry | Must belong to same inquiry |
| Quote Summary | group | Yes | Treatment, package, custom services, per-day plan | Read-only |
| Dates & Prices | table | Yes | Each selected date with price | One-to-one mapping |
| Estimated Grafts | number | Yes | Estimated graft count | Positive integer |
| Promotion | text/select | No | Promotion applied | Code or description |
| Clinician | text | Yes | Responsible clinician | Must be eligible |
| Treatment Plan (per-day) | table | Yes | Consecutive per-day entries | No gaps/overlaps |
| 3D Markup | viewer | No | Drawings over 3D image | Read-only snapshot |
| Note | text | No | Provider note | Read-only |
| Expiry | datetime | Yes | Computed deadline | From admin window |
| Provider Info | group | Yes | Provider/practice info | Read-only |
| Inquiry Context | group | Yes | Countries, problem, alerts, ranges, media/scan | From FR-003 |
| Audit Trail | log | Yes | Full change history | Immutable |
| Version History | list | Yes | Quote versions | Immutable |

#### Screen 7: Admin Inline Quote Edit

**Purpose**: Admin performs limited inline edits with audit

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Quote Selector | dropdown/list | Yes | Select target quote under inquiry | Must belong to same inquiry |
| Price per Date | repeater | Cond. | Edit price per selected date | Reason required |
| Package Inclusions | checklist | Cond. | Edit inclusions | Reason required |
| Estimated Grafts | number | Cond. | Adjust graft count | Positive integer; reason required |
| Custom Services | repeater | Cond. | Add/edit provider-defined services | Name/desc/cost; reason required |
| Treatment Plan (per-day) | repeater | Cond. | Edit consecutive per-day plan | No gaps/overlaps; reason required |
| Promotion | text/select | Cond. | Add/change promotion | Valid code; reason required |
| Notes | textarea | No | Admin note | Stored with audit |
| Clinician | select | Cond. | Change clinician | Must be eligible |
| Audit Reason | textarea | Yes | Reason for change | Required for any edit |

**Notes**:

- All inline edits auditable (who/when/before/after, reason); system re-notifies on impactful changes

## Business Rules

- Quotes MUST reference distributed inquiry ID and be linked to original patient object
- Quote data MUST append to inquiry data; no reduction or overwriting of inquiry-supplied fields. Downstream stages inherit upstream data.
- Only assigned clinic staff may submit/edit quotes for assigned inquiries
- Treatment type selection MUST use admin-curated treatment catalog; no free text
- Graft/quantity, price, scheduled slots MUST be present and valid
- Packages/add-ons field may be empty (if none offered by provider)
- Quotes CANNOT be hard deleted (only archived/soft deleted)
- All state transitions (draft→sent→expired, etc.) MUST be fully auditable
- Quotes may be edited only until accepted or expired
- Quotes MUST expire automatically on reaching set expiry date
- Each inquiry may have multiple quotes (for multi-provider or multi-package/option cases)
- Discounts are provider-managed (reviewed by admin if above configured threshold)
- All notifications MUST comply with platform notfication/audit/logging rules
- GDPR/data compliance: all quote objects are archived for ≥7 years
- Patient information remains censored at this stage until payment confirmation; only anonymized identifiers and allowed fields are visible to providers.
- Providers must select from patient-requested date ranges and may choose a subset; each selected date must have a specific price.

## Success Criteria

- **SC-001**: 100% of distributed inquiries receiving valid quotes from ≥1 provider within 72h
- **SC-002**: 100% of quote edits and deletions reflected in version/audit history
- **SC-003**: 95% of patient decisions (accept/decline) are processed with correct quote status update and notification
- **SC-004**: <5% of provider quote rejections due to missing/invalid fields
- **SC-005**: 0 hard deletes of quotes; 100% retrievable from archive for ≥7 years

## Functional Requirements Summary

### Core Requirements

- **REQ-004-001**: Providers MUST create, edit, and submit quotes with treatment, package, customization, dates, pre-scheduled appointment slot (date/time), and per-date pricing.
- **REQ-004-002**: System MUST enforce admin-controlled expiry window (default 48h) and compute deadlines per quote.
- **REQ-004-003**: System MUST auto-cancel other quotes for the same inquiry upon one acceptance and notify affected providers.
- **REQ-004-004**: System MUST support provider withdrawal after acceptance with admin resolution workflow and full audit.
- **REQ-004-005**: Admin MUST be able to inline edit policy-bound fields with required reason and re-notifications.

### Data Requirements

- **REQ-004-006**: Quotes MUST reference original inquiry and patient; quote data appends, never overwrites inquiry data.
- **REQ-004-007**: All quote edits and state transitions MUST be versioned and auditable.

### Security & Privacy Requirements

- **REQ-004-008**: Patient identifiers MUST remain anonymized to providers until payment confirmation.
- **REQ-004-009**: All quote data MUST be encrypted at rest and in transit; soft deletes only.

### Integration Requirements

- **REQ-004-010**: Module MUST integrate with FR-003 for inquiry context and FR-020 for notifications.
- **REQ-004-011**: Admin settings (expiry window) MUST be applied from A-09.

### Clarifications

- **REQ-004-012**: Refund/penalty policy depth for provider withdrawal may move to a dedicated FR if expanded.

## Key Entities

- **Quote**: id, inquiryId, providerId, treatmentId, packageId, customizations[], estimatedGrafts, datePrices[], appointmentSlotAt, appointmentTimeZone, clinicianId, promotionId, promotionNote, plan, note, status, expiresAt, createdAt, updatedAt
  - Relationships: belongsTo Inquiry; belongsTo Provider; hasMany QuoteVersion; hasMany QuoteAudit
- **QuoteVersion**: quoteId, version, changeset, createdAt, createdBy
  - Relationships: belongsTo Quote
- **QuoteAudit**: quoteId, action, actorId, reason, before, after, createdAt
  - Relationships: belongsTo Quote

## Dependencies

### Internal Dependencies

- FR-003: Inquiry Submission (quote distribution and reference)
- FR-020: Notifications & Alerts (quote distribution/updates)
- Admin-managed treatment catalog/package definitions (A-09)
- FR-019: Promotions & Discount Management (A-06)

### External Dependencies (APIs, Services)

- Calendar/appointment APIs for appointment integration
- Currency/exchange rate API for quote currency fields (if applicable)

### Data Dependencies

- Inquiry ID, Patient anonymized ID, Provider ID, Promotion ID (from A-06/FR-019), Audit log IDs

## Assumptions

### User Behavior Assumptions

- Providers are trained and will use the quote management UI in compliance with platform audit rules
- Patients will review quotes and act (accept/decline) within configured timeframes

### Technology Assumptions

- Providers have reliable access to the web app; network supports quote operations and media viewing
- Integration services (notifications, currency) are available with acceptable latency

### Business Process Assumptions

- All patients/inquiries are distributed only to eligible providers within jurisdiction
- Admin-curated treatment catalog/package definitions are up to date and applied consistently

## Implementation Notes

### Technical Considerations

- No free text for core treatment field (catalog enforced)
- Immutable audit/versioning for all edits and state transitions
- Expiry, soft-delete, and audit patterns conform to platform standards

### Integration Points

- FR-003: Inquiry context and distribution inputs
- FR-020: Notifications for creation/updates/expiry/status
- Admin (A-09): Treatment catalog/package definitions and expiry policy
- FR-019 / A-06: Promotions & Discount Management for promotionId, promotion configuration, and discount application rules

### Scalability Considerations

- Efficient querying/indexing for provider quote lists and filters
- Background jobs for mass notifications and expiry processing
- Rate limiting on edit/submit endpoints to prevent abuse

### Security Considerations

- Encrypt quote data at rest and in transit; enforce RBAC for provider staff
- Anonymize patient identifiers until payment confirmation
- Comprehensive audit logging (who/when/what-before/after, reason)

## Edge Cases

- Provider starts, then abandons, a draft: auto-archive to Drafts after 7 days
- Patient does not respond: quote expires, status auto-updated, provider notified
- Admin must audit archived/soft-deleted quote: accessible in "Archived" tab, audit trail modal enabled
- Provider attempts deletion post-acceptance: disallowed; only admin can archive with rationale
- Recovery from expired state: only admin can restore expired/archived quotes if justified (GDPR-compliant log)

## Glossary

- **Quote**: Provider-generated cost and treatment proposal for a given inquiry
- **Soft Delete**: Archive status, not a hard delete; record remains for compliance/audit
- **Treatment Catalog**: Admin-defined set of available treatments displayed to all providers for selection
- **Add-On/Package**: Optional offering by provider (e.g., hotel, transport, medications)

## References

## User Scenarios & Testing

### User Story 1 - Create and Submit Quote (Priority: P1)

Why: Core provider action enabling patient decision-making.

Independent Test: Provider opens distributed inquiry, fills required quote fields, submits; patient sees quote with expiry.

Acceptance Scenarios:

1. Given a distributed inquiry, When provider submits a valid quote, Then patient receives quote and expiry timer starts
2. Given required fields are missing, When submitting, Then system blocks with clear validation messages
3. Given a submitted quote, When viewing provider list, Then quote appears with correct status and audit entry

### User Story 2 - Edit Quote Before Expiry (Priority: P2)

Why: Providers need controlled flexibility prior to patient acceptance.

Independent Test: Provider edits a sent (pre-expiry) quote; changes versioned and patient notified.

Acceptance Scenarios:

1. Given a sent quote not yet expired, When editing price/package, Then version increments and audit logs record change
2. Given a significant change, When saved, Then patient is notified automatically
3. Given an expired quote, When editing, Then system blocks and shows policy notice

### User Story 3 - Auto-Expiry and Status Transitions (Priority: P1)

Why: Enforces time-bound decision windows.

Independent Test: Allow quote to reach expiry; verify status transitions and notifications.

Acceptance Scenarios:

1. Given a sent quote, When expiry time is reached, Then status becomes Expired and provider/patient are notified
2. Given patient accepts a quote, When acceptance is recorded, Then other quotes are cancelled and stakeholders notified

### Edge Cases (User Scenarios)

- Provider starts draft then abandons: auto-archive after 7 days
- Patient does not respond: quote expires and provider notified
- Provider attempts deletion post-acceptance: disallowed; admin-only archive with rationale
- Admin audits archived/soft-deleted quote: available in Archived view with full audit trail

- Design: Quote submission/management dashboard + details/flow (latest version approved by Product Owner)
- system-prd.md: FR-004, Notification/Retention/Audit policies
- Transcriptions: /transcriptions/Hairline-ProviderPlatformPart1.txt lines 200-350 (quote construction flows), /transcriptions/HairlineApp-Part2.txt (patient quote acceptance sequence)

## Verification Checklist

- [ ] All PRD sections filled, in required order and detail
- [ ] Fields and statuses match design and high-level docs
- [ ] State transitions, audit, and retention policy enforced
- [ ] Consistent with UI diagrams, data schema, and nomenclature
- [ ] No unresolved [NEEDS CLARIFICATION]
- [ ] Aligned with GDPR/data/retention and platform notification/audit rules

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-10-30 | 1.0 | Initial PRD creation | Product & Engineering |
| 2025-11-03 | 1.1 | Template normalization; added tenant breakdown, comms structure, screen tables, FR summary, entities | Product & Engineering |
| 2025-11-04 | 1.2 | Template compliance: added Actors/Trigger/Outcome to workflows; normalized Dependencies; restructured Assumptions; formalized Implementation Notes; added User Scenarios & Testing | Product & Engineering |

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | [Name] | [Date] | [Status] |
| Technical Lead | [Name] | [Date] | [Status] |
| Stakeholder | [Name] | [Date] | [Status] |
