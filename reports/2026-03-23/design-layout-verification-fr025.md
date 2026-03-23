# Design Layout Verification Report — FR-025

**Report Date**: 2026-03-23
**Report Type**: Design Layout Verification
**FR Scope**: FR-025 — Medical Questionnaire Management
**Flow Scope**: All admin-dashboard flows and screens defined in FR-025
**Layout Source**: `layout-temp/`
**Platform**: Admin Web
**Status**: 🔴 BLOCKED

---

## Summary Dashboard

| # | Flow | Module | Screens Required | Screens Verified | Layout Status | Field Coverage |
|---|------|--------|-----------------|-----------------|---------------|----------------|
| 1 | Workflow 1: Questionnaire Set Management | A-09: System Settings & Configuration | 7 | 7 | 🔴 BLOCKED | ~50% |
| 2 | Workflow 2: Severity Management | A-09: System Settings & Configuration | 1 | 1 | 🔴 BLOCKED | ~33% |
| 3 | Workflow 3: Questionnaire Deployment | A-09: System Settings & Configuration | 0 | 0 | 🟢 COMPLETE | n/a |
| 4 | Workflow 4: Inquiry Activation & Downstream Assignment | A-09: System Settings & Configuration | 1 | 1 | 🔴 BLOCKED | 0% |

**Overall**: 4 of 4 flows verified. 3 of 4 flows are 🔴 BLOCKED because key admin screens are missing or diverge materially from the FR.
**Screens**: 5 of 7 unique admin screen specs have some layout coverage (~71%). Screen 1 and Screen 5 have no dedicated design.

---

## Layout File Inventory

### Mapped to Spec Flows

| Layout File | Maps to Flow | Maps to Screen |
|-------------|-------------|----------------|
| `layout-temp/Questionnaire.jpg` | Workflow 1 | Screen 2 (Questionnaire Set Details) |
| `layout-temp/Fulltable.jpg` | Workflow 1 | Screen 2 (Questionnaire Set Details) |
| `layout-temp/Filter.jpg` | Workflow 1 | Screen 2 (Questionnaire Set Details) |
| `layout-temp/Question Editor.jpg` | Workflow 1 / Workflow 2 | Screen 3 (Question Editor) |
| `layout-temp/Categories.jpg` | Workflow 1 | Screen 4 (Category Management) |
| `layout-temp/Add/Edit Category.jpg` | Workflow 1 | Screen 4 (Category Management) |
| `layout-temp/Preview all.jpg` | Workflow 1 | Screen 6 (Questionnaire Preview) |
| `layout-temp/Version History & Audit Trail.jpg` | Workflow 1 | Screen 7 (Version History & Audit Trail) |

### Unmapped Files

| Layout File | Likely Purpose | Notes |
|-------------|---------------|-------|
| `layout-temp/.DS_Store` | macOS metadata | Ignore |

---

## Detailed Verification by Flow

---

### Flow 1: Questionnaire Set Management (Primary Flow)

**Status**: 🔴 BLOCKED — two required admin screens have no dedicated design, and the supplied "Questionnaire" layouts implement a question-level tabbed UI rather than the FR's questionnaire-set catalog and full set-details screen.
**Screens required**: 7
**Layout files**: `Questionnaire.jpg`, `Fulltable.jpg`, `Filter.jpg`, `Question Editor.jpg`, `Categories.jpg`, `Add/Edit Category.jpg`, `Preview all.jpg`, `Version History & Audit Trail.jpg`

#### Screen 1: Questionnaire Catalog

**Layout**: `{no dedicated layout file mapped}`

##### Flow Context

- **User arrives from**: Admin Settings → Questionnaire module entry
- **Screen purpose**: Browse questionnaire sets, inspect assignment/use, and open one set for editing or activation
- **Entry point**: Missing dedicated questionnaire-set catalog layout; provided files jump straight into a question-level tabbed module
- **Exit path**: Missing; no evidence of clicking a set name to open a set-details screen
- **Data continuity**: Issues; the supplied layouts show question rows and category tabs, not set-level records or inquiry designation state
- **Flow context issues**: No evidence of the FR's primary list of questionnaire sets, no visible set-level activation path, and no warning banner for unconfigured inquiry flow

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Set Name | Yes | ❌ | Required per Screen 1 spec row; no layout in `layout-temp/` shows questionnaire-set names as the primary list entity |
| Context Type | Yes | ❌ | No dedicated catalog layout mapped; provided tabbed list is question-level, not set-level |
| Question Count | No | ❌ | No mapped catalog view shows per-set question totals |
| Status | Yes | ❌ | No mapped catalog view shows per-set Draft / Active / Archived status |
| Version | No | ❌ | No mapped catalog view shows version column for questionnaire sets |
| Used In | No | ❌ | No mapped catalog view shows inquiry-flow / milestone assignment usage |
| Last Modified | No | ❌ | No mapped set catalog layout to verify against spec row |
| Created By | No | ❌ | No mapped set catalog layout to verify against spec row |
| Inquiry Active | No | ❌ | No badge or indicator showing "Active for Inquiry" for a questionnaire set |
| Search/Filters | No | ❌ | No mapped set-catalog search/filter layout; supplied `Filter.jpg` belongs to question-level list controls |
| Actions | — | ❌ | No evidence of View/Edit, Duplicate, Archive, Delete, or "Set as Active for Inquiry" at set level |

**Extra Elements**:

- None on a dedicated Screen 1 layout because no dedicated Screen 1 layout was provided

**Screen Status**: ⬜ NO DESIGN
**Field Coverage**: 0/3 (0%)
**Critical Issues**: Missing primary questionnaire-set catalog layout; no evidence of set-level navigation or inquiry activation controls

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| 🔴 Critical UX | The core entry screen for managing questionnaire sets is absent, so admins have no clear way to discover, compare, or activate sets as described in the FR. | Add a dedicated questionnaire-set catalog screen before detailed question-management tabs. |
| ⚠️ UX Improvement | The current layouts collapse multiple concerns into tabbed subpages without showing the parent set context. | Introduce a persistent set header with name, status, version, and usage summary before any child tabs. |

#### Screen 2: Questionnaire Set Details

**Layout**: `layout-temp/Questionnaire.jpg`, `layout-temp/Fulltable.jpg`, `layout-temp/Filter.jpg`

##### Flow Context

- **User arrives from**: Screen 1 by clicking a questionnaire set name
- **Screen purpose**: Manage one questionnaire set's metadata, ordered questions, preview, publish controls, and history
- **Entry point**: Partially present; `Questionnaire.jpg` shows a module page titled "Questionnaire" but not a selected set identity
- **Exit path**: Partial; question rows can be viewed/edited and preview opened, but no publish/activate control is visible
- **Data continuity**: Issues; set name, version, usage locations, and breadcrumb `Questionnaire Catalog → [Set Name]` are absent
- **Flow context issues**: The layout behaves like a question bank/list, not a set-details screen with set metadata and publish controls

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Set Name | Yes | ❌ | Spec row requires a set name field; `Questionnaire.jpg` only shows page title "Questionnaire" and question rows |
| Context Type | Yes | ❌⚠️ | `Questionnaire.jpg` / `Fulltable.jpg` show per-question `Context Type` column, not a set-level select field |
| Description | No | ❌ | No description field visible in any mapped layout file |
| Category | Yes | ❌⚠️ | `Fulltable.jpg` shows per-question `Category`, not a set-level category assignment from Screen 4 |
| Tags | No | ❌ | No chips/tags area visible |
| Status | read-only | ❌⚠️ | Status badges shown are per-question row status, not the set's Draft / Active / Archived badge |
| Version | read-only | ❌ | No set version field visible |
| Used In | read-only | ❌ | No usage locations visible |
| # | Yes | ✅ | `Fulltable.jpg` shows `Display Order` column with values 1-10, covering ordered question rows |
| Question Text | Yes | ✅ | `Questionnaire.jpg` and `Fulltable.jpg` show question text rows such as "Any known allergies to medications." |
| Question Type | Yes | ❌ | No question-type label column or chip visible |
| Severity | Conditional | ✅ | `Questionnaire.jpg` / `Fulltable.jpg` show severity badges such as `Critical`, `Standard`, `None` |
| Status | Yes | ✅ | Question-row status badges such as `Active` / `Inactive` are visible |
| Actions | — | ✅ | Row overflow menu shows `View`, `Edit`, `Delete` in `Questionnaire.jpg` / `Fulltable.jpg` |

**Extra Elements**:

- Search bar at top right of `Questionnaire.jpg`
- Top-level `+ Add New Question` button in `Questionnaire.jpg`
- `Filter.jpg` modal with `Category`, `Context type`, `Severity`, `Status`
- Tabs `Questionnaire`, `Categories`, `Version History & Audit Trail`

**Screen Status**: 🔴 FAIL
**Field Coverage**: 4/8 (50%)
**Critical Issues**: Missing set identity and metadata block; no publish/activate control; screen content is question-centric rather than set-centric

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| 🔴 Critical UX | The page never establishes which questionnaire set is being edited, so admins lose essential context before changing questions. | Add a set header with set name, status, version, category, tags, and usage summary above the question list. |
| ⚠️ UX Improvement | Tabs mix unrelated concerns without a strong parent/child hierarchy, and the primary CTA is `Add New Question` instead of publish-oriented workflow actions. | Reframe the page around the set lifecycle: metadata, questions, preview, publish, and history with clearer CTA priority. |
| 💡 UX Suggestion | The filter/search tools are visually standard but disconnected from a missing set summary/breadcrumb. | Add breadcrumb and sticky header actions to keep navigation and state visible while filtering long lists. |

#### Screen 3: Question Editor

**Layout**: `layout-temp/Question Editor.jpg`

##### Flow Context

- **User arrives from**: Screen 2 by clicking `Edit` on a question row or `Add New Question`
- **Screen purpose**: Configure one question's content, severity, conditional fields, and patient/provider presentation
- **Entry point**: Present; dedicated `Question Editor` page is visible in `Question Editor.jpg`
- **Exit path**: Partial; `Save Setting` button is visible, but there is no explicit cancel/back path shown in the content area
- **Data continuity**: Issues; the page does not show parent questionnaire set identity, question ID, or audit metadata
- **Flow context issues**: The editor only exposes a small subset of the FR's required configuration controls and omits most conditional sections

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Question Type | Yes | ✅ | `Question Editor.jpg` shows `Question Type` field populated with `Yes/No` |
| Question Text | Yes | ✅ | `Question Editor.jpg` shows `Question Text` input with sample value |
| Help Text | No | ❌ | No help-text field visible |
| Detail Prompt (Yes answer) | Conditional | ❌ | Missing despite the shown `Yes/No` question type and `Multi-Context` context |
| Scale Point Labels | Conditional | ❌ | No scale-label section visible |
| Scale Min / Max Labels | Conditional | ❌ | No min/max label section visible |
| Options | Conditional | ❌ | No options list builder visible |
| Placeholder Text | Conditional | ❌ | No placeholder-text field visible |
| Max Characters | Conditional | ❌ | No character-limit field visible |
| Severity Flag | Conditional | ✅ | `Severity` dropdown is visible with `None` selected |
| Alert Description | Conditional | ❌ | No alert-description field visible |
| Patient App — Display Label | No | ❌ | No patient-display-label override visible |
| Patient App — Show Question Number | No | ❌ | No checkbox visible |
| Patient App — Visible to Patient | No | ❌ | No checkbox visible |
| Provider App — Display Label | No | ❌ | No provider-display-label field visible |
| Provider App — Highlight Response | No | ❌ | No highlight-response checkbox visible |
| Question ID | read-only | ❌ | No read-only question ID visible |
| Created Date | read-only | ❌ | No created date visible |
| Last Modified | read-only | ❌ | No last-modified timestamp visible |
| Modified By | read-only | ❌ | No modified-by field visible |
| Status | Yes | ✅ | `Active question` toggle is visible |

**Extra Elements**:

- `Category` dropdown not specified on Screen 3
- `Context Type` dropdown not specified on Screen 3
- `Display Order` numeric field not specified on Screen 3

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 4/6 (67%)
**Critical Issues**: Missing conditional detail prompt and alert description for severity-aware Yes/No questions; no patient/provider display configuration

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | The form is compact and readable, but it hides the high-value configuration areas that explain how the question behaves in patient and provider apps. | Split the editor into grouped sections: content, answer-type settings, severity/alerting, patient display, provider display, and audit metadata. |
| ⚠️ UX Improvement | `Save Setting` is generic and the page lacks a visible cancel/back action. | Use task-specific CTAs such as `Save Question` and add a secondary `Cancel` action near the primary button. |
| 💡 UX Suggestion | The page has generous whitespace but little instructional text about locked question type behavior. | Add inline helper text and a first-save warning near the question type selector. |

#### Screen 4: Category Management

**Layout**: `layout-temp/Categories.jpg`, `layout-temp/Add/Edit Category.jpg`

##### Flow Context

- **User arrives from**: Questionnaire module tab or category-management action from set maintenance
- **Screen purpose**: Maintain the global category list and edit one category definition
- **Entry point**: Present; `Categories.jpg` shows the list and `Add/Edit Category.jpg` shows the edit form
- **Exit path**: Partial; row menu supports edit/delete and edit form has `Save Setting`, but deactivate semantics are unclear
- **Data continuity**: Correct for category name/description editing, but assigned-set count semantics are unclear
- **Flow context issues**: Category counts and state-management actions do not fully align with the FR wording

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Category Name | Yes | ✅ | `Categories.jpg` lists `Category Name`; `Add/Edit Category.jpg` includes editable `Category name` field |
| Description | No | ✅ | Description column and edit textarea are visible |
| Total Sets | No | ❌⚠️ | `Categories.jpg` shows `Question Count`, not the FR's `Total Sets` assigned to category |
| Status | Yes | ✅ | Active / Inactive badges and `Active category` toggle are visible |
| Actions | — | ❌⚠️ | Row menu shows `Edit` and `Delete`; FR also expects deactivate path on the screen |

**Extra Elements**:

- `Display Order` column and field not specified in the FR

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 2/2 (100%)
**Critical Issues**: Count semantics mismatch (`Question Count` vs assigned set count); deactivate action is not explicit on the list view

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | The list/edit pairing is straightforward, but the meaning of `Question Count` is ambiguous for a category-management surface. | Rename the derived count to match the real object being counted and surface tooltip/help text if needed. |
| 💡 UX Suggestion | The separate edit page is clean but heavier than the FR's inline/modal expectation. | Consider inline drawer or modal editing for faster category maintenance. |

#### Screen 5: Context Type Reference

**Layout**: `{no mapped layout file}`

##### Flow Context

- **User arrives from**: Admin seeking context-type guidance while creating or assigning a questionnaire set
- **Screen purpose**: Read-only reference for Inquiry / Aftercare / Multi-Context definitions and usage
- **Entry point**: Missing; no layout file shows a context-type reference view
- **Exit path**: Missing
- **Data continuity**: Not verifiable
- **Flow context issues**: The informational reference screen is entirely absent from the supplied layouts

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Context Type Name | read-only | ❌ | No layout file shows a dedicated context-type reference table or cards |
| Description | read-only | ❌ | No layout file shows context-type descriptions |
| Active Sets Count | read-only | ❌ | No layout file shows per-context active-set counts |
| Questionnaire Sets | read-only | ❌ | No layout file shows linked lists of sets per context type |
| Integration Points | read-only | ❌ | No layout file shows FR-003 / FR-011 integration references |

**Extra Elements**:

- None; no mapped design exists

**Screen Status**: ⬜ NO DESIGN
**Field Coverage**: 0/0 (n/a)
**Critical Issues**: Entire reference screen is missing

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| 🔴 Critical UX | Admins have no in-product reference for context-type differences, increasing the chance of wrong set configuration or assignment. | Add the dedicated read-only reference screen or contextual help panel described in the FR. |

#### Screen 6: Questionnaire Preview

**Layout**: `layout-temp/Preview all.jpg`

##### Flow Context

- **User arrives from**: Screen 2 via the preview action
- **Screen purpose**: Compare patient-facing render vs provider-summary render for one questionnaire set
- **Entry point**: Partial; `Preview all Questionnaire` view exists
- **Exit path**: Missing explicit back/close control in the visible content area
- **Data continuity**: Partial; the preview renders questionnaire content but does not show which draft/version is being previewed
- **Flow context issues**: Only one patient-style preview is shown; provider-summary and test-mode behavior are absent

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| View | Yes | ❌ | No tab selector for `Patient App (Mobile)` / `Provider Summary`; only one page title is visible in `Preview all.jpg` |
| Test Mode | No | ❌ | No toggle or simulation switch visible |
| Questionnaire Render | read-only | ✅ | `Preview all.jpg` shows rendered questions in display order |
| Sample Response Inputs | Conditional | ✅ | Yes/No response controls are visible beside each question |
| Provider Summary Render | Conditional | ❌ | No provider-summary preview area or alternate tab visible |
| Print Preview | No | ❌ | No print action visible |

**Extra Elements**:

- Right-side filter panel with `Category`, `Context type`, `Severity`, `Status`
- `Medical Alerts` label in content area, not specified as a standalone field

**Screen Status**: 🔴 FAIL
**Field Coverage**: 1/2 (50%)
**Critical Issues**: Missing required view switcher; no provider-summary preview; no print control

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| 🔴 Critical UX | The screen only previews one patient-style rendering, so admins cannot validate the provider-summary output that the FR explicitly requires. | Add a persistent two-tab preview pattern with equivalent content depth for both patient and provider views. |
| ⚠️ UX Improvement | The long yes/no list is readable, but the right-side filter panel competes with the main preview and may imply editing instead of previewing. | Reduce or collapse secondary controls and keep the preview surface dominant. |
| 💡 UX Suggestion | There is no clear indication that the preview reflects the current draft state. | Add draft/version badge and set name at the top of the preview. |

#### Screen 7: Version History & Audit Trail

**Layout**: `layout-temp/Version History & Audit Trail.jpg`

##### Flow Context

- **User arrives from**: Screen 2 via `View Version History`
- **Screen purpose**: Review published versions and per-action audit history for one questionnaire set
- **Entry point**: Present; `Version History & Audit Trail.jpg` shows both history tables on one page
- **Exit path**: Partial; no visible row actions or back action in content area, but the tabbed navigation is present
- **Data continuity**: Good; version rows and audit rows share the same questionnaire context
- **Flow context issues**: Required row actions are absent from the visible design

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Version Number | read-only | ✅ | `Version History & Audit Trail.jpg` shows `Version` column with values like `Qv0.001` |
| Published Date | read-only | ✅ | `Activation Date` column is visible; functionally equivalent to published date |
| Published By | read-only | ✅ | `Activated by` column shows `Admin`; functionally equivalent to published by |
| Question Count | read-only | ✅ | `Question count` column is visible |
| Changes Summary | read-only | ✅ | `Change summary` column is visible |
| Status | read-only | ✅ | Status badges appear in the version table |
| Actions | — | ❌ | No visible `View Snapshot` or `Restore as New Draft` action controls |
| Change Date | read-only | ✅ | `Change date` column is visible in Audit Trail |
| Admin Name | read-only | ✅ | `Admin name` column is visible |
| Action Type | read-only | ✅ | `Action type` column is visible |
| Question ID | read-only | ✅ | `Question ID` column is visible |
| Change Details | read-only | ✅ | `Change details` column is visible |
| IP Address | read-only | ✅ | `IP Address` column is visible |

**Extra Elements**:

- Combined single-page layout for version history and audit trail, whereas the FR describes them as sections of one screen

**Screen Status**: 🟢 GOOD
**Field Coverage**: 10/10 (100%)
**Critical Issues**: Missing row actions for snapshot/restore

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | The two stacked tables provide strong audit density, but the lack of visible row actions weakens the user's ability to act on the history. | Add explicit row-level actions for viewing snapshots and restoring a version as a new draft. |
| 💡 UX Suggestion | Dense table rows may become difficult to scan on smaller laptop screens. | Add sticky headers and optional row filters for large audit histories. |

**Flow Coverage Gaps**:

- No dedicated Screen 1 questionnaire-set catalog layout exists in `layout-temp/`
- No Screen 5 context-type reference layout exists in `layout-temp/`
- Screen 2 omits set-level metadata, usage summary, and publish controls
- Screen 6 omits provider-summary preview and print action

---

### Flow 2: Severity Management (Inquiry Context Only)

**Status**: 🔴 BLOCKED — the editor exposes a severity selector but omits the supporting alert-description and yes-answer detail controls needed for inquiry-alert configuration.
**Screens required**: 1
**Layout files**: `Question Editor.jpg`

#### Screen 3: Question Editor

**Layout**: `layout-temp/Question Editor.jpg`

##### Flow Context

- **User arrives from**: Workflow 1 set-details screen while editing an Inquiry or Multi-Context question
- **Screen purpose**: Assign severity metadata that drives downstream provider alerts for inquiry submissions
- **Entry point**: Present; `Question Editor.jpg` opens a dedicated question form
- **Exit path**: Partial; `Save Setting` exists, but no publish-readiness or draft-version cues are visible
- **Data continuity**: Issues; the editor does not show whether the parent set is currently Active vs Draft, which matters in this workflow
- **Flow context issues**: The screen lacks the explanatory and validation surfaces that connect severity configuration to downstream alert behavior

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Question Type | Yes | ✅ | `Question Editor.jpg` shows `Yes/No`, which is compatible with the inquiry alert workflow |
| Question Text | Yes | ✅ | The question text field is visible with sample content |
| Detail Prompt (Yes answer) | Conditional | ❌ | Missing even though the visible question is `Yes/No` and context is `Multi-Context` |
| Severity Flag | Conditional | ✅ | `Severity` dropdown is visible with `None` selected |
| Alert Description | Conditional | ❌ | No alert-description field or helper text visible |
| Provider App — Highlight Response | No | ❌ | No provider-highlight control visible despite provider alert emphasis in the workflow |
| Last Modified | read-only | ❌ | No metadata confirming active/draft edit context |
| Status | Yes | ✅ | `Active question` toggle is visible |

**Extra Elements**:

- `Category`, `Context Type`, and `Display Order` fields that are not part of the severity-management requirement set

**Screen Status**: 🔴 FAIL
**Field Coverage**: 3/5 (60%)
**Critical Issues**: Missing required `Alert Description`; missing required `Detail Prompt (Yes answer)`; no visible draft/published context for edits to active sets

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| 🔴 Critical UX | Admins can pick a severity value without seeing the resulting alert description or any preview of provider impact, which makes misconfiguration likely. | Pair the severity selector with an alert-description field and a provider-alert preview or summary. |
| ⚠️ UX Improvement | The editor does not communicate whether the admin is editing a draft or triggering a new draft from an active set. | Surface draft/active status and versioning guidance prominently in the editor header. |
| ⚠️ UX Improvement | The consequences of choosing `Critical`, `Standard`, or `No Alert` are not explained inline. | Add concise helper text under the severity control that explains how each option maps to provider alerts. |

**Flow Coverage Gaps**:

- No `Alert Description` field or preview
- No `Detail Prompt (Yes answer)` control for the visible Yes/No inquiry question
- No draft/active version state or publish-readiness indication

---

### Flow 3: Questionnaire Deployment (System Flow)

**Status**: 🟢 COMPLETE — this workflow is system-triggered in the patient/provider platforms and has no direct admin-dashboard screen specification to verify in `layout-temp/`.
**Screens required**: 0
**Layout files**: `{none — system flow}`

**Flow Coverage Gaps**:

- None for admin-dashboard layout verification; downstream patient/provider behavior should be verified against their own design scopes

---

### Flow 4: Inquiry Activation & Downstream Assignment

**Status**: 🔴 BLOCKED — Workflow 4 depends on a published-set catalog with designation state and activation action, but no dedicated Screen 1 layout exists in the supplied files.
**Screens required**: 1
**Layout files**: `{no dedicated Screen 1 layout}`

#### Screen 1: Questionnaire Catalog

**Layout**: `{no dedicated layout file mapped}`

##### Flow Context

- **User arrives from**: Admin returns to the questionnaire catalog after publishing a compatible Inquiry or Multi-Context set
- **Screen purpose**: Designate exactly one published set as active for Inquiry and see designation/assignment state
- **Entry point**: Missing; supplied layouts do not show a questionnaire-set catalog or activation state
- **Exit path**: Missing; no visible `Set as Active for Inquiry` action, confirmation flow, or designation removal path
- **Data continuity**: Issues; no current active-set indicator or "Used In" context is visible
- **Flow context issues**: The core activation flow is unsupported by the delivered designs

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Set Name | Yes | ❌ | No dedicated set list visible for admins to choose the active Inquiry questionnaire |
| Context Type | Yes | ❌ | No mapped screen shows set-level Inquiry / Aftercare / Multi-Context status in an activation-ready catalog |
| Status | Yes | ❌ | No mapped screen shows whether a set is Draft / Active / Archived at set level |
| Used In | No | ❌ | No usage-location context visible |
| Inquiry Active | No | ❌ | No `Active for Inquiry` badge or equivalent designation indicator visible |
| Actions | — | ❌ | No `Set as Active for Inquiry` action or confirmation affordance visible |

**Extra Elements**:

- None on a dedicated Screen 1 layout because the screen is missing

**Screen Status**: ⬜ NO DESIGN
**Field Coverage**: 0/3 (0%)
**Critical Issues**: Missing dedicated activation catalog; no activation CTA; no active-inquiry designation state

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| 🔴 Critical UX | Admins cannot complete the inquiry-activation workflow because the design never exposes the designated-set state or activation action. | Add a set-level catalog with `Set as Active for Inquiry`, active badge state, and replacement confirmation flow. |
| ⚠️ UX Improvement | The FR requires clear system feedback when no set is designated for Inquiry, but no such warning surface is designed. | Add a warning banner and empty-state guidance when the inquiry flow is unconfigured. |

**Flow Coverage Gaps**:

- No set-level activation action
- No current-designation badge or replacement confirmation pattern
- No unconfigured inquiry-flow warning banner

---

## Action Items

| Priority | Flow | Screen | Issue | Recommendation |
|----------|------|--------|-------|----------------|
| 🔴 Critical | Flow 1 / Flow 4 | Screen 1 | No questionnaire-set catalog or inquiry-activation UI is designed. | Design a dedicated set-level catalog with set name, status, version, used-in summary, `Active for Inquiry` badge, and `Set as Active for Inquiry` action + confirmation flow. |
| 🔴 Critical | Flow 1 | Screen 2 | Set-details screen is implemented as a question list and omits set metadata, usage summary, and publish controls. | Add a persistent set header and lifecycle controls (`Preview`, `Publish / Activate`, `View Version History`) above the ordered question list. |
| 🔴 Critical | Flow 2 | Screen 3 | Severity-management flow lacks `Detail Prompt (Yes answer)` and `Alert Description`, so alert configuration is incomplete. | Add both conditional fields with inline severity guidance and provider-alert preview. |
| 🔴 Critical | Flow 1 | Screen 5 | Context Type Reference screen is completely missing. | Add the read-only context reference surface or an equivalent guided help panel covering Inquiry / Aftercare / Multi-Context and their integration points. |
| 🔴 Critical | Flow 1 | Screen 6 | Preview screen only shows one patient-style view and cannot validate provider-summary output. | Add `Patient App` / `Provider Summary` tabs, test mode, and print action. |
| ⚠️ Important | Flow 1 | Screen 4 | Category list uses `Question Count` and hides deactivate semantics, which diverges from the FR. | Rename the derived count to match assigned questionnaire sets and expose a clear deactivate action/state. |
| ⚠️ UX Improvement | Flow 1 | Screen 7 | Version history lacks visible snapshot/restore actions. | Add explicit row-level actions and sticky table controls for long audit histories. |

### Priority Legend

- **🔴 Critical**: Blocks flow progression, breaks data integrity, or causes security/legal risk. Must fix before development.
- **🔴 Critical UX**: Severe usability issue that would prevent users from completing the flow or cause significant confusion. Must fix before development.
- **⚠️ Important**: Functional discrepancy that could cause user confusion or require rework during development. Should fix before development.
- **⚠️ UX Improvement**: Usability or design quality issue that deviates from platform conventions or best practices. Should fix before development.
- **💡 Suggestion**: Cosmetic or minor improvement. Can fix anytime.
- **💡 UX Suggestion**: Minor design enhancement that would improve polish. Can fix anytime.

---

## Notes

- Source FR: `local-docs/project-requirements/functional-requirements/fr025-medical-questionnaire-management/prd.md`
- Layout inventory captured from `layout-temp/` on 2026-03-23
- Layout review used direct image inspection plus OCR (`tesseract`) to verify visible labels and controls
- Supplied layouts behave as a question-centric tabbed module; they do not cover the FR's set-level catalog and activation model
- Web UX review references the latest Vercel Web Interface Guidelines fetched from the upstream source during this verification
