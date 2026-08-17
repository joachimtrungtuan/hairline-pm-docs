# FR-037 and FR-038 Monitoring Flows

**Date**: 2026-08-17
**Update Type**: Major functional-requirement creation and system-PRD alignment
**Status**: Draft PRDs created

## Summary

Created two independent monitoring FRs after FR-036:

- **FR-037 - Monitor Your Hair Loss**: Self-monitoring or provider-advice mode, optional longitudinal logs, Admin assignment/reassignment, cadence-limited provider advice, PDF export, and conversion into FR-003 treatment inquiry.
- **FR-038 - Monitor Your Transplant Progress**: Provider-free self-tracking, optional longitudinal logs, PDF export, and conversion into FR-011 standalone aftercare.

Both PRDs follow the canonical Spec Kit PRD template version 2.0.0 and define patient, provider where applicable, Admin, shared-service, workflow, screen, rule, data, success, dependency, testing, requirement, entity, change-log, and approval contracts.

## Confirmed Product Decisions Captured

### Shared Monitoring Contract

- A patient may have one active case per monitoring type, not one case globally.
- Logs are optional and use a consistent dated structure with severity from 1 to 10, notes, photos, and V1 standardized head scan photo sets.
- Monitoring completion generates a date-to-date PDF with complete logs, scan photos, logged-day count, and severity summary/trend.
- Admin may edit any case information, but every change requires immutable audit/version history.
- Previous monitoring history is not linked to a newly created monitoring case.

### FR-037 Hair-Loss Monitoring

- Patient chooses self-monitoring or provider-advice mode at case creation; mode cannot change mid-case.
- Advice-mode cases wait for Admin assignment while patient logging remains available.
- Provider may withdraw with a reason; case returns to Admin clearly marked for reassignment, and logging continues.
- Advice frequency is Admin-configurable as weekly or twice monthly.
- Advice mode requires the active FR-025 Inquiry medical questionnaire before provider access.
- Conversion to FR-003 pre-fills all compatible information, permits edits to every copied field, defaults to the latest scan while allowing another scan or retake, reconfirms medical answers, and attaches the monitoring PDF.
- Full monitoring-history linkage applies only during conversion into the distinct FR-003 inquiry.
- The assigned advice provider is the only initial quote recipient; without an assigned provider, standard FR-003 distribution applies.

### FR-038 Transplant-Progress Monitoring

- The feature is self-service only, with no provider advice, provider access, required cadence, milestones, overdue state, or compliance obligations.
- Intake reuses compatible external-treatment fields from FR-011 standalone aftercare.
- Conversion pre-fills an FR-011 standalone-aftercare request, permits edits to every copied field, defaults to the latest scan while allowing another scan or retake, and attaches the monitoring PDF.
- Monitoring completes by conversion only after successful standalone-request creation.
- FR-011 retains ownership of package selection, payment, Admin assignment, provider activation, milestones, and managed aftercare.

## Files Created

- `project-requirements/functional-requirements/fr037-monitor-hair-loss/prd.md`
- `project-requirements/functional-requirements/fr038-monitor-transplant-progress/prd.md`
- `project-requirements/update-logs/2026-08-17/FR037_FR038_MONITORING_FLOWS_2026-08-17.md`

## Files Updated

- `project-requirements/system-prd.md`: Added system-level FR-037 and FR-038 requirements and updated Last Updated date.
- `INDEX.md`: Updated system and functional-requirement counts to 38 and refreshed the index date.
- `project-requirements/update-logs/README.md`: Added this date section, functional-requirement quick reference, and Last Updated metadata.

## Scope Boundaries

- No source code under `main/` was changed.
- No existing FR-003, FR-011, FR-020, or FR-025 PRD was changed.
- No implementation tasks, database migration, API contract, design file, or Plane issue was created.
- True 3D scanning remains V2; V1 uses the existing standardized multi-view photo-set contract.

## Follow-Up

- Product, technical, design, and compliance review remain pending in both PRDs.
- Technical design should formalize shared monitoring entities, conversion idempotency, generated-PDF attachment handling, notification catalog entries, and provider authorization revocation.

## Subsequent Revisions

- **2026-08-17 - FR-037 v1.1**: Replaced the separate primary and alternative workflow diagrams with one unified conditional lifecycle flow covering duplicate-case handling, mode selection, medical validation, logging, Admin assignment/reassignment, provider review/advice/withdrawal, completion/PDF export, FR-003 conversion validation, and provider-routing outcomes.
- **2026-08-17 - FR-037 v1.2 and FR-038 v1.1**: Reorganized Screen Specifications using the verified multi-tenant FR convention: explicit Patient Platform Screens, Provider Platform Screens, and Admin Platform Screens sections with nested `#### Screen N` headings. Added tenant ownership summaries and made FR-038's absence of Provider Dashboard screens explicit.
- **2026-08-17 - Four service routes presentation**: Added a standalone nine-slide HTML deck at `reports/2026-08-17/hairline-four-service-routes-deck/index.html`. It summarizes the four patient entry routes, emphasizes FR-037, FR-038, and FR-011 across Patient, Provider, and Admin tenants, and uses looping animations to show monitoring and conversion data flows.
