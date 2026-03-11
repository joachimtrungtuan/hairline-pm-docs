# Provider Dashboard — Automated Test Requirements

**Date:** 2026-03-10
**Dashboard:** Provider Dashboard (`profile_type: "provider"`)
**Scope:** Main treatment flow — sign-in through treatment completion

---

## 1. Purpose

This document defines the requirements, rules, and reference materials for writing and running automated tests against the Provider Dashboard. The developer writing test scripts must read this document fully before starting.

---

## 2. Related Documents

### Functional Requirements (Source of Truth)

All test cases trace back to these FRs. When a test case references an FR, the developer must read the relevant section to understand the business rule being verified.

| FR | Title | Path | Relevant Sections |
|----|-------|------|-------------------|
| FR-009 | Provider Team & Role Management | `local-docs/project-requirements/functional-requirements/fr009-provider-team-roles/prd.md` | Team member invite acceptance, account creation from invitation, login, password reset, role-based access |
| FR-026 | App Settings & Security | `local-docs/project-requirements/system-prd.md` | Password policy consumed by FR-009 account setup and reset flows |
| FR-003 | Inquiry Submission & Distribution | Same directory | Inquiry distribution (5 min SLA), 72h expiry, patient masking |
| FR-004 | Quote Submission & Management | Same directory | Quote CRUD, packages, pricing, 48h quote expiry, 72h submission window |
| FR-006 | Booking & Scheduling | Same directory | Booking confirmation, table list view, deposit validation |
| FR-007/007B | Payment & Installments | Same directory | Stripe, deposit %, installment plans, 30-day completion rule |
| FR-010 | Treatment Execution & Documentation | Same directory | Check-in, payment validation, procedure docs, photo uploads |
| FR-011 | Aftercare & Recovery Management | Same directory | Templates, milestones, scans, questionnaires, progress tracking |
| FR-032 | Provider Dashboard Settings | `local-docs/project-requirements/system-prd.md` | Clinic profile, banking details, notification preferences |
| FR-020 | Notifications & Alerts | Same directory | Dropdown, infinite scroll, real-time delivery |

### System Documents

| Document | Path | Relevance |
|----------|------|-----------|
| System PRD | `local-docs/project-requirements/system-prd.md` | Overall system behavior and business rules |
| Technical Spec | `local-docs/project-requirements/system-technical-spec.md` | API contracts, data formats, status codes |
| Data Schema | `local-docs/project-requirements/system-data-schema.md` | Data models, field types, constraints, relationships |
| Constitution | `local-docs/project-requirements/constitution-summary.md` | Core principles and boundaries |
| Test Credentials | `main/hairline-backend/TEST_CREDENTIALS.md` | Pre-seeded test accounts |

### Codebase Reference

| Component | Path | Relevance |
|-----------|------|-----------|
| Playwright config | `main/hairline-frontend/playwright.config.ts` | Test runner configuration |
| Existing test specs | `main/hairline-frontend/tests/` | Patterns, auth setup, existing coverage |
| Frontend routes | `main/hairline-frontend/src/data.jsx` | Route definitions, `profileType` filtering |
| Provider pages | `main/hairline-frontend/src/pages/providerDashboard/` | UI components under test |
| Provider API slices | `main/hairline-frontend/src/features/hairlineProvider/` | RTK Query endpoints |
| Backend controllers | `main/hairline-backend/app/Http/Controllers/` | API endpoint implementations |
| Backend routes | `main/hairline-backend/routes/api.php` | API route definitions |
| Backend models | `main/hairline-backend/app/Models/` | Data models and relationships |
| Backend seeders | `main/hairline-backend/database/seeders/` | Test data generation |

---

## 3. Constitution — Rules for Conducting Tests

### 3.1 General Rules

1. **Business-first:** Every test must map to a business requirement. Do not test implementation details (CSS classes, internal state) — test user-visible behavior and API contracts.

2. **Isolation:** Each test must be independent. No test may depend on the execution order or result of another test. Use `beforeEach` / setup fixtures to establish preconditions.

3. **Deterministic:** Tests must produce the same result every run. Avoid time-dependent assertions unless explicitly testing time-based behavior (expiry, SLA). For time-based tests, use controlled timestamps or mock clocks.

4. **No hardcoded waits:** Use `await expect(...).toBeVisible()` or `waitForResponse()` patterns — never `page.waitForTimeout()` with arbitrary delays.

5. **Fail-fast on blockers:** If a precondition cannot be met (e.g., seeder data missing, API down), the test must fail immediately with a descriptive message — not silently pass or hang.

### 3.2 E2E Test Rules (Playwright)

1. **Use the existing Playwright project structure:** Provider tests run in the `chromium` project using `playwright/.auth/user.json` auth state.

2. **Follow the existing auth setup pattern:** Reuse `tests/auth.setup.ts` for clinician login. Create additional setup files only if a different role is needed (e.g., provider owner).

3. **Use role-based locators:** Prefer `getByRole()`, `getByText()`, `getByLabel()` over CSS selectors. This matches the existing test conventions.

4. **Screenshot on failure:** Already configured in `playwright.config.ts`. No additional setup needed.

5. **Test file location:** Place new provider test specs under `tests/treatment-flow/` to separate from existing test files.

### 3.3 API Test Rules (PHPUnit)

1. **Use the `db_test` database:** PHPUnit is already configured to use a separate test database. Never run tests against the development database.

2. **Use factories and seeders:** Create test data using Laravel factories. Do not insert raw SQL unless testing a specific database behavior.

3. **Test file location:** Place new test files under `tests/Feature/TreatmentFlow/` and `tests/Unit/TreatmentFlow/`.

4. **Assert response structure:** Always assert both HTTP status code AND response body structure. A 200 response with wrong data is still a bug.

5. **Test authentication:** Include both positive (valid token) and negative (no token, expired token, wrong role) assertions for every protected endpoint.

### 3.4 Parameterized Tests

Use parameterized tests (data providers in PHPUnit, `test.describe` loops in Playwright) for:

- Input validation with multiple valid/invalid combinations
- Calculations with different numeric inputs (pricing, deposits, installments, graft counts)
- Status transitions with all possible from/to combinations
- Time-boundary tests (just before, exactly at, just after expiry)
- Multi-currency amounts
- Role-based access across different permission levels

### 3.5 What to Test vs What NOT to Test

**Test:**
- All user-facing workflows (main flow, alternative flow, edge cases)
- All API endpoints in the treatment flow
- Business rule enforcement (expiry, payment validation, masking, permissions)
- Calculation accuracy (pricing, deposits, installments, commissions)
- Data integrity (required fields, constraints, relationships)
- Error handling (validation messages, unauthorized access, not found)
- State transitions (inquiry → quote → booking → treatment → aftercare → completed)

**Do NOT test:**
- Third-party library internals (Ant Design rendering, React Router mechanics)
- CSS styling or pixel-level layout (unless a specific UI bug is reported)
- Browser-specific behavior beyond Chromium (scope limited to Chromium)
- Mobile app (Flutter) — out of scope for this test plan
- Payment gateway internals (mock Stripe — test only your integration layer)

---

## 4. Environment Setup Checklist

Before writing or running any tests, verify:

- [ ] Docker containers running: `docker-compose ps` shows php, nginx, mysql, reverb, mailpit all "Up"
- [ ] Database seeded: `docker-compose exec php bash -c "php artisan db:seed --class=FullSeeder"` completed
- [ ] Frontend dependencies installed: `cd main/hairline-frontend && npm install`
- [ ] Playwright browsers installed: `npx playwright install chromium`
- [ ] Frontend dev server starts: `npm run dev` accessible at http://localhost:5173
- [ ] Backend API responds: `curl http://localhost:80/api/` returns response
- [ ] Mailpit accessible: http://localhost:8025 loads
- [ ] Test accounts work: Login as `provider1@hairline.app` / `password123` succeeds

---

## 5. Modules Under Test

The following provider dashboard modules are covered in this test plan, in treatment flow order:

| # | Module | Description | Primary FR |
|---|--------|-------------|------------|
| 1 | Authentication | Sign-in, invite acceptance, password reset, session | FR-009 |
| 2 | Onboarding & Profile | Clinic setup, credentials, team, banking | FR-009, FR-032 |
| 3 | Inquiry Review | Receiving, viewing, patient masking, medical data | FR-003 |
| 4 | Quote Management | Creation, packages, pricing, submission, drafts | FR-004 |
| 5 | Appointment | Confirmed bookings, table list view, unmasked patient | FR-006 |
| 6 | Treatment Execution | Check-in, documentation, photos, medications | FR-010 |
| 7 | Aftercare | Template, milestones, monitoring, patient submissions | FR-011 |
| 8 | Treatment Completion | Marking complete, history, lifecycle closure | FR-010, FR-011 |
| 9 | Cross-Cutting | Notifications, role-based access, data integrity | FR-020, FR-009 |
