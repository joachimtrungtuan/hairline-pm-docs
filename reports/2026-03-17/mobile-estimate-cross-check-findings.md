# Mobile Dev Estimate Cross-Check Findings

**Report Date**: 2026-03-17
**Report Type**: Scope & Alignment Audit
**Platform**: Patient Mobile App
**Source File**: `Hairline - Missing Flows Timeline - Feature Estimates & Timelines.csv` (same folder)
**Reference Documents**:

- `local-docs/reports/2026-02-05/missing-mobile-flows-design-complement.md` (v1.0 Final)
- FR PRDs under `local-docs/project-requirements/functional-requirements/`

**Purpose**: Cross-check the mobile development team's effort estimation against the approved design complement specification and underlying functional requirements. Identify discrepancies, scope gaps, FR violations, and items requiring clarification before implementation begins.

---

## Estimate Summary

| Category | Hours | Cost |
|----------|-------|------|
| Mobile FE | 92.5 | $2,081 |
| API Integration | 148 | $3,330 |
| Sub Total | 240.5 | $5,411 |
| Discount | — | -$1,000 |
| **Total** | **240.5** | **$4,411** |

Rate: $22.50/hour for both FE and API.

---

## Finding Categories

- **Scope Gap**: Item specified in design complement / FRs but missing from the estimate
- **Extra Scope**: Item in the estimate but not in the design complement's 15 missing flows
- **Discrepancy**: Same feature but different fields, behavior, or approach
- **FR Violation**: Conflicts with a functional requirement
- **Naming/Terminology**: Inconsistency that could cause confusion during implementation

---

## Findings

### 1. Travel Submission Flows — Entirely Missing from Estimate

**Category**: Scope Gap
**Severity**: High
**Affected Flows**: P04.1 (Passport Submission — Path A), P04.2 (Flight & Hotel Submission — Path B)
**Design Complement Screens**: P04.1-S1, P04.1-S2, P04.2-S1, P04.2-S2, P04.2-S3, P04.2-S4, P04.2-S5 (7 screens total)

The CSV covers read-only display of travel information inside the "In Progress > Booking Info Screen" (hotel details, flight details in the booking detail view). However, the **data collection flows** for travel are completely absent:

- **P04.1**: Passport Submission Form + Read-Only View (Path A — provider-included travel)
- **P04.2**: Travel Requirement Check ("Do you need travel?"), Outbound/Return Flight Submission, Hotel Submission, Read-Only View, Travel Itinerary View (Path B — patient self-booked)

These flows are triggered automatically when a booking reaches Confirmed status (FR-008 REQ-008-005) and are core to the patient journey. Without them, the booking detail screen has no source of travel data to display.

**Action Required**: Add all 7 travel submission screens to the estimate, or confirm they are already built and intentionally excluded.

---

### 2. Flight Detail — Total Price Field (FR Violation)

**Category**: FR Violation
**Severity**: High
**CSV Location**: Lines 319–320 ("Total Price Label", "Total Price Value") within In Progress > Booking Info Screen > Flight Details Section

The CSV includes a total price field in the flight detail display. This is **explicitly prohibited** by FR-008 REQ-008-009:

> *"`total_price` is explicitly excluded from this form. Flight cost is captured at the package/quote level (FR-004/FR-007)."*

The design complement P04.2-S2 also excludes this field. Including it creates a data integrity risk — there is no source for this value in the travel submission flow.

**Action Required**: Remove "Total Price Label" and "Total Price Value" from the flight detail section.

---

### 3. Flight Detail — Passenger Name and Seat Fields (Extra Fields)

**Category**: Discrepancy
**Severity**: Medium
**CSV Location**: Lines 315–322 ("Passenger Name Label/Value", "Seat Label/Value") within In Progress > Booking Info Screen > Flight Details Section

These fields appear in the CSV's flight detail section but are **not defined** in:

- Design complement P04.2-S2 (Flight Submission Form)
- FR-008's flight record field list

The design complement's flight fields are: airline name, flight number, departure/arrival airports, departure/arrival dates and times, ticket confirmation number, ticket class, baggage allowance, and special requests. "Passenger Name" and "Seat" are not part of the approved data model.

**Action Required**: Remove these fields, or provide justification and request a spec amendment.

---

### 4. Help & Support — Entirely Missing from Estimate

**Category**: Scope Gap
**Severity**: High
**Affected Flow**: P08.1 (Help & Support)
**Design Complement Screens**: P08.1-S1, P08.1-S2, P08.1-S3, P08.1-S4, P08.1-S5 (5 screens)

The CSV contains zero coverage for the patient Help & Support experience:

| Missing Screen | Purpose |
|---------------|---------|
| P08.1-S1: Help & Support Hub | Central entry point with search, browse, contact, tickets |
| P08.1-S2: Help Center Browser | Browse FAQs, Articles, Resources, Videos (4 content types) |
| P08.1-S3: My Support Tickets | List patient's support cases with filters |
| P08.1-S4: Ticket Detail | Full case thread with reply capability |
| P08.1-S5: Contact Support Form | Structured form for new support requests |

Multiple other flows route users to Help & Support: Cancel Inquiry (P02.2), Delete Account (P01.1), Payment Methods (P03.1), Expired Quotes (P02.3), and Travel Records (P04.1/P04.2). Without this module, those "Contact Support" CTAs have no destination.

**Action Required**: Add all 5 Help & Support screens to the estimate, or confirm they are already built.

---

### 5. Settings — Missing Main Screen and Notification Settings

**Category**: Scope Gap
**Severity**: Medium
**Affected Flow**: P01.2 (Settings Screen)
**Missing Screens**: P01.2-S1 (Settings Main Screen), P01.2-S2 (Notification Settings)

The CSV includes Privacy & Security, Change Password, Privacy Policy, and Terms & Conditions screens. However, it is missing:

- **P01.2-S1 (Settings Main Screen)**: The navigation hub that links to all settings sub-screens. Without it, there is no entry point to the screens that *are* estimated.
- **P01.2-S2 (Notification Settings)**: Global Email/Push toggles (MVP scope; per-category is V2). Required by FR-001 Screen 16 and FR-020 REQ-020-004.

**Action Required**: Add both screens, or confirm they are already implemented.

---

### 6. Expired Offers/Quotes — Missing from Estimate

**Category**: Scope Gap
**Severity**: Medium
**Affected Flow**: P02.3 (Expired Offers/Quotes)
**Design Complement Screens**: P02.3-S1 (Expired Quote Indicator), P02.3-S2 (All Quotes Expired State)

The design complement specifies:

- **P02.3-S1**: Visual treatment for expired quotes — grayed-out cards, "Expired" badge, disabled Accept button with explanatory tooltip, disabled Compare checkbox, static "Expired on [date]" replacing countdown timer
- **P02.3-S2**: Action state when all quotes have expired — explanation, Cancel Inquiry button, Contact Support link

Neither screen appears in the CSV. Quote expiry is a critical lifecycle event (default 48-hour window per FR-004 REQ-004-002) and patients will encounter expired quotes regularly.

**Action Required**: Add expired quote handling to the estimate.

---

### 7. Quote Comparison — Separate Screen vs. Inline Panel

**Category**: Discrepancy
**Severity**: Medium
**CSV Location**: Line 157, "Compare Offers Table Screen" (8h FE, 12h API — highest single-item estimate)

The CSV treats quote comparison as a **standalone dedicated screen**. The design complement P02.1 specifies it as a **conditional panel within the Inquiry Dashboard**:

> *"Quotes are displayed within the Inquiry Dashboard context; comparison is a conditional panel (not a separate screen)."* — P02.1 Business Rules

This is an architectural/navigation difference that affects:

- Navigation flow (new screen vs. inline expansion)
- Back-stack behavior
- State management (selection persists within dashboard context)

**Action Required**: Align on whether comparison stays inline (per spec) or moves to a separate screen. If the team prefers a separate screen, the spec change should be reviewed and approved before implementation.

---

### 8. Edit Payment Method — Card Credential Fields Must Be Read-Only in Edit Mode

**Category**: Discrepancy (PCI compliance implication)
**Severity**: High
**CSV Location**: Lines 884–893 ("Edit Payment Method Screen" with Card Number Field Prefilled, Cardholder Name Field, Expiry Date Field, CVV/CVC Field)

The CSV lists an Edit Payment Method screen, which is correct — the design complement P03.1-S2 defines a shared Add/Edit screen. However, the CSV presents all card fields (card number, expiry, CVV) as standard input fields alongside metadata fields, with no distinction between editable and read-only fields in edit mode.

The design complement P03.1-S2 specifies a clear split:

- **Editable in edit mode**: billing address, method nickname, default toggle
- **Read-only in edit mode**: card number (shown as masked "•••• 4242"), expiry date, CVV — these cannot be edited directly. Changing card credentials requires tapping "Replace card," which clears the form and re-renders the payment gateway's hosted secure fields for a fresh card entry, creating a new token

This distinction matters for PCI-DSS compliance (FR-007 REQ-007-008): card data must go through the payment gateway's hosted fields and is never transmitted to or stored on app servers. Displaying card credentials in standard editable form fields would violate this requirement.

**Action Required**: In the edit screen, card credential fields must be masked and read-only, with a "Replace card" action that triggers a new gateway-hosted field entry. Only metadata fields (billing address, nickname, default toggle) should be directly editable.

---

### 9. OTP Digit Count — Internal CSV Inconsistency

**Category**: Discrepancy
**Severity**: Low
**CSV Location**: Line 989 ("Enter the 4 digit code…") vs. Lines 990–996 (6 OTP input boxes)

The instruction text says "4 digit code" but the UI has 6 input boxes. Both the design complement (P01.1-S2) and FR-001 specify a **6-digit OTP**.

**Action Required**: Correct the instruction text to "6 digit code."

---

### 10. Review Status "Submitted" — Not a Valid Patient-Visible Status

**Category**: Naming/Terminology
**Severity**: Low
**CSV Location**: Line 761, "Status Badge (Submitted)" in My Reviews Screen

The design complement P05.3 defines only two patient-visible review statuses:

- **Published** (review is live and visible)
- **Removed by Admin** (admin removed for policy violation)

"Submitted" is not a valid state — reviews are published immediately upon submission with no moderation gate (per client transcription). The badge should be "Published."

**Action Required**: Replace "Submitted" with "Published" in the review status badges.

---

### 11. Notification UX — Multiple Approach Differences

**Category**: Discrepancy
**Severity**: Medium

| Feature | Design Complement (P06.1) | CSV Implementation |
|---------|--------------------------|-------------------|
| Filtering | Inline horizontal filter chips (10 categories) | Separate Filter Modal (lines 670–686) |
| Per-notification actions | Swipe-left: Mark as Read + Archive | Three-dot options menu (line 654) |
| Mark All as Read | Specified as button (P06.1-S2) | Not present |
| Date group headers | Today / Yesterday / This Week / Earlier | Not present |
| Pull-to-refresh | Specified | Not present |
| Notification bubble | Dedicated component spec (P06.1-S1) | Badge count in bottom nav only |
| Deep link from push tap | Specified behavior | Not addressed |

Individually these are not blockers, but collectively they represent a meaningfully different notification experience than what's specified.

**Action Required**: Review each difference and align on the intended UX before implementation. Some (filter modal vs. chips) are legitimate design choices; others (Mark All as Read, deep linking) are functional gaps.

---

### 12. Discount Code Screen — Additional Scope Not in Design Complement

**Category**: Extra Scope
**Severity**: Low (scope clarity issue)
**CSV Location**: Lines 234–246, "Discount Code Screen" (2h FE, 4h API)

This screen includes discount code input, cost breakdown (Provider Cost / Aftercare Cost / Discount / Total), and treatment/provider info. It is **not part of the 15 missing flows** in the design complement and does not appear in the FR-005 (Quote Comparison & Acceptance) screen list.

**Action Required**: Clarify whether this is intentionally bundled into this round. If yes, it should be called out as additional scope separate from the missing-flow package.

---

### 13. Aftercare Screens — Scope Ambiguity

**Category**: Extra Scope
**Severity**: Medium

The CSV's Aftercare module includes several screens that are **not part of the design complement's 15 missing flows**:

| CSV Screen | In Design Complement? | Notes |
|------------|----------------------|-------|
| External Treatment Info Screen | No | Step-based form for external treatment data |
| Aftercare Services Screen | No | Service selection with pricing |
| Aftercare Checkout Screen | No | Includes "Monthly Subscription" payment type (line 591) |

The "Monthly Subscription" payment type in the Aftercare Checkout is particularly notable — FR-007 and FR-007b define deposit, final payment, and installment payment models, but not a subscription model. This may represent new commercial scope.

**Action Required**: Clarify whether these screens are from existing Figma designs (already approved), or new additions that need spec approval. The subscription payment type needs explicit confirmation.

---

### 14. Delete Account — Deletion Reason Options Hardcoded

**Category**: Discrepancy
**Severity**: Low
**CSV Location**: Lines 948–959, "Deletion Reason Bottom Sheet" with 9 specific options

The CSV hardcodes specific deletion reason options:

- I no longer use this app
- I found a better alternative
- The app doesn't meet my needs
- Too many notifications or emails
- Concerns about privacy or data security
- I had technical issues or bugs
- The app is difficult to use
- I'm taking a break and may return later
- Others

The design complement P01.1-S1 states: *"Options are centrally managed (not hardcoded in this spec)."* The deletion reason is also specified as **optional** (not required).

These options should be fetched from an admin-configurable list, not hardcoded in the mobile app. The specific values listed in the CSV don't match any FR-sourced list.

**Action Required**: Implement deletion reasons as a dynamic list from the backend. Initial seed values can be defined, but the UI must support admin-managed options.

---

## Summary Table

| # | Finding | Category | Severity | Action |
|---|---------|----------|----------|--------|
| 1 | Travel submission flows (P04.1, P04.2) missing — 7 screens | Scope Gap | High | Add to estimate or confirm built |
| 2 | Flight detail includes prohibited `total_price` field | FR Violation | High | Remove field |
| 3 | Flight detail includes unspecified Passenger Name / Seat fields | Discrepancy | Medium | Remove or justify |
| 4 | Help & Support (P08.1) missing — 5 screens | Scope Gap | High | Add to estimate or confirm built |
| 5 | Settings main screen + notification settings missing | Scope Gap | Medium | Add or confirm built |
| 6 | Expired offers/quotes (P02.3) missing — 2 screens | Scope Gap | Medium | Add to estimate |
| 7 | Quote comparison: separate screen vs. spec's inline panel | Discrepancy | Medium | Align before implementation |
| 8 | Edit payment method: card fields must be read-only (PCI) | Discrepancy | High | Card fields masked + "Replace card" flow |
| 9 | OTP instruction says "4 digit" but UI has 6 boxes | Discrepancy | Low | Fix text to "6 digit" |
| 10 | Review status "Submitted" not valid per spec | Naming | Low | Use "Published" |
| 11 | Notification UX differs from spec in 7 areas | Discrepancy | Medium | Align before implementation |
| 12 | Discount Code screen is additional scope | Extra Scope | Low | Call out as extra or remove |
| 13 | Aftercare screens not in design complement (incl. subscription) | Extra Scope | Medium | Clarify source and approval |
| 14 | Delete account reason options hardcoded vs admin-managed | Discrepancy | Low | Use dynamic list from backend |

**High**: 4 findings (travel flows, flight total_price, Help & Support, payment edit mode PCI)
**Medium**: 5 findings
**Low**: 5 findings

---

## Recommended Next Steps

1. **Before implementation (High)**: Address Findings #1, #2, #4, #8 — scope gaps for travel/Help & Support, the prohibited total_price field, and the payment edit mode PCI requirement. These affect scope estimates and compliance.
2. **Before implementation (Medium)**: Align on Findings #5, #6, #7, #11 — missing settings/expired quote screens, comparison architecture, and notification UX approach. These are design decisions that affect navigation and interaction patterns.
3. **Housekeeping**: Resolve Findings #3, #9, #10, #14 — field corrections and naming fixes.
4. **Scope clarity**: Confirm Findings #12, #13 — whether extra items (Discount Code, Aftercare Checkout with subscriptions) are intentional additions or should be deferred.

Request the mobile team to revise the estimate with clear categorization:

- What is already built (excluded from this round)
- What is new scope (included)
- What is display-only vs. full submission flow
- What is future scope (should not be in this MVP round)
