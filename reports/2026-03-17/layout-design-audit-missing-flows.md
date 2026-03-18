# Layout Design Audit — Missing Mobile Flows

**Report Date**: 2026-03-17
**Report Type**: Design Layout Audit & Gap Analysis
**Source Spec**: `local-docs/reports/2026-02-05/missing-mobile-flows-design-complement.md` (v1.0 Final)
**Layout Source**: `layout-temp/` (initial batch + 2026-03-17 delivery)
**Platform**: Patient Mobile App
**Status**: In Progress — awaiting P04.1, P04.2, P08.1 Figma design file deliveries

---

## Summary Dashboard

| # | Flow | Module | Screens Required | Layout Status | Field Coverage |
|---|------|--------|-----------------|---------------|----------------|
| P01.1 | Delete Account | P-01: Auth & Profile | 3 (Warning, Identity Verification, Confirmation) | **🟡 Partial** | ~75% |
| P01.2 | Settings Screen | P-01: Auth & Profile | 5 (Main, Notifications, Privacy & Security, Privacy Policy, Terms & Conditions) | **🟢 Good** | ~90% |
| P01.3 | Change Password | P-01: Auth & Profile | 2 (Form, Confirmation) | **🟢 Complete** | ~98% |
| P02.1 | Compare Offers Side-by-Side | P-02: Quote Request | ~4 (Dashboard, Comparison Panel, Filter, Quote Cards) | **🟡 Partial** | ~65% |
| P02.2 | Cancel Inquiry | P-02: Quote Request | 2 (Confirmation Modal, Success) + error state | **🟢 Good** | ~85% |
| P02.3 | Expired Offers/Quotes | P-02: Quote Request | 2 (Expired Indicator, All Expired State) | **🟡 Partial** | ~40% |
| P02.4 | Legal/Policy Screens | P-02: Quote Request | 1 reusable viewer (3 document types) | **🟡 Partial** | ~70% (1 of 3 types) |
| P03.1 | Payment Methods Management | P-03: Booking & Payment | 3 (List, Add/Edit Form, Remove Modal) | **🟡 Partial** | ~60% |
| P04.1 | Passport Submission (Path A) | P-04: Travel & Logistics | 2 (Form, Read-Only View) | **🔴 No Figma design file** | — |
| P04.2 | Flight & Hotel Submission (Path B) | P-04: Travel & Logistics | 5 (Travel Check, Flight Form, Hotel Form, Read-Only, Itinerary) | **🔴 No Figma design file** | — |
| P05.1 | Day-to-Day Treatment Progress | P-05: Aftercare | 3 (Timeline, Day Popup, Completed View) | **🟡 Partial** | ~40% |
| P05.2 | Previous Treatments List | P-05: Aftercare | 1 (My Treatments List) | **🟡 Partial** | ~55% |
| P05.3 | Submitted Reviews List | P-05: Aftercare | 2 (Reviews List, Review Detail) | **🟢 Good** | ~85% |
| P06.1 | Notification Listing & Bubble | P-06: Communication | 2 (Bubble Component, Notification List) | **🟡 Partial** | ~65% |
| P08.1 | Help & Support | P-08: Help Center | 5 (Hub, Help Center, Tickets List, Ticket Detail, Contact Form) | **🔴 No Figma design file** | — |

**Overall**: 12 of 15 flows have extracted layout frames; 3 flows have no delivered Figma design files (P04.1, P04.2, P08.1).
**Screens**: ~35 of ~47 specified screens have layouts (~74% coverage).

---

## Layout File Inventory

### Mapped to Spec Flows

| Layout File | Maps to Flow | Maps to Screen |
|-------------|-------------|----------------|
| `Inquiries/Cancel Inquiry_.png` | P02.2 | P02.2-S1 (Confirmation Modal) |
| `Inquiries/Cancel Inquiry_ - ERROR.png` | P02.2 | P02.2-S1 error state (blocked stage) |
| `Inquiries/Cancellation Success Confirmation.png` | P02.2 | P02.2-S2 (Success) |
| `Offer/Offers.png` | P02.1 | P02.1-S1 (Quote list, no selection) |
| `Offer/Compare Offers.png` | P02.1 | P02.1-S1 (Quote list with selection + compare CTA) |
| `Offer/Compare Offers Table.png` | P02.1 | P02.1-S1 Comparison Panel |
| `Offer/Full table.png` | P02.1 | P02.1-S1 Comparison Panel (full width) |
| `Offer/Offers - Filter.png` | P02.1 | P02.1-S1 Sort & Filter |
| `Offer/Offers - Select date.png` | P02.1 | P02.1-S1 date selection bottom sheet |
| `Offer/Inquiry-Level Fields.png` | P02.1 | P02.1-S1 Inquiry-Level Fields section |
| `Offer/Expired Offers/Offers - Expired.png` | P02.3 | P02.3-S1 + P02.3-S2 combined |
| `Offer/Expired Offers/Offer single.png` | P02.3 | P02.3-S1 Expired quote detail |
| `Offer/Expired Offers/Offer single - Floating Button - Expired.png` | P02.3 | P02.3-S1 Expired quote with floating bar |
| `Offer/Cancellation policy.png` | P02.4 | P02.4-S1 (Legal Document Viewer — Cancellation Policy) |
| `Offer/Cancellation policy - Table of content open.png` | P02.4 | P02.4-S1 with TOC dropdown open |
| `Treatment list/My Treatments List.png` | P05.2 | P05.2-S1 (My Treatments List) |
| `Treatment list/Sorting.png` | P05.2 | P05.2-S1 Sort Options |
| `Profile > Delete account/Delete your account.png` | P01.1 | P01.1-S1 (Delete Account Warning) |
| `Profile > Delete account/Cannot delete account.png` | P01.1 | P01.1-S1 conditional (Blocking Message) |
| `Profile > Delete account/Deletion Reason.png` | P01.1 | P01.1-S1 conditional (Deletion Reason selector) |
| `Profile > Delete account/Final Confirmation.png` | P01.1 | P01.1-S1 conditional (Final Confirmation Modal) |
| `Profile > Delete account/Verify Your Identity/Password.png` | P01.1 | P01.1-S2 (Password verification) |
| `Profile > Delete account/Verify Your Identity/Password-1.png` | P01.1 | P01.1-S2 (Email OTP verification) |
| `Profile > Delete account/Verify Your Identity/Password/Error.png` | P01.1 | P01.1-S2 error state (password) |
| `Profile > Delete account/Verify Your Identity/Password/Error-1.png` | P01.1 | P01.1-S2 error state (OTP) |
| `Profile > Delete account/Deletion Request Submitted Confirmation.png` | P01.1 | P01.1-S3 (Confirmation) |
| `Profile/Screen P01.2-S1_ Settings Main Screen.png` | P01.2 | P01.2-S1 (Settings Main) |
| `Profile > Settings/Screen P01.2-S2_ Notification Settings.png` | P01.2 | P01.2-S2 (Notification Settings) |
| `Profile > Settings/P01.2-S3_ Privacy & Security Menu.png` | P01.2 | P01.2-S3 (Privacy & Security) |
| `Profile > Settings/P01.2-S4_ Privacy Policy.png` | P01.2 | P01.2-S4 (Privacy Policy) |
| `Profile > Settings/P01.2-S5_ Terms & Conditions.png` | P01.2 | P01.2-S5 (Terms & Conditions) |
| `Profile > Settings/Screen P01.3-S1_ Change Password Form.png` | P01.3 | P01.3-S1 (empty state) |
| `Profile > Settings/Change Password Form/Error.png` | P01.3 | P01.3-S1 (validation error state) |
| `Profile > Settings/Change Password Form/Success.png` | P01.3 | P01.3-S1 (all-valid state) |
| `Profile > Settings/Screen P01.3-S2_ Password Changed Confirmation.png` | P01.3 | P01.3-S2 (Confirmation) |
| `Profile > Payment methods/Payment Methods.png` | P03.1 | P03.1-S1 (List — populated) |
| `Profile > Payment methods/Empty.png` | P03.1 | P03.1-S1 (List — empty state) |
| `Profile > Payment methods/Action.png` | P03.1 | P03.1-S1 (Per-card action sheet) |
| `Profile > Payment methods/Add Payment Methods.png` | P03.1 | P03.1-S2 (Add mode) |
| `Profile > Payment methods/Edit Payment Methods.png` | P03.1 | P03.1-S2 (Edit mode) |
| `Profile > Payment methods/Remove Payment Methods/Default Card.png` | P03.1 | P03.1-S3 (Default card removal modal) |
| `Profile > Payment methods/Remove Payment Methods/Not default card.png` | P03.1 | P03.1-S3 (Non-default removal modal) |
| `In progress/Treatment.png` | P05.1 | P05.1-S1 (Treatment Progress Timeline) |
| `In progress/End of Treatment.png` | P05.1 | P05.1-S3 (Completed Treatment View) |
| `Profile > My reviews/My Reviews.png` | P05.3 | P05.3-S1 (My Reviews List) |
| `Profile > My reviews/Review Detail.png` | P05.3 | P05.3-S2 (Published state) |
| `Profile > My reviews/Review Detail - Edit.png` | P05.3 | P05.3-S2 (Edit form) |
| `Profile > My reviews/Review Detail - Removed.png` | P05.3 | P05.3-S2 (Removed by Admin state) |
| `Profile > My reviews/Review Detail - Takedown Request.png` | P05.3 | P05.3-S2 (Takedown Request modal) |
| `Notification/Notification - Having unread notification.png` | P06.1 | P06.1-S1 (Bubble with badge) |
| `Notification/Notification - Not any unread notification.png` | P06.1 | P06.1-S1 (Bubble — no badge) |
| `Notification/Notification - Very high counts unread notification.png` | P06.1 | P06.1-S1 (Bubble — 99+ cap) |
| `Notification/Notification list.png` | P06.1 | P06.1-S2 (Notification List) |
| `Notification/Notification list - Filter.png` | P06.1 | P06.1-S2 (Filter bottom sheet) |
| `Notification/Notification list - Apply Filter.png` | P06.1 | P06.1-S2 (Active filter state) |
| `Notification/Notification categories.png` | P06.1 | P06.1-S2 (Category icon reference) |

### Not Mapped to Missing Flows Spec (existing FR screens or extras)

| Layout File | Likely Purpose | Notes |
|-------------|---------------|-------|
| `Offer/Offer single.png` | FR-005 Screen 2 (Quote Detail) | Existing Figma scope — full offer detail |
| `Offer/Offer single - Floating Button.png` | FR-005 Screen 2 variant | Floating accept bar variant |
| `Offer/Offer single - Select date.png` | FR-005 Screen 2 date picker | Per-date selection bottom sheet |
| `Offer/Confirm accept offer.png` | FR-005 Screen 3 (Acceptance Modal) | Quote acceptance confirmation |
| `Offer/Discount code applied.png` | Not in missing flows spec | Discount code feature — not specified |
| `Offer/Extra (Upsell) screen.png` | Not in missing flows spec | Upsell/discount variant |
| `Offer/Provider single.png` | FR-015 / existing flow | Provider profile page |
| `Offer/Request single.png` | FR-003 Screen detail | Inquiry request detail view |
| `Offer/Treatment single.png` | Treatment catalog detail | Treatment type info page |
| `Offer/My Treatments List.png` | Inquiry dashboard variant | Home list at "Offers" stage |
| `Inquiries/My Treatments List.png` | Inquiry dashboard variant | Home list at "Requested" stage |
| `Inquiries/Requested details.png` | FR-003 Screen 8 | Inquiry detail at Requested stage |
| `Offer/Top.png` | Section header element | "Compare Offers Side-by-Side" text label |
| `Offer/PointerLabel/Note.png` | UI element | "RESOURCES" label |
| `Offer/Text + icon.png` | UI element | "Original Design" link |
| `Offer/Text + icon-1.png` | UI element | "Task Link" link |
| `Profile/Profile.png` | Parent Profile screen | Navigation entry point to Settings/Delete Account |
| `Profile/Edit profile.png` | Profile Edit form | Outside P01.2/P01.3 scope |
| `In progress/My Treatments List.png` | Case list view | Navigation entry screen for In Progress cases |
| `In progress/Booking info.png` | Booking details tab | Contains Journey Timeline (should be on P05.1 screens) |
| `In progress/Provider.png` | Provider details tab | Provider info for active case |
| `In progress/Problem.png` | Patient request tab | 3D scan and medical questionnaires |
| `Aftercare/*.png` (17 images) | FR-011 Aftercare scope | Aftercare milestone dashboard, medication, instructions, questionnaires, scan upload, payment. Outside P05.1 spec scope. |

---

## Detailed Audit by Flow

---

### Flow P01.1: Delete Account

**Status**: 🟡 Partial — layouts received, significant issues on S2
**Screens required**: 3
**Layout files**: `Delete your account.png`, `Cannot delete account.png`, `Deletion Reason.png`, `Final Confirmation.png`, `Verify Your Identity/Password.png`, `Verify Your Identity/Password-1.png`, `Verify Your Identity/Password/Error.png`, `Verify Your Identity/Password/Error-1.png`, `Deletion Request Submitted Confirmation.png`

#### Screen P01.1-S1: Delete Account Warning

**Layout**: `Profile > Delete account/Delete your account.png` + conditional overlays

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Warning Icon | Yes | ✅ | Red warning triangle at top center |
| Screen Title | Yes | ✅ | "Delete Your Account" displayed |
| Back Navigation | Yes | ✅ | Back arrow top-left |
| Blocking Message (Conditional) | Conditional | ✅ | `Cannot delete account.png` shows correct blocking modal with support path |
| Contact Support Link (Conditional) | Conditional | ✅ | "Contact support" button in blocking modal |
| Consequences Header | Yes | ✅ | "What may be deleted or anonymized" |
| Consequences List | Yes | ✅ | All 4 items present (Profile, Messages, Reviews, Media) |
| Retained Data Header | Yes | ✅ | "What will be retained (legal requirement)" |
| Retained Data Explanation | Yes | ✅ | Full text matches spec |
| Processing Timeline Notice | Yes | ✅ | "Verified deletion requests are completed within 30 calendar days." |
| Deletion Reason Selector (Optional) | No | ✅ | Dropdown with "Select one" placeholder; `Deletion Reason.png` shows expanded bottom sheet |
| Final Confirmation Modal | Conditional | ✅ | `Final Confirmation.png` with Confirm/Cancel |
| Request Deletion Button | Yes | ⚠️ | **Label mismatch**: Button reads "Delete your account" — spec says "Request Deletion" |
| Go Back Button | Yes | **❌ MISSING** | No secondary "Go Back" button — only back arrow exists |

#### Screen P01.1-S2: Identity Verification Step

**Layout**: `Profile > Delete account/Verify Your Identity/Password.png` (password tab), `Password-1.png` (OTP tab)

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Screen Title | Yes | ✅ | "Verify Your Identity" |
| Back Navigation | Yes | ✅ | Back arrow present |
| Security Icon | Yes | ✅ | Blue shield with checkmark |
| Instruction Text | Yes | ✅ | Exact match to spec |
| Verification Method Selector | Yes | ✅ | Chip/tab: "Password" and "Email OTP" |
| Password Field | Conditional | **❌ WRONG** | Shows "Email address" field instead of masked password input |
| Email OTP Field | Conditional | ⚠️ | 6 input boxes shown but instruction text says "4 digit" — spec requires "6-digit" |
| Resend OTP Link | Conditional | ✅ | "Resend code" link present |
| Error Message | Conditional | ✅ | Both password and OTP error states provided |
| Verify Button | Yes | ⚠️ | Button is green — spec requires red/destructive style |
| Cancel Button | Yes | **❌ MISSING** | No Cancel button — only back arrow |
| Password show/hide toggle | Yes | **❌ MISSING** | Not present (field type is wrong to begin with) |

**Extra element**: "Forgot your password?" link present but not specified in report.

#### Screen P01.1-S3: Deletion Request Submitted Confirmation

**Layout**: `Profile > Delete account/Deletion Request Submitted Confirmation.png`

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Confirmation Icon | Yes | ✅ | Green checkmark circle |
| Screen Title | Yes | ✅ | "Deletion Request Submitted" |
| Request Status | Yes | ✅ | "Pending Admin Review" badge |
| Request Reference | Yes | ⚠️ | Shows "Turkish Airlines" — **placeholder/dummy data** |
| Submitted Timestamp | Yes | ✅ | "10:15 AM, 26 June 2026" |
| Processing Timeline Notice | Yes | ✅ | Matches spec |
| What Happens Next Section | Yes | ✅ | All 4 required bullet items present |
| Retained Data Reminder | Yes | ✅ | Full text matches spec |
| Email Confirmation Notice | Yes | ✅ | Placeholder format present |
| Back to Profile Button | Yes | ✅ | Green button |

**Flow coverage gaps**:

- ⚠️ Lockout/rate-limit handling is not evidenced as a distinct UI state. The flow diagram includes it, but the current layouts only show retryable verification errors.
- ⚠️ Typo "Request Detailed" should be "Request Details" on S3

---

### Flow P01.2: Settings Screen

**Status**: 🟢 Good — 7/7 screens covered, minor gaps
**Screens required**: 5
**Layout files**: `Screen P01.2-S1_ Settings Main Screen.png`, `Screen P01.2-S2_ Notification Settings.png`, `P01.2-S3_ Privacy & Security Menu.png`, `P01.2-S4_ Privacy Policy.png`, `P01.2-S5_ Terms & Conditions.png`

#### Screen P01.2-S1: Settings Main Screen

**Layout**: `Profile/Screen P01.2-S1_ Settings Main Screen.png`

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Screen Title "Settings" | Yes | ✅ | Matches |
| Back Navigation | Yes | ✅ | Back arrow present |
| Notification Settings row | Yes | ✅ | Present — minor casing: "Notification settings" vs spec "Notification Settings" |
| Privacy & Security row | Yes | ✅ | Present — uses "Privacy and security" vs spec "Privacy & Security" |
| Terms & Conditions row | Yes | ✅ | Matches |
| Help & Support row | Yes | ✅ | Matches |

#### Screen P01.2-S2: Notification Settings

**Layout**: `Profile > Settings/Screen P01.2-S2_ Notification Settings.png`

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Screen Title | Yes | ✅ | "Notification Settings" |
| Back Navigation | Yes | ✅ | Present |
| Explanation Text | Yes | **❌ MISSING** | Spec requires "Choose how you want to receive notifications from Hairline." |
| MVP Notice | Conditional | **❌ MISSING** | Per-category preferences notice not shown |
| Global Email Toggle | Yes | ✅ | "Email Notifications" with ON toggle |
| Global Push Toggle | Yes | ✅ | "Push Notifications" with ON toggle |
| Mandatory Notifications Note | Yes | ✅ | Blue info card about security notifications |
| System Event Notifications Note | Yes | ✅ | Separate blue info card about automatic notifications |

#### Screen P01.2-S3: Privacy & Security Menu

**Layout**: `Profile > Settings/P01.2-S3_ Privacy & Security Menu.png`

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Screen Title | Yes | ✅ | "Privacy & Security" |
| Back Navigation | Yes | ✅ | Present |
| Change Password row | Yes | ✅ | Present |
| Privacy Policy row | Yes | ✅ | Shield-check icon present |

#### Screen P01.2-S4: Privacy Policy — FULLY COMPLIANT

**Layout**: `Profile > Settings/P01.2-S4_ Privacy Policy.png` — All 5 fields present and correct.

#### Screen P01.2-S5: Terms & Conditions — FULLY COMPLIANT

**Layout**: `Profile > Settings/P01.2-S5_ Terms & Conditions.png` — All 5 fields present and correct.

---

### Flow P01.3: Change Password

**Status**: 🟢 Complete — all fields covered with 3 state variants
**Screens required**: 2
**Layout files**: `Screen P01.3-S1_ Change Password Form.png`, `Change Password Form/Error.png`, `Change Password Form/Success.png`, `Screen P01.3-S2_ Password Changed Confirmation.png`

#### Screen P01.3-S1: Change Password Form — FULLY COMPLIANT

**Layouts**: Empty state, Error state, Success state — 3 variants covering all interactions.

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Screen Title | Yes | ✅ | "Change Password" |
| Back Navigation | Yes | ✅ | Present |
| Current Password (masked) | Yes | ✅ | Masked field with show/hide toggle |
| Forgot Your Password Link | Yes | ✅ | "Forgot your password?" in green text |
| New Password (masked) | Yes | ✅ | With show/hide toggle |
| Confirm New Password (masked) | Yes | ✅ | With show/hide toggle |
| Password Policy Helper | Yes | ✅ | 3 rules with color-coded checkmarks |
| Save Button | Yes | ✅ | Disabled when invalid, enabled when all pass |
| Error Message | Conditional | ✅ | Red text on failed rules in Error.png |

#### Screen P01.3-S2: Password Changed Confirmation — FULLY COMPLIANT

**Layout**: `Profile > Settings/Screen P01.3-S2_ Password Changed Confirmation.png` — All 4 fields present and correct.

---

### Flow P02.1: Compare Offers Side-by-Side

**Status**: 🟡 Partial — layouts present with field gaps
**Screens required**: ~4 logical views within P02.1-S1
**Layout files**: `Compare Offers.png`, `Compare Offers Table.png`, `Full table.png`, `Offers.png`, `Offers - Filter.png`, `Offers - Select date.png`, `Inquiry-Level Fields.png`

#### Screen P02.1-S1: Inquiry Dashboard with Quote Comparison

**Inquiry-Level Fields** (from `Inquiry-Level Fields.png`):

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Current Stage badge | Yes | ✅ | Shows "OFFERS" |
| Inquiry Reference | Yes | ✅ | HP202401 |
| Timeline | Yes | ✅ | Requested + Offers with timestamps |
| Inquiry Summary | Yes | ✅ | "Your request overview" with text |
| Medical Alerts | Yes | ✅ | "None" chip shown |
| Deadlines | Yes | ✅ | 25 Feb, 2024 |
| Next Actions | Yes | ✅ | "View all offer" + "View details" |

**Per-Quote Card Fields** (from `Offers.png`, `Compare Offers.png`):

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Treatment name | Yes | ⚠️ | Not shown separately — provider name dominates |
| Provider name & location | Yes | ✅ | "X Hair Transplant, Istanbul, Turkey" |
| Per-date Pricing | Yes | ✅ | Treatment time + Treatment price per date slot |
| Provider Reviews rating/count | Yes | ✅ | 4.8 stars (20 review) |
| Accept button | Yes | ✅ | Green "Accept" button |
| View Details button | Yes | ✅ | "View details" outline button |
| Compare Selection checkbox | Yes | ✅ | Circle checkboxes with "2 offers are selected (Maximum 3 offers select)" |
| Expiry Timer | Yes | **❌ MISSING** | No countdown timer visible on quote cards |
| Appointment Slot (Pre-Scheduled) | Yes | **❌ MISSING** | Only date ranges, no specific appointment slot |
| Inclusions chips | No | ❌ | Not on cards (only in detail/comparison) |
| Price per Graft | Yes | **❌ MISSING** | Not on cards (only in comparison table) |
| Provider Credentials Summary | Yes | **❌ MISSING** | Not on cards |
| Contact Support action | Yes | **❌ MISSING** | No per-quote Contact Support button |

**Comparison Panel** (from `Full table.png`, `Compare Offers Table.png`):

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Total price per date | Yes | ✅ | Multiple date/price rows shown |
| Graft count estimate | Yes | ✅ | "2,000 grafts" shown per offer |
| Graft estimation text | Yes | ✅ | Full graft estimation paragraph |
| Price per Graft | Yes | ✅ | "$1 - $10 / Graft" shown |
| Included services checklist | Yes | ✅ | Medical consultation, Maximum Grafts, PRP Injection, Washing Session, Life Time Warranty, Preferred Language Translator, 5 Stars Hotel Reservation, Business Class Flight |
| Accommodation section | Yes | ✅ | Hotel reservation details |
| Transportation section | Yes | ✅ | Airport transfer, hotel-facility transport |
| Flights section | Yes | ✅ | Flight inclusion note |
| Review rating/count comparison row | Yes | **⚠️ PARTIAL** | Rating/count is visible in each provider header, but not normalized as a dedicated comparison row |
| Soonest appointment slot row | Yes | **❌ MISSING** | Not a comparison row |
| Provider credentials summary row | Yes | **❌ MISSING** | Not a comparison row |

**Filter Panel** (from `Offers - Filter.png`):

| Field | Layout | Notes |
|-------|--------|-------|
| Min/Max Price | ✅ | Stepper inputs ($0–$10,000) |
| Min/Max Graft | ✅ | Stepper inputs (0–10,000) |
| Rating slider | ✅ | Range slider 1–5 stars |
| Earliest/Latest date | ✅ | Date picker fields |
| Apply/Reset buttons | ✅ | "Apply filter" / "Reset filter" |
| **Typo** | ⚠️ | "Slect date" → should be "Select date" |

**Flow/Navigation Issues**:

| Issue | Severity | Detail |
|-------|----------|--------|
| Comparison as separate screen | HIGH | Spec says comparison is a **conditional inline panel** within the dashboard. Layouts show it as a separate full-screen table. |
| Accept button on comparison table | ⚠️ | Comparison table has Accept/View details per column at bottom — acceptable alternative but flow differs from spec (acceptance should continue via FR-005 Screen 2 → Screen 3) |

---

### Flow P02.2: Cancel Inquiry

**Status**: 🟢 Good coverage — minor field gaps
**Screens required**: 2 + error state
**Layout files**: `Cancel Inquiry_.png`, `Cancel Inquiry_ - ERROR.png`, `Cancellation Success Confirmation.png`

#### Screen P02.2-S1: Cancel Inquiry Confirmation Modal

**Layout**: `Inquiries/Cancel Inquiry_.png`

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Warning Icon | Yes | ✅ | Red triangle with exclamation |
| Modal Title | Yes | ✅ | "Cancel Inquiry?" |
| Warning Message | Yes | ✅ | "Canceling this inquiry is irreversible. All quotes you've received will be cancelled and providers will be notified." |
| Current Stage Badge | Yes | ✅ | "REQUESTED" (green badge) |
| Inquiry Reference | Yes | ✅ | "Inquiry Reference: HP202401" |
| Impact Summary | Yes | **❌ MISSING** | Must show "X active quotes will be cancelled" or "No quotes received yet" |
| Cancellation Reason Label | Yes | ⚠️ | Shows "Cancellation Reason" — spec says "Why are you cancelling?" |
| Cancellation Reason Options | Yes | ✅ | All 7 options present |
| Additional Notes | Conditional | ✅ | Shown below "Other" option |
| Optional Feedback | No | ✅ | "Optional Feedback" field present |
| Provider Notification Note | Yes | ✅ | "Affected providers will be notified of this cancellation within 5 minutes" |
| Confirm Cancellation Button | Yes | ✅ | Red destructive button |
| Go Back Button | Yes | ✅ | Outline button |

**Text differences**:

- Option shows "Found a better option" — spec says "Found a better option **elsewhere**"
- Label "Cancellation Reason" — spec says "Why are you cancelling?"

#### Screen P02.2-S1 — Error State (Blocked Cancellation)

**Layout**: `Inquiries/Cancel Inquiry_ - ERROR.png`

| Field | Layout | Notes |
|-------|--------|-------|
| Error modal overlay | ✅ | Shown as modal on top of inquiry detail |
| Warning icon | ✅ | Red triangle |
| Blocking title | ✅ | "Cannot cancel inquiry at this stage" |
| Blocking explanation | **❌ Placeholder** | Lorem ipsum — needs real copy |
| Contact Support button | ✅ | "Contact support" (green button) |
| Background stage badge | ✅ | Shows "ACCEPTED" confirming blocked stage |

#### Screen P02.2-S2: Cancellation Success Confirmation

**Layout**: `Inquiries/Cancellation Success Confirmation.png`

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Success Icon | Yes | ✅ | Green checkmark circle |
| Confirmation Title | Yes | ✅ | "Inquiry Cancelled" |
| Confirmation Message | Yes | ✅ | "Your inquiry has been successfully cancelled." |
| Inquiry Reference + Badge | Yes | ✅ | "REQUESTED" badge + HP202401 |
| Cancellation Timestamp | Yes | ✅ | "14:00, 25 January, 2026" |
| Impact Summary (conditional) | Yes | ✅ | All 3 conditional variants shown with checkmarks |
| Provider Notification Status | Yes | ✅ | "All affected providers have been notified of this cancellation" |
| Back to My Inquiries Button | Yes | ✅ | "Back to My Inquiries" (green) |
| Start New Inquiry Button | Yes | ✅ | "Start New Inquiry" (outline) |
| Next Steps Section Label | Yes | **❌ MISSING** | Spec requires "What would you like to do next?" header |
| Contact Support Link | No (optional) | **❌ MISSING** | Spec says "Need help? Contact support" link |

---

### Flow P02.3: Expired Offers/Quotes

**Status**: 🟡 Partial — significant field gaps and flow issues
**Screens required**: 2 (Expired Indicator state + All Expired state)
**Layout files**: `Expired Offers/Offers - Expired.png`, `Expired Offers/Offer single.png`, `Expired Offers/Offer single - Floating Button - Expired.png`

#### Screen P02.3-S1: Expired Quote Indicator (within Quote List)

**Layout**: `Expired Offers/Offers - Expired.png` (list view), `Offer single.png` + `Offer single - Floating Button - Expired.png` (detail views)

**List view** (`Offers - Expired.png`):

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Expired Badge per card | Yes | ✅ | "Expired" label on each card (red text) |
| Card Overlay Styling (50% opacity) | Yes | ⚠️ | Cards appear slightly muted but NOT clearly at 50% opacity |
| Original Quote Summary | Yes | ✅ | Pricing and dates visible |
| View Details action | Yes | ✅ | "View details" link present |
| Expiry Date Display | Yes | **❌ MISSING** | No "Expired on [date]" shown per card in list view |
| Disabled Accept Button | Yes | **⚠️ AMBIGUOUS** | Buttons are visually muted versus active offer cards, but the disabled state is not explicit enough in the static list layout |
| Disabled Compare Checkbox | Yes | **❌ MISSING** | No checkboxes shown at all on expired cards |
| Contact Support Link | No | ❌ | Not present per card |
| Tooltip on disabled Accept tap | Yes | **❌ MISSING** | No tooltip design |

**Detail view** (`Offer single.png` expired variant, `Floating Button - Expired.png`):

| Field | Layout | Notes |
|-------|--------|-------|
| "Expired" section replacing Expiry Timer | ✅ | Red "Expired" banner with date |
| Expired date display | ✅ | "Expired on 12:00, 26 June 2025" |
| All quote details visible | ✅ | Full detail preserved |
| Accept button disabled | ✅ | Floating bar Accept button appears **grayed out/disabled** in `Floating Button - Expired.png` — correctly styled |
| De-emphasized visual treatment | ⚠️ | Content not sufficiently muted compared to active offer detail |

#### Screen P02.3-S2: All Quotes Expired State

**Layout**: Top banner area of `Expired Offers/Offers - Expired.png`

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| State explanation text | Yes | ✅ | "All Quotes Have Expired: The quotes you received for this inquiry have all expired. You can cancel this inquiry and submit a new one, or contact support for assistance." |
| Expired State Icon | Yes | **❌ MISSING** | Spec requires clock/hourglass icon at top center |
| State Title (standalone heading) | Yes | ⚠️ | Shown as banner text, not as prominent standalone "All Quotes Have Expired" heading |
| Inquiry Summary | Yes | **❌ MISSING** | Must include treatment type, submission date, number of expired quotes |
| Expired Quotes Count | Yes | **❌ MISSING** | "X quote(s) expired" |
| Last Expiry Date | Yes | **❌ MISSING** | "Last quote expired on [date]" |
| Cancel Inquiry Button (primary CTA) | Yes | **❌ CRITICAL** | No Cancel Inquiry button — this is a dead-end flow |
| Contact Support Link | Yes | **⚠️ PARTIAL** | Words "contact support" appear in banner text but not as a distinct tappable CTA button/link |

---

### Flow P02.4: Legal/Policy Screens (Quote Context)

**Status**: 🟡 Partial — only Cancellation Policy designed (1 of 3 document types)
**Screens required**: 1 reusable viewer (3 variants by title)
**Layout files**: `Cancellation policy.png`, `Cancellation policy - Table of content open.png`

#### Screen P02.4-S1: Legal Document Viewer (Shared Screen)

**Layout**: `Offer/Cancellation policy.png`

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Screen Title (dynamic) | Yes | ✅ | "Cancellation policy" — but spec expects it to also serve "Privacy Commitment" and "Terms of Service" |
| Back Navigation | Yes | ✅ | Back arrow present |
| Document Version | Conditional | ✅ | "Version: 1.0" shown |
| Last Updated | Conditional | ✅ | "Update: 23 June, 2025" shown |
| Document Content (scrollable rich text) | Yes | ✅ | Scrollable body with headings and paragraphs |
| Table of Contents | Conditional | ✅ | Dropdown with expandable section links |
| Scroll Progress Indicator | No (optional) | ❌ | Not present |

**Layout**: `Offer/Cancellation policy - Table of content open.png`

| Field | Layout | Notes |
|-------|--------|-------|
| TOC dropdown expanded | ✅ | Shows 4 items, all placeholder text ("Table of Contents item") |
| Section navigation links | ✅ | Tappable TOC items that scroll to sections |

**Issues**:

- ⚠️ Only **Cancellation Policy** designed — spec requires this viewer to be reusable for **Privacy Commitment** and **Terms of Service** with dynamic title
- ⚠️ Version + Last Updated combined in one line — spec shows them as separate badge + datetime fields
- ⚠️ TOC items are all placeholder text — need real or representative content

> **Placeholder — awaiting Privacy Commitment and Terms of Service layout variants**

---

### Flow P03.1: Payment Methods Management

**Status**: 🟡 Partial — all 3 screens present but significant issues on Edit mode and Remove modal
**Screens required**: 3
**Layout files**: `Payment Methods.png`, `Empty.png`, `Action.png`, `Add Payment Methods.png`, `Edit Payment Methods.png`, `Remove Payment Methods/Default Card.png`, `Remove Payment Methods/Not default card.png`

#### Screen P03.1-S1: Payment Methods List

**Layouts**: `Payment Methods.png` (populated), `Empty.png` (empty state), `Action.png` (action sheet)

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Screen Title | Yes | ✅ | "Payment Methods" |
| Back Navigation | Yes | ✅ | Present |
| Payment Method Cards | Yes | ✅ | 3 cards: Visa, AmEx, Mastercard with brand icons + last 4 |
| Default Badge | Yes | ✅ | "Default" badge on Visa card |
| Per-Card Actions | Yes | ✅ | Action sheet: Set as Default, Edit, Remove |
| Add Payment Method Button | Yes | ✅ | Green CTA at bottom |
| Empty State | Conditional | ✅ | Illustration + "No payment methods saved yet" + CTA |
| Expiry Date on cards | Yes | **❌ MISSING** | Cards show only brand + last 4 — no expiry (MM/YY) |
| Active Obligations Notice | Conditional | **❌ MISSING** | No conditional notice for pending payments |
| Error State | Conditional | **❌ MISSING** | No "Unable to load" with Retry |

**Extra**: Action sheet includes "View detail" — not specified in P03.1-S1.

#### Screen P03.1-S2: Add/Edit Payment Method

**Layouts**: `Add Payment Methods.png`, `Edit Payment Methods.png`

| Field | Required | Add Mode | Edit Mode | Notes |
|-------|----------|----------|-----------|-------|
| Screen Title (dynamic) | Yes | ✅ | **❌ WRONG** | Edit shows "Add Payment Method" instead of "Edit Payment Method" |
| Secure Form Notice | Yes | ✅ | ✅ | Shield icon + encrypted text |
| Card Number Input | Yes | ✅ | **❌ WRONG** | Edit shows full card number editable — must be masked read-only with "Replace card" link (PCI) |
| Cardholder Name | Yes | ✅ | ✅ | Present |
| Expiry Date | Yes | ✅ | ✅ | MM/YY format |
| CVV/CVC | Yes | ✅ | ✅ | Present |
| Billing Address | Yes | ✅ | ✅ | All subfields present |
| Method Nickname | No | **❌** | **❌** | Optional field missing from both forms |
| Set as Default Toggle | Yes | ✅ | ✅ | Present |
| Save Button | Yes | ✅ | ✅ | Correct labels per mode |
| Cancel Button | Yes | **❌** | **❌** | No Cancel button on either form |
| Error States | Conditional | **❌** | **❌** | No field-level or gateway error layouts |

**Extra**: Edit form has a red "Remove" button — not specified on S2 (removal should only trigger from S1 action menu).
**Typo**: Cardholder Name shows "Jonh Doe" — should be "John Doe".

#### Screen P03.1-S3: Remove Payment Method Confirmation Modal

**Layouts**: `Remove Payment Methods/Default Card.png`, `Remove Payment Methods/Not default card.png`

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Warning Icon | Yes | ✅ | Red warning triangle |
| Modal Title | Yes | ⚠️ | "Remove Payment Method" — spec requires question mark |
| Method Summary (card identification) | Yes | **❌ CRITICAL** | Neither modal identifies which card is being removed |
| Warning Message | Yes | ✅ | Correct conditional text per card type |
| Default Reassignment Notice | Conditional | ✅ | Shows reassignment to AmEx on default card removal |
| Remove Button | Yes | ✅ | Red destructive style |
| Go Back Button | Yes | **❌ WRONG** | Shows "Cancel" instead of "Go Back" |

**Flow issue**: Modals overlay the Edit form instead of the List screen — spec says removal triggers from S1 action menu.

---

### Flow P04.1: Passport Submission (Path A)

**Status**: 🔴 No Figma design file received
**Screens required**: 2

> **Placeholder — awaiting Figma design file delivery**

| Screen ID | Screen Name | Key Fields | Layout File | Status |
|-----------|------------|------------|-------------|--------|
| P04.1-S1 | Passport Submission Form | Screen Title, Booking Context Header, Submission Status Badge, Passport Photo Upload section (with preview, guidelines, progress), Personal Information section (Full Name, Date of Birth, Gender, Nationality, Place of Birth), Passport Information section (Passport Number, Issue Date, Expiry Date), Submit Button, Error State | — | 🔴 Missing |
| P04.1-S2 | Passport Details — Read-Only View | Screen Title, Submitted Status Banner, Booking Context Header, Submitted Badge + Timestamp, All fields read-only (masked passport number), Contact Support Button, Back to Booking Button | — | 🔴 Missing |

---

### Flow P04.2: Flight & Hotel Submission (Path B)

**Status**: 🔴 No Figma design file received
**Screens required**: 5

> **Placeholder — awaiting Figma design file delivery**

| Screen ID | Screen Name | Key Fields | Layout File | Status |
|-----------|------------|------------|-------------|--------|
| P04.2-S1 | Travel Requirement Check | Appointment Summary, Prompt Heading, "Yes" button, "No" button | — | 🔴 Missing |
| P04.2-S2 | Flight Information Submission | Screen Title (dynamic: Outbound/Return), Booking Context Header, Leg Type Indicator, Airline Name, Flight Number, Departure/Arrival Airport, Departure/Arrival Date & Time, Ticket Confirmation Number, Ticket Class, Baggage Allowance, Special Requests, Submit Button, Provider Visibility Notice | — | 🔴 Missing |
| P04.2-S3 | Hotel Information Submission | Screen Title, Booking Context Header, Hotel Name, Hotel Address, Check-In/Out Date & Time, Reservation Number, Room Type, Amenities, Transportation Details, Special Requests, Phone Number, Email, Submit Button, Provider Visibility Notice | — | 🔴 Missing |
| P04.2-S4 | Submitted Travel Record — Read-Only | Screen Title (dynamic), Locked Status Banner, Submitted Badge + Timestamp + Submitter, All fields read-only, Contact Support Button, Back to Itinerary Button | — | 🔴 Missing |
| P04.2-S5 | Travel Itinerary View | Screen Title, Booking Context Header, No Travel Required Message (conditional), Package Travel Items (conditional), Outbound/Return Flight sections (conditional), Hotel section (conditional), Awaiting prompts (conditional), Submission Timestamps | — | 🔴 Missing |

---

### Flow P05.1: Day-to-Day Treatment Progress

**Status**: 🟡 Partial — S1 and S3 have layouts with significant gaps; S2 missing entirely
**Screens required**: 3
**Layout files**: `In progress/Treatment.png` (S1), `In progress/End of Treatment.png` (S3)

#### Screen P05.1-S1: Treatment Progress Timeline

**Layout**: `In progress/Treatment.png`

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Case Status Badge | Yes | ✅ | Green "IN PROGRESS" badge |
| Provider / Clinic Name | Yes | **❌ MISPLACED** | On separate "Provider" tab, not on Treatment tab |
| Treatment Name | Yes | ✅ | "Fue Hair Transplant" |
| Package Name | No | ❌ | Not shown (may be acceptable if no package) |
| Assigned Clinician | Yes | ✅ | "Wade Warren" |
| Procedure Date | Yes | **❌ MISSING** | No distinct top-level procedure date field |
| Estimated Graft Count | Yes | ✅ | "Estimate Grafts: 2,000 grafts" |
| Beginning Note | Conditional | ❌ | Not shown (acceptable if none entered) |
| Overall Progress | Yes | ✅ | "1 of 5 days complete" with progress bar |
| Treatment Days List | Yes | ✅ | Days listed with dates — but **no color-coded status badges** per day |
| Journey Timeline | Yes | **❌ MISPLACED** | On "Booking info" tab, not on Treatment tab |

#### Screen P05.1-S2: Day Details Popup — ❌ NOT DESIGNED

No layout exists for this screen. Spec requires a popup showing Day Label, Scheduled Date, Day Description, color-coded Status Badge, and Close action.

#### Screen P05.1-S3: Completed Treatment View

**Layout**: `In progress/End of Treatment.png`

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Case Status Badge ("Completed") | Yes | **❌ WRONG** | Shows "IN PROGRESS" instead of "COMPLETED" |
| Provider / Clinic Name | Yes | **❌ MISSING** | Not on this tab |
| Treatment Name | Yes | **❌ MISSING** | Not on this tab |
| Actual Graft Count | Yes | ✅ | "Actual Graft Count: 1,000 grafts" |
| Estimated Graft Count | Yes | **❌ MISSING** | Only actual shown — spec requires both side-by-side |
| Treatment Summary Note | Yes | ✅ | "Conclusion notes" section |
| Prescription | Yes | ✅ | Present |
| Advice | Yes | ✅ | Present |
| Medication Instructions | Yes | ✅ | Present |
| Before/After Photos | Yes | **❌ MISSING** | No treatment photos section |
| Treatment Days Summary | Yes | **❌ MISSING** | No day-by-day record |
| Journey Timeline | Yes | **❌ MISSING** | Not on this tab |
| **3D Head Scan** | **No — MUST NOT SHOW** | **❌ VIOLATION** | "Final 3D Head scan" is displayed — spec explicitly prohibits showing head scans to patients |

**Structural note**: Screen is implemented as a tab within the In Progress shell rather than a separate dedicated Completed view. This is a navigation-pattern deviation, not by itself a proven spec defect.

---

### Flow P05.2: Previous Treatments List

**Status**: 🟡 Partial — layout present but wrong context and missing fields
**Screens required**: 1
**Layout files**: `Treatment list/My Treatments List.png`, `Treatment list/Sorting.png`

#### Screen P05.2-S1: My Treatments List

**Layout**: `Treatment list/My Treatments List.png`

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Screen Title "My Treatments" | Yes | **⚠️ Wrong** | Shows "Welcome to Hairline / Burak Yılmaz" — this is a home/dashboard, not "My Treatments" |
| Filter Tabs (All / In Progress / Completed / Cancelled) | No | ✅ | All 4 tabs present |
| Search Bar | No | ✅ | Search field present |
| Sort Options | No | ✅ | Sort icon → Most Recent / By Status / By Provider (from `Sorting.png`) |
| Treatment Card — Status Badge | Yes | ✅ | IN PROGRESS (blue), COMPLETED (green), CANCELLED (red) |
| Treatment Card — Provider Name & Avatar | Yes | ✅ | "X Hair Transplant" with provider icon |
| Treatment Card — Description preview | Yes | ✅ | Text preview with ellipsis |
| Treatment Card — Cancellation Reason | No (conditional) | ✅ | "Cancellation Reason:" shown on cancelled card |
| Treatment Card — Leave Review CTA | No (conditional) | ✅ | "Submit review" + "Not now" on completed card |
| Treatment Card — Treatment Name | Yes | **❌ MISSING** | Not shown as separate prominent field |
| Treatment Card — Treatment Dates | Yes | **❌ MISSING** | No start/end dates on cards |
| Treatment Card — Progress Indicator | No (conditional) | **❌ MISSING** | No "Day X of Y" on In Progress cards |
| Treatment Card — Outcome Summary | No (conditional) | **❌ MISSING** | No "2,500 grafts — FUE completed" on Completed cards |
| Empty State | No (conditional) | ❌ | Not shown |

**Issues**:

- ⚠️ Screen title / context is a **home dashboard** ("Welcome to Hairline"), not the "My Treatments" screen accessed from Profile → History. Entry point doesn't match spec.
- ⚠️ Cards show "PATIENT ID: HP202401" — spec says Treatment Name should be prominent, not Patient ID
- ⚠️ CTA text is "Submit review" — spec says "Leave a Review"
- ⚠️ Bottom navigation shows "My list / Notification / Message / Profile" — this is an app-wide home, not the treatments-specific screen

---

### Flow P05.3: Submitted Reviews List

**Status**: 🟢 Good — all screens covered with useful state variants
**Screens required**: 2
**Layout files**: `My Reviews.png`, `Review Detail.png`, `Review Detail - Edit.png`, `Review Detail - Removed.png`, `Review Detail - Takedown Request.png`

#### Screen P05.3-S1: My Reviews List

**Layout**: `Profile > My reviews/My Reviews.png`

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Screen Title | Yes | ✅ | "My Reviews" |
| Sort Options | Yes | ✅ | Sort icon in header |
| Review Card — Treatment Name | Yes | ✅ | "Treatment: Fue Hair Transplant" |
| Review Card — Provider Name & Avatar | Yes | ✅ | "X Hair Transplant" with avatar |
| Review Card — Overall Star Rating | Yes | ✅ | Star ratings shown |
| Review Card — Review Date | Yes | ✅ | "5 days ago" |
| Review Card — Review Excerpt | Yes | ✅ | Truncated text with "See more" |
| Review Card — Status Badge | Yes | ⚠️ | Shows "Published", "Submitted", "Removed" — **"Submitted" is not in spec** (spec defines only Published / Removed by Admin) |
| Empty State | Conditional | ❌ | Not shown |

#### Screen P05.3-S2: Review Detail View

**Layouts**: Published (`Review Detail.png`), Removed (`Review Detail - Removed.png`), Edit (`Review Detail - Edit.png`), Takedown (`Review Detail - Takedown Request.png`)

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Treatment Name | Yes | ✅ | Present |
| Provider Name & Avatar | Yes | ✅ | Present |
| Overall Star Rating | Yes | ✅ | Present |
| Category Ratings (4 sub-ratings) | Yes | ✅ | Facility / Staff / Results / Value all shown |
| Review Text | Yes | ✅ | Full text visible |
| Review Submission Date | Yes | ✅ | "5 days ago" |
| Review Photos | Yes | ✅ | Photo thumbnail present |
| Status Badge | Yes | ✅ | "Published" / "Removed" correctly differentiated |
| Admin Removal Reason | Conditional | ✅ | Shown prominently on Removed variant |
| Provider Response | Conditional | ❌ | Not visible (may be acceptable if no response exists) |
| Edit Review action | Conditional | ✅ | Visible on Published, correctly hidden on Removed |
| Request Takedown action | Conditional | ✅ | Present as "Takedown Request" button (word order differs from spec) with confirmation modal + 7-year retention notice |
| Back Navigation | Yes | ✅ | Present |

**Extra state variants** (Edit form, Takedown modal) are reasonable UX additions beyond the 2 spec screens.

---

### Flow P06.1: Notification Listing & Bubble

**Status**: 🟡 Partial — bubble component fully covered; list screen has interaction pattern differences and missing elements
**Screens required**: 2
**Layout files**: `Notification - Having unread notification.png`, `Notification - Not any unread notification.png`, `Notification - Very high counts unread notification.png`, `Notification list.png`, `Notification list - Filter.png`, `Notification list - Apply Filter.png`, `Notification categories.png`

#### Screen P06.1-S1: Notification Bubble Component — FULLY COMPLIANT

**Layouts**: 3 state variants covering all spec requirements.

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Bell Icon | Yes | ✅ | Bell in bottom nav bar |
| Unread Count Badge | Yes | ✅ | Red numeric badge |
| Badge hidden when count = 0 | Yes | ✅ | No badge in "Not any unread" variant |
| "99+" cap | Yes | ✅ | "99+" shown in high-count variant |
| New Notification Pulse | Yes | N/A | Cannot verify animation from static layout |

#### Screen P06.1-S2: Notification List Screen

**Layouts**: `Notification list.png`, `Notification list - Filter.png` (bottom sheet), `Notification list - Apply Filter.png` (active filter state)

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Screen Title | Yes | ✅ | "Notifications" |
| Back Navigation | Yes | **⚠️ PATTERN DIFFERS** | No back arrow — layout treats Notifications as a bottom-nav destination rather than a pushed screen |
| Search Bar | Yes | ✅ | Present below title |
| Mark All as Read | Conditional | **❌ MISSING** | Not visible anywhere |
| Filter Chips (inline) | Yes | **⚠️ PATTERN DIFFERS** | Spec requires inline horizontal chips; layout uses filter icon → bottom sheet modal. Categories match (All, Unread, Inquiry, Quote, Booking, Payment, Treatment, Aftercare, Account, Messaging). |
| Date Group Headers | Yes | **❌ MISSING** | No "Today", "Yesterday", "This Week", "Earlier" separators |
| Notification Card — Category Icon | Yes | ✅ | Color-coded icons per category |
| Notification Card — Title | Yes | ✅ | Bold titles shown |
| Notification Card — Message Preview | Yes | ✅ | 1-2 line preview |
| Notification Card — Timestamp | Yes | ✅ | Relative timestamps ("an hour ago", "3 days ago") |
| Notification Card — Read/Unread Indicator | Yes | **⚠️ PARTIAL** | Bold text for unread but no blue dot or background highlight per spec |
| Swipe Actions | Yes | **⚠️ PATTERN DIFFERS** | Three-dot overflow menu replaces swipe actions |
| Empty State | Conditional | ❌ | Not shown |

**Extra**: `Notification categories.png` defines 12 category icons (spec lists 8 patient-facing). Extra categories (Billing/Payouts, Reviews, Promotions, Provider/Compliance, System/Operations) may be admin/provider-only.

---

### Flow P08.1: Help & Support

**Status**: 🔴 No Figma design file received
**Screens required**: 5

> **Placeholder — awaiting Figma design file delivery**

| Screen ID | Screen Name | Key Fields | Layout File | Status |
|-----------|------------|------------|-------------|--------|
| P08.1-S1 | Help & Support Hub | Screen Title, Search Bar, Browse Help Center link, Contact Support link, My Support Tickets link (with badge count), Emergency Contact Section (phone + email) | — | 🔴 Missing |
| P08.1-S2 | Help Center Browser | Screen Title, Search Bar, Content Type Cards (FAQs, Articles, Resources, Videos), Featured/Popular Articles, FAQ Topic Sections (accordion), Article Subtype Filter, Article Detail (with "Was this helpful?" + Related Articles), Resource Detail (file preview + download), Video Detail (embedded player + transcript link) | — | 🔴 Missing |
| P08.1-S3 | My Support Tickets | Screen Title, Create New Ticket Button, Filter Chips (All/Open/In Progress/Resolved/Closed), Ticket Cards (Case ID, Title, Status Badge, Priority Badge, Submitted Date, Last Updated), Empty State | — | 🔴 Missing |
| P08.1-S4 | Ticket Detail View | Screen Title, Case ID, Status Badge, Priority Badge, Case Category, Submitted Date, Auto-Closure Countdown (Resolved only), Resolution Summary, Communication Thread (sender + body + timestamp + attachments), Reply Input Field (Open/In Progress/Resolved), Attachment Button, Send Reply Button, Closed Case Banner | — | 🔴 Missing |
| P08.1-S5 | Contact Support Form | Screen Title, Case Title, Category Picker (with inline descriptions), Description, Priority Picker (with self-triage descriptions), Attachments, Submit Button, Cancel/Discard | — | 🔴 Missing |

---

## Flow Integrity Check

For flows with layouts, does the navigation/flow work as specified?

| Flow | Spec Flow | Layout Flow | Verdict |
|------|-----------|-------------|---------|
| P01.1 | Profile → Delete Account → Warning → Re-auth → Confirmation | Warning → Conditional states → Verify Identity → Confirmation all present | **⚠️ Flow mostly works** — password field wrong type on S2; lockout handling is not evidenced as a distinct UI state |
| P01.2 | Profile → Settings → sub-screens → back | All 5 sub-screens present with back navigation | **✅ Flow works** |
| P01.3 | Privacy & Security → Change Password → Confirmation | Form → Confirmation with 3 state variants | **✅ Flow works** |
| P02.1 | Dashboard → Select ≥2 quotes → Comparison panel renders **inline** | Separate "Compare Offers Table" screen | **❌ Flow deviation** — spec says inline panel, layout is separate screen |
| P02.2 | Inquiry Detail → Cancel action → Confirmation Modal → (blocked: error modal) → (allowed: submit) → Success | All 3 states present with correct transitions | **✅ Flow works** |
| P02.3 | Dashboard with expired badges → All Expired state → Cancel Inquiry or Contact Support | All Expired banner shown but **no Cancel Inquiry CTA and no distinct Contact Support CTA** — recovery path is weak/dead-end | **❌ Flow broken** — no explicit recovery CTA from All Expired state |
| P02.4 | Quote Detail → Tap legal link → Document Viewer → Back to Quote Detail | Cancellation Policy viewer present with back nav | **⚠️ Flow partial** — only 1 of 3 document types designed |
| P03.1 | Profile → Payment Methods → List → Add/Edit/Remove | All screens present but **Remove modal overlays Edit form** instead of List | **⚠️ Flow deviation** — removal flow incorrectly routed through Edit screen |
| P05.1 | Open case → Treatment Timeline → Tap day → Popup; Completed → Summary | Timeline tab present, Completed tab present, **Day Popup missing entirely** | **❌ Flow broken** — day tap leads nowhere |
| P05.2 | Profile → History → My Treatments → Tap card → Detail | Layout is a home dashboard, not Profile-accessed screen | **⚠️ Flow context wrong** — entry point mismatch |
| P05.3 | Profile → My Reviews → List → Detail (Published/Removed) | All states covered including Edit and Takedown | **✅ Flow works** |
| P06.1 | Bell icon (any screen) → Notification List → Tap → deep link | Bubble + List present, filter via bottom sheet | **⚠️ Flow mostly works** — list behaves like a bottom-nav destination, so back navigation is a pattern deviation rather than a hard missing element |

---

## Priority Action Items

### Critical (Highest Priority)

| # | Item | Flow | Detail |
|---|------|------|--------|
| 1 | Design 3 missing flows | P04.1, P04.2, P08.1 | 12 screens with no delivered Figma design files |
| 2 | **Remove 3D Head Scan from Completed view** | P05.1-S3 | **Spec violation** — head scans must NOT be shown to patients; replace with Before/After treatment photos |
| 3 | **Fix password field on Identity Verification** | P01.1-S2 | Shows "Email address" field instead of masked password input |
| 4 | Design P05.1-S2 Day Details Popup | P05.1 | No layout exists — flow dead-ends on day tap |
| 5 | Clarify disabled state styling on expired quotes **in list view** | P02.3 | Expired cards are muted, but the Accept state is visually ambiguous in static layouts. Make the disabled state unmistakable in list view. |
| 6 | Add Cancel Inquiry CTA to All Expired state | P02.3 | Currently a dead-end with no way to proceed |
| 7 | Fix Edit Payment Method — card number must be masked | P03.1-S2 | Full card number shown as editable — PCI compliance violation |
| 8 | Fix Edit Payment Method title | P03.1-S2 | Shows "Add Payment Method" instead of "Edit Payment Method" |
| 9 | Add card identification to Remove modal | P03.1-S3 | Neither modal shows which card is being removed |

### High (Required Fields Missing)

| # | Item | Flow | Detail |
|---|------|------|--------|
| 10 | Add Expiry Timer to quote cards | P02.1 | No countdown timer visible — required by FR-005 |
| 11 | Fix comparison panel as inline (not separate screen) | P02.1 | Spec says conditional panel within dashboard, not separate view |
| 12 | Add "Go Back" button on Delete Account Warning | P01.1-S1 | Only back arrow exists — spec requires secondary CTA |
| 13 | Add "Cancel" button on Identity Verification | P01.1-S2 | Only back arrow exists — spec requires secondary CTA |
| 14 | Fix OTP instruction text "4 digit" → "6-digit" | P01.1-S2 | Contradicts 6 input boxes and spec requirement |
| 15 | Change Verify button to red/destructive style | P01.1-S2 | Currently green — spec requires red |
| 16 | Fix Completed Treatment View badge | P05.1-S3 | Shows "IN PROGRESS" instead of "COMPLETED" |
| 17 | Add missing fields to Completed Treatment View | P05.1-S3 | Missing: Estimated Graft Count, Before/After Photos, Treatment Days Summary, Journey Timeline, Provider Name, Treatment Name |
| 18 | Add day status badges to Treatment Timeline | P05.1-S1 | No color-coded badges (grey/blue/green/amber/red) on day rows |
| 19 | Add Journey Timeline to Treatment tab | P05.1-S1 | Currently on Booking info tab only |
| 20 | Add Impact Summary field | P02.2-S1 | Must show "X active quotes will be cancelled" dynamically |
| 21 | Add expired state detail fields | P02.3-S2 | Missing: Icon, Inquiry Summary, Expired Quotes Count, Last Expiry Date, Contact Support Link |
| 22 | Fix My Treatments List context | P05.2 | Must be "My Treatments" from Profile, not home dashboard |
| 23 | Add Treatment Name, Dates, Progress Indicator, Outcome Summary to cards | P05.2-S1 | Multiple required card fields missing |
| 24 | Complete comparison differentiators | P02.1 | Missing or not normalized: soonest appointment slot and provider credentials summary; review rating/count is visible in provider headers but not as a dedicated row |
| 25 | Add Mark All as Read button | P06.1-S2 | Required conditional element missing |
| 26 | Add Date Group Headers | P06.1-S2 | "Today", "Yesterday", "This Week", "Earlier" separators missing |
| 27 | Add expiry date (MM/YY) to payment method cards | P03.1-S1 | Required field missing from card list |
| 28 | Add Explanation Text to Notification Settings | P01.2-S2 | "Choose how you want to receive notifications from Hairline." missing |
| 29 | Fix Remove modal overlay context | P03.1-S3 | Modals overlay Edit form — should overlay List screen per flow |
| 30 | Fix Remove modal dismiss label | P03.1-S3 | "Cancel" should be "Go Back" per spec |

### Medium (Text Corrections & Polish)

| # | Item | Flow | Detail |
|---|------|------|--------|
| 31 | Fix CTA label "Delete your account" → "Request Deletion" | P01.1-S1 | Label implies immediate deletion; should indicate request |
| 32 | Fix placeholder "Turkish Airlines" on Request Reference | P01.1-S3 | Dummy data — needs realistic DSR reference ID |
| 33 | Fix typo "Request Detailed" → "Request Details" | P01.1-S3 | Typo in section header |
| 34 | Clarify lockout/rate-limit handling on Identity Verification | P01.1-S2 | Flow diagram includes a lockout state, but current layouts do not evidence a distinct non-retryable UI state |
| 35 | Align label casing on Settings Main | P01.2-S1 | "Notification settings" → "Notification Settings"; "Privacy and security" → "Privacy & Security" |
| 36 | Clarify "Submitted" review status | P05.3-S1 | Not in spec — may contradict "immediate publish" business rule |
| 37 | Add Read/Unread blue dot indicator | P06.1-S2 | Only bold text used — spec requires blue dot + background highlight |
| 38 | Fix label "Cancellation Reason" → "Why are you cancelling?" | P02.2-S1 | Label text mismatch |
| 39 | Fix option "Found a better option" → "Found a better option elsewhere" | P02.2-S1 | Text mismatch |
| 40 | Replace lorem ipsum in error state | P02.2-S1 error | Placeholder body text needs real copy |
| 41 | Add "What would you like to do next?" header | P02.2-S2 | Missing Next Steps Section Label |
| 42 | Design Privacy Commitment + Terms of Service variants | P02.4 | Reusable viewer needs all 3 title variants |
| 43 | Fix CTA "Submit review" → "Leave a Review" | P05.2-S1 | Text mismatch |
| 44 | Fix typo "Slect date" → "Select date" | P02.1 Filter | Typo in filter panel |
| 45 | Replace TOC placeholder text | P02.4 | "Table of Contents item" repeated — needs real or representative content |
| 46 | Add Cancel button to Add/Edit Payment forms | P03.1-S2 | No Cancel/discard button on either form |
| 47 | Decide on filter pattern: inline chips vs bottom sheet | P06.1-S2 | Spec says inline chips; layout uses bottom sheet modal |
| 48 | Fix typo "Jonh Doe" → "John Doe" | P03.1-S2 | Cardholder Name placeholder in Edit mode |
| 49 | Fix button label "Takedown Request" → "Request Takedown" | P05.3-S2 | Word order differs from spec |

---

## Appendix: Spec Cross-Reference

| Spec Section | Spec Screen Count | Layouts Present | Gap | Field Coverage |
|--------------|------------------|-----------------|-----|----------------|
| P-01: Auth & Profile Management (P01.1, P01.2, P01.3) | 10 screens | 10 (all covered) | 0 screens | ~85% (P01.1 has issues on S2; P01.2-S2 missing explanation text) |
| P-02: Quote Request & Management (P02.1, P02.2, P02.3, P02.4) | ~7 screens | ~7 (partial) | ~0 (field gaps) | ~65% (expired states weak; comparison missing rows) |
| P-03: Booking & Payment (P03.1) | 3 screens | 3 (all covered) | 0 screens | ~60% (Edit mode PCI issues; Remove modal missing card ID) |
| P-04: Travel & Logistics (P04.1, P04.2) | 7 screens | 0 | 7 | — |
| P-05: Aftercare & Progress (P05.1, P05.2, P05.3) | 6 screens | 5 (S2 popup missing) | 1 | ~60% (P05.1-S3 has spec violation; P05.2 wrong context) |
| P-06: Communication (P06.1) | 2 screens | 2 (all covered) | 0 screens | ~70% (missing date groups and Mark All as Read; back navigation is implemented as a tab-pattern variation) |
| P-08: Help Center (P08.1) | 5 screens | 0 | 5 | — |
| **Total** | **~47 screens** | **~35** | **~12** | **~70% average** |
