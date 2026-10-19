# Provider Dashboard — Manual Testing Plan (Reference Walkthrough)

**Date:** 2026-03-10
**Scope:** Main treatment flow — from sign-in through treatment completion
**Dashboard:** Provider Dashboard (`profile_type: "provider"`)
**Test Type:** Manual (exploratory + scripted)
**Related FRs:** FR-015, FR-003, FR-004, FR-006, FR-007/007B, FR-009, FR-010, FR-011, FR-020, FR-032, FR-026

---

## Usage Note

- This document is a manual walkthrough reference only.
- The canonical developer handoff and result-report artifact is [test-checklist-report.md](/Users/joachimtrungtuan/My%20Documents/Va%CC%82n%20Tay%20Media/Products/Hairline/local-docs/testing-plans/2026-03-10/automated/provider-dashboard/test-checklist-report.md).
- If any manual run is executed, record the final business gaps and discrepancies in the summary section of the automated checklist/report, not only inside step-level notes here.

## Scope & Deferred Items

**In scope:** Provider dashboard end-to-end flow — sign-in through treatment completion. Patient actions (inquiry submission, quote acceptance, payment) are simulated via seeded data or the mobile app used as an entry tool.

**Deferred to future testing round:**
- **Messaging & Communication (FR-012):** Only basic send/receive is verified in TC-P-005. Comprehensive messaging testing (delivery confirmation, real-time WebSocket updates, file/image sharing, message notifications, conversation threading) is deferred. This must be revisited when messaging is tested as a standalone module.
- **Provider Analytics & Reporting (FR-014):** Not covered in this flow-focused round.

## Table of Contents

1. [Test Environment Setup](#1-test-environment-setup)
2. [Test Data Seeding](#2-test-data-seeding)
3. [Test Scenarios](#3-test-scenarios)
   - [TC-P-001: Provider Owner Sign-In & Team Invitation Acceptance](#tc-p-001-provider-owner-sign-in--team-invitation-acceptance)
   - [TC-P-002: Provider Onboarding & Profile Setup](#tc-p-002-provider-onboarding--profile-setup)
   - [TC-P-003: Receiving & Reviewing Inquiries](#tc-p-003-receiving--reviewing-inquiries)
   - [TC-P-004: Creating & Submitting Quotes](#tc-p-004-creating--submitting-quotes)
   - [TC-P-004B: Quote Acceptance & Booking Transition (Provider Notification)](#tc-p-004b-quote-acceptance--booking-transition-provider-notification)
   - [TC-P-005: Appointment Confirmation & Scheduling](#tc-p-005-appointment-confirmation--scheduling)
   - [TC-P-006: Treatment Execution (Check-In to Completion)](#tc-p-006-treatment-execution-check-in-to-completion)
   - [TC-P-007: Aftercare Setup & Monitoring](#tc-p-007-aftercare-setup--monitoring)
   - [TC-P-008: Treatment Completion & Closure](#tc-p-008-treatment-completion--closure)
4. [End-to-End Flow Checklist](#4-end-to-end-flow-checklist)
5. [Manual Run Summary](#5-manual-run-summary)
6. [Defect Reporting Template](#6-defect-reporting-template)

---

## 1. Test Environment Setup

### Prerequisites

| Component | Setup Command | URL |
|-----------|--------------|-----|
| Backend (Docker) | `cd main/hairline-backend && docker-compose up -d` | http://localhost:80 |
| Frontend (Dev) | `cd main/hairline-frontend && npm run dev` | http://localhost:5173 |
| WebSocket (Reverb) | Included in Docker compose | ws://localhost:8081 |
| Database (MySQL) | Included in Docker compose | localhost:3307 |
| Mailpit (Email) | Included in Docker compose | http://localhost:8025 |

### Verification Checklist

- [ ] Docker containers running: `docker-compose ps` shows php, nginx, mysql, reverb, mailpit all "Up"
- [ ] Frontend accessible at http://localhost:5173 — shows Auth Panel with "Log in for Provider" and "Log in for Hairline Team"
- [ ] Backend API responding: `curl http://localhost:80/api/health` or similar returns 200
- [ ] Mailpit UI accessible at http://localhost:8025
- [ ] Database accessible: `docker-compose exec mysql mysql -u root -p` connects successfully

### Browser Requirements

- Chrome (latest) — primary testing browser
- One additional browser (Firefox or Safari) for cross-browser spot checks
- Browser DevTools open (Network tab) during testing for API monitoring

---

## 2. Test Data Seeding

### Step-by-Step Seeding Instructions

```bash
# 1. Enter the backend container
docker-compose exec php bash

# 2. Run fresh migrations (WARNING: destroys existing data)
php artisan migrate:fresh

# 3. Seed with BasicSeeder (fast — creates essential data + 2 fixed providers)
php artisan db:seed --class=BasicSeeder

# 4. Seed additional data for full flow testing
php artisan db:seed --class=FullSeeder
```

### Seeder Modes Reference

| Mode | Command | What it creates | Speed |
|------|---------|-----------------|-------|
| **Basic** | `--class=BasicSeeder` | Essential data + 2 fixed providers | Fast |
| **Development** | `--class=DevelopmentSeeder` | Basic + random providers/patients | Moderate |
| **Full** | `--class=FullSeeder` | Development + inquiries/quotes/treatments | Slow |

### Pre-Seeded Test Accounts

| Account | Email | Password | Role | Provider |
|---------|-------|----------|------|----------|
| Provider 1 (Owner) | `provider1@hairline.app` | `password123` | Provider Owner | Hair Clinic Istanbul |
| Clinician 1 | `clinician1@hairline.app` | `password123` | Clinician (Dr. Ahmed Hassan) | Hair Clinic Istanbul |
| Provider 2 (Owner) | `provider2@hairline.app` | `password123` | Provider Owner | Elite Hair Center |
| Admin Staff | `admin2@hairline.app` | `password123` | Admin Staff (Sarah Johnson) | Elite Hair Center |

### Creating Additional Test Providers

If you need more provider accounts for multi-provider testing:

```bash
# Inside the backend container
php artisan db:seed --class=ProviderSeeder        # Random providers
php artisan db:seed --class=ProviderUserSeeder     # Provider user accounts
php artisan db:seed --class=ProviderTeamMemberSeeder  # Team members for providers
```

### Creating Test Inquiry/Quote Data

```bash
# Seed inquiries that providers can receive
php artisan db:seed --class=InquirySeeder
php artisan db:seed --class=InquirySampleDataSeeder

# Seed quotes at various stages
php artisan db:seed --class=QuoteSeeder
php artisan db:seed --class=QuoteTestDataSeeder

# Seed treatment data
php artisan db:seed --class=TreatmentSeeder
php artisan db:seed --class=BookingDataSeeder
```

---

## 3. Test Scenarios

### TC-P-001: Provider Owner Sign-In & Team Invitation Acceptance

**Objective:** Verify provider access follows the approved model: owner account already created by admin, and additional staff join through invitation acceptance.
**FR Reference:** FR-015 (owner account provisioned by admin), FR-009 (team invitation acceptance), FR-026 (password policy)

#### Pre-conditions
- Fresh environment with seeded provider owner account
- Mailpit running for invitation email checks
- At least one pending invitation available for a new team member

#### Test Steps

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1 | Navigate to http://localhost:5173/auth | Auth Panel displayed with "Log in for Provider" and "Log in for Hairline Team" links | |
| 2 | Click "Log in for Provider" | Redirected to `/auth/provider/login` with Login heading | |
| 3 | Enter seeded provider owner credentials | Fields populated | |
| 4 | Click "Log in" button | "Login successful" toast, redirected to `/` (Dashboard) | |
| 5 | Verify provider name visible in header | Provider name/avatar shown in top-right | |
| 6 | Sign out | Returned to auth screen | |
| 7 | Open Mailpit (http://localhost:8025) and find a pending team invitation email | Invitation email received with secure link | |
| 8 | Open the invitation link | Account setup screen opens with invitee identity pre-filled | |
| 9 | Set password that matches policy (12+ chars, upper/lower/digit/special) and submit | Team member account created with assigned role | |
| 10 | Log in as the newly accepted team member | Dashboard loads with role-appropriate access only | |

#### Seeded Owner Sign-In Shortcut

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1 | Go to `/auth/provider/login` | Login form displayed | |
| 2 | Enter `provider1@hairline.app` / `password123` | Fields populated | |
| 3 | Check "Remember me" checkbox | Checkbox checked | |
| 4 | Click "Log in" | "Login successful" toast, redirected to Dashboard | |

#### Edge Cases to Verify

- [ ] Login with wrong password shows error message
- [ ] Login with non-existent email shows appropriate error
- [ ] Expired invitation link (7 days per FR-009) is rejected; Owner can resend invitation to generate fresh 7-day token
- [ ] Already-used invitation link redirects to login with message "This invitation has already been used. Please log in with your existing credentials."
- [ ] Invitee email already belongs to another provider organization — blocking error: "This email already belongs to another provider team" (FR-009 single-membership rule)
- [ ] Invite duplicate email within same organization — error: "This email is already part of your team"
- [ ] Owner role is NOT assignable from invitation flow — only Manager, Clinical Staff, Billing Staff are selectable (FR-009)
- [ ] Existing Hairline user is redirected to login-only invitation acceptance flow
- [ ] Password field masks input
- [ ] "Forgot password" link navigates to password reset flow
- [ ] Session persists on page refresh after login
- [ ] Logout clears session and redirects to `/auth`

---

### TC-P-002: Provider Onboarding & Profile Setup

**Objective:** Verify provider can complete profile setup including clinic details, credentials, awards, team members, banking, notification preferences, and access Help Centre.
**FR Reference:** FR-009 (Provider Team Management), FR-032 (Provider Dashboard Settings)

#### Pre-conditions
- Logged in as Provider Owner (`provider1@hairline.app`)

#### Profile Management (FR-032)

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1 | Navigate to Settings & Support > Provider Profile | Profile page loads with tabs (logo, name, description, languages, awards) | |
| 2 | Click "Edit Profile" | Profile editor loads with existing data pre-filled | |
| 3 | Upload clinic logo/profile picture (JPEG/PNG, <5MB) | Image uploads with preview; validated for format and size | |
| 4 | Update clinic name, description, contact email, city/location | Form saves per tab with "Profile updated successfully" message | |
| 5 | Select supported languages from multi-select dropdown | Multiple languages selectable from centrally managed list (FR-026) | |
| 6 | Add a new award (name, issuer, description, year, award image <2MB) | Award entry created with image preview | |
| 7 | Edit an existing award — change description | Edit saves successfully | |
| 8 | Delete an award — confirm deletion dialog | Award removed (soft-delete); confirmation dialog shown | |
| 9 | Click "Save Changes" on current tab | Tab-level save with success message; audit trail logged | |

#### Account Settings (FR-032)

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 10 | Navigate to Account Settings section | Phone, timezone, password change options visible | |
| 11 | Update phone number | Phone saved | |
| 12 | Change timezone | Timezone saved; affects time displays | |
| 13 | Change password (enter current + new matching FR-026 policy) | Password updated; success message shown | |

#### Notification Preferences (FR-032)

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 14 | Navigate to Notification Preferences | Individual notification toggles + global channel preferences (email, push) displayed | |
| 15 | Toggle off a specific notification category (e.g., quote alerts) | Preference saved | |
| 16 | Toggle global email channel off | Email notifications disabled; confirmation prompt shown | |
| 17 | Verify preference persists on page refresh | Saved state matches | |

#### Billing Settings (FR-032 — Owner Only)

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 18 | Navigate to Billing Settings (as Owner) | Banking/payout setup page loads | |
| 19 | Enter bank account details for payouts | Bank account info saved securely (format validated by S-02) | |
| 20 | Log in as non-Owner role (e.g., clinician) and attempt to access Billing Settings | Access denied — billing settings restricted to Owner role | |

#### Team Management (FR-009)

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 21 | Navigate to Team management from main nav | Team dashboard loads; current user shown as Owner | |
| 22 | View current team members with roles and status | Team list displays name, role, status (Active/Invited/Suspended) | |
| 23 | Click "Invite Team Member" | Invitation form opens: email, first name, last name, role selection | |
| 24 | Enter team member details, select role (Manager/Clinical Staff/Billing Staff) | Role options shown; Owner role NOT selectable | |
| 25 | Send invitation | Invitation created; "Invited" status shown; email sent to Mailpit | |
| 26 | Verify invitation email content | Email contains: invitation link, provider org name, role offered | |
| 27 | Accept invitation as new team member (set password, accept ToS) | Account created, linked to provider org with assigned role | |
| 28 | Log in as new team member | Dashboard loads with role-appropriate access only | |
| 29 | Change a team member's role (e.g., Clinical Staff → Manager) | Role updated; notification sent to team member | |
| 30 | Suspend a team member | Team member status changes to "Suspended"; access blocked | |
| 31 | Remove a team member | Team member removed from org; confirmation dialog shown | |

#### Help Centre & Support (FR-032)

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 32 | Navigate to Help Centre | Help Centre page loads with FAQs, guides, resources (read-only) | |
| 33 | Submit a support request via Contact Support form | Support case created; confirmation shown with case ID | |
| 34 | View "My Support Cases" — see submitted case | Case visible with status, communication thread | |

#### Edge Cases to Verify

- [ ] Upload image exceeding 5MB — error: "Image too large. Maximum size is 5MB"
- [ ] Upload unsupported image format (e.g., .gif, .bmp) — error message
- [ ] Award image exceeding 2MB — rejected with error
- [ ] Save profile with required field empty (clinic name) — field highlighted in red with error
- [ ] Unsaved changes warning when navigating away from edited tab
- [ ] Non-Owner attempts to change bank details — access denied
- [ ] Invite team member with invalid email format — inline validation error
- [ ] Invite email already used in same org — "This email is already part of your team"
- [ ] Resend expired invitation (7 days) — generates new token, invalidates old one
- [ ] Provider requests account deletion (soft-delete) — request submitted to admin for approval

#### Acceptance Criteria

- [ ] All profile fields save per tab and persist on page refresh
- [ ] File uploads (logo <5MB, award images <2MB) validated and display correct previews
- [ ] Award CRUD (create, read, update, delete) works with soft-delete
- [ ] Language selection from centralized list works (multi-select)
- [ ] Account settings (phone, timezone, password) save correctly
- [ ] Notification preferences (individual toggles + global channels) save and enforce
- [ ] Banking settings restricted to Owner role; other roles cannot access
- [ ] Team invitation emails arrive in Mailpit with correct content
- [ ] Role assignment limited to Manager/Clinical Staff/Billing Staff (not Owner)
- [ ] Role-based permissions restrict access appropriately (verify by logging in as different roles)
- [ ] Help Centre loads and support request submission works
- [ ] All profile changes logged in audit trail

---

### TC-P-003: Receiving & Reviewing Inquiries

**Objective:** Verify provider receives patient inquiries and can review patient details while patient identity remains masked.
**FR Reference:** FR-003 (Inquiry Management)

#### Pre-conditions
- Logged in as provider
- Inquiries seeded (run `InquirySampleDataSeeder` if needed)

#### Test Steps

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1 | Navigate to Inquiries page from sidebar | Inquiries list loads with inquiry cards | |
| 2 | Verify inquiry card shows: HPID, treatment type, date range | Card displays all required fields per FR-003 | |
| 3 | Verify patient identity is masked (no full name, no direct contact) | Patient shown as anonymous/coded identifier | |
| 4 | Click on an inquiry to view details | Inquiry detail page opens | |
| 5 | Verify inquiry detail shows: treatment type (Hair/Beard/Both), selected destinations, patient-requested date ranges | All patient-submitted fields visible (anonymized) | |
| 6 | Review patient detailed hair concerns (nature, duration, severity, previous treatments) | Concern details render clearly | |
| 7 | Review patient medical history summary | Medical info visible (3-tier color-coded alerts: Critical=red, Standard=yellow, None=green) | |
| 8 | Review head scan photo set (V1: multi-view 2D) | Photos load and are viewable/zoomable | |
| 9 | Verify inquiry expiration timer (72 hours from distribution) | Timer/countdown or expiry date displayed | |
| 10 | Check inquiry status indicators | Status clearly shown (New/Viewed/Quote Submitted/Expired) | |
| 11 | Verify multiple inquiries can be viewed in list | Pagination/scrolling works for multiple inquiries | |

#### Edge Cases to Verify

- [ ] Inquiry with no head scan photos — does the detail page handle missing media gracefully?
- [ ] Inquiry with maximum media uploads (5 photos/videos) — all load correctly?
- [ ] Inquiry with critical (red) medical alerts — alert is visually prominent and not missable
- [ ] Expired inquiry — "Create Quote" button is disabled or hidden; clear expired status shown
- [ ] Inquiry from patient who selected multiple countries — destination info displays correctly
- [ ] Rapid navigation between multiple inquiry details — no data bleed between inquiries
- [ ] Inquiry list with 50+ items — pagination/infinite scroll performs without lag

#### Acceptance Criteria

- [ ] Patient identity remains masked until quote acceptance + payment
- [ ] Medical alerts color-coding renders correctly (red/yellow/green per FR-003)
- [ ] Head scan photos load without errors
- [ ] Expired inquiries cannot be quoted
- [ ] Inquiry distribution timestamp is within 5 minutes of creation
- [ ] Maximum 10 providers per inquiry enforced

---

### TC-P-004: Creating & Submitting Quotes

**Objective:** Verify provider can create a comprehensive quote with treatment details, packages, pricing, and appointment slots.
**FR Reference:** FR-004 (Quote Management)

#### Pre-conditions
- Logged in as provider
- At least one active (non-expired) inquiry available

#### Test Steps — Quote Creation (per FR-004)

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1 | From inquiry detail, click "Create Quote" | Quote creation form opens with inquiry context visible | |
| 2 | Select treatment (admin-curated catalog) | Treatment selected | |
| 3 | Select package (optional, provider-bounded) | Package selected with customization options | |
| 4 | Customize package inclusions (e.g., PRP, day-3 wash, translator) | Checklist items toggle on/off | |
| 5 | Check Included Travel Services (`flight`, `hotel`, `transport`) | Services checked; system derives `travel_path` automatically | |
| 6 | Add Custom Services (name, description, cost) | Custom service rows added | |
| 7 | Enter estimated graft count | Numeric field accepts positive integer | |
| 8 | Select Treatment Dates (subset of patient-requested date ranges) | Dates selected; non-overlapping with patient's ranges | |
| 9 | Enter price per selected treatment date | Price fields accept amount with currency per date | |
| 10 | Set pre-scheduled appointment date/time | Date/time picker; must map to one of the selected Treatment Dates | |
| 11 | Select assigned clinician | Clinician selected from active/eligible team members | |
| 12 | Create Treatment Plan (per-day entries: day number, date, description) | Consecutive days with descriptions; no date gaps | |
| 13 | Optionally use 3D Markup (draw on head scan image) | Markup saved with audit | |
| 14 | Optionally apply a promotion code or note | Promotion value accepted | |
| 15 | Add optional note | Note saved | |
| 16 | Review summary (read-only) — verify all fields reflected correctly | Summary matches all entered data including total price calculation | |
| 17 | Submit quote | Quote submitted, status changes to "Submitted" | |
| 18 | Verify quote appears in Quotes list (unified, no tabs) with correct status | Quote visible with patient ID, treatment, price, date, status columns | |

#### Quote Editing & Lifecycle

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 19 | Edit a draft quote — change price and package | Changes saved with versioning | |
| 20 | Edit a submitted (pre-expiry) quote — modify graft count | Edit saved; patient auto-notified of significant edit | |
| 21 | Attempt to edit an expired quote | System blocks edit with clear error message | |
| 22 | Save a quote as draft and return later | Draft persists and is resumable | |
| 23 | Soft-delete a draft quote | Quote moves to Archived status with rationale prompt | |
| 24 | Check quote expiry indicator (48 hours from submission, admin-configured) | Expiry timer/date visible; provider sees computed expiry timestamp (cannot modify) | |
| 25 | Verify provider has 72-hour submission window from inquiry receipt | Cannot submit quote after 72-hour window | |

#### Edge Cases to Verify

- [ ] Submit quote with missing required fields (no treatment, no graft count, no dates, no clinician) — form validation blocks submission with field-level errors
- [ ] Enter 0 or negative graft count — validation rejects
- [ ] Select treatment dates outside patient's requested ranges — system blocks
- [ ] Create Treatment Plan with date gaps (e.g., skip a day) — system blocks
- [ ] Create quote for an inquiry that was just cancelled by patient — system blocks with "Inquiry no longer active" message
- [ ] While drafting a quote, another provider's quote gets accepted — drafting provider receives immediate notification; quote is locked with "Another Quote Accepted" banner
- [ ] Provider attempts to withdraw a quote after patient acceptance — system shows withdrawal request flow, not direct cancellation
- [ ] Quote list displays "Cancelled (Inquiry Cancelled)" quotes as greyed-out with badge and disabled actions
- [ ] Quote list displays "cancelled (other accepted)" quotes with "Another Quote Accepted" badge
- [ ] Auto-archive of abandoned drafts after 7 days

#### Acceptance Criteria

- [ ] All admin-curated treatments selectable
- [ ] Package items and custom services can be added/removed dynamically
- [ ] Price per date calculates correctly; total reflects all packages and custom services
- [ ] Treatment Plan per-day enforces consecutive dates with no gaps
- [ ] Quote cannot be submitted without required fields (treatment, graft count, dates, price per date, clinician, Treatment Plan)
- [ ] Appointment slot maps to one of the selected Treatment Dates
- [ ] Submitted quote is visible and trackable in unified list
- [ ] Draft quotes persist and can be resumed
- [ ] Quote status transitions are correct: Draft → Submitted → Expired/Accepted/Withdrawn/Archived/Cancelled
- [ ] All edits are versioned and auditable

---

### TC-P-004B: Quote Acceptance & Booking Transition (Provider Notification)

**Objective:** Verify provider receives notification and sees updated state when a patient accepts their quote and completes deposit payment (transition from quote to confirmed booking).
**FR Reference:** FR-005 (Quote Acceptance), FR-006 (Booking & Confirmation), FR-007 (Payment)

#### Pre-conditions
- A submitted quote exists for the logged-in provider
- Patient accepts the quote and completes deposit payment (simulated via seeder: `BookingDataSeeder` or `CompleteQuoteSeeder`, or triggered from mobile app)

#### Test Steps

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1 | Trigger quote acceptance + deposit payment (via seeder or mobile app) | Backend processes booking confirmation | |
| 2 | Check provider notification (bell icon / dropdown) | Real-time notification received: "Quote accepted — booking confirmed" (or similar) | |
| 3 | Navigate to Quotes list | Accepted quote shows status "Accepted" / "Booked" | |
| 4 | Verify other providers' quotes for the same inquiry are auto-cancelled | Other quotes show "cancelled (other accepted)" status (verify via admin or DB) | |
| 5 | Navigate to patient detail for the confirmed booking | Patient identity is now fully unmasked (full name, contact info visible) | |
| 6 | Verify booking details match the accepted quote exactly | Treatment type, dates, price, packages, clinician all match | |
| 7 | Check provider's booking/appointment list | New confirmed booking appears in table list format (no calendar view per FR-006) | |
| 8 | Verify deposit payment status visible | Payment status shows "Deposit Paid" with amount and percentage | |

#### Edge Cases to Verify

- [ ] Provider is offline when quote is accepted — notification appears on next login
- [ ] Notification links directly to the relevant booking/appointment detail
- [ ] If patient's deposit payment fails — provider is NOT notified of a confirmed booking; quote stays in "Submitted" status

#### Acceptance Criteria

- [ ] Provider receives timely notification of quote acceptance
- [ ] Patient identity unmasked only after quote acceptance + deposit payment (per constitution)
- [ ] Booking details exactly match the accepted quote
- [ ] Booking appears in table list format (not calendar view, per FR-006)
- [ ] Other providers notified that their quotes are cancelled for this inquiry

---

### TC-P-005: Appointment Confirmation & Scheduling

**Objective:** Verify provider sees confirmed appointments after patient accepts quote and completes payment.
**FR Reference:** FR-006 (Booking & Confirmation)

#### Pre-conditions
- A quote has been accepted by a patient (seed with `BookingDataSeeder` or `CompleteQuoteSeeder`)

#### Test Steps

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1 | Navigate to Appointments page | Appointments list loads | |
| 2 | Verify confirmed appointment shows patient details (now unmasked) | Patient full name, contact visible | |
| 3 | Check appointment date, time, treatment type | All booking details correct | |
| 4 | Verify payment status indicator (deposit received) | Payment status shown: "Deposit Paid" with amount | |
| 5 | View patient payment progress (FR-007) | Deposit status, installment progress (if applicable), final payment status visible | |
| 6 | Verify appointment in table list view | Appointment visible in table list with correct date/time (FR-006: no calendar view) | |
| 7 | Verify notification received for booking confirmation | Notification in dropdown/bell icon | |
| 8 | Access patient messaging (now enabled post-acceptance) | Chat/messaging interface accessible | |
| 9 | Send a test message to patient | Message sent, appears in conversation | |

#### Provider Payment Visibility (FR-007)

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 10 | View booking payment status on appointment/booking detail | Status displays one of: Unpaid / Deposit Paid / Final Paid / Refunded | |
| 11 | View patient payment progress breakdown | Deposit amount, remaining balance, installment progress (if installment plan) visible | |
| 12 | Verify provider CANNOT see patient card/bank details | No payment method details exposed — only status and amounts | |
| 13 | Navigate to payout/earnings section (if available) | Upcoming and completed payouts visible with commission deducted | |
| 14 | Verify payout shows commission deduction | Payout amount = total - commission (percentage or flat rate per FR-015 config) | |

#### Cancellation & Reschedule

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 15 | View cancellation policy details on booking | Cancellation policy visible with refund schedule | |
| 16 | Verify reschedule is NOT available (deferred to V2) | No reschedule button/option; date changes require admin intervention or cancellation/rebooking | |

#### Edge Cases to Verify

- [ ] Booking with installment plan — all installment milestones visible with dates and statuses
- [ ] Booking with full upfront payment — shows "Final Paid" without installment breakdown
- [ ] Patient cancels after deposit — provider sees updated status (refund in progress / cancelled); cancellation policy applied
- [ ] Provider views booking where payment is overdue — overdue indicator visible
- [ ] Provider receives overdue installment alert that may affect booking (FR-007B)
- [ ] Multiple bookings with different payment statuses — each displays independently and correctly
- [ ] Booking in 48-hour slot hold (payment pending after acceptance) — provider sees "pending payment" status, not "confirmed"

#### Acceptance Criteria

- [ ] Patient identity fully revealed after quote acceptance + payment
- [ ] Appointment shows in table list format with correct details (no calendar view per FR-006)
- [ ] Provider receives real-time notification of booking
- [ ] Payment status (deposit/installment/final) visible to provider without card details (FR-007)
- [ ] Commission-deducted payout amounts visible to provider
- [ ] Messaging channel opens between provider and patient (basic verification only — comprehensive messaging deferred)
- [ ] Appointment details match the accepted quote exactly

---

### TC-P-006: Treatment Execution (Check-In to Completion)

**Objective:** Verify provider can check in patient, document the procedure, and update treatment status through completion.
**FR Reference:** FR-010 (Treatment Execution)

#### Pre-conditions
- Confirmed appointment exists
- Patient has completed full payment
- Logged in as provider with clinician access

#### Test Steps

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1 | Navigate to Confirmed section in Patient Management | Confirmed bookings list loads | |
| 1b | Select a confirmed booking (procedure date = today, no outstanding balance) | Case detail page opens in tabbed view: Treatment Plan &#124; Note &#124; Book hotel & Book flight &#124; In Progress | |
| 2 | Initiate patient check-in (click "Check In" button) | System validates: procedure date ≤ today, no outstanding balance, role = Owner/Manager/Clinical Staff | |
| 3 | Validate full payment status during check-in | System confirms payment is complete | |
| 4 | Complete check-in process | Status changes to "In Progress" | |
| 5 | Document procedure: assign clinician | Clinician name recorded | |
| 6 | Document procedure: enter actual graft count | Graft count saved | |
| 7 | Document procedure: add clinical notes | Notes saved to treatment record | |
| 8 | Upload procedure photos (before/during/after) | Photos upload successfully with previews | |
| 9 | Add prescribed post-op medications | Medications list created | |
| 10 | Review treatment summary | All documented details visible in summary | |
| 11 | Mark procedure as complete | Status changes from "In Progress" to next stage | |

#### Treatment Day Management (per FR-010)

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 12 | View Treatment Plan tab with per-day entries from accepted quote | Day descriptions are read-only; day statuses editable | |
| 13 | Update Day 1 status to "In progress" | Status saved; synced to patient app and admin in real-time | |
| 14 | Add day note for Day 1 (provider-only clinical observation) | Note saved; NOT visible to patient | |
| 15 | Update Day 1 status to "Finished" | Status transitions correctly | |
| 16 | Repeat for subsequent days until all days are in terminal status | All days show Finished / Cancelled/Deferred / Need caution/attention | |
| 17 | Click "End Treatment" button | End of Treatment modal opens | |
| 18 | Fill end-of-treatment fields: conclusion notes, prescription, advice, medication, actual graft count, final head scan photo set | All fields accept input | |
| 19 | Submit end of treatment | System validates required fields; treatment documented; FR-011 aftercare triggered | |

#### Edge Cases to Verify (per FR-010 Alternative Flows)

- [ ] **Check-in with outstanding balance:** Check In button is disabled with clear reason ("Outstanding balance — full payment required")
- [ ] **Check-in for future procedure date:** Check In button is disabled ("Procedure date has not arrived yet")
- [ ] **Role-based access:** Billing Staff can view treatment details but CANNOT click Check In or document treatment; Owner/Manager/Clinical Staff can
- [ ] **Patient early arrival:** Provider clicks Check In early; system shows confirmation prompt for early check-in; if confirmed, treatment proceeds with early check-in timestamp recorded
- [ ] **Patient no-show:** Provider clicks "Cancel/Close Case" with reason "No-show"; system notifies admin; admin handles status transition and deposit retention manually
- [ ] **Medical complication prevents start:** Provider reviews Note tab, identifies disqualifying condition, clicks "Cancel/Close Case" with reason "Medical postponement"; system notifies admin for manual case management (no financial penalty)
- [ ] **Treatment interrupted during procedure:** Provider documents interruption in day note; sets day status to "Need caution/attention" or "Cancelled/Deferred"; if treatment cannot resume, provider closes case and admin is notified
- [ ] **Provider cancels in-progress case:** Provider clicks "Cancel/Close Case", selects reason from list (No-show, Patient cancellation, Medical, Operational, Other), adds note; system notifies admin for manual resolution
- [ ] **End Treatment with missing required fields:** System blocks submission and highlights missing fields
- [ ] **Day status "Need caution/attention":** Visual indicator clearly distinguishes this from normal "In progress" or "Finished"
- [ ] **Upload head scan photo set at beginning of treatment:** Photos upload and display correctly; stored securely
- [ ] **Resume documentation for an "In Progress" treatment from the In Progress section:** Treatment state preserved; provider can continue where they left off

#### Acceptance Criteria

- [ ] Check-in blocked if payment is incomplete OR procedure date is in the future
- [ ] Treatment status transitions: Confirmed → In Progress → (End Treatment triggers FR-011)
- [ ] Day-by-day status management works: Not started → In progress → Finished / Need caution/attention / Cancelled/Deferred
- [ ] Day descriptions (from quote Treatment Plan) are read-only; day notes are provider-only
- [ ] Real-time day status sync to patient app and admin platform
- [ ] All procedure documentation fields save correctly
- [ ] Head scan photo sets upload without error (V1: multi-view 2D photos)
- [ ] Medication prescriptions are associated with the treatment record
- [ ] Cancel/Close Case flow notifies admin with reason
- [ ] Role-based access enforced (Billing Staff = view-only)

---

### TC-P-007: Aftercare Setup & Monitoring

**Objective:** Verify provider can set up aftercare plan, assign templates, and monitor patient recovery.
**FR Reference:** FR-011 (Aftercare & Recovery)

#### Pre-conditions
- Treatment procedure marked as complete
- Aftercare templates seeded (`AftercareTemplatesSeeder`)

#### Test Steps

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1 | Navigate to AfterCare section from treatment | Aftercare setup page loads | |
| 2 | Select aftercare template from available options | Template selected with preview of milestones | |
| 3 | Customize aftercare instructions (edit template content) | Customizations saved | |
| 4 | Set milestone schedule (e.g., Day 1, Week 1, Month 1, Month 3, Month 6, Month 12) | Milestones created with dates | |
| 5 | Configure scan photo upload intervals for patient | Scan schedule set | |
| 6 | Configure questionnaire schedule (pain, sleep, compliance) | Questionnaire intervals set | |
| 7 | Activate aftercare plan | Status changes to "Aftercare" | |
| 8 | View aftercare dashboard/progress tracker | Dashboard shows milestones, patient submissions | |
| 9 | Review a patient-submitted scan photo (if test data exists) | Photo viewable with comparison tools | |
| 10 | Review patient questionnaire responses | Responses displayed in readable format | |
| 11 | Add aftercare notes/comments | Notes saved to aftercare record | |

#### Edge Cases to Verify

- [ ] **No aftercare template available:** System handles gracefully — provider can still create a custom plan or is blocked with clear message
- [ ] **Customize milestone durations beyond template defaults:** Modified durations persist correctly
- [ ] **Add patient-specific medications:** Medication name, dosage, frequency, special instructions all save correctly
- [ ] **Patient misses a milestone scan submission:** Provider sees overdue indicator on that milestone
- [ ] **Multiple aftercare cases active for same provider:** Each case displays independently with correct patient data
- [ ] **Aftercare plan activated before end-of-treatment is fully documented:** System blocks or warns
- [ ] **View aftercare for a treatment-linked case vs standalone aftercare case:** Both display correctly (if standalone is in scope)

#### Acceptance Criteria

- [ ] Aftercare templates load with pre-configured milestones (admin-created)
- [ ] Template customization (instructions, milestone durations, medications) persists
- [ ] Milestone dates calculate correctly from treatment completion date
- [ ] Patient scan photo set submissions visible to provider (V1: 2D multi-view)
- [ ] Questionnaire responses (pain, sleep, compliance) render correctly
- [ ] Aftercare specialist can be assigned (if applicable)
- [ ] Real-time notifications for patient aftercare submissions
- [ ] Medication setup (name, dosage, frequency, instructions) saves correctly

---

### TC-P-008: Treatment Completion & Closure

**Objective:** Verify provider can mark treatment as fully complete after aftercare period.
**FR Reference:** FR-010, FR-011

#### Pre-conditions
- Aftercare plan active with milestones progressed

#### Test Steps

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1 | Navigate to treatment/aftercare with completed milestones | Treatment detail shows aftercare progress | |
| 2 | Review all aftercare milestones marked as complete | All milestones show completed status | |
| 3 | Review final patient scan photos and outcomes | Final documentation accessible | |
| 4 | Mark treatment as "Completed" | Status changes to "Completed" | |
| 5 | Verify treatment appears in completed treatments list | Visible in provider's historical records | |
| 6 | Verify treatment record is archived in completed list | Treatment visible in provider's completed treatments history | |
| 7 | Verify patient messaging channel status | Messaging may transition to read-only or archive | |

#### Edge Cases to Verify

- [ ] **Mark treatment complete before all aftercare milestones are done:** System blocks or warns that milestones are still pending
- [ ] **Attempt to edit a completed treatment record:** System blocks edits (or requires explicit unlock/admin intervention)
- [ ] **View full treatment timeline from inquiry through completion:** All stages (inquiry → quote → booking → payment → treatment → aftercare → completed) are traceable
- [ ] **Provider has multiple completed treatments:** List/pagination works; each treatment has correct data
- [ ] **Messaging channel after completion:** Channel transitions to read-only or archived state

#### Acceptance Criteria

- [ ] Treatment status transitions: Aftercare → Completed
- [ ] Completed treatment archived in provider's history
- [ ] Completed treatment visible in provider's treatment history
- [ ] Full treatment timeline viewable from start to finish (all linked records)
- [ ] No further edits allowed on completed treatment (or with explicit unlock)
- [ ] Patient messaging channel appropriately transitioned (read-only or archived)

---

## 4. End-to-End Flow Checklist

Complete walkthrough of the entire treatment flow for a single patient-provider pair:

| # | Stage | Status | Notes |
|---|-------|--------|-------|
| 1 | Provider owner logs in / invited staff accepts invite | ☐ | |
| 2 | Provider completes profile & onboarding | ☐ | |
| 3 | Provider receives inquiry notification | ☐ | |
| 4 | Provider reviews inquiry (masked patient) | ☐ | |
| 5 | Provider creates and submits quote (with Treatment Plan, dates, clinician) | ☐ | |
| 6 | Quote accepted by patient, deposit paid | ☐ | Requires patient-side action or seeded data |
| 6b | Provider receives acceptance notification, patient unmasked | ☐ | TC-P-004B |
| 7 | Provider views confirmed appointment with payment status | ☐ | |
| 8 | Provider checks in patient | ☐ | |
| 9 | Provider documents treatment procedure | ☐ | |
| 10 | Provider completes procedure | ☐ | |
| 11 | Provider sets up aftercare plan | ☐ | |
| 12 | Provider monitors aftercare milestones | ☐ | |
| 13 | Provider marks treatment as completed | ☐ | |

---

## 5. Manual Run Summary

Use this only if a manual walkthrough is executed. Keep entries concise and business-focused.

### Run Statistics

| Metric | Count |
|--------|-------|
| Total scenarios executed | _____ |
| PASS | _____ |
| FAIL | _____ |
| BLOCKED | _____ |
| SKIP | _____ |

### Gaps & Discrepancies Found

| # | What is Broken | FR Violated | Risk if Unfixed | Scenario / Step |
|---|---------------|-------------|-----------------|-----------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

### Blocked Items

| Scenario / Step | Reason Blocked | Action Needed |
|-----------------|----------------|---------------|
| | | |

---

## 6. Defect Reporting Template

When a test step fails, log the defect using this format:

```
**Defect ID:** DEF-P-XXX
**Test Case:** TC-P-XXX, Step X
**Severity:** Critical / High / Medium / Low
**Summary:** [One-line description]
**Steps to Reproduce:**
1. ...
2. ...
3. ...
**Expected Result:** [What should happen]
**Actual Result:** [What actually happened]
**Screenshot/Recording:** [Attach or link]
**Browser/Device:** Chrome XX / macOS
**Environment:** Local (Docker backend + npm dev frontend)
**Notes:** [Any additional context]
```
