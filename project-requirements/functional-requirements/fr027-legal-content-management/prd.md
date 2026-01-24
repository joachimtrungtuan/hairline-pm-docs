# FR-027 - Legal Content Management

**Module**: A-09: System Settings & Configuration  
**Feature Branch**: `fr027-legal-content-management`  
**Created**: 2025-11-12  
**Status**: ✅ Verified & Approved  
**Source**: FR-027 in system-prd.md; Client transcriptions (Admin Platform Part 2: terms/consent updates)

---

## Executive Summary

Provide centralized management of legal content (Terms & Conditions, Privacy Policy, Consent forms) with versioning, preview, publishing, acceptance tracking, and audit trail. Admins can draft and preview content, publish new versions, and require users (patients and providers) to accept the latest terms where applicable. The system records which user accepted which version and when, while preserving full version history and logging all changes. This improves compliance, transparency, and reduces risk from untracked changes.

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-01)**: Display current legal documents; prompt for acceptance of new versions where required; store acceptance records per version.
- **Provider Platform (PR-01/PR-06)**: Display current legal documents; prompt provider users to accept new versions; track acceptance records for provider accounts.
- **Admin Platform (A-09)**: Create, edit, preview, stage and publish legal documents; view version history; configure acceptance rules; review acceptance coverage and audit logs.
- **Shared Services (S-XX)**: Versioning, publication state, acceptance tracking, and audit logging available across tenants.

### Multi-Tenant Breakdown

**Patient Platform (P-01)**:

- View latest Terms & Conditions, Privacy Policy, and relevant Consent forms
- Accept latest versions when prompted; acceptance recorded with timestamp and version ID
- View prior acceptances (history) for personal reference

**Provider Platform (PR-01/PR-06)**:

- View and accept latest legal content as a provider user
- Review acceptance status for their organization’s users (read-only)

**Admin Platform (A-09)**:

- Draft, edit, preview, and publish legal documents
- Maintain version history and compare versions (diff summary)
- Configure acceptance rules: who must accept, and when enforcement applies
- Monitor acceptance coverage and outstanding users

**Shared Services (S-XX)**:

- Version registry for legal documents (type, locale, version, status)
- Acceptance ledger per user, per document type and version
- Audit trail for all create/edit/publish actions

### Communication Structure

**In Scope**:

- In‑app prompts to accept new versions
- Admin notifications when publication succeeds and when acceptance coverage thresholds are unmet
- User reminders to accept pending legal content (rate‑limited)

**Out of Scope**:

- Real‑time chat or legal counsel workflows
- External e‑signature platforms (future consideration)

### Entry Points

- Admin: Settings → Legal Content → Documents (T&C, Privacy, Consent) → Draft/Preview/Publish
- Patient: First‑run or on change → Acceptance prompt; Profile → Legal → View documents
- Provider: First‑run or on change → Acceptance prompt; Settings → Legal → View documents

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
4. System publishes new version and marks it current; previous version archived
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
  1. System schedules activation
  2. On effective date, new version becomes current; prompts begin
- Outcome: Controlled rollout with clear timing

**B1: Publication Reversion**:

- Trigger: Admin needs to revert to previous version due to error
- Steps:
  1. System marks previous version current again
  2. Prompts update accordingly; audit entry recorded
- Outcome: Rapid recovery with traceability

---

## Screen Specifications

### Screen 1: Admin — Legal Documents List

**Purpose**: List all legal document types and versions, and provide entry points to draft, edit, preview, and publish.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Document Type | select | Yes | T&C, Privacy, Consent | Must be one of supported types |
| Locale | select | Yes | Display locale for translation; global content only | Must be supported locale |
| Version | text | Yes | Version identifier | Must be unique per document type |
| Status | badge | Yes | Draft / Current / Archived | Only one Current per type |
| Effective Date | date | Yes | Scheduled go-live date | Must be today or future |
| Requires Acceptance | boolean | Yes | Indicates if material change gating applies | Tied to Material flag from draft |
| Last Updated By/At | text | Yes | Audit info | Read-only |
| Actions | buttons | Yes | Draft new version, Edit draft, View history, Preview, Publish (if draft ready) | Edit shown for Draft/Archived versions; Publish disabled unless draft passes validation |

**Business Rules**:

- Only authorized Admin roles can access this list.
- Only one Current version per document type at a time; publishing a new version auto-archives the prior Current.
- Publish action is global (no region targeting); locale is for translation display only.
- Edit action opens the Draft/Edit screen for Draft versions; Current/Archived versions are view-only (preview/history).

**Notes**:

- Provide filters by Document Type, Status, and Locale.
- Show warning banners for pending acceptance coverage below threshold.

---

### Screen 2: Admin — Draft/Edit Legal Document

**Purpose**: Author or edit content for a legal document version prior to publication.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Document Type | select | Yes | T&C, Privacy, Consent | Locked after version creation |
| Locale | select | Yes | Translation locale for the current version's content. Multiple locales can exist for a single version. | Must be supported locale |
| Content | rich text editor with Markdown toggle | Yes | Full legal text | Min 200 chars; max 50k chars |
| Change Summary | textarea | Yes | Human-readable summary of changes | Max 500 chars |
| Material Change | boolean | Yes | Marks if re-acceptance required | Required to set acceptance gating |
| Effective Date | date/time | Yes | When this version becomes current | Cannot be in the past |
| Version Label | text | Yes | Semantic or numeric label | Must be unique per type |

**Business Rules**:

- Autosave drafts; warn on unsaved changes before exit.
- Material Change=true triggers acceptance requirement after publish.
- Effective Date controls activation; content remains Draft until published.

**Notes**:

- Provide side-by-side preview while editing.
- Show prior version summary for context.
- Editor supports toolbar for headings, lists, links, tables; allows paste with cleanup; block quotes disabled to avoid nesting signatures.

---

### Screen 3: Admin — Preview & Publish

**Purpose**: Review draft content, confirm details, and publish globally.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Content Preview | read-only | Yes | Rendered legal text | N/A |
| Version Diff Summary | read-only | Yes | Key changes vs. prior version | Must be generated from draft |
| Effective Date | read-only | Yes | Activation time | Must be set in draft |
| Material Change | read-only | Yes | Indicates acceptance requirement | Must match draft flag |
| Publish Button | button | Yes | Executes publish | Disabled until all validations pass |

**Business Rules**:

- Publish sets status to Current on Effective Date; prior Current auto-archives.
- Publishing logs an audit entry (who/when/what) and triggers acceptance prompts if Material Change=true.
- Publication is global; no regional/locale targeting.
- When a version is published globally, the system validates that at least the English (en-US) locale content is complete. If other locales are configured for this version, the Admin UI will provide a summary of their completeness, but publishing will proceed using the English (en-US) version as the mandatory default fallback if a specific locale is missing or incomplete (as per CL-3).

**Notes**:

- Show acceptance impact summary (number of users who must re-accept).
- Provide link back to edit draft if issues are found.

---

### Screen 4: Admin — Acceptance Coverage Dashboard

**Purpose**: Monitor acceptance coverage for current and recent versions.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Document Type | select | Yes | Filter by T&C, Privacy, Consent | Must be supported type |
| Version | select | Yes | Target version for coverage view | Must exist |
| Published/Eff. Dates | text | Yes | Publication and activation timestamps | Read-only |
| Material Change | badge | Yes | Indicates gating requirement | Read-only |
| Acceptance Rate | metric | Yes | % accepted | Computed from acceptance ledger |
| Pending Users | list/count | Yes | Users who haven’t accepted | Supports pagination/export |
| Reminders Sent | count | Yes | Reminder notifications issued | Read-only |

**Business Rules**:

- Data is read-only; reminders respect rate limits.
- Filters by document type and version; supports date range for trend.

**Notes**:

- Export pending list (CSV) for follow-up.
- Show audit link for the publication event.

---

### Screen 4A: Admin — Acceptance Detail List (Drilldown)

**Purpose**: Provide a paginated list of users per version, showing accepted vs. not accepted with filters and export.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules |
|------------|------|----------|-------------|------------------|
| Document Type | select | Yes | T&C, Privacy, Consent | Must be supported type |
| Version | select | Yes | Version for the detail list | Must exist |
| User Filter | search/filter | No | Search by name/email/user ID | Input sanitized |
| Status Filter | select | Yes | Accepted / Pending | Defaults to Pending |
| Locale | select | No | Filter by locale | Must be supported locale |
| Acceptance Timestamp | text | Yes (when accepted) | When the user accepted | Read-only |
| Acceptance Channel | text | No | Web / Mobile | Read-only |
| Reminder Status | text | No | Last reminder sent timestamp | Read-only |
| Export | button | No | Export current filtered set (CSV) | Enforces rate limits |

**Business Rules**:

- Mirrors filters from Screen 4 and inherits selected version/type.
- Status defaults to Pending to focus on outstanding users.
- Export constrained by role permissions and rate limits.

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
2. Given acceptance is recorded, When the user resumes activity, Then no further prompts are shown until the next version

### User Story 3 — View Acceptance Coverage (Priority: P2)

As an Admin, I can view acceptance coverage (who has accepted which version) and follow up with users who have not yet accepted.

**Independent Test**: Publish a new version; verify coverage dashboard shows accepted/pending counts and lists of users pending.

**Acceptance Scenarios**:

1. Given a recent publication, When Admin views coverage, Then accepted and pending users are listed with timestamps/version info

### Edge Cases

- Minor updates vs. material changes: non‑material edits may not require re‑acceptance; material changes do — rules configurable
- Existing users with pending procedures: allow read‑only access until acceptance; surface prompts at safe checkpoints
- Locale mismatch: default to primary language if localized version not available; log gaps for Admin
- Rollback after partial acceptance: reverting version preserves existing acceptance records; users accepted to reverted version remain valid per policy

---

## Functional Requirements Summary

### Core Requirements

- **REQ-027-001**: Admins MUST be able to create, edit, preview, and publish legal documents (T&C, Privacy, Consent)
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

- **REQ-027-011**: Only authorized Admin roles can create/edit/publish legal documents; publication actions require explicit confirmation
- **REQ-027-012**: Users MUST have clear access to read the full content prior to acceptance; records are retained to demonstrate consent
- **REQ-027-013**: Audit trail MUST be immutable and reviewable by authorized Admins

### Integration/Communication Requirements

- **REQ-027-014**: Users SHOULD receive clear prompts and reminders for pending acceptance respecting rate limits
- **REQ-027-015**: Legal content visibility and acceptance prompts MUST be available across Patient and Provider applications

### Clarifications (Resolved)

- CL‑1: Enforcement for existing users — Block core actions until acceptance; allow read‑only access where safe. Show rate‑limited reminders. Gating occurs at sign‑in and before core transactional flows.
- CL‑2: Material vs. minor changes — Material includes changes to obligations, data use/sharing, user rights, or liability; Minor includes formatting, typo fixes, or clarifications without policy change. Only material changes require re‑acceptance; Admin marks the publish accordingly.
- CL‑3: Locale handling — If a localized version is unavailable, default to the primary language and display a discreet notice. Log a task to add the missing locale. Acceptance using the fallback is considered valid.
- CL‑4: Regional customization — Legal content is uniform globally; no location‑based variants or region‑specific publication paths are required.

---

## Key Entities

- Legal Document: type (T&C, Privacy, Consent), locale, version, status, effective date, content, change summary  
  Relationships: has many versions; current version per locale

- Acceptance Record: user reference, document type, version, locale, timestamp, channel  
  Relationships: belongs to user and document type/version

- Audit Entry: actor, action (create/edit/publish/revert), timestamp, object reference, summary  
  Relationships: references Admin actor and document version

---

## Dependencies

### Internal Dependencies

- P-01: Auth & Profile — for gating and acceptance at sign‑in and profile areas
- PR-01/PR-06: Provider Auth/Settings — provider user acceptance and settings visibility
- A-09: System Settings — legal content management and publication

### Transcription References

- Admin desire to “update terms and conditions, consent, all of these different resources” in settings: AdminPlatformPart2.txt:14–15

---

## Success Criteria

- 100% of legal content publish actions captured in audit logs with who/when/what
- ≥ 95% of active users accept required versions within 14 days of publication
- 0% access to core actions for users with pending required acceptance (when enforcement enabled)
- Version rollback completes in ≤ 5 minutes with prompts updated accordingly
- Acceptance coverage report matches user totals with ≤ 0.5% variance

---

## Assumptions

- Admins will manage all legal content centrally within A‑09 settings
- Users will accept legal content on sign‑in or when accessing core flows after a new required version is published
- Locale coverage will follow product language availability; missing locales default to primary language until added

---

## Appendix: Change Log

| Date       | Version | Changes                | Author       |
|------------|---------|------------------------|--------------|
| 2025-11-12 | 1.0     | Initial PRD creation   | AI Assistant |
| 2025-12-11 | 1.1     | Marked Verified & Approved; added locale clarifications and screen specs | AI Assistant |

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
**Last Updated**: 2025-12-11
