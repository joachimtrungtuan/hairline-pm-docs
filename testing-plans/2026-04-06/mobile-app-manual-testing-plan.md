# Mobile App (Patient) — Manual Testing Plan

**Date:** 2026-04-06
**Scope:** API Integration & UI Development for complementary flows (Milestone: Missing Mobile Flows)
**Platform:** Android APK on physical device
**Test Type:** Manual (scripted walkthrough)
**Purpose:** Detect functional defects, UX/interaction errors, and data fetching/rendering issues before the next phase
**Source Reference:** `local-docs/reports/2026-02-05/missing-mobile-flows-design-complement.md`
**Previous Testing Round:** `local-docs/reports/2026-03-30/manual-testing-status-missing-mobile-flows-design-complement.md`

---

## Regression & Recheck Items (from 2026-03-30 round)

This build also requires rechecking items from the previous testing round. The table below summarizes what needs re-verification and why.

| Flow | Previous Status | Recheck Reason | What to Verify |
|------|----------------|----------------|----------------|
| P01.1 Delete Account | Approved | Error states not reproduced | **RC-01:** Reproduce blocking state (active treatment/payment), error/rate-limit states during identity verification |
| P01.2 Settings | Approved | External browser behavior for legal content | **RC-02:** Confirm Privacy Policy and Terms & Conditions still open correctly (previously via external browser — check if now in-app) |
| P01.3 Change Password | Approved | Regression check | **RC-03:** Verify change password flow and "Forgot your password?" link still work |
| P02.1 Compare Offers | Pending (blocked) | Was blocked by `ParseFailure` | **RC-04:** Recheck if quote creation now works; verify side-by-side comparison UI |
| P02.3 Expired Offers/Quotes | Needs Further Checking | Expired-quote states not evidenced | **RC-05:** Check if expired-quote indicators (P02.3-S1, P02.3-S2) are now present |
| P03.1 Payment Methods | Approved | Nickname display bug | **RC-06:** Verify if method nickname now displays on list (was showing card brand instead) |
| P04.1 Passport Submission | Pending (blocked) | Was blocked by `ParseFailure` | **RC-07:** Now covered in TC-M-007; verify full passport submission flow |
| P04.2 Flight & Hotel | Pending (blocked) | Was blocked by `ParseFailure` | **RC-08:** Now covered in TC-M-007; verify full flight + hotel submission flow |
| P05.1 Day-to-Day Treatment Progress | Pending (blocked) | Was blocked by `ParseFailure` | **RC-09:** Verify treatment progress timeline, day details popup, completed view |
| P05.2 Previous Treatments List | Approved | Empty state not verified | **RC-10:** Verify empty state displays correctly when no treatments exist |
| P05.3 My Reviews | Approved | Regression check | **RC-11:** Confirm list, detail, edit, takedown, load-more still work |
| P06.1 Notifications | Needs Further Checking | Swipe actions not verified | **RC-12:** Verify swipe-left reveals "Mark as Read" / "Archive" actions |
| P08.1 Help & Support | Needs Further Checking | Screen did not match spec | **RC-13:** Check if hub is now "Help & Support" (not "Support Team"); verify hub structure: search, Help Center, Contact Support, My Support Tickets, emergency contacts |

### `ParseFailure` Blocker (from previous round)

The previous round identified a `duration_of_concern` schema compatibility issue causing `ParseFailure` on quote creation. This blocked verification of P02.1, P04.1, P04.2, and P05.1. **This round must confirm whether this issue is resolved.** If it persists, mark affected test cases as blocked and document in the defect log.

---

## Build Scope

### API Integration (data flows end-to-end)

| Module | Flow Reference |
|--------|---------------|
| Notifications | P06.1 — Notification Listing & Bubble |
| Profile > Settings | P01.2 — Settings Screen |
| Profile > My Reviews | P05.3 — Submitted Reviews List |
| Profile > Payment Methods | P03.1 — Payment Methods Management |
| Profile > Delete Account | P01.1 — Delete Account (includes Verify Identity step) |

### UI Development (screens present, may not be fully functional)

| Module | Flow Reference |
|--------|---------------|
| Help & Support | P08.1 — Help & Support Hub, Help Center, Tickets, Contact Form |
| Travel & Logistics | P04.1 — Passport Submission, P04.2 — Flight & Hotel Submission |

### Temporary Navigation Note (from dev team)

> Because API integration for certain modules is incomplete, their UI isn't directly accessible through the normal app flow. Temporary placement:
> - **Passport, Hotel & Flight submission screens** → accessible from the **"Confirmed" view** in the bookings/inquiries section
> - **Travel Itinerary screen** → accessible from the **"In Progress" view**

---

## Test Environment

| Item | Detail |
|------|--------|
| Device | Android phone (physical) |
| Build | APK (provided by mobile dev team) |
| Backend | Staging / dev server (confirm URL with dev team before testing) |
| Test account | Create fresh — sign up or use seeded credentials from dev team |
| Data | Input from scratch during testing |

### Before You Start

- [ ] APK installed and launches without crash
- [ ] Can sign in / sign up successfully
- [ ] App loads home screen with bottom navigation visible
- [ ] Network connection is stable

---

## Test Scenarios

### Legend

| Symbol | Meaning |
|--------|---------|
| **[CHECK]** | Verify visually or by interaction |
| **[DATA]** | Verify data fetches/renders correctly |
| **[ACTION]** | Perform an action and observe result |
| **Pass / Fail / Partial / N/A** | Result per step |
| **Severity: Critical / Major / Minor / Cosmetic** | For any defect found |

---

### TC-M-001: Notifications — Bell Icon & List

**Goal:** Verify notification bubble renders, list loads, and basic interactions work.
**Flow:** P06.1

> Current known build state: the notification entry point is currently shown in the **bottom navigation bar**, not the top navigation bar assumed in the original draft of this plan. The screen opens successfully, but the backend is not yet returning notification data, so only empty-state/UI-shell validation is currently possible.

| # | Step | Expected Result | Result | Notes |
|---|------|-----------------|--------|-------|
| 1 | From any main screen, **[CHECK]** the notification entry point in app navigation | Notification entry point is visible and reachable from the main app shell | Pass | Present as an icon in the bottom navigation bar, not the top nav as originally assumed |
| 2 | **[CHECK]** if there is an unread count badge on the notification entry point | Badge shows count if unread notifications exist; hidden if 0 | N/A | Could not verify unread-count behavior because backend is not yet returning notifications |
| 3 | **[ACTION]** Tap the notification entry point | Notification List screen opens successfully | Pass | Screen opens successfully |
| 4 | **[CHECK]** screen layout: search bar, filter control, notification cards or empty state | Available UI elements are present and properly laid out for the current data state | Pass | Search bar and filter are present; backend currently returns no notifications, so empty state is shown instead of cards |
| 5 | **[CHECK]** filter control is visible | Notification filtering control is present and accessible | Pass | Filter control is visible, but filter behavior cannot be validated without notification data |
| 6 | **[ACTION]** Tap different filter chips / filter options | List filters accordingly; "All" shows everything | N/A | Filtering behavior not testable yet because no notification items are returned |
| 7 | **[ACTION]** Tap a notification card (if any exist) | Card visually marks as read (blue dot disappears, background changes); navigates to linked content if applicable | N/A | No notification items are currently returned by the backend, so card interaction cannot be tested |
| 8 | **[CHECK]** each notification card shows: category icon, title, message preview, timestamp, read/unread indicator | All fields render without clipping or overflow | N/A | No notification cards are currently available to inspect because the backend returns an empty state |
| 9 | **[ACTION]** Pull down to refresh | Loading indicator appears; list refreshes | Fail | Pull-down to refresh is currently missing on the notification list |
| 10 | **[ACTION]** Scroll to bottom of list | Pagination loads more items (or empty state if no more) | N/A | Pagination path cannot be tested because the notification list is empty |
| 11 | **[ACTION]** If "Clear Read" / "Mark All as Read" is visible, tap it | Bulk actions are visible when expected and, once data exists, should update read state accordingly | N/A | "Clear Read" and "Mark All as Read" are present in the UI, but action behavior cannot be validated without notification data |
| 12 | **[ACTION]** Tap back arrow | Returns to previous screen | Pass | Notification screen can be exited normally via back navigation |
| 13 | If list is empty: **[CHECK]** empty state message | Appropriate empty state shown (e.g., "No notifications yet") | Pass | Empty state shown: "No notifications yet" |

---

### TC-M-002: Profile > Settings

**Goal:** Verify Settings navigation, notification preferences, and legal content screens.
**Flow:** P01.2

| # | Step | Expected Result | Result | Notes |
|---|------|-----------------|--------|-------|
| 1 | Navigate to **Profile** tab, then tap **Settings** | Settings Main Screen loads with title "Settings" | Pass | Settings screen opens successfully |
| 2 | **[CHECK]** navigation rows: Notification Settings, Privacy & Security, Terms & Conditions, Help & Support | All 4 rows visible with icons and chevrons | Pass | All 4 rows are present as expected in docs |
| **Notification Settings** | | | | |
| 3 | **[ACTION]** Tap "Notification Settings" | Screen loads with title "Notification Settings" | Pass | Notification Settings screen opens successfully |
| 4 | **[CHECK]** Global Email toggle and Global Push toggle are present with ON/OFF states | Both toggles visible; should reflect current preference | Pass | Both Email Notifications and Push Notifications toggles are present |
| 5 | **[ACTION]** Toggle Email Notifications OFF then ON | Toggle animates; brief "Saved"/"Saving..." feedback appears; no crash | Fail | Success toast appears, but the toggle state does not actually change/persist |
| 6 | **[ACTION]** Toggle Push Notifications OFF then ON | Same as above | Fail | Success toast appears, but the toggle state does not actually change/persist |
| 7 | **[CHECK]** mandatory notifications note and system event notifications note are displayed | Informational text present below toggles | Pass | Informational notes are displayed below the two toggles |
| 8 | **[ACTION]** Tap back | Returns to Settings Main Screen | Pass | Both the in-app back button and the Android hardware back button return correctly to Settings Main Screen |
| **Privacy & Security** | | | | |
| 9 | **[ACTION]** Tap "Privacy & Security" | Screen loads with "Change Password" and "Privacy Policy" rows | Pass | Privacy & Security screen opens successfully |
| 10 | **[ACTION]** Tap "Privacy Policy" | Privacy Policy content opens correctly | Pass | Opens in the phone's external browser; this behavior is confirmed as aligned between client and dev team |
| 11 | **[DATA]** Check policy content renders | Text is readable, scrollable, no blank screen or loading stuck | Pass | Content renders in the external browser without blank/error state |
| 12 | **[ACTION]** Tap back to Privacy & Security, then back to Settings | Navigation stack works correctly | Pass | Back navigation works correctly; the Settings item screens can be exited using either the in-app back button or the Android hardware back button |
| **Terms & Conditions** | | | | |
| 13 | **[ACTION]** Tap "Terms & Conditions" | Terms content opens correctly | Pass | Opens in the phone's external browser; this behavior is confirmed as aligned between client and dev team |
| 14 | **[DATA]** Check content renders | Text is readable, no blank/error state | Pass | Content renders in the external browser without blank/error state |
| 15 | **[ACTION]** Tap back | Returns to Settings | Pass | Both the in-app back button and the Android hardware back button return correctly to Settings Main Screen |
| **Help & Support link** | | | | |
| 16 | **[ACTION]** Tap "Help & Support" from Settings | Navigates to Help & Support Hub (tested in TC-M-006) | | |
| 17 | **[ACTION]** Tap back | Returns to Settings | Pass | Both the in-app back button and the Android hardware back button return correctly to Settings Main Screen |

---

### TC-M-003: Profile > My Reviews

**Goal:** Verify reviews list loads, cards render, and detail view works.
**Flow:** P05.3

| # | Step | Expected Result | Result | Notes |
|---|------|-----------------|--------|-------|
| 1 | Navigate to **Profile** → **My Reviews** | "My Reviews" screen loads | Pass | My Reviews screen loads and shows the full review list, average star score, and total review count |
| 2 | **[CHECK]** if reviews exist: sort options visible (Most Recent / Rating High→Low / Rating Low→High) | Sort control is present | Fail | Sorting control/function is currently missing from the My Reviews list |
| 3 | If no reviews: **[CHECK]** empty state | Message like "No reviews yet" is displayed | Pass | Empty state is present with the message `No reviews yet` |
| 4 | **[DATA]** If reviews exist, check each card shows: treatment name, provider name & avatar, star rating, date, excerpt, status badge | All fields render correctly, no missing data or broken images | Pass | Each review shows star rating, posted date, status (Published or Removed), and the provider being reviewed |
| 5 | **[ACTION]** Tap a sort option | List reorders accordingly | N/A | Cannot execute because no sorting control/function is available on the My Reviews list |
| 6 | **[ACTION]** Tap a review card | Review Detail View opens | Pass | Review detail opens successfully when a review is tapped |
| 7 | **[CHECK]** detail view shows: treatment name, provider info, overall star rating, category ratings (Facility/Staff/Results/Value), full review text, submission date, status badge | All fields present and properly formatted | Pass | Detail view shows the rating breakdown, detailed review content, and edit action |
| 8 | **[CHECK]** if review photos exist, they display in gallery | Photos load, support swipe/zoom | Partial | Review flow has a photos area in edit mode, but the initial completed-case submit-review screen does not provide an image-upload control, so the end-to-end review photo flow is incomplete |
| 9 | **[CHECK]** if status is "Published": Edit Review and Request Takedown buttons visible | Buttons are present | Partial | Edit Review and Request Takedown are both available; request takedown can be submitted successfully. Edit Review still has 2 bugs: saving gets stuck in a long-running loading state and unsaved changes are lost after reopening; changing one rating criterion also forces the other criteria to change together. Additional review-flow context: the completed-case submit-review screen has no image-upload control and is not aligned with the edit-review screen layout |
| 10 | **[CHECK]** if provider response exists, it's shown | Response text and timestamp render correctly | | |
| 11 | **[ACTION]** Tap back | Returns to My Reviews list | Pass | Back navigation from My Reviews returns correctly to the Profile screen |

---

### TC-M-004: Profile > Payment Methods

**Goal:** Verify payment methods list, add/edit/remove flows, and data persistence.
**Flow:** P03.1

| # | Step | Expected Result | Result | Notes |
|---|------|-----------------|--------|-------|
| **Empty State** | | | | |
| 1 | Navigate to **Profile** → **Payment Methods** | Screen loads with title "Payment Methods" | Pass | Screen opens correctly with the title `Payment Methods` |
| 2 | **[CHECK]** if no methods saved: empty state illustration + "Add Payment Method" CTA | Empty state displays correctly | Pass | Empty state is present with illustration/text and `Add Payment Method` CTA when no cards are saved |
| **Add Payment Method** | | | | |
| 3 | **[ACTION]** Tap "Add Payment Method" | Add Payment Method form opens | Pass | Embedded payment gateway form opens correctly |
| 4 | **[CHECK]** form fields: card number, cardholder name, expiry date, CVV, optional billing address, nickname, "Set as default" toggle | All fields present with proper input types | Partial | Observed gateway form shows card number, expiry/CVC, billing region/ZIP, Link option, setup action, and `Set as default` toggle; cardholder name and nickname were not confirmed from the captured add-card form in this round |
| 5 | **[CHECK]** secure form notice ("Your payment details are secured and encrypted") is visible | Trust indicator displayed | Pass | Secure embedded Stripe/Link-style payment sheet and payment/legal notice are visible |
| 6 | **[ACTION]** Enter valid card details and tap "Save Payment Method" | Card saves; returns to Payment Methods List showing the new card | Pass | Test card can be added successfully and success toast is shown |
| 7 | **[DATA]** Verify the saved card shows: brand icon, masked last 4 digits, expiry, "Default" badge (if first card) | All data renders correctly | Pass | Brand icon, masked last 4 digits, and `Default` badge are visible on the saved-card list item; expiry is visible in Payment Method Details, and expired-card add attempts are blocked by Stripe gateway validation |
| **Validation** | | | | |
| 8 | **[ACTION]** Tap "Add Payment Method" again; leave fields empty and tap Save | Field-level validation errors shown (inline, specific per field) | Pass | Stripe-managed gateway form prevents empty submission and shows inline validation errors on required fields |
| 9 | **[ACTION]** Enter expired expiry date, tap Save | Error: expiry date must be current or future | Pass | Expired-card validation is enforced by the Stripe gateway layer, so expired cards cannot be added; this behavior is treated as pass for this round |
| **Card Management** | | | | |
| 10 | Add a second payment method (repeat steps 3–6) | Second card appears in list | Pass | Adding second and third payment methods works successfully |
| 11 | **[ACTION]** On the non-default card, tap "Set as Default" | Default badge moves to the selected card | Pass | `Set as Default` works from the three-dot context menu on each saved card |
| 12 | **[ACTION]** Tap "Edit" on a card | Edit form opens with pre-filled editable fields (nickname, billing address); card number shown as masked read-only | Partial | Payment Method Details opens and shows masked card data plus editable metadata fields; the `Set as default payment method` switch in Edit also works, but Method Nickname save still does not persist even though success toast appears |
| 13 | **[ACTION]** Tap "Remove" on a card | Remove Confirmation Modal appears with card summary and warning message | Pass | Remove confirmation modal appears correctly |
| 14 | **[CHECK]** modal shows correct card (brand + last 4 digits) | Card identification is accurate | Pass | For non-default cards, the remove modal does not show last 4 digits and this is accepted; for default-card removal, the modal includes reassignment messaging and identifies the replacement card using last 4 digits, which is also accepted |
| 15 | **[ACTION]** Tap "Remove" to confirm | Card removed; list updates; if removed card was default, default auto-reassigns | Pass | Removing saved cards works; when the default card is removed, default is reassigned to another saved card as warned |
| 16 | **[ACTION]** Tap "Go Back" on the modal instead | Modal dismisses, no changes | Pass | Tapping `Cancel` closes the remove modal and cancels the delete action as expected |

---

### TC-M-005: Profile > Delete Account (includes Verify Identity)

**Goal:** Verify the delete account flow end-to-end: warning screen, identity verification, confirmation.
**Flow:** P01.1

| # | Step | Expected Result | Result | Notes |
|---|------|-----------------|--------|-------|
| **Warning Screen** | | | | |
| 1 | Navigate to **Profile** → **Delete Account** (or equivalent path) | Delete Account Warning Screen loads with title "Delete Your Account" | Pass | Delete Account flow is reachable from `Profile > Delete Account` |
| 2 | **[CHECK]** warning icon, consequences list, retained data explanation, processing timeline notice | All informational sections render correctly | Pass | Warning icon, consequences list, retained-data explanation, and processing timeline notice are all present as expected |
| 3 | **[CHECK]** "Request Deletion" button (red/destructive style) and "Go Back" button | Both CTAs visible with correct styling | Pass | `Request Deletion` and `Go Back` buttons are both present with the expected styling/behavior |
| 4 | **[CHECK]** if blocking conditions exist (active treatment/payment): blocking message displayed, Request Deletion disabled | Blocking message is clear; includes "Contact Support" link | Pass | Blocking-condition coverage is accepted as pass for this round: accounts in active-treatment / pending-payment blocking states are treated under the same delete-flow restriction and cannot proceed |
| 5 | **[CHECK]** optional deletion reason selector | Dropdown/picker present; submission not blocked if left empty | Pass | Deletion reason selector is present on the confirm-reason step; current behavior requires a selected reason before proceeding, and this is accepted for the current build |
| **Identity Verification** | | | | |
| 6 | **[ACTION]** Tap "Request Deletion" (assuming no blocking conditions) | Identity Verification screen loads (or final confirmation if re-auth not required) | Pass | After the reason-confirm step is completed, the flow proceeds to Verify Identity |
| 7 | **[CHECK]** screen title "Verify Your Identity", security icon, instruction text | All elements present | Pass | `Verify Your Identity` title, security icon, and instruction text are all present as expected |
| 8 | **[CHECK]** verification method selector: "Password" and "Email OTP" chips | Both options available; tapping switches the input field | Pass | User can choose between password verification and email OTP verification |
| 9 | **[ACTION]** Select "Password" → enter correct password → tap "Verify" | Verification succeeds; proceeds to final confirmation modal | Pass | Password verification succeeds correctly; `Forgot password` is available from this step; successful password verification proceeds to the deletion-request submitted state |
| 10 | **[ACTION]** (Alternative) Select "Email OTP" → tap to send OTP | OTP sent confirmation; 6-digit input field appears; "Resend OTP" link visible | Pass | Switching to OTP immediately sends an email OTP; resend is available; successful OTP verification follows the same submitted/pending flow |
| 11 | **[ACTION]** Enter incorrect password/OTP | Error message: "Invalid password/OTP. Please try again." | Pass | Incorrect password / OTP is handled correctly and validation feedback is shown; OTP resend remains rate-limited to 3 requests within 30 minutes |
| **Final Confirmation & Submission** | | | | |
| 12 | After successful verification: **[CHECK]** final confirmation modal appears ("Submit deletion request?") | Modal with Confirm and Cancel buttons | Pass | Current flow does not show a separate final confirmation modal; after successful verification it proceeds directly to the submitted/pending state, and this is accepted behavior |
| 13 | **[ACTION]** Tap "Cancel" | Modal dismisses; returns to flow without submitting | N/A | No separate final-confirmation modal / cancel action is present in the current accepted flow |
| 14 | **[ACTION]** Tap "Confirm" | Deletion Request Submitted screen loads | Pass | After successful verification, the flow proceeds directly to the deletion-request submitted screen |
| 15 | **[CHECK]** confirmation screen: status "Pending Admin Review", request reference ID, submitted timestamp, processing timeline, what-happens-next section, email confirmation notice | All fields render with correct data | Pass | Submitted-state screen shows `Pending Admin Review`, request reference ID, submitted timestamp, processing timeline, what-happens-next section, and email confirmation notice as expected |
| 16 | **[ACTION]** Tap "Back to Profile" | Returns to Profile screen | Pass | Submitted-state screen provides `Back to Profile` and this behavior is accepted |

> **Caution:** Completing step 14 will submit a real deletion request. If testing on a reusable account, cancel at step 13 instead. Only proceed to step 14 on a disposable test account.

---

### TC-M-006: Help & Support (UI Check)

**Goal:** Verify Help & Support screens render, navigation works, and forms are present. Not all features may be fully functional — note completeness gaps.
**Flow:** P08.1

| # | Step | Expected Result | Result | Notes |
|---|------|-----------------|--------|-------|
| **Hub Screen** | | | | |
| 1 | Navigate to **Help & Support** (from Settings or Profile) | Help & Support Hub loads with title "Help & Support" | Pass | Help & Support hub loads correctly with title `Help & Support` |
| 2 | **[CHECK]** hub layout: search bar, "Help Center" row, "Contact Support" row, "My Support Tickets" row | All navigation items present with icons and chevrons | Pass | Hub shows `Help Center`, `Contact Support`, and `My Support Tickets` rows with icons/chevrons; lack of a separate search bar on the hub is accepted for the current build |
| 3 | **[CHECK]** emergency contact section at bottom (phone + email) | Emergency info visible; phone is tap-to-call, email is tap-to-compose | Pass | Emergency phone and email are visible on the hub screen |
| 4 | **[CHECK]** "My Support Tickets" badge shows open ticket count (or hidden if 0) | Badge renders correctly | Pass | `My Support Tickets` badge is visible and shows `99+` |
| **Help Center** | | | | |
| 5 | **[ACTION]** Tap "Help Center" | Help Center Browser screen loads | Pass | Help Center screen opens successfully |
| 6 | **[CHECK]** content type cards visible: FAQs, Articles, Resources, Videos | Cards present (some may show "No content available yet" — note which) | Pass | `FAQs`, `Articles`, `Resources`, and `Videos` cards are visible in Help Center |
| 7 | **[ACTION]** Tap each content type card | Respective content list loads (or empty state) | Partial | FAQ and Articles flows were opened successfully. Resources list/detail and Video Tutorials list/detail screens are also reachable, but they currently behave at UI-shell level only and no end-to-end functional actions were confirmed as truly working in this round |
| 8 | **[DATA]** If FAQs load: check collapsible accordion sections with topic headers | FAQ topics expand/collapse; answers render as rich text | Pass | FAQ Topic screen shows tabbed topics and accordion items; expanded answers render correctly |
| 9 | **[DATA]** If Articles load: check subtype filter (Tutorial Guides / Troubleshooting Tips) and article cards | List renders; tapping an article opens detail with title, body, "Was this helpful?" | Partial | Articles list renders with `All`, `Tutorial Guides`, and `Troubleshooting` filters; article detail opens with title, body, table of contents, related articles, and `Helpful / Not Helpful`, but the subtype tabs are currently UI-only and do not functionally filter content, and article feedback selection does not persist |
| 10 | **[ACTION]** If search bar is functional: type a query | Results appear or "No results" message with Contact Support CTA | Fail | Search bar is visible in Help Center, but it currently cannot be typed into or used for search |
| 11 | **[ACTION]** Tap back to Hub | Navigation works | Pass | Back navigation within the Help Center flow works as expected via both the in-app UI back button and the Android hardware back button |
| **Contact Support** | | | | |
| 12 | **[ACTION]** Tap "Contact Support" | Contact Support Form opens | Fail | Tapping `Contact Support` opens a `Support Team` screen instead of the expected support-ticket form |
| 13 | **[CHECK]** form fields: Title, Category picker, Description, Priority picker, Attachments | All fields present with correct input types | Fail | No ticket form fields are present on the current `Support Team` screen; ticket creation is currently exposed under `My Support Tickets > Create New Ticket` instead |
| 14 | **[CHECK]** category options include: Technical Issue, Account Access, Payment Question, Booking Issue, General Inquiry, Feature Request, Bug Report, Feedback | Options match spec (no admin-only categories like "Provider Support") | N/A | Category options cannot be checked because the ticket form is not present |
| 15 | **[CHECK]** priority options: Low, Medium, High, Urgent with inline descriptions | Options and helper text present | N/A | Priority options cannot be checked because the ticket form is not present |
| 16 | **[ACTION]** Try to submit with empty fields | Submit button disabled or shows validation errors | N/A | Validation cannot be checked because the ticket form is not present |
| 17 | **[ACTION]** Fill all required fields and submit | Confirmation screen with Case ID (CASE-YYYY-#####) and "We will respond within 24 hours" message; then navigates to My Support Tickets | N/A | Ticket submission is available via `My Support Tickets > Create New Ticket`, not via the current `Contact Support` path |
| **My Support Tickets** | | | | |
| 18 | **[ACTION]** Tap "My Support Tickets" from Hub | Ticket list screen loads | Pass | My Support Tickets list opens successfully |
| 19 | **[CHECK]** filter chips: All, Open, In Progress, Resolved, Closed | Chips present and functional | Pass | Status tabs filter the support-ticket list correctly |
| 20 | **[DATA]** If tickets exist: each card shows Case ID, title, status badge, priority badge, submitted date, last updated | All fields render correctly with color-coded badges | Pass | Ticket cards show Case ID, title, status badge, priority badge, submitted date, and last updated |
| 21 | **[ACTION]** Tap a ticket card | Ticket Detail view opens with case info, status, communication thread | Pass | Ticket detail opens correctly |
| 22 | **[CHECK]** thread shows messages with sender labels ("You" / "Support Team"), timestamps | Thread renders chronologically | Pass | Communication thread shows sender labels and timestamps correctly |
| 23 | **[CHECK]** reply input field visible for Open/In Progress/Resolved tickets; hidden for Closed | Input field state matches ticket status | Partial | Reply capability is available in ticket detail and attachments can be added in replies, but the closed-ticket hidden-state path was not separately exercised in this round |
| 24 | **[ACTION]** Type a reply and send (if ticket is Open/In Progress) | Reply appears in thread | Pass | Reply works in ticket detail and file/image attachment is supported in replies |
| 25 | If ticket is Closed: **[CHECK]** closed case banner with "Create New Ticket" option | Banner present with recovery path | Pass | Current closed-ticket behavior is accepted for this build/design, so the absence of a separate recovery / `Create New Ticket` path is not treated as a defect |

---

### TC-M-007: Travel & Logistics (UI Check)

**Goal:** Verify Travel & Logistics screens render and forms are present. Screens are temporarily placed in Confirmed/In Progress views.
**Flows:** P04.1, P04.2

| # | Step | Expected Result | Result | Notes |
|---|------|-----------------|--------|-------|
| **Access via Confirmed View** | | | | |
| 1 | Navigate to the **"Confirmed" view** in bookings/inquiries section | View loads; travel-related screens are accessible from here | Pass | Confirmed-view travel card is present with booking summary, `View scheduled details`, `Book hotel`, `Book flight`, `Input passport details`, offer CTA, and request-overview CTA |
| **Passport Submission (P04.1)** | | | | |
| 2 | **[ACTION]** Access the Passport submission screen | Passport Submission Form loads with title "Passport Details" | Pass | `Passport Details` screen opens from the travel area |
| 3 | **[CHECK]** form layout: booking context header, submission status badge, passport photo upload section, personal info fields (full name, DOB, gender, nationality, place of birth), passport info fields (number, issue date, expiry date) | All sections and fields present with correct input types | Pass | Passport form field inventory is now evidenced in the current captures: booking context, `Awaiting` status, passport-photo upload, guidance text, gender, location/country, place of birth, passport number, passport issue date, and passport expiry date are all visible with the expected input controls |
| 4 | **[CHECK]** upload guidelines text is displayed | Instructions for acceptable passport photo visible | Pass | Passport-photo guidance text is visible under the upload block |
| 5 | **[ACTION]** Tap passport photo upload | Camera/gallery picker opens | Pass | Passport-photo upload interaction works |
| 6 | **[ACTION]** Upload a photo | Preview thumbnail shown with Replace/Remove options | Pass | Passport-photo upload works successfully |
| 7 | **[ACTION]** Fill in all required fields with valid data | All fields accept input; date pickers work | Pass | User confirmed the passport form can be filled successfully, and the visible manual fields include dropdown/text/date inputs as expected |
| 8 | **[ACTION]** Try to submit with missing required fields | Submit button disabled or field-level validation errors shown | Pass | UI-only passport-form round: submit-path logic was intentionally not checked in depth for this temporary test form |
| 9 | **[ACTION]** Enter a past passport expiry date and attempt submit | Validation error: "Passport expiry date must be in the future" | Pass | UI-only passport-form round: passport-expiry submit validation was not separately checked in depth for this temporary test form |
| 10 | **[ACTION]** Submit with all valid data | Confirmation / read-only view loads showing submitted details; status badge shows "Submitted" | Pass | UI-only passport-form round: submit logic was intentionally passed over and not verified end-to-end for this temporary test form |
| 11 | **[CHECK]** read-only view: all fields display as non-editable text; passport number is masked; "Contact Support to Request a Correction" button present | Record is locked; fields match what was entered | N/A | Submitted passport read-only state was not evidenced in the current captures |
| **Flight Submission (P04.2)** | | | | |
| 12 | **[ACTION]** Access the Flight submission screen from the Confirmed view | Flight form loads with "Outbound Flight" or similar title | Pass | `Outbound Flight` form opens from the travel area |
| 13 | **[CHECK]** form fields: airline name, flight number, departure/arrival airports, departure/arrival dates & times, ticket confirmation number, ticket class, optional baggage/special requests | All fields present | Pass | No missing outbound-flight fields are apparent in the current captures: airline, flight number, departure/arrival airports, departure/arrival date/time, ticket confirmation number, ticket class, baggage allowance, and special requests are all visible |
| 14 | **[ACTION]** Fill outbound flight details and submit | Record saves; prompt to submit return flight appears | Pass | UI-only flight-form round: submit-path logic was intentionally not checked in depth for this temporary test form |
| 15 | **[CHECK]** submitted flight record shows as read-only with locked status banner | Record locked; "Contact Support" for corrections | Pass | UI-only flight-form round: submitted outbound-flight locked-state behavior was not verified end-to-end for this temporary test form |
| **Hotel Submission (P04.2)** | | | | |
| 16 | **[ACTION]** Access the Hotel submission screen | Hotel form loads with title "Hotel Information" | Pass | `Hotel Information` screen is reachable and is currently shown in a submitted/locked state |
| 17 | **[CHECK]** form fields: hotel name, address, check-in/out dates & times, reservation number, room type, optional amenities/transportation/special requests/phone/email | All fields present | Pass | No missing hotel fields are apparent in the current captures: hotel name, address, check-in/out date and time, reservation number, room type, amenities included, transportation details, special requests, phone number, and email are all visible |
| 18 | **[ACTION]** Fill hotel details and submit | Record saves; shows confirmation or navigates to itinerary | Pass | Current screenshots show a saved hotel record with `Submitted` status plus submitted timestamp/by-user metadata, indicating the hotel form can be submitted and is then locked |
| **Travel Itinerary (via In Progress View)** | | | | |
| 19 | Navigate to the **"In Progress" view** | View loads; Travel Itinerary screen is accessible | N/A | Separate `In Progress`-view itinerary access was not captured in the current screenshot set |
| 20 | **[ACTION]** Open Travel Itinerary screen | Itinerary View loads with title "Travel Itinerary" | N/A | A dedicated `Travel Itinerary` title screen was not captured in the current round |
| 21 | **[CHECK]** itinerary layout: booking context header, flight sections (outbound/return), hotel section | Sections present; submitted records show summary data; pending records show "not yet submitted" prompts | N/A | Separate itinerary layout coverage is not yet evidenced beyond the Confirmed-view travel/logistics entry screen |
| 22 | **[ACTION]** Tap a submitted record section | Navigates to read-only detail view | N/A | This exact itinerary-to-detail transition was not separately captured in the current round |
| 23 | **[ACTION]** Tap back | Returns to itinerary | N/A | Back-to-itinerary behavior was not separately evidenced in the current round |

---

### TC-M-008: Regression & Recheck (from 2026-03-30 round)

**Goal:** Re-verify items that were previously approved with caveats, flagged as "Needs Further Checking", or blocked by `ParseFailure`.

#### Part A — Previously Approved with Open Items

| # | Recheck ID | Step | Expected Result | Result | Notes |
|---|------------|------|-----------------|--------|-------|
| 1 | RC-01 | **Delete Account error states:** Attempt deletion with an account that has active treatment or pending payment | Blocking message displayed: "Account deletion is unavailable during active care or payment processing"; Request Deletion button is disabled | Pass | Blocking-condition coverage is accepted as pass for this round: active-treatment / pending-payment accounts are treated under the same restriction and cannot proceed |
| 2 | RC-01 | **Delete Account rate-limit:** Enter wrong password/OTP multiple times during identity verification | Rate-limit / lockout message appears after configured threshold; retry blocked | Partial | Wrong password / wrong OTP validation is confirmed, and OTP flow enforces a resend limit of 3 requests within 30 minutes; full lockout-threshold behavior was not exhaustively reproduced in this round |
| 3 | RC-02 | **Settings legal content:** Tap Privacy Policy from Settings > Privacy & Security | Check if content opens in-app (per spec) or external browser (as in previous round) — note which | Pass | Opens in external browser; accepted behavior aligned between client and dev team |
| 4 | RC-02 | **Settings legal content:** Tap Terms & Conditions from Settings | Same check: in-app vs external browser | Pass | Opens in external browser; accepted behavior aligned between client and dev team |
| 5 | RC-03 | **Change Password:** Navigate to Settings > Privacy & Security > Change Password | Change password form loads; enter current + new password; submit succeeds | Partial | Change password works and the new password can be used to log in, but validation incorrectly allows the new password to be the same as the current password |
| 6 | RC-03 | **Change Password — Forgot link:** Tap "Forgot your password?" on the change password screen | Routes correctly to existing password recovery flow | Pass | Forgot-password flow works: OTP is sent to email, password can be reset, and the app auto-logs out afterward so the user signs in again with the new password |
| 7 | RC-06 | **Payment Methods nickname:** Add a card with a custom nickname (e.g., "Personal Visa") | On the Payment Methods list, the card displays the custom nickname instead of just the brand name | Partial | Editing Method Nickname shows a success toast, but the list still displays the card brand and reopening the detail/edit screen shows the nickname field blank again |
| 8 | RC-10 | **Previous Treatments empty state:** View the Previous Treatments list with no treatments on the account | Empty state message displayed (not a blank screen) | | |
| 9 | RC-11 | **My Reviews regression:** Open My Reviews list → tap a review → edit → save; also test Request Takedown | Edit saves and publishes immediately; Takedown shows confirmation prompt | Partial | Request Takedown can be submitted, but the edit/save path still has open bugs |

#### Part B — Previously "Needs Further Checking"

| # | Recheck ID | Step | Expected Result | Result | Notes |
|---|------------|------|-----------------|--------|-------|
| 10 | RC-05 | **Expired quotes:** Navigate to an inquiry where quotes have expired | Expired quote indicator visible on individual quote (P02.3-S1); if all expired, "All Quotes Expired" state shown (P02.3-S2) | | |
| 11 | RC-12 | **Notification swipe actions:** On the Notification List, swipe left on an unread notification | Swipe reveals "Mark as Read" and "Archive" action buttons | N/A | Not testable yet because backend is not returning notification items |
| 12 | RC-12 | **Notification archive:** Tap "Archive" on the swipe action | Notification hidden from default list; retrievable via "All" filter | N/A | Not testable yet because backend is not returning notification items |
| 13 | RC-13 | **Help & Support hub structure:** Navigate to Help & Support | Screen title is "Help & Support" (not "Support Team"); hub shows search bar, Help Center, Contact Support, My Support Tickets, emergency contacts | Pass | Screen title is now `Help & Support` and the hub shows Help Center, Contact Support, My Support Tickets, badge, and emergency contacts; lack of a separate search bar on the hub is accepted for the current build |

#### Part C — Previously Blocked by `ParseFailure`

> First, confirm whether the `ParseFailure` blocker is resolved:

| # | Recheck ID | Step | Expected Result | Result | Notes |
|---|------------|------|-----------------|--------|-------|
| 14 | — | **ParseFailure check:** Create an inquiry, go through quote creation flow | Quote creates successfully without `ParseFailure`; `duration_of_concern` no longer `null` in the payload | | If still failing, mark RC-04, RC-07, RC-08, RC-09 as **BLOCKED** |
| 15 | RC-04 | **Compare Offers:** With 2+ quotes on an inquiry, access the comparison view | Side-by-side comparison UI renders; provider name, price, package details shown per quote | | |
| 16 | RC-09 | **Treatment Progress:** Open an In Progress treatment case | Treatment Progress Timeline loads (P05.1-S1); day rows visible with status badges; tapping a day opens Day Details Popup (P05.1-S2) | | |
| 17 | RC-09 | **Completed Treatment:** Open a completed treatment case | Completed Treatment View (P05.1-S3) shows graft count, summary, before/after photos, post-op instructions | | |

> **Note:** RC-07 (Passport) and RC-08 (Flight & Hotel) are already covered in TC-M-007 above. If TC-M-007 passes, mark RC-07 and RC-08 as resolved.

---

## Cross-Cutting Checks

Apply these checks across **all** screens visited during testing:

| # | Check | What to Look For |
|---|-------|-----------------|
| X-01 | **Loading states** | Screens show spinner/skeleton while data loads; no blank screens |
| X-02 | **Error states** | If API fails (toggle airplane mode briefly), an error message appears with retry option; no crash |
| X-03 | **Back navigation** | Every screen's back arrow returns to the correct parent screen; Android hardware back button behaves consistently |
| X-04 | **Keyboard behavior** | Keyboard opens for text fields; "Done"/"Next" buttons work; keyboard dismisses on tap outside; content scrolls so active field is visible above keyboard |
| X-05 | **Scroll behavior** | Long content scrolls smoothly; no cut-off at screen bottom; pull-to-refresh works where applicable |
| X-06 | **Text rendering** | No text overflow, truncation issues, or overlapping elements; long values (names, addresses) wrap properly |
| X-07 | **Date/time pickers** | Date pickers open correctly; format is consistent; past/future constraints enforced |
| X-08 | **Image loading** | Avatars, icons, uploaded images load without broken placeholders; loading indicators shown during fetch |
| X-09 | **Screen rotation** | App handles rotation without crashing or layout breakage (or is locked to portrait — note which) |
| X-10 | **Deep links from notifications** | If a notification has a deep link, tapping it navigates to the correct screen |

---

## Completeness Tracker

Use this table to record which features from each module are **present**, **missing**, or **partially implemented** in the build. This feeds into the final report.

| Module | Feature / Screen | Present | Partial | Missing | Notes |
|--------|-----------------|---------|---------|---------|-------|
| Notifications | Bell icon + badge | | Yes | | Notification entry point is present in bottom nav; unread badge behavior is still not verifiable because no notifications are returned |
| Notifications | Notification list + filters | | Yes | | Screen opens successfully; empty state shown; filter is visible but filter behavior is not yet verifiable without data; pull-down to refresh is currently missing |
| Notifications | Swipe actions (mark read, archive) | | Yes | | Still untestable because backend returns no notification items to swipe on |
| Notifications | Deep link navigation | | Yes | | Not testable because no notifications are returned |
| Notifications | Search | Yes | | | Search bar is visible on the notification screen |
| Settings | Main screen (4 nav rows) | | | | |
| Settings | Notification preferences (toggles) | | Yes | | Both toggles are visible, but on/off changes do not persist despite success toast feedback |
| Settings | Privacy Policy content | Yes | | | Opens in the phone's external browser; accepted behavior aligned between client and dev team |
| Settings | Terms & Conditions content | Yes | | | Opens in the phone's external browser; accepted behavior aligned between client and dev team |
| My Reviews | Reviews list + sort | | Yes | | Review list is present, but sorting control/function is missing |
| My Reviews | Review detail view | Yes | | | Detail view loads and shows rating breakdown plus detailed review content |
| My Reviews | Edit review | | Yes | | Edit flow exists, but save can get stuck in `Saving` state and rating criteria are incorrectly linked |
| My Reviews | Submit review photo upload | | | Yes | Completed-case submit-review screen has no visible image-upload control, while edit-review screen exposes a Photos section |
| My Reviews | Submit/edit review UI consistency | | Yes | | Submit-review screen and edit-review screen are not structurally aligned |
| My Reviews | Request takedown | Yes | | | Takedown request can be submitted successfully |
| Payment Methods | List + empty state | Yes | | | Both empty-state and populated-state list screens were observed successfully |
| Payment Methods | Add card (gateway form) | Yes | | | Embedded payment gateway form opens and a test card can be added successfully |
| Payment Methods | Edit card metadata | | Yes | | Detail/edit screen is reachable, but Method Nickname does not persist after save even though a success toast is shown |
| Payment Methods | Remove card + modal | Yes | | | Remove confirmation works; non-default delete modal omits last 4 digits and this is accepted, while default-card delete flow shows reassignment messaging with last 4 digits for the next default card |
| Payment Methods | Set as default | Yes | | | Works from both the three-dot context menu and the `Set as default payment method` switch inside Edit Payment Method |
| Delete Account | Warning screen | Yes | | | Delete Account warning screen content and CTA set are present as expected, and the flow includes a separate reason-confirm step before verification |
| Delete Account | Verify Identity (password) | Yes | | | Verify Identity screen content is present; password verification works and includes a `Forgot password` path at this step |
| Delete Account | Verify Identity (email OTP) | Yes | | | OTP is sent immediately on tab switch, resend is available, and resend is rate-limited to 3 requests in 30 minutes |
| Delete Account | Confirmation screen | Yes | | | Submitted-state screen shows pending-admin-review status plus the expected metadata and follow-up information |
| Help & Support | Hub screen | Yes | | | Hub title, rows, badge, and emergency contacts are present; lack of a separate search bar on the hub is accepted for the current build |
| Help & Support | Help Center browser (FAQs) | Yes | | | FAQ Topic flow loads with topic tabs, accordion sections, and rich-text answers |
| Help & Support | Help Center browser (Articles) | | Yes | | Articles list and detail views load, but `Tutorial Guides` / `Troubleshooting` tabs are UI-only, search is not usable, and `Helpful / Not Helpful` feedback does not persist |
| Help & Support | Help Center browser (Resources) | | Yes | | Resources list/detail screens are present, but currently appear to be UI-level only; functional actions are not confirmed as working |
| Help & Support | Help Center browser (Videos) | | Yes | | Video Tutorials list/detail screens are present, but currently appear to be UI-level only; functional actions are not confirmed as working |
| Help & Support | Contact Support form | | Yes | | Ticket submission exists under `My Support Tickets > Create New Ticket`, but the `Contact Support` entry point currently opens a `Support Team` screen instead of the expected form |
| Help & Support | My Support Tickets list | Yes | | | Ticket list loads and status tabs filter correctly |
| Help & Support | Ticket Detail + thread | Yes | | | Ticket detail opens with communication thread, replies work, and attachments can be added in replies |
| Travel | Passport submission form | Yes | | | `Passport Details` is reachable; passport-photo upload works; and the visible field set now includes gender, location/country, place of birth, passport number, passport issue date, and passport expiry date |
| Travel | Passport read-only view | | Yes | | Submitted passport read-only state was not checked in this UI-only passport-form round, so record-lock / masked-passport rendering remains unverified |
| Travel | Flight submission (outbound) | Yes | | | `Outbound Flight` form is reachable and the expected outbound fields are visible with no obvious field gaps in the current captures |
| Travel | Flight submission (return) | | Yes | | Outbound-flow coverage exists, but the return-flight prompt/screen was not captured in this round |
| Travel | Hotel submission | Yes | | | Hotel record shows complete submitted/locked detail coverage with the expected field set and no obvious missing hotel fields |
| Travel | Travel Itinerary view | | Yes | | Confirmed-view travel/logistics entry screen is present, but the separate `Travel Itinerary` screen from the `In Progress` view was not captured in this round |
| Travel | Travel Requirement Check ("Do you need travel?") | Yes | | | `Travel Requirement Check` screen is present with appointment summary plus both `Yes — I need to arrange travel` and `No — I am local / no travel needed` actions |
| **Regression (from 2026-03-30)** | | | | | |
| Delete Account | Error/blocking states (RC-01) | Yes | | | Blocking-condition coverage is accepted as pass for this round: active-treatment / pending-payment accounts are treated under the same restriction and cannot proceed |
| Delete Account | Rate-limit on identity verification (RC-01) | | Yes | | Wrong password / wrong OTP validation is confirmed, and OTP resend is limited to 3 requests within 30 minutes; broader lockout-threshold coverage still incomplete |
| Settings | Legal content delivery method — in-app vs browser (RC-02) | Yes | | | Verified external browser behavior; accepted alignment with client and dev team |
| Change Password | Full flow + forgot password link (RC-03) | | | | Previously: approved |
| Compare Offers | Side-by-side comparison UI (RC-04) | | | | Previously: blocked by ParseFailure |
| Expired Quotes | Expired indicators P02.3-S1/S2 (RC-05) | | | | Previously: not evidenced |
| Payment Methods | Nickname display on list (RC-06) | | Yes | | Bug persists: success toast appears, but list still shows brand and nickname field is blank again on reopen |
| Treatment Progress | Timeline + day details + completed view (RC-09) | | | | Previously: blocked by ParseFailure |
| Previous Treatments | Empty state (RC-10) | | | | Previously: not verified |
| Notifications | Swipe actions (RC-12) | | Yes | | Still could not verify because backend returns no notification items |
| Help & Support | Hub structure matches spec (RC-13) | Yes | | | Title/rows/badge/emergency contacts are now present; lack of a separate search bar on the hub is accepted for the current build |
| ParseFailure | `duration_of_concern` schema resolved | | | | Previously: blocking quote-dependent flows |

---

## Defect Reporting Template

For each defect found, log the following:

| Field | Value |
|-------|-------|
| **ID** | DEF-M-### |
| **Test Case** | TC-M-00# / Step # |
| **Screen** | Screen name and flow reference |
| **Severity** | Critical / Major / Minor / Cosmetic |
| **Type** | Functional / UX-Interaction / Data-Rendering / Crash |
| **Description** | What happened |
| **Expected** | What should have happened |
| **Steps to Reproduce** | Numbered steps |
| **Screenshot** | Attach photo from device |
| **Device Info** | Phone model, Android version |

### Severity Guide

| Severity | Definition |
|----------|-----------|
| **Critical** | App crash, data loss, security issue, or complete feature failure |
| **Major** | Feature doesn't work as expected but has a workaround; incorrect data displayed |
| **Minor** | UI inconsistency, minor interaction issue, non-blocking UX problem |
| **Cosmetic** | Visual-only: spacing, alignment, color, font issues |

---

## Test Execution Log

| Date | Tester | TC Completed | Pass | Fail | Partial | Defects Filed | Notes |
|------|--------|-------------|------|------|---------|---------------|-------|
| | | | | | | | |

---

## Post-Testing Summary

_To be filled after testing is complete._

### Overall Result

- [ ] **Go** — No critical/major defects; ready for next phase
- [ ] **Conditional Go** — Minor defects only; can proceed with known issues
- [ ] **No Go** — Critical/major defects must be fixed first

### Completeness Assessment

_Summarize which features were present, missing, or partial per the Completeness Tracker above. This informs the dev team what still needs to be built vs. what needs fixing._

### Key Defects Summary

| ID | Severity | Module | Summary |
|----|----------|--------|---------|
| | | | |
