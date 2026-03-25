# Design Layout Verification Report — FR-011 Patient Mobile

**Report Date**: 2026-03-25
**Report Type**: Design Layout Verification
**FR Scope**: FR-011 - Aftercare & Recovery Management
**Flow Scope**: FR-011 patient mobile screens only: Workflow 2 (Standalone Aftercare Service), Workflow 2b (Post-Treatment Aftercare Add-On), and Workflow 3 (Patient Aftercare Activities)
**Layout Source**: `layout-temp/aftercare/`
**Platform**: Patient Mobile
**Status**: 🔴 BLOCKED — all 3 in-scope FR-011 mobile flows still have implementation-blocking design gaps

---

## Summary Dashboard

| # | Flow | Module | Screens Required | Screens Verified | Layout Status | Field Coverage |
|---|------|--------|-----------------|-----------------|---------------|----------------|
| FR011-W2 | Standalone Aftercare Service | P-05: Aftercare & Progress Monitoring | 2 | 2 | 🟡 PARTIAL | ~91% |
| FR011-W2b | Post-Treatment Aftercare Add-On | P-05: Aftercare & Progress Monitoring | 2 | 2 | 🔴 BLOCKED | ~93% |
| FR011-W3 | Patient Aftercare Activities | P-05: Aftercare & Progress Monitoring | 5 | 5 | 🔴 BLOCKED | ~82% |

**Overall**: 0 of 3 flows verified as complete. 1 flow is partially aligned and 2 flows remain blocked by incomplete design coverage.
**Screens**: 9 of 9 in-scope FR-011 mobile screens have at least one mapped layout (100% mapped coverage), but several screens still fail field-level verification.

---

## Layout File Inventory

### Mapped to Spec Flows

| Layout File | Maps to Flow | Maps to Screen |
|-------------|-------------|----------------|
| `aftercare/Aftercare single.jpg` | FR011-W3 | Screen 1 (Aftercare Dashboard) |
| `aftercare/Milestone Detailed.jpg` | FR011-W3 | Screen 1 (Aftercare Dashboard - milestone detail state) |
| `aftercare/Scan Upload.jpg` | FR011-W3 | Screen 2 (Scan Upload) |
| `aftercare/Scan Upload/After scanning.jpg` | FR011-W3 | Screen 2 (Scan Upload - uploaded state) |
| `aftercare/Single Choice.jpg` | FR011-W3 | Screen 3 (Questionnaire Completion) |
| `aftercare/Single Choice-1.jpg` | FR011-W3 | Screen 3 (Questionnaire Completion) |
| `aftercare/Visual Scale Questions (5 option scale).jpg` | FR011-W3 | Screen 3 (Questionnaire Completion) |
| `aftercare/Visual Scale Questions (10 option scale).jpg` | FR011-W3 | Screen 3 (Questionnaire Completion) |
| `aftercare/Question Text Field.jpg` | FR011-W3 | Screen 3 (Questionnaire Completion) |
| `aftercare/Medication.jpg` | FR011-W3 | Screen 4 (Medication Schedule) |
| `aftercare/Instruction.jpg` | FR011-W3 | Screen 5 (Educational Resources) |
| `aftercare/Available Aftercare Services.jpg` | FR011-W2 | Screen 6 (Aftercare Service Purchase) |
| `aftercare/Available Aftercare Services-1.jpg` | FR011-W2 | Screen 6 (Aftercare Service Purchase) |
| `aftercare/Entry Point (Aftercare Service Purchase) - Standlone.jpg` | FR011-W2 | Screen 6 (Aftercare Service Purchase - entry point) |
| `aftercare/External Treatment Details.jpg` | FR011-W2 | Screen 6 (Aftercare Service Purchase - external treatment details state) |
| `aftercare/Aftercare Payment & Checkout/Payment type_ fixed.jpg` | FR011-W2 | Screen 7 (Aftercare Payment & Checkout) |
| `aftercare/Aftercare Payment & Checkout/Payment type_ Monthly Subscription.jpg` | FR011-W2 | Screen 7 (Aftercare Payment & Checkout) |
| `aftercare/post-treatment add-on.jpg` | FR011-W2b | Screen 6 (Aftercare Service Purchase - post-treatment add-on entry) |

### Unmapped Files

| Layout File | Likely Purpose | Notes |
|-------------|---------------|-------|
| `aftercare/My Treatments List.jpg` | My Treatments list variant | Outside the narrowed FR-011-only scope; relates to the `P05.2` mobile-complement screen, not an FR-011 patient screen |
| `aftercare/My Treatments List-1.jpg` | My Treatments list variant | Outside the narrowed FR-011-only scope; relates to the `P05.2` mobile-complement screen, not an FR-011 patient screen |

---

## Detailed Verification by Flow

---

### Flow FR011-W2: Standalone Aftercare Service

**Status**: 🟡 PARTIAL — service request, shared payment-method handling, and checkout are broadly designed, but Screen 6 still underspecifies pricing-method selection before checkout
**Screens required**: 2
**Layout files**: `aftercare/Available Aftercare Services.jpg`, `aftercare/Available Aftercare Services-1.jpg`, `aftercare/Entry Point (Aftercare Service Purchase) - Standlone.jpg`, `aftercare/External Treatment Details.jpg`, `aftercare/Aftercare Payment & Checkout/Payment type_ fixed.jpg`, `aftercare/Aftercare Payment & Checkout/Payment type_ Monthly Subscription.jpg`

#### Screen 6: Aftercare Service Purchase

**Layout**: `aftercare/Entry Point (Aftercare Service Purchase) - Standlone.jpg`, `aftercare/External Treatment Details.jpg`, `aftercare/Available Aftercare Services.jpg`, `aftercare/Available Aftercare Services-1.jpg`

##### Flow Context

- **User arrives from**: Patient uses the app entry point for standalone aftercare purchase per FR-011 Workflow 2 step 1.
- **Screen purpose**: Capture standalone treatment details, show purchasable aftercare services, and move the patient to checkout.
- **Entry point**: Present via `Entry Point (Aftercare Service Purchase) - Standlone.jpg`, then the info step in `External Treatment Details.jpg`.
- **Exit path**: Present via `Next step` CTA from info and services views.
- **Data continuity**: Partial. Standalone treatment details are captured, and the chosen pricing method plus total are visible in the next-step checkout layouts, but they are not confirmed on Screen 6 before the handoff.
- **Flow context issues**: Entry screen wording does not match the FR's service-type choices, and the pricing-choice / total-confirmation state appears in Screen 7 checkout rather than on Screen 6. This is a screen-boundary mismatch against the current FR-011 spec, not a full-flow omission.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Service Type | Yes | ❌⚠️ | Entry screen offers `Create request for full service` and `Purchase Aftercare Service`; FR-011 Screen 6 requires `Post-Treatment Add-On` vs `Standalone Service`. Layout file: `aftercare/Entry Point (Aftercare Service Purchase) - Standlone.jpg`. |
| Treatment Information | Conditional | ✅ | Correctly absent for standalone path. FR-011 marks this only for `post_treatment`. |
| External Treatment Details | Conditional | ✅ | Present as the info-step form in `aftercare/External Treatment Details.jpg`. |
| Treatment Date | Conditional | ✅ | Present in `aftercare/External Treatment Details.jpg`. |
| Treatment Type | Conditional | ✅ | Present in `aftercare/External Treatment Details.jpg`. |
| Treating Clinic | Conditional | ✅ | Present in `aftercare/External Treatment Details.jpg`. |
| Upload Treatment Documentation | No | ✅ | Optional upload block present in `aftercare/External Treatment Details.jpg`. |
| Available Aftercare Services | Yes | ✅ | Service list present in `aftercare/Available Aftercare Services.jpg`. |
| Service Name | Yes | ✅ | Present in service cards and detail state. |
| Service Description | Yes | ✅ | Present in service cards and detail state. |
| Duration | Yes | ✅ | Present in service cards and detail state. |
| Milestones Included | Yes | ✅ | Milestone list shown in `aftercare/Available Aftercare Services-1.jpg`. |
| Features Included | Yes | ✅ | Features list shown in `aftercare/Available Aftercare Services-1.jpg`. |
| Pricing Options | Yes | ✅ | Both fixed and monthly pricing are displayed in `aftercare/Available Aftercare Services.jpg`. |
| Payment Method | Conditional | ❌⚠️ | FR-011 requires an explicit fixed-vs-subscription choice on Screen 6 when both are available. The design shows that choice later in Screen 7 (`Payment type_ fixed.jpg` / `Payment type_ Monthly Subscription.jpg`), not on the services step itself. |
| Price (Fixed) | Conditional | ✅ | Present as `$2,500` in `aftercare/Available Aftercare Services.jpg`. |
| Price (Monthly) | Conditional | ✅ | Present as `$1000 / month` in `aftercare/Available Aftercare Services.jpg`. |
| Total Amount | Yes | ❌⚠️ | The total amount is shown in the Screen 7 checkout layouts, but no Screen 6 service-selection state shows it before proceeding to checkout. |
| Currency | Yes | ⚠️ | Dollar symbol is visible, but currency is implied rather than explicitly labeled. |
| Selected Service | Yes | ✅ | `Select Service` CTA and selected card styling indicate service selection. |
| Selected Payment Method | Conditional | ❌⚠️ | The selected pricing method becomes visible in Screen 7 checkout, but Screen 6 does not show which option was chosen before the handoff. |
| Current Concerns | No | ✅ | Present as optional textarea in `aftercare/External Treatment Details.jpg`. |
| Upload Photos | No | ✅ | Present as optional current-condition upload block. |
| Proceed to Payment | Yes | ✅ | `Next step` button is present on the info and service views. |

**Extra Elements**:

- Three-step progress indicator (`Info`, `Services`, `Checkout`) appears across the purchase flow. This is a useful enhancement but is not explicitly listed as a Screen 6 field in FR-011.

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 16/20 (80%)
**Critical Issues**: None. The screen remains navigable, but pricing-method selection and total confirmation are shifted into Screen 7 instead of being shown on Screen 6 as specified.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-17` CTA label clarity: the primary action is labeled `Next step`, which is generic for a paid healthcare flow and does not communicate that the user is proceeding to checkout. Evidence: `aftercare/External Treatment Details.jpg`, `aftercare/Available Aftercare Services.jpg`. | Rename the CTA to `Continue to Checkout` or equivalent. |
| ⚠️ UX Improvement | `U-23` terminology consistency: the entry screen mixes `Create request for full service` with `Purchase Aftercare Service`, while FR-011 Screen 6 defines service-type choices as standalone vs post-treatment add-on. Evidence: `aftercare/Entry Point (Aftercare Service Purchase) - Standlone.jpg`. | Align entry labels to the FR service types or clearly separate this entry screen from the FR-011 purchase flow. |

#### Screen 7: Aftercare Payment & Checkout

**Layout**: `aftercare/Aftercare Payment & Checkout/Payment type_ fixed.jpg`, `aftercare/Aftercare Payment & Checkout/Payment type_ Monthly Subscription.jpg`

##### Flow Context

- **User arrives from**: Selected aftercare service in Screen 6.
- **Screen purpose**: Review order details, choose payment method, provide payment details, accept policies, and complete payment.
- **Entry point**: Present. Both fixed-price and subscription checkout variants are designed.
- **Exit path**: Present through `Checkout` CTA and `Previous step` back path.
- **Data continuity**: Good. The selected service, price, and subscription totals carry forward correctly, and new-card / billing-address capture is handled through the shared payment-method flow already verified in `design-layout-verification-missing-mobile-flows-design-complement-p03.1.md`.
- **Flow context issues**: The checkout view itself shows saved-card selection plus an `Add Payment Method` handoff, so payment-input fields are not repeated inline.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Order Summary | Yes | ✅ | Present in both checkout variants. |
| Service Name | Yes | ✅ | Present. |
| Duration | Yes | ✅ | Present. |
| Payment Method Selected | Yes | ✅ | `Fixed` and `Monthly Subscription` tabs show the selected pricing mode. |
| Subtotal | Yes | ✅ | Present. |
| Platform Fee | Yes | ✅ | Present. |
| Tax | Yes | ✅ | Present. |
| Total Amount | Yes | ✅ | Present in both variants. |
| Monthly Payment Details | Conditional | ✅ | Present in `Payment type_ Monthly Subscription.jpg`. |
| Monthly Amount | Yes | ✅ | Present in subscription layout. |
| Number of Months | Yes | ✅ | Present in subscription layout. |
| Total Subscription Amount | Yes | ✅ | Present in subscription layout. |
| Payment Method Selection | Yes | ✅ | Saved-card radio list is present. |
| Card Number | Conditional | ✅ | Managed through the shared `P03.1-S2 Add/Edit Payment Method` screens, reached from `Add Payment Method`. |
| Expiry Date | Conditional | ✅ | Managed through the shared `P03.1-S2 Add/Edit Payment Method` screens. |
| CVV | Conditional | ✅ | Managed through the shared `P03.1-S2 Add/Edit Payment Method` screens. |
| Cardholder Name | Conditional | ✅ | Managed through the shared `P03.1-S2 Add/Edit Payment Method` screens. |
| Billing Address | Yes | ✅ | Captured in the shared `P03.1-S2 Add/Edit Payment Method` flow rather than repeated inline on checkout. |
| Street Address | Yes | ✅ | Managed through the shared `P03.1-S2 Add/Edit Payment Method` screens. |
| City | Yes | ✅ | Managed through the shared `P03.1-S2 Add/Edit Payment Method` screens. |
| State/Province | Yes | ✅ | Managed through the shared `P03.1-S2 Add/Edit Payment Method` screens. |
| Postal Code | Yes | ✅ | Managed through the shared `P03.1-S2 Add/Edit Payment Method` screens. |
| Country | Yes | ✅ | Managed through the shared `P03.1-S2 Add/Edit Payment Method` screens. |
| Terms & Conditions | Yes | ✅ | Present as agreement item. |
| Privacy Policy | Yes | ✅ | Present as agreement item. |
| Payment Processing | No | ❌ | No loading, processing, or retry state is shown. |
| Complete Payment | Yes | ✅ | `Checkout` CTA is present. |

**Extra Elements**:

- `Add Payment Method` is present, implying a separate saved-card flow not covered by the supplied layouts.

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 26/26 (100%)
**Critical Issues**: None. Card and billing capture are satisfied through the shared payment-method screens already verified in `P03.1`.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| 💡 UX Suggestion | `U-11` label clarity: `Payment Type` can be misread as tender type, while the FR field is actually the selected pricing model (fixed vs monthly subscription). Evidence: both checkout layouts. | Rename the segmented control label to `Pricing Option` or `Plan Type`. |

**Flow Coverage Gaps**:

- No payment-failure or retry layout is present for Workflow 2 alternative flow B1.
- No payment-success confirmation layout is present after checkout.

---

### Flow FR011-W2b: Post-Treatment Aftercare Add-On

**Status**: 🔴 BLOCKED — add-on intake is mostly represented, but Screen 6 still omits explicit pricing-method selection and total-before-checkout coverage even though Screen 7 is satisfied through the shared payment-method flow
**Screens required**: 2
**Layout files**: `aftercare/post-treatment add-on.jpg`, `aftercare/Available Aftercare Services.jpg`, `aftercare/Available Aftercare Services-1.jpg`, `aftercare/Aftercare Payment & Checkout/Payment type_ fixed.jpg`, `aftercare/Aftercare Payment & Checkout/Payment type_ Monthly Subscription.jpg`

#### Screen 6: Aftercare Service Purchase

**Layout**: `aftercare/post-treatment add-on.jpg`, `aftercare/Available Aftercare Services.jpg`, `aftercare/Available Aftercare Services-1.jpg`

##### Flow Context

- **User arrives from**: Hairline-treated patient selects `Add Aftercare Service` after treatment completion, per FR-011 Workflow 2b step 1.
- **Screen purpose**: Reuse the purchase flow with treatment history prefilled for a post-treatment add-on request.
- **Entry point**: Present as prefilled treatment-information step in `aftercare/post-treatment add-on.jpg`.
- **Exit path**: Present via `Next step` CTA to the services step.
- **Data continuity**: Mostly correct. Treatment data is auto-populated as required by Workflow 2b, and the pricing method plus total appear in the next-step checkout layouts, but they are not explicit on Screen 6 before checkout.
- **Flow context issues**: No visible indicator confirms the 90-day eligibility check or that the service type is specifically `post_treatment`. The pricing-choice / total-confirmation state is represented in Screen 7 checkout rather than on Screen 6, so this is best described as a screen-boundary mismatch against the FR rather than a full-flow omission.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Service Type | Yes | ⚠️ | Not shown as a separate control, but FR-011 notes service type may be auto-detected from treatment history. Current layout implies post-treatment context without explicitly labeling it. |
| Treatment Information | Conditional | ✅ | Present as the prefilled treatment-information block in `aftercare/post-treatment add-on.jpg`. |
| External Treatment Details | Conditional | ✅ | Correctly absent for post-treatment add-on path. |
| Treatment Date | Conditional | ✅ | Present and prefilled. |
| Treatment Type | Conditional | ✅ | Present and prefilled. |
| Treating Clinic | Conditional | ✅ | Present and prefilled. |
| Upload Treatment Documentation | No | ✅ | Present. |
| Available Aftercare Services | Yes | ✅ | Present in `aftercare/Available Aftercare Services.jpg`. |
| Service Name | Yes | ✅ | Present. |
| Service Description | Yes | ✅ | Present. |
| Duration | Yes | ✅ | Present. |
| Milestones Included | Yes | ✅ | Present in service detail state. |
| Features Included | Yes | ✅ | Present in service detail state. |
| Pricing Options | Yes | ✅ | Both price types are shown. |
| Payment Method | Conditional | ❌⚠️ | No explicit fixed-vs-subscription selector exists on Screen 6. The design shows that choice later in the Screen 7 checkout layouts. |
| Price (Fixed) | Conditional | ✅ | Present. |
| Price (Monthly) | Conditional | ✅ | Present. |
| Total Amount | Yes | ❌⚠️ | A total is shown in the Screen 7 checkout layouts, but no combined total appears on Screen 6 before checkout. |
| Currency | Yes | ⚠️ | Currency is implied by `$`, not explicitly labeled. |
| Selected Service | Yes | ✅ | Selection control is visible through `Select Service`. |
| Selected Payment Method | Conditional | ❌⚠️ | The chosen pricing mode becomes visible in Screen 7 checkout, but is not shown on Screen 6 before checkout. |
| Current Concerns | No | ✅ | Present. |
| Upload Photos | No | ✅ | Present. |
| Proceed to Payment | Yes | ✅ | `Next step` CTA is present. |

**Extra Elements**:

- Stepper (`Info`, `Services`, `Checkout`) is a helpful addition beyond the FR field table.

**Screen Status**: 🔴 FAIL
**Field Coverage**: 17/20 (85%)
**Critical Issues**: Three required Screen 6 fields are shifted into the Screen 7 checkout step instead of being represented on Screen 6: explicit payment-method choice, selected payment method, and total amount.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-17` CTA label clarity: `Next step` is too generic for a purchase handoff and does not tell the patient they are moving toward payment. Evidence: `aftercare/post-treatment add-on.jpg`, `aftercare/Available Aftercare Services.jpg`. | Rename to `Continue to Checkout`. |
| 💡 UX Suggestion | `U-02` information priority: the add-on intake screen does not visibly communicate the key eligibility context (`within 90 days` / matched to prior treatment), even though Workflow 2b depends on it. Evidence: `aftercare/post-treatment add-on.jpg`. | Add a short eligibility or source-treatment summary near the title. |

#### Screen 7: Aftercare Payment & Checkout

**Layout**: `aftercare/Aftercare Payment & Checkout/Payment type_ fixed.jpg`, `aftercare/Aftercare Payment & Checkout/Payment type_ Monthly Subscription.jpg`

##### Flow Context

- **User arrives from**: Add-on service selection in Screen 6.
- **Screen purpose**: Review selected add-on package and complete payment.
- **Entry point**: Present.
- **Exit path**: Present through `Checkout` CTA and `Previous step`.
- **Data continuity**: Good. Service and pricing details carry over correctly, and card / billing capture is handled by the shared `P03.1` payment-method screens.
- **Flow context issues**: The checkout state reuses the shared payment-method flow rather than duplicating card-entry fields inline.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Order Summary | Yes | ✅ | Present. |
| Service Name | Yes | ✅ | Present. |
| Duration | Yes | ✅ | Present. |
| Payment Method Selected | Yes | ✅ | Pricing mode is visible through the segmented control. |
| Subtotal | Yes | ✅ | Present. |
| Platform Fee | Yes | ✅ | Present. |
| Tax | Yes | ✅ | Present. |
| Total Amount | Yes | ✅ | Present. |
| Monthly Payment Details | Conditional | ✅ | Present in subscription variant. |
| Monthly Amount | Yes | ✅ | Present in subscription variant. |
| Number of Months | Yes | ✅ | Present in subscription variant. |
| Total Subscription Amount | Yes | ✅ | Present in subscription variant. |
| Payment Method Selection | Yes | ✅ | Present. |
| Card Number | Conditional | ✅ | Managed through the shared `P03.1-S2 Add/Edit Payment Method` screens. |
| Expiry Date | Conditional | ✅ | Managed through the shared `P03.1-S2 Add/Edit Payment Method` screens. |
| CVV | Conditional | ✅ | Managed through the shared `P03.1-S2 Add/Edit Payment Method` screens. |
| Cardholder Name | Conditional | ✅ | Managed through the shared `P03.1-S2 Add/Edit Payment Method` screens. |
| Billing Address | Yes | ✅ | Captured in the shared `P03.1-S2 Add/Edit Payment Method` flow. |
| Street Address | Yes | ✅ | Managed through the shared `P03.1-S2 Add/Edit Payment Method` screens. |
| City | Yes | ✅ | Managed through the shared `P03.1-S2 Add/Edit Payment Method` screens. |
| State/Province | Yes | ✅ | Managed through the shared `P03.1-S2 Add/Edit Payment Method` screens. |
| Postal Code | Yes | ✅ | Managed through the shared `P03.1-S2 Add/Edit Payment Method` screens. |
| Country | Yes | ✅ | Managed through the shared `P03.1-S2 Add/Edit Payment Method` screens. |
| Terms & Conditions | Yes | ✅ | Present. |
| Privacy Policy | Yes | ✅ | Present. |
| Payment Processing | No | ❌ | No processing/retry state shown. |
| Complete Payment | Yes | ✅ | Present. |

**Extra Elements**:

- `Add Payment Method` suggests an external saved-card flow, but that supporting design is not included in scope.

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 26/26 (100%)
**Critical Issues**: None. The dependent payment-method screens cover the card and billing fields.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| 💡 UX Suggestion | `U-11` label clarity: `Payment Type` reads like tender type rather than plan type. Evidence: both checkout layouts. | Rename to `Pricing Option` or `Billing Plan`. |

**Flow Coverage Gaps**:

- No automatic-assignment confirmation state is shown after payment success.
- No payment-failure retry layout is shown for Workflow 2b alternative flow B1b.

---

### Flow FR011-W3: Patient Aftercare Activities

**Status**: 🔴 BLOCKED — under a shared-tab-shell interpretation, dashboard, medication, and instructional-resource tabs are more aligned than the first pass suggested, but questionnaire coverage still fails and scan/resource gaps remain
**Screens required**: 5
**Layout files**: `aftercare/Aftercare single.jpg`, `aftercare/Milestone Detailed.jpg`, `aftercare/Scan Upload.jpg`, `aftercare/Scan Upload/After scanning.jpg`, `aftercare/Single Choice.jpg`, `aftercare/Single Choice-1.jpg`, `aftercare/Visual Scale Questions (5 option scale).jpg`, `aftercare/Visual Scale Questions (10 option scale).jpg`, `aftercare/Question Text Field.jpg`, `aftercare/Medication.jpg`, `aftercare/Instruction.jpg`

#### Screen 1: Aftercare Dashboard

**Layout**: `aftercare/Aftercare single.jpg`, `aftercare/Milestone Detailed.jpg`

##### Flow Context

- **User arrives from**: Activation notification or ongoing aftercare entry, per FR-011 Workflow 3.
- **Screen purpose**: Central hub for milestone progress, next tasks, and quick actions.
- **Entry point**: Present. `Aftercare single.jpg` acts as the dashboard overview.
- **Exit path**: Present via milestone tap-through, `Upload Scan`, `Complete Questionnaire`, medication tab, instruction tab, and support action.
- **Data continuity**: Good. Progress, upcoming tasks, medication adherence, and milestone detail are all visible.
- **Flow context issues**: Last scan upload and last questionnaire completion are not surfaced as separate dashboard summary items.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Overall Progress | Yes | ✅ | Present as `10% Overall progress`. |
| Current Milestone | Yes | ✅ | Present via current milestone cards and the `1st Milestone` / `Current` state in `Milestone Detailed.jpg`. |
| Days Remaining | No | ✅ | Remaining days shown on milestone card. |
| Next Task | No | ✅ | Upcoming-task list and next scan/questionnaire timestamps are shown. |
| Last Scan Upload | No | ❌ | Dashboard shows next scan timing, but not the last completed scan timestamp/status. |
| Last Questionnaire | No | ❌ | Dashboard shows next questionnaire timing, but not the last completed questionnaire timestamp. |
| Medication Adherence | No | ✅ | Present as dedicated adherence card. |
| Upcoming Tasks | No | ✅ | Present as task list. |
| Upload Scan | Conditional | ✅ | Present as quick action. |
| Complete Questionnaire | Conditional | ✅ | Present as quick action. |
| View Instructions | No | ✅ | Instruction tab provides access to instructions. |
| Contact Support | No | ✅ | `Need help` / support contact action is present. |

**Extra Elements**:

- Completed and due task sections add useful historical context beyond the minimum FR field table.

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 4/4 (100%)
**Critical Issues**: None.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| 💡 UX Suggestion | `U-04` section headings: the dashboard has many stacked regions, and `Upcoming Tasks`, `Connect With Aftercare support`, and completed tasks could benefit from slightly stronger section separation. Evidence: `aftercare/Aftercare single.jpg`. | Add clearer section labels or spacing to improve scanability. |

#### Screen 2: Scan Upload (V1 Photo Set)

**Layout**: `aftercare/Scan Upload.jpg`, `aftercare/Scan Upload/After scanning.jpg`

##### Flow Context

- **User arrives from**: Dashboard quick action or scan reminder notification.
- **Screen purpose**: Capture and upload scheduled milestone scan media.
- **Entry point**: Present.
- **Exit path**: Present through capture, upload, and retake actions.
- **Data continuity**: Partial. The due date and guidance carry through, but the milestone label and historical scan access are missing.
- **Flow context issues**: Static layouts do not show upload progress or previous-scan comparison access.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Milestone Name | Yes | ❌ | Title is only `Scan Upload`; current milestone name is not shown. |
| Scan Due Date | Yes | ✅ | Present. |
| Days Overdue | No | ✅ | Correctly absent in non-overdue state. |
| Scan Guidance | No | ✅ | Present as info box. |
| Camera Viewfinder | Yes | ✅ | Present in capture state. |
| Quality Indicator | Yes | ✅ | Present as three-dot quality indicator. |
| Capture Scan | Yes | ✅ | Present as `Scan head`. |
| Retake | Conditional | ✅ | Present in uploaded-preview state. |
| Upload Progress | No | ❌ | No upload progress indicator shown. |
| Upload Status | No | ❌ | No explicit success/error message shown after upload. |
| View Previous Scans | No | ❌ | No previous-scan access shown. |

**Extra Elements**:

- The preview state is clear and aligned to mobile capture expectations.

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 4/5 (80%)
**Critical Issues**: Milestone name is missing from a required scan task screen.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-02` information priority: the current milestone identity is absent, so patients only see a generic scan task without knowing which recovery phase it belongs to. Evidence: both scan-upload layouts. | Add milestone name/phase near the title or due date. |

#### Screen 3: Questionnaire Completion

**Layout**: `aftercare/Single Choice.jpg`, `aftercare/Single Choice-1.jpg`, `aftercare/Visual Scale Questions (5 option scale).jpg`, `aftercare/Visual Scale Questions (10 option scale).jpg`, `aftercare/Question Text Field.jpg`

##### Flow Context

- **User arrives from**: Dashboard quick action or questionnaire reminder notification.
- **Screen purpose**: Render milestone-specific questions and allow submission.
- **Entry point**: Present through several question-type variants.
- **Exit path**: Present only through `Submit`.
- **Data continuity**: Weak. The designs focus on individual questions but omit milestone, questionnaire-set, and due-status context.
- **Flow context issues**: No draft state or completion-status context is visible, which reduces traceability in an ongoing care flow.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Milestone Name | Yes | ❌ | No milestone or phase label is visible in any questionnaire layout. |
| Questionnaire Set | Yes | ❌ | No questionnaire-set title or identifier is shown. |
| Due Date | Yes | ❌ | Missing from all variants. |
| Completion Status | Yes | ❌ | Missing from all variants. |
| Questions | Yes | ✅ | Dynamic question rendering is clearly represented across select, radio, scale, and text variants. |
| Save Draft | No | ❌ | No draft/save action shown. |
| Submit | Yes | ✅ | Present. |
| Warning Message | No | ❌ | No concerning-response warning state shown. |

**Extra Elements**:

- Question-type variation coverage is strong: select, radio, scale, and text are all designed.

**Screen Status**: 🔴 FAIL
**Field Coverage**: 2/6 (33%)
**Critical Issues**: Four required contextual fields are missing: milestone, questionnaire set, due date, and completion status.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-02` information priority: the screen shows the current question but hides the patient’s care context, so users cannot tell which milestone or questionnaire they are completing. Evidence: all questionnaire layouts. | Add milestone name, questionnaire title, and due status at the top. |
| 💡 UX Suggestion | `U-26` progress indication: multi-question completion is implied, but no progress indicator shows how many questions remain. Evidence: all questionnaire layouts. | Add step count or progress bar for longer questionnaires. |

#### Screen 4: Medication Schedule

**Layout**: `aftercare/Medication.jpg`

##### Flow Context

- **User arrives from**: Dashboard tab navigation or medication-related reminders.
- **Screen purpose**: Track today's doses, adherence, and medication history.
- **Entry point**: Present.
- **Exit path**: Present through mark-taken / undo actions and tab navigation.
- **Data continuity**: Good. The layout includes adherence, today’s doses, full medication cards, and history.
- **Flow context issues**: View-history is embedded as a section instead of a separate link, but the information is still accessible.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Medication Name | Yes | ✅ | Present. |
| Dosage | Yes | ✅ | Present. |
| Frequency | Yes | ✅ | Present. |
| Special Instructions | No | ✅ | Present as descriptive text on medication cards. |
| Start Date | Yes | ✅ | Present. |
| End Date | Yes | ✅ | Present. |
| Today's Doses | Yes | ✅ | Present. |
| Dose Time | Yes | ✅ | Present. |
| Mark as Taken | Yes | ✅ | Present as button. |
| Missed Dose Indicator | No | ✅ | History section shows missed-status indicators and `2 missed doses`. |
| Weekly Adherence | Yes | ✅ | Present. |
| Missed Doses Count | Yes | ✅ | Present. |
| View History | No | ⚠️ | Implemented as an inline history section rather than a separate link. Functional but structurally different from spec. |

**Extra Elements**:

- Inline history is richer than the FR minimum.

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 10/10 (100%)
**Critical Issues**: None.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| 💡 UX Suggestion | `U-12` text truncation: longer medication descriptions are cramped inside the card body and may be hard to scan quickly. Evidence: `aftercare/Medication.jpg`. | Increase line spacing or collapse long notes behind a `Read more` action. |

#### Screen 5: Educational Resources

**Layout**: `aftercare/Instruction.jpg`

##### Flow Context

- **User arrives from**: Dashboard instruction tab or milestone detail flow.
- **Screen purpose**: Display milestone-specific instructions and downloadable resources.
- **Entry point**: Present.
- **Exit path**: Present through tab navigation and resource actions.
- **Data continuity**: Partial. The active `Instruction` tab inherits the common Aftercare shell, so shared context does not need to repeat here, but explicit resource-progress counters are still incomplete.
- **Flow context issues**: Under the shared-tab-shell interpretation, header/context duplication is no longer treated as required; the remaining gap is resource-specific progress tracking.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Resource Category | Yes | ⚠️ | The active `Instruction` tab and `Resources` section provide category context at the shell level, but there is no explicit per-resource category label. |
| Resource Title | Yes | ✅ | Present. |
| Resource Description | No | ✅ | Present for instruction cards; absent for PDF rows but optional. |
| Resource Type | Yes | ✅ | PDF iconography and the resource row structure make the downloadable type clear in the tabbed interface. |
| Resource URL | Yes | ✅ | `View` / `Download` actions provide the required access path even though the raw URL/file path is not printed. |
| Duration | Conditional | ✅ | Correctly absent for non-video resources. |
| File Size | Conditional | ❌ | Missing for downloadable PDFs. |
| Mark as Viewed | No | ❌⚠️ | Implemented as `Mark as read` button rather than checkbox. Functional intent is similar, but control type differs. |
| View/Download | Yes | ✅ | Present. |
| Resources Viewed Count | Yes | ❌ | Missing. |
| Total Resources | Yes | ❌ | Missing. |
| Completion Percentage | Yes | ❌ | Missing. |
| Mark All as Viewed | No | ❌ | Missing. |

**Extra Elements**:

- Emergency contact card is present at the bottom; this is helpful but not specified in Screen 5.

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 5/8 (62%)
**Critical Issues**: None. The blocking issue is reduced to missing resource-progress counters rather than a fundamentally unusable screen.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-02` information priority: within the shared tab shell, the resource list is understandable, but the screen still does not show any resource-specific completion/progress signal even though FR-011 expects compliance tracking for educational resources. Evidence: `aftercare/Instruction.jpg`. | Add viewed-count and completion-progress summary near the top of the tab. |
| 💡 UX Suggestion | `U-23` terminology consistency: the tab is labeled `Instruction`, while the FR screen is `Educational Resources`. Evidence: `aftercare/Instruction.jpg`. | Align terminology with the product spec or clearly distinguish instructions from broader resources. |

**Flow Coverage Gaps**:

- No overdue-task state is shown for Workflow 3 alternative flow C1.
- No urgent/concerning-response alert state is shown for Workflow 3 alternative flow C2.
- Questionnaire metadata remains underdesigned relative to FR-011.
- Educational resources are workable within the shared tab shell, but still missing explicit resource-progress counters.

---

## Action Items

| Priority | Flow | Screen | Issue | Recommendation |
|----------|------|--------|-------|----------------|
| 🔴 Critical | FR011-W2b | Screen 6 | Add-on purchase flow shows pricing choice and totals only in Screen 7 checkout, not on Screen 6 where the FR currently requires them | Either add the pricing-method selector and total summary to Screen 6, or revise the FR/design boundary so those fields are intentionally owned by Screen 7 |
| 🔴 Critical | FR011-W3 | Screen 3 | Questionnaire screen omits milestone, questionnaire-set, due date, and completion-status context | Add the full questionnaire header metadata and, ideally, progress indication |
| ⚠️ Important | FR011-W3 | Screen 5 | Educational resources tab still lacks explicit resource-progress tracking fields | Add viewed-count, total-resources count, and completion percentage summary inside the shared tab shell |
| ⚠️ Important | FR011-W2 | Screen 6 | Standalone entry wording does not match FR-011 service-type terminology | Align the entry options to `Standalone Service` / `Post-Treatment Add-On` or explicitly separate pre-entry from Screen 6 |
| ⚠️ Important | FR011-W3 | Screen 2 | Scan-upload screen hides the required milestone identity | Add milestone name and phase above the due date |

### Priority Legend

- **🔴 Critical**: Blocks flow progression, breaks data integrity, or causes security/legal risk. Must fix before development.
- **🔴 Critical UX**: Severe usability issue that would prevent users from completing the flow or cause significant confusion. Must fix before development.
- **⚠️ Important**: Functional discrepancy that could cause user confusion or require rework during development. Should fix before development.
- **⚠️ UX Improvement**: Usability or design quality issue that deviates from platform conventions or best practices. Should fix before development.
- **💡 Suggestion**: Cosmetic or minor improvement. Can fix anytime.
- **💡 UX Suggestion**: Minor design enhancement that would improve polish. Can fix anytime.

---

## Notes

- Verification source: `local-docs/project-requirements/functional-requirements/fr011-aftercare-recovery-management/prd.md`
- Scope narrowed on 2026-03-25 per user request: this report now covers only FR-011 patient-mobile screens and excludes `FR-010` / `P05.*` relationship checks.
- Only `layout-temp/aftercare/` files are considered in scope for this narrowed FR-011 mobile-only pass.
- Recheck applied on 2026-03-25: shared tabbed interfaces were treated as a common shell, so fields already satisfied by the shell are not expected to repeat on every tab.
- Shared payment-method dependency acknowledged on 2026-03-25: `FR011 Screen 7` reuses the already-verified `P03.1` payment-method add/edit screens for card and billing capture, so those fields are no longer treated as missing from the checkout layouts themselves.
