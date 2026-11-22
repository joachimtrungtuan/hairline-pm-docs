# FR-027 - Legal Content Management

**Module**: A-09: System Settings & Configuration  
**Feature Branch**: `fr027-legal-content-management`  
**Created**: 2025-11-12  
**Status**: ✅ Verified & Approved  
**Source**: FR-027 in system-prd.md; Client transcriptions (Admin Platform Part 2: terms/consent updates)

---

## Executive Summary

Provide centralized management of legal content (Terms & Conditions, Privacy Policy, Consent forms, Cancellation Policy) with versioning, preview, publishing, acceptance tracking, and audit trail. Admins can draft and preview content, publish new versions, and require users (patients and providers) to accept the latest terms where applicable. The system records which user accepted which version and when, while preserving full version history and logging all changes. This improves compliance, transparency, and reduces risk from untracked changes.

> **Note on Cancellation Policy**: Cancellation Policy is a read-only informational document that does NOT require user acceptance or consent confirmation. It is managed through the same versioning and publishing pipeline as other legal documents but the `Requires Acceptance` flag is always `No`. It is surfaced to patients in the quote acceptance context (FR-005) for transparency. (REQ-027-026)

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-01)**: Display current legal documents; prompt for acceptance of new versions where required; store acceptance records per version.
- **Provider Platform (PR-01/PR-06)**: Display current legal documents; prompt provider users to accept new versions; track acceptance records for provider accounts.
- **Admin Platform (A-09)**: Create, edit, preview, stage and publish legal documents; view version history; configure acceptance rules; review acceptance coverage and audit logs.
- **Shared Services (S-XX)**: Versioning, publication state, acceptance tracking, and audit logging available across tenants.

### Multi-Tenant Breakdown

**Patient Platform (P-01)**:

- View latest Terms & Conditions, Privacy Policy, Cancellation Policy, and relevant Consent forms (REQ-027-017)
- Accept latest versions when prompted; acceptance recorded with timestamp and version ID

**Provider Platform (PR-01/PR-06)**:

- View and accept latest legal content as a provider user (REQ-027-019)

**Admin Platform (A-09)**:

- Draft, edit, preview, and publish legal documents
- Maintain version history and compare versions (diff summary)
- Configure acceptance rules: who must accept, and when enforcement applies (REQ-027-021)
- Monitor acceptance coverage and outstanding users

**Shared Services (S-XX)**:

- Version registry for legal documents (type, locale, version, status)
- Acceptance ledger per user, per document type and version
- Audit trail for all create/edit/publish actions

### Communication Structure

**In Scope**:

- In‑app prompts to accept new versions
- Admin notifications when publication succeeds and when acceptance coverage thresholds are unmet (REQ-027-022, REQ-027-023)
- User reminders to accept pending legal content (rate‑limited)

**Out of Scope**:

- Real‑time chat or legal counsel workflows (REQ-027-025)
- External e‑signature platforms (future consideration) (REQ-027-025)

### Entry Points

- Admin: Settings → Legal Content → Documents (T&C, Privacy, Consent, Cancellation Policy) → Draft/Preview/Publish (REQ-027-016)
- Patient: First‑run or on change → Acceptance prompt; Settings → Terms & Conditions; Settings → Privacy & Security → Privacy Policy (REQ-027-016)
- Provider: First‑run or on change → Acceptance prompt; Settings → Legal → View documents (REQ-027-016)

---

## Business Workflows

### Main Flow: Admin Publishes New Legal Version

**Actors**: Admin, System  
**Trigger**: Admin finalizes draft and selects Publish  
**Outcome**: New version becomes current; acceptance rules apply; audit entry recorded

**Steps**:

1. Admin drafts or edits legal content (select document type and locale)
2. Admin previews content and reviews change summary
3. Admin sets publication details (effective date, acceptance requirement scope)
4. System publishes the new version; it becomes current on its effective date (until then it is Scheduled and the previous version stays current), and the previous version is then archived
5. System records audit entry (who/when/what changed) and notifies Admin
6. System triggers user acceptance prompts based on configured scope

### Main Flow: User Accepts New Version

**Actors**: Patient/Provider user, System  
**Trigger**: User signs in after a new required version is published  
**Outcome**: Acceptance captured; user proceeds to core functions

**Steps**:

1. User is shown the current legal documents requiring acceptance
2. User reviews content and accepts
3. System records acceptance (user, document type, version, timestamp, locale)
4. System resumes normal access without further prompts until next required version

### Alternative Flows

**A1: Scheduled Effective Date**:

- Trigger: Admin sets a future effective date
- Steps:
  1. System marks the new version Scheduled; the previous version stays Current until the effective date
  2. On effective date, new version becomes current and the previous version is archived; prompts begin
- Outcome: Controlled rollout with clear timing

**B1: Restoring an Earlier Version**:

- Trigger: Admin needs to go back to the text of an earlier version due to error
- Steps:
  1. There is no revert button; Admin creates a new draft from the old version
  2. Admin publishes the restored text as a new version through the normal publishing flow
  3. Prompts update accordingly; audit entry recorded
- Outcome: Rapid recovery with traceability; users who accepted only the replaced version are asked to accept the restored one

---

## Screen Specifications

### Screen 1: Admin — Legal Documents List

**Purpose**: List all legal document types and versions, and provide entry points to draft, edit, preview, and publish.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Document Type | select | Yes | T&C, Privacy, Consent, Cancellation Policy | Must be one of supported types | ENT-legal-document.document_type |
| Locale | select | Yes | Display locale for translation; global content only | Must be supported locale (REQ-027-046) | ENT-legal-document.locale |
| Version | text | Yes | Version identifier | Must be unique per document type (REQ-027-040) | ENT-legal-document.version |
| Status | badge | Yes | Draft / Scheduled / Current / Archived | See REQ-027-029 and REQ-027-030. | ENT-legal-document.status |
| Effective Date | date | Yes | Scheduled go-live date | Must be today or future (REQ-027-041) | ENT-legal-document.effective_date |
| Requires Acceptance | boolean | Yes | Indicates if material change gating applies | Tied to Material flag from draft (REQ-027-027) | ENT-legal-document.requires_acceptance |
| Last Updated By/At | text | Yes | Audit info | Read-only | ENT-legal-document.last_updated_by, ENT-legal-document.last_updated_at |
| Actions | buttons | Yes | Draft new version, Edit draft, View history, Preview, Publish (if draft ready) | See REQ-027-049 and REQ-027-050. | no graph field (control) |

**Business Rules**:

- See REQ-027-011.
- Only one Current version per document type at a time; when a newly published version becomes Current, the prior Current is auto-archived. (REQ-027-029)
- Publish action is global (no region targeting); locale is for translation display only. (REQ-027-003)
- Edit action opens the Draft/Edit screen for Draft versions; Current/Archived versions are view-only (preview/history). (REQ-027-049)

**Notes**:

- Provide filters by Document Type, Status, and Locale.
- Show warning banners for pending acceptance coverage below the Admin-set threshold. (REQ-027-024)

---

### Screen 2: Admin — Draft/Edit Legal Document

**Purpose**: Author or edit content for a legal document version prior to publication.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Document Type | select | Yes | T&C, Privacy, Consent, Cancellation Policy | Locked after version creation (REQ-027-044) | ENT-legal-document.document_type |
| Locale | select | Yes | Translation locale for the current version's content. Multiple locales can exist for a single version. | See REQ-027-046. | ENT-legal-document.locale |
| Content | rich text editor with Markdown toggle | Yes | Full legal text | Min 200 chars; max 50k chars (REQ-027-042) | ENT-legal-document.content |
| Change Summary | textarea | Yes | Human-readable summary of changes | Max 500 chars (REQ-027-043) | ENT-legal-document.change_summary |
| Material Change | boolean | Yes | Marks if re-acceptance required | Required to set acceptance gating (REQ-027-045) | ENT-legal-document.material_change |
| Effective Date | date/time | Yes | When this version becomes current | See REQ-027-041. | ENT-legal-document.effective_date |
| Version Label | text | Yes | Semantic or numeric label | See REQ-027-040. | ENT-legal-document.version |

**Business Rules**:

- Autosave drafts; warn on unsaved changes before exit. (REQ-027-047)
- Material Change=true triggers acceptance requirement after publish. (REQ-027-004)
- Effective Date controls activation; content remains Draft until published. (REQ-027-048)

**Notes**:

- Provide side-by-side preview while editing.
- Show prior version summary for context.
- Editor supports toolbar for headings, lists, links, tables; allows paste with cleanup; block quotes disabled to avoid nesting signatures. (REQ-027-051)

---

### Screen 3: Admin — Preview & Publish

**Purpose**: Review draft content, confirm details, and publish globally.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Content Preview | read-only | Yes | Rendered legal text | N/A | ENT-legal-document.content |
| Version Diff Summary | read-only | Yes | Key changes vs. prior version | Must be generated from draft (REQ-027-050) | ENT-legal-document.version_diff_summary |
| Effective Date | read-only | Yes | Activation time | Must be set in draft (REQ-027-050) | ENT-legal-document.effective_date |
| Material Change | read-only | Yes | Indicates acceptance requirement | Must match draft flag (REQ-027-050) | ENT-legal-document.material_change |
| Publish Button | button | Yes | Executes publish | Disabled until all validations pass (REQ-027-050) | no graph field (control) |

**Business Rules**:

- See REQ-027-029 and REQ-027-030.
- Publishing logs an audit entry (REQ-027-007) and triggers acceptance prompts if Material Change=true (REQ-027-004).
- See REQ-027-003.
- When a version is published globally, the system validates that at least the English (en-US) locale content is complete. If other locales are configured for this version, the Admin UI will provide a summary of their completeness, but publishing will proceed using the platform default language (English, en-US) version as the single fallback if a specific locale is missing or incomplete (as per CL-3). (REQ-027-036)

**Notes**:

- Show acceptance impact summary (number of users who must re-accept; REQ-027-052; ENT-legal-document.reaccept_user_count).
- Provide link back to edit draft if issues are found.

---

### Screen 4: Admin — Acceptance Coverage Dashboard

**Purpose**: Monitor acceptance coverage for current and recent versions.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Document Type | select | Yes | Filter by T&C, Privacy, Consent, Cancellation Policy | Must be supported type | ENT-legal-document.document_type |
| Version | select | Yes | Target version for coverage view | Must exist | ENT-legal-document.version |
| Published/Eff. Dates | text | Yes | Publication and activation timestamps | Read-only | ENT-legal-document.published_at, ENT-legal-document.effective_date |
| Material Change | badge | Yes | Indicates gating requirement | Read-only | ENT-legal-document.material_change |
| Acceptance Rate | metric | Yes | % accepted, out of the users who must accept that document | Computed from acceptance ledger (REQ-027-053) | ENT-legal-document.acceptance_rate |
| Pending Users | list/count | Yes | Users who haven’t accepted (REQ-027-053) | Supports pagination/export | ENT-legal-document.pending_user_count |
| Reminders Sent | count | Yes | Reminder notifications issued | Read-only | ENT-legal-document.reminders_sent_count |

**Business Rules**:

- Data is read-only; reminders respect the Admin-set reminder limit. (REQ-027-054, REQ-027-014)
- Filters by document type and version; supports date range for trend.

**Notes**:

- Export pending list (CSV) for follow-up. (REQ-027-055)
- Show audit link for the publication event.

---

### Screen 4A: Admin — Acceptance Detail List (Drilldown)

**Purpose**: Provide a paginated list of users per version, showing accepted vs. not accepted with filters and export.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Document Type | select | Yes | T&C, Privacy, Consent | Must be supported type | ENT-legal-acceptance.document_type |
| Version | select | Yes | Version for the detail list | Must exist | ENT-legal-acceptance.version |
| User Filter | search/filter | No | Search by name/email/user ID | Input sanitized (REQ-027-057) | ENT-legal-acceptance.user_id |
| Status Filter | select | Yes | Accepted / Pending | See REQ-027-056. | no graph field (control) |
| Locale | select | No | Filter by locale | See REQ-027-046. | ENT-legal-acceptance.locale |
| Acceptance Timestamp | text | Yes (when accepted) | When the user accepted | Read-only | ENT-legal-acceptance.accepted_at |
| Acceptance Channel | text | No | Web / Mobile | Read-only | ENT-legal-acceptance.channel |
| Reminder Status | text | No | Last reminder sent timestamp | Read-only | ENT-legal-reminder.sent_at |
| Export | button | No | Export current filtered set (CSV) | See REQ-027-055. | no graph field (control) |

**Business Rules**:

- Mirrors filters from Screen 4 and inherits selected version/type. (REQ-027-056)
- Status defaults to Pending to focus on outstanding users. (REQ-027-056)
- Export constrained by role permissions and rate limits. (REQ-027-055)

**Notes**:

- Accessed via drilldown from Pending Users on Screen 4 or via a “View Details” link.
- Include pagination and sorting by acceptance timestamp and user ID.

---

## User Scenarios & Testing

### User Story 1 — Publish Legal Document (Priority: P1)

As an Admin, I can draft, preview, and publish a new version of a legal document with an effective date so that the correct terms are shown to users and acceptance is tracked.

**Independent Test**: Publish a new version in staging; verify version status changes to current on effective date and audit entry exists.

**Acceptance Scenarios**:

1. Given a draft version, When Admin publishes with an effective date, Then the system sets it as current at the scheduled time and archives the prior version
2. Given a published version, When Admin reviews audit logs, Then the change is recorded with who/when/what changed

### User Story 2 — Accept New Terms (Priority: P1)

As a Patient or Provider user, I must review and accept the latest legal documents before continuing to use the platform when acceptance is required.

**Independent Test**: Seed a user on an older accepted version; publish a new required version; verify prompt, acceptance capture, and access restored after acceptance.

**Acceptance Scenarios**:

1. Given a new required version, When a user signs in, Then the system prompts for acceptance before accessing core features
2. Given acceptance is recorded, When the user resumes activity, Then no further prompts are shown until the next version (REQ-027-035)

### User Story 3 — View Acceptance Coverage (Priority: P2)

As an Admin, I can view acceptance coverage (who has accepted which version) and follow up with users who have not yet accepted.

**Independent Test**: Publish a new version; verify coverage dashboard shows accepted/pending counts and lists of users pending.

**Acceptance Scenarios**:

1. Given a recent publication, When Admin views coverage, Then accepted and pending users are listed with timestamps/version info

### Edge Cases

- Minor updates vs. material changes: non‑material edits may not require re‑acceptance; material changes do — rules configurable (REQ-027-004)
- Existing users with pending procedures: allow read‑only access until acceptance; surface prompts at safe checkpoints (REQ-027-034)
- Locale mismatch: fall back to the platform default language (English) if a localized version is not available; log gaps for Admin (REQ-027-036, REQ-027-037)
- Restoring an earlier text after partial acceptance: the restored text is published as a new version; existing acceptance records are preserved; users who accepted only the version that was replaced are asked to accept the restored version (REQ-027-031, REQ-027-032)

---

## Functional Requirements Summary

### Core Requirements

- **REQ-027-001**: Admins MUST be able to create, edit, preview, and publish legal documents (T&C, Privacy, Consent, Cancellation Policy)
- **REQ-027-002**: System MUST maintain version history with timestamps and change tracking; previous versions are preserved for reference
- **REQ-027-003**: Admins MUST be able to schedule an effective date for publication; publication applies globally (no regional variants)
- **REQ-027-004**: System MUST require acceptance for material changes as configured, prompting users appropriately
- **REQ-027-005**: System MUST track which user accepted which document type and version, with timestamp and locale displayed
- **REQ-027-006**: System MUST provide a coverage view for Admin to see acceptance status and follow‑up needs
- **REQ-027-007**: All legal content changes MUST be logged with who/when/what changed (audit trail)

### Data Requirements

- **REQ-027-008**: Legal document entities MUST include: type, locale (for translation only, no regional content variants), version, status (draft/current/archived), effective date, change summary
- **REQ-027-009**: Acceptance records MUST include: user, document type, version, timestamp, locale, and acceptance channel
- **REQ-027-010**: Version comparisons MUST present human‑readable change summaries (no raw diffs required for end‑users)

### Security & Privacy Requirements

- **REQ-027-011**: Only authorized Admin roles can access the Legal Documents list and create/edit/publish legal documents; publication actions require explicit confirmation
- **REQ-027-012**: Users MUST have clear access to read the full content prior to acceptance; records are retained to demonstrate consent
- **REQ-027-013**: Audit trail MUST be immutable and reviewable by authorized Admins

### Integration/Communication Requirements

- **REQ-027-014**: Users SHOULD receive clear prompts and reminders for pending acceptance respecting rate limits
- **REQ-027-015**: Legal content visibility and acceptance prompts MUST be available across Patient and Provider applications

### Clarifications (Resolved)

- CL‑1: Enforcement for existing users — Block core actions until acceptance; allow read‑only access where safe. Show rate‑limited reminders. Gating occurs at sign‑in and before core transactional flows. (REQ-027-033)
- CL‑2: Material vs. minor changes — Material includes changes to obligations, data use/sharing, user rights, or liability; Minor includes formatting, typo fixes, or clarifications without policy change. Only material changes require re‑acceptance; Admin marks the publish accordingly. (REQ-027-028)
- CL‑3: Locale handling — If a localized version is unavailable, fall back to the platform default language (English) and display a discreet notice. Log a task to add the missing locale. Acceptance using the fallback is considered valid. (REQ-027-036, REQ-027-037, REQ-027-038)
- CL‑4: Regional customization — Legal content is uniform globally; no location‑based variants or region‑specific publication paths are required. (REQ-027-003)
- CL‑5: Admin-set limits — The acceptance coverage warning threshold, the reminder limit and the export limit are set by Admin; none has a default value. FR-027 owns the acceptance rules setting (who must accept and when enforcement applies) and the acceptance coverage threshold setting.

---

## Dependencies

Related FRs: FR-005 (quote acceptance context where the Cancellation Policy is shown), FR-009 (provider team and role management). Platform areas: P-01 Auth & Profile (gating and acceptance at sign-in and profile areas); PR-01/PR-06 Provider Auth/Settings (provider user acceptance and settings visibility); A-09 System Settings (legal content management and publication).

---

## Appendix: Change Log

| Date       | Version | Changes                | Author       |
|------------|---------|------------------------|--------------|
| 2026-11-22 | 1.5 | Requirements graph programme baseline: PRD compressed to the checklist structure (each rule stated once, field rows tagged with graph field ids, dropped classes removed). No rule changes. Earlier history (v1.0 to v1.4) is in `archived/prd-baseline-2026-11-08/fr027-legal-content-management/` and in git history. The PRD names no change request. | Product Owner / Documentation |

---

## Appendix: Approvals

| Role            | Name | Date | Signature/Approval |
|-----------------|------|------|--------------------|
| Product Owner   | TBD  | 2025-12-11 | ✅ Approved |
| Technical Lead  | TBD  | 2025-12-11 | ✅ Approved |
| Stakeholder     | TBD  | 2025-12-11 | ✅ Approved |

---

**Template Version**: 2.0.0 (Constitution-Compliant)  
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)  
**Based on**: FR-027 Legal Content Management  
**Last Updated**: 2026-11-22
