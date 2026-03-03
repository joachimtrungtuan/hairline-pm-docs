# FR-013 - Reviews & Ratings

**Module**: P-02: Quote Request & Management | A-01: Patient Management & Oversight
**Feature Branch**: `fr013-reviews-ratings`
**Created**: 2025-11-11
**Status**: Draft
**Source**: FR-013 from local-docs/project-requirements/system-prd.md; Transcriptions (patient app, admin platform)

---

## Executive Summary

Enable verified patients to submit post‑procedure reviews with ratings and optional photos, published immediately upon submission (no pre-publication moderation gate). Admin retains the ability to edit or remove published reviews post-publication for policy violations. Display provider ratings (average, count, distribution) and allow providers to respond publicly. This builds trust, informs patient decision‑making, and provides providers and Hairline with structured feedback for quality improvement while maintaining fairness, authenticity, and compliance.

---

## Module Scope

### Multi-Tenant Architecture

- Patient Platform (P-02): Submit a review after confirmed procedure completion (time-gated 3+ months), provide overall and category ratings, write feedback, optionally attach before/after photos; review is published immediately upon submission; patient can edit their published review at any time.
- Provider Platform (PR-06 display context): View public reviews on provider profile, see rating averages and distribution, and post public responses to published reviews.
- Admin Platform (A-01): Monitor published reviews, edit or remove reviews post-publication for policy violations (PII, inappropriate content), manage flagged content, seed authenticated reviews for new providers, and produce reports on review volume and ratings trends.
- Shared Services (S-05, S-03): Media Storage for review photos; Notification Service for invite reminders, admin removal notifications, and provider reply alerts.

### Multi-Tenant Breakdown

Patient Platform (P-02):

- Receive invitation to review after procedure completion threshold.
- Submit ratings (overall 1–5 stars; category ratings) and feedback; optionally attach photos; review published immediately.
- Edit own published review at any time; view review status (Published / Removed by Admin).

Provider Platform (display + response):

- View published reviews on their profile with averages and distribution.
- Post a public response to individual reviews; receive notification on new published reviews.

Admin Platform (A-01):

- Review management dashboard with filters (date, provider, rating, status, flagged).
- Edit or remove published reviews for policy violations (with reason); redact sensitive data post-publication.
- Seed authenticated reviews for new providers (flagged as "Verified Off-platform").
- Manage review categories and invite cadence; export reports.

Shared Services (S-05, S-03):

- S-05 handles secure photo storage and retrieval.
- S-03 delivers invite/reminder emails/push and status notifications.

### Entry Points

- Time-gated invite after confirmed procedure completion (≥ 3 months) triggers review flow.
- Patient navigates to “Write a Review” from provider history.
- Providers access “Reviews” in dashboard to read and respond once published.
- Admins access “Review Management” from Admin platform navigation.

---

### Backlog (Future Enhancements)

- Admin-seeded authenticated reviews import for new providers (clearly flagged as “Verified Off‑platform” with verification source and date) — moved to main scope per client transcription (AdminPlatform-Part1, lines 91–100).

---

## Business Workflows

### Main Flow: Patient Submits a Review

Actors: Patient, System
Trigger: Patient opens “Write a Review” from invite or history
Outcome: Review published immediately with ratings, feedback, and optional photos; provider rating metrics updated

Steps:

1. Patient completes overall and category ratings, enters feedback, and optionally attaches photos.
2. System validates inputs (rating ranges, feedback length, file type/size) and verifies eligibility.
3. System publishes the review immediately and updates provider’s rating metrics.
4. Patient sees confirmation; review is live on the provider’s profile. Patient may edit the review at any time.

### A1: Admin Removes a Published Review (Post-Publication)

- Trigger: Admin identifies a policy violation in a published review (PII, inappropriate content, flagged by users/keyword detection).
- Steps:
  1. Admin reviews the published content and determines violation.
  2. Admin removes the review with a reason; system unpublishes and archives the review (retained per 7-year data policy).
  3. System notifies patient with removal reason.
- Outcome: Review removed from public view; patient sees “Removed by Admin” status with reason; provider rating metrics recalculated.

### A2: Admin Edits a Published Review (Post-Publication)

- Trigger: Admin identifies content requiring redaction (PII, sensitive data) but the review itself is otherwise valid.
- Steps:
  1. Admin redacts specific content (PII, inappropriate phrases) from the published review.
  2. System updates the published review with redacted content; audit trail records what was changed, by whom, and when.
- Outcome: Review remains published with redacted content; audit log preserved.

### B1: Provider Response

- Trigger: Provider posts a response to a published review.
- Steps:
  1. Provider writes response; System validates length and policy.
  2. System publishes response under provider identity.
- Outcome: Response visible with the review; patient notified.

### B2: Flagging/Inappropriate Content

- Trigger: Content flagged by users or keyword detection.
- Steps: System queues flagged content for admin review; Admin may redact, unpublish, or uphold.
- Outcome: Policy-compliant content remains; violations are removed with audit record.

---

## Screen Specifications

### Screen 1: Patient – Submit Review

Purpose: Allow eligible patients to submit a structured review post-procedure.

Data Fields:

| Field Name         | Type        | Required | Description                                  | Validation Rules                         |
|--------------------|-------------|----------|----------------------------------------------|------------------------------------------|
| Overall rating     | 1–5 stars   | Yes      | Overall experience                            | Integer 1–5                              |
| Category: Facility | 1–5 stars   | Yes      | Facility cleanliness                          | Integer 1–5                              |
| Category: Staff    | 1–5 stars   | Yes      | Staff professionalism                         | Integer 1–5                              |
| Category: Results  | 1–5 stars   | Yes      | Results satisfaction                          | Integer 1–5                              |
| Category: Value    | 1–5 stars   | Yes      | Value for money                               | Integer 1–5                              |
| Written feedback   | textarea    | Yes      | Narrative experience                          | 100–2000 chars                           |
| Photos             | images      | No       | Optional before/after images                  | Up to 5 files; jpg/png; max 10MB each    |

Business Rules:

- Eligibility enforced (completed procedure and ≥ 3 months).
- One review per completed procedure; patient can edit their published review at any time.
- Review is published immediately upon submission — no pre-publication moderation gate.
- Clear photo guidelines; sensitive/identifying content discouraged.

Notes:

- Show progress and save-draft; disclose display policies and admin's right to remove for violations.

---

### Screen 2: Admin – Review Management

Purpose: Monitor published reviews, edit or remove for policy violations, manage flags, and seed authenticated reviews for new providers.

Data Fields:

| Field Name    | Type   | Required | Description                                | Validation Rules       |
|---------------|--------|----------|--------------------------------------------|------------------------|
| Filters       | UI     | No       | Status (Published / Removed / Flagged), provider, date, rating | N/A                    |
| Review item   | Card   | Yes      | Ratings, feedback, photos, patient alias   | N/A                    |
| Actions       | Buttons| Yes      | Edit (redact), Remove (with reason)        | Reason min 10 chars    |
| Redaction     | Tools  | No       | Remove PII/violations from published review | Track changes in audit |
| Add Review    | Button | No       | Seed authenticated review for a provider (flagged as "Verified Off-platform") | Requires verification source and date |

Business Rules:

- Every admin action (edit, remove, seed) records admin identity, timestamp, and reason in audit trail.
- Redactions are tracked and visible in audit history.
- Removal is unpublish + archival (not permanent deletion) per 7-year data retention policy.
- Admin-seeded reviews must be flagged as "Verified Off-platform" with verification source and date (per client transcription: AdminPlatform-Part1, lines 91–100).

Notes:

- Bulk actions for clear-cut spam; export review management report.

---

### Screen 3: Provider – Reviews & Response

Purpose: Let providers see feedback and reply publicly.

Data Fields:

| Field Name         | Type   | Required | Description                          | Validation Rules       |
|--------------------|--------|----------|--------------------------------------|------------------------|
| Ratings summary    | Stats  | Yes      | Average rating, count, distribution  | N/A                    |
| Reviews list       | List   | Yes      | Published reviews                    | Sorted by recency      |
| Provider response  | Text   | No       | Public provider reply                | 50–1000 chars          |

Business Rules:

- Provider responses are public and immutable once posted (admin can remove on violation).

Notes:

- Encourage professional tone; display response timestamp and provider role.

---

## Business Rules

### General Module Rules

- Eligibility check required: only patients with a completed procedure may review.
- Time gating: review invitation and entry allowed ≥ 3 months post-procedure.
- One review per completed procedure; patient can edit their published review at any time (updated content published immediately).
- Ratings use 1–5 scale with half‑stars display allowed for averages.

### Data & Privacy Rules

- Patient display name uses aliasing (e.g., first name + initial) by default.
- Photos and text must not expose sensitive personal information; admin may redact or remove post-publication.
- Reviews retained for minimum 7 years; takedown requests handled by unpublish + archival with restricted access.
- All admin actions (edits, removals, seeded reviews) are fully auditable (who, when, what, reason).

### Admin Editability Rules

Editable by Admin:

- Review categories/labels; invitation cadence and reminders.
- Photo guidelines text; removal reasons catalogue.
- Visibility rules for display name (alias/full name toggle policy).

Fixed in Codebase (Not Editable):

- Eligibility logic requires completed procedure and time threshold.
- Minimum and maximum lengths for text fields and rating scale bounds.

Configurable with Restrictions:

- Flagging thresholds and auto-flag rules for admin review (within safe bounds approved by policy).

Admin-Seeded Review Policy:

- Admin-imported authenticated reviews must be flagged as "Verified Off‑platform" with verification source and date. These are published directly by admin (no patient submission flow).

---

## Success Criteria

### Patient Experience Metrics

- SC-001: 90% of eligible patients can complete a review in ≤ 3 minutes.
- SC-002: ≥ 30% invite‑to‑review conversion within 14 days of invite.
- SC-003: 95% of photo uploads validate on first attempt (guidelines clear).

### Provider Efficiency Metrics

- SC-004: 80% of published reviews receive a provider response within 5 business days.
- SC-005: Providers can locate any review and respond in ≤ 60 seconds.

### Admin Management Metrics

- SC-006: 95% of flagged reviews receive an admin review decision within 48 hours.
- SC-007: 100% of admin actions (edits, removals) capture admin identity, timestamp, and reason in audit log.

### System Performance Metrics

- SC-008: Ratings summary loads in ≤ 1 second for 95th percentile.
- SC-009: Zero data loss of submitted reviews; photos stored reliably with secure access.
- SC-010: 99.9% monthly uptime for review submission and viewing.

### Business Impact Metrics

- SC-011: Provider profile conversion rate improves by ≥ 10% after launch.
- SC-012: Average content volume reaches ≥ 3 new reviews per active provider/month by month 3.

---

## Dependencies

### Internal Dependencies (Other FRs/Modules)

- P-01: Auth & Profile Management – identity and role context.
- P-03: Booking & Payment – confirm procedure completion and dates for eligibility/time gating.
- S-05: Media Storage Service – secure handling of review photos.
- S-03: Notification Service – invitations, reminders, admin removal notifications, and provider response alerts.

### External Dependencies (APIs, Services)

- Email/push delivery providers for notifications (through S-03).

### Data Dependencies

- Completed procedure records with completion date and provider association.
- Provider profile identifiers for correct attribution and display.

---

## Assumptions

### User Behavior Assumptions

- Patients are willing to leave reviews when prompted and informed of display policies.
- Providers will respond to reviews to improve public trust.

### Technology Assumptions

- Modern mobile and web clients used; stable connectivity for uploads.
- Secure media storage available; common image formats supported.

### Business Process Assumptions

- Admin team monitors flagged reviews and review management dashboard during business hours.
- Legal/compliance guidance exists for defamation and takedown handling.

---

## Implementation Notes

### Technical Considerations

- Architecture: Reviews published immediately on write; admin audit logs for post-publication edits and removals.
- Media handling: Validate size/type, generate thumbnails; protect access.
- Anti‑abuse: Duplicate detection, keyword flags, rate limits for submissions and responses.

### Integration Points

- Patient app → Review service: submit (published immediately), edit, request takedown, status.
- Admin dashboard → Review service: review management, edit/remove, seed reviews, audits.
- Provider dashboard → Review service: fetch published reviews, post responses.

### Scalability Considerations

- Caching of ratings summary and distribution per provider.
- Paging and lazy load for reviews lists; background processing for photo thumbnails.

### Security Considerations

- Enforce RBAC for submit/moderate/respond actions.
- Encrypt data in transit and at rest; signed URLs for media.
- Full audit trail for all state changes; soft‑delete (unpublish) for takedowns.

---

## User Scenarios & Testing

### User Story 1 – Patient submits a review (P1)

Why: Capture authentic post‑procedure experience to inform others.

Independent Test: Eligible test patient submits review with photos; review is published immediately and visible on provider profile.

Acceptance Scenarios:

1. Given an eligible patient, when they submit required ratings and feedback, then the review is published immediately and the patient sees confirmation.
2. Given valid photos, when uploaded, then the system accepts and associates them with the review.
3. Given a published review, when the provider profile loads, then averages and distribution reflect the new review.

### User Story 2 – Admin removes a published review (P1)

Why: Ensure policy compliance post-publication.

Independent Test: Admin removes a published review for policy violation; review is unpublished with audit entry and patient is notified.

Acceptance Scenarios:

1. Given a published review with a policy violation, when an admin removes it with a reason, then the review is unpublished and archived, ratings metrics are recalculated, and the patient sees "Removed by Admin" status with the reason.
2. Given a removal, when the provider profile loads, then averages and distribution no longer include the removed review.

### User Story 3 – Provider responds to a review (P2)

Why: Encourage constructive dialogue and trust.

Independent Test: Provider posts a response; response appears under the review and patient is notified.

Acceptance Scenarios:

1. Given a published review, when a provider posts a response, then it appears publicly under the review.
2. Given a new response, when notifications trigger, then the reviewer receives a notification.

### Edge Cases

- Ineligible attempts (too early/no completed procedure) are blocked with clear messaging.
- Photos exceed limits: user informed, upload prevented until compliant.
- Duplicate or spam reviews: auto‑flag for admin review post-publication.
- Takedown request: review unpublished and archived; provider metrics recalculated.

---

## Functional Requirements Summary

### Core Requirements

- **REQ-013-001**: System MUST allow eligible patients to submit reviews (overall + categories, feedback, optional photos).
- **REQ-013-002**: System MUST enforce time gating (≥ 3 months) and single review per completed procedure.
- **REQ-013-003**: System MUST publish reviews immediately upon patient submission (no pre-publication moderation gate) and provide admin with post-publication edit/remove capabilities with full audit trail.
- **REQ-013-004**: System MUST display published reviews on provider profiles with provider responses; admin-removed reviews are unpublished and archived.
- **REQ-013-005**: System MUST calculate and display provider average rating, count, and distribution.

### Data Requirements

- **REQ-013-006**: System MUST link reviews to patient, provider, and completed procedure records.
- **REQ-013-007**: System MUST securely store and retrieve review photos with metadata.

### Security & Privacy Requirements

- **REQ-013-008**: System MUST alias reviewer identity by default and prevent exposure of PII in public views.
- **REQ-013-009**: System MUST encrypt review data and photos in transit and at rest and maintain auditable logs.
- **REQ-013-010**: System MUST support unpublish + archival for takedown and compliance requests.

### Integration Requirements

- **REQ-013-011**: System MUST send invite/reminder and status notifications via Notification Service.
- **REQ-013-012**: System MUST provide ratings summary endpoints for provider profiles with caching.

### Marking Unclear Requirements

No unresolved clarifications remain for V1 scope. Patient can edit their published review at any time (updated content published immediately). Admin can edit or remove post-publication for policy violations.

---

## Key Entities

- Review: overall rating, category ratings, feedback, status (Published / Removed by Admin), timestamps, links (patient, procedure, provider), source type (patient-submitted / admin-seeded "Verified Off-platform").
- ReviewPhoto: file references, thumbnails, alt text; associated review ID.
- AdminAction: action type (edit/remove), reason, admin identity, timestamp, changes made; associated review ID.
- ProviderResponse: text, author (provider), timestamp; associated review ID.

---

## Appendix: Change Log

| Date       | Version | Changes                                        | Author |
|------------|---------|------------------------------------------------|--------|
| 2025-11-11 | 1.0     | Initial PRD creation                           | AI     |
| 2025-11-11 | 1.1     | Filled scope, workflows, rules, and criteria   | AI     |
| 2026-03-03 | 1.2     | **Removed pre-publication moderation gate** — reviews now publish immediately upon patient submission (per client transcription: no moderation gate was requested). Admin retains post-publication edit/remove capability for policy violations. Key changes: (1) Main Flow updated — review published immediately, no "Pending Moderation" status; (2) A1/A2 workflows replaced — from approve/reject to post-publication remove/edit; (3) Screen 2 renamed from "Moderation Queue" to "Review Management"; (4) Patient can edit published review at any time; (5) Status values simplified to Published / Removed by Admin; (6) ModerationDecision entity replaced with AdminAction entity; (7) Admin-seeded reviews moved from Backlog to main admin scope per client transcription (AdminPlatform-Part1, lines 91–100); (8) All metrics, requirements, and business rules updated to reflect no-moderation model. | Product alignment (2026-03-03) |

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
**Based on**: FR-011 Aftercare & Recovery Management PRD
**Last Updated**: 2026-03-03
