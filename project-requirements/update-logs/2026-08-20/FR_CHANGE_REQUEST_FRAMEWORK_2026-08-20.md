# FR Change Request Framework

**Date**: 2026-08-20
**Documents**:
- `project-requirements/templates/change-request-template.md`
- `INDEX.md`
- FR-local Change Requests for FR-003, FR-004, FR-020, FR-025, FR-030, and FR-037
- The corresponding PRD change-log links

**Trigger**: Product-owner decision to preserve before/after traceability when a major requirement event changes FRs that may already be verified or implemented.

---

## Decision Applied

- A Change Request is required only for a major event: a new or materially revised FR changes another verified or implemented FR, or an approved restructure substantially changes requirements, ownership, workflow, data, security, or integration contracts.
- Small corrections remain in the PRD change log and normal update log.
- Each affected FR receives its own immutable Change Request file beside `prd.md`.
- The PRD remains the current approved contract. The Change Request preserves the baseline, approved delta, rationale, affected contracts, and implementation-reconciliation status.
- Documentation approval and implementation verification are separate statuses. A Change Request must not imply that deployed behavior already matches the revised PRD.
- Project-owned Change Request templates live under `project-requirements/templates/`. This location decision was expanded later the same day so all templates are physically project-owned there; `.specify/templates/` is now only the Spec Kit compatibility symlink. See `TEMPLATE_OWNERSHIP_RELOCATION_2026-08-20.md`.

## FR-037 Event Coverage

- FR-003 records the v1.8 exclusive-routing addition and v1.9 explicit-decline fallback.
- FR-004 records restricted initial quote authorization.
- FR-020 records monitoring delivery events.
- FR-025 records Inquiry-context questionnaire reuse for monitoring advice.
- FR-030 records the source-of-truth monitoring event configuration.
- FR-037 records the complete cross-FR decision and v1.9 clarification.

## Validation

- Confirmed affected FRs against commit `7317cc4` and the v1.9 follow-up against commit `935283e`.
- Confirmed every affected PRD change-log row links to its FR-local Change Request.
- Confirmed all Change Requests retain `Implementation Reconciliation: Required` until implementation evidence is reviewed.
- Confirmed `.specify/templates/` and its hardcoded script paths remain unchanged.
