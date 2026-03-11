# Admin Dashboard — Manual Testing Plan (Reference Walkthrough)

**Date:** 2026-03-10
**Scope:** Main treatment flow — from sign-in through treatment completion (admin oversight)
**Dashboard:** Admin/Hairline Team Dashboard (`profile_type: "hairline"`)
**Test Type:** Manual (exploratory + scripted)
**Related FRs:** FR-031, FR-003, FR-004, FR-006, FR-007/007B, FR-010, FR-011, FR-015, FR-016, FR-020

---

## Usage Note

- This document is a manual walkthrough reference only.
- The canonical developer handoff and result-report artifact is [test-checklist-report.md](/Users/joachimtrungtuan/My%20Documents/Va%CC%82n%20Tay%20Media/Products/Hairline/local-docs/testing-plans/2026-03-10/automated/admin-dashboard/test-checklist-report.md).
- If any manual run is executed, record the final business gaps and discrepancies in the summary section of the automated checklist/report, not only inside step-level notes here.

## Table of Contents

1. [Test Environment Setup](#1-test-environment-setup)
2. [Test Data Seeding](#2-test-data-seeding)
3. [Test Scenarios](#3-test-scenarios)
   - [TC-A-001: Admin Team Access & Sign-In](#tc-a-001-admin-team-access--sign-in)
   - [TC-A-002: Admin Onboarding & Dashboard Overview](#tc-a-002-admin-onboarding--dashboard-overview)
   - [TC-A-003: Managing Providers & Patients](#tc-a-003-managing-providers--patients)
   - [TC-A-004: Monitoring Inquiries](#tc-a-004-monitoring-inquiries)
   - [TC-A-005: Overseeing Quotes & Pricing](#tc-a-005-overseeing-quotes--pricing)
   - [TC-A-006: Booking & Payment Administration](#tc-a-006-booking--payment-administration)
   - [TC-A-007: Treatment Oversight & Progress Monitoring](#tc-a-007-treatment-oversight--progress-monitoring)
   - [TC-A-008: Aftercare Administration](#tc-a-008-aftercare-administration)
   - [TC-A-009: Treatment Completion](#tc-a-009-treatment-completion)
4. [End-to-End Admin Oversight Checklist](#4-end-to-end-admin-oversight-checklist)
5. [Manual Run Summary](#5-manual-run-summary)
6. [Defect Reporting Template](#6-defect-reporting-template)

---

## 1. Test Environment Setup

### Prerequisites

Same as Provider testing — all services must be running:

| Component | Setup Command | URL |
|-----------|--------------|-----|
| Backend (Docker) | `cd main/hairline-backend && docker-compose up -d` | http://localhost:80 |
| Frontend (Dev) | `cd main/hairline-frontend && npm run dev` | http://localhost:5173 |
| WebSocket (Reverb) | Included in Docker compose | ws://localhost:8081 |
| Database (MySQL) | Included in Docker compose | localhost:3307 |
| Mailpit (Email) | Included in Docker compose | http://localhost:8025 |

### Verification Checklist

- [ ] All Docker containers running (`docker-compose ps`)
- [ ] Frontend accessible at http://localhost:5173
- [ ] Backend API responding at http://localhost:80
- [ ] Mailpit UI accessible at http://localhost:8025

### Browser Requirements

- Chrome (latest) — primary
- DevTools open (Network tab) for API monitoring

---

## 2. Test Data Seeding

### Step-by-Step Seeding Instructions

```bash
# 1. Enter the backend container
docker-compose exec php bash

# 2. Run fresh migrations (WARNING: destroys existing data)
php artisan migrate:fresh

# 3. Seed with Full data for complete admin oversight testing
php artisan db:seed --class=FullSeeder
```

### Pre-Seeded Admin Test Accounts

| Account | Email | Password | Role |
|---------|-------|----------|------|
| Admin User | `admin@example.com` | `password` | Hairline Team (Admin) |

### Creating Additional Admin Accounts

```bash
# Inside the backend container
php artisan db:seed --class=UserSeeder           # General users
php artisan db:seed --class=RolePermissionSeeder  # Roles & permissions
php artisan db:seed --class=SupportUserSeeder     # Support team users
```

### Seeding Data for Each Treatment Flow Stage

```bash
# Providers for admin to manage
php artisan db:seed --class=ProviderSeeder
php artisan db:seed --class=ProviderUserSeeder

# Patients for admin to oversee
php artisan db:seed --class=PatientSeeder

# Inquiries at various stages
php artisan db:seed --class=InquirySampleDataSeeder

# Quotes at various stages (draft, submitted, accepted, expired)
php artisan db:seed --class=QuoteTestDataSeeder
php artisan db:seed --class=SubmittedQuotesSeeder
php artisan db:seed --class=CompleteQuoteSeeder

# Bookings and payments
php artisan db:seed --class=BookingDataSeeder
php artisan db:seed --class=PaymentSeeder
php artisan db:seed --class=PaymentHistorySeeder

# Treatments and aftercare
php artisan db:seed --class=TreatmentSeeder
php artisan db:seed --class=AftercareSeeder
php artisan db:seed --class=AfterCareFullDataSeeder

# Financial data for billing views
php artisan db:seed --class=FinancialDataSeeder
php artisan db:seed --class=ProviderBillingSeeder

# Dashboard sample data
php artisan db:seed --class=HairlineDashboardSampleDataSeeder
```

---

## 3. Test Scenarios

### TC-A-001: Admin Team Access & Sign-In

**Objective:** Verify provisioned admin team members can sign in and that revoked admin access is enforced.
**FR Reference:** FR-031 (Admin Access Control & Permissions)

#### Pre-conditions
- Seeded data with at least one active admin account and one revoked/removed admin account
- Provider test account available for route-isolation checks

#### Test Steps

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1 | Navigate to http://localhost:5173/auth | Auth Panel displayed with both login links | |
| 2 | Click "Log in for Hairline Team" | Redirected to `/auth/hairline-team/login` | |
| 3 | Enter `admin@example.com` / `password` | Fields populated | |
| 4 | Click "Log in" | "Login successful" toast, redirected to Dashboard | |
| 5 | Verify "Admin User" name visible in header | Admin name displayed in top-right | |
| 6 | Verify admin-specific navigation sidebar | Sidebar shows: Overview, Patients, Settings, Billing, etc. | |

#### Provisioned Team-Member Access Control

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 7 | Sign out from the active admin session | Returned to auth screen | |
| 8 | Attempt login using revoked or removed admin credentials | Access denied; protected admin routes remain inaccessible | |
| 9 | Log in with another active provisioned admin/team member account | Dashboard loads with only the permitted modules for that role | |
| 10 | While logged in as admin, navigate to a provider-only route | Access blocked or redirected | |
| 11 | Log in as provider in a separate session and navigate to an admin-only route | Access blocked or redirected | |

#### Edge Cases

- [ ] Admin login with wrong password shows error
- [ ] Revoked admin session is no longer usable after access removal
- [ ] Admin cannot access provider-specific routes
- [ ] Provider cannot access admin-specific routes (role isolation)
- [ ] Session timeout behavior (if applicable)

---

### TC-A-002: Admin Onboarding & Dashboard Overview

**Objective:** Verify admin dashboard shows real-time platform metrics and overview.
**FR Reference:** FR-016 (Admin Management)

#### Pre-conditions
- Logged in as admin (`admin@example.com`)
- Dashboard sample data seeded

#### Test Steps

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1 | View main dashboard/overview page | Dashboard loads with summary widgets | |
| 2 | Verify key metrics displayed: total providers, total patients | Numbers shown and non-zero (with seeded data) | |
| 3 | Verify active inquiries count | Count matches seeded inquiry data | |
| 4 | Verify active treatments count | Count displayed | |
| 5 | Check revenue/billing summary widget | Financial summary visible | |
| 6 | Verify notifications bell icon | Notifications dropdown functional | |
| 7 | Click notification to see detail | Notification expands or navigates to source | |
| 8 | Check real-time update (if WebSocket active) | New data appears without page refresh | |

#### Acceptance Criteria

- [ ] Dashboard loads within 3 seconds
- [ ] All metric widgets display data (no empty/error states with seeded data)
- [ ] Navigation sidebar reflects admin role (not provider role)
- [ ] Notifications dropdown shows with infinite scroll (FR-020)

---

### TC-A-003: Managing Providers & Patients

**Objective:** Verify admin can view, search, and manage provider and patient records.
**FR Reference:** FR-015 (Provider Management), FR-016 (Patient Management)

#### Pre-conditions
- Multiple providers and patients seeded

#### Provider Management

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1 | Navigate to provider management section | Provider list loads | |
| 2 | Search for a provider by name | Search results filter correctly | |
| 3 | Click on a provider to view details | Provider detail page loads with: clinic info, team, credentials | |
| 4 | View provider detail page | Provider detail page shows clinic info, team members, credentials, status | |
| 5 | Check provider status controls | Ability to set provider status: Active, Suspended, or Deactivated (FR-015) | |

#### Patient Management

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 6 | Navigate to Patients section | Patient list/table loads | |
| 7 | Search for a patient by name or ID | Search results filter correctly | |
| 8 | Sort patient table by various columns | Sorting works (name, date, status) | |
| 9 | Click on a patient to view details | Patient detail page: medical history, inquiries, treatments | |
| 10 | View patient's treatment history | Treatment timeline visible | |
| 11 | View patient billing/payment records | Payment history accessible | |

#### Acceptance Criteria

- [ ] Search is responsive and accurate
- [ ] Pagination works for large datasets
- [ ] Table sorting persists when navigating back
- [ ] Patient data shows masked/anonymized status correctly (before payment)
- [ ] Admin can view all data across all providers

---

### TC-A-004: Monitoring Inquiries

**Objective:** Verify admin can monitor all inquiries across the platform, including distribution status and expiration.
**FR Reference:** FR-003, FR-016

#### Pre-conditions
- Inquiries seeded at various stages (new, distributed, expired)

#### Test Steps

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1 | Navigate to inquiries oversight section | All platform inquiries listed | |
| 2 | Filter inquiries by status (New/Distributed/Expired/Quoted) | Filter works correctly | |
| 3 | View inquiry distribution details | Shows which providers received the inquiry | |
| 4 | Verify inquiry was distributed within 5-minute SLA | Timestamp difference between creation and distribution ≤ 5 min | |
| 5 | Check expired inquiry handling | Expired inquiries marked clearly, no actions available | |
| 6 | Verify inquiry-quote linkage visible | Can see which quotes were submitted for each inquiry | |
| 7 | Flag a conversation related to an inquiry | Flag saved (FR-016) | |

#### Acceptance Criteria

- [ ] Admin sees all inquiries across all providers (platform-wide view)
- [ ] Status filters narrow results correctly
- [ ] Distribution SLA tracking visible
- [ ] Expired inquiries handled gracefully
- [ ] Conversation flagging works (FR-016)

---

### TC-A-005: Overseeing Quotes & Pricing

**Objective:** Verify admin can monitor quotes, review pricing, and manage commission settings.
**FR Reference:** FR-004, FR-016

#### Pre-conditions
- Quotes at various stages seeded

#### Test Steps

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1 | Navigate to quotes/billing oversight | Quote list loads across all providers | |
| 2 | Filter quotes by status (Draft/Submitted/Accepted/Expired) | Filters work | |
| 3 | View individual quote details | Full quote visible: treatment type, packages, pricing, appointment | |
| 4 | Verify commission rate configuration | Commission settings accessible in admin settings | |
| 5 | Verify quote status transitions visible | Quote statuses (Draft/Submitted/Accepted/Expired) accurately displayed | |
| 6 | View quote expiry enforcement (48-hour) | Expired quotes marked and non-actionable | |

#### Acceptance Criteria

- [ ] Admin has visibility into all quotes platform-wide
- [ ] Commission rates apply correctly to quote pricing
- [ ] Quote status transitions are accurate
- [ ] Financial summaries match individual quote totals

---

### TC-A-006: Booking & Payment Administration

**Objective:** Verify admin can monitor bookings, process payments, manage deposits, and handle installment plans.
**FR Reference:** FR-006, FR-007/007B

#### Pre-conditions
- Bookings and payments seeded

#### Test Steps

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1 | Navigate to billing/payment administration | Payment records load | |
| 2 | View all bookings with payment status | List shows: patient, provider, amount, status (deposit/partial/full) | |
| 3 | Verify deposit percentage (20-30% configurable) | Deposit amount matches admin-configured percentage | |
| 4 | View installment plan details for a patient | Installment schedule visible (2-9 monthly, interest-free) | |
| 5 | Check payment must complete 30 days before procedure | System enforces 30-day rule | |
| 6 | View payment processing history (Stripe) | Transaction IDs, amounts, dates visible | |
| 7 | Check multi-currency support | Currency correctly displayed per transaction | |
| 8 | Navigate to patient billing detail page | Detailed billing breakdown shown | |
| 9 | Verify provider payout/billing records | Provider billing section shows earned amounts | |

#### Acceptance Criteria

- [ ] All payment records visible to admin
- [ ] Deposit percentage configurable in admin settings
- [ ] Installment plans calculate correctly
- [ ] Multi-currency amounts display correctly
- [ ] Payment history shows complete audit trail
- [ ] Provider billing/commission calculations are accurate

---

### TC-A-007: Treatment Oversight & Progress Monitoring

**Objective:** Verify admin can monitor active treatments, view progress, and intervene if needed.
**FR Reference:** FR-010, FR-016

#### Pre-conditions
- Treatments at various stages seeded (confirmed, in-progress, aftercare)

#### Test Steps

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1 | Navigate to treatments/patients overview | Active treatments listed | |
| 2 | Filter by treatment status (Confirmed/In Progress/Aftercare/Completed) | Filters work correctly | |
| 3 | View a treatment in "In Progress" status | Treatment detail shows: provider, patient, procedure docs | |
| 4 | View treatment timeline | Chronological view of all treatment events | |
| 5 | Check procedure documentation (photos, notes, medications) | Documentation uploaded by provider visible to admin | |
| 6 | Verify admin can add notes or flags to a treatment | Admin notes saved | |
| 7 | Check real-time status updates | Treatment status changes reflected without page refresh | |

#### Acceptance Criteria

- [ ] Admin has read access to all treatment records
- [ ] Treatment status transitions visible in timeline
- [ ] Procedure documentation (photos, notes) viewable
- [ ] Admin can flag or annotate treatments
- [ ] Filter/search works across large treatment datasets

---

### TC-A-008: Aftercare Administration

**Objective:** Verify admin can monitor aftercare plans, assign aftercare specialists, and review patient progress.
**FR Reference:** FR-011, FR-016

#### Pre-conditions
- Treatments in aftercare stage seeded (`AfterCareFullDataSeeder`)

#### Test Steps

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1 | Navigate to aftercare administration | Aftercare cases listed | |
| 2 | View aftercare plan for a patient | Plan shows: template, milestones, patient submissions | |
| 3 | Assign aftercare specialist to a case | Specialist assigned, reflected in case detail | |
| 4 | View patient milestone progress | Milestone completion status visible (Day 1, Week 1, etc.) | |
| 5 | Review patient scan photo submissions | Photos viewable with timestamps | |
| 6 | Review patient questionnaire responses (pain, sleep, compliance) | Responses displayed in structured format | |
| 7 | View aftercare messaging/communication | Aftercare conversations accessible | |
| 8 | Check standalone aftercare service pricing configuration | Template-based pricing configurable per FR-011: Fixed Price, Monthly Subscription, or Both; multi-currency support (pricing set per template per currency) | |

#### Acceptance Criteria

- [ ] Admin can view all aftercare cases platform-wide
- [ ] Aftercare specialist assignment works
- [ ] Patient milestone tracking accurate
- [ ] Scan photo comparisons available
- [ ] Questionnaire responses render correctly
- [ ] Aftercare pricing configurable

---

### TC-A-009: Treatment Completion

**Objective:** Verify admin can view completed treatments and their full lifecycle records.
**FR Reference:** FR-010, FR-011, FR-016

#### Pre-conditions
- Completed treatments in the system

#### Test Steps

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1 | Navigate to completed treatments view | Completed treatments listed | |
| 2 | View a completed treatment's full record | Full timeline: inquiry → quote → booking → treatment → aftercare → completion | |
| 3 | Check treatment outcome documentation | Final photos, notes, patient satisfaction visible | |
| 4 | Verify all linked records are consistent | Inquiry, quote, booking, payment, treatment, aftercare all cross-linked correctly | |
| 5 | Verify completed treatment is read-only (or requires explicit unlock to edit) | No accidental modifications to finalized records | |

#### Acceptance Criteria

- [ ] Completed treatments show full lifecycle history
- [ ] Treatment outcome documentation (photos, notes) viewable
- [ ] All linked records (inquiry → quote → booking → payment → aftercare) are consistent
- [ ] Completed treatments are appropriately locked from accidental edits

---

## 4. End-to-End Admin Oversight Checklist

Admin parallel verification of the treatment flow (performed alongside provider flow):

| # | Stage | Admin Action | Status | Notes |
|---|-------|-------------|--------|-------|
| 1 | Admin team access | Log in as active Hairline Team member | ☐ | |
| 2 | Dashboard overview | Verify platform metrics | ☐ | |
| 3 | Provider management | View/search providers | ☐ | |
| 4 | Inquiry monitoring | Verify inquiry distribution | ☐ | |
| 5 | Quote oversight | Monitor submitted quotes | ☐ | |
| 6 | Booking confirmation | Verify booking & payment records | ☐ | |
| 7 | Payment administration | Check deposit, installments | ☐ | |
| 8 | Treatment monitoring | View in-progress treatment | ☐ | |
| 9 | Aftercare oversight | Monitor aftercare milestones | ☐ | |
| 10 | Treatment completion | View completed treatment record | ☐ | |
| 11 | Treatment completion | View completed treatment full lifecycle | ☐ | |

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

```
**Defect ID:** DEF-A-XXX
**Test Case:** TC-A-XXX, Step X
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
