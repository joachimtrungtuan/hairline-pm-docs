# Design Layout Verification Report — FR-008

**Report Date**: 2026-04-13
**Report Type**: Design Layout Verification
**FR Scope**: FR-008 — Travel & Logistics Coordination
**Flow Scope**: Admin Platform confirmed-stage Travel section only, limited to hotel and flight coverage in Screen 11 and Screen 12 (Tabs 2 and 3)
**Layout Source**: `layout-temp/Confirmed details/Book hotel & Book flight/`
**Platform**: Admin Web
**Status**: 🔴 BLOCKED

---

## Summary Dashboard

| # | Flow | Module | Screens Required | Screens Verified | Layout Status | Field Coverage |
|---|------|--------|-----------------|-----------------|---------------|----------------|
| A-04-T | Admin confirmed booking travel section (hotel + flight only) | A-04: Travel Management | 3 | 3 | 🔴 BLOCKED | ~54% |

**Overall**: 1 of 3 screens is 🟡 PARTIAL and 2 of 3 screens are 🔴 FAIL. The scope is blocked because the travel overview model is missing and the hotel detail content is materially incorrect.
**Screens**: 3 of 3 specified screens have layouts, but only the flight tab is close to spec. Approximate required-field coverage is 19 of 35 fields (~54%).

---

## Layout File Inventory

### Mapped to Spec Screens

| Layout File | Maps to Flow | Maps to Screen | Notes |
|-------------|-------------|----------------|-------|
| `Confirmed details/Book hotel & Book flight/Flight details.jpg` | A-04-T | Screen 12 — Tab 2 Flight Details | Read-only populated flight state embedded inside confirmed booking page |
| `Confirmed details/Book hotel & Book flight/Flight details/Edit.jpg` | A-04-T | Screen 12 — Tab 2 Flight Details | Editable flight correction state embedded inside confirmed booking page |
| `Confirmed details/Book hotel & Book flight/Hotel details.jpg` | A-04-T | Screen 12 — Tab 3 Hotel Details | Read-only populated hotel state embedded inside confirmed booking page |
| `Confirmed details/Book hotel & Book flight/Hotel details/Edit.jpg` | A-04-T | Screen 12 — Tab 3 Hotel Details | Editable hotel correction state embedded inside confirmed booking page |
| `Confirmed details/Book hotel & Book flight/Awaiting patient’s hotel & flight details.jpg` | A-04-T | Screen 12 — Tab 2 Flight Details | Pending/awaiting state with call-to-action inside confirmed booking page |
| `Confirmed details/Book hotel & Book flight/Awaiting patient’s hotel & flight details/Edit.jpg` | A-04-T | Screen 12 — Tab 2 Flight Details | Editable pending state inside confirmed booking page |

### Unmapped / Out of Scope Files

| Layout File | Reason |
|-------------|--------|
| `Confirmed details/Book hotel & Book flight/Already had passport.jpg` | Passport scope is outside requested hotel/flight-only review |
| `Confirmed details/Book hotel & Book flight/Already had passport/Edit.jpg` | Passport scope is outside requested hotel/flight-only review |
| `Confirmed details/Book hotel & Book flight/Waiting passport.jpg` | Passport scope is outside requested hotel/flight-only review |
| `Confirmed details/Book hotel & Book flight/Waiting passport/Add passport.jpg` | Passport scope is outside requested hotel/flight-only review |

---

## Detailed Verification

### Screen 11: Travel Section — Admin Booking/Inquiry Detail Screen

**Layout files examined**:
- `Confirmed details/Book hotel & Book flight/Flight details.jpg`
- `Confirmed details/Book hotel & Book flight/Hotel details.jpg`
- `Confirmed details/Book hotel & Book flight/Awaiting patient’s hotel & flight details.jpg`

| Field Name | Required | Status | Notes |
|------------|----------|--------|-------|
| Travel Path | Yes | ❌ MISSING | No provider-included vs patient self-booked badge is visible in the travel section on any examined layout; evidence: all three files show header, banner, and detailed forms/cards only. |
| Outbound Flight Status | Yes | ❌ MISSING | No flight-status badge such as `Submitted` / `Awaiting` / `Not included` is shown. The layout jumps directly into a detailed flight card or edit form. |
| Return Flight Status | Yes | ❌ MISSING | No return-flight status badge is shown. A `Return Flight` tab exists, but it is a content tab, not a status indicator. |
| Hotel Status | Yes | ❌ MISSING | No hotel-status badge such as `Submitted` / `Awaiting` / `Not included` is visible. |
| Actions | Yes | ❌⚠️ MISMATCH | FR requires `Re-notify patient` and `Apply Correction (→ Screen 12)`. Layout instead shows a pencil edit icon and, in the awaiting state, an `Add flight details` CTA. There is no explicit re-notify action and no explicit navigation to a separate correction screen. |

#### UX/UI Evaluation

| Rule ID | Check | Severity | Finding | Evidence |
|---------|-------|----------|---------|----------|
| U-02 | Information priority | ⚠️ UX Improvement | The screen intended to be a travel-status overview gives no summary status block. The user must scan a long page of passport and detail content before understanding travel completion state. | `Flight details.jpg`, `Hotel details.jpg` — detailed passport and travel records dominate the page; no compact status overview is visible. |
| U-16 | Interactive vs static distinction | ⚠️ UX Improvement | The only route into correction appears to be a small pencil icon, which is easy to overlook and weaker than the FR’s explicit action model. | `Flight details.jpg`, `Hotel details.jpg` — pencil icon appears at the section header without labeled action text. |
| W-07 | Action placement | ⚠️ UX Improvement | The layout embeds edit controls inside the same long detail page rather than presenting a clear page-level action from the overview. This weakens the admin’s correction workflow for confirmed bookings. | `Awaiting patient’s hotel & flight details.jpg` and `Flight details/Edit.jpg` — overview, pending state, and edit state live in one continuous page. |

**Screen Summary**: 🔴 FAIL. Coverage for the hotel/flight-specific Screen 11 requirements is 0 of 5 fields passing. The layout identity is only a partial match because it uses the confirmed booking page and travel tab, but it skips the required status-summary model and collapses Screen 11 and Screen 12 into one page.

---

### Screen 12 — Tab 2: Flight Details

**Layout files examined**:
- `Confirmed details/Book hotel & Book flight/Flight details.jpg`
- `Confirmed details/Book hotel & Book flight/Flight details/Edit.jpg`
- `Confirmed details/Book hotel & Book flight/Awaiting patient’s hotel & flight details.jpg`
- `Confirmed details/Book hotel & Book flight/Awaiting patient’s hotel & flight details/Edit.jpg`

| Field Name | Required | Status | Notes |
|------------|----------|--------|-------|
| Leg Type | Yes | ✅ PASS | Active tab `Outbound Flight` communicates the current leg; `Return Flight` is shown as a sibling tab. |
| Airline Name | Yes | ✅ PASS | Present in both read-only and edit layouts (`Turkish Airlines`). |
| Flight Number | Yes | ✅ PASS | Present in both read-only and edit layouts (`TK142`). |
| Departure Airport | Yes | ✅ PASS | Present in both read-only and edit layouts. |
| Arrival Airport | Yes | ✅ PASS | Present in both read-only and edit layouts. |
| Departure Date | Yes | ⚠️ MINOR ISSUE | Present in the read-only state, but the edit state uses an empty `Select date` field instead of prefilled data. |
| Departure Time | Yes | ✅ PASS | Present in read-only and editable states. |
| Arrival Date | Yes | ⚠️ MINOR ISSUE | Present in the read-only state, but the edit state uses an empty `Select date` field instead of prefilled data. |
| Arrival Time | Yes | ✅ PASS | Present in read-only and editable states. |
| Ticket Confirmation Number | Yes | ✅ PASS | Present in both states. |
| Ticket Class | Yes | ✅ PASS | Present in both states (`Economy`). |
| Baggage Allowance | Yes | ✅ PASS | Present in both states. |
| Special Requests | Yes | ✅ PASS | Present in both states. |
| Submitted By | Yes | ❌ MISSING | No patient/provider identity or submission timestamp is visible in any of the supplied flight layouts. |
| Status | Yes | ❌ MISSING | No read-only badge such as `Submitted` / `Awaiting` is visible inside the tab content. |

#### UX/UI Evaluation

| Rule ID | Check | Severity | Finding | Evidence |
|---------|-------|----------|---------|----------|
| U-02 | Information priority | ⚠️ UX Improvement | The flight-correction task is buried below a large passport section, so the current task’s content is not the first thing an admin sees after entering correction mode. | `Flight details.jpg`, `Flight details/Edit.jpg` — passport occupies the entire upper section before flight content appears. |
| U-17 | CTA label clarity | 💡 UX Suggestion | `Save update` is understandable but less direct than standard web copy such as `Save changes` or `Apply correction`, which would align better with the FR’s correction workflow. | `Flight details/Edit.jpg` and `Awaiting patient’s hotel & flight details/Edit.jpg` — primary CTA uses `Save update`. |
| W-07 | Action placement | ⚠️ UX Improvement | Page-level save/cancel controls appear at the top of the section while the form is long, increasing the chance that users finish editing below the fold without a nearby completion action. | `Flight details/Edit.jpg` — `Save update` / `Cancel` are above the travel form; the form extends well below. |

**Screen Summary**: 🟡 PARTIAL. 11 of 15 required fields pass or pass with minor issues. The tab is recognizable as the admin flight correction view, but it omits `Submitted By` and `Status`, and it behaves like an embedded section inside the confirmed booking page rather than a distinct correction screen reached from Screen 11.

---

### Screen 12 — Tab 3: Hotel Details

**Layout files examined**:
- `Confirmed details/Book hotel & Book flight/Hotel details.jpg`
- `Confirmed details/Book hotel & Book flight/Hotel details/Edit.jpg`

| Field Name | Required | Status | Notes |
|------------|----------|--------|-------|
| Hotel Name | Yes | ❌⚠️ MISMATCH | Value shown is `Turkish Airlines`, which reads like airline data rather than hotel data; evidence: `Hotel details.jpg`, `Hotel details/Edit.jpg`. |
| Hotel Address | Yes | ❌⚠️ MISMATCH | Value shown is `TK142`, which is formatted like a flight number rather than an address. |
| Check-In Date | Yes | ❌⚠️ MISMATCH | Read-only state shows `Dhaka Hazrat Shahjalal International Airport (DAC)`, which is airport text, not a date. |
| Check-In Time | Yes | ❌⚠️ MISMATCH | Read-only state shows `Istanbul Airport (IST)`, which is airport text, not a time. |
| Check-Out Date | Yes | ✅ PASS | Present as a date in the read-only and edit layouts. |
| Check-Out Time | Yes | ✅ PASS | Present as a time in the read-only and edit layouts. |
| Reservation Number | Yes | ✅ PASS | Present in both states. |
| Room Type | Yes | ✅ PASS | Present in both states. |
| Amenities Included | Yes | ❌⚠️ MISMATCH | Value shown is `123456789`, which reads like a numeric token rather than amenities content. |
| Transportation Details | Yes | ❌⚠️ MISMATCH | Value shown is `Economy`, which matches a flight class better than transportation detail text. |
| Special Requests | Yes | ❌⚠️ MISMATCH | Value shown is `17Kg`, which matches baggage allowance rather than a special request. |
| Phone Number | Yes | ✅ PASS | Present in both states. |
| Email | Yes | ✅ PASS | Present in both states. |
| Submitted By | Yes | ❌ MISSING | No submitter identity or timestamp is visible in the hotel layouts. |
| Status | Yes | ❌ MISSING | No `Submitted` / `Awaiting` badge is visible within the hotel tab content. |

#### UX/UI Evaluation

| Rule ID | Check | Severity | Finding | Evidence |
|---------|-------|----------|---------|----------|
| U-11 | Label clarity | 🔴 Critical UX | Multiple labels are paired with values from the wrong domain, so admins would misread hotel data and could make the wrong correction. | `Hotel details.jpg` — `Hotel Address` shows `TK142`; `Check-In Date` shows airport text; `Special Requests` shows `17Kg`. |
| U-14 | Semantic color usage | 💡 UX Suggestion | The tab highlight styling is subtle relative to the amount of content below, making it easy to miss which travel sub-view is active on first scan. | `Hotel details.jpg`, `Hotel details/Edit.jpg` — active tab is indicated only by a green underline/text shift. |
| W-05 | Form layout | ⚠️ UX Improvement | The hotel edit form follows a consistent column layout, but incorrect prefilled content undermines the form’s clarity and makes the correction workflow error-prone. | `Hotel details/Edit.jpg` — hotel-labeled inputs are prefilled with flight-like sample content. |

**Screen Summary**: 🔴 FAIL. 6 of 15 required fields pass; 7 required fields are mismatched and 2 are missing. The hotel tab is recognizably intended as Screen 12 hotel correction, but the populated content is semantically incorrect in several fields, creating a high risk of admin error.

---

## Action Items

| Priority | Screen | Issue | Recommendation |
|----------|--------|-------|----------------|
| High | Screen 11 | Rebuild the admin travel overview to show travel path, outbound/return/hotel status badges, and explicit actions for `Re-notify patient` and `Apply Correction`. | Separate Screen 11 from the detail/edit layout and implement the status-summary model described in FR-008. |
| High | Screen 12 — Hotel Tab | Replace the copied flight data in hotel fields (`Hotel Address`, `Check-In Date`, `Check-In Time`, `Amenities Included`, `Transportation Details`, `Special Requests`). | Bind hotel-specific data and sample content to the hotel schema, then re-review with the corrected layout. |
| Medium | Screen 12 — Flight Tab | Add the required admin metadata fields `Submitted By` and `Status`. | Surface submitter identity/timestamp and status badge in both read-only and edit-related states. |
| Medium | Screen 12 — Flight and Hotel Tabs | Make correction mode a clearer destination from the overview. | Use an explicit `Apply correction` CTA and keep save/cancel controls closer to the edited content. |
| Low | Screen 12 — Flight Tab | Improve CTA copy and prefilled edit-state dates. | Rename `Save update` to a standard correction/save label and prefill editable date controls with current record values. |

## Notes

- This review is constrained to admin confirmed-stage hotel and flight coverage only; passport states were intentionally excluded.
- The provided layouts appear to combine Screen 11 and Screen 12 concepts into one confirmed booking page, so mapping fidelity must be checked carefully during analysis.
- `Awaiting patient’s hotel & flight details.jpg` was used as evidence for pending flight-state behavior, but no equally clear pending hotel-state layout was supplied in the scoped files.
