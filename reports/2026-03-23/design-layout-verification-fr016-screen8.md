# Design Layout Verification Report — FR-016

**Report Date**: 2026-03-23
**Report Type**: Design Layout Verification
**FR Scope**: FR-016 - Admin Patient Management
**Flow Scope**: Specific screen check: Screen 8 - Patient Deletion Requests List (GDPR)
**Layout Source**: `layout-temp/` and `layout-temp/Patient Deletion Requests Detailed/`
**Platform**: Admin Web
**Status**: 🔴 BLOCKED - layout coverage exists, but the review action, audit visibility, and approval safeguards do not fully match FR-016 Screen 8

---

## Summary Dashboard

| # | Flow | Module | Screens Required | Screens Verified | Layout Status | Field Coverage |
|---|------|--------|-----------------|-----------------|---------------|----------------|
| S8 | Patient Deletion Requests List (GDPR) | A-01: Patient Management & Oversight | 1 | 1 | 🔴 FAIL | ~75% |

**Overall**: 1 of 1 scoped units verified. The screen is visually designed, but the current layouts remain blocked by critical action/compliance gaps.
**Screens**: 1 of 1 specified screens have layouts (100% layout coverage).

---

## Layout File Inventory

### Mapped to Spec Flows

| Layout File | Maps to Flow | Maps to Screen |
|-------------|-------------|----------------|
| `layout-temp/Fulltable overview.jpg` | S8 scope | Screen 8 (Patient Deletion Requests List (GDPR)) |
| `layout-temp/Filter.jpg` | S8 scope | Screen 8 (Filter/search controls) |
| `layout-temp/Patient Deletion Requests Detailed/Status_ Pending Admin Review.jpg` | S8 scope | Screen 8 (Review modal / pending state) |
| `layout-temp/Patient Deletion Requests Detailed/Status_ Approved.jpg` | S8 scope | Screen 8 (Approved state / post-review variant) |

### Unmapped Files

| Layout File | Likely Purpose | Notes |
|-------------|---------------|-------|
| `layout-temp/Patients.jpg` | Patient list screen | Outside Screen 8 scope; likely maps to FR-016 Screen 1 |

---

## Detailed Verification by Flow

---

### Flow S8: Screen 8 Verification Scope

**Status**: 🔴 BLOCKED - the queue and modal are designed, but the review trigger, audit access, and destructive-action safeguards are not fully represented
**Screens required**: 1
**Layout files**: `layout-temp/Fulltable overview.jpg`, `layout-temp/Filter.jpg`, `layout-temp/Patient Deletion Requests Detailed/Status_ Pending Admin Review.jpg`, `layout-temp/Patient Deletion Requests Detailed/Status_ Approved.jpg`

#### Screen 8: Patient Deletion Requests List (GDPR)

**Layout**: `layout-temp/Fulltable overview.jpg`, `layout-temp/Filter.jpg`, `layout-temp/Patient Deletion Requests Detailed/Status_ Pending Admin Review.jpg`, `layout-temp/Patient Deletion Requests Detailed/Status_ Approved.jpg`

##### Flow Context

- **User arrives from**: After a patient submits a GDPR deletion request, admin opens `User management -> Patients -> Deletion Requests` per FR-016 User Story 6 acceptance step 1.
- **Screen purpose**: Show the pending deletion queue, let admin inspect request details, contact the patient if needed, then approve or deny.
- **Entry point**: Present. `Status_ Pending Admin Review.jpg` and `Status_ Approved.jpg` show breadcrumb `User Management / Patients` and active `Patient Deletion Requests` tab, matching the spec path.
- **Exit path**: Partial. The modal shows `Approve`, `Deny`, and `Close`, but the table itself exposes only an overflow/kebab icon rather than the explicit `Review` primary action required by the spec row `Table Column: Actions`.
- **Data continuity**: Correct. The selected row's patient name, email, patient ID, submitted date, SLA date, reason, and current status are carried into the modal detail view.
- **Flow context issues**:
  - No visible audit-trail jump for the selected request, even though the spec requires an audit trail link.
  - No visible blocked-approval state for "active obligations" from User Story 6 acceptance step 4.
  - No visible enhanced confirmation step or required justification cue for approve/deny actions.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Screen Title | Yes | ✅ | `Status_ Pending Admin Review.jpg` and `Status_ Approved.jpg` show active `Patient Deletion Requests` under `User Management / Patients`, which is functionally equivalent to the spec row `Screen Title` (`Deletion Requests` under `User management -> Patients`). |
| Search | No | ✅ | Search box is visible at the top-right of the page in both modal screenshots, matching the spec row `Search`. Static layouts do not prove debounce or email-search behavior. |
| Filters | No | ✅ | `Filter.jpg` shows filter controls for `Patient ID`, `Patient Name`, and `Current Status` with `Reset` and `Apply filter`, which satisfies the generic `Filters` group requirement at static-layout level. |
| Deletion Requests Table | Yes | ✅ | Queue table is clearly visible in `Fulltable overview.jpg` and behind the modal in both detail-state images. |
| Table Column: Patient ID | Yes | ✅ | `Patient ID` is visible as the first table column in `Fulltable overview.jpg`, and also appears inside the modal detail rows. |
| Table Column: Patient Name | Yes | ✅ | Patient names are visible in the table and repeated in the modal summary (`Aylin Kaya`, etc.), matching the spec row `Table Column: Patient Name`. |
| Table Column: Patient Email | Yes | ⚠️ | Email is visible under the patient name in the table rows and modal summary, but not as a dedicated standalone table column as specified. Evidence: `Fulltable overview.jpg`, both detail screenshots. |
| Table Column: Submitted At | Yes | ✅ | `Submitted At` column is visible in `Fulltable overview.jpg`, and the same value is shown in modal request details. |
| Table Column: Reason (Optional) | No | ✅ | `Reason` is visible in the table and in modal request details (`Too many notifications or emails`, etc.), matching the optional spec row. |
| Table Column: SLA Due By | Yes | ✅ | `SLA Due By` appears in the table and modal details in all relevant layouts. |
| Table Column: Actions | Yes | ❌⚠️ | The table shows an overflow/kebab icon, not a visible `Review` primary action as required by the spec row `Table Column: Actions`. Evidence: `Fulltable overview.jpg`, both detail screenshots. |
| Empty State | Conditional | ✅ | Only populated states were provided. Under the pass/fail rules, absence of the empty state is acceptable when the non-empty state is what is shown. |
| Review / Approve Modal | Conditional | ✅ | Both `Status_ Pending Admin Review.jpg` and `Status_ Approved.jpg` show the review modal open, satisfying the conditional modal state. |
| Modal: Patient Summary | Yes | ✅ | The modal header area shows patient avatar, name, and email; the related patient ID is immediately visible in the detail rows below, covering the summary information from the spec. |
| Modal: Request Details | Yes | ✅ | `Submitted At`, `SLA Due By`, and `Reason` are all visible in the modal details section. |
| Modal: Contact Options | Yes | ✅ | Phone and email action buttons are visible as icon controls in the modal header area in both modal layouts. |
| Modal: Admin Notes | No | ✅ | `Admin Notes` textarea is visible in both modal states. |
| Modal: Approve Button | Conditional | ❌⚠️ | `Approve` is visible in `Status_ Pending Admin Review.jpg`, but the layout does not show the spec-required enhanced confirmation and does not visibly require justification; only an optional `Admin Notes` field is shown. |
| Modal: Deny Button | Conditional | ❌⚠️ | `Deny` is visible in `Status_ Pending Admin Review.jpg`, but the layout does not visibly indicate the spec-required justification requirement before denial. |
| Modal: Close Button | Yes | ✅ | `Close` is clearly visible in both modal states. |
| Audit Trail Link | Yes | ❌ | No audit trail link is visible in the table, modal, or surrounding page chrome in any provided Screen 8 layout, despite the spec row `Audit Trail Link`. |

**Extra Elements**:

- `Current Status` table column and modal status row are visible in `Fulltable overview.jpg` and both modal screenshots, but `Current Status` is not listed as a Screen 8 field row in the FR data fields table. This appears intentional and useful.
- Pagination / item-count controls (`Total 85 items`, page numbers, `10/page`) are visible at the bottom of the modal screenshots, but pagination is not listed in the Screen 8 spec.

**Screen Status**: 🔴 FAIL
**Field Coverage**: 12/16 (75%)
**Critical Issues**:

- Spec-required `Review` primary action is not visibly present in the table; only an overflow icon is shown.
- No visible audit trail link for the request.
- Approve/Deny flows do not visibly enforce the required justification / enhanced confirmation safeguards for a deletion request.

##### UX/UI Design Evaluation

**Skills invoked**: ui-ux-pro-max, web-design-guidelines

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-17` CTA label clarity: the queue's review entry point is not explicit. `Fulltable overview.jpg` and both modal screenshots show only a kebab/overflow icon in the `Action` column, while the FR expects a visible `Review` action. | Replace the overflow-only trigger with a labeled `Review` button or clearly labeled inline action so admins can identify the next step immediately. |
| 🔴 Critical UX | `U-18` Destructive action safeguard: `Status_ Pending Admin Review.jpg` shows `Approve` as a direct green primary CTA next to `Deny`, with no visible secondary confirmation step and no visible required justification control, despite a high-impact deletion approval flow. | Introduce a mandatory confirmation layer and explicit required justification before approval. Visually separate the destructive approval path from low-risk actions. |
| ⚠️ UX Improvement | `U-11` Label clarity / `W-05` form layout: the only writable field in the modal is `Admin Notes`, but the FR requires justification for approve/deny. The current layout does not tell the admin whether notes are optional, required, or reused as justification. Evidence: `Status_ Pending Admin Review.jpg`. | Rename or annotate the field to reflect its role (`Required justification` when approving/denying), and show required-state guidance near the action buttons. |
| 💡 UX Suggestion | `W-06` Table design: patient email is embedded inside the `Patient Name` cell rather than occupying its own explicit column, which reduces scanability against the FR's separate `Patient Email` field row. Evidence: `Fulltable overview.jpg`. | Either split email into its own visible column or align the FR spec to the intended stacked-name/email table pattern. |

**Flow Coverage Gaps**:

- No empty-state layout was provided for the spec row `Empty State` (`No pending deletion requests`).
- No explicit blocked-approval layout was provided for the business rule that approval must be blocked when active obligations exist.
- No separate enhanced-confirmation state was provided for approve/deny actions, even though the FR requires those safeguards.

---

## Action Items

| Priority | Flow | Screen | Issue | Recommendation |
|----------|------|--------|-------|----------------|
| 🔴 Critical | S8 | Screen 8 | Queue row action does not expose the spec-required `Review` CTA; only an overflow icon is shown. | Make `Review` a visible action in the table row, or update the FR if overflow-menu review is the intended pattern. |
| 🔴 Critical | S8 | Screen 8 | Approval flow does not visibly enforce enhanced confirmation + required justification for deletion approval. | Add a required justification step and a separate confirmation state before final approval. |
| ⚠️ Important | S8 | Screen 8 | Denial flow does not visibly indicate required justification. | Convert `Admin Notes` into an explicit required justification field for deny, or add a dedicated required justification control. |
| ⚠️ Important | S8 | Screen 8 | Spec-required `Audit Trail Link` is absent from all provided layouts. | Surface a visible audit-trail link or button from the row or modal, pointing to Screen 7 filtered by request ID. |
| 💡 Suggestion | S8 | Screen 8 | Table shows `Current Status` and pagination as design additions, while `Patient Email` is visually merged under the name cell. | Reconcile the FR and layout so the data table structure is explicit and consistent. |

### Priority Legend

- **🔴 Critical**: Blocks flow progression, breaks data integrity, or causes security/legal risk. Must fix before development.
- **🔴 Critical UX**: Severe usability issue that would prevent users from completing the flow or cause significant confusion. Must fix before development.
- **⚠️ Important**: Functional discrepancy that could cause user confusion or require rework during development. Should fix before development.
- **⚠️ UX Improvement**: Usability or design quality issue that deviates from platform conventions or best practices. Should fix before development.
- **💡 Suggestion**: Cosmetic or minor improvement. Can fix anytime.
- **💡 UX Suggestion**: Minor design enhancement that would improve polish. Can fix anytime.

---

## Notes

- Source FR: `local-docs/project-requirements/functional-requirements/fr016-admin-patient-mgmt/prd.md`
- Scope limited to FR-016 Screen 8 based on user request
- Visual evidence used: `layout-temp/Fulltable overview.jpg`, `layout-temp/Filter.jpg`, `layout-temp/Patient Deletion Requests Detailed/Status_ Pending Admin Review.jpg`, `layout-temp/Patient Deletion Requests Detailed/Status_ Approved.jpg`
- `layout-temp/Patients.jpg` was cataloged as outside this screen scope and not evaluated
- UX/UI review applied local Screen 8 evidence against the skill's required rule set for Admin Web (Universal + Web checks)
