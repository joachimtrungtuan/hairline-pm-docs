# Design Layout Verification Report — FR-008

**Report Date**: 2026-04-02
**Report Type**: Design Layout Verification
**FR Scope**: FR-008 - Travel & Logistics Coordination
**Flow Scope**: Specific screens only: Screen 6, Screen 7, Screen 8, Screen 9, Screen 10 (Provider Platform)
**Layout Source**: `layout-temp/`
**Platform**: Provider Web
**Status**: Complete — Critical gaps found

---

## Summary Dashboard

| # | Flow | Module | Screens Required | Screens Verified | Layout Status | Field Coverage |
|---|------|--------|-----------------|-----------------|---------------|----------------|
| MF1 | Provider-Included Travel | PR-04: Provider Platform | 4 | 4 | 🔴 BLOCKED | ~85% |
| MF2 | Patient Self-Booked Travel | PR-04: Provider Platform | 1 | 1 | 🔴 BLOCKED | ~45% |

**Overall**: 2 of 2 flows verified. Both flows are blocked by critical layout gaps.
**Screens**: 5 of 5 specified screens have layouts reviewed (~69% aggregate field coverage across the scoped screens).

---

## Layout File Inventory

### Mapped to Spec Flows

| Layout File | Maps to Flow | Maps to Screen |
|-------------|-------------|----------------|
| `layout-temp/Waiting passport.jpg` | MF1 | Screen 6 (Travel Section — Booking/Quote Detail Screen) |
| `layout-temp/Already had passport.jpg` | MF1 | Screen 7 (Passport View — Provider) |
| `layout-temp/Flight details.jpg` | MF1 | Screen 6 (Travel Section — Booking/Quote Detail Screen, post-submission review variant) |
| `layout-temp/Hotel details.jpg` | MF2 | Screen 10 (Travel Details — Provider, hotel submitted-state variant) |
| `layout-temp/Hotel details copy.jpg` | MF1 | Screen 6 (Travel Section — Booking/Quote Detail Screen, duplicate post-submission review variant) |
| `layout-temp/Flight information (First time).jpg` | MF1 | Screen 8 (Flight Information — Provider Entry) |
| `layout-temp/Flight information (First time)Typing.jpg` | MF1 | Screen 8 (Flight Information — Provider Entry) |
| `layout-temp/Hotel information (First time).jpg` | MF1 | Screen 9 (Hotel Information — Provider Entry) |
| `layout-temp/Hotel information (First time) Typing.jpg` | MF1 | Screen 9 (Hotel Information — Provider Entry) |
| `layout-temp/Awaiting patient’s hotel & flight details.jpg` | MF2 | Screen 10 (Travel Details — Provider, awaiting state) |

### Unmapped Files

| Layout File | Likely Purpose | Notes |
|-------------|---------------|-------|
| None | — | — |

---

## Detailed Verification by Flow

---

### Flow MF1: Provider-Included Travel

**Status**: 🔴 BLOCKED — Screen 6 still lacks the required status-badge tracker, and its post-submission variants introduce off-spec edit/update behavior after provider records are supposed to be locked.
**Screens required**: 4
**Layout files**: `Waiting passport.jpg`, `Already had passport.jpg`, `Flight details.jpg`, `Hotel details copy.jpg`, `Flight information (First time).jpg`, `Flight information (First time)Typing.jpg`, `Hotel information (First time).jpg`, `Hotel information (First time) Typing.jpg`

#### Screen 6: Travel Section — Booking/Quote Detail Screen (Provider)

**Layout**: `layout-temp/Waiting passport.jpg`, `layout-temp/Flight details.jpg`, `layout-temp/Hotel details copy.jpg`

##### Flow Context

- **User arrives from**: Provider opens an already-confirmed booking and navigates to the travel area after the system has requested passport details from the patient. Flow evidence: Main Flow 1 steps A6-A8 in `local-docs/project-requirements/functional-requirements/fr008-travel-booking-integration/prd.md:107-113`.
- **Screen purpose**: Surface the Path A travel tracker inside the booking detail screen so the provider can see travel path, passport/flight/hotel statuses, and jump to the next required action. Spec evidence: Screen 6 purpose and business rules in `local-docs/project-requirements/functional-requirements/fr008-travel-booking-integration/prd.md:412-435`.
- **Entry point**: Present as a provider booking detail page, but the in-scope travel UI is rendered as a custom tab labeled `Book hotel & Book flight` rather than a collapsible `Travel` section. Across the supplied variants, the section jumps between an awaiting-passport state and composite post-submission review panels without ever showing the required tracker row.
- **Exit path**: Present but mismatched. The provider flow exposes `Book hotel`, `Book flight`, `Edit Hotel details`, and `Edit Outbound Flight details` actions in the supplied variants instead of the required Screen 6 action model (`View Passport`, `Enter Flight`, `Enter Hotel`) from `prd.md:425`, `prd.md:435`.
- **Data continuity**: Booking context is preserved via booking ID, treatment card, appointment/date/time/location summary, timeline, and later passport/travel detail panels, but the explicit travel-record statuses that should drive the flow are not surfaced.
- **Flow context issues**: The supplied Path A review variants combine passport and submitted travel details inline, which confirms they belong to the provider-included flow, but the design still bypasses the specified status tracker and allows post-submission editing that contradicts the locking rules in `prd.md:495` and `prd.md:529`.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Travel Path | Yes | ❌⚠️ | The green provider-owned banner (`Hotel and flight details added by the provider`) signals Path A in the submitted-state variants, but Screen 6 requires an explicit `Travel Path` badge per `prd.md:420`. |
| Passport Status | Yes (Path A) | ❌⚠️ | The layouts show either `Awaiting patient's passport details` or the full passport block, but Screen 6 requires a compact `Awaiting / Submitted / Incomplete` badge in the tracker row per `prd.md:421`. |
| Outbound Flight Status | Yes | ❌⚠️ | `layout-temp/Flight details.jpg` exposes an `Outbound Flight` tab with data, but the required `Not included / Awaiting / Submitted` badge is not shown anywhere. Spec: `prd.md:422`. |
| Return Flight Status | Yes | ❌⚠️ | A `Return Flight` tab exists in the Path A review variants, but no explicit return-flight status badge is rendered. Spec: `prd.md:423`. |
| Hotel Status | Yes | ❌⚠️ | `layout-temp/Hotel details copy.jpg` exposes a `Hotel details` tab with data, but the required `Not included / Awaiting / Submitted` badge is not shown anywhere. Spec: `prd.md:424`. |
| Actions | Yes | ❌⚠️ | Path A actions exist, but they are off-spec: `Book hotel` / `Book flight` replace `Enter Hotel` / `Enter Flight`, and post-submission variants expose `Edit ... details` even though the underlying records should be locked after submission (`prd.md:495`, `prd.md:529`). |

**Extra Elements**:

- The post-submission review variants combine passport details plus `Hotel & flight` tabs on the same booking-detail page, which is not a 1:1 screen shape described anywhere in FR-008.
- The review variants explicitly state the provider-entered details `can be updated if needed` and show `Edit ... details` buttons, which conflicts with the locking rules for submitted provider records in `prd.md:495` and `prd.md:529`.

**Screen Status**: 🔴 FAIL
**Field Coverage**: 0/6 (0%)
**Critical Issues**: The required badge-based status tracker is absent, and the post-submission variants suggest provider edits are still allowed after the PRD says submitted flight/hotel records are locked.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Severity | Observation | Recommendation | Evidence |
|---------|----------|-------------|----------------|----------|
| U-02 | 🔴 Critical UX | The most important travel state is never summarized at the top of the section. Providers have to infer progress from an empty passport card or from separate post-submission review tabs instead of scanning one status row. | Move the travel-path and per-record statuses into a top tracker row that is visible before the detail content. | `layout-temp/Waiting passport.jpg`, `layout-temp/Flight details.jpg`, `layout-temp/Hotel details copy.jpg`; Screen 6 tracker requirements in `prd.md:420-424`. |
| U-17 | ⚠️ UX Improvement | The Path A actions use inconsistent intent labels across states (`Book hotel`, `Book flight`, `Edit Hotel details`, `Edit Outbound Flight details`), which obscures whether the provider is booking externally, entering records, or editing locked data. | Standardize the Screen 6 CTA labels to the PRD action model: `View Passport`, `Enter Flight`, `Enter Hotel`; remove edit wording for locked records. | `layout-temp/Already had passport.jpg`, `layout-temp/Flight details.jpg`, `layout-temp/Hotel details copy.jpg`; action labels visible in booking-detail variants. |

#### Screen 7: Passport View — Provider

**Layout**: `layout-temp/Already had passport.jpg`

##### Flow Context

- **User arrives from**: Provider selects `View Passport` from the Screen 6 travel area after the patient has submitted passport information. Flow evidence: Main Flow 1 step A7 plus Screen 6 navigation rule in `prd.md:108`, `prd.md:435`.
- **Screen purpose**: Allow the provider to inspect the submitted passport in full before making the external booking. Spec evidence: `prd.md:441-463`.
- **Entry point**: Present. `layout-temp/Already had passport.jpg` keeps the provider inside the booking context and opens a `Passport details` card populated with image and form data.
- **Exit path**: Present. The layout includes `Book hotel` and `Book flight` buttons that let the provider continue to downstream entry screens after reviewing the passport.
- **Data continuity**: Correct. The same booking header, appointment summary, and confirmed state remain visible while the passport record is shown inline.
- **Flow context issues**: The passport view is embedded into the booking page rather than feeling like a distinct read-only destination, but it still supports the intended review step.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Full Name | Yes | ✅ | `Obama Michelle` is visible in `layout-temp/Already had passport.jpg`, matching Screen 7 `Full Name` display requirement in `prd.md:447`. |
| Passport Number | Yes | ✅ | Full passport number is visible in `layout-temp/Already had passport.jpg`, matching the assigned-provider visibility rule in `prd.md:448`, `prd.md:459`. |
| Date of Birth | Yes | ✅ | `29 Jan 1992` is visible in `layout-temp/Already had passport.jpg`, matching Screen 7 field `Date of Birth` in `prd.md:449`. |
| Gender | Yes | ✅ | `Female` is visible in `layout-temp/Already had passport.jpg`, matching Screen 7 field `Gender` in `prd.md:450`. |
| Location (Nationality) | Yes | ✅ | `Turkey` is visible in `layout-temp/Already had passport.jpg`, matching Screen 7 field `Location` in `prd.md:451`. |
| Place of Birth | Yes | ✅ | `Turkey` is visible in `layout-temp/Already had passport.jpg`, matching Screen 7 field `Place of birth` in `prd.md:452`. |
| Date of Issue | Yes | ✅ | `12 Feb 2018` is visible in `layout-temp/Already had passport.jpg`, matching Screen 7 field `Date of Issue` in `prd.md:453`. |
| Date of Expiry | Yes | ⚠️ | The field is present in `layout-temp/Already had passport.jpg`, but the label reads `Date of expired` instead of `Date of expiry`. This is functionally understandable but not exact. Spec: `prd.md:454`. |
| Passport Photo | Yes | ✅ | A full passport image is displayed at the top of the passport card in `layout-temp/Already had passport.jpg`, matching Screen 7 requirement in `prd.md:455`. |

**Extra Elements**:

- `Book hotel` and `Book flight` buttons appear inside the passport view. These are useful shortcuts, but they are not listed as Screen 7 fields and behave more like Screen 6 navigation affordances.

**Screen Status**: 🟢 GOOD
**Field Coverage**: 9/9 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

No reportable UX/UI issues from applicable static web checks.

#### Screen 8: Flight Information — Provider Entry (Path A)

**Layout**: `layout-temp/Flight information (First time).jpg`, `layout-temp/Flight information (First time)Typing.jpg`

##### Flow Context

- **User arrives from**: Provider reaches this form from the Screen 6 travel area after reviewing the passport and completing the external flight booking. Flow evidence: Main Flow 1 steps A7-A11 in `prd.md:108-114` and Screen 6 navigation rule in `prd.md:435`.
- **Screen purpose**: Capture the outbound and return flight records for a Path A appointment. Spec evidence: `prd.md:468-500`.
- **Entry point**: Present. The layout is clearly labeled `Flight information` and includes `Outbound Flight` / `Return Flight` tabs, which matches the two-leg flow noted in `prd.md:491-500`.
- **Exit path**: Present. A bottom-right submit CTA exists in both variants, allowing the provider to send/store the record.
- **Data continuity**: Correct. Breadcrumbs retain booking context (`Appointments / Confirmed / HP202401 / Flight information`), and the leg-type tabs preserve the Flow 1 outbound/return sequence.
- **Flow context issues**: One variant introduces a `Total Price` input that the PRD explicitly excludes from this screen.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Leg Type | Yes | ✅ | `Outbound Flight` and `Return Flight` tabs are visible in both flight layouts, satisfying the leg-type selector/header requirement in `prd.md:474`, `prd.md:491-493`. |
| Airline Name | Yes | ✅ | The `Airline Name` input is visible in both `Flight information` layouts, matching `prd.md:475`. |
| Flight Number | Yes | ✅ | The `Flight Number` input is visible in both `Flight information` layouts, matching `prd.md:476`. |
| Departure Airport | Yes | ✅ | The `Departure Airport` input is visible in both `Flight information` layouts, matching `prd.md:477`. |
| Arrival Airport | Yes | ✅ | The `Arrival Airport` input is visible in both `Flight information` layouts, matching `prd.md:478`. |
| Departure Date | Yes | ✅ | The `Departure Date` picker is visible in both layouts, matching `prd.md:479`. |
| Departure Time | Yes | ✅ | The `Departure Time` selector is visible in both layouts, matching `prd.md:480`. |
| Arrival Date | Yes | ✅ | The `Arrival date` picker is visible in both layouts, matching `prd.md:481`. |
| Arrival Time | Yes | ✅ | The `Arrival time` selector is visible in both layouts, matching `prd.md:482`. |
| Ticket Confirmation Number | Yes | ✅ | The `Ticket Confirmation Number` input is visible in both layouts, matching `prd.md:483`. |
| Ticket Class | Yes | ✅ | The `Ticket Class` select is visible in both layouts, matching `prd.md:484`. |
| Baggage Allowance | No | ✅ | The optional `Baggage Allowance` input is visible in both layouts, matching `prd.md:485`. |
| Special Requests | No | ✅ | The optional `Special Requests` input is visible in both layouts, matching `prd.md:486`. |

**Extra Elements**:

- `Total Price` appears at the bottom of `layout-temp/Flight information (First time)Typing.jpg`. This contradicts Screen 8's explicit business rule that `total_price` is excluded from the form in `prd.md:494`.

**Screen Status**: 🟢 GOOD
**Field Coverage**: 13/13 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Severity | Observation | Recommendation | Evidence |
|---------|----------|-------------|----------------|----------|
| U-17 | ⚠️ UX Improvement | The submit CTA label `Send information` is generic and does not clearly say whether the provider is saving one leg, both legs, or confirming the flight record. | Rename the CTA to something explicit such as `Save flight details` or `Save outbound flight`. | `layout-temp/Flight information (First time).jpg` and `layout-temp/Flight information (First time)Typing.jpg`; button label visible bottom-right. |

#### Screen 9: Hotel Information — Provider Entry (Path A)

**Layout**: `layout-temp/Hotel information (First time).jpg`, `layout-temp/Hotel information (First time) Typing.jpg`

##### Flow Context

- **User arrives from**: Provider reaches this form from the Path A travel area once hotel booking details are ready, either after or independently from the flight-entry step. Flow evidence: Main Flow 1 steps A12-A14 in `prd.md:113-116` and Screen 6 navigation rule in `prd.md:435`.
- **Screen purpose**: Capture the provider-booked hotel record and related transport notes for the patient. Spec evidence: `prd.md:505-530`.
- **Entry point**: Present. The layout is clearly labeled `Hotel information` and shows a hotel form with transportation and contact fields.
- **Exit path**: Present. A bottom-right submit CTA is visible in both hotel layouts.
- **Data continuity**: Correct. Breadcrumbs retain confirmed-booking context while the provider enters hotel information.
- **Flow context issues**: None beyond copy inconsistencies in helper text.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Hotel Name | Yes | ✅ | The `Hotel Name` input is visible in both hotel layouts; the typing variant populates it, matching `prd.md:511`. |
| Hotel Address | Yes | ✅ | The `Hotel Address` input is visible in both hotel layouts; the typing variant populates it, matching `prd.md:512`. |
| Check-In Date | Yes | ✅ | The `Check-In Date` picker is visible in both hotel layouts, matching `prd.md:513`. |
| Check-In Time | Yes | ✅ | The `Check-In Time` selector is visible in both hotel layouts, matching `prd.md:514`. |
| Check-Out Date | Yes | ⚠️ | The `Check-Out date` field is present, but `layout-temp/Hotel information (First time).jpg` uses helper copy about when the patient can begin the stay, which is the wrong explanation for check-out. Spec: `prd.md:515`. |
| Check-Out Time | Yes | ✅ | The `Check-Out time` selector is visible in both hotel layouts, matching `prd.md:516`. |
| Reservation Number | Yes | ✅ | The `Reservation Number` input is visible in both hotel layouts, matching `prd.md:517`. |
| Room Type | Yes | ✅ | The `Room Type` selector is visible in both hotel layouts, matching `prd.md:518`. |
| Amenities Included | No | ✅ | The optional `Amenities Included` input is visible in both hotel layouts, matching `prd.md:519`. |
| Transportation Details | No | ✅ | The optional `Transportation Details` input is visible in both hotel layouts, matching `prd.md:520`. |
| Special Requests | No | ✅ | The optional `Special Requests` input is visible in both hotel layouts, matching `prd.md:521`. |
| Phone Number | No | ⚠️ | The `Phone number` field is present, but `layout-temp/Hotel information (First time).jpg` shows unrelated helper copy below it and hardcodes a `+90` country prefix that is not specified in `prd.md:522`. |
| Email | No | ✅ | The optional `Email` input is visible in both hotel layouts, matching `prd.md:523`. |

**Extra Elements**:

- None.

**Screen Status**: 🟢 GOOD
**Field Coverage**: 13/13 (100%)
**Critical Issues**: None

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Severity | Observation | Recommendation | Evidence |
|---------|----------|-------------|----------------|----------|
| U-11 | ⚠️ UX Improvement | Helper copy under `Check-Out date` and `Phone number` does not describe the field below it, which weakens form clarity. | Rewrite helper copy so each hint explains the specific field directly below it, or remove the hint where unnecessary. | `layout-temp/Hotel information (First time).jpg`; helper text under check-out and phone fields. |
| U-17 | 💡 UX Suggestion | The CTA label `Send information` is generic for a provider-owned hotel record workflow. | Rename the CTA to `Save hotel details` for clearer intent. | `layout-temp/Hotel information (First time).jpg` and `layout-temp/Hotel information (First time) Typing.jpg`; button label visible bottom-right. |

**Flow Coverage Gaps**:

- No designed Screen 6 state shows the required travel-path badge plus passport/flight/hotel status badges together.
- The supplied Path A post-submission review variants do not cleanly map to a defined FR-008 screen and currently contradict the locked-after-submission rules by exposing `Edit ... details`.
- `Total Price` appears in one Screen 8 variant even though Screen 8 explicitly excludes price capture from this form.

---

### Flow MF2: Patient Self-Booked Travel

**Status**: 🔴 BLOCKED — Screen 10 now has both an awaiting state and one patient-submitted hotel-detail state, but the submitted hotel review violates the read-only rule, misbinds hotel fields to flight-derived values, and still leaves flight submitted states missing.
**Screens required**: 1
**Layout files**: `Awaiting patient’s hotel & flight details.jpg`, `Hotel details.jpg`

#### Screen 10: Travel Details — Booking/Quote Detail Screen (Provider, Path B)

**Layout**: `layout-temp/Awaiting patient’s hotel & flight details.jpg`, `layout-temp/Hotel details.jpg`

##### Flow Context

- **User arrives from**: Provider selects `View Travel Details` from Screen 6 after the patient submits travel records for a Path B appointment. Flow evidence: Main Flow 2 steps B9-B11 in `local-docs/project-requirements/functional-requirements/fr008-travel-booking-integration/prd.md:160-174` and Screen 6 navigation rule in `prd.md:432-435`.
- **Screen purpose**: Let the provider review patient-submitted flight and hotel details inline within the booking context, without editing and without any passport section. Spec evidence: `prd.md:534-587`.
- **Entry point**: Present. `layout-temp/Awaiting patient’s hotel & flight details.jpg` and `layout-temp/Hotel details.jpg` both keep the provider inside the booking detail page and show a patient-owned travel area with `Hotel details / Outbound Flight / Return Flight` tabs.
- **Exit path**: The awaiting-state file is read-only, but `layout-temp/Hotel details.jpg` exposes an `Edit Hotel details` action even though Path B must remain entirely read-only.
- **Data continuity**: Booking header, confirmed status, appointment summary, and timeline are preserved. The banner correctly states the information is provided by the patient and cannot be edited by the provider.
- **Flow context issues**: Only the hotel submitted-detail state is evidenced. No compliant outbound-flight or return-flight submitted layouts are provided, the hotel state contradicts the read-only rule with an edit CTA, and the structure uses tabs instead of the specified collapsible sub-sections.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Flight / Airline Name | Yes | ❌ | No Path B outbound-flight or return-flight submitted-detail layout was provided, so this field cannot be verified. Spec: `prd.md:542`. |
| Flight / Flight Number | Yes | ❌ | No Path B outbound-flight or return-flight submitted-detail layout was provided, so this field cannot be verified. Spec: `prd.md:543`. |
| Flight / Departure Airport | Yes | ❌ | No Path B outbound-flight or return-flight submitted-detail layout was provided, so this field cannot be verified. Spec: `prd.md:544`. |
| Flight / Arrival Airport | Yes | ❌ | No Path B outbound-flight or return-flight submitted-detail layout was provided, so this field cannot be verified. Spec: `prd.md:545`. |
| Flight / Departure Date | Yes | ❌ | No Path B outbound-flight or return-flight submitted-detail layout was provided, so this field cannot be verified. Spec: `prd.md:546`. |
| Flight / Departure Time | Yes | ❌ | No Path B outbound-flight or return-flight submitted-detail layout was provided, so this field cannot be verified. Spec: `prd.md:547`. |
| Flight / Arrival Date | Yes | ❌ | No Path B outbound-flight or return-flight submitted-detail layout was provided, so this field cannot be verified. Spec: `prd.md:548`. |
| Flight / Arrival Time | Yes | ❌ | No Path B outbound-flight or return-flight submitted-detail layout was provided, so this field cannot be verified. Spec: `prd.md:549`. |
| Flight / Ticket Confirmation Number | Yes | ❌ | No Path B outbound-flight or return-flight submitted-detail layout was provided, so this field cannot be verified. Spec: `prd.md:550`. |
| Flight / Ticket Class | Yes | ❌ | No Path B outbound-flight or return-flight submitted-detail layout was provided, so this field cannot be verified. Spec: `prd.md:551`. |
| Flight / Baggage Allowance | Yes | ❌ | No Path B outbound-flight or return-flight submitted-detail layout was provided, so this field cannot be verified. Spec: `prd.md:552`. |
| Flight / Special Requests | Yes | ❌ | No Path B outbound-flight or return-flight submitted-detail layout was provided, so this field cannot be verified. Spec: `prd.md:553`. |
| Flight / Submitted By | Yes | ❌ | No Path B outbound-flight or return-flight submitted-detail layout was provided, so this field cannot be verified. Spec: `prd.md:554`. |
| Flight / Status | Yes | ❌ | No Path B outbound-flight or return-flight submitted-detail layout was provided, so this field cannot be verified. Spec: `prd.md:555`. |
| Hotel / Hotel Name | Yes | ⚠️ | Label is present in `layout-temp/Hotel details.jpg`, but the value is `Turkish Airlines` (airline name), showing flight-to-hotel data misbinding. Spec: `prd.md:563`. |
| Hotel / Hotel Address | Yes | ⚠️ | Label is present, but the value is `TK142` (flight number), not a hotel address. Spec: `prd.md:564`. |
| Hotel / Check-In Date | Yes | ⚠️ | Label is present, but the value is `Dhaka Hazrat Shahjalal International Airport (DAC)`, which is an airport, not a date. Spec: `prd.md:565`. |
| Hotel / Check-In Time | Yes | ⚠️ | Label is present, but the value is `Istanbul Airport (IST)`, which is an airport, not a time. Spec: `prd.md:566`. |
| Hotel / Check-Out Date | Yes | ⚠️ | A date is shown (`February 25, 2024`), but the surrounding field order demonstrates that flight-style values have been shifted into hotel labels rather than correctly bound hotel-stay data. Spec: `prd.md:567`. |
| Hotel / Check-Out Time | Yes | ⚠️ | A time is shown (`10:00 AM (local time)`), but the section is populated from the same shifted flight-style value set. Spec: `prd.md:568`. |
| Hotel / Reservation Number | Yes | ⚠️ | Label is present, but the value is another date (`February 25, 2024`), not a reservation number. Spec: `prd.md:569`. |
| Hotel / Room Type | Yes | ⚠️ | Label is present, but the value is `4:00 PM (local time)`, not a room type. Spec: `prd.md:570`. |
| Hotel / Amenities Included | Yes | ⚠️ | Label is present, but the value is `123456789`, which reads like a booking reference rather than amenities text. Spec: `prd.md:571`. |
| Hotel / Transportation Details | Yes | ⚠️ | Label is present, but the value is `Economy` (ticket class), not transportation detail. Spec: `prd.md:572`. |
| Hotel / Special Requests | Yes | ⚠️ | Label is present, but the value is `17Kg` (baggage allowance), not a hotel request. Spec: `prd.md:573`. |
| Hotel / Phone Number | Yes | ⚠️ | Label is present, but the value is `$700 USD (Including taxes and fees)`, not a contact number. Spec: `prd.md:574`. |
| Hotel / Email | Yes | ⚠️ | Label is present, but the value is `Vegetarian meal requested.`, which is a special-request sentence, not an email address. Spec: `prd.md:575`. |
| Hotel / Submitted By | Yes | ❌ | Missing from the submitted hotel state. The PRD requires patient name plus submission timestamp. Spec: `prd.md:576`. |
| Hotel / Status | Yes | ❌ | Missing from the submitted hotel state. The PRD requires `Submitted / Awaiting` status display. Spec: `prd.md:577`. |

**Extra Elements**:

- The valid awaiting-state layout uses tabbed sub-navigation (`Hotel details / Outbound Flight / Return Flight`) instead of the two collapsible sub-sections specified in `prd.md:536`.
- `layout-temp/Hotel details.jpg` exposes an `Edit Hotel details` button even though Path B is explicitly read-only per `prd.md:580-586`.

**Screen Status**: 🔴 FAIL
**Field Coverage**: 13/29 (45%)
**Critical Issues**: The only supplied Screen 10 submitted-detail state is a hotel tab that exposes forbidden provider editing and maps hotel labels to flight-derived values. Outbound/return submitted states are still not evidenced, and `Submitted By` / `Status` metadata is missing.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Severity | Observation | Recommendation | Evidence |
|---------|----------|-------------|----------------|----------|
| U-04 | 🔴 Critical UX | The patient-owned hotel review shows an `Edit Hotel details` button directly below a banner that says the provider cannot edit the information. | Remove the edit CTA and keep the entire Path B review surface read-only; route corrections through admin contact as required by the PRD. | `layout-temp/Hotel details.jpg`; patient-owned banner and edit button appear in the same card. |
| U-05 | 🔴 Critical UX | The hotel detail values are mapped from flight-style data (`Turkish Airlines`, `TK142`, airport names, baggage, price), making the review unusable and untrustworthy. | Rebind the Screen 10 hotel detail labels to the actual hotel schema before development handoff. | `layout-temp/Hotel details.jpg`; hotel labels display airline, flight, airport, baggage, and price values. |
| U-20 | ⚠️ UX Improvement | The awaiting-state design uses a single generic `Awaiting patient's hotel & flight details` message, which does not distinguish between hotel, outbound-flight, and return-flight status. | Show separate empty states per sub-section so providers know which exact record is still pending. | `layout-temp/Awaiting patient’s hotel & flight details.jpg`; generic empty-state block under tabbed details. |
| U-03 | ⚠️ UX Improvement | The layout uses three tabs instead of the specified two collapsible detail sub-sections, which makes the provider switch context more than the PRD intends for a read-only inline review. | Replace the tabbed structure with the specified `Flight Details` and `Hotel Details` collapsible sections, and nest outbound/return within Flight Details. | `layout-temp/Awaiting patient’s hotel & flight details.jpg`; tabbed structure visible under the patient-owned banner while `prd.md:536` specifies collapsible sub-sections. |

**Flow Coverage Gaps**:

- No submitted-state layout was provided for outbound flight or return flight.
- The hotel submitted-state layout is present, but its values are misbound and it still omits the required `Submitted By` and `Status` metadata.
- A dedicated `Return flight not yet submitted` state, as required by `prd.md:557` and `prd.md:582`, was not evidenced in the provided layouts.

---

## Action Items

| Priority | Flow | Screen | Issue | Recommendation |
|----------|------|--------|-------|----------------|
| 🔴 Critical | MF1 | Screen 6 | Provider travel tracker is missing the required travel-path badge, passport/flight/hotel statuses, and Screen 6 action set. | Redesign Screen 6 as a status-first travel section with explicit badges and buttons for `View Passport`, `Enter Flight`, and `Enter Hotel`. |
| 🔴 Critical | MF1 | Screen 6 | The post-submission Path A review variants expose `Edit ... details` and `can be updated if needed` messaging even though submitted provider records should be locked. | Remove post-submission edit/update affordances from the booking-detail travel review and route corrections through admin only. |
| 🔴 Critical | MF2 | Screen 10 | The only submitted-detail Path B evidence is a hotel review state that exposes forbidden editing and maps hotel labels to flight-derived values, while outbound/return submitted states are still missing. | Rebuild Screen 10 as a read-only patient review surface, bind hotel labels to the hotel schema, and provide compliant outbound/return submitted states. |
| ⚠️ Important | MF2 | Screen 10 | Required `Submitted By` and `Status` fields are missing from the hotel submitted state and still unverified for outbound/return flight. | Add patient name + submission timestamp and `Submitted / Awaiting` state labels to both flight and hotel sections. |
| ⚠️ Important | MF1 | Screen 8 | A `Total Price` field appears in one flight-entry variant even though Screen 8 explicitly excludes price capture. | Remove `Total Price` from Screen 8 and keep price information at the quote/package layer only. |
| ⚠️ UX Improvement | MF2 | Screen 10 | The empty state does not distinguish between hotel, outbound-flight, and return-flight pending states. | Provide separate empty-state messaging per sub-section, including the required `Return flight not yet submitted` state. |
| 💡 UX Suggestion | MF1 | Screen 8 | The CTA `Send information` is generic for a provider data-entry flow. | Rename the CTA to `Save flight details`. |
| 💡 UX Suggestion | MF1 | Screen 9 | The CTA `Send information` is generic for a provider data-entry flow. | Rename the CTA to `Save hotel details`. |

### Priority Legend

- **🔴 Critical**: Blocks flow progression, breaks data integrity, or causes security/legal risk. Must fix before development.
- **🔴 Critical UX**: Severe usability issue that would prevent users from completing the flow or cause significant confusion. Must fix before development.
- **⚠️ Important**: Functional discrepancy that could cause user confusion or require rework during development. Should fix before development.
- **⚠️ UX Improvement**: Usability or design quality issue that deviates from platform conventions or best practices. Should fix before development.
- **💡 Suggestion**: Cosmetic or minor improvement. Can fix anytime.
- **💡 UX Suggestion**: Minor design enhancement that would improve polish. Can fix anytime.

---

## Notes

- Verification source: `local-docs/project-requirements/functional-requirements/fr008-travel-booking-integration/prd.md`
- Scope limited to Provider Platform Screen 6 through Screen 10 only.
- `layout-temp/Hotel details.jpg` was remapped during the patient-self-booked recheck to Path B Screen 10 because it carries the patient-owned banner and a submitted hotel-detail state.
- `layout-temp/Flight details.jpg` and `layout-temp/Hotel details copy.jpg` remain Path A provider-included post-submission review variants.
- Supplemental web UX heuristics were checked against the latest Vercel Web Interface Guidelines: [command.md](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md).
