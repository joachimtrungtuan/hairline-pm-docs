# Design Layout Verification Report — Missing Mobile Flows Design Complement

**Report Date**: 2026-03-24
**Report Type**: Design Layout Verification
**FR Scope**: FR-004, FR-005
**Flow Scope**: P02.3 Expired Offers/Quotes
**Layout Source**: `layout-temp/`
**Platform**: Patient Mobile App
**Status**: 🟡 PARTIAL
**Approval Status**: 🟢 Approved with minor issues

---

## Summary Dashboard

| # | Flow | Module | Screens Required | Screens Verified | Layout Status | Field Coverage |
|---|------|--------|-----------------|-----------------|---------------|----------------|
| P02.3 | Expired Offers/Quotes | P-02: Quote Request & Management | 2 | 2 | 🟡 PARTIAL | 16/17 (~94%) |

**Overall**: 1 of 1 flows verified. The expired-quote list/detail treatment is well covered, and the all-expired state is mostly complete, but one required presentation element is still missing. The remaining issue is accepted as minor for now.
**Screens**: 2 of 2 specified screens have layouts (100% screen coverage).

---

## Layout File Inventory

### Mapped to Spec Flows

| Layout File | Maps to Flow | Maps to Screen | Notes |
|-------------|-------------|----------------|-------|
| `layout-temp/Expired Offers/Offer single.jpg` | P02.3 | P02.3-S1 | Inquiry detail with standard offer state candidate |
| `layout-temp/Expired Offers/Offer single - Floating Button - Expired.jpg` | P02.3 | P02.3-S1 | Inquiry detail expired-offer overlay/state candidate |
| `layout-temp/Expired Offers/Offers - Expired.jpg` | P02.3 | P02.3-S1 | Quote-list expired-state candidate |
| `layout-temp/Expired Offers/Offers - All Quotes Expired State.jpg` | P02.3 | P02.3-S2 | All-quotes-expired screen candidate |

### Unmapped Files

| Layout File | Likely Purpose | Notes |
|-------------|---------------|-------|
| `layout-temp/Compare Offers.jpg` | P02.1 comparison screen | Outside P02.3 scope |
| `layout-temp/Compare Offers Table.jpg` | P02.1 comparison-table state | Outside P02.3 scope |
| `layout-temp/Full table.jpg` | P02.1 comparison-table state | Outside P02.3 scope |
| `layout-temp/Cancel Inquiry_.jpg` | P02.2 confirmation modal | Outside P02.3 scope |
| `layout-temp/Cancel Inquiry_ - ERROR.jpg` | P02.2 modal error state | Outside P02.3 scope |
| `layout-temp/Cancellation Success Confirmation.jpg` | P02.2 success screen | Outside P02.3 scope |
| `layout-temp/Cancellation policy.jpg` | P02.4 document viewer | Outside P02.3 scope |
| `layout-temp/Cancellation policy - Table of content open.jpg` | P02.4 document viewer variant | Outside P02.3 scope |
| `layout-temp/Cancellation policy - Scroll Progress Indicator.jpg` | P02.4 document viewer variant | Outside P02.3 scope |

---

## Detailed Verification by Flow

---

### Flow P02.3: Expired Offers/Quotes

**Status**: 🟡 PARTIAL — the expired-quote states are largely complete, but the all-expired state is missing its required top icon treatment
**Approval**: 🟢 Approved with minor issues — remaining findings are accepted as minor and do not need revisit at this stage
**Screens required**: 2
**Layout files**: `Expired Offers/Offer single.jpg`, `Expired Offers/Offer single - Floating Button - Expired.jpg`, `Expired Offers/Offers - Expired.jpg`, `Expired Offers/Offers - All Quotes Expired State.jpg`

#### Screen P02.3-S1: Expired Quote Indicator (State Variation within Inquiry Detail)

**Layout**: `layout-temp/Expired Offers/Offer single.jpg`, `layout-temp/Expired Offers/Offer single - Floating Button - Expired.jpg`, `layout-temp/Expired Offers/Offers - Expired.jpg`

##### Flow Context

- **User arrives from**: Inquiry Dashboard after the system has marked one or more quotes as expired, per `missing-mobile-flows-design-complement.md:609-623`
- **Screen purpose**: Visually de-emphasize expired quotes while still allowing the patient to inspect them in read-only mode or contact support
- **Entry point**: Present. The list and detail assets clearly show expired quotes surfaced inside the broader offers experience
- **Exit path**: Present. The expired quote remains viewable in read-only mode, the accept action is disabled with explanatory feedback, and support access remains available
- **Data continuity**: Correct. The expired views preserve treatment name, pricing, appointment slots, provider info, and quote reference data while replacing the active countdown with an `Expired on` timestamp
- **Flow context issues**: None

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Expired Badge | Yes | ✅ | The expired states show a prominent `Expired` label / banner on the quote card |
| Card Overlay Styling | Yes | ✅ | The expired quote card uses de-emphasized styling with lighter text and muted controls compared with the active quotes shown below |
| Expiry Date Display | Yes | ✅ | The active countdown is replaced by `Expired on 12:00 June 22, 2026` in the expired states |
| Original Quote Summary | Yes | ✅ | Treatment name, appointment options, pricing, provider card, and inclusions remain visible in read-only form |
| Price per Graft | Yes | ✅ | `Offers - Expired.jpg` shows `Price per Graft: $10 / Graft` on the expired quote card |
| Provider Info | Yes | ✅ | Provider name, rating, and credentials remain visible on the expired quote card |
| Disabled Accept Button | Yes | ✅ | The expired quote shows a disabled `Accept` button and a tooltip explaining that the quote can no longer be accepted |
| Disabled Compare Checkbox | Yes | ✅ | The expired list state shows a disabled-looking selection control at the top-right of the expired quote and a tooltip when the patient attempts to interact |
| View Details Action | Yes | ✅ | `View details` remains available below the expired quote card |
| Contact Support Link | No | ✅ | Support access remains available as `Contact Support` beside `View details` in the list state |

**Extra Elements**:

- None

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 9/9 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| None | No UX/UI issues identified from the static expired-card layouts beyond the documented field coverage | None |

#### Screen P02.3-S2: All Quotes Expired State

**Layout**: `layout-temp/Expired Offers/Offers - All Quotes Expired State.jpg`

##### Flow Context

- **User arrives from**: The inquiry dashboard after the system determines that all received quotes for the inquiry have expired, per `missing-mobile-flows-design-complement.md:625-627`
- **Screen purpose**: Explain that no valid quotes remain and route the patient toward cancellation or support
- **Entry point**: Present. The screen title, explanatory message, inquiry summary, and CTA set clearly indicate the all-expired branch
- **Exit path**: Present. `Cancel Inquiry` routes to Flow `P02.2`, and `Need help? Contact support` provides the support path
- **Data continuity**: Correct. The state preserves inquiry summary details, quote count, last expiry date, and a collapsed list of expired quotes beneath the primary state block
- **Flow context issues**: The required top-centered expired-state icon is not evidenced in the provided layout

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Expired State Icon | Yes | ❌ | No clock/hourglass-style icon is visible above the `All Quotes Have Expired` title in `Offers - All Quotes Expired State.jpg` |
| State Title | Yes | ✅ | `All Quotes Have Expired` is displayed prominently at the top |
| Explanation Message | Yes | ✅ | The explanatory message tells the patient the quotes have expired and suggests cancelling the inquiry or contacting support |
| Inquiry Summary | Yes | ✅ | The `Inquiry Summary` block includes treatment type, submission date, and number of expired quotes |
| Expired Quotes Count | Yes | ✅ | `Number of expired quotes: 4` is shown in the summary block |
| Last Expiry Date | Yes | ✅ | `Last Expiry Date: 12:00 June 22, 2026` is visible below the summary |
| Cancel Inquiry Button | Yes | ✅ | `Cancel Inquiry` is shown as the primary CTA |
| Contact Support Link | Yes | ✅ | `Need help? Contact support` is visible as the support action |

**Extra Elements**:

- Collapsed expired quote cards remain visible below the primary state block for reference, matching the business-rule expectation

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 7/8 (88%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| None | No standalone UX/UI issues were identified beyond the missing top icon. The hierarchy, messaging, and CTA separation are otherwise clear | None |

**Flow Coverage Gaps**:

- The all-expired state is missing the required top-centered expired-state icon / illustration

---

## Action Items

| Priority | Flow | Screen | Issue | Recommendation |
|----------|------|--------|-------|----------------|
| ⚠️ Important | P02.3 | P02.3-S2 | Required expired-state icon is missing from the top of the all-expired state | Add the specified neutral clock/hourglass icon above the title to complete the state design |

### Priority Legend

- **🔴 Critical**: Blocks flow progression, breaks data integrity, or causes security/legal risk. Must fix before development.
- **🔴 Critical UX**: Severe usability issue that would prevent users from completing the flow or cause significant confusion. Must fix before development.
- **⚠️ Important**: Functional discrepancy that could cause user confusion or require rework during development. Should fix before development.
- **⚠️ UX Improvement**: Usability or design quality issue that deviates from platform conventions or best practices. Should fix before development.
- **💡 Suggestion**: Cosmetic or minor improvement. Can fix anytime.
- **💡 UX Suggestion**: Minor design enhancement that would improve polish. Can fix anytime.

---

## Notes

- Verification was performed against Flow `P02.3` only
- The expired quote list/detail treatment is materially aligned with the spec; the remaining gap is a small but required presentation element on the all-expired state
- User approval was granted on 2026-03-24 to accept the remaining finding as minor and defer further revision
- Source specification: `local-docs/reports/2026-02-05/missing-mobile-flows-design-complement.md`
