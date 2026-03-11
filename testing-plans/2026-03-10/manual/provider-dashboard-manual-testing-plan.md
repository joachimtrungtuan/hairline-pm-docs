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

## Table of Contents

1. [Test Environment Setup](#1-test-environment-setup)
2. [Test Data Seeding](#2-test-data-seeding)
3. [Test Scenarios](#3-test-scenarios)
   - [TC-P-001: Provider Owner Sign-In & Team Invitation Acceptance](#tc-p-001-provider-owner-sign-in--team-invitation-acceptance)
   - [TC-P-002: Provider Onboarding & Profile Setup](#tc-p-002-provider-onboarding--profile-setup)
   - [TC-P-003: Receiving & Reviewing Inquiries](#tc-p-003-receiving--reviewing-inquiries)
   - [TC-P-004: Creating & Submitting Quotes](#tc-p-004-creating--submitting-quotes)
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
- [ ] Expired invitation link is rejected and re-invite is required
- [ ] Existing Hairline user is redirected to login-only invitation acceptance flow
- [ ] Password field masks input
- [ ] "Forgot password" link navigates to password reset flow
- [ ] Session persists on page refresh after login
- [ ] Logout clears session and redirects to `/auth`

---

### TC-P-002: Provider Onboarding & Profile Setup

**Objective:** Verify provider can complete profile setup including clinic details, credentials, team members, and banking information.
**FR Reference:** FR-009 (Provider Team Management), FR-032 (Provider Dashboard Settings)

#### Pre-conditions
- Logged in as Provider Owner (`provider1@hairline.app`)

#### Test Steps

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1 | Navigate to Settings page | Settings page with tabs/sections loads | |
| 2 | Update clinic name, description, and contact info | Form saves successfully with confirmation | |
| 3 | Upload clinic logo and gallery images | Images upload with preview, saved to profile | |
| 4 | Add credentials: certifications, licenses, years of experience | Credentials section populated and saved | |
| 5 | Add banking/payment details (FR-032) | Banking details saved securely | |
| 6 | Configure notification preferences | Preferences saved | |
| 7 | Navigate to Team management | Team page loads with current provider as Owner | |
| 8 | Invite a new team member (e.g., clinician) via email | Invitation sent, pending status shown | |
| 9 | Set team member role and permissions | Role assigned (Clinician/Manager/Billing Staff) | |
| 10 | Verify assigned languages (English, Turkish) | Language assignments visible | |

#### Acceptance Criteria

- [ ] All profile fields save and persist on page refresh
- [ ] File uploads display correct previews
- [ ] Team invitation emails arrive in Mailpit
- [ ] Role-based permissions restrict access appropriately (test by logging in as clinician vs owner)
- [ ] Incomplete profile shows completion indicator or prompts

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
| 5 | Review patient medical history summary | Medical info visible (color-coded alerts: red/yellow/green) | |
| 6 | Review head scan photos | Photos load and are viewable/zoomable | |
| 7 | Verify inquiry expiration timer (72 hours from distribution) | Timer/countdown or expiry date displayed | |
| 8 | Check inquiry status indicators | Status clearly shown (New/Viewed/Quote Submitted/Expired) | |
| 9 | Verify multiple inquiries can be viewed in list | Pagination/scrolling works for multiple inquiries | |

#### Acceptance Criteria

- [ ] Patient identity remains masked until quote acceptance + payment
- [ ] Medical alerts color-coding renders correctly
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

#### Test Steps

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1 | From inquiry detail, click "Create Quote" or equivalent | Quote creation form opens | |
| 2 | Select treatment type (FUE/FUT/DHI) | Treatment type selected | |
| 3 | Enter graft count estimate | Numeric field accepts valid graft count | |
| 4 | Set base treatment price | Price field accepts amount with currency | |
| 5 | Add optional packages: hotel accommodation | Package added with pricing | |
| 6 | Add optional packages: airport transport | Package added with pricing | |
| 7 | Add optional packages: PRP treatment | Package added with pricing | |
| 8 | Enter provider credentials and experience highlights | Credentials section populated | |
| 9 | Set pre-scheduled appointment date/time (one per quote) | Date/time picker allows single slot selection; must map to one of the selected Treatment Dates | |
| 10 | Review total price calculation (base + packages) | Total auto-calculates correctly | |
| 11 | Submit quote | Quote submitted, status changes to "Submitted" | |
| 12 | Verify quote appears in Quotes list with "Submitted" status | Quote visible in quotes section | |
| 13 | Attempt to edit a submitted quote | Edit capability available (or appropriate restriction) | |

#### Quote Expiry Testing

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 14 | Check quote expiry indicator (48 hours from submission) | Expiry timer/date visible on quote | |
| 15 | Verify provider has 72-hour submission window from inquiry receipt | Cannot submit quote after 72-hour window | |

#### Acceptance Criteria

- [ ] All treatment types (FUE, FUT, DHI) selectable
- [ ] Package items can be added/removed dynamically
- [ ] Total price calculates correctly as packages change
- [ ] Quote cannot be submitted without required fields (treatment type, graft count, price)
- [ ] Appointment slots conform to provider's available schedule
- [ ] Submitted quote is visible and trackable
- [ ] Draft quotes can be saved and resumed

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
| 4 | Verify payment status indicator (deposit received) | Payment status shown (partial/full) | |
| 5 | Verify appointment in table list view | Appointment visible in table list with correct date/time (FR-006: no calendar view) | |
| 6 | Verify notification received for booking confirmation | Notification in dropdown/bell icon | |
| 7 | Access patient messaging (now enabled post-acceptance) | Chat/messaging interface accessible | |
| 8 | Send a test message to patient | Message sent, appears in conversation | |

#### Acceptance Criteria

- [ ] Patient identity fully revealed after quote acceptance + payment
- [ ] Appointment shows in table list format with correct details (no calendar view per FR-006)
- [ ] Provider receives real-time notification of booking
- [ ] Messaging channel opens between provider and patient
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
| 1 | Navigate to the confirmed appointment/treatment | Treatment detail page loads | |
| 2 | Initiate patient check-in | Check-in form/flow starts | |
| 3 | Validate full payment status during check-in | System confirms payment is complete | |
| 4 | Complete check-in process | Status changes to "In Progress" | |
| 5 | Document procedure: assign clinician | Clinician name recorded | |
| 6 | Document procedure: enter actual graft count | Graft count saved | |
| 7 | Document procedure: add clinical notes | Notes saved to treatment record | |
| 8 | Upload procedure photos (before/during/after) | Photos upload successfully with previews | |
| 9 | Add prescribed post-op medications | Medications list created | |
| 10 | Review treatment summary | All documented details visible in summary | |
| 11 | Mark procedure as complete | Status changes from "In Progress" to next stage | |

#### Acceptance Criteria

- [ ] Check-in blocked if payment is incomplete
- [ ] Treatment status transitions: Confirmed → In Progress → (procedure complete)
- [ ] All procedure documentation fields save correctly
- [ ] Photos upload without error and display in treatment timeline
- [ ] Medication prescriptions are associated with the treatment record
- [ ] Treatment timeline/history shows chronological entries

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

#### Acceptance Criteria

- [ ] Aftercare templates load with pre-configured milestones
- [ ] Template customization persists
- [ ] Milestone dates calculate correctly from treatment date
- [ ] Patient scan submissions visible to provider
- [ ] Questionnaire responses render correctly
- [ ] Aftercare specialist can be assigned (if applicable)
- [ ] Real-time notifications for patient aftercare submissions

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

#### Acceptance Criteria

- [ ] Treatment status transitions: Aftercare → Completed
- [ ] Completed treatment archived in provider's history
- [ ] Completed treatment visible in provider's treatment history
- [ ] Full treatment timeline viewable from start to finish
- [ ] No further edits allowed on completed treatment (or with explicit unlock)

---

## 4. End-to-End Flow Checklist

Complete walkthrough of the entire treatment flow for a single patient-provider pair:

| # | Stage | Status | Notes |
|---|-------|--------|-------|
| 1 | Provider owner logs in / invited staff accepts invite | ☐ | |
| 2 | Provider completes profile & onboarding | ☐ | |
| 3 | Provider receives inquiry notification | ☐ | |
| 4 | Provider reviews inquiry (masked patient) | ☐ | |
| 5 | Provider creates and submits quote | ☐ | |
| 6 | Quote accepted, appointment confirmed | ☐ | Requires patient-side action or seeded data |
| 7 | Provider views confirmed appointment | ☐ | |
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
