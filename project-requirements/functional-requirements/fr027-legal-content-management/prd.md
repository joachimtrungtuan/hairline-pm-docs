# Product Requirements Document: Legal Content Management

**Module**: A-09: System Settings & Configuration  
**Feature Branch**: `fr027-legal-content-management`  
**Created**: 2025-11-12  
**Status**: Draft  
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

**A2: Locale‑Specific Publication**:

- Trigger: Admin publishes only for selected locales or regions
- Steps:
  1. System targets prompts and acceptance rules by locale/region
  2. Prior version remains current elsewhere
- Outcome: Regionalized compliance

**B1: Publication Reversion**:

- Trigger: Admin needs to revert to previous version due to error
- Steps:
  1. System marks previous version current again
  2. Prompts update accordingly; audit entry recorded
- Outcome: Rapid recovery with traceability

---

## User Scenarios & Testing

### User Story 1 — Publish Legal Document (Priority: P1)

As an Admin, I can draft, preview, and publish a new version of a legal document with an effective date so that the correct terms are shown to users and acceptance is tracked.

**Independent Test**: Publish a new version in staging; verify version status changes to current on effective date and audit entry exists.

**Acceptance Scenarios**:

1. Given a draft version, When Admin publishes with an effective date, Then the system sets it as current at the scheduled time and archives the prior version
2. Given a published version, When Admin reviews audit logs, Then the change is recorded with who/when/what changed
3. Given locale‑specific publication, When Admin targets a region, Then only users in targeted locales are prompted

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

- FR-027.1: Admins MUST be able to create, edit, preview, and publish legal documents (T&C, Privacy, Consent)
- FR-027.2: System MUST maintain version history with timestamps and change tracking; previous versions are preserved for reference
- FR-027.3: Admins MUST be able to schedule an effective date and target locales/regions for publication
- FR-027.4: System MUST require acceptance for material changes as configured, prompting users appropriately
- FR-027.5: System MUST track which user accepted which document type and version, with timestamp and locale displayed
- FR-027.6: System MUST provide a coverage view for Admin to see acceptance status and follow‑up needs
- FR-027.7: All legal content changes MUST be logged with who/when/what changed (audit trail)

### Data Requirements

- FR-027.D1: Legal document entities MUST include: type, locale, version, status (draft/current/archived), effective date, change summary
- FR-027.D2: Acceptance records MUST include: user, document type, version, timestamp, locale, and acceptance channel
- FR-027.D3: Version comparisons MUST present human‑readable change summaries (no raw diffs required for end‑users)

### Security & Privacy Requirements

- FR-027.S1: Only authorized Admin roles can create/edit/publish legal documents; publication actions require explicit confirmation
- FR-027.S2: Users MUST have clear access to read the full content prior to acceptance; records are retained to demonstrate consent
- FR-027.S3: Audit trail MUST be immutable and reviewable by authorized Admins

### Integration/Communication Requirements

- FR-027.I1: Users SHOULD receive clear prompts and reminders for pending acceptance respecting rate limits
- FR-027.I2: Legal content visibility and acceptance prompts MUST be available across Patient and Provider applications

### Clarifications (Resolved)

- CL‑1: Enforcement for existing users — Block core actions until acceptance; allow read‑only access where safe. Show rate‑limited reminders. Gating occurs at sign‑in and before core transactional flows.
- CL‑2: Material vs. minor changes — Material includes changes to obligations, data use/sharing, user rights, or liability; Minor includes formatting, typo fixes, or clarifications without policy change. Only material changes require re‑acceptance; Admin marks the publish accordingly.
- CL‑3: Locale handling — If a localized version is unavailable, default to the primary language and display a discreet notice. Log a task to add the missing locale. Acceptance using the fallback is considered valid.

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
**Based on**: FR-027 Legal Content Management  
**Last Updated**: 2025-11-12
