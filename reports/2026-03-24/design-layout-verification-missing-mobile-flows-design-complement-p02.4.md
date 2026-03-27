# Design Layout Verification Report — Missing Mobile Flows Design Complement

**Report Date**: 2026-03-24
**Report Type**: Design Layout Verification
**FR Scope**: FR-005, FR-027
**Flow Scope**: P02.4 Legal/Policy Screens (Quote Context)
**Layout Source**: `layout-temp/`
**Platform**: Patient Mobile App
**Status**: 🟡 PARTIAL
**Approval Status**: 🟢 Approved with minor issues

---

## Summary Dashboard

| # | Flow | Module | Screens Required | Screens Verified | Layout Status | Field Coverage |
|---|------|--------|-----------------|-----------------|---------------|----------------|
| P02.4 | Legal/Policy Screens (Quote Context) | P-02: Quote Request & Management | 1 | 1 | 🟡 PARTIAL | 6/6 (100%) |

**Overall**: 1 of 1 flows verified. The shared legal-document viewer structure is present and field-complete for the cancellation-policy case, but the current layout set does not evidence the other document-title variants or the documented load-failure state. The remaining issues are accepted as minor for now.
**Screens**: 1 of 1 specified screens have layouts (100% screen coverage).

---

## Layout File Inventory

### Mapped to Spec Flows

| Layout File | Maps to Flow | Maps to Screen | Notes |
|-------------|-------------|----------------|-------|
| `layout-temp/Cancellation policy.jpg` | P02.4 | P02.4-S1 | Legal document viewer default state candidate |
| `layout-temp/Cancellation policy - Table of content open.jpg` | P02.4 | P02.4-S1 | Table-of-contents variant candidate |
| `layout-temp/Cancellation policy - Scroll Progress Indicator.jpg` | P02.4 | P02.4-S1 | Scroll-progress variant candidate |

### Unmapped Files

| Layout File | Likely Purpose | Notes |
|-------------|---------------|-------|
| `layout-temp/Compare Offers.jpg` | P02.1 comparison screen | Outside P02.4 scope |
| `layout-temp/Compare Offers Table.jpg` | P02.1 comparison-table state | Outside P02.4 scope |
| `layout-temp/Full table.jpg` | P02.1 comparison-table state | Outside P02.4 scope |
| `layout-temp/Cancel Inquiry_.jpg` | P02.2 confirmation modal | Outside P02.4 scope |
| `layout-temp/Cancel Inquiry_ - ERROR.jpg` | P02.2 modal error state | Outside P02.4 scope |
| `layout-temp/Cancellation Success Confirmation.jpg` | P02.2 success screen | Outside P02.4 scope |
| `layout-temp/Expired Offers/Offer single.jpg` | P02.3 inquiry detail state | Outside P02.4 scope |
| `layout-temp/Expired Offers/Offer single - Floating Button - Expired.jpg` | P02.3 inquiry detail expired state | Outside P02.4 scope |
| `layout-temp/Expired Offers/Offers - Expired.jpg` | P02.3 quote-list expired state | Outside P02.4 scope |
| `layout-temp/Expired Offers/Offers - All Quotes Expired State.jpg` | P02.3 all-expired state | Outside P02.4 scope |

---

## Detailed Verification by Flow

---

### Flow P02.4: Legal/Policy Screens (Quote Context)

**Status**: 🟡 PARTIAL — the shared document-viewer layout is complete for the cancellation-policy variant, but the full flow coverage is incomplete because other document types and the load-error state are not evidenced
**Approval**: 🟢 Approved with minor issues — remaining findings are accepted as minor and do not need revisit at this stage
**Screens required**: 1
**Layout files**: `Cancellation policy.jpg`, `Cancellation policy - Table of content open.jpg`, `Cancellation policy - Scroll Progress Indicator.jpg`

#### Screen P02.4-S1: Legal Document Viewer (Shared Screen)

**Layout**: `layout-temp/Cancellation policy.jpg`, `layout-temp/Cancellation policy - Table of content open.jpg`, `layout-temp/Cancellation policy - Scroll Progress Indicator.jpg`

##### Flow Context

- **User arrives from**: Quote Detail, after the patient taps one of the legal links under the terms acknowledgment area, per `missing-mobile-flows-design-complement.md:689-704`
- **Screen purpose**: Present a reusable, read-only legal document viewer for quote-context legal content without introducing acceptance actions on this screen
- **Entry point**: Present for the cancellation-policy variant. The title and legal metadata align with the tapped `Cancellation Policy` case
- **Exit path**: Present. A back arrow is visible at the top-left of each viewer variant
- **Data continuity**: Correct. The screen preserves the read-only document-viewer pattern with title, metadata, long-form content, and optional navigation aids
- **Flow context issues**: Only the cancellation-policy document type is evidenced; the privacy-commitment and terms-of-service variants are not present in the current layout set

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Screen Title | Yes | ✅ | The title `Cancellation policy` is displayed at the top and matches the shown document type |
| Back Navigation | Yes | ✅ | A back arrow is visible at top-left across the viewer variants |
| Document Version | Conditional | ✅ | Version metadata is shown as `Version: 1.0` in the default / TOC-open variants |
| Last Updated | Conditional | ✅ | Update metadata is shown alongside the version (`Update: 23 June, 2025`) |
| Document Content | Yes | ✅ | Long-form legal content with headings and paragraph blocks is visible and scrollable in all variants |
| Table of Contents | Conditional | ✅ | The viewer includes a `Table of Contents item` control and an expanded TOC variant |
| Scroll Progress Indicator | No | ✅ | The `Scroll Progress Indicator` variant shows a top progress bar for reading progress |

**Extra Elements**:

- None

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 6/6 (100%)
**Critical Issues**: None at the field-row level; remaining gaps are flow-coverage gaps for unsupported document-type variants and the missing load-error state

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| None | No UX/UI issues identified from the static viewer layouts. The screen uses readable long-form typography, clear back navigation, and sensible optional reading aids (TOC/progress) | None |

**Flow Coverage Gaps**:

- No layout was provided showing the `Privacy Commitment` title variant of the shared viewer
- No layout was provided showing the `Terms of Service` title variant of the shared viewer
- No non-blocking load-error state with `Retry` and `Back` options is evidenced in the current layout set

---

## Action Items

| Priority | Flow | Screen | Issue | Recommendation |
|----------|------|--------|-------|----------------|
| ⚠️ Important | P02.4 | P02.4-S1 | Only the cancellation-policy instantiation of the shared viewer is evidenced | Add layout variants for `Privacy Commitment` and `Terms of Service` so the shared-screen title behavior is fully covered |
| ⚠️ Important | P02.4 | P02.4-S1 | Load-failure handling required by the business rules is not evidenced | Add a non-blocking error state with `Retry` and `Back` actions for failed legal-content loads |

### Priority Legend

- **🔴 Critical**: Blocks flow progression, breaks data integrity, or causes security/legal risk. Must fix before development.
- **🔴 Critical UX**: Severe usability issue that would prevent users from completing the flow or cause significant confusion. Must fix before development.
- **⚠️ Important**: Functional discrepancy that could cause user confusion or require rework during development. Should fix before development.
- **⚠️ UX Improvement**: Usability or design quality issue that deviates from platform conventions or best practices. Should fix before development.
- **💡 Suggestion**: Cosmetic or minor improvement. Can fix anytime.
- **💡 UX Suggestion**: Minor design enhancement that would improve polish. Can fix anytime.

---

## Notes

- Verification was performed against Flow `P02.4` only
- The shared viewer structure itself is sound; the remaining gaps are coverage gaps for additional document types and the fallback/error state
- User approval was granted on 2026-03-24 to accept the remaining findings as minor and defer further revision
- Source specification: `local-docs/reports/2026-02-05/missing-mobile-flows-design-complement.md`
