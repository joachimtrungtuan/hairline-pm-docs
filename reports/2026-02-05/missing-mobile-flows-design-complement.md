# Missing Mobile App Flows — Figma Design Complement Report

**Report Date**: 2026-02-05
**Report Type**: Design Gap Analysis & Screen Specification
**Platform**: Patient Mobile App
**Prepared For**: UI/UX Design Team
**Purpose**: Document missing flows not yet present in Figma, providing flow diagrams and screen specifications to guide design complementation.

---

## Summary Dashboard

| # | Flow | Module | Related FRs | Status |
|---|------|--------|-------------|--------|
| P01.1 | Delete Account | P-01: Auth & Profile Management | FR-001, FR-026, FR-023 | 🔴 Not Designed |
| P01.2 | Settings Screen | P-01: Auth & Profile Management | FR-026, FR-020 | 🔴 Not Designed |
| P02.1 | Compare Offers Side-by-Side | P-02: Quote Request & Management | FR-005 | 🔴 Not Designed |
| P02.2 | Cancel Inquiry | P-02: Quote Request & Management | FR-003, FR-005 | 🔴 Not Designed |
| P02.3 | Expired Offers/Quotes | P-02: Quote Request & Management | FR-004, FR-005 | 🔴 Not Designed |
| P02.4 | Legal/Policy Screens (Quote Context) | P-02: Quote Request & Management | FR-005, FR-027 | 🔴 Not Designed |
| P03.1 | Payment Methods Management | P-03: Booking & Payment | FR-007, FR-007b | 🔴 Not Designed |
| P04.1 | Input Passport Details | P-04: Travel & Logistics | FR-008 | 🔴 Not Designed |
| P04.2 | Input Hotel & Flight Details | P-04: Travel & Logistics | FR-008 | 🔴 Not Designed |
| P05.1 | Day-to-Day Treatment Progress | P-05: Aftercare & Progress Monitoring | FR-010, FR-011 | 🔴 Not Designed |
| P05.2 | Previous Treatments List | P-05: Aftercare & Progress Monitoring | FR-010, FR-011 | 🔴 Not Designed |
| P05.3 | Submitted Reviews List | P-05: Aftercare & Progress Monitoring | FR-013 | 🔴 Not Designed |
| P06.1 | Notification Listing & Bubble | P-06: Communication | FR-020 | 🔴 Not Designed |
| P08.1 | Help & Support | P-08: Help Center & Support Access | FR-033, FR-034 | 🔴 Not Designed |

---

## How to Use This Document

Each flow section below contains:

1. **Mermaid flow diagram** — visual representation of the user journey
2. **Screen specifications** — field-level detail in the standard 5-column table format
3. **Concise business rules** — key constraints per screen

**For agents filling in content**:

- Read the referenced FR PRD files under `local-docs/project-requirements/functional-requirements/` for full business context
- Screen spec tables use the standard 5-column format: **Field Name** | **Type** | **Required** | **Description** | **Validation Rules**
- Accepted `Type` values: `text`, `number`, `badge`, `checkbox`, `select`, `list`, `table`, `group`, `chips`, `buttons`, `modal`, `toggle`, `datetime`, `image`, `icon`, `link`, `action`
- Keep business rules to 3–5 bullet points per screen
- Use Mermaid `flowchart TD` (top-down) syntax for flow diagrams
- Reference specific FR screens where applicable (e.g., "FR-005 Screen 3")
- Wrap all mermaid node labels in quotes if they contain special characters

---

## P-01: Auth & Profile Management

### Flow P01.1: Delete Account

**Related FRs**: FR-001 (Patient Authentication), FR-026 (App Settings & Security), FR-023 (Data Retention & Compliance)
**Source Reference**: `local-docs/project-requirements/functional-requirements/fr026-app-settings-security/prd.md`, `fr023-data-retention-compliance/prd.md`
**Status**: 🔴 Not Designed

#### Flow Diagram

```mermaid
%% PLACEHOLDER — Agent Instructions:
%% Create a flowchart TD showing:
%% 1. Patient navigates to Settings → Account → "Delete Account"
%% 2. System shows warning screen with consequences
%% 3. Decision: "Active bookings or pending payments?" → Yes: block deletion, show reason / No: proceed
%% 4. Patient selects deletion reason (required)
%% 5. System requires identity verification (password or biometric)
%% 6. Final confirmation modal ("This action cannot be undone")
%% 7. Patient confirms → account scheduled for deletion
%% 8. Grace period screen (e.g., "Account will be deleted in 30 days. Log in to cancel.")
%% 9. Patient is logged out; after grace period → system permanently deletes per FR-023
%% Reference FR-026 for settings structure, FR-023 for data retention/deletion rules
```

#### Screen Specifications

##### Screen P01.1-S1: Delete Account Warning

**Purpose**: Inform patient of consequences before proceeding with account deletion

<!-- PLACEHOLDER — Agent Instructions:
Read FR-026 and FR-023 PRDs for account deletion rules and data retention compliance.

Create a table with these expected fields:
- Warning icon/illustration
- "Delete Your Account" header
- Consequences list (what will be permanently deleted):
  - Treatment history
  - Messages and communications
  - Reviews submitted
  - Payment method data
  - Saved preferences
- What will NOT be deleted (legal/compliance data retained per policy)
- Active obligations check (active bookings, pending payments → shown if applicable, blocks deletion)
- Deletion reason selector (required)
- Optional feedback text field
- "Continue to Delete" destructive CTA
- "Go Back" safe CTA

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- Cannot delete if active bookings exist (must cancel/complete first)
- Cannot delete if pending payments exist (must settle first)
- Deletion reason is required before proceeding
- Must clearly communicate grace period duration
- Comply with GDPR / applicable data protection — some data retained per legal obligation (FR-023)
-->

##### Screen P01.1-S2: Identity Verification Step

**Purpose**: Verify patient identity before processing account deletion

<!-- PLACEHOLDER — Agent Instructions:
Create a table with these expected fields:
- "Verify Your Identity" header
- Verification method options (password input OR biometric prompt)
- Password field (if password method selected)
- "Verify & Delete" CTA (destructive style)
- "Cancel" action
- Failed attempt counter / error message area

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- Must authenticate successfully before deletion proceeds
- Max 3 failed attempts → temporary lockout with cooldown
- Biometric can be offered as alternative to password if device supports it
-->

##### Screen P01.1-S3: Deletion Scheduled Confirmation

**Purpose**: Confirm account is scheduled for deletion and communicate grace period

<!-- PLACEHOLDER — Agent Instructions:
Create a table with these expected fields:
- Confirmation icon/illustration
- "Account Deletion Scheduled" message
- Grace period info ("Your account will be permanently deleted on [date]")
- Recovery instructions ("Log back in within X days to recover your account")
- "Log Out Now" CTA
- Email confirmation note ("A confirmation email has been sent to [email]")

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- Grace period duration (e.g., 30 days — verify with FR-023)
- Logging in during grace period automatically cancels the scheduled deletion
- Confirmation email sent immediately upon scheduling
- Patient is logged out after viewing this screen
-->

---

### Flow P01.2: Settings Screen

**Related FRs**: FR-026 (App Settings & Security), FR-020 (Notifications & Alerts)
**Source Reference**: `local-docs/project-requirements/functional-requirements/fr026-app-settings-security/prd.md`
**Status**: 🔴 Not Designed

#### Flow Diagram

```mermaid
%% PLACEHOLDER — Agent Instructions:
%% Create a flowchart TD showing:
%% 1. Patient taps Settings (from profile or tab bar)
%% 2. Settings main screen with navigation sections:
%%    a. Notification Settings → sub-screen (P01.2-S2)
%%    b. Privacy & Security → sub-screen (P01.2-S3)
%%    c. Help & Support → navigates to P-08 flow (P08.1)
%%    d. About → sub-screen (P01.2-S4)
%% 3. Each sub-screen has its own content and back navigation to settings main
%% Keep it as a simple navigation tree — no complex decision logic
%% Reference FR-026 for settings structure, FR-020 for notification preferences
```

#### Screen Specifications

##### Screen P01.2-S1: Settings Main Screen

**Purpose**: Top-level settings navigation hub

<!-- PLACEHOLDER — Agent Instructions:
Read FR-026 PRD for settings structure.

Create a table with these expected fields:
- Screen title ("Settings")
- User profile summary at top (name, email, avatar — tappable to navigate to profile)
- Navigation sections (each as a tappable row with icon + label + chevron):
  - Notification Settings → navigates to P01.2-S2
  - Privacy & Security → navigates to P01.2-S3
  - Help & Support → navigates to Flow P08.1 (P-08: Help Center & Support Access)
  - About → navigates to P01.2-S4
- App version display at bottom

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- Navigation sections are static items — always visible
- Profile summary reflects current user data in real-time
- App version auto-populated from build configuration
-->

##### Screen P01.2-S2: Notification Settings

**Purpose**: Manage push, email, and SMS notification preferences

<!-- PLACEHOLDER — Agent Instructions:
Read FR-020 PRD for notification types and patient preference options.

Create a table with these expected fields:
- "Notification Settings" header
- Push notifications master toggle (enable/disable all optional)
- Per-category toggles:
  - Quote notifications (new quote received, quote expiring)
  - Booking notifications (confirmation, reminders)
  - Payment notifications (payment due, payment confirmed)
  - Treatment notifications (progress updates, aftercare reminders)
  - Message notifications (new messages from provider)
  - Promotional notifications (offers, news)
- Email notification preferences (same categories or simplified)
- SMS notification preferences (critical only: payment, booking)

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- Some notifications are mandatory and cannot be disabled (e.g., payment due, security alerts)
- Master toggle off disables all optional notifications only
- Changes auto-save (no explicit save button needed)
- Default for new accounts: all notifications enabled
-->

##### Screen P01.2-S3: Privacy & Security Settings

**Purpose**: Manage privacy preferences and security options

<!-- PLACEHOLDER — Agent Instructions:
Read FR-026 PRD for security settings.

Create a table with these expected fields:
- "Privacy & Security" header
- Change Password action (navigates to change password flow)
- Biometric authentication toggle (Face ID / Touch ID)
- Two-factor authentication toggle/setup
- Active sessions list (optional — show logged-in devices)
- Data sharing preferences
- Download My Data action (GDPR right to data portability)
- Delete Account link (→ navigates to Flow P01.1)
- Login activity / recent logins

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- Password change requires current password verification
- 2FA setup follows standard TOTP or SMS verification flow
- "Download My Data" may take processing time — notify patient when ready
- Delete Account links to Flow P01.1 (separate flow with its own screens)
-->

> **Help & Support** is specified under **P-08: Help Center & Support Access** → see [Flow P08.1](#flow-p081-help--support) below.
> The Settings main screen links to it as a navigation item.

##### Screen P01.2-S4: About Screen

**Purpose**: Display app information and legal links

<!-- PLACEHOLDER — Agent Instructions:
Create a table with these expected fields:
- "About" header
- App name and logo
- App version number
- Terms of Service link (→ legal content screen, reuses pattern from Flow P02.4)
- Privacy Policy link (→ legal content screen)
- Licenses / Open Source credits
- Rate the App action (→ app store listing)
- Social media links (optional)
- Company information

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- Version number auto-populated from app build
- Legal links open the same legal content viewer pattern used in Flow P02.4
- "Rate the App" opens the respective app store (iOS App Store / Google Play)
-->

---

## P-02: Quote Request & Management

### Flow P02.1: Compare Offers Side-by-Side

**Related FRs**: FR-005 (Quote Comparison & Acceptance)
**Source Reference**: `local-docs/project-requirements/functional-requirements/fr005-quote-comparison-acceptance/prd.md`
**Status**: 🔴 Not Designed

#### Flow Diagram

```mermaid
%% PLACEHOLDER — Agent Instructions:
%% Create a flowchart TD showing:
%% 1. Patient opens inquiry with multiple received quotes
%% 2. Patient selects 2+ quotes to compare via checkboxes
%% 3. Decision: "Quotes selected >= 2?" → No: disable compare button / Yes: enable
%% 4. Patient taps "Compare Selected"
%% 5. System displays side-by-side comparison view
%% 6. Patient can toggle comparison fields (price, timeline, inclusions, provider rating)
%% 7. Decision: "Accept from comparison?"
%%    → Yes: leads to FR-005 acceptance flow
%%    → No: dismiss comparison, return to quote list
%% Reference FR-005 PRD "Main Flow: Patient Accepts a Quote" and screen definitions
```

#### Screen Specifications

##### Screen P02.1-S1: Quote Selection for Comparison

**Purpose**: Allow patient to select multiple quotes from their inquiry to enter comparison mode

<!-- PLACEHOLDER — Agent Instructions:
Read FR-005 PRD, specifically the quote listing screens.
This screen appears within the inquiry detail context (see FR-003 Screen 8).
Patient sees all received quotes and can check 2–4 to compare.

Create a table with these expected fields:
- Quote cards list (each showing: provider name, total price, treatment summary, validity/expiry date, provider rating)
- Selection checkbox per quote card
- "Compare Selected (N)" button (enabled when 2+ selected, max 4)
- Selected count indicator
- Filter/sort options (by price, rating, date received)
- Navigation back to inquiry detail

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- Minimum 2, maximum 4 quotes selectable for comparison
- Only valid (non-expired, non-withdrawn) quotes can be selected for comparison
- Quotes must belong to the same inquiry
- Default sort: most recently received first
-->

##### Screen P02.1-S2: Side-by-Side Comparison View

**Purpose**: Display selected quotes in a structured comparison layout

<!-- PLACEHOLDER — Agent Instructions:
Read FR-005 PRD for quote detail fields and comparison criteria.
This is a dedicated comparison screen showing quotes as columns with comparison attribute rows.

Create a table with these expected fields:
- Column headers: one per selected quote (provider name & avatar)
- Comparison rows (one row per attribute):
  - Total price & currency
  - Treatment package breakdown
  - Estimated timeline / duration
  - Inclusions list (what's covered)
  - Exclusions list (what's not covered)
  - Provider rating & review count
  - Quote validity / expiry date
- "Accept This Quote" CTA per column
- "Back to Quotes" navigation
- Horizontal scroll / swipeable columns for mobile layout

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- Comparison rows should visually highlight best values (e.g., lowest price in green, highest rating highlighted)
- "Accept" from comparison follows the same acceptance flow as FR-005
- If a quote expires while patient is on comparison screen, show expired indicator and disable its acceptance
- Mobile layout: swipeable columns or horizontal scroll with sticky first-column labels
-->

---

### Flow P02.2: Cancel Inquiry

**Related FRs**: FR-003 (Inquiry Submission), FR-005 (Quote Comparison & Acceptance)
**Source Reference**: `local-docs/project-requirements/functional-requirements/fr003-inquiry-submission/prd.md`, `fr005-quote-comparison-acceptance/prd.md`
**Status**: 🔴 Not Designed

#### Flow Diagram

```mermaid
%% PLACEHOLDER — Agent Instructions:
%% Create a flowchart TD showing:
%% 1. Patient opens inquiry detail (any inquiry in stages: Inquiry, Quoted, Accepted — before Confirmed)
%% 2. Patient taps "Cancel Inquiry" option (in action menu or bottom action area)
%% 3. System checks current stage:
%%    Decision: "Stage is Confirmed, Booked, In Progress, or Completed?"
%%    → Yes: show error "Cannot cancel at this stage"
%%    → No (Inquiry/Quoted/Accepted): proceed
%% 4. Show confirmation modal with cancellation reason
%% 5. Patient selects reason and confirms
%% 6. System updates inquiry status to "Cancelled"
%% 7. System notifies relevant providers (if quotes were received)
%% 8. Show cancellation success screen
%% Reference FR-003 for inquiry stages, FR-005 for quote lifecycle impact
```

#### Screen Specifications

##### Screen P02.2-S1: Cancel Inquiry Confirmation Modal

**Purpose**: Confirm patient's intent to cancel and capture cancellation reason

<!-- PLACEHOLDER — Agent Instructions:
Read FR-003 PRD for inquiry lifecycle stages and FR-005 for quote impact.
This is a modal/bottom sheet overlaying the inquiry detail screen.

Create a table with these expected fields:
- Warning icon
- Warning message explaining consequences of cancellation
- Current inquiry stage display
- Cancellation reason selector (predefined options + "Other" with free text)
- Optional additional notes text field
- Impact summary (e.g., "X quotes will be cancelled", "Providers will be notified")
- "Confirm Cancellation" destructive CTA
- "Go Back" dismiss CTA

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- Cancellation allowed only in stages: Inquiry, Quoted, Accepted (before Confirmed)
- If quotes exist, all associated quotes are auto-cancelled upon inquiry cancellation
- Cancellation reason is required before confirming
- Cancellation is irreversible — UI must make this clear
- All associated providers receive notification of the cancellation
-->

##### Screen P02.2-S2: Cancellation Success Confirmation

**Purpose**: Confirm the inquiry has been successfully cancelled

<!-- PLACEHOLDER — Agent Instructions:
Create a table with these expected fields:
- Success/completion icon or illustration
- "Inquiry Cancelled" confirmation message
- Cancelled inquiry reference number
- Summary of what was cancelled (inquiry + number of quotes affected)
- "Back to My Inquiries" primary CTA
- "Start New Inquiry" secondary CTA

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- Cancelled inquiry remains visible in inquiry list with "Cancelled" badge
- Patient cannot reopen a cancelled inquiry — must create a new one
-->

---

### Flow P02.3: Expired Offers/Quotes

**Related FRs**: FR-004 (Quote Submission), FR-005 (Quote Comparison & Acceptance)
**Source Reference**: `local-docs/project-requirements/functional-requirements/fr005-quote-comparison-acceptance/prd.md`
**Status**: 🔴 Not Designed

#### Flow Diagram

```mermaid
%% PLACEHOLDER — Agent Instructions:
%% Create a flowchart TD showing:
%% 1. System detects quote past expiry date (background check or on screen load)
%% 2. Quote status updated to "Expired"
%% 3. Patient opens inquiry detail → sees expired badge on quote(s)
%% 4. Patient taps expired quote → detail view with "Expired" overlay
%% 5. Decision: "All quotes for this inquiry expired?"
%%    → Yes: show "All Quotes Expired" state with option to request re-quotes or cancel inquiry
%%    → No: show remaining valid quotes normally, expired ones grayed out
%% 6. If patient requests re-quote → system sends request to provider(s)
%% Reference FR-005 for quote expiry rules, FR-004 for provider-side quote lifecycle
```

#### Screen Specifications

##### Screen P02.3-S1: Expired Quote Indicator (State Variation within Inquiry Detail)

**Purpose**: Visual treatment for expired quotes in the quote list

<!-- PLACEHOLDER — Agent Instructions:
Read FR-005 PRD for quote states and expiry behavior.
This is NOT a standalone screen — it is a state variation of the quote card within the inquiry detail quote list.

Create a table describing the visual modifications applied to an expired quote card:
- Expired badge/label overlay on the quote card
- Grayed-out styling for the entire expired quote card
- Expiry date display ("Expired on [date]")
- "Request New Quote" action button (if provider allows re-quoting)
- Disabled "Accept" button with tooltip or explanation text
- Original quote summary remains visible but visually de-emphasized

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- Expired quotes cannot be accepted under any circumstance
- Expired quotes remain visible for reference but are visually de-emphasized
- If all quotes for an inquiry are expired, show the "All Expired" state (Screen P02.3-S2)
- Provider may or may not allow re-quoting — check FR-004 for re-quote rules
- Expiry is determined by the quote's validity_end_date field
-->

##### Screen P02.3-S2: All Quotes Expired State

**Purpose**: Action state displayed when all received quotes for an inquiry have expired

<!-- PLACEHOLDER — Agent Instructions:
Create a table with these expected fields:
- Illustration/icon for the expired state
- Message explaining that all quotes have expired
- "Request New Quotes" primary CTA (re-notify providers to submit new quotes)
- "Cancel Inquiry" secondary action
- "Contact Support" tertiary link
- Inquiry summary (service type, date originally submitted)

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- "Request New Quotes" re-opens the inquiry for provider quoting
- System auto-notifies previously quoted providers about the re-quote opportunity
- Patient may also choose to cancel the inquiry entirely from this state
-->

---

### Flow P02.4: Legal/Policy Screens (Quote Context)

**Related FRs**: FR-005 (Quote Comparison & Acceptance), FR-027 (Legal Content Management)
**Source Reference**: `local-docs/project-requirements/functional-requirements/fr027-legal-content-management/prd.md`, `fr005-quote-comparison-acceptance/prd.md`
**Status**: 🔴 Not Designed

#### Flow Diagram

```mermaid
%% PLACEHOLDER — Agent Instructions:
%% Create a flowchart TD showing:
%% 1. Patient views quote/offer detail screen
%% 2. Patient taps one of the legal links: "Cancellation Policy" | "Privacy Commitment" | "Terms of Service"
%% 3. System navigates to the corresponding legal document screen (P02.4-S1/S2/S3)
%% 4. Patient reads the document (scrollable full content)
%% 5. Patient taps "Back" to return to quote detail
%% Note: These are read-only viewing screens — no acceptance action is required here.
%% The actual acceptance/agreement happens during the quote acceptance flow (FR-005).
%% Reference FR-027 for legal content management and versioning rules.
```

#### Screen Specifications

##### Screen P02.4-S1: Cancellation Policy Screen

**Purpose**: Display the cancellation policy applicable to the quote/treatment

<!-- PLACEHOLDER — Agent Instructions:
Read FR-027 PRD for legal content structure and display requirements.
This is a full-screen document viewer accessed from the quote detail screen.

Create a table with these expected fields:
- Screen title ("Cancellation Policy")
- Back/close navigation
- Policy content body (rich text / markdown rendered, scrollable)
- Last updated date
- Applicable provider name (if provider-specific policy)
- Applicable treatment type (if treatment-specific)
- Scroll progress indicator
- Optional "Download PDF" action

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- Content is fetched from backend, managed by admin via FR-027
- May include provider-specific cancellation terms alongside platform-wide terms
- Content must be the version applicable at the time the quote was created (versioned content)
- Read-only — no acceptance checkbox on this screen
-->

##### Screen P02.4-S2: Privacy Commitment Screen

**Purpose**: Display the privacy commitment and data handling practices

<!-- PLACEHOLDER — Agent Instructions:
Similar structure to Screen P02.4-S1.

Create a table with these expected fields:
- Screen title ("Privacy Commitment")
- Back/close navigation
- Privacy content body (rich text, scrollable)
- Last updated date
- Key sections: data collected, how it's used, who it's shared with, patient rights
- Scroll progress indicator

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- Must comply with applicable data protection regulations
- Content managed centrally via FR-027
- Should highlight medical data handling practices specifically (medical tourism context)
-->

##### Screen P02.4-S3: Terms of Service Screen

**Purpose**: Display the platform terms of service

<!-- PLACEHOLDER — Agent Instructions:
Similar structure to Screen P02.4-S1.

Create a table with these expected fields:
- Screen title ("Terms of Service")
- Back/close navigation
- ToS content body (rich text, scrollable)
- Last updated date
- Table of contents / section navigation (for long documents)
- Scroll progress indicator

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- Content managed via FR-027
- Version shown should match what patient will agree to (or current version if pre-acceptance)
- Must include effective date of the terms
-->

---

## P-03: Booking & Payment

### Flow P03.1: Payment Methods Management

**Related FRs**: FR-007 (Payment Processing), FR-007b (Payment Installments)
**Source Reference**: `local-docs/project-requirements/functional-requirements/fr007-payment-processing/prd.md`, `fr007b-payment-installments/prd.md`
**Status**: 🔴 Not Designed

#### Flow Diagram

```mermaid
%% PLACEHOLDER — Agent Instructions:
%% Create a flowchart TD showing:
%% 1. Patient navigates to Settings/Profile → Payment Methods
%% 2. System displays list of saved payment methods
%% 3. Decision branches from the list:
%%    a. "Add New" → payment method input form → validate → save → return to list
%%    b. "Edit" on existing → edit form (pre-filled) → validate → save → return to list
%%    c. "Remove" on existing → confirmation modal → remove → return to list
%%    d. "Set as Default" on existing → update default indicator → visual confirmation
%% 4. Each payment method card shows: type icon, masked number, expiry, default badge
%% Reference FR-007 for payment method types and validation rules
```

#### Screen Specifications

##### Screen P03.1-S1: Payment Methods List

**Purpose**: Display all saved payment methods with management actions

<!-- PLACEHOLDER — Agent Instructions:
Read FR-007 PRD for supported payment types and storage rules.
Accessed from the patient's settings/profile area.

Create a table with these expected fields:
- Screen title ("Payment Methods")
- Payment method cards list (each showing: type icon, card brand, masked last 4 digits, expiry date, default badge)
- Per-card actions: Set as Default, Edit, Remove
- "Add Payment Method" button
- Empty state (no methods saved — prompt to add first method)

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- At least one payment method required if patient has active bookings with pending payments
- Default method is used for installment auto-charges (FR-007b)
- Cannot remove the only saved method if active payment obligations exist
- Card details are tokenized — only masked info is displayed
-->

##### Screen P03.1-S2: Add/Edit Payment Method

**Purpose**: Form to add a new or edit an existing payment method

<!-- PLACEHOLDER — Agent Instructions:
Create a table with these expected fields:
- Screen title ("Add Payment Method" or "Edit Payment Method")
- Card number input (with live formatting as user types)
- Cardholder name
- Expiry date (MM/YY)
- CVV/CVC
- Billing address fields (if required by payment gateway)
- "Set as default" toggle
- "Save" primary CTA
- "Cancel" secondary action
- Secure transaction badge / encryption indicator

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- Card number must pass Luhn algorithm validation
- Expiry date must be a future date
- CVV is 3 digits (Visa/MC) or 4 digits (Amex)
- If this is the first method added, auto-set as default
- PCI compliance: card data is sent directly to payment gateway for tokenization, never stored on app servers
-->

---

## P-04: Travel & Logistics

### Flow P04.1: Input Passport Details

**Related FRs**: FR-008 (Travel Booking Integration)
**Source Reference**: `local-docs/project-requirements/functional-requirements/fr008-travel-booking-integration/prd.md`
**Status**: 🔴 Not Designed

#### Flow Diagram

```mermaid
%% PLACEHOLDER — Agent Instructions:
%% Create a flowchart TD showing:
%% 1. Booking confirmed → travel managed by provider (provider handles flight & hotel)
%% 2. Patient receives notification/prompt to submit passport details
%% 3. Patient navigates to booking detail → Travel section → "Submit Passport Details"
%% 4. Patient fills in passport form (personal details + passport fields)
%% 5. Patient uploads passport scan/photo
%% 6. System validates input (basic field validation)
%% 7. System saves and notifies provider that passport details are submitted
%% 8. Decision: "Details locked by provider for booking?"
%%    → Yes: show read-only view with "Contact provider to modify" message
%%    → No: details remain editable
%% Reference FR-008 for travel booking integration rules
```

#### Screen Specifications

##### Screen P04.1-S1: Passport Details Form

**Purpose**: Collect patient's passport information for provider-managed travel booking

<!-- PLACEHOLDER — Agent Instructions:
Read FR-008 PRD for travel integration and required passenger details.
Accessed from the booking detail under the Travel section.

Create a table with these expected fields:
- Full name (as printed on passport)
- Passport number
- Issuing country
- Nationality
- Date of birth
- Gender
- Passport issue date
- Passport expiry date
- Passport photo/scan upload (front page image)
- Special requirements (e.g., wheelchair assistance, dietary needs)
- "Submit" primary CTA
- "Save as Draft" secondary action

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- Passport expiry must be at least 6 months from the scheduled travel date
- Name must match passport document exactly
- Photo upload: accepted formats (JPG, PNG, PDF), max file size limit
- Details remain editable until provider locks them for flight booking
- Locked state shows read-only view with "Contact provider to modify" message
- Data is encrypted at rest (medical tourism context — sensitive PII)
-->

---

### Flow P04.2: Input Hotel & Flight Details (Self-Managed)

**Related FRs**: FR-008 (Travel Booking Integration)
**Source Reference**: `local-docs/project-requirements/functional-requirements/fr008-travel-booking-integration/prd.md`
**Status**: 🔴 Not Designed

#### Flow Diagram

```mermaid
%% PLACEHOLDER — Agent Instructions:
%% Create a flowchart TD showing:
%% 1. Booking confirmed → patient handles own travel (self-managed)
%% 2. Patient receives prompt to submit travel details for provider coordination
%% 3. Patient navigates to booking detail → Travel section → "Add Travel Details"
%% 4. Two sub-sections: Flight Details + Hotel/Accommodation Details
%% 5. Patient fills in flight details (airline, flight number, dates, times)
%% 6. Patient fills in hotel details (name, address, check-in/out dates)
%% 7. System saves → details visible to provider for logistics coordination
%% 8. Patient can edit/update details until treatment start date
%% Reference FR-008 for self-managed travel fields and provider visibility
```

#### Screen Specifications

##### Screen P04.2-S1: Flight Details Input

**Purpose**: Collect patient's self-booked flight information

<!-- PLACEHOLDER — Agent Instructions:
Read FR-008 PRD for self-managed travel flow.

Create a table with these expected fields:
- Outbound flight section:
  - Airline name
  - Flight number
  - Departure airport/city
  - Arrival airport/city
  - Departure date & time
  - Arrival date & time
- Return flight section (same fields as outbound)
- Booking reference number
- "Add Connecting Flight" option (for multi-leg journeys)
- Upload booking confirmation document (optional)
- "Save" CTA

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- Arrival date must be before or on treatment start date (with reasonable buffer)
- Return date must be after estimated treatment end date
- Flight details are shared with provider for airport pickup coordination (if applicable)
- Patient can update details anytime before the treatment start date
-->

##### Screen P04.2-S2: Hotel/Accommodation Details Input

**Purpose**: Collect patient's self-booked accommodation information

<!-- PLACEHOLDER — Agent Instructions:
Create a table with these expected fields:
- Hotel/accommodation name
- Address (street, city, postal code, country)
- Check-in date
- Check-out date
- Booking reference number
- Contact phone number of hotel
- Room type (optional)
- Upload booking confirmation document (optional)
- Map preview of location (auto-generated from address, optional)
- Distance from clinic indicator (if clinic address is known)
- "Save" CTA

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- Check-in date must be on or before treatment start date
- Check-out date must be after estimated treatment end date (accounting for recovery period)
- Details are shared with provider for logistics coordination
- Patient can update details anytime before check-in date
-->

---

## P-05: Aftercare & Progress Monitoring

### Flow P05.1: Day-to-Day Treatment Progress

**Related FRs**: FR-010 (Treatment Execution), FR-011 (Aftercare Recovery Management)
**Source Reference**: `local-docs/project-requirements/functional-requirements/fr010-treatment-execution/prd.md`, `fr011-aftercare-recovery-management/prd.md`
**Status**: 🔴 Not Designed

#### Flow Diagram

```mermaid
%% PLACEHOLDER — Agent Instructions:
%% Create a flowchart TD showing:
%% 1. Treatment case reaches "In Progress" status
%% 2. Patient opens case detail → "Treatment Progress" tab/section
%% 3. System displays timeline/calendar view of treatment days
%% 4. Each day entry shows: provider notes, photos, medications, status
%% 5. Patient can:
%%    a. View a day's details (provider-submitted updates) → Day Detail View
%%    b. Add own notes/journal entry for a day
%%    c. Upload progress photos
%%    d. Log symptoms or concerns
%% 6. Overall progress indicator visible (day X of Y, percentage, milestone markers)
%% 7. "Contact Provider" quick action accessible from progress view
%% Reference FR-010 for treatment execution tracking, FR-011 for aftercare monitoring
```

#### Screen Specifications

##### Screen P05.1-S1: Treatment Progress Timeline

**Purpose**: Day-by-day overview of the treatment progress

<!-- PLACEHOLDER — Agent Instructions:
Read FR-010 and FR-011 PRDs for treatment phases and progress tracking mechanisms.
This is the main progress view within an active treatment case.

Create a table with these expected fields:
- Treatment case header (treatment name, provider name, start date)
- Overall progress bar/indicator (day X of Y)
- Current phase indicator (e.g., "Pre-op Day 2", "Recovery Day 5")
- Timeline/calendar view with day entries
- Each day card: date, status icon (completed/current/upcoming), summary text, photo thumbnail (if any)
- Filter options: All days, Provider updates only, My entries only
- "Add Today's Entry" floating action button
- Quick access actions: Contact Provider, Emergency Info

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- Provider-submitted entries are read-only for patients
- Patients can only add entries for the current day or past days (not future)
- Photos uploaded by patient are visible to the assigned provider
- Timeline auto-scrolls to the current day on load
- Progress percentage calculated from treatment plan total duration
-->

##### Screen P05.1-S2: Day Detail View

**Purpose**: Detailed view of a single day's treatment progress entries

<!-- PLACEHOLDER — Agent Instructions:
Create a table with these expected fields:
- Day header (date, day number in plan, phase name)
- Provider section:
  - Provider notes (rich text, read-only)
  - Provider-uploaded photos (gallery view)
  - Medications administered/prescribed
  - Vital signs / measurements (if recorded)
  - Next steps / instructions for the patient
- Patient section:
  - Patient journal entry (text input, editable)
  - Patient-uploaded photos
  - Symptom log (pain level 1–10 slider, symptom checklist)
  - Questions/concerns for provider (text input)
- Status badge (e.g., "On Track", "Attention Needed")
- "Edit My Entry" action
- Navigation: Previous Day / Next Day arrows

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- Patient entries can be edited within 24 hours of initial submission
- Provider entries appear in real-time as the provider submits updates
- Photos support zoom and swipeable gallery view
- Symptom data is structured for provider dashboard analytics
- Critical symptom selections (e.g., high pain, bleeding) should trigger a prompt to contact the provider
-->

---

### Flow P05.2: Previous Treatments List

**Related FRs**: FR-010 (Treatment Execution), FR-011 (Aftercare Recovery Management)
**Source Reference**: `local-docs/project-requirements/functional-requirements/fr010-treatment-execution/prd.md`
**Status**: 🔴 Not Designed

#### Flow Diagram

```mermaid
%% PLACEHOLDER — Agent Instructions:
%% Create a flowchart TD showing:
%% 1. Patient navigates to Profile/History → "My Treatments"
%% 2. System displays list of all treatment cases (all statuses)
%% 3. Each card shows: treatment name, provider, dates, status badge, outcome
%% 4. Patient can filter by: All, In Progress, Completed, Cancelled
%% 5. Patient taps a treatment → navigates to treatment case detail
%% Keep it simple — primarily a list and navigation flow
```

#### Screen Specifications

##### Screen P05.2-S1: My Treatments List

**Purpose**: List all patient's treatment cases across all stages

<!-- PLACEHOLDER — Agent Instructions:
Create a table with these expected fields:
- Screen title ("My Treatments")
- Filter tabs/chips: All, In Progress, Completed, Cancelled
- Treatment case cards, each showing:
  - Treatment name / type
  - Provider name & avatar
  - Treatment dates (start → end, or expected dates)
  - Current status badge (In Progress, Completed, Cancelled)
  - Outcome summary (for completed cases)
  - Thumbnail photo (if available)
- Sort options: Most recent, Status, Provider
- Empty state per filter tab (e.g., "No completed treatments yet")
- Search treatments input (for patients with many treatments)

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- Default sort: most recent first
- In Progress treatments pinned to top of "All" list
- Cancelled treatments display cancellation reason
- Completed treatments show option to leave a review (if not yet reviewed, links to FR-013)
- All treatment cards are tappable — navigate to the full treatment case detail
-->

---

### Flow P05.3: Submitted Reviews List

**Related FRs**: FR-013 (Reviews & Ratings)
**Source Reference**: `local-docs/project-requirements/functional-requirements/fr013-reviews-ratings/prd.md`
**Status**: 🔴 Not Designed

#### Flow Diagram

```mermaid
%% PLACEHOLDER — Agent Instructions:
%% Create a flowchart TD showing:
%% 1. Patient navigates to Profile → "My Reviews"
%% 2. System displays list of all reviews submitted by the patient
%% 3. Each review card shows: treatment name, provider, star rating, date, excerpt
%% 4. Patient taps a review → full review detail view
%% 5. Decision: "Within edit window?" → Yes: show "Edit Review" option / No: read-only
%% Keep it simple — list view + detail view
%% Reference FR-013 for review structure and edit policies
```

#### Screen Specifications

##### Screen P05.3-S1: My Reviews List

**Purpose**: List all reviews submitted by the patient

<!-- PLACEHOLDER — Agent Instructions:
Read FR-013 PRD for review structure and patient review management rules.
Accessed from patient profile area.

Create a table with these expected fields:
- Screen title ("My Reviews")
- Review cards, each showing:
  - Treatment name / type
  - Provider name & avatar
  - Star rating (1–5)
  - Review date
  - Review text excerpt (truncated to 2 lines)
  - Status badge (Published, Under Review, Draft)
- Sort options: Most recent, Rating (high to low / low to high)
- Empty state ("No reviews yet — complete a treatment to leave a review")

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- Only completed treatments can have reviews
- Reviews may have a limited edit window (e.g., 30 days after submission — check FR-013)
- Published reviews are visible to other patients and the provider
- "Under Review" status indicates the review is being moderated
-->

##### Screen P05.3-S2: Review Detail View

**Purpose**: Full view of a submitted review with edit capability

<!-- PLACEHOLDER — Agent Instructions:
Create a table with these expected fields:
- Treatment name & provider info header
- Star rating display (large)
- Full review text
- Review submission date
- Photos attached to review (gallery, if any)
- Provider response section (if the provider has responded)
- "Edit Review" button (visible only if within edit window)
- "Delete Review" option
- Back navigation

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- Edit is only available within the allowed edit window (check FR-013 for specific duration)
- Delete requires a confirmation prompt
- Provider responses are read-only for the patient
- Edited reviews may go back to "Under Review" moderation status
-->

---

## P-06: Communication

### Flow P06.1: Notification Listing & Bubble

**Related FRs**: FR-020 (Notifications & Alerts)
**Source Reference**: `local-docs/project-requirements/functional-requirements/fr020-notifications-alerts/prd.md`
**Status**: 🔴 Not Designed

#### Flow Diagram

```mermaid
%% PLACEHOLDER — Agent Instructions:
%% Create a flowchart TD showing:
%% 1. Notification bubble visible on main navigation bar (shows unread count badge)
%% 2. Patient taps notification bell/icon
%% 3. System displays notification list screen
%% 4. Notifications grouped by date (Today, Yesterday, Earlier)
%% 5. Each notification shows: category icon, title, message preview, timestamp, read/unread indicator
%% 6. Patient taps a notification → marks as read AND navigates to the relevant screen (deep link)
%% 7. "Mark All as Read" action available
%% 8. Notification types: quote received, booking update, payment due, treatment update, new message, system alert
%% Reference FR-020 for notification types, categories, and delivery rules
```

#### Screen Specifications

##### Screen P06.1-S1: Notification Bubble Component

**Purpose**: Persistent unread notification indicator in app navigation

<!-- PLACEHOLDER — Agent Instructions:
This is a UI component that appears on the main tab bar or app header — not a full screen.

Create a table with these expected fields:
- Bell/notification icon
- Unread count badge (number overlay)
- Badge visibility rules (hidden when count is 0, shows "99+" for counts exceeding 99)
- Tap action (navigate to notification list screen P06.1-S2)
- Animation/attention indicator for newly arrived notifications

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- Badge count reflects unread notifications only
- Count updates in real-time (via push notification or periodic polling)
- Badge is hidden when unread count is 0
- Tapping the bell icon navigates to the list — it does NOT mark notifications as read
-->

##### Screen P06.1-S2: Notification List Screen

**Purpose**: Full chronological list of all patient notifications

<!-- PLACEHOLDER — Agent Instructions:
Read FR-020 PRD for notification types, categories, and retention rules.

Create a table with these expected fields:
- Screen title ("Notifications")
- "Mark All as Read" action button
- Date group headers (Today, Yesterday, This Week, Earlier)
- Notification cards, each showing:
  - Category icon (quote, payment, treatment, message, system)
  - Notification title (bold if unread)
  - Message preview (1–2 lines, truncated)
  - Timestamp (relative format: "2h ago", "Yesterday at 3:00 PM")
  - Read/unread visual indicator (dot or background color difference)
  - Swipe actions: Mark as Read, Delete
- Filter tabs: All, Quotes, Payments, Treatment, Messages
- Empty state ("No notifications yet")
- Pull-to-refresh gesture
- Infinite scroll / pagination for long lists

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- Tapping a notification marks it as read AND navigates to the relevant screen via deep link
- Notifications ordered newest first within each date group
- Old notifications may expire per data retention policy (check FR-020 and FR-023)
- System notifications (e.g., maintenance, policy updates) styled differently from transactional ones
- Deleted notifications are soft-deleted and not recoverable by the patient
-->

---

## P-08: Help Center & Support Access

### Flow P08.1: Help & Support

**Related FRs**: FR-033 (Help Centre Management), FR-034 (Support Center Ticketing)
**Source Reference**: `local-docs/project-requirements/functional-requirements/fr033-help-centre-management/prd.md`, `fr034-support-center-ticketing/prd.md`
**Status**: 🔴 Not Designed

#### Flow Diagram

```mermaid
%% PLACEHOLDER — Agent Instructions:
%% Create a flowchart TD showing:
%% 1. Patient navigates to Help & Support (from Settings P01.2-S1 or other entry points)
%% 2. Help & Support hub screen with options:
%%    a. FAQ / Help Center → browse articles/categories → view article detail
%%    b. Contact Support → create new support ticket (FR-034 flow)
%%    c. My Support Tickets → list of open/closed tickets → view ticket detail
%%    d. Live Chat (if available) → opens chat interface
%%    e. Emergency Contact → displays contact info directly
%% 3. Each sub-flow has back navigation to the Help & Support hub
%% Reference FR-033 for help centre content structure, FR-034 for ticketing flow
```

#### Screen Specifications

##### Screen P08.1-S1: Help & Support Hub

**Purpose**: Central access point for all help resources and support channels

<!-- PLACEHOLDER — Agent Instructions:
Read FR-033 (Help Centre Management) and FR-034 (Support Center Ticketing) PRDs.
This screen is the entry point for all help and support features.
Accessed from Settings (P01.2-S1) and potentially from other deep links in the app.

Create a table with these expected fields:
- Screen title ("Help & Support")
- Search bar (search across FAQ articles)
- Quick help categories (tappable cards/tiles for common topics)
- Navigation sections:
  - FAQ / Help Center (→ browse help articles, FR-033)
  - Contact Support (→ create support ticket, FR-034)
  - My Support Tickets (→ list of patient's tickets, FR-034)
  - Live Chat (if available)
- Emergency contact section (always visible):
  - Emergency phone number
  - Emergency email
- Back navigation

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- Help Center content is read-only for patients (managed by admin via FR-033)
- Search covers all published help articles
- Emergency contact information is always visible and accessible
- Support ticket creation follows FR-034 flow and rules
- Live Chat availability depends on business hours configuration
-->

##### Screen P08.1-S2: Help Center / FAQ Browser

**Purpose**: Browse and search help articles organized by category

<!-- PLACEHOLDER — Agent Instructions:
Read FR-033 PRD for help centre content structure and categories.

Create a table with these expected fields:
- Screen title ("Help Center")
- Search bar (with auto-suggest)
- Category list (tappable, each showing: icon, category name, article count)
- Featured/popular articles section
- Recently viewed articles (if applicable)
- Article list within a category:
  - Article title
  - Brief excerpt
  - Last updated indicator
- Article detail view:
  - Article title
  - Content body (rich text, scrollable)
  - "Was this helpful?" feedback (Yes/No)
  - "Contact Support" CTA if article didn't help
  - Related articles list
- Back navigation (category → hub)

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- Articles are organized by categories defined in FR-033
- Search returns results ranked by relevance
- Article content is read-only, managed by admin
- "Was this helpful?" feedback is sent to the admin dashboard
- If no articles match search, show "Contact Support" prompt
-->

##### Screen P08.1-S3: My Support Tickets

**Purpose**: List all support tickets submitted by the patient

<!-- PLACEHOLDER — Agent Instructions:
Read FR-034 PRD for support ticket structure and lifecycle.

Create a table with these expected fields:
- Screen title ("My Support Tickets")
- "Create New Ticket" button
- Ticket list, each card showing:
  - Ticket reference number
  - Subject / title
  - Status badge (Open, In Progress, Waiting for Reply, Resolved, Closed)
  - Date submitted
  - Last updated timestamp
  - Assigned agent name (optional)
- Filter options: All, Open, Resolved
- Sort: Most recent first
- Empty state ("No support tickets — need help? Create a ticket")
- Tapping a ticket → ticket detail view with conversation thread

Format:
| Field Name | Type | Required | Description | Validation Rules |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
-->

**Business Rules**:
<!-- PLACEHOLDER — Agent Instructions:
Include rules for:
- Tickets ordered by most recently updated
- Open tickets pinned to top
- Patient can reply to open tickets (adds to conversation thread)
- Resolved/closed tickets are read-only
- Patient can reopen a resolved ticket within a defined window (check FR-034)
-->

---

## Placeholder for Additional Flows

<!-- INSTRUCTIONS FOR ADDING NEW FLOWS:

When new missing flows are identified, follow these steps:

1. Determine which patient module (P-01 through P-08) the flow belongs to:
   - P-01: Auth & Profile Management
   - P-02: Quote Request & Management
   - P-03: Booking & Payment
   - P-04: Travel & Logistics
   - P-05: Aftercare & Progress Monitoring
   - P-06: Communication
   - P-07: 3D Scan Capture & Viewing
   - P-08: Help Center & Support Access

2. Add the flow under the appropriate module section above.
   If the module section doesn't exist yet (P-07, P-08), create it following the same heading pattern.

3. Assign the next sequential flow number within that module:
   e.g., if P-02 has flows P02.1–P02.4, the next flow is P02.5.

4. Update the Summary Dashboard table at the top of this document.

5. Follow the exact same template per flow:
   - Flow header with: Related FRs, Source Reference, Status
   - Mermaid flow diagram (flowchart TD)
   - Screen specifications: one sub-section per screen with:
     - Purpose (one line)
     - 5-column table: Field Name | Type | Required | Description | Validation Rules
     - Concise business rules (3–5 bullets)

6. Reference existing FR PRD documents for traceability.
-->

---

## Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-02-05 | 0.1 | Initial structure with placeholders for 14 missing flows across 7 patient modules (P-01, P-02, P-03, P-04, P-05, P-06, P-08) | Product & Engineering |
