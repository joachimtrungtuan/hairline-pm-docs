# FR-022 Provider Status Filter Aligned with FR-015

**Date:** 2026-10-22
**Type:** PRD correction (minor; product decision by the user)
**Document:** `functional-requirements/fr022-search-filtering/prd.md` v2.17 → v2.18

## Why

B01 manual testing and the 2026-10-21 code review compared the admin provider list with FR-022 and FR-015 and found they disagreed. FR-022 listed a Draft provider status, an Approve action, and a default "All" status filter. FR-015 creates providers as Active, has no Draft status or Approve action, and opens the provider list on Active providers only. The user decided that FR-015 is correct.

## What Changed

- **FR-015 / Screen 1 Status filter:** the options are now Active, Suspended and Deactivated (Draft removed). The default is Active, which matches the FR-015 Screen 1 Default View. Clearing the filter shows every status.
- **Main Flow 2 diagram:**
  - The list opens on Active providers.
  - Reset restores the Active-only default.
  - The action node reads "manage status" instead of "approve onboarding".
- **User Story 2:**
  - Scenario 3 filters by Suspended instead of Draft and says that providers are created Active.
  - Scenario 5 points to the FR-015 status actions (Suspend, Reactivate, Deactivate) instead of an Approve action.
- Added the v2.18 row to Appendix: Change Log and set Last Updated to 2026-10-22.

## Not Changed

- FR-015 is unchanged, and no Change Request was raised. This is a small correction that brings FR-022 into line with FR-015.
- PRD status and approvals are unchanged.

## Related

- The bug-fix tasks for the provider list and status filter are in `project-automation/task-creation/2026-10-22/implementation-tasks-2026-10-22-001.md`.
