# Testing Archive

This folder holds testing artifacts created before 2026-10-19, when testing was consolidated into the `local-docs/testing/` hub (see [../TEST-STRATEGY.md](../TEST-STRATEGY.md)).

- Files are retained **unchanged** for history and traceability. Do not edit them.
- Paths and relative links inside these files point to their original locations and may be broken by design. Use the table below to map an original path to its archive path.
- New testing work never starts here. Use `manual/`, `automated/`, and `results/` instead.

## Contents

| Original path | Archive path | Date | What it covered | Superseded by |
|---|---|---|---|---|
| `testing-plans/2026-01-27/mobile-app-comprehensive-testing-plan.md` | `testing-plans/2026-01-27/mobile-app-comprehensive-testing-plan.md` | 2026-01-27 | Comprehensive manual and usability test plan for the patient mobile app (pre-release) | n/a — mobile app tested separately |
| `testing-plans/2026-03-09/admin-dashboard-manual-testing-plan.md` | `testing-plans/2026-03-09/admin-dashboard-manual-testing-plan.md` | 2026-03-09 | Admin dashboard manual test plan, main treatment flow | `manual/v2/phases/` |
| `testing-plans/2026-03-09/admin-dashboard-automated-testing-plan.md` | `testing-plans/2026-03-09/admin-dashboard-automated-testing-plan.md` | 2026-03-09 | Admin dashboard automated (Playwright and PHPUnit) test plan, main treatment flow | `automated/web-e2e/` |
| `testing-plans/2026-03-09/provider-dashboard-manual-testing-plan.md` | `testing-plans/2026-03-09/provider-dashboard-manual-testing-plan.md` | 2026-03-09 | Provider dashboard manual test plan, main treatment flow | `manual/v2/phases/` |
| `testing-plans/2026-03-09/provider-dashboard-automated-testing-plan.md` | `testing-plans/2026-03-09/provider-dashboard-automated-testing-plan.md` | 2026-03-09 | Provider dashboard automated (Playwright and PHPUnit) test plan, main treatment flow | `automated/web-e2e/` |
| `testing-plans/2026-03-10/automated/testing-strategy.md` | `testing-plans/2026-03-10/automated/testing-strategy.md` | 2026-03-10 | Automated testing strategy for provider and admin dashboards (local offline environment decision) | `TEST-STRATEGY.md` and `automated/web-e2e/` |
| `testing-plans/2026-03-10/automated/admin-dashboard/test-requirements.md` | `testing-plans/2026-03-10/automated/admin-dashboard/test-requirements.md` | 2026-03-10 | Rules and references for writing admin dashboard automated tests | `automated/web-e2e/` |
| `testing-plans/2026-03-10/automated/admin-dashboard/test-checklist-report.md` | `testing-plans/2026-03-10/automated/admin-dashboard/test-checklist-report.md` | 2026-03-10 | Blank admin dashboard automated test checklist and report template | `automated/web-e2e/` |
| `testing-plans/2026-03-10/automated/admin-dashboard/dev_2026-03-18_admin_test-report.md` | `testing-plans/2026-03-10/automated/admin-dashboard/dev_2026-03-18_admin_test-report.md` | 2026-03-18 | Developer-filled admin dashboard automated test run results | `automated/web-e2e/` |
| `testing-plans/2026-03-10/automated/admin-dashboard/audit_2026-03-18_admin.md` | `testing-plans/2026-03-10/automated/admin-dashboard/audit_2026-03-18_admin.md` | 2026-03-18 | Code audit of failed and blocked admin dashboard test cases | `automated/web-e2e/` |
| `testing-plans/2026-03-10/automated/provider-dashboard/test-requirements.md` | `testing-plans/2026-03-10/automated/provider-dashboard/test-requirements.md` | 2026-03-10 | Rules and references for writing provider dashboard automated tests | `automated/web-e2e/` |
| `testing-plans/2026-03-10/automated/provider-dashboard/test-checklist-report.md` | `testing-plans/2026-03-10/automated/provider-dashboard/test-checklist-report.md` | 2026-03-10 | Blank provider dashboard automated test checklist and report template | `automated/web-e2e/` |
| `testing-plans/2026-03-10/automated/provider-dashboard/dev_2026-03-18_provider_test-report.md` | `testing-plans/2026-03-10/automated/provider-dashboard/dev_2026-03-18_provider_test-report.md` | 2026-03-18 | Developer-filled provider dashboard automated test run results | `automated/web-e2e/` |
| `testing-plans/2026-03-10/automated/provider-dashboard/audit_2026-03-18_provider.md` | `testing-plans/2026-03-10/automated/provider-dashboard/audit_2026-03-18_provider.md` | 2026-03-18 | Code audit of failed and blocked provider dashboard test cases | `automated/web-e2e/` |
| `testing-plans/2026-03-10/manual/admin-dashboard-manual-testing-plan.md` | `testing-plans/2026-03-10/manual/admin-dashboard-manual-testing-plan.md` | 2026-03-10 | Admin dashboard manual test plan, reference walkthrough of the main treatment flow | `manual/v2/phases/` |
| `testing-plans/2026-03-10/manual/provider-dashboard-manual-testing-plan.md` | `testing-plans/2026-03-10/manual/provider-dashboard-manual-testing-plan.md` | 2026-03-10 | Provider dashboard manual test plan, reference walkthrough of the main treatment flow | `manual/v2/phases/` |
| `testing-plans/2026-04-06/mobile-app-manual-testing-plan.md` | `testing-plans/2026-04-06/mobile-app-manual-testing-plan.md` | 2026-04-06 | Patient mobile app manual test plan for the missing mobile flows milestone (Android APK) | n/a — mobile app tested separately |
| `testing-plans/2026-04-09/mobile-app-manual-testing-plan.md` | `testing-plans/2026-04-09/mobile-app-manual-testing-plan.md` | 2026-04-09 | Copy of the 2026-04-06 patient mobile app manual test plan used in the 2026-04-09 round | n/a — mobile app tested separately |
| `reports/2026-03-27/manual-testing-status-missing-mobile-flows-design-complement.md` | `reports/2026-03-27/manual-testing-status-missing-mobile-flows-design-complement.md` | 2026-03-27 | Manual test tracker for missing mobile flows from the design complement | n/a — mobile app tested separately |
| `reports/2026-03-30/manual-testing-status-missing-mobile-flows-design-complement.md` | `reports/2026-03-30/manual-testing-status-missing-mobile-flows-design-complement.md` | 2026-03-30 | Carry-forward of the missing mobile flows manual test tracker | n/a — mobile app tested separately |
| `reports/2026-04-06/mobile-app-testing-report.md` | `reports/2026-04-06/mobile-app-testing-report.md` | 2026-04-06 | Patient mobile app manual testing bug and findings report | n/a — mobile app tested separately |
| `reports/2026-04-09/mobile-app-testing-report.md` | `reports/2026-04-09/mobile-app-testing-report.md` | 2026-04-09 | Patient mobile app manual testing bug and findings report, 2026-04-09 round | n/a — mobile app tested separately |
| `reports/2026-04-09/android-qa-new-inquiry.md` | `reports/2026-04-09/android-qa-new-inquiry.md` | 2026-04-09 | Android emulator QA session for new inquiry creation (ended in ANR) | n/a — mobile app tested separately |
| `reports/2026-04-09/android-qa-tc-m-002-settings.md` | `reports/2026-04-09/android-qa-tc-m-002-settings.md` | 2026-04-09 | Android emulator QA session for Profile > Settings (TC-M-002) | n/a — mobile app tested separately |
| `reports/2026-04-15/hairline-mobile-april-2026-postman-collection-test-report.md` | `reports/2026-04-15/hairline-mobile-april-2026-postman-collection-test-report.md` | 2026-04-15 | Live API sweep of the mobile Apr 2026 Postman collection (71 endpoints) | n/a — mobile app tested separately |
| `reports/2026-04-20/hairline-mobile-april-2026-postman-collection-test-report.md` | `reports/2026-04-20/hairline-mobile-april-2026-postman-collection-test-report.md` | 2026-04-20 | Retest of the mobile Apr 2026 Postman collection sweep | n/a — mobile app tested separately |
| `reports/2026-04-22/integrated-testing-plan-report.md` | `reports/2026-04-22/integrated-testing-plan-report.md` | 2026-04-22 | Integrated full-lifecycle test plan and live report for the patient mobile app | n/a — mobile app tested separately |

All original paths are relative to `local-docs/`. All archive paths are relative to this folder.
