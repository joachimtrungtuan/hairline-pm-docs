# Product Requirements Document: Data Retention & Compliance

**Module**: A-09: System Settings & Configuration (Cross-Cutting Concern)  
**Feature Branch**: `fr023-data-retention-compliance`  
**Created**: 2025-11-12  
**Status**: Draft  
**Source**: FR-023 in system-prd.md; Client transcriptions (HairlineApp-Part1.txt, Hairline-AdminPlatform-Part1.txt, Hairline-ProviderPlatformPart1.txt)

---

## Executive Summary

Establish organization-wide data retention, auditability, and privacy controls to meet healthcare and financial record-keeping obligations while honoring user privacy rights. This feature defines retention policies (minimum 7 years for medical and financial records), enforces soft-deletion only for critical data, provides GDPR-compliant data export and deletion request handling, anonymizes patient data used in analytics, and maintains comprehensive audit logs for all data access and modification events. The outcome is a compliant, transparent, and testable framework applicable across Patient, Provider, and Admin applications.

---

## Success Criteria

- 100% of patient data export requests delivered within 7 calendar days of verification.
- 100% of valid deletion requests processed within 30 calendar days, with legally retained records restricted appropriately (no anonymization for retained medical/financial records).
- 0% of critical records (medical, financial) hard-deleted before end-of-retention period.
- 100% of read/write access to protected records captured in audit logs with who/when/what.
- 0% personally identifiable patient attributes present in analytics dashboards or reports.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform**: View retention policy; request data export; request account/data deletion; receive status updates and outcomes.
- **Provider Platform**: View applicable retention/privacy policy; cannot permanently delete protected records; access read-only audit trail for activity by their users.
- **Admin Platform (A-09)**: Configure retention settings (by data category/region), triage and fulfill export/deletion requests, review audit trails, approve exceptions.
- **Shared Services**: Cross-cutting job scheduling for retention enforcement; audit logging; anonymization pipeline; export packaging; notification templates.

### Communication Structure

**In Scope**:

- User notifications for DSR (Data Subject Request) status changes (submission, verification required, in progress, fulfilled).
- Admin notifications for new DSRs and approaching deadlines.
- Compliance reporting exports (downloadable by Admin).

**Out of Scope**:

- Real-time chat/video features (managed by other modules).
- Payment flow changes beyond record retention.
- Third-party DPO/legal tooling integrations (future consideration).

### Entry Points

- Patient: Profile/Privacy screen → Request Export; Request Deletion.
- Provider: Settings → Data Policy (read-only); Activity Logs.
- Admin: Compliance dashboard → Retention Settings; DSR Queue; Audit Logs; Reports.

---

## Business Workflows

### Main Flow: Data Export Request (DSR)

**Actors**: Patient, Admin, System  
**Trigger**: Patient submits data export request from Privacy screen  
**Outcome**: Patient receives machine-readable export; Admin log reflects completion

**Steps**:

1. Patient submits DSR (export) and completes identity verification.
2. System acknowledges request and places it in Admin DSR queue.
3. Admin reviews request scope and confirms eligibility.
4. System assembles export package (account data, communications, bookings, media references).
5. System delivers export securely to Patient; logs event; marks request Completed.

### Main Flow: Deletion Request (Right to Erasure)

**Actors**: Patient, Admin, System  
**Trigger**: Patient requests deletion from Privacy screen  
**Outcome**: Non-legally-required data deleted or anonymized; protected data retained with access restrictions; audit logged

**Steps**:

1. Patient submits deletion request and completes verification.
2. System classifies data by category and applicable retention/jurisdiction.
3. Admin reviews classification and approves action.
4. System performs deletion/anonymization for non-protected data; restricts access to protected records.
5. System records actions in audit log and notifies Patient of outcome and legal basis.

### Alternative Flows

**A1: Verification Required**

- Trigger: Submitted DSR lacks sufficient identity proof.
- Steps:
  1. System flags request as Verification Required and notifies Patient.
  2. Patient provides additional verification.
  3. Admin validates and resumes processing.
- Outcome: Export/deletion proceeds; SLA clock pauses during verification.

**A2: Exclusion of Legally Retained Data**

- Trigger: Data categories include records subject to mandatory retention.
- Steps:
  1. Admin confirms exclusion of protected medical/financial records.
  2. System includes metadata references and explains legal basis in export notes.
- Outcome: Export excludes protected content; notes document rationale.

**B1: Export Assembly Failure**

- Trigger: A data category fails to assemble (e.g., corrupt media reference).
- Steps:
  1. System logs failure with category, record IDs, and error details.
  2. Admin retries assembly after remediation or excludes failed category with documented reason.

---

## User Stories

### User Story 1 - Export My Data (Priority: P1)

As a Patient, I want to request and receive a copy of my data so that I can review, correct, or transfer it to another service.

**Independent Test**: Submit DSR with a seeded test user and verify packaged export contents and delivery within SLA.

**Acceptance Scenarios**:

1. Given a verified patient, When they submit a data export request, Then the system confirms receipt and shows status In Progress.
2. Given an export in progress, When assembly completes, Then the patient receives a secure link and the request shows Completed.
3. Given legal retention constraints, When certain records are excluded, Then the export includes a rationale note listing exclusions.

### User Story 2 - Delete My Account/Data (Priority: P1)

As a Patient, I want to request deletion of my account and personal data so that I can exercise my right to be forgotten.

**Independent Test**: Submit deletion request, verify anonymization/deletion actions and communication of legally retained records within 30 days.

**Acceptance Scenarios**:

1. Given a verified deletion request, When approved by Admin, Then non-protected personal data is deleted and protected records are restricted/anonymized.
2. Given the deletion request completion, When patient reviews notification, Then it lists actions taken and legal basis for any retained records.

### User Story 3 - Review Audit Trail (Priority: P1)

As an Admin, I need a complete audit trail of access and modifications to protected records so I can investigate incidents and demonstrate compliance.

**Independent Test**: Perform seeded read/write events and verify audit log captures actor, timestamp, action, object, and outcome; export is downloadable.

**Acceptance Scenarios**:

1. Given protected data access, When a user views a medical record, Then an audit entry records who, when, what, and outcome.
2. Given a modification to a protected record, When the change is saved, Then the audit log includes before/after metadata and actor.

### Edge Cases

- Patient submits multiple DSRs concurrently → System merges or queues with clear status; SLA applies per consolidated request.
- Media files included in export exceed download limits → Provide chunked downloads and expirations.
- Patient requests deletion while active booking exists → System pauses deletion until booking resolves; communicates timeline.
- Jurisdiction conflict (e.g., EU vs non-EU residency) → Default to stricter retention; flag for Admin review.

---

## Functional Requirements Summary

### Core Requirements

- FR-023.1: System MUST retain patient medical records for a minimum of 7 years; hard-deletion is prohibited before expiry.
- FR-023.2: System MUST retain financial transaction records for a minimum of 7 years; hard-deletion is prohibited before expiry.
- FR-023.3: System MUST support soft-deletes only for protected categories (medical, financial, identity), preserving recoverability and auditability.
- FR-023.4: System MUST provide GDPR-compliant data export in a machine-readable, portable format (with media referenced via secure links) including account/profile, bookings, messages, and media references; raw audit logs are excluded by default and provided only upon explicit request subject to review.
- FR-023.5: System MUST allow patients to request data deletion (erasure); non-protected data is deleted or anonymized; protected medical/financial records are retained without anonymization but with strict access restrictions and documented legal basis.
- FR-023.6: System MUST anonymize patient data in analytics and reports (no direct identifiers, quasi-identifiers masked or aggregated).
- FR-023.7: System MUST maintain audit logs for all read and write access to protected records, including actor, timestamp, object, action, outcome.
- FR-023.8: System MUST provide Admin views to configure retention by data category and jurisdiction and to manage DSR queues.
- FR-023.9: System MUST notify Patients and Admins about DSR status updates and completion outcomes.

### Data Requirements

- FR-023.D1: System MUST classify data into categories: Medical Records, Financial Records, Communications, Media, Account Profile, Analytics.
- FR-023.D2: Each category MUST have an assigned retention policy and legal basis (with jurisdiction overrides).
- FR-023.D3: Audit log entries MUST be immutable and retained for at least 7 years.
- FR-023.D4: Backups MUST occur at least every 6 hours with 30-day retention (per system PRD) and exclude already-deleted personal data beyond backup windows.

### Security & Privacy Requirements

- FR-023.S1: Exports MUST be delivered via secure, time-bound links; access requires identity verification.
- FR-023.S2: Deletion actions MUST purge search indexes and caches for impacted personal data.
- FR-023.S3: Anonymization MUST remove direct identifiers and reduce re-identification risk for quasi-identifiers.
- FR-023.S4: System MUST capture consent for analytics usage where applicable and honor opt-outs in non-essential analytics.

### Integration Requirements

- FR-023.I1: Provide Admin export of audit logs and retention reports in portable, non-proprietary formats.
- FR-023.I2: Provide programmatic access for DSR submission/status for Patient app integration.
- FR-023.I3: Provide event notifications for DSR lifecycle events to internal communication channels.

### Clarifications (Resolved)

- CL-1: Erasure handling for medical/financial records — Retain without anonymization but fully restrict access during the legal retention period; document legal basis in outcomes.
- CL-2: Data export scope — Include account/profile, bookings, messages, and media references. Exclude raw audit logs by default; make available upon explicit request subject to security/legal review.
- CL-3: Audit log retention — Retain audit logs for 7 years; logs are immutable and included in compliance reporting (exports are summaries unless otherwise requested).

---

## Key Entities

- Data Subject Request (DSR): id, type (export/deletion), requester, verification status, submitted/updated dates, outcome  
  Relationships: belongs to Patient; processed by Admin; linked to export package and actions taken

- Retention Policy: id, data category, default retention, legal basis, jurisdiction overrides  
  Relationships: applied to records via category mapping; referenced by enforcement jobs

- Audit Log Entry: id, actor, timestamp, object type/id, action (read/write/delete), outcome, context  
  Relationships: references users and data categories; immutable store

- Export Package: id, requester, contents manifest, delivery method, expiration, download events  
  Relationships: linked to DSR; references object categories included

---

## Dependencies

### Internal Dependencies

- A-09: System Settings & Configuration (retention policy configuration, DSR management).
- S-03: Notification Service (DSR status notifications to users/admins).

### External/Reference Dependencies

- GDPR (data portability, right to erasure) and applicable healthcare retention regulations.

---

## Assumptions

- Retention minimums (7 years) apply to medical and financial records platform-wide unless stricter jurisdictional rules exist.
- Backups run every 6 hours with 30-day retention per system PRD; deleted data may persist in backups until window expiry.
- Patients are willing and able to complete identity verification for DSRs via standard methods.

---

## Appendix: Change Log

| Date       | Version | Changes                                           | Author       |
|------------|---------|---------------------------------------------------|--------------|
| 2025-11-12 | 1.0     | Initial PRD creation                              | AI Assistant |
| 2025-11-12 | 1.1     | Added Success Criteria and clarified dependencies | AI Assistant |

---

## Appendix: Approvals

| Role            | Name | Date | Signature/Approval |
|-----------------|------|------|--------------------|
| Product Owner   |      |      |                    |
| Technical Lead  |      |      |                    |
| Stakeholder     |      |      |                    |

---

**Template Version**: 2.0.0 (Constitution-Compliant)  
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)  
**Based on**: FR-023 Data Retention & Compliance  
**Last Updated**: 2025-11-12
