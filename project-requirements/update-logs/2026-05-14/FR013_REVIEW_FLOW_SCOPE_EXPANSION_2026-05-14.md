# FR-013 Review Flow Scope Expansion

**Date**: 2026-05-14
**Report Type**: PRD Major Revision - Scope Alignment
**Affected Documents**:

- `local-docs/project-requirements/functional-requirements/fr013-reviews-ratings/prd.md`

---

## Summary

Expanded FR-013 to align with current phase scope and the latest reviewed UI flow direction: admin review insert/edit is now explicit in-phase scope, patient direct delete is replaced by a governed takedown request workflow, and screen/workflow coverage is expanded across Patient, Provider, and Admin platforms.

## Major Changes Applied

### 1) Scope and Workflow Alignment

- Clarified main-flow prerequisite: patient must have a completed treatment case.
- Added/updated alternative workflows:
  - Admin inserts authenticated review (`Verified Off-platform`)
  - Admin edits existing review
  - Patient submits takedown request
  - Admin approves/rejects takedown request
- Preserved no pre-publication moderation gate for patient submissions.

### 2) Screen Specifications Expansion

- Expanded from 3 high-level screens to 8 operational screens:
  - **Patient**: Submit Review, Submitted Reviews List, Review Detail + Takedown Request
  - **Provider**: Reviews List + Filters, Review Detail + Response
  - **Admin**: Reviews Management List, Review Detail/Insert/Edit, Takedown Requests Queue
- Added provider filter expectations for multi-case visibility where a patient can have multiple treatment cases with the same provider.
- Added admin filtering expectations by provider, patient, and case.

### 3) Governance and Rule Updates

- Replaced patient direct deletion with admin-decided takedown flow.
- Updated business rules, edge cases, and user stories to reflect takedown states and decisions.
- Updated admin action model to include insert/edit/remove and takedown decisions.

### 4) Requirement and Entity Updates

- Reworked and expanded REQ set to cover:
  - Patient list/detail/takedown surfaces
  - Provider list/filter/detail surfaces
  - Admin insert/edit/remove/takedown decision operations
  - Canonical schema continuity across tenants
- Added explicit `TakedownRequest` entity and expanded `AdminAction` semantics.

---

## Resulting Version State

- FR-013 PRD updated to **v1.10**
- `Last Updated` set to **2026-05-14**
- Scope now reflects current-phase operational requirements for patient/provider/admin review management, patient-facing provider review display, review settings/export, and takedown processing.

## Follow-Up Alignment (Same Day)

- Reconciled takedown/detail interactions with the shared mobile UI flow screenshots and `local-docs/reports/2026-02-05/missing-mobile-flows-design-complement.md` (`P05.3` section).
- Added patient review-detail requirements for:
  - Provider response block visibility
  - Read-only removed state with admin removal reason
  - Pre-filled edit flow for published reviews
  - Takedown bottom-sheet/modal behavior with optional patient message
  - Mandatory 7-year retention notice before takedown submission
- Added patient list-sort and empty-state details to align with the documented mobile flow.
- Added another same-day UI alignment for Patient `My Reviews` list to match the latest visual: header title + sort icon, card-level rating/time row, treatment line, excerpt + "See more", provider avatar/name row, and app-facing status badges.
- Added provider-side follow-up refinements: provider review list now explicitly supports filtering by patient, and Provider Review Detail now includes a detailed inline Provider Response Composer interaction model/state (non-separate screen) with validation, cancel/submit behavior, and post-publish immutability rules.
- Added incremental screen-number cleanup and coverage expansion: replaced the non-incremental `Screen 5A` label with a merged inline composer state inside Provider Review Detail, renumbered the Screen Specifications to `Screen 1` through `Screen 10`, added patient-facing Provider Profile Reviews for clinic/provider review display, added Admin Review Settings & Export, and synchronized related requirements, user stories, metrics, entities, and changelog entry `v1.8`.
- Cleaned up Screen Specifications heading hierarchy by removing the duplicate Patient Platform subsection heading so Screens 1-4 sit under one Patient Platform section before Provider/Admin sections.
- Clarified Screen 4 as an embedded Provider Profile Reviews Section inside the quoting/provider-profile review flow, not a standalone provider profile screen; removed duplicated provider-profile content and kept only FR-013 review fields, `View all`, preview/full-list behavior, and data-model connection notes.
- Clarified Screen 5 context: Provider Reviews List & Filters may appear as a dedicated Provider Dashboard list or be embedded/linked from the provider's own profile detail section, final placement is left to UX/UI design, and non-review profile fields remain owned by the provider profile detail spec.
- Added `Admin removal reason` to Screen 9 so approved takedown/removal decisions persist the same patient-facing reason shown on Screen 3 when review status is `Removed`.
- Verification follow-up after FR-013 review: aligned `system-prd.md` to immediate review publication with post-publication admin flagging/removal instead of pre-publication moderation; expanded FR-013 module/dependency traceability to include PR-06, S-03, S-05, FR-020, FR-022, FR-030, and FR-032; added FR-013 PRD changelog entry `v1.9`.
- Backend-aligned review status vocabulary after code inspection: removed `Submitted` as a review status, kept patient-facing status to `Published` / `Removed`, documented `Flagged` as admin-internal, and separated takedown request state (`Pending` / `Approved` / `Rejected`) from review visibility status; added FR-013 PRD changelog entry `v1.10`.
