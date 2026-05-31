# Design Layout Verification Report - FR-013 Screens 5-10

**Report Date**: 2026-05-27
**Report Type**: Design Layout Verification
**FR Scope**: FR-013 - Reviews & Ratings
**Screen Scope**: Screen 5 through Screen 10
**Requirement Source**: `local-docs/project-requirements/functional-requirements/fr013-reviews-ratings/prd.md`
**Layout Source**: `layout-temp/`
**Platform**: Provider Web + Admin Web
**Status**: 🟡 PARTIAL - all requested screens have layouts, but several required fields/actions are missing or mismatched.

---

## Summary Dashboard

| Screen | Platform | Layout Status | Field Coverage | Screen Status |
|---|---|---:|---:|---|
| Screen 5 - Provider Reviews List & Filters | Provider Web | Present | 8/9 required or conditional fields | 🟡 PARTIAL |
| Screen 6 - Provider Review Detail & Response | Provider Web | Present | 10/11 required or triggered fields | 🔴 FAIL |
| Screen 7 - Admin Reviews Management List | Admin Web | Present | 8/9 required fields | 🟡 PARTIAL |
| Screen 8 - Admin Review Detail, Insert & Edit | Admin Web | Present | 17/19 required or triggered fields | 🔴 FAIL |
| Screen 9 - Admin Takedown Requests Queue | Admin Web | Present | 8/10 required or triggered fields | 🔴 FAIL |
| Screen 10 - Admin Review Settings & Export | Admin Web | Present | 9/9 required or conditional fields | 🟢 COMPLETE |

**Overall**: 6 of 6 requested screens have layout coverage. 3 screens fail because critical required fields or validation-critical controls are absent or contradicted by the design.
**Critical field issues**: 5

---

## Layout File Inventory

### Mapped to Requested Screens

| Layout File | Maps to Screen | Notes |
|---|---|---|
| `Fulltable overview (Admin) (Provider list).jpg` | Screen 5 | Provider reviews table state |
| `Filter (Admin) (Provider list).jpg` | Screen 5 | Provider filter state |
| `Review.jpg` | Screen 5 | Provider profile reviews list state |
| `Review Detail & Response.jpg` | Screen 6 | Provider response composer state |
| `Review Detail & Response - Provider's Response.jpg` | Screen 6 | Provider response existing/detail state |
| `Review Management (Admin).jpg` | Screen 7 | Admin review management page |
| `Filter (Admin).jpg` | Screen 7 | Admin review filter state |
| `Fulltable overview (Admin).jpg` | Screen 7 | Admin table variant |
| `Review Detail - Patient-submitted (Admin).jpg` | Screen 8 | Existing patient-submitted detail |
| `Review Detail - Verified  Off-platform (Admin).jpg` | Screen 8 | Existing verified off-platform detail |
| `Add Review (Admin).jpg` | Screen 8 | Admin insert state |
| `Edit Review (Admin).jpg` | Screen 8 | Admin edit state |
| `Remove Review (Admin).jpg` | Screen 8 | Admin remove modal |
| `Admin Removal Reason (Admin).jpg` | Screen 8 / Screen 9 | Removal/takedown approval reason modal |
| `Takedown Requests Queue (Admin).jpg` | Screen 9 | Admin takedown queue |
| `Review Settings & Export (Admin).jpg` | Screen 10 | Admin settings and export |

### Unmapped Files

| Layout File | Likely Purpose | Notes |
|---|---|---|
| `Fulltable overview.jpg` | Provider reviews table variant | Similar to Screen 5; not required after mapped Provider list files |
| `Filter.jpg` | Provider filter variant | Similar to Screen 5; not required after mapped Provider filter file |
| `Providers Details - Review (Admin).jpg` | Admin provider detail reviews embed | Related admin context, not directly Screen 5-10 |

---

## Detailed Verification by Screen

### Screen 5: Provider - Reviews List & Filters

**Spec evidence**: PRD Screen 5 data fields, lines 302-324. Flow context: provider opens Review Detail from list to Screen 6, lines 129-137.
**Layout evidence**: `Fulltable overview (Admin) (Provider list).jpg`, `Filter (Admin) (Provider list).jpg`, `Review.jpg`

#### Flow Context

- **User arrives from**: Provider dashboard/profile reviews section.
- **Screen purpose**: Show published provider reviews across treatment cases and allow filtering.
- **Entry point**: Present. `Review.jpg` shows Provider Profile > Reviews tab and `Fulltable overview (Admin) (Provider list).jpg` shows the provider review table.
- **Exit path**: Present. Row action / `View detail` affordance opens detail.
- **Data continuity**: Partial. Treatment/case context is present in table variants, but the Provider Profile list variant omits some management columns.

#### Field Verification

| Field | Required | Layout | Notes |
|---|---:|---|---|
| Ratings summary | Yes | ✅ | `Review.jpg` shows average rating `4.6`, count `128 reviews`, and distribution; matches spec row `Ratings summary`. |
| Review list | Yes | ✅ | Provider list/table files show published review rows; matches spec row `Review list`. |
| Review source type | Yes | ✅ | `Patient-submitted` and `Verified Off-platform` badges visible; matches spec row `Review source type`. |
| Reviewer alias | Yes | ❌⚠️ | Aliases like `Sarah M.` appear, but `Fulltable overview (Admin) (Provider list).jpg` also exposes patient email addresses, which conflicts with the spec's no-PII alias rule. |
| Case/treatment context | Yes | ✅ | Case IDs and treatment/procedure names visible in provider table variants; matches spec row `Case/treatment context`. |
| Response status | Yes | ✅ | `Responded` / `No response` visible; matches spec row `Response status`. |
| Filters | No | ✅ | `Filter (Admin) (Provider list).jpg` includes Patient, Treatment Case, Status, Date Range, Rating Range, Source Type, Flagged Status. |
| Sort | No | ⚠️ | Sort/column option icons appear, but current sort state is not explicit; spec default is recency. |
| Open detail | Yes | ✅ | Row action / `View detail` affordance visible; matches navigation to Screen 6. |

**Extra Elements**:

- `Status` and `Flagged` appear in provider table variants. These are useful moderation/status fields but not listed in Screen 5 provider spec.
- Patient email appears under reviewer alias, which is not allowed by the Screen 5 no-PII rule.

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 8/9 required or conditional fields (89%)
**Critical Issues**: Reviewer alias includes visible email in a provider-facing list.

#### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`
**Platform checks applied**: Universal + Web

| Rule ID | Check | Severity | Finding | Evidence |
|---|---|---|---|---|
| U-13 | Text contrast | ⚠️ UX Improvement | Placeholder text in filter inputs appears very light and likely below WCAG body-text contrast. | `Filter (Admin) (Provider list).jpg` - `Select`, `Start date`, `End date`, `Min`, `Max` placeholders are light grey on white. |
| U-11 | Label clarity | ⚠️ UX Improvement | Rating range uses calendar icons, which suggests a date picker rather than numeric rating input. | `Filter (Admin) (Provider list).jpg` - calendar icon appears in `Rating Range`. |
| W-06 | Table design | ⚠️ UX Improvement | Provider table relies on ambiguous vertical ellipsis icons in headers without clear sort/filter state. | `Fulltable overview (Admin) (Provider list).jpg` - header icons next to most columns do not indicate sort direction or filter state. |
| W-06 | Table design | ⚠️ UX Improvement | Pagination is not visible in the provider table image even though the spec requires paginated list behavior. | `Fulltable overview (Admin) (Provider list).jpg` - visible scrollbar but no page controls. |

---

### Screen 6: Provider - Review Detail & Response

**Spec evidence**: PRD Screen 6 data fields, lines 333-365. Flow context: B1 Provider Response, lines 129-137.
**Layout evidence**: `Review Detail & Response.jpg`, `Review Detail & Response - Provider's Response.jpg`

#### Flow Context

- **User arrives from**: Screen 5 review row/detail action.
- **Screen purpose**: Inspect review details and submit or view a public provider response.
- **Entry point**: Present. Back to All Reviews is visible.
- **Exit path**: Partial. A submit action is visible in composer state, but no cancel response action is visible.
- **Data continuity**: Present for review payload, reviewer, rating, treatment context, and photos.

#### Field Verification

| Field | Required | Layout | Notes |
|---|---:|---|---|
| Review detail payload | Yes | ✅ | Ratings, feedback, photos, case/treatment context visible in both detail files. |
| Review source type | Yes | ❌ | No `Patient-submitted` / `Verified Off-platform` badge is visible in the provider detail layouts. |
| Reviewer alias | Yes | ✅ | Reviewer name/label visible as `Vincze Nikolett`; matches display-label row, though alias policy should be checked for PII separately. |
| Photos | No | ✅ | Three review photo thumbnails visible. |
| Provider response card | No | ✅ | Existing response state shows a provider response card with responding entity and role. |
| Respond as Provider | Conditional | ⚠️ | Composer is visible directly; no separate `Respond as Provider` button state is shown. |
| Response composer | Conditional | ✅ | Inline composer/panel visible in `Review Detail & Response.jpg`. |
| Response text | Yes when composing | ✅ | Textarea visible. |
| Character counter | Yes when composing | ❌⚠️ | Counter shows `0 / 40`; spec requires 50-1000 chars. This contradicts validation rules. |
| Cancel response | Yes when composing | ❌ | No cancel response action visible in composer state. |
| Submit response | Yes when composing | ❌⚠️ | Submit action exists but is labeled `Submit Responde`, a typo that weakens action clarity. |

**Extra Elements**:

- Generic Provider Profile surrounding tabs and placeholder subtitle appear; these are outside the Screen 6 review-response spec.

**Screen Status**: 🔴 FAIL
**Field Coverage**: 10/11 required or triggered fields (91%), but critical validation/action mismatches fail the screen.
**Critical Issues**:

- Character counter contradicts required 50-1000 character validation.
- Cancel response action is missing in composer state.

#### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`
**Platform checks applied**: Universal + Web

| Rule ID | Check | Severity | Finding | Evidence |
|---|---|---|---|---|
| U-17 | CTA label clarity | ⚠️ UX Improvement | Submit button text has a typo: `Submit Responde`. | `Review Detail & Response.jpg` - response composer button. |
| U-19 | Error state clarity | ⚠️ UX Improvement | Composer shows a 40-character limit but no visible validation guidance for required 50-1000 chars. | `Review Detail & Response.jpg` - `0 / 40` counter beside textarea. |
| U-07 | Vertical spacing | 💡 UX Suggestion | Character counter is visually detached from the textarea, weakening association. | `Review Detail & Response.jpg` - counter appears far to the right of composer field. |
| W-04 | Breadcrumbs / page title | 💡 UX Suggestion | Detail page is nested under Provider Profile tabs; title exists, but breadcrumb still says Provider Profile rather than Reviews detail. | `Review Detail & Response.jpg` - breadcrumb `Settings & Support / Provider Profile`. |

---

### Screen 7: Admin - Reviews Management List

**Spec evidence**: PRD Screen 7 data fields, lines 370-392. Flow context: admin add/edit/takedown and flagging flows, lines 92-146.
**Layout evidence**: `Review Management (Admin).jpg`, `Filter (Admin).jpg`, `Fulltable overview (Admin).jpg`

#### Flow Context

- **User arrives from**: Admin Review Management.
- **Screen purpose**: Monitor reviews and open detail, takedown queue, or settings/export.
- **Entry point**: Present. Review Management page and Reviews List tab visible.
- **Exit path**: Partial. Detail, takedown queue, settings/export tabs are visible; row menu only shows `View detail`.
- **Data continuity**: Present for list rows and status/source/flag/response badges.

#### Field Verification

| Field | Required | Layout | Notes |
|---|---:|---|---|
| Reviews list | Yes | ✅ | Admin reviews table visible; table variants include review rows. |
| Source type | No | ✅ | `Patient-submitted` and `Verified Off-platform` visible as badges and filterable. |
| Flagged status | No | ✅ | `Flagged` badge and flagged filter visible. |
| Response status | No | ✅ | `Responded` / `No response` visible. |
| Filters | No | ✅ | `Filter (Admin).jpg` includes Provider, Patient, Treatment Case, Status, Date Range, Rating Range, Source Type, Flagged Status. |
| Search | No | ✅ | Search input visible with placeholder `Search patient`. |
| Open detail | Yes | ✅ | Row action menu shows `View detail`. |
| Open takedown queue | Yes | ✅ | `Takedown Requests Queue` tab visible. |
| Open review settings | No | ✅ | `Review Settings & Export` tab visible. |

**Extra Elements**:

- Add Review button appears on Screen 7. This aligns with Screen 8 add flow but is not listed in Screen 7's data table.
- Summary rating/distribution appears on management page; helpful but not listed in Screen 7.

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 8/9 required fields pass; screen is functionally present but has a pagination inconsistency.
**Critical Issues**: None blocking, but list pagination data is internally inconsistent.

#### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`
**Platform checks applied**: Universal + Web

| Rule ID | Check | Severity | Finding | Evidence |
|---|---|---|---|---|
| W-06 | Table design | ⚠️ UX Improvement | Pagination shows `Total 85 items`, `10 / page`, but a page `50` option; 85 items at 10/page should not yield 50 pages. | `Review Management (Admin).jpg` - pagination controls. |
| U-22 | Component consistency | 💡 UX Suggestion | `No response` is rendered as plain/neutral text in one admin list while other response/status values use badge styling. | `Review Management (Admin).jpg` - Response column. |
| U-22 | Component consistency | 💡 UX Suggestion | Filter and Add Review buttons use slightly inconsistent sizing/styling for peer toolbar actions. | `Review Management (Admin).jpg` - top-right list toolbar. |
| W-10 | Keyboard accessibility indicators | ⚠️ UX Improvement | Static layouts do not show focus states for table actions, filter controls, or pagination. | `Review Management (Admin).jpg`, `Filter (Admin).jpg`. |

---

### Screen 8: Admin - Review Detail, Insert & Edit

**Spec evidence**: PRD Screen 8 data fields, lines 395-425. Flow context: A1 Admin Inserts Authenticated Review, A2 Admin Edits Existing Review, B2 Flagging, lines 92-146.
**Layout evidence**: `Review Detail - Patient-submitted (Admin).jpg`, `Review Detail - Verified  Off-platform (Admin).jpg`, `Add Review (Admin).jpg`, `Edit Review (Admin).jpg`, `Remove Review (Admin).jpg`, `Admin Removal Reason (Admin).jpg`

#### Flow Context

- **User arrives from**: Screen 7 review row action or Add Review button.
- **Screen purpose**: Inspect existing review, edit/remove with audit reason, or insert verified off-platform review with provenance.
- **Entry point**: Present. Detail, add, edit, and remove states exist.
- **Exit path**: Present. Back, save/cancel, and remove confirmation actions are visible.
- **Data continuity**: Partial. Existing detail shows review content, status/source/flagging, and audit trail. Add state captures provenance but misses explicit attestation checkbox.

#### Field Verification

| Field | Required | Layout | Notes |
|---|---:|---|---|
| Review detail payload | Yes | ✅ | Detail, add, and edit states show review content, ratings, photos, and treatment context. |
| Source type | Yes | ✅ | Detail states show `Patient-submitted` or `Verified Off-platform`; add state has Source platform/source metadata. |
| Flagged status | No | ✅ | Existing detail states show `Flagged`. |
| Audit trail preview | Yes | ✅ | Audit Trail table visible in existing detail states. |
| Edit fields | No | ✅ | `Edit Review (Admin).jpg` shows editable feedback, photo controls, ratings, edit reason, additional details. |
| Remove review | No | ✅ | Remove Review button and modal visible. |
| Add review | No | ✅ | `Add Review (Admin).jpg` shows add form and Save Review action. |
| Source verification | Yes for add | ⚠️ | Source Verification group present, but admin attestation is text only without visible checkbox/control. |
| Source platform | Yes for add | ✅ | Dropdown visible. |
| Source URL | Conditional for add | ✅ | URL field visible with `http://` prefix. |
| Evidence file(s) | Yes for add | ✅ | Evidence file upload visible. |
| Capture date | Yes for add | ✅ | Capture date picker visible. |
| Permission record | Yes for add | ⚠️ | Upload and text-reference fields visible, but mutual exclusivity/required path is unclear. |
| Reviewer display name | Yes for add | ❌⚠️ | Field exists, but placeholder says `Treatment Name...`, which mislabels the expected reviewer alias. |
| Patient/reviewer photo | No for add | ✅ | Upload area visible. |
| Removal/edit reason | Conditional | ✅ | Edit Reason dropdown, Additional Details textarea, Remove Reason dropdown, and removal details textarea visible. |

**Extra Elements**:

- Clinic/provider and treatment name fields appear in add form; useful for review payload context but not explicitly named in Screen 8's source metadata rows.

**Screen Status**: 🔴 FAIL
**Field Coverage**: 17/19 required or triggered fields (89%), but critical compliance controls are missing/mismatched.
**Critical Issues**:

- Admin attestation text is present without a visible checkbox/control, so consent confirmation cannot be verified as an explicit required action.
- Reviewer display name field uses the wrong placeholder, risking wrong data entry for a public alias.

#### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`
**Platform checks applied**: Universal + Web

| Rule ID | Check | Severity | Finding | Evidence |
|---|---|---|---|---|
| U-11 | Label clarity | ⚠️ UX Improvement | Reviewer display name input placeholder says `Treatment Name...`, contradicting the field label. | `Add Review (Admin).jpg` - Review section. |
| U-18 | Destructive action safeguard | ⚠️ UX Improvement | Remove modal has destructive styling, but required reason is not visually marked and no validation state is shown. | `Remove Review (Admin).jpg` - Remove Reason field and Remove Review button. |
| U-17 | CTA label clarity | ⚠️ UX Improvement | Admin attestation appears as text without a checkbox, so the required confirmation action is not visually clear. | `Add Review (Admin).jpg` - attestation paragraph. |
| U-22 | Component consistency | 💡 UX Suggestion | Category rating star styles vary between detail states, with `Value` appearing visually different. | `Review Detail - Verified  Off-platform (Admin).jpg` - Category Ratings row. |
| W-05 | Form layout | ⚠️ UX Improvement | Required fields in the Add Review form are not visually marked. | `Add Review (Admin).jpg` - form labels lack `*` or required text. |

---

### Screen 9: Admin - Takedown Requests Queue

**Spec evidence**: PRD Screen 9 data fields, lines 428-454. Flow context: A4 Admin Processes Takedown Request, lines 119-126.
**Layout evidence**: `Takedown Requests Queue (Admin).jpg`, `Admin Removal Reason (Admin).jpg`

#### Flow Context

- **User arrives from**: Screen 7 `Takedown Requests Queue` tab or takedown queue entry.
- **Screen purpose**: Review patient takedown reason, inspect linked review, approve or reject with admin justification.
- **Entry point**: Present. Takedown queue tab and request list exist.
- **Exit path**: Partial. Approve/reject actions are visible, and removal reason modal exists for approval, but the base screen decision note is generic and single-line.
- **Data continuity**: Present for request metadata, linked review, current status, patient reason, and decision history.

#### Field Verification

| Field | Required | Layout | Notes |
|---|---:|---|---|
| Request queue | Yes | ✅ | Left request queue with pending/approved/rejected statuses visible. |
| Request metadata | Yes | ✅ | Requester, provider, case, created date visible in queue and detail panel. |
| Linked review preview | Yes | ✅ | Linked Review block shows status, rating, review text, and submission date. |
| Current review status | Yes | ✅ | `Published` badge visible in Linked Review. |
| Request reason | Yes | ✅ | Patient request reason appears in highlighted box. |
| Decision action | Yes | ✅ | Approve Takedown and Reject Takedown buttons visible. |
| Decision note | Yes | ❌⚠️ | Decision Note is a single-line input; spec requires textarea with 10-1000 chars. |
| Admin removal reason | Conditional | ⚠️ | `Admin Removal Reason (Admin).jpg` supplies a textarea modal, but no removal reason catalog/select is visible in that modal. |
| Decision history | No | ✅ | Decision History table visible. |
| Decision timestamp | Conditional | ✅ | Decision history includes timestamps after events. |

**Extra Elements**:

- Basic date/status filters exist; useful but not specified in Screen 9 field table.

**Screen Status**: 🔴 FAIL
**Field Coverage**: 8/10 required or triggered fields (80%)
**Critical Issues**:

- Decision note type/validation does not match the required textarea 10-1000 char justification.
- Admin removal reason modal lacks the reason catalog/select expected from Screen 10's removal reason catalog and Screen 9's approval workflow.

#### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`
**Platform checks applied**: Universal + Web

| Rule ID | Check | Severity | Finding | Evidence |
|---|---|---|---|---|
| U-17 | CTA label clarity | ⚠️ UX Improvement | Decision note is generic; approval needs a patient-facing removal reason and rejection needs a rejection reason. | `Takedown Requests Queue (Admin).jpg` - `Decision Note` field. |
| W-05 | Form layout | ⚠️ UX Improvement | Decision Note is a single-line input instead of a textarea, limiting admin justification entry. | `Takedown Requests Queue (Admin).jpg` - field under approve/reject controls. |
| U-02 | Information priority | 💡 UX Suggestion | Selected request in left queue is not visually distinct from other cards. | `Takedown Requests Queue (Admin).jpg` - first queue item feeds right detail but lacks selected styling. |
| U-23 | Terminology consistency | 💡 UX Suggestion | Date formats vary between queue/detail/history. | `Takedown Requests Queue (Admin).jpg` - `01 May 2026 · 09:12`, `Submitted 14 Jan 2026`, and `2026-05-13 09:14:22`. |
| U-18 | Destructive action safeguard | ⚠️ UX Improvement | Static queue screen does not show confirmation state for approve/reject decisions. | `Takedown Requests Queue (Admin).jpg` - approve/reject buttons visible without confirmation. |

---

### Screen 10: Admin - Review Settings & Export

**Spec evidence**: PRD Screen 10 data fields, lines 457-480. Flow context: Admin configures settings/export, user story lines 706-714.
**Layout evidence**: `Review Settings & Export (Admin).jpg`

#### Flow Context

- **User arrives from**: Screen 7 Review Settings & Export tab.
- **Screen purpose**: Configure FR-013-owned labels, photo guidance, moderation settings, takedown SLA, and export; link to FR-030 for invite/reminder cadence.
- **Entry point**: Present. Active `Review Settings & Export` tab visible.
- **Exit path**: Present. Configure, save, and export actions are visible.
- **Data continuity**: Present for settings and export controls.

#### Field Verification

| Field | Required | Layout | Notes |
|---|---:|---|---|
| Review categories/labels | Yes | ✅ | Canonical key and editable display-label table visible. |
| Invitation cadence link-out | Yes | ✅ | Current cadence plus `Configure` button visible; suitable link-out to FR-030. |
| Reminder settings link-out | No | ✅ | Reminder setting plus `Configure` button visible. |
| Photo guidelines text | Yes | ✅ | Rich text/textarea visible with guideline copy. |
| Removal reason catalog | Yes | ✅ | Active/inactive reason list, toggles, delete icons, and add-new reason input visible. |
| Reviewer display policy | Yes | ✅ | Alias-only policy box visible with collision suffix rule. |
| Flagging thresholds | No | ✅ | Duplicate, spam, and keyword threshold controls visible with safe ranges. |
| Takedown SLA settings | No | ✅ | Decision SLA and escalation threshold controls visible. |
| Export reviews report | No | ✅ | Export type, date range, file format, and Export action visible. |

**Extra Elements**:

- Multiple section-level `Save Setting` buttons; not a spec issue, but it may create ambiguity about persistence boundaries.

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 9/9 required or conditional fields (100%)
**Critical Issues**: None.

#### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`
**Platform checks applied**: Universal + Web

| Rule ID | Check | Severity | Finding | Evidence |
|---|---|---|---|---|
| U-17 | CTA label clarity | 💡 UX Suggestion | Repeated `Save Setting` buttons can make it unclear whether settings save per section or globally. | `Review Settings & Export (Admin).jpg` - multiple Save Setting buttons. |
| U-06 | Horizontal alignment | 💡 UX Suggestion | Removal reason delete icons appear slightly misaligned with their toggles. | `Review Settings & Export (Admin).jpg` - Removal Reason Catalog rows. |
| U-16 | Interactive vs static distinction | 💡 UX Suggestion | Reviewer Display Policy appears like a selected configurable block but has no visible action or disabled state. | `Review Settings & Export (Admin).jpg` - green policy box. |
| W-07 | Action placement | 💡 UX Suggestion | Export panel sits as a separate right-side block while settings content is long-form left column, which may feel detached from the active tab content. | `Review Settings & Export (Admin).jpg` - Export block at right. |

---

## Action Items

| Priority | Screen | Issue | Recommendation |
|---|---|---|---|
| 🔴 Critical | Screen 6 | Response counter shows `0 / 40`, contradicting required 50-1000 chars. | Update composer validation and counter to 50-1000 chars; block submit outside bounds. |
| 🔴 Critical | Screen 6 | Cancel response action is missing in composer state. | Add Cancel Response with unsaved-content confirmation. |
| 🔴 Critical | Screen 8 | Admin attestation lacks a visible checkbox/control. | Add required checkbox for consent attestation before Save Review is enabled. |
| 🔴 Critical | Screen 9 | Decision note is single-line and not a 10-1000 char textarea. | Replace with textarea, validation, and error state. |
| 🔴 Critical | Screen 9 | Approval flow lacks structured admin removal reason catalog in the modal. | Add reason catalog/select plus patient-facing reason textarea for approval. |
| ⚠️ Important | Screen 5 | Provider list exposes patient emails under reviewer aliases. | Remove emails from provider-facing review list; use alias-only display. |
| ⚠️ Important | Screen 8 | Reviewer display name placeholder says `Treatment Name...`. | Replace with alias-oriented placeholder such as `e.g., Sarah M.` and enforce PII-safe validation. |
| ⚠️ Important | Screen 7 | Pagination count is inconsistent with total/items per page. | Correct total-page calculation and pagination display. |
| 💡 Suggestion | Screen 10 | Repeated Save Setting buttons create persistence ambiguity. | Clarify per-section save behavior or add one Save All Settings action. |

---

## Notes

- Verification used static JPG layouts only; focus states, hover states, route behavior, and API-side validation could not be confirmed from static images.
- Claims above are limited to visible evidence in `layout-temp/` and the FR-013 PRD screen tables.
- The current design set covers every requested screen, so there are no `NO DESIGN` gaps for Screens 5-10.
