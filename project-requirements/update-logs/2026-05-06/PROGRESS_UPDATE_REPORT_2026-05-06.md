# Update Log - 2026-05-06

**Type**: New Report - Progress Update  
**Date**: 2026-05-06

## Summary

Created `local-docs/reports/2026-05-06/project-progress-update-report.md`: a refreshed progress update report based on the January 27 milestone report structure.

## What Was Created

- Preserved the Executive Summary and three-tenant report structure:
  - Mobile App (Patient Platform)
  - Provider Dashboard
  - Admin Dashboard
- Preserved module-level progress tables while reducing the columns to:
  - Module
  - Component
  - What Users Can Do
  - What Users Cannot Yet Do
- Removed prior status labels, completion percentages, categories, and detailed notes from the report draft.
- Added verification-boundary guidance for the next filling phase:
  - Mobile app progress should be filled from user updates and PRD/FR checklist review, not the outdated mobile codebase.
  - Provider/Admin progress should be filled only after fresh code review.
- Replaced the long ending sections with a concise `Comprehensive Findings & Next Phase` section.

## Scope Notes

No progress verification was performed during the initial report setup. The report currently contains fill-in sections for the later PRD/FR checklist consolidation and fresh implementation review.

## Same-Day Structure Correction

- Restored the full module table column set from the previous milestone reports: `Module / Component`, `Status`, `Completion %`, `What Users Can Do`, `What Users Cannot Yet Do`, `Category`, and `Notes`.
- Cleared update-dependent cells to `[To be updated]`.
- Moved the previous report checklist items into `What Users Cannot Yet Do` as the baseline for the upcoming PRD/FR completeness audit and progress review.
- Corrected the patient module reference from `P-01 through P-10` to the source-aligned `P-01 through P-08`, while preserving business-flow subrows for reporting (`P-02a`, `P-02b`, `P-02c`, `P-03a`, `P-03b`, `P-05b`).
- Replaced the incorrect patient row labels `P-09` and `P-10` with source-aligned business subflow labels and updated the mobile `What Users Cannot Yet Do` checklists with missing business-outcome items only (travel coordination, booking/payment outcomes, aftercare reminders, and help/support flows).

## PRD Cross-Check & Business-Level Rewrite (2026-05-07)

**Trigger**: Previous AI agent had filled the `What Users Can Do` / `What Users Cannot Yet Do` columns with implementation-level detail (backend enforcement notes, code path references, FR compliance flags) rather than business-level user action language appropriate for stakeholder review.

**Changes made**:

- **Full reset to 0%**: All checklist items moved to `What Users Cannot Yet Do`; `What Users Can Do` set to "None" for all modules. Progress verification is deferred to a separate pass against the codebase.
- **Business-level language**: All checklist items rewritten as user-facing actions (verbs: submit, view, upload, accept, cancel, configure, etc.) — no technical references to controllers, models, or internal flow divergences.
- **PRD cross-check**: All 32 modules cross-referenced against the relevant FR PRD Module Scope sections (FR-001 through FR-035 as applicable). Checklist items reflect the current PRD scope, not just the January 2026 baseline.
- **New items identified from PRDs (not in January 2026 report)**:
  - P-01: Manage notification preferences; Request account deletion; View and accept Terms & Conditions / Privacy Policy / Consent forms (FR-001, FR-027)
  - P-02a: Cancel a submitted inquiry (explicit Workflow 5 in FR-003) — previously grouped under P-02b
  - P-02b: Accept one quote / auto-cancel competing quotes made explicit (FR-005)
  - P-03a: View cancellation policy and refund terms; Cancel a confirmed booking (FR-006)
  - P-04: Full MVP travel coordination scope now captured — passport, self-booked flights/hotel, provider-booked path (FR-008)
  - P-06, PR-07: Audio/video call capability with providers via Twilio (FR-012) — not in January report
  - P-07: Clarified as V1 photo-set scope only; V2 3D model features explicitly noted as out of MVP scope
  - PR-01: View and accept platform Terms & Conditions as a provider organization (FR-009, FR-027)
  - PR-06: Full package catalog management, treatment pricing configuration (FR-032, FR-024)
  - A-06: Provider acceptance/decline workflow for both-fees discounts made explicit (FR-019)
  - A-08: Full 7-screen admin analytics suite now listed (FR-014 Screens 7–13)
  - A-09c: Consolidated all 6 system settings FRs (FR-026 through FR-031) into one module row with full capability list
  - A-10: Support case management via FR-034 added alongside communication monitoring
- **FR references added** to Notes column for every module row to enable future traceability.
- **Out-of-scope modules**: Language cleaned to business level; status kept as ⛔️ / N/A.

## PR-01 Live Codebase Verification (2026-05-07)

**Module**: PR-01 Auth & Team Management | **Status**: 🟨 In Progress | **Score**: 88%

**Files verified** (React frontend — `main/hairline-frontend/src/`):
- `pages/auth/login/Login.jsx` — provider login with `useLoginMutation`
- `pages/auth/forgotPassword/ForgotPassword.jsx` — complete 4-step password reset flow
- `components/shared/LogoutButton.jsx` — logout with `/auth/logout` API call
- `pages/providerDashboard/Team.jsx` + `components/providerComponents/team/TeamTable.jsx` — team dashboard
- `components/providerComponents/team/InviteModal.jsx` — invite with role selection via `useInviteMemberMutation`
- `components/providerComponents/team/InvitationTable.jsx` — resend/cancel invitations
- `components/providerComponents/team/TeamActions.jsx` — Active/Inactive status toggle
- `pages/providerDashboard/team/TeamMemberDetail.jsx` — role change modal (wired), suspend modal (UI only — `// TODO: wire to suspend/remove API`)
- `components/providerComponents/team/ActivityLogTab.jsx` — full log view with filters and CSV export
- `components/providerComponents/providerSettings/AccountInformation.jsx` — account name, phone, timezone, password change
- `pages/auth/invitation/InvitationLanding.jsx` + `SignupForm.jsx` — invitation acceptance with T&C checkbox

**Partial items (not yet complete):**
- Edit team member profile details: button present in `TeamMemberDetail.jsx` but no `onClick` handler or navigation wired
- Formal suspend with session revocation: modal UI built; `handleSubmitSuspend` explicitly deferred with `// TODO: wire to suspend/remove API once available`
- View platform T&C as standalone provider page: no dedicated T&C viewer in provider dashboard; checkbox-only at signup/invitation

## Full Provider & Admin Tenant Codebase Verification (2026-05-07)

All Provider (PR-02a through PR-07) and Admin (A-01 through A-10) modules verified against live frontend (`main/hairline-frontend/`) and backend (`main/hairline-backend/`) code using Haiku subagents. Results written to report immediately after each module.

### Provider Tenant Results

| Module | Score | Status |
|--------|-------|--------|
| PR-01: Auth & Team Management | 88% | 🟨 In Progress |
| PR-02a: Inquiry Management & Review | 67% | 🟨 In Progress |
| PR-02b: Quote Creation & Submission | 92% | 🟨 In Progress |
| PR-03: Treatment Execution & Documentation | 100% | ✅ Completed |
| PR-04: Aftercare Participation | 88% | 🟨 In Progress |
| PR-05: Financial Management & Reporting | 85% | 🟨 In Progress |
| PR-06: Profile & Settings Management | 88% | 🟨 In Progress |
| PR-07: Communication & Messaging | 79% | 🟨 In Progress |

**Notable Provider gaps:** Medical questionnaire display not wired in inquiry detail (PR-02a); withdraw/archive quote status not implemented (PR-02b); audio/video calls backend-only, no frontend (PR-07); package catalog create/edit missing from provider UI (PR-06).

### Admin Tenant Results

| Module | Score | Status |
|--------|-------|--------|
| A-01: Patient Management & Oversight | 75% | 🟨 In Progress |
| A-02: Provider Management & Onboarding | 94% | 🟨 In Progress |
| A-03: Aftercare Team Management | 80% | 🟨 In Progress |
| A-04: Travel Management | 80% | 🟨 In Progress |
| A-05a: Patient Billing | 90% | 🟨 In Progress |
| A-05b: Provider Payouts | 50% | 🟨 In Progress |
| A-05c: Financial Reconciliation | 90% | 🟨 In Progress |
| A-06: Discount & Promotion Management | 50% | 🟨 In Progress |
| A-07: Affiliate Program Management | 50% | 🟨 In Progress |
| A-08: Analytics & Reporting | 57% | 🟨 In Progress |
| A-09a: Content & Treatment Management | 75% | 🟨 In Progress |
| A-09b: Aftercare Template Configuration | 71% | 🟨 In Progress |
| A-09c: System Settings & Payment Rules | 77% | 🟨 In Progress |
| A-10: Communication Monitoring & Support | 93% | 🟨 In Progress |

**Notable Admin gaps:** Provider payout invoicing/PDF missing (A-05b); both-fees discount approval workflow not built (A-06); affiliate payouts and reporting absent (A-07); patient funnel and pricing intelligence analytics missing (A-08); treatment global activate/deactivate UI only console.log (A-09a); keyword moderation rules hardcoded (A-10).

## PR-02a Re-Verification (2026-05-07)

**Trigger**: Score of 67% flagged as suspicious. Direct code review (no subagent) performed to re-verify all checklist items.

**Root cause of error**: The Haiku subagent missed two facts:
1. `MedicalQuestionnairesLite.jsx` is rendered at `TableDetails.jsx:249` under the `isSingle` branch — the component was imported AND used, the agent only verified import.
2. `InquiriesFilterDrawer` renders at `DataTable.jsx:119` on a separate condition (`filterType === "inquiries"`) that is independent of `isShowSortOrFilter={false}` — the agent saw the `false` prop and concluded filters were hidden.

**Corrections**:
- Filter and search: ✅ `InquiriesFilterDrawer` exposes all fields (age range, dates, location, problem type, medical alert, patient ID/name); backend `InquiryController@index` supports every param.
- Inquiry detail completeness: ✅ `TableDetails.jsx` renders date ranges, problem description, 3D scan viewer, patient info, and medical questionnaire.
- Medical questionnaire with alert levels: ✅ `MedicalQuestionnairesLite` renders alert level badge + up to 3 Q&A items; backend `InquiryController@show` returns `medical_info.alert_level` and `medical_info.questionnaires` (lines 1168–1184).

**Revised score**: 67% → **100% ✅ Completed** (6/6 items verified)

## PR-04 Re-Verification & Category Column Restoration (2026-05-07)

### PR-04 Re-Verification

**Trigger**: Score of 88% queried; "template selection incomplete" and "questionnaire responses missing" flags re-examined via direct code review.

**Corrections**:
- Template selection and activation: ✅ — `AddAfterCareModal` is a complete 6-step wizard (Select Patient → Template Selection → Milestone Customization → Medication → Instructions → Review). `EndTheTreatmentModal.jsx:226` sets `pendingAftercareSetup` in localStorage on treatment completion; `AfterCare.jsx:31–48` reads it on mount and auto-opens the modal at the template step. `useCreateCompleteAftercareMutation` submits the full payload with `template_key`, `milestones`, `medications`, and `instructions`. Flow is fully functional end-to-end.
- Patient-submitted questionnaire response content: 🟨 (confirmed partial) — `AfterCareDetailsMilestones` renders questionnaire task status (name, completed/due date, next/overdue task cards) per milestone; the individual answer content (patient's actual responses to each question) is genuinely not displayed.

**Revised score**: 88% → **94%** (7/8 items; 1 genuine partial remaining)

### Category Column Restoration

**Issue**: The Category column across all Provider and Admin module rows incorrectly showed "Provider Dashboard" / "Admin Dashboard" (tenant labels) instead of priority/severity classifications matching the January 27 milestone report format.

**Action**: All 21 module rows updated with priority-based categories:
- ⚠️ Critical: PR-01, PR-02a, PR-02b, PR-03, PR-04, PR-07, A-01, A-02, A-03, A-05a, A-05b, A-09a, A-09b
- 📋 Standard: PR-05, PR-06, A-04, A-05c, A-06, A-07, A-08, A-09c, A-10

Category legend added to both Provider and Admin section headers.

## PR-07 Re-Verification (2026-05-07)

**Module**: PR-07 Communication & Messaging | **Status**: 🟨 In Progress | **Score**: 79% → **93%**

**Root cause of error**: The prior Haiku subagent missed three implemented subsystems:
1. `VideoCallPage.jsx` — full Twilio Video SDK integration (local/remote video, mute, camera toggle, end call) at route `/call/:callId`
2. `IncomingCallHandler.jsx` + `useIncomingCall.jsx` — real-time incoming call notification (Modal with Accept/Reject buttons) via Laravel Echo `private-user.{type}.{id}` channel; both mounted globally in `App.jsx`
3. `useFcmNotifications.jsx` — FCM push notifications with foreground `antdMessage.info` toast; also mounted in `App.jsx`

**Attachments backend confirmed**: `ChatController@sendMessage` (line 990) stores files to `chat/attachments/{conversation_id}/`, enforces 5-file limit and 10MB max per file. Backend route `POST /chat/send` maps to this handler.

**Corrections**:
- Attach and share media: ✅ — FE: `ChatWindow.jsx` full file input UI + `PatientProviderChat.jsx` sends via `formData.append('attachments[]', file)` to `/chat/send`; BE: `ChatController@sendMessage` stores files to `chat/attachments/{conversation_id}/`
- Receive incoming audio/video calls: ✅ — `IncomingCallHandler` + `IncomingCallModal` (Accept/Reject) + `VideoCallPage.jsx` (Twilio Video SDK) all fully wired in `App.jsx`
- Real-time push notifications: ✅ — `useFcmNotifications` in `App.jsx` shows foreground toast via `antdMessage.info`; background push via FCM device token registration

**Genuine partial remaining**:
- Initiate outgoing audio/video calls from chat: 🟨 — `callService.js` has `initiateCall()` hitting `/calls/initiate`; no call-initiation button present in `ChatWindow.jsx`

**Revised score**: 79% → **93%** (6.5/7 items; 1 genuine partial remaining)

## A-01, A-02, A-03 Re-Verification (2026-05-07)

### A-01: Patient Management & Oversight | Score: **75% — unchanged, content corrected**

**Medical history and scan photo sets**: Prior assessment said "no dedicated medical document storage UI verified" (implying 🟥). Direct review confirms: `PatientDetail.jsx` Tab 1 renders `VisualEvidence` (inquiry scan photos) and `MedicalQuestionnairesLite` (medical questionnaire + alert levels); Tab 8 renders `AfterCareDetailsMilestones` loaded via `useGetAfterCareMilestonesScansQuery`. Medical data IS accessible — moved to "Can Do" (✅).

**Review moderation**: Prior assessment said "only patient-self edit supported; no admin moderation UI" (implying 🟥). Backend verification reveals a complete `AdminReviewController` with full admin review management: `GET /` (list), `DELETE /{id}` (remove), `PATCH /{id}/redact`, `PATCH /{id}/flag`, `PATCH /{id}/unflag`, plus takedown request approve/reject (FR-013). Frontend: no admin review moderation UI wired — `ProviderReviews.jsx` at `/reviews/:id` is provider-facing only. Updated to 🟨 partial in "Cannot Yet Do".

**Net score effect**: Medical ✅ (+1.0) and reviews 🟨 (+0.5) replace two prior 🟥 items (0.0 each). Total = 7.5/10 = **75%** — numerically unchanged but distribution corrected.

**Confirmed unchanged items**:
- Manually intervene in bookings: 🟥 — no admin cancel/reschedule backend routes; no frontend UI
- Patient analytics: 🟥 — no dedicated admin patient analytics dashboard

---

### A-02: Provider Management & Onboarding | Score: **94% — confirmed**

Backend route `POST /providers/{id}/resend-activation` → `ProviderManagementController@resendActivation` confirmed at line 496. No frontend UI button found in any admin provider page (`Providers.jsx`, `ProvidersBilling.jsx`, `ProviderStaff.jsx`, `ProviderPayoutDetail.jsx`). Score of 94% confirmed accurate — 1 partial item (backend implemented, frontend missing).

---

### A-03: Aftercare Team Management | Score: 80% → **70%**

**Root cause of error**: Prior agent scored "Reassign aftercare cases to different providers" as ✅ (Can Do). Direct review of `AdminActionsTab.jsx` found the Reassign Provider modal's `<Select>` has hardcoded placeholder options:
```jsx
{/* TODO: Load providers from API */}
<Option value="provider1">Provider 1</Option>
<Option value="provider2">Provider 2</Option>
```
The `useReassignProviderMutation` hook IS wired to `POST /after-care/reassign-provider` with reason capture, but the provider dropdown cannot select real providers from the system — making actual reassignment impossible in practice. Updated to 🟨 partial → moved to "Cannot Yet Do".

**Confirmed correct**:
- Edit Aftercare Plan: "Edit Aftercare Plan functionality coming soon" (`AdminActionsTab.jsx:122`) — 🟥 confirmed; no backend endpoint for plan editing found

**Revised score**: 80% → **70%** (3.5/5 items: 3 ✅ + 1 🟨 reassign + 1 🟥 edit plan)

## A-03 Second Re-Verification (2026-05-07)

**Trigger**: After the 70% correction, a deeper pass was requested — specifically to verify the standalone aftercare request flow that had been scored as ✅ (Can Do).

**Files read**: `StandaloneAfterCareRequestDetails.jsx`, `AfterCareOverView.jsx`, `AssignProviderModal.jsx`

### Standalone flow findings

**Assign Provider** (`AssignProviderModal.jsx`):
- Uses `useGetAvailableProvidersQuery` from `standaloneAftercareApiSlice` — fetches real providers from backend with live search ✅
- Distinct from `AdminActionsTab.jsx` reassign which uses hardcoded options — these are two separate paths

**Activate Standalone Request**:
- `useActivateRequestMutation` imported and `handleActivate` handler defined in `StandaloneAfterCareRequestDetails.jsx:367`
- `handleActivate` is **never called** — no UI button or link has an `onClick={handleActivate}`
- `AfterCareOverView.jsx` ActionDropDown has `"Activate Aftercare"` as a `<Link>` element with **no `to` prop** (dead link)
- Result: activation step has no functional UI trigger 🟥

**Complete (End Treatment)**:
- `useCompleteRequestMutation` wired; "End treatment" button renders only when `status === "active"`
- Since activation has no UI trigger, `status === "active"` is never reached → "End treatment" is effectively unreachable 🟥

**Reject**:
- `RejectRequestModal` imported and opened via `onReject` callback in `ConsultationSidebarDefault` ✅

**Active state management** (`ConsultationSidebarActive`):
- Four buttons rendered: "Chat with patient", "Adjust Aftercare Plan", "Request Additional Scan", "Escalate Case"
- None have `onClick` handlers — all are inert UI shells 🟥

### Score correction

Standalone flow item reclassified from ✅ → 🟨: core assign and reject work via real APIs; but activation (and therefore completion) has no UI trigger, and active-state management buttons are all missing `onClick`.

**Revised score**: 70% → **60%** (3.0/5: 2 ✅ view cases + escalate via AdminActionsTab; 2 🟨 standalone partial + reassign hardcoded; 1 🟥 edit plan)

## A-04, A-05a, A-05b Verification (2026-05-07)

### A-04: Travel Management | Score: **80% — confirmed**

**Files read**: `AdminTravelOverview.jsx`, `AdminTravelCorrection.jsx`, `BookHotelAndFlight.jsx`, `TravelSection.jsx`, `TravelFlightBooking.jsx`, `PatientDetail.jsx`

All 4 Can Do items confirmed:
- View travel status: ✅ — `TravelSection` returns `AdminTravelOverview` for `profile_type === "hairline"` users; shows passport, outbound flight, return flight, hotel status with submitter audit trail
- Monitor automated travel submission status: ✅ — status tags (Submitted/Awaiting/Correction Needed/Incomplete) per record type
- Re-trigger travel submissions: ✅ — `useRenotifyTravelMutation` wired in `AdminTravelOverview`, called via `handleRenotify(recordType)` for awaiting/correction_needed statuses
- Edit/override travel records: ✅ — `AdminTravelCorrection` uses `useUpdateFlightMutation` and `useUpdateHotelMutation`; `allowEdit={false}` prop from `PatientDetail` only affects the provider-side `HotelAndFlight` component, NOT the admin edit path (guarded by `isAdmin`)

Travel API configuration settings: ✅ confirmed not implemented — `TravelFlightBooking.jsx` renders only `<h3>In Progress ... </h3>`.

**Score unchanged: 80%**

---

### A-05a: Patient Billing | Score: **90% → 80%**

**Files read**: `PatientsBilling.jsx`, `PatientBillingDetails.jsx` (first 120 lines)

**Confirmed ✅ items:**
- View all patient invoices — `useGetPatientsBillingQuery` (falls back to mock data if API returns empty)
- Monitor installment plan progress — visual progress bar + full installment schedule in detail view
- Process refunds — `useProcessPatientRefundMutation` via `ProcessRefundModal`
- Send individual payment reminders — `useSendPaymentReminderMutation` in re-auth modal
- Override payment status — `useOverridePaymentStatusMutation` with reason + re-auth (was not separately listed; now explicit)

**Newly found 🟥 gaps (not previously in Cannot Yet Do):**
- **Bulk "Send Reminders (All Overdues)"**: top-bar `<Button>` with no `onClick` — renders but does nothing
- **Download individual invoice**: "Download Invoice" in the action dropdown hits the `else { message.info('Action download (Simulated)') }` branch — simulated, not implemented

**Score corrected**: 90% → **80%** (bulk send and invoice download both moved from implied ✅ to 🟥)

---

### A-05b: Provider Payouts | Score: **50% → 33%**

**Files read**: `ProvidersBilling.jsx`, `ProviderPayoutDetail.jsx`

**Root cause of error**: Prior agent scored "Approve and process provider payouts (with re-auth modal)" as ✅. Direct code review reveals both the list view and detail view use `setTimeout` simulation instead of calling the real mutations:

- `ProvidersBilling.jsx` `onReauthFinish`: `setTimeout(() => { message.success(...) }, 1500)` — no API call; mutations are never invoked
- `ProviderPayoutDetail.jsx` `onReauthFinish`: `setTimeout(() => { navigate(...?mock_status=failed) })` — developer demo that navigates to a mock state; `approvePayout()` never called
- `onRetryFinish` (detail): same pattern — `setTimeout` simulation; `retryPayout()` never called

**Additional gaps found:**
- "Download Detailed Report" button in `ProviderPayoutDetail.jsx`: `<Button className="btn-download" icon={<DownloadOutlined />}>` — no `onClick` handler
- "Outstanding Earnings" column in list: hardcoded `net_payout * 1.2` calculation — not real data
- Bank Account column in list: hardcoded `record.id % 2 === 0 ? "Visa..." : "Mastercard..."` — not real provider bank data

**Confirmed ✅ items:**
- View payout list with sectioning (overdue/failed/pending) — `useGetProviderBillingsQuery` real API
- View payout detail with per-booking breakdown (treatment amount, commission deducted, net contribution, adjustments, financial summary) — `useGetProviderPayoutDetailQuery` real API
- Add internal notes — `useUpdateProviderBillNoteMutation` wired properly via `handleAddNote`

**Revised score**: 50% → **33%** (3 ✅ view/detail/notes out of 9 total items)

---

## A-05c and A-06 Verification — 2026-05-07

### A-05c: Financial Reconciliation & Reporting

**Prior score**: 90% | **Revised score**: **10%**

**Critical finding — RevenueDashboard.jsx is pure UI prototype with no API integration:**
- `RevenueDashboard.jsx`: zero `useQuery`/`useMutation` imports; all data is inlined as hardcoded constants (`const KPIs = {...}`, `const outstandingInvoices = [...]`, `const discountUsage = [...]`, `const affiliateSummary = [...]`, chart datasets). The component renders a complete-looking Financial Reporting screen but every figure shown is hardcoded.
- `DiscountUsageOverview.jsx`: imports `discountUsageMockData` from a static data file — no API call.
- `AffiliateBilling.jsx`: `const data = [{ id: "aff001", patient_name: "Quentin Xavier", ... }]` — fully inlined hardcoded records.
- "Export Full Report" button: `<Button icon={<ExportOutlined />}>Export Full Report</Button>` — no `onClick` handler.
- Currency selector (USD/EUR): present in RevenueDashboard but data does not change with selection — all figures are static.

**What is real:**
- `FinanCialOverView.jsx` uses `useGetRevenueQuery`, `useGetRevenuePerPatientsQuery`, `useGetProviderResponseTimesQuery`, `useGetPendingPaymentsQuery` — these are real APIs providing summary revenue and pending payment data. This is the only real data connection in A-05c scope.

**Impact on report:**
All four Can Do items (aging buckets, multi-currency reporting, discount usage tracking, affiliate commission tracking) were incorrect — they describe features in RevenueDashboard which is fully mock data. Items moved to Cannot Yet Do. Score drops from 90% to 10%.

---

### A-06: Discount & Promotion Management

**Prior score**: 50% | **Revised score**: **50%** (composition corrected)

**Correction to Cannot Yet Do — hairline-fee-only discounts CAN be created:**
- `SetDiscountModal.jsx` (used via `AllPromotions.jsx` with `isTeam=true`) calls `${baseUrl}/discount/create-discount` via a real `axios.post`.
- The "Discount Sub Type" dropdown contains two options: `"Both fees" (both_fees)` and `"Hairline" (hairline_fees)` — both types are available from the admin UI.
- The prior report's Cannot Yet Do item "Create platform-wide (hairline-fee-only) discount codes" is incorrect; hairline-fee-only creation is already functional.

**New gap found — Applied and Completed detail lists use mock data:**
- `AppliedDiscounts.jsx`: `import { discountData } from '../../../data'` — filtered from a global static mock array; no API call.
- `CompletedDiscount.jsx`: same pattern — `discountData.filter(item => item.status === "completed")` from the same static data file.

**Confirmed ✅ items:**
- Discount creation with full parameters (both subtype options) — `SetDiscountModal` real API via `axios.post`
- Promotions overview stats (all/applied/completed counts) — `HairlinePromotions.jsx` uses `useGetDiscountStatisticsQuery()` real API
- Full discount list — `AllPromotions.jsx` uses `useGetAllDiscountsQuery()` real API

**Score stays 50%**, but report is corrected: hairline-fee-only creation moves to Can Do; applied/completed detail lists added to Cannot Yet Do.

---

## A-07 and A-08 Verification — 2026-05-07

### A-07: Affiliate Program Management

**Prior score**: 50% | **Revised score**: **50%** (confirmed)

**Confirmed ✅ items:**
- Affiliate onboarding wizard (Profile → Commission → Discount Codes → Summary): each step makes real API calls — `axios.post(${baseUrl}/affiliates)`, `axios.post(...affiliates/${id}/commission)`, `axios.post(...affiliates/${id}/discount-code)`. Discount code generation (percentage or fixed amount, expiration, usage limits) is included within the wizard and connected to the backend.
- Affiliate list management: `AffiliateManagementOverView.jsx` uses `useGetAffiliatesQuery` — real API with search, sorting, and delete (`useDeleteAffiliateMutation`).
- Affiliate detail view: `AffiliateDetails.jsx` uses `useGetAffiliateByIdQuery` — real API. Shows revenue, payouts, applied/completed discounts, profit, commission details, and discount codes where available.

**Confirmed 🟥 items:**
- Affiliate payouts: `AffiliateBilling.jsx` renders a hardcoded `const data = [{ id: "aff001", patient_name: "Quentin Xavier", ... }]` array with no API call. The "Pay" button has no `onClick` handler.
- Affiliate performance stats (detail): revenue, payouts, and profit fields show real API data, but referral counts, conversion rates, and channel metrics are absent — consistent with the report's "total revenue is displayed but referral counts, conversion rates, and channel metrics are missing."
- Commission auto-calculation on booking completion and affiliate performance reports: not verified against backend but no frontend evidence of these flows exists.

**Score unchanged at 50%.**

---

### A-08: Analytics & Reporting

**Prior score**: 57% | **Revised score**: **57%** (confirmed)

**Confirmed ✅ items (4 of 7 screens):**
- Platform Overview Dashboard: `AnalyticsOverView.jsx` (`useGetAnalyticsOverviewQuery`) + `HairlineOverview.jsx` (`useGetAllOverViewsQuery`, `useGetOverViewsSimpleQuery`) — real APIs providing active providers, patient signups, inquiries, and quote data.
- Provider Performance & Engagement: `ProviderPerformance.jsx` uses `useGetTopProvidersQuery` and `useGetProvidersResponseTimeQuery` — real APIs with date range filtering.
- Treatment Outcomes: `TreatmentsOutcomes.jsx` uses `useGetTreatmentOutcomesQuery` — real API with start/end date parameters.
- Financial Health & Cashflow: `FinanCialOverView.jsx` uses `useGetRevenueQuery`, `useGetRevenuePerPatientsQuery`, `useGetProviderResponseTimesQuery`, `useGetPendingPaymentsQuery` — real APIs.

**Confirmed 🟥 / 🟨 items:**
- Patient Acquisition & Funnel: `ConversionAndMarketing.jsx` uses `useGetProviderPerformanceDashboardQuery` — a real API that returns `funnel_breakdown`, `revenue_over_time`, `top_countries`, `average_treatment_time`, `patient_average_age`, `patients_by_location`. However the page renders under the heading "Provider Performance" and primarily shows provider-centric metrics. It does not implement a patient acquisition funnel (inquiry → quote → booking conversion rates). Report description is accurate.
- Geographic Intelligence: no dedicated screen found in the codebase.
- Pricing Intelligence: no dedicated screen found in the codebase.

**Score unchanged at 57%.**

---

## A-09a, A-09b, A-09c Verification — 2026-05-07

### A-09a: Content & Treatment Management

**Prior score**: 75% | **Revised score**: **33%**

**Confirmed ✅ items:**
- Treatment catalog CRUD: `Treatments.jsx` uses `useGetAllHairlineTreatmentsQuery` — real API with search/filter. `CreateTreatment.jsx` calls `axios.post(${baseUrl}/treatment/create-treatment)` — real API.
- Media upload (videos, images): included in `CreateTreatment.jsx` via `axios.post` with multipart FormData — real API.

**Critical finding — questionnaire management is entirely in-memory mock:**
- `QuestionnaireCatalog.jsx` calls `useQuestionnaireCatalogData()` which imports `questionnaireCatalogMockResponse` from `./questionnaireCatalog/mockData.js`. All state (rows, meta) is initialized from mock data via `useState`. Operations (duplicate, archive, delete, setInquiryActive) call `setRows(...)` — local React state only.
- `QuestionnaireSetDetails.jsx` similarly uses `useQuestionnaireSetDetailsData()` which imports from its own `mockData.js`.
- No API calls anywhere in the questionnaire flow. All changes reset on page reload.

**Confirmed 🟥 items:**
- Deactivate treatment: `TreatmentCard.jsx` deactivate `onClick` → `console.log("Deactivate treatment:", id)` — no API call.
- Provider packages view: `Packages.jsx` renders a single `Package.jsx` component with hardcoded "Fue Hair Transplant" and `₺1999 – ₺6500` — no API call.

**Questionnaire management (2 Can Do items) moved to Cannot Yet Do. Score drops from 75% to 33%.**

---

### A-09b: Aftercare Template Configuration

**Prior score**: 71% | **Revised score**: **71%** (confirmed)

**Confirmed ✅ items:**
- Milestone CRUD: `AfterCareMilestones.jsx` uses `useGetAftercareMilestonesQuery` — real API. `CreateMilestoneModal` provides CRUD.
- Questionnaire assignment: `AfterCareQuestionnaire.jsx` uses `useGetAftercareQuestionsQuery` — real API.
- Resources: `AfterCareResource.jsx` uses `useGetResourcesQuery` — real API.
- Scan photo schedules: `milestone.scan_schedule` is rendered from real milestone data.
- Payment options (general tab): `AfterCareGeneral.jsx` uses `useGetAftercarePaymentOptionsQuery`, `useLazyGetDeleteAftercarePaymentOptionsQuery` — real APIs.

**Confirmed 🟥 items:**
- No pricing configuration screen found for marking templates as purchasable.
- No status toggle (activate/deactivate) found in any aftercare settings component.

**Score unchanged at 71%.**

---

### A-09c: System Settings & Payment Rules

**Prior score**: 77% | **Revised score**: **56%**

**Confirmed ✅ items (real API connections verified):**
- Auth throttling/OTP: `authenticationThrottlingApiSlice.jsx` exists; `AuthenticationThrottlingEditor.jsx` uses it.
- App data lists: dedicated API slices for countries, discovery questions, cancellation reasons, deletion reasons — all confirmed present.
- Legal documents: `legalDocumentsApiSlice.jsx`; `LegalDocumentsList.jsx` and `EditLegalDocument.jsx` use it.
- Stripe accounts: `StripeAccounts.jsx` uses `useGetPaymentConfigurationsQuery` — real API.
- Currency conversion: `currencyConversionApiSlice.jsx`; `CurrencyConversionForm.jsx` and `CurrencyConversionDashboard.jsx` use it.
- Deposit rates: `DepositRate.jsx` uses `updateGlobalRate()` and `addProviderRate()` mutations — real API calls.
- Installment plan rules: `SplitPayment.jsx` uses `useGetSplitPaymentConfigQuery`, `useUpdateSplitPaymentConfigMutation`, `usePreviewInstallmentScheduleMutation` — real APIs.

**Confirmed 🟥 items (moved from Can Do to Cannot Yet Do):**
- Global commission rate configuration: `CommissionRate.jsx` has `// Mock data - matching Figma design` comment; save buttons call `message.success("Save Setting (mock)")` — no API call.
- Notification templates: `NotificationTemplateEditor.jsx` — `handleSaveDraft`, `handleActivate`, `handleSendTest` all use `await new Promise(r => setTimeout(r, ...))` — simulated with no API. `EmailTemplates.jsx` is a fully static hardcoded page.
- Admin team member management: `AdminUsersTab.jsx` imports `getAdminUsersMock` from `mockRolePermissionsData.js`; `handleInviteSubmit` only calls `setUsers((prev) => [newUser, ...prev])` — in-memory state, no API, resets on reload.
- Admin roles management: `AdminRolesTab.jsx` imports `getAdminRolesMock`; `EditRolePermissionsPage.jsx` imports `getRoleByIdMock`, `getRolesMock`, `updateRoleMock` — all from `mockRolePermissionsData.js`.

**Score drops from 77% to 56%.** 9 real items remain in Can Do; 7 items (3 newly moved + 4 existing) are in Cannot Yet Do.

---

### A-10: Communication Monitoring & Support

**Prior score**: 93% | **Revised score**: **5%**

**Evidence — all major components are mock/simulated:**
- `SupportCenter.jsx`: `import { mockSupportMessages } from "./mockSupportMessages"` — entire conversation monitoring list is static mock data.
- `SupportTickets.jsx`: `const [data, setData] = useState(buildMockData)` where `buildMockData()` programmatically generates 52 fake support cases (`CASE-2025-12345` through `CASE-2025-12396`) — no API call anywhere in the file.
- `SupportCaseDetail.jsx`: No API imports. Case reassign and reopen handlers both use `await new Promise((resolve) => setTimeout(resolve, 800))` — simulated delays with no backend call.
- `SupportCaseForm.jsx`: No API imports. Submit handler calls `message.success(isEdit ? "Support case updated (mock)." : "Support case created (mock).")` — explicitly mock-labelled confirmation.
- `SupportCaseResolutionPage.jsx`: Resolution submit handler uses `await new Promise((resolve) => setTimeout(resolve, 900))` — simulated with no API call.
- `Chat.jsx`: Hardcoded profile picture (`profilePicture1`), hardcoded name "Mark Perry", hardcoded timestamp "Last message 2 minute ago" — fully static UI shell with no data layer.
- `Messages.jsx`: Only icon imports — static content only.

**Confirmed 🟥 items (all 13 original Can Do items moved to Cannot Yet Do):**
- Conversation monitoring, filtering, search — all on mock data
- Keyword flag alerts, manual flagging, flag history — no flagging system connected
- Emergency intervention — simulated, no real send
- Export conversation logs — button present, no implementation
- Create/manage/resolve support cases — mock form submission, mock case list, simulated case actions
- Assign cases to team members — hardcoded `STAFF_OPTIONS` array, no backend
- Two-way case thread — hardcoded static contact, no real messages
- Bulk close/reassign — UI only, no backend connection
- Export individual case data — no implementation

**Single partial credit item**: All support center screens (conversation monitoring, case list, case detail, case creation form, resolution page) are built and navigable as a UI prototype.

**Score drops from 93% to 5%.** 1 partial item remains in Can Do; 14 items are in Cannot Yet Do (13 newly moved + 1 existing "configure keyword rules" + 1 existing "view analytics").
