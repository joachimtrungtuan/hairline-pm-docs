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

## Scope & Deferred Items

**In scope:** Admin dashboard end-to-end oversight — sign-in, provider/patient management, and monitoring the full treatment lifecycle. Patient actions are simulated via seeded data or the mobile app as an entry tool.

**Deferred to future testing round:**
- **Messaging & Communication oversight (FR-012):** Only basic messaging visibility is verified. Comprehensive messaging testing (conversation flagging depth, real-time sync, file sharing) is deferred. Must be revisited when messaging is tested as a standalone module.
- **Admin Analytics & Reporting:** Dashboard metric accuracy is spot-checked but not exhaustively validated against DB counts.

## Table of Contents

1. [Test Environment Setup](#1-test-environment-setup)
2. [Test Data Seeding](#2-test-data-seeding)
3. [Test Scenarios](#3-test-scenarios)
   - [TC-A-001: Admin Team Access & Sign-In](#tc-a-001-admin-team-access--sign-in)
   - [TC-A-002: Admin Onboarding & Dashboard Overview](#tc-a-002-admin-onboarding--dashboard-overview)
   - [TC-A-003: Admin Creates Provider Account (FR-015 Wizard Flow)](#tc-a-003-admin-creates-provider-account-fr-015-wizard-flow)
   - [TC-A-003B: Managing Providers & Patients](#tc-a-003b-managing-providers--patients)
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

#### Super Admin RBAC Configuration (FR-031)

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 12 | Log in as Super Admin and navigate to System Settings > Access Control | RBAC configuration module loads (FR-031) | |
| 13 | View admin role permission matrix (Super Admin, Aftercare Specialist, Billing Staff, Support Staff) | All admin roles displayed with their permission toggles | |
| 14 | View provider role permission matrix (Owner, Manager, Clinical Staff, Billing Staff) | All provider roles displayed with configurable permissions | |
| 15 | Modify a permission for a provider role (e.g., toggle Clinical Staff access to billing) | Permission change saved; audit trail logged | |
| 16 | Log in as non-Super Admin (e.g., Aftercare Specialist) and attempt to access RBAC configuration | Access denied — only Super Admins can access this module | |
| 17 | Invite a new admin team member (enter email, assign role) | Invitation sent; pending status shown | |

#### Edge Cases

- [ ] Admin login with wrong password shows error
- [ ] Revoked admin session is no longer usable after access removal
- [ ] Admin cannot access provider-specific routes
- [ ] Provider cannot access admin-specific routes (role isolation)
- [ ] Non-Super Admin cannot access RBAC configuration (FR-031) — access blocked or module hidden
- [ ] Permission changes take effect immediately for affected users (or on next login)
- [ ] Admin role with reduced permissions only sees permitted modules in sidebar
- [ ] Session timeout behavior (if applicable)
- [ ] Audit trail records all permission changes with user, timestamp, and before/after values

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

#### Edge Cases to Verify

- [ ] Dashboard with no seeded data — widgets show zero counts or empty states gracefully (no broken UI)
- [ ] Notification dropdown with many items — infinite scroll works (FR-020)
- [ ] Click notification that links to a deleted/archived record — handles gracefully (404 page or redirect)
- [ ] Different admin roles see different sidebar modules based on RBAC (FR-031)

#### Acceptance Criteria

- [ ] Dashboard loads within 3 seconds
- [ ] All metric widgets display data (no empty/error states with seeded data)
- [ ] Navigation sidebar reflects admin role permissions (not provider role)
- [ ] Notifications dropdown shows with infinite scroll (FR-020)
- [ ] Real-time WebSocket updates functional (if Reverb running)

---

### TC-A-003: Admin Creates Provider Account (FR-015 Wizard Flow)

**Objective:** Verify admin can create a new provider account using the wizard-style interface, and the provider receives activation email and can set up their account.
**FR Reference:** FR-015 (Provider Management — Admin-Initiated)

#### Pre-conditions
- Logged in as admin
- Mailpit running for activation email

#### Provider Creation Wizard

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1 | Navigate to Provider Management section | Provider list loads with "Add New Provider" button visible (top-right) | |
| 2 | Click "Add New Provider" | Wizard-style creation form opens | |
| 3 | **Step 1 — Basic Information:** Enter profile picture/logo (optional), cover image (optional), full name, email, phone (with country code), bio/description (min 50 chars), seat limit (default 100) | All fields accept input; bio enforces 50-char minimum | |
| 4 | **Step 2 — Professional Details:** Enter specialty, medical license number, years of experience, languages spoken (at least 1), awards (optional) | Fields save; at least 1 language required | |
| 5 | **Step 3 — Clinic Information:** Enter clinic name, full address (street, city, state, postal code, country), clinic phone, operating hours | All address fields populated | |
| 6 | **Step 4 — Document Upload:** Upload medical license (required, PDF/image), board certifications (optional), malpractice insurance (optional) | Files upload with preview; documents are for record-keeping only | |
| 7 | **Step 5 — Commission Configuration:** Select commission model (Percentage or Flat Rate), enter value | Commission value saved | |
| 8 | **Step 6 — Review Summary:** Review all entered information | Summary accurately reflects all input from Steps 1-5 | |
| 9 | Click "Create Provider" | System validates required fields and creates provider with status = "Active" | |
| 10 | Check Mailpit for activation email | Provider receives welcome email with one-time password setup link (expires 24 hours) | |
| 11 | Open activation link from email | Password creation form displayed | |
| 12 | Set password (min 12 chars, uppercase/lowercase/digit/special) | Password validated and saved | |
| 13 | Log in as new provider on Provider Dashboard | Provider dashboard loads; onboarding/welcome screen prompts profile completion | |
| 14 | Verify new provider appears in admin's Provider Management list | Provider listed with "Active" status, correct details | |

#### Provider Status Management

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 15 | Suspend an active provider | Status changes to "Suspended" (yellow badge); provider notified | |
| 16 | Attempt to log in as the suspended provider | Access denied or restricted | |
| 17 | Reactivate the suspended provider | Status returns to "Active" (green badge) | |
| 18 | Deactivate a provider | Status changes to "Deactivated" (red badge); provider notified | |
| 19 | Toggle "Featured Provider" for an active provider | Featured badge (gold star) appears; provider visible in patient app featured list | |
| 20 | Resend activation email for a provider who hasn't set password yet | New activation email sent to Mailpit; previous link invalidated | |

#### Edge Cases to Verify

- [ ] **Create provider with missing required fields** (no name, no email, no clinic name, bio < 50 chars, no language) — wizard blocks progression with field-level validation
- [ ] **Create provider with duplicate email** — system rejects with clear error
- [ ] **Activation link expired (24+ hours)** — link rejected; provider can request resend from login page ("Didn't receive activation email?")
- [ ] **Resend activation email rate-limited** — max 3 resend requests per hour per email
- [ ] **Password too weak** — system rejects with specific feedback (which criteria failed)
- [ ] **Admin edits provider commission after creation** — change persists; affects future payout calculations
- [ ] **Document upload with invalid file type** — system rejects with clear error
- [ ] **Provider profile changes (via FR-032) sync to admin view** — changes made by provider in their dashboard reflect in admin's provider detail page

#### Acceptance Criteria

- [ ] Full 6-step wizard flow completes without errors
- [ ] All required field validations enforce correctly at each step
- [ ] Activation email arrives with working one-time link
- [ ] Provider can set password and log in after account creation
- [ ] Provider status transitions work: Active ↔ Suspended → Deactivated
- [ ] Featured provider toggle reflects in patient-facing listings
- [ ] Commission configuration (Percentage / Flat Rate) saves correctly
- [ ] Status badge colors correct: Active (green), Suspended (yellow), Deactivated (red)

---

### TC-A-003B: Managing Providers & Patients

**Objective:** Verify admin can view, search, and manage existing provider and patient records.
**FR Reference:** FR-015 (Provider Management), FR-016 (Patient Management)

#### Pre-conditions
- Multiple providers and patients seeded

#### Provider Management

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1 | Navigate to provider management section | Provider list loads (default: Active providers) | |
| 2 | Search for a provider by name, clinic name, or email | Search results filter correctly (case-insensitive) | |
| 3 | Filter by status (Active, Suspended, Deactivated) | Filters narrow results correctly | |
| 4 | Filter by Featured only | Only featured providers shown | |
| 5 | Sort provider table by name, created date, commission rate | Sorting works for each column | |
| 6 | Click on a provider to view details | Provider detail page: clinic info, team, credentials, commission, documents, status | |
| 7 | Verify provider detail shows documents status (Complete/Incomplete) | Documents status column accurate | |

#### Patient Management

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 8 | Navigate to Patients section | Patient list/table loads | |
| 9 | Search for a patient by name or ID | Search results filter correctly | |
| 10 | Sort patient table by various columns | Sorting works (name, date, status) | |
| 11 | Click on a patient to view details | Patient detail page: medical history, inquiries, treatments | |
| 12 | View patient's treatment history | Treatment timeline visible | |
| 13 | View patient billing/payment records | Payment history accessible | |

#### Edge Cases to Verify

- [ ] Search with partial text matches results correctly
- [ ] Provider list with 50+ entries — pagination works (50 per page per FR-015)
- [ ] Navigate away and back — filters/sorting persist
- [ ] Patient data shows correct masked/unmasked state depending on treatment stage

#### Acceptance Criteria

- [ ] Search is responsive and accurate across provider name, clinic, email, license number
- [ ] Pagination works for large datasets (50 per page)
- [ ] Table sorting works and persists
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
| 8 | Edit/override an inquiry detail (admin authority per FR-003) | Edit saved with audit trail | |
| 9 | Soft-delete an inquiry | Inquiry removed from active list; remains in archive with audit record | |

#### Edge Cases to Verify

- [ ] Inquiry cancelled by patient — all linked quotes show "Cancelled (Inquiry Cancelled)"; inquiry is read-only
- [ ] Inquiry distributed to maximum 10 providers — distribution count visible and capped
- [ ] Inquiry with critical medical alerts — alerts prominently displayed in admin view
- [ ] Admin reassigns inquiry to different providers — reassignment reflected with audit trail
- [ ] Inquiry soft-deleted by admin — disappears from active list but remains in audit/archive

#### Acceptance Criteria

- [ ] Admin sees all inquiries across all providers (platform-wide view)
- [ ] Status filters narrow results correctly
- [ ] Distribution SLA tracking visible (≤5 minutes)
- [ ] Expired inquiries handled gracefully
- [ ] Conversation flagging works (FR-016)
- [ ] Inquiry-to-quote linkage visible for cross-referencing

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

#### Edge Cases to Verify

- [ ] **Quote soft-deleted by provider:** Admin can see archived quote in audit trail and restore if needed
- [ ] **Provider withdrawal after acceptance:** Admin sees "provider-withdrawn" status; can resolve (re-route, reschedule, or cancel with refund)
- [ ] **All quotes for an inquiry expired with none accepted:** Admin can see expired state; patient may need to create new inquiry
- [ ] **Quote with cancelled inquiry:** Quote shows "Cancelled (Inquiry Cancelled)" status; admin can view but not reactivate
- [ ] **Admin inline edit of a quote (policy-bound):** Admin can edit within policy limits; changes audited

#### Acceptance Criteria

- [ ] Admin has visibility into all quotes platform-wide
- [ ] Commission rates apply correctly to quote pricing
- [ ] Quote status transitions are accurate (Draft/Submitted/Accepted/Expired/Withdrawn/Archived/Cancelled)
- [ ] Financial summaries match individual quote totals
- [ ] Admin can perform soft delete/restore with full audit trail
- [ ] Provider withdrawal cases visible and resolvable

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

#### Edge Cases to Verify

- [ ] **Payment failure with retry:** Admin sees payment failure record and retry attempts (exponential backoff per FR-007)
- [ ] **48-hour slot hold after failed payment:** Admin can see held slot status; slot auto-releases after 48 hours
- [ ] **Patient cancels during 48-hour slot hold:** Slot released immediately; no payment collected; admin can verify
- [ ] **Refund processing:** Admin processes refund per cancellation policy; refund status trackable
- [ ] **Installment completion enforcement (≥30 days before procedure):** System enforces the rule; admin can verify
- [ ] **Multi-currency display consistency:** Same booking shows correct currency throughout all admin views

#### Acceptance Criteria

- [ ] All payment records visible to admin
- [ ] Deposit percentage configurable in admin settings (default 20-30% range, via FR-029)
- [ ] Installment plans calculate correctly (2-9 monthly, interest-free per FR-007B)
- [ ] Multi-currency amounts display correctly
- [ ] Payment history shows complete audit trail
- [ ] Provider billing/commission calculations are accurate
- [ ] Refund processing workflow functional

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
| 7 | View payment status on treatment detail (outstanding balance / split pay) | Payment status visible for operational follow-up (FR-010) | |
| 8 | Check real-time status updates | Treatment status changes reflected without page refresh | |

#### Edge Cases to Verify

- [ ] **Admin edits an active treatment record:** Day statuses, notes, end-of-treatment fields editable by admin (per FR-010)
- [ ] **Admin manually triggers status transition:** Admin can override treatment status if needed
- [ ] **No-show case escalated to admin:** Admin receives notification with reason; can handle status transition, deposit retention, and rebooking manually
- [ ] **Medical postponement escalated to admin:** Admin transitions case to "Postponed" (admin-managed label); initiates rescheduling with no financial penalty
- [ ] **Treatment interrupted — admin intervention:** Admin handles case closure, partial documentation, financial reconciliation
- [ ] **Real-time treatment progress:** Admin sees current day and day status for all active treatments without page refresh

#### Acceptance Criteria

- [ ] Admin has read AND edit access to all treatment records (per FR-010)
- [ ] Treatment status transitions visible in timeline
- [ ] Day-by-day status and progress visible for active treatments
- [ ] Procedure documentation (photos, notes) viewable
- [ ] Admin can flag, annotate, and edit treatments
- [ ] Cancel/Close case escalations from providers visible with reason and notes
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

#### Edge Cases to Verify

- [ ] **Admin reassigns aftercare case to different specialist:** Reassignment reflected; new specialist notified
- [ ] **Aftercare escalation from provider:** Admin receives escalation notification and can intervene
- [ ] **Standalone aftercare request (external clinic patient):** Admin can intake, assign, and configure standalone aftercare case
- [ ] **Aftercare template management:** Admin can create/edit/delete milestone templates, questionnaire templates, and educational resources
- [ ] **Overdue patient milestone:** Admin sees overdue indicator; can send reminder or flag case

#### Acceptance Criteria

- [ ] Admin can view all aftercare cases platform-wide
- [ ] Aftercare specialist assignment works
- [ ] Patient milestone tracking accurate
- [ ] Scan photo set comparisons available (V1: 2D multi-view)
- [ ] Questionnaire responses render correctly
- [ ] Aftercare pricing configurable per template per currency (Fixed Price, Monthly Subscription, or Both per FR-011)
- [ ] Template management (create/edit) functional

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

#### Edge Cases to Verify

- [ ] **Completed treatment with partial aftercare (some milestones incomplete):** Admin can see which milestones were skipped or incomplete
- [ ] **Completed treatment where provider withdrawal occurred mid-process:** Full audit trail shows the intervention history
- [ ] **Admin attempts to edit a completed treatment:** System blocks or requires explicit unlock with audit logging
- [ ] **Cross-reference consistency:** Inquiry HPID → Quote → Booking → Payment → Treatment → Aftercare all linked with matching IDs and amounts

#### Acceptance Criteria

- [ ] Completed treatments show full lifecycle history
- [ ] Treatment outcome documentation (photos, notes) viewable
- [ ] All linked records (inquiry → quote → booking → payment → aftercare) are consistent and cross-referenced
- [ ] Completed treatments are appropriately locked from accidental edits
- [ ] Full audit trail preserved across all stages

---

## 4. End-to-End Admin Oversight Checklist

Admin parallel verification of the treatment flow (performed alongside provider flow):

| # | Stage | Admin Action | Status | Notes |
|---|-------|-------------|--------|-------|
| 1 | Admin team access | Log in as active Hairline Team member | ☐ | |
| 1b | RBAC configuration | Super Admin verifies role permissions (FR-031) | ☐ | TC-A-001 |
| 2 | Dashboard overview | Verify platform metrics | ☐ | |
| 2b | Provider creation | Create new provider via 6-step wizard; verify activation email | ☐ | TC-A-003 |
| 3 | Provider management | View/search/filter providers and patients | ☐ | TC-A-003B |
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
