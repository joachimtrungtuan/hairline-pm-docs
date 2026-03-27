# Design Layout Verification Report — P04.1, P04.2

**Report Date**: 2026-03-24
**Report Type**: Design Layout Verification
**FR Scope**: FR-008 — Travel & Logistics Coordination
**Flow Scope**: P04.1 Passport Submission (Path A), P04.2 Flight & Hotel Submission (Path B)
**Layout Source**: `layout-temp/`
**Platform**: Patient Mobile App
**Status**: 🔴 BLOCKED

---

## Summary Dashboard

| # | Flow | Module | Screens Required | Screens Verified | Layout Status | Field Coverage |
|---|------|--------|-----------------|-----------------|---------------|----------------|
| P04.1 | Passport Submission (Path A) | P-04: Travel & Logistics | 2 | 2 | 🔴 BLOCKED | ~100% |
| P04.2 | Flight & Hotel Submission (Path B) | P-04: Travel & Logistics | 5 | 5 | 🟡 PARTIAL | ~96% |

**Overall**: 2 of 2 flows verified. `P04.1` remains **BLOCKED**, while `P04.2` is now **PARTIAL** after confirming the missing read-only travel-record layouts.
**Screens**: 7 of 7 specified screens have mapped layouts (100% layout coverage).

---

## Layout File Inventory

### Mapped to Spec Flows

| Layout File | Maps to Flow | Maps to Screen |
|-------------|-------------|----------------|
| `layout-temp/P04.1-S1_ Passport Submission Form.jpg` | P04.1 | P04.1-S1 (Passport Submission Form) |
| `layout-temp/P04.1-S1_ Passport Submission Form - Error State.jpg` | P04.1 | P04.1-S1 (Passport Submission Form, error state) |
| `layout-temp/P04.1-S1_ Passport Submission Form - Upload passport successfully.jpg` | P04.1 | P04.1-S1 (Passport Submission Form, upload success state) |
| `layout-temp/P04.1-S2_ Passport Details — Submitted/Read-Only View.jpg` | P04.1 | P04.1-S2 (Passport Details — Submitted / Read-Only View) |
| `layout-temp/P04.2-S1_ Travel Requirement Check.jpg` | P04.2 | P04.2-S1 (Travel Requirement Check) |
| `layout-temp/P04.2-S2_ Flight Information — Patient Submission.jpg` | P04.2 | P04.2-S2 (Flight Information — Patient Submission) |
| `layout-temp/P04.2-S2_ Flight Information — Patient Submission - Error.jpg` | P04.2 | P04.2-S2 (Flight Information — Patient Submission, error state) |
| `layout-temp/P04.2-S3_ Hotel Information — Patient Submission.jpg` | P04.2 | P04.2-S3 (Hotel Information — Patient Submission) |
| `layout-temp/P04.2-S3_ Hotel Information — Patient Submission - Error.jpg` | P04.2 | P04.2-S3 (Hotel Information — Patient Submission, error state) |
| `layout-temp/Flight Information.jpg` | P04.2 | P04.2-S4 (Submitted Travel Record — Read-Only View, flight variant) |
| `layout-temp/Hotel Information.jpg` | P04.2 | P04.2-S4 (Submitted Travel Record — Read-Only View, hotel variant) |
| `layout-temp/P04.2-S5_ Travel Itinerary View — Patient - Travel Required.jpg` | P04.2 | P04.2-S5 (Travel Itinerary View — Patient, travel required state) |
| `layout-temp/P04.2-S5_ Travel Itinerary View — Patient - No Travel Required.jpg` | P04.2 | P04.2-S5 (Travel Itinerary View — Patient, no travel required state) |

### Unmapped Files

| Layout File | Likely Purpose | Notes |
|-------------|---------------|-------|
| None | — | All in-scope files are now mapped |

---

## Detailed Verification by Flow

---

### Flow P04.1: Passport Submission (Path A)

**Status**: 🔴 BLOCKED — Core layouts exist for both specified screens, but the submitted/read-only screen still violates the spec by exposing the passport image, and the flow set does not evidence the rejected validation paths described in the workflow.
**Screens required**: 2
**Layout files**: `layout-temp/P04.1-S1_ Passport Submission Form.jpg`, `layout-temp/P04.1-S1_ Passport Submission Form - Error State.jpg`, `layout-temp/P04.1-S1_ Passport Submission Form - Upload passport successfully.jpg`, `layout-temp/P04.1-S2_ Passport Details — Submitted/Read-Only View.jpg`

#### Screen P04.1-S1: Passport Submission Form

**Layout**: `layout-temp/P04.1-S1_ Passport Submission Form.jpg`, `layout-temp/P04.1-S1_ Passport Submission Form - Error State.jpg`, `layout-temp/P04.1-S1_ Passport Submission Form - Upload passport successfully.jpg`

##### Flow Context

- **User arrives from**: Automated passport request after a confirmed booking with provider-included travel, opened via notification or `Booking Detail → Travel`.
- **Screen purpose**: Capture passport photo plus manually entered passport details before provider travel booking proceeds.
- **Entry point**: Present. The layout shows booking context and an initial `Awaiting` submission state consistent with the flow trigger.
- **Exit path**: Partially present. `Submit Passport Details` and a secondary `Cancel` action are visible, but no discard-unsaved-changes prompt is evidenced.
- **Data continuity**: Correct. Booking reference, treatment type, provider, procedure date, and travel destination are carried into the form.
- **Flow context issues**: The provided layout set does not show the rejected validation branch described in the flow diagram, including field-level errors for invalid inputs, failed photo quality, or expiry-date rejection.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Screen Title | Yes | ✅ | `Passport Details` shown at top of `P04.1-S1_ Passport Submission Form.jpg`. |
| Back Navigation | Yes | ✅ | Back arrow is visible in the top-left. |
| Booking Context Header | Yes | ✅ | Booking reference, treatment type, provider name, procedure date, and travel destination are shown in the booking summary block. |
| Submission Status Badge | Yes | ✅ | `Awaiting` badge is visible to the right of the submission status row. |
| Section: Passport Photo | Yes | ✅ | `Passport Photo` heading and upload subsection are present. |
| Passport Photo Upload | Yes | ✅ | Upload target with add icon is present in the default state. |
| Upload Preview | Conditional | ✅ | The upload-success and error-state variants show a thumbnail preview with `Replace` and `Remove` actions. |
| Upload Guidelines | Yes | ✅ | Instructional copy about uploading a clear passport data page is visible below the upload area. |
| Upload Progress Indicator | Conditional | ⚠️ | No in-progress upload state is evidenced; only empty, uploaded, and submit-error variants are present. |
| Section: Personal Information | Yes | ✅ | `Personal Information` heading is present. |
| Full Name (as on passport) | Yes | ✅ | Text input field is present under the personal-information section. |
| Date of Birth | Yes | ✅ | Date input with calendar affordance is present. |
| Gender | Yes | ✅ | `Pick Gender` selector row is present. |
| Location (Nationality) | Yes | ✅ | `Location` row with `Pick Country` placeholder is present and functionally maps to nationality. |
| Place of Birth | Yes | ✅ | Text input field is present. |
| Section: Passport Information | Yes | ✅ | `Passport Information` heading is present. |
| Passport Number | Yes | ✅ | Text input field is present. |
| Passport Issue Date | Yes | ✅ | Date input with calendar affordance is present. |
| Passport Expiry Date | Yes | ✅ | Date input with calendar affordance is present. |
| Submit Button | Yes | ✅ | Green `Submit Passport Details` primary CTA is visible at the bottom of the form. |
| Error State (Conditional) | Conditional | ✅ | `P04.1-S1_ Passport Submission Form - Error State.jpg` shows the specified connection-failure message with `Retry`. |

**Extra Elements**:

- `Cancel` button appears below the primary CTA even though it is not listed in the field table; it aligns with the flow’s `Back / Cancel` branch.
- Upload preview variant adds `Replace` and `Remove` actions, which are sensible affordances but are not explicitly enumerated in the screen table.

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 21/21 (100%)
**Critical Issues**: None in the provided static layouts, but the layout set does not evidence the field-level rejected-submission path described in the flow.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-19` Error-state clarity: the provided error treatment only shows a generic connection-failure modal, so the recovery path for invalid passport data, failed photo quality, or expiry-date rejection is not visually communicated. Evidence: `layout-temp/P04.1-S1_ Passport Submission Form - Error State.jpg` shows only a global retry modal. | Add explicit inline validation/error variants for invalid fields, failed photo-quality checks, and expiry-date rejection so users can correct the specific problem without guesswork. |

#### Screen P04.1-S2: Passport Details — Submitted / Read-Only View

**Layout**: `layout-temp/P04.1-S2_ Passport Details — Submitted/Read-Only View.jpg`

##### Flow Context

- **User arrives from**: Successful submission from `P04.1-S1`, or reopening an already locked passport record from `Booking Detail → Travel`.
- **Screen purpose**: Confirm that the passport record was submitted and locked, while giving the patient a support path for corrections.
- **Entry point**: Present. Submitted banner, status badge, and submission timestamp clearly indicate a post-submit state.
- **Exit path**: Present. `Contact Support to Request a Correction` and `Back to Booking` actions are both visible.
- **Data continuity**: Partial. The same booking context and entered passport data carry forward, but the screen still surfaces the passport image even though the confirmation view should be text-only.
- **Flow context issues**: The screen incorrectly exposes the passport photo, which the spec says must stay hidden in the confirmation view.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Screen Title | Yes | ✅ | `Passport Details` title is present. |
| Back Navigation | Yes | ✅ | Back arrow is visible in the top-left. |
| Submitted Status Banner | Yes | ✅ | Blue informational banner states that the passport details have been submitted and are locked. |
| Booking Context Header | Yes | ✅ | Booking reference, treatment type, provider name, and procedure date are shown; travel destination is also carried over. |
| Submitted Badge | Yes | ✅ | Green `Submitted` status badge is visible beside the submission status row. |
| Submission Timestamp | Yes | ✅ | Timestamp text `Submitted on June 24, 2026 at 23:30` is shown below the status row. |
| Full Name (Read-Only) | Yes | ✅ | `Jane Doe` is shown as read-only text. |
| Date of Birth (Read-Only) | Yes | ✅ | `25-03-1983` is shown as read-only text. |
| Gender (Read-Only) | Yes | ✅ | `Female` is shown as read-only text. |
| Location / Nationality (Read-Only) | Yes | ✅ | `France` is shown under the `Location` label. |
| Place of Birth (Read-Only) | Yes | ✅ | `Paris` is shown as read-only text. |
| Passport Number (Read-Only, Masked) | Yes | ✅ | The current layout shows the value in masked form, with only the leading digits visible and the remainder obscured by asterisks. |
| Passport Issue Date (Read-Only) | Yes | ✅ | `25-03-2026` is shown as read-only text. |
| Passport Expiry Date (Read-Only) | Yes | ✅ | `25-03-2036` is shown as read-only text. |
| Contact Support Button | Yes | ✅ | `Contact Support to Request a Correction` button is visible. |
| Back to Booking Button | Yes | ✅ | `Back to Booking` secondary action is visible. |

**Extra Elements**:

- Passport photo preview is displayed in the confirmation view, even though the spec explicitly says the confirmation view must not show the passport image.

**Screen Status**: 🔴 FAIL
**Field Coverage**: 16/16 (100%)
**Critical Issues**: The confirmation view still exposes the passport photo despite the spec explicitly forbidding it.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-02` Information priority: the confirmation screen gives a large, above-the-fold area to the passport photo even though the user’s primary need is to confirm status, review submitted text fields, or reach the correction action. Evidence: `layout-temp/P04.1-S2_ Passport Details — Submitted/Read-Only View.jpg` shows the photo block above the main read-only details and CTA stack. | Remove the passport image from the patient confirmation view and keep the status banner, timestamp, submitted fields, and correction CTA as the primary above-the-fold content. |

**Flow Coverage Gaps**:

- No layout file shows the rejected-submission path with field-level validation, failed passport-photo quality handling, or the explicit `Passport expiry date must be in the future` error described in the flow.
- No layout file evidences the `Discard unsaved changes?` confirmation that appears in the back/cancel branch of the flow diagram.

---

### Flow P04.2: Flight & Hotel Submission (Path B)

**Status**: 🟡 PARTIAL — All five screens now have mapped layouts, but the flow still has design/spec gaps around misleading secondary-action semantics, missing validation-state coverage, and invalid hotel sample data in the read-only itinerary/detail views.
**Screens required**: 5
**Layout files**: `layout-temp/P04.2-S1_ Travel Requirement Check.jpg`, `layout-temp/P04.2-S2_ Flight Information — Patient Submission.jpg`, `layout-temp/P04.2-S2_ Flight Information — Patient Submission - Error.jpg`, `layout-temp/P04.2-S3_ Hotel Information — Patient Submission.jpg`, `layout-temp/P04.2-S3_ Hotel Information — Patient Submission - Error.jpg`, `layout-temp/Flight Information.jpg`, `layout-temp/Hotel Information.jpg`, `layout-temp/P04.2-S5_ Travel Itinerary View — Patient - Travel Required.jpg`, `layout-temp/P04.2-S5_ Travel Itinerary View — Patient - No Travel Required.jpg`

#### Screen P04.2-S1: Travel Requirement Check

**Layout**: `layout-temp/P04.2-S1_ Travel Requirement Check.jpg`

##### Flow Context

- **User arrives from**: Automated travel-request notification after a confirmed booking with patient self-booked travel, opened from `Booking Detail → Travel`.
- **Screen purpose**: Let the patient choose between continuing the travel-submission workflow or declaring that no travel is required.
- **Entry point**: Present. The screen opens with appointment context and the required travel question.
- **Exit path**: Present. Both `Yes — I need to arrange travel` and `No — I am local / no travel needed` paths are visible.
- **Data continuity**: Correct for the spec. Clinic name and appointment date are shown in the appointment summary.
- **Flow context issues**: The `No travel needed` choice is styled like a destructive action, which does not match its role as a valid alternative flow.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Appointment Summary | Yes | ✅ | `Clinic Name` and `Appointment Date` are shown in `P04.2-S1_ Travel Requirement Check.jpg`. |
| Prompt Heading | Yes | ✅ | `Do you need to arrange travel for this appointment?` is shown prominently. |
| Option A: Yes | Yes | ✅ | Green primary CTA `Yes — I need to arrange travel` is present. |
| Option B: No | Yes | ❌⚠️ | The secondary `No — I am local / no travel needed` action is styled in red, which conveys a destructive/error meaning instead of a neutral alternative path. |

**Extra Elements**:

- Screen title `Travel Requirement Check` is shown even though it is not listed in the field table.
- Back navigation is present even though the screen table does not explicitly enumerate it.

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 3/4 (75%)
**Critical Issues**: None, but the visual treatment of the `No travel needed` path is misleading.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-14` Semantic color usage: the `No — I am local / no travel needed` action is shown as a red destructive button even though it is a normal branch of the flow, not an error or harmful action. Evidence: `layout-temp/P04.2-S1_ Travel Requirement Check.jpg`. | Restyle the `No travel needed` option as a neutral secondary action so users do not interpret it as a dangerous or irreversible mistake. |

#### Screen P04.2-S2: Flight Information — Patient Submission

**Layout**: `layout-temp/P04.2-S2_ Flight Information — Patient Submission.jpg`, `layout-temp/P04.2-S2_ Flight Information — Patient Submission - Error.jpg`

##### Flow Context

- **User arrives from**: The `Yes` branch from `P04.2-S1`, then reused later for the optional return-flight submission.
- **Screen purpose**: Collect one flight leg’s confirmed travel details and submit them as a locked record.
- **Entry point**: Present for the outbound variant. The screen clearly identifies the outbound leg and shows booking context.
- **Exit path**: Partially present. `Submit` and `Cancel` are visible, but no return-flight variant or discard-unsaved-changes confirmation is evidenced.
- **Data continuity**: Correct. Booking reference, treatment type, provider, procedure date, and destination context are carried into the form.
- **Flow context issues**: Only the outbound-leg variant is provided; the return-leg state that the flow explicitly reuses is not evidenced.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Screen Title | Yes | ✅ | `Outbound Flight` is shown in the provided variant. |
| Back Navigation | Yes | ✅ | Back arrow is visible in the top-left. |
| Booking Context Header | Yes | ✅ | Booking reference, treatment type, provider name, procedure date, and travel destination are shown. |
| Leg Type Indicator | Yes | ✅ | `Outbound` badge is visible beside the `Leg Type` row. |
| Airline Name | Yes | ✅ | Text input field is present. |
| Flight Number | Yes | ✅ | Text input field is present. |
| Departure Airport | Yes | ✅ | Text input field is present. |
| Arrival Airport | Yes | ✅ | Text input field is present. |
| Departure Date | Yes | ✅ | Date input with calendar affordance is present. |
| Departure Time | Yes | ✅ | Time input with clock affordance is present. |
| Arrival Date | Yes | ✅ | Date input with calendar affordance is present. |
| Arrival Time | Yes | ✅ | Time input with clock affordance is present. |
| Ticket Confirmation Number | Yes | ✅ | Text input field is present. |
| Ticket Class | Yes | ✅ | `Pick Class` selector is present. |
| Baggage Allowance | No | ✅ | Optional baggage-allowance field is present. |
| Special Requests | No | ✅ | Optional special-requests field is present. |
| Submit Button | Yes | ⚠️ | Primary CTA is shown only as `Submit`; the spec calls for a leg-specific label such as `Submit Outbound Flight` or `Submit Return Flight`. |
| Cancel Button | Yes | ✅ | Secondary `Cancel` action is present. |
| Provider Visibility Notice | Yes | ✅ | Informational note about provider visibility is shown above the action area. |
| Error State (Conditional) | Conditional | ✅ | `P04.2-S2_ Flight Information — Patient Submission - Error.jpg` shows the specified connection-failure state with `Retry`. |

**Extra Elements**:

- No separate return-flight layout is provided even though this screen is specified to support both `outbound` and `return` states.

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 18/18 (100%)
**Critical Issues**: None in the provided outbound variant, but the return-flight variant is missing from the layout set.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-17` CTA label clarity: the primary button is labeled only `Submit`, which is less explicit than the specified leg-aware action label for a screen reused across outbound and return submissions. Evidence: `layout-temp/P04.2-S2_ Flight Information — Patient Submission.jpg`. | Rename the CTA dynamically to `Submit Outbound Flight` or `Submit Return Flight` so the action remains unambiguous in both variants. |
| ⚠️ UX Improvement | `U-19` Error-state clarity: the provided error state only shows a generic connection-failure modal, so the layout set does not communicate how users recover from invalid date order or other field-level validation failures described in the flow. Evidence: `layout-temp/P04.2-S2_ Flight Information — Patient Submission - Error.jpg`. | Add inline validation/error variants for date-order problems and other field-level failures, not just a generic network retry modal. |

#### Screen P04.2-S3: Hotel Information — Patient Submission

**Layout**: `layout-temp/P04.2-S3_ Hotel Information — Patient Submission.jpg`, `layout-temp/P04.2-S3_ Hotel Information — Patient Submission - Error.jpg`

##### Flow Context

- **User arrives from**: After flight submission in `P04.2-S2`, once the system prompts the patient to submit hotel details.
- **Screen purpose**: Collect confirmed hotel details that will feed the unified itinerary for provider coordination.
- **Entry point**: Present. The layout shows the hotel form with booking context at the top.
- **Exit path**: Partially present. `Submit` and `Cancel` are visible, but no discard-unsaved-changes confirmation or invalid-date validation variant is evidenced.
- **Data continuity**: Correct. The same booking context is carried into the hotel form.
- **Flow context issues**: The provided layout set covers only the default and connection-error states; it does not show the validation branch for invalid check-in/check-out dates.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Screen Title | Yes | ✅ | `Hotel Information` title is present. |
| Back Navigation | Yes | ✅ | Back arrow is visible in the top-left. |
| Booking Context Header | Yes | ✅ | Booking reference, treatment type, provider name, procedure date, and travel destination are shown. |
| Hotel Name | Yes | ✅ | Text input field is present. |
| Hotel Address | Yes | ✅ | Text input field is present. |
| Check-In Date | Yes | ✅ | Date input with calendar affordance is present. |
| Check-In Time | Yes | ✅ | Time input with clock affordance is present. |
| Check-Out Date | Yes | ✅ | Date input with calendar affordance is present. |
| Check-Out Time | Yes | ✅ | Time input with clock affordance is present. |
| Reservation Number | Yes | ✅ | Text input field is present. |
| Room Type | Yes | ✅ | `Pick Room Type` selector is present. |
| Amenities Included | No | ✅ | Optional amenities field is present. |
| Transportation Details | No | ✅ | Optional transportation-details field is present. |
| Special Requests | No | ✅ | Optional special-requests field is present. |
| Phone Number | No | ✅ | Optional phone-number field is present. |
| Email | No | ✅ | Optional email field is present. |
| Submit Button | Yes | ⚠️ | Primary CTA is shown only as `Submit`; the spec calls for `Submit Hotel Details`. |
| Cancel Button | Yes | ✅ | Secondary `Cancel` action is present. |
| Provider Visibility Notice | Yes | ✅ | Informational note about provider visibility is shown above the action area. |
| Error State (Conditional) | Conditional | ✅ | `P04.2-S3_ Hotel Information — Patient Submission - Error.jpg` shows the specified connection-failure state with `Retry`. |

**Extra Elements**:

- No additional layout state is provided for the `check_out_date after check_in_date` validation branch described in the spec.

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 15/15 (100%)
**Critical Issues**: None in the provided default/error layouts, but the invalid-date validation state is not evidenced.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-17` CTA label clarity: the primary action is labeled only `Submit` instead of the more explicit `Submit Hotel Details`. Evidence: `layout-temp/P04.2-S3_ Hotel Information — Patient Submission.jpg`. | Use the full hotel-specific CTA label from the spec so the action is self-descriptive at the bottom of a long form. |
| ⚠️ UX Improvement | `U-19` Error-state clarity: the provided error-state layout only covers a generic connection problem and does not show how the UI explains invalid hotel date sequences to the user. Evidence: `layout-temp/P04.2-S3_ Hotel Information — Patient Submission - Error.jpg`. | Add inline validation variants for `check_out_date after check_in_date` failures rather than relying only on a global retry modal. |

#### Screen P04.2-S4: Submitted Travel Record — Read-Only View

**Layout**: `layout-temp/Flight Information.jpg`, `layout-temp/Hotel Information.jpg`

##### Flow Context

- **User arrives from**: Tapping a submitted outbound flight, return flight, or hotel record from `P04.2-S5`.
- **Screen purpose**: Show the locked, read-only details for an already submitted travel record and offer a correction path through support/admin.
- **Entry point**: Present. Separate read-only layouts are provided for a submitted flight record and a submitted hotel record.
- **Exit path**: Present. Both variants show back navigation plus `Back to Itinerary` and support/correction actions.
- **Data continuity**: Mostly correct. The flight and hotel layouts carry forward the same submitted values shown in the itinerary, but the hotel sample data still shows a check-out date earlier than check-in.
- **Flow context issues**: The screen exists and satisfies the itinerary detail-view transition, but the hotel example data contradicts the booking-date rule and the record-level screen includes a provider-visibility notice that is not part of the read-only spec.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Screen Title | Yes | ✅ | Dynamic titles are present as `Outbound Flight` in `Flight Information.jpg` and `Hotel Information` in `Hotel Information.jpg`; the hotel label is functionally equivalent to the specified `Hotel Details`. |
| Back Navigation | Yes | ✅ | Both variants show the back arrow in the top-left. |
| Locked Status Banner | Yes | ✅ | Both layouts show the info banner explaining that the record is submitted, locked, and requires support for correction. |
| Submitted Badge | Yes | ✅ | Both variants display the green `Submitted` badge in the status row. |
| Submission Timestamp | Yes | ✅ | Both variants show `Submitted on June 24, 2026 at 23:30`. |
| Submitter | Yes | ✅ | Both variants show `Submitted by: John Doe`. |
| All Record Fields (Read-Only) | Yes | ⚠️ | Both variants show the submitted fields in read-only form, but the hotel example data violates the underlying business rule by showing a check-out date earlier than check-in. |
| Contact Support Button | Yes | ✅ | `Contact Support to Request a Correction` is visible in both variants. |
| Back to Itinerary Button | Yes | ✅ | `Back to Itinerary` is visible in both variants. |

**Extra Elements**:

- Both read-only variants include the `These details will be shared with your provider for logistics coordination` notice, which belongs to the submission forms and is not specified for the locked read-only screen.

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 9/9 (100%)
**Critical Issues**: None. The screen exists and covers the required locked-record detail state, though the hotel sample data should still be corrected.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-19` Error/data clarity: the hotel read-only variant displays contradictory stay dates (`Check-In Date 25-07-24`, `Check-Out Date 24-07-24`), which undermines trust in the locked record view. Evidence: `layout-temp/Hotel Information.jpg`. | Correct the hotel example data and ensure the locked-record view only renders values that satisfy the same date-order rules as the submission form. |
| 💡 UX Suggestion | `U-23` Terminology consistency: the hotel record uses `Hotel Information` while the spec names the generic read-only state `Hotel Details`. The meaning is clear, but the naming diverges across the flow. Evidence: `layout-temp/Hotel Information.jpg`. | Standardize the hotel read-only title with the chosen itinerary/detail terminology across `P04.2-S4` and `P04.2-S5`. |

#### Screen P04.2-S5: Travel Itinerary View — Patient

**Layout**: `layout-temp/P04.2-S5_ Travel Itinerary View — Patient - Travel Required.jpg`, `layout-temp/P04.2-S5_ Travel Itinerary View — Patient - No Travel Required.jpg`

##### Flow Context

- **User arrives from**: Either immediately after selecting `No travel needed` on `P04.2-S1`, or after completing hotel submission in `P04.2-S3`.
- **Screen purpose**: Present a unified, read-only itinerary assembled from submitted travel records and pending prompts.
- **Entry point**: Present. Both the no-travel state and populated itinerary state are provided.
- **Exit path**: Partial. Back navigation is visible, the return-flight prompt includes a `Submit Return Flight` CTA, and `P04.2-S4` now exists for locked-record drill-down, but the populated itinerary sections still do not clearly advertise their tap-through behavior.
- **Data continuity**: Partial. Booking context, outbound-flight content, pending-return prompt, and hotel content are shown, but the hotel sample data itself violates the business-rule date order.
- **Flow context issues**: The itinerary depends on a missing read-only detail screen, and the hotel block shows a check-out date earlier than the check-in date.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Screen Title | Yes | ✅ | `Travel Itinerary` title is shown in both provided states. |
| Back Navigation | Yes | ✅ | Back arrow is visible in the no-travel state and implied in the populated state layout set. |
| Booking Context Header | Yes | ✅ | Booking reference, treatment type, provider name, procedure date, and travel destination are shown. |
| No Travel Required Message (Conditional) | Conditional | ✅ | `P04.2-S5_ Travel Itinerary View — Patient - No Travel Required.jpg` shows `No travel required for this appointment.` with no extra itinerary sections. |
| Section: Package Travel Items (Conditional) | Conditional | ✅ | `P04.2-S5_ Travel Itinerary View — Patient - Travel Required.jpg` shows a `Package Travel` section with accommodation and transportation items. |
| Section: Outbound Flight | Conditional | ✅ | Populated outbound-flight details are shown with timestamp and submitter. |
| Section: Return Flight | Conditional | ✅ | The layout uses a `Return Flight` block to hold the pending-return state; no submitted return-record detail is shown because the condition is not met. |
| Outbound Awaiting Prompt (Conditional) | Conditional | ✅ | Not triggered in the provided populated state because outbound details already exist. |
| Return Awaiting Prompt (Conditional) | Conditional | ✅ | `Return flight not yet submitted` plus `Submit Return Flight` CTA are visible. |
| Section: Hotel | Conditional | ❌⚠️ | Hotel details are shown, but the displayed sample data has `Check-In Date` `25-07-24` and `Check-Out Date` `24-07-24`, which violates the `check_out_date after check_in_date` business rule. |
| Hotel Awaiting Prompt (Conditional) | Conditional | ✅ | Not triggered in the provided populated state because hotel details already exist. |
| Submission Timestamps | Yes | ✅ | Timestamp and submitter are shown for outbound flight and hotel sections. |

**Extra Elements**:

- `Flights` grouping label and `Outbound - Economy class` summary chip are present as useful grouping enhancements, though they are not explicitly named in the field table.

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 8/9 (89%)
**Critical Issues**: None at screen-structure level, but the hotel block displays sample data that contradicts the hotel date-order rule.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `mobile-design`

| Severity | Observation | Recommendation |
|----------|-------------|----------------|
| ⚠️ UX Improvement | `U-16` Interactive vs static distinction: the populated outbound-flight and hotel sections read like static text blocks, so the expected tap-through behavior to a read-only detail screen is not visually obvious. Evidence: `layout-temp/P04.2-S5_ Travel Itinerary View — Patient - Travel Required.jpg`. | Add clear affordances such as chevrons, card styling, or explicit `View details` labels on tappable itinerary sections. |
| ⚠️ UX Improvement | `U-19` Error/data clarity: the hotel section displays contradictory stay dates, which undermines trust in the itinerary and makes it harder for users to validate their submitted records. Evidence: `layout-temp/P04.2-S5_ Travel Itinerary View — Patient - Travel Required.jpg` shows `Check-In Date 25-07-24` and `Check-Out Date 24-07-24`. | Correct the hotel example data and validate the rendered itinerary content against the same date-order rules used in the submission form. |

**Flow Coverage Gaps**:

- No return-flight submission variant is provided for `P04.2-S2`; only the outbound state is shown.
- No layout file evidences the field-level validation branches for invalid flight-date or hotel-date sequences, or the discard-unsaved-changes confirmations described in the flow.

---

## Action Items

| Priority | Flow | Screen | Issue | Recommendation |
|----------|------|--------|-------|----------------|
| 🔴 Critical | P04.1 | P04.1-S2 | Passport photo is displayed in the confirmation/read-only screen even though the spec explicitly says the confirmation view must not show the passport image. | Remove the passport photo block from the patient confirmation view and keep only the approved read-only text fields. |
| ⚠️ Important | P04.1 | P04.1-S1 | The flow diagram defines rejected-validation states (field errors, photo-quality failure, expiry-date failure), but the layout set shows only a generic connection-error modal. | Add explicit validation-state layouts for rejected passport submissions and the discard-unsaved-changes branch. |
| ⚠️ Important | P04.2 | P04.2-S2 / P04.2-S3 | Flight and hotel forms only show generic connection-error modals; field-level validation branches and discard-confirmation states are not designed. | Add inline validation/error variants for date-order and required-field failures, plus the discard-unsaved-changes confirmation states. |
| ⚠️ Important | P04.2 | P04.2-S5 | The hotel section in the populated itinerary shows a check-out date earlier than check-in, contradicting the business rule and weakening trust in the rendered itinerary. | Correct the itinerary sample data and validate the rendered hotel block against the same date-order rules as the submission form. |
| ⚠️ Important | P04.2 | P04.2-S4 / P04.2-S5 | The hotel read-only/detail states still show a check-out date earlier than check-in, contradicting the hotel business rule. | Correct the hotel sample data across both the locked record view and itinerary view so rendered examples stay consistent with valid submissions. |
| ⚠️ UX Improvement | P04.2 | P04.2-S1 | The `No travel needed` path is styled as a red/destructive action even though it is a legitimate alternate flow. | Restyle the secondary option as a neutral secondary CTA. |
| ⚠️ UX Improvement | P04.2 | P04.2-S5 | Submitted itinerary sections do not clearly advertise that they should open a read-only detail view. | Add clear tap affordances such as chevrons, card styling, or `View details` labels on tappable sections. |

### Priority Legend

- **🔴 Critical**: Blocks flow progression, breaks data integrity, or causes security/legal risk. Must fix before development.
- **🔴 Critical UX**: Severe usability issue that would prevent users from completing the flow or cause significant confusion. Must fix before development.
- **⚠️ Important**: Functional discrepancy that could cause user confusion or require rework during development. Should fix before development.
- **⚠️ UX Improvement**: Usability or design quality issue that deviates from platform conventions or best practices. Should fix before development.
- **💡 Suggestion**: Cosmetic or minor improvement. Can fix anytime.
- **💡 UX Suggestion**: Minor design enhancement that would improve polish. Can fix anytime.

---

## Notes

- Requirement source: `local-docs/reports/2026-02-05/missing-mobile-flows-design-complement.md`
- Layout files inventoried from `layout-temp/` on 2026-03-24
- `layout-temp/Flight Information.jpg` and `layout-temp/Hotel Information.jpg` were reclassified during follow-up review as the `P04.2-S4` flight and hotel read-only record variants
- User approved both `P04.1` and `P04.2` on 2026-03-24 despite the remaining documented issues; approval status is tracked separately from the technical verification verdicts above
- Review was performed from the provided static images only; behaviors that require interaction (keyboard handling, actual tap targets, runtime loading states) could not be directly exercised
- Primary evidence came from the named `P04.1-*` and `P04.2-*` layout files; unmapped auxiliary exports were not needed to reach the documented verdicts
