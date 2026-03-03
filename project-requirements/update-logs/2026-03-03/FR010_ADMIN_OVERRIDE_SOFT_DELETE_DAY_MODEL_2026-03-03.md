# FR-010 Alignment — Admin Override (Reasoned Audit), Soft Delete Only, Day-Only In Progress Model

**Date**: 2026-03-03  
**Type**: Major Update  
**Documents**:
- `local-docs/project-requirements/functional-requirements/fr010-treatment-execution/prd.md` (v1.6 → v1.7)
- `local-docs/project-requirements/functional-requirements/fr004-quote-submission/prd.md` (v1.6 → v1.7)

---

## Summary

Aligned FR-010 treatment execution documentation rules to product decisions:

- In Progress is **day-only** (per-day status + quote-provided day description + per-day notes)
- Admin can override locked fields **at any time**, but overrides require a **reasoned audit trail**
- All delete/remove actions are **soft delete (archive) only**; no hard deletes for PHI media or treatment documentation

---

## Changes Applied

### 1) FR-010 — Day-only progress model (no “activity status”)

- Removed “activity completion/status” wording from scope, success criteria, and integration notes
- Removed `activity_status_updated` event type; day progress is represented as **day status** only
- Standardized terminology to **Treatment Plan (per-day)** seeded from the accepted quote (`plan`)

### 2) FR-010 — Admin override with reason + preserved audit history

- Clarified that provider locks after Check In remain, but **admin can override** clinician / plan-related fields when needed
- Added explicit requirement: **each admin edit must include a reason**, stored with before/after values in audit trail

### 3) FR-010 — Soft delete only for treatment media and documentation

- Updated admin media “remove” behavior to **archive (soft-delete)** with retention + restore semantics
- Updated audit rule to explicitly forbid hard deletes for treatment documentation + associated media

### 4) FR-004 — Quote `plan` schema clarified for downstream FR-010

- Defined **Treatment Plan (per-day)** entry fields: `dayNumber`, `date`, `description`
- Documented `plan` as ordered per-day entries used by FR-010 to seed day descriptions (read-only in FR-010)

