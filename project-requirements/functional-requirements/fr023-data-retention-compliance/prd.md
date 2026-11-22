# FR-023 - Data Retention & Compliance

**Module**: A-09: System Settings & Configuration (Cross-Cutting Concern)  
**Feature Branch**: `fr023-data-retention-compliance`  
**Created**: 2025-11-12  
**Status**: Draft  
**Source**: FR-023 in system-prd.md; Client transcriptions (HairlineApp-Part1.txt, Hairline-AdminPlatform-Part1.txt, Hairline-ProviderPlatformPart1.txt)

---

## Executive Summary

Establish organization-wide data retention, auditability, and privacy controls to meet healthcare and financial record-keeping obligations while honoring user privacy rights. This feature defines retention policies (one retention period for medical records, financial records and audit logs; see system PRD, Platform-Wide Rules: One 10-year retention period), enforces soft-deletion only for critical data, provides GDPR-compliant deletion request handling (right to erasure), anonymizes patient data used in analytics, and maintains comprehensive audit logs for all data access and modification events. The outcome is a compliant, transparent, and testable framework applicable across Patient, Provider, and Admin applications.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform**: View retention policy; request account/data deletion; receive status updates and outcomes. (REQ-023-020)
- **Provider Platform**: View applicable retention/privacy policy; cannot permanently delete protected records; access read-only audit trail for activity by their users. (REQ-023-021, REQ-023-022, REQ-023-023)
- **Admin Platform (A-09)**: Configure retention settings (by data category/region), triage and fulfill deletion requests, review audit trails. (REQ-023-007, REQ-023-024)
- **Shared Services**: Cross-cutting job scheduling for retention enforcement (REQ-023-026); audit logging; anonymization pipeline; notification templates.

### Communication Structure

**In Scope**:

- User notifications for DSR (Data Subject Request) status changes (submission, verification required, in progress, fulfilled). (REQ-023-028)
- Admin notifications for new DSRs and approaching deadlines (REQ-023-029). The submission notice to the Patient and the new-request notice to Admins use the same account-deletion-requested event (FR-001).
- Compliance reporting exports (downloadable by Admin).

**Out of Scope** (REQ-023-027):

- Real-time chat/video features (managed by other modules).
- Payment flow changes beyond record retention.
- Third-party DPO/legal tooling integrations (future consideration).

### Entry Points

- Patient: Profile > Delete Account.
- Provider: Settings → Data Policy (read-only); Activity Logs.
- Admin: Compliance dashboard → Retention Settings; DSR Queue; Audit Logs; Reports.

All three entry points: REQ-023-019.

---

## Business Workflows

### Main Flow: Deletion Request (Right to Erasure)

**Actors**: Patient, Admin, System  
**Trigger**: Patient requests deletion from Profile > Delete Account  
**Outcome**: Non-legally-required data deleted or anonymized; protected data retained in anonymised form with access restrictions; audit logged

**Steps**:

1. Patient submits deletion request and completes verification.
2. System classifies data by category and applicable retention/jurisdiction.
3. Admin reviews classification and approves action.
4. System performs deletion/anonymization for non-protected data; anonymises and restricts access to protected records.
5. System records actions in audit log and notifies Patient of outcome and legal basis.

### Alternative Flows

**A1: Verification Required**

- Trigger: Submitted DSR lacks sufficient identity proof.
- Steps:
  1. System flags request as Verification Required and notifies Patient.
  2. Patient provides additional verification.
  3. Admin validates and resumes processing.
- Outcome: Deletion request processing proceeds; the 30-day deadline always runs from submission and does not pause during verification.

**A2: Exclusion of Legally Retained Data**

- Trigger: Data categories include records subject to mandatory retention.
- Steps:
  1. Admin confirms exclusion of protected medical/financial records.
  2. System includes the legal basis and scope of retained categories in the patient outcome notification.
- Outcome: Deletion/anonymization completes for non-protected data; outcome documents retained data and legal basis.

Rules carried by the flows above: Main Flow steps 1 to 5 (REQ-023-030, REQ-023-031, REQ-023-032, REQ-023-004, REQ-023-033); A1 (REQ-023-034, REQ-023-041); A2 (REQ-023-036, REQ-023-033).

---

## User Stories

### User Story 1 - Delete My Account/Data (Priority: P1)

As a Patient, I want to request deletion of my account and personal data so that I can exercise my right to be forgotten.

**Independent Test**: Submit deletion request, verify anonymization/deletion actions and communication of legally retained records within 30 days.

**Acceptance Scenarios**:

1. Given a verified deletion request, When approved by Admin, Then non-protected personal data is deleted and protected records are restricted/anonymized.
2. Given the deletion request completion, When patient reviews notification, Then it lists actions taken and legal basis for any retained records.

### User Story 2 - Review Audit Trail (Priority: P1)

As an Admin, I need a complete audit trail of access and modifications to protected records so I can investigate incidents and demonstrate compliance.

**Independent Test**: Perform seeded read/write events and verify audit log captures actor, timestamp, action, object, and outcome.

**Acceptance Scenarios**:

1. Given protected data access, When a user views a medical record, Then an audit entry records who, when, what, and outcome.
2. Given a modification to a protected record, When the change is saved, Then the audit log includes before/after metadata and actor.

### Edge Cases

- Patient submits multiple DSRs concurrently → System merges them into one request with clear status; SLA applies per consolidated request. (REQ-023-037)
- Patient requests deletion while active booking exists → System pauses deletion until booking resolves; communicates timeline. (REQ-023-038)
- Jurisdiction conflict (e.g., EU vs non-EU residency) → Default to stricter retention; flag for Admin review. (REQ-023-039)
- Patient requests data deletion after cancelling their inquiry → Cancelled inquiry is a terminal state with no active obligation; deletion request should proceed normally. Cancelled inquiry records, cascaded cancelled quotes, and associated audit entries are retained per the system PRD, Platform-Wide Rules: One 10-year retention period and REQ-023-003 even after the deletion request is fulfilled — retained records are kept in anonymised form. (REQ-023-040)

---

## Functional Requirements Summary

### Core Requirements

- **REQ-023-001**: Retired. Retention of medical records (including head-scan media), financial transaction records and audit logs, and the ban on hard-deletion before expiry, follow the system PRD, Platform-Wide Rules: One 10-year retention period.
- **REQ-023-003**: System MUST support soft-deletes only for protected categories (Medical Records, Financial Records, Account Profile), preserving recoverability and auditability. Patient-cancelled inquiries (FR-003 Workflow 5) and all records generated from the cancellation cascade — including auto-cancelled quotes with status "Cancelled (Inquiry Cancelled)" per FR-004 — are subject to the same retention rules as completed inquiries and quotes. They are soft-deleted/archived, never hard-deleted before the retention period expires; AcceptanceEvents are retained and never deleted (FR-005 REQ-005-023). This applies to inquiry records, quote records, acceptance events (including superseded AcceptanceEvents per FR-005), and associated audit trail entries.
- **REQ-023-004**: System MUST allow patients to request data deletion (erasure); non-protected data is deleted or anonymized; protected records (Medical Records, Financial Records, Account Profile) are retained in anonymised form, with strict access restrictions and documented legal basis.
- **REQ-023-005**: System MUST anonymize patient data in analytics and reports (no direct identifiers, quasi-identifiers masked or aggregated).
- **REQ-023-006**: System MUST maintain audit logs for all read and write access to protected records, including actor, timestamp, object, action, outcome.
- **REQ-023-007**: System MUST provide Admin views to configure retention by data category and jurisdiction and to manage DSR queues.
- **REQ-023-008**: System MUST notify Patients and Admins about DSR status updates and completion outcomes.

### Data Requirements

- **REQ-023-009**: System MUST classify data into categories: Medical Records, Financial Records, Communications, Media, Account Profile, Analytics.
- **REQ-023-010**: Each category MUST have an assigned retention policy and legal basis (with jurisdiction overrides).
- **REQ-023-011**: Audit log entries MUST be immutable; their retention follows the system PRD, Platform-Wide Rules: One 10-year retention period.
- **REQ-023-012**: Backups MUST occur at least every 6 hours with 30-day retention (per system PRD) and exclude already-deleted personal data beyond backup windows.

### Security & Privacy Requirements

- **REQ-023-013**: Deletion actions MUST purge search indexes and caches for impacted personal data.
- **REQ-023-014**: Anonymization MUST remove direct identifiers and reduce re-identification risk for quasi-identifiers.
- **REQ-023-015**: System MUST capture consent for analytics usage where applicable and honor opt-outs in non-essential analytics.

### Integration Requirements

- **REQ-023-016**: Provide Admin export of audit logs and retention reports in portable, non-proprietary formats.
- **REQ-023-017**: Provide programmatic access for DSR submission/status for Patient app integration.
- **REQ-023-018**: Provide event notifications for DSR lifecycle events to internal communication channels.

### Clarifications (Resolved)

- CL-1: Erasure handling for medical/financial records — see REQ-023-004. Access is fully restricted during the legal retention period.
- CL-3: Audit log retention — see REQ-023-011. Logs are included in compliance reporting (summaries unless otherwise requested). (REQ-023-016)

### Additional Business Rules (moved from dropped sections)

- The retention, audit-log and anonymisation rules of this module apply to the whole platform (Patient, Provider and Admin applications), not to one module only.
- Data Subject Request (DSR): This is the single deletion-request record of the platform: the patient Delete Account screen (FR-001) and the Admin deletion requests queue (FR-016) both use it, and this FR owns it.
- Verified deletion requests are completed within 30 calendar days (REQ-001-094, owned by FR-001).
- Deleted data may persist in backups until window expiry (REQ-023-012).

---

## Dependencies

Related FRs: FR-001 (Delete Account screen, account-deletion-requested event), FR-003 (patient-cancelled inquiry, Workflow 5), FR-004 (auto-cancelled quotes), FR-005 (AcceptanceEvents retained, REQ-005-023), FR-016 (Admin deletion requests queue). System modules: A-09 System Settings & Configuration (retention policy configuration, DSR management); S-03 Notification Service (DSR status notifications to users/admins).

---

## Appendix: Change Log

| Date       | Version | Changes                                           | Author       |
|------------|---------|---------------------------------------------------|--------------|
| 2026-11-22 | 1.7 | Requirements graph programme baseline: PRD compressed to the checklist structure (each rule stated once, dropped classes removed; this PRD has no screen field tables, so no field rows are tagged). No rule changes. Earlier history (v1.0 to v1.6) is in `archived/prd-baseline-2026-11-08/fr023-data-retention-compliance/` and in git history; this PRD names no change request. | Product Owner / Documentation |

---

## Appendix: Approvals

| Role            | Name | Date | Signature/Approval |
|-----------------|------|------|--------------------|

---

**Template Version**: 2.0.0 (Constitution-Compliant)  
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)  
**Based on**: FR-023 Data Retention & Compliance  
**Last Updated**: 2026-11-22
