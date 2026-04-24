# Integrated Testing Plan & Report — Patient Mobile App

**Report Date**: 2026-04-22  
**Report Type**: Integrated Testing Plan + Live Report  
**Platform**: Patient Mobile App  
**Phase**: Integrated Testing (Full Lifecycle Flow)  
**Status**: In Progress  
**Prepared By**: _(fill in tester name / agent ID)_  
**Last Updated**: 2026-04-22

---

## Purpose

This document is both a **pre-written testing plan** and a **live testing report**. The plan columns (Module → Expected Result) are pre-populated and must not be changed. The result columns (Actual Result, Status & Notes) are filled in by the tester or agent during or after testing.

This is an **integrated test phase**, meaning each test case must be evaluated not in isolation but as part of the full patient lifecycle:

```
Inquiry Submission → Offers (Quote Review & Acceptance) → In Progress (Treatment) → Aftercare
```

Test cases are ordered within each module to follow this lifecycle sequence.

---

## Scope

| Module | Screens Covered |
|--------|----------------|
| **Inquiries** | Inquiry Overview Screen, Cancel Inquiry Screen, Inquiry Cancelled Success Screen, Cannot Cancel Inquiry Modal |
| **Offers** | Offers List Screen, Offers Selection Screen, Offers Bottom Sheet, Filter Offers Modal, Compare Offers Table Screen, Treatment Details Screen, Accept Offer Confirmation Modal, Discount Code Screen, Cancellation Policy Screen |
| **In Progress** | Booking Info Screen, Provider Tab Screen, Problem Tab Screen, Treatment Tab Screen, End of Treatment Screen |
| **Aftercare** | My List Dashboard Screen, Aftercare Milestones Screen, Milestone Detail Screen, Scan Upload Screen, Pain Assessment Screen, Pain Assessment Extended Screen, Question Text Input Screen, Question Multiple Choice Screen, Question Dropdown Screen, Medication Screen, Instruction Screen, External Treatment Info Screen, Aftercare Services Screen, Aftercare Checkout Screen, Completed Inquiry Dashboard Card |

---

## How to Fill In This Report

### For Agents Joining Mid-Test

> **READ THIS SECTION BEFORE FILLING IN ANY RESULTS.**

1. **Do not modify** the plan columns: ID, Module, Flow/Screen, Case Type, Prerequisites, Testing Steps, Testing Data, Expected Result.
2. **Fill in** only: Actual Result, Status & Notes.
3. For **Actual Result**: describe what actually happened in the app — screenshots, API responses, error messages, or behavior observed. Be specific. If a field shows wrong data, quote the exact value shown.
4. For **Status & Notes**: use one of the status values below, then add any relevant notes:
   - `✅ Pass` — behavior matches Expected Result exactly
   - `❌ Fail` — behavior does not match Expected Result; describe the gap
   - `⚠️ Partial` — some aspects pass, some fail; describe both
   - `🔲 Blocked` — cannot test due to a prerequisite issue (e.g., API error, missing test data)
   - `⏭️ Skipped` — not tested in this round; must note the reason
5. For **blocked** tests: add the blocking reason and the ticket/issue reference if one exists.
6. If a test triggers an **unexpected crash or critical error**: mark `❌ Fail` and add `[CRITICAL]` prefix in Notes.

### Column Definitions

| Column | Content |
|--------|---------|
| **ID** | Unique test case identifier — do not change |
| **Module** | Feature module — do not change |
| **Flow / Screen** | Screen or sub-flow being tested — do not change |
| **Case Type** | `Happy` / `Edge` / `Error` / `Integration` — do not change |
| **Prerequisites** | Required app state before starting this test — do not change |
| **Testing Steps** | Numbered steps to reproduce — do not change |
| **Testing Data** | Specific input values to use — do not change |
| **Expected Result** | What should happen — do not change |
| **Actual Result** | _(Fill in)_ What actually happened — be specific |
| **Status & Notes** | _(Fill in)_ Pass / Fail / Partial / Blocked / Skipped + notes |

---

## Standard Test Accounts & Mock Data

Use the following standardized data set across all test cases for consistency. If a specific test case requires different data, that data is specified in the Testing Data column of that case.

### Patient Accounts

| Role | Email | Password | Notes |
|------|-------|----------|-------|
| Primary Test Patient | `testpatient@hairline.test` | `Test@1234!` | Used for all patient flows |
| Second Patient (for edge cases) | `testpatient2@hairline.test` | `Test@1234!` | Used when 2 accounts needed |

### Inquiry Seed Data

| Field | Value |
|-------|-------|
| Treatment type | Hair |
| Destination countries | Canada, Åland Islands |
| Nature of concern | `Receding hairline at temples, thinning at crown` |
| Duration of concern | `1-2 years` (select from dropdown; maps to `duration_of_concern_id: 3`) |
| Previous treatments | `None` |
| Symptom severity | `7` (out of 10 slider) |
| Lifestyle factors | `No smoking, moderate alcohol` |
| Additional notes | `Prefer FUE method` |
| Media uploads | 3 JPG files, each ~1MB, clear lighting |

### Offer / Quote Seed Data

| Field | Value |
|-------|-------|
| Provider | Estepera Clinic (Canada) |
| Treatment | FUE Hair Transplant |
| Graft count (estimated) | 2,500 |
| Price | USD 2,500 |
| Appointment date | 2026-07-15 09:00 |
| Quote expiry | 7 days from quote creation date |

### Discount Codes

| Code | Type | Expected Behavior |
|------|------|-------------------|
| `HAIR10` | Valid — 10% off | Applied successfully; total reduced |
| `ABCXYZ` | Invalid — does not exist | Error: "Invalid discount code" |
| `OLDCODE` | Expired — past expiry date | Error: "This code has expired" |

### Payment Info (Test Cards)

| Field | Value |
|-------|-------|
| Card number | `4242 4242 4242 4242` (Visa test) |
| Expiry | `12/27` |
| CVV | `123` |
| Cardholder name | `Test Patient` |
| Billing address | `123 Test Street, Bangkok, Thailand` |

### Aftercare Questionnaire Answers

| Question Type | Sample Answer |
|---------------|---------------|
| Pain level (0–10 slider) | `3` |
| Text input (open-ended) | `Mild soreness around the transplanted area, no swelling` |
| Yes/No | `No` for all complication questions (baseline pass) |
| Multiple choice (sleep quality) | `Sleeping well, 7-8 hours` |
| Dropdown (activity level) | `Light activity only` |

---

## Section 1: Inquiries Module

> **Context**: Covers the patient's view of a submitted inquiry and the cancellation flow. The inquiry is the root entity from which all downstream flows (Offers → Booking → Treatment → Aftercare) originate. Test cases here must verify both read states (overview at different lifecycle stages) and the write/action flows (cancel inquiry and the resulting screens).
>
> **Source PRDs**: FR-003 (Inquiry Submission & Distribution), P02.2 (Cancel Inquiry flow from `missing-mobile-flows-design-complement.md`)

| ID | Module | Flow / Screen | Case Type | Prerequisites | Testing Steps | Testing Data | Expected Result | Actual Result | Status & Notes |
|----|--------|--------------|-----------|---------------|---------------|--------------|-----------------|---------------|----------------|
| INQ-001 | Inquiries | Inquiry Overview Screen | Happy | Patient logged in. A submitted inquiry exists with status **"Inquiry"** (submitted but no quotes received yet). | 1. Open app. 2. Navigate to inquiry list / dashboard. 3. Tap the inquiry card (status: Inquiry). 4. Observe the Inquiry Overview Screen. | Inquiry with no quotes. Status badge = `Inquiry`. | Screen displays: inquiry status badge `Inquiry`, submission date, treatment type (Hair), destination countries (Canada, Åland Islands), problem summary, medical alert level. No offer cards visible yet. Timeline shows submission event only. Next Actions show `Cancel Inquiry` option only. | Dashboard shows inquiry card with badge `REQUESTED` (app uses "REQUESTED" not "Inquiry"). Tapping opens overview screen with: `REQUESTED` badge + Patient ID (e.g. HPID2512-0014), "Your request overview" section showing the nature of concern text (e.g. "Thin 2304"), "View 3D Head Scan" green button (for viewing uploaded head scan media), "Date preferences" section showing multiple date range pills (e.g. "1 Jun 2026 – 14 Jun 2026", "1 Jul 2026 – 14 Jul 2026", "1 Aug 2026 – 14 Aug 2026"), "Medical history overview" section with "View all" button (medical detail gated behind tap), "Request timeline" showing a single "Inquiry" event with timestamp (correct — no other events for a fresh inquiry). "Cancel request" red bottom button visible. Treatment type (Hair), destination countries, and medical alert level are **not** displayed directly on this screen. No dedicated "Next Actions" section — cancel is a persistent bottom button. No offer cards visible (correct for this status). | ⚠️ Partial — Core overview screen renders correctly. Timeline correctly shows only the Inquiry event. Cancel action is accessible. New finding: "View 3D Head Scan" button present (not in expected result — positive addition). Gaps: (1) badge label is `REQUESTED` vs expected `Inquiry` — PRD terminology mismatch; (2) treatment type and destination countries not shown on the overview screen; (3) medical alert level not visible; (4) date preferences section with multiple ranges present but not specified in expected result. Confirm with team whether absent fields are intentional design or spec gaps. |
| INQ-002 | Inquiries | Inquiry Overview Screen | Happy | Patient logged in. An inquiry exists with status **"Quoted"** (≥1 quote received). | 1. Open app. 2. Navigate to inquiry list. 3. Tap the inquiry card (status: Quoted). 4. Observe the Inquiry Overview Screen. | Inquiry with ≥1 active offer. Status badge = `Quoted`. | Screen displays: status badge `Quoted`, quote count shown, each quote card visible (provider name, price, expiry countdown), Sort & Filter controls present. Actions: `View Details`, `Cancel Inquiry`. | _(fill in)_ | _(fill in)_ |
| INQ-003 | Inquiries | Inquiry Overview Screen | Happy | Patient logged in. An inquiry exists with status **"Accepted"** (one quote accepted, booking pending). | 1. Open app. 2. Navigate to inquiry list. 3. Tap the accepted inquiry card. 4. Observe the Inquiry Overview Screen. | Inquiry with 1 accepted quote. Status badge = `Accepted`. | Screen displays: status badge `Accepted`, accepted quote highlighted, non-selected quotes show `Cancelled (Other quote accepted)` badge. Cancel Inquiry still available (48-hour hold active). | _(fill in)_ | _(fill in)_ |
| INQ-004 | Inquiries | Inquiry Overview Screen | Edge | Patient logged in. An inquiry exists where **all offers have expired** (expiry countdown reached zero). | 1. Navigate to inquiry list. 2. Tap the inquiry where all offers are expired. 3. Observe the Inquiry Overview Screen and offer cards. | All quote cards expired. Status badge = `Quoted` (inquiry still open). | All quote cards display `Expired` badge. Accept buttons disabled. Comparison checkboxes disabled for expired offers. A guidance message is shown: "All quotes have expired. You may cancel this inquiry or contact support." | _(fill in)_ | _(fill in)_ |
| INQ-005 | Inquiries | Inquiry Overview Screen | Edge | Patient logged in. A previously **cancelled** inquiry exists. | 1. Navigate to inquiry list. 2. Tap a cancelled inquiry card. 3. Observe the screen. | Cancelled inquiry. Status badge = `Cancelled`. | Screen is read-only. Status badge = `Cancelled`. All action buttons (Accept, Compare) are disabled. Quote cards remain visible for reference but all interactions disabled. Cancel Inquiry button not shown. | _(fill in)_ | _(fill in)_ |
| INQ-006 | Inquiries | Cancel Inquiry Screen (modal) | Happy | Patient logged in. Inquiry in **"Inquiry"** status (no quotes received). | 1. Open the inquiry overview for an inquiry with status `Inquiry`. 2. Tap "Cancel Inquiry" from the action menu / button. 3. Observe the Cancel Inquiry modal. 4. Confirm cancellation. | Inquiry status: `Inquiry`. Cancellation reason: `No longer interested` (select from dropdown). | Cancel Inquiry modal appears with: inquiry summary, cancellation reason dropdown, warning message. On confirm: modal closes, navigation moves to Inquiry Cancelled Success Screen. | _(fill in)_ | _(fill in)_ |
| INQ-007 | Inquiries | Cancel Inquiry Screen (modal) | Happy | Patient logged in. Inquiry in **"Quoted"** status (≥1 active quote). | 1. Open inquiry overview (status: `Quoted`, with ≥1 active offer). 2. Tap "Cancel Inquiry". 3. Confirm cancellation. | Inquiry status: `Quoted`, 2 active offers. Cancellation reason: `Changed my mind`. | Cancel modal warns that all received offers will also be cancelled. On confirm: all quote cards transition to `Cancelled (Inquiry Cancelled)`. Success screen appears. Push notification received by patient. | _(fill in)_ | _(fill in)_ |
| INQ-008 | Inquiries | Cancel Inquiry Screen (modal) | Happy | Patient logged in. Inquiry in **"Accepted"** status, within 48-hour post-acceptance hold window. | 1. Open inquiry overview (status: `Accepted`). 2. Tap "Cancel Inquiry". 3. Confirm cancellation. | Inquiry status: `Accepted`, within 48-hour hold. Cancellation reason: `Found a different clinic`. | Modal warns: accepted quote will be cancelled, 48-hour appointment slot hold will be released. On confirm: inquiry → `Cancelled`, accepted quote → `Cancelled (Inquiry Cancelled)`, hold released. Success screen appears. | _(fill in)_ | _(fill in)_ |
| INQ-009 | Inquiries | Cannot Cancel Inquiry Modal | Error | Patient logged in. Inquiry is in a **non-cancellable** stage (e.g., `Completed`, `In Progress`, or `Aftercare`). | 1. Navigate to a completed or in-progress inquiry. 2. Attempt to access the "Cancel Inquiry" option (if visible). 3. Observe the resulting modal or behavior. | Inquiry status: `Completed` or `Aftercare`. | Cannot Cancel Inquiry modal appears explaining why cancellation is blocked (e.g., "Your treatment is already in progress. To cancel, please contact support."). No cancellation is processed. A "Contact Support" option is provided. | _(fill in)_ | _(fill in)_ |
| INQ-010 | Inquiries | Cannot Cancel Inquiry Modal | Error | Patient logged in. Inquiry in **"Accepted"** status but **beyond** the 48-hour hold window (booking confirmed and payment started). | 1. Open inquiry overview (accepted + booking confirmed post-48 hours). 2. Attempt to cancel. | Inquiry status: `Accepted`, booking progressed beyond 48-hour hold. | Cannot Cancel modal displays the specific blocking reason referencing the confirmed booking. "Contact Support" CTA present. No cancellation occurs. | _(fill in)_ | _(fill in)_ |
| INQ-011 | Inquiries | Inquiry Cancelled Success Screen | Happy | Prerequisite: INQ-006 or INQ-007 completed (cancellation confirmed). | 1. Complete a cancellation from INQ-006 or INQ-007. 2. Observe the screen shown after confirmation. | Result of a successful cancellation. | Inquiry Cancelled Success Screen appears: confirmation copy ("Your inquiry has been cancelled"), inquiry summary (ID, treatment type), action button to return to dashboard or submit a new inquiry. No error states. | _(fill in)_ | _(fill in)_ |
| INQ-012 | Inquiries | Inquiry Overview Screen | Integration | Patient account with inquiries at multiple lifecycle stages (one per status). | 1. Open the inquiry list. 2. Verify each inquiry card shows the correct status badge. 3. Tap into each status variant and verify the Inquiry Overview Screen reflects the correct state and available actions. | Inquiries at statuses: `Inquiry`, `Quoted`, `Accepted`, `Completed`, `Cancelled`. | Each inquiry card shows the correct status badge. The Inquiry Overview Screen for each shows the correct stage-appropriate content and action set (no actions bleed between stages). Navigation back to list works correctly from each. | _(fill in)_ | _(fill in)_ |

---

## Section 2: Offers Module

> **Context**: Covers all screens in the offer review, comparison, and acceptance flow. This maps to FR-004 (Quote Submission — data source) and FR-005 (Quote Comparison & Acceptance — patient interaction). In-app terminology uses "Offers" for what PRDs call "Quotes". Test cases must validate both UI correctness and business rule enforcement (e.g., exactly one acceptance per inquiry, expired offers blocked).
>
> **Source PRDs**: FR-004, FR-005, P02.1 (Compare Offers Side-by-Side), P02.3 (Expired Offers), P02.4 (Legal/Policy Screens) from `missing-mobile-flows-design-complement.md`

| ID | Module | Flow / Screen | Case Type | Prerequisites | Testing Steps | Testing Data | Expected Result | Actual Result | Status & Notes |
|----|--------|--------------|-----------|---------------|---------------|--------------|-----------------|---------------|----------------|
| OFF-001 | Offers | Offers List Screen | Happy | Patient logged in. Inquiry in `Quoted` status with **3 active, non-expired offers**. | 1. Open inquiry (status: `Quoted`). 2. Observe the Offers List Screen. 3. Verify each offer card's content. | 3 active offers: Provider A (USD 2,500), Provider B (USD 3,000), Provider C (USD 2,200). All expiry countdowns > 24 hours. | All 3 offer cards visible. Each card shows: provider name, treatment name, price, estimated graft count, expiry countdown (live timer), rating, Accept and View Details buttons. Sort and Filter controls present. Default sort: Quote Date (most recent first). | _(fill in)_ | _(fill in)_ |
| OFF-002 | Offers | Offers List Screen | Edge | Patient logged in. Inquiry in `Quoted` status with **exactly 1 active offer**. | 1. Open inquiry (status: `Quoted`, 1 offer). 2. Observe Offers List Screen. | 1 offer from Provider A only. | Single offer card displayed. Compare checkbox may be shown but comparison requires ≥2 offers — verify behavior (disabled or hidden). Sort/filter controls still present. No errors. | _(fill in)_ | _(fill in)_ |
| OFF-003 | Offers | Offers List Screen | Edge | Patient logged in. Inquiry in `Inquiry` status with **no offers received yet**. | 1. Open inquiry (status: `Inquiry`). 2. Navigate to the Offers / Quotes section within the inquiry. | No offers. Inquiry status: `Inquiry`. | Empty state displayed: message such as "Waiting for providers to respond" or similar placeholder copy. No offer cards. No Sort/Filter or Compare controls shown (or grayed out). | _(fill in)_ | _(fill in)_ |
| OFF-004 | Offers | Offers List Screen | Edge | Patient logged in. Inquiry in `Quoted` status where **all offers are expired**. | 1. Open inquiry with all offers past their expiry date. 2. Observe Offers List Screen. | All offers expired (expiry timestamps in the past). | All offer cards display `Expired` badge. Expiry countdown replaced by static "Expired on [date]" text. Accept button disabled on all cards. Compare checkboxes disabled. Guidance message shown to patient. | _(fill in)_ | _(fill in)_ |
| OFF-005 | Offers | Offers Bottom Sheet (Offer Options) | Happy | Patient logged in. Inquiry with ≥1 active offer. | 1. Open inquiry (status: `Quoted`). 2. On an active offer card, tap the options/more menu to open the Offer Bottom Sheet. 3. Observe available options. | Active offer (Provider A, USD 2,500). | Bottom sheet opens with options: `View Details`, `Compare`, `Contact Support`. All options tappable. | _(fill in)_ | _(fill in)_ |
| OFF-006 | Offers | Offers Bottom Sheet (Offer Options) | Edge | Patient logged in. Inquiry with at least 1 **expired** offer. | 1. Open inquiry with ≥1 expired offer. 2. Tap options menu on the expired offer card. 3. Observe the bottom sheet options. | Expired offer (expiry date in the past). | Bottom sheet appears. `Accept` option absent or disabled. `View Details` may still be available (read-only). Options correctly restricted for expired state. | _(fill in)_ | _(fill in)_ |
| OFF-007 | Offers | Filter Offers Modal | Happy | Patient logged in. Inquiry with ≥2 offers with different submission dates. | 1. Open Offers List Screen. 2. Tap "Filter" control. 3. Select a date range that includes ≥1 offer. 4. Apply filter. 5. Observe filtered results. | Date range filter: from 2026-06-01 to 2026-06-30. At least 1 offer submitted in this range. | Filter modal opens. Date range picker functional. After Apply: offer list shows only offers matching the date range. Active filter indicator shown. | _(fill in)_ | _(fill in)_ |
| OFF-008 | Offers | Filter Offers Modal | Edge | Patient logged in. Inquiry with ≥1 offer. | 1. Open Offers List Screen. 2. Tap "Filter". 3. Set a date range in the far future that no offer falls within. 4. Apply filter. | Date range: 2030-01-01 to 2030-12-31. No offers exist in this range. | Empty state shown after filter applied: "No offers match your filter." Clear filter option available. No crash or error. | _(fill in)_ | _(fill in)_ |
| OFF-009 | Offers | Filter Offers Modal | Happy | Prerequisite: OFF-007 or OFF-008 completed (filter applied). | 1. With an active filter applied, tap "Clear Filters" or "Reset". 2. Observe the offer list. | Filter applied from OFF-007 or OFF-008. | All offers restored to the unfiltered list. Active filter indicator removed. Default sort order restored. | _(fill in)_ | _(fill in)_ |
| OFF-010 | Offers | Offers Selection Screen | Happy | Patient logged in. Inquiry with ≥3 active offers at different price points. | 1. Open Offers List Screen. 2. Tap the Sort control. 3. Select "Price: Low to High". 4. Observe the reordered list. | Offers: Provider A USD 2,500, Provider B USD 3,000, Provider C USD 2,200. | Offers reordered: Provider C (USD 2,200) → Provider A (USD 2,500) → Provider B (USD 3,000). Sort indicator updated on the control. | _(fill in)_ | _(fill in)_ |
| OFF-011 | Offers | Offers Selection Screen | Happy | Patient logged in. Inquiry with ≥3 active offers with different ratings. | 1. Open Offers List Screen. 2. Tap Sort. 3. Select "Rating" (highest first). 4. Observe ordering. | Provider A rating 4.8, Provider B rating 4.2, Provider C rating 4.5. | Offers reordered: Provider A (4.8) → Provider C (4.5) → Provider B (4.2). | _(fill in)_ | _(fill in)_ |
| OFF-012 | Offers | Compare Offers Table Screen | Happy | Patient logged in. Inquiry with ≥2 active offers. | 1. Open Offers List Screen. 2. Select 2 offer checkboxes. 3. Tap "Compare". 4. Observe Compare Offers Table Screen. | Compare: Provider A (USD 2,500, 2,500 grafts, rating 4.8) vs Provider C (USD 2,200, 2,200 grafts, rating 4.5). | Comparison table rendered side-by-side. Rows include: total price, price per graft, graft count, review rating, soonest appointment slot, provider credentials, included services checklist. All data accurate per each offer. | _(fill in)_ | _(fill in)_ |
| OFF-013 | Offers | Compare Offers Table Screen | Happy | Patient logged in. Inquiry with ≥3 active offers. | 1. Open Offers List Screen. 2. Select 3 offer checkboxes. 3. Tap "Compare". 4. Observe Compare Offers Table Screen. | All 3 providers selected: A, B, C. | 3-column comparison table rendered. All 3 offers shown side-by-side. All comparison rows present. No data truncated. | _(fill in)_ | _(fill in)_ |
| OFF-014 | Offers | Compare Offers Table Screen | Edge | Patient logged in. Inquiry with ≥4 active offers. | 1. Open Offers List Screen. 2. Select 3 checkboxes (at maximum). 3. Attempt to check a 4th offer. | 4 active offers available. | 4th checkbox is disabled or unresponsive. A tooltip or message indicates: "Maximum 3 offers can be compared at once." No more than 3 offers selected. | _(fill in)_ | _(fill in)_ |
| OFF-015 | Offers | Compare Offers Table Screen | Edge | Patient logged in. Inquiry with 1 active offer and 1 expired offer. | 1. Attempt to select the expired offer checkbox. 2. Select the active offer. 3. Attempt comparison with only 1 valid offer. | 1 active + 1 expired offer. | Expired offer checkbox is disabled (cannot be selected for comparison). With only 1 active offer selected, Compare button remains disabled (requires ≥2). | _(fill in)_ | _(fill in)_ |
| OFF-016 | Offers | Treatment Details Screen | Happy | Patient logged in. Inquiry with ≥1 active offer. | 1. From Offers List, tap "View Details" on an active offer. 2. Observe the Treatment Details Screen. | Offer: Provider A, FUE Hair Transplant, USD 2,500, 2,500 estimated grafts, appointment 2026-07-15. | Treatment Details Screen shows: treatment name, provider name + credentials, price breakdown, graft count, appointment slot (date/time), included services/package, expiry countdown, Terms checkbox, Accept button (enabled), Contact Support button. | _(fill in)_ | _(fill in)_ |
| OFF-017 | Offers | Discount Code Screen | Happy | Patient logged in. On Treatment Details Screen or checkout flow where discount code entry is available. | 1. Navigate to the Discount Code input (from Treatment Details or checkout). 2. Enter a valid discount code. 3. Tap "Apply". | Discount code: `HAIR10` (valid, 10% off). | Code accepted. Discount applied: 10% deducted from total. Updated total displayed. Success indicator shown (e.g., green checkmark, "Code applied"). | _(fill in)_ | _(fill in)_ |
| OFF-018 | Offers | Discount Code Screen | Edge | Patient logged in. On Discount Code Screen. | 1. Enter an invalid discount code. 2. Tap "Apply". | Discount code: `ABCXYZ` (does not exist). | Error message displayed: "Invalid discount code. Please check the code and try again." No discount applied. Total unchanged. Code input field remains editable. | _(fill in)_ | _(fill in)_ |
| OFF-019 | Offers | Discount Code Screen | Edge | Patient logged in. On Discount Code Screen. | 1. Enter an expired discount code. 2. Tap "Apply". | Discount code: `OLDCODE` (expired). | Error message displayed: "This discount code has expired." No discount applied. Total unchanged. | _(fill in)_ | _(fill in)_ |
| OFF-020 | Offers | Cancellation Policy Screen | Happy | Patient logged in. Treatment Details Screen open for an active offer. | 1. From Treatment Details Screen, tap "Cancellation Policy" link. 2. Observe the Cancellation Policy Screen. | Active offer context. | Cancellation Policy Screen opens: screen title "Cancellation Policy", policy content displayed (read-only), version info present, Back navigation returns to Treatment Details Screen. Content is not editable. | _(fill in)_ | _(fill in)_ |
| OFF-021 | Offers | Accept Offer Confirmation Modal | Edge | Patient logged in. On Treatment Details Screen for an active, unexpired offer. | 1. On Treatment Details Screen, verify the Terms Acknowledgment checkbox is unchecked. 2. Observe the Accept button state without checking the box. | Terms checkbox: unchecked. Active, unexpired offer. | Accept button is disabled (grayed out) while Terms checkbox is unchecked. No acceptance possible without checking the box. | _(fill in)_ | _(fill in)_ |
| OFF-022 | Offers | Accept Offer Confirmation Modal | Happy | Patient logged in. On Treatment Details Screen. Terms checkbox unchecked. No prior accepted offer for this inquiry. | 1. Check the Terms Acknowledgment checkbox. 2. Verify Accept button becomes enabled. 3. Tap "Accept". 4. Observe the Confirmation Modal. 5. Review the summary. 6. Tap "Confirm". | Active offer: Provider A, USD 2,500, FUE Hair Transplant, appointment 2026-07-15. Terms checkbox: checked. | Accept button enables on checkbox tick. Confirmation Modal appears: shows offer summary (provider, price, treatment, appointment date), Terms re-noted, Next Steps info ("You'll be directed to complete payment"). "Confirm" and "Cancel" buttons present. On Confirm: modal closes, inquiry status updates to `Accepted`. Other offers for same inquiry now show `Cancelled (Other quote accepted)`. 48-hour payment hold begins. | _(fill in)_ | _(fill in)_ |
| OFF-023 | Offers | Accept Offer Confirmation Modal | Edge | Patient logged in. On Treatment Details Screen for an **expired** offer. | 1. Open Treatment Details for an offer whose expiry timer has reached zero. 2. Observe Accept button state. | Expired offer (expiry date in the past). Terms checkbox checked. | Accept button remains disabled regardless of Terms checkbox state. Expiry timer shows "Expired on [date]". No acceptance flow initiated. | _(fill in)_ | _(fill in)_ |
| OFF-024 | Offers | Accept Offer Confirmation Modal | Edge | Patient logged in. Inquiry where one offer was already accepted (OFF-022 completed). Attempt to accept a second offer for the same inquiry. | 1. Return to Offers List for the same inquiry. 2. Open Treatment Details for a second (non-accepted) offer. 3. Observe Accept button state. | Inquiry with 1 already-accepted offer. Second offer is active and unexpired. | Accept button disabled or absent for the second offer. Message shown: "You have already accepted an offer for this inquiry." The second offer card may show `Cancelled` badge. | _(fill in)_ | _(fill in)_ |
| OFF-025 | Offers | Accept Offer Confirmation Modal | Error | Patient logged in. Active offer, Terms checkbox checked. Network connectivity degraded or simulated API failure. | 1. Enable airplane mode or simulate API failure. 2. On Treatment Details Screen, check Terms checkbox. 3. Tap Accept. 4. In Confirmation Modal, tap Confirm. 5. Observe error handling. | Network unavailable or API returns 500 error. | Error state shown: "Something went wrong. Please try again." or equivalent. No duplicate acceptance created. Inquiry status not changed. Option to retry or go back. | _(fill in)_ | _(fill in)_ |
| OFF-026 | Offers | Full Offer Lifecycle | Integration | Patient logged in. Fresh inquiry submitted with ≥3 quotes received. | 1. Open inquiry (status: `Quoted`). 2. Review Offers List. 3. Apply a filter, then reset. 4. Sort by Price (Low to High). 5. Select 2 offers, open Compare Table. 6. Open Treatment Details for the cheapest offer. 7. Apply discount code `HAIR10`. 8. Check Terms. 9. Accept the offer. 10. Verify inquiry status → `Accepted`. 11. Verify other offers → `Cancelled`. | 3 offers, codes above, acceptance of Provider C (cheapest). | Each step completes without errors. Final state: inquiry `Accepted`, accepted offer highlighted, all others `Cancelled (Other quote accepted)`. 48-hour countdown shown. Navigation back to inquiry dashboard works. | _(fill in)_ | _(fill in)_ |

---

## Section 3: In Progress Module

> **Context**: Covers the patient's view of an active treatment case. After offer acceptance and booking confirmation, the provider "checks in" the patient to start the In Progress phase. The patient sees a read-only tabbed view of their case with real-time day-by-day progress. The End of Treatment Screen shows the completed treatment summary (patient view).
>
> **Assumption**: "Booking Info Screen", "Provider Tab Screen", "Problem Tab Screen", and "Treatment Tab Screen" are the four main tab views within the In Progress case detail on the patient side. This mirrors FR-010 Screen 1 (In Progress Case View) + FR-010 Day Details Popup.  
> _(If these map differently in the actual app — e.g., as separate screens rather than tabs — adjust navigation steps accordingly and note this in the Actual Result column.)_
>
> **Source PRDs**: FR-010 (Treatment Execution & Documentation), P05.1 (Day-to-Day Treatment Progress) from `missing-mobile-flows-design-complement.md`

| ID | Module | Flow / Screen | Case Type | Prerequisites | Testing Steps | Testing Data | Expected Result | Actual Result | Status & Notes |
|----|--------|--------------|-----------|---------------|---------------|--------------|-----------------|---------------|----------------|
| INP-001 | In Progress | Booking Info Screen | Happy | Patient logged in. Offer accepted, booking confirmed, provider has checked the patient in (case status: **In Progress**). | 1. Navigate to the In Progress section of the app. 2. Tap the active In Progress case. 3. Open or navigate to the Booking Info Screen / tab. 4. Review all displayed fields. | In Progress case. Provider: Estepera Clinic. Appointment: 2026-07-15. Treatment: FUE Hair Transplant. | Booking Info shows: case ID, provider name, clinic address, appointment date, treatment type, booking status (`In Progress`), assigned clinician name. All data matches what was in the accepted offer. | _(fill in)_ | _(fill in)_ |
| INP-002 | In Progress | Booking Info Screen | Edge | Patient logged in. Offer accepted. Booking **confirmed** but provider has **not yet checked in** the patient (case status: **Confirmed**). | 1. Navigate to an accepted case that is `Confirmed` (payment done, but treatment not yet started). 2. Open the Booking Info view. | Case status: `Confirmed`. Check-in not yet done by provider. | Booking Info shows correct booking details. Treatment has not started. No "In Progress" day progress visible. Status badge: `Confirmed`. | _(fill in)_ | _(fill in)_ |
| INP-003 | In Progress | Provider Tab Screen | Happy | Patient logged in. Case status: **In Progress**. | 1. Open the active In Progress case. 2. Navigate to the Provider Tab. 3. Review all displayed provider information. | Active case. Provider: Estepera Clinic, Canada. Clinician: Dr. Ahmed (example). | Provider Tab shows: clinic name, clinic address, clinic contact (phone/email), assigned clinician name, provider credentials summary, provider rating. All data read-only. | _(fill in)_ | _(fill in)_ |
| INP-004 | In Progress | Problem Tab Screen | Happy | Patient logged in. Case status: **In Progress**. | 1. Open the active In Progress case. 2. Navigate to the Problem Tab. 3. Review all displayed problem/medical information. | Inquiry seed data: treatment type Hair, nature of concern "Receding hairline...", duration "1-2 years", severity 7. | Problem Tab shows: treatment type, nature of concern, duration of concern, previous treatments, symptom severity (displayed as number or visual scale), medical alert level. Matches what was submitted in the original inquiry. All read-only. | _(fill in)_ | _(fill in)_ |
| INP-005 | In Progress | Treatment Tab Screen | Happy | Patient logged in. Case status: **In Progress**. Treatment plan has multiple days (e.g., 4-day plan). Some days started, some pending. | 1. Open the active In Progress case. 2. Navigate to the Treatment Tab. 3. Review the day-by-day treatment plan list. | 4-day treatment plan. Day 1: `Finished`. Day 2: `In progress`. Day 3: `Not started`. Day 4: `Not started`. | Treatment Tab shows: one row per treatment day. Each row: day number, day label/description (from provider's treatment plan), status badge. Day 1 badge: `Finished`. Day 2 badge: `In progress`. Days 3–4: `Not started`. Estimated graft count displayed. Actual graft count shown as pending (not yet confirmed). | _(fill in)_ | _(fill in)_ |
| INP-006 | In Progress | Treatment Tab Screen | Happy | Patient logged in. Case status: **In Progress**. At least 1 day in Treatment Tab. | 1. Open Treatment Tab. 2. Tap on any treatment day row. 3. Observe the Day Details Popup. | Tap Day 1: "Day 1 of 4 — Consultation & Scans", status: `Finished`. | Day Details Popup appears: shows day number, day description, and current status badge. Close action available (tap outside or Close button). Popup dismissed returns to Treatment Tab. No editing available from patient side. | _(fill in)_ | _(fill in)_ |
| INP-007 | In Progress | Treatment Tab Screen | Happy | Patient logged in. Provider has just checked the patient in. No days have been updated yet. | 1. Open the Treatment Tab immediately after check-in (all days at initial state). | All 4 days status: `Not started`. | All day rows show status badge `Not started`. No progress percentage or completion shown. Treatment is "live" but no days advanced yet. | _(fill in)_ | _(fill in)_ |
| INP-008 | In Progress | Treatment Tab Screen | Edge | Patient logged in. Case: In Progress. Mixed day statuses — some terminal, some still active. | 1. Open Treatment Tab with mixed day statuses. 2. Tap each day row to view Day Details Popup. | Day 1: `Finished`. Day 2: `Finished`. Day 3: `Need caution/attention`. Day 4: `Not started`. | Each day shows correct status badge. Day 3 may have a distinct visual indicator (caution color). Day 4 `Not started` still visible. Treatment not yet complete (not all days terminal). | _(fill in)_ | _(fill in)_ |
| INP-009 | In Progress | Treatment Tab Screen | Edge | Patient logged in. Case: In Progress. **All days** are in terminal status (Finished, Cancelled/Deferred, or Need caution/attention). | 1. Open Treatment Tab when all days are in terminal status. 2. Observe whether the UI changes to signal treatment completion (patient-facing cue). | All 4 days: `Finished`. | Treatment Tab shows all days with `Finished` badge. Patient-facing notice or progress indicator may show "All treatment days completed." Patient awaits provider to trigger End Treatment — no patient action required here. | _(fill in)_ | _(fill in)_ |
| INP-010 | In Progress | End of Treatment Screen | Happy | Patient logged in. Provider has completed the End of Treatment workflow (case status transitions from `In Progress` → `Completed`). Patient receives completion notification. | 1. Open the app after receiving the treatment completion notification. 2. Navigate to the previously In Progress case. 3. Observe the End of Treatment / Completed Treatment Screen. | Provider completed End of Treatment: conclusion notes written, prescription given, actual graft count 2,450, before/after photos uploaded. | Screen shows read-only completed treatment summary: actual graft count (2,450), treatment summary / conclusion note, prescription text, post-op advice, medication instructions. Before/after photos viewable. Status badge: `Completed`. No "In Progress" day progress visible (replaced by completion summary). | _(fill in)_ | _(fill in)_ |
| INP-011 | In Progress | End of Treatment Screen | Happy | Prerequisite: INP-010 completed (case = `Completed`). | 1. From the End of Treatment Screen, locate the post-op instruction fields. 2. Verify all three fields are present and populated. | Prescription, Advice, and Medication Instructions set by provider at End of Treatment. | Post-op instruction fields visible and populated: (1) Prescription — medication names/dosages, (2) Advice — recovery guidance text, (3) Medication Instructions — drug name, dosage, frequency, duration. All read-only; no editing option for patient. | _(fill in)_ | _(fill in)_ |
| INP-012 | In Progress | End of Treatment Screen | Edge | Prerequisite: INP-010 completed. Provider uploaded before/after photos. | 1. On the End of Treatment Screen, navigate to the before/after photo section. 2. Tap individual photos to view full-screen. | Before/after photos uploaded by provider (2 before, 2 after). | Photo gallery section visible. Before and after photos shown. Tapping a photo opens a full-screen viewer. Photos are correctly labeled as before/after. Download or share option may or may not be present — note what's shown. | _(fill in)_ | _(fill in)_ |
| INP-013 | In Progress | Full In Progress Lifecycle | Integration | Patient logged in. Case status: **In Progress** with all 4 tabs available. | 1. Open the In Progress case. 2. Navigate to Booking Info tab — verify all booking data. 3. Switch to Provider tab — verify provider details. 4. Switch to Problem tab — verify hair concern data matches inquiry. 5. Switch to Treatment tab — verify day rows with statuses. 6. Tap Day 1 row → Day Details Popup → Close. 7. Tap Day 2 row → Day Details Popup → Close. 8. Navigate back to inquiry list. | All seed data from inquiry, offer, and provider end-of-day updates. | All 4 tabs accessible and display correct, consistent data. Navigation between tabs smooth (no crashes, no data reload delays > 3s). Back navigation works. Day Details Popup opens and closes correctly from Treatment tab. | _(fill in)_ | _(fill in)_ |

---

## Section 4: Aftercare Module

> **Context**: Covers the full aftercare experience after treatment completion. The app enters this phase automatically (treatment-linked) or via manual purchase (standalone). Test cases cover the dashboard, milestones, questionnaire screens (pain assessment, text input, MCQ, dropdown), scan upload, medication/instruction views, the standalone service purchase flow, and the Completed Inquiry Dashboard Card.
>
> **Source PRDs**: FR-011 (Aftercare & Recovery Management). Questionnaire screen types (Pain Assessment, Text Input, MCQ, Dropdown) are driven by FR-025 (Medical Questionnaire Management).
>
> **Note on Standalone vs Treatment-Linked**: Most test cases here assume treatment-linked aftercare (automatically activated after End of Treatment). Tests AFC-020–AFC-025 cover the standalone aftercare service purchase path.

| ID | Module | Flow / Screen | Case Type | Prerequisites | Testing Steps | Testing Data | Expected Result | Actual Result | Status & Notes |
|----|--------|--------------|-----------|---------------|---------------|--------------|-----------------|---------------|----------------|
| AFC-001 | Aftercare | My List Dashboard Screen | Happy | Patient logged in. Provider completed End of Treatment. Aftercare plan **activated** (treatment-linked). Patient received activation notification. | 1. Open the app. 2. Navigate to the Aftercare section. 3. Open My List / Aftercare Dashboard. | Treatment-linked aftercare, plan: "Standard FUE Aftercare - 12 months". | Dashboard shows: active aftercare plan name, overall progress indicator, next milestone due date, last scan upload status, last questionnaire status, and a list of upcoming tasks. Plan status: `Active`. | _(fill in)_ | _(fill in)_ |
| AFC-002 | Aftercare | My List Dashboard Screen | Edge | Patient logged in. **No aftercare** plan has been activated for this patient. | 1. Navigate to the Aftercare section. 2. Open the Aftercare Dashboard. | No aftercare plan exists for this patient. | Empty state displayed: "No aftercare plan active." Option to request standalone aftercare service shown (link to Aftercare Services Screen). No errors. | _(fill in)_ | _(fill in)_ |
| AFC-003 | Aftercare | My List Dashboard Screen | Happy | Prerequisite: AFC-001 (aftercare active). Patient has completed some tasks (1 scan uploaded, 1 questionnaire done). | 1. From Aftercare Dashboard, review the progress summary fields. | 1 scan uploaded, 1 questionnaire submitted. Milestone 1: partially complete. | Dashboard updates: last scan upload shows date and `Uploaded` status. Last questionnaire shows date and `Completed` status. Progress indicator reflects partial completion. | _(fill in)_ | _(fill in)_ |
| AFC-004 | Aftercare | Aftercare Milestones Screen | Happy | Prerequisite: AFC-001 (aftercare active). Multiple milestones defined: some upcoming, some completed. | 1. From Aftercare Dashboard, navigate to the Milestones Screen. 2. Observe the milestones list. | Plan with 4 milestones: Week 1 (completed), Week 4 (upcoming), Month 3 (upcoming), Month 6 (upcoming). | Milestones list shows all 4 entries with correct labels and due dates. Week 1 shows `Completed` badge. Others show `Upcoming` or `Pending` badge. Milestones are ordered chronologically. | _(fill in)_ | _(fill in)_ |
| AFC-005 | Aftercare | Aftercare Milestones Screen | Edge | Prerequisite: AFC-001 (aftercare active). At least 1 milestone is **overdue** (due date in the past, not completed). | 1. Navigate to Milestones Screen. 2. Identify the overdue milestone. | Week 4 milestone due date has passed without completion. | Overdue milestone shows `Overdue` badge (distinct color — typically red/amber). Overdue status clearly differentiated from `Upcoming` and `Completed`. May display urgency notice or prompt to complete. | _(fill in)_ | _(fill in)_ |
| AFC-006 | Aftercare | Milestone Detail Screen | Happy | Prerequisite: AFC-001 (aftercare active). At least 1 **pending** milestone. | 1. From Milestones Screen, tap a pending milestone. 2. Observe Milestone Detail Screen. 3. Review all fields and available actions. | Week 4 milestone (pending). Contains: scan upload task + pain assessment questionnaire. | Milestone Detail shows: milestone name ("Week 4 Check-in"), due date, list of required tasks (scan upload, questionnaire), completion status per task. Action buttons for each task: `Upload Scan`, `Complete Questionnaire`. Task buttons lead to respective screens. | _(fill in)_ | _(fill in)_ |
| AFC-007 | Aftercare | Milestone Detail Screen | Edge | Prerequisite: AFC-004 (Week 1 milestone completed). | 1. From Milestones Screen, tap the completed milestone (Week 1). 2. Observe Milestone Detail Screen. | Week 1 milestone: all tasks completed. | Milestone Detail shows `Completed` badge. All tasks show completed state with completion timestamps. No action buttons active (tasks locked as read-only). | _(fill in)_ | _(fill in)_ |
| AFC-008 | Aftercare | Scan Upload Screen | Happy | Prerequisite: AFC-006 (pending milestone). Tap "Upload Scan" from Milestone Detail. | 1. From Milestone Detail, tap "Upload Scan". 2. Observe Scan Upload Screen. 3. Upload 3 photos (JPG, ~1MB each). 4. Submit. | 3 head scan photos: front view, left side view, top-down view. Each ~1MB, JPG format. Good lighting, clear hair/scalp visible. | Scan Upload Screen shows instructions for photo capture. Photo picker/camera available. After selecting 3 photos: thumbnail previews shown. Submit button active. On submit: success confirmation shown, milestone scan task marked `Completed`. | _(fill in)_ | _(fill in)_ |
| AFC-009 | Aftercare | Scan Upload Screen | Edge | Prerequisite: On Scan Upload Screen. | 1. Attempt to upload more photos than the allowed limit. | Upload limit: 5 photos (from FR-003 upload policy). Attempt: 6 photos. | Error message or system block: "You can upload a maximum of [N] photos per submission." Photos beyond the limit not accepted. Previously selected photos within the limit retained. | _(fill in)_ | _(fill in)_ |
| AFC-010 | Aftercare | Scan Upload Screen | Error | Prerequisite: On Scan Upload Screen. | 1. Attempt to select and upload a file with an unsupported format (e.g., PDF or GIF). | Upload file: `test-document.pdf` (~500KB). | Error message displayed: "Unsupported file type. Please upload JPG or PNG images." File rejected. No crash. | _(fill in)_ | _(fill in)_ |
| AFC-011 | Aftercare | Scan Upload Screen | Error | Prerequisite: On Scan Upload Screen. Photos selected. Network connectivity disabled (airplane mode or simulated API failure). | 1. Select valid photos. 2. Enable airplane mode. 3. Tap Submit. 4. Observe error handling. | 3 valid JPG photos. Network unavailable. | Error message: "Upload failed. Please check your connection and try again." Upload not lost — photos may remain selected. Retry option available. No crash. | _(fill in)_ | _(fill in)_ |
| AFC-012 | Aftercare | Pain Assessment Screen | Happy | Prerequisite: AFC-006 (pending milestone with questionnaire). Tap "Complete Questionnaire" from Milestone Detail. Questionnaire type: Pain Assessment. | 1. From Milestone Detail, tap "Complete Questionnaire". 2. On Pain Assessment Screen, answer all questions. 3. Submit. | Pain level slider: `3` (out of 10). Affected areas: `Crown, temples` (if multi-select). Additional pain description: `Mild soreness, no swelling`. | Pain Assessment Screen renders correctly. Questions displayed. Slider functional (0–10). Submit enabled after all required questions answered. On submit: questionnaire recorded, milestone questionnaire task marked `Completed`. | _(fill in)_ | _(fill in)_ |
| AFC-013 | Aftercare | Pain Assessment Extended Screen | Edge | Prerequisite: AFC-012 — but with a flagged answer that triggers extended follow-up. | 1. On Pain Assessment Screen, set pain level to `7` (high — likely to trigger follow-up). 2. Submit. 3. Observe if extended screen appears. | Pain level: `7`. Complication question: `Yes, I have noticed unusual swelling`. | Pain Assessment Extended Screen appears with follow-up questions (detailed symptom fields, onset date, severity). Patient completes extended questions. On final submit: questionnaire recorded with flag. Aftercare team may be alerted. | _(fill in)_ | _(fill in)_ |
| AFC-014 | Aftercare | Question Text Input Screen | Happy | Prerequisite: On an aftercare questionnaire with a text-input question. | 1. Navigate to a questionnaire with a text input question. 2. Tap the text input field. 3. Enter a valid answer. 4. Proceed to next question or submit. | Text input field. Answer: `Mild soreness around the transplanted area, no swelling noted. Healing appears normal.` (< 500 chars). | Text field accepts the input. Character count indicator shown (if applicable). No formatting errors. "Next" or "Submit" button active. | _(fill in)_ | _(fill in)_ |
| AFC-015 | Aftercare | Question Text Input Screen | Edge | Prerequisite: On a questionnaire with a **required** text input question. | 1. Leave the text input field empty. 2. Attempt to proceed to the next question or submit. | Required text field: empty. | Validation error shown: "This field is required." or equivalent inline error. Cannot proceed until field is filled. No crash. | _(fill in)_ | _(fill in)_ |
| AFC-016 | Aftercare | Question Multiple Choice Screen | Happy | Prerequisite: On a questionnaire with a multiple-choice question. | 1. Navigate to a MCQ question. 2. Tap one answer option. 3. Verify selection state. 4. Proceed. | MCQ question: "How would you describe your sleep quality?". Options: `Sleeping well (7–8 hrs)`, `Occasionally disrupted`, `Frequently disrupted`, `Unable to sleep`. Select: `Sleeping well (7–8 hrs)`. | Selected option is visually highlighted. Only one option selectable at a time (single-select). "Next" button active after selection. Selection is retained if user navigates back. | _(fill in)_ | _(fill in)_ |
| AFC-017 | Aftercare | Question Dropdown Screen | Happy | Prerequisite: On a questionnaire with a dropdown question. | 1. Navigate to a dropdown question. 2. Tap the dropdown control. 3. Select an option from the dropdown list. 4. Proceed. | Dropdown question: "Current activity level". Options: `Bed rest`, `Light activity only`, `Moderate activity`, `Full activity`. Select: `Light activity only`. | Dropdown opens correctly. All options listed. Selected option shown in the dropdown field. "Next" button active after selection. | _(fill in)_ | _(fill in)_ |
| AFC-018 | Aftercare | Medication Screen | Happy | Prerequisite: AFC-001 (aftercare active). Provider specified medications at End of Treatment. | 1. From Aftercare Dashboard or Milestone Detail, navigate to the Medication Screen. 2. Review the medication schedule. | Medications: (1) Minoxidil 5% — apply once daily, 6 months. (2) Finasteride 1mg — one tablet daily, 12 months. (3) Antibiotic — one tablet 3x/day, 7 days. | Medication Screen shows each medication with: name, dosage, frequency, duration, and any special instructions. Information is read-only. | _(fill in)_ | _(fill in)_ |
| AFC-019 | Aftercare | Instruction Screen | Happy | Prerequisite: AFC-001 (aftercare active). Provider added post-op instructions. | 1. From Aftercare Dashboard or relevant milestone, navigate to the Instruction Screen. 2. Review displayed instructions. | Post-op advice includes: washing instructions, sleeping position guidance, sun exposure restrictions, activity restrictions (no heavy exercise for 2 weeks). | Instruction Screen displays all post-op guidance. Content is read-only. Instructions presented clearly (may be categorized or in a scrollable list). | _(fill in)_ | _(fill in)_ |
| AFC-020 | Aftercare | External Treatment Info Screen | Happy | Patient logged in. Patient had treatment at an **external clinic** (not Hairline). Navigating to request standalone aftercare. | 1. Navigate to Aftercare Services. 2. Select standalone aftercare. 3. On the External Treatment Info Screen, fill in all required fields. 4. Proceed. | External treatment details: Treatment date: `2026-03-01`. Treatment type: `FUE Hair Transplant`. Clinic name: `Istanbul Hair Center`. Location: `Istanbul, Turkey`. Approximate graft count: `2,000`. | All fields accept input correctly. Validation passes when all required fields filled. Proceed button active. Data carries forward to service selection step. | _(fill in)_ | _(fill in)_ |
| AFC-021 | Aftercare | External Treatment Info Screen | Edge | Prerequisite: On External Treatment Info Screen. | 1. Leave required fields empty (clinic name, treatment date). 2. Attempt to proceed. | Required fields: Treatment date = empty. Clinic name = empty. | Inline validation errors shown for empty required fields: "Treatment date is required", "Clinic name is required". Proceed button disabled or submission blocked. | _(fill in)_ | _(fill in)_ |
| AFC-022 | Aftercare | Aftercare Services Screen | Happy | Patient logged in. Navigating from External Treatment Info Screen (standalone path) or from the empty dashboard (AFC-002). | 1. Navigate to Aftercare Services Screen. 2. Browse available service packages. 3. Tap a package to view details. | Packages available: "Standard FUE Aftercare – 6 months" (USD 299), "Premium FUE Aftercare – 12 months" (USD 499). | Services Screen shows a list of available aftercare packages. Each entry: package name, duration, description, price. Tapping a package shows a detail view or expands details. Proceed to checkout available. | _(fill in)_ | _(fill in)_ |
| AFC-023 | Aftercare | Aftercare Services Screen | Edge | Patient logged in. **No aftercare packages** are currently available (all packages unpublished or filtered out). | 1. Navigate to Aftercare Services Screen. 2. Observe the screen when no packages match. | No aftercare packages published or compatible with patient's profile. | Empty state displayed: "No aftercare services are currently available." No packages listed. Contact support option may be shown. No crash. | _(fill in)_ | _(fill in)_ |
| AFC-024 | Aftercare | Aftercare Checkout Screen | Happy | Prerequisite: AFC-022 (package selected). On Aftercare Checkout Screen. | 1. From Aftercare Services, select "Standard FUE Aftercare – 6 months" (USD 299). 2. Proceed to Aftercare Checkout. 3. Enter payment details. 4. Accept terms. 5. Submit payment. | Package: Standard FUE Aftercare – 6 months, USD 299. Card: `4242 4242 4242 4242`, expiry `12/27`, CVV `123`, name `Test Patient`. | Checkout Screen shows order summary (package name, duration, price), payment form, and terms checkbox. On successful payment: confirmation screen shown, email sent to patient, request status → `Pending Assignment`. | _(fill in)_ | _(fill in)_ |
| AFC-025 | Aftercare | Aftercare Checkout Screen | Error | Prerequisite: AFC-022 (package selected). Simulated payment failure (use declined test card). | 1. On Aftercare Checkout, enter a declined card. 2. Submit payment. 3. Observe error handling. | Declined card: `4000 0000 0000 0002`, expiry `12/27`, CVV `123`. | Payment failure error displayed: "Payment declined. Please check your card details or try a different payment method." Retry option available. No duplicate payment created. Checkout remains accessible for retry. | _(fill in)_ | _(fill in)_ |
| AFC-026 | Aftercare | Completed Inquiry Dashboard Card | Happy | Patient logged in. Treatment has been completed (provider triggered End of Treatment). Case status: `Completed`. | 1. Navigate to the main Inquiry list / dashboard. 2. Locate the completed inquiry card. 3. Observe the card's content and status. | Completed treatment case. FUE Hair Transplant with Estepera Clinic. | Dashboard card displays: inquiry/case identifier, treatment type, provider name, completion date, status badge `Completed` (or `Aftercare` if aftercare is active). Card is tappable and navigates to the case detail. | _(fill in)_ | _(fill in)_ |
| AFC-027 | Aftercare | Completed Inquiry Dashboard Card | Happy | Prerequisite: AFC-026. Aftercare is active (AFC-001). | 1. Tap the Completed/Aftercare inquiry card on the dashboard. 2. Verify where it navigates. 3. Navigate back to the dashboard. | Active aftercare. Completed treatment. | Tapping the card navigates to the correct detail screen (End of Treatment view or Aftercare Dashboard — note which). Back navigation returns correctly to inquiry list. Status on card matches actual case state. No stale state shown. | _(fill in)_ | _(fill in)_ |
| AFC-028 | Aftercare | Full Aftercare Lifecycle | Integration | Patient logged in. Aftercare active. All prerequisite data set up: pending milestone with scan + questionnaire tasks. | 1. Open Aftercare Dashboard (AFC-001). 2. Navigate to Milestones Screen. 3. Tap pending milestone. 4. From Milestone Detail, tap "Upload Scan". 5. Upload 3 valid head scan photos. 6. Return to Milestone Detail. 7. Tap "Complete Questionnaire". 8. Answer all questions (Pain level 3, MCQ: Sleeping well, Dropdown: Light activity, Text: "No swelling"). 9. Submit questionnaire. 10. Return to Milestone Detail — verify both tasks marked complete. 11. Return to Dashboard — verify progress updated. 12. Check Medication Screen. 13. Check Instruction Screen. | Scan: 3 JPG photos. Questionnaire answers from standard data set (see Standard Mock Data above). | All steps complete without error. After completing scan and questionnaire: milestone task statuses → `Completed`. Dashboard progress updated. Navigation between screens smooth (no crashes). Medication and Instruction screens load and display provider-set content correctly. | _(fill in)_ | _(fill in)_ |

---

## Appendix: Testing Observations & Raw Data

> **Purpose**: This section is the free-form scratchpad for the testing session. Use it to record:
> - Raw API responses (JSON payloads) that explain unexpected behavior
> - Screenshots or screen recording links
> - Reproduction steps for intermittent bugs
> - Environment notes (app version, device, OS version, network)
> - Blocker status and related ticket references
> - Cross-test observations (e.g., a bug found in OFF-022 that also affects INQ-008)
>
> Keep entries dated and attributed. Format is flexible — just keep it traceable back to a test case ID.

### Environment Info

_(Fill in before testing starts)_

| Field | Value |
|-------|-------|
| App Version | _(e.g., 1.2.3-build 204)_ |
| Device | _(e.g., iPhone 15 Pro, iOS 18.1)_ |
| Test Environment | _(staging / dev / prod)_ |
| Backend API Version | _(fill in)_ |
| Test Session Start | _(fill in)_ |
| Test Session End | _(fill in)_ |
| Tester | _(fill in)_ |

---

### Observation Log

> Format each entry as: `[DATE TIME] [TEST-ID] Description of observation / raw data`

```
[YYYY-MM-DD HH:MM] [TEST-ID] — Paste raw API response, error logs, or observation notes here.

Example:
[2026-04-22 10:35] [OFF-022] — Acceptance API returned 200 but inquiry status did not update in the UI. 
Raw response: { "status": "success", "data": { "id": "...", "status": "accepted" } }
UI still showing "Quoted" badge after 30 seconds. Possible state sync issue.
```

---

### Known Issues at Test Start

> List any known pre-existing issues (from previous test sessions) that may affect results. Reference the test case IDs likely to be impacted.

| Issue | Affected Test IDs | Status |
|-------|-------------------|--------|
| `ParseFailure` on quote creation when `duration_of_concern` is null (top-level field null, value only in `problem_detail`) | OFF-001, OFF-012, OFF-022, OFF-026, INP-001 to INP-013 | _(open / resolved — check before testing)_ |
| P02.1 (Compare Offers) blocked by ParseFailure — could not verify in 2026-03-30 round | OFF-012, OFF-013, OFF-014, OFF-015 | _(open / resolved)_ |
| P04.1 / P04.2 (Passport/Flight submission) blocked by ParseFailure in 2026-03-30 round | Not in scope for this test | N/A |

---

*End of Document*
