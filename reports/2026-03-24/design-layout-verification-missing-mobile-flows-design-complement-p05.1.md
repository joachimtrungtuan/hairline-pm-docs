# Design Layout Verification Report — Missing Mobile Flows Design Complement

**Report Date**: 2026-03-24
**Report Type**: Design Layout Verification
**FR Scope**: FR-010, FR-011
**Flow Scope**: P05.1 Day-to-Day Treatment Progress
**Layout Source**: `layout-temp/in progress/`
**Platform**: Patient Mobile App
**Status**: 🟡 PARTIAL
**Approval Status**: 🟢 Approved with minor issues

---

## Summary Dashboard

| # | Flow | Module | Screens Required | Screens Verified | Layout Status | Field Coverage |
|---|------|--------|-----------------|-----------------|---------------|----------------|
| P05.1 | Day-to-Day Treatment Progress | P-05: Aftercare & Progress Monitoring | 3 | 3 | 🟡 PARTIAL | 23/26 (~88%) |

**Overall**: 1 of 1 flows verified. After remapping all `in progress` files as a reorganized tabbed case-detail experience, the flow is substantially covered, but the completed-state evidence and day-detail interaction model still diverge from the source spec.
**Screens**: 3 of 3 specified screens have layout evidence when the designer's tabbed reorganization is taken into account (100% screen coverage).

---

## Layout File Inventory

### Mapped to Spec Flows

| Layout File | Maps to Flow | Maps to Screen | Notes |
|-------------|-------------|----------------|-------|
| `layout-temp/in progress/Booking info.jpg` | P05.1 | P05.1-S1 / P05.1-S3 | Shared case-shell booking tab; provides start date and journey timeline context |
| `layout-temp/in progress/Provider.jpg` | P05.1 | P05.1-S1 / P05.1-S3 | Shared case-shell provider tab; provides provider/clinic identity context |
| `layout-temp/in progress/Treatment.jpg` | P05.1 | P05.1-S1 / P05.1-S2 | Treatment tab with overall progress and expanded day-level treatment details inline |
| `layout-temp/in progress/End of Treatment.jpg` | P05.1 | P05.1-S3 | Completed-treatment summary tab with outcome and post-op content |

### Unmapped Files

| Layout File | Likely Purpose | Notes |
|-------------|---------------|-------|
| `layout-temp/in progress/Problem.jpg` | Case problem / questionnaire tab | Related to the same case shell but outside the `P05.1` treatment-progress / completed-summary requirements |
| `layout-temp/in progress/My Treatments List.jpg` | P05.2 list state | Belongs to sibling flow P05.2 |
| `layout-temp/in progress/My Treatments List 2.jpg` | P05.2 list state variant | Belongs to sibling flow P05.2 |
| `layout-temp/in progress/My Treatments List - Empty.jpg` | P05.2 empty state | Belongs to sibling flow P05.2 |
| `layout-temp/in progress/Sorting.jpg` | P05.2 sort/filter state | Belongs to sibling flow P05.2 |

---

## Detailed Verification by Flow

---

### Flow P05.1: Day-to-Day Treatment Progress

**Status**: 🟡 PARTIAL — the flow is largely represented through a reorganized multi-tab case shell, but the inline day-detail model and completed-state coverage still diverge from the source spec
**Approval**: 🟢 Approved with minor issues — the reorganization is accepted for design sign-off, with the remaining mismatches documented for follow-up
**Screens required**: 3
**Layout files**: `Booking info.jpg`, `Provider.jpg`, `Treatment.jpg`, `End of Treatment.jpg`

#### Screen P05.1-S1: Treatment Progress Timeline

**Layout**: `layout-temp/in progress/Booking info.jpg`, `layout-temp/in progress/Provider.jpg`, `layout-temp/in progress/Treatment.jpg`

##### Flow Context

- **User arrives from**: Active treatment case entry from Home or My Treatments, per the flow diagram at `missing-mobile-flows-design-complement.md:1284-1286`
- **Screen purpose**: Show the patient's in-progress treatment record with high-level progress and per-day status information
- **Entry point**: Present. The designer appears to have implemented `P05.1-S1` as a tabbed case-detail shell: `Booking info`, `Provider`, and `Treatment` share the same `IN PROGRESS` header and patient/case identity
- **Exit path**: Partial. The treatment tab provides day-by-day detail inline rather than clearly indicating the separate day-details popup defined in the source flow
- **Data continuity**: Good. Across the three tabs, the screen family shows provider identity, start date, journey timeline, treatment identity, assigned clinician, estimated graft count, beginning note, and day-by-day progress
- **Flow context issues**: The treatment tab appears to use always-visible inline day details instead of the popup interaction described in the source spec

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Case Status Badge | Yes | ✅ | Green `IN PROGRESS` badge is visible at the top of `Treatment.jpg`, matching the spec row for the status badge in `P05.1-S1` |
| Provider / Clinic Name | Yes | ✅ | `Provider.jpg` shows the provider card with `X Hair Transplant` and `Istanbul, Turkey` within the same shared `IN PROGRESS` case shell |
| Treatment Name | Yes | ✅ | `Fue Hair Transplant` is visible near the top and functionally matches the treatment-name field |
| Package Name | No | ⚠️ | A package-style value (`6 days`) and a long inclusions list are shown, but the package label itself is not explicit; treated as partial evidence for the optional package/add-on context |
| Assigned Clinician | Yes | ✅ | `Assigned Clinician` with `Wade Warren` is visible mid-screen |
| Procedure Date | Yes | ✅ | `Booking info.jpg` shows `Start treatment — 20 Feb at 10:12 am`, which provides the scheduled treatment date in the same tabbed case shell |
| Estimated Graft Count | Yes | ✅ | `Estimate Grafts` / `2,000 grafts` is shown near the top of the screen |
| Beginning Note | No | ✅ | `Beginning Note` section is visible with body text, satisfying the optional note field |
| Overall Progress | Yes | ✅ | `1 of 5 days complete` is visible above the treatment-day list |
| Treatment Days List | Yes | ✅ | `Treatment.jpg` shows a multi-row treatment-process list with per-day dates, statuses, and descriptive text, satisfying the required day-list field |
| Journey Timeline | Yes | ✅ | `Booking info.jpg` includes a timeline with `Requested`, `Offers`, `Offer Accepted`, `Scheduled`, `Confirmed`, and `In Progress`, satisfying the cross-stage timeline requirement in a sibling tab of the same screen shell |

**Extra Elements**:

- `PATIENT ID: HP202401` is shown at the top, but patient ID is not part of the `P05.1-S1` screen spec
- `Price per Graft` and the long `Medical Treatment Inclusions` list add quote/package detail beyond the core treatment-progress brief

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 9/9 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-02 Information priority`: in the reorganized shell, the key progress tab still places quote/package detail (`Price per Graft`, inclusions list) ahead of the actual treatment-progress content | Reorder the treatment tab so progress summary and day-by-day tracking appear before commercial/package detail |
| ⚠️ UX Improvement | `U-03 Visual grouping`: provider identity, booking timeline, and treatment-progress content are split across tabs with limited cross-tab summary on the active treatment tab | Add a compact summary block on the treatment tab so patients do not need to switch tabs to understand core case context |

#### Screen P05.1-S2: Day Details Popup

**Layout**: `layout-temp/in progress/Treatment.jpg` (inline expanded day entries rather than a separate popup file)

##### Flow Context

- **User arrives from**: Tapping a treatment day row on `P05.1-S1`, per `missing-mobile-flows-design-complement.md:1288-1290`
- **Screen purpose**: Provide a focused, informational popup for a single treatment day with date, description, and current status badge
- **Entry point**: Partial. No separate popup is shown, but `Treatment.jpg` displays expanded day entries inline beneath `Treatment process`, which appears to be the designer's replacement for a popup drill-down
- **Exit path**: Partial. Because the detail is embedded inline instead of shown in a popup, there is no dedicated close/dismiss action for this unit
- **Data continuity**: Present. Each inline day block carries the selected day label, date, descriptive text, and status within the same treatment-progress tab
- **Flow context issues**: The interaction model has changed from `tap row -> popup` to always-visible inline day details, so the screen is represented but reorganized

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Day Label | Yes | ✅ | Expanded day entries in `Treatment.jpg` show labels such as `Day 1` |
| Scheduled Date | Yes | ✅ | Expanded day entries show per-day dates such as `21 Feb, 2025` |
| Day Description | Yes | ✅ | Each day block includes a descriptive text section beneath the date/title |
| Status Badge | Yes | ✅ | At least some day entries show explicit status text such as `Not started`; colored status chips are also visible next to day rows |
| Close | — | ❌⚠️ | No close/dismiss control exists because the day detail is integrated inline instead of presented as a popup |

**Extra Elements**:

- None

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 4/4 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-25 Back navigation`: the inline-detail reorganization removes the dedicated popup dismissal pattern defined in the source spec, so the exit from a focused day detail is less explicit | If the inline pattern is intentional, add clearer expand/collapse affordances or update the spec to document that the popup was intentionally replaced |

#### Screen P05.1-S3: Completed Treatment View

**Layout**: `layout-temp/in progress/End of Treatment.jpg`, with partial case-shell context from `Booking info.jpg`, `Provider.jpg`, and `Treatment.jpg`

##### Flow Context

- **User arrives from**: Provider completes the end-treatment workflow and the patient opens the completed treatment record, per `missing-mobile-flows-design-complement.md:1295-1299`
- **Screen purpose**: Show the patient the completed-treatment outcome summary, including definitive graft count and provider-authored post-op information
- **Entry point**: Present. The layout clearly shows a `COMPLETED` badge and the `End of Treatment` tab active
- **Exit path**: Partial. The back arrow is visible, and the design clearly uses the same tabbed case-shell model, but the completed-state journey transition into Aftercare is not explicitly shown
- **Data continuity**: Partial. The completed tab carries the outcome-specific content, while some identity/context fields appear only in sibling tabs from the same shell pattern
- **Flow context issues**: The designer appears to have reorganized `P05.1-S3` into a tab of the broader case shell, but completed-state-specific cross-tab evidence is still incomplete

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Case Status Badge | Yes | ✅ | Green `COMPLETED` badge is visible at the top of `End of Treatment.jpg` |
| Provider / Clinic Name | Yes | ⚠️ | `Provider.jpg` shows the provider/clinic card within the same case-shell pattern, but this field is not visible directly on the delivered `End of Treatment` tab |
| Treatment Name | Yes | ⚠️ | `Treatment.jpg` shows `Fue Hair Transplant`, but the completed tab itself does not surface the treatment name |
| Package Name | No | ✅ | Optional package field is not shown, which is acceptable if no package was selected |
| Assigned Clinician | Yes | ⚠️ | `Treatment.jpg` shows `Assigned Clinician — Wade Warren`, but the completed tab does not repeat it |
| Procedure Date | Yes | ⚠️ | `Booking info.jpg` shows the treatment start date in the shared shell, but the completed tab does not display it directly |
| Actual Graft Count | Yes | ✅ | `Actual Graft Count` with `1,000 grafts` is visible |
| Estimated Graft Count | Yes | ❌⚠️ | The original estimate exists on the in-progress treatment tab, but it is not shown alongside the actual graft count on the completed tab as required |
| Treatment Summary Note | Yes | ✅ | `Treatment Summary Note` section is present |
| Prescription | Yes | ✅ | `Prescription` section is present |
| Advice | Yes | ✅ | `Advice` section is present |
| Medication Instructions | Yes | ✅ | `Medication Instructions` section is present |
| Before/After Photos | No | ✅ | A photo is shown under `Before and After Photos`, satisfying the optional gallery field |
| Treatment Days Summary | Yes | ❌⚠️ | A day-by-day list exists on `Treatment.jpg`, but a completed-state summary with terminal day statuses is not evidenced in the delivered end-treatment tab |
| Journey Timeline | Yes | ❌⚠️ | `Booking info.jpg` shows the journey timeline only through `In Progress`; the required `Aftercare`-highlighted completed-state timeline is not evidenced |

**Extra Elements**:

- `PATIENT ID: HP202401` is shown in the header but is not a specified field for `P05.1-S3`

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 10/13 (77%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-02 Information priority`: the completed tab surfaces narrative note sections first, but the core case identity and estimate-vs-actual comparison are either missing or only available in sibling tabs | Add a concise completed-case summary block above the note sections so the patient immediately sees treatment identity, provider, date, and estimate-vs-actual graft context |

**Flow Coverage Gaps**:

- The source spec's popup-based day-detail interaction has been replaced by inline expanded day entries, so the design/spec should be aligned explicitly
- The completed-state tab still does not show the estimate-vs-actual comparison, terminal treatment-days summary, or an `Aftercare`-highlighted journey timeline

---

## Action Items

| Priority | Flow | Screen | Issue | Recommendation |
|----------|------|--------|-------|----------------|
| ⚠️ Important | P05.1 | P05.1-S2 | The designer replaced the popup detail with always-visible inline day details, but the spec still documents a popup-and-close interaction | Either update the spec to accept the inline pattern or add explicit expand/collapse affordances that preserve the intended focused-day interaction |
| ⚠️ Important | P05.1 | P05.1-S3 | The completed-state tab does not evidence the required estimate-vs-actual comparison, terminal treatment-days summary, or `Aftercare` timeline state | Expand the completed tab to show those completed-state-specific elements directly |
| ⚠️ UX Improvement | P05.1 | P05.1-S1 | Commercial quote/package content still dominates the top of the treatment tab and weakens treatment-progress scannability | Reorder and regroup the treatment tab so progress-critical information leads the layout |

### Priority Legend

- **🔴 Critical**: Blocks flow progression, breaks data integrity, or causes security/legal risk. Must fix before development.
- **🔴 Critical UX**: Severe usability issue that would prevent users from completing the flow or cause significant confusion. Must fix before development.
- **⚠️ Important**: Functional discrepancy that could cause user confusion or require rework during development. Should fix before development.
- **⚠️ UX Improvement**: Usability or design quality issue that deviates from platform conventions or best practices. Should fix before development.
- **💡 Suggestion**: Cosmetic or minor improvement. Can fix anytime.
- **💡 UX Suggestion**: Minor design enhancement that would improve polish. Can fix anytime.

---

## Notes

- Verification was requested for Flow `P05.1` only
- Source specification: `local-docs/reports/2026-02-05/missing-mobile-flows-design-complement.md`
- Related FR references: `local-docs/project-requirements/functional-requirements/fr010-treatment-execution/prd.md`, `local-docs/project-requirements/functional-requirements/fr011-aftercare-recovery-management/prd.md`
- Evidence reviewed: `layout-temp/in progress/Booking info.jpg`, `layout-temp/in progress/Provider.jpg`, `layout-temp/in progress/Treatment.jpg`, `layout-temp/in progress/End of Treatment.jpg`, and `layout-temp/in progress/Problem.jpg`
- User approval granted on 2026-03-24 to accept the remaining `P05.1` issues as minor for design sign-off
