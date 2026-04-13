# FR-022 Follow-Up Alignment

**Date**: 2026-04-13  
**Scope**: User-directed follow-up edits after `FR-022` verification

---

## Summary

Applied the selected follow-up resolutions across the search/filter documentation set:

1. Updated `system-prd.md` to follow `FR-003 / Screen 7a` for patient provider discovery criteria.
2. Removed unsupported export behavior from `FR-012 / Screen 5` so conversation-list export remains deferred until a dedicated export requirement is re-specified.
3. Removed unsupported admin global-search and cross-module-search claims from `FR-022` entry points.

Per user instruction, the Screen 7a contract change for Issue 1 was limited to `system-prd.md`. `FR-022` was not updated for that specific filter-set discrepancy in this pass.

---

## Files Updated

- `local-docs/project-requirements/system-prd.md`
  - Replaced the stale Screen 7a filter summary with wording that matches the current `FR-003` provider-selection criteria.

- `local-docs/project-requirements/functional-requirements/fr012-secure-messaging/prd.md`
  - Removed Screen 5 export statements from Business Rules and Notes.
  - Added an internal change-log entry documenting the deferral.

- `local-docs/project-requirements/functional-requirements/fr022-search-filtering/prd.md`
  - Removed unsupported admin global-search and cross-module-search entry-point bullets.
  - Added an internal change-log entry documenting the follow-up decision.

---

## Rationale

- `FR-003` was chosen as the authority for Screen 7a behavior.
- `FR-012` export language conflicted with the deferred/export-incomplete stance already established in `FR-022`.
- The admin global-search claim in `FR-022` had no backing source FR or screen specification.

---

## Outcome

- System PRD now matches the current `FR-003` Screen 7a description.
- Messaging export is no longer implied as part of the approved `FR-012` monitoring screen scope.
- `FR-022` no longer overstates unsupported admin entry-point behavior.
