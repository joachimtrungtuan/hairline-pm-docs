# Design Layout Verification Report - FR-021 Screen 2 to Screen 10

**Report Date**: 2026-06-04
**Report Type**: Design Layout Verification
**FR Scope**: FR-021 - Multi-Language & Localization
**Screen Scope**: Screen 2 through Screen 10 (expanded in place from original Screen 3-10 scope)
**Processing Granularity**: Screen by screen
**Layout Source**: `layout-temp/`
**Platform**: Provider Web + Admin Web
**Status**: 🔴 FAIL - all requested screens have layouts, but Screen 8 and Screen 9 contain critical publish-control issues, and several screens need terminology/field-coverage corrections before development handoff.

---

## Summary Dashboard

| # | Flow | Module | Screens Required | Screens Verified | Layout Status | Field Coverage |
|---|------|--------|-----------------|-----------------|---------------|----------------|
| Provider/Admin Localization Management | Screen 2 Provider selector + Screen 3-10 Admin localization operations | PR-06 + A-09: Profile & Settings / System Settings & Configuration | 9 | 9 | 🔴 FAIL | ~98% |

**Overall**: 9 of 9 requested Provider/Admin Web screens have layout coverage. 1 screen fails because publish action appears available in an invalid state; Screen 8 remains partial with a critical publish-summary control issue.
**Screens**: 9 of 9 specified screens have layouts (100% layout coverage). Screen statuses: 6 GOOD, 2 PARTIAL, 1 FAIL.
**Critical field/UX issues**: 2

---

## Layout File Inventory

### Mapped to Spec Screens

| Layout File | Maps to Flow | Maps to Screen | Notes |
|-------------|-------------|----------------|-------|
| `layout-temp/Top-Bar Language Selector (Provider).jpg` | A1: User Selects Language | Screen 2 (Provider Dashboard - Top-Bar Language Selector) | Provider dashboard language-selector state. |
| `layout-temp/Hairline Overview (Admin).jpg` | A1: User Selects Language | Screen 3 (Admin Platform - Top-Bar Language Selector) | Preliminary mapping by filename/content area; verify during Screen 3 analysis. |
| `layout-temp/Localization - Language List.jpg` | Main Flow: Admin Updates and Publishes Translation Version | Screen 4 (Admin - Localization Dashboard & Language Management) | Preliminary mapping by filename. |
| `layout-temp/Full Table.jpg` | Main Flow: Admin Updates and Publishes Translation Version | Screen 4 (Admin - Localization Dashboard & Language Management) | Full table variant showing native name and direction columns. |
| `layout-temp/Language Detail.jpg` | Main Flow: Admin Updates and Publishes Translation Version | Screen 5 (Admin - Language Detail) | Preliminary mapping by filename. |
| `layout-temp/Translation Key Inventor.jpg` | Main Flow: Admin Updates and Publishes Translation Version | Screen 6 (Admin - Translation Key Inventory) | Main key-inventory screen. Local filename is stale, but the revised user-provided Screen 6 screenshot shows the tab corrected to `Translation Key Inventory` and language filter corrected to `Turkish (tr)`. |
| `layout-temp/Full Table-2.jpg` | Main Flow: Admin Updates and Publishes Translation Version | Screen 6 (Admin - Translation Key Inventory) | Full-table variant showing Screen / Context, English Source Value, and Selected-Language Value columns. |
| `layout-temp/Translation Key Detail Editor.jpg` | Main Flow: Admin Updates and Publishes Translation Version | Screen 7 (Admin - Translation Key Detail Editor) | Preliminary mapping by filename. |
| `layout-temp/JSON Import.jpg` | Main Flow: Admin Updates and Publishes Translation Version | Screen 8 (Admin - JSON Import Modal/Screen) | Preliminary mapping by filename. |
| `layout-temp/Language Version History & Rollback.jpg` | Main Flow: Admin Updates and Publishes Translation Version | Screen 9 (Admin - Language Version History & Rollback) | Preliminary mapping by filename. |
| `layout-temp/Compare Versions.jpg` | Main Flow: Admin Updates and Publishes Translation Version | Screen 9 (Admin - Language Version History & Rollback) | Likely comparison/rollback variant for Screen 9. |
| `layout-temp/Compare Versions-1.jpg` | Main Flow: Admin Updates and Publishes Translation Version | Screen 9 (Admin - Language Version History & Rollback) | Likely comparison/rollback variant for Screen 9. |
| `layout-temp/Machine Translation Provider And Draft Generation.jpg` | C1: Machine Translation Draft Generation | Screen 10 (Admin - Machine Translation Provider & Draft Generation) | Preliminary mapping by filename. |

### Unmapped Files

| Layout File | Likely Purpose | Notes |
|-------------|---------------|-------|
| `layout-temp/Full Table-1.jpg` | Machine-translation job-history table variant | Inspected during Screen 6 pass; content matches Screen 10-style job history rather than Screen 6 key inventory. Not used for field coverage. |
| `layout-temp/Full Table-3.jpg` | Table variant | Not used as primary evidence; no screen-specific mapping needed after named Screen 2-10 layouts covered the scope. |

---

## Detailed Verification by Flow

---

### Flow: Provider/Admin Localization Management - Screen 2 to Screen 10

**Status**: 🔴 FAIL - all screens have matching layouts, but publish-without-summary controls must be corrected.
**Screens required**: 9
**Layout files**: `Top-Bar Language Selector (Provider).jpg`, `Hairline Overview (Admin).jpg`, `Localization - Language List.jpg`, `Language Detail.jpg`, `Translation Key Inventor.jpg`, `Full Table-2.jpg`, `Translation Key Detail Editor.jpg`, `JSON Import.jpg`, `Language Version History & Rollback.jpg`, `Compare Versions*.jpg`, `Machine Translation Provider And Draft Generation.jpg`

#### Screen 2: Provider Dashboard - Top-Bar Language Selector

**Layout**: `layout-temp/Top-Bar Language Selector (Provider).jpg`

##### Flow Context

- **User arrives from**: Any Provider Dashboard workflow where the persistent top bar is visible; A1 starts when the provider opens the tenant-specific language selector.
- **Screen purpose**: Allow provider users to switch Provider Dashboard interface language without leaving their current workflow.
- **Entry point**: Present. The language selector is visible in the top-right top bar near provider account/profile controls.
- **Exit path**: Present as selectable language options in the open dropdown; no separate save/apply button is visible, so the design implies auto-apply.
- **Data continuity**: Correct at layout level. The selector appears over an active Provider Dashboard view with sidebar, dashboard filters, inbox table, and current account context intact.
- **Flow context issues**: Static JPG cannot verify preference persistence, bundle fetch, refresh/re-render behavior, or fallback behavior if a selected locale becomes inactive.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Current language | Yes | ✅ | Top-right selector shows UK flag and `English` with chevron. Proof: layout `Top-Bar Language Selector (Provider).jpg`; spec Screen 2 data field `Current language`, line 267. |
| Available languages | Yes | ⚠️ | Open dropdown shows readable language options with flags, including English, Turkce, Arabic, Deutsch, Francais, Espanol, Russian, Chinese, Korean, Portuguese, Italiano, Nederlands, Japanese, Persian, and Ukrainian. Proof: layout `Top-Bar Language Selector (Provider).jpg`; spec Screen 2 data field `Available languages`, line 268. Static image cannot prove inactive locales are hidden. |
| Save/apply action | Yes | ⚠️ | No explicit Save/Apply button is visible; selectable dropdown options imply auto-apply, which the spec allows. Proof: layout `Top-Bar Language Selector (Provider).jpg`; spec Screen 2 data field `Save/apply action`, line 269. Static image cannot verify preference persistence before refresh/re-render. |

**Extra Elements**:

- Provider dashboard shell, sidebar, account control, country filter, dashboard metrics, and inquiry table are visible. These are standard context elements and support route/task preservation.

**Screen Status**: 🟢 GOOD
**Field Coverage**: 3/3 (100%; two fields have static-image behavior limits)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`
**Platform checks applied**: Universal + Web

| Rule ID | Check | Severity | Finding | Evidence |
|---|---|---|---|---|
| W-10 | Keyboard accessibility indicators | ⚠️ UX Improvement | Focus state and keyboard behavior for the dropdown cannot be verified from the static JPG. | `Top-Bar Language Selector (Provider).jpg` shows open dropdown but no focus/keyboard state variant. |
| U-15 | Color not sole indicator | 💡 UX Suggestion | Current selected language is clear in the trigger, but selected state inside the open dropdown is subtle and may rely mainly on text styling. | `Top-Bar Language Selector (Provider).jpg` shows `English` in the menu without a strong selected marker such as checkmark/background. |

#### Screen 3: Admin Platform - Top-Bar Language Selector

**Layout**: `layout-temp/Hairline Overview (Admin).jpg`

##### Flow Context

- **User arrives from**: Any Admin Platform context where the persistent top bar is visible; A1 starts when the admin opens the tenant-specific language selector.
- **Screen purpose**: Allow the admin to change Admin Platform UI language while staying in the current administrative context.
- **Entry point**: Present. The language selector is visible in the top-right global top bar near profile/session controls.
- **Exit path**: Present as selectable language options in the open dropdown; no separate apply button is visible, so the design implies auto-apply.
- **Data continuity**: Correct at layout level. The selector appears inside the persistent Admin shell over an existing Hairline Overview page, supporting context preservation.
- **Flow context issues**: Static JPG cannot verify whether selecting a language persists preference, fetches the latest published admin bundle, or re-renders localized text.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Current language | Yes | ✅ | Visible as `English` in the top-right top-bar selector with a flag and chevron. Proof: layout `Hairline Overview (Admin).jpg`; spec Screen 3 data field `Current language`, line 298. |
| Available languages | Yes | ⚠️ | Open dropdown shows language options with flags, including English, Turkce, Arabic, Deutsch, Francais, Espanol, Russian, Chinese, Korean, Portuguese, Italiano, Nederlands, Japanese, Persian, and Ukrainian. Proof: layout `Hairline Overview (Admin).jpg`; spec Screen 3 data field `Available languages`, line 299. Minor limitation: the static image cannot prove inactive locales are hidden, and the PRD states initial supported languages are English and Turkish while additional languages are expandable. |
| Apply action | Yes | ⚠️ | No explicit Apply/Save button is visible; the open dropdown implies auto-apply on option selection, which the spec allows. Proof: layout `Hairline Overview (Admin).jpg`; spec Screen 3 data field `Apply action`, line 300. Static image cannot verify actual persistence behavior. |

**Extra Elements**:

- Global Admin navigation, search, help, notification, profile dropdown, sidebar, and Hairline Overview table are visible. These are standard shell/context elements and support the PRD note that the selector lives in the top bar near profile/session controls.

**Screen Status**: 🟢 GOOD
**Field Coverage**: 3/3 (100%; two fields have static-image verification limits)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`
**Platform checks applied**: Universal + Web

| Rule ID | Severity | Observation | Recommendation |
|---------|----------|-------------|----------------|
| W-10 | UX Improvement | Focus state and keyboard navigation for the dropdown cannot be verified from the static JPG. This matters because the fetched Web Interface Guidelines require visible focus states and keyboard support for interactive controls. Evidence: layout `Hairline Overview (Admin).jpg` shows the control visually, but no state variants are provided. | Provide an additional focused/keyboard state or implementation note confirming focus-visible styling and keyboard operation. |
| U-15 | UX Suggestion | The current selected option inside the open dropdown does not appear visually distinguished from other language options; the selected language is only clear from the closed trigger. Evidence: `English` in the dropdown appears same weight/background as neighboring language options in `Hairline Overview (Admin).jpg`. | Add a checkmark, selected background, or text state so current selection is not communicated only by the trigger. |

#### Screen 4: Admin - Localization Dashboard & Language Management

**Layout**: `layout-temp/Localization - Language List.jpg`

##### Flow Context

- **User arrives from**: Admin opens Localization Management from Settings > Localization.
- **Screen purpose**: Provide the localization landing dashboard where Admin manages available languages/locales and release readiness across tenants.
- **Entry point**: Present. Sidebar highlights Settings > Localization; main content title and Language List tab are visible.
- **Exit path**: Present. Tabs and row actions provide routes to key inventory/version history, while language rows imply navigation to Screen 5.
- **Data continuity**: Correct across the default and full-table variants. The screen shows locale readiness, native names, direction metadata, and version data.
- **Flow context issues**: None blocking in the revised Screen 4 screenshot. The opened `Deactivate` action is no longer shown on the default `en` row.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Language list | Yes | ✅ | Table titled `Language List` is visible. Proof: layout `Localization - Language List.jpg`; spec Screen 4 data field `Language list`, line 324. |
| Locale code | Yes | ✅ | `Locale Code` column is visible with values including `en`, `tr`, `az`, `de`, `fr`, `es`, `ru`, `zh`, `ko`, `pt`. Proof: layout `Localization - Language List.jpg`; spec Screen 4 data field `Locale code`, line 325. |
| English name | Yes | ✅ | `English Name` column is visible with values including English, Turkish, Arabic, German, French, Spanish, Russian, Chinese (Simplified), Korean, Portuguese. Proof: layout `Localization - Language List.jpg`; spec Screen 4 data field `English name`, line 326. |
| Native name | Yes | ✅ | `Native Name` column is visible in the full-table variant with values including English, Turkce, Arabic script, Deutsch, Francais, Espanol, Russian, Chinese, Korean, and Portuguese. Proof: layout `Full Table.jpg`; spec Screen 4 data field `Native name`, line 327. |
| Direction | Yes | ✅ | `Direction` column is visible in the full-table variant with LTR/RTL badges. Proof: layout `Full Table.jpg`; spec Screen 4 data field `Direction`, line 328. |
| Status | Yes | ✅ | `Status` column is visible with badge values including Active, Inactive, and Preparation. Proof: layout `Full Table.jpg`; spec Screen 4 data field `Status`, line 329. |
| Default locale | Yes | ✅ | `Default Locale` column is visible; `en` row shows a `Default` badge and other rows show dashes. Proof: layout `Localization - Language List.jpg`; spec Screen 4 data field `Default locale`, line 330. |
| Tenant coverage | No | ✅ | `Tenant Coverage` group is visible with Patient, Provider, and Admin percentage columns. Proof: layout `Localization - Language List.jpg`; spec Screen 4 data field `Tenant coverage`, line 331. |
| Last published version | No | ✅ | `Last Published Version` column is visible with values like `v12 - all surfaces`, `v8 - patient, provider`, and `Not published`. Proof: layout `Localization - Language List.jpg`; spec Screen 4 data field `Last published version`, line 332. |
| Add language action | Yes | ✅ | `Add Language` button with plus icon is visible. Proof: layout `Localization - Language List.jpg`; spec Screen 4 data field `Add language action`, line 333. |
| Remove/deactivate action | Conditional | ✅ | Revised Screen 4 screenshot shows `Deactivate` spelled correctly on a non-default language row, while the `en` row remains marked `Default`. This satisfies the conditional deactivate action while preserving default-locale protection in the visible state. Proof: user-provided revised Screen 4 screenshot; spec Screen 4 data field `Remove/deactivate action`, line 334 and business rules lines 339, 347. |

**Extra Elements**:

- Main content tabs: `Language List`, `Translation Key Inventor`, and `Language Version History & Rollback`. These support in-scope navigation, though `Inventor` appears to be a typo for `Inventory`.
- Pagination controls and item count (`Total 85 items`, page selector) are present; useful for a large language catalog.
- Global Admin shell elements are present and consistent with the Admin Platform.

**Screen Status**: 🟢 GOOD
**Field Coverage**: 9/9 required/conditional fields acceptable at layout level (100%); remaining issue is a non-blocking tab-label typo.
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`
**Platform checks applied**: Universal + Web

| Rule ID | Severity | Observation | Recommendation |
|---------|----------|-------------|----------------|
| U-23 | UX Improvement | The layout uses `Translation Key Inventor`, while the PRD uses `Translation Key Inventory`. Evidence: layout `Localization - Language List.jpg`; spec Screen 6 heading line 389. | Correct terminology to `Inventory` for consistency across the flow. |

#### Screen 5: Admin - Language Detail

**Layout**: `layout-temp/Language Detail.jpg`

##### Flow Context

- **User arrives from**: Screen 4 by selecting a language row, here Turkish (`tr`).
- **Screen purpose**: Provide one language's working hub for coverage, draft status, edit/import/export routes, version history, and machine translation.
- **Entry point**: Present. Breadcrumb shows `Setting / Localization / Turkish (tr)` and the page header is Turkish-specific.
- **Exit path**: Present. The screen offers `Edit Keys`, `Import JSON`, `Export JSON`, `Version History`, `Machine Translation`, and `Back to Language List`.
- **Data continuity**: Correct. Actions and copy preserve Turkish context in descriptions such as "for Turkish" and "Opens filtered to this language."
- **Flow context issues**: None blocking.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Language header | Yes | ✅ | Header shows `Turkish`, native name `Turkce`, locale badge `tr`, direction badge `LTR`, and status badge `Active`. Proof: layout `Language Detail.jpg`; spec Screen 5 data field `Language header`, line 363. |
| Tenant coverage | Yes | ✅ | Tenant Coverage section shows Patient App 87%, Provider Dashboard 74%, Admin Platform 41%, and Shared / Notification 20% with progress bars. Proof: layout `Language Detail.jpg`; spec Screen 5 data field `Tenant coverage`, line 364. |
| Pending draft changes | No | ✅ | `Pending Draft Changes` card shows `12` changes awaiting publish. Proof: layout `Language Detail.jpg`; spec Screen 5 data field `Pending draft changes`, line 365. |
| Missing keys | No | ✅ | `Missing Keys` card shows `38` keys without Turkish value. Proof: layout `Language Detail.jpg`; spec Screen 5 data field `Missing keys`, line 366. |
| Review-needed keys | No | ✅ | Revised Screen 5 screenshot shows `Review-Needed Keys` with count `5` and description `keys requiring review after source changes`, which distinguishes review-needed translations from missing translations. Proof: user-provided revised Screen 5 screenshot; spec Screen 5 data field `Review-needed keys`, line 367. |
| Edit keys route | Yes | ✅ | `Edit Keys` action card is visible and states it opens the key inventory filtered to Turkish. Proof: layout `Language Detail.jpg`; spec Screen 5 data field `Edit keys route`, line 368. |
| Import JSON route | Yes | ✅ | `Import JSON` action card is visible and states upload/validate/import for Turkish. Proof: layout `Language Detail.jpg`; spec Screen 5 data field `Import JSON route`, line 369. |
| Export JSON action | No | ✅ | `Export JSON` card includes surface dropdown, published/latest dropdown, and `Export JSON` button; it describes translator handoff/backup/review and no state modification. Proof: layout `Language Detail.jpg`; spec Screen 5 data field `Export JSON action`, line 370. |
| Version history route | Yes | ✅ | `Version History` action card is visible and mentions published versions, publishing draft changes, prior bundles, and rollback. Proof: layout `Language Detail.jpg`; spec Screen 5 data field `Version history route`, line 371. |
| Machine translation route | Conditional | ✅ | `Machine Translation` action card is visible for Turkish, a non-English target language. Proof: layout `Language Detail.jpg`; spec Screen 5 data field `Machine translation route`, line 372. |

**Extra Elements**:

- `Back to Language List` button is present and supports navigation back to Screen 4.
- Global Admin shell, search, notifications, user profile, and language selector are present.
- The action grid leaves an empty sixth card slot/blank area, likely from a fixed 3-column layout.

**Screen Status**: 🟢 GOOD
**Field Coverage**: 9/9 required/conditional fields acceptable at layout level (100%).
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`
**Platform checks applied**: Universal + Web

| Rule ID | Severity | Observation | Recommendation |
|---------|----------|-------------|----------------|
| U-16 | UX Suggestion | Action cards rely mostly on an up-right arrow icon to communicate clickability. Evidence: `Language Detail.jpg` cards for Edit Keys, Import JSON, Version History, and Machine Translation. | Ensure full-card hover/focus states are visible in implementation or provide clearer button affordances. |
| W-02 | UX Suggestion | The fixed 3-column action grid leaves an empty slot after five action cards, which can look unfinished on desktop. Evidence: `Language Detail.jpg` Actions section. | Let the grid wrap naturally or balance the final row when there are five cards. |

#### Screen 6: Admin - Translation Key Inventory

**Layout**: `layout-temp/Translation Key Inventor.jpg`, `layout-temp/Full Table-2.jpg`

##### Flow Context

- **User arrives from**: Screen 5 via `Edit Keys`, or from the Localization main tabs.
- **Screen purpose**: Browse translation keys by tenant surface and open a selected key for detail editing.
- **Entry point**: Present. Main localization tab is selected, and tenant sub-tabs are visible.
- **Exit path**: Present. Row action menu includes `View`, which appears to open key detail.
- **Data continuity**: Correct in the revised Screen 6 screenshot. The language filter preserves Turkish context and displays `Turkish (tr)`.
- **Flow context issues**: None blocking after the full-table variant. `Full Table-2.jpg` shows source/context and selected-language value columns needed for comparison before opening a key.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Tenant sub-screen | Yes | ✅ | Tenant tabs `Patient App`, `Provider Dashboard`, and `Admin Platform` are visible, with Patient App selected. Proof: layout `Translation Key Inventor.jpg`; spec Screen 6 data field `Tenant sub-screen`, line 398. |
| Selected language filter | No | ✅ | Language dropdown is visible and displays `Turkish (tr)` in the revised Screen 6 screenshot. Proof: user-provided revised Screen 6 screenshot; spec Screen 6 data field `Selected language filter`, line 399. |
| Namespace/group | Yes | ✅ | Namespace dropdown and `Namespace` table column are visible. Row examples include `common`, `auth`, `settings.language`, `profile`, and `inquiry`. Proof: layout `Translation Key Inventor.jpg`; spec Screen 6 data field `Namespace/group`, line 400. |
| Key pattern / key | Yes | ✅ | `Key` column is visible with stable key examples such as `common.save`, `auth.login.title`, and `settings.language.fallback_notice`. Proof: layout `Translation Key Inventor.jpg`; spec Screen 6 data field `Key pattern / key`, line 401. |
| Screen/context | No | ✅ | `Screen / Context` column is visible in the full-table variant with examples such as `Global - all screens`, `Login screen - page title`, and `Settings - Language & Region`. Proof: layout `Full Table-2.jpg`; spec Screen 6 data field `Screen/context`, line 402. |
| English source value | Conditional | ✅ | `English Source Value` column is visible in the full-table variant with values such as `Save`, `Loading...`, `Sign In`, and `Language & Region`. Proof: layout `Full Table-2.jpg`; spec Screen 6 data field `English source value`, line 403. |
| Selected-language value | Conditional | ✅ | `Selected-Language Value` column is visible in the full-table variant with translated/missing values such as `Kaydet`, `Giris Yap`, `Dil & Bolge`, and `-- missing`. Proof: layout `Full Table-2.jpg`; spec Screen 6 data field `Selected-language value`, line 404. |
| Coverage/status | Yes | ✅ | `Coverage/Status` column is visible with badges such as Published, Missing, and Draft. Proof: layout `Translation Key Inventor.jpg`; spec Screen 6 data field `Coverage/status`, line 405. |
| Source value owner | No | ✅ | `Source Value Owner` column is visible with values such as `P-00 / common`, `FR-001`, and `FR-021`. Proof: layout `Translation Key Inventor.jpg`; spec Screen 6 data field `Source value owner`, line 406. |
| Required at launch | Yes | ✅ | `Required at Launch` column is visible with values such as `P1` and `P2`. Proof: layout `Translation Key Inventor.jpg`; spec Screen 6 data field `Required at launch`, line 407. |
| Flexibility status | Yes | ✅ | `Flexibility Status` column is visible with `Baseline` values. Proof: layout `Translation Key Inventor.jpg`; spec Screen 6 data field `Flexibility status`, line 408. |
| Open key action | Yes | ✅ | `Action` column is visible; opened row menu shows `View`, which functions as the open-key route. Proof: layout `Translation Key Inventor.jpg`; spec Screen 6 data field `Open key action`, line 409. |

**Extra Elements**:

- Filters for Status and free-text search are present and useful.
- Revised Screen 6 screenshot shows the main tab corrected to `Translation Key Inventory`.
- `Full Table-2.jpg` provides the expanded table state for source/context and source/target value review.
- Files `Full Table.jpg`, `Full Table-1.jpg`, and `Full Table-3.jpg` are other table variants; `Full Table.jpg` supports Screen 4, `Full Table-1.jpg` matches Screen 10-style job history, and `Full Table-3.jpg` supports Screen 9 version history.

**Screen Status**: 🟢 GOOD
**Field Coverage**: 9/9 required/conditional fields acceptable at layout level (100%).
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`
**Platform checks applied**: Universal + Web

| Rule ID | Severity | Observation | Recommendation |
|---------|----------|-------------|----------------|
| W-06 | UX Suggestion | `P1`, `P2`, and `Baseline` are compact governance labels without visible legend. Evidence: `Translation Key Inventor.jpg` table columns `Required at Launch` and `Flexibility Status`. | Add tooltips, a legend, or expanded labels for launch priority and flexibility status. |
| U-22 | UX Suggestion | Main tabs use pill styling while tenant sub-tabs use underline styling; this is understandable but visually mixed in a dense data screen. Evidence: `Translation Key Inventor.jpg`. | Keep the hierarchy but standardize spacing/scale so primary and secondary tabs feel intentionally related. |

#### Screen 7: Admin - Translation Key Detail Editor

**Layout**: `layout-temp/Translation Key Detail Editor.jpg`

##### Flow Context

- **User arrives from**: Screen 6 row action / open key route.
- **Screen purpose**: Review one translation key and save per-language edits as draft.
- **Entry point**: Present. Page title is `Translation Key Detail Editor` and back button returns to `Translation Key Inventor`.
- **Exit path**: Present. `Save Draft` and `Cancel` actions are visible.
- **Data continuity**: Present. Key identity preserves `auth.login.title`, Patient App tenant/surface, `auth` namespace, and Turkish language value.
- **Flow context issues**: The layout does not show all active language values; it shows English source plus Turkish only.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Translation key | Yes | ✅ | `Translation Key` field shows `auth.login.title`. Proof: layout `Translation Key Detail Editor.jpg`; spec Screen 7 data field `Translation key`, line 497. |
| Tenant/surface | Yes | ✅ | `Tenant / Surface` field shows `Patient App`. Proof: layout `Translation Key Detail Editor.jpg`; spec Screen 7 data field `Tenant/surface`, line 498. |
| Group/namespace | Yes | ✅ | `Group / Namespace` field shows `auth`. Proof: layout `Translation Key Detail Editor.jpg`; spec Screen 7 data field `Group/namespace`, line 499. |
| Screen/context | No | ✅ | `Screen / Context` field shows `Login screen - page title`. Proof: layout `Translation Key Detail Editor.jpg`; spec Screen 7 data field `Screen/context`, line 500. |
| Description/context | No | ✅ | `Description / Context` textarea explains the login heading usage and line-length guidance. Proof: layout `Translation Key Detail Editor.jpg`; spec Screen 7 data field `Description/context`, line 501. |
| English source value | Yes | ✅ | `English Source Value` textarea shows `Sign In`. Proof: layout `Translation Key Detail Editor.jpg`; spec Screen 7 data field `English source value`, line 502. |
| Locale values | Conditional | 🟡 | `Active Language Values` section shows Turkish value `Giris Yapd`, but no other active language values are visible/accessed in the layout. Proof: layout `Translation Key Detail Editor.jpg`; spec Screen 7 data field `Locale values`, line 503 and business rule line 516. |
| Selected language highlight | No | ✅ | Turkish is visibly singled out under Active Language Values, matching the selected language context from Screen 5/6. Proof: layout `Translation Key Detail Editor.jpg`; spec Screen 7 data field `Selected language highlight`, line 504. |
| Character guidance | No | ✅ | Description/context text includes `Keep short - fits on one line`, which provides display-length guidance. Proof: layout `Translation Key Detail Editor.jpg`; spec Screen 7 data field `Character guidance`, line 505. |
| Change reason | Conditional | ✅ | `Change Reason Required` textarea is visible with placeholder explaining source/sensitive translation change reason. Proof: layout `Translation Key Detail Editor.jpg`; spec Screen 7 data field `Change reason`, line 506. |
| History panel | No | ✅ | `History` table is visible with change date, admin name, action type, and change details. Proof: layout `Translation Key Detail Editor.jpg`; spec Screen 7 data field `History panel`, line 507. |
| Save draft action | Yes | ✅ | Green `Save Draft` button is visible and paired with `Cancel`. Proof: layout `Translation Key Detail Editor.jpg`; spec Screen 7 data field `Save draft action`, line 508. |

**Extra Elements**:

- `Cancel` action is present and useful.
- History entries show concrete examples of draft/edit/import/publish lineage.
- Back button label uses `Translation Key Inventor`, which repeats the inventory typo from Screen 6.

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 10/11 required or conditional fields acceptable at layout level (91%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`
**Platform checks applied**: Universal + Web

| Rule ID | Check | Severity | Finding | Evidence |
|---|---|---|---|---|
| U-23 | Terminology consistency | ⚠️ UX Improvement | Back button says `Translation Key Inventor` instead of `Translation Key Inventory`. | `Translation Key Detail Editor.jpg`; spec Screen 6/7 uses inventory/detail terminology. |
| U-15 | Color not sole indicator | ⚠️ UX Improvement | History and language value statuses are text-heavy; Review Needed/Pending Publish state is only embedded inside history copy and not summarized near the edited value. | `Translation Key Detail Editor.jpg` history table includes review-needed text, but the Turkish textarea lacks a visible status badge. |
| W-05 | Form layout | 💡 UX Suggestion | Read-only identity fields look like editable dropdowns because they use select-style chevrons. | `Translation Key Detail Editor.jpg` Key Identity fields show disabled-looking dropdown controls. |

#### Screen 8: Admin - JSON Import Modal/Screen

**Layout**: `layout-temp/JSON Import.jpg`

##### Flow Context

- **User arrives from**: Screen 5 `Import JSON` route for a selected language, or main flow JSON import branch.
- **Screen purpose**: Upload, validate, and import a JSON translation package as draft or as a controlled publish.
- **Entry point**: Present. Breadcrumb shows `Setting / Localization / Turkish (tr) / JSON Import`.
- **Exit path**: Present. `Cancel`, `Import and Publish Version`, and `Back to Language List` are visible.
- **Data continuity**: Partial. Breadcrumb preserves Turkish context, but target language field says `Turkist (tr)`.
- **Flow context issues**: The layout appears to allow the publish action while the required publish summary field is empty.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Target language | Yes | ⚠️ | Target language select is present but displays `Turkist (tr)`, a typo for Turkish. Proof: layout `JSON Import.jpg`; spec Screen 8 data field `Target language`, line 537. |
| Tenant/surface | Yes | ✅ | `Tenant / Surface` select shows `Patient App`. Proof: layout `JSON Import.jpg`; spec Screen 8 data field `Tenant/surface`, line 538. |
| Group/namespace | Yes | ✅ | `Group / Namespace` select shows `common`. Proof: layout `JSON Import.jpg`; spec Screen 8 data field `Group/namespace`, line 539. |
| File | Yes | ✅ | Upload/file section shows `vi.common.patient-app.json` and `Replace` action. Proof: layout `JSON Import.jpg`; spec Screen 8 data field `File`, line 540. |
| Import mode | Yes | ✅ | Import Mode radio cards show `Overwrite draft values` selected and `Add missing keys only` available. Proof: layout `JSON Import.jpg`; spec Screen 8 data field `Import mode`, line 541. |
| Validation preview | Yes | ✅ | Validation Preview panel shows Created, Updated, Unchanged, Skipped, Row warnings, and Errors counts. Proof: layout `JSON Import.jpg`; spec Screen 8 data field `Validation preview`, line 542. |
| Import decision | Yes | ✅ | Import Decision radio cards show `Import as Draft` and `Import and Publish Version`, with the latter selected. Proof: layout `JSON Import.jpg`; spec Screen 8 data field `Import decision`, line 543. |
| Publish summary | Conditional | ❌⚠️ | Publish summary textarea is visible but empty/placeholder-only while `Import and Publish Version` is selected and the green publish button appears enabled. Proof: layout `JSON Import.jpg`; spec Screen 8 data field `Publish summary`, line 544. |
| Error report | Conditional | ✅ | `Download Error Report` action is visible below validation warnings. Proof: layout `JSON Import.jpg`; spec Screen 8 data field `Error report`, line 545. |

**Extra Elements**:

- `Back to Language List` button appears even though the import was entered from Turkish language detail; useful but may skip back past Language Detail.
- Warning detail panel includes specific placeholder/length issues, which supports the validation preview requirement.

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 8/9 required or triggered fields acceptable at layout level (89%)
**Critical Issues**:

- Publish confirmation appears available before required publish summary entry.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`
**Platform checks applied**: Universal + Web

| Rule ID | Check | Severity | Finding | Evidence |
|---|---|---|---|---|
| U-17 | CTA label clarity | 🔴 Critical UX | The primary CTA `Import and Publish Version` appears enabled while the required `Publish summary` is empty. This can lead to a blocked/invalid publish attempt or missing audit reason. | `JSON Import.jpg`; publish decision selected, summary placeholder visible, green CTA visible. |
| U-23 | Terminology consistency | ⚠️ UX Improvement | Target language displays `Turkist (tr)`. | `JSON Import.jpg` Import Target section. |
| U-14 | Semantic color usage | 💡 UX Suggestion | Warning count is amber and errors count is red, which is good; however the `Download Error Report` label appears even when Errors count is `0`, while the visible issues are row warnings. | `JSON Import.jpg` Validation Preview section. |

#### Screen 9: Admin - Language Version History & Rollback

**Layout**: `layout-temp/Language Version History & Rollback.jpg`, `layout-temp/Compare Versions.jpg`

##### Flow Context

- **User arrives from**: Screen 5 Version History route, Screen 8 import+publish path, or main localization tab.
- **Screen purpose**: Review pending draft changes, publish a new bundle version, inspect prior versions, compare versions, and roll back.
- **Entry point**: Present. `Language Version History & Rollback` tab is selected.
- **Exit path**: Present. `Publish Version`, `Discard Draft`, `Compare`, and row-level `Rollback` are visible.
- **Data continuity**: Partial. Filters preserve language/surface/group context, but language field shows `Turkist (tr)`.
- **Flow context issues**: Publish CTA appears enabled while Change Summary is empty.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Version ID | Yes | ✅ | Published Version History table shows version IDs such as `v-tr-PA-appt-0015`. Proof: layout `Language Version History & Rollback.jpg`; spec Screen 9 data field `Version ID`, line 573. |
| Language | Yes | ⚠️ | Language filters/table values are visible, but top filter shows `Turkist (tr)`. Proof: layout `Language Version History & Rollback.jpg`; spec Screen 9 data field `Language`, line 574. |
| Tenant/surface | Yes | ✅ | Tenant/surface filter and table column show `Patient App`. Proof: layout `Language Version History & Rollback.jpg`; spec Screen 9 data field `Tenant/surface`, line 575. |
| Group/namespace | No | ✅ | Namespace filter and table column show `Appointment` / `appointments`. Proof: layout `Language Version History & Rollback.jpg`; spec Screen 9 data field `Group/namespace`, line 576. |
| Source type | Yes | 🟡 | Compare modal version selectors show source labels such as JSONImport and Manual Patch, but the main version-history table does not clearly expose a dedicated Source Type badge/column. Proof: layouts `Language Version History & Rollback.jpg`, `Compare Versions.jpg`; spec Screen 9 data field `Source type`, line 577. |
| Change summary | Yes | 🟡 | Change Summary textarea is present for publish, and the version table appears to include summary snippets, but the publish summary is empty while publish CTA is visible. Proof: layout `Language Version History & Rollback.jpg`; spec Screen 9 data field `Change summary`, line 578. |
| Pending changes | No | ✅ | Pending Changes list shows keys and statuses such as Edited/New. Proof: layout `Language Version History & Rollback.jpg`; spec Screen 9 data field `Pending changes`, line 579. |
| Coverage summary | No | ✅ | Coverage Summary shows 148 Translated, 12 Draft/Review, and 4 Missing. Proof: layout `Language Version History & Rollback.jpg`; spec Screen 9 data field `Coverage summary`, line 580. |
| Validation status | Yes | ✅ | Validation Status warning panel is visible, and table rows show Pass/Warning badges. Proof: layout `Language Version History & Rollback.jpg`; spec Screen 9 data field `Validation status`, line 581. |
| Publish action | Conditional | ❌⚠️ | `Publish Version` button appears enabled while Change Summary textarea is empty. Proof: layout `Language Version History & Rollback.jpg`; spec Screen 9 data field `Publish action`, line 582 and change summary requirement line 578. |
| Rollback action | Conditional | ✅ | Row action menu includes `Rollback`. Proof: layout `Language Version History & Rollback.jpg`; spec Screen 9 data field `Rollback action`, line 583. |
| Compare versions action | No | ✅ | `Compare` button is visible, and `Compare Versions.jpg` shows version selectors, changed count, key/value diff table, and Added/Removed/Edited badges. Proof: layouts `Language Version History & Rollback.jpg`, `Compare Versions.jpg`; spec Screen 9 data field `Compare versions action`, line 584. |

**Extra Elements**:

- `Discard Draft` action is visible and useful for draft management.
- Compare modal includes dimmed background and close control.

**Screen Status**: 🔴 FAIL
**Field Coverage**: 10/11 required or triggered fields acceptable at layout level (91%), but publish validation/control mismatch is critical.
**Critical Issues**:

- Publish action appears available before required change summary/reason is provided.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`
**Platform checks applied**: Universal + Web

| Rule ID | Check | Severity | Finding | Evidence |
|---|---|---|---|---|
| U-17 | CTA label clarity | 🔴 Critical UX | `Publish Version` appears enabled even though `Change Summary` is empty, which risks missing required publish rationale/audit data. | `Language Version History & Rollback.jpg`; Change Summary placeholder is visible above green Publish Version button. |
| U-23 | Terminology consistency | ⚠️ UX Improvement | Language filter shows `Turkist (tr)`. | `Language Version History & Rollback.jpg`. |
| W-06 | Table design | ⚠️ UX Improvement | Source type is not clearly represented as a dedicated badge/column in the main version-history table, although it appears in compare selectors. | `Language Version History & Rollback.jpg` history table; `Compare Versions.jpg` modal selectors. |
| U-12 | Text truncation | 💡 UX Suggestion | Compare modal version B selector truncates long version/source label without exposing the full value in the static design. | `Compare Versions.jpg` selector text ends with ellipsis. |

#### Screen 10: Admin - Machine Translation Provider & Draft Generation

**Layout**: `layout-temp/Machine Translation Provider And Draft Generation.jpg`

##### Flow Context

- **User arrives from**: Screen 5 Machine Translation route, or main flow machine translation branch.
- **Screen purpose**: Configure machine-translation provider access and generate review-required draft values for a selected non-English language.
- **Entry point**: Present. Breadcrumb shows Turkish language context and machine-translation screen title.
- **Exit path**: Present. `Generate Draft`, `Cancel`, `Back to Language List`, and job-history review are visible.
- **Data continuity**: Partial. Breadcrumb preserves Turkish context, but target language field says `Turkist (Tr)`.
- **Flow context issues**: None blocking.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Provider | Yes | ✅ | Provider select shows `Google Cloud Translation`. Proof: layout `Machine Translation Provider And Draft Generation.jpg`; spec Screen 10 data field `Provider`, line 610. |
| Provider status | Yes | ✅ | Provider status badge shows `Connected`. Proof: layout `Machine Translation Provider And Draft Generation.jpg`; spec Screen 10 data field `Provider status`, line 611. |
| API key / credential | Conditional | ✅ | API key field is visible and masked after prefix `AIza...`. Proof: layout `Machine Translation Provider And Draft Generation.jpg`; spec Screen 10 data field `API key / credential`, line 612. |
| Supported languages | No | ✅ | Supported languages list shows Turkish, German, French, Spanish, Italian, Portuguese, plus `+48 more`. Proof: layout `Machine Translation Provider And Draft Generation.jpg`; spec Screen 10 data field `Supported languages`, line 613. |
| Target language | Yes | ⚠️ | Target language select is visible but says `Turkist (Tr)`, a typo/casing issue for Turkish (`tr`). Proof: layout `Machine Translation Provider And Draft Generation.jpg`; spec Screen 10 data field `Target language`, line 614. |
| Tenant/surface scope | Yes | ✅ | Multi-select shows Patient App, Provider Dashboard, and Admin Platform selected. Proof: layout `Machine Translation Provider And Draft Generation.jpg`; spec Screen 10 data field `Tenant/surface scope`, line 615. |
| Group/namespace scope | No | ✅ | Group/Namespace select shows `All Namespace`. Proof: layout `Machine Translation Provider And Draft Generation.jpg`; spec Screen 10 data field `Group/namespace scope`, line 616. |
| Generation mode | Yes | ✅ | Radio cards show `Prefill Missing Keys` selected and `Replace Entire Language` available with caution text. Proof: layout `Machine Translation Provider And Draft Generation.jpg`; spec Screen 10 data field `Generation mode`, line 617. |
| Preview counts | Yes | ✅ | Preview Counts panel shows eligible, missing, skipped, replacements, errors, and estimated usage cost. Proof: layout `Machine Translation Provider And Draft Generation.jpg`; spec Screen 10 data field `Preview counts`, line 618. |
| Confirmation reason | Yes | ✅ | Confirmation reason textarea is filled with a business reason for Turkish launch preparation. Proof: layout `Machine Translation Provider And Draft Generation.jpg`; spec Screen 10 data field `Confirmation reason`, line 619. |
| Generate draft action | Yes | ✅ | Green `Generate Draft` button is visible. Proof: layout `Machine Translation Provider And Draft Generation.jpg`; spec Screen 10 data field `Generate draft action`, line 620. |
| Job history | No | ⚠️ | Job History table is visible with job ID, mode, scope, keys, status, created, and errors, but does not show actor, target language, or provider columns described by the spec. Proof: layout `Machine Translation Provider And Draft Generation.jpg`; spec Screen 10 data field `Job history`, line 621. |

**Extra Elements**:

- `Cancel` and `Back to Language List` controls are visible.
- Estimated usage cost is shown, matching the PRD note to show cost/usage warnings where available.

**Screen Status**: 🟢 GOOD
**Field Coverage**: 11/11 required or conditional fields acceptable at layout level (100%); optional job-history metadata is incomplete.
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`
**Platform checks applied**: Universal + Web

| Rule ID | Check | Severity | Finding | Evidence |
|---|---|---|---|---|
| U-23 | Terminology consistency | ⚠️ UX Improvement | Target language displays `Turkist (Tr)` instead of Turkish (`tr`). | `Machine Translation Provider And Draft Generation.jpg`. |
| W-06 | Table design | 💡 UX Suggestion | Job History omits actor, target language, and provider, which the spec describes as useful audit metadata. | `Machine Translation Provider And Draft Generation.jpg` Job History section. |
| U-17 | CTA label clarity | 💡 UX Suggestion | `Generate Draft` is clear, but the CTA area does not restate that generated values become Review Needed drafts only. | `Machine Translation Provider And Draft Generation.jpg` Confirmation/CTA area; spec Screen 10 business rules require review-needed draft behavior. |

**Flow Coverage Gaps**:

- Screen 4 is now acceptable after the revised screenshot: native name, direction, status badges, and non-default `Deactivate` behavior are covered; only `Translation Key Inventor` remains as a terminology typo.
- Screens 8 and 9 show publish CTAs in states where required summary/reason fields are still empty.
- Several screens still use inconsistent terminology: `Turkist`, `Inventor`, and inconsistent casing for locale code `Tr`.

---

## Action Items

| Priority | Flow | Screen | Issue | Recommendation |
|----------|------|--------|-------|----------------|
| 🔴 Critical UX | Admin Localization Management | Screen 8 | `Import and Publish Version` appears enabled while required publish summary is empty. | Disable publish CTA until publish summary and authorization requirements are satisfied. |
| 🔴 Critical UX | Admin Localization Management | Screen 9 | `Publish Version` appears enabled while required change summary is empty. | Disable publish CTA until change summary/reason and validation requirements are satisfied. |
| ⚠️ UX Improvement | Admin Localization Management | Screens 4, 7, 8, 9, 10 | Remaining terminology errors: `Turkist`, `Translation Key Inventor`, and Screen 10 locale code casing `Tr`. Screen 6 has been corrected in the revised screenshot. | Correct to `Turkish` and `Translation Key Inventory`; standardize locale code casing as `tr`. |
| ⚠️ UX Improvement | Admin Localization Management | Screen 7 | Only Turkish is visible under active language values; all active language values are not shown or clearly accessible. | Add tabs/accordion/list for all active language values while highlighting the selected language. |
| 💡 UX Suggestion | Admin Localization Management | Screen 10 | Job History omits actor, target language, and provider columns described in the spec. | Add audit metadata columns or a row detail drawer for these fields. |

### Priority Legend

- **Critical**: Blocks flow progression, breaks data integrity, or causes security/legal risk. Must fix before development.
- **Critical UX**: Severe usability issue that would prevent users from completing the flow or cause significant confusion. Must fix before development.
- **Important**: Functional discrepancy that could cause user confusion or require rework during development. Should fix before development.
- **UX Improvement**: Usability or design quality issue that deviates from platform conventions or best practices. Should fix before development.
- **Suggestion**: Cosmetic or minor improvement. Can fix anytime.
- **UX Suggestion**: Minor design enhancement that would improve polish. Can fix anytime.

---

## Notes

- Requirement source: `local-docs/project-requirements/functional-requirements/fr021-i18n-localization/prd.md`
- UX/UI rules source: `local-docs/project-automation/skills-engineering/verify-design-layout/references/ux-ui-evaluation-rules.md`
- Web Interface Guidelines source fetched 2026-06-04 from `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`
- Layout files are JPG screenshots in `layout-temp/`.
- Image analysis for Screen 7 used local visual inspection after the external image-analysis tool returned transient network errors.
