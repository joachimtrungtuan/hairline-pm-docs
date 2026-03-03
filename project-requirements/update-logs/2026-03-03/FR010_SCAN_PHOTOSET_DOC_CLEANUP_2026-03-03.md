# FR-010 Scan Photo Set (V1) + System PRD Alignment

**Date**: 2026-03-03  
**Type**: Major Update  

**Documents Updated**:
- `local-docs/project-requirements/system-prd.md`
- `local-docs/project-requirements/system-technical-spec.md`
- `local-docs/project-requirements/system-data-schema.md`
- `local-docs/project-requirements/functional-requirements/fr010-treatment-execution/prd.md` (v1.5 → v1.6)
- `local-docs/project-requirements/functional-requirements/fr002-medical-history/prd.md`
- `local-docs/project-requirements/functional-requirements/fr003-inquiry-submission/prd.md`
- `local-docs/project-requirements/functional-requirements/fr011-aftercare-recovery-management/prd.md`
- `local-docs/project-requirements/functional-requirements/fr012-secure-messaging/prd.md`
- `local-docs/project-requirements/functional-requirements/fr016-admin-patient-mgmt/prd.md`
- `local-docs/project-requirements/constitution-summary.md`
- `local-docs/progress-tracking/module-progress-checklist-2025-11-12.md`
- `local-docs/progress-tracking/module-progress-checklist-2025-12-01.md`
- `local-docs/reports/2025-10-27/hairline-implementation-status-summary.md`
- `local-docs/testing-plans/2026-01-27/mobile-app-comprehensive-testing-plan.md`
- `local-docs/README.md`
- `local-docs/project-requirements/update-logs/2025-10-30/FR002_MINIMAL_SPECS_2025-10-30.md`
- `local-docs/project-requirements/update-logs/FR010_REVISION_2026-02-27.md`
- `local-docs/project-requirements/update-logs/FR010_REVISION_2026-02-28.md`
- `local-docs/project-requirements/update-logs/README.md`

---

## Summary

- Standardized head scan capture terminology for V1 as a photo set (true 3D deferred to V2) in FR-010 and system PRD.
- Propagated the V1 photo set note to related technical/spec/QA docs (system technical spec, data schema, testing plan, messaging admin actions).
- Updated no-show handling and payment responsibility language in system PRD to match current product decisions.
- Removed deprecated scan-overlay requirements/notes across local-docs (PRDs, logs, and progress trackers) to prevent implementation drift.

---

## Changes Applied

### 1) System PRD alignment

- FR-002: Removed scan-overlay requirement.
- FR-010: Updated requirements to the "Check In" model with outstanding-balance gating; clarified completion handoff to FR-011; described head scan assets as a V1 photo set.
- EC-004: Moved deposit/payout actions to admin review and reconciliation; system keeps No-Show as a flag/label and handles notifications.

### 2) FR-010 PRD (v1.6)

- Replaced "3D head scan" fields with "head scan photo set (V1)" across workflows, screens, requirements, entities, and edge cases.
- Normalized media limits and security wording (RBAC + file-type rules + encryption statements).
- Removed deprecated media policy notes; cleaned placeholders in approvals.

### 3) Cross-doc cleanup

- FR-002/FR-003/FR-011/FR-016: Removed scan-overlay wording from business rules, requirements, and acceptance scenarios; retained secure storage/access-control language.
- Progress trackers, reports, and update logs: Removed scan-overlay tasks/notes to keep implementation guidance consistent with current scope.

### 4) V1 scan terminology propagation

- `system-technical-spec.md`: Marked V1 scan capture as a photo set; moved ARKit/ARCore true 3D guidance to a V2 section.
- `system-data-schema.md`: Clarified `scan_url`/scan entities describe photo set media in V1 and true 3D assets in V2.
- `fr012-secure-messaging/prd.md`: Updated admin intervention wording to "request scan/photo set" (V1).
- `mobile-app-comprehensive-testing-plan.md`: Updated scan capture/monitoring tests to photo set terminology for V1; true 3D called out as V2.

---

## Follow-ups

- If we still need an explicit anti-leak control for media distribution, define an alternative (e.g., strict access controls + signed URLs + download audit + EXIF scrubbing) in the relevant services/FRs.
