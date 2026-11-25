# FR-027 - Legal Content Management

**Module**: A-09: System Settings & Configuration  
**Feature Branch**: `fr027-legal-content-management`  
**Created**: 2025-11-12  
**Status**: ✅ Verified & Approved  
**Source**: FR-027 in system-prd.md; Client transcriptions (Admin Platform Part 2: terms/consent updates)

---

## Executive Summary

Provide centralized management of legal content (Terms & Conditions, Privacy Policy, Consent forms, Cancellation Policy) with versioning, preview, publishing, acceptance tracking, and audit trail. Admins can draft and preview content, publish new versions, and require users (patients and providers) to accept the latest terms where applicable. The system records which user accepted which version and when, while preserving full version history and logging all changes. This improves compliance, transparency, and reduces risk from untracked changes.

> **Note on Cancellation Policy**: Cancellation Policy is a read-only informational document that has no per-version acceptance record in this module's acceptance tracking. It is managed through the same versioning and publishing pipeline as other legal documents but the `Requires Acceptance` flag is always `No` and `Material Change` is fixed to `No`. It is shown through the full policy link on the FR-006 booking and payment screens; the refund ladder numbers come from FR-029 and the legal text must not restate them. The one exception is the booking flow: the patient ticks the Cancellation Policy acknowledgment checkbox on the FR-006 booking and payment screen at every booking (REQ-006-038, field Cancellation Policy Ack). That per-booking acknowledgment is owned and stored by FR-006 with the booking and records which policy version was shown; it is not a legal document acceptance under this module, creates no record in the acceptance ledger, and is not counted in acceptance rates, the Pending set or reminders here. (REQ-027-026, REQ-027-027)

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-01)**: Display current legal documents; prompt for acceptance of new versions where required; store acceptance records per version.
- **Provider Platform (PR-01/PR-06)**: Display current legal documents; prompt provider users to accept new versions; track acceptance records for provider accounts.
- **Admin Platform (A-09)**: Create, edit, preview, stage and publish legal documents; view version history; configure acceptance rules; review acceptance coverage and audit logs.
- **Shared Services (S-XX)**: Versioning, publication state, acceptance tracking, and audit logging available across tenants.

### Multi-Tenant Breakdown

**Patient Platform (P-01)**:

- View latest Terms & Conditions, Privacy Policy, Cancellation Policy, and the general Consent text (REQ-027-017)
- Accept latest versions when prompted, on the shared acceptance prompt screen (REQ-027-058); acceptance recorded with timestamp and version ID; a new patient accepts the Current Terms & Conditions and Privacy Policy at registration (REQ-027-062)

**Provider Platform (PR-01/PR-06)**:

- Every provider team member views and accepts the latest legal content personally, on the same prompt screen (REQ-027-019, REQ-027-058); a new team member accepts the Current Terms & Conditions and Privacy Policy at invitation acceptance (REQ-027-062)

**Admin Platform (A-09)**:

- Draft, edit, preview, and publish legal documents
- Maintain version history and compare versions (diff summary)
- Configure acceptance rules together with the coverage threshold, reminder limit and export limit in the Legal settings panel on Screen 1; the audience per document type is fixed (Terms & Conditions and Privacy Policy: patients and provider team members; general Consent: patients only; Cancellation Policy: nobody) and the acceptance rules can only switch the acceptance requirement of a type off for an audience (REQ-027-021, REQ-027-059)
- Monitor acceptance coverage and outstanding users

**Shared Services (S-XX)**:

- Version registry for legal documents: version label, status, effective date, Material Change and change summary belong to the version; each locale text is a child of it (REQ-027-061)
- Acceptance ledger per user, per document type and version
- Audit trail for all create, edit, publish, schedule, activate, archive, withdraw and settings-change actions, viewable as a read-only list on Screen 1 (REQ-027-013)
- Daily job that sends reminders and checks coverage (REQ-027-063)

### Communication Structure

**In Scope**:

- In‑app prompts to accept new versions
- Admin notifications: to the publishing Admin when publication succeeds, and to Admins holding A-09 Edit Settings when the Acceptance Rate of a Current version is below the Admin-set threshold, from 14 days after the version became Current and once per version (REQ-027-022, REQ-027-023, REQ-027-063)
- User reminders to accept pending legal content: to each user in the Pending set (REQ-027-053), at most one every 7 days per user, up to the reminder limit, sent by the daily job (REQ-027-063)
- These three notices are catalogue events of FR-030 (`legal.version_published`, `legal.coverage_below_threshold` and `legal.acceptance_reminder`, FR-030 REQ-030-239 to REQ-030-241); recipients, timing and cadence stay as stated in this module (REQ-027-022, REQ-027-023, REQ-027-063)

**Out of Scope**:

- Real‑time chat or legal counsel workflows (REQ-027-025)
- External e‑signature platforms (future consideration) (REQ-027-025)
- Admin Terms of Service acceptance at account creation, owned by FR-031 (REQ-027-025)

### Entry Points

- Admin: Settings → Legal Content → Documents (T&C, Privacy, Consent, Cancellation Policy) → Draft/Preview/Publish (REQ-027-016)
- Patient: First‑run (at registration) or on change → Acceptance prompt; Settings → Terms & Conditions; Settings → Privacy & Security → Privacy Policy; Settings → Consent (REQ-027-016, REQ-027-062)
- Provider: First‑run (at invitation acceptance) or on change → Acceptance prompt; Settings → Legal → View documents (REQ-027-016, REQ-027-062)

---

## Business Workflows

### Main Flow: Admin Publishes New Legal Version

**Actors**: Admin, System  
**Trigger**: Admin finalizes draft and selects Publish  
**Outcome**: New version becomes current (or Scheduled); acceptance rules apply once it is Current; audit entries recorded

**Steps**:

1. Admin drafts or edits legal content (select document type and locale)
2. Admin previews content and reviews change summary
3. Admin reviews the effective date and Material Change set in the draft and confirms publication (REQ-027-011, REQ-027-050)
4. System publishes the new version at the Publish click; it is Current at once, or Scheduled when the effective date is in the future (the previous version stays Current until then), and the previous version is then archived (REQ-027-030)
5. System records the audit entries (who/when/what changed, actions in REQ-027-013) and notifies the publishing Admin (REQ-027-007, REQ-027-013, REQ-027-022)
6. When the version is Current, System triggers user acceptance prompts if Material Change = Yes and Requires Acceptance = Yes, within the configured scope (REQ-027-004, REQ-027-030)

### Main Flow: User Accepts New Version

**Actors**: Patient/Provider user, System  
**Trigger**: User signs in after a new required version is Current, or registers or accepts an invitation for the first time  
**Outcome**: Acceptance captured; user proceeds to core functions

**Steps**:

1. At first run, System asks a new patient at registration, or a new provider team member at invitation acceptance, to accept the Current Terms & Conditions and Privacy Policy; a patient is asked for the general consent at first sign-in, a provider team member is not (REQ-027-062, REQ-027-021)
2. Daily, System sends a reminder to each user in the Pending set (at most one every 7 days, up to the reminder limit) and, from 14 days after a version became Current, checks its Acceptance Rate and raises the Admin alert once per version while the rate is below the threshold (REQ-027-053, REQ-027-063)
3. User is shown the current legal documents requiring acceptance, on the acceptance prompt screen shared by the patient app and the provider portal, where a user who does not accept can continue with limited access (REQ-027-058, REQ-027-033, Screen 5)
4. User reviews content and accepts; each provider team member accepts personally (REQ-027-012, REQ-027-019)
5. System records acceptance (user, document type, version, timestamp, locale, channel)
6. System resumes normal access without further prompts until next required version (REQ-027-035)

### Alternative Flows

**A1: Scheduled Effective Date**:

- Trigger: Admin sets a future effective date
- Steps:
  1. System marks the new version Scheduled; the previous version stays Current until the effective date (REQ-027-030)
  2. On effective date, new version becomes current and the previous version is archived; audit entries recorded (activate, archive); prompts begin when Material Change = Yes and Requires Acceptance = Yes
  3. Until then a Scheduled version is view-only; there is at most one per document type, and Admin may withdraw it back to Draft, audited (REQ-027-060)
- Outcome: Controlled rollout with clear timing

**B1: Restoring an Earlier Version**:

- Trigger: Admin needs to go back to the text of an earlier version due to error
- Steps:
  1. There is no revert button; Admin opens Screen 1 and creates a new draft from the old version on a Current or Archived row (REQ-027-031, REQ-027-049)
  2. Admin publishes the restored text as a new version through the normal publishing flow (same edit, preview and publish steps) with Material Change fixed to Yes and not editable on Screen 2 (No for the Cancellation Policy)
  3. The audit entries of the normal publish are recorded (REQ-027-013); prompts follow the normal flow
- Outcome: Rapid recovery with traceability; every base member with no ledger row for the restored version or for the version it was restored from is asked to accept it (REQ-027-032, REQ-027-053)

---

## Screen Specifications

### Screen 1: Admin — Legal Documents List

**Purpose**: List all legal document types and versions, and provide entry points to draft, edit, preview, and publish.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Document Type | select | Yes | T&C, Privacy, Consent, Cancellation Policy | Must be one of supported types | ENT-legal-document.document_type |
| Locale | select | Yes | Display locale for translation; global content only | Must be supported locale (REQ-027-046) | ENT-legal-document.locale |
| Version | text | Yes | Version identifier | Must be unique per document type; all locale texts of a version share it (REQ-027-040, REQ-027-061) | ENT-legal-document.version |
| Status | badge | Yes | Draft / Scheduled / Current / Archived | See REQ-027-029, REQ-027-030 and REQ-027-060. | ENT-legal-document.status |
| Effective Date | date/time | Yes | Scheduled go-live date and time, stored in UTC and shown in the Admin's time zone | Cannot be in the past at save; checked again at Publish (REQ-027-041) | ENT-legal-document.effective_date |
| Requires Acceptance | boolean | Yes | Indicates if material change gating applies | Tied to Material flag from draft; always No for the Cancellation Policy (REQ-027-027) | ENT-legal-document.requires_acceptance |
| Last Updated By/At | text | Yes | Audit info | Read-only | ENT-legal-document.last_updated_by, ENT-legal-document.last_updated_at |
| Actions | buttons | Yes | Draft new version, Edit draft, Create draft from this version (Current and Archived rows), View history (filters the list to the document type), Preview, Publish (if draft ready), Withdraw (Scheduled row), Add locale text (Current row, for a missing locale only) | See REQ-027-031, REQ-027-037, REQ-027-049, REQ-027-050 and REQ-027-060. | no graph field (control) |
| Legal settings | panel | Yes | Acceptance rules, coverage threshold (percent), reminder limit (reminders per user per version), export limit (exports per Admin per day) | Each change is audited; behaviour while unset in REQ-027-059 | SET-legal-acceptance-rules, SET-legal-coverage-threshold, SET-legal-reminder-limit, SET-legal-export-limit |
| Audit trail | list | Yes | Read-only list of audit entries (action, actor, time, summary), filtered to one document or unfiltered | Opened filtered from a document row or the Screen 4 audit link, and unfiltered from the Legal settings panel, where the settings_change entries are seen (REQ-027-013) | ENT-legal-audit-entry.action, ENT-legal-audit-entry.actor_id, ENT-legal-audit-entry.occurred_at, ENT-legal-audit-entry.summary |
| Locale gap badge | badge | No | Shown on a version row when a user was served the fallback text | Set when the fallback is served; cleared when Admin adds that locale's text to the Current version (REQ-027-037) | no graph field (control) |

**Business Rules**:

- See REQ-027-011.
- Admin edits the four legal settings in the Legal settings panel; while a value is unset there is no banner or alert, no reminders and CSV export is blocked, and a Material Change = Yes version gates the fixed audience of its document type. The acceptance rules can only switch the acceptance requirement of a type off for an audience; they cannot widen the audience or change the gated actions. (REQ-027-021, REQ-027-059)
- A Scheduled version is view-only; at most one Scheduled version per document type; Admin may withdraw it back to Draft, audited. (REQ-027-060)
- Only one Current version per document type at a time; when a newly published version becomes Current, the prior Current is auto-archived. (REQ-027-029)
- Publish action is global (no region targeting); locale is for translation display only. (REQ-027-003)
- Edit action opens the Draft/Edit screen for Draft versions; Scheduled, Current and Archived versions are view-only (preview/history), except that Admin may add a missing locale text to a Current version: it is audited as edit, makes no new version and needs no re-acceptance, and existing locale texts stay view-only. (REQ-027-049, REQ-027-037)

**Notes**:

- Provide filters by Document Type, Status, and Locale.
- Show a warning banner when the Acceptance Rate of the Current version is below the Admin-set threshold, from 14 days after the version became Current (the same start as the Admin alert); unset means no banner. (REQ-027-024, REQ-027-059, REQ-027-063)

---

### Screen 2: Admin — Draft/Edit Legal Document

**Purpose**: Author or edit content for a legal document version prior to publication.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Document Type | select | Yes | T&C, Privacy, Consent, Cancellation Policy | Locked after version creation (REQ-027-044) | ENT-legal-document.document_type |
| Locale | select | Yes | Translation locale for the current version's content. Multiple locales can exist for a single version; each locale text is a child of the version. | See REQ-027-046 and REQ-027-061. | ENT-legal-document.locale |
| Content | rich text editor with Markdown toggle | Yes | Full legal text | Min 200 chars; max 50k chars (REQ-027-042) | ENT-legal-document.content |
| Change Summary | textarea | Yes | Human-readable summary of changes | Max 500 chars (REQ-027-043) | ENT-legal-document.change_summary |
| Material Change | boolean | Yes | Marks if re-acceptance required | Required to set acceptance gating (REQ-027-045); fixed to No and not editable for the Cancellation Policy (REQ-027-026); fixed to Yes and not editable for a draft created from an earlier version (REQ-027-031) | ENT-legal-document.material_change |
| Effective Date | date/time | Yes | When this version becomes current, in UTC and shown in the Admin's time zone | See REQ-027-041. | ENT-legal-document.effective_date |
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
| Version Diff Summary | read-only | Yes | Key changes vs. prior version | Must be generated from draft; for the first version of a document type it reads "Initial version" and does not block Publish (REQ-027-050) | ENT-legal-document.version_diff_summary |
| Effective Date | read-only | Yes | Activation time, shown in the Admin's time zone | Must be set in draft; re-checked at Publish, and a time already past makes the version Current immediately (REQ-027-041, REQ-027-050) | ENT-legal-document.effective_date |
| Material Change | read-only | Yes | Indicates acceptance requirement | Must match draft flag (REQ-027-050) | ENT-legal-document.material_change |
| Publish Button | button | Yes | Executes publish | Disabled until all validations pass; the validation is repeated at Publish (REQ-027-050) | no graph field (control) |

**Business Rules**:

- See REQ-027-029 and REQ-027-030.
- Admin confirms publication explicitly; the Publish click publishes the version and logs the audit entries on both branches, Current at once or Scheduled for a future effective date. (REQ-027-007, REQ-027-011, REQ-027-030)
- Acceptance prompts start only when the version is Current and Material Change=true and Requires Acceptance=true. (REQ-027-004, REQ-027-030)
- See REQ-027-003.
- When a version is published globally, the system validates that at least the English (en-US) locale content is complete. If other locales are configured for this version, the Admin UI will provide a summary of their completeness, but publishing will proceed using the platform default language (English, en-US) version as the single fallback if a specific locale is missing or incomplete (as per CL-3). The legal fallback is fixed to English (en-US) and does not follow the FR-021 fallback order. (REQ-027-036)

**Notes**:

- Show acceptance impact summary (number of users who would be Pending if the version became Current now; REQ-027-052, REQ-027-053; ENT-legal-document.reaccept_user_count).
- Provide link back to edit draft if issues are found. A second Publish for a document type that already has a Scheduled version is rejected here and the Admin stays on this screen. (REQ-027-060)

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
| Acceptance Rate | metric | Yes | % accepted out of the version's acceptance base: the Active patient accounts and team members of Active providers, in the document type's audience (REQ-027-021), that existed when the version became Current; accepted means a ledger row for this version or, for a restored version, for the version it was restored from | Computed from the acceptance ledger; an account that leaves Active leaves the base; not applicable for the Cancellation Policy and for Material Change = No versions (REQ-027-053) | ENT-legal-document.acceptance_rate |
| Pending Users | list/count | Yes | The rest of the acceptance base, without an accepted ledger row as above; prompts, reminders and the Screen 3 re-accept count use this same set (REQ-027-053) | Supports pagination/export; not applicable where the rate is not applicable | ENT-legal-document.pending_user_count |
| Reminders Sent | count | Yes | Reminder notifications issued: the count of the version's legal reminder records (REQ-027-063) | Read-only | ENT-legal-document.reminders_sent_count |

**Business Rules**:

- Data is read-only; reminders respect the Admin-set reminder limit. (REQ-027-054, REQ-027-014)
- Filters by document type and version; supports date range for trend.

**Notes**:

- Export pending list (CSV) for follow-up; blocked while the export limit is unset. (REQ-027-055, REQ-027-059)
- Show audit link for the publication event; it opens the Audit trail list on Screen 1 filtered to the document. (REQ-027-013)

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

### Screen 5: Patient and Provider — Acceptance Prompt

**Purpose**: One prompt screen shared by the patient app and the provider portal where a user reviews and accepts the legal documents that need acceptance (REQ-027-058). Graph screen SCR-027-06.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
|------------|------|----------|-------------|------------------|-------------|
| Document Type | text | Yes | Each document that needs acceptance | Read-only | ENT-legal-document.document_type |
| Version | text | Yes | Version to accept | Read-only | ENT-legal-document.version |
| Effective Date | text | Yes | When the version applies | Read-only | ENT-legal-document.effective_date |
| Full Text | read-only | Yes | Full legal text in the user's language, or English with a discreet notice when the fallback applies (REQ-027-036) | Opened before Accept is enabled | ENT-legal-document.content |
| Language | text | Yes | Locale of the text shown | Read-only | ENT-legal-document.locale |
| Accept | buttons | Yes | One Accept per document | Enabled only after the full text has been opened | no graph field (control) |
| Continue with limited access | button | No | Lets the user carry on without accepting; sign-out and the FR-001 account-deletion link are offered beside it (REQ-027-033) | Shown at sign-in only, not at a gated action | no graph field (control) |

**Business Rules**:

- The blocked state applies only at the gated actions of REQ-027-033, where this screen is shown again and stays blocked until every listed document is accepted; an accepted state follows acceptance. At sign-in the user may instead continue with limited access, sign out or use the FR-001 account-deletion link. (REQ-027-058, REQ-027-033)
- Each provider team member accepts personally. (REQ-027-019)
- Acceptance is recorded once per version per user. (REQ-027-035)

**Notes**:

- Shown at first run (registration for a patient, invitation acceptance for a provider team member) and at sign-in after a required version becomes Current. (REQ-027-062)

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
2. Given acceptance is recorded, When the user resumes activity, Then no further prompts are shown until the next version; FR-003 asks again at an inquiry only when the Current Terms & Conditions are not accepted (REQ-027-035)

### User Story 3 — View Acceptance Coverage (Priority: P2)

As an Admin, I can view acceptance coverage (who has accepted which version) and follow up with users who have not yet accepted.

**Independent Test**: Publish a new version; verify coverage dashboard shows accepted/pending counts and lists of users pending.

**Acceptance Scenarios**:

1. Given a recent publication, When Admin views coverage, Then accepted and pending users are listed with timestamps/version info

### Edge Cases

- Minor updates vs. material changes: non‑material edits may not require re‑acceptance; material changes do — rules configurable (REQ-027-004)
- Existing users with pending procedures: aftercare, messaging, scheduled installments and viewing stay available until acceptance; prompts are shown at sign-in and at the blocked actions (REQ-027-033, REQ-027-034)
- Locale mismatch: fall back to English (en-US) if a localized version is not available; Screen 1 shows a Locale gap badge on the version row until Admin adds that locale's text to the Current version (REQ-027-036, REQ-027-037)
- Restoring an earlier text after partial acceptance: the restored text is published as a new version with Material Change fixed to Yes; existing acceptance records are preserved; every base member with no ledger row for the restored version or for the version it was restored from is asked to accept it (REQ-027-031, REQ-027-032, REQ-027-053)
- Accounts outside the acceptance base (dormant, deletion-requested, deleted, suspended, offboarded) are not counted and are prompted at their next sign-in if they return; accounts created after the version became Current accept at first run and are not in the base (REQ-027-053, REQ-027-062)
- A minor version does not cancel a material requirement: a user must accept the Current text of a type while the latest Material Change = Yes version up to and including it is not accepted by them; first run asks for the Current text whatever its flag; such a user is still prompted and reminded when the Current version's rate is not applicable (REQ-027-035, REQ-027-053)
- Effective date already past at Publish: the version becomes Current immediately (REQ-027-041)
- A second Publish for a document type that already has a Scheduled version is rejected until that version is withdrawn or live (REQ-027-060)

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

- **REQ-027-008**: Legal document entities MUST include: type, locale (for translation only, no regional content variants), version, status (draft/scheduled/current/archived), effective date, change summary; version-level attributes and locale texts follow REQ-027-061
- **REQ-027-009**: Acceptance records MUST include: user, document type, version, timestamp, locale, and acceptance channel
- **REQ-027-010**: Version comparisons MUST present human‑readable change summaries (no raw diffs required for end‑users)

### Security & Privacy Requirements

- **REQ-027-011**: Only authorized Admin roles can use the FR-027 Admin screens and exports: A-09 Edit Settings to create, edit, publish, withdraw and change the legal settings and to export CSV; A-09 View Settings to view the lists, acceptance status and audit trail; publication actions require explicit confirmation
- **REQ-027-012**: Users MUST have clear access to read the full content prior to acceptance; acceptance records, legal audit entries and reminders are retained to demonstrate consent under the FR-023 retention rules (10-year floor, anonymised in place at approved deletion; anonymised rows are not counted in coverage)
- **REQ-027-013**: Audit trail MUST be immutable and reviewable by authorized Admins as a read-only Audit trail list on Screen 1. The list is filtered to one document from a document row or the Screen 4 audit link, and also opens unfiltered from the Legal settings panel; the object reference is empty for settings_change. Audit actions: create on the first save of a draft; edit when the Admin leaves the editor with changes (not per autosave) and when a locale text is added to a Current version; Publish now writes publish, activate and archive (of the prior Current); Publish with a future effective date writes publish and schedule, and the effective date then writes activate and archive; withdraw writes withdraw; a settings change writes settings_change

### Integration/Communication Requirements

- **REQ-027-014**: Users SHOULD receive clear prompts and reminders for pending acceptance respecting rate limits (reminder cadence and limit in REQ-027-063)
- **REQ-027-015**: Legal content visibility and acceptance prompts MUST be available across Patient and Provider applications, on the shared prompt screen of REQ-027-058

### Clarifications (Resolved)

- CL‑1: Enforcement for existing users — Until acceptance a patient cannot submit an inquiry, accept a quote or start a payment, and a provider cannot accept an inquiry or submit a quote; everything else stays available (aftercare, messaging, scheduled installments, viewing). A user who does not accept stays limited and may sign out or use the FR-001 account-deletion route. Show rate‑limited reminders. Gating occurs at sign‑in and at those actions. (REQ-027-033, REQ-027-034)
- CL‑2: Material vs. minor changes — Material includes changes to obligations, data use/sharing, user rights, or liability; Minor includes formatting, typo fixes, or clarifications without policy change. Only material changes require re‑acceptance; Admin marks the publish accordingly. (REQ-027-028)
- CL‑3: Locale handling — If a localized version is unavailable, fall back to the platform default language (English) and display a discreet notice. Log a task to add the missing locale. Acceptance using the fallback is considered valid. (REQ-027-036, REQ-027-037, REQ-027-038)
- CL‑4: Regional customization — Legal content is uniform globally; no location‑based variants or region‑specific publication paths are required. (REQ-027-003)
- CL‑5: Admin-set limits — The acceptance coverage warning threshold, the reminder limit and the export limit are set by Admin in the Legal settings panel; none has a default value, and the behaviour while a value is unset is in REQ-027-059. FR-027 owns the acceptance rules setting (it can only switch the acceptance requirement of a document type off for an audience, REQ-027-021) and the acceptance coverage threshold setting.

---

## Dependencies

Related FRs: FR-006 (booking and payment screens that link to the full Cancellation Policy), FR-009 (provider team and role management), FR-001 (account creation and the account-deletion route), FR-023 (retention of acceptance records), FR-029 (refund ladder numbers; the legal text does not restate them). Platform areas: P-01 Auth & Profile (gating and acceptance at sign-in and profile areas); PR-01/PR-06 Provider Auth/Settings (provider user acceptance and settings visibility); A-09 System Settings (legal content management and publication).

---

## Appendix: Change Log

| Date       | Version | Changes                | Author       |
|------------|---------|------------------------|--------------|
| 2026-11-22 | 1.5 | Requirements graph programme baseline: PRD compressed to the checklist structure (each rule stated once, field rows tagged with graph field ids, dropped classes removed). No rule changes. Earlier history (v1.0 to v1.4) is in `archived/prd-baseline-2026-11-08/fr027-legal-content-management/` and in git history. The PRD names no change request. | Product Owner / Documentation |
| 2026-11-24 | 1.6 | Logic review pass 1 (30 findings): Legal settings panel with unset behaviour (REQ-027-059); shared acceptance prompt Screen 5 (REQ-027-058); publish and audit at the Publish click on both branches and prompts only when Current; Scheduled status view-only and withdrawable (REQ-027-060); one version model (REQ-027-061); first-run acceptance (REQ-027-062); daily reminder and coverage job (REQ-027-063); restore reuses the main publish steps and is always material; acceptance base, once-per-version acceptance, per-member provider acceptance, gated actions, Cancellation Policy shown through the FR-006 link; audit actions replaced; effective date in UTC with a re-check at Publish; fallback fixed to English. Owner defaults 77 to 86. | Product Owner / Documentation |
| 2026-11-24 | 1.7 | Logic review pass 2 (16 findings, FR-027 side 15, FR-022 queued): one acceptance base and Pending set for prompts, reminders, re-accept count and rate, with a fixed audience per document type (REQ-027-053, REQ-027-021, REQ-027-032, REQ-027-035, REQ-027-062); banner and alert both start 14 days after Current; Screen 5 limited-access exit; Admin may add a missing locale text to a Current version; audit actions per event (REQ-027-013); Audit trail also opens unfiltered; settings, withdraw and rejected second Publish as flow steps; provider first-run and sign-in prompts; alert and notice recipients; Consent entry in patient Settings; restore draft Material Change fixed on Screen 2. Owner defaults 87 and 88. | Product Owner / Documentation |
| 2026-11-25 | 1.8 | Cross-FR alignment: legal notices are catalogue events owned by FR-030 (REQ-030-239 to REQ-030-241); the REQ-006-038 acknowledgment at booking is separate from legal acceptance (REQ-027-026). | Product Owner / Documentation |
| 2026-11-25 | 1.9 | Owner ruling: the Cancellation Policy has no per-version acceptance record here, but the patient acknowledges it with a checkbox at every booking; that per-booking acknowledgment is owned and stored by FR-006 with the booking (REQ-006-038), records the policy version shown, and is not counted in acceptance rates, the Pending set or reminders (REQ-027-026). | Product Owner / Documentation |

---

## Appendix: Approvals

Approved by the Product Owner as part of the requirements baseline of 2026-11-25. Record: `project-requirements/baseline-sign-off.md`. Changes after that date are listed in the Change Log above.

---

**Template Version**: 2.0.0 (Constitution-Compliant)  
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)  
**Based on**: FR-027 Legal Content Management  
**Last Updated**: 2026-11-25
