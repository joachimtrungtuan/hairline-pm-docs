# Design Layout Verification Report — Missing Mobile Flows Design Complement

**Report Date**: 2026-03-24
**Report Type**: Design Layout Verification
**FR Scope**: FR-013
**Flow Scope**: P05.3 Submitted Reviews List
**Layout Source**: `layout-temp/reviews/`
**Platform**: Patient Mobile App
**Status**: 🟡 PARTIAL
**Approval Status**: 🟢 Approved with minor issues

---

## Summary Dashboard

| # | Flow | Module | Screens Required | Screens Verified | Layout Status | Field Coverage |
|---|------|--------|-----------------|-----------------|---------------|----------------|
| P05.3 | Submitted Reviews List | P-05: Aftercare & Progress Monitoring | 2 | 2 | 🟡 PARTIAL | 15/15 (100%) |

**Overall**: 1 of 1 flows verified. The review list and detail views are both designed, but the list introduces an off-spec `Submitted` review status that conflicts with the immediate-publish requirement.
**Screens**: 2 of 2 specified screens have layouts (100% screen coverage).

---

## Layout File Inventory

### Mapped to Spec Flows

| Layout File | Maps to Flow | Maps to Screen | Notes |
|-------------|-------------|----------------|-------|
| `layout-temp/reviews/My Reviews.jpg` | P05.3 | P05.3-S1 | Primary list-state candidate |
| `layout-temp/reviews/My Reviews - Empty.jpg` | P05.3 | P05.3-S1 | Empty-state candidate |
| `layout-temp/reviews/Review Detail.jpg` | P05.3 | P05.3-S2 | Primary detail-state candidate |
| `layout-temp/reviews/Review Detail - Edit.jpg` | P05.3 | P05.3-S2 | Published review edit-state candidate |
| `layout-temp/reviews/Review Detail - Removed.jpg` | P05.3 | P05.3-S2 | Removed-by-admin state candidate |
| `layout-temp/reviews/Review Detail - Takedown Request.jpg` | P05.3 | P05.3-S2 | Takedown confirmation / request-state candidate |

### Unmapped Files

| Layout File | Likely Purpose | Notes |
|-------------|---------------|-------|
| None | None | All files under `layout-temp/reviews/` are in scope for P05.3 candidate coverage |

---

## Detailed Verification by Flow

---

### Flow P05.3: Submitted Reviews List

**Status**: 🟡 PARTIAL — both screens are present, but the list-screen review-status model is not fully aligned to the spec
**Approval**: 🟢 Approved with minor issues — the flow is accepted for design sign-off, with the remaining terminology mismatch documented for follow-up
**Screens required**: 2
**Layout files**: `My Reviews.jpg`, `My Reviews - Empty.jpg`, `Review Detail.jpg`, `Review Detail - Edit.jpg`, `Review Detail - Removed.jpg`, `Review Detail - Takedown Request.jpg`

#### Screen P05.3-S1: My Reviews List

**Layout**: `layout-temp/reviews/My Reviews.jpg`, `layout-temp/reviews/My Reviews - Empty.jpg`

##### Flow Context

- **User arrives from**: Profile -> `My Reviews`, per the flow diagram at `missing-mobile-flows-design-complement.md:1458-1465`
- **Screen purpose**: Show all submitted patient reviews, let the patient sort the list, and open a review detail view
- **Entry point**: Present. `My Reviews.jpg` and `My Reviews - Empty.jpg` both show the dedicated `My Reviews` list screen with back navigation
- **Exit path**: Present. Review cards are visibly tappable list items that lead into the review-detail experience; a sort control is also present in the top-right corner
- **Data continuity**: Mostly correct. Cards carry forward treatment name, provider branding, star rating, excerpt, date context, and status, but one card uses a `Submitted` status that does not match the source rules
- **Flow context issues**: The source business rules at `missing-mobile-flows-design-complement.md:1500-1504` say reviews publish immediately and that the patient-facing states are `Published` or `Removed by Admin`. The delivered list introduces a third `Submitted` state that suggests moderation/pending review

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Screen Title | Yes | ✅ | `My Reviews` is shown prominently at the top of both list-state images |
| Sort Options | No | ⚠️ | A sort-control icon is present at the top-right, but no opened sort menu/options are shown in the provided review layouts |
| Review Card — Treatment Name | Yes | ✅ | Each card shows `Treatment: Fue Hair Transplant` |
| Review Card — Provider Name & Avatar | Yes | ✅ | Each card shows provider branding/logo plus `X Hair Transplant` |
| Review Card — Overall Star Rating | Yes | ✅ | Each card shows a star row at the top-left of the review card |
| Review Card — Review Date | Yes | ⚠️ | The cards show relative time (`5 days ago`) instead of a fuller date representation, but the review timing context is still present |
| Review Card — Review Excerpt | Yes | ✅ | Each card shows a truncated excerpt with `See more` |
| Review Card — Status Badge | Yes | ❌⚠️ | The top badges include `Published`, `Submitted`, and `Removed`; `Submitted` is off-spec because the flow defines immediate publication, and `Removed` omits the `by Admin` actor from the source badge label |
| Empty State | No | ✅ | `My Reviews - Empty.jpg` shows `No reviews yet` and `Complete a treatment to leave a review` |

**Extra Elements**:

- None

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 7/7 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-23 Terminology consistency`: the list mixes `Published`, `Submitted`, and `Removed` labels even though the documented patient-facing lifecycle is `Published` or `Removed by Admin`, which can make patients think reviews await moderation | Align the badge terminology to the approved status model and explicitly use `Removed by Admin` for admin-removal states |

#### Screen P05.3-S2: Review Detail View

**Layout**: `layout-temp/reviews/Review Detail.jpg`, `layout-temp/reviews/Review Detail - Edit.jpg`, `layout-temp/reviews/Review Detail - Removed.jpg`, `layout-temp/reviews/Review Detail - Takedown Request.jpg`

##### Flow Context

- **User arrives from**: Tapping a review card on `P05.3-S1`, per `missing-mobile-flows-design-complement.md:1463-1481`
- **Screen purpose**: Show the full submitted review, optional provider response, and the published/removed actions available to the patient
- **Entry point**: Present. The published, removed, edit, and takedown-request variants all clearly belong to the `Review Detail` screen
- **Exit path**: Present. The published state includes `Edit Review` and `Takedown Request`, the removed state hides those actions, and back navigation is visible in all full-screen variants
- **Data continuity**: Correct. Treatment name, provider branding, overall/category ratings, review text, photos, status state, provider response, and takedown messaging are coherently carried into the detail flow
- **Flow context issues**: None

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Treatment Name | Yes | ✅ | `Treatment: Fue Hair Transplant` is shown in the published, removed, and edit variants |
| Provider Name & Avatar | Yes | ✅ | The provider logo/avatar and `X Hair Transplant` are shown throughout the detail variants |
| Overall Star Rating | Yes | ✅ | Overall rating is visible as large star rating / `4/5 star` in the detail and edit views |
| Category Ratings | Yes | ✅ | `Facility`, `Staff`, `Results`, and `Value` ratings are shown in both display and edit states |
| Review Text | Yes | ✅ | The review narrative text is shown in the published and removed views, and in the editable `Feedback` field in edit mode |
| Review Submission Date | Yes | ⚠️ | The published detail view shows relative time (`5 days ago`) rather than a full date-time for the review itself, but the submission timing context is present |
| Review Photos | No | ✅ | A photo is shown in the display states and an editable photo area is shown in edit mode |
| Status Badge | Yes | ⚠️ | `Published` matches the spec; `Removed` conveys the removed state but shortens the specified `Removed by Admin` wording |
| Admin Removal Reason | No | ✅ | `Review Detail - Removed.jpg` shows a blue `Removal Reason` banner for the removed state |
| Provider Response | No | ✅ | `Review Detail.jpg` shows a `Provider Response` card with provider identity and timestamp |
| Edit Review | No | ✅ | The published detail view includes an `Edit Review` CTA, and `Review Detail - Edit.jpg` shows the pre-filled edit form |
| Request Takedown | No | ✅ | The published detail view includes a `Takedown Request` CTA, and `Review Detail - Takedown Request.jpg` shows the confirmation state with the data-retention warning |
| Back Navigation | Yes | ✅ | Back arrows are visible on the full-screen detail states |

**Extra Elements**:

- The takedown request sheet includes a free-text `Message` field, which is not explicitly listed in the screen spec but is a reasonable enhancement for request context

**Screen Status**: 🟢 GOOD
**Field Coverage**: 8/8 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| None | No standalone UX/UI issues were identified in the review-detail layouts beyond the status-label wording already captured in field verification | None |

**Flow Coverage Gaps**:

- The list screen uses an off-spec `Submitted` status, which conflicts with the immediate-publish review workflow
- The `Removed` label should be clarified to `Removed by Admin` to match the documented patient-facing review state

---

## Action Items

| Priority | Flow | Screen | Issue | Recommendation |
|----------|------|--------|-------|----------------|
| ⚠️ Important | P05.3 | P05.3-S1 | Review-status badges are not aligned to the source workflow; one card uses `Submitted` even though reviews should publish immediately | Remove the `Submitted` state from the patient list and use only the approved lifecycle labels (`Published`, `Removed by Admin`) |
| 💡 Suggestion | P05.3 | P05.3-S2 | Removed-state badge wording is shortened to `Removed` instead of `Removed by Admin` | Use the full patient-facing status wording to make the removal actor explicit |

### Priority Legend

- **🔴 Critical**: Blocks flow progression, breaks data integrity, or causes security/legal risk. Must fix before development.
- **🔴 Critical UX**: Severe usability issue that would prevent users from completing the flow or cause significant confusion. Must fix before development.
- **⚠️ Important**: Functional discrepancy that could cause user confusion or require rework during development. Should fix before development.
- **⚠️ UX Improvement**: Usability or design quality issue that deviates from platform conventions or best practices. Should fix before development.
- **💡 Suggestion**: Cosmetic or minor improvement. Can fix anytime.
- **💡 UX Suggestion**: Minor design enhancement that would improve polish. Can fix anytime.

---

## Notes

- Verification was requested for Flow `P05.3` only
- Source specification: `local-docs/reports/2026-02-05/missing-mobile-flows-design-complement.md`
- Related FR references: `local-docs/project-requirements/functional-requirements/fr013-reviews-ratings/prd.md`
- Evidence reviewed: `layout-temp/reviews/My Reviews.jpg`, `layout-temp/reviews/My Reviews - Empty.jpg`, `layout-temp/reviews/Review Detail.jpg`, `layout-temp/reviews/Review Detail - Edit.jpg`, `layout-temp/reviews/Review Detail - Removed.jpg`, and `layout-temp/reviews/Review Detail - Takedown Request.jpg`
- User approval granted on 2026-03-24 to accept the remaining `P05.3` issues as minor for design sign-off
