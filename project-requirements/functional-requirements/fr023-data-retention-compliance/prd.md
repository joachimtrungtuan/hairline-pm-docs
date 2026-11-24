# FR-023 - Data Retention & Compliance

**Module**: A-09: System Settings & Configuration (Cross-Cutting Concern)  
**Feature Branch**: `fr023-data-retention-compliance`  
**Created**: 2025-11-12  
**Status**: Draft  
**Source**: FR-023 in system-prd.md; Client transcriptions (HairlineApp-Part1.txt, Hairline-AdminPlatform-Part1.txt, Hairline-ProviderPlatformPart1.txt)

---

## Executive Summary

Establish organization-wide data retention, auditability, and privacy controls to meet healthcare and financial record-keeping obligations while honoring user privacy rights. This feature defines retention policies (one retention period for medical records, financial records and audit logs; see system PRD, Platform-Wide Rules: One 10-year retention period), enforces soft deletion for every record (nothing is physically removed before the retention period ends; see system PRD, Platform-Wide Rules: Soft deletes only), provides GDPR-compliant deletion request handling (right to erasure, met by anonymising or archiving in place), anonymizes patient data used in analytics, and maintains comprehensive audit logs for all data access and modification events. The outcome is a compliant, transparent, and testable framework applicable across Patient, Provider, and Admin applications.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform**: View retention policy; request account/data deletion; receive status updates and outcomes. (REQ-023-020)
- **Provider Platform**: View applicable retention/privacy policy; cannot permanently delete protected records; access read-only audit trail for activity by their users. (REQ-023-021, REQ-023-022, REQ-023-023)
- **Admin Platform (A-09)**: Configure retention settings (by data category/region), triage and fulfill deletion requests, review audit trails. (REQ-023-007, REQ-023-024)
- **Shared Services**: Cross-cutting job scheduling for retention enforcement (REQ-023-026); audit logging; anonymization pipeline; notification templates.

### Communication Structure

**In Scope**:

- User notifications for DSR (Data Subject Request) status changes. (REQ-023-028)
- Admin notifications for new DSRs and approaching deadlines (REQ-023-029). The submission notice to the Patient and the new-request notice to Admins use the same account-deletion-requested event (FR-001).
- Compliance reporting exports (downloadable by Admin).

**Out of Scope** (REQ-023-027):

- Real-time chat/video features (managed by other modules).
- Payment flow changes beyond record retention.
- Third-party DPO/legal tooling integrations (future consideration).
- Patient data export (data portability). It is not offered at launch. The system PRD still lists GDPR data export under this module; that line is queued for amendment, and no FR owns an export until the owner brings it back into scope.

### Entry Points

- Patient: Profile > Delete Account. The patient sees the retention policy as the retained-data text on that screen (FR-001); no separate patient policy screen exists.
- Provider: Settings → Data Policy (read-only); Activity Logs.
- Admin: Compliance dashboard → Retention Settings; DSR Queue; Audit Logs; Reports.

All three entry points: REQ-023-019. Only the Delete Account screen (FR-001) and the DSR Queue (FR-016, Patient Deletion Requests, Screen 8) are specified in an FR. The Provider Data Policy and Activity Logs screens and the Admin Retention Settings, Audit Logs and Reports screens are not specified yet, so REQ-023-007, REQ-023-016 and REQ-023-024 are platform-wide rules until a screen owner takes them.

---

## Business Workflows

### Main Flow: Deletion Request (Right to Erasure)

**Actors**: Patient, Admin, System  
**Trigger**: Patient requests deletion from Profile > Delete Account  
**Outcome**: Every category anonymised or archived in place, nothing physically removed; protected data retained in anonymised form with access restrictions; the patient's open inquiry cancelled; audit logged

**Steps**:

1. Patient submits the deletion request from the Delete Account screen (FR-001). The system records it as Pending Admin Review and sets its deadline.
2. System classifies the patient's data by category, retention and jurisdiction, using the record-type mapping below.
3. Admin reviews the classification on the DSR Queue (FR-016, Screen 8) and decides: approve, deny (A2), or find the identity proof insufficient (A1).
4. On approve, the Admin confirms that the protected categories (Medical Records, Financial Records, Account Profile) are retained in anonymised form with restricted access. Every patient has an Account Profile, so this confirmation is part of every approval.
5. System checks the active obligations again and refreshes the classification. If an obligation exists, approval is blocked (A3). Otherwise the request becomes In Progress.
6. System cancels the patient's open inquiry through FR-003 (REQ-003-103) before anything is anonymised.
7. System anonymises or archives in place the data of every category and restricts access to the protected records.
8. System records the actions in the audit log, sets the request to Fulfilled and sends the patient one outcome notice with the actions taken and the legal basis and scope of the retained categories.

### Alternative Flows

**A1: Verification Required**

- Trigger: At review, the Admin finds the identity proof of the request insufficient. FR-001 already re-authenticates the patient at submission; the Admin decides whether more proof is needed and may contact the patient (REQ-016-170).
- Steps:
  1. System sets the request to Verification Required and notifies the Patient.
  2. Patient provides additional verification.
  3. Admin validates it on the DSR Queue; the request returns to Pending Admin Review and review resumes at Main Flow step 3.
- Exit: If the patient does not supply the proof, or the proof stays insufficient, the request stays open until an Admin denies it with a reason (A2). It never closes by itself.
- Outcome: Deletion request processing proceeds; the 30-day deadline always runs from submission and does not pause during verification. After the deadline the queue shows the request as overdue and it stays open.

**A2: Denied**

- Trigger: An Admin denies the request at review, or because verification cannot be completed.
- Steps:
  1. Admin denies the request on the DSR Queue and enters a reason (required).
  2. System sets the request to Denied and notifies the Patient with the reason.
- Outcome: Nothing is cancelled and nothing is anonymised; the request stays auditable. The patient may submit a new deletion request.

**A3: Blocked by an obligation**

- Trigger: At approval, the patient has an active obligation (REQ-023-038).
- Steps:
  1. System keeps the request in Pending Admin Review, marks it blocked by obligation and tells the Patient the expected timeline.
  2. When the obligation clears, the Admin approves again (Main Flow step 3).
- Outcome: The 30-day deadline keeps running. If it passes while the request is blocked, the queue shows it as overdue and the breach is excused.

Rules carried by the flows above: Main Flow steps 1 to 8 (REQ-023-030, REQ-023-037, REQ-023-031, REQ-023-032, REQ-023-036, REQ-023-038, REQ-023-042, REQ-023-004, REQ-023-033, REQ-023-046); A1 (REQ-023-034, REQ-023-041); A2 (REQ-023-043); A3 (REQ-023-038, REQ-023-041).

---

## User Stories

### User Story 1 - Delete My Account/Data (Priority: P1)

As a Patient, I want to request deletion of my account and personal data so that I can exercise my right to be forgotten.

**Independent Test**: Submit deletion request, verify anonymization/archival actions and communication of legally retained records within 30 days.

**Acceptance Scenarios**:

1. Given a deletion request with no active obligation, When approved by Admin, Then the open inquiry is cancelled first, every category is anonymised or archived in place, and the protected records are restricted.
2. Given the deletion request completion, When patient reviews notification, Then it lists actions taken and legal basis for any retained records.
3. Given a deletion request, When an Admin denies it with a reason, Then the patient is notified with the reason and nothing is cancelled or anonymised.

### User Story 2 - Review Audit Trail (Priority: P1)

As an Admin, I need a complete audit trail of access and modifications to protected records so I can investigate incidents and demonstrate compliance.

**Independent Test**: Perform seeded read/write events and verify audit log captures actor, timestamp, action, object, and outcome.

**Acceptance Scenarios**:

1. Given protected data access, When a user views a medical record, Then an audit entry records who, when, what, and outcome.
2. Given a modification to a protected record, When the change is saved, Then the audit log includes before/after metadata and actor.

### Edge Cases

- Patient submits multiple DSRs concurrently → System merges them into one request with clear status; SLA applies per consolidated request, from the earliest submission date. (REQ-023-037)
- An obligation exists at approval (for example a booking made after the request was submitted) → Approval is blocked, the request stays Pending Admin Review, and the patient is told the expected timeline. (REQ-023-038)
- Jurisdiction conflict (e.g., EU vs non-EU residency) → The longer retention period applies; the request is flagged for Admin review before approval. (REQ-023-039, REQ-023-045)
- Patient requests data deletion after cancelling their inquiry → Cancelled inquiry is a terminal state with no active obligation; deletion request should proceed normally. Cancelled inquiry records, cascaded cancelled quotes, and associated audit entries are retained per the system PRD, Platform-Wide Rules: One 10-year retention period and REQ-023-003 even after the deletion request is fulfilled — retained inquiry and quote records are kept in anonymised form. (REQ-023-040)
- Patient still has an open inquiry when the request is approved → The system cancels it at approval, never at submission. A denied or blocked request cancels nothing. (REQ-023-042)
- Patient submits a new request after a denial → Allowed; it is a new request with its own deadline. (REQ-023-043)

---

## Functional Requirements Summary

### Core Requirements

- **REQ-023-001**: Retired. Retention of medical records (including head-scan media), financial transaction records and audit logs, and the ban on hard-deletion before expiry, follow the system PRD, Platform-Wide Rules: One 10-year retention period.
- **REQ-023-003**: Every delete MUST be a soft delete (REQ-SYS-003): the record is archived or anonymised in place and is never physically removed before the retention period ends (REQ-SYS-002). The protected categories (Medical Records, Financial Records, Account Profile) are additionally restricted, with access limited to the legal purpose. Patient-cancelled inquiries (FR-003 Workflow 5), inquiries cancelled by the system when a deletion request is approved (REQ-023-042), and all records generated from the cancellation cascade — including auto-cancelled quotes with status "Cancelled (Inquiry Cancelled)" per FR-004 — are subject to the same retention rules as completed inquiries and quotes. AcceptanceEvents are retained and never deleted (FR-005 REQ-005-023). This applies to inquiry records, quote records, acceptance events (including superseded AcceptanceEvents per FR-005), and associated audit trail entries, which are kept unchanged (REQ-023-011).
- **REQ-023-004**: System MUST allow patients to request data deletion (erasure). On an approved request no category is physically removed (REQ-SYS-002, REQ-SYS-003): the personal data of the non-protected categories (Communications, Media, Analytics) is anonymised in place, or archived and made inaccessible; the protected categories (Medical Records, Financial Records, Account Profile) are retained in anonymised form, with strict access restrictions and documented legal basis.
- **REQ-023-005**: System MUST anonymize patient data in analytics and reports (no direct identifiers, quasi-identifiers masked or aggregated).
- **REQ-023-006**: System MUST maintain audit logs for all read and write access to protected records, including actor, timestamp, object, action, outcome. The medical data access log and admin action log (FR-016) and the patient audit log (FR-001) feed this one audit record.
- **REQ-023-007**: System MUST provide Admin views to configure retention by data category and jurisdiction (never below 10 years, REQ-023-045) and to manage DSR queues.
- **REQ-023-008**: System MUST notify Patients and Admins about DSR status updates and completion outcomes.

### Data Requirements

- **REQ-023-009**: System MUST classify data into categories: Medical Records, Financial Records, Communications, Media, Account Profile, Analytics. Head and monitoring scan media belong to Medical Records, and every record type belongs to exactly one category (REQ-023-044).
- **REQ-023-010**: Each category MUST have an assigned retention policy and legal basis (with jurisdiction overrides that may only extend the period, REQ-023-045).
- **REQ-023-011**: Audit log entries MUST be immutable; their retention follows the system PRD, Platform-Wide Rules: One 10-year retention period. An entry is never edited and never marked deleted: after a fulfilled deletion request it is anonymised by removing the identifying data from the patient record the entry points to, so the entry stays unchanged and no longer identifies the patient.
- **REQ-023-012**: Backups MUST occur at least every 6 hours with 30-day retention (per system PRD) and exclude already-deleted personal data beyond backup windows.
- **REQ-023-044**: System MUST assign every record type to exactly one data category by the record-type mapping below. Reviews, messages and support cases are Communications and are anonymised in place. Inquiries are Medical Records, and quotes, acceptance events and bookings are Financial Records; they are retained records under REQ-023-003 and REQ-023-040. Scan media are Medical Records.
- **REQ-023-045**: The retention period of every category MUST default to 10 years and MUST NOT be set below 10 years (REQ-SYS-002). A jurisdiction override may only extend the period, and the stricter retention on a jurisdiction conflict is the longer period.

#### Record-Type Mapping

Protected categories are Medical Records, Financial Records and Account Profile. The other three are not protected, but nothing in any category is physically removed.

| Record type | Category | Protected | Treatment on an approved request |
|-------------|----------|-----------|----------------------------------|
| Inquiry, including a cancelled inquiry | Medical Records | Yes | Retained in anonymised form, access restricted |
| Scan media (head and monitoring) | Medical Records | Yes | Retained in anonymised form, access restricted |
| Quote, including a cascade-cancelled quote | Financial Records | Yes | Retained in anonymised form, access restricted |
| Acceptance event | Financial Records | Yes | Retained in anonymised form, never deleted |
| Booking | Financial Records | Yes | Retained in anonymised form, access restricted |
| Payment and refund | Financial Records | Yes | Retained in anonymised form, access restricted |
| Profile, consent and preferences | Account Profile | Yes | Retained in anonymised form, access restricted |
| Review | Communications | No | Anonymised in place |
| Message | Communications | No | Anonymised in place |
| Support case | Communications | No | Anonymised in place |
| Notification record | Communications | No | Anonymised in place |
| Other uploaded media | Media | No | Archived and made inaccessible, or anonymised in place |
| Analytics event | Analytics | No | Anonymised in place |

### Security & Privacy Requirements

- **REQ-023-013**: Deletion actions MUST purge search indexes and caches for impacted personal data.
- **REQ-023-014**: Anonymization MUST remove direct identifiers and reduce re-identification risk for quasi-identifiers.
- **REQ-023-015**: System MUST capture consent for analytics usage where applicable and honor opt-outs in non-essential analytics.

### Integration Requirements

- **REQ-023-016**: Provide Admin export of audit logs and retention reports in portable, non-proprietary formats.
- **REQ-023-017**: Provide programmatic access for DSR submission/status for Patient app integration.
- **REQ-023-018**: Provide event notifications for DSR lifecycle events to internal communication channels.

### Deletion Request Handling

- **REQ-023-028**: Patients are notified of each DSR status change: submission, verification required, in progress, blocked by obligation (with the expected timeline), denied (with the reason), and fulfilled.
- **REQ-023-029**: Admins are notified of new DSRs and, 7 calendar days before the deadline, of an approaching deadline.
- **REQ-023-031**: System classifies the patient's data by category and applicable retention/jurisdiction when a deletion request is processed, and refreshes the classification when the Admin approves.
- **REQ-023-032**: Admin reviews the classification and approves the action before anonymization or restriction is performed; the Admin may instead deny the request (REQ-023-043) or find the identity proof insufficient (REQ-023-034).
- **REQ-023-033**: System records the anonymisation actions in the audit log and notifies the patient of the outcome once, listing the actions taken and the legal basis and scope of the retained categories.
- **REQ-023-034**: An Admin decides at review whether the identity proof of a deletion request is sufficient. When it is not, the request is set to Verification Required and the patient is notified; the patient provides additional verification and an Admin validates it, which returns the request to Pending Admin Review. A request in Verification Required stays open until an Admin validates the proof or denies the request with a reason (REQ-023-043); it never closes by itself.
- **REQ-023-036**: Every approval includes the Admin's confirmation that the protected categories (Medical Records, Financial Records, Account Profile) are retained in anonymised form with restricted access, because every patient account has an Account Profile; anonymisation of the other categories completes with it.
- **REQ-023-037**: When a patient submits multiple DSRs concurrently, the system merges them into one request with a clear status; the SLA applies per consolidated request and the merged request keeps the earliest submission date.
- **REQ-023-038**: System MUST keep one list of active obligations: an inquiry at the Accepted stage or later that is not Cancelled (FR-003 REQ-003-103), an active booking, treatment or aftercare in progress, a payment in progress, and a pending refund. FR-001 and FR-003 block the submission of a request while an obligation of the list exists. An obligation that arises after submission blocks approval: the system checks the list again when the Admin approves, keeps the request Pending Admin Review, marks it blocked by obligation and tells the patient the expected timeline. Nothing else is restricted for the patient while the request is pending.
- **REQ-023-039**: On a jurisdiction conflict (for example EU versus non-EU residency), the system applies the longer retention period (REQ-023-045) and flags the request for Admin review before approval.
- **REQ-023-040**: A deletion request made after the patient cancelled an inquiry proceeds normally, because a cancelled inquiry is a terminal state with no active obligation. Inquiries cancelled by the patient, inquiries cancelled by the system at approval (REQ-023-042), cascaded cancelled quotes, and associated audit entries are retained per the system PRD, Platform-Wide Rules: One 10-year retention period and REQ-023-003 even after the deletion request is fulfilled; the retained inquiry and quote records are kept in anonymised form and the audit entries are kept unchanged (REQ-023-011).
- **REQ-023-041**: The 30-day deadline of a deletion request always runs from submission (the earliest submission date of a merged request) and does not pause during verification or while an obligation blocks approval. When the deadline passes on an open request, the queue shows it as overdue and the request stays open; an overdue request blocked by an obligation is shown as an excused breach.
- **REQ-023-042**: When an Admin approves a deletion request, the system MUST cancel the patient's open inquiry through FR-003 (REQ-003-103) before any data is anonymised, so the cancellation and its provider notices run on the identifiable record. The cancellation happens at approval, never at submission; a denied request and a request blocked by an obligation cancel nothing. The cancelled inquiry and quotes are retained under REQ-023-003 and REQ-023-040.
- **REQ-023-043**: An Admin MAY deny a deletion request on the DSR Queue (FR-016) while it is open, including a request in Verification Required that cannot be completed. A denial requires a reason; the system sets the status to Denied, notifies the patient with the reason, cancels nothing and anonymises nothing, and the request stays auditable. The patient may submit a new deletion request after a denial.
- **REQ-023-046**: The status of a deletion request is set only as follows: Pending Admin Review at submission, and again when an Admin validates the verification or an obligation block clears; Verification Required when an Admin finds the proof insufficient; In Progress when an Admin approves and the obligation check passes; Fulfilled when the system sends the outcome notice after anonymisation; Denied when an Admin denies. The request also carries two flags, blocked by obligation and jurisdiction review required. FR-016 shows the status and owns the deletion certificate (REQ-016-062); it does not set Fulfilled.

### Clarifications (Resolved)

- CL-1: Erasure handling for medical/financial records — see REQ-023-004. Access is fully restricted during the legal retention period.
- CL-3: Audit log retention — see REQ-023-011. Logs are included in compliance reporting (summaries unless otherwise requested). (REQ-023-016)

### Additional Business Rules (moved from dropped sections)

- The retention, audit-log and anonymisation rules of this module apply to the whole platform (Patient, Provider and Admin applications), not to one module only.
- Data Subject Request (DSR): This is the single deletion-request record of the platform: the patient Delete Account screen (FR-001) and the Admin deletion requests queue (FR-016) both use it, and this FR owns it.
- Deletion requests are completed within 30 calendar days of submission (REQ-023-041; REQ-001-094 and REQ-016-188 restate the clock).
- Deleted data may persist in backups until window expiry (REQ-023-012).

---

## Dependencies

Related FRs: FR-001 (Delete Account screen, account-deletion-requested event, submission blocks), FR-003 (inquiry cancelled at approval, REQ-003-103; patient-cancelled inquiry, Workflow 5), FR-004 (auto-cancelled quotes), FR-005 (AcceptanceEvents retained, REQ-005-023), FR-016 (Admin deletion requests queue, approval and denial, deletion certificate). System modules: A-09 System Settings & Configuration (retention policy configuration, DSR management); S-03 Notification Service (DSR status notifications to users/admins).

---

## Appendix: Change Log

| Date       | Version | Changes                                           | Author       |
|------------|---------|---------------------------------------------------|--------------|
| 2026-11-22 | 1.7 | Requirements graph programme baseline: PRD compressed to the checklist structure (each rule stated once, dropped classes removed; this PRD has no screen field tables, so no field rows are tagged). No rule changes. Earlier history (v1.0 to v1.6) is in `archived/prd-baseline-2026-11-08/fr023-data-retention-compliance/` and in git history; this PRD names no change request. | Product Owner / Documentation |
| 2026-11-24 | 1.8 | Logic review pass 1: approval cancels the open inquiry through FR-003 before anonymisation; nothing is physically removed in any category; Denied outcome added; one obligation list blocks approval while the 30-day clock keeps running; status lifecycle, verification states and flags defined; one protected list and the exclusion confirmation moved into the main flow; record-type mapping added; audit entries anonymised by unlinking; retention default and floor of 10 years with longer-only overrides; deadline-approaching threshold and merged-request date set; patient data export stated out of scope. | Product Owner / Documentation |

---

## Appendix: Approvals

| Role            | Name | Date | Signature/Approval |
|-----------------|------|------|--------------------|

---

**Template Version**: 2.0.0 (Constitution-Compliant)  
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)  
**Based on**: FR-023 Data Retention & Compliance  
**Last Updated**: 2026-11-24
