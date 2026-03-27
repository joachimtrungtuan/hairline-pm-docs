# Design Layout Verification Report — Missing Mobile Flows Design Complement

**Report Date**: 2026-03-24
**Report Type**: Design Layout Verification
**FR Scope**: FR-003, FR-005
**Flow Scope**: P02.2 Cancel Inquiry
**Layout Source**: `layout-temp/`
**Platform**: Patient Mobile App
**Status**: 🟡 PARTIAL
**Approval Status**: 🟢 Approved with minor issues

---

## Summary Dashboard

| # | Flow | Module | Screens Required | Screens Verified | Layout Status | Field Coverage |
|---|------|--------|-----------------|-----------------|---------------|----------------|
| P02.2 | Cancel Inquiry | P-02: Quote Request & Management | 2 | 2 | 🟡 PARTIAL | 18/23 (~78%) |

**Overall**: 1 of 1 flows verified. Both required screens are present, but several state details and conditional outcomes do not yet align cleanly with the cancellation rules. The remaining issues are accepted as minor for now.
**Screens**: 2 of 2 specified screens have layouts (100% screen coverage).

---

## Layout File Inventory

### Mapped to Spec Flows

| Layout File | Maps to Flow | Maps to Screen | Notes |
|-------------|-------------|----------------|-------|
| `layout-temp/Cancel Inquiry_.jpg` | P02.2 | P02.2-S1 | Confirmation modal candidate |
| `layout-temp/Cancel Inquiry_ - ERROR.jpg` | P02.2 | P02.2-S1 | Confirmation modal validation/error variant |
| `layout-temp/Cancellation Success Confirmation.jpg` | P02.2 | P02.2-S2 | Success confirmation screen candidate |

### Unmapped Files

| Layout File | Likely Purpose | Notes |
|-------------|---------------|-------|
| `layout-temp/Compare Offers.jpg` | P02.1 comparison screen | Outside P02.2 scope |
| `layout-temp/Compare Offers Table.jpg` | P02.1 comparison-table state | Outside P02.2 scope |
| `layout-temp/Full table.jpg` | P02.1 comparison-table state | Outside P02.2 scope |
| `layout-temp/Expired Offers/Offer single.jpg` | P02.3 inquiry detail state | Outside P02.2 scope |
| `layout-temp/Expired Offers/Offer single - Floating Button - Expired.jpg` | P02.3 inquiry detail expired state | Outside P02.2 scope |
| `layout-temp/Expired Offers/Offers - Expired.jpg` | P02.3 quote-list expired state | Outside P02.2 scope |
| `layout-temp/Expired Offers/Offers - All Quotes Expired State.jpg` | P02.3 all-expired state | Outside P02.2 scope |
| `layout-temp/Cancellation policy.jpg` | P02.4 document viewer | Outside P02.2 scope |
| `layout-temp/Cancellation policy - Table of content open.jpg` | P02.4 document viewer variant | Outside P02.2 scope |
| `layout-temp/Cancellation policy - Scroll Progress Indicator.jpg` | P02.4 document viewer variant | Outside P02.2 scope |

---

## Detailed Verification by Flow

---

### Flow P02.2: Cancel Inquiry

**Status**: 🟡 PARTIAL — the core confirmation and success states are designed, but stage handling, reference formatting, and conditional impact messaging still need correction
**Approval**: 🟢 Approved with minor issues — remaining findings are accepted as minor and do not need revisit at this stage
**Screens required**: 2
**Layout files**: `Cancel Inquiry_.jpg`, `Cancel Inquiry_ - ERROR.jpg`, `Cancellation Success Confirmation.jpg`

#### Screen P02.2-S1: Cancel Inquiry Confirmation Modal

**Layout**: `layout-temp/Cancel Inquiry_.jpg`, `layout-temp/Cancel Inquiry_ - ERROR.jpg`

##### Flow Context

- **User arrives from**: Inquiry Dashboard / inquiry detail, after the patient chooses `Cancel Inquiry` from the action menu, per `missing-mobile-flows-design-complement.md:510-520`
- **Screen purpose**: Confirm the patient's intent, collect a cancellation reason, and explain the downstream impact before the cancellation is submitted
- **Entry point**: Present. `Cancel Inquiry_.jpg` shows the intended destructive confirmation modal with reason capture
- **Exit path**: Partially present. The confirmation modal includes `Confirm Cancellation` and `Go back`, and the blocked-state variant includes `Contact support`, but the blocked-state example uses an ineligible-stage mapping that conflicts with the specified allowed stages
- **Data continuity**: Partial. The modal shows a stage badge, reference, and quote-impact summary, but the displayed stage/reference formatting does not fully align with the specification
- **Flow context issues**: The blocked-state variant shows `ACCEPTED` as non-cancellable even though the flow explicitly allows cancellation in the `Accepted` stage

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Warning Icon | Yes | ✅ | Both modal variants show a prominent red warning icon at the top |
| Modal Title | Yes | ❌⚠️ | The title text `Cancel Inquiry?` is correct, but it is rendered in dark text rather than the specified red/destructive styling |
| Warning Message | Yes | ✅ | The default modal explains that cancellation is irreversible, quotes will be cancelled, and providers will be notified |
| Current Stage Badge | Yes | ❌⚠️ | The default modal shows `REQUESTED` and the blocked variant shows `ACCEPTED`; the spec expects the canonical lifecycle labels `Inquiry`, `Quoted`, or `Accepted`, and `Accepted` should not be blocked |
| Inquiry Reference | Yes | ❌⚠️ | A reference is shown as `HP202401`, but the format does not evidence the specified `HPID + YY + MM + 4-digit sequence` pattern |
| Impact Summary | Yes | ✅ | The default modal includes `1 active quotes will be cancelled`, which satisfies the impact-summary requirement for a quoted inquiry |
| Cancellation Reason Label | Yes | ✅ | `Why are you cancelling?` is shown above the reason options |
| Cancellation Reason Selector | Yes | ✅ | The layout provides a selectable list of reasons and shows `Other` selected in the illustrated state |
| Cancellation Reason Options | Yes | ✅ | All required reasons are visible: changed mind, better option, medical concerns, financial reasons, travel restrictions, timeline, and other |
| Additional Notes (Conditional) | Conditional | ✅ | Because `Other` is selected, `Additional Notes` is displayed as required |
| Optional Feedback Field | No | ✅ | `Optional Feedback` is shown below the conditional notes field |
| Provider Notification Note | Yes | ✅ | The informational note states that affected providers will be notified within 5 minutes |
| Confirm Cancellation Button | Yes | ✅ | `Confirm Cancellation` is present in a destructive red style |
| Go Back Button | Yes | ✅ | `Go back` is present as the neutral dismissal action |

**Extra Elements**:

- The blocked-state variant is shown on top of a full inquiry-detail background with a `Cancel request` button rather than as the same confirmation modal flow; this is useful context but not part of the base modal spec

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 10/13 (~77%)
**Critical Issues**: The blocked-state example contradicts the allowed-stage rule by preventing cancellation in the `Accepted` stage

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| None | No standalone UX/UI issues were identified beyond the documented state-rule mismatches. The modal hierarchy, CTA separation, and vertical spacing are otherwise clear in the static layouts | None |

#### Screen P02.2-S2: Cancellation Success Confirmation

**Layout**: `layout-temp/Cancellation Success Confirmation.jpg`

##### Flow Context

- **User arrives from**: Successful completion of the cancellation process after status updates, quote cancellation, notifications, and audit logging, per `missing-mobile-flows-design-complement.md:531-538`
- **Screen purpose**: Confirm that the inquiry has been cancelled and give the patient clear next-step navigation
- **Entry point**: Present. `Cancellation Success Confirmation.jpg` matches the intended success branch with a completion icon and cancellation summary
- **Exit path**: Present. The screen provides both `Back to My Inquiries` and `Start New Inquiry`, plus an optional support link
- **Data continuity**: Partial. The screen reflects the cancelled inquiry reference and timestamp, but the impact summary is still presented as a design-note list of all possible variants rather than the actual one for the shown inquiry
- **Flow context issues**: The impact summary remains generic instead of showing the single correct cascade result for the specific cancelled inquiry

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Success Icon | Yes | ✅ | A prominent green completion icon is shown at the top |
| Confirmation Title | Yes | ✅ | The title `Inquiry Cancelled` is displayed prominently |
| Confirmation Message | Yes | ✅ | The screen includes `Your inquiry has been successfully cancelled.` |
| Cancelled Inquiry Reference | Yes | ❌⚠️ | A reference is shown, but it uses the same `HP202401` format rather than the specified `HPID + YY + MM + 4-digit sequence`, and the layout adds an unspecified `REQUESTED` badge |
| Cancellation Timestamp | Yes | ✅ | A cancellation timestamp is shown in the blue information box |
| Impact Summary | Yes | ❌⚠️ | Instead of showing the single correct outcome, the layout lists all three conditional impact-summary variants simultaneously under `Conditional based on inquiry stage` |
| Provider Notification Status | Yes | ✅ | The screen confirms that affected providers have been notified |
| Next Steps Section Label | Yes | ✅ | `What would you like to do next?` is shown as the next-step section header |
| Back to My Inquiries Button | Yes | ✅ | The primary CTA `Back to My Inquiries` is visible |
| Start New Inquiry Button | Yes | ✅ | The secondary CTA `Start New Inquiry` is visible |
| Contact Support Link | No | ✅ | `Need help? Contact support` is present as the optional support action |

**Extra Elements**:

- `REQUESTED` stage badge on the success screen — not listed in the success-screen spec

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 8/10 (80%)
**Critical Issues**: The success-state impact summary does not yet resolve to the single correct cancellation outcome for the displayed inquiry

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-11 Label clarity`: the success screen shows all three conditional impact-summary variants at once, which reads like internal design notes rather than a finalized patient-facing outcome | Replace the placeholder list with the one actual impact-summary message that matches the cancelled inquiry stage and cascade result |

**Flow Coverage Gaps**:

- The blocked-state example uses `ACCEPTED` as a non-cancellable stage, which conflicts with the flow definition that allows cancellation for `Accepted`
- Inquiry references shown in both screens do not yet evidence the specified HPID-style format
- The success screen still exposes all impact-summary variants at once instead of the actual resolved outcome for the cancelled inquiry

---

## Action Items

| Priority | Flow | Screen | Issue | Recommendation |
|----------|------|--------|-------|----------------|
| 🔴 Critical | P02.2 | P02.2-S1 | Blocked-state example contradicts the stage-eligibility rule by preventing cancellation in the `Accepted` stage | Replace the blocked-state example with a truly ineligible stage (`Confirmed`, `In Progress`, `Aftercare`, or `Completed`) or update the badge/content so the state matches the business rules |
| ⚠️ Important | P02.2 | P02.2-S2 | Success screen shows all impact-summary variants simultaneously instead of the single correct outcome | Bind the success message to the actual cancellation result for the displayed inquiry and remove the placeholder list |
| ⚠️ Important | P02.2 | P02.2-S1 / P02.2-S2 | Inquiry reference formatting does not evidence the specified HPID pattern | Update the reference examples to a compliant HPID-format sample across both screens |
| 💡 Suggestion | P02.2 | P02.2-S1 | Modal title is not styled in the specified destructive red treatment | Restyle the `Cancel Inquiry?` title to match the destructive-spec emphasis if that visual requirement is still intended |

### Priority Legend

- **🔴 Critical**: Blocks flow progression, breaks data integrity, or causes security/legal risk. Must fix before development.
- **🔴 Critical UX**: Severe usability issue that would prevent users from completing the flow or cause significant confusion. Must fix before development.
- **⚠️ Important**: Functional discrepancy that could cause user confusion or require rework during development. Should fix before development.
- **⚠️ UX Improvement**: Usability or design quality issue that deviates from platform conventions or best practices. Should fix before development.
- **💡 Suggestion**: Cosmetic or minor improvement. Can fix anytime.
- **💡 UX Suggestion**: Minor design enhancement that would improve polish. Can fix anytime.

---

## Notes

- Verification was performed against Flow `P02.2` only
- The current layouts cover both required screens and the main cancellation journey, but they still include placeholder or contradictory state content that should be resolved before final sign-off
- User approval was granted on 2026-03-24 to accept the remaining findings as minor and defer further revision
- Source specification: `local-docs/reports/2026-02-05/missing-mobile-flows-design-complement.md`
