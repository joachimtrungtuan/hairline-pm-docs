# Design Layout Verification Report — FR-026

**Report Date**: 2026-04-02
**Report Type**: Design Layout Verification
**FR Scope**: FR-026 - App Settings & Security Policies
**Flow Scope**: Screen 5a and Screen 5b only
**Layout Source**: `layout-temp/`
**Platform**: Admin Web
**Status**: 🟡 PARTIAL

---

## Summary Dashboard

| # | Flow | Module | Screens Required | Screens Verified | Layout Status | Field Coverage |
|---|------|--------|-----------------|-----------------|---------------|----------------|
| A4 | Admin Edits Inquiry Cancellation Reasons | A-09: System Settings & Configuration | 1 | 1 | 🟡 PARTIAL | ~50% |
| A5 | Admin Edits Account Deletion Reasons | A-09: System Settings & Configuration | 1 | 1 | 🟡 PARTIAL | ~75% |

**Overall**: 2 of 2 scoped flows verified. Both flows have design coverage, but both are incomplete against FR-026 because required supporting states and business-rule-specific row behavior are missing or mismatched.
**Screens**: 2 of 2 specified screens have layouts (~100% layout coverage).

---

## Layout File Inventory

### Mapped to Spec Flows

| Layout File | Maps to Flow | Maps to Screen |
|-------------|-------------|----------------|
| `layout-temp/General Settings - App Data  - Inquiry Cancellation Reasons.jpg` | A4 | Screen 5a (Inquiry Cancellation Reasons Manager) |
| `layout-temp/Inquiry Cancellation Reasons.jpg` | A4 | Screen 5a (Add reason modal state) |
| `layout-temp/General Settings - App Data  - Inquiry Cancellation Reasons-1.jpg` | A5 | Screen 5b (Account Deletion Reasons Manager) |
| `layout-temp/Inquiry Cancellation Reasons-1.jpg` | A5 | Screen 5b (Add reason modal state) |

### Unmapped Files

| Layout File | Likely Purpose | Notes |
|-------------|---------------|-------|
| None | N/A | All files in `layout-temp/` map to the requested scope |

---

## Detailed Verification by Flow

---

### Flow A4: Admin Edits Inquiry Cancellation Reasons

**Status**: 🟡 PARTIAL — The main list screen and add modal are present, but the fixed `Other` business rule is not respected in the visible row data, and supporting states called out by the FR are missing.
**Screens required**: 1
**Layout files**: `layout-temp/General Settings - App Data  - Inquiry Cancellation Reasons.jpg`, `layout-temp/Inquiry Cancellation Reasons.jpg`

#### Screen 5a: Inquiry Cancellation Reasons Manager

**Layout**: `layout-temp/General Settings - App Data  - Inquiry Cancellation Reasons.jpg`, `layout-temp/Inquiry Cancellation Reasons.jpg`

##### Flow Context

- **User arrives from**: FR-026 `### Alternative Flows > A4: Admin Edits Inquiry Cancellation Reasons` by navigating to `Settings -> App Data -> Inquiry Cancellation Reasons`.
- **Screen purpose**: Manage predefined cancellation reason options consumed by FR-003 Screen 8a.
- **Entry point**: Present. The list screen clearly shows `App Data` with the `Inquiry Cancellation Reasons` tab selected.
- **Exit path**: Partial. The add modal shows `Cancel` and `Save`, but no post-save `Change Reason` modal is provided.
- **Data continuity**: Partial. The list and modal share the same schema, but the visible fixed terminal row is `Others` rather than the required `Other`.
- **Flow context issues**:
  - No layout provided for the mandatory `Change Reason` modal required after save.
  - No visible drag-and-drop or reorder affordance despite A4 and Screen 5a notes requiring drag-and-drop reordering.
  - No visible usage analytics block or date range filter.
  - No visible warning state before deactivating a frequently selected reason.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Reason Label | Yes | ❌⚠️ | Field is present in both the table and add modal, but the fixed terminal option is shown as `Others` in the list screen. FR-026 `### Screen 5a` requires fixed `Other` (singular). Evidence: `layout-temp/General Settings - App Data  - Inquiry Cancellation Reasons.jpg` table last row. |
| Requires Explanation | Yes | ❌⚠️ | Field is present as both a table column and a checkbox in the add modal, but the visible terminal `Others` row shows `-` instead of an always-on explanation flag. FR-026 `### Screen 5a` states `Other` must always require explanation. Evidence: `layout-temp/General Settings - App Data  - Inquiry Cancellation Reasons.jpg` table last row; checkbox field visible in `layout-temp/Inquiry Cancellation Reasons.jpg`. |
| Display Order | No | ✅ | Present as `Order` column in the list and numeric input in the add modal. Functional label equivalence is acceptable. Evidence: both 5a layout files. |
| Active | Yes | ✅ | Present as `Status` pills in the list and `Status` dropdown in the add modal with `Active` selected. Evidence: both 5a layout files. |

**Extra Elements**:

- Left application sidebar, top header utilities, and App Data tab strip are present as surrounding admin-shell navigation. These are expected admin web chrome, not scope issues.

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 2/4 (50%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: ui-ux-pro-max, web-design-guidelines

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-18` Destructive action safeguard: the open row menu styles `Archive` the same way as `Edit`, with no destructive color, warning icon, or confirmation cue visible. Evidence: `layout-temp/General Settings - App Data  - Inquiry Cancellation Reasons.jpg` right-side action menu. | Differentiate `Archive` visually from safe actions and pair it with a confirmation state. |
| ⚠️ UX Improvement | `W-06` Table design / `U-16` Interactive vs static distinction: reordering is a core flow requirement, but no drag handle, move affordance, or reorder control is visible; only static order numbers are shown. Evidence: `layout-temp/General Settings - App Data  - Inquiry Cancellation Reasons.jpg` table and `layout-temp/Inquiry Cancellation Reasons.jpg` modal. | Add a clear drag handle or explicit reorder interaction so admins can understand how ordering is changed. |
| 💡 UX Suggestion | `U-23` Terminology consistency: breadcrumb text reads `Setting / General Setting / App Data`, while sidebar labels use `Settings` and `General Settings`. Evidence: both 5a layout files. | Normalize breadcrumb and sidebar terminology to one naming convention. |

**Flow Coverage Gaps**:

- No design provided for the mandatory change-reason confirmation modal after save.
- No alternate state showing validation feedback for duplicate reason labels.
- No state showing deactivation warning for frequently selected reasons.
- No layout evidence for usage analytics with date range filter.

---

### Flow A5: Admin Edits Account Deletion Reasons

**Status**: 🟡 PARTIAL — The main list screen and add modal are present, but the fixed `Others` row does not visibly enforce the required explanation rule, and the supporting states specified by the FR are missing.
**Screens required**: 1
**Layout files**: `layout-temp/General Settings - App Data  - Inquiry Cancellation Reasons-1.jpg`, `layout-temp/Inquiry Cancellation Reasons-1.jpg`

#### Screen 5b: Account Deletion Reasons Manager

**Layout**: `layout-temp/General Settings - App Data  - Inquiry Cancellation Reasons-1.jpg`, `layout-temp/Inquiry Cancellation Reasons-1.jpg`

##### Flow Context

- **User arrives from**: FR-026 `### Alternative Flows > A5: Admin Edits Account Deletion Reasons` by navigating to `Settings -> App Data -> Account Deletion Reasons`.
- **Screen purpose**: Manage predefined deletion reason options consumed by FR-001 Screen 16.
- **Entry point**: Present. The list screen clearly shows `App Data` with the `Account Deletion Reasons` tab selected.
- **Exit path**: Partial. The add modal shows `Cancel` and `Save`, but no post-save `Change Reason` modal is provided.
- **Data continuity**: Partial. The list and modal share the same schema, but the terminal `Others` row does not visibly show the required explanation state.
- **Flow context issues**:
  - No layout provided for the mandatory `Change Reason` modal required after save.
  - No visible drag-and-drop or reorder affordance despite A5 and Screen 5b notes requiring drag-and-drop reordering.
  - No visible usage analytics block or date range filter.
  - No visible warning state before deactivating a frequently selected reason.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Reason Label | Yes | ✅ | Present in both the table and add modal, and the fixed terminal row is labeled `Others`, matching FR-026 `### Screen 5b`. Evidence: `layout-temp/General Settings - App Data  - Inquiry Cancellation Reasons-1.jpg` table last row and `layout-temp/Inquiry Cancellation Reasons-1.jpg` modal. |
| Requires Explanation | Yes | ❌⚠️ | Field is present as both a table column and a checkbox in the add modal, but the visible terminal `Others` row shows `-` instead of the required always-on explanation state. FR-026 `### Screen 5b` states `Others` must always require explanation. Evidence: `layout-temp/General Settings - App Data  - Inquiry Cancellation Reasons-1.jpg` table last row. |
| Display Order | No | ✅ | Present as `Order` column in the list and numeric input in the add modal. Functional label equivalence is acceptable. Evidence: both 5b layout files. |
| Active | Yes | ✅ | Present as `Status` pills in the list and `Status` dropdown in the add modal with `Active` selected. Evidence: both 5b layout files. |

**Extra Elements**:

- Left application sidebar, top header utilities, and App Data tab strip are present as surrounding admin-shell navigation. These are expected admin web chrome, not scope issues.

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 3/4 (75%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: ui-ux-pro-max, web-design-guidelines

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-18` Destructive action safeguard: the open row menu styles `Archive` the same way as `Edit`, with no destructive color, warning icon, or confirmation cue visible. Evidence: `layout-temp/General Settings - App Data  - Inquiry Cancellation Reasons-1.jpg` right-side action menu. | Differentiate `Archive` visually from safe actions and pair it with a confirmation state. |
| ⚠️ UX Improvement | `W-06` Table design / `U-16` Interactive vs static distinction: reordering is a core flow requirement, but no drag handle, move affordance, or reorder control is visible; only static order numbers are shown. Evidence: `layout-temp/General Settings - App Data  - Inquiry Cancellation Reasons-1.jpg` table and `layout-temp/Inquiry Cancellation Reasons-1.jpg` modal. | Add a clear drag handle or explicit reorder interaction so admins can understand how ordering is changed. |
| 💡 UX Suggestion | `U-23` Terminology consistency: breadcrumb text reads `Setting / General Setting / App Data`, while sidebar labels use `Settings` and `General Settings`. Evidence: both 5b layout files. | Normalize breadcrumb and sidebar terminology to one naming convention. |

**Flow Coverage Gaps**:

- No design provided for the mandatory change-reason confirmation modal after save.
- No alternate state showing validation feedback for duplicate reason labels.
- No state showing deactivation warning for frequently selected reasons.
- No layout evidence for usage analytics with date range filter.

---

## Action Items

| Priority | Flow | Screen | Issue | Recommendation |
|----------|------|--------|-------|----------------|
| ⚠️ Important | A4 | 5a | Fixed final reason is shown as `Others`, but FR-026 Screen 5a requires fixed `Other`. | Correct the fixed row label and ensure the screen uses 5a-specific content instead of a reused 5b list. |
| ⚠️ Important | A4 | 5a | Fixed final reason does not visibly enforce `Requires Explanation = true`. | Show the fixed `Other` row with explanation enabled and locked. |
| ⚠️ Important | A5 | 5b | Fixed `Others` row does not visibly enforce `Requires Explanation = true`. | Show the fixed `Others` row with explanation enabled and locked. |
| ⚠️ Important | A4 | 5a | Mandatory post-save `Change Reason` modal is missing from the design set. | Add the save-confirmation reason modal state with 10-500 char requirement. |
| ⚠️ Important | A5 | 5b | Mandatory post-save `Change Reason` modal is missing from the design set. | Add the save-confirmation reason modal state with 10-500 char requirement. |
| ⚠️ UX Improvement | A4 | 5a | No visible reorder affordance for a drag-and-drop-managed list. | Add drag handles or explicit reorder controls. |
| ⚠️ UX Improvement | A5 | 5b | No visible reorder affordance for a drag-and-drop-managed list. | Add drag handles or explicit reorder controls. |
| ⚠️ UX Improvement | A4 | 5a | `Archive` is not visually differentiated from `Edit` in the action menu. | Apply destructive styling and confirmation cues to archive/deactivate actions. |
| ⚠️ UX Improvement | A5 | 5b | `Archive` is not visually differentiated from `Edit` in the action menu. | Apply destructive styling and confirmation cues to archive/deactivate actions. |
| 💡 Suggestion | A4 | 5a | Usage analytics and deactivation-warning states called out in the FR are absent. | Add supplemental states for analytics, warnings, and filters. |
| 💡 Suggestion | A5 | 5b | Usage analytics and deactivation-warning states called out in the FR are absent. | Add supplemental states for analytics, warnings, and filters. |

### Priority Legend

- **🔴 Critical**: Blocks flow progression, breaks data integrity, or causes security/legal risk. Must fix before development.
- **🔴 Critical UX**: Severe usability issue that would prevent users from completing the flow or cause significant confusion. Must fix before development.
- **⚠️ Important**: Functional discrepancy that could cause user confusion or require rework during development. Should fix before development.
- **⚠️ UX Improvement**: Usability or design quality issue that deviates from platform conventions or best practices. Should fix before development.
- **💡 Suggestion**: Cosmetic or minor improvement. Can fix anytime.
- **💡 UX Suggestion**: Minor design enhancement that would improve polish. Can fix anytime.

---

## Notes

- Requirement source used: `local-docs/project-requirements/functional-requirements/fr026-app-settings-security/prd.md`, specifically `### Alternative Flows > A4`, `### Alternative Flows > A5`, `### Screen 5a`, and `### Screen 5b`.
- Layout evidence used: the four JPG files currently present in `layout-temp/`.
- This review was limited to the requested screens only; no other FR-026 screens were evaluated.
