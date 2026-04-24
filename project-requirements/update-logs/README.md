# Update Logs

This folder contains documentation update reports and verification logs for the Hairline platform system documentation, organized by date for easy retrieval.

---

## Organization by Date

### 2025-10-23/ (7 files)

#### **Major Documentation Updates & Verification**

- `DOCUMENTATION_UPDATES_2025-10-23.md` - Complete changelog of all system documentation updates
- `VERIFICATION_REPORT_2025-10-23.md` - Comprehensive verification report confirming consistency
- `WORKFLOW_CORRECTION_2025-10-23.md` - Provider Quote Management process correction
- `WORKFLOW_CLARIFICATION_2025-10-23.md` - Status transitions during treatment execution
- `TREATMENT_PACKAGE_CLARIFICATION_2025-10-23.md` - Critical Treatments vs Packages architecture
- `REQUIREMENTS_IMPLEMENTATION_2025-10-23.md` - Complete implementation of verification issues
- `REQUIREMENTS_VERIFICATION_2025-10-23.md` - Comprehensive verification against transcriptions

### 2025-10-27/ (2 files)

#### **Cross-Reference Updates & FR-025 Creation**

- `CROSS_REFERENCE_UPDATES_2025-10-27.md` - Cross-reference consistency updates and FR order correction
- `FR025_PRD_CREATION_2025-10-27.md` - FR-025 Medical Questionnaire Management PRD creation

### 2025-10-28/ (3 files)

#### **Module Restructure & PRD Creation**

- `MODULE_RESTRUCTURE_2025-10-28.md` - MAJOR module restructure aligning Provider Platform modules
- `DOCUMENTATION_CONSISTENCY_FIXES_2025-10-28.md` - Critical and high-priority documentation fixes
- `FR001_PRD_CREATION_2025-10-28.md` - FR-001 Patient Authentication PRD creation

### 2025-10-30/ (3 files)

#### **PRD Verification & Documentation Sync**

- `FR001_PRD_VERIFIED_2025-10-30.md` - FR-001 status set to Verified & Approved; detailed Screen 13/15 finalized
- `DOCUMENTATION_SYNC_2025-10-30.md` - Synced high-level docs and README date to Oct 30, 2025
- `FR002_MINIMAL_SPECS_2025-10-30.md` - FR-002 screen specs minimized to integration contracts; verified consistency

### 2025-10-31/ (2 files)

#### **Aftercare & Quotes Updates**

- `FR011_FR025_Updates_2025-10-31.md` - Adjustments to Aftercare and Medical Questionnaire PRDs
- `FR004_PRD_UPDATES_2025-10-31.md` - Quote Submission & Management updates (expiry policy, scenarios, unified list, admin inline edit)

### 2025-11-04/ (1 file)

#### **FR-005 PRD Verification**

- `FR005_PRD_VERIFIED_2025-11-04.md` - FR-005 Quote Comparison & Acceptance PRD reviewed and verified

### 2025-11-06/ (1 file)

#### **FR-026 Analysis & Critical Issues Resolution**

- `FR026_ANALYSIS_C1_RESOLVED_2025-11-06.md` - FR-026 App Settings & Security Policies analysis and resolution
  - **C1 (Critical)**: Rollback contradiction resolved → Forward-only model approved
  - **C2 (Critical)**: Missing client requirements resolved → 5 new FRs created (FR-027 through FR-031)
  - **H1 (High)**: HTML sanitization specification added to Security Considerations
  - **H2 (High)**: OTP rate limiting logic clarified in Business Rules (business requirements only)
  - **H5 (High)**: Missing module dependencies added (FR-024, FR-011, Admin Auth)
  - **Final Verification**: Confirmed FR-026 PRD covers all in-scope client requirements with no major discrepancies
  - **Status**: All critical and high-priority issues resolved; implementation-ready

### 2026-02-25/ (1 file)

#### **FR-025 Verification & System PRD Alignment**

- `FR025_VERIFICATION_UPDATES_2026-02-25.md` - FR-025 Medical Questionnaire Management post-verification updates
  - Inquiry question type constraint changed to soft warning (Yes/No recommended, other types allowed after confirm)
  - Visual Scale 1–5 removed; replaced by Visual Scale 1–10 as sole visual scale type
  - FR-002 dependency removed (no actual data flow)
  - FR-020 alert event integration note added
  - System PRD: Bulk Operations and Question Templates deferred to V2 (not in client transcriptions)
  - System PRD: Question Grouping aligned to set-level categorisation per FR-025 design
  - System PRD: Question types expanded from Yes/No-only to full type list

### 2026-02-05/ (1 file)

#### **Cancel Inquiry FR Updates**

- `2026-02-05-cancel-inquiry-fr-updates.md` - Cancel inquiry feature updates

### 2026-02-13/ (2 files)

#### **Plane Automation Improvements & Secrets Scan**

- `PLANE_API_IMPROVEMENTS_2026-02-13.md` - Summary of `plane-api-commands` skill/workflow improvements, including HTML cleanup, issue-update support, skip-parameter support, and `.env` sandbox handling notes
- `SECRETS_SCAN_REPORT_2026-02-13.md` - Confirmed no hardcoded secrets under `local-docs/project-automation`; credential handling remained limited to environment files, placeholders, and non-secret resource identifiers

### 2026-02-27/ (1 file)

#### **FR-010 Major Revision — Tabbed Display & Day-by-Day Model**

- `FR010_REVISION_2026-02-27.md` - FR-010 major revision (v1.1 → v1.2): entry point corrected to Confirmed list, tabbed case detail page adopted, day-by-day treatment plan model enforced, clinician model aligned, elapsed time removed, consent withdrawal simplified, graft number clarified

### 2026-02-28/ (1 file)

#### **FR-010 Second Revision — Mermaid Workflows & 3-Tenant Screen Specs**

- `FR010_REVISION_2026-02-28.md` - FR-010 second revision pass (v1.2 → v1.3)
  - Admin full edit capability restored (confirmed in AdminPlatform-Part1 transcription)
  - Deprecated media note removed; elapsed time annotation removed cleanly
  - Entry point wording clarified (tab becomes active AS case transitions Confirmed → In Progress)
  - Donor area and clinician reassignment removed (not in client transcriptions)
  - End Treatment gate added (all days must reach terminal status)
  - Graft count confirmed as single end-of-treatment entry (no per-day tracking)
  - A3 (mid-procedure plan modification) and A4 (multi-day flow) and B4 (consent withdrawal) removed
  - All business workflows converted to Mermaid `flowchart TD` format
  - Screen Specifications completely restructured to 3-tenant format: Patient (2), Provider (4), Admin (2) screens

### 2026-03-02/ (2 files)

#### **FR-012 Implementation Tasks (Provider + Admin Focus)**

- `IMPLEMENTATION_TASKS_FR012_2026-03-02.md` - Task breakdowns created for FR-012 gaps (Provider PR-07 + Admin A-10), including FE-only tasks and supporting FE+BE/BE tasks

#### **FR-010 Post-Verification Issue Resolution**

- `FR010_VERIFICATION_FIXES_2026-03-02.md` - FR-010 v1.3 → v1.4: 14 verification issues resolved
  - Aftercare scope boundary fixed (FR-010 stops at Complete Treatment; FR-011 owns aftercare)
  - Media types clarified (treatment photos + 3D head scans as distinct types)
  - Final 3D Head Scan made required; RBAC aligned to FR-031 (Owner + Manager + Clinical Staff)
  - Singular clinician model aligned to FR-004; donor/recipient removed
  - No-Show/Postponed clarified as admin-managed labels; User Story 2 rewritten (no Pause)

### 2026-03-03/ (7 files)

#### **FR-006 + FR-010 Alignment**

- `FR006_FR010_ALIGNMENT_2026-03-03.md` - Added Aftercare to FR-006 booking statuses; clarified FR-010 payment gating (no payment capture), No-Show label semantics, and medication free-text model

#### **FR-010 Scan Photo Set (V1) + Doc Cleanup**

- `FR010_SCAN_PHOTOSET_DOC_CLEANUP_2026-03-03.md` - Standardized FR-010 head scan capture for V1 as a photo set, aligned system PRD wording, and removed deprecated scan-overlay notes across local docs

#### **FR-010 Admin Override + Soft Delete + Day-Only In Progress**

- `FR010_ADMIN_OVERRIDE_SOFT_DELETE_DAY_MODEL_2026-03-03.md` - Clarified day-only In Progress model (status + quote plan description + notes), required admin override reasons in audit trail, and enforced soft-delete-only semantics for treatment documentation/media (plus FR-004 plan schema clarification)

#### **FR-010 PRD Verified**

- `FR010_PRD_VERIFIED_2026-03-03.md` - FR-010 PRD status set to Verified & Approved; approvals updated to ✅ Approved; footer confirmed aligned to `prd-template.md`

#### **P-05 Flows Design Complement**

- `P05_FLOWS_DESIGN_COMPLEMENT_2026-03-03.md` - Filled in all 3 P-05 placeholder flows (P05.1 Day-to-Day Treatment Progress, P05.2 Previous Treatments List, P05.3 Submitted Reviews List) in the Missing Mobile Flows Design Complement report; replaced Mermaid and screen spec placeholders with complete diagrams, screen spec tables (12 screens across 3 flows), and business rules sourced from FR-010, FR-011, FR-013; updated summary dashboard and flow header statuses to 🟡 Specified

#### **FR-013 Moderation Gate Removed**

- `FR013_MODERATION_REMOVED_2026-03-03.md` - Removed pre-publication moderation gate from FR-013 (not requested in client transcriptions); reviews now publish immediately upon patient submission; admin retains post-publication edit/remove capability for policy violations; ModerationDecision entity replaced with AdminAction; admin-seeded reviews moved from Backlog to main scope per client transcription

#### **P-05 Mobile UX/UI Implementation Tasks**

- `IMPLEMENTATION_TASKS_P05_UXUI_2026-03-03.md` - Created Plane-ready UX/UI tasks for P-05 mobile flows (P05.1–P05.3) screens; assigned to Mr. Khue

### 2026-04-13/ (5 files)

#### **FR-022 Verification + FR-008 Provider Design Review**

- `FR022_VERIFICATION_FIXES_2026-04-13.md` - FR-022 fourth verification pass (v2.4): specialist filter removed from provider scope; B2 overflow workflow removed (pagination is sole model); REQ-022-009 moved to P2; 4 stale system PRD screen code cross-references updated; Active Status + Available Capacity filters added to FR-003/Screen 7a; Implementation Notes debounce corrected. **Fifth pass (v2.5)**: commission type corrected from "Tier-based" to "Flat Rate" (FR-015 sync gap); User Story 2 Scenario 3 status corrected to "Draft"; FR-001 auth dependency replaced with FR-031; PostgreSQL references removed (MySQL 8.0+ only); provider platform max search query length defined (200 chars)
- `FR008_PROVIDER_DESIGN_LAYOUT_VERIFICATION_2026-04-13.md` - FR-008 provider full-scope layout verification; Main Flow 1 is `🟡 PARTIAL`, Main Flow 2 is `🔴 BLOCKED` due to missing Path B detail-state coverage, missing `View Travel Details`, and misbound hotel review fields
- `FR022_FR019_ALIGNMENT_2026-04-13.md` - Applied selected FR-022 follow-up resolutions: moved FR-012 messaging search surfaces to P2 and reassigned provider messaging to PR-07, removed non-authoritative search-result export behavior outside deferred REQ-022-009, finalized FR-019 Screen 4 (Discount Code Catalog), and aligned the system PRD FR-022 summary
- `FR022_FOLLOWUP_ALIGNMENT_2026-04-13.md` - User-directed follow-up pass: aligned the system PRD Screen 7a summary to FR-003, removed Screen 5 export behavior from FR-012, and removed unsupported admin global/cross-module search claims from FR-022
- `FR022_STATUS_VERIFIED_2026-04-13.md` - Finalized FR-022 to the verified PRD state: status set to `✅ Verified & Approved`, approvals completed, and change log updated to match `prd-template.md`

### 2026-04-15/ (1 file)

#### **Hairline Mobile April 2026 Postman Collection Test**

- `HAIRLINE_MOBILE_APRIL_2026_POSTMAN_COLLECTION_TEST_2026-04-15.md` - Live sweep of the Hairline Mobile April 2026 API collection routes; 44 original endpoints were tested in the initial sweep, 29 of those are now confirmed meaningful, 7 return successful but sparse payloads pending product confirmation, 8 remain unresolved failures, and 25 follow-up validations were run separately to clear ambiguity. Follow-up checks confirmed the ISO-3 city lookup, meaningful `inquiry_id` payloads, brute-force quote-bearing inquiry coverage, successful provider profile and treatment update retries, an endpoint-correction retry guide for resolved endpoints including the quote decimal-precision rule, and a separate sparse-payload review for endpoints that may legitimately return empty arrays.
- **2026-04-20**: `POSTMAN_STATE_DEPENDENT_RETEST_2026-04-20.md` - Completed the state-dependent portion of the Apr 2026 collection report with Postman MCP retests. The confirmed-state travel updates still hard-lock after submission, duplicate review prevention still fires on the known completed quote, aftercare confirmation still stops at the Stripe client step, purchase history is still empty for the main test account, and the documented instructions route now returns HTML 404 during recheck.

### 2026-04-16/ (2 files)

#### **FR-014 Provider Dashboard Design Lock**

- `FR014_DASHBOARD_DESIGN_LOCK_2026-04-16.md` - FR-014 PRD major rewrite (v1.0 → v2.0) to match the finalized Provider Main Dashboard design (Figma node 6358-111596). Design is locked — do not reopen layout or widget-type decisions. Key changes: single-page cockpit (3 sections: A Inbox, B Performance, C Financials); global filters now Time range (default Last 4 weeks) + Country; cross-filtering specified; Section A (Inbox) fully specified with TTFQ tiles and inquiry queue; Section B widgets updated to funnel chart (correct stages), bullet chart (TTFQ vs SLA), calendar heatmap (Booking Intensity Index), and donut chart (Patient Location); Section C updated to area line (Earnings Trend), Pareto bar (Revenue by Treatment), stacked horizontal bar (Quote→Payment Aging, new), and column bar + inline table (Payouts); low-sample threshold changed from <5 to <30 inquiries.

#### **FR-014 12-Screen Analytics Suite Expansion**

- `FR014_12_SCREEN_EXPANSION_2026-04-16.md` - FR-014 PRD full expansion (v2.0 → v3.0): from 3 screens to 13-screen analytics suite (5 Provider + 7 Admin + 1 Export Config). Screen 1 remains locked. New provider screens: Performance & Conversion Deep-Dive (Screen 2), Patient Analytics (Screen 3), Finance & Payouts Deep-Dive (Screen 4), Pricing & Benchmarks (Screen 5). New admin screens: Platform Overview (Screen 6), Provider Performance & Engagement (Screen 7), Patient Acquisition & Funnel (Screen 8), Geographic Intelligence (Screen 9), Treatment Outcomes/Satisfaction (Screen 10), Financial Health & Cashflow (Screen 11), Pricing Intelligence (Screen 12). 104 functional requirements total (REQ-014-001 through REQ-014-104). All widgets verified against system-data-schema.md; data constraints documented (no team-level TTFQ, booking-level affiliate tracking only, satisfaction-only outcome proxy).

### 2026-04-17/ (3 files)

#### **FR-014 Verification Fixes**

- `FR014_VERIFICATION_FIXES_2026-04-17.md` - FR-014 PRD v3.0 → v3.1 post-verification fixes. Screen 7 admin drill-downs corrected (Tiles 4/5 → Screen 8; B4 → Screen 11; Section C financial tiles C1–C4 → Screen 12). Screen count narrative corrected to "13-screen suite (12 analytical + 1 export config)". `quotes.sent_at` and `quotes.accepted_at` timestamp columns added to system-data-schema.md (populated on status transitions; feed TTFQ and Quote→Payment aging analytics). System PRD FR-014 expanded with a dedicated Admin Requirements subsection (12 new bullets) covering platform overview, provider performance & engagement, patient acquisition, geographic intelligence, treatment outcomes, financial health, pricing intelligence, anonymisation, admin-configurable parameters, and audit logging. Screen 2 per-widget "minimum 10 inquiries" exception removed — unified under global Rule 7 (<30). Drill-down references standardised to number-only form. Approvals table placeholders replaced with "Pending review".
- `FR014_CODE_ALIGNED_FIXES_2026-04-17.md` - FR-014 PRD v3.1 → v3.2 code-alignment pass after source-code verification. Percentage-only commission analytics updated to support both Percentage and Flat Rate provider commission models. Dependency references corrected to the implemented sources (`providers.timezone`, `provider_commissions.type/price/payment_cycle`, `banking_details.currency`, `inquiry_providers`). Admin analytics restored to responsive-web scope. Provider-specific SLA storage documented as an unresolved canonical-data dependency.
- `FR014_VERIFICATION_FIXES_V2_2026-04-17.md` - FR-014 PRD v3.2 → v3.3 second verification round. Commission formula updated to conditional (percentage vs. flat-rate). Last-activity source resolved to `provider_activity_logs.action_at` after backend migration audit (confirmed `provider_users.last_login_at` does not exist; `provider_activity_logs` added to system-data-schema.md). SLA scoped to platform-wide configurable target in minutes (per-provider overrides deferred). Screen 7 B2 self-referential drill-down fixed to Screen 8. Module Scope corrected to 6-screen provider suite. Admin workflow extended to include Screens 11 and 13. Screen 6 export exclusion for Screen 1 documented. REQ numbering resequenced: Screen 6 moved to REQ-014-060–063; Screens 7–13 shifted to REQ-014-064–104 (continuous 001–104).

### 2026-04-18/ (2 files)

#### **FR-014 Backend Alignment**

- `FR014_BACKEND_ALIGNMENT_2026-04-18.md` - FR-014 follow-up alignment after the verification report. Backend cross-check confirmed patient-country provenance should normalize on `patients.location_id -> countries.id/name`, with legacy `patients.location` retained only as a temporary fallback for unmigrated rows. Removed the unsupported IP-geolocation fallback from FR-014, aligned the system PRD FR-014 SLA parameter to a single platform-wide target, and added Screen 6 export-service dependencies (`S-03` Notification Service, `S-05` Media Storage Service).

#### **FR-014 Verification Fixes v3.5**

- `FR014_VERIFICATION_FIXES_V35_2026-04-18.md` - FR-014 PRD v3.4 → v3.5 verification fixes. Screen 6 PDF branding narrowed to `providers.profile_image` only (colors-from-profile removed — no schema field). Rule 10 updated to cap FX fallback at 48 hours, beyond which affected widgets show "FX data unavailable". Added Assumption 8 recording that provider-side analytics widgets are PRD-derived by design (not a transcription discrepancy — future verification passes must not re-flag). Added Assumption 9 (FX freshness cap) and Assumption 10 (legacy `patients.location` fallback UI indicator).

### 2026-04-20/ (2 files)

#### **FR-017 Full-Scope Design Layout Verification**

- `FR017_DESIGN_LAYOUT_VERIFICATION_2026-04-20.md` - FR-017 full-scope layout verification; `F1`, `F4`, and `F7` are `🟢 COMPLETE`, `F2`, `F3`, `F5`, `F6`, and `F8` are `🟡 PARTIAL`; both provider-finance screens now have layout coverage, but Screen 10 is still incomplete because only the payout-detail state is evidenced

#### **Postman State-Dependent Retest**

- `POSTMAN_STATE_DEPENDENT_RETEST_2026-04-20.md` - Completed the `State-Dependent Failures` section in the Apr 2026 mobile API test report using live Postman MCP retests. Confirmed travel-update lock responses, duplicate-review protection, Stripe client-confirmation dependency, empty purchase history, no active aftercare state, and a new route discrepancy on `get-aftercare-instructions-medications`.

### 2026-03-06/ (1 file)

#### **P-06 + P-08 Mobile UX/UI Implementation Tasks**

- `IMPLEMENTATION_TASKS_P06_P08_UXUI_2026-03-06.md` - Created Plane-ready UX/UI tasks for P-06 and P-08 mobile flows (P06.1, P08.1), with one task per screen and Mr. Khue recorded as assignee

### 2026-03-09/ (1 file)

#### **FR-034 FE + BE Implementation Tasks**

- `IMPLEMENTATION_TASKS_FR034_2026-03-09.md` - Created Plane-ready FR-034 task breakdowns with frontend tasks split by admin screen and backend tasks grouped by broader support-center capabilities; assigned to Joachim Trung

### 2026-03-10/ (2 files)

#### **Testing Plan Alignment**

- `TESTING_PLAN_ALIGNMENT_2026-03-10.md` - Corrected automated testing-plan FR traceability, removed unsupported admin/provider registration assumptions, and replaced ambiguous expected outcomes with PRD-backed assertions
- `TESTING_PLAN_REVIEW_FIXES_2026-03-10.md` - Fixed stale manual auth scope, clarified canonical developer-report artifacts, and added missing FR traceability for automated password/payment coverage

### 2026-03-11/ (1 file)

#### **Legal Static Content Creation**

- `LEGAL_STATIC_CONTENT_2026-03-11.md` - Created first publishable draft set of public legal/support pages for Privacy Policy, Terms of Use, Contact Support, and Account Deletion under `local-docs/project-static-content/legal-content/`, aligned to current Hairline support, deletion, retention, and medical-data handling requirements

### 2026-03-18/ (1 file)

#### **Layout Audit Status Corrections**

- `AUDIT_REPORT_STATUS_CORRECTIONS_2026-03-18.md` - Corrected the missing mobile flows layout audit report to match the actual delivered layouts, downgrading overstated findings and aligning flow verdicts/action items to evidence-backed status

### 2026-03-19/ (2 files)

#### **Provider Dashboard Audit — Second-Pass Verification**

- `AUDIT_VERIFICATION_PROVIDER_2026-03-19.md` - Codebase verification pass on `audit_2026-03-18_provider.md`; 6 verdict corrections applied (P-ONB-016 CORRECT→BUG, P-QOT-035 NDR→BUG, P-APT-015 CORRECT→NDR, P-TRT-021 CORRECT→PARTIAL, P-TRT-028 NDR→PARTIAL, P-AFT-018 NDR→MISSING); 2 new P2 bugs added; overall totals updated to BUG 17, PARTIAL 62, CORRECT 171, MISSING 2, NDR 3

#### **Missing Mobile Flows Backend API Audit**

- `MISSING_MOBILE_FLOWS_BACKEND_API_AUDIT_2026-03-19.md` - Created a backend endpoint readiness audit for all 15 missing patient mobile flows, mapping each flow to existing patient-facing APIs, partial implementations, and missing backend contracts

### 2026-03-23/ (1 file)

#### **FR-025 Admin Dashboard Design Verification**

- `FR025_DESIGN_LAYOUT_VERIFICATION_2026-03-23.md` - Full FR-025 admin-dashboard layout verification against the approved PRD; Workflow 1, Workflow 2, and Workflow 4 blocked by missing set-level catalog/activation design and incomplete severity-preview coverage

### 2026-03-24/ (10 files)

#### **P01 Delete Account Design Layout Verification**

- `P01_DELETE_ACCOUNT_DESIGN_LAYOUT_VERIFICATION_2026-03-24.md` - Re-verified flow `P01.1 Delete Account` against the refreshed mobile layouts; all 3 screens now designed, overall flow verdict `🟡 PARTIAL` and user approval `🟢 Approved with minor issues`

#### **P01 Settings Screen Design Layout Verification**

- `P01_SETTINGS_SCREEN_DESIGN_LAYOUT_VERIFICATION_2026-03-24.md` - Re-verified flow `P01.2 Settings Screen` against the refreshed mobile layouts; all 5 screens now designed and the overall flow verdict is `🟢 COMPLETE`

#### **P01 Change Password Design Layout Verification**

- `P01_CHANGE_PASSWORD_DESIGN_LAYOUT_VERIFICATION_2026-03-24.md` - Verified flow `P01.3 Change Password` against the current mobile layouts; both primary screens are present, overall verdict remains `🟡 PARTIAL`, and approval was granted with deferred missing failure-state variants

#### **P02 Quote Request & Management Design Layout Verification**

- `P02_DESIGN_LAYOUT_VERIFICATION_2026-03-24.md` - Verified all four `P02` mobile flows against the current layout set; `P02.1` through `P02.4` are all `🟡 PARTIAL`, with follow-up work focused on missing state coverage and a few rule mismatches

#### **P03 Payment Methods Design Layout Verification**

- `P03_PAYMENT_METHODS_DESIGN_LAYOUT_VERIFICATION_2026-03-24.md` - Verified flow `P03.1 Payment Methods Management` against the current mobile layouts; all 3 screens are present, overall verdict is `🟡 PARTIAL`, and follow-up work is limited to edit-mode restrictions and remove-confirmation details

#### **P04 Travel & Logistics Design Layout Verification**

- `P04_TRAVEL_LOGISTICS_DESIGN_LAYOUT_VERIFICATION_2026-03-24.md` - Verified flows `P04.1` and `P04.2` against the current mobile layout set; both flows are `🔴 BLOCKED` due to passport-confirmation privacy issues, a missing `P04.2-S4` read-only travel-record screen, and itinerary/detail-state gaps

#### **P05 Aftercare & Progress Monitoring Design Layout Verification**

- `P05_AFTERCARE_PROGRESS_DESIGN_LAYOUT_VERIFICATION_2026-03-24.md` - Verified flows `P05.1`, `P05.2`, and `P05.3` against the current mobile layout set; `P05.1` is `🔴 BLOCKED`, `P05.2` is `🟢 COMPLETE`, and `P05.3` is `🟡 PARTIAL` due to a missing day-details popup and off-spec review-status terminology

#### **P06 Notification Design Layout Verification**

- `P06_NOTIFICATION_DESIGN_LAYOUT_VERIFICATION_2026-03-24.md` - Verified flow `P06.1 Notification Listing & Bubble` against the current mobile notification layouts; overall verdict is `🟡 PARTIAL` due to a missing back arrow, off-spec filter interaction model, and unread-state control mismatches

#### **P08 Help & Support Design Layout Verification**

- `P08_HELP_SUPPORT_DESIGN_LAYOUT_VERIFICATION_2026-03-24.md` - Verified flow `P08.1 Help & Support` against the current help-center mobile layouts; overall verdict is `🟡 PARTIAL` and the flow is approved with minor issues after downgrading the remaining gaps to UX/detail follow-up

#### **Aftercare FR-010 / FR-011 Relationship Audit**

- `AFTERCARE_FR010_FR011_RELATIONSHIP_AUDIT_2026-03-24.md` - Cross-mapped current Aftercare mobile layouts to `FR-010`, `FR-011`, and the `P05.*` mobile complement flows; found `FR011-W2`, `FR011-W2b`, `FR011-W3`, and `P05.1` still blocked, with `P05.2` complete and `P05.3` partial

### 2026-03-25/ (1 file)

#### **Aftercare FR-011 Mobile Scope Narrowing**

- `AFTERCARE_FR011_MOBILE_SCOPE_NARROWING_2026-03-25.md` - Narrowed the existing Aftercare relationship report to `FR-011` patient mobile screens only, removing `FR-010` / `P05.*` coverage from the report body while preserving the FR-011 field-level verification findings

### 2026-03-26/ (1 file)

#### **Layout Temp FR Audit**

- `LAYOUT_TEMP_FR_AUDIT_2026-03-26.md` - Cross-audited the current root-level `layout-temp/` folder to identify direct FR ownership, derived FR content references, and current compliance status across inquiry, quote comparison, quote detail, legal-policy, provider-profile, and treatment-detail layout clusters; this is the canonical consolidated report for the `2026-03-26` layout-temp review

### 2026-03-27/ (1 file)

#### **Missing Mobile Flows Manual Testing Tracker**

- `MISSING_MOBILE_FLOWS_MANUAL_TESTING_TRACKER_2026-03-27.md` - Created a single-table manual-testing tracker for all 15 missing mobile flows, with placeholders for progress, approval, correct items, incorrect items, further checks, and raw tester notes

### 2026-04-03/ (2 files)

#### **FR-025 Design Layout Re-Verification**

- `FR025_DESIGN_LAYOUT_VERIFICATION_2026-04-03.md` - Re-verified FR-025 Medical Questionnaire Management against 18 new admin layout files covering all 7 screens; 6/7 screens 🟢 GOOD+; S6 🟡 PARTIAL (Print Preview missing, non-critical); no required fields missing; 0 Critical UX issues; 13 UX Improvement + 5 UX Suggestion issues documented

#### **FR-022 Screen Specifications Overhaul**

*(See 2026-04-02 section for context — file dated 2026-04-03)*

---

### 2026-04-07/ (1 file)

#### **Mobile App Testing Report Progress Update**

- `MOBILE_APP_TESTING_REPORT_PROGRESS_UPDATE_2026-04-07.md` - Updated the April 6 patient mobile testing report and manual testing plan to reflect the current notification UI shell (bottom-nav entry point, empty state, visible search/filter/bulk actions) while keeping data-driven notification behavior blocked pending Firebase registration and backend delivery

---

### 2026-04-02/ (9 files)

#### **FR-017 Post-Verification Fixes (Round 2)**

- `FR017_POST_VERIFICATION_FIXES_2026-04-02.md` - 8 fixes applied after client transcription review: installment cutoff aligned to FR-029-configurable; discount creation removed from FR-017 system PRD entry; 2-person secondary approval for refunds removed (zero transcription evidence); FR-005 dependency corrected to FR-006; Screen 6 Affiliate Billing two-tab layout added per client request; Screen 3 Due Date provenance documented; integration numbering corrected 1/4/5→1/2/3; SC-019 concurrent admin target corrected from 500 to 50

#### **FR-017 Screen Completeness Audit Fixes**

- `FR017_SCREEN_COMPLETENESS_FIXES_2026-04-02.md` - 18-gap screen completeness audit: added Retry Payout action + Failed section (Screen 1); Approve Confirmation Modal (Screen 2); "At Risk" status + retry indicator (Screen 3); new Screen 3a Invoice Detail (installment schedule, payment history, refund history); new Screen 3b Refund Confirmation Modal; Overdue aging breakdown (Screen 5); Payment Method provenance + Process Payout confirmation + date filter (Screen 6); new Screen 7 Transaction Search & Audit Log; new Screen 8 Currency Alert Detail Modal; refunded treatment display + failed payout status (Screen 9); Failed status + provider message (Screen 10); Entity 1 and Entity 6 status enums corrected

#### **FR-017 Screen Operational Hardening**

- `FR017_SCREEN_OPERATIONAL_HARDENING_2026-04-02.md` - Added batch payout approval controls, dispute-resolution workflow support, re-authentication steps for financial actions, affiliate payout failure/retry handling, reconciliation metadata, reminder and override histories, dashboard exception KPIs, provider transparency improvements, and entity/requirement alignment for the hardened screen model

#### **FR-017 Decision Alignment**

- `FR017_DECISION_ALIGNMENT_2026-04-02.md` - Finalized the post-verification product decisions: FR-018 retains affiliate management/commission calculation while FR-017 owns affiliate billing and payout execution; provider payouts are approval-first with automatic payout-day processing in MVP; commission-adjustment routing corrected from FR-029 to FR-015; stale Super Admin secondary-approval wording removed

#### **FR-017 Second Completeness Audit Fixes**

- `FR017_SECOND_COMPLETENESS_AUDIT_2026-04-02.md` - 13-gap second-pass audit (v1.7→v1.8): Entity 5 action_type list corrected (6 missing values added); Entity 3 gained next_retry_date; Entity 2 gained Voided status + audit fields; Screen 1 added Active Currency Alerts KPI; Screen 2 added Unapprove + Void Statement actions with formal Batch Approval Confirmation Modal; Screen 4/4a added Send Reminder Confirmation Modal and Override Status re-auth requirement; Screen 5 added filter/search/CSV export; Screen 6 added Add Note action, Bulk Payout Toolbar, and Bulk Confirmation Modal; Screen 7 Target Payout Cycle clarified to select dropdown; duplicate FR-006 dependency removed; refund-after-payout edge case documented

#### **FR-017 Constitution and Ownership Alignment**

- `FR017_CONSTITUTION_AND_OWNERSHIP_ALIGNMENT_2026-04-02.md` - Finalized the agreed post-verification decisions across the constitution, FR-017, FR-015, and FR-029: removed mandatory multi-person refund approval from the constitution, split commission ownership between FR-029 global defaults and FR-015 provider-specific overrides, and normalized provider bank-detail ownership to FR-032 Billing Settings

#### **FR-017 Status Verification**

- `FR017_STATUS_VERIFIED_2026-04-02.md` - Updated FR-017 from Draft to ✅ Verified & Approved and aligned its approval metadata to the PRD template pattern used by other verified FRs

#### **FR-029 / FR-015 Commission Dual Management Alignment**

- `FR029_FR015_COMMISSION_DUAL_MANAGEMENT_2026-04-02.md` - Reversed the same-day global-only commission split in favor of the implemented design: FR-029 Screen 5 again manages provider-specific commission scopes alongside the global default, FR-015 remains the single-provider commission + payout-frequency surface, and FR-017 now consumes the shared effective commission configuration model

#### **FR-008 Provider Design Layout Verification**

- `FR008_PROVIDER_DESIGN_LAYOUT_VERIFICATION_2026-04-02.md` - Verified FR-008 provider screens 6-10 against the current layout set; both covered flows are `🔴 BLOCKED` because Screen 6 lacks the required travel-status tracker and Screen 10’s patient-owned review remains off-spec with forbidden editing, misbound hotel data, and missing flight submitted states

### 2026-04-01/ (3 files)

#### **FR-017 Scope Update**

- `FR017_SCOPE_UPDATE_2026-04-01.md` - FR-017 patient invoice history BACKLOG; provider section split Stage 1 (earnings) / Stage 2 (payouts); Screen 4 replaced with read-only discount usage view (creation deferred to FR-019); Stripe Account Management scope removed (owned by FR-029/A-09)

#### **FR-017 Verification Alignment**

- `FR017_VERIFICATION_ALIGNMENT_2026-04-01.md` - Applied accepted FR-017 verification resolutions: discount creation removed from FR-017 in favor of FR-019, provider commission ownership corrected to FR-015 with Percentage/Flat Rate support, payout approval clarified as buffer-window approval with payout-day Stripe processing, and MVP MFA wording aligned to the constitution

#### **FR-017 Post-Verification Fixes**

- `FR017_POST_VERIFICATION_FIXES_2026-04-01.md` - 9 fixes from FR-017 verification: replaced shared database with API (Constitution Principle I), added 5 missing dependencies (FR-006/018/029/030/032), renamed Commission % to Commission for dual model support, standardized approval threshold at £10,000, clarified dynamic currency pairs via FR-029, added buffer window to FR-029, added Conversion Rate provenance, updated system PRD payout schedule, reworded Assumption 7 for S-06

### 2026-03-30/ (1 file)

#### **Missing Mobile Flows Manual Testing Tracker Refresh**

- `MISSING_MOBILE_FLOWS_MANUAL_TESTING_TRACKER_REFRESH_2026-03-30.md` - Created a new dated baseline copy of the missing mobile flows manual-testing tracker for retesting the latest app version while preserving the prior round as comparison history

### 2026-03-28/ (3 files)

#### **FR-001 Screen Restructure & Renumber**

- `FR001_Screen_Renumber_2026-03-28.md` - Corrected screen misclassification in FR-001 prd.md: Screens 14–19 (patient profile, settings, account management) were placed under Admin; only Screen 13 was a genuine admin screen. Restructured section headings and renumbered all screens: patient Screens 1–18 sequential, admin Screen 19. Updated all cross-references in prd.md and 8 external files (update-logs, task-creation, reports).

#### **FR-026 / FR-001 Account Deletion Reasons Admin Management**

- `FR026_FR001_AccountDeletionReasons_2026-03-28.md` - Added "Account Deletion Reasons" as a new centrally managed App Data list in FR-026 (Screen 5b, workflow A5, 9 seeded options, Entity 7, REQ-026-012b). FR-001 Screen 16 validation rule and dependency updated. Report file updated. Mirrors Inquiry Cancellation Reasons pattern.

#### **FR-026 Verification Fixes (v1.3 → v1.4)**

- `FR026_VERIFICATION_FIXES_2026-03-28.md` - Applied 8 verification fixes: removed duplicate MFA bullet (deferred to FR-031); added flag_url to Entity 4 and REQ-026-011; added IP/device-level rate limiting as fixed-in-codebase; corrected stale FR-003 Screen 11 → Screen 8a (6 occurrences); fixed propagation test scenarios from 30 seconds to 1 minute; moved FR-024/FR-011 to Downstream Consumers section; standardised "Friend Referral" seeding data; corrected FR-003 module name to P-02: Quote Request & Management.

---

### 2026-04-09/ (1 file)

#### **Update Log Archive Reorganization**

- `UPDATE_LOG_ARCHIVE_REORGANIZATION_2026-04-09.md` - Moved the misplaced February 13, 2026 documentation reports out of `local-docs/project-automation/logs/` into `update-logs/2026-02-13/`, standardized their filenames, and refreshed the update-log index

### 2026-04-12/ (6 files)

#### **FR-022 Major Revision**

- `FR022_MAJOR_REVISION_2026-04-12.md` - FR-022 major revision: all business workflow flows converted to non-linear Mermaid diagrams (3 main + 6 alternative); all screen spec headings renamed to canonical `FR-XXX / Screen N` / `FR-XXX / Screen N / Tab M` format; Master Reference Table screen codes and gap markers corrected; 8 screen spec content corrections from cross-FR audit

#### **FR-022 Verification Fixes (Cross-FR Search/Filter Consistency)**

- `FR022_VERIFICATION_FIXES_2026-04-12.md` - 15 cross-FR search/filter consistency fixes: added FR-019/Screen 4 + FR-012/Screen 2 to Master Reference Table and screen specs; added A-06 module section; removed A-08 scope; fixed FR-016/Screen 7 (no search, added Show Only My Actions toggle); fixed FR-010/Screen 3 date default (All dates → Current month); removed wrong Clinician/Specialist filter from FR-011/Screen 8; removed "role" token from FR-009/Screen 10 search; added 3 new filters to FR-011/Screen 13; corrected debounce language in Rule 6 and Admin Editability; fixed performance SLA 500ms → 300ms in Performance Rule 1 and REQ-022-005; removed REQ-022-045/046; renamed Screen 11 heading to "Hairline Overview Dashboard"; updated FR-019 (v1.2), FR-011 (v1.3), and FR-005 (v1.5) with matching fixes

#### **FR-022 Scope Alignment**

- `FR022_SCOPE_ALIGNMENT_2026-04-12.md` - Applied selected post-verification resolutions: trimmed FR-022 provider-search scope to match FR-003 Screen 7a, removed deferred/untracked FR-022 search requirements without active screen coverage, and promoted Help Centre full-text search to explicit P1 scope across FR-035 and FR-033

#### **FR-022 Source-of-Truth Alignment (Follow-up)**

- `FR022_SOURCE_OF_TRUTH_ALIGNMENT_2026-04-12.md` - Follow-up alignment pass: added the remaining missing Help & Support screens from FR-035 and FR-032 into FR-022, corrected Provider Messages to source from FR-012 Screen 3 with exact filter behavior, and aligned A-02 provider-management search/filter wording plus FR-015 commission filter values to the admin dashboard model

#### **FR-022 Verification Round 2 Fixes**

- `FR022_VERIFICATION_ROUND2_2026-04-12.md` - Second verification pass: removed "treatment type" filter (absent from screen spec) from REQ-022-002, Module Scope, and Main Flow 1; fixed Main Flow 2 diagram nodes to match FR-015/Screen 1 exactly; removed P-03 and A-08 from FR-022 module list in system-prd.md; rewrote User Story 2/Scenario 2 to test Location filter (not search field); enumerated Transaction Search status options per record type; updated footer date and approvals table

#### **FR-022 Verification Round 3 Fixes**

- `FR022_VERIFICATION_ROUND3_2026-04-12.md` - Third verification pass (v2.3): resolved PHI masking gap — patient name excluded from provider-facing search (FR-003/Screen 9, FR-004/Screen 2) pre-payment confirmation; standardized all search matching to fuzzy (database full-text indexes) across all screen specs and rules; admin max search length corrected 100→200 chars; multi-select filter Logic column updated from AND to OR (within field) with disambiguation note in Control Behavior Standards; expanded Internal Dependencies with full 30+ FR source maintenance table; added Provider Platform entry points; added missing 300ms debounce to FR-035/Screen 1; marked REQ-022-009 export as P2 spec gap with TODO

### 2026-04-13/ (4 files)

#### **FR-022 Verification Round 4 Fixes**

- `FR022_VERIFICATION_FIXES_2026-04-13.md` - Fourth verification pass (v2.4): removed "specialist" from Module Scope PR-04 and REQ-022-039 (specialist filter is admin-only, not in provider screen spec); removed B2 overflow workflow (100-result truncation contradicted REQ-022-006 pagination — pagination is now sole model); moved REQ-022-009 export from P1 to P2 (incomplete spec); updated 4 stale system PRD screen code references (P-02-001→FR-003/Screen 7a, P-02-002→FR-005/Screen 1, A-01-007→FR-016/Screen 1, A-09-010→FR-031/Screen 5); added Active Status and Available Capacity filters to FR-003/Screen 7a per system PRD L441; corrected Implementation Notes debounce from blanket 500ms to 300–500ms per REQ-022-012
- `FR008_PROVIDER_DESIGN_LAYOUT_VERIFICATION_2026-04-13.md` - FR-008 provider full-scope layout verification; Main Flow 1 is `🟡 PARTIAL`, Main Flow 2 is `🔴 BLOCKED` due to missing Path B detail-state coverage, missing `View Travel Details`, and misbound hotel review fields
- `FR022_FOLLOWUP_ALIGNMENT_2026-04-13.md` - User-directed follow-up pass: aligned `system-prd.md` Screen 7a wording to FR-003, removed FR-012 conversation-export behavior, and removed unsupported FR-022 admin global/cross-module search claims
- `FR022_STATUS_VERIFIED_2026-04-13.md` - Verification completion pass: status changed to `✅ Verified & Approved`, approvals finalized, and footer/change-log metadata aligned to the template

---

## Quick Reference by Topic

### Documentation Updates

- **2025-10-23**: `DOCUMENTATION_UPDATES_2025-10-23.md` - Complete changelog
- **2025-10-27**: `CROSS_REFERENCE_UPDATES_2025-10-27.md` - Cross-reference fixes
- **2025-10-28**: `MODULE_RESTRUCTURE_2025-10-28.md` - Module structure changes
- **2026-03-10**: `TESTING_PLAN_ALIGNMENT_2026-03-10.md` - Automated testing-plan alignment to approved FR/system PRD scope
- **2026-03-10**: `TESTING_PLAN_REVIEW_FIXES_2026-03-10.md` - Manual/automated testing-plan follow-up fixes after review
- **2026-03-11**: `LEGAL_STATIC_CONTENT_2026-03-11.md` - Public legal/support page draft creation for Privacy Policy, Terms of Use, Contact Support, and Account Deletion
- **2026-03-18**: `AUDIT_REPORT_STATUS_CORRECTIONS_2026-03-18.md` - Corrected the missing mobile flows layout audit report to distinguish proven defects from pattern deviations and ambiguous static-state findings
- **2026-03-19**: `AUDIT_VERIFICATION_PROVIDER_2026-03-19.md` - Provider dashboard audit second-pass: 6 verdict corrections, 2 new P2 bugs (no self-revoke guard, no quote-edit status guard), totals updated
- **2026-03-19**: `MISSING_MOBILE_FLOWS_BACKEND_API_AUDIT_2026-03-19.md` - Backend endpoint readiness audit for all 15 missing patient mobile flows against `main/hairline-backend`
- **2026-04-07**: `MOBILE_APP_TESTING_REPORT_PROGRESS_UPDATE_2026-04-07.md` - April 6 patient mobile testing artifacts updated for notification coverage: bottom-nav entry point, empty state, visible search/filter/bulk actions recorded, while swipe/deep-link/data-driven behavior remains blocked pending Firebase registration and backend delivery
- **2026-04-15**: `HAIRLINE_MOBILE_APRIL_2026_POSTMAN_COLLECTION_TEST_2026-04-15.md` - Live API sweep of the Hairline Mobile April 2026 collection routes; 44 original endpoints were tested in the initial sweep, 29 are confirmed meaningful after follow-up validation, 7 return successful but sparse payloads pending product confirmation, 8 remain unresolved failures, and 25 follow-up validations were run separately to clear ambiguity. Follow-up checks verified that `GET /localization/get-cities/CAN` returns `200` when the country input is the ISO alpha-3 code, that quote-bearing inquiries return meaningful `quote/get-quotes` payloads, that `POST /settings/update-provider-profile` and `POST /treatment/update-treatment` succeed with the required IDs/payloads, and that the report now includes an endpoint-correction retry guide for resolved reruns, including the `quote_amount` decimal-precision rule
- **2026-04-23**: `BUG_REPORT_SKELETON_2026-04-23.md` - Created a concise mobile bug report table skeleton starting from `HL61`
- **2026-04-24**: `PROVIDER_ADMIN_MILESTONE_REPORT_2026-04-24.md` - Created Provider/Admin milestone status report with verified module completion estimates, risks, dependencies, and remaining effort; Mobile App deferred
- **2026-04-18**: `FR014_BACKEND_ALIGNMENT_2026-04-18.md` - FR-014 follow-up alignment after verification: backend cross-check confirmed canonical patient-country provenance is `patients.location_id -> countries.id/name`; FR-014 now documents legacy `patients.location` only as a temporary fallback, removes unsupported IP-geolocation fallback wording, aligns the system PRD SLA parameter to a platform-wide target, and adds Screen 6 service dependencies (`S-03`, `S-05`)
- **2026-04-18**: `FR014_VERIFICATION_FIXES_V35_2026-04-18.md` - FR-014 PRD v3.4 → v3.5 verification fixes: Screen 6 PDF branding narrowed to `providers.profile_image` only; Rule 10 FX fallback capped at 48 hours; Assumption 8 added to record provider-side analytics widgets as PRD-derived by design (future passes must not re-flag as transcription discrepancies); Assumptions 9–10 added for FX freshness cap and legacy location UI indicator

- **2026-02-13**: `PLANE_API_IMPROVEMENTS_2026-02-13.md` - `plane-api-commands` automation improvements: HTML cleanup, issue-update support, skip-parameter support, and sandbox-handling notes
- **2026-02-13**: `SECRETS_SCAN_REPORT_2026-02-13.md` - Secrets scan confirming no hardcoded credentials under `local-docs/project-automation`
- **2026-04-09**: `UPDATE_LOG_ARCHIVE_REORGANIZATION_2026-04-09.md` - Archive maintenance pass moving misplaced February 13 reports into the canonical `update-logs/2026-02-13/` bucket and standardizing their filenames

### Verification Reports

- **2025-10-23**: `VERIFICATION_REPORT_2025-10-23.md` - Comprehensive verification
- **2025-10-23**: `REQUIREMENTS_VERIFICATION_2025-10-23.md` - Requirements verification
- **2026-03-23**: `FR025_DESIGN_LAYOUT_VERIFICATION_2026-03-23.md` - FR-025 admin dashboard layout verification; 3 flows blocked due to missing or divergent designs
- **2026-03-24**: `P01_DELETE_ACCOUNT_DESIGN_LAYOUT_VERIFICATION_2026-03-24.md` - P01.1 delete-account mobile layout verification rerun; all screens now exist, overall verdict `🟡 PARTIAL` and approval `🟢 Approved with minor issues`
- **2026-03-24**: `P01_SETTINGS_SCREEN_DESIGN_LAYOUT_VERIFICATION_2026-03-24.md` - P01.2 settings-screen mobile layout verification rerun; all screens now exist and the overall verdict is `🟢 COMPLETE`
- **2026-03-24**: `P01_CHANGE_PASSWORD_DESIGN_LAYOUT_VERIFICATION_2026-03-24.md` - P01.3 change-password mobile layout verification; both primary screens exist, overall verdict `🟡 PARTIAL`, and approval was granted with deferred missing failure-state variants
- **2026-03-24**: `P02_DESIGN_LAYOUT_VERIFICATION_2026-03-24.md` - P02 quote-request mobile layout verification across `P02.1`–`P02.4`; all four flows are `🟡 PARTIAL` with targeted follow-up gaps documented in the per-flow reports
- **2026-03-24**: `P03_PAYMENT_METHODS_DESIGN_LAYOUT_VERIFICATION_2026-03-24.md` - P03.1 payment-methods mobile layout verification; all three screens exist, overall verdict `🟡 PARTIAL`, with targeted follow-up on edit-mode card restrictions and remove-confirmation identification
- **2026-03-24**: `P04_TRAVEL_LOGISTICS_DESIGN_LAYOUT_VERIFICATION_2026-03-24.md` - P04.1/P04.2 travel-logistics mobile layout verification; both flows are `🔴 BLOCKED` due to passport-confirmation privacy issues, missing `P04.2-S4`, and itinerary/detail-state gaps
- **2026-03-24**: `P05_AFTERCARE_PROGRESS_DESIGN_LAYOUT_VERIFICATION_2026-03-24.md` - P05 mobile layout verification across `P05.1`–`P05.3`; after a full in-progress-tab remap, `P05.1` is `🟡 PARTIAL`, `P05.2` is `🟢 COMPLETE`, and `P05.3` is `🟡 PARTIAL` with review-status terminology follow-up
- **2026-03-24**: `P06_NOTIFICATION_DESIGN_LAYOUT_VERIFICATION_2026-03-24.md` - P06.1 notification mobile layout verification; overall verdict `🟡 PARTIAL` because the delivered list omits back navigation and replaces the approved chip-bar filter model with a modal filter sheet
- **2026-03-24**: `P08_HELP_SUPPORT_DESIGN_LAYOUT_VERIFICATION_2026-03-24.md` - P08.1 help/support mobile layout verification; overall verdict `🟡 PARTIAL`, and the flow is approved with minor issues after treating the remaining gaps as UX/detail follow-up rather than blockers
- **2026-03-24**: `AFTERCARE_FR010_FR011_RELATIONSHIP_AUDIT_2026-03-24.md` - Broader Aftercare relationship audit across `FR-010`, `FR-011`, and `P05.*`; maps the current layout set across `aftercare/`, `in progress/`, and `reviews/`, with checkout, questionnaire, educational-resource, and day-detail gaps still blocking full alignment
- **2026-03-25**: `AFTERCARE_FR011_MOBILE_SCOPE_NARROWING_2026-03-25.md` - Scope update for the shared Aftercare report: it now serves as an `FR-011` patient-mobile-only verification artifact, with the broader `FR-010` / `P05.*` relationships removed from the report body
- **2026-03-26**: `LAYOUT_TEMP_FR_AUDIT_2026-03-26.md` - Canonical cross-audit of the current `layout-temp/` root folder; confirms 4 primary FR screen owners (`FR-003`, `FR-004`, `FR-005`, `FR-027`), 2 additional direct content relationships (`FR-024`, `FR-032`), and separates compliant, partial, reference-only, and unmapped layout families
- **2026-03-27**: `MISSING_MOBILE_FLOWS_MANUAL_TESTING_TRACKER_2026-03-27.md` - Created a reusable manual-testing tracker for all 15 missing mobile flows with per-row placeholders for progress, approval, correct items, incorrect items, further checks, and raw tester notes
- **2026-03-30**: `MISSING_MOBILE_FLOWS_MANUAL_TESTING_TRACKER_REFRESH_2026-03-30.md` - Created a new dated baseline copy of the missing mobile flows manual-testing tracker for a fresh app retest round while preserving the March 27 version as history
- **2026-04-02**: `FR008_PROVIDER_DESIGN_LAYOUT_VERIFICATION_2026-04-02.md` - FR-008 provider layout verification for Screens 6-10; both provider travel flows are `🔴 BLOCKED` because Screen 6 lacks the required travel summary/status actions and Screen 10’s patient self-booked review is still off-spec with forbidden editing, misbound hotel data, and missing flight submitted states
- **2026-04-13**: `FR008_PROVIDER_DESIGN_LAYOUT_VERIFICATION_2026-04-13.md` - FR-008 provider full-scope layout verification; Main Flow 1 is `🟡 PARTIAL`, Main Flow 2 is `🔴 BLOCKED` because Path B still lacks valid submitted flight-detail states and the tracker/detail handoff remains incomplete
- **2026-04-03**: `FR025_DESIGN_LAYOUT_VERIFICATION_2026-04-03.md` - FR-025 admin layout re-verification (all 7 screens, 18 files); 6/7 🟢 GOOD+; S6 🟡 PARTIAL (Print Preview missing); no required fields missing; 0 Critical UX issues

### Workflow Corrections

- **2025-10-23**: `WORKFLOW_CORRECTION_2025-10-23.md` - Provider Quote Management
- **2025-10-23**: `WORKFLOW_CLARIFICATION_2025-10-23.md` - Status transitions

### Architecture Changes

- **2025-10-23**: `TREATMENT_PACKAGE_CLARIFICATION_2025-10-23.md` - Treatments vs Packages
- **2025-10-28**: `MODULE_RESTRUCTURE_2025-10-28.md` - Provider Platform modules

### Functional Requirements

- **2025-10-23**: `REQUIREMENTS_IMPLEMENTATION_2025-10-23.md` - Implementation summary
- **2025-10-27**: `FR025_PRD_CREATION_2025-10-27.md` - FR-025 PRD creation
- **2025-10-28**: `FR001_PRD_CREATION_2025-10-28.md` - FR-001 PRD creation
- **2025-11-04**: `FR005_PRD_VERIFIED_2025-11-04.md` - FR-005 PRD verification
- **2025-11-06**: `FR026_ANALYSIS_C1_RESOLVED_2025-11-06.md` - FR-026 analysis and critical issues resolution
- **2026-02-25**: `FR025_VERIFICATION_UPDATES_2026-02-25.md` - FR-025 verification and system PRD alignment
- **2026-02-27**: `FR010_REVISION_2026-02-27.md` - FR-010 major revision: tabbed display model, entry point fix, day-by-day model, clinician model, status list, elapsed time removal, withdraw consent simplification, graft number, and Cancel button
- **2026-02-28**: `FR010_REVISION_2026-02-28.md` - FR-010 second revision: admin edit capability, Mermaid workflow conversion, 3-tenant screen specifications restructure
- **2026-03-02**: `IMPLEMENTATION_TASKS_FR012_2026-03-02.md` - FR-012 implementation task breakdowns (Provider + Admin focus)
- **2026-03-02**: `FR010_VERIFICATION_FIXES_2026-03-02.md` - FR-010 post-verification: 14 issues resolved (aftercare scope, media types, RBAC, clinician model, etc.)
- **2026-03-03**: `FR006_FR010_ALIGNMENT_2026-03-03.md` - FR-006/FR-010 alignment: Aftercare status, payment gating, No-Show label, medication free-text
- **2026-03-03**: `FR010_SCAN_PHOTOSET_DOC_CLEANUP_2026-03-03.md` - FR-010 scan photo set (V1) + scan-overlay wording cleanup across local docs; system PRD alignment
- **2026-03-03**: `FR010_ADMIN_OVERRIDE_SOFT_DELETE_DAY_MODEL_2026-03-03.md` - FR-010 admin override + soft delete + day-only In Progress model; FR-004 plan schema clarification
- **2026-03-03**: `FR010_PRD_VERIFIED_2026-03-03.md` - FR-010 PRD status set to Verified & Approved; approvals updated; footer confirmed aligned to template
- **2026-03-03**: `FR013_MODERATION_REMOVED_2026-03-03.md` - FR-013 moderation gate removed; reviews publish immediately; admin retains post-publication edit/remove
- **2026-03-03**: `IMPLEMENTATION_TASKS_P05_UXUI_2026-03-03.md` - P-05 mobile UX/UI implementation task breakdowns (P05.1–P05.3)
- **2026-03-06**: `IMPLEMENTATION_TASKS_P06_P08_UXUI_2026-03-06.md` - P-06 and P-08 mobile UX/UI implementation task breakdowns (P06.1, P08.1), one task per screen for Mr. Khue
- **2026-03-09**: `IMPLEMENTATION_TASKS_FR034_2026-03-09.md` - FR-034 support-center implementation task breakdowns with FE split by screens 1-7 and BE grouped into larger capability tasks for Joachim Trung
- **2026-03-28**: `FR001_Screen_Renumber_2026-03-28.md` - FR-001 screen section restructure and full renumber: patient Screens 1–18, admin Screen 19; 8 external files updated
- **2026-03-28**: `FR026_FR001_AccountDeletionReasons_2026-03-28.md` - FR-026 Account Deletion Reasons: new Screen 5b, workflow A5, 9 seeded options, Entity 7, REQ-026-012b; FR-001 Screen 16 dependency and validation rule updated
- **2026-03-28**: `FR026_VERIFICATION_FIXES_2026-03-28.md` - FR-026 v1.4 verification fixes: MFA deferred, flag_url added, IP rate limiting documented, FR-003 screen ref corrected, propagation test scenarios fixed, dependency direction corrected, seed data label aligned
- **2026-04-01**: `FR017_SCOPE_UPDATE_2026-04-01.md` - FR-017 scope update: patient invoice history BACKLOG; provider section split into Stage 1 (earnings tracking) / Stage 2 (payout consolidation); Screen 4 replaced with read-only discount usage view (creation moved to FR-019); Stripe Account Management removed from A-05 scope (owned by FR-029/A-09); Rules 7/8 and editability items redirected to FR-019/FR-029
- **2026-04-01**: `FR017_VERIFICATION_ALIGNMENT_2026-04-01.md` - FR-017 post-verification alignment: discount ownership fully moved to FR-019, provider commission contract corrected to FR-015, normal-cycle payout approval separated from payout-day Stripe processing, and MVP MFA wording aligned to the constitution
- **2026-04-01**: `FR017_POST_VERIFICATION_FIXES_2026-04-01.md` - 9 post-verification fixes across FR-017, FR-029, and system PRD: constitution compliance (shared DB → API), 5 missing dependencies, commission column dual-model support, approval threshold, dynamic currency pairs, buffer window ownership, data provenance, payout schedule, S-06 acknowledgment
- **2026-04-02**: `FR017_POST_VERIFICATION_FIXES_2026-04-02.md` - 8 fixes (round 2): installment cutoff moved from hardcoded to FR-029-configurable; system PRD discount creation removed from FR-017; 2-person refund approval removed (no client basis); FR-005 dependency corrected to FR-006; Screen 6 two-tab layout added per client transcription; Due Date provenance documented; integration numbering corrected; SC-019 concurrent admin target corrected to 50
- **2026-04-02**: `FR017_SCREEN_COMPLETENESS_FIXES_2026-04-02.md` - 18-gap screen completeness audit: added Retry Payout action + Failed section (Screen 1); Approve Confirmation Modal (Screen 2); "At Risk" status + retry indicator (Screen 3); new Screen 3a Invoice Detail (installment schedule, payment history, refund history); new Screen 3b Refund Confirmation Modal; Overdue aging breakdown (Screen 5); Payment Method provenance + Process Payout confirmation + date filter (Screen 6); new Screen 7 Transaction Search & Audit Log; new Screen 8 Currency Alert Detail Modal; refunded treatment display + failed payout status (Screen 9); Failed status + provider message (Screen 10); Entity 1 and Entity 6 status enums corrected
- **2026-04-02**: `FR017_SCREEN_OPERATIONAL_HARDENING_2026-04-02.md` - FR-017 screen model hardening: batch approval UX, payout readiness states, financial re-authentication, affiliate payout failure/retry handling, dispute-resolution controls, reminder/override histories, dashboard exception KPIs, and reconciliation metadata aligned across screens and entities
- **2026-04-02**: `FR017_DECISION_ALIGNMENT_2026-04-02.md` - Final decision alignment across FR-017 and system PRD: affiliate management/calculation stays in FR-018 while affiliate billing/payout execution moves under FR-017, provider payouts remain approval-first with automatic payout-day processing, commission routing points back to FR-015, and stale Super Admin secondary-approval wording is removed
- **2026-04-02**: `FR017_SECOND_COMPLETENESS_AUDIT_2026-04-02.md` - 13-gap second-pass audit (v1.7→v1.8): Entity 5 action_type list corrected (6 missing values); Entity 3 next_retry_date added; Entity 2 Voided status added; Screen 1 Active Currency Alerts KPI; Screen 2 Unapprove + Void Statement actions + Batch Approval Confirmation Modal; Screen 4/4a Send Reminder Confirmation Modal + Override Status re-auth; Screen 5 filter/search/CSV export; Screen 6 Add Note + Bulk Payout Toolbar + Bulk Confirmation Modal; Screen 7 Target Payout Cycle clarified; duplicate FR-006 dependency removed; refund-after-payout edge case documented
- **2026-04-02**: `FR017_CONSTITUTION_AND_OWNERSHIP_ALIGNMENT_2026-04-02.md` - Constitution + ownership normalization pass: refund governance changed from mandatory dual approval to documented justification + audit trail, commission ownership split between FR-029 global defaults and FR-015 provider-specific overrides, and provider bank details normalized to FR-032 Billing Settings
- **2026-04-02**: `FR017_STATUS_VERIFIED_2026-04-02.md` - FR-017 status transition: updated the PRD to ✅ Verified & Approved and aligned its approval metadata to the standard verified-template pattern
- **2026-04-02**: `FR029_FR015_COMMISSION_DUAL_MANAGEMENT_2026-04-02.md` - Restored dual commission-management surfaces to match the implemented admin design: FR-029 again manages provider-specific commission scopes centrally, FR-015 remains the single-provider commission + payout-frequency screen, and FR-017 was updated to consume the shared effective commission configuration
- **2026-04-03**: `FR022_SCREEN_SPECIFICATIONS_OVERHAUL_2026-04-03.md` - FR-022 Screen Specifications rewritten: three-tenant structure (Patient/Provider/Admin), 54-screen master reference table, Provider Platform screens added (PR-01–PR-06, previously missing), control behaviors mini-tables, maintenance convention note, system PRD FR-022 section updated with FR-022 as single source of truth
- **2026-04-03**: `FR025_DESIGN_LAYOUT_VERIFICATION_2026-04-03.md` - FR-025 admin layout re-verification against 18 new layout files (all 7 admin screens covered); 6/7 screens GOOD+; S6 PARTIAL (Print Preview missing, non-critical); 0 critical field gaps; 13 UX Improvement + 5 UX Suggestion issues identified
- **2026-04-12**: `FR022_MAJOR_REVISION_2026-04-12.md` - FR-022 major revision: all business workflow flows converted to non-linear Mermaid diagrams (3 main + 6 alternative flows); all screen specification headings renamed from invented module codes to canonical `FR-XXX / Screen N` / `FR-XXX / Screen N / Tab M` format; Master Reference Table screen codes and gap markers corrected; 8 screen spec content corrections from cross-FR audit (added filters, fixed status option enums)
- **2026-04-12**: `FR022_VERIFICATION_FIXES_2026-04-12.md` - 15 cross-FR search/filter consistency fixes across FR-022, FR-019, FR-011, and FR-005: new screens added to Master Reference Table and spec section (FR-019/Screen 4, FR-012/Screen 2, A-06 module); wrong fields removed (Clinician/Specialist from FR-011/Screen 8, role token from FR-009/Screen 10 search, search view from FR-016/Screen 7); filter additions (3 new filters to FR-011/Screen 13, Show Only My Actions toggle to FR-016/Screen 7); date default corrected (FR-010/Screen 3); debounce Rule 6 and performance SLA 300ms corrected; stale REQ-022-045/046 removed; screen name aligned (Hairline Overview Dashboard)
- **2026-04-12**: `FR022_SCOPE_ALIGNMENT_2026-04-12.md` - Post-verification resolution pass: FR-022 trimmed back to source-backed patient provider-search criteria, untracked/deferred FR-022 search requirements removed, and FR-035/FR-033 aligned to require Help Centre full-text search in P1
- **2026-04-12**: `FR022_SOURCE_OF_TRUTH_ALIGNMENT_2026-04-12.md` - Follow-up FR-022 alignment: added missing Help & Support hub/library/filter screens from FR-035 and FR-032, corrected Provider Messages to FR-012 Screen 3 with exact search/filter controls, and normalized A-02 provider-management criteria plus the FR-015 commission filter contract
- **2026-04-12**: `FR022_VERIFICATION_ROUND2_2026-04-12.md` - FR-022 second verification pass: removed unimplemented treatment type filter from REQ-022-002/Module Scope/Main Flow 1; fixed Main Flow 2 diagram nodes; removed P-03 and A-08 from system-prd.md FR-022 module list; rewrote User Story 2/Scenario 2; enumerated Transaction Search status options per record type; updated footer date and approvals table
- **2026-04-12**: `FR022_VERIFICATION_ROUND3_2026-04-12.md` - FR-022 third verification pass (v2.3): PHI masking gap fixed; all search standardized to fuzzy matching; admin max length 100→200 chars; filter Logic column OR-within-field with disambiguation note; expanded dependency table (30+ source FRs); Provider Platform entry points added; FR-035/Screen 1 debounce added; REQ-022-009 export marked P2 spec gap
- **2026-04-13**: `FR022_VERIFICATION_FIXES_2026-04-13.md` - FR-022 fourth verification pass (v2.4): specialist filter removed from provider scope; B2 overflow workflow removed (pagination is sole model); REQ-022-009 moved to P2; 4 stale system PRD screen code cross-references updated; Active Status + Available Capacity filters added to FR-003/Screen 7a; Implementation Notes debounce corrected. Fifth pass (v2.5): commission type "Tier-based" → "Flat Rate" (FR-015 sync gap); User Story 2 Scenario 3 status corrected to "Draft"; FR-001 auth dependency replaced with FR-031; PostgreSQL references removed (MySQL 8.0+ only); provider platform max query length defined (200 chars)
- **2026-04-13**: `FR022_FR019_ALIGNMENT_2026-04-13.md` - Selected resolution pass: moved FR-012 messaging search/filter surfaces to P2 and reassigned provider messaging to PR-07, removed non-authoritative search-result export behavior outside deferred REQ-022-009, finalized FR-019 Screen 4 (Discount Code Catalog), and aligned the system PRD FR-022 summary
- **2026-04-13**: `FR022_FOLLOWUP_ALIGNMENT_2026-04-13.md` - User-directed FR-022 follow-up alignment: system PRD Screen 7a wording reverted to match FR-003, FR-012 conversation export removed, and unsupported FR-022 admin global/cross-module search claims removed
- **2026-04-13**: `FR022_STATUS_VERIFIED_2026-04-13.md` - FR-022 verification completion: PRD status set to `✅ Verified & Approved`, approvals finalized, and governance metadata aligned to `prd-template.md`
- **2026-04-16**: `FR014_DASHBOARD_DESIGN_LOCK_2026-04-16.md` - FR-014 PRD v2.0: single-page cockpit design locked; Section A (Inbox with TTFQ), Section B (funnel, bullet chart, calendar heatmap, donut), Section C (area line, Pareto, aging stacked bar, payouts); global filters, cross-filtering, and all calculation specs documented
- **2026-04-16**: `FR014_12_SCREEN_EXPANSION_2026-04-16.md` - FR-014 PRD v3.0: expanded to 13-screen analytics suite (5 Provider + 7 Admin + 1 Export Config); 104 functional requirements; all widgets verified against schema; data constraints documented
- **2026-04-17**: `FR014_VERIFICATION_FIXES_2026-04-17.md` - FR-014 PRD v3.1 verification fixes: Screen 7 admin drill-downs corrected (Tiles 4/5 → Screen 8; B4 → Screen 11; C1–C4 → Screen 12); `quotes.sent_at`/`accepted_at` columns added to schema; system PRD FR-014 admin requirements subsection added (12 new bullets); screen count narrative unified to "13-screen suite (12 analytical + 1 export config)"; Screen 2 low-sample rule consolidated under Rule 7; approvals marked pending
- **2026-04-17**: `FR014_CODE_ALIGNED_FIXES_2026-04-17.md` - FR-014 PRD v3.2 code-alignment pass: financial analytics formulas updated to support both percentage and flat-rate provider commission models; dependency ownership corrected to code-backed sources (`provider_commissions`, `banking_details`, `inquiry_providers`, `providers.timezone`); admin analytics returned to responsive-web scope; provider-specific SLA persisted source still flagged as unresolved
- **2026-04-17**: `FR014_VERIFICATION_FIXES_V2_2026-04-17.md` - FR-014 PRD v3.3 second verification round: commission formula corrected to conditional (percentage/flat-rate); last-activity source resolved to `provider_activity_logs.action_at` (backend confirmed — `provider_users.last_login_at` never existed); `provider_activity_logs` added to system-data-schema.md; SLA scoped to platform-wide minutes (per-provider deferred); Screen 7 B2 drill-down fixed; admin workflow extended to Screens 11 + 13; REQ numbering resequenced 001–104 gap-free
- **2026-04-18**: `FR014_BACKEND_ALIGNMENT_2026-04-18.md` - FR-014 follow-up alignment: patient-country provenance normalized to `patients.location_id -> countries.name` with documented legacy fallback, unsupported geolocation fallback removed, system PRD FR-014 SLA wording aligned to platform-wide scope, and Screen 6 dependencies expanded to `S-03` and `S-05`
- **2026-04-18**: `FR014_VERIFICATION_FIXES_V35_2026-04-18.md` - FR-014 PRD v3.5: Screen 6 branding scoped to `providers.profile_image` (no brand colors in schema); Rule 10 FX fallback capped at 48h; provider-side analytics widgets formally accepted as PRD-derived (Assumption 8) so future verifications do not re-flag them as transcription gaps; legacy `patients.location` fallback given a UI indicator requirement
- **2026-04-20**: `FR017_DESIGN_LAYOUT_VERIFICATION_2026-04-20.md` - FR-017 full-scope layout verification; admin billing/investigation surfaces are mostly designed, provider payout batch states still have confirmation mismatches, `provider-earnings/` now covers Screen 9, and `payout-history/` now covers a partial Screen 10 payout-detail state while the parent list view remains missing

### Design Specifications

- **2026-03-03**: `P05_FLOWS_DESIGN_COMPLEMENT_2026-03-03.md` - P-05 flows (P05.1, P05.2, P05.3) fully specified in Missing Mobile Flows Design Complement report

### 2025-12-22/ (1 file)

#### **Provider Module Catalog Extension**

- `PROVIDER_COMMUNICATION_MODULE_2025-12-22.md` - Added `PR-07: Communication & Messaging` and aligned FR-012 + tracking docs

---

## Purpose

These reports serve as:

1. **Audit trail** for documentation changes
2. **Reference** for stakeholders reviewing updates
3. **Context** for development team during implementation
4. **Historical record** of decision-making process

---

## File Naming Convention

Update logs follow this naming convention:

```sh
{REPORT_TYPE}_{YYYY-MM-DD}.md
```

Example: `DOCUMENTATION_UPDATES_2025-10-23.md`

---

### 2026-04-03/ (1 file)

#### **FR-022 Screen Specifications Overhaul**

- `FR022_SCREEN_SPECIFICATIONS_OVERHAUL_2026-04-03.md` - Comprehensive rewrite of FR-022 Screen Specifications: three-tenant structure (Patient/Provider/Admin), 54-screen master reference table (Module → FR → Screen), Provider Platform screens fully added (PR-01–PR-06, previously missing), control behaviors mini-tables for all screens, maintenance convention note, Executive Summary and Module Scope updated, Functional Requirements Summary expanded (REQ-022-033 through REQ-022-056), system PRD FR-022 section priority corrected (P2→P1 for Provider/Admin) and pointers added at inline filter references

---

### 2026-04-22/ (1 file)

#### **Integrated Testing Plan — Patient Mobile App**

- `TESTING_PLAN_2026-04-22.md` - Created comprehensive integrated testing plan & live report skeleton for patient mobile app: 79 test cases across Inquiries, Offers, In Progress, and Aftercare modules; covers happy, edge, and error cases with full mock data and agent fill-in guide

### 2026-04-23/ (1 file)

#### **Mobile Bug Report Skeleton**

- `BUG_REPORT_SKELETON_2026-04-23.md` - Created concise mobile bug report table skeleton starting from `HL61`

### 2026-04-24/ (1 file)

#### **Provider/Admin Milestone Status Report**

- `PROVIDER_ADMIN_MILESTONE_REPORT_2026-04-24.md` - Created the April 24 milestone status report using the January 27 report skeleton; Provider modules PR-01–PR-07 and Admin rows A-01–A-10 were re-verified against current frontend/backend code and relevant PRDs/FRs, with Mobile App intentionally deferred

---

**Last Updated**: April 24, 2026
