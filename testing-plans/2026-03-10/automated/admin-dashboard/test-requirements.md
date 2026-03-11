# Admin Dashboard — Automated Test Requirements

**Date:** 2026-03-10
**Dashboard:** Admin/Hairline Team Dashboard (`profile_type: "hairline"`)
**Scope:** Main treatment flow — admin oversight from sign-in through treatment completion

---

## 1. Purpose

This document defines the requirements, rules, and reference materials for writing and running automated tests against the Admin Dashboard. The developer writing test scripts must read this document fully before starting.

---

## 2. Related Documents

### Functional Requirements (Source of Truth)

| FR | Title | Path | Relevant Sections |
|----|-------|------|-------------------|
| FR-031 | Admin Access Control & Permissions | `local-docs/project-requirements/system-prd.md` | Admin team member provisioning, role assignment, access validation |
| FR-003 | Inquiry Submission & Distribution | Same directory | Distribution monitoring, SLA tracking (5 min) |
| FR-004 | Quote Submission & Management | Same directory | Quote oversight, commission settings |
| FR-006 | Booking & Scheduling | Same directory | Booking records, deposit configuration |
| FR-007/007B | Payment & Installments | Same directory | Payment administration, deposit %, installment management |
| FR-029 | Payment System Configuration | `local-docs/project-requirements/system-prd.md` | Deposit range configuration, installment option boundaries, new-booking-only config effects |
| FR-010 | Treatment Execution & Documentation | Same directory | Treatment monitoring, status tracking |
| FR-011 | Aftercare & Recovery Management | Same directory | Aftercare oversight, specialist assignment, standalone pricing |
| FR-015 | Provider Management (Admin-Initiated) | `local-docs/project-requirements/system-prd.md` | Provider onboarding, commission config (Percentage/Flat Rate), status management (Active/Suspended/Deactivated) |
| FR-016 | Admin Patient Management | Same directory | Search, view, flag conversations, activity monitoring, write actions, GDPR |
| FR-020 | Notifications & Alerts | Same directory | Dropdown, infinite scroll, real-time delivery |

### System Documents

| Document | Path | Relevance |
|----------|------|-----------|
| System PRD | `local-docs/project-requirements/system-prd.md` | Business rules, admin capabilities |
| Technical Spec | `local-docs/project-requirements/system-technical-spec.md` | API contracts, response formats |
| Data Schema | `local-docs/project-requirements/system-data-schema.md` | Data models, relationships, constraints |
| Constitution | `local-docs/project-requirements/constitution-summary.md` | Core principles |
| Test Credentials | `main/hairline-backend/TEST_CREDENTIALS.md` | Pre-seeded test accounts |

### Codebase Reference

| Component | Path | Relevance |
|-----------|------|-----------|
| Playwright config | `main/hairline-frontend/playwright.config.ts` | Test runner configuration |
| Existing team tests | `main/hairline-frontend/tests/` | Auth setup, existing patterns |
| Team auth setup | `main/hairline-frontend/tests/team-auth.setup.ts` | Admin login fixture |
| Frontend routes | `main/hairline-frontend/src/data.jsx` | Route definitions, `profileType: "hairline"` |
| Team pages | `main/hairline-frontend/src/pages/teamDashboard/` | Admin UI components |
| Team API slices | `main/hairline-frontend/src/features/hairlineTeam/` | Admin RTK Query endpoints |
| Backend controllers | `main/hairline-backend/app/Http/Controllers/` | API implementations |
| Backend routes | `main/hairline-backend/routes/api.php` | API route definitions |
| Backend seeders | `main/hairline-backend/database/seeders/` | Test data generation |

---

## 3. Constitution — Rules for Conducting Tests

### 3.1 General Rules

1. **Business-first:** Every test maps to a business requirement. Test user-visible behavior and API contracts, not implementation details.

2. **Isolation:** Each test is independent. No test depends on execution order. Use setup fixtures for preconditions.

3. **Deterministic:** Same result every run. Use controlled data for time-based assertions.

4. **No hardcoded waits:** Use Playwright auto-waiting (`toBeVisible()`, `waitForResponse()`) — never arbitrary timeouts.

5. **Fail-fast:** If preconditions fail (missing data, API down), fail immediately with a clear message.

### 3.2 E2E Test Rules (Playwright)

1. **Use `team-chromium` project:** Admin tests run using `playwright/.auth/team-user.json` auth state.

2. **Reuse `tests/team-auth.setup.ts`:** Existing admin auth setup logs in as `admin@example.com`.

3. **Role-based locators:** Use `getByRole()`, `getByText()`, `getByLabel()` over CSS selectors.

4. **Test file location:** Place admin test specs under `tests/admin-treatment-flow/`.

### 3.3 API Test Rules (PHPUnit)

1. **Use `db_test` database:** Never run tests against the development database.

2. **Use factories/seeders:** Create test data with Laravel factories.

3. **Test file location:** `tests/Feature/AdminTreatmentFlow/` and `tests/Unit/AdminTreatmentFlow/`.

4. **Assert response structure:** Always check both HTTP status AND response body.

5. **Test role isolation:** Every admin endpoint must be tested with: valid admin token, provider token (should 403), no token (should 401).

### 3.4 Admin-Specific Testing Considerations

1. **Platform-wide visibility:** Admin sees data across ALL providers and patients. Tests must verify cross-provider data aggregation, not just single-provider data.

2. **Read-heavy operations:** Admin dashboard is primarily oversight (read) with limited write operations (status changes, specialist assignment, configuration). Focus assertions on data completeness and accuracy.

3. **Financial precision:** All monetary assertions must check exact values (no floating-point rounding errors). Use parameterized tests for calculations.

4. **Configuration effects:** When admin changes a setting (deposit %, commission rate), verify that subsequent operations use the new value.

### 3.5 Parameterized Tests

Use parameterized tests for:

- Commission rate calculations across different quote amounts
- Deposit percentage calculations (admin-configurable 20-30% range per FR-029 across various totals)
- Installment schedule calculations (2-9 months, divisible and non-divisible amounts)
- Multi-currency display (USD, EUR, GBP, TRY)
- Search queries (exact match, partial, no match, special characters, empty)
- Sort operations (ascending/descending for each sortable column)
- Filter combinations (single filter, multiple filters, filter + sort + search)
- Pagination boundaries (0 items, 1 item, exact page size, page size + 1)
- Role-based access (admin token, provider token, no token, expired token)
- Treatment status transitions (all valid/invalid state changes)

### 3.6 What to Test vs What NOT to Test

**Test:**
- Platform-wide data visibility (admin sees all providers/patients)
- Search, filter, sort, pagination across all data views
- Financial calculations and precision
- Configuration changes and their downstream effects
- Role isolation (admin cannot access provider-only endpoints; provider cannot access admin endpoints)
- Specialist assignment and workflow
- Notification delivery and display
- Admin write actions (password reset, account unlock, profile edit, account suspension)
- GDPR data deletion workflow

**Do NOT test:**
- Third-party library internals
- CSS/styling details
- Mobile app behavior
- Provider-side workflows (covered in Provider test plan)
- Stripe internals (mock the payment gateway)

---

## 4. Environment Setup Checklist

Before writing or running any tests, verify:

- [ ] Docker containers running: `docker-compose ps` shows all services "Up"
- [ ] Database seeded with full data: `php artisan db:seed --class=FullSeeder`
- [ ] Additional admin data seeded: `HairlineDashboardSampleDataSeeder`, `FinancialDataSeeder`, `AfterCareFullDataSeeder`
- [ ] Frontend dependencies installed: `npm install`
- [ ] Playwright browsers installed: `npx playwright install chromium`
- [ ] Frontend dev server accessible at http://localhost:5173
- [ ] Backend API accessible at http://localhost:80
- [ ] Admin login works: `admin@example.com` / `password` → Dashboard loads
- [ ] Admin navigation shows: Overview, Patients, Settings, Billing

---

## 5. Modules Under Test

| # | Module | Description | Primary FR |
|---|--------|-------------|------------|
| 1 | Authentication | Admin sign-in, session, access control, role isolation | FR-031 |
| 2 | Dashboard Overview | Platform metrics, real-time updates, notifications | FR-016, FR-020 |
| 3 | Provider Management | List, search, detail, performance, status controls | FR-015 |
| 4 | Patient Management | List, search, sort, detail, treatment history, billing | FR-016 |
| 5 | Inquiry Monitoring | Platform-wide inquiries, filters, distribution SLA, flagging | FR-003, FR-016 |
| 6 | Quote Oversight | All quotes, filters, commission config | FR-004, FR-015, FR-016 |
| 7 | Payment Administration | Payments, deposits, installments, multi-currency, provider billing | FR-007/007B |
| 8 | Treatment Monitoring | Active treatments, filters, timeline, documentation access | FR-010, FR-016 |
| 9 | Aftercare Administration | Cases, specialist assignment, milestones, submissions | FR-011, FR-016 |
| 10 | Treatment Completion | Completed treatments, treatment lifecycle closure | FR-010, FR-011, FR-016 |
| 11 | Cross-Cutting | Role isolation, data integrity, notifications, configuration | FR-020 |
