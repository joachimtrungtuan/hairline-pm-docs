# Provider Dashboard — Automated Testing Plan

**Date:** 2026-03-09
**Scope:** Main treatment flow — from sign-in through treatment completion
**Dashboard:** Provider Dashboard (`profile_type: "provider"`)
**Test Type:** Automated (Playwright E2E + PHPUnit API)
**Related FRs:** FR-001, FR-004, FR-009, FR-010, FR-011, FR-012, FR-014

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

### Local vs Remote Testing — Recommendation

| Aspect | Local Testing | Remote/Staging Testing |
|--------|--------------|----------------------|
| **Speed** | Fast (no network latency) | Slower (network overhead) |
| **Data control** | Full control (seed/reset freely) | Shared data, risk of conflicts |
| **Isolation** | Complete isolation | May be affected by other testers |
| **Backend access** | Docker containers, can exec into PHP | Limited to API endpoints only |
| **WebSocket** | Local Reverb on port 8081 | Requires WSS via `backend.hairline.app:443` |
| **Email testing** | Mailpit captures all emails locally | Real email delivery or staging SMTP |
| **Database reset** | `migrate:fresh --seed` anytime | Cannot reset staging DB freely |
| **Debugging** | Full logs, DB queries, breakpoints | Limited to API responses |

**Recommendation: Use LOCAL environment for automated testing.**

Reasons:

1. Your project already has Playwright configured against `localhost:5173` with auto-start dev server
2. Backend Docker provides identical environment to staging/production
3. You can freely seed/reset data between test runs without affecting other users
4. PHPUnit tests use a separate `db_test` database — already configured in Docker
5. Mailpit captures emails locally for OTP verification testing

**Use staging only for**: Final pre-release smoke tests and cross-environment validation.

### Testing Pyramid for This Flow

```md
┌─────────────────────────┐
│   E2E (Playwright)      │  ← Full user flows (sign-in → completion)
│   ~15-20 test specs     │    Slow but high confidence
├─────────────────────────┤
│   API Integration       │  ← Backend endpoint tests (PHPUnit Feature)
│   (PHPUnit Feature)     │    Medium speed, tests business logic
│   ~30-40 test cases     │
├─────────────────────────┤
│   Unit Tests            │  ← Service/model logic (PHPUnit Unit)
│   (PHPUnit Unit)        │    Fast, tests calculations/validations
│   ~20-30 test cases     │
└─────────────────────────┘
```

### Framework Choices (Already in Project)

| Layer | Framework | Config File | Existing Tests |
|-------|-----------|------------|----------------|
| E2E | **Playwright 1.54.2** | `playwright.config.ts` | 21 spec files |
| API/Feature | **PHPUnit 10.1** | `phpunit.xml` | Feature + Unit tests |
| Code Style | **Laravel Pint** | `pint.json` | N/A |

### Existing Playwright Auth Setup (Reuse)

Your project already has two auth setup files — reuse them:

| Auth State | Setup File | Storage State | Credentials |
|------------|-----------|---------------|-------------|
| Provider (Clinician) | `tests/auth.setup.ts` | `playwright/.auth/user.json` | `clinician1@hairline.app` / `password123` |
| Admin (Team) | `tests/team-auth.setup.ts` | `playwright/.auth/team-user.json` | `admin@example.com` / `password` |

Provider tests run in the `chromium` project (depends on `setup`).
Team tests run in the `team-chromium` project (depends on `team-setup`).

---

## 2. Environment Setup

### Prerequisites

```bash
# 1. Start backend services
cd main/hairline-backend
docker-compose up -d

# 2. Verify all containers are running
docker-compose ps
# Expected: php, nginx, mysql, reverb, mailpit — all "Up"

# 3. Run database migrations and seed
docker-compose exec php bash -c "php artisan migrate:fresh --seed --seeder=FullSeeder"

# 4. Install frontend dependencies (if not done)
cd main/hairline-frontend
npm install

# 5. Install Playwright browsers (first time only)
npx playwright install chromium

# 6. Verify dev server starts
npm run dev
# Should be accessible at http://localhost:5173
```

### Environment Variables

Ensure `main/hairline-frontend/.env` (or `.env.development`) contains:

```env
VITE_MAIN_URL=http://localhost:80
VITE_API_URL=http://localhost:80/api
VITE_WS_HOST=localhost
VITE_WS_PORT=8081
VITE_WSS_PORT=8081
VITE_WS_FORCE_TLS=false
VITE_WS_ENCRYPTED=false
VITE_PUSHER_APP_KEY=<your-key>
VITE_PUSHER_APP_CLUSTER=mt1
```

---

## 3. Test Data Seeding & Fixtures

### Database Reset Script (Run Before Full Test Suite)

Create or use the following script to prepare a clean test database:

```bash
#!/bin/bash
# reset-test-db.sh — Run inside backend container

echo "Resetting database..."
php artisan migrate:fresh

echo "Seeding base data..."
php artisan db:seed --class=BasicSeeder

echo "Seeding inquiry/quote data..."
php artisan db:seed --class=InquirySampleDataSeeder
php artisan db:seed --class=QuoteTestDataSeeder

echo "Seeding booking/treatment data..."
php artisan db:seed --class=BookingDataSeeder
php artisan db:seed --class=TreatmentSeeder

echo "Seeding aftercare data..."
php artisan db:seed --class=AftercareTemplatesSeeder
php artisan db:seed --class=AfterCareFullDataSeeder

echo "Seeding dashboard data..."
php artisan db:seed --class=HairlineDashboardSampleDataSeeder

echo "Database ready for testing!"
```

### Provider Auth Fixture

The existing `tests/auth.setup.ts` handles provider authentication. It logs in as `clinician1@hairline.app` and saves the session to `playwright/.auth/user.json`.

For additional provider accounts, create a new setup file:

```typescript
// tests/provider-owner-auth.setup.ts
import { test as setup, expect } from '@playwright/test';

setup.use({ headless: true });

const authFile = 'playwright/.auth/provider-owner.json';

setup('authenticate as provider owner', async ({ page }) => {
    await page.goto('/auth/provider/login');
    await page.getByRole('textbox', { name: 'Username' }).fill('provider1@hairline.app');
    await page.getByRole('textbox', { name: 'Password' }).fill('password123');
    await page.getByRole('button', { name: 'Log in' }).click();
    await expect(page).toHaveURL('/');
    await expect(page.getByText('Login successful')).toBeVisible();
    await page.context().storageState({ path: authFile });
});
```

---

## 4. Playwright E2E Test Specifications

### Test File Organization

```md
tests/
├── auth.setup.ts                          # (existing) Provider clinician auth
├── team-auth.setup.ts                     # (existing) Admin auth
├── provider-owner-auth.setup.ts           # NEW — Provider owner auth
├── treatment-flow/                        # NEW — Treatment flow tests
│   ├── provider-sign-in.spec.ts
│   ├── provider-onboarding.spec.ts
│   ├── provider-inquiry-review.spec.ts
│   ├── provider-quote-creation.spec.ts
│   ├── provider-appointment.spec.ts
│   ├── provider-treatment-execution.spec.ts
│   ├── provider-aftercare.spec.ts
│   └── provider-treatment-completion.spec.ts
```

### Spec 1: provider-sign-in.spec.ts

**Purpose:** Verify provider authentication flows.

| Test Case | Description | Acceptance Criteria |
|-----------|-------------|-------------------|
| `should display role selection page` | Navigate to `/auth`, verify both login links visible | Both "Log in for Provider" and "Log in for Hairline Team" links present |
| `should navigate to provider login` | Click "Log in for Provider" | URL is `/auth/provider/login`, Login heading visible |
| `should login with valid provider credentials` | Enter `provider1@hairline.app` / `password123`, submit | "Login successful" toast, redirect to `/`, provider name in header |
| `should login with valid clinician credentials` | Enter `clinician1@hairline.app` / `password123`, submit | "Login successful" toast, redirect to `/`, "Dr. Ahmed Hassan" in header |
| `should reject invalid credentials` | Enter wrong password, submit | Error message shown, stay on login page |
| `should navigate to registration page` | Click "Register now!" link | Registration form displayed |
| `should navigate to forgot password` | Click "Forgot password" link | Password reset page displayed |
| `should logout successfully` | After login, click user menu → Logout | Redirected to `/auth`, session cleared |
| `should persist session on refresh` | After login, refresh page | Still logged in, dashboard visible |

### Spec 2: provider-onboarding.spec.ts

**Purpose:** Verify provider profile setup and team management.

| Test Case | Description | Acceptance Criteria |
|-----------|-------------|-------------------|
| `should load settings page` | Navigate to Settings | Settings page with sections loads |
| `should update clinic information` | Edit clinic name, description, save | Changes persist on page refresh |
| `should upload clinic images` | Upload logo/gallery images | Images display in preview, saved to profile |
| `should configure treatment types` | Toggle FUE/FUT/DHI | Treatment types saved |
| `should manage team members` | Navigate to Team page | Team list shows current members with roles |
| `should invite new team member` | Fill invite form, submit | Invitation sent, pending status shown |

### Spec 3: provider-inquiry-review.spec.ts

**Purpose:** Verify provider can view and review patient inquiries.

| Test Case | Description | Acceptance Criteria |
|-----------|-------------|-------------------|
| `should display inquiry list` | Navigate to Inquiries | Inquiry cards load with HPID, treatment type |
| `should mask patient identity` | View inquiry details | No patient full name visible, anonymized ID shown |
| `should display medical alerts` | View inquiry with medical history | Color-coded alerts (red/yellow/green) render |
| `should show head scan photos` | View inquiry detail with scans | Photos load, viewable |
| `should show expiry information` | View inquiry | Expiry timer/date visible (72h from distribution) |
| `should prevent quoting on expired inquiry` | Navigate to expired inquiry | Quote creation button disabled or hidden |

### Spec 4: provider-quote-creation.spec.ts

**Purpose:** Verify quote creation, package configuration, and submission.

| Test Case | Description | Acceptance Criteria |
|-----------|-------------|-------------------|
| `should open quote creation form` | Click "Create Quote" from inquiry | Quote form loads with treatment type selector |
| `should select treatment type` | Select FUE | Treatment type selected and displayed |
| `should set graft count` | Enter graft count (e.g., 3000) | Numeric value accepted |
| `should set base price` | Enter treatment price | Price field accepts amount |
| `should add optional packages` | Add hotel, transport, PRP | Packages added, each with pricing |
| `should calculate total correctly` | Base + packages | Total auto-calculates and matches sum |
| `should remove package` | Remove a package | Package removed, total recalculates |
| `should set appointment slots` | Select date/time | Calendar/picker allows selection |
| `should submit quote` | Submit completed quote | Status changes to "Submitted", toast confirmation |
| `should show quote in quotes list` | Navigate to Quotes | Submitted quote visible with correct status |
| `should validate required fields` | Submit without treatment type | Validation error shown |
| `should save as draft` | Save without submitting | Draft quote saved, editable later |

### Spec 5: provider-appointment.spec.ts

**Purpose:** Verify appointment display after quote acceptance.

| Test Case | Description | Acceptance Criteria |
|-----------|-------------|-------------------|
| `should display confirmed appointments` | Navigate to Appointments | Confirmed appointments listed |
| `should show unmasked patient details` | View confirmed appointment | Patient full name and contact visible |
| `should display payment status` | View appointment details | Deposit/payment status indicator shown |
| `should show appointment in calendar` | View calendar view | Appointment blocked on calendar |
| `should enable patient messaging` | Click message/chat | Chat interface opens with patient |

### Spec 6: provider-treatment-execution.spec.ts

**Purpose:** Verify treatment check-in, documentation, and procedure completion.

| Test Case | Description | Acceptance Criteria |
|-----------|-------------|-------------------|
| `should initiate patient check-in` | Click check-in on confirmed appointment | Check-in flow starts |
| `should validate payment before check-in` | Attempt check-in | Payment status validated (blocks if incomplete) |
| `should complete check-in` | Complete check-in steps | Status changes to "In Progress" |
| `should document clinician assignment` | Assign clinician to procedure | Clinician name recorded |
| `should record graft count` | Enter actual graft count | Graft count saved |
| `should add clinical notes` | Enter procedure notes | Notes saved to record |
| `should upload procedure photos` | Upload before/during/after photos | Photos upload, display in treatment record |
| `should add medications` | Add post-op medication prescription | Medications saved |
| `should complete procedure` | Mark procedure as complete | Status transitions from "In Progress" |

### Spec 7: provider-aftercare.spec.ts

**Purpose:** Verify aftercare plan setup and monitoring.

| Test Case | Description | Acceptance Criteria |
|-----------|-------------|-------------------|
| `should load aftercare section` | Navigate to AfterCare | Aftercare page loads |
| `should select aftercare template` | Choose template from list | Template selected, milestones previewed |
| `should customize instructions` | Edit template content | Customizations saved |
| `should set milestone schedule` | Configure milestones (Day 1, Week 1, Month 1, etc.) | Milestones created with calculated dates |
| `should activate aftercare plan` | Activate the plan | Status changes to "Aftercare" |
| `should display aftercare progress` | View aftercare dashboard | Patient submissions, milestones visible |

### Spec 8: provider-treatment-completion.spec.ts

**Purpose:** Verify treatment can be marked as complete.

| Test Case | Description | Acceptance Criteria |
|-----------|-------------|-------------------|
| `should display treatment with completed milestones` | View aftercare progress | All milestones show completion |
| `should mark treatment as completed` | Click "Complete Treatment" | Status changes to "Completed" |
| `should show in completed treatments list` | Navigate to treatment history | Completed treatment visible |
| `should update analytics` | Check performance metrics | Metrics reflect new completion |

---

## 5. PHPUnit API Test Specifications

### Test File Organization

```md
tests/
├── Feature/
│   └── TreatmentFlow/
│       ├── ProviderAuthTest.php
│       ├── ProviderProfileTest.php
│       ├── InquiryReviewTest.php
│       ├── QuoteManagementTest.php
│       ├── AppointmentTest.php
│       ├── TreatmentExecutionTest.php
│       ├── AftercareTest.php
│       └── TreatmentCompletionTest.php
└── Unit/
    └── TreatmentFlow/
        ├── QuotePriceCalculationTest.php
        ├── InquiryExpiryTest.php
        └── MilestoneScheduleTest.php
```

### API Tests Overview

#### ProviderAuthTest.php

| Test Method | Endpoint | Expected |
|-------------|----------|----------|
| `test_provider_can_login` | `POST /api/login` | 200 + JWT token |
| `test_login_fails_with_wrong_password` | `POST /api/login` | 401 |
| `test_provider_can_register` | `POST /api/register` | 201 + user created |
| `test_token_refresh` | `POST /api/token/refresh` | 200 + new token |
| `test_provider_can_logout` | `POST /api/logout` | 200 + token revoked |

#### InquiryReviewTest.php

| Test Method | Endpoint | Expected |
|-------------|----------|----------|
| `test_provider_can_list_inquiries` | `GET /api/provider/inquiries` | 200 + inquiry list |
| `test_inquiry_masks_patient_identity` | `GET /api/provider/inquiries/{id}` | Patient name is null/masked |
| `test_expired_inquiry_not_quotable` | `POST /api/provider/inquiries/{id}/quote` | 422 or 403 |
| `test_inquiry_includes_medical_data` | `GET /api/provider/inquiries/{id}` | Medical history + scan photos |

#### QuoteManagementTest.php

| Test Method | Endpoint | Expected |
|-------------|----------|----------|
| `test_provider_can_create_quote` | `POST /api/provider/quotes` | 201 + quote created |
| `test_quote_requires_treatment_type` | `POST /api/provider/quotes` (no type) | 422 validation error |
| `test_quote_calculates_total_correctly` | `POST /api/provider/quotes` | Total = base + sum(packages) |
| `test_provider_can_add_packages` | `POST /api/provider/quotes/{id}/packages` | 200 + package added |
| `test_quote_submission` | `PUT /api/provider/quotes/{id}/submit` | 200 + status "Submitted" |
| `test_cannot_submit_after_72h` | `PUT /api/provider/quotes/{id}/submit` (late) | 422 |

#### TreatmentExecutionTest.php

| Test Method | Endpoint | Expected |
|-------------|----------|----------|
| `test_provider_can_check_in_patient` | `POST /api/provider/treatments/{id}/check-in` | 200 + status "In Progress" |
| `test_check_in_blocked_without_payment` | `POST /api/provider/treatments/{id}/check-in` | 422 |
| `test_provider_can_document_procedure` | `PUT /api/provider/treatments/{id}` | 200 + data saved |
| `test_provider_can_upload_procedure_photos` | `POST /api/provider/treatments/{id}/photos` | 201 + photo stored |
| `test_provider_can_complete_procedure` | `PUT /api/provider/treatments/{id}/complete` | 200 + status updated |

#### AftercareTest.php

| Test Method | Endpoint | Expected |
|-------------|----------|----------|
| `test_provider_can_select_aftercare_template` | `POST /api/provider/aftercare` | 201 + plan created |
| `test_milestones_created_from_template` | `GET /api/provider/aftercare/{id}/milestones` | Milestones list populated |
| `test_provider_can_view_patient_submissions` | `GET /api/provider/aftercare/{id}/submissions` | Patient scans + questionnaires |
| `test_aftercare_activation` | `PUT /api/provider/aftercare/{id}/activate` | 200 + status "Aftercare" |

#### TreatmentCompletionTest.php

| Test Method | Endpoint | Expected |
|-------------|----------|----------|
| `test_provider_can_complete_treatment` | `PUT /api/provider/treatments/{id}/finish` | 200 + status "Completed" |
| `test_completed_treatment_in_history` | `GET /api/provider/treatments?status=completed` | Treatment in results |

---

## 6. Test Execution Instructions

### Running Playwright E2E Tests

```bash
cd main/hairline-frontend

# Run ALL tests (auto-starts dev server)
npx playwright test

# Run only provider treatment flow tests
npx playwright test tests/treatment-flow/

# Run a specific spec
npx playwright test tests/treatment-flow/provider-sign-in.spec.ts

# Run in headed mode (see browser)
npx playwright test --headed tests/treatment-flow/

# Run with UI mode (interactive debugging)
npx playwright test --ui

# Run and generate HTML report
npx playwright test --reporter=html
npx playwright show-report

# Run only the "chromium" project (provider tests)
npx playwright test --project=chromium
```

### Running PHPUnit API Tests

```bash
cd main/hairline-backend

# Run inside Docker container
docker-compose exec php bash

# Run ALL tests
php artisan test

# Run only treatment flow tests
php artisan test --filter=TreatmentFlow

# Run a specific test file
php artisan test tests/Feature/TreatmentFlow/QuoteManagementTest.php

# Run with coverage report
php artisan test --coverage

# Run specific test suites
php artisan test --testsuite=Feature
php artisan test --testsuite=Unit
```

### Full Test Suite (Recommended Order)

```bash
# 1. Reset database
docker-compose exec php bash -c "php artisan migrate:fresh && php artisan db:seed --class=FullSeeder"

# 2. Run backend unit tests first (fastest)
docker-compose exec php bash -c "php artisan test --testsuite=Unit"

# 3. Run backend feature/API tests
docker-compose exec php bash -c "php artisan test --testsuite=Feature"

# 4. Run Playwright E2E tests (slowest, depends on backend)
cd main/hairline-frontend && npx playwright test
```

---

## 7. CI/CD Integration Notes

### GitHub Actions (Existing Workflow)

The frontend already has `.github/workflows/publish.yml`. To add test execution:

```yaml
# Suggested addition to CI workflow
test:
  runs-on: ubuntu-latest
  services:
    mysql:
      image: mysql:8.0
      env:
        MYSQL_DATABASE: db_test
        MYSQL_ROOT_PASSWORD: root
      ports:
        - 3306:3306
  steps:
    - uses: actions/checkout@v4

    # Backend tests
    - name: Setup PHP
      uses: shivammathur/setup-php@v2
      with:
        php-version: '8.3'
    - name: Install backend dependencies
      run: cd main/hairline-backend && composer install
    - name: Run PHPUnit
      run: cd main/hairline-backend && php artisan test

    # Frontend E2E tests
    - name: Setup Node
      uses: actions/setup-node@v4
      with:
        node-version: '20'
    - name: Install frontend dependencies
      run: cd main/hairline-frontend && npm ci
    - name: Install Playwright
      run: cd main/hairline-frontend && npx playwright install --with-deps chromium
    - name: Run Playwright
      run: cd main/hairline-frontend && npx playwright test
```

### Test Artifacts

- **Playwright HTML report:** `main/hairline-frontend/playwright-report/`
- **Playwright screenshots (on failure):** `main/hairline-frontend/test-results/`
- **Playwright traces:** `main/hairline-frontend/test-results/` (on first retry)
- **PHPUnit coverage:** Generated with `--coverage` flag
