# Design Layout Verification Report — FR-032

**Report Date**: 2026-03-27
**Report Type**: Design Layout Verification
**FR Scope**: FR-032 — Provider Dashboard Settings & Profile Management
**Flow Scope**: Screen 5.7, Screen 5.8, Screen 5.9 within Main Flow: View and Reply to Support Cases (Two-Way Communication)
**Layout Source**: `layout-temp/`
**Platform**: Provider Web
**Status**: 🟡 PARTIAL

---

## Summary Dashboard

| # | Flow | Module | Screens Required | Screens Verified | Layout Status | Field Coverage |
|---|------|--------|-----------------|-----------------|---------------|----------------|
| Support Cases | View and Reply to Support Cases (Two-Way Communication) | PR-06: Profile & Settings Management | 3 | 3 | 🟡 PARTIAL | ~66% |

**Overall**: 1 of 1 flows verified. The support case flow is PARTIAL: all three screens have layouts, but each screen contains structural mismatches against the FR that should be corrected before development handoff.
**Screens**: 3 of 3 specified screens have layouts (100% layout coverage).

---

## Layout File Inventory

### Mapped to Spec Flows

| Layout File | Maps to Flow | Maps to Screen |
|-------------|-------------|----------------|
| `layout-temp/My Support Cases.jpg` | Support Cases | Screen 5.7 (My Support Cases List) |
| `layout-temp/Filter.jpg` | Support Cases | Screen 5.7 (My Support Cases List) — filter state |
| `layout-temp/Fulltable overview.jpg` | Support Cases | Screen 5.7 (My Support Cases List) — wide table overview state |
| `layout-temp/Support Case Detail/Open.jpg` | Support Cases | Screen 5.8 (Support Case Detail View) — open case state |
| `layout-temp/Support Case Detail_ Closed.jpg` | Support Cases | Screen 5.8 (Support Case Detail View) — closed case state |
| `layout-temp/Reopen Case Request.jpg` | Support Cases | Screen 5.9 (Reopen Case Request Modal) |

### Unmapped Files

| Layout File | Likely Purpose | Notes |
|-------------|---------------|-------|
| None | N/A | All relevant image files in `layout-temp/` map to the in-scope support case screens. Hidden file `.DS_Store` ignored. |

---

## Detailed Verification by Flow

---

### Flow Support Cases: View and Reply to Support Cases (Two-Way Communication)

**Status**: 🟡 PARTIAL — all required screens exist, but the implemented layouts diverge from the spec in table structure, field treatments, and closed/reopen state behavior
**Screens required**: 3
**Layout files**: `layout-temp/My Support Cases.jpg`, `layout-temp/Filter.jpg`, `layout-temp/Fulltable overview.jpg`, `layout-temp/Support Case Detail/Open.jpg`, `layout-temp/Support Case Detail_ Closed.jpg`, `layout-temp/Reopen Case Request.jpg`

#### Screen 5.7: My Support Cases List

**Layout**: `layout-temp/My Support Cases.jpg`, `layout-temp/Filter.jpg`, `layout-temp/Fulltable overview.jpg`

##### Flow Context

- **User arrives from**: Help Centre category navigation after selecting "My Support Cases"
- **Screen purpose**: View submitted support cases and feedback, filter/search them, and open a case for detail and reply actions
- **Entry point**: Present — breadcrumb `Settings & Support / Help Centre / My Support Cases List` and Help Centre navigation context are visible in `layout-temp/My Support Cases.jpg`
- **Exit path**: Present — Case IDs are styled as blue links and the list is clearly positioned as the source screen for the detail view in `layout-temp/My Support Cases.jpg`
- **Data continuity**: Issues — support requests and feedback are both represented, but the main list view swaps in an unlisted `Category` column and date-only values where the spec requires datetimes
- **Flow context issues**: No blocking flow gap visible from the provided layouts; the main discrepancies are data presentation and table structure

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Filter Bar | No | ✅ | Present across `layout-temp/My Support Cases.jpg` and `layout-temp/Filter.jpg`; includes Status, Type, Date Range, Reset, and Apply filter actions |
| Search Bar | No | ✅ | Search input is visible above the table in `layout-temp/My Support Cases.jpg` |
| Quick Stats Bar | N/A | ✅ | Four summary cards are present: Open Cases, In Progress, Resolved, Unread Messages |
| Case List Table | N/A | ✅ | Main list/table is present in both `layout-temp/My Support Cases.jpg` and `layout-temp/Fulltable overview.jpg` |
| Table Column 1: Case ID | N/A | ✅ | CASE identifier column is present and styled as clickable links |
| Table Column 2: Title | N/A | ✅ | Case title column is visible in `layout-temp/Fulltable overview.jpg`; partially obscured in the main screen capture |
| Table Column 3: Type | N/A | ❌⚠️ | Value is present, but rendered as plain colored text (`Support Request` / `Feedback`) instead of the specified badge treatment |
| Table Column 4: Status | N/A | ✅ | Color-coded status badges are present for Open, In Progress, Closed, and Resolved |
| Table Column 5: Feedback Resolution | No | ✅ | Resolution badges are visible for feedback rows: Implemented, Planned, Under Review, Declined |
| Table Column 6: Submitted Date | N/A | ❌⚠️ | Column is present, but rows show date only (`Sep 25, 2025`) rather than the specified datetime value |
| Table Column 7: Last Updated | N/A | ❌⚠️ | Column is present, but rows show date only rather than the specified datetime value |
| Table Column 8: Unread | No | ✅ | Unread count column is present with numeric values or empty state dashes |
| Pagination Controls | N/A | ❌⚠️ | Pagination exists, but the control shows `10/page` while the spec requires 20 cases per page by default |

**Extra Elements**:

- Checkbox selection column appears at the far left of the table, but no selection/bulk-action behavior is specified for Screen 5.7
- `Category` column appears between Feedback Resolution and Submitted Date in both table layouts, but it is not defined in the Screen 5.7 specification

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 9/13 specified fields fully matched (69%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `W-06` / `W-08`: The primary table view is too dense and structurally unstable. In `layout-temp/My Support Cases.jpg`, the title area is partially obscured while the rightmost `Unread` header is truncated, which makes the main scanning view harder to parse. | Reduce visible columns in the default viewport, or rebalance widths so all specified columns are readable without clipping in the default state. |
| ⚠️ UX Improvement | `U-03` / `W-06`: The table introduces an unlisted `Category` column and checkbox selection controls without corresponding actions, adding visual noise to a list whose primary task is search/filter/open. | Remove non-spec columns and bulk-selection affordances unless they support a documented user action in this flow. |

#### Screen 5.8: Support Case Detail View

**Layout**: `layout-temp/Support Case Detail/Open.jpg`, `layout-temp/Support Case Detail_ Closed.jpg`

##### Flow Context

- **User arrives from**: Clicking a case row or Case ID from Screen 5.7
- **Screen purpose**: Review full case details and communication history, reply to admin for open/in-progress cases, or request reopen for closed cases
- **Entry point**: Present — breadcrumb trail returns the user to `My Support Cases List`, aligning with the list-to-detail transition in `layout-temp/Support Case Detail/Open.jpg` and `layout-temp/Support Case Detail_ Closed.jpg`
- **Exit path**: Present — both states show `Back to List`, and the closed state also surfaces `Request ReOpen Case`
- **Data continuity**: Issues — core case identity data carries through, but the detail page introduces several non-spec metadata rows (`Ticket Source`, `Submitter Type`, `Category`, `Tag`) while omitting the specified disabled reply guidance for closed cases
- **Flow context issues**: Closed-state guidance is incomplete; the layout removes the reply composer instead of showing the specified disabled state message that tells the provider why they must request a reopen

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Case ID | N/A | ✅ | Case ID is visible in the header (`CASE-2025-12345`) |
| Case Title | N/A | ✅ | Title is shown in the detail summary panel |
| Status Badge | N/A | ✅ | Open/Closed status appears in the header as a colored badge |
| Feedback Resolution Badge | No | ❌⚠️ | `Under Review` is shown as plain text in the summary panel rather than a distinct badge treatment |
| Case Type | N/A | ✅ | Case type is displayed in the summary panel |
| Priority | N/A | ✅ | Priority is visible in the header as an `Urgent` badge |
| Submitted Date | N/A | ❌⚠️ | Date is present, but only as calendar date (`Sep 25, 2025`) instead of the specified datetime value |
| Last Updated | N/A | ❌⚠️ | Date is present, but only as calendar date instead of the specified datetime value |
| Original Description | N/A | ✅ | Description block is present below the summary information |
| Communication Thread | N/A | ✅ | Threaded conversation is visible with sender names, badges, timestamps, and message blocks |
| Reply Message Box | No | ❌⚠️ | Open state includes a reply composer, but the closed state removes it entirely instead of showing the specified disabled box/message |
| Attach Files Button | No | ❌⚠️ | No explicit `Attach Files` button is visible; only a small paperclip icon appears in the rich-text toolbar, which does not clearly meet the specified upload control |
| Send Reply Button | N/A | ✅ | Reply action button is visible in the open-state layout |
| Request Reopen Button | N/A | ✅ | Closed-state layout surfaces a prominent reopen action button |
| Case Timeline | N/A | ✅ | Timeline is present in a right-hand rail with multiple case events |
| Back to List Button | N/A | ✅ | Both states provide a `Back to List` action |

**Extra Elements**:

- Additional metadata rows appear that are not specified in FR-032 Screen 5.8: `Ticket Source`, `Submitter Type`, `Category`, and `Tag`
- Standalone `Attachments` section appears above the communication thread; this may be useful, but it is not defined as a separate screen field in the screen spec

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 10/16 specified fields fully matched (63%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-02` / `U-03` / `W-05`: The detail summary emphasizes internal/system metadata (`Ticket Source`, `Submitter Type`, `Category`, `Tag`) ahead of the conversation task, which weakens the screen’s focus on case status, description, and reply workflow. | Re-prioritize the summary panel around case state, dates, description, and conversation; move internal metadata to a secondary section or remove it if it is not part of the provider-facing requirement. |
| ⚠️ UX Improvement | `U-19` / `U-16`: The closed-state design removes the reply composer entirely instead of showing the specified disabled reply state with explanatory guidance, which makes the reason for the blocked action less clear. | Keep a disabled reply area with the required message (`This case is closed... Request Reopen`) so the restriction is explained in-context before the user takes the reopen action. |

#### Screen 5.9: Reopen Case Request Modal

**Layout**: `layout-temp/Reopen Case Request.jpg`

##### Flow Context

- **User arrives from**: Screen 5.8 closed-case detail after clicking "Request Reopen"
- **Screen purpose**: Collect reopening reason and optional priority escalation before reopening a closed case
- **Entry point**: Present — modal is shown on top of the closed case detail screen in `layout-temp/Reopen Case Request.jpg`
- **Exit path**: Present — modal exposes both `Cancel` and `Reopen Case` actions
- **Data continuity**: Mostly correct — previous resolution summary and prior closure date are carried into the modal for context
- **Flow context issues**: Priority control wording/default state do not match the spec's `Keep Current / Change to ...` model

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Previous Resolution Summary | N/A | ✅ | Summary block is visible near the top of the modal |
| Previous Closure Date | N/A | ❌⚠️ | Closure information is shown as date-only (`Sep 25, 2025`) rather than the specified datetime value |
| Reopening Reason | Yes | ✅ | Required textarea is present in the modal body |
| Priority Update | No | ❌⚠️ | Control is labeled `New Priority` with default `Select`; the spec requires a `Priority Update` control with explicit `Keep Current` as the default option |
| Submit Reopen Request Button | Yes | ✅ | Primary CTA is present as `Reopen Case`; wording is functionally equivalent to submit reopen request |
| Cancel Button | Yes | ✅ | Secondary dismiss action is present |

**Extra Elements**:

- Close (`X`) icon appears in the modal chrome in addition to the explicit `Cancel` button

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 4/6 specified fields fully matched (67%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-11` / `W-05`: The priority control is less explicit than the spec. `New Priority` + `Select` does not communicate that keeping the current priority is the safe default path. | Rename the field to match the requirement intent (`Priority Update`) and make `Keep Current` the visible default option in the dropdown. |

**Flow Coverage Gaps**:

- No layout was provided for the post-submit confirmation state that should return the user to Screen 5.8 with status updated to `Open`
- No static evidence was provided for the closed-case disabled reply message required on Screen 5.8 before the reopen action is triggered

---

## Action Items

| Priority | Flow | Screen | Issue | Recommendation |
|----------|------|--------|-------|----------------|
| ⚠️ Important | Support Cases | Screen 5.8 | Closed-case detail view removes the reply composer entirely instead of showing the specified disabled reply state and explanatory message. | Keep a disabled reply box/message visible in the closed state so the reopen path is explained in context before the user clicks reopen. |
| ⚠️ Important | Support Cases | Screen 5.7 | The list view adds unlisted checkbox/category columns and makes the specified table harder to scan in the default viewport. | Remove non-spec columns or rebalance widths so the specified columns remain readable without clipping. |
| ⚠️ Important | Support Cases | Screen 5.7 | Type is rendered as plain text, list dates omit time, and pagination defaults to 10 per page instead of 20. | Align table cell treatments and defaults with the FR: badge styling for Type, datetime values, and 20 rows per page. |
| ⚠️ Important | Support Cases | Screen 5.9 | Priority control no longer communicates the `Keep Current` default path defined in the FR. | Rename the field to match the requirement intent and make `Keep Current` the visible default option. |
| 💡 Suggestion | Support Cases | Screen 5.8 | Provider-facing detail view gives too much prominence to internal metadata (`Ticket Source`, `Submitter Type`, `Category`, `Tag`). | Move internal metadata to a secondary section or remove it from the provider UI if it is not part of the approved requirement. |

### Priority Legend

- **🔴 Critical**: Blocks flow progression, breaks data integrity, or causes security/legal risk. Must fix before development.
- **🔴 Critical UX**: Severe usability issue that would prevent users from completing the flow or cause significant confusion. Must fix before development.
- **⚠️ Important**: Functional discrepancy that could cause user confusion or require rework during development. Should fix before development.
- **⚠️ UX Improvement**: Usability or design quality issue that deviates from platform conventions or best practices. Should fix before development.
- **💡 Suggestion**: Cosmetic or minor improvement. Can fix anytime.
- **💡 UX Suggestion**: Minor design enhancement that would improve polish. Can fix anytime.

---

## Notes

- Source FR document: `local-docs/project-requirements/functional-requirements/fr032-provider-dashboard-settings/prd.md`
- Verification scope limited to Screen 5.7, Screen 5.8, and Screen 5.9
- Layout files evaluated from `layout-temp/`
- UX/UI evaluation applied Provider Web checks from `verify-design-layout/references/ux-ui-evaluation-rules.md` with supporting review from `ui-ux-pro-max` and current Vercel web interface guidelines
- No update log entry created because this verification covers a limited subset of one flow rather than a full FR or multi-flow verification
