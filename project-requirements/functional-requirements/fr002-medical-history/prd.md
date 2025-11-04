# Medical History & 3D Scanning - Product Requirements Document (FR-002)

**Module**: P-07: 3D Scan Capture & Viewing (consumer) | S-01: 3D Media Processing Service | S-05: Media Storage Service | A-09: System Settings & Configuration (Questionnaire Templates Integration)  
**Feature Branch**: `002-medical-history-spec`  
**Created**: 2025-10-30  
**Status**: ✅ Verified & Approved  
**Source**: FR-002 from system-prd.md

## Executive Summary

FR-002 defines shared backend engines for processing medical intake data and head media, consumed by FR-003 (Inquiry) and others. It excludes patient-facing UI. The engine ingests medical questionnaire responses (defined/versioned via FR-025), generates severity alerts, validates and processes head media, applies anonymization/watermarking, and persists artifacts for provider review. For the current release, the patient app supplies a guided head video (not a 3D model); the engine validates and stores this media.
This FR covers backend engines only; patient capture UX is handled by FR-003 and consumed by `P-07` for V1.

## Module Scope

### Multi-Tenant Architecture

- **Shared Services (S-01, S-05)**: 3D Media Processing Service | Media Storage Service | Medical Intake Engine
- **Patient Platform (P-07)**: 3D Scan Capture & Viewing (consumer via FR-003)
- **Provider Platform (PR-02)**: Inquiry & Quote Management (read-only consumption)
- **Admin Platform (A-09)**: System Settings & Configuration (Questionnaire Templates Integration)

### Multi-Tenant Breakdown

**Patient Platform (P-07)**:

- Patient-facing capture UI is handled by FR-003 (Inquiry Submission module)
- Patient app submits questionnaire responses and head video to engine via FR-003
- Patients do not directly interact with FR-002 engine; all interaction through FR-003

**Provider Platform (PR-02)**:

- Providers consume read-only processed artifacts (normalized questionnaire, alerts, watermarked media)
- Provider review UI is handled by FR-003/PR-02; engine remains passive after initial processing
- Providers see anonymized artifacts until payment confirmation (per system PRD)

**Admin Platform (A-09)**:

- Admin manages questionnaire templates, sections, fields, and risk-tag rules via FR-025
- Admin configures validation rules, media constraints, and alert thresholds
- Admin cannot modify fixed security constraints (encryption, retention policies)
- Template versioning and publishing managed through FR-025; engine consumes published versions

**Shared Services (S-01, S-05)**:

- **S-01: 3D Media Processing Service**: Validates head video quality, applies watermarking, handles media transformations
- **S-05: Media Storage Service**: Stores processed media artifacts with secure access controls
- **Medical Intake Engine**: Validates questionnaire responses, computes severity alerts, normalizes data, manages versioning
- Engine operations are stateless between calls except for persisted artifacts
- All processing includes configuration version stamping (templateVersion, rulesetVersion)

### Communication Structure

**In Scope**:

- FR-003 → Engine: Submission of questionnaire responses and head video for processing
- Engine → FR-003: Return of normalized payload, alert tags, and media URIs
- Engine → Providers (via FR-003/PR-02): Read-only access to processed artifacts
- Admin → Engine (via FR-025): Template and rule configuration updates
- Engine → System: Automatic consumption of published template versions

**Out of Scope**:

- Patient-facing capture UI (handled by FR-003)
- Provider review UI (handled by FR-003/PR-02)
- Real-time chat between patients and providers
- Appointment scheduling functionality
- Pricing setup and quote management (covered by FR-004)
- Direct patient-provider communication

### Entry Points

1. **FR-003 Submission**: FR-003 (Inquiry Submission) calls engine API with questionnaire responses and head video
2. **Template Updates**: Engine automatically consumes updated templates/rules when FR-025 publishes new versions
3. **Admin Configuration**: Admin publishes template versions via FR-025 (A-09 settings); engine applies to new inquiries

## Business Workflows

### Workflow 1: Intake Processing (Engine Flow)

Actors: FR-003 (caller), Engine
Trigger: FR-003 submits questionnaire responses and media metadata to the engine
Outcome: Engine returns normalized intake payload, derived alerts, and stored media URI(s)

Main Flow:

1. FR-003 submits questionnaire responses (with templateVersion) and head video metadata.
2. Engine validates completeness against FR-025 template and media constraints.
3. Engine computes severity alerts/risk tags based on configured rules.
4. Engine watermarks head video with anonymized patient identifier and persists to storage.
5. Engine returns normalized intake payload, alert tags, and media URIs to FR-003.

Alternative Flows:

- A1: Media validation fails → Engine returns structured error codes and guidance for re-upload.
- A2: Template version mismatch → Engine records used version and returns policy-compliant response (or requests resubmission per FR-025 rules).

### Workflow 2: Distribution Consumption (Read Flow)

Actors: FR-003 (distributor), Providers (consumers)
Trigger: FR-003 requests engine-normalized payload and media URIs for distribution
Outcome: Providers receive read-only normalized payload and media links via FR-003

Main Flow:

1. FR-003 retrieves engine-normalized payload and media URIs.
2. FR-003 distributes to providers; providers consume read-only.
3. Provider actions (review, revision request) handled by FR-003/FR-004; engine remains passive.

### Workflow 3: Admin Template Management (Management)

Actors: Admin, System
Trigger: Admin publishes or deprecates questionnaire templates/rules in FR-025
Outcome: Engine consumes the published version and applies to new submissions

Main Flow:

1. Admin opens Medical Questionnaire Templates in settings.
2. Admin creates/edits templates: sections, fields, required/optional, help text, and risk-tag rules.
3. Admin publishes a template version; System versions templates and applies to new inquiries only.

Alternative Flows:

- C1: Admin deprecates a template → System keeps prior versions for existing inquiries; new inquiries use the latest published version.

## Screen Specifications (Minimal - Integration Contracts)

Backend-only: This FR provides integration contracts used by FR-003 (patient capture/distribution) and PR-02 (provider read-only). No user-facing screens are defined in this FR.

**Request (from FR-003)**:

- templateVersion (string)
- responses (object keyed by questionId per FR-025)
- media: one of
  - headVideo { uri, durationSeconds, sizeBytes, frameHints? }
  - altPhotos { uris[] } | altClips { uris[] }  // aligns with system PRD alt media support
- patientContext { anonymizedPatientId }

**Response (to FR-003 / PR-02)**:

- normalized { responsesNormalized, templateVersionUsed }
- alerts RiskTag[] { code, label, severity (info|warn|critical), rationale, derivedFrom }
- media { storedUri, watermarkRef, validationStatus }
- audit { processingId, processedAt }

**Rules**:

- Enforce FR-025 required fields and media constraints; stamp templateVersionUsed/rulesetVersion.
- Watermark media with anonymizedPatientId; no PII in payloads.
- Providers see anonymized artifacts until payment confirmation (system PRD alignment).
- On validation failure, return structured error codes and remediation guidance; do not persist artifacts.

## Business Rules

### General Rules

1. Engine operations are fully auditable (timestamps, actor/service, reasons on overrides).
2. Draft/submit/edit UX is defined in FR-003; engine is stateless between calls except persisted artifacts.
3. All processing includes configuration version stamping (templateVersion, rulesetVersion).

### Data & Privacy Rules

1. Patient PII is hidden from providers until booking payment is confirmed; providers see anonymized ID only.
2. Medical records retained minimum 7 years; deletion requests result in archival/anonymization (no hard deletes).
3. All access is role-based; admin access is logged with justification for sensitive views.

### Media Rules (Head Video Intake)

1. For this release, head media is a guided video file captured in the patient app and uploaded to the system.
2. Minimum duration: 15 seconds (configurable via A-09 policy); must include front, top, left, and right angles.
3. Maximum upload size: 50MB; basic brightness/blur checks enforced.
4. On validation failure, engine returns structured error codes and guidance to the caller (FR-003).

### Admin Editability

1. Admin can manage templates, guidance copy, and risk-tag rules.
2. Admin cannot alter fixed security constraints (e.g., password policy, OTP length).
3. Admin edits are versioned; prior versions remain accessible for existing inquiries.

## User Scenarios & Testing

### User Story 1 - Process Intake Payload (Priority: P1)

Why: Core value of engine; required for all downstream flows.

Independent Test: Submit valid responses + compliant head video metadata and verify normalized payload, alerts, and stored media URIs are returned within SLA.

Acceptance Scenarios:

1. Given valid responses and compliant media, When submitted, Then engine returns normalized payload, alerts, and stored URI in < 3s (p95)
2. Given responses reference a published templateVersion, When processed, Then response stamps templateVersionUsed and rulesetVersion
3. Given anonymizedPatientId in context, When media is stored, Then watermarkRef is present and no PII appears in payloads

### User Story 2 - Handle Validation Failures (Priority: P1)

Why: Clear guidance reduces retries and support burden.

Independent Test: Submit payloads violating media duration/size/quality and verify structured error codes with remediation guidance; no artifacts persisted.

Acceptance Scenarios:

1. Given video duration below minimum, When processed, Then engine returns MEDIA_DURATION_TOO_SHORT with guidance; no storage
2. Given file size exceeds limit, When processed, Then engine returns MEDIA_SIZE_EXCEEDED with compression guidance; no storage
3. Given brightness/blur below threshold, When processed, Then engine returns MEDIA_QUALITY_INSUFFICIENT with retake instructions; no storage

### Edge Cases

- Media too short or poor lighting: engine rejects with specific error codes and guidance.
- Template version mismatch: engine records used version and returns policy-compliant response.
- Oversize file: engine rejects with size error and suggested compression guidance.

## Success Criteria

### Provider Efficiency Metrics

- SC-002-P1: Providers can triage inquiry medical risk in under 2 minutes using engine-generated alerts (median).
- SC-002-P2: 95% of provider reviews do not require manual admin correction of alerts.

### Admin Management Metrics

- SC-002-A1: 100% of engine responses stamped with templateVersion and rulesetVersion used.
- SC-002-A2: Audit trail completeness is 100% for all engine operations (who/when/what-before/after).

### System Performance Metrics

- SC-002-S1: 99% of valid submissions produce normalized payload + media URIs in < 3 seconds (p95).
- SC-002-S2: 95% of compliant head videos pass validation on first attempt.
- SC-002-S3: 0% PII detected in engine responses during automated checks.

### Business Impact Metrics

- SC-002-B1: < 5% of engine rejections attributed to ambiguous error guidance (tracked via support tags).
- SC-002-B2: 80%+ of inquiries proceed to distribution without engine-related blockers.

---

## Functional Requirements Summary

### Core Requirements

- FR-002-CR1: Engine MUST validate responses against FR-025 template requirements
- FR-002-CR2: Engine MUST derive risk/alert tags deterministically from rules
- FR-002-CR3: Engine MUST validate, watermark, and persist media artifacts
- FR-002-CR4: Engine MUST return normalized payload, alerts, media URIs, and audit fields

### Data Requirements

- FR-002-DR1: Responses MUST be stamped with templateVersionUsed and rulesetVersion
- FR-002-DR2: Media artifacts MUST store watermarkRef and validationStatus
- FR-002-DR3: Audit records MUST capture processingId and processedAt

### Security & Privacy Requirements

- FR-002-SP1: No PII in engine responses; anonymized identifiers only
- FR-002-SP2: Media MUST be watermarked with anonymizedPatientId
- FR-002-SP3: All operations MUST be fully auditable and retention-compliant

### Integration Requirements

- FR-002-IR1: Engine MUST consume questionnaire templates/rules from FR-025 (read-only)
- FR-002-IR2: Engine MUST expose processing API consumed by FR-003
- FR-002-IR3: Engine MUST return structured error codes for validation failures

## Dependencies

### Internal Dependencies

- FR-003: Inquiry Submission & Distribution (caller for capture and distribution)
- FR-025: Medical Questionnaire Management (templates and rules)
- FR-020: Notifications & Alerts (used by consumer modules for user messaging)

### External Dependencies

- Cloud Storage Service: secure object storage for media artifacts (URIs consumed by FR-003/PR-02)
- Email/Notification Service (indirect via consumer modules): surface validation failures to patients/providers

### Data Dependencies

- Questionnaire templates, categories, and severity rules from Admin Settings (FR-025)

---

## Key Entities

- IntakeProcessingRequest: templateVersion, responses, media(headVideo|altPhotos|altClips), patientContext(anonymizedPatientId)
  - Key attributes: required fields completeness, media metadata
  - Relationships: references published questionnaire template (FR-025)

- IntakeProcessingResult: normalizedPayload, alerts[], mediaRef, audit
  - Key attributes: templateVersionUsed, rulesetVersion, processingId, processedAt
  - Relationships: links to stored media artifact and audit log

- RiskTag: code, label, severity(info|warn|critical), rationale, derivedFrom
  - Relationships: belongs to IntakeProcessingResult

- MediaArtifact: storedUri, watermarkRef, validationStatus, metadata
  - Relationships: referenced by IntakeProcessingResult

## Assumptions

### User Behavior Assumptions

- Patients capture and upload guided head videos following instructions in FR-003
- Providers review anonymized artifacts and alerts without requiring PII pre-payment
- Admins proactively maintain questionnaire templates and risk rules (FR-025)

### Technology Assumptions

- Patient devices can record compliant video (duration, size, quality) per policy
- Stable connectivity allows upload of video within size constraints
- Cloud storage is available for persisted media artifacts with secure access

### Business Process Assumptions

- FR-003 manages drafts/resubmissions and user communications
- New submissions use the latest published questionnaire/rules; existing retain prior versions
- All access is mediated by platform RBAC and immutable audit logging

## Implementation Notes

### Technical Considerations

- Stateless processing per request; artifacts persisted in storage with references returned
- Deterministic normalization and alert derivation based on versioned rules
- Media validation includes duration, size, brightness/blur heuristics

### Integration Points

- FR-003 → Engine: POST intake processing request (responses, templateVersion, media metadata)
- Engine → FR-003: normalized payload, alerts, media URIs, audit identifiers
- Engine ← FR-025: consumes published templates/rules (read-only)

### Scalability Considerations

- Asynchronous media processing where needed to meet p95 < 3s response target
- Storage lifecycle policies for long-term retention and quick retrieval
- Horizontal scaling of processing workers; rate limiting to protect services

### Security Considerations

- No PII in engine responses; anonymized identifiers only
- Media watermarked with anonymizedPatientId; artifacts access-controlled
- Full audit trail for processing operations and configuration versions

---

## Appendix: Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-10-30 | 1.0 | Initial PRD creation | Product & Engineering |
| 2025-11-04 | 1.1 | Template alignment: workflows metadata, assumptions, implementation notes, user scenarios, FR summary, key entities, external deps, status blocks | Product & Engineering |

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
|------|------|------|--------------------|
| Product Owner | [Name] | [Date] | [Status] |
| Technical Lead | [Name] | [Date] | [Status] |
| Stakeholder | [Name] | [Date] | [Status] |

---

**Document Status**: ✅ Complete  
**Maintained By**: Product & Engineering Teams  
**Review Cycle**: Monthly or upon major changes
