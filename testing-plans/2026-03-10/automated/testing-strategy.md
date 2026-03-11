# Automated Testing Strategy — Hairline Platform

**Date:** 2026-03-10
**Decision:** Local (offline) testing environment
**Scope:** Provider Dashboard + Admin Dashboard — main treatment flow

---

## 1. Environment Decision: Local Testing

All automated tests run against the **local development environment**:

| Component | Local Setup | URL |
|-----------|------------|-----|
| Frontend | `npm run dev` | http://localhost:5173 |
| Backend | `docker-compose up -d` | http://localhost:80 |
| WebSocket | Docker (Reverb) | ws://localhost:8081 |
| Database | Docker (MySQL 8.0) | localhost:3307 |
| Test Database | Docker (MySQL 8.0) | `db_test` (PHPUnit) |
| Email | Docker (Mailpit) | http://localhost:8025 |
| phpMyAdmin | Docker | http://localhost:8080 |

**Why local:**

1. Playwright already configured against `localhost:5173` with auto-start dev server
2. Backend Docker provides identical environment to staging/production
3. Database can be freely reset/reseeded between test runs
4. PHPUnit uses a separate `db_test` database — already configured
5. Mailpit captures all emails locally for OTP verification testing
6. Full debugging access: logs, DB queries, breakpoints
7. No risk of interfering with other testers or shared environments

**Staging is used only for:** Final pre-release smoke tests and cross-environment validation.

---

## 2. Testing Pyramid

```
┌──────────────────────────────┐
│      E2E (Playwright)        │  Full user flows (sign-in → completion)
│      ~20-30 test specs       │  Slow but high confidence
├──────────────────────────────┤
│      API Integration         │  Backend endpoint tests (PHPUnit Feature)
│      (PHPUnit Feature)       │  Medium speed, tests business logic + API contracts
│      ~40-60 test cases       │
├──────────────────────────────┤
│      Unit Tests              │  Service/model logic (PHPUnit Unit)
│      (PHPUnit Unit)          │  Fast, tests calculations/validations
│      ~30-40 test cases       │
└──────────────────────────────┘
```

---

## 3. Frameworks (Already in Project)

| Layer | Framework | Config | Existing Coverage |
|-------|-----------|--------|-------------------|
| E2E | Playwright 1.54.2 | `playwright.config.ts` | 21 spec files (auth, login, dashboard, treatments) |
| API/Feature | PHPUnit 10.1 | `phpunit.xml` | Admin features, service unit tests |
| Code Style | Laravel Pint | Backend | N/A |
| Linting | ESLint | Frontend | Configured |

---

## 4. Auth State Configuration

Playwright uses pre-authenticated storage states to avoid re-login in every test:

| Auth State | Setup File | Storage State File | Credentials | Playwright Project |
|------------|-----------|-------------------|-------------|-------------------|
| Provider (Clinician) | `tests/auth.setup.ts` | `playwright/.auth/user.json` | `clinician1@hairline.app` / `password123` | `chromium` |
| Admin (Team) | `tests/team-auth.setup.ts` | `playwright/.auth/team-user.json` | `admin@example.com` / `password` | `team-chromium` |

Provider tests run in the `chromium` project. Admin tests run in the `team-chromium` project. Both can run in parallel.

---

## 5. Test Execution Commands

### Frontend (Playwright)

```bash
cd main/hairline-frontend

npx playwright test                                    # All tests
npx playwright test --project=chromium                 # Provider tests only
npx playwright test --project=team-chromium            # Admin tests only
npx playwright test --headed                           # See browser
npx playwright test --ui                               # Interactive UI mode
npx playwright test --reporter=html && npx playwright show-report  # HTML report
```

### Backend (PHPUnit)

```bash
cd main/hairline-backend
docker-compose exec php bash

php artisan test                          # All tests
php artisan test --testsuite=Feature      # Feature tests
php artisan test --testsuite=Unit         # Unit tests
php artisan test --coverage               # With coverage report
```

### Full Suite (Recommended Order)

```bash
# 1. Reset & seed database
docker-compose exec php bash -c "php artisan migrate:fresh && php artisan db:seed --class=FullSeeder"

# 2. Backend unit tests (fastest)
docker-compose exec php bash -c "php artisan test --testsuite=Unit"

# 3. Backend feature tests
docker-compose exec php bash -c "php artisan test --testsuite=Feature"

# 4. Frontend E2E tests (slowest)
cd main/hairline-frontend && npx playwright test
```

---

## 6. Test Data Seeding

### Seeder Modes

| Mode | Command | What It Creates | When to Use |
|------|---------|-----------------|-------------|
| Basic | `--class=BasicSeeder` | Essential data + 2 fixed providers | Quick smoke tests |
| Development | `--class=DevelopmentSeeder` | Basic + random providers/patients | Moderate testing |
| Full | `--class=FullSeeder` | Development + inquiries/quotes/treatments | Comprehensive testing |

### Pre-Seeded Test Accounts

| Account | Email | Password | Role | Provider |
|---------|-------|----------|------|----------|
| Provider 1 (Owner) | `provider1@hairline.app` | `password123` | Provider Owner | Hair Clinic Istanbul |
| Clinician 1 | `clinician1@hairline.app` | `password123` | Clinician | Hair Clinic Istanbul |
| Provider 2 (Owner) | `provider2@hairline.app` | `password123` | Provider Owner | Elite Hair Center |
| Admin Staff | `admin2@hairline.app` | `password123` | Admin Staff | Elite Hair Center |
| Admin User | `admin@example.com` | `password` | Hairline Team (Admin) | N/A |

### Targeted Seeders (Run After FullSeeder for Specific Stages)

```bash
# Financial / billing data
php artisan db:seed --class=FinancialDataSeeder
php artisan db:seed --class=ProviderBillingSeeder
php artisan db:seed --class=PaymentHistorySeeder

# Aftercare data
php artisan db:seed --class=AfterCareFullDataSeeder
php artisan db:seed --class=AftercareTemplatesSeeder

# Dashboard metrics
php artisan db:seed --class=HairlineDashboardSampleDataSeeder
```

---

## 7. Test Artifacts & Reports

| Artifact | Location |
|----------|----------|
| Playwright HTML report | `main/hairline-frontend/playwright-report/` |
| Screenshots (on failure) | `main/hairline-frontend/test-results/` |
| Traces (on retry) | `main/hairline-frontend/test-results/` |
| PHPUnit coverage | Generated with `--coverage` flag |

---

## 8. Testing Types & When to Use Each

Beyond standard test cases, the following specialized testing types are required across both dashboards. Each type catches a different class of bugs.

### 8.1 Smoke Tests (`@smoke`)

**What:** A small subset (~10-15 tests) that verifies "is the system alive and fundamentally working?" before running the full suite.

**When to run:** Before every full test run. Also useful as a quick check after deployments or environment setup.

**How to implement:**
- Tag selected tests with `@smoke` (PHPUnit group) or `test.describe('smoke', ...)` (Playwright)
- Choose one test per module that covers the most critical happy path
- Target: entire smoke suite completes in under 2 minutes

**Execution:**
```bash
# PHPUnit
php artisan test --group=smoke

# Playwright
npx playwright test --grep @smoke
```

**Selection criteria for smoke tests:**
- Provider: login, view inquiry list, create quote, view appointment, check-in, view aftercare
- Admin: login, dashboard metrics load, patient list loads, payment list loads, analytics loads

### 8.2 Parameterized Tests (`[PARAM]`)

**What:** One test definition, multiple input/output combinations. Catches calculation errors, boundary issues, and missed edge cases.

**When to use:** Any test involving calculations, validation rules, status transitions, time boundaries, or multi-input logic.

**How to implement:**
- PHPUnit: `@dataProvider` methods
- Playwright: `for` loops or `[...data].forEach()` within `test.describe`

**Already planned for:** price calculations, deposit %, installment plans, commission rates, password validation, inquiry/quote expiry boundaries, pagination, sort columns, role-based API access, currency display, status transitions, conversion rates.

### 8.3 Idempotency Tests

**What:** Call the same operation multiple times with the same data. Verify the system produces the correct result without corruption, duplication, or side effects.

**Why critical:** In a medical/payment platform, double-submissions (double payment, duplicate quote, duplicate check-in) can cause real financial and clinical harm.

**When to use:**
- Any POST/PUT endpoint that creates or modifies data
- Any UI action that submits a form or triggers a state change
- Payment processing endpoints (most critical)

**How to implement:**
- Call the endpoint/action twice with identical data
- Assert: either same successful result both times (for idempotent operations) OR rejection of the duplicate (for non-idempotent operations)
- Verify no duplicate records in database

### 8.4 Race Condition Tests

**What:** Simulate two users performing conflicting actions at the same time. Verify the system handles concurrency without data corruption.

**Why critical:** Multiple providers quoting the same inquiry, two admins changing the same setting, or concurrent payment submissions can corrupt data if not handled.

**When to use:**
- Multiple providers acting on the same inquiry
- Concurrent quote submissions
- Simultaneous payment processing
- Admin configuration changes during active operations

**How to implement:**
- PHPUnit: Use `Promise\all()` or run two requests in rapid succession within the same test
- Check that database constraints prevent duplicates
- Check that optimistic/pessimistic locking works
- Verify final state is consistent (no half-applied changes)

### 8.5 Data Consistency Tests

**What:** After a complete workflow, verify that ALL related records across ALL tables are consistent with each other.

**Why critical:** The treatment flow spans 6+ database tables (inquiry → quote → booking → payment → treatment → aftercare). If any record is out of sync, the UI shows contradictory information and business logic breaks.

**When to use:**
- After completing a full treatment flow (end-to-end)
- After status transitions
- After payment processing
- After aftercare activation

**How to implement:**
- Run a full flow via API
- Query each related table and assert consistency:
  - Inquiry status matches quote status
  - Quote amount matches payment amount
  - Treatment patient_id matches booking patient_id
  - Aftercare treatment_id references the correct treatment
  - Financial records sum correctly
  - Timeline entries exist for every state change

### 8.6 Regression Tests (`@regression`)

**What:** Tests specifically written to prevent a previously-found bug from returning.

**When to use:** Every time a bug is fixed, a new test case must be added and tagged `@regression`.

**How to implement:**
- Tag with `@regression` (PHPUnit group) or include in a `regression/` test folder
- The test must reproduce the exact conditions that caused the original bug
- Reference the original defect description in the test name or comment

**Execution:**
```bash
# Run regression suite after any code change
php artisan test --group=regression
npx playwright test --grep @regression
```

### Summary: Test Execution Order

```
1. Smoke tests          (~2 min)   — Is the system alive?
2. Unit tests           (~5 min)   — Are calculations correct?
3. Parameterized tests  (~5 min)   — Are all input combinations handled?
4. API integration      (~10 min)  — Do endpoints behave correctly?
5. Idempotency tests    (~3 min)   — Are double-submissions safe?
6. Race condition tests (~3 min)   — Is concurrency handled?
7. E2E tests            (~15 min)  — Do full user flows work?
8. Data consistency     (~5 min)   — Is cross-table data coherent?
9. Regression tests     (~5 min)   — Are old bugs still fixed?
```

---

## 9. Folder Structure

```
local-docs/testing-plans/2026-03-10/
├── automated/
│   ├── testing-strategy.md               ← This file
│   ├── provider-dashboard/
│   │   ├── test-requirements.md          ← Constitution, related docs, how to conduct
│   │   └── test-checklist-report.md      ← Detailed checklist + report template
│   └── admin-dashboard/
│       ├── test-requirements.md
│       └── test-checklist-report.md
└── manual/
    ├── provider-dashboard-manual-testing-plan.md
    └── admin-dashboard-manual-testing-plan.md
```
