# Inquiry Configuration Change Request — 2026-09-04

## Summary

Recorded the approved client requirement to make inquiry treatment-area choices and the inquiry date blocked window configurable through Admin settings. This is a documentation decision only; implementation reconciliation remains required.

## Documents Updated

- `functional-requirements/fr003-inquiry-submission/prd.md` — v2.5 defines the dynamic treatment-area and lead-time consumer contract, with a 3-day default.
- `functional-requirements/fr026-app-settings-security/prd.md` — v1.6 defines Admin ownership, Workflow A6, Screen 5c, auditing, requirements, and entity contracts, with a 3-day default.
- `system-prd.md` — aligned the FR-003 and FR-026 summaries with the approved cross-FR contract.
- `functional-requirements/fr003-inquiry-submission/change-request-2026-09-04-inquiry-configuration.md` — before/after FR-003 contract and reconciliation boundary.
- `functional-requirements/fr026-app-settings-security/change-request-2026-09-04-inquiry-configuration.md` — before/after FR-026 ownership contract and reconciliation boundary.
- `product-plans/2026-05-29/sprint-1-readiness-fix-backlog.md` — added P-02-005 and P-02-006 with `Recorded only` status.

## Approved Contract

- Admin manages active, ordered treatment-area options with stable IDs, labels, and image/icon assets. Default seed options remain Hair, Beard, and Both.
- Admin sets the minimum inquiry lead time as a whole-day blocked window. The approved default is 3 days; a value of 3 makes the third day after today the first eligible date.
- The patient configuration response and backend submission validation must use the same current lead-time value.
- Existing inquiries retain their selected treatment-area snapshot when the catalog changes.

## Explicit Boundaries

- Location starting-price endpoint work is deferred and was not added to Sprint 1 scope.
- This does not claim that the existing mobile client already renders arbitrary dynamic options or assets. That compatibility must be demonstrated during implementation reconciliation.
- No source code, database migration, API implementation, or production configuration was changed.

## Same-Day Correction

- Product Owner clarified that the approved default minimum inquiry lead time is 3 days, not 30 days. FR-003 v2.3, FR-026 v1.6, the system PRD, the P-02-006 backlog row, both Change Requests, and the related draft task artifact were updated. The configurable range and all other date constraints are unchanged.
- Verification correction: FR-003 v2.4 limits exclusive-provider conversion and its decline fallback to FR-037. FR-038 remains self-service and converts only to FR-011. FR-003 now also declares FR-026 as the owner of its inquiry-configuration dependency.
- Verification correction: FR-003 v2.5 aligns Workflow 1's service-selection step with the dynamic Admin-managed treatment-area catalog; it no longer presents Hair, Beard, and Both as a fixed enum.

## Validation

- Verified the two backlog rows use `Recorded only` and do not carry task IDs.
- Verified each affected FR has its own approved Change Request, PRD version row, and reciprocal FR reference.
- Verified the requested pricing item is absent from this change set.
- Verification follow-up: FR-026 now names FR-003's treatment-area, lead-time, and snapshot integration plus S-05's treatment-area asset responsibility in Dependencies, and adds a dedicated end-to-end inquiry-configuration acceptance scenario.
- Verification follow-up: FR-026 v1.7 now rejects deactivation of the final active inquiry treatment-area option, preventing a configuration that would block all new inquiries.
