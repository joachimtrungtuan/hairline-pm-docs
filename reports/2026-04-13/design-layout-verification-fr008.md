# Design Layout Verification Report — FR-008

**Report Date**: 2026-04-13
**Report Type**: Design Layout Verification
**FR Scope**: FR-008 - Travel & Logistics Coordination
**Flow Scope**: Full provider scope (Main Flow 1 + Main Flow 2, Provider Platform only)
**Layout Source**: `layout-temp/`
**Platform**: Provider Web
**Status**: Complete — provider scope verified with one blocked flow

---

## Summary Dashboard

| # | Flow | Module | Screens Required | Screens Verified | Layout Status | Field Coverage |
|---|------|--------|-----------------|-----------------|---------------|----------------|
| MF1 | Provider-Included Travel | A-04: Travel Management / Provider Platform | 4 | 4 | 🟡 PARTIAL | ~95% |
| MF2 | Patient Self-Booked Travel | A-04: Travel Management / Provider Platform | 2 | 2 | 🔴 BLOCKED | ~60% |

**Overall**: 2 of 2 provider flows verified. Main Flow 1 is mostly covered but still off-spec around action/state handling; Main Flow 2 is blocked because the submitted flight-detail screen is not actually designed and the hotel-detail state contains field-binding errors.
**Screens**: 6 of 6 provider screens were reviewed against current layouts (~83% aggregate field coverage across the scoped screens).

---

## Layout File Inventory

### Mapped to Spec Flows

| Layout File | Maps to Flow | Maps to Screen |
|-------------|-------------|----------------|
| `layout-temp/Provider-Included Travel/Waiting passport.jpg` | MF1 | Screen 6 (Travel Section — Booking/Quote Detail Screen), Path A awaiting-passport state |
| `layout-temp/Provider-Included Travel/Already had passport.jpg` | MF1 | Screen 6 + Screen 7 combined (Travel Section with passport-submitted state + Passport View) |
| `layout-temp/Provider-Included Travel/Flight details.jpg` | MF1 | Screen 6 post-submission review variant with outbound-flight detail tab |
| `layout-temp/Provider-Included Travel/Hotel details.jpg` | MF1 | Screen 6 post-submission review variant with hotel-detail tab |
| `layout-temp/Flight information (First time).jpg` | MF1 | Screen 8 (Flight Information — Provider Entry), blank/default state |
| `layout-temp/Flight information (First time)Typing.jpg` | MF1 | Screen 8 (Flight Information — Provider Entry), typing/populated state |
| `layout-temp/Hotel information (First time).jpg` | MF1 | Screen 9 (Hotel Information — Provider Entry), blank/default state |
| `layout-temp/Hotel information (First time) Typing.jpg` | MF1 | Screen 9 (Hotel Information — Provider Entry), typing/populated state |
| `layout-temp/Patient Self-Booked Travel/Awaiting patient’s hotel & flight details.jpg` | MF2 | Screen 6 (Travel Section — Booking/Quote Detail Screen), Path B awaiting state |
| `layout-temp/Patient Self-Booked Travel/Flight details.jpg` | MF2 | Screen 10 (Travel Details — Provider, Path B), outbound-flight detail state |
| `layout-temp/Patient Self-Booked Travel/Hotel details.jpg` | MF2 | Screen 10 (Travel Details — Provider, Path B), hotel-detail state |

### Unmapped Files

| Layout File | Likely Purpose | Notes |
|-------------|---------------|-------|
| `layout-temp/Confirmed.jpg` | Confirmed appointments list view | Context screen outside FR-008 provider travel section scope; appears to be FR-006 booking list entry point |
| `layout-temp/Confirmed Filter.jpg` | Confirmed appointments list filter drawer | Context/admin list support outside FR-008 provider travel section scope |
| `layout-temp/Fulltable overview.jpg` | Table overview / data inventory | Context artifact, not a provider travel screen in FR-008 |

---

## Detailed Verification by Flow

---

### Flow MF1: Provider-Included Travel

**Status**: 🟡 PARTIAL — all required Path A screens exist, but Screen 6 conflates tracker/detail states and post-submission review still exposes edit behavior that contradicts the lock rules.
**Screens required**: 4
**Layout files**: `layout-temp/Provider-Included Travel/Waiting passport.jpg`, `layout-temp/Provider-Included Travel/Already had passport.jpg`, `layout-temp/Provider-Included Travel/Flight details.jpg`, `layout-temp/Provider-Included Travel/Hotel details.jpg`, `layout-temp/Flight information (First time).jpg`, `layout-temp/Flight information (First time)Typing.jpg`, `layout-temp/Hotel information (First time).jpg`, `layout-temp/Hotel information (First time) Typing.jpg`

#### Screen 6: Travel Section — Booking/Quote Detail Screen (Provider)

**Layout**: `layout-temp/Provider-Included Travel/Waiting passport.jpg`, `layout-temp/Provider-Included Travel/Already had passport.jpg`, `layout-temp/Provider-Included Travel/Flight details.jpg`, `layout-temp/Provider-Included Travel/Hotel details.jpg`

##### Flow Context

- **User arrives from**: Provider opens a confirmed booking after the system has requested passport details from the patient. Flow evidence: Main Flow 1 steps A6-A8 in `prd.md:107-113`.
- **Screen purpose**: Surface the Path A travel tracker inside the booking detail screen so the provider can see travel path, passport/flight/hotel statuses, and move to the next required travel action. Spec evidence: `prd.md:412-435`.
- **Entry point**: Present. All supplied Path A variants stay inside the confirmed booking/quote detail context and keep the `Travel` tab active.
- **Exit path**: Present but partially off-spec. The submitted-passport state exposes `Enter Hotel` and `Enter Flight`, while later review variants expose `Edit Hotel details` / `Edit Outbound Flight Details` instead of staying read-only after submission.
- **Data continuity**: Correct. Booking ID, treatment card, appointment/date/time/location summary, and timeline remain visible across all Path A variants.
- **Flow context issues**: The design merges Screen 6 and Screen 7 in the submitted-passport state instead of using a separate `View Passport` action, and the post-submission detail variants imply provider editing is still allowed after records should be locked.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Travel Path | Yes | ✅ | `Provider-included` badge is visible in `layout-temp/Provider-Included Travel/Waiting passport.jpg` and `layout-temp/Provider-Included Travel/Already had passport.jpg`, matching `prd.md:420`. |
| Passport Status | Yes (Path A only) | ✅ | `Awaiting` is visible in `Waiting passport.jpg`, and `Submitted by John at 11:11, June 26, 2025` is visible in later Path A states. This satisfies the required passport-status tracker in `prd.md:421`, though the submitted state adds timestamp metadata. |
| Outbound Flight Status | Yes | ✅ | `Awaiting` appears in `Waiting passport.jpg`, and `Submitted` appears in the post-submission review variants, matching `prd.md:422`. |
| Return Flight Status | Yes | ✅ | `Awaiting` appears in `Waiting passport.jpg`, and `Submitted` appears in the post-submission review variants, matching `prd.md:423`. |
| Hotel Status | Yes | ✅ | `Awaiting` appears in `Waiting passport.jpg`, and `Submitted` appears in the post-submission review variants, matching `prd.md:424`. |
| Actions | Yes | ❌⚠️ | `Enter Hotel` and `Enter Flight` are visible in `Already had passport.jpg`, but the design never shows the required `View Passport` action from `prd.md:425`, and the review variants replace locked-state viewing with `Edit ... details`, which contradicts the lock rules in `prd.md:495` and `prd.md:529`. |

**Extra Elements**:

- The submitted-passport state renders the full passport card inline instead of requiring a dedicated `View Passport` step.
- The post-submission review variants add a `Hotel & flight` tab set with `Edit ... details` actions that are not defined in FR-008.

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 5/6 (83%)
**Critical Issues**: Action behavior drifts from the PRD once records are submitted; the review variants imply provider edits are still possible after lock.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Severity | Observation | Recommendation | Evidence |
|---------|----------|-------------|----------------|----------|
| U-17 | ⚠️ UX Improvement | The Path A section mixes `Enter ...` and `Edit ... details` actions across states, so the provider cannot tell whether they are entering a first record or modifying a locked one. | Keep Screen 6 CTAs aligned to the PRD action model and remove edit wording from locked review states. | `layout-temp/Provider-Included Travel/Already had passport.jpg`, `layout-temp/Provider-Included Travel/Flight details.jpg`, `layout-temp/Provider-Included Travel/Hotel details.jpg` |
| W-07 | 💡 UX Suggestion | Primary travel actions move around between variants: no CTA in the awaiting state, bottom-right buttons in the submitted-passport state, then text-style edit actions inside the detail tabs. | Standardize travel actions to a single placement within the Screen 6 tracker card. | Same three Path A booking-detail variants |

#### Screen 7: Passport View — Provider

**Layout**: `layout-temp/Provider-Included Travel/Already had passport.jpg`

##### Flow Context

- **User arrives from**: Provider selects the passport-review step after the patient submits passport details. Flow evidence: Main Flow 1 step A7 and Screen 6 navigation rule in `prd.md:108` and `prd.md:435`.
- **Screen purpose**: Let the provider view the submitted passport in full so they can complete the external booking. Spec evidence: `prd.md:441-463`.
- **Entry point**: Present. `Already had passport.jpg` keeps the provider inside the confirmed booking context and opens the passport-detail block with all required fields.
- **Exit path**: Present. `Enter Hotel` and `Enter Flight` actions allow the provider to continue into the downstream travel-entry forms after reviewing the passport.
- **Data continuity**: Correct. The same booking header, appointment summary, and confirmed timeline remain visible while the passport detail card is shown.
- **Flow context issues**: The passport view is embedded rather than isolated as a separate destination, but it still fulfills the review step.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Full Name | Yes | ✅ | `Obama Michelle` is visible in `layout-temp/Provider-Included Travel/Already had passport.jpg`, matching `prd.md:447`. |
| Passport Number | Yes | ✅ | Full passport number is visible in `Already had passport.jpg`, matching assigned-provider visibility in `prd.md:448` and `prd.md:459`. |
| Date of Birth | Yes | ✅ | `29 Jan 1992` is visible, matching `prd.md:449`. |
| Gender | Yes | ✅ | `Female` is visible, matching `prd.md:450`. |
| Location (Nationality) | Yes | ✅ | `Turkey` is visible, matching `prd.md:451`. |
| Place of Birth | Yes | ✅ | `Turkey` is visible, matching `prd.md:452`. |
| Date of Issue | Yes | ✅ | `12 Feb 2018` is visible, matching `prd.md:453`. |
| Date of Expiry | Yes | ✅ | `12 Feb 2028` is visible, matching `prd.md:454`. |
| Passport Photo | Yes | ✅ | A full passport image is displayed at the top of the passport block, matching `prd.md:455`. |

**Extra Elements**:

- `Enter Hotel` and `Enter Flight` buttons appear beneath the passport details. These are useful shortcuts, but they are Screen 6 navigation affordances rather than Screen 7 fields.

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 9/9 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Severity | Observation | Recommendation | Evidence |
|---------|----------|-------------|----------------|----------|
| None | — | No reportable static-layout UX/UI issues. | — | `layout-temp/Provider-Included Travel/Already had passport.jpg` |

#### Screen 8: Flight Information — Provider Entry (Path A)

**Layout**: `layout-temp/Flight information (First time).jpg`, `layout-temp/Flight information (First time)Typing.jpg`

##### Flow Context

- **User arrives from**: Provider reaches this form from Screen 6 after reviewing the passport and completing the external flight booking. Flow evidence: Main Flow 1 steps A7-A11 in `prd.md:108-114` and Screen 6 navigation rule in `prd.md:435`.
- **Screen purpose**: Capture outbound and return flight records for a Path A appointment. Spec evidence: `prd.md:466-500`.
- **Entry point**: Present. The layouts are clearly labeled `Flight information` and include `Outbound Flight` / `Return Flight` tabs, matching the two-leg structure in `prd.md:474` and `prd.md:491-499`.
- **Exit path**: Present. Both variants include a bottom-right `Save flight details` CTA.
- **Data continuity**: Correct. Breadcrumbs retain confirmed-booking context while the provider works inside a dedicated flight-entry screen.
- **Flow context issues**: The typing variant introduces a `Total Price` field even though `prd.md:494` explicitly excludes `total_price` from this form.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Leg Type | Yes | ✅ | `Outbound Flight` and `Return Flight` tabs are visible in both layouts, satisfying `prd.md:474` and `prd.md:491-499`. |
| Airline Name | Yes | ✅ | `Airline Name` input is visible in both layouts, matching `prd.md:475`. |
| Flight Number | Yes | ✅ | `Flight Number` input is visible in both layouts, matching `prd.md:476`. |
| Departure Airport | Yes | ✅ | `Departure Airport` input is visible in both layouts, matching `prd.md:477`. |
| Arrival Airport | Yes | ✅ | `Arrival Airport` input is visible in both layouts, matching `prd.md:478`. |
| Departure Date | Yes | ✅ | `Departure Date` picker is visible in both layouts, matching `prd.md:479`. |
| Departure Time | Yes | ✅ | `Departure Time` selector is visible in both layouts, matching `prd.md:480`. |
| Arrival Date | Yes | ✅ | `Arrival date` picker is visible in both layouts, matching `prd.md:481`. |
| Arrival Time | Yes | ✅ | `Arrival time` selector is visible in both layouts, matching `prd.md:482`. |
| Ticket Confirmation Number | Yes | ✅ | `Ticket Confirmation Number` input is visible in both layouts, matching `prd.md:483`. |
| Ticket Class | Yes | ✅ | `Ticket Class` select is visible in both layouts, matching `prd.md:484`. |
| Baggage Allowance | No | ✅ | Optional `Baggage Allowance` input is visible in both layouts, matching `prd.md:485`. |
| Special Requests | No | ✅ | Optional `Special Requests` input is visible in both layouts, matching `prd.md:486`. |

**Extra Elements**:

- `Total Price` appears in `layout-temp/Flight information (First time)Typing.jpg`, contradicting the exclusion rule in `prd.md:494`.

**Screen Status**: 🟢 GOOD
**Field Coverage**: 13/13 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Severity | Observation | Recommendation | Evidence |
|---------|----------|-------------|----------------|----------|
| None | — | No reportable static-layout UX/UI issues. | — | `layout-temp/Flight information (First time).jpg`, `layout-temp/Flight information (First time)Typing.jpg` |

#### Screen 9: Hotel Information — Provider Entry (Path A)

**Layout**: `layout-temp/Hotel information (First time).jpg`, `layout-temp/Hotel information (First time) Typing.jpg`

##### Flow Context

- **User arrives from**: Provider reaches this form from Screen 6 once hotel booking details are ready, after or independently from the flight-entry step. Flow evidence: Main Flow 1 steps A12-A14 in `prd.md:113-116` and Screen 6 navigation rule in `prd.md:435`.
- **Screen purpose**: Capture the provider-booked hotel record and related transport notes for the patient. Spec evidence: `prd.md:503-530`.
- **Entry point**: Present. The layout is clearly labeled `Hotel information` and shows all expected hotel form fields.
- **Exit path**: Present. A bottom-right `Save hotel details` CTA is visible in both hotel layouts.
- **Data continuity**: Correct. Breadcrumbs retain confirmed-booking context while the provider enters hotel information.
- **Flow context issues**: None material in the current layouts.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Hotel Name | Yes | ✅ | `Hotel Name` input is visible in both hotel layouts, matching `prd.md:511`. |
| Hotel Address | Yes | ✅ | `Hotel Address` input is visible in both hotel layouts, matching `prd.md:512`. |
| Check-In Date | Yes | ✅ | `Check-In Date` picker is visible in both hotel layouts, matching `prd.md:513`. |
| Check-In Time | Yes | ✅ | `Check-In Time` selector is visible in both hotel layouts, matching `prd.md:514`. |
| Check-Out Date | Yes | ✅ | `Check-Out date` field is visible in both hotel layouts, matching `prd.md:515`. |
| Check-Out Time | Yes | ✅ | `Check-Out time` selector is visible in both hotel layouts, matching `prd.md:516`. |
| Reservation Number | Yes | ✅ | `Reservation Number` input is visible in both hotel layouts, matching `prd.md:517`. |
| Room Type | Yes | ✅ | `Room Type` selector is visible in both hotel layouts, matching `prd.md:518`. |
| Amenities Included | No | ✅ | Optional `Amenities Included` input is visible in both hotel layouts, matching `prd.md:519`. |
| Transportation Details | No | ✅ | Optional `Transportation Details` input is visible in both hotel layouts, matching `prd.md:520`. |
| Special Requests | No | ✅ | Optional `Special Requests` input is visible in both hotel layouts, matching `prd.md:521`. |
| Phone Number | No | ✅ | Optional `Phone number` input is visible in both hotel layouts, matching `prd.md:522`. |
| Email | No | ✅ | Optional `Email` input is visible in both hotel layouts, matching `prd.md:523`. |

**Extra Elements**:

- None.

**Screen Status**: 🟢 COMPLETE
**Field Coverage**: 13/13 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Severity | Observation | Recommendation | Evidence |
|---------|----------|-------------|----------------|----------|
| None | — | No reportable static-layout UX/UI issues. | — | `layout-temp/Hotel information (First time).jpg`, `layout-temp/Hotel information (First time) Typing.jpg` |

**Flow Coverage Gaps**:

- No dedicated Path A review state shows the submitted passport plus submitted travel details without exposing edit behavior.
- The combined booking-detail variants blur the intended boundary between Screen 6 and Screen 7; either the design should split them or the spec should be updated deliberately.
- `Total Price` appears in one Screen 8 variant even though the PRD explicitly excludes it from the provider flight-entry form.

---

### Flow MF2: Patient Self-Booked Travel

**Status**: 🔴 BLOCKED — the flow has an awaiting-state tracker, but the submitted detail coverage is incomplete and one of the provided review states is a duplicated hotel-detail layout instead of a flight-detail view.
**Screens required**: 2
**Layout files**: `layout-temp/Patient Self-Booked Travel/Awaiting patient’s hotel & flight details.jpg`, `layout-temp/Patient Self-Booked Travel/Flight details.jpg`, `layout-temp/Patient Self-Booked Travel/Hotel details.jpg`

#### Screen 6: Travel Section — Booking/Quote Detail Screen (Provider)

**Layout**: `layout-temp/Patient Self-Booked Travel/Awaiting patient’s hotel & flight details.jpg`

##### Flow Context

- **User arrives from**: Provider opens a confirmed Path B booking after the system prompts the patient to submit travel details. Flow evidence: Main Flow 2 steps B9-B10 in `prd.md:160-161` and Screen 6 rules in `prd.md:429-435`.
- **Screen purpose**: Surface the Path B travel tracker in booking context and give the provider access to the read-only details view. Spec evidence: `prd.md:412-435`.
- **Entry point**: Present. `Awaiting patient’s hotel & flight details.jpg` keeps the provider on the confirmed booking detail page with the `Travel` tab active.
- **Exit path**: Missing. The screen does not show the required `View Travel Details` action from `prd.md:425` and `prd.md:432-435`; it only lists status badges.
- **Data continuity**: Correct. Booking header, treatment card, appointment summary, and timeline remain in place.
- **Flow context issues**: The provider has no explicit CTA to move from the tracker to the detail view, even though Screen 10 is supposed to be reachable from this screen.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Travel Path | Yes | ✅ | `Patient self-booked` badge is visible in `layout-temp/Patient Self-Booked Travel/Awaiting patient’s hotel & flight details.jpg`, matching `prd.md:420` for Path B. |
| Passport Status | No (hidden for Path B) | ✅ | Passport status is correctly absent in the Path B awaiting state, matching `prd.md:421`. |
| Outbound Flight Status | Yes | ✅ | `Awaiting` badge is visible, matching `prd.md:422`. |
| Return Flight Status | Yes | ✅ | `Awaiting` badge is visible, matching `prd.md:423`. |
| Hotel Status | Yes | ✅ | `Awaiting` badge is visible, matching `prd.md:424`. |
| Actions | Yes | ❌ | The required `View Travel Details` action is not visible anywhere in the awaiting-state layout, despite being required for Path B in `prd.md:425` and `prd.md:432-435`. |

**Extra Elements**:

- None.

**Screen Status**: 🟡 PARTIAL
**Field Coverage**: 5/6 (83%)
**Critical Issues**: Missing `View Travel Details` action leaves the provider without an explicit, spec-backed path to the read-only detail view.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Severity | Observation | Recommendation | Evidence |
|---------|----------|-------------|----------------|----------|
| U-17 | ⚠️ UX Improvement | The awaiting-state tracker has no explicit action that tells the provider how to open the underlying detail view once records are ready. | Add the required `View Travel Details` CTA or a clearly interactive status-row affordance. | `layout-temp/Patient Self-Booked Travel/Awaiting patient’s hotel & flight details.jpg` |

#### Screen 10: Travel Details — Booking/Quote Detail Screen (Provider, Path B)

**Layout**: `layout-temp/Patient Self-Booked Travel/Flight details.jpg`, `layout-temp/Patient Self-Booked Travel/Hotel details.jpg`

##### Flow Context

- **User arrives from**: Provider opens the Path B read-only travel details after viewing the tracker on Screen 6. Flow evidence: Main Flow 2 steps B9-B11 in `prd.md:160-162` and Screen 10 definition in `prd.md:532-587`.
- **Screen purpose**: Show patient-submitted flight and hotel records inline within the booking context, entirely read-only and without any passport section. Spec evidence: `prd.md:534-587`.
- **Entry point**: Partially present. The submitted-state layouts remain in booking context and add a `Hotel & flight` section with tabs, but there is no separate evidence-backed entry affordance from Screen 6.
- **Exit path**: Present at booking-page level only; no secondary CTA is needed because the screen is read-only.
- **Data continuity**: Partial. The top travel-status card carries travel path plus `Submitted by John at 11:11, June 26, 2025` audit text for outbound, return, and hotel, but the actual detail asset coverage is incomplete.
- **Flow context issues**: Both provided submitted-state assets resolve to the hotel-detail tab. There is no distinct outbound-flight detail layout, and the active hotel-detail state also swaps check-in/check-out date/time content.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Flight Details - Outbound | Yes | ❌⚠️ | `layout-temp/Patient Self-Booked Travel/Flight details.jpg` is visually identical to the hotel-detail asset and still shows the `Hotel details` tab active with hotel fields, so the outbound-flight subsection required by `prd.md:538-557` is not actually designed. |
| Flight Details - Return | Conditional | ❌ | The status tracker above shows return flight as `Submitted`, so the condition is met, but there is no distinct return-flight detail state and no inline `Return flight not yet submitted` message. Spec: `prd.md:557`. |
| Hotel Details | Yes | ❌⚠️ | The hotel-detail state contains most required fields, but `Check-in Time` shows a date and `Check-Out date` shows a time, so the hotel subsection is present but misbound against `prd.md:563-577`. |
| Submitted By | Yes | ✅ | The status card above the detail section shows `Submitted by John at 11:11, June 26, 2025` for outbound, return, and hotel, covering the submission metadata requirement in `prd.md:554` and `prd.md:576`. |
| Status | Yes | ✅ | `Submitted` badges are visible for outbound, return, and hotel in the submitted-state layouts, matching `prd.md:555` and `prd.md:577`. |

**Extra Elements**:

- Both submitted-state files resolve to the same hotel-detail presentation; there is no evidence-backed distinct outbound-flight detail asset.

**Screen Status**: 🔴 FAIL
**Field Coverage**: 2/5 (40%)
**Critical Issues**: Outbound and return flight details are not actually designed, and the only submitted hotel-detail state contains field/value binding errors.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Severity | Observation | Recommendation | Evidence |
|---------|----------|-------------|----------------|----------|
| U-11 | ⚠️ UX Improvement | The hotel-detail labels do not match their displayed values: `Check-in Time` shows `December 26, 2023`, while `Check-Out date` shows `2:00 PM (local time)`. | Correct the field/value bindings so each label presents data in the expected format. | `layout-temp/Patient Self-Booked Travel/Hotel details.jpg` |
| U-23 | ⚠️ UX Improvement | The file named `Flight details.jpg` resolves to the same hotel-detail view as the hotel asset, so the tab/state naming is inconsistent with the actual screen content. | Provide distinct submitted-state assets for hotel, outbound flight, and return flight, each with matching active-tab state and content. | `layout-temp/Patient Self-Booked Travel/Flight details.jpg` vs `layout-temp/Patient Self-Booked Travel/Hotel details.jpg` |

**Flow Coverage Gaps**:

- No distinct submitted-state layout exists for outbound-flight details in Path B.
- No distinct submitted-state layout exists for return-flight details in Path B even though the status tracker marks return flight as submitted.
- The current hotel-detail state must correct the date/time field bindings before implementation.

---

## Action Items

| Priority | Flow | Screen | Issue | Recommendation |
|----------|------|--------|-------|----------------|
| 🔴 Critical | MF2 | Screen 10 | Path B submitted flight-details screen is missing; the `Flight details.jpg` asset duplicates the hotel-detail state instead of showing outbound flight content. | Design dedicated outbound-flight and return-flight submitted-state views with the correct active tabs and field content. |
| 🔴 Critical | MF2 | Screen 10 | Hotel-detail submitted state misbinds date/time fields (`Check-in Time` shows a date; `Check-Out date` shows a time). | Correct the data bindings so all hotel labels display the correct value types. |
| ⚠️ Important | MF2 | Screen 6 | Path B tracker lacks the required `View Travel Details` action. | Add the explicit read-only detail CTA on Screen 6. |
| ⚠️ Important | MF1 | Screen 6 | Post-submission Path A review variants expose `Edit ... details`, conflicting with the PRD lock rules after submission. | Remove edit actions from submitted states or make the state clearly admin-only if the behavior is intentional. |
| ⚠️ Important | MF1 | Screen 8 | `Total Price` appears in one provider flight-entry variant even though FR-008 excludes it from this form. | Remove the extra field or move price capture to the owning quote/package flow. |
| 💡 Suggestion | MF1 | Screen 6 / Screen 7 | Passport review is merged inline into Screen 6 instead of flowing through a dedicated `View Passport` action. | Either split the screens to match the PRD or formally update the spec to document the merged pattern. |

### Priority Legend

- **🔴 Critical**: Blocks flow progression, breaks data integrity, or causes security/legal risk. Must fix before development.
- **🔴 Critical UX**: Severe usability issue that would prevent users from completing the flow or cause significant confusion. Must fix before development.
- **⚠️ Important**: Functional discrepancy that could cause user confusion or require rework during development. Should fix before development.
- **⚠️ UX Improvement**: Usability or design quality issue that deviates from platform conventions or best practices. Should fix before development.
- **💡 Suggestion**: Cosmetic or minor improvement. Can fix anytime.
- **💡 UX Suggestion**: Minor design enhancement that would improve polish. Can fix anytime.

---

## Notes

- Requirement source: `local-docs/project-requirements/functional-requirements/fr008-travel-booking-integration/prd.md`
- Review restricted to provider-platform scope only (Screen 6, Screen 7, Screen 8, Screen 9, Screen 10)
- Unmapped `Confirmed*` and `Fulltable overview` files were cataloged but excluded from verdicts because they are not FR-008 provider travel screens
- Current provider design direction keeps all travel work inside the confirmed booking detail screen, which aligns with FR-008’s “no standalone dashboard” rule, but some state transitions and screen boundaries still need cleanup.
