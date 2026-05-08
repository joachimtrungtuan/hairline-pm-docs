# Update Log — Admin Module Re-Verification

**Type**: Progress Report Correction — Live Codebase Review  
**Date**: 2026-05-07  
**Scope**: Admin tenant modules A-03, A-05b, A-05c, A-09a, A-09c, A-10  
**Report Updated**: `local-docs/reports/2026-05-06/project-progress-update-report.md`

---

## Trigger

Six admin modules showed suspiciously low completion percentages in the progress report. A direct live-codebase review was requested to reconcile the reported figures against actual frontend + backend implementation.

---

## Methodology

Each module was reviewed by reading the live React frontend source files in `main/hairline-frontend/` and backend route/controller files in `main/hairline-backend/`. The review distinguished between: (a) real RTK Query / axios API calls against real backend routes, (b) hardcoded mock data or local `useState` with static values, and (c) `setTimeout`-based simulations substituting for real API calls.

---

## Findings Summary

| Module | Old % | Revised % | Direction | Root Cause of Change |
|--------|--------|-----------|-----------|----------------------|
| A-03: Aftercare Team Management | 60% | 63% | ↑ | Standalone activation, assign-provider, and active-case detail were already wired with real APIs — prior report underestimated these flows |
| A-05b: Provider Payouts | 33% | 20% | ↓ | `POST billing/approve-provider-payout` and `POST billing/retry-provider-payout` backend routes do not exist; payout detail page is entirely mocked; billing list overwrites real DB data with hardcoded values |
| A-05c: Financial Reconciliation & Reporting | 10% | 12% | ↑ slightly | `FinancialOverView` tab has 4 real API-backed charts; primary `RevenueDashboard` screen is 100% hardcoded mock data (`// MOCK DATA based on exact Figma PRD image`) |
| A-09a: Content & Treatment Management | 33% | 30% | ↓ slightly | Treatments list/detail are genuinely real; questionnaire catalog (all CRUD) and category management initialise from local mock files — no API calls at all; create-set form is a dead no-op |
| A-09c: System Settings & Payment Rules | 56% | 10% | ↓ major | Commission rate save calls `message.success("Save Setting (mock)")`; notification templates/rules use `setTimeout` simulations; admin team management and invite flow are pure local-state mutations; backend API surface for all these is complete but zero frontend wiring |
| A-10: Communication Monitoring & Support | 5% | 22% | ↑ | UI/UX layer is ~70% complete with real business logic (multi-dimension filtering engine, keyword detection, flag state machine, emergency intervention workflow, CSV/PDF export, case resolution validation); backend API surface is ~65% ready; but frontend-to-backend wiring is 0% — no RTK Query slices exist for any support/monitoring feature |

---

## Key Corrections by Module

### A-03 (63%)
**More done than reported:**
- Standalone aftercare request activation is wired (`useActivateRequestMutation` → real backend route) — the earlier 60% figure had this as unavailable
- Assign provider to standalone request uses `useGetAvailableProvidersQuery` loading real providers (not hardcoded)
- Active case detail tabs (milestones, medications, instructions, communication log, progress tracking) all use real API calls

**Still broken/missing:**
- Reassign active case provider dropdown hardcoded to "Provider 1 / Provider 2" stubs (`// TODO: Load providers from API`)
- Edit aftercare plan → placeholder `message.info("coming soon")`
- Add notes → placeholder `message.info("coming soon")`
- Active case sidebar quick-action buttons (Adjust Plan, Request Scan, Escalate) have no `onClick` handlers

---

### A-05b (20%)
**Key findings:**
- Billing list fetch and pay-provider-bill are real API calls
- `POST billing/approve-provider-payout` does not exist in `api.php` — frontend's `onReauthFinish` runs a `setTimeout` then navigates to `?mock_status=failed`
- `POST billing/retry-provider-payout` does not exist in `api.php` — same setTimeout simulation
- Payout detail page uses a hardcoded `queryFn` returning static data (fixed clinic name, IBAN, treatment rows, financial figures); `mock_status` URL param drives the UI state
- Billing list `transformResponse` overwrites all meaningful fields (status, commission, payout reference, readiness status) with hardcoded/index-based logic

---

### A-05c (12%)
**Key findings:**
- `RevenueDashboard.jsx` (the main A-05c screen) has zero API calls — all KPIs, chart series, tables, discount usage, and affiliate summary are `const` hardcoded values with an explicit comment: `// MOCK DATA based on exact Figma PRD image`
- Currency selector and period selector are cosmetic; no data re-fetches on selection
- Export Full Report button has no `onClick` handler
- `DiscountUsageOverview.jsx` imports from a local mock data file
- The `FinancialOverView` tab (4 charts via real APIs) is the only real data connection in this module's scope

---

### A-09a (30%)
**Key findings:**
- `QuestionnaireCatalog.jsx` initialises all state from `questionnaireCatalogMockResponse` in a local `mockData.js` — zero backend calls
- All questionnaire mutations (duplicate, archive, delete, set-active) are local `setRows(...)` React state updates; changes reset on page reload
- Create New Questionnaire Set modal `onFinish` calls `setCreateOpen(false)` — the form is a dead no-op
- Backend has full CRUD at `/questionnaire-sets` and `/questionnaire-categories` — entirely unused by frontend
- Treatment activate/deactivate: `onClick` → `console.log("Deactivate treatment:", id)` only

---

### A-09c (10%)
**Key findings:**
- `CommissionRate.jsx`: `MOCK_PROVIDER_SCOPES` hardcoded array; save → `message.success("Save Setting (mock)")`; backend `/commission-rates` CRUD is complete but unused
- `NotificationRuleEditor.jsx`: every action (fetch rule, save draft, activate, send test) has an explicit `// TODO` comment; all replaced with `setTimeout(500)` simulations
- `NotificationTemplateEditor.jsx`: edit pre-fills hardcoded field values; save/activate/send-test all use `new Promise(r => setTimeout(r, 500))` with no API call; revert version says "(API integration pending)"
- `AdminUsersTab.jsx`: loads `getAdminUsersMock()` from mock file; all user mutations are local state; no API call; invitations push to local state only — no email sent
- Prior 56% estimate reflected UI completion, not functional API integration

---

### A-10 (22%)
**Key findings:**
- No RTK Query slices exist for any support ticket or conversation monitoring feature anywhere in the frontend directory
- `SupportTickets.jsx` generates 52 synthetic records via `buildMockData()` function
- `SupportCaseDetail.jsx` reassign and reopen: `await new Promise(resolve => setTimeout(resolve, 800))` — confirmed fake
- `SupportCaseForm.jsx` submit: `message.success("Support case created (mock).")` — explicitly mock-labelled
- Backend has a substantial API surface: conversations, manual flags, keyword flags, emergency intervention, support contact, keyword rules — all routes present
- The UI/UX layer is well-built (real filtering logic, real keyword detection, real state machines) — raises the estimate from 5% to 22%, but end-to-end real data usage is 0%
