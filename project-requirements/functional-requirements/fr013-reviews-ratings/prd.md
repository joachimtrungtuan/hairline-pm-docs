# Product Requirements Document: Reviews & Ratings

**Module**: P-02: Quote Request & Management | A-01: Patient Management & Oversight
**Feature Branch**: `fr013-reviews-ratings`
**Created**: 2025-11-11
**Status**: Draft
**Source**: FR-013 from local-docs/project-requirements/system-prd.md; Transcriptions (patient app, admin platform)

---

## Executive Summary

Enable verified patients to submit post‑procedure reviews with ratings and optional photos, subject to admin moderation before publication. Display provider ratings (average, count, distribution) and allow providers to respond publicly. This builds trust, informs patient decision‑making, and provides providers and Hairline with structured feedback for quality improvement while maintaining fairness, authenticity, and compliance.

---

## Module Scope

### Multi-Tenant Architecture

- Patient Platform (P-02): Submit a review after confirmed procedure completion (time-gated 3+ months), provide overall and category ratings, write feedback, optionally attach before/after photos, view own submitted review status (pending/approved/rejected), and edit prior to moderation decision.
- Provider Platform (PR-06 display context): View public reviews on provider profile, see rating averages and distribution, and post public responses to approved reviews.
- Admin Platform (A-01): Moderate incoming reviews (approve/reject with reason), redact PII/inappropriate content, manage flagged content, and produce reports on review volume and ratings trends.
- Shared Services (S-05, S-03): Media Storage for review photos; Notification Service for invite reminders, moderation outcomes, and provider reply alerts.

### Multi-Tenant Breakdown

Patient Platform (P-02):

- Receive invitation to review after procedure completion threshold.
- Submit ratings (overall 1–5 stars; category ratings) and feedback; optionally attach photos.
- View status and outcome of moderation; see published review on provider profile.

Provider Platform (display + response):

- View published reviews on their profile with averages and distribution.
- Post a public response to individual reviews; receive notification on new published reviews.

Admin Platform (A-01):

- Review moderation queue with filters (date, provider, rating, status, flagged).
- Approve, reject (with reason), or request edits; redact sensitive data.
- Manage review categories and invite cadence; export reports.

Shared Services (S-05, S-03):

- S-05 handles secure photo storage and retrieval.
- S-03 delivers invite/reminder emails/push and status notifications.

### Entry Points

- Time-gated invite after confirmed procedure completion (≥ 3 months) triggers review flow.
- Patient navigates to “Write a Review” from provider history.
- Providers access “Reviews” in dashboard to read and respond once published.
- Admins access “Moderation” from Admin platform navigation.

---

### Backlog (Future Enhancements)

- Admin-seeded authenticated reviews import for new providers (clearly flagged as “Verified Off‑platform” with verification source and date). Publication still follows moderation policy to maintain authenticity and fairness.

---

## Business Workflows

### Main Flow: Patient Submits a Review

Actors: Patient, System, Admin (later moderation)
Trigger: Patient opens “Write a Review” from invite or history
Outcome: Review submitted for moderation with ratings, feedback, and optional photos

Steps:

1. Patient completes overall and category ratings, enters feedback, and optionally attaches photos.
2. System validates inputs (rating ranges, feedback length, file type/size) and verifies eligibility.
3. System records the review as “Pending Moderation” and notifies Admin queue.
4. Patient sees confirmation and pending status; may edit until moderation begins.

### A1: Admin Moderation – Approve

- Trigger: Admin reviews a pending submission and approves it.
- Steps:
  1. Admin confirms no policy violations, optional redaction performed.
  2. System publishes the review and updates provider’s rating metrics.
- Outcome: Review appears on provider profile; patient and provider are notified.

### A2: Admin Moderation – Reject/Request Edits

- Trigger: Admin finds violation or requires clarification.
- Steps:
  1. Admin rejects with reason or requests edits.
  2. System notifies patient with reason; patient may resubmit.
- Outcome: Review remains unpublished until an approved version is submitted.

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
- One review per completed procedure; editing allowed until moderation starts.
- Clear photo guidelines; sensitive/identifying content discouraged.

Notes:

- Show progress and save-draft; disclose moderation and display policies.

---

### Screen 2: Admin – Moderation Queue

Purpose: Efficiently review, approve, reject, or request edits; manage flags.

Data Fields:

| Field Name    | Type   | Required | Description                                | Validation Rules       |
|---------------|--------|----------|--------------------------------------------|------------------------|
| Filters       | UI     | No       | Status, provider, date, rating, flags      | N/A                    |
| Review item   | Card   | Yes      | Ratings, feedback, photos, patient alias   | N/A                    |
| Actions       | Buttons| Yes      | Approve, Reject (reason), Request Edits    | Reason min 10 chars    |
| Redaction     | Tools  | No       | Remove PII/violations before approval      | Track changes in audit |

Business Rules:

- Every decision records moderator, timestamp, and reason.
- Redactions are tracked and visible in audit history.

Notes:

- Bulk actions for clear-cut spam; export moderation report.

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
- One review per completed procedure; subsequent updates via edit (pre‑moderation) or addendum after approval.
- Ratings use 1–5 scale with half‑stars display allowed for averages.

### Data & Privacy Rules

- Patient display name uses aliasing (e.g., first name + initial) by default.
- Photos and text must not expose sensitive personal information; admin may redact or reject.
- Reviews retained for minimum 7 years; takedown requests handled by unpublish + archival with restricted access.
- All moderation and publication actions are fully auditable (who, when, what, reason).

### Admin Editability Rules

Editable by Admin:

- Review categories/labels; invitation cadence and reminders.
- Photo guidelines text; moderation reasons catalogue.
- Visibility rules for display name (alias/full name toggle policy).

Fixed in Codebase (Not Editable):

- Eligibility logic requires completed procedure and time threshold.
- Minimum and maximum lengths for text fields and rating scale bounds.

Configurable with Restrictions:

- Flagging thresholds and auto‑hold rules (within safe bounds approved by policy).

Moderation Policy Notes:

- Admin-imported authenticated reviews must be flagged as "Verified Off‑platform" and subject to the same moderation standards before publication.

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

- SC-006: 95% of reviews receive a moderation decision within 48 hours.
- SC-007: 100% of decisions capture moderator, timestamp, and reason in audit log.

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
- S-03: Notification Service – invitations, reminders, and decision notifications.

### External Dependencies (APIs, Services)

- Email/push delivery providers for notifications (through S-03).

### Data Dependencies

- Completed procedure records with completion date and provider association.
- Provider profile identifiers for correct attribution and display.

---

## Assumptions

### User Behavior Assumptions

- Patients are willing to leave reviews when prompted and informed of moderation policy.
- Providers will respond to reviews to improve public trust.

### Technology Assumptions

- Modern mobile and web clients used; stable connectivity for uploads.
- Secure media storage available; common image formats supported.

### Business Process Assumptions

- Admin team monitors moderation queue daily during business hours.
- Legal/compliance guidance exists for defamation and takedown handling.

---

## Implementation Notes

### Technical Considerations

- Architecture: Separate review write path (pending) and read path (published) with audit logs.
- Media handling: Validate size/type, generate thumbnails; protect access.
- Anti‑abuse: Duplicate detection, keyword flags, rate limits for submissions and responses.

### Integration Points

- Patient app → Review service: submit, edit prior to moderation, status.
- Admin dashboard → Review service: moderation queue, decisions, audits.
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

Independent Test: Eligible test patient submits review with photos; appears in moderation queue.

Acceptance Scenarios:

1. Given an eligible patient, when they submit required ratings and feedback, then the review saves as Pending and confirms to the patient.
2. Given valid photos, when uploaded, then the system accepts and associates them with the review.

### User Story 2 – Admin approves a review (P1)

Why: Ensure quality and policy compliance.

Independent Test: Admin approves a pending review; it publishes with audit entry.

Acceptance Scenarios:

1. Given a pending review, when an admin approves it, then the review is published and ratings metrics update.
2. Given publication, when the provider profile loads, then averages and distribution reflect the new review.

### User Story 3 – Provider responds to a review (P2)

Why: Encourage constructive dialogue and trust.

Independent Test: Provider posts a response; response appears under the review and patient is notified.

Acceptance Scenarios:

1. Given a published review, when a provider posts a response, then it appears publicly under the review.
2. Given a new response, when notifications trigger, then the reviewer receives a notification.

### Edge Cases

- Ineligible attempts (too early/no completed procedure) are blocked with clear messaging.
- Photos exceed limits: user informed, upload prevented until compliant.
- Duplicate or spam reviews: auto‑flag and queue for moderation.
- Takedown request: review unpublished and archived; provider metrics recalculated.

---

## Functional Requirements Summary

### Core Requirements

- **REQ-013-001**: System MUST allow eligible patients to submit reviews (overall + categories, feedback, optional photos).
- **REQ-013-002**: System MUST enforce time gating (≥ 3 months) and single review per completed procedure.
- **REQ-013-003**: System MUST provide admin moderation with approve/reject/request edits and audit trail.
- **REQ-013-004**: System MUST publish approved reviews on provider profiles with provider responses.
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

No unresolved clarifications remain for V1 scope; editing after approval is limited to provider response. Future enhancements may include patient edit windows for typos post‑publication with re‑moderation.

---

## Key Entities

- Review: overall rating, category ratings, feedback, status, timestamps, links (patient, procedure, provider).
- ReviewPhoto: file references, thumbnails, alt text; associated review ID.
- ModerationDecision: status (approved/rejected/request edits), reason, moderator, timestamp.
- ProviderResponse: text, author (provider), timestamp; associated review ID.

---

## Appendix: Change Log

| Date       | Version | Changes                                        | Author |
|------------|---------|------------------------------------------------|--------|
| 2025-11-11 | 1.0     | Initial PRD creation                           | AI     |
| 2025-11-11 | 1.1     | Filled scope, workflows, rules, and criteria   | AI     |

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
**Last Updated**: 2025-11-03
