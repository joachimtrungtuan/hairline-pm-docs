# Design Layout Verification Report — FR-019

**Report Date**: 2026-05-21
**Report Type**: Design Layout Verification
**FR Scope**: FR-019 — Promotions & Discount Management
**Flow Scope**: Full FR-019 check for Screens 1-10 only (Screen 11 excluded by request)
**Layout Source**: `layout-temp/`
**Platform**: Mixed — Admin Web and Provider Web only for this review scope
**Status**: 🔴 BLOCKED — all 10 in-scope screens now have mapped layouts, but Admin Screens 3/4 and Provider Screen 9 still fail the FR contract.

---

## Summary Dashboard

| # | Flow | Module | Screens Required | Screens Verified | Layout Status | Field Coverage |
|---|------|--------|-----------------|-----------------|---------------|----------------|
| A-06 | Admin Promotion Management | A-06: Discount & Promotion Management | 6 | 6 | 🔴 BLOCKED | ~91.7% |
| PR-02/PR-05 | Provider Promotion Management | PR-02/PR-05: Provider + Financial Reporting | 4 | 4 | 🔴 BLOCKED | ~91.2% |

**Overall**: 2 of 2 in-scope platform flows are blocked. Admin coverage remains blocked by override-governance and portfolio-filter gaps; the new Screen 6 file resolves the earlier missing-column failure on the admin redemption log. Provider coverage improves again because the new provider Screen 10 full-table file resolves the previously missing Patient and explicit State columns, leaving Screen 9 as the only provider fail.
**Screens**: 10 of 10 in-scope specified screens have layout candidates (100% candidate coverage); 3 are COMPLETE, 1 is GOOD, 3 are PARTIAL, and 3 are FAIL.

---

## Layout File Inventory

### Mapped to Spec Flows

| Layout File | Maps to Flow | Maps to Screen | Notes |
|-------------|-------------|----------------|-------|
| `Filter_Promotion Program Hub.jpg` | A-06 | Screen 1 (Promotion Program Hub) | Filter state |
| `Fulltable overview_Promotion Program Hub.jpg` | A-06 | Screen 1 (Promotion Program Hub) | Full table state |
| `Promotion Program Hub.jpg` | A-06 | Screen 1 (Promotion Program Hub) | Main state |
| `Promotion Detail (Create/Promotion Detail (Create/Edit) - Both Fees.jpg` | A-06 | Screen 2 (Promotion Detail Create/Edit) | Both-fees program form |
| `Promotion Detail (Create/Promotion Detail (Create/Edit) - Hairline Only.jpg` | A-06 | Screen 2 (Promotion Detail Create/Edit) | Hairline-only program form |
| `Promotion Detail (Create/Promotion Detail (Create/Edit) - Provider Only.jpg` | A-06 | Screen 2 (Promotion Detail Create/Edit) | Provider-only program type within the admin form system; not the provider-owned Screen 9 |
| `Provider Adoption Manager.jpg` | A-06 | Screen 3 (Provider Adoption Manager) | Main state |
| `Fulltable overview_Provider Adoption Manager.jpg` | A-06 | Screen 3 (Provider Adoption Manager) | Full table state |
| `Provider Promotion Portfolio.jpg` | A-06 | Screen 4 (Provider Promotion Portfolio) | Main state; title text still mismatched in the file |
| `Fulltable overview_Provider Promotion Portfolio.jpg` | A-06 | Screen 4 (Provider Promotion Portfolio) | Full table state |
| `Hairline-Funded & Direct-Issued Codes Manager.jpg` | A-06 | Screen 5 (Hairline-Funded & Direct-Issued Codes Manager) | Main state |
| `Fulltable overview_Hairline Codes Manager.jpg` | A-06 | Screen 5 (Hairline-Funded & Direct-Issued Codes Manager) | Full table state |
| `Promotion Analytics & Applications - Overview (Analytics).jpg` | A-06 | Screen 6 (Promotion Analytics & Applications) | Admin analytics overview |
| `Promotion Analytics & Applications - Overview (Analytics)-1.jpg` | A-06 | Screen 6 (Promotion Analytics & Applications) | Admin applications tab state |
| `Fulltable overview_Promotion Analytics & Applications (Admin).jpg` | A-06 | Screen 6 (Promotion Analytics & Applications) | Admin full-table state with separate Program, Patient, Provider, Quote / Booking ID, State, and Status columns |
| `Fulltable overview_Promotion Analytics & Applications.jpg` | A-06 | Screen 6 (Promotion Analytics & Applications) | Additional redemption-log full-table state |
| `Admin Campaigns - Pending.jpg` | PR-02/PR-05 | Screen 7 (Admin Campaigns) | Pending tab |
| `Admin Campaigns - Active.jpg` | PR-02/PR-05 | Screen 7 (Admin Campaigns) | Active tab |
| `Admin Campaigns - Active-1.jpg` | PR-02/PR-05 | Screen 7 (Admin Campaigns) | Past-tab state despite filename |
| `My Promotions.jpg` | PR-02/PR-05 | Screen 8 (My Promotions List) | Main list and action-menu state |
| `Filter_My Promotions (Providers).jpg` | PR-02/PR-05 | Screen 8 (My Promotions List) | Filter state |
| `Fulltable overview_My Promotions (Providers).jpg` | PR-02/PR-05 | Screen 8 (My Promotions List) | Full table state |
| `New Promotion_Edit Promotion.jpg` | PR-02/PR-05 | Screen 9 (Promotion Detail Create/Edit) | Provider-owned standalone create/edit flow |
| `Promotion Analytics & Applications - Overview (Analytics - Provider).jpg` | PR-02/PR-05 | Screen 10 (Provider Promotion Analytics & Applications) | Provider analytics overview |
| `Promotion Analytics & Applications - Applications (Redemption Log).jpg` | PR-02/PR-05 | Screen 10 (Provider Promotion Analytics & Applications) | Provider applications/redemption log state |
| `Fulltable overview_Promotion Analytics & Applications (Provider).jpg` | PR-02/PR-05 | Screen 10 (Provider Promotion Analytics & Applications) | Provider full-table state with explicit State and Patient columns |

### Unmapped Files

| Layout File | Likely Purpose | Notes |
|-------------|---------------|-------|
| `Filter.jpg` | Generic filter state | Filename does not identify which FR-019 screen it belongs to |
| `Fulltable overview.jpg` | Generic full-table state | Filename does not identify which FR-019 screen it belongs to |

---

## Detailed Verification by Flow

---

### Flow A-06: Admin Promotion Management

**Status**: 🔴 BLOCKED — Screens 3 and 4 still fail; Screen 6 improves to partial after the new admin full-table evidence.
**Screens required**: 6
**Layout files**: `Filter_Promotion Program Hub.jpg`, `Fulltable overview_Promotion Program Hub.jpg`, `Promotion Program Hub.jpg`, `Promotion Detail (Create/Edit) - Both Fees.jpg`, `Promotion Detail (Create/Edit) - Hairline Only.jpg`, `Promotion Detail (Create/Edit) - Provider Only.jpg`, `Fulltable overview_Provider Adoption Manager.jpg`, `Provider Adoption Manager.jpg`, `Fulltable overview_Provider Promotion Portfolio.jpg`, `Provider Promotion Portfolio.jpg`, `Fulltable overview_Hairline Codes Manager.jpg`, `Hairline-Funded & Direct-Issued Codes Manager.jpg`, `Promotion Analytics & Applications - Overview (Analytics).jpg`, `Promotion Analytics & Applications - Overview (Analytics)-1.jpg`, `Fulltable overview_Promotion Analytics & Applications (Admin).jpg`, `Fulltable overview_Promotion Analytics & Applications.jpg`

#### Screen 1: Admin — Promotion Program Hub

**Layout**: `Promotion Program Hub.jpg`, `Filter_Promotion Program Hub.jpg`, `Fulltable overview_Promotion Program Hub.jpg`

##### Flow Context

- **User arrives from**: Admin navigation into the promotion hub / discount management module.
- **Screen purpose**: Master catalog for every promotion program type, including Admin-via-Provider, Provider Self-Created, and Hairline-Funded & Direct-Issued records.
- **Entry point**: Present — layout shows the hub list and filter entry points.
- **Exit path**: Present — row menu includes View, Pause, Archive, View Adoptions, and View Applications actions.
- **Data continuity**: Mostly correct — all three program types are represented, but usage formatting is inconsistent with the FR's redeemed-count-vs-limit requirement.
- **Flow context issues**: Downstream Screen 6 pre-filtering cannot be verified from the static layout; Resume state is not captured.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Code / keyword search | No | ✅ | `Promotion Program Hub.jpg` shows `Search code, name...`, matching the search field in PRD lines 172-174. |
| Filter: Program Type | No | ❌⚠️ | `Filter_Promotion Program Hub.jpg` shows a plain dropdown; PRD line 173 requires multi-select. |
| Filter: Scope | No | ❌⚠️ | `Filter_Promotion Program Hub.jpg` shows a plain dropdown; PRD line 174 requires multi-select. |
| Filter: Status | No | ❌⚠️ | `Filter_Promotion Program Hub.jpg` shows a plain dropdown; PRD line 175 requires multi-select. |
| Filter: Funding Model | No | ❌⚠️ | `Filter_Promotion Program Hub.jpg` shows a plain dropdown; PRD line 176 requires multi-select. |
| Filter: Provider Participation | No | ✅ | `Filter_Promotion Program Hub.jpg` shows a dropdown, matching PRD line 177. |
| Filter: Date Range | No | ✅ | `Filter_Promotion Program Hub.jpg` shows start/end date inputs with calendar affordance, matching PRD line 178. |
| Filter: Usage | No | ❌⚠️ | `Fulltable overview_Promotion Program Hub.jpg` shows some usage values as `Not started` or `-`, while PRD line 179 defines usage as redeemed-count threshold/range. |
| Filter: ROI | No | ✅ | `Filter_Promotion Program Hub.jpg` shows ROI as dropdown, matching PRD line 180. |
| Result Count | Yes | ✅ | `Promotion Program Hub.jpg` shows `Total 85 items`, matching PRD line 181. |
| Results Table | Yes | ✅ | `Promotion Program Hub.jpg` and `Fulltable overview_Promotion Program Hub.jpg` show a populated table, matching PRD line 182. |
| Code / Program Name | Yes | ✅ | `Fulltable overview_Promotion Program Hub.jpg` shows code/name as the primary identifier, matching PRD lines 186-188. |
| Program Type | Yes | ✅ | `Fulltable overview_Promotion Program Hub.jpg` shows badges for all three program types, matching PRD line 189. |
| Owner | Yes | ✅ | `Fulltable overview_Promotion Program Hub.jpg` shows admin/provider owners, matching PRD line 190. |
| Funding Model | Yes | ✅ | `Fulltable overview_Promotion Program Hub.jpg` shows Both Fees, Hairline Only, and Provider Only, matching PRD line 191. |
| Participating Providers | Yes | ✅ | `Fulltable overview_Promotion Program Hub.jpg` shows provider counts, All Providers, and N/A Direct-Issued, matching PRD line 192. |
| Status | Yes | ✅ | Layouts show Draft, Pending Approval, Active, Paused, Expired, and Archived statuses, matching PRD line 193. |
| Active Window | Yes | ✅ | Layouts show date ranges such as `01 Jun - 31 Aug 2026`, matching PRD line 194. |
| Usage | Yes | ❌⚠️ | `Fulltable overview_Promotion Program Hub.jpg` mixes numeric ratios with `Not started` / `-`; PRD line 195 requires redeemed count vs limit. |
| ROI Tier | Yes | ✅ | `Fulltable overview_Promotion Program Hub.jpg` shows High, Mid, Low, and Not yet calculated, matching PRD line 196. |
| Last Updated | Yes | ✅ | `Fulltable overview_Promotion Program Hub.jpg` includes timestamp values and visible descending order, matching PRD line 197. |
| View Detail | Yes | ⚠️ | Row menu shows `View` in `Promotion Program Hub.jpg`; function is present but less explicit than PRD line 201. |
| Pause / Resume | Yes | ✅ | Row menu shows `Pause`; Resume state is not captured but Paused lifecycle rows exist. |
| Archive | Yes | ✅ | Row menu shows `Archive`, matching PRD line 203. |
| View Adoptions | Conditional | ✅ | `Promotion Program Hub.jpg` shows `View Adoptions` for an Admin-via-Provider row, matching PRD line 204. |
| View Applications | Yes | ✅ | `Promotion Program Hub.jpg` shows `View Applications`, matching PRD line 205. |

**Conditional States**:

- `View Adoptions` is visible for an Admin-via-Provider row.
- `Pause` is visible for an active row; no separate Resume menu capture was provided.
- `View Applications` exists, but Screen 6 pre-filter behavior cannot be verified from a static layout.

**Extra Elements**:

- `Export` button appears in `Promotion Program Hub.jpg`; it is not listed in the PRD Screen 1 field table.
- Global app shell elements are visible but treated as outside the FR-019 field contract.

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 21/26 pass-or-minor (80.8%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: ui-ux-pro-max, web-design-guidelines

| Rule ID | Severity | Observation | Recommendation |
|---------|----------|-------------|----------------|
| U-17 | ⚠️ UX Improvement | Row menu uses `View`, which is less explicit than the FR's `View Detail` action and sits beside `View Adoptions` / `View Applications`. Evidence: `Promotion Program Hub.jpg`. | Rename the menu item to `View Detail` so the destination is unambiguous. |

#### Screen 2: Admin — Promotion Detail (Create / Edit)

**Layout**: `Promotion Detail (Create/Promotion Detail (Create/Edit) - Both Fees.jpg`, `Promotion Detail (Create/Promotion Detail (Create/Edit) - Hairline Only.jpg`, `Promotion Detail (Create/Promotion Detail (Create/Edit) - Provider Only.jpg`

##### Flow Context

- **User arrives from**: Screen 1 row detail or create action.
- **Screen purpose**: Type-aware form to define and govern a promotion program across its lifecycle.
- **Entry point**: Present — page title, breadcrumb, and form structure identify the promotion detail editor.
- **Exit path**: Present — lifecycle/governance controls and audit trail are visible; static files do not prove submit behavior.
- **Data continuity**: Correct — program type changes show relevant sections for Both Fees, Hairline Only, and Provider Only variants.
- **Flow context issues**: No layout captures the required inline validation error for `Application Mode = Auto-applied` on Both-Fees programs.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Program Name | Yes | ✅ | Text input labeled `Program Name` appears in all three variants, matching PRD line 236. |
| Description | No | ✅ | Multiline `Description` textarea appears in all three variants, matching PRD line 237. |
| Discount Type | Yes | ✅ | Select control labeled `Discount Type` appears, matching PRD line 238. |
| Value | Yes | ✅ | Numeric value input appears in all variants, matching PRD line 239. |
| Applies To | Yes | ✅ | Select control labeled `Applies To` appears, matching PRD line 240. |
| Code(s) | Conditional | ✅ | Chip-style code field appears with sample `SUMMER25`, matching PRD line 241. |
| Application Mode | Yes | ✅ | Select control labeled `Application Mode` appears, matching PRD line 242. |
| Start / End Date | Yes | ✅ | Combined date-range control appears, matching PRD line 243. |
| Total Usage Limit | No | ✅ | Numeric input appears, matching PRD line 244. |
| Per-User Usage Limit | No | ✅ | Numeric input appears, matching PRD line 245. |
| Lifecycle State | Yes | ✅ | Controlled `Draft` badge appears; audit trail also shows lifecycle transition detail, matching PRD line 246. |
| Funding Model | All | ✅ | Read-only/derived field shows Both Fees, Hairline Only, or Provider Only by variant, matching PRD line 252. |
| Target Providers | Admin-via-Provider | ✅ | Present only in the Both Fees layout, matching PRD line 253. |
| Approval Routing | Admin-via-Provider | ✅ | Present only in the Both Fees layout, matching PRD line 254. |
| Auto-Decline Window | Admin-via-Provider | ✅ | Present only in the Both Fees layout, matching PRD line 255. |
| Issuance Channel | Hairline-Funded & Direct-Issued | ✅ | Present only in the Hairline Only layout, matching PRD line 256. |
| Recipient Binding | Hairline-Funded & Direct-Issued | ✅ | Present only in the Hairline Only layout with recipient chip, matching PRD line 257. |
| Bulk Generate Codes | Hairline-Funded & Direct-Issued | ✅ | Present only in the Hairline Only layout with quantity input and generate action, matching PRD line 258. |
| Audit Trail Panel | Yes | ✅ | Visible in all three layouts with date, admin, action type, and details columns, matching PRD lines 261-263. |

**Conditional States**:

- Type-specific sections are correctly swapped across the three provided files.
- The invalid Both-Fees `Application Mode = Auto-applied` inline error required by PRD line 278 is not represented by a separate state.

**Extra Elements**:

- `Export` and `+ New Program` controls appear in the layout and look hub-level rather than detail-specific; they are not listed in the Screen 2 PRD fields.

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 19/19 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: ui-ux-pro-max, web-design-guidelines

| Rule ID | Severity | Observation | Recommendation |
|---------|----------|-------------|----------------|
| U-19 | ⚠️ UX Improvement | The supplied files do not show inline error treatment for the Both-Fees restriction on `Application Mode = Auto-applied`. Evidence: default `Application Mode` select in `Promotion Detail (Create/Edit) - Both Fees.jpg`, no blocked/error-state variant. | Add an error-state layout or inline helper/error treatment showing why Auto-applied is not permitted for Both-Fees programs. |

#### Screen 3: Admin — Provider Adoption Manager

**Layout**: `Provider Adoption Manager.jpg`, `Fulltable overview_Provider Adoption Manager.jpg`

##### Flow Context

- **User arrives from**: Screen 1 `View Adoptions` action for an Admin-via-Provider program.
- **Screen purpose**: Show every targeted provider's adoption status and allow admin override decisions.
- **Entry point**: Present — top summary card identifies the program.
- **Exit path**: Partially present — row menu exposes Re-invite, Force-Revoke, and Mark Exempt actions.
- **Data continuity**: Correct — program name, dates, value, and funding model are visible in the program header.
- **Flow context issues**: Mandatory reason capture for admin overrides is not visible.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Program Header | Yes | ✅ | `Provider Adoption Manager.jpg` shows program name, dates, value, and Both Fees funding model, matching PRD line 294. |
| Provider Row | Yes | ✅ | Both layouts show one row per targeted provider, matching PRD line 295. |
| Provider | Yes | ✅ | Rows show provider name and region, matching PRD lines 299-300. |
| Status | Yes | ✅ | `Fulltable overview_Provider Adoption Manager.jpg` shows Pending, Accepted, Declined, Auto-Declined, Revoked-by-Provider, and Revoked-by-Admin, matching PRD line 301. |
| Decided At | Yes | ✅ | Timestamp column is visible, matching PRD line 302. |
| Decided By | Yes | ✅ | Provider/admin actor values are visible, matching PRD line 303. |
| Comment | No | ✅ | Comment column is visible with text or blank marker, matching PRD line 304. |
| Redemptions | Yes | ✅ | Redemptions column shows counts, matching PRD line 305. |
| Admin Actions | Yes | ✅ | Row menu exposes Re-invite, Force-Revoke, and Mark Exempt, matching PRD line 306. |
| Override reason text | Yes | ❌ | PRD line 312 requires all admin overrides to be logged with mandatory reason text; no reason-entry modal, drawer, or field appears in either layout file. |

**Conditional States**:

- Status variants are represented for all six listed statuses.
- Row actions appear status-dependent.
- Missing conditional state: override confirmation / reason-entry state.

**Extra Elements**:

- `Search Provider`, `Export CSV`, pagination, total count, and page-size controls appear but are not listed in the Screen 3 PRD table.

**Screen Status**: 🔴 FAIL
**Field Coverage**: 9/10 (90%)
**Critical Issues**:

- Mandatory reason capture for admin overrides is missing; this weakens auditability and governance required by PRD line 312.

##### UX/UI Design Evaluation

**Skills invoked**: ui-ux-pro-max, web-design-guidelines

| Rule ID | Severity | Observation | Recommendation |
|---------|----------|-------------|----------------|
| U-18 | 🔴 Critical UX | `Force-Revoke` appears in the same neutral menu styling as safe actions like `Mark Exempt`, and no reason-confirmation state is shown. Evidence: `Fulltable overview_Provider Adoption Manager.jpg` row action menu. | Add a destructive confirmation state with mandatory reason text, and visually distinguish Force-Revoke from safe actions. |

#### Screen 4: Admin — Provider Promotion Portfolio

**Layout**: `Provider Promotion Portfolio.jpg`, `Fulltable overview_Provider Promotion Portfolio.jpg`

##### Flow Context

- **User arrives from**: Provider drill-down from hub/adoption context.
- **Screen purpose**: Per-provider view of adopted admin programs and provider self-created programs.
- **Entry point**: Present — provider header and KPI strip identify the provider context.
- **Exit path**: Partially present — row actions imply detail/governance access.
- **Data continuity**: Mostly correct — provider-level KPIs and promotion rows are visible.
- **Flow context issues**: Layout page title reads `Provider Adoption Manager`, not `Provider Promotion Portfolio`; mandatory reason-entry state is not shown for governance actions.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Provider Header | Yes | ✅ | `Provider Promotion Portfolio.jpg` shows provider name, region, contact details, and KPI context, matching PRD line 331. |
| Filter: Record Type | No | ❌ | No visible multi-select for Adopted-Admin / Self-Created; only a generic filter button is shown, while PRD line 332 specifies the field. |
| Filter: Status | No | ❌ | No visible status multi-select appears, while PRD line 333 specifies it. |
| Filter: Date Range | No | ❌ | No visible date-range picker appears, while PRD line 334 specifies it. |
| Results Table | Yes | ✅ | Table is present in both files, matching PRD line 335. |
| Program Name | Yes | ✅ | Program names are shown, matching PRD line 341. |
| Record Type | Yes | ⚠️ | Column is labeled `Program Type` instead of `Record Type`, but badge values distinguish Adopted-Admin / Self-Created per PRD line 342. |
| Funding Model | Yes | ✅ | Both Fees and Provider Only values appear, matching PRD line 343. |
| Status | Yes | ✅ | Lifecycle badges are visible, matching PRD line 344. |
| Active Window | Yes | ✅ | Date ranges appear, matching PRD line 345. |
| Redemptions | Yes | ✅ | Redemption counts appear, matching PRD line 346. |
| Revenue Impact | Yes | ✅ | Currency impact with split amounts appears, matching PRD line 347. |
| Row Action | Yes | ✅ | Row action menu/detail access appears, matching PRD line 348. |
| Adoption Rate KPI | Yes | ✅ | KPI card is visible, matching PRD line 352. |
| Self-Created Active Count KPI | Yes | ✅ | KPI card is visible, matching PRD line 353. |
| Total Redemptions KPI | Yes | ✅ | KPI card with 30d / 90d / 365d context is visible, matching PRD line 354. |
| Total Discount Issued KPI | Yes | ✅ | Currency KPI is visible, matching PRD line 355. |
| Read-only self-created detail state | Conditional | ⚠️ | Row action implies detail access, but no read-only Screen 2 state is provided for PRD line 359. |
| Pause / Archive reason text | Conditional | ⚠️ | Pause and Archive actions are visible, but mandatory reason-entry UI from PRD line 360 is not shown. |

**Conditional States**:

- Filter-expanded state is not provided, so the required filter controls cannot be confirmed.
- Pause/archive reason-entry state is not shown.
- Read-only Screen 2 state for self-created programs is not shown.

**Extra Elements**:

- Search program input, Export CSV, pagination/page-size controls, and provider rating appear but are not listed in Screen 4 PRD fields.

**Screen Status**: 🔴 FAIL
**Field Coverage**: 16/19 pass-or-minor (84.2%)
**Critical Issues**:

- Required filter controls are not visible in provided layouts.

##### UX/UI Design Evaluation

**Skills invoked**: ui-ux-pro-max, web-design-guidelines

| Rule ID | Severity | Observation | Recommendation |
|---------|----------|-------------|----------------|
| U-23 | ⚠️ UX Improvement | Page title says `Provider Adoption Manager` while the FR screen name is `Provider Promotion Portfolio`. Evidence: `Provider Promotion Portfolio.jpg` vs PRD line 323. | Align the page title with the FR screen name. |
| U-18 | ⚠️ UX Improvement | `Pause` and `Archive` appear as plain menu items beside safe actions, with no visible destructive differentiation. Evidence: row menu in the Screen 4 layouts. | Add visual differentiation and confirmation/reason-entry state for governed actions. |

#### Screen 5: Admin — Hairline-Funded & Direct-Issued Codes Manager

**Layout**: `Hairline-Funded & Direct-Issued Codes Manager.jpg`, `Fulltable overview_Hairline Codes Manager.jpg`

##### Flow Context

- **User arrives from**: Screen 1 Hairline-Funded program management or Screen 2 Hairline-Funded variant.
- **Screen purpose**: Manage Hairline-funded/direct-issued codes across open, affiliate-bound, segment-bound, and individually issued channels.
- **Entry point**: Present — program selector and issuance channel context appear.
- **Exit path**: Present — bulk generate, revoke, export, and row-level controls are visible.
- **Data continuity**: Mostly correct — selected affiliate-bound program maps to recipient binding and redemption statuses.
- **Flow context issues**: Revoke-reason and in-progress cancellation/notification state is not represented.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Program Selector | Yes | ✅ | Top dropdown is visible, matching PRD line 376. |
| Issuance Channel | Yes | ⚠️ | Present but rendered like a disabled select/input rather than plain label; still communicates the PRD line 377 value. |
| Codes Table | Yes | ✅ | Table is visible and populated in both files, matching PRD line 378. |
| Bulk Generate | No | ✅ | `Generate` action is visible, matching PRD line 379. |
| Bulk Revoke | No | ✅ | `Revoke` action is visible; mandatory reason state from PRD line 380 is not shown. |
| Export | No | ✅ | `Export` action is visible, matching PRD line 381. |
| Code | Yes | ✅ | Code strings such as `AFF-SPR26-A1B2C3` appear, matching PRD line 387. |
| Recipient Binding | Yes | ✅ | Affiliate names appear, matching PRD line 388. |
| Issued At | Yes | ✅ | Generation dates appear, matching PRD line 389. |
| Issued By | Yes | ✅ | Admin user appears, matching PRD line 390. |
| Redemption Status | Yes | ✅ | Unused, In-Progress, Redeemed, Revoked, and Expired badges appear, matching PRD line 391. |
| Redeemed By | Yes | ✅ | Patient identifiers appear where redeemed, matching PRD line 392. |
| Redeemed At | Yes | ✅ | Redeemed timestamps appear, matching PRD line 393. |
| Discount Issued | Yes | ✅ | Currency amounts appear, matching PRD line 394. |

**Conditional States**:

- Populated affiliate-bound list is covered.
- All listed redemption statuses are visible.
- Revoke-reason modal/dialog is not shown.
- Open-code, segment-bound, individually-issued, and patient-notification revocation states are not directly evidenced by this layout set.

**Extra Elements**:

- Program summary strip, search input, row selection checkboxes, selected-count badge, per-row kebab menu, pagination, page count, page-size selector, and total-items counter appear as useful table chrome but are not listed in the Screen 5 PRD field table.

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 14/14 (100%)
**Critical Issues**: None for the default/populated manager state.

##### UX/UI Design Evaluation

**Skills invoked**: ui-ux-pro-max, web-design-guidelines

| Rule ID | Severity | Observation | Recommendation |
|---------|----------|-------------|----------------|
| U-23 | 💡 UX Suggestion | Sidebar shortens the page name to `Hairline-Funded Codes Manager`, while breadcrumb/title use `Hairline-Funded & Direct-Issued Codes Manager`. Evidence: `Hairline-Funded & Direct-Issued Codes Manager.jpg`. | Align navigation terminology with the page title. |
| W-08 | ⚠️ UX Improvement | Top summary strip, bulk action bar, and dense 8-column table make the screen heavy to scan. Evidence: both Screen 5 layout files. | Add stronger separation between summary, actions, and table header, or collapse lower-priority summary details. |

#### Screen 6: Admin — Promotion Analytics & Applications

**Layout**: `Promotion Analytics & Applications - Overview (Analytics).jpg`, `Promotion Analytics & Applications - Overview (Analytics)-1.jpg`, `Fulltable overview_Promotion Analytics & Applications (Admin).jpg`, `Fulltable overview_Promotion Analytics & Applications.jpg`

##### Flow Context

- **User arrives from**: Admin analytics navigation, Screen 1 `View Applications`, or KPI drill-down.
- **Screen purpose**: Combined analytics and redemption-log surface preserving Applied vs Completed lifecycle states.
- **Entry point**: Present — Overview and Applications tabs are visible.
- **Exit path**: Partially present — Applications row actions exist, but confirmation/reason states are not shown.
- **Data continuity**: Mostly correct — Overview KPIs are represented and the new admin full-table file shows the redemption-log source columns and distinct lifecycle state.
- **Flow context issues**: KPI drill-to-filter state and reverse/refund/void confirmation states are still not represented.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Overview tab | Yes | ✅ | `Promotion Analytics & Applications - Overview (Analytics).jpg` shows Overview selected, matching PRD line 415. |
| Applications tab | Yes | ✅ | `Promotion Analytics & Applications - Overview (Analytics)-1.jpg` shows Applications selected, matching PRD line 429. |
| Date range filter | Yes | ✅ | `Last 30 days` dropdown appears, matching PRD line 427. |
| Program type filter | Yes | ✅ | `All Types` dropdown appears, matching PRD line 427. |
| Funding model filter | Yes | ✅ | `All Models` dropdown appears, matching PRD line 427. |
| Provider filter | Yes | ✅ | `All Providers` dropdown appears, matching PRD line 427. |
| Region filter | Yes | ✅ | `All Region` dropdown appears, matching PRD line 427. |
| Active Programs KPI | Yes | ✅ | Active Programs card with type breakdown appears, matching PRD line 419. |
| Total Redemptions KPI | Yes | ✅ | Total Redemptions card with 7/30/90/365 toggle appears, matching PRD line 420. |
| Total Discount Value Issued KPI | Yes | ✅ | Currency KPI with Hairline/provider split appears, matching PRD line 421. |
| Redemption Funnel | Yes | ✅ | Funnel shows Issued → Code Entered → Validated → In-Progress → Completed, matching PRD line 422. |
| ROI by Program Type | Yes | ✅ | Chart appears, matching PRD line 423. |
| Top 10 Programs by Redemptions | Yes | ✅ | Ranked chart appears, matching PRD line 424. |
| Top 10 Programs by Discount Value | Yes | ✅ | Ranked chart appears, matching PRD line 425. |
| KPI drill to Applications tab | Yes | ⚠️ | PRD line 456 requires KPI drill filtering; no clickable cue or filtered-result state is visible. |
| Redemption ID | Yes | ✅ | `Fulltable overview_Promotion Analytics & Applications (Admin).jpg` shows Redemption ID, matching PRD line 435. |
| Code | Yes | ✅ | Code column appears, matching PRD line 436. |
| Program | Yes | ✅ | `Fulltable overview_Promotion Analytics & Applications (Admin).jpg` shows a separate Program column with name + type, matching PRD line 437. |
| State | Yes | ✅ | New full-table files show a distinct `Applied` / `Completed` state column separate from Status, matching PRD line 438 and rule at line 454. |
| Patient | Yes | ✅ | `Fulltable overview_Promotion Analytics & Applications (Admin).jpg` shows Patient identifiers, matching PRD line 439. |
| Provider | Yes | ✅ | `Fulltable overview_Promotion Analytics & Applications (Admin).jpg` shows the Provider column, matching PRD line 440. |
| Quote / Booking ID | Yes | ✅ | `Fulltable overview_Promotion Analytics & Applications (Admin).jpg` shows Quote / Booking IDs, matching PRD line 441. |
| Discount Value | Yes | ✅ | Currency value appears, matching PRD line 442. |
| Funding Split | Yes | ✅ | Hairline/provider split appears, matching PRD line 443. |
| Applied At | Yes | ✅ | Applied timestamp appears, matching PRD line 444. |
| Completed At | Yes | ✅ | Completed timestamp/blank marker appears, matching PRD line 445. |
| Status | Yes | ✅ | Active/Reversed/Refunded/Voided chips appear, matching PRD line 446. |
| View Detail | Yes | ⚠️ | Menu shows `View` in `Promotion Analytics & Applications - Overview (Analytics)-1.jpg`; function is present but less explicit than PRD line 447. |
| Reverse | Yes | ❌⚠️ | The visible menu still shows `Reversed`, a state label instead of action label `Reverse` from PRD line 447. |
| Refund | Yes | ✅ | Refund action appears, matching PRD line 447. |
| Void | Yes | ✅ | Void action appears, matching PRD line 447. |
| Mandatory reason + FR-017 reconciliation | Yes | ⚠️ | Required by PRD line 455; no confirmation/reason state is shown in any supplied file. |

**Conditional States**:

- Overview 30-day default is visible.
- Completed At blank state is visible for incomplete rows.
- Distinct `Applied` and `Completed` state chips are now visible in the new full-table files.
- Reverse/refund/void confirmation and mandatory reason state is not shown.
- Empty/loading/error states are not provided.

**Extra Elements**:

- `Search code, ID`, Export button, and `Overall conversion 20%` badge appear but are not listed in the Screen 6 PRD fields.

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 31/32 pass-or-minor (96.9%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: ui-ux-pro-max, web-design-guidelines

| Rule ID | Severity | Observation | Recommendation |
|---------|----------|-------------|----------------|
| W-06 / U-08 | ⚠️ UX Improvement | The new full-table file resolves the missing columns, but the admin redemption log remains visually dense and would likely require horizontal management on narrower widths. Evidence: `Fulltable overview_Promotion Analytics & Applications (Admin).jpg`. | Keep the restored columns, but add clear horizontal-scroll affordance or table column management. |
| U-18 / U-23 / W-07 | ⚠️ UX Improvement | Destructive actions are mixed into the same kebab menu as `View`, and `Reversed` still uses state terminology instead of action terminology. Evidence: `Promotion Analytics & Applications - Overview (Analytics)-1.jpg`. | Rename `Reversed` to `Reverse`, separate destructive actions visually, and add confirmation/reason state. |

**Flow Coverage Gaps**:

- Screen 3 is missing mandatory override reason capture and destructive-action safeguard.
- Screen 4 omits required visible filters and has a screen-title mismatch.
- Screen 6 still needs explicit KPI drill-to-filter evidence plus reverse/refund/void confirmation and reason states.
- Several required confirmation/error states are not represented: Both-Fees auto-applied validation, admin override reason, revoke reason, reverse/refund/void reason.

---

### Flow PR-02/PR-05: Provider Promotion Management

**Status**: 🔴 BLOCKED — all four provider screens have layouts, and only Screen 9 still fails the FR contract.
**Screens required**: 4
**Layout files**: `Admin Campaigns - Pending.jpg`, `Admin Campaigns - Active.jpg`, `Admin Campaigns - Active-1.jpg`, `My Promotions.jpg`, `Filter_My Promotions (Providers).jpg`, `Fulltable overview_My Promotions (Providers).jpg`, `New Promotion_Edit Promotion.jpg`, `Promotion Analytics & Applications - Overview (Analytics - Provider).jpg`, `Promotion Analytics & Applications - Applications (Redemption Log).jpg`, `Fulltable overview_Promotion Analytics & Applications (Provider).jpg`

#### Screen 7: Provider — Admin Campaigns

**Layout**: `Admin Campaigns - Pending.jpg`, `Admin Campaigns - Active.jpg`, `Admin Campaigns - Active-1.jpg`

##### Flow Context

- **User arrives from**: Provider PR-02 / PR-05 navigation.
- **Screen purpose**: Provider inbox/hub for admin-originated campaigns, including pending decisions, accepted adoptions, and past outcomes.
- **Entry point**: Present — dedicated provider navigation item and page shell are visible.
- **Exit path**: Present for Accept / Decline / Revoke Adoption actions, but the revoke-reason confirmation state is not shown.
- **Data continuity**: Correct — the same campaign card structure is preserved across Pending, Active, and Past states with timestamped decision history.
- **Flow context issues**: Required revoke-with-reason confirmation is not represented.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Pending tab | Yes | ✅ | `Admin Campaigns - Pending.jpg` shows the Pending tab with count. |
| Active tab | Yes | ✅ | `Admin Campaigns - Active.jpg` shows the Active tab with count. |
| Past tab | Yes | ✅ | `Admin Campaigns - Active-1.jpg` shows the Past tab, despite the filename. |
| Program Name | Yes | ✅ | Campaign names are visible in all three states. |
| Description | Yes | ✅ | Each card includes descriptive copy under the title. |
| Discount Type / Value | Yes | ✅ | Discount summary is visible on each card. |
| Active Window | Yes | ✅ | Date ranges are visible on all states. |
| Financial Impact Preview | Yes | ✅ | Impact preview is shown on Pending, Active, and Past cards. |
| Decision Buttons (Pending tab) | Yes | ✅ | `Accept Campaign` and `Decline` CTAs are present in the Pending state. |
| Revoke Adoption (Active tab) | Yes | ✅ | `Revoke Adoption` CTA is present in the Active state. |
| Decision Timestamp | Yes | ✅ | Accepted / Declined / Auto-Declined / Revoked timestamps are visible. |
| Revoke reason state | Conditional | ❌ | No modal, drawer, or inline reason capture is shown for the revoke flow. |

**Conditional States**:

- Pending, Active, and Past states are represented.
- Auto-Declined and Revoked-by-Provider examples are represented in the Past tab.
- Revoke Adoption reason capture is not represented.

**Extra Elements**:

- `Applies To` and deadline badges appear on the cards; these enrich the handoff and do not conflict with the FR.

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 11/12 pass-or-minor (91.7%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: ui-ux-pro-max, web-design-guidelines

| Rule ID | Severity | Observation | Recommendation |
|---------|----------|-------------|----------------|
| U-19 / W-07 | ⚠️ UX Improvement | The destructive `Revoke Adoption` action is visible, but the reason-confirmation state required by the flow is not supplied. Evidence: `Admin Campaigns - Active.jpg`. | Add the revoke confirmation/reason state so providers can see how the required comment is captured before the action is executed. |

#### Screen 8: Provider — My Promotions (List)

**Layout**: `My Promotions.jpg`, `Filter_My Promotions (Providers).jpg`, `Fulltable overview_My Promotions (Providers).jpg`

##### Flow Context

- **User arrives from**: Provider PR-02 / PR-05 navigation.
- **Screen purpose**: List every provider self-created promotion and provide management actions.
- **Entry point**: Present — provider navigation, page title, and list/table shell are visible.
- **Exit path**: Present — row action menu supports edit/pause/archive/application drill-in, but a paused-row Resume capture is not shown.
- **Data continuity**: Correct — the table shows provider-owned promotions with status, redemption count, and savings totals.
- **Flow context issues**: Resume state is implied by paused rows but not explicitly shown in an open menu state.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Filter Bar: Status | Yes | ✅ | `Filter_My Promotions (Providers).jpg` shows Status filter control. |
| Filter Bar: Date Range | Yes | ✅ | `Filter_My Promotions (Providers).jpg` shows date-range control. |
| Filter Bar: Keyword Search | Yes | ✅ | `My Promotions.jpg` shows search-by-name-or-code input. |
| Promotion Name | Yes | ✅ | Name column is visible. |
| Code | Yes | ✅ | Code column is visible, including `—` for no-code promotions. |
| Type / Value | Yes | ✅ | `Fulltable overview_My Promotions (Providers).jpg` shows type/value combinations. |
| Applies To | Yes | ✅ | Applies To column is visible. |
| Active Window | Yes | ✅ | Active window column is visible. |
| Status | Yes | ✅ | Draft, Active, Paused, and Expired states are visible. |
| Redemptions | Yes | ✅ | Redemptions column is visible. |
| Savings Issued | Yes | ✅ | Savings Issued column is visible. |
| Row Actions | Yes | ⚠️ | Edit, Pause, Archive, and View application are shown, but an explicit Resume menu state for a paused row is not supplied. |

**Conditional States**:

- Active, Draft, Paused, and Expired rows are represented.
- Filter state is represented in a separate file.
- Resume action is implied by paused rows but not explicitly captured.

**Extra Elements**:

- `+ New Promotion` CTA is visible and aligns with the provider flow.

**Screen Status**: 🟢 GOOD
**Field Coverage**: 12/12 pass-or-minor (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: ui-ux-pro-max, web-design-guidelines

| Rule ID | Severity | Observation | Recommendation |
|---------|----------|-------------|----------------|
| W-06 | 💡 UX Suggestion | The supplied action-menu state is attached to an active row only; a paused-row `Resume` state is not shown. Evidence: `My Promotions.jpg`. | Add one paused-row action-menu capture so the developer handoff covers the full lifecycle action set explicitly. |

#### Screen 9: Provider — Promotion Detail (Create / Edit)

**Layout**: `New Promotion_Edit Promotion.jpg`

##### Flow Context

- **User arrives from**: Provider My Promotions list or inline FR-004 quote creation modal.
- **Screen purpose**: Provider creates/edits a self-created promotion, either reusable or ad-hoc quote-bound.
- **Entry point**: Present for Mode 1 standalone creation — provider shell, `My Promotions` breadcrumb, and create form are visible.
- **Exit path**: Present for standalone draft/publish flow; missing for Mode 2 inline quote-bound flow.
- **Data continuity**: Partial — standalone form data is represented, but quote-bound context and reusable-toggle behavior are missing.
- **Flow context issues**: The file only covers Mode 1. Mode 2 inline creation from FR-004 is not represented.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Promotion Name | Yes | ✅ | `New Promotion_Edit Promotion.jpg` shows the Promotion Name input. |
| Description | No | ✅ | Description textarea is visible. |
| Discount Type | Yes | ✅ | Discount Type select is visible. |
| Value | Yes | ✅ | Value field is visible. |
| Applies To | Yes | ✅ | Applies To select is visible. |
| Code | Optional | ✅ | Code input is visible in the Distribution section. |
| Application Mode | Yes | ❌⚠️ | The layout shows a `Distribution` dropdown with `Code only entry`, but does not clearly expose the full `List-selection / Code-only / Either` Application Mode contract. |
| Start / End Date | Yes | ✅ | Start / End Date control is visible. |
| Total Usage Limit | No | ✅ | Total Usage Limit field is visible. |
| Per-User Usage Limit | No | ✅ | Per-User Usage Limit field is visible. |
| Save as reusable | Mode 2 only | ❌ | No inline Mode 2 state or `Save as reusable` toggle is provided. |
| Funding Model fixed Provider Only | Yes | ❌ | No explicit fixed `Provider Only` field is shown in the provider-owned layout. |
| No admin approval required | Yes | ✅ | Provider shell and direct Publish CTA are shown; no approval workflow is visible. |
| Mode 1 standalone reusable behavior | Yes | ✅ | Standalone provider create flow is represented. |
| Mode 2 quote-bound behavior | Yes | ❌ | No quote-bound modal, bound quote context, or ad-hoc save behavior is shown. |

**Conditional States**:

- Mode 1 standalone creation is represented.
- Mode 2 inline quote-bound creation is not represented.
- `Save as reusable` toggle state is not represented.
- List-selection / Either variants of Application Mode are not represented.

**Extra Elements**:

- Form sections (`Basic Information`, `Discount Details`, `Distribution`, `Active Window & Limits`) are a helpful design grouping and do not conflict with the FR.

**Screen Status**: 🔴 FAIL
**Field Coverage**: 11/15 pass-or-minor (73.3%)
**Critical Issues**:

- Mode 2 inline quote-bound creation is missing.
- The fixed `Provider Only` funding-model contract is not shown.

##### UX/UI Design Evaluation

**Skills invoked**: ui-ux-pro-max, web-design-guidelines

| Rule ID | Severity | Observation | Recommendation |
|---------|----------|-------------|----------------|
| U-26 | 🔴 Critical UX | The supplied design shows only the standalone create page, but the FR requires a second entry mode opened inline from quote drafting. Evidence: `New Promotion_Edit Promotion.jpg`; no quote context or modal frame is present. | Add a dedicated Mode 2 inline modal layout with bound-quote context and the `Save as reusable` toggle. |
| U-23 | ⚠️ UX Improvement | `Distribution` does not clearly communicate the full Application Mode contract (`List-selection / Code-only / Either`). | Rename or supplement the control so the available provider application modes are explicit. |

#### Screen 10: Provider — Promotion Analytics & Applications

**Layout**: `Promotion Analytics & Applications - Overview (Analytics - Provider).jpg`, `Promotion Analytics & Applications - Applications (Redemption Log).jpg`, `Fulltable overview_Promotion Analytics & Applications (Provider).jpg`

##### Flow Context

- **User arrives from**: Provider analytics navigation or Screen 8 `View Applications`.
- **Screen purpose**: Provider-scoped analytics and redemption log for self-created promotions plus adopted admin campaigns.
- **Entry point**: Present — provider page shell, provider navigation, and both tabs are visible.
- **Exit path**: Present — applications rows expose provider-appropriate actions (`View Quote`, `Remove Discount`, `Replace with Different Promotion`) on unbooked quotes.
- **Data continuity**: Correct — provider-specific metrics and split views are visible, and the new full-table file shows quote/case context, patient identifiers, and distinct lifecycle state.
- **Flow context issues**: None in the supplied static states beyond the already-known absence of separate confirmation states for mutations.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Overview tab | Yes | ✅ | Provider overview tab is visible. |
| Redemptions KPI | Yes | ✅ | Redemptions KPI is visible. |
| Savings Issued | Yes | ✅ | Provider Savings Issued KPI is visible. |
| Conversion Lift vs baseline | Yes | ✅ | Conversion Lift KPI is visible. |
| ROI Estimate per program | Yes | ✅ | ROI Estimate KPI is visible. |
| Adopted-Admin vs Self-Created split | Yes | ✅ | Provider split chart is visible. |
| Top performing programs | Yes | ✅ | Top-performing-program charts are visible. |
| Applications tab | Yes | ✅ | Applications tab is visible. |
| Redemption ID | Yes | ✅ | Redemption ID column is visible. |
| Code / Program | Yes | ✅ | Code/program compound column is visible. |
| State | Yes | ✅ | `Fulltable overview_Promotion Analytics & Applications (Provider).jpg` shows a distinct `Applied` / `Completed` state column, matching the provider contract. |
| Patient | Yes | ✅ | `Fulltable overview_Promotion Analytics & Applications (Provider).jpg` shows Patient identifiers, matching the provider contract. |
| Quote / Case ID | Yes | ✅ | Quote / Case ID column is visible. |
| Discount Value | Yes | ✅ | Discount Value column is visible. |
| Applied At / Completed At | Yes | ✅ | Both timestamps are represented in one compound column. |
| Row Actions | Yes | ✅ | `View Quote`, `Remove Discount`, and `Replace with Different Promotion` are shown. |
| Remove / Replace only before booking | Conditional | ✅ | The action menu is shown on `Quote (not booked)` rows, matching the conditional rule. |
| Provider cannot reverse completed redemption | Yes | ✅ | No admin-only reverse/refund/void actions appear in the provider file. |

**Conditional States**:

- Provider overview and provider applications states are both represented.
- Unbooked quote action state is represented.
- Distinct `Applied` and `Completed` state examples are represented in the new full-table file.

**Extra Elements**:

- Provider-level filters (`Date Range`, `State`, `Program Type`, `Applied At`) appear in the applications state and are compatible with the flow.

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 18/18 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: ui-ux-pro-max, web-design-guidelines

| Rule ID | Severity | Observation | Recommendation |
|---------|----------|-------------|----------------|
| W-06 | 💡 UX Suggestion | The full provider table now satisfies the FR contract, but the combined quote/case, timestamp, and action columns still make the table visually dense. Evidence: `Fulltable overview_Promotion Analytics & Applications (Provider).jpg`. | Keep the restored columns, but consider column management or responsive table behavior for narrower widths. |

**Flow Coverage Gaps**:

- Screen 7 needs the revoke-reason confirmation state.
- Screen 8 needs one explicit paused-row `Resume` action state.
- Screen 9 still lacks the inline quote-bound Mode 2 flow and fixed Provider Only field treatment.

---

## Action Items

| Priority | Flow | Screen | Issue | Recommendation |
|----------|------|--------|-------|----------------|
| 🔴 Critical | A-06 | Screen 3 | Admin override actions still have no visible mandatory reason-capture state. | Add confirmation/reason states for Force-Revoke, Re-invite, and Mark Exempt. |
| 🔴 Critical | A-06 | Screen 4 | Portfolio contract is still incomplete: required filter states are not visible and the primary title remains mismatched. | Show Record Type / Status / Date Range filter states and align the visible page title to `Provider Promotion Portfolio`. |
| ⚠️ Important | A-06 | Screen 6 | Reverse/refund/void confirmation and mandatory reason state are still not shown, and the visible menu still uses `Reversed` instead of `Reverse`. | Keep the restored full redemption-log schema, but add confirmation/reason states and align the action label to `Reverse`. |
| 🔴 Critical | PR-02/PR-05 | Screen 9 | Provider create/edit flow still misses Mode 2 inline quote-bound creation and does not show the fixed `Provider Only` funding contract. | Add the FR-004 inline modal variant, `Save as reusable` toggle, and explicit Provider Only treatment. |
| ⚠️ Important | A-06 | Screen 1 | Program Type, Scope, Status, and Funding Model filters are still presented as single-select controls instead of multi-select controls. | Redesign those filters as visible multi-select controls. |
| ⚠️ Important | A-06 | Screen 1 | Usage values still mix ratios with `Not started` / `-` instead of a consistent redeemed-count-vs-limit presentation. | Normalize Usage formatting or document the intentional exception explicitly. |
| ⚠️ Important | A-06 | Screen 5 | Revoke-reason state is not shown for direct-issued code revocation. | Add a revoke confirmation/reason layout, especially for `In-Progress` cancellation. |
| ⚠️ Important | PR-02/PR-05 | Screen 7 | Revoke Adoption reason capture is not shown. | Add the revoke confirmation/reason state to complete the provider flow. |
| 💡 Suggestion | PR-02/PR-05 | Screen 8 | The supplied list screens do not explicitly show the paused-row `Resume` action state. | Add one paused-row menu capture for full lifecycle handoff coverage. |
| 💡 UX Suggestion | A-06 | Screens 4, 5 | Terminology drift remains in some titles/sidebar labels. | Align titles and navigation labels with the FR screen names. |

### Priority Legend

- **Critical**: Blocks flow progression, breaks data integrity, or causes security/legal risk. Must fix before development.
- **Critical UX**: Severe usability issue that would prevent users from completing the flow or cause significant confusion. Must fix before development.
- **Important**: Functional discrepancy that could cause user confusion or require rework during development. Should fix before development.
- **UX Improvement**: Usability or design quality issue that deviates from platform conventions or best practices. Should fix before development.
- **Suggestion**: Cosmetic or minor improvement. Can fix anytime.
- **UX Suggestion**: Minor design enhancement that would improve polish. Can fix anytime.

---

## Notes

- Source requirement document: `local-docs/project-requirements/functional-requirements/fr019-promotions-discounts/prd.md`
- Verification used FR-019 PRD sections `Business Workflows` and `Screen Specifications`, plus a fresh `layout-temp/` inventory on 2026-05-21.
- No JSON exports were provided; all layout evidence came from JPG files in `layout-temp/`.
- This revision corrects the previous report's false `NO DESIGN` classification for Provider Screens 7, 8, and 10, and remaps Provider Screen 9 to `New Promotion_Edit Promotion.jpg` instead of the admin-owned `Provider Only` variant under Screen 2.
- `Admin Campaigns - Active-1.jpg` is treated as the Past-tab state based on visible content, not its filename.
- Generic files `Filter.jpg` and `Fulltable overview.jpg` were cataloged as unmapped because filenames/content mapping could not be tied to a specific FR-019 screen without guessing.
