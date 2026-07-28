# Design Layout Verification Report - FR-018 Admin + Affiliate

**Report Date**: 2026-07-08, continued 2026-07-09  
**Report Type**: Design Layout Verification  
**FR Scope**: FR-018 - Affiliate Management  
**Flow Scope**: Admin Platform Screens (A-07) and Affiliate Platform / AFF side screens.  
**Layout Source**: `layout-temp/`  
**Platform**: Admin Web and Affiliate Portal Web  
**Status**: 🔴 BLOCKED

---

## Summary Dashboard

| # | Flow | Module | Screens Required | Screens Verified | Layout Status | Field Coverage |
|---|------|--------|-----------------|-----------------|---------------|----------------|
| Admin-01 | Affiliate Management Dashboard | A-07: Affiliate Program Management | 1 | 1 | 🟡 PARTIAL | 13/13 required and listed fields covered; 1 conditional mismatch |
| Admin-02 | Add/Edit Affiliate Form | A-07: Affiliate Program Management | 1 | 1 | 🟡 PARTIAL | 20/20 fields covered; commission edit mismatch |
| Admin-03 | Affiliate Detail | A-07: Affiliate Program Management | 1 | 1 | 🔴 FAIL | Hub present, but critical action routing incomplete |
| Admin-03.1 | Suspend / Reinstate Affiliate Modal | A-07: Affiliate Program Management | 1 | 1 | 🔴 FAIL | Critical submit gate mismatch |
| Admin-03.2 | Edit Commission Structure Modal | A-07: Affiliate Program Management | 1 | 1 | 🔴 FAIL | Full edit page supplied instead of modal |
| Admin-03.3 | Deactivate / Offboard Affiliate Modal | A-07: Affiliate Program Management | 1 | 1 | 🔴 FAIL | Terminal action gate and copy mismatch |
| Admin-04 | Affiliate Code Generation | A-07: Affiliate Program Management | 1 | 1 | 🔴 FAIL | Required Application Method missing |
| Admin-04.1 | Code Generation Results | A-07: Affiliate Program Management | 1 | 1 | 🟡 PARTIAL | Core results present; retry mechanics unclear |
| Admin-05 | Promo Code Management | A-07: Affiliate Program Management | 1 | 1 | 🟢 GOOD | Core promo registry fields covered; minor action/color gaps |
| Admin-06 | Promo Code Detail | A-07: Affiliate Program Management | 1 | 1 | 🟢 GOOD | Shared detail covered; action typo and edit affordance gaps |
| Admin-07 | Affiliate Payout Status & History | A-07: Affiliate Program Management | 1 | 1 | 🟢 GOOD | Read-only payout workspace covered; minor label/metadata gaps |
| Admin-08 | Payout / Transaction Detail | A-07: Affiliate Program Management | 1 | 1 | 🟡 PARTIAL | Paid state complete; failed state drops required detail sections |
| AFF-09 | Affiliate Portal Shell | Affiliate Portal scoped surface | 1 | 1 | 🟢 COMPLETE | Four-tab shell present; refresh behavior not visually verifiable |
| AFF-09.1 | Overview Tab | Affiliate Portal scoped surface | 1 | 1 | 🟡 PARTIAL | 8/8 listed fields covered; monthly toggle, countdown, and refresh affordance missing |
| AFF-09.2 | Promo Codes Tab | Affiliate Portal scoped surface | 1 | 1 | 🟢 GOOD | List and detail fields covered; zero-referral initial state not shown |
| AFF-09.3 | Payouts Tab | Affiliate Portal scoped surface | 1 | 1 | 🟡 PARTIAL | Payout fields covered; below-threshold rollover note missing |
| AFF-09.4 | Profile Tab | Affiliate Portal scoped surface | 1 | 1 | 🟢 GOOD | Profile fields covered; immutable-email note missing |
| AFF-10 | Affiliate Onboarding & Activation | Affiliate Portal scoped surface | 1 | 1 | 🟡 PARTIAL | Flow screens supplied; activation email content not verifiable from layouts |
| AFF-10.1 | Set Password | Affiliate Portal scoped surface | 1 | 1 | 🟡 PARTIAL | 6/6 fields covered; valid-link status is only implied |
| AFF-10.2 | Resend Activation Email | Affiliate Portal scoped surface | 1 | 1 | 🟢 COMPLETE | Default, validation, success, and rate-limit states covered |
| AFF-10.3 | Welcome / Get Started | Affiliate Portal scoped surface | 1 | 1 | 🟢 GOOD | 7/7 fields covered; referral label typo and URL truncation |

**Overall**: Admin side and Affiliate side verification complete. Overall report remains 🔴 BLOCKED because admin-side critical blockers exist; AFF side is 🟡 PARTIAL with no AFF critical blocker.  
**Screens**: 21 of 21 specified admin and affiliate screens mapped and verified.

---

## Layout File Inventory

### Mapped to Spec Screens

| Layout File | Maps to Flow | Maps to Screen | Notes |
|-------------|-------------|----------------|-------|
| `layout-temp/Overview.png` | Admin-01 | Screen 1 (Affiliate Management Dashboard) | Dashboard main state |
| `layout-temp/Full Table (overview - admin).png` | Admin-01 | Screen 1 (Affiliate Management Dashboard) | Dashboard table detail |
| `layout-temp/Filter (overview - admin).png` | Admin-01 | Screen 1 (Affiliate Management Dashboard) | Dashboard filter state |
| `layout-temp/Add/Add New Affiliate.png` | Admin-02 | Screen 2 (Add/Edit Affiliate Form) | Add state |
| `layout-temp/Add/Edit Affiliate.png` | Admin-02 | Screen 2 (Add/Edit Affiliate Form) | Edit state |
| `layout-temp/Add/Fixed Amount per Booking.png` | Admin-02 | Screen 2 (Add/Edit Affiliate Form) | Fixed commission variant |
| `layout-temp/Save blocked.png` | Admin-02 | Screen 2 (Add/Edit Affiliate Form) | Validation / blocked save state |
| `layout-temp/Affiliate Detail.png` | Admin-03 | Screen 3 (Affiliate Detail) | Detail page |
| `layout-temp/Suspend/Reinstate Affiliate (Modal).png` | Admin-03.1 | Screen 3.1 (Suspend / Reinstate Affiliate Modal) | Status action modal |
| `layout-temp/Edit Commission Structure.png` | Admin-03.2 | Screen 3.2 (Edit Commission Structure Modal) | Commission edit screen / modal |
| `layout-temp/Fixed Amount.png` | Admin-04 | Screen 4 (Affiliate Code Generation) | Discount fixed amount variant |
| `layout-temp/Deactivate/Offboard Affiliate (Modal).png` | Admin-03.3 | Screen 3.3 (Deactivate / Offboard Affiliate Modal) | Offboarding modal |
| `layout-temp/Generate Affiliate Code - Single Affiliate.png` | Admin-04 | Screen 4 (Affiliate Code Generation) | Single affiliate code generation |
| `layout-temp/Generate Affiliate Code - Single Affiliate-1.png` | Admin-04 | Screen 4 (Affiliate Code Generation) | Code generation variant |
| `layout-temp/Generate Affiliate Code - Single Affiliate-2.png` | Admin-04 | Screen 4 (Affiliate Code Generation) | Code generation variant |
| `layout-temp/Code Generation Results.png` | Admin-04.1 | Screen 4.1 (Code Generation Results) | Results state |
| `layout-temp/Promo Code Management.jpg` | Admin-05 | Screen 5 (Promo Code Management) | Promo management main state |
| `layout-temp/Full Table (promo - admin).jpg` | Admin-05 | Screen 5 (Promo Code Management) | Promo table detail |
| `layout-temp/Filter (promo - admin).jpg` | Admin-05 | Screen 5 (Promo Code Management) | Promo filter state |
| `layout-temp/Promo Code Detail.jpg` | Admin-06 | Screen 6 (Promo Code Detail) | Promo code detail |
| `layout-temp/Payout Status & History - Overview.jpg` | Admin-07 | Screen 7 (Affiliate Payout Status & History) | Overview tab/state |
| `layout-temp/Payout Status & History - Current Cycle.jpg` | Admin-07 | Screen 7 (Affiliate Payout Status & History) | Current cycle state |
| `layout-temp/Payout Status & History - Billing History.jpg` | Admin-07 | Screen 7 (Affiliate Payout Status & History) | Billing history state |
| `layout-temp/Full Table (payout - admin).jpg` | Admin-07 | Screen 7 (Affiliate Payout Status & History) | Payout table detail |
| `layout-temp/Filter (payout - admin).jpg` | Admin-07 | Screen 7 (Affiliate Payout Status & History) | Payout filter state |
| `layout-temp/Transaction Detail.jpg` | Admin-08 | Screen 8 (Payout / Transaction Detail) | Transaction detail |
| `layout-temp/Payout/Transaction Detail - Status = Failed.jpg` | Admin-08 | Screen 8 (Payout / Transaction Detail) | Failed status variant |
| `layout-temp/Payout Status & History - Overview (aff).jpg` | AFF-09.1 | Screen 9.1 (Overview Tab) | Affiliate overview dashboard |
| `layout-temp/Promo Codes.jpg` | AFF-09.2 | Screen 9.2 (Promo Codes Tab) | Affiliate promo codes tab |
| `layout-temp/Full table (promo - aff).jpg` | AFF-09.2 | Screen 9.2 (Promo Codes Tab) | Affiliate promo table detail |
| `layout-temp/Filter (promo - aff).jpg` | AFF-09.2 | Screen 9.2 (Promo Codes Tab) | Affiliate promo filter state |
| `layout-temp/Promo Code Detail (aff).jpg` | AFF-09.2 | Screen 9.2 (Promo Codes Tab) | Affiliate promo code detail/drill-in |
| `layout-temp/Payouts (aff).jpg` | AFF-09.3 | Screen 9.3 (Payouts Tab) | Affiliate payouts tab |
| `layout-temp/Filter (payout - aff).jpg` | AFF-09.3 | Screen 9.3 (Payouts Tab) | Affiliate payout filter state |
| `layout-temp/Payout details (payout - aff).jpg` | AFF-09.3 | Screen 9.3 (Payouts Tab) | Affiliate payout detail/drill-in |
| `layout-temp/Profile (aff).jpg` | AFF-09.4 | Screen 9.4 (Profile Tab) | Affiliate profile tab |
| `layout-temp/Default Form.jpg` | AFF-10.2 | Screen 10.2 (Resend Activation Email) | Resend activation default form |
| `layout-temp/After Submission.jpg` | AFF-10.2 | Screen 10.2 (Resend Activation Email) | Resend success/generic submission state |
| `layout-temp/Rate Limited (More Than 3 Requests per Hour).jpg` | AFF-10.2 | Screen 10.2 (Resend Activation Email) | Resend rate-limited state |
| `layout-temp/Set Your Password.jpg` | AFF-10.1 | Screen 10.1 (Set Password) | Activation password form |
| `layout-temp/Validation Error.jpg` | AFF-10.1 | Screen 10.1 (Set Password) | Activation validation error state |
| `layout-temp/Validation Errors (Weak/Mismatched Password).jpg` | AFF-10.1 | Screen 10.1 (Set Password) | Weak/mismatched password state |
| `layout-temp/Expired or Already-Used Activation Link H Hairline.jpg` | AFF-10.1 | Screen 10.1 (Set Password) | Expired/already-used activation link state |
| `layout-temp/↳ Welcome/Welcome.jpg` | AFF-10.3 | Screen 10.3 (Welcome / Get Started) | First-login welcome state |

### Unmapped Files

| Layout File | Likely Purpose | Notes |
|-------------|---------------|-------|
| `layout-temp/Arrow.png` | Annotation asset | Outside spec screen review scope |
| `layout-temp/Arrow-1.png` | Annotation asset | Outside spec screen review scope |
| `layout-temp/Content.png` | Extracted/modal content asset | Outside spec screen review scope unless referenced by mapped modal |
| `layout-temp/Content-1.png` | Extracted/modal content asset | Outside spec screen review scope unless referenced by mapped modal |

---

## Detailed Verification by Flow

### Admin-01: Affiliate Management Dashboard

**Status**: 🟡 PARTIAL — required table fields are represented, but pagination and high-pending-payout warning behavior do not match the PRD.  
**Screens required**: 1  
**Layout files**: `layout-temp/Overview.png`, `layout-temp/Full Table (overview - admin).png`, `layout-temp/Filter (overview - admin).png`

#### Screen 1: Affiliate Management Dashboard (Overview)

**Layout**: `layout-temp/Overview.png`, `layout-temp/Full Table (overview - admin).png`, `layout-temp/Filter (overview - admin).png`

##### Flow Context

- **User arrives from**: Admin Dashboard > Affiliate Management, or from A4 bulk campaign setup entry.
- **Screen purpose**: Let admins scan affiliate performance, filter/select eligible affiliates, open affiliate detail/edit actions, and launch bulk code generation.
- **Entry point**: Present — `Overview.png` shows the Affiliate Management page and `Add New Affiliate`.
- **Exit path**: Present with minor terminology issues — row actions include `View`, `Edit`, `Suspend`, `Generate Report`; selected rows expose `Generate Code`.
- **Data continuity**: Correct for visible rows — affiliate identity, eligibility, referral, revenue, code, and payout data appear in the table.
- **Flow context issues**: `Generate Code` is singular while the bulk flow requires generating codes for selected affiliates; page size shows `10 / page` instead of the PRD's 25 affiliates per page.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Affiliate Name | Yes | ✅ | Visible in `Full Table (overview - admin).png` as names including `Glow & Grow Media`, `HairRevive Clinic Network`, and `Scalp Society UK`; matches PRD Screen 1 field row. |
| Contact Email | Yes | ✅ | Visible in `Full Table (overview - admin).png` as emails including `contact@glowgrow.com` and `partnerships@hairrevive.au`; matches PRD Screen 1 field row. |
| Total Referrals | N/A | ✅ | Visible in `Full Table (overview - admin).png` as numeric counts including `312`, `278`, and `195`; matches PRD Screen 1 field row. |
| Total Revenue | N/A | ✅ | Visible in `Full Table (overview - admin).png` as currency values including `$148,200` and `$134,500`; matches PRD Screen 1 field row. |
| Total Commissions Paid | N/A | ✅ | Visible in `Full Table (overview - admin).png` as currency values including `$18,640` and `$16,980`; matches PRD Screen 1 field row. |
| Pending Payout | N/A | ⚠️ | Visible in `Full Table (overview - admin).png` as values including `$2,340` and `$1,560`, but amounts above the PRD note threshold of `$1000` are not highlighted yellow. |
| Status | Yes | ✅ | Visible in `Full Table (overview - admin).png` as badges for `Active`, `Pending`, `Suspended`, and `Inactive`; matches PRD Screen 1 field row and status-indicator rule. |
| Country/Region | No | ✅ | Visible in `Full Table (overview - admin).png` as countries including `United States`, `Australia`, `United Kingdom`, `Vietnam`, `Canada`, `Singapore`, and `Germany`; matches PRD Screen 1 field row. |
| Affiliate Type | No | ✅ | Visible in `Full Table (overview - admin).png` as `Influencer`, `Clinic Partner`, `Organization`, and `Other`; matches PRD Screen 1 field row. |
| Performance Tier | N/A | ✅ | Visible in `Full Table (overview - admin).png` as `Gold`, `Silver`, `Bronze`, and unset rows; matches PRD Screen 1 field row. |
| Campaign Eligibility | N/A | ✅ | Visible in `Overview.png` and `Full Table (overview - admin).png` as `Eligible` and `Not Eligible`; matches PRD Screen 1 field row. |
| Active Codes Count | N/A | ✅ | Visible in `Full Table (overview - admin).png` as values including `3`, `5`, `2`, `1`, and `0`; matches PRD Screen 1 field row. |
| Actions | N/A | ⚠️ | Visible in `Overview.png`; row menu includes `View`, `Edit`, `Suspend`, and `Generate Report`. PRD uses `View Details`, and bulk banner uses singular `Generate Code` instead of `Generate Codes`. |

##### Conditional States

| State | Status | Evidence |
|-------|--------|----------|
| Multi-select bulk state | ✅ | `Overview.png` shows `3 selected`, `Generate Code`, and `Clear Selection`, matching the selected-affiliates path in PRD Screen 1 acceptance criteria. |
| Filter panel state | ✅ | `Filter (overview - admin).png` includes `Status`, `Country / Region`, `Affiliate Type`, `Language`, `Performance Tier`, `Campaign Eligibility`, and `Payout Setup`, matching PRD Screen 1 filtering rules. |
| Ineligible rows | ✅ | `Overview.png` and `Full Table (overview - admin).png` show `Not Eligible` badges on rows including `Nguyen Hair Collective`, `FakeRef Agency`, and `OldPartner Inc.`. |
| Pending status | ✅ | `Full Table (overview - admin).png` shows `Pending` badges for incomplete activation/setup states. |
| High pending payout warning | ❌ | `Full Table (overview - admin).png` shows pending payouts above `$1000`, but no yellow row/background treatment required by PRD Screen 1 notes. |
| Tooltip on Total Commissions Paid | N/A | Static layout files do not expose hover state; tooltip cannot be verified from the provided images. |
| Pagination size | ❌⚠️ | `Overview.png` shows `10 / page`; PRD Screen 1 business rule requires 25 affiliates per page. |

**Extra Elements**:

- `Export CSV` — visible in `Overview.png`; not specified by PRD Screen 1 fields or rules.
- Global shell controls — top-right search, inbox, notifications, profile, and language controls in `Overview.png`; treated as app chrome outside FR-018 screen content.

**Screen Status**: 🟡 PARTIAL  
**Field Coverage**: 13/13 listed fields covered (100%)  
**Critical Issues**: None at required-field level. Conditional behavior gaps: missing yellow high-payout warning and page-size mismatch.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Check | Severity | Finding | Evidence |
|---------|-------|----------|---------|----------|
| U-23 | Terminology consistency | ⚠️ UX Improvement | The same action is named differently across the screen: row menu uses `View` while PRD uses `View Details`, and bulk action uses singular `Generate Code` for a selected group. | `layout-temp/Overview.png` |
| U-14 | Semantic color usage | ⚠️ UX Improvement | Pending payout values above the PRD warning threshold are rendered as plain table text, so the warning condition is not visually emphasized. | `layout-temp/Full Table (overview - admin).png` |

**Flow Coverage Gaps**:

- Pagination default does not match the PRD requirement of 25 affiliates per page.
- Static files do not verify the hover tooltip for last payout date on `Total Commissions Paid`.

---

### Admin-02: Add/Edit Affiliate Form

**Status**: 🟡 PARTIAL — all specified fields are present, but edit-mode commission controls conflict with the PRD rule that commission changes use Screen 3.2.  
**Screens required**: 1  
**Layout files**: `layout-temp/Add/Add New Affiliate.png`, `layout-temp/Add/Edit Affiliate.png`, `layout-temp/Add/Fixed Amount per Booking.png`, `layout-temp/Save blocked.png`

#### Screen 2: Add/Edit Affiliate Form

**Layout**: `layout-temp/Add/Add New Affiliate.png`, `layout-temp/Add/Edit Affiliate.png`, `layout-temp/Add/Fixed Amount per Booking.png`, `layout-temp/Save blocked.png`

##### Flow Context

- **User arrives from**: `Add New Affiliate` on Screen 1, or `Edit` on an existing affiliate row/detail.
- **Screen purpose**: Create or edit affiliate identity, contact, payout bank details, fixed payout schedule, activation metadata, and internal notes.
- **Entry point**: Present — create and edit variants are provided.
- **Exit path**: Present — create state has `Create Affiliate`; edit state has `Save Changes`; blocked-save state shows validation gating.
- **Data continuity**: Correct for edit state — contact email is locked, bank account is masked, activation state is visible, and last login has a pending-account empty value.
- **Flow context issues**: Edit state still exposes commission editing, while PRD Screen 2 notes require commission changes on an existing affiliate to be made via Screen 3.2 so an effective date is captured.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Affiliate Name | Yes | ✅ | Present in `Add New Affiliate.png` and populated in `Edit Affiliate.png`; matches PRD Screen 2 field row. |
| Contact Email | Yes | ✅ | Present in create state and disabled in `Edit Affiliate.png`, matching the PRD edit restriction that email cannot be changed after creation. |
| Phone Number | No | ✅ | Present as a phone/contact input in add/edit layouts; matches PRD Screen 2 field row. |
| Language(s) | No | ✅ | Present as a multi-select chip input; matches PRD Screen 2 field row. |
| Country/Region | No | ✅ | Present as a select field; matches PRD Screen 2 field row. |
| Affiliate Type | No | ✅ | Present as a select field; matches PRD Screen 2 field row. |
| Tax / VAT / Business Reg ID | No | ⚠️ | Field is present, but the placeholder in the layout says `Phone Number`, which is stale copy against PRD Screen 2. |
| Account Holder Name | Yes | ✅ | Present in bank details section; matches PRD Screen 2 required field row. |
| Bank Name | Yes | ✅ | Present in bank details section; matches PRD Screen 2 required field row. |
| Account Number | Yes | ✅ | Present in create state and masked with last digits visible in edit state, matching the PRD bank-masking rule. |
| Routing / SWIFT Code | Yes | ✅ | Present in bank details section; matches PRD Screen 2 required field row. |
| IBAN | Conditional | ⚠️ | Field is present, but placeholder repeats `Routing / SWIFT Code`, which is incorrect for the IBAN conditional field. |
| Commission Type | Yes | ❌⚠️ | Present, but editable in `Edit Affiliate.png`; PRD Screen 2 says existing affiliate commission changes must use Screen 3.2 to capture an effective date. |
| Commission Percentage | Conditional | ❌⚠️ | Present with preview in percentage state, but remains editable in edit mode contrary to the Screen 3.2 handoff rule. |
| Commission Fixed Amount | Conditional | ❌⚠️ | Present in `Fixed Amount per Booking.png`, but fixed-amount editing in Screen 2 conflicts with the PRD Screen 3.2 handoff for existing affiliates. |
| Payout Schedule | N/A | ✅ | Visible as read-only `Monthly on the 7th`, matching PRD Screen 2 default/fixed schedule rule. |
| Performance Tier | N/A | ✅ | Visible as a read-only badge in edit state; matches PRD Screen 2. |
| Activation Status | N/A | ✅ | Visible as read-only `Invited` in edit state with `Resend Activation Email`, matching PRD Screen 2 activation-state rule. |
| Last Login | N/A | ✅ | Visible as read-only `Never logged in` in edit state, matching PRD Screen 2. |
| Notes (Internal) | No | ✅ | Present as textarea; matches PRD Screen 2 field row. |

##### Conditional States

| State | Status | Evidence |
|-------|--------|----------|
| Create state | ✅ | `Add New Affiliate.png` shows create mode with `Create Affiliate`, no account-status block, and percentage commission default. |
| Edit state | 🟡 | `Edit Affiliate.png` correctly locks contact email and shows activation state, but incorrectly leaves commission editing in Screen 2. |
| Percentage commission preview | ✅ | `Add New Affiliate.png` shows a commission preview callout, matching the PRD commission-validation rule. |
| Fixed amount commission | ⚠️ | `Fixed Amount per Booking.png` covers the fixed amount variant, but includes stale section copy above the commission controls. |
| High commission warning >20% | N/A | Static provided layouts do not show a >20% commission warning state. |
| Auto-save every 30 seconds | N/A | Static provided layouts do not verify timed auto-save behavior. |
| Save blocked / validation | ✅ | `Save blocked.png` provides a blocked-save/validation state for incomplete or invalid form data. |

**Extra Elements**:

- None identified beyond standard admin shell/navigation chrome.

**Screen Status**: 🟡 PARTIAL  
**Field Coverage**: 20/20 specified fields covered (100% visual coverage; 3 commission fields mismatched in edit context)  
**Critical Issues**: Existing-affiliate commission editing is exposed in Screen 2 instead of Screen 3.2, risking missing effective-date capture.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Check | Severity | Finding | Evidence |
|---------|-------|----------|---------|----------|
| U-11 | Label clarity | ⚠️ UX Improvement | Stale placeholders can mislead data entry: Tax / VAT / Business Reg ID uses `Phone Number`, and IBAN uses `Routing / SWIFT Code`. | `layout-temp/Add/Add New Affiliate.png`, `layout-temp/Add/Edit Affiliate.png` |
| U-11 | Label clarity | ⚠️ UX Improvement | Fixed-amount variant contains stale section copy above the commission radios, weakening form clarity. | `layout-temp/Add/Fixed Amount per Booking.png` |
| W-07 | Action placement | 💡 UX Suggestion | Page actions sit bottom-left of the narrow form column rather than a more consistent web page-action position. | `layout-temp/Add/Add New Affiliate.png`, `layout-temp/Add/Edit Affiliate.png` |

**Flow Coverage Gaps**:

- High-commission warning state (`>20%`) is not verifiable in the supplied static layouts.
- Timed auto-save behavior is not verifiable from static layouts.

---

### Admin-03: Affiliate Detail

**Status**: 🔴 FAIL — the page is recognizable as the affiliate hub, but missing the `Edit Commission Structure` entry point blocks the PRD's commission-edit flow.  
**Screens required**: 1  
**Layout files**: `layout-temp/Affiliate Detail.png`

#### Screen 3: Affiliate Detail

**Layout**: `layout-temp/Affiliate Detail.png`

##### Flow Context

- **User arrives from**: `View Details` on Screen 1 affiliate table.
- **Screen purpose**: Single-affiliate hub for account details, assigned codes, payout history/upcoming payout, audit events, and status/action management.
- **Entry point**: Present — affiliate detail layout is provided.
- **Exit path**: Partially present — edit, add discount code, generate codes, resend activation, suspend, and deactivate actions are visible; `Generate Report` and `Edit Commission Structure` are missing.
- **Data continuity**: Partially correct — selected affiliate identity and related code/payout/audit data are shown, but upcoming payout is collapsed into metrics rather than its required panel.
- **Flow context issues**: Missing `Edit Commission Structure` blocks A2 routing to Screen 3.2; row drill-in to Screen 6/8 is implied but not visually explicit.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Affiliate Header | N/A | ✅ | `Affiliate Detail.png` shows affiliate name, status badge, affiliate ID, type, country, and activation status; matches PRD Screen 3 header composite. |
| Summary Metrics | N/A | ⚠️ | Core metrics are visible, but upcoming payout content is merged into the metric strip and `Included Bookings` appears as an extra top-level metric. |
| Account Details Panel | N/A | ❌⚠️ | Mostly present, with masked payment data, but it is not a faithful read-only mirror of Screen 2: notes are moved out, commission rate is simplified, and `Payout Method` is added. |
| Assigned Promo Codes List | N/A | ⚠️ | Code rows and core metrics are visible, but row-to-Screen-6 navigation and status/created-date ordering are not explicit. Extra `Expiry` column appears. |
| Payout History List | N/A | ⚠️ | Payout rows and core values are visible, but row-to-Screen-8 navigation is not visually obvious. Extra `Completed Bookings` column appears. |
| Upcoming Payout Panel | N/A | ❌ | PRD requires a dedicated panel with next amount, scheduled date, completed bookings count, and tooltip-backed booking breakdown; layout collapses this into summary metrics and does not show tooltip affordance. |
| Activity / Audit Panel | N/A | ✅ | Chronological audit events are visible; matches PRD Screen 3 field row. |
| Internal Notes | No | ✅ | Notes textarea with character counter is visible; matches PRD Screen 3 field row. |
| Actions | N/A | ❌⚠️ | `Edit`, `Add Discount Code`, `Generate Codes`, `Resend Activation Email`, `Suspend`, and `Deactivate` are visible; `Generate Report` and `Edit Commission Structure` are missing, and `Add Discount Code` should match PRD label `Add New Discount Code`. |

##### Conditional States

| State | Status | Evidence |
|-------|--------|----------|
| Activation Status = Invited | ⚠️ | `Affiliate Detail.png` shows `Invited` and `Resend Activation Email`, but not the explicit `Invited — activation pending` treatment required by PRD Screen 3 notes. |
| Activation Status = Active | N/A | Static layout does not show active-state disabling of `Resend Activation Email`. |
| Status = Suspended | N/A | Static layout does not show `Suspend` swapping to `Reinstate`. |
| Status = Inactive | N/A | Static layout does not show terminal inactive/offboarded state. |
| Commission edit routing | ❌ | `Affiliate Detail.png` does not show `Edit Commission Structure`; PRD Screen 3 requires this action to open Screen 3.2. |
| Upcoming payout tooltip | ❌ | Static layout does not show the required tooltip listing completed bookings contributing to upcoming payout. |

**Extra Elements**:

- `Included Bookings` summary metric — belongs in the upcoming payout panel rather than top-level summary per PRD Screen 3.
- `Payout Method` in Account Details — not listed in PRD Screen 3 field set.
- `Expiry` column in Assigned Promo Codes — not listed in PRD Screen 3 list description.
- `Completed Bookings` column in Payout History — not listed in PRD Screen 3 payout history description.

**Screen Status**: 🔴 FAIL  
**Field Coverage**: 6/9 field groups pass or minor; 3/9 groups have missing or mismatched required behavior  
**Critical Issues**: Missing `Edit Commission Structure` action blocks A2 commission-edit flow; missing `Generate Report` action leaves a PRD action unavailable.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Check | Severity | Finding | Evidence |
|---------|-------|----------|---------|----------|
| U-17 | CTA label clarity | 🔴 Critical UX | Required commission-edit action is absent, so admins cannot determine how to perform the A2 commission-change task from this hub. | `layout-temp/Affiliate Detail.png` |
| U-16 | Interactive vs static distinction | ⚠️ UX Improvement | Promo code and payout rows imply drill-in navigation, but there is no strong visible affordance that rows open Screen 6 or Screen 8. | `layout-temp/Affiliate Detail.png` |
| U-02 | Information priority | ⚠️ UX Improvement | Upcoming payout is required as a dedicated panel with booking-count context, but the layout buries it in the metric strip. | `layout-temp/Affiliate Detail.png` |
| U-23 | Terminology consistency | 💡 UX Suggestion | Action label uses `Add Discount Code` while the PRD action is `Add New Discount Code`. | `layout-temp/Affiliate Detail.png` |

**Flow Coverage Gaps**:

- No visible `Edit Commission Structure` route to Screen 3.2.
- No visible `Generate Report` action.
- Static layout does not demonstrate active/suspended/inactive state-gating for activation resend and suspend/reinstate.

---

### Admin-03.1: Suspend / Reinstate Affiliate Modal

**Status**: 🔴 FAIL — modal shell exists, but action control type and destructive submit gating do not satisfy the PRD.  
**Screens required**: 1  
**Layout files**: `layout-temp/Suspend/Reinstate Affiliate (Modal).png`

#### Screen 3.1: Suspend / Reinstate Affiliate (Modal)

**Layout**: `layout-temp/Suspend/Reinstate Affiliate (Modal).png`

##### Flow Context

- **User arrives from**: `Suspend` on Screen 1 or Screen 3, or `Reinstate` for a suspended affiliate.
- **Screen purpose**: Confirm a reversible suspension/reinstatement status change while preventing accidental destructive action.
- **Entry point**: Present — suspend modal is shown.
- **Exit path**: Present but mismatched — `Suspend Affiliate` CTA is visible, but it appears enabled and positive-styled before required validation is satisfied.
- **Data continuity**: Affiliate identity context is visible in an extra summary block.
- **Flow context issues**: No reinstate variant is provided; no invalid-reason or disabled-submit state is shown.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Action | N/A | ❌⚠️ | PRD Screen 3.1 requires read-only display of `Suspend` or `Reinstate`; `Reinstate Affiliate (Modal).png` shows a dropdown-style `Suspend` control with a chevron. |
| Reason | Yes | ⚠️ | Textarea is visible, but no min 20 / max 500 helper, counter, or invalid-state treatment is shown. |
| Confirm Checkbox | Yes | ⚠️ | Checkbox is visible, but copy is a longer explanatory sentence instead of the specified `I confirm this action`. |
| Submit gate | Required behavior | ❌ | PRD requires Submit disabled until reason is valid and checkbox checked; layout shows a green `Suspend Affiliate` button that appears enabled. |

##### Conditional States

| State | Status | Evidence |
|-------|--------|----------|
| Suspend open state | ⚠️ | `Reinstate Affiliate (Modal).png` shows suspend wording and required controls, but not disabled submit. |
| Reinstate open state | ❌⚠️ | No reinstate-specific variant is provided, even though PRD Screen 3.1 covers suspend and reinstate. |
| Successful suspend outcome | ❌ | No state shows status updated, codes disabled, pending payouts held, or notification sent. |
| Successful reinstate outcome | ❌ | No state shows return to `Active` or payout resumption. |
| Invalid reason | ❌ | No validation state for <20 or >500 character reason is provided. |

**Extra Elements**:

- Affiliate summary block — useful confirmation context, but not listed in PRD Screen 3.1 field set.
- Dropdown chevron on Action — reinforces the wrong editable-control behavior.
- Cancel/close affordances — standard modal extras.

**Screen Status**: 🔴 FAIL  
**Field Coverage**: 3/4 visible field/behavior groups present, but 2 critical mismatches  
**Critical Issues**: Submit gate appears enabled before required confirmation; destructive suspend action is styled as positive/green.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Check | Severity | Finding | Evidence |
|---------|-------|----------|---------|----------|
| U-18 | Destructive action safeguard | 🔴 Critical UX | `Suspend Affiliate` is styled green/positive and appears enabled, so the destructive status action is not visually safeguarded. | `layout-temp/Suspend/Reinstate Affiliate (Modal).png` |
| U-14 | Semantic color usage | 🔴 Critical UX | Suspension uses positive green styling instead of destructive/warning styling. | `layout-temp/Suspend/Reinstate Affiliate (Modal).png` |
| U-19 | Error state clarity | ⚠️ UX Improvement | No helper/error state explains the reason length requirement or disabled-submit conditions. | `layout-temp/Suspend/Reinstate Affiliate (Modal).png` |
| W-05 | Form layout | ⚠️ UX Improvement | `Action` is rendered as a dropdown instead of a read-only display, violating the field's intended semantics. | `layout-temp/Suspend/Reinstate Affiliate (Modal).png` |

**Flow Coverage Gaps**:

- No reinstate variant.
- No invalid reason state.
- No visibly disabled submit state.

---

### Admin-03.2: Edit Commission Structure Modal

**Status**: 🔴 FAIL — supplied layout is a full affiliate edit page, not the focused commission-change modal required by the PRD.  
**Screens required**: 1  
**Layout files**: `layout-temp/Edit Commission Structure.png`

#### Screen 3.2: Edit Commission Structure (Modal)

**Layout**: `layout-temp/Edit Commission Structure.png`

##### Flow Context

- **User arrives from**: `Edit Commission Structure` action on Screen 2 or Screen 3.
- **Screen purpose**: Change an existing affiliate commission with a future effective date and explicit confirmation, without retroactive recalculation.
- **Entry point**: Mismatched — layout title is `Edit Affiliate`, not a focused commission modal.
- **Exit path**: Mismatched — page-level `Save Changes` appears at the bottom of a long edit page instead of a confirm-gated modal submit.
- **Data continuity**: Partial — commission percentage, effective date, and confirmation text are visible.
- **Flow context issues**: The modal surface is missing; unrelated affiliate edit sections dilute the commission-change task and the confirm gate is not visibly enforced.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Commission Type | Yes | ✅ | `Edit Commission Structure.png` shows `Percentage` and `Fixed Amount` radio choices; matches PRD Screen 3.2. |
| Commission Percentage | Conditional | ⚠️ | Percentage field is visible with `15%` and stepper controls, but the 5-25% allowed range is not surfaced in the UI. |
| Commission Fixed Amount | Conditional | ❌ | No valid fixed-commission branch is shown for Screen 3.2. `Fixed Amount.png` is a discount configuration asset, not a commission modal. |
| Effective Date | Yes | ⚠️ | Date field is visible, but today/future-only restriction is not surfaced. |
| Confirm | Yes | ❌⚠️ | Checkbox text is visible, but required submit gating is not demonstrated; `Save Changes` appears enabled. |
| Submit action | Required behavior | ❌ | PRD requires confirm-gated submit for the commission modal; layout shows page-level `Save Changes` after unrelated form sections. |

##### Conditional States

| State | Status | Evidence |
|-------|--------|----------|
| Type = Percentage | ⚠️ | `Edit Commission Structure.png` shows percentage branch, but no explicit 5-25% range guidance. |
| Type = Fixed Amount | ❌ | No Screen 3.2 fixed-commission branch is provided. |
| Effective date in past | ❌ | No blocked past-date state or `Effective date cannot be in the past` error is provided. |
| Confirm unchecked | ❌ | Submit does not visibly appear disabled before confirmation. |
| Saved notification/audit outcome | N/A | Notification and audit behavior cannot be verified from static layout. |

**Extra Elements**:

- `Basic Information`, `Bank / Payout Details`, `Account Status`, and `Internal Notes` sections — unrelated to the Screen 3.2 modal and make the surface too broad.
- `Payout Schedule` row inside the commission card — not part of the Screen 3.2 data fields.

**Screen Status**: 🔴 FAIL  
**Field Coverage**: 3/5 required/conditional fields visible, but modal container and confirm-gated submit behavior fail  
**Critical Issues**: Missing focused modal; no valid fixed-commission branch; confirm gate not demonstrated.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Check | Severity | Finding | Evidence |
|---------|-------|----------|---------|----------|
| U-02 | Information priority | ⚠️ UX Improvement | Commission-change task is not the dominant task; layout is framed as full affiliate editing. | `layout-temp/Edit Commission Structure.png` |
| U-03 | Visual grouping | ⚠️ UX Improvement | Commission controls are embedded among unrelated sections instead of isolated in the required modal group. | `layout-temp/Edit Commission Structure.png` |
| W-07 | Action placement | ⚠️ UX Improvement | Primary action is far below the commission fields in a long page, not in a modal footer adjacent to the task. | `layout-temp/Edit Commission Structure.png` |
| U-19 | Error state clarity | ⚠️ UX Improvement | No visible validation guidance for past effective dates or disabled submit conditions. | `layout-temp/Edit Commission Structure.png` |

**Flow Coverage Gaps**:

- No focused Screen 3.2 modal layout.
- No fixed-commission branch for this modal.
- No past-date error state.
- No disabled-submit state before confirmation.

---

### Admin-03.3: Deactivate / Offboard Affiliate Modal

**Status**: 🔴 FAIL — final balance data is present, but the terminal offboarding modal leaks suspend-flow copy and the submit gate appears enabled.  
**Screens required**: 1  
**Layout files**: `layout-temp/Deactivate/Offboard Affiliate (Modal).png`

#### Screen 3.3: Deactivate / Offboard Affiliate (Modal)

**Layout**: `layout-temp/Deactivate/Offboard Affiliate (Modal).png`

##### Flow Context

- **User arrives from**: `Deactivate / Offboard` on Screen 3.
- **Screen purpose**: Permanently move affiliate to inactive state with explicit final settlement and no silent reactivation.
- **Entry point**: Present — offboarding modal title and final settlement content are visible.
- **Exit path**: Mismatched — `Deactivate & Offboard` appears enabled and green while reason is blank and confirmation unchecked.
- **Data continuity**: Mostly correct — affiliate settlement numbers are shown for the visible net >= $50 case.
- **Flow context issues**: Stale `Suspend` and `suspension` copy appears in the terminal offboarding modal.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Reason | Yes | ⚠️ | Textarea is visible in `Offboard Affiliate (Modal).png`, but placeholder still says `suspension`, which is wrong for permanent offboarding. |
| Final Balance Summary | N/A | ✅ | Gross pending, reversals/refunds, and net final balance are visible; matches PRD Screen 3.3. |
| Settlement Outcome | N/A | ✅ | Visible `Pay final balance` outcome matches the displayed net >= $50 branch in PRD Screen 3.3. |
| Confirm Checkbox | Yes | ✅ | Exact confirmation text is visible: `I confirm this affiliate will be permanently deactivated`. |
| Submit gate | Required behavior | ❌ | PRD requires Submit disabled until reason is valid and checkbox checked; layout shows green `Deactivate & Offboard` CTA that appears enabled. |

##### Conditional States

| State | Status | Evidence |
|-------|--------|----------|
| Net final balance >= $50 | ✅ | `Offboard Affiliate (Modal).png` shows `Pay final balance`, matching PRD branch. |
| Net final balance below $50 | ⚠️ | Forfeit branch is required by PRD Screen 3.3 but not represented in supplied static layouts. |
| Negative net balance | ⚠️ | Write-off branch is required by PRD Screen 3.3 but not represented in supplied static layouts. |
| Reason invalid / checkbox unchecked | ❌ | No disabled-submit or validation state is shown. |

**Extra Elements**:

- `Action` dropdown labeled `Suspend` — stale content from Screen 3.1 and not part of Screen 3.3.

**Screen Status**: 🔴 FAIL  
**Field Coverage**: 4/4 fields visible, but critical submit behavior fails  
**Critical Issues**: Submit gate appears enabled before required reason and confirmation; stale suspend copy could cause wrong-action confusion.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Check | Severity | Finding | Evidence |
|---------|-------|----------|---------|----------|
| U-18 | Destructive action safeguard | 🔴 Critical UX | Irreversible offboarding CTA appears green/positive and enabled before confirmation, weakening safeguards for a terminal action. | `layout-temp/Deactivate/Offboard Affiliate (Modal).png` |
| U-23 | Terminology consistency | ⚠️ UX Improvement | Modal mixes offboarding with suspend language (`Suspend`, `suspension`), making the terminal flow feel like a recycled suspension variant. | `layout-temp/Deactivate/Offboard Affiliate (Modal).png` |
| U-19 | Error state clarity | ⚠️ UX Improvement | No visible validation message or disabled-state explanation for blank reason/unchecked confirmation. | `layout-temp/Deactivate/Offboard Affiliate (Modal).png` |

**Flow Coverage Gaps**:

- No below-threshold forfeiture variant.
- No negative-balance write-off variant.
- No disabled-submit state.

---

### Admin-04: Affiliate Code Generation

**Status**: 🔴 FAIL — generation modes are mostly represented, but the required `Application Method` field is missing.  
**Screens required**: 1  
**Layout files**: `layout-temp/Generate Affiliate Code - Single Affiliate.png`, `layout-temp/Generate Affiliate Code - Single Affiliate-1.png`, `layout-temp/Generate Affiliate Code - Single Affiliate-2.png`, `layout-temp/Fixed Amount.png`

#### Screen 4: Affiliate Code Generation

**Layout**: `layout-temp/Generate Affiliate Code - Single Affiliate.png`, `layout-temp/Generate Affiliate Code - Single Affiliate-1.png`, `layout-temp/Generate Affiliate Code - Single Affiliate-2.png`, `layout-temp/Fixed Amount.png`

##### Flow Context

- **User arrives from**: Screen 1 selected affiliates bulk action, Screen 3 add/generate code actions, or single-affiliate code creation.
- **Screen purpose**: Create one affiliate-bound code for a single affiliate, selected set, or filtered segment, then route to Screen 4.1 for bulk outcomes or Screen 6 for single-code confirmation/detail.
- **Entry point**: Present — generation form layouts are supplied.
- **Exit path**: Partially present — submit actions are visible, but missing `Application Method` means a required decision point is unavailable.
- **Data continuity**: Partial — single affiliate, selected affiliates, and filtered segment contexts are represented, but filtered segment does not clearly preserve a saved-filter snapshot.
- **Flow context issues**: Required application method and Rule 15 margin guard behavior are not visible.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Linked Affiliate | Conditional | ✅ | Present in single mode; matches PRD Screen 4 conditional requirement. |
| Generation Mode | Yes | ✅ | Single, Selected Affiliates, and Filtered Segment radio choices are visible. |
| Affiliate Selection | Conditional | ✅ | Selected Affiliates mode shows multi-select chips; matches PRD Screen 4. |
| Filter Criteria | Conditional | ❌⚠️ | Filtered Segment mode shows generic filters, but does not clearly represent a saved filter used to snapshot the segment. |
| Campaign Name | Yes | ✅ | Present and editable; matches PRD Screen 4. |
| Code Pattern | Conditional | ✅ | Present in bulk modes and hidden from single mode; matches PRD Screen 4. |
| Discount Code | Conditional | ✅ | Present in single mode; matches PRD Screen 4. |
| Discount Type | Yes | ✅ | Shows `Hairline Fee Only`; functionally matches `Hairline Fees Only`. |
| Discount Amount Type | Yes | ✅ | Percentage and Fixed Amount options are visible. |
| Discount Percentage | Conditional | ⚠️ | Percentage value state is visible, but the 5-30% range is not surfaced. |
| Discount Fixed Amount | Conditional | ✅ | `Fixed Amount.png` shows fixed-amount discount branch. |
| Application Method | Yes | ❌ | Required Auto-apply vs Code-based radio is absent from supplied layouts. |
| Expiration Date | No | ⚠️ | Date field is visible, but future-date rule is not surfaced. |
| Maximum Usage Count | No | ⚠️ | Field is visible, but completed-paid-only meaning is not shown. |
| Per-Patient Usage Limit | No | ✅ | Default `1` is visible; matches PRD Screen 4. |
| Status | Yes | ✅ | Active toggle is visible; label `Code Status` is a minor terminology drift. |

##### Conditional States

| State | Status | Evidence |
|-------|--------|----------|
| Single Affiliate | ✅ | Single mode shows linked affiliate and discount code while hiding bulk-only controls. |
| Selected Affiliates | ✅ | Selected mode shows multi-select chips and code-pattern preview. |
| Filtered Segment | ❌⚠️ | Filter block is visible, but saved-filter/snapshot semantics are not explicit. |
| Fixed Amount discount | ✅ | `Fixed Amount.png` confirms fixed discount branch. |
| Rule 15 percentage margin guard | ❌ | No blocked shortfall state is shown for discount + commission exceeding Hairline commission. |
| Rule 15 fixed amount warning | ❌ | No fixed-amount review warning is shown. |

**Extra Elements**:

- Code preview chips — useful but not explicitly listed in PRD Screen 4.
- Stepper controls on numeric inputs — acceptable implementation detail.
- Footer copyright and standard admin shell — outside FR-018 screen contract.

**Screen Status**: 🔴 FAIL  
**Field Coverage**: 15/16 specified fields visible; 1 required field missing  
**Critical Issues**: Missing `Application Method` blocks a required generation decision.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Check | Severity | Finding | Evidence |
|---------|-------|----------|---------|----------|
| W-05 | Form layout | 🔴 Critical UX | Required `Application Method` control is missing, so admins cannot choose auto-apply vs code-based use. | `layout-temp/Generate Affiliate Code - Single Affiliate.png`, `layout-temp/Generate Affiliate Code - Single Affiliate-1.png`, `layout-temp/Generate Affiliate Code - Single Affiliate-2.png` |
| U-23 | Terminology consistency | 💡 UX Suggestion | Toggle is labeled `Code Status` while the PRD field is `Status`. | Screen 4 supplied generation layouts |
| U-19 | Error state clarity | ⚠️ UX Improvement | Rule 15 margin guard is not surfaced near discount fields; no percentage block state or fixed-amount warning is shown. | Screen 4 supplied generation layouts and `layout-temp/Fixed Amount.png` |
| W-05 | Form layout | ⚠️ UX Improvement | Filtered Segment uses generic filter dropdowns rather than a clearly saved filter/snapshot control. | `layout-temp/Generate Affiliate Code - Single Affiliate-2.png` |

**Flow Coverage Gaps**:

- Required `Application Method` missing.
- No Rule 15 percentage-block state.
- No Rule 15 fixed-amount warning.
- Filtered segment snapshot semantics are unclear.

---

### Admin-04.1: Code Generation Results

**Status**: 🟡 PARTIAL — core batch results and actions are present, but failed-row retry mechanics are not explicit.  
**Screens required**: 1  
**Layout files**: `layout-temp/Code Generation Results.png`

#### Screen 4.1: Code Generation Results

**Layout**: `layout-temp/Code Generation Results.png`

##### Flow Context

- **User arrives from**: Screen 4 after bulk generation in Selected Affiliates or Filtered Segment mode.
- **Screen purpose**: Persisted full-screen batch result summary with created/skipped/failed breakdown, per-row reasons, retry path, CSV export, and View Codes route.
- **Entry point**: Present — `Code Generation Results.png` is a full page, not a transient modal.
- **Exit path**: Present — `Retry Failed Only`, `Download CSV`, and `View Codes` actions are visible.
- **Data continuity**: Correct for batch identity and outcome counts.
- **Flow context issues**: Failed-row selection is not visible, and same-snapshot/idempotent retry is not communicated.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Batch ID | N/A | ✅ | Present as read-only system identifier; matches PRD Screen 4.1. |
| Campaign Name | N/A | ✅ | Present as read-only campaign value; matches PRD Screen 4.1. |
| Requested Count | N/A | ✅ | Present as `Requested` KPI; matches PRD Screen 4.1. |
| Created Count | N/A | ✅ | Present as `Created` KPI; matches PRD Screen 4.1. |
| Skipped Count | N/A | ✅ | Present as `Skipped` KPI; matches PRD Screen 4.1. |
| Failed Count | N/A | ✅ | Present as `Failed` KPI; matches PRD Screen 4.1. |
| Result Rows | N/A | ⚠️ | Rows show affiliate, generated code, outcome, and reason, but failed-row selectability for retry is not visible. |
| Actions | N/A | ✅ | `Retry Failed Only`, `Download CSV`, and `View Codes` are all visible. |

##### Conditional States

| State | Status | Evidence |
|-------|--------|----------|
| Partial failure batch | ⚠️ | Counts and retry CTA are visible, but failed-row selection/auto-targeting is not explicit. |
| All-success batch | N/A | Static layout does not show Failed Count = 0 state or disabled/hidden retry behavior. |
| Persisted revisit | ✅ | Full page with Batch ID supports revisitable persisted batch requirement. |
| Retry same campaign/snapshot | ⚠️ | Required business rule is not communicated in the UI. |

**Extra Elements**:

- Generation Mode — useful metadata beyond PRD Screen 4.1 fields.
- Run Date & Time — useful audit context.
- Search field and pagination — sensible table enhancements.

**Screen Status**: 🟡 PARTIAL  
**Field Coverage**: 8/8 field groups visible; 1 behavior affordance incomplete  
**Critical Issues**: None blocking, but retry target semantics are ambiguous.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Check | Severity | Finding | Evidence |
|---------|-------|----------|---------|----------|
| W-06 | Table design | ⚠️ UX Improvement | Failed rows are not visibly selectable, and the table does not clarify whether `Retry Failed Only` automatically targets every failed row. | `layout-temp/Code Generation Results.png` |
| U-12 | Text truncation | ⚠️ UX Improvement | Long failure reason is truncated; full detail needs hover, expansion, or row detail. | `layout-temp/Code Generation Results.png` |

**Flow Coverage Gaps**:

- Failed-row retry mechanics need explicit selectability or auto-target explanation.
- Idempotent retry with same campaign/snapshot is not visible.

---

### Admin-05: Promo Code Management

**Status**: 🟢 GOOD — promo-code table and filter coverage match the PRD; remaining issues are minor action-state and status-color evidence gaps.  
**Screens required**: 1  
**Layout files**: `layout-temp/Promo Code Management.jpg`, `layout-temp/Full Table (promo - admin).jpg`, `layout-temp/Filter (promo - admin).jpg`

#### Screen 5: Promo Code Management

**Layout**: `layout-temp/Full Table (promo - admin).jpg`, `layout-temp/Filter (promo - admin).jpg`  
**Mapping note**: `layout-temp/Promo Code Management.jpg` appears to show affiliate-list content rather than promo-code rows, so it is treated as a mismapped asset and not used as primary Screen 5 evidence.

##### Flow Context

- **User arrives from**: Admin navigation to Promo Code Management, or Screen 4.1 `View Codes` filtered to a generation batch.
- **Screen purpose**: System-wide promo-code registry for browsing, filtering, acting on affiliate-bound codes, and opening shared Screen 6 detail.
- **Entry point**: Present — promo-code table and filter modal are supplied.
- **Exit path**: Partially present — row action affordance exists, but the exact `View Detail` / `Activate-Deactivate` action menu is not fully exposed in the correct promo-table capture.
- **Data continuity**: Correct — table rows show code, campaign, affiliate, usage, conversion, revenue, commission, status, and created date.
- **Flow context issues**: `Promo Code Management.jpg` is mismapped; status-color coverage for Expired and Revoked is incomplete.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Discount Code | N/A | ✅ | Visible in `Full Table (promo - admin).jpg`; matches PRD Screen 5 field row. |
| Campaign Name | N/A | ✅ | Visible in `Full Table (promo - admin).jpg`; matches PRD Screen 5 field row. |
| Linked Affiliate | N/A | ✅ | Linked affiliate names are visible in the promo table; matches PRD Screen 5 and should link to Screen 3. |
| Discount | N/A | ✅ | Percent and currency discount values are visible; matches PRD Screen 5. |
| Application Method | N/A | ✅ | `Code-based` and `Auto-apply` values are visible; matches PRD Screen 5. |
| Applied / Completed | N/A | ✅ | Inline paired counts are visible; matches PRD Screen 5 usage-stat requirement. |
| Conversion Rate | N/A | ✅ | Conversion percentages are visible; matches PRD Screen 5. |
| Revenue | N/A | ✅ | Currency revenue values are visible; matches PRD Screen 5. |
| Commission | N/A | ✅ | Currency commission values are visible; matches PRD Screen 5. |
| Status | N/A | ✅ | Status badges are visible; Active and usage-limit-like orange states are covered. Expired gray and Revoked red are not fully demonstrated. |
| Created Date | N/A | ✅ | Created date column is visible; matches PRD Screen 5. |
| Actions | N/A | ⚠️ | Row action affordance exists, but the correct promo-table capture does not fully expose exact `View Detail` and `Activate/Deactivate` menu options. |

##### Conditional States

| State | Status | Evidence |
|-------|--------|----------|
| Default list state | ✅ | `Full Table (promo - admin).jpg` shows the promo-code registry table. |
| Search active/inactive | ✅ | Search bar pattern is visible in the layout set. |
| Filter panel | ✅ | `Filter (promo - admin).jpg` includes required filter controls for status, campaign, affiliate, discount type, application method, and created date range. |
| Bulk-selected state | ✅ | Selection/bulk-action pattern is visible in the layout set. |
| Active status color | ✅ | Active green status is visible. |
| Usage-limit color | ✅ | Orange status treatment is visible. |
| Expired status color | ⚠️ | Expired state is not cleanly gray in the supplied promo table; visible chip reads closer to red/pink. |
| Revoked status color | N/A | Revoked red state is not visible in supplied Screen 5 layouts. |
| Pagination 50 per page | ⚠️ | Pagination exists, but the PRD default of 50 codes per page is not clearly verified from the supplied capture. |

**Extra Elements**:

- Sort chevrons on performance columns — useful table affordance, not explicitly required by PRD Screen 5.
- Standard admin breadcrumb and left navigation — shell UI, not a Screen 5 issue.
- `Promo Code Management.jpg` mismapped content — should be replaced or renamed because it shows affiliate-list content rather than promo-code rows.

**Screen Status**: 🟢 GOOD  
**Field Coverage**: 12/12 field groups visible; 1 action-menu detail only partially exposed  
**Critical Issues**: None.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Check | Severity | Finding | Evidence |
|---------|-------|----------|---------|----------|
| U-14 | Semantic color usage | ⚠️ UX Improvement | Expired badge does not clearly match the PRD note requiring gray; it reads closer to red/pink in the supplied promo-table capture. | `layout-temp/Full Table (promo - admin).jpg` |
| W-06 | Table design | 💡 UX Suggestion | Row action affordance exists, but the exact `View Detail` and `Activate/Deactivate` options are not exposed in the correct promo-table capture. | `layout-temp/Full Table (promo - admin).jpg` |
| U-23 | Terminology consistency | 💡 UX Suggestion | One file named `Promo Code Management.jpg` contains affiliate-list content, creating handoff ambiguity for designers/developers. | `layout-temp/Promo Code Management.jpg` |

**Flow Coverage Gaps**:

- Exact row action menu for `View Detail` and `Activate/Deactivate` should be captured.
- Expired and Revoked status examples should be captured with the PRD-specified gray/red coding.
- Pagination should visibly confirm 50 codes per page if that is the intended default.

---

### Admin-06: Promo Code Detail

**Status**: 🟢 GOOD — shared promo-code detail structure is present; remaining issues are action-label polish and editable-subset discoverability.  
**Screens required**: 1  
**Layout files**: `layout-temp/Promo Code Detail.jpg`

#### Screen 6: Promo Code Detail (Shared)

**Layout**: `layout-temp/Promo Code Detail.jpg`

##### Flow Context

- **User arrives from**: Screen 5 promo-code table row or Screen 3 assigned promo-codes list.
- **Screen purpose**: Shared single-code workspace showing settings, linked affiliate, performance, usage trend, generation source, status controls, and audit history.
- **Entry point**: Present — detail layout is supplied and includes breadcrumb/deep-page context.
- **Exit path**: Present with minor issue — status controls are visible, but `Extend Expiration` is misspelled as `Extent Expiration`.
- **Data continuity**: Correct — one linked affiliate, code metadata, settings, performance, generation source, and audit history are shown.
- **Flow context issues**: Editable subset is not clearly discoverable from the settings panel.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Code Header | N/A | ⚠️ | Code text, campaign, status badge, and created date are visible in `Promo Code Detail.jpg`, but split between title/meta areas rather than one tight header composite. |
| Linked Affiliate | N/A | ✅ | Exactly one affiliate is visible and presented as a link target to Screen 3; matches PRD Screen 6 one-affiliate rule. |
| Code Settings Panel | N/A | ⚠️ | Discount type/value, application method, expiration, max usage, and per-patient limit are present, but editable subset affordance is not obvious. |
| Performance Panel | N/A | ✅ | Applied, completed, conversion rate, revenue, and commission earned are visible; matches PRD Screen 6. |
| Usage Over Time | N/A | ✅ | Applications/completions trend chart is visible; matches PRD Screen 6. |
| Generation Source | N/A | ✅ | Single/batch source with batch path is visible; matches PRD Screen 6. |
| Status Controls | N/A | ⚠️ | Activate/deactivate/expiration controls are visible, but `Extend Expiration` is misspelled as `Extent Expiration`. |
| Audit / History | N/A | ✅ | Append-only lifecycle event list is visible; matches PRD Screen 6. |

##### Conditional States

| State | Status | Evidence |
|-------|--------|----------|
| Opened from Screen 5 | ✅ | Layout supports shared detail screen with breadcrumb/deep-page context. |
| Opened from Screen 3 | ✅ | Layout is generic enough to be identical from affiliate assigned-codes list. |
| Active code | ✅ | Active status and context-dependent controls are visible. |
| Inactive / expired / revoked visibility | ⚠️ | PRD requires visibility for inactive/expired/revoked codes; layout demonstrates active detail only. |
| Reassignment blocked | N/A | Static layout does not show an attempted linked-affiliate edit or block message. |
| Discount value fixed after creation | N/A | Static layout does not show attempted discount edit or block message. |
| Editable expiration / usage / status subset | ⚠️ | Status controls are visible, but settings panel does not make expiration/usage-limit editability clear. |

**Extra Elements**:

- Code ID in header band — useful metadata, subordinate to the required header composite.
- Breadcrumb/back-link context — useful for shared detail orientation.
- FR-019 redemption-status context — useful to distinguish redemption lifecycle from affiliate attribution.

**Screen Status**: 🟢 GOOD  
**Field Coverage**: 8/8 field groups visible; 3 minor/editability issues  
**Critical Issues**: None.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Check | Severity | Finding | Evidence |
|---------|-------|----------|---------|----------|
| U-17 | CTA label clarity | ⚠️ UX Improvement | Top-right action reads `Extent Expiration`; should be `Extend Expiration`. | `layout-temp/Promo Code Detail.jpg` |
| U-23 | Terminology consistency | ⚠️ UX Improvement | Misspelled expiration action is inconsistent with PRD Screen 6 status-control terminology. | `layout-temp/Promo Code Detail.jpg` |
| W-05 | Form layout | ⚠️ UX Improvement | Settings block reads as static even though PRD allows editing expiration and usage limits; editable fields need clearer affordance. | `layout-temp/Promo Code Detail.jpg` |

**Flow Coverage Gaps**:

- No inactive/expired/revoked variants.
- No attempted linked-affiliate reassignment block state.
- No attempted discount-value edit block state.

---

### Admin-07: Affiliate Payout Status & History

**Status**: 🟢 GOOD — overview/current-cycle/billing-history structure matches the PRD; remaining gaps are label, notes, and metadata visibility issues.  
**Screens required**: 1  
**Layout files**: `layout-temp/Payout Status & History - Overview.jpg`, `layout-temp/Payout Status & History - Current Cycle.jpg`, `layout-temp/Payout Status & History - Billing History.jpg`, `layout-temp/Full Table (payout - admin).jpg`, `layout-temp/Filter (payout - admin).jpg`

#### Screen 7: Affiliate Payout Status & History

**Layout**: `layout-temp/Payout Status & History - Overview.jpg`, `layout-temp/Payout Status & History - Current Cycle.jpg`, `layout-temp/Payout Status & History - Billing History.jpg`, `layout-temp/Full Table (payout - admin).jpg`, `layout-temp/Filter (payout - admin).jpg`

##### Flow Context

- **User arrives from**: Admin payout status/history navigation, or from affiliate payout review workflows.
- **Screen purpose**: Read-only review surface for affiliate payout cycle status, history, reconciliation, and export/detail navigation.
- **Entry point**: Present — overview, current-cycle, and billing-history subviews are supplied.
- **Exit path**: Present — `View Detail` routes to Screen 8, CSV/export actions are visible.
- **Data continuity**: Mostly correct — month, totals, affiliate rows, Stripe transfer data, masked bank details, statuses, and failure reasons are visible.
- **Flow context issues**: Internal notes edit path is unclear; transaction ID and completed bookings are not consistently surfaced across primary table states.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Payout Month | Yes | ✅ | Month dropdown is visible across supplied Screen 7 subviews; matches PRD Screen 7. |
| Overall Totals | N/A | ✅ | Summary cards show total owed, paid, affiliate count, and failed payouts; matches PRD Screen 7. |
| Affiliate Name | N/A | ✅ | Affiliate names are visible in payout rows; matches PRD Screen 7. |
| Total Completed Bookings | N/A | ⚠️ | Present in the wide/full-table concept, but not consistently surfaced in primary Current Cycle/Billing History frames. |
| Total Commissions Owed | N/A | ✅ | Visible as `Commissions Owed`; functionally matches PRD Screen 7. |
| Payment Method | N/A | ✅ | Visible as `Stripe Transfer`, matching FR-017/A-05 execution ownership. |
| Payment Details | N/A | ✅ | Masked bank details are visible with last digits; matches PRD Screen 7 masking requirement. |
| Payout Status | N/A | ✅ | Pending, Processing, Paid, and Failed badges are visible. |
| Transaction ID | N/A | ⚠️ | Visible in wide table concept, but not consistently shown in main visible table states. |
| Notes | No | ⚠️ | Notes exist in full-table concept, but no clear editable textarea/path for internal delay notes is exposed. |
| Actions | N/A | ❌⚠️ | `View Detail` and CSV/export actions are visible, but row menu label says `Download Recipe` instead of required `Download Receipt`. |

##### Conditional States

| State | Status | Evidence |
|-------|--------|----------|
| Overview subview | ✅ | Overview layout shows month scope and overall payout totals. |
| Current Cycle subview | ✅ | Current-cycle layout shows read-only cycle list and no payout-processing controls. |
| Billing History subview | ✅ | Billing-history layout shows search/filter/export tools. |
| Pending payout | ✅ | Amber pending badge is visible. |
| Processing payout | ✅ | Processing badge is visible. |
| Paid payout | ✅ | Green paid badge is visible. |
| Failed payout | ✅ | Failed rows show red treatment and failure reason text. |
| View Detail | ✅ | Row action supports navigation to shared Screen 8. |
| Retry payout | ✅ | Correctly absent from FR-018 screen; retry is owned by FR-017 Screen 6 per PRD. |
| Internal note about delay | ⚠️ | Allowed by PRD, but no clear inline edit surface is provided. |

**Extra Elements**:

- Automated generation on the 7th — correct lifecycle rule, not directly visible in static layout.
- 7-year retention — required history behavior, not directly verifiable from static layout.
- Failure reason display — helpful and aligned with PRD note.

**Screen Status**: 🟢 GOOD  
**Field Coverage**: 11/11 field groups visible or partially visible; no ownership violation  
**Critical Issues**: None.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Check | Severity | Finding | Evidence |
|---------|-------|----------|---------|----------|
| U-23 | Terminology consistency | ⚠️ UX Improvement | Row menu label says `Download Recipe`; PRD requires `Download Receipt`. | Screen 7 supplied payout layouts |
| W-06 | Table design | ⚠️ UX Improvement | Required history/reconciliation columns are not consistently surfaced across visible states. | `layout-temp/Full Table (payout - admin).jpg`, Current Cycle/Billing History captures |
| W-05 | Form layout | 💡 UX Suggestion | Internal notes are allowed by PRD, but the editable note path is not obvious. | Screen 7 supplied payout layouts |

**Flow Coverage Gaps**:

- Correct `Download Receipt` label should be shown.
- Internal payout-delay notes need a clear edit surface.
- Transaction ID and completed-bookings fields should be consistently visible or available in row detail.

---

### Admin-08: Payout / Transaction Detail

**Status**: 🟡 PARTIAL — paid-state detail is strong, but failed-state variant does not preserve the full shared-detail content.  
**Screens required**: 1  
**Layout files**: `layout-temp/Transaction Detail.jpg`, `layout-temp/Payout/Transaction Detail - Status = Failed.jpg`

#### Screen 8: Payout / Transaction Detail (Shared)

**Layout**: `layout-temp/Transaction Detail.jpg`, `layout-temp/Payout/Transaction Detail - Status = Failed.jpg`

##### Flow Context

- **User arrives from**: Screen 7 payout row or Screen 3 affiliate payout list.
- **Screen purpose**: Shared payout/transaction workspace showing full booking breakdown, commission reconciliation, payment details, status timeline, failure reason when failed, notes, and receipt export.
- **Entry point**: Present — paid and failed status variants are supplied.
- **Exit path**: Present with copy issue — `Download Receipt` action exists but is misspelled as `Download Recipe`.
- **Data continuity**: Paid state is complete; failed state loses several lower detail sections.
- **Flow context issues**: Failed variant breaks the shared-detail consistency requirement by omitting included bookings, commission calculation, payment details, transaction ID, and notes.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Payout Header | N/A | ✅ | Affiliate name, payout month, status badge, and payout ID are visible in both paid and failed variants. |
| Affiliate Link | N/A | ✅ | Affiliate name reads as a link to Screen 3; matches PRD Screen 8. |
| Period | N/A | ✅ | Payout period is visible in both variants. |
| Included Bookings | N/A | ❌⚠️ | Present in `Transaction Detail.jpg`, but absent from failed-state variant, breaking shared-detail parity. |
| Commission Calculation | N/A | ❌⚠️ | Gross commission, reversals/refunds, and net amount are visible in paid state but not preserved in failed state. |
| Payment Method | N/A | ❌⚠️ | Visible as Stripe transfer in paid state, but omitted in failed-state capture. |
| Payment Details | N/A | ❌⚠️ | Masked bank details with last 4 digits are correct in paid state, but omitted in failed state. |
| Transaction ID | N/A | ❌⚠️ | Present in paid state, missing from failed-state capture. |
| Status Timeline | N/A | ✅ | Pending → Processing → Paid/Failed timeline with timestamps is visible in both variants. |
| Failure Reason | N/A | ✅ | Correctly visible only in failed-state variant. |
| Notes | No | ❌⚠️ | Notes textarea is present in paid state, but not preserved in failed-state capture. |
| Actions | N/A | ⚠️ | Receipt action exists in both variants, but label says `Download Recipe` instead of `Download Receipt`. |

##### Conditional States

| State | Status | Evidence |
|-------|--------|----------|
| Shared screen from Screen 7 and Screen 3 | ❌⚠️ | Breadcrumb shows Screen 7 origin only; Screen 3-origin parity is not demonstrated. |
| Back/origin context | ✅ | Breadcrumb provides Screen 7 payout-history context. |
| Paid status | ✅ | Full reconciliation view is shown in `Transaction Detail.jpg`. |
| Failed status | ❌⚠️ | Failure banner and timeline are visible, but lower reconciliation/payment sections disappear. |
| Reversals/refunds as negative line items | ✅ | Paid state shows distinct `Reversal` rows with negative treatment. |
| Retry ownership read-only | ✅ | No retry control appears, correctly preserving FR-017 retry ownership. |

**Extra Elements**:

- `Promo Code` and `Type` columns in Included Bookings — useful audit detail.
- `Account Holder` in Payment Details — useful extra payment metadata.
- `Save Note` button — sensible admin notes affordance.
- Table pagination/total count — helpful for long booking lists.

**Screen Status**: 🟡 PARTIAL  
**Field Coverage**: Paid state covers 12/12 field groups; failed state omits 6 required shared-detail groups  
**Critical Issues**: Failed-state variant does not preserve full reconciliation/payment context.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Check | Severity | Finding | Evidence |
|---------|-------|----------|---------|----------|
| U-17 | CTA label clarity | ⚠️ UX Improvement | Export action is labeled `Download Recipe` instead of `Download Receipt`, weakening the receipt export intent. | `layout-temp/Transaction Detail.jpg`, `layout-temp/Payout/Transaction Detail - Status = Failed.jpg` |
| U-03 | Visual grouping | ⚠️ UX Improvement | Failed-state variant drops key reconciliation/payment sections rather than preserving the same shared-detail information architecture. | `layout-temp/Payout/Transaction Detail - Status = Failed.jpg` |
| W-04 | Breadcrumbs / page title | 💡 UX Suggestion | Only Screen 7 origin is demonstrated; Screen 3-origin back context should be captured for the shared screen. | `layout-temp/Transaction Detail.jpg` |

**Flow Coverage Gaps**:

- Failed-state detail must preserve included bookings, commission calculation, payment method/details, transaction ID, and notes.
- Screen 3-origin shared-detail breadcrumb/back context is not demonstrated.
- Receipt action label should be corrected from `Download Recipe` to `Download Receipt`.

---

### AFF-09: Affiliate Portal Shell

**Status**: 🟢 COMPLETE — four-tab shell is present across AFF layouts, with Overview shown as the default landing tab. Refresh cadence and RBAC behavior cannot be verified from static images.  
**Screens required**: 1  
**Layout files**: `layout-temp/Payout Status & History - Overview (aff).jpg`, `layout-temp/Promo Codes.jpg`, `layout-temp/Payouts (aff).jpg`, `layout-temp/Profile (aff).jpg`

#### Screen 9: Affiliate Portal

##### Flow Context

- **User arrives from**: Affiliate login after activation or normal return login.
- **Screen purpose**: Shared authenticated shell for Overview, Promo Codes, Payouts, and Profile.
- **Entry point**: Present — `Payout Status & History - Overview (aff).jpg` shows Overview selected by default.
- **Exit path**: Present — tab navigation exposes `Overview`, `Promo Codes`, `Payouts`, and `Profile`.
- **Data continuity**: Correct in static scope — affiliate-only statistics and portal tabs are shown; no patient identity is visible.
- **Flow context issues**: Secure login/RBAC, 5-minute refresh cadence, and tab-routing behavior are not directly verifiable from static layouts.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Overview tab | N/A | ✅ | Visible and selected in `Payout Status & History - Overview (aff).jpg`, matching PRD Screen 9 tabs and default-tab rule. |
| Promo Codes tab | N/A | ✅ | Visible in the shared tab bar in `Promo Codes.jpg`, matching PRD Screen 9 tabs. |
| Payouts tab | N/A | ✅ | Visible in the shared tab bar in `Payouts (aff).jpg`, matching PRD Screen 9 tabs. |
| Profile tab | N/A | ✅ | Visible in the shared tab bar in `Profile (aff).jpg`, matching PRD Screen 9 tabs. |
| Referral Link copy affordance | N/A | ✅ | `Payout Status & History - Overview (aff).jpg` shows `Copy Referal Link`, matching PRD Screen 9 referral-link copy requirement with a spelling issue captured under Screen 9.1. |
| Patient identity privacy | N/A | ✅ | AFF overview, promo, payout, and profile layouts show aggregated/code/payout data only; no patient names are visible, matching PRD Screen 9 privacy rule. |

##### Conditional States

| State | Status | Evidence |
|-------|--------|----------|
| Overview shown by default | ✅ | `Payout Status & History - Overview (aff).jpg` shows Overview selected. |
| Manual refresh / 5-minute refresh indication | ❌ | No refresh button, timestamp, or refresh cadence note is visible in mapped Screen 9 layouts. |
| RBAC / own-data-only enforcement | N/A | Static images cannot verify auth enforcement or tenant scoping behavior. |

**Extra Elements**:

- Global header controls — search, notifications, account menu, and language picker are visible across AFF shell layouts; treated as app chrome outside FR-018 screen content.

**Screen Status**: 🟢 COMPLETE  
**Field Coverage**: 4/4 tabs covered; shell privacy and referral-copy affordance represented  
**Critical Issues**: None.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Check | Severity | Finding | Evidence |
|---------|-------|----------|---------|----------|
| W-03 | Navigation structure | Pass | Four-tab portal navigation is persistent and the active tab is clear across the AFF layouts. | `layout-temp/Payout Status & History - Overview (aff).jpg`, `layout-temp/Promo Codes.jpg`, `layout-temp/Payouts (aff).jpg`, `layout-temp/Profile (aff).jpg` |
| W-04 | Breadcrumbs / page title | Pass | Page title hierarchy and active tab state are visually clear. | `layout-temp/Promo Codes.jpg` |

**Flow Coverage Gaps**:

- Static layouts do not verify secure login/RBAC enforcement.
- Static layouts do not show refresh cadence or a manual refresh affordance.

### AFF-09.1: Overview Tab

**Status**: 🟡 PARTIAL — all listed dashboard fields are represented, but monthly breakdown toggle, next-payout countdown, and refresh affordance are not shown.  
**Screens required**: 1  
**Layout files**: `layout-temp/Payout Status & History - Overview (aff).jpg`

#### Screen 9.1: Overview Tab

##### Flow Context

- **User arrives from**: Affiliate Portal default landing tab after login.
- **Screen purpose**: Show affiliate performance summary, referral link, conversion funnel, and payout timing.
- **Entry point**: Present — Overview tab is selected.
- **Exit path**: Present — affiliate can move to Promo Codes, Payouts, or Profile tabs.
- **Data continuity**: Correct — the layout shows affiliate-owned metrics, referral link, and aggregated charts without patient identity.
- **Flow context issues**: No visible monthly breakdown toggle, payout countdown, or refresh indicator.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Total Referrals (All-Time) | N/A | ✅ | Metric card visible in `Payout Status & History - Overview (aff).jpg`, matching PRD Screen 9.1. |
| Referrals This Month | N/A | ✅ | Metric card visible in `Payout Status & History - Overview (aff).jpg`, matching PRD Screen 9.1. |
| Total Revenue Generated | N/A | ✅ | Metric card visible in `Payout Status & History - Overview (aff).jpg`, matching PRD Screen 9.1. |
| Total Commissions Earned | N/A | ✅ | Metric card visible in `Payout Status & History - Overview (aff).jpg`, matching PRD Screen 9.1. |
| Commissions Paid | N/A | ✅ | Metric card visible in `Payout Status & History - Overview (aff).jpg`, matching PRD Screen 9.1. |
| Pending Payout | N/A | ✅ | Prominent metric card visible in `Payout Status & History - Overview (aff).jpg`, matching PRD Screen 9.1. |
| Next Payout Date | N/A | ⚠️ | Date value is visible in `Payout Status & History - Overview (aff).jpg`, but no countdown to the next payout date is shown as required by PRD Screen 9.1 acceptance criteria. |
| Referral Link | N/A | ⚠️ | Referral URL and copy action are visible, but the CTA label says `Copy Referal Link` instead of `Copy Referral Link`. |
| Conversion Funnel | N/A | ✅ | `Conversion Funnel` chart shows `Code Applied`, `Checkout Started`, and `Payment Completed`, matching PRD Screen 9.1. |
| Referrals Over Time | N/A | ✅ | Line chart visible in `Payout Status & History - Overview (aff).jpg`, matching PRD Screen 9.1 notes. |
| Export Report | N/A | ✅ | `Download Report` action is visible, matching PRD Screen 9.1 export rule. |

##### Conditional States

| State | Status | Evidence |
|-------|--------|----------|
| Monthly breakdown toggle | ❌ | No `All-Time` / `Current Month` toggle is visible in `Payout Status & History - Overview (aff).jpg`. |
| Pending payout countdown | ❌ | Next payout date is visible, but no countdown text appears in `Payout Status & History - Overview (aff).jpg`. |
| Refresh behavior | ❌ | No manual refresh button or last-updated timestamp is visible in `Payout Status & History - Overview (aff).jpg`. |

**Extra Elements**: None beyond specified dashboard components and app chrome.

**Screen Status**: 🟡 PARTIAL  
**Field Coverage**: 8/8 listed data fields covered; 3 conditional/business-rule affordances missing  
**Critical Issues**: None.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Check | Severity | Finding | Evidence |
|---------|-------|----------|---------|----------|
| U-23 | Terminology consistency | ⚠️ UX Improvement | Copy action label uses `Referal` instead of `Referral`, creating inconsistent terminology against the PRD. | `layout-temp/Payout Status & History - Overview (aff).jpg` |
| U-17 | CTA label clarity | ⚠️ UX Improvement | `Download Report` is clear, but the missing monthly toggle makes it unclear whether the export covers all-time or current-month data. | `layout-temp/Payout Status & History - Overview (aff).jpg` |
| U-02 | Information priority | Pass | Pending payout is visually emphasized before charts, matching the PRD priority. | `layout-temp/Payout Status & History - Overview (aff).jpg` |

**Flow Coverage Gaps**:

- Add `All-Time` / `Current Month` breakdown toggle.
- Add next-payout countdown text beside the payout date.
- Add refresh affordance or last-updated indicator for the portal refresh rule.

### AFF-09.2: Promo Codes Tab

**Status**: 🟢 GOOD — list, filter, detail, copy/share, and marketing-material fields are covered; zero-referral initial state and disabled-copy behavior for inactive historical codes are not demonstrated.  
**Screens required**: 1  
**Layout files**: `layout-temp/Promo Codes.jpg`, `layout-temp/Full table (promo - aff).jpg`, `layout-temp/Filter (promo - aff).jpg`, `layout-temp/Promo Code Detail (aff).jpg`

#### Screen 9.2: Promo Codes Tab

##### Flow Context

- **User arrives from**: Affiliate Portal Promo Codes tab.
- **Screen purpose**: Let the affiliate view assigned codes, inspect per-code performance, copy/share active code links, and access campaign materials.
- **Entry point**: Present — promo list and full table layouts are provided.
- **Exit path**: Present — row `View` action opens the promo detail layout.
- **Data continuity**: Correct — list and detail preserve code, campaign, status, performance, revenue, and commission data.
- **Flow context issues**: No zero-referral newly-generated code state; disabled-copy behavior for expired/revoked codes is not visible.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Discount Code | N/A | ✅ | Visible in `Full table (promo - aff).jpg`, matching PRD Screen 9.2 list field. |
| Campaign Name | N/A | ✅ | Visible in `Full table (promo - aff).jpg`, matching PRD Screen 9.2 list field. |
| Status | N/A | ✅ | Active, Inactive, Expired, and Revoked statuses are visible in `Promo Codes.jpg` and `Full table (promo - aff).jpg`. |
| Active Window | N/A | ✅ | Date ranges are visible in `Full table (promo - aff).jpg`, matching PRD Screen 9.2. |
| Discount | N/A | ✅ | Discount values are visible in `Full table (promo - aff).jpg`, matching PRD Screen 9.2. |
| Application Method | N/A | ✅ | Application method is visible in `Full table (promo - aff).jpg`, matching PRD Screen 9.2. |
| Applied Count | N/A | ✅ | Count visible in `Full table (promo - aff).jpg`, matching PRD Screen 9.2. |
| Completed Count | N/A | ✅ | Count visible in `Full table (promo - aff).jpg`, matching PRD Screen 9.2. |
| Conversion Rate | N/A | ✅ | Percentage visible in `Full table (promo - aff).jpg`, matching PRD Screen 9.2. |
| Revenue Generated | N/A | ✅ | Revenue visible in `Full table (promo - aff).jpg`, matching PRD Screen 9.2. |
| Commission Earned | N/A | ✅ | Commission visible in `Full table (promo - aff).jpg`, matching PRD Screen 9.2. |
| Created Date | N/A | ✅ | Created date visible in `Full table (promo - aff).jpg`, matching PRD Screen 9.2. |
| Code Header | N/A | ✅ | `Promo Code Detail (aff).jpg` shows code, campaign, status, and active window, matching PRD Screen 9.2 detail field. |
| Discount Terms | N/A | ✅ | Detail layout shows discount terms and application/copy context, matching PRD Screen 9.2. |
| Usage Over Time | N/A | ✅ | Chart visible in `Promo Code Detail (aff).jpg`, matching PRD Screen 9.2. |
| Applied / Completed | N/A | ✅ | Counts visible in `Promo Code Detail (aff).jpg`, matching PRD Screen 9.2. |
| Revenue / Commission | N/A | ✅ | Revenue and commission metrics visible in `Promo Code Detail (aff).jpg`, matching PRD Screen 9.2. |
| Last Used Date | N/A | ✅ | Last-used data visible in `Promo Code Detail (aff).jpg`, matching PRD Screen 9.2. |
| Copy / Share Action | N/A | ⚠️ | Copy promo code and referral-link actions are visible, but the layout repeats `Referal` typo. |
| Marketing Materials | N/A | ✅ | `Promo Code Detail (aff).jpg` shows externally hosted material links with `Open` actions, matching PRD Screen 9.2. |

##### Conditional States

| State | Status | Evidence |
|-------|--------|----------|
| Status filtering | ✅ | `Filter (promo - aff).jpg` shows status filter controls. |
| Historical expired/revoked visibility | ✅ | Expired and revoked rows are visible in promo table layouts. |
| Disabled active-copy for expired/revoked codes | ⚠️ | Expired/revoked rows are visible, but disabled-copy behavior is not shown in static layouts. |
| Zero-referral newly generated code state | ❌ | No layout shows a newly generated code with zero applied/completed referrals. |

**Extra Elements**:

- Search field — visible in `Promo Codes.jpg`; useful but not specified in PRD Screen 9.2.
- Row action menu — visible in `Promo Codes.jpg`; useful route to detail but not listed as a field.

**Screen Status**: 🟢 GOOD  
**Field Coverage**: 21/21 list and detail fields covered  
**Critical Issues**: None.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Check | Severity | Finding | Evidence |
|---------|-------|----------|---------|----------|
| U-23 | Terminology consistency | ⚠️ UX Improvement | Detail copy action uses `Copy Referal Link`; spelling should be `Referral` across the AFF portal. | `layout-temp/Promo Code Detail (aff).jpg` |
| W-06 | Table design | Pass | Promo table has clear headers, stable row layout, and pagination. | `layout-temp/Full table (promo - aff).jpg` |
| U-03 | Visual grouping | Pass | Code detail groups header, usage, performance, and marketing materials clearly. | `layout-temp/Promo Code Detail (aff).jpg` |

**Flow Coverage Gaps**:

- Add a zero-referral initial-state example for a newly generated affiliate code.
- Capture disabled-copy behavior for expired/revoked codes.

### AFF-09.3: Payouts Tab

**Status**: 🟡 PARTIAL — payout list and detail fields are covered, but the required below-$50 threshold rollover note is missing.  
**Screens required**: 1  
**Layout files**: `layout-temp/Payouts (aff).jpg`, `layout-temp/Filter (payout - aff).jpg`, `layout-temp/Payout details (payout - aff).jpg`

#### Screen 9.3: Payouts Tab

##### Flow Context

- **User arrives from**: Affiliate Portal Payouts tab.
- **Screen purpose**: Show upcoming payout, payout history, and detail/receipt for paid payouts.
- **Entry point**: Present — `Payouts (aff).jpg` shows top panel and payout history.
- **Exit path**: Present — row `View` action opens `Payout details (payout - aff).jpg`.
- **Data continuity**: Correct — detail preserves payout period, amounts, masked bank account, transaction reference, and aggregated bookings without patient identity.
- **Flow context issues**: Below-threshold rollover note is missing even though a low pending amount is visible.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Next Payout Date | N/A | ✅ | Visible in `Payouts (aff).jpg`, matching PRD Screen 9.3 upcoming payout panel. |
| Pending Amount | N/A | ✅ | Visible in `Payouts (aff).jpg`, matching PRD Screen 9.3. |
| Included Bookings Count | N/A | ✅ | Visible in `Payouts (aff).jpg`, matching PRD Screen 9.3. |
| Minimum Threshold Note | N/A | ❌ | `Payouts (aff).jpg` shows a low pending amount, but no below-$50 rollover note required by PRD Screen 9.3. |
| Payout Period | N/A | ✅ | Visible in payout history table, matching PRD Screen 9.3. |
| Net Amount | N/A | ✅ | Visible in payout history and detail layouts, matching PRD Screen 9.3. |
| Status | N/A | ✅ | Status badges visible in payout history and detail, matching PRD Screen 9.3. |
| Completed Bookings | N/A | ✅ | Visible in payout history table, matching PRD Screen 9.3. |
| Payout Date | N/A | ✅ | Visible in payout history table, matching PRD Screen 9.3. |
| Transaction Reference | N/A | ✅ | Visible in payout history/detail, matching PRD Screen 9.3. |
| Payout Header | N/A | ✅ | `Payout details (payout - aff).jpg` shows payout header, matching PRD Screen 9.3. |
| Period | N/A | ✅ | Visible in `Payout details (payout - aff).jpg`, matching PRD Screen 9.3. |
| Gross Commission | N/A | ✅ | Visible in `Payout details (payout - aff).jpg`, matching PRD Screen 9.3. |
| Reversals / Refunds | N/A | ✅ | Visible in `Payout details (payout - aff).jpg`, matching PRD Screen 9.3. |
| Included Bookings | N/A | ✅ | Aggregated booking IDs, dates, totals, and commissions are visible without patient identity, matching PRD Screen 9.3 privacy rule. |
| Payment Method | N/A | ✅ | Visible in `Payout details (payout - aff).jpg`, matching PRD Screen 9.3. |
| Bank Account | N/A | ✅ | Masked bank account is visible in `Payout details (payout - aff).jpg`, matching PRD Screen 9.3. |
| Download Receipt | N/A | ✅ | Paid payout detail shows `Download Receipt`, matching PRD Screen 9.3. |

##### Conditional States

| State | Status | Evidence |
|-------|--------|----------|
| Below-$50 threshold note | ❌ | No rollover message is visible in `Payouts (aff).jpg` despite the below-threshold scenario. |
| Paid receipt download | ✅ | `Payout details (payout - aff).jpg` shows `Download Receipt` for a paid payout. |
| Privacy / no patient identity | ✅ | Detail layout uses booking IDs and aggregated totals only. |

**Extra Elements**:

- Filter button — visible in `Payouts (aff).jpg`; useful but not listed in PRD Screen 9.3.
- Row action menu — visible in `Payouts (aff).jpg`; useful route to detail but not listed as a field.

**Screen Status**: 🟡 PARTIAL  
**Field Coverage**: 17/18 listed field groups covered  
**Critical Issues**: None.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Check | Severity | Finding | Evidence |
|---------|-------|----------|---------|----------|
| U-20 | Empty/conditional state design | ⚠️ UX Improvement | Below-threshold rollover condition is not explained, so affiliates may not understand why a small pending amount will not be paid this cycle. | `layout-temp/Payouts (aff).jpg` |
| U-02 | Information priority | Pass | Upcoming payout and pending amount are placed above payout history, matching the task priority. | `layout-temp/Payouts (aff).jpg` |
| W-06 | Table design | Pass | Payout history table has clear headers, status labels, row actions, and pagination. | `layout-temp/Payouts (aff).jpg` |

**Flow Coverage Gaps**:

- Add below-$50 minimum threshold note and rollover explanation.

### AFF-09.4: Profile Tab

**Status**: 🟢 GOOD — account, payout, commission, and security fields are covered; explicit immutable-email note is missing.  
**Screens required**: 1  
**Layout files**: `layout-temp/Profile (aff).jpg`

#### Screen 9.4: Profile Tab

##### Flow Context

- **User arrives from**: Affiliate Portal Profile tab or Welcome `Complete Profile` CTA.
- **Screen purpose**: Let affiliate edit non-sensitive profile/security fields while keeping admin-controlled payout and identity fields read-only.
- **Entry point**: Present — Profile tab selected.
- **Exit path**: Present — save-style profile/security controls are visible in the layout.
- **Data continuity**: Correct — admin-controlled identity, payout, commission, and status fields are shown as read-only; phone/language/security controls are editable.
- **Flow context issues**: The immutable email explanation required by PRD Screen 9.4 is not visible.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Affiliate Name | Read-only | ✅ | Visible and read-only in `Profile (aff).jpg`, matching PRD Screen 9.4. |
| Contact Email | Read-only | ⚠️ | Visible and read-only in `Profile (aff).jpg`, but no note explains that email change requires a new account. |
| Phone Number | Editable | ✅ | Editable field visible in `Profile (aff).jpg`, matching PRD Screen 9.4. |
| Language(s) | Editable | ✅ | Editable language control visible in `Profile (aff).jpg`, matching PRD Screen 9.4. |
| Country/Region | Read-only | ✅ | Visible read-only field in `Profile (aff).jpg`, matching PRD Screen 9.4. |
| Affiliate Type | Read-only | ✅ | Visible read-only field in `Profile (aff).jpg`, matching PRD Screen 9.4. |
| Tax / VAT / Business Reg ID | Read-only | ✅ | Visible read-only field in `Profile (aff).jpg`, matching PRD Screen 9.4. |
| Member Since | Read-only | ✅ | Visible in `Profile (aff).jpg`, matching PRD Screen 9.4. |
| Activation Status | Read-only | ✅ | Visible in `Profile (aff).jpg`, matching PRD Screen 9.4. |
| Bank Account | Read-only | ✅ | Masked account visible in `Profile (aff).jpg`, matching PRD Screen 9.4. |
| Bank Name | Read-only | ✅ | Visible in `Profile (aff).jpg`, matching PRD Screen 9.4. |
| Commission Structure | Read-only | ✅ | Visible in `Profile (aff).jpg`, matching PRD Screen 9.4. |
| Payout Schedule | Read-only | ✅ | Visible in `Profile (aff).jpg`, matching PRD Screen 9.4. |
| Account Status | Read-only | ✅ | Visible in `Profile (aff).jpg`, matching PRD Screen 9.4. |
| Change Password | Editable | ✅ | Password controls visible in `Profile (aff).jpg`, matching PRD Screen 9.4. |
| MFA (optional) | Editable | ✅ | MFA toggle visible in `Profile (aff).jpg`, matching PRD Screen 9.4 future/non-MVP control. |

##### Conditional States

| State | Status | Evidence |
|-------|--------|----------|
| Only phone/language/security editable | ✅ | Editable controls are limited to phone, language, password fields, and MFA in `Profile (aff).jpg`. |
| Admin-controlled fields read-only | ✅ | Identity, payout, commission, and status fields are visually disabled/read-only in `Profile (aff).jpg`. |
| Email immutable explanation | ❌ | No note explains that email change requires a new account. |
| Bank masking | ✅ | Masked bank account is shown in `Profile (aff).jpg`. |

**Extra Elements**: None beyond required profile/security controls and app chrome.

**Screen Status**: 🟢 GOOD  
**Field Coverage**: 16/16 fields covered  
**Critical Issues**: None.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Check | Severity | Finding | Evidence |
|---------|-------|----------|---------|----------|
| U-11 | Label clarity | ⚠️ UX Improvement | Contact Email is read-only, but no explanatory note clarifies the immutable-email rule. | `layout-temp/Profile (aff).jpg` |
| U-16 | Interactive vs static distinction | Pass | Editable fields and read-only admin-controlled fields are visually distinct. | `layout-temp/Profile (aff).jpg` |
| U-22 | Component consistency | Pass | Account, payout, commission, and security field styling is consistent across sections. | `layout-temp/Profile (aff).jpg` |

**Flow Coverage Gaps**:

- Add explicit immutable-email note explaining that email changes require a new account.

### AFF-10: Affiliate Onboarding & Activation

**Status**: 🟡 PARTIAL — activation flow screens are supplied, but the activation email itself is not included and cannot be verified.  
**Screens required**: 1  
**Layout files**: `layout-temp/Set Your Password.jpg`, `layout-temp/Default Form.jpg`, `layout-temp/After Submission.jpg`, `layout-temp/Rate Limited (More Than 3 Requests per Hour).jpg`, `layout-temp/↳ Welcome/Welcome.jpg`

#### Screen 10: Affiliate Onboarding & Activation

##### Flow Context

- **User arrives from**: One-time activation email or login-page resend path.
- **Screen purpose**: Cover activation sequence from set-password through first-login welcome.
- **Entry point**: Partially present — set-password, resend, and welcome layouts are provided, but the activation email layout/content is not.
- **Exit path**: Present in static screen set — Set Password leads to login/portal by spec, Resend produces confirmation/rate-limit states, Welcome has `Complete Profile` and `Get Started`.
- **Data continuity**: Correct across supplied screens — invited email/password activation, resend email, assigned codes, commission, payout schedule, and referral link are represented.
- **Flow context issues**: Activation email content cannot be verified from provided layouts.

##### Flow Verification

| Requirement | Required | Layout | Notes |
|-------------|----------|--------|-------|
| Activation email contains one-time Set Password link and login email | Yes | ⬜ | No activation email layout file is present in `layout-temp/`, so this acceptance criterion cannot be verified. |
| Set Password screen provided | Yes | ✅ | `Set Your Password.jpg` and validation/expired variants cover Screen 10.1. |
| Resend Activation screen provided | Yes | ✅ | Default, validation, success, and rate-limit states cover Screen 10.2. |
| Welcome / Get Started screen provided | Yes | ✅ | `↳ Welcome/Welcome.jpg` covers Screen 10.3. |

**Screen Status**: 🟡 PARTIAL  
**Field Coverage**: 3/4 flow artifacts verifiable from layouts  
**Critical Issues**: No activation email layout for the email-content acceptance criterion.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Check | Severity | Finding | Evidence |
|---------|-------|----------|---------|----------|
| U-26 | Progress indication | 💡 UX Suggestion | Activation journey screens do not show a visible step/progress marker across Set Password, Welcome, and Profile completion. | `layout-temp/Set Your Password.jpg`, `layout-temp/↳ Welcome/Welcome.jpg` |

**Flow Coverage Gaps**:

- Add or provide activation email layout/content to verify one-time set-password link and login-email copy.

### AFF-10.1: Set Password

**Status**: 🟡 PARTIAL — password fields and validation states are covered, but valid-link status is implied rather than explicitly displayed on the active form.  
**Screens required**: 1  
**Layout files**: `layout-temp/Set Your Password.jpg`, `layout-temp/Validation Error.jpg`, `layout-temp/Validation Errors (Weak/Mismatched Password).jpg`, `layout-temp/Expired or Already-Used Activation Link H Hairline.jpg`

#### Screen 10.1: Set Password (Activation Landing)

##### Flow Context

- **User arrives from**: One-time activation link in the activation email.
- **Screen purpose**: Let affiliate create a strong password and activate account.
- **Entry point**: Present — `Set Your Password.jpg` shows account email and password form.
- **Exit path**: Present — `Set Password` CTA submits activation.
- **Data continuity**: Correct — invited account email is fixed and password creation is scoped to activation.
- **Flow context issues**: `Validation Error.jpg` is a resend-activation validation form, not a Set Password state.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Activation Link Status | N/A | ⚠️ | `Set Your Password.jpg` implies validity through expiry helper copy; explicit expired/used state is visible only in `Expired or Already-Used Activation Link H Hairline.jpg`. |
| Account Email | N/A | ✅ | Fixed email display is visible in `Set Your Password.jpg`, matching PRD Screen 10.1. |
| New Password | Yes | ✅ | Password field visible in `Set Your Password.jpg` and weak/mismatch variant, matching PRD Screen 10.1. |
| Confirm Password | Yes | ✅ | Confirm field visible in `Set Your Password.jpg` and weak/mismatch variant, matching PRD Screen 10.1. |
| Password Strength Meter | N/A | ✅ | Strength meter visible in `Set Your Password.jpg` and weak/mismatch variant, matching PRD Screen 10.1. |
| Set Password | N/A | ✅ | Submit button visible in `Set Your Password.jpg`, matching PRD Screen 10.1. |

##### Conditional States

| State | Status | Evidence |
|-------|--------|----------|
| Expired/already-used link | ✅ | `Expired or Already-Used Activation Link H Hairline.jpg` shows explanatory message and resend option. |
| Weak password | ✅ | `Validation Errors (Weak/Mismatched Password).jpg` shows weak-password blocking message. |
| Mismatched password | ✅ | `Validation Errors (Weak/Mismatched Password).jpg` shows mismatch blocking message. |
| Single-use token invalidation after success | N/A | Backend behavior is not visually verifiable from the provided layouts. |

**Extra Elements**:

- Global public-site header and footer security/privacy copy are visible in activation layouts; treated as app chrome outside Screen 10.1 fields.

**Screen Status**: 🟡 PARTIAL  
**Field Coverage**: 6/6 fields covered  
**Critical Issues**: None.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Check | Severity | Finding | Evidence |
|---------|-------|----------|---------|----------|
| U-11 | Label clarity | ⚠️ UX Improvement | Active form does not show a dedicated valid-link status element; validity is only implied by helper copy. | `layout-temp/Set Your Password.jpg` |
| U-04 | Section headings | ⚠️ UX Improvement | Public-site header is visually prominent on the activation task screen and adds noise relative to the password setup action. | `layout-temp/Set Your Password.jpg` |
| U-19 | Error state clarity | Pass | Weak and mismatched password errors are visible and field-specific. | `layout-temp/Validation Errors (Weak/Mismatched Password).jpg` |

**Flow Coverage Gaps**:

- Add explicit active valid-link status on the set-password form.

### AFF-10.2: Resend Activation Email

**Status**: 🟢 COMPLETE — default, validation, generic success, and rate-limit states are covered.  
**Screens required**: 1  
**Layout files**: `layout-temp/Default Form.jpg`, `layout-temp/After Submission.jpg`, `layout-temp/Rate Limited (More Than 3 Requests per Hour).jpg`

#### Screen 10.2: Resend Activation Email

##### Flow Context

- **User arrives from**: Login-page `Didn't receive activation email?` path or expired-link recovery.
- **Screen purpose**: Let invited affiliates request a new activation link without revealing account existence.
- **Entry point**: Present — `Default Form.jpg` shows email field and resend CTA.
- **Exit path**: Present — submit leads to generic confirmation or rate-limit state.
- **Data continuity**: Correct — only email is collected; no account status is revealed.
- **Flow context issues**: Unknown/already-active case is not separately shown, but generic confirmation covers the required non-disclosure pattern.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Email | Yes | ✅ | Email field visible in `Default Form.jpg`, `Validation Error.jpg`, `After Submission.jpg`, and `Rate Limited (More Than 3 Requests per Hour).jpg`, matching PRD Screen 10.2. |
| Resend Activation | N/A | ✅ | `Resend Activation Email` CTA visible in default, validation, success, and rate-limited states, matching PRD Screen 10.2. |
| Confirmation Message | N/A | ✅ | `After Submission.jpg` shows generic confirmation copy, matching PRD Screen 10.2 non-disclosure rule. |

##### Conditional States

| State | Status | Evidence |
|-------|--------|----------|
| Invalid email validation | ✅ | `Validation Error.jpg` shows inline invalid-email error. |
| Generic success message | ✅ | `After Submission.jpg` shows the generic `if an account exists` message. |
| Rate limit | ✅ | `Rate Limited (More Than 3 Requests per Hour).jpg` shows a 3/hour rate-limit message. |
| Unknown/already-active account | ✅ | Covered by generic confirmation pattern in `After Submission.jpg`; static layout does not need to reveal separate account status. |

**Extra Elements**:

- Global public-site header and footer security/privacy copy are visible in resend layouts; treated as app chrome outside Screen 10.2 fields.

**Screen Status**: 🟢 COMPLETE  
**Field Coverage**: 3/3 fields covered  
**Critical Issues**: None.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Check | Severity | Finding | Evidence |
|---------|-------|----------|---------|----------|
| U-19 | Error state clarity | Pass | Invalid-email and rate-limit states clearly explain the issue near the relevant form. | `layout-temp/Validation Error.jpg`, `layout-temp/Rate Limited (More Than 3 Requests per Hour).jpg` |
| U-17 | CTA label clarity | Pass | `Resend Activation Email` clearly describes the action. | `layout-temp/Default Form.jpg` |

**Flow Coverage Gaps**: None.

### AFF-10.3: Welcome / Get Started

**Status**: 🟢 GOOD — all specified onboarding fields are covered; referral label typo and URL truncation need cleanup.  
**Screens required**: 1  
**Layout files**: `layout-temp/↳ Welcome/Welcome.jpg`

#### Screen 10.3: Welcome / Get Started (First Login)

##### Flow Context

- **User arrives from**: First successful login after activation.
- **Screen purpose**: Introduce affiliate program basics, assigned codes, commission, payout schedule, referral link, and entry CTAs.
- **Entry point**: Present — welcome header and program overview visible.
- **Exit path**: Present — `Complete Profile` and `Get Started` CTAs are visible.
- **Data continuity**: Correct — assigned codes, commission, payout schedule, and referral link are present and affiliate-scoped.
- **Flow context issues**: Static layout cannot verify post-dismissal routing to Overview or one-time display persistence.

##### Field Verification

| Field | Required | Layout | Notes |
|-------|----------|--------|-------|
| Welcome Header | N/A | ✅ | `Welcome to Hairline!` visible in `↳ Welcome/Welcome.jpg`, matching PRD Screen 10.3. |
| Assigned Codes Summary | N/A | ✅ | Assigned code cards visible in `↳ Welcome/Welcome.jpg`, matching PRD Screen 10.3. |
| Commission Summary | N/A | ✅ | Commission card visible in `↳ Welcome/Welcome.jpg`, matching PRD Screen 10.3. |
| Payout Schedule | N/A | ✅ | Payout schedule card visible in `↳ Welcome/Welcome.jpg`, matching PRD Screen 10.3. |
| Referral Link | N/A | ⚠️ | Referral URL is visible, but label says `Referal Link` and URL truncates with ellipsis in `↳ Welcome/Welcome.jpg`. |
| Complete Profile CTA | N/A | ✅ | `Complete Profile` CTA visible in `↳ Welcome/Welcome.jpg`, matching PRD Screen 10.3. |
| Get Started CTA | N/A | ✅ | `Get Started` CTA visible in `↳ Welcome/Welcome.jpg`, matching PRD Screen 10.3. |

##### Conditional States

| State | Status | Evidence |
|-------|--------|----------|
| Shown once note | ✅ | `↳ Welcome/Welcome.jpg` includes one-time onboarding note. |
| Complete Profile routes to Screen 9.4 | N/A | Routing behavior cannot be verified from static layout. |
| Get Started routes to Overview | N/A | Routing behavior cannot be verified from static layout. |

**Extra Elements**:

- `Copy Link` button beside referral field — useful copy affordance beyond the listed referral field.
- Global header/footer — treated as app chrome outside Screen 10.3 fields.

**Screen Status**: 🟢 GOOD  
**Field Coverage**: 7/7 fields covered  
**Critical Issues**: None.

##### UX/UI Design Evaluation

**Skills invoked**: `ui-ux-pro-max`, `web-design-guidelines`

| Rule ID | Check | Severity | Finding | Evidence |
|---------|-------|----------|---------|----------|
| U-11 | Label clarity | ⚠️ UX Improvement | Referral label is misspelled as `Referal Link`. | `layout-temp/↳ Welcome/Welcome.jpg` |
| U-12 | Text truncation | ⚠️ UX Improvement | Referral URL is truncated with ellipsis without visible full-value affordance other than copy. | `layout-temp/↳ Welcome/Welcome.jpg` |
| U-01 | Primary action prominence | Pass | `Get Started` is visually stronger than `Complete Profile`, matching the primary path into Overview. | `layout-temp/↳ Welcome/Welcome.jpg` |

**Flow Coverage Gaps**:

- Correct `Referal` to `Referral`.
- Consider showing full referral URL on hover/expand or make copy state explicit.

## Action Items

| Priority | Flow | Screen | Issue | Recommendation |
|----------|------|--------|-------|----------------|
| Critical | Admin-03 | Screen 3 Affiliate Detail | Missing `Edit Commission Structure` action blocks A2 routing to Screen 3.2. | Add explicit `Edit Commission Structure` action and route it to the commission modal. |
| Critical | Admin-03.1 | Screen 3.1 Suspend / Reinstate | Submit gate appears enabled before required reason and confirmation, and destructive action is green. | Make submit disabled until valid, use destructive/warning styling, and provide reinstate/invalid-reason variants. |
| Critical | Admin-03.2 | Screen 3.2 Edit Commission Structure | Supplied design is a full edit page, not the required modal; fixed commission branch and disabled-submit/past-date states are missing. | Create a focused modal with percentage/fixed branches, effective date validation, and confirm-gated submit. |
| Critical | Admin-03.3 | Screen 3.3 Deactivate / Offboard | Terminal offboarding submit appears enabled and includes stale suspend-flow copy. | Correct offboarding copy, enforce disabled submit until valid, and add below-threshold/negative settlement variants. |
| Critical | Admin-04 | Screen 4 Affiliate Code Generation | Required `Application Method` control is missing. | Add Auto-apply vs Code-based field across applicable modes. |
| Important | Admin-03 | Screen 3 Affiliate Detail | `Generate Report` action and dedicated Upcoming Payout panel are missing; Screen 6/8 row drill-in affordance is weak. | Add missing action, restore upcoming payout panel with booking tooltip, and make row navigation explicit. |
| Important | Admin-08 | Screen 8 Payout / Transaction Detail | Failed-state variant drops included bookings, commission calculation, payment details, transaction ID, and notes. | Preserve the full shared-detail content in failed state while adding failure reason/timeline. |
| Important | Admin-01 | Screen 1 Dashboard | Pagination shows `10 / page` instead of PRD default 25 and high pending payouts are not highlighted. | Set default page size to 25 and add yellow warning treatment for pending payout over $1000. |
| Important | Admin-02 | Screen 2 Add/Edit Affiliate | Edit mode exposes commission controls even though existing commission changes must move through Screen 3.2. | Remove or lock commission editing from Screen 2 edit state and route changes to Screen 3.2. |
| Important | Admin-04 | Screen 4 Affiliate Code Generation | Rule 15 margin guard states are not shown. | Add percentage block/shortfall state and fixed-amount review warning state. |
| Important | AFF-09.1 | Screen 9.1 Overview Tab | Monthly breakdown toggle, next-payout countdown, and refresh affordance are missing from the affiliate overview layout. | Add All-Time / Current Month toggle, countdown text beside next payout date, and refresh or last-updated affordance. |
| Important | AFF-09.3 | Screen 9.3 Payouts Tab | Below-$50 minimum threshold rollover note is missing even though a low pending amount scenario is visible. | Add threshold note explaining rollover to the next payout cycle when pending amount is below $50. |
| Important | AFF-10 | Screen 10 Activation Flow | Activation email layout/content is not provided, so the one-time set-password link and login-email copy cannot be verified. | Provide activation email design or content capture for verification against Screen 10 acceptance criteria. |
| UX Improvement | Admin-04.1 | Screen 4.1 Results | Retry Failed Only mechanics are unclear and long failure reasons truncate. | Add failed-row selection or auto-target explanation plus full reason expand/tooltip. |
| UX Improvement | Admin-05 | Screen 5 Promo Code Management | `Promo Code Management.jpg` is mismapped and status/action variants are incomplete. | Replace mismapped asset, capture exact row menu, and add Expired/Revoked status examples. |
| UX Improvement | Admin-06 | Screen 6 Promo Code Detail | `Extent Expiration` typo and editable subset affordance issue. | Correct to `Extend Expiration` and expose editable expiration/usage controls clearly. |
| UX Improvement | Admin-07 | Screen 7 Payout Status & History | `Download Recipe` typo, unclear notes edit path, inconsistent transaction/completed-booking visibility. | Correct label, add notes edit affordance, and make reconciliation metadata consistently available. |
| UX Improvement | AFF-09.2 | Screen 9.2 Promo Codes Tab | Zero-referral initial state and disabled-copy behavior for expired/revoked codes are not demonstrated. | Add newly generated zero-state code example and expired/revoked disabled-copy state. |
| UX Improvement | AFF-09.4 | Screen 9.4 Profile Tab | Contact email is read-only but has no explanatory immutable-email note. | Add note that email changes require a new affiliate account. |
| UX Improvement | AFF-10.1 | Screen 10.1 Set Password | Valid-link status is only implied on the active set-password form. | Add explicit active/valid activation-link status on the form. |
| UX Improvement | AFF-10.3 | Screen 10.3 Welcome / Get Started | Referral label is misspelled as `Referal`, and the referral URL is truncated. | Correct spelling and add hover/expand/full-value affordance or stronger copy confirmation. |

### Priority Legend

- **Critical**: Blocks flow progression, breaks data integrity, or causes security/legal risk. Must fix before development.
- **Critical UX**: Severe usability issue that would prevent users from completing the flow or cause significant confusion. Must fix before development.
- **Important**: Functional discrepancy that could cause user confusion or require rework during development. Should fix before development.
- **UX Improvement**: Usability or design quality issue that deviates from platform conventions or best practices. Should fix before development.
- **Suggestion**: Cosmetic or minor improvement. Can fix anytime.
- **UX Suggestion**: Minor design enhancement that would improve polish. Can fix anytime.

---

## Notes

- Source PRD: `local-docs/project-requirements/functional-requirements/fr018-affiliate-management/prd.md`
- Requirement source lines loaded incrementally per screen. Admin screen section is lines 319-819; Affiliate Platform screen section is lines 820-1158.
- UX/UI rules applied from `local-docs/project-automation/skills-engineering/verify-design-layout/references/ux-ui-evaluation-rules.md`.
- AFF screen image analysis delegated to low-cost sub-agents per `verify-design-layout` workflow; main agent wrote the report sections and action items.
