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

- Shared Services: Medical Intake Engine (questionnaire validation, alert generation); 3D Media Processing (validation, watermarking); Media Storage
- Consumer Modules: FR-003 Inquiry (capture and distribution), PR-02 Provider Review (read-only consumption), FR-011 Aftercare (follow-up media)
- Admin Platform (A-09): Questionnaire templates and risk-tag rules powering the engine

### Communication Structure

- This FR exposes backend contracts only; patient/provider UI is handled in FR-003/PR-02.
- Admin ↔ System: Templates and rules are managed in FR-025; the engine consumes published versions.

Out-of-scope for this FR: Real-time chat, appointment scheduling, and pricing setup (covered by other FRs).

### Entry Points

1. FR-003 submits questionnaire responses and head video to the engine
2. Engine validates, normalizes, watermarks and stores artifacts; returns payload to FR-003
3. Engine consumes updated templates/rules upon FR-025 publication

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
