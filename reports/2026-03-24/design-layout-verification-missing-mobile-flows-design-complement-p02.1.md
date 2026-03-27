# Design Layout Verification Report — Missing Mobile Flows Design Complement

**Report Date**: 2026-03-24
**Report Type**: Design Layout Verification
**FR Scope**: FR-005
**Flow Scope**: P02.1 Compare Offers Side-by-Side
**Layout Source**: `layout-temp/`
**Platform**: Patient Mobile App
**Status**: 🟡 PARTIAL
**Approval Status**: 🟢 Approved with minor issues

---

## Summary Dashboard

| # | Flow | Module | Screens Required | Screens Verified | Layout Status | Field Coverage |
|---|------|--------|-----------------|-----------------|---------------|----------------|
| P02.1 | Compare Offers Side-by-Side | P-02: Quote Request & Management | 1 | 1 | 🟡 PARTIAL | 13/18 (~72%) |

**Overall**: 1 of 1 flows verified. The layout set covers the quote-list and side-by-side comparison mechanics, but it does not evidence the full inquiry-dashboard context required by the spec. The remaining issues are accepted as minor for now.
**Screens**: 1 of 1 specified screens have layouts (100% screen coverage).

---

## Layout File Inventory

### Mapped to Spec Flows

| Layout File | Maps to Flow | Maps to Screen | Notes |
|-------------|-------------|----------------|-------|
| `layout-temp/Compare Offers.jpg` | P02.1 | P02.1-S1 | Comparison view candidate with side-by-side offer cards |
| `layout-temp/Compare Offers Table.jpg` | P02.1 | P02.1-S1 | Comparison table / expanded detail candidate |
| `layout-temp/Full table.jpg` | P02.1 | P02.1-S1 | Full-width comparison-table state candidate |

### Unmapped Files

| Layout File | Likely Purpose | Notes |
|-------------|---------------|-------|
| `layout-temp/Cancel Inquiry_.jpg` | P02.2 confirmation modal | Outside P02.1 scope |
| `layout-temp/Cancel Inquiry_ - ERROR.jpg` | P02.2 modal error state | Outside P02.1 scope |
| `layout-temp/Cancellation Success Confirmation.jpg` | P02.2 success screen | Outside P02.1 scope |
| `layout-temp/Expired Offers/Offer single.jpg` | P02.3 inquiry detail state | Outside P02.1 scope |
| `layout-temp/Expired Offers/Offer single - Floating Button - Expired.jpg` | P02.3 inquiry detail expired state | Outside P02.1 scope |
| `layout-temp/Expired Offers/Offers - Expired.jpg` | P02.3 quote-list expired state | Outside P02.1 scope |
| `layout-temp/Expired Offers/Offers - All Quotes Expired State.jpg` | P02.3 all-expired state | Outside P02.1 scope |
| `layout-temp/Cancellation policy.jpg` | P02.4 document viewer | Outside P02.1 scope |
| `layout-temp/Cancellation policy - Table of content open.jpg` | P02.4 document viewer variant | Outside P02.1 scope |
| `layout-temp/Cancellation policy - Scroll Progress Indicator.jpg` | P02.4 document viewer variant | Outside P02.1 scope |

---

## Detailed Verification by Flow

---

### Flow P02.1: Compare Offers Side-by-Side

**Status**: 🟡 PARTIAL — comparison mechanics are designed, but several required inquiry-context elements and state branches are not evidenced in the current layouts
**Approval**: 🟢 Approved with minor issues — remaining findings are accepted as minor and do not need revisit at this stage
**Screens required**: 1
**Layout files**: `Compare Offers.jpg`, `Compare Offers Table.jpg`, `Full table.jpg`

#### Screen P02.1-S1: Inquiry Dashboard with Quote Comparison (Enhanced)

**Layout**: `layout-temp/Compare Offers.jpg`, `layout-temp/Compare Offers Table.jpg`, `layout-temp/Full table.jpg`

##### Flow Context

- **User arrives from**: Inquiry Dashboard / quote list entry point, per the flow diagram in `missing-mobile-flows-design-complement.md:429`
- **Screen purpose**: Let the patient review received quotes inside the inquiry dashboard, select up to three eligible quotes, and compare them side by side before viewing details or accepting one
- **Entry point**: Partially present. The layouts clearly show the quote-list and compare-selection area, but they do not evidence the broader inquiry-dashboard context referenced in the spec
- **Exit path**: Present for the main happy path. The layouts show `Compare Offers`, `Accept`, and `View details` actions, but there is no explicit evidence of the blocked 4th-selection branch or disabled expired/withdrawn selection behavior
- **Data continuity**: Partial. Quote-level comparison data is shown, but inquiry-level context such as stage, timeline, summary, and medical alerts is not evidenced
- **Flow context issues**: Missing visual evidence for the underlying inquiry dashboard context and the max-3-selection warning/disabled-state branches defined in the flow diagram

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Screen Context | Yes | ⚠️ | The layouts clearly show an offers/comparison experience, but the visible title is `Offers` / `Compare Offers Table` rather than an explicit enhanced inquiry-dashboard context |
| Current Stage | Yes | ❌ | No inquiry-stage badge (Inquiry / Quoted / Accepted / Cancelled / etc.) is visible in any provided layout |
| Timeline | Yes | ❌ | No chronological inquiry-status timeline is evidenced in `Compare Offers.jpg`, `Compare Offers Table.jpg`, or `Full table.jpg` |
| Inquiry Summary | Yes | ❌ | No read-only inquiry summary block is visible in the current layouts |
| Medical Alerts | Yes | ❌ | No medical-risk chips or alert indicators are visible in the current layouts |
| Deadlines | Yes | ❌ | The quote cards show quote expiry timing, but no inquiry-level response/expiry deadline block is evidenced |
| Next Actions | Yes | ✅ | The layouts show clear actionable controls including `Compare Offers`, `Accept`, and `View details` tied to the quote review/acceptance flow |
| Treatment | Yes | ✅ | `Fue Hair Transplant` / provider treatment names are visible in the quote card and comparison views |
| Inclusions | No | ✅ | `Compare Offers.jpg` shows a `What's include` section listing package items such as medical consultation, maximum grafts, and PRP injection |
| Included Services | No | ✅ | The layouts list included services and comparison rows for medical/treatment inclusions and travel package inclusions |
| Per-date Pricing | Yes | ✅ | The comparison table shows multiple date/price cells for each quote |
| Appointment Slot (Pre-Scheduled) | Yes | ✅ | Quote comparison cards show offered treatment times such as `1-5 of Feb, 25` |
| Price per Graft | Yes | ✅ | `Compare Offers.jpg` shows `Price per Graft: $10 / Graft`, and the comparison views include a `Price per Graft` row |
| Provider Reviews | No | ✅ | Provider review rating/count is visible as `4.8` and `(20 review)` in the comparison layouts |
| Provider Credentials Summary | Yes | ✅ | Provider credentials such as `ISHRS Member • MOH Licensed` are visible |
| Expiry Timer | Yes | ✅ | `Compare Offers.jpg` shows `Remaining Time: 1 day 10 hours` for the quote card |
| Actions | Yes | ✅ | `Accept` and `View details` buttons are visible in the comparison panel; the compare bar enables the comparison action on the list state |
| Quotes Received | Yes | ✅ | `Compare Offers.jpg` states `Total 4 offer on your request a quote`, evidencing the quotes list |
| Sort & Filter | Yes | ✅ | Filter and sort controls are visible near the top (`Filter`, `Recent`) |
| Compare Selection (Per Quote) | No | ✅ | A selected-state control is visible on the quote card, and the compare bar confirms `2 offers are selected` |
| Comparison View Panel | Conditional | ✅ | The `Compare Offers Table.jpg` and `Full table.jpg` assets clearly show the rendered comparison panel |
| Comparison Differentiators | Conditional | ✅ | The comparison rows include total price, price per graft, graft count, provider reviews, appointment dates, credentials, and included services, satisfying the minimum differentiators set |

**Extra Elements**:

- None

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 13/18 (~72%)
**Critical Issues**: Inquiry-stage context, timeline, inquiry summary, medical alerts, and inquiry-level deadlines are not evidenced in the provided layouts

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-09 Text readability`, `M-08 Single-column layout`: the `Compare Offers Table.jpg` mobile view compresses dense multi-column comparison content into very small text, making the table hard to scan on a phone-sized layout | Rework the mobile comparison view into a more readable stacked-card or horizontally paged comparison pattern with larger text and clearer column separation |
| 💡 UX Suggestion | `U-11 Label clarity`: the heading/copy uses inconsistent phrasing such as `What's include`, `Total 4 offer on your request a quote`, and `(20 review)` | Normalize copy to clearer patient-facing grammar before final sign-off |

**Flow Coverage Gaps**:

- No layout evidences the required inquiry-level dashboard context fields: current stage, timeline, inquiry summary, medical alerts, and inquiry-level deadlines
- No layout evidences the explicit `Maximum 3 quotes for comparison` warning branch when a patient attempts a 4th selection
- No layout evidences expired/withdrawn quotes rendered as disabled for comparison selection on this screen

---

## Action Items

| Priority | Flow | Screen | Issue | Recommendation |
|----------|------|--------|-------|----------------|
| 🔴 Critical | P02.1 | P02.1-S1 | Required inquiry-dashboard context is missing from the current layouts | Add visible inquiry-stage, timeline, inquiry summary, medical-alert, and inquiry-deadline sections so the screen matches the enhanced dashboard spec instead of only the quote comparison area |
| ⚠️ Important | P02.1 | P02.1-S1 | Max-3 selection warning branch is not evidenced | Add a state or interaction design showing the `Maximum 3 quotes for comparison` message when a 4th quote is selected |
| ⚠️ Important | P02.1 | P02.1-S1 | Disabled-state handling for expired/withdrawn quotes is not evidenced in the compare-selection UI | Add a quote-card state showing disabled compare selection and disabled accept behavior for ineligible quotes |
| ⚠️ UX Improvement | P02.1 | P02.1-S1 | Mobile comparison table is too dense and text appears too small to scan comfortably | Redesign the comparison view for mobile readability using larger text and a less compressed layout |
| 💡 Suggestion | P02.1 | P02.1-S1 | Several labels use awkward grammar | Normalize patient-facing copy across the list and comparison panel |

### Priority Legend

- **🔴 Critical**: Blocks flow progression, breaks data integrity, or causes security/legal risk. Must fix before development.
- **🔴 Critical UX**: Severe usability issue that would prevent users from completing the flow or cause significant confusion. Must fix before development.
- **⚠️ Important**: Functional discrepancy that could cause user confusion or require rework during development. Should fix before development.
- **⚠️ UX Improvement**: Usability or design quality issue that deviates from platform conventions or best practices. Should fix before development.
- **💡 Suggestion**: Cosmetic or minor improvement. Can fix anytime.
- **💡 UX Suggestion**: Minor design enhancement that would improve polish. Can fix anytime.

---

## Notes

- Verification was performed against Flow `P02.1` only
- The current layouts provide strong evidence for quote-level comparison data but not for the full enhanced inquiry-dashboard wrapper defined in the spec
- User approval was granted on 2026-03-24 to accept the remaining findings as minor and defer further revision
- Source specification: `local-docs/reports/2026-02-05/missing-mobile-flows-design-complement.md`
