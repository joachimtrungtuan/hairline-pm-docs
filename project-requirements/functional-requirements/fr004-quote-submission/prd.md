# Quote Submission & Management Module - Product Requirements Document

**Module**: PR-02: Inquiry & Quote Management
**Feature Branch**: `fr004-quote-submission-management`
**Created**: 2025-10-30
**Status**: Draft
**Source**: FR-004 from system-prd.md

## Executive Summary

The Quote Submission & Management module empowers providers to receive distributed patient inquiries and create, edit, submit, and manage detailed quotes, as well as manage quote lifecycle (status changes, expiry, withdrawal/cancellation) in a compliant, auditable manner. All patient-facing interactions—including quote status acknowledgment and soft delete handling—are workflow-driven and designed for regulatory transparency and minimum friction, as per UI/UX design diagrams and system PRD rules.

## Module Scope

### Multi-Tenant Architecture

- **Provider Platform (PR-02)**: Core quote management and submission
- **Patient Platform (P-02)**: Quote review/acceptance/cancellation (read-only for submission)
- **Admin Platform (A-01)**: Audit, visibility, and override authority on all quote objects

### Communication Structure

- **System → Provider**: Automatic notifications for new inquiries and time-bound updates
- **Provider → System**: Quote draft, edit, status transitions, deletion, and archiving actions
- **System → Patient**: Notification of quote creation/expiry/status via platform subsystem
- **Admin → All Parties**: Oversight, intervention, and audit logging

### Entry Points

1. Provider receives auto-distributed inquiry from FR-003
2. Provider opens Quote Management dashboard (new, draft, sent, history, archive bins)
3. Provider creates and edits quote using dedicated, field-driven quote entry screens
4. Patient receives and views quote(s) in patient app
5. Admin can access, search, or override quote status from admin platform

## Business Workflows

### Workflow 1: Provider Quote Creation (Primary Flow)

**Actors**: Provider, System, Admin (observer/audit)

- Provider receives inquiry and opens details
- Provider fills required quote fields (treatment, pricing, scheduling, packages)
- Provider submits quote (system validates required/optional fields)
- System delivers quote to patient and logs audit entry

### Workflow 2: Quote Editing

- Provider may edit draft or sent (pre-expiry) quotes (field, price, package edits)
- All changes are versioned/audited
- Edits on expired/withdrawn/archived quote are prohibited
- Patient auto-notified of significant edits if not yet accepted

### Workflow 3: Quote Expiry & Status Transitions

- Each quote has an explicit expiry date (admin-controlled). Default expiry window is 48 hours; providers cannot modify this window and only see the computed expiry timestamp.
- Upon expiry, system updates quote to "expired" status; quote can no longer be accepted
- Provider may withdraw or archive quotes pre-acceptance
- Patient acceptance auto-moves quote to "accepted"/"booked" status
- All state transitions are logged and result in notifications as appropriate

### Workflow 4: Quote Deletion (Soft Delete)

- Provider may soft-delete a quote before acceptance (removes from provider listing, not from audit/archive or patient record)
- System sets status = Archived with rationale
- Soft-deletes are fully auditable and revertible only by admin

### Workflow 5: Admin Oversight

- Admin dashboard lists all provider quotes, searchable/filterable by state/date/provider/inquiry
- Admin can perform soft delete or restore; view/edit audit trail and full quote history

### Workflow 6: Provider Withdrawal After Acceptance

**Actors**: Provider, Admin, Patient, System

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

- All inquiry context/fields (auto-copied from distributed inquiry; append-only — never replace inquiry data).
- Field order (matches implemented design):
  1) Select treatment (admin-curated; compulsory)
  2) Select package (provider-bounded; optional, per quote)
  3) Customize package → What to include (per quote):
     - Medical consultation
     - Maximum grafts
     - PRP injection
     - Washing session on 3rd day
     - Life time warranty
     - Preferred language translator
     - [Add more services]
     - Travel & accommodation arrangements
       - Hotel accommodation (pick star level)
       - Facility–hotel transport
       - Airport–hotel transport
       - Flight arrangements (pick flying class)
       - [Add more services]
  4) Estimate grafts
     - Estimate number of grafts required
     - Draw on 3D image to communicate with the patient
  5) Select treatment date(s)
     - From patient-requested date ranges; provider may choose a subset (not required to quote all)
  6) Price
     - Quote price per each selected date range
     - Add promotion
  7) Select the clinician
  8) Add treatment plan
  9) Add note (long text)
  10) View summary (read-only): Treatment chosen; Package chosen; Customization; Estimated grafts; Date(s) with price per date; Clinician; Note
  11) Expiry (read-only): shows admin-defined window (default 48h) and computed deadline

Notes:

- Treatment vs Package: Treatment is admin-controlled and compulsory; Package is provider-bounded and optional. Package customization is per quote instance.

#### Screen 2: Quote List (Unified; no tabs)

- Single unified list (no tab segmentation) to reflect globally unified case statuses.
- Columns:
  - Patient identifier (auto-generated anonymized ID)
  - Name (partly censored)
  - Age (number)
  - Problem/concern (enum)
  - Treatment & package chosen
  - Date ranges quoted (multiple; provider-chosen subset)
  - Price (multiple; mapped to date ranges)
  - Location
  - Medical alerts (chips)
  - Quoted date
  - Action (Edit, Soft Delete, View Details)
- Search/filter: by patient/inquiry/treatment/date/status/provider/location/alerts

#### Screen 3: Quote Details Popup/Screen

- Full quote breakdown, all submitted fields
- Edit and Delete (soft) if eligible
- Complete provider/practice info as per platform rules
- Audit/version history popup

### Patient Platform (Read-only for this module)

#### Screen 4: Quote Review

- Quotes grouped/listed per inquiry
- Major fields: Treatment, price breakdown, add-ons, status (Pending, Accepted, Expired), expiration timer
- Accept/Decline buttons (with warning for expiration/withdrawal)
- Provider info and medical details as allowed by privacy rules
- Notification of new/updated/expired quotes

### Admin Platform

#### Screen 5: Quote Oversight/Audit Dashboard

- Search/filter for all quotes by provider/inquiry/status/date/location/alerts
- Restore or permanently archive (special action)
- Audit trail modal for every quote (who, what, when, previous value)
- View all quote version history

#### Screen 6: Admin Inline Quote Edit

- Admin can inline-edit quotes where policy requires intervention: price per selected date range, package inclusions, notes, and clinician (with audit reason).
- All inline edits are auditable (who/when/before/after, reason). System re-notifies patient and provider when changes are impactful.

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

## Dependencies

- **Internal**:
  - FR-003: Inquiry Submission (quote distribution and reference)
  - FR-020: Notifications & Alerts (quote distribution/updates)
  - Admin-managed treatment catalog/package definitions (A-09)
- **External**: Calendar/inquiry APIs for appointment integration, currency/exchange rate API for quote currency fields if applicable
- **Data**: Inquiry ID, Patient anonymized ID, Provider ID, Audit log IDs

## Assumptions

- Providers are fully onboarded and have active staff/clinic profiles
- All patients/inquiries distributed to eligible providers in jurisdiction
- Admin-curated treatment catalog is up to date and available
- Provider staff are trained to use quote management UI and comply with platform audit rules

## Implementation Notes

- No free text for core treatment field (catalog enforced)
- Expiry, soft-delete, and audit patterns as per platform standard (see system PRD/constitution)
- Integration points: Inquiry module (FR-003), notification service (FR-020), admin treatment settings
- Currency and pricing logic leverages platform-wide exchange rate/service

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
