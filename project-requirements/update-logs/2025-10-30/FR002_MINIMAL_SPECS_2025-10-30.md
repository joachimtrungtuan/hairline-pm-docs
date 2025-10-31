# FR-002 Minimal Screen Specs & Consistency Check - October 30, 2025

Status: ✅ Complete

Scope: Reduce FR-002 Screen Specifications to minimal integration contracts and verify consistency with system PRD and client transcriptions.

## Changes

- Replaced expanded screen subsections with a single "Screen Specifications (Minimal - Integration Contracts)":
  - Request: templateVersion, responses, media (headVideo | altPhotos | altClips), patientContext
  - Response: normalized, alerts, media, audit
  - Rules: enforce FR-025 constraints; watermark; anonymization until payment; structured errors
- Clarified V1 head-video ingestion with alternative media support; 3D model ingestion remains a future extension handled by consumer UIs.
- Simplification: Removed user stories and numbered functional requirements; retained only integration contracts, business rules, and edge cases.

## Consistency Verification

- Matched `system-prd.md` FR-002 items:
  - Alt media support (photos/videos) — included
  - Scan validation feedback — structured error codes with guidance
  - Watermarking with unique/anonymized identifier — included
  - Medical history/risk alerts — RiskTag severity mapping retained
  - Anonymization until payment — enforced in rules
- Aligned with transcriptions: provider reads anonymized intake; engine provides normalized payload and media URIs.

## Notes

- Full UI screens remain in FR-003 (patient capture/distribution) and PR-02 (provider review).
