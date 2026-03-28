# Design Layout Verification Report — FR-016

**Report Date**: 2026-03-27
**Report Type**: Design Layout Verification
**FR Scope**: FR-016 — Admin Patient Management
**Flow Scope**: Screen 8 within B5: Patient requests data deletion (GDPR)
**Layout Source**: `layout-temp/`, `layout-temp/Patient Deletion Requests Detailed/`
**Platform**: Admin Web
**Status**: 🟡 PARTIAL

---

## Summary Dashboard

| # | Flow | Module | Screens Required | Screens Verified | Layout Status | Field Coverage |
|---|------|--------|-----------------|-----------------|---------------|----------------|
| B5 | Patient requests data deletion (GDPR) | A-01: Patient Management & Oversight | 1 | 1 | 🟡 PARTIAL | ~63% |

**Overall**: 1 of 1 flows verified. The deletion-request flow is PARTIAL: the list and modal states exist, but the queue defaults, key table columns, row action treatment, and audit/compliance evidence do not fully match the FR.
**Screens**: 1 of 1 specified screens have layouts (100% layout coverage).

---

## Layout File Inventory

### Mapped to Spec Flows

| Layout File | Maps to Flow | Maps to Screen |
|-------------|-------------|----------------|
| `layout-temp/Filter.jpg` | B5 | Screen 8 (Patient Deletion Requests List (GDPR)) — filtered list state |
| `layout-temp/Fulltable overview.jpg` | B5 | Screen 8 (Patient Deletion Requests List (GDPR)) — full-width table overview |
| `layout-temp/Patient Deletion Requests Detailed/Status_ Pending Admin Review.jpg` | B5 | Screen 8 (Patient Deletion Requests List (GDPR)) — review modal / pending state |
| `layout-temp/Patient Deletion Requests Detailed/Status_ Approved.jpg` | B5 | Screen 8 (Patient Deletion Requests List (GDPR)) — approved state variant |

### Unmapped Files

| Layout File | Likely Purpose | Notes |
|-------------|---------------|-------|
| `layout-temp/Patients.jpg` | Patient list or overview screen from a different FR-016 screen | Outside current Screen 8 scope |

---

## Detailed Verification by Flow

---

### Flow B5: Patient requests data deletion (GDPR)

**Status**: 🟡 PARTIAL — the screen is recognizable and covers the queue plus review modal, but it diverges from the FR in default filtering, identifier/column treatment, action disclosure, and audit/compliance support
**Screens required**: 1
**Layout files**: `layout-temp/Filter.jpg`, `layout-temp/Fulltable overview.jpg`, `layout-temp/Patient Deletion Requests Detailed/Status_ Pending Admin Review.jpg`, `layout-temp/Patient Deletion Requests Detailed/Status_ Approved.jpg`

#### Screen 8: Patient Deletion Requests List (GDPR)

**Layout**: `layout-temp/Filter.jpg`, `layout-temp/Fulltable overview.jpg`, `layout-temp/Patient Deletion Requests Detailed/Status_ Pending Admin Review.jpg`, `layout-temp/Patient Deletion Requests Detailed/Status_ Approved.jpg`

##### Flow Context

- **User arrives from**: `User Management → Patients → Deletion Requests`, as defined in User Story 6 acceptance scenario 1 and reflected by the breadcrumb plus active `Patient Deletion Requests` tab in the provided modal-backed layouts
- **Screen purpose**: Provide the admin queue for GDPR deletion requests, let the admin inspect a request, optionally contact the patient, and approve or deny the request
- **Entry point**: Present — `Status_ Pending Admin Review.jpg` and `Status_ Approved.jpg` show the breadcrumb `User Management / Patients` and an active `Patient Deletion Requests` tab, matching the PRD route in the Screen 8 spec and User Story 6 acceptance scenario
- **Exit path**: Partial — the modal provides `Approve`, `Deny`, and `Close` actions in the pending state, but there is no visible audit-trail link and no provided state showing the required blocked-approval message or enhanced confirmation/justification step
- **Data continuity**: Partial — patient identity, submitted timestamp, reason, and SLA due date carry from the table into the modal, but the identifier format changes between HPID-style values and short alphanumeric IDs across the provided layouts
- **Flow context issues**: No layout shows the empty-state queue, the approval-blocked state for active obligations, or the required audit-trail access after approve/deny actions

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Screen Title | Yes | ✅ | Functionally present as the active `Patient Deletion Requests` tab under `User Management / Patients` in `layout-temp/Patient Deletion Requests Detailed/Status_ Pending Admin Review.jpg` and `layout-temp/Patient Deletion Requests Detailed/Status_ Approved.jpg`, matching the Screen 8 placement requirement in FR-016 PRD lines 580-581 |
| Search | No | ✅ | Search input is visible at the top-right of the list screen behind the modal in both `Status_ Pending Admin Review.jpg` and `Status_ Approved.jpg`; debounce/case-insensitive behavior cannot be verified from static layouts |
| Filters | No | ❌⚠️ | `layout-temp/Filter.jpg` provides filters for `Patient ID`, `Patient Name`, and `Current Status`, but the filter set does not expose patient email and the default `Pending Admin Review` state is not shown as preselected even though the FR requires that default |
| Deletion Requests Table | Yes | ✅ | The queue table is clearly present in `layout-temp/Fulltable overview.jpg`, but the visible rows mix `Pending Admin Review` and `Approved` requests and are not obviously sorted by oldest pending first as required by FR-016 PRD lines 583-590 |
| Table Column: Patient ID | Yes | ❌⚠️ | Present in `layout-temp/Fulltable overview.jpg`, but the left-hand table variant and both modal states use short alphanumeric IDs such as `9F4E5D2A` instead of the specified HPID-style identifier |
| Table Column: Patient Name | Yes | ✅ | Present in `layout-temp/Fulltable overview.jpg`; each row shows the patient name and implies row-level identity continuity into the modal |
| Table Column: Patient Email | Yes | ❌⚠️ | Email is visible in `layout-temp/Fulltable overview.jpg`, but it is merged under `Patient Name` rather than shown as its own required read-only column |
| Table Column: Submitted At | Yes | ❌⚠️ | The left table variant in `layout-temp/Fulltable overview.jpg` shows `Submitted At` with datetime values, but the right table variant drops the column entirely, so the required field is not preserved consistently across the provided layouts |
| Table Column: Reason (Optional) | No | ✅ | Present in `layout-temp/Fulltable overview.jpg`, and the modal expands the same reason text in both `Status_ Pending Admin Review.jpg` and `Status_ Approved.jpg`, which aligns with the FR's truncated-in-table / expanded-in-modal pattern |
| Table Column: SLA Due By | Yes | ❌⚠️ | Present in `layout-temp/Fulltable overview.jpg` and both modal states, but displayed as a date without time even though the FR defines the field as `datetime`; some rows are also visually truncated (`November 5, 20...`) |
| Table Column: Actions | Yes | ❌⚠️ | The list uses an unlabeled kebab menu in `layout-temp/Fulltable overview.jpg` instead of the specified direct `Review` action that should open the review/approve modal |
| Empty State | Conditional | ✅ | The provided layouts all show populated queue states, so the absence of the empty-state message is acceptable for this non-triggering condition; no dedicated empty-state mock was provided |
| Review / Approve Modal | Conditional | ✅ | Present in both `layout-temp/Patient Deletion Requests Detailed/Status_ Pending Admin Review.jpg` and `layout-temp/Patient Deletion Requests Detailed/Status_ Approved.jpg`, matching the modal requirement when the admin reviews a request |
| Modal: Patient Summary | Yes | ✅ | The modal header block shows patient name, email, and patient identifier in both modal layouts; the summary group is clearly present even though the identifier format is inconsistent with the HPID requirement noted above |
| Modal: Request Details | Yes | ✅ | The modal includes `Submitted At`, `SLA Due By`, and `Reason` in both states, satisfying the required request-details group from FR-016 PRD lines 594-596 |
| Modal: Contact Options | Yes | ❌⚠️ | The call/email actions are present in both modal layouts, but only as icon buttons with no visible `Call patient` / `Email patient` labels, making the quick actions less explicit than specified |
| Modal: Admin Notes | No | ✅ | `Admin Notes` textarea is present in both `Status_ Pending Admin Review.jpg` and `Status_ Approved.jpg` |
| Modal: Approve Button | Conditional | ✅ | `Approve` appears as a primary green action in `layout-temp/Patient Deletion Requests Detailed/Status_ Pending Admin Review.jpg`; the required confirmation/justification step cannot be verified from the provided static layouts |
| Modal: Deny Button | Conditional | ✅ | `Deny` appears as a red destructive action in `layout-temp/Patient Deletion Requests Detailed/Status_ Pending Admin Review.jpg`; the required justification step cannot be verified from the provided static layouts |
| Modal: Close Button | Yes | ✅ | `Close` is visible in both modal states, and the modal also includes a top-right dismiss icon |
| Audit Trail Link | Yes | ❌ | No audit-trail link is visible in the list or the modal in any provided layout, even though FR-016 PRD line 600 requires a direct link to the request's audit records |

**Extra Elements**:

- Pagination controls (`Total 85 items`, page numbers, `10/page`) appear in the modal-backed list view, but pagination is not explicitly listed in the Screen 8 data fields table
- Patient avatar chips are displayed beside names in the table and modal summary, though avatars are not specified in the Screen 8 field list
- The modal includes a `Current Status` row in addition to the required request details; this is useful context but not part of the explicit Screen 8 request-details definition

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 10/16 required fields fully matched (63%)
**Critical Issues**: Missing `Audit Trail Link`; list action is hidden behind a kebab menu instead of exposing the required `Review` action directly

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-16` / `U-17`: The list's primary row action is hidden behind an unlabeled kebab menu in `layout-temp/Fulltable overview.jpg`, so the screen does not visually communicate the FR's intended `Review` action as the obvious next step. | Replace the kebab-only treatment with a visible `Review` button or add a clearly labeled primary action in each row. |
| ⚠️ UX Improvement | `U-11` / `U-16`: The modal contact actions in `layout-temp/Patient Deletion Requests Detailed/Status_ Pending Admin Review.jpg` and `layout-temp/Patient Deletion Requests Detailed/Status_ Approved.jpg` are icon-only circles, which makes `Call patient` versus `Email patient` less explicit than the FR wording. | Add text labels or tooltipped icon buttons so the quick actions are immediately understandable without icon interpretation. |
| ⚠️ UX Improvement | `W-06` / `W-08`: The provided table variants are structurally inconsistent. One variant shows `Submitted At` and non-HPID IDs while the other drops `Submitted At` and reflows the columns, which makes the queue harder to scan and undermines confidence that the same required data will remain visible across states. | Standardize the table schema across all variants: keep HPID, Patient Name, Patient Email, Submitted At, Reason, SLA Due By, Current Status, and a direct review action visible in the default queue. |
| 💡 UX Suggestion | `U-03` / `W-05`: The filter drawer in `layout-temp/Filter.jpg` is visually clean but sparse, and it separates targeted fields (`Patient ID`, `Patient Name`, `Current Status`) from the main search input without clarifying how the two mechanisms work together. | Add helper text or a clearer label hierarchy so admins understand when to use global search versus structured filters. |

**Flow Coverage Gaps**:

- No empty-state layout was provided for the conditional `No pending deletion requests` scenario
- No layout shows the blocked approval state required when the patient has active obligations and approval must be prevented with an actionable message
- No layout shows the enhanced confirmation + justification step required for approve/deny actions under the Screen 8 business rules
- No layout shows the required audit-trail link or the post-action audit access path

---

## Action Items

| Priority | Flow | Screen | Issue | Recommendation |
|----------|------|--------|-------|----------------|
| 🔴 Critical | B5 | Screen 8 | The required `Audit Trail Link` is missing from all provided layouts, leaving no visible access path to request-specific audit records after review decisions. | Add a clear audit-trail entry point in the list or modal that opens Screen 7 filtered to the request ID, as required by FR-016 PRD line 600. |
| ⚠️ Important | B5 | Screen 8 | The queue does not behave like the specified default pending-review list: provided table states mix `Approved` and `Pending Admin Review` rows, and the filter UI does not show the required default `Pending Admin Review` state. | Align the default queue and filter state with the FR so admins land on pending requests sorted by oldest pending first. |
| ⚠️ Important | B5 | Screen 8 | The table schema is inconsistent with the FR: patient email is merged into the name cell, submitted-at visibility changes across variants, and some identifiers are not HPID-style values. | Normalize the table columns and identifiers across all screen variants so the required data is always visible in the same places. |
| ⚠️ Important | B5 | Screen 8 | The required `Review` action is hidden behind an unlabeled kebab menu instead of being surfaced directly in the Actions column. | Expose `Review` as the primary row action and keep secondary actions, if any, behind an overflow menu. |
| ⚠️ Important | B5 | Screen 8 | The design set does not show the approval-blocked state or the enhanced confirmation/justification step required by the Screen 8 business rules. | Add dedicated layouts for blocked approval and confirmation/justification so development has the necessary compliance states. |
| 💡 Suggestion | B5 | Screen 8 | The modal contact buttons rely on icon-only affordances, which makes the quick actions slightly less explicit than the FR wording. | Add text labels or tooltips for `Call patient` and `Email patient`. |

### Priority Legend

- **🔴 Critical**: Blocks flow progression, breaks data integrity, or causes security/legal risk. Must fix before development.
- **🔴 Critical UX**: Severe usability issue that would prevent users from completing the flow or cause significant confusion. Must fix before development.
- **⚠️ Important**: Functional discrepancy that could cause user confusion or require rework during development. Should fix before development.
- **⚠️ UX Improvement**: Usability or design quality issue that deviates from platform conventions or best practices. Should fix before development.
- **💡 Suggestion**: Cosmetic or minor improvement. Can fix anytime.
- **💡 UX Suggestion**: Minor design enhancement that would improve polish. Can fix anytime.

---

## Notes

- Verification source: `local-docs/project-requirements/functional-requirements/fr016-admin-patient-mgmt/prd.md`
- Flow context source: `B5: Patient requests data deletion (GDPR)` in FR-016 PRD lines 259-274 and `User Story 6` acceptance scenarios in lines 932-945
- Field checks were performed against Screen 8 in FR-016 PRD lines 572-610 and the following layout files: `layout-temp/Filter.jpg`, `layout-temp/Fulltable overview.jpg`, `layout-temp/Patient Deletion Requests Detailed/Status_ Pending Admin Review.jpg`, `layout-temp/Patient Deletion Requests Detailed/Status_ Approved.jpg`
- Hidden file `.DS_Store` in `layout-temp/` ignored.
