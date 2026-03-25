# Design Layout Verification Report — FR-032

**Report Date**: 2026-03-23
**Report Type**: Design Layout Verification
**FR Scope**: FR-032 — Provider Dashboard Settings & Profile Management
**Flow Scope**: Specific screens: Screen 5.7, Screen 5.8, Screen 5.9 within Main Flow: View and Reply to Support Cases (Two-Way Communication)
**Layout Source**: `layout-temp/`
**Platform**: Provider Web
**Status**: 🟡 PARTIAL

---

## Summary Dashboard

| # | Flow | Module | Screens Required | Screens Verified | Layout Status | Field Coverage |
|---|------|--------|-----------------|-----------------|---------------|----------------|
| 5 | View and Reply to Support Cases (Two-Way Communication) | PR-06: Profile & Settings Management | 3 | 3 | 🟡 PARTIAL | ~83% |

**Overall**: 1 of 1 flows verified. The flow is **PARTIAL** because all three target screens exist, but each contains at least one spec discrepancy that should be corrected before development.
**Screens**: 3 of 3 specified screens have layouts (~100% layout coverage).

---

## Layout File Inventory

### Mapped to Spec Flows

| Layout File | Maps to Flow | Maps to Screen |
|-------------|-------------|----------------|
| `layout-temp/My Support Cases.jpg` | 5 | 5.7 (My Support Cases List) |
| `layout-temp/Filter.jpg` | 5 | 5.7 (My Support Cases List, filter state) |
| `layout-temp/Fulltable overview.jpg` | 5 | 5.7 (My Support Cases List, table state) |
| `layout-temp/Support Case Detail > Open.jpg` | 5 | 5.8 (Support Case Detail View) |
| `layout-temp/Support Case Detail_ Closed.jpg` | 5 | 5.8 (Support Case Detail View, closed state) |
| `layout-temp/Reopen Case Request.jpg` | 5 | 5.9 (Reopen Case Request Modal) |

### Unmapped Files

| Layout File | Likely Purpose | Notes |
|-------------|---------------|-------|
| `layout-temp/Contact Support.jpg` | Screen 5.5 | Outside current scope |
| `layout-temp/FAQ’s.jpg` | Screen 5.1 | Outside current scope |
| `layout-temp/Feedback & Suggestions.jpg` | Screen 5.6 | Outside current scope |
| `layout-temp/Help Centre.jpg` | Screen 5 home | Outside current scope |
| `layout-temp/Major Outage.jpg` | Screen 5.10 state | Outside current scope |
| `layout-temp/Partial Outage.jpg` | Screen 5.10 state | Outside current scope |
| `layout-temp/Resource Library.jpg` | Screen 5.3 | Outside current scope |
| `layout-temp/Service Status.jpg` | Screen 5.10 | Outside current scope |
| `layout-temp/Tutorial Guides, Troubleshooting Tips, Policy Information - Detail.jpg` | Screen 5.2 detail state | Outside current scope |
| `layout-temp/Tutorial Guides, Troubleshooting Tips, Policy Information.jpg` | Screen 5.2 | Outside current scope |
| `layout-temp/Video Tutorials.jpg` | Screen 5.4 | Outside current scope |

---

## Detailed Verification by Flow

---

### Flow 5: View and Reply to Support Cases (Two-Way Communication)

**Status**: 🟡 PARTIAL — All three in-scope screens are designed, but the current layouts still diverge from FR-032 on default-state behavior, explicit attachment flow, full datetime display, and reopen-modal defaults.
**Screens required**: 3
**Layout files**: `layout-temp/My Support Cases.jpg`, `layout-temp/Filter.jpg`, `layout-temp/Fulltable overview.jpg`, `layout-temp/Support Case Detail > Open.jpg`, `layout-temp/Support Case Detail_ Closed.jpg`, `layout-temp/Reopen Case Request.jpg`

#### Screen 5.7: My Support Cases List

**Layout**: `layout-temp/My Support Cases.jpg`, `layout-temp/Filter.jpg`, `layout-temp/Fulltable overview.jpg`

##### Flow Context

- **User arrives from**: Help Centre category navigation after the provider selects "My Support Cases" in the flow step 2; supported by breadcrumb `Settings & Support / Help Centre / My Support Cases List` in `layout-temp/My Support Cases.jpg`.
- **Screen purpose**: List all submitted support requests and feedback so the provider can filter, search, review unread replies, and open a case detail view; sourced from FR-032 `#### Screen 5.7: My Support Cases List`.
- **Entry point**: Present. The breadcrumb, page title, and Help Centre highlight in `layout-temp/My Support Cases.jpg` align with the flow trigger and entry from Help Centre.
- **Exit path**: Present. `Case ID` values are rendered as clickable blue links in `layout-temp/My Support Cases.jpg` and `layout-temp/Fulltable overview.jpg`, matching the business rule that case row or Case ID opens Screen 5.8.
- **Data continuity**: Partial. Case identifiers, type, status, dates, feedback resolution, and unread counts are shown, but the visible default dataset includes `Closed` and `Resolved` cases and a `Dec 12, 2024` record, which conflicts with the default-view rule for only `Open` and `In Progress` cases from the last 90 days.
- **Flow context issues**: The provided default-state layout does not evidence the required default filter behavior from the FR.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Filter Bar | No | ✅ | Present in `layout-temp/Filter.jpg` with `Status`, `Type`, and `Date Range` controls plus `Reset` and `Apply filter`; matches FR-032 Screen 5.7 `Filter Bar` field group. |
| Search Bar | No | ✅ | Present at the top of `layout-temp/My Support Cases.jpg` with search icon; aligns with FR-032 Screen 5.7 `Search Bar`. |
| Quick Stats Bar | N/A | ✅ | Four summary cards are visible in `layout-temp/My Support Cases.jpg` for `Open Cases`, `In Progress`, `Resolved`, and `Unread Messages`, matching the FR metrics group. |
| Case List Table | N/A | ❌⚠️ | Table is present, but the shown default state in `layout-temp/My Support Cases.jpg` and `layout-temp/Fulltable overview.jpg` includes `Resolved` and `Closed` rows and an older `Dec 12, 2024` item, contradicting the FR business rule that the default view shows only `Open` and `In Progress` cases from the last 90 days. |
| Table Column 1: Case ID | N/A | ✅ | Visible as linked IDs such as `CASE-2025-12345` in `layout-temp/My Support Cases.jpg` and `layout-temp/Fulltable overview.jpg`; matches FR-032 Screen 5.7 column 1. |
| Table Column 2: Title | N/A | ✅ | Visible as `Case Title` with row values in `layout-temp/Fulltable overview.jpg`; matches FR-032 Screen 5.7 column 2. |
| Table Column 3: Type | N/A | ⚠️ | Present in `layout-temp/Fulltable overview.jpg`, but rendered as colored text labels (`Support Request`, `Feedback`) rather than distinct badges as specified in FR-032 Screen 5.7 column 3. |
| Table Column 4: Status | N/A | ✅ | Present as color-coded badges (`Open`, `In Progress`, `Closed`, `Resolved`) in `layout-temp/My Support Cases.jpg` and `layout-temp/Fulltable overview.jpg`; aligns with FR-032 Screen 5.7 column 4. |
| Table Column 5: Feedback Resolution | No | ✅ | Present for feedback rows with `Implemented`, `Planned`, `Under Review`, and `Declined` badges in `layout-temp/Fulltable overview.jpg`; aligns with FR-032 Screen 5.7 column 5. |
| Table Column 6: Submitted Date | N/A | ✅ | Present in both case-list images with date values like `Sep 25, 2025`; aligns with FR-032 Screen 5.7 column 6. |
| Table Column 7: Last Updated | N/A | ✅ | Present in both case-list images with date values like `Sep 25, 2025`; aligns with FR-032 Screen 5.7 column 7. |
| Table Column 8: Unread | No | ⚠️ | Present as numeric values in the `Unread` column in `layout-temp/My Support Cases.jpg` and `layout-temp/Fulltable overview.jpg`, but the provided design does not show the explicit badge/icon treatment or `2 new` style called for in FR-032 Screen 5.7 column 8. |
| Pagination Controls | N/A | ✅ | Pagination is visible at the bottom of `layout-temp/My Support Cases.jpg` with page numbers and page-size selector, matching FR-032 Screen 5.7 `Pagination Controls`. |

**Extra Elements**:

- Leading row-selection checkboxes appear in `layout-temp/My Support Cases.jpg` and `layout-temp/Fulltable overview.jpg` with no matching spec entry or visible bulk action.
- A `Category` column appears in both case-list layouts, but FR-032 Screen 5.7 specifies an 8-column table without `Category`.

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 12/13 (92%)
**Critical Issues**: Default table state does not match the required default filter behavior for `Open` + `In Progress` cases from the last 90 days.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `W-06` Table clarity issue: `layout-temp/My Support Cases.jpg` shows the frozen `Case ID` column visually overlapping the adjacent title area, which obscures headers and row content and weakens scanability for the main list view. | Reduce the sticky-column overlay, add a clear divider/shadow treatment, or widen the first two columns so `Case Title` remains legible in the default view. |
| ⚠️ UX Improvement | `W-06` / `U-16` The list includes row-selection checkboxes in `layout-temp/My Support Cases.jpg` and `layout-temp/Fulltable overview.jpg`, but there is no visible bulk action or explanation of what selecting rows does, which introduces unnecessary ambiguity. | Remove the checkbox column unless bulk actions are planned for this screen, or add a clear bulk-actions toolbar and header state to justify selection. |

#### Screen 5.8: Support Case Detail View

**Layout**: `layout-temp/Support Case Detail > Open.jpg`, `layout-temp/Support Case Detail_ Closed.jpg`

##### Flow Context

- **User arrives from**: Screen 5.7 after the provider clicks a case row or Case ID; supported by the breadcrumb path and by linked Case IDs on the prior screen.
- **Screen purpose**: Show complete case information, full conversation history, timeline, and the context-specific action to reply or request reopen; sourced from FR-032 `#### Screen 5.8: Support Case Detail View`.
- **Entry point**: Present. Both layouts keep the Help Centre breadcrumb trail and page title `Support Case Detail`, which supports the transition from Screen 5.7.
- **Exit path**: Present. `Back to List` is visible in both `layout-temp/Support Case Detail > Open.jpg` and `layout-temp/Support Case Detail_ Closed.jpg`, and the closed-state action includes `Request Reopen Case`.
- **Data continuity**: Mostly correct. Case metadata, description, conversation thread, and timeline are all carried into the detail view, but the date fields omit the required time component and the reply composer does not show a distinct `Attach Files` control.
- **Flow context issues**: The detail screen is structurally correct, but two spec-critical interaction details are weakened in the provided layouts: full datetime display and a clear file-attachment affordance for replies.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Case ID | N/A | ✅ | Visible beneath the page title in both detail states as `CASE-2025-12345`, matching FR-032 Screen 5.8 `Case ID`. |
| Case Title | N/A | ✅ | Present in the left metadata panel in both detail layouts, matching FR-032 Screen 5.8 `Case Title`. |
| Status Badge | N/A | ✅ | Present beside the case ID in both detail states (`Open` in `Support Case Detail > Open.jpg`, `Closed` in `Support Case Detail_ Closed.jpg`), matching FR-032 Screen 5.8 `Status Badge`. |
| Feedback Resolution Badge | No | ⚠️ | Present as `Under Review` in the metadata panel, but the provided layout reads more like plain text than a distinct badge/chip as specified in FR-032 Screen 5.8 `Feedback Resolution Badge`. |
| Case Type | N/A | ✅ | Present as `Feedback` in the metadata panel in both detail states, matching FR-032 Screen 5.8 `Case Type`. |
| Priority | N/A | ✅ | Present beside the case ID as `Urgent`, matching FR-032 Screen 5.8 `Priority`. |
| Submitted Date | N/A | ❌⚠️ | Present in both detail layouts, but shown only as `Sep 25, 2025` without time, which does not meet the FR-032 Screen 5.8 `datetime (readonly)` requirement. |
| Last Updated | N/A | ❌⚠️ | Present in both detail layouts, but shown only as `Sep 25, 2025` without time, which does not meet the FR-032 Screen 5.8 `datetime (readonly)` requirement. |
| Original Description | N/A | ✅ | Present in both detail layouts under `Description`, matching FR-032 Screen 5.8 `Original Description`. |
| Communication Thread | N/A | ✅ | Present in both detail layouts with sender names, role badges, timestamps, and message content, aligning with FR-032 Screen 5.8 `Communication Thread` and its structure notes. |
| Reply Message Box | No | ✅ | Present in `layout-temp/Support Case Detail > Open.jpg` as `Reply to Supporter` with an editor area; absent in the closed-state image, which aligns with the rule that reply is not enabled for closed cases. |
| Attach Files Button | No | ❌⚠️ | No dedicated `Attach Files` button is visible in `layout-temp/Support Case Detail > Open.jpg`; only a small paperclip icon appears in the editor toolbar, which is weaker than the explicit file-upload control required by FR-032 Screen 5.8. |
| Send Reply Button | N/A | ⚠️ | Present in `layout-temp/Support Case Detail > Open.jpg` as a green `Reply` button; functionally correct, but the label is less explicit than the FR-032 `Send Reply Button`. |
| Request Reopen Button | N/A | ✅ | Present only in `layout-temp/Support Case Detail_ Closed.jpg` as `Request Reopen Case`, correctly matching the conditional visibility rule in FR-032 Screen 5.8. |
| Case Timeline | N/A | ✅ | Present in both detail states as a right-side vertical timeline with events such as `Attachments`, `Assignments`, and `Case creation`, matching FR-032 Screen 5.8 `Case Timeline`. |
| Back to List Button | N/A | ✅ | Present in both detail states within the `Action` box, matching FR-032 Screen 5.8 `Back to List Button`. |

**Extra Elements**:

- `Ticket Source`, `Submitter Type`, `Category`, and `Tag` appear as extra metadata rows in both layouts with no matching FR-032 Screen 5.8 field entries.
- A standalone `Attachments` block appears above the communication thread in both layouts; this is not explicitly defined as a separate field in FR-032 Screen 5.8.

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 13/16 (81%)
**Critical Issues**: `Submitted Date` and `Last Updated` do not show full datetime values, and the reply composer lacks a clear dedicated `Attach Files` control.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-01` The primary reply action in `layout-temp/Support Case Detail > Open.jpg` is a small green button beneath a large metadata stack, so the main conversational task is not visually as prominent as the surrounding static content. | Increase the visual weight and placement of the reply composer and send action so replying reads as the primary task on open cases. |
| ⚠️ UX Improvement | `U-13` / `W-08` The timeline text in both detail layouts is extremely light and low-contrast relative to the white background, which makes event details hard to scan. | Increase contrast and spacing in the timeline so event names and timestamps remain readable without zooming. |

#### Screen 5.9: Reopen Case Request Modal

**Layout**: `layout-temp/Reopen Case Request.jpg`

##### Flow Context

- **User arrives from**: Screen 5.8 closed-case detail after the provider clicks `Request Reopen Case`; the dimmed background in `layout-temp/Reopen Case Request.jpg` clearly shows the modal launched from the closed-state detail view.
- **Screen purpose**: Capture the provider's reopen reason and optional priority change before sending the request back into the support flow; sourced from FR-032 `#### Screen 5.9: Reopen Case Request Modal`.
- **Entry point**: Present. The modal sits over the closed support-case detail view, which matches the FR rule that it is only accessible from Screen 5.8 when the case is closed.
- **Exit path**: Present. `Cancel` closes the modal without changes, and the green `Reopen Case` action provides the submit path.
- **Data continuity**: Partial. The modal carries prior context via resolution summary and closure date, but the closure field drops the required time component and the priority selector does not show the required default `Keep Current` state.
- **Flow context issues**: The modal structure is correct, but the provided design weakens two explicit spec details: full closure datetime and default priority behavior.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Previous Resolution Summary | N/A | ✅ | Present in `layout-temp/Reopen Case Request.jpg` as a text block beneath the modal title, matching FR-032 Screen 5.9 `Previous Resolution Summary`. |
| Previous Closure Date | N/A | ❌⚠️ | Present as `Sep 25, 2025`, but the FR-032 Screen 5.9 field requires a `datetime (readonly)` value and the time component is missing. |
| Reopening Reason | Yes | ✅ | Present as a textarea labeled `Reopening Reason` in `layout-temp/Reopen Case Request.jpg`, matching FR-032 Screen 5.9 `Reopening Reason`. |
| Priority Update | No | ❌⚠️ | Present as a dropdown, but labeled `New Priority` with placeholder `Select`; this does not evidence the FR-032 Screen 5.9 requirement that the default option be `Keep Current`. |
| Submit Reopen Request Button | Yes | ⚠️ | Present as a green `Reopen Case` button; functionally equivalent, but less explicit than the FR-032 `Submit Reopen Request Button` label. |
| Cancel Button | Yes | ✅ | Present as `Cancel` in the modal footer, matching FR-032 Screen 5.9 `Cancel Button`. |

**Extra Elements**:

- A close (`X`) icon appears outside the modal card in the dimmed backdrop area; this is a reasonable modal affordance but is not explicitly listed in FR-032 Screen 5.9.

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 4/6 (67%)
**Critical Issues**: `Previous Closure Date` omits time, and the priority selector does not show the required default `Keep Current` option/state.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-11` / `W-05` The priority field in `layout-temp/Reopen Case Request.jpg` is labeled `New Priority` with a generic `Select` placeholder, which obscures the intended default behavior and makes the field less self-explanatory than the FR wording. | Rename the field to `Priority Update` and prefill the dropdown with `Keep Current` so the optional nature and default state are explicit. |
| ⚠️ UX Improvement | `U-19` The modal does not surface the `min 20 / max 500` character guidance for the reopening reason, so users only learn validation rules after submission. | Add helper text and a live character counter below the textarea to make the validation constraints visible before submit. |

**Flow Coverage Gaps**:

- No dedicated layout is provided for the optional warning state noted in FR-032 Screen 5.9 (`This case was recently closed...`).
- No layout is provided for the suggested response-time guidance note (`Our team typically responds to reopen requests within 4 hours.`).

---

## Action Items

| Priority | Flow | Screen | Issue | Recommendation |
|----------|------|--------|-------|----------------|
| ⚠️ Important | 5 | 5.7 | Default case-list layout shows `Resolved` / `Closed` rows and an older-than-90-days record, which conflicts with the required default filter state. | Update the default screen state so it visibly loads only `Open` and `In Progress` cases from the last 90 days, sorted by `Last Updated` descending. |
| ⚠️ Important | 5 | 5.8 | Reply composer does not expose a clear dedicated `Attach Files` control. | Add an explicit attachment button/control near the reply box with the intended upload affordance and constraints. |
| ⚠️ Important | 5 | 5.8 | `Submitted Date` and `Last Updated` omit the required time component in the detail view. | Show full datetime values for both fields in the read-only metadata area. |
| ⚠️ Important | 5 | 5.9 | Priority selector does not show the required default `Keep Current` state. | Prefill the dropdown with `Keep Current` and align the label with the spec's `Priority Update`. |
| ⚠️ UX Improvement | 5 | 5.7 | Sticky first-column treatment reduces legibility of the adjacent title column. | Adjust the frozen-column layout so `Case Title` remains readable in the primary table view. |
| ⚠️ UX Improvement | 5 | 5.8 | Timeline content is too low-contrast for comfortable scanning. | Increase contrast and spacing in the timeline event list. |
| ⚠️ UX Improvement | 5 | 5.9 | Reopen modal does not expose the textarea validation guidance before submission. | Add helper copy and a live character counter for the reopen-reason field. |

### Priority Legend

- **🔴 Critical**: Blocks flow progression, breaks data integrity, or causes security/legal risk. Must fix before development.
- **🔴 Critical UX**: Severe usability issue that would prevent users from completing the flow or cause significant confusion. Must fix before development.
- **⚠️ Important**: Functional discrepancy that could cause user confusion or require rework during development. Should fix before development.
- **⚠️ UX Improvement**: Usability or design quality issue that deviates from platform conventions or best practices. Should fix before development.
- **💡 Suggestion**: Cosmetic or minor improvement. Can fix anytime.
- **💡 UX Suggestion**: Minor design enhancement that would improve polish. Can fix anytime.

---

## Notes

- Report seeded from `local-docs/project-automation/skills-engineering/verify-design-layout/assets/report-template.md`
- Requirement source: `local-docs/project-requirements/functional-requirements/fr032-provider-dashboard-settings/prd.md`
- Evidence reviewed from `layout-temp/My Support Cases.jpg`, `layout-temp/Filter.jpg`, `layout-temp/Fulltable overview.jpg`, `layout-temp/Support Case Detail > Open.jpg`, `layout-temp/Support Case Detail_ Closed.jpg`, and `layout-temp/Reopen Case Request.jpg`
- Findings were limited to Screen 5.7, Screen 5.8, and Screen 5.9 only; other Help Centre screens were cataloged but not evaluated
- This verification is based on static layout evidence only; interaction-only behaviors that were not visually represented were not assumed
