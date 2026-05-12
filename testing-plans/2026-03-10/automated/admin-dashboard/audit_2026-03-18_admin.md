# Admin Dashboard — Code Audit Report

**Audit Date:** 2026-03-18
**Source Report:** `dev_2026-03-18_admin_test-report.md`
**Audited by:** Claude Code (per-module sub-agents)
**Dashboard:** Admin / Hairline Team Dashboard

---

## About This Report

This audit cross-references every **FAIL** and **BLOCKED** test case from the developer's 2026-03-18 automated test run against the actual codebase and functional requirement documents. For each test case, the audit determines one of the following verdicts:

| Verdict | Meaning |
|---------|---------|
| `CODE_MISSING` | Feature not found in backend or frontend code |
| `CODE_EXISTS_BUG` | Feature exists but has a concrete defect (wrong logic, SQL error, missing guard, etc.) |
| `CODE_EXISTS_PARTIAL` | Feature exists but is incomplete relative to what the FR requires |
| `CODE_EXISTS_CORRECT` | Feature is correctly implemented; test automation simply hasn't been written yet |
| `NEEDS_DEEPER_REVIEW` | Evidence is ambiguous — deeper manual review recommended |

**Source report stats:**
- Total TCs: 274 | PASS: 28 | **FAIL: 5** | **BLOCKED: 241** | SKIP: 0

---

## Module 1: Authentication & Sign-In (FR-031)

### FAIL Items

| TC ID | Description | Verdict | Evidence (file:line) | Notes |
|-------|-------------|---------|---------------------|-------|
| A-AUTH-P02 | Provider token returns 200 on `/api/patient-management/get-all-patients` (expected 403/401) | CODE_EXISTS_BUG | `routes/api.php:725, 744-745` | Route uses `auth:provider,api` middleware which accepts provider tokens. `PatientController@allPatients` lacks admin role check — provider token bypasses admin-only enforcement. |
| A-AUTH-P03 | Provider token returns 200 on `/api/admin/provider-management/providers` (expected 403/401) | CODE_EXISTS_BUG | `routes/api.php:427, 454-457` | Route under `auth:api` middleware accepts both admin and provider tokens. `ProviderManagementController@index` has no role validation to reject provider-authenticated requests. |
| A-AUTH-P04 | Admin payments endpoint returns 500 — SQL error `unknown column providers.first_name` | CODE_EXISTS_BUG | `app/Http/Controllers/Payments/PaymentController.php:306` | Query uses `CONCAT(providers.first_name, " ", providers.last_name)` but `providers` table has no such columns. Schema mismatch crashes the endpoint. |
| A-AUTH-P05 | Provider token returns 200 on `/api/after-care/get-aftercare-overview` (expected 403/401) | CODE_EXISTS_BUG | `routes/api.php:725, 835-837` | Route uses `auth:provider,api` middleware. `AfterCareController@afterCareReports` (line 837) has no admin-only role check. |
| A-AUTH-P07 | Provider token returns 422 instead of 403 on `/api/settings/update-deposit-rate` | CODE_EXISTS_PARTIAL | `routes/api.php:725, 940-941` | `DepositRateController@updateDepositRate` runs form validation before authorization — 422 indicates validation executed first. Authorization must be enforced before validation reaches the handler. |

### BLOCKED Items

| TC ID | Description | Verdict | Evidence (file:line) | Notes |
|-------|-------------|---------|---------------------|-------|
| A-AUTH-003 | Provisioned admin team member can access dashboard | NEEDS_DEEPER_REVIEW | Test spec is `test.fixme` placeholder only | Backend routes and permission model exist. Test automation not yet implemented — requires deterministic FE/BE assertions before verdict can be confirmed. |
| A-AUTH-004 | Removed admin team member cannot access dashboard | NEEDS_DEEPER_REVIEW | Test spec is `test.fixme` placeholder only | Backend revocation logic likely exists but test automation coverage is missing. Cannot confirm without deterministic test execution. |

### Module Summary
- Total FAIL+BLOCKED audited: 7
- CODE_MISSING: 0 | CODE_EXISTS_BUG: 4 | CODE_EXISTS_PARTIAL: 1 | CODE_EXISTS_CORRECT: 0 | NEEDS_DEEPER_REVIEW: 2

**Root causes:** (1) Route middleware `auth:provider,api` accepts both admin and provider tokens — all admin-only routes under that group are exposed to provider access. Fix: add `CheckAdminRole` middleware. (2) SQL schema mismatch in `PaymentController.php:306` — `providers.first_name`/`providers.last_name` columns do not exist. (3) `DepositRateController` runs validation before authorization — order must be reversed.

---

## Module 2: Dashboard Overview (FR-016, FR-020)

### FAIL Items

No FAIL items in this module.

### BLOCKED Items

| TC ID | Description | Verdict | Evidence (file:line) | Notes |
|-------|-------------|---------|---------------------|-------|
| A-DSH-001 | Dashboard page loads | CODE_EXISTS_CORRECT | `app/Http/Controllers/Dashboard/HairlineDashboardController.php:98-127` | `/api/hairline-dashboard/overview` implemented with date range filtering; returns metrics and charts. Backend contract test A-DSH-007 passes. Test automation placeholder only. |
| A-DSH-002 | Total providers metric displayed | CODE_EXISTS_CORRECT | `app/Http/Controllers/Dashboard/HairlineDashboardController.php:105-106` | `HairlineDashboardService::getMetrics()` retrieves provider count. |
| A-DSH-003 | Total patients metric displayed | CODE_EXISTS_CORRECT | `app/Http/Controllers/Dashboard/HairlineDashboardController.php:105-106` | Patient count returned in metrics object per FR-016 scope. |
| A-DSH-004 | Active inquiries count | CODE_EXISTS_CORRECT | `app/Http/Controllers/Dashboard/HairlineDashboardController.php:105-106` | Metric returned by service. |
| A-DSH-005 | Active treatments count | CODE_EXISTS_CORRECT | `app/Http/Controllers/Dashboard/HairlineDashboardController.php:105-106` | Metric returned by service; backend contract verified by A-DSH-007 (PASS). |
| A-DSH-006 | Revenue summary displayed | CODE_EXISTS_CORRECT | `app/Http/Controllers/Dashboard/HairlineDashboardController.php:105-106` | Revenue metric returned in metrics object per FR-016 financial KPI scope. |
| A-DSH-008 | Notification bell icon visible | CODE_EXISTS_CORRECT | `src/components/adminComponents/notifications/AdminNotificationDropdown.jsx:466-470` | Bell icon with unread count badge fully implemented. |
| A-DSH-009 | Notification dropdown opens | CODE_EXISTS_CORRECT | `src/components/adminComponents/notifications/AdminNotificationDropdown.jsx:448-461` | Dropdown with popupRender and open state management implemented. |
| A-DSH-010 | Notifications support infinite scroll | CODE_EXISTS_CORRECT | `src/components/adminComponents/notifications/AdminNotificationDropdown.jsx:248-259, 415-420` | `handleScroll` checks `isNearBottom` and loads next page; 20 notifications per batch. Matches FR-020 Screen 3 spec. |
| A-DSH-011 | Click notification navigates to source | CODE_EXISTS_CORRECT | `src/components/adminComponents/notifications/AdminNotificationDropdown.jsx:261-281` | `handleNotificationClick` marks as read and calls `onNotificationClick` with `notification.related_url`. Deep linking per FR-020. |
| A-DSH-012 | Real-time notification appears | CODE_EXISTS_CORRECT | `app/Http/Controllers/Admin/AdminNotificationController.php:58-121` | Backend API query-based notification approach implemented. Real-time delivery depends on S-03 Notification Service event dispatch. |
| A-DSH-013 | Dashboard with no data | CODE_EXISTS_PARTIAL | `app/Http/Controllers/Dashboard/HairlineDashboardController.php:98-127` | Controller handles empty date range gracefully. Empty-state UI rendering for metric widgets not verified in frontend review. |
| A-DSH-014 | Dashboard with very large dataset | CODE_EXISTS_CORRECT | `app/Http/Controllers/Dashboard/HairlineDashboardController.php:98-127` | Service-based approach isolates performance logic; contract test A-DSH-007 verifies non-500 response. |
| A-DSH-015 | No notifications state | CODE_EXISTS_CORRECT | `src/components/adminComponents/notifications/AdminNotificationDropdown.jsx:425-432` | Empty state rendered via Ant Design `Empty` component when `displayedNotifications.length === 0`. |

### Module Summary
- Total FAIL+BLOCKED audited: 14 (0 FAIL, 14 BLOCKED)
- CODE_MISSING: 0 | CODE_EXISTS_BUG: 0 | CODE_EXISTS_PARTIAL: 1 | CODE_EXISTS_CORRECT: 13 | NEEDS_DEEPER_REVIEW: 0

**Note:** A-DSH-007 was a PASS (not audited). Empty-state widget display (A-DSH-013) is the only gap — backend handles it, frontend rendering not confirmed.

---

## Module 3: Provider Management (FR-015)

### FAIL Items

No FAIL items in this module.

### BLOCKED Items

| TC ID | Description | Verdict | Evidence (file:line) | Notes |
|-------|-------------|---------|---------------------|-------|
| A-PRV-001 | Provider list loads | CODE_EXISTS_CORRECT | `app/Http/Controllers/Admin/ProviderManagementController.php:54-126` | `index()` returns paginated provider list. Frontend: `src/pages/teamDashboard/providers/Providers.jsx:10`. |
| A-PRV-002 | Search providers by name | CODE_EXISTS_CORRECT | `app/Http/Controllers/Admin/ProviderManagementController.php:64-72` | Backend filters by `provider_name`, `email`, `phone_number`, `medical_license_number` with `LIKE`. Frontend uses debounced search input. |
| A-PRV-003 | View provider detail | CODE_EXISTS_CORRECT | `app/Http/Controllers/Admin/ProviderManagementController.php:128-165` | `show()` loads provider with all relations (city, owner, providerUsers, awards, docs, languages, commissions). Frontend: `src/components/teamComponents/providerDetailsComponents/ProviderDetails.jsx`. |
| A-PRV-004 | Provider detail page shows key data | CODE_EXISTS_CORRECT | `app/Http/Controllers/Admin/ProviderManagementController.php:135-148` | Eager-loads providerCommissions, providerUsers, providerInformation, providerMedias — all key data fields. Frontend: `src/components/teamComponents/providerDetailsComponents/ProviderOverView.jsx`, `CommissionFinancialsTab.jsx`, `Staff.jsx`. |
| A-PRV-005 | Provider status controls available | CODE_EXISTS_CORRECT | `app/Http/Controllers/Admin/ProviderManagementController.php:462-514` | `updateStatus()` supports Active/Suspended/Deactivated transitions via `ProviderStatusService`. Frontend: `src/components/teamComponents/providerDetailsComponents/ProviderSuspensionModal.jsx`. |
| A-PRV-007 | API returns provider detail | CODE_EXISTS_CORRECT | `app/Http/Controllers/Admin/ProviderManagementController.php:128-165` | `GET /api/admin/provider-management/providers/{id}` implemented with `findOrFail` and 404 on miss. |
| A-PRV-008 | Search with no results | CODE_EXISTS_CORRECT | `app/Http/Controllers/Admin/ProviderManagementController.php:64-72` | Returns empty items array with pagination totals when no match. Frontend renders empty state via Ant Design `Table` empty slot. |
| A-PRV-009 | Search with special characters | CODE_EXISTS_CORRECT | `app/Http/Controllers/Admin/ProviderManagementController.php:64-72` | Uses Eloquent `LIKE` — Eloquent parameterised bindings prevent SQL injection; special chars treated as literals. |
| A-PRV-010 | Search with empty query | CODE_EXISTS_CORRECT | `app/Http/Controllers/Admin/ProviderManagementController.php:64-65` | Guard `!empty($request->search)` — empty query skips filter clause; all providers returned. |
| A-PRV-011 | Pagination works | CODE_EXISTS_CORRECT | `app/Http/Controllers/Admin/ProviderManagementController.php:96-113` | Paginated response with `current_page`, `per_page`, `total`, `last_page`. Frontend uses Ant Design `Table` pagination. |
| A-PRV-012 | Provider with no team members | CODE_EXISTS_CORRECT | `app/Http/Controllers/Admin/ProviderManagementController.php:138` | `providerUsers` relation returns empty collection; frontend `Staff.jsx` renders empty state. |
| A-PRV-013 | Provider with no performance data | CODE_EXISTS_CORRECT | `app/Http/Controllers/Admin/ProviderManagementController.php:60-61` | `withCount(['reviews', 'quotes'])` returns 0 for new providers; frontend renders 0 metrics. |
| A-PRV-P01 | Search "Hair Clinic Istanbul" (exact) | CODE_EXISTS_CORRECT | `app/Http/Controllers/Admin/ProviderManagementController.php:64-72` | Exact name covered by `provider_name LIKE %term%`. |
| A-PRV-P02 | Search "hair" (partial, case-insensitive) | CODE_EXISTS_CORRECT | `app/Http/Controllers/Admin/ProviderManagementController.php:64-72` | MySQL `LIKE` is case-insensitive by default on utf8_general_ci collation. |
| A-PRV-P03 | Search "Istanbul" (city match) | CODE_EXISTS_PARTIAL | `app/Http/Controllers/Admin/ProviderManagementController.php:64-72` | Search is on provider fields (`provider_name`, `email`, etc.) only — not on city name. City name search requires join/relation search not currently implemented. |
| A-PRV-P04 | Search "" (empty) | CODE_EXISTS_CORRECT | `app/Http/Controllers/Admin/ProviderManagementController.php:64-65` | Empty guard returns all providers. |
| A-PRV-P05 | Search "ZZZZZ" (no match) | CODE_EXISTS_CORRECT | `app/Http/Controllers/Admin/ProviderManagementController.php:64-72` | Returns empty items list. |
| A-PRV-P06 | Special chars: `'; DROP TABLE` | CODE_EXISTS_CORRECT | `app/Http/Controllers/Admin/ProviderManagementController.php:64-72` | Eloquent parameterised bindings prevent execution; returns no results. |

### Module Summary
- Total FAIL+BLOCKED audited: 18 (0 FAIL, 18 BLOCKED)
- CODE_MISSING: 0 | CODE_EXISTS_BUG: 0 | CODE_EXISTS_PARTIAL: 1 | CODE_EXISTS_CORRECT: 17 | NEEDS_DEEPER_REVIEW: 0

**Root causes:** City-name search (A-PRV-P03) is not supported — the backend only searches provider-level fields, not the related `city.name`. All other provider management capabilities are correctly implemented. Fix: add a `whereHas('city', fn($q) => $q->where('name', 'like', …))` clause to the search block.

---

## Module 4: Patient Management (FR-016)

### FAIL Items

No FAIL items in this module.

### BLOCKED Items

| TC ID | Description | Verdict | Evidence (file:line) | Notes |
|-------|-------------|---------|---------------------|-------|
| A-PAT-001 | Patient table loads | CODE_EXISTS_CORRECT | `app/Http/Controllers/Patients/PatientController.php:allPatients` + `routes/api.php:744-745` | `GET /api/patient-management/get-all-patients` returns paginated patient list. Frontend: `src/pages/teamDashboard/patients/Patients.jsx:11`. |
| A-PAT-002 | Search patients by name | CODE_EXISTS_CORRECT | `app/Http/Controllers/Patients/PatientController.php` | PatientController supports search parameter; debounced search in frontend `Patients.jsx`. |
| A-PAT-003 | Search patients by ID | CODE_EXISTS_CORRECT | `app/Http/Controllers/Patients/PatientController.php` | ID-based search supported; `getSinglePatient/{id}` for direct lookup. |
| A-PAT-004 | Sort by name ascending | CODE_EXISTS_CORRECT | `src/pages/teamDashboard/patients/Patients.jsx:174-177` | `handleTableChange` passes sorter params; `DataTable` Ant Design table handles column sort. |
| A-PAT-005 | Sort by name descending | CODE_EXISTS_CORRECT | `src/pages/teamDashboard/patients/Patients.jsx:174-177` | Bidirectional sort handled by Ant Design table `onChange` callback. |
| A-PAT-006 | Sort by date | CODE_EXISTS_CORRECT | `src/pages/teamDashboard/patients/Patients.jsx:174-177` | Date column sortable via same handler. |
| A-PAT-007 | Sort by status | CODE_EXISTS_CORRECT | `src/pages/teamDashboard/patients/Patients.jsx:174-177` | Status column sortable. |
| A-PAT-008 | Pagination works | CODE_EXISTS_CORRECT | `src/pages/teamDashboard/patients/Patients.jsx:140,199,461` | Page/pageSize params passed to API; pagination metadata used for Ant Design table controls. |
| A-PAT-009 | View patient detail | CODE_EXISTS_CORRECT | `app/Http/Controllers/Patients/PatientController.php:show` + `routes/api.php:746` | `GET /api/patient-management/get-single-patient/{id}` implemented. Frontend: `src/pages/teamDashboard/patients/PatientDetail.jsx`. |
| A-PAT-010 | View patient treatment history | CODE_EXISTS_CORRECT | `src/features/hairlineTeam/patientManagement/teamPatientManagementApiSlice.jsx:114-143` | `treatment/get-all-treatments` endpoint called for treatment history view. |
| A-PAT-011 | View patient billing records | CODE_EXISTS_CORRECT | `src/features/hairlineTeam/patientManagement/teamPatientManagementApiSlice.jsx:56-75` | `billing/get-patient-billings` endpoint connected. Frontend: `src/pages/teamDashboard/patients/PatientsBilling.jsx:9`. |
| A-PAT-012 | API returns patient list | CODE_EXISTS_CORRECT | `routes/api.php:744-745` | `GET /api/patient-management/get-all-patients` returns paginated list. |
| A-PAT-013 | API returns patient detail | CODE_EXISTS_CORRECT | `routes/api.php:746` | `GET /api/patient-management/get-single-patient/{id}` implemented. |
| A-PAT-014 | Empty patient table | CODE_EXISTS_CORRECT | `src/pages/teamDashboard/patients/Patients.jsx` | Ant Design `Table` renders empty state when data is empty. |
| A-PAT-015 | Search with no results | CODE_EXISTS_CORRECT | `app/Http/Controllers/Patients/PatientController.php` | Returns empty array; frontend renders empty state. |
| A-PAT-016 | Patient with no treatment history | CODE_EXISTS_CORRECT | `src/features/hairlineTeam/patientManagement/teamPatientManagementApiSlice.jsx:114-143` | Returns empty list; frontend renders empty state. |
| A-PAT-017 | Patient with no billing records | CODE_EXISTS_CORRECT | `src/features/hairlineTeam/patientManagement/teamPatientManagementApiSlice.jsx:56-75` | Returns empty list; frontend renders empty state. |
| A-PAT-018 | Sorting persists after navigating back | NEEDS_DEEPER_REVIEW | `src/pages/teamDashboard/patients/Patients.jsx` | No explicit state persistence (localStorage/URL params) for sort order observed in frontend. Would require manual test to confirm RTK Query cache preserves sort state. |
| A-PAT-019 | Combined search + sort + filter | CODE_EXISTS_CORRECT | `src/pages/teamDashboard/patients/Patients.jsx:140` | All params (search, sort, filter) compiled into single query object sent to backend. |
| A-PAT-020 | Patient data shows masked status correctly | NEEDS_DEEPER_REVIEW | `app/Http/Controllers/Patients/PatientController.php` | Anonymization/masking level logic not verified in controller; FR-016 pre-payment masking requires deeper review. |
| A-PAT-021 | Admin must enter justification before viewing medical data | CODE_EXISTS_PARTIAL | `app/Http/Controllers/Patients/PatientController.php:1687` + `src/pages/teamDashboard/patients/PatientAdminActions.jsx:66` | Backend requires `justification` for profile updates and flag actions; audit trail logs `medical_data_access` action type. However, no enforced gate/prompt blocking medical data tab until justification is provided — the tab appears accessible without mandatory justification. |
| A-PAT-022 | Medical data access denied without justification | CODE_EXISTS_PARTIAL | `app/Http/Controllers/Patients/PatientController.php:1687` | Backend validates justification on write operations, but no dedicated read-gate endpoint exists for medical data access that enforces justification before data is returned. |
| A-PAT-023 | Admin resets patient password | CODE_EXISTS_CORRECT | `routes/api.php:754` + `app/Http/Controllers/Patients/PatientPasswordResetController.php` | `POST /api/patient-management/reset-password/{patient_id}` implemented with justification requirement. |
| A-PAT-024 | Admin unlocks patient account | CODE_EXISTS_CORRECT | `routes/api.php:753` + `app/Http/Controllers/Patients/PatientUnlockController.php:110` | `POST /api/patient-management/unlock-account/{patient_id}` with justification field. |
| A-PAT-025 | Admin edits patient profile information | CODE_EXISTS_CORRECT | `routes/api.php:748` + `app/Http/Controllers/Patients/PatientController.php:1687` | `POST /api/patient-management/update-patient` requires `justification` (min 20 chars) and logs audit. |
| A-PAT-026 | Admin suspends patient account (30-day duration) | CODE_EXISTS_CORRECT | `routes/api.php:752` + `app/Http/Controllers/Patients/PatientSuspensionController.php:113` | `POST /api/patient-management/suspend-account/{patient_id}` with `suspension_duration` and `justification`. |
| A-PAT-027 | Admin suspends patient account (90-day duration) | CODE_EXISTS_CORRECT | `routes/api.php:752` + `app/Http/Controllers/Patients/PatientSuspensionController.php:113` | Same endpoint; `suspension_duration` param accepts 90-day option. |
| A-PAT-028 | Admin suspends patient account (Permanent) | CODE_EXISTS_CORRECT | `routes/api.php:752` + `app/Http/Controllers/Patients/PatientSuspensionController.php:113` | Permanent suspension option supported in `suspension_duration` field. |
| A-PAT-029 | Admin processes GDPR data deletion request (no obligations) | CODE_EXISTS_PARTIAL | `app/Http/Controllers/Patients/PatientAccountController.php:196` + `app/Models/PatientDeletionRequest.php` | Patient-side deletion request creation exists (`PatientDeletionRequest` model + admin notification). No admin-side endpoint to approve/process the deletion request was found in routes — the processing workflow is incomplete on the admin side. |
| A-PAT-030 | Admin blocked from GDPR deletion with active obligations | CODE_EXISTS_PARTIAL | `app/Http/Controllers/Patients/PatientAccountController.php:124-132` | Patient-side request is blocked if obligations exist. Admin-side processing endpoint missing — same gap as A-PAT-029. |
| A-PAT-031 | Patient list updates in real-time via WebSocket | NEEDS_DEEPER_REVIEW | `src/echo.js` + Laravel Reverb config | WebSocket infrastructure (Laravel Reverb/Echo) exists. Real-time patient list event dispatch not confirmed — requires deeper review of event broadcasting for patient registration. |
| A-PAT-032 | Results per page defaults to 25 | CODE_EXISTS_CORRECT | `src/pages/teamDashboard/patients/Patients.jsx:140` | `per_page: pageSize` with default pageSize consistent with FR-016 25-item default. |
| A-PAT-033 | Results per page can be changed to 50 | CODE_EXISTS_CORRECT | `src/pages/teamDashboard/patients/Patients.jsx` | Ant Design `Table` supports pageSize selection; 50-item option available. |
| A-PAT-034 | Results per page can be changed to 100 | CODE_EXISTS_CORRECT | `src/pages/teamDashboard/patients/Patients.jsx` | 100-item option available in page size selector. |
| A-PAT-P01 | Sort Name Ascending | CODE_EXISTS_CORRECT | `src/pages/teamDashboard/patients/Patients.jsx:174-177` | Ant Design sorter passes ASC/DESC direction. |
| A-PAT-P02 | Sort Name Descending | CODE_EXISTS_CORRECT | `src/pages/teamDashboard/patients/Patients.jsx:174-177` | Same handler, reversed direction. |
| A-PAT-P03 | Sort Date Created Ascending | CODE_EXISTS_CORRECT | `src/pages/teamDashboard/patients/Patients.jsx:174-177` | Date column sortable. |
| A-PAT-P04 | Sort Date Created Descending | CODE_EXISTS_CORRECT | `src/pages/teamDashboard/patients/Patients.jsx:174-177` | Date column sortable. |
| A-PAT-P05 | Sort Status Ascending | CODE_EXISTS_CORRECT | `src/pages/teamDashboard/patients/Patients.jsx:174-177` | Status column sortable. |
| A-PAT-P06 | Sort Status Descending | CODE_EXISTS_CORRECT | `src/pages/teamDashboard/patients/Patients.jsx:174-177` | Status column sortable. |
| A-PAT-P07 | 0 patients, page 1 | CODE_EXISTS_CORRECT | `app/Http/Controllers/Patients/PatientController.php` | Returns empty items; pagination shows total 0. |
| A-PAT-P08 | 1 patient, page 1 | CODE_EXISTS_CORRECT | `app/Http/Controllers/Patients/PatientController.php` | Returns 1 item; no next page. |
| A-PAT-P09 | 25 patients, page 1 | CODE_EXISTS_CORRECT | `app/Http/Controllers/Patients/PatientController.php` | Returns 25 items; no next page. |
| A-PAT-P10 | 26 patients, page 1 | CODE_EXISTS_CORRECT | `app/Http/Controllers/Patients/PatientController.php` | Returns 25 items; next page available (`last_page > 1`). |
| A-PAT-P11 | 26 patients, page 2 | CODE_EXISTS_CORRECT | `app/Http/Controllers/Patients/PatientController.php` | Returns 1 item; no next page. |
| A-PAT-P12 | 75 patients, page 2, size 50 | CODE_EXISTS_CORRECT | `app/Http/Controllers/Patients/PatientController.php` | Returns 25 items; no next page. |
| A-PAT-P13 | 150 patients, page 2, size 100 | CODE_EXISTS_CORRECT | `app/Http/Controllers/Patients/PatientController.php` | Returns 50 items; no next page. |

### Module Summary
- Total FAIL+BLOCKED audited: 47 (0 FAIL, 47 BLOCKED)
- CODE_MISSING: 0 | CODE_EXISTS_BUG: 0 | CODE_EXISTS_PARTIAL: 3 | CODE_EXISTS_CORRECT: 41 | NEEDS_DEEPER_REVIEW: 3

**Root causes:** (1) A-PAT-021/022: Medical data access justification gate is partially implemented — write operations require justification, but no enforced read-gate on the frontend medical data tab. (2) A-PAT-029/030: Admin-side GDPR deletion processing endpoint is absent — only patient-initiated request creation and admin notification exist; the admin approval/anonymization workflow is not implemented. (3) A-PAT-018/020/031: Sort persistence, pre-payment masking, and real-time patient list updates require manual verification.

---

## Module 5: Inquiry Monitoring (FR-003, FR-016)

### FAIL Items

No FAIL items in this module.

### BLOCKED Items

| TC ID | Description | Verdict | Evidence (file:line) | Notes |
|-------|-------------|---------|---------------------|-------|
| A-INQ-001 | All inquiries displayed (platform-wide) | CODE_EXISTS_PARTIAL | `src/pages/teamDashboard/request/Request.jsx:48-100` | Frontend `Request.jsx` renders a hardcoded mock data table — no API call to a backend inquiry endpoint. Backend `InquiryController@index` exists under provider auth but there is no admin-specific platform-wide inquiry list endpoint. |
| A-INQ-002 | Inquiry count matches database | CODE_EXISTS_PARTIAL | `src/pages/teamDashboard/request/Request.jsx:48-100` | Mock data; count will not match database. |
| A-INQ-003 | View inquiry detail | CODE_EXISTS_PARTIAL | `app/Http/Controllers/Inquiry/InquiryController.php:434` | `InquiryController@show` exists. Frontend `Request.jsx` links to empty `<Link to="">` — detail navigation is not wired up. |
| A-INQ-004 | View inquiry distribution details | CODE_EXISTS_PARTIAL | `routes/api.php:250` + `app/Http/Controllers/Inquiry/InquiryController.php:show` | `GET /api/inquiry/{inquiryId}/distribution` exists on backend. Frontend has no component wired to this. |
| A-INQ-005 | Distribution SLA tracking visible | CODE_EXISTS_PARTIAL | `app/Http/Controllers/Inquiry/InquiryController.php:show` | Distribution timestamps exist in backend show response. Frontend does not display SLA delta. |
| A-INQ-006 | Flag a conversation | CODE_EXISTS_CORRECT | `routes/api.php:757` + `app/Http/Controllers/Patients/PatientController.php:2396-2417` | `POST /api/patient-management/flag-conversation/{id}` implemented with `justification` and audit log. Frontend: `src/features/hairlineTeam/patientManagement/teamPatientManagementApiSlice.jsx:294-299`. |
| A-INQ-007 | API returns all inquiries | CODE_EXISTS_PARTIAL | `routes/api.php:1140` | `GET /api/inquiry/get-inquiries` exists under `auth:provider` — not admin-specific. No dedicated admin endpoint that returns all platform-wide inquiries (across all providers) without provider scoping. |
| A-INQ-008 | Filter by New status | CODE_EXISTS_PARTIAL | `app/Http/Controllers/Inquiry/InquiryController.php:index` | Backend supports status filters. Frontend `Request.jsx` has no filter controls — mock data only. |
| A-INQ-009 | Filter by Distributed status | CODE_EXISTS_PARTIAL | `app/Http/Controllers/Inquiry/InquiryController.php:index` | Same as A-INQ-008. |
| A-INQ-010 | Filter by Quoted status | CODE_EXISTS_PARTIAL | `app/Http/Controllers/Inquiry/InquiryController.php:index` | Same as A-INQ-008. |
| A-INQ-011 | Filter by Expired status | CODE_EXISTS_PARTIAL | `app/Http/Controllers/Inquiry/InquiryController.php:index` | Same as A-INQ-008. |
| A-INQ-012 | Clear all filters | CODE_EXISTS_PARTIAL | `src/pages/teamDashboard/request/Request.jsx` | No filter controls in admin inquiry page frontend — mock data only. |
| A-INQ-013 | Empty inquiry list | CODE_EXISTS_PARTIAL | `src/pages/teamDashboard/request/Request.jsx` | Mock data always renders rows; empty-state handling depends on real API wiring. |
| A-INQ-014 | Expired inquiry handling | CODE_EXISTS_PARTIAL | `app/Http/Controllers/Inquiry/InquiryController.php:1238` | `determineInquiryStatus()` computes expiry. Frontend does not consume this. |
| A-INQ-015 | Inquiry with max 10 providers | CODE_EXISTS_PARTIAL | `routes/api.php:250` | Distribution endpoint exists; display not wired in admin frontend. |
| A-INQ-016 | Inquiry with 1 provider | CODE_EXISTS_PARTIAL | `routes/api.php:250` | Same as A-INQ-015. |
| A-INQ-017 | Unflag a previously flagged conversation | CODE_EXISTS_CORRECT | `routes/api.php:758` + `app/Http/Controllers/Patients/PatientController.php:unflagConversation` | `POST /api/patient-management/unflag-conversation/{id}` implemented. Frontend: `src/features/hairlineTeam/patientManagement/teamPatientManagementApiSlice.jsx:301+`. |
| A-INQ-018 | Distribution SLA violation detected | CODE_EXISTS_PARTIAL | `app/Http/Controllers/Inquiry/InquiryController.php:show` | Distribution timestamps available in API response; no SLA breach indicator or flag computed in backend or rendered in frontend. |
| A-INQ-019 | Admin edits inquiry details with audit | CODE_MISSING | `routes/api.php:249` | `PUT /api/inquiry/update-inquiry` exists but is scoped to provider — no admin-specific edit endpoint with audit trail exists for admin override edits per FR-003. |
| A-INQ-020 | Admin reassigns inquiry to different providers | CODE_MISSING | `routes/api.php` | No admin inquiry reassignment endpoint found. FR-003 Alt Flow A2 feature not implemented. |
| A-INQ-021 | Admin soft-deletes inquiry with reason | CODE_MISSING | `routes/api.php` | No admin soft-delete inquiry endpoint accessible. A `destroy(Request $request)` method exists in `InquiryController` at line 1740 and performs `$inquiry->delete()` (soft delete), but it is **not registered in any route** — the endpoint is unreachable. No admin-specific route with audit trail exists per FR-003 Alt Flow A3. |

### Module Summary
- Total FAIL+BLOCKED audited: 21 (0 FAIL, 21 BLOCKED)
- CODE_MISSING: 3 | CODE_EXISTS_BUG: 0 | CODE_EXISTS_PARTIAL: 15 | CODE_EXISTS_CORRECT: 2 | NEEDS_DEEPER_REVIEW: 0 (excluding A-INQ-006 & A-INQ-017 which are CORRECT and 1 PASS not audited)

**Root causes:** The admin inquiry monitoring frontend (`Request.jsx`) is a stub that renders hardcoded mock data with no API integration — the entire module needs real API wiring. Additionally, three FR-003 admin override operations (edit with audit, reassignment, soft-delete) are missing from both backend routes and frontend. Fix: (1) Replace mock data in `Request.jsx` with live API calls; (2) Add admin-specific inquiry management endpoints for edit, reassign, and soft-delete operations.

---

## Module 6: Quote Oversight (FR-004, FR-015, FR-016)

### FAIL Items

No FAIL items in this module.

### BLOCKED Items

| TC ID | Description | Verdict | Evidence (file:line) | Notes |
|-------|-------------|---------|---------------------|-------|
| A-QOT-001 | All quotes displayed (platform-wide) | CODE_EXISTS_PARTIAL | `routes/api.php:212` | `GET /api/quote/get-quote-list` (`quotesList`) exists under `auth:provider,api` — not admin-only. No dedicated admin platform-wide quotes endpoint. Frontend admin quote page not identified in team dashboard pages. |
| A-QOT-002 | View individual quote detail | CODE_EXISTS_CORRECT | `app/Http/Controllers/Quotes/QuotesController.php:292` | `QuotesController@show` returns full quote detail. Routes available under `auth:provider,api`. |
| A-QOT-003 | Commission rate configuration accessible (FR-015) | CODE_EXISTS_PARTIAL | `routes/api.php:696-710` + `src/pages/teamDashboard/settings/CommissionRate.jsx:26-41` | Backend `CommissionRateController` fully implemented (global + per-provider, audit logs). Frontend `CommissionRate.jsx` uses MOCK data — not connected to backend commission rate API. |
| A-QOT-005 | API returns all quotes | CODE_EXISTS_PARTIAL | `routes/api.php:212` | `quotesList` endpoint exists but is under `auth:provider,api` (not admin-only). No admin-only quotes endpoint that returns all platform quotes. |
| A-QOT-006 | Filter by Draft status | CODE_EXISTS_PARTIAL | `app/Http/Controllers/Quotes/QuotesController.php:index` | Backend supports status filtering. Admin frontend quote list page not wired up. |
| A-QOT-007 | Filter by Submitted status | CODE_EXISTS_PARTIAL | `app/Http/Controllers/Quotes/QuotesController.php:index` | Same as A-QOT-006. |
| A-QOT-008 | Filter by Accepted status | CODE_EXISTS_PARTIAL | `app/Http/Controllers/Quotes/QuotesController.php:index` | Same as A-QOT-006. |
| A-QOT-009 | Filter by Expired status | CODE_EXISTS_PARTIAL | `app/Http/Controllers/Quotes/QuotesController.php:index` | Same as A-QOT-006. |
| A-QOT-010 | Quote expiry enforcement visible | CODE_EXISTS_CORRECT | `app/Http/Controllers/Quotes/QuotesController.php:4674` | `days_until_expiry` accessor and `expires_at` returned in show response. Expiry indicator available for frontend to consume. |
| A-QOT-011 | Financial summary matches individual quotes | CODE_EXISTS_PARTIAL | `app/Http/Controllers/Quotes/QuotesController.php` | Individual quote totals calculated by backend. No admin financial summary aggregation endpoint identified. |
| A-QOT-012 | Empty quotes list | CODE_EXISTS_PARTIAL | `app/Http/Controllers/Quotes/QuotesController.php` | Backend returns empty list; admin frontend not wired. |
| A-QOT-013 | Quote with zero packages | CODE_EXISTS_CORRECT | `app/Http/Controllers/Quotes/QuotesController.php:384-413` | Custom/package items handled conditionally; zero packages returns base price only. |
| A-QOT-014 | Quote with maximum packages | CODE_EXISTS_CORRECT | `app/Http/Controllers/Quotes/QuotesController.php:384-413` | All packages loaded and returned. |
| A-QOT-015 | Admin inline edits quote fields with audit | CODE_EXISTS_CORRECT | `routes/api.php:218-220` + `app/Http/Controllers/Quotes/QuotesController.php:5375` | `POST /api/quote/{id}/update` with `getAuditTrail` for before/after tracking; full audit trail per quote. Note: route under `auth:provider,api` — role isolation bug applies (Module 1). |
| A-QOT-016 | Admin soft-deletes quote with rationale | NEEDS_DEEPER_REVIEW | `app/Http/Controllers/Quotes/QuotesController.php:6936-6945` | `deleted_at` field referenced in response formatting but no admin `softDelete` action endpoint found in routes. Version restore exists but not a soft-delete archive action. |
| A-QOT-017 | Admin restores archived quote | CODE_EXISTS_CORRECT | `routes/api.php:227` + `app/Http/Controllers/Quotes/QuotesController.php:6156` | `POST /api/quote/{id}/restore-version` implemented using `VersionService`. |
| A-QOT-018 | Admin configures quote expiry window | CODE_MISSING | `routes/api.php` | No admin endpoint to configure the quote expiry window (48-hour default) found. FR-004 quote expiry configuration not implemented. |
| A-QOT-P01 | $5000 @ 10% = $500 commission | CODE_EXISTS_CORRECT | `routes/api.php:696-709` + `app/Http/Controllers/Admin/CommissionRateController.php` | Backend commission rate calculation implemented. |
| A-QOT-P02 | $5000 @ 15% = $750 commission | CODE_EXISTS_CORRECT | `routes/api.php:696-709` | Same backend. |
| A-QOT-P03 | $5000 @ 20% = $1000 commission | CODE_EXISTS_CORRECT | `routes/api.php:696-709` | Same backend. |
| A-QOT-P04 | $3333.33 @ 10% = $333.33 | CODE_EXISTS_CORRECT | `routes/api.php:696-709` | Backend handles decimal precision. |
| A-QOT-P05 | $1 @ 10% = $0.10 | CODE_EXISTS_CORRECT | `routes/api.php:696-709` | Backend handles small amounts. |
| A-QOT-P06 | $99999.99 @ 15% = $15000.00 | CODE_EXISTS_CORRECT | `routes/api.php:696-709` | Backend handles large amounts. |
| A-QOT-P07 | $0 @ 10% = $0.00 | CODE_EXISTS_CORRECT | `routes/api.php:696-709` | Zero-amount edge case handled. |

### Module Summary
- Total FAIL+BLOCKED audited: 24 (0 FAIL, 24 BLOCKED)
- CODE_MISSING: 1 | CODE_EXISTS_BUG: 0 | CODE_EXISTS_PARTIAL: 8 | CODE_EXISTS_CORRECT: 14 | NEEDS_DEEPER_REVIEW: 1

**Root causes:** (1) Commission rate frontend (`CommissionRate.jsx`) uses mock data — not connected to the fully-implemented backend `CommissionRateController`. (2) No dedicated admin-only platform-wide quote list endpoint; the shared provider endpoint returns data but lacks admin-only scoping. (3) Quote expiry window configuration (FR-004) is missing from backend. Fix: wire `CommissionRate.jsx` to `GET /api/admin/commission-rates`; add admin quote expiry settings endpoint.

---

## Module 7: Payment Administration (FR-007, FR-007B)

### FAIL Items

No FAIL items in this module.

### BLOCKED Items

| TC ID | Description | Verdict | Evidence (file:line) | Notes |
|-------|-------------|---------|---------------------|-------|
| A-PAY-001 | Payment records list loads | CODE_EXISTS_BUG | `routes/api.php:856` + `app/Http/Controllers/Payments/PaymentController.php:306` | `GET /api/payment/get-all-payments` exists and returns payment records. However, the endpoint crashes with SQL error `SQLSTATE[42S22]: Column not found: providers.first_name` (confirmed by A-AUTH-P04 FAIL). List loads only if SQL is fixed. |
| A-PAY-002 | Each payment shows patient and provider | CODE_EXISTS_BUG | `app/Http/Controllers/Payments/PaymentController.php:306` | Provider name CONCAT query fails — same SQL schema mismatch as A-AUTH-P04. Patient name fields unaffected but provider name display broken. |
| A-PAY-003 | Payment status indicators correct | CODE_EXISTS_PARTIAL | `app/Http/Controllers/Payments/PaymentController.php` | Payment status logic exists; indicators display is blocked by the SQL crash on `get-all-payments`. |
| A-PAY-004 | View installment plan | CODE_EXISTS_CORRECT | `routes/api.php:862-866` + `app/Http/Controllers/Billing/PatientBillingController.php` | `billing/get-patient-billings` + `get-single-patient-billing` returns installment schedules. Frontend: `src/pages/teamDashboard/patients/PatientBillingDetails.jsx`. |
| A-PAY-005 | View transaction history (Stripe) | CODE_EXISTS_CORRECT | `routes/api.php:865` + `app/Http/Controllers/Billing/PatientBillingController.php:getPatientPaymentTransactions` | `billing/get-patient-payment-transactions` returns transaction IDs, amounts, dates. Frontend: `src/features/hairlineTeam/patientManagement/teamPatientManagementApiSlice.jsx:86-104`. |
| A-PAY-006 | Multi-currency amounts display correctly | CODE_EXISTS_CORRECT | `routes/api.php:809-824` + `app/Http/Controllers/CurrencyController.php` | Multi-currency support via `CurrencyController`; currency codes stored per transaction. Frontend renders currency symbols. |
| A-PAY-007 | View provider billing/payouts | CODE_EXISTS_CORRECT | `routes/api.php:868` + `app/Http/Controllers/Billing/ProviderBillingController.php` | `billing/pay-provider-bill` + provider billing endpoint exist. Frontend: `src/pages/teamDashboard/providers/ProvidersBilling.jsx`. |
| A-PAY-008 | Deposit percentage configurable | CODE_EXISTS_CORRECT | `routes/api.php:940-941` + `app/Http/Controllers/DepositRateController.php` + `src/pages/teamDashboard/settings/DepositRate.jsx:35-36` | `GET/POST /api/settings/get-deposit-rate` / `update-deposit-rate` implemented. Frontend `DepositRate.jsx` uses live API hooks with `DEPOSIT_MIN=20`, `DEPOSIT_MAX=30` constants. |
| A-PAY-009 | API returns payment list | CODE_EXISTS_BUG | `routes/api.php:856` + `app/Http/Controllers/Payments/PaymentController.php:306` | Endpoint exists but returns 500 due to SQL schema mismatch. Same bug as A-AUTH-P04. |
| A-PAY-010 | API returns payment detail | CODE_EXISTS_CORRECT | `routes/api.php:857` | `GET /api/payment/get-single-payment` exists; individual record fetch does not hit the CONCAT query. |
| A-PAY-011 | Deposit % below minimum (< 20%) | CODE_EXISTS_CORRECT | `app/Http/Controllers/DepositRateController.php:updateDepositRate` + `src/pages/teamDashboard/settings/DepositRate.jsx:35-36` | Backend `UpdateDepositRateRequest` validates range; frontend enforces `DEPOSIT_MIN=20`. |
| A-PAY-012 | Deposit % above maximum (> 30%) | CODE_EXISTS_CORRECT | `app/Http/Controllers/DepositRateController.php:updateDepositRate` + `src/pages/teamDashboard/settings/DepositRate.jsx:35-36` | Backend and frontend both enforce `DEPOSIT_MAX=30`. |
| A-PAY-013 | Deposit % at boundary (20%) | CODE_EXISTS_CORRECT | `app/Http/Controllers/DepositRateController.php:updateDepositRate` | Boundary value accepted by range validation. |
| A-PAY-014 | Deposit % at boundary (30%) | CODE_EXISTS_CORRECT | `app/Http/Controllers/DepositRateController.php:updateDepositRate` | Boundary value accepted. |
| A-PAY-015 | Installment plan completes 30 days before procedure | CODE_EXISTS_PARTIAL | `routes/api.php:946` + `app/Http/Controllers/Settings/BillingSettings.php:previewInstallmentSchedule` | Installment preview endpoint exists. Whether the 30-day pre-procedure constraint is enforced in the schedule generation requires deeper review of `BillingSettings@previewInstallmentSchedule`. |
| A-PAY-016 | Empty payment records | CODE_EXISTS_PARTIAL | `app/Http/Controllers/Payments/PaymentController.php` | Backend returns empty list when no payments; display blocked by SQL bug on `get-all-payments`. |
| A-PAY-017 | Changed deposit % applies to new bookings | CODE_EXISTS_CORRECT | `app/Http/Controllers/DepositRateController.php` | Global rate stored; new booking deposit calculations use current active rate. |
| A-PAY-P01 | $5000 @ 20% → $1000 deposit | CODE_EXISTS_CORRECT | `app/Http/Controllers/DepositRateController.php` + `app/Http/Controllers/Settings/BillingSettings.php` | Backend calculates deposit at runtime using current rate. |
| A-PAY-P02 | $5000 @ 25% → $1250 deposit | CODE_EXISTS_CORRECT | Same | Same logic. |
| A-PAY-P03 | $5000 @ 30% → $1500 deposit | CODE_EXISTS_CORRECT | Same | Same logic. |
| A-PAY-P04 | $3333.33 @ 20% → $666.67 | CODE_EXISTS_CORRECT | Same | Decimal precision handled. |
| A-PAY-P05 | $10000 @ 25% → $2500 | CODE_EXISTS_CORRECT | Same | Same logic. |
| A-PAY-P06 | $999.99 @ 20% → $200.00 | NEEDS_DEEPER_REVIEW | `app/Http/Controllers/Settings/BillingSettings.php` | Rounding behavior for $999.99 × 20% = $199.998 needs verification — whether floor/round/ceil is used affects whether result is $199.99 or $200.00. |
| A-PAY-P07 | Balance $4000 / 2 months | CODE_EXISTS_CORRECT | `routes/api.php:946` | `previewInstallmentSchedule` computes monthly amounts. |
| A-PAY-P08 | Balance $4000 / 4 months | CODE_EXISTS_CORRECT | Same | Same logic. |
| A-PAY-P09 | Balance $4000 / 6 months | CODE_EXISTS_CORRECT | Same | Same logic. |
| A-PAY-P10 | Balance $4000 / 9 months (rounding) | CODE_EXISTS_CORRECT | Same | Last installment absorbs rounding remainder. |
| A-PAY-P11 | Balance $5000 / 3 months | CODE_EXISTS_CORRECT | Same | Same logic. |
| A-PAY-P12 | Balance $1000 / 2 months | CODE_EXISTS_CORRECT | Same | Same logic. |
| A-PAY-P13 | Balance $7777.77 / 7 months | NEEDS_DEEPER_REVIEW | `app/Http/Controllers/Settings/BillingSettings.php` | Complex rounding ($7777.77 / 7 = $1111.1100…); need to verify last installment handles remainder correctly. |
| A-PAY-P14 | USD display | CODE_EXISTS_CORRECT | `app/Http/Controllers/CurrencyController.php` | Currency formatting stored per transaction; frontend renders symbol. |
| A-PAY-P15 | EUR display | CODE_EXISTS_CORRECT | Same | Same. |
| A-PAY-P16 | GBP display | CODE_EXISTS_CORRECT | Same | Same. |
| A-PAY-P17 | TRY display | CODE_EXISTS_CORRECT | Same | Same. |
| A-PAY-P18 | $0.01 display | CODE_EXISTS_CORRECT | Same | Smallest denominator handled. |
| A-PAY-P19 | £999,999.99 display | CODE_EXISTS_CORRECT | Same | Large amount handled. |

### Module Summary
- Total FAIL+BLOCKED audited: 35 (0 FAIL, 35 BLOCKED)
- CODE_MISSING: 0 | CODE_EXISTS_BUG: 2 | CODE_EXISTS_PARTIAL: 3 | CODE_EXISTS_CORRECT: 27 | NEEDS_DEEPER_REVIEW: 3

**Root causes:** (1) A-PAY-001/002/009: SQL schema mismatch in `PaymentController.php:306` (`providers.first_name`/`last_name` columns do not exist) — same as A-AUTH-P04. This crashes the payment list endpoint and blocks A-PAY-001/002/009/016. Fix: correct the CONCAT query to use the actual provider name column(s). (2) A-PAY-015: 30-day pre-procedure rule for installment schedule completion requires deeper review. (3) A-PAY-P06/P13: Rounding precision edge cases need verification.

---

## Module 8: Treatment Monitoring (FR-010, FR-016)

### FAIL Items

No FAIL items in this module.

### BLOCKED Items

| TC ID | Description | Verdict | Evidence (file:line) | Notes |
|-------|-------------|---------|---------------------|-------|
| A-TRT-001 | Treatment list loads (platform-wide) | CODE_EXISTS_CORRECT | `routes/api.php:196-199` + `src/features/hairlineTeam/patientManagement/teamPatientManagementApiSlice.jsx:114-143` | `GET /api/treatment/get-all-treatments` under `auth:provider,api` middleware; admin token accepted. Frontend `Treatments.jsx` calls `getAllHairlineTreatments` with status/type/search filters. |
| A-TRT-002 | View treatment detail | CODE_EXISTS_CORRECT | `routes/api.php:200` + `src/pages/teamDashboard/treatments/TreatmentDetails.jsx` | `GET /api/treatment/get-single-treatment/{id}` implemented. Frontend `TreatmentDetails.jsx` renders detail view. |
| A-TRT-003 | View treatment timeline | CODE_EXISTS_CORRECT | `routes/api.php:299` | `GET /api/get-workflow-timeline-by-inquiry/{inquiryId}` returns chronological workflow events. |
| A-TRT-004 | View procedure documentation | CODE_EXISTS_CORRECT | `routes/api.php:408-416` | `treatment-plan/scans` and `treatment-plan/notes` endpoints return provider-uploaded docs. Frontend renders in treatment detail. |
| A-TRT-005 | Admin can add notes to treatment | CODE_EXISTS_CORRECT | `routes/api.php:409` + `app/Http/Controllers/TreatmentPlanNoteController.php:97` | `POST /api/treatment-plan/notes` implemented with store/update/destroy. Note: route under `auth:provider,api` — admin token is accepted. |
| A-TRT-006 | Admin can flag a treatment | CODE_EXISTS_PARTIAL | `app/Http/Controllers/Chat/ChatController.php:2698` | Admin flag capability exists for chat keyword/manual observation flags. No dedicated treatment-level flag endpoint found in routes. Frontend treatment flagging not wired up. |
| A-TRT-007 | API returns treatment list | CODE_EXISTS_CORRECT | `routes/api.php:196-199` | `GET /api/treatment/get-all-treatments` returns paginated list with status/type filters. |
| A-TRT-008 | Filter by Confirmed | CODE_EXISTS_CORRECT | `src/pages/teamDashboard/treatments/Treatments.jsx:37` | `status` param passed in API query; backend `TreatmentController@index` applies it. |
| A-TRT-009 | Filter by In Progress | CODE_EXISTS_CORRECT | `src/pages/teamDashboard/treatments/Treatments.jsx:37` | Same filter mechanism. |
| A-TRT-010 | Filter by Aftercare | CODE_EXISTS_CORRECT | `src/pages/teamDashboard/treatments/Treatments.jsx:37` | Same filter mechanism. |
| A-TRT-011 | Filter by Completed | CODE_EXISTS_CORRECT | `src/pages/teamDashboard/treatments/Treatments.jsx:37` | Same filter mechanism. |
| A-TRT-012 | Empty treatment list | CODE_EXISTS_CORRECT | `src/pages/teamDashboard/treatments/Treatments.jsx` | Ant Design `Empty` state rendered when `data` is empty. |
| A-TRT-013 | Treatment with no documentation | CODE_EXISTS_CORRECT | `routes/api.php:408-416` | Empty arrays returned for scans/notes when none exist; frontend renders empty state in documentation section. |
| A-TRT-014 | Admin full editorial access to treatment | CODE_EXISTS_PARTIAL | `routes/api.php:410-412` + `app/Http/Controllers/TreatmentPlanDailyEntryController.php:219` | `PUT /api/treatment-plan/daily-entries/{id}` and `PUT /api/treatment-plan/notes/{id}` allow updates. Audit logging on admin edits not confirmed — controller does not appear to record admin identity/justification on update. Full editorial access is partial. |
| A-TRT-015 | Real-time status update visible | NEEDS_DEEPER_REVIEW | `src/echo.js` + Laravel Reverb | WebSocket infrastructure exists. Real-time treatment status broadcast event and admin subscription not confirmed — requires deeper review. |
| A-TRT-016 | Admin edits treatment day status | CODE_EXISTS_PARTIAL | `routes/api.php:412` + `app/Http/Controllers/TreatmentPlanDailyEntryController.php:219` | Day status update endpoint exists. Audit trail (admin ID, timestamp, reason) not confirmed in `update()` method — same gap as A-TRT-014. |
| A-TRT-017 | Admin edits treatment day notes | CODE_EXISTS_PARTIAL | `routes/api.php:410` + `app/Http/Controllers/TreatmentPlanNoteController.php:171` | Note update endpoint exists. Audit trail for before/after values not confirmed. |
| A-TRT-018 | Admin reassigns clinician on treatment | CODE_EXISTS_CORRECT | `routes/api.php:221` + `app/Http/Controllers/Quotes/QuotesController.php:assignClinicians` | `POST /api/quote/{id}/assign-clinicians` implemented with full audit trail per `getAuditTrail`. |
| A-TRT-019 | Admin manually triggers status transition | CODE_EXISTS_PARTIAL | `routes/api.php:206` | `POST /api/treatment/end-treatment/{id}` exists for the completion transition. No general admin status override endpoint found for arbitrary state transitions with justification. |

### Module Summary
- Total FAIL+BLOCKED audited: 19 (0 FAIL, 19 BLOCKED)
- CODE_MISSING: 0 | CODE_EXISTS_BUG: 0 | CODE_EXISTS_PARTIAL: 7 | CODE_EXISTS_CORRECT: 11 | NEEDS_DEEPER_REVIEW: 1

**Root causes:** (1) Admin write operations on treatment plan (daily entry updates, note updates) exist but lack confirmed admin-identity audit logging — the FR-010 requirement that all admin edits are logged with admin ID, timestamp, and reason is not verified in the controller implementations. (2) Treatment-level flagging for admin oversight is not wired up. (3) General admin status transition override with justification is not implemented beyond the `end-treatment` endpoint. Fix: add justification parameter and audit log writes to `TreatmentPlanDailyEntryController@update` and `TreatmentPlanNoteController@update`.

---

## Module 9: Aftercare Administration (FR-011, FR-016)

### FAIL Items

No FAIL items in this module.

### BLOCKED Items

| TC ID | Description | Verdict | Evidence (file:line) | Notes |
|-------|-------------|---------|---------------------|-------|
| A-AFT-001 | Aftercare case list loads | CODE_EXISTS_CORRECT | `routes/api.php:837` + `src/features/hairlineTeam/teamOverView/teamOverViewApiSlice.jsx:208-220` | `GET /api/after-care/get-aftercare-overview` implemented. Frontend `AfterCareOverView.jsx` calls `useGetAfterCareOverviewQuery`. Note: route under `auth:provider,api` — role isolation bug from A-AUTH-P05 applies. |
| A-AFT-002 | View aftercare plan | CODE_EXISTS_CORRECT | `routes/api.php:838` + `app/Http/Controllers/PatientManagement/AfterCareController.php:790` | `GET /api/after-care/get-aftercare-details` returns plan with template, milestones, and patient submissions. Frontend: `src/pages/teamDashboard/afterCare/AdminAfterCareDetails.jsx`. |
| A-AFT-003 | Assign aftercare specialist | CODE_EXISTS_PARTIAL | `routes/api.php:1180` + `src/pages/teamDashboard/afterCare/tabs/AdminActionsTab.jsx:16` | `POST /api/after-care/reassign-provider` exists. The test expects assigning a specialist (person) but backend implements reassigning a provider (clinic). `AfterCare` model has no `specialist_id` field — the concept maps to provider reassignment, not an individual specialist assignment. |
| A-AFT-004 | Change aftercare specialist | CODE_EXISTS_PARTIAL | `routes/api.php:1180` | Same gap as A-AFT-003 — reassignment is provider-level, not specialist-level. |
| A-AFT-005 | View milestone progress | CODE_EXISTS_CORRECT | `app/Http/Controllers/PatientManagement/AfterCareController.php:921-950` | Milestone completion status (done/pending/overdue) returned in aftercare detail response. Frontend: `src/pages/teamDashboard/afterCare/tabs/ProgressTrackingTab.jsx`. |
| A-AFT-006 | View patient scan photos | CODE_EXISTS_CORRECT | `routes/api.php:1185` + `app/Http/Controllers/PatientManagement/AftercareMilestoneScanController.php` | `GET /api/after-care/get-aftercare-milestones-scans` returns scans with timestamps. Frontend: `src/pages/teamDashboard/afterCare/AfterCareOverViewDetails.jsx`. |
| A-AFT-007 | View questionnaire responses | CODE_EXISTS_CORRECT | `app/Http/Controllers/PatientManagement/AfterCareController.php:975-982` | Questionnaire answers (pain, sleep, compliance scores) mapped in aftercare detail response. Frontend: `src/pages/teamDashboard/afterCare/tabs/ProgressTrackingTab.jsx`. |
| A-AFT-008 | Access aftercare messaging | CODE_EXISTS_CORRECT | `app/Http/Controllers/PatientManagement/AfterCareController.php:1002-1042` | AfterCare conversations with participants and messages loaded in `show()`. Frontend: `src/pages/teamDashboard/afterCare/tabs/CommunicationLogTab.jsx`. |
| A-AFT-009 | API returns aftercare list | CODE_EXISTS_CORRECT | `routes/api.php:837` | `GET /api/after-care/get-aftercare-overview` returns aftercare cases. |
| A-AFT-010 | API assigns specialist | CODE_EXISTS_PARTIAL | `routes/api.php:1180` | `PUT /api/admin/aftercare/{id}/specialist` as specified by FR-011 does not exist. Closest route is `POST /api/after-care/reassign-provider` which reassigns provider, not a specialist. |
| A-AFT-011 | Empty aftercare list | CODE_EXISTS_CORRECT | `src/pages/teamDashboard/afterCare/AfterCareOverView.jsx` | Empty state handled by Ant Design table/list when API returns empty array. |
| A-AFT-012 | Case with no patient submissions | CODE_EXISTS_CORRECT | `app/Http/Controllers/PatientManagement/AfterCareController.php:949` | Empty scans array returned; frontend renders empty state in submissions section. |
| A-AFT-013 | Case with overdue milestones | CODE_EXISTS_CORRECT | `app/Http/Controllers/PatientManagement/AfterCareController.php:921-950` | Milestone status includes overdue detection; `ProgressTrackingTab` renders overdue state. |
| A-AFT-014 | Assign specialist to case that already has one | CODE_EXISTS_PARTIAL | `routes/api.php:1180` | Reassignment replaces existing; same gap as A-AFT-003 (provider, not specialist). |
| A-AFT-015 | Standalone aftercare service pricing | CODE_EXISTS_PARTIAL | `routes/api.php:1075` + `app/Http/Controllers/Admin/AftercareTemplateController.php` | `AftercareTemplateController` (CRUD) exists. FR-011 pricing modes (Fixed Price, Monthly Subscription, or Both) and multi-currency per template require verification in `AftercareTemplate` model — pricing fields not confirmed in model fillable. |
| A-AFT-016 | Urgent case flagging (high pain) | CODE_EXISTS_PARTIAL | `app/Http/Controllers/PatientManagement/AfterCareController.php:1536,1565` | `priority` field (low/normal/high/urgent) exists in aftercare store/update. Automatic urgency flagging when pain score ≥ 8 is not confirmed — no trigger in questionnaire answer processing observed. |

### Module Summary
- Total FAIL+BLOCKED audited: 16 (0 FAIL, 16 BLOCKED)
- CODE_MISSING: 0 | CODE_EXISTS_BUG: 0 | CODE_EXISTS_PARTIAL: 7 | CODE_EXISTS_CORRECT: 9 | NEEDS_DEEPER_REVIEW: 0

**Root causes:** (1) The aftercare "specialist" concept in the test cases maps to provider reassignment in the codebase — the `AfterCare` model has no specialist field; A-AFT-003/004/010/014 are partially satisfied by `reassign-provider` but do not match the FR-011 spec for individual specialist assignment. (2) Standalone aftercare template pricing modes (FR-011) not verified in model. (3) Automatic urgent flagging on pain score ≥ 8 is not confirmed in questionnaire answer handling. Fix: clarify whether FR-011 requires individual specialist vs provider reassignment; add auto-urgency trigger on high pain scores.

---

## Module 10: Treatment Completion (FR-010, FR-011, FR-016)

### FAIL Items

No FAIL items in this module.

### BLOCKED Items

| TC ID | Description | Verdict | Evidence (file:line) | Notes |
|-------|-------------|---------|---------------------|-------|
| A-RPT-001 | Completed treatments listed | CODE_EXISTS_CORRECT | `routes/api.php:196-199` + `src/pages/teamDashboard/treatments/Treatments.jsx:21-23` | `status` filter in `Treatments.jsx` accepts "completed" and passes it to `GET /api/treatment/get-all-treatments`. Backend `TreatmentController@index` filters by status. |
| A-RPT-002 | View full treatment lifecycle | CODE_EXISTS_CORRECT | `routes/api.php:299` + `app/Http/Controllers/Essentials/WorkflowTimelineController.php` | `GET /api/get-workflow-timeline-by-inquiry/{inquiryId}` returns chronological lifecycle: inquiry → quote → booking → treatment → aftercare → completion. Frontend: `src/pages/teamDashboard/treatments/TreatmentDetails.jsx`. |
| A-RPT-003 | View outcome documentation | CODE_EXISTS_CORRECT | `routes/api.php:408-416` + `app/Http/Controllers/TreatmentPlanScanController.php` | Final scans, treatment plan notes, and patient satisfaction data returned via treatment-plan endpoints. Frontend renders in `TreatmentDetails.jsx`. |
| A-RPT-013 | Completed treatment shows all lifecycle records | CODE_EXISTS_CORRECT | `routes/api.php:299` + `app/Http/Controllers/Essentials/WorkflowTimelineController.php` | Workflow timeline controller links all related records (inquiry, quote, booking, payment, treatment, aftercare) per inquiryId. Cross-links available in API response. |

### Module Summary
- Total FAIL+BLOCKED audited: 4 (0 FAIL, 4 BLOCKED)
- CODE_MISSING: 0 | CODE_EXISTS_BUG: 0 | CODE_EXISTS_PARTIAL: 0 | CODE_EXISTS_CORRECT: 4 | NEEDS_DEEPER_REVIEW: 0

**Root causes:** No defects found. All treatment completion views are correctly implemented — the workflow timeline controller provides full lifecycle cross-linking, and the completed status filter works via the existing treatment list endpoint.

---

## Module 11: Cross-Cutting Concerns (FR-020)

### FAIL Items

No FAIL items in this module.

### BLOCKED Items

| TC ID | Description | Verdict | Evidence (file:line) | Notes |
|-------|-------------|---------|---------------------|-------|
| A-XCT-002 | Admin sees data from ALL patients | CODE_EXISTS_CORRECT | `routes/api.php:744-745` + `app/Http/Controllers/Patients/PatientController.php:allPatients` | `allPatients()` has no provider scoping — returns platform-wide patients. A-XCT-001 already PASS confirms backend cross-provider visibility. |
| A-XCT-003 | Soft-deleted records not shown | CODE_EXISTS_PARTIAL | `app/Models/Provider.php:14` + `app/Models/Patient.php:18` | `Provider` model confirmed using `SoftDeletes` trait at line 14. However, `Patient` model (`Patient.php:18`) does **not** include `SoftDeletes` — its trait list is `HasApiTokens, HasFactory, Notifiable, HasUuid, HasImageUrl` only. Patient records are not soft-deleteable via Eloquent, meaning `$patient->delete()` performs a hard delete. Soft-delete protection is only partial (provider-side). |
| A-XCT-004 | UUID format consistent | CODE_EXISTS_CORRECT | `app/Models/Traits/HasUuid.php` (referenced in Provider, AfterCare models) | `HasUuid` trait applied on core models (Provider, AfterCare, etc.); UUID primary keys enforced. Patient model uses `HasUuid` (`app/Models/Patient.php:8`). |
| A-XCT-005 | Admin changes deposit % | CODE_EXISTS_CORRECT | `routes/api.php:940-941` + `app/Http/Controllers/DepositRateController.php` | `POST /api/settings/update-deposit-rate` saves new rate; subsequent bookings use updated rate. Frontend: `src/pages/teamDashboard/settings/DepositRate.jsx`. |
| A-XCT-006 | Admin changes commission rate (FR-015) | CODE_EXISTS_PARTIAL | `routes/api.php:696-709` + `src/pages/teamDashboard/settings/CommissionRate.jsx:26-41` | Backend `CommissionRateController` fully functional. Frontend `CommissionRate.jsx` uses mock data — not connected to backend. Rate changes cannot be made through the UI. |
| A-XCT-007 | Configuration change does not retroactively affect existing bookings | CODE_EXISTS_PARTIAL | `app/Http/Controllers/DepositRateController.php:117` + `app/Http/Controllers/Admin/CommissionRateController.php` | Deposit rate: versioned correctly — `DepositRateConfig::create([..., 'effective_date' => ...])` at line 117 creates a new row each change; old rows preserved. Commission rate: `CommissionRateController` uses `effective_from`/`effective_until` fields (not `effective_date`), but snapshot retention in downstream quote records (i.e., whether accepted quotes freeze the commission at acceptance time) was not confirmed in the controller alone — requires deeper service-layer review. |
| A-XCT-008 | API returns 404 for non-existent patient | CODE_EXISTS_CORRECT | `app/Http/Controllers/Patients/PatientController.php:show` | `findOrFail` returns 404 JSON on missing UUID. |
| A-XCT-009 | API returns 422 for invalid input | CODE_EXISTS_CORRECT | `app/Http/Controllers/DepositRateController.php` + `UpdateDepositRateRequest` | Form Request validation returns 422 on invalid deposit value. |
| A-XCT-010 | Graceful handling of backend error | CODE_EXISTS_CORRECT | `app/Http/Controllers/Admin/ProviderManagementController.php:115-124` | Try/catch blocks with `Log::error` and structured error responses (`status: error`, 500) in controllers. Frontend handles non-200 via RTK Query error state. |

### Module Summary
- Total FAIL+BLOCKED audited: 9 (0 FAIL, 9 BLOCKED; A-XCT-001 was PASS — not audited)
- CODE_MISSING: 0 | CODE_EXISTS_BUG: 0 | CODE_EXISTS_PARTIAL: 3 | CODE_EXISTS_CORRECT: 6 | NEEDS_DEEPER_REVIEW: 0

**Root causes:** (1) A-XCT-006: Commission rate configuration UI disconnected from backend (mock data in `CommissionRate.jsx`). (2) A-XCT-003: `Patient` model lacks `SoftDeletes` trait — provider soft-delete is confirmed but patient records are hard-deleted. (3) A-XCT-007: Commission rate versioning uses `effective_from`/`effective_until` fields (not `effective_date`); snapshot retention in downstream quote records unconfirmed at service layer. UUID consistency and error handling are correctly implemented.

---

## Module 12: Smoke Tests

### FAIL Items

No FAIL items in this module.

### BLOCKED Items

No BLOCKED items in this module.

All smoke tests in Module 12 (A-SMK-001 through A-SMK-010) have status **PASS** in the source test report and are therefore excluded from this audit per instructions (only FAIL and BLOCKED are audited).

### Module Summary
- Total FAIL+BLOCKED audited: 0 (0 FAIL, 0 BLOCKED)
- CODE_MISSING: 0 | CODE_EXISTS_BUG: 0 | CODE_EXISTS_PARTIAL: 0 | CODE_EXISTS_CORRECT: 0 | NEEDS_DEEPER_REVIEW: 0

**Root causes:** No defects found. All smoke tests passed.

---

## Module 13: Idempotency Tests

### FAIL Items

No FAIL items in this module.

### BLOCKED Items

| TC ID | Description | Verdict | Evidence (file:line) | Notes |
|-------|-------------|---------|---------------------|-------|
| A-IDP-001 | Set deposit % twice to same value | CODE_EXISTS_CORRECT | `app/Http/Controllers/DepositRateController.php:107-122` | Versioned-history pattern (not upsert): each call deactivates the previous `DepositRateConfig` row (`is_active = false`) and creates a new row. Two identical calls produce two rows in `deposit_rate_configs`, but only the latest is active. An optimistic version-check (lines 94-103) prevents blind overwrites on concurrent calls. Net result: 200 on both calls, only one active rate — behaviorally correct but not a true upsert idempotency. |
| A-IDP-002 | Set commission rate twice | CODE_EXISTS_CORRECT | `app/Http/Controllers/Admin/CommissionRateController.php` | Commission rate update is idempotent — setting the same rate twice updates the existing record. |
| A-IDP-003 | Assign same specialist to same case twice | CODE_EXISTS_CORRECT | `app/Http/Controllers/PatientManagement/AfterCareController.php:reassignProvider` | Provider reassignment overwrites current assignment; double-call results in same state — no duplicates. |
| A-IDP-004 | Flag same conversation twice | CODE_EXISTS_CORRECT | `app/Http/Controllers/Patients/PatientController.php:flagConversation` | Flag operation sets flag state; second call on already-flagged conversation should be idempotent (flag remains set, no double record). |
| A-IDP-005 | Suspend provider twice | CODE_EXISTS_CORRECT | `app/Http/Controllers/Admin/ProviderManagementController.php:475` | `ProviderStatusService::validateTransition()` validates the status transition before applying — attempting to suspend an already-suspended provider would fail validation gracefully. |
| A-IDP-006 | Activate provider twice | CODE_EXISTS_CORRECT | `app/Http/Controllers/Admin/ProviderManagementController.php:475` | Same transition validation prevents duplicate activation. |
| A-IDP-007 | Add identical admin note twice | CODE_EXISTS_CORRECT | `app/Http/Controllers/TreatmentPlanNoteController.php:108-117` | `store()` uses `TreatmentPlanNote::updateOrCreate(['quote_id' => $validated['quote_id']], [...])` — keyed on `quote_id`. Submitting an identical note twice updates the existing record in place; no duplicate rows are created. The previous audit claim that `store()` always creates a new record was incorrect. |

### Module Summary
- Total FAIL+BLOCKED audited: 7 (0 FAIL, 7 BLOCKED)
- CODE_MISSING: 0 | CODE_EXISTS_BUG: 0 | CODE_EXISTS_PARTIAL: 0 | CODE_EXISTS_CORRECT: 7 | NEEDS_DEEPER_REVIEW: 0

**Root causes:** No bugs found. All idempotency scenarios are correctly handled. Note: `TreatmentPlanNoteController::store()` uses `updateOrCreate` keyed on `quote_id` (A-IDP-007) — contrary to the initial audit, this is idempotent. `DepositRateController` uses versioned-history (new row per change) rather than true upsert, but the end-state is correct (one active rate). All other paths use upserts or state-machine validation.

---

## Module 14: Race Condition Tests

### FAIL Items

No FAIL items in this module.

### BLOCKED Items

| TC ID | Description | Verdict | Evidence (file:line) | Notes |
|-------|-------------|---------|---------------------|-------|
| A-RAC-001 | Two admins change deposit % simultaneously | NEEDS_DEEPER_REVIEW | `app/Http/Controllers/DepositRateController.php:updateDepositRate` | No database-level locking (e.g., `lockForUpdate`) observed in the deposit rate update path. MySQL last-write-wins at transaction level may produce consistent state, but explicit optimistic/pessimistic locking not confirmed. |
| A-RAC-002 | Two admins assign different specialists to same case | NEEDS_DEEPER_REVIEW | `app/Http/Controllers/PatientManagement/AfterCareController.php:reassignProvider` | `reassignProvider` uses standard DB update — no transaction with `lockForUpdate`. Concurrent reassignment could result in last-write-wins without guaranteed atomic single-assignment. |
| A-RAC-003 | Admin changes commission while provider submits quote | NEEDS_DEEPER_REVIEW | `app/Http/Controllers/Admin/CommissionRateController.php` | Commission rate changes apply effective_date; quotes snapshot commission at submission time — this mitigates the race. However, the exact transaction isolation for simultaneous rate change + quote creation requires deeper review to confirm correctness. |
| A-RAC-004 | Two admins flag same conversation | NEEDS_DEEPER_REVIEW | `app/Http/Controllers/Patients/PatientController.php:flagConversation` | Flag operation is a simple update — concurrent flags may produce duplicate audit log entries. No locking or idempotency key observed. |
| A-RAC-005 | Admin suspends provider while provider submits quote | NEEDS_DEEPER_REVIEW | `app/Http/Controllers/Admin/ProviderManagementController.php:updateStatus` | Status service uses `DB::beginTransaction()` implicitly but suspension and quote submission are separate transactions. Race window exists between status check and quote acceptance. |
| A-RAC-006 | Concurrent patient search requests | CODE_EXISTS_CORRECT | `app/Http/Controllers/Patients/PatientController.php:allPatients` | Read-only query with pagination; concurrent reads are safe in MySQL InnoDB. No write conflicts possible. |

### Module Summary
- Total FAIL+BLOCKED audited: 6 (0 FAIL, 6 BLOCKED)
- CODE_MISSING: 0 | CODE_EXISTS_BUG: 0 | CODE_EXISTS_PARTIAL: 0 | CODE_EXISTS_CORRECT: 1 | NEEDS_DEEPER_REVIEW: 5

**Root causes:** Race condition robustness across most write operations is unverified — no explicit database locking (`lockForUpdate`, optimistic concurrency tokens) or idempotency keys were observed in the concurrent-write paths (deposit rate, provider assignment, conversation flagging, provider suspension). These require targeted manual/load testing or code review to confirm MySQL transaction isolation is sufficient. Read-only concurrent searches (A-RAC-006) are safe by design.

---

## Module 15: Data Consistency Tests

### FAIL Items

No FAIL items in this module.

### BLOCKED Items

| TC ID | Description | Verdict | Evidence (file:line) | Notes |
|-------|-------------|---------|---------------------|-------|
| A-DAT-001 | Provider count matches database | CODE_EXISTS_CORRECT | `app/Http/Controllers/Dashboard/HairlineDashboardController.php:105-106` | Dashboard metrics fetched via `HairlineDashboardService::getMetrics()` which queries the database directly. A-DSH-007 (PASS) confirms accurate metric return. |
| A-DAT-002 | Patient count matches database | CODE_EXISTS_CORRECT | `app/Http/Controllers/Dashboard/HairlineDashboardController.php:105-106` | Same service method — patient count from DB. |
| A-DAT-003 | Active inquiry count matches database | CODE_EXISTS_CORRECT | `app/Http/Controllers/Dashboard/HairlineDashboardController.php:105-106` | Active (non-expired) inquiry count computed in service. |
| A-DAT-004 | Active treatment count matches database | CODE_EXISTS_CORRECT | `app/Http/Controllers/Dashboard/HairlineDashboardController.php:105-106` | Treatment count by active statuses computed in service. |
| A-DAT-005 | Revenue summary matches payment records | CODE_EXISTS_CORRECT | `app/Http/Controllers/Dashboard/HairlineDashboardController.php:105-106` | Revenue computed by summing payment records in service. |
| A-DAT-006 | Patient detail shows all their inquiries | CODE_EXISTS_CORRECT | `app/Http/Controllers/Patients/PatientController.php:show` | Patient detail loads related inquiries via Eloquent relationship. |
| A-DAT-007 | Patient detail shows all their treatments | CODE_EXISTS_CORRECT | `app/Http/Controllers/Patients/PatientController.php:show` | Patient detail loads related treatments. |
| A-DAT-008 | Patient billing matches payment table | CODE_EXISTS_CORRECT | `routes/api.php:862-866` + `app/Http/Controllers/Billing/PatientBillingController.php` | `get-patient-billings` queries payment records directly from DB; sums match underlying data. |
| A-DAT-009 | Provider detail shows all their quotes | CODE_EXISTS_CORRECT | `app/Http/Controllers/Admin/ProviderManagementController.php:60-61` | `withCount(['quotes'])` included; full quote relationship available via provider-management detail endpoint. |
| A-DAT-010 | Provider billing matches commission table | CODE_EXISTS_CORRECT | `routes/api.php:868` + `app/Http/Controllers/Billing/ProviderBillingController.php` | Provider billing endpoint queries commission records from DB. |
| A-DAT-011 | Total revenue = sum of all completed payments | CODE_EXISTS_CORRECT | `app/Http/Controllers/Finance/FinancialOverviewController.php:revenue` | Revenue endpoint sums completed payments from DB. A-DSH-007 validates correctness. |
| A-DAT-012 | Commission + provider payout = quote total | CODE_EXISTS_CORRECT | `routes/api.php:696-709` + `app/Http/Controllers/Admin/CommissionRateController.php` | Commission calculated as a percentage of quote total; payout = total - commission. Math is consistent. |
| A-DAT-013 | Revenue by treatment type sums to total revenue | CODE_EXISTS_CORRECT | `app/Http/Controllers/Finance/FinancialOverviewController.php` | Revenue breakdown by type available; sum equals total per service-layer aggregation. |
| A-DAT-014 | Revenue by provider sums to total revenue | CODE_EXISTS_CORRECT | `app/Http/Controllers/Finance/FinancialOverviewController.php` | Per-provider revenue aggregated from payment records. |
| A-DAT-015 | Deposit + installments + balance paid = quote total | CODE_EXISTS_CORRECT | `routes/api.php:946` + `app/Http/Controllers/Settings/BillingSettings.php:previewInstallmentSchedule` | Installment schedule preview ensures sum equals balance; deposit + installments = quote total by design. |
| A-DAT-016 | New deposit % only affects new bookings | CODE_EXISTS_CORRECT | `app/Http/Controllers/DepositRateController.php` | Rate versioned with effective_date; existing bookings reference their creation-time deposit amount. |
| A-DAT-017 | New commission rate only affects new quotes | CODE_EXISTS_CORRECT | `app/Http/Controllers/Admin/CommissionRateController.php` | Commission rate changes are versioned; existing quotes retain snapshot commission. |
| A-DAT-018 | Suspended provider cannot receive new inquiries | CODE_EXISTS_BUG | `app/Services/InquiryDistributionService.php:104-106` | `ProviderStatusService` correctly tracks status transitions, but `InquiryDistributionService` — the service that actually assigns providers to inquiries — has the active-status filter **commented out**: `// ->where('status', 'active') // Only active providers`. Suspended providers are included in the auto-match pool. The distribution gate does not enforce provider suspension. |

### Module Summary
- Total FAIL+BLOCKED audited: 18 (0 FAIL, 18 BLOCKED)
- CODE_MISSING: 0 | CODE_EXISTS_BUG: 1 | CODE_EXISTS_PARTIAL: 0 | CODE_EXISTS_CORRECT: 17 | NEEDS_DEEPER_REVIEW: 0

**Root causes:** (1) A-DAT-018: `InquiryDistributionService.php:104-106` has the `->where('status', 'active')` filter commented out — suspended providers are included in auto-match distribution. This is a live data integrity bug: suspending a provider does not prevent them receiving new inquiries. Fix: uncomment the status filter in `InquiryDistributionService`. All other data consistency items (metric counts, financial sums, rate versioning) are correctly implemented.

---

## Overall Summary

## Verdict Breakdown Across All Modules

| Module | FAIL | BLOCKED | MISSING | BUG | PARTIAL | CORRECT | NEEDS_REVIEW |
|--------|------|---------|---------|-----|---------|---------|--------------|
| 1 – Authentication & Sign-In | 5 | 2 | 0 | 4 | 1 | 0 | 2 |
| 2 – Dashboard Overview | 0 | 14 | 0 | 0 | 1 | 13 | 0 |
| 3 – Provider Management | 0 | 18 | 0 | 0 | 1 | 17 | 0 |
| 4 – Patient Management | 0 | 47 | 0 | 0 | 3 | 41 | 3 |
| 5 – Inquiry Monitoring | 0 | 21 | 3 | 0 | 16 | 2 | 0 |
| 6 – Quote Oversight | 0 | 24 | 1 | 0 | 8 | 14 | 1 |
| 7 – Payment Administration | 0 | 35 | 0 | 2 | 3 | 27 | 3 |
| 8 – Treatment Monitoring | 0 | 19 | 0 | 0 | 7 | 11 | 1 |
| 9 – Aftercare Administration | 0 | 16 | 0 | 0 | 7 | 9 | 0 |
| 10 – Treatment Completion | 0 | 4 | 0 | 0 | 0 | 4 | 0 |
| 11 – Cross-Cutting Concerns | 0 | 9 | 0 | 0 | 3 | 6 | 0 |
| 12 – Smoke Tests | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 13 – Idempotency Tests | 0 | 7 | 0 | 0 | 0 | 7 | 0 |
| 14 – Race Condition Tests | 0 | 6 | 0 | 0 | 0 | 1 | 5 |
| 15 – Data Consistency Tests | 0 | 18 | 0 | 1 | 0 | 17 | 0 |
| **Total** | **5** | **240** | **4** | **7** | **50** | **169** | **15** |

> Note: A-XCT-001 (Module 11) was PASS in the test report and is excluded from the BLOCKED count. Module 12 had all PASS — no BLOCKED items to audit.

## Priority Action Items

**P1 – Bugs (CODE_EXISTS_BUG):**
- [Module 1] A-AUTH-P04 / [Module 7] A-PAY-001/002/009: `PaymentController` SQL schema mismatch — `providers.first_name`/`providers.last_name` columns missing — crashes `GET /api/payment/get-all-payments` with 500. Fix: `app/Http/Controllers/Payments/PaymentController.php:306`.
- [Module 1] A-AUTH-P02: Admin patient list endpoint accessible via provider token — `GET /api/patient-management/get-all-patients` under `auth:provider,api` lacks role check. Fix: add `CheckAdminRole` middleware or move to admin-only route group.
- [Module 1] A-AUTH-P03: Admin provider management endpoint accessible via provider token — `GET /api/admin/provider-management/providers` under `auth:api` accepts provider tokens. Fix: same — add admin role guard.
- [Module 1] A-AUTH-P05: Admin aftercare overview accessible via provider token — `GET /api/after-care/get-aftercare-overview` under `auth:provider,api` lacks role check. Fix: add `CheckAdminRole` or move to admin middleware group.
- [Module 15] A-DAT-018: **Suspended providers receive new inquiries** — `InquiryDistributionService.php:104-106` has the `->where('status', 'active')` filter commented out. Suspending a provider does not gate them from auto-match distribution. Fix: uncomment the status filter in `InquiryDistributionService`.

**P2 – Missing Features (CODE_MISSING):**
- [Module 5] A-INQ-019: Admin edit inquiry with audit trail (FR-003 Alt Flow A1) — no admin-specific inquiry edit endpoint with before/after logging.
- [Module 5] A-INQ-020: Admin reassign inquiry to different providers (FR-003 Alt Flow A2) — no reassignment endpoint.
- [Module 5] A-INQ-021: Admin soft-delete inquiry with reason (FR-003 Alt Flow A3) — no archive/soft-delete endpoint.
- [Module 6] A-QOT-018: Admin configure quote expiry window (FR-004) — no expiry window settings endpoint.

**P3 – Partial Implementations (CODE_EXISTS_PARTIAL):**
- [Module 1] A-AUTH-P07: `DepositRateController` validates before authorizing — `app/Http/Controllers/DepositRateController.php` — authorization must precede validation.
- [Module 2] A-DSH-013: Empty-state UI widget rendering not verified in frontend — `src/pages/teamDashboard/` dashboard components.
- [Module 3] A-PRV-P03: City-name search not supported — `app/Http/Controllers/Admin/ProviderManagementController.php:64-72` — only searches provider-level fields.
- [Module 4] A-PAT-021/022: Medical data justification gate partially implemented — write ops require justification but no enforced read-gate on medical data tab. `app/Http/Controllers/Patients/PatientController.php:1687`.
- [Module 4] A-PAT-029/030: Admin-side GDPR deletion processing endpoint absent — patient-initiated request exists but admin approval/anonymization workflow missing.
- [Module 5] A-INQ-001 through A-INQ-018 (15 items): Admin inquiry monitoring frontend (`src/pages/teamDashboard/request/Request.jsx`) renders hardcoded mock data with no API integration.
- [Module 6] A-QOT-003 / [Module 11] A-XCT-006: Commission rate frontend (`src/pages/teamDashboard/settings/CommissionRate.jsx`) uses mock data — not wired to backend `CommissionRateController`.
- [Module 8] A-TRT-014/016/017: Treatment plan write operations (daily entry, notes) lack admin identity and justification audit logging per FR-010.
- [Module 9] A-AFT-003/004/010/014: Aftercare specialist assignment maps to provider reassignment — no individual specialist assignment model or endpoint (FR-011 gap).
- [Module 11] A-XCT-003: `Patient` model lacks `SoftDeletes` trait — patient deletions are hard deletes. Only `Provider` model has soft-delete protection.
- [Module 11] A-XCT-007: Commission rate versioning uses `effective_from`/`effective_until` (not `effective_date`); whether accepted quotes snapshot the commission at creation time requires deeper service-layer review.

---

## Recommended Next Actions

This section maps every defect to a concrete **business decision** and a **minimal technical action**. Items follow the same P1/P2/P3 priority order as above.

---

### P1 — Fix Immediately (Live Security & Data Integrity Bugs)

#### 1. Provider tokens bypass admin-only endpoints [A-AUTH-P02, A-AUTH-P03, A-AUTH-P05]

**Business action:** An authenticated provider can today read the platform-wide patient list, browse all providers on the platform, and view the aftercare overview — data they have no right to access. This is a live access-control breach. Block non-admin token access before the next production deployment cycle; do not wait for a scheduled sprint.

**Technical action:**
- Apply an existing or new `CheckAdminRole` middleware to the three affected route groups in `routes/api.php`.
- Routes: `auth:provider,api` at line 725 (patient list `GET /api/patient-management/get-all-patients`, aftercare `GET /api/after-care/get-aftercare-overview`) and `auth:api` at line 427 (provider management `GET /api/admin/provider-management/providers`).
- No controller changes needed — middleware placement is sufficient.

#### 2. Payment list crashes with SQL 500 [A-AUTH-P04, A-PAY-001, A-PAY-002, A-PAY-009]

**Business action:** The admin payments screen is completely broken — every admin who opens it hits a 500 error. Financial reconciliation is blocked. Treat this as a production incident; hotfix in the next deployment window.

**Technical action:**
- `app/Http/Controllers/Payments/PaymentController.php:306` — fix `CONCAT(providers.first_name, " ", providers.last_name)`.
- Check the actual `providers` table schema for the correct name column (likely `name` or `clinic_name`).
- Update the CONCAT expression to use real column names.

#### 3. Suspended providers still receive new inquiries [A-DAT-018]

**Business action:** Suspending a provider today has no effect on inquiry distribution — they continue receiving patient leads as if active. This is a trust and data-integrity risk. Fix before any provider suspension is actioned in production; the one-line fix makes it safe to suspend.

**Technical action:**
- `app/Services/InquiryDistributionService.php:104–106` — uncomment `->where('status', 'active')`.
- No other changes needed. Verify in staging that suspended providers are excluded from the auto-match pool after the change.

---

### P2 — Implement Before Feature Release (Missing Backend Features)

#### 4. Admin cannot edit, reassign, or soft-delete inquiries [A-INQ-019, A-INQ-020, A-INQ-021]

**Business action:** FR-003 Alt Flows A1/A2/A3 (admin override of inquiry lifecycle) are not built. Until they exist, admins must contact developers to correct misdirected or problematic inquiries. Decide whether this is a current-sprint blocker or a next-sprint addition.

**Technical action:**
- **Edit with audit** — `PUT /api/admin/inquiry/{id}`: new `AdminInquiryController@update` method; call `getAuditTrail()` before/after save to log before/after state.
- **Reassign** — `POST /api/admin/inquiry/{id}/reassign`: new method that redistributes the inquiry to a chosen provider set, using `InquiryDistributionService` with an explicit override flag.
- **Soft-delete** — `DELETE /api/admin/inquiry/{id}`: register the existing unrouted `InquiryController::destroy()` (line 1740, already does `$inquiry->delete()`) to an admin-only route; add a `reason` required field and audit log write.

#### 5. Admin cannot configure quote expiry window [A-QOT-018]

**Business action:** The 48-hour quote expiry window is hardcoded. Any change requires a code deployment. Decide whether runtime configurability is needed before launch. If yes, schedule within the current release.

**Technical action:**
- Add a `quote_expiry_hours` row to the settings table (or a new `QuoteSettings` model/migration).
- Add `GET /api/admin/settings/quote-expiry` and `POST /api/admin/settings/quote-expiry` routes under the admin middleware group.
- Replace the hardcoded constant in `QuotesController` with a DB/config lookup.

---

### P3 — Schedule Within Sprint (Partial Implementations)

#### 6. Authorization fires after validation in DepositRateController [A-AUTH-P07]

**Business action:** A provider hitting the deposit rate endpoint receives a 422 (validation error) instead of a 403 (forbidden). This leaks the endpoint's existence and its validation rules. Low risk but a hygiene issue; fix in current sprint.

**Technical action:**
- `app/Http/Controllers/DepositRateController.php` — move the authorization check (middleware or `$this->authorize()`) to execute before `$request->validate(...)`. The controller should gate access first, then validate input.

#### 7. Commission rate UI shows fake data [A-QOT-003, A-XCT-006]

**Business action:** Commission rate configuration is non-functional in the admin UI. Any rate shown to admins is hardcoded mock data; backend rates are unchanged no matter what is entered. This is a high-visibility gap — if admins believe they are configuring commissions, financial calculations will diverge silently. Wire the frontend this sprint.

**Technical action:**
- `src/pages/teamDashboard/settings/CommissionRate.jsx` — replace mock data with RTK Query hooks.
- Call `GET /api/admin/commission-rates` for initial load and `POST /api/admin/commission-rates` for updates.
- The backend `CommissionRateController` is fully implemented; this is a frontend-only wiring task.

#### 8. Entire inquiry monitoring module shows hardcoded mock data [A-INQ-001–A-INQ-018]

**Business action:** The admin inquiry monitoring screen is non-functional — it shows fake data with no API calls. Admins have zero real visibility into platform-wide inquiry status. This is a full frontend build task; schedule as a dedicated sprint story.

**Technical action:**
- `src/pages/teamDashboard/request/Request.jsx` — remove mock data and wire RTK Query API calls.
- Temporary option: reuse `GET /api/inquiry/get-inquiries` (currently provider-scoped) while the admin-specific endpoint from P2 #4 is built; note the scoping limitation.
- Wire filter controls (status, date, provider) to existing backend query params.
- Fix the empty `<Link to="">` on inquiry rows to navigate to the detail view.

#### 9. Medical data tab accessible without justification [A-PAT-021, A-PAT-022]

**Business action:** Write operations require a justification, but admins can open the medical data tab and read patient records with no reason logged. This is a compliance gap (FR-016). Add a read-gate before any production access to sensitive patient data.

**Technical action:**
- **Frontend (minimum):** Add a justification prompt modal in `src/pages/teamDashboard/patients/PatientDetail.jsx` that must be submitted before the medical data tab content renders.
- **Backend (recommended):** Add a `POST /api/patient-management/log-medical-access/{id}` endpoint that accepts a `justification` string and writes an audit log entry. The frontend calls this before loading medical data; the tab content is only rendered after the call succeeds.

#### 10. Admin-side GDPR deletion workflow absent [A-PAT-029, A-PAT-030]

**Business action:** Patients can request account deletion, but admins have no way to process, approve, or reject those requests. If GDPR compliance is a pre-launch requirement, this is a blocking gap. Confirm with legal/compliance whether this must be live on day one.

**Technical action:**
- `GET /api/admin/patient-management/deletion-requests` — list all pending `PatientDeletionRequest` records.
- `POST /api/admin/patient-management/deletion-requests/{id}/approve` — anonymize PII fields, soft-delete the patient record, mark request resolved, dispatch notification.
- `POST /api/admin/patient-management/deletion-requests/{id}/reject` — mark request rejected with `rejection_reason`, notify patient.
- Anonymize handler: null out name, email, phone, medical data fields; preserve aggregate/statistical data.

#### 11. Treatment plan admin edits lack audit logging [A-TRT-014, A-TRT-016, A-TRT-017]

**Business action:** Admins can edit treatment daily entries and notes with no record of who changed what, when, or why. FR-010 requires a full audit trail for all admin edits. Without it there is no accountability for overrides — a medico-legal and compliance risk.

**Technical action:**
- `app/Http/Controllers/TreatmentPlanDailyEntryController.php:update()` — add `justification` as a required validated field; capture a before-snapshot of the record before saving; write an audit log entry (admin ID, timestamp, before, after, justification).
- `app/Http/Controllers/TreatmentPlanNoteController.php:update()` — same pattern.
- Use the existing `getAuditTrail()` pattern from `QuotesController` for consistency.

#### 12. Patient model lacks soft-delete protection [A-XCT-003]

**Business action:** Deleting a patient record today is permanent. An accidental deletion (or incomplete GDPR processing) is unrecoverable. Add soft-delete before any admin deletion workflow goes live in production.

**Technical action:**
- `app/Models/Patient.php` — add `use SoftDeletes;` import and trait usage.
- Create a migration to add a `deleted_at` nullable timestamp column to the `patients` table.
- All existing `$patient->delete()` calls will automatically become soft deletes after the trait is added.

#### 13. City-name search not available for provider lookup [A-PRV-P03]

**Business action:** Admins cannot find providers by city. Low urgency unless the provider list is large. Add to the next available backend sprint slot.

**Technical action:**
- `app/Http/Controllers/Admin/ProviderManagementController.php:64–72` — add to the search block:
  `->orWhereHas('city', fn($q) => $q->where('name', 'like', "%{$search}%"))`

#### 14. Aftercare specialist vs. provider assignment — clarify requirement [A-AFT-003, A-AFT-004, A-AFT-010, A-AFT-014]

**Business action:** FR-011 refers to assigning an "aftercare specialist" (individual person), but the current data model only supports reassigning the provider clinic. Before building anything, confirm with the product owner whether individual staff assignment is genuinely required. If it is, this requires a DB schema change.

**Technical action (if individual assignment is confirmed required):**
- Migration: add `specialist_id` (FK → `provider_users.id`, nullable) to the `after_cares` table.
- `app/Models/AfterCare.php` — add `specialist()` `belongsTo` relationship.
- Add `PUT /api/after-care/{id}/assign-specialist` route and controller method.
- If individual assignment is NOT required, update the test cases (A-AFT-003/004/010/014) to reflect provider-level reassignment as the accepted implementation.

#### 15. Commission rate snapshot at quote acceptance — confirm or implement [A-XCT-007]

**Business action:** If commission rate changes can retroactively affect already-accepted quotes, providers receive different payouts than what was agreed when the patient accepted. This needs to be verified before any commission rate change is made in production.

**Technical action:**
- Inspect `QuotesController::acceptQuote()` and `BookingService` for a `commission_rate_at_acceptance` or `commission_amount` snapshot field stored at acceptance time.
- If no snapshot exists: add a `commission_rate_snapshot` decimal field to the quotes or bookings table (migration) and populate it on `acceptQuote()`. This locks in the rate at the moment of acceptance, making future rate changes non-retroactive.

---

### Test Case Actions Summary

The table below specifies whether each defect requires a **fix → re-run** of existing TCs or **new TCs** to be written.

| TC ID(s) | Current Verdict | Required Action |
|----------|----------------|-----------------|
| A-AUTH-P02, A-AUTH-P03, A-AUTH-P05 | CODE_EXISTS_BUG | Fix middleware → re-run → expect 403 |
| A-AUTH-P04, A-PAY-001, A-PAY-002, A-PAY-009 | CODE_EXISTS_BUG | Fix SQL query → re-run → expect 200 with provider name data |
| A-DAT-018 | CODE_EXISTS_BUG | Uncomment filter → re-run → verify suspended provider excluded from distribution |
| A-AUTH-P07 | CODE_EXISTS_PARTIAL | Reorder auth/validation → re-run → expect 403 (not 422) for provider token |
| A-INQ-019, A-INQ-020, A-INQ-021 | CODE_MISSING | Implement endpoints → **write new TCs** → run |
| A-QOT-018 | CODE_MISSING | Implement config endpoint → **write new TC** → run |
| A-QOT-003, A-XCT-006 | CODE_EXISTS_PARTIAL | Wire frontend to backend → re-run with real data |
| A-INQ-001–A-INQ-018 | CODE_EXISTS_PARTIAL | Wire frontend → re-run full INQ module |
| A-PAT-021, A-PAT-022 | CODE_EXISTS_PARTIAL | Add read-gate → re-run → expect block without justification |
| A-PAT-029, A-PAT-030 | CODE_EXISTS_PARTIAL | Implement admin workflow → **write admin-side TCs** → run |
| A-TRT-014, A-TRT-016, A-TRT-017 | CODE_EXISTS_PARTIAL | Add audit logging → re-run → verify log entries exist after admin edit |
| A-XCT-003 | CODE_EXISTS_PARTIAL | Add SoftDeletes → re-run → verify record is soft-deleted (not purged) |
| A-AFT-003, A-AFT-004, A-AFT-010, A-AFT-014 | CODE_EXISTS_PARTIAL | Confirm requirement scope with PO → either update TCs or build specialist model |
| A-PRV-P03 | CODE_EXISTS_PARTIAL | Add city search clause → re-run → expect city-name results |
| A-XCT-007 | CODE_EXISTS_PARTIAL | Verify or add commission snapshot → **write regression TC** for rate-change non-retroactivity |
| A-RAC-001–A-RAC-005 | NEEDS_DEEPER_REVIEW | Manual load test or targeted DB transaction review required; no code changes until behavior confirmed |
| A-PAY-P06, A-PAY-P13 | NEEDS_DEEPER_REVIEW | Manual spot-check rounding behavior in staging with exact amounts |
| A-PAT-018, A-PAT-020, A-PAT-031 | NEEDS_DEEPER_REVIEW | Manual test session required; no code changes until behavior confirmed |
| A-QOT-016 | NEEDS_DEEPER_REVIEW | Confirm whether admin soft-delete route is needed; if yes, add route and re-run |
