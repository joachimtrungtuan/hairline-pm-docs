# Admin Dashboard — Automated Testing Plan

**Date:** 2026-03-09
**Scope:** Main treatment flow — admin oversight from sign-in through treatment completion
**Dashboard:** Admin/Hairline Team Dashboard (`profile_type: "hairline"`)
**Test Type:** Automated (Playwright E2E + PHPUnit API)
**Related FRs:** FR-001, FR-003, FR-004, FR-006, FR-007/007B, FR-010, FR-011, FR-016, FR-020

---

## Table of Contents

1. [Testing Strategy & Recommendations](#1-testing-strategy--recommendations)
2. [Environment Setup](#2-environment-setup)
3. [Test Data Seeding & Fixtures](#3-test-data-seeding--fixtures)
4. [Playwright E2E Test Specifications](#4-playwright-e2e-test-specifications)
5. [PHPUnit API Test Specifications](#5-phpunit-api-test-specifications)
6. [Test Execution Instructions](#6-test-execution-instructions)
7. [CI/CD Integration Notes](#7-cicd-integration-notes)

---

## 1. Testing Strategy & Recommendations

### Local vs Remote — Same Recommendation as Provider

**Use LOCAL environment for all automated tests.** See Provider automated testing plan for detailed rationale.

Summary: Playwright is already configured against `localhost:5173`, backend Docker provides full environment parity, `db_test` database isolates test runs, and Mailpit captures emails locally.

### Admin-Specific Testing Considerations

| Consideration | Impact | Approach |
|--------------|--------|----------|
| Admin sees **all** data platform-wide | Tests need seeded data across multiple providers/patients | Use `FullSeeder` for comprehensive data |
| Admin has oversight-only role (limited write) | Focus on read/view/filter tests over CRUD | More assertion-heavy tests |
| Admin manages billing/payments | Financial calculations must be precise | Include numeric precision assertions |
| Admin role isolation | Provider routes must be inaccessible | Include negative access tests |

### Existing Admin Auth Setup (Reuse)

The project already has `tests/team-auth.setup.ts` which logs in as `admin@example.com` / `password` and saves session to `playwright/.auth/team-user.json`.

Admin E2E tests run in the **`team-chromium`** Playwright project (depends on `team-setup`).

---

## 2. Environment Setup

### Prerequisites

Same Docker + frontend setup as Provider. Ensure all containers are running:

```bash
# 1. Start backend
cd main/hairline-backend && docker-compose up -d

# 2. Seed with full data (admin needs data across all entities)
docker-compose exec php bash -c "php artisan migrate:fresh --seed --seeder=FullSeeder"

# 3. Seed additional admin-specific data
docker-compose exec php bash -c "\
  php artisan db:seed --class=HairlineDashboardSampleDataSeeder && \
  php artisan db:seed --class=FinancialDataSeeder && \
  php artisan db:seed --class=ProviderBillingSeeder && \
  php artisan db:seed --class=PaymentHistorySeeder && \
  php artisan db:seed --class=AfterCareFullDataSeeder \
"

# 4. Start frontend
cd main/hairline-frontend && npm run dev
```

### Creating Multiple Admin/Team Accounts

```bash
# Inside backend container

# Seed role permissions (ensures admin roles exist)
php artisan db:seed --class=RolePermissionSeeder

# Seed support users (additional team members)
php artisan db:seed --class=SupportUserSeeder
```

### Admin Test Accounts Available After Seeding

| Account | Email | Password | Role |
|---------|-------|----------|------|
| Primary Admin | `admin@example.com` | `password` | Hairline Team (Admin) |
| Support Users | Created by `SupportUserSeeder` | `password` (default) | Hairline Team (Support) |

---

## 3. Test Data Seeding & Fixtures

### Comprehensive Seed Script for Admin Testing

Admin testing requires data across the entire platform. Use this seed script:

```bash
#!/bin/bash
# seed-admin-test-data.sh — Run inside backend container

echo "=== Resetting database ==="
php artisan migrate:fresh

echo "=== Base data ==="
php artisan db:seed --class=BasicSeeder

echo "=== Providers (multiple) ==="
php artisan db:seed --class=ProviderSeeder
php artisan db:seed --class=ProviderUserSeeder
php artisan db:seed --class=ProviderTeamMemberSeeder

echo "=== Patients ==="
php artisan db:seed --class=PatientSeeder

echo "=== Inquiries at various stages ==="
php artisan db:seed --class=InquirySampleDataSeeder

echo "=== Quotes at various stages ==="
php artisan db:seed --class=QuoteTestDataSeeder
php artisan db:seed --class=SubmittedQuotesSeeder
php artisan db:seed --class=CompleteQuoteSeeder

echo "=== Bookings & Payments ==="
php artisan db:seed --class=BookingDataSeeder
php artisan db:seed --class=PaymentSeeder
php artisan db:seed --class=PaymentHistorySeeder

echo "=== Treatments ==="
php artisan db:seed --class=TreatmentSeeder

echo "=== Aftercare ==="
php artisan db:seed --class=AftercareTemplatesSeeder
php artisan db:seed --class=AfterCareFullDataSeeder

echo "=== Financial / Billing ==="
php artisan db:seed --class=FinancialDataSeeder
php artisan db:seed --class=ProviderBillingSeeder

echo "=== Dashboard overview data ==="
php artisan db:seed --class=HairlineDashboardSampleDataSeeder

echo "=== Notifications ==="
php artisan db:seed --class=NotificationSeeder

echo "=== Admin data ready! ==="
```

### Admin Auth Fixture

The existing `tests/team-auth.setup.ts` handles admin authentication:

```typescript
// Already exists — tests/team-auth.setup.ts
setup('authenticate as team user', async ({ page }) => {
    await page.goto('/auth/hairline-team/login');
    await page.getByRole('textbox', { name: 'Username' }).fill('admin@example.com');
    await page.getByRole('textbox', { name: 'Password' }).fill('password');
    await page.getByRole('button', { name: 'Log in' }).click();
    await expect(page).toHaveURL('/');
    await expect(page.getByRole('button', { name: /Admin User/ })).toBeVisible();
    await page.context().storageState({ path: 'playwright/.auth/team-user.json' });
});
```

---

## 4. Playwright E2E Test Specifications

### Test File Organization

```md
tests/
├── team-auth.setup.ts                     # (existing) Admin auth setup
├── admin-treatment-flow/                  # NEW — Admin oversight flow tests
│   ├── admin-sign-in.spec.ts
│   ├── admin-dashboard-overview.spec.ts
│   ├── admin-provider-management.spec.ts
│   ├── admin-patient-management.spec.ts
│   ├── admin-inquiry-monitoring.spec.ts
│   ├── admin-quote-oversight.spec.ts
│   ├── admin-payment-administration.spec.ts
│   ├── admin-treatment-monitoring.spec.ts
│   ├── admin-aftercare-oversight.spec.ts
│   └── admin-treatment-completion-reporting.spec.ts
```

All specs should use the `team-chromium` project:

```typescript
// Example spec header for all admin tests
import { test, expect } from '@playwright/test';

// This spec runs in the team-chromium project which uses team-user.json auth state
test.describe('Admin - [Section Name]', () => {
    // tests here are already authenticated as admin
});
```

### Spec 1: admin-sign-in.spec.ts

**Purpose:** Verify admin authentication and role-based access.

| Test Case | Description | Acceptance Criteria |
|-----------|-------------|-------------------|
| `should display hairline team login` | Navigate to `/auth/hairline-team/login` | Login form visible with heading |
| `should login with valid admin credentials` | Enter `admin@example.com` / `password` | "Login successful", redirect to `/`, "Admin User" in header |
| `should reject invalid credentials` | Enter wrong password | Error message, stay on login page |
| `should show admin navigation sidebar` | After login, check sidebar | Admin-specific nav items (Overview, Patients, Settings, Billing) |
| `should not show provider-specific nav` | After login, check sidebar | No Inquiries, Appointments, Quotes (provider items) absent |
| `should logout successfully` | Click user menu → Logout | Redirected to `/auth` |
| `should block access to provider routes` | Navigate to provider-only URL | Redirected or 403/access denied |

### Spec 2: admin-dashboard-overview.spec.ts

**Purpose:** Verify admin dashboard loads with platform metrics.

| Test Case | Description | Acceptance Criteria |
|-----------|-------------|-------------------|
| `should load dashboard page` | Navigate to dashboard | Page loads within 3 seconds |
| `should display total providers metric` | Check metrics widget | Provider count shown, non-zero with seeded data |
| `should display total patients metric` | Check metrics widget | Patient count shown |
| `should display active inquiries count` | Check metrics widget | Inquiry count displayed |
| `should display active treatments count` | Check metrics widget | Treatment count displayed |
| `should display revenue summary` | Check financial widget | Revenue figure displayed |
| `should show notifications` | Click bell icon | Notifications dropdown opens with items |
| `should support notification infinite scroll` | Scroll notifications dropdown | More notifications load (FR-020) |

### Spec 3: admin-provider-management.spec.ts

**Purpose:** Verify admin can view and search providers.

| Test Case | Description | Acceptance Criteria |
|-----------|-------------|-------------------|
| `should display provider list` | Navigate to provider section | Provider list/table loads |
| `should search providers by name` | Enter search query | Results filter in real-time |
| `should view provider details` | Click a provider | Detail page: clinic info, team, credentials, performance |
| `should display provider performance metrics` | View provider analytics | Quote conversion rate, treatment count visible |
| `should have provider status controls` | View provider actions | Approve/suspend/flag options available |

### Spec 4: admin-patient-management.spec.ts

**Purpose:** Verify admin can view, search, and sort patient records.

| Test Case | Description | Acceptance Criteria |
|-----------|-------------|-------------------|
| `should display patient table` | Navigate to Patients | Patient table loads with data |
| `should search patients` | Enter patient name/ID | Results filter correctly |
| `should sort by name` | Click name column header | Rows reorder alphabetically |
| `should sort by date` | Click date column header | Rows reorder by date |
| `should sort by status` | Click status column header | Rows reorder by status |
| `should paginate patient list` | Navigate to page 2 | Next page of results loads |
| `should view patient detail` | Click a patient row | Detail page: medical history, inquiries, treatments, billing |
| `should view patient treatment history` | On detail page, check history | Treatment timeline visible |
| `should view patient billing records` | On detail page, check billing | Payment history accessible |

### Spec 5: admin-inquiry-monitoring.spec.ts

**Purpose:** Verify admin can monitor all inquiries platform-wide.

| Test Case | Description | Acceptance Criteria |
|-----------|-------------|-------------------|
| `should display all inquiries` | Navigate to inquiry monitoring | Inquiry list loads (all providers) |
| `should filter by status - New` | Select "New" filter | Only new inquiries shown |
| `should filter by status - Distributed` | Select "Distributed" filter | Only distributed inquiries shown |
| `should filter by status - Expired` | Select "Expired" filter | Only expired inquiries shown |
| `should view inquiry distribution details` | Click an inquiry | Shows which providers received it |
| `should verify distribution SLA` | Check timestamps | Distribution within 5 minutes of creation |
| `should flag a conversation` | Flag an inquiry conversation | Flag saved (FR-016) |

### Spec 6: admin-quote-oversight.spec.ts

**Purpose:** Verify admin can monitor quotes across the platform.

| Test Case | Description | Acceptance Criteria |
|-----------|-------------|-------------------|
| `should display all quotes` | Navigate to quote oversight | Quote list loads across all providers |
| `should filter by Draft status` | Apply filter | Only drafts shown |
| `should filter by Submitted status` | Apply filter | Only submitted quotes shown |
| `should filter by Accepted status` | Apply filter | Only accepted quotes shown |
| `should filter by Expired status` | Apply filter | Only expired quotes shown |
| `should view quote details` | Click a quote | Full details: treatment type, packages, pricing, appointment |
| `should display commission configuration` | Navigate to settings | Commission rate settings accessible |
| `should show conversion metrics` | Check analytics | Quote-to-booking conversion rate displayed |

### Spec 7: admin-payment-administration.spec.ts

**Purpose:** Verify admin can manage payments, deposits, and installments.

| Test Case | Description | Acceptance Criteria |
|-----------|-------------|-------------------|
| `should display payment records` | Navigate to billing | Payment list loads |
| `should show payment status indicators` | View list | Status: deposit/partial/full shown per record |
| `should view installment plan` | Click a patient with installments | Schedule visible (2-9 monthly, interest-free) |
| `should display multi-currency amounts` | View payments in different currencies | Currency codes display correctly |
| `should view payment transaction history` | Click a payment | Stripe transaction IDs, amounts, dates visible |
| `should view provider billing/payouts` | Navigate to provider billing | Provider earnings, commission deductions shown |
| `should access deposit configuration` | Navigate to admin settings | Deposit percentage (20-30%) configurable |

### Spec 8: admin-treatment-monitoring.spec.ts

**Purpose:** Verify admin can monitor active treatments.

| Test Case | Description | Acceptance Criteria |
|-----------|-------------|-------------------|
| `should display active treatments` | Navigate to treatments view | Treatment list loads |
| `should filter by Confirmed status` | Apply filter | Only confirmed treatments shown |
| `should filter by In Progress status` | Apply filter | Only in-progress treatments shown |
| `should filter by Aftercare status` | Apply filter | Only aftercare treatments shown |
| `should filter by Completed status` | Apply filter | Only completed treatments shown |
| `should view treatment details` | Click a treatment | Detail page: provider, patient, procedure docs |
| `should view treatment timeline` | Check timeline section | Chronological events displayed |
| `should view procedure documentation` | Check documentation | Photos, notes, medications viewable by admin |

### Spec 9: admin-aftercare-oversight.spec.ts

**Purpose:** Verify admin can monitor and manage aftercare cases.

| Test Case | Description | Acceptance Criteria |
|-----------|-------------|-------------------|
| `should display aftercare cases` | Navigate to aftercare administration | Aftercare case list loads |
| `should view aftercare plan` | Click a case | Plan: template, milestones, patient submissions |
| `should assign aftercare specialist` | Select specialist for a case | Specialist assigned, reflected in case detail |
| `should view milestone progress` | Check milestones | Completion status for each milestone |
| `should view patient scan photos` | Check submissions | Photos viewable with timestamps |
| `should view questionnaire responses` | Check submissions | Pain, sleep, compliance responses displayed |
| `should access aftercare messaging` | Click communication | Aftercare conversations accessible |

### Spec 10: admin-treatment-completion-reporting.spec.ts

**Purpose:** Verify admin can view completed treatments and platform reports.

| Test Case | Description | Acceptance Criteria |
|-----------|-------------|-------------------|
| `should display completed treatments` | Filter to completed | Completed treatments listed |
| `should view full treatment lifecycle` | Click completed treatment | Full timeline: inquiry → quote → booking → treatment → aftercare → completion |
| `should view outcome documentation` | Check final records | Final photos, notes, satisfaction data |
| `should display analytics dashboard` | Navigate to analytics | Platform analytics loads |
| `should show quote conversion rates` | Check analytics | Conversion metrics displayed (FR-014) |
| `should show provider performance rankings` | Check analytics | Provider comparison data |
| `should show revenue reports` | Check financial analytics | Revenue by treatment type, provider, period |
| `should export report data` | Click export button | CSV/PDF export downloads successfully |

---

## 5. PHPUnit API Test Specifications

### Test File Organization

```md
tests/
├── Feature/
│   └── AdminTreatmentFlow/
│       ├── AdminAuthTest.php
│       ├── AdminDashboardTest.php
│       ├── AdminProviderManagementTest.php
│       ├── AdminPatientManagementTest.php
│       ├── AdminInquiryMonitoringTest.php
│       ├── AdminQuoteOversightTest.php
│       ├── AdminPaymentTest.php
│       ├── AdminTreatmentMonitoringTest.php
│       ├── AdminAftercareTest.php
│       └── AdminReportingTest.php
└── Unit/
    └── AdminTreatmentFlow/
        ├── CommissionCalculationTest.php
        ├── PaymentSplitTest.php
        └── DepositCalculationTest.php
```

### API Tests Overview

#### AdminAuthTest.php

| Test Method | Endpoint | Expected |
|-------------|----------|----------|
| `test_admin_can_login` | `POST /api/login` | 200 + JWT token + `profile_type: "hairline"` |
| `test_admin_login_fails_wrong_password` | `POST /api/login` | 401 |
| `test_admin_cannot_access_provider_endpoints` | `GET /api/provider/inquiries` | 403 |
| `test_provider_cannot_access_admin_endpoints` | `GET /api/admin/patients` | 403 |

#### AdminDashboardTest.php

| Test Method | Endpoint | Expected |
|-------------|----------|----------|
| `test_admin_can_get_dashboard_metrics` | `GET /api/admin/dashboard` | 200 + metrics object |
| `test_dashboard_returns_provider_count` | `GET /api/admin/dashboard` | `providers_count >= 1` |
| `test_dashboard_returns_patient_count` | `GET /api/admin/dashboard` | `patients_count >= 0` |
| `test_dashboard_returns_revenue_summary` | `GET /api/admin/dashboard` | Revenue data present |

#### AdminProviderManagementTest.php

| Test Method | Endpoint | Expected |
|-------------|----------|----------|
| `test_admin_can_list_providers` | `GET /api/admin/providers` | 200 + paginated provider list |
| `test_admin_can_search_providers` | `GET /api/admin/providers?search=Istanbul` | Filtered results |
| `test_admin_can_view_provider_detail` | `GET /api/admin/providers/{id}` | 200 + full provider data |
| `test_admin_can_update_provider_status` | `PUT /api/admin/providers/{id}/status` | 200 + status updated |

#### AdminPatientManagementTest.php

| Test Method | Endpoint | Expected |
|-------------|----------|----------|
| `test_admin_can_list_patients` | `GET /api/admin/patients` | 200 + paginated patient list |
| `test_admin_can_search_patients` | `GET /api/admin/patients?search=John` | Filtered results |
| `test_admin_can_view_patient_detail` | `GET /api/admin/patients/{id}` | 200 + full patient data |
| `test_admin_can_view_patient_treatments` | `GET /api/admin/patients/{id}/treatments` | 200 + treatment list |
| `test_admin_can_view_patient_billing` | `GET /api/admin/patients/{id}/billing` | 200 + payment records |

#### AdminInquiryMonitoringTest.php

| Test Method | Endpoint | Expected |
|-------------|----------|----------|
| `test_admin_can_list_all_inquiries` | `GET /api/admin/inquiries` | 200 + all platform inquiries |
| `test_admin_can_filter_by_status` | `GET /api/admin/inquiries?status=new` | Filtered results |
| `test_admin_can_view_distribution_details` | `GET /api/admin/inquiries/{id}` | Shows provider assignments |
| `test_admin_can_flag_conversation` | `POST /api/admin/conversations/{id}/flag` | 200 + flag saved |

#### AdminPaymentTest.php

| Test Method | Endpoint | Expected |
|-------------|----------|----------|
| `test_admin_can_list_payments` | `GET /api/admin/payments` | 200 + payment list |
| `test_admin_can_view_payment_detail` | `GET /api/admin/payments/{id}` | 200 + Stripe transaction data |
| `test_admin_can_view_installment_plan` | `GET /api/admin/patients/{id}/installments` | 200 + installment schedule |
| `test_admin_can_configure_deposit` | `PUT /api/admin/settings/deposit` | 200 + deposit % updated |
| `test_admin_can_view_provider_billing` | `GET /api/admin/providers/{id}/billing` | 200 + earnings data |

#### AdminAftercareTest.php

| Test Method | Endpoint | Expected |
|-------------|----------|----------|
| `test_admin_can_list_aftercare_cases` | `GET /api/admin/aftercare` | 200 + aftercare list |
| `test_admin_can_assign_specialist` | `PUT /api/admin/aftercare/{id}/specialist` | 200 + specialist assigned |
| `test_admin_can_view_milestones` | `GET /api/admin/aftercare/{id}/milestones` | 200 + milestone list |
| `test_admin_can_view_patient_submissions` | `GET /api/admin/aftercare/{id}/submissions` | 200 + scan photos + questionnaires |

#### AdminReportingTest.php

| Test Method | Endpoint | Expected |
|-------------|----------|----------|
| `test_admin_can_get_analytics` | `GET /api/admin/analytics` | 200 + analytics data |
| `test_analytics_includes_conversion_rate` | `GET /api/admin/analytics` | `quote_conversion_rate` present |
| `test_analytics_includes_revenue_breakdown` | `GET /api/admin/analytics` | Revenue by type/provider/period |
| `test_admin_can_export_report` | `GET /api/admin/reports/export` | 200 + downloadable file |

### Unit Tests

#### CommissionCalculationTest.php

| Test Method | Description | Expected |
|-------------|-------------|----------|
| `test_commission_calculated_correctly` | Quote total × commission rate | Exact amount match |
| `test_commission_rounds_to_two_decimals` | Edge case pricing | No floating point errors |
| `test_zero_commission_returns_zero` | 0% rate | Commission = 0 |

#### PaymentSplitTest.php

| Test Method | Description | Expected |
|-------------|-------------|----------|
| `test_installment_split_even` | 6 months, divisible total | Equal monthly amounts |
| `test_installment_split_remainder` | 7 months, non-divisible | Remainder added to first payment |
| `test_installment_must_complete_30_days_before` | Schedule calculation | Last payment ≥ 30 days before procedure |

#### DepositCalculationTest.php

| Test Method | Description | Expected |
|-------------|-------------|----------|
| `test_deposit_at_20_percent` | Min deposit | Amount = total × 0.20 |
| `test_deposit_at_30_percent` | Max deposit | Amount = total × 0.30 |
| `test_deposit_configurable` | Change admin setting | New percentage applied to next booking |

---

## 6. Test Execution Instructions

### Running Admin E2E Tests

```bash
cd main/hairline-frontend

# Run ONLY admin/team tests (team-chromium project)
npx playwright test --project=team-chromium

# Run specific admin flow tests
npx playwright test tests/admin-treatment-flow/

# Run a specific admin spec
npx playwright test tests/admin-treatment-flow/admin-dashboard-overview.spec.ts

# Run in headed mode (see browser)
npx playwright test --project=team-chromium --headed

# Run with UI mode
npx playwright test --project=team-chromium --ui
```

### Running Admin API Tests

```bash
cd main/hairline-backend
docker-compose exec php bash

# Run admin-specific tests
php artisan test --filter=AdminTreatmentFlow

# Run specific test file
php artisan test tests/Feature/AdminTreatmentFlow/AdminPaymentTest.php

# Run unit tests for admin calculations
php artisan test tests/Unit/AdminTreatmentFlow/
```

### Full Admin Test Suite (Recommended Order)

```bash
# 1. Reset and seed database for admin testing
docker-compose exec php bash -c "\
  php artisan migrate:fresh && \
  php artisan db:seed --class=FullSeeder && \
  php artisan db:seed --class=HairlineDashboardSampleDataSeeder && \
  php artisan db:seed --class=FinancialDataSeeder && \
  php artisan db:seed --class=AfterCareFullDataSeeder
"

# 2. Run backend unit tests (fastest)
docker-compose exec php bash -c "php artisan test tests/Unit/AdminTreatmentFlow/"

# 3. Run backend feature/API tests
docker-compose exec php bash -c "php artisan test tests/Feature/AdminTreatmentFlow/"

# 4. Run Playwright E2E admin tests
cd main/hairline-frontend && npx playwright test --project=team-chromium
```

---

## 7. CI/CD Integration Notes

### Same CI Workflow as Provider

Admin tests should be added to the same GitHub Actions workflow. Add a separate job or extend the existing one:

```yaml
test-admin:
  runs-on: ubuntu-latest
  needs: [test-provider]  # Run after provider tests
  steps:
    - uses: actions/checkout@v4
    - name: Run admin API tests
      run: cd main/hairline-backend && php artisan test --filter=AdminTreatmentFlow
    - name: Run admin E2E tests
      run: cd main/hairline-frontend && npx playwright test --project=team-chromium
```

### Test Artifacts

Same artifact locations as Provider tests:

- **Playwright HTML report:** `main/hairline-frontend/playwright-report/`
- **Screenshots on failure:** `main/hairline-frontend/test-results/`
- **Traces on retry:** `main/hairline-frontend/test-results/`

### Parallel Execution Strategy

For faster CI runs, provider and admin E2E tests can run in parallel since they use separate Playwright projects and auth states:

```bash
# Run both projects in parallel
npx playwright test --project=chromium --project=team-chromium
```
