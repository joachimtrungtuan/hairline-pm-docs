# Design Layout Verification Report — Missing Mobile Flows Design Complement

**Report Date**: 2026-03-24
**Report Type**: Design Layout Verification
**FR Scope**: FR-020
**Flow Scope**: P06.1 Notification Listing & Bubble
**Layout Source**: `layout-temp/`
**Platform**: Patient Mobile App
**Status**: 🟡 PARTIAL
**Approval Status**: 🟢 Approved with minor issues

---

## Summary Dashboard

| # | Flow | Module | Screens Required | Screens Verified | Layout Status | Field Coverage |
|---|------|--------|-----------------|-----------------|---------------|----------------|
| P06.1 | Notification Listing & Bubble | P-06: Communication | 2 | 2 | 🟡 PARTIAL | 16/20 (80%) |

**Overall**: 1 of 1 flows verified. The notification bubble component is broadly aligned, but the delivered notification list diverges from the required back-navigation, filter-chip, and unread-state behavior.
**Screens**: 2 of 2 specified screens have layouts (100% screen coverage).

---

## Layout File Inventory

### Mapped to Spec Flows

| Layout File | Maps to Flow | Maps to Screen | Notes |
|-------------|-------------|----------------|-------|
| `layout-temp/Notification - Not any unread notification.jpg` | P06.1 | P06.1-S1 | Bubble component state with zero unread notifications |
| `layout-temp/Notification - Having unread notification.jpg` | P06.1 | P06.1-S1 | Bubble component state with unread badge visible |
| `layout-temp/Notification - Very high counts unread notification.jpg` | P06.1 | P06.1-S1 | Bubble component state showing capped high-count badge |
| `layout-temp/Notification list.jpg` | P06.1 | P06.1-S2 | Default populated notification list candidate |
| `layout-temp/Notification list - Empty.jpg` | P06.1 | P06.1-S2 | Empty-state candidate |
| `layout-temp/Notification list - Filter.jpg` | P06.1 | P06.1-S2 | Filter interaction state candidate |
| `layout-temp/Notification list - Apply Filter.jpg` | P06.1 | P06.1-S2 | Filtered-results state candidate |
| `layout-temp/Notification categories.jpg` | P06.1 | P06.1-S2 | Category/filter taxonomy state candidate |
| `layout-temp/Swipe Actions.jpg` | P06.1 | P06.1-S2 | Swipe-left action state candidate |

### Unmapped Files

| Layout File | Likely Purpose | Notes |
|-------------|---------------|-------|
| None | None | All current files in `layout-temp/` appear to map to P06.1 verification scope |

---

## Detailed Verification by Flow

---

### Flow P06.1: Notification Listing & Bubble

**Status**: 🟡 PARTIAL — both required screens are designed, but the notification list does not fully match the specified navigation and filtering model
**Approval**: 🟢 Approved with minor issues — the flow is accepted for design sign-off, with the remaining list-screen mismatches documented for follow-up
**Screens required**: 2
**Layout files**: `Notification - Not any unread notification.jpg`, `Notification - Having unread notification.jpg`, `Notification - Very high counts unread notification.jpg`, `Notification list.jpg`, `Notification list - Empty.jpg`, `Notification list - Filter.jpg`, `Notification list - Apply Filter.jpg`, `Notification categories.jpg`, `Swipe Actions.jpg`

#### Screen P06.1-S1: Notification Bubble Component

**Layout**: `layout-temp/Notification - Not any unread notification.jpg`, `layout-temp/Notification - Having unread notification.jpg`, `layout-temp/Notification - Very high counts unread notification.jpg`

##### Flow Context

- **User arrives from**: Any main patient app screen such as Home, Inquiries, Treatments, or Profile, per the flow diagram at `missing-mobile-flows-design-complement.md:1556-1564`
- **Screen purpose**: Provide persistent unread-notification awareness without forcing the patient to open the full notification list, per `missing-mobile-flows-design-complement.md:1602-1606`
- **Entry point**: Present. All three images show the bell in the persistent bottom navigation area of the mobile shell
- **Exit path**: Partially evidenced. The bell is clearly shown as a tappable navigation item, but the static screenshots do not prove the tap result or confirm that it opens `P06.1-S2` without marking items as read
- **Data continuity**: Correct. The component reflects unread state transitions via no badge, a numeric badge (`9`), and a capped high-count badge (`99+`)
- **Flow context issues**: The required tap behavior and background pulse animation cannot be verified from static layout evidence alone

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Bell Icon | Yes | ✅ | A bell icon is visible in the bottom navigation across all three screenshots, matching the notification-entry component required by `missing-mobile-flows-design-complement.md:1610` |
| Unread Count Badge | Conditional | ✅ | The zero-unread state hides the badge in `Notification - Not any unread notification.jpg`; unread states show `9` and `99+` badges in `Notification - Having unread notification.jpg` and `Notification - Very high counts unread notification.jpg`, matching `missing-mobile-flows-design-complement.md:1611,1617-1619` |
| New Notification Pulse | Conditional | ⚠️ | No pulse or animated-attention treatment is visible in the provided static screenshots, so the background-arrival animation defined at `missing-mobile-flows-design-complement.md:1612,1621` cannot be verified |
| Tap Action | Yes | ⚠️ | The bell is positioned as a tappable nav item, but a static image cannot prove that tapping opens `P06.1-S2` and does not mark notifications as read, as required by `missing-mobile-flows-design-complement.md:1613,1620` |

**Extra Elements**:

- None

**Screen Status**: 🟢 GOOD
**Field Coverage**: 4/4 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| None | No standalone UX/UI issue is clearly evidenced from the three static component screenshots. The bell remains visible, the unread badge is legible, and the bottom-nav placement aligns with mobile conventions | None |

#### Screen P06.1-S2: Notification List Screen

**Layout**: `layout-temp/Notification list.jpg`, `layout-temp/Notification list - Empty.jpg`, `layout-temp/Notification list - Filter.jpg`, `layout-temp/Notification list - Apply Filter.jpg`, `layout-temp/Notification categories.jpg`, `layout-temp/Swipe Actions.jpg`

##### Flow Context

- **User arrives from**: Tapping the bell component from any main patient app screen, per `missing-mobile-flows-design-complement.md:1561-1568`
- **Screen purpose**: Show the full patient notification history with search, filtering, read/archive actions, and deep-link handoff, per `missing-mobile-flows-design-complement.md:1628-1659`
- **Entry point**: Present. All six provided list-state images clearly show the `Notifications` screen and its notification-feed context
- **Exit path**: Partially evidenced. Notification rows, `Mark All as Read`, filtering, and swipe actions are shown, but the spec-required top-left back path is absent from every delivered layout
- **Data continuity**: Mostly correct. The list reflects category, title, preview, and time metadata, and the bottom-nav badge still carries an unread count into the screen shell
- **Flow context issues**: The delivered filtering model uses an icon-triggered modal rather than the specified horizontal chip bar, and the screen omits the required back arrow despite the flow diagram including a back path at `missing-mobile-flows-design-complement.md:1597`

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Screen Title | Yes | ✅ | `Notifications` is shown prominently at the top across all list-state screenshots, matching `missing-mobile-flows-design-complement.md:1634` |
| Back Navigation | Yes | ❌ | No top-left back arrow is visible in `Notification list.jpg`, `Notification list - Empty.jpg`, `Notification list - Filter.jpg`, `Notification list - Apply Filter.jpg`, or `Swipe Actions.jpg`, despite the required back action at `missing-mobile-flows-design-complement.md:1635` |
| Search Bar | Yes | ✅ | A top search field is present in every provided list-state image; the placeholder is shortened to `Search`, but the search affordance defined at `missing-mobile-flows-design-complement.md:1636` is present |
| Mark All as Read Button | Conditional | ❌⚠️ | The control appears in populated states as expected, but it is also still visible in `Notification list - Empty.jpg` where no unread notifications exist, contradicting the visibility rule at `missing-mobile-flows-design-complement.md:1637` |
| Filter Chips | Yes | ❌⚠️ | The delivered UI uses a filter icon that opens a bottom-sheet modal with status/type buttons (`Notification list - Filter.jpg`) instead of a horizontally scrollable on-screen chip bar with one active chip, as required by `missing-mobile-flows-design-complement.md:1638` |
| Date Group Headers | Yes | ✅ | `Today`, `Yesterday`, `This week`, and `Earlier` section labels are visible in `Notification list.jpg`, matching the grouped chronology required at `missing-mobile-flows-design-complement.md:1639,1654` |
| Notification Card | Yes | ✅ | The feed is composed of tappable notification rows with icon, title, preview, and time metadata, matching `missing-mobile-flows-design-complement.md:1640` |
| — Category Icon | Yes | ✅ | Distinct category icons are visible for account/auth, inquiry, quote, treatment, and messaging/support examples in `Notification list.jpg` and `Notification list - Apply Filter.jpg`, satisfying `missing-mobile-flows-design-complement.md:1641` |
| — Notification Title | Yes | ✅ | Titles such as `Email Verification / OTP Code`, `Inquiry Submitted`, and `Quote Submitted` are clearly shown, satisfying `missing-mobile-flows-design-complement.md:1642` |
| — Message Preview | Yes | ✅ | Each row shows a truncated preview line below the title, matching the 1–2 line summary defined at `missing-mobile-flows-design-complement.md:1643` |
| — Timestamp | Yes | ✅ | Relative timestamps such as `an hour ago`, `1 days ago`, and `7 days ago` are visible, satisfying the relative-time requirement at `missing-mobile-flows-design-complement.md:1644` |
| — Read/Unread Indicator | Yes | ❌⚠️ | Read/unread differentiation is present, but the delivered treatment uses tinted cards and red edge markers rather than the specified blue dot plus highlighted unread card background defined at `missing-mobile-flows-design-complement.md:1645` |
| — Swipe Actions | Conditional | ✅ | `Swipe Actions.jpg` shows the swipe-left row actions `Mark as read` and `Archive`, satisfying the conditional action defined at `missing-mobile-flows-design-complement.md:1646` |
| Empty State | Conditional | ✅ | `Notification list - Empty.jpg` shows a dedicated empty illustration and `No notifications yet` message, satisfying the default empty-state requirement at `missing-mobile-flows-design-complement.md:1647` |
| Pull-to-Refresh | Yes | ⚠️ | The static screenshots do not show a pull-to-refresh gesture state or loading indicator, so the behavior defined at `missing-mobile-flows-design-complement.md:1648` cannot be verified from the provided layouts |
| Pagination | Yes | ⚠️ | No bottom-loading or next-page state is shown in the provided screenshots, so the infinite-scroll pagination behavior defined at `missing-mobile-flows-design-complement.md:1649` cannot be verified from static evidence |

**Extra Elements**:

- `Notification categories.jpg` introduces additional taxonomy entries such as `Billing/Payouts`, `Reviews`, `Promotions/Discounts`, `Provider/Compliance`, and `System/Operations`, which extend beyond the patient filter set listed in `missing-mobile-flows-design-complement.md:1638`

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 12/16 (75%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-23` Terminology consistency: the delivered filter taxonomy mixes labels such as `Account/Auth`, `Billing/Payouts`, and other extended categories that do not match the patient notification categories defined for this flow. Evidence: `Notification categories.jpg`, `Notification list - Filter.jpg`. | Align the visible filter/category naming to the approved patient taxonomy, or explicitly revise the source flow/spec if the broader notification catalog is intentional. |
| ⚠️ UX Improvement | `M-09` Gesture affordance: the default list view does not provide any visual hint that rows support swipe-left actions, even though `Swipe Actions.jpg` reveals a hidden action rail. Evidence: `Notification list.jpg` compared with `Swipe Actions.jpg`. | Add a subtle affordance for swipeable rows, or expose the actions through a visible overflow/menu pattern if swipe discovery is not reliable enough. |

**Flow Coverage Gaps**:

- The list screen omits the spec-required top-left back navigation
- The delivered filtering model replaces the specified on-screen horizontal chip bar with an icon-triggered modal filter sheet
- `Mark All as Read` is still visible in the empty state, even though the spec says it should appear only when unread notifications exist
- The read/unread styling does not match the specified blue-dot indicator model
- Pull-to-refresh and pagination behaviors are not directly evidenced in the provided static layouts

---

## Action Items

| Priority | Flow | Screen | Issue | Recommendation |
|----------|------|--------|-------|----------------|
| ⚠️ Important | P06.1 | P06.1-S2 | Back navigation is required by the flow spec but missing from all delivered notification-list layouts | Add the top-left back arrow or formally update the flow/spec to approve the notification list as a first-level tab destination without back navigation |
| ⚠️ Important | P06.1 | P06.1-S2 | The delivered filter experience uses an icon-triggered modal instead of the specified horizontal chip bar, and the taxonomy no longer matches the approved patient categories | Rework the screen to use the specified chip bar, or revise the source flow/spec and downstream implementation assumptions to match the modal-filter design |
| ⚠️ Important | P06.1 | P06.1-S2 | `Mark All as Read` remains visible in the empty state where there are no unread notifications | Hide the control whenever unread count is zero, including empty and no-results states |
| 💡 Suggestion | P06.1 | P06.1-S2 | Read/unread styling uses a different indicator treatment than the approved blue-dot model | Either align the visuals to the specified unread indicator or update the spec to document the new pattern consistently |
| ⚠️ UX Improvement | P06.1 | P06.1-S2 | Swipe actions are hidden with no visible affordance in the default list | Add a discoverability cue for swipe, or expose the actions through a more visible control pattern |

### Priority Legend

- **🔴 Critical**: Blocks flow progression, breaks data integrity, or causes security/legal risk. Must fix before development.
- **🔴 Critical UX**: Severe usability issue that would prevent users from completing the flow or cause significant confusion. Must fix before development.
- **⚠️ Important**: Functional discrepancy that could cause user confusion or require rework during development. Should fix before development.
- **⚠️ UX Improvement**: Usability or design quality issue that deviates from platform conventions or best practices. Should fix before development.
- **💡 Suggestion**: Cosmetic or minor improvement. Can fix anytime.
- **💡 UX Suggestion**: Minor design enhancement that would improve polish. Can fix anytime.

---

## Notes

- Verification requested for Flow `P06.1` only
- Source specification: `local-docs/reports/2026-02-05/missing-mobile-flows-design-complement.md`
- Related FR reference: `local-docs/project-requirements/functional-requirements/fr020-notifications-alerts/prd.md`
- Evidence reviewed: `layout-temp/Notification - Not any unread notification.jpg`, `layout-temp/Notification - Having unread notification.jpg`, `layout-temp/Notification - Very high counts unread notification.jpg`, `layout-temp/Notification list.jpg`, `layout-temp/Notification list - Empty.jpg`, `layout-temp/Notification list - Filter.jpg`, `layout-temp/Notification list - Apply Filter.jpg`, `layout-temp/Notification categories.jpg`, `layout-temp/Swipe Actions.jpg`
- Bubble-component verification relied on static component states only; animation and tap behavior remain partially unverified because no interactive prototype or video evidence was provided
- User approval granted on 2026-03-26 to accept the remaining `P06.1` issues as minor for design sign-off
