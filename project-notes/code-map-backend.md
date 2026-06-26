# Code Map — hairline-backend (Laravel 10 API; serves all 3 platforms: Patient mobile, Provider web, Admin web)

Curated folder-group map (folder-level, not file-level — refresh when modules are
added/restructured, flagged by check-code-map-drift.sh). For the SIGNATURES of one
subdir on demand (do NOT persist): repomix <subdir> --compress --remove-comments --style markdown -o -
**Locator, not evidence:** this map tells you WHERE to look; read the actual source for any
finding. It exists to prevent broad searches, never to replace reading the code.

Single Laravel codebase exposing one REST API (OAuth2 / Laravel Passport) consumed by
all three clients. Boundary is by URL prefix in `routes/api.php` (`/auth`, `/patient*`,
`/provider*`, `/admin*`, plus shared `/help-centre`, `/chat`, `/calls`, `/quote`,
`/inquiry`). Controllers, Requests, Resources and Services mirror those domains.
Module codes: Patient P-01..P-08, Provider PR-01..PR-07, Admin A-01..A-10, Shared
S-01..S-06. Models map to entities in `system-data-schema.md`.

## routes/ (api.php, channels.php, console.php, web.php)
- **Purpose:** The authoritative module map. `api.php` (~2.3k lines) declares every endpoint grouped by prefix; the prefix tree is the source of truth for which controller serves which platform/module. `channels.php` = broadcast auth (chat/calls); `console.php` = scheduled commands; `web.php` minimal.
- **Modules:** all (cross-platform routing surface).
- **FRs:** all.
- **Entry points / key files:** `routes/api.php` (read prefix groups first); `routes/channels.php`.

## app/Http/Controllers/Authentication/ + Authentication routes
- **Purpose:** Login, registration, OTP, password reset, token issuance for patient/provider/admin guards.
- **Modules:** P-01, PR-01, A (auth surface).
- **FRs:** FR-001, FR-009.
- **Entry points / key files:** `AuthController.php`.

## app/Http/Controllers/Patients/ (incl. Patients/HelpCentre/)
- **Purpose:** Patient-facing account, profile, head photos, destinations, payment methods, reviews, suspension, treatment history, support tickets, help-centre articles. Mobile app's primary backend.
- **Modules:** P-01, P-02, P-03, P-05, P-08.
- **FRs:** FR-001, FR-002, FR-005, FR-007, FR-013, FR-035.
- **Entry points / key files:** `PatientController.php`, `PatientHeadPhotoController.php`, `PatientSupportTicketController.php`.

## app/Http/Controllers/Inquiry/ + Quotes/ + Bookings/
- **Purpose:** Inquiry submission/distribution, quote lifecycle (incl. flights/hotels/schedule sub-resources), booking & scheduling. Spans patient request side and provider response side.
- **Modules:** P-02, P-03, PR-02, A-01.
- **FRs:** FR-003, FR-004, FR-005, FR-006, FR-008.
- **Entry points / key files:** `Inquiry/InquiryController.php`, `Quotes/QuotesController.php`, `Bookings/BookingController.php`.

## app/Http/Controllers/Provider/ + Providers/ (incl. Providers/HelpCentre/)
- **Purpose:** Provider self-service: activation, team & staff invitations, role/permissions, campaigns, my-promotions, reviews, notifications, locale, translation bundles, provider/staff user management, provider support cases, help-centre content.
- **Modules:** PR-01, PR-02, PR-05, PR-06, PR-07.
- **FRs:** FR-009, FR-019, FR-032, FR-033.
- **Entry points / key files:** `Provider/ProviderActivationController.php`, `Provider/ProviderTeamController.php`, `Providers/ProviderController.php`.

## app/Http/Controllers/Packages/ + Performance/ + (Treatment* root controllers)
- **Purpose:** Treatment & package catalog, treatment execution/documentation, treatment plans (notes, daily entries, scans), performance/outcome reporting. Root-level `TreatmentExecutionController`, `TreatmentPhotoController`, `TreatmentPlan*Controller`.
- **Modules:** PR-03, PR-06, A-09.
- **FRs:** FR-010, FR-024.
- **Entry points / key files:** `Packages/TreatmentController.php`, `TreatmentExecutionController.php`, `Performance/ProviderPerformanceReportController.php`.

## app/Http/Controllers/PatientManagement/ + (Aftercare root controllers)
- **Purpose:** Aftercare & recovery: aftercare plans, milestones, milestone scans, standalone aftercare requests, in-progress patient tracking.
- **Modules:** P-05, PR-04, A-03.
- **FRs:** FR-011.
- **Entry points / key files:** `PatientManagement/AfterCareController.php`, `PatientManagement/StandaloneAftercareController.php`, `PatientManagement/AftercareMilestoneScanController.php`.

## app/Http/Controllers/Chat/ + Notifications/ + TwilioCallController + Webhooks/
- **Purpose:** Messaging (patient↔provider chat, aftercare chat), device-token registration, Twilio voice/video calls, inbound Stripe & Twilio webhooks.
- **Modules:** P-06, PR-07, A-10, S-03.
- **FRs:** FR-012, FR-020.
- **Entry points / key files:** `Chat/ChatController.php`, `Chat/AftercareChatController.php`, `TwilioCallController.php`, `Webhooks/StripeWebhookController.php`.

## app/Http/Controllers/Payments/ + Billing/ + Finance/
- **Purpose:** Payment intents/confirmation, installments/split payment, patient & provider billing, payouts (provider + affiliate), finance reporting, transaction search, financial audit, currency alerts.
- **Modules:** P-03, A-05, PR-05, S-02.
- **FRs:** FR-007, FR-007B, FR-017, FR-014.
- **Entry points / key files:** `Payments/PaymentController.php`, `Billing/ProviderBillingController.php`, `Finance/FinanceReportingController.php`.

## app/Http/Controllers/Analytics/ + Dashboard/
- **Purpose:** Provider analytics & exports, provider/hairline dashboards, finance/pricing analytics, overview metrics.
- **Modules:** PR-05, A-08.
- **FRs:** FR-014.
- **Entry points / key files:** `Analytics/AnalyticsController.php`, `Dashboard/ProviderDashboardController.php`, `Dashboard/HairlineDashboardController.php`.

## app/Http/Controllers/Affiliate/
- **Purpose:** Affiliate program (codes, commissions, payouts) — affiliate-facing surface; admin-side affiliate management lives under Admin controllers + Billing payouts.
- **Modules:** A-07.
- **FRs:** FR-018.
- **Entry points / key files:** `Affiliate/AffiliateController.php`.

## app/Http/Controllers/Admin/ (incl. Admin/HelpCentre/)
- **Purpose:** Largest controller group — admin operations: provider onboarding/adoption/impersonation/portfolio/team, patient management & deletion requests, reviews moderation/export/settings, promotions hub/detail/analytics, translation/locale management, notifications & templates, commission rates, support cases, aftercare templates/discount codes, audit trail, payment configuration, patient invoices.
- **Modules:** A-01, A-02, A-03, A-06, A-08, A-09, A-10.
- **FRs:** FR-015, FR-016, FR-019, FR-021, FR-027, FR-029, FR-030, FR-031, FR-033, FR-034, FR-036.
- **Entry points / key files:** `Admin/ProviderManagementController.php`, `Admin/AdminPromotionHubController.php`, `Admin/AdminReviewModerationController.php`, `Admin/AdminTranslationKeyController.php`.

## app/Http/Controllers/Settings/
- **Purpose:** System & platform configuration: app/general settings, after-care settings & resources, banking, billing, country/discovery questions, email/OTP templates, legal documents, notification preferences, auth throttling, provider/patient settings, terms & conditions.
- **Modules:** A-09, PR-06.
- **FRs:** FR-021, FR-023, FR-025, FR-026, FR-027, FR-028, FR-029, FR-030, FR-032.
- **Entry points / key files:** `Settings/SettingsController.php`, `Settings/AppSettingController.php`, `Settings/LegalDocumentController.php`.

## app/Http/Controllers/Questionnaire/
- **Purpose:** Medical questionnaire catalog: categories, contexts, questions, sets, preview/versioning.
- **Modules:** A-09.
- **FRs:** FR-025, FR-002.
- **Entry points / key files:** `Questionnaire/QuestionnaireSetController.php`, `Questionnaire/QuestionnaireQuestionController.php`.

## app/Http/Controllers/HelpCentre/ + Permission/ + Essentials/ + Common/ + Travel/ + Internal/
- **Purpose:** Cross-cutting support surfaces. HelpCentre = patient/provider FAQ/resource/tutorial/video read APIs; Permission = RBAC role/permission endpoints; Essentials = countries/cities, discounts, passport, status options, workflow timeline; Common = shared lookup data; Travel = itinerary & travel notifications; Internal = internal notification dispatch/render.
- **Modules:** S-03, S-04, S-06, A-09, PR-01.
- **FRs:** FR-008, FR-020, FR-031, FR-033, FR-022.
- **Entry points / key files:** `Permission/RolePermissionController.php`, `Travel/TravelItineraryController.php`, `Internal/NotificationDispatchController.php`.

## app/Http/Controllers/ (root-level controllers)
- **Purpose:** Misc cross-cutting endpoints not in a domain subfolder: currency & currency-conversion config, deposit rates, files, legal pages (public), locations & regional groups, reviews, location pricing.
- **Modules:** A-05, A-09, S-05, S-02.
- **FRs:** FR-028, FR-029, FR-007, FR-013, FR-027.
- **Entry points / key files:** `CurrencyController.php`, `FileController.php`, `LocationController.php`, `Controller.php` (base).

## app/Http/Middleware/
- **Purpose:** Request guards: auth, scope/access checks (`CheckProviderAccess`, `CheckScopes`), suspension checks (admin/patient/provider), patient verification, authorization-denial logging, help-centre view tracking, version-modification prevention.
- **Modules:** — (cross-cutting infra).
- **FRs:** FR-031, FR-001, FR-026.
- **Entry points / key files:** `Authenticate.php`, `CheckProviderAccess.php`, `CheckScopes.php`.

## app/Http/Requests/ (Admin/, Patient/, Provider/, Questionnaire/, Quote/, + root)
- **Purpose:** Form-request validation classes, namespaced to mirror controllers. Define input contracts per endpoint.
- **Modules:** matches owning controller domain.
- **FRs:** validation for the FRs of their domain.
- **Entry points / key files:** browse the subfolder matching the controller you're tracing (e.g. `Requests/Admin/Review/`).

## app/Http/Resources/ (incl. Admin/)
- **Purpose:** API response transformers (JSON shaping). Sparse — only a subset of endpoints use formal Resources (questionnaire, support-case, admin review).
- **Modules:** — (presentation).
- **FRs:** —.
- **Entry points / key files:** `Resources/Admin/AdminReviewDetailResource.php`, `Resources/SupportCaseResource.php`.

## app/Models/ (incl. Models/Support/, Models/Traits/)
- **Purpose:** ~240 Eloquent models — the persistence layer. Each maps to a table/entity in `system-data-schema.md`. Covers every domain: patients/providers/quotes/inquiries/bookings/payments/aftercare/reviews/promotions/affiliates/translations/support/notifications/currency/questionnaires. `Traits/` = shared model behavior (HasUuid, HasImageUrl, HasScheduledRoles); `Support/` = support-center config models.
- **Modules:** all.
- **FRs:** all (data layer). Conceptually maps to schema entities in `system-data-schema.md`.
- **Entry points / key files:** `Patient.php`, `Provider.php`, `Quote.php`, `Inquiry.php`, `Payment.php`, `AfterCare.php`.

## app/Services/ (incl. Admin/, Analytics/, Finance/, Push/, RBAC/, Travel/)
- **Purpose:** Business-logic layer (~120 services) sitting between controllers and models. Domain-grouped subfolders: Analytics (platform/provider/financial-health/geographic/pricing/outcomes metrics), Finance (currency exposure/alerts), Push (FCM/log drivers), RBAC (custom permission registrar), Travel (path service), Admin (suspension). Flat services cover quotes, bookings, payments/Stripe, promotions, aftercare, translations, notifications, GDPR/deletion, support cases.
- **Modules:** all.
- **FRs:** all (logic layer).
- **Entry points / key files:** `Analytics/PlatformMetricsService.php`, `StripePaymentService.php`, `NotificationDispatchService.php`, `PromotionRedemptionService.php`.

## app/Notifications/ (incl. Notifications/Support/) + app/Mail/ + app/Channels/
- **Purpose:** Outbound notification classes (~70: quotes, bookings, payments, aftercare, reviews, treatment, support, account lifecycle), Mailables (email bodies), and `FcmChannel` custom push channel.
- **Modules:** S-03.
- **FRs:** FR-020, FR-030.
- **Entry points / key files:** `Channels/FcmChannel.php`, `Notifications/NewMessageReceivedNotification.php`, `Mail/NotificationMail.php`.

## app/Events/ + app/Listeners/ + app/Observers/
- **Purpose:** Event-driven side effects. Events (Support/*, MessageSent, IncomingCall, TreatmentCompleted, DisputeResolved) broadcast or trigger Listeners (support timeline/notifications). Observers (Booking/Inquiry/Patient/ProviderUser/Quote) hook model lifecycle for audit & sync.
- **Modules:** S-06 (audit), S-03, A-10.
- **FRs:** FR-012, FR-020, FR-023.
- **Entry points / key files:** `Events/MessageSent.php`, `Listeners/Support/RecordTimelineEventListener.php`, `Observers/QuoteObserver.php`.

## app/Jobs/ (incl. Jobs/Analytics/)
- **Purpose:** Queued background work: analytics aggregation (platform/provider daily metrics, quote-aging snapshot, engagement status), finance & provider analytics export generation, patient deletion processing, email & push dispatch.
- **Modules:** A-08, S-03, A-09.
- **FRs:** FR-014, FR-020, FR-023.
- **Entry points / key files:** `Jobs/SendPushNotificationJob.php`, `Jobs/Analytics/AggregatePlatformDailyMetrics.php`.

## app/Console/Commands/
- **Purpose:** Scheduled/CLI tasks: role activation, quote-expiry checks, payment-due reminders, currency/exchange-rate sync, geo data sync, cleanup of expired tokens/drafts/exports, notification test/trigger, seeders for test data.
- **Modules:** — (operational/infra), S-02, S-03.
- **FRs:** FR-004, FR-020, FR-021, FR-028.
- **Entry points / key files:** `Console/Kernel.php` (schedule definitions), `CheckQuoteExpiry.php`, `SyncExchangeRatesFromAPI.php`.

## app/Enums/ + app/Rules/ + app/Helpers/ + app/Contracts/
- **Purpose:** Supporting primitives. Enums (case status/priority/type, profile type, provider designation, questionnaire context, ticket source). Rules (custom validators: strong password, head-scan payload, date ranges, video duration). Helpers (HtmlSanitizer, UrlHelper). Contracts (PushNotificationDriver interface).
- **Modules:** — (cross-cutting).
- **FRs:** —.
- **Entry points / key files:** `Enums/CaseStatus.php`, `Rules/HeadScanPayloadValidator.php`, `Contracts/PushNotificationDriver.php`.

## app/Providers/
- **Purpose:** Laravel service providers: app bootstrap, auth/policy registration, broadcast, event-listener wiring, image, route binding.
- **Modules:** — (framework infra).
- **FRs:** —.
- **Entry points / key files:** `EventServiceProvider.php`, `AuthServiceProvider.php`, `RouteServiceProvider.php`.

## database/migrations/
- **Purpose:** ~180 schema migrations, the chronological record of the physical DB. Together they realize the entities in `system-data-schema.md`. Read newest dates for recent schema additions.
- **Modules:** all.
- **FRs:** all (schema).
- **Entry points / key files:** browse by date prefix; latest = `2025_11_26_*_create_registration_drafts_table.php`.

## database/factories/ + database/seeders/
- **Purpose:** Model factories (subset: providers, patients, quotes, inquiries, payments, reviews, promotions, translations) and seeders (locations, help-centre, provider billing/team, aftercare data) for tests and local data.
- **Modules:** — (testing / data support).
- **FRs:** FR (testing).
- **Entry points / key files:** `factories/PatientFactory.php`, `factories/QuoteFactory.php`.

## app/Http/Schemas/ + app/Schemas/
- **Purpose:** OpenAPI/Swagger annotation holders (ApiSchemas, TreatmentPlanSchemas, FinancialBillingSchemas) for generated API docs.
- **Modules:** — (docs).
- **FRs:** —.
- **Entry points / key files:** `app/Schemas/ApiSchemas.php`.

## app/requirements/
- **Purpose:** In-repo markdown analysis notes (aftercare cases, in-progress tab, quote/inquiry workflow guides) left by devs — NOT code. Reference only.
- **Modules:** —.
- **FRs:** —.
- **Entry points / key files:** `app/requirements/QUOTE_INQUIRY_STATUS_WORKFLOW_GUIDE.md`.

## Notes / unmapped
- The tech-spec's controller list under `Backend Architecture` is a small illustrative subset; the real controller tree is far larger (this map supersedes it).
- Affiliate logic is split: `Affiliate/` (affiliate-facing) + Admin controllers + `Billing/AffiliatePayoutController` all touch A-07/A-18 flows — trace via the `affiliates` prefix in `api.php`.
- A few root-level controllers (currency-conversion, legal pages) overlap in name with `Settings/` equivalents; confirm the live binding in `api.php` before assuming which is wired.
- FR bindings are best-effort from PRD module codes; treat `—` entries as genuinely cross-cutting/infra.
