# Design Layout Verification Report — FR-029

**Report Date**: 2026-04-02
**Report Type**: Design Layout Verification
**FR Scope**: FR-029 — Payment System Configuration
**Flow Scope**: Main Flow: Configure Currency Conversion Rules; Screen 2A and Screen 2B only
**Layout Source**: `layout-temp/`
**Platform**: Admin Web
**Status**: 🔴 BLOCKED

---

## Summary Dashboard

| # | Flow | Module | Screens Required | Screens Verified | Layout Status | Field Coverage |
|---|------|--------|-----------------|-----------------|---------------|----------------|
| 2 | Configure Currency Conversion Rules | A-09: System Settings & Configuration | 2 | 2 | 🔴 BLOCKED | ~70% |

**Overall**: 0 of 1 scoped flows verified. The scoped flow is BLOCKED because Screen 2B fails a mandatory auto-fetch step.
**Screens**: 2 of 2 specified screens have layouts (~100% layout coverage), but only 1 of 2 screens is implementation-ready.

---

## Layout File Inventory

### Mapped to Spec Flows

| Layout File | Maps to Flow | Maps to Screen |
|-------------|-------------|----------------|
| `layout-temp/Currency Conversion.jpg` | 2 | 2A (Currency Conversion — Pair List & Global Settings) |
| `layout-temp/Fulltable overview - Currency Pair.jpg` | 2 | 2A (Currency Conversion — Pair List & Global Settings) |
| `layout-temp/Add Pair - Rate mode Auto-fetch from soucre.jpg` | 2 | 2B (Add / Edit Currency Pair) |
| `layout-temp/Add Pair - Rate mode Manual Input.jpg` | 2 | 2B (Add / Edit Currency Pair) |

### Unmapped Files

| Layout File | Likely Purpose | Notes |
|-------------|---------------|-------|
| `layout-temp/Group 1000007778.jpg` | Unknown | Present in `layout-temp/` but not confidently mapped from filename alone |

---

## Detailed Verification by Flow

---

### Flow 2: Configure Currency Conversion Rules

**Status**: 🔴 BLOCKED — Screen 2A is partial and Screen 2B fails a critical auto-fetch requirement.
**Screens required**: 2
**Layout files**: `layout-temp/Currency Conversion.jpg`, `layout-temp/Fulltable overview - Currency Pair.jpg`, `layout-temp/Add Pair - Rate mode Auto-fetch from soucre.jpg`, `layout-temp/Add Pair - Rate mode Manual Input.jpg`

#### Screen 2A: Currency Conversion — Pair List & Global Settings

**Layout**: `layout-temp/Currency Conversion.jpg`, `layout-temp/Fulltable overview - Currency Pair.jpg`

##### Flow Context

- **User arrives from**: The admin clicks the `Currency Conversion` tab from Payment Configuration, per `prd.md` Main Flow: Configure Currency Conversion Rules (lines 127-140).
- **Screen purpose**: This is the central dashboard for global defaults, rate sources, and the configured currency-pair list, matching `prd.md` Screen 2A (lines 427-510).
- **Entry point**: Present. `Currency Conversion.jpg` shows the page title and breadcrumb `Settings / Payment Settings / Currency Conversion`, which aligns with the flow trigger.
- **Exit path**: Present. The layout exposes `Save Setting`, `Add Source`, and `Add Pair`, and the pair-row action menu in `Fulltable overview - Currency Pair.jpg` shows `Edit`, `Delete`, and `Sync Now`.
- **Data continuity**: Correct for this entry screen. No prior form data needs to carry in; the page instead surfaces current global settings, source health, and pair status.
- **Flow context issues**: Source-row actions are not fully legible in the static image, so `Delete Source` and `Test Connection` cannot be conclusively verified from the provided evidence.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Global Default Markup % | Yes | ✅ | Numeric input is visible in the `Global Settings` card in `layout-temp/Currency Conversion.jpg`, matching `prd.md` line 434. |
| Global Default Sync Frequency | Yes | ✅ | Select field is visible under Global Default Markup % in `layout-temp/Currency Conversion.jpg`, matching `prd.md` line 435. |
| Rate Protection Threshold | Yes | ✅ | Numeric input is visible in the same card in `layout-temp/Currency Conversion.jpg`, matching `prd.md` line 436. |
| Source Name | Yes | ✅ | `Rate Sources` table includes a `Source Name` column in `layout-temp/Currency Conversion.jpg`, matching `prd.md` line 452. |
| Provider Type | Yes | ✅ | `Provider Type` column is visible in `layout-temp/Currency Conversion.jpg`, matching `prd.md` line 453. |
| API Key | Yes | ✅ | `API Key` column is visible with masked credential values in `layout-temp/Currency Conversion.jpg`, matching `prd.md` line 454. |
| Status (source) | N/A | ✅ | `Status` health pills are visible in the `Rate Sources` table in `layout-temp/Currency Conversion.jpg`, matching `prd.md` line 455. |
| Last Tested | N/A | ✅ | `Last Tested` timestamps are visible in the `Rate Sources` table in `layout-temp/Currency Conversion.jpg`, matching `prd.md` line 456. |
| Pair | Yes | ✅ | `Pair` column is visible in both `layout-temp/Currency Conversion.jpg` and `layout-temp/Fulltable overview - Currency Pair.jpg`, matching `prd.md` line 476. |
| Mode | Yes | ✅ | `Mode` column is visible in `layout-temp/Fulltable overview - Currency Pair.jpg`, matching `prd.md` line 477. |
| Source (pair) | Yes | ✅ | `Source` column is visible in `layout-temp/Fulltable overview - Currency Pair.jpg`, matching `prd.md` line 478. |
| Base Rate | Yes | ✅ | `Base Rate` column is visible in both Screen 2A layouts, matching `prd.md` line 479. |
| Markup % | Yes | ✅ | `Markup %` column is visible in both Screen 2A layouts, matching `prd.md` line 480. |
| Effective Rate | Yes | ✅ | `Effective Rate` column is visible in both Screen 2A layouts, matching `prd.md` line 481. |
| Sync Frequency | Yes | ✅ | `Sync Freq` column is visible in both Screen 2A layouts, matching `prd.md` line 482. |
| Last Updated | Yes | ✅ | `Last Updated` column is visible in both Screen 2A layouts, matching `prd.md` line 483. |
| Status (pair) | Yes | ✅ | `Healthy`, `Degraded`, and `Error` status pills are visible in `layout-temp/Fulltable overview - Currency Pair.jpg`, matching `prd.md` line 484. |
| Info banner: USD fallback notice | Yes | ❌ | The required prominent banner described in `prd.md` line 502 is not visible in either Screen 2A layout. |
| Sorting and filtering on pair list | Yes | ❌⚠️ | Sort chevrons are visible on headers in `layout-temp/Fulltable overview - Currency Pair.jpg`, but no filter controls for pair/mode/status/last updated are visible, so the requirement in `prd.md` line 503 is only partially met. |
| Pair count summary | Yes | ❌⚠️ | `Total 80 Items` is visible at the bottom of the table in `layout-temp/Currency Conversion.jpg`, but the required mode breakdown such as `9 auto, 3 manual` from `prd.md` line 504 is not shown. |
| Alert badge count in tab/section header | Yes | ❌ | No alert badge count is visible in the tab or section header despite the requirement in `prd.md` line 505. |

**Extra Elements**:

- `layout-temp/Currency Conversion.jpg` includes a `Lorem ipsum` subtitle under the page title. This does not map to FR-029 and looks like placeholder copy rather than intentional product content.
- Standard admin sidebar navigation and page breadcrumb are present; these are useful context elements but are not explicitly defined in the screen field tables.

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 18/21 (86%)
**Critical Issues**: None. Core configuration fields and pair-list columns are present, but several specified supporting UI requirements are missing or only partially implemented.

##### UX/UI Design Evaluation

**Skills invoked**: ui-ux-pro-max, web-design-guidelines

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-17` CTA label clarity: the global-settings action is labeled `Save Setting`, which is ambiguous on a page with multiple configurable areas. Evidence: `layout-temp/Currency Conversion.jpg` shows the green button inside the Global Settings card. | Rename the button to `Save Global Settings` so the action scope is explicit. |
| ⚠️ UX Improvement | `W-06` Table design: the pair list shows sortable columns and pagination, but no visible filtering controls even though this screen is expected to support filtering by pair, mode, status, and last updated. Evidence: `layout-temp/Currency Conversion.jpg` and `layout-temp/Fulltable overview - Currency Pair.jpg`. | Add visible filter controls above the pair table or in a table toolbar. |
| 💡 UX Suggestion | `U-23` Terminology consistency: the section heading reads `Currency Pair` while the content is a multi-row table of many pairs. Evidence: `layout-temp/Currency Conversion.jpg`. | Rename the section to `Currency Pairs` to better match the content and reduce minor wording friction. |

#### Screen 2B: Add / Edit Currency Pair

**Layout**: `layout-temp/Add Pair - Rate mode Auto-fetch from soucre.jpg`, `layout-temp/Add Pair - Rate mode Manual Input.jpg`

##### Flow Context

- **User arrives from**: The admin clicks `Add Pair` from Screen 2A, per `prd.md` Main Flow: Configure Currency Conversion Rules step 6 (line 141).
- **Screen purpose**: The form should let the admin create or edit one USD-to-target pair, choose auto-fetch vs manual mode, preview the effective rate, and return to Screen 2A after saving, matching `prd.md` Screen 2B (lines 513-568).
- **Entry point**: Present. Both layouts clearly show the `Add Pair` form title with the expected core fields.
- **Exit path**: Partial. `Cancel` and a green primary `Add` button are visible in both layouts, but the required `Test Connection & Fetch Rate` step for auto-fetch mode is missing, so the auto path cannot be validated against the flow.
- **Data continuity**: Partial. The auto-fetch layout shows a `Source` dropdown that should be populated from sources defined on Screen 2A, but the static design does not show source status or the fetched-rate confirmation that the spec requires.
- **Flow context issues**: Auto mode omits the mandatory fetch/test step, and manual mode still shows `Sync Frequency` even though the spec says it should be hidden when rate mode is manual.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Base Currency | N/A | ❌⚠️ | The field shows fixed value `USD`, but it is styled like a selectable dropdown with a chevron in both layouts. `prd.md` line 519 requires display-only fixed USD. |
| Target Currency | Yes | ✅ | Select field is visible in both layouts, matching `prd.md` line 520. |
| Rate Mode | Yes | ✅ | Auto-fetch/manual radio options are visible in both layouts, matching `prd.md` line 521. |
| Source | Conditional | ✅ | Visible in the auto-fetch layout and hidden in the manual layout, matching `prd.md` lines 522 and 556. |
| Manual Base Rate | Conditional | ✅ | Hidden in the auto-fetch layout and visible in the manual layout, matching `prd.md` lines 523 and 553-556. |
| Markup % | No | ✅ | Numeric input is visible in both layouts, matching `prd.md` line 524. |
| Sync Frequency | No | ❌⚠️ | The field is correctly visible in auto-fetch mode, but it remains visible in the manual layout even though `prd.md` line 557 says it should be hidden / not applicable in manual mode. |
| Effective Rate | N/A | ✅ | `Effective Rate: N/A` preview is visible in both layouts, matching `prd.md` line 526. |
| Test Connection & Fetch Rate | Yes (auto-fetch) | ❌ | No `Test Connection & Fetch Rate` action is visible anywhere in the auto-fetch layout, despite `prd.md` line 529 and lines 548-550 making it mandatory before save. This is a critical flow blocker. |
| Save / submit action | Yes | ⚠️ | A green primary action exists, but it is labeled `Add` instead of `Save`. On a create state this is functionally close, but it also appears available without the mandatory fetch-test step. |
| Cancel | Yes | ✅ | `Cancel` button is visible in both layouts, matching `prd.md` line 531. |
| Inline help text for base rate meaning | Yes | ❌ | The explanatory help text required in `prd.md` line 563 is not visible in either layout. |
| Source status indicator near dropdown | Yes (auto-fetch) | ❌ | The auto-fetch layout does not show the source health indicator required by `prd.md` line 564. |
| Estimated conversion rate impact | Yes | ❌ | No explanatory preview such as `5% markup on 0.92 USD/EUR = 0.966 effective rate` is visible, despite `prd.md` line 565. |
| Last sync and next scheduled sync | Yes (auto-fetch) | ❌ | No timestamps or scheduling hint are visible below the auto-fetch form, despite `prd.md` line 566. |
| Rate History link / section | Conditional (edit only) | ✅ | Not required in the provided add-state layouts; acceptable absence per `prd.md` line 567. |

**Extra Elements**:

- The numeric inputs show plus/minus steppers, which are not explicitly called out in the FR but are compatible with number-entry controls.
- No separate `Edit Pair` state is provided, so edit-only affordances could not be verified beyond the add-state layout.

**Screen Status**: 🔴 FAIL
**Field Coverage**: 8/15 (53%)
**Critical Issues**: Missing `Test Connection & Fetch Rate` in auto-fetch mode; manual mode incorrectly keeps `Sync Frequency` visible; base currency is styled as editable instead of display-only.

##### UX/UI Design Evaluation

**Skills invoked**: ui-ux-pro-max, web-design-guidelines

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| 🔴 Critical UX | `U-01` and `U-17`: the auto-fetch layout makes `Add` the primary action but does not show the mandatory `Test Connection & Fetch Rate` step first. This can lead the admin toward the wrong next action and obscures the gating rule required by the flow. Evidence: `layout-temp/Add Pair - Rate mode Auto-fetch from soucre.jpg`. | Add a distinct `Test Connection & Fetch Rate` button above the primary save action and keep the save action disabled until the fetch succeeds. |
| ⚠️ UX Improvement | `U-16`: `Base Currency` appears as an editable dropdown because it uses a select-style field with a chevron, even though the value must be fixed to USD. Evidence: both `Add Pair` layouts show the chevron on the `USD` field. | Restyle `Base Currency` as read-only text or a disabled field without a dropdown affordance. |
| ⚠️ UX Improvement | `U-03` and `W-05`: manual mode still shows `Sync Frequency`, which is unrelated in this state and increases cognitive load. Evidence: `layout-temp/Add Pair - Rate mode Manual Input.jpg`. | Hide `Sync Frequency` whenever `Rate Mode = Manual`, and tighten the form layout around only relevant inputs. |
| 💡 UX Suggestion | `U-11`: the form omits the inline explanatory copy for what the base rate means, even though the screen relies on financial terminology. Evidence: neither add-state layout shows helper text under `Manual Base Rate` or `Target Currency`. | Add the spec's helper copy to reduce ambiguity around rate semantics. |

**Flow Coverage Gaps**:

- No dedicated layout for `Test Connection & Fetch Rate` success state or fetched-rate confirmation.
- No edit-state layout to verify `Rate History`, auto-to-manual mode switching, or pre-filled data behavior.
- Source-row actions on Screen 2A are too low-resolution to confirm `Delete Source` and `Test Connection`.

---

## Action Items

| Priority | Flow | Screen | Issue | Recommendation |
|----------|------|--------|-------|----------------|
| 🔴 Critical | 2 | 2B | Auto-fetch mode is missing the mandatory `Test Connection & Fetch Rate` step required before save. | Add a dedicated fetch-test action, surface the fetched-rate confirmation, and keep the primary save action disabled until the test succeeds. |
| 🔴 Critical UX | 2 | 2B | The green primary `Add` CTA is shown before the required fetch-test step, which encourages the wrong next action. | Rework the auto-fetch state so the fetch-test step is visually primary until it succeeds, then enable save. |
| ⚠️ Important | 2 | 2B | `Sync Frequency` remains visible in manual mode even though the FR says it is hidden / not applicable. | Hide `Sync Frequency` whenever `Rate Mode = Manual`. |
| ⚠️ Important | 2 | 2B | `Base Currency` is styled like an editable dropdown instead of a fixed display-only USD field. | Restyle the field as read-only text or a disabled input without a chevron. |
| ⚠️ Important | 2 | 2A | The required USD fallback info banner is missing from the currency-pair dashboard. | Add the specified banner explaining that unconfigured currencies default to USD for payment collection. |
| ⚠️ Important | 2 | 2A | Pair-list support requirements are incomplete: no visible filters, no auto/manual count breakdown, and no alert badge count. | Add a table toolbar with filters plus a summary/header area for pair counts and alert badges. |
| 💡 Suggestion | 2 | 2A | Placeholder `Lorem ipsum` copy is still visible under the page title. | Replace the placeholder subtitle with production-ready explanatory text or remove it. |
| 💡 UX Suggestion | 2 | 2A | The heading `Currency Pair` is singular even though the section lists many pairs. | Rename the section to `Currency Pairs`. |

### Priority Legend

- **🔴 Critical**: Blocks flow progression, breaks data integrity, or causes security/legal risk. Must fix before development.
- **🔴 Critical UX**: Severe usability issue that would prevent users from completing the flow or cause significant confusion. Must fix before development.
- **⚠️ Important**: Functional discrepancy that could cause user confusion or require rework during development. Should fix before development.
- **⚠️ UX Improvement**: Usability or design quality issue that deviates from platform conventions or best practices. Should fix before development.
- **💡 Suggestion**: Cosmetic or minor improvement. Can fix anytime.
- **💡 UX Suggestion**: Minor design enhancement that would improve polish. Can fix anytime.

---

## Notes

- Verification scope limited to Screen 2A and Screen 2B of FR-029.
- Requirement source: `local-docs/project-requirements/functional-requirements/fr029-payment-system-config/prd.md`
- Layout inventory based on files currently present under `layout-temp/`.
- Review performed against static JPG layouts only; interaction-only behavior was evaluated only when the required control was visibly represented.
- `layout-temp/Group 1000007778.jpg` was left unmapped because its filename did not provide enough evidence to tie it to Screen 2A or 2B.
