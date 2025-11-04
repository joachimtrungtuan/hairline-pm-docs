# Medical History & 3D Scanning - Product Requirements Document (FR-002)

**Module**: P-07: 3D Scan Capture & Viewing (consumer) | S-01: 3D Media Processing Service | S-05: Media Storage Service | A-09: System Settings & Configuration (Questionnaire Templates Integration)  
**Feature Branch**: `002-medical-history-spec`  
**Created**: 2025-10-30  
**Status**: Verified & Approved  
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

Main Flow:

1. FR-003 retrieves engine-normalized payload and media URIs.
2. FR-003 distributes to providers; providers consume read-only.
3. Provider actions (review, revision request) handled by FR-003/FR-004; engine remains passive.

### Workflow 3: Admin Template Management (Management)

Actors: Admin, System

Main Flow:

1. Admin opens Medical Questionnaire Templates in settings.
2. Admin creates/edits templates: sections, fields, required/optional, help text, and risk-tag rules.
3. Admin publishes a template version; System versions templates and applies to new inquiries only.

Alternative Flows:

- C1: Admin deprecates a template → System keeps prior versions for existing inquiries; new inquiries use the latest published version.

## Screen Specifications (Minimal - Integration Contracts)

This FR exposes backend contracts used by FR-003 (patient capture/distribution) and PR-02 (provider read-only). UI screens live in those FRs.

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

## Edge Cases

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

## Dependencies

### Internal Dependencies

- FR-003: Inquiry Submission & Distribution (caller for capture and distribution)
- FR-025: Medical Questionnaire Management (templates and rules)
- FR-020: Notifications & Alerts (used by consumer modules for user messaging)

### Data Dependencies

- Questionnaire templates, categories, and severity rules from Admin Settings (FR-025)

## Assumptions

1. FR-003 handles all patient-facing capture, drafts, and submissions.
2. Patients use smartphones capable of recording compliant video under guidance.
3. Admin maintains questionnaire templates and risk rules proactively via FR-025.
4. Providers consume anonymized artifacts via FR-003/PR-02 without PII pre-payment.

## Implementation Notes

Technical details intentionally omitted; this PRD focuses on user value, scope, rules, and outcomes. Security, retention, anonymization, audit, and non-deletion policies follow the Constitution.

---

**Document Status**: Draft  
**Maintained By**: Product & Engineering Teams  
**Review Cycle**: Monthly or upon major changes
