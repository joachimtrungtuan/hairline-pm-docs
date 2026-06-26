# Code Map — hairline-frontend (React 18 + Vite + Redux Toolkit/RTK Query; serves Provider web + Admin web dashboards)

Curated folder-group map (folder-level, not file-level — refresh when modules are
added/restructured, flagged by check-code-map-drift.sh). For the SIGNATURES of one
subdir on demand (do NOT persist): repomix <subdir> --compress --remove-comments --style markdown -o -
**Locator, not evidence:** this map tells you WHERE to look; read the actual source for any
finding. It exists to prevent broad searches, never to replace reading the code.

One React SPA hosting BOTH the Provider dashboard and the Admin (internal "team")
dashboard, gated by role/route. The platform split runs through three parallel trees:
`features/hairlineProvider/*` + `pages/providerDashboard/*` + `components/providerComponents/*`
= Provider (PR-0x); `features/hairlineTeam/*` + `pages/teamDashboard/*` + `components/teamComponents/*`
= Admin (A-0x); `features/auth` + `features/common` + `components/shared` = cross-cutting (S-0x).
Data access is RTK Query: every `*ApiSlice` injects endpoints into the root `apiSlice`.
Module codes: Provider PR-01..PR-07, Admin A-01..A-10, Shared S-01..S-06.

## app/
- **Purpose:** Redux store + root RTK Query `apiSlice` (base query, auth header, tag types). Every feature slice injects into this.
- **Modules:** — (infra).
- **FRs:** —.
- **Entry points / key files:** `app/store.jsx`, `app/api/apiSlice.jsx`.

## features/auth/ + features/common/ + features/provider/ + features/both/
- **Purpose:** Cross-cutting data slices. `auth` = login/token state; `common` = shared lookup queries; `provider` = provider entity slice shared by both dashboards; `both/timeline` = workflow-timeline slice used by both platforms.
- **Modules:** S-03, PR-01, A.
- **FRs:** FR-001, FR-009, FR-022.
- **Entry points / key files:** `features/auth/authApiSlice.jsx`, `features/auth/authSlice.jsx`.

## features/hairlineProvider/ (RTK Query slices)
- **Purpose:** All Provider-platform data slices: aftercare + aftercare-chat, analytics/financial-forecast, appointments/quotes, dashboard, helpCentre, inquiries, notifications, patientManagement, patient↔provider chat (incl. optimistic `sendState` message state machine), profileSettings, promotions.
- **Modules:** PR-02, PR-03, PR-04, PR-05, PR-06, PR-07.
- **FRs:** FR-003, FR-004, FR-010, FR-011, FR-012, FR-014, FR-019, FR-032, FR-033.
- **Entry points / key files:** `inquiries/inquiriesApiSlice.jsx`, `appointments/quotesApiSlice.jsx`, `patientProviderChat/chatApiSlice.jsx`, `patientProviderChat/sendState/useOutgoingMessageMachine.js`.

## features/hairlineTeam/ (RTK Query slices)
- **Purpose:** All Admin-platform data slices: affiliateManagement, analytics (+fixtures), localization, notifications, patientManagement (incl. deletion requests), promotions, reviews, settings (large: currency/conversion, legal docs, OTP, payment config, questionnaire catalog, split payment, throttling, discovery questions, etc.), supportCenter (+ aftercare support), teamOverView, standalone aftercare.
- **Modules:** A-01, A-02, A-05, A-06, A-07, A-08, A-09, A-10.
- **FRs:** FR-015, FR-016, FR-017, FR-018, FR-019, FR-021, FR-023..FR-031, FR-034.
- **Entry points / key files:** `settings/` slices, `reviews/reviewsApiSlice.jsx`, `promotions/promotionsApiSlice.jsx`, `analytics/analyticsApiSlice.jsx`.

## pages/auth/
- **Purpose:** Login, signup, forgot-password, invitation landing/signup screens (shared by both platforms).
- **Modules:** S, PR-01.
- **FRs:** FR-001, FR-009.
- **Entry points / key files:** `pages/auth/login/Login.jsx`, `pages/auth/invitation/InvitationLanding.jsx`.

## pages/providerDashboard/ (Provider screens)
- **Purpose:** Provider UI screens. Major sub-areas: addTreatment, afterCareDetails (milestones, clinician, instructions, medications), appointments (inquiry/quote detail, travel, medical questionnaires, treatment plan, visual evidence), communication (aftercare chat), packages, patientManagement (in-progress / completed treatment), patientProviderChat, promotions, providerProfile, treatments/pricingConfig, team, analytics sections, plus root pages (Dashboard, Finance, EarningsTracker, Performance, Reviews, Questionnaires, HelpCenter, PayoutHistory).
- **Modules:** PR-02, PR-03, PR-04, PR-05, PR-06, PR-07.
- **FRs:** FR-003, FR-004, FR-006, FR-010, FR-011, FR-012, FR-013, FR-014, FR-024, FR-032, FR-033.
- **Entry points / key files:** `pages/providerDashboard/Dashboard.jsx`, `appointments/InquiryDetail.jsx`, `appointments/QuoteDetails.jsx`, `AfterCareDetails.jsx`.

## pages/teamDashboard/ (Admin screens)
- **Purpose:** Admin UI screens — the largest page tree. Sub-areas: addProvider/editAffiliate/addAffiliate (multi-step), adminLocalization (json import, machine translation, version history, key inventory/detail), adminReviewsManagement (list/detail/settings/takedown), affiliateManagement, afterCare (standalone aftercare + clinician chat + tabs), analytics (platform overview + financial-health/geographic/patient-acquisition/pricing/provider-performance/treatment-outcomes workspaces + transaction search), billingFinance, hairline-promotions, hairlineFundedCodesManager, packages, patients (detail/billing/communication/payment), promotionAnalyticsApplications, promotionDetail, promotionProgramHub, providerAdoptionManager, providerDetails, providerPromotionPortfolio, providers (payout/billing/staff), settings (very large: currency, questionnaire catalog, support center config, roles/permissions, legal docs, country/discovery, notifications, payment config, provider/patient FAQ & resources & tutorials), support-center (ticketing + chat).
- **Modules:** A-01, A-02, A-03, A-05, A-06, A-07, A-08, A-09, A-10.
- **FRs:** FR-015..FR-019, FR-021, FR-023..FR-031, FR-033, FR-034, FR-036.
- **Entry points / key files:** `teamDashboard/analytics/platformOverview/PlatformOverview.jsx`, `adminReviewsManagement/AdminReviewsManagement.jsx`, `settings/SupportCenterConfig.jsx`, `promotionProgramHub/PromotionProgramHub.jsx`.

## pages/public/
- **Purpose:** Unauthenticated public legal pages (terms/privacy render).
- **Modules:** A-09.
- **FRs:** FR-027.
- **Entry points / key files:** `pages/public/PublicLegalPage.jsx`.

## components/providerComponents/
- **Purpose:** Provider-specific UI building blocks: afterCare forms (clinician/instruction/medication/milestone/patient/review/template steps), createQuoteStep (treatment selection, pricing, promotions), dashBoardComponent (appointments tables, patient management, charts), helpCentre, hotelAndFlight, inProgress, makeScheduleStep, notifications, onboarding tour, package, promotions, providerProfile, providerSettings, team, treatment.
- **Modules:** PR-02, PR-03, PR-04, PR-05, PR-06, PR-07.
- **FRs:** FR-004, FR-006, FR-009, FR-010, FR-011, FR-014, FR-019, FR-032.
- **Entry points / key files:** `createQuoteStep/`, `dashBoardComponent/appointments/`, `afterCare/`.

## components/teamComponents/ + components/adminComponents/ + components/admin/
- **Purpose:** Admin-specific UI blocks: addProviderSteps/addAffiliateSteps (wizards), billing, package, providerDetailsComponents, settings (afterCareQuestionnaire, appSettings, notification templates/rules), teamDashboardComponents, treatmentComponents; admin notification dropdown; feature-flag/edit-patient admin widgets.
- **Modules:** A-01, A-02, A-06, A-07, A-09.
- **FRs:** FR-015, FR-016, FR-018, FR-019, FR-024, FR-025, FR-030.
- **Entry points / key files:** `teamComponents/addProviderSteps/`, `teamComponents/settings/`, `adminComponents/notifications/AdminNotificationDropdown.jsx`.

## components/shared/ + components/analytics/ + components/icons/ + components/PhoneInput/ + components/ProviderAvatar/
- **Purpose:** Reusable cross-platform UI: navBar, sideBar/sidebarMenu, breadcrumb, filterDrawer (per-domain filter drawers), DataTable, timeline, pageTitle, accessDenied, icons; shared analytics chart components; phone input & avatar widgets; root-level CallButton / IncomingCallHandler / InvoicesList.
- **Modules:** S-03, — (cross-cutting UI).
- **FRs:** FR-012, FR-022.
- **Entry points / key files:** `shared/navBar/NavBar.jsx`, `shared/DataTable.jsx`, `shared/sideBar/SideBar.jsx`.

## hooks/
- **Purpose:** Custom React hooks: useAuth, useDebounce, useFcmNotifications, useFeatureFlag, useFetch, useGlobalChatNotifications, useIncomingCall, usePasswordValidation.
- **Modules:** S-03, PR-01.
- **FRs:** FR-001, FR-012, FR-020.
- **Entry points / key files:** `hooks/useAuth.jsx`, `hooks/useFcmNotifications.jsx`.

## utils/ + services/
- **Purpose:** Cross-cutting helpers: accessControl (config + RBAC gate), PrivateRoute/PublicRoute guards, baseUrl, maskSensitiveValues, stepValidation, travelHotelStatus, urlHelper; `services/callService.js` (Twilio call orchestration).
- **Modules:** A-09 (access control), S-04 (travel).
- **FRs:** FR-031, FR-008, FR-012.
- **Entry points / key files:** `utils/accessControl.js`, `utils/PrivateRoute.jsx`, `services/callService.js`.

## data/
- **Purpose:** Static/mock data and reference catalogs: notification event catalog, discount-usage mock data, aftercare overview mock + types, quote-edit role matrix. Used as fixtures/reference, not live data.
- **Modules:** — (reference/fixtures).
- **FRs:** —.
- **Entry points / key files:** `data/notificationEventCatalog.js`, `data/quote-edit-role-matrix.md`.

## assets/
- **Purpose:** Static images, icons (incl. filter icons), SVGs.
- **Modules:** — (static).
- **FRs:** —.
- **Entry points / key files:** `assets/images/`, `assets/icons/`.

## src root (App.jsx, main.jsx, firebase.js, echo.js, style.scss)
- **Purpose:** App bootstrap and routing (`App.jsx` defines React Router v6 routes — the screen-to-URL map), Vite entry (`main.jsx`), Firebase/FCM init, Laravel Echo websocket setup, global styles.
- **Modules:** — (infra), S-03.
- **FRs:** FR-012, FR-020.
- **Entry points / key files:** `App.jsx` (route table), `firebase.js`, `echo.js`.

## Notes / unmapped
- The tech-spec's `Frontend Architecture (Web)` shows a slimmed structure; the live tree is far broader (many analytics/settings workspaces) — this map supersedes it.
- Numerous `BACKEND_INTEGRATION*.md` files live inside feature folders (esp. teamDashboard); they are dev integration notes keyed to HAIRL-#### tickets, not code.
- `.backup`, `copy`, and `*Test`/`*Debug` files (e.g. `Information.jsx.backup`, `AppointmentDetail copy.jsx`, several `TTFQvsSLAChart*Test.jsx`) are stray dev artifacts — do not treat as canonical entry points.
- The web app does NOT serve patients (patient UI is the Flutter app). Any "patient" pages here are admin/provider views OF patients (PatientDetail, patient management), not the patient client.
- FR bindings are best-effort from PRD module codes; `—` = cross-cutting/infra.
