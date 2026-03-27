# Design Layout Verification Report — Missing Mobile Flows Design Complement

**Report Date**: 2026-03-24
**Report Type**: Design Layout Verification
**FR Scope**: FR-007, FR-007b
**Flow Scope**: P03.1 Payment Methods Management
**Layout Source**: `layout-temp/`
**Platform**: Patient Mobile App
**Status**: 🟡 PARTIAL
**Approval Status**: 🟢 Approved with minor issues

---

## Summary Dashboard

| # | Flow | Module | Screens Required | Screens Verified | Layout Status | Field Coverage |
|---|------|--------|-----------------|-----------------|---------------|----------------|
| P03.1 | Payment Methods Management | P-03: Booking & Payment | 3 | 3 | 🟡 PARTIAL | 31/35 (~89%) |

**Overall**: 1 of 1 flows verified. The list management states are strong, but edit-mode restrictions and removal-identification details do not fully match the spec. The remaining findings are accepted as minor for now.
**Screens**: 3 of 3 specified screens have layouts (100% screen coverage).

---

## Layout File Inventory

### Mapped to Spec Flows

| Layout File | Maps to Flow | Maps to Screen | Notes |
|-------------|-------------|----------------|-------|
| `layout-temp/Payment Methods.jpg` | P03.1 | P03.1-S1 | Primary payment-methods list state candidate |
| `layout-temp/Action.jpg` | P03.1 | P03.1-S1 | Per-card action sheet / list interaction state candidate |
| `layout-temp/Empty.jpg` | P03.1 | P03.1-S1 | Empty-state candidate |
| `layout-temp/Empty-1.jpg` | P03.1 | P03.1-S1 | Alternate empty/list transition candidate |
| `layout-temp/Active Obligations Notice.jpg` | P03.1 | P03.1-S1 | Inline blocked-removal / active-obligations state candidate |
| `layout-temp/Add Payment Methods.jpg` | P03.1 | P03.1-S2 | Add payment method form candidate |
| `layout-temp/Edit Payment Methods.jpg` | P03.1 | P03.1-S2 | Edit payment method form candidate |
| `layout-temp/Remove Payment Methods/Default Card.jpg` | P03.1 | P03.1-S3 | Remove confirmation modal for default-card case |
| `layout-temp/Remove Payment Methods/Not default card.jpg` | P03.1 | P03.1-S3 | Remove confirmation modal for non-default-card case |

### Unmapped Files

| Layout File | Likely Purpose | Notes |
|-------------|---------------|-------|
| `layout-temp/Profile.jpg` | Profile screen | Upstream entry context only; outside direct P03.1 screen-spec scope |

---

## Detailed Verification by Flow

---

### Flow P03.1: Payment Methods Management

**Status**: 🟡 PARTIAL — the flow is broadly designed end-to-end, but edit-mode card restrictions and remove-confirmation identification are not fully aligned with the specification
**Approval**: 🟢 Approved with minor issues — remaining findings are accepted as minor and do not need revisit at this stage
**Screens required**: 3
**Layout files**: `Payment Methods.jpg`, `Action.jpg`, `Empty.jpg`, `Empty-1.jpg`, `Active Obligations Notice.jpg`, `Add Payment Methods.jpg`, `Edit Payment Methods.jpg`, `Remove Payment Methods/Default Card.jpg`, `Remove Payment Methods/Not default card.jpg`

#### Screen P03.1-S1: Payment Methods List

**Layout**: `layout-temp/Payment Methods.jpg`, `layout-temp/Action.jpg`, `layout-temp/Empty.jpg`, `layout-temp/Empty-1.jpg`, `layout-temp/Active Obligations Notice.jpg`

##### Flow Context

- **User arrives from**: Profile -> Payment Methods, per the flow diagram at `missing-mobile-flows-design-complement.md:745-749`
- **Screen purpose**: Show saved payment methods, allow default/edit/remove management, and provide an add-method entry point
- **Entry point**: Present. `Profile.jpg` acts as the upstream profile context, and the destination layouts clearly show the `Payment Methods` screen in both populated and empty states
- **Exit path**: Present. The screen has a back arrow, an add-method CTA, per-card actions via the action sheet, and a retry path in the load-error state
- **Data continuity**: Correct. The list shows token-safe card brand, masked last 4 digits, expiry, and default indication without exposing full payment credentials
- **Flow context issues**: None

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Screen Title | Yes | ✅ | `Payment Methods` is shown prominently at the top across all list-state variants |
| Back Navigation | Yes | ✅ | A back arrow is visible at top-left in all provided list-state layouts |
| Payment Method Cards | Yes | ✅ | `Payment Methods.jpg` and `Active Obligations Notice.jpg` show three saved card entries with brand icon, masked last 4 digits, and expiry date |
| Default Badge (Per Card) | Conditional | ✅ | The Visa card is marked `Default`, satisfying the default indicator requirement |
| Per-Card Action: Set as Default | Conditional | ✅ | `Action.jpg` shows `Set as Default` in the action sheet for a non-default card |
| Per-Card Action: Edit | Yes | ✅ | `Action.jpg` shows `Edit` as a per-card action |
| Per-Card Action: Remove | Yes | ✅ | `Action.jpg` shows `Remove` as a per-card action |
| Add Payment Method Button | Yes | ✅ | A prominent `Add Payment Method` button is visible at the bottom of the populated, empty, and blocked-state screens |
| Empty State Illustration | Conditional | ✅ | `Empty.jpg` shows the illustration, empty-state title, and supporting message when no payment methods exist |
| Empty State CTA | Conditional | ✅ | `Empty.jpg` includes the `Add Payment Method` CTA inside the empty state |
| Active Obligations Notice (Conditional) | Conditional | ✅ | `Active Obligations Notice.jpg` shows `You have pending payments — at least one payment method is required.` inline above the list |
| Error State (Conditional) | Conditional | ✅ | `Empty-1.jpg` shows a load-failure state with warning icon and `Retry` button; the copy is abbreviated (`Unable to load`) but functionally matches the intended state |

**Extra Elements**:

- `View detail` appears in `Action.jpg` as an extra per-card action not listed in the screen specification

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 12/12 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| None | No UX/UI issues identified from the static list-state layouts. The hierarchy, state handling, and CTA placement are clear across populated, empty, blocked, and load-error states | None |

#### Screen P03.1-S2: Add/Edit Payment Method

**Layout**: `layout-temp/Add Payment Methods.jpg`, `layout-temp/Edit Payment Methods.jpg`

##### Flow Context

- **User arrives from**: `Add Payment Method` from the list screen, or `Edit` on an existing saved card, per `missing-mobile-flows-design-complement.md:759-786`
- **Screen purpose**: Capture a new payment method securely or let the patient update editable payment-method metadata
- **Entry point**: Present. The two layouts clearly show add mode and edit mode for the payment method form
- **Exit path**: Present, but partially evidenced. The add-mode layout shows both `Save Payment Method` and `Cancel`; edit mode shows `Save Changes`, but the secondary cancel action is not visible in the provided screenshot
- **Data continuity**: Partial. Add mode provides blank hosted-field style inputs, and edit mode pre-fills masked card data plus address metadata, but the edit-state field behavior does not fully match the edit-mode restrictions defined in the spec
- **Flow context issues**: Edit mode appears to expose credential fields (`Expiry Date`, `CVV/CVC`) directly instead of forcing card replacement through a `Replace card` path

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Screen Title | Yes | ✅ | `Add Payment Method` and `Edit Payment Method` are shown correctly in the respective modes |
| Back Navigation | Yes | ✅ | A back arrow is visible at top-left in both layouts |
| Secure Form Notice | Yes | ✅ | Both layouts show `Your payment details are secured and encrypted` with a security icon near the bottom of the form |
| Card Number Input | Yes (card type) | ❌⚠️ | Add mode shows a card-number field as expected, but edit mode shows masked digits without the required `Replace card` action for re-entering a new card |
| Cardholder Name | Yes (card type) | ✅ | Cardholder name is present in both modes and prefilled in edit mode |
| Expiry Date | Yes (card type) | ❌⚠️ | Add mode is correct, but edit mode appears to expose `Expiry Date` directly (`12/30`) instead of treating payment credentials as replace-only fields |
| CVV/CVC | Yes (card type) | ❌⚠️ | Add mode is correct, but edit mode still shows an active `CVV/CVC` field, which conflicts with the edit-mode rule that credentials are not directly editable |
| Billing Address (Conditional) | Conditional | ✅ | Address line 1/2, city, state/region, postal code, and country are present in both modes |
| Method Nickname (Optional) | No | ✅ | `Method Nickname` field is present in both modes |
| Set as Default Toggle | No | ✅ | The `Set as default payment method` toggle is shown in both modes |
| Save Button | Yes | ✅ | `Save Payment Method` appears in add mode and `Save Changes` appears in edit mode |
| Cancel Button | Yes | ⚠️ | `Cancel` is visible in add mode; the edit-mode screenshot does not show the secondary cancel action, so coverage for edit mode is incomplete |
| Secure Transaction Badge | Yes | ✅ | The security notice box at the bottom functions as the secure transaction / encryption indicator |
| Field-Level Error Messages (Conditional) | Conditional | ✅ | Edit mode shows an inline card-number error: `invalid card number. Please check and try again.` |
| Gateway Error Message (Conditional) | Conditional | ✅ | No gateway-decline state is shown in the provided layouts, which is acceptable for the default/edit-error states provided |

**Extra Elements**:

- None

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 12/15 (80%)
**Critical Issues**: Edit mode appears to allow direct credential-field editing instead of requiring the replace-card flow specified in the business rules

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| None | No standalone UX/UI issues were identified beyond the documented edit-mode rule mismatch. The form hierarchy, spacing, and CTA placement are otherwise clear in the static layouts | None |

#### Screen P03.1-S3: Remove Payment Method Confirmation Modal

**Layout**: `layout-temp/Remove Payment Methods/Default Card.jpg`, `layout-temp/Remove Payment Methods/Not default card.jpg`

##### Flow Context

- **User arrives from**: `Remove` on a saved payment method, after the system confirms that removal is allowed, per `missing-mobile-flows-design-complement.md:764-777`
- **Screen purpose**: Confirm the patient's intent to remove a saved payment method and communicate any reassignment / installment consequences
- **Entry point**: Present. Both provided modal states clearly show the destructive confirmation step after selecting `Remove`
- **Exit path**: Present. Both modal states include `Remove` and `Go back`
- **Data continuity**: Partial. The modal variants communicate the correct consequence messages, but they do not clearly identify the selected card within the modal body as the spec requires
- **Flow context issues**: The method being removed is only inferable from the dimmed background or reassignment notice, not explicitly summarized in the modal content

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Warning Icon | Yes | ✅ | Both modal variants show a prominent red warning icon at the top |
| Modal Title | Yes | ❌⚠️ | `Remove Payment Method?` is correct, but it is rendered in dark text rather than the specified red/destructive title styling |
| Method Summary | Yes | ❌ | Neither modal includes a dedicated in-modal summary of the card being removed (brand, last 4 digits, expiry); the non-default state only leaves the card partially visible in the dimmed background |
| Warning Message | Yes | ✅ | Both modal variants include the required consequence explanation, with dynamic messaging for permanent removal vs installment-linked removal |
| Default Reassignment Notice (Conditional) | Conditional | ✅ | `Default Card.jpg` shows the reassignment notice to `American Express •••• 4242` |
| Active Installments Warning (Conditional) | Conditional | ✅ | `Default Card.jpg` warns that the card is currently used for scheduled installment payments and that the patient will need to update the method |
| Remove Button | Yes | ✅ | Both modal variants include a destructive red `Remove` button |
| Go Back Button | Yes | ✅ | Both modal variants include `Go back` as the neutral dismissal action |

**Extra Elements**:

- None

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 7/8 (88%)
**Critical Issues**: The modal does not clearly identify which saved payment method is being removed inside the confirmation content

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| None | No standalone UX/UI issues were identified beyond the documented method-summary gap and title-styling mismatch. The modal hierarchy and CTA separation are otherwise clear | None |

**Flow Coverage Gaps**:

- The edit-mode form does not evidence the required `Replace card` path or the rule that credential fields are not directly editable
- The remove-confirmation modal does not include the required in-modal card summary identifying the method being removed
- The `first payment method forces default ON` state is not explicitly evidenced in the current add-form layout set

---

## Action Items

| Priority | Flow | Screen | Issue | Recommendation |
|----------|------|--------|-------|----------------|
| ⚠️ Important | P03.1 | P03.1-S2 | Edit mode appears to allow direct editing of expiry/CVV and lacks the required `Replace card` path | Redesign edit mode so card credentials are replace-only and expose a clear `Replace card` action for new-card entry |
| ⚠️ Important | P03.1 | P03.1-S3 | Remove confirmation modal does not include the required in-modal method summary | Add the card brand, masked last 4 digits, and expiry inside the modal content so patients can verify the exact card being removed |
| 💡 Suggestion | P03.1 | P03.1-S3 | Modal title is not styled in the specified destructive red treatment | Restyle the title to match the destructive emphasis if that visual requirement is still intended |
| 💡 Suggestion | P03.1 | P03.1-S2 | First-method forced-default state is not evidenced | Add a first-method add-form variant showing the default toggle forced ON if that behavior should be visually documented |

### Priority Legend

- **🔴 Critical**: Blocks flow progression, breaks data integrity, or causes security/legal risk. Must fix before development.
- **🔴 Critical UX**: Severe usability issue that would prevent users from completing the flow or cause significant confusion. Must fix before development.
- **⚠️ Important**: Functional discrepancy that could cause user confusion or require rework during development. Should fix before development.
- **⚠️ UX Improvement**: Usability or design quality issue that deviates from platform conventions or best practices. Should fix before development.
- **💡 Suggestion**: Cosmetic or minor improvement. Can fix anytime.
- **💡 UX Suggestion**: Minor design enhancement that would improve polish. Can fix anytime.

---

## Notes

- Verification was performed against Flow `P03.1` only
- The current layouts cover the main happy path, empty state, blocked-removal notice, add/edit form, and remove modal variants
- The overall `PARTIAL` verdict is driven by edit-mode and removal-confirmation rule mismatches rather than missing primary screens
- User approval was granted on 2026-03-24 to accept the remaining findings as minor and defer further revision
- Source specification: `local-docs/reports/2026-02-05/missing-mobile-flows-design-complement.md`
- Related FR references: `local-docs/project-requirements/functional-requirements/fr007-payment-processing/prd.md`, `local-docs/project-requirements/functional-requirements/fr007b-payment-installments/prd.md`
